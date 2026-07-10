# Adjudication round 2: un-fuse adapter/decorator, factory-method/prototype, refcount/ABA,
# list-virtualization/stream-windowing; merge setjmp pair; aka hygiene; decision log.
import json, io, sys, os, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
SCRATCH = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(SCRATCH, "merged_design.json"), encoding="utf-8") as f:
    data = json.load(f)
els = data["elements"]
by_id = {e["id"]: e for e in els}
LOG = []

def norm(s):
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()

def raw_entries():
    for sub in ("sweeps", os.path.join("sweeps", "gaps")):
        p = os.path.join(SCRATCH, sub)
        for fn in sorted(os.listdir(p)):
            if fn.endswith(".json") and os.path.isfile(os.path.join(p, fn)):
                with open(os.path.join(p, fn), encoding="utf-8") as f:
                    d = json.load(f)
                for x in d.get("elements", []):
                    yield d.get("scout", fn[:-5]), x

RAW = list(raw_entries())

def rebuild(name, kind, strip_akas=()):
    """merge all raw entries whose exact name matches; return merged element"""
    g = [(s, x) for s, x in RAW if norm(x["name"]) == norm(name)]
    assert g, name
    top = g[0][1]
    akas, seen = [], {norm(name)} | {norm(a) for a in strip_akas}
    sources, scouts, tags = [], [], []
    for s, x in g:
        scouts.append(s)
        for a in [x["name"]] + (x.get("aka") or []):
            if norm(a) not in seen:
                seen.add(norm(a))
                akas.append(a)
        sources.append({"src": x["named_in"], "corpus_id": x.get("named_in_corpus_id")})
        for t in x.get("tags") or []:
            if t not in tags:
                tags.append(t)
    named = next((s for s in sources if s["corpus_id"]), sources[0])
    return {"id": re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-"), "name": name,
            "aka": akas, "kind": kind, "what": top["what"], "problem": top["problem"],
            "named_in": named["src"], "named_in_corpus_id": named["corpus_id"], "tags": tags,
            "borderline": top.get("borderline"), "confidence": top.get("confidence", "established"),
            "scouts": sorted(set(scouts)), "kind_votes": {kind: 1}, "sources_all": sources}

def drop(eid):
    e = by_id.pop(eid)
    els.remove(e)
    return e

def add(e):
    els.append(e)
    by_id[e["id"]] = e

# 1. adapter / decorator
a = by_id["adapter"]
a["aka"] = ["Wrapper (GoF alias, shared with Decorator)"]
add(rebuild("Decorator", "oo-patterns", strip_akas=("Wrapper",)))
by_id["decorator"]["aka"].append("Wrapper (GoF alias, shared with Adapter)")
LOG.append("SPLIT: GoF Decorator had been folded into Adapter (both carry the GoF alias 'Wrapper'); restored as its own element. The shared alias is kept on both entries in annotated, non-colliding form.")

# 2. factory-method / prototype
fm = drop("factory-method")
add(rebuild("Factory Method", "oo-patterns", strip_akas=("Prototype", "clone", "covariant clone")))
add(rebuild("Prototype", "oo-patterns", strip_akas=("Virtual Constructor",)))
by_id["prototype"]["aka"] += ["Virtual Constructor (C++ clone idiom usage)"]
LOG.append("SPLIT: GoF Prototype had been folded into Factory Method ('Virtual Constructor' names Factory Method in GoF but also the C++ clone idiom); restored as its own element; the ambiguous alias annotated on Prototype, GoF's own 'Virtual Constructor' kept on Factory Method.")

# 3. reference-counting / ABA tagged-pointer
rc = by_id["reference-counting"]
ABA_AKAS = {"aba mitigation via tagged pointer", "generation count", "modification counter",
            "stamped reference", "version counter"}
rc["aka"] = [x for x in rc["aka"] if norm(x) not in ABA_AKAS]
add(rebuild("ABA Mitigation via Tagged Pointer", "synchronization-coordination"))
LOG.append("SPLIT: ABA mitigation (tagged pointer / version counter beside a CAS-updated word) had fused into Reference Counting via the shared 'version counter' alias; restored as its own synchronization element - counting for reclamation and counting for ABA-detection are different mechanisms.")

# 4. list-virtualization / stream-windowing
lv = by_id["list-virtualization"]
STREAM_AKAS = {"windowing", "stream windowing", "tumbling window", "fixed window",
               "sliding window", "hopping window", "session window", "window operator"}
lv["aka"] = [x for x in lv["aka"] if norm(x) not in STREAM_AKAS]
lv["scouts"] = [s for s in lv["scouts"] if s != "gap-adversarial"]
lv["sources_all"] = [s for s in lv["sources_all"] if "Dataflow" not in s["src"]]
add(rebuild("Stream Windowing", "data-flow-buffering", strip_akas=("windowing",)))
LOG.append("SPLIT: Stream Windowing (Dataflow Model) had folded into UI list-virtualization via the bare 'windowing' alias; restored; the ambiguous alias dropped from both.")

# 5. setjmp/longjmp duplicate pair
s1 = by_id["setjmp-longjmp-exception-handling"]
s2 = drop("setjmp-longjmp-structured-error-handling")
s1["id"] = "setjmp-longjmp-error-handling"
s1["name"] = "setjmp/longjmp Error Handling"
seen = {norm(x) for x in s1["aka"]} | {norm(s1["name"])}
for x in s2["aka"]:
    if norm(x) not in seen:
        s1["aka"].append(x)
s1["sources_all"] += s2["sources_all"]
s1["scouts"] = sorted(set(s1["scouts"] + s2["scouts"]))
LOG.append("MERGE: the two setjmp/longjmp error-handling entries (corpus-seed and idioms scouts) were one mechanism; merged as setjmp-longjmp-error-handling with Hanson's Except module and CException among the aliases.")

# 6. aka hygiene
crc = by_id["cyclic-redundancy-check"]
crc["aka"] = [x for x in crc["aka"] if norm(x) not in ("message digest for integrity", "checksum")]
LOG.append("AKA: CRC no longer claims 'checksum' (broader family; additive checksums are recorded in CRC's note, not as a second element) nor 'message digest' (cryptographic-hash-function now exists and the conflation is an altitude error).")
by_id["optimistic-ui-update"]["aka"] = [x for x in by_id["optimistic-ui-update"]["aka"] if norm(x) != "latency compensation"]
LOG.append("AKA: 'latency compensation' removed from optimistic-ui-update - it is Bernier's netcode umbrella term (lag-compensation element).")
by_id["lsm-tree"]["aka"] = [x for x in by_id["lsm-tree"]["aka"] if norm(x) != "log structured storage engine"]
LOG.append("AKA: lsm-tree narrowed - 'log-structured storage engine' now names the distinct log-structured-storage element (LFS lineage: append + segment cleaning, no sorted-run merging).")
bs = by_id["byte-stuffing"]
bs["aka"] = [x for x in bs["aka"] if "cobs" not in norm(x) and "bit stuffing" not in norm(x)]
LOG.append("AKA: byte-stuffing no longer lists COBS or bit-stuffing as aliases - both are separate elements (COBS is a distinct algorithmic approach; bit stuffing is the bit-level HDLC variant).")
lru = by_id["lru-cache"]
lru["aka"] = [x for x in lru["aka"] if "eviction-policy variants" not in x]
LOG.append("KEEP-BOTH: lru-cache (the concrete keyed structure: hash map + recency list) vs cache-eviction-policy (the policy family with LRU/LFU/CLOCK/ARC as named members) - structure vs policy; aliases disentangled; Phase 3 relates them.")
by_id["pool-allocation"]["aka"].append("memory slab (Zephyr k_mem_slab)")
by_id["immutable-value"]["aka"].append("Immutable Instance (Fluent C)")
by_id["dedicated-ownership"]["aka"].append("Caller-Owned Instance (Fluent C)")
by_id["enumeration-method"]["aka"].append("Callback Iterator (Fluent C)")
rb = by_id["ring-buffer"]
rb["borderline"] = None
rb["tags"] = [t for t in rb["tags"] if t != "borderline"]

k = by_id["kahan-summation"]
k["borderline"] = "algorithm-variant adjacency (excluded by one hunter, added by another); kept as the one named designer mechanism for compensated float accumulation"
if "borderline" not in k["tags"]:
    k["tags"].append("borderline")
LOG.append("CONFLICT RESOLVED: Kahan summation - one hunter excluded it as algorithmics-zoo, another added it independently; editor keeps it borderline-tagged (the numeric axis's named mechanism for compensated accumulation); deeper variants stay with the datastructures corpus.")
LOG.append("KEEP: LMAX Disruptor kept as its own element against a fold-into-ring-buffer recommendation - a published, named mechanism (preallocated ring + sequence barriers + claim strategies) with its own naming source; Phase 3 relates it to ring-buffer.")
LOG.append("KEEP (block decision): the cryptographic-primitive band (cryptographic hash, MAC, AEAD, CSPRNG, nonce, salted password hashing) kept with borderline tags - designer-reachable named building blocks the rest of the catalog already presupposes (constant-time comparison, Merkle tree, secure zeroization); algorithm families (SHA-2 vs BLAKE3 etc.) stay out.")
LOG.append("ANCHOR COVERAGE: 'semantic data types' (mission calibration anchor) is not a published element name in any source checked (incl. White 2011/2024); the mechanism is covered by newtype (Whole Value folded as alias, Cunningham CHECKS 1994), value-object, quantity, and the new units-of-measure-types (Kennedy). 'Asynchronous programming models' anchor is covered by async-await-model + coroutine + future-promise + event-loop + proactor rather than one umbrella entry.")
LOG.append("HONEST GAP: MPU-based task/memory isolation (FreeRTOS-MPU, Zephyr user mode) is real practice but has no single established element name across vendors - not cataloged; revisit if a citable pattern name emerges. Power-management mechanism names beyond tickless idle (race-to-sleep etc.) similarly failed the establishedness gate.")

# write back
ids = [e["id"] for e in els]
assert len(ids) == len(set(ids)), [i for i in ids if ids.count(i) > 1]
els.sort(key=lambda m: (m["kind"], m["id"]))
data["elements"] = els
with open(os.path.join(SCRATCH, "merged_design.json"), "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=1)
dec = os.path.join(SCRATCH, "decisions_design.json")
old = json.load(open(dec, encoding="utf-8"))["log"] if os.path.exists(dec) else []
with open(dec, "w", encoding="utf-8") as f:
    json.dump({"log": old + LOG}, f, ensure_ascii=False, indent=1)
with open(os.path.join(SCRATCH, "elements_index.txt"), "w", encoding="utf-8") as f:
    for e in sorted(els, key=lambda x: x["id"]):
        f.write(f"{e['id']} | {e['name']} | aka: {', '.join(e['aka'])} | {e['kind']}\n")
print(f"elements: {len(els)}; log entries: {len(old + LOG)}")
for e in ["decorator", "prototype", "aba-mitigation-via-tagged-pointer", "stream-windowing", "setjmp-longjmp-error-handling"]:
    print(" ", e, "->", by_id[e]["kind"], "| aka:", by_id[e]["aka"][:4])
