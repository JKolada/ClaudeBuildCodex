# 16 — Prowadzenie Claude: skille, modele, autopilot, tło, agentowe workflow

> Reszta doktryny jest o **budowaniu**; ten rozdział o **dobrym prowadzeniu agenta.** Claude Code ma
> funkcje, które zmieniają koszt i tempo *każdego* zadania. Używaj ich świadomie — różnica między wolną,
> klikaną sesją a szybką siedzi głównie tutaj.

## Skille i slash-komendy

**Skill** to powtarzalna procedura wywoływana slashem (`/run`, `/run-tests`, `/add-migration`,
`/update-ai-readme`). Kodyfikuje „jak my to robimy", więc agent wykonuje **sprawdzony przepis zamiast
zgadywać** za każdym razem. Buduj własne do powtarzalnych przepływów; korzystaj też z wbudowanych.
Dyscyplina i „kiedy zbudować" → [02](02-skills-and-refactoring.md).

- **Twórz własną slash-komendę** do każdego przepływu, który powtarzasz (≥3 razy lub łatwy do pomylenia).
  Jedna jasna komenda dla agenta + fallback dla człowieka; jasny kontrakt wyjścia (0 = zielone).
- **Skill to przepis (dla agenta), nie hook** (automatyzacja wykonywana przez harness). „Zawsze rób X po Y" =
  hook w configu, nie skill.

## Dobierz model do zadania

Dopasuj model do roboty — to pokrętło koszt/jakość, nie domyślny ustawiony raz:

- **Tani/szybki model** do roboty ograniczonej i mechanicznej: zmiany nazw, proste edycje, wyszukiwanie,
  mechaniczny refaktor.
- **Mocny model** do trudnych 10%: architektura, paskudne wielo-plikowe bugi, projekt z realnym tradeoffem.
- **Przełączaj w trakcie sesji**, gdy zmienia się zadanie. Nie płać top-tierem za `git status`; nie
  oszczędzaj na migracji, która może zgubić dane. Gdy tani model się zapętla — **eskaluj**; gdy mocny
  marnuje się na rutynie — **zejdź niżej**. Mierz wynikiem, nie nawykiem.

## Autopilot — preferowany domyślny tryb

**Najlepiej działaj na autopilocie** (autonomicznie / auto-accept) przy pracy niskiego ryzyka i dobrze
zakresowanej. Jest szybciej, a Ty zostajesz **architektem decyzji, nie klikaczem potwierdzeń.**

- **Ustaw bariery raz, potem puść.** Polityki w `CLAUDE.md` (nigdy deploy/push bez „wdrażaj"; dry-run
  domyślny; prod święty) to one *czynią* autopilota bezpiecznym — agent wykonuje swobodnie *w ich ramach*
  i commituje często, zatrzymując się tylko przy tym, co nieodwracalne lub na zewnątrz (→ [06](06-collaboration-and-memory.md), Przykazanie VI).
- **Twarde bramki wciąż wymagają jawnego „tak":** deploy, swap prod-bazy, push/publikacja, destrukcyjne
  kasowanie, wszystko na zewnątrz. Autopilot ≠ brak nadzoru przy niebezpiecznych operacjach.
- **Zysk:** przeglądasz **plany i wyniki**, nie każdy klawisz. Plan → iteruj → review (→ [06](06-collaboration-and-memory.md)) na wysokości decyzji.

## Uruchamiaj długie rzeczy w tle

Długie operacje — serwery dev, buildy, suity testów, scrapery, deploye — **odpalaj w tle**, żeby sesja szła
dalej; dostaniesz powiadomienie, gdy skończą.

- **Nie blokuj rozmowy odpytywaniem długiego joba.** Wrzuć w tło, rób dalej swoje, odczytaj wynik, gdy
  przyjdzie.
- **Spinaj z wznawialnymi/checkpointowanymi jobami** (→ [14](14-operational-resilience.md), [15](15-scraping-ai-and-chatbots.md)) dla wszystkiego, co może paść w połowie — job w tle, który nie jest wznawialny, po prostu pada poza wzrokiem.

## Agentowe workflow — rozprosz, gdy się opłaca

Do pracy, która się **dekomponuje** — szerokie szukanie po wielu plikach, wielowymiarowy przegląd,
równoległe niezależne edycje, duża migracja — **odpalaj subagentów równolegle.** Zostaje Ci **wniosek**,
nie surowe zrzuty plików.

- **Wzorce:** równolegli czytelnicy → synteza; znajdź → **adwersarialnie zweryfikuj** każde znalezisko;
  migruj plik-po-pliku w izolacji; pętla-aż-do-sucha dla odkrywania o nieznanym rozmiarze.
- **Deterministyczny workflow** (orkiestrowani subagenci: fan-out → weryfikacja → synteza) do dużych,
  ustrukturyzowanych przebiegów, gdzie kontrola przepływu ma być kodem, nie zgadywaniem modelu. **Jeden
  agent** do skupionego wyszukania.
- **Świadomy kosztu:** fan-out pali tokeny. Sięgaj po niego, gdy szerokość, równoległość albo niezależna
  weryfikacja realnie pomaga — nie do poprawki na jedną linię.

## Anty-wzorce
- 🚫 **Top-tier do `git status`; tani model do migracji gubiącej dane.** Złe pokrętło w obie strony.
- 🚫 **Ręczne potwierdzanie każdej bezpiecznej edycji** zamiast autopilota w ustawionych barierach — wolno i uczy przyklepywania.
- 🚫 **Blokowanie sesji** długim jobem, który mógł iść w tle.
- 🚫 **Jeden szeregowy agent do pracy idealnie równoległej** — albo workflow na 12 agentów do trywialnej zmiany.
- 🚫 **Własny skill na coś robionego raz** — to tylko narzut (→ [02](02-skills-and-refactoring.md)).

## Dla nowych projektów
Ustaw bariery w `CLAUDE.md` **najpierw** (żeby autopilot był bezpieczny), dodaj wcześnie powtarzalne skille
(`/run`, `/run-tests`), domyślnie graj **autopilot + tło** na mielenie, przełączaj modele wg zadania, a po
**agentowe workflow** sięgaj przy dużych przebiegach. → [02](02-skills-and-refactoring.md), [07](07-new-project-day-0.md)
