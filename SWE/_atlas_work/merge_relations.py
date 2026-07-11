# WS1 merge/validate/audit: fold the 25 research groups' within-realm edges into the existing 1132-edge
# bridge, with strict validation, dedup (exact + symmetric + vs existing), conflict resolution, a
# degree cap (anti-hairball), and an optional computed co-realization backbone (1C) for arch stragglers.
# Emits _atlas_work/bridge_v1_1.json + merge_stats.json and prints the acceptance table.
import json, os, io, sys, glob
from collections import Counter, defaultdict
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.normpath(os.path.join(ROOT, "..", "explorer", "build", "element_src"))

CROSS = {"realizes", "enables"}; CROSS_REV = {"constrains"}
SYM = {"composes-with", "alternative-to"}         # symmetric within-realm
DIR = {"specializes", "uses"}                     # directional within-realm (both realms)
IMPL = {"implements"}                             # directional design-only
WITHIN = SYM | DIR | IMPL
NEW_KINDS = WITHIN
MAX_DEG = 14                                       # within-realm degree cap per node (anti-hairball)

D = json.load(open(os.path.join(SRC, "design.json"), encoding="utf-8"))["elements"]
A = json.load(open(os.path.join(SRC, "architecture.json"), encoding="utf-8"))["elements"]
B = json.load(open(os.path.join(SRC, "bridge.json"), encoding="utf-8"))
realm = {e["id"]: "design" for e in D}; realm.update({e["id"]: "architecture" for e in A})
kind = {e["id"]: e["kind"] for e in D}; kind.update({e["id"]: e["kind"] for e in A})
qa = {}
for e in A:
    qa[e["id"]] = set(t.split(":", 1)[1] for t in (e.get("tags") or []) if t.startswith("qa:"))

def canon(f, k, t):
    """Canonical key for dedup: symmetric kinds are order-independent."""
    if k in SYM:
        a, b = sorted([f, t]); return (a, k, b)
    return (f, k, t)

# ---- existing edges: exact keys, symmetric-pair keys, and within-realm degree ----
existing = B["edges"]
exist_keys = set(); pair_sym = {}      # frozenset(pair) -> kind, to catch composes/alternative conflicts
deg = defaultdict(int)
for e in existing:
    f, k, t = e["from"], e["kind"], e["to"]
    exist_keys.add(canon(f, k, t))
    if k in WITHIN and realm.get(f) == realm.get(t):
        deg[f] += 1; deg[t] += 1
    if k in SYM:
        pair_sym[frozenset((f, t))] = k

# ---- load research output (final/ preferred, harvest/ fallback when a group's verify didn't land) ----
raw = []; per_group = Counter(); source_of = {}
def load_edges(path):
    try:
        d = json.load(open(path, encoding="utf-8"))
    except Exception as ex:
        print(f"  !! could not parse {path}: {ex}"); return []
    g = d.get("group", os.path.basename(path)[:-5])
    return [dict(e, _group=g) for e in d.get("edges", [])]
final_names = set()
for path in sorted(glob.glob(os.path.join(ROOT, "final", "*.json"))):
    b = os.path.basename(path); final_names.add(b); source_of[b] = "final"
    raw += load_edges(path)
for path in sorted(glob.glob(os.path.join(ROOT, "harvest", "*.json"))):
    b = os.path.basename(path)
    if b not in final_names:
        source_of[b] = "harvest-fallback"; raw += load_edges(path)
print(f"loaded {len(raw)} raw edges from {len(source_of)} group files "
      f"({sum(1 for v in source_of.values() if v=='final')} final, "
      f"{sum(1 for v in source_of.values() if v=='harvest-fallback')} harvest-fallback)")

# ---- validate + dedup + conflict + degree-cap ----
rej = Counter(); accepted = []; new_keys = set()
# score for degree-cap ordering: sourced first, then priority-connecting (low current degree), then group
def score(e):
    f, t = e["from"], e["to"]
    s = 2 if e.get("provenance") == "sourced" else 0
    lowdeg = (deg[f] == 0) + (deg[t] == 0)      # connecting a still-relationless node is valuable
    return (s + lowdeg * 2, -(deg[f] + deg[t]))
# pre-clean + validate
clean = []
for e in raw:
    f, k, t = e.get("from"), e.get("kind"), e.get("to")
    prov = e.get("provenance", "editorial")
    if k not in NEW_KINDS: rej["bad-kind"] += 1; continue
    if f not in realm or t not in realm: rej["unknown-id"] += 1; continue
    if f == t: rej["self-loop"] += 1; continue
    if realm[f] != realm[t]: rej["cross-realm"] += 1; continue
    if k in IMPL and realm[f] != "design": rej["implements-nondesign"] += 1; continue
    cite = (e.get("cite") or "").strip()
    if prov == "sourced" and not cite:
        prov = "editorial"; rej["demoted-nocite"] += 1
    if prov not in ("sourced", "editorial"): prov = "editorial"
    clean.append({"from": f, "kind": k, "to": t, "provenance": prov,
                  "cite": cite or None, "note": (e.get("note") or "").strip()[:180], "group": e.get("_group")})
# order by score so degree-cap keeps the best; sourced + priority-connecting win
clean.sort(key=score, reverse=True)
cur_deg = dict(deg)
for e in clean:
    f, k, t = e["from"], e["kind"], e["to"]
    key = canon(f, k, t)
    if key in exist_keys or key in new_keys: rej["dup"] += 1; continue
    # symmetric conflict: same unordered pair already composes/alternative (existing or new) with other kind
    if k in SYM:
        pk = pair_sym.get(frozenset((f, t)))
        if pk and pk != k: rej["sym-conflict"] += 1; continue
    # directional conflict: reverse already present for specializes/implements (asymmetric hierarchy)
    if k in ("specializes",) and (canon(t, k, f) in exist_keys or canon(t, k, f) in new_keys):
        rej["dir-conflict"] += 1; continue
    if cur_deg[f] >= MAX_DEG or cur_deg[t] >= MAX_DEG: rej["degree-cap"] += 1; continue
    new_keys.add(key); accepted.append(e); cur_deg[f] += 1; cur_deg[t] += 1
    if k in SYM: pair_sym[frozenset((f, t))] = k
    per_group[e["group"]] += 1

# ---- 1C: computed co-realization backbone for still-disconnected arch nodes ----
within_deg_after = defaultdict(int)
for e in existing:
    if e["kind"] in WITHIN and realm.get(e["from"]) == realm.get(e["to"]):
        within_deg_after[e["from"]] += 1; within_deg_after[e["to"]] += 1
for e in accepted:
    within_deg_after[e["from"]] += 1; within_deg_after[e["to"]] += 1
arch_ids = [e["id"] for e in A]
still_disc = [i for i in arch_ids if within_deg_after[i] == 0]
# design elements realizing each arch target (from cross edges realizes/enables)
realizers = defaultdict(set)
for e in existing:
    if e["kind"] in CROSS: realizers[e["to"]].add(e["from"])
derived = []; derived_keys = set()
def try_derive(a1, a2, note):
    key = canon(a1, "composes-with", a2)
    if key in exist_keys or key in new_keys or key in derived_keys: return False
    derived_keys.add(key)
    derived.append({"from": key[0], "kind": "composes-with", "to": key[2], "provenance": "derived",
                    "cite": None, "note": note[:180], "group": "1C-derived"})
    return True
for i in list(still_disc):
    best = None
    # (a) most co-realizing design elements
    for j in arch_ids:
        if j == i: continue
        shared = realizers[i] & realizers[j]
        if len(shared) >= 3 and (best is None or len(shared) > best[1]):
            best = (j, len(shared))
    if best:
        if try_derive(i, best[0], f"{best[1]} design elements realize both (computed co-realization backbone)"):
            within_deg_after[i] += 1; within_deg_after[best[0]] += 1; continue
    # (b) same-QA tactic fallback
    if kind[i] == "tactic" and qa.get(i):
        for j in arch_ids:
            if j != i and kind[j] == "tactic" and (qa[i] & qa.get(j, set())):
                if try_derive(i, j, f"same quality-attribute tactic ({sorted(qa[i]&qa[j])[0]}); backbone link"):
                    within_deg_after[i] += 1; within_deg_after[j] += 1; break

# ---- assemble enriched edge set + recompute metrics ----
merged = existing + accepted + derived
def metrics(edges):
    adj = defaultdict(set); wd = 0; wa = 0
    for e in edges:
        f, k, t = e["from"], e["kind"], e["to"]
        if k in WITHIN and realm.get(f) == realm.get(t):
            adj[f].add(t); adj[t].add(f)
            if realm[f] == "design": wd += 1
            else: wa += 1
    sib_less_d = sum(1 for e in D if not adj[e["id"]])
    disc_a = sum(1 for e in A if not adj[e["id"]])
    md = 2 * (wd + wa) / (len(D) + len(A))
    return dict(within_design=wd, within_arch=wa, sibling_less_design=sib_less_d,
                disconnected_arch=disc_a, mean_within_degree=round(md, 2), adj=adj)

m0 = metrics(existing); m1 = metrics(merged)
# deterministic label-prop modularity on within-realm graph of merged
def modularity(edges):
    adj = defaultdict(set); ew = []
    for e in edges:
        f, t, k = e["from"], e["to"], e["kind"]
        if k in WITHIN and realm.get(f) == realm.get(t):
            adj[f].add(t); adj[t].add(f); ew.append((f, t))
    ids = sorted(set([e["id"] for e in D] + [e["id"] for e in A]))
    lab = {n: n for n in ids}
    for _ in range(30):
        ch = 0
        for n in ids:
            if not adj[n]: continue
            c = Counter(lab[x] for x in adj[n]); mx = max(c.values())
            best = min(l for l, v in c.items() if v == mx)
            if lab[n] != best: lab[n] = best; ch += 1
        if not ch: break
    M = len(ew)
    if not M: return 0.0, 0
    deg2 = defaultdict(int)
    for f, t in ew: deg2[f] += 1; deg2[t] += 1
    e_in = Counter(); dsum = Counter()
    for n in ids: dsum[lab[n]] += deg2[n]
    for f, t in ew:
        if lab[f] == lab[t]: e_in[lab[f]] += 1
    Q = sum((e_in[c] / M) - (dsum[c] / (2 * M)) ** 2 for c in dsum)
    return round(Q, 3), len(set(lab[n] for n in ids if adj[n]))

Q, ncomm = modularity(merged)
prov_new = Counter(e["provenance"] for e in accepted)
kind_new = Counter(e["kind"] for e in accepted)

out = {"edges": merged, "unbridged": B.get("unbridged", [])}
json.dump(out, open(os.path.join(ROOT, "bridge_v1_1.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
stats = dict(existing_edges=len(existing), new_accepted=len(accepted), derived=len(derived),
             total=len(merged), rejected=dict(rej), per_group=dict(per_group),
             prov_new=dict(prov_new), kind_new=dict(kind_new),
             baseline=dict(within_design=m0["within_design"], within_arch=m0["within_arch"],
                           sibling_less_design=m0["sibling_less_design"], disconnected_arch=m0["disconnected_arch"],
                           mean_within_degree=m0["mean_within_degree"]),
             enriched=dict(within_design=m1["within_design"], within_arch=m1["within_arch"],
                           sibling_less_design=m1["sibling_less_design"], disconnected_arch=m1["disconnected_arch"],
                           mean_within_degree=m1["mean_within_degree"], modularity=Q, communities=ncomm))
json.dump(stats, open(os.path.join(ROOT, "merge_stats.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

def row(label, now, target, val, ok):
    print(f"  {label:32} {str(now):>6} -> {str(val):>6}   target {target:>6}   {'OK' if ok else 'MISS'}")
print("== WS1 merge — acceptance ==")
print(f"research groups loaded: {len({e['group'] for e in accepted})}  raw edges: {len(raw)}  accepted: {len(accepted)}  derived(1C): {len(derived)}")
print(f"new provenance: {dict(prov_new)}  |  new kinds: {dict(kind_new)}")
print(f"rejected: {dict(rej)}")
print("metric                             now  ->  new     target      status")
row("within-architecture edges", m0["within_arch"], ">=250", m1["within_arch"], m1["within_arch"] >= 250)
row("within-design edges", m0["within_design"], ">=700", m1["within_design"], m1["within_design"] >= 700)
row("disconnected architecture", m0["disconnected_arch"], "<=15", m1["disconnected_arch"], m1["disconnected_arch"] <= 15)
row("sibling-less design", m0["sibling_less_design"], "<=100", m1["sibling_less_design"], m1["sibling_less_design"] <= 100)
row("mean within-degree", m0["mean_within_degree"], ">=4.5", m1["mean_within_degree"], m1["mean_within_degree"] >= 4.5)
row("modularity (islandy)", "0.79", ">=0.55", Q, Q >= 0.55)
print(f"\nwrote bridge_v1_1.json ({len(merged)} edges) + merge_stats.json")
