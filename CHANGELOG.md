# Changelog — Rzemiosło (The Craft)

Wszystkie istotne zmiany doktryny **Rzemiosło — The Craft (Kolada Build)**. Wersjonowanie **semantyczne**
(MAJOR.MINOR.PATCH). **Data wpisu = dzień publikacji** — wtedy wersja została zdeployowana na
[codex.jakub.solutions](https://codex.jakub.solutions) i gotowa do pobrania.

Zasada: jedno źródło prawdy. `version` w [codex.json](codex.json) zawsze odpowiada najwyższemu
wpisowi poniżej. Każde wydanie tagujemy w gicie (`vMAJOR.MINOR.PATCH`) — Przykazanie VIII.

> **MAJOR** — przebudowa/usunięcie reguł lub rozdziału (zmiana niekompatybilna z dotychczasowym
> rozumieniem). **MINOR** — nowy rozdział lub istotna nowa reguła. **PATCH** — doprecyzowanie,
> przykład, literówka, drobna korekta.

## 1.0.0 — 2026-06-19

Pierwsze publiczne wydanie — **kompletna doktryna The Craft**, gotowa do wpięcia jako `docs/rules/`
w nowym projekcie. Od pierwszego commita po prod: jak budować z Claude tak, żeby projekt został
zrozumiały, bezpieczny w zmianie i godny zaufania.

### Dodane
- **17 rozdziałów w dwóch językach** (EN kanon + PL — te same rozdziały, te same kotwice):
  **Dekalog** (00) + rdzeń (01–08) + pogłębienie (09–16) — od dokumentacji, testów, gita i wdrożeń,
  przez prawo, SEO i model danych, po wydajność, odporność operacyjną, scraping/AI i prowadzenie Claude.
- **Czytnik HTML** paczki — render `.md` z dwukliku (`file://`), tryb jasny/ciemny, przełącznik EN/PL.
- **Witryna** [codex.jakub.solutions](https://codex.jakub.solutions) — przyjazne opakowanie z pobieraniem.

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
