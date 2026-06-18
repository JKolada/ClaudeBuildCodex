# What The Craft is

> **The Craft is the art of building end-to-end applications with Claude — apps that are scalable,
> maintainable, and easy to keep evolving, migrating, and changing across the whole life of the
> project.** Not a framework, not a library — a **human + agent doctrine**: a tight set of rules,
> commandments, and anti-patterns that keep the code understandable to the next session, testable,
> safe to change, and trustworthy — from the first commit to production with real users.

## In one paragraph

Most AI-built projects don't fall apart because the agent can't write code — they fall apart because
**nobody set the rules**. The Craft is those rules: you attach them to a project as `docs/rules/`, and
from **Day 0** Claude knows "how we do things here." The result is an app with an **extremely flexible
structure of files and technologies** — you start simple (one server, one database), and the structure
is ready for growth from the outset: separated layers, feature flags, forward-only migrations, slug
instead of ID. You evolve, migrate, and scale **without rewriting from scratch** — all with **respect
for personal privacy and the law** (GDPR, consents, protecting the creator) built in from the start,
not bolted on at the end.

## What you get

- **Code that reads like prose** — matched to its surroundings, easy to review for a human *and* an agent.
- **Git history as the project's memory** — search before you write; never reinvent what already exists.
- **Verification instead of declaration** — "it works" means proof: a smoke test, an HTTP code, numbers, a screenshot.
- **Safe changes** — dry-run by default, a backup before every migration, production is sacred, user data is untouchable.
- **Flexibility and scalability** — a monolith on a single VPS as the simple default, with an explicit growth path (SQLite → PostgreSQL, VPS → serverless) when a metric forces it.
- **Legal peace of mind** — terms of service, a privacy policy, and disclaimers as the creator's armor, not an afterthought.

---

# Why you should try building an app with The Craft

**Because the difference isn't *whether* the agent writes the code — it's what your project looks like
three months from now.** Without rules, every agent session adds a little chaos: inconsistent style,
documentation that lies, a migration with no backup, a deploy "because it's done." A quarter later you
have an app you're afraid to touch. The Craft reverses that trajectory: **every change leaves the
project cleaner, not worse.**

**You start fast, not cheap.** One server, a simple stack, a monolith — something you can hold in your
head: one deploy, one log, one backup, one rollback. That isn't "primitive" — it's **cheap to
maintain**. And when real scale finally arrives, the structure is already waiting for it: layers are
separated, keys are stable, migrations are one-way. Growth and migration stop being a rewrite and
become an addition.

**Human and agent play toward the same goal.** Plan → iterate → review. The agent doesn't guess — it
follows a proven recipe, searches the history, reports honestly (failures included, not just wins). You
stay the architect of decisions, not the proofreader of chaos. It's a collaboration where **trust is
built on proof**, not optimism.

**Privacy and the law are handled from Day 0.** GDPR, consents, retention, protecting the creator —
written as policies into the project's constitution before the first real user shows up. No late-night
scrambles "because someone asked to delete their account."

**Best of all: it's reusable.** The Craft isn't built "for one project." You attach it as `docs/rules/`
to **every** new app, fill in the [brief](index.html#brief), and go — and each new project benefits
from the lessons of the last.

> **Try it once.** Take your next idea, attach The Craft, start from [Day 0](07-new-project-day-0.md),
> and build it like a craftsman — slow where a mistake is expensive, fast where it's cheap. You'll see
> the difference not on day one, but in **month three** — when the app is still a pleasure to work on.
> Start with the [Decalogue](00-commandments.md): the whole doctrine on a single screen.
