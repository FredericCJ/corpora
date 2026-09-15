# DSP Kernel Patterns — Ground-Truth Manifest

**Purpose.** How a coding agent writes, registers, vectorizes, and proves a DSP op: the canonical kernel shape (K1), the block-quantum/partition contract (K2), parameter consume/ramp/land (K3), the add-an-op recipe (K4), the SIMD ladder (K5), the pinned floating-point regime (K6), denormal/NaN hygiene (K7), and one complete worked op (K8).

Facts verified 2026-08-12. Version-dependent claims route to reference/audio_platform_baseline_manifest.md (the hub); if any file disagrees with the hub, the hub wins.

Reasoning root: the child booklet at `realtime-audio-pc-architecture-and-design-r1.md` (repo root). This file operationalizes booklet ch. 4, §9.1–§9.3, §9.6, §9.7, §14.3; it cites, never re-argues.

**Tag legend.** [ESTABLISHED: src] named primary source · [VERSION-DEPENDENT - hub H1..H9] · [MEASURED 2026-08-12] run on the reference machine, command recorded · [OPEN: ASSUMED | NEEDS-INPUT] project decision · [CC-FACT] model knowledge of API/toolchain mechanics without a source opened this session · [FLAGGED-SECONDARY] · [UNVERIFIED]. An untagged factual claim is a defect in this file.

**This file's measured battery** (stated once; rows below quote individual results from it). Every C snippet in K1–K8 was compiled on the reference machine, clang 22.1.8 CLANG64, target x86_64-w64-windows-gnu [MEASURED 2026-08-12]:

```
clang -c -std=c17 -O3 -march=x86-64-v3 -ffp-contract=fast -Wall -Wextra -Werror \
      -Rpass=loop-vectorize -Rpass-missed=loop-vectorize p_kern.c   # exit 0, remarks quoted below
clang -c -std=c17 -O3 -march=x86-64-v3 -ffp-contract=fast -Rpass=slp-vectorizer p_kern.c
llvm-nm -u p_kern.o        # zero undefined symbols
llvm-objdump -d p_kern.o   # ymm FMA confirmed in the voice-bundle kernel
```

**Deferred to siblings, not duplicated.** RT-plane banned operations and guard machinery → reference/rt_plane_rules_manifest.md sections R2/R4; FTZ/DAZ set mechanism → R5. Channels that deliver parameters and events → reference/concurrency_channels_manifest.md sections C6/C2; resource swaps → C3. Flag canon and remark-gate wiring → reference/toolchain_build_manifest.md sections B2/B8. Test machinery this file points into → reference/testing_verification_manifest.md sections T2/T4/T5/T6/T11. Arena/pool layout and alignment → reference/memory_residency_manifest.md sections M2/M3/M4/M8. The optimization ladder above the vectorize rung → reference/optimization_microarch_manifest.md sections P1/P2. Agent entry card: cards/write-dsp-kernel.md.

---

## K1. The kernel shape contract

The unit of optimization is the kernel: one op's transform of one block [ESTABLISHED: booklet §9.1, §4.4]. Everything downstream — the vectorizer, llvm-mca, the reviewer, the property suite — assumes the canonical shape below; a kernel off-shape is a defect even when it sounds right.

### The two-layer signature convention

Registered entries share one erased signature (the schedule's kernel table is homogeneous — calling a function through a mismatched pointer type is undefined behavior [ESTABLISHED: C17 6.3.2.3]); the typed kernel underneath carries the `restrict` contract:

```c
/* layer 1 — erased dispatch signature: every registered op entry implements exactly this */
typedef void (*kernel_fn)(const float *const *in, float *const *out,
                          void *restrict st, const void *restrict p, uint32_t n);

/* layer 2 — typed kernel: planar float, restrict-qualified, counted */
void op_biquad_run(const float *restrict in, float *restrict out,
                   biquad_state_t *restrict st,
                   const biquad_params_t *restrict p, uint32_t n);

/* the entry unpacks and asserts restrict at the point of use, then calls the typed kernel */
void op_biquad_entry(const float *const *in, float *const *out,
                     void *restrict st, const void *restrict p, uint32_t n)
{
    const float *restrict in0 = in[0];
    float *restrict out0 = out[0];
    op_biquad_run(in0, out0, (biquad_state_t *)st, (const biquad_params_t *)p, n);
}
```

Both layers compile clean in the battery [MEASURED 2026-08-12]. `n` is frames; legal values per K2/K3 (whole quantum in steady state, 1..quantum on event splits).

### The restrict discipline

- `restrict` on an array-of-pointers does **not** qualify the pointed-to channel pointers; qualify at the point of use by loading each channel pointer into a `restrict` local before the loop — that is what the entry layer is for [ESTABLISHED: C17 6.7.3.1, formal definition of restrict].
- The qualifier is *true, not hopeful*: the graph compiler's buffer-slot assignment guarantees distinct slots do not alias [ESTABLISHED: booklet §9.1, §4.2]. A violated `restrict` is silent UB the compiler will not diagnose — the guarantee is the slot allocator's, tested, not the kernel author's, hoped.
- Default: all ops are out-of-place. An op that wants `in == out` must declare in-place capability in its contract and drop `restrict` on those arguments; the slot allocator only emits overlapping slots for declared in-place ops [OPEN: ASSUMED default]. Route: host-test-catchable — the slot-assignment suite (T6) asserts no undeclared overlap.

### Rule rows

| # | rule | route | enforcer |
|---|---|---|---|
| K1-R1 | Planar `float32`: one contiguous array per channel; no interleaved audio inside the core (interleave/deinterleave lives at adapters — reference/device_adapter_manifest.md section D9) | host-test-catchable | port/pool contract suite (T6) [ESTABLISHED: booklet §9.1, §9.3] |
| K1-R2 | Buffer-pool slots 64-byte aligned (`_Alignas(64)` compiles clean on this toolchain [MEASURED 2026-08-12, measured block]); rung-1 kernels may *benefit from* but must not *require* alignment; only rung-3 intrinsic TUs may demand it, backed by the pool contract (M4) | host-test-catchable + runtime-catchable (dev asserts, R4) | pool suite; go-live asserts |
| K1-R3 | `in`/`out` restrict per the discipline above; no in-place execution unless declared | host-test-catchable | slot-assignment suite (T6) |
| K1-R4 | Counted loops with block-constant bounds: trip count derives arithmetically from `n`; nothing in the body mutates it [ESTABLISHED: booklet §9.1] | contract-only (review, cards/review-code.md) — side-caught: a broken shape usually kills vectorization and fails the remark gate (B8) for listed kernels | review + remark gate |
| K1-R5 | Parameters resolved **before** the loop into locals; the per-sample body reads only locals and streams. A parameter fetch inside the sample loop is a load the register allocator should have owned [ESTABLISHED: booklet §9.1] | contract-only | review; the audible subfamily (zipper) is caught by T5 properties |
| K1-R6 | No calls in the body except compiler-port intrinsic spellings — an opaque call is an optimization barrier and a stack the analyzer cannot see past [ESTABLISHED: booklet §9.1] | build-catchable | config/audit_symbols.py: `llvm-nm -u` per core object vs. allowlist (llvm-nm present [MEASURED 2026-08-12, measured block]) |
| K1-R7 | No OS headers in core TUs (booklet invariant 8) | build-catchable | config/audit_includes.py — allowlist: `stdint.h`, `stddef.h`, `stdbool.h`, `math.h` (exact set only, K6), the compiler-port header [OPEN: ASSUMED allowlist] |
| K1-R8 | No allocation/lock/blocking identifiers reachable from kernel TUs | compiler-catchable | config/rt_prelude_poison.h — `#pragma GCC poison` produces "attempt to use a poisoned identifier" on this toolchain [MEASURED 2026-08-12, measured block] |
| K1-R9 | No writable globals in kernel TUs: state exists in the state block or it does not exist | build-catchable | audit_symbols.py rejects writable-section symbols (nm classes D/B/C) in core objects [CC-FACT: nm symbol-class letters] |
| K1-R10 | Kernel TU inputs: streams, state block, resolved params, `n` — nothing else (no clock, no channel reads, no globals) [ESTABLISHED: booklet §4.1] | contract-only + build side-catch (R6/R7/R9 close most holes) | review |

Traceability: every K1 audit failure names the offending TU + symbol/include in its message, so the patch is mechanical — no rerun needed to locate it (E6 message contract).

### Never (K1)

- Never branch on a parameter inside the sample loop — specialize at graph-compile time [ESTABLISHED: booklet §4.2] or hoist to block level.
- Never fetch through a pointer chain per sample (`st->cfg->gain`): flatten into locals pre-loop.
- Never call libm transcendentals in core (K6), allocate, log, format, or touch a channel — R2 owns the full ban table.
- Never keep hidden `static` state — it breaks partition invariance (K2), replay (booklet §13.3), and the multi-instance case at once.

---

## K2. Block quantum and partition invariance

### The quantum declaration

- The core processes fixed blocks of `RT_QUANTUM` frames; the device period is the shell's problem [ESTABLISHED: booklet §4.4]. Small power of two, commonly 16–64.
- `RT_QUANTUM` must be a multiple of the **widest dispatched** SIMD lane count so steady-state kernels have no scalar tail [ESTABLISHED: booklet §9.7]: floor x86-64-v3 = 8 float lanes; a dispatched 512-bit tier = 16 [VERSION-DEPENDENT - hub H8].
- Default `RT_QUANTUM = 32` [OPEN: ASSUMED — satisfies 8- and 16-lane tiers, sits inside the booklet's 16–64 window; re-pin per product after the P2 bench].
- Declared once, statically checked (compiles clean in the battery [MEASURED 2026-08-12]):

```c
/* core/rt_config.h */
#define RT_QUANTUM      32u
#define RT_INV_QUANTUM  (1.0f / (float)RT_QUANTUM)   /* ramp steps multiply; no divide on the plane */
_Static_assert(RT_QUANTUM % 16u == 0, "quantum must be a multiple of the widest lane count");
```

Route: compiler-catchable (`_Static_assert` [ESTABLISHED: C17 6.7.10]).

### Device periods are assembled from quanta

- The adapter's paced loop (reference/device_adapter_manifest.md sections D3/D7) cuts each device period into whole quanta; a remainder carries in a small FIFO to the next callback. Cost: up to one quantum of added latency when `period % RT_QUANTUM != 0`, accounted in the end-to-end latency budget [ESTABLISHED: booklet §4.4, §7.3].
- **The quantum grid is anchored to stream position, never to callbacks**: quantum k spans stream frames `[k*RT_QUANTUM, (k+1)*RT_QUANTUM)` regardless of how callbacks partition the stream. All per-quantum actions — consume (K3), land (K3), hygiene flush (K7) — key to this grid. A grid that re-phases per render call moves those actions with callback size and silently violates invariant 20. Route: host-test-catchable — the partition property below is exactly the detector.

### Invariant 20 — the partition property

- Statement: the core's output is invariant to callback-size partitioning within the quantum contract — one span rendered as one call, or as any legal sequence of smaller calls, yields **byte-identical** output [ESTABLISHED: booklet invariant 20, §4.4, §14.3].
- Test pointer: reference/testing_verification_manifest.md section T5 — every op and the whole schedule, one-span vs. every interesting partition, byte-compared; the harness pins the parameter/event feed to quantum indices so only partitioning varies.
- This property is what makes the device period a free product variable (booklet invariant 16) — and it is the single highest-yield regression net the domain has [ESTABLISHED: booklet §14.3].

The defect family it catches — all one disease (state keyed to the *call* instead of the *stream*):

| defect | symptom |
|---|---|
| filter/delay state reset per callback | sound changes with buffer size setting [ESTABLISHED: booklet §4.4] |
| ramp restarted per callback | zipper/pumping that varies with period [ESTABLISHED: booklet §4.4] |
| meter/envelope decay per call, not per sample | meters read differently at different latencies [ESTABLISHED: booklet §4.4] |
| hygiene flush keyed to kernel invocation | last-ulp divergence between partitions (K7 rule) |
| target consume keyed to callback, not quantum | parameter timing drifts with period (K3) |
| quantum grid re-phased per render call | all per-quantum actions move (this section) |

Failure artifact self-locates (the doctrine): a T5 partition failure reports op id, seed, partition vector, and the first diverging frame index; bisection over the schedule attributes the op — what failed, where, and why, without a rerun (T13).

Event splits (K3) are also legal partitions *inside* a quantum: kernels accept any `n` in `1..RT_QUANTUM` [OPEN: ASSUMED — decision recorded in K3].

---

## K3. Parameter consume and ramp

Parameters are a dataflow, not calls: the control plane writes targets through channels (atomic scalars per independent parameter — reference/concurrency_channels_manifest.md section C6; grouped/ordered changes and events through the command ring — C2); the RT plane consumes at quantum boundaries [ESTABLISHED: booklet §4.3]. Parameters are values, never pointers; anything structural (new IR, new wavetable) is a resource swap via snapshot machinery (C3) [ESTABLISHED: booklet §4.3, parent invariant 12].

### The three declared semantics

Every parameter states its update semantics in the op contract — unstated smoothing is how two implementations of one op disagree audibly [ESTABLISHED: booklet §4.3]:

| semantics | contract fields | consume point | per-block behavior |
|---|---|---|---|
| **smoothed** | ramp shape (linear default) + duration (default one quantum) | quantum start | interpolate current → target across the block |
| **stepped** | — | quantum start | constant across the quantum; steps at quantum edges |
| **event** | event id + payload schema (O2) | at the event's frame | block loop splits at event frames; apply between segments |

Route: compiler-catchable — the semantics field is a mandatory column of the op registry row (K4 step 1); it cannot be omitted without breaking the X-macro expansion.

### The consume/ramp/land protocol

Per quantum, per smoothed parameter: (1) **consume** the target once, pre-loop, from its channel; (2) **resolve** the per-frame step `dc = (tgt - cur) * RT_INV_QUANTUM` — multiply, never divide on the plane [ESTABLISHED: booklet §9.3]; (3) **run** the kernel with ramp locals; (4) **land**: state value `:=` target exactly at quantum end, killing accumulation drift.

Two ramp spellings — the difference is measured, not stylistic:

```c
/* indexed ramp — per-sample independent: VECTORIZES */
for (uint32_t i = 0; i < n; ++i)
    out[i] = in[i] * (g0 + (float)i * dg);

/* accumulated ramp — loop-carried float dependence: DOES NOT vectorize under the pinned regime */
for (uint32_t i = 0; i < n; ++i) { out[i] = in[i] * g; g += dg; }
```

[MEASURED 2026-08-12, battery: indexed emits `remark: vectorized loop (vectorization width: 8, interleaved count: 4)`; accumulated emits `remark: loop not vectorized`. Cause: rewriting the accumulation needs re-association, which K6 bans in core TUs — the compiler is *correctly* refusing.]

Rules:

- Vectorizable ops write ramps **indexed** (`base + (float)(i0 + i) * dc`, `i0` = frame offset within the quantum) — exact under any segment split by construction, and `(float)i` is exact for `i < 2^24` [ESTABLISHED: IEEE 754 binary32, 24-bit significand], which `RT_QUANTUM` trivially satisfies. Route: build-catchable via the remark gate for listed kernels.
- Honestly-serial kernels (IIR) may **accumulate**, and then must write the ramped values back to state at kernel exit so event-split segments continue bit-exactly (K8 shows it). Route: host-test-catchable — the T5 partition sweep includes event-split partitions.
- Ramps are defined over the **quantum**, never over "the callback" — a callback-spanning ramp is defect family K2, row 2.

### Sample-accurate event splitting

Events (note-on at frame 37) travel timestamped in the command ring; the block loop splits at event frames [ESTABLISHED: booklet §4.3]. Shape (conventions of this package; not in the compiled battery):

```c
/* precondition: drain converted stream-absolute frames to quantum-relative and
   clamped late events to the current position; events are sorted by frame;
   events beyond this quantum stay queued. */
uint32_t i = 0;
while (i < RT_QUANTUM) {
    const rt_event_t *ev  = evq_peek(q);                       /* NULL when empty */
    const uint32_t    seg = (ev && ev->frame < RT_QUANTUM) ? ev->frame : RT_QUANTUM;
    if (seg > i)
        sched_run_segment(s, i, seg - i);                      /* params stay frozen */
    while (ev && ev->frame == seg) {
        op_apply_event(s, ev);                                 /* between segments only */
        evq_pop(q); ev = evq_peek(q);
    }
    i = seg;
}
```

Consequences, priced:

- Segments have arbitrary length → **kernels accept any `n` in `1..RT_QUANTUM`**; SIMD kernels carry a scalar epilogue exercised only on split paths, while the steady state stays tail-free because `RT_QUANTUM` is lane-multiple [ESTABLISHED: booklet §9.7 for the tail-free steady state]. [OPEN: ASSUMED — the alternative quantizes event frames to lane multiples (8 frames ≈ 167 µs at 48 kHz), trading sample accuracy for tail-free kernels; NEEDS-INPUT if a product wants that trade.]
- Therefore the T5 property sweep **must include odd `n`** (1, W−1, W+1, a prime) or the epilogue is untested code on the hot plane. Route: host-test-catchable.
- The whole schedule runs per segment (op order preserved); event floods are bounded by the ring's declared capacity + overflow policy with drops counted (C2; booklet invariant 2).

### Never (K3)

- Never consume a target mid-quantum, and never poll a channel from inside a kernel — consume is the schedule's job, pre-loop (K1-R10).
- Never apply an event without splitting: that is stepped semantics wearing an event costume, and it audibly quantizes timing to the quantum.
- Never smuggle a pointer through a parameter channel — ownership transfer nobody contracted [ESTABLISHED: booklet §4.3].

---

## K4. Add-an-op walkthrough

The agent recipe. File-location conventions in this section are [OPEN: ASSUMED] until the project pins them; **the gates are the contract** — each step names the gate that catches skipping it. The registry is the single source of truth the gates audit against:

```c
/* core/kernels/ops.def — one X-macro row per op; every column mandatory */
/*  name    id      state_t         params_t         latency  tol_ulp */
OP(biquad,  0x0107, biquad_state_t, biquad_params_t, 0,       1)
```

Expansion sites: the `op_code_t` enum, both kernel tables (K5), the arena-sizing table (booklet §4.5 step 4), the generated docs table. A missing column fails every expansion — compiler-catchable by construction.

1. **Define the contract** — `core/kernels/<name>.h`: state struct, params struct, per-parameter declared semantics (K3), legal parameter ranges, latency in frames, tolerance in ulp. Add the `ops.def` row. *Gate:* compiler-catchable — the row does not expand without the types and fields; review card cards/write-dsp-kernel.md.
2. **Register ids** — op id in `ops.def` (stable, never reused: schedule hashes, goldens, and session replays reference it [ESTABLISHED: booklet §4.2 — the schedule is evidence]); runtime event ids per reference/observability_flightring_manifest.md section O2; boundary-validation error codes per reference/error_tracing_contract_manifest.md section E3. *Gate:* build-catchable — config/check.sh id-uniqueness audit (G3) fails naming both claimants.
3. **Write the scalar kernel** — `core/kernels/<name>.c`, per K1. This is the twin (K5) even if a SIMD tier comes later — it is written first, not retrofitted. *Gate:* compiler-catchable poison (K1-R8) + build-catchable include/symbol audits (K1-R6/R7/R9).
4. **Declare latency and tolerance honestly** — latency = frames of pure delay introduced (0 for memoryless and IIR ops; compensated group delay for linear-phase FIR). *Gate:* host-test-catchable — the T6 latency property renders an impulse and asserts measured offset == declared; T4 comparisons consume `tol_ulp`. A lie fails with declared-vs-measured in the message — self-locating.
5. **Graph-compiler registration** — the schedule emitter picks the op up from `ops.def`: kernel-table row (K5), state/param sizes into arena sizing, slot arity for buffer assignment. *Gate:* compiler-catchable (X-macro) + host-test-catchable — the schedule-compile smoke test instantiates every registered op once (T6).
6. **Write the tests the change owes** (T11) — `tests/ops/<name>_test.c`: unit rows; the T5 property set instantiated (partition invariance incl. event splits and odd `n`, silence-tail, no-NaN-under-fuzz, bounded-out; linearity if claimed); golden master(s) per T4; twin equivalence if a SIMD tier exists. *Gate:* build-catchable — the check.sh coverage audit cross-references `ops.def` against test names; the T2 naming contract is what makes op↔test linkage mechanical (traceability doctrine at work). Missing suite fails the G1 ledger.
7. **Add the bench entry** — `bench/<name>_bench.c` under the P2 protocol; if the op is on a product hot path, list it in `bench/hot_kernels.list` — listing is what wires both the remark gate (K5) and the bench-regression gate (G4). *Gate:* build-catchable — same cross-reference audit; an unlisted hot kernel has contract-only performance until listed, and review must say so.
8. **Docs row** — the op table is *generated* from `ops.def` into the project reference (build target). *Gate:* build-catchable for presence (generated = cannot drift); the prose meaning of parameters stays contract-only review.

Removal runs the recipe in reverse: delete the row, let the same audits enumerate every orphaned artifact (tests, goldens, bench, docs).

### Nonlinear / harmonic-generating ops — the recipe's silent gap

The eight steps above and T11's "new op / kernel" row cover shape, latency, ids, and the six T5 properties — none of which bounds harmonic content. A waveshaper, saturator, or hard/soft clipper generates energy above its input's bandwidth; run unmitigated at a typical sample rate, that energy aliases straight back into the passband, and nothing in K1–K8 or T5 catches it (partition invariance, silence-tail, no-NaN, and bounded-out are all satisfied by a badly-aliasing clipper). Whether such an op owns an oversampling stage, a bandlimited derivation (e.g. ADAA), or a documented, reviewed Nyquist-margin exception is [OPEN: NEEDS-INPUT] — the recipe does not resolve it, and shipping a harmonic-generating op without an explicit answer here is an aliasing defect nobody's gate was watching for.

---

## K5. The SIMD ladder

Strictly in this order [ESTABLISHED: booklet §9.7]; each rung is entered only when the previous rung failed a **measurement** (P1/P2), never a vibe. The class floor guarantees 8-wide single-precision FMA [ESTABLISHED: booklet §9.7; ISA floor: hub H8].

### Rung 1 — auto-vectorization, verified

The K1 shape + SoA layout (M8) is designed to auto-vectorize; rung 1 is where kernels should live and die [ESTABLISHED: booklet §9.7]. "Verified" means remark-gated, because the silent failure mode is a toolchain bump quietly de-vectorizing a hot kernel (booklet invariant 15):

- Loop-vectorizer remark to gate on — `clang -c -O3 -march=x86-64-v3 -Rpass=loop-vectorize` on a restrict-qualified float saxpy emits: `remark: vectorized loop (vectorization width: 8, interleaved count: 4)` [MEASURED 2026-08-12, measured block].
- **Fixed-trip inner loops vectorize by a different mechanism**: a trip-8 voice-bundle loop is fully unrolled at -O3 and vectorized by SLP — it emits **no** loop-vectorize remark (`-Rpass-missed=loop-vectorize` even reports the enclosing loop "not vectorized") while `-Rpass=slp-vectorizer` reports `remark: Stores SLP vectorized with cost -85 and with tree size 24` and the disassembly shows 8-lane `vfmadd231ps`/`vmulps` on ymm [MEASURED 2026-08-12, battery]. **The remark gate must match the kernel's mechanism**: gate loop-shaped kernels on `loop-vectorize`, bundle kernels on `slp-vectorizer` or on an objdump check for vector FMA. Wiring: B8/G4.
- Machine-readable remarks: `-fsave-optimization-record` emits per-TU YAML with file:line:col for the gate to parse instead of grepping stderr [CC-FACT — flag long-standing in clang; verify once against the pinned toolchain, hub H3]. Remarks are self-locating failure artifacts: the gate's failure message carries the kernel's source location verbatim.
- Route: build-catchable — a listed hot kernel that stops vectorizing fails the build (B8, G4).

### Rung 2 — pragma hints via the compiler port

Where the vectorizer balks for a stated, understood reason (assumed dependence the design knows is false; profitability misjudgment on a short loop), encode the fact the human knows, in place, with the reason in a comment [ESTABLISHED: booklet §9.7]:

```c
/* compiler-port spelling; the pragma line is MEASURED-accepted under -Werror on this toolchain */
#pragma clang loop vectorize(enable) vectorize_width(8) interleave_count(4)
for (uint32_t i = 0; i < n; ++i) ...
```

[MEASURED 2026-08-12, battery: the pragma compiles under `-Wall -Wextra -Werror` and the loop vectorizes width 8, interleave 4.] `vectorize(assume_safety)` additionally asserts no loop-carried dependence — a wrong assertion is silent miscompilation, so it requires a comment naming *why* the dependence is false, plus review [CC-FACT: clang loop-pragma semantics].

Limit, measured: pragmas do not override numeric legality — the accumulated ramp stays scalar with or without the hint (K3); restructure the arithmetic instead. Route: build-catchable for the effect (remark gate); contract-only for the justifying comment.

### Rung 3 — intrinsic TUs, init-time dispatch, the scalar twin

For algorithms lane-shaped in ways no vectorizer finds: FFT butterflies, polyphase interleaves, horizontal reductions in a compressor's link stage [ESTABLISHED: booklet §9.7].

- One TU per ISA tier — `core/kernels/<name>_<isa>.c` [OPEN: ASSUMED naming] — compiled with that tier's target flags, quarantined like any platform fact (per-leg flag rows: B4).
- Dispatch binds **once, at the composition root, before go-live** — never per-call detection, never IFUNC across the portability line [ESTABLISHED: booklet §9.7, invariant 12]:

```c
typedef struct { kernel_fn k[OP_COUNT]; } rt_kernel_table_t;   /* OP_COUNT from ops.def */

extern const rt_kernel_table_t rt_kernels_scalar; /* the twins: complete by construction   */
extern const rt_kernel_table_t rt_kernels_v3;     /* intrinsic tier: sparse rows fall back */

/* composition root, once: CPUID -> pick table -> freeze pointer into the engine.
   The RT plane sees one immutable table pointer for the life of the stream.   */
const rt_kernel_table_t *rt_kernels_bind(void);
```

- **The twin is the contract** [ESTABLISHED: booklet §9.7]: the scalar twin is simultaneously the fallback tier, the readable specification, and the test oracle. Equivalence intrinsic-vs-twin is a per-commit host test at the op's pinned `tol_ulp` — tolerance regime owned by reference/testing_verification_manifest.md section T4. A twin that drifts fails the build, not the listener.
- Wider tiers (512-bit and beyond) are additional dispatch entries built the same twin-tested way, justified by bench + soak on the deployed population — the floor never rises [ESTABLISHED: booklet §9.7]; per-generation frequency caveats are hub facts [VERSION-DEPENDENT - hub H8].

### Lane rules and Never (K5)

- **Lanes are instances** (voices, channels) wherever the choice exists — horizontal single-signal vectorization spends its gains on shuffles [ESTABLISHED: booklet §9.7]. K8's bundle kernel is the template.
- `RT_QUANTUM` is lane-multiple, so the steady state has no scalar tail; only event splits exercise the epilogue (K2/K3).
- **Never inline assembly, at all** — intrinsics keep the scheduler, allocator, and analyzers in play; the day an intrinsic cannot express it is the day to file the toolchain issue [ESTABLISHED: booklet §9.7]. Route: build-catchable — check.sh greps core TUs for `asm`/`__asm__` (G3).
- Never detect ISA per call; never re-bind after go-live. Route: host-test-catchable — T6 asserts table-pointer identity across a session.
- Never hand-unroll what the vectorizer already does — the µop cache is a budget and the vectorizer's defaults are near-right on this class [ESTABLISHED: booklet §9.3]; measure first (P2).

---

## K6. The floating-point regime

Booklet invariants 4 and 11 as kernel-facing mechanism [ESTABLISHED: booklet §9.6]. The flag canon lives in reference/toolchain_build_manifest.md section B2; this section states what kernels may assume.

### Pinned flags per TU class

| flag / class | core kernel TUs | control/shell TUs | tag & note |
|---|---|---|---|
| `-ffp-contract=fast` | **pinned ON, both legs** | ON | [ESTABLISHED: booklet §9.6] Consequence, documented: results differ from a no-FMA build in the last ulp — harmless *because* it is pinned identically on both legs and inside every golden's conditions |
| value-changing fast-math: `-ffast-math`, `-funsafe-math-optimizations`, `-fassociative-math`, `-freciprocal-math`, `-ffinite-math-only`, `-fno-signed-zeros` | **banned** | by measured exception only (B2) | [ESTABLISHED: booklet §9.6 for the ban; CC-FACT for the clang flag spellings] Each breaks determinism (invariant 11) or the NaN/Inf semantics K7 relies on. A wanted fast-math-style win is written into the algebra by hand, visible and tested [ESTABLISHED: booklet §9.2, §9.6] |
| `-fno-math-errno` | ON | ON | [CC-FACT] not value-changing; frees the compiler to inline `sqrtf` & co. as instructions. Pin explicitly; do not rely on a target default |
| `-fveclib=<lib>` | **never set** | — | [CC-FACT] would route vectorized loops to an external vector-math library: cross-leg nondeterminism + an instant audit_symbols failure |

Route: build-catchable — check.sh verifies the canon against the compile database (G3). Link-time trap worth one row: GNU-driver toolchains link `crtfastmath.o` into binaries built with `-ffast-math`/`-Ofast`, setting FTZ/DAZ **process-wide** in a startup constructor — one more reason the core ban is absolute and FTZ is set explicitly per RT thread instead (R5) [CC-FACT — verify on this leg via the map file, B9].

What the regime buys: same state + params + input + kernel selection + pinned flags → **bit-identical output on both legs** [ESTABLISHED: booklet §4.1, §9.6, invariant 11]; the cross-leg exact-golden gate (G6) turns that from a promise into a per-commit test.

### The vendored-math rule and the IEEE-exact carve-out

- The two legs' libm implementations legitimately differ in ulp → **determinism paths call no system math library** [ESTABLISHED: booklet §9.6]. Transcendentals in kernels are the codebase's own vendored approximations (polynomial/table), each with a contract: domain, max error (ulp or dB floor), and an oracle test against a high-precision reference (T4/T5). An approximation nobody contracted is a drifting golden master [ESTABLISHED: booklet §9.3]. The control plane uses system libm freely.
- **Carve-out — the IEEE-exact set is allowed in core**: `fabsf`, `copysignf`, `sqrtf`, `fminf`, `fmaxf`, `fmaf`. These are exact operations, not approximations — square root is correctly rounded [ESTABLISHED: C17 Annex F (IEC 60559 binding), F.10.4.5], abs/copysign are sign-bit operations, fmin/fmax NaN handling is pinned [ESTABLISHED: C17 Annex F.10.9] — so they cannot diverge across legs. On this toolchain a TU calling all six compiles to **zero undefined symbols** — everything lowers inline to instructions [MEASURED 2026-08-12, battery: `llvm-nm -u` empty].
- Enforcement: config/audit_symbols.py — core objects' permitted undefined set is `{memcpy, memset, compiler-rt builtins}` (the compiler may synthesize those calls even without source spelling [CC-FACT]); any `sinf`/`cosf`/`expf`/`powf`/`tanhf`/… import fails the build naming TU + symbol. Route: build-catchable.

### Width policy

| quantity | width | rationale | tag |
|---|---|---|---|
| stream samples, buses, scratch | `float` | bandwidth + 8 lanes per ymm | [ESTABLISHED: booklet §9.6] |
| op state, default | `float` | same economics | [ESTABLISHED: booklet §9.6] |
| low-frequency biquad coefficients/state (poles near DC) | `double`, **by named exception** in the op contract, cost recorded (half the lanes, twice the bytes) | 32-bit conditioning goes unstable near DC | [ESTABLISHED: booklet §9.6] |
| long mix accumulations | `float` + structural compensation (balanced-tree order; Kahan ≈ 4× the adds, reserved for offline/mastering paths) | re-association is manual and visible | [ESTABLISHED: booklet §9.2] |
| stream position / time | `uint64_t` frames — the core's only clock | position in the stream is the clock | [ESTABLISHED: booklet §4.1] |
| `long double` | **banned in core, both legs** | MinGW leg = 80-bit x87, other ABIs = 64-bit → cross-leg divergence by type choice | [CC-FACT ABI widths; route: build-catchable — check.sh grep (G3)] |

---

## K7. Denormal and NaN hygiene

Audio is the denormal literature's favorite victim: decaying tails and feedback paths glide asymptotically into the denormal range and sit there, each op taking a microcode assist — a reverb idling at 2% CPU costing 40% on *silence* [ESTABLISHED: booklet §9.6].

### Mode set — but algorithms stay mode-independent

- FTZ/DAZ is set per RT thread at thread start — mechanism and MXCSR details: reference/rt_plane_rules_manifest.md section R5; `_MM_SET_FLUSH_ZERO_MODE + _MM_SET_DENORMALS_ZERO_MODE → MXCSR=0x9fc0` on the reference machine [MEASURED 2026-08-12, measured block]. The development-build patrol re-verifies at block edges, because a library call on the wrong plane can silently restore precise mode — a performance cliff no correctness test sees [ESTABLISHED: booklet §9.6]. Route: runtime-catchable (dev guards, R4).
- **Kernel cost must not depend on the FP mode**: feedback structures carry algorithmic hygiene, and the mode becomes defense in depth, not a correctness input [ESTABLISHED: booklet §9.6]. Detector: the T5 silence-tail property runs in a plain host test process (no FTZ) and asserts state decays *exactly clean* — an op relying on FTZ to terminate its tail fails there, on any machine.

### The two hygiene patterns (feedback paths)

```c
/* A — quantum-edge flush of decayed state: runs in the op's QUANTUM EPILOGUE,
       never in the kernel body (see the partition rule below). */
static inline float rt_flush_tiny(float x) {
    return (fabsf(x) < 1e-20f) ? 0.0f : x;   /* ~ -400 dBFS; fabsf lowers inline, K6 */
}

/* B — sub-audible injection at the feedback summing point: per sample, stateless
       against partitioning, kills the decay-to-denormal asymptote at the source. */
st->dn = -st->dn;                 /* alternating ±1e-15f, set at op init */
const float xf = x + st->dn;      /* feed the recursion the offset, not the raw input */
```

- Threshold `1e-20f` and offset `1e-15f` are the field's standard practice values; booklet §9.6 names the patterns editorially, the constants are the project's to pin [OPEN: ASSUMED values].
- Noise-shaped dither variants draw from the seeded PRNG owned by state — never entropy the shell did not inject [ESTABLISHED: booklet §4.1].
- **Partition rule**: hygiene actions key to the quantum grid (pattern A: epilogue, once per quantum) or to the sample (pattern B) — **never to kernel invocation**. A flush per segment or per callback produces different output under different partitions: invariant-20 violation, same disease as per-callback resets (K2 table). Route: host-test-catchable — the T5 partition sweep includes an event-split partition precisely to catch this.

### Properties and fuzz (owed by every op with memory)

| property | assertion | route / pointer |
|---|---|---|
| silence-tail | silence in → silence out, and state decays below the op's declared floor within its declared time constant, ending exactly clean | host-test-catchable — T5 [ESTABLISHED: booklet §14.3] |
| no-NaN/denormal generation | full-range fuzz over *legal* parameter ranges never yields NaN/Inf/denormal in output **or state** | host-test-catchable — T5; fuzz lane T9 [ESTABLISHED: booklet §14.3] |
| bounded-in → bounded-out | for the sentinel-guarded bus | host-test-catchable — T5 [ESTABLISHED: booklet §14.3] |

A NaN in a feedback path is permanent and spreading; kernels do **not** test per sample — the dev patrol scans block edges and state snapshots, and boundary validation (E3 expected-condition codes) keeps illegal parameters out [ESTABLISHED: booklet §9.6]. Route: runtime-catchable (dev) + host-test-catchable (properties).

### The output sentinel (final bus, always on)

```c
/* clamp + replace + count; one pass at the final mix bus, before adapter conversion (D9) */
static inline float rt_bus_sentinel(float x, uint32_t *bad) {
    if (!(x > -2.0f && x < 2.0f)) {                       /* NaN fails both compares */
        *bad += 1;
        x = (x != x) ? 0.0f : (x < 0.0f ? -2.0f : 2.0f);  /* NaN -> 0; Inf/runaway -> clamp */
    }
    return x;
}
```

- The loop form vectorizes: `remark: vectorized loop (vectorization width: 8, interleaved count: 2)` [MEASURED 2026-08-12, battery] — cheap enough to be always-on, invariant-5 economics. Clamp bound ±2.0 (+6 dB over full scale) [OPEN: ASSUMED].
- The count lands in the per-quantum counter canon (reference/observability_flightring_manifest.md section O5); the first occurrence per session emits a flight-ring event with schedule context (O2). Together they join the evidence chain (reference/error_tracing_contract_manifest.md section E7) and the session report (E8): a nonzero sentinel count arrives self-located — which session, which quantum, how many samples, and what parameter/event activity preceded it in the ring. Route: runtime-catchable.
- The sentinel **replaces, never fixes**: the defect stays a defect (disposition per plane: E2); the sentinel's job is that the listener keeps ears and the agent gets a trail.

### Never (K7)

- Never silence-gate a kernel with a per-sample data-dependent branch — it trades constant cost for a mispredicting branch plus a denormal-tail cliff plus block-size-variant behavior; gate at block granularity with hysteresis, or not at all [ESTABLISHED: booklet §9.8 rung 1].
- Never flush state inside the kernel body (partition hazard — rule above).
- Never test for NaN per sample in release kernels; that is the patrol's and the sentinel's job [ESTABLISHED: booklet §9.6].

---

## K8. Worked example: op `biquad`

The K4 recipe instantiated on one tiny real op. All code below is from this file's compiled battery [MEASURED 2026-08-12].

### Contract (`core/kernels/biquad.h` + `ops.def` row)

```c
OP(biquad, 0x0107, biquad_state_t, biquad_params_t, /*latency*/ 0, /*tol_ulp*/ 1)
```

| field | value | tag |
|---|---|---|
| function | 2nd-order IIR section, direct form 2 transposed | [CC-FACT: standard DF2T structure] |
| params | `c[5] = {b0,b1,b2,a1,a2}`, computed **control-side at edit rate** — coefficient math never runs in the kernel | [ESTABLISHED: booklet §9.3] |
| semantics | smoothed, linear, one quantum (K3) | contract field |
| validation (control-side, per E3) | stability triangle `|a2| < 1 && |a1| < 1 + a2`; violation → `E_OP_COEFFS_UNSTABLE`, rejected at the boundary | [CC-FACT: standard 2nd-order stability condition] |
| state | `z1, z2` + current-coefficient mirror `c[5]` (ramp continuation) | this file |
| latency | **0 frames** (IIR phase delay is not latency); asserted by the T6 impulse property | K4 step 4 |
| tol_ulp | 1, for twin/tier equivalence (T4) | [OPEN: ASSUMED] |
| width exception | none at audio rates; a near-DC variant registers separately as `biquad_lf` with `double` state per the K6 width table | [ESTABLISHED: booklet §9.6] |
| RT event ids | none — the bus sentinel (K7) owns output faults | — |

Ramp caveat, priced: linearly interpolating between two stable coefficient sets can pass through ringing intermediates on large jumps; the control plane rate-limits target deltas [OPEN: ASSUMED policy — NEEDS-INPUT if the product prefers crossfaded coefficient swaps via the C3 snapshot path instead].

### State, params, resolve/land

```c
typedef struct { float z1, z2, c[5]; } biquad_state_t;    /* c = current coefficients, ramping */
typedef struct { float tgt[5], dc[5]; } biquad_params_t;  /* resolved at quantum start */

/* resolve (quantum start): dc[k] = (tgt[k] - st->c[k]) * RT_INV_QUANTUM   — multiply, no divide
   land    (quantum end):   st->c[k] = tgt[k]            — exact landing kills accumulation drift */
```

### Scalar kernel — the twin (~20 lines, compiled)

```c
void op_biquad_run(const float *restrict in, float *restrict out,
                   biquad_state_t *restrict st,
                   const biquad_params_t *restrict p, uint32_t n)
{
    const float d0 = p->dc[0], d1 = p->dc[1], d2 = p->dc[2],
                d3 = p->dc[3], d4 = p->dc[4];              /* params pre-loop: K1-R5 */
    float b0 = st->c[0], b1 = st->c[1], b2 = st->c[2],
          a1 = st->c[3], a2 = st->c[4];
    float z1 = st->z1, z2 = st->z2;
    for (uint32_t i = 0; i < n; ++i) {
        const float x = in[i];
        const float y = b0 * x + z1;                        /* DF2T */
        z1 = b1 * x - a1 * y + z2;
        z2 = b2 * x - a2 * y;
        out[i] = y;
        b0 += d0; b1 += d1; b2 += d2; a1 += d3; a2 += d4;   /* accumulated ramp: serial kernel */
    }
    st->c[0] = b0; st->c[1] = b1; st->c[2] = b2; st->c[3] = a1; st->c[4] = a2;
    st->z1 = z1; st->z2 = z2;      /* raw writeback; hygiene flush lives in the quantum epilogue */
}
```

- The loop reports `remark: loop not vectorized` [MEASURED 2026-08-12, battery] — **expected and accepted**: DF2T is honestly serial (`z1 → y → z1`); the win is across instances, not inside the chain [ESTABLISHED: booklet §9.2]. Do not list this kernel in the loop-vectorize remark gate; list the bundle below.
- Accumulate-spelling ramp + coefficient writeback gives bit-exact continuation across event-split segments (K3 rule for serial kernels); the land step at quantum end snaps `c[]` to `tgt[]`.
- Hygiene per K7 pattern A, in the epilogue, not here:

```c
void rt_quantum_epilogue_biquad(biquad_state_t *restrict st) {
    st->z1 = rt_flush_tiny(st->z1);
    st->z2 = rt_flush_tiny(st->z2);
}
```

### SoA 8-voice bundle — the rung-1 vector form

```c
typedef struct { float z1[8], z2[8]; } bq8_state_t;                    /* lanes are instances */
typedef struct { float b0[8], b1[8], b2[8], a1[8], a2[8]; } bq8_coefs_t;

void op_biquad8_run(const float (*restrict in)[8], float (*restrict out)[8],
                    bq8_state_t *restrict st, const bq8_coefs_t *restrict p, uint32_t n)
{
    for (uint32_t i = 0; i < n; ++i) {
        for (uint32_t v = 0; v < 8; ++v) {                 /* fixed trip 8: unroll + SLP */
            const float x = in[i][v];
            const float y = p->b0[v] * x + st->z1[v];
            st->z1[v] = p->b1[v] * x - p->a1[v] * y + st->z2[v];
            st->z2[v] = p->b2[v] * x - p->a2[v] * y;
            out[i][v] = y;
        }
    }
}
```

- Layout `[frame][voice]`: eight voices contiguous per frame — eight serial chains run in parallel lanes, the first-choice IIR answer because it changes no numerics [ESTABLISHED: booklet §9.2, §9.7].
- Vectorizes by **full unroll + SLP**, not the loop vectorizer: no loop-vectorize remark; `-Rpass=slp-vectorizer` reports `Stores SLP vectorized with cost -85 and with tree size 24`, and `llvm-objdump -d` shows 8-lane `vfmadd231ps`/`vmulps` on ymm registers [MEASURED 2026-08-12, battery]. Gate this kernel on the SLP remark or the objdump check (K5 rung 1; wiring G4).
- Coefficient ramp omitted in the sketch; the production version ramps per-voice exactly as the twin does.

### Owed artifacts (K4 steps 6–8 instantiated)

Names follow T2's `suite.module.contract[.case]` id grammar [reference/testing_verification_manifest.md section T2 owns the naming contract; where T2 differs, T2 wins]:

| artifact | name / location | gate |
|---|---|---|
| unit | `unit.biquad.coeff_landing_exact` · `unit.biquad.latency_is_declared_0` (impulse offset) | T6 |
| properties | `property.biquad.partition_invariance` (byte-compare; partitions include event splits and odd `n`) · `property.biquad.silence_tail_decay` · `property.biquad.no_nan_under_param_fuzz` (legal-range coefficient fuzz) · `property.biquad.bounded_out` | T5 |
| golden, exact regime | `tests/golden/biquad/lp_2k_48k.exact.raw` + `.json` sidecar (op id, params, `RT_QUANTUM`, flag fingerprint, tol=0) — byte-equal across **both legs**, per commit | T4 + G6 |
| golden, tolerance regime | twin vs `op_biquad8_run` per lane, `tol_ulp = 1` | T4 |
| bench | `bench/biquad_bench.c` (twin + bundle rows); bundle listed in `bench/hot_kernels.list` → remark gate + bench gate armed | P2 protocol; G4 |
| docs | row generated from `ops.def` | K4 step 8 |

Failure artifacts self-locate (the doctrine, closed loop): a partition failure prints op id, seed, partition vector, first diverging frame; a twin failure prints lane, frame, ulp distance vs `tol_ulp`; a remark-gate failure prints the kernel's file:line from the optimization record — in every case the agent gets what failed, where, and why, machine-readable, without a rerun (E6 message contract; T13 reading guide).

### Decisions you must not invent (register for this whole file)

`RT_QUANTUM` value (ASSUMED 32) · event-split policy: arbitrary-`n` kernels vs lane-quantized event frames (ASSUMED arbitrary-`n`) · hygiene constants (flush threshold ASSUMED `1e-20f`, injection offset ASSUMED `±1e-15f`) · sentinel clamp bound (ASSUMED ±2.0) · `tol_ulp` per op class (ASSUMED 1 for biquad-class) · op-id space partitioning (ASSUMED 16-bit, family-prefixed) · large-jump coefficient policy: rate-limited ramp vs crossfaded snapshot swap (NEEDS-INPUT) · `hot_kernels.list` membership per product (NEEDS-INPUT) · in-place op allowance (ASSUMED none). Every ASSUMED default above is usable today; every NEEDS-INPUT row blocks sealing the corresponding op contract.
