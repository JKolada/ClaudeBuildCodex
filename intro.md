# Czym jest Rzemiosło — The Craft

> **Rzemiosło (The Craft) to sztuka stawiania aplikacji end-to-end z Claude — takich, które
> są skalowalne, utrzymywalne i łatwe do dalszego rozwoju, migracji i zmiany przez całe życie
> projektu.** Nie framework, nie biblioteka — **doktryna współpracy człowiek + agent**: zwarty
> zestaw reguł, przykazań i antywzorców, dzięki którym kod zostaje zrozumiały dla następnej sesji,
> testowalny, bezpieczny w zmianie i godny zaufania — od pierwszego commita po prod z żywymi
> użytkownikami.

## W jednym akapicie

Większość projektów budowanych z AI nie rozsypuje się dlatego, że agent nie umie pisać kodu —
rozsypuje się dlatego, że **nikt nie ustalił zasad**. The Craft to właśnie te zasady: dołączasz je
do projektu jako `docs/rules/`, a Claude od **Dnia 0** wie „jak my to robimy". Efekt to aplikacja
o **ekstremalnie elastycznej strukturze plików i technologii** — zaczynasz prosto (jeden serwer,
jedna baza), a struktura jest z góry gotowa na wzrost: rozdzielone warstwy, feature flags, migracje
forward-only, slug zamiast ID. Rozwijasz, migrujesz i skalujesz **bez przepisywania od zera**. Wszystko
z **poszanowaniem prywatności osobistej i prawa** (RODO/GDPR, zgody, ochrona twórcy) wpisanym od
początku, nie doklejonym na końcu.

## Co dostajesz

- **Kod, który czyta się jak proza** — dopasowany do otoczenia, łatwy w review przez człowieka *i* agenta.
- **Historia git jako pamięć projektu** — szukasz, zanim napiszesz; nic nie wymyślasz od nowa.
- **Weryfikację zamiast deklaracji** — „działa" znaczy dowód: smoke test, kod HTTP, liczby, screenshot.
- **Bezpieczeństwo zmian** — dry-run domyślnie, backup przed każdą migracją, prod święty, dane userów nienaruszalne.
- **Elastyczność i skalowalność** — monolit na jednym VPS jako prosty default, z jawną ścieżką wzrostu (SQLite → PostgreSQL, VPS → serverless), gdy metryka tego wymusi.
- **Spokój prawny** — regulamin, polityka prywatności i disclaimery jako zbroja twórcy, nie refleksja po fakcie.

---

# Dlaczego warto spróbować napisać aplikację z The Craft

**Bo różnica nie jest w tym, *czy* agent napisze kod — tylko w tym, *jak* będzie wyglądał Twój
projekt za trzy miesiące.** Bez zasad każda sesja z agentem dokłada trochę chaosu: niespójny styl,
dokumentacja, która kłamie, migracja bez backupu, deploy „bo gotowe". Po kwartale masz aplikację,
której boisz się dotknąć. The Craft odwraca tę trajektorię: **każda zmiana zostawia projekt
czytelniejszym, nie gorszym.**

**Zaczynasz szybko, a nie tanim kosztem.** Jeden serwer, prosty stack, monolit — coś, co ogarniasz
w głowie: jeden deploy, jeden log, jeden backup, jeden rollback. To nie jest „prymitywne" — to jest
**tanie w utrzymaniu**. A gdy naprawdę przyjdzie skala, struktura już na nią czeka: warstwy są
rozdzielone, klucze stabilne, migracje jednokierunkowe. Rozwój i migracja przestają być
przepisywaniem — stają się dokładaniem.

**Człowiek i agent grają do jednej bramki.** Plan → iteruj → review. Agent nie zgaduje — wykonuje
sprawdzony przepis, szuka w historii, raportuje uczciwie (z błędami, nie tylko z sukcesami). Ty
zostajesz architektem decyzji, nie korektorem chaosu. To współpraca, w której **zaufanie buduje się
na dowodzie**, a nie na optymizmie.

**Prywatność i prawo masz z głowy od Dnia 0.** RODO/GDPR, zgody, retencja, ochrona twórcy — wpisane
jako polityki w konstytucję projektu, zanim pojawi się pierwszy realny użytkownik. Żadnych nocnych
poprawek „bo ktoś poprosił o usunięcie konta".

**Najlepsze: to jest reużywalne.** The Craft nie jest „pod jeden projekt". Dołączasz go jako
`docs/rules/` do **każdej** nowej aplikacji, wypełniasz [brief](index.html#brief) i ruszasz — a każdy
kolejny projekt korzysta z lekcji poprzedniego.

> **Spróbuj raz.** Weź następny pomysł, dołącz The Craft, zacznij od [Dnia 0](07-nowy-projekt-checklist.md)
> i zbuduj go jak rzemieślnik — wolno tam, gdzie błąd jest drogi; szybko tam, gdzie jest tani.
> Zobaczysz różnicę nie pierwszego dnia, ale **trzeciego miesiąca** — gdy aplikacja wciąż jest
> przyjemna do rozwijania. Zacznij od [Dekalogu](00-przykazania.md): cała doktryna na jednym ekranie.
