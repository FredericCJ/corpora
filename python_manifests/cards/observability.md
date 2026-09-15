# Card: logging, metrics and traces

**Load when:** adding logging, choosing a severity, wiring structured output, or considering telemetry.
**Depth:** `reference/logging_observability_manifest.md`. Live-process diagnosis is
`cards/diagnose-runtime.md`; error-side obligations are `cards/handle-errors.md`.

## The load-bearing rule

**Components emit; applications route.** A reusable component that configures logging drags its policy
into every consumer, and that is the constraint most often violated.

| you are writing… | you do |
|---|---|
| a library, or any module meant to be lifted elsewhere | `logger = logging.getLogger(__name__)` at module scope, add `NullHandler` to your top-level logger, and **configure nothing** — no handlers, no levels, no `basicConfig` |
| an application entry point | configure **once**, as early as possible, and own all routing |

## Severity — five emittable levels, chosen by consequence

| level | means | who acts |
|---|---|---|
| `DEBUG` | developer tracing at component seams | nobody, until debugging |
| `INFO` | a normal, notable event completed | nobody; it is the narrative |
| `WARNING` | something degraded or deprecated; the operation continued | someone, eventually |
| `ERROR` | an operation failed; the process continues | someone, now |
| `CRITICAL` | the process cannot continue meaningfully | someone, immediately |

`NOTSET` is a **sentinel, not a sixth level** — it means "inherit", and treating it as a severity is a
recurring error. Choose the level by *who must act*, never by how bad it felt.

**`logging` vs the alternatives:** a message about program execution → `logging`. A message telling a
*developer* their code should change → `warnings.warn`. Program output that is the point of the program →
`print`/stdout. Those three are not interchangeable.

## Do

1. **Lazy `%`-style arguments**: `logger.info("loaded %s in %dms", name, ms)`. An f-string formats even
   when the level is disabled and destroys the ability to aggregate by message. Route: `lint-catchable`
   `G001`–`G004` — **off by default**, so select them.
2. **`logger.exception()` inside the handler**, never `logger.error(str(e))` — the traceback is the
   artefact. Route: `TRY400`. And `.exception()` **outside** an `except` block attaches `None` as the
   exception (`LOG004` — stabilised but *not* default-enabled).
3. **Log once, at the handling boundary.** Not at every frame on the way up.
4. **Structured fields, not interpolated prose.** `extra={...}` with a stable key set, or a structured
   logging pipeline. A log line is a record with fields, and the message is one of them.
5. **Correlate.** One id per unit of work, carried in a `contextvars` context and attached by a `Filter`.
   Know the boundaries: a Task **copies** the context at creation; threads do not inherit it.
6. **Keep hot paths off the I/O path** with a queue handler — and know that **every default in that
   mechanism surprises people**: the record-preparation step is destructive, handler levels are not
   respected by default, the enqueue path can drop, and the listener must be explicitly stopped.
   → observability §9a
7. **Every accumulator needs a purge.** Rotation for files, bounds for caches, cleanup for temp files. An
   unbounded log is a disk outage with a delay.

## Never

- **A secret, credential, token, key or PII in a log line** — including inside an exception message, a
  `repr`, or a serialised request body. Redact in a **`Filter` at the logger**, not in the formatter: the
  formatter runs too late and only covers the handlers that use it. Cover `record.args` and `exc_text`
  too, and place the filter **upstream of any queue handler**.
- **`print()` for diagnostics.** Route: `T201`.
- **A library calling `basicConfig`, adding a handler, or setting a level.**
- **`logger.error()` in an `except` block** where `logger.exception()` is meant.
- **Log-and-rethrow at every level.**
- **Trusting log injection to be someone else's problem** — a newline in user input forges a log record.

## Choosing the signal

A **log** is one event with context, for reading. A **metric** is an aggregate, for alerting and trend.
A **trace** is a causal path across boundaries, for latency attribution. Emitting a log line per request
to count requests is the most common mis-choice: that is a metric. → observability §8c

## Before adopting OpenTelemetry

The distinction the manifest insists on: **spec-stable is not implementation-stable.** Check the
*Python* implementation's status for the **logs** signal specifically — traces and metrics being stable
tells you nothing about it — and pin deliberately. The severity-number mapping and which values are
*fields* rather than attributes are exact and easy to get wrong. If the logs path is not stable, emit
structured stdlib logging behind your own seam and adopt later; that is a supported position, not a
compromise. → observability §8b

## Decisions you must not invent

Whether output is JSON or human-readable, and per environment · the stable field set and its owner ·
what the correlation id is and where it enters · whether telemetry is adopted at all, and pinned how ·
the redaction list · retention and rotation · which of `LOG004`/`LOG007`/`LOG014` are enforced as errors,
given where this codebase draws its log-once boundary.

## Go deeper

| question | where |
|---|---|
| the severity model and the print/`warnings`/`logging` decision table | observability §2 |
| logger hierarchy, propagation, effective level | observability §3a |
| library discipline in full — the `NullHandler` contract | observability §4 |
| application-side configuration | observability §5 |
| structured and contextual logging | observability §7 |
| correlation, `contextvars`, tasks and threads | observability §8 |
| queue handoff and its four biting defaults | observability §9a |
| redaction placement, and log injection as a separate obligation | observability §11 |
| an audit log is not an application log | observability §11a |
