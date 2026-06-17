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
Reguła z WhiskyPolska, którą warto przenieść: **każdy katalog ma `AI_README.md`**, a jego
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
- **Linki względne** między plikami `.md` — żeby dało się klikać i walidować.
- **Jeden „spis treści"** (jak `docs/AI_README.md` w WhiskyPolska) z tabelą „gdzie zacząć dla zadania X".
- Ciężkie rzeczy (regeneracja statycznego HTML z docsów) — **nie przy każdym commicie**;
  rób zbiorczo i sugeruj userowi, nie odpalaj sam.

## Anty-wzorce
- 🚫 „Zaktualizuję docs na końcu" → koniec nie nadchodzi, dokumentacja kłamie.
- 🚫 AI_README opisujący *intencję* zamiast *stanu* — agent działa na tym, co napisane, nie na marzeniach.
- 🚫 Duplikowanie stanu z `CLAUDE.md` do pięciu miejsc — jedno źródło prawdy, reszta linkuje.

## Dla EchoInsight
Zacznij od `CLAUDE.md` (stack, „nie świadczymy usług terapeutycznych", „nie czytamy rozmów",
polityka prywatności/anonimizacji jako twarda reguła) + `AI_README.md` w katalogach
auth / i18n / pipeline-anonimizacji. Privacy-by-design zapisz jako **politykę w konstytucji**,
nie jako luźną notatkę. → [08](08-echoinsight.md)
