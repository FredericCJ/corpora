# Phase 3a merge: arch scout JSONs -> merged architecture element set + reviews + parked-intake audit.
import json, io, sys, os, re, difflib
from collections import defaultdict, Counter
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
SCRATCH = os.path.dirname(os.path.abspath(__file__))
SW = os.path.join(SCRATCH, "p3", "sweeps")

PRIORITY = ["arch-posa1-styles", "arch-bass-tactics", "arch-shaw-garlan-tmd", "arch-description-42010",
            "arch-embedded-refarch", "arch-distributed-enterprise", "arch-quality-deployment", "arch-parked-intake"]
CONF = {"established": 0, "spot-checked": 1, "needs-check": 2}
KINDS = {"style", "pattern", "tactic", "connector", "deployment", "reference-architecture", "description"}

def norm(s):
    s = re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()
    toks = [t for t in s.split() if t and t != "the"]
    if len(toks) > 1 and toks[-1] in ("pattern", "style", "architecture", "tactic"):
        toks = toks[:-1]
    if toks and len(toks[-1]) > 3 and toks[-1].endswith("s") and not toks[-1].endswith("ss"):
        toks = toks[:-1] + [toks[-1][:-1]]
    return " ".join(toks)

def prio(s):
    return PRIORITY.index(s) if s in PRIORITY else len(PRIORITY)

entries, rejected = [], []
for fn in sorted(os.listdir(SW)):
    if not fn.endswith(".json"):
        continue
    d = json.load(open(os.path.join(SW, fn), encoding="utf-8"))
    sc = d.get("scout", fn[:-5])
    for e in d.get("elements", []):
        if isinstance(e.get("aka"), str):
            e["aka"] = [a.strip() for a in e["aka"].split(",") if a.strip() and a.strip() != "—"]
        e["aka"] = [a for a in (e.get("aka") or []) if norm(a)]
        e["_scout"] = sc
        entries.append(e)
    for r in d.get("rejected", []) or []:
        r["_scout"] = sc
        rejected.append(r)

class UF:
    def __init__(self): self.p = {}
    def find(self, x):
        self.p.setdefault(x, x)
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]; x = self.p[x]
        return x
    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb: self.p[rb] = ra

uf, owner = UF(), {}
for i, e in enumerate(entries):
    keys = {norm(e["name"])} | {norm(a) for a in e["aka"]}
    keys.discard("")
    a0 = f"e{i}"
    uf.find(a0)
    for k in keys:
        if k in owner: uf.union(owner[k], a0)
        else: owner[k] = a0
groups = defaultdict(list)
for i, e in enumerate(entries):
    groups[uf.find(f"e{i}")].append(e)

merged = []
for g in groups.values():
    g = sorted(g, key=lambda e: (prio(e["_scout"]), CONF.get(e.get("confidence", "needs-check"), 2)))
    top = g[0]
    name = top["name"].strip()
    seen = {norm(name)}
    akas, tags, scouts, sources = [], [], [], []
    for e in g:
        scouts.append(e["_scout"])
        for a in [e["name"]] + e["aka"]:
            if norm(a) not in seen:
                seen.add(norm(a)); akas.append(a.strip())
        for t in e.get("tags") or []:
            if t not in tags: tags.append(t)
        s = (e.get("named_in") or "").strip()
        if s and s not in [x["src"] for x in sources]:
            sources.append({"src": s, "corpus_id": e.get("named_in_corpus_id")})
    kinds = Counter(e.get("kind", "") for e in g)
    kind = kinds.most_common(1)[0][0] if kinds[kinds.most_common(1)[0][0]] > 1 or len(kinds) == 1 else top.get("kind")
    named = next((s for s in sources if s["corpus_id"]), sources[0] if sources else {"src": "", "corpus_id": None})
    merged.append({
        "id": re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-"),
        "name": name, "aka": akas, "kind": kind, "realm": "architecture",
        "what": top.get("what", ""), "problem": top.get("problem", ""),
        "named_in": named["src"], "named_in_corpus_id": named["corpus_id"],
        "tags": tags, "borderline": next((e.get("borderline") for e in g if e.get("borderline")), None),
        "confidence": {v: k for k, v in CONF.items()}[min(CONF.get(e.get("confidence", "needs-check"), 2) for e in g)],
        "scouts": sorted(set(scouts)), "kind_votes": dict(kinds), "sources_all": sources,
    })

# ---- id uniqueness across ALL namespaces
design = json.load(open(os.path.join(SCRATCH, "merged_design.json"), encoding="utf-8"))["elements"]
design_ids = {e["id"] for e in design}
design_names = {norm(e["name"]): e["id"] for e in design}
for e in design:
    for a in e.get("aka", []):
        design_names.setdefault(norm(a), e["id"])
work_ids = {l.split("\t")[0] for l in open(os.path.join(SCRATCH, "work_ids.tsv"), encoding="utf-8")}
p8_ids = {l.split("\t")[0] for l in open(os.path.join(SCRATCH, "pass8_ids.tsv"), encoding="utf-8")}
SUFF = {"style": "-style", "pattern": "-pattern", "tactic": "-tactic", "connector": "-connector",
        "deployment": "-deployment", "reference-architecture": "-refarch", "description": "-view"}
taken = set(design_ids) | work_ids | p8_ids
renamed = []
merged.sort(key=lambda m: (m["kind"], m["id"]))
for m in merged:
    if m["id"] in taken:
        old = m["id"]
        m["id"] = m["id"] + SUFF.get(m["kind"], "-arch")
        n = 2
        while m["id"] in taken:
            m["id"] = old + SUFF.get(m["kind"], "-arch") + str(n); n += 1
        renamed.append((old, m["id"]))
    taken.add(m["id"])
dups = [i for i, c in Counter(m["id"] for m in merged).items() if c > 1]

# ---- same-name-two-realms report
shared = sorted({m["id"] for m in merged if norm(m["name"]) in design_names} |
                {m["id"] for m in merged for a in m["aka"] if norm(a) in design_names})

# ---- parked-intake audit: all 203 accounted for?
parked = json.load(open(os.path.join(SCRATCH, "p3", "parked.json"), encoding="utf-8"))["parked"]
mkeys = set()
for m in merged:
    mkeys |= {norm(m["name"])} | {norm(a) for a in m["aka"]}
rkeys = {norm(r.get("name", "")) for r in rejected}
unaccounted = []
for p in parked:
    k = norm(p["name"])
    ktoks = set(k.split())
    hit = (k in mkeys or k in rkeys or
           any(ktoks and (ktoks <= set(mk.split()) or set(mk.split()) <= ktoks) for mk in mkeys if mk) or
           any(difflib.SequenceMatcher(None, k, rk).ratio() > 0.8 for rk in rkeys if rk))
    if not hit:
        unaccounted.append(p["name"])

# ---- near-miss review
names = [(m["id"], norm(m["name"]), m["kind"]) for m in merged]
nm = []
for i in range(len(names)):
    for j in range(i + 1, len(names)):
        a, b = names[i], names[j]
        r = difflib.SequenceMatcher(None, a[1], b[1]).ratio()
        ta, tb = set(a[1].split()), set(b[1].split())
        if r >= 0.87 or (ta and tb and (ta <= tb or tb <= ta) and abs(len(ta) - len(tb)) <= 1):
            nm.append((round(r, 2), a[0], b[0], a[2], b[2]))

json.dump({"elements": merged, "rejected": rejected},
          open(os.path.join(SCRATCH, "merged_arch.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump({"near_misses": nm, "renamed": renamed, "dup_ids": dups,
           "multi_kind": [{"id": m["id"], "votes": m["kind_votes"]} for m in merged if len(m["kind_votes"]) > 1],
           "bad_kind": [m["id"] for m in merged if m["kind"] not in KINDS],
           "shared_names_with_design": shared, "parked_unaccounted": unaccounted},
          open(os.path.join(SCRATCH, "review_arch.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

print(f"raw {len(entries)} -> merged {len(merged)} architecture elements; rejected records: {len(rejected)}")
print("per-kind:", dict(sorted(Counter(m['kind'] for m in merged).items())))
print("confidence:", dict(Counter(m['confidence'] for m in merged)))
print(f"renamed for cross-namespace collisions: {len(renamed)}: {renamed[:12]}")
print(f"dup ids: {dups}")
print(f"bad kinds: {[m['id'] for m in merged if m['kind'] not in KINDS][:10]}")
print(f"shared names with design realm (same-name-two-realms): {len(shared)}: {shared[:15]}")
print(f"parked candidates unaccounted for: {len(unaccounted)}: {unaccounted[:15]}")
print(f"near-misses to review: {len(nm)}")
for x in nm[:25]:
    print("  ", x)
