# The Slack app

## Create it

1. Go to https://api.slack.com/apps, choose **Create New App**, then **From a manifest**, pick the workspace and paste `template/slack-manifest.yaml`. Rename `agent-bot` if you like.
2. Under **Basic Information**, open **App-Level Tokens** and generate a token with scope `connections:write`. That is `SLACK_APP_TOKEN` (`xapp-…`).
3. Under **Install App**, install it to the workspace. Then under **OAuth & Permissions**, copy the **Bot User OAuth Token**. That is `SLACK_BOT_TOKEN` (`xoxb-…`).
4. In the channel, `/invite @agent-bot`. Private channels work too, through `groups:history`.
5. Find the ids:
   - **Channel id:** open the channel details; it's at the bottom (`C…`).
   - **Your user id:** your profile, then **⋯**, then **Copy member ID** (`U…`).
   - **Bot user id:** `doctor.py` prints it from `auth.test`.

## Scopes and why

| Scope | For |
|---|---|
| `channels:history`, `groups:history` | receiving messages and reading whole threads for context |
| `app_mentions:read` | mention events (ignored; messages carry the tag too) |
| `chat:write` | replies, progress lines and outcomes |
| `files:read` | downloading screenshots and CSVs people attach |
| `files:write` | attaching CSVs and reports to the thread (otherwise they are pasted) |
| `users:read` | optional; for resolving names if you extend the bot |

After changing scopes, **reinstall** the app, or the token keeps its old scopes.

## Events

`message.channels` and `message.groups`, delivered over Socket Mode. You don't need a Request URL. If messages never arrive, check that Socket Mode is on, the event subscriptions are saved, and the bot is in the channel.

## Etiquette the bot follows

- It always replies in a thread, never at the top level.
- It acknowledges within seconds with something specific, posts a progress line every 10 minutes at most, then gives the outcome.
- Long answers are split on paragraph breaks into several messages, never cut off.
- It never uses `@channel`, and never DMs people.
