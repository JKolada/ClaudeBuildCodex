# 07 — Nowy projekt: Dzień 0

Konkretna checklista, którą Claude wykonuje (z Kubą) **rozpoczynając nowy projekt**.
Cel: po Dniu 0 każda kolejna sesja ma grunt pod nogami.

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

> **Minimalny Dzień 0**, gdy nie ma czasu na wszystko: `CLAUDE.md` (stack + jak uruchomić +
> polityki) → `.gitignore` → jeden skill `/run-<projekt>` ze smoke testem → szkielet testów →
> katalog `backups/`. Reszta dorasta z projektem.
