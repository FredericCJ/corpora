# Shared family assignment (7 families of ATLAS_SPEC §3). Element-aware: design by kind; architecture
# tactics by quality-attribute, patterns by domain tag. Imported by consolidate.py and layout_atlas.py.
import json, os
SRC = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "explorer", "build", "element_src"))
_D = json.load(open(os.path.join(SRC, "design.json"), encoding="utf-8"))["elements"]
_A = json.load(open(os.path.join(SRC, "architecture.json"), encoding="utf-8"))["elements"]
ELEM = {e["id"]: e for e in _D}; ELEM.update({e["id"]: e for e in _A})
REALM = {e["id"]: "design" for e in _D}; REALM.update({e["id"]: "architecture" for e in _A})

DK2F = {
 "synchronization-coordination": "concurrency", "execution-concurrency": "concurrency", "scheduling-time": "concurrency",
 "data-structures": "data", "persistence-durability": "data", "caching-memoization": "data",
 "data-representation": "data", "serialization-framing": "data",
 "communication": "communication",
 "oo-patterns": "structure", "construction-api": "structure", "code-structure": "structure", "state-management": "structure",
 "error-handling": "reliability", "robustness-security": "reliability",
 "resource-management": "resource", "data-flow-buffering": "resource", "embedded-systems": "resource", "numeric-precision": "resource",
 "functional-type-idioms": "foundations", "parsing-text": "foundations", "testing-constructs": "foundations",
}
def _tags(e): return set(e.get("tags") or [])
def _qa(e): return set(t.split(":", 1)[1] for t in _tags(e) if t.startswith("qa:"))
def family_of(eid):
    e = ELEM[eid]; k = e["kind"]
    if REALM[eid] == "design":
        return DK2F.get(k, "foundations")
    if k == "tactic":
        q = _qa(e)
        if q & {"availability", "security", "safety", "reliability"}: return "reliability"
        if q & {"performance", "scalability", "energy-efficiency", "resource-efficiency"}: return "resource"
        return "structure"
    if k == "pattern":
        tg = _tags(e)
        if tg & {"distributed", "messaging", "integration", "middleware", "networking", "network"}: return "communication"
        if tg & {"data", "database"}: return "data"
        if tg & {"embedded", "real-time", "safety-critical"}: return "resource"
        if tg & {"security"}: return "reliability"
        return "structure"
    return {"style": "structure", "connector": "communication", "description": "foundations",
            "deployment": "resource", "reference-architecture": "foundations"}.get(k, "structure")
