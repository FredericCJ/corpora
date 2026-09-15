# Concurrency & Determinism — Ground-Truth Manifest

**Purpose.** A citable ground-truth reference for adding concurrency to **small-to-mid-scale,
strictly-typed, single-process Python** built as a functional core inside an imperative shell. It
grounds six decisions: **(1)** which of the four CPython execution substrates a piece of work
belongs in; **(2)** how task lifetime, cancellation and timeouts are structured so no work outlives
its scope; **(3)** how every queue and executor is bounded, drained and shut down; **(4)** who owns
each piece of mutable state and how ambient context crosses a thread or task boundary; **(5)** which
seams are injected so concurrent code is deterministic enough to test; and **(6)** how a concurrent
failure is diagnosed once it happens. **Scope.** One process, one machine, tens-to-hundreds of
concurrent in-flight operations — not a distributed platform. Where a mechanism's home is
distributed systems or an RTOS, this file says so and refuses it (§11); that refusal is content, not
a gap. This file is **GROUNDING, not a rulebook**: cite a principle when it materially shapes a
decision; reason past it when the situation does not match. Every factual claim is tagged
**ESTABLISHED** (normative and stable in the cited primary source), **VERSION-DEPENDENT** (bound to
the exact version named), **OPEN** (no authoritative source — a convention this project must pin),
or **CC-FACT** (Claude Code mechanics; none arise here); **FLAGGED-SECONDARY** appears inline
wherever the only available evidence was a secondary source, and **UNVERIFIED** marks a citation a
source asserts that was not confirmed against a primary record this pass (used for corpus provenance
— see Sources). Sibling manifests are cross-referenced and **not duplicated**: release dates and
support phases live in `python_platform_baseline_manifest.md`; general test determinism (clock,
seed, snapshot, fixtures) in `python_testing_tooling_manifest.md`; `except*` mechanics and the
exception contract in `error_tracing_contract_manifest.md`; process attach, profilers and
post-mortem tooling in `python_runtime_diagnostics_manifest.md`; log emission in
`logging_observability_manifest.md`; the paradigm-choice reasoning frame — a different menu from
this file's four substrates, see §2.1 — in `architecture_manifest_default.md`.

**Version anchor.** Behaviour here is stated for CPython as pinned in
`python_platform_baseline_manifest.md` (verified 2026-08-08); per-feature gates are tagged inline as
**VERSION-DEPENDENT (3.n)**. This file asserts no CPython release dates and no support phases of its
own. **Third-party pins are this file's own subject matter**, since the hub owns only CPython facts:
**anyio 4.14.2** and **trio 0.33.0**, both verified 2026-08-08 against the release pages in Sources
(§4.8, §9.2, §9.3). `pytest-asyncio` is cited without a pin because the obligation is routed to
`python_testing_tooling_manifest.md`, which owns test-tool versions.

---

## TL;DR

- **Default to no concurrency in the core.** Keep domain logic synchronous, single-threaded and
  pure; put the loop, the pool, the queue and the clock in the shell behind injected seams. Named:
  `functional-core-imperative-shell` (Bernhardt, 2012), which `realizes` the tactic
  `limit-nondeterminism` (Bass, Clements & Kazman, 2021) — citations under **Named vocabulary**.
  **§3** — ESTABLISHED as vocabulary, OPEN as project policy.
- **Pick the substrate from the table in §2, not from habit.** asyncio for I/O waits with no CPU
  parallelism; threads for blocking I/O and GIL-releasing C code; subinterpreters for isolation with
  in-process messaging; processes for CPU-bound pure Python on a GIL build — VERSION-DEPENDENT (3.14
  for the four-substrate stdlib surface).
- **A bare `asyncio.create_task(...)` whose result is discarded is a defect.** The loop keeps only
  weak references to tasks, so a fire-and-forget task can be garbage-collected mid-execution. Use
  `asyncio.TaskGroup` (VERSION-DEPENDENT 3.11+) or retain a strong reference — ESTABLISHED.
  **§4.2**.
- **Every queue declares `maxsize` and an overflow policy.** `asyncio.Queue()` and `queue.Queue()`
  default to unbounded, and `concurrent.futures` work queues are unbounded by construction with
  `Executor.map()` collecting its inputs eagerly unless `buffersize=` is passed (VERSION-DEPENDENT
  3.14) — ESTABLISHED. An unbounded queue is a memory leak with a pleasant API. **§7.1**.
- **`asyncio.CancelledError` subclasses `BaseException`**, so `except Exception:` correctly misses
  it while bare `except:` / `except BaseException:` catastrophically swallows it, hanging the
  enclosing `TaskGroup` or timeout forever — ESTABLISHED. **§4.5**.
- **Free-threading is officially supported and still optional; it is not the default on any
  version.** Gate builds on `sysconfig.get_config_var("Py_GIL_DISABLED")` and runtime on
  `sys._is_gil_enabled()` — they answer different questions — VERSION-DEPENDENT (3.13+). **§5**.
- **Concurrency determinism is bought at four seams — clock, seed, executor, event loop.** Never
  sleep to synchronise; `ThreadPoolExecutor(max_workers=1)` is not "single-threaded under test".
  Test-order and network nondeterminism are separate obligations, owned by
  `python_testing_tooling_manifest.md` §6c. **§9** — ESTABLISHED.

---

## 1. The execution model is chosen before any primitive

### 1.1 Run-to-completion — the guarantee that makes await-free code implicitly atomic

**ESTABLISHED as vocabulary.** The property that governs every asyncio codebase has a name the
Python documentation never supplies: **`run-to-completion-event-processing`** (Samek, 2008). The
catalog statement: each event is processed fully — all transitions, entry/exit actions — before the
next event is dequeued, so *the machine is never observed mid-transition*; the problem it names is
that "allowing a new event to interrupt in-progress transition processing creates unanalyzable
interleavings".

**The Python consequence, stated once and relied on everywhere below — ESTABLISHED.** On one event
loop, a coroutine step between two `await` expressions is never interleaved with another task on
that loop. Therefore:

- A read-modify-write sequence containing **no** `await` needs **no** lock on a single-loop asyncio
  program.
- Inserting **one** `await` anywhere inside such a sequence re-opens the interleaving window. The
  refactor "extract this into an `async def` helper" can silently introduce a race.
- The guarantee is a property of the *loop*, not of `async` syntax. It does not survive a move to
  threads (§2), a second loop, or `loop.run_in_executor` (§7).

**Sourced relations — ESTABLISHED as vocabulary.** `finite-state-machine --uses-->
run-to-completion-event-processing` (provenance: sourced; Samek, PSiCC2 ch. 2) — "processes each
event fully before dequeuing the next, never observed mid-transition". And
`run-to-completion-event-processing --enables--> actor-based-architecture` (sourced; Samek) — "actor
/ active-object message processing depends on RTC semantics to avoid reentrant state corruption".
That edge is the licence for the queue-per-stateful-resource design in §8.1, rather than an
assertion of taste.

### 1.2 Reactor vs proactor — why identical code behaves differently per platform

**ESTABLISHED.** `asyncio.EventLoop` "is an alias to `SelectorEventLoop` on Unix and
`ProactorEventLoop` on Windows", so loop-specific behaviour — subprocess support, signal handling —
differs by platform with byte-identical application code.

**Vocabulary, with its provenance wart carried forward.** Python names its own classes after the two
POSA2 event-demultiplexing patterns: `reactor` (readiness-based, over `selectors`) and `proactor`
(completion-based, over IOCP), related by the sourced edge `proactor --alternative-to--> reactor` —
"same event-demux role, opposite I/O model". **Their naming source, POSA Vol. 2 (corpus `posa2`), is
recorded in the corpus as UNVERIFIED with the year UNRESOLVED**, and that single record also backs
`half-sync-half-async`, `asynchronous-completion-token`, `thread-specific-storage`,
`monitor-object`, `scoped-locking` and `leader-followers` — the largest single provenance risk in
this file. Do not upgrade the status without a fresh primary check — OPEN (provenance). The corpus
element `event-loop` is separately named from **Wikipedia**; cite `reactor`/POSA2 or Node's
documentation instead — OPEN (provenance).

**Design consequence — OPEN (project policy).** Any behaviour that depends on which loop
implementation is running (signal handlers, subprocess transports, socket options) is a
**platform-conditional** in the shell and must be named as such in the spec. It is not something to
discover from a CI failure.

### 1.3 The chosen architecture removes options from the design layer beneath it

**ESTABLISHED as vocabulary; the relation is editorial.** The corpus records `superloop-architecture
--constrains--> multi-state-task` (provenance: **editorial** — house judgment, not a sourced claim):
"the no-OS cooperative loop forbids blocking waits, forcing long activities into stepwise
state-machine form". Only two `constrains` edges touch the whole concurrency slice; this is the
load-bearing one, and its general form is the single design law of an asyncio codebase: **choosing a
cooperative loop deletes blocking calls from the vocabulary of every module beneath it.** The
transposed remedy is `multi-state-task` (Pont, 2001 — corpus record **UNVERIFIED**): for CPU-bound
work that must run on the loop thread, chunk it and yield between steps (`await asyncio.sleep(0)`).
Everything else that blocks goes to a thread (§3.3, §4.9).

---

## 2. The four-substrate decision table

### 2.1 The table — consult this before writing a single primitive

**These four are CPython *substrates*, not paradigms — OPEN as a mapping (this file's reading of
the two menus, not a claim either source makes).** They are not the same list as the four
state-sharing paradigms in `architecture_manifest_default.md` §3.4 (shared-memory-with-locks,
message-passing, single-threaded event loop, parallel pure transformations). The paradigm is chosen
first and usually admits more than one substrate: message-passing can be built on any of threads,
subinterpreters or processes, while shared-memory-with-locks presupposes threads. Only the event
loop lines up one-to-one. Read §3.4 for *which discipline* the work adopts and this table for
*which CPython machinery* implements it.

**VERSION-DEPENDENT (3.14).** CPython offers exactly four concurrency substrates in the standard
library: cooperative single-threaded scheduling (`asyncio`), OS threads (`threading`,
`concurrent.futures.ThreadPoolExecutor`), multiple interpreters in one process
(`concurrent.interpreters`, `concurrent.futures.InterpreterPoolExecutor`), and separate OS processes
(`multiprocessing`, `concurrent.futures.ProcessPoolExecutor`).

| model | correct when | real CPU parallelism | data-sharing cost at the boundary | characteristic **silent** failure | testability cost |
|---|---|---|---|---|---|
| **asyncio** | I/O-bound work with many concurrent waits; one owner thread; you control the whole call tree | **None.** All tasks run on one thread of one interpreter | Zero — same objects, same heap. Await-free sequences are implicitly atomic (§1.1) | A synchronous blocking call inside a coroutine stalls **every** task on that loop. No exception; just latency | "Almost all asyncio objects are not thread safe" — a harness driving them from a second thread must go through `loop.call_soon_threadsafe()` or `asyncio.run_coroutine_threadsafe()`. No stdlib mock clock and no deterministic scheduler (§9.2) |
| **threads** | Blocking I/O; C-extension code that releases the GIL; libraries with no async API | **Only on a free-threaded build** (§5). None for pure-Python bytecode on a GIL build | Zero — shared memory, and therefore shared hazards | Data races on shared mutable state, and lock-ordering deadlock. **Neither raises an exception** | Nondeterministic interleaving: the same test can pass thousands of times and fail once. The stdlib provides **no scheduler control**; documented mitigations are barriers/events plus repetition (§10.6) |
| **subinterpreters** | Process-like isolation wanted at thread-like startup cost, with in-process communication | **Yes** — interpreters do not share the GIL, so threads plus multiple interpreters give full multi-core parallelism (VERSION-DEPENDENT: isolation since 3.12; stdlib API 3.14) | `pickle` for most objects; a small directly-shared set; `NotShareableError` for the rest (§6.1) | An unmarked C extension re-enables the GIL process-wide with only a **printed warning**; a non-shareable worker exception is replaced by `None` (§6.2) | No shared fixtures, fakes, monkeypatches or in-process doubles cross the boundary — the worker re-executes real code |
| **processes** | CPU-bound **pure-Python** work on a GIL build; hard fault isolation | **Yes** | `pickle` plus a full module re-import per worker under `spawn`/`forkserver` | A worker dying mid-task surfaces as `concurrent.futures.BrokenProcessPool` (VERSION-DEPENDENT 3.3+, derived from `BrokenExecutor`, formerly `RuntimeError`); orphaned children; pickling errors at the boundary | Coverage, monkeypatching, fixtures and in-process fakes do not cross the boundary; module-level side effects execute **again in every worker** |

Every cell is ESTABLISHED except where a version gate is written inline.

**Two readings of the table that decide most cases — derived from the ESTABLISHED cells above; OPEN
as a decision rule.** (a) If the work **waits**, the answer is asyncio or threads and the only real
question is whether the library has an async API. (b) If the work **computes**, the answer is
processes on a GIL build and *possibly* subinterpreters or free-threaded threads — and what you are
choosing between is `pickle`-at-the-boundary versus shared-mutable-state hazards. No option avoids
both.

### 2.2 How the work is *shaped*, once the substrate is fixed

**ESTABLISHED as vocabulary.** The corpus records four peer structures for parallel work, with two
sourced and two editorial relations between them: `fork-join --alternative-to--> master-slave`
(editorial), `spmd --alternative-to--> master-slave` (sourced; Mattson et al., 2004, ch. 5), and
`pipeline-parallelism --alternative-to--> loop-parallelism` (editorial).

| shape | Python spelling | choose when | the failure it invites |
|---|---|---|---|
| `fork-join` | `async with asyncio.TaskGroup()`; `concurrent.futures.wait` | a bounded fan-out whose results are all needed at one join point | unbounded fan-out — N is an input, not a constant |
| `master-slave` | `Executor.map` over a work list | homogeneous independent items, results order-insensitive or index-keyed | eager input collection (§7.2) and swallowed exceptions (§7.3) |
| `pipeline-parallelism` | stages as tasks joined by **bounded** queues | stages have different rates and per-stage state | the slowest stage sets throughput and the queue in front of it grows (§7.1) |
| `loop-parallelism` | chunk the iteration space, one chunk per worker | a hot numeric loop over a partitionable domain | at this scale usually the wrong layer — prefer a vectorised library call |

Names and Python spellings: ESTABLISHED. The "choose when" column: OPEN (a project decision rule).

**Sourced spine for the pipeline shape — ESTABLISHED as vocabulary.** `pipeline-parallelism
--uses--> producer-consumer` (sourced; Mattson et al.) — "adjacent stages are producer/consumer
pairs connected by bounded queues"; `pipeline-parallelism --realizes--> pipes-and-filters` (sourced;
Garlan & Shaw, as recorded in the corpus) and `collection-pipeline --realizes--> pipes-and-filters`
(sourced; Fowler, 2015), with `coroutine --enables--> pipes-and-filters` (editorial). One vocabulary
therefore covers generator expressions, task pipelines and system topology: `pipes-and-filters`
(POSA Vol. 1, 1996).

### 2.3 Epistemic note — what the design corpus does *not* know about Python concurrency

**OPEN.** The SWE corpus contains **no Python-specific concurrency work record at all**; the single
Python-rooted source in its whole concurrency slice is Nathaniel J. Smith, *Notes on structured
concurrency, or: Go statement considered harmful*, vorpus.org, 2018-04-25 (corpus `vorpussc`,
verified). There is no corpus element for `asyncio`, `contextvars`, the GIL, free-threading, or
function colouring. **Every runtime claim in this file is therefore sourced to python.org or to a
library's own documentation, and every *name* is sourced to the corpus. Do not let the two channels
swap roles.** Two ids a later author will reach for do not exist under the expected name: the
element is `event-driven-architecture` (not `event-driven`) and `shared-nothing-architecture` (not
`shared-nothing`).

---

## 3. The default for a small strictly-typed app: single-threaded core, concurrency at the edge

### 3.1 The argument, not the assertion

**ESTABLISHED as vocabulary; the recommendation drawn from it is OPEN (project policy).** Three
named mechanisms in the corpus `realize` **one** tactic, `limit-nondeterminism` (Bass, Clements &
Kazman, 2021), whose own framing is this file's thesis: *nondeterministic systems are pernicious to
test because failures do not reproduce*. All three edges are recorded as **editorial** (house
judgment, presented as such, not as a sourced fact):

1. `functional-core-imperative-shell --realizes--> limit-nondeterminism` — "a pure core is
   deterministic and testable without mocks; nondeterminism is confined to the shell." Corpus aka:
   **"impureim sandwich"**.
2. `structured-concurrency --realizes--> limit-nondeterminism` — "confining task lifetimes to
   lexical scopes eliminates unconstrained parallelism (orphaned tasks, leaked threads)."
3. `thread-confinement --realizes--> limit-nondeterminism` (Goetz et al., 2006): "if data is only
   ever touched by one thread, thread safety follows by construction."

So the recommendation is not "concurrency is frightening". It is that one tactic is served three
times over, and the cheapest of the three at this scale needs **no** concurrency primitives in the
core at all. A pure `def decide(state, event) -> list[Command]` that imports no clock, no HTTP
client and no session is deterministic by construction, needs no scheduler control to test, and is
untouched by every hazard in §5 and §7.

**Why Python takes this branch rather than the type-level one.** The sourced edge
`functional-core-imperative-shell --alternative-to--> monad` (Seemann, 2020) states the choice
exactly: "both separate pure logic from effects — an impure/pure/impure boundary vs type-level (IO)
monadic sequencing". Python has no do-notation and no higher-kinded types, so the boundary form is
the only branch that survives contact with a real codebase — §11.3. The precedent for taking it to
the extreme is `thread-confinement --enables--> lmax-architecture` (editorial; Fowler, 2011) — "the
single-threaded business-logic processor is thread confinement applied at system scale". One
process, one writer, everything else I/O, is a citable design, not a compromise.

### 3.2 The rule

**OPEN — a project policy that must be written into the spec, not inferred.**

> A module that both **computes** and **schedules** is untestable by construction. Concurrency
> primitives — event loop, task group, executor, queue, lock, clock, sleep, `random` — appear only
> in the shell, and the shell receives every one of them through an injected seam (§9.2).

Mechanical enforcement, stated honestly — this is the rung of the collection's enforcement ladder
where concurrency policy either bites or evaporates. Every route below is OPEN (a project decision)
except where the cell says otherwise:

| the rule | what mechanically enforces it |
|---|---|
| the core imports no `asyncio`, `threading`, `concurrent.futures`, `multiprocessing`, `time`, `random` | **Fitness function** — an import-direction check owned and configured in `python_module_boundaries_manifest.md`, wired into CI by `python_quality_gates_manifest.md` |
| the core contains no `async def` | **Contract-only in this file.** A lint route plausibly exists, but no rule code was verified in this pass, so none is asserted; see `python_linting_practices_manifest.md` for the rule inventory — OPEN |
| the shell takes its clock, executor and loop as parameters | **Type-catchable** — declare them as `Protocol`s, and a module that reaches for the global instead fails the checker (`python_typing_contract_manifest.md` owns Protocol mechanics) |
| the core is deterministic | **Test-catchable** — property-based tests with a fixed seed and no injected fakes pass only if the core is pure (`python_testing_tooling_manifest.md`) |
| no queue is unbounded | **Contract-only / review** — no verified rule code catches `asyncio.Queue()` with a defaulted `maxsize`; §7.1 states the rule and admits nothing mechanically enforces it — OPEN |

### 3.3 The escalation ladder — stay on the lowest rung that works

1. **Synchronous, single-threaded, no concurrency.** Correct for almost every CLI, batch job,
   generator pipeline and library. Measure before leaving this rung.
2. **One `asyncio` loop in the shell, `TaskGroup` for fan-out, blocking calls pushed to a thread**
   via `asyncio.to_thread(...)` / `loop.run_in_executor(...)`. The default for anything doing
   concurrent I/O. The pattern has a name — `half-sync-half-async` (POSA2, **UNVERIFIED**): "combine
   the performance of asynchronous event handling with the programming simplicity of synchronous
   code, without either style polluting the other", with `to_thread`/`run_in_executor` as the
   queueing layer between the two halves.
3. **A thread pool with no async at all**, when the whole program is blocking I/O and introducing a
   loop would colour the entire call tree for no gain.
4. **Processes**, when profiling proves the work is CPU-bound pure Python. The honest architecture
   is `shared-nothing-architecture` (Stonebraker, 1986 — corpus record **UNVERIFIED**):
   process-per-core with **no** shared mutable state, coordinating only by messages. This is why
   `multiprocessing.Manager` shared state is an anti-pattern and not a convenience.
5. **Subinterpreters or a free-threaded build**, only with a measured baseline and a named owner for
   the hazards in §5 and §6 — VERSION-DEPENDENT (3.14 for both stdlib surfaces).

**Scale discipline — OPEN (judgment, stated as this collection's scale policy).** Rungs above 4 are
where a small application starts paying distributed-systems costs inside one process. If the answer
to "how many cores does this need" is "one, and it is waiting on a socket", every rung above 2 is
over-engineering.

---

## 4. Structured concurrency: task lifetime, cancellation, timeouts

**ESTABLISHED as vocabulary.** `structured-concurrency` (Smith, 2018); the catalog aka list already
contains **"nursery (Trio)"**. The rule this licenses, in the catalog's own words: fire-and-forget
spawning "breaks local reasoning, error propagation, and cancellation". Three composition edges make
the section's shape: `structured-concurrency --composes-with--> cancellation-token` (sourced; Trio
nurseries / Smith 2018) — "a task scope cancels its whole child tree via a scope-bound cancellation
token"; `--composes-with--> two-phase-termination` (editorial) — "exiting a task scope requires all
children to reach a clean terminated state first"; and `--composes-with--> future-promise`
(editorial).

### 4.1 `TaskGroup` semantics — VERSION-DEPENDENT (3.11+)

| behaviour | exact semantics |
|---|---|
| first failure | "The first time any of the tasks belonging to the group fails with an exception other than `asyncio.CancelledError`, the remaining tasks in the group are cancelled." |
| after that | "No further tasks can then be added to the group." |
| the body | If the `async with` body is still active, "the task directly containing the `async with` statement is also cancelled. The resulting `asyncio.CancelledError` will interrupt an `await`, but it will not bubble out of the containing `async with` statement." |
| aggregation | Surviving non-`CancelledError` exceptions "are combined in an `ExceptionGroup` or `BaseExceptionGroup` (as appropriate)... which is then raised" (§4.6) |
| the base-exception exception | "If any task fails with `KeyboardInterrupt` or `SystemExit`, the task group still cancels the remaining tasks and waits for them, but then the initial `KeyboardInterrupt` or `SystemExit` is re-raised instead of `ExceptionGroup` or `BaseExceptionGroup`." |
| non-exceptional early exit | `TaskGroup.cancel()` — VERSION-DEPENDENT (**3.15**): "a non-exceptional, early exit of the task group's lifetime". Cancels every not-yet-done task **and the group's own body**; "the task group context manager will exit *without* `asyncio.CancelledError` being raised"; idempotent; may be called after the group has exited; if called before entry "the group will be cancelled upon entry" |
| `GeneratorExit` | A special case was added — documented as "Changed in version 3.15: Addition of the special case for `GeneratorExit`" — VERSION-DEPENDENT (3.15) |

All rows VERSION-DEPENDENT (3.11) unless a later gate is written in the cell.

**The pre-3.15 shape you will find in existing code.** Before `TaskGroup.cancel()`, early
non-exceptional exit required "unintuitive boilerplate such as an extra task raising a custom
exception which is then suppressed as it exits the task group" — VERSION-DEPENDENT (3.15, as the
documented description of what it replaces). When the floor is below 3.15, that boilerplate is the
correct answer, not a smell; when the floor reaches 3.15, deleting it is a mechanical refactor.

**`gather` is not a task group.** `asyncio.gather(..., return_exceptions=False)` propagates the
first exception to the awaiting task but "other awaitables in the `aws` sequence won't be cancelled
and will continue to run" — the opposite of `TaskGroup` — ESTABLISHED. Treat `gather` as legacy for
anything with a failure path; it leaks running work on error.

### 4.2 The orphan ban — why a reference must be held

**ESTABLISHED.** "Save a reference to tasks passed to this function, to avoid a task disappearing
mid-execution. The event loop only keeps weak references to tasks." A fire-and-forget
`asyncio.create_task(...)` whose return value is discarded can therefore be garbage-collected before
it completes — and its failure is not merely late, it is *gone*.

The documented fallback when a task genuinely cannot live in a scope: gather them in a `set` and
`task.add_done_callback(background_tasks.discard)`. The documentation attaches the warning that must
be carried with it: "this approach never awaits the tasks, so if a task fails, its exception is
never retrieved and asyncio logs a 'Task exception was never retrieved' message when the task is
garbage collected" — ESTABLISHED (§10.3).

**Rule.** A `create_task` call whose result is neither stored nor awaited is rejected at review.
Prefer `TaskGroup`; the strong-reference set is the exception that must be justified in the spec —
OPEN (project policy).

### 4.3 Timeouts and deadline propagation

**VERSION-DEPENDENT (3.11+).** `asyncio.timeout(delay)` and `asyncio.timeout_at(when)`. Two facts
that reverse most people's expectations:

- Inside the block, the mechanism is `asyncio.CancelledError`. "The `asyncio.timeout()` context
  manager is what transforms the `asyncio.CancelledError` into a `TimeoutError`, which means the
  `TimeoutError` can only be caught *outside* of the context manager." A `try/except TimeoutError`
  placed **inside** the `async with` never fires — ESTABLISHED.
- `asyncio.timeout(None)` creates a deadline-less scope whose deadline can be installed later with
  `cm.reschedule(new_deadline)`, using `get_running_loop().time()` as the clock — VERSION-DEPENDENT
  (3.11). This is the seam for "the deadline is known only after the handshake".

**The design rule, with its name — ESTABLISHED as vocabulary.** `deadline-propagation` — Beyer,
Jones, Petoff & Murphy (eds.), *Site Reliability Engineering*, 2016 (corpus `googlesre`, verified),
from "Addressing Cascading Failures"; the sourced edge is `deadline-propagation --realizes-->
timeout-tactic`. The catalog problem statement is the rule: "independent per-hop timeouts let deep
call chains do work the original caller has already abandoned." Pass an **absolute** deadline down
the call chain and enforce it with `asyncio.timeout_at(deadline)` at each stage — never a fresh
relative timeout per hop. The paired sourced edge is `cancellation-token --composes-with-->
deadline-propagation` (Go's `context.Context` carries both `Done()` and `Deadline()`), which is
exactly what an explicit context object (§8.1) should carry in Python.

### 4.4 The cancellation contract

**ESTABLISHED as vocabulary, with a Python-specific inversion.** The corpus element is
`cancellation-token` (Microsoft Learn, *Cancellation in Managed Threads*, living) — a signal that
long-running operations "poll or subscribe to, exiting cooperatively". Its `named_in` field also
credits Ajmani's 2014 Go blog post, **for which the corpus holds no work record**, so that half of
the attribution is uncited — OPEN (provenance). It `realizes` two tactics at once — `--realizes-->
cancel` and `--realizes--> timeout-tactic` (both editorial) — which is why `asyncio.timeout()` is
built on cancellation rather than beside it.

**Python inverts the token — ESTABLISHED.** asyncio cancellation is **exception-delivered, not
polled**:

| API | exact behaviour |
|---|---|
| `Task.cancel(msg=None)` | "arranges for a `CancelledError` exception to be thrown into the wrapped coroutine on the next cycle of the event loop" and "does not guarantee that the Task will be cancelled". Returns `False` if the task is already done or cancelled — ESTABLISHED |
| suppressing it | "Should the coroutine nevertheless decide to suppress the cancellation, it needs to call `Task.uncancel()` in addition to catching the exception" — VERSION-DEPENDENT (3.11 for `uncancel`/`cancelling`; 3.13 "changed to rescind pending cancellation requests upon reaching zero") |
| `Task.uncancel()` | Decrements the cancel-request count and returns the remainder. It is what "allows for elements of structured concurrency like Task groups and `asyncio.timeout()` to continue running, isolating cancellation to the respective structured block" — and the documentation also says it "isn't expected to be used by end-user code" — VERSION-DEPENDENT (3.11) |
| `Task.cancelling()` | Returns cancel requests minus `uncancel()` calls. "If this number is greater than zero but the Task is still executing, `cancelled()` will still return `False`" — **`cancelling() > 0` does not mean cancelled** — VERSION-DEPENDENT (3.11) |
| `Task.exception()` | Does **not** return cancellation as a value: it "raises a `CancelledError` exception" for a cancelled task and "raises an `InvalidStateError` exception" if the task is not done — ESTABLISHED |
| `asyncio.shield(aw)` | Protects the **inner** awaitable, not the caller: "if the coroutine containing it is cancelled, the Task running in `something()` is not cancelled... Although its caller is still cancelled, so the `await` expression still raises a `CancelledError`." If the inner task cancels itself, "that would also cancel `shield()`" — ESTABLISHED |

**Consequence the corpus element does not state.** Purely synchronous code has no suspension point
and therefore **cannot be cancelled** — which is why `multi-state-task` (§1.3) and
`half-sync-half-async` (§3.3) are load-bearing rather than decorative. For **threads**, the token
form is the *only* available shape: Python has no thread cancellation at all, so pass a
`threading.Event` and poll it — exactly the catalog's "poll or subscribe to, exiting cooperatively"
— ESTABLISHED.

**Cleanup rule.** The documentation prescribes `try/finally` for cleanup, and says that when
`CancelledError` is explicitly caught "it should generally be propagated when clean-up is complete"
— ESTABLISHED. anyio states it without hedging: "Always reraise the cancellation exception if you
catch it. Failing to do so may cause undefined behavior in your application" — ESTABLISHED (anyio).
Cleanup that must itself `await` has to sit in a shielded scope — "the shielded block will be exempt
from cancellation except when the shielded block itself is being cancelled" — because awaiting
inside a cancelled scope otherwise means "the operation will be cancelled immediately" — ESTABLISHED
(anyio).

### 4.5 `CancelledError` is a `BaseException`, and what that breaks

**ESTABLISHED.** `asyncio.CancelledError` "directly subclasses `BaseException`" (VERSION-DEPENDENT:
it became a `BaseException` subclass in **3.8**), so:

- `except Exception:` around a coroutine body **does not** catch cancellation. That is correct and
  deliberate; do not "fix" it.
- Bare `except:` and `except BaseException:` **do** catch it. Combined with `pass` or with a
  swallowing log-and-continue, this silently defeats cancellation and hangs the enclosing
  `TaskGroup` or `asyncio.timeout` **forever**. This is the single most damaging handler shape in
  async Python.
- `trio.Cancelled` is designed the same way: it "inherits from BaseException, like KeyboardInterrupt
  and SystemExit do, so that it won't be caught by catch-all `except Exception:` blocks", and you
  "should do some cleanup and then re-raise it or otherwise let it continue propagating" —
  ESTABLISHED (trio).

The general exception-hierarchy rules — `except Exception` catching `ExceptionGroup` but not
`BaseExceptionGroup`, the bare-except prohibition, chaining — are owned by
`error_tracing_contract_manifest.md` §11, §12, §18.

### 4.6 Failures arrive as an `ExceptionGroup`

**VERSION-DEPENDENT (3.11).** A `TaskGroup` raises its children's failures aggregated: a plain
`except ValueError:` around `async with asyncio.TaskGroup()` does **not** catch a `ValueError`
raised in a child; `except* ValueError:` does. The `CancelledError` produced by sibling cancellation
is **not** a member of the group — ESTABLISHED.

**All `except*` mechanics are owned by `error_tracing_contract_manifest.md` §18** — the
split/subgroup model, the always-a-group `as` target, the `TypeError` for naming a
`BaseExceptionGroup` subclass, the SyntaxErrors (mixing `except` with `except*`, bare `except*:`,
`return`/`break`/`continue` inside a clause), and the automatic propagation of leftovers. Do not
restate them here; the only concurrency-side obligation is: **a component that fans out with
`TaskGroup` documents its failure surface as a group, and its callers are written with `except*`.**

For assertions on group shape in tests, `python_testing_tooling_manifest.md` owns the tooling
choice; the two verified primitives are `pytest.RaisesGroup`/`pytest.RaisesExc` — VERSION-DEPENDENT
(pytest 8.4+) — and `trio.testing.RaisesGroup`, which "by default requires all specified exceptions
present with no others, order-independent, with `allow_unwrapped=True` and `flatten_subgroups=True`
modifiers" — ESTABLISHED (trio).

### 4.7 The eager task factory is a semantic change, never a free speedup

**VERSION-DEPENDENT (3.12).** `asyncio.eager_task_factory` and
`asyncio.create_eager_task_factory(custom_task_constructor)`, installed with
`loop.set_task_factory(asyncio.eager_task_factory)`. With it, "coroutines begin execution
synchronously during `Task` construction. Tasks are only scheduled on the event loop if they block."
And: "if the coroutine returns or raises, the task is never scheduled to the event loop."

Consequences that break real code: any ordering assumption that `create_task()` returns before the
coroutine body runs; any exception-timing assumption; any test that counts loop iterations.
**Rule:** installing an eager task factory is a declared, spec-level decision for the whole
application, not a per-module optimisation — OPEN (project policy).

### 4.8 Edge vs level cancellation — the asyncio/trio gap that porting hides

**ESTABLISHED.** anyio states the contrast in its own documentation: anyio cancel scopes and task
groups "use *level cancellation*... it will get hit with a cancellation exception any time it hits a
*yield point*", whereas on plain asyncio "a `CancelledError` is raised in the task and the task then
gets to handle it however it likes, even opting to ignore it entirely" (edge cancellation). trio's
cancellation is level-triggered: once a scope is cancelled, "all cancellable operations in that
block will keep raising `Cancelled`", and `CancelScope` exposes `deadline`, `shield`,
`cancel_called` and `cancelled_caught` with `move_on_after`/`fail_after` (relative) and
`move_on_at`/`fail_at` (absolute).

**trio's checkpoint rule is the property asyncio lacks** — ESTABLISHED: "if you call an async
function provided by Trio (`await <something in trio>`), and it doesn't raise an exception, then it
*always* acts as a checkpoint", where a checkpoint is "a point where Trio checks for cancellation"
and where the scheduler may switch tasks. Synchronous functions contain no checkpoints, so a
pure-CPU loop is uncancellable. On asyncio there is no equivalent guarantee, and **a third-party
async function may contain no suspension point at all**.

**Decision, and the honest cost.** anyio 4.14.2 "implements Trio-like structured concurrency on top
of asyncio" and lets applications "run unmodified on either asyncio or Trio"; trio 0.33.0 "is based
on a new way of thinking that we call 'structured concurrency'" — VERSION-DEPENDENT (anyio 4.14.2,
trio 0.33.0). These pins are this file's own subject and were verified 2026-08-08 against the
release
pages in Sources; the hub owns only CPython version facts. Taking the dependency buys level
cancellation, a mature deterministic-clock story (§9.2) and `wait_all_tasks_blocked` (§9.3).
Declining it keeps a zero-dependency stdlib surface and costs you those three things. **What is not
a valid position: writing code that assumes level cancellation while running on raw asyncio.** Code
ported from trio/anyio to plain asyncio silently loses the guarantee that a cancelled scope keeps
raising at every yield point — OPEN (the dependency choice is the project's; the prohibition is
not).

If the floor is below 3.11, note that anyio 4.14.0 also added `TaskGroup.cancel()` — the same
affordance CPython adds in 3.15 — VERSION-DEPENDENT (anyio 4.14.0).

### 4.9 The blocking call, and the CPU loop that cannot be cancelled

**ESTABLISHED.** A synchronous blocking call inside a coroutine stalls every task on the loop, and
asyncio debug mode surfaces it by logging callbacks that exceed `loop.slow_callback_duration`
(default 0.1 s) — see §10.1. Two remedies, and they are not interchangeable:

- **The call blocks on I/O or on a GIL-releasing C extension** → move it to a thread
  (`asyncio.to_thread` / `loop.run_in_executor`). Note the constraint: since 3.11 the `executor`
  argument of `loop.run_in_executor` "must be an instance of `ThreadPoolExecutor`"; a
  `ProcessPoolExecutor` is **not** accepted, and `InterpreterPoolExecutor` is accepted only because
  it subclasses `ThreadPoolExecutor` (§6.2) — VERSION-DEPENDENT (3.11).
- **The call is pure-Python CPU work that must stay on the loop thread** → `multi-state-task`: chunk
  it and `await asyncio.sleep(0)` between steps (§1.3). This also restores cancellability, because
  each yield is a delivery point for `CancelledError`.

---

## 5. Free-threading as behaviour

**Status routes to the hub.** `python_platform_baseline_manifest.md` owns the phase timeline,
release dates and per-version support statements. Two attributions matter here because getting them
backwards is the most likely factual error on this topic — VERSION-DEPENDENT, per-PEP:

- **PEP 703** "Making the Global Interpreter Lock Optional in CPython" — Final, Python-Version
  **3.13**. This is the **implementation** PEP.
- **PEP 779** "Criteria for supported status for free-threaded Python" — Final, Python-Version
  **3.14**. This is the PEP that made the free-threaded build **officially supported while still
  optional**. Attributing supported status to PEP 703 is wrong.
- Making free-threading the **default** build (Phase III) is explicitly out of scope of PEP 779:
  "the decision to make free-threaded Python the default (phase III) is very different... That's
  left for a future PEP." No such PEP exists — OPEN (unscheduled, by the source's own statement).

### 5.1 Detection — build and runtime are different questions

**VERSION-DEPENDENT (3.13+).** Three documented mechanisms, and they do not answer the same
question:

| mechanism | answers | use it for |
|---|---|---|
| `sysconfig.get_config_var("Py_GIL_DISABLED")` → `1` | Was this interpreter **built** with free-threading support? Documented as "recommended" for build-configuration decisions | wheel selection, packaging, compile-time branches |
| `sys._is_gil_enabled()` | Is the GIL **actually disabled in this running process**? | runtime assertions, benchmark guards, parallelism preconditions |
| `python -VV` / `sys.version` contain `"free-threading build"` | build identity as a string | logging the environment; not a programmatic gate |

**The trap that follows.** A free-threaded build running under `-X gil=1` has `Py_GIL_DISABLED == 1`
**and** `sys._is_gil_enabled() == True` simultaneously. Using the `sysconfig` value as a runtime
check is therefore wrong in a way that reads as correct — VERSION-DEPENDENT (3.13+). The leading
underscore on `sys._is_gil_enabled()` makes agents shy away from it in favour of something
incorrect; use it anyway, and note that it is a private API — its stability is not guaranteed by the
compatibility policy — OPEN.

**The switches** — VERSION-DEPENDENT (3.13): `-X gil=0,1` "forces the GIL to be disabled or enabled,
respectively. Setting to `0` is only available in builds configured with `--disable-gil`".
`PYTHON_GIL=1` forces it on; `PYTHON_GIL=0` "needs Python configured with the `--disable-gil` build
option". **`-X gil` takes precedence over the environment variable** — so a container's `PYTHON_GIL`
can be silently overridden by an entrypoint flag.

### 5.2 The atomicity assumptions people wrongly draw from the GIL

**VERSION-DEPENDENT (3.13+) — and the important half is that most of these were never true.**

| assumption | verdict |
|---|---|
| "`dict`/`list`/`set` operations are atomic, so I need no lock" | `dict`, `list` and `set` use internal locks on free-threaded builds, **but** the documentation says "Python has not historically guaranteed specific behavior for concurrent modifications to these built-in types, so this should be treated as a description of the current implementation, not a guarantee of current or future behavior". Use `threading.Lock` |
| "`counter += 1` is atomic under the GIL" | **Never true.** It is a read-modify-write across bytecodes on every build. A lost update is possible with the GIL enabled |
| "`d[k] = d[k] + 1` is safe because dicts are thread-safe" | **Never true**, for the same reason: the read and the write are separate operations |
| "one iterator can be consumed from several threads" | Documented as unsafe: "threads may see duplicate or missing elements" |
| "`frame.f_locals` is readable from a monitoring thread" | Accessing `frame.f_locals` for a frame executing in **another** thread may **crash the interpreter** |
| "a free-threaded interpreter means my program runs in parallel" | Importing one C extension that does not declare free-threading support re-enables the GIL at runtime with nothing but a **printed warning**. The program stays correct and gets no faster |

**The 3.15 remedies for the shared-iterator hazard** — VERSION-DEPENDENT (3.15), and they do **not**
exist on 3.14, so do not offer these names to a project on an earlier floor:
`threading.serialize_iterator(iterable)` (serializes `__next__`, plus `send`/`throw`/`close` if
present, under a lock; no value duplicated or skipped); `threading.synchronized_iterator(func)` (a
decorator for generator functions, wrapping each produced iterator); and
`threading.concurrent_tee(iterable, n=2)` (n independent iterators, buffered until every branch has
consumed a value; `n == 0` returns an empty tuple, negative `n` raises `ValueError`).

**Also fixed in 3.15** — VERSION-DEPENDENT (3.15): "the import system now acquires per-module locks
in hierarchical order (parent packages before their submodules)", which previously let one thread
importing `pkg.sub` and another importing `pkg.sub.mod` block each other. On an earlier floor,
concurrent first-import of a package tree is a real deadlock source; import eagerly at startup from
one thread.

**Where the design corpus is silent.** The corpus element `safe-publication` (JCiP) concerns a
memory model Python does not expose to application code, and the corpus has **zero coverage of
free-threading**. Nothing in the design vocabulary tells you whether a publication idiom is safe on
`python3.14t`; the runtime documentation in §5.1–§5.4 is the only authority — OPEN.

### 5.3 C extensions: the declaration, the borrowed-reference trap, and critical sections

**VERSION-DEPENDENT (3.13+).** "Extension modules need to explicitly indicate that they support
running with the GIL disabled; otherwise importing the extension will raise a warning and enable the
GIL at runtime." Multi-phase-init modules add the `Py_mod_gil` slot with value `Py_MOD_GIL_NOT_USED`
(guarded `#if PY_VERSION_HEX >= 0x030D0000`); single-phase-init modules call
`PyUnstable_Module_SetGIL(m, Py_MOD_GIL_NOT_USED)` under `#ifdef Py_GIL_DISABLED`.

Borrowed-reference C APIs are unsafe under free threading if the container mutates concurrently; the
documented strong-reference replacements are `PyList_GetItemRef()`, `PyDict_GetItemRef()`,
`PyDict_GetItemStringRef()`, `PyWeakref_GetRef()` and `PyImport_AddModuleRef()` — VERSION-DEPENDENT
(3.13+).

**Critical sections are not mutual exclusion.** `Py_BEGIN_CRITICAL_SECTION` /
`Py_END_CRITICAL_SECTION` (one object) and `Py_BEGIN_CRITICAL_SECTION2` / `Py_END_CRITICAL_SECTION2`
(two objects), built on `PyMutex`, "must be used in matching pairs and must appear in the same C
scope" and "are no-ops in non-free-threaded builds". Critically: "critical sections may temporarily
release their locks, allowing other threads to modify the protected data." An extension can
therefore pass every test on a GIL build and race only on a free-threaded one — VERSION-DEPENDENT
(3.13+).

**Stable-ABI status carries a live documentation conflict.** PEP 803 (`abi3t`) is Final for
**3.15**: extensions opt in with `Py_TARGET_ABI3T=<version>` (auto-defined when `Py_LIMITED_API=v`
and `Py_GIL_DISABLED` are both set), `PyObject` becomes opaque, wheels carry the compressed tag set
`abi3.abi3t` and filename-tagged extensions use `.abi3t.so`; it requires the PEP 697 APIs (negative
`basicsize`, `PyObject_GetTypeData()`), the PEP 793 `PyModExport_*` hook and the PEP 820 `PySlot`
structure — VERSION-DEPENDENT (3.15). **But** the 3.15 free-threading-extensions HOWTO still says
"the free-threaded build does not currently support the Limited C API or the stable ABI" and still
recommends `py_limited_api=not sysconfig.get_config_var("Py_GIL_DISABLED")`. **OPEN — treat the
HOWTO paragraph as stale text pending update; either target `abi3t` deliberately or ship a separate
version-specific free-threaded wheel.** "We ship `abi3`, so we support free-threading" is false.

**New C code should not add `PyGILState_*` calls.** PEP 788 (Final, **3.15**) adds
`PyInterpreterGuard` (prevents finalization while held), `PyInterpreterView` (a thread-safe
interpreter reference without an attached thread state), `PyThreadState_Ensure()`,
`PyThreadState_EnsureFromView()` and `PyThreadState_Release()`, and **soft-deprecates** the
`PyGILState` family: "soft deprecations only mean that these APIs will not be developed further;
there is no plan to remove `PyGILState` from Python's C API" — VERSION-DEPENDENT (3.15). Existing
calls are not a bug; new ones are a choice to explain.

### 5.4 The honest performance statement — do not merge the numbers

**VERSION-DEPENDENT, and each figure belongs to its source. Four different numbers describe this one
property; quote the source alongside the figure or omit the figure.**

| source | figure |
|---|---|
| Free-threading HOWTO (identical wording in the 3.14 and 3.15 docs) | "On the pyperformance benchmark suite, the average overhead ranges from about 1% on macOS aarch64 to 8% on x86-64 Linux systems." |
| What's New in 3.14 | the "performance penalty on single-threaded code" is "roughly 5-10% (depending on platform and C compiler)" |
| PEP 703 (2023) | 6% (Intel Skylake) / 5% (AMD Zen 3) single-threaded; 8% / 7% multi-threaded |
| PEP 779 | proposed "15% as a hard performance target" for Phase II |

3.14 enabled the specializing adaptive interpreter (PEP 659) in free-threaded mode, which is the
main reason the overhead figures dropped — VERSION-DEPENDENT (3.14).

**What none of these figures tell you** is whether *your* workload gets faster. That depends on
whether it is CPU-bound in pure Python, whether every loaded extension declares free-threading
support (§5.3), and how much of the work is serialised behind a lock you added to make it correct.
Measure with `sys._is_gil_enabled()` asserted in the harness, or do not claim a speedup — OPEN.

### 5.5 Identical code, different behaviour, per build

**VERSION-DEPENDENT (3.14).** Two runtime knobs default differently by build: `-X
thread_inherit_context=0,1` / `PYTHON_THREAD_INHERIT_CONTEXT` (a new `threading.Thread` copies the
context of the caller of `Thread.start()`) and `-X context_aware_warnings=0,1` /
`PYTHON_CONTEXT_AWARE_WARNINGS` (`warnings.catch_warnings` stores filter state in a `ContextVar`).
Both "default to `1` on free-threaded builds and to `0` otherwise".

Consequences — VERSION-DEPENDENT (3.14): identical code observes **different `contextvars`
propagation into threads** on `python3.14` versus a free-threaded build (§8.3), and warning-filter
scoping changes, which is a real source of flaky warning assertions. **Set both flags explicitly if
behaviour must match across builds.**

---

## 6. Subinterpreters: the boundary contract

**VERSION-DEPENDENT (3.14).** PEP 734 is Final with Python-Version 3.14. The stdlib module is
`concurrent.interpreters` — **renamed** from the PEP's original `interpreters`, and built on the
private `_interpreters`. Its public surface per `__all__`: `get_current()`, `get_main()`,
`create()`, `list_all()`, `is_shareable()`, `Interpreter`, `create_queue`, `Queue`, and the
exceptions `InterpreterError`, `InterpreterNotFoundError`, `ExecutionFailed`, `NotShareableError`,
`QueueEmpty`, `QueueFull`.

**A live naming discrepancy — OPEN.** The library documentation names the queue exceptions
`QueueEmptyError` and `QueueFullError`, while `__all__` in the shipped source exports `QueueEmpty`
and `QueueFull`. Prefer the documented `QueueEmptyError`/`QueueFullError` in written specs and
**verify against the interpreter you actually target** before writing an `except` clause.

`Interpreter` methods — VERSION-DEPENDENT (3.14): `is_running()`, `close()`, `prepare_main(ns=None,
**kwargs)`, `exec(code, /, dedent=True)`, `call(callable, /, *args, **kwargs)`,
`call_in_thread(callable, /, *args, **kwargs)`. `exec()` and `call()` raise `ExecutionFailed`
(carrying `excinfo`) when the code inside raises.

### 6.1 What crosses the boundary

**VERSION-DEPENDENT (3.14).** Three tiers, and the third is the one that bites:

1. **Directly shared or copied efficiently:** `None`, `bool`, `bytes`, `str`, `int`, `float`, and
   `tuple` of similarly supported objects.
2. **Actually shares mutable data:** `memoryview` and the cross-interpreter `Queue`.
3. **Everything else:** "by default, most objects are copied with `pickle` when they are passed to
   another interpreter." Anything that cannot be sent raises `NotShareableError`.

**Queue signature, source over docs.** The documentation renders the constructor as
`concurrent.interpreters.create_queue()` with no parameters, but the shipped source in both the 3.14
and 3.15 branches is `def create(maxsize=0, *, unbounditems=UNBOUND)`, exported as `create_queue`;
PEP 734 also specifies `create_queue(maxsize=0)`. **Cross-interpreter queues are therefore boundable
today despite the docs** — VERSION-DEPENDENT (3.14, 3.15), which matters for §7.1. `Queue.put(obj,
block=True, timeout=None, *, unbounditems=None)` and `Queue.get(block=True, timeout=None)`; the
`Queue` implements the `queue.Queue` interface. **There is no `syncobj` parameter** — do not promise
one.

**Isolation is not a security boundary — ESTABLISHED.** The documentation states that interpreters
"in the same process can technically never be strictly isolated from one another since there are few
restrictions on memory access within the same process." A subinterpreter is not a sandbox for
untrusted code, and no amount of care in application code makes it one.

**The name for the design this forces — ESTABLISHED as vocabulary.** `defunctionalization` — John C.
Reynolds, *Definitional Interpreters for Higher-Order Programming Languages*, 1972 (corpus
`reynolds72`, verified), with `defunctionalization --uses--> tagged-union` (sourced; Reynolds 1972;
Danvy & Nielsen 2001) and `--alternative-to--> function-object` (editorial). Because a lambda,
closure or local class cannot cross the boundary, cross-interpreter and cross-process work must be
represented as **data**: a frozen dataclass tagged union of job kinds plus one top-level `def
apply(job)` dispatcher. The catalog problem statement is the rule — "turning behavior into data" so
higher-order programs can be "serialized, stored, or sent". Union/`Literal`-tag mechanics belong to
`python_typing_contract_manifest.md`.

### 6.2 The executor

**VERSION-DEPENDENT (3.14).** `concurrent.futures.InterpreterPoolExecutor(max_workers=None,
thread_name_prefix='', initializer=None, initargs=())` is declared as `class
InterpreterPoolExecutor(_thread.ThreadPoolExecutor)` — one OS thread per worker, each thread owning
its own interpreter. Because it **is** a `ThreadPoolExecutor` subclass, it is accepted by
`loop.run_in_executor()` (§4.9).

Two behaviours to design around:

- **It pickles at every hop.** It "serializes the `initializer` and `initargs` using `pickle`", the
  worker "serializes the callable and arguments using `pickle`", and "the worker likewise serializes
  the return value when sending it back." A closure, a lambda, a local class or an open socket
  cannot be submitted.
- **It can lose an exception.** The implementation puts the exception on the results queue and, on
  `interpreters.NotShareableError`, substitutes `None` after reporting that the "exception is not
  shareable". A non-picklable exception type raised in a worker therefore **does not arrive
  intact**: a failing job can look like a job that returned nothing — VERSION-DEPENDENT (3.14,
  3.15). Design the job protocol so every failure is a picklable value, not an exotic exception
  type.

`chunksize` on `Executor.map()` "has no effect" with `ThreadPoolExecutor` and
`InterpreterPoolExecutor`; it chunks only for `ProcessPoolExecutor` — ESTABLISHED.

### 6.3 When this is the right tool rather than a novelty

**VERSION-DEPENDENT (3.14) — the documentation states its own limitations**, and they are the
decision criteria: "interpreter startup not yet optimized"; "each interpreter uses more memory than
necessary"; "limited options for sharing objects between interpreters"; "many third-party extension
modules not yet compatible"; "unfamiliar programming model for most users".

**OPEN (a decision rule this project must adopt or reject).** Choose subinterpreters when **all** of
the following hold: the work is CPU-bound pure Python; the job and result are already `pickle`-clean
(or defunctionalised, §6.1); process startup cost or process count is a measured problem; and no
third-party extension in the worker path is incompatible. If any one fails, `ProcessPoolExecutor` is
the lower-risk answer and threads-on-a-GIL-build is the wrong answer regardless. Isolation with
in-process messaging is a genuine niche — it is not a general replacement for either of its
neighbours in §2.1.

---

## 7. Executors, queues, backpressure and shutdown

### 7.1 Every queue declares a `maxsize` and an overflow policy

**ESTABLISHED as a tactic; the default is the defect.** `bound-queue-sizes` (Bass, Clements &
Kazman, 2021) requires "an explicit policy for what happens when queues overflow". `asyncio.Queue`
treats `maxsize <= 0` as infinite, and `queue.Queue(maxsize=0)` is likewise unbounded — ESTABLISHED.
**An unbounded queue in a specified system is therefore a defect, not a default**: it has no
overflow policy, so it does not level load, it defers failure to an out-of-memory kill.

Named vocabulary: `producer-consumer` (Dijkstra, EWD123, 1965), whose catalog aka is **"bounded
buffer"** — *bounded* is the entire point; and `backpressure` (Nygard, *Release It!* — corpus record
**UNVERIFIED, year UNRESOLVED**; also the *Reactive Streams Specification*, verified), whose catalog
problem is "unbounded queues hide overload until memory or latency blows up". The editorial edges
that connect them: `producer-consumer --realizes--> queue-based-load-leveling`, `bound-queue-sizes
--composes-with--> queue-based-load-leveling` ("a load-levelling buffer smooths bursts; bounding its
size sets the overflow policy that protects resources"), and `backpressure --realizes-->
manage-event-arrival`, whose out-of-band siblings are `token-bucket` and `throttle`.

**In Python, `await queue.put(x)` on a bounded queue *is* backpressure; `queue.put_nowait(x)`
discards it** — ESTABLISHED. The decision table below names ESTABLISHED APIs; choosing a row per
queue is OPEN (project policy):

| overflow policy | Python spelling | correct when |
|---|---|---|
| **block the producer** (backpressure) | `await q.put(item)` / `q.put(item)` on a bounded queue | the producer can be slowed — the default choice for in-process pipelines |
| **fail fast** | `q.put_nowait(item)` and handle `asyncio.QueueFull` / `queue.Full` | the producer must not be blocked and a rejection is a valid outcome (e.g. an admission gate) |
| **drop oldest** | `collections.deque(maxlen=n)` | a metrics/telemetry buffer where recency beats completeness |
| **shed with an explicit signal** | check `q.qsize()` against a threshold and return a typed rejection | the caller must be told; the rejection belongs in the error contract (`error_tracing_contract_manifest.md`) |

`collections.deque(maxlen=n)` is the stdlib bounded overwriting FIFO — the corpus name is
`ring-buffer`, whose specialisations `disruptor --specializes--> ring-buffer` and
`spsc-lock-free-ring-buffer --specializes--> ring-buffer` (both sourced) are **not** transposable
(§11.2) — ESTABLISHED.

**Graceful drain — VERSION-DEPENDENT (3.13).** `Queue.shutdown(immediate=False)` with
`asyncio.QueueShutDown` (asyncio) and `queue.ShutDown` (threads) is the drain primitive. With
`immediate=True` the queue is drained, the unfinished-task count is reduced by the number drained,
and blocked `get()` callers raise the shutdown exception. Below 3.13 the substitute is a sentinel
per consumer, which must be counted correctly — a classic off-by-N hang.

`queue.SimpleQueue` is unbounded, and its C implementation is reentrant — "`put()` or `get()` calls
can be interrupted by another `put()` call in the same thread without deadlocking" — which makes it
the safe choice inside destructors and weakref callbacks, and the wrong choice everywhere else —
ESTABLISHED.

**Worker fleets.** N worker tasks pulling one bounded queue is `competing-consumers` (Hohpe & Woolf,
2003), with `competing-consumers --specializes--> producer-consumer` and `--composes-with-->
thread-pool` (both editorial): "a thread pool's workers are competing consumers over a shared
in-process task queue". When per-key ordering must survive, hash the key to one of N single-consumer
queues; the corpus name is `sequential-convoy`, which exists precisely because "per-key ordering
must survive in a competing-consumers world that otherwise destroys sequence". **Resource
partitioning:** `bulkhead` (Nygard — **UNVERIFIED**) is a separate `asyncio.Semaphore` (or a
separate executor) per downstream dependency, so one slow dependency cannot consume all concurrency;
the sourced edge `bulkhead --realizes--> bulkhead-deployment-isolation` ties the in-process and
deployment forms together.

### 7.2 Executors are unbounded, and `map()` is eager

**ESTABLISHED / VERSION-DEPENDENT (3.14).** The `concurrent.futures` work queue is effectively
unbounded, and "the `iterables` are collected immediately rather than lazily, unless a `buffersize`
is specified to limit the number of submitted tasks whose results have not yet been yielded. If the
buffer is full, iteration over the `iterables` pauses until a result is yielded from the buffer."
`buffersize` was added in **3.14** and is the **only in-stdlib backpressure knob for executors**.
Feeding a generator of a million items to `map()` on an earlier floor materialises a million
submissions.

Everything else needs an explicit `queue.Queue(maxsize=N)` or `asyncio.Queue(maxsize=N)` in
**front** of the pool, with a bounded number of `submit()` calls in flight — OPEN (project policy;
the stdlib supplies no such bound).

**Default `max_workers` is version-dependent and platform-capped** — VERSION-DEPENDENT (3.8, 3.13):
`ThreadPoolExecutor` was `cpu_count * 5` in 3.5, `min(32, os.cpu_count() + 4)` from 3.8, and
`min(32, (os.process_cpu_count() or 1) + 4)` from 3.13; `ProcessPoolExecutor` defaults to
`os.process_cpu_count()` from 3.13, and on Windows `max_workers` "must be less than or equal to 61"
with the `None` default capped at 61. **Set it explicitly.** A defaulted pool size is a capacity
decision made by the interpreter version.

Vocabulary fold — ESTABLISHED as vocabulary: `executor`, `thread-pool`, `future-promise` and
`fork-join` are a near-literal transliteration of the JCiP Executor framework into
`concurrent.futures`; keep the sourced edge `executor --composes-with--> thread-pool` (JCiP ch. 6),
which is why *submission* policy and *execution* policy are separate knobs — and why a bounded queue
in front of an unbounded pool is the missing submission policy.

### 7.3 Exception propagation through futures

**ESTABLISHED.** Two different rules, and the second loses exceptions silently:

- `Executor.submit()` captures the callable's exception in the `Future`; it is re-raised on
  `Future.result()`.
- `Executor.map()`: "if a `fn` call raises an exception, then that exception will be raised when its
  value is retrieved from the iterator." **A `map()` whose result iterator is never consumed
  swallows every worker exception.** `list(executor.map(...))` propagates; a bare
  `executor.map(...)` discards every failure.

`concurrent.futures.wait(fs, timeout=None, return_when=ALL_COMPLETED)` returns a named 2-tuple of
sets `(done, not_done)` where `done` **includes cancelled futures**; `FIRST_EXCEPTION` "will return
when any future finishes by raising an exception. If no future raises an exception then it is
equivalent to `ALL_COMPLETED`." `as_completed(fs, timeout=None)` measures its timeout "from the
original call to `as_completed()`", not per item — ESTABLISHED. Both are easy to misread as
per-future timeouts.

Broken-pool signals — VERSION-DEPENDENT (3.3, 3.7, 3.15): `BrokenThreadPool` (3.7) is raised when a
`ThreadPoolExecutor` worker "has failed initializing"; `BrokenProcessPool` (3.3) when a
`ProcessPoolExecutor` worker "has terminated in a non-clean fashion", and from 3.15 "the resulting
traceback will now tell you the PID and exit code of the terminated process."

### 7.4 Shutdown: the two-phase shape

**ESTABLISHED as vocabulary.** `two-phase-termination` — Mark Grand, *Patterns in Java, Volume 1*,
1998 (corpus `grandjava`, verified), whose catalog problem statement *is* the rule: "forcibly
killing threads corrupts shared state and leaks resources." The composition edges:
`two-phase-termination --uses--> cancellation-token` (editorial) — "the phase-1 termination request
is exactly a cancellation flag the target polls at safe points" — and `structured-concurrency
--composes-with--> two-phase-termination` (editorial).

The shape, in order, for an asyncio shell — OPEN (project policy), built from the ESTABLISHED
primitives named in each step:

1. **Signal.** `loop.add_signal_handler(...)` sets an `asyncio.Event`. Why a bridge is needed has a
   name — `self-pipe-trick` (Kerrisk, 2010, sec. 63.5.2): "signals interrupt at arbitrary points and
   cannot safely do real work, and `select`/`poll` cannot wait on them directly". Python's spellings
   are `signal.set_wakeup_fd` and `loop.add_signal_handler`, with `socket.socketpair()` as the
   Windows fallback; sourced edge `self-pipe-trick --composes-with--> event-loop` (D. J. Bernstein).
2. **Stop admitting work.** Producers observe the event and stop; the admission gate starts
   rejecting.
3. **Drain.** `await queue.join()`, or `Queue.shutdown()` (VERSION-DEPENDENT 3.13) for the explicit
   drain, with a bounded overall deadline (§4.3).
4. **Cancel the remainder.** Cancel worker tasks; each re-raises `CancelledError` after cleanup
   (§4.4).
5. **Only then** exit the task group / `Executor.shutdown`.

**`shutdown(cancel_futures=True)` is not a stop button** — VERSION-DEPENDENT (3.9):
`Executor.shutdown(wait=True, cancel_futures=False)`; `cancel_futures` "will cancel all pending
futures that the executor has not started running. Any futures that are completed or running won't
be cancelled, regardless of the value of `cancel_futures`." With both `True`, running futures
complete first and only the remainder are cancelled. **There is no stdlib mechanism to interrupt a
running thread**, so any worker that can run long must poll a `threading.Event` at its own safe
points (§4.4). Design the worker body around that from the start; retrofitting it is a rewrite.

### 7.5 The deadlock the documentation warns about

**ESTABLISHED.** "Deadlocks can occur when the callable associated with a `Future` waits on the
results of another `Future`." Nesting `submit()` inside a task already running on the same pool
hangs with **no exception and no timeout** once workers are exhausted. **Rule: a task running on a
pool never submits to that pool.** If a job needs sub-jobs, either restructure it as a pipeline
stage with its own queue (§2.2) or use a second, separately sized pool — and record the
lock-free/wait-free family as out of scope (§11.2).

Lock ordering is the other silent hang. `architecture_manifest_default.md` §3.4 states the house
rule — if locks are necessary, the lock order is part of the design — and this file adds only that
Python offers neither `ordered-locking` nor `deadlock-detection` as a mechanism (§11.2), so a
documented lock order plus §10.4's watchdog is the whole toolkit. That absence is asserted from the
seed pack's adjudication rather than from a primary source that enumerates it — OPEN.

### 7.6 Process pools: the start method changed, and pickling is the contract

**VERSION-DEPENDENT (3.14).** "On POSIX platforms the default start method was changed from `fork`
to `forkserver`", for `multiprocessing` and `concurrent.futures.ProcessPoolExecutor`; `spawn`
remains the default on Windows and macOS; "code that requires `fork` must explicitly specify that
via `get_context()` or `set_start_method()`". In 3.14 "`forkserver` now authenticates its control
socket to avoid relying solely on filesystem permissions."

Consequences to design for: code with mutable module-level state that silently worked under `fork`
now sees a **fresh import per worker**, so module-level side effects run again in every worker — and
that is the same fact that makes coverage, monkeypatching and in-process fakes not cross the
boundary (§2.1). Separately, `fork` from a multi-threaded process has raised `DeprecationWarning`
since **3.12**: "if Python is able to detect that your process has multiple threads, the `os.fork()`
function that this start method calls internally will raise a `DeprecationWarning`" —
VERSION-DEPENDENT (3.12). Mixing threads and `fork` is on a deprecation path, not merely
discouraged.

`set_start_method(method, force=False)` raises `RuntimeError` if the start method has already been
set and `force` is not `True`; `get_context(method=None)` with the global method unset "will set it
to the system default" — ESTABLISHED. Tests that switch start methods must therefore control
ordering or use per-context objects; a test that calls `set_start_method` at import time will break
another test that does the same.

---

## 8. Ownership: confinement, `contextvars`, and the explicit context object

### 8.1 The three-way rule for ambient state, stated once

**ESTABLISHED as vocabulary; the ranking is this file's policy.** The corpus states the choice as an
editorial edge: `context-object --alternative-to--> thread-specific-storage` — "both supply ambient
execution-scoped state: pass it explicitly in a context object vs stash it in thread-local storage".
Names: `context-object` (POSA Vol. 4, 2007); `thread-specific-storage` (POSA2, **UNVERIFIED**);
`thread-confinement` (JCiP, 2006), with `thread-confinement --uses--> thread-specific-storage`
(sourced; JCiP 3.3.3) and `--alternative-to--> monitor-object` (sourced; JCiP ch. 3) — "confining
data to one thread removes shared mutable state, avoiding the locking a monitor provides". **Confine
or lock; doing both badly is the common failure.**

| rank | mechanism | use when | why not higher |
|---|---|---|---|
| 1 | **explicit parameter / `context-object`** — a frozen `RequestContext` dataclass threaded through calls | almost always. It is visible in signatures, type-checked, and trivially testable | verbose in deep call chains — which is usually a signal the chain is too deep |
| 2 | **`contextvars.ContextVar`** | genuinely cross-cutting ambient values (correlation id, tenant, deadline) that every layer would otherwise thread through untouched | invisible in signatures; propagation rules are subtle (§8.2, §8.3); a `ContextVar` read in the core makes the core impure |
| 3 | **`threading.local()`** | only for genuinely per-**thread** resources (a thread-confined DB connection, a thread-owned buffer) | **wrong by construction in asyncio**: many tasks share one thread, so thread-local ambient state silently leaks between logical requests |

**Confinement as the primary tool.** One owning task or thread per mutable structure, with
`loop.call_soon_threadsafe` as the only cross-thread door — ESTABLISHED for the asyncio
thread-safety constraint (§2.1). The architectural form is `actor-based-architecture` (Hewitt,
Bishop & Steiger, 1973): one bounded queue plus one owning task per stateful resource; callers send
messages and never touch state. "Message-owned state removes locks and makes distribution and
supervision natural." That recommendation is licensed by `run-to-completion-event-processing
--enables--> actor-based-architecture` (§1.1), not by preference. For multiplexed protocol clients
(JSON-RPC, AMQP, custom framing), the corpus name for the `dict[request_id, asyncio.Future]`
correlation table is `asynchronous-completion-token` (POSA2, **UNVERIFIED**) — "re-associate each
completion with the context needed to process it, without searching". Pair it with a bounded
in-flight limit and a deadline per entry, or it is a memory leak with a correlation id.

### 8.2 What a Task copies, and what it does not

**VERSION-DEPENDENT.** The two documented seams for supplying context explicitly:
`asyncio.Runner.run(coro, *, context=None)` accepts a custom `contextvars.Context` —
VERSION-DEPENDENT (3.11) — and `-X thread_inherit_context` controls whether a new `threading.Thread`
copies the context of the caller of `Thread.start()` — VERSION-DEPENDENT (3.14), **default `1` on
free-threaded builds and `0` otherwise** (§5.5).

Read that pair carefully — VERSION-DEPENDENT (3.14): **thread context inheritance is build-dependent
and therefore not something to rely on implicitly.** If a worker thread needs the caller's
correlation id, either set `-X thread_inherit_context=1` explicitly for every deployment, or —
preferably — pass a `context-object` argument (§8.1 rank 1), which is invariant across builds,
versions and substrates.

### 8.3 Where propagation silently breaks

**ESTABLISHED / VERSION-DEPENDENT, per row.**

| boundary | what happens to ambient context |
|---|---|
| `asyncio.create_task` / `TaskGroup.create_task` | a `contextvars.Context` copy is taken — writes inside the task do **not** propagate back out to the parent. Code that "sets a ContextVar in a task so the caller sees it" is broken — ESTABLISHED |
| `loop.run_in_executor` / `asyncio.to_thread` | a thread boundary. Do not assume the loop's context is visible; pass what the worker needs as arguments — ESTABLISHED for the thread-safety constraint (§2.1) |
| `threading.Thread(...)` | build-dependent (§8.2) — VERSION-DEPENDENT (3.14) |
| a subinterpreter or a process | nothing propagates. Everything crosses as pickled data or not at all (§6.1, §7.6) — VERSION-DEPENDENT (3.14) |
| `warnings.catch_warnings()` across threads | filter state is a `ContextVar` when `-X context_aware_warnings=1`, which is the **default on free-threaded builds only** — VERSION-DEPENDENT (3.14) |

Correlation-id propagation for logs is owned by `logging_observability_manifest.md` §8; this table
states only where the mechanism itself stops working.

### 8.4 The other route to safe sharing: do not share mutable state

**ESTABLISHED as vocabulary.** Four editorial edges point at one tactic: `immutable-value
--enables--> introduce-concurrency`, and the same for `value-semantics`, `copied-value` and
`safe-publication`. `immutable-value` (POSA Vol. 4, 2007) states the problem in the sentence this
section exists to carry: "shared mutable values require defensive copies or synchronization;
immutability makes sharing safe by construction."

The Python mechanisms: `@dataclass(frozen=True, slots=True)` with `tuple` / `frozenset` / `Mapping`
field types; `defensive-copy` (Bloch, 2018, Item 50) at trust boundaries, with the sourced tradeoff
`defensive-copy --alternative-to--> immutable-value` ("both stop external aliases mutating internal
state; immutability removes the need, else copy defensively"); and for large shared state,
`persistent-data-structure` (carrying work Okasaki, 1998), with `hash-array-mapped-trie-hamt
--implements--> persistent-data-structure` (sourced; Bagwell 2001) — the HAMT that CPython's own
`contextvars` is implemented on. **Caveat: frozen is shallow.** A frozen dataclass holding a `list`
still permits mutation of that list's contents; the field-type discipline is what closes it, and
`python_typing_contract_manifest.md` owns the frozen-dataclass and immutability mechanics.

---

## 9. Determinism as a design obligation

### 9.1 The tactic, named

**ESTABLISHED as vocabulary.** `limit-nondeterminism` (Bass, Clements & Kazman, 2021). Its own
framing: *nondeterministic systems are pernicious to test because failures do not reproduce.* §3.1
named the three mechanisms that realize it; this section gives the seams.

**Scope boundary, stated so it is not crossed.** This file owns determinism **of concurrent code** —
scheduler, event loop, ordering, races. `python_testing_tooling_manifest.md` owns determinism of
tests in general — fixture isolation, snapshot stability, the clock and seed policy for the suite as
a whole. Where a seam is shared (the clock, the seed), this file states the *concurrency* obligation
and defers the *suite* policy.

### 9.2 The four injected seams — and nothing else buys determinism

| seam | inject | Python facts that constrain the choice |
|---|---|---|
| **clock** | a `Clock` protocol; never call `time.time()` / `datetime.now()` / `loop.time()` in the core | Fowler's rule, verbatim: "Always wrap the system clock, so it can be easily substituted for testing." — ESTABLISHED. trio ships the only mature deterministic clock in this ecosystem: `trio.testing.MockClock(rate=0.0, autojump_threshold=inf)`; with the default `rate=0.0` "the clock only advances through manual calls to `jump()` or when the `autojump_threshold` is triggered", and with a threshold set it "watches the execution of the run loop, and any time things have settled down and everyone's waiting for a timeout, it jumps the clock forward to that timeout". `jump(seconds)` raises `ValueError` for negative values — ESTABLISHED |
| **seed** | own a `random.Random(seed)` instance; never module-level `random` | `PYTHONHASHSEED` accepts a decimal integer in [0, 4294967295]; "specifying the value 0 will disable hash randomization"; unset or `random` means a random seed; its stated purpose is "to allow repeatable hashing, such as for selftests for the interpreter itself". `-R` "only has an effect if the `PYTHONHASHSEED` environment variable is set to anything other than `random`" — ESTABLISHED. Hypothesis' own seeding surface (`derandomize`, the CI profile, `@seed()`) is owned by `python_testing_tooling_manifest.md` §4a and §6c; the concurrency-side point is only that a fixed seed does not survive a race (§9.6) |
| **executor** | pass the `Executor` in; supply a synchronous fake in tests | The documentation blesses exactly this: `Future.set_result()`, `Future.set_exception()` and `Future.set_running_or_notify_cancel()` "should only be used by `Executor` implementations and unit tests". Since 3.8 `set_result`/`set_exception` raise `concurrent.futures.InvalidStateError` if the future is already done — VERSION-DEPENDENT (3.8) |
| **event loop** | `loop_factory` | There is **no stdlib asyncio mock clock and no stdlib deterministic asyncio scheduler**. The documented substitution seam is `loop_factory` on `asyncio.run()` (VERSION-DEPENDENT 3.12) or `asyncio.Runner` (VERSION-DEPENDENT 3.11) — supply a loop subclass overriding `time()`. **The policy system is deprecated and "will be removed in Python 3.16"** — `get_event_loop_policy()`, `set_event_loop_policy()`, `DefaultEventLoopPolicy`, `AbstractEventLoopPolicy`; harnesses that install a custom policy must migrate — VERSION-DEPENDENT (removal in 3.16) |

Two more loop facts that bite harnesses — VERSION-DEPENDENT: every `asyncio.run()` call creates and
closes a **new** event loop (`asyncio.run(coro, *, debug=None, loop_factory=None)`; `debug` became
`None`-by-default in 3.10 "to respect the global debug mode settings", `loop_factory` was added in
3.12, and in 3.14 `coro` "can be any awaitable object"). `asyncio.Runner(*, debug=None,
loop_factory=None)` — 3.11 — is the documented seam for running several coroutines on **one** loop
and initialises lazily. And `asyncio.get_event_loop()` "raises a `RuntimeError` if there is no
current event loop" from **3.14**; the old implicit loop-creation behaviour is gone.

**The async-test-runner surface is owned by `python_testing_tooling_manifest.md` §6d** — plugin
choice, `asyncio_mode`, and the loop-scope settings whose defaults are documented as changing. The
only concurrency-side obligation here: **the loop lifetime a test runs under is part of the seam, so
it is pinned explicitly and never inherited from a plugin default** — OPEN (project policy).

### 9.3 Never sleep to synchronise

**ESTABLISHED.** Fowler's rule, verbatim (spelling as in the source): "Never use bare sleeps to wait
for asynchonous responses: use a callback or polling." Where polling is unavoidable, his guidance is
a small `pollingInterval` with a high `waitLimit`.

The instruments, in order of preference:

1. **A signal the code already has** — `asyncio.Event`, `threading.Event`, a completion callback, a
   queue item, `await queue.join()`.
2. **A settled-scheduler probe** — `trio.testing.wait_all_tasks_blocked(cushion=0.0)` "blocks until
   there are no runnable tasks": the sleep-free replacement for `await asyncio.sleep(0.1)` as a
   synchronisation device — ESTABLISHED. **There is no stdlib asyncio equivalent** — OPEN: on raw
   asyncio, use an `Event`, and if you find yourself wanting `wait_all_tasks_blocked`, that is an
   argument for the anyio/trio dependency (§4.8).
3. **Explicit ordering** — `trio.testing.Sequencer` forces "code in different tasks to run in an
   explicit linear order" — ESTABLISHED; on threads, `threading.Barrier` and `threading.Event` play
   the same role.

`await asyncio.sleep(0.05)` in a test is not a synchronisation primitive. It is a bet on the
machine, and it loses in CI — ESTABLISHED, by the rule quoted above.

### 9.4 Make concurrent code run single-threaded under test

**ESTABLISHED.** Inject the `Executor` (§9.2) and supply a synchronous fake whose `submit()` runs
the callable inline and returns a `Future` completed via `set_result()`/`set_exception()` — the
exact use the documentation sanctions for "`Executor` implementations and unit tests".

**`ThreadPoolExecutor(max_workers=1)` is not equivalent.** Work still runs on another thread, just
serialised — so it preserves the timing nondeterminism, the exception marshalling and the debugger
opacity you were trying to remove — ESTABLISHED. It is a throughput knob, not a determinism tool.

For asyncio, the equivalent moves are — OPEN (project policy): one `asyncio.Runner` per test with an
injected `loop_factory` (§9.2); no real network or filesystem in the loop; and every timeout under
test driven by an injected clock rather than by wall time.

### 9.5 Deterministic replay, where the domain permits it

**ESTABLISHED as vocabulary.** `deterministic-lockstep` (Fiedler, gafferongames.com, living; Bettner
& Terrano, GDC 2001, recorded on the same element). The strongest form of the determinism claim:
replay a run from a **seed plus an ordered input log** and get a bit-identical result.

**This is reachable only if the core is `functional-core-imperative-shell`** — ESTABLISHED as
vocabulary, OPEN as a design claim: a core that reads a clock, a `ContextVar` or `random` cannot be
replayed, no matter how good the log is. The ordering primitive when wall time is not trustworthy is
`logical-clock` (Lamport, 1978): a monotonically increasing per-process sequence number attached to
every emitted event. At this scale use the **counter**; the element's aka list ("vector clock",
"version vector", "hybrid logical clock") belongs to distributed systems, and adopting those forms
in a single-process app is over-engineering (§11.3).

**What replay buys and costs — OPEN (project policy).** A failing concurrent run becomes a fixture.
**What it costs:** every input must be captured in order, and every nondeterministic source must
already be injected. Adopt it for a core with real sequencing logic (a protocol engine, a scheduler,
a state machine); do not build the harness for a CRUD shell.

### 9.6 What determinism you cannot buy — and the name for containing the rest

**ESTABLISHED, and this is the honest limit of the section.**

| you can make deterministic | you cannot make deterministic |
|---|---|
| a pure core, given injected clock and seed | OS thread scheduling. The stdlib exposes **no scheduler control** |
| asyncio task ordering, given an injected loop and no real I/O | whether a data race manifests on this run |
| timeout behaviour, given an injected clock | the interleaving that a free-threaded build chooses |
| the *set* of Hypothesis examples, given `derandomize` or `@seed` | the wall-clock duration of anything that touches a network |

Hypothesis states its own limit, and it applies to every seam above: a fixed seed reproduces cases
only "assuming that there are no other sources of nondeterminisim, such as timing, hash
randomization, or external state" (spelling as in the source) — ESTABLISHED. So pin `PYTHONHASHSEED`
**as well** as the seed, and expect neither to save a test that races.

**The named containment tactic for the residue is Quarantine** (Fowler, *Eradicating Non-Determinism
in Tests*): "place any non-deterministic test in a quarantined area. (But fix quarantined tests
quickly.)" His six categories are Quarantine, Lack of Isolation, Asynchronous Behavior, Remote
Services, Time, and Resource Leaks — ESTABLISHED. Quarantine is a **time-boxed holding pen with a
named owner**, not a permanent flaky marker; the suite-level policy belongs to
`python_testing_tooling_manifest.md`.

**One academic family is deliberately not claimed.** Schedule-bounding techniques (preemption
bounding, delay bounding) surfaced only in search results during verification; the underlying papers
were not loaded, so **no claim about their content or findings is made here** — OPEN.

---

## 10. Diagnosing concurrent failure

Process attach, profilers, `tracemalloc` and post-mortem tooling are owned by
`python_runtime_diagnostics_manifest.md`. This section states only the concurrency-specific
instruments and their concurrency-specific failure modes.

### 10.1 asyncio debug mode belongs in CI

**ESTABLISHED.** Enable it with any of `PYTHONASYNCIODEBUG=1`, `-X dev` (Python Development Mode),
`asyncio.run(..., debug=True)`, or `loop.set_debug()`. What it gives you:

- logs callbacks slower than `loop.slow_callback_duration` (**default 100 ms / 0.1 s**) — the
  detector for the blocking call in §4.9;
- logs slow I/O-selector executions;
- **raises** on non-threadsafe API calls from the wrong thread — in debug mode, APIs such as
  `loop.call_soon()` and `loop.call_at()` "raise an exception if they are called from a wrong
  thread";
- emits a `RuntimeWarning` with the creation traceback for never-awaited coroutines.

**Rule — OPEN (project policy):** the test command runs with `-X dev`, and
`loop.slow_callback_duration` is tuned to a project-specific number rather than left at the default,
because 100 ms is a very generous budget for a loop that is supposed to be doing nothing but
waiting.

### 10.2 The async task graph

**VERSION-DEPENDENT (3.14) — none of this exists on 3.13.** In-process:
`asyncio.print_call_graph(future=None, /, *, file=None, depth=1, limit=None)`,
`asyncio.format_call_graph(future=None, /, *, depth=1, limit=None)` and
`asyncio.capture_call_graph(future=None, /, *, depth=1, limit=None)`, returning a
`FutureCallGraph(future, call_stack, awaited_by)` whose `call_stack` is a tuple of
`FrameCallGraphEntry(frame)` and whose `awaited_by` is a tuple of nested `FutureCallGraph` objects.
With no current task and no `future`, `format_call_graph()` returns an empty string and
`capture_call_graph()` returns `None` — so a diagnostic that prints nothing is not necessarily
broken.

Out-of-process: `python -m asyncio ps PID` prints a flat task table (tid, task id, task name,
coroutine stack, awaiter chain, awaiter name, awaiter id) and `python -m asyncio pstree PID` renders
the await tree; if cycles are detected in the await graph the tool raises an error listing the cycle
paths.

**The procedure has an off switch you do not control.** It rests on PEP 768 `sys.remote_exec(pid,
script)` (Final, 3.14), which can be disabled by the `PYTHON_DISABLE_REMOTE_DEBUG` environment
variable (any value, **including empty**), by `-X disable-remote-debug`, or by a build configured
`--without-remote-debug` — VERSION-DEPENDENT (3.14). Consequence: `python -m asyncio ps` silently
has no target in hardened environments and containers. **If a stuck-task procedure is in the
runbook, the absence of those switches is a deployment requirement**, and the attach mechanics
themselves are owned by `python_runtime_diagnostics_manifest.md`.

**Rule — OPEN (project policy):** on a 3.14+ floor, a long-running task that exceeds its budget logs
`asyncio.format_call_graph()` output on the failure path. That single line converts "it hung" into
"it was awaiting this".

### 10.3 "Task exception was never retrieved" is a test failure, not log noise

**ESTABLISHED.** A task whose exception is never read logs `Task exception was never retrieved` with
the future repr and the exception — **at destruction time**, i.e. at garbage collection, or never.
Debug mode adds the task-creation traceback.

Because the message arrives at GC, it can appear in a completely unrelated test, or in production
minutes after the failure, or not at all. **Rule — OPEN (project policy): the test suite treats that
message as a failure** (via a log-capturing check or a custom `loop.set_exception_handler` that
raises), and §4.2's orphan ban is what prevents it in the first place.

### 10.4 The deadlock watchdog

**ESTABLISHED.** `faulthandler.dump_traceback(file=sys.stderr, all_threads=True)` dumps every
thread's Python traceback, and `faulthandler.dump_traceback_later(timeout, repeat=False,
file=sys.stderr, exit=False)` is the watchdog form — the standard "the test suite hung, show me
where" instrument. `faulthandler.enable(file=sys.stderr, all_threads=True, c_stack=True)` installs
handlers for SIGSEGV, SIGFPE, SIGABRT, SIGBUS and SIGILL, with `c_stack=True` (VERSION-DEPENDENT
3.14) also printing the C stack after the Python traceback — useful when a crash is inside an
extension. Enable at startup with `-X faulthandler` or `PYTHONFAULTHANDLER`.
`faulthandler.register(signum, ...)` is "not available on Windows" — ESTABLISHED.

**The instrument degrades exactly where you need it most — VERSION-DEPENDENT (3.14):** "Changed in
version 3.14: only the current thread is dumped if the GIL is disabled to prevent the risk of data
races." On a free-threaded build the all-threads dump you rely on for deadlock diagnosis becomes a
single-thread dump. Plan a second signal — per-worker heartbeat logging with a bounded interval — if
free-threaded deadlock diagnosis matters. The general `faulthandler` surface is owned by
`python_runtime_diagnostics_manifest.md`.

`threading.settrace_all_threads(func)` and `threading.setprofile_all_threads(func)` install a
trace/profile function on "all threads started from the `threading` module and all Python threads
that are currently executing" — VERSION-DEPENDENT (3.12) — which is the hook for building an in-test
scheduler observer without touching each thread. Treat it as a diagnostic, not as production
instrumentation.

### 10.5 Data races on free-threaded builds: be honest, the answer is "little"

**FLAGGED-SECONDARY (py-free-threading.github.io, maintained by "Quansight Labs & open source
contributors") — ESTABLISHED within that source.** The only race detector CPython supports directly
is **ThreadSanitizer**, via the `--with-thread-sanitizer` configure option; the guide's build line
is `./configure --disable-gil --with-thread-sanitizer --prefix $PWD/cpython-tsan`, and CPython
carries a suppressions file at `Tools/tsan/suppressions_free_threading.txt`. Useful `TSAN_OPTIONS`
include `halt_on_error`, `suppressions`, `allocator_may_return_null`, `exitcode` and `log_path`.

**And its limit, which is the important part — FLAGGED-SECONDARY (same source):** TSan instruments
**compiled** code. It does **not** detect Python-level races — two threads doing `counter += 1`, or
a lost update through a `dict`. **No pure-Python race detector is recommended by the free-threading
guide.** Anyone promising that a tool will find your Python-level races is wrong.

`gdb`/`lldb` with the CPython `py-` command set (`py-bt`) work with `PYTHON_GIL=0`, but the same
guide footnotes that the lldb Python integration "is not correctly working on lldb after CPython
3.12" — **FLAGGED-SECONDARY, and OPEN** as to current status.

### 10.6 Therefore: stress and repetition, with the right expectations

**FLAGGED-SECONDARY (py-free-threading.github.io; the `pytest-run-parallel` README reached via a
search summary rather than a full page load).** The practical Python-level tactic is stress plus
repetition: `pytest-run-parallel` and `pytest-freethreaded` run the same test in a thread pool;
`pytest-run-parallel --forever` loops until a crash; and `pytest-repeat --count=100` (e.g.
`PYTHON_GIL=0 pytest -x -v --count=100 test_concurrent.py`) is recommended because "given the
non-deterministic nature of parallel execution, tests may still pass most of the time". Thread
barriers that align threads raise the clash probability.

Two corrections to the obvious misreading — FLAGGED-SECONDARY: `pytest-run-parallel` is explicitly
"not an alternative to pytest-xdist" and "not useful to speed up the execution of a test suite" — it
re-runs each test in a thread pool to **expose thread-unsafety**. And it automatically marks tests
that use `warnings` as thread-unsafe on Python 3.13 and older, and on 3.14 when the interpreter is
not configured for thread-safe warnings (see `-X context_aware_warnings`, §5.5) — VERSION-DEPENDENT
(3.13, 3.14).

**Free-threaded ecosystem readiness is not quantified in this file** — the source that would have
supplied a wheel-coverage figure returned HTTP 403 during verification, so **no number is asserted**
— OPEN. Determine it for your own dependency set with an actual install on a free-threaded
interpreter.

---

## 11. The do-not-transpose table

The seed pack adjudicates these; the verdicts are carried, not re-decided. An agent that imports a
row from §11.2 or §11.3 into a small Python app has produced a defect, not a sophistication.

### 11.1 The runtime already does this — a mapping table, never guidance

**ESTABLISHED as vocabulary; the mapping is the whole content.** Each corpus name maps to a stdlib
object. Import the row to make a design review conversation possible; do not write a pattern
implementation.

| corpus element | Python spelling | note |
|---|---|---|
| `monitor-object`, `scoped-locking` | `threading.Lock` + `with lock:` (and the `asyncio.*` twins) | `with lock:` **is** scoped locking / RAII |
| `reentrant-lock` | `threading.RLock` | sourced-adjacent editorial edge `thread-safe-interface --alternative-to--> reentrant-lock`: restructure the interface, or reach for `RLock` |
| `condition-variable`, `semaphore`, `latch` | `threading.Condition`, `Semaphore`, `Event`/`Barrier`, and the `asyncio.*` twins | `semaphore` naming: Dijkstra EWD123 (corpus `ewd123`, verified); `monitor-object` lineage: C. A. R. Hoare, *Monitors: An Operating System Structuring Concept*, CACM 17(10), 1974, DOI 10.1145/355620.361161 (corpus `hoaremonitors`) |
| `readers-writer-lock` | **absent** | Python has **no stdlib readers-writer lock**. State the absence; a hand-rolled one is a bug farm |
| `balking` / `guarded-suspension` | `lock.locked()` early-return vs `async with lock` | editorial edge `balking --alternative-to--> guarded-suspension`: same trigger, immediate failure vs waiting for the guard |
| `executor`, `thread-pool`, `future-promise`, `fork-join` | `concurrent.futures.*`, `asyncio.gather`, `TaskGroup` | §7.2. `future-promise`'s naming source (Liskov & Shrira, PLDI '88, corpus `liskovpromises`) is recorded **UNVERIFIED** |
| `coroutine`, `async-await-model` | `async def` / `await` — the language | citable origins: Melvin E. Conway, 1963 (corpus `conway1963`, verified) for `coroutine`; Syme, Petricek & Lomov, *The F# Asynchronous Programming Model*, 2011 (corpus `symeasync`, verified) for async/await, with `async-await-model --specializes--> coroutine` ("async functions are stackless coroutines") |
| `event-loop`, `reactor`, `proactor` | `asyncio.EventLoop`, `SelectorEventLoop`, `ProactorEventLoop` | §1.2, with the POSA2 and Wikipedia provenance caveats |
| `green-threads` | gevent/eventlet — history | the editorial edge `green-threads --alternative-to--> async-await-model` ("stackful user-space threads vs stackless compiler-rewritten async functions") is the exact axis of the gevent-vs-asyncio choice and the reason `await` must be written explicitly. Naming source is **Wikipedia** — OPEN (provenance) |
| `ring-buffer` | `collections.deque(maxlen=n)` | §7.1. Do not import the lock-free variants |
| `timeout` | `asyncio.timeout()`, socket timeouts | keep the sourced same-name edge `timeout --realizes--> timeout-tactic` so mechanism and tactic stay linked |
| `thunk` | `functools.cached_property`, a zero-arg lambda | keep only the editorial distinction `thunk --alternative-to--> future-promise`: "a thunk is lazy/synchronous, a future is asynchronous" |
| `continuation-passing-style` | `loop.call_soon` / `Future.add_done_callback` | asyncio's callback layer **is** CPS; `async`/`await` exists precisely so application code never writes it. Mention, do not teach |
| `currying-partial-application` | `functools.partial` | the corpus aka list literally reads "functools.partial (Python realization)" |
| `double-checked-locking` | module-level initialisation or `functools.cache` | the sourced edge `double-checked-locking --composes-with--> safe-publication` (JCiP 16.2.4: "DCL is broken without safe publication; making the reference volatile fixes it") is the reason **not** to hand-roll one in Python — you cannot supply the missing half |
| `safe-publication` | nothing to write | Python does not expose a memory model to application code. The corpus has **zero** free-threading coverage, so this is OPEN there rather than answered (§5.2) |
| `trampoline` | a `while` loop over returned step objects | Ganz, Friedman & Wand, *Trampolined Style*, ICFP '99, pp. 18-27 (corpus `ganztrampoline`, verified). CPython has **no tail-call elimination**, and raising `sys.setrecursionlimit` is not a fix. Edges: `trampoline --uses--> thunk`; `trampoline --realizes--> exception-prevention` ("prevents stack-overflow failures from arising at all"). The stack is a bounded resource, and a deeply recursive core is a crash waiting for a bigger input |

### 11.2 C / kernel / hardware / RTOS concerns — drop entirely

**ESTABLISHED as vocabulary; the verdict is the seed pack's.** There is **no correct Python spelling
of any of these**, because each requires control over instruction ordering, cache lines, interrupt
masking or a frame budget that Python does not give application code.

| family | elements (corpus ids) | why it cannot transpose |
|---|---|---|
| memory model & lock-free | `memory-barrier`, `acquire-release-ordering`, `compare-and-swap-loop`, `spinlock`, `test-and-test-and-set-lock`, `ticket-lock`, `mcs-queue-lock`, `sequence-lock`, `eventcount`, `futex`, `flat-combining`, `restartable-sequences`, `aba-mitigation-via-tagged-pointer`, `false-sharing-avoidance-via-cache-line-padding`, `read-copy-update` | all require control over instruction ordering and cache lines. If a design needs these, it needs a different language for that component. Cite Herlihy, Shavit, Luchangco & Spear, *The Art of Multiprocessor Programming*, 2nd ed., 2020, ISBN 978-0-12-415950-1 (corpus `herlihyshavit`, verified) to explain the exclusion, not to implement it |
| RTOS / embedded C / statechart frameworks | `critical-region`, `interrupt-masking-critical-section`, `nested-interrupt-handling`, `event-flags-group`, `direct-to-task-notification`, `guarded-call`, `rendezvous`, `priority-inheritance-protocol`, `priority-ceiling-protocol`, `ordered-locking`, `simultaneous-locking`, `protothread`, `cyclic-executive`, `time-triggered-co-operative-scheduler`, `multiple-event-receptor`, `single-event-receptor`, `decomposed-and-state`, `deferred-event`, `reminder`, `ultimate-hook`, `transition-to-history` | no interrupts, no priority inheritance, no scheduler hooks. **`multi-state-task` is the one member of this family that does transpose** (§1.3) |
| frame-budget / lock-policy designs | `spsc-lock-free-ring-buffer`, `disruptor`, `double-buffer`, `job-system`, `game-loop`, `stencil`, `spmd`, `fast-path`, `lock-striping`, `coarse-grained-lock`, `strategized-locking`, `thread-safe-interface`, `leader-followers` | each needs memory-ordering control, a compile-time lock-policy parameter, or a frame budget |
| language-runtime internals | `safepoint`, `deoptimization`, `threaded-code`, `bytecode-virtual-machine` | CPython has analogues, but they are not application-level design elements |

### 11.3 Right idea, wrong manifest — do not import here

**ESTABLISHED as vocabulary; the verdict is the seed pack's.**

| family | elements | belongs to |
|---|---|---|
| database / transaction concurrency control | `two-phase-locking`, `timestamp-ordering-concurrency-control`, `multiversion-concurrency-control`, `snapshot-isolation`, `lock-escalation`, `multi-granularity-locking`, `deadlock-detection`, `optimistic-concurrency-control`, `software-transactional-memory`, `fencing-token` | a persistence / data-store manifest. Adopting MVCC vocabulary for in-process state at this scale is over-engineering |
| business-transaction-scale locking | `optimistic-offline-lock`, `pessimistic-offline-lock`, `implicit-lock` | an application-architecture manifest |
| collaborative-editing convergence | `operational-transformation`, `conflict-free-replicated-data-type-crdt` | a distributed-state manifest. In a single-process app these solve a problem you do not have |
| effect systems | `monad`, `free-monad`, `tagless-final`, `effect-handler` | nowhere in Python. No do-notation, no higher-kinded types, no `effect`/`handle`; every attempt produces a library nobody reads. Import the **relation** instead — `functional-core-imperative-shell --alternative-to--> monad` (sourced; Seemann) — so the file can say *why* it takes the other branch (§3.1) |
| distributed time | `logical-clock`'s vector-clock / version-vector / hybrid-logical-clock forms | a distributed-systems manifest. The single-process form — a monotonic counter — is in §9.5 |

---

## Anti-patterns checklist

Each is a violation of a section above. **Reject on sight.**

- **Bare `asyncio.create_task(...)` with the result discarded** — the loop holds tasks weakly
  (§4.2).
- **`except Exception:` used to catch cancellation** — `CancelledError` is a `BaseException` (§4.5).
- **`except:` / `except BaseException:` in a task body** — swallows cancellation and hangs the
  enclosing `TaskGroup` or timeout forever (§4.5).
- **Catching `CancelledError` and not re-raising** — needs `Task.uncancel()` if the denial is
  genuine; anyio calls failing to re-raise "undefined behavior" (§4.4).
- **`await` during cleanup inside a cancelled scope, unshielded** — cancelled immediately (§4.4).
- **`except ValueError:` around `async with asyncio.TaskGroup()`** — failures arrive as a group
  (§4.6).
- **`try/except TimeoutError` inside `async with asyncio.timeout(...)`** — catchable only outside
  (§4.3).
- **Reading `Task.cancelling() > 0` as "cancelled"** — `cancelled()` is still `False` (§4.4).
- **`asyncio.shield()` used expecting the *caller* to survive** — it protects the inner awaitable
  (§4.4).
- **Installing `eager_task_factory` as a free speedup** — it changes ordering and exception timing
  (§4.7).
- **A blocking call inside a coroutine** — stalls every task on the loop (§4.9).
- **`asyncio.gather` on a path with a failure mode** — it does not cancel siblings (§4.1).
- **A fresh relative timeout at every hop** — pass an absolute deadline (§4.3).
- **`sysconfig.get_config_var("Py_GIL_DISABLED")` as a runtime GIL check** — it reports build
  capability; under `-X gil=1` it is still `1` while the GIL is on (§5.1).
- **Claiming free-threading is the default, or crediting PEP 703 with "officially supported"** — PEP
  779 is the supported-status PEP (§5).
- **Claiming a free-threaded speedup without asserting `sys._is_gil_enabled()`** — one unmarked C
  extension re-enables the GIL with a printed warning (§5.1, §5.3).
- **Relying on `dict`/`list`/`set` internal locks** — "not a guarantee"; `counter += 1` was never
  atomic (§5.2).
- **Sharing one iterator across threads** — "duplicate or missing elements"; the
  `threading.serialize_iterator` family exists only from 3.15 (§5.2).
- **Reading another thread's `frame.f_locals`** — may crash the interpreter (§5.2).
- **Quoting one free-threading overhead figure as *the* number** — four live in four sources (§5.4).
- **Assuming C critical sections give mutual exclusion** — they "may temporarily release their
  locks" and are no-ops on GIL builds (§5.3).
- **"We ship `abi3`, so we support free-threading"** — false, and the HOWTO conflicts with PEP 803
  (§5.3).
- **Treating subinterpreters as a sandbox** — never strictly isolated within a process (§6.1).
- **Submitting a lambda, closure or local class to `InterpreterPoolExecutor`** — everything is
  pickled and a non-shareable worker exception becomes `None` (§6.2).
- **Believing `create_queue()` takes no arguments** — the shipped signature is `create(maxsize=0, *,
  unbounditems=UNBOUND)`; there is no `syncobj` (§6.1).
- **Writing `interpreters` as the module name** — it is `concurrent.interpreters` (§6).
- **Any queue created without an explicit `maxsize` and a written overflow policy** (§7.1).
- **`Executor.map()` whose result iterator is never consumed** — every worker exception is lost
  (§7.3).
- **Treating an executor as bounded** — unbounded queue, and `map()` collects eagerly without
  `buffersize` (§7.2).
- **A defaulted `max_workers`** — a capacity decision made by the interpreter version (§7.2).
- **`shutdown(cancel_futures=True)` as a stop button** — only *pending* work is cancelled (§7.4).
- **Nesting `submit()` on the same pool** — documented deadlock, no exception, no timeout (§7.5).
- **Locks without a documented lock order** — Python has neither deadlock detection nor ordered
  locking (§7.5; `architecture_manifest_default.md` §3.4).
- **Assuming `fork` is the POSIX default** — `forkserver` from 3.14; `fork` from a multi-threaded
  process has warned since 3.12 (§7.6).
- **Module-level side effects in code a process pool imports** — they run again in every worker
  (§7.6).
- **`multiprocessing.Manager` shared mutable state** — shared-nothing is the design (§3.3).
- **`threading.local()` for request-scoped state in asyncio** — many tasks share one thread (§8.1).
- **Setting a `ContextVar` in a task and expecting the caller to see it** — the task gets a copy
  (§8.3).
- **Relying on thread context inheritance** — the default differs by build (§5.5, §8.2).
- **Passing a `ProcessPoolExecutor` to `loop.run_in_executor`** — must be a `ThreadPoolExecutor`
  (§4.9).
- **Installing a custom asyncio event-loop policy in tests** — deprecated with a removal scheduled;
  use `loop_factory` / `asyncio.Runner` (§9.2).
- **`await asyncio.sleep(0.05)` as test synchronisation** — "never use bare sleeps" (§9.3).
- **`ThreadPoolExecutor(max_workers=1)` called "single-threaded under test"** — it keeps the thread
  boundary (§9.4).
- **A fixed seed presented as making a concurrent test deterministic** (§9.6).
- **Letting a plugin default decide event-loop lifetime under test** — pin it
  (§9.2; `python_testing_tooling_manifest.md` §6d).
- **Treating "Task exception was never retrieved" as log noise** — it arrives at GC, or never
  (§10.3).
- **Relying on an all-threads `faulthandler` dump on a free-threaded build** — it degrades to the
  current thread only (§10.4).
- **Expecting ThreadSanitizer to find Python-level races** — it instruments compiled code (§10.5).
- **Calling `pytest-run-parallel` a speedup** — explicitly not an xdist alternative (§10.6).
- **Importing any row of §11.2 or §11.3 into a small single-process app** — over-engineering by
  construction.

---

## Open questions to resolve before building

Each is a decision this project must make and record, split per
`software_spec_discipline_manifest.md` §G5 into **ASSUMED** (proceeding on a default) and
**NEEDS-INPUT** (awaiting the owner).

1. **OPEN — the minimum version floor for concurrency features.** `TaskGroup` / `asyncio.timeout`
   need 3.11, the eager task factory 3.12, `Queue.shutdown` 3.13, `concurrent.interpreters` /
   `InterpreterPoolExecutor` / `map(buffersize=)` / the asyncio task graph 3.14, and
   `TaskGroup.cancel()` / the `threading.serialize_iterator` family 3.15. The floor decides which
   sections here are available at all; route the version and support facts through
   `python_platform_baseline_manifest.md`.
2. **OPEN — raw asyncio, or anyio/trio.** §4.8 states what each buys (level cancellation,
   `MockClock`, `wait_all_tasks_blocked`) and costs. Decide once, project-wide; a codebase holding
   both models is the worst outcome.
3. **OPEN — where exactly the core/shell seam sits**, and therefore which modules may import
   `asyncio`, `threading` or `concurrent.futures` at all. `error_tracing_contract_manifest.md` §6
   requires the same seam tagged for error conversion — use one seam, not two.
4. **OPEN — the overflow policy per queue** (§7.1): a chosen row from that table, an owner, and
   whether overflow is observable to the caller as a typed rejection.
5. **OPEN — `max_workers` and the in-flight bound per pool** (§7.2), as numbers with a rationale.
6. **OPEN — whether the project targets a free-threaded build at all** (§5). If yes: name the
   hazard-list owner, the CI job that runs on the free-threaded interpreter, and the assertion that
   `sys._is_gil_enabled()` is `False` where parallelism is claimed. If no, say so explicitly so the
   question stops recurring.
7. **OPEN — whether "Task exception was never retrieved" and asyncio debug-mode warnings fail the
   build** (§10.1, §10.3), and what `loop.slow_callback_duration` is set to.
8. **OPEN — the deterministic-replay decision** (§9.5): is the core sequenced enough to justify a
   seed-plus-input-log harness, or is per-seam injection sufficient? Answer before designing the
   log.
9. **OPEN — the quarantine policy for irreducibly flaky concurrent tests** (§9.6): where they live,
   who owns them, the time box. The suite mechanism belongs to `python_testing_tooling_manifest.md`.
10. **OPEN (provenance) — whether to keep leaning on POSA2 vocabulary.** `reactor`, `proactor`,
    `half-sync-half-async`, `thread-specific-storage` and `asynchronous-completion-token` all rest
    on one corpus record recorded UNVERIFIED with an unresolved year (§1.2). Verify the ISBN and
    year once, or use the names descriptively without presenting them as sourced.
11. **OPEN — the `concurrent.interpreters` queue-exception names**:
    `QueueEmptyError`/`QueueFullError` in the docs versus `QueueEmpty`/`QueueFull` in `__all__`
    (§6). Verify against the interpreter you target before writing an `except` clause.

---

## Sources (accessed 8 Aug 2026)

- Four concurrency substrates; `InterpreterPoolExecutor`; the five stated subinterpreter
  limitations; free-threaded penalty "roughly 5-10%"; PEP 659 in free-threaded mode; `-X
  context_aware_warnings` and `thread_inherit_context` defaults; `python -m asyncio ps|pstree`;
  `forkserver` as the POSIX default — https://docs.python.org/3/whatsnew/3.14.html . Accessed 8 Aug
  2026.
- `TaskGroup.cancel()` and the boilerplate it replaces; `threading.serialize_iterator` /
  `synchronized_iterator` / `concurrent_tee`; hierarchical per-module import locks; PID and exit
  code for an abruptly dead pool child; PEP 803; PEP 788 —
  https://docs.python.org/3.15/whatsnew/3.15.html . Accessed 8 Aug 2026.
- PEP 703 (Final, Python-Version 3.13) — the implementation PEP; `--disable-gil`, `Py_GIL_DISABLED`,
  the `t` ABI tag, 5-6% / 7-8% overhead — https://peps.python.org/pep-0703/ . Accessed 8 Aug 2026.
- PEP 779 (Final, Python-Version 3.14) — Phase II as "officially supported but still optional"; the
  15% target; Phase III "left for a future PEP" — https://peps.python.org/pep-0779/ . Accessed 8 Aug
  2026.
- PEP 734 (Final, 3.14) — the rename to `concurrent.interpreters`, `Interpreter` methods,
  `create_queue(maxsize=0)`, crossing rules, exception family — https://peps.python.org/pep-0734/ .
  Accessed 8 Aug 2026.
- PEP 768 (Final, 3.14) — `sys.remote_exec(pid, script)` and the `PYTHON_DISABLE_REMOTE_DEBUG` / `-X
  disable-remote-debug` / `--without-remote-debug` off switches — https://peps.python.org/pep-0768/
  . Accessed 8 Aug 2026.
- PEP 803 (Final, 3.15) — `abi3t`, `Py_TARGET_ABI3T`, opaque `PyObject`, the `abi3.abi3t` wheel tag,
  `.abi3t.so` — https://peps.python.org/pep-0803/ . Accessed 8 Aug 2026.
- PEP 788 (Final, 3.15) — interpreter guards and views, `PyThreadState_Ensure()` / `_Release()`, the
  `PyGILState` soft deprecation — https://peps.python.org/pep-0788/ . Accessed 8 Aug 2026.
- Free-threading HOWTO — build vs runtime detection; `PYTHON_GIL` / `-X gil`; the automatic GIL
  re-enable with a printed warning; the 1%-to-8% sentence; `frame.f_locals` and shared-iterator
  hazards; built-in locking as an implementation detail —
  https://docs.python.org/3/howto/free-threading-python.html and
  https://docs.python.org/3.15/howto/free-threading-python.html . Accessed 8 Aug 2026.
- Free-threading extensions HOWTO — `Py_mod_gil` / `Py_MOD_GIL_NOT_USED`,
  `PyUnstable_Module_SetGIL()`, the borrowed-to-strong replacements, `Py_BEGIN_CRITICAL_SECTION`
  semantics, and the still-live "does not currently support the Limited C API or the stable ABI"
  paragraph — https://docs.python.org/3/howto/free-threading-extensions.html and
  https://docs.python.org/3.15/howto/free-threading-extensions.html . Accessed 8 Aug 2026.
- Command line — `-X gil=0,1` and `PYTHON_GIL` precedence, `-X dev`, `-X thread_inherit_context`,
  `-X context_aware_warnings`, `PYTHONHASHSEED` range and the `0`-disables rule, `-R` —
  https://docs.python.org/3/using/cmdline.html . Accessed 8 Aug 2026.
- `concurrent.interpreters` — shareable types, the pickle default, `Interpreter` signatures, "since
  Python 3.12" for GIL non-sharing, the not-strictly-isolated statement,
  `QueueEmptyError`/`QueueFullError` —
  https://docs.python.org/3/library/concurrent.interpreters.html and
  https://docs.python.org/3.15/library/concurrent.interpreters.html . Accessed 8 Aug 2026.
- Shipped queue source — `create(maxsize=0, *, unbounditems=UNBOUND)`, `Queue.put`/`get` signatures,
  no `syncobj` —
  https://raw.githubusercontent.com/python/cpython/3.14/Lib/concurrent/interpreters/_queues.py and
  https://raw.githubusercontent.com/python/cpython/3.15/Lib/concurrent/interpreters/_queues.py .
  Accessed 8 Aug 2026.
- Shipped `__all__` for the module —
  https://raw.githubusercontent.com/python/cpython/3.15/Lib/concurrent/interpreters/__init__.py .
  Accessed 8 Aug 2026.
- `InterpreterPoolExecutor` as a `ThreadPoolExecutor` subclass, and `None` substituted for a
  non-shareable worker exception —
  https://raw.githubusercontent.com/python/cpython/3.15/Lib/concurrent/futures/interpreter.py .
  Accessed 8 Aug 2026.
- `concurrent.futures` — `map()` exceptions at retrieval; `shutdown(wait, cancel_futures)`;
  `max_workers` defaults and the Windows 61 cap; `chunksize` a no-op for thread and interpreter
  pools; `map(buffersize=)` and eager collection; `BrokenThreadPool` / `BrokenProcessPool`; the
  nested-future deadlock warning; the `set_result` / `set_exception` /
  `set_running_or_notify_cancel` unit-test sanction; `wait()` / `as_completed()` and
  `FIRST_EXCEPTION` — https://docs.python.org/3/library/concurrent.futures.html . Accessed 8 Aug
  2026.
- asyncio tasks — `TaskGroup` failure, cancellation and aggregation plus the
  `KeyboardInterrupt`/`SystemExit` case; `timeout`/`timeout_at` and `reschedule()`;
  `eager_task_factory`; `cancel`/`uncancel`/`cancelling`; `shield()`; the weak-reference warning;
  `CancelledError` subclassing `BaseException` — https://docs.python.org/3/library/asyncio-task.html
  . Accessed 8 Aug 2026.
- `TaskGroup.cancel()` "Added in version 3.15" with its non-exceptional-exit semantics, and the 3.15
  `GeneratorExit` case — https://docs.python.org/3.15/library/asyncio-task.html . Accessed 8 Aug
  2026.
- asyncio development mode — activation routes; `loop.slow_callback_duration` default 100 ms;
  wrong-thread exceptions for `call_soon`/`call_at`; never-awaited warnings; "Task exception was
  never retrieved"; `call_soon_threadsafe` / `run_coroutine_threadsafe`; "almost all asyncio objects
  are not thread safe" — https://docs.python.org/3/library/asyncio-dev.html . Accessed 8 Aug 2026.
- asyncio call-graph introspection — `print_call_graph` / `format_call_graph` /
  `capture_call_graph`, `FutureCallGraph`, `FrameCallGraphEntry`, and the empty / `None` returns —
  https://docs.python.org/3/library/asyncio-graph.html . Accessed 8 Aug 2026.
- `asyncio.run` and `asyncio.Runner` — `loop_factory`, `Runner.run(coro, *, context=None)`, lazy
  loop initialisation, a new loop per `run()` —
  https://docs.python.org/3/library/asyncio-runner.html . Accessed 8 Aug 2026.
- asyncio event loop — the policy system "deprecated and will be removed in Python 3.16";
  `get_event_loop()` raising `RuntimeError`; `run_in_executor` requiring a `ThreadPoolExecutor`;
  `asyncio.EventLoop` aliasing per platform —
  https://docs.python.org/3/library/asyncio-eventloop.html . Accessed 8 Aug 2026.
- `asyncio.Queue` — `maxsize <= 0` infinite, `shutdown(immediate=False)` and `QueueShutDown`, "not
  thread safe" — https://docs.python.org/3/library/asyncio-queue.html . Accessed 8 Aug 2026.
- `queue` — blocking-put semantics, `shutdown` and `queue.ShutDown`, `SimpleQueue`'s unbounded
  reentrant implementation — https://docs.python.org/3/library/queue.html . Accessed 8 Aug 2026.
- `multiprocessing` — start methods, the 3.14 POSIX default change to `forkserver`, the 3.12
  `DeprecationWarning` for `os.fork()` in a multi-threaded process, `get_context` /
  `set_start_method(force=)` — https://docs.python.org/3/library/multiprocessing.html . Accessed 8
  Aug 2026.
- `threading` (3.15) — `serialize_iterator`, `synchronized_iterator`, `concurrent_tee(iterable,
  n=2)` with the `n == 0` and negative-`n` rules; `settrace_all_threads` / `setprofile_all_threads`
  — https://docs.python.org/3.15/library/threading.html . Accessed 8 Aug 2026.
- `faulthandler` — `dump_traceback`, `dump_traceback_later`, `enable(..., c_stack=True)`,
  `register()` unavailable on Windows, and "only the current thread is dumped if the GIL is
  disabled" — https://docs.python.org/3/library/faulthandler.html . Accessed 8 Aug 2026.
- anyio 4.14.2 — "Trio-like structured concurrency on top of asyncio" —
  https://pypi.org/project/anyio/ . Accessed 8 Aug 2026. Version history, including 4.14.0's
  `TaskGroup.cancel()` and the 4.14.1 / 4.14.2 deadlock and cancellation-delivery fixes —
  https://anyio.readthedocs.io/en/stable/versionhistory.html . Accessed 8 Aug 2026.
- anyio cancellation — level versus edge cancellation (quoted), the shielding rule, "always reraise
  the cancellation exception if you catch it" —
  https://anyio.readthedocs.io/en/stable/cancellation.html . Accessed 8 Aug 2026.
- trio 0.33.0 — "based on a new way of thinking that we call 'structured concurrency'" —
  https://pypi.org/project/trio/ . Accessed 8 Aug 2026. Version note: `/en/latest/history.html` plus
  PyPI are canonical; `/en/stable/history.html` is a stale mirror —
  https://trio.readthedocs.io/en/latest/history.html . Accessed 8 Aug 2026.
- trio core — nursery entry/exit and `start_soon`; `ExceptionGroup` on child failure; `CancelScope`
  attributes; `move_on_after` / `fail_after` / `move_on_at` / `fail_at`; level-triggered
  cancellation; the checkpoint rule; `trio.Cancelled` inheriting `BaseException` —
  https://trio.readthedocs.io/en/stable/reference-core.html . Accessed 8 Aug 2026.
- trio testing — `MockClock(rate=0.0, autojump_threshold=inf)` and `jump()`'s `ValueError`,
  `wait_all_tasks_blocked(cushion=0.0)`, `Sequencer`, `RaisesGroup` —
  https://trio.readthedocs.io/en/stable/reference-testing.html . Accessed 8 Aug 2026.
- pytest-asyncio — the loop-scope settings and their documented future default change, cited here
  only to route the obligation to the manifest that owns it —
  https://pytest-asyncio.readthedocs.io/en/latest/reference/configuration.html . Accessed 8 Aug
  2026; release identity — https://pypi.org/project/pytest-asyncio/ . Accessed 8 Aug 2026.
- Hypothesis — `derandomize`, `@seed()` overriding it, and the fixed-seed caveat about timing, hash
  randomization and external state — https://hypothesis.readthedocs.io/en/latest/reference/api.html
  . Accessed 8 Aug 2026.
- Martin Fowler, *Eradicating Non-Determinism in Tests* — the six categories, "never use bare
  sleeps", "always wrap the system clock", quarantine —
  https://martinfowler.com/articles/nonDeterminism.html . Accessed 8 Aug 2026.
- **FLAGGED-SECONDARY** — ThreadSanitizer for CPython: `--with-thread-sanitizer`, `TSAN_OPTIONS`,
  `Tools/tsan/suppressions_free_threading.txt`, compiled-code-only coverage. Maintained by
  "Quansight Labs & open source contributors" —
  https://py-free-threading.github.io/thread_sanitizer/ . Accessed 8 Aug 2026.
- **FLAGGED-SECONDARY** — Python-level race hunting: `pytest-run-parallel`, `pytest-freethreaded`,
  `pytest-repeat --count=100` with `PYTHON_GIL=0`, barriers, and the gdb/lldb `py-` caveat after
  CPython 3.12 — https://py-free-threading.github.io/debugging/ . Accessed 8 Aug 2026.
- **FLAGGED-SECONDARY** (README reached via a search-result summary, not a full page load) —
  `pytest-run-parallel` is "not an alternative to pytest-xdist", has `--forever`, and auto-marks
  warnings-using tests as thread-unsafe on 3.13 and older —
  https://github.com/Quansight-Labs/pytest-run-parallel . Accessed 8 Aug 2026.

### Named vocabulary — naming sources as recorded in the SWE corpus

Verification status is the corpus's own field; anything marked UNVERIFIED must not be presented as
verified by a later pass. Books and papers are cited bibliographically because the corpus records no
URL for them; no URL is invented.

**Verified in the corpus.**

- `limit-nondeterminism`, `bound-queue-sizes` — Bass, Clements & Kazman, *Software Architecture in
  Practice*, 4th ed., 2021, ISBN 978-0-13-688609-9 (`bck`).
- `structured-concurrency` — Nathaniel J. Smith, *Notes on structured concurrency, or: Go statement
  considered harmful*, vorpus.org, 2018-04-25 (`vorpussc`).
- `run-to-completion-event-processing` — Miro Samek, *Practical UML Statecharts in C/C++*, 2nd ed.,
  2008, Newnes, ISBN 978-0-7506-8706-5 (`samekbook`).
- `functional-core-imperative-shell` — Gary Bernhardt, *Functional Core, Imperative Shell*, Destroy
  All Software screencast, 2012 (`bernhardtfcis`); the `alternative-to--> monad` edge is sourced to
  Mark Seemann, *Impureim sandwich*, ploeh blog, 2020.
- `thread-confinement`, the `executor`/`thread-pool` framing, `double-checked-locking` — Goetz,
  Peierls, Bloch, Bowbeer, Holmes & Lea, *Java Concurrency in Practice*, 2006, ISBN
  978-0-321-34960-6 (`jcip`).
- `two-phase-termination`, `balking`, `guarded-suspension` — Mark Grand, *Patterns in Java, Volume
  1*, 1998 (`grandjava`).
- `cancellation-token` — Microsoft Learn, *Cancellation in Managed Threads*, living
  (`mscancellation`). The element's Go-blog half (Ajmani, 2014) **has no corpus work record** —
  OPEN.
- `deadline-propagation` — Beyer, Jones, Petoff & Murphy (eds.), *Site Reliability Engineering*,
  2016 (`googlesre`), "Addressing Cascading Failures".
- `producer-consumer`, `semaphore` — Dijkstra, *Cooperating Sequential Processes* (EWD123), 1965, E.
  W. Dijkstra Archive, UT Austin (`ewd123`; the transcription page is undated and 1965 is the
  archive's standard dating); also Allen B. Downey, *The Little Book of Semaphores* (`downeysem`,
  **year not recorded in the corpus**).
- `monitor-object` lineage — C. A. R. Hoare, *Monitors: An Operating System Structuring Concept*,
  CACM 17(10), 1974, DOI 10.1145/355620.361161 (`hoaremonitors`).
- `competing-consumers` — Hohpe & Woolf, *Enterprise Integration Patterns*, 2003 (`hohpe`).
  `sequential-convoy` and `queue-based-load-leveling` — Azure Architecture Center Cloud Design
  Patterns (`azurepatterns`) — **the corpus record's title is stored as "Cloud Design Patterns:
  Cache-Aside"; cite the specific Azure page, never that title** — OPEN (provenance).
- `self-pipe-trick` — Michael Kerrisk, *The Linux Programming Interface*, 2010, sec. 63.5.2
  (`kerrisktlpi`); the `composes-with--> event-loop` edge is sourced to D. J. Bernstein.
- `pipes-and-filters` — Buschmann, Meunier, Rohnert, Sommerlad & Stal, *POSA Vol. 1: A System of
  Patterns*, 1996 (`posa1`). `collection-pipeline` — Martin Fowler, *Collection Pipeline*,
  martinfowler.com, 2015 (`fowlerpipeline`). `lmax-architecture` — Martin Fowler, *The LMAX
  Architecture*, martinfowler.com, 2011-07-12 (`lmaxfowler`).
- `immutable-value`, `context-object`, `copied-value` — Buschmann, Henney & Schmidt, *POSA Vol. 4: A
  Pattern Language for Distributed Computing*, 2007 (`posa4`).
- `defensive-copy` — Joshua Bloch, *Effective Java*, 3rd ed., 2018, Item 50 (`effjava`).
- `defunctionalization` — John C. Reynolds, *Definitional Interpreters for Higher-Order Programming
  Languages*, 1972 (`reynolds72`). `trampoline` — Ganz, Friedman & Wand, *Trampolined Style*, ICFP
  '99, pp. 18-27 (`ganztrampoline`).
- `actor-based-architecture` — Hewitt, Bishop & Steiger, *A Universal Modular ACTOR Formalism for
  Artificial Intelligence*, IJCAI-73, 1973 (`hewitt1973`).
- `logical-clock` — Leslie Lamport, *Time, Clocks, and the Ordering of Events in a Distributed
  System*, CACM 1978 (`lamportclocks`). `deterministic-lockstep` — Glenn Fiedler, *Deterministic
  Lockstep*, gafferongames.com, living (`gafferongames`, verified per the corpus note; Bettner &
  Terrano, GDC 2001, recorded on the same element).
- `coroutine` — Melvin E. Conway, 1963 (`conway1963`). `async-await-model` — Syme, Petricek & Lomov,
  *The F# Asynchronous Programming Model*, 2011 (`symeasync`).
- `spmd`, `master-slave`, `pipeline-parallelism` and the `fork-join` framing — Mattson, Sanders &
  Massingill, *Patterns for Parallel Programming*, 2004, ISBN 978-0-321-22811-6 (`mattsonppp`), ch.
  5.
- The lock-free family, cited only to explain its exclusion — Herlihy, Shavit, Luchangco & Spear,
  *The Art of Multiprocessor Programming*, 2nd ed., 2020, ISBN 978-0-12-415950-1 (`herlihyshavit`).
- `persistent-data-structure` — the naming work (Driscoll, Sarnak, Sleator & Tarjan, JCSS 1989)
  **has no corpus work record**; the carrying work is Chris Okasaki, *Purely Functional Data
  Structures*, 1998, doi:10.1017/CBO9780511530104 (`okasaki`), with `hash-array-mapped-trie-hamt`
  sourced to Phil Bagwell, *Ideal Hash Trees*, 2001 (`bagwell2001`) — OPEN (naming provenance).

**UNVERIFIED in the corpus — do not upgrade without a fresh primary check.**

- `reactor`, `proactor`, `half-sync-half-async`, `leader-followers`,
  `asynchronous-completion-token`, `thread-specific-storage`, `monitor-object`, `scoped-locking`,
  `thread-safe-interface`, `strategized-locking`, `double-checked-locking` — Schmidt, Stal, Rohnert
  & Buschmann, *POSA Vol. 2: Patterns for Concurrent and Networked Objects* (`posa2`, **unverified;
  year UNRESOLVED**).
- `backpressure`, `bulkhead`, `timeout` — Nygard, *Release It!* (`nygard`, **unverified; year
  UNRESOLVED**).
- `shared-nothing-architecture` — Stonebraker, *The Case for Shared Nothing*, IEEE Database
  Engineering Bulletin 9(1), 1986 (`sharednothing`, **unverified; the corpus records that no DOI
  exists**).
- `multi-state-task` — M. J. Pont, *Patterns for Time-Triggered Embedded Systems*, 2001 (`pont`).
- `future-promise` — Liskov & Shrira, PLDI '88 (`liskovpromises`). `event-driven-architecture` —
  Richards & Ford, *Fundamentals of Software Architecture* (`richardsford`, **year UNRESOLVED**).
- `event-loop` and `green-threads` are named from **Wikipedia** in the corpus; cite `reactor`/POSA2,
  Node's documentation, or JEP 444 instead — OPEN (provenance).

### Sibling manifests (cross-referenced, not duplicated)

- `python_platform_baseline_manifest.md` — **all** release dates, support phases, EOL,
  PEP-status-by- version, interpreter switches and build variants. This file states behaviour and
  gates it inline; it asserts no schedule of its own.
- `python_testing_tooling_manifest.md` — determinism of tests **in general**: §6c (suite-wide clock
  and seed policy, record/playback, quarantine), §4a (Hypothesis settings and the CI profile), §6d
  (async test runners, plugin choice and loop scope), §6e (parallel execution), plus the
  `ExceptionGroup`-assertion tooling choice. This file owns determinism **of concurrent code** only,
  and that manifest's §6c defers the design rationale here.
- `error_tracing_contract_manifest.md` — `except*` mechanics (§18), the exception hierarchy and
  bare-except prohibition (§11, §12), chaining, and where the result/exception seam sits (§6). This
  file states only the cancellation- and TaskGroup-specific consequences.
- `python_runtime_diagnostics_manifest.md` — process attach, `sys.remote_exec` / `pdb -p PID`,
  `faulthandler` as a general surface, `tracemalloc`, profilers, post-mortem and health surfaces.
  This file states only the concurrency-specific instruments and their concurrency-specific
  degradations.
- `logging_observability_manifest.md` — log emission, handlers, structured output and correlation-ID
  propagation. This file states only where the propagation *mechanism* stops working (§8.3).
- `python_typing_contract_manifest.md` — `Protocol` seams for injected clocks and executors, frozen
  dataclasses, immutability and tagged-union mechanics used by §6.1 and §8.4.
- `python_module_boundaries_manifest.md` — the import-direction fitness function that mechanically
  enforces §3.2's core/shell rule.
- `python_quality_gates_manifest.md` — which of §3.2's and §10's checks run in CI, how they fail,
  and how the standard is ratcheted in without a big-bang rewrite.
- `python_language_hazards_manifest.md` — intrinsic language footguns and their enforcement routes.
  `python_linting_practices_manifest.md` — the rule inventory this file declines to guess at (§3.2).
- `architecture_manifest_default.md` — the paradigm-choice reasoning frame (§3.4 concurrency, §3.2
  state and ownership, §4.4 determinism), including the house rule that a documented lock order is
  part of the design. Its four state-sharing paradigms are **not** this file's four substrates
  (§2.1).
- `software_spec_discipline_manifest.md` — §G5 ASSUMED/NEEDS-INPUT split for every open question
  above.
