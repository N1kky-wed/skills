#!/usr/bin/env bash
# Combine one or more PR branches with the latest main in a scratch worktree and run the
# project's safe test command there. Nothing is pushed or merged.
#   integrate.sh <branch> [branch ...]
# Configure via env vars, or a file <repo>/.claude/agent-profile.env that sets them:
#   REPO       repo checkout to branch from              (default: git toplevel of $PWD)
#   MAIN       main branch name                          (default: origin's HEAD, else main)
#   WT         scratch worktree path                     (default: <repo>/../wt-integ-scratch)
#   TEST_CMD   command run inside the worktree; must exit non-zero on failure (required unless
#              auto-detected: npm test / pytest / go test / cargo test)
#   SYNTAX_CMD optional quick check run before tests (e.g. "npx tsc --noEmit")
# Exit 0 only if every merge was clean and the checks passed.
set -uo pipefail
[ $# -ge 1 ] || { echo "usage: $0 <branch> [branch ...]" >&2; exit 2; }

REPO=${REPO:-$(git rev-parse --show-toplevel 2>/dev/null)}
[ -n "$REPO" ] || { echo "run inside the repo or set REPO" >&2; exit 2; }
[ -f "$REPO/.claude/agent-profile.env" ] && . "$REPO/.claude/agent-profile.env"
MAIN=${MAIN:-$(git -C "$REPO" symbolic-ref --short refs/remotes/origin/HEAD 2>/dev/null | sed 's#^origin/##')}
MAIN=${MAIN:-main}
WT=${WT:-$(dirname "$REPO")/wt-integ-scratch}

if [ -z "${TEST_CMD:-}" ]; then
  if   [ -f "$REPO/package.json" ];   then TEST_CMD="npm test --silent"
  elif [ -f "$REPO/pyproject.toml" ] || [ -f "$REPO/pytest.ini" ]; then TEST_CMD="python -m pytest -q"
  elif [ -f "$REPO/go.mod" ];         then TEST_CMD="go test ./..."
  elif [ -f "$REPO/Cargo.toml" ];     then TEST_CMD="cargo test --quiet"
  else echo "set TEST_CMD (no test runner detected); exclude tests that touch real systems" >&2; exit 2; fi
  echo "TEST_CMD auto-detected: $TEST_CMD  (check the project profile excludes live tests)"
fi

git -C "$REPO" fetch -q origin || exit 1
git -C "$REPO" worktree remove --force "$WT" 2>/dev/null
git -C "$REPO" branch -D integ/scratch >/dev/null 2>&1
git -C "$REPO" worktree add -q -b integ/scratch "$WT" "origin/$MAIN" || exit 1
cd "$WT" || exit 1

for b in "$@"; do
  if git merge -q --no-edit "origin/$b" >/dev/null 2>&1; then echo "merged: $b"
  else
    echo "CONFLICT merging $b in:"; git diff --name-only --diff-filter=U | sed 's/^/  /'
    echo "Resolve in $WT (git add, then git commit --no-edit), then re-run the checks by hand."; exit 3
  fi
done

ok=1
if [ -n "${SYNTAX_CMD:-}" ]; then bash -c "$SYNTAX_CMD" || { echo "syntax/lint check failed"; ok=0; }; fi
bash -c "$TEST_CMD" || ok=0
echo "integration $(git rev-parse --short HEAD) on $MAIN: $([ $ok = 1 ] && echo PASS || echo FAIL)"
[ $ok = 1 ]
