# AI_README — katalog Rzemiosło (The Craft)

> Mapa katalogu dla następnej sesji / innego agenta. Czytaj **przed** dotknięciem plików tutaj.
> Konstytucja repo: [CLAUDE.md](CLAUDE.md). Test jakości tego pliku: czy po przeczytaniu możesz
> bezpiecznie zmienić cokolwiek w tym katalogu, nie skanując wszystkich plików?
>
> **Podział plików meta** (→ [01](01-documentation-and-ai-readme.md)): `README.md` = opis dla GitHuba
> (publiczny, EN). `CLAUDE.md` = konstytucja repo (jeden język, **nie tłumaczona**). **`AI_README` jest
> tłumaczony per język** — ten plik to wersja **PL**; EN/baza w [`../AI_README.md`](../AI_README.md).

## Co to za katalog

Repozytorium **dokumentacji** (nie aplikacja): doktryna „Rzemiosło — The Craft" (Kolada Build).
Treść to ręcznie pisany markdown; `index.html` jest jej przeglądarką (statyczna SPA, bez build-stepu).
Cel: zestaw reguł reużywalny jako `/docs/rules/` w nowych projektach **oraz** materiał publiczny
dla osób zaczynających z Claude. Szczegóły i polityki → [CLAUDE.md](CLAUDE.md).

## Rdzeń (to repo) vs Web (siostrzane repo)

**Podział ról — nie duplikuj między nimi:**

- **To repo (`ClaudeBuildCodex`, marka „Rzemiosło") = rdzeń kanoniczny.** Forma: **techniczna, zwarta, imperatywna;
  bazą jest angielski** (PL tłumaczenie w `pl/`) — źródło prawdy reguł, dołączane do projektów jako `/docs/rules/`. Optymalizowane pod
  **agenta i osobę techniczną**: gęstość ponad przystępność. Tu wersjonujemy doktrynę (craft.json).
- **Siostrzane `ClaudeBuildCodexWeb` (marka „Rzemiosło Web") = projekt prezentacyjny.** Bierze tę samą doktrynę i **rozwija
  poszczególne tematy** w przyjaźniejszej, obszerniejszej formie. **To Web — nie to repo — odpowiada za:**
  publiczną stronę, **edycje** (techniczna / BIZ-TECH / biznesowa), **wersje językowe** i **budowanie paczek
  `docs/rules/` w konkretnym języku**. Konsumuje treść tego repo + `craft.json` przy buildzie.

> **To repo jest TYLKO zestawem reguł.** Nie jest produktem prezentacyjnym. `index.html` tutaj to
> **minimalny czytnik lokalny/dev** (podgląd treści dla autora i agenta), **nie** publiczna witryna —
> dlatego nie umieszczamy tu badge'y edycji, marketingu ani przełącznika języka. Cała prezentacja,
> edycje i pakowanie wielojęzyczne dzieją się w **The Craft Web** (osobny projekt). Jeśli kusi Cię,
> by tu dodać warstwę prezentacji/marketingu/edycji — to materiał dla Web, nie dla rdzenia.

Kierunek wersji EN i pakowania per język → [docs/plans/0001-i18n-and-packaging.md](docs/plans/0001-i18n-and-packaging.md).

## Indeks plików

| Plik | Po co to |
|------|----------|
| `index.html` | **Minimalny czytnik lokalny/dev** (podgląd treści dla autora/agenta) — NIE publiczna witryna. Strona główna (dekalog + karty) + widok rozdziału + brief + przełącznik języka EN/PL (domyślnie EN). |
| `intro.md` | **Manifest** — „Czym jest The Craft" + artykuł „dlaczego warto". Dokument specjalny (poza numerowaną listą), routowany jako `#intro`; jest też `pl/intro.md`. |
| `00`–`16` (root) | **Treść EN — kanoniczna, baza, źródło prawdy.** Slugi/numery = stabilne kotwice, wspólne dla wszystkich języków. |
| `pl/` | **Treść PL** — równoległy zestaw `00-*.md`…`16-*.md` (te same nazwy plików, treść po polsku). Tłumaczenie EN. |
| `docs/` | Plany i decyzje meta repo (nie treść doktryny): `docs/AI_README.md`, `docs/plans/`. |
| `content.js` | **Generowany** snapshot `.md` osadzony w JS — pozwala renderować treść po `file://`. Nie edytuj ręcznie. |
| `build.py` | Skrypt buildu: łączy pliki `.md` → `content.js`. Uruchom po edycji treści (`python build.py`). |
| `test.py` | **Smoke test** (czysty Python): parytet PL↔EN, martwe linki, świeżość `content.js`, spójność `CHAPTERS`/tabel/`craft.json`, oraz **statyczna nawigacja `index.html`** (linki `href="#…"`, `data-i18n`↔`UI`, `data-bf-label`↔`BRIEF_FIELDS`). `python test.py`. |
| `CLAUDE.md` | Konstytucja repo: czym jest, stack, jak uruchomić, polityki, stan bieżący. |
| `AI_README.md` | Ten plik — mapa katalogu. |
| `README.md` | Wejście dla człowieka: spis rozdziałów + „jak czytać". |
| `craft.json` | **Wersja wydania** (`version` + `released`) + nazwy marki (`name`/`name_short`/`name_en`). Źródło stempla dla witryny Rzemiosło Web. |
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
| `16-driving-claude.md` | Prowadzenie Claude Code: skille/slash-komendy, dobór modelu, autopilot (preferowany), praca w tle, agentowe workflow/subagenci. |

Rozdziały dzielą się na **rdzeń** (`00`–`08`) i **pogłębienie** (`09`–`16`). Każdy = jedno
przykazanie/temat, zwarty, zakończony antywzorcami.

## Indeks tematów → plik (grep-friendly)

> **Szukasz konkretu? Nie czytaj wszystkiego.** `grep -i <temat>` po tym indeksie (polskie keywordy) →
> nazwa pliku w tej samej linii → przeczytaj **tylko ten rozdział**. Tak oszczędzasz kontekst w
> docelowym projekcie (reguła: [01](01-documentation-and-ai-readme.md)).
> **To wersja PL** (tłumaczenie). Baza (EN) i jej keywordy są w rootcie ([`../AI_README.md`](../AI_README.md));
> slug pliku jest wspólny dla wszystkich języków. Inne języki: w analogicznych podfolderach.

- **`00-commandments.md`** — przykazania, dekalog, 10 przykazań, siedem grzechów głównych, złota zasada, altytuda, rdzeń doktryny.
- **`01-documentation-and-ai-readme.md`** — dokumentacja, AI_README, CLAUDE.md, docs, /docs, plany, grep, indeks słów kluczowych, oszczędność kontekstu, czytnik, documentation.html, regeneracja, struktura folderów.
- **`02-skills-and-refactoring.md`** — skill, slash-komenda, /run, /add-migration, automatyzacja, hook, refaktoring, prior-art, reuse, backward-compat, shim, SOLID, single responsibility, open/closed, dependency inversion, /simplify, /code-review.
- **`03-testing-and-verification.md`** — test, testowanie, TDD, test-first, piramida testów, unit, integration, e2e, Playwright, pytest, Jest, smoke test, weryfikuj nie deklaruj, regresja, CI.
- **`04-scripts-and-databases.md`** — skrypt, mutacja, dry-run, --execute, idempotencja, migracja, forward-only, backup, restore, retencja, seed, backfill, baza danych.
- **`05-git-and-deployments.md`** — git, git log -S, pickaxe, blame, deploy, wdrożenie, tag, rollback, swap bazy, konta, slug, okno maintenance, nginx, pm2, sesje, kolejność FK, integrity_check, sieroty, .gitignore, CRLF, issue, issues, GitHub Issues, jednostka pracy, gałąź, gałęzie, branching, trunk-based, krótka gałąź, PR, pull request, review, recenzja, praca zespołowa.
- **`06-collaboration-and-memory.md`** — współpraca, plan iteruj review, pamięć, potwierdzaj nieodwracalne, raportuj uczciwie, feedback, podsumowanie zmian, widget, następne działania, język natywny.
- **`07-new-project-day-0.md`** — nowy projekt, Dzień 0, checklista, brief, brief produktowy, monetyzacja, onboarding, setup, wpięcie The Craft, docs/rules, submodule, poziom techniczny, języki programisty, znane technologie, runbook.
- **`08-stack-and-technologies.md`** — stack, technologie, Python, Node.js, FastAPI, SQLite, PostgreSQL, Docker, nginx, pm2, Hetzner, VPS, monolit, serverless, scale-to-zero, ADR, Lucide, baseline, Claude Code, GitHub, Git, GitHub Issues, TDD.
- **`09-law-and-protecting-the-creator.md`** — prawo, regulamin, polityka prywatności, RODO, zgody, cookie, disclaimer, JDG, bramka wieku, 18+, retencja danych, prawa użytkownika, usunięcie konta, ochrona twórcy.
- **`10-seo-and-translations.md`** — SEO, hreflang, JSON-LD, schema, canonical, sitemap, meta, OG, Open Graph, E-E-A-T, YMYL, programmatic SEO, tłumaczenia, i18n, l10n, parytet językowy, RTL, lokalizacja.
- **`11-data-model-and-normalization.md`** — model danych, normalizacja, denormalizacja, słownik lookup, controlled vocabulary, slug, slug zamiast ID, active-row, expired_at, partial index, junction, M:N, klucz obcy, ERD, schemat.
- **`12-flexibility-and-scalability.md`** — elastyczność, skalowalność, rozdziel warstwy, granice, feature flag, ship dark, ramp, scale-to-zero, always-on, cold start, cache, inwalidacja, over-engineering, ADR.
- **`13-performance-frontend-and-sql.md`** — wydajność, mierz najpierw, Lighthouse, Core Web Vitals, CWV, LCP, CLS, INP, indeks, partial index, EXPLAIN QUERY PLAN, N+1, SELECT *, WAL, WebP, cache busting, lazy load, streaming, SSE, paginacja.
- **`14-operational-resilience.md`** — odporność, runtime, crash, unhandledRejection, uncaughtException, pętla restartów, retry, backoff, timeout, 429, rate limit, rotacja, User-Agent, wznawialne, checkpoint, scraper, długie joby, SMTP, 587, STARTTLS, deliverability, SPF, DKIM, poczta, kwota, koszt, abuse, sesje, MemoryStore.
- **`15-scraping-ai-and-chatbots.md`** — scraping, scraper, crawler, robots.txt, selektor, parsing, BeautifulSoup, requests, fuzzy match, rapidfuzz, dedup, delta, incremental, AI API, LLM, model, JSON schema, tool use, kontrakt wyjścia, cache, kwota, chatbot, asystent, system prompt, grounding, RAG, prompt injection, halucynacja, eval, golden set, disclaimer.
- **`16-driving-claude.md`** — Claude Code, skill, skille, slash-komenda, slash, /run, /run-tests, hook, model, przełączanie modeli, autopilot, auto-accept, autonomiczny, tło, background, run_in_background, długie zadania, agentowe, subagent, workflow, fan-out, równolegle, orkiestracja, bariery.

## Architektura `index.html` (kontrakt)

Jeden plik, bez zależności build. Mechanika:

- **`CHAPTERS`** (tablica w `<script>`) — **jedyne źródło** listy rozdziałów. Z niej generują się:
  karty na stronie głównej, `<select>` w czytniku, nawigacja prev/next. Pola: `file, no, group
  ("core"|"deep"), title, desc`.
- **Routing przez hash:** `#NN-nazwa` → widok rozdziału; pusty/`#` → strona główna. `route()`
  reaguje na `hashchange`.
- **Język (treść + cały chrome):** `LANG` (`en`/`pl`, domyślnie **`en`**, zapis w `localStorage` `rzemioslo-lang`).
  Treść rozdziału z `file` (EN, root) albo `pl/`+`file` (PL). **Chrome jest w pełni dwujęzyczny** —
  słownik `UI` (`data-i18n`/`data-i18n-html`) + `CH_EN` (tytuły/opisy rozdziałów) + `BRIEF_FIELDS`
  (pola briefu); `applyChrome()` przerysowuje wszystko przy starcie i przy `#langToggle`. Dodajesz
  string do chrome → dodaj klucz do `UI` (oba języki), inaczej zostanie po polsku.
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
- **Parytet EN↔PL:** zmiana reguły w `00`–`16` (EN, kanon) wymaga aktualizacji odpowiednika w `pl/` (ta sama
  lista, te same nazwy plików). PL to **tłumaczenie**, nie osobna doktryna. `content.js` trzyma oba języki.
- **Nazwy plików = stabilne kotwice** (`#NN-nazwa`, cele linków względnych), **wspólne dla EN i PL**.
  Nie lokalizujemy nazw plików — tylko treść w środku. Nie zmieniaj bez powodu.
- **Marka:** zmiany kolorów rób na zmiennych CSS (`--accent`, `--accent-2`, `--grad`), nie na
  wartościach w miejscu użycia. Tryb jasny i ciemny muszą oba wyglądać dobrze.
- **Treść generyczna, nie „pod jeden projekt".** Konkretne projekty służą
  tylko za ilustrację (`np. …`, „projekt referencyjny"), nigdy za temat rozdziału. Nie czyń żadnego projektu bohaterem doktryny.
- **Dwa języki: EN (kanon, root, baza) + PL (`pl/`).** Pisz reguły przekładalnie. Kierunek i konwencja →
  [docs/plans/0001-i18n-and-packaging.md](docs/plans/0001-i18n-and-packaging.md). Paczki per język montuje Web.

## Liczby

- 17 rozdziałów (`00`–`16`) + `README.md`, w **dwóch językach** (EN root = baza + PL `pl/`).
  Rdzeń: 9 plików (00–08). Pogłębienie: 8 (09–16).
- `index.html`: 1 plik; runtime z CDN (`marked` + Google Fonts). Build: `build.py` → `content.js`
  (EN: 19 dok. ~110 tys. znaków; PL: 18 dok. ~102 tys. znaków — rozdziały + `intro` + README; struktura `{lang:{slug:md}}`).
- **Dokumenty specjalne (poza numerowaną listą):** `intro.md` (manifest, route `#intro`) i widok
  briefu (`#brief`) — routowane osobno, nie ma ich w tablicy `CHAPTERS`.
- **Smoke test:** `python test.py` (parytet PL↔EN, martwe linki, świeżość `content.js`, spójność
  `CHAPTERS`/tabel/`craft.json`, statyczna nawigacja `index.html`: linki `href="#…"` + `data-i18n`↔`UI`
  + `data-bf-label`↔`BRIEF_FIELDS`). Plus „test ręczny" = podgląd przez serwer **i** z dwukliku (`file://`)
  + klik po rozdziałach i przełącznik EN/PL (zachowanie runtime JS, którego smoke nie łapie).
