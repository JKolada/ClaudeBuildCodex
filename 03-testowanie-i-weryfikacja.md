# 03 — Testowanie i weryfikacja

> Przykazanie III: *Weryfikuj, nie deklaruj.*

Dwie różne rzeczy, często mylone:
- **Testy** — zautomatyzowana siatka bezpieczeństwa, którą uruchamiasz wielokrotnie.
- **Weryfikacja** — dowód, że *ta konkretna zmiana* robi to, co miała, **zaobserwowany**, nie założony.

Obie są obowiązkowe. Test, który przechodzi, nie znaczy, że feature działa w przeglądarce;
ręczna weryfikacja bez testów nie chroni przed regresją jutro.

## Piramida (z WhiskyPolska)

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
WhiskyPolska tak złapaliśmy i naprawiliśmy zastane `ERR_HTTP_HEADERS_SENT` na `/mapa`).

## Raport ma być uczciwy
- Testy padają → powiedz to **z outputem**, nie chowaj.
- Coś pominięto → powiedz, że pominięto.
- Gdy 2 testy padają z **dryfu danych** (np. cohort-fixture `85% vs 85%`), a nie z regresji
  — **odróżnij** to jawnie i nie blokuj nimi deployu, ale zaproponuj follow-up (regeneracja fixture'ów).
- „Zrobione i zweryfikowane" mów dopiero, gdy naprawdę zweryfikowane — bez hedgingu, ale i bez ściemy.

## Liczby weryfikuj u źródła
Nie ufaj liczbie z pamięci ani z dokumentacji — odpytaj bazę/test. Dokumentacja się starzeje;
`SELECT COUNT(*)` nie kłamie. (Przykazanie X: „liczby weryfikuj".)

## Web — sprawdzony zestaw kontroli (z jakub.solutions)
Dla stron/projektów webowych ten zestaw testów już się u nas sprawdził (40 metod / 235
subtestów na jakub.solutions) — przenoś go domyślnie:
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

## Dla EchoInsight
Twój explicite cel: **unit + Playwright + testy różnymi technikami**. Plan:
- **Auth** — najpierw test odtwarzający dzisiejszy bug logowania, potem fix (TDD na ścieżce krytycznej).
- **Playwright** — happy-path rozmowy, gating darmowego zakresu, zmiana języka (i18n), zgody/disclaimery.
- **Pipeline anonimizacji** — testy jednostkowe, że z destylatu **nie da się** odtworzyć
  tożsamości (to test prywatności, nie tylko funkcji — patrz [08](08-echoinsight.md)).
- **Wydajność** — zmierz przed/po (czas odpowiedzi, TTFB), nie „wydaje się szybciej".
