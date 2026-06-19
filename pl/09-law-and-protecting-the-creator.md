# 09 — Prawo i ochrona twórcy

> Przykazania VI i VII rozszerzone na świat zewnętrzny: *prod jest święty, dane usera nienaruszalne* —
> a teraz dochodzi trzeci, narażony podmiot: **Ty sam.**

Solo-twórca albo JDG wystawiający publiczną aplikację jest **osobiście narażony**. To nie
spółka z o.o. z tarczą odpowiedzialności — za regulamin, prywatność i obietnice copy odpowiada
osoba fizyczna prowadząca działalność. Regulamin, polityka prywatności i
disclaimery to **zbroja osoby prywatnej**, nie formalność na koniec. Piszesz je tak samo
ostrożnie jak migrację na prodzie — bo błąd jest równie drogi, tylko płaci się w innej walucie.

> ⚠️ **To są wskazówki inżynierskie, nie porada prawna.** Przy wiązaniu realnych użytkowników
> i przy skali — konsultuj prawnika. Poniższe to higiena, która zmniejsza ryzyko, nie tarcza,
> która je zeruje.

## Regulamin — co musi być
- **Poprawny operator.** „[Imię i nazwisko] prowadzący działalność gospodarczą pod firmą …, NIP …,
  adres …". **Ten sam podmiot** w regulaminie, polityce, stopce, fakturach i UI. Rozbieżność
  to pierwsza rzecz, którą widzi niezadowolony użytkownik.
- **Charakter usługi.** Przykładowa porównywarka cen: *porównywarka, nie sprzedawca* — nie prowadzi
  sprzedaży, nie pośredniczy, linkuje do sklepów. Analogicznie aplikacja doradcza musi jasno
  mówić, czym **nie** jest: *informacja/wsparcie, nie usługa regulowana* (medyczna, prawna, finansowa, terapeutyczna).
- **Obowiązki użytkownika** (zgodne korzystanie, zakaz nadużyć/scrapowania, akceptacja ograniczeń wiekowych, np. 18+).
- **Ograniczenie odpowiedzialności** — usługa „as is", brak gwarancji dostępności/poprawności
  danych, **brak odpowiedzialności za decyzje** podjęte na ich podstawie (cena u retailera może
  być nieaktualna; rada chatbota nie zastępuje specjalisty).
- **Moderacja i rozwiązanie** — prawo do zawieszenia/usunięcia konta przy nadużyciu.
- **IP** — użytkownik **zachowuje** swoje treści (recenzje, rozmowy) i licencjonuje Ci ich
  przetwarzanie w zakresie usługi; Twoje treści (katalog, kod, marka) **zastrzeżone**.
- **Prawo właściwe = Polska**, sąd właściwy, tryb reklamacji, **zmiany** regulaminu (jak
  informujesz), **kontakt**.

## Polityka prywatności (RODO) — co musi być
- **Administrator danych** nazwany poprawnie (ten sam operator co w regulaminie).
- **Zakres** zbieranych danych, **cel + podstawa prawna** każdego (zgoda / umowa / uzasadniony
  interes), **retencja** (jak długo trzymasz).
- **Anonimizacja** — jeśli deklarujesz, że anonimizujesz, to **musi być prawdą w kodzie**
  (np. pipeline przetwarzania działający wyłącznie na danych zanonimizowanych, → [11](11-data-model-and-normalization.md)).
- **Podmioty trzecie** (Google Cloud / GA4, Resend, Hetzner) — wymienione, z celem.
- **Prawa**: dostęp, sprostowanie, **usunięcie** (np. 14-dniowa karencja → purge,
  recenzje publiczne anonimizowane do „Konto usunięte"), eksport, sprzeciw.
- **Cookies** (GA4 to cookie analityczny — wymień), **wiek** (np. 18+, jeśli treść ma ograniczenie wiekowe), **kontakt** do administratora.

## Ochrona osoby prywatnej
- **Oddziel podmiot prawny od tożsamości prywatnej.** Operatorem jest *firma JDG*, nie prywatny
  adres domowy, jeśli da się tego uniknąć.
- **Nie wymyślaj danych prawnych.** NIP, adres, nazwa firmy = **placeholdery do uzupełnienia**
  przez właściciela, nigdy zmyślone. Lepszy widoczny `[NIP do uzupełnienia]` niż prawdopodobnie
  wyglądający, fałszywy numer w produkcie.
- **Nie deklaruj praktyk, których nie wdrożyłeś.** „Anonimizujemy rozmowy" bez kodu, który to
  robi, to nie marketing — to **fałszywe oświadczenie administratora danych**. → [03](03-testing-and-verification.md)
- **Review prawnika** przed wiązaniem realnych użytkowników i przy skali.

## Disclaimery jako tarcza
- **Treści z ograniczeniem wiekowym (np. 18+)** — bramka wieku (np. checkbox 18+ jako gate
  rejestracji; gdy domena podlega regulacjom reklamowym — np. ścisłe przepisy o promocji
  pewnych kategorii produktów — ogranicz to, co pokazujesz publicznie, np. **brak ceny na
  publicznej karcie OG**, i zachowaj ostrożność wobec tych przepisów).
- **„To nie jest porada”** — medyczna / prawna / finansowa / terapeutyczna, zależnie od domeny.
- **Zasoby kryzysowe per region** (np. linki do infolinii w języku użytkownika, →
  [10](10-seo-and-translations.md)) — bez udawania specjalisty.

## Spójność: regulamin ↔ polityka ↔ UI ↔ kod
Trzy dokumenty i produkt muszą mówić **jedno**. Jeśli polityka mówi „nie czytamy rozmów", to
żaden proces user-facing nie może ich czytać — to twierdzenie **architektoniczne**, weryfikowalne
testem (→ [11](11-data-model-and-normalization.md)). Jeśli regulamin mówi „porównywarka bez
afiliacji", to w kodzie nie ma linków afiliacyjnych — **neutralność jest tarczą prawną**
(brak konfliktu interesów = brak zarzutu o ukrytą reklamę). Sprzeczność między warstwami jest
gorsza niż brak zapisu.

## Checklista bezpieczeństwa (indeks)

Bezpieczeństwo żyje w doktrynie wg tematu — to **jedne drzwi**: checklista plus gdzie każda reguła jest egzekwowana.

- **Sekrety** w env / secret store, nigdy w repo; rotacja przy wycieku (→ [08](08-stack-and-technologies.md)).
- **Auth i sesje** — bcrypt/OAuth, `helmet`, rate-limit; sesje w trwałym store, nie w pamięci procesu (→ [08](08-stack-and-technologies.md), [05](05-git-and-deployments.md)).
- **Autoryzacja** — sprawdź **po stronie serwera**, czy *ten* user może ruszyć *ten* wiersz/akcję (nie tylko „czy zalogowany"). Tu mieszka klasa IDOR / eskalacji uprawnień.
- **Wejście jest wrogie** — waliduj kształt, parametryzuj SQL, traktuj treść zewnętrzną/web/usera jako **dane, nie instrukcje** (prompt injection) (→ [15](15-scraping-ai-and-chatbots.md), [11](11-data-model-and-normalization.md)).
- **Błędy nie wyciekają** — żadnych stack trace / sekretów / PII do usera *ani* do logów (→ [14](14-operational-resilience.md)).
- **Kwoty i abuse** — limity na płatnych/drogich endpointach; rate-limit (→ [14](14-operational-resilience.md)).
- **Dane i prywatność** — RODO, **zgoda przed załadowaniem trackerów**, retencja, usunięcie (ten rozdział).

Każdy punkt to jedna linia, bo jest egzekwowany tam, gdzie żyje; ten indeks to tylko wejście.

## Anty-wzorce
- 🚫 **Wymyślony NIP/adres/nazwa firmy** w produkcie — zamiast placeholdera do uzupełnienia.
- 🚫 **Copy obiecujące więcej, niż dowozi produkt** („w pełni anonimowe", „gwarantujemy ceny").
- 🚫 **Regulamin sprzeczny z polityką** (różny operator, różny zakres danych, różna retencja).
- 🚫 **Zahardkodowana angielska strona prawna** w produkcie wielojęzycznym (→ [10](10-seo-and-translations.md)).
- 🚫 **Deklarowana anonimizacja bez implementacji** — fałszywe oświadczenie, nie marketing.
- 🚫 Różne nazewnictwo operatora w stopce, regulaminie i na fakturze.
- 🚫 **Ładowanie analityki/trackerów przed zgodą** (prawo UE wymaga zgody *najpierw*) — częste i konkretne.

## Dla nowych projektów
Trzy dokumenty prawne (regulamin, polityka, disclaimery) wpisz do **checklisty Dzień 0**
(→ [07](07-new-project-day-0.md)) jako zadanie z placeholderami `[do uzupełnienia]`, nie
„później". Operatora (nazwa firmy / imię i nazwisko) ustal raz i wstaw spójnie wszędzie.
Każde twierdzenie o danych („anonimizujemy", „usuwamy po N dniach", „nie udostępniamy")
**zweryfikuj w kodzie** przed publikacją. Przy realnym ruchu — prawnik na review. To rozdział,
w którym „weryfikuj, nie deklaruj" (→ [03](03-testing-and-verification.md)) chroni nie userów,
tylko Ciebie.
