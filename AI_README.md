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

Kierunek wersji EN i pakowania per język → [docs/plans/0001-i18n-i-pakowanie.md](docs/plans/0001-i18n-i-pakowanie.md).

## Indeks plików

| Plik | Po co to |
|------|----------|
| `index.html` | **Minimalny czytnik lokalny/dev** (podgląd treści dla autora/agenta) — NIE publiczna witryna. Strona główna (dekalog + karty) + widok rozdziału + brief + przełącznik języka treści (PL/EN). |
| `intro.md` | **Manifest** — „Czym jest The Craft" + artykuł „dlaczego warto". Dokument specjalny (poza numerowaną listą), routowany jako `#intro`; jest też `en/intro.md`. |
| `00`–`14` (root) | **Treść PL** (kanoniczna, źródło prawdy). Slugi/numery = stabilne kotwice, wspólne dla wszystkich języków. |
| `en/` | **Treść EN** — równoległy zestaw `00-*.md`…`14-*.md` (te same nazwy plików, treść po angielsku). Tłumaczenie PL. |
| `docs/` | Plany i decyzje meta repo (nie treść doktryny): `docs/AI_README.md`, `docs/plans/`. |
| `content.js` | **Generowany** snapshot `.md` osadzony w JS — pozwala renderować treść po `file://`. Nie edytuj ręcznie. |
| `build.py` | Skrypt buildu: łączy pliki `.md` → `content.js`. Uruchom po edycji treści (`python build.py`). |
| `CLAUDE.md` | Konstytucja repo: czym jest, stack, jak uruchomić, polityki, stan bieżący. |
| `AI_README.md` | Ten plik — mapa katalogu. |
| `README.md` | Wejście dla człowieka: spis rozdziałów + „jak czytać". |
| `codex.json` | **Wersja wydania** (`version` + `released`) + nazwy marki (`name`/`name_short`/`name_en`). Źródło stempla dla witryny Rzemiosło Web. |
| `CHANGELOG.md` | Historia wydań Rzemiosła (semver, data = dzień publikacji). |
| `00-przykazania.md` | **Dekalog** — 10 przykazań, 7 grzechów, złota zasada altytudy. Rdzeń. |
| `01-dokumentacja-i-ai-readme.md` | Trzy warstwy docs: CLAUDE.md / AI_README / docs. Kiedy aktualizować. |
| `02-skille-i-refaktoring.md` | Kiedy zbudować skill/slash-command; dyscyplina refaktoringu; SOLID (z feature flags i rozdziel-warstwy). |
| `03-testowanie-i-weryfikacja.md` | Piramida testów, „weryfikuj, nie deklaruj", smoke. |
| `04-skrypty-i-bazy-danych.md` | Dry-run/`--execute`, idempotencja, migracje forward-only, backupy. |
| `05-git-i-wdrozenia.md` | Szukaj w git, taguj deploy, swap bazy z zachowaniem kont. Najgęstszy rozdział. |
| `06-wspolpraca-i-pamiec.md` | Plan→iteruj→review, pamięć, potwierdzaj nieodwracalne, raportuj uczciwie. |
| `07-nowy-projekt-checklist.md` | Checklista „Dzień 0": brief produktowy (język, funkcje, monetyzacja, UX, animacje, marketing) + setup repo. |
| `08-stack-i-technologie.md` | Uniwersalny stack: Python, bazy, web/API, Docker, serwery (Hetzner) + TDD jako twardy rdzeń. |
| `09-prawo-i-ochrona-tworcy.md` | Regulamin, polityka prywatności, disclaimery jako ochrona twórcy / JDG. |
| `10-seo-i-tlumaczenia.md` | hreflang, JSON-LD, E-E-A-T/YMYL, parytet językowy jako test. |
| `11-model-danych-normalizacja.md` | Słowniki lookup, slug zamiast ID, active-row, świadoma denormalizacja. |
| `12-elastycznosc-i-skalowalnosc.md` | Rozdziel warstwy, feature flags, scale-to-zero vs always-on, nie over-engineeruj. |
| `13-wydajnosc-frontend-i-sql.md` | Mierz najpierw, indeksy + partial index, brak N+1, streaming czatu, CWV. |
| `14-odpornosc-operacyjna.md` | Crash-proof runtime, wznawialne joby, zawodne API (backoff/rotacja), limity providera + poczta, kwoty kosztów. |

Rozdziały dzielą się na **rdzeń** (`00`–`08`) i **pogłębienie** (`09`–`14`). Każdy = jedno
przykazanie/temat, zwarty, zakończony antywzorcami.

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
- **Parytet PL↔EN:** zmiana reguły w `00`–`14` (PL) wymaga aktualizacji odpowiednika w `en/` (ta sama
  lista, te same nazwy plików). EN to **tłumaczenie**, nie osobna doktryna. `content.js` trzyma oba języki.
- **Nazwy plików = stabilne kotwice** (`#NN-nazwa`, cele linków względnych), **wspólne dla PL i EN**.
  Nie lokalizujemy nazw plików — tylko treść w środku. Nie zmieniaj bez powodu.
- **Marka:** zmiany kolorów rób na zmiennych CSS (`--accent`, `--accent-2`, `--grad`), nie na
  wartościach w miejscu użycia. Tryb jasny i ciemny muszą oba wyglądać dobrze.
- **Treść generyczna, nie „pod jeden projekt".** Konkretne projekty służą
  tylko za ilustrację (`np. …`, „projekt referencyjny"), nigdy za temat rozdziału. Nie czyń żadnego projektu bohaterem doktryny.
- **Dwa języki: PL (kanon, root) + EN (`en/`).** Pisz reguły przekładalnie. Kierunek i konwencja →
  [docs/plans/0001-i18n-i-pakowanie.md](docs/plans/0001-i18n-i-pakowanie.md). Paczki per język montuje Web.

## Liczby

- 15 rozdziałów (`00`–`14`) + `README.md`, w **dwóch językach** (PL root + EN `en/`).
  Rdzeń: 9 plików (00–08). Pogłębienie: 6 (09–14).
- `index.html`: 1 plik; runtime z CDN (`marked` + Google Fonts). Build: `build.py` → `content.js`
  (PL: 17 dok. ~91 tys. znaków; EN: 16 dok. ~90 tys. znaków — rozdziały + `intro` + README; struktura `{lang:{slug:md}}`).
- **Dokumenty specjalne (poza numerowaną listą):** `intro.md` (manifest, route `#intro`) i widok
  briefu (`#brief`) — routowane osobno, nie ma ich w tablicy `CHAPTERS`.
- Brak testów (repo dokumentacji). „Test" = podgląd przez serwer **i** z dwukliku (`file://`) + klik po rozdziałach.
