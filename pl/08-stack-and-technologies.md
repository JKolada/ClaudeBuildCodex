# 08 — Stack i technologie

> Złota zasada altytudy zastosowana do wyboru narzędzi: *najprostsze, co uniesie wymaganie;*
> *złożoność dokładasz, gdy metryka ją wymusi (→ [12](12-flexibility-and-scalability.md)).*

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

## Sprawdzony zestaw (konkretny baseline)

Zestaw przerobiony w boju na realnym projekcie — bierz z niego to, czego wymaga zadanie, resztę pomiń.
Wszystko **dojrzałe, dobrze udokumentowane, łatwe do testowania i hostowania na jednym VPS**:

| Warstwa | Narzędzia |
|---------|-----------|
| **Narzędzie główne / proces** | **Anthropic Claude — Claude Desktop / Claude Code** (agent, którym budujesz) · **Git** (historia, → [05](05-git-and-deployments.md)) · **GitHub** (zdalne repo, PR) · **GitHub Issues** (taski, → [07](07-new-project-day-0.md)) |
| **Format / treść** | HTML5 (server-rendered), Markdown (docs), **JSON** (API, config), XML gdy wymusza integracja |
| **Dane / zapytania** | **SQL** — SQLite (WAL) na start → PostgreSQL przy skali; migracje forward-only |
| **Backend / skrypty** | **Python** (dane, scrapery, migracje na stdlib) · **Node.js + Express** (web/API) · EJS (szablony serwerowe) |
| **Frontend** | minimalny **JS** (vanilla), `marked` do renderu MD; **ikony SVG: wyłącznie Lucide** (jedno źródło geometrii, spójność); fonty self-host |
| **Sesje / bezpieczeństwo** | trwały store sesji (osobny plik, → [14](14-operational-resilience.md)), `helmet`, rate-limit, `bcrypt`, OAuth (passport) |
| **Poczta** | SMTP (587 STARTTLS), zweryfikowana domena nadawcy (→ [14](14-operational-resilience.md)) |
| **Media / obraz** | konwersja do **WebP** (Pillow); porównania obrazów (OpenCV) tylko gdy realnie trzeba |
| **Ingest / scraping** | `requests` + BeautifulSoup (+lxml), fuzzy-match (rapidfuzz), Playwright gdy trzeba przeglądarki (→ [14](14-operational-resilience.md)) |
| **LLM** | klient API (Claude / Anthropic SDK), odpowiedzi **streamowane SSE** (→ [13](13-performance-frontend-and-sql.md)) |
| **Testy** | `pytest` (Python) · Jest + supertest (Node) · Playwright (e2e) (→ [03](03-testing-and-verification.md)) |
| **Build / dev** | esbuild, nodemon; Docker dla powtarzalności |
| **Serwer / ops** | jeden **VPS (Hetzner)** + nginx (TLS, reverse proxy) + `pm2`/`systemd`; analityka GA4 |

**Reguła ikon:** dla SVG trzymaj się **jednego zestawu — Lucide** (geometria w `<symbol>`/sprite,
reszta to styl). Mieszanie bibliotek ikon = niespójny UI i rozjazd wag/stroke'ów.

## Python jako domyślny język
- **Dlaczego:** czytelność (kod jak proza — łatwy review przez człowieka *i* agenta), baterie
  w zestawie, jeden język na API + skrypty + dane/LLM. Mniej kontekstów do trzymania w głowie.
- **FastAPI** dla API: typy + walidacja (Pydantic) + **auto-OpenAPI = darmowy kontrakt** granicy
  front↔back (→ [12](12-flexibility-and-scalability.md)). **pytest** dla testów (→ [03](03-testing-and-verification.md)).
- **Reproducible env:** wirtualne środowisko + **pinned deps** (lock). „Działało wczoraj" znika.
- **Format i typy jako kontrakt:** `ruff`/`black`, type hints. Spójny styl = tańszy review (→ [02](02-skills-and-refactoring.md)).

## Baza danych — od prostego do skali
- **Start: SQLite.** Zero-ops, jeden plik, świetne do MVP i always-on VPS. Nie zaczynaj od
  rozproszonej bazy „bo kiedyś urośnie".
- **Skala: PostgreSQL** — gdy boli współbieżny zapis, role, złożone relacje, rozszerzenia.
  Migrację SQLite→PG przewiduj w modelu od początku (→ [11](11-data-model-and-normalization.md)).
- **Reguły niezależne od silnika:** migracje **forward-only** + backup przed każdą (→ [04](04-scripts-and-databases.md)),
  **slug zamiast ID** w odniesieniach user-danych, indeksy **po pomiarze**, nie z przeczucia (→ [13](13-performance-frontend-and-sql.md)).
- NoSQL / rozproszone — dopiero gdy relacyjna realnie nie wystarcza, nie wcześniej.

## Web i API — kontrakt jako granica
- **Im mniej JS, tym lepiej.** Server-rendered HTML domyślnie; SPA/Next.js tylko gdy interakcja
  tego naprawdę wymaga. Lekki front = szybszy i tańszy w utrzymaniu (→ [13](13-performance-frontend-and-sql.md)).
- **Kontrakt API (OpenAPI) jest granicą** między front a back — pozwala wymienić jedną stronę
  bez dotykania drugiej (→ [12](12-flexibility-and-scalability.md)). Wersjonuj go; błędy zwracaj **ustrukturyzowane**.
- **Streaming / SSE** dla długich odpowiedzi (czat, LLM token-by-token) — user widzi efekt od
  razu, nie pustkę (→ [13](13-performance-frontend-and-sql.md)).

## Docker — powtarzalność, nie kult
- **Po co:** ten sam obraz lokalnie / w CI / na prodzie. „U mnie działa" przestaje istnieć.
- **Higiena:** mały obraz (multi-stage, slim base, **pinned** wersje), `.dockerignore`, proces
  **non-root**. `docker-compose` do lokalnego złożenia (app + baza).
- **Nie konteneryzuj na siłę** pojedynczego skryptu. Docker tam, gdzie zależności bolą — nie jako rytuał.

## Serwer i hosting — jeden box, dobre nawyki

> **Monolit jest domyślną architekturą — promuj go jako najłatwiejszy w utrzymaniu.** Jedna
> aplikacja (web + API + zadania) i jedna baza na **jednym VPS** to coś, co ogarniasz w głowie:
> jeden deploy, jeden log, jeden backup, jeden rollback. Debug to czytanie jednego procesu, nie
> korelowanie śladów po sieci. Rozbicie na usługi/serverless **dokłada** sieć, wersjonowanie
> kontraktów i klasę nowych awarii (→ [14](14-operational-resilience.md)) — sięgaj po nie dopiero,
> gdy **metryka** (ruch, zespół, izolacja awarii) realnie tego wymaga, nie „bo tak się robi".

- **Default: jeden VPS (Hetzner) + nginx** (reverse proxy, TLS) + `systemd`/`pm2`/Docker do
  procesów. Tani, przewidywalny, pełna kontrola, **zero cold startu**. Wiele projektów na jednym
  boxie = osobny vhost + osobny katalog, te same reguły deployu (→ [05](05-git-and-deployments.md)).
- **Scale-to-zero** (Cloud Run / serverless) gdy ruch nierówny/globalny, a **cold start**
  akceptowalny; **always-on VPS** gdy ruch przewidywalny. Świadomy tradeoff koszt/latencja,
  zapisany jako ADR (→ [12](12-flexibility-and-scalability.md)).
- **Usługi zarządzane** (baza, mail, storage) gdy zdejmują ops **taniej**, niż kosztuje
  samodzielne utrzymanie.
- **Sekrety** w env / secret store — **nigdy** w repo (→ [09](09-law-and-protecting-the-creator.md)).

## TDD i pokrycie zmian — twardy rdzeń
Najważniejsze kryterium doboru stacku: ma być **testowalny od pierwszej linijki**. Technologia,
której nie umiesz łatwo objąć testem (test-first, szybki i deterministyczny suite, CI bramkujące),
jest złym wyborem — nawet jeśli modna. Mechanika TDD i pokrycie zmian = kanon w → [03](03-testing-and-verification.md);
tu tylko twarda konsekwencja: **wybieraj tech, która to umożliwia, i traktuj „commit bez testu" jako
niekompletny** (→ [00](00-commandments.md)).

## Reguła wyboru technologii
1. **Najprostsze, co uniesie dzisiejsze wymaganie**, z jawną ścieżką wzrostu (SQLite→PG, VPS→serverless).
2. **Testowalność i ekosystem** ważniejsze niż nowość.
3. Każdy nietrywialny wybór = **ADR**: jedno „dlaczego" + odrzucone alternatywy. Następna sesja
   (człowiek albo agent) ma wiedzieć, czemu tak.

## Anty-wzorce
- 🚫 **Mikroserwisy / Kubernetes / rozproszona baza na MVP** — złożoność, której nikt jeszcze nie potrzebuje (→ [12](12-flexibility-and-scalability.md)).
- 🚫 **Stack pod CV/modę** zamiast pod problem i testowalność.
- 🚫 **Zmiana zachowania bez testu** („dodam później" — nie dodasz).
- 🚫 **Sekrety w repo**; brak pinów wersji → „działało wczoraj".
- 🚫 **SPA / ciężki JS** tam, gdzie wystarczy serwerowy HTML.
- 🚫 **Docker/Cloud jako kult** zamiast narzędzia dobranego do problemu.
