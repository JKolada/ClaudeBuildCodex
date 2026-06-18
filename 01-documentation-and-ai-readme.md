# 01 — Dokumentacja i AI_README

> Przykazanie I: *Dokumentuj dla agenta, nie dla archiwum.*

Dokumentacja w projekcie z agentem AI ma jeden nadrzędny cel: **żeby następna sesja (albo
inny agent) zrozumiała katalog bez czytania całego kodu.** To nie jest archiwum dla potomnych
— to interfejs onboardingu, czytany co sesję.

## Trzy warstwy dokumentacji

| Warstwa | Plik | Rola |
|---------|------|------|
| **Konstytucja** | `CLAUDE.md` (root) | Źródło prawdy o projekcie: stack, jak uruchomić, polityki (np. „nigdy nie deployuj automatycznie"), aktualny stan. Ładowane co sesję. |
| **Mapa katalogu** | `AI_README.md` (w każdym istotnym katalogu) | Co tu jest, API modułów, gotchas, liczby. Czytasz **przed** dotknięciem kodu w tym katalogu. |
| **Encyklopedia / plany** | `docs/` | Stabilna referencja (architektura, schemat DB), plany na przyszłość, standardy. |

### `CLAUDE.md` — konstytucja
- Krótkie „Quick orientation" (tabela: warstwa → tech → lokalizacja).
- **Jak uruchomić** każdy element (dokładne komendy z interpreterem/portem).
- **Polityki, które nadpisują domyślne zachowanie** — najważniejsze: deployment policy
  („nigdy automatycznie na prod"), git workflow, zasady scraperów/walidacji.
- Sekcja **„Current state"** z datą i liczbami (ile rekordów, jakie migracje zastosowane).
  To jest pierwsze, co czyta agent — musi być aktualne.
- **Reguła:** instrukcje w `CLAUDE.md` mają pierwszeństwo przed domyślnym zachowaniem agenta.
  Pisz je jak prawo: konkretnie, z „dlaczego".

### `AI_README.md` — w każdym katalogu
Reguła z projektu referencyjnego, którą warto przenieść: **każdy katalog ma `AI_README.md`**, a jego
aktualizacja jest częścią workflow commita:

```
kod  →  /update-ai-readme  →  git commit
```

Co powinno być w `AI_README.md`:
- **Indeks plików/modułów** z jednozdaniowym „po co to".
- **API** kluczowych funkcji (sygnatura + kontrakt), żeby nie czytać implementacji.
- **Gotchas** — pułapki, których nie widać z kodu (np. „FB nie renderuje WebP jako og:image",
  „ten CDN zwraca 200 z HTML przy błędzie").
- **Liczby** — ile rekordów, ile testów, jakie pokrycie. Liczby się starzeją → aktualizuj.
- **Martwe wpisy usuwaj** — odniesienie do skasowanego kodu jest gorsze niż brak wpisu.

> **Test jakości AI_README:** czy agent po jego przeczytaniu może bezpiecznie zmienić kod w
> tym katalogu, nie skanując wszystkich plików? Jeśli nie — czegoś brakuje.

**Reguła wiążąca warstwy:** `CLAUDE.md` (root) **wskazuje na `AI_README.md` w każdym folderze**
jako obowiązkowe uzupełnienie — to konstytucja deleguje szczegóły katalogu do jego mapy. Konstytucja
mówi „gdzie i czym jest projekt"; `AI_README` mówi „co dokładnie jest w tym katalogu". Bez tego
wskazania nowa sesja nie wie, że mapy istnieją.

## AI_README pod grep — oszczędność kontekstu

W docelowym projekcie agent **nie czyta wszystkiego** — przy konkretnym zadaniu **grepuje po słowach
kluczowych** i czyta tylko trafiony plik. Dlatego `AI_README.md` projektuj jako **indeks pod grep**,
nie jako prozę:

- **Opis każdego pliku gęsty w keywordy.** Nie „różne reguły", lecz konkretne terminy, których ktoś
  poszuka: nazwy funkcji, pojęcia, technologie, **synonimy** i **oba języki**, jeśli projekt jest
  dwujęzyczny (`RODO`/`GDPR`, `migracja`/`migration`, `kolejka`/`queue`). `grep -i <temat>` ma trafić
  w **jedną linię** i wskazać właściwy plik.
- **Jeden plik = jeden temat.** Dziel treść tak, by trafienie było precyzyjne. Temat rozlany na pięć
  plików = pięć trafień i przepalony kontekst; temat zwarty w jednym = jedno trafienie, jedno czytanie
  (→ [12](12-flexibility-and-scalability.md): rozdziel warstwy).
- **Mapa „temat → plik".** Trzymaj w `AI_README` zwięzły indeks (keywordy + nazwa pliku w jednej linii),
  utrzymywany aktualnie. To nawigacja: grep po nim zwraca *gdzie iść*, nie całą treść.
- **Po co:** kontekst to budżet. Im celniej `AI_README` kieruje, tym mniej tokenów schodzi na szukanie,
  a więcej zostaje na robotę. To Przykazanie II (szukaj, zanim napiszesz) zastosowane do **czytania**.

## Struktura `/docs` i foldery

Dokumentacja „cięższa niż mapa katalogu" mieszka w **`/docs`** — jedno miejsce na stabilną
referencję i plany, żeby nie puchły `AI_README` ani `CLAUDE.md`:

```
docs/
  AI_README.md          # spis treści docs: „gdzie zacząć dla zadania X"
  architecture.md       # warstwy, granice, przepływy
  data_model.md         # schemat DB, ERD, controlled vocabulary (→ [11])
  deployment_runbook.md # procedura + ponumerowane lekcje z incydentów (→ [05], [14])
  plans/                # plany na przyszłość, RFC, decyzje (jeden plik = jeden temat)
    NNNN-tytul.md
```

- **`/docs/plans/`** — żywy backlog decyzji i projektów. Plan to dokument, nie myśl w głowie:
  problem → opcje → wybór → „dlaczego". Zrealizowany plan zostaje jako zapis decyzji.
- **Folder bez `AI_README.md` to folder-zagadka.** Tworząc nowy istotny katalog — twórz go **razem**
  z `AI_README.md` (choćby szkielet). To samo przy refaktorze: rozbijasz moduł na podkatalogi →
  każdy nowy katalog dostaje mapę w tym samym kroku, nie „później".
- **Im konkretniej, tym lepiej.** Lepsza struktura folderów (jasne granice: dane / ingest / web /
  skrypty, → [12](12-flexibility-and-scalability.md)) + gęstszy, konkretny `AI_README` w każdym z
  nich bije jeden ogólnikowy plik w rootcie. Ważne informacje (gotchas, kontrakty, liczby) trzymaj
  **blisko kodu, którego dotyczą**.

## Kiedy aktualizować (a kiedy nie)

| Zmiana | Aktualizować dokumentację? |
|--------|----------------------------|
| Nowy moduł / funkcja / skrypt / flaga CLI | ✅ |
| Nowa migracja / kolumna / tabela | ✅ (doc DB + doc skryptów) |
| Zmiana liczby testów / rekordów | ✅ |
| Zmiana zachowania (nowy próg, nowy fallback) | ✅ |
| Czysty bugfix bez zmiany API/struktury | ❌ (odnotuj, że sprawdziłeś) |
| Literówka, formatowanie | ❌ |

## Dokumentacja jako kod
- **Źródło prawdy to `.md`** — ręcznie pisany, wersjonowany w git jak reszta kodu. Historia docsów
  (`git log` po `.md`) mówi *kiedy i czemu* reguła się zmieniła. Nie trzymaj prawdy w wygenerowanym HTML.
- **Linki względne** między plikami `.md` — żeby dało się klikać i walidować.
- **Jeden „spis treści"** (np. `docs/AI_README.md`) z tabelą „gdzie zacząć dla zadania X".

## Czytnik dokumentacji i regeneracja

`.md` jest źródłem prawdy, ale człowiek czyta wygodniej w przeglądarce. Dodaj **prosty czytnik
`documentation.html` w rootcie repo** — renderuje `.md` (np. `marked`), wersjonowany w git jak
każdy plik. Jeden plik, bez bundlera; działa z dwukliku i z serwera (ten codex sam tak działa).

- **Wygenerowany artefakt (snapshot/HTML) jest pochodną, nie źródłem.** Commituj go, ale **nigdy
  nie edytuj ręcznie** — nadpisze go build.
- **Regeneracja NIE odpala się sama.** Żadnego auto-buildu przy każdym commicie (szum, zwłoka,
  konflikty). Odpalasz ją **na polecenie** — najlepiej skillem (→ [02](02-skills-and-refactoring.md)),
  nie hookiem.
- **Skill regeneracji patrzy w git od ostatniej aktualizacji docsów.** Zamiast ślepo przebudowywać
  wszystko: czyta `git log <ostatni-commit-docs>..HEAD` (albo od taga `docs-*`), widzi **co realnie
  się zmieniło** (Przykazanie II → [05](05-git-and-deployments.md)), aktualizuje dotknięte sekcje i
  **wypisuje, co zmienił**. Tani, świadomy, sprawdzalny — zamiast „przebuduj i ufaj".

## Anty-wzorce
- 🚫 „Zaktualizuję docs na końcu" → koniec nie nadchodzi, dokumentacja kłamie.
- 🚫 AI_README opisujący *intencję* zamiast *stanu* — agent działa na tym, co napisane, nie na marzeniach.
- 🚫 Duplikowanie stanu z `CLAUDE.md` do pięciu miejsc — jedno źródło prawdy, reszta linkuje.
- 🚫 **Opis pliku zbyt ogólny** („różne reguły", „helpery") — grep nie trafia, agent skanuje wszystko
  i przepala kontekst. Opisuj keywordami, nie etykietami.

## W praktyce
Start nowego projektu: najpierw `CLAUDE.md` (stack, jak uruchomić, polityki i **twarde reguły
domeny** — np. prywatność, ograniczenia prawne), potem `AI_README.md` w katalogach o największej
wadze (auth, i18n, pipeline'y danych). Reguły nadrzędne (np. privacy-by-design) zapisuj jako
**politykę w konstytucji**, nie jako luźną notatkę. → [07](07-new-project-day-0.md)
