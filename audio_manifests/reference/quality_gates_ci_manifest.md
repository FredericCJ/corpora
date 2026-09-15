# Quality Gates & CI — Ground-Truth Manifest

**Purpose.** One ledger of every blocking gate, one script that runs them everywhere, the structural audits that make the architecture mechanical, and the ratchet that only ever tightens — so a red gate routes the coding agent straight to a patch, with self-locating, machine-readable failure artifacts.

Facts verified 2026-08-12. Version-dependent claims route to reference/audio_platform_baseline_manifest.md (the hub); if any file disagrees with the hub, the hub wins.

Reasoning root: the child booklet `realtime-audio-pc-architecture-and-design-r1.md` (repo root) — chiefly booklet ch. 15 (the enforcement ladder), booklet section 14.5–14.6 (performance regression, the CI matrix), booklet section 10.2 (the flag canon), booklet section 10.8 (the verification toolchain). This file operationalizes the booklet; it never re-argues it.

Tag legend: [ESTABLISHED: source] · [VERSION-DEPENDENT - hub H<n>] · [MEASURED <date>] (run on the reference machine; command recorded) · [OPEN — ASSUMED/NEEDS-INPUT] · [CC-FACT] (model knowledge, no named primary source) · [FLAGGED-SECONDARY] · [UNVERIFIED]. Routes are the booklet's seven: compiler-catchable, analysis-catchable, build-catchable, host-test-catchable, target-test-catchable, runtime-catchable, contract-only [ESTABLISHED: booklet section 15.1].

---

## G1. The gate ledger

This table is the traceability spine of CI: for every gate — WHAT ran, WHEN it runs, what red MEANS, WHERE the failure artifact lands, and WHERE to read before patching. A gate whose failure cannot answer those five questions is a defect in this file, not in the code that tripped it [OPEN — ASSUMED, house doctrine]. Cadences are the booklet's ladder: per commit / per merge / per release [ESTABLISHED: booklet section 14.6].

Table-level tags: cadence, meaning, and route columns are [ESTABLISHED: booklet ch. 15, section 14.6] unless a row says otherwise; command spellings and artifact paths are this package's pins, wired in `config/check.sh` and `config/ci-github.yml` [OPEN — ASSUMED; change them there and here together, per G8].

### Blocking, per commit — both legs unless a row says otherwise

| # | gate | command | red means | artifact lands | fix route |
|---|---|---|---|---|---|
| 1 | format | `./check.sh format` | tree diverges from `config/.clang-format` | clang-format diagnostics, file:line, stderr | run `./check.sh --fix` locally; never hand-format |
| 2 | tidy | `./check.sh tidy` | analysis-catchable defect (bugprone-*/clang-analyzer-* are promoted to errors in `config/.clang-tidy`) | `file:line:col: warning/error: … [check-name]` | fix, or NOLINT + deviation record per reference/toolchain_build_manifest.md section B3; G8 polices |
| 3 | build (×2 legs) | `./check.sh build` | warning-canon violation under `-Werror`, poison hit, `_Static_assert`, configure drift | compiler diagnostics; a poison hit prints `attempt to use a poisoned identifier` [MEASURED 2026-08-12] | reference/toolchain_build_manifest.md section B11; poison hits → reference/rt_plane_rules_manifest.md section R2 |
| 4 | unit + property | `./check.sh unit` (ctest) | behavioral regression or property counterexample | ctest log; the failing test's name self-locates per reference/testing_verification_manifest.md section T2; session report per run (E8) | reference/testing_verification_manifest.md section T13 |
| 5 | tolerance goldens | ctest rows inside gate 4 (label `golden`) | numeric drift beyond the pinned tolerance | diff report under `build/<preset>/golden_diffs/` | reference/testing_verification_manifest.md section T4; intended change → baseline ritual, G8 |
| 6 | ASan+UBSan lane | `./check.sh san` | memory error / undefined behavior in the host suite | sanitizer report, self-locating — UBSan prints `file:line:col: runtime error: …` + SUMMARY line [MEASURED 2026-08-12: `p12_ubsan.c:2:34: runtime error: signed integer overflow: 2147483647 + 1 cannot be represented in type int`] | reference/testing_verification_manifest.md section T8; crash harvest → reference/error_tracing_contract_manifest.md section E9 |
| 7 | TSan lane | `./check.sh tsan` — **Linux leg only**, TSan runtime absent on CLANG64 [MEASURED 2026-08-12 — hub H5] | data race / ordering violation in the stress suites | TSan report, both stacks | reference/testing_verification_manifest.md section T8; blessed idioms → reference/rt_plane_rules_manifest.md section R6 + reference/concurrency_channels_manifest.md |
| 8 | remark gate | `./check.sh remark` | a hot kernel silently de-vectorized — invariant 15 [ESTABLISHED: booklet ch. 3] | `build/<perf-preset>/remarks.log` + `GATE-FAIL gate=remark tu=…` rows | G4 here; ladder → reference/dsp_kernel_patterns_manifest.md section K5; tools → reference/optimization_microarch_manifest.md section P3 |
| 9 | include audit | inside `./check.sh audits` | boundary arrow broken — core saw an adapter/OS header (invariant 8) [ESTABLISHED: booklet section 15.3] | `VIOLATION [INC-xx]` lines (grammar: G9) | G9; zone law → booklet section 15.3 |
| 10 | symbol audit | inside `./check.sh audits` (post-build) | OS import reached the core lib (invariant 8, link half) | `VIOLATION [SYM-01]` lines (grammar: G9) | G9; syscall classes → reference/rt_plane_rules_manifest.md section R7 |
| 11 | session-report schema | `./check.sh schema` | report writer drifted from `config/session_report.schema.json` — the agent feedback loop broke silently | validator errors per sample file | reference/error_tracing_contract_manifest.md section E8; writer → reference/observability_flightring_manifest.md section O7 |

### Blocking, per merge

| # | gate | command | red means | artifact lands | fix route |
|---|---|---|---|---|---|
| 12 | cross-leg exact golden | CI job pair `render-linux` → `compare-win` (config/ci-github.yml) | determinism regression across legs — invariant 11 [ESTABLISHED: booklet ch. 3, section 14.6] | divergence pair under CI artifact `cross-leg-divergence` + `GATE-FAIL gate=cross-leg-golden case=…` | G6 → reference/dsp_kernel_patterns_manifest.md section K6, reference/toolchain_build_manifest.md section B2 |
| 13 | map-file + conditional audits | project `tools/` scripts per G3 (conditional half already runs per commit via INC-05) | section/#ifdef discipline broken | audit output, VIOLATION-style lines | G3 |
| 14 | bench compare | `./check.sh bench` — advisory locally, **blocking on merge where a same-machine baseline exists** | perf regression beyond the tolerance band [ESTABLISHED: booklet section 14.5] | `build/<preset>/bench/*.json` + compare report | G4; protocol → reference/optimization_microarch_manifest.md section P2 |

### Blocking, per release — target rungs, real machines

| # | gate | red means | artifact | spec |
|---|---|---|---|---|
| 15 | soak + headroom floor | invariant 6 headroom claim fails on the reference class | session reports the release notes cite | G7 |
| 16 | buffer sweep | robustness curve regressed (invariant 16) | xrun-vs-period curve artifact | G7 |
| 17 | loopback latency | computed latency sum (booklet section 7.3) diverges from measured | loopback report | G7 |
| 18 | device-matrix smoke | a supported interface fails bring-up | per-device log set | G7; device list → hub H6 |

### Advisory rows (report, trend, alarm — never a silent number)

- **Fuzz budget lane** — libFuzzer targets for every foreign-byte parser, run continuously at CI's budget [ESTABLISHED: booklet section 10.8]; runtime present on both legs [MEASURED 2026-08-12 — hub H5]. Crash artifact + repro input → reference/testing_verification_manifest.md section T9. *(host-test-catchable)*
- **Budget trends** [ESTABLISHED: booklet section 15.4]: go-live time; per-block working set vs cache budget (reference/memory_residency_manifest.md section M8); stack watermarks vs budgets (section M7); ring high-water vs capacity (reference/concurrency_channels_manifest.md section C2); cycles-per-frame vs baseline (P2); headroom floor (G7); computed-vs-measured latency remainder (G7). Each trended with an alarm; a budget checked once is a snapshot. *(build/host/target-test-catchable per row)*

### Artifact-path convention

[OPEN — ASSUMED; pinned here for the family: changing it means updating `config/ci-github.yml` upload globs, `config/check.sh`, and the T/E/O files' pointers together.]

| artifact | path |
|---|---|
| session reports (E8/O7) | `build/<preset>/session_reports/*.json` |
| golden diffs (T4) | `build/<preset>/golden_diffs/` |
| bench JSON (P2) | `build/<preset>/bench/*.json` |
| vectorization remarks (G4) | `build/<perf-preset>/remarks.log` |
| ctest logs | `build/<preset>/Testing/` |

### Reading a red row — the failure-to-patch chain

The ledger exists so this loop never needs archaeology (the E1 loop, applied to CI — reference/error_tracing_contract_manifest.md section E1):

1. **WHAT**: the `GATE-FAIL gate=<name> …` line names the gate; the ledger row above names what red means for it.
2. **WHERE**: the gate's own tool output is self-locating by contract — compiler/tidy/sanitizer print `file:line`, tests carry self-locating names (T2), audits print `path:line: VIOLATION [rule]`. If a gate's output ever fails to locate, that is a defect to fix in the gate, with priority over the code defect it reported [OPEN — ASSUMED, house doctrine].
3. **WHY + context**: pull the artifact from the path column (locally it is already on disk; in CI, download the leg's `*-gate-evidence` bundle). Session reports and golden diffs carry the machine-readable context (build identity per reference/toolchain_build_manifest.md section B10, seeds, case ids).
4. **Patch**: read the fix-route column *before* editing — it names the file that owns the contract the failure broke. Patching against the route (e.g. widening a tolerance to green gate 5) is a G8 rule-3 event, not a fix.
5. **Re-run the one gate** (`./check.sh <gate>`), then the default set before pushing.

Worked example. Gate 9 prints `core/kernels/biquad.c:3: VIOLATION [INC-02] OS header <windows.h> in OS-free zone 'core' …`. WHAT: include audit; red means the core/ports boundary broke. WHERE: file and line are in the message. WHY: someone wanted `QueryPerformanceCounter` in a kernel — the clock belongs behind a port. Patch: move the OS call to the adapter behind the clock port (booklet section 5.4), take the value as data; the fix-route column already pointed to booklet section 15.3's arrow law. Total artifacts consulted: the one VIOLATION line. That is the standard the other rows are held to.

### What the ledger honestly does not cover

The gates end where the contract-only register begins: loop-boundedness arguments, happens-before write-ups for new channel shapes, wait-freedom claims, per-op latency declarations, degrade-ladder policy, bench-environment honesty, profile-corpus representativeness — reviewed **by name** on the review checklist, never implied to be gated [ESTABLISHED: booklet section 15.5]. The register lives in reference/rt_plane_rules_manifest.md section R8; the review procedure in cards/review-code.md. A green ledger plus an unreviewed register is half a verification story — say which half you have.

## G2. The check.sh contract

One script, three places: editor, pre-commit hook, and CI all run `config/check.sh`. The parity law: **a gate that only runs in CI teaches people to push and wait, and a gate that only runs locally does not exist** [ESTABLISHED: house law, python-agent-ground `config/check.sh`, adopted for this family]. If a check belongs in CI, it goes into check.sh and CI calls the script.

### Invocation

| call | behavior |
|---|---|
| `./check.sh` | default blocking gates, stop at first failure |
| `./check.sh --all` | every default gate, report all failures, exit non-zero at the end |
| `./check.sh --fix` | apply clang-format in place, then run gates — **LOCAL ONLY, never CI** |
| `./check.sh tidy audits` | only the named gates |
| `./check.sh san` / `tsan` / `bench` | named-only lanes (not in the default set) |

Default set: `format tidy build unit audits remark schema`. Named-only: `san tsan bench` — CI wires them as separate steps (G5) so a sanitizer red is its own visible lane, not a buried half of "build" [OPEN — ASSUMED, this package's pin].

Gate order inside the default set is cheapest-first with one exception: `audits` runs after `build` because the symbol audit needs the linked core lib. `format` before `tidy` because tidy diagnostics on unformatted code produce columns that move after formatting [OPEN — ASSUMED ordering, pinned in the script].

### Wiring the three places

| place | wiring |
|---|---|
| editor / agent loop | run `./check.sh <gate>` for the gate the change touches, `./check.sh` before handing off; the script is the interface — no IDE-private task definitions that drift from it [OPEN — ASSUMED] |
| pre-commit hook | `.git/hooks/pre-commit` (or the hook framework's entry) is one line: `exec ./check.sh` — a hook that does anything else violates parity [OPEN — ASSUMED] |
| CI | `./check.sh --all` per leg job, plus the named lanes as separate steps — config/ci-github.yml, walkthrough in G5 |

### Leg awareness

check.sh runs the **current-OS leg**; CI runs both legs by running the same script once per leg job [ESTABLISHED: booklet section 14.6 — the two-leg matrix is invariant 9's proof]. Detection: `uname -s` matching `*_NT*` selects the Windows leg — in the MSYS2 CLANG64 shell `uname -s` prints `MINGW64_NT-10.0-26200`, so the `_NT` suffix, not a "CLANG64" string, is the discriminator [MEASURED 2026-08-12: `MSYSTEM=CLANG64 bash -lc 'uname -s'`]. The Windows leg then requires `MSYSTEM=CLANG64` and exits 2 otherwise — building in MSYS/MINGW64/UCRT64 links the wrong runtime family (hub H3) [VERSION-DEPENDENT - hub H3]. *(build-catchable — the wrong-shell guard)*

### Environment pins (override → env var; defaults are DECIDE rows)

| pin | env var | default | must match |
|---|---|---|---|
| gate preset | `CHECK_PRESET` | `<leg>-test` | `config/CMakePresets.json` (reference/toolchain_build_manifest.md section B5) |
| perf preset (remark/bench) | `CHECK_PERF_PRESET` | `<leg>-perf` | same |
| san / tsan presets | `CHECK_SAN_PRESET` / `CHECK_TSAN_PRESET` | `<leg>-test` (ASan+UBSan already ride cfg-test) / `linux-tsan` | same; T8 |
| core lib (symbol audit) | `CHECK_CORE_LIB` | `build/<preset>/core/libaudio_core.a` | the build's real output path |
| symbol allowlist | `CHECK_SYMBOL_ALLOWLIST` | `config/core_symbol_allowlist.txt` | created by the G9 bootstrap ritual |
| kernel manifest (remark) | `CHECK_KERNEL_MANIFEST` | `tools/kernel_manifest.txt` | G4 |
| schema samples | `CHECK_SCHEMA_SAMPLES` | `test/data/session_reports` | E8 sample set |

All rows [OPEN — ASSUMED defaults; each carries a DECIDE comment in the script].

### Machine-readable failure grammar

Every failed gate prints, besides its tool output, exactly one routing line — the doctrine made mechanical: the artifact itself tells the agent what failed and where to read:

```
GATE-FAIL gate=<name> route=<file/section to read before patching>
```

Placeholder gates that are not yet wired print `GATE-NOT-WIRED gate=<name> … route=…` and pass; G8 obliges the project to flip each one blocking during bring-up. A leg-inapplicable gate prints `SKIP gate=<name> reason=…` (e.g. tsan on Windows — hub H5). Exit codes: `0` all pass · `1` at least one gate failed · `2` usage or wrong environment. [All: this package's contract, implemented in `config/check.sh`; guard behavior verified by running the script — MEASURED 2026-08-12.]

Guard transcripts [MEASURED 2026-08-12: `sh check.sh format` in a MINGW64 (non-CLANG64) shell; `MSYSTEM=CLANG64 sh check.sh nosuchgate`]:

```
check.sh: MSYSTEM='MINGW64' -- the Windows leg builds only in the MSYS2
CLANG64 environment (hub H3). Open a CLANG64 shell, not MSYS/MINGW64/UCRT64.
(exit 2)

check.sh: unknown gate 'nosuchgate' (known: format tidy build unit audits remark schema san tsan bench)
(exit 2)
```

Both errors are self-locating in the doctrine's sense: they name the wrong state, the right state, and where the right state is documented — an agent seeing either knows the patch is to its environment, not to the code.

### Never

- **Never `--fix` in CI.** CI reports; humans and hooks fix. *(contract-only, stated in the script header)*
- **Never wholesale `clang-tidy --fix`** — fix-its can change semantics near `volatile`, atomics, and macro-heavy DSP code; apply per-check, reviewed [CC-FACT]. *(contract-only)*
- **Never green a gate by loosening its config in the same change that trips it** — a loosening is its own reviewed commit with a ledger row (G8). *(contract-only, review checklist)*
- **Never let a `GATE-NOT-WIRED` line survive past project bring-up** — the ratchet's first job (G8). *(contract-only)*
- **Never run the Windows gates outside the CLANG64 shell** — enforced, exit 2. *(build-catchable)*

## G3. Structural audits

The build-graph gates of booklet section 15.3, as runnable scripts plus their rule rows. Every audit fails the build; prose made law [ESTABLISHED: booklet section 15.3].

| audit | mechanism | asserts | route |
|---|---|---|---|
| include audit | `config/audit_includes.py` (G9) | `core/` includes only `core/` + `ports/` (+ compiler port); adapters include ports + own subtree, never a sibling adapter; nothing includes `adapters/` except the composition root; `core/ports` are OS-header-free | build-catchable |
| symbol audit | `config/audit_symbols.py` over the linked core static lib via llvm-nm [MEASURED 2026-08-12: llvm-nm lists object symbols] | the core lib's undefined-symbol set ⊆ reviewed allowlist: C-runtime math/memory primitives + port symbols — **no OS import passes** (invariant 8, link half) | build-catchable |
| conditional-inclusion confinement | folded into the include audit as rule INC-05 | no OS/compiler conditional token (`_WIN32`, `__linux__`, `_MSC_VER`, …) in `core/`/`ports/`; adapters and shell only; compiler port exempt [ESTABLISHED: booklet section 5.5, 5.6] | build-catchable |
| map-file audit | project `tools/` script over lld map files (`-Wl,-Map,<file>` on both legs' lld [CC-FACT — verify the spelling on first wiring; linking rows: reference/toolchain_build_manifest.md section B9]) | RT-hot code/data land in their collected sections; guard-page symbols where the layout plan says; section sizes feed the size trend | build-catchable |

Notes that keep these audits honest:

- **The two halves of invariant 8 are deliberately redundant.** The include audit catches the *spelling* of a dependency at its cheapest rung; the symbol audit catches what arrives indirectly (a helper library, a transitively pulled object). Same pattern as poison-header vs interposition-net [ESTABLISHED: booklet section 15.2].
- **libm rows in the allowlist are a decision, not a default.** Invariant 11 bans system-math calls on determinism-relevant paths; non-determinism-relevant core code may still call `sinf` [ESTABLISHED: booklet ch. 3, invariant 11]. Which libm symbols the allowlist admits is [OPEN — NEEDS-INPUT: per-project; the exact-golden suite (G6) is the backstop either way]. Kernel-side replacements: reference/dsp_kernel_patterns_manifest.md section K6.
- **The map-file audit has no packaged script** — its rows depend on the project's section-naming plan (B9). Write it in project `tools/`, versioned with the code, printing the same `VIOLATION` grammar as G9 so one parser reads all audits [OPEN — ASSUMED convention]. Row spec, from booklet section 15.3 [ESTABLISHED]:

| map-file audit row | asserts |
|---|---|
| RT-hot collection | every symbol in the hot-function list (the same list the remark gate keys on, G4) landed in the collected RT-hot section per the B9 layout plan |
| RT-data collection | RT-touched data objects in their collected section — layout is the cache's landlord (booklet section 8.4) |
| guard symbols | stack/arena guard symbols present where the memory plan places them (reference/memory_residency_manifest.md section M7) |
| size trend | per-section sizes emitted as a JSON row per build; the trend, not the number, alarms (booklet section 15.4) |

- **Textual limits.** The include audit reads `#include`/`#if` lines; it does not preprocess. A dependency smuggled through a macro is the symbol audit's or review's catch — registered residue, reference/rt_plane_rules_manifest.md section R8. *(contract-only residue, stated)*

### Who catches what — the redundancy matrix

The audits overlap by design; this matrix is what to consult when deciding whether a new hazard needs a new rule or already has two nets [OPEN — ASSUMED compilation; each cell's mechanism is ESTABLISHED per its file]:

| hazard | compile time | build/audit time | runtime (dev builds) |
|---|---|---|---|
| core calls `malloc` by name | poison prelude — compile error [MEASURED 2026-08-12: `attempt to use a poisoned identifier`] | symbol audit (`malloc` not allowlisted) | interposition net via `--wrap` [MEASURED 2026-08-12: `-Wl,--wrap=malloc` links; wraps CRT-startup allocs too] (R4) |
| core includes an OS header | — | include audit INC-02 | — |
| core reaches an OS symbol through a helper lib | — | symbol audit SYM-01 | RT guard traps the blocking call class (R4) |
| per-OS `#ifdef` leaks into core | — | include audit INC-05 | cross-leg golden divergence (G6), late and expensive — the audit exists so it never gets that far |
| kernel silently de-vectorizes | — | remark gate (G4) | bench trend drift (G4), late — same rationale |

## G4. Remark + bench gate wiring

### The remark gate (invariant 15, vectorization half)

A hot kernel the compiler quietly stopped vectorizing is a regression nobody filed [ESTABLISHED: booklet section 14.5]. Wiring, as implemented in `config/check.sh`:

1. **The kernel manifest** — `tools/kernel_manifest.txt` [OPEN — ASSUMED path; env `CHECK_KERNEL_MANIFEST`], one row per hot TU: `core/kernels/biquad.c` or `core/kernels/biquad.c:process_block` (everything after the first `:` is for humans; the gate keys on the TU path). `#` comments and blank lines allowed. Curated by hand: a kernel enters the manifest when it enters the hot set (reference/dsp_kernel_patterns_manifest.md section K4's walkthrough ends with this row).

   ```
   # tools/kernel_manifest.txt -- hot TUs whose vectorization is a build gate (invariant 15)
   core/kernels/biquad.c:biquad_process_block
   core/kernels/mix.c:mix_accumulate
   core/kernels/gain_ramp.c        # whole-TU row: every hot loop in it
   ```
2. **Build with remarks on.** The perf/ship presets always build under ThinLTO (B2/B8's class×config matrix), so the compile-time `-Rpass=loop-vectorize` remark is SILENT and the link-time row (`AUDIO_LTO_REMARK_LDFLAGS`, already wired into cfg-perf/cfg-ship) is what actually fires [MEASURED 2026-08-12 — B8]. That link-time remark lands on **stdout**, not stderr; check.sh captures both streams into the same log (`cmake --build --preset "$PERF_PRESET" >"$log" 2>&1`) so neither route is silently dropped.
3. **Force re-emission.** Remarks only appear for TUs that actually compile, so the gate touches every manifest TU before building — an incremental build otherwise skips them and a green gate would be vacuous [CC-FACT: ninja rebuilds on mtime].
4. **Grep the anchor — both shapes.** The perf/ship presets always build kernel-class TUs under ThinLTO (B2's class×config matrix), and B8's measured discovery is that under `-flto=thin` the compile-time `-Rpass` remark is SILENT — only the link-time row (`AUDIO_LTO_REMARK_LDFLAGS`, already wired into cfg-perf/cfg-ship) fires, and it drops the `remark:` tag: `<tu>:<line>:<col>: vectorized loop (vectorization width: 8, interleaved count: 4)` [MEASURED 2026-08-12, B8]. The gate must therefore grep `<tu>:[0-9]+:[0-9]+: (remark: )?vectorized loop` per manifest row — both the compile-time and link-time shapes hit, substring match so a build-relative path prefix still hits.
5. **Fail loud and routed.** Each missing row prints `GATE-FAIL gate=remark tu=<tu> reason=no-vectorized-loop-remark route=dsp_kernel_patterns K5 + optimization P3`, and the gate exits non-zero.

The gate asserts *presence*, not width — width rides the ISA floor (hub H8) and belongs to the bench lane, not a grep [OPEN — ASSUMED]. Upgrade path when file-granularity gets too coarse: `-fsave-optimization-record` emits per-TU YAML opt records carrying pass and function names — machine-readable, per-function gating [CC-FACT: verify the field names on your first record before parsing; toolchain rows → B8].

Failure semantics: red here means the *toolchain changed its mind* about your kernel — a flag drifted (B2), an aliasing or layout change defeated the vectorizer (K5), or a toolchain bump changed cost models (re-run the bump ritual, G8). It is never fixed by deleting the manifest row without a review [ESTABLISHED: booklet section 10.2 — the canon is diffed, not eroded]. *(build-catchable)*

### The bench gate (invariant 15, measurement half)

- **Protocol and JSON shape** are owned by reference/optimization_microarch_manifest.md section P2 (pinned core, elevation, warm-up, distribution min/median/p99/max, cycles-per-frame, environment block) [ESTABLISHED: booklet section 10.6].
- **Baseline law: same machine or no gate.** CI gates on same-machine baselines with tolerance bands; cross-machine numbers compare only as ratios against a reference kernel [ESTABLISHED: booklet section 10.6]. Hosted CI runners have no stable machine identity, so **bench never blocks on hosted runners** — the yml marks the lane `continue-on-error` (G5). The blocking compare runs where a pinned baseline exists: the reference machine locally, or a reference-class self-hosted runner [OPEN — NEEDS-INPUT: does the project run one?].
- **Advisory locally, blocking on merge** (on that baseline-bearing runner): `CHECK_BENCH_BLOCKING=1` flips the check.sh lane from warn to fail [OPEN — ASSUMED mechanism, pinned in check.sh].
- **Tolerance bands**: [OPEN — ASSUMED starting point: median +5%, p99 +10%, per kernel, vs the committed baseline JSON; tighten with data, per G8]. A regression prints the kernel, both numbers, and the band — the failure names its own threshold. *(host-test-catchable locally, target-test-catchable on the reference rig)*
- **The compare's failure line** follows the house grammar so the same CI annotator reads it [OPEN — ASSUMED spec for the project-side compare tool]:

  ```
  GATE-FAIL gate=bench kernel=<name> stat=<median|p99> baseline=<cycles/frame> now=<cycles/frame> band=+<pct>% route=optimization P4-P7
  ```

  The route lands in the optimization file's recipe sections because a bench regression is a performance defect with a diagnosis ladder, not a build defect: reference/optimization_microarch_manifest.md section P7 (stall/flush table) is the first read when the remark gate is still green but cycles moved.
- **Baseline update ritual**: a deliberate improvement re-records the baseline in its own commit, with the bench JSON diff and the reason line — G8 rule 2. The baseline file carries the machine identity block from P2; a baseline whose machine block does not match the runner refuses to gate [OPEN — ASSUMED, implement in the compare tool].

## G5. The dual-leg CI matrix — config/ci-github.yml walkthrough

The file is **EXAMPLE-ONLY** (its header says so): copy into `.github/workflows/`, resolve the DECIDE rows, re-pin action tags per org policy. CI adds exactly two things over check.sh: the second leg, and artifact upload. Everything else funnels through the script — the parity law (G2).

| job | runner | steps → gates | notes |
|---|---|---|---|
| `win` | `windows-latest` | checkout → setup-msys2 (CLANG64) → `./check.sh --all` → `./check.sh san` → bench (advisory) → upload evidence | every run step executes in the CLANG64 shell via `defaults.run.shell: msys2 {0}` [CC-FACT: msys2/setup-msys2 action and its `msystem:`/`install:` inputs exist — verify the tag] |
| `linux` | `ubuntu-latest` | checkout → apt install → `./check.sh --all` → `./check.sh san` → `./check.sh tsan` → bench (advisory) → upload evidence | TSan lane lives here and only here [MEASURED 2026-08-12: TSan runtime absent on CLANG64 — hub H5] |
| `render-linux` → `compare-win` | both | per-merge exact-golden pair | G6 |

Load-bearing details, each in the yml as a comment:

- **Windows package row** = hub H3's install list: `mingw-w64-clang-x86_64-{clang,lld,llvm,clang-tools-extra,clang-analyzer,compiler-rt,cmake,ninja,python}` plus msys `git make diffutils`. Package names exist in the pacman repo [MEASURED 2026-08-12: `mingw-w64-clang-x86_64-cmake 4.3.4-1`, `mingw-w64-clang-x86_64-ninja 1.13.2-1`; clang family 22.1.8-1 — hub H3] [VERSION-DEPENDENT - hub H3].
- **`git` inside MSYS2**: check.sh calls `git ls-files` in the MSYS2 shell, whose PATH does not carry the runner's host git by default [CC-FACT].
- **Why the CLANG64 shell is load-bearing for the san lane**: ASan on this leg links a dynamic runtime that lives in `clang64/bin`, already on PATH inside the shell — san-built test executables run clean there [MEASURED 2026-08-12: `-fsanitize=address` links and runs on CLANG64 — hub H5]. Running the same binaries from a non-MSYS2 context must ship that DLL's directory on PATH or they die at load [CC-FACT].
- **Line endings**: check.sh is POSIX sh; CRLF breaks it. Commit `.gitattributes` with `*.sh text eol=lf` [CC-FACT]. *(build-catchable — the failure is immediate and self-announcing)*
- **Linux toolchain skew**: `ubuntu-latest` ships the image's clang, not the pinned major; the bare `apt-get install clang` line is a runnable placeholder — production wiring uses the pinned major per hub H4 [VERSION-DEPENDENT - hub H4]. Flag canon assumes the pin (B2).
- **Artifacts upload red or green** (`if: always()`): session reports, golden diffs, bench JSON, remarks.log, ctest XML — the G1 path convention. A red CI run that uploads nothing has destroyed the evidence the agent needs; upload is part of the gate, not a courtesy [OPEN — ASSUMED, house doctrine].
- **Cost note**: `update: true` + full package install runs per job; cache via the action's built-in mechanisms when it hurts [CC-FACT — verify current caching guidance before adding knobs].

### Reading a red CI run

Order of reads, fixed so the agent never scrolls logs blind [OPEN — ASSUMED procedure]:

1. **Which job** — leg tells you scope: one leg red = leg-specific (adapter, per-leg flag row, toolchain skew); both legs red = core/portable defect. That asymmetry is the two-leg matrix's diagnostic dividend [ESTABLISHED: booklet section 14.6 — invariant 9's proof doubles as a bisection].
2. **Which step** — steps map 1:1 to gates (the table above); the step name is the gate name.
3. **The `GATE-FAIL` / `VIOLATION` lines** in that step's log — grep for them; they are the routed summary.
4. **The evidence bundle** — download `<leg>-gate-evidence`; session reports and diffs carry the machine-readable context (T13 reads them field by field).
5. **Reproduce locally on the same leg** with the single named gate: `./check.sh <gate>`. If it does not reproduce, suspect the DECIDE rows drifting between local and CI (preset names, pinned versions — hub H9's re-check triggers).

### Extending the matrix

Nightly/cron lanes (fuzz budget, soak-lite, long property sweeps) attach as additional jobs calling the same script with their named gate — never as bespoke YAML logic [OPEN — ASSUMED]. Fuzz targets: reference/testing_verification_manifest.md section T9; libFuzzer runtime present on both legs [MEASURED 2026-08-12 — hub H5].

## G6. The cross-leg exact-golden gate

One leg renders the exact suite, the other **byte-compares** — the determinism contract of invariant 11 enforced as a merge gate [ESTABLISHED: booklet section 14.6: "one leg renders, the other byte-compares"].

**Job shape** (implemented as `render-linux` → `compare-win` in config/ci-github.yml):

1. `render-linux` (on merge only: `if: github.event_name == 'push'`): build the perf preset, run the offline renderer over the exact-golden case list, upload the rendered set as artifact `exact-goldens-linux`. Renderer invocation is a DECIDE row — harness spec: reference/testing_verification_manifest.md section T3.
2. `compare-win`: download the artifact, render the same cases locally in the CLANG64 environment, `cmp` each pair. Any differing byte prints `GATE-FAIL gate=cross-leg-golden case=<name> route=quality_gates_ci G6` and fails; both rendered sets upload as `cross-leg-divergence` for offline analysis.

**Preconditions** — the gate is meaningful only when these hold; check them before blaming the code [ESTABLISHED: booklet section 9.6/10.2 via reference/dsp_kernel_patterns_manifest.md section K6]:

| precondition | pinned where |
|---|---|
| kernel dispatch forced to one pinned tier on both legs (no per-machine SIMD selection in the exact suite) | renderer flag, T3; ladder → K5 |
| contraction pinned: same `-ffp-contract` row both legs | flag canon, B2 |
| no value-changing fast-math on kernel TUs | flag canon, B2 |
| no system-libm call on the rendered paths | symbol audit + K6 |
| same sample formats/quantum in the case list | T4 case registry |

**Failure = determinism regression.** Triage in order [OPEN — ASSUMED order; each mechanism ESTABLISHED per its file]:

| symptom | first suspect | route |
|---|---|---|
| every case diverges | flag parity drift between the legs' toolchain files — the usual culprit after a toolchain bump | B2 diff; G8 rule 6 |
| one kernel's cases diverge | FP regime drift in that kernel: a new libm call, a contraction-sensitive rewrite, a fresh intrinsic | K6; symbol audit confirms the libm half |
| diverges only at block boundaries | hidden per-callback state — partition invariance broke, not determinism | invariant 20's property suite, reference/testing_verification_manifest.md section T5 |
| diverges after an `#ifdef`-scented diff | an arch/OS conditional reached core — INC-05 should have caught it; extend the token list | G9; G8 rule 1 |

Direction of render/compare (Linux renders, Windows compares) is [OPEN — ASSUMED: either direction proves the same equality; swap freely]. *(build-catchable in cadence, host-test-catchable in mechanism)*

## G7. Soak + release rungs

The target-test-catchable rungs: real machines of the reference class, real audio devices, both OSes [ESTABLISHED: booklet section 14.6]. These do not run on hosted CI (G5's yml ends by saying so) — they run on the reference rig(s), scripted, producing artifacts the release notes cite by name.

| rung | harness | gate | artifact |
|---|---|---|---|
| **soak** | hours-long real-device run at the shipped period matrix, always-on monitors as witness [ESTABLISHED: booklet section 14.6] | headroom floor: callback-cost p99.99 ≤ 50% of period on the reference class, AND zero unexplained xruns — invariant 6's floor with p99.99 pinned as the gate statistic so one cosmic-ray outlier cannot invalidate an 8-hour run; max is still reported and every xrun still needs a classified cause [OPEN — ASSUMED refinement of invariant 6's "worst observed"] | the run's session reports (E8) + cost histograms (reference/observability_flightring_manifest.md section O4) |
| **buffer sweep** | sweep the supported period range, count/classify xruns per point | the xrun-vs-period robustness curve regenerated and not regressed vs last release — invariant 16 [ESTABLISHED: booklet ch. 3] | the curve, a published artifact |
| **loopback latency** | physical loopback, measure round trip | measured ≈ computed end-to-end sum (booklet section 7.3); tolerance [OPEN — NEEDS-INPUT: per product, ms] | loopback report with the per-stage ledger |
| **device-matrix smoke** | bring-up + short stream on the deployment's supported interface list (hub H6) | every listed device opens, streams, recovers from a forced format change (T6 fault verbs) | per-device log set |

**The honesty rules** [ESTABLISHED: booklet section 14.6]:

- Release notes **cite the artifacts** — session-report ids, the curve, the loopback ledger. A performance claim without its artifact is folklore (invariant 15).
- **A skipped rung is a declared risk**, written in the notes — a risk decision, not an oversight.
- The **toolchain-bump ritual** re-runs everything above plus the full golden-exact matrix *before* the hub row advances [ESTABLISHED: booklet section 14.6, section 10.2]. *(target-test-catchable; the declaration itself contract-only)*

Release-notes evidence block, the template [OPEN — ASSUMED format; the obligation is ESTABLISHED: booklet section 14.6]:

```
release-evidence:
  soak:      run-id=<session-report id>  machine=<hub H2 row>  periods=<matrix>  p99.99/period=<pct>  xruns=<n, classified>
  sweep:     artifact=<curve file>       supported-range=<min..max frames>
  loopback:  measured=<ms>  computed=<ms>  (booklet section 7.3 ledger attached)
  devices:   list=<hub H6 row>  failures=<none | named>
  skipped:   <rung>: <declared risk + reason>          # only if any
```

Soak runs are driven by the same session-report machinery the product always runs (invariant 5) — the rung adds duration and a gate, not new instrumentation; diagnosis mode for a red soak: reference/observability_flightring_manifest.md section O9, autopsy taxonomy booklet section 11.5.

## G8. The ratchet

How gates change over time. Direction is the whole rule: **tighter is routine, looser is an event** [ESTABLISHED: booklet ch. 15 meta-invariant — a rule with no enforcer is a preference].

1. **New rule: advisory → measured → blocking.** A new gate (or tidy check, or audit rule) enters as report-only (`GATE-NOT-WIRED`/warn), runs long enough to measure its noise, gets its threshold set from data, then flips blocking with a dated ledger row in G1. Shipping a placeholder forever is the failure mode this staging exists to prevent — bring-up ends when no `GATE-NOT-WIRED` lines print. [OPEN — ASSUMED, house convention.]
2. **Baseline updates are reviewed diffs.** Golden masters, bench baselines, the symbol allowlist, tolerance bands: every update is a commit whose diff is read, with a one-line reason recorded (T4's ritual for goldens; G9's for the allowlist). Regenerate-and-commit-blind is how a regression becomes the new truth. *(contract-only, review checklist)*
3. **Never silently loosen.** Removing a tidy check, widening a band, allowlisting a symbol, exempting a file: each is its own commit, named in the message, with a ledger/deviation row and — where temporary — an expiry note. A loosening folded into a feature diff fails review. *(contract-only)*
4. **Suppressions carry reasons.** `NOLINT(<check>)` needs a trailing reason and a deviation record (B3); an allowlist entry needs its comment; an INC rule exemption needs its table row comment. The G9 scripts and `config/.clang-tidy` are written so the reviewable text sits next to the exception. *(analysis/build-catchable for presence; the reason's quality: contract-only)*
5. **Audit scripts version with the code.** `config/audit_*.py`, check.sh, the tidy/format configs, kernel manifest, allowlists: same repo, same commit — a gate change and the code change it permits land atomically and revert atomically [ESTABLISHED: booklet section 15.3 — "versioned, run in CI, failing the build"].
6. **Toolchain bumps re-arm everything.** New clang major or OS baseline: re-run remark gates, bench suite, golden masters, the full ledger, and the cross-leg exact matrix *before* the hub row moves; diff the flag canon per B2 [ESTABLISHED: booklet section 10.2, 14.6]. Re-check triggers list: hub H9.

The dated ledger row, template [OPEN — ASSUMED format]. Every gate state change (advisory→blocking, threshold move, exemption) appends one row to a `GATES-CHANGELOG` block kept at the bottom of the project's copy of this file or beside check.sh — the ratchet's audit trail:

```
2026-08-12  remark    advisory->blocking   rows=3 kernels   noise-run=14d clean   by=<reviewer>
2026-08-12  tidy      -readability-magic-numbers   reason=coefficient blocks   expiry=none
```

A row without a reason is itself a G8 rule-4 violation. Reviewers check the changelog before trusting any green run that follows a gate change. *(contract-only, but one `grep -c` away from a fitness function)*

## G9. Audit-script reference

Both scripts are stdlib-only Python, print one machine-parseable `VIOLATION` line per finding plus one summary line — the same grammar family so one CI annotator parses both — and share the exit-code contract [behavior verified by running both scripts against planted-defect fixtures, MEASURED 2026-08-12; transcripts below]:

| exit | meaning | agent action |
|---|---|---|
| 0 | clean (or a bootstrap dump completed) | proceed |
| 1 | ≥1 VIOLATION printed | read the lines; each names its rule and location; fix-routes in the rule tables below |
| 2 | usage/environment error (bad root, missing lib/allowlist, nm not found, malformed allowlist) | the message names the missing piece and where it is documented; fix the wiring, not the code |

### config/audit_includes.py — the include audit (+ conditional confinement)

```
python config/audit_includes.py <repo-root>
python config/audit_includes.py <repo-root> --list-rules
```

- **Walks** the zone directories (`core ports adapters shell tools tests` — a DATA tuple at the top of the script; edit to match the tree) for `.c`/`.h` files.
- **Rules** (each detail line names its rule id):

| rule | fires when | route |
|---|---|---|
| INC-01 | quoted include crosses a zone boundary the ALLOW table forbids (incl. `..` parent-relative includes, which defeat the audit) | build-catchable |
| INC-02 | OS header (`<windows.h>`, `<alsa/…>`, `<sys/…>`, `<pthread.h>`, …) in OS-free `core`/`ports` | build-catchable |
| INC-03 | an adapter includes a sibling adapter subtree (legs never cross) | build-catchable |
| INC-04 | banned facility header (`stdio.h`, `locale.h`, `threads.h`) in `core`/`ports` — include-granularity twin of the poison prelude (`config/rt_prelude_poison.h`, R2) | build-catchable |
| INC-05 | OS/compiler conditional token (`_WIN32`, `__linux__`, `_MSC_VER`, …) on an `#if*` line in `core`/`ports`; compiler port exempt (default `ports/compiler_port.h`, a DECIDE constant) | build-catchable |

- **Output grammar** (paths repo-relative, POSIX slashes — so the `file:line:` prefix stays colon-parseable on Windows):

```
^(?P<file>[^:]+):(?P<line>[0-9]+): VIOLATION \[(?P<rule>INC-[0-9]{2})\] (?P<detail>.*)$
include-audit: files=<n> violations=<m>
```

- **Example run** [MEASURED 2026-08-12, planted-defect fixture tree]:

```
core/kernels/biquad.c:3: VIOLATION [INC-02] OS header <windows.h> in OS-free zone 'core' (invariant 8; symbol audit is the link-time twin)
core/kernels/biquad.c:4: VIOLATION [INC-04] banned facility header <stdio.h> in zone 'core' (rt_plane_rules R2; config/rt_prelude_poison.h)
core/kernels/biquad.c:5: VIOLATION [INC-01] include "adapters/alsa/alsa_adapter.h" -> zone 'adapters' not allowed from zone 'core' (allowed: core, ports)
core/kernels/biquad.c:6: VIOLATION [INC-05] OS/compiler conditional token '_WIN32' in zone 'core' (confinement: adapters/shell only; compiler port exempt)
core/kernels/biquad.c:7: VIOLATION [INC-01] parent-relative include "../secret.h" defeats the audit -- include repo-root-relative or same-dir only
ports/audio_port.h:1: VIOLATION [INC-02] OS header <alsa/asoundlib.h> in OS-free zone 'ports' (invariant 8; symbol audit is the link-time twin)
adapters/wasapi/wasapi_adapter.c:1: VIOLATION [INC-03] adapter 'wasapi' includes sibling adapter 'alsa' -- adapter subtrees never cross
include-audit: files=6 violations=7
```

- **Editing the tables**: `ZONES`, `ALLOW`, `OS_HEADERS(_PREFIXES)`, `BANNED_FACILITY_HEADERS`, `COMPILER_PORT_EXEMPT` are data at the top of the script, each with its DECIDE comment. Additions tighten freely; removals follow G8 rule 3. One shipped judgment to review at adoption: the `tests` zone may include `adapters` so port-contract suites (T6) can instantiate the real adapter — tighten if your suites go through shell factories [OPEN — ASSUMED].

### config/audit_symbols.py — the symbol audit

```
python config/audit_symbols.py <static-lib> <allowlist> [--nm PATH]
python config/audit_symbols.py <static-lib> --print-undefined      # bootstrap dump
```

- **Mechanism**: `llvm-nm --undefined-only --format=posix <lib>`; collects type-`U` symbols per archive member (`llvm-nm` binary from `--nm`, else `$LLVM_NM`, else PATH). Weak-undefined (`w`/`v`) are ignored — they bind to null when absent; review one by hand if it appears [CC-FACT].
- **Allowlist grammar** (one entry per line; documented in the script header): exact symbol name, or a single trailing-`*` prefix glob (`art_port_*`); `#` comments full-line or trailing; blank lines ignored; any other glob form is a config error (exit 2, with file:line). Names are raw nm names — x86_64 ELF and x86_64 COFF both carry undecorated C names, so one allowlist serves both legs [CC-FACT, and consistent with the measured run below].
- **Output grammar**:

```
^VIOLATION \[SYM-01\] undefined symbol '(?P<sym>[^']+)' not in allowlist \(member: (?P<member>[^)]+)\)$
symbol-audit: lib=<lib> undefined=<n> allowlisted=<k> violations=<m>
```

- **Example run** [MEASURED 2026-08-12: fixture lib built with CLANG64 clang 22.1.8, one planted OS import; allowlist = `memcpy`, `sinf`, `art_port_*`]:

```
VIOLATION [SYM-01] undefined symbol 'VirtualLock' not in allowlist (member: core_bit.o)
symbol-audit: lib=libcore_bit.a undefined=4 allowlisted=3 violations=1
```

- **Bootstrap ritual** (creates `config/core_symbol_allowlist.txt`): build the core lib (`./check.sh build`), run `--print-undefined`, review **every** symbol against reference/rt_plane_rules_manifest.md section R7 and invariant 8 — memory/math primitives and port symbols pass, anything OS-shaped means a boundary leak to fix *now* — then commit the reviewed allowlist with a comment per line-group. Never seed the allowlist from output unread; that would launder today's leak into tomorrow's baseline. Expect compiler-runtime helpers to appear per leg (e.g. stack-probe/ssp symbols); admit them named, not globbed [CC-FACT — the dump itself is the authoritative spelling]. Dump format [MEASURED 2026-08-12, same fixture]:

```
UNDEF VirtualLock members=core_bit.o
UNDEF art_port_read_clock members=core_bit.o
UNDEF memcpy members=core_bit.o
UNDEF sinf members=core_bit.o
symbol-audit: lib=libcore_bit.a undefined=4 (dump mode)
```

  Reading that dump per the ritual: `memcpy`/`sinf` → allowlist (primitives; libm nuance in G3); `art_port_read_clock` → allowlist via the port prefix; `VirtualLock` → a Windows import inside core — a real boundary leak; the fix is a port, never an allowlist row. *(build-catchable thereafter; the review itself contract-only)*

### Wiring

Both scripts run inside `./check.sh audits` (G2): include audit always; symbol audit once `CHECK_CORE_LIB` and the allowlist exist (until then it prints `GATE-NOT-WIRED gate=symbol-audit …` — flip it during bring-up, G8 rule 1). CI gets them via `./check.sh --all` on both legs (G5); the audits are leg-independent text/object checks, so two-leg runs are redundancy, not coverage — kept anyway because they are cheap [OPEN — ASSUMED].

The two grammar regexes above are the single source for any CI annotator or log parser — new audits (the map-file script, the bench compare) adopt the same `VIOLATION [<RULE-ID>]` / `GATE-FAIL key=value` shapes rather than inventing a third format, so the agent-side parser stays one function [OPEN — ASSUMED, house convention]. Machine-readable failure formats are the package doctrine, not a nicety: the artifact is the interface between a failed run and the patch (reference/error_tracing_contract_manifest.md section E1).
