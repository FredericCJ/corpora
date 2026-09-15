# Error handling and diagnosability - seed pack (mined 2026-08-08)

Mined from `SWE/explorer/data/elements.json` (1083 nodes / 2811 edges), `design_elements_catalog_v1_0.md`,
`architecture_elements_catalog_v1_0.md`, `design_elements_corpus_v1_0.md`, `explorer/data/corpus.json`.
Every id below was verified to exist in `elements.json`; absences are called out as findings.
Targets: `error_tracing_contract_manifest.md`, `logging_observability_manifest.md`,
NEW `python_runtime_diagnostics_manifest.md`.

**The headline.** All 50 `design/error-handling` elements were read. The two target manifests already own
the *channel* question well (raise vs typed in-band) but contain **zero** vocabulary for the other three
families: the words `timeout`, `retry`, `backoff`, `jitter`, `circuit`, `supervis`, `crash`, `watchdog`,
`heartbeat`, `self-test`, `health`, `faulthandler`, `rotat`, and `audit` do not appear in either file
(grepped 2026-08-08). The corpus supplies named, cited vocabulary for all of them.

**The 50 error-handling elements sorted into the manifest's own frame** (ids verified; `*` = proposed
import, `~` = fold, `x` = do-not-transpose):

- **RAISE-channel mechanisms** — `setjmp-longjmp-error-handling`x, `samurai-principle`~, `fail-fast`*,
  `guard-clause`~, `error-handler`~, `complete-parameter-checking`*, `copy-and-swap`x, `goto-cleanup`x,
  `cleanup-record`x, `log-errors`~, `meaningless-behavior`*, `deferred-validation`*.
- **Typed in-band result mechanisms** — `result-type`~ (the manifest's `EmitOk | EmitError`),
  `railway-oriented-programming`*, `notification`*, `exceptional-value`*, `marked-data`*,
  `return-status-code`x, `special-return-value`x, `sentinel-value`x, `correcting-audits`*.
- **Supervision / recovery topology** — `error-kernel`*, `supervisor`~, `let-it-crash`*, `escalation`*,
  `restart`~, `safe-state`*, `quarantine`*, `rollback`*, `roll-forward`*, `software-rejuvenation`*,
  `heartbeat`*, `dead-letter-channel`x(scale), `recovery-blocks`x, `n-version-programming`x.
- **Transient-fault mechanisms** — `retry-with-exponential-backoff-and-jitter`*, `retry-budget`x(scale),
  `timeout`*, `circuit-breaker`* (gated), `riding-over-transients`*, `happy-eyeballs`x(already in stdlib),
  `leaky-bucket-counter`*, `loop-timeout`x.
- **Diagnosability** — `diagnostic-context`~, `diagnostic-logger`~, `log-errors`~, `core-dump`*,
  `built-in-self-test`*, `heartbeat`*, `stack-painting-watermarking`x, `cyclic-redundancy-check`x.
- **Embedded/hardware only** — `brown-out-handling`x, plus the C-idiom cluster already listed above.

## Import table

| element id | realm/kind | catalog name | named-in (citable) | Python instantiation | destination manifest + section |
|---|---|---|---|---|---|
| `timeout` | design/error-handling | Timeout | Nygard, *Release It!* 2nd ed. (2018) — corpus record **UNVERIFIED** | Every blocking call takes a bound: `requests.get(..., timeout=(connect, read))` (requests has **no** default timeout), `httpx.Timeout`, `socket.settimeout`, `subprocess.run(timeout=)`, `asyncio.timeout()` (3.11+) / `asyncio.wait_for`, `Future.result(timeout=)`, `threading.Event.wait(timeout=)`, `queue.get(timeout=)`, driver-level `connect_timeout`/`statement_timeout` | `error_tracing_contract_manifest.md` §NEW "Transient-fault mechanisms" — the highest-value single import in this slice |
| `retry-with-exponential-backoff-and-jitter` | design/error-handling | Retry with Exponential Backoff and Jitter | Brooker, *Timeouts, Retries, and Backoff with Jitter*, Amazon Builders' Library — **UNVERIFIED**; Beyer et al., *SRE* (2016, verified) | `tenacity` `@retry(stop=stop_after_attempt(n), wait=wait_exponential_jitter())`; `urllib3.util.Retry(total=, backoff_factor=, backoff_jitter=)` behind `HTTPAdapter`; or ~12 lines with `random.uniform`. Precondition: the operation must be idempotent (see Relations #15) | `error_tracing_contract_manifest.md` §NEW "Transient-fault mechanisms" |
| `riding-over-transients` | design/error-handling | Riding Over Transients | Hanmer, *Patterns for Fault Tolerant Software* — **UNVERIFIED** | Do not act on the first failure; act when failures *persist*. Concretely: the decaying counter below gates escalation, and the first N failures log at DEBUG/INFO only | `error_tracing_contract_manifest.md` §NEW "Transient-fault mechanisms" |
| `leaky-bucket-counter` | design/error-handling | Leaky Bucket Counter | Hanmer — **UNVERIFIED** | ~10 lines, no dependency: `score += 1` on error, `score -= (now - last) * leak_rate` on read via `time.monotonic()`; trip at a threshold. Encodes an acceptable *rate*, not a count | `error_tracing_contract_manifest.md` §NEW "Transient-fault mechanisms" |
| `circuit-breaker` | design/error-handling | Circuit Breaker | Nygard (2018) — **UNVERIFIED**; Kuhn/Hanafee/Allen, *Reactive Design Patterns* (2017, verified) | `pybreaker`, or a 3-state class (closed/open/half-open) over the leaky-bucket counter. **Gate:** import the *name*, adopt the mechanism only when the same dependency is called repeatedly in a loop and failing fast beats waiting. A one-shot CLI invocation needs `timeout` + bounded retry, not a breaker | `error_tracing_contract_manifest.md` §NEW "Transient-fault mechanisms" (with the gate stated inline) |
| `fail-fast` | design/error-handling | Fail Fast | Nygard (2018) — **UNVERIFIED** | Startup preflight in `__main__` before any work: validate config, resolve paths, probe dependency reachability with a short timeout, then run. "Report failure immediately, rather than doing work that is doomed to fail slowly" | `error_tracing_contract_manifest.md` §7 / §15 |
| `safe-state` | design/error-handling | Safe State | ISO 26262:2018, *Road vehicles — Functional safety* (verified) | A *named, reachable* state entered on fault detection: refuse to start on bad config with a distinct exit code (`os.EX_CONFIG`), flip to read-only, disable the failing feature flag, park background workers, cooperative shutdown for threads. Not "an unhandled traceback" | `python_runtime_diagnostics_manifest.md` §"Failure disposition"; cross-ref `error_tracing_contract_manifest.md` §7 |
| `let-it-crash` | design/error-handling | Let It Crash | Nygard (2018) — **UNVERIFIED**; Candea & Fox, *Crash-Only Software* (2003, verified); Kuhn et al. (2017, verified) | Do **not** write `except Exception:` recovery for unanticipated errors. Let it propagate, exit non-zero, and let the **external** restarter recreate the process: systemd `Restart=on-failure`, a container restart policy, gunicorn/uvicorn worker recycling. Do **not** hand-roll a supervisor tree | `error_tracing_contract_manifest.md` §NEW "Failure disposition & recovery topology" |
| `error-kernel` | design/error-handling | Error Kernel | Kuhn, Hanafee & Allen, *Reactive Design Patterns* (2017, verified) | The failure-containment reading of functional-core/imperative-shell: irreplaceable state lives in the pure core that does no I/O; risky work runs in an expendable unit that may die — a `ProcessPoolExecutor` worker, a subprocess, a task whose exception is confined. "Keep the irreplaceable state … in a small, maximally simple core, delegating risky or failure-prone work to expendable child components" | `error_tracing_contract_manifest.md` §6 (names the *why* behind the seam) |
| `escalation` | design/error-handling | Escalation | Hanmer — **UNVERIFIED**; Preschern, *Fluent C* (2022, verified) for the ladder | Write the ladder down: retry the call → reset the client / reopen the connection → re-exec (`os.execv`) or exit non-zero → let the process manager restart. "An ordered ladder bounds recovery time while preferring the least disruptive action that works" | `error_tracing_contract_manifest.md` §NEW "Failure disposition & recovery topology" |
| `rollback` | design/error-handling | Rollback (backward error recovery) | Hanmer — **UNVERIFIED**; BCK 4th ed. (2021, verified) for the tactic twin | DB transaction (`with conn:`), `contextlib.ExitStack.callback` compensations, write-temp-then-`os.replace` for atomic publish | `error_tracing_contract_manifest.md` §NEW "Failure disposition & recovery topology" |
| `roll-forward` | design/error-handling | Roll-Forward (forward error recovery) | Hanmer — **UNVERIFIED** | Skip the bad record, advance the offset/cursor, record the rejection, keep going. "Rolling back can be impossible … moving forward to the next safe state keeps the system live" | `error_tracing_contract_manifest.md` §NEW "Failure disposition & recovery topology" |
| `marked-data` | design/error-handling | Marked Data | Hanmer — **UNVERIFIED** | The rejects sink: a `Rejected` variant in the output union, an `errors` column, a sibling `rejects.jsonl`. "Deleting bad data may be worse than keeping it; an explicit corruption mark contains the error while preserving structure and audit trail" | `error_tracing_contract_manifest.md` §NEW "Failure disposition & recovery topology" (the file/batch answer where a broker DLQ is over-scale) |
| `quarantine` | design/error-handling | Quarantine | Hanmer — **UNVERIFIED** | After N failures (leaky-bucket gated) disable the plugin/endpoint/worker and keep serving the rest: mark a failed `importlib.metadata` entry point as skipped, stop scheduling a task, route its inputs to the rejects sink | `python_runtime_diagnostics_manifest.md` §"Failure disposition" |
| `railway-oriented-programming` | design/error-handling | Railway-Oriented Programming | Wlaschin, *Railway Oriented Programming* (2014, verified) | The composition rule the manifest's `EmitOk \| EmitError` lacks: one `bind`/`then` helper plus early return over a list of steps, or `returns` (`Result`, `flow`, `bind`). Honest caveat: Python has no do-notation, so a deep monadic chain reads worse than an explicit early-return pipeline — import the *discipline*, not a monad stack | `error_tracing_contract_manifest.md` §4 (new subsection: composing result-returning steps) |
| `notification` | design/error-handling | Notification | Fowler, *eaaDev* (verified, living) | The in-band aggregate: a frozen `Notification(errors: tuple[Err, ...])` returned from validators; `pydantic.ValidationError.errors()` **is** a notification. "An object that accumulates errors … instead of throwing on first failure" | `error_tracing_contract_manifest.md` §18 (as the in-band peer of `ExceptionGroup`) |
| `exceptional-value` | design/error-handling | Exceptional Value | Cunningham, *The CHECKS Pattern Language of Information Integrity* (PLoP 1994, verified) | A frozen `Invalid(raw=..., reason=...)` / `Missing` singleton that flows through the domain and is rejected at the output boundary; `decimal.Decimal("NaN")` and `pandas.NA` are instances of the idea. Names the *third disposition*: absorb, rather than raise or short-circuit | `error_tracing_contract_manifest.md` §3 (widen the frame) |
| `meaningless-behavior` | design/error-handling | Meaningless Behavior | Cunningham (1994, verified) | The citable justification for EAFP at domain altitude: write domain functions with **no** defensive `is None`/`isinstance` guards, let the computation fail, recover at the shell/presentation boundary | `error_tracing_contract_manifest.md` §13 (gives EAFP a design rationale, not just an idiom label) |
| `complete-parameter-checking` | design/error-handling | Complete Parameter Checking | Hanmer — **UNVERIFIED** | `pydantic` / `TypeAdapter.validate_python` at *every* public entry point, every time. This is what "parse, don't validate" is, named — including the cost the source states: "at the cost of some performance" | `error_tracing_contract_manifest.md` §15 (name the policy the manifest already chose) |
| `deferred-validation` | design/error-handling | Deferred Validation | Cunningham (1994, verified) | An all-optional `Draft` model for in-progress data plus `Model.model_validate()` only at save/commit; `model_construct()` to skip validation deliberately. "Scaling the rigor of the check to the consequences of that action" | `error_tracing_contract_manifest.md` §15 (the opposite pole; see the `alternative-to` edge) |
| `correcting-audits` | design/error-handling | Correcting Audits | Hanmer — **UNVERIFIED** | An `app verify [--repair]` command that scans persisted state for structural violations (orphan rows, missing blobs, checksum mismatch) and repairs or reports | `python_runtime_diagnostics_manifest.md` §"Self-checking surfaces" |
| `built-in-self-test` | design/error-handling | Built-In Self-Test | **Corpus `named_in` is a Wikipedia page** — cite the covering work instead: IEC 61508-7:2010 technique catalog (verified) | `selfcheck()` behind `app --self-test`: dependency/version consistency (`importlib.metadata.version`), checksum bundled data (`hashlib.file_digest`, 3.11+), round-trip the serializers, ping each dependency with a short timeout, assert the migration head. Fast form at startup, full form on demand | `python_runtime_diagnostics_manifest.md` — **organizing element** for §"Self-checking surfaces" |
| `core-dump` | design/error-handling | Core Dump | **Corpus `named_in` is the bare work id `white` (data defect)** — covering works: White, *Making Embedded Systems* 2nd ed. (2024, verified); FSF, *Debugging with GDB* 10th ed. (verified) | `faulthandler.enable()` / `PYTHONFAULTHANDLER=1` (C+Python traceback on SIGSEGV/SIGABRT); `faulthandler.dump_traceback_later(t, exit=True)` for hangs; `faulthandler.register(signal.SIGUSR1)` for on-demand dumps; `sys.excepthook` / `threading.excepthook` writing a sanitized crash report (traceback + `tracemalloc` snapshot + context); `pdb.post_mortem()`; real core files + gdb `py-bt` | `python_runtime_diagnostics_manifest.md` — **organizing element** for §"Post-mortem capture" |
| `maintenance-interface` | architecture/pattern | Maintenance Interface | Hanmer — **UNVERIFIED** | A control channel distinct from the service interface: a loopback Unix-domain socket / `aiomonitor`-style REPL, an `admin` CLI subcommand group, or `SIGUSR1` → dump state. "Mixing management traffic with application traffic obscures both and blocks maintenance exactly when the service path is congested or broken" | `python_runtime_diagnostics_manifest.md` — **organizing element** for §"The diagnostic surface" |
| `specialized-interfaces` | architecture/tactic | Specialized Interfaces | Bass, Clements & Kazman, *SAiP* 4th ed. (2021, verified) | Explicit `dump_state()` / `reset()` / `set_verbosity()` plus `--dump-state` flags, kept in one separated module (`_diagnostics.py`) so they can be reviewed or removed — not scattered `print`s. The tactic's own words: "clearly separated from functional interfaces so they can be removed" | `python_runtime_diagnostics_manifest.md` §"The diagnostic surface" |
| `record-playback` | architecture/tactic | Record/Playback | BCK 4th ed. (2021, verified) | Capture inputs at the shell boundary (`--record`) and replay them (`--replay`); `vcrpy`/`responses` for HTTP; promote the captured payload into a pytest regression fixture. "Record information as it crosses interfaces and use the recorded state to 'play the system back'" | `python_runtime_diagnostics_manifest.md` §"Reproducing a field failure" |
| `heartbeat` | design/error-handling | Heartbeat | Hanmer — **UNVERIFIED**; BCK 4th ed. (2021, verified) for the `heartbeat-tactic` twin | systemd `Type=notify` + `WatchdogSec` with `sd_notify("WATCHDOG=1")`; or a supervisor thread checking a `last_progress = time.monotonic()` stamp written by the worker loop; or re-arming `faulthandler.dump_traceback_later` each iteration as a hang detector. **Not** ping/echo across nodes | `python_runtime_diagnostics_manifest.md` §"Liveness" |
| `sanity-check` | design/robustness-security | Sanity Check | Douglass, *Real-Time Design Patterns* (verified, author corpus) | A plausibility check on computed output that **survives `-O`**: `if not (0.0 <= p <= 1.0): raise ImplausibleResult(...)`, counted and logged at WARNING. Distinct from `assert`. "Full result verification is often infeasible, but gross faults are cheap to catch" | `python_runtime_diagnostics_manifest.md` §"Self-checking surfaces"; cross-ref `error_tracing_contract_manifest.md` §14 |
| `software-rejuvenation` | design/error-handling | Software Rejuvenation | Huang, Kintala, Kolettis & Fulton (1995) — **UNVERIFIED**; BCK `removal-from-service` (2021, verified) is the standards-grade twin | gunicorn/uvicorn `--max-requests` + `--max-requests-jitter`, systemd `RuntimeMaxSec=`, a scheduled restart. State it as what it is: a **concession** to a leak you have not found, paired with `steady-state` | `python_runtime_diagnostics_manifest.md` §"Long-running processes" |
| `steady-state` | design/resource-management | Steady State | Nygard (2018) — **UNVERIFIED** | For every accumulator, a purge: `logging.handlers.RotatingFileHandler` / `TimedRotatingFileHandler` (or `logrotate`), `functools.lru_cache(maxsize=)` never unbounded, `tempfile.TemporaryDirectory` as a context manager. **The logging manifest configures file handlers but never mentions rotation** — this closes that hole | `logging_observability_manifest.md` §5 (application-side configuration) |
| `audit-log` | design/robustness-security | Audit Log | Fowler, *eaaDev* (verified) is the only work in the corpus record; the `named_in` prose additionally names Core Security Patterns (2005) and Schneier & Kelsey (1999) with **no backing work records** | A separate `audit` logger with its own handler and a schema'd record (actor, action, target, time, source), append-only, **not** level-suppressible, distinct from the debug/app logger. "Ordinary debug logging is neither complete, attributable, nor protected against tampering" | `logging_observability_manifest.md` §NEW "An audit log is not an application log" |

## Fold table

| element id | catalog name | the manifest already calls this | note |
|---|---|---|---|
| `result-type` | Result Type | `error_tracing` §3–§4 "in-band typed value", `EmitOk \| EmitError` | Exact match. Import the **citation** the manifest lacks: Douglas, *P1028 SG14 status_code and standard error object* (WG21, 2020, verified) and Wlaschin (2014). The manifest presents the union encoding with python.org typing cites only |
| `tagged-union` | Tagged Union | §4 "tagged/discriminated union" | `result-type -specializes-> tagged-union`; the manifest already uses the word |
| `option-type` | Option Type | `T \| None` absence handling | Fold, but state the sourced distinction (Relations #4): Option signals absence *with no reason*, Result carries the reason |
| `functional-core-imperative-shell` | Functional Core, Imperative Shell | §6, the whole seam section | **The manifest tags this OPEN — "no single primary source prescribes the seam" — but the corpus records a naming work: Bernhardt, Destroy All Software (2012, verified).** The *pattern* is citable; only the *seam placement* is genuinely OPEN. Split the tag |
| `exception-handling` (tactic) | Exception Handling | §3 raise channel + §11 hierarchy | BCK: "mechanisms ranging from function return codes to exception classes carrying name, origin, and cause" — the arch-altitude statement that return codes and exception classes are one family |
| `exception-detection` (tactic) | Exception Detection | §12 / §15 boundary checks | BCK refines it into system exceptions, parameter fence, parameter typing, timeout |
| `exception-prevention` (tactic) | Exception Prevention | §15 "make illegal states unrepresentable" | Fold with synonym; `exceptional-value -realizes-> exception-prevention` and `steady-state -realizes-> exception-prevention` |
| `executable-assertions` (tactic) | Executable Assertions | §14 assertions | Fold with synonym — but note BCK files it under **observability**, not correctness (REFINE #6) |
| `design-by-contract` | Design by Contract | §14 "pre/post-conditions" | Import the citation: Meyer, *Object-Oriented Software Construction*. **Discrepancy:** element `named_in` says 1988 (1st ed.); the corpus work record is the 2nd ed., 1997 |
| `samurai-principle` | Samurai Principle | §7 "unrecoverable at this layer / programmer error → raise" | Preschern's name — "return victorious or not at all". Fold the mechanism, import the name |
| `error-handler` | Error Handler | §6 shell owns conversion; §20 shell owns logging | Hanmer's name for concentrating error processing outside mainline flow |
| `guard-clause` | Guard Clause | §12 "keep the protected region minimal" (adjacent, not identical) | Statement-level shape; the corpus flags it `borderline` as below design altitude. Route to `python_linting_practices_manifest.md`, not here |
| `diagnostic-logger` | Diagnostic Logger | `logging` §3 Logger / Handler / Formatter / Filter | Exact match. Import the naming work: Harrison, "Patterns for Logging Diagnostic Messages", *PLoPD3* (1997, verified) — the manifest cites only python.org |
| `diagnostic-context` | Diagnostic Context (MDC/NDC) | `logging` §7 contextual logging + §8 `contextvars` Filter / `structlog.contextvars` | Exact match; the manifest's mechanism is right but **unnamed**. MDC/NDC is the industry name, Harrison/PLoPD3 the citation |
| `correlation-identifier` | Correlation Identifier | `logging` §8 correlation / trace IDs | Hohpe & Woolf (2003, verified). `diagnostic-context -composes-with-> correlation-identifier` |
| `supervisor`, `supervision-tree-otp`, `restart`, `monitor` (tactic) | Supervisor / Supervision Tree / Restart / Monitor | absent from both manifests — correctly so | These are the **process manager**, not app code: systemd, the container orchestrator, the WSGI worker manager. Fold them into `let-it-crash`'s "who restarts you" clause; do not build them |
| `crash-only-software` | Crash-Only Software | — | The architecture-altitude form of `let-it-crash`; cite Candea & Fox (2003, verified) alongside it |
| `timeout-tactic`, `heartbeat-tactic`, `rollback-tactic`, `retry` (tactics) | same names | — | Same-name two-realm twins of the design elements; cite BCK 4th ed. for the tactic form when a textbook is wanted over a practitioner source |
| `checkpointing` | Checkpointing | — | `rollback -uses-> checkpointing`; fold into `rollback`'s Python instantiation |
| `two-phase-termination` | Two-Phase Termination | — | Grand, *Patterns in Java* v1 (1998, verified). Fold into `safe-state`: the cooperative-shutdown protocol (a `threading.Event` observed at safe points) is *how* a Python worker reaches its safe state |
| `abort`, `degradation` (tactics) | Abort / Degradation | — | Fold into `safe-state`: `abort` = terminate before damage; `degradation` = "maintain the most critical system functions while dropping … less critical ones". The BCK-cited vocabulary for safe-state's two flavours |
| `sentinel-value` | Sentinel Value | — | `None` / a module-private `object()` / `Ellipsis` are legitimate for **absence**; using them for **failure** is the anti-pattern. Fold as a caution in §22 |
| `dead-letter-channel` | Dead Letter Channel | — | The broker form of `marked-data`. Import `marked-data`; keep DLQ as the name used only once a real queue exists |

## Relations worth stating

Edges taken verbatim from `elements.json`. `[S]` = `provenance: sourced`, `[E]` = `editorial`.

1. `return-status-code -alternative-to-> result-type` **[E]** — *"Numeric/enum status plus out-params vs a
   typed success/error sum in the function signature."* The manifest's §3 choice as a graph fact.
2. `notification -alternative-to-> result-type` **[E]** — *"Gather all errors before returning vs
   short-circuiting on the first error value."* **This is the rule §18 is missing:** batch/field validation
   wants the aggregate, not the first-failure short-circuit — and it wants it *in-band*.
3. `railway-oriented-programming -composes-with-> result-type` **[S]** cite: Wlaschin — *"ROP is defined as
   composition over result types."* You cannot import Result and skip the composition discipline.
4. `result-type -alternative-to-> option-type` **[E]** — *"Result carries an error value where Option only
   signals presence/absence with no reason."* The decision rule for `T | None` vs `Ok | Err`.
5. `deferred-validation -alternative-to-> complete-parameter-checking` **[E]** — *"Opposite
   validation-placement policies: check everything at every boundary vs delay comprehensive checking until
   use."* §15 must say which pole it picks.
6. `exceptional-value -composes-with-> meaningless-behavior` **[S]** cite: Cunningham, CHECKS —
   *"Meaningless Behavior operates over Exceptional Values, rejecting meaningless results at output."* The
   two are defined in terms of each other: you may not adopt "no defensive checks" without a value that can
   carry the badness.
7. `exceptional-value -specializes-> special-case` **[S]** cite: Fowler, PoEAA 'Special Case'; Cunningham
   'Exceptional Value'. Ties CHECKS vocabulary to Null Object / Special Case the manifest can already reach.
8. `exceptional-value -realizes-> exception-prevention` **[E]** — the absorbing value *prevents the
   exception arising*, which is why it is a third disposition and not a variant of raise.
9. `return-status-code -alternative-to-> samurai-principle` **[S]** cite: Preschern, *Fluent C* — *"Return an
   error the caller can handle vs assert/abort when it cannot be meaningfully handled."* The sourced form of
   §7's decision rule.
10. `log-errors -alternative-to-> return-status-code` **[S]** cite: Preschern — *"Log at the point of error
    rather than forcing all debug info back through return values."* In tension with `logging` §10; see
    REFINE #1.
11. `diagnostic-context -composes-with-> diagnostic-logger` **[S]** cite: log4j/SLF4J MDC — *"The logger
    auto-appends the thread-bound context stash to every message emitted in scope."* The
    Filter-stamps-contextvars mechanism, named.
12. `diagnostic-context -enables-> log-aggregation` **[E]** and `-enables-> distributed-tracing` **[E]** —
    in-process correlation ids are the **precondition** for anything centralized. State the dependency so a
    small app builds the cheap half and stops there.
13. `timeout -composes-with-> circuit-breaker` **[S]** cite: Nygard — *"timeouts detect the slow failure, the
    breaker stops repeating it."*
14. `retry-with-exponential-backoff-and-jitter -composes-with-> timeout` **[S]** cite: Nygard — *"Each
    attempt is bounded by a timeout so a hung call fails and frees the retry to try again."* Retry without a
    per-attempt timeout is a hang, not a retry.
15. `retry-with-exponential-backoff-and-jitter -composes-with-> idempotent-receiver` **[S]** cite: Hohpe &
    Woolf, EIP — *"Safe automatic retry requires the receiver to tolerate duplicate delivery
    idempotently."* **Any retry guidance the manifest adds must carry this precondition.**
16. `leaky-bucket-counter -composes-with-> riding-over-transients` **[S]** cite: Hanmer — *"Riding Over
    Transients uses Leaky Bucket Counters to distinguish transient from persistent faults."* Mechanism and
    policy arrive as a pair.
17. `riding-over-transients -alternative-to-> fail-fast` **[E]** — *"Tolerate and ignore momentary
    self-clearing faults until they persist vs report failure immediately."* The sharpest tradeoff in the
    slice; a manifest naming only one pole will be misapplied.
18. `circuit-breaker -composes-with-> fail-fast` **[S]** cite: Nygard — *"An open breaker fails fast,
    rejecting calls instead of blocking on a dead dependency."*
19. `escalation -composes-with-> leaky-bucket-counter` **[S]** cite: Preschern — *"Escalate to a more drastic
    recovery only when the decaying error counter crosses its threshold."* And `escalation -uses-> restart`
    **[S]** — *"the ladder climbs from retry to restart-task/process up to reboot."*
20. `let-it-crash -composes-with-> supervisor` **[S]** cite: Armstrong — *"The philosophy presupposes the
    supervisor as the external recovery mechanism."* Recommending let-it-crash without naming the restarter
    is recommending data loss.
21. `error-kernel -composes-with-> let-it-crash` **[S]** cite: Armstrong, *Programming Erlang* — *"Let
    expendable children crash while the small, simple error kernel preserves irreplaceable state."* This is
    *where the state must live* for crashing to be cheap — the failure-side argument for
    functional-core/imperative-shell.
22. `roll-forward -alternative-to-> rollback` **[S]** cite: Hanmer — *"Forward vs backward recovery from the
    same catalog."* The two, and only two, directions after a caught failure.
23. `software-rejuvenation -alternative-to-> let-it-crash` **[E]** — *"Proactive scheduled restart before
    aging fails vs reactive crash-and-restart after failure."* And `-composes-with-> steady-state` **[S]**
    cite: Nygard.
24. `core-dump -composes-with-> let-it-crash` **[E]** — *"Capture a dump as the unit crashes, before the
    supervisor recreates it, for later diagnosis."* The reason `faulthandler` must be enabled *before*
    let-it-crash is adopted.
25. `core-dump -enables-> maintenance-interface` **[E]** — the dump is the payload the diagnostic channel
    retrieves. The edge note itself records a gap: *"missing a more specific postmortem-diagnostics arch
    element (flight recorder/black box)."*
26. `watchdog -composes-with-> sanity-check` **[E]** — *"Watchdog catches hangs (liveness); sanity check
    catches implausible outputs (correctness): complementary fault classes."* The two axes a diagnostics
    manifest must cover separately.
27. `built-in-self-test -composes-with-> safe-state` **[E]** — *"On a self-test failure the system enters its
    predefined fail-safe state instead of running."* A self-test without a defined refusal is decoration.
28. `heartbeat -uses-> timeout` **[E]** — *"Liveness is judged by a timeout window: a beat not seen before it
    expires counts as a missed beat."*
29. `watchdog -alternative-to-> heartbeat` **[S]** cite: Hanmer — *"Both detect a failed/hung component by
    missed periodic signals; watchdog is local, heartbeat is across a link."* Selects the local form for a
    single-process app.
30. `quarantine -composes-with-> restart` **[E]** — *"Fence off the faulty unit first, then restart it once
    it can no longer contaminate others."* An ordering rule an agent will otherwise get backwards.

## Do-not-transpose

**"The language already does this."**

- `setjmp-longjmp-error-handling` — Python has native `raise`/`try`/`except`; the C macro machinery has no
  analogue and no purpose.
- `goto-cleanup`, `cleanup-record` — `try/finally`, `with`, and `contextlib.ExitStack` replace both.
  `ExitStack` *is* the cleanup record: it tracks exactly what was acquired.
- `copy-and-swap` — the C++ strong-exception-guarantee problem for assignment does not exist in Python. The
  transposed intent is immutability (`dataclasses.replace`) or atomic publish (`os.replace`).
- `return-status-code`, `special-return-value` — Python has exceptions *and* typed unions; errno survives
  only as `OSError.errno`. In-band `-1`/`None`-as-error is an anti-pattern here and shadows legitimate `None`.
- `happy-eyeballs` — **already provided by the stdlib**: `asyncio` connection setup takes a
  `happy_eyeballs_delay` (and `interleave`) parameter. Pass the parameter; do not implement RFC 8305. Cite
  RFC 8305 only to explain *why* the parameter exists.
- `sentinel-value` — legitimate for absence (`None`, a module-private `object()`, `Ellipsis`), never for
  failure signalling. Not an import; a caution.

**"C / embedded / hardware concern."**

- `brown-out-handling` — supply-voltage supervision. No Python analogue at any level.
- `stack-painting-watermarking` — CPython gives the program no paintable fixed stacks. The observable
  analogues are `RecursionError`, `sys.setrecursionlimit`, `threading.stack_size`, and `faulthandler` on
  stack overflow — mention them under `core-dump`; do not import this element.
- `loop-timeout` — Python does not busy-poll hardware flags; the transposed form collapses into `timeout` on
  the blocking call, already imported.
- `cyclic-redundancy-check` — `zlib.crc32` exists, but CRC *as a RAM/ROM fault-detection tactic* is
  embedded. Use it only as the artifact-integrity step **inside** `built-in-self-test`.
- `program-sequence-monitoring` — control-flow monitoring against corrupted execution. CPython fails
  differently; an explicit state machine with illegal-transition errors is a different element, not this one.
- `guard-page`, `stack-canary`, `memory-poisoning`, `pointer-check`, `smart-data` — memory-safety mechanisms
  whose fault class CPython removes.
- `secure-zeroization` — worth one honest line elsewhere: Python cannot reliably zero a secret in memory, so
  this is **unachievable**, not unnecessary.

**"SCALE: distributed-systems machinery — over-import would be actively harmful"** (PLAN house rule 11).

- `retry-budget` — caps *aggregate* retry load as a fraction of primary requests across many clients. One
  small process cannot generate retry amplification worth budgeting. Adopt only when many instances retry
  one backend. Name it in prose as the thing you are *not* doing; do not build it.
- `dead-letter-channel` — presupposes a broker. At this scale the answer is `marked-data`: a rejects file or
  table.
- `supervisor`, `supervision-tree-otp`, `escalating-restart`, `monitor` — the restarter is systemd / the
  orchestrator / the worker manager. A hand-rolled Python supervision tree is a second, untested scheduler.
- `heartbeat` in its ping/echo form, plus `ping-echo`, `health-check-api`, `log-aggregation`,
  `distributed-tracing` — all presuppose multiple network peers. Import only the in-process precondition
  (`diagnostic-context`) and the local liveness form. Do **not** adopt OpenTelemetry for a single-process app
  (the logging manifest §8 already says this — reinforce it).
- `redundant-spare`, `replication`, `functional-redundancy`, `analytic-redundancy`, `masking`, `voting`,
  `state-resynchronization`, `shadow`, `non-stop-forwarding`, `software-upgrade` (ISSU), `reconfiguration`,
  `predictive-model` — availability tactics for redundant deployments. None apply.
- `n-version-programming`, `recovery-blocks` — require independently developed implementations plus a voter
  or acceptance test. Safety-critical process machinery, not a small-app mechanism. Nearest legitimate Python
  move: a fallback path with an explicit validity check — do not call it recovery blocks.
- `transactions` (the BCK tactic) — reads as ACID-via-two-phase-commit across distributed components. A
  single-process app wants the local DB transaction, which `rollback` already covers.

## Citable works to add to Sources

Recorded exactly as the corpus records them. **UNVERIFIED** = the corpus's own `verification` field says
`unverified`; do not present these as verified in a manifest.

- Bass, L., Clements, P. & Kazman, R. — *Software Architecture in Practice*, 4th ed., 2021. Addison-Wesley
  SEI, ISBN 978-0-13-688609-9. Verified. (exception detection/handling/prevention, monitor, self-test,
  sanity checking, timeout, heartbeat, retry, rollback, degradation, abort, removal from service, executable
  assertions, specialized interfaces, record/playback)
- Cunningham, W. — *The CHECKS Pattern Language of Information Integrity*, 1994. PLoP '94; c2.com Portland
  Pattern Repository, https://c2.com/ppr/checks.html . Verified. (exceptional value, meaningless behavior,
  deferred validation)
- Preschern, C. — *Fluent C: Principles, Practices, and Patterns*, 2022. O'Reilly, 2022-11-22,
  ISBN 978-1492097334. Verified. (log errors, return status code, special return value, samurai principle,
  the escalation ladder)
- Preschern, C. — EuroPLoP/PLoP error-handling pattern-paper series. **UNVERIFIED** — corpus note:
  *"2019-2021; exact titles/years unconfirmed."* Do not cite a specific paper title or year.
- Martin, R. C., Riehle, D. & Buschmann, F. (eds.) — *Pattern Languages of Program Design 3*, 1997.
  Addison-Wesley, ISBN 978-0-201-31011-5. Verified. Carries Harrison, "Patterns for Logging Diagnostic
  Messages" per the `diagnostic-logger` / `diagnostic-context` `named_in`.
- Wlaschin, S. — *Railway Oriented Programming*, 2014. fsharpforfunandprofit.com / NDC,
  https://fsharpforfunandprofit.com/rop/ . Verified.
- Douglas, N. (WG21) — *P1028 SG14 status_code and standard error object*, 2020 (R3). Verified. (the
  `result-type` naming record)
- Fowler, M. — *Further Enterprise Application Architecture development* (eaaDev pattern drafts), living.
  Verified. (Notification; Audit Log)
- Kuhn, R., with Hanafee, B. & Allen, J. — *Reactive Design Patterns*, 2017. Manning, ISBN 978-1-61729-180-7.
  Verified. (error kernel, let-it-crash, supervision, circuit breaker)
- Ericsson / Erlang-OTP team — *OTP Design Principles* (Erlang/OTP System Documentation), living.
  https://www.erlang.org/doc/system/design_principles.html . Verified. (supervisor, restart strategies)
- Candea, G. & Fox, A. — *Crash-Only Software*, 2003. HotOS IX (USENIX),
  https://dslab.epfl.ch/pubs/crashonly.pdf . Verified.
- Beyer, B., Jones, C., Petoff, J. & Murphy, N. R. (eds.) — *Site Reliability Engineering: How Google Runs
  Production Systems*, 2016. O'Reilly; https://sre.google/sre-book/ . Verified. (ch. 22, cascading failures
  and the retry budget)
- Bernhardt, G. — *Functional Core, Imperative Shell*, 2012. Destroy All Software screencast (Classic
  Season 4). Verified. **Use this to de-OPEN the pattern name in `error_tracing` §6.**
- Grand, M. — *Patterns in Java, Volume 1*, 1998. Verified. (two-phase termination / cooperative shutdown)
- Meyer, B. — *Object-Oriented Software Construction*, 2nd ed., 1997. Verified. **Discrepancy:** the
  `design-by-contract` element's `named_in` says 1988 (1st ed.); the work record is the 2nd ed. Pick one and
  say which.
- Hohpe, G. & Woolf, B. — *Enterprise Integration Patterns*, 2003. Verified. (correlation identifier,
  idempotent receiver, dead letter channel)
- ISO — *ISO 26262:2018, Road vehicles — Functional safety* (2nd ed., 12 parts). Verified. (safe state)
- IEC — *IEC 61508:2010, Functional safety of E/E/PE safety-related systems* (Ed. 2.0, 7 parts). Verified.
  Part 7 is the technique catalog covering self-test/BIST, program sequence monitoring, diverse/N-version
  programming, and recovery blocks.
- Douglass, B. P. — *Real-Time Design Patterns; Doing Hard Time; Real-Time UML* (author corpus,
  Addison-Wesley), living. Verified. (sanity check, watchdog)
- White, E. — *Making Embedded Systems: Design Patterns for Great Software*, 2nd ed., 2024. O'Reilly,
  ISBN 9781098151546. Verified. (core dump as a hard-fault-handler mechanism)
- Free Software Foundation — *Debugging with GDB*, Tenth Edition, living. sourceware.org/gdb. Verified.
  (core-file production and analysis)
- Koopman, P. — *Better Embedded System Software*, 2010. Drumnadrochit Press, ISBN 978-0-9844490-0-2.
  Verified. (the watchdog chapter: correct kicking discipline; what a watchdog can and cannot detect)
- Schinazi, D. & Pauly, T. — *RFC 8305: Happy Eyeballs Version 2*, 2017. IETF. Verified. (cite only to
  explain `happy_eyeballs_delay`)
- **UNVERIFIED** Hanmer, R. — *Patterns for Fault Tolerant Software*. Corpus record: year `UNRESOLVED`,
  `verification: unverified`, no identifier; the element `named_in` prose says 2007. **This is the most
  load-bearing source in the slice** — 18 elements depend on it (complete parameter checking, correcting
  audits, error handler, escalation, heartbeat, leaky bucket counter, marked data, quarantine, restart,
  riding over transients, roll-forward, rollback, maintenance interface, units of mitigation, checkpointing,
  CRC, and more). Any manifest importing from it must carry the unverified flag or re-verify first.
- **UNVERIFIED** Nygard, M. — *Release It!* Corpus record: year `UNRESOLVED`, `verification: unverified`;
  element prose says 2nd ed. 2018. Covers timeout, circuit breaker, fail fast, let-it-crash, steady state,
  bulkhead. Second most load-bearing; same caution.
- **UNVERIFIED** Brooker, M. — *Timeouts, Retries, and Backoff with Jitter*, Amazon Builders' Library,
  living. Corpus note: *"URL 301s to builder.aws.com, which renders client-side; article content could not
  be loaded this session."* Google SRE (verified) substitutes for the retry budget, but there is **no
  verified source in the corpus for backoff-with-jitter itself**.
- **UNVERIFIED** Huang, Y., Kintala, C., Kolettis, N. & Fulton, N. D. — *Software Rejuvenation: Analysis,
  Module and Applications*, 1995. FTCS-25, pp. 381-390. Corpus note: *"doi + primary DL page not loaded;
  venue/pages from search indexes."* BCK's `removal-from-service` tactic (verified) is the safe substitute.
- **UNVERIFIED** Randell, B. — *System Structure for Software Fault Tolerance*, 1975. IEEE TSE SE-1(2),
  220-232. (recovery blocks — not imported)
- **UNVERIFIED** Avizienis, A. — *The N-Version Approach to Fault-Tolerant Software*, 1985. IEEE TSE
  SE-11(12), 1491-1501, DOI 10.1109/TSE.1985.231893 — the DOI comes from a search result, not a loaded page.
  (not imported)
- **UNVERIFIED** Pont, M. J. — *Patterns for Time-Triggered Embedded Systems*, 2001. (loop timeout — not
  imported)
- **UNVERIFIED** FreeRTOS project — *Mastering the FreeRTOS Real-Time Kernel*, living. (stack watermarking —
  not imported)

## Where the catalogs REFINE or CONTRADICT the manifest's framing

**1. `logging` §10 "log ONCE at the handling boundary" collides with a named, sourced pattern.**
Preschern's `log-errors` prescribes the opposite placement: *"Record error details on a separate diagnostic
channel … **at the point where the error occurs**, instead of forcing all debug information through return
values to the caller,"* because *"Callers need only actionable error information, but programmers debugging
the system need full detail."* The corpus records `log-errors -alternative-to-> return-status-code` **[S]**.
The manifest's log-once rule is right about *duplicate stack traces* but, stated flatly, it pushes authors to
discard information that exists only at the raise site. The resolution is two audiences on two levels:
**DEBUG detail at the error site** (locals the boundary can no longer see) plus **exactly one
ERROR+traceback at the handling boundary**. Add the refinement and cite it.

**2. `error_tracing` §18 routes aggregate failures into the wrong channel.**
§3's own rule is that contract-level outcomes go **in-band**. But §18 offers `ExceptionGroup`/`except*` as
the answer for *"multiple independent validation failures"* — the raise channel — contradicting §3 for the
most common case in the manifest's own domain. The corpus names the in-band peer: `notification` (Fowler),
with `notification -alternative-to-> result-type` **[E]** — *"Gather all errors before returning vs
short-circuiting on the first error value"* — and `notification -specializes-> collecting-parameter`. Python
already ships one: `pydantic.ValidationError.errors()` is a notification. **Reframe §18 as a three-way
choice** — first-error Result, in-band Notification, raised ExceptionGroup — and reserve the group for
*concurrent tasks*, the case PEP 654 actually argues for.

**3. §15's "push checking to the boundary" is asserted too flatly; the corpus records three named,
mutually exclusive placement policies joined by an explicit `alternative-to` edge.**
`complete-parameter-checking` (Hanmer): validate all parameters at component boundaries *every time*,
*"detecting errors close to their source at the cost of some performance."*
`deferred-validation` (Cunningham): *"Delay comprehensive validity checking … until an action requires it,
scaling the rigor of the check to the consequences of that action,"* because *"Eager validation at entry time
rejects legitimately incomplete in-progress data and hard-codes one rigidity level."*
`meaningless-behavior` (Cunningham): omit checks in the domain, recover at the presentation boundary.
Edge: `deferred-validation -alternative-to-> complete-parameter-checking` — *"Opposite validation-placement
policies."* "Parse, don't validate" **is** complete-parameter-checking. §15 should name its choice, state the
cost its own source states, and note that editable/in-progress data is the case where deferred validation is
correct — something the current text cannot express.

**4. §13's EAFP gets a design-level rationale and a citable name.**
The manifest justifies EAFP with the glossary's *"clean and fast style."* `meaningless-behavior` supplies the
design argument: *"Defensive checks duplicated through every domain method obscure the model; centering
recovery at the presentation boundary keeps domain code minimal while tolerating bad data."* That is EAFP as
an architectural placement decision, not a stylistic preference — and per the **sourced** CHECKS edge it
pairs with `exceptional-value`: you may not adopt "no defensive checks" unless some value can carry the
badness forward.

**5. §3's "exactly two channels exist" is true of propagation but hides a third disposition.**
`exceptional-value` is neither raised nor short-circuited: *"A distinguished value object representing
missing or invalid input that flows through the domain model, absorbing or rejecting messages instead of
raising errors."* Its `-realizes-> exception-prevention` edge explains why it is its own category: it stops
the exception arising. Suggested reframing: **two propagation channels, three dispositions — raise,
return-typed, absorb-and-mark** (`exceptional-value` + `marked-data`). For data-shaped Python work (ETL,
batch, reporting) absorb-and-mark is the *dominant* disposition, and the manifest's lack of a name for it
pushes authors into `try/except/continue` with no record.

**6. §14's assertion dichotomy is missing a third kind, and the corpus reframes what assertions are for.**
§14 splits assertions into can't-happen invariants (`assert`, vanishes under `-O`) versus boundary input
(parse/raise). `sanity-check` (Douglass) names the third: a lightweight **plausibility monitor on outputs**
that must survive `-O` — *"Full result verification is often infeasible, but gross faults are cheap to catch;
checking plausibility gives broad fault coverage at minimal cost."* Separately, BCK files
`executable-assertions` under `bck-cat:control-and-observe-system-state` — a *testability/observability*
tactic: *"so the program flags when and where it enters a faulty state."* An assertion is a diagnosability
device, not only a correctness device; that reframing is the bridge from §14 into the new
runtime-diagnostics manifest.

**7. §7's raise-decision rule has a sourced name and is weaker than its source.**
`return-status-code -alternative-to-> samurai-principle` **[S]** (Preschern): *"Return an error the caller can
handle vs assert/abort when it cannot be meaningfully handled."* The Samurai Principle — *"return victorious
or not at all"* — names what §7 states as prose, and goes further: for unhandleable errors you should **not
return an error at all**, because *"Propagating unhandleable errors buries the fault and corrupts state
downstream."*

**8. §6's OPEN tag on functional-core/imperative-shell is too pessimistic.**
§6 says *"no single primary source prescribes the seam."* True of the *seam placement* — but the corpus holds
`functional-core-imperative-shell` as an element with a verified naming work (Bernhardt, Destroy All
Software, 2012) and a sourced `alternative-to monad` edge. Split the tag: the **pattern** is
ESTABLISHED-with-citation, the **seam placement in this codebase** stays OPEN. And `error-kernel` supplies
the failure-side argument §6 lacks — the core is where irreplaceable state lives *because* crashing must stay
cheap at the leaves.

**9. Retry guidance without idempotency is a data-corruption recommendation.**
The corpus states it as a sourced edge: `retry-with-exponential-backoff-and-jitter -composes-with->
idempotent-receiver` **[S]** (Hohpe & Woolf). Neither manifest currently mentions retry at all; the moment
one does, this precondition — plus `-composes-with-> timeout` **[S]** (*"each attempt is bounded by a
timeout"*) — must ship with it as a hard requirement, not a tip.

**10. fail-fast and riding-over-transients are opposites, and the manifests name neither.**
`riding-over-transients -alternative-to-> fail-fast` **[E]**: *"Tolerate and ignore momentary self-clearing
faults until they persist vs report failure immediately."* An agent handed only §2's slogan ("fail loud, fail
typed") will escalate on the first transient network blip. The corpus supplies both poles *and* the decision
mechanism (`leaky-bucket-counter`: *"distinguishing an acceptable background rate of transient errors from a
persistent fault requires rate, not count; the leak encodes the acceptable rate"*). "Errors should never pass
silently" is a rule about *silence*, not about *immediate escalation* — the manifest currently blurs the two.

**11. Neither manifest has a name for the state you go to on failure.**
`safe-state` (ISO 26262): *"A predefined operating condition without unreasonable risk that the system
deliberately enters on fault detection."* With `abort` and `degradation` (BCK) as its two flavours and
`two-phase-termination` (Grand) as its Python mechanism. §23's flowchart ends at "log with
logger.exception(), never pass silently" — it never asks *what state the program is now in*. For a CLI or
service that means distinct exit codes, a read-only mode, a disabled feature flag, parked workers.

**12. Diagnosability already has an arch-altitude vocabulary — and the corpus files it under TESTABILITY,
which is itself the finding.**
`specialized-interfaces`, `record-playback`, `localize-state-storage`, `abstract-data-sources`, `sandbox`,
and `executable-assertions` all carry `bck-cat:control-and-observe-system-state` — BCK's *testability*
tactics. Read as diagnostics they are exactly the new manifest's spine: a separated diagnostic surface that
can be removed, capture-and-replay of the fault-inducing state, one place to dump state from, swappable data
sources, and in-code oracles. **The new manifest should adopt that claim explicitly and cite it: testability
tactics and diagnosability tactics are one family, differing only in whether the observer is a test or an
operator.** Organize `python_runtime_diagnostics_manifest.md` around five named elements —
`built-in-self-test` (self-checking surfaces), `core-dump` (post-mortem capture), `maintenance-interface` +
`specialized-interfaces` (the diagnostic surface), `heartbeat` (liveness), `record-playback` (reproducing a
field failure) — with `sanity-check`, `correcting-audits`, `quarantine`, `safe-state`, and
`software-rejuvenation` as the response half.

**13. Absences in the corpus that oblige the manifests to keep certain claims OPEN.** Verified by search
over all 1083 nodes:

- **No element for exception chaining / cause preservation** (`raise X from Y`, `__cause__`). §8–§10 are the
  manifest's own synthesis over python.org and stay language-cited only; no pattern-literature name exists.
- **No element for exception-safety guarantees** (basic/strong/nothrow). Only `copy-and-swap` implies the
  strong guarantee.
- **No element for a stable/namespaced error code** or an error-code registry. §16's stable-error-code
  convention and §17's version-stable error contract have **zero corpus backing** and must stay OPEN — do
  not dress them up with a borrowed citation.
- **No `structured-logging` element.** The only structured-observability elements
  (`log-aggregation`, `distributed-tracing`, `health-check-api`) are all microservice-shaped
  (Richardson, *Microservices Patterns*, 2018, verified). The logging manifest's structlog/JSON guidance is
  correctly tagged OPEN.
- **No architecture element for the circuit breaker** — the corpus says so itself in the edge note on
  `circuit-breaker -realizes-> ignore-faulty-behavior`: *"no circuit-breaker arch element exists yet
  (missing)."* Likewise *"no roll-forward tactic exists in the arch catalog (missing)"* and *"a
  hedged-request tactic is missing from the arch catalog."*
- **No element for exit codes, profiling, or traceback rendering.** The runtime-diagnostics manifest's
  profiler and exit-code content will be python.org-cited only, with no named-pattern vocabulary — say so
  rather than implying coverage.

**14. Corpus data defects — do not propagate these into a manifest.**

- `core-dump.named_in` is the bare string `"white"` (a work id leaked into a citation field) and its `tags`
  array is **character-split into 264 single-character entries**; the intended text is *"embedded, debugging,
  borderline — diagnostics/tooling-adjacent mechanism …"*. Cite White (2024) and the GDB manual instead of
  the field.
- The same char-split defect affects 7 nodes: `expression-builder`, `draw-call-batching`, `stream-trigger`,
  `texture-atlas`, `core-dump`, `semantic-model`, `system-tick`. `system-tick` also has a bare-work-id
  `named_in`.
- `built-in-self-test.named_in` is *"Built-in self-test - Wikipedia"* — a tertiary source. The citable
  covering work in its `works` list is IEC 61508-7:2010. Cite the standard.
- `design-by-contract.named_in` says Meyer (1988) while the corpus work record is *OOSC* 2nd ed. (1997).
- `hanmer` and `nygard` carry `year: UNRESOLVED, verification: unverified` in both `corpus.json` and
  `elements.json.works`, yet their `design_elements_corpus_v1_0.md` membership lines are tagged
  `{… | verified}` — that tag covers the *membership claim*, not the bibliographic record. Between them they
  are the naming source for roughly half this slice. Re-verify both before any manifest presents their
  patterns as verified ground truth.
