<!-- What the agents should know about your project. Delete this comment and
fill in. Keep it short and factual; it is pasted into every prompt.
Never put secrets here (this file is read by agents and may be quoted). -->

What the product is, in two lines.

Where the data lives and how to read it, e.g.:
    dbq main "select count(*) from users where created_at > now() - interval '7 days'"
    tables: users(id, email, created_at, plan), orders(id, user_id, total, created_at)

Conventions worth repeating (the repo's CLAUDE.md / AGENTS.md are read anyway).

What the bot must never do here (e.g. "never email customers").
