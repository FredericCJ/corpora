# Phase 1 merge: scout JSONs -> merged element set + ambiguity review lists.
import json, re, sys, io, os, difflib
from collections import defaultdict, Counter

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
SCRATCH = os.path.dirname(os.path.abspath(__file__))
SWEEPS = os.path.join(SCRATCH, "sweeps")

# canonical-name priority: catalogs whose names are canonical come first
PRIORITY = ["gof", "posa", "douglass-samek", "nystrom-games", "eip-messaging", "poeaa-ddd",
            "embedded-mech", "concurrency", "lockfree-mem", "dsa-blocks", "db-internals",
            "idioms", "functional", "resilience", "parsing-serial", "os-network",
            "ui-reactive", "wiki-longtail", "corpus-seed", "gap"]
CONF_RANK = {"established": 0, "spot-checked": 1, "needs-check": 2}
AXES = {"data-representation","data-flow-buffering","execution-concurrency","state-management",
        "resource-management","error-handling","communication","oo-patterns","data-structures",
        "embedded-systems","caching-memoization","synchronization-coordination","scheduling-time",
        "parsing-text","serialization-framing","persistence-durability","numeric-precision",
        "construction-api","functional-type-idioms","robustness-security"}

STOP_SUFFIX = {"pattern", "idiom", "mechanism"}

def norm(s):
    s = s.lower().strip()
    s = re.sub(r"[^a-z0-9]+", " ", s).strip()
    toks = [t for t in s.split() if t]
    if toks and toks[0] == "the":
        toks = toks[1:]
    if len(toks) > 1 and toks[-1] in STOP_SUFFIX:
        toks = toks[:-1]
    # light plural fold on last token
    if toks and len(toks[-1]) > 3 and toks[-1].endswith("s") and not toks[-1].endswith("ss"):
        toks = toks[:-1] + [toks[-1][:-1]]
    return " ".join(toks)

def prio(scout):
    return PRIORITY.index(scout) if scout in PRIORITY else len(PRIORITY)

def load_scouts():
    entries, parked, excluded, notes = [], [], [], {}
    for fn in sorted(os.listdir(SWEEPS)):
        if not (fn.startswith("scout-") and fn.endswith(".json")):
            continue
        with open(os.path.join(SWEEPS, fn), encoding="utf-8") as f:
            d = json.load(f)
        scout = d.get("scout", fn[6:-5])
        for e in d.get("elements", []):
            e["_scout"] = scout
            entries.append(e)
        for p in d.get("parked_architecture", []) or []:
            p["_scout"] = scout
            parked.append(p)
        for x in d.get("excluded_notable", []) or []:
            x["_scout"] = scout
            excluded.append(x)
        if d.get("notes"):
            notes[scout] = d["notes"]
    return entries, parked, excluded, notes

class UF:
    def __init__(self):
        self.p = {}
    def find(self, x):
        self.p.setdefault(x, x)
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x
    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.p[rb] = ra

def cluster(entries):
    uf = UF()
    key_owner = {}          # normalized alias -> first entry index (representative key)
    for i, e in enumerate(entries):
        keys = {norm(e.get("name", ""))}
        for a in e.get("aka", []) or []:
            k = norm(a)
            if k:
                keys.add(k)
        keys.discard("")
        e["_keys"] = keys
        anchor = f"e{i}"
        uf.find(anchor)
        for k in keys:
            if k in key_owner:
                uf.union(key_owner[k], anchor)
            else:
                key_owner[k] = anchor
    groups = defaultdict(list)
    for i, e in enumerate(entries):
        groups[uf.find(f"e{i}")].append(e)
    return list(groups.values())

def merge_group(g):
    g = sorted(g, key=lambda e: (prio(e["_scout"]), CONF_RANK.get(e.get("confidence", "needs-check"), 2)))
    top = g[0]
    name = top.get("name", "").strip()
    akas, tags, sources, corpus_ids, scouts = [], [], [], [], []
    seen_aka = {norm(name)}
    for e in g:
        scouts.append(e["_scout"])
        for a in [e.get("name", "")] + (e.get("aka") or []):
            k = norm(a)
            if k and k not in seen_aka:
                seen_aka.add(k)
                akas.append(a.strip())
        for t in e.get("tags") or []:
            if t and t not in tags:
                tags.append(t)
        ni = (e.get("named_in") or "").strip()
        if ni and ni not in [s[0] for s in sources]:
            sources.append((ni, e.get("named_in_corpus_id")))
        cid = e.get("named_in_corpus_id")
        if cid and cid not in corpus_ids:
            corpus_ids.append(cid)
    kinds = Counter(e.get("kind", "") for e in g)
    kind = kinds.most_common(1)[0][0]
    if kinds[kind] == 1 and len(kinds) > 1:
        kind = top.get("kind", kind)
    # naming source: prefer one with a corpus id, else top-priority entry's
    named = None
    for e in g:
        if e.get("named_in_corpus_id"):
            named = (e["named_in"], e["named_in_corpus_id"])
            break
    if not named:
        named = (top.get("named_in", ""), None)
    borderline = next((e.get("borderline") for e in g if e.get("borderline")), None)
    conf = min((CONF_RANK.get(e.get("confidence", "needs-check"), 2) for e in g))
    conf = {v: k for k, v in CONF_RANK.items()}[conf]
    return {
        "id": re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-"),
        "name": name,
        "aka": akas,
        "kind": kind,
        "what": top.get("what", ""),
        "problem": top.get("problem", ""),
        "named_in": named[0],
        "named_in_corpus_id": named[1],
        "tags": tags,
        "borderline": borderline,
        "confidence": conf,
        "scouts": sorted(set(scouts)),
        "kind_votes": dict(kinds),
        "sources_all": [{"src": s, "corpus_id": c} for s, c in sources],
    }

def near_misses(merged):
    """clusters whose canonical names look similar but were not aka-linked"""
    out = []
    names = [(m["id"], norm(m["name"]), m) for m in merged]
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            a, b = names[i], names[j]
            if not a[1] or not b[1]:
                continue
            ta, tb = set(a[1].split()), set(b[1].split())
            ratio = difflib.SequenceMatcher(None, a[1], b[1]).ratio()
            subset = (ta and tb) and (ta <= tb or tb <= ta)
            if ratio >= 0.86 or (subset and abs(len(ta) - len(tb)) <= 1):
                out.append({"a": a[0], "b": b[0], "a_name": a[2]["name"], "b_name": b[2]["name"],
                            "a_kind": a[2]["kind"], "b_kind": b[2]["kind"],
                            "a_what": a[2]["what"], "b_what": b[2]["what"],
                            "ratio": round(ratio, 2)})
    return out

def main():
    entries, parked, excluded, notes = load_scouts()
    groups = cluster(entries)
    merged = [merge_group(g) for g in groups]
    # id uniqueness + collision with corpus work ids
    ids = Counter(m["id"] for m in merged)
    dup_ids = [i for i, c in ids.items() if c > 1]
    for m in merged:
        if ids[m["id"]] > 1:
            m["id"] = m["id"] + "-" + m["kind"].split("-")[0]
    work_ids = set()
    with open(os.path.join(SCRATCH, "work_ids.tsv"), encoding="utf-8") as f:
        for line in f:
            work_ids.add(line.split("\t")[0])
    collisions = [m["id"] for m in merged if m["id"] in work_ids]
    merged.sort(key=lambda m: (m["kind"], m["id"]))

    bad_kind = [{"id": m["id"], "kind": m["kind"]} for m in merged
                if m["kind"] not in AXES and not m["kind"].startswith("proposed:")]
    multi_kind = [{"id": m["id"], "votes": m["kind_votes"]} for m in merged if len(m["kind_votes"]) > 1]

    with open(os.path.join(SCRATCH, "merged_design.json"), "w", encoding="utf-8") as f:
        json.dump({"elements": merged, "parked_architecture": parked,
                   "excluded_notable": excluded, "scout_notes": notes}, f, ensure_ascii=False, indent=1)
    review = {"near_misses": near_misses(merged), "multi_kind": multi_kind,
              "bad_kind": bad_kind, "dup_ids_renamed": dup_ids, "work_id_collisions": collisions}
    with open(os.path.join(SCRATCH, "review_design.json"), "w", encoding="utf-8") as f:
        json.dump(review, f, ensure_ascii=False, indent=1)

    print(f"raw entries: {len(entries)}  -> merged: {len(merged)}")
    print(f"parked: {len(parked)}  excluded_notable: {len(excluded)}")
    print("confidence:", dict(Counter(m['confidence'] for m in merged)))
    print("per-axis:")
    for k, c in sorted(Counter(m["kind"] for m in merged).items()):
        print(f"  {k}: {c}")
    print(f"near_misses: {len(review['near_misses'])}  multi_kind: {len(multi_kind)}  bad_kind: {len(bad_kind)}")
    print(f"dup ids renamed: {dup_ids}  work-id collisions: {collisions}")

if __name__ == "__main__":
    main()
