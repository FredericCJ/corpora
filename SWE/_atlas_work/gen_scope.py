# WS1 scope map: partition the 1083 elements into coherent within-realm research groups, compute the
# priority set (sibling-less design / disconnected arch), and emit per-group scope files + a global id
# index. Agents consume these to research REAL within-realm relations for atlas enrichment.
import json, os, io, sys, re
from collections import Counter, defaultdict
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.abspath(__file__))          # SWE/_atlas_work
SRC = os.path.normpath(os.path.join(ROOT, "..", "explorer", "build", "element_src"))
OUT = os.path.join(ROOT, "scope"); os.makedirs(OUT, exist_ok=True)

D = json.load(open(os.path.join(SRC, "design.json"), encoding="utf-8"))["elements"]
A = json.load(open(os.path.join(SRC, "architecture.json"), encoding="utf-8"))["elements"]
B = json.load(open(os.path.join(SRC, "bridge.json"), encoding="utf-8"))
node = {e["id"]: {"realm": "design", "kind": e["kind"], "e": e} for e in D}
node.update({e["id"]: {"realm": "architecture", "kind": e["kind"], "e": e} for e in A})

# ---- within-realm adjacency from existing edges (for dedup + degree + connectivity) ----
WITHIN_KINDS = {"specializes", "composes-with", "alternative-to", "implements", "uses"}
within_adj = defaultdict(set); within_edges_by_realm = defaultdict(list)
for e in B["edges"]:
    f, k, t = e["from"], e["kind"], e["to"]
    if f in node and t in node and k in WITHIN_KINDS and node[f]["realm"] == node[t]["realm"]:
        within_adj[f].add(t); within_adj[t].add(f)
        within_edges_by_realm[node[f]["realm"]].append({"from": f, "kind": k, "to": t})
sibling_less_design = sorted(e["id"] for e in D if not within_adj[e["id"]])
disconnected_arch = sorted(e["id"] for e in A if not within_adj[e["id"]])

# ---- DESIGN groups: 22 kinds -> 15 topical research groups ----
DGROUP = {
 "oo-patterns":               ("D01", "Object-oriented design patterns (GoF & kin)"),
 "synchronization-coordination":("D02","Synchronization & coordination primitives"),
 "execution-concurrency":     ("D03", "Execution, concurrency & scheduling"),
 "scheduling-time":           ("D03", "Execution, concurrency & scheduling"),
 "resource-management":       ("D04", "Resource management & lifetime"),
 "data-structures":           ("D05", "Data structures"),
 "error-handling":            ("D06", "Error handling & fault resilience"),
 "robustness-security":       ("D07", "Robustness & security idioms"),
 "communication":             ("D08", "Communication & messaging"),
 "data-representation":       ("D09", "Data representation & serialization"),
 "serialization-framing":     ("D09", "Data representation & serialization"),
 "state-management":          ("D10", "State management"),
 "construction-api":          ("D11", "Object construction & API design"),
 "persistence-durability":    ("D12", "Persistence, durability & caching"),
 "caching-memoization":       ("D12", "Persistence, durability & caching"),
 "data-flow-buffering":       ("D13", "Data flow, buffering & parsing"),
 "parsing-text":              ("D13", "Data flow, buffering & parsing"),
 "functional-type-idioms":    ("D14", "Functional & type-system idioms"),
 "embedded-systems":          ("D15", "Embedded, numeric, structural & testing idioms"),
 "numeric-precision":         ("D15", "Embedded, numeric, structural & testing idioms"),
 "code-structure":            ("D15", "Embedded, numeric, structural & testing idioms"),
 "testing-constructs":        ("D15", "Embedded, numeric, structural & testing idioms"),
}
DLIT = {
 "D01": "GoF Design Patterns 'Related Patterns' sections; Refactoring.Guru / SourceMaking 'Relations with Other Patterns'; POSA1; Fowler PoEAA; Riehle pattern collaboration.",
 "D02": "Little Book of Semaphores (Downey); Butenhof POSIX Threads; Herlihy & Shavit Art of Multiprocessor Programming; Java Concurrency in Practice; POSA2 concurrency patterns.",
 "D03": "POSA2 (Reactor/Proactor/Active Object/Half-Sync); Nystrom Game Programming Patterns (game loop, update); Schmidt et al.; real-time scheduling (Liu, Buttazzo).",
 "D04": "Stroustrup / Meyers Effective C++ (RAII, smart pointers); Alexandrescu Modern C++ Design; pool/arena literature; Preschern 'Fluent C' resource patterns.",
 "D05": "CLRS; Sedgewick; Okasaki Purely Functional Data Structures; Knuth TAOCP; database index structures (B-tree/LSM) DDIA.",
 "D06": "Preschern error-handling patterns (Fluent C); Nygard Release It! (stability patterns); POSA3; exception-safety (Sutter Exceptional C++); Erlang/OTP supervision.",
 "D07": "Secure design patterns (Schumacher POSA-security); OWASP; Viega & McGraw Building Secure Software; Saltzer & Schroeder principles; sandboxing/isolation idioms.",
 "D08": "Hohpe & Woolf Enterprise Integration Patterns; POSA4 distributed; Coulouris Distributed Systems; RPC/streaming idioms; Tanenbaum networking.",
 "D09": "Serialization/wire-format literature (Protocol Buffers, ASN.1); parsing framing; Martin Data representation; endianness/marshalling idioms; TLV.",
 "D10": "GoF State/Memento; Nystrom (state machines, snapshot); Fowler event sourcing; state-management UI (flux/redux lineage); immutable state idioms.",
 "D11": "GoF creational; Effective Java (Bloch) builders/factories; fluent-interface (Fowler); Alexandrescu policy-based construction; dependency injection (Fowler).",
 "D12": "DDIA (Kleppmann) storage & retrieval; write-ahead log / LSM; caching patterns (cache-aside, write-through); ORM patterns (Fowler PoEAA).",
 "D13": "Reactive Streams; pipes-and-filters idioms; buffering (ring/double buffer); backpressure; tokenizer/lexer/parser pipelines; Nystrom data locality.",
 "D14": "Okasaki; Wadler (monads/functors); Scott Programming Language Pragmatics; typeclass/trait idioms; functional error handling (Option/Either); persistent structures.",
 "D15": "Preschern 'Fluent C'; Pont Patterns for Time-Triggered Embedded Systems; embedded C idioms; fixed-point/numeric; testing patterns (xUnit Patterns, Meszaros).",
}

# ---- ARCH groups ----
def qa_of(e):
    return [t.split(":", 1)[1] for t in (e.get("tags") or []) if t.startswith("qa:")]
def arch_group(e):
    k = e["kind"]
    if k == "tactic":
        q = set(qa_of(e))
        if q & {"availability", "reliability"}: return ("A01", "Availability & reliability tactics")
        if q & {"security", "safety"}: return ("A02", "Security & safety tactics")
        if q & {"performance", "scalability", "energy-efficiency", "resource-efficiency"}:
            return ("A03", "Performance, scalability & energy tactics")
        return ("A04", "Modifiability, integrability, deployability, testability & usability tactics")
    if k == "style": return ("A05", "Architecture styles (boxology family tree)")
    if k == "pattern":
        tg = set(e.get("tags") or [])
        if tg & {"web", "cloud", "microservices", "integration", "observability", "ops"}:
            return ("A10", "Web, cloud, microservices & integration patterns")
        if tg & {"distributed", "messaging", "middleware", "networking", "network", "workflow"}:
            return ("A06", "Distributed systems & messaging patterns")
        return ("A07", "Enterprise, data, embedded & security patterns")
    if k == "connector" or k == "description": return ("A08", "Connectors & architecture description")
    return ("A09", "Deployment & reference architectures")  # deployment, reference-architecture
ALIT = {
 "A01": "Bass, Clements & Kazman 'Software Architecture in Practice' (3rd ed.) availability tactic tree (fault detection/recovery-preparation/recovery-reintroduction/prevention); Nygard Release It!; Hanmer Patterns for Fault Tolerant Software.",
 "A02": "Bass-Clements-Kazman security & safety tactic trees (detect/resist/react/recover); NIST; Schumacher security patterns; IEC 61508 / ISO 26262 safety mechanisms; Leveson Engineering a Safer World.",
 "A03": "Bass-Clements-Kazman performance tactics (control resource demand / manage resources); scalability tactics; energy-efficiency tactics; Smith & Williams Performance Solutions.",
 "A04": "Bass-Clements-Kazman modifiability/deployability/testability/usability/integrability tactic trees (localize changes, defer binding, restrict dependencies, etc.).",
 "A05": "Shaw & Garlan 'Software Architecture: Perspectives'; Garlan & Shaw 'Intro to Software Architecture' boxology; Taylor, Medvidovic & Dashofy style taxonomy; Fielding REST; dataflow/call-return/repository/layered/event families.",
 "A06": "POSA1 & POSA4 (distributed-object, broker, proxy); Hohpe & Woolf EIP (channels, routing, transformation, endpoints); Coulouris/Tanenbaum distributed systems; each pattern realizes/refines a style and relates to sibling patterns.",
 "A10": "Richardson 'Microservices Patterns'; cloud design patterns (Azure/AWS well-architected); Fowler; API gateway/BFF/service mesh/observability; web application patterns; each pattern realizes/refines a style and relates to siblings.",
 "A07": "Fowler PoEAA (enterprise/data source/domain logic); POSA; embedded/real-time patterns (Douglass Real-Time Design Patterns; Pont); security patterns; each pattern realizes/refines a style.",
 "A08": "Taylor, Medvidovic & Dashofy connector taxonomy (procedure-call, event, data-access, linkage, stream, arbitrator, adaptor, distributor); Mehta et al. 'Towards a Taxonomy of Software Connectors'; ADLs (ACME, xADL, Wright).",
 "A09": "Deployment & infrastructure patterns (Nginx/container/orchestration); reference architectures (AUTOSAR, Lambda/Kappa, microservices RA, IoT RA); Bass deployment tactics.",
}

# ---- assign, collect members ----
groups = defaultdict(lambda: {"members": [], "title": "", "realm": "", "lit": ""})
def short(e):
    w = re.sub(r"\s+", " ", e.get("what", "")).strip()
    return {"id": e["id"], "name": e["name"], "kind": e["kind"],
            "aka": (e.get("aka") or [])[:3], "what": w[:240]}
for e in D:
    gid, title = DGROUP[e["kind"]]
    g = groups[gid]; g["title"] = title; g["realm"] = "design"; g["lit"] = DLIT[gid]
    g["members"].append(short(e))
for e in A:
    gid, title = arch_group(e)
    g = groups[gid]; g["title"] = title; g["realm"] = "architecture"; g["lit"] = ALIT[gid]
    g["members"].append(short(e))

prio = set(sibling_less_design) | set(disconnected_arch)
id_index = [{"id": i, "name": node[i]["e"]["name"], "kind": node[i]["kind"], "realm": node[i]["realm"]}
            for i in sorted(node)]
json.dump(id_index, open(os.path.join(ROOT, "id_index.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)

manifest = []
for gid in sorted(groups):
    g = groups[gid]
    mids = {m["id"] for m in g["members"]}
    existing = [e for e in within_edges_by_realm[g["realm"]] if e["from"] in mids and e["to"] in mids]
    pset = sorted(mids & prio)
    scope = {"group": gid, "title": g["title"], "realm": g["realm"], "literature": g["lit"],
             "member_count": len(g["members"]),
             "target_edges": round(len(g["members"]) * 1.2),
             "priority_ids": pset, "members": sorted(g["members"], key=lambda m: m["id"]),
             "existing_intra_edges": existing}
    json.dump(scope, open(os.path.join(OUT, gid + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    manifest.append((gid, g["realm"], len(g["members"]), len(pset), len(existing), g["title"]))

print("== WS1 scope map ==")
print(f"design elements {len(D)} | arch {len(A)} | total {len(node)}")
print(f"sibling-less design: {len(sibling_less_design)} | disconnected arch: {len(disconnected_arch)}")
print(f"existing within-design edges {len(within_edges_by_realm['design'])} | within-arch {len(within_edges_by_realm['architecture'])}")
print(f"\n{len(manifest)} research groups (gid | realm | members | priority | existing-intra | title):")
for gid, realm, n, p, ex, title in manifest:
    print(f"  {gid} {realm[:1]}  n={n:3}  prio={p:3}  ex={ex:3}  {title}")
json.dump({"groups": [m[0] for m in manifest]}, open(os.path.join(ROOT, "scope_manifest.json"), "w", encoding="utf-8"))
