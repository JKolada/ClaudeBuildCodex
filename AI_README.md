# AI_README — The Craft directory map

> Directory map for the next session / another agent. Read it **before** touching any files here.
> Repo constitution: [CLAUDE.md](CLAUDE.md). Quality test for this file: after reading it, can you
> safely change anything in this directory without scanning every file?
>
> **Meta-file split** (→ [01](01-documentation-and-ai-readme.md)): `README.md` = description for GitHub
> (public, EN). `CLAUDE.md` = repo constitution (single language, **not translated**). **`AI_README` is
> translated per language** — this file (root) is the **EN/base** version; the PL copy lives in [`pl/AI_README.md`](pl/AI_README.md).

## What this directory is

A **documentation** repository (not an application): the "Rzemiosło — The Craft" doctrine (Kolada Build).
The content is hand-written markdown; `index.html` is its viewer (a static SPA, no build step).
Goal: a rule set reusable as `/docs/rules/` in new projects **and** public material for
people starting out with Claude. Details and policies → [CLAUDE.md](CLAUDE.md).

## Core (this repo) vs Web (sibling repo)

**Split of responsibilities — do not duplicate between them:**

- **This repo (`ClaudeBuildCodex`, the "Rzemiosło" brand) = canonical core.** Form: **technical, terse, imperative;
  English is the base** (PL translation in `pl/`) — the source of truth for the rules, attached to projects as `/docs/rules/`. Optimized for
  **the agent and the technical reader**: density over approachability. This is where we version the doctrine (codex.json).
- **The sibling `ClaudeBuildCodexWeb` (the "Rzemiosło Web" brand) = the presentation project.** It takes the same doctrine and **expands
  individual topics** into a friendlier, more extensive form. **Web — not this repo — is responsible for:**
  the public site, **editions** (technical / BIZ-TECH / business), **language versions**, and **building
  `docs/rules/` packages in a specific language**. It consumes this repo's content + `codex.json` at build time.

> **This repo is ONLY a rule set.** It is not a presentation product. The `index.html` here is a
> **minimal local/dev reader** (content preview for the author and agent), **not** a public site —
> which is why we don't put edition badges, marketing, or a language switcher here. All presentation,
> editions, and multi-language packaging happen in **The Craft Web** (a separate project). If you're tempted
> to add a presentation/marketing/edition layer here — that's material for Web, not for the core.

Direction for the EN version and per-language packaging → [docs/plans/0001-i18n-and-packaging.md](docs/plans/0001-i18n-and-packaging.md).

## File index

| File | What it's for |
|------|----------|
| `index.html` | **Minimal local/dev reader** (content preview for the author/agent) — NOT a public site. Home page (decalogue + cards) + chapter view + brief + EN/PL language switcher (EN by default). |
| `intro.md` | **Manifesto** — "What The Craft is" + a "why it's worth it" article. A special document (outside the numbered list), routed as `#intro`; there's also `pl/intro.md`. |
| `00`–`15` (root) | **EN content — canonical, base, source of truth.** Slugs/numbers = stable anchors, shared across all languages. |
| `pl/` | **PL content** — a parallel set of `00-*.md`…`15-*.md` (the same file names, content in Polish). Translation of the EN. |
| `docs/` | Plans and meta decisions for the repo (not doctrine content): `docs/AI_README.md`, `docs/plans/`. |
| `content.js` | **Generated** snapshot of the `.md` embedded in JS — lets content render over `file://`. Do not edit by hand. |
| `build.py` | Build script: concatenates `.md` files → `content.js`. Run after editing content (`python build.py`). |
| `test.py` | **Smoke test** (pure Python): PL↔EN parity, dead links, `content.js` freshness, consistency of `CHAPTERS`/tables/`codex.json`, and **static `index.html` navigation** (`href="#…"` links, `data-i18n`↔`UI`, `data-bf-label`↔`BRIEF_FIELDS`). `python test.py`. |
| `CLAUDE.md` | Repo constitution: what it is, the stack, how to run it, policies, current state. |
| `AI_README.md` | This file — the directory map. |
| `README.md` | Entry point for a human: chapter list + "how to read it". |
| `codex.json` | **Release version** (`version` + `released`) + brand names (`name`/`name_short`/`name_en`). The source of the stamp for the Rzemiosło Web site. |
| `CHANGELOG.md` | Rzemiosło release history (semver, date = publication day). |
| `00-commandments.md` | **Decalogue** — 10 commandments, 7 sins, the golden rule of altitude. The core. |
| `01-documentation-and-ai-readme.md` | Three layers of docs: CLAUDE.md / AI_README / docs. When to update them. |
| `02-skills-and-refactoring.md` | When to build a skill/slash-command; refactoring discipline; SOLID (with feature flags and separate-the-layers). |
| `03-testing-and-verification.md` | Test pyramid, "verify, don't declare", smoke. |
| `04-scripts-and-databases.md` | Dry-run/`--execute`, idempotency, forward-only migrations, backups. |
| `05-git-and-deployments.md` | Search in git, tag deploys, swap the database while preserving accounts. The densest chapter. |
| `06-collaboration-and-memory.md` | Plan→iterate→review, memory, confirm the irreversible, report honestly. |
| `07-new-project-day-0.md` | "Day 0" checklist: product brief (language, features, monetization, UX, animations, marketing) + repo setup. |
| `08-stack-and-technologies.md` | Universal stack: Python, databases, web/API, Docker, servers (Hetzner) + TDD as the hard core. |
| `09-law-and-protecting-the-creator.md` | Terms, privacy policy, disclaimers as protection for the creator / sole proprietorship. |
| `10-seo-and-translations.md` | hreflang, JSON-LD, E-E-A-T/YMYL, language parity as a test. |
| `11-data-model-and-normalization.md` | Lookup dictionaries, slug instead of ID, active-row, deliberate denormalization. |
| `12-flexibility-and-scalability.md` | Separate the layers, feature flags, scale-to-zero vs always-on, don't over-engineer. |
| `13-performance-frontend-and-sql.md` | Measure first, indexes + partial index, no N+1, chat streaming, CWV. |
| `14-operational-resilience.md` | Crash-proof runtime, resumable jobs, unreliable APIs (backoff/rotation), provider limits + email, cost quotas. |
| `15-scraping-ai-and-chatbots.md` | Effective scraping (official source, shape validation, delta), AI APIs for specific tasks (contract/cache/quotas), configurable+grounded chatbots. |
| `16-driving-claude.md` | Operating Claude Code: skills/slash-commands, picking the model, autopilot (preferred), background jobs, agentic workflows/subagents. |

The chapters split into a **core** (`00`–`08`) and a **deep dive** (`09`–`16`). Each = one
commandment/topic, terse, ending with anti-patterns.

## Topic index → file (grep-friendly)

> **Looking for something specific? Don't read everything.** `grep -i <topic>` over this index (PL+EN keywords) →
> the file name on the same line → read **only that chapter**. That's how you save context in the
> target project (rule: [01](01-documentation-and-ai-readme.md)).
> The file slug is shared between EN (root, base) and PL (`pl/`).

- **`00-commandments.md`** — dekalog, decalogue, 10 przykazań, ten commandments, 7 grzechów, seven deadly sins, złota zasada, golden rule, altytuda, altitude, rdzeń doktryny, core.
- **`01-documentation-and-ai-readme.md`** — dokumentacja, documentation, AI_README, CLAUDE.md, docs, /docs, plany, plans, grep, keyword index, oszczędność kontekstu, context economy, czytnik, documentation.html, regeneracja, struktura folderów, folder structure.
- **`02-skills-and-refactoring.md`** — skill, slash-command, /run, /add-migration, automatyzacja, automation, hook, refaktoring, refactoring, prior-art, reuse, backward-compat, shim, SOLID, single responsibility, open/closed, dependency inversion, /simplify, /code-review.
- **`03-testing-and-verification.md`** — test, testowanie, testing, TDD, test-first, piramida, test pyramid, unit, integration, e2e, Playwright, pytest, Jest, smoke test, weryfikuj nie deklaruj, verify don't declare, regresja, regression, CI.
- **`04-scripts-and-databases.md`** — skrypt, script, mutacja, dry-run, --execute, idempotencja, idempotency, migracja, migration, forward-only, backup, restore, retencja, retention, seed, backfill, baza, database.
- **`05-git-and-deployments.md`** — git, git log -S, pickaxe, blame, deploy, wdrożenie, deployment, tag, rollback, swap bazy, database swap, konta, accounts, slug, maintenance window, nginx, pm2, sesje, sessions, FK order, integrity_check, sieroty, orphans, .gitignore, CRLF.
- **`06-collaboration-and-memory.md`** — współpraca, collaboration, plan iteruj review, plan iterate review, pamięć, memory, memory/, potwierdzaj nieodwracalne, confirm irreversible, raportuj uczciwie, report honestly, feedback.
- **`07-new-project-day-0.md`** — nowy projekt, new project, Dzień 0, Day 0, checklist, brief, brief produktowy, product brief, monetyzacja, monetization, onboarding, setup, poziom techniczny, technical level, runbook.
- **`08-stack-and-technologies.md`** — stack, technologie, technologies, Python, Node.js, FastAPI, SQLite, PostgreSQL, Docker, nginx, pm2, Hetzner, VPS, monolit, monolith, serverless, scale-to-zero, ADR, Lucide, baseline, Claude Code, GitHub, Git, GitHub Issues, TDD.
- **`09-law-and-protecting-the-creator.md`** — prawo, law, regulamin, terms of service, ToS, polityka prywatności, privacy policy, RODO, GDPR, zgody, consent, cookie, disclaimer, JDG, sole proprietorship, bramka wieku, age gate, 18+, retencja, prawa użytkownika, user rights, usunięcie konta, account deletion, ochrona twórcy.
- **`10-seo-and-translations.md`** — SEO, hreflang, JSON-LD, schema, canonical, sitemap, meta, OG, Open Graph, E-E-A-T, YMYL, programmatic SEO, tłumaczenia, translations, i18n, l10n, parytet językowy, language parity, RTL, lokalizacja.
- **`11-data-model-and-normalization.md`** — model danych, data model, normalizacja, normalization, denormalizacja, denormalization, słownik, lookup table, controlled vocabulary, slug, slug zamiast ID, slug not ID, active-row, expired_at, partial index, junction, M:N, klucz obcy, foreign key, ERD, schemat.
- **`12-flexibility-and-scalability.md`** — elastyczność, flexibility, skalowalność, scalability, rozdziel warstwy, separate layers, granice, boundaries, feature flag, feature flags, ship dark, ramp, scale-to-zero, always-on, cold start, cache, invalidation, over-engineering, ADR.
- **`13-performance-frontend-and-sql.md`** — wydajność, performance, mierz najpierw, measure first, Lighthouse, Core Web Vitals, CWV, LCP, CLS, INP, indeks, index, partial index, EXPLAIN QUERY PLAN, N+1, SELECT *, WAL, WebP, cache busting, lazy load, streaming, SSE, pagination, paginacja.
- **`14-operational-resilience.md`** — odporność, resilience, runtime, crash, unhandledRejection, uncaughtException, restart loop, retry, backoff, timeout, 429, rate limit, rotacja, rotation, User-Agent, resumable, wznawialne, checkpoint, scraper, długie joby, long jobs, SMTP, 587, STARTTLS, deliverability, SPF, DKIM, email, poczta, kwota, quota, koszt, cost, abuse, sesje, sessions, MemoryStore.
- **`15-scraping-ai-and-chatbots.md`** — scraping, scraper, crawler, robots.txt, selektor, selector, parsing, BeautifulSoup, requests, fuzzy match, rapidfuzz, dedup, delta, incremental, AI API, LLM, model, JSON schema, tool use, kontrakt wyjścia, output contract, cache, kwota, quota, chatbot, asystent, assistant, system prompt, grounding, RAG, prompt injection, halucynacja, hallucination, eval, golden set, disclaimer.
- **`16-driving-claude.md`** — Claude Code, skill, skille, slash-command, slash, /run, /run-tests, hook, model, modele, przełączanie modeli, model switch, autopilot, auto-accept, autonomiczny, autonomous, tło, background, run_in_background, długie zadania, long jobs, agentic, agentowe, subagent, subagenci, workflow, fan-out, równolegle, parallel, orkiestracja, orchestration, bariery, guardrails.

## `index.html` architecture (contract)

A single file, no build dependencies. Mechanics:

- **`CHAPTERS`** (an array in `<script>`) — **the single source** of the chapter list. From it are generated:
  the cards on the home page, the `<select>` in the reader, prev/next navigation. Fields: `file, no, group
  ("core"|"deep"), title, desc`.
- **Hash routing:** `#NN-name` → chapter view; empty/`#` → home page. `route()`
  reacts to `hashchange`.
- **Language (content + the whole chrome):** `LANG` (`en`/`pl`, default **`en`**, saved in `localStorage` `rzemioslo-lang`).
  Chapter content from `file` (EN, root) or `pl/`+`file` (PL). **The chrome is fully bilingual** —
  the `UI` dictionary (`data-i18n`/`data-i18n-html`) + `CH_EN` (chapter titles/descriptions) + `BRIEF_FIELDS`
  (brief fields); `applyChrome()` redraws everything at startup and on `#langToggle`. Add a
  string to the chrome → add a key to `UI` (both languages), otherwise it stays in Polish.
- **Render (two-track):** first `fetch(langPath(file))` (fresh `.md`, when served); on a fetch
  error (`file://`) — the `window.RZEMIOSLO_DOCS[LANG][slug]` snapshot from `content.js`. The result →
  `marked.parse()` → `.prose`, cached in memory (`cache[LANG+":"+file]`).
- **`rewriteLinks()`** after render: `*.md` links → `#slug` (SPA navigation), `index.html` → `#`,
  external `http(s)` → `target=_blank`; tables wrapped in `.tablewrap` for scrolling on mobile.
- **Theme:** `[data-theme]` on `<html>` (`light`/`dark`); no attribute = follow the system. The switcher
  in the topbar saves the choice in `localStorage` (`rzemioslo-theme`); a script in `<head>` sets it
  before render (no flash).
- **Fallback note** shows only when **both** sources fail (no `content.js` and `file://`).

## Gotchas

- **`file://` blocks `fetch`** — which is why content works from a double-click **only** from the
  `content.js` snapshot. After editing `.md` run `python build.py`, otherwise `file://` will show stale content.
  When served (`http(s)://`, GitHub Pages) it always takes the fresh `.md`; on GitHub the `.md` renders natively.
- **`content.js` is generated** — don't edit it by hand (the build will overwrite it). Commit it so `file://`
  works after the repo is cloned.
- **`marked` is loaded from a CDN** — without network the render won't work (there's a soft fallback to `<pre>`).
- **`index.html` does NOT contain chapter content** — it reads `.md`/`content.js`. Don't paste content into the HTML.
- **Add/change a chapter → sync 3 places + build:** `CHAPTERS` (index.html), the table
  in `README.md`, the table in this file, then `python build.py`. A mismatch = a dead entry (worse than none).
- **EN↔PL parity:** changing a rule in `00`–`15` (EN, canon) requires updating the counterpart in `pl/` (the same
  list, the same file names). PL is a **translation**, not a separate doctrine. `content.js` holds both languages.
- **File names = stable anchors** (`#NN-name`, targets of relative links), **shared between EN and PL**.
  We don't localize file names — only the content inside. Don't change them without reason.
- **Brand:** make color changes on the CSS variables (`--accent`, `--accent-2`, `--grad`), not on the
  values at the point of use. Light and dark mode must both look good.
- **Content is generic, not "for one project".** Specific projects serve
  only as illustration (`e.g. …`, "reference project"), never as the topic. Don't make any project the hero of the doctrine.
- **Two languages: EN (canon, root, base) + PL (`pl/`).** Write rules translatably. Direction and convention →
  [docs/plans/0001-i18n-and-packaging.md](docs/plans/0001-i18n-and-packaging.md). Per-language packages are assembled by Web.

## Numbers

- 17 chapters (`00`–`16`) + `README.md`, in **two languages** (EN root = base + PL `pl/`).
  Core: 9 files (00–08). Deep dive: 7 (09–15).
- `index.html`: 1 file; runtime from a CDN (`marked` + Google Fonts). Build: `build.py` → `content.js`
  (EN: 19 docs ~110k chars; PL: 18 docs ~102k chars — chapters + `intro` + README; structure `{lang:{slug:md}}`).
- **Special documents (outside the numbered list):** `intro.md` (manifesto, route `#intro`) and the
  brief view (`#brief`) — routed separately, not present in the `CHAPTERS` array.
- **Smoke test:** `python test.py` (PL↔EN parity, dead links, `content.js` freshness, consistency of
  `CHAPTERS`/tables/`codex.json`, static `index.html` navigation: `href="#…"` links + `data-i18n`↔`UI` +
  `data-bf-label`↔`BRIEF_FIELDS`). Plus a "manual test" = preview via a server **and** from a double-click
  (`file://`) + clicking through chapters and the EN/PL switcher (runtime JS behavior the smoke test doesn't catch).
