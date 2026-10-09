# Local setup (copy to local.md beside SKILL.md and fill in; local.md is never committed)

Everything here is optional: the skill runs without this file and asks for what it needs.

- **Gemini key file:** `<path to the .env holding GEMINI_API_KEY=...>`. Pass it as `--env` to `gemini_image.py` or set
  `MAHORAGA_ENV` to it when running the Gemini scripts. Leave this out if `GEMINI_API_KEY` is already set in your
  environment. Say whether test generations need asking first.
- **Git identity:** `<name>` / `<email>` for commits made as you (else the repo's own git config is used).
- **Vercel:** your usual scope slug, and any scope the CLI can deploy to that `vercel teams ls` does not list.
- **Off limits:** folders or files never to open.

## Where past projects live

| Project | Folder |
|---|---|
| `<name>` | `<path>` |

Borrowed scripts take folders from environment variables named in their docstrings: `SITE_DIR`, `RAW_DIR`,
`WORK_DIR`, `FRAMES_DIR`, `FONTS_DIR`, `MEETS_REPO`, `AVATARS_DIR`, `PEOPLE_DIR`.
