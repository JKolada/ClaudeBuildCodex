# The Craft — Rzemiosło <sub>(Kolada Build)</sub>

> **The art of building end-to-end applications with Claude** — scalable, maintainable, and easy to
> evolve, migrate, and change. Not a framework or a library: a **human + agent doctrine** — a tight set
> of rules, commandments, and anti-patterns that keep a project understandable, testable, safe to change,
> and trustworthy, from the first commit to production with real users.

New here? Read the manifesto: **[What The Craft is](intro.md)** · or the whole doctrine on one screen:
**[00 — Decalogue](00-commandments.md)**.

## Adopt it in your project

The Craft is meant to be dropped into a project as `docs/rules/`, so the agent reads it from Day 0:

```bash
git submodule add https://github.com/JKolada/ClaudeBuildCodex docs/rules
# or just copy the files into docs/rules/
```

Then point your project's `CLAUDE.md` at it (full steps → [07 — New project: Day 0](07-new-project-day-0.md)):

> **Read `docs/rules/` every session — it is the build doctrine (The Craft).** For a specific topic,
> `grep -i <keyword>` over `docs/rules/AI_README.md` → the right chapter; read only that one.

## Languages

**English is the base** — the canonical doctrine lives in the repo root. **Polski** is a 1:1 translation
under [`pl/`](pl/00-commandments.md) (same chapters, same filenames). The in-browser reader
([index.html](index.html)) renders the `.md` and has an **EN | PL** switch (default EN). On GitHub the
`.md` files render natively — just click the links below.

## Chapters

| # | Chapter | What it covers |
|---|---------|----------------|
| 00 | [Decalogue](00-commandments.md) | 10 commandments — the doctrine's core, to memorize |
| 01 | [Documentation and AI_README](01-documentation-and-ai-readme.md) | `AI_README` in every directory, `CLAUDE.md` as source of truth, the grep index, docs as code |
| 02 | [Skills and refactoring](02-skills-and-refactoring.md) | When to build a skill/slash-command, refactoring discipline, SOLID |
| 03 | [Testing and verification](03-testing-and-verification.md) | Test pyramid, "verify, don't declare", smoke tests |
| 04 | [Scripts and databases](04-scripts-and-databases.md) | Idempotency, dry-run/--execute, forward-only migrations, backups |
| 05 | [Git and deployments](05-git-and-deployments.md) | Search git before coding, tag every deploy, swap the DB while preserving accounts |
| 06 | [Collaboration and memory](06-collaboration-and-memory.md) | Plan→iterate→review, memory, confirm the irreversible, report honestly |
| 07 | [New project: Day 0](07-new-project-day-0.md) | Wire The Craft in + product brief + a concrete startup checklist |
| 08 | [Stack and technologies](08-stack-and-technologies.md) | Python, databases, web/API, Docker, servers (Hetzner), TDD — a simple, scalable default |
| 09 | [Law and protecting the creator](09-law-and-protecting-the-creator.md) | Terms, privacy policy, disclaimers as the creator's armor |
| 10 | [SEO and translations](10-seo-and-translations.md) | hreflang, JSON-LD, programmatic SEO, E-E-A-T/YMYL, language parity as a test |
| 11 | [Data model and normalization](11-data-model-and-normalization.md) | Lookup tables, slug instead of ID, active-row, deliberate denormalization |
| 12 | [Flexibility and scalability](12-flexibility-and-scalability.md) | Separate the layers, feature flags, scale-to-zero vs always-on, don't over-engineer |
| 13 | [Performance: frontend and SQL](13-performance-frontend-and-sql.md) | Measure first, indexes + partial index, no N+1, chat streaming, CWV |
| 14 | [Operational resilience](14-operational-resilience.md) | Crash-proof runtime, resumable jobs, unreliable APIs (backoff/rotation), provider limits, cost quotas |
| 15 | [Scraping, AI APIs, and chatbots](15-scraping-ai-and-chatbots.md) | Effective scraping, AI for specific tasks (contract + cache), configurable & grounded assistants |
| 16 | [Driving Claude](16-driving-claude.md) | Skills/slash-commands, picking the model, autopilot (preferred), background work, agentic workflows |

## The philosophy in one sentence

> **Build like a craftsman — slow where a mistake is expensive, fast where it's cheap; and leave behind a
> workshop where the next person (human or agent) immediately knows where everything is.**

---

*A living document — updated after every project that taught us something. A doctrine that doesn't change
is dead.* · Part of **[jakub.solutions](https://jakub.solutions)** — Jakub Kolada.
Maintainer/build docs: [CLAUDE.md](CLAUDE.md) · [AI_README.md](AI_README.md).
