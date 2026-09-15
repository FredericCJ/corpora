# audio-rt-ground — endeavour state

**Status 2026-08-12: COMPLETE, SEALED, NOT COMMITTED** (house rule: commit only on request).
Built by two workflows + inline authoring; verified by a 4-agent end-result pass; all 39
verification findings applied by a fixer agent; mechanical audit CLEAN.

## The package

`E:\dev\corpora\audio_manifests\` = **audio-rt-ground** (~1 MB): knowledge database for coding
agents implementing real-time audio in C17 on Linux/Windows NT, clang/LLVM + MSYS2 CLANG64.
Fulfils the child booklet's §16.3 `audio_manifests/` declaration. Doctrine: testability +
traceability as the agent's feedback loop (failure artifacts self-locating, machine-parseable;
the failure→patch loop is package law, AGENTS.md + cards/diagnose-failure.md).

- AGENTS.md (20 non-negotiables, 7 routes, tag protocol, router) · README · INDEX.json (693
  sections) · adapters/claude-code/SKILL.md (name: audio-rt-ground)
- reference/ 13 manifests, dictated section ids: hub H1-9 (version hub, MEASURED rows) ·
  toolchain B1-11 · rt-rules R1-8 · concurrency C1-9 (impls survived full memory-model
  adversarial review) · device D1-9 · testing T1-13 (TESTFAIL v1 grammar) · error-tracing E1-10
  (CHECK-FAIL grammar, failure→patch loop) · observability O1-9 (event registry, 56-byte
  fr_event) · memory M1-8 · kernels K1-8 (biquad walkthrough) · optimization P1-10 · gates G1-9
  · booklet_map
- cards/ 13 task cards · config/ 12 artifacts (check.sh [preset+printf bugs fixed, functionally
  verified], CMakePresets.json [+linux-tsan], toolchains ×2, .clang-format, .clang-tidy [330
  checks verified], rt_prelude_poison.h [compile-verified], ci-github.yml,
  session_report.schema.json [schema-validated], audit_includes.py + audit_symbols.py
  [fixture-verified byte-for-byte], .gitattributes [LF for *.sh])

## Gates (run before any commit)

`python _work/build_index.py` → `python _work/audit.py` → CLEAN (last run: 29 files, 585
pointers, 693 sections, CLEAN). Plus: `sh -n config/check.sh`, JSON parses.

## Build history

WF1 `wf_3c34a31a-e92`: 14 fable writers (~1.8M tok); 13 returned, gates writer completed files
but died at final return on session token limit. WF2 `wf_0620e1c1-133`: 4 verifiers per the
user's cheapest-able directive (3 sonnet + 1 fable adversarial; ~1.4M tok) → 39 findings
(11 critical / 14 major / 14 minor) + long survived-list (SPSC wraparound math, generation
reclaim, mailbox ownership, seqlock fences, eventcount wake protocol, WASAPI init dance, PGO
cycle, audit-script fixtures — all attacks failed). Fixer (sonnet, ~370k tok) applied 39/39,
reconciled the one conflicting pair (kept LEG + added PRESET_LEG; SAN_PRESET→cfg-test,
+linux-tsan), extended same-defect fixes to unquoted occurrences, resealed CLEAN.

Headline defects caught & fixed: check.sh preset names (windows-* vs win-*) + printf leading-
dash bug (both first-run fatal); E3-4 id-space model rewritten to O2's distinct-spaces; E5
fault verbs re-keyed to D1/D8's three port verbs; G4 remark gate rewritten for the measured
ThinLTO silence (link-time AUDIO_LTO_REMARK_LDFLAGS, dual-shape grep); D1 teardown order
(join before release — use-after-free); R7/R2 vs C7 worker-park doctrine carve-out; seqlock
plane direction R6(d)/R3.2 aligned to C5; M7 stack painting made real (paint parameter); ~60
OPEN(ASSUMED/NEEDS-INPUT) product decisions remain tagged in-file by design.

## If resuming / extending

Next moves (not requested): commit (on user request only — package + booklet r1.0 are both
uncommitted); vendor into a real project (E:\dev\audio is the natural consumer: copy config/,
follow cards/start-project.md); the ~60 OPEN rows want product decisions; periodic hub H9
re-check triggers (clang major, pacman -Syu); a future corpus pass could promote the booklet's
external register into work records. User directive on record (memory:
workflow-dispatch-economy): dynamic workflows dispatch cheapest-able models; verify end result.
