# 14 — Operational resilience and external dependencies

> Commandments III, V, VI at the runtime layer: *prod lives in an unreliable world*. The network
> drops, the provider blocks ports, the scraper dies halfway, a paid API costs on every request.
> The doctrine in chapters 03–05 covers **code and deployment**; this chapter is about what
> happens **after** — when real users and independent systems hit a running service.

These lessons were paid for dearly: nearly every one is a prod incident, not theory. The common
denominator — **the worst bugs don't shout, they quietly hang, log out, or drain the budget.**

## 1. One bad request must not take down the process

An uncaught `throw`/rejection in an async handler can kill the **entire** server (Node/Express:
rejection → process exit → pm2 restart loop). Build a net at the process level:

- **Global catchers**: `process.on('unhandledRejection')` and `'uncaughtException')` — they log and
  shut down in a controlled way, leaving no zombie process.
- **An async-route wrapper** that passes the error to `next(err)` instead of losing it in an uncaught promise.
- **500 middleware** that **doesn't leak the stack trace** to the user (→ [09](09-law-and-protecting-the-creator.md)).
- **Defense on edge data**: an OAuth account with no password, a `null` field where the code assumes a string —
  these are real inputs once you let real users in (often surfaces **after a database swap**, → [05](05-git-and-deployments.md)).

> Rule: *a throw in one request degrades that request, not the service.* Test it for regressions (→ [03](03-testing-and-verification.md)).

## 2. Long jobs: resumable and detached from the agent session

A "collect everything → save once" scraper/ETL loses 100% of its work on every crash. Write in **batches**:

- **Checkpoint completed units** (a file/table of URLs/IDs) — a restart resumes from where it left off, not from scratch.
- **Save every N**, not at the end — a crash costs the last batch, not the whole run.
- **Run long jobs from a real terminal**, not from a Claude session in the background. The agent's
  background is a **non-durable runner** — tearing down the session host kills the process halfway
  (it's not anti-bot, it's a vanishing runner).
- End-to-end idempotency (→ [04](04-scripts-and-databases.md)): a resumed job doesn't duplicate already-saved data.

## 3. Treat external sources as hostile

Other people's APIs and pages drop connections, rate-limit (429), return 200 with an error page. Assume they're unreliable:

- **A timeout on every call** — without it the socket hangs forever (a silent freeze, not an error).
- **Retry with exponential backoff** (e.g. 10/20/30 s), with an upper bound on attempts.
- **Rotate session and User-Agent** under heavy I/O — a fresh `Session` (new TCP/cookies) per batch,
  a UA from a pool of real browsers (some hosts drop you after a few hundred requests from one session).
- **Validate the response, not the status** — a "200 + error page" is a failure; check the shape of the data.

## 4. The provider's infrastructure imposes limits — verify end-to-end

Hosting has its own network rules that break "working" code only in prod:

- **Ports can be blocked.** E.g. outbound SMTP 465 may be closed → use **587 + STARTTLS**.
  `secure:true` on a blocked port **hangs every send** until timeout — set hard
  connection/greeting timeouts so the error is loud.
- **Mail deliverability isn't "I sent it."** A verified sender domain (SPF/DKIM), a real
  test send, GDPR-compliant opt-in (→ [09](09-law-and-protecting-the-creator.md)). An email that
  "went out" but landed in spam/nowhere is a bug.
- **Check this on the provider's prod/staging**, not locally — your local network doesn't have these blocks (→ [03](03-testing-and-verification.md)).

## 5. Every paid resource behind a hard quota

An endpoint calling a paid API (LLM, geocoding, email) with no limit is an open tab and an abuse vector:

- **A quota per user** (monthly/daily window) with a **clear message** and a **reset date up front**.
- **Differentiate per tier** (free vs premium), enforce it server-side.
- **Rate-limit + security headers** (helmet/limiter) as a permanent part of the stack (→ [08](08-stack-and-technologies.md)).
- Tie it to the law and the terms of service: a limit and how you communicate it are also protection against abuse (→ [09](09-law-and-protecting-the-creator.md)).

## Anti-patterns
- 🚫 **No global error catcher** — one bad request restarts the service for everyone.
- 🚫 **A scraper with no checkpoints** run from the session background — crash = run from scratch, vanishing runner = perpetual failure.
- 🚫 **An external call with no timeout and backoff** — a silent freeze or a ban after a string of 429s.
- 🚫 **"I sent the email" ≠ I delivered it** — no verification of port/domain/deliverability.
- 🚫 **A paid API with no quota** — a surprise bill and an open abuse vector.
- 🚫 **Sessions in process memory** — every deploy logs everyone out (→ [05](05-git-and-deployments.md)).

## For new projects
Add to Day 0 (→ [07](07-new-project-day-0.md)) **before** the first real user shows up:
a global error handler + a 500 with no leak, timeouts and backoff on every external I/O, quotas on
paid endpoints, a durable session store in a separate file. It's cheaper now than as a 2 a.m. incident.
Every prod incident → an entry in the runbook with a date and a numbered lesson (→ [05](05-git-and-deployments.md), [06](06-collaboration-and-memory.md)).
