# CLAUDE.md — Claude Build Codex

> Konstytucja tego repozytorium. Instrukcje tutaj **mają pierwszeństwo** przed domyślnym
> zachowaniem agenta. Czytane co sesję — utrzymuj je aktualne (Przykazanie I).

## Czym jest ten projekt

**Claude Build Codex** to **doktryna budowania i prowadzenia aplikacji end-to-end
z Claude**: zwarty zestaw konkretnych **reguł, przykazań i antywzorców**. Nie podręcznik
frameworka — *doktryna współpracy* człowiek + agent przez całe życie projektu (od pierwszego
commita po prod z żywymi użytkownikami).

Sygnatura: **jakub.solutions** · Jakub Kolada — Insurance Systems Architect & IT Consultant.
Paleta (fiolet→cyan) i typografia (Playfair Display + Outfit) spójne z marką.

**Dwie role docelowe (projektuj treść pod obie):**
1. **Reuse jako `/docs/rules/`** — repo dołączane do każdego nowego projektu (np. git submodule),
   żeby agent miał te zasady w kontekście od Dnia 0.
2. **Materiał publiczny** — pomoc dla **każdej** osoby zaczynającej przygodę z Claude, nie tylko
   dla autora. Stąd treść ma być **generyczna**: reguły uniwersalne, a konkretne projekty (np.
   WhiskyPolska) służą tylko za ilustrację — nigdy za temat. Nie pisz doktryny „pod jeden projekt".

## Stack i charakter repo

| Warstwa | Tech | Lokalizacja |
|---------|------|-------------|
| Treść (źródło prawdy) | Markdown, ręcznie pisany | `00-*.md` … `13-*.md`, `README.md` |
| Przeglądarka treści | Jeden statyczny plik, SPA | `index.html` |
| Render markdown | `marked` z CDN (jsdelivr), hash-routing | inline w `index.html` |
| Snapshot treści (artefakt) | `.md` osadzone w JS, by działało po `file://` | `content.js` (generowany) |
| Build snapshotu | Skrypt łączący `.md` → `content.js` | `build.py` |
| Czcionki | Google Fonts (Playfair Display, Outfit, JetBrains Mono) | `<link>` w `index.html` |

**Jedyny build to `build.py`** (concat `.md` → `content.js`) — żadnego bundlera, package.json,
testów ani backendu. To repozytorium **dokumentacji**. „Kod" to `index.html` + `build.py`; trzymaj
prosto, nie over-engineeruj (→ [12](12-elastycznosc-i-skalowalnosc.md)).

## Jak uruchomić / podejrzeć

`index.html` ładuje treść **dwutorowo**: najpierw świeży `.md` przez `fetch()` (gdy strona jest
serwowana — zawsze aktualne), a gdy fetch jest zablokowany (`file://`), z osadzonego snapshotu
`content.js`. Dzięki temu działa **i z dwukliku, i z serwera**:

```bash
# podgląd z serwerem (zawsze świeże .md):
python -m http.server 8080      # → http://localhost:8080/   (albo: npx serve .)

# dwuklik index.html (file://) działa, o ile content.js jest aktualny:
python build.py                 # regeneruje content.js z plików .md
```

- Po `http(s)://` (localhost, GitHub Pages, hosting) — render z **żywych** `.md`.
- Po `file://` (dwuklik) — render ze snapshotu `content.js` (dlatego regeneruj go po edycji `.md`).
- Na GitHubie pliki `.md` renderują się natywnie (linki w kartach działają z palca).

## Polityki (nadpisują domyślne zachowanie)

- **Treść = pliki `.md`.** `index.html` ich nie zawiera — czyta je przez `fetch` (świeże) lub ze
  snapshotu `content.js` (file://). Jedno źródło prawdy. Edytujesz rozdział → edytujesz `.md`, nie HTML.
- **Po edycji `.md` uruchom `python build.py`** — regeneruje `content.js` (snapshot dla `file://`).
  `content.js` jest **generowany** (commituj go, ale nie edytuj ręcznie — nadpisze go build).
- **Lista rozdziałów żyje w jednym miejscu** — tablica `CHAPTERS` w `<script>` w `index.html`.
  Dodajesz/zmieniasz rozdział → aktualizujesz `CHAPTERS` (karty, dropdown i prev/next generują się
  z niej) **oraz** tabelę w `README.md` i `AI_README.md`.
- **Numeracja i slugi są stabilne** — `NN-nazwa.md`. Nie zmieniaj istniejących nazw plików bez
  potrzeby; są kotwicami (`#NN-nazwa`) i celami linków względnych między rozdziałami.
- **Linki między rozdziałami:** względne, w formie `[NN](NN-nazwa.md)` — `index.html` przepisuje
  je na hash-route w locie, a na GitHubie działają natywnie. Nie wpisuj `#`-linków w `.md`.
- **Ton i forma:** zwarte, imperatywne, z „dlaczego". Każdy rozdział = jedno przykazanie/temat,
  zakończony antywzorcami. Bez lania wody — to codex, nie esej.
- **Polski** to język treści. Terminy techniczne (commit, dry-run, deploy) zostają po angielsku.
  W przyszłości planowana **wersja angielska** — pisz reguły tak, by dały się przetłumaczyć (bez
  nieprzekładalnych gier słownych w samych regułach). Na razie nie twórz wersji EN.
- **Marka:** zachowaj paletę CSS (`--accent` fiolet, `--accent-2` cyan), Playfair w nagłówkach,
  minimalistyczny styl. Tryb jasny/ciemny: domyślnie wg systemu (`prefers-color-scheme`),
  z ręcznym przełącznikiem (`[data-theme]` na `<html>`, zapis w `localStorage`).
- **Commituj swobodnie i często** (wiele małych, spójnych commitów) — bez pytania o zgodę do każdego.
  Warunek: każdy commit **aktualizuje AI_README** zgodnie ze zmianą i najlepiej odnosi się do numeru
  taska. **Wyraźnej zgody wymagają tylko:** deploy na produkcję, swap bazy na produkcji oraz
  **push/publikacja** do zdalnego repo. To sedno Przykazania VI — nie dotyczy lokalnych commitów.
- **Wersja Claude Build Codex mieszka tutaj** (treść = to, co wersjonujemy): `codex.json` (`version` +
  `released`) i `CHANGELOG.md`. Wydanie = podnieś `codex.json`, dopisz wpis w `CHANGELOG.md` z datą
  publikacji, commit + **annotated tag** `vX.Y.Z` (Przykazanie VIII). `version` musi zgadzać się z
  najwyższym wpisem changeloga. Witryna `Claude Build Codex Web` konsumuje to przy buildzie i stempluje.

## Stan bieżący (2026-06-18)

- **14 rozdziałów** (`00`–`13`) + `README.md`. Rdzeń: 00–08; pogłębienie: 09–13.
- `index.html` — SPA-czytnik: strona główna (dekalog + karty) i widok rozdziału (render `.md`,
  select rozdziałów, prev/next, responsywny mobile/desktop, przełącznik jasny/ciemny). Treść:
  fetch świeżych `.md`, a po `file://` — snapshot `content.js`.
- `build.py` → `content.js` (snapshot dla `file://`). `CLAUDE.md` + `AI_README.md` — dokumentacja repo.
- Brak otwartych TODO w treści. Wersja żywa — rozszerzana po projektach, które czegoś nauczyły.

## Dla agenta zaczynającego sesję tutaj

1. Przeczytaj [00 — Dekalog](00-przykazania.md) — cała doktryna na jednym ekranie.
2. Zmiana treści → odpowiedni plik `.md`. Zmiana wyglądu/nawigacji → `index.html`.
3. Po zmianie listy rozdziałów zsynchronizuj **trzy** miejsca: `CHAPTERS`, `README.md`, `AI_README.md`.
4. **Po edycji `.md` → `python build.py`** (regeneruje `content.js`).
5. Sprawdź render przez lokalny serwer, zanim uznasz, że „działa" (Przykazanie III).
