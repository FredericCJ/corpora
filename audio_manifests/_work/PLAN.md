# audio-rt-ground — build plan (2026-08-12)

Package: `E:\dev\corpora\audio_manifests\` = **audio-rt-ground** — knowledge database for a coding
agent implementing real-time audio processing on Linux/Windows NT with clang/LLVM (MSYS2 CLANG64 on
Windows). Fulfils the child booklet's §16.3 declaration (this IS the family's version-hub package).
Model: `manifests/` (python-agent-ground) format — AGENTS.md + cards/ + reference/ + config/ +
adapters/ + INDEX.json + _work/.

**Doctrine (the user's commission): testability + traceability as the agent's feedback loop** —
error traces, logs, and test reports must tell the coding agent exactly what failed and how, so it
can patch. Every failure artifact is machine-readable, self-locating, and routed.

## Sources of truth
- Reasoning root: `E:\dev\corpora\realtime-audio-pc-architecture-and-design-r1.md` (child booklet
  r1.0; 17 ch, 20 invariants, DT-1..7). Package cites it, never re-argues.
- Format exemplar: `manifests/` (AGENTS.md, cards/diagnose-runtime.md, config/check.sh,
  adapters/claude-code/SKILL.md, INDEX.json) — read 2026-08-12.
- MEASURED battery (this machine, clang 22.1.8 CLANG64, 2026-08-12): poison pragma works;
  -Wl,--wrap=malloc works (wraps CRT-internal allocs too); -Rpass=loop-vectorize remark "width: 8,
  interleaved: 4" at -O3 -march=x86-64-v3; C17 stdatomic+_Alignas(64) ok; FTZ/DAZ via
  _MM_SET_FLUSH_ZERO_MODE+_MM_SET_DENORMALS_ZERO_MODE → MXCSR=0x9fc0; AvSetMmThreadCharacteristicsW
  L"Pro Audio" grants (handle+index) with -lavrt; WASAPI headers compile in C (COBJMACROS/CINTERFACE,
  IMMDeviceEnumerator + IAudioClient3 macros); VirtualLock=1 after SetProcessWorkingSetSizeEx raise;
  ASan links+runs; UBSan message format captured; llvm-mca -mcpu=alderlake works (dispatch width 6);
  llvm-nm works; pacman has mingw-w64-clang-x86_64-cmake 4.3.4-1 + ninja 1.13.2-1 (NOT installed).

## Layout + section-id scheme
reference/ (13): audio_platform_baseline (H1-9, THE HUB) · toolchain_build (B1-11) ·
rt_plane_rules (R1-8) · concurrency_channels (C1-9) · device_adapter (D1-9) ·
testing_verification (T1-13) · error_tracing_contract (E1-10) · observability_flightring (O1-9) ·
memory_residency (M1-8) · dsp_kernel_patterns (K1-8) · optimization_microarch (P1-10) ·
quality_gates_ci (G1-9) · booklet_map (no §s; I write).
cards/ (13): start-project, build-and-flags, write-dsp-kernel, write-rt-code, concurrency-channels,
device-adapters, write-tests, diagnose-failure, handle-errors, observability, optimize-performance,
gates-and-ci, review-code.
config/: toolchain-clang64-windows.cmake, toolchain-linux-clang.cmake, CMakePresets.json,
.clang-format, .clang-tidy, rt_prelude_poison.h, check.sh, ci-github.yml, session_report.schema.json,
audit_includes.py, audit_symbols.py.
adapters/claude-code/SKILL.md (name: audio-rt-ground). AGENTS.md + README.md + INDEX.json: me.
Tags: ESTABLISHED/VERSION-DEPENDENT(→hub §Hx)/MEASURED(cmd+date)/OPEN(ASSUMED|NEEDS-INPUT)/
FLAGGED-SECONDARY/UNVERIFIED/CC-FACT. Routes: the booklet's seven (compiler/analysis/build/
host-test/target-test/runtime-catchable, contract-only).

## Phases
1. DONE measure battery + exemplar extraction.
2. WF1: 14 writers (12 reference+config, 2 card batches) → files on disk.
3. Me: AGENTS.md, README.md, booklet_map.md, _work/build_index.py → INDEX.json, _work/audit.py → run.
4. WF2: verifiers — mechanical audit, RT/concurrency adversarial, toolchain runnability (RUNS the
   package's commands), booklet-consistency, navigation drill (implement-an-op), traceability drill
   (failing-artifact→patch walk).
5. Adjudicate, fix, reseal (audit CLEAN), RESUME_STATE, memory. NO commit unless asked.
