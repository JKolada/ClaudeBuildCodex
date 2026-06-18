# 07 — New project: Day 0

A concrete checklist Claude runs **when starting a new project**.
Goal: after Day 0, every subsequent session has solid ground underfoot.

## 0. Product brief — ask before anything is built

Before the first line of code and before `CLAUDE.md`, **ask the user a set of questions** — and don't
guess the default answers where they change architecture, law, or brand. These decisions are cheaper on
paper than in code (i18n bolted on later is a rewrite; monetization after the fact is a data migration).
Ask concisely, in groups; if the user doesn't know something, propose a default and flag it as an
assumption. Ask the same questions when **applying the doctrine to an existing project** — there as an audit
("what's already there, what's missing").

- **User's technical level and communication style.** Ask this **first** — it sets the register
  for the whole conversation. Do you write or read code? Do you know terms like repo, deploy, database,
  and API, or should I translate them? Do you prefer technical decisions made for you (with a short "why"),
  or do you want to understand them and co-decide? How should I report progress: a terse "works / doesn't
  work", or with details? → When the answers are "non-technical," **switch the register**: no unexplained
  jargon, analogies instead of terms, closed questions with a recommendation instead of open technical ones,
  default decisions plus consent instead of deliberation. Same doctrine content, different delivery
  (→ editions: technical / BIZ-TECH / business, see repo header).
- **Target languages and markets.** One language or many? Which ones, in what order, and which is the
  source of truth? Is content parity a requirement? RTL? Currencies, timezones, date formats? → decides
  i18n from Day 0 and the data structure ([10](10-seo-i-tlumaczenia.md), [11](11-model-danych-normalizacja.md)).
- **Features — core vs. "later".** What's the MVP (without which the product doesn't exist), and what's
  nice-to-have? Accounts and roles? Static content or user-generated? External integrations
  (payments, maps, AI, email)? → defines the layers and feature flags ([12](12-elastycznosc-i-skalowalnosc.md)).
- **Monetization.** Free, paid, freemium, subscription, one-off, ads, affiliate? When does
  payment appear — Day 1, or after traction? Which provider (Stripe or other), invoices, VAT/OSS? →
  touches the data model and legal obligations ([09](09-prawo-i-ochrona-tworcy.md), [11](11-model-danych-normalizacja.md)).
- **UX style and visual direction.** Who's the target group, and what's the tone (serious B2B ↔ playful
  consumer)? Is there an existing brand (palette, typography, logo), or do we build from scratch? Dense
  dashboard or airy landing? Light/dark mode? Is accessibility (WCAG) a requirement?
- **Animation and the interface's "feel."** Static and fast, or rich in microinteractions
  and transitions? Performance budget and `prefers-reduced-motion` as a rule? → animation must not fight
  Core Web Vitals ([13](13-wydajnosc-frontend-i-sql.md)).
- **Marketing tone.** What's the one-sentence value prop, who is the customer, and what do we avoid in
  the tone? Are the name, domain, and tagline set? It's the same "why" that later drives the changelog
  and copy written in the user's language ([08](08-stack-i-technologie.md) → [01](01-dokumentacja-i-ai-readme.md)).

> **Record the answers**, don't just hear them: hard decisions → `CLAUDE.md` (policies) and `memory/`
> (business goal, constraints — step 10). Clearly mark any assumptions made on the user's behalf, so they
> can be verified later.

**Where the brief lands.** You'll fill it out fastest in the Craft reader (the "Brief" view → generates
ready-made Markdown). The completed brief:
- **save as `brief-projektu.md` in the new project's root folder** (Craft is included as
  `docs/rules/`, so the brief sits *next to* it — in the project repo root, not in `docs/rules/`), **or**
- **paste the whole thing straight into Claude Code / Claude Desktop opened in the project's root folder** as
  the first message.

The brief is the entry point to the rest of Day 0: from it spring `CLAUDE.md` (step 2) and the `memory/` entry (step 10).

### Anti-patterns
- 🚫 **Jumping to code without a brief** — "I'll start and ask along the way." Language, monetization, and
  brand written in after the fact are a rewrite, not a fix.
- 🚫 **Burying the user in questions** — 30 questions at once discourages. Ask in groups, about what changes
  the plan; propose the rest as defaults.
- 🚫 **Silent assumptions** — adopting "probably just Polish" or "probably free" without flagging
  that it's your assumption, not the user's decision.
- 🚫 **Jargon aimed at a non-technical user** — "I'll rebase and bump semver after the migration" to someone
  who doesn't code. First establish the level, then pick the language. Failing to adapt the register cuts out
  half the doctrine's audience.

## 1. Recon (before you write anything — Commandment II)
- [ ] Read the existing `CLAUDE.md` / `AI_README.md` / `README`, if present.
- [ ] `git log --oneline -20`, `git status` — what's there, what's in progress, any orphans or junk.
- [ ] Identify the stack, how to run it, and where the data lives.
- [ ] List what you **don't yet know** — and ask only about what changes the plan.

## 2. Project constitution — `CLAUDE.md`
- [ ] Quick orientation (layer → tech → location).
- [ ] Exact run commands (interpreter, port, env).
- [ ] **Overriding policies**: "never deploy automatically", privacy/compliance, git workflow.
- [ ] A "Current state" section with a date and numbers.

## 3. Repo hygiene
- [ ] `.gitignore`: dependencies, local databases, backups (`*.bak`), generated assets, temp, scratch.
      (Remember: `#` comment on its own line.)
- [ ] Commit convention + deploy tagging.
- [ ] Task tracking (Issues / `docs/plans/`) — where the tasks live.

## 4. Per-directory documentation
- [ ] `AI_README.md` in every meaningful directory (a skeleton at least).
- [ ] `docs/` for stable reference (architecture, data schema) and plans.

## 5. Skills (automating the repetitive)
- [ ] `/run-<project>` — run + smoke test (N routes, markers, exit code).
- [ ] `/run-tests` — full suite (unit + integration + e2e).
- [ ] `/update-ai-readme` — sync docs before a commit.
- [ ] `/add-migration` — if a relational database (number → SQL → apply → AI_README → commit).

## 6. Tests and verification
- [ ] Unit + integration skeleton; smoke test with markers.
- [ ] (If UI) Playwright on a separate port.
- [ ] Rule: critical-path tests before a commit; "verify, don't declare".

## 7. Databases and scripts
- [ ] Forward-only migrations + a `backups/` directory + retention.
- [ ] Every mutating script: `--dry-run` by default, `--execute` deliberately, idempotent.
- [ ] **Nightly backup** from the moment of the first real users.

## 8. Production (prepare, don't fire)
- [ ] Deploy runbook (code-only vs maintenance window) — write it before it's needed.
- [ ] Branded maintenance page + flag (e.g. nginx `/tmp/<app>_maintenance`).
- [ ] Rollback plan: code tag + database backup.
- [ ] Public "What's new" changelog (pinned), written in the user's language.

## 9. Compliance / privacy (if it touches people's data)
- [ ] Privacy policy + consents, anonymization, retention — **as a rule in the constitution**.
- [ ] Disclaimers (e.g. "for adults", "we don't provide therapeutic services").
- [ ] i18n from the start, if the product is global.

## 10. Memory
- [ ] Record in `memory/`: who the user is, the business goal, hard project constraints
      (what isn't in the code).

---

> **Minimal Day 0**, when there's no time for everything: a short **brief** (step 0: language, MVP,
> monetization, tone) → `CLAUDE.md` (stack + how to run +
> policies) → `.gitignore` → one `/run-<project>` skill with a smoke test → a test skeleton →
> a `backups/` directory. The rest grows with the project.
