# Testing & Verification — Ground-Truth Manifest

**Purpose.** The testability centerpiece of audio-rt-ground: every suite kind this codebase runs, the naming and self-location contract every failure obeys, the offline renderer that makes the signal engine testable headless, and the reading guide that turns any failure artifact into a patch. The doctrine this file serves: **testability and traceability are the coding agent's feedback loop** — a failure artifact must state WHAT failed, WHERE, and WHY, machine-readably, with enough context to rerun and patch. An artifact that does not is itself the defect.

Facts verified 2026-08-12. Version-dependent claims route to reference/audio_platform_baseline_manifest.md (the hub); if any file disagrees with the hub, the hub wins.

Reasoning root: the child booklet `realtime-audio-pc-architecture-and-design-r1.md` (repo root) — ch. 14 throughout, plus §4.4 (invariant 20), §9.6–9.7, §10.8, §13.3. This file operationalizes the booklet and never re-argues it.

**Blanket tag.** The TESTFAIL grammar, directory names, artifact filenames, JSON field names, and CLI spellings of package-internal tools (`offline_render`, the golden diff/approve tools, the fake-device script) are this package's own conventions — [OPEN — ASSUMED house convention; this file is their definition]. Change them coherently across the package or not at all. Booklet obligations and external-tool facts are tagged inline.

**Deferred to siblings, not duplicated.** Bench protocol → reference/optimization_microarch_manifest.md section P2. Gate wiring and CI mechanics → reference/quality_gates_ci_manifest.md sections G1–G9. Error codes, result types, session-report schema, crash/dirty-exit mechanics → reference/error_tracing_contract_manifest.md sections E3/E4/E8/E9. Flight ring and heartbeat → reference/observability_flightring_manifest.md sections O3/O6. Torture recipes → reference/concurrency_channels_manifest.md section C8. Fake/real adapter internals → reference/device_adapter_manifest.md. Card front-ends: cards/write-tests.md, cards/diagnose-failure.md.

---

## T1. Test topology

The signal engine runs headless, deterministic, and faster than real time on any developer or CI machine — no audio device, no elevated privileges, no kernel in the loop; the offline build IS the product's own core, bit for bit (invariant 11), and "target" rungs exist to prove the shell (OS negotiation, elevation, tail behavior), not the math. [ESTABLISHED: booklet §14.1]

### Suite kinds × location × runner × cadence

Cadence column is booklet §14.6's ladder [ESTABLISHED]; placement and runner are house convention (blanket tag).

| suite kind | proves | lives in | runs against | runner | cadence |
|---|---|---|---|---|---|
| unit-kernel | one op/function honors its K1 contract | `test/unit/` | host core, both legs | suite exe (via ctest) | per-commit |
| table | per-op boundary matrices: param extremes, denormal-adjacent input, full-scale/DC, every supported rate [ESTABLISHED: booklet §14.3] | `test/unit/` | host core | suite exe | per-commit |
| property | the T5 canon | `test/property/` | host core | suite exe, seeded | per-commit |
| golden tolerance | ULP/dB-bounded equivalence: twin-vs-SIMD, approximation-vs-oracle | `test/golden/` | offline renderer (T3) | golden runner | per-commit |
| golden exact | bit-identical pinned-path output, both legs | `test/golden/` | offline renderer | golden runner | per-commit same-leg; per-merge cross-leg (G6) |
| port-contract nominal | adapter meets the D1 port contract | `test/contract/` | fake AND real adapters | suite exe; real = device-in-loop | per-commit (fake); per-release (real) |
| port-contract fault | designed events recover (invariant 19) | `test/contract/` | fakes only, by construction | suite exe | per-commit |
| state-machine | stream/device/elevation/ladder machines: transition coverage + illegal-transition asserts [ESTABLISHED: booklet §14.3] | `test/contract/` | fakes | suite exe | per-commit |
| channel stress | torture recipes of C8 | `test/stress/` | host threads | stress exe, bounded duration | per-commit short; nightly long [OPEN — ASSUMED] |
| sanitizer legs | all of the above under ASan/UBSan (both legs) and TSan (Linux only) | build variants (T8) | same suites, minus bench | same runners | per-commit |
| fuzz | foreign-byte parsers never crash (T9) | `test/fuzz/` | libFuzzer exes | libFuzzer | per-commit budget + continuous |
| bench | cost regression under the P2 protocol | `test/bench/` | pinned machine | bench harness | per-commit compare; per-merge trend |
| soak | headroom floor (invariant 6), real devices, both OSes | `test/soak/` | reference-class machines | soak driver | per-release |

### Directory layout convention

```
test/
  unit/            unit-kernel + table suites; regressions/ = fuzz-minimized repros (T9)
  property/        property canon; _artifacts/ = failure repro bundles (git-ignored, CI-uploaded)
  golden/          golden runner + diff/approve tools
    masters/       approved .f32 masters + MANIFEST.sha256 + MANIFEST.meta.json (T4)
  contract/        port-contract nominal + fault suites; state-machine suites
  stress/          channel tortures, shutdown storms, dirty-exit harness (T7)
  bench/           bench lane (T10 -> P2)
  fuzz/            <target>/fuzz_<target>.c + seeds/ + corpus/   [extends the dictated set]
  soak/            release-rung drivers (target-test)            [extends the dictated set]
tools/offline_render/   the harness engine (T3)
```

Runner: each suite compiles to a standalone executable emitting the T2 output contract; `ctest` is only the launcher/mux (config via B5's CMake presets — reference/toolchain_build_manifest.md section B5). Filter one test: `ctest -R '^property\.biquad\.' --output-on-failure` [CC-FACT: CTest flags — verify `ctest --help`]. The T2 contract is binding; the runner choice is [OPEN — ASSUMED: ctest].

### Never

- Never gate a leg on a lane it cannot run: TSan is absent on CLANG64 [MEASURED 2026-08-12: no tsan in clang runtime libs] — TSan lanes are Linux-only rows [VERSION-DEPENDENT - hub H5]. *(build-catchable — CI matrix declares lanes per leg, G5)*
- Never sleep-to-synchronize in a test; join via the harness's eventcount (C7) or bounded op counts. Wall-clock sleeps are flake generators. *(contract-only — reviewed)*
- Never compare bench absolutes across machines; gates compare same-machine baselines only (T10). [ESTABLISHED: booklet §14.5] *(build-catchable — bench gate refuses foreign baseline fingerprint, G4)*
- Never print a failure outside the TESTFAIL block (T2). *(build-catchable — G3 audit greps test TUs for raw `printf("FAIL` patterns [OPEN — ASSUMED audit rule])*
- Never auto-approve a golden master (T4). *(contract-only + G3 audit assist)*

---

## T2. Naming + self-location contract

This section is the traceability core. A failing test is a work order: it names WHAT (the contract one-liner), WHERE (module + owning reference section + sample position), WHY (expected vs actual with bits, seed), and HOW TO RERUN (seed, input artifact, build identity). Everything downstream — the diagnose-failure card, CI triage, the agent's patch loop — parses this one format.

### Test identity

```
test_id  = suite "." module "." contract [ "." case ]
suite    = unit|table|property|golden|contract|state|stress|fuzz|bench|soak
module   = the TU/op/adapter under test        (biquad, spsc_ring, wasapi_adapter)
contract = snake_case name of the claim        (partition_invariance, lp24_sweep)
case     = variant                             (exact, tol, tier_v3, seed label)
charset  = [a-z0-9_] per segment; "." reserved as separator
example  = golden.biquad.lp24_sweep.exact
```

### The rules

| # | RULE | route |
|---|---|---|
| T2-1 | Every test has a stable `test_id`; renaming one is a change that owes a note (T11). Ids are grep-anchors: `TEST_ID=` appears exactly once per failure. | build-catchable — G3 audit rejects duplicate/malformed ids [OPEN — ASSUMED audit rule] |
| T2-2 | Every test file opens with a header comment: `SPEC: reference/<file>.md <sec>` + `CONTRACT: <one line>` — the reference section that OWNS the contract under test. A test that cannot name its spec section is testing nothing. | build-catchable — G3 grep for the `SPEC:` header |
| T2-3 | Every failure prints exactly one TESTFAIL v1 block (below), then exits nonzero. Pass output is one line: `OK <test_id>`. | host-test-catchable — runner treats malformed output as failure; helper below is the enforcement |
| T2-4 | Audio diffs report the FIRST divergence as `SAMPLE` + `CHANNEL` + both values in decimal AND bit pattern (ulp math needs bits). | contract-only — use `fail_audio()`, never ad-hoc prints |
| T2-5 | Every randomized test prints `SEED`; rerunning with that seed must reproduce. No `time()`, no unseeded RNG, anywhere in test code. | host-test-catchable — CI reruns each failure once with the printed seed and flags non-reproduction [OPEN — ASSUMED CI rule] |
| T2-6 | Input artifacts are written BEFORE the comparison runs, kept on failure under `test/*/_artifacts/<test_id>/`, deleted on pass, uploaded by CI on failure. | contract-only |
| T2-7 | Every block carries `BUILD_ID` (source rev + flag fingerprint + kernel schema hash — reference/toolchain_build_manifest.md section B10; invariant 17). | build-catchable — helper links the B10 symbol |

### TESTFAIL v1 block

Machine-parse rule: block delimited by the two sentinel lines; one `KEY=value` per line; split at the FIRST `=`; keys are the fixed set below; extensions must be prefixed `X_`. [blanket tag]

```
--- TESTFAIL v1 ---
TEST_ID=property.biquad.partition_invariance.rand_cuts
SPEC=reference/dsp_kernel_patterns_manifest.md K2
CONTRACT=output invariant to callback partitioning within the block quantum
SAMPLE=48213
CHANNEL=1
EXPECT=0.664490044 (0x3f2a1c00)
ACTUAL=0.664490104 (0x3f2a1c01)
SEED=0x9e3779b97f4a7c15
INPUT=test/property/_artifacts/property.biquad.partition_invariance.rand_cuts/in.f32
BUILD_ID=g68f2854+clang22.1.8+x64v3+ffp-contract-fast+schema-4f2a
--- END TESTFAIL ---
```

Required always: `TEST_ID`, `SPEC`, `CONTRACT`, `EXPECT`, `ACTUAL`, `BUILD_ID`. Required for audio diffs: `SAMPLE`, `CHANNEL`. Required when randomized: `SEED` (`SEED=0x0` marks a deterministic test). Required when a repro artifact exists: `INPUT`. Optional free text: `MSG=` (last line before the sentinel).

### The emit helper (the only legal failure reporter)

```c
/* test_fail.h — RULE T2-3. C17. */
#include <inttypes.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

extern const char *build_id_string(void);   /* toolchain_build B10 */

typedef struct {
  const char *test_id;   /* <suite>.<module>.<contract>[.<case>] */
  const char *spec;      /* "reference/<file>.md <sec>"          */
  const char *contract;  /* one-line claim                       */
  uint64_t    seed;      /* 0 = deterministic                    */
  const char *input;     /* repro artifact path, or "-"          */
} test_ctx;

static uint32_t f32_bits(float x) { uint32_t u; memcpy(&u, &x, sizeof u); return u; }

_Noreturn static void fail_audio(const test_ctx *c, uint64_t sample, unsigned ch,
                                 float expect, float actual) {
  printf("--- TESTFAIL v1 ---\n");
  printf("TEST_ID=%s\nSPEC=%s\nCONTRACT=%s\n", c->test_id, c->spec, c->contract);
  printf("SAMPLE=%" PRIu64 "\nCHANNEL=%u\n", sample, ch);
  printf("EXPECT=%.9g (0x%08" PRIx32 ")\n", (double)expect, f32_bits(expect));
  printf("ACTUAL=%.9g (0x%08" PRIx32 ")\n", (double)actual, f32_bits(actual));
  printf("SEED=0x%016" PRIx64 "\nINPUT=%s\n", c->seed, c->input);
  printf("BUILD_ID=%s\n--- END TESTFAIL ---\n", build_id_string());
  fflush(stdout); exit(1);
}
```

Bit access via `memcpy`, not union punning or pointer casts — the strictly portable route [ESTABLISHED: C17 6.5, 6.2.6]. `%.9g` round-trips binary32 exactly [ESTABLISHED: C17 5.2.4.2.2 — 9 significant decimal digits suffice for float].

---

## T3. Offline renderer harness

`tools/offline_render` is the second composition root: it binds the fake device and fake clock adapters and drives the REAL schedule executor over scripted sessions at file-write speed. One artifact, five duties: test-suite engine, golden-master generator, PGO workload (reference/toolchain_build_manifest.md section B7), replay consumer (booklet §13.3), profiling target (reference/optimization_microarch_manifest.md section P3). It is maintained as a product, not a script. [ESTABLISHED: booklet §14.1]

### The contract

```
offline_render --schedule <file> --session <file> [--in <wav>...] --out <dir>
               --report <session_report.json> --seed <u64> --tier <scalar|v3|v512>
               --block <frames> --rate <hz> [--frames <n>] [--pace realtime]

offline_render --schedule <file> --corpus <lockfile> --out <dir> --seed <u64>
               --tier <scalar|v3|v512> --block <frames> --rate <hz>       /* batch/PGO mode: B7 */
```

| clause | statement | route |
|---|---|---|
| deterministic | same schedule + session + inputs + seed + tier + BUILD_ID → byte-identical output. This is invariant 11 made executable. [ESTABLISHED: booklet §14.1, §9.6] | host-test-catchable — the exact golden regime (T4) is the standing proof |
| tier pinning | `--tier` forces the init-time dispatch table to one tier (K5); env `AUDIO_RT_TIER` is the CI-matrix override; flag wins over env [OPEN — ASSUMED names] | host-test-catchable — renderer refuses a tier the host CPU lacks, with a distinct exit code |
| no privileges | never opens a device, never elevates, never locks memory — runs on any CI box [ESTABLISHED: booklet §14.1] | build-catchable — links fake adapters only; symbol audit (G3) proves no OS audio import |
| real executor | renders through the product's schedule executor and composition mechanics — never a parallel implementation | contract-only — reviewed; drift here silently voids every golden |
| report always | every run emits a session report (E8 schema, config/session_report.schema.json) carrying BUILD_ID, tier, seed, histograms, counters; dev builds validate the report against the schema [OPEN — ASSUMED] | host-test-catchable |
| exit codes | 0 = ok; nonzero classes from the E3 registry (session parse error, schedule error, tier unavailable, io error) — reference/error_tracing_contract_manifest.md section E3 owns the numbers | contract-only until E3 pins them |
| pacing | default as-fast-as-possible; `--pace realtime` shapes callbacks for soak-style host runs [ESTABLISHED: booklet §14.2] | — |

### Session scripts and replay

A session script is the serialized control-plane command stream — the same schema the command ring records (reference/observability_flightring_manifest.md section O2), timestamped in samples. Hand-written scripts and field-recorded rings are the same format by design: a field glitch replays bit-exactly on the developer machine and becomes tomorrow's regression test as workflow, not heroics. [ESTABLISHED: booklet §13.3]

Input WAVs: RIFF float32/PCM; conversion rules live in reference/device_adapter_manifest.md section D9 [OPEN — ASSUMED support set]. Outputs for golden comparison are written as raw f32 (T4 storage format), post-conversion-free.

---

## T4. Golden masters

Two regimes, never confused [ESTABLISHED: booklet §14.3]:

| regime | comparison | scope | preconditions | cadence |
|---|---|---|---|---|
| **exact** | byte-identical (bit compare of f32 streams) | the pinned-kernel path; cross-leg Linux↔Windows | pinned dispatch tier (`--tier v3` [OPEN — ASSUMED: floor tier per booklet §1.2]); `-ffp-contract=fast` pinned identically both legs (B2, invariant 11); NO system libm on any determinism path — vendored kernels only (K6) [ESTABLISHED: booklet §9.6] | same-leg per-commit; cross-leg per-merge (G6) |
| **tolerance** | ULP bound or dB floor per the op's contract | everything legitimately variant: SIMD tier vs scalar twin (invariant 12), approximation vs high-precision oracle, cross-tier dispatch equivalence | tolerance pinned in the op contract (K1); starting defaults: twin ≤ 4 ulp, oracle floor −120 dBFS [OPEN — ASSUMED defaults; each op must pin its own] | per-commit |

An exact-regime failure is a toolchain-or-discipline regression BY DEFINITION — the determinism conditions of §9.6 make cross-OS bit-equality a test [ESTABLISHED: booklet §14.3]. Comparison discipline (ulp distance on bit patterns, dB on RMS delta) is owned by reference/dsp_kernel_patterns_manifest.md section K6.

### Master storage

```
test/golden/masters/
  golden.biquad.lp24_sweep.f32      raw float32, little-endian, channel-planar (ch0 block, then ch1)
  MANIFEST.sha256                   sha256sum -c compatible: "<hex>  <relpath>" per line
  MANIFEST.meta.json                per-master: frames, channels, rate, tier, seed, session file,
                                    build_id of the approved render, approved_by, approved_date, reason, spec
```

Raw files carry no header — `MANIFEST.meta.json` is normative for shape; a master absent from BOTH manifest files does not exist. Verify integrity: `sha256sum -c MANIFEST.sha256` from `masters/` [CC-FACT: coreutils/MSYS2 sha256sum]. *(host-test-catchable — the golden runner refuses unhashed masters)*

### Cross-leg mechanics (the G6 gate)

Per merge: each leg renders every exact-regime session; the gate compares sha256(linux render) == sha256(windows render) == manifest hash. Hashes travel between CI jobs, not WAVs; on mismatch both candidates upload and the diff tool produces the first-divergence report below. [ESTABLISHED cadence: booklet §14.6; mechanics blanket-tag]

### The diff report

```json
{ "report": "golden_diff/v1", "regime": "exact",
  "test_id": "golden.biquad.lp24_sweep.exact",
  "master": "test/golden/masters/golden.biquad.lp24_sweep.f32",
  "candidate": "artifacts/win/golden.biquad.lp24_sweep.f32",
  "frames": 480000, "channels": 2,
  "first_divergence": { "sample": 48213, "channel": 1,
    "expect": "0x3f2a1c00", "actual": "0x3f2a1c01", "ulp": 1 },
  "diverging_samples": 9182, "max_ulp": 3, "rms_delta_db": -132.4,
  "tier": "v3", "seed": "0x9e3779b97f4a7c15", "build_id": "..." }
```

### Approve-the-diff workflow

1. Regenerate: `offline_render` with the session's pinned seed/tier → `candidate/`.
2. Diff: golden diff tool → `golden_diff_report.json` (above) with per-sample first divergence.
3. Adjudicate: a human or the agent matches the report against the change's DECLARED intent (the T11 row that predicted a golden change). An unpredicted golden diff is a bug until proven otherwise.
4. Approve: the approve tool moves candidate → masters and rewrites BOTH manifests with `approved_by`, `approved_date`, `reason`, new `build_id`.

| RULE | route |
|---|---|
| NEVER auto-approve. A snapshot suite with auto-approval is a change recorder, not a test. [ESTABLISHED: booklet §14.3] | contract-only — reviewed; G3 audit assist: any commit touching `masters/` must also touch `MANIFEST.meta.json` with a nonempty `reason` [OPEN — ASSUMED audit rule] |
| Masters are never hand-edited; only the approve tool writes `masters/`. | contract-only + host-test-catchable (hash gate catches tampering) |
| A tolerance widened to make a test pass is a T11 "kernel optimization" change owing bench + twin evidence, not a quick fix. | contract-only — reviewed |

---

## T5. Property suite

The canon, in yield order. Each row is host-test-catchable on the pure core, per-commit, both legs. [ESTABLISHED: booklet §14.3, §4.4]

| id | property | claim | catches | owner |
|---|---|---|---|---|
| P-PART | **block-partition invariance** (invariant 20) | render a span as ONE call vs any legal partition into smaller calls → byte-equal output | hidden per-callback state: filter reset per callback, ramp restart, meter decaying per call instead of per sample — the classic defect family [ESTABLISHED: booklet §4.4]. The single highest-yield regression net this domain has [ESTABLISHED: booklet §14.3] | reference/dsp_kernel_patterns_manifest.md section K2 |
| P-SIL | silence→silence + state-decay-clean | N blocks of zeros in → zeros out, AND all state fields decay below the denormal floor (no denormal idling) | denormal-range idling (the 2%→40% CPU cliff, booklet §9.6), DC leaks, self-oscillation | K7 |
| P-TAIL | tail decay | impulse, then silence → output below the op's declared floor within its declared time constant | unbounded tails, wrong decay constants, zombie feedback | K1 (the op contract declares the constant) |
| P-FUZZ | full-range parameter fuzz | any seeded random legal parameter trajectory + legal input → no NaN, no Inf, no denormal in output OR state snapshots | parameter-edge blowups, unstable coefficient regions | K3 + K7 |
| P-LIN | linearity where claimed | `render(a·x) == a·render(x)` and superposition, within the op's tolerance, only for ops whose contract claims linearity | nonlinearity leaking into "linear" ops (saturation left enabled, denormal hygiene offsets applied wrongly) | K1 |
| P-TWIN | twin equivalence (invariant 12) | every SIMD tier vs its scalar twin ≤ the pinned tolerance, every tier forced via `--tier`/dispatch override | tier drift — a twin that drifts fails the build, not the listener [ESTABLISHED: booklet §9.7] | K5 |

### Legal cuts for P-PART

The core accepts spans in multiples of its declared block quantum; the shell assembles device periods from core blocks [ESTABLISHED: booklet §4.4]. So P-PART cuts are random quantum multiples; the shell-side assembly of odd periods is proven separately by the port-contract suite (T6) at the shell boundary.

```c
/* SPEC: reference/dsp_kernel_patterns_manifest.md K2
   CONTRACT: output invariant to callback partitioning (invariant 20) */
void prop_partition(const op_api *op, void *state, const float *in, uint32_t n,
                    float *whole, float *parts, test_ctx *c) {
  op->reset(state);
  op->process(state, in, whole, n);                 /* one span            */
  op->reset(state);
  rng_t r = rng_from(c->seed);
  for (uint32_t off = 0; off < n; ) {               /* random legal cuts   */
    uint32_t len = rand_quantum_multiple(&r, n - off);
    op->process(state, in + off, parts + off, len);
    off += len;
  }
  for (uint32_t i = 0; i < n; i++)                  /* byte-compare (T2)   */
    if (f32_bits(whole[i]) != f32_bits(parts[i]))
      fail_audio(c, i, 0u, whole[i], parts[i]);
}
```

### Code shapes and required failure keys

| id | shape | required TESTFAIL keys beyond the always-set |
|---|---|---|
| P-PART | above; also run the WHOLE schedule, not just ops — the composition can hide state the ops don't | SAMPLE, CHANNEL, SEED (cut sequence derives from it), INPUT |
| P-SIL | feed `k` quanta of zeros after a warm-up burst; assert output bits == 0x00000000 and `op->state_scan(state)` reports max |field| below floor | SAMPLE, CHANNEL; `X_STATE_FIELD=` name of the offending state member |
| P-TAIL | unit impulse at sample 0, render `ceil(constant·rate)` + margin; assert RMS of last quantum < floor | `X_RMS_DB=`, `X_FLOOR_DB=`, `X_WINDOW=` |
| P-FUZZ | seeded trajectory generator walks each param across its full legal range with random slews; scan output + state per quantum via the K7 patrol scan | SEED, INPUT (the trajectory file, replayable by T3 as a session script), `X_PARAM=` |
| P-LIN | render x, a·x, x+y separately; compare per T4 tolerance discipline | SAMPLE, CHANNEL, `X_SCALE=` |
| P-TWIN | render same input per tier; compare ulp distance per sample against pinned bound | SAMPLE, CHANNEL, `X_TIER=`, `X_ULP=`, `X_BOUND=` |

State constructibility makes these tractable: a filter mid-decay or a voice mid-release is a value tests build directly, not a state driven to [ESTABLISHED: booklet §14.2].

---

## T6. Port contract suites + fault injection

The partition [ESTABLISHED: booklet §14.2]: **nominal cases run against fake AND real adapters** — the fake earns the word "fake" only by passing the same contract suite as the real adapter; **fault cases run against the fake by construction**. Real-adapter runs are the per-release device-in-loop rung *(target-test-catchable)*; everything else here is *(host-test-catchable)* per commit.

### Fake device scripting interface

Scriptable in exactly the dimensions the real device varies [ESTABLISHED: booklet §14.2]:

| dimension | script control | exercises |
|---|---|---|
| period sequence | fixed N; explicit list; repeating pattern (e.g. 480,480,448,512 — shared-engine jitter shape) | D3/D7 loop pacing, shell block assembly (the T5 P-PART complement) |
| pacing | as-fast-as-possible (render) / real-time-shaped (soak-style host run) | overload timing realism |
| format grants | grant as asked; force downgrade (rate/channels); refuse | D9 negotiation, invariant 19 |
| fault verbs | inject at callback N or sample S: `underrun_recovered`, `device_lost`, `format_invalidated` (D8 verb set) | recovery machines |
| scripted callback cost | ppm-of-period cost the deadline monitor "measures" (via the fake clock) | the degrade ladder without burning CPU [ESTABLISHED: booklet §12.2 — CI drives synthetic overload through the fake clock] |

```c
typedef enum { FK_PERIOD, FK_JITTER_US, FK_FAULT, FK_GRANT, FK_COST_PPM } fk_kind;
typedef struct {
  uint32_t at_callback;   /* applied before the Nth callback           */
  fk_kind  kind;
  int64_t  a, b;          /* kind-specific: frames / us / D8 verb / ppm */
} fk_step;                /* a script = defaults + ordered fk_step[]    */
```

### Fault case matrix (per commit, vs fake)

Every row asserts, in addition to its own column: counters tick (invariant 2/5), events land in the flight ring (O3), the RT plane never blocks or allocates during handling (R2 guards armed), and the user-visible mode is reported, never silent (invariant 14/19). [ESTABLISHED: booklet §14.4]

| case | script | must assert | fix domain |
|---|---|---|---|
| device lost mid-block | `FK_FAULT device_lost` at callback N | adapter converts to the D8 verb; recovery machine runs (D4/D7); output ramps, no click; core state untouched | reference/device_adapter_manifest.md sections D4/D7/D8 |
| format invalidated mid-session | `FK_FAULT format_invalidated` | renegotiation path (D9); stream rebuilt; session continuity per product policy [OPEN — NEEDS-INPUT: continuity policy] | D9 |
| elevation denied at go-live / revoked mid-stream | thread-port fake denies MMCSS/SCHED_FIFO grant | degraded mode entered AND reported (invariant 14); no silent hope; recovery on re-grant | hub H7; booklet §11.1 |
| residency denied | memory-port fake refuses lock | go-live refuses or degrades per M5/M6 policy; never streams unlocked silently [OPEN — NEEDS-INPUT: refuse vs degrade] | reference/memory_residency_manifest.md sections M5/M6 |
| pool exhaustion | event flood generator at max rate | shed policy engages; drops COUNTED (invariant 2); no block, no corruption | M3 |
| disk starvation | streaming-worker port fake delays reads | RT plane reads only what the ring holds (wait-free); starvation is a counted, audible-policy event, not a stall | C2; booklet §6.5 |
| overload ladder walk | `FK_COST_PPM` staircase up then down | every enabled rung engages in order (shed → tier drop → voice steal → bypass → fade-to-silence), stream stays alive at the terminal rung, recovery walks back DOWN in order | booklet §12.2; rung policies are product config *(contract-only, product-recorded)* |
| hysteresis | `FK_COST_PPM` sinusoid straddling a rung threshold | rung transitions bounded (no per-callback flapping); count transitions, assert ≤ scripted expectation | booklet §12.2 |

### State-machine suites

Stream, device, elevation, and ladder machines: transition coverage plus illegal-transition assertions, host-run against the fakes [ESTABLISHED: booklet §14.3]. Each machine's legal-transition table lives with its owner (D-file for stream/device; hub H7 for elevation; booklet §12.2 for the ladder); the suite is generated from that table so the table IS the spec. *(host-test-catchable)*

---

## T7. Concurrency suites

Concurrency failures do not reproduce politely, so they get their own lane [ESTABLISHED: booklet §14.4].

| suite | what | where it runs | route |
|---|---|---|---|
| channel tortures | full/empty boundary races on every ring; swap/retire generation races on the snapshot path; seqlock read-retry storms; mailbox exchange storms — recipes in reference/concurrency_channels_manifest.md section C8, not duplicated here | per-commit under TSan on the **Linux leg only** — TSan runtime is ABSENT on CLANG64 [MEASURED 2026-08-12; hub H5]; plain + ASan/UBSan variants on BOTH legs [MEASURED 2026-08-12: ASan/UBSan link and run on CLANG64] | host-test-catchable |
| shutdown storms | loop: start stream on fakes → random block count → random command traffic → stop mid-traffic; assert join completes within a watchdog deadline (C7 eventcount join, C9 protocol); no leak (LSan, Linux leg), no race (TSan, Linux leg) | both legs; TSan/LSan columns Linux | host-test-catchable |
| dirty-exit harvest | below | both legs | host-test-catchable |

One leg's race detection speaks for both: the code under test is identical (invariant 9) and TSan checks the C11 memory model, not the hardware — the §6.6 discipline is what makes this transfer valid. [ESTABLISHED: booklet §10.8]

### Dirty-exit harvest recipe

Proves invariant 18's "crash and exit preserve the flight ring" without a real crash:

1. Spawn the process under test with `--evidence-dir D` (flight ring backed per O3, heartbeat per O6).
2. Wait for streaming + first heartbeat (poll the heartbeat artifact; no sleeps beyond the poll interval).
3. Hard-kill: `kill -9 <pid>` (Linux) / `taskkill /F /PID <pid>` (Windows) [CC-FACT: OS kill commands] — no cleanup path runs, by design.
4. Relaunch with the same `--evidence-dir`.
5. Assert: harvest artifact produced (E9 mechanics), carrying the PRIOR session's BUILD_ID, its last ring events up to near kill time, and a dirty-exit disposition flag.

Failure output per T2; `INPUT=` names the evidence dir, preserved for the agent. Mechanism owner: reference/error_tracing_contract_manifest.md section E9 + reference/observability_flightring_manifest.md section O3.

### Rules

| RULE | route |
|---|---|
| A TSan finding is not "fixed" until a named C8 torture reproduces it and then passes; a race without a reproducing torture gets one written first. | contract-only — reviewed; the torture then makes it host-test-catchable forever |
| Stress suites bound their duration by op count, not wall time; per-commit budget ~5 s per torture [OPEN — ASSUMED], nightly runs extend iterations, not logic. | host-test-catchable |
| No suite in this section runs on the RT plane of a real device — real-device concurrency evidence comes from the soak rung's always-on monitors (T12). | contract-only |

---

## T8. Sanitizer legs

Availability matrix is a hub fact [VERSION-DEPENDENT - hub H5]. Verified on this machine: ASan links and runs clean on CLANG64; UBSan runs and reports; TSan runtime absent on CLANG64; libFuzzer runtime present [MEASURED 2026-08-12].

### Build flags per lane

| lane | legs | flags (test builds) | tag |
|---|---|---|---|
| ASan | both | `-fsanitize=address -fno-omit-frame-pointer -g -O1` | flags [ESTABLISHED: Clang docs]; runs on CLANG64 [MEASURED 2026-08-12, dynamic runtime in `clang64/bin` on PATH] |
| UBSan | both | `-fsanitize=undefined -fno-sanitize-recover=all -g -O1` — no-recover makes every UB hit a hard CI failure | flags [ESTABLISHED: Clang docs]; runs on CLANG64 [MEASURED 2026-08-12] |
| ASan+UBSan combined | both | `-fsanitize=address,undefined` — one lane where CI minutes are tight | [CC-FACT — combination supported; verify with a smoke target] |
| TSan | Linux only | `-fsanitize=thread -g -O1 -fno-omit-frame-pointer`; NOT combinable with ASan | flags [ESTABLISHED: Clang docs]; CLANG64 absence [MEASURED 2026-08-12; hub H5] |
| LSan (leaks) | Linux only | via ASan lane, `ASAN_OPTIONS=detect_leaks=1` | [CC-FACT — leak detection not available in the MinGW ASan runtime; verify once with `ASAN_OPTIONS=help=1`; hub H5] |

Runtime options: `ASAN_OPTIONS=abort_on_error=1`, `UBSAN_OPTIONS=print_stacktrace=1:halt_on_error=1`, `TSAN_OPTIONS=halt_on_error=1:second_deadlock_stack=1` [CC-FACT — option names from the sanitizer runtimes; enumerate with `<SAN>_OPTIONS=help=1 ./exe`]. Sanitizer lanes rerun the T1 suites; they add no suites of their own.

### UBSan output — teach the parser

Verbatim from this machine [MEASURED 2026-08-12]:

```
p12_ubsan.c:2:34: runtime error: signed integer overflow: 2147483647 + 1 cannot be represented in type 'int'
```

followed by a `SUMMARY:` line [MEASURED 2026-08-12]; summary shape `SUMMARY: UndefinedBehaviorSanitizer: <class> <file>:<line>:<col>` [CC-FACT].

Parse recipe (Windows-drive-colon safe): split the line on the literal `": runtime error: "`; the right side is the description; rsplit the left side on `:` twice to peel column then line; the remainder is the path (which may itself contain `C:`). Do NOT regex `^([^:]+):` — it breaks on drive letters.

### ASan report anatomy

[CC-FACT — shape stable across LLVM releases; confirm against any local run]

```
==<pid>==ERROR: AddressSanitizer: <class> on address 0x... at pc 0x... bp 0x... sp 0x...
<READ|WRITE> of size <n> at 0x... thread T<k>
    #0 0x... in <function> <file>:<line>          <- the access stack (the WHERE)
0x... is located <off> bytes <before|after|inside> <size>-byte region [0x...,0x...)
allocated by thread T<j> here:
    #0 0x... in malloc
    #1 0x... in <function> <file>:<line>          <- the allocation stack (the WHOSE)
[freed by thread T<i> here: ...]                  <- present for use-after-free
SUMMARY: AddressSanitizer: <class> <file>:<line> in <function>
```

Read all stacks before patching: the access stack says where it blew, the allocation (and free) stack says whose memory it was — the patch usually belongs to the second.

### Sanitizer-to-patch routing

| report class | usual root cause here | owning section |
|---|---|---|
| heap-buffer-overflow on an audio bus | frame-count/quantum arithmetic off by one block | reference/dsp_kernel_patterns_manifest.md section K2; scratch sizing M4 |
| use-after-free / use-after-return | generation-handle misuse; snapshot retired while a reader held it | reference/memory_residency_manifest.md section M3; reference/concurrency_channels_manifest.md section C3 |
| stack-buffer-overflow | RT stack budget breach, oversized locals | M7; banned constructs R2 |
| data race (TSan) | ordering idiom deviates from the blessed set | reference/rt_plane_rules_manifest.md section R6; C2–C5 |
| lock-order-inversion (TSan) | control-plane locks during teardown | C9 |
| signed-integer-overflow (UBSan) | sample-position or index math in `int` — positions are `uint64_t`, ring indices wrap unsigned | K1 loop math; C2 index discipline |
| shift/out-of-bounds (UBSan) | dispatch-table or lookup-table indexing | K5; D9 |

Note the false-positive posture: the CRT wraps and startup allocations observed under `--wrap=malloc` [MEASURED 2026-08-12: 3 pre-main hits] mean allocation-tracking assertions must scope to post-init, stream-live windows — the R4 guard machinery owns that scoping.

---

## T9. Fuzzing

Everything that parses bytes it did not write gets a libFuzzer target as part of its definition of done: session files, WAV/media containers, control-protocol frames [ESTABLISHED: booklet §10.8, §14.4]. libFuzzer runtime present on CLANG64 (`libclang_rt.fuzzer*`) [MEASURED 2026-08-12]; presence per leg is a hub row [VERSION-DEPENDENT - hub H5].

### Target shape

```c
/* SPEC: reference/error_tracing_contract_manifest.md E3
   CONTRACT: session parser returns a typed error on any byte input; never crashes */
#include <stddef.h>
#include <stdint.h>
int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
  static arena_t scratch;                 /* reset per iteration, M4 pattern */
  arena_reset(&scratch);
  (void)session_parse(data, size, &scratch);  /* any E3 result is a pass    */
  return 0;                               /* crash/sanitizer hit = finding  */
}
```

Entry point name [ESTABLISHED: LLVM libFuzzer docs]. The harness rule: parse into a per-iteration-reset scratch arena so leak reports attribute to the parser, not the harness.

### Layout and commands

```
test/fuzz/<target>/fuzz_<target>.c    seeds/ (committed)    corpus/ (grown, committed or cached)
```

| action | command | tag |
|---|---|---|
| build | `clang -O1 -g -fsanitize=fuzzer,address,undefined -o fuzz_session test/fuzz/session/fuzz_session.c <parser objs>` | `-fsanitize=fuzzer` [ESTABLISHED: LLVM libFuzzer docs] |
| run (budgeted) | `./fuzz_session seeds corpus -max_total_time=300 -rss_limit_mb=2048 -artifact_prefix=artifacts/fuzz/session/` | flag names [CC-FACT — LLVM libFuzzer docs; `./fuzz_session -help=1` lists them] |
| merge corpus | `./fuzz_session -merge=1 corpus new_inputs` | [CC-FACT — same pointer] |
| minimize a crash | `./fuzz_session -minimize_crash=1 -exact_artifact_path=min.bin -runs=100000 artifacts/fuzz/session/crash-<hash>` | [CC-FACT — same pointer] |

### Crash artifact handling (the law)

1. The crash file (`crash-<hash>`) plus the sanitizer report on stderr IS the failure artifact; CI uploads both.
2. Reproduce: `./fuzz_session crash-<hash>` (single-input mode).
3. Minimize (command above).
4. Commit the minimized input under `test/unit/regressions/` as a table-suite case with id `unit.<parser>.regressions.crash_<shorthash>` and a `SPEC:` pointing at the parser's E3 contract.
5. Fix the parser to return a typed E3 error for that shape. A fuzz finding closed without a committed regression case is not closed. *(host-test-catchable thereafter; the workflow itself: contract-only, reviewed)*

Fuzz targets follow the T2 contract only via their regression cases — the fuzzer's own output format is LLVM's, read per T13.

---

## T10. Bench lane

Protocol, harness shape, warmup/median discipline, and counter selection are owned by reference/optimization_microarch_manifest.md section P2 — this section only wires benches into testing.

- Artifact: `bench_results.json` per run — `{ kernel, test_id, frames, cycles_per_frame_median, mad, tier, build_id, machine_fingerprint (hub H2), baseline_ref }` [blanket tag].
- Gate: compare against the SAME-MACHINE committed baseline; fail on delta beyond the kernel's band (default ±5% [OPEN — ASSUMED; tune per kernel]). The gate refuses a baseline whose machine fingerprint differs — cross-machine absolutes are folklore; gates alarm on regression, absolute truth belongs to the soak rig [ESTABLISHED: booklet §14.5]. *(build-catchable via G4 wiring)*
- Trend: per-merge, whole-schedule renders (cycles per frame, offline) appended to `bench_trend.json` [ESTABLISHED cadence: booklet §14.6].
- Remark tie-in: every bench regression is read NEXT TO the remark-gate output (B8; invariant 15) — a hot kernel that silently de-vectorized is the first hypothesis, and the remark diff confirms or eliminates it in seconds. This machine's healthy reference remark: `vectorized loop (vectorization width: 8, interleaved count: 4)` on a restrict-qualified saxpy at `-O3 -march=x86-64-v3` [MEASURED 2026-08-12: `clang -c -O3 -march=x86-64-v3 -Rpass=loop-vectorize`].

---

## T11. What-a-change-owes

The card-facing law. A change ships with its evidence or does not ship; cards/write-tests.md and cards/review-code.md enforce this table by name. Route for the table itself: *(contract-only — reviewed)*, backed by the named gates *(build/host-test-catchable)* where mechanical.

| change | required tests | required artifacts | gates that must pass |
|---|---|---|---|
| new op / kernel | unit + full table matrix; ALL six T5 properties; tolerance golden for a reference session; P-TWIN if it ships SIMD; fuzz target if it parses foreign bytes | K1 op contract (declared tail constant, tolerances, linearity claim); approved master + manifest entries; `SPEC:` headers | per-commit suite, both legs; remark gate lists it if declared hot (B8) |
| new op / kernel, harmonic-generating (waveshapers, saturators, hard/soft clippers) | everything the "new op / kernel" row requires, plus an aliasing-bound decision (dsp_kernel_patterns K4) | the above, plus — if unmitigated — a documented, reviewed Nyquist-margin exception | same, plus review checks the exception is on file (cards/review-code.md) |
| kernel optimization | T5 re-run; P-TWIN; exact goldens UNCHANGED byte-for-byte, or a T4 approval whose `reason` names this change | before/after `bench_results.json` pair (P2) | bench gate; golden exact; sanitizer lanes |
| new SIMD tier | P-TWIN at the pinned tolerance for the new tier; P-PART forced to the new tier; dispatch test: binds once at init, never per call (invariant 12) | dispatch-table entry; bench justification (booklet §9.7 rung 4: bench, not datasheet) | G4 remark + bench gates |
| channel change | the channel's C8 torture; TSan lane (Linux); shutdown storm; ASan/UBSan lanes | torture recipe entry in C8; R6 idiom citation in the code | TSan clean; sanitizer lanes |
| adapter change | port-contract nominal vs fake AND real; FULL T6 fault matrix vs fake | updated D8 conversion rows; fault script | contract suites; per-release device-in-loop rung scheduled |
| parameter added | P-FUZZ including the new param; K3 consume/ramp property; P-PART re-run (ramps are per-callback-state magnets) | param registry entry; default + range in the op contract | property suite, both legs |
| schedule-compiler change | whole-schedule P-PART; ALL exact goldens; state-machine suites | kernel schema hash bump (B10); replay-compat note (T3 sessions must still load or be migrated) | G6 cross-leg exact golden; G3 structural audits |
| flag canon change | FULL exact-golden matrix both legs; T5 canon; full bench sweep | B2 canon diff; hub row update | everything per-merge runs; treat as toolchain-bump ritual |
| dependency / toolchain bump | everything above it in this table, plus fuzz corpus re-run | hub row move + H9 re-check record | full matrix BEFORE the hub row moves [ESTABLISHED: booklet §14.6] |

An unpredicted golden diff, bench regression, or new sanitizer hit under a change not listed in its row is a stop-the-line finding, not noise.

---

## T12. CI cadences

The ladder, both legs always (invariant 9 — the CI matrix is its proof). Cadences [ESTABLISHED: booklet §14.6]; artifact names blanket-tag; wiring lives in reference/quality_gates_ci_manifest.md section G5 and config/ci-github.yml; `config/check.sh` is the local mirror of the per-commit rung (G2 owns its contract).

| rung | runs | named artifacts |
|---|---|---|
| **per-commit** (both legs, every push) | build at full warning canon (B3); unit + table; property canon; tolerance goldens; same-leg exact goldens; port-contract fake nominal + fault; state-machine; short channel stress; ASan + UBSan lanes; TSan stress lane (Linux); remark gates (B8); fuzz smoke (60 s/target [OPEN — ASSUMED budget]); bench compare | `artifacts/<leg>/test_report.json` (aggregated TESTFAIL blocks + counts), `artifacts/<leg>/san_asan.log`, `san_ubsan.log`, `artifacts/linux/tsan_stress.log`, `artifacts/<leg>/remark_gate.json`, `artifacts/<leg>/bench_results.json` |
| **per-merge** | cross-leg exact golden handshake (G6); whole-schedule bench trend; structural audits (G3: `config/audit_includes.py`, `config/audit_symbols.py`); fuzz budget run + corpus merge | `artifacts/cross/golden_exact_report.json`, `artifacts/cross/bench_trend.json`, `artifacts/<leg>/audit_report.json`, `artifacts/fuzz/**` |
| **per-release** (target rungs: real machines of the reference class, real devices, both OSes) | soak — hours-long real-device runs at the shipped period matrix, always-on monitors as witness, gating the invariant-6 headroom floor (worst callback ≤ 50% of period); buffer sweep regenerating the invariant-16 robustness curve; loopback latency vs the §7.3 computed sum; device-matrix smoke; real-adapter contract suites | `artifacts/release/soak_session_report.json` (E8 schema — the release notes cite it), `robustness_curve.json`, `loopback_latency.json`, `device_matrix_smoke.json` |

| RULE | route |
|---|---|
| A release that skips a rung names the skip in its notes — a skipped rung is a risk decision, not an oversight. [ESTABLISHED: booklet §14.6] | contract-only — release checklist |
| Toolchain-bump ritual: a new clang major or OS baseline re-runs everything above plus the full golden-exact matrix BEFORE the hub row moves. [ESTABLISHED: booklet §14.6] | build-catchable — hub H9 re-check triggers; G1 ledger row |
| Every CI artifact above embeds BUILD_ID (invariant 17); an artifact without one is rejected by the gate that consumes it. | build-catchable — G2/G4 |

---

## T13. Reading failure artifacts

The diagnose-failure card's backend (cards/diagnose-failure.md routes here). For each artifact type: what it looks like, what it tells you, your first three moves, and which reference section owns the fix domain. Every type ends in a named owner — meet one that doesn't, and that is a defect in this file.

### Unit / table failure (TESTFAIL block)

- **Looks like:** the T2 block on stdout; runner reports the exe nonzero.
- **Tells you:** the contract, its owning spec section, exact expected/actual.
- **Moves:** (1) parse the block — `SPEC=` is the contract's home; (2) open that section and the module source side by side; (3) rerun just it: `ctest -R '^<test_id>$' --output-on-failure` on the SAME leg the failure came from.
- **Owner:** whatever `SPEC=` names — that is the point of T2-2.

### Property failure (seeded)

- **Looks like:** TESTFAIL block with `SEED=` and `INPUT=` (repro bundle under `_artifacts/`).
- **Tells you:** which property broke and the first diverging sample.
- **Moves:** (1) rerun with the printed seed — non-reproduction is itself a finding (unseeded randomness, T2-5 violation); (2) classify by property id: P-PART → hidden per-callback state (the §4.4 family: reset-per-callback, ramp restart, meter decay per call) — owner K2; P-SIL/P-FUZZ NaN/denormal → K7; P-TWIN → K5; (3) shrink: replay the `INPUT` trajectory through `offline_render` and bisect the span/cut list.
- **Owner:** per property row in T5.

### Golden diff report (`golden_diff/v1` JSON)

- **Looks like:** the T4 JSON — regime, first divergence with bits, `max_ulp`, `rms_delta_db`.
- **Tells you:** exact regime → a toolchain-or-discipline regression BY DEFINITION [ESTABLISHED: booklet §14.3]; tolerance regime → kernel drift beyond contract.
- **Moves:** (1) exact: diff `BUILD_ID` (flag fingerprint!) between legs/against the master's meta — a contraction or tier drift is the usual killer (B2, K6 preconditions); (2) confirm tier + no-libm preconditions held (`meta.tier`, symbol audit); (3) if preconditions held, bisect commits with same-leg regeneration; approve ONLY with a T11 row that predicted the change.
- **Owner:** K6 (FP regime) / B2 (flags) / G6 (gate mechanics).

### TSan report (Linux lane)

- **Looks like:** `WARNING: ThreadSanitizer: data race (pid=...)`, then two stacks — `Read of size 4 at 0x... by thread T1:` / `Previous write of size 4 ... by main thread:` — then the location of the object, then `SUMMARY: ThreadSanitizer: data race <file>:<line>` [CC-FACT — shape; confirm on any local run].
- **Tells you:** both racing access sites and the object; that the C11 model is violated regardless of whether the hardware would have punished it [ESTABLISHED: booklet §10.8].
- **Moves:** (1) map both stacks to the channel primitive (C2–C5) and the object; (2) diff the code against the R6 blessed ordering idioms — the fix is almost always "use the idiom", not "add a fence"; (3) write or extend the C8 torture until it reproduces, then patch (T7 rule).
- **Owner:** reference/concurrency_channels_manifest.md sections C2–C5; reference/rt_plane_rules_manifest.md section R6.

### ASan report

- **Looks like:** the T8 anatomy — error class, access stack, region relation line, allocation (and free) stack, SUMMARY.
- **Tells you:** where it blew AND whose memory it was.
- **Moves:** (1) classify the error class via the T8 routing table; (2) read the allocation stack and map it to an M1 allocation class — arena (M2), pool/generation (M3), scratch (M4), stack (M7); (3) if the region is an audio bus, check quantum/frame math first (K2).
- **Owner:** reference/memory_residency_manifest.md; K2 for bus arithmetic.

### UBSan line

- **Looks like:** `p12_ubsan.c:2:34: runtime error: signed integer overflow: 2147483647 + 1 cannot be represented in type 'int'` + SUMMARY [MEASURED 2026-08-12].
- **Tells you:** exact file:line:col and the UB class — parse per the T8 recipe (split on `": runtime error: "`, drive-colon safe).
- **Moves:** (1) open the location; (2) apply the class fix from the T8 routing table (positions to `uint64_t`, ring indices unsigned-wrap, table indexing bounds); (3) add a unit regression with the exact triggering values from the message.
- **Owner:** per the T8 routing table row.

### Bench regression JSON

- **Looks like:** `bench_results.json` with `delta_pct` beyond band, plus the gate's refusal line.
- **Tells you:** cost regressed; correctness said nothing.
- **Moves:** (1) read the remark-gate diff first — de-vectorization is hypothesis #1 (invariant 15; B8); (2) rerun on the pinned machine per P2 to exclude thermal/power noise; (3) `llvm-mca -mcpu=alderlake` before/after on the kernel's `-S` output [MEASURED 2026-08-12: works on this machine, reports Dispatch Width: 6] and consult the P7 stall table.
- **Owner:** reference/optimization_microarch_manifest.md sections P2/P3/P7.

### Fuzz crash

- **Looks like:** `crash-<hash>` file under `artifact_prefix`, sanitizer report on stderr, libFuzzer's final `DEDUP_TOKEN`/stack lines [CC-FACT — shape].
- **Tells you:** a byte pattern that crashes a parser that must never crash.
- **Moves:** (1) reproduce single-input: `./fuzz_<target> crash-<hash>`; (2) minimize (T9 command); (3) commit the regression case and fix the parser to return a typed E3 error.
- **Owner:** the parser's module; contract in reference/error_tracing_contract_manifest.md section E3.

### CI gate log

- **Looks like:** one `GATE=<id> STATUS=FAIL DETAIL=<one line>` per failed gate (G2's check.sh contract), with the gate's artifact attached.
- **Tells you:** which ledger row refused the change.
- **Moves:** (1) look the gate id up in the G1 ledger — it names its owning section and its artifact; (2) reproduce locally: `config/check.sh` (the per-commit mirror; per-gate invocation per G2); (3) fix in the owning section's domain, never by editing the gate.
- **Owner:** reference/quality_gates_ci_manifest.md sections G1/G2.

### The escalation rule

If an artifact resists all three moves, capture don't thrash: bundle the artifact + `BUILD_ID` + repro command into `_work/` and re-read the owning section top to bottom — the failure is usually a violated precondition of a neighboring contract, and the section's own rules table names it. *(contract-only — this is the agent's working discipline)*
