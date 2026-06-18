# 03 — Testowanie i weryfikacja

> Przykazanie III: *Weryfikuj, nie deklaruj.*

Dwie różne rzeczy, często mylone:
- **Testy** — zautomatyzowana siatka bezpieczeństwa, którą uruchamiasz wielokrotnie.
- **Weryfikacja** — dowód, że *ta konkretna zmiana* robi to, co miała, **zaobserwowany**, nie założony.

Obie są obowiązkowe. Test, który przechodzi, nie znaczy, że feature działa w przeglądarce;
ręczna weryfikacja bez testów nie chroni przed regresją jutro.

## Piramida (z projektu referencyjnego)

| Poziom | Narzędzie | Co pokrywa | Kiedy |
|--------|-----------|------------|-------|
| **Unit** | pytest / Jest | logika czysta (normalizer, matcher, helpery, walidatory) | co commit |
| **Integration** | Supertest (HTTP) | trasy, auth-guardy, API JSON | co commit |
| **E2E / browser** | Playwright | realne ścieżki w przeglądarce, na osobnym porcie | przed deployem / przy UI |
| **Smoke** | skrypt (`smoke.ps1`) | „czy serwer wstaje i N tras zwraca poprawnie" | po restarcie / przed/po deployu |

Reguły, które się sprawdziły:
- **Uruchamiaj testy przed commitem** ścieżki krytycznej.
- **Jest z `--runInBand`**, gdy serwer dev/preview chodzi (konflikt portów/DB).
- **Smoke test ma markery** — sprawdza, że wyrenderowała się *właściwa* strona (np. `price-gate`
  dla anonima, nie tylko HTTP 200).
- **Testy auth z obu stron** — anonim odbity do logowania **i** zalogowany widzi treść.

## „Weryfikuj, nie deklaruj" — w praktyce

Po zmianie obserwowalnej w aplikacji **pokaż dowód**, nie proś usera, żeby sam sprawdził:
- kod HTTP / `redirect_url` (curl `-o /dev/null -w`),
- fragment HTML potwierdzający (np. `og:image` wskazuje na właściwy plik),
- liczby z bazy (ile kont, ile cen, `integrity_check: ok`),
- screenshot przy zmianach wizualnych.

Po **deployu** — smoke test na żywym serwerze (przez `localhost` za flagą maintenance), a
gdy znajdziesz błąd w oknie — napraw go w oknie, jeśli to trywialne i bezpieczne (w
projekcie referencyjnym tak złapaliśmy i naprawiliśmy zastane `ERR_HTTP_HEADERS_SENT` na `/mapa`).

## Raport ma być uczciwy
- Testy padają → powiedz to **z outputem**, nie chowaj.
- Coś pominięto → powiedz, że pominięto.
- Gdy 2 testy padają z **dryfu danych** (np. cohort-fixture `85% vs 85%`), a nie z regresji
  — **odróżnij** to jawnie i nie blokuj nimi deployu, ale zaproponuj follow-up (regeneracja fixture'ów).
- „Zrobione i zweryfikowane" mów dopiero, gdy naprawdę zweryfikowane — bez hedgingu, ale i bez ściemy.

## Liczby weryfikuj u źródła
Nie ufaj liczbie z pamięci ani z dokumentacji — odpytaj bazę/test. Dokumentacja się starzeje;
`SELECT COUNT(*)` nie kłamie. (Przykazanie X: „liczby weryfikuj".)

## Web — sprawdzony zestaw kontroli
Dla stron/projektów webowych ten zestaw testów już się w praktyce sprawdził (typowy zestaw
to kilkadziesiąt metod i kilkaset subtestów) — przenoś go domyślnie:
- **SEO meta** (title/description per strona), **canonical + hreflang**, **JSON-LD**.
- **Dostępność**: kontrast tokenów kolorów, nawigacja klawiaturą, sensowne `alt`/aria.
- **Parytet EN↔PL** (i każdej pary językowej): brakujący klucz/strona w jednym języku = **test, który pada**.
- **Martwe linki wewnętrzne** — żaden link w buildzie nie prowadzi w pustkę.
- **Spójność motywu** (theme cookie / dark-light) i poprawność builda (każda strona się wyrenderowała).

## Anty-wzorce
- 🚫 „Powinno działać" jako konkluzja.
- 🚫 Uruchomienie tylko jednego testu i ogłoszenie „suite zielony".
- 🚫 Pominięcie smoke testu po deployu, bo „przecież testy przeszły".
- 🚫 Mylenie „kod się kompiluje" z „feature działa dla użytkownika".

## TDD — domyślny tryb pracy

Test **najpierw**, nie po fakcie. Cykl:
1. **Czerwony** — napisz test, który opisuje oczekiwane zachowanie i **pada**.
2. **Zielony** — najmniejsza zmiana w kodzie, aż test przechodzi.
3. **Refactor** — posprzątaj przy zielonym suite (→ [02](02-skille-i-refaktoring.md)).

Bug naprawiasz tak samo: **najpierw test odtwarzający** błąd, potem fix — test zostaje jako
regresja, żeby błąd nie wrócił.

> **Każda zmiana w commicie niesie test.** Twarda reguła: commit, który zmienia zachowanie, a
> nie dodaje/zmienia testu, jest **niekompletny**. Nowy endpoint → test trasy; nowy próg/fallback
> → test progu; naprawiony bug → test regresji. „Dodam testy później" = grzech (koniec nie
> nadchodzi). → [00](00-przykazania.md), [08](08-stack-i-technologie.md)

- **Testuj kontrakt, nie implementację** — inaczej refactor kruszy testy bez realnej regresji.
- **Suite szybki i deterministyczny** — wolny lub migający suite przestaje być uruchamiany;
  izoluj I/O, ustaw seedy, `--runInBand` przy współdzielonym porcie/DB.
- **CI bramkuje** — czerwone testy blokują merge i deploy; testy ścieżki krytycznej odpalasz przed commitem.
