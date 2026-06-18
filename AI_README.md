# AI_README — katalog Claude Build Codex

> Mapa katalogu dla następnej sesji / innego agenta. Czytaj **przed** dotknięciem plików tutaj.
> Konstytucja repo: [CLAUDE.md](CLAUDE.md). Test jakości tego pliku: czy po przeczytaniu możesz
> bezpiecznie zmienić cokolwiek w tym katalogu, nie skanując wszystkich plików?

## Co to za katalog

Repozytorium **dokumentacji** (nie aplikacja): doktryna „Claude Build Codex".
Treść to ręcznie pisany markdown; `index.html` jest jej przeglądarką (statyczna SPA, bez build-stepu).
Cel: zestaw reguł reużywalny jako `/docs/rules/` w nowych projektach **oraz** materiał publiczny
dla osób zaczynających z Claude. Szczegóły i polityki → [CLAUDE.md](CLAUDE.md).

## Indeks plików

| Plik | Po co to |
|------|----------|
| `index.html` | Czytnik SPA: strona główna (dekalog + karty) + widok rozdziału renderujący `.md`, przełącznik jasny/ciemny. |
| `content.js` | **Generowany** snapshot `.md` osadzony w JS — pozwala renderować treść po `file://`. Nie edytuj ręcznie. |
| `build.py` | Skrypt buildu: łączy pliki `.md` → `content.js`. Uruchom po edycji treści (`python build.py`). |
| `CLAUDE.md` | Konstytucja repo: czym jest, stack, jak uruchomić, polityki, stan bieżący. |
| `AI_README.md` | Ten plik — mapa katalogu. |
| `README.md` | Wejście dla człowieka: spis rozdziałów + „jak czytać". |
| `codex.json` | **Wersja wydania** (`version` + `released`). Źródło stempla dla witryny Claude Build Codex Web. |
| `CHANGELOG.md` | Historia wydań Claude Build Codex (semver, data = dzień publikacji). |
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

Rozdziały dzielą się na **rdzeń** (`00`–`08`) i **pogłębienie** (`09`–`13`). Każdy = jedno
przykazanie/temat, zwarty, zakończony antywzorcami.

## Architektura `index.html` (kontrakt)

Jeden plik, bez zależności build. Mechanika:

- **`CHAPTERS`** (tablica w `<script>`) — **jedyne źródło** listy rozdziałów. Z niej generują się:
  karty na stronie głównej, `<select>` w czytniku, nawigacja prev/next. Pola: `file, no, group
  ("core"|"deep"), title, desc`.
- **Routing przez hash:** `#NN-nazwa` → widok rozdziału; pusty/`#` → strona główna. `route()`
  reaguje na `hashchange`.
- **Render (dwutorowo):** najpierw `fetch(file)` (świeże `.md`, gdy serwowane); na błędzie fetcha
  (`file://`) — snapshot `window.RZEMIOSLO_DOCS[slug]` z `content.js`. Wynik → `marked.parse()` →
  `.prose`, cache w pamięci (`cache[file]`).
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
- **Nazwy plików = stabilne kotwice** (`#NN-nazwa`, cele linków względnych). Nie zmieniaj bez powodu.
- **Marka:** zmiany kolorów rób na zmiennych CSS (`--accent`, `--accent-2`, `--grad`), nie na
  wartościach w miejscu użycia. Tryb jasny i ciemny muszą oba wyglądać dobrze.
- **Treść generyczna, nie „pod jeden projekt".** Konkretne projekty służą
  tylko za ilustrację (`np. …`, „projekt referencyjny"), nigdy za temat rozdziału. Nie czyń żadnego projektu bohaterem doktryny.
- **Wersja angielska** planowana w przyszłości — pisz reguły przekładalnie. Na razie język = polski.

## Liczby

- 14 rozdziałów (`00`–`13`) + `README.md`. Rdzeń: 9 plików (00–08). Pogłębienie: 5 (09–13).
- `index.html`: 1 plik; runtime z CDN (`marked` + Google Fonts). Build: `build.py` → `content.js`
  (15 dokumentów, ~67 tys. znaków).
- Brak testów (repo dokumentacji). „Test" = podgląd przez serwer **i** z dwukliku (`file://`) + klik po rozdziałach.
