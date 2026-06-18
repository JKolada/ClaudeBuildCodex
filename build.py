#!/usr/bin/env python3
"""Buduje content.js — snapshot rozdziałów .md osadzony w JS.

Po co: przeglądarka blokuje fetch() plików lokalnych przez file://, więc otwarcie
index.html z dysku (dwuklik) nie mogłoby renderować .md. Dane wczytane przez <script>
(content.js) działają też po file://. Pliki .md pozostają jedynym źródłem prawdy —
content.js to artefakt generowany.

Użycie:  python build.py
Uruchom po każdej edycji .md (albo przed publikacją). index.html i tak woli świeże .md
przez fetch, gdy strona jest serwowana — content.js jest fallbackiem dla file://.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def collect(base):
    """Zbierz {slug: markdown} z katalogu base (rozdziały NN-*.md + intro + README, jeśli są)."""
    docs = {}
    files = sorted(p for p in base.glob("[0-9][0-9]-*.md"))
    for extra in ("intro.md", "README.md"):  # nie-numerowane dokumenty specjalne
        p = base / extra
        if p.exists():
            files.append(p)
    for path in files:
        docs[path.stem] = path.read_text(encoding="utf-8")  # slug = nazwa bez .md
    return docs

def content_js():
    """Zwróć (tekst content.js, mapę {lang:{slug:md}}). Jedno źródło prawdy buildu — używa go też test."""
    # Wielojęzycznie: EN kanonicznie w rootcie, PL w pl/. Każdy język = osobny namespace.
    langs = {"en": ROOT}
    pl_dir = ROOT / "pl"
    if pl_dir.is_dir():
        langs["pl"] = pl_dir
    by_lang = {code: collect(base) for code, base in langs.items()}
    # ensure_ascii=True → czysty ASCII (odporne na detekcję kodowania po file://).
    payload = json.dumps(by_lang, ensure_ascii=True, sort_keys=True)
    text = (
        "/* PLIK GENEROWANY przez build.py — nie edytuj ręcznie. "
        "Źródłem prawdy są pliki .md. Struktura: { lang: { slug: markdown } }. */\n"
        "window.RZEMIOSLO_DOCS = " + payload + ";\n"
    )
    return text, by_lang

def main():
    text, by_lang = content_js()
    (ROOT / "content.js").write_text(text, encoding="utf-8")
    parts = []
    for code, docs in sorted(by_lang.items()):
        total = sum(len(v) for v in docs.values())
        parts.append(f"{code}: {len(docs)} docs, {total} chars")
    print("content.js — " + " | ".join(parts) + ".")

if __name__ == "__main__":
    main()
