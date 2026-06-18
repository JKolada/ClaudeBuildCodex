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

def main():
    docs = {}
    files = sorted(p for p in ROOT.glob("[0-9][0-9]-*.md"))
    readme = ROOT / "README.md"
    if readme.exists():
        files.append(readme)
    for path in files:
        slug = path.stem  # nazwa bez .md
        docs[slug] = path.read_text(encoding="utf-8")

    # ensure_ascii=True → czysty ASCII (odporne na detekcję kodowania po file://).
    payload = json.dumps(docs, ensure_ascii=True, sort_keys=True)
    out = (
        "/* PLIK GENEROWANY przez build.py — nie edytuj ręcznie. "
        "Źródłem prawdy są pliki .md. */\n"
        "window.RZEMIOSLO_DOCS = " + payload + ";\n"
    )
    (ROOT / "content.js").write_text(out, encoding="utf-8")
    total = sum(len(v) for v in docs.values())
    print(f"content.js: {len(docs)} docs, {total} chars.")

if __name__ == "__main__":
    main()
