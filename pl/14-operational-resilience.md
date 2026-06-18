# 14 — Odporność operacyjna i zewnętrzne zależności

> Przykazania III, V, VI w warstwie runtime: *prod żyje w zawodnym świecie*. Sieć rwie,
> provider blokuje porty, scraper pada w połowie, płatne API kosztuje przy każdym żądaniu.
> Doktryna z rozdziałów 03–05 dba o **kod i wdrożenie**; ten rozdział o tym, co dzieje się
> **po** — gdy realni użytkownicy i niezależne systemy uderzają w działający serwis.

Te lekcje są drogo opłacone: prawie każda to incydent na prodzie, nie teoria. Wspólny mianownik —
**najgorsze bugi nie krzyczą, tylko cicho zawieszają, wylogowują albo drenują budżet.**

## 1. Jeden zły request nie może położyć procesu

Niezłapany `throw`/rejection w handlerze async potrafi ubić **cały** serwer (Node/Express:
rejection → exit procesu → pętla restartów pm2). Zbuduj siatkę na poziomie procesu:

- **Globalne łapacze**: `process.on('unhandledRejection')` i `'uncaughtException')` — logują i
  kontrolowanie kończą, nie zostawiają zombie-procesu.
- **Wrapper async-route** przekazujący błąd do `next(err)` zamiast gubić go w niezłapanym promise.
- **Middleware 500**, który **nie wycieka stack trace** użytkownikowi (→ [09](09-law-and-protecting-the-creator.md)).
- **Defensywa na danych z brzegu**: konto OAuth bez hasła, pole `null` tam gdzie kod zakłada string —
  to realne wejścia, gdy wpuścisz prawdziwych userów (często ujawnia się **po swapie bazy**, → [05](05-git-and-deployments.md)).

> Reguła: *throw w jednym żądaniu degraduje to żądanie, nie serwis.* Otestuj regresyjnie (→ [03](03-testing-and-verification.md)).

## 2. Długie zadania: wznawialne i odpięte od sesji agenta

Scraper/ETL „zbierz wszystko → zapisz raz" traci 100% pracy przy każdym crashu. Pisz **batchami**:

- **Checkpoint zrobionych jednostek** (plik/tabela z URL-ami/ID) — restart wznawia od miejsca, nie od zera.
- **Zapis co N**, nie na końcu — crash kosztuje ostatni batch, nie cały run.
- **Długi run odpalaj z realnego terminala**, nie z tła sesji Claude. Tło agenta to **nietrwały
  runner** — teardown hosta sesji ubija proces w połowie (to nie anti-bot, to znikający runner).
- Idempotencja całości (→ [04](04-scripts-and-databases.md)): wznowiony job nie dubluje już zapisanych danych.

## 3. Zewnętrzne źródła traktuj jak wrogie

Cudze API i strony rwą połączenia, rate-limitują (429), zwracają 200 z HTML-em błędu. Zakładaj zawodność:

- **Timeout na każde wywołanie** — bez niego socket wisi w nieskończoność (cichy zawis, nie błąd).
- **Retry z exponential backoff** (np. 10/20/30 s), z górnym limitem prób.
- **Rotacja sesji i User-Agent** przy masowym I/O — nowe `Session` (świeże TCP/cookies) co batch,
  UA z puli realnych przeglądarek (część hostów rwie po ~kilkuset żądaniach z jednej sesji).
- **Waliduj odpowiedź, nie status** — „200 + strona błędu" to porażka; sprawdź kształt danych.

## 4. Infrastruktura providera narzuca limity — weryfikuj end-to-end

Hosting ma własne reguły sieciowe, które kładą „działający" kod dopiero na prodzie:

- **Porty bywają blokowane.** Np. wyjściowy SMTP 465 potrafi być zamknięty → użyj **587 + STARTTLS**.
  `secure:true` na zablokowanym porcie **zawiesza każdą wysyłkę** aż do timeoutu — ustaw twarde
  connection/greeting timeouts, żeby błąd był głośny.
- **Deliverability poczty to nie „wysłałem".** Zweryfikowana domena nadawcy (SPF/DKIM), realne
  wysłanie testowe, opt-in zgodny z RODO (→ [09](09-law-and-protecting-the-creator.md)). E-mail, który
  „wyszedł", a wylądował w spamie/nigdzie, to bug.
- **Sprawdź to na prodzie/stagingu providera**, nie lokalnie — lokalna sieć nie ma tych blokad (→ [03](03-testing-and-verification.md)).

## 5. Każdy płatny zasób za twardą kwotą

Endpoint wołający płatne API (LLM, geokodowanie, e-mail) bez limitu to otwarty rachunek i wektor nadużyć:

- **Kwota per użytkownik** (okno miesięczne/dobowe) z **jasnym komunikatem** i **datą resetu z góry**.
- **Różnicuj per tier** (free vs premium), egzekwuj po stronie serwera.
- **Rate-limit + nagłówki bezpieczeństwa** (helmet/limiter) jako stały element stacku (→ [08](08-stack-and-technologies.md)).
- Powiąż z prawem i regulaminem: limit i jego komunikacja to też ochrona przed abuse (→ [09](09-law-and-protecting-the-creator.md)).

## Anty-wzorce
- 🚫 **Brak globalnego łapacza błędów** — jeden zły request restartuje serwis dla wszystkich.
- 🚫 **Scraper bez checkpointów** odpalany z tła sesji — crash = run od zera, znikający runner = wieczna porażka.
- 🚫 **Zewnętrzne wywołanie bez timeoutu i backoffu** — cichy zawis albo ban po serii 429.
- 🚫 **„Wysłałem maila" ≠ dostarczyłem** — brak weryfikacji portu/domeny/dostarczalności.
- 🚫 **Płatne API bez kwoty** — niespodziewany rachunek i otwarty wektor nadużyć.
- 🚫 **Sesje w pamięci procesu** — każdy deploy wylogowuje wszystkich (→ [05](05-git-and-deployments.md)).

## Dla nowych projektów
Wpisz do Dnia 0 (→ [07](07-new-project-day-0.md)) **zanim** pojawi się pierwszy realny user:
globalny error-handler + 500 bez wycieku, timeouty i backoff na każdym zewnętrznym I/O, kwoty na
płatnych endpointach, trwały store sesji w osobnym pliku. To tańsze teraz niż jako incydent o 2 w nocy.
Każdy incydent prod → wpis w runbooku z datą i ponumerowaną lekcją (→ [05](05-git-and-deployments.md), [06](06-collaboration-and-memory.md)).
