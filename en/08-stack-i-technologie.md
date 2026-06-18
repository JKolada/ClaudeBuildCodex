# 08 — Stack and technologies

> The golden rule of altitude applied to tool choice: *the simplest thing that meets the requirement;*
> *complexity is added when a metric forces it (→ [12](12-elastycznosc-i-skalowalnosc.md)).*

The doctrine is language-agnostic — but the choice of stack decides **how cheap a mistake is**
and **how easily you can test it**. This chapter is a sensible *default* for a project run
with Claude: universal, simple, flexible, and scalable. Not dogma — a starting point you
depart from deliberately (and record why, as an ADR).

## Default stack (a reasonable start)

| Layer | Default | When to change |
|-------|---------|----------------|
| Backend / scripts | **Python** (+ FastAPI for the API) | Front and back share TypeScript → Node |
| Database | **SQLite** | Concurrent writes / roles / relations / scale → **PostgreSQL** |
| Web / front | Server-rendered HTML + a bit of JS | Rich, interactive UI → Next.js |
| API | REST/JSON with an explicit contract (OpenAPI) | gRPC only at real need |
| Cache / queue | none → add Redis when the traffic profile forces it | not "just in case" |
| Packaging | **Docker** (reproducibility) | trivial script with no dependencies → no container |
| Hosting | one **VPS (Hetzner)** + nginx | uneven/global traffic → serverless (scale-to-zero) |

Overriding rule: **boring, mature technology beats trendy.** What counts is the ecosystem, the documentation,
and testability — not the hype.

## Proven toolkit (a concrete baseline)

A toolkit battle-tested on a real project — take what the task requires, skip the rest.
Everything here is **mature, well-documented, and easy to test and host on a single VPS**:

| Layer | Tools |
|-------|-------|
| **Primary tool / process** | **Anthropic Claude — Claude Desktop / Claude Code** (the agent you build with) · **Git** (history, → [05](05-git-i-wdrozenia.md)) · **GitHub** (remote repo, PR) · **GitHub Issues** (tasks, → [07](07-nowy-projekt-checklist.md)) |
| **Format / content** | HTML5 (server-rendered), Markdown (docs), **JSON** (API, config), XML when an integration forces it |
| **Data / queries** | **SQL** — SQLite (WAL) to start → PostgreSQL at scale; forward-only migrations |
| **Backend / scripts** | **Python** (data, scrapers, migrations on stdlib) · **Node.js + Express** (web/API) · EJS (server-side templates) |
| **Frontend** | minimal **JS** (vanilla), `marked` for MD rendering; **SVG icons: Lucide only** (one source of geometry, consistency); self-hosted fonts |
| **Sessions / security** | persistent session store (a separate file, → [14](14-odpornosc-operacyjna.md)), `helmet`, rate-limit, `bcrypt`, OAuth (passport) |
| **Mail** | SMTP (587 STARTTLS), verified sender domain (→ [14](14-odpornosc-operacyjna.md)) |
| **Media / image** | conversion to **WebP** (Pillow); image comparison (OpenCV) only when truly needed |
| **Ingest / scraping** | `requests` + BeautifulSoup (+lxml), fuzzy-match (rapidfuzz), Playwright when a browser is needed (→ [14](14-odpornosc-operacyjna.md)) |
| **LLM** | API client (Claude / Anthropic SDK), responses **streamed over SSE** (→ [13](13-wydajnosc-frontend-i-sql.md)) |
| **Tests** | `pytest` (Python) · Jest + supertest (Node) · Playwright (e2e) (→ [03](03-testowanie-i-weryfikacja.md)) |
| **Build / dev** | esbuild, nodemon; Docker for reproducibility |
| **Server / ops** | one **VPS (Hetzner)** + nginx (TLS, reverse proxy) + `pm2`/`systemd`; GA4 analytics |

**Icon rule:** for SVG, stick to **one set — Lucide** (geometry in a `<symbol>`/sprite,
the rest is style). Mixing icon libraries = inconsistent UI and mismatched weights/strokes.

## Python as the default language
- **Why:** readability (code like prose — easy to review by a human *and* an agent), batteries
  included, one language for API + scripts + data/LLM. Fewer contexts to hold in your head.
- **FastAPI** for the API: types + validation (Pydantic) + **auto-OpenAPI = a free contract** at the
  front↔back boundary (→ [12](12-elastycznosc-i-skalowalnosc.md)). **pytest** for tests (→ [03](03-testowanie-i-weryfikacja.md)).
- **Reproducible env:** a virtual environment + **pinned deps** (lock). "Worked yesterday" goes away.
- **Format and types as a contract:** `ruff`/`black`, type hints. Consistent style = cheaper review (→ [02](02-skille-i-refaktoring.md)).

## Database — from simple to scale
- **Start: SQLite.** Zero-ops, one file, great for an MVP and an always-on VPS. Don't start with
  a distributed database "because it'll grow someday".
- **Scale: PostgreSQL** — when concurrent writes, roles, complex relations, or extensions start to hurt.
  Anticipate the SQLite→PG migration in the model from the start (→ [11](11-model-danych-normalizacja.md)).
- **Engine-independent rules:** **forward-only** migrations + a backup before each (→ [04](04-skrypty-i-bazy-danych.md)),
  **slug instead of ID** in references to user data, indexes **after measurement**, not on a hunch (→ [13](13-wydajnosc-frontend-i-sql.md)).
- NoSQL / distributed — only when relational genuinely doesn't suffice, not before.

## Web and API — the contract as the boundary
- **The less JS, the better.** Server-rendered HTML by default; SPA/Next.js only when the interaction
  truly requires it. A light front = faster and cheaper to maintain (→ [13](13-wydajnosc-frontend-i-sql.md)).
- **The API contract (OpenAPI) is the boundary** between front and back — it lets you swap one side
  without touching the other (→ [12](12-elastycznosc-i-skalowalnosc.md)). Version it; return **structured** errors.
- **Streaming / SSE** for long responses (chat, LLM token-by-token) — the user sees the effect right
  away, not emptiness (→ [13](13-wydajnosc-frontend-i-sql.md)).

## Docker — reproducibility, not a cult
- **What for:** the same image locally / in CI / in prod. "Works on my machine" ceases to exist.
- **Hygiene:** a small image (multi-stage, slim base, **pinned** versions), `.dockerignore`, a
  **non-root** process. `docker-compose` for local assembly (app + database).
- **Don't containerize by force** a single script. Docker where dependencies hurt — not as a ritual.

## Server and hosting — one box, good habits

> **The monolith is the default architecture — favor it as the easiest to maintain.** One
> application (web + API + jobs) and one database on **one VPS** is something you can hold in your head:
> one deploy, one log, one backup, one rollback. Debugging means reading a single process, not
> correlating traces across a network. Splitting into services/serverless **adds** the network, contract
> versioning, and a whole class of new failures (→ [14](14-odpornosc-operacyjna.md)) — reach for them only
> when a **metric** (traffic, team, failure isolation) genuinely requires it, not "because that's how it's done."

- **Default: one VPS (Hetzner) + nginx** (reverse proxy, TLS) + `systemd`/`pm2`/Docker for
  processes. Cheap, predictable, full control, **zero cold start**. Many projects on one
  box = a separate vhost + a separate directory, the same deploy rules (→ [05](05-git-i-wdrozenia.md)).
- **Scale-to-zero** (Cloud Run / serverless) when traffic is uneven/global and the **cold start**
  is acceptable; **always-on VPS** when traffic is predictable. A deliberate cost/latency tradeoff,
  recorded as an ADR (→ [12](12-elastycznosc-i-skalowalnosc.md)).
- **Managed services** (database, mail, storage) when they take ops off your plate for **less** than
  maintaining it yourself would cost.
- **Secrets** in env / a secret store — **never** in the repo (→ [09](09-prawo-i-ochrona-tworcy.md)).

## TDD and change coverage — the hard core
The most important criterion for choosing a stack: it must be **testable from the first line**. A technology
you can't easily wrap in a test (test-first, a fast and deterministic suite, gating CI)
is a bad choice — even if it's trendy. The mechanics of TDD and change coverage = the canon in → [03](03-testowanie-i-weryfikacja.md);
here, just the hard consequence: **choose tech that makes it possible, and treat "a commit without a test" as
incomplete** (→ [00](00-przykazania.md)).

## The technology-choice rule
1. **The simplest thing that meets today's requirement**, with an explicit growth path (SQLite→PG, VPS→serverless).
2. **Testability and ecosystem** matter more than novelty.
3. Every non-trivial choice = an **ADR**: one "why" + the rejected alternatives. The next session
   (human or agent) should know why it's done this way.

## Anti-patterns
- 🚫 **Microservices / Kubernetes / a distributed database on an MVP** — complexity no one needs yet (→ [12](12-elastycznosc-i-skalowalnosc.md)).
- 🚫 **A stack for the CV/the trend** instead of for the problem and testability.
- 🚫 **Changing behavior without a test** ("I'll add it later" — you won't).
- 🚫 **Secrets in the repo**; no version pins → "worked yesterday".
- 🚫 **SPA / heavy JS** where server-side HTML would do.
- 🚫 **Docker/Cloud as a cult** instead of a tool fit to the problem.
