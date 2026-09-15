# Card: add concurrency

**Load when:** introducing threads, `asyncio`, processes or subinterpreters — or changing anything that
already uses them.
**Depth:** `reference/python_concurrency_determinism_manifest.md`. Failure-channel design is in
`cards/handle-errors.md`; version status of free-threading and subinterpreters is a hub fact.

## First, consider not doing it

Concurrency is the most expensive thing you can add to a testable system: it converts deterministic
failures into intermittent ones. **Push it to the edge and keep the core sequential and pure.** A
single-threaded core with a concurrent shell is testable; the reverse is not. If the motivation is
latency on a handful of I/O calls, that is `asyncio` in the shell — not a threaded architecture.

## Choose the model deliberately

| model | correct when | real parallelism | characteristic silent failure |
|---|---|---|---|
| **`asyncio`** | many concurrent I/O waits, one CPU's worth of work | no (one thread) | a blocking call stalls the whole loop; an un-referenced task vanishes |
| **threads** | blocking I/O in libraries with no async API; GUI/driver callbacks | not on a GIL build | data races on shared mutable state; the GIL never guaranteed what people assume |
| **processes** | CPU-bound work | yes | everything crossing the boundary must pickle; costs are easy to underestimate |
| **subinterpreters** | isolated in-process parallelism | yes | a narrow boundary contract — what may cross is restricted |

Free-threaded builds change the threading answer, but **status and detection are hub facts** — check
hub §5 rather than assuming, and never quote a bare performance percentage: the primary sources disagree
and the manifest forbids it.

## Do — `asyncio`

1. **`TaskGroup`, not bare `create_task`.** A task with no reference held can be garbage-collected
   mid-flight (`RUF006`). A `TaskGroup` gives you structured lifetime: nothing outlives the block.
2. **Failures arrive as an `ExceptionGroup`.** Write `except*`, and read the `except*` rules in
   `cards/handle-errors.md` — they are rules, not style.
3. **`asyncio.timeout()` for deadlines**, and propagate the deadline rather than re-deriving it at each
   layer.
4. **`CancelledError` is a `BaseException`.** `except Exception` does not catch it — by design. Never
   swallow it; if you must clean up, re-raise. Shield only what genuinely must complete, and understand
   that shielding delays shutdown.
5. **Never a blocking call in a coroutine** — no `time.sleep`, no synchronous HTTP, no blocking file I/O
   on a hot path. Route: `lint-catchable` `ASYNC`.
6. **Retrieve every task's exception.** An unretrieved exception surfaces only as a late warning, often
   after the context that would explain it is gone.

## Do — anything concurrent

7. **Every queue declares `maxsize` and an overflow policy** — block, drop-oldest, drop-newest, or fail.
   An unbounded queue is a deferred out-of-memory failure that looks like a memory leak.
8. **Shutdown is part of the design, not an afterthought.** Two phases: stop accepting, then drain with a
   deadline. Decide `cancel_futures` explicitly. A process that cannot shut down cleanly cannot be
   deployed safely.
9. **State ownership is explicit.** Thread confinement by default; a `contextvars` context, a
   `threading.local`, or an explicitly-passed context object — chosen, not defaulted. Know that a Task
   *copies* the context at creation, and that this does not propagate across threads.
10. **Never `sleep` to synchronise.** An event, a condition, or a barrier — `sleep` is a race with a
    timer.

## Determinism — the part that makes it testable

Four seams, all injected as parameters:

- **the clock** — never call `time.time()` or `datetime.now()` in logic under test
- **the seed** — one source of randomness, injected
- **the executor** — so a test can substitute an inline, single-threaded one
- **the event loop / scheduler** — so ordering is controlled, not observed

With those four, most concurrent logic runs **single-threaded and ordered under test**, which is the only
way concurrent code gets a non-flaky suite. Where the domain permits, deterministic replay against a
recorded interleaving is stronger still. What you **cannot** buy this way: proof of absence of races —
that needs a different class of tool, and on free-threaded builds the honest answer about tooling today
is "little". → concurrency §8–§9

## Never

- Share mutable state across threads with no lock and no stated ownership rule.
- Assume any Python operation is atomic because of the GIL.
- Catch `Exception` around an `await` where cancellation must propagate.
- Start a background task in module scope or at import time.
- Add a thread pool to make tests faster.
- Import an RTOS or C-idiom concurrency mechanism because the name is familiar — the manifest's
  do-not-transpose table says which ones the runtime already handles. → concurrency §10

## Diagnosing it later

`asyncio` debug mode · a task-graph dump · never-retrieved-exception warnings · a `faulthandler`
watchdog for deadlocks. Set these up **before** you need them. → `cards/diagnose-runtime.md`

## Decisions you must not invent

Which model, and why the simpler one was rejected · whether free-threading is supported, experimental,
or out of scope · queue bounds and overflow policy per queue · the shutdown contract and its deadline ·
what is allowed to cross a process or interpreter boundary.

## Go deeper

| question | where |
|---|---|
| the four-model table, argued in full | concurrency §1 |
| structured concurrency, cancellation, shielding | concurrency §3 |
| free-threading as behaviour: locking, C extensions, atomicity myths | concurrency §4 |
| subinterpreter boundary contract | concurrency §5 |
| backpressure and shutdown obligations | concurrency §6 |
| determinism tactics and their limits | concurrency §8 |
| version status of any of the above | hub §4a, §5 |
