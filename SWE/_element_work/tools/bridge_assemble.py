# Phase 3b assembly: p3bridge/*.json -> validated edge set + mechanical bridging audit + emit.
import json, io, sys, os
from collections import Counter, defaultdict
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
SCRATCH = os.path.dirname(os.path.abspath(__file__))

CROSS = {"realizes", "enables"}          # design -> architecture
CROSS_REV = {"constrains"}               # architecture -> design
WITHIN = {"specializes", "composes-with", "alternative-to"}
IMPL = {"implements"}                    # design -> design (idiom realizes element)
ALL_KINDS = CROSS | CROSS_REV | WITHIN | IMPL

design = {e["id"] for e in json.load(open(os.path.join(SCRATCH, "merged_design.json"), encoding="utf-8"))["elements"]}
arch = {e["id"] for e in json.load(open(os.path.join(SCRATCH, "merged_arch.json"), encoding="utf-8"))["elements"]}

edges, unbridged, bad = [], [], []
seen = set()
for fn in sorted(os.listdir(os.path.join(SCRATCH, "p3bridge"))):
    if not fn.endswith(".json"):
        continue
    d = json.load(open(os.path.join(SCRATCH, "p3bridge", fn), encoding="utf-8"))
    grp = d.get("group", fn[:-5])
    for e in d.get("edges", []):
        f, k, t = e.get("from", ""), e.get("kind", ""), e.get("to", "")
        prov = e.get("provenance", "editorial")
        key = (f, k, t)
        if key in seen:
            continue
        ok = k in ALL_KINDS and prov in ("sourced", "editorial")
        if k in CROSS:
            ok = ok and f in design and t in arch
        elif k in CROSS_REV:
            ok = ok and f in arch and t in design
        elif k in IMPL:
            ok = ok and f in design and t in design and f != t
        elif k in WITHIN:
            ok = ok and ((f in design and t in design) or (f in arch and t in arch)) and f != t
        if prov == "sourced" and not (e.get("cite") or "").strip():
            ok = False
        if not ok:
            bad.append({"group": grp, **e})
            continue
        seen.add(key)
        edges.append({"from": f, "kind": k, "to": t, "provenance": prov,
                      "cite": (e.get("cite") or "").strip() or None,
                      "note": (e.get("note") or "").strip(), "group": grp})
    for u in d.get("unbridged", []) or []:
        u["group"] = grp
        unbridged.append(u)

bridged = {e["from"] for e in edges if e["kind"] in CROSS} | {e["to"] for e in edges if e["kind"] in CROSS_REV}
unbridged_ids = {u.get("id") for u in unbridged}
missing = sorted(design - bridged - unbridged_ids)          # neither bridged nor declared
false_unbridged = sorted(unbridged_ids & bridged)           # declared unbridged but has an edge
kc = Counter(e["kind"] for e in edges)
pc = Counter(e["provenance"] for e in edges)

json.dump({"edges": edges, "unbridged": unbridged}, open(os.path.join(SCRATCH, "bridge.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
json.dump(bad, open(os.path.join(SCRATCH, "bridge_rejected.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump({"missing": missing, "false_unbridged": false_unbridged},
          open(os.path.join(SCRATCH, "bridge_missing.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"edges kept: {len(edges)}  rejected malformed: {len(bad)}")
print("by kind:", dict(sorted(kc.items())))
print("provenance:", dict(pc), f" sourced ratio: {pc.get('sourced',0)/max(1,len(edges)):.0%}")
print(f"bridging rule: {len(bridged)}/{len(design)} design elements have >=1 cross-realm edge")
print(f"declared unbridged: {len(unbridged_ids)}  |  false-unbridged (declared but bridged): {false_unbridged[:10]}")
print(f"MISSING (neither bridged nor declared): {len(missing)}: {missing[:25]}")
if bad[:8]:
    print("sample rejects:", json.dumps(bad[:8], ensure_ascii=False)[:800])
