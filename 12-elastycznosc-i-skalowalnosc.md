# 12 — Elastyczność i skalowalność

> Złota zasada altytudy zastosowana do architektury: *wolno tam, gdzie błąd jest drogi; szybko
> tam, gdzie tani.* Skaluj, gdy metryka tego wymaga — nie wcześniej, nie „na zapas".

Elastyczność to zdolność zmiany **bez przepisywania**; skalowalność to zdolność wzrostu **bez
przebudowy**. Oba bierze się z tych samych nawyków: rozdziel warstwy, zmieniaj additive, schowaj
ryzyko za flagą, nie sprzęgaj stanu tam, gdzie nie musisz. I — równie ważne — **nie
over-engineeruj**: prosta architektura, którą umiesz rozwinąć, bije rozproszoną, której nie
potrzebujesz.

## Rozdziel warstwy
- **DB ↔ ingest ↔ web** to trzy oddzielne światy. WhiskyPolska: SQLite (dane) ↔ scrapery Python
  (ingest) ↔ Node/Express (web) — łączy je **kontrakt** (schemat, → [11](11-model-danych-normalizacja.md)),
  nie wspólny kod. Wymienisz scraper bez dotykania weba.
- **Kontrakt API jako granica** — np. front Next.js ↔ backend Python przez jawny kontrakt
  (OpenAPI). Granica, której się trzymasz, pozwala wymienić każdą stronę osobno. → [08](08-stack-i-technologie.md)
- **Wspólny backend pod web + przyszły mobile.** ADR z wyprzedzeniem: SQLite vs Postgres, sesja
  vs JWT (WhiskyPolska: sesja dla weba; mobile w przyszłości → rozważ JWT na wspólnym backendzie).
  Decyzję **zapisz**, nie trzymaj w głowie. → [01](01-dokumentacja-i-ai-readme.md)

## Zmieniaj tak, by się dało cofnąć i rampować
- **Additive / backward-compatible** — nowa kolumna, nowy endpoint, nowy język; nie łam tego,
  co działa (→ [11](11-model-danych-normalizacja.md)).
- **Feature flags** — `feature_flags` w bazie + przełączniki typu `BETA_ALL_PREMIUM`. **Ship dark,
  potem ramp**: kod jedzie wyłączony, włączasz dla części, potem dla wszystkich. Bez flag każda
  zmiana jest all-or-nothing.
- **Stateless, gdzie się da** — im mniej stanu w procesie, tym łatwiej skalować poziomo.

## Platforma: scale-to-zero vs always-on
Realna decyzja z dwóch projektów, **świadomy tradeoff koszt/latencja**:
- **Cloud Run (scale-to-zero)** — płacisz za użycie, zero ruchu = zero kosztu, ale **cold start**
  dodaje latencję pierwszego żądania. Dobre przy nierównym, globalnym ruchu.
- **VPS always-on (Hetzner + pm2)** — WhiskyPolska: stały koszt, **zero cold startu**, pełna
  kontrola. Dobre przy przewidywalnym ruchu i SQLite na dysku.
Wybór = profil ruchu i budżet, nie moda. Zapisz jako ADR.

## Cache i pipeline'y
- **Warstwy cache** z jawną inwalidacją: WhiskyPolska invaliduje cache w pipeline `full`,
  rankingi cache'owane **10 min**, statyki z `max-age` (godzina dev / 7 dni immutable prod).
- **Composable, idempotentne pipeline'y** — `normalize → metadata → enrich → validate → stats`;
  każdy etap odpalalny osobno, ponowne uruchomienie bezpieczne (→ [04](04-skrypty-i-bazy-danych.md)).
- **i18n / multi-market od początku, jeśli globalnie** (np. 16 języków od startu, nie doklejone
  później — → [10](10-seo-i-tlumaczenia.md)).

## Nie over-engineeruj
- **Zacznij prosto.** SQLite + statyczny build (jakub.solutions: build statyczny w Pythonie)
  obsługują zadziwiająco duży ruch. WhiskyPolska na SQLite/WAL serwuje ~8,5k whisky bez Postgresa.
- **Skaluj, gdy metryka tego wymaga** — nie „bo kiedyś urośnie". Right-size do realnego ruchu.
- Migracja SQLite→Postgres, monolit→serwisy: **gdy liczby tego żądają**, z ADR, nie prewencyjnie.

## Anty-wzorce
- 🚫 **Przedwczesna złożoność rozproszona** (mikroserwisy/Kafka/k8s na 100 userów).
- 🚫 **Stanowe sprzężenie blokujące skalowanie** (stan sesji w pamięci procesu bez storu).
- 🚫 **Big-bang rewrite** zamiast zmian additive (→ [04](04-skrypty-i-bazy-danych.md)).
- 🚫 **Brak feature flags** → każda zmiana wymuszona all-or-nothing, brak rampu/dark-shipu.
- 🚫 **Ignorowanie kosztu always-on** (płacisz za idle, gdy scale-to-zero by pasował) — i odwrotnie.
- 🚫 Przepisanie na Postgres „na zapas", gdy SQLite jeszcze się nie zadyszał.

## Dla nowych projektów
Na Dzień 0 (→ [07](07-nowy-projekt-checklist.md)) ustal **trzy granice** (DB / ingest / web) i
zapisz **trzy ADR**: baza (SQLite vs Postgres), sesja vs JWT, platforma (VPS vs Cloud Run).
Wprowadź `feature_flags` od początku — to najtańsza polisa na elastyczność. Zacznij od
najprostszego stacku, który dowozi (statyk/SQLite), a skalowanie odłóż do chwili, gdy konkretna
metryka (latencja, koszt, rozmiar bazy) tego zażąda — i wtedy decyduj liczbami, nie przeczuciem
(→ [13](13-wydajnosc-frontend-i-sql.md)).
