"""Convert the old Firebase Realtime Database export (data/firebase/*.json) into data/catalog.json.

The 2024-25 Aipex site kept a hand-curated list of AI tools and apps in Firebase (models, categories,
tags; votes were a plain counter). This keeps that list as a static file the site reads directly.
Re-export with:  curl https://aipex-6d63b-default-rtdb.europe-west1.firebasedatabase.app/<path>.json
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FB = ROOT / "data" / "firebase"


def load(name):
    return json.loads((FB / name).read_text(encoding="utf-8"))


def main():
    models = load("models.json")
    categories = sorted(set(load("categories.json").values()))
    tags = sorted(set(load("tags.json").values()))

    tools = []
    for fid, m in models.items():
        cats = []
        for c in m.get("categories") or []:
            if c and c not in cats:
                cats.append(c)
        tools.append({
            "id": fid,
            "name": m["name"].strip(),
            "categories": cats,
            "tags": sorted(set(t for t in (m.get("tags") or []) if t)),
            "license": m.get("license"),
            "open": m.get("license") == "Open Source",
            "link": m.get("weblink"),
            "editorChoice": bool(m.get("editorChoice")),
            "votes": m.get("votes") or 0,
            "created": (m.get("createdAt") or "")[:10],
            "updated": (m.get("lastUpdated") or "")[:10],
        })
    tools.sort(key=lambda t: (not t["editorChoice"], -t["votes"], t["name"].lower()))

    out = {"source": "Aipex Firebase database (2024-2025), imported 2026-10-18",
           "categories": categories, "tags": tags, "tools": tools}
    (ROOT / "data" / "catalog.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(tools)} tools, {len(categories)} categories, {len(tags)} tags")


if __name__ == "__main__":
    main()
