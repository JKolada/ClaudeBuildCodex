# 05 — Git and Deployments

> Commandments II, VI, VII, VIII, IX. The densest chapter, because a mistake here is the most expensive.

## Git — two habits for most tasks

### A. Search the history BEFORE you implement
```bash
git log --oneline -- <path>           # history of a file/directory
git log -S"symbol" --oneline          # pickaxe: where a symbol/flag/column was born
git log -G"regex" --oneline           # commits whose DIFF matches the regex
git log --grep="word" --oneline       # search commit messages (that's where features are described)
git blame <file> -L a,b               # who/when/why
git show <commit>                     # the full change + context
```
Combine this with a grep over the tree + the directory's `AI_README.md`. History + code + docs = the full
picture in a minute. It pays off with: unfamiliar code, a hunch of "haven't we done this
already?", a column/flag of unknown origin, dating a regression, and before every refactor.

### B. A clean, coherent `git status`
- **Separate unrelated changes** into distinct commits (one topic = one commit).
- **Catch junk early:** `.bak`, temp files, accidental databases (`web/_Proj…db`),
  a file named `-w` from a botched `curl`. Add the patterns to `.gitignore` (note: gitignore
  **has no inline comments** — put the `#` on its own line).
- **Tell a real diff from CRLF noise:** `git status` shows a file as changed but
  `git diff HEAD` is empty → it's only EOL, not work. Don't commit the noise.
- **Orphans (uncommitted work in the background)** — in a project run across multiple sessions
  ("user + Claude"), other sessions leave changes in the tree. Before a deploy: is this real, complete
  work (commit/confirm it), or a WIP/experiment (leave it)? **Don't sweep someone else's uncommitted work
  into a deploy without confirmation.**

### What finishes a commit
- Messages in English, descriptive (what + why), `fixes #N`/`refs #N` to the issue.
- Link the PR/issue with the full URL, not "PR #123".

## Teamwork: issues and simple branches

> Solo on `main` with commit discipline is enough. **From the second person** onward you need two
> things: a **shared task list** (issues) and **lightweight branching** — so you don't step on each
> other and "who's doing what" stays visible.

### Issues = units of work (one source of "what and why")
- **One task = one issue.** Title = the outcome ("Cart drops items after refresh"), body = context,
  acceptance criteria, links. This is where the **why** lives — not in your head, not in chat.
- **The issue number ties the work together:** branch, commits (`refs #N`), PR, and discussion.
  `fixes #N` in the PR **closes** the issue on merge (→ "What finishes a commit").
- **Issue before code** for anything non-trivial or someone else's report — so scope and decision are
  written down before a diff exists. Small, concrete issues > one big "epic for everything".
- **The backlog is a list, not memory.** Labels (`bug`/`feat`/`chore`, priority); close what's stale.
  An issue dead for weeks = a decision to make (do it / drop it), not a zombie.

### Simple branches (small teams, trunk-based)
- **`main` is always deployable.** In multi-person work, don't commit straight to `main` — it's the
  shared table holding what goes to prod.
- **A short branch per task:** `feat/NN-cart`, `fix/NN-login` (NN = issue number). It lives
  **hours–days, not weeks** — the longer it lives, the more painful the merge.
- **A small PR > a big PR.** One topic, reviewable in fifteen minutes. Nobody reads a giant PR
  carefully — it passes "on trust", i.e. without review.
- **Merge, then delete the branch.** Once it's in `main`: delete the branch, pull `main`, start the
  next one fresh. Stale branches are debt and a lie about the project's state.
- **Sync with `main` often** (merge/rebase into your branch) — small, frequent conflicts instead of
  one giant conflict at the end.

> **Review isn't a formality — it's a second pair of eyes before prod.** On a team every PR has a
> reviewer; solo, the "reviewer" is a deliberate second pass over the diff (and Claude as devil's
> advocate). A change lands on `main` reviewed, not "because it works on my machine".

### Anti-patterns
- 🚫 Committing straight to `main` while someone else is in the project → their work lands on a half-done state.
- 🚫 A long-lived "my big refactor" branch → merge hell and weeks of drift from `main`.
- 🚫 Working without an issue → scope and the "why" vanish; a month later nobody knows why it exists.
- 🚫 `fixes #N` in a commit to a work branch → the issue closes prematurely (the **PR/merge** closes it, not every commit).
- 🚫 An "everything at once" PR → review becomes fiction, regressions slip through.

## Deployments — THE OVERRIDING POLICY

> ⛔ **Never deploy to prod automatically.** `git pull` on the server, `pm2 reload`,
> a database swap, `migrate.py` on prod, the maintenance flag — **only when the user says so
> explicitly** ("ship it", "deploy"). You may **proactively propose** a deploy when it's ready — but
> you wait for an explicit "yes". Commit + push on request is **not** a deploy. This rule beats "auto mode".

### Two deploy types
- **Code-only (no migrations/dependencies)** → zero-downtime: `git pull` + `pm2 reload`.
- **With a migration/dependency change/database swap** → a **maintenance window** (nginx flag → 503 +
  branded page), a few seconds of downtime, a guarantee the app isn't running on a half-migrated schema.

### Tag EVERY deploy
```bash
git tag -a deploy-$(date +%F) -m "What goes to prod: <one sentence>"   # -2/-3 for the next one that day
git push --tags
```
- What's live: `git describe --tags --abbrev=0 --match 'deploy-*'`.
- Rollback of code: `git checkout <deploy-tag> && pm2 reload`.
- Rollback of schema: restore the backup (forward-only!).

### A changelog with every deploy
A public "What's new" — **in plain language, no jargon** (no scraper/migration/commit). Write
**what the user gains**. Bump the `updated:` date. It's part of the deploy checklist, not optional.

---

## Database swap preserving accounts — the runbook (the hardest operation)

A full swap of the prod database (e.g. a local catalog with all the work) **while preserving live
accounts**. This is where most of the traps lie. Lessons from the reference project:

### Rules that save user data (Commandment VII)
1. **"Users" is many tables, not one `users`.** Enumerate **every** table with an FK to the
   user: accounts, carts, reviews, likes, badges, games, chat (sessions +
   messages + limits), feedback, sessions. Map a table without `user_id` (e.g. `chat_messages`)
   through its parent (`session_id`). Gate each one on the existence of the column/table.
2. **Map by a STABLE key (slug), not by ID.** `product_id` drifts between
   databases after merges — a user's review must land via `slug → new_id`, and a missing
   slug is **skipped and logged**, not pushed in blindly.
3. **The source of truth for accounts is LIVE prod**, not an old snapshot — so you don't lose
   registrations from the last hour. Run the migration **in the maintenance window, after `pm2 stop`**,
   reading the stopped, consistent prod database.
4. **FK-safe order**: WIPE children before parents, INSERT parents before children
   (e.g. `reviews` before `review_likes`; `chat_sessions` before `chat_messages`).
5. **Back up live prod BEFORE the swap** (`.backup replaced-prod-<ts>.db`) — that's your rollback.
6. **Verify the merged database**: account count = prod, 0 dangling reviews (slug-remap OK),
   `integrity_check: ok`, FK violations ≤ the pre-existing state (no more).
7. **Sessions are separate, ephemeral state — don't mix them into the swapped database.** Keep the session
   store in a **separate file** (e.g. `sessions.db`) from the catalog database you sometimes swap wholesale —
   otherwise the swap zeroes out logged-in users. An in-process memory store logs everyone out on **every**
   restart/deploy and leaks memory (→ [14](14-operational-resilience.md)).

### The sequence (non-invasive phase → window → finalization)
**Phase 1 (the service is live):**
- push code to GitHub;
- **copy gitignored images/assets separately** (rsync or tar-over-ssh, **not** through git),
  BEFORE the window — they're inert until you swap the database. Send only the delta (count what's missing).
- pre-upload a clean catalog snapshot to the server (`/tmp`).

**Phase 2 (maintenance window, a dozen-odd seconds), atomically (`set -e`):**
`flag ON → git pull → pm2 stop → back up live prod → migrate-users (source = prod) →
swap the file (rm wal/shm, mv, PRAGMA journal_mode=WAL) → pm2 start → SMOKE TEST → flag OFF`.

**Phase 3:** tag `deploy-…-2` + push, FB/SEO re-scrape if applicable, clean up `/tmp` and local temp.

### Smoke test after the swap (before you drop the flag)
Via `localhost` (bypasses the nginx maintenance): home/catalog/detail → 200, og:image →
the right file, redirects (e.g. merged → 301 to the survivor), numbers in the database (accounts/records),
**`pm2 logs` for errors**. If you find a trivial, safe bug — fix it in the window and ship it
(commit → pull → reload) instead of releasing a known 500.

### Gitignored assets and the deploy
Images/files that are in `.gitignore` **don't ride along with `git pull`**. Either sync them
(rsync/tar) or generate them on the server (if it has the tooling). In the reference project the call was
**to copy from local**, because the server has no Pillow and the swap changes the catalog.

## Anti-patterns
- 🚫 Auto-deploy / "it's ready, so I'm shipping it".
- 🚫 A swap "except accounts" = only `users` → loss of reviews/badges/chat.
- 🚫 Mapping user data by ID instead of slug → reviews land on the wrong product.
- 🚫 A migration on an old snapshot → loss of fresh registrations.
- 🚫 No deploy tag → "what's live?" becomes a guessing game.
- 🚫 Transferring 1.5 GB of assets **inside** the maintenance window → long downtime (do it before the window).
- 🚫 Sessions in a swapped database (or in process memory) → the deploy logs everyone out.
- 🚫 A deploy-script invariant left untested — e.g. `$(date)` expanded once at file-creation time
  (so every backup overwrites the same file). Lock the deploy script's invariants down with a test.

> **The runbook is the memory of incidents, not your head.** Every prod failure → an entry in the runbook
> with a date and a numbered lesson (e.g. "never SCP a live `.db` — use `.backup`; WAL holds fresh pages").
> The next swap reads the runbook, doesn't repeat the mistake (→ [06](06-collaboration-and-memory.md), [14](14-operational-resilience.md)).

## Shared infrastructure
Projects can share a single **Hetzner VPS**: static sites (a `dist/` build) go via
`scp`/`rsync` + an nginx vhost; Node apps via `git pull` + `pm2 reload` behind
nginx. One server = a shared `backups/` directory and the same habits (deploy tag, maintenance
flag). A new project on the same box: a separate vhost + a separate directory, the same rules.

## In practice
Deploy the critical path (e.g. login) with a test and a full smoke (registration, login,
logout, session persistence). At the first real user traffic, set up immediately: a nightly database
backup, deploy tagging, a branded maintenance page. → [03](03-testing-and-verification.md)
