# 16 — Driving Claude: skills, models, autopilot, background, agentic work

> The rest of the doctrine is about **building**; this chapter is about **operating the agent well.**
> Claude Code has features that change the cost and speed of *every* task. Use them deliberately —
> the difference between a slow, click-heavy session and a fast one is mostly here.

## Skills and slash-commands

A **skill** is a reusable procedure invoked with a slash (`/run`, `/run-tests`, `/add-migration`,
`/update-ai-readme`). It codifies "how we do it here", so the agent runs a **proven recipe instead of
guessing** each time. Build your own for repeatable flows; lean on the built-in ones too. Discipline and
"when to build one" → [02](02-skills-and-refactoring.md).

- **Create a custom slash-command** for any flow you repeat (≥3 times, or easy to get wrong). One clear
  command for the agent + a human fallback; a clear exit contract (0 = green).
- **A skill is a recipe (for the agent), not a hook** (automation the harness runs). "Always do X after Y" =
  a hook in config, not a skill.

## Pick the model for the task

Match the model to the job — it's a cost/quality dial, not a default:

- **Fast/cheaper model** for bounded, mechanical work: renames, simple edits, lookups, mechanical refactors.
- **Powerful model** for the hard 10%: architecture, gnarly multi-file bugs, design with real trade-offs.
- **Switch mid-session** as the task changes. Don't pay top-tier for `git status`; don't cheap out on the
  migration that can lose data. If a cheap model loops or stalls, **escalate**; if a strong one is idle on
  rote work, **drop down**. Measure by outcome, not by habit.

## Autopilot — the preferred default

**Prefer running on autopilot** (autonomous / auto-accept) for low-risk, well-scoped work. It's faster and
keeps you the **architect of decisions, not the clicker of confirmations.**

- **Set the guardrails once, then let it run.** Policies in `CLAUDE.md` (never deploy/push without "deploy";
  dry-run is the default; prod is sacred) are what *make* autopilot safe — the agent executes freely *inside*
  them and commits often, pausing only for what's irreversible or outward-facing (→ [06](06-collaboration-and-memory.md), Commandment VI).
- **The hard gates still need an explicit "yes":** deploy, prod DB swap, push/publish, destructive deletes,
  anything outward-facing. Autopilot ≠ unsupervised on dangerous ops.
- **The win:** you review **plans and outcomes**, not every keystroke. Plan → iterate → review (→ [06](06-collaboration-and-memory.md)) at the altitude of decisions.

## Run long things in the background

Long operations — dev servers, builds, test suites, scrapers, deploys — **run in the background** so the
session keeps moving; you're notified when they finish.

- **Don't block the conversation polling a long job.** Background it, continue other work, read the result
  when it lands.
- **Pair with resumable/checkpointed jobs** (→ [14](14-operational-resilience.md), [15](15-scraping-ai-and-chatbots.md)) for anything that can die mid-run — a background job that isn't resumable just fails out of sight.

## Agentic workflows — fan out when it pays

For work that **decomposes** — broad search across many files, multi-dimension review, parallel independent
edits, a large migration — **spawn subagents and run them concurrently.** You keep the **conclusion**, not the
raw file dumps.

- **Patterns:** parallel readers → synthesis; find → **adversarially verify** each finding; migrate
  site-by-site in isolation; loop-until-dry for unknown-size discovery.
- **Deterministic workflow** (orchestrated subagents: fan-out → verify → synthesize) for large, structured
  passes where control flow should be code, not model-driven. A **single agent** for a focused lookup.
- **Cost-aware:** fan-out burns tokens. Reach for it when breadth, parallelism, or independent verification
  genuinely helps — not for a one-line fix.

## Anti-patterns
- 🚫 **Top-tier model for `git status`; a cheap model for a data-losing migration.** Wrong dial both ways.
- 🚫 **Hand-confirming every safe edit** instead of autopilot within set guardrails — slow, and it trains you to rubber-stamp.
- 🚫 **Blocking the session** on a long job you could have backgrounded.
- 🚫 **One serial agent for embarrassingly parallel work** — or a 12-agent workflow for a trivial change.
- 🚫 **A custom skill for something done once** — that's just overhead (→ [02](02-skills-and-refactoring.md)).

## For new projects
Set the `CLAUDE.md` guardrails **first** (so autopilot is safe), add your repeatable skills early
(`/run`, `/run-tests`), default to **autopilot + background** for the grind, switch models by task, and
reach for **agentic workflows** on the big sweeps. → [02](02-skills-and-refactoring.md), [07](07-new-project-day-0.md)
