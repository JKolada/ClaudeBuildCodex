# 04 — Scripts and Databases

> Commandments IV and V: *Dry-run is the default; the backup is your rollback mechanism.*

## Scripts — the rules

### 1. Dry-run is the default
Every script that **changes data** runs as `--dry-run` by default and prints the plan:
what, how many rows, where. A deliberate `--execute` turns on the mutation. This has saved the
reference project more than once — you see "4 OK, 0 skipped" before anything is written.

```
python -m scripts.x.do_thing            # dry-run: shows the plan
python -m scripts.x.do_thing --execute  # writes
```

### 2. Idempotency
A script run twice should yield the same state, not a doubled one. Write migrations and content loaders
so that `INSERT OR IGNORE` / `UPSERT` make a re-run safe (in the reference project the content
loaders from an external database are explicitly idempotent, and that's a deploy requirement).

### 3. Organize by pipeline stage
Group scripts by phase (`setup/`, `normalize/`, `enrich/`, `validate/`, `images/`,
`dedup/`, `orchestration/`). Leave **compatibility shims** when you move files.
Compose them into **composable pipelines** (`post-scrape`, `full`) — but **keep
catalog-mutating operations OUT of the automatic pipeline** (run dedup/merge by hand:
dry-run → review → `--execute`).

### 4. Log what you did NOT do
If a script truncates scope (top-N, sampling, skipped rows) — **print it**. A silent
truncation reads as "I covered everything" when you didn't.

### 5. Record the environment in the docs
The interpreter, the variables (`PYTHONIOENCODING=utf-8` on Windows), where to get the venv. The agent
doesn't guess the path to Python — it reads it from `CLAUDE.md`.

## Databases and migrations

### Migrations are forward-only
No down-migrations. One numbered file = one step forward. **Rolling back a schema =
restoring the backup**, not a reverse migration. Therefore:

### Back up BEFORE every schema/data change on prod
```bash
sqlite3 data/app.db ".backup backups/pre-deploy-$(date +%F_%H%M%S).db"
```
This isn't caution — it's the *undo mechanism*. Keep a retention window (e.g. 14 days) and name the
snapshots legibly (`pre-deploy-*`, `pre-swap-*`, `replaced-prod-*`).

### Additive > destructive
`ADD COLUMN` is backward-compatible (old code still works). **Never DROP/RENAME a
column in the same migration where running old code still uses it** — split the destructive
change into a later deploy, once nothing reads the column anymore.

### Integrity after the fact
After every data operation: `PRAGMA integrity_check` + `PRAGMA foreign_key_check` +
count the rows. Distinguish **pre-existing noise** (orphaned staging rows present both before and after)
from a **regression** (new violations that weren't there before). In the reference project the merged DB
had *fewer* violations than the local one — a signal that the migration cleaned up rather than broke things.

### "Active row" model instead of overwriting
A pattern from prices: instead of an in-place UPDATE, **expire** the old row (`expired_at`) and insert
a new one; a partial unique index enforces "one active per key". History is preserved and the audit trail
comes for free. Consider this model anywhere history has value.

### Make a transfer snapshot with `.backup` / `VACUUM INTO`, not `cp` on a live file
A live SQLite with WAL copied via `cp` can be inconsistent. `.backup` (online-safe) or
`VACUUM INTO` give a consistent, defragmented copy. **Never SCP a live `.db`.**

## Anti-patterns
- 🚫 A mutating script without `--dry-run`.
- 🚫 A deploy with a migration but no backup "because it's additive".
- 🚫 DROPping a column used by running code.
- 🚫 `cp app.db` with the server running → an inconsistent snapshot.
- 🚫 Wiring a catalog-mutating operation into the automatic pipeline.

## In practice
- Relational database → forward-only migrations + a backup before each one.
- **A pipeline processing sensitive data** (e.g. anonymization / distilling submissions) = a separate,
  idempotent script with dry-run; the contract: raw data in, **PII-free data** out,
  with a test that re-identification is impossible. Keep it OUT of the user-facing path. →
  [09](09-law-and-protecting-the-creator.md), [11](11-data-model-and-normalization.md)
