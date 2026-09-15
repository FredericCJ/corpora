# Card: design error handling

**Load when:** deciding how a failure travels, adding an exception type, validating input, or touching a
`try` block.
**Depth:** `reference/error_tracing_contract_manifest.md`. Type-system mechanics live in
`reference/python_typing_contract_manifest.md`; logging policy in `cards/observability.md`.

## The one decision everything follows from

Python has **no checked exceptions** — a `raise` is invisible to the type system, so it is not part of a
function's enforced signature. An in-band value **is** enforceable. So:

| the failure is… | channel | why |
|---|---|---|
| an expected, recoverable **domain outcome** the caller must reason about (validation rejected, not-found where absence is normal, business rule denied) | **typed in-band result** — a union of frozen variants | the checker forces every caller to handle it; adding a variant **breaks the build** at every non-exhaustive call site |
| genuinely exceptional, unrecoverable at this layer, or a **programmer error** | **`raise`** | the caller cannot usefully be forced to handle it |
| a fault you deliberately absorb and record | **absorb-and-mark** | the value carries the degradation forward |

Close every union with `case _: assert_never(x)`. Without it, adding a variant is silent — which
forfeits the only reason to choose this channel.

## Do

1. **One project base exception, then specific subclasses.** Never raise the base directly — it defeats
   narrow catching.
2. **Structured attributes, not parsed strings.** A stable error code, the offending value, and the
   remediation as fields. A message is for humans; attributes are the contract.
3. **Wrap at every boundary: `raise Domain(...) from low`.** `__cause__` (explicit `from`) and
   `__context__` (implicit, during handling) render differently — know which you are setting. Use
   `from None` only when you can state why deleting the cause helps.
4. **Catch narrowly, and use `else`.** Put only the line that can fail inside `try`; the success path
   goes in `else`, so you cannot accidentally catch an exception from it.
5. **Parse at the boundary.** One function per external shape, returning your own typed value or your own
   error. Convert the validation library's error into your taxonomy *there* — never let its exception
   type become your public contract.
6. **Errors are a versioned public contract.** Document which errors a function raises or returns.
   Removing or renaming one is a breaking change and needs the deprecation window
   (`python_module_boundaries_manifest.md` §9.3).
7. **Install the unhandled-exception hooks you actually need.** There are four —
   `sys.excepthook`, `threading.excepthook`, `sys.unraisablehook`, and the asyncio loop handler — and
   installing one does **not** cover the others. A project that sets `sys.excepthook` and believes it is
   covered is a real, common failure.
8. **Preserve traceback quality.** Fine-grained error locations (PEP 657) are a diagnosis asset; know
   which flags erase them before you set them. → error-tracing §12–§13

## Never

- **`assert` as enforcement.** Stripped under `-O`. Assertions are for programmer-believed invariants
  whose violation means a bug — and even then, audit every one before enabling `-O`. Because `S101` is
  enforced in `src`, a legitimate internal-invariant assert carries a per-site
  `# noqa: S101  # internal invariant` — never a global ignore.
- **Bare `except`, `except BaseException`, or catch-and-ignore.** Suppress explicitly and narrowly with
  `contextlib.suppress`.
- **`except Exception` where cancellation must pass through.** `CancelledError` derives from
  `BaseException` precisely so that `except Exception` does not eat it.
- **`return`/`break`/`continue` out of a `finally`** — it discards the in-flight exception.
- **Retrofitting `ExceptionGroup`/`except*` onto an existing single-exception API.** Introduce a new API.
- **Leaking a library's exception type across your API.**

## `except*` — rules, not style

- A handler receives a **subgroup**, never a bare exception; write it to handle a group.
- You cannot mix `except*` and plain `except` in one `try`.
- Leftover exceptions propagate as a group — do not assume your handler consumed everything.
- `TaskGroup` failures arrive as an `ExceptionGroup`, so async code meets this whether you chose it or
  not. → `cards/concurrency.md`

## Reporting many failures — pick one deliberately

**First-error result** (cheapest, loses information) · **in-band Notification** (collects all, stays a
value — right for form and config validation) · **raised `ExceptionGroup`** (right for concurrent
failure). → error-tracing §18

## Resilience mechanisms — check the scale before importing

`timeout` and **bounded** retry with backoff **and jitter** are appropriate almost everywhere. A
**circuit breaker, bulkhead, supervision tree, dead-letter queue or retry budget in a single-process
application is distributed-systems machinery at the wrong scale** — it adds failure modes it cannot pay
for. The manifest gates each one explicitly; read the gate, not just the name. → error-tracing §8

## Decisions you must not invent

The result/raise seam — exactly where conversion happens · the error-code scheme and whether it is part
of the public contract · hand-rolled union vs a `Result` library · whether `-O` is ever used in
production · which of the four hooks are installed and what each does.

## Go deeper

| question | where |
|---|---|
| the two channels and three dispositions, argued | error-tracing §3 |
| exhaustiveness, `Never`, `assert_never` | error-tracing §5, typing §2 |
| composing result-returning steps without a monad stack | error-tracing §4a |
| chaining, `__cause__` vs `__context__`, traceback rendering | error-tracing §8–§9 |
| validation placement policies, and the parse-function contract | error-tracing §15 |
| async failure surfaces: cancellation, never-retrieved | error-tracing §18a, concurrency card |
| testing the error contract | `cards/write-tests.md` |
