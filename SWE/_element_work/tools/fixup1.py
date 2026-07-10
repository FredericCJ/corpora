# Adjudication round 1: splits, merges, renames, kind overrides + decision log.
import json, io, sys, os, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
SCRATCH = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(SCRATCH, "merged_design.json"), encoding="utf-8") as f:
    data = json.load(f)
els = data["elements"]
by_id = {e["id"]: e for e in els}
LOG = []

def scout_entry(scout, eid):
    with open(os.path.join(SCRATCH, "sweeps", f"scout-{scout}.json"), encoding="utf-8") as f:
        d = json.load(f)
    for x in d["elements"]:
        if x["id"] == eid:
            return x
    raise KeyError(f"{scout}:{eid}")

def as_merged(x, scout, kind=None, aka=None, drop_aka=()):
    a = aka if aka is not None else list(x.get("aka") or [])
    a = [t for t in a if t.lower() not in {d.lower() for d in drop_aka}]
    return {"id": x["id"], "name": x["name"], "aka": a, "kind": kind or x["kind"],
            "what": x["what"], "problem": x["problem"], "named_in": x["named_in"],
            "named_in_corpus_id": x.get("named_in_corpus_id"), "tags": x.get("tags") or [],
            "borderline": x.get("borderline"), "confidence": x.get("confidence", "established"),
            "scouts": [scout], "kind_votes": {kind or x["kind"]: 1},
            "sources_all": [{"src": x["named_in"], "corpus_id": x.get("named_in_corpus_id")}]}

# ---- 1. split the loop mega-cluster ------------------------------------------
old = by_id.pop("game-loop")
els.remove(old)
super_loop = as_merged(scout_entry("embedded-mech", "super-loop"), "embedded-mech",
                       kind="embedded-systems")
game_loop = as_merged(scout_entry("nystrom-games", "game-loop"), "nystrom-games",
                      drop_aka=("main loop",))
game_loop["aka"] += ["fixed timestep loop", "update-render loop"]
ev = as_merged(scout_entry("concurrency", "event-loop"), "concurrency", drop_aka=("main loop",))
ui_ev = scout_entry("ui-reactive", "event-loop")
for a in ui_ev.get("aka", []):
    if a.lower() not in {x.lower() for x in ev["aka"]} and a.lower() not in ("main loop", "message dispatcher"):
        ev["aka"].append(a)
ev["sources_all"].append({"src": ui_ev["named_in"], "corpus_id": ui_ev.get("named_in_corpus_id")})
ev["scouts"].append("ui-reactive")
md = as_merged(scout_entry("eip-messaging", "message-dispatcher"), "eip-messaging",
               kind="communication")
els += [super_loop, game_loop, ev, md]
LOG.append("SPLIT: transitive-aka fusion of super-loop / game-loop / event-loop / Message Dispatcher (chained via 'main loop' and 'message dispatcher' aliases) split into four elements; 'main loop' kept as alias only on super-loop (in embedded usage it names the superloop; the games/UI senses are folded into their own entries). Four genuinely different mechanisms: bare-metal task cycling (Pont/White), timestep-controlled update-render (Nystrom), event demultiplex-dispatch (event loop), and EIP's dispatcher-to-performers.")

# ---- 2. split test-double out of null-object ----------------------------------
no = by_id["null-object"]
no["aka"] = ["Active Nothing"]
no["kind"] = "oo-patterns"
td = as_merged(scout_entry("wiki-longtail", "test-double"), "wiki-longtail",
               kind="testing-constructs")
els.append(td)
LOG.append("SPLIT: Test Double (Meszaros) had fused into Null Object via shared 'stub' alias; restored as its own element under the new testing-constructs axis. Null Object keeps only 'Active Nothing' as alias. Special Case (PoEAA) kept as a separate element (Fowler's generalization: special-behavior subclasses beyond the null case) - the pair gets a specializes relation in Phase 3 rather than a fold.")

# ---- 3. merge message queues; keep mailbox distinct ----------------------------
mq = by_id["message-queuing"]
eq = by_id.pop("event-queue")
els.remove(eq)
mq["id"] = "message-queue"
mq["name"] = "Message Queue"
mq["aka"] = [a for a in mq["aka"] if a.lower() != "task mailbox"] + ["event queue", "event buffer"]
mq["sources_all"] += eq["sources_all"]
mq["scouts"] = sorted(set(mq["scouts"] + eq["scouts"]))
LOG.append("MERGE: message-queuing (Douglass Queuing + EIP Point-to-Point Channel) and Nystrom's Event Queue are one mechanism - canonicalized as message-queue with 'event queue' folded as alias. 'task mailbox' alias removed: Mailbox stays a separate element (bounded one-slot/small exchange object with RTOS semantics distinct from an unbounded FIFO channel).")

# ---- 4. fold segregated-free-lists into free-list ------------------------------
sfl = by_id.pop("segregated-free-lists")
els.remove(sfl)
fl = by_id["free-list"]
fl["kind"] = "resource-management"
fl["aka"] += ["segregated free lists", "size-class bins"]
fl["sources_all"] += sfl["sources_all"]
fl["scouts"] = sorted(set(fl["scouts"] + sfl["scouts"]))
LOG.append("MERGE: segregated free lists folded into free-list as the size-class refinement (same naming source, Wilson et al. allocation survey); free-list assigned to resource-management (allocator role). TLSF stays a separate element (a specific named two-level policy, not a synonym).")

# ---- 5. renames ----------------------------------------------------------------
ren = by_id["protothreads"]; ren["id"] = "protothread"
LOG.append("RENAME: element id 'protothreads' -> 'protothread' to avoid exact collision with the corpus work id 'protothreads' (Dunkels' paper); the element and the work stay linked via named-in.")
occ = by_id["optimistic-concurrency-via-version-validation"]
occ["id"] = "optimistic-concurrency-control"; occ["name"] = "Optimistic Concurrency Control"
occ["aka"] = sorted(set(occ["aka"] + ["OCC", "optimistic locking", "version validation"]))
LOG.append("RENAME: canonical name for the version-validate-commit mechanism set to the established 'Optimistic Concurrency Control' (Kung & Robinson).")
bp = by_id["back-pressure"]; bp["id"] = "backpressure"; bp["name"] = "Backpressure"
bp["aka"] = [a for a in bp["aka"] if a.lower() != "backpressure"] + ["Back Pressure (Nygard)"]
LOG.append("RENAME: back-pressure -> backpressure (Reactive Streams spelling), Nygard's 'Back Pressure' kept as alias.")
sig = by_id["signals-fine-grained-reactivity"]; sig["id"] = "reactive-signals"

# ---- 6. reference counting canonicalization ------------------------------------
rc = by_id["counted-pointer"]
rc["id"] = "reference-counting"; rc["name"] = "Reference Counting"
rc["aka"] = sorted(set([a for a in rc["aka"] if a] + ["Counted Pointer", "counted body", "refcounting"]))
best = next((s for s in rc["sources_all"] if "Collins" in s["src"] or "Garbage Collection Handbook" in s["src"] or "Jones" in s["src"]), None)
if best:
    rc["named_in"], rc["named_in_corpus_id"] = best["src"], best["corpus_id"]
LOG.append("CANONICALIZATION: the reference-count mechanism entry is named 'Reference Counting' (general mechanism); POSA1's Counted Pointer kept as the idiom alias rather than a second element - one mechanism, one entry. Smart Pointer remains separate (ownership-wrapper family: unique/shared/weak semantics, not only counting).")
sp = by_id["smart-pointer"]
sp["aka"] = [a for a in sp["aka"] if a.lower() not in ("reference-counted pointer", "handle object")]

# ---- 7. context manager folds into dispose pattern -----------------------------
dp = by_id["dispose-pattern"]
dp["aka"] += ["context manager (Python with-statement)"]
if "python" not in dp["tags"]:
    dp["tags"].append("python")
LOG.append("FOLD: Python's context-manager protocol recorded as an alias of the Dispose pattern (same mechanism: deterministic scoped finalization hook) rather than a separate element.")

# ---- 8. kind overrides ----------------------------------------------------------
KIND = {"watchdog": "robustness-security", "leaky-bucket": "scheduling-time",
        "token-bucket": "scheduling-time", "heartbeat": "error-handling",
        "idempotent-receiver": "communication", "checkpointing": "persistence-durability",
        "small-buffer-optimization": "resource-management", "marker-interface": "oo-patterns",
        "special-case": "oo-patterns", "function-pointer-dispatch-table": "oo-patterns",
        "guard-clause": "error-handling", "x-macro": "code-structure",
        "include-guard": "code-structure", "organizing-files-in-modular-c-programs": "code-structure",
        "escaping-ifdef-hell": "code-structure", "service-stub": "testing-constructs",
        "object-mother": "testing-constructs", "test-data-builder": "testing-constructs",
        "humble-object": "testing-constructs", "hydration": "state-management"}
for k, v in KIND.items():
    if k in by_id:
        by_id[k]["kind"] = v
LOG.append("AXES: two axes added to the mission's twenty - code-structure (x-macro, include guard, modular C file organization, #ifdef variant-management patterns: source-level organization mechanisms with no better home) and testing-constructs (test double, service stub, object mother, test data builder, humble object: code-level constructs, not process practices). Kind overrides applied where scout votes split (watchdog->robustness-security, token/leaky bucket->scheduling-time, heartbeat->error-handling, checkpointing->persistence-durability, SBO->resource-management, etc.); kinds remain scaffolding, not ontology.")
LOG.append("KEEP-BOTH decisions (near-miss pairs that are genuinely distinct mechanisms): read/write/behind-through caches; wrapper-facade vs facade; static-factory-method vs factory-method; hardware-proxy/adapter vs GoF proxy/adapter; command vs command-processor; aggregator vs event-aggregator; leaky-bucket (shaper) vs leaky-bucket-counter (Hanmer error counter); bit-stuffing vs byte-stuffing; optimistic vs pessimistic offline lock; lookup (POSA3) vs lookup-table (LUT); loop-timeout (Pont, poll-loop bound) vs timeout (Nygard, blocking-call bound); shadow-paging vs paging (Noble-Weir); monad vs free-monad; visitor vs acyclic-visitor (published variant with its own forces); hooks (Noble-Weir ROM hooks) vs hook-method (Pree) vs ultimate-hook (Samek); delegation vs event-delegation (DOM); stack (structure) vs stack-first (Preschern allocation policy); reactive-programming (model umbrella) vs functional-reactive-programming (Elliott-Hudak) vs reactive-signals (fine-grained implementation) - specializes edges in Phase 3.")
LOG.append("ALIAS AMBIGUITY: 'main loop' names different mechanisms per community (embedded superloop / game loop / event loop) - resolved to super-loop only; search still finds the others by name.")

# ---- write back ------------------------------------------------------------------
ids = [e["id"] for e in els]
assert len(ids) == len(set(ids)), [i for i in ids if ids.count(i) > 1]
els.sort(key=lambda m: (m["kind"], m["id"]))
data["elements"] = els
with open(os.path.join(SCRATCH, "merged_design.json"), "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=1)
dec_path = os.path.join(SCRATCH, "decisions_design.json")
old_log = []
if os.path.exists(dec_path):
    with open(dec_path, encoding="utf-8") as f:
        old_log = json.load(f).get("log", [])
with open(dec_path, "w", encoding="utf-8") as f:
    json.dump({"log": old_log + LOG}, f, ensure_ascii=False, indent=1)
work_ids = {l.split("\t")[0] for l in open(os.path.join(SCRATCH, "work_ids.tsv"), encoding="utf-8")}
print(f"elements now: {len(els)}; work-id collisions: {[e['id'] for e in els if e['id'] in work_ids]}")
print(f"decision log entries: {len(old_log + LOG)}")
from collections import Counter
print("axes:", dict(sorted(Counter(e['kind'] for e in els).items())))
