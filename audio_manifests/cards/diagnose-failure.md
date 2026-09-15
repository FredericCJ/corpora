# Card: diagnose a red artifact

**Load when:** any artifact is red — a failed unit or property test, a golden diff, a sanitizer
report, a bench regression, an xrun, a session-report anomaly, a guard trip, a crash dump, a CI gate.
**Depth:** every dispatch row below names its owning reference section. The loop and the evidence
chain: `reference/error_tracing_contract_manifest.md` sections E1, E7. Reading failure artifacts:
`reference/testing_verification_manifest.md` section T13. Designing the error side:
`cards/handle-errors.md`. The instruments themselves: `cards/observability.md`.

Facts verified 2026-08-12. Version-dependent claims route to
`reference/audio_platform_baseline_manifest.md` (the hub); if any file disagrees with the hub, the
hub wins. Reasoning root: the child booklet `realtime-audio-pc-architecture-and-design-r1.md`
(repo root) — operationalized here, never re-argued.

## The failure-to-patch loop

The doctrine this package exists for, stated once (normative:
`reference/error_tracing_contract_manifest.md` section E1): every failure artifact is
machine-readable and **self-locating** — it names WHAT failed, WHERE, and WHY, with enough context
to patch. The loop:

**READ** the artifact's fields — not the code, not yet → **LOCATE** via the self-locating fields
(file:line, registry code, seed, build identity) → **ATTRIBUTE** to a defect class via the dispatch
table → **PATCH** at the owning layer → **PROVE** by rerunning the named gate → **RECORD** what the
change owes (`reference/testing_verification_manifest.md` section T11).

Two laws, absolute:

- **Never patch without reading the artifact's fields first.** A patch made from the symptom
  instead of the fields fixes the wrong layer; the fields exist so you do not guess.
  *(contract-only — this card is the register entry)* [ESTABLISHED: booklet section 13.1,
  postmortem-first, operationalized]
- **Never mark fixed without rerunning the named gate.** The gate column below *is* the definition
  of "fixed"; a fix without its gate rerun is a hypothesis. *(host/target-test-catchable — the gate
  itself is the enforcer)*

Corollary: **an artifact that could not locate its own fault is a second defect.** Patch the
evidence gap — the missing field, counter, or event — alongside the fault. [ESTABLISHED: booklet
section 2.4 — "an xrun with no witness … a lie the system tells its own recorder"]

## The dispatch table

Route on artifact type, never on hunch. Owning-section and gate columns are the ATTRIBUTE and PROVE
steps. [Table rows derive from booklet ch. 12–15 and the dictated package map; per-row tags inline.]

| artifact | what it tells you — read these fields first | first three moves | owning reference | the gate that proves the fix |
|---|---|---|---|---|
| **unit fail** | TESTFAIL v1 block (anatomy below): `TEST_ID=`, `SPEC=` (the section owning the contract), `CONTRACT=`, `EXPECT=`/`ACTUAL=` with bit patterns, `BUILD_ID=` | 1) reproduce by exact `TEST_ID=`; 2) open the `SPEC=` section — it owns the contract under test; 3) read the `EXPECT=`/`ACTUAL=` delta (bits included) and decide wrong-code vs wrong-test vs stale-master before editing either | `reference/testing_verification_manifest.md` sections T2, T13 | the named test green, then its full lane via `config/check.sh` |
| **property fail** | TESTFAIL block with `SEED=`, `INPUT=` (kept artifact under `test/*/_artifacts/<test_id>/`), `SAMPLE=`/`CHANNEL=` of first divergence | 1) rerun with the printed `SEED=` — the core is deterministic, it MUST reproduce, and non-reproduction is its own finding [ESTABLISHED: booklet section 14.1; rule T2-5]; 2) read the kept `INPUT=` artifact, not the original session; 3) if it is the block-partition property, hunt hidden per-callback state (invariant 20) | `reference/testing_verification_manifest.md` section T5; `reference/dsp_kernel_patterns_manifest.md` section K2 | same-seed rerun green, then the full-seed property lane |
| **golden diff** | `TEST_ID=` (suite `golden.*`, case `exact` \| `tol`), first divergence as `SAMPLE=`/`CHANNEL=` with decimal AND bit pattern, `BUILD_ID=` per leg | 1) regime first: **exact** regime diff = determinism regression (flags, libm creep, FP regime) by definition [ESTABLISHED: booklet section 14.3] — not a numeric judgment call; 2) diff the two builds' flag fingerprints / build identity; 3) tolerance regime: compare against the oracle at the *contracted* tolerance before touching the master | `reference/testing_verification_manifest.md` section T4; `reference/toolchain_build_manifest.md` sections B2, B8; `reference/dsp_kernel_patterns_manifest.md` section K6 | golden suite green; exact regime: the cross-leg gate, `reference/quality_gates_ci_manifest.md` section G6 |
| **ASan report** | error kind (`heap-use-after-free`, `heap-buffer-overflow`, …), access address+size, three stacks: access, allocation, free [CC-FACT: ASan report anatomy] | 1) read all three stacks before any code; 2) map the address to its allocation class — which arena/pool/slot (`M1`); 3) if pooled: check generation-handle discipline (`M3`) | `reference/memory_residency_manifest.md` sections M1, M3; `reference/testing_verification_manifest.md` section T8 | ASan lane green, both legs [MEASURED 2026-08-12: ASan links and runs clean on CLANG64] |
| **UBSan line** | `file:line:col`, category, operand values (anatomy below) | 1) open the exact `file:line:col`; 2) decide whether the arithmetic contract or the code is wrong; 3) fix the contract or the type — never mask with a cast | `reference/testing_verification_manifest.md` section T8 | UBSan lane green |
| **TSan report** (Linux leg only [MEASURED 2026-08-12: no TSan runtime in CLANG64 clang libs]) | race kind, address, two stack pairs with thread names/planes, locks held | 1) name both threads' planes and the channel between them; 2) check the accesses against the four blessed ordering idioms (`R6`); 3) write or repair the happens-before argument — never "fix" with seq_cst or a lock | `reference/concurrency_channels_manifest.md` section C8; `reference/rt_plane_rules_manifest.md` section R6 | TSan torture lane green (Linux), plus the happens-before note in review *(contract-only half)* |
| **bench regression** | kernel id, baseline vs current distribution (min/median/p99/max cycles-per-frame), machine identity, frequency-policy label, cache state | 1) environment parity check — different machine, governor label, or SMT state means *measurement*, not regression [ESTABLISHED: booklet section 10.6]; 2) rerun at protocol N; 3) attribute: remarks diff (de-vectorization?) then `llvm-mca` delta on the kernel | `reference/optimization_microarch_manifest.md` sections P2, P3, P7 | bench gate back inside its band (`reference/quality_gates_ci_manifest.md` section G4) AND remark gate still green |
| **xrun autopsy** | class counters: wakeup-gap vs duration split, minor/major faults, involuntary context switches, ring events around the xrun | 1) classify by signature [ESTABLISHED: booklet sections 2.4, 11.5]: gap grew = late wakeup; faults/involuntary switches mid-work = external stall; duration grew + quiet counters = self-overrun; stream fault = device-side; 2) route by class: self → `cards/optimize-performance.md`; late wakeup → `reference/optimization_microarch_manifest.md` section P9; external → `reference/memory_residency_manifest.md` sections M5/M6 or deployment rows; device → `reference/device_adapter_manifest.md` section D4; 3) confirm with a diagnosis-mode capture before shipping the fix | `reference/observability_flightring_manifest.md` section O9; `reference/device_adapter_manifest.md` section D4 | soak rung: no recurrence at the same period, headroom floor held (invariant 6) |
| **session report anomaly** | schema-versioned fields: output-sentinel interventions, xrun counters by class, degrade-rung history, per-ring drop counters, histogram tail | 1) sentinel > 0 is a filed bug upstream **by definition** [ESTABLISHED: booklet section 12.5] — never tune the sentinel; 2) correlate the counter spike to event-stream timestamps; 3) replay: recorded command ring + events reproduce the session offline, bit-exactly [ESTABLISHED: booklet section 13.3] | `reference/observability_flightring_manifest.md` section O7; `reference/error_tracing_contract_manifest.md` section E8 | the replay-derived regression test green, counter zero on scenario rerun |
| **guard trip** | callsite, banned family (alloc / lock / wait / syscall), thread name + plane, flight-ring context | 1) read the callsite: direct spelling (a poison gap — should not have compiled) vs indirect arrival (function pointer, third-party — the interposition net's catch) [ESTABLISHED: booklet section 15.2]; 2) move the operation across the plane boundary or pre-claim the resource (`R2` names the replacement per row); 3) third-party code on the RT plane: shrink that surface — a call whose implementation you cannot name is blocking until proven otherwise [ESTABLISHED: booklet section 11.4] | `reference/rt_plane_rules_manifest.md` sections R2, R4 | guard-armed test lane clean rerun |
| **crash dump** | build identity stamp, crash event, flight-ring region (in the dump by construction), faulting stack | 1) resolve symbols from the archived debug artifacts matching the build id [ESTABLISHED: booklet section 10.4]; 2) harvest: next start's dirty-exit path emits the prior ring tail and counters as its first events [ESTABLISHED: booklet section 13.4]; 3) read the last events before death — the story is in the ring, not the stack alone | `reference/error_tracing_contract_manifest.md` section E9; `reference/observability_flightring_manifest.md` section O3 | dirty-exit-harvest test green, plus the fix's own named gate from this table |
| **CI gate fail** | gate id (ledger row), leg, exit code, artifact path | 1) open the gate's own artifact — every gate emits one (`G2` contract); 2) route that artifact's type back through THIS table; 3) never rerun-to-green without a recorded cause — a flake is its own defect class with a quarantine decision [OPEN: flake policy — NEEDS-INPUT] | `reference/quality_gates_ci_manifest.md` sections G1, G2 | the same gate id green on the same leg |

## The three machine formats, parsed

### 1. CHECK-FAIL line (format v1) — one line per check failure

```
CHECK-FAIL id=<REGISTRY_NAME> file=<repo-relative> line=<n> expr="<predicate>" expected="<x>" actual="<y>" ctx=<k1=v1,k2=v2,k3=v3> build=<git-short[-dirty]>
```

Example:

```
CHECK-FAIL id=MEM_HANDLE_STALE file=core/pool.c line=142 expr="handle_gen(h)==pool_gen(p,h)" expected="7" actual="9" ctx=pool=voices,slot=13,block=88412 build=8c1f22e
```

Field roles: WHAT = `id` (an E3 registry symbol — grep it for the owning module and its reference
section) plus `expr`/`expected`/`actual`; WHERE = `file`/`line`, repo-relative; WHY-context =
`ctx` (up to three `key=val` pairs) and `build` (must equal the session report's build id). The
marker and field order are **frozen v1** — any change ships under a new marker, never a silent
field change — and RT-plane checks never format: they emit a binary ring event the control-plane
drain renders into this identical line. [ESTABLISHED:
`reference/error_tracing_contract_manifest.md` section E6, rules E6-1/E6-2 — the normative
grammar and parse regex live there]

### 2. UBSan runtime line — measured on this toolchain

```
p12_ubsan.c:2:34: runtime error: signed integer overflow: 2147483647 + 1 cannot be represented in type int
SUMMARY: UndefinedBehaviorSanitizer: ...
```

[MEASURED 2026-08-12: CLANG64 clang 22.1.8, `-fsanitize=undefined`; a `SUMMARY:` line naming the
same location follows the report.] Parse: `<file>:<line>:<col>: runtime error: <category>:
<operands and why>`. The column number is exact — it points at the *operator*, not the statement.
[CC-FACT: column semantics]

### 3. TESTFAIL v1 block — one per failing test, sentinel-delimited

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

Parse rules: one `KEY=value` per line, split at the FIRST `=`; fixed key set, extensions prefixed
`X_`; audio diffs report the FIRST divergence in decimal AND bit pattern (ulp math needs bits);
`SEED=` is mandatory on randomized kinds and rerunning with it must reproduce; `INPUT=` artifacts
are kept on failure, deleted on pass; pass output is exactly `OK <test_id>`. [ESTABLISHED:
`reference/testing_verification_manifest.md` section T2 — normative grammar, the `test_id`
scheme, and the emitting helper's contract live there]

## When the artifact is not enough

1. **Arm diagnosis mode** (`reference/observability_flightring_manifest.md` section O9) — free on
   the RT plane when off, adds per-callback fault/switch/gap deltas and off-plane tracer
   correlation (ETW / perf) when on [ESTABLISHED: booklet section 11.5].
2. **Replay it**: command-ring recording + deterministic core = the session re-rendered offline at
   file-write speed [ESTABLISHED: booklet section 13.3]. A field glitch becomes a regression test
   as workflow, not heroics.
3. **Then file the evidence gap** — the field or counter that would have made steps 1–2
   unnecessary. That patch is owed with the fix (What you owe, below).

## Never

- Patch code and test in the same motion to make red go green — decide which is wrong first.
  *(contract-only, review)*
- Re-approve a golden master to silence a diff — approval without a first-divergence analysis
  turns the suite into a change recorder [ESTABLISHED: booklet section 14.3]. *(contract-only;
  the approve-the-diff rule is the register entry)*
- Rerun a flaky lane until green with no recorded cause. *(contract-only — flake register)*
- Compare bench numbers across machines or frequency-policy labels as if same-machine.
  *(build-catchable — the bench artifact carries the machine identity, the gate refuses
  mismatches)*
- "Fix" a race with `memory_order_seq_cst` or a new lock on the RT plane — route to the blessed
  idioms (`reference/rt_plane_rules_manifest.md` section R6). *(analysis + host-test-catchable)*
- Suppress a sanitizer finding without a dated deviation record. *(contract-only, review)*
- Delete or overwrite the failing artifact before it is harvested into the fix's record.
  *(contract-only)*

## What you owe

A closed diagnosis carries: the artifact fields you read (quoted), the attribution (dispatch row +
owning section), the patch, the named gate rerun green (command + result), and — where the
artifact under-located the fault — the evidence-gap patch. That bundle is what
`reference/testing_verification_manifest.md` section T11 collects; without the gate rerun it is
not a fix, it is a diff.

## Decisions you must not invent

Flake quarantine policy and who may invoke it · golden-master diff approval authority · the
product's xrun SLO (misses/day at stated period — booklet section 2.3 makes it a product pin) ·
whether diagnosis mode may be enabled at a user site · crash-dump and session-report upload
consent · deviation-record acceptance authority.

## Go deeper

| question | where |
|---|---|
| worked failure-to-patch examples, end to end | `reference/error_tracing_contract_manifest.md` section E10 |
| the evidence chain: artifact → code → gate | `reference/error_tracing_contract_manifest.md` section E7 |
| reading each artifact type, full walkthroughs | `reference/testing_verification_manifest.md` section T13 |
| xrun classification machinery, diagnosis mode | `reference/observability_flightring_manifest.md` section O9 |
| the stall/flush diagnostic table (tail chasing) | `reference/optimization_microarch_manifest.md` section P7 |
| device fault verbs and recovery protocols | `reference/device_adapter_manifest.md` sections D4, D8 |
| crash capture and the dirty-exit harvest | `reference/error_tracing_contract_manifest.md` section E9 |
| session report fields | `config/session_report.schema.json` + `reference/error_tracing_contract_manifest.md` section E8 |
