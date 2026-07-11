# Phase 3a adjudication: merges, renames, editor adds, design-realm repair, decision log.
import json, io, sys, os, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
SCRATCH = os.path.dirname(os.path.abspath(__file__))

A = json.load(open(os.path.join(SCRATCH, "merged_arch.json"), encoding="utf-8"))
els = A["elements"]
by_id = {e["id"]: e for e in els}
LOG = []

def merge(keep, drop):
    a, b = by_id[keep], by_id.pop(drop)
    els.remove(b)
    seen = {x.lower() for x in [a["name"]] + a["aka"]}
    for x in [b["name"]] + b["aka"]:
        if x.lower() not in seen:
            a["aka"].append(x)
    a["sources_all"] += [s for s in b["sources_all"] if s["src"] not in [x["src"] for x in a["sources_all"]]]
    a["scouts"] = sorted(set(a["scouts"] + b["scouts"]))
    for t in b["tags"]:
        if t not in a["tags"]:
            a["tags"].append(t)

merge("anti-corruption-layer", "anticorruption-layer")
merge("remote-procedure-invocation", "remote-procedure-invocation-integration-style")
merge("privilege-separation-pattern", "privilege-separation-process-topology")
merge("container", "container-component-container")
LOG.append("MERGE: four same-element pairs from different scouts folded (anti-corruption layer, EIP remote-procedure-invocation integration style, Provos privilege separation, POSA4 component container).")

REN = {"privilege-separation-pattern": "privilege-separation-arch",
       "container": "component-container",
       "moon-voting-architecture": "m-out-of-n-voting",
       "half-object-plus-protocol-distribution-structure": "half-object-plus-protocol-arch",
       "hardware-abstraction-layer-architectural-layer": "hardware-abstraction-layer-arch"}
for old, new in REN.items():
    by_id[old]["id"] = new
    by_id[new] = by_id.pop(old)
LOG.append("RENAME: id hygiene - privilege-separation-arch, component-container (POSA4 sense; the OS/deployment container is its own new element), m-out-of-n-voting, half-object-plus-protocol-arch, hardware-abstraction-layer-arch.")
LOG.append("KEEP-BOTH: dataflow-architecture (Shaw-Garlan classical family) vs streaming-dataflow-architecture (Akidau unbounded-stream topology) - specializes edge in 3b; monitor (Bass tactic) vs design-realm monitor (Hoare) per same-name-two-realms; channel-architecture (Douglass) vs message-channel (connector); temporal-firewall (Kopetz) vs firewall; time-triggered-bus (connector) vs time-triggered-architecture (style).")

ADDS = [
 {"id": "subsumption-architecture", "name": "Subsumption Architecture", "aka": ["behavior-based layered control"],
  "kind": "style", "what": "Layers of behavior-producing modules run concurrently, with higher layers subsuming (suppressing/overriding) the outputs of lower ones instead of a central planner.",
  "problem": "Robot control needs robust real-time reaction without a monolithic sense-plan-act pipeline; layered competence levels degrade gracefully and are incrementally buildable.",
  "named_in": "A Robust Layered Control System for a Mobile Robot - Brooks (IEEE J. Robotics and Automation, 1986)",
  "tags": ["robotics", "embedded"]},
 {"id": "os-container", "name": "OS Container", "aka": ["Linux container", "Docker container", "containerized deployment unit"],
  "kind": "deployment", "what": "An OS-level isolated execution unit packaging an application with its dependencies, sharing the host kernel, used as the standard unit of deployment and scheduling.",
  "problem": "Deployable units need environment-independent packaging and fast, dense isolation without full-VM overhead; containers make the deployment topology reproducible and orchestratable.",
  "named_in": "Design Patterns for Container-based Distributed Systems - Burns & Oppenheimer (USENIX HotCloud 2016)",
  "tags": ["cloud", "deployment"]},
 {"id": "distributed-tracing", "name": "Distributed Tracing", "aka": ["end-to-end request tracing", "trace/span infrastructure"],
  "kind": "pattern", "what": "Propagates a trace context across service boundaries and records per-hop spans so one request's path, latency and failures can be reconstructed system-wide.",
  "problem": "In multi-service topologies no single log explains a slow or failed request; correlated spans restore end-to-end causality.",
  "named_in": "Dapper, a Large-Scale Distributed Systems Tracing Infrastructure - Sigelman et al. (Google TR, 2010)",
  "tags": ["distributed", "observability"]},
 {"id": "log-aggregation", "name": "Log Aggregation", "aka": ["centralized logging"],
  "kind": "pattern", "what": "All services ship logs to a central searchable store rather than keeping them on individual hosts.",
  "problem": "Per-host logs are useless when instances are ephemeral and requests span services; central aggregation restores a single queryable operational record.",
  "named_in": "Microservices Patterns - Richardson (2018), Log aggregation pattern",
  "tags": ["distributed", "observability"]},
 {"id": "health-check-api", "name": "Health Check API", "aka": ["health endpoint monitoring"],
  "kind": "pattern", "what": "Each service exposes an endpoint reporting its own liveness/readiness, polled by orchestrators and load balancers to route around unhealthy instances.",
  "problem": "Infrastructure must distinguish a live-but-degraded instance from a dead one to place traffic and restarts correctly; a self-reported health contract makes that decision mechanical.",
  "named_in": "Microservices Patterns - Richardson (2018), Health check API pattern",
  "tags": ["distributed", "observability"]},
]
skipped_adds = []
for x in ADDS:
    if x["id"] in by_id:
        skipped_adds.append(x["id"])
        continue
    x.update({"realm": "architecture", "borderline": None, "confidence": "established",
              "scouts": ["editor"], "kind_votes": {x["kind"]: 1},
              "named_in_corpus_id": None,
              "sources_all": [{"src": x["named_in"], "corpus_id": None}]})
    els.append(x)
    by_id[x["id"]] = x
if skipped_adds:
    print("editor adds already present (scout-covered), skipped:", skipped_adds)
LOG.append("EDITOR ADDS (scout-flagged gaps, certain sources): subsumption-architecture (Brooks 1986 - robotics control vocabulary, bridge target for behavior-tree); os-container (Burns-Oppenheimer 2016 - the deployment-unit sense, distinct from POSA4 component-container); the observability structures the quality scout flagged as unowned - distributed-tracing (Dapper 2010), log-aggregation + health-check-api (Richardson 2018). Declined: sense-plan-act (naming diffuse across robotics texts), models of computation (leeseshia - modeling formalisms, a different band than architecture elements; logged not cataloged), 'metrics collection' (Richardson names it but it folds into log-aggregation/observability family - too thin alone... kept OUT, noted).")
A["rejected"].append({"name": "Competing Consumers (system-topology sense)", "decision": "drop",
                      "into": "competing-consumers (design realm)",
                      "why": "the in-process element owns the mechanism; the scaling-topology sense is expressed by bridging it to messaging/message-broker/load-balanced pools, not by a second node", "_scout": "editor"})
LOG.append("INTAKE AUDIT CLOSURE: 'Pipes and Filters (POSA1)' was a fuzz miss (pipes-and-filters is cataloged); 'Competing Consumers' now carries an explicit drop record (bridge, not catalog).")

# ---- design-realm repair: Message Translator (EIP) was never cataloged in Phase 1
D = json.load(open(os.path.join(SCRATCH, "merged_design.json"), encoding="utf-8"))
if not any(e["id"] == "message-translator" for e in D["elements"]):
    D["elements"].append({
        "id": "message-translator", "name": "Message Translator",
        "aka": ["payload transformer", "message transformation"],
        "kind": "communication",
        "what": "A filter placed between messaging participants that converts a message's data format/schema so sender and receiver can each keep their own model.",
        "problem": "Endpoints evolve and disagree on formats; translating in the channel decouples their data models without changing either endpoint.",
        "named_in": "Enterprise Integration Patterns - Hohpe & Woolf (2003)",
        "named_in_corpus_id": None, "tags": ["messaging"], "borderline": None,
        "confidence": "established", "scouts": ["editor-p3"],
        "kind_votes": {"communication": 1},
        "sources_all": [{"src": "Enterprise Integration Patterns - Hohpe & Woolf (2003)", "corpus_id": None}],
    })
    D["elements"].sort(key=lambda m: (m["kind"], m["id"]))
    json.dump(D, open(os.path.join(SCRATCH, "merged_design.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    # pass-8: eip work gains the element
    P = json.load(open(os.path.join(SCRATCH, "pass8_works.json"), encoding="utf-8"))
    for w in P["works"]:
        if w["id"] == "eip":
            if "message-translator" not in w["elements"]:
                w["elements"].append("message-translator")
                w["elements"].sort()
    json.dump(P, open(os.path.join(SCRATCH, "pass8_works.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    dd = json.load(open(os.path.join(SCRATCH, "decisions_design.json"), encoding="utf-8"))
    dd["log"].append("POST-FREEZE REPAIR (2026-07-11, via Phase 3a audit): Message Translator (EIP 2003) was missed by the Phase 1 EIP scout's altitude triage though it passes cleanly (in-process payload transformation); added as design element 709 with eip as covering work. Flagged independently by the POSA1 architecture scout.")
    json.dump(dd, open(os.path.join(SCRATCH, "decisions_design.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("design repair applied: message-translator added (709 elements); eip coverage updated")

ids = [e["id"] for e in els]
assert len(ids) == len(set(ids)), [i for i in ids if ids.count(i) > 1]
els.sort(key=lambda m: (m["kind"], m["id"]))
json.dump(A, open(os.path.join(SCRATCH, "merged_arch.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump({"log": LOG}, open(os.path.join(SCRATCH, "decisions_arch.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
from collections import Counter
print(f"architecture elements: {len(els)}")
print("per-kind:", dict(sorted(Counter(e['kind'] for e in els).items())))
