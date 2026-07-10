# Phase 2 assembly: p2out/*.json -> deduped pass-8 work set + reachability audit.
import json, io, sys, os, re
from collections import Counter, defaultdict
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
SCRATCH = os.path.dirname(os.path.abspath(__file__))

def tkey(title):
    t = re.sub(r"[^a-z0-9 ]", "", title.lower())
    t = re.sub(r"\b(the|a|an|of|for|and|in|to|on|with|vol|volume|ed|edition|2nd|3rd|4th|1st)\b", " ", t)
    return re.sub(r"\s+", " ", t).strip()[:60]

ROLE_RANK = {"anchor": 0, "core": 1, "advanced": 2, "survey": 3}
VER_RANK = {"verified": 0, "unverified": 1}

with open(os.path.join(SCRATCH, "merged_design.json"), encoding="utf-8") as f:
    ELEMENTS = {e["id"] for e in json.load(f)["elements"]}
WORK_IDS = {l.split("\t")[0] for l in open(os.path.join(SCRATCH, "work_ids.tsv"), encoding="utf-8")}

by_key = {}
route_notes, route_gaps = {}, []
for fn in sorted(os.listdir(os.path.join(SCRATCH, "p2out"))):
    if not fn.endswith(".json"):
        continue
    d = json.load(open(os.path.join(SCRATCH, "p2out", fn), encoding="utf-8"))
    route = d["route"]
    route_notes[route] = d.get("notes", "")
    for g in d.get("gaps", []):
        g["route"] = route
        route_gaps.append(g)
    for w in d.get("works", []):
        w["routes"] = [route]
        w["elements"] = [e for e in (w.get("elements") or [])]
        key = w["id"] if w["action"] == "membership" else ("t:" + tkey(w["title"]))
        if key in by_key:
            h = by_key[key]
            h["elements"] = sorted(set(h["elements"]) | set(w["elements"]))
            h["routes"] = sorted(set(h["routes"] + [route]))
            if ROLE_RANK.get(w.get("role", "core"), 1) < ROLE_RANK.get(h.get("role", "core"), 1):
                h["role"] = w["role"]
            if VER_RANK.get(w.get("verification"), 1) < VER_RANK.get(h.get("verification"), 1):
                for f2 in ("title", "authors", "year", "venue", "ident", "type", "verification", "unresolved", "note"):
                    if w.get(f2) is not None:
                        h[f2] = w[f2]
            if h.get("action") == "new" and w["action"] == "membership":
                h["action"], h["id"] = "membership", w["id"]
        else:
            by_key[key] = w

works = list(by_key.values())
# id checks for new works
used = set(WORK_IDS)
renames = []
for w in works:
    if w["action"] == "membership":
        if w["id"] not in WORK_IDS:
            renames.append(("MEMBERSHIP-ID-UNKNOWN", w["id"], w["title"][:50]))
        continue
    wid = re.sub(r"[^a-z0-9]", "", w["id"].lower()) or tkey(w["title"]).replace(" ", "")[:16]
    base = wid
    n = 2
    while wid in used or wid in ELEMENTS:
        wid = f"{base}{n}"
        n += 1
    if wid != w["id"]:
        renames.append(("RENAMED", w["id"], wid))
    w["id"] = wid
    used.add(wid)

# element coverage / bogus element ids
covered = defaultdict(list)
bogus = []
for w in works:
    for e in w["elements"]:
        if e in ELEMENTS:
            covered[e].append(w["id"])
        else:
            bogus.append((w["id"], e))
uncovered = sorted(ELEMENTS - set(covered))
gap_ids = {g["element"] for g in route_gaps}

out = {"works": sorted(works, key=lambda w: (w["routes"][0], w["action"], w["id"])),
       "route_notes": route_notes, "route_gaps": route_gaps,
       "uncovered": uncovered}
json.dump(out, open(os.path.join(SCRATCH, "pass8_works.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

n_m = sum(1 for w in works if w["action"] == "membership")
n_n = len(works) - n_m
n_v = sum(1 for w in works if w.get("verification") == "verified")
print(f"works: {len(works)} = {n_m} memberships + {n_n} new | verified {n_v} / unverified {len(works)-n_v-n_m} (memberships excluded from verification need)")
print(f"membership-id problems: {[r for r in renames if r[0]=='MEMBERSHIP-ID-UNKNOWN']}")
print(f"new-id renames: {[(a,b) for t,a,b in renames if t=='RENAMED']}")
print(f"bogus element ids in coverage lists: {len(bogus)}: {bogus[:10]}")
print(f"elements covered: {len(covered)}/{len(ELEMENTS)}; uncovered: {len(uncovered)}")
print("uncovered sample:", uncovered[:20])
print(f"declared route gaps: {len(route_gaps)}; declared-but-actually-covered: {sorted(gap_ids & set(covered))[:10]}")
cov_counts = Counter(len(v) for v in covered.values())
print("coverage multiplicity histogram:", dict(sorted(cov_counts.items())))
