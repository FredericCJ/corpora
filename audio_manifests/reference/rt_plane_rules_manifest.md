# Real-Time Plane Rules — Ground-Truth Manifest

**Purpose.** The operational law of the real-time plane: the thread inventory, the banned-operations table, the bounded-work discipline, the guard machinery that enforces them, the per-thread FP regime, the four blessed memory-ordering idioms, the syscall classification, and the honest contract-only residue.

Facts verified 2026-08-12. Version-dependent claims route to reference/audio_platform_baseline_manifest.md (the hub); if any file disagrees with the hub, the hub wins.

Reasoning root: the child booklet `realtime-audio-pc-architecture-and-design-r1.md` (repo root). This file operationalizes booklet sections 2.2, 6.1–6.2, 6.6–6.7, 9.6, 15.2 and invariants 1–4, 13–14; it never re-argues them.

**Tag legend.** ESTABLISHED (named primary source) · VERSION-DEPENDENT (- hub H\<n\>) · MEASURED (this machine, 2026-08-12, command recorded) · OPEN (ASSUMED / NEEDS-INPUT) · CC-FACT (model knowledge of API/OS mechanics, no named primary source — verify pointer given where it matters). Every RULE row names one of the seven enforcement routes.

---

## R1. The two planes and the thread inventory

One line through the process: on one side every thread the device clock paces — the **real-time plane**; on the other, everything else — the **control plane** [ESTABLISHED: booklet section 2.2]. Every rule in this file does one of two jobs: keep the RT plane bounded, or move data across the line without poisoning it. On the RT plane, invariant 1 is law: no lock, no allocation, no blocking syscall, no I/O, no unbounded loop — bounded work, wait-free communication, pre-claimed memory, nothing else [ESTABLISHED: booklet ch. 3, invariant 1].

### The thread role inventory

The process thread population is a **closed, named inventory — a composition-root fact, not an emergent property** [ESTABLISHED: booklet section 6.1]:

| role | plane | created | waits on | may block? |
|---|---|---|---|---|
| device loop (one per stream) | RT | composition root | the device's pacing signal **only** (reference/device_adapter_manifest.md sections D3, D7) | only there |
| RT workers (fixed pool) | RT | composition root | the fork-join gate (eventcount — reference/concurrency_channels_manifest.md section C7) | only there |
| control (UI, session, device juggling) | control | composition root | anything | freely |
| streaming worker (disk prefetch/spool) | control | composition root | its request queue | freely |
| telemetry drain | control | composition root | the flight ring's drain cadence (reference/observability_flightring_manifest.md section O6) | freely |

Operational law: **non-stop-forwarding** — the RT plane keeps rendering when the control plane stalls, hangs, or restarts. A frozen UI must produce frozen *meters*, never frozen *audio*; that sentence is the architecture's acceptance test and it is testable — reference/testing_verification_manifest.md section T7 injects a stalled control plane and asserts the stream [ESTABLISHED: booklet section 6.1].

### Rules

| # | rule | route |
|---|---|---|
| R1.1 | Every thread's plane is **declared at creation**: the thread adapter sets the plane tag (R4) and embeds the plane in the thread's OS-visible name. "A thread whose plane nobody stated is a real-time defect that hasn't happened yet" [ESTABLISHED: booklet section 2.2]. | contract-only (inventory reviewed by name, R8) + runtime-catchable (the guard requires the tag) |
| R1.2 | The inventory is closed: a go-live assert compares the live thread census against the composition root's declared list and refuses go-live on mismatch (self-locating failure per reference/error_tracing_contract_manifest.md section E6). | runtime-catchable |
| R1.3 | **The RT population is fixed between go-live and teardown.** No thread creation, destruction, or plane migration while the stream is live. Changing the RT population is a stream-contract reconfiguration: fade, stop, join, rebuild, relock, re-elevate, restart — the shutdown protocol, reference/concurrency_channels_manifest.md section C9 [ESTABLISHED: booklet section 6.8]. | runtime-catchable (wrap net traps thread-create syscalls on the RT plane, R4) + contract-only |
| R1.4 | Each thread's **waiting policy is declared at creation** and matches its row above: device loop blocks in exactly one place, never sleeps, never yields, never polls; workers park on the eventcount; control threads take ordinary bounded waits [ESTABLISHED: booklet section 6.7]. | contract-only (R8) + compiler-catchable (sleep/yield poison, R2) |
| R1.5 | Go-live order: residency asserts (invariant 3, reference/memory_residency_manifest.md sections M5–M6), elevation verified with denial-as-a-mode (invariant 14; hub H7), FTZ/DAZ verified (R5), **then** the guard arms (R4). | runtime-catchable |

Thread-name scheme [OPEN — ASSUMED]: `rt_dev<n>`, `rt_wrk<n>`, `ct_<role>` prefixes, so crash dumps and session reports self-locate by name (reference/error_tracing_contract_manifest.md section E8). Pin it in the project spec.

### The thread port's creation contract

Plane, name, and wait policy are **fields of the creation descriptor**, not conventions — the adapter cannot create a thread whose plane nobody stated (R1.1) [OPEN — ASSUMED shape; the thread port's full signature is owned by the port list, booklet ch. 5]:

```c
typedef enum { WAIT_DEVICE_SIGNAL, WAIT_EVENTCOUNT, WAIT_BLOCKING_OK } rt_wait_kind_t;

typedef struct {
    const char     *name;        /* "rt_wrk3": plane prefix, visible in dumps (E8) */
    rt_plane_t      plane;       /* PLANE_RT | PLANE_CONTROL — sets the R4 tag    */
    rt_wait_kind_t  waits_on;    /* must match the R1 inventory row               */
    size_t          stack_bytes; /* fixed, locked for RT (M7)                     */
    int             elevation;   /* request verified at go-live (invariant 14)    */
    void          (*entry)(void *);
    void           *arg;
} rt_thread_desc_t;
```

The adapter's thread-start hook runs, in order: set plane tag → set thread name → apply elevation request → `rt_thread_fp_init()` if RT (R5) → call `entry`. One adapter, one place, both legs.

---

## R2. The banned-operations table

The centerpiece. Rows are operation families banned on the RT plane between go-live and teardown; init/teardown code runs on the control plane and uses them freely. Poison = config/rt_prelude_poison.h (compile error in RT-core TUs); wrap = the dev-build interposition net (R4); the two overlap by design — poison catches direct spelling at compile time, wrap catches what arrives through function pointers and third-party objects at run time [ESTABLISHED: booklet section 15.2].

| operation family | why banned (one line) | enforcement | route | use instead |
|---|---|---|---|---|
| **allocation** (malloc family, aligned_alloc, strdup, mmap/VirtualAlloc) | allocator takes locks and syscalls, worst case unbounded; all RT memory is pre-claimed and resident (invariant 3) | poison + wrap | compiler-catchable + runtime-catchable | immortal arena, pools, frame scratch — reference/memory_residency_manifest.md sections M2, M3, M4 |
| **locks / waits** (mutex, condvar, rwlock, CRITICAL_SECTION, futex/WaitOnAddress wait (sole exception: the thread-port eventcount park, C7 — classification R7), ambient try-lock-fallback) | a lock is a bet on the holder's promptness; the holder can be preempted, paged, throttled — wait unbounded in your terms [ESTABLISHED: booklet section 6.2] | poison (C11 + POSIX/NT spellings) + wrap + port choke points (R4) | compiler-catchable + runtime-catchable | wait-free channels — reference/concurrency_channels_manifest.md sections C1–C6 |
| **blocking syscalls** (read/write/poll/select, sockets, DeviceIoControl, WaitFor\*) | the kernel gives no latency contract; one deschedule = one missed deadline [ESTABLISHED: booklet ch. 2] | wrap (per-leg list, R4) + OS-free core (include + symbol audits — reference/quality_gates_ci_manifest.md section G3) | runtime-catchable + build-catchable | the single designed device wait (D3/D7); everything else crosses to the control plane via channels |
| **file / console I/O** (fopen/fread/fwrite, WriteFile, console writes) | syscall-backed, buffer locks, a wedged console blocks the writer; invariant 13 | poison + OS-free core | compiler-catchable + build-catchable | structured events into the flight ring — reference/observability_flightring_manifest.md section O3; drained and rendered off-plane |
| **formatting** (printf family, v\*printf, \*scanf, locale) | unbounded cost per conversion, locale locks and lazy init, hidden allocation; invariant 13 | poison | compiler-catchable | event id + raw operands into the ring (O2); render in the drain; message contract reference/error_tracing_contract_manifest.md section E6 |
| **string/stdio lazy init + hidden static state** (strtok, strerror, rand/srand, getenv, first-use stdio buffers) | first call allocates or races shared state; a cost cliff on the first block that touches it [CC-FACT] | poison | compiler-catchable | caller-owned state; explicit PRNG state passed to kernels — reference/dsp_kernel_patterns_manifest.md sections K3, K7 |
| **dlopen / LoadLibrary** | loader lock + file I/O + relocation, mid-stream [CC-FACT] | poison + symbol audit (G3) | compiler-catchable + build-catchable | bind everything at the composition root; kernel dispatch binds once at init (invariant 12; reference/dsp_kernel_patterns_manifest.md section K5) |
| **C++ exceptions / unwind** (and setjmp/longjmp) | unwinders allocate and take locks [CC-FACT]; non-local exit voids every boundedness argument (R3) | `#error` on C++ in the poison prelude + poison setjmp/longjmp + symbol audit rejecting `__cxa_*`/`_Unwind_*` imports [CC-FACT: symbol names — verify with llvm-nm on the linked core] | build-catchable + compiler-catchable | result codes — reference/error_tracing_contract_manifest.md section E4; dispositions E2 |
| **VLA / alloca** | stack growth unbounded at compile time; busts the fixed RT stack budget (reference/memory_residency_manifest.md section M7) | `-Werror=vla -Werror=alloca` in the RT-core flag row (reference/toolchain_build_manifest.md sections B2–B3) [MEASURED 2026-08-12: both fire on clang 22.1.8; alloca is a macro over `__builtin_alloca` (clang64 malloc.h:238), so poison cannot see it] | compiler-catchable | fixed worst-case buffers from the frame scratch arena (M4) |
| **recursion** | data-dependent stack depth; same budget bust | clang-tidy `misc-no-recursion` on RT TUs [MEASURED 2026-08-12: check present in clang-tidy 22.1.8; command `clang-tidy --checks='misc-no-recursion' --list-checks`]; wire in config/.clang-tidy | analysis-catchable | iteration over an explicit fixed-capacity work array |
| **unbounded loops / retries** | wait-freedom is bounded steps per operation; a retry-until-success loop can be starved forever by a peer [ESTABLISHED: booklet section 6.2] | nothing mechanical — R3 discipline, reviewed by name | contract-only (register R8) | counted loops with named bounds; bounded retry with declared, counted fallback (R3) |
| **sleep / yield** (Sleep, nanosleep, usleep, sched_yield, SwitchToThread, thrd_yield) | a yield is a scheduler donation with no contract on either kernel; sleep-to-poll adds at least timer-granularity latency [ESTABLISHED: booklet section 6.7] | poison + wrap | compiler-catchable + runtime-catchable | block in the one designed wait; eventcount park/wake (C7); never poll what a peer could signal |
| **process exit** (exit, abort, quick_exit, atexit, raise) *(extension row)* | rips the process out from under the device; the safe state is fade-to-silence, device kept healthy (invariant 7) | poison | compiler-catchable | degrade ladder + shutdown protocol (C9); in dev builds the guard's test-fail hook (R4) |

Allowlist notes (also documented in config/rt_prelude_poison.h): `memcpy/memmove/memset/memcmp` are the blessed bulk-move primitives — bounded, stateless, lock-free [CC-FACT]. `math.h` is allowed on the RT plane, but determinism-relevant (golden-mastered) paths call the vendored kernels instead (reference/dsp_kernel_patterns_manifest.md section K6) [ESTABLISHED: booklet section 9.6].

### Reading the enforcement failures (they are self-locating)

- Poison, at compile time: `error: attempt to use a poisoned identifier` at the exact use site (file:line:col) [MEASURED 2026-08-12, clang 22.1.8]. If it points inside a system header, an RT-core TU included a non-blessed header — remove the include; do not bless the header to make the error go away.
- Poison rejects `#undef` and re-`#define` of the identifier too — you cannot suppress it from source [MEASURED 2026-08-12: `#include <stdio.h>` after the prelude fails at stdio.h:14 `#undef snprintf`].
- Wrap net, at run time: one `EV_GUARD_*` flight-ring event carrying symbol id + return address (R4); symbolize offline, patch at the named line. The compile error and the runtime event name the same defect at different rungs.

### Never

- **Never** call a banned family "just once at stream start" from an RT thread — init happens on the control plane *before arming*; after go-live there is no such thing as once (invariant 1). Route: runtime-catchable (the guard arms at go-live, R4).
- **Never** adopt try-lock-with-fallback as ambient policy — admissible in principle, refused here: it turns every access into a branch between two behaviors, and the channels cover every legitimate need [ESTABLISHED: booklet section 6.2]. Route: contract-only (R8).
- **Never** "pre-warm" a banned facility to make it RT-safe — moving the first-call cost does not remove the lock it takes on call N. Route: compiler-catchable (it is still poisoned).
- **Never** move core logic into an RT-adapter TU to escape the poison prelude — the include audit walks the boundary (reference/quality_gates_ci_manifest.md section G3). Route: build-catchable.
- **Never** accept "it didn't glitch" as evidence of compliance — the guard, the deadline histograms, and the counters are the evidence (invariants 5–6; reference/observability_flightring_manifest.md sections O4–O5). Route: runtime-catchable.
- **Never** log, format, or print on the RT plane, including "temporarily for debugging" — that is invariant 13 verbatim; diagnosis mode exists for exactly this (reference/observability_flightring_manifest.md section O9). Route: compiler-catchable + runtime-catchable.

---

## R3. Bounded-work rules

Invariant 1's positive half: from the device wakeup to the submission, every operation completes in bounded time **by construction** [ESTABLISHED: booklet ch. 3, invariant 1]. Boundedness is argued, not measured: the argument is the artifact.

| # | rule | route |
|---|---|---|
| R3.1 | Every loop on the RT path is **counted**, with a bound provable from constants fixed at go-live: block quantum, channel count, ring capacity, pool size, voice cap. The bound is named at the loop in a comment (`/* bound: MAX_BLOCK */`). | contract-only — reviewed by name (R8) |
| R3.2 | **No data-dependent unbounded retries.** CAS-retry against a contended word belongs to the control plane's side of the boundary, if anywhere [ESTABLISHED: booklet section 6.2]. RT-side retry loops carry a compile-time cap and a declared fallback, and the exhaustion is counted (never silent — invariant 2). | contract-only + host-test-catchable (torture suites C8 assert progress under a stalled peer) |
| R3.3 | **Wait-free means**: *this* thread completes *this* operation in a bounded number of its own steps, regardless of every other thread — including a dead one. A push onto a full ring **completes** by returning "full", counted — that is the overflow policy, not a failure of it [ESTABLISHED: booklet section 6.2, citing Herlihy]. | host-test-catchable (per-channel contract suites, T6/T7) |
| R3.4 | Work per callback is proportional to the block size and nothing else: no hidden per-session scans, no cost that grows with uptime. The partition-invariance property (invariant 20) is the regression net. | host-test-catchable (reference/testing_verification_manifest.md section T5) |
| R3.5 | A third-party call on the RT path needs a named-implementation boundedness argument before it exists (R7's rule; register R8). Default answer: no. | contract-only |

Bounded-retry idiom (R3.2's cap+counted-fallback shape — the control plane's capped seqlock read of a C5 gauge cluster, R6 idiom (d) after its C5-direction fix; an RT-side retry loop, where one is genuinely needed, carries the identical cap+counted-fallback shape):

```c
/* bound: SEQ_RETRY_MAX = 4. fallback: keep last-good copy; miss is counted. */
for (unsigned k = 0; k < SEQ_RETRY_MAX; k++) {
    if (seq_try_read(&q->params, &p)) { st->last_good = p; return &st->last_good; }
}
atomic_fetch_add_explicit(&st->seq_miss, 1, memory_order_relaxed);
return &st->last_good;   /* stale by at most one control-plane write burst */
```

The boundedness **argument** for each RT TU (which loops, which bounds, why the bounds hold) is reviewed by name — route contract-only, register R8; there is no static tool that proves it here [ESTABLISHED: booklet ch. 3, invariant 1 route note].

### Legal bound sources (what a loop may bind to)

| constant | fixed at | anchor |
|---|---|---|
| block quantum / max block size | stream negotiation, before go-live | reference/dsp_kernel_patterns_manifest.md section K2 |
| channel count / format width | stream negotiation | reference/device_adapter_manifest.md section D9 |
| ring / mailbox capacity | composition root | reference/concurrency_channels_manifest.md sections C2, C4 |
| pool capacity, voice cap | composition root | reference/memory_residency_manifest.md section M3 |
| worker count (fixed pool) | composition root | R1 inventory; C7 |
| retry caps (`SEQ_RETRY_MAX` etc.) | compile-time constants | R3.2 |

A "bound" that is none of these — derived from input data, from a queue depth observed at run time, or from wall-clock — is not a bound; it is a hazard the review must argue down (R8).

---

## R4. The guard machinery

Three cooperating mechanisms make invariant 1 mechanical in development and test builds [ESTABLISHED: booklet section 15.2]. Ship builds compile the net out; the poison prelude stays — it costs nothing.

| mechanism | catches | when | build |
|---|---|---|---|
| plane tag (thread-local) | classifies the caller | always | all builds (cheap) |
| poison prelude (config/rt_prelude_poison.h) | direct spelling of banned identifiers | compile time | all builds |
| `--wrap` interposition net | calls via function pointers, CRT internals, third-party objects | run time | dev/test builds only |
| port choke points | OS waits/locks routed through our own thread port | run time | dev/test asserts in port code |

### The plane tag and arming

```c
typedef enum { PLANE_CONTROL = 0, PLANE_RT = 1 } rt_plane_t;
static _Thread_local rt_plane_t g_plane;    /* set once by the thread adapter at creation (R1.1) */
static atomic_bool g_guard_armed;           /* set at go-live (R1.5), cleared at teardown entry */
```

The guard **arms at go-live, not at process start**. Consequence of the measured wrap behavior: `__wrap_malloc` intercepts CRT-internal startup allocations too — 3 hits observed before `main` in a trivial exe [MEASURED 2026-08-12: `-Wl,--wrap=malloc` on the lld MinGW driver]. Init-time hits are expected and legal; only post-arming, RT-plane hits trap. Teardown disarms first (C9), so join/free paths are legal again.

### The interposition net (dev builds)

Link the dev leg with `-Wl,--wrap=<sym>` per list; works on lld's MinGW driver [MEASURED 2026-08-12] and on the Linux leg's lld — same mechanism, one list [ESTABLISHED: booklet section 15.2]. Canonical shim:

```c
void *__real_malloc(size_t);
void *__wrap_malloc(size_t n) {
    rt_guard_trap_if_armed(EV_GUARD_ALLOC, __builtin_return_address(0));
    return __real_malloc(n);
}
```

Wrap list (starter; the project pins the full list in the build preset — config/CMakePresets.json): both legs: `malloc calloc realloc free aligned_alloc`. Linux adds: `pthread_mutex_lock pthread_cond_wait pthread_cond_timedwait nanosleep poll read write sem_wait`. Windows adds: the malloc family only [OPEN — NEEDS-INPUT: whether `--wrap` intercepts dllimport-ed Win32 calls (`Sleep`, `WaitForSingleObject`) is unverified — call sites may go through `__imp_` thunks that bypass symbol wrapping [CC-FACT — verify per symbol with a link test before relying on it]. Mitigation that works regardless: all waits/locks on Windows route through the thread port, and the port implementation carries the guard check — the choke-point row above].

`--wrap` intercepts references resolved in **this link**; calls internal to already-linked DLLs (ucrtbase to itself, audio engine DLLs) are invisible to it [CC-FACT]. That residue is why the RT plane's third-party surface is kept near-nil (R8) and why R7's naming rule exists.

### The poison prelude

The build system forces it — not politeness — into the RT-core TU class only: `clang -std=c17 ... -include config/rt_prelude_poison.h` [MEASURED 2026-08-12: `-include` prepends the file and poison fires as documented in the header]. RT-adapter TUs (must see OS/ALSA/WASAPI headers) do **not** get the prelude; they are covered by the net, the choke points, and review. TU classes: reference/toolchain_build_manifest.md section B1. The header's blessed-block ordering rule and its measured firewall behavior are documented in the file itself — read it before editing it.

### Trap behavior (the failure artifact is self-locating)

On a post-arming banned call from a tagged RT thread, `rt_guard_trap_if_armed`:

1. writes one event to the flight ring: `{EV_GUARD_<family>, tid, wrapped-symbol id, return address, block index}` — ids from the registry, reference/observability_flightring_manifest.md section O2; return address symbolizes offline to file:line (evidence chain, reference/error_tracing_contract_manifest.md section E7);
2. breaks if a debugger is attached (`IsDebuggerPresent` / Linux `TracerPid` scan, then `__builtin_debugtrap()`) [CC-FACT];
3. under the test harness: fails the test through the harness hook with the E6-format message (WHAT symbol, WHERE retaddr, WHY plane+armed) — reference/testing_verification_manifest.md section T2;
4. in a standalone dev run: counts it, flags the heartbeat (O6), and the session report (E8) carries the event — the run is red, not aborted; overload can never fire the guard, only a rule violation can [ESTABLISHED: booklet section 15.2].

### Worked failure, end to end (the E1 loop in miniature)

What the agent sees when the guard fires, and what it does — full walkthroughs: reference/error_tracing_contract_manifest.md section E10; artifact reading: reference/testing_verification_manifest.md section T13.

```
event    : {id: EV_GUARD_ALLOC, tid: "rt_wrk2", sym: malloc, ret: 0x7ff6a2c31141, block: 48211}
symbolize: llvm-symbolizer --obj=build/dev/app.exe 0x7ff6a2c31141
           -> resize_scratch  core/kernels/conv_fir.c:141
diagnose : conv_fir grows a temp when the impulse-response length parameter changes
patch    : pre-size at prepare() on the control plane (K3 parameter protocol), or take the
           worst-case block from the frame scratch arena (M4); re-run the T6 fault suite
```

WHAT (symbol) + WHERE (file:line via return address) + WHY (plane, armed, block index) arrive in one event — the failure artifact locates the patch site without a rerun. That is the doctrine this package exists for; the guard is its RT-plane instance.

### Guard rules

| # | rule | route |
|---|---|---|
| R4.1 | The tag + arming flag are the guard's only state; checking them is branch-and-load, cheap enough for dev-build port choke points. | runtime-catchable |
| R4.2 | The wrap list is part of the build identity (reference/toolchain_build_manifest.md section B10): a dev binary states which symbols were netted, so a green run's coverage is auditable. | build-catchable |
| R4.3 | A guard trap in CI fails the job; there is no allowlist mechanism. If the call is legitimate, the code is wrong about *when* it runs (before arming vs after) — fix the phase, not the guard. | host-test-catchable |
| R4.4 | New third-party code on the RT plane adds its blocking symbols to the wrap list **or** a named-implementation argument to the register (R8) — one of the two, before merge. | contract-only |

---

## R5. FTZ/DAZ per thread

Why: denormal operands/results take a microcode assist costing tens-to-hundreds of cycles, and audio's decaying tails glide asymptotically *into* the denormal range and sit there — the classic reverb that idles at 2% CPU and costs 40% on silence [ESTABLISHED: booklet section 9.6]. Stall taxonomy: reference/optimization_microarch_manifest.md section P7. Invariant 4 makes the mode per-RT-thread law.

### The recipe (thread adapter, thread-start hook, every RT thread)

```c
#include <immintrin.h>
void rt_thread_fp_init(void) {
    _MM_SET_FLUSH_ZERO_MODE(_MM_FLUSH_ZERO_ON);
    _MM_SET_DENORMALS_ZERO_MODE(_MM_DENORMALS_ZERO_ON);
}
```

[MEASURED 2026-08-12: after this pair, MXCSR = 0x9fc0 (FTZ|DAZ set, all exception masks default) on clang 22.1.8/CLANG64.] MXCSR is per-thread register state, saved and restored across context switches, so the hook runs in **every** RT thread, not once per process [CC-FACT — Intel SDM is the primary source for MXCSR semantics]. x87 is not in play in the x86-64 SSE ABI; MXCSR governs SSE/AVX arithmetic [CC-FACT]. The same hook is where the plane tag (R4) is set — one adapter, one place. ISA-floor and flag anchors: hub H8 [VERSION-DEPENDENT - hub H8].

MXCSR anchors [ESTABLISHED: Intel SDM vol. 1, MXCSR register]:

| field | bit(s) | mask | in the measured 0x9fc0? |
|---|---|---|---|
| FTZ (flush results to zero) | 15 | `0x8000` | yes |
| exception masks (all set = default) | 7–12 | `0x1f80` | yes |
| DAZ (treat denormal inputs as zero) | 6 | `0x0040` | yes |

`0x8000 | 0x1f80 | 0x0040 = 0x9fc0` — the measured value decomposes exactly; the patrol below checks only the FTZ|DAZ bits and leaves mask policy alone.

### The dev-build patrol

A library call on the wrong plane can silently restore precise mode, and the failure is a *performance* cliff no correctness test sees [ESTABLISHED: booklet section 9.6]. So dev builds re-verify at block edges:

```c
#define RT_FTZ_DAZ_BITS 0x8040u   /* FTZ | DAZ */
static inline void rt_fp_patrol(uint32_t block_idx) {
    uint32_t csr = _mm_getcsr();
    if ((csr & RT_FTZ_DAZ_BITS) != RT_FTZ_DAZ_BITS)
        rt_event2(EV_FP_MODE_LOST, block_idx, csr);   /* self-locating: which block, what mode */
}
```

Route: runtime-catchable (patrol event + red session report), backed by host-test-catchable properties proving kernels emit no denormal/NaN from legal input (reference/testing_verification_manifest.md section T5; invariant 4). The mode is defense in depth, not a correctness input: feedback kernels also carry algorithmic hygiene so their cost does not depend on the FP mode — reference/dsp_kernel_patterns_manifest.md section K7 [ESTABLISHED: booklet section 9.6]. A NaN in nominal operation is a defect, not a curiosity; the patrol scans block edges and state snapshots, never per sample.

ARM64 port note: the equivalent is FPCR flush-to-zero control; out of scope until a port exists [OPEN — NEEDS-INPUT; hub H8 owns ISA anchors].

---

## R6. Memory-ordering blessed idioms

One language for concurrent correctness: the C11/C17 memory model, `stdatomic.h`, **explicit** orderings — regardless of x86-TSO. The hardware is the wrong adversary: the *compiler* reorders what the hardware would not, and the model is the only statement of intent an ARM64 port or a race detector can audit [ESTABLISHED: booklet section 6.6]. `stdatomic.h` acquire/release and `_Alignas(64)` compile clean on the pinned toolchain [MEASURED 2026-08-12].

Exactly four idioms cover this codebase; each use cites its idiom letter in a comment [ESTABLISHED: booklet section 6.6]. Choosing one:

| you need | idiom | channel home |
|---|---|---|
| hand filled slots/indices to one consumer, in order | (a) release-publish / acquire-consume | SPSC ring — C2; snapshot swap — C3 |
| count events; stamp generations read for trend; single independent param targets | (b) relaxed counters / independent values | counters canon — reference/observability_flightring_manifest.md section O5; params — concurrency C6 |
| latest-value-wins slot, one writer one reader | (c) acq_rel exchange | triple-slot mailbox — C4 |
| multi-word value read coherently, written rarely | (d) seqlock pair | seqlock — C5 |
| anything else | none — it is a new channel shape | R6.5: written happens-before argument first |

### (a) Release-publish / acquire-consume — SPSC ring (C2), snapshot swap (C3)

```c
/* producer: payload first, then publish the index — idiom (a) */
ring->slot[w & RING_MASK] = v;                              /* plain stores */
atomic_store_explicit(&ring->w, w + 1, memory_order_release);

/* consumer: acquire the index, then read only below it — idiom (a) */
size_t wi = atomic_load_explicit(&ring->w, memory_order_acquire);
/* every payload store sequenced before that release is visible here */
```

Rule: payload is plain memory owned by the publish protocol; the atomic is the only gate. Never read payload beyond an acquired index.

### (b) Relaxed counters — statistics, drop counts, generation stamps read for trend

```c
atomic_fetch_add_explicit(&st->drops, 1, memory_order_relaxed);   /* idiom (b) */
```

Rule: a relaxed value orders nothing — it must never gate access to non-atomic data.

### (c) Acquire-release exchange — the triple-slot mailbox (C4)

```c
/* writer hands over a filled slot and takes back the previous one — idiom (c) */
unsigned prev = atomic_exchange_explicit(&mb->latest, filled, memory_order_acq_rel);
```

`acq_rel` because both sides pass payload through the same word: release your writes, acquire the peer's.

### (d) The seqlock pair (C5)

```c
typedef struct { _Atomic unsigned seq; _Atomic uint64_t d0, d1; } seqlock_t;

void seq_write(seqlock_t *q, uint64_t a, uint64_t b) {        /* RT side, one writer — C5 direction: RT publishes, control reads */
    unsigned s = atomic_load_explicit(&q->seq, memory_order_relaxed);
    atomic_store_explicit(&q->seq, s + 1, memory_order_relaxed);  /* odd: writing */
    atomic_thread_fence(memory_order_release);                    /* odd visible before data */
    atomic_store_explicit(&q->d0, a, memory_order_relaxed);
    atomic_store_explicit(&q->d1, b, memory_order_relaxed);
    atomic_store_explicit(&q->seq, s + 2, memory_order_release);  /* even: stable */
}
bool seq_try_read(const seqlock_t *q, uint64_t *a, uint64_t *b) { /* control side; cap retries (C5 row: cap ~1000, threshold reported) */
    unsigned s0 = atomic_load_explicit(&q->seq, memory_order_acquire);
    if (s0 & 1u) return false;
    *a = atomic_load_explicit(&q->d0, memory_order_relaxed);
    *b = atomic_load_explicit(&q->d1, memory_order_relaxed);
    atomic_thread_fence(memory_order_acquire);                    /* data loads before recheck */
    return atomic_load_explicit(&q->seq, memory_order_relaxed) == s0;
}
```

Data words are relaxed atomics so the recipe is race-free under the C model; the fence pairing is the published one [ESTABLISHED: Boehm, "Can Seqlocks Get Along with Programming Language Memory Models?", MSPC 2012]. Full channel contract, sizing, and torn-read tests: reference/concurrency_channels_manifest.md section C5.

### Rules

| # | rule | route |
|---|---|---|
| R6.1 | **Bare `seq_cst` is unreviewed code**: a non-`_explicit` atomic op or an explicit `memory_order_seq_cst` outside channel implementations is rejected — unstated intent that also buys a full-fence store on x86 [ESTABLISHED: booklet section 6.6]. | analysis-catchable — structural audit greps for atomic ops without `_explicit` and for `seq_cst` outside the concurrency dir (reference/quality_gates_ci_manifest.md sections G3, G9) |
| R6.2 | **Fences are exceptional**: `atomic_thread_fence` appears only inside channel implementations; the channels are the concurrency API [ESTABLISHED: booklet section 6.6]. | analysis-catchable (same audit) |
| R6.3 | **`volatile` is not a concurrency tool.** Sole quarantined exception: signal/exception-context flags in adapters [ESTABLISHED: booklet section 6.6]. | analysis-catchable (audit) + contract-only for the exception's justification |
| R6.4 | Every atomic use cites its idiom letter (a–d) in a comment. | contract-only (reviewed by name, R8) |
| R6.5 | A **new channel shape** requires a written happens-before argument in the canon's terms before merge; the stress suites (C8) and the Linux TSan leg are the mechanical net under it, not the proof. TSan runtime is ABSENT on CLANG64 — Linux leg only [MEASURED 2026-08-12; availability matrix: hub H5]. | contract-only (R8) + host-test-catchable (T7, T8) |
| R6.6 | RT-plane atomics must be lock-free at their width — a libatomic lock is a lock (R2). Pin it: `_Static_assert(ATOMIC_LLONG_LOCK_FREE == 2, "RT plane needs lock-free 64-bit atomics");` and per-channel asserts on wider types [ESTABLISHED: C17 7.17.1 lock-free macros]. | compiler-catchable |

---

## R7. Syscall classification

The RT plane is syscall-free except at designed edges. **The rule: a call whose implementation you cannot name is blocking until proven otherwise** [ESTABLISHED: booklet section 15.2, quoting section 11.4]. "Usually" and "typically" below are load-bearing — name the mechanism, then let the bench lane price it on the reference machine (reference/optimization_microarch_manifest.md sections P2–P3).

| call | leg | class | named mechanism / basis |
|---|---|---|---|
| `clock_gettime(CLOCK_MONOTONIC)` | Linux | safe-fast | vDSO user-mode fast path, usually no kernel entry; falls back to a real syscall on unusual clocksources [CC-FACT — verify: `strace` a tight loop, expect no per-call syscall] |
| `QueryPerformanceCounter` | Windows | safe-fast | user-mode read (invariant TSC + shared-page scaling), no kernel transition on modern NT [CC-FACT — MS "Acquiring high-resolution time stamps" is the doc to verify against] |
| `__rdtsc()` | both | safe-fast | one instruction; needs invariant-TSC assumption + calibration (P3) [CC-FACT] |
| `GetTickCount64` | Windows | safe, coarse | shared-page read; millisecond-class resolution [CC-FACT] |
| futex `FUTEX_WAKE` / `WakeByAddressSingle`/`WakeByAddressAll` (incl. INT_MAX) / `SetEvent` (wake side only) | both | conditionally safe | kernel entry that returns without waiting; bounded work, tail not contractual — admitted **only** at named channel edges: the eventcount wake (C7), the loop hand-offs (D3/D7) [CC-FACT] |
| the device wait (`poll` on ALSA descriptors / wait on the WASAPI event) | both | THE one designed block | one per device-loop thread (R1); owned by reference/device_adapter_manifest.md sections D3, D7 |
| futex `FUTEX_WAIT_PRIVATE` / `WaitOnAddress` (eventcount park) | both | second designed block — RT workers only, at the C7 gate, via the thread port | kernel re-checks `*addr` against the undesired value atomically vs wakes, so the park cannot lose a wake [ESTABLISHED: futex(2); WaitOnAddress MEASURED probe, C7] |
| device submission (`snd_pcm_*` commit/write; `GetBuffer/ReleaseBuffer`) | both | port-owned | classification and fault conversion owned by D1, D3–D8; not general-purpose calls |
| `mmap/munmap/mprotect`, `VirtualAlloc/VirtualFree/VirtualProtect` | both | banned | allocation class (R2, M1); `mprotect`-class calls also trigger cross-core TLB shootdown IPIs that stall sibling threads [CC-FACT] |
| file/socket/pipe/console I/O (`read/write/send/recv`, `ReadFile/WriteFile`, console) | both | banned | R2 rows 3–4 |
| any lock/wait (`futex` wait, `WaitOnAddress`, `WaitForSingleObject`, mutex/condvar) — banned everywhere EXCEPT the two designed blocks above (device wait; C7 eventcount park) | both | banned | R2 row 2; R2 row 12 for sleep/yield |
| `fork/exec/CreateProcess/system` | both | banned | R2 row 3 |
| `ioctl/DeviceIoControl` (generic) | both | banned unless port-owned | only the device port's own designed requests pass, inside the adapter (D-sections) |
| CRT calls with lazy state (`strerror`, `getenv`, first-use stdio) | both | banned | R2 row 6 |
| `AvSetMmThreadCharacteristicsW` (MMCSS) | Windows | thread-setup only | called once at RT thread start by the adapter, never per block [MEASURED 2026-08-12: returns non-null handle with `-lavrt`, task index 418 observed]; policy: hub H7, loop: D7 |

Budget discipline: even safe-fast entries are counted — timestamps per block ≤ 2 (block edges) plus the histogram write; anything more is a review item [OPEN — ASSUMED budget; adjust in the project spec]. Per-leg specifics and re-check triggers on kernel/OS updates: hub H4, H6, H9 [VERSION-DEPENDENT - hub H9].

### Classifying a new call — the procedure

1. Name the implementation: vDSO/shared-page/instruction (safe-fast), kernel-entry-no-wait (conditionally safe), or anything that can wait/fault/allocate (banned). Cannot name it → **blocking until proven otherwise** [ESTABLISHED: booklet section 15.2].
2. Record the evidence: source read, `strace`/ETW observation, or vendor doc — with a re-check trigger at hub H9.
3. If conditionally safe: name the single channel edge that may issue it; add it to the wrap list anyway (R4) so a stray use still traps.
4. Price it on the reference machine via the bench lane before it enters a per-block path (P2–P3; T10 owns the gate).

### Decisions you must not invent

Per-block syscall/timestamp budget (OPEN above) · the Windows wrap list and the dllimport-interception answer (R4 OPEN) · the thread-name scheme (R1 OPEN) · MMCSS task-name and priority policy (hub H7; device loop D7) · which ALSA wait/submission variant the device port uses (D2–D3) · spin budget of the eventcount hybrid (product-tuned — C7; booklet section 6.7).

---

## R8. Contract-only register

The meta-invariant: **a rule with no enforcer is a preference** — route it, or register it here and review for it by name [ESTABLISHED: booklet ch. 3; register discipline: booklet section 15.5]. This file's register — the checklist lives in cards/review-code.md; the write-side card is cards/write-rt-code.md:

| # | item | what review checks | when |
|---|---|---|---|
| 1 | loop boundedness (R3.1–R3.2) | every RT-path loop names its bound; the bound derives from go-live constants; retries carry cap + counted fallback | every PR touching RT TUs |
| 2 | happens-before arguments (R6.5) | written argument in the canon's terms (pairing, fence synchronization) attached to the PR for any new/changed channel | on channel change |
| 3 | third-party surface ≈ nil (R4 residue) | any third-party call on the RT path has a named-implementation boundedness case in the register; default is no | on dependency or adapter change |
| 4 | syscall naming (R7) | every "safe-fast" claim names its mechanism and its re-check trigger (hub H9) | on adapter change + release rung |
| 5 | plane inventory completeness (R1.1, R1.4) | the composition root's thread list matches the documented R1 table shape: plane, waits-on, may-block, wait policy | on any thread-creation change |
| 6 | idiom citations (R6.4) | each atomic op cites idiom a–d | every PR touching atomics |

Register cadence: items are reviewed by name per the triggers above; the register itself is re-audited at each release rung (reference/quality_gates_ci_manifest.md section G7). What this file does **not** own: channel internals (C2–C7), residency mechanics (M5–M6), device-loop specifics (D3, D7), kernel FP hygiene (K7), gate wiring (G1–G5).

### Go deeper

| question | where |
|---|---|
| which channel to use, and its full contract | reference/concurrency_channels_manifest.md sections C1–C7 |
| what memory the plane may touch, and how it became resident | reference/memory_residency_manifest.md sections M1–M8 |
| the one blocking wait per device loop, per leg | reference/device_adapter_manifest.md sections D3, D7 |
| how a guard trap becomes a patch | reference/error_tracing_contract_manifest.md section E10; reference/testing_verification_manifest.md section T13 |
| the CI legs that run the guard, sanitizers, and torture suites | reference/quality_gates_ci_manifest.md section G5; reference/testing_verification_manifest.md sections T7, T8, T12 |
| the flag rows carrying `-Werror=vla -Werror=alloca` and the forced `-include` | reference/toolchain_build_manifest.md sections B2–B4 |
| writing new RT code against these rules | cards/write-rt-code.md; reviewing it: cards/review-code.md |
