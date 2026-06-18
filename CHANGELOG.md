# Changelog — Claude Build Codex

Wszystkie istotne zmiany doktryny **Claude Build Codex**. Wersjonowanie **semantyczne**
(MAJOR.MINOR.PATCH). **Data wpisu = dzień publikacji** — wtedy wersja została zdeployowana na
[codex.jakub.solutions](https://codex.jakub.solutions) i gotowa do pobrania.

Zasada: jedno źródło prawdy. `version` w [codex.json](codex.json) zawsze odpowiada najwyższemu
wpisowi poniżej. Każde wydanie tagujemy w gicie (`vMAJOR.MINOR.PATCH`) — Przykazanie VIII.

> **MAJOR** — przebudowa/usunięcie reguł lub rozdziału (zmiana niekompatybilna z dotychczasowym
> rozumieniem). **MINOR** — nowy rozdział lub istotna nowa reguła. **PATCH** — doprecyzowanie,
> przykład, literówka, drobna korekta.

## 1.0.0 — 2026-06-18

Pierwsze publiczne wydanie. Pełna doktryna gotowa do użycia jako `/docs/rules/` w nowym projekcie.

### Dodane
- **Dekalog** (rozdział 00) — 10 przykazań, 7 grzechów głównych, złota zasada altytudy.
- **Rdzeń (01–08):** dokumentacja i AI_README · skille i refaktoring · testowanie i weryfikacja
  (z TDD jako twardym rdzeniem) · skrypty i bazy danych · git i wdrożenia · współpraca i pamięć ·
  nowy projekt „Dzień 0" · **stack i technologie** (Python, bazy, web/API, Docker, Hetzner, TDD).
- **Pogłębienie (09–13):** prawo i ochrona twórcy · SEO i tłumaczenia · model danych i
  normalizacja · elastyczność i skalowalność · wydajność frontend i SQL.
- **Czytnik HTML** (`index.html`): render `.md` w przeglądarce, działa też z dwukliku
  (`file://`) dzięki snapshotowi `content.js`, tryb jasny/ciemny, ikony Lucide (SVG).
- **Build Codex Web** — przyjazna, wielojęzyczna witryna-opakowanie z pobieraniem tej paczki.

---

<!--
Szablon kolejnego wpisu:

## 1.1.0 — RRRR-MM-DD
### Dodane
- …
### Zmienione
- …
### Usunięte
- …
-->
