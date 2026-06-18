# 05 — Git i wdrożenia

> Przykazania II, VI, VII, VIII, IX. Najgęstszy rozdział, bo tu błąd jest najdroższy.

## Git — dwa nawyki na większości zadań

### A. Szukaj w historii ZANIM zaimplementujesz
```bash
git log --oneline -- <ścieżka>      # historia pliku/katalogu
git log -S"symbol" --oneline        # pickaxe: gdzie narodził się symbol/flaga/kolumna
git log -G"regex" --oneline         # commity, których DIFF pasuje do regex
git log --grep="słowo" --oneline    # przeszukaj treści commitów (tam opisane są featury)
git blame <plik> -L a,b             # kto/kiedy/dlaczego
git show <commit>                   # pełna zmiana + kontekst
```
Łącz to z grep po drzewie + `AI_README.md` katalogu. Historia + kod + docs = pełny obraz w
minutę. Robi to różnicę przy: nieznanym kodzie, hunchu „czy my już tego nie robiliśmy",
kolumnie/fladze nieznanego pochodzenia, datowaniu regresji, przed każdym refaktorem.

### B. Czysty, spójny `git status`
- **Rozdzielaj niezwiązane zmiany** na osobne commity (jeden temat = jeden commit).
- **Wykrywaj śmieci wcześnie:** `.bak`, pliki tymczasowe, przypadkowe bazy (`web/_Proj…db`),
  plik o nazwie `-w` z błędnego `curl`. Dodaj wzorce do `.gitignore` (uwaga: gitignore
  **nie ma komentarzy w tej samej linii** — `#` w osobnej linii).
- **Odróżniaj realny diff od szumu CRLF:** `git status` pokazuje plik jako zmieniony, a
  `git diff HEAD` jest pusty → to tylko EOL, nie praca. Nie commituj szumu.
- **Sieroty (niezacommitowana praca w tle)** — w projekcie prowadzonym wielosesyjnie
  („użytkownik + Claude") inne sesje zostawiają zmiany w drzewie. Przed deployem: czy to realna,
  kompletna praca (commituj/potwierdź), czy WIP/eksperyment (zostaw)? **Nie wmiataj cudzej
  niezacommitowanej pracy do deployu bez potwierdzenia.**

### Co kończy commit
- Wiadomości po angielsku, opisowe (co + dlaczego), `fixes #N`/`refs #N` do issue.
- Linkuj PR/issue pełnym URL-em, nie „PR #123".

## Wdrożenia — POLITYKA NADRZĘDNA

> ⛔ **Nigdy nie deployuj na prod automatycznie.** `git pull` na serwerze, `pm2 reload`,
> swap bazy, `migrate.py` na prodzie, flaga maintenance — **tylko gdy user powie wprost**
> („wdrażaj", „deploy"). Możesz **proaktywnie zaproponować** deploy, gdy gotowe — ale czekasz
> na jawne „tak". Commit + push na życzenie to **nie** deploy. Ta reguła bije „auto mode".

### Dwa typy deployu
- **Code-only (bez migracji/zależności)** → zero-downtime: `git pull` + `pm2 reload`.
- **Z migracją/zmianą zależności/swapem bazy** → **okno maintenance** (flaga nginx → 503 +
  branded strona), kilka sekund downtime, gwarancja że app nie biegnie na pół-zmigrowanym schemacie.

### Taguj KAŻDY deploy
```bash
git tag -a deploy-$(date +%F) -m "Co idzie na prod: <jedno zdanie>"   # -2/-3 dla kolejnego tego dnia
git push --tags
```
- Co jest live: `git describe --tags --abbrev=0 --match 'deploy-*'`.
- Rollback kodu: `git checkout <deploy-tag> && pm2 reload`.
- Rollback schematu: przywróć backup (forward-only!).

### Changelog przy każdym deployu
Publiczny „Co nowego" — **prostym językiem, bez żargonu** (żadnego scraper/migracja/commit).
Pisz, **co użytkownik zyskuje**. Bump daty `updated:`. To część checklisty deployu, nie opcja.

---

## Swap bazy z zachowaniem kont — runbook (najtrudniejsza operacja)

Pełna podmianka prod-bazy (np. lokalny katalog z całą pracą) **z zachowaniem żywych kont**.
To tu jest najwięcej pułapek. Lekcje z projektu referencyjnego:

### Zasady, które ratują dane userów (Przykazanie VII)
1. **„Użytkownicy" to wiele tabel, nie jedna `users`.** Wylicz **każdą** tabelę z FK do
   użytkownika: konta, koszyki, recenzje, polubienia, odznaki, gry, czat (sesje +
   wiadomości + limity), feedback, sesje. Tabelę bez `user_id` (np. `chat_messages`) mapuj
   po jej rodzicu (`session_id`). Gateuj każdą na istnienie kolumny/tabeli.
2. **Mapuj po STABILNYM kluczu (slug), nie po ID.** `product_id` dryfuje między
   bazami po merge'ach — recenzja użytkownika musi trafić po `slug → nowe_id`, a brakujący
   slug jest **pomijany i logowany**, nie wpychany na ślepo.
3. **Źródłem prawdy dla kont jest ŻYWY prod**, nie stary snapshot — żeby nie zgubić
   rejestracji z ostatniej godziny. Migrację uruchom **w oknie maintenance, po `pm2 stop`**,
   czytając zatrzymaną, spójną prod-bazę.
4. **Kolejność FK-safe**: WIPE dzieci przed rodzicami, INSERT rodziców przed dziećmi
   (np. `reviews` przed `review_likes`; `chat_sessions` przed `chat_messages`).
5. **Backup żywego proda PRZED swapem** (`.backup replaced-prod-<ts>.db`) — to Twój rollback.
6. **Zweryfikuj scaloną bazę**: liczba kont = prod, 0 wiszących recenzji (slug-remap OK),
   `integrity_check: ok`, naruszenia FK ≤ stan zastany (nie więcej).
7. **Sesje to osobny, ulotny stan — nie mieszaj ich z podmienianą bazą.** Trzymaj store sesji w
   **osobnym pliku** (np. `sessions.db`) niż baza katalogowa, którą czasem podmieniasz w całości —
   inaczej swap wyzeruje zalogowanych. Store w pamięci procesu wylogowuje wszystkich przy **każdym**
   restarcie/deployu i przecieka pamięć (→ [14](14-odpornosc-operacyjna.md)).

### Sekwencja (faza nieinwazyjna → okno → finalizacja)
**Faza 1 (serwis żyje):**
- push kodu na GitHub;
- **obrazki/assety gitignorowane kopiuj osobno** (rsync albo tar-over-ssh, **nie** przez git),
  PRZED oknem — są nieaktywne, dopóki nie podmienisz bazy. Wysyłaj tylko deltę (policz brakujące).
- pre-upload czystego snapshotu katalogu na serwer (`/tmp`).

**Faza 2 (okno maintenance, kilkanaście sekund), atomowo (`set -e`):**
`flaga ON → git pull → pm2 stop → backup żywego proda → migrate-users (źródło = prod) →
swap pliku (rm wal/shm, mv, PRAGMA journal_mode=WAL) → pm2 start → SMOKE TEST → flaga OFF`.

**Faza 3:** tag `deploy-…-2` + push, FB/SEO re-scrape jeśli dotyczy, sprzątanie `/tmp` i lokalnych temp.

### Smoke test po swapie (zanim zdejmiesz flagę)
Przez `localhost` (omija nginx maintenance): home/katalog/detal → 200, og:image →
właściwy plik, redirecty (np. scalone → 301 do survivora), liczby w bazie (konta/rekordy),
**`pm2 logs` na błędy**. Znaleziony, trywialny i bezpieczny bug — napraw w oknie i dociągnij
(commit → pull → reload), zamiast wypuszczać znane 500.

### Asety gitignorowane a deploy
Obrazki/pliki, które są w `.gitignore`, **nie jadą przez `git pull`**. Albo je zsynchronizuj
(rsync/tar), albo wygeneruj na serwerze (jeśli ma narzędzia). W projekcie referencyjnym decyzja:
**kopiujemy z lokalnej**, bo serwer nie ma Pillow, a swap zmienia katalog.

## Anty-wzorce
- 🚫 Auto-deploy / „skoro gotowe to wrzucam".
- 🚫 Swap „prócz kont" = tylko `users` → utrata recenzji/odznak/czatu.
- 🚫 Mapowanie user-danych po ID zamiast slug → recenzje lądują na złym produkcie.
- 🚫 Migracja na starym snapshocie → utrata świeżych rejestracji.
- 🚫 Brak tagu deployu → „co jest live?" staje się zgadywanką.
- 🚫 Transfer 1.5 GB assetów **w** oknie maintenance → długi downtime (rób przed oknem).
- 🚫 Sesje w bazie podmienianej swapem (albo w pamięci procesu) → deploy wylogowuje wszystkich.
- 🚫 Niezmiennik skryptu deployu nietknięty testem — np. `$(date)` rozwinięty raz przy tworzeniu
  pliku (każdy backup nadpisuje ten sam plik). Zabetonuj niezmienniki deploy-skryptu testem.

> **Runbook to pamięć incydentów, nie głowa.** Każda awaria na prodzie → wpis w runbooku z datą
> i ponumerowaną lekcją (np. „nigdy nie SCP żywej `.db` — użyj `.backup`; WAL trzyma świeże strony").
> Następny swap czyta runbook, nie powtarza błędu (→ [06](06-wspolpraca-i-pamiec.md), [14](14-odpornosc-operacyjna.md)).

## Wspólna infrastruktura
Projekty mogą dzielić jeden **Hetzner VPS**: statyczne (build `dist/`) idą przez
`scp`/`rsync` + nginx vhost; aplikacje Node przez `git pull` + `pm2 reload` za
nginx. Jeden serwer = wspólny katalog `backups/`, te same nawyki (tag deployu, maintenance
flag). Nowy projekt na tym samym boxie: osobny vhost + osobny katalog, te same reguły.

## W praktyce
Ścieżkę krytyczną (np. logowanie) wdrażaj z testem i pełnym smoke (rejestracja, login,
wylogowanie, trwałość sesji). Przy pierwszym realnym ruchu userów ustaw od razu: nightly backup
bazy, tagowanie deployów, branded maintenance page. → [03](03-testowanie-i-weryfikacja.md)
