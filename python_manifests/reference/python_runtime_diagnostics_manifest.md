# Runtime Diagnostics & Live Debuggability — Ground-Truth Manifest

**Purpose.** A citable ground-truth reference for inspecting a **running or crashed** Python process
in **small-to-mid-scale, strictly-typed, single-process Python** organized as a functional core
inside an imperative shell. It grounds six decisions: (1) which instrument answers which symptom,
and which of them must be armed *before* the incident to be usable *during* it; (2) whether to
attach to a live process or restart it; (3) which instrumentation substrate a home-grown probe
builds on; (4) what a failure report must carry for a field failure to be replayable without the
developer's machine; (5) which self-diagnosis surfaces the application builds itself, and which are
over-engineering at this scale; (6) which diagnostic switches are safe to leave on in production.
**Scope** is the live process: attach, monitor, dump, sample, post-mortem, self-test. This file is
**GROUNDING, not a rulebook**: cite a principle when it materially shapes a decision; reason past it
when the situation does not match. Every factual claim is tagged **ESTABLISHED** (normative and
stable in the cited primary source), **VERSION-DEPENDENT** (bound to the exact version named),
**OPEN** (no authoritative source — a convention this project must pin), or **CC-FACT** (Claude-Code
mechanics; none arise here); **FLAGGED-SECONDARY** appears inline where the only available evidence
was secondary, and **UNVERIFIED** marks a citation a source asserts that was not confirmed against a
primary record this pass (used for corpus provenance in §10 — see Sources). Statements about which
sibling file owns a topic, and pointers between sections, are collection conventions rather than
factual claims and carry no tag.

**Scope boundary — three siblings own the adjacent halves and are referenced, never repeated.** Log
and telemetry *emission* — levels, handlers, formatters, structured fields, correlation IDs,
rotation — belongs to `logging_observability_manifest.md`. The error *contract* — propagation
channels, chaining, the exception hierarchy, assertion policy, failure disposition on the raise side
— belongs to `error_tracing_contract_manifest.md`. Version, support-phase, PEP-status,
interpreter-switch-inventory and build-variant facts belong to
`python_platform_baseline_manifest.md`. This file owns only what you do when a process is **already
misbehaving**, and what must have been designed in advance for that to be possible.

**Version anchor.** Behaviour here is stated for CPython as pinned in
`python_platform_baseline_manifest.md` (verified 2026-08-08); per-feature gates are tagged inline.

---

## TL;DR

- **Arm four things at startup or lose the incident.** `PYTHONFAULTHANDLER=1`,
  `faulthandler.register(signal.SIGUSR1)` on POSIX, all four unhandled-exception channels routed
  into
  `logging`, and `PYTHONBREAKPOINT=0`. Cost is approximately zero, and none of them can be added
  once the process is already wedged — VERSION-DEPENDENT (3.14 baseline; §11c).
- **Attach instead of restarting: `python -m pdb -p PID`.** PEP 768 makes this safe, and free when
  unused, but it needs a matching `major.minor` interpreter, OS debugger permission, loopback
  reachability *back* to the debugger, and a target that reaches a bytecode boundary — a process
  blocked in a syscall is not attachable — VERSION-DEPENDENT (3.14) (§2).
- **Build new probes on `sys.monitoring`, never on `sys.settrace`.** Six tool ids exist in total,
  and `cProfile` plus coverage.py already occupy two of them during an ordinary test run —
  VERSION-DEPENDENT (3.12+) (§3).
- **Leak attribution needs `tracemalloc.start(25)`, not `start()`.** The default records **one**
  frame, almost always inside a library helper, and `-X dev` does not enable tracemalloc at all —
  VERSION-DEPENDENT (3.4+) (§5b).
- **Every profiler lies in a different direction; name the build before quoting a number.** A
  deterministic profiler distorts call-heavy code, a sampler reports estimates with a stated margin
  of error and can miss short-lived functions entirely, and native frames are absent without the
  perf trampoline plus frame pointers — VERSION-DEPENDENT (3.15 for the stdlib sampler) (§6f).
- **Diagnosability is designed, not installed.** The reproducibility contract of §11 — interpreter
  and build identity, behaviour-changing flags, content-hashed inputs, a stack — is what converts
  "cannot reproduce" into a replay, and it costs four `sys`/`sysconfig` calls — ESTABLISHED (§11a).

---

## 1. The diagnosability contract, and the symptom → instrument table

### 1a. The organising claim

**OPEN — this is the file's synthesis, not a sourced definition.** A system is **diagnosable** when
a failure can be explained from artefacts alone: without a rerun, and without a code change. Every
mechanism below is judged against that bar, and the bar has a sharp consequence — a diagnostic that
requires editing the source and re-running (the `print` statement) is not a diagnostic of a
*shipped* system at all. The supporting facts are established individually and cited in place; the
criterion itself is a project convention, and §11 is its mechanical form.

**ESTABLISHED.** The corollary is an ordering rule rather than a preference. Instruments split into
those that must be **armed before the failure** (`faulthandler`, the four exception hooks,
`tracemalloc`, shell-boundary input capture, a `weakref` canary) and those that can be **brought to
a live victim** (`pdb -p`, `profiling.sampling attach`, `py-spy`, `gdb -p`, `SIGUSR1` if
registered). Anything in the first group that was not armed is unavailable for this incident,
permanently. §11c is the always-on set that follows from this.

### 1b. Symptom → instrument, one hop

**ESTABLISHED / VERSION-DEPENDENT as tagged per row.** Read the row, use the first instrument, and
read the fourth column before believing the output.

| Symptom | First instrument (one hop) | Fallback | Precondition, and what it will **not** show | Tag |
|---|---|---|---|---|
| Process vanished, no traceback (`SIGSEGV`/`SIGABRT`/`SIGBUS`/`SIGFPE`/`SIGILL`) | `PYTHONFAULTHANDLER=1` stderr dump (§4a) | core file + `gdb <python> <core>`, then `thread apply all py-bt` (§4e) | Env var set **before** launch. No source lines, max 100 frames / 100 threads, most-recent-call **first**. Silent for `SIGKILL`, OOM-kill, `MemoryError`, clean `sys.exit()` | VERSION-DEPENDENT (3.14) |
| Process exited non-zero, nothing in the log | the four unhandled-exception channels (§4g) | `sys.last_exc` + `pdb.pm()` in the same process | Hooks installed at startup. `sys.excepthook` alone covers no thread, GC, asyncio or `SystemExit` failure | VERSION-DEPENDENT (3.12) |
| Not progressing, and the process was instrumented | `faulthandler.dump_traceback_later(t, repeat=True)` (§4b) | `kill -SIGUSR1` if `faulthandler.register` was pre-installed | Watchdog thread; `register` is POSIX-only. `exit=True` calls `_exit()` and loses buffered logs | ESTABLISHED |
| Wedged, nothing pre-installed | `python -m profiling.sampling dump PID` (§4d) | `py-spy dump --pid PID`; then `gdb -p PID` + `thread apply all py-bt` | 3.15 for the stdlib form; ptrace-level OS permission; every out-of-process tool is minor-version-coupled | VERSION-DEPENDENT (3.15) |
| Wedged inside `asyncio` | `python -m asyncio pstree PID` (§4f) | `asyncio.print_call_graph()` in-process | 3.14. Errors out on a cyclic await graph; tasks wired with raw `add_done_callback()` are invisible | VERSION-DEPENDENT (3.14) |
| Memory growing without bound | `weakref` canary at the lifecycle boundary (§5d), then `tracemalloc` two-snapshot `compare_to(..., 'traceback')` (§5b) | `memray run --native` (§5e) | tracemalloc must be started **before** the allocations, with `nframe >= 25`. Blind to non-`PyMem_*` allocations; memray is Linux/macOS only | ESTABLISHED |
| Slow, and you may restart it | `python -m profiling.sampling run` (§6c) or `cProfile` (§6b) | `-X perf` + `perf record` for native frames (§6d) | Deterministic profiling distorts call-heavy code; the sampler reports estimates | VERSION-DEPENDENT (3.15) |
| Slow, and you may **not** restart it | `python -m profiling.sampling attach PID` (§6c) | `py-spy record --pid PID`; `austin -p PID` (§6e) | py-spy 0.4.2 and austin 4.0.0 declare support only through 3.14 | VERSION-DEPENDENT (3.15) |
| Slow startup / slow imports | `-X importtime=2` (§7c) | `-v` / `-vv` for the module search itself | 3.14 for `=2`, which prints the literal string `cached`, not a float. Output "may be broken in multi-threaded application" | VERSION-DEPENDENT (3.14) |
| Wrong answer, nothing raised | in-code plausibility checks that survive `-O` (§10b `sanity-check`) | a `verify [--repair]` audit over persisted state (§10b `correcting-audits`) | Nothing raised means no traceback, no `sys.last_exc` and no post-mortem entry point: this symptom is diagnosable only if it was designed for | OPEN |
| Cannot reproduce | replay the captured shell-boundary inputs (§10b `record-playback`) | `-X dev` + `-W error` to surface warnings the default filters hid (§7a, §7b) | Capture must pre-exist the failure. §11b is the checklist | ESTABLISHED |
| "What am I even running?" | `sys.version`, `sys._xoptions`, `sys.flags`, `sysconfig.get_config_var("Py_GIL_DISABLED")`, `sys._is_gil_enabled()` (§11a) | `python -VV` | Free. Do this first in any performance or concurrency argument (§9d) | VERSION-DEPENDENT (3.13+) |

### 1c. What each instrument costs when nothing is wrong

**ESTABLISHED / OPEN as tagged.** Steady-state cost is what decides whether an instrument can be
left on. Where no primary source quantifies an overhead, this table says so rather than inventing a
figure.

| Instrument | Cost while idle | Cost while active | Tag |
|---|---|---|---|
| PEP 768 attach interface | **zero by construction** — debugger fields are read only when `eval_breaker` is already set, a check the eval loop performs anyway | one script execution at the next safe point | ESTABLISHED |
| `faulthandler.enable()` | handlers installed; nothing runs until a fatal signal arrives | a signal-safe dump | ESTABLISHED |
| `faulthandler.dump_traceback_later()` | — | one watchdog thread | ESTABLISHED |
| `sys.monitoring` | free for events not armed; un-instrumented code keeps its specialised bytecode | PEP 669: "orders of magnitudes less than for `sys.settrace()`" for a small event set | ESTABLISHED |
| audit hooks, none installed | PEP 578 measured "between 1.05x faster to 1.05x slower" — inside noise | paid on **every** audited event, and `import`, `open` and attribute access are hot | ESTABLISHED |
| `tracemalloc` | — | captures `nframe` frames per allocation. Unquantified in the docs, which is itself why `-X dev` excludes it ("the overhead cost (to performance and memory) would be too large"). Measure it with `tracemalloc.get_tracemalloc_memory()` | OPEN |
| `gc.set_debug(gc.DEBUG_LEAK)` | — | **unbounded memory growth by design** (§5c) | ESTABLISHED |
| `profiling.sampling` (external) | zero — "The target process requires no modification and need not be restarted"; target overhead "virtually zero" | zero on the target | VERSION-DEPENDENT (3.15) |
| `-X perf` trampoline | off by default | "not free while active": a trampoline is compiled before the execution of every Python function | ESTABLISHED |

---
## 2. Attach, don't restart — the PEP 768 safe-attach interface

### 2a. The interface, exactly

**VERSION-DEPENDENT (3.14).** PEP 768 ("Safe external debugger interface for CPython") is **Final**,
`Python-Version: 3.14`. The feature exists in every 3.14.x and later and in **no** 3.13.x. There is
one user-facing entry point and one Python API:

| Surface | Exact form | Note |
|---|---|---|
| Operator entry point | `python -m pdb -p PID` (`-p`, `--pid`), added 3.14 | Full synopsis: `python -m pdb [-c command] (-m module \| -p pid \| pyfile) [args ...]` |
| Python API | `sys.remote_exec(pid, script)` | `script` is a **path** (`str \| bytes \| PathLike`) to a file of Python code — **not** a source string. Availability: Unix, Windows |
| Underlying function | `pdb.attach(pid, commands=())` | **Absent from `pdb.__all__`**, which is `["run", "pm", "Pdb", "runeval", "runctx", "runcall", "set_trace", "post_mortem", "set_default_backend", "get_default_backend", "help"]`. Treat the CLI as the supported interface |

**VERSION-DEPENDENT (3.14).** `sys.remote_exec()` returns **immediately** and there is **no
interface to learn when, or whether, the code ran**; the target executes it at its next eval-loop
safe point. The caller must keep the script file alive until it observes a side effect — deleting
the file right after the call is a race.

**ESTABLISHED.** Passing a *path* rather than *code* is a deliberate mitigation: PEP 768 states it
"prevents attackers with arbitrary writes from escalating to arbitrary code execution through this
interface." **ESTABLISHED.** Overhead when unused is zero by construction (§1c).

### 2b. What the interface does **not** do — the four coupling constraints

**VERSION-DEPENDENT (3.14).** Each of these is a real, observed failure mode, not a theoretical one.

1. **It does not interrupt a blocked process.** `Doc/library/pdb.rst` states verbatim: "Attaching to
   a process that is blocked in a system call or waiting for I/O will only work once the next
   bytecode instruction is executed or when the process receives a signal." A process blocked in
   `accept()`, `time.sleep()`, or a C extension's blocking call is **not attachable** until it
   returns to bytecode. For that case use an out-of-process stack dump instead (§4d).
2. **It does not cross a network-namespace boundary.** Attach is socket-based once bootstrapped:
   `pdb.attach()` opens `socket.create_server(("localhost", 0))`, writes a temp connect script
   calling `pdb._connect(host="localhost", port=..., frame=sys._getframe(1), ...)`, chmods that
   script readable by group and other, calls `sys.remote_exec(pid, connect_script.name)`, then
   blocks on `server.accept()`. **The target dials back to the debugger's loopback address.** A
   target in another container has a different `localhost`, and the target's uid must be able to
   *read* the temp script path.
3. **It does not tolerate a version mismatch.** The target must run the **same `major.minor`
   CPython**; for pre-release interpreters the version must match **exactly**.
   `_PdbServer.protocol_version()` returns `int(f"{major:02X}{minor:02X}{revision:02X}F0", 16)` with
   `revision = 0` by default.
4. **It does not time out.** There is no timeout on the accept — `Lib/pdb.py` carries the literal
   comment `# TODO Add a timeout? Or don't bother since the user can ^C?`. Against a truly wedged
   process, `python -m pdb -p PID` hangs until interrupted, so **failure to attach looks exactly
   like the hang you were investigating**.

**VERSION-DEPENDENT (3.14).** Two further sharp edges. The injected script path lives in a **fixed
512-byte buffer** (`Include/cpython/pystate.h`: `#define _Py_MAX_SCRIPT_PATH_SIZE 512`), so a deep
container mount or a long `TMPDIR` is a genuine truncation risk. And on Windows the client uses a
**second** socket connection plus a signal-raising thread (`use_signal_thread = sys.platform ==
"win32"`, `interrupt_sock`), where on POSIX `interrupt_sock` is `None` — interrupt semantics differ
by platform.

**ESTABLISHED.** Access control is the OS's, unchanged from native debuggers: Linux `ptrace` /
`CAP_SYS_PTRACE` / `/proc/sys/kernel/yama/ptrace_scope`; macOS `task_for_pid()` (root, a debugger
entitlement, or SIP disabled); Windows `PROCESS_VM_READ` + `PROCESS_VM_WRITE` / `SeDebugPrivilege`.
The same requirement governs `profiling.sampling attach` (§6c) and `py-spy` (§6e), so solving it
once solves it for the whole out-of-process family.

### 2c. The kill switches — and the CPython documentation bug that makes one of them a no-op

**VERSION-DEPENDENT (3.14).** Three opt-outs exist, in decreasing order of finality:

| Opt-out | Exact spelling | Effect |
|---|---|---|
| Build option | `--without-remote-debug` | Leaves `Py_REMOTE_DEBUG` undefined and hard-wires `config->remote_debug = 0` |
| Interpreter option | `-X disable-remote-debug` — **hyphens** | Disables the interface for this process |
| Environment variable | `PYTHON_DISABLE_REMOTE_DEBUG` | Disables the interface for this process |

**VERSION-DEPENDENT (3.14, 3.15, 3.16) — CPython documentation bug, still live on 2026-08-08.**
`Doc/using/cmdline.rst` documents `-X disable_remote_debug` (**underscores**) on both the 3.14
branch and `main`, but `Python/initconfig.c` looks up only `config_get_xoption(config,
L"disable-remote-debug")` (**hyphens**) on both branches, and `--help-xoptions` prints the
hyphenated form. **The interpreter does not error on unknown `-X` names**, so the underscore
spelling is silently ignored and the operator believes remote debugging is off when it is on. Copy
the hyphenated form into any hardening checklist.

**VERSION-DEPENDENT (3.14) — second doc/implementation disagreement.** `cmdline.rst` says the
variable disables the feature "If this variable is set to a non-empty string".
`config_init_remote_debug()` reads it with `Py_GETENV()`, which is a bare `getenv()`, and tests only
`if (env)`. Therefore **`PYTHON_DISABLE_REMOTE_DEBUG=` (empty) DOES disable it** — PEP 768 states
this correctly ("any value (including empty string)"). Contrast `PYTHONFAULTHANDLER` and
`PYTHONDEVMODE`, read via `config_get_env()` → `_Py_GetEnv()`, which returns `NULL` when `var[0] ==
'\0'` and so treats empty as **unset**. An empty value in a Dockerfile, `.env` file or Kubernetes
manifest therefore silently breaks `pdb -p` and `profiling.sampling attach` while silently leaving
faulthandler off — opposite senses, same kind of typo.

**Recommendation, and the reason.** Leave remote debugging **enabled** in production. It costs
nothing when unused (§1c), it is the only instrument that turns "restart it and hope" into "look at
it", and the OS permission gate is the real control (§2b). Disable it only where the threat model
says an attacker already has arbitrary local writes plus the ability to signal your process — in
which case `--without-remote-debug` at build time, not a `-X` flag, is the honest answer — OPEN (a
project threat-model decision; see §Open questions).

### 2d. Detecting or refusing injected debugging

**VERSION-DEPENDENT (3.14).** Two audit events fire, in different processes: **`sys.remote_exec`**
(args: `pid`, script path) in the **calling** process, and **`cpython.remote_debugger_script`**
(arg: script path) in the **target**. The second is the hook to install if injection must be
detected or refused. Read §8a first: an audit hook cannot be removed once installed, and a hook that
raises takes the process down rather than refusing cleanly.

**VERSION-DEPENDENT (3.14.5).** CPython 3.14.5 hardened `_remote_debugging` "by validating remote
debug offset tables before using them to size memory reads or interpret remote layouts" — a
Security-section fix. Treat the *debugger* side as attack surface too when it runs against untrusted
PIDs.

---

## 3. `sys.monitoring` (PEP 669) — the modern instrumentation substrate

### 3a. Why it replaces `settrace`/`setprofile` for anything new

**ESTABLISHED.** PEP 669 ("Low Impact Monitoring for CPython") states the difference plainly: "If a
small set of events are active, e.g. for a debugger, then the overhead of callbacks will be orders
of magnitudes less than for `sys.settrace()` and much cheaper than using PEP 523." The mechanism is
what matters: `sys.settrace` is all-or-nothing per thread and fires on every line, whereas
`sys.monitoring` arms individual events per code object, so un-instrumented code keeps its
specialised bytecode.

**VERSION-DEPENDENT (3.12).** PEP 669 is **Final**, `Python-Version: 3.12`; `sys.monitoring` does
not exist before 3.12. On 3.12+ any new tool uses it, and `sys.settrace` is for reading existing
tools rather than writing new ones (§8b). A probe that must also run on 3.11 needs a second
implementation — usually the argument for using an existing tool instead.

### 3b. The tool-id budget is six, and it is already half spent

**VERSION-DEPENDENT (3.12+).** There are exactly **six tool ids, 0–5 inclusive**. Four are named:
`DEBUGGER_ID = 0`, `COVERAGE_ID = 1`, `PROFILER_ID = 2`, `OPTIMIZER_ID = 5`. **3 and 4 are unnamed
and free.** The docs state "All IDs are treated the same by the VM with regard to events" — the
constants are a **cooperation convention, not an enforcement mechanism**.

**VERSION-DEPENDENT (3.12+).** `use_tool_id(tool_id, name, /)` "Raises a `ValueError` if `tool_id`
is in use." This is the single most common way two diagnostic tools collide at runtime, and two
stdlib occupants make it likely:

| Occupant | Id | Since | Consequence |
|---|---|---|---|
| `cProfile` | 2 (`PROFILER_ID`), registered under the name `"cProfile"` | 3.12 — `Modules/_lsprof.c` calls `use_tool_id`, `register_callback`, `set_events`, `free_tool_id`; the 3.11 file contains zero references to monitoring | `cProfile.Profile().enable()` raises `ValueError` when a second live `cProfile.Profile`, or any third-party profiler that claimed `PROFILER_ID`, already holds it. 3.14.7 shipped "Fix `cProfile.Profile.enable` to no longer overwrite errors from `sys.monitoring`" (gh-153068) |
| coverage.py `sysmon` core | 1 (`COVERAGE_ID`) | selectable with `COVERAGE_CORE=sysmon` or `core = sysmon`; **the default on Python 3.14+ where supported** — FLAGGED-SECONDARY (the default claim comes from coverage.readthedocs.io text surfaced via search rather than a fetched page) | `sysmon` does not support plugins, dynamic contexts, or some concurrency libraries, and on 3.12/3.13 it does not support branch coverage |

**VERSION-DEPENDENT (3.14).** So a `pytest --cov` run that also profiles is already contending for
the budget. Practical rule for a home-grown probe: claim **id 3 or 4** with a distinctive name, wrap
`use_tool_id` in a handler that reports *which* tool holds the id via `get_tool(id)`, and always
release with `free_tool_id()` rather than `clear_tool_id()` — `clear_tool_id` unregisters all events
and callbacks but **keeps** the id, while `free_tool_id` clears and then releases it.

### 3c. Three event classes, and only one of them can be disabled

**VERSION-DEPENDENT (3.14).** The partition is the part agents get wrong, because `DISABLE` — the
mechanism that makes coverage measurement cheap — works on only one class.

| Class | Events | Tied to a code location? | `DISABLE` allowed? |
|---|---|---|---|
| **Local** | `PY_START`, `PY_RESUME`, `PY_RETURN`, `PY_YIELD`, `CALL`, `LINE`, `INSTRUCTION`, `JUMP`, `BRANCH_LEFT`, `BRANCH_RIGHT`, `STOP_ITERATION` | yes | yes |
| **Ancillary** | `C_RAISE`, `C_RETURN` | gated by `CALL` | — |
| **Other** | `PY_THROW`, `PY_UNWIND`, `RAISE`, `EXCEPTION_HANDLED`, `RERAISE` | no | not individually, through 3.14 |

**VERSION-DEPENDENT (3.12+).** `DISABLE` returned from a callback stops that callback for that
`(code, instruction_offset)` **permanently**, until `restart_events()`. It "does not change which
events are set, or any other code locations for the same event."

**VERSION-DEPENDENT (3.12–3.14).** Returning `DISABLE` from a callback for an "other" event raises
`ValueError` **"in a non-specific location (that is, no traceback will be provided)"** — an
essentially undebuggable error. **VERSION-DEPENDENT (3.15).** 3.15 relaxes this (gh-146182):
`PY_THROW`, `PY_UNWIND`, `RAISE`, `EXCEPTION_HANDLED` and `RERAISE` can be enabled and disabled
**per code object**, and returning `DISABLE` from their callbacks disables the event for the whole
code object "rather than raising `ValueError` as in prior versions". The same callback is therefore
a crash on 3.14 and correct on 3.15 — if a probe must span both, guard on the version explicitly.

**VERSION-DEPENDENT (3.12+).** `C_RETURN` and `C_RAISE` "will only be seen if the corresponding
`CALL` event is being monitored". Arming them alone yields **silence, not an error**.

**VERSION-DEPENDENT (3.12+).** `restart_events()` is **global, not per-tool**. Any tool may re-arm
every other tool's disabled locations, so a correct tool must tolerate receiving events it had
disabled.

**VERSION-DEPENDENT (3.14).** `BRANCH` is **deprecated in 3.14** in favour of `BRANCH_LEFT` /
`BRANCH_RIGHT`, because "they can be disabled independently" and so give "much better performance".

### 3d. Callback arities are per-event and positional

**VERSION-DEPENDENT (3.14).** Treating the second argument uniformly produces plausible, wrong
output — the classic silent defect in a hand-rolled probe.

| Event(s) | Callback signature |
|---|---|
| `PY_START`, `PY_RESUME`, `INSTRUCTION` | `(code, instruction_offset)` |
| `PY_RETURN`, `PY_YIELD` | `(code, instruction_offset, retval)` |
| `CALL`, `C_RAISE`, `C_RETURN` | `(code, instruction_offset, callable, arg0)` — `arg0` may be `MISSING` |
| **`LINE`** | **`(code, line_number)` — a line number, not an instruction offset** |
| `BRANCH_LEFT`, `BRANCH_RIGHT`, `JUMP` | `(code, instruction_offset, destination_offset)` |
| exception events | `(code, instruction_offset, exception)` |

**VERSION-DEPENDENT (3.14.7).** 3.14.7 fixed "undefined behaviour when a `sys.monitoring` callback
raised an exception while the program was following a branch or loop" (gh-152375). A callback that
can raise is a correctness hazard for the interpreter, not merely for the tool: keep callbacks
total, and route their own failures to a log rather than letting them propagate.

### 3e. `pdb` runs two debugger cores, and the default is not the one you get

**VERSION-DEPENDENT (3.14).** `pdb` gained a selectable backend in 3.14 —
`pdb.set_default_backend(backend)` and `pdb.get_default_backend()`, with backends `'settrace'` and
`'monitoring'`. **The default is `'settrace'`.** But `pdb.rst` states verbatim: "`breakpoint()` and
`set_trace()` will not be affected by this function. They always use `'monitoring'` backend." One
interpreter therefore runs two different debugger cores depending on how pdb was entered, and any
performance or tool-collision reasoning based on the default is wrong for the two most common entry
points. `bdb.Bdb` carries the `backend` argument; `pdb.Pdb` in 3.14 accepts `mode`, `backend` and
`colorize`.

---
## 4. Crash, hang, and wedge

### 4a. `faulthandler` catches exactly five signals and nothing else

**VERSION-DEPENDENT (3.14).** `faulthandler.enable(file=sys.stderr, all_threads=True, c_stack=True)`
installs handlers for exactly five signals — `SIGSEGV`, `SIGFPE`, `SIGABRT`, `SIGBUS`, `SIGILL` —
plus a Windows exception handler since 3.6. `c_stack=True` is **new in 3.14**, as is
`faulthandler.dump_c_stack(file=sys.stderr)`, which "Dump[s] the C stack trace of the current
thread"; where the build or OS does not support it, "this prints an error in place of a dumped C
stack" rather than raising.

**VERSION-DEPENDENT (3.3+).** Startup switches are `-X faulthandler` or `PYTHONFAULTHANDLER`
(**non-empty** — `config_init` reads it via `config_get_env()`, so `PYTHONFAULTHANDLER=` is *unset*,
the opposite of `PYTHON_DISABLE_REMOTE_DEBUG` in §2c).

**ESTABLISHED.** faulthandler catches **fatal signals only**. It does **not** catch `SIGKILL`,
`SIGSTOP`, an OOM-kill, a clean `sys.exit()`, `MemoryError`, an uncaught Python exception, or a
hang. An agent that installs faulthandler "for crashes" has not covered the most common production
terminations — the OOM killer and an uncaught exception. Those are §4g's job.

**VERSION-DEPENDENT (3.10+).** Since 3.10 the dump "mentions if a garbage collector collection is
running" when `all_threads` is true — a direct signal for "crashed inside a finalizer", which
changes the investigation entirely (§5c).

**VERSION-DEPENDENT (3.14) — free-threaded caveat, verbatim:** "Only the current thread is dumped if
the GIL is disabled to prevent the risk of data races." On a free-threaded build `all_threads=True`
is silently downgraded and a crash dump shows one stack (§9c).

### 4b. Hang detection with cooperation: the watchdog and the on-demand dump

**ESTABLISHED.** `faulthandler.dump_traceback_later(timeout, repeat=False, file=sys.stderr,
exit=False)` is the hang detector. "This function is implemented using a watchdog thread." The timer
has sub-second resolution, and calling it again replaces the parameters and resets the timeout —
which is exactly what makes it usable as a progress watchdog: re-arm it at the top of each loop
iteration and a stalled iteration dumps every thread's stack (§10b `watchdog`).

**ESTABLISHED.** `exit=True` calls `_exit()` with status 1: "Note `_exit()` exits the process
immediately, which means it doesn't do any cleanup like flushing file buffers." Buffered `logging`
records and stdio output are lost precisely when they matter most. Prefer `exit=False` plus an
explicit cooperative shutdown (§10b `safe-state`), and reserve `exit=True` for a supervised process
where the restart is the point.

**ESTABLISHED.** `faulthandler.register(signum, file=sys.stderr, all_threads=True, chain=False)` and
`unregister(signum)` are **"Not available on Windows."** The `SIGUSR1`-dumps-a-stack runbook is
POSIX-only and needs a documented Windows alternative (§4d) before it goes into a cross-platform
runbook.

**VERSION-DEPENDENT (3.15).** 3.15 adds a `max_threads` parameter to `faulthandler.enable()`,
`dump_traceback()`, `dump_traceback_later()` and `register()` (gh-149085) — relevant only if the
100-thread cap in §4c is biting.

### 4c. faulthandler's output is deliberately crippled — do not expect a traceback

**ESTABLISHED.** Because the handler may call only signal-safe functions, it cannot allocate heap
memory and its output is impoverished by design: **no source lines** (filename, function name and
line number only), strings truncated at **500 characters**, at most **100 frames** and **100
threads**, non-ASCII mangled via `backslashreplace`, and most-recent-call **first** — reversed
relative to a normal Python traceback. Anyone reading a faulthandler dump as if it were a
`traceback.print_exc()` output reads the stack upside down.

**ESTABLISHED — the file-descriptor hazard.** `enable()`, `dump_traceback_later()` and `register()`
retain the *file descriptor*, not the file object. If that file is closed and the fd is reused,
tracebacks are written into an unrelated file. **Re-call these functions whenever the log sink is
replaced** — which means faulthandler setup must run *after* logging configuration, and again after
any handler rotation that reopens a file (rotation policy: `logging_observability_manifest.md`).

### 4d. Getting a stack out of a wedged process, with nothing pre-installed

**In-process, dependency-free — ESTABLISHED.** `sys._current_frames()` returns a dict mapping thread
id to the topmost frame, and its documented purpose is "debugging deadlocks without requiring
cooperation from deadlocked threads". Render with `traceback.format_stack(frame)`. It raises the
audit event `sys._current_frames`. **This is the correct implementation of a `SIGUSR1`-style thread
dump inside a maintenance interface (§10b `maintenance-interface`) — but see §9c: printing
`f_locals` from these frames can crash a free-threaded interpreter.**

**Out-of-process, ordered by cost — VERSION-DEPENDENT as marked.**

| Order | Command | Requires | Note |
|---|---|---|---|
| a | `python -m profiling.sampling dump PID` | 3.15 | Stdlib. Prints "a traceback-style stack of every thread (or all asyncio tasks with `--async-aware`). Useful for investigating hung processes." |
| b | `py-spy dump --pid PID` (add `--locals`) | py-spy 0.4.2 | Interpreter-version-independent tool, but declares support only for CPython 2.3–2.7 and 3.3–**3.14** |
| c | `austin -w PID` / `--where=PID` | austin 4.0.0 | "Dump[s] the stacks of all the threads within the" target. Declares 3.9–**3.14** |
| d | `gdb -p PID` then `thread apply all py-bt` | gdb 7.0+ with Python support, plus debug info — **POSIX in practice**: `py-bt` comes from the `python-gdb.py` helper that distributions install (§4e) | The only answer when the target is blocked below Python entirely (§4e) |
| e | `kill -SIGUSR1 PID` | `faulthandler.register(signal.SIGUSR1)` pre-installed; POSIX | Cheapest of all — if it was armed |
| f | `python -m asyncio pstree PID` | 3.14 | Async task tree (§4f) |

**VERSION-DEPENDENT (3.15).** Options (a) and (f) need a modern interpreter; (b)–(e) are
interpreter-version-independent as *tools* but (b) and (c) are coupled to the versions they parse.
§6e records the lag: as of 2026-08-08 neither py-spy nor austin claims 3.15.

**Platform — rows (d) and (e) are POSIX, and the ladder narrows on Windows.** Row (e) needs
`faulthandler.register`, which is "Not available on Windows" (§4b), and row (d)'s `py-bt` comes from
the distribution-installed helper (§4e). What is left on a Windows host is (b) py-spy 0.4.2, whose
README declares Linux, macOS, **Windows** and FreeBSD (64-bit Windows only) — VERSION-DEPENDENT
(py-spy 0.4.2) — (c) austin 4.0.0, whose compatibility table lists Windows x86_64/i686 —
VERSION-DEPENDENT (austin 4.0.0) — and the remote-attach forms (a) and (f), whose availability §2a
records as "Unix, Windows". So a Windows wedge is still diagnosable, but not with gdb and not with a
signal; the runbook must say which of the four it uses. Core files and WER (§4e) cover the *crash*
case, not the wedge case, and the Windows substitute for the `SIGUSR1` runbook remains OPEN (see
§Open questions).

### 4e. Core files, gdb, and when gdb is the only answer

**ESTABLISHED.** Nothing in Python configures core dumps. They are an OS concern: `ulimit -c`,
`/proc/sys/kernel/core_pattern`, systemd-coredump, Windows WER. Decide this at deployment time,
because a crash with `ulimit -c 0` leaves only the faulthandler dump.

**ESTABLISHED.** The gdb helpers (`howto/gdb_helpers.html`, "Debugging C API extensions and CPython
Internals with GDB") ship with CPython as `python-gdb.py` (from `Tools/gdb/libpython.py`, installed
by distributions as `libpython3.14-gdb.py`), loaded via `add-auto-load-safe-path` or `source`.
Commands: `py-bt`, `py-bt-full`, `py-list`, `py-locals`, `py-print`, `py-up`, `py-down`. Requires
gdb 7.0+ with Python support plus debug info (`apt install python3-dbg`, `dnf debuginfo-install
python3`).

**ESTABLISHED.** `thread apply all py-bt` is the one-line "what is every thread doing at the Python
level" command, and it works identically on a live `gdb -p PID` and on a core file (`gdb
/path/to/python /path/to/core`). **gdb is the only answer when** the process is blocked below Python
(in a C extension, in the kernel, or in a signal handler), when the interpreter itself is corrupt so
no in-process or attach-based mechanism can be trusted, or when all you have is a core file.

**ESTABLISHED — the honest tension.** "Optimized builds may lose frame information", so `py-up` and
`py-down` may be unable to read Python frame information: **a release-optimised interpreter is a
worse crash-analysis target than a `--with-pydebug` one**. This runs directly against §6f's rule
that performance must be measured on the shipped build. The two goals want different builds; the
resolution is to ship the optimised build, keep debug info available for it, and never reason about
performance from the debug build. Build-variant inventory: `python_platform_baseline_manifest.md`.

### 4f. Async hangs have their own instruments

**VERSION-DEPENDENT (3.14).** `python -m asyncio ps PID` prints a table of tasks with coroutine
stacks and awaiter chains; `python -m asyncio pstree PID` prints the await tree. Both raise an error
if the await graph contains cycles. Both are built on the PEP 768 out-of-process machinery, so §2b's
constraints apply in full.

**VERSION-DEPENDENT (3.14).** In-process equivalents: `asyncio.capture_call_graph()`,
`asyncio.format_call_graph()` and `asyncio.print_call_graph()` (all taking `depth`/`limit`),
returning `FutureCallGraph` / `FrameCallGraphEntry`. Code that wires futures with raw
`add_done_callback()` instead of `shield()`/`TaskGroup` must call `future_add_to_awaited_by()` /
`future_discard_from_awaited_by()` itself **or be invisible in `ps`/`pstree`** — a design
obligation, not a tooling detail: choosing raw callbacks over structured concurrency costs you the
hang diagnostic. Structured concurrency and cancellation:
`python_concurrency_determinism_manifest.md`.

### 4g. Post-mortem: the four last-resort channels, and `sys.last_exc`

**ESTABLISHED.** `sys.excepthook` alone covers **none** of: thread failures, destructor/GC/weakref
failures, asyncio callback and never-retrieved failures, executor done-callback failures, or
`SystemExit`. A process that wants every failure recorded must install all four channels — the three
hooks plus the asyncio loop handler — and additionally retrieve `concurrent.futures` results by
hand,
because that library ships no hook at all (`error_tracing_contract_manifest.md` §20a). That file
owns
the contract and the install-function shape; this file states only why each one is a *diagnostics*
obligation.

| Channel | Hook | Diagnostics consequence if unclaimed | Tag |
|---|---|---|---|
| Main-thread uncaught | `sys.excepthook(type, value, traceback)` | `SystemExit` never reaches it | ESTABLISHED |
| Thread `run()` escape | `threading.excepthook(args)` — `exc_type`, `exc_value`, `exc_traceback`, `thread` | "If `exc_type` is `SystemExit`, the exception is silently ignored": a worker calling `sys.exit()` produces **no output at all** | VERSION-DEPENDENT (3.8; `threading.__excepthook__` 3.10) |
| Destructor / GC / weakref callback | `sys.unraisablehook(unraisable)` — `exc_type`, `exc_value`, `exc_traceback`, `err_msg`, `object` | The only channel for failures the interpreter cannot raise; the default merely prints to stderr. Two documented hazards: storing `exc_value` "creates a reference cycle" (clear it), and storing `object` "can resurrect objects being finalized" | VERSION-DEPENDENT (3.8+) |
| asyncio | `loop.set_exception_handler(handler)` | Never-retrieved task exceptions surface only at GC time, via the `asyncio` logger | ESTABLISHED |

**VERSION-DEPENDENT (3.12, 3.13).** In-process post-mortem is two calls: `sys.last_exc` (3.12,
superseding the deprecated `sys.last_type` / `sys.last_value` / `sys.last_traceback`) carries the
exception, and `pdb.pm()` enters post-mortem on it. `pdb.post_mortem(t=None)` gained **support for
exception objects in 3.13** (previously traceback objects only). This is the shape of "debug a
failure from an artefact" *inside* one process — and the reason a crash handler should stash the
exception object rather than only its formatted text.

**VERSION-DEPENDENT (3.7+).** `breakpoint()` calls `sys.breakpointhook()`, which consults
**`PYTHONBREAKPOINT`**: unset or empty means `"pdb.set_trace"`, a dotted path names any callable
(`PYTHONBREAKPOINT=IPython.terminal.debugger.set_trace`), and **`PYTHONBREAKPOINT=0` makes
`breakpoint()` a no-op that returns immediately**. That is the correct way to neuter stray
breakpoints in CI and production *without editing code*; the lint rule that stops them being
committed in the first place belongs to `python_linting_practices_manifest.md`, which owns the exact
rule code — this file does not invent one.

---

## 5. Memory: attributing growth to a call site

### 5a. The escalation ladder

**ESTABLISHED.** Five steps, cheapest first. Do not skip to step 2: without step 1 you do not know
whether anything is actually leaking.

1. **`weakref` canary** proves an object outlives its scope (§5d).
2. **`tracemalloc` two-snapshot `compare_to(old, 'traceback')` with `nframe >= 25`** names the
   allocating stack (§5b).
3. **`tracemalloc.get_object_traceback(obj)`** maps a specific live suspect back to its allocation
   site.
4. **`gc.get_referrers(obj)`** or `objgraph.show_backrefs` finds who is holding it (§5c).
5. **`memray run --native`** if the allocation is not visible to `PyMem_*` at all (§5e).

### 5b. `tracemalloc`: two defaults that defeat beginners, and three structural blind spots

**VERSION-DEPENDENT (3.4+).** `tracemalloc.start(nframe=1)` — the default of **one frame** records
only the allocating line, which is almost always a helper inside a library and useless for
attribution. Set `nframe` to 10–25 (`-X tracemalloc=25`, `PYTHONTRACEMALLOC=25`) if you intend to
attribute a leak to a call site.

**VERSION-DEPENDENT (3.4+).** `ResourceWarning` names the allocation site **only if tracemalloc is
on**. Verbatim from `devmode.rst`: without it you get `ResourceWarning: Enable tracemalloc to get
the object allocation traceback`; with `-X dev -X tracemalloc=5` you additionally get `Object
allocated at (most recent call last): ...`. **`-X dev` alone is not enough** (§7a).

**ESTABLISHED — what tracemalloc structurally cannot see:** allocations made **before** `start()`;
allocations that do not go through `PyMem_*`/`PyObject_*` (a C extension calling `malloc()`
directly, and most third-party native libraries); and memory already released before the snapshot. A
flat tracemalloc diff is therefore not evidence of no leak — it is evidence of no leak *in the
traced domain*.

**ESTABLISHED.** `Snapshot.compare_to(old_snapshot, key_type, cumulative=False)` and
`Snapshot.statistics(key_type, cumulative=False)` accept exactly three `key_type` values:
`'filename'`, `'lineno'`, `'traceback'`. Leak attribution is the two-snapshot `compare_to(...,
'traceback')` diff, never a single snapshot. `get_traced_memory() -> (current, peak)`,
`reset_peak()` (3.9) and `get_tracemalloc_memory()` (tracemalloc's own cost) cover measurement;
`Filter` / `DomainFilter` narrow a snapshot. `Snapshot.dump(filename)` / `Snapshot.load(filename)`
is what makes a leak investigation an *artefact* rather than a live session — dump from the
maintenance interface (§10b `maintenance-interface`), analyse offline.

**VERSION-DEPENDENT (3.7+).** Since 3.7 tracemalloc frames are ordered **oldest to most recent**;
code written against 3.6 or earlier that indexes `traceback[0]` expecting the allocating line gets
the outermost frame instead.

### 5c. `gc` introspection, and the debug flag that leaks on purpose

**ESTABLISHED.** The debug flags are `DEBUG_STATS`, `DEBUG_COLLECTABLE`, `DEBUG_UNCOLLECTABLE`,
`DEBUG_SAVEALL`, and `DEBUG_LEAK`, which is exactly `DEBUG_COLLECTABLE | DEBUG_UNCOLLECTABLE |
DEBUG_SAVEALL`.

**ESTABLISHED — `DEBUG_SAVEALL` / `DEBUG_LEAK` deliberately leak**: "all unreachable objects found
will be appended to `garbage` rather than being freed". Setting `DEBUG_LEAK` in a long-running
process is an unbounded memory leak *introduced by the leak detector*. It is a bounded-run
diagnostic, and if a maintenance interface exposes it, it must be separately gated with a documented
reason (§10b `maintenance-interface`).

**ESTABLISHED.** `gc.garbage` "should be empty most of the time" since **3.4** (PEP 442): objects
with `__del__` no longer end up there. A non-empty `gc.garbage` in 2026 means a C extension type
with a non-`NULL` `tp_del`, or `DEBUG_SAVEALL`. A non-empty list at shutdown emits a
`ResourceWarning` (silent by default) since 3.2. **The inverse inference is the trap: an empty
`gc.garbage` is not evidence of no leaks** — cycles are collected, not reported there.

**ESTABLISHED.** Cycle-hunting API: `gc.get_referrers(*objs)` (who points at this),
`gc.get_referents(*objs)`, `gc.get_objects(generation=None)`, `gc.is_tracked(obj)`,
`gc.is_finalized(obj)` (3.9), `gc.get_stats()` (3.4), `gc.get_count()`, `gc.get_threshold()` /
`set_threshold()`, `gc.freeze()` / `unfreeze()` (3.7), `gc.callbacks` (3.3). `gc.freeze()` before a
`fork()` stops copy-on-write pages being dirtied by a collection in each child — a behaviour change
that alters what a post-fork leak measurement means.

**ESTABLISHED.** `gc.get_referrers()` walks every tracked object, is **O(heap)**, and will report
the *investigating* frame, the debugger's frame, and interpreter-internal containers among the
referrers. It is a last resort, not a routine probe. **VERSION-DEPENDENT (3.14.7).** Objects with no
container semantics are not GC-tracked at all, so cycles cannot involve them and
`gc.get_referrers()` will not find them; 3.14.7 shipped several "defer GC tracking" changes
(`set.intersection`, `set.difference`, `array.array`), so `gc.is_tracked()` answers can differ
**between patch releases**.

**VERSION-DEPENDENT (3.14.5) — GC model churn inside one minor version.** 3.14.0–3.14.4 shipped an
incremental collector: `gc.collect(1)` "performs an increment of collection", `set_threshold()`'s
`threshold2` was ignored, and generation 1 was removed from `gc.get_objects()`. **3.14.5 reverted
all three** to 3.13 behaviour after "reports of significant memory pressure in production
environments". Any runbook or leak test keyed on `gc.collect(1)` behaves differently on
3.14.0–3.14.4 than on 3.13 and 3.14.5+. Pin the patch version in the report (§11b).

**VERSION-DEPENDENT (3.13+, free-threaded).** Free-threaded builds add a heuristic gate: "If memory
usage has not increased by 10% since the last collection AND the net number of allocations has not
exceeded 40 times `threshold0`, the collection is not run." Leak tests that assume `threshold0`
alone triggers a collection are unreliable there.

### 5d. The `weakref` canary is the only leak detector cheap enough to leave on

**ESTABLISHED.** Hold `weakref.ref(obj)` (or `weakref.finalize(obj, callback)`) at a lifecycle
boundary and assert the referent is `None` after the owner should have died. It needs no
tracemalloc, no gc debug flags, and no external tool, and **it survives in production**.
`WeakValueDictionary` / `WeakSet` registries give the same signal for whole populations.

**Enforcement — OPEN (a project convention resting on the ESTABLISHED fact above).** This is the one
memory check that is mechanically enforceable: a unit test that creates, drops and asserts
collection (fixture shape: `python_testing_tooling_manifest.md`). The free-threaded collection gate
above makes a bare `gc.collect()` less deterministic than it looks.

### 5e. `memray`, and the native allocations nothing else sees

**VERSION-DEPENDENT (memray 1.20.0).** memray is at 1.20.0 and **runs on Linux and macOS only** —
verbatim from its PyPI page: "Memray only works on Linux and MacOS, and cannot be installed on other
platforms." It declares support for Python 3.9 through 3.15. **It therefore cannot be an
unconditional dev dependency in a cross-platform project** — put it behind an environment marker or
an optional extra (dependency-declaration mechanics: `python_module_boundaries_manifest.md`).

**VERSION-DEPENDENT (memray 1.20.0).** Subcommands: `memray run` (capture), then `flamegraph`,
`table`, `tree`, `stats`, `summary`, `parse`; `memray live` for an interactive TUI. `memray run
--native` adds C/C++ allocation frames, which is **the only way to attribute a leak inside a native
dependency**. The pytest plugin is `pytest-memray` (1.10.0), enabled with `--memray`.

---
## 6. Profiling — the 3.15 reorganisation, and when each profiler lies

### 6a. PEP 799 moves the stdlib profilers, and puts a sampler in the box

**VERSION-DEPENDENT (3.15).** PEP 799 is **Final**, `Python-Version: 3.15`, Resolution 2025-08-21.
It creates a package `profiling` containing **`profiling.tracing`** (deterministic, relocated from
`cProfile`) and **`profiling.sampling`** (statistical, new). `cProfile` "remains as an alias for
backwards compatibility." `profile` is deprecated in 3.15 and **"will be removed in Python 3.17"**,
on this exact schedule, verbatim: "In Python 3.15: importing `profile` emits a `DeprecationWarning`.
In Python 3.16: all uses of `profile` emit a `DeprecationWarning`. In Python 3.17: the module will
be removed from the standard library."

**Migration rule — VERSION-DEPENDENT (3.15).** New code imports `profiling.tracing` on 3.15+; code
that must span 3.14 and 3.15 imports `cProfile`, which is correct on both and is the alias
afterwards. Nothing should import `profile`. Release-date and support-phase facts for 3.15:
`python_platform_baseline_manifest.md`.

### 6b. Deterministic profiling (`profiling.tracing` / `cProfile`)

**ESTABLISHED.** `cProfile` and `profile` are **deterministic** profilers: "all *function call*,
*function return*, and *exception* events are monitored, and precise timings are made for the
intervals between these events". `cProfile` is the C implementation and the recommended one;
`profile` is pure Python and exists mainly for extension.

**VERSION-DEPENDENT (3.12+).** On 3.12 and later `cProfile` is implemented **on `sys.monitoring`**
and hard-codes tool id 2 (§3b). Two consequences an agent will hit: a second live `cProfile.Profile`
raises `ValueError` from `enable()`, and a `pytest --cov` run has already claimed a second id.

**ESTABLISHED.** It is **per-thread** — `sys.setprofile`'s scope. Without `threading.setprofile()`,
worker-thread time is simply absent from the profile, and the docs warn that "multiple threads
cannot be reliably profiled due to inability to detect context switches" (§8b).

### 6c. Statistical profiling (`profiling.sampling`, "Tachyon")

**VERSION-DEPENDENT (3.15).** A stdlib statistical sampling profiler now exists:
`profiling.sampling`, codenamed Tachyon, added in 3.15. It is **not** in 3.14 or any earlier
release, and as of 2026-08-08 it ships only in 3.15.0rc1. Do not put `python -m profiling.sampling`
in a runbook that targets 3.14.

**VERSION-DEPENDENT (3.15).** Four subcommands, exactly: **`run`**, **`attach`**, **`dump`**,
**`replay`**.

| Axis | Flag / value | Note |
|---|---|---|
| Sampling rate | **`-r` / `--sampling-rate`**, source default `"1khz"` | **Not** `-i`/`--interval`. Accepts `10000`, `10khz`, `10k`. Documented "up to 1,000,000 Hz" |
| Mode | `--mode {wall\|cpu\|gil\|exception}`, default `wall` | `wall` counts real elapsed time including I/O; `cpu` only active CPU execution; `gil` only time holding the GIL; `exception` samples only threads with an active exception |
| Output | `--pstats` (default, `pstats`-compatible), `--collapsed`, `--flamegraph` (self-contained HTML), `--gecko` (Firefox Profiler), `--heatmap`, `--jsonl`, `--binary` (`--compression auto\|zstd\|none`), `--diff-flamegraph BASELINE`, `--live` | `--diff-flamegraph` is the regression instrument: profile the baseline, profile the change, diff |
| Other | `-d/--duration`, `-a/--all-threads`, `--native`, `--no-gc`, `--opcodes`, `--subprocesses`, `--blocking`, `--realtime-stats`, `--async-aware`, `--async-mode {running\|all}`, `-o/--output`, `--browser`, `--sort`, `-l/--limit`, `--no-summary` | `--async-aware` is what makes `dump` useful on a hung asyncio app (§4d) |

**VERSION-DEPENDENT (3.15).** It samples **externally**: "The target process requires no
modification and need not be restarted", and overhead on the target is "virtually zero". It requires
the same debugger-level OS permissions as PEP 768 attach (§2b), and it carries the same version
coupling — profiler and target must share the same Python **minor** version, pre-release versions
must match **exactly**, and **a free-threaded build cannot attach to a standard build or vice
versa** (§9c).

### 6d. Native frames: `-X perf`, `-X perf_jit`, and PEP 831

**VERSION-DEPENDENT (3.12+).** `-X perf` enables the Linux perf trampoline so "the `perf` profiler
will be able to report Python calls". Equivalent env var `PYTHONPERFSUPPORT=1`. Programmatic
control: `sys.activate_stack_trampoline("perf")` / `sys.deactivate_stack_trampoline()` /
`sys.is_stack_trampoline_active()`, all added in 3.12, **Linux only**. Precedence: the `sys`
functions beat `-X`, which beats the env var. Default is off.

**ESTABLISHED.** The mechanism has a cost and a distortion: the trampoline interposes "a small piece
of code compiled on the fly before the execution of every Python function" and teaches perf the
mapping via perf map files. It is not free while active, and **it changes the shape of native
stacks** — so a native profile taken with the trampoline is not the native profile of the shipped
process.

**ESTABLISHED.** `-X perf` requires a frame-pointer build: verify with `python -m sysconfig | grep
'no-omit-frame-pointer'` and `python -m sysconfig | grep HAVE_PERF_TRAMPOLINE`, and build with
`CFLAGS="-fno-omit-frame-pointer -mno-omit-leaf-frame-pointer"`.

**VERSION-DEPENDENT (3.13+).** `-X perf_jit` (env `PYTHON_PERF_JIT_SUPPORT`) is the DWARF variant
for non-frame-pointer builds. It writes `/tmp/perf-$PID.dump` and needs a two-step pipeline — `perf
record -F 9999 -g -k 1 --call-graph dwarf`, then `perf inject --jit`, then `perf report` — has
"Higher overhead", needs `perf > v6.8` (or v6.7.2+), and for `-O0` builds needs `--call-graph
dwarf,65528` (default 8192).

**VERSION-DEPENDENT (3.15).** PEP 831 ("Frame Pointers Everywhere") is **Final**, `Python-Version:
3.15`: CPython is built with `-fno-omit-frame-pointer -mno-omit-leaf-frame-pointer` **by default**
on supporting platforms, and exposes them through `sysconfig` so extension modules inherit them. The
PEP's own warning is the operationally important part: **"A single native component built without
frame pointers can break stack unwinding for the whole Python process."** One badly built wheel
invalidates every native profile in the process.

### 6e. Third-party samplers, and the version lag that breaks runbooks

**VERSION-DEPENDENT as tagged.** The ecosystem has not caught up with 3.15, which is a scheduling
fact a runbook must encode rather than discover.

| Tool | Version (date) | Declares support for | Sharp edge |
|---|---|---|---|
| py-spy | 0.4.2 (2026-04-24) | CPython 2.3–2.7 and 3.3–**3.14**; does **not** claim 3.15 | `record -o profile.svg --pid PID`, `top --pid PID`, `dump --pid PID` (`--locals`); flags `--native`, `--subprocesses`, `--gil`, `--idle`, `--nonblocking`. On Linux, attaching to a non-child "will usually require root"; fix via `ptrace_scope`, `--cap-add SYS_PTRACE` (Docker), or a `SYS_PTRACE` capability (Kubernetes **drops it by default**) |
| austin | 4.0.0 (2025-11-01), PyPI dist **`austin-dist`** | 3.9–**3.14**; not 3.15 | `-i/--interval=n_us`, `-c/--cpu`, `-C/--children`, `-m/--memory` (byte delta between samples), `-w/--where=PID`, `-x/--exposure=n_sec`, `-P/--pipe`, `-o/--output`. **MOJO binary output is the default in 4.0**, so naive consumers of the old text format break. The `austinp` variant (Linux, `-DAUSTINP`) uses `ptrace` + `libunwind` for native frames |
| Scalene | 2.3.0 (2026-05-12) | `requires_python = "!=3.11.0,>=3.8"` — excludes 3.11.0 exactly | — |
| pyinstrument | 5.1.3 (2026-07-29) | — | — |

### 6f. When each profiler lies

**This is the section to read before quoting a number.** Each row is a documented property, not a
suspicion.

| Instrument | How it lies | Tag |
|---|---|---|
| Deterministic (`profiling.tracing` / `cProfile`) | It monitors **every** call, return and exception with precise interval timings, so its overhead is proportional to **call count**. Call-heavy code is inflated relative to loop-heavy code doing the same work: the profiler distorts exactly the property it is measuring. No primary source quantifies the factor — measure your own workload before believing a ranking of small functions | ESTABLISHED mechanism; OPEN magnitude |
| Deterministic, threads | Per-thread scope: worker-thread time is **absent**, not small, without `threading.setprofile()`; and "multiple threads cannot be reliably profiled due to inability to detect context switches" | ESTABLISHED |
| Statistical (Tachyon, py-spy, austin) | Numbers are estimates, stated verbatim: "The time values shown in Tachyon's output are **estimates derived from sample counts**, not direct measurements... With 100,000 samples, a function showing 5% has a margin of error of roughly plus/minus 0.5%. With only 1,000 samples, the same 5% measurement could actually represent anywhere from 3% to 7%." **Short-lived functions can be missed entirely** | VERSION-DEPENDENT (3.15) |
| Statistical, mode confusion | `--mode wall` includes I/O wait; `--mode cpu` excludes it; `--mode gil` counts only GIL-held time. A "hot" function under one mode can be invisible under another, and a `gil`-mode conclusion is void if the GIL was silently re-enabled (§9c) | VERSION-DEPENDENT (3.15) |
| Native (`perf` without the trampoline) | Python functions simply do not appear; the profile attributes everything to the eval loop. With the trampoline they appear, but the native stack shape has changed | ESTABLISHED |
| Native, frame pointers | Without frame pointers the interpreter "may not be able to show Python functions in the output of `perf`", and one native component built without them "can break stack unwinding for the whole Python process" | VERSION-DEPENDENT (3.15 for defaults) |
| Native, JIT build | `sys.activate_stack_trampoline()` "Cannot be activated if JIT is active" — `-X perf` is **not** a way to profile a JIT build; and on 3.13/3.14 JIT builds, native profilers and debuggers cannot unwind through JIT frames at all (§9a) | VERSION-DEPENDENT (3.12+) |
| Any profiler, wrong build | A debug build changes the allocator (debug hooks), the default warning filters (empty), and frozen-module state (off in debug builds, on in release) — so both runtime and import cost differ from the shipped artefact | ESTABLISHED |

**The rule that follows — OPEN (project policy, but strongly recommended).** A performance claim is
admissible only if it names the interpreter version, the build variant (free-threaded or not, JIT on
or off, tail-call or not, pydebug or release), the instrument, and the mode. §9d states the same
rule from the build side; §11b puts it in the report.

---

## 7. Development-time switches — what each one actually turns on

The **inventory** of `-X` options and `PYTHON*` variables, with version-added stamps, belongs to
`python_platform_baseline_manifest.md`. This section states only the *diagnostic behaviour* an agent
gets wrong: what a switch enables, and — more often the defect — what it silently does not.

### 7a. `-X dev` / `PYTHONDEVMODE` — what it does **not** do, and why that is a diagnostics fact

**The effect list is not restated here.** `python_platform_baseline_manifest.md` §6b owns what
Development Mode enables and what it does not, with the version stamps — it is the
interpreter-switch
inventory this file cedes in its scope block. This section states only the residue that changes what
an agent does during an incident.

**Two non-effects are documented verbatim, two follow from the effect list being closed —
ESTABLISHED.** The docs state that dev mode "does not enable the `tracemalloc` module by default,
because the overhead cost (to performance and memory) would be too large", and that it "does not
prevent the `-O` command line option from removing `assert` statements nor from setting `__debug__`
to
`False`". The other two are absences from that list rather than sentences in it, and both are live
agent errors: dev mode does not enable `-X importtime` or `-X showrefcount` (§7c), and it does not
turn warnings into errors — it installs the `default` filter, and only `-W error` makes a warning
fatal (§7b).

**Why each matters here.** The `tracemalloc` non-effect means the allocation traceback a
`ResourceWarning` asks for still has to be armed in advance (§5b) — dev mode makes the warning
visible and leaves it unattributable. The `-O` non-effect's consequence for invariants is owned by
`error_tracing_contract_manifest.md` §14; this file notes only the diagnostics half: an invariant
that must hold in production cannot be an `assert`, and §10b's `sanity-check` row names the
mechanism that replaces it.

**ESTABLISHED.** `-X dev` "can only be enabled at the Python startup"; there is no runtime toggle.
Read it back with `sys.flags.dev_mode` — which is why it belongs in the failure report (§11b). Where
the allocator hooks are too slow to leave on, `PYTHONMALLOC=default` keeps the rest of dev mode; the
hub records that escape with the effect list.

### 7b. Warnings: visible is not the same as fatal

**ESTABLISHED.** `-W` takes `action:message:category:module:lineno`. Actions: `default`, `error`,
`always`, `all` (same as `always`), `module`, `once`, `ignore`; they may be abbreviated (`-Wi` ==
`-Wignore`). `message` must match the **whole** message, case-**insensitively**; `module` matches
the fully qualified module name, case-**sensitively**; `lineno` 0 matches all lines. Empty fields
match everything and trailing empty fields may be omitted.

**ESTABLISHED — two precedence traps.** With multiple `-W` options, "the action for the **last**
matching option is performed" — the opposite of first-match-wins intuition. And **"Invalid `-W`
options are ignored"**: a typo produces no error, only a note printed when the first warning is
issued. `PYTHONWARNINGS` is a comma-separated list with "filters later in the list taking precedence
over those earlier in the list".

**ESTABLISHED.** `-W error` is the switch that converts a warning into a failure; `-X dev` only
makes the warning *visible*. A suite that wants a `DeprecationWarning` to fail the build needs `-W
error` or a pytest `filterwarnings = error` setting — owned by `python_testing_tooling_manifest.md`,
gated in CI by `python_quality_gates_manifest.md`.

### 7c. Import cost, refcounts, verbosity

**VERSION-DEPENDENT (3.14).** `-X importtime` prints module name, cumulative time and self time.
**`-X importtime=2`, new in 3.14, also reports already-loaded modules, printing the literal string
`cached` in both time columns**; values other than `1` and `2` are reserved. Env equivalent
`PYTHONPROFILEIMPORTTIME=1|2`. Two caveats: a parser expecting floats **crashes** on `cached`, and
the documented limitation is that "its output may be broken in multi-threaded application".

**VERSION-DEPENDENT (3.4+, debug build only).** `-X showrefcount` "only works on debug builds"
(`--with-pydebug`). On a normal interpreter the option is **accepted and silently does nothing**. A
debug build also adds `sys.gettotalrefcount()`, `d` to `sys.abiflags`, `-d`/`PYTHONDEBUG`,
`__lltrace__`, and `Py_DEBUG`/`Py_REF_DEBUG`.

**ESTABLISHED.** `PYTHONVERBOSE` / `-v` prints a message each time a module is initialised, with the
file it loaded from; **`-vv`** additionally prints a message for every file *checked* during the
search and reports module cleanup at exit. This is the instrument for "why is it importing *that*",
which `-X importtime` cannot answer.

**VERSION-DEPENDENT (3.13, debug build only).** `-X presite=package.module` / `PYTHON_PRESITE`
imports a module before `site` and before `__main__` exists — the earliest diagnostics hook — but
**requires `--with-pydebug`**; on a release interpreter the option does not exist, so the earliest
practical hook is the application entry point, which is where §11c arms.

### 7d. Switches that silently degrade diagnosability

**VERSION-DEPENDENT (3.11+).** `-X no_debug_ranges` strips the end-line and column tables from code
objects, which removes the `^^^^` fine-grained carets from **every future traceback**. Adopting it
to shrink `.pyc` files is a permanent diagnosability trade, usually made without realising it.
**OPEN — pack conflict on the env-var spelling.** The two fact packs for this pass record it
differently (`PYTHONNODEBUGRANGES` in one, `PYTHON_NODEBUGRANGES` in the other). The `-X` form is
agreed; verify the environment-variable spelling against `using/cmdline.html` before putting it in a
deployment config, and note that an unknown `PYTHON*` variable, like an unknown `-X` name, fails
silently.

---
## 8. Instruments of last resort — audit hooks and trace functions

### 8a. Audit hooks (PEP 578): one-way, unremovable, and not a sandbox

**ESTABLISHED.** PEP 578 ("Runtime Audit Hooks") is **Final**, `Python-Version: 3.8`. API:
`sys.audit(event, *args)`, `sys.addaudithook(hook)`, C-level `PySys_Audit()` and
`PySys_AddAuditHook()`, plus the open hook `io.open_code(path)` / `PyFile_OpenCode()` /
`PyFile_SetOpenCodeHook()`. The full event catalogue is `library/audit_events.html`.

**ESTABLISHED.** Five properties decide whether a hook is the right instrument:

1. **"Hooks cannot be removed or replaced."** There is no `removeaudithook`. An audit hook is a
   one-way, process-lifetime commitment.
2. **Scope differs by registration path.** C hooks added via `PySys_AddAuditHook()` are **global**
   and run first; Python hooks added via `sys.addaudithook()` are **per-(sub)interpreter**.
3. **A raising hook takes the process with it.** An exception raised in a hook is re-raised by
   `sys.audit()`, "later hooks are ignored", and "in general the Python runtime should terminate". A
   raising hook *does* block the audited operation — at the cost of an unrecoverable process, not a
   clean refusal.
4. **It is not a sandbox.** PEP 578: "This is not sandboxing, as this proposal does not attempt to
   prevent malicious behavior." The `sys` docs add that hooks added from Python "can be trivially
   disable[d] or bypass[ed]" by malicious code; security-relevant hooks must be installed via the C
   API **before runtime initialisation**, and modules permitting arbitrary memory modification
   (`ctypes`) must be removed or watched. Using `sys.addaudithook()` as a security control is the
   canonical misuse.
5. **Installation can fail silently.** "If existing hooks raise `RuntimeError`, new hook is NOT
   added and exception is suppressed", so "Callers cannot assume hook was added" — VERSION-DEPENDENT
   (3.8.1+): since 3.8.1 non-`RuntimeError` exceptions are no longer suppressed.

**ESTABLISHED.** Cost: with no hooks installed, PEP 578 reports "the vast majority of benchmarks
showing between 1.05x faster to 1.05x slower" — inside noise. The cost of a *registered* hook is
paid on **every** audited event, and `object.__getattr__`, `import` and `open` are hot.

**Verdict at this scale — OPEN (project decision).** The legitimate uses are narrow and specific:
detecting injected debugging via `cpython.remote_debugger_script` (§2d), and recording which files
or sockets a process actually touched during a hard-to-reproduce run. Both are *investigative*,
bounded-run uses. A permanently installed audit hook in a small application is over-engineering with
an unremovable failure mode; `logging` plus §11's report carries the same information at a fraction
of the risk.

### 8b. `sys.settrace` vs `sys.setprofile`: disjoint event sets, asymmetric semantics

**ESTABLISHED.** The event sets do not overlap the way the names suggest. `sys.settrace(tracefunc)`
events are `'call'`, `'line'`, `'return'`, `'exception'`, `'opcode'`. **It never receives
`'c_call'`, `'c_return'`, `'c_exception'`** — those go only to `sys.setprofile()`. Conversely
`setprofile` never receives `'line'`. Choosing the wrong one produces a tool that is quietly blind
to half of what it claims to measure.

**ESTABLISHED.** Return values are load-bearing for one and ignored by the other: the trace
function's return value becomes the **local trace function for the new scope** (`None` disables
tracing for it), whereas the profile function's return "is ignored". **Accidentally returning `None`
from a trace function silently drops all further events in that frame** — the single most common bug
in a hand-rolled tracer.

**VERSION-DEPENDENT (3.7+).** Per-frame throttles: `frame.f_trace_lines = False` suppresses `'line'`
events, and `frame.f_trace_opcodes = True` is **required** to get `'opcode'` events at all.

**ESTABLISHED.** Both are **per-thread**: `threading.settrace()` / `threading.setprofile()` install
a function for threads created *afterwards*, and `sys.settrace()` in the main thread does not reach
existing workers. Both carry a CPython implementation-detail note — "intended only for implementing
debuggers, profilers, coverage tools and the like" — raise the audit events `sys.settrace` /
`sys.setprofile`, and disable recursive tracing while the trace function runs (`sys.call_tracing()`
to trace deliberately).

**VERSION-DEPENDENT (3.12+).** For any new tool, use `sys.monitoring` (§3): `settrace` cannot be
scoped to a subset of events or code objects, so it de-optimises the whole thread. And whatever
installs a tracer must remove it: a tracer left installed in production is an unbounded, invisible
slowdown (see Anti-patterns).

**ESTABLISHED.** `sys._getframe([depth])` is documented as "For internal and specialized purposes
only", is "Not guaranteed to exist in all Python implementations", raises `ValueError` past the
stack bottom, and raises the audit event `sys._getframe`; `sys._getframemodulename()` was added in
3.12 — VERSION-DEPENDENT (3.12+). Frame walking is legitimate inside a diagnostic module and nowhere
else.

---

## 9. Diagnosability under a JIT, tail-call, or free-threaded build

### 9a. JIT

**VERSION-DEPENDENT (3.13–3.16).** The JIT is still **opt-in at build time** on 3.15 and on `main`:
`--enable-experimental-jit=[no|yes|yes-off|interpreter]`, and "`--enable-experimental-jit=no` is the
default behavior if the option is not provided". Runtime override is `PYTHON_JIT=0|1` (`yes-off`
builds it but starts disabled). PEP 744 remains **Draft** and says the JIT "is likely to remain
[disabled by default] for the foreseeable future". **Do not attribute observed behaviour to the JIT
without checking `PYTHON_JIT` and the build.**

**VERSION-DEPENDENT (3.13+).** Python-level observability is explicitly preserved. PEP 744: "Tools
that profile and debug Python code will continue to work fine. This includes in-process tools that
use Python-provided functionality (like `sys.monitoring`, `sys.settrace`, or `sys.setprofile`)" and
"The behavior of Python code should be completely unchanged."

**VERSION-DEPENDENT (3.13, 3.14).** Native observability is not: **"Profilers and debuggers for C
code are currently unable to trace back through JIT frames."** On a 3.13/3.14 JIT build, `perf`,
`gdb` backtraces and native crash handlers stop at generated code.

**VERSION-DEPENDENT (3.15).** 3.15 fixes that **partially**: "The JIT compiler now publishes unwind
information for generated machine code to the GDB interface on supported Linux ELF platforms. When
libgcc frame registration is available, the same unwind information is also registered for GNU
`backtrace()` stack walkers." Read the scope literally — Linux ELF, GDB and `backtrace()`. It is
**not** a blanket promise for `perf`, macOS, or Windows.

**VERSION-DEPENDENT (3.12+).** Hard incompatibility: `sys.activate_stack_trampoline()` "Cannot be
activated if JIT is active." `-X perf` and the JIT are mutually exclusive.

### 9b. Tail-call interpreter

**VERSION-DEPENDENT (3.14).** A separate, orthogonal axis: `--with-tail-call-interp`, added 3.14,
opt-in, needing a compiler with proper tail calls and the `preserve_none` calling convention (Clang
19+), PGO "highly recommended". The whatsnew calls it "an internal implementation detail with no
visible behavior changes" — true at the Python level, false at the native level.

**VERSION-DEPENDENT (3.15).** In 3.15 it stops being hypothetical: **"the official Windows 64-bit
binaries on python.org now use" the tail-calling interpreter** (a Visual Studio 2026 / MSVC 18
feature). Native stack shapes and disassembly on the *stock* Windows build differ between 3.14 and
3.15 with no source change and no flag on your side.

### 9c. Free-threaded builds

**VERSION-DEPENDENT (3.13+).** Detect the build with `sysconfig.get_config_var("Py_GIL_DISABLED") ==
1` — the docs call this "the recommended mechanism for decisions related to the build configuration"
— and the runtime state with `sys._is_gil_enabled()`. `python -VV` and `sys.version` contain the
string "free-threading build"; `sys.abiflags` gains `t`.

**VERSION-DEPENDENT (3.13+) — the GIL can come back without you asking.** "The GIL may also
automatically be enabled when importing a C-API extension module that is not explicitly marked as
supporting free threading. A warning will be printed in this case." A "free-threaded" deployment can
therefore be running **with the GIL on**, which invalidates any `--mode gil` profiling conclusion
(§6f). Force with `-X gil=0|1` / `PYTHON_GIL`, where `-X gil` takes precedence.

**VERSION-DEPENDENT (3.13+, free-threaded) — the sharpest diagnostics footgun, verbatim: "It is not
safe to access `frame.f_locals` from a frame object if that frame is currently executing in another
thread, and doing so may crash the interpreter."** This is exactly what a naive
`sys._current_frames()` + `f_locals` dumper does, and exactly what `py-spy dump --locals` asks for.
**Rule: a thread dump renders `traceback.format_stack(frame)` and nothing else** unless the target
build is known to have the GIL enabled.

**VERSION-DEPENDENT (3.13+, free-threaded).** Also documented as not thread-safe: "it is generally
not thread-safe to access the same iterator object from multiple threads concurrently, and threads
may see duplicate or missing elements" — a source of phantom bugs that present as data corruption
rather than as a concurrency error, and therefore get misdiagnosed. Concurrency semantics and the
safe patterns: `python_concurrency_determinism_manifest.md`.

**VERSION-DEPENDENT (3.14, 3.15).** Free-threaded builds add thread-local bytecode, `-X tlbc=[0|1]`
/ `PYTHON_TLBC`, which appears in `--help-xoptions` only under `#ifdef Py_GIL_DISABLED` and is
**undocumented in the 3.14 branch's `Doc/using/cmdline.rst`**, documented only on `main`. Because
each thread can hold its own copy of a code object's bytecode, **a tool that keys on code-object
identity or instruction offsets is wrong under free threading** unless it is `co_tlbc` /
`tlbc_index` aware — the debug-offsets header exposes `_Py_Debug_code_object_co_tlbc` and
`_Py_Debug_interpreter_frame_tlbc_index` for precisely this.

**VERSION-DEPENDENT (3.14).** `faulthandler` dumps only the current thread (§4a).
**VERSION-DEPENDENT (3.13+).** `PYTHONMALLOC` values are restricted, and `--without-mimalloc`
"Cannot be used with `--disable-gil`" (§5c). **VERSION-DEPENDENT (3.15).** An out-of-process sampler
cannot cross the build boundary in either direction (§6c).

**VERSION-DEPENDENT (3.14).** Single-threaded cost is stated in the 3.14 whatsnew as "roughly 5-10%
depending on platform and C compiler" — always quote the platform, never a bare number, and never
use a free-threaded profile to justify an optimisation on a GIL build.

### 9d. The rule: a performance or concurrency claim must name the build

**OPEN — project policy, and the one rule in this file worth enforcing mechanically.** Four axes
vary independently and each changes what an instrument can see: interpreter minor version, GIL vs
free-threaded, JIT off/on, tail-call vs computed-goto, and release vs pydebug. **Enforcement
route:** emit the identity block of §11a into every benchmark artefact and every failure report, and
have the report renderer refuse to produce output without it. Nothing in the language enforces this
— it is a fitness function the project writes, and `python_quality_gates_manifest.md` owns where it
runs.

---

## 10. Designing for diagnosis

This is the architectural half of the file: what must exist in the *application* for §§1–9 to have
anything to read. Vocabulary is imported from the SWE design/architecture corpus; every element id
below was verified present in `elements.json` by the seed pack for this pass, and every naming work
is recorded **as the corpus records it**, including where the corpus's own record is unverified
(full bibliography and verification status: Sources → "Named vocabulary").

### 10a. The claim: testability tactics and diagnosability tactics are one family

**Named vocabulary — ESTABLISHED-with-citation.** Bass, Clements & Kazman, *Software Architecture in
Practice*, 4th ed., 2021 (verified) file `specialized-interfaces`, `record-playback`,
`localize-state-storage`, `abstract-data-sources`, `sandbox` and `executable-assertions` under the
category `bck-cat:control-and-observe-system-state` — **testability** tactics. Read as diagnostics
they are this section's spine: a separated diagnostic surface that can be removed,
capture-and-replay of the fault-inducing state, one place to dump state from, swappable data
sources, and in-code oracles.

**The claim — OPEN (this file's synthesis over the cited BCK categorisation):** testability tactics
and diagnosability tactics are one family, differing only in whether the observer is a test or an
operator. The consequence is practical — `python_testing_tooling_manifest.md`'s seams (injected
clock, injected seed, injected data source) *are* the diagnosability seams, so a codebase that
already has them is diagnosable almost for free. One further BCK reframing matters:
`executable-assertions` is filed under **observability**, not correctness — "so the program flags
when and where it enters a faulty state" — which is the bridge from
`error_tracing_contract_manifest.md` §14 into this file.

### 10b. The nine mechanisms, their Python form, and whether to bother

**Tag per row as marked.** "Worth it?" is a judgement about a small-to-mid single-process app, per
PLAN house rule 11; where a mechanism's home is distributed systems the row says so plainly.

| Element (id) | Naming work, as the corpus records it | Python mechanism | Worth it at this scale? |
|---|---|---|---|
| `built-in-self-test` | Corpus `named_in` is a Wikipedia page (a data defect); cite **IEC 61508-7:2010**, the technique catalogue (verified) | `selfcheck()` behind `app --self-test`: dependency presence and version agreement via `importlib.metadata.version`, bundled-data checksums via `hashlib.file_digest` (3.11+), serializer round-trip, short-timeout probe of each configured endpoint, config-schema-versus-code agreement. Fast form at startup, full form on demand | **Yes, reduced.** The highest-value single check is version agreement with native dependencies, because that failure is otherwise diagnosed as a mysterious segfault (§4a). **How far to go is OPEN** — no authoritative bar was found. Established content: only what cannot be checked statically and would otherwise fail late — importability, path writability, endpoint reachability, schema agreement. It is **not** a substitute for tests; it converts a mid-run failure into a startup failure |
| `maintenance-interface` + `specialized-interfaces` | Hanmer, *Patterns for Fault Tolerant Software* (**UNVERIFIED**); Bass, Clements & Kazman 2021 (verified) — "clearly separated from functional interfaces so they can be removed" | One `_diagnostics.py` holding explicit `dump_state()` / `reset()` / `set_verbosity()`, reached by an `app diag ...` subcommand group and, on POSIX, `SIGUSR1`. Not scattered `print` calls, and not endpoints bolted onto the service path | **Yes, as a CLI group plus a signal.** Hanmer's argument for a separate channel: mixing management traffic with application traffic obscures both and blocks maintenance exactly when the service path is broken. A loopback socket REPL earns its place only in a service that cannot be restarted to be inspected. **Shape is OPEN**; `health-check-api`, `log-aggregation` and `distributed-tracing` (Richardson 2018, verified) are microservice-shaped and are over-engineering here — the same conclusion `logging_observability_manifest.md` reaches from the emission side |
| `sanity-check` | Douglass, *Real-Time Design Patterns* etc. (author corpus, verified) — "gross faults are cheap to catch" | A plausibility check on computed output that **survives `-O`**: `if not (0.0 <= p <= 1.0): raise ImplausibleResult(...)`, counted and logged at WARNING. **ESTABLISHED:** `-O` strips `assert` and sets `__debug__` false, and `-X dev` does not prevent it (§7a) | **Yes, always** — three lines. It is the *only* first instrument for the "wrong answer, nothing raised" row of §1b; without it that row has no entry point at all. Assertion policy itself: `error_tracing_contract_manifest.md` §14 |
| `correcting-audits` | Hanmer (**UNVERIFIED**) | An `app verify [--repair]` command that scans persisted state for structural violations — orphan rows, missing blobs, checksum mismatch — and repairs or reports | **Yes if the app owns state that outlives a process; no if stateless.** Use `zlib.crc32`/`hashlib` *inside* the audit as the integrity step; do **not** import `cyclic-redundancy-check` as a fault-detection tactic — that is embedded-domain vocabulary |
| `watchdog` (local), not `heartbeat` (across a link) | Douglass (verified) and Koopman, *Better Embedded System Software*, 2010 (verified) for the watchdog; Hanmer (**UNVERIFIED**) for `heartbeat`, with the `heartbeat-tactic` twin in BCK 2021 (verified) | Cheapest first: re-call `faulthandler.dump_traceback_later(t, repeat=True)` at the top of each loop iteration (zero dependencies, dumps every thread at the stall — §4b); a `last_progress = time.monotonic()` stamp checked by a supervisor thread, which is the only form that distinguishes "running but not progressing" from "slow"; or systemd `Type=notify` + `WatchdogSec` with `sd_notify("WATCHDOG=1")` | **Yes for a long-running loop, in the local form.** The corpus edge `watchdog -alternative-to-> heartbeat` [sourced: Hanmer] gives the selection rule: "watchdog is local, heartbeat is across a link" — the ping/echo form presupposes network peers and is out of scale. `heartbeat -uses-> timeout` [editorial]: liveness is a timeout window, so a beat not seen before it expires counts as missed. Deployment details are OPEN (not Python facts) |
| `safe-state`, with `abort` / `degradation` / `two-phase-termination` | ISO 26262:2018 (verified) for `safe-state`; BCK 2021 (verified) for `abort` ("terminate before damage") and `degradation` ("maintain the most critical system functions while dropping … less critical ones"); Grand, *Patterns in Java v1*, 1998 (verified) for `two-phase-termination` | A *named, reachable* state entered on fault detection: refuse to start on bad config with a distinct exit code (`os.EX_CONFIG`), flip to read-only, disable the failing feature flag, park background workers, cooperative shutdown via a `threading.Event` observed at safe points. **Not "an unhandled traceback"** | **Yes, nearly free** — the work is *naming* the states and the exit codes. The diagnosability payoff is direct: a distinct exit code plus one ERROR record is an artefact; a traceback on the stderr of a container that has already been replaced is not |
| `quarantine` | Hanmer (**UNVERIFIED**) | After repeated failures, disable the plugin/endpoint/worker and keep serving the rest: mark a failed `importlib.metadata` entry point as skipped, stop scheduling a task, route its inputs to the rejects sink | **Yes where a plugin seam exists** (seam mechanics: `python_module_boundaries_manifest.md`); otherwise machinery without a subject. Ordering rule from `quarantine -composes-with-> restart` [editorial]: **fence off the faulty unit first, then restart it** — an agent will otherwise get this backwards. The failure-rate gate that decides *when* (`leaky-bucket-counter`, `riding-over-transients`) and the rejects sink itself (`marked-data`) belong to `error_tracing_contract_manifest.md` |
| `software-rejuvenation` | Huang, Kintala, Kolettis & Fulton, 1995 (**UNVERIFIED**); the standards-grade twin is BCK's `removal-from-service` (verified) | gunicorn/uvicorn `--max-requests` + `--max-requests-jitter`, systemd `RuntimeMaxSec=`, or a scheduled restart | **Configure it in the process manager if the process is long-running; never in application code.** State it as what it is: **a concession to a leak you have not found.** `software-rejuvenation -alternative-to-> let-it-crash` [editorial] frames the choice as proactive restart before aging fails versus reactive crash-and-restart after. Its obligatory partner `steady-state` (Nygard, **UNVERIFIED**) — a purge for every accumulator — is owned by `logging_observability_manifest.md`. Adopted without `steady-state` and without §5's hunt, it converts a diagnosable leak into an invisible one: the restart hides the evidence. Treat every rejuvenation interval as an open leak ticket |
| `record-playback` | Bass, Clements & Kazman 2021 (verified) — "Record information as it crosses interfaces and use the recorded state to 'play the system back'" | Capture inputs at the **shell** boundary (the imperative shell is by construction the only place non-deterministic input enters) behind `--record`, replay with `--replay`; `vcrpy` or `responses` for HTTP; promote a captured payload into a pytest regression fixture | **Yes for any non-trivial input format — the highest-value item in §10.** It is the only answer to the "cannot reproduce" row of §1b, and the only mechanism here whose absence cannot be remedied after the failure: everything else explains a failure you are watching, this one lets you *re-run* one you were not. Cost is proportional to how clean the functional-core/imperative-shell seam already is (`architecture_manifest_default.md` owns the seam rationale) |

### 10c. Three ordering rules the corpus states and an agent will otherwise invert

**Named vocabulary — provenance marked per edge: [sourced] carries a citation in the corpus, while
[editorial] is the corpus's own note and is therefore OPEN as a claim.**

- **Arm the dump before adopting let-it-crash.** `core-dump -composes-with-> let-it-crash`
  [editorial]: capture the dump *as* the unit crashes, before the supervisor recreates it.
  `faulthandler` must be on before the first crash, not after it (§4a, §11c).
- **A self-test without a defined refusal is decoration.** `built-in-self-test -composes-with->
  safe-state` [editorial]: on self-test failure the process enters its safe state rather than
  logging and continuing.
- **Watchdog and sanity check are not substitutes.** `watchdog -composes-with-> sanity-check`
  [editorial]: the watchdog catches hangs (liveness), the sanity check catches implausible outputs
  (correctness) — complementary fault classes, so covering one leaves the other open.

**Do not build a supervision tree — OPEN (scale judgement, PLAN house rule 11).** The corpus
elements `supervisor`, `supervision-tree-otp`, `restart` and `monitor` describe the **process
manager** — systemd, the container orchestrator, the WSGI worker manager — not application code; a
hand-rolled Python supervision tree is a second, untested scheduler. The `let-it-crash` disposition
that pairs with them (Candea & Fox, *Crash-Only Software*, 2003, verified; Kuhn, Hanafee & Allen
2017, verified; Nygard **UNVERIFIED**) is owned by `error_tracing_contract_manifest.md`. Two further
elements are deliberately **not** imported: `dead-letter-channel` presupposes a broker and
`retry-budget` presupposes many clients retrying one backend — both are distributed-systems
machinery at the wrong scale.
---

## 11. The reproducibility contract

**Named vocabulary.** The organising element is `core-dump` (design/error-handling). Its corpus
`named_in` field is a data defect (the bare work id `white`), so cite the covering works its record
carries: White, *Making Embedded Systems: Design Patterns for Great Software*, 2nd ed., 2024
(verified) and the Free Software Foundation, *Debugging with GDB*, Tenth Edition (verified). The
corpus edge `core-dump -enables-> maintenance-interface` [editorial] states the relationship this
file implements: the dump is the payload the diagnostic channel retrieves. The corpus's own note on
that edge records a gap — there is **no** more specific post-mortem-diagnostics architecture element
(no "flight recorder" / "black box"), so the shape of a crash-report artefact is OPEN and this
section is a project convention built on established mechanisms, not an imported pattern.

### 11a. The four recoverables

**ESTABLISHED.** A failure is reproducible from artefacts alone only when four things are
recoverable **without the developer's machine**. Each is a mechanically dumpable fact, and dumping
all four at startup is cheap.

| Recoverable | Mechanical source | Tag |
|---|---|---|
| **(a) The exact interpreter and build** | `sys.version`, `sys.implementation`, `sysconfig.get_config_var("Py_GIL_DISABLED")`, `sys._is_gil_enabled()`, whether the JIT was on (`PYTHON_JIT` and the build), whether it was a tail-call build | VERSION-DEPENDENT (3.13+ for the GIL calls) |
| **(b) The resolved configuration and behaviour-changing environment** | the effective config object, plus `sys._xoptions` for `-X` options and `sys.flags.dev_mode` for dev mode | ESTABLISHED |
| **(c) The inputs, by content hash** | `hashlib.file_digest` (3.11+) over each input artefact, plus the captured payload of §10b's `record-playback` row | VERSION-DEPENDENT (3.11+) |
| **(d) A stack** | the exception and its chain for a raised failure; a `faulthandler` dump for a fatal signal; `sys._current_frames()` for a hang | ESTABLISHED |

**ESTABLISHED — determinism inputs that belong in (b).** `PYTHONHASHSEED` (an integer 0–4294967295,
`0` disables randomisation) and, VERSION-DEPENDENT (3.13), `-X cpu_count=n` / `PYTHON_CPU_COUNT`
(which overrides `os.cpu_count()` and `os.process_cpu_count()`) change program behaviour without
changing the source, so a report that omits them cannot explain a difference between two runs. **The
obligation to inject the seed and the clock rather than reading them ambiently is not restated
here:** `python_testing_tooling_manifest.md` owns the injection seams, and
`python_concurrency_determinism_manifest.md` owns keeping concurrent code deterministic under test.
This file states only that whatever those files inject must appear in the report.

### 11b. What a failure report must carry

**OPEN — this is the project's convention; every field below is an established mechanism, the *set*
is a decision.** Minimum contents, in the order that makes triage fastest:

1. **Correlation id** — one value shared by every record for this unit of work. The transport
   (`contextvars` filter or `structlog.contextvars`) and the naming (`correlation-identifier`; Hohpe
   & Woolf, *Enterprise Integration Patterns*, 2003, verified) are owned by
   `logging_observability_manifest.md`; this file requires only that the id appears in the crash
   artefact as well as in the log stream, or the two cannot be joined.
2. **Interpreter and build identity block** — §11a(a), verbatim strings, not a parsed summary.
3. **Behaviour-changing flags** — §11a(b): `sys._xoptions`, `sys.flags.dev_mode`, `PYTHONHASHSEED`,
   the patch version (§5c: `gc.collect(1)` semantics moved inside the 3.14 line).
4. **The exception, its `__cause__` chain and its `__notes__`** — format owned by
   `error_tracing_contract_manifest.md`; this file requires that the exception *object* be retained
   where post-mortem is possible (§4g), not only its rendered text.
5. **Input identity** — §11a(c): content hashes, plus a pointer to the captured replay payload
   (§10b `record-playback`).
6. **A stack for every thread** — §11a(d).
7. **Resource state at failure** — `gc.get_count()`, `gc.get_stats()`, and
   `tracemalloc.get_traced_memory()` if tracing was on. Cheap, and it separates "leak" from "spike"
   immediately.

**Enforcement — OPEN, and say it plainly.** Nothing in Python enforces this list. The only
mechanical routes are (i) a single `build_failure_report()` function that all four
unhandled-exception hooks call, so the fields cannot diverge per channel, and (ii) a test that
asserts the report contains each key. Route (i) is structural, route (ii) is a test; there is no
type-level or lint-level enforcement, and pretending otherwise is exactly the decay the collection's
thesis warns about. CI placement: `python_quality_gates_manifest.md`.

### 11c. The always-on baseline

**VERSION-DEPENDENT (3.14 baseline; 3.15 for the sampler).** The cheapest defensible always-on
diagnosability configuration for a Python service, entirely from the stdlib. Every item is verified
in the section named; total cost is approximately zero.

| Item | Mechanism | Why it must be on *before* the incident | §|
|---|---|---|---|
| Crash tracebacks | `PYTHONFAULTHANDLER=1` | Cannot be installed into a process that has already received `SIGSEGV` | §4a |
| On-demand thread dump | `faulthandler.register(signal.SIGUSR1)` (POSIX) | The cheapest wedge diagnostic, and it needs no attach permission | §4b |
| Complete failure capture | all four unhandled-exception channels routed into `logging` | Thread, GC and asyncio failures are otherwise silent or stderr-only | §4g |
| No accidental breakpoints | `PYTHONBREAKPOINT=0` | A stray `breakpoint()` in production is a hang, and this neuters it without a code change | §4g |
| Attachability | remote debugging left **enabled** | `pdb -p` and `profiling.sampling attach` cannot be enabled retroactively | §2c |

**Deliberately *not* in the baseline — OPEN (policy over the costs established in §1c):**
`tracemalloc` (unquantified overhead — turn on for a bounded investigation, and remember it cannot
see earlier allocations); `gc.set_debug(DEBUG_LEAK)` (leaks by design); any `sys.settrace` tracer
(de-optimises the thread); a registered audit hook (unremovable, paid on every hot event); `-X perf`
(changes native stack shape and is incompatible with a JIT build); `-X dev` (its allocator hooks and
warning filters change behaviour, so it belongs in development and CI, not production).

---

## Anti-patterns checklist

Each is a violation of a section above. Reject on sight. Every line restates a fact established and
tagged in the section it names; no new claims are introduced here.

- **`print()` as the primary diagnostic instrument** — it cannot be filtered per component, corrupts
  machine-readable stdout, carries no structured field to correlate on, is edited into and out of
  source so the diagnostic is not reproducible from a released artefact, and produces no traceback,
  no frame and no post-mortem entry point (§1a, §4g; emission alternatives:
  `logging_observability_manifest.md`).
- **Profiling a debug build, or quoting a number without naming the build** — a debug build changes
  the allocator, the warning filters and frozen-module state; free-threaded, JIT and tail-call
  builds each change what the instrument can see (§6f, §9d).
- **Leaving a tracer or profiler installed in production** — `sys.settrace` de-optimises the whole
  thread and cannot be scoped; a `cProfile` left enabled holds `sys.monitoring` tool id 2 and breaks
  the next tool that needs it (§3b, §8b).
- **Catching to log and then re-raising at every level** — produces N stack traces for one failure
  and destroys the log-once boundary; the handling boundary logs, the intermediate layers do not
  (`error_tracing_contract_manifest.md` §10, `logging_observability_manifest.md` §10).
- **Drawing a conclusion from a sampler's blind spot** — "the function does not appear in the
  profile" after 1,000 samples means nothing: a true 5% can read as 3% or 7%, and short-lived
  functions can be missed entirely (§6f).
- **Copying `-X disable_remote_debug` from the CPython docs** — the underscore spelling is silently
  ignored; only `-X disable-remote-debug` works, and unknown `-X` names do not error (§2c).
- **Setting `PYTHON_DISABLE_REMOTE_DEBUG=` to "leave it unset"** — an empty value **disables**
  remote debugging, the opposite of `PYTHONFAULTHANDLER=` (§2c, §4a).
- **`tracemalloc.start()` with no `nframe`** — one recorded frame, almost always a library helper;
  leak attribution needs `start(25)` or `-X tracemalloc=25`, and `traceback[0]` is the *outermost*
  frame since 3.7 (§5b).
- **Expecting `-X dev` to enable tracemalloc, fail on warnings, or defeat `-O`** — it does none of
  the three (§7a).
- **`gc.set_debug(gc.DEBUG_LEAK)` in a long-running process** — it includes `DEBUG_SAVEALL` and
  therefore leaks unboundedly by design: the leak detector becomes the leak (§5c).
- **`gc.get_referrers()` as a routine probe** — O(heap), and it reports the investigator's own
  frames among the referrers (§5c).
- **Installing faulthandler and calling crash coverage done** — it catches five signals and not
  `SIGKILL`, the OOM killer, `MemoryError`, an uncaught exception, or a hang (§4a).
- **Reading a faulthandler dump as a normal traceback** — no source lines, 100-frame/100-thread
  caps, 500-character truncation, and most-recent-call **first** (§4c).
- **`dump_traceback_later(..., exit=True)` in a process whose logs matter** — `_exit()` flushes
  nothing (§4b).
- **Re-pointing the log sink without re-calling `faulthandler.enable()`** — it retains the file
  *descriptor*, so dumps can land in an unrelated reused fd (§4c).
- **Printing `f_locals` from `sys._current_frames()` (or `py-spy dump --locals`) against a
  free-threaded build** — documented as possibly crashing the interpreter (§9c).
- **Believing a `--mode gil` result without checking `sys._is_gil_enabled()`** — an unmarked C
  extension silently re-enables the GIL with only a printed warning (§9c).
- **`-X perf` to profile a JIT build** — `sys.activate_stack_trampoline()` "Cannot be activated if
  JIT is active" (§6d, §9a).
- **Returning `DISABLE` from a `RAISE`/`PY_UNWIND`/`RERAISE` callback on 3.12–3.14** — `ValueError`
  "in a non-specific location", no traceback; correct only from 3.15 (§3c).
- **Treating every `sys.monitoring` callback's second argument as an instruction offset** — `LINE`
  passes a line number (§3d).
- **`sys.addaudithook()` as a security control** — explicitly not a sandbox, trivially bypassable
  from Python, unremovable once added, and silently not-added if an existing hook raises
  `RuntimeError` (§8a).
- **A hand-rolled supervision tree, retry budget, dead-letter queue, or health-check HTTP port in a
  single-process app** — the restarter is systemd or the orchestrator, and the rest is
  distributed-systems machinery at the wrong scale (§10b, §10c).
- **A self-test that logs its failure and continues** — a self-test without a defined refusal is
  decoration; on failure enter the safe state (§10b `safe-state`, §10c).
- **Scheduled restarts adopted instead of finding the leak** — rejuvenation without `steady-state`
  and without §5's hunt hides the evidence it was meant to survive (§10b `software-rejuvenation`).

---

## Open questions to resolve before building

Each is a decision this project must make and record, per the epistemic-tagging discipline of
`software_spec_discipline_manifest.md` §G5.

1. **OPEN — Is remote debugging enabled in production?** Recommended yes (§2c: zero idle cost, OS
   permission is the real gate). Decide, record the threat model, and if the answer is no use
   `--without-remote-debug` at build time rather than the `-X` flag whose documented spelling is a
   no-op.
2. **OPEN — What is the minimum interpreter version for the runbook?** The instrument set changes
   sharply: `python -m pdb -p PID` and `python -m asyncio pstree` need 3.14; `python -m
   profiling.sampling` needs 3.15, whose final release is scheduled after this file's access date;
   py-spy and austin declare support only through 3.14. Pin one baseline and write the runbook
   against it (support windows: `python_platform_baseline_manifest.md`).
3. **OPEN — How far does the startup self-test go?** No authoritative bar exists (§10b). Decide the
   split between a fast startup preflight and a full `--self-test`, and name the safe state each
   failure leads to.
4. **OPEN — What shape is the maintenance interface?** CLI subcommand group, `SIGUSR1` handler,
   loopback socket, or some combination (§10b `maintenance-interface`). The *facts it reports* are
   fixed; the shape is not.
   Include the Windows answer, since `faulthandler.register` does not exist there.
5. **OPEN — Which state-mutating probes are exposed, and behind what gate?**
   `gc.set_debug(gc.DEBUG_LEAK)` and `tracemalloc.start()` both change runtime behaviour
   (§10b `maintenance-interface`).
   Name the gate and the maximum duration.
6. **OPEN — Is `tracemalloc` on at startup in production?** `-X tracemalloc=25` is the difference
   between an attributable `ResourceWarning` and an unattributable one (§5b), and its overhead is
   unquantified in any primary source. Decide per deployment, not per developer.
7. **OPEN — What exactly is in the failure report, and who renders it?** §11b lists a defensible
   minimum; the set is a convention. Decide the field list and the single function that produces it,
   since nothing mechanical keeps the four channels in agreement.
8. **OPEN — Is shell-boundary record/playback in scope for v1?** It is the only answer to "cannot
   reproduce" (§10b `record-playback`) and the only §10 mechanism whose absence cannot be remedied
   afterwards. If it is deferred, record what will be lost.
9. **OPEN — Which build variant is shipped, and is debug info kept for it?** §4e's tension is real:
   the optimised build is the correct performance target and the worse crash-analysis target. Decide
   whether debug symbols are archived alongside each release artefact.
10. **OPEN — Verify the `-X no_debug_ranges` environment-variable spelling.** The two fact packs for
    this pass disagree (`PYTHONNODEBUGRANGES` vs `PYTHON_NODEBUGRANGES`); the `-X` form is agreed
    (§7d). An unknown `PYTHON*` name fails silently, so this must be checked against
    `using/cmdline.html` before it enters a deployment config.
11. **OPEN — Re-verify the two most load-bearing naming sources before quoting them as ground
    truth.** The SWE corpus records both Hanmer, *Patterns for Fault Tolerant Software* and Nygard,
    *Release It!* with `year: UNRESOLVED` and `verification: unverified`, and between them they name
    `maintenance-interface`, `quarantine`, `correcting-audits`, `heartbeat` and `fail-fast` used
    above. They are flagged inline here; a manifest that presents them as verified would be wrong.

---

## Sources (accessed 8 Aug 2026)

Each entry states what it establishes; the claims themselves are tagged at their point of use above.
Only URLs carried by this pass's fact and seed packs appear here — none was invented.

### PEPs

- PEP 768 — safe external debugger interface: Final, Python-Version 3.14; `sys.remote_exec`;
  `PYTHON_DISABLE_REMOTE_DEBUG` disabling on any value including empty; `--without-remote-debug`;
  the eval-breaker safe point; the ptrace / `task_for_pid` / `PROCESS_VM_READ` permission set; the
  path-not-code rationale — https://peps.python.org/pep-0768/ ;
  https://raw.githubusercontent.com/python/peps/main/peps/pep-0768.rst . Accessed 8 Aug 2026.
- PEP 669 — low-impact monitoring: Final, Python-Version 3.12; the "orders of magnitudes less than
  `sys.settrace()`" claim; six tool ids; `DISABLE`; `restart_events()` not being tool-specific —
  https://peps.python.org/pep-0669/ ;
  https://raw.githubusercontent.com/python/peps/main/peps/pep-0669.rst . Accessed 8 Aug 2026.
- PEP 799 — the `profiling` package: Final, Python-Version 3.15, Resolution 2025-08-21;
  `profiling.tracing` / `profiling.sampling`; `cProfile` retained as an alias; the `profile`
  deprecation schedule 3.15 → 3.16 → removal in 3.17 — https://peps.python.org/pep-0799/ ;
  https://raw.githubusercontent.com/python/peps/main/peps/pep-0799.rst . Accessed 8 Aug 2026.
- PEP 831 — frame pointers everywhere: Final, Python-Version 3.15, Resolution 2026-04-30; the
  single-component unwinding warning —
  https://raw.githubusercontent.com/python/peps/main/peps/pep-0831.rst . Accessed 8 Aug 2026.
- PEP 578 — runtime audit hooks: Final, Python-Version 3.8; the API surface; "Hooks cannot be
  removed or replaced"; "This is not sandboxing"; the 1.05x benchmark range —
  https://peps.python.org/pep-0578/ ;
  https://raw.githubusercontent.com/python/peps/main/peps/pep-0578.rst . Accessed 8 Aug 2026.
- PEP 744 — JIT compilation: still **Draft**, Informational, no Resolution; the JIT not default;
  "Profilers and debuggers for C code are currently unable to trace back through JIT frames";
  Python-level tools unaffected — https://peps.python.org/pep-0744/ ;
  https://raw.githubusercontent.com/python/peps/main/peps/pep-0744.rst . Accessed 8 Aug 2026.

### CPython documentation

- Command line and environment — every `-X` and `PYTHON*` switch quoted in §§2, 5, 7, 9: `dev`,
  `faulthandler`, `importtime[=2]`, `showrefcount`, `tracemalloc[=N]`, `perf`, `perf_jit`, `gil`,
  `presite`, `cpu_count`, `no_debug_ranges`; the `-W` grammar, actions and last-match-wins
  precedence; `PYTHONVERBOSE` `-v`/`-vv`; `PYTHONMALLOC` values; `PYTHONBREAKPOINT` including the
  `"0"` no-op; `PYTHONHASHSEED` — https://docs.python.org/3/using/cmdline.html . Accessed 8 Aug
  2026.
- Python Development Mode — the seven effects, the four non-effects, startup-only plus
  `sys.flags.dev_mode`, and the `ResourceWarning` / `Object allocated at` worked example —
  https://docs.python.org/3/library/devmode.html . Accessed 8 Aug 2026.
- `faulthandler` — `enable(file, all_threads, c_stack)`; `dump_c_stack()` (3.14); the five signals;
  the free-threaded single-thread note; the `dump_traceback_later` watchdog and `exit=True` →
  `_exit()`; `register`/`unregister` unavailable on Windows; the 100-frame / 100-thread /
  500-character / no-source-line / reversed-order limits; the file-descriptor hazard —
  https://docs.python.org/3/library/faulthandler.html . Accessed 8 Aug 2026.
- `sys.monitoring` — tool ids 0–5 and the four named constants; `use_tool_id` raising `ValueError`;
  `clear_tool_id` versus `free_tool_id`; the local / ancillary / other partition; `BRANCH`
  deprecated in 3.14; per-event callback signatures; the `DISABLE`-on-a-global-event `ValueError`
  "in a non-specific location" — https://docs.python.org/3/library/sys.monitoring.html . Accessed 8
  Aug 2026.
- `sys` — `settrace`/`setprofile` event sets, the C-call asymmetry and return-value semantics;
  `f_trace_lines`/`f_trace_opcodes`; per-thread scope; `sys._current_frames()`; `sys._getframe`;
  `sys.remote_exec` and both audit events; `activate_stack_trampoline` and "Cannot be activated if
  JIT is active"; the `addaudithook` not-a-sandbox and silent-failure notes; `unraisablehook`;
  `sys.last_exc` — https://docs.python.org/3/library/sys.html . Accessed 8 Aug 2026.
- `pdb` — the `-p/--pid` synopsis (3.14) and the blocked-in-a-syscall note; `set_default_backend`
  with default `'settrace'` and the "always use `'monitoring'`" note; `set_trace(header=,
  commands=)`; the 3.13 immediate-entry change; `post_mortem` exception-object support —
  https://docs.python.org/3/library/pdb.html . Accessed 8 Aug 2026.
- `tracemalloc` — `start(nframe=1)`; `compare_to`/`statistics` and the three `key_type` values;
  `Filter`/`DomainFilter`; the 3.7 frame-order change; the limitations list —
  https://docs.python.org/3/library/tracemalloc.html . Accessed 8 Aug 2026.
- `gc` — the `DEBUG_*` constants and `DEBUG_LEAK = COLLECTABLE | UNCOLLECTABLE | SAVEALL`;
  `gc.garbage` empty since 3.4 (PEP 442); the 3.14 incremental collector and its 3.14.5 reversion;
  the free-threaded 10% / 40× collection gate — https://docs.python.org/3/library/gc.html . Accessed
  8 Aug 2026.
- `threading` — `excepthook` fields, `SystemExit` silently ignored, the reference-cycle and
  resurrection warnings — https://docs.python.org/3/library/threading.html . Accessed 8 Aug 2026.
- Deterministic versus statistical profiling, and `cProfile` recommended over `profile` —
  https://docs.python.org/3/library/profile.html . Accessed 8 Aug 2026.
- `profiling.sampling` (3.15) — the subcommands; the permission requirements; "The target process
  requires no modification and need not be restarted"; the same-minor-version and
  free-threaded-must-match constraints; the sample-count margin-of-error passage —
  https://docs.python.org/3.15/library/profiling.sampling.html . Accessed 8 Aug 2026.
- The Linux `perf` HOWTO — the three activation paths and their precedence; the `perf inject --jit`
  pipeline; perf map files; the frame-pointer CFLAGS and the two `sysconfig` checks; the perf > v6.8
  requirement — https://docs.python.org/3/howto/perf_profiling.html . Accessed 8 Aug 2026.
- Remote debugging attachment protocol — `PyRuntime` location, `_Py_DebugOffsets` validation,
  `debugger_script_path` and the eval-breaker bit, and the not-a-stable-ABI statement —
  https://docs.python.org/3/howto/remote_debugging.html . Accessed 8 Aug 2026.
- GDB helpers — `python-gdb.py` from `Tools/gdb/libpython.py`, the loading recipe, the `py-*`
  command set, the gdb 7.0+ and debuginfo requirements, "Optimized builds may lose frame
  information", and `thread apply all py-bt` on a live process or a core file —
  https://docs.python.org/3/howto/gdb_helpers.html . Accessed 8 Aug 2026.
- asyncio call-graph introspection — `capture_call_graph` / `format_call_graph` / `print_call_graph`
  (3.14) and the `future_add_to_awaited_by` requirement for low-level code —
  https://docs.python.org/3/library/asyncio-graph.html . Accessed 8 Aug 2026.
- Free-threading HOWTO — `sys._is_gil_enabled()`; `sysconfig.get_config_var("Py_GIL_DISABLED")` as
  "the recommended mechanism"; automatic GIL re-enablement by an unmarked C extension; **the
  `frame.f_locals`-from-another-thread crash warning**; the iterator thread-safety warning —
  https://docs.python.org/3/howto/free-threading-python.html . Accessed 8 Aug 2026.
- Configure options — `--enable-experimental-jit=[no|yes|yes-off|interpreter]` defaulting to `no`;
  `--with-tail-call-interp`; `--disable-gil`; `--without-remote-debug`; `--with-pydebug`;
  `--with-trace-refs`; `--enable-pystats`; the sanitizer options —
  https://docs.python.org/3/using/configure.html . Accessed 8 Aug 2026.
- What's New in 3.14 — the PEP 768 section; `python -m asyncio ps`/`pstree`;
  `--with-tail-call-interp`; the free-threading single-thread penalty; `faulthandler.dump_c_stack`;
  `-X importtime=2`; the incremental GC and its 3.14.5 reversion —
  https://docs.python.org/3/whatsnew/3.14.html . Accessed 8 Aug 2026.
- What's New in 3.15 — the Tachyon section (rates up to 1,000,000 Hz, the `--mode` values, the
  output formats, "Useful for investigating hung processes"); PEP 799; PEP 831; per-code-object
  `sys.monitoring` "other" events (gh-146182); `faulthandler` `max_threads` (gh-149085); JIT
  unwinding for GDB and GNU `backtrace()` (gh-146071, gh-149104); the MSVC 18 Windows tail-calling
  interpreter (gh-143068) — https://docs.python.org/3.15/whatsnew/3.15.html ;
  https://raw.githubusercontent.com/python/cpython/main/Doc/whatsnew/3.15.rst . Accessed 8 Aug 2026.

### CPython source and release notes

- `initconfig.c` on both 3.14 and `main` — `config_init_remote_debug()` reading
  `Py_GETENV("PYTHON_DISABLE_REMOTE_DEBUG")` and `config_get_xoption(L"disable-remote-debug")`
  (hyphens), and `Py_GETENV` as a bare `getenv()` —
  https://raw.githubusercontent.com/python/cpython/3.14/Python/initconfig.c ;
  https://raw.githubusercontent.com/python/cpython/main/Python/initconfig.c . Accessed 8 Aug 2026.
- `preconfig.c` — `_Py_GetEnv()` returning `NULL` when `var[0] == '\0'`, which is why empty means
  *unset* for `PYTHONFAULTHANDLER` and `PYTHONDEVMODE` —
  https://raw.githubusercontent.com/python/cpython/3.14/Python/preconfig.c . Accessed 8 Aug 2026.
- `Doc/using/cmdline.rst` on both branches — the documented (incorrect) `-X disable_remote_debug`
  spelling and the "non-empty string" wording; `-X tlbc` documented only on `main` —
  https://raw.githubusercontent.com/python/cpython/3.14/Doc/using/cmdline.rst ;
  https://raw.githubusercontent.com/python/cpython/main/Doc/using/cmdline.rst . Accessed 8 Aug 2026.
- `Lib/pdb.py` — `__all__` without `attach`; the `attach()` body (loopback `create_server`, the temp
  connect script, `sys.remote_exec`, `server.accept()`) and its "TODO Add a timeout?" comment;
  `use_signal_thread`; `_PdbServer.protocol_version()` —
  https://raw.githubusercontent.com/python/cpython/3.14/Lib/pdb.py . Accessed 8 Aug 2026.
- `Modules/_lsprof.c` on 3.14 versus 3.11 — `self->tool_id = PY_MONITORING_PROFILER_ID;` and
  `use_tool_id(..., "cProfile")` versus zero monitoring references, dating the switch to 3.12 —
  https://raw.githubusercontent.com/python/cpython/3.14/Modules/_lsprof.c ;
  https://raw.githubusercontent.com/python/cpython/3.11/Modules/_lsprof.c . Accessed 8 Aug 2026.
- `_Py_MAX_SCRIPT_PATH_SIZE 512`, and the debug-offsets cookie plus the `co_tlbc` / `tlbc_index`
  offsets — https://raw.githubusercontent.com/python/cpython/3.14/Include/cpython/pystate.h ;
  https://raw.githubusercontent.com/python/cpython/3.14/Include/internal/pycore_debug_offsets.h .
  Accessed 8 Aug 2026.
- `Lib/profiling/sampling/cli.py` — the exact flag inventory including `-r/--sampling-rate` with
  source default `"1khz"`, and the subcommands `run`, `attach`, `dump`, `replay` —
  https://raw.githubusercontent.com/python/cpython/main/Lib/profiling/sampling/cli.py . Accessed 8
  Aug 2026.
- 3.14.7 (`.. release date: 2026-08-05`) — the `sys.monitoring` branch/loop callback fix
  (gh-152375), the `cProfile.Profile.enable` fix (gh-153068), the deferred-GC-tracking changes; and
  3.14.5 (2026-05-10) — the `_remote_debugging` offset-table validation hardening —
  https://raw.githubusercontent.com/python/cpython/3.14/Misc/NEWS.d/3.14.7.rst ;
  https://raw.githubusercontent.com/python/cpython/3.14/Misc/NEWS.d/3.14.5.rst . Accessed 8 Aug
  2026.

### Tool releases — versions, platform support, CLI surface

- memray 1.20.0 (2026-08-07), Linux and macOS only ("cannot be installed on other platforms"),
  Python 3.9–3.15, the subcommand set and `--native`; pytest-memray 1.10.0 (2026-08-07) —
  https://pypi.org/pypi/memray/json ; https://pypi.org/project/memray/ ;
  https://pypi.org/pypi/pytest-memray/json . Accessed 8 Aug 2026.
- py-spy 0.4.2 (2026-04-24), support declared for CPython 2.3–2.7 and 3.3–3.14, the
  `record`/`top`/`dump` subcommands and flags, the root / `ptrace_scope` / `SYS_PTRACE`
  requirements, and the OS list — "works on Linux, OSX, Windows and FreeBSD", with 32-bit Windows
  answered "Not yet" in the FAQ (§4d) — https://pypi.org/pypi/py-spy/json ;
  https://raw.githubusercontent.com/benfred/py-spy/master/README.md . Accessed 8 Aug 2026.
- austin-dist 4.0.0 (2025-11-01), the 3.9–3.14 compatibility table — which also lists the
  supported platforms and architectures, Windows x86_64/i686 among them (§4d) — the flag set, MOJO
  as the default output, and the `austinp` variant; plus the confirmation that the PyPI name
  `austin`
  is an unrelated 2016 package (2016.0.1) — https://pypi.org/pypi/austin-dist/json ;
  https://raw.githubusercontent.com/P403n1x87/austin/master/README.md ;
  https://pypi.org/pypi/austin/json . Accessed 8 Aug 2026.
- Scalene 2.3.0 (2026-05-12) with `requires_python = "!=3.11.0,>=3.8"`; pyinstrument 5.1.3
  (2026-07-29); coverage.py 7.15.4 (2026-08-06); objgraph 3.6.2 (2024-10-10) —
  https://pypi.org/pypi/scalene/json ; https://pypi.org/pypi/pyinstrument/json ;
  https://pypi.org/pypi/coverage/json ; https://pypi.org/pypi/objgraph/json . Accessed 8 Aug 2026.
- **FLAGGED-SECONDARY.** coverage.py's `sysmon` core (`COVERAGE_CORE=sysmon` / `core = sysmon`), its
  status as the default on Python 3.14+ where supported, and its plugin / dynamic-context / branch
  limitations. The evidence for this pass was documentation text surfaced via search rather than a
  fetched page — https://coverage.readthedocs.io/en/latest/ . Accessed 8 Aug 2026.

### Named vocabulary — naming works, as the SWE corpus records them

Element ids come from `SWE/design_elements_corpus_v1_0.md`, `design_elements_catalog_v1_0.md` and
`architecture_elements_catalog_v1_0.md`, each verified present in `elements.json` by the seed pack
for this pass. Verification status is the corpus's own: **UNVERIFIED** means its `verification`
field says so, and this file does not upgrade it. No URL is invented for a print work.

| Naming work | Status | Elements used here |
|---|---|---|
| Bass, Clements & Kazman, *Software Architecture in Practice*, 4th ed., 2021 (Addison-Wesley SEI, ISBN 978-0-13-688609-9) | verified | `specialized-interfaces`, `record-playback`, `executable-assertions`, `heartbeat-tactic`, `abort`, `degradation`, `removal-from-service`, and the `bck-cat:control-and-observe-system-state` grouping |
| IEC 61508:2010, Ed. 2.0, Part 7 (technique catalogue) | verified | `built-in-self-test` — the citable covering work, since the element's `named_in` field is a Wikipedia page (a corpus data defect) |
| ISO 26262:2018, *Road vehicles — Functional safety*, 2nd ed. | verified | `safe-state` |
| Douglass, B. P., *Real-Time Design Patterns* / *Doing Hard Time* / *Real-Time UML* (author corpus, Addison-Wesley), living | verified | `sanity-check`, `watchdog` |
| Koopman, P., *Better Embedded System Software*, 2010 (ISBN 978-0-9844490-0-2) | verified | the watchdog chapter: kicking discipline, and what a watchdog cannot detect |
| White, E., *Making Embedded Systems*, 2nd ed., 2024 (O'Reilly, ISBN 9781098151546) | verified | `core-dump` — covering work, since the element's `named_in` field is the bare work id `white` (a corpus data defect) |
| Free Software Foundation, *Debugging with GDB*, Tenth Edition, living (sourceware.org/gdb) | verified | `core-dump` — second covering work; core-file production and analysis |
| Grand, M., *Patterns in Java, Volume 1*, 1998 | verified | `two-phase-termination`, the cooperative-shutdown mechanism inside `safe-state` |
| Candea, G. & Fox, A., *Crash-Only Software*, 2003, HotOS IX — https://dslab.epfl.ch/pubs/crashonly.pdf | verified | `crash-only-software`, the architecture-altitude form of `let-it-crash` |
| Kuhn, R., with Hanafee, B. & Allen, J., *Reactive Design Patterns*, 2017 (Manning, ISBN 978-1-61729-180-7) | verified | `error-kernel`; co-names `let-it-crash` |
| Hohpe, G. & Woolf, B., *Enterprise Integration Patterns*, 2003 | verified | `correlation-identifier`; `dead-letter-channel` (named to mark it out of scale) |
| Richardson, C., *Microservices Patterns*, 2018 | verified | `health-check-api`, `log-aggregation`, `distributed-tracing` — recorded to mark them out of scale, not as imports |
| Hanmer, R., *Patterns for Fault Tolerant Software* | **UNVERIFIED** — corpus record has `year: UNRESOLVED`, no identifier; element prose says 2007 | `maintenance-interface`, `quarantine`, `correcting-audits`, `heartbeat`, `restart`, and the watchdog-versus-heartbeat selection rule. **The most load-bearing source in this slice; re-verify before treating it as ground truth** |
| Nygard, M., *Release It!* | **UNVERIFIED** — corpus record has `year: UNRESOLVED`; element prose says 2nd ed. 2018 | `fail-fast`, `steady-state`; co-names `let-it-crash` |
| Huang, Kintala, Kolettis & Fulton, *Software Rejuvenation*, 1995, FTCS-25 | **UNVERIFIED** — corpus note: DOI and primary page could not be loaded | `software-rejuvenation`; the verified substitute is `removal-from-service` |

### Sibling manifests (cross-referenced, not duplicated)

- `python_platform_baseline_manifest.md` — the version hub: release dates, support phases, PEP
  status by version, the complete `-X`/`PYTHON*` switch inventory with version-added stamps, build
  variants (free-threaded, JIT, tail-call, pydebug, trace-refs, pystats), and the minimum-target
  policy. This file states behaviour and cites the hub for *when*.
- `logging_observability_manifest.md` — everything on the **emission** side: severity levels,
  Logger/Handler/Formatter/Filter, library-versus-application configuration, structured and
  contextual logging, correlation-ID transport, log rotation and the `steady-state` accumulator
  discipline, the audit log, and the log-once boundary. This file never configures a handler.
- `error_tracing_contract_manifest.md` — the error **contract**: the two propagation channels and
  the typed-result encoding, chaining and `__cause__`, the exception hierarchy, narrow catching,
  assertion policy and the `-O` caveat (§14), boundary validation, and the raise-side disposition
  vocabulary (`fail-fast`, `let-it-crash`, `escalation`, `rollback`, `roll-forward`, `marked-data`).
  This file owns only `safe-state` and `quarantine`, and only as diagnostic surfaces.
- `python_testing_tooling_manifest.md` — the injection seams this file depends on (clock, seed, data
  source), `filterwarnings = error` as the warning gate, coverage configuration, and
  `pytest-memray`. Diagnosability and testability share these seams (§10a).
- `python_concurrency_determinism_manifest.md` — the execution models, structured concurrency and
  cancellation, and keeping concurrent code deterministic under test; free-threading and
  subinterpreter facts as *behaviour*. This file states only what those builds do to the
  *instruments* (§9c).
- `python_module_boundaries_manifest.md` — the unit of change: project layout, the import system as
  a boundary, plugin seams (the subject `quarantine` needs), dependency declaration and environment
  markers (the memray platform constraint), and machine-enforced dependency direction. Keeping
  `_diagnostics.py` separable is that file's mechanism, applied here (§10b
  `maintenance-interface`).
- `python_quality_gates_manifest.md` — where checks run and how they fail: the CI matrix, the `-W
  error` gate, and the fitness function that enforces §9d's "name the build" rule. This file names
  the obligation; that file wires it.
- `python_linting_practices_manifest.md` — the rule set, including the exact rule codes that ban
  committed `breakpoint()` calls and stray `print` debugging. This file states the runtime
  neutraliser (`PYTHONBREAKPOINT=0`) and defers the codes rather than inventing them.
- `python_language_hazards_manifest.md` — intrinsic language footguns routed to their enforcement
  mechanism; the hazards that *produce* the symptoms in §1b.
- `architecture_manifest_default.md` — the reasoning frame: component and interface vocabulary, the
  functional-core/imperative-shell rationale that makes the `record-playback` capture boundary of
  §10b well-defined, and debuggability as a design property.
- `software_spec_discipline_manifest.md` — §G5 open-question discipline, epistemic tagging, and the
  obligation to record every OPEN above as a pinned project decision.
- `spec_recovery_reverse_engineering_manifest.md` — recovering intent from an existing system; the
  runtime observations in §§2–6 are its dynamic-analysis inputs.



