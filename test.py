#!/usr/bin/env python3
"""Prosty smoke test repo (czysty Python, zero zależności).

Łapie regresje strukturalne, o które prosi sama doktryna: parytet PL↔EN, martwe
linki między rozdziałami, nieaktualny content.js, rozjazd CHAPTERS/tabel/codex.json.
NIE testuje runtime JS (od tego jest podgląd w przeglądarce — Przykazanie III).

Użycie:  python test.py      # exit 0 = zielone, exit 1 = lista problemów
"""
import json
import re
import sys
from pathlib import Path

import build  # współdzielone: build.content_js(), build.collect()

ROOT = Path(__file__).resolve().parent
TR = ROOT / "pl"   # tłumaczenie (PL); kanon (EN) jest w rootcie
errors = []

try:  # Windows: konsola bywa cp1252 — wymuś UTF-8, by polskie znaki nie wywaliły printu.
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


def err(msg):
    errors.append(msg)


def chapter_files(base):
    return sorted(p.name for p in base.glob("[0-9][0-9]-*.md"))


def cross_links(path):
    # linki w stylu [tekst](NN-nazwa.md) lub (NN-nazwa.md#kotwica)
    return re.findall(r"\]\((\d\d-[a-z0-9-]+\.md)(?:#[^)]*)?\)", path.read_text(encoding="utf-8"))


def main():
    base = chapter_files(ROOT)              # kanon (EN) w rootcie
    tr = chapter_files(TR) if TR.is_dir() else []   # tłumaczenie (PL) w pl/

    # 1) Parytet EN↔PL — ten sam zestaw nazw plików (rozdziały + intro).
    if set(base) != set(tr):
        only_base = sorted(set(base) - set(tr))
        only_tr = sorted(set(tr) - set(base))
        if only_base:
            err(f"Parytet: rozdziały bez tłumaczenia PL (pl/): {only_base}")
        if only_tr:
            err(f"Parytet: rozdziały w pl/ bez kanonu EN: {only_tr}")
    for extra in ("intro.md",):
        if (ROOT / extra).exists() and not (TR / extra).exists():
            err(f"Parytet: brak tłumaczenia pl/{extra}")

    # 2) Martwe linki między rozdziałami (cel musi istnieć w tym samym katalogu).
    docs = [ROOT / n for n in base] + [ROOT / "intro.md"]
    docs += [TR / n for n in tr] + [TR / "intro.md"]
    for d in docs:
        if not d.exists():
            continue
        for target in cross_links(d):
            if not (d.parent / target).exists():
                err(f"Martwy link: {d.relative_to(ROOT)} → {target} (brak {d.parent.name}/{target})")

    # 3) Świeżość content.js — musi być zgodny z aktualnymi .md.
    expected, _ = build.content_js()
    actual = (ROOT / "content.js").read_text(encoding="utf-8")
    if expected != actual:
        err("content.js jest nieaktualny — uruchom: python build.py")

    # 4) CHAPTERS (index.html) ↔ pliki ↔ codex.json.
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    chapters = re.findall(r'file:"(\d\d-[a-z0-9-]+\.md)"', html)
    for f in chapters:
        if not (ROOT / f).exists():
            err(f"CHAPTERS: wpis bez pliku kanonu (EN): {f}")
        if TR.is_dir() and not (TR / f).exists():
            err(f"CHAPTERS: wpis bez tłumaczenia: pl/{f}")
    missing_in_chapters = sorted(set(base) - set(chapters))
    if missing_in_chapters:
        err(f"CHAPTERS: rozdziały na dysku nieobecne w index.html: {missing_in_chapters}")
    codex = json.loads((ROOT / "codex.json").read_text(encoding="utf-8"))
    if codex.get("chapters") != len(chapters):
        err(f"codex.json chapters={codex.get('chapters')} ≠ liczba rozdziałów ({len(chapters)})")

    # 5) Każdy rozdział wymieniony w README i AI_README (reguła „trzy miejsca w zgodzie").
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    ai = (ROOT / "AI_README.md").read_text(encoding="utf-8")
    for f in base:
        if f not in readme:
            err(f"README.md nie wymienia rozdziału: {f}")
        if f not in ai:
            err(f"AI_README.md nie wymienia rozdziału: {f}")

    # 6) Nawigacja index.html: każdy STATYCZNY link `href="#..."` prowadzi gdzieś sensownie.
    # Klasa znaków [a-z0-9_-] pomija stringi JS (`#'+slug(...)`); `#ic-*` to sprite SVG (<use>), nie nawigacja.
    slugs = {c[:-3] for c in chapters}           # bez ".md"
    valid_hash = slugs | {"", "brief", "intro"}  # "" = href="#" (strona główna)
    for h in re.findall(r'href="#([a-z0-9_-]*)"', html):
        if h.startswith("ic-"):
            continue
        if h not in valid_hash:
            err(f"index.html: link #{h} nie prowadzi do strony/rozdziału (nav/footer/manifest/brief)")

    # 7) Każdy `data-i18n`/`data-i18n-html` ma klucz w słowniku UI (inaczej zostaje nieprzetłumaczony).
    m = re.search(r"var UI = \{(.*?)\n  \};", html, re.S)
    ui_keys = set(re.findall(r"\n    ([A-Za-z0-9_]+):", m.group(1))) if m else set()
    if not ui_keys:
        err("index.html: nie znaleziono słownika UI (zmiana struktury?) — sprawdź test 7.")
    for key in sorted(set(re.findall(r'data-i18n(?:-html)?="([^"]+)"', html))):
        if key not in ui_keys:
            err(f"index.html: data-i18n „{key}” bez klucza w UI (zostanie nieprzetłumaczone)")

    # 8) Każdy `data-bf-label` (etykieta pola checkbox) ma wpis w BRIEF_FIELDS.
    # Zawężone do `bf-...`, by pominąć selektor JS `data-bf-label="'+f.id+'"`.
    bf_ids = set(re.findall(r'\{id:"(bf-[a-z0-9-]+)"', html))
    for bid in sorted(set(re.findall(r'data-bf-label="(bf-[a-z0-9-]+)"', html))):
        if bid not in bf_ids:
            err(f"index.html: data-bf-label „{bid}” bez wpisu w BRIEF_FIELDS")

    if errors:
        print(f"FAIL — {len(errors)} problem(ów):")
        for e in errors:
            print(f"  - {e}")
        return 1
    print(f"OK — {len(base)} rozdziałów EN(kanon)/PL, content.js świeży, linki i metadane spójne.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
