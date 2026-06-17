# 10 — SEO i tłumaczenia

> Przykazanie III rozszerzone na widoczność: *weryfikuj, nie deklaruj* — także to, że strona
> jest indeksowalna, kompletna we wszystkich językach i mierzona, a nie „chyba wygląda OK".

Aplikacja, której nikt nie znajdzie, nie istnieje. SEO i i18n to nie warstwa marketingu doklejana
na końcu — to **kontrakt z wyszukiwarką i z użytkownikiem**, że strona jest zrozumiała dla
crawlera i kompletna w jego języku. Tak jak AI_README jest interfejsem dla agenta, tak metadane
i tłumaczenia są interfejsem dla świata.

## Fundamenty SEO (każda strona)
- **`<title>` + `meta description`** unikalne per strona (nie jeden globalny).
- **Canonical** — jeden URL prawdy dla każdej treści (chroni przed duplikatami z parametrów).
- **hreflang** — przy wielojęzyczności obowiązkowe: każda wersja językowa wskazuje pozostałe
  (EchoInsight: 16 języków → 16 wzajemnych `hreflang` + `x-default`).
- **JSON-LD** — `Organization` (home), `Article` (blog/wpisy), `ItemList` (rankingi).
- **`sitemap.xml`** (z priorytetami) + **`robots.txt`** (co indeksować, gdzie sitemap).
- **Semantyczne nagłówki** (jedno `h1`, hierarchia `h2/h3`), **OG/Twitter cards** (WhiskyPolska:
  karty OG share — ale **bez ceny na publicznej karcie**, → [09](09-prawo-i-ochrona-tworcy.md)).
- **Czyste slugi** (`/ranking/whisky-do-200-zl`, nie `?id=42`) i **linkowanie wewnętrzne**
  (nav-drawer + footer + linki kontekstowe między stronami).

## Programmatic i editorial SEO
- **Programmatic** — kuratorskie landing pages pod **zapytania transakcyjne**. WhiskyPolska:
  7 stron `/ranking/:slug` („whisky do 100/200/300 zł", „najlepsza torfowa", „bourbon na prezent")
  — każda to **ręcznie pisany wstęp** PL/EN + ponumerowana **TOP-N** + pełna filtrowalna tabela +
  `ItemList` JSON-LD. **Guardy jakości** są częścią SEO: tylko 700 ml, `requireRating`,
  `minShops` — żeby strona nie była cienką wydmuszką.
- **Editorial** — huby treści/blog pod **zapytania informacyjne** (artykuły EchoInsight o rozwoju,
  poradniki WhiskyPolska). Treść, która **realnie odpowiada** na pytanie, nie keyword-stuffing.

## E-E-A-T i YMYL
Google ocenia rygorystycznie strony **YMYL** (Your Money or Your Life) — zdrowie, finanse,
religia, bezpieczeństwo. EchoInsight (wsparcie duchowe) i WhiskyPolska (alkohol, wydatki) oba w
to wpadają. Liczy się **E-E-A-T**: Experience, Expertise, Authoritativeness, Trust.
- Rzetelność i **źródła** (skąd cena, skąd ocena — WhiskyPolska linkuje WhiskyBase/sklep).
- **Autorstwo** i operator jasno nazwany (→ [09](09-prawo-i-ochrona-tworcy.md)) budują Trust.
- **Zero porad medycznych** w EchoInsight — disclaimer + ścieżka kryzysowa, nie diagnoza.

## Core Web Vitals jako czynnik rankingowy
Szybkość to nie tylko UX — to sygnał rankingowy. LCP/CLS/INP wpadają do oceny strony. Mierz i
popraw (→ [13](13-wydajnosc-frontend-i-sql.md)); nie „wydaje się szybko", tylko liczby.

## Tłumaczenia / i18n
- **Kompletność = test, który pada.** Brakujący klucz albo strona w którymkolwiek języku → test
  failuje (jak na jakub.solutions: **parytet EN↔PL** + martwe linki). Żaden język „w połowie".
- **hreflang** spina wersje (patrz wyżej).
- **Ciepły rejestr w KAŻDYM języku** — to nie dosłowność, to ton. Tłumaczenie poprawne
  gramatycznie, ale zimne, jest błędem (EchoInsight: „jesteśmy tu, żeby pomóc" musi brzmieć
  ciepło po arabsku tak samo jak po polsku).
- **MT + review człowieka dla treści wrażliwych** — Gemini tłumaczy szkielet, człowiek
  przegląda disclaimery, komunikaty kryzysowe, prawne (→ [09](09-prawo-i-ochrona-tworcy.md)).
- **RTL** (arabski) — layout musi się odbić, nie tylko tekst.
- **GA4 + Search Console** (zanonimizowane) — *które zapytania konwertują*, w którym języku
  ruch rośnie. Dane sterują tym, gdzie pisać następny landing.

## Anty-wzorce
- 🚫 **SEO-spam** / keyword-stuffing — Google to karze, nie nagradza.
- 🚫 **Cienkie strony programmatic** bez wartości (TOP-N bez guardów jakości, 2-sklepowe wydmuszki).
- 🚫 **Brak hreflang** w aplikacji wielojęzycznej → wyszukiwarka serwuje zły język.
- 🚫 **Zimne / błędne MT** w produkcie wrażliwym bez review człowieka.
- 🚫 **Angielskie UI lub strony prawne** w aplikacji 16-językowej (→ [09](09-prawo-i-ochrona-tworcy.md)).
- 🚫 **Ignorowanie Core Web Vitals** — wolna strona traci ranking i użytkownika (→ [13](13-wydajnosc-frontend-i-sql.md)).

## Dla EchoInsight
i18n od pierwszego dnia (16 języków, next-intl): hreflang dla każdej pary, **test parytetu**
jako bramka CI, RTL dla arabskiego, ciepły rejestr w każdym języku. Treści YMYL (wsparcie
duchowe) — zero porad medycznych, jasne autorstwo (operator Jakub.Solutions), zasoby kryzysowe
per region. Search Console od startu, żeby wiedzieć, **które języki i tematy** ciągną ruch. →
[08](08-echoinsight.md)
