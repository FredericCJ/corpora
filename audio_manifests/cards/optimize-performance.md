# Card: optimize performance

**Load when:** a histogram tail, a bench outlier, a headroom shortfall — or any change proposed
"to make it faster".
**Depth:** `reference/optimization_microarch_manifest.md` (P1–P10). Kernel-shape law:
`reference/dsp_kernel_patterns_manifest.md`. Memory and layout:
`reference/memory_residency_manifest.md` section M8. Toolchain rungs:
`reference/toolchain_build_manifest.md` sections B6–B8.

Facts verified 2026-08-12. Version-dependent claims route to
`reference/audio_platform_baseline_manifest.md` (the hub); if any file disagrees with the hub, the
hub wins. Reasoning root: the child booklet `realtime-audio-pc-architecture-and-design-r1.md`
(repo root) — operationalized here, never re-argued.

## The two oracles

They outrank intuition and this card [ESTABLISHED: booklet ch. 9 preamble]:

1. **The bench harness** (P2): measured cycles on the reference class, distribution reported,
   tail included.
2. **llvm-mca** (P3): explains *why* a loop costs what it costs. [MEASURED 2026-08-12:
   `llvm-mca -mcpu=alderlake` on `clang -S` output works on the reference machine; reports
   `Dispatch Width: 6`]

Standing law: **no optimization lands without its before/after measurement** (invariant 15), and
no measurement outlives a toolchain bump unverified. *(build-catchable: bench + remark gates,
`reference/quality_gates_ci_manifest.md` section G4)* This domain's accounting: **the mean is
nearly worthless, the maximum is nearly everything** — a change is judged on average cost AND
variance, and trading a little mean for a lot of tail is a win. [ESTABLISHED: booklet section 2.6]

## The ladder — walk top-down, each rung gated by a measurement

[Derives from booklet section 9.8 (DT-7).] Exit condition: invariant 6's headroom floor (worst
observed callback ≤ 50% of period on the reference class) — **not** "as fast as possible";
unspent engineering is a budget too.

| rung | move | the gate that admits it |
|---|---|---|
| 0 | **measure and attribute**: compute-bound, memory-bound, or OS-induced? (histogram, bench, counters, the P7 stall table) | an attribution — or stop; an optimization aimed at the wrong bound is pure risk |
| 1 | **don't do the work**: algorithm, precomputation, edit-time specialization, lower quality tier. Trap priced here: silence-gating a kernel buys a data-dependent branch + a denormal-tail cliff + block-size-variant behavior — gate at block granularity with hysteresis, or not at all | kernel bench delta |
| 2 | **fix the memory**: working set inside cache budget, SoA, alignment, stride hygiene (M8). Largest and most durable wins | bench delta + working-set report diff |
| 3 | **shape the instructions**: accumulator fan-out, chain shortening, hoisted division, branch hierarchy (P4, P5) | bench delta + `llvm-mca` delta — "verify with the pipeline analyzer, not vibes" |
| 4 | **vectorize**, strictly in ladder order (`reference/dsp_kernel_patterns_manifest.md` section K5): auto-vectorization verified by remarks → pragma-assisted with reason in comment → intrinsic kernel with scalar twin, init-time dispatch (invariant 12) | remark gate + twin-equivalence test at pinned tolerance |
| 5 | **let the toolchain at it**: ThinLTO, PGO fed by the offline renderer, layout (B6, B7) | bench + remark gates re-run under LTO — inlining changes both |
| 6 | **parallelize** (`reference/concurrency_channels_manifest.md` section C7) — only after the single-core story is told | whole-schedule bench + soak tail |
| 7 | **buy it from the OS or deployment** (P9): elevation, placement, power floors, hardening rows | soak tail on the target rung |

## Bench protocol, condensed

Normative: `reference/optimization_microarch_manifest.md` section P2. [Derives from booklet
section 10.6.] A number missing any row below is not evidence:

- **Environment declared**: one named P-core, elevated like the RT plane, warm-up first, machine
  identified (CPU model, governor/power state, SMT state).
- **Frequency policy labeled** — deployment-real governor *or* pinned-frequency diagnostic run,
  stated as which. The rule that catches the most nonsense.
- **Distribution, never a scalar**: min / median / p99 / max over N ≥ 1000, normalized to
  **cycles per frame**.
- **Cache state declared**: hot-cache and cold-start are different benchmarks; run both for
  anything the composition root or a graph swap touches.
- **The sink is real**: outputs land in an optimizer-opaque sink, or you measured the empty loop.
- **Artifacts are JSON, versioned, compared**: same-machine baselines with tolerance bands;
  cross-machine only as ratios against a reference kernel measured in the same session.

## Reading the machine — commands

```sh
clang -std=c17 -O3 -march=x86-64-v3 -Rpass=loop-vectorize -Rpass-missed=loop-vectorize -c kernel.c
# healthy hot kernel: "vectorized loop (vectorization width: 8, interleaved count: 4)"
#   [MEASURED 2026-08-12: CLANG64 clang 22.1.8, restrict-qualified float saxpy]

clang -std=c17 -O3 -march=x86-64-v3 -S kernel.c -o kernel.s
llvm-mca -mcpu=alderlake kernel.s
# reference machine reports Dispatch Width: 6   [MEASURED 2026-08-12]
```

`-mcpu` names the *measurement* machine, `-march=x86-64-v3` names the *ship floor* — do not
conflate them; ISA floor and flag anchors are hub rows [VERSION-DEPENDENT - hub H8].

## When the tail will not reproduce on the bench

Walk the flush/stall inventory — `reference/optimization_microarch_manifest.md` section P7
[derives from booklet section 9.5]: branch mispredicts · denormal assists · page faults · false
sharing · contended RMW / seq_cst fences · store-forwarding and 4 KiB-aliasing stalls · frequency
and C-state transitions · µop-cache/i-cache overflow · (self-modifying code: refused outright).
Most rows have a counter or trace event that convicts or acquits — arm diagnosis mode
(`reference/observability_flightring_manifest.md` section O9) and read, don't guess.

Denormals are not an optimization topic: FTZ/DAZ per RT thread is invariant 4.
[MEASURED 2026-08-12: `_MM_SET_FLUSH_ZERO_MODE(_MM_FLUSH_ZERO_ON)` +
`_MM_SET_DENORMALS_ZERO_MODE(_MM_DENORMALS_ZERO_ON)` → MXCSR=0x9fc0 on the reference machine.]
Mechanics: `reference/rt_plane_rules_manifest.md` section R5; algorithmic hygiene:
`reference/dsp_kernel_patterns_manifest.md` section K7.

## The OS rung, quick rows

- **Windows elevation**: MMCSS "Pro Audio" via `AvSetMmThreadCharacteristicsW`, linked `-lavrt`
  [MEASURED 2026-08-12: returns a non-null handle on the reference machine, task index 418
  observed; `AvRevertMmThreadCharacteristics` works]. Linux: SCHED_FIFO via limits/rtkit/
  capability, in the product's recorded order [ESTABLISHED: booklet section 11.1]. Either way:
  **ask, verify the grant, treat refusal as a reported degraded mode** (invariant 14)
  *(runtime-catchable — go-live asserts)*. Conventions: hub H7.
- **PGO** rides the offline renderer — a deterministic, representative workload by construction;
  the profile corpus is versioned, because a stale profile mis-lays the binary. [ESTABLISHED:
  booklet section 10.5] Workflow: `reference/toolchain_build_manifest.md` section B7.
- **BOLT is Linux-leg only** [MEASURED 2026-08-12: absent from CLANG64]. The Windows layout story
  is PGO + function-sections + linker ordering. [ESTABLISHED: booklet section 10.5]
- Placement (P-cores, no SMT sharing between RT threads), power floors, and the priced deployment
  hardening rows: `reference/optimization_microarch_manifest.md` section P9.

## Refusals — re-proposed annually, still refused

[Derives from booklet sections 9.7, 11.7; register: `reference/optimization_microarch_manifest.md`
section P10.] Inline assembly (intrinsics or file the toolchain issue) · hand-scheduling a serial
dependency chain (the out-of-order engine already does it) · value-changing fast-math in core TUs
(write the algebra by hand instead — K6) · kernel modules/drivers to win priority · undocumented
scheduler tunables from forums · disabling OS security mitigations as tuning · the global
timer-resolution squeeze. Each is a review checklist line *(contract-only,
`reference/rt_plane_rules_manifest.md` section R8)*.

## Never

- Land an optimization without before/after JSON from the pinned protocol. *(build-catchable:
  bench gate)*
- Compare numbers across machines, governors, or frequency-policy labels as if same-machine.
  *(build-catchable: the artifact carries machine identity)*
- Per-call SIMD tier detection — dispatch binds once at init (invariant 12).
  *(host-test-catchable: dispatch suite)*
- Trade tail for mean — a 20% mean win that stalls 2 ms hourly is a defect with good marketing.
  [ESTABLISHED: booklet section 2.6] *(target-test-catchable: soak)*
- Benchmark a debug/dev configuration, or an unlabeled frequency policy. *(contract-only: the
  protocol's environment honesty is a register row)*
- Force-unroll or special-flag one kernel ad hoc — a special flag is a new canon row or a design
  smell. [ESTABLISHED: booklet section 10.2] *(build-catchable: flags come from TU class)*

## What you owe

Before/after bench JSON attached to the change · remark gate still green (the hot-kernel list
still vectorizes) · soak tail unchanged or better on the next target rung · the attribution note —
which ladder rung, which oracle, which bound · if a flag or tier changed: the toolchain-bump
revalidation note. An optimization nobody measured is folklore (invariant 15).

## Decisions you must not invent

Per-kernel bench tolerance bands · whether a wider SIMD tier ships (a deployed-population fact,
not a datasheet fact) · adopted deployment-hardening rows · whether release notes cite
governor-real or pinned-frequency numbers · hard core-pinning as default vs deployment row ·
the product's headroom target beyond invariant 6's floor.

## Go deeper

| question | where |
|---|---|
| the full ladder with worked attributions | `reference/optimization_microarch_manifest.md` section P1 |
| bench protocol, exact fields and JSON shape | `reference/optimization_microarch_manifest.md` section P2 |
| llvm-mca, remarks, counters — usage | `reference/optimization_microarch_manifest.md` section P3 |
| ILP recipes: accumulators, serial filters | `reference/optimization_microarch_manifest.md` section P4 |
| branch discipline and dispatch | `reference/optimization_microarch_manifest.md` section P5 |
| cache recipes | `reference/optimization_microarch_manifest.md` section P6 |
| stall/flush diagnostic table | `reference/optimization_microarch_manifest.md` section P7 |
| PGO/BOLT operations | `reference/optimization_microarch_manifest.md` section P8; `reference/toolchain_build_manifest.md` section B7 |
| OS techniques and hardening rows | `reference/optimization_microarch_manifest.md` section P9 |
| SIMD ladder and scalar twins | `reference/dsp_kernel_patterns_manifest.md` section K5 |
| FP regime, denormal hygiene | `reference/dsp_kernel_patterns_manifest.md` sections K6, K7 |
| layout and working-set budget | `reference/memory_residency_manifest.md` section M8 |
