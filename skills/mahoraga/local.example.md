# Local setup (copy to local.md and fill in; local.md is not committed)

- **Gemini key:** `GEMINI_API_KEY` in `<path to your .env>`. Pass `--env` to `gemini_image.py` or set `MAHORAGA_ENV`.
  Say whether test generations need asking first.
- **Git identity:** `<name>` / `<email>` for commits made as you.
- **Vercel:** your usual scope slug, and any scope the CLI can deploy to that `vercel teams ls` does not list.
- **Off limits:** folders or files never to open.

## Where past projects live

| Project | Folder |
|---|---|
| `<name>` | `<path>` |

Borrowed scripts read folders from `MEETS_REPO`, `SITE_DIR`, `PEOPLE_DIR` and `AVATARS_DIR`.
