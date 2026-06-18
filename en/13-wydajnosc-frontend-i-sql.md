# 13 — Performance: frontend and SQL

> Commandment III in pure form: *verify, don't declare* — applied to speed.
> "Feels faster" doesn't exist. **Before/after numbers** exist.

Performance isn't a hunch, it's a measurement. The most common optimization mistake: guessing what's
slow and "fixing" it without proof it was the problem. Measure **first**, fix what the metric points
to, and **prove with a number** that you improved it. Performance is also SEO (Core Web Vitals
→ [10](10-seo-i-tlumaczenia.md)) and cost (a faster query = a cheaper server → [12](12-elastycznosc-i-skalowalnosc.md)).

## Measure first
- **Lighthouse / Core Web Vitals**: LCP (largest contentful paint), CLS (layout shift),
  INP (interaction), TBT. These are hard numbers, not impressions.
- **Before/after, not "feels faster."** E.g. home-page optimization: preload hero,
  GPU-promoted animations, `content-visibility: auto` below the fold; you report LCP before and after,
  not "probably lighter." → [03](03-testowanie-i-weryfikacja.md)
- **SQL: `EXPLAIN QUERY PLAN`** tells you whether a query uses an index or scans the whole table.

## Frontend
- **Code-splitting** + **lazy-load below-fold** — don't load what the user can't see.
- **Images**: WebP (e.g. convert everything to WebP q=95), responsive `srcset`,
  **preload hero** (LCP), the rest lazy.
- **Fonts**: self-host (e.g. Playfair/Outfit, as on jakub.solutions), `font-display: swap` — text
  visible before the font arrives.
- **`content-visibility: auto`** on sections below the fold — the browser skips rendering what's offscreen.
- **GPU-promoted animations** (`translateZ(0)`/`transform`) instead of layout-triggering properties.
- **Static caching**: `immutable` + long `max-age` in prod (e.g. 7 days immutable in prod).
- **Cache-busting per deploy**: since CSS/JS are `immutable`, append `?v=<git-short-hash>` to
  every link — each deploy changes the URL → fresh fetch. Without it the user sees the **old app**
  (broken layout) until a hard refresh (→ [05](05-git-i-wdrozenia.md)).
- **Streaming / SSE for chat** — the LLM response **token-by-token** (e.g. via SSE), the user sees
  the first words right away instead of a blank screen until generation finishes. → [08](08-stack-i-technologie.md)
- **Server-side pagination** — never ship the whole catalog to the browser (e.g.
  server-side pagination for a few thousand items).

## SQL
- **Indexes** on columns in `WHERE` and `JOIN` — a hot query without an index is a full table scan.
- **Partial indexes** — e.g. `uniq_prices_active … WHERE expired_at IS NULL` (an index
  only on active prices — smaller, faster, enforces uniqueness, → [11](11-model-danych-normalizacja.md)).
- **`EXPLAIN QUERY PLAN`** before and after adding an index — proof the plan changed.
- **Avoid N+1** — no query in a loop per row; batch/join in one shot.
- **`SELECT` only the columns you need** — not `SELECT *` when you need three fields.
- **Server-side pagination** + **cached aggregates** (e.g. `site_stats` instead of
  `COUNT(*)` over the whole database on every visit to the home page).
- **WAL** (SQLite) — readers don't block the writer; the default mode in the reference project.
- **Careful with `LIKE '%foo'`** — a leading wildcard kills the index (full scan); consider FTS if
  it's a hot search path.

## Anti-patterns
- 🚫 **Optimization without measurement** — "I improved it" without knowing whether it was slow (→ [03](03-testowanie-i-weryfikacja.md)).
- 🚫 **No index on a hot query** — the most common cause of a slow catalog page.
- 🚫 **N+1 in a loop** — 200 queries where one join would do.
- 🚫 **`SELECT *`** — you transfer and deserialize columns you don't use.
- 🚫 **Client-side pagination of huge sets** — shipping a few thousand records to show 20.
- 🚫 **Blocking the UI waiting for the full LLM response** instead of streaming (→ [12](12-elastycznosc-i-skalowalnosc.md)).
- 🚫 **No cache on expensive aggregates** — `COUNT(*)` over the whole database on every request.

## For new projects
Add to Day 0 (→ [07](07-nowy-projekt-checklist.md)): a **Lighthouse baseline** right after the
first working page (you have a reference point), indexes on filter columns from the first
migration, `EXPLAIN QUERY PLAN` as a habit on every hot query. The overriding rule:
**no optimization without a before-and-after number** — because without proof an "optimization" can
be a regression in disguise (→ [03](03-testowanie-i-weryfikacja.md)). Speed is both SEO
(→ [10](10-seo-i-tlumaczenia.md)) and infrastructure cost (→ [12](12-elastycznosc-i-skalowalnosc.md))
— one investment, three returns.
