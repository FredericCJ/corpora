# Card: write tests

**A failing test must tell the agent WHAT failed, WHERE, and WHY, with machine-readable context to patch — the failure artifact is the feedback loop.**

Facts verified 2026-08-12. Version-dependent claims route to reference/audio_platform_baseline_manifest.md (the hub); if any file disagrees with the hub, the hub wins.
Reasoning root: the child booklet `realtime-audio-pc-architecture-and-design-r1.md` (repo root). This card operationalizes it; it never re-argues it.

**Load when:** writing tests, deciding which suites a change owes, adding or updating golden masters, scripting the fake device.
**Depth:** reference/testing_verification_manifest.md. Reading a failure you did not write: cards/diagnose-failure.md. Gate wiring: cards/gates-and-ci.md.

## The standard this card serves

**The entire signal engine runs headless, deterministic, and faster than real time on any dev or CI box — no device, no privileges, no kernel in the loop** [ESTABLISHED: booklet section 14.1]. Host tests are therefore cheap; the only expensive rungs are the release-time target rungs, and nothing on this card needs them.

## Suite selection by change type (T11 condensed)

| you changed | you owe |
|---|---|
| a kernel / DSP op | twin equivalence at pinned tolerance; golden (exact regime, both legs, if pinned path; tolerance regime otherwise); property canon incl. partition invariance; boundary-table row; bench before/after if perf-relevant; remark-gate entry if hot [ESTABLISHED: booklet sections 14.3, 14.5] |
| RT-plane code | guard-clean dev-build suite run; boundedness argument filed (reference/rt_plane_rules_manifest.md section R8); ASan+UBSan legs [ESTABLISHED: booklet sections 15.2, 10.8] |
| a channel | contract suite + torture on the Linux TSan lane; drop/high-water counters asserted [ESTABLISHED: booklet section 14.4] |
| adapter / device code | port contract suite against fake (and real where available); fault-injection rows per verb touched [ESTABLISHED: booklet sections 14.2, 14.4] |
| an error path | fault injection proving the disposition and the evidence chain end-to-end (event marked, counted, report row present) [ESTABLISHED: booklet section 12.1] |
| a parser of foreign bytes (session, media, control frames) | a libFuzzer target as part of the definition of done — runtime present on both legs [MEASURED 2026-08-12: libclang_rt.fuzzer* present on CLANG64] [ESTABLISHED: booklet section 10.8] |
| composition root / shutdown | root-order test on the fakes; shutdown-storm coverage [ESTABLISHED: booklet sections 4.5, 14.4] |
| flags / toolchain | see cards/build-and-flags.md — remark gates, bench, goldens re-run |

## Test ids and self-location (T2 condensed)

Test ids are stable, hierarchical, grep-able: `<suite>.<unit>.<case>` — the id is the cross-reference key between CI logs, session reports, and the registry. The failure output REQUIREMENTS — every failing test MUST emit, machine-readable:

1. the **test id** (stable across renames of prose, never reused);
2. **file:line** of the assertion that fired;
3. **expected vs actual as values**, not prose — first differing frame/field, both values, in a parseable form;
4. the **contract violated** — invariant number, property name, or registry code;
5. the **exact reproduction command**, copy-paste runnable;
6. the **seed/parameters** for any generated or fuzzed case;
7. the **build identity** — revision, leg, configuration, flag fingerprint [ESTABLISHED: booklet ch. 3 invariant 17];
8. **artifact paths** where produced — golden diff, ring dump, sanitizer log.

[OPEN ASSUMED: this list restates the doctrine; the normative wording is reference/testing_verification_manifest.md section T2 — if wording differs, T2 wins.] A conforming failure, for shape (T2's own literal example):

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

## Golden masters (T4 condensed)

Two regimes [ESTABLISHED: booklet section 14.3]:

- **exact** — bit-identical output; per commit on each leg, per merge cross-leg (one leg renders, the other byte-compares); applies to the pinned-kernel path, where the FP regime makes cross-OS bit-equality a test and its failure a toolchain-or-discipline regression by definition;
- **tolerance** — ULP- or dB-floor-bounded; for the legitimately variant: SIMD tier vs scalar twin, approximation kernels vs high-precision oracles, cross-tier dispatch.

Workflow: generate with the offline renderer (`tools/`), commit the master as an **approved artifact**; on intentional change, regenerate → review the diff → approve with the reason in the commit. A snapshot suite with auto-approval is a change recorder, not a test [ESTABLISHED: booklet section 14.3]. Master provenance carries the build identity of the generator run.

## Property canon (T5 condensed)

On the pure core, per op and whole-schedule [ESTABLISHED: booklet section 14.3]:

| property | catches |
|---|---|
| silence in → silence out, **state decaying clean** (denormal patrol on state) | idle-cost cliffs, dirty tails |
| bounded in → bounded out (sentinel-guarded bus) | blowups the sentinel would otherwise absorb silently |
| tail decay below floor within the op's declared constant | wrong decay constants, stuck state |
| no NaN/denormal from any legal input under full-range parameter fuzz | the permanent-and-spreading NaN class |
| linearity where the op claims it | accidental nonlinearity |
| **partition invariance** (invariant 20): one span vs every interesting partition, byte-compared | hidden per-callback state — the highest-yield net this domain has |

Plus boundary tables (parameter extremes, denormal-adjacent, DC, full-scale, every supported rate) and state-machine suites with illegal-transition assertions [ESTABLISHED: booklet section 14.3].

## Fake-device scripting (T3/T6 condensed)

The fake is scriptable in exactly the dimensions the real device varies [ESTABLISHED: booklet section 14.2]:

| dimension | script |
|---|---|
| period sequences | fixed; alternating; legal shared-mode jitter |
| format grants | grant-as-requested; downgrade; refusal |
| fault verbs | inject `underrun-recovered` / `device-lost` / `format-invalidated` at a chosen block |
| pacing | as-fast-as-possible (rendering) or real-time-shaped (soak-style host runs) |

The fake earns the word "fake" by passing the same contract suite as the real adapter [ESTABLISHED: booklet section 14.2]. The fake clock synthesizes drift/jitter to order — the only way to test a ppm-scale estimator in milliseconds.

## Sanitizer and race lanes

ASan+UBSan wrap the host suites per commit on both legs [MEASURED 2026-08-12: ASan links and runs clean on CLANG64; UBSan reports `file:line: runtime error: ...` plus a SUMMARY line — already self-locating]. TSan is **Linux-lane only** [MEASURED 2026-08-12: runtime absent on CLANG64]; the C11-model discipline makes one leg's detection speak for both [ESTABLISHED: booklet section 10.8].

## Never

- Auto-approve golden updates (route: contract-only, review) [ESTABLISHED: booklet section 14.3].
- Write a naked `assert(x)` in a test — no expected/actual values means a non-conforming failure artifact (route: analysis-catchable in test lint; contract-only in review).
- Sleep-based synchronization or wall-clock timing assumptions in host suites — the suites are deterministic by construction [ESTABLISHED: booklet section 14.1].
- Mark a one-leg failure "flaky" — a test that passes on one leg only is a broken build [ESTABLISHED: booklet ch. 3 invariant 9].
- Touch a real device in per-commit suites; real devices belong to the release rungs [ESTABLISHED: booklet section 14.6].
- Skip partition invariance for any stateful op.
- Reuse a test id, or let an id drift from its registry references.
- Regenerate a master in the same change as the logic edit without a reviewed diff and a stated reason.

## Decisions you must not invent

- Tolerance values per kernel (twin, oracle, cross-tier) — [OPEN NEEDS-INPUT; each kernel's contract pins its own].
- Golden corpus contents (which sessions, which parameter sweeps) — [OPEN NEEDS-INPUT; also the PGO workload, booklet section 10.5].
- Bench tolerance bands and baseline machines — [OPEN NEEDS-INPUT; reference/testing_verification_manifest.md section T10].
- Continuous fuzz budget — [OPEN ASSUMED: whatever CI affords, per booklet section 10.8].
- The release-rung device matrix — [OPEN NEEDS-INPUT; hub-enumerated per deployment].

## What you owe when done

This card *is* the owing side of the loop: reference/testing_verification_manifest.md section T11 defines what each change type owes, and this card's tables are its condensation — when in doubt, T11 wins. Every owed suite runs green on both legs through config/check.sh; the gate ledger reference/quality_gates_ci_manifest.md section G1 records which gate proves which invariant; new failure modes get registry codes (reference/error_tracing_contract_manifest.md section E3) so the next failure self-locates. A change whose tests cannot fail informatively has not been tested — it has been decorated.

## Go deeper

| question | where |
|---|---|
| test topology and cadences | reference/testing_verification_manifest.md sections T1, T12 |
| naming + self-location contract, normative | reference/testing_verification_manifest.md section T2 |
| offline renderer harness | reference/testing_verification_manifest.md section T3 |
| goldens / properties / port suites | reference/testing_verification_manifest.md sections T4, T5, T6 |
| concurrency suites | reference/testing_verification_manifest.md section T7 |
| sanitizer legs + fuzzing | reference/testing_verification_manifest.md sections T8, T9 |
| bench lane | reference/testing_verification_manifest.md section T10 |
| what a change owes, normative | reference/testing_verification_manifest.md section T11 |
| reading failure artifacts | reference/testing_verification_manifest.md section T13 |
| session report schema | reference/error_tracing_contract_manifest.md section E8; config/session_report.schema.json |
