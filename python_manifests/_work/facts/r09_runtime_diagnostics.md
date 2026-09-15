# Python runtime diagnostics, debuggability & profiling - fact pack (verified 2026-08-08)

**Scope.** The "diagnosable" pillar beyond logging: how a running Python process is inspected,
attached to, sampled, dumped, and made to explain itself. Every version, date, PEP status, flag
and API name below was loaded live from a primary source on 2026-08-08 - peps.python.org,
docs.python.org, devguide.python.org, python.org/downloads, the PyPI JSON API, or CPython's own
source, `Doc/*.rst` and `Misc/NEWS.d` at `raw.githubusercontent.com/python/cpython`. Where CPython's
*documentation* and CPython's *implementation* disagree, the implementation is quoted and the doc
bug is named.

## Version table

| thing | current version | released (ISO date) | source URL | tag |
|---|---|---|---|---|
| CPython (latest stable) | 3.14.7 | 2026-08-05 | https://www.python.org/downloads/ ; https://raw.githubusercontent.com/python/cpython/3.14/Misc/NEWS.d/3.14.7.rst (`.. release date: 2026-08-05`) | VERSION-DEPENDENT (3.14) |
| CPython 3.14 series, first release | 3.14.0 | 2025-10-07 | https://devguide.python.org/versions/ | ESTABLISHED |
| CPython 3.14.6 | 3.14.6 | 2026-06-10 | https://raw.githubusercontent.com/python/cpython/3.14/Misc/NEWS.d/3.14.6.rst | VERSION-DEPENDENT (3.14) |
| CPython 3.14.5 (GC reversion landed here) | 3.14.5 | 2026-05-10 | https://raw.githubusercontent.com/python/cpython/3.14/Misc/NEWS.d/3.14.5.rst | VERSION-DEPENDENT (3.14) |
| CPython 3.13 (latest patch) | 3.13.14 | 2026-06-10 | https://www.python.org/downloads/ | VERSION-DEPENDENT (3.13) |
| CPython 3.15 (newest prerelease) | 3.15.0rc1 | 2026-08-04 | https://peps.python.org/pep-0790/ | VERSION-DEPENDENT (3.15) |
| CPython 3.15.0 final | *scheduled* | 2026-10-01 | https://peps.python.org/pep-0790/ ; https://devguide.python.org/versions/ | VERSION-DEPENDENT (3.15) |
| CPython `main` branch targets | 3.16 | in development | https://devguide.python.org/versions/ | VERSION-DEPENDENT (3.16) |
| PEP 768 - Safe external debugger interface | Final | Created 2024-11-25, Resolution 2025-03-17, Python-Version 3.14 | https://raw.githubusercontent.com/python/peps/main/peps/pep-0768.rst | ESTABLISHED |
| PEP 669 - Low Impact Monitoring | Final | Created 2021-08-18, Python-Version 3.12 | https://raw.githubusercontent.com/python/peps/main/peps/pep-0669.rst | ESTABLISHED |
| PEP 799 - dedicated `profiling` package | Final | Created 2025-07-21, Resolution 2025-08-21, Python-Version 3.15 | https://raw.githubusercontent.com/python/peps/main/peps/pep-0799.rst | VERSION-DEPENDENT (3.15) |
| PEP 831 - Frame Pointers Everywhere | Final | Created 2026-03-14, Resolution 2026-04-30, Python-Version 3.15 | https://raw.githubusercontent.com/python/peps/main/peps/pep-0831.rst | VERSION-DEPENDENT (3.15) |
| PEP 578 - Runtime Audit Hooks | Final | Created 2018-06-16, Python-Version 3.8 | https://raw.githubusercontent.com/python/peps/main/peps/pep-0578.rst | ESTABLISHED |
| PEP 744 - JIT Compilation | **Draft** (Informational) | Created 2024-04-11, Python-Version 3.13, no Resolution | https://raw.githubusercontent.com/python/peps/main/peps/pep-0744.rst | VERSION-DEPENDENT (3.13+) |
| PEP 790 - Python 3.15 release schedule | Active | rc1 2026-08-04, rc2 2026-09-01, final 2026-10-01 | https://peps.python.org/pep-0790/ | VERSION-DEPENDENT (3.15) |
| memray | 1.20.0 | 2026-08-07 | https://pypi.org/pypi/memray/json ; https://pypi.org/project/memray/ | VERSION-DEPENDENT |
| pytest-memray | 1.10.0 | 2026-08-07 | https://pypi.org/pypi/pytest-memray/json | VERSION-DEPENDENT |
| py-spy | 0.4.2 | 2026-04-24 | https://pypi.org/pypi/py-spy/json ; https://raw.githubusercontent.com/benfred/py-spy/master/README.md | VERSION-DEPENDENT |
| austin (PyPI dist `austin-dist`) | 4.0.0 | 2025-11-01 | https://pypi.org/pypi/austin-dist/json ; https://raw.githubusercontent.com/P403n1x87/austin/master/README.md | VERSION-DEPENDENT |
| Scalene | 2.3.0 | 2026-05-12 | https://pypi.org/pypi/scalene/json | VERSION-DEPENDENT |
| pyinstrument | 5.1.3 | 2026-07-29 | https://pypi.org/pypi/pyinstrument/json | VERSION-DEPENDENT |
| coverage.py | 7.15.4 | 2026-08-06 | https://pypi.org/pypi/coverage/json | VERSION-DEPENDENT |
| objgraph | 3.6.2 | 2024-10-10 | https://pypi.org/pypi/objgraph/json | VERSION-DEPENDENT |

## Facts

### A. PEP 768 - the external debugger attach interface

1. PEP 768 is **Final**, `Python-Version: 3.14`, Created 2024-11-25, Resolution 2025-03-17; the
   feature exists in every 3.14.x and later and in **no** 3.13.x - VERSION-DEPENDENT (3.14)
2. The entire user-facing Python surface is one function: `sys.remote_exec(pid, script)`. `script` is
   a **path** (`str | bytes | PathLike`) to a file containing Python code, **not** a source string.
   Availability: Unix, Windows - VERSION-DEPENDENT (3.14)
3. `sys.remote_exec()` returns **immediately** and there is **no interface to learn when, or whether,
   the code ran**; the target executes it at its next eval-loop safe point. The caller must keep the
   script file alive until it observes a side effect - VERSION-DEPENDENT (3.14)
4. The documented attach entry point is `python -m pdb -p PID` (`-p`, `--pid`), added in 3.14. The
   full synopsis is `python -m pdb [-c command] (-m module | -p pid | pyfile) [args ...]` - VERSION-DEPENDENT (3.14)
5. `Doc/library/pdb.rst` carries this note verbatim: "Attaching to a process that is blocked in a
   system call or waiting for I/O will only work once the next bytecode instruction is executed or
   when the process receives a signal." A process blocked in `accept()`, `time.sleep()`, or a C
   extension's blocking call is **not** attachable until it returns to bytecode - VERSION-DEPENDENT (3.14)
6. The underlying function is `pdb.attach(pid, commands=())`, but it is **absent from `pdb.__all__`**
   (`["run", "pm", "Pdb", "runeval", "runctx", "runcall", "set_trace", "post_mortem",
   "set_default_backend", "get_default_backend", "help"]`). Treat the CLI as the supported
   interface - VERSION-DEPENDENT (3.14)
7. Attach is **socket-based once bootstrapped**: `pdb.attach()` opens
   `socket.create_server(("localhost", 0))`, writes a temp connect script calling
   `pdb._connect(host="localhost", port=..., frame=sys._getframe(1), ...)`, chmods that script
   readable by group and other, calls `sys.remote_exec(pid, connect_script.name)`, then blocks on
   `server.accept()`. **The target dials back to the debugger's loopback address** - VERSION-DEPENDENT (3.14)
8. Consequence of 7: `pdb -p` cannot cross a network-namespace boundary - a target in another
   container has a different `localhost` - and the target's uid must be able to *read* the temp
   script path - VERSION-DEPENDENT (3.14)
9. There is **no timeout** on the accept. `Lib/pdb.py` carries the literal comment
   `# TODO Add a timeout? Or don't bother since the user can ^C?`. Against a truly wedged process,
   `python -m pdb -p PID` hangs until interrupted - VERSION-DEPENDENT (3.14)
10. On Windows the client uses a **second** socket connection plus a signal-raising thread
    (`use_signal_thread = sys.platform == "win32"`, `interrupt_sock`); on POSIX `interrupt_sock` is
    `None`. Interrupt semantics therefore differ by platform - VERSION-DEPENDENT (3.14)
11. Version coupling: the target must run the **same `major.minor` CPython**; for pre-release
    interpreters the version must match **exactly**. `_PdbServer.protocol_version()` returns
    `int(f"{major:02X}{minor:02X}{revision:02X}F0", 16)` with `revision = 0` by default - VERSION-DEPENDENT (3.14)
12. Kill switches, exact spellings: environment variable **`PYTHON_DISABLE_REMOTE_DEBUG`**;
    interpreter option **`-X disable-remote-debug`** (hyphens - see fact 13); build option
    `--without-remote-debug`, which leaves `Py_REMOTE_DEBUG` undefined and hard-wires
    `config->remote_debug = 0` - VERSION-DEPENDENT (3.14)
13. **CPython documentation bug, still live on 2026-08-08.** `Doc/using/cmdline.rst` documents
    `-X disable_remote_debug` (underscores) on **both** the 3.14 branch and `main`, but
    `Python/initconfig.c` looks up only `config_get_xoption(config, L"disable-remote-debug")`
    (hyphens) on both branches, and `--help-xoptions` prints `-X disable-remote-debug: disable
    remote debugging; also PYTHON_DISABLE_REMOTE_DEBUG`. The interpreter does not error on unknown
    `-X` names, so the underscore form is silently ignored and the operator believes remote debugging
    is off when it is on - VERSION-DEPENDENT (3.14, 3.15, 3.16)
14. **Second doc/implementation disagreement.** `cmdline.rst` says "If this variable is set to a
    non-empty string, it disables the remote debugging feature". `config_init_remote_debug()` reads
    it with `Py_GETENV()`, which is a bare `getenv()` (`if (Py_IgnoreEnvironmentFlag) return NULL;
    return getenv(name);`), and only tests `if (env)`. Therefore **`PYTHON_DISABLE_REMOTE_DEBUG=`
    (empty) DOES disable it**. PEP 768 states this correctly ("any value (including empty string)").
    Contrast `PYTHONFAULTHANDLER` / `PYTHONDEVMODE`, read via `config_get_env()` -> `_Py_GetEnv()`,
    which returns `NULL` when `var[0] == '\0'` and so treats empty as **unset** - VERSION-DEPENDENT (3.14)
15. Wire protocol (`howto/remote_debugging.html`, "Remote debugging attachment protocol"): locate the
    `PyRuntime` structure (`.PyRuntime` ELF section, `__DATA,__PyRuntime` Mach-O section, or the
    `PyRuntim` PE section - truncated to 8 characters by PE), read `_Py_DebugOffsets` at its start,
    validate `cookie` against the literal `"xdebugpy"`
    (`Include/internal/pycore_debug_offsets.h`: `#define _Py_Debug_Cookie "xdebugpy"`), validate
    `version` and `free_threaded`, then write `debugger_script_path`, set `debugger_pending_call = 1`,
    and OR bit 5 (`_PY_EVAL_PLEASE_STOP_BIT`, value 32) into `eval_breaker` - VERSION-DEPENDENT (3.14)
16. `debugger_script_path` is a **fixed 512-byte buffer**: `Include/cpython/pystate.h` defines
    `#define _Py_MAX_SCRIPT_PATH_SIZE 512` and `char debugger_script_path[_Py_MAX_SCRIPT_PATH_SIZE];`.
    Deep container mounts or a long `TMPDIR` are a genuine truncation risk - VERSION-DEPENDENT (3.14)
17. Writing a **path** rather than code is a deliberate mitigation: PEP 768 states it "prevents
    attackers with arbitrary writes from escalating to arbitrary code execution through this
    interface" - ESTABLISHED
18. Overhead when unused is **zero by construction**: the debugger fields are read only when
    `eval_breaker` is already set, a check the eval loop already performs - ESTABLISHED
19. OS permissions are the real access control, unchanged from native debuggers: Linux `ptrace` /
    `CAP_SYS_PTRACE` / `/proc/sys/kernel/yama/ptrace_scope`; macOS `task_for_pid()` (root, debugger
    entitlement, or SIP disabled); Windows `PROCESS_VM_READ` + `PROCESS_VM_WRITE` /
    `SeDebugPrivilege` - ESTABLISHED
20. Two audit events fire: **`sys.remote_exec`** (args `pid`, script path) in the *calling* process,
    and **`cpython.remote_debugger_script`** (arg: script path) in the *target*. The second is the
    hook to install to detect or refuse injected debugging - VERSION-DEPENDENT (3.14)
21. `_Py_DebugOffsets` is **not stable ABI**: its layout holds within a minor version and may change
    across them, which is why version validation is mandatory - ESTABLISHED
22. 3.14.5 (2026-05-10) hardened `_remote_debugging` "by validating remote debug offset tables before
    using them to size memory reads or interpret remote layouts" - a Security-section fix - VERSION-DEPENDENT (3.14.5)

### B. sys.monitoring (PEP 669)

23. PEP 669 is **Final**, `Python-Version: 3.12`; `sys.monitoring` exists from 3.12 onward and not
    before - VERSION-DEPENDENT (3.12)
24. There are exactly **6 tool ids, 0-5 inclusive**. Named: `DEBUGGER_ID = 0`, `COVERAGE_ID = 1`,
    `PROFILER_ID = 2`, `OPTIMIZER_ID = 5`. **3 and 4 are unnamed and free.** The docs state "All IDs
    are treated the same by the VM with regard to events" - the constants are a cooperation
    convention, not an enforcement mechanism - VERSION-DEPENDENT (3.12+)
25. `use_tool_id(tool_id, name, /)` **"Raises a `ValueError` if `tool_id` is in use."** This is the
    single most common way two diagnostic tools collide at runtime - VERSION-DEPENDENT (3.12+)
26. Full API: `use_tool_id`, `clear_tool_id` (unregister all events and callbacks, keep the id),
    `free_tool_id` (calls `clear_tool_id`, then releases the id), `get_tool(id) -> str | None`,
    `get_events(id) -> int`, `set_events(id, event_set)`, `get_local_events(id, code)`,
    `set_local_events(id, code, event_set)`, `restart_events()`, plus the sentinels `DISABLE`,
    `MISSING`, and `NO_EVENTS` (documented as "An alias for `0`") - VERSION-DEPENDENT (3.12+)
27. Events partition into three classes with different powers. **Local events** (tied to a code
    location, disable-able): `PY_START`, `PY_RESUME`, `PY_RETURN`, `PY_YIELD`, `CALL`, `LINE`,
    `INSTRUCTION`, `JUMP`, `BRANCH_LEFT`, `BRANCH_RIGHT`, `STOP_ITERATION`. **Ancillary events**
    (gated by `CALL`): `C_RAISE`, `C_RETURN`. **Other events** (not tied to a location, not
    individually disable-able in 3.14): `PY_THROW`, `PY_UNWIND`, `RAISE`, `EXCEPTION_HANDLED`,
    `RERAISE` - VERSION-DEPENDENT (3.14)
28. `C_RETURN` and `C_RAISE` "will only be seen if the corresponding `CALL` event is being
    monitored". Subscribing to `C_RETURN` alone yields nothing - VERSION-DEPENDENT (3.12+)
29. `DISABLE` is what makes coverage cheap: returning it from a callback stops that callback for that
    `(code, instruction_offset)` **permanently**, until `restart_events()`. It "does not change which
    events are set, or any other code locations for the same event" - VERSION-DEPENDENT (3.12+)
30. Through 3.14, returning `DISABLE` from a callback for a global/"other" event raises `ValueError`
    **"in a non-specific location (that is, no traceback will be provided)"** - an essentially
    undebuggable error - VERSION-DEPENDENT (3.12-3.14)
31. `restart_events()` is **global, not per-tool**. Any tool may re-arm every other tool's disabled
    locations, so a correct tool must tolerate receiving events it had disabled - VERSION-DEPENDENT (3.12+)
32. `BRANCH` is **deprecated in 3.14** in favour of `BRANCH_LEFT` / `BRANCH_RIGHT`, because
    "they can be disabled independently" and so give "much better performance" - VERSION-DEPENDENT (3.14)
33. Callback signatures differ per event and are positional. `PY_START`/`PY_RESUME`/`INSTRUCTION`:
    `(code, instruction_offset)`. `PY_RETURN`/`PY_YIELD`: `(code, instruction_offset, retval)`.
    `CALL`/`C_RAISE`/`C_RETURN`: `(code, instruction_offset, callable, arg0)` where `arg0` may be
    `MISSING`. **`LINE`: `(code, line_number)` - a line number, not an instruction offset.**
    `BRANCH_LEFT`/`BRANCH_RIGHT`/`JUMP`: `(code, instruction_offset, destination_offset)`. Exception
    events: `(code, instruction_offset, exception)` - VERSION-DEPENDENT (3.14)
34. Why it is cheaper than `settrace`/`setprofile`: PEP 669 states "If a small set of events are
    active, e.g. for a debugger, then the overhead of callbacks will be orders of magnitudes less
    than for `sys.settrace()` and much cheaper than using PEP 523." `settrace` is all-or-nothing per
    thread and fires on every line; `sys.monitoring` arms individual events per code object, so
    un-instrumented code keeps its specialised bytecode - ESTABLISHED
35. **`cProfile` is implemented on `sys.monitoring` from 3.12.** `Modules/_lsprof.c` in 3.12+ calls
    `sys.monitoring.use_tool_id`, `register_callback`, `set_events`, `free_tool_id`; the 3.11
    `_lsprof.c` contains zero references to monitoring. The tool id is hard-coded -
    `self->tool_id = PY_MONITORING_PROFILER_ID;` (= 2) - and registered under the name `"cProfile"` - VERSION-DEPENDENT (3.12+)
36. Consequence of 35: `cProfile.Profile().enable()` raises `ValueError` when tool id 2 is already
    held - by a second live `cProfile.Profile`, or by any third-party profiler that claimed
    `PROFILER_ID`. 3.14.7 shipped a related fix: "Fix `cProfile.Profile.enable` to no longer
    overwrite errors from `sys.monitoring`" (gh-153068) - VERSION-DEPENDENT (3.12+)
37. `coverage.py` uses `sys.monitoring` via its `sysmon` core, selectable with `COVERAGE_CORE=sysmon`
    or `core = sysmon` in config, and **it is the default on Python 3.14+** where supported. `sysmon`
    does not support plugins, dynamic contexts, or some concurrency libraries; on 3.12/3.13 it does
    not support branch coverage. FLAGGED-SECONDARY: the sysmon-is-default claim comes from
    coverage.readthedocs.io text surfaced via search rather than a fetched page; the 7.15.4 version and
    its 2026-08-06 date are from the PyPI JSON API - VERSION-DEPENDENT (3.14)
38. `pdb` gained a selectable backend in 3.14: `pdb.set_default_backend(backend)` and
    `pdb.get_default_backend()`, with backends `'settrace'` and `'monitoring'`. **The default is
    `'settrace'`** - VERSION-DEPENDENT (3.14)
39. But `pdb.rst` states verbatim: "`breakpoint()` and `set_trace()` will not be affected by this
    function. They always use `'monitoring'` backend." One interpreter therefore runs two different
    debugger cores depending on how pdb was entered - VERSION-DEPENDENT (3.14)
40. `bdb.Bdb` is the class that carries the `backend` argument; `pdb.Pdb` in 3.14 accepts `mode`,
    `backend` and `colorize` arguments - VERSION-DEPENDENT (3.14)

### C. Crash and hang diagnosis

41. `faulthandler.enable(file=sys.stderr, all_threads=True, c_stack=True)` installs handlers for
    exactly five signals: `SIGSEGV`, `SIGFPE`, `SIGABRT`, `SIGBUS`, `SIGILL`, plus a Windows
    exception handler since 3.6. `c_stack=True` is **new in 3.14** - VERSION-DEPENDENT (3.14)
42. Startup switches: `-X faulthandler` or `PYTHONFAULTHANDLER` (non-empty). Both route to
    `faulthandler.enable()` at startup, and `config_init` reads the env var via `config_get_env()`,
    so `PYTHONFAULTHANDLER=` (empty) is **unset**, not enabled - VERSION-DEPENDENT (3.3+)
43. faulthandler catches **fatal signals only**. It does **not** catch `SIGKILL`, `SIGSTOP`, OOM-kill,
    a clean `sys.exit()`, `MemoryError`, an uncaught Python exception, or a hang. For a hang you need
    `dump_traceback_later()`, `register()`, or an external attach - ESTABLISHED
44. `faulthandler.dump_c_stack(file=sys.stderr)` was added in 3.14; it "Dump[s] the C stack trace of
    the current thread". If the build or OS does not support it, "this prints an error in place of a
    dumped C stack" rather than raising - VERSION-DEPENDENT (3.14)
45. **3.14 free-threaded caveat, verbatim:** "Only the current thread is dumped if the GIL is disabled
    to prevent the risk of data races." So on a free-threaded build `all_threads=True` is silently
    downgraded and a crash dump shows one stack - VERSION-DEPENDENT (3.14)
46. `faulthandler.dump_traceback_later(timeout, repeat=False, file=sys.stderr, exit=False)` is the
    hang detector. "This function is implemented using a watchdog thread." The timer has sub-second
    resolution. Calling it twice replaces the parameters and resets the timeout - ESTABLISHED
47. `exit=True` in `dump_traceback_later()` calls `_exit()` with status 1: "Note `_exit()` exits the
    process immediately, which means it doesn't do any cleanup like flushing file buffers." Logs
    buffered in `logging` handlers or stdio are lost - ESTABLISHED
48. `faulthandler.register(signum, file=sys.stderr, all_threads=True, chain=False)` and
    `unregister(signum)` are **"Not available on Windows."** The `SIGUSR1`-dumps-a-stack pattern is
    POSIX-only - ESTABLISHED
49. faulthandler's output is deliberately crippled because it must be signal-safe: it cannot allocate
    heap memory, cannot use non-signal-safe functions, shows no source lines (filename, function
    name and line number only), truncates strings at 500 characters, caps at 100 frames and 100
    threads, mangles non-ASCII via `backslashreplace`, and prints most-recent-call **first**
    (reversed relative to a normal Python traceback) - ESTABLISHED
50. File-descriptor hazard: `enable()`, `dump_traceback_later()` and `register()` retain the *file
    descriptor*, not the file object. If that file is closed and the fd is reused, tracebacks are
    written into the wrong file. Re-call these functions whenever the sink is replaced - ESTABLISHED
51. Since 3.10 the dump "mentions if a garbage collector collection is running" when
    `all_threads` is true - a direct signal for "crashed inside a finalizer" - VERSION-DEPENDENT (3.10+)
52. 3.15 adds a `max_threads` parameter to `faulthandler.enable()`, `dump_traceback()`,
    `dump_traceback_later()` and `register()` (gh-149085) - VERSION-DEPENDENT (3.15)
53. In-process, dependency-free stack dump of every thread: `sys._current_frames()` returns a dict
    mapping thread id to the topmost frame, and its documented purpose is "debugging deadlocks
    without requiring cooperation from deadlocked threads". Render with `traceback.format_stack(frame)`.
    It raises the audit event `sys._current_frames` - ESTABLISHED
54. External stack out of a wedged process, ordered by cost, with no debugger client attached:
    (a) 3.15 stdlib: `python -m profiling.sampling dump PID` - "print a traceback-style stack of every
    thread (or all asyncio tasks with `--async-aware`). Useful for investigating hung processes.";
    (b) `py-spy dump --pid PID` (add `--locals`); (c) `austin -w PID` / `--where=PID`, which "Dump[s]
    the stacks of all the threads within the" target; (d) `gdb -p PID` with the py-* helpers;
    (e) `kill -SIGUSR1` if `faulthandler.register(signal.SIGUSR1)` was pre-installed;
    (f) `python -m asyncio pstree PID` for an async task tree. Option (a) needs 3.15 and option (f)
    needs 3.14; (b)-(e) are interpreter-version-independent - VERSION-DEPENDENT (3.15)
55. gdb helpers (`howto/gdb_helpers.html`, "Debugging C API extensions and CPython Internals with
    GDB"): the extension file is `python-gdb.py`, sourced from `Tools/gdb/libpython.py`, installed by
    distributions as `libpython3.14-gdb.py` or `python3.14-gdb.py`. Load via
    `add-auto-load-safe-path` in `~/.gdbinit` or `source /path/to/python-gdb.py`. Commands: `py-bt`,
    `py-bt-full`, `py-list`, `py-locals`, `py-print`, `py-up`, `py-down`. Requires gdb 7.0+ with
    Python support plus debug info (`dnf debuginfo-install python3`, `apt install python3-dbg`) - ESTABLISHED
56. `thread apply all py-bt` is the one-line "what is every thread doing at the Python level"
    command; it works on both a live `gdb -p PID` and a core file (`gdb /path/to/python /path/to/core`) - ESTABLISHED
57. Optimised builds degrade the gdb helpers: "Optimized builds may lose frame information", so
    `py-up` and `py-down` may be unable to read Python frame information. A release-optimised
    interpreter is a worse crash-analysis target than a `--with-pydebug` one - ESTABLISHED
58. Core dumps: nothing in Python configures them. They are an OS concern (`ulimit -c`,
    `/proc/sys/kernel/core_pattern`, systemd-coredump, Windows WER). faulthandler is compatible with
    system fault handlers like Apport and the Windows fault handler, and uses `sigaltstack()` where
    available so it can still dump on a stack overflow - ESTABLISHED
59. `PYTHONDUMPREFS` exists but only on a `--with-trace-refs` build; it "can dump objects and
    reference counts still alive at Python exit". Since 3.13 that build is **ABI compatible** with
    release and debug builds, which makes it usable against real wheels - VERSION-DEPENDENT (3.13+)
60. Async hangs: `python -m asyncio ps PID` prints a table of tasks with coroutine stacks and awaiter
    chains; `python -m asyncio pstree PID` prints the await tree. Both raise an error if the await
    graph contains cycles. Added in 3.14; both are built on the PEP 768 out-of-process machinery - VERSION-DEPENDENT (3.14)
61. In-process async introspection: `asyncio.capture_call_graph(future=None, /, *, depth=1,
    limit=None)`, `asyncio.format_call_graph(...)` and `asyncio.print_call_graph(future=None, /, *,
    file=None, depth=1, limit=None)`, returning `FutureCallGraph(future, call_stack, awaited_by)` and
    `FrameCallGraphEntry(frame)`. All added in 3.14 - VERSION-DEPENDENT (3.14)
62. The await graph is **not free**: code using low-level `Future.add_done_callback()` instead of
    `shield()`/`TaskGroup` must call `future_add_to_awaited_by()` and
    `future_discard_from_awaited_by()` itself, or it will be invisible in `ps`/`pstree` - VERSION-DEPENDENT (3.14)

### D. Memory diagnosis

63. `tracemalloc.start(nframe=1)` - the default of **1 frame** records only the allocating line, which
    is almost always a helper inside a library and useless for attribution. Set `nframe` to 10-25
    (`-X tracemalloc=25`, `PYTHONTRACEMALLOC=25`) if you intend to attribute a leak to a call site - VERSION-DEPENDENT (3.4+)
64. `tracemalloc` cannot see: allocations made **before** `start()`; allocations that do not go
    through `PyMem_*`/`PyObject_*` (a C extension calling `malloc()` directly, and most third-party
    native libraries); and memory already released before the snapshot - ESTABLISHED
65. `Snapshot.compare_to(old_snapshot, key_type, cumulative=False)` and
    `Snapshot.statistics(key_type, cumulative=False)` accept exactly three `key_type` values:
    `'filename'`, `'lineno'`, `'traceback'`. Leak attribution is the two-snapshot
    `compare_to(..., 'traceback')` diff, not a single snapshot - ESTABLISHED
66. `tracemalloc.get_object_traceback(obj)` maps a *live object you already hold* back to its
    allocation site - the correct tool once `gc`/`objgraph` has identified a suspect instance - ESTABLISHED
67. Other API: `stop()`, `is_tracing()`, `clear_traces()`, `get_traced_memory() -> (current, peak)`,
    `get_tracemalloc_memory()` (tracemalloc's own overhead), `reset_peak()` (added 3.9),
    `get_traceback_limit()`, `take_snapshot()`, `Snapshot.dump(filename)` /
    `Snapshot.load(filename)`, `Snapshot.filter_traces([...])`, `Filter(inclusive,
    filename_pattern, lineno=None, all_frames=False, domain=None)`, `DomainFilter(inclusive, domain)`
    (3.6), `Traceback.format(limit=None, most_recent_first=False)`, `Traceback.total_nframe` (3.9) - ESTABLISHED
68. Since 3.7 tracemalloc frames are ordered **oldest to most recent**; code written against 3.6 or
    earlier that indexes `traceback[0]` expecting the allocating line gets the outermost frame - VERSION-DEPENDENT (3.7+)
69. `ResourceWarning` only tells you *where the resource was allocated* if tracemalloc is on.
    Verbatim from `devmode.rst`: without it you get `ResourceWarning: Enable tracemalloc to get the
    object allocation traceback`; with `-X dev -X tracemalloc=5` you additionally get
    `Object allocated at (most recent call last): ...`. **`-X dev` alone is not enough** - VERSION-DEPENDENT (3.4+)
70. `gc` debug flags: `DEBUG_STATS`, `DEBUG_COLLECTABLE`, `DEBUG_UNCOLLECTABLE`, `DEBUG_SAVEALL`, and
    `DEBUG_LEAK`, which is exactly `DEBUG_COLLECTABLE | DEBUG_UNCOLLECTABLE | DEBUG_SAVEALL` - ESTABLISHED
71. `gc.DEBUG_SAVEALL` / `DEBUG_LEAK` **deliberately leak**: "all unreachable objects found will be
    appended to `garbage` rather than being freed". Setting `DEBUG_LEAK` in a long-running process is
    an unbounded memory leak by design - ESTABLISHED
72. `gc.garbage` "should be empty most of the time" since **3.4** (PEP 442): objects with `__del__`
    no longer end up there. A non-empty `gc.garbage` in 2026 means a C extension type with a
    non-`NULL` `tp_del`, or `DEBUG_SAVEALL`. A non-empty list at shutdown emits a `ResourceWarning`
    (silent by default) since 3.2 - ESTABLISHED
73. Reference-cycle hunting API: `gc.get_referrers(*objs)` (who points at this), `gc.get_referents(*objs)`
    (what this points at), `gc.get_objects(generation=None)`, `gc.is_tracked(obj)`,
    `gc.is_finalized(obj)` (3.9), `gc.get_stats()` (3.4), `gc.get_count()`, `gc.get_threshold()` /
    `set_threshold()`, `gc.freeze()` / `unfreeze()` / `get_freeze_count()` (3.7), `gc.callbacks` (3.3) - ESTABLISHED
74. `gc.get_referrers()` walks every tracked object, is O(heap), and will report the *investigating*
    frame, the debugger's frame, and interpreter-internal containers among the referrers. It is a
    last resort, not a routine probe - ESTABLISHED
75. Objects with no container semantics are not GC-tracked at all, so cycles cannot involve them and
    `gc.get_referrers()` will not find them; 3.14.7 shipped several "defer GC tracking" changes
    (`set.intersection`, `set.difference`, `array.array`), so `gc.is_tracked()` answers can differ
    between patch releases - VERSION-DEPENDENT (3.14.7)
76. **GC model churn in the 3.14 line.** 3.14.0-3.14.4 shipped an incremental collector: `gc.collect(1)`
    "performs an increment of collection", `set_threshold()`'s `threshold2` was ignored, and
    generation 1 was removed from `gc.get_objects()`. **3.14.5 reverted all three** to 3.13
    behaviour after "reports of significant memory pressure in production environments". Any code or
    runbook that keys off `gc.collect(1)` behaves differently on 3.14.0-3.14.4 than on 3.14.5+ - VERSION-DEPENDENT (3.14.5)
77. Free-threaded builds add a heuristic gate to collection: "If memory usage has not increased by
    10% since the last collection AND the net number of allocations has not exceeded 40 times
    `threshold0`, the collection is not run." Leak tests that assume `threshold0` alone triggers a
    collection are unreliable there - VERSION-DEPENDENT (3.13+, free-threaded)
78. `gc.freeze()` moves all currently tracked objects into a permanent generation exempt from
    collection - the standard pre-`fork()` call to stop copy-on-write pages being dirtied by a
    collection in each child - ESTABLISHED
79. Weakref-based leak detection is the cheapest always-on canary: hold `weakref.ref(obj)` (or
    `weakref.finalize(obj, callback)`) at a lifecycle boundary and assert the referent is `None`
    after the owner should have died. It needs no tracemalloc, no gc debug flags, and no external
    tool, and it survives in production. `WeakValueDictionary` / `WeakSet` registries give the same
    signal for populations - ESTABLISHED
80. **memray runs on Linux and macOS only.** Verbatim from its PyPI page: "Memray only works on Linux
    and MacOS, and cannot be installed on other platforms." Version 1.20.0 declares support for
    Python 3.9 through 3.15 - VERSION-DEPENDENT (memray 1.20.0)
81. memray subcommands: `memray run` (capture), then `flamegraph`, `table`, `tree`, `stats`,
    `summary`, `parse`; `memray live` for an interactive TUI. `memray run --native` adds C/C++
    allocation frames, which is the only way to attribute a leak inside a native dependency. The
    pytest plugin is `pytest-memray` (1.10.0), enabled with `--memray` - VERSION-DEPENDENT (memray 1.20.0)
82. Attributing a leak to a call site, in escalating order: (1) `weakref` canary proves an object
    outlives its scope; (2) `tracemalloc` two-snapshot `compare_to(..., 'traceback')` with
    `nframe >= 25` names the allocating stack; (3) `tracemalloc.get_object_traceback(obj)` on the
    specific suspect; (4) `gc.get_referrers(obj)` or `objgraph.show_backrefs` finds who is holding
    it; (5) `memray run --native` if the allocation is not visible to `PyMem_*` - ESTABLISHED
83. `PYTHONMALLOC=debug` (or `malloc_debug`, `pymalloc_debug`, `mimalloc_debug`) installs
    `PyMem_SetupDebugHooks` and detects buffer underflow, buffer overflow, memory-allocator API
    violation and unsafe GIL usage. On free-threaded builds only `default`, `debug`, `mimalloc` and
    `mimalloc_debug` are accepted - `malloc` and `pymalloc` are rejected - VERSION-DEPENDENT (3.13+)

### E. Profiling

84. `cProfile` and `profile` are **deterministic** profilers: "all *function call*, *function return*,
    and *exception* events are monitored, and precise timings are made for the intervals between
    these events". `cProfile` is the C implementation and the recommended one; `profile` is pure
    Python and exists mainly for extension - ESTABLISHED
85. **PEP 799 (Final, `Python-Version: 3.15`, Resolution 2025-08-21) reorganises stdlib profiling.**
    New package `profiling`, containing `profiling.tracing` (deterministic, relocated from
    `cProfile`) and `profiling.sampling` (statistical). `cProfile` "remains as an alias for backwards
    compatibility." `profile` is deprecated in 3.15 and **"will be removed in Python 3.17"** - VERSION-DEPENDENT (3.15)
86. PEP 799's deprecation schedule, verbatim: "In Python 3.15: importing `profile` emits a
    `DeprecationWarning`. In Python 3.16: all uses of `profile` emit a `DeprecationWarning`. In
    Python 3.17: the module will be removed from the standard library." - VERSION-DEPENDENT (3.15)
87. **A stdlib statistical sampling profiler now exists: `profiling.sampling`, codenamed Tachyon,
    added in 3.15.** It is not in 3.14 or any earlier release. As of 2026-08-08 it is available only
    in 3.15.0rc1 (2026-08-04); 3.15.0 final is scheduled for 2026-10-01 - VERSION-DEPENDENT (3.15)
88. `python -m profiling.sampling` has four subcommands, verified against
    `Lib/profiling/sampling/cli.py`: **`run`**, **`attach`**, **`dump`**, **`replay`** - VERSION-DEPENDENT (3.15)
89. The sampling-rate flag is **`-r` / `--sampling-rate`**, not `-i`/`--interval`. Source default is
    the string `"1khz"` (parsed by `_parse_sampling_rate` into `sample_interval_usec`), accepting
    forms like `10000`, `10khz`, `10k`. The whatsnew documents rates "up to **1,000,000 Hz**" - VERSION-DEPENDENT (3.15)
90. Modes: `--mode {wall|cpu|gil|exception}`, default `wall`. `wall` counts real elapsed time
    including I/O; `cpu` counts only active CPU execution; `gil` counts only time holding the GIL;
    `exception` samples only threads with an active exception - VERSION-DEPENDENT (3.15)
91. Output formats: `--pstats` (default, `pstats`-compatible), `--collapsed`, `--flamegraph`
    (self-contained HTML), `--gecko` (Firefox Profiler), `--heatmap`, `--jsonl`, `--binary`
    (`--compression auto|zstd|none`), `--diff-flamegraph BASELINE`, `--live` (terminal UI). Other
    flags: `-d/--duration`, `-a/--all-threads`, `--native`, `--no-gc`, `--opcodes`, `--subprocesses`,
    `--blocking`, `--realtime-stats`, `--async-aware`, `--async-mode {running|all}`, `-o/--output`,
    `--browser`, `--sort`, `-l/--limit`, `--no-summary` - VERSION-DEPENDENT (3.15)
92. Tachyon samples **externally**, so "The target process requires no modification and need not be
    restarted" and overhead on the target is "virtually zero". It requires the same
    debugger-level OS permissions as PEP 768 attach - VERSION-DEPENDENT (3.15)
93. Tachyon version coupling: the profiler and target must share the same Python **minor** version;
    pre-release versions must match exactly; and a free-threaded build cannot attach to a standard
    build or vice versa - VERSION-DEPENDENT (3.15)
94. Tachyon's numbers are estimates, stated verbatim: "The time values shown in Tachyon's output are
    **estimates derived from sample counts**, not direct measurements... With 100,000 samples, a
    function showing 5% has a margin of error of roughly plus/minus 0.5%. With only 1,000 samples,
    the same 5% measurement could actually represent anywhere from 3% to 7%." Short-lived functions
    can be missed entirely - VERSION-DEPENDENT (3.15)
95. `-X perf` enables the Linux perf trampoline: "the `perf` profiler will be able to report Python
    calls". Equivalent env var `PYTHONPERFSUPPORT=1`. Programmatic control:
    `sys.activate_stack_trampoline("perf")` / `sys.deactivate_stack_trampoline()` /
    `sys.is_stack_trampoline_active()`, all added in 3.12, Linux only. Precedence: the `sys`
    functions beat `-X`, which beats the env var. Default is "off" - VERSION-DEPENDENT (3.12+)
96. The trampoline works by interposing "a small piece of code compiled on the fly before the
    execution of every Python function" and teaching perf the mapping via **perf map files**. It is
    therefore not free while active, and it changes the shape of native stacks - ESTABLISHED
97. `-X perf` requires a frame-pointer build. Check with `python -m sysconfig | grep
    'no-omit-frame-pointer'` and `python -m sysconfig | grep HAVE_PERF_TRAMPOLINE`; build with
    `CFLAGS="-fno-omit-frame-pointer -mno-omit-leaf-frame-pointer"` - ESTABLISHED
98. `-X perf_jit` (added 3.13, env `PYTHON_PERF_JIT_SUPPORT`) is the DWARF variant for non-frame-pointer
    builds. It writes `/tmp/perf-$PID.dump` and needs a two-step pipeline:
    `perf record -F 9999 -g -k 1 --call-graph dwarf -o perf.data python -X perf_jit script.py`, then
    `perf inject -i perf.data --jit --output perf.jit.data`, then `perf report -g -i perf.jit.data`.
    It has "Higher overhead", needs `perf > v6.8` (or v6.7.2+), and for `-O0` builds the DWARF stack
    dump size must be raised (`--call-graph dwarf,65528`; default 8192) - VERSION-DEPENDENT (3.13+)
99. **PEP 831 (Final, 3.15) builds CPython with frame pointers by default** on supporting platforms,
    using `-fno-omit-frame-pointer` and `-mno-omit-leaf-frame-pointer`, and exposes them through
    `sysconfig` so extension modules inherit them. The PEP's own warning: "A single native component
    built without frame pointers can break stack unwinding for the whole Python process." - VERSION-DEPENDENT (3.15)
100. **py-spy 0.4.2 supports CPython 2.3-2.7 and 3.3-3.14 only** (its README states the range
     explicitly). It does **not** claim 3.15. Anything built on py-spy will fail against a 3.15
     interpreter until py-spy ships support - VERSION-DEPENDENT (py-spy 0.4.2)
101. py-spy subcommands: `py-spy record -o profile.svg --pid PID`, `py-spy top --pid PID`,
     `py-spy dump --pid PID` (add `--locals`). Flags: `--native`, `--subprocesses`, `--gil` (only
     threads holding the GIL), `--idle`, `--nonblocking`. On Linux, attaching to a process that is
     not a child "will usually require root"; the fix is `ptrace_scope` or `--cap-add SYS_PTRACE`
     (Docker) / a `SYS_PTRACE` capability (Kubernetes drops it by default) - VERSION-DEPENDENT (py-spy 0.4.2)
102. **Austin 4.0.0 supports Python 3.9-3.14** per its README compatibility table; not 3.15. Flags:
     `-i/--interval=n_us`, `-c/--cpu` (on-CPU stacks only; replaced the old `--sleepless`),
     `-C/--children`, `-m/--memory` (metric becomes the byte delta between samples),
     `-w/--where=PID` (dump all thread stacks), `-x/--exposure=n_sec`, `-P/--pipe`, `-o/--output`.
     **MOJO binary output is the default in 4.0**, so naive consumers of the old text format break.
     The `austinp` variant (Linux, `-DAUSTINP`) uses `ptrace` + `libunwind` for native frames - VERSION-DEPENDENT (austin 4.0.0)
103. On PyPI the name **`austin` is an unrelated 2016 package** ("austin scipy package", 2016.0.1);
     the real profiler distributes as **`austin-dist`** (4.0.0, 2025-11-01). `pip install austin`
     installs the wrong thing - VERSION-DEPENDENT (PyPI, checked 2026-08-08)
104. Scalene 2.3.0 (2026-05-12) declares `requires_python = "!=3.11.0,>=3.8"` - it explicitly
     excludes 3.11.0 exactly. pyinstrument is at 5.1.3 (2026-07-29) - VERSION-DEPENDENT (scalene 2.3.0, pyinstrument 5.1.3)
105. `-X pystats` and `PYTHONSTATS` exist only on a `--enable-pystats` build (macro `Py_STATS`),
     which also adds `sys._stats_on()`, `sys._stats_off()`, `sys._stats_clear()`, `sys._stats_dump()`.
     On a normal interpreter the `-X pystats` option does not exist - VERSION-DEPENDENT (3.11+)

### F. Interactive debugging

106. `breakpoint()` (3.7+) calls `sys.breakpointhook()`, whose default implementation consults
     **`PYTHONBREAKPOINT`**. Unset or empty means `"pdb.set_trace"`. A dotted path names any callable
     (`PYTHONBREAKPOINT=IPython.terminal.debugger.set_trace`). **`PYTHONBREAKPOINT=0` makes
     `breakpoint()` a no-op that returns immediately** - the correct way to neuter stray breakpoints
     in CI or production without editing code - VERSION-DEPENDENT (3.7+)
107. `pdb.set_trace(*, header=None, commands=None)`: `header` added 3.7, `commands` added 3.14.
     **In 3.13 `set_trace()` changed to enter the debugger immediately rather than on the next line**;
     code that relied on the old off-by-one lands somewhere else on 3.13+ - VERSION-DEPENDENT (3.13, 3.14)
108. Post-mortem: `pdb.post_mortem(t=None)` gained **support for exception objects in 3.13**
     (previously traceback objects only); `pdb.pm()` enters post-mortem on the exception in
     `sys.last_exc`. This is the shape of "debug a failure from an artefact" inside one process - VERSION-DEPENDENT (3.13)
109. pdb by version: 3.2 `-c/--command`; 3.7 `-m`, `breakpoint()`, `set_trace(header=)`; 3.11 `.pdbrc`
     read as UTF-8 rather than the system locale; 3.12 convenience variables (`$_frame`, `$_retval`,
     `$_exception`); 3.13 immediate `set_trace()`, exception objects in `post_mortem()`,
     `$_asynctask`; 3.14 `-p/--pid`, `set_trace(commands=)`, `Pdb(mode=, backend=, colorize=)`,
     `set_default_backend()`/`get_default_backend()`, `run`/`restart` disabled in inline mode; 3.15
     pdb uses the new interactive shell (PyREPL) as its default input shell - VERSION-DEPENDENT (3.15)
110. Print-debugging is a last resort in a diagnosable system for mechanical reasons, not stylistic
     ones: `print()` bypasses the level and filter machinery so it cannot be turned off per
     component; it emits to stdout, corrupting machine-readable output and pipelines; it carries no
     structured fields, so it cannot be correlated with a request or trace id; it is edited into and
     out of source, so the diagnostic is not reproducible from a released artefact; and it produces
     no traceback, no frame, and no post-mortem entry point. Every one of those is addressed by
     `logging` (see `logging_observability_manifest.md`) plus one of `breakpoint()`,
     `pdb.post_mortem()`, `faulthandler`, or an external sampler - ESTABLISHED

### G. Development-time switches

111. **`-X dev` / `PYTHONDEVMODE` turns on exactly seven things**, per `devmode.rst`: (1) the
     `default` warning filter, surfacing `DeprecationWarning`, `ImportWarning`,
     `PendingDeprecationWarning` and `ResourceWarning`; (2) memory-allocator debug hooks checking
     buffer underflow, buffer overflow, allocator API violation and unsafe GIL usage
     (`PYTHONMALLOC=debug`); (3) `faulthandler.enable()` at startup; (4) asyncio debug mode
     (`PYTHONASYNCIODEBUG=1`); (5) checking the `encoding` and `errors` arguments of encode/decode
     operations (3.9); (6) `io.IOBase.__del__` logging `close()` exceptions (3.8); (7)
     `sys.flags.dev_mode = True`. The docs summarise it as
     `PYTHONMALLOC=debug PYTHONASYNCIODEBUG=1 python -W default -X faulthandler` "but with
     additional effects" - VERSION-DEPENDENT (3.7+)
112. What `-X dev` does **not** do: it does not enable `tracemalloc` ("because the overhead cost (to
     performance and memory) would be too large"), does not enable `-X importtime` or
     `-X showrefcount`, does not turn warnings into errors, and "does not prevent the `-O` command
     line option from removing `assert` statements nor from setting `__debug__` to `False`" - ESTABLISHED
113. `-X dev` "can only be enabled at the Python startup"; there is no runtime toggle. Read it back
     with `sys.flags.dev_mode`. Its allocator hooks can be suppressed while keeping the rest by
     setting `PYTHONMALLOC=default` - ESTABLISHED
114. `-X importtime` prints module name, cumulative time and self time. **`-X importtime=2`, new in
     3.14, also reports already-loaded modules, printing the literal string `cached` in both time
     columns**; values other than `1` and `2` are reserved. Env equivalent
     `PYTHONPROFILEIMPORTTIME=1|2`. Documented caveat: "its output may be broken in multi-threaded
     application" - VERSION-DEPENDENT (3.14)
115. `-W` takes `action:message:category:module:lineno`. Actions: `default`, `error`, `always`, `all`
     (same as `always`), `module`, `once`, `ignore`; they may be abbreviated (`-Wi` == `-Wignore`).
     `message` must match the **whole** message, case-insensitively; `module` matches the fully
     qualified module name, case-**sensitively**; `lineno` 0 matches all lines. Empty fields match
     everything and trailing empty fields may be omitted - ESTABLISHED
116. Precedence traps in `-W`: with multiple `-W` options, "the action for the **last** matching
     option is performed", and **"Invalid `-W` options are ignored"** - a typo produces no error, only
     a note printed when the first warning is issued. `PYTHONWARNINGS` is a comma-separated list with
     "filters later in the list taking precedence over those earlier in the list" - ESTABLISHED
117. `-W error` is the switch that converts a warning into a test failure; `-X dev` only makes the
     warning *visible*. A test suite that wants deprecation warnings to fail the build needs
     `-W error` (or a pytest `filterwarnings = error` config), not `-X dev` - ESTABLISHED
118. `-X showrefcount` "only works on debug builds" (`--with-pydebug`). On a normal interpreter the
     option is accepted and silently does nothing. A debug build also adds
     `sys.gettotalrefcount()`, `d` to `sys.abiflags`, `-d`/`PYTHONDEBUG`, `__lltrace__`, and
     `Py_DEBUG`/`Py_REF_DEBUG` - VERSION-DEPENDENT (3.4+, debug build only)
119. `PYTHONVERBOSE` / `-v` prints a message each time a module is initialised, with the file or
     built-in it loaded from. **`-vv`** additionally prints a message for every file *checked* while
     searching for a module and reports module cleanup at exit. Since 3.10 `site` also reports
     site-specific paths and the `.pth` files it processed. `PYTHONVERBOSE` set to an integer is
     equivalent to repeating `-v` - ESTABLISHED
120. `-X presite=package.module` (3.13) imports a module before `site` and before `__main__` exists -
     the earliest available hook for installing diagnostics. It **requires a `--with-pydebug`
     build**; on a release interpreter the option does not exist. Env equivalent `PYTHON_PRESITE` - VERSION-DEPENDENT (3.13, debug build only)
121. `-X no_debug_ranges` / `PYTHONNODEBUGRANGES` (3.11) strips the end-line and column tables from
     code objects, which removes the `^^^^` fine-grained carets from tracebacks. Shipping it to
     shrink `.pyc` files silently degrades every future traceback - VERSION-DEPENDENT (3.11+)
122. `PYTHON_COLORS=1|0` (3.13) controls interpreter colourisation; `NO_COLOR` is honoured in 3.15.
     Colour codes in captured logs are a common cause of unreadable CI artefacts - VERSION-DEPENDENT (3.13+)
123. Sanitizer builds for native-extension diagnosis: `--with-address-sanitizer` (3.6, combine with
     `--without-pymalloc`), `--with-undefined-behavior-sanitizer` (3.6),
     `--with-thread-sanitizer` (3.13), `--with-valgrind` - VERSION-DEPENDENT (3.13+)

### H. Audit hooks and settrace as last resort

124. PEP 578 is **Final**, `Python-Version: 3.8`. API: `sys.audit(event, *args)`,
     `sys.addaudithook(hook)`, C-level `PySys_Audit()` and `PySys_AddAuditHook()`, plus the verified
     open hook `io.open_code(path)` / `PyFile_OpenCode()` / `PyFile_SetOpenCodeHook()`.
     The full event catalogue is `library/audit_events.html` - ESTABLISHED
125. **"Hooks cannot be removed or replaced."** There is no `removeaudithook`. An audit hook is a
     one-way, process-lifetime commitment - ESTABLISHED
126. Scope differs by registration path: C hooks added via `PySys_AddAuditHook()` are **global** and
     run first; Python hooks added via `sys.addaudithook()` are **per-(sub)interpreter** - ESTABLISHED
127. An exception raised in a hook is re-raised by `sys.audit()`, "later hooks are ignored", and "in
     general the Python runtime should terminate". A raising hook therefore *does* block the audited
     operation - but at the cost of an unrecoverable process, not a clean refusal - ESTABLISHED
128. **Audit hooks are not a sandbox.** PEP 578: "This is not sandboxing, as this proposal does not
     attempt to prevent malicious behavior." The `sys` docs add that hooks added from Python "can be
     trivially disable[d] or bypass[ed]" by malicious code; security-relevant hooks must be installed
     via the C API **before runtime initialisation**, and modules permitting arbitrary memory
     modification (`ctypes`) must be removed or watched - ESTABLISHED
129. `sys.addaudithook()` may silently fail: "If existing hooks raise `RuntimeError`, new hook is NOT
     added and exception is suppressed", so "Callers cannot assume hook was added". Since 3.8.1
     non-`RuntimeError` exceptions are no longer suppressed - VERSION-DEPENDENT (3.8.1+)
130. Cost of audit hooks with none installed: PEP 578 reports "the vast majority of benchmarks showing
     between 1.05x faster to 1.05x slower" - i.e. inside noise. The cost of a *registered* hook is
     paid on every audited event, and events like `object.__getattr__`, `import` and `open` are hot - ESTABLISHED
131. A Python audit hook is normally invisible to trace functions: "When tracing is enabled (via
     `settrace()`), Python hooks are only traced if callable has `__cantrace__` member set to a true
     value" - VERSION-DEPENDENT (3.8+)
132. `sys.settrace(tracefunc)` events are `'call'`, `'line'`, `'return'`, `'exception'`, `'opcode'`.
     **It never receives `'c_call'`, `'c_return'`, `'c_exception'`** - those go only to
     `sys.setprofile()`. Conversely `setprofile` never receives `'line'` - ESTABLISHED
133. `settrace` returns matter and `setprofile` returns do not: the trace function's return value
     becomes the local trace function for the new scope (`None` disables tracing for it), whereas
     the profile function's return "is ignored". Returning `None` from a trace function by accident
     silently drops all further events in that frame - ESTABLISHED
134. Per-frame throttles (3.7+): `frame.f_trace_lines = False` suppresses `'line'` events, and
     `frame.f_trace_opcodes = True` is required to get `'opcode'` events at all - VERSION-DEPENDENT (3.7+)
135. Both are **per-thread**. `threading.settrace()` / `threading.setprofile()` install a trace or
     profile function for threads created afterwards; `sys.settrace()` in the main thread does not
     reach worker threads. The docs also warn that "multiple threads cannot be reliably profiled due
     to inability to detect context switches" - ESTABLISHED
136. Both carry a CPython implementation-detail note: "intended only for implementing debuggers,
     profilers, coverage tools and the like", with behaviour "part of the implementation platform,
     rather than part of the language definition". They raise the audit events `sys.settrace` and
     `sys.setprofile`. Recursive tracing is disabled while the trace function runs; use
     `sys.call_tracing()` to trace deliberately - ESTABLISHED
137. On 3.12+ prefer `sys.monitoring` over `sys.settrace` for any new tool: `settrace` cannot be
     scoped to a subset of events or code objects, so it de-optimises the whole thread - VERSION-DEPENDENT (3.12+)
138. `sys.unraisablehook(unraisable)` is the only hook for exceptions the interpreter cannot raise -
     failures in `__del__`, in weakref callbacks, and during GC. The `unraisable` object carries
     `exc_type`, `exc_value`, `exc_traceback`, `err_msg`, `object`. Two documented hazards: storing
     `exc_value` "creates a reference cycle" (clear it), and storing `object` "can resurrect objects
     being finalized". A diagnosable system routes this to the log; the default only prints to
     stderr - VERSION-DEPENDENT (3.8+)
139. `threading.excepthook()` handles exceptions escaping `Thread.run()`; `sys.excepthook()` handles
     uncaught exceptions on the main thread. Both are needed for complete coverage - ESTABLISHED
140. `sys._getframe([depth])` raises `ValueError` if `depth` exceeds the stack, is documented as
     "For internal and specialized purposes only", is "Not guaranteed to exist in all Python
     implementations", and raises the audit event `sys._getframe`. `sys._getframemodulename([depth])`
     was added in 3.12 - VERSION-DEPENDENT (3.12+)

### I. Observability under a JIT, tail-call, or free-threaded build

141. **The JIT is still opt-in at build time on 3.15 and on `main`.**
     `--enable-experimental-jit=[no|yes|yes-off|interpreter]`, and
     "`--enable-experimental-jit=no` is the default behavior if the option is not provided". Runtime
     override `PYTHON_JIT=0|1` (`yes-off` builds it but starts disabled). PEP 744 remains **Draft**
     and says the JIT "is likely to remain [disabled by default] for the foreseeable future" - VERSION-DEPENDENT (3.13-3.16)
142. PEP 744 on Python-level observability: "Tools that profile and debug Python code will continue to
     work fine. This includes in-process tools that use Python-provided functionality (like
     `sys.monitoring`, `sys.settrace`, or `sys.setprofile`)" and "The behavior of Python code should
     be completely unchanged." - VERSION-DEPENDENT (3.13+)
143. PEP 744 on native observability: **"Profilers and debuggers for C code are currently unable to
     trace back through JIT frames."** So on a 3.13/3.14 JIT build, `perf`, `gdb` backtraces and
     native crash handlers stop at generated code - VERSION-DEPENDENT (3.13, 3.14)
144. **3.15 fixes exactly that, partially:** "The JIT compiler now publishes unwind information for
     generated machine code to the GDB interface on supported Linux ELF platforms. When libgcc frame
     registration is available, the same unwind information is also registered for GNU `backtrace()`
     stack walkers." The wording is scoped to Linux ELF plus GDB and `backtrace()` - it is not a
     blanket promise for `perf`, macOS, or Windows - VERSION-DEPENDENT (3.15)
145. **Hard incompatibility:** `sys.activate_stack_trampoline()` "Cannot be activated if JIT is
     active." `-X perf` and the JIT are mutually exclusive; the perf trampoline is not a way to profile
     a JIT build - VERSION-DEPENDENT (3.12+)
146. The tail-call interpreter is a separate axis: `--with-tail-call-interp`, added 3.14, opt-in,
     needs a compiler with proper tail calls and the `preserve_none` calling convention (Clang 19+),
     with PGO "highly recommended". The whatsnew calls it "an internal implementation detail with no
     visible behavior changes" - VERSION-DEPENDENT (3.14)
147. **But in 3.15 it stops being hypothetical on Windows: "the official Windows 64-bit binaries on
     python.org now use" the tail-calling interpreter** (enabled by a Visual Studio 2026 / MSVC 18
     feature). Native stack shapes and disassembly on the stock Windows build therefore differ from
     3.14 - VERSION-DEPENDENT (3.15)
148. Free-threaded build detection: `sys._is_gil_enabled()` for the runtime state, and
     `sysconfig.get_config_var("Py_GIL_DISABLED") == 1` for the build - the docs call the latter "the
     recommended mechanism for decisions related to the build configuration". `python -VV` and
     `sys.version` contain the string "free-threading build"; `sys.abiflags` gains `t` - VERSION-DEPENDENT (3.13+)
149. The GIL can come back without you asking: "The GIL may also automatically be enabled when
     importing a C-API extension module that is not explicitly marked as supporting free threading.
     A warning will be printed in this case." A "free-threaded" deployment can therefore be running
     with the GIL on, which invalidates any `--mode gil` profiling conclusion. Force with
     `-X gil=0|1` / `PYTHON_GIL`, where `-X gil` takes precedence - VERSION-DEPENDENT (3.13+)
150. **The sharpest free-threading diagnostics footgun, verbatim: "It is not safe to access
     `frame.f_locals` from a frame object if that frame is currently executing in another thread, and
     doing so may crash the interpreter."** This is exactly what a naive `sys._current_frames()` +
     `f_locals` dumper, or a `--locals` stack dump, does - VERSION-DEPENDENT (3.13+, free-threaded)
151. Also documented as not thread-safe under free threading: "it is generally not thread-safe to
     access the same iterator object from multiple threads concurrently, and threads may see
     duplicate or missing elements" - a source of phantom bugs that look like data corruption - VERSION-DEPENDENT (3.13+, free-threaded)
152. Free-threaded builds add thread-local bytecode, `-X tlbc=[0|1]` / `PYTHON_TLBC`, which appears in
     `--help-xoptions` only under `#ifdef Py_GIL_DISABLED`. It is **undocumented in the 3.14 branch's
     `Doc/using/cmdline.rst`** and documented only on `main`. Because each thread can hold its own
     copy of a code object's bytecode, tools that key on code-object identity or instruction offsets
     need `co_tlbc` / `tlbc_index` awareness - the debug-offsets header exposes
     `_Py_Debug_code_object_co_tlbc` and `_Py_Debug_interpreter_frame_tlbc_index` for precisely this - VERSION-DEPENDENT (3.14, 3.15)
153. `PYTHONMALLOC` is restricted under free threading: only `default`, `debug`, `mimalloc` and
     `mimalloc_debug` are accepted, and `--without-mimalloc` "Cannot be used with `--disable-gil`" - VERSION-DEPENDENT (3.13+)
154. Free-threaded single-threaded cost is stated in the 3.14 whatsnew as "roughly 5-10% depending on
     platform and C compiler" - relevant when a profile taken on a free-threaded build is used to
     justify an optimisation on a GIL build - VERSION-DEPENDENT (3.14)

### J. Self-diagnosis by design

155. A failure is reproducible from artefacts alone only when four things are recoverable **without
     the developer's machine**: (a) the exact interpreter (`sys.version`, `sys.implementation`,
     `sysconfig.get_config_var("Py_GIL_DISABLED")`, whether the JIT was on, whether it was a
     tail-call build); (b) the resolved configuration and the environment variables that changed
     interpreter behaviour (`-X` options are readable from `sys._xoptions`, dev mode from
     `sys.flags.dev_mode`); (c) the inputs, by content hash; (d) a stack. Each of (a)-(c) is a
     mechanically dumpable fact, and dumping them at startup is cheap - ESTABLISHED
156. A startup self-test's only defensible content is what cannot be checked statically and would
     otherwise fail late and confusingly: importability and version of every native dependency,
     writability of every configured path, reachability of every configured endpoint, and agreement
     between the config schema version and the code. This is not a substitute for tests; it converts
     a mid-run failure into a startup failure. No authoritative bar was found for how far a startup
     self-test should go; it is a project judgment call - OPEN
157. `assert` is the wrong mechanism for any invariant that must survive `-O`: `-O` removes `assert`
     statements and sets `__debug__` to `False`, and `-X dev` does **not** prevent that. Invariants
     that must hold in production need an explicit `if ...: raise` - ESTABLISHED
158. A maintenance/introspection interface should expose the same facts as the diagnostics above
     rather than a parallel truth: the interpreter and build identity (fact 155a), the effective
     config, the current `logging` levels per logger, `gc.get_stats()` / `gc.get_count()`,
     `tracemalloc.get_traced_memory()` when tracing is on, and a thread dump built from
     `sys._current_frames()` - all read-only. Introspection endpoints that *mutate* state
     (`gc.set_debug(gc.DEBUG_LEAK)`, `tracemalloc.start()`) must be separately gated: per fact 71 the
     first of those leaks by design - ESTABLISHED
159. Health endpoints and readiness/liveness split, invariant-check placement, and the exact
     structure of a maintenance interface have no authoritative Python-specific bar; treat the shape
     as a project decision and only the *facts it reports* as fixed - OPEN
160. The cheapest always-on diagnosability configuration for a Python service, all of it from the
     stdlib: `PYTHONFAULTHANDLER=1` (crash tracebacks), a `faulthandler.register(signal.SIGUSR1)`
     call on POSIX (on-demand thread dump), `sys.unraisablehook` and `threading.excepthook` routed
     into `logging`, `PYTHONBREAKPOINT=0` (no accidental breakpoints), and remote debugging left
     **enabled** so `pdb -p` and (on 3.15) `profiling.sampling attach` work when needed. Cost is
     approximately zero; each item is verified above - VERSION-DEPENDENT (3.14 baseline; 3.15 for the sampler)

## What changed since 2026-06-16

Real deltas, each dated by a primary source. The window is 2026-06-16 to 2026-08-08.

1. **CPython 3.14.7 released 2026-08-05** (`Misc/NEWS.d/3.14.7.rst`, `.. release date: 2026-08-05`).
   3.14.6 was 2026-06-10, so 3.14.7 is the first patch release inside the window. Diagnostics-relevant
   entries: "Fix undefined behaviour when a `sys.monitoring` callback raised an exception while the
   program was following a branch or loop" (gh-152375, dated 2026-06-27); "Fix
   `cProfile.Profile.enable` to no longer overwrite errors from `sys.monitoring`" (gh-153068, dated
   2026-07-05); several "Defer GC tracking" changes affecting `gc.is_tracked()` answers for `set`,
   `frozenset` and `array.array`; and a fix to a free-threaded data race in `gc.get_count`.
2. **Python 3.15.0rc1 released 2026-08-04** (PEP 790 schedule). Betas 2-4 (through 2026-07-18) and
   rc1 all landed inside the window; 3.15 is now feature-frozen and release-candidate, with final
   scheduled 2026-10-01. This is what makes the 3.15 diagnostics surface worth writing down now
   rather than treating as speculative.
3. **The stdlib now has a statistical sampling profiler in a release candidate.** PEP 799 (Final,
   Resolution 2025-08-21) landed as `profiling`, `profiling.tracing` and `profiling.sampling`
   (Tachyon) for 3.15; `docs.python.org/3.15/library/profiling.sampling.html` renders from
   3.15.0rc1. `profile` is deprecated with removal in 3.17. Before this window there was no released
   or release-candidate stdlib sampler to point an agent at.
4. **`python -m profiling.sampling dump PID` is now the stdlib answer for hung processes** - the
   3.15 whatsnew describes it as printing "a traceback-style stack of every thread (or all asyncio
   tasks with `--async-aware`). Useful for investigating hung processes." Previously this required
   py-spy, austin, or gdb.
5. **PEP 831 (Final, Resolution 2026-04-30) ships in 3.15**: CPython is built with
   `-fno-omit-frame-pointer -mno-omit-leaf-frame-pointer` by default, propagated through `sysconfig`.
   The PEP was resolved just before the window but first appears in a release candidate inside it.
6. **JIT frames become unwindable by GDB and GNU `backtrace()` on Linux ELF in 3.15** (gh-146071,
   gh-149104). PEP 744's "Profilers and debuggers for C code are currently unable to trace back
   through JIT frames" is now version-scoped rather than universal.
7. **The stock Windows 64-bit binary changes interpreter in 3.15**: "the official Windows 64-bit
   binaries on python.org now use" the tail-calling interpreter, via a Visual Studio 2026 / MSVC 18
   feature (gh-143068).
8. **`sys.monitoring` gains per-code-object control of the "other" events in 3.15** (gh-146182):
   `PY_THROW`, `PY_UNWIND`, `RAISE`, `EXCEPTION_HANDLED` and `RERAISE` can now be enabled and
   disabled per code object, and returning `DISABLE` from their callbacks disables the event for the
   whole code object "rather than raising `ValueError` as in prior versions".
9. **`faulthandler` gains `max_threads`** in 3.15 on `enable()`, `dump_traceback()`,
   `dump_traceback_later()` and `register()` (gh-149085).
10. **Tool releases inside the window**: memray 1.20.0 (2026-08-07) and pytest-memray 1.10.0
    (2026-08-07) - both one day before this fact pack; coverage.py 7.15.4 (2026-08-06); pyinstrument
    5.1.3 (2026-07-29). py-spy is unchanged at 0.4.2 (2026-04-24) and **still declares support only
    through 3.14**; austin is unchanged at 4.0.0 (2025-11-01) and **still declares support only
    through 3.14**. The sampler ecosystem has not yet caught up with 3.15.
11. **Not a delta, stated to prevent a wrong inference**: the incremental-GC reversion happened in
    **3.14.5, released 2026-05-10** - *before* this window. Anything written after 2026-05-10 should
    already describe `gc.collect(1)` as collecting the middle generation.
12. **Not a delta**: PEP 768, PEP 669 and PEP 578 statuses, the `-X`/env-var surface of 3.14, and the
    `--enable-experimental-jit=no` default are all unchanged in the window. The
    `-X disable_remote_debug` documentation bug (fact 13) is **still unfixed on both the 3.14 branch
    and `main` as of 2026-08-08**.

## Corrections to existing manifests

Target file(s): NEW: `python_runtime_diagnostics_manifest.md`

**No corrections.** The nine existing manifests in `E:/dev/corpora/manifests/` contain **zero**
occurrences of `faulthandler`, `tracemalloc`, `sys.monitoring`, `PEP 669`, `PEP 768`, `PEP 578`,
`py-spy`, `memray`, `austin`, `Scalene`, `cProfile`, `pdb`, `breakpoint()`, `PYTHONBREAKPOINT`,
`-X dev`, `PYTHONDEVMODE`, `-X importtime`, `-X showrefcount`, `settrace`, `setprofile`, `perf
trampoline`, `gc.set_debug`, `post-mortem` or `core dump` (verified by grep across all nine files on
2026-08-08). There is nothing stale to correct because there is nothing to correct - this is a
genuine gap, not a decayed section.

Two adjacent claims were checked specifically and are **accurate**, so they are recorded here as
verified-not-stale rather than corrected:

- `error_tracing_contract_manifest.md` §21 version matrix: `ExceptionGroup`/`except*` and
  `add_note`/`__notes__` at 3.11, callable `split`/`subgroup` condition at 3.13. Consistent with
  PEP 654 and PEP 678; no change.
- `error_tracing_contract_manifest.md` §14 and its open question on `-O`: "If `-O` is ever used,
  audit every must-survive check to confirm it is not an `assert`." Confirmed correct against
  `devmode.rst`, which states that Python Development Mode "does not prevent the `-O` command line
  option from removing `assert` statements nor from setting `__debug__` to `False`". The new
  diagnostics manifest should cross-reference this rather than restate it.

## New content the manifest set should carry

**1. Attach, don't restart: the PEP 768 remote-debug interface**
Destination: **NEW: `python_runtime_diagnostics_manifest.md`**
PEP 768 Final, 3.14; `sys.remote_exec(pid, script_path)` is the whole Python surface and it takes a
path, not source. The operator-facing entry point is `python -m pdb -p PID`. Pin the four coupling
constraints that make it fail in practice: same `major.minor` interpreter (exact match for
pre-releases), OS debugger permission (ptrace/Yama, `task_for_pid`, `SeDebugPrivilege`), loopback
reachability from target back to debugger because `pdb.attach()` opens a local server socket, and a
512-byte cap on the injected script path. State that the target must reach a bytecode boundary, so a
process blocked in a syscall is not attachable, and that `pdb -p` has no accept timeout. Record both
kill switches with the correct spelling (`-X disable-remote-debug`, hyphens) and the fact that an
empty `PYTHON_DISABLE_REMOTE_DEBUG` disables it. Name `cpython.remote_debugger_script` as the audit
event to hook if injection must be detected.

**2. `sys.monitoring` is the modern instrumentation substrate; six tool ids is the budget**
Destination: **NEW: `python_runtime_diagnostics_manifest.md`**
PEP 669 Final, 3.12. Six ids, 0-5; `DEBUGGER_ID`/`COVERAGE_ID`/`PROFILER_ID`/`OPTIMIZER_ID` are a
convention, 3 and 4 are free, and `use_tool_id` raises `ValueError` on collision. Give the three
event classes (local, ancillary, other) because only local events can be `DISABLE`d, and the exact
callback arities - `LINE` receives a line number, everything else an instruction offset. Note that
`cProfile` silently occupies `PROFILER_ID` on 3.12+ and coverage.py's `sysmon` core is the 3.14+
default, so the budget is already half-spent in a normal test run. State the 3.15 relaxation for
"other" events. Direct any new tool to `sys.monitoring` rather than `sys.settrace`.

**3. Crash, hang, and wedge: choosing among faulthandler, gdb, and out-of-process samplers**
Destination: **NEW: `python_runtime_diagnostics_manifest.md`**
A decision table keyed on the failure mode. Fatal signal -> `PYTHONFAULTHANDLER=1` (five signals
only; `c_stack=True` since 3.14; only the current thread on free-threaded builds). Suspected hang
with cooperation -> `faulthandler.dump_traceback_later(timeout, repeat=True)`, noting the watchdog
thread and that `exit=True` calls `_exit()` without flushing. Wedged with no prior instrumentation ->
`python -m profiling.sampling dump PID` (3.15), `py-spy dump`, `austin -w PID`, or
`gdb -p PID` + `thread apply all py-bt`. Async hang -> `python -m asyncio pstree PID`. In-process
thread dump -> `sys._current_frames()` + `traceback.format_stack`. Close with faulthandler's hard
limits (100 frames, 100 threads, 500 chars, no source lines, reversed order) so nobody expects a
normal traceback.

**4. Memory diagnosis: attributing a leak to a call site**
Destination: **NEW: `python_runtime_diagnostics_manifest.md`**
The five-step escalation of fact 82, with the two defaults that defeat beginners: `tracemalloc`
records **one** frame by default, and `ResourceWarning` only names the allocation site when
tracemalloc is running (`-X dev` alone is not enough). List what tracemalloc structurally cannot see.
Then `gc`: `DEBUG_LEAK` includes `DEBUG_SAVEALL` and therefore leaks on purpose; `gc.garbage` has
been empty since 3.4 except for C types with `tp_del`; `get_referrers` is O(heap) and reports the
investigator's own frames. Then the weakref canary as the only technique cheap enough to leave on.
Then memray for native allocations, with its Linux/macOS-only constraint stated plainly. Close with
the 3.14.0-3.14.4 vs 3.14.5+ `gc.collect(1)` split.

**5. Profiling: deterministic, statistical, and native, and when each lies**
Destination: **NEW: `python_runtime_diagnostics_manifest.md`**
`cProfile` measures every call and return, is per-thread, and holds `PROFILER_ID`. `profiling.sampling`
(3.15, `-r/--sampling-rate` default `1khz`, up to 1 MHz, `--mode wall|cpu|gil|exception`) measures
from outside with near-zero target overhead but reports estimates with a stated margin of error and
can miss short-lived functions. `-X perf` gives native+Python stacks on Linux only, needs frame
pointers (default from 3.15 per PEP 831), and **cannot be activated while the JIT is active**. Record
the four-subcommand CLI (`run`/`attach`/`dump`/`replay`) and the same-minor-version and
free-threaded-must-match constraints. Include the ecosystem lag: py-spy 0.4.2 and austin 4.0.0 both
stop at 3.14.

**6. Development-time switches: what each one actually turns on**
Destination: **NEW: `python_runtime_diagnostics_manifest.md`**
The exact seven effects of `-X dev`, plus the explicit non-effects (no tracemalloc, no importtime, no
`-W error`, no protection from `-O`). Then `-X importtime` / `=2` with the `cached` marker and the
multi-threaded caveat; `-W`'s `action:message:category:module:lineno` grammar with last-match-wins
and silently-ignored-invalid-options; `PYTHONWARNINGS` later-wins ordering; `-X showrefcount` and
`-X presite` as debug-build-only; `PYTHONVERBOSE` `-v` vs `-vv`; `-X no_debug_ranges` as a traceback
downgrade. State that `-X dev` is startup-only and readable from `sys.flags.dev_mode`.

**7. Audit hooks and trace functions as instruments of last resort**
Destination: **NEW: `python_runtime_diagnostics_manifest.md`**
PEP 578 Final, 3.8. Hooks cannot be removed; Python hooks are per-interpreter and trivially
bypassable; only `PySys_AddAuditHook()` before initialisation is security-relevant; audit hooks are
explicitly not a sandbox; a raising hook aborts the operation *and* should end the process. Then
`sys.settrace` vs `sys.setprofile`: disjoint event sets (`settrace` never sees `c_call`, `setprofile`
never sees `line`), return-value semantics that differ, per-thread scope requiring
`threading.settrace`, and `f_trace_lines`/`f_trace_opcodes`. Conclude: on 3.12+ new tools use
`sys.monitoring`; `settrace` is for reading, not writing.

**8. Diagnosability under a JIT, tail-call, or free-threaded build**
Destination: **NEW: `python_runtime_diagnostics_manifest.md`**
What becomes unreliable, with the version gate on each. JIT: Python-level tools unaffected per PEP
744; native unwinding broken on 3.13/3.14 and fixed for GDB and `backtrace()` on Linux ELF only in
3.15; `-X perf` mutually exclusive with the JIT; still `--enable-experimental-jit=no` by default
through `main`. Tail-call: opt-in in 3.14 but the default on the stock 3.15 Windows x64 binary.
Free-threaded: `faulthandler` dumps only the current thread; **`frame.f_locals` from a foreign
executing frame may crash the interpreter**; the GIL can be re-enabled silently by an unmarked C
extension, invalidating `--mode gil` conclusions; `-X tlbc` means bytecode identity is per-thread;
`PYTHONMALLOC` values are restricted.

**9. Self-diagnosis: reproducible from artefacts alone**
Destination: **NEW: `python_runtime_diagnostics_manifest.md`** (cross-references
`architecture_manifest_default.md` for the component/interface vocabulary and
`logging_observability_manifest.md` for the emission side)
The four recoverables - interpreter and build identity, effective configuration plus behaviour-
changing `-X`/env vars (`sys._xoptions`, `sys.flags.dev_mode`), content-hashed inputs, and a stack -
and the mechanical calls that produce each. A read-only introspection surface reporting the same
facts the diagnostics report, with any state-mutating probe (`gc.set_debug(DEBUG_LEAK)`,
`tracemalloc.start()`) separately gated because it changes memory behaviour. Invariants that must
survive `-O` cannot be `assert` - cross-reference `error_tracing_contract_manifest.md` §14. Mark
health-endpoint shape and startup self-test scope as OPEN project decisions.

**10. Cross-reference stub: diagnosis beyond logging**
Destination: `logging_observability_manifest.md` (new short section, near §13 checklists)
Six to ten lines only, no duplication: name the failure classes logging cannot address - fatal signal,
hang, leak, and "it is slow" - and point at the four stdlib mechanisms that do (`faulthandler`,
`sys._current_frames()`, `tracemalloc`, `profiling.sampling` / `cProfile`), plus
`sys.unraisablehook` and `threading.excepthook` as the two hooks a logging setup must claim or lose
exceptions entirely. Then defer to the new manifest.

## Traps for coding agents

1. **`-X disable_remote_debug` does nothing.** CPython's own docs use underscores; the implementation
   accepts only `-X disable-remote-debug` (hyphens), and unknown `-X` names are silently accepted.
   An agent that copies the documented spelling into a hardening checklist ships a no-op.
2. **`PYTHON_DISABLE_REMOTE_DEBUG=` (empty) disables remote debugging**, contradicting the docs'
   "non-empty string", because it is read with bare `getenv()` rather than `_Py_GetEnv()`. An empty
   value in a Dockerfile, `.env`, or Kubernetes manifest silently breaks `pdb -p` and (on 3.15)
   `profiling.sampling attach`. The opposite holds for `PYTHONFAULTHANDLER` and `PYTHONDEVMODE`,
   where empty means unset.
3. **`pdb -p PID` is not `gdb -p PID`.** It needs a bytecode boundary in the target (so a process
   blocked in a syscall is unreachable), loopback reachability *back* to the debugger, a readable
   temp script path under 512 bytes, and an exactly matching `major.minor` interpreter. There is no
   accept timeout, so failure looks like a hang.
4. **The pdb default backend is `'settrace'`, but `breakpoint()` and `pdb.set_trace()` always use
   `'monitoring'`.** `pdb.set_default_backend('monitoring')` does not change what `breakpoint()`
   does, and performance or tool-collision reasoning based on the default is wrong for the two most
   common entry points.
5. **`cProfile` silently claims `sys.monitoring` tool id 2 on 3.12+.** Two concurrent
   `cProfile.Profile` objects, or cProfile plus any tool that took `PROFILER_ID`, raise `ValueError`
   from `enable()`. Since coverage.py's `sysmon` core is the default on 3.14+, a `pytest --cov` run
   that also profiles is already contending for the six-id budget.
6. **Only *local* `sys.monitoring` events can be `DISABLE`d.** Returning `DISABLE` from a
   `RAISE`/`PY_UNWIND`/`RERAISE`/`EXCEPTION_HANDLED`/`PY_THROW` callback raises `ValueError`
   "in a non-specific location... no traceback will be provided" on 3.12-3.14. 3.15 changes this to
   disable per code object instead - so the same callback is a crash on 3.14 and correct on 3.15.
7. **`restart_events()` is global.** A tool that assumes its `DISABLE`d locations stay disabled will
   silently start receiving events again when an unrelated tool restarts them.
8. **`sys.monitoring`'s `LINE` callback receives a line number, every other callback an instruction
   offset.** Treating the second argument uniformly produces plausible, wrong output.
9. **`C_RETURN`/`C_RAISE` require `CALL` to be monitored.** Arming them alone yields silence, not an
   error.
10. **`tracemalloc.start()` defaults to `nframe=1`.** The one recorded frame is almost always inside
    a library helper. Leak attribution needs `start(25)` or `-X tracemalloc=25`, and the frame order
    changed to oldest-first in 3.7 so `traceback[0]` is the outermost frame, not the allocation site.
11. **`-X dev` does not enable `tracemalloc`.** `ResourceWarning` under `-X dev` prints only
    `Enable tracemalloc to get the object allocation traceback`. Both switches are needed.
12. **`-X dev` does not turn warnings into errors and does not defeat `-O`.** It adds the `default`
    filter; failing a build on a `DeprecationWarning` requires `-W error` or a pytest
    `filterwarnings` setting. And `-O` still strips `assert` statements under `-X dev`.
13. **`gc.DEBUG_LEAK` leaks.** It includes `DEBUG_SAVEALL`, which appends every unreachable object to
    `gc.garbage` instead of freeing it. Setting it in a long-running service is an unbounded leak
    introduced by the leak detector.
14. **`gc.collect(1)` means different things across 3.14 patch releases.** An increment of collection
    on 3.14.0-3.14.4, the middle generation on 3.13 and on 3.14.5+. `set_threshold`'s `threshold2`
    and generation 1 in `gc.get_objects()` moved with it.
15. **`faulthandler` catches five signals and nothing else.** Not `SIGKILL`, not the OOM killer, not
    `MemoryError`, not an uncaught Python exception, not a hang. An agent that installs faulthandler
    "for crashes" has not covered the most common production terminations.
16. **`faulthandler.register()` and `unregister()` do not exist on Windows.** The
    `kill -SIGUSR1`-to-dump-stacks runbook is POSIX-only.
17. **On free-threaded builds `faulthandler` dumps only the current thread**, regardless of
    `all_threads=True`, "to prevent the risk of data races".
18. **`faulthandler.dump_traceback_later(..., exit=True)` calls `_exit()`** - no buffer flushing, so
    buffered log records and stdio output are lost exactly when they matter most.
19. **faulthandler retains a file descriptor, not a file object.** Replace the sink and the tracebacks
    can land in an unrelated reused fd.
20. **`sys.settrace` never sees C calls and `sys.setprofile` never sees lines.** Choosing the wrong
    one produces a tool that is quietly blind to half of what it claims to measure.
21. **Trace-function return values are load-bearing; profile-function return values are ignored.**
    Returning `None` from a trace function disables tracing for that scope.
22. **`sys.settrace` is per-thread.** Without `threading.settrace()` a debugger or coverage tool sees
    nothing in worker threads. The same applies to `sys.setprofile`/`threading.setprofile` and to
    `cProfile`.
23. **`frame.f_locals` on a frame executing in another thread may crash a free-threaded
    interpreter.** Any `sys._current_frames()`-based dumper that also prints locals is a segfault
    waiting for concurrency.
24. **A "free-threaded" process may be running with the GIL on**, silently re-enabled by an unmarked
    C extension (with only a printed warning). Check `sys._is_gil_enabled()` before believing any
    GIL-mode profiling result.
25. **`sys.activate_stack_trampoline()` cannot be used while the JIT is active.** `-X perf` is not a
    way to profile a JIT build.
26. **On 3.13/3.14 JIT builds, native profilers and debuggers cannot unwind through JIT frames.**
    3.15 fixes this only for GDB and GNU `backtrace()` on supported Linux ELF platforms - not
    universally, not for `perf`, not on macOS or Windows.
27. **The JIT is not enabled by default anywhere**, including on `main`; `--enable-experimental-jit=no`
    is the default and PEP 744 is still Draft. Do not attribute observed behaviour to the JIT without
    checking `PYTHON_JIT` and the build.
28. **There is no `python -m profiling.sampling` before 3.15.** Do not emit it in a runbook targeting
    3.14, and note that as of 2026-08-08 3.15 exists only as rc1 (final scheduled 2026-10-01).
29. **The Tachyon rate flag is `-r`/`--sampling-rate` (default `"1khz"`), not `-i`/`--interval`.**
    The subcommands are exactly `run`, `attach`, `dump`, `replay`.
30. **Every out-of-process tool is version-coupled.** Tachyon requires the same Python minor version
    and the same free-threaded-vs-standard build. py-spy 0.4.2 declares 3.3-3.14 and austin 4.0.0
    declares 3.9-3.14, so **neither claims 3.15** - a "just use py-spy" recommendation breaks on the
    next release.
31. **`pip install austin` installs an unrelated 2016 scipy package.** The profiler is `austin-dist`.
32. **memray cannot be installed on Windows at all** ("Memray only works on Linux and MacOS, and
    cannot be installed on other platforms"), so it cannot be an unconditional dev dependency in a
    cross-platform project. Austin 4.0 also switched its default output to the binary MOJO format,
    breaking naive text parsers.
33. **`-X showrefcount` and `-X presite` require a debug build**; on a release interpreter they are
    accepted and do nothing. `-X pystats` requires `--enable-pystats`.
34. **Invalid `-W` options are silently ignored**, and with several filters the **last** match wins -
    the opposite of first-match-wins intuition. In `PYTHONWARNINGS`, later entries take precedence.
35. **`-X importtime` output "may be broken in multi-threaded application"** and `-X importtime=2`
     prints the literal string `cached` in both numeric columns - a parser expecting floats crashes.
36. **`sys.remote_exec()` gives no completion signal.** Deleting the script file immediately after the
    call is a race; the target may not have read it yet.
37. **Audit hooks cannot be removed, are per-interpreter when added from Python, are trivially
    bypassable, and are explicitly not a sandbox.** Using `sys.addaudithook()` as a security control
    is the canonical misuse; a raising hook takes the process down rather than refusing cleanly.
38. **`sys.addaudithook()` can fail silently** if an existing hook raises `RuntimeError` - the
    exception is suppressed and the hook is not added.
39. **`-X no_debug_ranges` / `PYTHONNODEBUGRANGES` removes the fine-grained caret markers from every
    future traceback.** Adopting it to shrink `.pyc` files is a permanent diagnosability trade.
40. **`gc.garbage` being empty is not evidence of no leaks.** It has been empty by design since 3.4
    (PEP 442) except for C types with a non-`NULL` `tp_del`. Cycles are collected, not reported there.

## Sources (accessed 2026-08-08)

- https://raw.githubusercontent.com/python/peps/main/peps/pep-0768.rst - PEP 768 header verbatim: Status Final, Created 25-Nov-2024, Python-Version 3.14, Resolution 17-Mar-2025
- https://peps.python.org/pep-0768/ - `sys.remote_exec` signature, `PYTHON_DISABLE_REMOTE_DEBUG` disabling on any value including empty string, `--without-remote-debug`, `_PyRemoteDebuggerSupport`, `_debugger_support` offsets, eval-breaker safe point, ptrace/`task_for_pid`/`PROCESS_VM_READ` permissions, path-not-code security rationale
- https://raw.githubusercontent.com/python/peps/main/peps/pep-0669.rst - PEP 669 header: Final, Created 18-Aug-2021, Python-Version 3.12
- https://peps.python.org/pep-0669/ - "orders of magnitudes less than for `sys.settrace()`", 6 tool ids, `DISABLE` semantics, `restart_events()` not tool-specific
- https://raw.githubusercontent.com/python/peps/main/peps/pep-0799.rst + https://peps.python.org/pep-0799/ - PEP 799 Final, Resolution 21-Aug-2025, Python-Version 3.15; `profiling`/`profiling.tracing`/`profiling.sampling`; `cProfile` alias retained; `profile` deprecation 3.15 -> 3.16 -> removal 3.17 (verbatim)
- https://raw.githubusercontent.com/python/peps/main/peps/pep-0831.rst - PEP 831 Final, Created 14-Mar-2026, Resolution 30-Apr-2026, Python-Version 3.15
- https://raw.githubusercontent.com/python/peps/main/peps/pep-0578.rst + https://peps.python.org/pep-0578/ - PEP 578 Final, 3.8; `sys.audit`/`sys.addaudithook`/`PySys_Audit`/`PySys_AddAuditHook`/`io.open_code`; "Hooks cannot be removed or replaced"; "This is not sandboxing"; 1.05x benchmark range
- https://raw.githubusercontent.com/python/peps/main/peps/pep-0744.rst + https://peps.python.org/pep-0744/ - PEP 744 still **Draft**, Informational, no Resolution; JIT not default; "Profilers and debuggers for C code are currently unable to trace back through JIT frames"; `sys.monitoring`/`settrace`/`setprofile` continue to work
- https://peps.python.org/pep-0790/ - Python 3.15 schedule: beta 1 2026-05-07 through beta 4 2026-07-18, rc1 2026-08-04, rc2 2026-09-01, final 2026-10-01; Status Active
- https://devguide.python.org/versions/ - 3.15 prerelease (2026-10-01), 3.14 bugfix (2025-10-07, EOL 2030-10), 3.13 bugfix, 3.12/3.11/3.10 security, 3.9 end-of-life; `main` targets 3.16
- https://www.python.org/downloads/ - Python 3.14.7 released 2026-08-05; Python 3.13.14 released 2026-06-10
- https://raw.githubusercontent.com/python/cpython/3.14/Misc/NEWS.d/3.14.7.rst - `.. release date: 2026-08-05`; gh-152375 `sys.monitoring` callback UB on branch/loop; gh-153068 `cProfile.Profile.enable` vs `sys.monitoring` errors; deferred GC tracking for set/frozenset/array; `gc.get_count` free-threaded data race
- https://raw.githubusercontent.com/python/cpython/3.14/Misc/NEWS.d/3.14.6.rst - `.. release date: 2026-06-10`; faulthandler double-import crash fix; `-X perf_jit` entry
- https://raw.githubusercontent.com/python/cpython/3.14/Misc/NEWS.d/3.14.5.rst - `.. release date: 2026-05-10`; `_remote_debugging` offset-table validation hardening (Security)
- https://raw.githubusercontent.com/python/cpython/3.14/Python/initconfig.c - `config_init_remote_debug()` reads `Py_GETENV("PYTHON_DISABLE_REMOTE_DEBUG")` and `config_get_xoption(config, L"disable-remote-debug")`; `Py_GETENV` defined as bare `getenv()`; `config_get_env` -> `_Py_GetEnv`; `usage_xoptions` text for every `-X` flag including the hyphenated `disable-remote-debug`, `pystats` under `#ifdef Py_STATS`, `tlbc` under `#ifdef Py_GIL_DISABLED`
- https://raw.githubusercontent.com/python/cpython/main/Python/initconfig.c - the hyphenated `disable-remote-debug` lookup persists on `main`
- https://raw.githubusercontent.com/python/cpython/3.14/Python/preconfig.c - `_Py_GetEnv()` body: returns `NULL` when `var[0] == '\0'`
- https://raw.githubusercontent.com/python/cpython/3.14/Doc/using/cmdline.rst and .../main/Doc/using/cmdline.rst - the documented (incorrect) `-X disable_remote_debug` spelling and the "non-empty string" wording for `PYTHON_DISABLE_REMOTE_DEBUG`, on both branches; `-X tlbc` documented only on `main`
- https://docs.python.org/3/using/cmdline.html - exact semantics and versionadded for `-X dev`, `faulthandler`, `importtime`/`=2`, `showrefcount`, `tracemalloc[=N]`, `perf`, `perf_jit`, `gil`, `presite`, `cpu_count`, `no_debug_ranges`, `thread_inherit_context`, `context_aware_warnings`; `-W` grammar and action list; `PYTHONVERBOSE` `-v`/`-vv`; `PYTHONMALLOC` values and free-threaded restriction; `PYTHONBREAKPOINT` including the `"0"` no-op; `PYTHONPERFSUPPORT`, `PYTHON_PERF_JIT_SUPPORT`, `PYTHON_JIT`, `PYTHON_GIL`, `PYTHON_COLORS`
- https://docs.python.org/3/library/pdb.html + https://raw.githubusercontent.com/python/cpython/3.14/Doc/library/pdb.rst - `python -m pdb [-c command] (-m module | -p pid | pyfile)`; `-p/--pid` versionadded 3.14 and the blocked-in-syscall note verbatim; `set_default_backend`/`get_default_backend` with default `'settrace'` and the "always use `'monitoring'`" note; `set_trace(header=, commands=)`; 3.13 immediate-entry change; `post_mortem` exception-object support
- https://raw.githubusercontent.com/python/cpython/3.14/Lib/pdb.py - `__all__` without `attach`; `attach()` body (`socket.create_server(("localhost", 0))`, temp connect script, chmod +r group/other, `sys.remote_exec`, `server.accept()` with the "TODO Add a timeout?" comment); `use_signal_thread = sys.platform == "win32"`; `_PdbServer.protocol_version()`
- https://docs.python.org/3/library/sys.monitoring.html + https://raw.githubusercontent.com/python/cpython/3.14/Doc/library/sys.monitoring.rst - tool ids 0-5 and the four named constants; `use_tool_id` "Raises a `ValueError` if `tool_id` is in use"; `clear_tool_id` vs `free_tool_id`; local/ancillary/other event partition; `BRANCH` deprecated in 3.14; per-event callback signatures; `DISABLE` global-event `ValueError` "in a non-specific location"; `NO_EVENTS`; `MISSING`
- https://raw.githubusercontent.com/python/cpython/3.14/Modules/_lsprof.c - `self->tool_id = PY_MONITORING_PROFILER_ID;`, `use_tool_id(..., "cProfile")`, `register_callback`, `set_events`, `free_tool_id`; the callback table mapping `PY_MONITORING_EVENT_*` to methods
- https://raw.githubusercontent.com/python/cpython/3.11/Modules/_lsprof.c and .../3.12/Modules/_lsprof.c - zero vs 31 references to monitoring, dating the cProfile switch to 3.12
- https://raw.githubusercontent.com/python/cpython/3.12/Doc/whatsnew/3.12.rst - PEP 669 section; `sys.activate_stack_trampoline`/`deactivate_stack_trampoline` added
- https://docs.python.org/3/library/faulthandler.html + https://raw.githubusercontent.com/python/cpython/3.14/Doc/library/faulthandler.rst - `enable(file, all_threads=True, c_stack=True)`; `dump_c_stack()` versionadded 3.14; the five signals; 3.14 "Only the current thread is dumped if the GIL is disabled to prevent the risk of data races" verbatim; `dump_traceback_later` watchdog thread, sub-second resolution, `exit=True` -> `_exit()` without flushing; `register`/`unregister` "Not available on Windows"; the limitation list (100 frames, 100 threads, 500 chars, no heap allocation, no source lines, reversed order); the file-descriptor hazard; 3.10 GC-running note
- https://docs.python.org/3/library/devmode.html + https://raw.githubusercontent.com/python/cpython/3.14/Doc/library/devmode.rst - the complete seven-item effects list; the `PYTHONMALLOC=debug PYTHONASYNCIODEBUG=1 python -W default -X faulthandler` summary; "does not enable the `tracemalloc` module by default"; "does not prevent the `-O` command line option from removing `assert` statements"; startup-only + `sys.flags.dev_mode`; the `ResourceWarning: Enable tracemalloc to get the object allocation traceback` vs `Object allocated at` worked example
- https://docs.python.org/3/library/tracemalloc.html - `start(nframe=1)`, `stop`, `is_tracing`, `clear_traces`, `get_traced_memory`, `get_tracemalloc_memory`, `reset_peak` (3.9), `take_snapshot`, `get_object_traceback`, `get_traceback_limit`; `Snapshot.compare_to`/`statistics` with `key_type` in `'filename'|'lineno'|'traceback'`; `Filter`/`DomainFilter`; `Traceback.format`/`total_nframe`; 3.7 frame-order change; the limitations list
- https://docs.python.org/3/library/gc.html - full API signatures; `DEBUG_*` constants and `DEBUG_LEAK = DEBUG_COLLECTABLE | DEBUG_UNCOLLECTABLE | DEBUG_SAVEALL`; `gc.garbage` empty since 3.4 (PEP 442) except C types with non-`NULL` `tp_del`; 3.2 shutdown `ResourceWarning`; the 3.14 incremental-GC behaviour and its 3.14.5 reversion; threshold semantics; the free-threaded 10%/40x collection gate
- https://docs.python.org/3/library/sys.html - `settrace`/`setprofile` event sets and the C-call asymmetry; return-value semantics; `f_trace_lines`/`f_trace_opcodes` (3.7); per-thread scope and `threading.settrace`; `sys._current_frames()` "debugging deadlocks without requiring cooperation from deadlocked threads"; `sys._getframe`/`_getframemodulename` (3.12); `sys.remote_exec` availability, same-`major.minor` requirement and both audit events (`sys.remote_exec`, `cpython.remote_debugger_script`); `activate_stack_trampoline("perf")`/`deactivate`/`is_active` (3.12, Linux only) and **"Cannot be activated if JIT is active"**; `sys.addaudithook` not-a-sandbox and silent-failure notes; `__cantrace__`; `sys.unraisablehook` attributes and its cycle/resurrection hazards
- https://docs.python.org/3/whatsnew/3.14.html - PEP 768 section with `sys.remote_exec`, `python -m pdb -p 1234`, `PYTHON_DISABLE_REMOTE_DEBUG`, `--without-remote-debug`; `python -m asyncio ps` / `pstree` with sample output; `--with-tail-call-interp` (Clang 19+, 3-5% pyperformance, opt-in); PEP 779 free-threading officially supported and the 5-10% single-thread penalty; `faulthandler.dump_c_stack`; `-X importtime=2`; the incremental GC and its 3.14.5 reversion
- https://raw.githubusercontent.com/python/cpython/main/Doc/whatsnew/3.15.rst + https://docs.python.org/3.15/whatsnew/3.15.html - Tachyon section verbatim (up to 1,000,000 Hz; `run`/`attach`/`dump` modes; the four `--mode` values; every output format; "Useful for investigating hung processes"); PEP 799 reorganisation and `profile` removal in 3.17; PEP 831 frame-pointers-by-default with the single-component warning; `sys.monitoring` per-code-object "other" events (gh-146182); `faulthandler` `max_threads` (gh-149085); the JIT upgrade list including "GDB and GNU `backtrace()` unwinding support" (gh-146071, gh-149104); the MSVC 18 Windows tail-calling interpreter (gh-143068)
- https://docs.python.org/3.15/library/profiling.sampling.html - subcommand synopsis, permission requirements (ptrace/Yama, macOS entitlement, `SeDebugPrivilege`), "The target process requires no modification and need not be restarted", same-minor-version and free-threaded-must-match constraints, the sample-count margin-of-error passage
- https://raw.githubusercontent.com/python/cpython/main/Lib/profiling/sampling/cli.py - the exact flag inventory: `-r/--sampling-rate` with source default `"1khz"` (not `-i/--interval`); `-d/--duration`, `-a/--all-threads`, `--blocking`, `--native`, `--no-gc`, `--opcodes`, `--realtime-stats`, `--subprocesses`, `--mode`, `--async-aware`, `--async-mode`, `--pstats`, `--collapsed`, `--flamegraph`, `--diff-flamegraph`, `--gecko`, `--heatmap`, `--jsonl`, `--binary`, `--compression`, `-o/--output`, `--browser`, `--sort`, `-l/--limit`, `--no-summary`; subcommands `run`, `attach`, `dump`, `replay`
- https://docs.python.org/3/howto/perf_profiling.html - the three activation paths and their precedence; `perf record -F 9999 -g`; the `-k 1 --call-graph dwarf` + `perf inject --jit` pipeline; perf map files and `/tmp/perf-$PID.dump`; frame-pointer CFLAGS and the `sysconfig` checks (`no-omit-frame-pointer`, `HAVE_PERF_TRAMPOLINE`); perf > v6.8 requirement; `--call-graph dwarf,65528` for `-O0`
- https://docs.python.org/3/howto/remote_debugging.html - "Remote debugging attachment protocol": per-platform `PyRuntime` location, `_Py_DebugOffsets` cookie/version/free_threaded validation, `debugger_script_path` + `debugger_pending_call` + eval-breaker bit 5 (`_PY_EVAL_PLEASE_STOP_BIT`), suspend-target recommendation, not-a-stable-ABI statement
- https://raw.githubusercontent.com/python/cpython/3.14/Include/internal/pycore_debug_offsets.h - `#define _Py_Debug_Cookie "xdebugpy"`; `_Py_Debug_Free_Threaded`; `_Py_Debug_code_object_co_tlbc` and `_Py_Debug_interpreter_frame_tlbc_index`; `debugger_script_path` / `debugger_script_path_size` offsets
- https://raw.githubusercontent.com/python/cpython/3.14/Include/cpython/pystate.h - `#define _Py_MAX_SCRIPT_PATH_SIZE 512` and `char debugger_script_path[_Py_MAX_SCRIPT_PATH_SIZE];`
- https://docs.python.org/3/howto/gdb_helpers.html - "Debugging C API extensions and CPython Internals with GDB": `python-gdb.py`, `Tools/gdb/libpython.py`, `libpython3.14-gdb.py`/`python3.14-gdb.py`, `add-auto-load-safe-path` and `source`; `py-bt`, `py-bt-full`, `py-list`, `py-locals`, `py-print`, `py-up`, `py-down`; gdb 7.0+ with Python support, debuginfo packages; optimised builds losing frame info; `gdb -p PID`, core files, `thread apply all py-bt`
- https://devguide.python.org/development-tools/gdb/ - redirects gdb guidance to `howto/gdb_helpers.html`
- https://docs.python.org/3/using/configure.html + https://raw.githubusercontent.com/python/cpython/main/Doc/using/configure.rst - `--enable-experimental-jit=[no|yes|yes-off|interpreter]` with `no` as the default on both 3.14 and `main`; `--with-tail-call-interp` (3.14); `--disable-gil`; `--without-remote-debug` and `Py_REMOTE_DEBUG`; `--with-pydebug` and the debug-build effect list; `--with-trace-refs` (`Py_TRACE_REFS`, `sys.getobjects()`, `PYTHONDUMPREFS`, ABI-compatible since 3.13); `--enable-pystats` and the `sys._stats_*` functions; the sanitizer options; `--without-mimalloc` incompatible with `--disable-gil`
- https://docs.python.org/3/library/profile.html + https://raw.githubusercontent.com/python/cpython/3.14/Doc/library/profile.rst - the definition of deterministic profiling versus statistical profiling; `cProfile` recommended over `profile`
- https://docs.python.org/3/library/asyncio-graph.html - "Call graph introspection": `capture_call_graph`, `format_call_graph`, `print_call_graph` (all 3.14), `FutureCallGraph`, `FrameCallGraphEntry`, and the `future_add_to_awaited_by`/`future_discard_from_awaited_by` requirement for low-level code
- https://docs.python.org/3/howto/free-threading-python.html - `sys._is_gil_enabled()`, `sysconfig.get_config_var("Py_GIL_DISABLED")`, `python -VV` / `sys.version` containing "free-threading build"; `-X gil` / `PYTHON_GIL`; automatic GIL re-enablement on importing an unmarked C extension with a printed warning; **"It is not safe to access `frame.f_locals` from a frame object if that frame is currently executing in another thread, and doing so may crash the interpreter"**; the iterator thread-safety warning
- https://pypi.org/pypi/memray/json + https://pypi.org/project/memray/ - 1.20.0 released 2026-08-07; "Memray only works on Linux and MacOS, and cannot be installed on other platforms"; Python 3.9-3.15; `run`/`flamegraph`/`table`/`tree`/`stats`/`summary`/`live`/`parse`; `--native`
- https://pypi.org/pypi/pytest-memray/json - 1.10.0 released 2026-08-07
- https://pypi.org/pypi/py-spy/json + https://raw.githubusercontent.com/benfred/py-spy/master/README.md - 0.4.2 released 2026-04-24; "versions 2.3-2.7 and 3.3-3.14"; `record`/`top`/`dump` with `--locals`, `--native`, `--subprocesses`, `--gil`, `--idle`, `--nonblocking`; root/`ptrace_scope` requirement for non-child attach; `SYS_PTRACE` for Docker and Kubernetes
- https://pypi.org/pypi/austin-dist/json + https://raw.githubusercontent.com/P403n1x87/austin/master/README.md - austin-dist 4.0.0 released 2025-11-01; compatibility table "3.9-3.14 | 4.0"; `-i/--interval`, `-c/--cpu`, `-C/--children`, `-m/--memory`, `-w/--where=PID`, `-x/--exposure`, `-P/--pipe`, `-o/--output`; MOJO default output; the `austinp` ptrace+libunwind variant
- https://pypi.org/pypi/austin/json - the PyPI name `austin` is an unrelated 2016 package (2016.0.1, "austin scipy package")
- https://pypi.org/pypi/scalene/json - 2.3.0 released 2026-05-12, `requires_python = "!=3.11.0,>=3.8"`
- https://pypi.org/pypi/pyinstrument/json - 5.1.3 released 2026-07-29
- https://pypi.org/pypi/coverage/json - 7.15.4 released 2026-08-06, `requires_python >= 3.10`
- https://pypi.org/pypi/objgraph/json - 3.6.2 released 2024-10-10
- https://coverage.readthedocs.io/en/latest/ (via search result text, FLAGGED-SECONDARY) - `COVERAGE_CORE=sysmon` / `core = sysmon`; sysmon is the default on Python 3.14+ where supported; no plugin, dynamic-context or full concurrency support; no branch coverage on 3.12/3.13
