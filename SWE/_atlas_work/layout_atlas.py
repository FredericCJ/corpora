# WS2 layout precompute: deterministic geography for the atlas. Reads islands.json (structure) +
# island_names.json (semantic names) + bridge_v1_1.json, computes STABLE seeded coordinates (no RNG):
#   - L0 meta-graph (islands as bubbles) via seeded Fruchterman-Reingold on the route graph
#   - L1 per-island radial layout (hub centre, members on degree rings)
#   - L1 convex hull per island (for the tinted coastline)
# Emits explorer/build/element_src/atlas.json (the canonical WS2 deliverable). No Math.random anywhere:
# every seed derives from md5(id), fixed iteration counts -> byte-identical across builds.
import json, os, io, sys, hashlib, math
from collections import defaultdict
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.normpath(os.path.join(ROOT, "..", "explorer", "build", "element_src"))

FAMILIES = [
 {"id": "concurrency",   "name": "Concurrency & Coordination",     "hex": "#0072B2"},
 {"id": "data",          "name": "Data & Storage",                 "hex": "#009E73"},
 {"id": "communication", "name": "Communication & Distribution",   "hex": "#56B4E9"},
 {"id": "structure",     "name": "Structure & Creation",           "hex": "#CC79A7"},
 {"id": "reliability",   "name": "Reliability & Safety",           "hex": "#D55E00"},
 {"id": "resource",      "name": "Resource & Runtime",             "hex": "#E69F00"},
 {"id": "foundations",   "name": "Foundations & Types",            "hex": "#949494"},
]

D = json.load(open(os.path.join(SRC, "design.json"), encoding="utf-8"))["elements"]
A = json.load(open(os.path.join(SRC, "architecture.json"), encoding="utf-8"))["elements"]
BR = json.load(open(os.path.join(ROOT, "bridge_v1_1.json"), encoding="utf-8"))
ISL = json.load(open(os.path.join(ROOT, "islands.json"), encoding="utf-8"))
try:
    NAMES = json.load(open(os.path.join(ROOT, "island_names.json"), encoding="utf-8"))
except OSError:
    NAMES = {}
meta = {e["id"]: e for e in D}; meta.update({e["id"]: e for e in A})
realm = {e["id"]: "design" for e in D}; realm.update({e["id"]: "architecture" for e in A})

def h01(s, salt=""):
    """Deterministic pseudo-random in [0,1) from an id (stable across runs/OS)."""
    return (int(hashlib.md5((salt + s).encode("utf-8")).hexdigest(), 16) % 1000000) / 1000000.0

# adjacency (all edges, undirected) for degree + island-local layout
adj = defaultdict(set)
for e in BR["edges"]:
    if e["from"] != e["to"]:
        adj[e["from"]].add(e["to"]); adj[e["to"]].add(e["from"])

islands = ISL["islands"]; routes = ISL["routes"]
idset = {i["id"] for i in islands}

# ---- L0: seeded Fruchterman-Reingold on the meta-graph (islands + routes) ----
pos = {i["id"]: [h01(i["id"], "x"), h01(i["id"], "y")] for i in islands}
route_w = {(r["from"], r["to"]): r["weight"] for r in routes}
n = len(islands); area = 1.0
k = math.sqrt(area / max(1, n)) * 1.4
temp = 0.12; ITERS = 400
ids = [i["id"] for i in islands]
size = {i["id"]: i["size"] for i in islands}
for it in range(ITERS):
    disp = {i: [0.0, 0.0] for i in ids}
    for a in range(n):
        for b in range(a + 1, n):
            ia, ib = ids[a], ids[b]
            dx = pos[ia][0] - pos[ib][0]; dy = pos[ia][1] - pos[ib][1]
            d = math.hypot(dx, dy) or 1e-4
            f = k * k / d                                  # repulsion
            ux, uy = dx / d, dy / d
            disp[ia][0] += ux * f; disp[ia][1] += uy * f
            disp[ib][0] -= ux * f; disp[ib][1] -= uy * f
    for (fa, fb), w in route_w.items():
        dx = pos[fa][0] - pos[fb][0]; dy = pos[fa][1] - pos[fb][1]
        d = math.hypot(dx, dy) or 1e-4
        f = d * d / k * (0.5 + 0.08 * math.log1p(w))       # attraction, gentle weight scaling
        ux, uy = dx / d, dy / d
        disp[fa][0] -= ux * f; disp[fa][1] -= uy * f
        disp[fb][0] += ux * f; disp[fb][1] += uy * f
    for i in ids:
        dx, dy = disp[i]; dl = math.hypot(dx, dy) or 1e-4
        pos[i][0] += dx / dl * min(dl, temp); pos[i][1] += dy / dl * min(dl, temp)
    temp = max(0.008, temp * 0.985)
# normalize to [0.06,0.94]
xs = [p[0] for p in pos.values()]; ys = [p[1] for p in pos.values()]
x0, x1 = min(xs), max(xs); y0, y1 = min(ys), max(ys)
def nx(v): return 0.06 + 0.88 * (v - x0) / ((x1 - x0) or 1)
def ny(v): return 0.06 + 0.88 * (v - y0) / ((y1 - y0) or 1)
maxsize = max(size.values())
for i in islands:
    p = pos[i["id"]]
    i["cx"] = nx(p[0]); i["cy"] = ny(p[1])
    i["r"] = 0.03 + 0.06 * math.sqrt(size[i["id"]] / maxsize)
# collision relaxation: nudge overlapping island bubbles apart so the map reads cleanly
# (deterministic: fixed passes, id-ordered pairs, no RNG)
MARG = 0.012
for _ in range(250):
    moved = False
    for a in range(n):
        for b in range(a + 1, n):
            ia, ib = islands[a], islands[b]
            dx = ia["cx"] - ib["cx"]; dy = ia["cy"] - ib["cy"]
            dd = math.hypot(dx, dy) or 1e-4
            need = ia["r"] + ib["r"] + MARG
            if dd < need:
                push = (need - dd) / 2.0; ux, uy = dx / dd, dy / dd
                ia["cx"] += ux * push; ia["cy"] += uy * push
                ib["cx"] -= ux * push; ib["cy"] -= uy * push
                moved = True
    if not moved: break
for i in islands:
    i["cx"] = round(min(0.98 - i["r"], max(0.02 + i["r"], i["cx"])), 4)
    i["cy"] = round(min(0.98 - i["r"], max(0.02 + i["r"], i["cy"])), 4)
    i["r"] = round(i["r"], 4)

# ---- L1: per-island radial layout (hub centre; members on rings by within-island degree) ----
def convex_hull(pts):
    pts = sorted(set(pts))
    if len(pts) <= 2: return pts
    def cross(o, a, b): return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])
    lo = []
    for p in pts:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 0: lo.pop()
        lo.append(p)
    up = []
    for p in reversed(pts):
        while len(up) >= 2 and cross(up[-2], up[-1], p) <= 0: up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]

for isl in islands:
    members = isl["members"]; mset = set(members); hub = isl["hub"]
    wdeg = {m: sum(1 for nb in adj[m] if nb in mset) for m in members}
    others = [m for m in members if m != hub]
    others.sort(key=lambda m: (-wdeg[m], m))          # high-degree inner
    placed = {hub: (0.5, 0.5)}
    R = len(others)
    rings = max(1, math.ceil(math.sqrt(R / 2.0)))     # ~even ring fill
    per = math.ceil(R / rings) if R else 1
    pmax = 0.44
    for idx, m in enumerate(others):
        ring = idx // per                             # 0..rings-1
        rank = idx % per
        rad = pmax * (ring + 1) / rings
        ang = 2 * math.pi * (rank / per) + 2 * math.pi * h01(m, "a") * 0.12 + ring * 0.6
        placed[m] = (0.5 + rad * math.cos(ang), 0.5 + rad * math.sin(ang))
    mem_out = []
    for m in members:
        x, y = placed[m]
        mem_out.append({"id": m, "name": meta[m]["name"], "realm": realm[m], "kind": meta[m]["kind"],
                        "family": None, "x": round(x, 4), "y": round(y, 4), "deg": wdeg[m]})
    isl["hull"] = [[round(x, 4), round(y, 4)] for x, y in convex_hull([(mm["x"], mm["y"]) for mm in mem_out])]
    isl["members_xy"] = mem_out
    isl["name"] = NAMES.get(isl["id"], {}).get("name") or isl.get("name") or isl["id"]
    isl["blurb"] = NAMES.get(isl["id"], {}).get("blurb", "")
    if isl["id"] in NAMES and NAMES[isl["id"]].get("family"):
        isl["family"] = NAMES[isl["id"]]["family"]

# ---- family per member (for colouring within L1) ----
sys.path.insert(0, ROOT)
from families import family_of
for isl in islands:
    for mm in isl["members_xy"]:
        mm["family"] = family_of(mm["id"])

# ---- Bridge-Flow (view 11): design families (left) -> architecture anchors (right) ----
CROSS = {"realizes", "enables"}
anchor_in = defaultdict(lambda: defaultdict(int))   # arch anchor -> family -> count
for e in BR["edges"]:
    if e["kind"] in CROSS and realm.get(e["from"]) == "design" and realm.get(e["to"]) == "architecture":
        anchor_in[e["to"]][family_of(e["from"])] += 1
anchor_tot = {a: sum(f.values()) for a, f in anchor_in.items()}
top_anchors = sorted(anchor_tot, key=lambda a: -anchor_tot[a])[:40]
flows = []
for a in top_anchors:
    for fam, ct in anchor_in[a].items():
        flows.append({"from": fam, "to": a, "weight": ct})
bridge_flow = {
 "families": FAMILIES,
 "anchors": [{"id": a, "name": meta[a]["name"], "kind": meta[a]["kind"], "total": anchor_tot[a]} for a in top_anchors],
 "flows": flows,
}

# ---- assemble atlas.json ----
out_islands = []
for isl in islands:
    out_islands.append({
        "id": isl["id"], "name": isl["name"], "blurb": isl.get("blurb", ""),
        "family": isl["family"], "size": isl["size"],
        "hub": isl["hub"], "representatives": isl["representatives"],
        "cohesion": round(isl["internal_edges"] / max(1, isl["size"]), 2),
        "cx": isl["cx"], "cy": isl["cy"], "r": isl["r"], "hull": isl["hull"],
        "members": isl["members_xy"], "neighbours": isl["neighbours"],
        "top_kinds": isl["top_kinds"], "realm_split": isl["realm_split"],
    })
atlas = {
 "meta": {"atlas": "archipelago", "islandCount": len(islands),
          "elementCount": sum(i["size"] for i in islands), "edgeCount": len(BR["edges"]),
          "families": FAMILIES},
 "islands": out_islands, "routes": routes, "bridgeFlow": bridge_flow,
}
OUT = os.path.join(SRC, "atlas.json")
json.dump(atlas, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"wrote {OUT}")
print(f"  {len(islands)} islands, {len(routes)} routes, {len(top_anchors)} bridge-flow anchors")
print(f"  elements placed: {atlas['meta']['elementCount']}/{len(meta)}")
print(f"  L0 bubble spread: x[{min(i['cx'] for i in out_islands):.2f},{max(i['cx'] for i in out_islands):.2f}] "
      f"y[{min(i['cy'] for i in out_islands):.2f},{max(i['cy'] for i in out_islands):.2f}]")
