#!/usr/bin/env bash
# Set the bot up on a VPS (Ubuntu/Debian). Idempotent: safe to re-run.
#
#   bash install.sh /home/bot/slack-agent-bot
#
# Copies the template there (keeping an existing .env and state), makes the
# venv, installs the systemd unit, and runs doctor. Does NOT start the service
# until doctor passes.
set -euo pipefail
HERE="$(cd "$(dirname "$0")/.." && pwd)"
ROOT="${1:-$HOME/slack-agent-bot}"
USER_NAME="$(id -un)"

command -v python3 >/dev/null || { echo "need python3 (apt install python3 python3-venv)"; exit 1; }
command -v git >/dev/null || { echo "need git"; exit 1; }

mkdir -p "$ROOT"
# rsync keeps the operator's .env, voice/context edits, state and repo.
rsync -a --exclude .env --exclude state --exclude repo --exclude work --exclude out --exclude in --exclude __pycache__ \
  $( [[ -f "$ROOT/voice.md" ]] && echo --exclude voice.md ) \
  $( [[ -f "$ROOT/context.md" ]] && echo --exclude context.md ) \
  "$HERE/template/" "$ROOT/"
[[ -f "$ROOT/.env" ]] || { cp "$ROOT/.env.example" "$ROOT/.env"; chmod 600 "$ROOT/.env"; echo "created $ROOT/.env: fill it in"; }

python3 -m venv "$ROOT/.venv"
"$ROOT/.venv/bin/pip" install -q --upgrade pip
"$ROOT/.venv/bin/pip" install -q -r "$ROOT/requirements.txt"

# The repo checkout the bot works on.
SLUG="$(grep -E '^REPO_SLUG=' "$ROOT/.env" | cut -d= -f2- || true)"
if [[ -n "$SLUG" && "$SLUG" != your-org/your-repo && ! -d "$ROOT/repo/.git" ]]; then
  gh repo clone "$SLUG" "$ROOT/repo" || git clone "https://github.com/$SLUG" "$ROOT/repo"
fi

CLAUDE_DIR="$(dirname "$(command -v claude || echo /usr/local/bin/claude)")"
SVC_PATH="$ROOT/bin:$CLAUDE_DIR:/usr/local/bin:/usr/bin:/bin"
sed -e "s#__USER__#$USER_NAME#g" -e "s#__ROOT__#$ROOT#g" -e "s#__HOME__#$HOME#g" -e "s#__PATH__#$SVC_PATH#g" \
  "$ROOT/systemd/slack-agent-bot.service" > "$ROOT/slack-agent-bot.service"

echo
echo "next:"
echo "  1. fill in $ROOT/.env (and context.md, voice.md)"
echo "  2. cd $ROOT && .venv/bin/python doctor.py"
echo "  3. sudo cp $ROOT/slack-agent-bot.service /etc/systemd/system/"
echo "     sudo systemctl daemon-reload && sudo systemctl enable --now slack-agent-bot"
echo "  4. journalctl -u slack-agent-bot -f   and tag the bot in its channel"
