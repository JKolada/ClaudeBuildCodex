# AI_README — `docs/`

Dokumentacja „cięższa niż mapa katalogu": **plany i decyzje dotyczące samego repo Rzemiosło**.
Konwencja z rozdziału [01](../01-documentation-and-ai-readme.md). Uwaga: **to repo to zestaw reguł** —
`docs/` trzyma plany jego rozwoju i decyzje meta, **nie** treść doktryny (ta żyje w `00-*.md`…`14-*.md`).

## Zawartość

| Ścieżka | Po co |
|---------|-------|
| `plans/` | Decyzje i kierunki rozwoju. Jeden plik = jeden temat (`NNNN-tytuł.md`). |
| `plans/0001-i18n-and-packaging.md` | Kierunek: wersje językowe (EN) + pakowanie `docs/rules/` per język przez The Craft Web. |
| `plans/0002-monetization-and-payments.md` | **Niezrealizowane** — monetyzacja i płatności. Brak hands-on → świadomie bez rozdziału doktryny; plan trzyma kierunek. |

## Zasady

- **`docs/` i `plans/` opisują stan BIEŻĄCY, nie historię.** Wszystko jest wersjonowane w git — więc
  **nie trzymaj tu wpisów-zombie** (skończonych zadań, nieaktualnych decyzji). Skończone/nieaktualne →
  **usuń**; historię i tak masz w `git log`.
- **Plan = problem → opcje → decyzja → „dlaczego".** Gdy plan się zrealizuje: jego decyzja **awansuje** do
  [CLAUDE.md](../CLAUDE.md) / właściwego dokumentu (tam *obowiązuje*), a sam plan **zamykasz/usuwasz**.
  `plans/` trzyma tylko otwarte, aktywne kierunki.
- Numeracja `NNNN` rośnie monotonicznie; numeru usuniętego planu nie reużywaj (był kotwicą w historii).
