"""Build data/aipex.json from the raw leaderboard dumps in data/raw/.

Inputs
  data/raw/arena.json      Arena leaderboards  {source, url, categories:[{category, metric, higher_is_better, entries:[...]}]}
  data/raw/others.json     other leaderboards  {sources:[{source, url, categories:[...]}], open_models:[...]}
  data/categories.json     maps "<source> :: <category>" to an Aipex category, and lists the Aipex categories
  data/models.json         per-model facts: open weights, licence, VRAM (overrides what the raw files say)
  data/aliases.json        model-name aliases -> canonical name

Scoring
  Within one source category, a score becomes 100 * 2^(-(leader - score) / (leader - 15th place)):
  the leader is 100, the 15th place 50, and so on, whatever the list length (lower-is-better metrics use
  the distance the other way). A model's Aipex score is the mean over the boards that rank it; in
  categories fed by several boards it is shrunk toward 50 with the weight of half a board.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
REF_RANK = 15
PRIOR = 50.0        # neutral score a missing board is assumed to give
PRIOR_WEIGHT = 0.5   # worth half a board


def load(name, default=None):
    p = DATA / name
    if not p.exists():
        if default is None:
            sys.exit(f"missing {p}")
        return default
    return json.loads(p.read_text(encoding="utf-8"))


def norm_key(name):
    s = name.lower()
    s = re.sub(r"^[\w.-]+/", "", s)                 # hf-style org/ prefix
    s = re.sub(r"\(.*?\)", "", s)                   # parenthesised notes
    s = re.sub(r"\b(preview|latest|exp|experimental)\b", "", s)
    s = re.sub(r"[^a-z0-9.]+", "-", s).strip("-")
    # word order varies between boards ("Omni 1.1 Flash" / "Omni Flash 1.1"): compare as a sorted token set
    return "-".join(sorted(t for t in s.split("-") if t))


OPEN_LICENCES = {
    "apache-2.0": "Apache-2.0", "apache 2.0": "Apache-2.0", "mit": "MIT", "cc-by-4.0": "CC-BY-4.0",
    "cc-by-nc-4.0": "CC-BY-NC-4.0", "cc-by-sa-4.0": "CC-BY-SA-4.0", "gpl-3.0": "GPL-3.0", "bsd-3-clause": "BSD-3",
    "openrail": "OpenRAIL", "openrail++": "OpenRAIL++", "llama3": "Llama", "gemma": "Gemma",
}


def licence_of(text):
    """Return a short licence label if the raw licence text means open weights, else None."""
    if not text:
        return None
    t = str(text).strip().lower()
    if any(w in t for w in ("propriet", "closed", "close source", "no open")) or t in ("api", "commercial"):
        return None
    if t in ("-", "unknown", "n/a", "none", "null"):
        return None
    if t in OPEN_LICENCES:
        return OPEN_LICENCES[t]
    for k, v in OPEN_LICENCES.items():
        if t.startswith(k):
            return v
    if "huggingface.co" in t or t.startswith(("open weight", "open source", "open-weight", "other", "open")):
        return "Open"
    # any other named licence (Llama Community, Qianwen, Modified MIT, CC-BY-NC, MRL, ...) means downloadable weights
    label = re.sub(r"\s*\b(license|licence|agreement)\b", "", str(text).strip(), flags=re.I).strip(" -")
    return label[:24] or "Open"


def vram_from_name(name):
    """Q4 VRAM estimate from a parameter count in the model name ("Gemma 4 31B", "Qwen3-30B-A3B"), else None."""
    m = re.search(r"(?<![\w.])(\d+(?:\.\d+)?)\s*[bB](?![a-zA-Z])", name)
    if not m:
        return None
    b = float(m.group(1))
    if b <= 0 or b > 2000:
        return None
    return round(b * 0.5625 * 1.15 + 0.5, 1)


EFFORT = re.compile(r"\s*\((?:\s*(?:max|high|xhigh|medium|low|minimal|thinking|reasoning|default fallback|non-reasoning|fc)\s*,?)+\)", re.I)


def display_name(name):
    """Drop reasoning-effort tags such as "(High)" or "(Max, Default Fallback)" from a model name."""
    return EFFORT.sub("", name).strip()


def keep_models(recs):
    """Top 30 overall, plus the best open models, so the open/VRAM filters always have candidates."""
    top = recs[:30]
    rest = [m for m in recs[30:] if m["open"]]
    keep = set(range(min(10, len(rest))))
    for limit in (8, 24, 32):   # the best few for each VRAM filter
        fits = [i for i, m in enumerate(rest) if m["vram_gb"] is not None and m["vram_gb"] <= limit]
        keep.update(fits[:5])
    return top + [rest[i] for i in sorted(keep)]


def main():
    cats_cfg = load("categories.json")
    models_cfg = load("models.json", {})
    aliases = {norm_key(k): v for k, v in load("aliases.json", {}).items()}

    raw_sources = []
    arena = load("raw/arena.json", {})
    if arena:
        raw_sources.append({"source": arena.get("source", "Arena"), "url": arena.get("url"), "categories": arena.get("categories", [])})
    others = load("raw/others.json", {})
    raw_sources += others.get("sources", [])
    open_models = list(others.get("open_models", []))
    for extra in sorted((DATA / "raw").glob("extra-*.json")):
        x = json.loads(extra.read_text(encoding="utf-8"))
        raw_sources += x.get("sources", [])
        open_models += x.get("open_models", [])

    # one board per (source, category): longer lists from extra files are merged into the same board,
    # so they share its scale; the first file to list a model keeps its entry
    merged = {}
    for src in raw_sources:
        tgt = merged.setdefault(src["source"], {"source": src["source"], "url": src.get("url"), "categories": []})
        tgt["url"] = tgt["url"] or src.get("url")
        for c in src.get("categories", []):
            have = next((h for h in tgt["categories"] if h["category"] == c["category"]), None)
            if have is None:
                tgt["categories"].append(dict(c, entries=list(c.get("entries", []))))
                continue
            known = {norm_key(e["model"]): e for e in have["entries"]}
            for e in c.get("entries", []):
                k = norm_key(e["model"])
                if k not in known:
                    have["entries"].append(e)
                elif not licence_of(known[k].get("license")) and licence_of(e.get("license")):
                    known[k]["license"] = e["license"]
    raw_sources = list(merged.values())

    # facts about open models from the research dumps, overridden by models.json
    facts = {}
    for m in open_models:
        v = m.get("vram_gb") or {}
        vram = v.get("q4") or v.get("fp8") or v.get("fp16")
        f = {"open": True, "license": licence_of(m.get("license")) or "Open", "vram_gb": vram, "vram_note": m.get("vram_note")}
        facts[norm_key(m["model"])] = f
        if m.get("hf_id"):
            facts.setdefault(norm_key(m["hf_id"]), f)
    for name, f in models_cfg.items():
        facts.setdefault(norm_key(name), {}).update(f)

    mapping = cats_cfg["map"]             # "Source :: Category" -> aipex category id (or null to skip)
    aipex_cats = {c["id"]: c for c in cats_cfg["categories"]}

    sources_out = {}
    per_cat = {cid: {} for cid in aipex_cats}   # cid -> canonical -> model record
    unmapped = []

    # "X (open weights only)" boards share X's scale: fold their entries into X so open models
    # below X's top 15 still get a place, instead of a second board whose leader scores 100.
    for src in raw_sources:
        base = {c["category"]: c for c in src.get("categories", [])}
        keep = []
        for c in src.get("categories", []):
            m = re.match(r"^(.*?)\s*\(open weights only\)\s*(.*)$", c["category"])
            parent = base.get((m.group(1) + (" " + m.group(2) if m.group(2) else "")).strip()) if m else None
            if parent is not None:
                seen = {norm_key(e["model"]) for e in parent["entries"]}
                parent["entries"] = parent["entries"] + [dict(e) for e in c["entries"] if norm_key(e["model"]) not in seen]
                open_keys = {norm_key(x["model"]) for x in c["entries"]}
                for e in parent["entries"]:
                    if norm_key(e["model"]) in open_keys and not licence_of(e.get("license")):
                        e["license"] = "open weights"
            else:
                keep.append(c)
        src["categories"] = keep

    for src in raw_sources:
        sname = src["source"]
        for cat in src.get("categories", []):
            key = f"{sname} :: {cat['category']}"
            cid = mapping.get(key, "__missing__")
            if cid == "__missing__":
                unmapped.append(key)
                continue
            if cid is None or cid not in aipex_cats:
                continue
            entries = [e for e in cat.get("entries", []) if isinstance(e.get("score"), (int, float))]
            if not entries:
                continue
            hib = cat.get("higher_is_better", True)
            entries.sort(key=lambda e: e["score"], reverse=hib)
            top = entries[0]["score"]
            ref = entries[min(REF_RANK, len(entries)) - 1]["score"]
            sid = re.sub(r"[^a-z0-9]+", "-", sname.lower()).strip("-")
            sources_out[sid] = {"id": sid, "name": sname, "url": src.get("url") or cat.get("url")}
            for e in entries:
                # leader = 100, the board's 15th place = 50, halving again for each further gap of that size;
                # independent of how long the list is, and never negative
                gap = abs(top - ref)
                n = 100.0 if gap == 0 else 100.0 * 2 ** (-abs(top - e["score"]) / gap)
                k = norm_key(e["model"])
                canon = aliases.get(k, e["model"])
                if "/" in canon and " " not in canon:      # Hugging Face id: org/name
                    e = dict(e, org=e.get("org") or canon.split("/", 1)[0])
                ck = norm_key(canon)
                rec = per_cat[cid].setdefault(ck, {"name": canon, "org": e.get("org"), "sources": {}})
                if not rec.get("org") and e.get("org"):
                    rec["org"] = e["org"]
                lic = licence_of(e.get("license"))
                if lic:
                    rec.setdefault("license_seen", lic)
                prev = rec["sources"].get(sid)
                # same source, several sub-boards mapped to one category: keep the best
                if prev is None or n > prev["norm"]:
                    rec["sources"][sid] = {"id": sid, "raw": e["score"], "metric": cat.get("metric", ""), "norm": round(n, 1)}

    n_sources = {cid: len({sid for r in recs.values() for sid in r["sources"]}) for cid, recs in per_cat.items()}
    out_cats = []
    for c in cats_cfg["categories"]:
        recs = []
        for ck, r in per_cat[c["id"]].items():
            f = facts.get(ck) or facts.get(norm_key(r["name"])) or {}
            srcs = list(r["sources"].values())
            score = sum(s["norm"] for s in srcs) / len(srcs)
            if n_sources[c["id"]] > 1:
                # several boards cover this category: pull models seen by few of them toward the middle,
                # so a single board's leader doesn't outrank a model that leads on all of them
                # (only ever downward: a weak model must not be lifted toward the middle)
                score = min(score, (sum(s["norm"] for s in srcs) + PRIOR * PRIOR_WEIGHT) / (len(srcs) + PRIOR_WEIGHT))
            is_open = f.get("open", bool(r.get("license_seen")))
            recs.append({
                "name": display_name(r["name"]), "org": f.get("org") or r.get("org"),
                "open": bool(is_open),
                "license": f.get("license") or r.get("license_seen") if is_open else None,
                "vram_gb": (f.get("vram_gb") or vram_from_name(r["name"])) if is_open else None,
                "vram_note": f.get("vram_note") or ("Estimate from the parameter count in the name, 4-bit" if is_open and vram_from_name(r["name"]) else None),
                "score": round(score, 2), "sources": srcs,
            })
        # mean favours models seen by several boards; break ties by source count
        recs.sort(key=lambda m: (m["score"], len(m["sources"])), reverse=True)
        if recs:
            out_cats.append({"id": c["id"], "name": c["name"], "group": c["group"], "models": keep_models(recs)})

    out = {
        "updated": arena.get("retrieved") or others.get("retrieved"),
        "sources": sorted(sources_out.values(), key=lambda s: s["name"]),
        "categories": out_cats,
    }
    (DATA / "aipex.json").write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"{len(out_cats)} categories, {len(sources_out)} sources")
    if unmapped:
        print("UNMAPPED (add to data/categories.json map):")
        for u in sorted(set(unmapped)):
            print("  ", u)


if __name__ == "__main__":
    main()
