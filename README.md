# Rzemiosło — The Build Codex

> Przykazania budowania i prowadzenia aplikacji **end-to-end** z Claude.
> Destylat doświadczeń z realnych projektów (m.in. WhiskyPolska), pisany pod **każdy kolejny projekt z Claude**.
>
> Warsztat **[jakub.solutions](https://jakub.solutions)** · Jakub Kolada — Insurance Systems Architect & IT Consultant.
> Marka, paleta (fiolet→cyan) i typografia (Playfair Display + Outfit) spójne z [Jakub.Solutions](../Jakub.Solutions).

To nie jest podręcznik frameworka. To **doktryna współpracy** — zestaw zasad, o których
Claude ma pamiętać **rozpoczynając i prowadząc projekt z Kubą**, żeby aplikacja przez całe
życie (od pierwszego commita po wdrożenie na prod z żywymi użytkownikami) była: zrozumiała
dla agenta, testowalna, bezpieczna w zmianie i godna zaufania.

## Jak czytać

- **[index.html](index.html)** — czytnik dla człowieka: spis przykazań + rozdziały renderowane
  z `.md` w przeglądarce, wygodne na telefonie i desktopie, z przełącznikiem jasny/ciemny.
  **Otwórz z dwukliku** (działa dzięki snapshotowi `content.js`) lub przez serwer
  (`python -m http.server 8080`) / hosting — serwowane zawsze pokazuje świeże `.md`.
- **Edytujesz treść?** Po zmianie `.md` uruchom `python build.py`, żeby odświeżyć snapshot dla `file://`.
- **Na GitHubie** pliki `.md` renderują się natywnie — wystarczy klikać linki w tabeli niżej.
- **Spieszysz się?** Przeczytaj [00 — Dekalog](00-przykazania.md). To cała doktryna w jednym ekranie.
- **Zaczynasz nowy projekt?** Idź do [07 — Nowy projekt: Dzień 0](07-nowy-projekt-checklist.md).

## Spis rozdziałów

| # | Rozdział | O czym |
|---|----------|--------|
| 00 | [Dekalog](00-przykazania.md) | 10 przykazań — rdzeń doktryny, do zapamiętania |
| 01 | [Dokumentacja i AI_README](01-dokumentacja-i-ai-readme.md) | `AI_README.md` w każdym katalogu, `CLAUDE.md` jako źródło prawdy, docs jako kod |
| 02 | [Skille i refaktoring](02-skille-i-refaktoring.md) | Kiedy zbudować skill, slash-command, dyscyplina refaktoringu |
| 03 | [Testowanie i weryfikacja](03-testowanie-i-weryfikacja.md) | Piramida testów, „weryfikuj, nie deklaruj", smoke testy |
| 04 | [Skrypty i bazy danych](04-skrypty-i-bazy-danych.md) | Idempotencja, dry-run/--execute, migracje forward-only, backupy |
| 05 | [Git i wdrożenia](05-git-i-wdrozenia.md) | Szukaj w git przed kodowaniem, taguj każdy deploy, swap bazy z zachowaniem kont |
| 06 | [Współpraca i pamięć](06-wspolpraca-i-pamiec.md) | Plan→iteruj→review, pamięć, potwierdzaj nieodwracalne, raportuj uczciwie |
| 07 | [Nowy projekt: Dzień 0](07-nowy-projekt-checklist.md) | Konkretna checklista startu nowego projektu |
| 08 | [Stack i technologie](08-stack-i-technologie.md) | Python, bazy, web/API, Docker, serwery (Hetzner), TDD — uniwersalny, prosty, skalowalny default |
| 09 | [Prawo i ochrona twórcy](09-prawo-i-ochrona-tworcy.md) | Regulamin, polityka prywatności, disclaimery jako zbroja osoby prywatnej / JDG |
| 10 | [SEO i tłumaczenia](10-seo-i-tlumaczenia.md) | hreflang, JSON-LD, programmatic SEO, E-E-A-T/YMYL, parytet językowy jako test |
| 11 | [Model danych i normalizacja](11-model-danych-normalizacja.md) | Słowniki lookup, slug zamiast ID, active-row, świadoma denormalizacja |
| 12 | [Elastyczność i skalowalność](12-elastycznosc-i-skalowalnosc.md) | Rozdziel warstwy, feature flags, scale-to-zero vs always-on, nie over-engineeruj |
| 13 | [Wydajność: frontend i SQL](13-wydajnosc-frontend-i-sql.md) | Mierz najpierw, indeksy + partial index, brak N+1, streaming czatu, CWV |

## Filozofia w jednym zdaniu

> **Buduj tak, jak rzemieślnik — wolno tam, gdzie błąd jest drogi; szybko tam, gdzie jest
> tani; i zostaw po sobie warsztat, w którym następny (człowiek albo agent) od razu wie,
> gdzie co leży.**

---

*Wersja żywa — aktualizuj po każdym projekcie, który czegoś nauczył. Doktryna, która się nie
zmienia, jest martwa.*
