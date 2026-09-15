# Card: diagnose a running or crashed process

**Load when:** something is hung, crashed, leaking, slow, or producing a wrong answer in an environment
you cannot simply re-run under a debugger.
**Depth:** `reference/python_runtime_diagnostics_manifest.md`. Logs and telemetry are
`cards/observability.md`; the error *contract* is `cards/handle-errors.md`.

## The standard this card serves

**A system is diagnosable when a failure can be explained from artefacts alone — no rerun, no code
change.** Everything below is either an instrument for reading a live process, or a design move that
makes the artefacts sufficient.

## Symptom → instrument

| symptom | first move |
|---|---|
| **hung / wedged** | get a stack without restarting: `python -m pdb -p PID`, an out-of-process sampler, or `faulthandler`'s timeout watchdog if it was armed |
| **crashed hard** (segfault, fatal error) | `faulthandler` output; a core file plus `py-bt`; `gdb -p` as the last resort |
| **crashed with a traceback** | the traceback *is* the artefact — check nothing erased its fine-grained locations; post-mortem with `pdb.post_mortem()` / `sys.last_exc` |
| **leaking memory** | `tracemalloc` snapshot diff to attribute to a call site; `gc` introspection for cycles; `memray` for the allocation tree |
| **slow** | a **statistical** sampler first (cheap, production-safe), a deterministic profiler only when you already know where to look |
| **wrong answer, not reproducible** | stop debugging and fix the artefacts — see "design for diagnosis" below |

## Attach instead of restarting

PEP 768 (3.14) makes attaching to a live process safe and free when idle:

- **Operator entry point:** `python -m pdb -p PID`.
- **API:** `sys.remote_exec(pid, script)` — `script` is a **path to a file**, not a source string. It
  returns immediately; the target runs it at its next safe point.
- **Disabled by** `PYTHON_DISABLE_REMOTE_DEBUG` (**any** value, *including empty*),
  `-X disable-remote-debug`, or a build configured `--without-remote-debug`.

Two traps worth knowing before an incident: **a hung target makes attach look identical to a hang** — the
command simply waits; and **disabling remote debug in a hardened image silently removes `pdb -p` and
sampler attach**, which is a decision to take deliberately, not a default to inherit.

## Instruments, and what each costs

- **`sys.monitoring`** (PEP 669) is the modern instrumentation substrate: per-event enable/disable, so
  you pay only for events you want. It replaces `settrace`/`setprofile` for anything performance-
  sensitive, and coverage tooling now builds on it. The tool-id budget is small — check before claiming
  one.
- **`faulthandler`** — arm it in the entry point. Enables a Python traceback on fatal errors, and a
  timeout mode that dumps every thread's stack after N seconds, which is how you catch a deadlock that
  only happens in production.
- **`tracemalloc`** — snapshot, diff, attribute. The overhead is real, so gate it behind a switch.
- **Profilers.** The reorganisation matters: `profiling.tracing` is the deterministic profiler
  (`cProfile` is now an alias), and `profiling.sampling` is a statistical sampler with `--pstats`,
  `--collapsed`, `--flamegraph`, `--gecko`, `--heatmap` and `--live` outputs. The old `profile` module is
  deprecated. **Version-gate all of this against hub §4a** — and know that external samplers state their
  own interpreter support (py-spy, for instance, does not claim the newest release).
- **When each profiler lies:** a deterministic profiler's overhead distorts the thing it measures; a
  sampler is blind between samples; native frames are missing without the `perf` trampoline. Never draw
  a conclusion from a sampler's blind spot.

## Development-time switches

`-X dev` / `PYTHONDEVMODE` turns on a set of checks you want in test runs and never in production —
**and it is required, alongside `filterwarnings`, for `ResourceWarning` to surface at all**.
`-X importtime` for slow startup. `-W error` to make a warning fail. The full switchboard is a **hub**
fact (§6), catalogued once there rather than duplicated here.

## Design for diagnosis — do this before you need it

The instruments above only help if the process was built to be read:

1. **Built-in self-test at startup** — validate configuration, connectivity and invariants, and refuse to
   start on failure with a **distinct exit code**. A process that starts broken is the expensive case.
2. **A separable maintenance/introspection surface** — health, version, build variant, current
   configuration — kept behind its own seam so it can be removed or restricted without touching logic.
3. **Sanity checks that survive `-O`.** An `assert` does not. If the check must hold in production, it is
   an `if` and a `raise`.
4. **Liveness**: a local heartbeat or watchdog for hang detection.
5. **Every artefact carries its provenance**: interpreter version, **build variant** (free-threaded? JIT?
   tail-call?), the flags in force, the seed, and the correlation id. A performance claim or crash report
   without the build variant is not evidence — and under a JIT or tail-call build, some observations
   become unreliable.
6. **Reproducibility from artefacts alone** — record enough at the shell boundary that a field failure
   replays. This is what closes "not reproducible".

## Never

- **Print-debugging as the primary instrument.** It changes timing, ships by accident, and answers one
  question. Route: `lint-catchable` `T201`.
- **Profile a debug build**, or compare a measurement across build variants.
- **Leave a tracer, profiler or `tracemalloc` enabled in production** because it was useful once.
- **Catch-log-rethrow at every level** to "get more diagnostics". It produces N copies of one event and
  buries the handling boundary.
- **Claim a leak from one snapshot.** Diff two.
- **Treat audit hooks as a sandbox.** They observe; they do not contain.

## Decisions you must not invent

Whether remote debugging stays enabled in production images · whether `faulthandler` is armed at start
and with what timeout · which diagnostic surfaces exist and who may reach them · where the build-variant
stamp is recorded, and what rejects an artefact lacking it · whether long-running processes get
rejuvenation or a safe-state fallback.

## Go deeper

| question | where |
|---|---|
| the attach interface in full, including what it does not do | diagnostics §2 |
| `sys.monitoring` events and the tool-id budget | diagnostics §3 |
| hang and crash capture, core files, `gdb` | diagnostics §4 |
| memory attribution | diagnostics §5 |
| profiling, and precisely when each profiler lies | diagnostics §6 |
| the design-for-diagnosis catalogue with citations | diagnostics §9–§10 |
| the `-X` / `PYTHON*` switchboard | hub §6 |
