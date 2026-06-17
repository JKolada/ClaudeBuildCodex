# 08 — Zastosowanie: EchoInsight.Me

Doktryna przełożona na konkretny projekt. **EchoInsight.Me** — ogólnoświatowy,
wielkoduszny chatbot do rozwoju osobistego i pomocy duchowej. Cel etapu: doprowadzić stronę
do stanu **darmowym w ograniczonym zakresie**, z pełnymi zapewnieniami o prywatności,
ciepłym minimalistycznym UX i solidnym fundamentem technicznym.

> Ten rozdział to żywy backlog — aktualizuj go w `Z:\_Projects\EchoInsight`, a tu zostaw wersję-doktrynę.

## Misja i twarde ograniczenia (→ `CLAUDE.md` jako reguły)
- **Darmowe w ograniczonym zakresie.** Zero linków do płatności. Jasny komunikat: „usługa jest
  darmowa w ograniczonym zakresie; naszym celem jest pomóc".
- **Dla pełnoletnich.** **Nie świadczymy usług terapeutycznych** — widoczny, łagodny disclaimer
  + ścieżka do realnej pomocy w kryzysie (linki do infolinii) bez udawania terapeuty.
- **Nie czytamy rozmów, by ulepszać system.** To zapewnienie musi być **prawdziwe w
  architekturze**, nie tylko w copy. → patrz „Prywatność" niżej.
- **Prywatność i anonimizacja** przechowywanych rozmów = reguła nadrzędna w konstytucji, nie notatka.

## Backlog priorytetowy

### P0 — fundament (blokuje „użyteczne za darmo")
- [ ] **Fix logowania** (ścieżka krytyczna). TDD: test odtwarzający bug → fix → pełny smoke
      (rejestracja / login / logout / trwałość sesji). → [03](03-testowanie-i-weryfikacja.md), [05](05-git-i-wdrozenia.md)
- [ ] **Gating darmowego zakresu** — limit (np. wiadomości/sesja albo /dzień), czytelny,
      bez żadnych linków płatności. Komunikat o limicie ciepły, nie zniechęcający.
- [ ] **Strona-zapewnienie o prywatności** + zgody (anonimizacja, retencja, „nie czytamy rozmów").
- [ ] **Disclaimery**: pełnoletność, brak terapii, ścieżka kryzysowa.

### P1 — jakość i zaufanie
- [ ] **Wydajność** — zmierz (TTFB, czas odpowiedzi, streaming), popraw, **udowodnij liczbami przed/po**.
- [ ] **i18n** — sprawdź, że WSZYSTKIE używane języki są kompletnie przetłumaczone (UI +
      disclaimery + komunikaty błędów + system messages). Brakujące klucze = test, który pada.
- [ ] **Pipeline anonimizowanej destylacji** (Gemini) — patrz osobna sekcja niżej.
- [ ] **Testy**: unit (logika gating/anonimizacji/i18n) + Playwright (rozmowa, limit, zmiana
      języka, zgody, login).

### P2 — dopieszczenie
- [ ] UX polish (mikro-animacje, ton odpowiedzi, onboarding).
- [ ] Dostępność (kontrast, klawiatura, czytniki ekranu) — przy „uniwersalnych kolorach" to naturalne.
- [ ] Telemetria **nie-treściowa** (zliczenia, nie zawartość) do mierzenia użycia.

## Prywatność = architektura, nie copy (najważniejsze)

Zapewnienie „nie czytamy rozmów i anonimizujemy" musi wynikać z budowy systemu:

1. **Rozdziel dwie ścieżki danych:**
   - *user-facing* — obsługa rozmowy w czasie rzeczywistym;
   - *insight* — **osobny, idempotentny pipeline** (Gemini), który **destyluje wnioski** do
     rozwoju system instruction, operując **wyłącznie na zanonimizowanych danych**.
2. **Anonimizacja PRZED destylacją:** usuwanie PII (imiona, lokalizacje, kontakty, szczegóły
   identyfikujące) zanim cokolwiek trafi do warstwy wniosków. Kontrakt skryptu:
   *wejście = surowe rozmowy → wyjście = wnioski bez danych osobowych*.
3. **Test prywatności, nie tylko funkcji:** jednostkowy test, że z destylatu **nie da się**
   odtworzyć tożsamości (re-identyfikacja niemożliwa). To jest test, który MUSI istnieć. → [03](03-testowanie-i-weryfikacja.md)
4. **Retencja i kasowanie:** jasna polityka „ile trzymamy", anonimizacja przechowywanych
   rozmów, ścieżka usunięcia danych przez użytkownika.
5. **„Nie czytamy rozmów" znaczy: żaden człowiek ani proces user-facing nie ogląda treści**;
   destylacja jest zautomatyzowana i zanonimizowana. Napisz to dokładnie tak w polityce — i
   trzymaj się tego w kodzie. → [04](04-skrypty-i-bazy-danych.md)

## UX — minimalistycznie, ale ciepło
- **Uniwersalne, spokojne kolory** (neutralna baza + jeden ciepły akcent). Bez krzykliwości,
  bez „sprzedażowego" tonu. (Paleta tego zestawu docs — `index.html` — jest celowo taka; może
  posłużyć za punkt wyjścia.)
- **Ciepło w odbiorze** — ton odpowiedzi, mikro-copy („jesteśmy tu, żeby pomóc"), brak ścian tekstu.
- **Minimalizm** = mniej elementów, więcej oddechu; nie „pusto i zimno".
- Plan → szkic → review: pokaż 1–2 ekrany, zbierz feedback, dopiero potem rozwijaj. → [06](06-wspolpraca-i-pamiec.md)

## i18n — dyscyplina
- Każdy używany język **kompletny**: UI, disclaimery, błędy, komunikaty limitu, system messages.
- **Test parytetu językowego** (jak na jakub.solutions: EN↔PL parity + martwe linki) — brakujący
  klucz/strona w którymkolwiek języku = **test, który pada**. Żaden język nie zostaje „w połowie". → [03](03-testowanie-i-weryfikacja.md)
- Ton ciepły **w każdym** języku — to nie tylko dosłowne tłumaczenie, ale i rejestr.

## Launch checklist (etap „użyteczne za darmo")
- [ ] Login działa (z testem) · gating darmowy bez linków płatności
- [ ] Polityka prywatności + zgody + disclaimery (pełnoletność, brak terapii, kryzys) we wszystkich językach
- [ ] Pipeline destylacji zanonimizowany + test re-identyfikacji
- [ ] Wydajność zmierzona i poprawiona (liczby przed/po)
- [ ] Unit + Playwright zielone · smoke test po deployu
- [ ] Nightly backup bazy · tagowanie deployów · branded maintenance page
- [ ] UX: spokojne kolory, ciepły ton, przejrzane na 1–2 ekranach

---

> Mapowanie na doktrynę: prywatność/skrypty → [04](04-skrypty-i-bazy-danych.md);
> login/testy → [03](03-testowanie-i-weryfikacja.md); deploy/backup/tag → [05](05-git-i-wdrozenia.md);
> UX/ton/plan-review → [06](06-wspolpraca-i-pamiec.md); start → [07](07-nowy-projekt-checklist.md).
