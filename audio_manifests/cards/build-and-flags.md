# Card: build and flags

**Every TU gets its flags from its declared class × configuration; nobody flags ad hoc.**

Facts verified 2026-08-12. Version-dependent claims route to reference/audio_platform_baseline_manifest.md (the hub); if any file disagrees with the hub, the hub wins.
Reasoning root: the child booklet `realtime-audio-pc-architecture-and-design-r1.md` (repo root). This card operationalizes it; it never re-argues it.

**Load when:** adding a translation unit, choosing a preset, changing any flag, a build breaks, or a toolchain bump is proposed.
**Depth:** reference/toolchain_build_manifest.md. Environment and package versions: the hub. Kernels' flag consequences: cards/write-dsp-kernel.md.

## The standard this card serves

**Flags are the law of the build: one canon table, owned in the per-leg toolchain files, organized by TU class × configuration, every cross-leg deviation its own dated row** (route: build-catchable end to end) [ESTABLISHED: booklet section 10.2].

## The four TU classes

Adding a TU = declaring its class. The class decides its flags; the file never does [ESTABLISHED: booklet section 10.2].

| class | contents | the rules |
|---|---|---|
| `core-kernel` | hot DSP kernels | `-O3`, ISA floor `-march=x86-64-v3`, vectorize remarks wired, **no value-changing math relaxations** |
| `core` | graph compiler, schedule executor, parameter system | `-O2`; OS-free (invariant 8) |
| `shell-adapter` | shell, OS adapters | `-O2`; OS headers allowed |
| `test-tool` | tests, tools, harnesses | `-O2` + instrumentation freedom |

RT-class TUs additionally get config/rt_prelude_poison.h force-included by the build system (route: compiler-catchable) [ESTABLISHED: booklet section 15.2]. Everywhere-flags, both legs: `-std=c17`, the promoted warning canon with `-Werror`, `-ffp-contract=fast`, `-fvisibility=hidden`, `-ffunction-sections -fdata-sections`, debug info always generated [ESTABLISHED: booklet section 10.2]. Exact spellings live in config/toolchain-clang64-windows.cmake and config/toolchain-linux-clang.cmake; the hub dates them.

## Which preset when

| you are | configuration | notes |
|---|---|---|
| editing / daily loop | `dev` | `-O1 -g`, asserts + RT guards on — the guard trapping you is the feedback loop working [ESTABLISHED: booklet section 10.2, 15.2] |
| running suites | `test` | `-O2 -g`, asserts on; ASan+UBSan variants run on both legs [MEASURED 2026-08-12: `-fsanitize=address` links+runs clean on CLANG64; UBSan prints file:line + SUMMARY]; TSan variant exists **only on the Linux leg** [MEASURED 2026-08-12: no tsan runtime in CLANG64 clang libs] |
| measuring / profiling | `perf` | ship's optimization + profiling hooks; bench protocol: reference/optimization_microarch_manifest.md section P2 |
| releasing | `ship` | `-O3` + ThinLTO + PGO, guards compiled out, poison headers stay [ESTABLISHED: booklet sections 10.2–10.3, 15.2] |

Preset ids: read config/CMakePresets.json; never guess [OPEN ASSUMED: `<leg>-<config>` scheme — reference/toolchain_build_manifest.md section B5 is normative].

## Adding a TU — the whole procedure

1. Name its class (table above). If you cannot, the file is mixing planes — split it.
2. Add it to that class's target/source list per reference/toolchain_build_manifest.md section B5. No per-file `COMPILE_OPTIONS`, ever (route: build-catchable).
3. If RT-class: the poison prelude and the RT-TU analysis pack (no recursion, no VLA/alloca, banned families) now apply — see cards/write-rt-code.md (routes: compiler + analysis-catchable) [ESTABLISHED: booklet section 15.1].
4. Build **both** legs before pushing; one-leg compiles are broken builds [ESTABLISHED: booklet ch. 3 invariant 9].

## Changing a flag — the ritual

A kernel that "just needs" one special flag is either a new canon row or a design smell [ESTABLISHED: booklet section 10.2].

1. Propose the row against reference/toolchain_build_manifest.md section B2 (canon) or B4 (per-leg deviation), with the measurement or defect that motivates it.
2. Review, date, land it in the toolchain file(s) — never inline in a target, never in a source pragma.
3. Re-run what the flag can invalidate: remark gates (B8), bench baselines (P2), golden masters if any FP-relevant flag moved (reference/testing_verification_manifest.md section T4).

## Remark gates — what you watch

Hot kernels compile with vectorization remarks wired; the gate fails the build when a listed kernel silently de-vectorizes [ESTABLISHED: booklet ch. 3 invariant 15]. Reference remark, healthy kernel: `clang -c -O3 -march=x86-64-v3 -Rpass=loop-vectorize` on a restrict-qualified float saxpy → `remark: vectorized loop (vectorization width: 8, interleaved count: 4)` [MEASURED 2026-08-12]. Wiring: reference/toolchain_build_manifest.md section B8; kernel-side duties: cards/write-dsp-kernel.md.

## Build breaks — first moves

Full table: reference/toolchain_build_manifest.md section B11.

| symptom | meaning | move |
|---|---|---|
| `attempt to use a poisoned identifier` | you called a banned symbol in an RT TU [MEASURED 2026-08-12: exact clang text] | move the work off-plane or through a channel — never weaken the poison list |
| sanitizer runtime unresolved | wrong environment or preset | CLANG64 ships the ASan dynamic runtime in `clang64/bin` on PATH [MEASURED 2026-08-12]; TSan does not exist on this leg — use the Linux preset |
| CRT/link mismatch, `__imp_` noise | not building inside CLANG64, or a foreign-environment library leaked in | rebuild in CLANG64; audit the library's origin (B11) [ESTABLISHED: booklet section 10.1] |
| remark gate failed | a hot kernel stopped vectorizing | cards/write-dsp-kernel.md; diff the kernel and the flags, not the gate |
| works on one leg only | invariant 9 violation | fix now; the CI matrix will refuse it anyway |

## Reproducing a remark locally

`clang -c -O3 -march=x86-64-v3 -Rpass=loop-vectorize <kernel>.c` shows what vectorized [MEASURED 2026-08-12: that invocation produced the reference remark above]; add `-Rpass-missed=loop-vectorize -Rpass-analysis=loop-vectorize` to see what did not, and why [CC-FACT: clang remark-flag family — the gate's exact invocation is owned by reference/toolchain_build_manifest.md section B8]. Judge against the healthy reference: a width drop (8 → 4) with no flag change is a regression to file, not noise.

## Build identity

Every linked artifact embeds revision + toolchain + flag fingerprint + kernel schema hash, and every session report and crash record carries it [ESTABLISHED: booklet ch. 3 invariant 17] — the provenance half of the doctrine: a failure artifact that cannot name its build cannot be patched against. Mechanics: reference/toolchain_build_manifest.md section B10. Ship links archive their map file and split DWARF (B9); `llvm-nm`/`llvm-objdump` are present for symbol and section inspection [MEASURED 2026-08-12: pacman -Q].

## Toolchain bump — the ritual

A new clang major (or OS baseline) advances the hub row only **after** re-running the remark gates, the bench suite, and the full golden-exact matrix [ESTABLISHED: booklet sections 10.2, 14.6]. Triggers and checklist: reference/audio_platform_baseline_manifest.md section H9; cadence: reference/testing_verification_manifest.md section T12. Budget the bump as a change like any other — it owes T11's suites.

## Never

- Per-file or per-directory flag overrides; flags come from the class (route: build-catchable).
- Any value-changing fast-math in `core`/`core-kernel`: `-ffast-math`, `-funsafe-math-optimizations`, `-ffinite-math-only`, `-fassociative-math` — each breaks determinism or the NaN semantics the regime relies on [ESTABLISHED: booklet section 9.6].
- Raising the ISA floor above `x86-64-v3`; wider tiers are dispatch entries, not flags [ESTABLISHED: booklet section 9.7].
- Disabling a warning locally without a deviation record (reference/toolchain_build_manifest.md section B3).
- Turning off `-Werror` "temporarily".
- Letting the legs' flags drift except through a dated B4 row.
- Trusting any remark, bench, or golden result across a flag or toolchain change you did not re-run.

## Decisions you must not invent

- The warning canon's exact member list — owned by reference/toolchain_build_manifest.md section B3 and the config artifacts; never extend it inline [OPEN ASSUMED: canon as shipped in config/].
- Ship-build assert policy (keep, strip, or field-assert subset) — [OPEN NEEDS-INPUT; booklet section 10.2 defers to the parent's field-assert policy].
- Per-leg hardening rows (ELF relro set, PE hardening set) — deployment policy [OPEN NEEDS-INPUT].
- Fat-LTO experiments — Thin is the default; fat is a measured per-release experiment [OPEN ASSUMED per booklet section 10.3].
- PGO profile corpus contents — [OPEN NEEDS-INPUT; the corpus is versioned and its representativeness is a reviewed claim, booklet section 10.5].

## What you owe when done

Any build-system or flag change owes: both legs building at the full canon, the remark-gate output for the hot-kernel list attached (unchanged, or changed with the measurement that justifies it), bench baselines re-validated if optimization-relevant, goldens re-run if FP-relevant — that is this change type's row in reference/testing_verification_manifest.md section T11 — and the gate ledger of reference/quality_gates_ci_manifest.md section G1 stays whole via config/check.sh. A flag change with no re-run evidence is an unverified claim wearing a commit message.

## Go deeper

| question | where |
|---|---|
| TU classes and configuration model, normatively | reference/toolchain_build_manifest.md section B1 |
| the flag canon table, exact spellings | reference/toolchain_build_manifest.md section B2 |
| warning canon | reference/toolchain_build_manifest.md section B3 |
| per-leg rows and parity policing | reference/toolchain_build_manifest.md section B4 |
| ThinLTO, PGO workflow | reference/toolchain_build_manifest.md sections B6, B7 |
| remark-gate wiring | reference/toolchain_build_manifest.md section B8; reference/quality_gates_ci_manifest.md section G4 |
| linking, static policy, map files | reference/toolchain_build_manifest.md section B9 |
| troubleshooting, exhaustively | reference/toolchain_build_manifest.md section B11 |
| package/version rows, re-check triggers | reference/audio_platform_baseline_manifest.md sections H3, H9 |
