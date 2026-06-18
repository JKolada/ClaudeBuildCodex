# 07 — Nowy projekt: Dzień 0

Konkretna checklista, którą Claude wykonuje (z Kubą) **rozpoczynając nowy projekt**.
Cel: po Dniu 0 każda kolejna sesja ma grunt pod nogami.

## 0. Brief produktowy — dopytaj, zanim cokolwiek powstanie

Przed pierwszą linią kodu i przed `CLAUDE.md` **zadaj użytkownikowi zestaw pytań** — i nie zgaduj
domyślnych odpowiedzi tam, gdzie zmieniają architekturę, prawo lub markę. Te decyzje są tańsze na
papierze niż w kodzie (i18n dorzucony później to przepisywanie, monetyzacja po fakcie to migracja
danych). Pytaj zwięźle, grupami; jeśli czegoś user nie wie — zaproponuj domyślną i zaznacz ją jako
założenie. Te same pytania zadaj **aplikując doktrynę do istniejącego projektu** — wtedy jako audyt
(„co już jest, czego brak").

- **Języki docelowe i rynki.** Jeden język czy wiele? Które, w jakiej kolejności, który jest
  źródłem prawdy? Parytet treści jako wymóg? RTL? Waluty/strefy/format dat? → decyduje o i18n od
  Dnia 0 i strukturze danych ([10](10-seo-i-tlumaczenia.md), [11](11-model-danych-normalizacja.md)).
- **Funkcjonalności — rdzeń vs „później".** Co jest MVP (bez czego produkt nie istnieje), a co
  jest miłe-do-mienia? Konta i role? Treść statyczna czy user-generated? Integracje zewnętrzne
  (płatności, mapy, AI, e-mail)? → wyznacza warstwy i feature flags ([12](12-elastycznosc-i-skalowalnosc.md)).
- **Monetyzacja.** Darmowe, płatne, freemium, subskrypcja, jednorazowo, reklamy, afiliacja? Kiedy
  pojawia się płatność (Dzień 1 czy po trakcji)? Dostawca (Stripe/inny), faktury, VAT/OSS? →
  dotyka modelu danych i obowiązków prawnych ([09](09-prawo-i-ochrona-tworcy.md), [11](11-model-danych-normalizacja.md)).
- **Styl UX i kierunek wizualny.** Grupa docelowa i ton (poważny B2B ↔ zabawowy konsumencki)?
  Jest marka (paleta, typografia, logo) czy tworzymy od zera? Gęsty dashboard czy przewiewny
  landing? Tryb jasny/ciemny? Dostępność (WCAG) jako wymóg?
- **Animacje i „odczucie" interfejsu.** Statyczny i szybki, czy bogaty w mikrointerakcje
  i przejścia? Budżet wydajności i `prefers-reduced-motion` jako zasada? → animacja nie może bić
  się z Core Web Vitals ([13](13-wydajnosc-frontend-i-sql.md)).
- **Wydźwięk marketingowy.** Jedno zdanie wartości (value prop), kto jest klientem, czego unikamy
  w tonie? Nazwa/domena/hasło ustalone? To samo „dlaczego", które potem napędza changelog
  i copy pisane językiem użytkownika ([08](08-stack-i-technologie.md) → [01](01-dokumentacja-i-ai-readme.md)).

> **Zapisz odpowiedzi**, nie tylko je usłysz: twarde decyzje → `CLAUDE.md` (polityki) i `memory/`
> (cel biznesowy, ograniczenia — krok 10). Założenia przyjęte za usera oznacz wyraźnie, by dało
> się je później zweryfikować.

### Anty-wzorce
- 🚫 **Skok do kodu bez briefu** — „zacznę, dopytam po drodze". Język, monetyzacja i marka
  wpisane po fakcie to przepisywanie, nie poprawka.
- 🚫 **Zasypanie pytaniami** — 30 pytań naraz zniechęca. Pytaj grupami, o to co zmienia plan;
  resztę zaproponuj jako domyślne.
- 🚫 **Ciche założenia** — przyjęcie „pewnie tylko polski" albo „pewnie za darmo" bez zaznaczenia,
  że to Twoje założenie, nie decyzja użytkownika.

## 1. Rozpoznanie (zanim cokolwiek napiszesz — Przykazanie II)
- [ ] Przeczytaj istniejący `CLAUDE.md` / `AI_README.md` / `README`, jeśli są.
- [ ] `git log --oneline -20`, `git status` — co już jest, co w toku, czy są sieroty/śmieci.
- [ ] Zidentyfikuj stack, sposób uruchomienia, gdzie żyją dane.
- [ ] Wypisz, czego **jeszcze nie wiesz** — i dopytaj tylko o to, co zmienia plan.

## 2. Konstytucja projektu — `CLAUDE.md`
- [ ] Quick orientation (warstwa → tech → lokalizacja).
- [ ] Dokładne komendy uruchomienia (interpreter, port, env).
- [ ] **Polityki nadrzędne**: „nigdy nie deployuj automatycznie", privacy/compliance, git workflow.
- [ ] Sekcja „Current state" z datą i liczbami.

## 3. Higiena repo
- [ ] `.gitignore`: zależności, lokalne bazy, backupy (`*.bak`), assety generowane, temp, scratch.
      (Pamiętaj: `#` komentarz w osobnej linii.)
- [ ] Konwencja commitów + tagowania deployów.
- [ ] Task tracking (Issues / `docs/plans/`) — gdzie żyją zadania.

## 4. Dokumentacja per katalog
- [ ] `AI_README.md` w każdym istotnym katalogu (choćby szkielet).
- [ ] `docs/` na stabilną referencję (architektura, schemat danych) i plany.

## 5. Skille (automatyzacja powtarzalnego)
- [ ] `/run-<projekt>` — uruchom + smoke test (N tras, markery, exit code).
- [ ] `/run-tests` — pełny suite (unit + integration + e2e).
- [ ] `/update-ai-readme` — sync docsów przed commitem.
- [ ] `/add-migration` — jeśli relacyjna baza (numer → SQL → apply → AI_README → commit).

## 6. Testy i weryfikacja
- [ ] Szkielet unit + integration; smoke test z markerami.
- [ ] (Jeśli UI) Playwright na osobnym porcie.
- [ ] Zasada: testy ścieżki krytycznej przed commitem; „weryfikuj, nie deklaruj".

## 7. Bazy i skrypty
- [ ] Migracje forward-only + katalog `backups/` + retencja.
- [ ] Każdy skrypt mutujący: `--dry-run` domyślnie, `--execute` świadomie, idempotentny.
- [ ] **Nightly backup** od momentu pierwszych prawdziwych userów.

## 8. Produkcja (przygotuj, nie odpalaj)
- [ ] Runbook deployu (code-only vs okno maintenance) — spisz, zanim będzie potrzebny.
- [ ] Branded maintenance page + flaga (np. nginx `/tmp/<app>_maintenance`).
- [ ] Plan rollbacku: tag kodu + backup bazy.
- [ ] Publiczny changelog „Co nowego" (pinned), pisany językiem użytkownika.

## 9. Compliance / prywatność (jeśli dotyczy danych ludzi)
- [ ] Polityka prywatności + zgody, anonimizacja, retencja — **jako reguła w konstytucji**.
- [ ] Disclaimery (np. „dla pełnoletnich", „nie świadczymy usług terapeutycznych").
- [ ] i18n od początku, jeśli produkt globalny.

## 10. Pamięć
- [ ] Zapisz w `memory/`: kim jest user, cel biznesowy, twarde ograniczenia projektu
      (to, czego nie ma w kodzie).

---

> **Minimalny Dzień 0**, gdy nie ma czasu na wszystko: krótki **brief** (krok 0: język, MVP,
> monetyzacja, ton) → `CLAUDE.md` (stack + jak uruchomić +
> polityki) → `.gitignore` → jeden skill `/run-<projekt>` ze smoke testem → szkielet testów →
> katalog `backups/`. Reszta dorasta z projektem.
