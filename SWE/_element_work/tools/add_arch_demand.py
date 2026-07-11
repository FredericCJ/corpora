import json, io, sys, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
SCRATCH = os.path.dirname(os.path.abspath(__file__))
os.chdir(SCRATCH)

A = json.load(open("merged_arch.json", encoding="utf-8"))
ids = {e["id"] for e in A["elements"]}

NEW = [
 {"id":"event-driven-architecture","name":"Event-Driven Architecture","kind":"style",
  "aka":["EDA","event-driven system","broker/mediator event topology"],
  "what":"The system is organized around the production, detection, and asynchronous reaction to events, with components emitting and subscribing to event notifications through a mediator or broker rather than calling each other directly.",
  "problem":"Components must stay decoupled and independently scalable while reacting to state changes whose timing and origin they do not control; routing interactions as asynchronous events removes direct dependencies and lets producers and consumers evolve and scale separately.",
  "named_in":"Fundamentals of Software Architecture - Richards & Ford (2020), Event-Driven Architecture Style","named_in_corpus_id":"richardsford",
  "tags":["distributed","enterprise"]},
 {"id":"master-worker","name":"Master-Worker","kind":"pattern",
  "aka":["task farm","master/worker","boss/worker","farmer/worker"],
  "what":"A master component partitions work into independent tasks and dispatches them to a pool of identical worker components, then collects and combines their results.",
  "problem":"A large, largely-independent, throughput-bound workload must be spread across many workers with dynamic load balancing and without workers coordinating with one another; a master centralizes task hand-out and result collection.",
  "named_in":"Patterns for Parallel Programming - Mattson, Sanders & Massingill (2004), Master/Worker pattern","named_in_corpus_id":"mattsonppp",
  "tags":["parallel","concurrency"]},
 {"id":"data-parallel-architecture","name":"Data-Parallel Architecture","kind":"style",
  "aka":["SPMD","single program multiple data","data parallelism","geometric decomposition"],
  "what":"The same program is applied concurrently across partitions of a large regular data set, each unit of execution running identical code over its own data slice (SPMD / geometric decomposition).",
  "problem":"A computation over a large regular data structure must exploit many processing units; partitioning the data and running one program across all partitions converts data size into parallelism while keeping the code single-sourced.",
  "named_in":"Patterns for Parallel Programming - Mattson, Sanders & Massingill (2004), SPMD & Geometric Decomposition patterns","named_in_corpus_id":"mattsonppp",
  "tags":["parallel","hpc"]},
 {"id":"service-registry","name":"Service Registry","kind":"pattern",
  "aka":["service discovery","service directory"],
  "what":"A continually-updated database of available service instances and their network locations, which instances register with on startup and which clients or routers query to discover where to send requests.",
  "problem":"In a dynamic deployment where instances come and go and change location, clients cannot hard-code endpoints; a registry holds the current authoritative map that service discovery uses to route requests.",
  "named_in":"Microservices Patterns - Richardson (2018), Service registry / Service discovery patterns","named_in_corpus_id":"richardsonmp",
  "tags":["distributed","microservices"]},
]
added = []
for x in NEW:
    if x["id"] in ids:
        print("SKIP exists:", x["id"]); continue
    x.update({"realm":"architecture","borderline":None,"confidence":"established","scouts":["editor-p3b-demand"],
              "kind_votes":{x["kind"]:1},"sources_all":[{"src":x["named_in"],"corpus_id":x["named_in_corpus_id"]}]})
    A["elements"].append(x); ids.add(x["id"]); added.append(x["id"])
A["elements"].sort(key=lambda m:(m["kind"],m["id"]))
json.dump(A, open("merged_arch.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)

dec = json.load(open("decisions_arch.json", encoding="utf-8"))
dec["log"].append("DEMAND-DRIVEN GROWTH (Phase 3b feedback): four architecture elements added after bridge agents reported forced convergence onto generic targets - event-driven-architecture (richardsford; event-loop/reactor were funnelling into event-based-implicit-invocation), master-worker (mattsonppp; thread-pool/fork-join were funnelling into the introduce-concurrency tactic), data-parallel-architecture/SPMD (mattsonppp; spmd/parallel-reduction/stencil/loop-parallelism had no data-parallel style), service-registry (richardsonmp; service-locator had only the generic 'discover' tactic). All four naming sources were already in the verified work set.")
json.dump(dec, open("decisions_arch.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)

ED = {"group":"gEDITOR","edges":[
 {"from":"event-loop","kind":"enables","to":"event-driven-architecture","provenance":"editorial","cite":None,"note":"the event loop is the in-process engine that makes an event-driven topology run: it demultiplexes and dispatches the events EDA is organized around"},
 {"from":"reactor","kind":"enables","to":"event-driven-architecture","provenance":"editorial","cite":None,"note":"the reactor's synchronous event demultiplexing is a canonical realization substrate for an event-driven architecture"},
 {"from":"thread-pool","kind":"realizes","to":"master-worker","provenance":"sourced","cite":"mattsonppp, Master/Worker pattern (Supporting Structures): a shared work queue feeding a pool of identical workers","note":"a worker pool draining a task queue is the textbook realization of master/worker"},
 {"from":"fork-join","kind":"enables","to":"master-worker","provenance":"editorial","cite":None,"note":"fork/join task decomposition can be structured as master-dispatched work with joined results"},
 {"from":"work-stealing","kind":"alternative-to","to":"fork-join","provenance":"editorial","cite":None,"note":"work-stealing and centralized fork/join are alternative task-distribution disciplines for the same divide-and-conquer parallelism"},
 {"from":"spmd","kind":"realizes","to":"data-parallel-architecture","provenance":"sourced","cite":"mattsonppp, SPMD pattern","note":"SPMD is the canonical realization of the data-parallel style"},
 {"from":"parallel-reduction","kind":"realizes","to":"data-parallel-architecture","provenance":"editorial","cite":None,"note":"a parallel reduction is a data-parallel collective over a partitioned data set"},
 {"from":"stencil","kind":"realizes","to":"data-parallel-architecture","provenance":"sourced","cite":"mattsonppp, Geometric Decomposition pattern","note":"stencil computation is geometric-decomposition data parallelism"},
 {"from":"loop-parallelism","kind":"realizes","to":"data-parallel-architecture","provenance":"editorial","cite":None,"note":"parallelizing loop iterations over data partitions is the data-parallel style in the small"},
 {"from":"message-translator","kind":"realizes","to":"messaging","provenance":"sourced","cite":"eip, Message Translator sits within the Messaging integration style","note":"in-process payload transformation realized inside a messaging topology (repairs the dropped same-name arch node)"},
 {"from":"seda-staged-event-driven-architecture","kind":"specializes","to":"event-driven-architecture","provenance":"editorial","cite":None,"note":"SEDA is a staged, queue-decoupled specialization of the event-driven style"},
 {"from":"mapreduce","kind":"specializes","to":"data-parallel-architecture","provenance":"editorial","cite":None,"note":"MapReduce is a batch, shuffle-based specialization of data-parallel processing"},
],"unbridged":[],"notes":"editor pass: demand-driven new-node wiring for already-completed groups + message-translator realm repair"}
json.dump(ED, open("p3bridge/gEDITOR.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("added arch elements:", added, "| total arch:", len(A["elements"]), "| editor edges:", len(ED["edges"]))
