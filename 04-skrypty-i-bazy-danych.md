# 04 — Skrypty i bazy danych

> Przykazania IV i V: *Dry-run jest domyślny; backup to mechanizm rollbacku.*

## Skrypty — zasady

### 1. Tryb próbny jest domyślny
Każdy skrypt, który **zmienia dane**, działa domyślnie jako `--dry-run` i wypisuje plan:
co, ile wierszy, gdzie. Mutację włącza świadome `--execute`. To uratowało WhiskyPolska
niejeden raz — widzisz „4 OK, 0 pominiętych" zanim cokolwiek się zapisze.

```
python -m scripts.x.do_thing            # dry-run: pokazuje plan
python -m scripts.x.do_thing --execute  # zapisuje
```

### 2. Idempotencja
Skrypt odpalony dwa razy ma dać ten sam stan, nie podwojony. Migracje/loadery treści
pisz tak, by `INSERT OR IGNORE` / `UPSERT` — żeby ponowne uruchomienie było bezpieczne
(w WhiskyPolska loadery treści Whiskypedii są jawnie idempotentne i to jest wymóg deployu).

### 3. Organizacja przez etapy pipeline'u
Skrypty grupuj wg fazy (`setup/`, `normalize/`, `enrich/`, `validate/`, `images/`,
`dedup/`, `orchestration/`). Zostaw **shim-y kompatybilności**, gdy przenosisz pliki.
Złóż je w **komponowalne pipeline'y** (`post-scrape`, `full`) — ale **mutujące katalog
operacje trzymaj POZA automatycznym pipeline'em** (dedup/merge odpalasz ręcznie:
dry-run → review → `--execute`).

### 4. Loguj, czego NIE zrobiłeś
Jeśli skrypt ucina zakres (top-N, sampling, pominięte wiersze) — **wypisz to**. Ciche
ucięcie czyta się jako „pokryłem wszystko", a nie pokryłeś.

### 5. Środowisko zapisz w dokumentacji
Interpreter, zmienne (`PYTHONIOENCODING=utf-8` na Windows), skąd brać venv. Agent nie
zgaduje ścieżki do Pythona — czyta ją z `CLAUDE.md`.

## Bazy danych i migracje

### Migracje są forward-only
Brak down-migracji. Jeden numerowany plik = jeden krok naprzód. **Rollback schematu =
przywrócenie backupu**, nie odwrotna migracja. Dlatego:

### Backup PRZED każdą zmianą schematu/danych na prodzie
```bash
sqlite3 data/whisky.db ".backup backups/pre-deploy-$(date +%F_%H%M%S).db"
```
To nie ostrożność — to *mechanizm cofania*. Trzymaj retencję (np. 14 dni) i nazwij
snapshoty czytelnie (`pre-deploy-*`, `pre-swap-*`, `replaced-prod-*`).

### Additive > destructive
`ADD COLUMN` jest backward-compatible (stary kod dalej działa). **Nigdy nie DROP/RENAME
kolumny w tej samej migracji, której wciąż używa działający stary kod** — rozbij zmianę
destrukcyjną na późniejszy deploy, gdy nikt już kolumny nie czyta.

### Integralność po fakcie
Po każdej operacji na danych: `PRAGMA integrity_check` + `PRAGMA foreign_key_check` +
policz wiersze. Odróżnij **szum zastany** (osierocone wiersze staging obecne i przed, i po)
od **regresji** (nowe naruszenia, których wcześniej nie było). W WhiskyPolska merged DB
miała *mniej* naruszeń niż lokalna — to był sygnał, że migracja posprzątała, nie zepsuła.

### Model „aktywny wiersz" zamiast nadpisywania
Wzorzec z cen: zamiast UPDATE in-place, **wygaszaj** stary wiersz (`expired_at`) i wstawiaj
nowy; partial unique index pilnuje „jeden aktywny na klucz". Historia zostaje, audyt jest
darmowy. Rozważ taki model wszędzie, gdzie historia ma wartość.

### Snapshot do transferu rób przez `.backup` / `VACUUM INTO`, nie `cp` żywego pliku
Żywy SQLite z WAL skopiowany `cp` bywa niespójny. `.backup` (online-safe) albo
`VACUUM INTO` dają spójną, zdefragmentowaną kopię. **Nigdy nie SCP żywego `.db`.**

## Anty-wzorce
- 🚫 Skrypt mutujący bez `--dry-run`.
- 🚫 Deploy z migracją bez backupu „bo additive".
- 🚫 DROP kolumny używanej przez działający kod.
- 🚫 `cp whisky.db` przy włączonym serwerze → niespójny snapshot.
- 🚫 Wpięcie operacji mutującej katalog w automatyczny pipeline.

## Dla EchoInsight
- Jeśli relacyjna baza → migracje forward-only + backup przed każdą.
- **Pipeline anonimizacji** (Gemini destyluje wnioski) = osobny, idempotentny skrypt z
  dry-run; jego kontrakt: na wejściu surowe rozmowy, na wyjściu **wnioski bez danych
  osobowych**, z testem, że re-identyfikacja jest niemożliwa. Trzymaj go POZA ścieżką
  user-facing. → [08](08-echoinsight.md)
