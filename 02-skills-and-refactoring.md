# 02 — Skille i refaktoring

> Przykazania I i X: zautomatyzuj to, co powtarzalne; refaktoruj tak, by kod czytał się jak sąsiedni.

## Skille (slash-commands) — kiedy i po co

Skill to powtarzalna procedura zamknięta w jednym wywołaniu (`/run-projekt`, `/run-tests`,
`/update-ai-readme`, `/add-migration`). W projekcie referencyjnym skille okazały się dźwignią, bo
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
4. **Backward-compat przy zmianach strukturalnych.** W projekcie referencyjnym przeniesienie skryptów do
   podpakietów zostawiło shim-y re-eksportujące ze starych ścieżek — stare wywołania dalej
   działają. Nie psuj cudzych wejść.
5. **Małe kroki, weryfikowane.** Refaktor → testy zielone → commit. Nie „wielki przepis na
   raz", po którym nie wiadomo, co pękło.

### Jakość bez polowania na bugi
Rozdziel dwa tryby przeglądu (jak `/simplify` vs `/code-review`):
- **Uproszczenie/reuse/wydajność** — czyszczenie, bez szukania błędów.
- **Przegląd poprawności** — adversarialne szukanie bugów.
Nie mieszaj — każdy ma inny cel i inny próg pewności.

## SOLID — projektowanie, które się nie zatyka

> Nie dogmat, lecz **pięć testów na to, czy zmiana będzie tania**. Stosuj proporcjonalnie do
> ryzyka (→ [12](12-flexibility-and-scalability.md): nie over-engineeruj). SOLID to nie pretekst
> do warstw abstrakcji „na wszelki wypadek".

- **S — Single responsibility.** Jeden moduł = jeden powód do zmiany. To ta sama dyscyplina, co
  „jeden commit = jedna rzecz" (refaktor albo zachowanie, nie oba). Funkcja, którą trzeba ruszać
  z trzech niezwiązanych powodów, to trzy funkcje.
- **O — Open/closed.** Rozszerzaj bez rozcinania sprawdzonego kodu. Tu wpinają się **feature flags**
  (→ [12](12-flexibility-and-scalability.md)): nową ścieżkę dokładasz za flagą i shipujesz dark,
  zamiast przepisywać istniejącą gałąź i ryzykować regresję.
- **L — Liskov.** Podtyp ma dotrzymać kontraktu nadtypu — bez „wyjątku, który wszystko psuje".
  Jeśli implementacja łamie założenia wołającego, to nie jest podtyp, tylko pułapka.
- **I — Interface segregation.** Wąskie, celowe interfejsy zamiast jednego boga-interfejsu.
  Wołający nie powinien zależeć od metod, których nie używa.
- **D — Dependency inversion.** Zależ od abstrakcji, nie od konkretu. To kodowy odpowiednik
  „rozdziel warstwy" (→ [12](12-flexibility-and-scalability.md)): logika nie zna dostawcy bazy
  czy kolejki z palca — dostaje go przez granicę, więc da się go podmienić (i przetestować, → [03](03-testing-and-verification.md)).

### Anty-wzorce
- 🚫 **SOLID jako kult** — pięć warstw i fabryka fabryk dla CRUD-a na trzy pola. Zasada D ma
  ułatwiać podmianę, nie mnożyć pliki. Mierz potrzebę, nie cytuj liter.
- 🚫 **Open/closed bez flag** — „rozszerzasz", edytując w miejscu gorącą ścieżkę bez przełącznika
  i bez rampu (→ [12](12-flexibility-and-scalability.md): brak feature flags).
- 🚫 **Abstrakcja zanim są dwa przypadki** — interfejs wyssany z jednego użycia zgaduje przyszłość.
  Najpierw drugi konkret, potem wspólny kontrakt (reuse > rewrite, ale nie reuse > realność).

## W praktyce
- Skille na start: `/run` (serwer + smoke), `/run-tests` (unit + e2e), `/update-ai-readme`,
  `/add-migration` (jeśli relacyjna baza). → [08](08-stack-and-technologies.md)
- Refaktor ścieżki krytycznej (np. logowania) rób **osobnym, otestowanym** krokiem: najpierw
  test odtwarzający bieżący stan/bug, potem zmiana. → [03](03-testing-and-verification.md)
