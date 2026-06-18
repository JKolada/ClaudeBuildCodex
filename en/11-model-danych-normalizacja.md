# 11 — Data model and normalization

> Commandments V and VII at the root: *a backup is a rollback, user data inviolable* — but before
> you safeguard anything, it must have a **shape** in which change is cheap and predictable.

The schema is **the contract of the whole system**. Scrapers, web, pipelines, migrations — everything rests
on it. A poorly normalized model takes its revenge on every layer: duplicate data drifts,
mappings on an unstable key lose records, computed values diverge from one another.
Normalize first; denormalize **deliberately** and with a named source of truth.

## Normalize first
- **No repeating groups.** A value once, in one place.
- **Vocabularies in lookup tables.** In the reference project: `countries` / `regions` / `product_types` /
  `tag_types` — not free-text in a column. Plus a **`CHECK` on `products.type`**
  (`type_a | type_b | type_c | …`) — the database rejects garbage before it gets in.
- **Junction tables for M:N.** A product has many tags/attributes → **`product_tags`** (junction),
  not `primary_tag` + `secondary_tag` as two free-text fields (those were dropped by migration 090 —
  the junction is the sole store of attributes).

## Stable keys — slug, not ID
**IDs drift.** After duplicate merges `product_id` changes (the canonical row absorbs the rows,
the duplicate one disappears). That is why **the stable identifier is the slug**, not the numeric key.
The hardest lesson from the reference project — the prod-database swap: **you map user data by slug → new ID**,
never by the old ID (a review would land on the wrong product). A missing slug you **skip and log**,
you don't push it through blindly. → [05](05-git-i-wdrozenia.md)

## Active-row instead of overwriting
A pattern from prices, worth carrying everywhere history has value:
- An **`expired_at`** column (NULL = active). A price change → you expire the old row, insert a new one.
- A **partial unique index** `WHERE expired_at IS NULL` — enforces "one active per key"
  (one active price per (product, retailer)).
- A **history table** (`price_history`) records every price ever seen.
- The effect: **audit for free** — you know what changed and when, without triggers.

## When to denormalize (deliberately)
Denormalization is legal **for reads** — but always name the **source of truth** and guard consistency:
- **Displayed/computed fields → compute in helpers, don't store.** `display_name` (brand + variant +
  edition name) computed dynamically in `web/src/helpers.js`. Stored, it would drift after every
  change to a component.
- **A denormalized cache with a clear source.** `ext_profile_cache` holds data from an external source; the
  `ext_*` columns **were removed from `products`** (migration 051) — the cache is the sole source, no two truths.
- **A snapshot with a live fallback.** `site_stats.json` is a dump of numbers (products/prices/retailers);
  read by the home page, but with a **fallback to the live database** when the snapshot is stale.

## Migrations and integrity
- **Forward-only + additive** — `ADD COLUMN` is backward-compatible; **never DROP/RENAME
  a column used by working old code** (→ [04](04-skrypty-i-bazy-danych.md)).
- **FK integrity check** after every operation (`PRAGMA foreign_key_check`).
- **Gating on column existence** — the script checks whether a column/table exists before it
  operates on it (survives different schema states between environments).

## The schema as a documented contract
ERD + controlled vocabulary in docs (e.g. `db_schema.md` with a Mermaid ERD,
`data_model_reference.md` with the allowed values for `type`/`region`/`tag_types`). A schema
nobody documented is a schema the next session guesses. → [01](01-dokumentacja-i-ai-readme.md)

## Anti-patterns
- 🚫 **Free-text where there should be a lookup** (country as a string → 5 spellings of "USA"/"U.S.A."/"United States").
- 🚫 **A duplicated source of truth without synchronization** (external data in `products` *and* in the cache → divergence).
- 🚫 **Mapping user data by a mutable ID** instead of the slug → a review on the wrong product.
- 🚫 **Storing a computed value that drifts** (`display_name` as a column).
- 🚫 **A destructive migration under working old code** (DROP of a column the web still reads).
- 🚫 Two free-text fields instead of a junction table for an M:N relation.

## In practice
When you declare privacy, **the data model must enforce it**. Separate the paths: user-facing
data and a separate, idempotent processing pipeline, operating **exclusively on anonymized
data** (PII removed *before* processing). The claim "we don't read the data" must
follow from the **schema and the script's contract**, not from copy — and have a **re-identification test** that
proves identity cannot be reconstructed. → [04](04-skrypty-i-bazy-danych.md), [09](09-prawo-i-ochrona-tworcy.md)
