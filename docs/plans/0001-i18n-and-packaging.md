# 0001 — Wersje językowe i pakowanie per język

> Status: **EN zrealizowane; od 2026-06-19 EN jest BAZĄ.** Repo dwujęzyczne. Pakowanie per język
> (Web) i kolejne języki — nadal otwarte. Dotyczy podziału ról między **to repo (rdzeń reguł)**
> a **The Craft Web (prezentacja + pakowanie)**.
>
> **Aktualizacja 2026-06-19 — odwrócenie kanonu:** angielski stał się **bazą**. Układ jest teraz
> **EN w rootcie (kanon), PL w `pl/`** (wcześniej PL root + `en/`). Domyślny język czytnika = EN.
> `codex.json`: `default_language: "en"`, `lang_paths {"en":".","pl":"pl"}`. Poniższe wzmianki o
> „PL w rootcie / `en/`" są historyczne — obowiązuje wersja z tej notki.

## Zrealizowane (2026-06-18)

- **Układ: PL kanonicznie w rootcie, EN w `en/`** (te same nazwy plików `00-*.md`…`14-*.md`).
  Świadome odejście od pierwotnego `lang/pl` + `lang/en`: zerowe ryzyko dla istniejących linków PL,
  a Web i tak czyta `lang_paths` z `codex.json` (`{"pl":".","en":"en"}`). Pełną symetrię `lang/<code>/`
  można wprowadzić później, jeśli dojdzie trzeci język.
- **Slugi/numery wspólne dla obu języków** (kotwice). Treść EN to tłumaczenie 1:1 listy rozdziałów.
- **Nazwy plików = angielskie** (`00-commandments.md`, `01-documentation-and-ai-readme.md`, …) —
  rename z polskich slugów na życzenie. Wspólne dla PL i EN; pozostają stabilnymi kotwicami. **Zmienia
  to wcześniejszą decyzję** (poniżej, „Konwencja…") o trzymaniu polskich slugów — ta jest już nieaktualna.
- **`build.py`** generuje `content.js` jako `{lang:{slug:md}}` (PL + EN). **`codex.json`** zyskał
  `languages`, `default_language`, `lang_paths`.
- **Czytnik** (`index.html`) ma minimalny **przełącznik treści PL/EN** (`#langToggle`, zapis w
  `localStorage` `rzemioslo-lang`); fetch z rootu (PL) lub `en/` (EN); chrome strony zostaje PL.
- **Parytet jako reguła** (CLAUDE.md + AI_README): zmiana reguły w PL → aktualizacja `en/` w tym kroku.

## Problem

Rdzeń reguł jest po polsku. Chcemy:
1. wersji **angielskiej** (i docelowo kolejnych języków),
2. żeby **The Craft Web** budował z tego **paczki `docs/rules/` w konkretnym języku** (do dołączenia
   do nowego projektu jako submoduł/zip), stemplowane wersją z `codex.json`.

Pytanie: gdzie żyje kanoniczna treść tłumaczeń i jak rozdzielić to od warstwy prezentacji.

## Decyzje (przyjęte)

1. **Kanoniczna treść każdego języka żyje w TYM repo.** Rdzeń jest źródłem prawdy — także dla
   tłumaczeń. Parytet językowy jest wtedy testowalny 1:1 (→ [10](../../10-seo-and-translations.md):
   żaden język „w połowie"). Web **renderuje i pakuje**, nie tłumaczy w oderwaniu od źródła.
2. **Na teraz: PL jest jedynym językiem.** Nie przebudowujemy struktury, dopóki treść się nie
   ustabilizuje. Ten plan ustala **konwencję do wdrożenia, gdy ruszymy EN** — żeby nie łamać linków
   i kotwic przedwcześnie.
3. **Edycje (techniczna / BIZ-TECH / biznesowa) to domena Web, nie tego repo.** Rdzeń trzyma tylko
   rejestr **TECHNICZNY** — w każdym języku. „Zmiękczanie" rejestru robi Web.

## Konwencja do wdrożenia (gdy zaczynamy EN)

- **Układ per język w katalogach:** `lang/pl/NN-*.md`, `lang/en/NN-*.md` (mirror tej samej listy
  rozdziałów). Migracja = przeniesienie obecnych `00-*.md`…`14-*.md` z rootu do `lang/pl/`.
  - **Slugi/numery plików zostają stabilne i wspólne** dla wszystkich języków — są kotwicami i celami
    linków względnych (→ [05](../../05-git-and-deployments.md)). Lokalizujemy **treść**, nie nazwy plików.
    **Aktualizacja:** slugi są teraz **angielskie** (`NN-english-slug.md`, np. `00-commandments.md`) —
    wspólne dla PL i EN. (Wcześniejszy zapis o polskich slugach jest nieaktualny; patrz „Zrealizowane".)
- **`codex.json` zyskuje:** `languages: ["pl","en"]`, `default_language: "pl"`. `version`/`released`
  pozostają wspólne dla całego wydania (jedna doktryna, wiele języków).
- **`build.py`** generuje snapshot per język (`content.<lang>.js` albo namespace w `content.js`).
  Lokalny czytnik `index.html` pozostaje **minimalny** (podgląd, domyślnie PL) — **przełącznik języka
  i pełna prezentacja to Web**, nie rdzeń.
- **Parytet jako bramka (→ [10](../../10-seo-and-translations.md)):** EN musi mieć komplet rozdziałów co
  PL (ta sama lista, te same kotwice). Brakujący/rozjechany rozdział = build fail, nie „pół wersji".

## Rola The Craft Web (pakowanie)

- Pobiera `lang/<code>/` + `codex.json` z tego repo przy buildzie.
- Emituje **paczkę per język** (np. `the-craft-<code>.zip` lub gotowe drzewo `docs/rules/<code>/`),
  ostemplowaną `version` + `language`, gotową do wpięcia w nowy projekt.
- Renderuje publiczną witrynę i **edycje** (techniczna → BIZ-TECH → biznesowa) jako warstwę podania
  nad tą samą treścią. Macierz `język × edycja` żyje po stronie Web; rdzeń dostarcza język × TECHNICZNA.

## Co pakować do zipa `docs/rules/` (spec dla Web)

Paczka = **przeglądalny pakiet codexu**: agent go grepuje (`AI_README`), a człowiek **przegląda wprost w
projekcie** czytnikiem (dwuklik `index.html`, nie surowy `.md`). Zostaje doktryna + czytnik; wypada tylko
meta utrzymania **tego** repo.

**Pakuj — treść:**

- **`AI_README.md`** — *wejście agenta*: mapa rozdziałów + grep-index. (Bez przycinania — czytnik/build są
  w paczce, więc opis `index.html`/`build.py` jest tu prawdziwy.)
- **`00-commandments.md` … `16-driving-claude.md`** — komplet rozdziałów (17).
- **`intro.md`** — manifest.
- **`pl/`** (i kolejne `<lang>/`) — wersje w innych językach, jeśli chcesz pełny **przełącznik EN/PL** w
  czytniku. Per-jeden-język: pomiń pozostałe (czytnik wtedy jednojęzyczny).
- **`craft.json`** — stempel: `version`, `language`(/`languages`), `edition`, `released`, `source` (commit/URL).
  Żeby projekt wiedział, którą wersję ma i czy jest update. Pola z `codex.json`.

**Pakuj — czytnik (do swobodnego przeglądania):**

- **`index.html` + `content.js`** — czytnik SPA: dwuklik → ładny render doktryny, tryb jasny/ciemny,
  przełącznik języka. Działa po `file://` dzięki snapshotowi `content.js` (bez serwera).
- **`build.py`** — żeby po ewentualnej edycji `.md` w projekcie odświeżyć snapshot (`python build.py`).
- **`public/logo.png`** — bo `index.html` referuje logo/favicon (inaczej broken).

**NIE pakuj** (meta utrzymania tego repo, nie doktryna):

- `CLAUDE.md` (konstytucja **tego** repo — docelowy projekt ma własny `CLAUDE.md`),
- `README.md` (front door GitHuba), `docs/` (plany repo), `CHANGELOG.md`, `test.py` (CI tego repo), `.git*`.

**Struktura zipa (pełna, dwujęzyczna — zalecana do przeglądania):**

```
docs/rules/
  AI_README.md          # mapa + grep-index (EN/baza)
  index.html  content.js  build.py  public/logo.png   # czytnik
  intro.md
  00-commandments.md … 16-driving-claude.md           # treść EN
  pl/  AI_README.md  intro.md  00-…16-….md             # treść PL
  craft.json
```

**Gotchas pakowania:**

- **Cross-linki** w rozdziałach (`[NN](NN-nazwa.md)`) działają w `docs/rules/` (te same nazwy, jeden
  katalog) — **nie ruszaj**. `intro.md` linkuje do `index.html#brief` — w paczce z czytnikiem **działa**.
- **Slug wspólny dla języków** → ten sam układ niezależnie od liczby języków; różni się tylko treść.
- **Per-język vs pełna paczka:** pełna (root + `pl/` + czytnik) = działający przełącznik EN/PL; jednojęzyczna
  = mniejszy zip, czytnik bez drugiego języka. Wybór po stronie Web (przycisk „pobierz: EN / PL / EN+PL").
- **Edycja:** na teraz tylko **TECHNICZNA**; BIZ-TECH/biznesowa to ten sam zestaw plików, inny rejestr →
  pole `edition` w stemplu, gdy powstaną.
- **Wpięcie u klienta** (→ [07](../../07-new-project-day-0.md)): submodule albo kopia + wpis w `CLAUDE.md`
  projektu „czytaj `docs/rules/` co sesję; grep po `docs/rules/AI_README.md`; do przeglądania otwórz `docs/rules/index.html`".

## Otwarte (do rozstrzygnięcia przy starcie EN)

- **Workflow tłumaczenia:** człowiek vs agent + review; jak pilnować, że zmiana reguły w PL
  pociąga aktualizację EN (np. checklista/te­st parytetu, oznaczanie „stale translation").
- **Kto i gdzie pisze edycje BIZ-TECH/biznesowe** (Web) — osobny plan, gdy dojdziemy do tej warstwy.
- **Nazwa marki w EN** już jest: „The Craft — Kolada Build" (PL: „Rzemiosło").

## Następny krok

Nie ruszamy struktury teraz. Gdy treść PL się ustabilizuje i zdecydujemy zacząć EN — realizujemy
„Konwencję do wdrożenia" w jednym, świadomym refaktorze (przeniesienie do `lang/pl/`, dodanie
`lang/en/`, aktualizacja `build.py`, `codex.json`, czytnika i trzech miejsc listy rozdziałów).
