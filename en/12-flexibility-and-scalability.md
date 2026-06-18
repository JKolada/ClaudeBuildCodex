# 12 — Flexibility and scalability

> The golden rule of altitude applied to architecture: *slow where a mistake is expensive; fast
> where it's cheap.* Scale when a metric demands it — not sooner, not "just in case."

Flexibility is the ability to change **without a rewrite**; scalability is the ability to grow
**without a rebuild**. Both come from the same habits: separate the layers, make changes additive,
hide risk behind a flag, don't couple state where you don't have to. And — just as important —
**don't over-engineer**: a simple architecture you can grow into beats a distributed one you don't
need.

## Separate the layers
- **DB ↔ ingest ↔ web** are three separate worlds. In the reference project: SQLite (data) ↔ Python scrapers
  (ingest) ↔ Node/Express (web) — bound by a **contract** (the schema, → [11](11-data-model-and-normalization.md)),
  not by shared code. You can swap the scraper without touching the web layer.
- **The API contract is the boundary** — e.g. a Next.js frontend ↔ a Python backend via an explicit
  contract (OpenAPI). A boundary you hold to lets you replace either side independently. → [08](08-stack-and-technologies.md)
- **A shared backend for web + a future mobile app.** An ADR ahead of time: SQLite vs Postgres, session
  vs JWT (e.g. sessions for web; mobile later → consider JWT on the shared backend).
  **Write the decision down**, don't keep it in your head. → [01](01-documentation-and-ai-readme.md)

## Make changes reversible and rampable
- **Additive / backward-compatible** — a new column, a new endpoint, a new language; don't break
  what works (→ [11](11-data-model-and-normalization.md)).
- **Feature flags** — `feature_flags` in the database + toggles like `BETA_ALL_PREMIUM`. **Ship dark,
  then ramp**: the code ships off, you turn it on for a slice, then for everyone. Without flags every
  change is all-or-nothing.
- **Stateless where you can** — the less state in the process, the easier it is to scale horizontally.

## Platform: scale-to-zero vs always-on
A real decision from two projects, a **deliberate cost/latency tradeoff**:
- **Cloud Run (scale-to-zero)** — you pay for usage, zero traffic = zero cost, but **cold start**
  adds latency to the first request. Good for uneven, global traffic.
- **VPS always-on (Hetzner + pm2)** — e.g. a fixed cost, **zero cold start**, full
  control. Good for predictable traffic and SQLite on disk.
The choice comes down to traffic profile and budget, not fashion. Record it as an ADR.

## Cache and pipelines
- **Cache layers** with explicit invalidation: e.g. cache invalidation in the `full` pipeline,
  rankings cached for **10 min**, statics with `max-age` (an hour in dev / 7 days immutable in prod).
- **Composable, idempotent pipelines** — `normalize → metadata → enrich → validate → stats`;
  each stage runnable on its own, a re-run is safe (→ [04](04-scripts-and-databases.md)).
- **i18n / multi-market from the start, if global** (e.g. 16 languages from day one, not bolted on
  later — → [10](10-seo-and-translations.md)).

## Don't over-engineer
- **Start simple.** SQLite + a static build (e.g. a static build in Python)
  handle a surprising amount of traffic. The reference project on SQLite/WAL serves a few thousand items without Postgres.
- **Scale when a metric demands it** — not "because it'll grow someday." Right-size to real traffic.
- A SQLite→Postgres migration, monolith→services: **when the numbers demand it**, with an ADR, not preemptively.

## Anti-patterns
- 🚫 **Premature distributed complexity** (microservices/Kafka/k8s for 100 users).
- 🚫 **Stateful coupling that blocks scaling** (session state in process memory with no store).
- 🚫 **Big-bang rewrite** instead of additive changes (→ [04](04-scripts-and-databases.md)).
- 🚫 **No feature flags** → every change forced into all-or-nothing, no ramp/dark-ship.
- 🚫 **Ignoring the cost of always-on** (paying for idle when scale-to-zero would fit) — and vice versa.
- 🚫 Rewriting to Postgres "just in case" while SQLite hasn't even broken a sweat.

## For new projects
On Day 0 (→ [07](07-new-project-day-0.md)) set **three boundaries** (DB / ingest / web) and
write **three ADRs**: database (SQLite vs Postgres), session vs JWT, platform (VPS vs Cloud Run).
Introduce `feature_flags` from the start — it's the cheapest insurance policy on flexibility. Start
with the simplest stack that delivers (statics/SQLite), and defer scaling to the moment a concrete
metric (latency, cost, database size) demands it — and then decide by the numbers, not by hunch
(→ [13](13-performance-frontend-and-sql.md)).
