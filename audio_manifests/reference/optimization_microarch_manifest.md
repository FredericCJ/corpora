# Optimization and Microarchitecture — Operations Manifest

**Purpose.** The measure-first performance rulebook: the optimization ladder as an operating procedure, the pinned bench protocol and its JSON artifact, the tools that attribute cost, the ILP/branch/cache recipes, the stall-diagnosis dispatch table, PGO/BOLT operations, and the OS techniques with their verify-the-grant obligations.

Facts verified 2026-08-12. Version-dependent claims route to reference/audio_platform_baseline_manifest.md (the hub); if any file disagrees with the hub, the hub wins.

Reasoning root: the booklet `realtime-audio-pc-architecture-and-design-r1.md` (repo root) — this file operationalizes booklet ch. 9, sections 10.5–10.7, ch. 11, and section 15.4. It never re-argues them. Task entry: `cards/optimize-performance.md`; red-artifact entry: `cards/diagnose-failure.md`.

Two standing laws govern every section below [ESTABLISHED: booklet ch. 9 preamble, invariant 15]:

- **No optimization lands without its before/after measurement**, and no measurement outlives a toolchain bump unverified (re-check triggers: hub H9).
- The oracles are the bench harness (P2) and the static pipeline analyzer (P3) — they outrank intuition **and this file**.

Tag legend: [ESTABLISHED: source] · [VERSION-DEPENDENT - hub Hn] · [MEASURED 2026-08-12] (reference machine or a command actually run) · [OPEN-ASSUMED]/[OPEN-NEEDS-INPUT] (project decision) · [CC-FACT] (model knowledge of API/tool mechanics, no named primary source — verify at the given pointer before betting the build on it).

---

## P1. The optimization ladder

Booklet DT-7 (section 9.8), made operational. Walk top-down. Never start below rung 0. [ESTABLISHED: booklet 9.8]

| rung | move | operational content | owner |
|---|---|---|---|
| 0 | **measure + attribute** | classify the cost: compute-, memory-, or OS-bound (triage table below) | P2, P3, P7 |
| 1 | **remove the work** | algorithm, precomputation, edit-time specialization, lower quality tier | booklet 4.2; trap priced below |
| 2 | **memory/layout** | working set into budget, SoA, alignment, stride hygiene | P6, reference/memory_residency_manifest.md section M8 |
| 3 | **ILP + branches** | accumulators, chain shape, hoisted division, decision residence | P4, P5 |
| 4 | **SIMD** | the four-rung SIMD ladder, in order | reference/dsp_kernel_patterns_manifest.md section K5 |
| 5 | **toolchain** | ThinLTO, PGO, layout — amplifies whatever shape the code has | P8; reference/toolchain_build_manifest.md sections B6, B7 |
| 6 | **parallelism** | RT worker pool over the graph, after the single-core story is told | reference/concurrency_channels_manifest.md section C7 |
| 7 | **OS/deployment** | elevation, placement, power, hardening rows — the rung you control least | P9 |

### Rung 0 attribution triage

Run the bench (P2) and one counter pass (P3), then classify [CC-FACT: triage thresholds are heuristics; the convicting counters are P7's]:

| evidence | verdict | go to |
|---|---|---|
| measured cycles/frame ≈ llvm-mca predicted throughput | compute-bound at machine capability | rungs 1, 3, 4 |
| measured ≫ mca prediction; low IPC; data cache-miss counters high | memory-bound | rung 2 (P6) |
| tail only in situ, bench clean; fault/context-switch/wakeup-gap counters dirty | OS-induced | P7 lead-in, P9; reference/observability_flightring_manifest.md section O9 |
| tail scales with signal content (silence, decays, transients) | data-dependent: denormals or mispredicts | P7 rows 2, 1 |

An optimization aimed at the wrong bound is pure risk [ESTABLISHED: booklet 9.8 rung 0].

### Rung 1's priced trap: silence gating

Gating a kernel on silence trades constant cost for: a data-dependent branch (mispredict class), a denormal-tail cliff as the signal decays into the gate (booklet 9.6), and block-size-variant behavior. **Gate at block granularity with hysteresis, or not at all** [ESTABLISHED: booklet 9.8 rung 1].

| RULE | route |
|---|---|
| Silence/idle gates operate per block with hysteresis, never per sample; the gated kernel keeps partition invariance | host-test-catchable — the partition-invariance property (reference/testing_verification_manifest.md section T5) fails on block-size-variant gating |

### Gates between rungs, and the exit

| RULE | route |
|---|---|
| Every rung transition (and every landed optimization) attaches two artifacts to the change: kernel **bench delta** (P2 JSON, same machine, same frequency policy) and system **soak-tail delta** (histogram p99/max vs baseline, reference/quality_gates_ci_manifest.md section G7) | target-test-catchable — bench lane + soak rung; wiring in reference/quality_gates_ci_manifest.md section G4; what-a-change-owes: reference/testing_verification_manifest.md section T11 |
| **Exit = headroom floor met** (booklet invariant 6), not "as fast as possible" — unspent engineering is a budget too. Stop when the soak histogram on the reference class clears the floor | target-test-catchable — headroom is a trended budget fitness function (booklet 15.4) |
| A change that improves the bench median but worsens soak p99/max does not land | target-test-catchable — both artifacts gate |

---

## P2. The bench protocol

The package pin of booklet 10.6. The protocol is itself code in `tools/` and versioned [ESTABLISHED: booklet 10.6]. Two engineers' numbers may only disagree if their JSON artifacts differ in a declared field.

### Environment rows

| row | requirement | tag |
|---|---|---|
| pinning | one named P-core, affinity-pinned for the bench run | [ESTABLISHED: booklet 10.6] |
| elevation | same elevation as the RT plane (MMCSS Pro Audio / SCHED_FIFO per P9) so the bench sees RT-plane scheduling | [ESTABLISHED: booklet 10.6] |
| warm-up | discarded warm-up iterations first — arrives at measurement already credible to the governor (booklet 11.3) | [ESTABLISHED: booklet 10.6] |
| iterations | N ≥ 1000 measured iterations after warm-up | [ESTABLISHED: booklet 10.6] |
| report | **distribution, never a scalar**: min (the machine's honest capability), median, p99, max, spread — normalized to **cycles per frame** | [ESTABLISHED: booklet 10.6] |
| cache state | hot-cache (steady-state streaming) is the default; cold-start is a *different benchmark* — run both for anything the composition root or a graph swap touches | [ESTABLISHED: booklet 10.6] |
| machine identity | CPU model, SMT state, governor/power plan, OS — recorded in the artifact | [ESTABLISHED: booklet 10.6] |

### The frequency-policy declaration rule

Every artifact declares exactly one of [ESTABLISHED: booklet 10.6]:

- `"governor"` — deployment-real power policy, frequency left floating, distribution reported as-is; or
- `"pinned"` — pinned-frequency diagnostic run (deployment row: governor/plan forced to performance), labeled as such.

Honesty note: `rdtsc` counts **invariant-TSC reference ticks at a constant rate, not core cycles**; under a floating governor the same work shows varying TSC cost. That is *why* the policy field exists — compare like with like, and treat `governor`-mode numbers as wall-time-per-frame in disguise [CC-FACT: Intel SDM, invariant TSC; verify per hub H2].

| RULE | route |
|---|---|
| A bench artifact missing `frequency_policy`, machine identity, or `build_id` is rejected by the bench harness before results are written | target-test-catchable — schema validation in the bench lane (reference/testing_verification_manifest.md section T10) |
| Baselines compare **same-machine only**; cross-machine comparison only as **ratios against the fixed reference kernel measured in the same session** | target-test-catchable — the harness refuses absolute cross-machine diffs (machine id mismatch) |

The fixed reference kernel that anchors cross-machine ratios: [OPEN-NEEDS-INPUT: which kernel is pinned as the reference — proposal: the K8 biquad at 8 voices plus a 1k-tap FIR, frozen at r1].

### Timebase: serialized timestamps

Production code never reads TSC directly — it times via the clock port; the bench harness uses the clock port's **bench mode**, which on x86 is `rdtsc` with serialization at the measurement edges so the out-of-order engine cannot smear work across the boundary [ESTABLISHED: booklet 10.6; mechanism CC-FACT below].

```c
#include <stdint.h>
#include <x86intrin.h>            /* __rdtsc, __rdtscp, _mm_lfence  [CC-FACT] */

static inline uint64_t bench_t0(void) {
    _mm_lfence();                  /* prior work drains before the stamp        */
    uint64_t t = __rdtsc();        /* rdtsc is NOT itself serializing [CC-FACT] */
    _mm_lfence();                  /* the stamp lands before the kernel starts  */
    return t;
}
static inline uint64_t bench_t1(void) {
    unsigned aux;
    uint64_t t = __rdtscp(&aux);   /* stamps after prior instructions complete  */
    _mm_lfence();                  /* later code cannot hoist above the stamp   */
    return t;
}
```

[CC-FACT: `lfence;rdtsc` / `rdtscp;lfence` is the Intel-documented measurement idiom — verify against Intel SDM "RDTSCP" notes before changing it.]

### The sink is real

A benchmarked kernel the optimizer deleted measures the empty loop [ESTABLISHED: booklet 10.6]. The sink lives in the bench TU (kernel code stays intrinsics-only per K5):

```c
static volatile float bench_sink_f32;               /* volatile store: work must exist */
static void bench_sink(const float *restrict y, int n) {
    float acc = 0.0f;
    for (int i = 0; i < n; ++i) acc += y[i];        /* same cost baseline & candidate  */
    bench_sink_f32 = acc;
}
```

The zero-cost alternative — an empty `asm volatile` operand escape — is permitted **in the bench TU only** [CC-FACT: the DoNotOptimize idiom; the no-inline-asm rule of K5 binds kernels, not the harness].

### The JSON artifact (self-locating, machine-parseable)

One object per benched kernel per variant. Fields are normative; the schema file ships with the harness [OPEN-ASSUMED: `tools/bench/bench_result.schema.json`, schema-versioned like config/session_report.schema.json].

| field | type | content |
|---|---|---|
| `schema` | string | `"bench-result/1"` |
| `bench_id` | string | self-locating id: `<kernel>.<variant>` e.g. `"biquad_tdf2_x8.hot"` |
| `kernel`, `variant` | string | kernel symbol name; `"hot"` or `"cold"` |
| `git_rev`, `build_id` | string | ties the number to code + flags (reference/toolchain_build_manifest.md section B10) |
| `toolchain` | string | e.g. `"clang 22.1.8 CLANG64"` — hub H3 owns the pin |
| `machine` | object | `cpu`, `smt` (on/off), `os`, `pinned_cpu` |
| `frequency_policy` | string | `"governor"` or `"pinned"` (rule above) |
| `elevation` | object | `{requested, granted}` from the P9 grant readback |
| `block_frames`, `iters`, `warmup` | int | the run's shape |
| `cycles_per_frame` | object | `{min, median, p99, max}` |
| `spread_pct` | number | (p99−min)/min × 100 |
| `ref_ratio` | number? | this kernel / reference kernel, same session (cross-machine currency) |
| `utc` | string | ISO 8601 |

The doctrine: a regressed bench artifact alone tells the agent WHAT (bench_id → kernel symbol), WHERE (git_rev, build_id), and WHY-candidates (variant, spread, frequency_policy) — then P7 dispatches the why. CI gates on same-machine baselines with tolerance bands [tolerance values OPEN-NEEDS-INPUT — wiring: reference/quality_gates_ci_manifest.md section G4].

### Running and comparing

Harness CLI contract [OPEN-ASSUMED: harness lives in `tools/bench/`, one binary, kernel registry compiled in]:

```
bench_kernel --id biquad_tdf2_x8 --variant hot --block 64 --iters 2000 --json out/biquad.hot.json
bench_compare --baseline baselines/<machine-id>/ --candidate out/ --tolerance-from ci   # exit != 0 on regression
```

- `bench_compare` failure output is self-locating: one line per regressed kernel — `bench_id`, baseline vs candidate median and p99, delta %, both build_ids — parseable, no prose [OPEN-ASSUMED: output contract, mirrors the check-message contract in reference/error_tracing_contract_manifest.md section E6].
- Baseline update is deliberate, never automatic: a landed improvement re-blesses the baseline in the same change, and the ratchet direction is down (reference/quality_gates_ci_manifest.md section G8).
- **Cold variant recipe**: between iterations, walk a dummy buffer larger than L3 (> 30 MiB on the reference machine [MEASURED 2026-08-12; hub H2]) to evict kernel state, and measure the first block only. Eviction cost stays outside the timestamps. [CC-FACT: standard cache-eviction idiom — the honest cold measurement is the one the composition root and graph-swap paths actually pay.]

---

## P3. Measurement tools

### llvm-mca — the static pipeline analyzer

Present and working on the reference machine; `-mcpu=alderlake` reports `Dispatch Width: 6` [MEASURED 2026-08-12: `llvm-mca -mcpu=alderlake` on clang `-S` output].

```
clang -S -O3 -march=x86-64-v3 -o - kernel.c | llvm-mca -mcpu=alderlake
clang -S -O3 -march=x86-64-v3 -o - kernel.c | llvm-mca -mcpu=alderlake -timeline -bottleneck-analysis
```

[CC-FACT: `-timeline`, `-bottleneck-analysis`, `-iterations=N` flags — llvm-mca docs.] Feed it the hot loop only (extract the kernel into its own TU, or mark the region with `__asm volatile("# LLVM-MCA-BEGIN"/"# LLVM-MCA-END")` comments in the assembly — bench-TU-only trick [CC-FACT]).

What to read, in order:

| output | tells you | act |
|---|---|---|
| Block RThroughput | predicted cycles/iteration at steady state | compare to measured cycles/frame ÷ iterations — the rung-0 compute-vs-memory verdict |
| uOps Per Cycle vs Dispatch Width (6) | how full the machine is | ≪6 with long timeline stalls ⇒ dependency chain ⇒ P4 |
| Resource pressure per port | structural hazard: which unit saturates | divider pressure ⇒ hoist per P4; port-balanced ⇒ done |
| Timeline (`-timeline`) | the chain, visually — who waits on whom | accumulator count per P4 |

**mca models the core only**: it assumes L1 hits and perfect prediction — it can never convict memory or mispredict stalls [CC-FACT: llvm-mca documented limitations]. Memory verdicts come from counters (below) and P7.

Shape of the read (field names are the tool's; numbers here are placeholders except the measured one):

```
Dispatch Width:    6          <- alderlake [MEASURED 2026-08-12]
uOps Per Cycle:    <u>        <- u << 6 while pressure is low => chain-bound, go P4
Block RThroughput: <r>        <- predicted cycles/iteration; compare to measured
Resources:
[0] <port>  ...    <- one port near 100% while others idle => structural, P4/P6
```

The comparison that decides rung 0: `measured cycles/frame ÷ (frames/iteration)` vs `Block RThroughput`. Within ~20% ⇒ compute-bound and the loop is what mca says it is; measured 2× or more above ⇒ the cost is somewhere mca cannot see — memory (P6) or a P7 stall class [OPEN-ASSUMED: the 20%/2× thresholds are working heuristics, not hub facts].

### Optimization remarks

```
clang -c -O3 -march=x86-64-v3 -Rpass=loop-vectorize -Rpass-missed=loop-vectorize -Rpass-analysis=loop-vectorize kernel.c
```

On a restrict-qualified float saxpy this emits `remark: vectorized loop (vectorization width: 8, interleaved count: 4)` [MEASURED 2026-08-12]. Read `width` = lanes, `interleaved count` = independent chains the vectorizer built (P4's product). `-Rpass-missed`/`-Rpass-analysis` name the blocker when it did not vectorize. `-fsave-optimization-record` emits machine-readable `.opt.yaml` for the remark gate [CC-FACT: clang docs]. The gate that fails the build when a listed hot kernel stops vectorizing: reference/toolchain_build_manifest.md section B8; wiring reference/quality_gates_ci_manifest.md section G4 [ESTABLISHED: booklet 10.5, invariant 15].

### Hardware counters

Linux (the counter leg — run it even for Windows-observed regressions; the code is identical, booklet 10.8's TSan logic applies to counters too):

```
perf stat -e cycles,instructions,cache-misses,branch-misses,page-faults,context-switches -- ./bench_kernel --id biquad_tdf2_x8
perf stat --topdown -- ./bench_kernel ...        # level-1 bound classification
```

[CC-FACT: perf event spellings; `perf list` on the rig is the authority — hub H9 re-check trigger.] Derive per-frame rates: counter ÷ frames rendered; IPC = instructions/cycles. Windows: ETW capture via `wpr -start GeneralProfile` analyzed in WPA, or Intel VTune microarchitecture exploration for port pressure [CC-FACT: pointers only; neither is installed as part of this package — hub H5 owns availability].

### Disassembly check

Find the symbol, then read the loop body:

```
llvm-nm bench_kernel.o | grep -i biquad          # llvm-nm lists object symbols [MEASURED 2026-08-12]
llvm-objdump -d --symbolize-operands bench_kernel.o
```

What convicts what [CC-FACT: x86 mnemonics]:

| you see in the hot loop | verdict |
|---|---|
| `vfmadd…ps` on `ymm` registers | vectorized FMA — rung 4 healthy |
| `…ss`/`…sd` scalar ops only | vectorization lost — check remarks, K5 |
| `vminps`/`vmaxps`/`vblendvps`/`cmov` | branchless select — P5 healthy |
| conditional jumps inside the sample loop | a per-sample branch survived — P5 |
| `call` inside the loop body | kernel shape broken (K1: no calls in the body) |
| `vdivps`/`vsqrtps` per sample | unhoisted division — P4 |

---

## P4. ILP recipes

### The accumulator rule

One accumulator serializes a reduction on FMA latency: each add waits ~4–5 cycles while the core could issue two per cycle [ESTABLISHED: booklet 9.2]. Independent accumulators needed = **latency × throughput ≈ 8–10 chains on the class** (exact product per microarchitecture generation: [VERSION-DEPENDENT - hub H8]). Because value-changing fast-math is off in the core (K6), the compiler may **not** re-associate a single float accumulator for you — the multi-accumulator shape is written in the source, and the combine order is part of the contract [ESTABLISHED: booklet 9.2, 9.6].

```c
/* 8 lanes x 4 chains = 32 partials ~ the FMA latency x throughput product
   (hub H8). n % 32 == 0 by the block-quantum rule (dsp K2). */
float energy_r32(const float *restrict x, int n) {
    float p[32] = {0};
    for (int i = 0; i < n; i += 32)
        for (int j = 0; j < 32; ++j)     /* inner loop fully unrolls at -O3;   */
            p[j] += x[i + j] * x[i + j]; /* p[] promoted to 4 ymm accumulators */
    float s = 0.0f;                      /* combine once, fixed order:         */
    for (int j = 0; j < 32; ++j)         /* the algebra is the contract (K6)   */
        s += p[j];
    return s;
}
```

Verify the promotion happened (P3 objdump: four `ymm` accumulators, no stack spills in the loop) — the shape is a request, the disassembly is the fact [ESTABLISHED: booklet ch. 9 oracle rule].

| RULE | route |
|---|---|
| Reductions (mix busses, dot products, energy sums) in hot kernels use the multi-accumulator shape sized per hub H8, combined once at block end in a fixed order | build-catchable where the remark gate pins width×interleave for the kernel (B8); target-test-catchable otherwise (bench delta exposes the serial spine) |
| Floating-point re-association happens in the source, never via a fast-math flag; where summation error matters at the re-association, `kahan-summation` at ~4× the adds — offline/mastering paths only | compiler-catchable — core TU flag canon forbids the reassociation flags (reference/toolchain_build_manifest.md section B2); the Kahan budget decision is contract-only |

### Recursive filters: honestly serial

An IIR's next output needs its last — no window hides a true dependency; a biquad chain's cost is its latency chain [ESTABLISHED: booklet 9.2]. Mitigations **in preference order**:

| order | move | price | verification |
|---|---|---|---|
| 1 | **go wide across voices/instances**: 8 voices in 8 SoA lanes = 8 independent chains | none — numerics unchanged | bench; reference/dsp_kernel_patterns_manifest.md section K8 is the worked example |
| 2 | transposed filter forms (chain-shape variants, same cost class) | numerics shift within tolerance | [VERSION-DEPENDENT - hub H8: same-cost variant set]; measure, don't assume |
| 3 | cascade re-derived as parallel filter bank (sums independent sections) | re-derived coefficients, different rounding | oracle test at tolerance (reference/testing_verification_manifest.md section T5) before landing |
| 4 | block-level reformulation (state-space over the block) | numerics **and** complexity | oracle test at tolerance; treat as a new op, golden master re-blessed (T4) |

**Refused**: hand-scheduling the serial chain's instructions — the out-of-order engine already does that; the win is structural or absent [ESTABLISHED: booklet 9.2]. Route: contract-only (review checklist, P10 spirit).

### Chain algebra beyond filters

Chain-shortening pays everywhere: a long expression re-associated into a balanced tree, a running max as a tournament rather than a scan [ESTABLISHED: booklet 9.2]. Same contract as the accumulator rule — the rewrite is in the source, visible and tested, never delegated to a flag:

```c
/* running peak over a block: tournament, not scan.
   The scan is one compare chain n long; the tournament is 4 chains + a tail. */
float peak_r4(const float *restrict x, int n) {     /* n % 4 == 0 (K2) */
    float m0 = 0, m1 = 0, m2 = 0, m3 = 0;           /* peaks are >= 0 after fabsf */
    for (int i = 0; i < n; i += 4) {
        m0 = fmaxf(m0, fabsf(x[i+0]));  m1 = fmaxf(m1, fabsf(x[i+1]));
        m2 = fmaxf(m2, fabsf(x[i+2]));  m3 = fmaxf(m3, fabsf(x[i+3]));
    }
    return fmaxf(fmaxf(m0, m1), fmaxf(m2, m3));     /* balanced combine, fixed order */
}
```

max/abs are re-association-safe (no rounding change), so this rewrite needs no tolerance re-blessing — unlike additive re-association, which does (T5 oracle) [CC-FACT: fmax/fabs exactness per IEEE 754; the additive caveat is booklet 9.2].

### Structural hazards

Division and square root are order-of-magnitude outliers (tens of cycles, poorly pipelined) [ESTABLISHED: booklet 9.3]:

| RULE | route |
|---|---|
| Anything derivable from parameters (1/f, gain curves, normalization) is computed at edit rate or baked by the graph compiler — never at sample rate | analysis-catchable in part (P3 objdump/mca port pressure on the divider); contract-only for the derivation judgment |
| Residual per-sample division becomes a per-block reciprocal multiply; a genuinely per-sample root/reciprocal uses the ISA approximation+refinement idiom **with its tolerance written into the kernel contract and tested at that tolerance** | host-test-catchable — the tolerance test (T5); an uncontracted approximation is a drifting golden master |

---

## P5. Branch discipline

A mispredict is a mid-teens-cycle pipeline hole on the class [ESTABLISHED: booklet 9.4]. The discipline is **where a decision may live**:

| residence | decisions | cost | mechanism |
|---|---|---|---|
| **edit time** | mode, topology, mono/stereo, quality tier, bypass | free — compiled out | graph compiler emits the specialized op variant; the shipped sample loop contains no branch the edit model already decided [ESTABLISHED: booklet 9.4] |
| **block rate** | ramp active? event in this block? | ~free — predicts near-perfectly | per-block gate opens a straight branch-free run of samples |
| **sample rate** | *selection, not control*: clamp, min/max, crossfade select, waveshaper segment | scarce budget | must compile branchless — below |

### Branchless idioms

The clean C spelling reliably lowers to conditional moves and vector blends on the pinned toolchain [ESTABLISHED: booklet 9.4]:

```c
static inline float clamp01(float x)              /* min/max idiom */
    { return fminf(fmaxf(x, 0.0f), 1.0f); }
static inline float xfade(float a, float b, float t)
    { return a + t * (b - a); }                   /* arithmetic, no select at all */
static inline float gate_hard(float x, float thr)
    { return (x > thr) ? x : 0.0f; }              /* ternary = selection */
```

| RULE | route |
|---|---|
| Per-sample selection is spelled as ternary / `fminf`/`fmaxf` / arithmetic — never `if` statements in the sample body | contract-only — no pinned check in config/.clang-tidy flags a per-sample `if`; the mechanical audit is the objdump probe on a bench outlier |
| Lowering is **verified, not trusted**, whenever the bench flags an outlier: P3 objdump probe (`vmin/vmax/vblendv/cmov` present, no `jcc` in the loop). Only after a verified lowering failure may a kernel reach for the compiler port's select intrinsics | target-test-catchable — bench outlier triggers the probe; the intrinsic escalation is recorded in the kernel header |
| Data-dependent per-sample branches (gates, transient detectors — the one legitimately unpredictable class): restructure to compute-both-blend where the both-cost is cheap; accept the mispredict where the taken path is genuinely rare **and** expensive; the kernel comment says which | contract-only — the comment is the contract; review checks it exists |

### Cold-path outlining

Error and rare paths are annotated cold through the compiler port and outlined, so the hot loop's fall-through is the common case and i-cache lines carry no exception prose [ESTABLISHED: booklet 9.4]. Spelling: `RT_COLD` = `__attribute__((cold, noinline))` on the rare-path function; `RT_UNLIKELY(x)` = `__builtin_expect(!!(x), 0)` at the guard [CC-FACT: GCC/clang attribute mechanics; macro names are the compiler port's — reference/rt_plane_rules_manifest.md section R4 owns the port header]. PGO then physically separates hot from cold text (P8).

### Dispatch spelling

The schedule loop's own branch — *which kernel next* [ESTABLISHED: booklet 9.4]:

| seam | spelling | why |
|---|---|---|
| built-in op set | `enum` switch | optimizer inlines small ops into the executor; ThinLTO (B6) makes that real across TUs |
| extension seam (open op set) | function-pointer dispatch table | the only spelling an open set permits; indirect predictor learns a stable schedule's call sequence either way |

Filed "measured, revisit per toolchain major" [ESTABLISHED: booklet 9.4] — re-check trigger lives in hub H9. Route: target-test-catchable (schedule-executor bench in the lane).

---

## P6. Cache recipes

Order matters: check the budget before touching layout, layout before prefetch.

1. **Working-set budget check first.** Per-block working set (state touched + live buffers) vs the cache budget comes from the schedule compiler's report and is a trended fitness function [ESTABLISHED: booklet 15.4]. Budget numbers and layout doctrine are owned by reference/memory_residency_manifest.md section M8. Reference-machine anchors: L1d 48 KiB per P-core, L2 1.25 MiB per P-core, L3 30 MiB shared [MEASURED 2026-08-12; canonical row: hub H2]. A kernel whose state misses L2 does not get fixed by rung 3 or 4 — go back to rung 2.
2. **SoA.** Lanes are instances (voices, channels); horizontal single-signal vectorization spends its gains on shuffles [ESTABLISHED: booklet 9.7]. SoA is simultaneously the ILP answer (P4), the SIMD answer (K5), and the structural-hazard answer (unit-stride loads keep gather/scatter out of the stream, booklet 9.3).
3. **Stream sequentially.** Unit stride in, unit stride out; interleave/deinterleave only at the device adapters (reference/device_adapter_manifest.md section D9). The hardware prefetcher on this class handles unit-stride audio streams; the moment a kernel strides, it pays [ESTABLISHED: booklet 9.3, 8.4 via M8].
4. **Software prefetch: measured-only last resort.** `__builtin_prefetch` [CC-FACT: clang builtin] enters a kernel only with a P2 bench delta attached, a comment naming the distance and why the hardware prefetcher loses, and a **re-measure-per-toolchain-bump obligation** — prefetch distance is machine- and codegen-sensitive. Route: target-test-catchable (bench baseline diff on toolchain bump is a hub H9 trigger).
5. **Non-temporal stores: off the default menu.** They bypass the cache that the *next kernel in the schedule is about to read the block from* — the streaming-store use case (write once, never read soon) is the opposite of a processing graph's dataflow [ESTABLISHED: booklet 9.5 table context; mechanism CC-FACT]. Adapter-edge use would also drag fence obligations in. Anyone proposing one writes the P2 measurement first. Route: contract-only (review) — no analysis catches a plausible-looking `_mm_stream_ps`.

---

## P7. Stall/flush diagnostic table

Booklet 9.5 operationalized: **the perf-debugging dispatch table.** Entry condition: the histogram (reference/observability_flightring_manifest.md section O4) grew a tail, or a P2 bench shows an outlier. First split the taxonomy with diagnosis-mode per-callback counters (O9): **late wakeup** (wakeup-to-start gap grew → scheduling, go to P9) vs **external stall** (involuntary switches / faults mid-work → rows 3, 11 below) vs **self-overrun** (duration grew, counters quiet → rows 1, 2, 6, 9 and rung-0 triage) [ESTABLISHED: booklet 11.5].

Counter spellings are Linux `perf` and uarch-specific [CC-FACT — verify with `perf list` on the rig; hub H9]. Fix owners are this package's sections.

| # | symptom (histogram/bench) | stall class | convicting counter or probe | fix owner |
|---|---|---|---|---|
| 1 | p99 ≫ min on a kernel with data-dependent selects; jitter tracks signal content | branch mispredict | `branch-misses` per frame high vs a straight-line kernel; VTune "Bad Speculation" on Windows [CC-FACT] | P5 hierarchy |
| 2 | cost explodes on silence/decay tails — the idling-reverb signature (2%→40%) | denormal assist (microcoded FP) | probe 1: `_mm_getcsr()` on the RT thread — expect FTZ\|DAZ set (0x9fc0 observed [MEASURED 2026-08-12]); probe 2: bench the kernel on a decayed-state snapshot; counter: FP-assist event, uarch-specific [CC-FACT] | reference/rt_plane_rules_manifest.md section R5 (per-thread FTZ/DAZ) + dsp K7 (hygiene) |
| 3 | first-callback / post-swap spike; tail correlates with graph swaps or UI activity | page fault | diagnosis-mode minor/major fault deltas per callback (O9); `page-faults` in bench | reference/memory_residency_manifest.md sections M5/M6 |
| 4 | tail appears only when the control plane is busy; two threads' lines ping | false sharing | `perf c2c record/report` on Linux [CC-FACT]; probe: pad the suspect shared struct to 64 B and re-bench — the delta convicts | channel padding rules, reference/concurrency_channels_manifest.md section C2; layout M8 |
| 5 | RT thread slows when parameter traffic is heavy | contended/locked RMW, seq_cst fence | `perf record` hotspot on a `lock`-prefixed instruction [CC-FACT]; probe: replay with the producer silenced | reference/rt_plane_rules_manifest.md section R6 (blessed idioms); channel choice C1 |
| 6 | kernel cost swings with buffer base addresses; min moves when the pool re-lays slots | store-forward block / 4 KiB alias | `ld_blocks.store_forward`, `ld_blocks_partial.address_alias` [CC-FACT — uarch event names]; probe: offset one buffer by 64 B and by 4 KiB±64 B, re-bench | M8 stride staggering + pool alignment |
| 7 | first blocks after idle inflated; whole distribution shifts with power plan | frequency ramp / C-state exit (macro-stall) | probe: re-run the fixed reference kernel back-to-back — if it moved too, it is machine state, not your change; check governor/plan state | P9 power holds + composition-root warm-up (booklet 11.3) |
| 8 | hot loop regressed after adding code/unroll; IPC low, data-cache counters clean | µop-cache overflow / i-cache miss | `perf stat --topdown` front-end-bound share [CC-FACT]; probe: loop body byte size via objdump vs prior rev; mca uOps count | P5 outlining, unroll restraint (booklet 9.3), P8 layout |
| 9 | ms-scale unattributed gaps; every counter above quiet | SMI/firmware — the irreducible residue | nothing in-process convicts it; dedicated-rig hunt on Linux is a hub row [VERSION-DEPENDENT - hub H4] | posture: minimize exposure, bound damage, report honestly [ESTABLISHED: booklet 11.5] |
| 10 | involuntary context switches mid-block | preemption by a peer/interrupt | O9 counters; system-tracer correlation (ETW / perf sched) off-plane [ESTABLISHED: booklet 11.5] | P9 placement + deployment rows |
| — | self-modifying/JIT code stalls | none | refused outright in this codebase [ESTABLISHED: booklet 9.5] | P10 |

| RULE | route |
|---|---|
| Every tail investigation starts at this table with the O9 taxonomy split, and the finding attaches to the xrun's flight-ring event so the field report carries its own diagnosis | runtime-catchable — diagnosis mode armed; the soak rig runs the first counter layer always (target-test-catchable) [ESTABLISHED: booklet 11.5] |

---

## P8. PGO and BOLT operations

### PGO, end to end

Full workflow ownership: reference/toolchain_build_manifest.md section B7. The operational sequence [CC-FACT: clang PGO mechanics; flag names verified against clang docs before pinning in B7]:

```
# 1. instrumented build (IR-level PGO)
clang -O3 -march=x86-64-v3 ... -fprofile-generate=prof/ -o offline_render_inst
# 2. the ONLY sanctioned workload: the offline renderer over the versioned corpus
./offline_render_inst --corpus corpus/v1.lock      # T3 corpus-mode harness, real schedule executor
# 3. merge
llvm-profdata merge -o app.profdata prof/*.profraw # llvm-profdata present [MEASURED 2026-08-12]
# 4. optimized rebuild
clang -O3 -march=x86-64-v3 ... -fprofile-use=app.profdata -o offline_render
```

Enable clang's stale-profile diagnostics on step 4 (`-Wprofile-instr-out-of-date`, `-Wprofile-instr-unprofiled` [CC-FACT: clang warning groups — verify spelling in clang 22 docs]) and treat out-of-date as an error in CI.

Interactions, so nobody discovers them in a red build:

- PGO rides the **same ThinLTO configuration** as the release build (reference/toolchain_build_manifest.md section B6) — profiling a non-LTO build and applying to an LTO build degrades match rates [CC-FACT: clang PGO/LTO interaction].
- Instrumented builds are slower and allocate profile counters — never bench, never soak, never golden-master on an instrumented binary; it exists only to run the corpus [CC-FACT].
- `LLVM_PROFILE_FILE="prof/%m.profraw"` (the `%m` pattern) keeps multi-binary runs from clobbering profiles [CC-FACT: compiler-rt profile runtime].
- Context-sensitive PGO (`-fcs-profile-generate` second pass) exists; it is a measured-only escalation after plain PGO plateaus, not a default [CC-FACT: clang docs; decision OPEN-ASSUMED: not adopted at r1].

**The offline-renderer-as-workload rule.** This codebase has what PGO deployments rarely enjoy: a deterministic, representative workload by construction — the offline render harness (reference/testing_verification_manifest.md section T3) driving the real schedule executor over real sessions. The profile teaches the block loop's true branch biases, the dispatch's hot ops, and the hot/cold split P5 outlined [ESTABLISHED: booklet 10.5].

| RULE | route |
|---|---|
| The profile corpus (which sessions, which parameter sweeps) is **versioned with the build system**; the corpus id is part of build identity (B10). A stale or toy profile quietly *mis*-lays the binary | build-catchable — build identity mismatch fails the PGO build step |
| PGO builds ride the same remark gates as plain builds (B8): a kernel that de-vectorizes under PGO fails the same gate | build-catchable |
| Synthetic micro-benches are never the PGO workload | contract-only — review; the corpus manifest names only T3 sessions |

Corpus contents: [OPEN-NEEDS-INPUT — which sessions and parameter sweeps constitute `corpus/v1`; proposal: one dense mix session, one automation-heavy session, one idle/silence session so cold paths stay cold].

### BOLT: Linux leg only

llvm-bolt is **absent on CLANG64** [MEASURED 2026-08-12: not in the clang runtime/tool set] — BOLT is ELF-only post-link optimization; **never on the Windows leg** [ESTABLISHED: booklet 10.5]. The Windows leg's layout story ends at PGO + function-sections + linker ordering (reference/toolchain_build_manifest.md section B9).

Linux shape [CC-FACT: BOLT README mechanics — verify flags against the pinned LLVM's BOLT docs before wiring]:

```
# prerequisite: link with -Wl,--emit-relocs (and non-stripped)
perf record -e cycles:u -j any,u -o perf.data -- ./offline_render --corpus corpus/v1.lock   # LBR samples
perf2bolt -p perf.data -o perf.fdata ./offline_render
llvm-bolt ./offline_render -o ./offline_render.bolt -data=perf.fdata \
    -reorder-blocks=ext-tsp -reorder-functions=hfsort -split-functions -split-all-cold -icf=1
```

Expectations, stated so nobody over-promises: **single-digit percent on large instruction footprints** (full product text: UI + engine + adapters); a tight DSP kernel loop that already fits the µop cache gains approximately nothing [ESTABLISHED: booklet 10.5 — "pays off on large instruction footprints"]. Apply BOLT **on top of** the PGO build, profiled with the same corpus. Cross-leg determinism (invariant 11) is unaffected — layout moves code, not results [ESTABLISHED: booklet 10.5].

| RULE | route |
|---|---|
| BOLT is a Linux-leg, measured, hub-documented row ([VERSION-DEPENDENT - hub H5]); its bench + soak deltas land like any rung-5 change | target-test-catchable — P1 gate |

---

## P9. OS techniques

Everything here is a **request** — the kernel may refuse, revoke, or degrade any of it. The one absolute: **ask, verify what was granted, treat refusal as a designed, reported mode** (booklet invariant 14) [ESTABLISHED: booklet ch. 11]. Exact privilege spellings and version floors: hub H7.

The degraded-mode reporting rule, once for the whole section: every grant attempt emits a machine-readable record `{mechanism, requested, granted, os_error}` through control-plane logging (reference/observability_flightring_manifest.md section O8) and into the session report (reference/error_tracing_contract_manifest.md section E8); the composition root's recorded shortfall policy decides run/degrade/refuse. Route: runtime-catchable — the readback is code, and a start-up self-check asserts the report exists.

### Elevation

**Linux** — request SCHED_FIFO for RT threads only, via the deployment's recorded order of the three sanctioned shapes: raised `RLIMIT_RTPRIO` for the audio group → rtkit session broker → granted capability [ESTABLISHED: booklet 11.1; spellings hub H7]. Design facts honored, not fought: kernel RT throttling stays on (bounded work never approaches it; disabling it is a deployment choice, never a product requirement); broker budgets carry a kill semantic — the deadline monitor keeps the budget unreachable [ESTABLISHED: booklet 11.1].

```c
static int rt_elevate_verify(pthread_t th, int want_prio) {
    struct sched_param sp = { .sched_priority = want_prio };
    int rc = pthread_setschedparam(th, SCHED_FIFO, &sp);   /* [ESTABLISHED: sched(7)] */
    if (rc != 0) return -rc;              /* try next path in the H7 recorded order */
    int pol; struct sched_param got;
    pthread_getschedparam(th, &pol, &got);        /* read BACK: only the grant counts */
    if (pol != SCHED_FIFO || got.sched_priority != want_prio) return -EPERM;
    return 0;   /* caller emits {mechanism:"sched_fifo", requested, granted} via O8 */
}
```

Priorities within the band are ours: device loop above workers; **only the plane is elevated** — a control thread at RT priority is a design defect by definition [ESTABLISHED: booklet 11.1].

**Windows** — the sanctioned elevation is MMCSS, per thread, at thread start (device loop and RT workers):

```c
DWORD idx = 0;
HANDLE h = AvSetMmThreadCharacteristicsW(L"Pro Audio", &idx);  /* link -lavrt */
/* non-null handle observed, task index 418 [MEASURED 2026-08-12] */
if (!h) { /* GetLastError() -> {mechanism:"mmcss", granted:false} via O8; degraded mode */ }
...
AvRevertMmThreadCharacteristics(h);        /* works [MEASURED 2026-08-12]; thread exit */
```

Optional within-class nudge: `AvSetMmThreadPriority(h, AVRT_PRIORITY_HIGH)` [CC-FACT: avrt.h — verify against MS AvRt docs]. **Raw REALTIME_PRIORITY_CLASS is refused as ambient policy** — it requires elevation rights, starves the system's own machinery, and buys nothing MMCSS does not grant more safely [ESTABLISHED: booklet 11.1]. Loop integration: reference/device_adapter_manifest.md section D7.

The only elevation that counts is the one the tail distribution shows — the histogram is the standing evidence [ESTABLISHED: booklet 11.1]. Route for both legs: runtime-catchable (readback) + target-test-catchable (soak histogram).

### Placement

Intent, per thread, through the thread port; hard pinning is a deployment scalpel [ESTABLISHED: booklet 11.2].

**Windows — P-core intent = EcoQoS/power-throttling off** for the process and each RT thread [CC-FACT: Win32 processthreadsapi, Windows 11 QoS machinery — verify struct/field names in MS docs]:

```c
THREAD_POWER_THROTTLING_STATE s = {
    .Version     = THREAD_POWER_THROTTLING_CURRENT_VERSION,
    .ControlMask = THREAD_POWER_THROTTLING_EXECUTION_SPEED,
    .StateMask   = 0,                      /* 0 under the mask = throttling OFF */
};
if (!SetThreadInformation(th, ThreadPowerThrottling, &s, sizeof s))
    /* GetLastError() -> O8 degraded-mode record; never abort */;
/* process-wide twin: PROCESS_POWER_THROTTLING_STATE + SetProcessInformation(
   GetCurrentProcess(), ProcessPowerThrottling, ...) [CC-FACT] */
```

**Linux — affinity mask over P-cores where the deployment discovers topology**: hybrid core lists at `/sys/devices/cpu_core/cpus` vs `/sys/devices/cpu_atom/cpus`; SMT pairs at `/sys/devices/system/cpu/cpuN/topology/thread_siblings_list`; apply with `pthread_setaffinity_np` and read back with `pthread_getaffinity_np` [CC-FACT: Linux sysfs/pthread mechanics — verify paths on the rig; a correctly-configured distro scheduler may be trusted instead, a hub-dated judgment per kernel generation, hub H4].

| RULE | route |
|---|---|
| **Two RT threads never share a physical core** — SMT siblings share ports and L1/L2; co-residency is a scheduled-in structural hazard. Worker-pool size and masks respect physical topology (C7); the device loop ideally owns a physical core | runtime-catchable — the thread port asserts sibling-disjoint masks at pool start; reference machine: 8P×2SMT+8E [MEASURED 2026-08-12; hub H2] |
| Affinity is a scalpel: default = intent (QoS/preference); hard mask = deployment row. The control plane is **never** pinned | contract-only — review + deployment doc; the code default is intent-only |

### Power

Two taxes: **C-state exit latency** (a deeply-napped core answers the wakeup hundreds of µs late — at a 1.33 ms period, the whole reserve) and **frequency ramp** (first milliseconds after wake run below clock while the governor decides you are real) [ESTABLISHED: booklet 11.3].

**Linux — the latency floor, held while streaming**:

```c
static int pmqos_fd = -1;
int pmqos_acquire(int32_t max_exit_us) {           /* 0 = shallowest C-states only */
    pmqos_fd = open("/dev/cpu_dma_latency", O_WRONLY);   /* [CC-FACT: PM QoS iface] */
    if (pmqos_fd < 0) return -errno;
    if (write(pmqos_fd, &max_exit_us, 4) != 4) { int e = errno; close(pmqos_fd); return -e; }
    return 0;   /* kernel holds the floor while the fd stays OPEN; close() on stream stop */
}
```

**Windows — power request while streaming**: `PowerCreateRequest` + `PowerSetRequest(h, PowerRequestSystemRequired)` keeps the system awake for the stream's duration; `PowerClearRequest` on stop [CC-FACT: Win32 power requests — verify REASON_CONTEXT setup in MS docs]. There is no per-process C-state-floor API on Windows equivalent to `cpu_dma_latency`; deeper floors are power-plan deployment rows [CC-FACT]. Whether the Windows leg holds a power request by default while streaming: [OPEN-ASSUMED: yes, scoped exactly to the stream, released on stop — mirrors the Linux hold and the booklet's honesty rows about battery cost].

Warm-up: the composition root's warm-up exists partly to arrive at go-live already credible to the governor; the bench declares frequency policy for the same reason (P2) [ESTABLISHED: booklet 11.3]. The product must remain acceptable on the **stock** plan — the histogram is the judge [ESTABLISHED: booklet 11.3].

### Deployment hardening rows

A product that *requires* any row below is misdesigned (invariant 6 is proven on the stock machine); a deployment that wants headroom can buy it [ESTABLISHED: booklet 11.6]. Each adopted row is recorded in the deployment's hub section **with its verification command** (hub H7/H4).

| row | buys | costs | spelling anchor |
|---|---|---|---|
| dedicated/isolated cores (Linux boot isolation; Windows CPU sets) | scheduler noise removed from the plane | cores gone from the system; per-machine config | `isolcpus=`/`nohz_full=` cmdline; CPU Sets API [CC-FACT] |
| PREEMPT_RT kernel flavor | scheduler/IRQ-path tails shrink dramatically | a kernel decision the deployment owns; SMIs untouched | availability per distro [VERSION-DEPENDENT - hub H4] |
| IRQ affinity steered off RT cores (Linux) | driver interrupt storms miss the plane | config fragility across reboots/devices | `/proc/irq/N/smp_affinity` [CC-FACT] |
| SMT disabled in firmware | sibling interference gone; worst case sharper | throughput for the rest of the machine | firmware setup |
| governor/plan pinned to performance | frequency floors, no ramp tax | watts, heat, battery | `cpupower frequency-set -g performance`; `powercfg` high-performance [CC-FACT] |
| audio-group limits preconfigured (memlock, rtprio) | the elevation dance always succeeds | distribution packaging work | limits.conf rows, hub H7 |

---

## P10. Refusals register

Each row is one line, its why, and the review rule that keeps it dead — because each is re-proposed annually with fresh enthusiasm [ESTABLISHED: booklet 11.7]. All rows route **contract-only**: they live on the review checklist (cards/review-code.md) and in the booklet's contract-only register (booklet 15.5); no tool catches a plausible-looking PR that violates them.

| refusal | why | review rule |
|---|---|---|
| kernel modules or drivers shipped to win priority disputes | a support catastrophe wearing a performance costume [ESTABLISHED: booklet 11.7] | any PR adding kernel-mode components or driver installers is rejected on sight |
| undocumented scheduler knobs cargo-culted from forums | unverifiable, version-fragile — if it cannot be a dated hub row with a verification command, it does not exist [ESTABLISHED: booklet 11.7] | every OS tunable in a PR must cite its hub row; no hub row, no merge |
| disabling OS security mitigations as a tuning tip | measured wins on this workload do not justify the posture; never normalized [ESTABLISHED: booklet 11.7] | reject any build flag, registry key, or cmdline touching mitigation state |
| global timer-resolution squeeze (`timeBeginPeriod(1)` and kin [CC-FACT: winmm]) | the event-driven design never needed it; it taxes the whole machine to hide a pacing defect [ESTABLISHED: booklet 11.7, 7.4] | reject any timer-resolution call; pacing is the device's event, reference/device_adapter_manifest.md sections D3/D7 |
| folklore drop/dup "clock sync" (dropping/duplicating frames to chase drift) | drift is accounted and resampled where the design says [ESTABLISHED: booklet 7.2]; drop/dup is an audible defect masquerading as sync | any sample-discarding or sample-repeating path outside the designed drift owner is rejected |
| hand-scheduled instructions / inline asm in kernels | the OoO engine already schedules; intrinsics keep the compiler and analyzers in play [ESTABLISHED: booklet 9.2, 9.7] | `asm` outside the bench TU fails review; file the toolchain issue instead |
| self-modifying/JIT code on the RT plane | flush class with no owner — refused outright [ESTABLISHED: booklet 9.5] | no runtime codegen dependencies, ever |

When a refused row seems genuinely needed, the move is not an exception in code review — it is a booklet revision proposal with measurements attached [OPEN-ASSUMED: house change-control convention, mirrors the hub-wins rule].
