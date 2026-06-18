# 03 — Testing and Verification

> Commandment III: *Verify, don't declare.*

Two different things, often conflated:
- **Tests** — an automated safety net you run repeatedly.
- **Verification** — proof that *this specific change* does what it was meant to, **observed**, not assumed.

Both are mandatory. A passing test doesn't mean the feature works in the browser;
manual verification without tests won't protect you from tomorrow's regression.

## The pyramid (from the reference project)

| Level | Tool | What it covers | When |
|-------|------|----------------|------|
| **Unit** | pytest / Jest | pure logic (normalizer, matcher, helpers, validators) | every commit |
| **Integration** | Supertest (HTTP) | routes, auth guards, JSON API | every commit |
| **E2E / browser** | Playwright | real browser paths, on a separate port | before deploy / when touching UI |
| **Smoke** | script (`smoke.ps1`) | "does the server come up and do N routes respond correctly" | after restart / before and after deploy |

Rules that have proven themselves:
- **Run the tests before committing** the critical path.
- **Jest with `--runInBand`** when a dev/preview server is running (port/DB conflicts).
- **Smoke tests have markers** — they check that the *right* page rendered (e.g. `price-gate`
  for an anonymous user, not just HTTP 200).
- **Test auth from both sides** — anonymous user bounced to login **and** logged-in user sees the content.

## "Verify, don't declare" — in practice

After a change observable in the app, **show proof**; don't ask the user to check it themselves:
- HTTP status / `redirect_url` (curl `-o /dev/null -w`),
- a confirming HTML fragment (e.g. `og:image` points at the right file),
- numbers from the database (how many accounts, how many prices, `integrity_check: ok`),
- a screenshot for visual changes.

After a **deploy** — a smoke test against the live server (via `localhost`, behind the maintenance
flag); and when you find a bug inside the window, fix it in the window if it's trivial and safe (in the
reference project this is how we caught and fixed a pre-existing `ERR_HTTP_HEADERS_SENT` on `/mapa`).

## The report must be honest
- Tests fail → say so **with the output**; don't hide it.
- Something was skipped → say it was skipped.
- When 2 tests fail from **data drift** (e.g. cohort fixture `85% vs 85%`) rather than a regression
  — **flag it explicitly**, don't let it block the deploy, but propose a follow-up (regenerate the fixtures).
- Say "done and verified" only when it's actually verified — no hedging, but no bluffing either.

## Verify numbers at the source
Don't trust a number from memory or from the docs — query the database/test. Docs go stale;
`SELECT COUNT(*)` doesn't lie. (Commandment X: "verify the numbers".)

## Web — a proven set of checks
For web sites/projects this set of tests has already proven itself in practice (a typical set runs
to a few dozen methods and a few hundred subtests) — carry it over by default:
- **SEO meta** (title/description per page), **canonical + hreflang**, **JSON-LD**.
- **Accessibility**: color-token contrast, keyboard navigation, sensible `alt`/aria.
- **EN↔PL parity** (and every language pair): a missing key/page in one language = **a test that fails**.
- **Dead internal links** — no link in the build leads into the void.
- **Theme consistency** (theme cookie / dark-light) and build correctness (every page rendered).

## Anti-patterns
- 🚫 "Should work" as a conclusion.
- 🚫 Running a single test and declaring "suite green".
- 🚫 Skipping the smoke test after deploy because "the tests passed anyway".
- 🚫 Confusing "the code compiles" with "the feature works for the user".

## TDD — the default working mode

Test **first**, not after the fact. The cycle:
1. **Red** — write a test that describes the expected behavior and **fails**.
2. **Green** — the smallest code change until the test passes.
3. **Refactor** — clean up against a green suite (→ [02](02-skille-i-refaktoring.md)).

You fix a bug the same way: **first a test that reproduces** the bug, then the fix — the test stays
as a regression guard so the bug doesn't come back.

> **Every change in a commit carries a test.** Hard rule: a commit that changes behavior but
> doesn't add/change a test is **incomplete**. New endpoint → route test; new threshold/fallback
> → threshold test; fixed bug → regression test. "I'll add tests later" = a sin (later never
> comes). → [00](00-przykazania.md), [08](08-stack-i-technologie.md)

- **Test the contract, not the implementation** — otherwise a refactor crumbles tests with no real regression.
- **Keep the suite fast and deterministic** — a slow or flaky suite stops getting run;
  isolate I/O, set seeds, `--runInBand` on a shared port/DB.
- **CI gates** — red tests block merge and deploy; you run critical-path tests before committing.
