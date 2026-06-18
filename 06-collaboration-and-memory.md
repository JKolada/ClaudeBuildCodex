# 06 — Collaboration and Memory

> Commandments VI and X: how we work together and how we keep from losing context.

## Collaboration style (user + Claude)

- **Plan → iterate → review.** First show a plan or a **small sketch** (3 examples, not 100),
  gather feedback, then scale. OG cards in the reference project: 3 → fixes → 10 → fixes
  → 100. Never the other way around.
- **Recommend; don't lay out a menu of options.** When weighing a choice, give a
  **recommendation** with reasoning, not an exhaustive list you won't act on anyway. Ask only when
  the answer genuinely changes what you do next (and when it doesn't follow from the code or a sensible default).
- **Verify numbers at the source** — not from memory, not from docs.
- **UX with warmth.** Correctness is the minimum; the product should be pleasant. Aesthetics and tone
  matter (especially in sensitive products: minimalist, but warm).
- **Language:** PL in conversation and changelog, EN in code/commits/technical docs — the way we
  naturally work. Technical terms in English within Polish text are fine.
- **Separate unrelated things** — in commits and in thinking. One topic at a time.

## Confirm what's irreversible and "external"

Actions that are hard to undo or that reach beyond the machine — **confirm first**, unless you have
standing authorization or an explicit "do it without asking":
- prod deploy, sending emails, publishing content, deleting/overwriting data.
- **Consent in one context does not carry over to the next.** "Deploy X" ≠ "deploy everything, always".
- **Before you delete/overwrite — look at the target.** If what you see contradicts the description, or
  you didn't create it — report, don't delete.
- Publishing to an external service = content may get indexed/cached, even after deletion.

## Memory (cross-session)

The agent's file-based memory (`memory/`) holds what **can't be read from the code/git**:
- **who the user is** (role, preferences), **feedback** (how I should work — with the "why"),
  **project state** not derivable from the repo, **pointers** to resources (URLs, dashboards, issues).
- **Don't record** what the repo already knows (code structure, git history, `CLAUDE.md`).
  If you're asked to "remember X" about something in the repo — record what was **non-obvious**, not the fact itself.
- **Relative dates → absolute** ("next week" → a concrete date).
- Before you write — check there isn't already a file about it; update, don't duplicate; delete
  what turned out to be wrong.
- **Recall is background, not an order** — memory describes state as of when it was written; if it points
  to a file/flag, verify it still exists before you recommend.

## Reporting (Commandment III, once more, because it matters most)
The facts > a good impression. "Tests failed — here's the output." "A step was skipped." "Done and
verified" — without hedging, when truly verified.

## Anti-patterns
- 🚫 Scaling before review.
- 🚫 A survey of options instead of a recommendation.
- 🚫 Overwriting/deleting without looking at the target.
- 🚫 Memory as a dumping ground for facts from the repo.
- 🚫 Treating one-time consent as standing.
