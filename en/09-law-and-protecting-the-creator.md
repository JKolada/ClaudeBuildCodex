# 09 — Law and protecting the creator

> Commandments VI and VII extended to the outside world: *prod is sacred, user data inviolable* —
> and now a third exposed party joins: **you yourself.**

A solo creator or a sole proprietorship shipping a public application is **personally exposed**. This is not
a limited-liability company with a liability shield — a private individual running a business answers
for the terms of service, the privacy policy and the promises in the copy. Terms of service, the privacy policy and
disclaimers are **the private person's armor**, not a formality tacked on at the end. You write them just as
carefully as a migration on prod — because a mistake is just as costly, only paid in a different currency.

> ⚠️ **These are engineering pointers, not legal advice.** When you start binding real users
> and at scale — consult a lawyer. The following is hygiene that lowers risk, not a shield
> that zeroes it out.

## Terms of service — what must be there
- **The correct operator.** "[Full name], trading as …, tax ID …,
  address …". **The same entity** across the terms, the policy, the footer, invoices and the UI. A discrepancy
  is the first thing an unhappy user notices.
- **Nature of the service.** Take a price comparison site: *a comparison engine, not a seller* — it does not sell,
  does not act as an intermediary, it links to shops. By analogy, an advisory application must clearly
  state what it is **not**: *information/support, not a regulated service* (medical, legal, financial, therapeutic).
- **User obligations** (lawful use, no abuse/scraping, acceptance of age restrictions, e.g. 18+).
- **Limitation of liability** — service "as is", no warranty of availability/correctness
  of data, **no liability for decisions** made on its basis (a price at a retailer may
  be stale; a chatbot's advice does not replace a specialist).
- **Moderation and termination** — the right to suspend/delete an account on abuse.
- **IP** — the user **retains** their content (reviews, conversations) and grants you a license to
  process it within the scope of the service; your content (catalog, code, brand) is **reserved**.
- **Governing law = Poland**, competent court, complaints procedure, **changes** to the terms (how
  you notify), **contact**.

## Privacy policy (GDPR) — what must be there
- **Data controller** named correctly (the same operator as in the terms).
- **Scope** of data collected, **purpose + legal basis** for each (consent / contract / legitimate
  interest), **retention** (how long you keep it).
- **Anonymization** — if you declare that you anonymize, it **must be true in the code**
  (e.g. a processing pipeline running exclusively on anonymized data, → [11](11-data-model-and-normalization.md)).
- **Third parties** (Google Cloud / GA4, Resend, Hetzner) — listed, with purpose.
- **Rights**: access, rectification, **erasure** (e.g. a 14-day grace period → purge,
  public reviews anonymized to "Account deleted"), export, objection.
- **Cookies** (GA4 is an analytics cookie — list it), **age** (e.g. 18+, if content is age-restricted), **contact** for the controller.

## Protecting the private person
- **Separate the legal entity from your private identity.** The operator is the *sole proprietorship*, not a private
  home address, wherever that can be avoided.
- **Do not invent legal data.** Tax ID, address, company name = **placeholders to be filled in**
  by the owner, never made up. A visible `[tax ID to be filled in]` is better than a plausible-looking,
  false number in the product.
- **Do not declare practices you have not implemented.** "We anonymize conversations" without code that
  does it is not marketing — it is a **false statement by the data controller**. → [03](03-testing-and-verification.md)
- **Lawyer review** before binding real users and at scale.

## Disclaimers as a shield
- **Age-restricted content (e.g. 18+)** — an age gate (e.g. an 18+ checkbox as a registration
  gate; when the domain is subject to advertising regulation — e.g. strict rules on promoting
  certain product categories — limit what you show publicly, e.g. **no price on the
  public OG card**, and stay cautious about those rules).
- **"This is not advice"** — medical / legal / financial / therapeutic, depending on the domain.
- **Crisis resources per region** (e.g. links to helplines in the user's language, →
  [10](10-seo-and-translations.md)) — without pretending to be a specialist.

## Consistency: terms ↔ policy ↔ UI ↔ code
The three documents and the product must say **one thing**. If the policy says "we do not read conversations", then
no user-facing process may read them — that claim is **architectural**, verifiable by a
test (→ [11](11-data-model-and-normalization.md)). If the terms say "a comparison engine without
affiliation", then there are no affiliate links in the code — **neutrality is a legal shield**
(no conflict of interest = no charge of hidden advertising). A contradiction between layers is
worse than a missing clause.

## Anti-patterns
- 🚫 **An invented tax ID/address/company name** in the product — instead of a placeholder to be filled in.
- 🚫 **Copy promising more than the product delivers** ("fully anonymous", "we guarantee prices").
- 🚫 **Terms contradicting the policy** (different operator, different data scope, different retention).
- 🚫 **A hardcoded English legal page** in a multilingual product (→ [10](10-seo-and-translations.md)).
- 🚫 **Declared anonymization without implementation** — a false statement, not marketing.
- 🚫 Different naming of the operator in the footer, the terms and on the invoice.

## For new projects
Put the three legal documents (terms of service, policy, disclaimers) into the **Day 0 checklist**
(→ [07](07-new-project-day-0.md)) as a task with `[to be filled in]` placeholders, not
"later". Settle the operator (company name / full name) once and insert it consistently everywhere.
Every claim about data ("we anonymize", "we delete after N days", "we do not share")
**verify in the code** before publishing. Once you have real traffic — get a lawyer to review it. This is the chapter
where "verify, don't declare" (→ [03](03-testing-and-verification.md)) protects not the users,
but you.
