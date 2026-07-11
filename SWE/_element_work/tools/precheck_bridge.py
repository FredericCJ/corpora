import json, io, sys, os
from collections import Counter
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
SCRATCH = os.path.dirname(os.path.abspath(__file__))
os.chdir(SCRATCH)

design = {e["id"] for e in json.load(open("merged_design.json", encoding="utf-8"))["elements"]}
arch = {e["id"] for e in json.load(open("merged_arch.json", encoding="utf-8"))["elements"]}
CROSS = {"realizes", "enables"}; CROSS_REV = {"constrains"}
WITHIN = {"specializes", "composes-with", "alternative-to"}; IMPL = {"implements"}

bad_targets = Counter()
per_group = {}
for fn in sorted(os.listdir("p3bridge")):
    if not fn.endswith(".json"): continue
    d = json.load(open(os.path.join("p3bridge", fn), encoding="utf-8"))
    g = d.get("group", fn[:-5]); bad = []
    for e in d.get("edges", []):
        f, k, t = e.get("from"), e.get("kind"), e.get("to")
        ok = True
        if k in CROSS: ok = f in design and t in arch
        elif k in CROSS_REV: ok = f in arch and t in design
        elif k in IMPL: ok = f in design and t in design and f != t
        elif k in WITHIN: ok = ((f in design and t in design) or (f in arch and t in arch)) and f != t
        else: ok = False
        if not ok:
            bad.append((f, k, t))
            for x in (f, t):
                if x not in design and x not in arch: bad_targets[x] += 1
    per_group[g] = (len(d.get("edges", [])), len(bad), bad[:4])
for g in sorted(per_group):
    n, nb, sample = per_group[g]
    flag = "" if nb == 0 else f"  <-- {nb} INVALID"
    print(f"{g}: {n} edges, {nb} invalid{flag}")
    for s in sample: print("     bad:", s)
print("\nunknown ids referenced (not in either realm):", dict(bad_targets.most_common(20)))
