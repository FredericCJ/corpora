# Card: gates and CI

**Load when:** wiring CI, adding or changing a gate, deciding what blocks a merge, preparing a
release, or bumping the toolchain.
**Depth:** `reference/quality_gates_ci_manifest.md` (G1–G9). Test content: `cards/write-tests.md`.
Reading a red gate: `cards/diagnose-failure.md`. Build mechanics:
`reference/toolchain_build_manifest.md`.

Facts verified 2026-08-12. Version-dependent claims route to
`reference/audio_platform_baseline_manifest.md` (the hub); if any file disagrees with the hub, the
hub wins. Reasoning root: the child booklet `realtime-audio-pc-architecture-and-design-r1.md`
(repo root) — operationalized here, never re-argued.

## The law

**A rule with no enforcer is a preference.** [ESTABLISHED: booklet ch. 3, the meta-invariant]
Every gate here is a versioned script that runs identically locally and in CI, fails the build,
and **emits a machine-readable, self-locating artifact** — the artifact is what
`cards/diagnose-failure.md` dispatches on; a gate that only says "red" is half a gate.

## The gate ledger, condensed

Normative ledger: `reference/quality_gates_ci_manifest.md` section G1. [Cadence rows derive from
booklet sections 14.6, 15.3; per-leg availability facts tagged inline.]

| cadence | gates (both legs unless noted) | blocking |
|---|---|---|
| **per commit** | build at the full warning canon, `-Werror` · unit + property + table + tolerance-golden suites · fault-injection suites on the fakes · ASan + UBSan lanes [MEASURED 2026-08-12: both link and run on CLANG64] · TSan stress lane — **Linux leg only** [MEASURED 2026-08-12: no TSan runtime on CLANG64] · vectorization-remark gates · bench vs same-machine baseline · quick structural audits | yes |
| **per merge** | cross-leg **exact** golden gate (G6): one leg renders, the other byte-compares — the determinism contract enforced [ESTABLISHED: booklet section 14.6] · whole-schedule bench trends · include / symbol / map audits (`config/audit_includes.py`, `config/audit_symbols.py`; G3) · conditional-inclusion audit | yes |
| **per release** (target rungs, real reference-class machines, both OSes) | soak at the shipped period matrix gating invariant 6's headroom floor · buffer sweep regenerating the xrun-vs-period robustness curve (invariant 16) · loopback latency vs the computed sum · device-matrix smoke | yes for release; a skipped rung is named in the release notes — a risk decision, not an oversight [ESTABLISHED: booklet section 14.6] |
| **toolchain bump** | everything above **plus** the full golden-exact matrix, re-run BEFORE the hub row advances | yes — the platform ships inside every binary |

## check.sh — one entry point

`config/check.sh` is the local spine: the same command CI runs, lane-selectable, exit code = gate
verdict, artifacts under the per-gate paths the contract names. Lane vocabulary and flags are
normative in the script's own help and `reference/quality_gates_ci_manifest.md` section G2 — do
not invent lane names. A gate that exists only in CI teaches push-and-wait; a gate that exists
only locally does not exist. *(build-catchable — CI runs the identical script,
`config/ci-github.yml`)*

## What blocks merge

- Any per-commit or per-merge gate red on either leg (invariant 9: every commit builds and tests
  both legs from the same sources). *(build-catchable)*
- A cross-leg exact-golden mismatch — a determinism regression **by definition**, never
  re-approved to green without a first-divergence analysis. [ESTABLISHED: booklet section 14.3]
- A structural-audit finding: OS symbol in core, include-arrow violation, `#ifdef` outside
  confinement, registry/schema id reuse. *(build-catchable, G3)*
- Advisory gates never block — but each carries an owner and a dated promotion decision, or it
  does not exist. *(contract-only, the ledger row records both)*

## Adding a gate = the ratchet

Procedure (normative: `reference/quality_gates_ci_manifest.md` section G8):

1. Gate lands as: script in the repo + artifact spec + `check.sh` lane + CI wiring running the
   **same command**.
2. Baseline recorded — today's measured number, dated.
3. Direction one-way, with a **floor and an owner** named in the ledger row. A ratchet with
   neither is a number that drifts.
4. Advisory period is dated; promotion to blocking happens on the date, or the date moves with a
   recorded reason.

The standing budgets ride this machinery as fitness functions [ESTABLISHED: booklet section
15.4]: go-live time · per-block working set vs cache budget · stack watermarks · ring depths vs
capacity · cycles-per-frame vs baseline · headroom floor · computed-vs-measured latency remainder.
Trended with alarms — a budget checked once is a snapshot. Wiring:
`reference/quality_gates_ci_manifest.md` section G4.

## Artifact locations

Every gate emits one; CI's job is transport, not interpretation. [Doctrine; paths normative in G2
and `config/ci-github.yml`.]

| gate | artifact |
|---|---|
| test suites | KEY=value fail blocks + suite report (`reference/testing_verification_manifest.md` section T2) |
| golden gates | diff report: master id, regime, max deviation, first divergent frame |
| sanitizer lanes | the sanitizer's own report, captured whole |
| remark gates | per-kernel remark list + diff vs the committed expectation |
| bench gates | before/after JSON distributions, machine identity embedded |
| structural audits | findings as file:line rows (JSON) |
| soak rung | session reports — the same schema users attach to bug reports (`config/session_report.schema.json`) |
| buffer sweep | the robustness curve, a published artifact (invariant 16) |

## The dual-leg matrix

Per-leg tool reality, pinned [normative availability matrix: hub H5 — VERSION-DEPENDENT - hub H5]:

| lane | Linux leg | Windows leg (CLANG64) |
|---|---|---|
| ASan / UBSan | yes [CC-FACT: standard clang runtimes] | yes [MEASURED 2026-08-12] |
| TSan | yes — the concurrency lane lives here | **no** [MEASURED 2026-08-12] |
| libFuzzer | yes [CC-FACT] | yes [MEASURED 2026-08-12: `libclang_rt.fuzzer*` present] |
| BOLT | optional, measured row | **no** [MEASURED 2026-08-12] |

Single-leg TSan speaks for both legs because the code under test is identical and TSan checks the
C11 model, not the hardware — the discipline of
`reference/rt_plane_rules_manifest.md` section R6 is what makes this transfer valid.
[ESTABLISHED: booklet section 10.8]

## Never

- A gate that runs only in CI, or only locally. *(build-catchable — same-script rule)*
- Autofix in CI — CI reports; humans and hooks fix. *(contract-only)*
- Rerun-to-green without a recorded cause; flakes are quarantined by policy, not by retry.
  *(contract-only — flake register)*
- Absolute-number bench gates: gate on regression vs same-machine baseline; absolute truth belongs
  to the soak. [ESTABLISHED: booklet section 14.5] *(build-catchable)*
- Unpinned toolchain in CI images — versions are hub rows; a silent compiler bump is a silent
  re-verification skip. *(build-catchable: build-identity assertion, invariant 17)*
- Skipping a release rung silently. *(contract-only — release-notes honesty rule)*
- A new "must" in prose without a gate, an analysis rule, or a register entry — route it or it
  does not exist. *(contract-only — the meta-invariant applied to this very file)*

## What you owe

A new gate ships with: its artifact spec · its `check.sh` lane · CI wiring running the same
command · a ledger row with baseline, floor, owner, and promotion date (G1/G8). A changed gate
ships with: a diff of what it now catches vs before, and a migration note for in-flight branches.
A removed gate ships with the recorded decision that retires its rule — otherwise the rule just
became a preference.

## Decisions you must not invent

Soak duration and the product SLO it gates · the supported device matrix · flake quarantine
policy · advisory-gate promotion authority · the per-product blocking set beyond this card's
floor · which machine class hosts the bench lane (the same-machine baseline requirement makes
this a real decision).

## Go deeper

| question | where |
|---|---|
| the full gate ledger with exit codes and runtimes | `reference/quality_gates_ci_manifest.md` section G1 |
| check.sh contract and lane vocabulary | `reference/quality_gates_ci_manifest.md` section G2 + `config/check.sh` |
| structural audits: include, symbol, map, ifdef | `reference/quality_gates_ci_manifest.md` section G3 |
| remark + bench gate wiring | `reference/quality_gates_ci_manifest.md` section G4 |
| the dual-leg CI matrix | `reference/quality_gates_ci_manifest.md` section G5 |
| cross-leg exact-golden gate mechanics | `reference/quality_gates_ci_manifest.md` section G6 |
| soak and release rungs | `reference/quality_gates_ci_manifest.md` section G7 |
| the ratchet | `reference/quality_gates_ci_manifest.md` section G8 |
| audit-script reference | `reference/quality_gates_ci_manifest.md` section G9 |
| CI cadences from the test side | `reference/testing_verification_manifest.md` section T12 |
