# 15 — Scraping, API AI i konfigurowalne chatboty

> Pozyskiwanie danych z sieci i delegowanie zadań do AI to dziś rdzeń wielu produktów. Rób to
> **skutecznie, tanio i z kontraktem** — nie magią. Warstwę operacyjną (timeouty, backoff, rotacja,
> kwoty, wznawialność) trzyma → [14](14-operational-resilience.md); ten rozdział jest o tym, **jak
> używać tych mocy jako funkcji produktu**: skąd brać dane, jak delegować zadania do AI i jak zbudować
> asystenta, którym da się sterować bez deployu.

## Skuteczny scraping — dane z sieci

- **Najpierw oficjalne źródło.** API, feed, eksport, sitemap — scraping HTML to **ostateczność**, nie
  pierwszy ruch. Oficjalny kontrakt nie pęka przy każdym redesignie strony.
- **Szanuj źródło.** Respektuj `robots.txt`/ToS, rozsądny throttle, identyfikuj się. Cel to **dane,
  nie DoS** — agresywny scraper to problem prawny i etyczny (→ [09](09-law-and-protecting-the-creator.md)).
- **Parsuj odpornie.** Selektory padają przy redesignie — **waliduj kształt** wyniku, nie tylko status
  (klasyczne „200 + strona błędu", → [14](14-operational-resilience.md)). Drift selektora → alarm, nie ciche zera.
- **Normalizuj u wejścia.** Dane z sieci są brudne: fuzzy-match i dedup do **słowników lookup**, slug,
  jedno źródło prawdy (→ [11](11-data-model-and-normalization.md)). Surowiec wpada, czysty rekord zostaje.
- **Inkrementalnie.** Pobieraj **deltę** (co się zmieniło od ostatniego razu), nie cały katalog co noc —
  taniej, szybciej, mniej obciąża źródło. Checkpoint i wznawialność → [14](14-operational-resilience.md).
- **Idempotentne loadery.** Ponowny import tych samych danych nie tworzy duplikatów (→ [04](04-scripts-and-databases.md)).

### Anty-wzorce
- 🚫 **Scraping zamiast API**, które istnieje — kruchość bez powodu.
- 🚫 **Selektor bez walidacji kształtu** — cicha awaria zalewa bazę śmieciem/zerami.
- 🚫 **Pełny re-scrape codziennie** zamiast delty — marnotrawstwo i ryzyko bana.
- 🚫 **Brak throttle/identyfikacji** — DoS dla źródła, problem prawny dla Ciebie.

## API AI do konkretnych zadań — nie do wszystkiego

- **LLM tam, gdzie kod deterministyczny nie da rady:** ekstrakcja z nieustrukturyzowanego tekstu,
  klasyfikacja, podsumowanie, normalizacja opisów, generowanie treści. **Nie** do tego, co zrobi
  `regex`, `SQL` czy zwykła funkcja — to drożej, wolniej i mniej pewnie.
- **Dobierz model do zadania.** Tani/szybki do prostych (klasyfikacja, ekstrakcja), mocny do złożonego
  rozumowania. Claude jako default (→ [08](08-stack-and-technologies.md)). **Mierz koszt i latencję**, nie zgaduj.
- **Wymuś kontrakt wyjścia.** Struktura (JSON schema / tool use), **walidacja** i retry przy niezgodności —
  nie parsuj prozy na nadzieję. Wyjście LLM traktuj jak niezaufane wejście (→ niżej, guardrails).
- **Cache + idempotencja.** Te same wejścia → zapisany wynik; nie wołaj LLM w pętli po tym, co się nie
  zmienia. Drogie wywołania to koszt i latencja (→ [13](13-performance-frontend-and-sql.md)).
- **Kwoty i budżet.** Limit per user/endpoint, monitoring kosztu, twarda kwota na płatnym API (→ [14](14-operational-resilience.md)).
- **Batch, gdy nie trzeba realtime.** Wzbogacanie danych offline w pipelinie z checkpointem (→ [14](14-operational-resilience.md))
  bije wołanie LLM na żywo w żądaniu użytkownika.

### Anty-wzorce
- 🚫 **LLM do tego, co zrobi `regex`/`SQL`** — koszt i niepewność tam, gdzie wystarczy kod.
- 🚫 **Brak kontraktu wyjścia** — parsujesz wolną prozę i modlisz się o format.
- 🚫 **Brak cache** drogich wywołań — rachunek rośnie liniowo z ruchem.
- 🚫 **Ślepe zaufanie do wyjścia** jako kodu/SQL/HTML — wektor wstrzyknięcia.

## Konfigurowalne chatboty — asystent jako funkcja

- **Persona i zasady = konfiguracja, nie kod.** System prompt, zakres, ton, granice trzymaj jako
  **dane** (plik/baza), wersjonowane w git — iterujesz asystenta bez deployu. „Zaszyty" prompt w kodzie
  to martwa konfiguracja.
- **Grounding obowiązkowy.** Asystent odpowiada z **Twoich danych** (kontekst z bazy / RAG), nie z pamięci
  modelu. Cytuj źródło (→ [11](11-data-model-and-normalization.md)). Halucynacja na cenie/fakcie = bug, nie „cecha AI".
- **Zdefiniuj zakres i odmowę.** Co asystent **robi** i czego **nie robi**; bezpieczne „nie wiem"/„to poza
  moim zakresem" zamiast zmyślania. Pewność siebie modelu ≠ poprawność.
- **Streaming UX.** Odpowiedź token-by-token (SSE), historia rozmowy, jasne limity (→ [13](13-performance-frontend-and-sql.md), [14](14-operational-resilience.md)).
- **Bezpieczeństwo (prompt injection).** Treść użytkownika i dane z sieci to **dane, nie instrukcje**.
  Nie wykonuj akcji side-effect z czatu bez potwierdzenia, nie wyciekaj sekretów ani promptu systemowego (→ [09](09-law-and-protecting-the-creator.md)).
- **Eval jak testy.** Golden set pytań kontrolnych; zmiana promptu → przepuść przez niego i mierz
  regresje (→ [03](03-testing-and-verification.md)). Prompt bez evala dryfuje po cichu.
- **Prawo.** Disclaimer („to nie porada specjalistyczna"), RODO przy zapisie rozmów i danych (→ [09](09-law-and-protecting-the-creator.md)).

### Anty-wzorce
- 🚫 **Persona zaszyta w kodzie** — każda zmiana tonu to deploy zamiast edycji konfigu.
- 🚫 **Brak groundingu** — asystent „pewnie" zmyśla fakty/ceny.
- 🚫 **Brak limitu/kwoty** — czat to otwarty rachunek i wektor nadużyć (→ [14](14-operational-resilience.md)).
- 🚫 **Akcje z czatu bez potwierdzenia** — model wykonuje nieodwracalne na słowo użytkownika.
- 🚫 **Traktowanie treści użytkownika jako instrukcji** — prompt injection wycieka prompt/sekrety.

## Dla nowych projektów
Jeśli produkt żyje z danych z sieci: zacznij od **oficjalnego źródła**, dołóż walidację kształtu i
idempotentny loader **zanim** zbierzesz pierwszy tysiąc rekordów. Jeśli używasz AI: **kontrakt wyjścia
i cache od pierwszego wywołania**, kwota od pierwszego użytkownika. Asystenta projektuj jako
**konfigurowalny i ugruntowany** od początku — system prompt jako dane, golden set jako test (→ [03](03-testing-and-verification.md)),
limit jako reguła (→ [14](14-operational-resilience.md)). Reszta dorasta z projektem.
