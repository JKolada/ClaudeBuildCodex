# 00 — Decalogue

The core of the doctrine. If you read only one file from this set — make it this one.
Each commandment is expanded in a later chapter.

---

### I. Document for the agent, not for the archive.
Every directory has an `AI_README.md`. You update it **before** the commit, not "someday."
Documentation read before touching the code saves hours of re-derivation;
documentation tacked on afterwards ("I'll document at the end") drifts away from the code and starts
to lie — because the context has already evaporated, and "the end" never comes. → [01](01-dokumentacja-i-ai-readme.md)

### II. Search the history before you write a single line.
`git log -S"symbol"`, `git log --grep`, `git blame`, the directory's AI_README. Most
"new" problems someone has already solved in this repo — a helper exists, there was a migration, there's a
reason the code has this shape. Re-derivation costs more than a minute of searching. → [05](05-git-i-wdrozenia.md)

### III. Verify, don't declare.
You don't write "it works" — you show **proof**: a smoke test, an HTTP status code, numbers, a screenshot.
If tests fail — you say so, with the output. If a step was skipped — you say it was skipped.
Trust is built on an honest report, not on optimism. → [03](03-testowanie-i-weryfikacja.md)

### IV. Dry-run is the default; `--execute` is deliberate.
Every script that changes data first **shows its plan** (what, how much, where). You run the
mutation only after reading that plan. A script with no dry-run mode is a weapon with no
safety catch. → [04](04-skrypty-i-bazy-danych.md)

### V. The backup is a rollback mechanism, not a precaution.
Migrations are **forward-only** (no down-migrations). A snapshot **before** every schema or data
change on prod. Reverting the schema = restoring the backup. The backup isn't
"just in case" — it's the *only* way back. → [04](04-skrypty-i-bazy-danych.md)

### VI. Prod is sacred — you don't touch it without an explicit "deploy."
Commit and push on request are **not** a deploy. `git pull` on the server, `pm2 reload`, a database
swap, the maintenance flag — only when the user says so outright. Always confirm irreversible,
"outward-facing" actions (publishing, sending, deleting). Consent in one context
does not carry over to the next. → [05](05-git-i-wdrozenia.md)

### VII. User data is inviolable.
When swapping the database: enumerate **every** table with an FK to the user (accounts, reviews, carts,
badges, games, chat, sessions), map user data by a **stable key** (slug), not by ID
(IDs drift across merges), the source of truth for accounts is **live prod**, and afterwards
run `integrity_check` and count the rows. → [05](05-git-i-wdrozenia.md)

### VIII. Tag every deploy and write what the user gained.
An annotated tag (`deploy-YYYY-MM-DD`) is the only stable marker of "what's live" and the basis for
rollback. With every deploy, update the public changelog — **in plain language, without
jargon** (no "scraper/migration/commit"; write what the user gains). → [05](05-git-i-wdrozenia.md)

### IX. Small, coherent commit; one topic.
Split unrelated changes into separate commits. Keep `git status` clean — catch junk
(`.bak`, temp files, stray databases) and orphans (uncommitted work in the background)
**early**, before they sneak into a deploy. Tell a real diff from CRLF noise. → [05](05-git-i-wdrozenia.md)

### X. Plan → iterate → review.
First show a plan or a sketch (3 examples, not 100). Gather feedback. Only then
scale. **Verify numbers** at the source. Deliver UX with **warmth** in how it's received, not just
correctness — the product should be pleasant, not merely functional. → [06](06-wspolpraca-i-pamiec.md)

---

## Seven deadly sins (what NOT to do)

1. **Inflated optimism in the report** — "everything works" with no proof. (breaks III)
2. **Mutation without a plan** — running a data-changing script straight with `--execute`. (breaks IV)
3. **Auto-deploy** — "it's ready, so I'll push it to prod." (breaks VI)
4. **An "everything but accounts" DB swap treated as a single `users` table** — losing reviews/badges/chat, because not all FK tables were enumerated. (breaks VII)
5. **Junk-drawer commit** — unrelated changes + artifacts in one commit. (breaks IX)
6. **Scaling before review** — generating 500 items before the user saw 3. (breaks X)
7. **Documentation "later"** — the code ships, the AI_README lags behind, the next session wanders. (breaks I)

---

## The golden rule of altitude

> **Slow where a mistake is expensive (prod, user data, schema). Fast where it's
> cheap (local experiment, UI sketch, dry-run).** Match your pace to the cost of error, not to
> your impatience.
