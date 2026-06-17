# 00 — Dekalog

Rdzeń doktryny. Jeśli przeczytasz tylko jeden plik z tego zestawu — niech to będzie ten.
Każde przykazanie ma rozwinięcie w dalszych rozdziałach.

---

### I. Dokumentuj dla agenta, nie dla archiwum.
Każdy katalog ma `AI_README.md`. Aktualizujesz go **przed** commitem, nie „kiedyś".
Dokumentacja, którą czyta się przed dotknięciem kodu, oszczędza godziny re-derywacji;
dokumentacja pisana po fakcie gnije. → [01](01-dokumentacja-i-ai-readme.md)

### II. Szukaj w historii, zanim napiszesz linijkę.
`git log -S"symbol"`, `git log --grep`, `git blame`, AI_README katalogu. Większość
„nowych" problemów ktoś już rozwiązał w tym repo — istnieje helper, była migracja, jest
powód, dla którego kod ma taki kształt. Re-derywacja jest droższa niż minuta szukania. → [05](05-git-i-wdrozenia.md)

### III. Weryfikuj, nie deklaruj.
Nie piszesz „działa" — pokazujesz **dowód**: smoke test, kod HTTP, liczby, screenshot.
Jeśli testy padają — mówisz to z outputem. Jeśli krok pominięto — mówisz, że pominięto.
Zaufanie buduje się na uczciwym raporcie, nie na optymizmie. → [03](03-testowanie-i-weryfikacja.md)

### IV. Dry-run jest domyślny; `--execute` jest świadomy.
Każdy skrypt, który zmienia dane, najpierw **pokazuje plan** (co, ile, gdzie). Mutację
odpalasz dopiero po przeczytaniu tego planu. Skrypt bez trybu próbnego to broń bez
bezpiecznika. → [04](04-skrypty-i-bazy-danych.md)

### V. Backup to mechanizm rollbacku, nie ostrożność.
Migracje **forward-only** (bez down-migracji). Snapshot **przed** każdą zmianą schematu
lub danych na prodzie. Cofnięcie schematu = przywrócenie backupu. Backup nie jest
„na wszelki wypadek" — jest *jedyną* drogą powrotu. → [04](04-skrypty-i-bazy-danych.md)

### VI. Prod jest święty — nie dotykasz go bez wyraźnego „wdrażaj".
Commit i push na życzenie to **nie** deploy. `git pull` na serwerze, `pm2 reload`, swap
bazy, flaga maintenance — tylko gdy user powie wprost. Działania nieodwracalne i „na
zewnątrz" (publikacja, wysyłka, kasowanie) potwierdzaj zawsze. Zgoda w jednym kontekście
nie rozciąga się na następny. → [05](05-git-i-wdrozenia.md)

### VII. Dane użytkownika są nienaruszalne.
Przy podmiance bazy: wylicz **każdą** tabelę z FK do użytkownika (konta, recenzje, koszyki,
odznaki, gry, czat, sesje), mapuj user-dane po **stabilnym kluczu** (slug), nie po ID
(ID dryfują po merge'ach), źródłem prawdy dla kont jest **żywy prod**, a po wszystkim
sprawdź `integrity_check` i policz wiersze. → [05](05-git-i-wdrozenia.md)

### VIII. Taguj każdy deploy i pisz, co user zyskał.
Annotated tag (`deploy-RRRR-MM-DD`) to jedyny stabilny znacznik „co jest live" i podstawa
rollbacku. Przy każdym deployu zaktualizuj publiczny changelog — **prostym językiem, bez
żargonu** (żadnego „scraper/migracja/commit"; pisz, co użytkownik zyskuje). → [05](05-git-i-wdrozenia.md)

### IX. Mały, spójny commit; jeden temat.
Rozdzielaj niezwiązane zmiany na osobne commity. Trzymaj `git status` czysty — śmieci
(`.bak`, pliki tymczasowe, przypadkowe bazy) i sieroty (niezacommitowana praca w tle)
wykrywaj **wcześnie**, zanim wmieszają się w deploy. Rozróżniaj realny diff od szumu CRLF. → [05](05-git-i-wdrozenia.md)

### X. Plan → iteruj → review.
Najpierw pokaż plan albo szkic (3 przykłady, nie 100). Zbierz feedback. Dopiero potem
skaluj. **Liczby weryfikuj** u źródła. UX dowieź z **ciepłem** w odbiorze, nie tylko
poprawnością — produkt ma być przyjemny, nie tylko działający. → [06](06-wspolpraca-i-pamiec.md)

---

## Siedem grzechów głównych (czego NIE robić)

1. **Nadęty optymizm w raporcie** — „wszystko działa" bez dowodu. (łamie III)
2. **Mutacja bez planu** — odpalenie skryptu zmieniającego dane od razu z `--execute`. (łamie IV)
3. **Auto-deploy** — „skoro gotowe, to wrzucam na prod". (łamie VI)
4. **Swap bazy „prócz kont" potraktowany jako jedna tabela `users`** — utrata recenzji/odznak/czatu, bo nie wyliczono wszystkich tabel FK. (łamie VII)
5. **Commit-śmietnik** — niezwiązane zmiany + artefakty w jednym commicie. (łamie IX)
6. **Skalowanie przed review** — wygenerowanie 500 sztuk, zanim user zobaczył 3. (łamie X)
7. **Dokumentacja „później"** — kod idzie, AI_README zostaje w tyle, następna sesja błądzi. (łamie I)

---

## Złota zasada altytudy

> **Wolno tam, gdzie błąd jest drogi (prod, dane userów, schemat). Szybko tam, gdzie jest
> tani (lokalny eksperyment, szkic UI, dry-run).** Tempo dobieraj do kosztu pomyłki, nie do
> niecierpliwości.
