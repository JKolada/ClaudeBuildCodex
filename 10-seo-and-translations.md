# 10 — SEO and translations

> Commandment III extended to visibility: *verify, don't declare* — including that the site
> is indexable, complete across all languages and measured, not "it probably looks OK".

An application nobody can find does not exist. SEO and i18n are not a marketing layer tacked on
at the end — they are a **contract with the search engine and with the user** that the site is understandable to
the crawler and complete in its language. Just as AI_README is the interface for the agent, so metadata
and translations are the interface for the world.

## SEO fundamentals (every page)
- **`<title>` + `meta description`** unique per page (not one global one).
- **Canonical** — one URL of truth for each piece of content (protects against duplicates from parameters).
- **hreflang** — mandatory once you go multilingual: each language version points to the others
  (e.g. 16 languages → 16 reciprocal `hreflang` + `x-default`).
- **JSON-LD** — `Organization` (home), `Article` (blog/posts), `ItemList` (rankings).
- **`sitemap.xml`** (with priorities) + **`robots.txt`** (what to index, where the sitemap is).
- **Semantic headings** (one `h1`, an `h2/h3` hierarchy), **OG/Twitter cards** (e.g.
  OG share cards — but **no price on the public card** when the domain requires it, → [09](09-law-and-protecting-the-creator.md)).
- **Clean slugs** (`/ranking/produkty-do-200-zl`, not `?id=42`) and **internal linking**
  (nav-drawer + footer + contextual links between pages).

## Programmatic and editorial SEO
- **Programmatic** — curated landing pages targeting **transactional queries**. In the reference
  project: several `/ranking/:slug` pages ("products under 100/200/300 PLN", "best in category X", "for a gift")
  — each a **hand-written intro** PL/EN + a numbered **TOP-N** + a full filterable table +
  `ItemList` JSON-LD. **Quality guards** are part of SEO: qualifying filters, `requireRating`,
  `minShops` — so the page is not a thin shell.
- **Editorial** — content hubs/blog targeting **informational queries** (e.g. topical guides
  about products). Content that **genuinely answers** the question, not keyword-stuffing.

## E-E-A-T and YMYL
Google rates **YMYL** (Your Money or Your Life) pages rigorously — health, finance,
religion, safety. A price comparison site falls into this, for instance (spending, age-restricted content), as does any
health, finance or support application. What counts is **E-E-A-T**: Experience, Expertise, Authoritativeness, Trust.
- Reliability and **sources** (where the price comes from, where the rating comes from — the reference project links the external data source/shop).
- **Authorship** and a clearly named operator (→ [09](09-law-and-protecting-the-creator.md)) build Trust.
- **Zero medical advice** in health/support products — a disclaimer + a crisis path, not a diagnosis.

## Core Web Vitals as a ranking factor
Speed is not only UX — it is a ranking signal. LCP/CLS/INP feed into the page's assessment. Measure and
fix (→ [13](13-performance-frontend-and-sql.md)); not "it feels fast", but numbers.

## Translations / i18n
- **Completeness = a test that fails.** A missing key or a page in any language → the test
  fails (in practice: **EN↔PL parity** + dead links). No language "half done".
- **hreflang** ties the versions together (see above).
- **A warm register in EVERY language** — this is not literalness, it is tone. A translation that is
  grammatically correct but cold is a bug (e.g. "we're here to help" must sound warm in
  Arabic just as it does in Polish).
- **MT + human review for sensitive content** — Gemini translates the skeleton, a human
  reviews the disclaimers, the crisis messages, the legal copy (→ [09](09-law-and-protecting-the-creator.md)).
- **RTL** (Arabic) — the whole layout must mirror, not just the text.
- **GA4 + Search Console** (anonymized) — *which queries convert*, in which language
  traffic is growing. The data steers where to write the next landing.

## Anti-patterns
- 🚫 **SEO spam** / keyword-stuffing — Google penalizes it, does not reward it.
- 🚫 **Thin programmatic pages** with no value (TOP-N without quality guards, 2-shop shells).
- 🚫 **No hreflang** in a multilingual application → the search engine serves the wrong language.
- 🚫 **Cold / wrong MT** in a sensitive product without human review.
- 🚫 **English UI or legal pages** in a 16-language application (→ [09](09-law-and-protecting-the-creator.md)).
- 🚫 **Ignoring Core Web Vitals** — a slow page loses ranking and the user (→ [13](13-performance-frontend-and-sql.md)).

## In practice
i18n from day one in a global application (e.g. 16 languages, next-intl): hreflang for every
pair, a **parity test** as a CI gate, RTL for right-to-left languages, a warm register in
every language. YMYL content (health/support/finance) — zero regulated advice, clear authorship
and operator, crisis resources per region. Search Console from the start, so you know **which languages
and topics** drive traffic. → [09](09-law-and-protecting-the-creator.md), [13](13-performance-frontend-and-sql.md)
