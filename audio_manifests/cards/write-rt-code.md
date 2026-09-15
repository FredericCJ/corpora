# Card: write real-time-plane code

**On the RT plane you do bounded work and nothing else — and the dev build traps every violation, which is the feedback loop working, not an obstacle.**

Facts verified 2026-08-12. Version-dependent claims route to reference/audio_platform_baseline_manifest.md (the hub); if any file disagrees with the hub, the hub wins.
Reasoning root: the child booklet `realtime-audio-pc-architecture-and-design-r1.md` (repo root). This card operationalizes it; it never re-argues it.

**Load when:** writing or touching anything a device-loop or RT-worker thread executes — kernels, the schedule executor, channel RT sides, adapter paced loops.
**Depth:** reference/rt_plane_rules_manifest.md. Channels: cards/concurrency-channels.md. Kernels: cards/write-dsp-kernel.md. What the plane does with faults: cards/handle-errors.md.

## The standard this card serves

**From device wakeup to submission, every operation completes in bounded time by construction: no lock, no allocation, no blocking syscall, no I/O, no unbounded loop** [ESTABLISHED: booklet ch. 3 invariant 1]. The no-locks rule is settled by argument in booklet section 6.2 — do not relitigate it; a lock's worst case on a desktop kernel cannot fit a millisecond budget.

## Plane declaration

Every thread belongs to exactly one plane, declared at creation through the thread port — plane, stack size (pre-sized, guard-paged, prefaulted for RT), priority class request, placement hint; the grant is **reported, not assumed** [ESTABLISHED: booklet sections 5.3, 6.1; ch. 3 invariant 14]. The plane tag is what the guard machinery keys on [ESTABLISHED: booklet section 15.2]. The RT thread population is fixed between go-live and teardown; creating a thread after go-live is a control-plane-only act [ESTABLISHED: booklet section 5.3]. The plane assignment of every new thread is a named review question (route: contract-only, reference/rt_plane_rules_manifest.md section R8).

## The banned table (R2 condensed)

| banned on the RT plane | why | route |
|---|---|---|
| allocation family (`malloc`/`calloc`/`realloc`/`free`, `strdup`, anything that might allocate) | unbounded; lock-taking; page-faulting | compiler-catchable (poison) + runtime-catchable (wrap net) |
| locks and waits (mutexes, condvars, semaphores, try-lock fallbacks) | wait bounded by a preemptible, pageable peer — priority inversion without rescue | analysis-catchable + runtime-catchable (guard) |
| blocking syscalls; file/socket I/O | a scheduler visit with no bound | runtime-catchable (wrap net) + contract-only residue |
| stdio, formatting, locale (`printf` family, `fopen`, `setlocale`) | all of the above, plus allocation | compiler-catchable (poison) [ESTABLISHED: booklet ch. 3 invariant 13] |
| `sleep`/`yield` in any spelling | a scheduler donation with no contract on either kernel | analysis-catchable (poison list) [ESTABLISHED: booklet section 6.7] |
| recursion, VLA, `alloca` | unbounded stack against a pre-sized budget | analysis-catchable (RT-TU rule pack) [ESTABLISHED: booklet section 15.1] |
| unbounded loops; loop bounds mutated in-body | invariant 1's residue | contract-only — written boundedness argument, reviewed by name (R8) |
| CAS retry loops on the RT side | starvable by a peer = not wait-free | host-test-catchable (channel contract suites) + review [ESTABLISHED: booklet section 6.2] |
| third-party/opaque calls | any call whose implementation you cannot name is blocking until proven otherwise | contract-only [ESTABLISHED: booklet sections 11.4, 15.2] |

The one sanctioned block: the device loop waiting on the device's own pacing signal, inside the adapter [ESTABLISHED: booklet section 5.1].

## Crossing the boundary: five channels only

Anything entering or leaving the plane travels one of the five channel shapes — atomic parameter, SPSC ring, snapshot swap, latest-value mailbox, seqlock — selected by the decision tree in cards/concurrency-channels.md. Parameters are consumed as *targets* and interpolated; they never carry pointers [ESTABLISHED: booklet section 4.3]. A sixth shape requires a written happens-before argument and review (route: contract-only) [ESTABLISHED: booklet section 6.6].

## FTZ/DAZ — per RT thread, at thread start

The thread adapter sets it; dev builds re-verify at block edges, because a wrong-plane library call can silently restore precise mode and the failure is a performance cliff no correctness test sees [ESTABLISHED: booklet section 9.6; ch. 3 invariant 4]. x86 leg mechanism:

```c
#include <immintrin.h>
_MM_SET_FLUSH_ZERO_MODE(_MM_FLUSH_ZERO_ON);
_MM_SET_DENORMALS_ZERO_MODE(_MM_DENORMALS_ZERO_ON);
/* MXCSR reads back 0x9fc0 with both set */
```

[MEASURED 2026-08-12: MXCSR=0x9fc0 after both calls, CLANG64 clang 22.1.8]. Per-ISA/per-OS spellings: [VERSION-DEPENDENT - hub H8].

## The guard machinery — what your dev build will do to you

Three cooperating mechanisms make invariant 1 mechanical in dev/test builds [ESTABLISHED: booklet section 15.2]:

1. **Poison headers** — RT-class TUs force-include config/rt_prelude_poison.h; a banned symbol fails to *compile*: `attempt to use a poisoned identifier` [MEASURED 2026-08-12: `#pragma GCC poison malloc` produces exactly that on CLANG64 clang 22.1.8].
2. **The interposition net** — dev builds wrap the allocator, lock/wait, and known-blocking families via the linker's wrap facility, both legs [MEASURED 2026-08-12: `-Wl,--wrap=malloc` works under lld's MinGW driver]. Reading wrap logs on the Windows leg: expect ~3 CRT-internal startup allocations before `main` — pre-main hits are the CRT, not your leak [MEASURED 2026-08-12].
3. **The trap** — every wrapped entry checks the plane tag; RT plane → log the callsite into the flight ring, break if a debugger is attached, fail the test otherwise. Overload cannot fire it; only a rule violation can.

When the guard fires: read the callsite it logged, then move the work to the control plane or restate it as channel traffic. Never widen the blessed list, never wrap the guard in a "just this once". Ship builds compile the net out; the poison stays (it costs nothing).

## Bounded work, bounded memory

- Every RT-plane loop names its bound, and the bound derives from block-constant quantities — frames, voices, ops in the schedule; the written boundedness argument is the review artifact (route: contract-only, reference/rt_plane_rules_manifest.md section R8) [ESTABLISHED: booklet ch. 3 invariant 1].
- Touch only memory allocated, locked, and prefaulted before go-live [ESTABLISHED: booklet ch. 3 invariant 3]. Per-block temporaries come from the frame scratch arena, reset each block — reference/memory_residency_manifest.md section M4.
- The stack is a pre-sized, guard-paged, prefaulted budget; no VLA/alloca (route: analysis-catchable), watermarks checked in soak — reference/memory_residency_manifest.md section M7 [ESTABLISHED: booklet section 8.2].
- Overload is **not** a rule violation: it enters the degrade ladder on measured headroom and cannot fire the guard — only a banned operation can [ESTABLISHED: booklet sections 12.2, 15.2]. Ladder behavior: cards/handle-errors.md.

## Waiting policy (DT-5 condensed)

| thread | waits on | and nothing else |
|---|---|---|
| device loop | the device's pacing signal | never sleeps, yields, or polls [ESTABLISHED: booklet section 6.7] |
| RT workers | the eventcount hybrid — bounded spin, then park | spin budget product-tuned; parked when the stream stops [ESTABLISHED: booklet section 6.5] |
| control plane | ordinary blocking waits with timeouts | its own card |

## Faults on the plane: absorb and mark

The RT plane cannot return errors mid-block, cannot block, cannot log, cannot stop. Every detected fault: substitute the safe value (silence for a starved voice, clamp for an over), **mark a structured event into the flight ring, count it**, keep rendering — the mark *is* the error handling; absorbing without a record is `try/continue` with extra steps [ESTABLISHED: booklet section 12.1]. Dispositions and event mechanics: reference/error_tracing_contract_manifest.md section E2; reference/observability_flightring_manifest.md section O3. This is the doctrine end-to-end: the mark carries what/where/why so the drained artifact patches the defect.

## Never

- Take any lock, even "briefly held" — settled, booklet section 6.2 (routes: analysis + runtime-catchable).
- Allocate, free, or call anything that might (route: compiler-catchable poison).
- Format, log, print, or touch stdio/locale on-plane [ESTABLISHED: booklet ch. 3 invariant 13].
- Use `volatile` as a concurrency tool — it is a review-flagged defect outside quarantined adapter signal contexts [ESTABLISHED: booklet section 6.6].
- Write a bare seq_cst atomic — unstated intent plus an x86 fence cost per store; cite one of the four blessed idioms in a comment [ESTABLISHED: booklet section 6.6].
- Create or destroy threads mid-stream [ESTABLISHED: booklet section 5.3].
- Call into third-party code whose blocking behavior you cannot name (route: contract-only).
- Suppress or bypass the guard instead of moving the work.

## Decisions you must not invent

- RT worker pool size — bounded above by physical P-cores available to the process [ESTABLISHED: booklet section 6.5]; the exact count is [OPEN NEEDS-INPUT].
- Eventcount spin budget — [OPEN NEEDS-INPUT; product-tuned ≈ the fork latency it must hide, booklet section 6.7].
- Degrade-ladder thresholds and hysteresis — [OPEN NEEDS-INPUT; booklet section 12.2 makes them recorded product policy].
- Elevation-denial policy at go-live (proceed degraded vs refuse) — [OPEN NEEDS-INPUT; booklet section 4.5 step 6].
- Which blocking-syscall wrappers the net covers per leg — [OPEN ASSUMED: the R4 list as shipped; extend it through review, reference/rt_plane_rules_manifest.md section R4].

## What you owe when done

Per reference/testing_verification_manifest.md section T11: a guard-clean run of the host suites in a dev build (the trap failing a test *is* the report — its artifact names the callsite); the written boundedness argument for any new RT-plane loop, filed in the contract-only register (reference/rt_plane_rules_manifest.md section R8); channel contract + stress suites if you touched a channel (cards/concurrency-channels.md); ASan+UBSan legs green on both legs, TSan lane green on Linux. The gate ledger reference/quality_gates_ci_manifest.md section G1 holds it all via config/check.sh. RT code with no failing-mode evidence is untested RT code.

## Go deeper

| question | where |
|---|---|
| the two planes + thread inventory | reference/rt_plane_rules_manifest.md section R1 |
| banned operations, the full table | reference/rt_plane_rules_manifest.md section R2 |
| bounded-work rules and loop arguments | reference/rt_plane_rules_manifest.md section R3 |
| guard machinery internals | reference/rt_plane_rules_manifest.md section R4 |
| FTZ/DAZ per thread, per leg | reference/rt_plane_rules_manifest.md section R5; hub H8 |
| blessed memory-ordering idioms | reference/rt_plane_rules_manifest.md section R6 |
| syscall classification per leg | reference/rt_plane_rules_manifest.md section R7 |
| contract-only register | reference/rt_plane_rules_manifest.md section R8 |
| stacks, residency, arenas | reference/memory_residency_manifest.md sections M2, M4, M7 |
