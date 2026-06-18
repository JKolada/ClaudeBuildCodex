# AI_README — katalog Rzemiosło (The Craft)

> Mapa katalogu dla następnej sesji / innego agenta. Czytaj **przed** dotknięciem plików tutaj.
> Konstytucja repo: [CLAUDE.md](CLAUDE.md). Test jakości tego pliku: czy po przeczytaniu możesz
> bezpiecznie zmienić cokolwiek w tym katalogu, nie skanując wszystkich plików?

## Co to za katalog

Repozytorium **dokumentacji** (nie aplikacja): doktryna „Rzemiosło — The Craft" (Kolada Build).
Treść to ręcznie pisany markdown; `index.html` jest jej przeglądarką (statyczna SPA, bez build-stepu).
Cel: zestaw reguł reużywalny jako `/docs/rules/` w nowych projektach **oraz** materiał publiczny
dla osób zaczynających z Claude. Szczegóły i polityki → [CLAUDE.md](CLAUDE.md).

## Rdzeń (to repo) vs Web (siostrzane repo)

**Podział ról — nie duplikuj między nimi:**

- **To repo (`ClaudeBuildCodex`, marka „Rzemiosło") = rdzeń kanoniczny.** Forma: **techniczna, zwarta, imperatywna,
  po polsku** — źródło prawdy reguł, dołączane do projektów jako `/docs/rules/`. Optymalizowane pod
  **agenta i osobę techniczną**: gęstość ponad przystępność. Tu wersjonujemy doktrynę (codex.json).
- **Siostrzane `ClaudeBuildCodexWeb` (marka „Rzemiosło Web") = projekt prezentacyjny.** Bierze tę samą doktrynę i **rozwija
  poszczególne tematy** w przyjaźniejszej, obszerniejszej formie. **To Web — nie to repo — odpowiada za:**
  publiczną stronę, **edycje** (techniczna / BIZ-TECH / biznesowa), **wersje językowe** i **budowanie paczek
  `docs/rules/` w konkretnym języku**. Konsumuje treść tego repo + `codex.json` przy buildzie.

> **To repo jest TYLKO zestawem reguł.** Nie jest produktem prezentacyjnym. `index.html` tutaj to
> **minimalny czytnik lokalny/dev** (podgląd treści dla autora i agenta), **nie** publiczna witryna —
> dlatego nie umieszczamy tu badge'y edycji, marketingu ani przełącznika języka. Cała prezentacja,
> edycje i pakowanie wielojęzyczne dzieją się w **The Craft Web** (osobny projekt). Jeśli kusi Cię,
> by tu dodać warstwę prezentacji/marketingu/edycji — to materiał dla Web, nie dla rdzenia.

Kierunek wersji EN i pakowania per język → [docs/plans/0001-i18n-and-packaging.md](docs/plans/0001-i18n-and-packaging.md).

## Indeks plików

| Plik | Po co to |
|------|----------|
| `index.html` | **Minimalny czytnik lokalny/dev** (podgląd treści dla autora/agenta) — NIE publiczna witryna. Strona główna (dekalog + karty) + widok rozdziału + brief + przełącznik języka treści (PL/EN). |
| `intro.md` | **Manifest** — „Czym jest The Craft" + artykuł „dlaczego warto". Dokument specjalny (poza numerowaną listą), routowany jako `#intro`; jest też `en/intro.md`. |
| `00`–`15` (root) | **Treść PL** (kanoniczna, źródło prawdy). Slugi/numery = stabilne kotwice, wspólne dla wszystkich języków. |
| `en/` | **Treść EN** — równoległy zestaw `00-*.md`…`15-*.md` (te same nazwy plików, treść po angielsku). Tłumaczenie PL. |
| `docs/` | Plany i decyzje meta repo (nie treść doktryny): `docs/AI_README.md`, `docs/plans/`. |
| `content.js` | **Generowany** snapshot `.md` osadzony w JS — pozwala renderować treść po `file://`. Nie edytuj ręcznie. |
| `build.py` | Skrypt buildu: łączy pliki `.md` → `content.js`. Uruchom po edycji treści (`python build.py`). |
| `test.py` | **Smoke test** (czysty Python): parytet PL↔EN, martwe linki, świeżość `content.js`, spójność `CHAPTERS`/tabel/`codex.json`. `python test.py`. |
| `CLAUDE.md` | Konstytucja repo: czym jest, stack, jak uruchomić, polityki, stan bieżący. |
| `AI_README.md` | Ten plik — mapa katalogu. |
| `README.md` | Wejście dla człowieka: spis rozdziałów + „jak czytać". |
| `codex.json` | **Wersja wydania** (`version` + `released`) + nazwy marki (`name`/`name_short`/`name_en`). Źródło stempla dla witryny Rzemiosło Web. |
| `CHANGELOG.md` | Historia wydań Rzemiosła (semver, data = dzień publikacji). |
| `00-commandments.md` | **Dekalog** — 10 przykazań, 7 grzechów, złota zasada altytudy. Rdzeń. |
| `01-documentation-and-ai-readme.md` | Trzy warstwy docs: CLAUDE.md / AI_README / docs. Kiedy aktualizować. |
| `02-skills-and-refactoring.md` | Kiedy zbudować skill/slash-command; dyscyplina refaktoringu; SOLID (z feature flags i rozdziel-warstwy). |
| `03-testing-and-verification.md` | Piramida testów, „weryfikuj, nie deklaruj", smoke. |
| `04-scripts-and-databases.md` | Dry-run/`--execute`, idempotencja, migracje forward-only, backupy. |
| `05-git-and-deployments.md` | Szukaj w git, taguj deploy, swap bazy z zachowaniem kont. Najgęstszy rozdział. |
| `06-collaboration-and-memory.md` | Plan→iteruj→review, pamięć, potwierdzaj nieodwracalne, raportuj uczciwie. |
| `07-new-project-day-0.md` | Checklista „Dzień 0": brief produktowy (język, funkcje, monetyzacja, UX, animacje, marketing) + setup repo. |
| `08-stack-and-technologies.md` | Uniwersalny stack: Python, bazy, web/API, Docker, serwery (Hetzner) + TDD jako twardy rdzeń. |
| `09-law-and-protecting-the-creator.md` | Regulamin, polityka prywatności, disclaimery jako ochrona twórcy / JDG. |
| `10-seo-and-translations.md` | hreflang, JSON-LD, E-E-A-T/YMYL, parytet językowy jako test. |
| `11-data-model-and-normalization.md` | Słowniki lookup, slug zamiast ID, active-row, świadoma denormalizacja. |
| `12-flexibility-and-scalability.md` | Rozdziel warstwy, feature flags, scale-to-zero vs always-on, nie over-engineeruj. |
| `13-performance-frontend-and-sql.md` | Mierz najpierw, indeksy + partial index, brak N+1, streaming czatu, CWV. |
| `14-operational-resilience.md` | Crash-proof runtime, wznawialne joby, zawodne API (backoff/rotacja), limity providera + poczta, kwoty kosztów. |
| `15-scraping-ai-and-chatbots.md` | Skuteczny scraping (oficjalne źródło, walidacja kształtu, delta), AI-API do konkretnych zadań (kontrakt/cache/kwoty), konfigurowalne+ugruntowane chatboty. |

Rozdziały dzielą się na **rdzeń** (`00`–`08`) i **pogłębienie** (`09`–`15`). Każdy = jedno
przykazanie/temat, zwarty, zakończony antywzorcami.

## Indeks tematów → plik (grep-friendly)

> **Szukasz konkretu? Nie czytaj wszystkiego.** `grep -i <temat>` po tym indeksie (PL+EN keywordy) →
> nazwa pliku w tej samej linii → przeczytaj **tylko ten rozdział**. Tak oszczędzasz kontekst w
> docelowym projekcie (reguła: [01](01-documentation-and-ai-readme.md#ai_readme-pod-grep--oszczędność-kontekstu)).
> Slug pliku jest wspólny dla PL (root) i EN (`en/`).

- **`00-commandments.md`** — dekalog, decalogue, 10 przykazań, ten commandments, 7 grzechów, seven deadly sins, złota zasada, golden rule, altytuda, altitude, rdzeń doktryny, core.
- **`01-documentation-and-ai-readme.md`** — dokumentacja, documentation, AI_README, CLAUDE.md, docs, /docs, plany, plans, grep, keyword index, oszczędność kontekstu, context economy, czytnik, documentation.html, regeneracja, struktura folderów, folder structure.
- **`02-skills-and-refactoring.md`** — skill, slash-command, /run, /add-migration, automatyzacja, automation, hook, refaktoring, refactoring, prior-art, reuse, backward-compat, shim, SOLID, single responsibility, open/closed, dependency inversion, /simplify, /code-review.
- **`03-testing-and-verification.md`** — test, testowanie, testing, TDD, test-first, piramida, test pyramid, unit, integration, e2e, Playwright, pytest, Jest, smoke test, weryfikuj nie deklaruj, verify don't declare, regresja, regression, CI.
- **`04-scripts-and-databases.md`** — skrypt, script, mutacja, dry-run, --execute, idempotencja, idempotency, migracja, migration, forward-only, backup, restore, retencja, retention, seed, backfill, baza, database.
- **`05-git-and-deployments.md`** — git, git log -S, pickaxe, blame, deploy, wdrożenie, deployment, tag, rollback, swap bazy, database swap, konta, accounts, slug, maintenance window, nginx, pm2, sesje, sessions, FK order, integrity_check, sieroty, orphans, .gitignore, CRLF.
- **`06-collaboration-and-memory.md`** — współpraca, collaboration, plan iteruj review, plan iterate review, pamięć, memory, memory/, potwierdzaj nieodwracalne, confirm irreversible, raportuj uczciwie, report honestly, feedback.
- **`07-new-project-day-0.md`** — nowy projekt, new project, Dzień 0, Day 0, checklist, brief, brief produktowy, product brief, monetyzacja, monetization, onboarding, setup, poziom techniczny, technical level, runbook.
- **`08-stack-and-technologies.md`** — stack, technologie, technologies, Python, Node.js, FastAPI, SQLite, PostgreSQL, Docker, nginx, pm2, Hetzner, VPS, monolit, monolith, serverless, scale-to-zero, ADR, Lucide, baseline, Claude Code, GitHub, Git, GitHub Issues, TDD.
- **`09-law-and-protecting-the-creator.md`** — prawo, law, regulamin, terms of service, ToS, polityka prywatności, privacy policy, RODO, GDPR, zgody, consent, cookie, disclaimer, JDG, sole proprietorship, bramka wieku, age gate, 18+, retencja, prawa użytkownika, user rights, usunięcie konta, account deletion, ochrona twórcy.
- **`10-seo-and-translations.md`** — SEO, hreflang, JSON-LD, schema, canonical, sitemap, meta, OG, Open Graph, E-E-A-T, YMYL, programmatic SEO, tłumaczenia, translations, i18n, l10n, parytet językowy, language parity, RTL, lokalizacja.
- **`11-data-model-and-normalization.md`** — model danych, data model, normalizacja, normalization, denormalizacja, denormalization, słownik, lookup table, controlled vocabulary, slug, slug zamiast ID, slug not ID, active-row, expired_at, partial index, junction, M:N, klucz obcy, foreign key, ERD, schemat.
- **`12-flexibility-and-scalability.md`** — elastyczność, flexibility, skalowalność, scalability, rozdziel warstwy, separate layers, granice, boundaries, feature flag, feature flags, ship dark, ramp, scale-to-zero, always-on, cold start, cache, invalidation, over-engineering, ADR.
- **`13-performance-frontend-and-sql.md`** — wydajność, performance, mierz najpierw, measure first, Lighthouse, Core Web Vitals, CWV, LCP, CLS, INP, indeks, index, partial index, EXPLAIN QUERY PLAN, N+1, SELECT *, WAL, WebP, cache busting, lazy load, streaming, SSE, pagination, paginacja.
- **`14-operational-resilience.md`** — odporność, resilience, runtime, crash, unhandledRejection, uncaughtException, restart loop, retry, backoff, timeout, 429, rate limit, rotacja, rotation, User-Agent, resumable, wznawialne, checkpoint, scraper, długie joby, long jobs, SMTP, 587, STARTTLS, deliverability, SPF, DKIM, email, poczta, kwota, quota, koszt, cost, abuse, sesje, sessions, MemoryStore.
- **`15-scraping-ai-and-chatbots.md`** — scraping, scraper, crawler, robots.txt, selektor, selector, parsing, BeautifulSoup, requests, fuzzy match, rapidfuzz, dedup, delta, incremental, AI API, LLM, model, JSON schema, tool use, kontrakt wyjścia, output contract, cache, kwota, quota, chatbot, asystent, assistant, system prompt, grounding, RAG, prompt injection, halucynacja, hallucination, eval, golden set, disclaimer.

## Architektura `index.html` (kontrakt)

Jeden plik, bez zależności build. Mechanika:

- **`CHAPTERS`** (tablica w `<script>`) — **jedyne źródło** listy rozdziałów. Z niej generują się:
  karty na stronie głównej, `<select>` w czytniku, nawigacja prev/next. Pola: `file, no, group
  ("core"|"deep"), title, desc`.
- **Routing przez hash:** `#NN-nazwa` → widok rozdziału; pusty/`#` → strona główna. `route()`
  reaguje na `hashchange`.
- **Język treści:** `LANG` (`pl`/`en`, zapis w `localStorage` `rzemioslo-lang`). Ścieżka rozdziału =
  `file` (PL, root) albo `en/`+`file` (EN). Przełącznik `#langToggle` w topbarze. Chrome strony
  (dekalog, karty, brief) zostaje po polsku — pełna prezentacja wielojęzyczna to The Craft Web.
- **Render (dwutorowo):** najpierw `fetch(langPath(file))` (świeże `.md`, gdy serwowane); na błędzie
  fetcha (`file://`) — snapshot `window.RZEMIOSLO_DOCS[LANG][slug]` z `content.js`. Wynik →
  `marked.parse()` → `.prose`, cache w pamięci (`cache[LANG+":"+file]`).
- **`rewriteLinks()`** po renderze: linki `*.md` → `#slug` (nawigacja w SPA), `index.html` → `#`,
  zewnętrzne `http(s)` → `target=_blank`; tabele owijane w `.tablewrap` dla scrolla na mobile.
- **Motyw:** `[data-theme]` na `<html>` (`light`/`dark`); brak atrybutu = wg systemu. Przełącznik
  w topbarze zapisuje wybór w `localStorage` (`rzemioslo-theme`); skrypt w `<head>` ustawia go
  przed renderem (bez mignięcia).
- **Notatka-fallback** pokazuje się tylko, gdy zawiodą **oba** źródła (brak `content.js` i `file://`).

## Gotchas

- **`file://` blokuje `fetch`** — dlatego treść działa z dwukliku **tylko** ze snapshotu
  `content.js`. Po edycji `.md` uruchom `python build.py`, inaczej `file://` pokaże stare treści.
  Serwowane (`http(s)://`, GitHub Pages) zawsze bierze świeże `.md`; na GitHubie `.md` renderują się natywnie.
- **`content.js` jest generowany** — nie edytuj ręcznie (build nadpisze). Commituj go, by `file://`
  działało po sklonowaniu repo.
- **`marked` ładowany z CDN** — bez sieci render nie zadziała (jest miękki fallback do `<pre>`).
- **`index.html` NIE zawiera treści rozdziałów** — czyta `.md`/`content.js`. Nie wklejaj treści do HTML.
- **Dodajesz/zmieniasz rozdział → zsynchronizuj 3 miejsca + build:** `CHAPTERS` (index.html), tabela
  w `README.md`, tabela w tym pliku, potem `python build.py`. Rozjazd = martwy wpis (gorszy niż brak).
- **Parytet PL↔EN:** zmiana reguły w `00`–`15` (PL) wymaga aktualizacji odpowiednika w `en/` (ta sama
  lista, te same nazwy plików). EN to **tłumaczenie**, nie osobna doktryna. `content.js` trzyma oba języki.
- **Nazwy plików = stabilne kotwice** (`#NN-nazwa`, cele linków względnych), **wspólne dla PL i EN**.
  Nie lokalizujemy nazw plików — tylko treść w środku. Nie zmieniaj bez powodu.
- **Marka:** zmiany kolorów rób na zmiennych CSS (`--accent`, `--accent-2`, `--grad`), nie na
  wartościach w miejscu użycia. Tryb jasny i ciemny muszą oba wyglądać dobrze.
- **Treść generyczna, nie „pod jeden projekt".** Konkretne projekty służą
  tylko za ilustrację (`np. …`, „projekt referencyjny"), nigdy za temat rozdziału. Nie czyń żadnego projektu bohaterem doktryny.
- **Dwa języki: PL (kanon, root) + EN (`en/`).** Pisz reguły przekładalnie. Kierunek i konwencja →
  [docs/plans/0001-i18n-and-packaging.md](docs/plans/0001-i18n-and-packaging.md). Paczki per język montuje Web.

## Liczby

- 16 rozdziałów (`00`–`15`) + `README.md`, w **dwóch językach** (PL root + EN `en/`).
  Rdzeń: 9 plików (00–08). Pogłębienie: 7 (09–15).
- `index.html`: 1 plik; runtime z CDN (`marked` + Google Fonts). Build: `build.py` → `content.js`
  (PL: 18 dok. ~97 tys. znaków; EN: 17 dok. ~96 tys. znaków — rozdziały + `intro` + README; struktura `{lang:{slug:md}}`).
- **Dokumenty specjalne (poza numerowaną listą):** `intro.md` (manifest, route `#intro`) i widok
  briefu (`#brief`) — routowane osobno, nie ma ich w tablicy `CHAPTERS`.
- **Smoke test:** `python test.py` (parytet PL↔EN, martwe linki, świeżość `content.js`, spójność
  `CHAPTERS`/tabel/`codex.json`). Plus „test ręczny" = podgląd przez serwer **i** z dwukliku (`file://`)
  + klik po rozdziałach i przełącznik PL/EN (rzeczy runtime JS, których smoke nie łapie).
