# 02 — Skille i refaktoring

> Przykazania I i X: zautomatyzuj to, co powtarzalne; refaktoruj tak, by kod czytał się jak sąsiedni.

## Skille (slash-commands) — kiedy i po co

Skill to powtarzalna procedura zamknięta w jednym wywołaniu (`/run-projekt`, `/run-tests`,
`/update-ai-readme`, `/add-migration`). W WhiskyPolska skille okazały się dźwignią, bo
**kodyfikują „jak my to robimy"** — agent nie zgaduje, tylko wykonuje sprawdzony przepis.

### Zbuduj skill, gdy:
- procedurę powtarzasz **≥3 razy** (uruchom serwer + 22 smoke-checki, odpal testy, dodaj scraper);
- kolejność kroków jest **łatwa do pomylenia** (migracja: numer → SQL → `migrate.py` → AI_README → commit);
- istnieje **„gotcha" specyficzna dla projektu**, którą agent musi za każdym razem pamiętać
  (np. „na Windows ustaw `PYTHONIOENCODING=utf-8` przed scraperem", „Jest z `--runInBand`,
  gdy serwer chodzi").

### Dobry skill ma:
- **jedną komendę agenta** + jedną dla człowieka (fallback);
- **jasny kontrakt wyjścia** (exit 0 = zielone; exit 1 = co padło);
- **listę gotchas** specyficznych dla platformy/projektu;
- sekcję „kiedy NIE jest potrzebny".

### Anty-wzorce
- 🚫 Skill na coś, co robisz raz — to tylko narzut.
- 🚫 Skill, który ukrywa, co robi — gdy odpala destrukcję, ma to **wypisać** (np. „usunąłem dead code").
- 🚫 Mylenie skilla (przepis dla agenta) z hookiem (automatyzacja wykonywana przez harness).
  „Od teraz zawsze rób X po Y" = hook w configu, nie pamięć/skill.

## Refaktoring — dyscyplina

> **Złota zasada:** pisz kod, który czyta się jak kod obok niego. Dopasuj gęstość komentarzy,
> nazewnictwo i idiom do otoczenia. Spójność > Twoje preferencje.

### Zasady
1. **Szukaj prior-artu przed refaktorem** (przykazanie II). Zanim przepiszesz — `git log -S`,
   `git blame`. Często „brzydki" kształt ma powód (kompatybilność, edge-case, dawna decyzja).
2. **Refaktor osobno od zmiany zachowania.** Jeden commit = albo czyszczenie, albo nowa
   funkcja. Mieszanie utrudnia review i rollback.
3. **Reuse > rewrite.** Najpierw sprawdź, czy helper już istnieje (matcher, normalizer,
   `upsert_price`). Duplikacja logiki to dług.
4. **Backward-compat przy zmianach strukturalnych.** W WhiskyPolska przeniesienie skryptów do
   podpakietów zostawiło shim-y re-eksportujące ze starych ścieżek — stare wywołania dalej
   działają. Nie psuj cudzych wejść.
5. **Małe kroki, weryfikowane.** Refaktor → testy zielone → commit. Nie „wielki przepis na
   raz", po którym nie wiadomo, co pękło.

### Jakość bez polowania na bugi
Rozdziel dwa tryby przeglądu (jak `/simplify` vs `/code-review` w WhiskyPolska):
- **Uproszczenie/reuse/wydajność** — czyszczenie, bez szukania błędów.
- **Przegląd poprawności** — adversarialne szukanie bugów.
Nie mieszaj — każdy ma inny cel i inny próg pewności.

## W praktyce
- Skille na start: `/run` (serwer + smoke), `/run-tests` (unit + e2e), `/update-ai-readme`,
  `/add-migration` (jeśli relacyjna baza). → [08](08-stack-i-technologie.md)
- Refaktor ścieżki krytycznej (np. logowania) rób **osobnym, otestowanym** krokiem: najpierw
  test odtwarzający bieżący stan/bug, potem zmiana. → [03](03-testowanie-i-weryfikacja.md)
