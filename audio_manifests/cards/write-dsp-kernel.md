# Card: write a DSP kernel

**A kernel is a bounded, branch-poor, planar-float transform of one block whose output and cost are both contracts — proven by twin, golden, property, and bench, never by listening.**

Facts verified 2026-08-12. Version-dependent claims route to reference/audio_platform_baseline_manifest.md (the hub); if any file disagrees with the hub, the hub wins.
Reasoning root: the child booklet `realtime-audio-pc-architecture-and-design-r1.md` (repo root). This card operationalizes it; it never re-argues it.

**Load when:** adding a DSP op, modifying a kernel's math, or reviewing one.
**Depth:** reference/dsp_kernel_patterns_manifest.md. Performance work beyond the shape rules: cards/optimize-performance.md. The plane rules the kernel runs under: cards/write-rt-code.md.

## The standard this card serves

**The canonical kernel shape is designed to auto-vectorize, to be analyzable, and to be testable offline bit-for-bit** [ESTABLISHED: booklet sections 9.1, 14.1]. Deviations are measured exceptions with written contracts, not style.

## The shape rules

| rule | why | route |
|---|---|---|
| planar `float` blocks in/out; contiguous per-channel arrays; aligned; `restrict`-qualified | the buffer-pool slot discipline makes `restrict` true, not hopeful | compiler-catchable (canon flags) + contract-only (slot discipline) [ESTABLISHED: booklet section 9.1] |
| counted loops, block-constant bounds; nothing in the body mutates the bound | analyzability — vectorizer, llvm-mca, reviewer | analysis-catchable + review [ESTABLISHED: booklet section 9.1] |
| parameters resolved before the loop: targets consumed, coefficients fetched, ramps set up block-side | a parameter fetch inside the sample loop is a load the register allocator should have owned | contract-only, reviewed [ESTABLISHED: booklet sections 4.3, 9.1] |
| no calls in the body except compiler-port intrinsics | an opaque call is an optimization barrier and an unanalyzable stack | analysis-catchable (RT-TU pack) [ESTABLISHED: booklet section 9.1] |
| per-sample decisions are selection, not control: ternaries/min/max lowering to branchless forms | a mispredict is a mid-teens-cycle hole | host-test-catchable (bench flags outliers) [ESTABLISHED: booklet section 9.4] |
| block quantum is a multiple of the widest lane count — no scalar tail loop | a tail loop is code to maintain, test, and mispredict | build-catchable (static assert on quantum) [ESTABLISHED: booklet section 9.7] |

The teaching example — ramped gain, canonical in every clause:

```c
/* Canonical kernel shape (booklet 9.1): planar float, restrict, counted loop,
   params resolved block-side, no calls in the body. */
typedef struct { float cur, step; } gain_ramp;   /* set up at block edge (K3) */

void op_gain_process(float *restrict out, const float *restrict in,
                     gain_ramp *restrict rp, uint32_t nframes)
{
    float g = rp->cur;
    const float step = rp->step;
    for (uint32_t i = 0; i < nframes; ++i) {  /* block-constant bound */
        out[i] = in[i] * g;
        g += step;                            /* smoothing is the contract, not a nicety */
    }
    rp->cur = g;                              /* state advances once per block */
}
```

## Add an op — the walkthrough (K4 condensed)

1. **Declare it as data**: op id in the schedule's op table, state struct sized into the state arena, every parameter with its declared update semantics — smoothed (ramp shape+duration), stepped-at-block, or sample-accurate event. Unstated smoothing is how two implementations disagree audibly [ESTABLISHED: booklet section 4.3].
2. **Write the scalar twin first.** It is the readable specification, the fallback tier, and the test oracle [ESTABLISHED: booklet section 9.7].
3. **Wire the graph compiler**: mode decisions (bypass, mono/stereo, quality tier) are compiled out as emitted variants — the shipped sample loop contains no branch the edit model already decided [ESTABLISHED: booklet section 9.4].
4. **Parameter consume/ramp at the block edge** per reference/dsp_kernel_patterns_manifest.md section K3; sample-accurate events split the block at event boundaries [ESTABLISHED: booklet section 4.3].
5. **Write the owed tests** (block below) — before optimizing anything.
6. **SIMD only when the bench says so**, in ladder order (K5): auto-vectorize verified by remark → pragma-assisted with the reason in a comment → intrinsic kernel as its own TU with init-time dispatch and the scalar twin as contract. Never inline assembly; never per-call dispatch [ESTABLISHED: booklet section 9.7; ch. 3 invariant 12].
7. **If the kernel is hot, register it in the remark-gate list** (reference/toolchain_build_manifest.md section B8) so a toolchain bump cannot silently de-vectorize it [ESTABLISHED: booklet ch. 3 invariant 15]. Healthy reference remark on this machine: `vectorized loop (vectorization width: 8, interleaved count: 4)` [MEASURED 2026-08-12: clang -O3 -march=x86-64-v3 -Rpass=loop-vectorize, restrict float saxpy].

## The FP regime you write under (K6 condensed)

- FTZ/DAZ is set per RT thread by the thread adapter — not by your kernel; your kernel adds **algorithmic hygiene anyway** at feedback points (sub-audible offset/dither or periodic state flush) so cost does not depend on FP mode [ESTABLISHED: booklet section 9.6].
- Contraction is pinned on (`-ffp-contract=fast`) identically on both legs; value-changing fast-math is off in core. Want re-association? Write the algebra by hand, in the source, where it is visible and tested [ESTABLISHED: booklet sections 9.2, 9.6].
- Determinism-relevant paths call the codebase's vendored math kernels, never libm — the two legs' libm differ in ulp [ESTABLISHED: booklet section 9.6].
- `float` is the default; `double` by named exception recorded in the op's contract with its cost (classic case: low-frequency biquad coefficients near DC) [ESTABLISHED: booklet section 9.6].
- No NaN and no denormal in nominal operation — a property test proves the kernel cannot generate one from legal input; the dev-build patrol scans block edges [ESTABLISHED: booklet ch. 3 invariant 4; section 14.3].
- Any approximation (reciprocal/rsqrt refinement, polynomial) carries its tolerance **in the kernel's contract** and is tested at that tolerance — an uncontracted approximation is a drifting golden master [ESTABLISHED: booklet section 9.3].

## Where a decision may live

The branch hierarchy mirrors the graph compiler [ESTABLISHED: booklet section 9.4]:

| tier | cost | what lives here |
|---|---|---|
| edit time | free | mode decisions — bypass, mono/stereo, quality tier, topology — compiled out as emitted op variants |
| block rate | cheap; predicts near-perfectly | is this ramp active, did an event land in this block — gating straight branch-free sample runs |
| sample rate | the scarce budget | selection only — clamps, min/max, crossfade selects — spelled as ternaries/min-max that lower branchless |

Schedule dispatch itself: enum-switch for the built-in op set (ThinLTO inlines the small ops), pointer table at the extension seam — a measured choice, revisited per toolchain major [ESTABLISHED: booklet section 9.4].

## State rules

- Kernel state lives in the state arena at the slot the schedule compiler assigned; kernels receive pointers, never own storage [ESTABLISHED: booklet sections 4.5, 8.3].
- State advances once per block, never per process-call — per-callback state is the defect family invariant 20 exists to catch [ESTABLISHED: booklet section 4.4].
- State is a value: tests construct a filter mid-decay or a voice mid-release directly, so state structs stay plain data with no hidden initialization [ESTABLISHED: booklet section 14.2].

## Partition invariance — the property that owns you

Output must be invariant to how a span is partitioned into process calls, within the quantum contract [ESTABLISHED: booklet ch. 3 invariant 20]. The defect family it catches: hidden per-callback state — a filter that resets per call, a ramp that restarts, a meter that decays per call instead of per sample [ESTABLISHED: booklet section 4.4]. If your op fails it, the state model is wrong; fix the state, never the test.

## Never

- Allocate, lock, log, or call the OS — kernels are RT-plane code; cards/write-rt-code.md governs (routes: compiler + runtime-catchable).
- Call libm in a golden-covered path [ESTABLISHED: booklet section 9.6] (route: build-catchable symbol audit).
- Inline assembly, at all — intrinsics keep the compiler and analyzers in play [ESTABLISHED: booklet section 9.7].
- Per-call SIMD detection; dispatch binds once at init [ESTABLISHED: booklet ch. 3 invariant 12].
- Data-dependent per-sample branches without a comment stating why compute-both-blend loses [ESTABLISHED: booklet section 9.4].
- Silence-gate per sample — gate at block granularity with hysteresis, or not at all [ESTABLISHED: booklet section 9.8].
- Hand-schedule a serial IIR chain — the out-of-order engine already does that; the win is structural (wide across voices, transposed forms, parallel banks) or absent [ESTABLISHED: booklet section 9.2].
- Ship an optimization without its before/after measurement [ESTABLISHED: booklet ch. 3 invariant 15] (route: host-test-catchable bench gate).

## Decisions you must not invent

- The block quantum size (a small power of two, 16–64 frames; also a multiple of the widest lane count) — [OPEN NEEDS-INPUT; product pins it per booklet section 4.4].
- Default ramp shape and duration per parameter class — [OPEN NEEDS-INPUT; each parameter's contract states its own].
- Per-kernel tolerance values (twin equivalence, approximation vs oracle) — [OPEN NEEDS-INPUT; pinned in each kernel's contract, tested at that number].
- The quality-tier set an op must emit for the degrade ladder — [OPEN NEEDS-INPUT; booklet section 12.2 rung 2].
- Which ops take the `double` exception — [OPEN ASSUMED: none until a conditioning analysis or test demands it].

## What you owe when done

Per reference/testing_verification_manifest.md section T11, a new or changed kernel owes: **twin equivalence** at the pinned tolerance (scalar vs every SIMD tier); **golden master** — exact regime, both legs, if on the pinned path, tolerance regime otherwise; **properties** — silence→silence with clean state decay, bounded→bounded, no NaN/denormal from legal input under parameter fuzz, tail decay within the declared constant, and partition invariance; a **boundary-table row** (parameter extremes, denormal-adjacent input, DC, full-scale, every supported rate); a **bench** entry with before/after cycles-per-frame if performance-relevant; and the **remark-gate registration** if hot. All green on both legs through config/check.sh — the gate ledger reference/quality_gates_ci_manifest.md section G1 is what makes the kernel's contract enforceable rather than aspirational. Before trusting a green run, confirm neither the symbol-audit nor the remark gate printed GATE-NOT-WIRED (reference/quality_gates_ci_manifest.md section G9's bootstrap ritual; section G8 rule 1) — a not-wired gate passes silently and proves nothing about libm imports or de-vectorization. A failing artifact must name the kernel, the property, the seed, and the first differing frame — self-locating, per the doctrine.

## Go deeper

| question | where |
|---|---|
| kernel shape contract, normatively | reference/dsp_kernel_patterns_manifest.md section K1 |
| block quantum + partition invariance | reference/dsp_kernel_patterns_manifest.md section K2 |
| parameter consume/ramp mechanics | reference/dsp_kernel_patterns_manifest.md section K3 |
| the full add-an-op walkthrough | reference/dsp_kernel_patterns_manifest.md section K4 |
| SIMD ladder + scalar twins | reference/dsp_kernel_patterns_manifest.md section K5 |
| FP regime + denormal/NaN hygiene | reference/dsp_kernel_patterns_manifest.md sections K6, K7 |
| worked biquad example | reference/dsp_kernel_patterns_manifest.md section K8 |
| ILP, branches, cache — past the shape rules | reference/optimization_microarch_manifest.md sections P4–P6 |
| numeric suite (goldens, properties, oracles) | reference/testing_verification_manifest.md sections T4, T5 |
