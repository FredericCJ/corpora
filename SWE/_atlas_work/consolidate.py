# WS2 §2.3 consolidation (graph part): deterministic Louvain over the enriched graph (all edges — islands
# span realms via bridge edges, so a topic island = a design cluster + the architecture it realizes),
# then curation (merge tiny, cap to 15-25), family assignment, hub, representatives, neighbours.
# Emits _atlas_work/islands.json (structure; NO names, NO coords). Naming + layout are later steps.
import json, os, io, sys, hashlib
from collections import Counter, defaultdict
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.normpath(os.path.join(ROOT, "..", "explorer", "build", "element_src"))

D = json.load(open(os.path.join(SRC, "design.json"), encoding="utf-8"))["elements"]
A = json.load(open(os.path.join(SRC, "architecture.json"), encoding="utf-8"))["elements"]
BR = json.load(open(os.path.join(ROOT, "bridge_v1_1.json"), encoding="utf-8"))   # WS1 output
elem = {e["id"]: e for e in D}; elem.update({e["id"]: e for e in A})
realm = {e["id"]: "design" for e in D}; realm.update({e["id"]: "architecture" for e in A})

# family assignment lives in families.py (shared with layout_atlas.py)
sys.path.insert(0, ROOT)
from families import family_of

# ---- build undirected weighted graph over ALL edges (within + cross realm) ----
adj = defaultdict(lambda: defaultdict(float))
for e in BR["edges"]:
    f, t = e["from"], e["to"]
    if f in realm and t in realm and f != t:
        adj[f][t] += 1.0; adj[t][f] += 1.0
nodes = sorted(elem)
for n in nodes: adj[n]  # ensure singletons present

# ---- deterministic Louvain ----
def louvain(adj0):
    # level graph as dict node -> {nbr: w}; node ids are hashable
    def local_move(g, self_loops):
        k = {n: sum(g[n].values()) + 2 * self_loops.get(n, 0.0) for n in g}
        m = (sum(k.values())) / 2.0
        if m == 0: return {n: n for n in g}
        comm = {n: n for n in g}
        stot = {n: k[n] for n in g}
        improved = True; passes = 0
        while improved and passes < 100:
            improved = False; passes += 1
            for n in sorted(g, key=lambda x: str(x)):
                c0 = comm[n]
                # weights from n into each neighbouring community
                wc = defaultdict(float)
                for nb, w in g[n].items():
                    if nb != n: wc[comm[nb]] += w
                # remove n from c0
                stot[c0] -= k[n]
                best_c, best_gain = c0, 0.0
                # candidate communities: neighbours' + staying; deterministic order
                cands = sorted(set(list(wc.keys()) + [c0]), key=lambda x: str(x))
                for c in cands:
                    gain = wc.get(c, 0.0) - stot[c] * k[n] / (2.0 * m)
                    if gain > best_gain + 1e-12 or (abs(gain - best_gain) <= 1e-12 and str(c) < str(best_c) and c != c0):
                        best_gain, best_c = gain, c
                comm[n] = best_c; stot[best_c] += k[n]
                if best_c != c0: improved = True
        return comm
    # multilevel
    g = {n: dict(adj0[n]) for n in adj0}
    self_loops = defaultdict(float)
    node2orig = {n: {n} for n in g}
    mapping = {n: n for n in g}          # original node -> current level node
    while True:
        comm = local_move(g, self_loops)
        # relabel communities compactly
        cs = {c: i for i, c in enumerate(sorted(set(comm.values()), key=lambda x: str(x)))}
        comm = {n: cs[c] for n, c in comm.items()}
        if len(set(comm.values())) == len(g):     # no aggregation possible
            break
        # aggregate
        ng = defaultdict(lambda: defaultdict(float)); nsl = defaultdict(float)
        for n in g:
            cn = comm[n]
            nsl[cn] += self_loops[n]
            for nb, w in g[n].items():
                if nb == n: continue
                if comm[nb] == cn: nsl[cn] += w / 2.0
                else: ng[cn][comm[nb]] += w
        # update original mapping
        for orig in mapping: mapping[orig] = comm[mapping[orig]]
        g = {c: dict(ng[c]) for c in set(comm.values())}
        for c in g: g[c]  # ensure present
        self_loops = nsl
        if len(g) <= 1: break
    return mapping

part = louvain(adj)
comm_members = defaultdict(list)
for n, c in part.items(): comm_members[c].append(n)

# ---- curation: merge tiny into best-connected neighbour; cap island count to <=25 ----
def cross_weight(members_a, setb, membership):
    w = defaultdict(float)
    for n in members_a:
        for nb, ww in adj[n].items():
            cb = membership.get(nb)
            if cb is not None and cb != membership[n]: w[cb] += ww
    return w
membership = dict(part)
def recompute():
    cm = defaultdict(list)
    for n, c in membership.items(): cm[c].append(n)
    return cm
def best_neighbour(c, cm):
    w = defaultdict(float)
    for n in cm[c]:
        for nb, ww in adj[n].items():
            cb = membership[nb]
            if cb != c: w[cb] += ww
    if not w: return None
    return max(sorted(w), key=lambda x: (w[x], -len(cm[x])))
def best_by_kind(c, cm):
    """Fallback for graph-orphan islands: merge into the island sharing the most element kinds."""
    kc = Counter(elem[n]["kind"] for n in cm[c])
    best, bestscore = None, -1
    for o in sorted(cm):
        if o == c: continue
        ko = Counter(elem[n]["kind"] for n in cm[o])
        s = sum(min(kc[k], ko[k]) for k in kc)
        if s > bestscore or (s == bestscore and best is not None and len(cm[o]) > len(cm[best])):
            bestscore, best = s, o
    return best
MIN_SIZE = 8
changed = True
while changed:
    changed = False
    cm = recompute()
    for c in sorted(cm, key=lambda x: len(cm[x])):
        if len(cm[c]) < MIN_SIZE:
            tgt = best_neighbour(c, cm) or best_by_kind(c, cm)
            if tgt is not None:
                for n in cm[c]: membership[n] = tgt
                changed = True; break
# cap to 25: merge smallest into best neighbour until <=25 (and >=15 target range)
while True:
    cm = recompute()
    if len(cm) <= 25: break
    c = min(cm, key=lambda x: len(cm[x]))
    tgt = best_neighbour(c, cm)
    if tgt is None: break
    for n in cm[c]: membership[n] = tgt

# ---- compact island ids, compute hub / reps / family / neighbours ----
cm = recompute()
order = sorted(cm, key=lambda c: -len(cm[c]))
iid = {c: f"isl{ i+1:02d}" for i, c in enumerate(order)}
def within_deg(n, members_set):
    return sum(1 for nb in adj[n] if nb in members_set)
islands = []
membership_iid = {}
for c in order:
    members = sorted(cm[c])
    mset = set(members)
    for n in members: membership_iid[n] = iid[c]
    degs = {n: within_deg(n, mset) for n in members}
    hub = max(members, key=lambda n: (degs[n], -len(n)))
    reps = [n for n in sorted(members, key=lambda n: (-degs[n], n)) if n != hub][:3]
    fam = Counter(family_of(n) for n in members).most_common(1)[0][0]
    realm_split = Counter(realm[n] for n in members)
    kinds = Counter(elem[n]["kind"] for n in members).most_common(5)
    islands.append({"id": iid[c], "members": members, "size": len(members), "hub": hub,
                    "representatives": reps, "family": fam,
                    "realm_split": dict(realm_split), "top_kinds": kinds,
                    "internal_edges": sum(degs.values()) // 2})
# neighbours + routes (aggregated cross-island edge weight)
route_w = defaultdict(float)
for e in BR["edges"]:
    a, b = membership_iid.get(e["from"]), membership_iid.get(e["to"])
    if a and b and a != b:
        route_w[tuple(sorted((a, b)))] += 1.0
nbrs = defaultdict(list)
for (a, b), w in route_w.items():
    nbrs[a].append((b, w)); nbrs[b].append((a, w))
for isl in islands:
    ns = sorted(nbrs[isl["id"]], key=lambda x: -x[1])
    isl["neighbours"] = [{"island": b, "weight": int(w)} for b, w in ns]

routes = [{"from": a, "to": b, "weight": int(w)} for (a, b), w in sorted(route_w.items())]
out = {"islands": islands, "routes": routes, "membership": membership_iid}
json.dump(out, open(os.path.join(ROOT, "islands.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# modularity of final partition
def modularity():
    m = sum(sum(adj[n].values()) for n in adj) / 2.0
    if m == 0: return 0.0
    q = 0.0
    for isl in islands:
        ms = set(isl["members"])
        e_in = sum(adj[u][v] for u in ms for v in adj[u] if v in ms) / 2.0
        deg = sum(sum(adj[n].values()) for n in ms)
        q += e_in / m - (deg / (2 * m)) ** 2
    return q
print(f"== WS2 consolidation ==  {len(islands)} islands (from {len(set(part.values()))} raw Louvain communities)")
print(f"modularity Q = {modularity():.3f}   total elements placed: {sum(i['size'] for i in islands)}/{len(elem)}")
print(f"{'island':7} {'size':>4} {'d/a':>7} {'family':13} hub / top-kinds")
for isl in islands:
    da = f"{isl['realm_split'].get('design',0)}/{isl['realm_split'].get('architecture',0)}"
    tk = ",".join(f"{k}:{v}" for k, v in isl["top_kinds"][:3])
    print(f"  {isl['id']:5} {isl['size']:>4} {da:>7} {isl['family']:13} {isl['hub']}  [{tk}]")
placed = sum(i["size"] for i in islands)
assert placed == len(elem), f"UNPLACED: {len(elem)-placed}"
print("\nwrote islands.json (structure only; naming + layout next)")
