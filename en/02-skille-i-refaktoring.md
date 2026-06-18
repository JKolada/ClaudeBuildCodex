# 02 — Skills and refactoring

> Commandments I and X: automate the repeatable; refactor so the code reads like its neighbor.

## Skills (slash-commands) — when and why

A skill is a repeatable procedure wrapped in a single invocation (`/run-projekt`, `/run-tests`,
`/update-ai-readme`, `/add-migration`). In the reference project, skills proved to be a lever, because they
**codify "how we do it"** — the agent doesn't guess, it follows a proven recipe.

### Build a skill when:
- you repeat the procedure **≥3 times** (start server + 22 smoke-checks, run tests, add a scraper);
- the order of steps is **easy to get wrong** (migration: number → SQL → `migrate.py` → AI_README → commit);
- there's a **project-specific "gotcha"** the agent must remember every time
  (e.g. "on Windows set `PYTHONIOENCODING=utf-8` before the scraper," "Jest with `--runInBand`
  when the server is running").

### A good skill has:
- **one command for the agent** + one for the human (fallback);
- a **clear output contract** (exit 0 = green; exit 1 = what failed);
- a **list of gotchas** specific to the platform/project;
- a "when it's NOT needed" section.

### Anti-patterns
- 🚫 A skill for something you do once — that's pure overhead.
- 🚫 A skill that hides what it does — when it runs something destructive, it must **print it** (e.g. "I removed dead code").
- 🚫 Confusing a skill (a recipe for the agent) with a hook (automation run by the harness).
  "From now on always do X after Y" = a hook in the config, not memory/a skill.

## Refactoring — the discipline

> **Golden rule:** write code that reads like the code next to it. Match comment density,
> naming, and idiom to the surroundings. Consistency > your preferences.

### Rules
1. **Search for prior art before refactoring** (Commandment II). Before you rewrite — `git log -S`,
   `git blame`. Often an "ugly" shape has a reason (compatibility, an edge-case, an old decision).
2. **Refactor separately from a behavior change.** One commit = either cleanup or a new
   feature. Mixing them makes review and rollback harder.
3. **Reuse > rewrite.** First check whether a helper already exists (a matcher, a normalizer,
   `upsert_price`). Duplicated logic is debt.
4. **Backward-compat on structural changes.** In the reference project, moving the scripts into
   subpackages left shims re-exporting from the old paths — old calls still
   work. Don't break others' entry points.
5. **Small steps, verified.** Refactor → tests green → commit. Not "one big rewrite at
   once," after which you can't tell what broke.

### Quality without bug-hunting
Separate the two review modes (like `/simplify` vs `/code-review`):
- **Simplification/reuse/efficiency** — cleanup, without hunting for bugs.
- **Correctness review** — adversarial bug-hunting.
Don't mix them — each has a different goal and a different confidence bar.

## SOLID — design that doesn't clog up

> Not a dogma, but **five tests of whether a change will be cheap**. Apply it proportionally to
> risk (→ [12](12-elastycznosc-i-skalowalnosc.md): don't over-engineer). SOLID is not a pretext
> for "just in case" layers of abstraction.

- **S — Single responsibility.** One module = one reason to change. It's the same discipline as
  "one commit = one thing" (refactor or behavior, not both). A function you have to touch
  for three unrelated reasons is three functions.
- **O — Open/closed.** Extend without cutting into proven code. This is where **feature flags**
  plug in (→ [12](12-elastycznosc-i-skalowalnosc.md)): you add the new path behind a flag and ship dark,
  instead of rewriting the existing branch and risking a regression.
- **L — Liskov.** A subtype must honor the supertype's contract — no "exception that breaks everything."
  If an implementation breaks the caller's assumptions, it's not a subtype, it's a trap.
- **I — Interface segregation.** Narrow, purposeful interfaces instead of one god-interface.
  A caller shouldn't depend on methods it doesn't use.
- **D — Dependency inversion.** Depend on an abstraction, not a concrete. It's the code-level counterpart of
  "separate the layers" (→ [12](12-elastycznosc-i-skalowalnosc.md)): the logic doesn't hardcode the database
  or queue provider — it receives it across a boundary, so it can be swapped (and tested, → [03](03-testowanie-i-weryfikacja.md)).

### Anti-patterns
- 🚫 **SOLID as a cult** — five layers and a factory of factories for a three-field CRUD. Rule D is meant to
  ease swapping, not multiply files. Measure the need, don't quote the letters.
- 🚫 **Open/closed without flags** — you "extend" by editing a hot path in place with no toggle
  and no ramp (→ [12](12-elastycznosc-i-skalowalnosc.md): no feature flags).
- 🚫 **Abstraction before there are two cases** — an interface extrapolated from a single use guesses the future.
  Get the second concrete case first, then the shared contract (reuse > rewrite, but not reuse > reality).

## In practice
- Skills to start: `/run` (server + smoke), `/run-tests` (unit + e2e), `/update-ai-readme`,
  `/add-migration` (if a relational database). → [08](08-stack-i-technologie.md)
- Do a refactor of a critical path (e.g. login) as a **separate, tested** step: first a
  test reproducing the current state/bug, then the change. → [03](03-testowanie-i-weryfikacja.md)
