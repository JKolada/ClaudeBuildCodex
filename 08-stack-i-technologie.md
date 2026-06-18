# 08 — Stack i technologie

> Złota zasada altytudy zastosowana do wyboru narzędzi: *najprostsze, co uniesie wymaganie;*
> *złożoność dokładasz, gdy metryka ją wymusi (→ [12](12-elastycznosc-i-skalowalnosc.md)).*

Doktryna jest agnostyczna co do języka — ale wybór stacku decyduje, **jak tani jest błąd**
i **jak łatwo to przetestować**. Ten rozdział to rozsądny *default* dla projektu prowadzonego
z Claude: uniwersalny, prosty, elastyczny i skalowalny. Nie dogmat — punkt wyjścia, od którego
odchodzisz świadomie (i zapisujesz dlaczego jako ADR).

## Domyślny stack (sensowny start)

| Warstwa | Default | Kiedy zmienić |
|---------|---------|---------------|
| Backend / skrypty | **Python** (+ FastAPI dla API) | Front i back dzielą TypeScript → Node |
| Baza | **SQLite** | Współbieżny zapis / role / relacje / skala → **PostgreSQL** |
| Web / front | Server-rendered HTML + trochę JS | Bogaty, interaktywny UI → Next.js |
| API | REST/JSON z jawnym kontraktem (OpenAPI) | gRPC dopiero przy realnej potrzebie |
| Cache / kolejka | brak → dołóż Redis, gdy profil ruchu wymusi | nie „na zapas" |
| Pakowanie | **Docker** (powtarzalność) | trywialny skrypt bez zależności → bez kontenera |
| Hosting | jeden **VPS (Hetzner)** + nginx | nierówny/globalny ruch → serverless (scale-to-zero) |

Reguła nadrzędna: **nudna, dojrzała technologia bije modną.** Liczy się ekosystem, dokumentacja
i testowalność — nie hype.

## Python jako domyślny język
- **Dlaczego:** czytelność (kod jak proza — łatwy review przez człowieka *i* agenta), baterie
  w zestawie, jeden język na API + skrypty + dane/LLM. Mniej kontekstów do trzymania w głowie.
- **FastAPI** dla API: typy + walidacja (Pydantic) + **auto-OpenAPI = darmowy kontrakt** granicy
  front↔back (→ [12](12-elastycznosc-i-skalowalnosc.md)). **pytest** dla testów (→ [03](03-testowanie-i-weryfikacja.md)).
- **Reproducible env:** wirtualne środowisko + **pinned deps** (lock). „Działało wczoraj" znika.
- **Format i typy jako kontrakt:** `ruff`/`black`, type hints. Spójny styl = tańszy review (→ [02](02-skille-i-refaktoring.md)).

## Baza danych — od prostego do skali
- **Start: SQLite.** Zero-ops, jeden plik, świetne do MVP i always-on VPS. Nie zaczynaj od
  rozproszonej bazy „bo kiedyś urośnie".
- **Skala: PostgreSQL** — gdy boli współbieżny zapis, role, złożone relacje, rozszerzenia.
  Migrację SQLite→PG przewiduj w modelu od początku (→ [11](11-model-danych-normalizacja.md)).
- **Reguły niezależne od silnika:** migracje **forward-only** + backup przed każdą (→ [04](04-skrypty-i-bazy-danych.md)),
  **slug zamiast ID** w odniesieniach user-danych, indeksy **po pomiarze**, nie z przeczucia (→ [13](13-wydajnosc-frontend-i-sql.md)).
- NoSQL / rozproszone — dopiero gdy relacyjna realnie nie wystarcza, nie wcześniej.

## Web i API — kontrakt jako granica
- **Im mniej JS, tym lepiej.** Server-rendered HTML domyślnie; SPA/Next.js tylko gdy interakcja
  tego naprawdę wymaga. Lekki front = szybszy i tańszy w utrzymaniu (→ [13](13-wydajnosc-frontend-i-sql.md)).
- **Kontrakt API (OpenAPI) jest granicą** między front a back — pozwala wymienić jedną stronę
  bez dotykania drugiej (→ [12](12-elastycznosc-i-skalowalnosc.md)). Wersjonuj go; błędy zwracaj **ustrukturyzowane**.
- **Streaming / SSE** dla długich odpowiedzi (czat, LLM token-by-token) — user widzi efekt od
  razu, nie pustkę (→ [13](13-wydajnosc-frontend-i-sql.md)).

## Docker — powtarzalność, nie kult
- **Po co:** ten sam obraz lokalnie / w CI / na prodzie. „U mnie działa" przestaje istnieć.
- **Higiena:** mały obraz (multi-stage, slim base, **pinned** wersje), `.dockerignore`, proces
  **non-root**. `docker-compose` do lokalnego złożenia (app + baza).
- **Nie konteneryzuj na siłę** pojedynczego skryptu. Docker tam, gdzie zależności bolą — nie jako rytuał.

## Serwer i hosting — jeden box, dobre nawyki
- **Default: jeden VPS (Hetzner) + nginx** (reverse proxy, TLS) + `systemd`/`pm2`/Docker do
  procesów. Tani, przewidywalny, pełna kontrola. Wiele projektów na jednym boxie = osobny vhost
  + osobny katalog, te same reguły deployu (→ [05](05-git-i-wdrozenia.md)).
- **Scale-to-zero** (Cloud Run / serverless) gdy ruch nierówny/globalny, a **cold start**
  akceptowalny; **always-on VPS** gdy ruch przewidywalny. Świadomy tradeoff koszt/latencja,
  zapisany jako ADR (→ [12](12-elastycznosc-i-skalowalnosc.md)).
- **Usługi zarządzane** (baza, mail, storage) gdy zdejmują ops **taniej**, niż kosztuje
  samodzielne utrzymanie.
- **Sekrety** w env / secret store — **nigdy** w repo (→ [09](09-prawo-i-ochrona-tworcy.md)).

## TDD i pokrycie zmian — twardy rdzeń
Najważniejsze kryterium doboru stacku: ma być **testowalny od pierwszej linijki**. Technologia,
której nie umiesz łatwo objąć testem (test-first, szybki i deterministyczny suite, CI bramkujące),
jest złym wyborem — nawet jeśli modna. Mechanika TDD i pokrycie zmian = kanon w → [03](03-testowanie-i-weryfikacja.md);
tu tylko twarda konsekwencja: **wybieraj tech, która to umożliwia, i traktuj „commit bez testu" jako
niekompletny** (→ [00](00-przykazania.md)).

## Reguła wyboru technologii
1. **Najprostsze, co uniesie dzisiejsze wymaganie**, z jawną ścieżką wzrostu (SQLite→PG, VPS→serverless).
2. **Testowalność i ekosystem** ważniejsze niż nowość.
3. Każdy nietrywialny wybór = **ADR**: jedno „dlaczego" + odrzucone alternatywy. Następna sesja
   (człowiek albo agent) ma wiedzieć, czemu tak.

## Anty-wzorce
- 🚫 **Mikroserwisy / Kubernetes / rozproszona baza na MVP** — złożoność, której nikt jeszcze nie potrzebuje (→ [12](12-elastycznosc-i-skalowalnosc.md)).
- 🚫 **Stack pod CV/modę** zamiast pod problem i testowalność.
- 🚫 **Zmiana zachowania bez testu** („dodam później" — nie dodasz).
- 🚫 **Sekrety w repo**; brak pinów wersji → „działało wczoraj".
- 🚫 **SPA / ciężki JS** tam, gdzie wystarczy serwerowy HTML.
- 🚫 **Docker/Cloud jako kult** zamiast narzędzia dobranego do problemu.
