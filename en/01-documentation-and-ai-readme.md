# 01 — Documentation and AI_README

> Commandment I: *Document for the agent, not for the archive.*

Documentation in a project with an AI agent has one overriding goal: **to let the next session (or
another agent) understand a directory without reading all of its code.** This is not an archive for
posterity — it's an onboarding interface, read every session.

## The three layers of documentation

| Layer | File | Role |
|---------|------|------|
| **Constitution** | `CLAUDE.md` (root) | Source of truth about the project: stack, how to run it, policies (e.g. "never deploy automatically"), current state. Loaded every session. |
| **Directory map** | `AI_README.md` (in every significant directory) | What's here, the module APIs, gotchas, numbers. You read it **before** touching code in this directory. |
| **Encyclopedia / plans** | `docs/` | Stable reference (architecture, DB schema), future plans, standards. |

### `CLAUDE.md` — the constitution
- A short "Quick orientation" (a table: layer → tech → location).
- **How to run** each piece (exact commands with interpreter/port).
- **Policies that override default behavior** — most important: the deployment policy
  ("never automatically to prod"), the git workflow, scraper/validation rules.
- A **"Current state"** section with a date and numbers (how many records, which migrations applied).
  This is the first thing the agent reads — it must be current.
- **Rule:** instructions in `CLAUDE.md` take precedence over the agent's default behavior.
  Write them like law: concrete, with the "why."

### `AI_README.md` — in every directory
A rule from the reference project worth carrying over: **every directory has an `AI_README.md`**, and
updating it is part of the commit workflow:

```
code  →  /update-ai-readme  →  git commit
```

What belongs in `AI_README.md`:
- A **file/module index** with a one-sentence "what it's for."
- The **API** of the key functions (signature + contract), so you don't read the implementation.
- **Gotchas** — traps invisible from the code (e.g. "FB won't render WebP as og:image,"
  "this CDN returns 200 with HTML on error").
- **Numbers** — how many records, how many tests, what coverage. Numbers go stale → update them.
- **Delete dead entries** — a reference to deleted code is worse than no entry.

> **The AI_README quality test:** after reading it, can the agent safely change code in this
> directory without scanning every file? If not — something's missing.

**The rule that binds the layers:** `CLAUDE.md` (root) **points to the `AI_README.md` in every folder**
as a mandatory complement — the constitution delegates directory detail to its map. The constitution
says "where and what the project is"; the `AI_README` says "what exactly is in this directory." Without that
pointer, a new session doesn't know the maps exist.

## The `/docs` structure and folders

Documentation "heavier than a directory map" lives in **`/docs`** — one place for stable
reference and plans, so the `AI_README`s and `CLAUDE.md` don't balloon:

```
docs/
  AI_README.md          # table of contents for docs: "where to start for task X"
  architecture.md       # layers, boundaries, flows
  data_model.md         # DB schema, ERD, controlled vocabulary (→ [11])
  deployment_runbook.md # procedure + numbered lessons from incidents (→ [05], [14])
  plans/                # future plans, RFCs, decisions (one file = one topic)
    NNNN-tytul.md
```

- **`/docs/plans/`** — a living backlog of decisions and designs. A plan is a document, not a thought
  in your head: problem → options → choice → "why." A finished plan stays as a record of the decision.
- **A folder without an `AI_README.md` is a mystery folder.** When you create a new significant directory, create it
  **together** with an `AI_README.md` (even a skeleton). Same when refactoring: you break a module into subdirectories →
  each new directory gets its map in the same step, not "later."
- **The more concrete, the better.** A better folder structure (clear boundaries: data / ingest / web /
  scripts, → [12](12-flexibility-and-scalability.md)) + a denser, concrete `AI_README` in each of
  them beats one vague file in the root. Keep important information (gotchas, contracts, numbers)
  **close to the code it concerns**.

## When to update (and when not)

| Change | Update the documentation? |
|--------|----------------------------|
| New module / function / script / CLI flag | ✅ |
| New migration / column / table | ✅ (DB doc + scripts doc) |
| Change in the number of tests / records | ✅ |
| Change in behavior (new threshold, new fallback) | ✅ |
| Pure bugfix with no API/structure change | ❌ (note that you checked) |
| Typo, formatting | ❌ |

## Documentation as code
- **The source of truth is `.md`** — hand-written, versioned in git like the rest of the code. The history of the docs
  (`git log` over the `.md`) tells you *when and why* a rule changed. Don't keep the truth in generated HTML.
- **Relative links** between `.md` files — so they can be clicked and validated.
- **One "table of contents"** (e.g. `docs/AI_README.md`) with a "where to start for task X" table.

## The documentation reader and regeneration

`.md` is the source of truth, but a human reads more comfortably in a browser. Add a **simple reader
`documentation.html` in the repo root** — it renders the `.md` (e.g. `marked`), versioned in git like
every file. One file, no bundler; works from a double-click and from a server (this codex itself works that way).

- **The generated artifact (snapshot/HTML) is a derivative, not the source.** Commit it, but **never
  edit it by hand** — the build will overwrite it.
- **Regeneration does NOT fire by itself.** No auto-build on every commit (noise, lag,
  conflicts). You run it **on command** — best via a skill (→ [02](02-skills-and-refactoring.md)),
  not a hook.
- **The regeneration skill looks at git since the last docs update.** Instead of blindly rebuilding
  everything: it reads `git log <last-docs-commit>..HEAD` (or from a `docs-*` tag), sees **what actually
  changed** (Commandment II → [05](05-git-and-deployments.md)), updates the touched sections, and
  **prints what it changed**. Cheap, deliberate, checkable — instead of "rebuild and trust."

## Anti-patterns
- 🚫 "I'll update the docs at the end" → the end never comes, the documentation lies.
- 🚫 An AI_README describing *intent* instead of *state* — the agent acts on what's written, not on wishes.
- 🚫 Duplicating state from `CLAUDE.md` into five places — one source of truth, the rest link.

## In practice
Starting a new project: first `CLAUDE.md` (stack, how to run it, policies and **hard domain
rules** — e.g. privacy, legal constraints), then `AI_README.md` in the directories that carry the most
weight (auth, i18n, data pipelines). Record overriding rules (e.g. privacy-by-design) as a
**policy in the constitution**, not as a loose note. → [07](07-new-project-day-0.md)
