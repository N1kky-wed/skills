# VPS setup (Ubuntu / Debian)

Two vCPUs, 4 GB RAM and 20 GB disk are enough for 2 workers on a small or medium repo. A big monorepo with heavy installs wants 8 GB. No inbound ports are needed, because Socket Mode is outbound only.

## 1. A dedicated user

```bash
sudo adduser --disabled-password --gecos "" bot
sudo -iu bot          # everything below runs as `bot` unless it says sudo
```

## 2. Toolchain

```bash
sudo apt update && sudo apt install -y git python3 python3-venv rsync jq postgresql-client
# Node via nvm (the claude CLI is an npm package)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
source ~/.bashrc && nvm install --lts
npm install -g @anthropic-ai/claude-code
# GitHub CLI
sudo apt install -y gh    # or the official apt repo for a newer version
```

Also install whatever the repo needs to run its tests: pnpm (`corepack enable`), Python, Go, Docker and so on. If the repo pins versions, match them.

## 3. Log in

**Claude.** Pick one option.

- **Interactive login, stored in `~/.claude`:** run `claude`, follow the login, then `/exit`. Works with a Pro, Max or Team subscription.
- **Long-lived token:** run `claude setup-token` on any machine and put the result in `.env` as `CLAUDE_CODE_OAUTH_TOKEN=…`.
- **API key:** put `ANTHROPIC_API_KEY=…` in `.env`. Billing is per token, so set a spend limit.

Check that it works headlessly:

```bash
claude -p "reply with ok"
```

**GitHub.**

```bash
gh auth login            # HTTPS; paste a fine-grained token scoped to the one repo
gh auth setup-git        # so plain `git push` uses the same credential
git config --global user.name  "agent-bot"
git config --global user.email "agent-bot@users.noreply.github.com"
```

The token needs Contents read/write, Pull requests read/write, Issues read/write (for `BOT_OPEN_ISSUES`) and Metadata read. Nothing else.

## 4. Install the bot

```bash
git clone https://github.com/<you>/skills ~/skills     # or wherever this skill lives
bash ~/skills/skills/slack-agent-bot/scripts/install.sh ~/slack-agent-bot
cd ~/slack-agent-bot
nano .env                 # fill it in (see .env.example), then:
chmod 600 .env
bash ~/skills/skills/slack-agent-bot/scripts/install.sh ~/slack-agent-bot   # again: clones the repo now REPO_SLUG is set
nano context.md           # what the agents should know about the project
.venv/bin/python doctor.py
.venv/bin/python -m unittest discover -s tests
```

## 5. Run as a service

```bash
sudo cp ~/slack-agent-bot/slack-agent-bot.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now slack-agent-bot
journalctl -u slack-agent-bot -f
```

To let the bot user restart its own service without a password, for example for a teammate operating it through Claude:

```bash
echo 'bot ALL=(root) NOPASSWD: /bin/systemctl restart slack-agent-bot, /bin/systemctl status slack-agent-bot' \
  | sudo tee /etc/sudoers.d/slack-agent-bot
```

## 6. Upgrading

Pull the skills repo and re-run `install.sh`. It keeps `.env`, `context.md`, `voice.md`, the state and the checkout. Then check `bin/botctl status` and restart once nothing is in flight.

## Notes

- **nvm paths.** systemd does not read `~/.bashrc`. `install.sh` writes the directory holding `claude` into the unit's `PATH`. After a Node upgrade, re-run `install.sh`, copy the unit again and run `daemon-reload`.
- **Disk.** Each running job holds a full worktree, plus `node_modules` and the like. pnpm or uv caches make that cheap after the first install. Prune `out/` occasionally.
- **Time zone.** Set `timedatectl set-timezone …` if people will read timestamps in the logs.
