# 11 — Model danych i normalizacja

> Przykazania V i VII u korzenia: *backup to rollback, dane usera nienaruszalne* — ale zanim
> coś zabezpieczysz, musi mieć **kształt**, w którym zmiana jest tania i przewidywalna.

Schemat to **kontrakt całego systemu**. Scrapery, web, pipeline'y, migracje — wszystko opiera
się na nim. Źle znormalizowany model mści się na każdej warstwie: duplikaty danych dryfują,
mapowania po niestabilnym kluczu gubią rekordy, wartości wyliczane rozjeżdżają się ze sobą.
Normalizuj najpierw; denormalizuj **świadomie** i z nazwanym źródłem prawdy.

## Normalizuj najpierw
- **Bez powtarzających się grup.** Wartość raz, w jednym miejscu.
- **Słowniki w tabelach lookup.** W projekcie referencyjnym: `countries` / `regions` / `product_types` /
  `tag_types` — nie free-text w kolumnie. Dodatkowo **`CHECK` na `products.type`**
  (`type_a | type_b | type_c | …`) — baza odrzuca śmieć, zanim wejdzie.
- **Tabele łączące dla M:N.** Produkt ma wiele tagów/atrybutów → **`product_tags`** (junction),
  nie `primary_tag` + `secondary_tag` jako dwa free-text pola (te skasowano migracją 090 —
  junction jest jedynym magazynem atrybutów).

## Stabilne klucze — slug, nie ID
**ID dryfują.** Po merge'ach duplikatów `product_id` się zmienia (kanon przejmuje wiersze,
zduplikowany ginie). Dlatego **stabilnym identyfikatorem jest slug**, nie klucz numeryczny.
Najtwardsza lekcja z projektu referencyjnego — swap prod-bazy: **dane użytkownika mapujesz po slug → nowe ID**,
nigdy po starym ID (recenzja trafiłaby na zły produkt). Brakujący slug **pomijasz i logujesz**,
nie wpychasz na ślepo. → [05](05-git-i-wdrozenia.md)

## Active-row zamiast nadpisywania
Wzorzec z cen, wart przeniesienia wszędzie, gdzie historia ma wartość:
- Kolumna **`expired_at`** (NULL = aktywny). Zmiana ceny → wygaszasz stary wiersz, wstawiasz nowy.
- **Partial unique index** `WHERE expired_at IS NULL` — wymusza „jeden aktywny na klucz"
  (jedna aktywna cena na (produkt, retailer)).
- **Tabela historii** (`price_history`) zapisuje każdą cenę, jaką widziano.
- Efekt: **audyt za darmo** — wiesz, co i kiedy się zmieniło, bez triggerów.

## Kiedy denormalizować (świadomie)
Denormalizacja jest legalna **dla odczytu** — ale zawsze nazwij **źródło prawdy** i pilnuj spójności:
- **Pola wyświetlane/wyliczane → licz w helperach, nie składuj.** `display_name` (brand + wariant +
  nazwa edycji) liczony dynamicznie w `web/src/helpers.js`. Składowany dryfowałby po każdej
  zmianie składnika.
- **Cache denormalizowany z jasnym źródłem.** `ext_profile_cache` trzyma dane z zewnętrznego źródła; kolumny
  `ext_*` **usunięto z `products`** (migracja 051) — cache jest jedynym źródłem, brak dwóch prawd.
- **Snapshot z live-fallback.** `site_stats.json` to zrzut liczb (produkty/ceny/retailerzy);
  czytany przez home, ale z **fallbackiem na żywą bazę**, gdy snapshot nieaktualny.

## Migracje i integralność
- **Forward-only + additive** — `ADD COLUMN` jest backward-compatible; **nigdy DROP/RENAME
  kolumny używanej przez działający stary kod** (→ [04](04-skrypty-i-bazy-danych.md)).
- **FK integrity check** po każdej operacji (`PRAGMA foreign_key_check`).
- **Gating na istnienie kolumny** — skrypt sprawdza, czy kolumna/tabela istnieje, zanim na niej
  operuje (przeżywa różne stany schematu między środowiskami).

## Schemat jako udokumentowany kontrakt
ERD + controlled vocabulary w docs (np. `db_schema.md` z Mermaid ERD,
`data_model_reference.md` z dozwolonymi wartościami `type`/`region`/`tag_types`). Schemat,
którego nikt nie udokumentował, jest schematem, który następna sesja zgaduje. → [01](01-dokumentacja-i-ai-readme.md)

## Anty-wzorce
- 🚫 **Free-text tam, gdzie powinien być słownik** (kraj jako string → 5 pisowni „Szkocja").
- 🚫 **Duplikat źródła prawdy bez synchronizacji** (dane zewnętrzne w `products` *i* w cache → rozjazd).
- 🚫 **Mapowanie user-danych po zmiennym ID** zamiast slug → recenzja na złym produkcie.
- 🚫 **Składowanie wartości wyliczanej, która dryfuje** (`display_name` jako kolumna).
- 🚫 **Destrukcyjna migracja pod działającym starym kodem** (DROP kolumny, którą web jeszcze czyta).
- 🚫 Dwa free-text pola zamiast tabeli łączącej dla relacji M:N.

## W praktyce
Gdy deklarujesz prywatność, **model danych musi ją egzekwować**. Rozdziel ścieżki: dane
user-facing i osobny, idempotentny pipeline przetwarzania, operujący **wyłącznie na danych po
anonimizacji** (PII usunięte *przed* przetwarzaniem). Twierdzenie „nie czytamy danych" musi
wynikać ze **schematu i kontraktu skryptu**, nie z copy — i mieć **test re-identyfikacji**, który
dowodzi, że nie da się odtworzyć tożsamości. → [04](04-skrypty-i-bazy-danych.md), [09](09-prawo-i-ochrona-tworcy.md)
