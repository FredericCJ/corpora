# Type/functional idioms and concurrency - seed pack (mined 2026-08-08)

**Corpus mined:** `SWE/explorer/data/elements.json` (1083 nodes / 2811 edges / 417 work records),
`design_elements_catalog_v1_0.md`, `architecture_elements_catalog_v1_0.md`,
`design_elements_corpus_v1_0.md`, `design_elements_bridge_v1_1.md`, `explorer/data/corpus.json`.
**Targets:** `manifests/python_typing_contract_manifest.md` (existing, 8 sections) and
`manifests/python_concurrency_determinism_manifest.md` (NEW, does not exist yet).

**Slice census (verified counts, not estimates).** `functional-type-idioms` = **26** elements
(matches the brief). `execution-concurrency` = **37**. `synchronization-coordination` = **57**.
`state-management` = **31**. Every id below was checked against `elements.json` before being written.

**Four ids named in the brief are NOT in `functional-type-idioms`** - the absence is itself a finding,
because it tells you which catalog *kind* to search next time:
`result-type` and `railway-oriented-programming` live in **design/error-handling**;
`immutable-value` lives in **design/state-management**; `smart-constructor` lives in
**design/construction-api**. All four exist; only their filing was mis-predicted.

**Two ids in the brief do not exist at all** and must not be cited under those names:
there is no `event-driven` (the element is **`event-driven-architecture`**, architecture/style) and no
`shared-nothing` (the element is **`shared-nothing-architecture`**, architecture/style).

**Vocabulary the corpus genuinely does NOT have** (checked by full-text scan of `elements.json`):
no element named *"parse, don't validate"* (0 hits - the manifest's own slogan has no corpus name;
its two nearest named equivalents are `smart-constructor` and `functional-core-imperative-shell`);
no `asyncio`, `contextvars`, GIL, free-threading, function-colouring, `assert_never`, or
exhaustiveness element; no `discriminated-union` id (it is an **aka of `tagged-union`**); no
`branded-type`. The SWE corpus contains **no Python-specific concurrency work record at all** - the
single Python-rooted source in the whole concurrency slice is `vorpussc` (Trio's structured-concurrency
essay). Any Python runtime claim in the new manifest must be sourced from python.org, not from here.

---

## Import table

Only elements the target manifest genuinely lacks. Fold candidates are in the next table.

| element id | realm/kind | catalog name | named-in (citable) | Python instantiation | destination manifest + section |
|---|---|---|---|---|---|
| `smart-constructor` | design / construction-api | Smart Constructor | *Smart constructors*, Haskell wiki (living; corpus work `hswikismart`, verified) | The **only** exported way to build the type: `@dataclass(frozen=True, slots=True)` whose `__init__` is not public API, fronted by one `@classmethod parse(cls, raw: object) -> Self` that validates/normalises. Library forms: `pydantic.TypeAdapter(T).validate_python`, `attrs` field `validator=`/`converter=`. Catalog wording to reuse verbatim: "hiding the raw data constructor makes invalid values unrepresentable to the rest of the program." | typing manifest **§5** (replaces the unnamed "Decision - boundary vs core placement") + **Recommendations Stage 2** |
| `result-type` | design / error-handling | Result Type | P1028 *SG14 status_code and standard error object* - N. Douglas, WG21, 2020 (corpus id `p1028`, verified, R3) | `@dataclass(frozen=True, slots=True) class Ok[T]` / `class Err[E]`; `type Result[T, E] = Ok[T] \| Err[E]` (PEP 695); consumed by `match` with a final `case _ as x: assert_never(x)` so the checker proves exhaustiveness. Library: `returns.result`. The corpus aka list includes `expected`, `outcome`, `error union` - useful when the team argues over naming. | typing manifest **§5** (new "Which error channel" subsection) + **§7** (`Raises:` vs typed failure) |
| `railway-oriented-programming` | design / error-handling | Railway-Oriented Programming | *Railway Oriented Programming* - Scott Wlaschin, fsharpforfunandprofit.com / NDC, 2014 (`wlaschinrop`, verified) | A `bind(f, r)` helper folded over a list of `Result`-returning steps, or `returns.pipeline.flow(...).bind(...)`. In plain stdlib: an early-return `for step in steps:` loop that short-circuits on the first `Err`. | typing manifest **§5**, immediately after `result-type` |
| `tagged-union` | design / data-representation | Tagged Union | *Types and Programming Languages* - Benjamin C. Pierce, 2002, MIT Press, ISBN 0-262-16209-1 (`piercetapl`, verified) | A `Literal["circle"]` tag field on each frozen dataclass + `type Shape = Circle \| Square` + `match`/`assert_never`. pydantic form: `Annotated[Union[...], Field(discriminator="kind")]`. Catalog wording: "enables exhaustive case analysis so unhandled alternatives are caught statically." | typing manifest **§2**, directly after the `Enum`/`Literal` bullet |
| `notification` | design / error-handling | Notification | *Notification* - Martin Fowler, eaaDev (`eaadev`, living, verified) | This is exactly what `pydantic.ValidationError.errors()` returns: **all** field failures accumulated, not the first. Stdlib form: a `list[Problem]` returned from a validator instead of raising. | typing manifest **§5** (names the semantics the pydantic bullet already describes but cannot refer to) |
| `quantity` | design / data-representation | Quantity | *Analysis Patterns: Reusable Object Models* - Martin Fowler, 1996 (`fowleranalysis`, verified) | `pint.Quantity`, `astropy.units`, or a frozen dataclass `Measure(value: float, unit: Unit)` whose `__add__` rejects mismatched units at runtime. **This is Python's real answer to units, not `NewType`.** | typing manifest **§4**, units-of-measure bullet |
| `phantom-type` | design / functional-type-idioms | Phantom Type | *Domain Specific Embedded Compilers* - Leijen & Meijer, DSL '99, 1999 (`leijenmeijer99`, **UNVERIFIED**) | PEP 695: `class Tainted[S]: __slots__ = ("raw",)` with `S` never stored; marker classes `class Raw: ...` / `class Clean: ...`; the checker separates `Tainted[Raw]` from `Tainted[Clean]` at zero runtime cost. Catalog wording: "a type parameter that appears in a type's signature but not in its runtime representation." | typing manifest **§2** (new bullet) and **§4** (mechanism for the typestate bullet) |
| `sealed-trait` | design / functional-type-idioms | Sealed Trait | Rust API Guidelines, C-SEALED (`rustapiguidelines`, living, verified) | Python has **no** sealing mechanism. The transposable half: `@final` on every variant class + a module-level `type X = A \| B` alias that is the only public spelling, so adding a variant is a visible edit to one line. Enforcement is checker-and-convention, never runtime. | typing manifest **§2**, next to `tagged-union` |
| `immutable-value` | design / state-management | Immutable Value | *POSA Vol. 4: A Pattern Language for Distributed Computing* - Buschmann, Henney, Schmidt, 2007 (`posa4`, verified) | `@dataclass(frozen=True, slots=True)` with `tuple`/`frozenset`/`Mapping` field types. The catalog problem statement is the sentence §6 is missing: "Shared mutable values require defensive copies or synchronization; immutability makes sharing safe by construction." | typing manifest **§6** (gives the section its name) + concurrency manifest (shared read-only state) |
| `defensive-copy` | design / robustness-security | Defensive Copy | *Effective Java*, 3rd ed. - Joshua Bloch, 2018, Item 50 (`effjava`, verified) | `tuple(items)` / `dict(mapping)` / `frozenset(...)` in `__post_init__` (via `object.__setattr__` when frozen); `copy.deepcopy` at trust boundaries; return `types.MappingProxyType(self._d)` from accessors. | typing manifest **§6** - the concrete fix for the "frozen dataclass holding a `list`" hole the manifest identifies but leaves open |
| `persistent-data-structure` | design / data-structures | Persistent Data Structure | *Making Data Structures Persistent* - Driscoll, Sarnak, Sleator & Tarjan, JCSS 1989 (**naming source has no corpus work record**; the carrying corpus work is `okasaki`, *Purely Functional Data Structures*, 1998, doi:10.1017/CBO9780511530104, verified) | `pyrsistent.PMap`/`PVector`; `immutables.Map` - the HAMT that **CPython's own `contextvars` is implemented on**. Third option in §6 alongside frozen-and-shallow and copy-defensively. | typing manifest **§6** + concurrency manifest (lock-free shared snapshots) |
| `lens` | design / functional-type-idioms | Lens | *Combinators for Bi-Directional Tree Transformations* - Foster, Greenwald, Moore, Pierce, Schmitt, ACM TOPLAS 29(3), 2007 (`fosterlenses`, verified) | No idiomatic optics library in Python. The transposable core is `dataclasses.replace(outer, inner=replace(outer.inner, f=v))` wrapped in small named `with_*` helpers; `BaseModel.model_copy(update=...)` is the shallow pydantic form. Import the **name and the problem** ("each level otherwise requires manual copy-and-replace code"), not the machinery. | typing manifest **§6** - answers "how do I update a nested frozen record", which the manifest never addresses |
| `functional-core-imperative-shell` | design / functional-type-idioms | Functional Core, Imperative Shell | *Functional Core, Imperative Shell* - Gary Bernhardt, Destroy All Software screencast, 2012 (`bernhardtfcis`, verified) | A pure module of `def decide(state, event) -> list[Command]` that imports no clock, no `httpx`, no session; a thin `async def handle()` at the edge performing all IO. Catalog aka: **"impureim sandwich"**. | **BOTH**: typing manifest §5 (names the boundary/core decision) and concurrency manifest (determinism - it `realizes` `limit-nondeterminism`) |
| `defunctionalization` | design / functional-type-idioms | Defunctionalization | *Definitional Interpreters for Higher-Order Programming Languages* - John C. Reynolds, 1972 (`reynolds72`, verified) | The non-obvious high-value import: `ProcessPoolExecutor`/`multiprocessing` **cannot pickle lambdas or closures**, so cross-process work must be represented as a frozen-dataclass tagged union plus a top-level `def apply(job)` dispatcher. Catalog problem: "turning behavior into data" so higher-order programs can be "serialized, stored, or sent". | concurrency manifest, **process-pool / job-submission section** |
| `trampoline` | design / execution-concurrency | Trampoline | *Trampolined Style* - Ganz, Friedman & Wand, ICFP '99, pp. 18-27 (`ganztrampoline`, verified) | CPython has no tail-call elimination; raising `sys.setrecursionlimit` is not a fix. Convert deep or mutual recursion into `while` over returned step objects/closures. Edges: `trampoline --uses--> thunk`; `trampoline --realizes--> exception-prevention` ("prevents stack-overflow failures from arising at all"). | concurrency manifest, **"the stack is a bounded resource"** |
| `collection-pipeline` | design / functional-type-idioms | Collection Pipeline | *Collection Pipeline* - Martin Fowler, martinfowler.com, 2015 (`fowlerpipeline`, verified) | Generator expressions + `itertools`; `async for` over async generators for the streaming form. The value is the sourced edge `collection-pipeline --realizes--> pipes-and-filters`, which licenses one vocabulary across in-process and system scale. | concurrency manifest, **in-process dataflow** |
| `structured-concurrency` | design / execution-concurrency | Structured Concurrency | *Notes on structured concurrency, or: Go statement considered harmful* - Nathaniel J. Smith, vorpus.org, 2018-04-25 (`vorpussc`, verified) | `asyncio.TaskGroup` (3.11+) / `trio.open_nursery`. The catalog's aka list already contains **"nursery (Trio)"**. Rule this licenses: a bare `asyncio.create_task` with no scope owner is a spec violation, because "fire-and-forget spawning breaks local reasoning, error propagation, and cancellation." | concurrency manifest, **task lifetime (§1)** |
| `cancellation-token` | design / execution-concurrency | Cancellation Token | *Cancellation in Managed Threads* - Microsoft Learn (living; `mscancellation`, verified). named-in also credits Ajmani, "Go Concurrency Patterns: Context" (2014) - **that blog has no corpus work record** | asyncio: `Task.cancel()` delivers `CancelledError` **at the next await point** (exception-delivered, not polled); `asyncio.timeout()`/`timeout_at()` are the scoped form. Threads: there is **no** stdlib token - pass a `threading.Event` and poll it, exactly the catalog's "poll or subscribe to, exiting cooperatively." | concurrency manifest, **cancellation (§2)** |
| `two-phase-termination` | design / execution-concurrency | Two-Phase Termination | *Patterns in Java, Vol. 1* - Mark Grand, 1998 (`grandjava`, verified) | `loop.add_signal_handler` sets an `asyncio.Event`; producers stop; `await queue.join()`; then cancel workers. Threads: `ThreadPoolExecutor.shutdown(wait=True, cancel_futures=...)`. Catalog problem statement is the rule: "Forcibly killing threads corrupts shared state and leaks resources." | concurrency manifest, **shutdown (§3)** |
| `run-to-completion-event-processing` | design / state-management | Run-to-Completion Event Processing | *Practical UML Statecharts in C/C++*, 2nd ed. - Miro Samek, 2008, Newnes, ISBN 978-0-7506-8706-5 (`samekbook`, verified) | **The missing name for asyncio's core guarantee.** A coroutine step between two `await`s is never interleaved with another task on the same loop, so await-free critical sections need no lock - and inserting one `await` inside them re-opens the window. Catalog: "the machine is never observed mid-transition." | concurrency manifest, **§0 the execution model** (highest-leverage single import) |
| `reactor` / `proactor` | design / execution-concurrency | Reactor; Proactor | *POSA Vol. 2* - Schmidt, Stal, Rohnert, Buschmann (`posa2`, **UNVERIFIED, year UNRESOLVED**) | Python **names its own classes after these**: `asyncio.SelectorEventLoop` is a reactor over `selectors` (readiness-based); `WindowsProactorEventLoopPolicy` is a proactor over IOCP (completion-based). The sourced edge `proactor --alternative-to--> reactor` ("same event-demux role, opposite I/O model") explains the platform split in one line. | concurrency manifest, **§0 the execution model** |
| `half-sync-half-async` | design / execution-concurrency | Half-Sync/Half-Async | *POSA Vol. 2* (`posa2`, **UNVERIFIED**) | `asyncio.to_thread` / `loop.run_in_executor` **is** the queueing layer between the asynchronous layer and blocking service threads. Names the discipline: "combine the performance of asynchronous event handling with the programming simplicity of synchronous code, without either style polluting the other." | concurrency manifest, **blocking-call quarantine** |
| `producer-consumer` | design / communication | Producer-Consumer | *Cooperating Sequential Processes* (EWD123) - Dijkstra, 1965 (`ewd123`, verified; also `downeysem`, Downey, *The Little Book of Semaphores*, verified) | `asyncio.Queue(maxsize=N)` / `queue.Queue(maxsize=N)`. Catalog aka: **"bounded buffer"** - the word *bounded* is the whole point. | concurrency manifest, **queues (§4)** |
| `backpressure` | design / data-flow-buffering | Backpressure | *Release It!*, 2nd ed. - Michael Nygard, 2018 (`nygard`, **UNVERIFIED, year UNRESOLVED**); also *Reactive Streams Specification* (`reactivestreams`, living, verified) | `await queue.put(x)` on a bounded queue *is* backpressure; `queue.put_nowait` discards it. Catalog problem: "Unbounded queues hide overload until memory or latency blows up." | concurrency manifest, **queues (§4)** |
| `thread-confinement` | design / synchronization-coordination | Thread Confinement | *Java Concurrency in Practice* - Goetz et al., 2006, ISBN 978-0-321-34960-6 (`jcip`, verified) | One owning task/thread per mutable structure; `loop.call_soon_threadsafe` as the only cross-thread door. "If data is only ever touched by one thread, thread safety follows by construction." | concurrency manifest, **§5 ownership** |
| `thread-specific-storage` | design / execution-concurrency | Thread-Specific Storage | *POSA Vol. 2* (`posa2`, **UNVERIFIED**) | `threading.local()` - and the load-bearing Python warning: it is **wrong** in asyncio because many tasks share one thread. `contextvars.ContextVar` is the per-task analogue. | concurrency manifest, **§5 ownership** (paired with the next row) |
| `context-object` | design / state-management | Context Object | *POSA Vol. 4* - Buschmann, Henney, Schmidt, 2007 (`posa4`, verified) | An explicit `RequestContext` frozen dataclass threaded through calls. The editorial edge `context-object --alternative-to--> thread-specific-storage` ("pass it explicitly vs stash it in thread-local storage") is exactly the `contextvars`-vs-parameter decision the new manifest must state. | concurrency manifest, **§5 ownership** |
| `deadline-propagation` | design / scheduling-time | Deadline Propagation | *Site Reliability Engineering* - Beyer, Jones, Petoff, Murphy (eds.), 2016 (`googlesre`, verified) | Pass an **absolute** deadline down the call chain; enforce with `asyncio.timeout_at(deadline)` at each stage. Sourced edge `deadline-propagation --realizes--> timeout-tactic`. Catalog problem: "independent per-hop timeouts let deep call chains do work the original caller has already abandoned." | concurrency manifest, **timeouts (§6)** |
| `self-pipe-trick` | design / synchronization-coordination | Self-Pipe Trick | *The Linux Programming Interface* - Michael Kerrisk, 2010, sec. 63.5.2 (`kerrisktlpi`, verified) | `signal.set_wakeup_fd` and `loop.add_signal_handler`; `socket.socketpair()` for the Windows fallback. Explains **why** signal handling and event loops need a bridge: "signals interrupt at arbitrary points and cannot safely do real work, and select/poll cannot wait on them directly." | concurrency manifest, **signals** |
| `asynchronous-completion-token` | design / execution-concurrency | Asynchronous Completion Token | *POSA Vol. 2* (`posa2`, **UNVERIFIED**) | `dict[req_id, asyncio.Future]` for any multiplexed protocol client (JSON-RPC, AMQP, custom framing) - "re-associate each completion with the context needed to process it, without searching." | concurrency manifest, **multiplexed clients** |
| `competing-consumers` + `sequential-convoy` | design / execution-concurrency; architecture / pattern | Competing Consumers; Sequential Convoy | *Enterprise Integration Patterns* - Hohpe & Woolf, 2003 (`hohpe`, verified); Azure Architecture Center Cloud Design Patterns (`azurepatterns`, living, verified - see the caveat in Sources) | N worker tasks pulling one `asyncio.Queue`; when per-key order must survive, hash the key to one of N single-consumer queues. Convoy exists precisely because "per-key ordering must survive in a competing-consumers world that otherwise destroys sequence." | concurrency manifest, **worker fleets (§4)** |
| `limit-nondeterminism` | architecture / tactic | Limit Nondeterminism | *Software Architecture in Practice*, 4th ed. - Bass, Clements & Kazman, 2021, ISBN 978-0-13-688609-9 (`bck`, verified) | Inject a `Clock` protocol instead of calling `datetime.now()`; own a `random.Random(seed)` instance instead of module-level `random`; monotonic counters instead of wall-clock ordering; fix `PYTHONHASHSEED` in CI. The tactic's own framing is the manifest's thesis: "nondeterministic systems are pernicious to test because failures do not reproduce." | concurrency manifest - **name the whole manifest around this tactic** |
| `logical-clock` | design / synchronization-coordination | Logical Clock | Lamport, *Time, Clocks, and the Ordering of Events in a Distributed System*, CACM 1978 (`lamportclocks`, verified; also `kleppmannddia`) | A monotonically increasing per-process sequence number attached to every emitted event, merged on receipt - the ordering primitive when `time.time()` is not trustworthy and `time.monotonic()` is per-process. aka includes "vector clock", "version vector", "hybrid logical clock". | concurrency manifest, **event ordering** |
| `deterministic-lockstep` | design / state-management | Deterministic Lockstep | Fiedler, *Deterministic Lockstep* (gafferongames.com, verified live per corpus note); Bettner & Terrano, GDC 2001 (`gafferongames`, verified) | The strongest form of the determinism claim: replay a run from a seed plus an ordered input log and get a bit-identical result. In Python this is the design that makes record/replay testing of a concurrent core possible - and it is only reachable if the core is `functional-core-imperative-shell`. | concurrency manifest, **record/replay testing** |
| `multi-state-task` | design / execution-concurrency | Multi-State Task | *Patterns for Time-Triggered Embedded Systems* - M. J. Pont, 2001 (`pont`, **UNVERIFIED**) | For CPU-bound work that must run on the loop thread: chunk it and `await asyncio.sleep(0)` between steps. The catalog problem statement transposes exactly: "a cooperative scheduler cannot tolerate tasks that block or run long." | concurrency manifest, **don't block the loop** |
| `bulkhead` | design / resource-management | Bulkhead | *Release It!* - Nygard (`nygard`, **UNVERIFIED**) | A separate `asyncio.Semaphore` (or separate executor) per downstream dependency, so one slow dependency cannot consume all concurrency. Sourced edge `bulkhead --realizes--> bulkhead-deployment-isolation` ties the in-process and deployment forms together. | concurrency manifest, **resource partitioning** |
| `actor-based-architecture` | architecture / style | Actor-Based Architecture | Hewitt, Bishop & Steiger, *A Universal Modular ACTOR Formalism for Artificial Intelligence*, IJCAI-73, 1973 (`hewitt1973`, verified) | One `asyncio.Queue` + one owning task per stateful resource; callers send messages, never touch state. Style statement: "message-owned state removes locks and makes distribution and supervision natural." | concurrency manifest, **§7 architecture options** |
| `shared-nothing-architecture` | architecture / style | Shared-Nothing Architecture | Stonebraker, *The Case for Shared Nothing*, IEEE Database Engineering Bulletin 9(1), 1986 (`sharednothing`, **UNVERIFIED - no DOI exists**) | The honest Python answer to CPU-bound scaling: process-per-core with **no** shared mutable state, coordinating only by messages. Name it so the manifest can say why `multiprocessing.Manager` shared state is the anti-pattern. | concurrency manifest, **§7 architecture options** |
| `pipes-and-filters` | architecture / style | Pipes and Filters | *POSA Vol. 1* - Buschmann, Meunier, Rohnert, Sommerlad, Stal, 1996 (`posa1`, verified) | Stages as tasks joined by bounded `asyncio.Queue`s (or generators for the single-threaded form). Two sourced edges make it the spine of the dataflow section: `pipeline-parallelism --realizes--> pipes-and-filters` and `coroutine --enables--> pipes-and-filters` ("Conway's original coroutine use was a pipeline"). | concurrency manifest, **§7 architecture options** |
| `bound-queue-sizes` | architecture / tactic | Bound Queue Sizes | *Software Architecture in Practice*, 4th ed. (`bck`, verified) | `asyncio.Queue()` defaults to `maxsize=0` = **unbounded**. The tactic requires "an explicit policy for what happens when queues overflow" - so an unbounded queue in a spec'd system is a defect, not a default. | concurrency manifest, **queues (§4)** and Recommendations |

---

## Fold table

Vocabulary the target already teaches under another name. Fold, record the synonym, do not re-import.

| element id | catalog name | the manifest already calls this | note |
|---|---|---|---|
| `newtype` | Newtype | **`typing.NewType`** (typing manifest §2, verbatim: "prevent mixing semantically different values that share a representation") | Exact synonym. Import only the corpus **aka list** ("tiny types", "whole value (related CHECKS pattern)", "strong typedef", "micro type") and the sourced edge `smart-constructor --composes-with--> newtype`, whose note is the rule §2 is missing: "A smart constructor wraps a newtype and is exported instead of the raw constructor, so the type's invariant cannot be bypassed." |
| `option-type` | Option Type | **`Optional[T]` / `T \| None`** (§2, §7) | Same thing. Two things worth lifting: the sourced edge `option-type --specializes--> tagged-union` (Option is the two-case sum type) and `result-type --alternative-to--> option-type`, note: "Result carries an error value where Option only signals presence/absence with no reason." **Provenance caveat:** `named_in` is "Haskell 98 Language and Libraries Report (2003)" but that report is **not** a corpus work record; the backing works are `huttonhaskell` and `rustbook`. |
| `typestate` | Typestate | **§4, "Stateful protocols / typestate (ESTABLISHED)"** - already named | The manifest names it only to declare it impossible. See REFINES item 1: the corpus supplies the mechanism (`phantom-type --implements--> typestate`, sourced) and the tactic (`typestate --realizes--> interlock`), which turns a flat "no" into a partial yes. |
| `units-of-measure-types` | Units-of-Measure Types | **§4, "Units of measure (ESTABLISHED)"** - already named | Fold the name; import instead the **`alternative-to` pair** `units-of-measure-types --alternative-to--> quantity` and the sourced mechanism `units-of-measure-types --uses--> phantom-type` (Kennedy 2009; boost::units; Haskell `dimensional`). |
| `interior-mutability` | Interior Mutability | **§5/§6's `object.__setattr__(self, name, value)` workaround** on frozen dataclasses | The manifest presents this as a wart in §6 ("`object.__setattr__` can bypass the freeze entirely") and as a *required technique* in §5 (derived fields in `__post_init__`) without connecting the two. `interior-mutability` is the name that connects them, plus the tradeoff edge `interior-mutability --alternative-to--> immutable-value`. |
| `value-semantics`, `copied-value` | Value Semantics; Copied Value | **§6's read-only-container and frozen-dataclass discussion** | C++/enterprise framing (`iglberger`, `posa4`). `copied-value --implements--> value-semantics`, and both `--enables--> introduce-concurrency`. Keep as a one-line mention in the concurrency manifest's "why immutability" paragraph; `defensive-copy` and `immutable-value` are the importable Python-shaped forms. |
| `currying-partial-application` | Currying / Partial Application | **`functools.partial`** - the corpus aka literally reads "functools.partial (Python realization)" | Already ambient in Python. Not a contract element; no manifest section needs it. |
| `monitor-object`, `scoped-locking`, `condition-variable`, `semaphore`, `reentrant-lock`, `readers-writer-lock`, `latch` | (POSA2 / Hoare / Dijkstra / JCiP synchronizers) | The stdlib: `threading.Lock`, `with lock:` (= scoped locking, RAII), `RLock`, `Condition`, `Semaphore`, `Event`/`Barrier`, and their `asyncio.*` twins | Fold as a **mapping table**, one row each, in a "the runtime already gives you these" section - not as imported vocabulary. Two edges are worth stating outright: `thread-safe-interface --alternative-to--> reentrant-lock` (restructure vs `RLock`) and `balking --alternative-to--> guarded-suspension` (`lock.locked()` early-return vs `async with lock`). Python has **no** stdlib readers-writer lock - state that absence. |
| `executor`, `thread-pool`, `future-promise`, `fork-join` | Executor; Thread Pool; Future/Promise; Fork-Join | `concurrent.futures.Executor` / `ThreadPoolExecutor` / `Future`; `asyncio.gather` + `TaskGroup` | Python's `concurrent.futures` is a near-literal transliteration of the JCiP Executor framework. Fold the names, keep the sourced edge `executor --composes-with--> thread-pool` (JCiP ch. 6) to explain why submission policy and execution policy are separate knobs. |
| `coroutine`, `async-await-model` | Coroutine; Async-Await Model | `async def` / `await` - the language itself | Fold, but cite: Conway 1963 (`conway1963`, verified) for coroutine and Syme, Petricek & Lomov, *The F# Asynchronous Programming Model*, 2011 (`symeasync`, verified) for async/await - a non-obvious, citable origin for a Python manifest. Keep the sourced edge `async-await-model --specializes--> coroutine` ("async functions are stackless coroutines"). |
| `event-loop` | Event Loop | `asyncio.EventLoop` | Fold the name. **Provenance caveat:** the element's `named_in` is literally *"Event loop - Wikipedia"*; the backing works are `nodeeventloop` (verified) and `posa2` (unverified). Cite `reactor`/POSA2 or Node's docs, not the Wikipedia string. |
| `ring-buffer` | Ring Buffer | `collections.deque(maxlen=n)` | The bounded, overwriting FIFO is in the stdlib. Fold; do not import the lock-free variants. |
| `green-threads` | Green Threads | gevent/eventlet (historical) | Fold as history. The editorial edge `green-threads --alternative-to--> async-await-model` ("stackful user-space threads vs stackless compiler-rewritten async functions") is the exact axis of the gevent-vs-asyncio choice and the reason `await` must be written explicitly. **Provenance caveat:** `named_in` is "Green thread - Wikipedia"; backing work is `jep444`. |
| `timeout` | Timeout | `asyncio.timeout()` / socket timeouts | Fold; keep the sourced same-name edge `timeout --realizes--> timeout-tactic` so the design mechanism and the BCK tactic stay linked. |
| `safe-publication` | Safe Publication | (no manifest section yet) | Fold into a **mention**: the JCiP discipline concerns a memory model Python does not expose to application code. Say what the runtime does for you, and flag free-threading as an open item - the corpus has zero coverage of it. |

---

## Relations worth stating

Edges lifted from `elements.json`. `[S]` = `provenance: "sourced"` (a citable source states the
relation), `[E]` = `provenance: "editorial"` (house judgment, marked as such in the corpus - present it
that way, never as a fact).

**Why a mechanism is chosen (the `realizes` / `enables` spine).**

1. `superloop-architecture --constrains--> multi-state-task` `[E]` - *"The no-OS cooperative loop
   forbids blocking waits, forcing long activities into stepwise state-machine form."* This is the
   single design law of an asyncio codebase, and it is a **`constrains`** edge: architecture dictating
   design. Only two `constrains` edges touch this whole slice; this is the load-bearing one.
2. `finite-state-machine --uses--> run-to-completion-event-processing` `[S]` (Samek, PSiCC2 ch. 2) -
   *"processes each event fully before dequeuing the next, never observed mid-transition."* The
   property that makes await-free code implicitly atomic.
3. `run-to-completion-event-processing --enables--> actor-based-architecture` `[S]` (Samek) - *"actor /
   active-object message processing depends on RTC semantics to avoid reentrant state corruption."*
   State this before recommending a queue-per-resource design.
4. `structured-concurrency --realizes--> limit-nondeterminism` `[E]` - *"Confining task lifetimes to
   lexical scopes eliminates unconstrained parallelism (orphaned tasks, leaked threads)."*
5. `thread-confinement --realizes--> limit-nondeterminism` `[E]` and
   `functional-core-imperative-shell --realizes--> limit-nondeterminism` `[E]` - *"a pure core is
   deterministic and testable without mocks; nondeterminism is confined to the shell."* Three named
   mechanisms realising **one** tactic: that is the new manifest's whole argument in one sentence.
6. `immutable-value --enables--> introduce-concurrency` `[E]`, `value-semantics --enables-->
   introduce-concurrency` `[E]`, `copied-value --enables--> introduce-concurrency` `[E]`,
   `safe-publication --enables--> introduce-concurrency` `[E]` - four routes to the same tactic; the
   typing manifest's §6 immutability work is a **prerequisite** for the concurrency manifest, not a
   separate topic.
7. `producer-consumer --realizes--> queue-based-load-leveling` `[E]` and `bound-queue-sizes
   --composes-with--> queue-based-load-leveling` `[E]` - *"A load-leveling buffer smooths bursts;
   bounding its size sets the overflow policy that protects resources."* Together: an unbounded
   `asyncio.Queue()` is not load-levelling, it is a memory leak with a nice API.
8. `backpressure --realizes--> manage-event-arrival` `[E]` - backpressure is the in-band mechanism of
   the arrival-rate tactic; `token-bucket` and `throttle` are the out-of-band ones.
9. `deadline-propagation --realizes--> timeout-tactic` `[S]` (Google SRE, "Addressing Cascading
   Failures") - *"deadline propagation described as the distributed form of per-stage timeouts."*
10. `cancellation-token --realizes--> cancel` `[E]` **and** `--realizes--> timeout-tactic` `[E]` - one
    mechanism serves two tactics; that is why `asyncio.timeout()` is built on cancellation.
11. `option-type`, `newtype`, `tagged-union`, `phantom-type`, `units-of-measure-types`,
    `smart-constructor` and `trampoline` **all `--realizes--> exception-prevention`** `[E]` (BCK
    tactic: keep faults from arising). This reframes the typing manifest's §4 from a negative
    inventory ("what the type system cannot express") into a positive one ("six named ADT-based
    prevention mechanisms, and which of them Python supports").
12. `result-type --realizes--> exception-handling` `[E]` - *"the typed evolution of the tactic's
    return-code end of the handling-mechanism range."* `Result` and `raise` are two points on **one**
    BCK spectrum, not rival religions.
13. `typestate --realizes--> interlock` `[E]` - *"encoding protocol state in types enforces legal
    operation ordering - the interlock tactic's ordering protection, moved to compile time."*
14. `collection-pipeline --realizes--> pipes-and-filters` `[S]` (Fowler), `pipeline-parallelism
    --realizes--> pipes-and-filters` `[S]` (Garlan & Shaw) and `coroutine --enables-->
    pipes-and-filters` `[E]` - the same style at three altitudes, so one vocabulary covers generators,
    task pipelines and system topology.
15. `thread-confinement --enables--> lmax-architecture` `[E]` - *"the single-threaded business logic
    processor is thread confinement applied at system scale."* The citable precedent for "one process,
    one writer, everything else is IO."

**Which of two mechanisms to pick (the `alternative-to` decision rules).**

16. `defensive-copy --alternative-to--> immutable-value` `[S]` (Bloch, *Effective Java*: "make
    defensive copies" / "minimize mutability") - *"Both stop external aliases mutating internal state;
    immutability removes the need, else copy defensively."* Precisely the choice §6 leaves open.
17. `interior-mutability --alternative-to--> immutable-value` `[E]` - *"Given a shared reference, keep
    the value truly immutable or allow controlled runtime-checked mutation."*
18. `units-of-measure-types --alternative-to--> quantity` `[E]` - *"Static type-level vs runtime
    value-object realization of unit-safe arithmetic."* Python can only take the second branch well.
19. `units-of-measure-types --alternative-to--> newtype` `[E]` - type-level unit parameters vs
    wrapping quantities in distinct newtypes: the manifest currently recommends only the weakest of
    the three options without naming the other two.
20. `result-type --alternative-to--> option-type` `[E]`; `notification --alternative-to--> result-type`
    `[E]` (*"Gather all errors before returning vs short-circuiting on the first error value"*);
    `return-status-code --alternative-to--> result-type` `[E]`; `sealed-trait --alternative-to-->
    tagged-union` `[E]`; `type-safe-enum --alternative-to--> tagged-union` `[E]`. A five-way named
    decision space for "how does failure or variance leave a function" - the typing manifest currently
    has one channel (`raise`) and one doc convention (`Raises:`).
21. `functional-core-imperative-shell --alternative-to--> monad` `[S]` (Mark Seemann, *Impureim
    sandwich*, ploeh blog, 2020) - *"Both separate pure logic from effects: an impure/pure/impure
    boundary vs type-level (IO) monadic sequencing."* The citable reason Python takes the FCIS branch
    and drops the monad branch.
22. `thread-confinement --alternative-to--> monitor-object` `[S]` (JCiP ch. 3) - *"Confining data to
    one thread removes shared mutable state, avoiding the locking a monitor provides."* Confine **or**
    lock; doing both badly is the common failure.
23. `context-object --alternative-to--> thread-specific-storage` `[E]` - *"Both supply ambient
    execution-scoped state: pass it explicitly in a context object vs stash it in thread-local
    storage."* The `contextvars`-vs-parameter decision, stated once.
24. `green-threads --alternative-to--> async-await-model` `[E]`; `coroutine --alternative-to-->
    green-threads` `[E]`; `proactor --alternative-to--> reactor` `[S]` (POSA2); `leader-followers
    --alternative-to--> half-sync-half-async` `[S]` (POSA2: *"L/F trades the queue layer away for
    lower latency"*). The four axes of "which concurrency substrate".
25. `balking --alternative-to--> guarded-suspension` `[E]` - *"Same trigger (precondition not met):
    balking returns/fails immediately, guarded suspension waits until the guard holds."*
26. `thunk --alternative-to--> future-promise` `[E]` - *"a thunk is lazy/synchronous, a future is
    asynchronous."* Names the `functools.cached_property` vs `asyncio.Future` distinction.
27. `deadlock-detection --alternative-to--> ordered-locking` `[S]` (Silberschatz) - prevention up front
    vs detect-then-abort. Python offers neither mechanism; ordered locking is the only available branch.
28. `fork-join --alternative-to--> master-slave` `[E]`, `spmd --alternative-to--> master-slave` `[S]`
    (Mattson et al., *Supporting Structures*), `pipeline-parallelism --alternative-to-->
    loop-parallelism` `[E]` - the four peer choices for structuring parallel work
    (`TaskGroup` / `Pool.map` / staged tasks / SPMD-style rank code).

**Composition rules (what must be paired).**

29. `smart-constructor --composes-with--> newtype` `[S]` (Haskell wiki) - the
    invariant-cannot-be-bypassed rule; plus `smart-constructor --specializes--> static-factory-method`
    `[E]`.
30. `railway-oriented-programming --composes-with--> result-type` `[S]` (Wlaschin) - ROP is *defined*
    as composition over Results; do not present them as two ideas.
31. `structured-concurrency --composes-with--> cancellation-token` `[S]` (Trio nurseries / Smith 2018)
    - *"a task scope cancels its whole child tree via a scope-bound cancellation token"*; plus
    `--composes-with--> two-phase-termination` `[E]` (*"exiting a task scope requires all children to
    reach a clean terminated state first"*) and `--composes-with--> future-promise` `[E]`.
32. `cancellation-token --composes-with--> deadline-propagation` `[S]` (Go `context.Context` carries
    both `Done()` and `Deadline()`) and `two-phase-termination --uses--> cancellation-token` `[E]`
    (*"the phase-1 termination request is exactly a cancellation flag the target polls at safe
    points"*).
33. `thread-confinement --uses--> thread-specific-storage` `[S]` (JCiP 3.3.3) and `--composes-with-->
    safe-publication` `[E]` (serial thread confinement = hand-off via a safe-publication step).
34. `pipeline-parallelism --uses--> producer-consumer` `[S]` (Mattson et al.) - *"adjacent stages are
    producer/consumer pairs connected by bounded queues."*
35. `thread-pool --uses--> producer-consumer` `[E]`; `competing-consumers --specializes-->
    producer-consumer` `[E]`; `competing-consumers --composes-with--> thread-pool` `[E]` - *"a thread
    pool's workers are competing consumers over a shared in-process task queue."*
36. `self-pipe-trick --composes-with--> event-loop` `[S]` (D. J. Bernstein) and `--composes-with-->
    reactor` `[E]` - why `add_signal_handler` exists at all.
37. `defunctionalization --uses--> tagged-union` `[S]` (Reynolds 1972; Danvy & Nielsen 2001) and
    `--alternative-to--> function-object` `[E]` - the pickle-a-job rule and its inverse.
38. `persistent-data-structure --uses--> immutable-value` `[S]` (Okasaki 1998) and
    `hash-array-mapped-trie-hamt --implements--> persistent-data-structure` `[S]` (Bagwell 2001;
    Clojure docs) - the exact lineage of `immutables.Map` under `contextvars`.
39. `lens --composes-with--> persistent-data-structure` `[E]`, `--composes-with--> value-semantics`
    `[E]`, `--alternative-to--> zipper` `[E]` - the nested-immutable-update cluster §6 lacks.
40. `newtype --composes-with--> phantom-type` `[E]` and `units-of-measure-types --uses--> phantom-type`
    `[S]` (Kennedy 2009; boost::units; Haskell `dimensional`) - the mechanism chain from `NewType` up
    to dimensional analysis.
41. `phantom-type --implements--> typestate` `[S]` (*The Embedded Rust Book*, "Typestate Programming":
    zero-sized phantom type parameters encode the peripheral's protocol state) and `marker-interface
    --alternative-to--> phantom-type` `[E]`.
42. `double-checked-locking --composes-with--> safe-publication` `[S]` (JCiP 16.2.4: *"DCL is broken
    without safe publication; making the reference volatile fixes it"*) - cite this when telling
    Python authors to use module-level init or `functools.cache` instead of a hand-rolled DCL.
43. `hierarchical-state-machine --specializes--> finite-state-machine` `[S]` (Harel 1987) and
    `state-transition-table --implements--> finite-state-machine` `[S]` (Douglass) - three named FSM
    options for protocol code instead of one unnamed `if self.state ==` chain.
44. `disruptor --specializes--> ring-buffer` `[S]` and `spsc-lock-free-ring-buffer --specializes-->
    ring-buffer` `[S]` - state the specializations so a Python author knows `deque(maxlen=)` is the
    base case and the other two are the non-transposable refinements.

---

## Do-not-transpose

Elements a later author might reach for by mistake. One line of reason each.

**The language already does this (import the name only as a mapping row, never as guidance).**

- `module-pattern` - Python has real modules and `__all__`; closure-based encapsulation is a JS
  workaround for a language that lacked namespaces.
- `function-object` - every Python callable is already a stateful object; `__call__` needs no pattern.
- `type-erasure` - Python is dynamically typed; there is nothing to erase. Its `--alternative-to-->
  curiously-recurring-template-pattern-crtp` is a C++-internal choice.
- `traits-class`, `sfinae`, `tag-dispatching`, `typelist`, `expression-templates` - C++ compile-time
  metaprogramming. `functools.singledispatch` covers the one useful piece (runtime type dispatch) and
  needs none of this vocabulary.
- `currying-partial-application` - `functools.partial` is in the corpus's own aka list.
- `thunk` - `functools.cached_property` or a zero-arg lambda; the mechanism is ambient. Keep only the
  `thunk --alternative-to--> future-promise` distinction.
- `continuation-passing-style` - asyncio's `loop.call_soon` / `Future.add_done_callback` layer *is*
  CPS; `async`/`await` exists precisely so application code never writes it. Mention, do not teach.
- `reentrant-lock`, `condition-variable`, `semaphore`, `monitor-object`, `scoped-locking`, `latch`,
  `executor`, `thread-pool`, `future-promise`, `ring-buffer`, `event-loop`, `reactor`, `proactor`,
  `coroutine`, `async-await-model`, `green-threads`, `balking`, `guarded-suspension`, `fork-join` -
  all stdlib. Fold into one mapping table under "the runtime does this for you".
- `safe-publication` - Python does not expose a memory model to application code; there is nothing to
  do and nothing to get wrong at this layer. Flag free-threading as OPEN (the corpus has zero coverage
  of it) rather than making a claim.

**This is a C / kernel / hardware concern (drop entirely).**

- `memory-barrier`, `acquire-release-ordering`, `compare-and-swap-loop`, `spinlock`,
  `test-and-test-and-set-lock`, `ticket-lock`, `mcs-queue-lock`, `sequence-lock`, `eventcount`,
  `futex`, `flat-combining`, `restartable-sequences`, `aba-mitigation-via-tagged-pointer`,
  `false-sharing-avoidance-via-cache-line-padding`, `read-copy-update` - all require control over
  instruction ordering and cache lines that Python does not give you. There is no correct Python
  spelling of any of them.
- `critical-region`, `interrupt-masking-critical-section`, `nested-interrupt-handling`,
  `event-flags-group`, `direct-to-task-notification`, `guarded-call`, `rendezvous`,
  `priority-inheritance-protocol`, `priority-ceiling-protocol`, `ordered-locking`,
  `simultaneous-locking`, `protothread`, `cyclic-executive`, `time-triggered-co-operative-scheduler`,
  `multiple-event-receptor`, `single-event-receptor`, `decomposed-and-state`, `deferred-event`,
  `reminder`, `ultimate-hook`, `transition-to-history` - RTOS / embedded-C / statechart-framework
  mechanisms. (`multi-state-task` is the one member of this family that *does* transpose; see the
  import table.)
- `spsc-lock-free-ring-buffer`, `disruptor`, `double-buffer`, `job-system`, `game-loop`, `stencil`,
  `spmd`, `fast-path`, `lock-striping`, `coarse-grained-lock`, `strategized-locking`,
  `thread-safe-interface`, `leader-followers` - each needs memory-ordering control, or a compile-time
  lock-policy parameter, or a frame budget. Not Python problems.
- `safepoint`, `deoptimization`, `threaded-code`, `bytecode-virtual-machine` - language-runtime
  internals. CPython has analogues, but they are not application-level design elements.

**Right idea, wrong manifest (drop from this slice; do not delete from the corpus).**

- `two-phase-locking`, `timestamp-ordering-concurrency-control`, `multiversion-concurrency-control`,
  `snapshot-isolation`, `lock-escalation`, `multi-granularity-locking`, `deadlock-detection`,
  `optimistic-concurrency-control`, `software-transactional-memory`, `fencing-token` -
  database/transaction concurrency control; belongs to a persistence or data-store manifest.
- `optimistic-offline-lock`, `pessimistic-offline-lock`, `implicit-lock` - PoEAA
  business-transaction-scale locking; belongs to an application-architecture manifest.
- `operational-transformation`, `conflict-free-replicated-data-type-crdt` - collaborative-editing
  convergence; a distributed-state manifest.
- `monad`, `free-monad`, `tagless-final`, `effect-handler` - Python has no do-notation, no
  higher-kinded types and no `effect`/`handle`; every attempt produces a library nobody reads. Import
  the **relation** instead (`functional-core-imperative-shell --alternative-to--> monad`, sourced to
  Seemann) so the manifest can say *why* it takes the other branch, and cite `effect-handler
  --alternative-to--> monad` for completeness.

---

## Citable works to add to Sources

As recorded in the corpus. **Verification status is the corpus's own field** - anything marked
UNVERIFIED must not be presented as verified by a later pass.

**Verified.**

- Goetz, Peierls, Bloch, Bowbeer, Holmes & Lea, *Java Concurrency in Practice*, 2006. Addison-Wesley
  Professional, ISBN 978-0-321-34960-6. (`jcip`) - thread confinement, safe publication, executors,
  thread pools, lock striping, latches, DCL/safe-publication interaction.
- Nathaniel J. Smith, *Notes on structured concurrency, or: Go statement considered harmful*, 2018.
  vorpus.org, dated 2018-04-25. (`vorpussc`) - the naming essay for structured concurrency /
  nurseries; the acknowledged source behind Trio, Kotlin coroutine scopes and JEP 453. **The only
  Python-rooted source in this whole concurrency slice.**
- Bass, Clements & Kazman, *Software Architecture in Practice*, 4th ed., 2021. Addison-Wesley/SEI,
  ISBN 978-0-13-688609-9. (`bck`) - `limit-nondeterminism`, `bound-queue-sizes`,
  `introduce-concurrency`, `exception-prevention`, `interlock`, `timeout`, `schedule-resources`.
- Miro Samek, *Practical UML Statecharts in C/C++*, 2nd ed., 2008. Newnes, ISBN 978-0-7506-8706-5.
  (`samekbook`) - run-to-completion semantics, FSM/HSM.
- Buschmann, Henney & Schmidt, *POSA Vol. 4: A Pattern Language for Distributed Computing*, 2007.
  (`posa4`) - `immutable-value`, `context-object`, `copied-value`, `methods-for-states`.
- Buschmann, Meunier, Rohnert, Sommerlad & Stal, *POSA Vol. 1: A System of Patterns*, 1996. (`posa1`)
  - `pipes-and-filters`, `master-slave`.
- Benjamin C. Pierce, *Types and Programming Languages*, 2002. MIT Press, ISBN 0-262-16209-1.
  (`piercetapl`) - tagged unions / sums.
- N. Douglas (WG21), *P1028: SG14 status_code and standard error object*, 2020 (R3). (`p1028`) -
  naming source for `result-type`.
- Scott Wlaschin, *Railway Oriented Programming*, 2014. fsharpforfunandprofit.com / NDC,
  https://fsharpforfunandprofit.com/rop/. (`wlaschinrop`)
- haskell.org wiki contributors, *Smart constructors*, living.
  https://wiki.haskell.org/Smart_constructors. (`hswikismart`)
- Gary Bernhardt, *Functional Core, Imperative Shell*, 2012. Destroy All Software screencast
  (Classic Season 4). (`bernhardtfcis`)
- Foster, Greenwald, Moore, Pierce & Schmitt, *Combinators for Bi-Directional Tree Transformations: A
  Linguistic Approach to the View Update Problem*, ACM TOPLAS 29(3), 2007. (`fosterlenses`) - the
  corpus record omits the DOI (ACM DL blocked); the author-hosted UPenn PDF was the verified copy.
- John C. Reynolds, *Definitional Interpreters for Higher-Order Programming Languages*, 1972.
  (`reynolds72`) - `defunctionalization`.
- Ganz, Friedman & Wand, *Trampolined Style*, ICFP '99, Paris, pp. 18-27. (`ganztrampoline`)
- Chris Okasaki, *Purely Functional Data Structures*, 1998. Cambridge UP,
  doi:10.1017/CBO9780511530104. (`okasaki`) - the corpus's carrying work for
  `persistent-data-structure`.
- Phil Bagwell, *Ideal Hash Trees*, 2001. (`bagwell2001`) - HAMT, the structure under
  `immutables.Map`/`contextvars`.
- Joshua Bloch, *Effective Java*, 3rd ed., 2018. (`effjava`) - `defensive-copy` (Item 50),
  `marker-interface`, `type-safe-enum`.
- Martin Fowler, *Analysis Patterns: Reusable Object Models*, 1996. (`fowleranalysis`) - `quantity`.
- Martin Fowler, *Collection Pipeline*, 2015. martinfowler.com. (`fowlerpipeline`)
- Martin Fowler, *Notification*, eaaDev (living). (`eaadev`)
- Martin Fowler, *The LMAX Architecture*, 2011-07-12. martinfowler.com. (`lmaxfowler`)
- Mark Grand, *Patterns in Java, Volume 1*, 1998. (`grandjava`) - `two-phase-termination`, `balking`,
  `guarded-suspension`, `scheduler`.
- Mattson, Sanders & Massingill, *Patterns for Parallel Programming*, 2004. Addison-Wesley,
  ISBN 978-0-321-22811-6. (`mattsonppp`) - SPMD, loop parallelism, fork/join, master/worker, pipeline
  (ch. 5, Supporting Structures).
- McCool, Robison & Reinders, *Structured Parallel Programming*, 2012. (`mccoolspp`) -
  `parallel-reduction`, `stencil`.
- Michael Kerrisk, *The Linux Programming Interface*, 2010, sec. 63.5.2 "The Self-Pipe Trick".
  (`kerrisktlpi`)
- Edsger W. Dijkstra, *Cooperating Sequential Processes* (EWD123), 1965. E. W. Dijkstra Archive, UT
  Austin. (`ewd123`) - producer-consumer / bounded buffer / semaphores. Corpus note: the transcription
  page itself is undated; 1965 is the archive's standard dating.
- Allen B. Downey, *The Little Book of Semaphores*. (`downeysem`) - **year not recorded** in the corpus.
- C. A. R. Hoare, *Monitors: An Operating System Structuring Concept*, CACM 17(10), 1974.
  DOI 10.1145/355620.361161. (`hoaremonitors`)
- Leslie Lamport, *Time, Clocks, and the Ordering of Events in a Distributed System*, CACM 1978.
  (`lamportclocks`)
- Hewitt, Bishop & Steiger, *A Universal Modular ACTOR Formalism for Artificial Intelligence*,
  IJCAI-73, 1973. (`hewitt1973`)
- Melvin E. Conway, *Design of a Separable Transition-Diagram Compiler*, 1963 (`conway1963`); and
  de Moura & Ierusalimschy, *Revisiting Coroutines*, 2009 (`revisitcoro`).
- Syme, Petricek & Lomov, *The F# Asynchronous Programming Model*, 2011. (`symeasync`) - the naming
  source for `async-await-model`; a non-obvious but correct citation for a Python manifest.
- Microsoft Learn, *Cancellation in Managed Threads*, living. (`mscancellation`)
- Beyer, Jones, Petoff & Murphy (eds.), *Site Reliability Engineering*, 2016. (`googlesre`) - deadline
  propagation ("Addressing Cascading Failures").
- Hohpe & Woolf, *Enterprise Integration Patterns*, 2003. (`hohpe`) - `competing-consumers`,
  `polling-consumer`, `event-driven-consumer`.
- Rust library team, *Rust API Guidelines* (C-SEALED), living. (`rustapiguidelines`)
- Klabnik & Nichols, *The Rust Programming Language*, living. (`rustbook`) - `interior-mutability`
  ("RefCell<T> and the Interior Mutability Pattern").
- Reactive Streams initiative, *Reactive Streams Specification*, living. (`reactivestreams`) -
  demand-signalled backpressure.
- Glenn Fiedler, *Gaffer On Games* (Deterministic Lockstep), living. (`gafferongames`)
- Herlihy, Shavit, Luchangco & Spear, *The Art of Multiprocessor Programming*, 2nd ed., 2020. Morgan
  Kaufmann, ISBN 978-0-12-415950-1. (`herlihyshavit`) - cite only if the manifest explains why the
  lock-free family is out of scope.

**UNVERIFIED in the corpus - do not upgrade without a fresh primary check.**

- Schmidt, Stal, Rohnert & Buschmann, *POSA Vol. 2: Patterns for Concurrent and Networked Objects*.
  (`posa2`) - **verification: unverified; year: UNRESOLVED**; corpus note: "Capture ISBN before ingest
  per report." This single record backs `reactor`, `proactor`, `active-object`,
  `half-sync-half-async`, `leader-followers`, `asynchronous-completion-token`, `monitor-object`,
  `scoped-locking`, `thread-safe-interface`, `strategized-locking`, `thread-specific-storage` and
  `double-checked-locking`. **The largest single provenance risk in this slice** - if the new manifest
  leans on POSA2 vocabulary, verify the ISBN and year first.
- Nygard, *Release It!*. (`nygard`) - **unverified; year UNRESOLVED** (the corpus cites the 2nd ed. as
  2018 elsewhere). Backs `backpressure`, `timeout`, `bulkhead`, `circuit-breaker`.
- Welsh, Culler & Brewer, *SEDA: An Architecture for Well-Conditioned, Scalable Internet Services*,
  SOSP '01. (`sedasosp`) - **unverified**; corpus note: ACM DL 403; DOI 10.1145/502034.502057 and
  pages 230-243 corroborated via dblp only.
- Stonebraker, *The Case for Shared Nothing*, IEEE Database Engineering Bulletin 9(1), 1986.
  (`sharednothing`) - **unverified**; corpus note: no DOI exists; volume and pages 4-9 via dblp only.
- Strom & Yemini, *Typestate: A Programming Language Concept for Enhancing Software Reliability*,
  IEEE TSE SE-12(1), 1986. (`stromyemini86`) - **unverified** (IEEE Xplore not loadable).
- Leijen & Meijer, *Domain Specific Embedded Compilers*, DSL '99. (`leijenmeijer99`) - **unverified**
  (USENIX 403). The naming source for `phantom-type`.
- Rust Embedded WG / Ferrous Systems, *The Embedded Rust Book* (Typestate Programming), living.
  (`embeddedrust`) - **unverified**. Carries the sourced `phantom-type --implements--> typestate` edge.
- Harel, *Statecharts: A Visual Formalism for Complex Systems*, 1987. (`harel87`) - **unverified**
  (DOI unreachable).
- Liskov & Shrira, *Promises: Linguistic Support for Efficient Asynchronous Procedure Calls in
  Distributed Systems*, PLDI '88. (`liskovpromises`) - **unverified** (ACM DL blocked). Naming source
  for `future-promise`.
- M. J. Pont, *Patterns for Time-Triggered Embedded Systems*, 2001. (`pont`) - **unverified**. Naming
  source for `multi-state-task` and `loop-timeout`.
- Richards & Ford, *Fundamentals of Software Architecture*. (`richardsford`) - **unverified; year
  UNRESOLVED**. Naming source for `event-driven-architecture`.
- Drepper, *What Every Programmer Should Know About Memory*, 2007. (`dreppermem`) - **unverified**;
  corpus note: "strongly believed extant, not fetched."
- Dunkels et al., *Protothreads*, SenSys 2006. (`protothreads`) - **unverified**. Dropped anyway.
- Ingerman, *Thunks*, CACM 1961. (`ingerman61`) - **unverified**.

**Two provenance warts to carry forward verbatim.**

1. `azurepatterns` is one corpus record whose **title is stored as "Cloud Design Patterns:
   Cache-Aside"** yet it is used as the citation for *Queue-Based Load Leveling* and *Sequential
   Convoy*. Cite the specific Azure page, not this record's title.
2. Three elements have a `named_in` string with **no matching corpus work record**, so the naming
   source itself is uncited: `option-type` (Haskell 98 Report, 2003 - backed only by `huttonhaskell`
   and `rustbook`), `persistent-data-structure` (Driscoll/Sarnak/Sleator/Tarjan 1989 - backed only by
   `okasaki`) and `cancellation-token`'s Go-blog half (Ajmani 2014 - backed only by `mscancellation`).
   Separately, `event-loop` and `green-threads` are named from **Wikipedia**; cite `reactor`/POSA2 or
   Node's docs and JEP 444 instead.

---

## Where the catalogs REFINE or CONTRADICT the manifest's framing

**1. "No typestate in Python" is too flat - the corpus supplies a mechanism and a partial yes.**
§4 asserts: *"Stateful protocols / typestate (ESTABLISHED). ... The type of an object does not change
as its internal state mutates (no typestate in Python's type system)."* The catalog's definition is
narrower and more useful: typestate *"consum[es] and return[s] distinct types per transition ... so
illegal operations for the current state do not compile"*, and the sourced edge `phantom-type
--implements--> typestate` (Embedded Rust Book) names the encoding. Python **can** do the transition
half - `def connect(self: Closed) -> Open` returning a different class, or a PEP-695 phantom parameter
`Conn[Open]` - and this is checker-enforced. What Python **cannot** do is invalidate the stale handle,
because it has no move semantics and no linear types. The corrected claim: *"Python can encode protocol
state in the type at each transition boundary; it cannot prevent reuse of the pre-transition value."*
That is a materially different instruction to an implementer, and `typestate --realizes--> interlock`
supplies the architecture-level reason to bother.

**2. §4 recommends the weakest of three named unit mechanisms.** §4 says: *"Units of measure ... Best
partial mitigation is `NewType` per unit, but arithmetic between them is not dimensionally checked."*
The corpus holds three distinct related elements and two edges that rank them:
`units-of-measure-types` (Kennedy 2009 / F# 2.0) `--uses--> phantom-type` `[S]`, `--alternative-to-->
newtype` `[E]`, and `--alternative-to--> quantity` `[E]` (*"static type-level vs runtime value-object
realization of unit-safe arithmetic"*). Python cannot take the type-level branch (no dimension
inference through arithmetic), so the **correct** primary recommendation is the `quantity` branch -
`pint`/`astropy.units` - with `NewType` as the zero-dependency fallback, not the best answer. The
manifest currently names only the fallback.

**3. §2 treats `NewType` as complete; the corpus says it is half a pattern.** The sourced edge
`smart-constructor --composes-with--> newtype` (Haskell wiki) states the missing half: *"A smart
constructor wraps a newtype and is exported instead of the raw constructor, so the type's invariant
cannot be bypassed."* §2 correctly notes `NewType` is "a thin callable that returns its argument" -
i.e. `UserId(-1)` type-checks fine. Pairing the two elements makes the rule statable: **a `NewType`
without a smart constructor is a naming convention, not a contract.**

**4. "Parse, don't validate" is a slogan with no corpus name - and two named halves.** Full-text scan
of `elements.json`: **zero** hits for "parse, don't validate". Its two named components are
`smart-constructor` (the construction boundary: *"hiding the raw data constructor makes invalid values
unrepresentable"*) and `functional-core-imperative-shell` (the component structure: *"a pure
decision-making core wrapped by a thin imperative layer that performs all IO and mutation"*). Naming
both turns §5's decision paragraph into two citable, composable elements - and `smart-constructor
--specializes--> static-factory-method` tells an implementer exactly what to write.

**5. §6 identifies the shallow-immutability hole and then leaves it open.** §6: *"The immutability is
shallow - a frozen dataclass holding a `list` still allows mutation of that list's contents."* The
corpus supplies three named mechanisms plus a **sourced** tradeoff between the first two:
`defensive-copy --alternative-to--> immutable-value` (Bloch: *"Both stop external aliases mutating
internal state; immutability removes the need, else copy defensively"*), and
`persistent-data-structure --uses--> immutable-value` (Okasaki) as the third option for large shared
state. §6 should end with a decision rule (`tuple`/`frozenset` field types → copy at the boundary →
persistent structure), not with an observation.

**6. §5 and §6 describe `object.__setattr__` twice without connecting them - the corpus name is
`interior-mutability`.** §5 mandates it (*"on a `frozen=True` dataclass ... you must use
`object.__setattr__`"*); §6 indicts it (*"`object.__setattr__` can bypass the freeze entirely"*).
`interior-mutability` (*"allow controlled mutation through shared (immutable) references by moving
aliasing checks to runtime"*) plus `--alternative-to--> immutable-value` names the *one* mechanism and
frames it as a bounded, deliberate escape hatch - which is exactly the manifest's own house style for
`cast` and `# type: ignore`, applied consistently.

**7. The manifest has one error channel and no vocabulary for choosing.** §5 and §7 assume exceptions
plus a `Raises:` docstring section. The corpus holds a five-element decision space with symmetric
`alternative-to` edges: `result-type` ↔ `option-type` (*"Result carries an error value where Option
only signals presence/absence with no reason"*), `notification` ↔ `result-type` (*"Gather all errors
before returning vs short-circuiting on the first error value"*), `return-status-code` ↔ `result-type`,
and `result-type --realizes--> exception-handling` (*"the typed evolution of the tactic's return-code
end of the handling-mechanism range"*). Two consequences: (a) `raise` vs `Result` is a **position on
one BCK spectrum**, not a religious choice, so the manifest can state a threshold instead of a
preference; (b) pydantic's collect-all-field-errors behaviour **is** `notification`, so the manifest
can finally state the rule it currently cannot express - *boundary validation uses Notification
semantics (accumulate); core logic uses Result or exceptions (short-circuit).*

**8. §4's negative framing hides that the corpus files all of it as one positive tactic.** §4 is a
list of things the type system "CANNOT express". In the corpus, seven design elements (`option-type`,
`newtype`, `tagged-union`, `phantom-type`, `units-of-measure-types`, `smart-constructor`, `trampoline`)
all `realize` the **same** BCK tactic `exception-prevention` - *"keep faults from arising"*. Reframing
§4 as "seven named prevention mechanisms; Python supports five and a half" is both more actionable and
more citable than a list of impossibilities, and it lets §4 link forward to the runtime section
instead of merely deferring to it.

**9. For the NEW concurrency manifest: `run-to-completion` is the name for asyncio's central
guarantee, and no Python doc supplies it.** Samek's element (*"Each event is processed fully - all
transitions, entry/exit actions - before the next event is dequeued, so the machine is never observed
mid-transition"*; problem: *"allowing a new event to interrupt in-progress transition processing
creates unanalyzable interleavings"*) is precisely why a Python author needs no lock between two
statements with no `await` between them, and why adding one `await` re-opens the window. Build §0 of
the new manifest on this element; the sourced edge `run-to-completion-event-processing --enables-->
actor-based-architecture` then licenses the queue-per-resource recommendation instead of asserting it.

**10. The single design law of an asyncio codebase is a `constrains` edge, not a design element.**
`superloop-architecture --constrains--> multi-state-task`: *"The no-OS cooperative loop forbids
blocking waits, forcing long activities into stepwise state-machine form."* Only two `constrains`
edges touch this entire slice. Lead the new manifest with the general form of that sentence: the chosen
architecture removes options from the design layer beneath it - here, blocking calls.

**11. `threading.local()` is the wrong default in asyncio, and the corpus states the choice as an
edge.** `context-object --alternative-to--> thread-specific-storage`: *"Both supply ambient
execution-scoped state: pass it explicitly in a context object vs stash it in thread-local storage."*
Because many asyncio tasks share one thread, thread-local ambient state silently leaks between logical
requests. State the three-way rule once (explicit `context-object` → `contextvars.ContextVar` →
`threading.local()` only for genuinely per-thread resources) rather than rediscovering it per module.

**12. Python's cancellation is exception-delivered, not token-polled - the corpus's element is the
token form.** `cancellation-token` describes a signal that *"long-running operations poll or subscribe
to."* asyncio inverts this: `Task.cancel()` raises `CancelledError` **inside** the coroutine at its
next suspension point. Two consequences the manifest must state and the corpus element does not:
(a) `except Exception:` swallows nothing, but bare `except:`/`except BaseException:` swallows
cancellation, so broad handlers are cancellation bugs; (b) purely synchronous code has no suspension
point and therefore **cannot** be cancelled - which is why `multi-state-task` and
`half-sync-half-async` are load-bearing rather than optional. For threads, the corpus's token form is
the *only* available shape (`threading.Event`), since Python has no thread cancellation at all.

**13. `bound-queue-sizes` makes the asyncio default a defect.** The BCK tactic requires *"an explicit
policy for what happens when queues overflow"*, and `bound-queue-sizes --composes-with-->
queue-based-load-leveling` says *"a load-leveling buffer smooths bursts; bounding its size sets the
overflow policy."* `asyncio.Queue()` defaults to `maxsize=0`, i.e. unbounded, i.e. no policy. The new
manifest can therefore make a hard, sourced rule - **every queue declares `maxsize` and an overflow
policy** - rather than a stylistic suggestion.

**14. Three named mechanisms realise one determinism tactic - that is the new manifest's thesis.**
`structured-concurrency`, `thread-confinement` and `functional-core-imperative-shell` all
`--realizes--> limit-nondeterminism` (*"nondeterministic systems are pernicious to test because
failures do not reproduce"*). Structure the manifest as that tactic plus its three mechanisms plus the
Python instantiation of each, and `deterministic-lockstep` becomes the natural terminal claim
(seed + ordered input log → bit-identical replay). This also gives the two manifests a shared spine:
`immutable-value` and `functional-core-imperative-shell` appear in both, with the typing manifest
establishing the preconditions the concurrency manifest depends on.
