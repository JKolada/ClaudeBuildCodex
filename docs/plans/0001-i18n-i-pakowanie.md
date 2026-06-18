# 0001 — Wersje językowe i pakowanie per język

> Status: **przyjęty kierunek, realizacja odroczona** (na razie PL jest jedynym językiem).
> Data decyzji: 2026-06-18. Dotyczy podziału ról między **to repo (rdzeń reguł)** a **The Craft Web
> (prezentacja + pakowanie)**.

## Problem

Rdzeń reguł jest po polsku. Chcemy:
1. wersji **angielskiej** (i docelowo kolejnych języków),
2. żeby **The Craft Web** budował z tego **paczki `docs/rules/` w konkretnym języku** (do dołączenia
   do nowego projektu jako submoduł/zip), stemplowane wersją z `codex.json`.

Pytanie: gdzie żyje kanoniczna treść tłumaczeń i jak rozdzielić to od warstwy prezentacji.

## Decyzje (przyjęte)

1. **Kanoniczna treść każdego języka żyje w TYM repo.** Rdzeń jest źródłem prawdy — także dla
   tłumaczeń. Parytet językowy jest wtedy testowalny 1:1 (→ [10](../../10-seo-i-tlumaczenia.md):
   żaden język „w połowie"). Web **renderuje i pakuje**, nie tłumaczy w oderwaniu od źródła.
2. **Na teraz: PL jest jedynym językiem.** Nie przebudowujemy struktury, dopóki treść się nie
   ustabilizuje. Ten plan ustala **konwencję do wdrożenia, gdy ruszymy EN** — żeby nie łamać linków
   i kotwic przedwcześnie.
3. **Edycje (techniczna / BIZ-TECH / biznesowa) to domena Web, nie tego repo.** Rdzeń trzyma tylko
   rejestr **TECHNICZNY** — w każdym języku. „Zmiękczanie" rejestru robi Web.

## Konwencja do wdrożenia (gdy zaczynamy EN)

- **Układ per język w katalogach:** `lang/pl/NN-*.md`, `lang/en/NN-*.md` (mirror tej samej listy
  rozdziałów). Migracja = przeniesienie obecnych `00-*.md`…`14-*.md` z rootu do `lang/pl/`.
  - **Slugi/numery plików zostają stabilne i wspólne** dla wszystkich języków (`NN-<pl-slug>.md`) —
    są kotwicami i celami linków względnych (→ [05](../../05-git-i-wdrozenia.md)). Nie lokalizujemy
    nazw plików; lokalizujemy **treść** w środku. (Alternatywa — slugi per język — odrzucona: rozsypuje
    cross-linki i mapowanie 1:1.)
- **`codex.json` zyskuje:** `languages: ["pl","en"]`, `default_language: "pl"`. `version`/`released`
  pozostają wspólne dla całego wydania (jedna doktryna, wiele języków).
- **`build.py`** generuje snapshot per język (`content.<lang>.js` albo namespace w `content.js`).
  Lokalny czytnik `index.html` pozostaje **minimalny** (podgląd, domyślnie PL) — **przełącznik języka
  i pełna prezentacja to Web**, nie rdzeń.
- **Parytet jako bramka (→ [10](../../10-seo-i-tlumaczenia.md)):** EN musi mieć komplet rozdziałów co
  PL (ta sama lista, te same kotwice). Brakujący/rozjechany rozdział = build fail, nie „pół wersji".

## Rola The Craft Web (pakowanie)

- Pobiera `lang/<code>/` + `codex.json` z tego repo przy buildzie.
- Emituje **paczkę per język** (np. `the-craft-<code>.zip` lub gotowe drzewo `docs/rules/<code>/`),
  ostemplowaną `version` + `language`, gotową do wpięcia w nowy projekt.
- Renderuje publiczną witrynę i **edycje** (techniczna → BIZ-TECH → biznesowa) jako warstwę podania
  nad tą samą treścią. Macierz `język × edycja` żyje po stronie Web; rdzeń dostarcza język × TECHNICZNA.

## Otwarte (do rozstrzygnięcia przy starcie EN)

- **Workflow tłumaczenia:** człowiek vs agent + review; jak pilnować, że zmiana reguły w PL
  pociąga aktualizację EN (np. checklista/te­st parytetu, oznaczanie „stale translation").
- **Kto i gdzie pisze edycje BIZ-TECH/biznesowe** (Web) — osobny plan, gdy dojdziemy do tej warstwy.
- **Nazwa marki w EN** już jest: „The Craft — Kolada Build" (PL: „Rzemiosło").

## Następny krok

Nie ruszamy struktury teraz. Gdy treść PL się ustabilizuje i zdecydujemy zacząć EN — realizujemy
„Konwencję do wdrożenia" w jednym, świadomym refaktorze (przeniesienie do `lang/pl/`, dodanie
`lang/en/`, aktualizacja `build.py`, `codex.json`, czytnika i trzech miejsc listy rozdziałów).
