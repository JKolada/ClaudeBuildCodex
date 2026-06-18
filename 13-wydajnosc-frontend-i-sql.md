# 13 — Wydajność: frontend i SQL

> Przykazanie III w czystej postaci: *weryfikuj, nie deklaruj* — zastosowane do szybkości.
> „Wydaje się szybciej" nie istnieje. Istnieją **liczby przed/po**.

Wydajność to nie przeczucie, to pomiar. Najczęstszy błąd optymalizacji: zgadywanie, co jest
wolne, i „poprawianie" tego bez dowodu, że było problemem. Mierz **najpierw**, popraw to, co
metryka wskazuje, i **udowodnij liczbą**, że poprawiłeś. Wydajność to też SEO (Core Web Vitals
→ [10](10-seo-i-tlumaczenia.md)) i koszt (szybsze zapytanie = tańszy serwer → [12](12-elastycznosc-i-skalowalnosc.md)).

## Mierz najpierw
- **Lighthouse / Core Web Vitals**: LCP (largest contentful paint), CLS (layout shift),
  INP (interaction), TBT. To są twarde liczby, nie wrażenia.
- **Przed/po, nie „wydaje się szybciej".** Np. optymalizacja home: preload hero,
  GPU-promoted animacje, `content-visibility: auto` poniżej folda; raportujesz LCP przed i po,
  nie „chyba lżej". → [03](03-testowanie-i-weryfikacja.md)
- **SQL: `EXPLAIN QUERY PLAN`** mówi, czy zapytanie używa indeksu, czy skanuje całą tabelę.

## Frontend
- **Code-splitting** + **lazy-load below-fold** — nie ładuj tego, czego user nie widzi.
- **Obrazy**: WebP (np. konwersja wszystkich do WebP q=95), responsive `srcset`,
  **preload hero** (LCP), reszta lazy.
- **Fonty**: self-host (np. Playfair/Outfit, jak na jakub.solutions), `font-display: swap` — tekst
  widoczny zanim font dojdzie.
- **`content-visibility: auto`** na sekcjach poniżej folda — przeglądarka pomija render niewidocznego.
- **GPU-promoted animacje** (`translateZ(0)`/`transform`) zamiast layoutujących właściwości.
- **Cache statyków**: `immutable` + długi `max-age` na prodzie (np. 7 dni immutable prod).
- **Streaming / SSE dla czatu** — odpowiedź LLM **token-by-token** (np. przez SSE), user widzi
  pierwsze słowa od razu, a nie pustkę do końca generacji. → [08](08-stack-i-technologie.md)
- **Server-side pagination** — nigdy nie ślij całego katalogu do przeglądarki (np.
  paginacja po stronie serwera dla ~kilku tysięcy pozycji).

## SQL
- **Indeksy** na kolumnach z `WHERE` i `JOIN` — gorące zapytanie bez indeksu to skan całej tabeli.
- **Partial indexes** — np. `uniq_prices_active … WHERE expired_at IS NULL` (indeks
  tylko na aktywnych cenach — mniejszy, szybszy, wymusza unikalność, → [11](11-model-danych-normalizacja.md)).
- **`EXPLAIN QUERY PLAN`** przed i po dodaniu indeksu — dowód, że plan się zmienił.
- **Unikaj N+1** — nie zapytanie w pętli po każdym wierszu; batch/join za jednym razem.
- **`SELECT` tylko potrzebnych kolumn** — nie `SELECT *`, gdy potrzebujesz trzech pól.
- **Paginacja server-side** + **cache'owane agregaty** (np. `site_stats` zamiast
  `COUNT(*)` po całej bazie na każde wejście na home).
- **WAL** (SQLite) — czytelnicy nie blokują pisarza; domyślny tryb w projekcie referencyjnym.
- **Ostrożnie z `LIKE '%foo'`** — wiodący wildcard zabija indeks (full scan); rozważ FTS, jeśli
  to gorąca ścieżka wyszukiwania.

## Anty-wzorce
- 🚫 **Optymalizacja bez pomiaru** — „poprawiłem", nie wiedząc, czy było wolne (→ [03](03-testowanie-i-weryfikacja.md)).
- 🚫 **Brak indeksu na gorącym zapytaniu** — najczęstsza przyczyna wolnej strony katalogu.
- 🚫 **N+1 w pętli** — 200 zapytań tam, gdzie wystarczył jeden join.
- 🚫 **`SELECT *`** — przesyłasz i deserializujesz kolumny, których nie używasz.
- 🚫 **Client-side pagination ogromnych zbiorów** — ślesz kilka tysięcy rekordów, by pokazać 20.
- 🚫 **Blokowanie UI w oczekiwaniu na pełną odpowiedź LLM** zamiast streamingu (→ [12](12-elastycznosc-i-skalowalnosc.md)).
- 🚫 **Brak cache drogich agregatów** — `COUNT(*)` po całej bazie na każde żądanie.

## Dla nowych projektów
Wpisz do Dnia 0 (→ [07](07-nowy-projekt-checklist.md)): **baseline Lighthouse** zaraz po
pierwszej działającej stronie (masz punkt odniesienia), indeksy na kolumnach filtrów od
pierwszej migracji, `EXPLAIN QUERY PLAN` jako nawyk przy każdym gorącym zapytaniu. Reguła
nadrzędna: **żadna optymalizacja bez liczby przed i po** — bo bez dowodu „optymalizacja" bywa
regresją w przebraniu (→ [03](03-testowanie-i-weryfikacja.md)). Szybkość to jednocześnie SEO
(→ [10](10-seo-i-tlumaczenia.md)) i koszt infrastruktury (→ [12](12-elastycznosc-i-skalowalnosc.md))
— jedna inwestycja, trzy zwroty.
