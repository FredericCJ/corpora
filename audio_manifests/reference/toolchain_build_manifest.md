# Toolchain & Build — Ground-Truth Manifest

**Purpose.** The build law of audio-rt-ground: the TU-class × configuration flag model, the exact
flag and warning canons, the two-leg parity rules, CMake+Ninja operation, ThinLTO, PGO, the remark
gates, linking and debug-artifact policy, build identity, and the build-failure → fix table — one
clang/LLVM family on two legs (Windows MSYS2 CLANG64, Linux), C17.

Facts verified 2026-08-12. Version-dependent claims route to
reference/audio_platform_baseline_manifest.md (the hub); if any file disagrees with the hub, the
hub wins.

Reasoning root: the child booklet `realtime-audio-pc-architecture-and-design-r1.md` (repo root).
This file operationalizes booklet ch. 10 (toolchain as a port), sections 5.5–5.6 (one codebase,
compiler port), and 14.6 (toolchain-bump ritual); it never re-argues them.

**Tag legend.** [ESTABLISHED: src] named primary source · [VERSION-DEPENDENT - hub Hn] ·
[MEASURED 2026-08-12] ran on the reference machine, command recorded · [OPEN] project decision
(ASSUMED vs NEEDS-INPUT) · [CC-FACT] model knowledge of API/toolchain mechanics, no primary source
inline · [FLAGGED-SECONDARY] · [UNVERIFIED]. Two MEASURED sources exist: the hub's package battery
(quoted) and **this file's own flag battery** (clang 22.1.8, target `x86_64-w64-windows-gnu`,
CLANG64; commands inline). Untagged factual claims are defects.

**Deferred to siblings, not duplicated.** Package/version rows and install state → hub H2/H3/H4;
sanitizer/BOLT availability → hub H5; ISA floor value → hub H8; bump triggers → hub H9. Gate
wiring and `check.sh` → reference/quality_gates_ci_manifest.md sections G2/G4; structural audits
→ G3; CI matrix → G5. Bench protocol → reference/optimization_microarch_manifest.md section P2;
PGO/BOLT *operations* → P8. Sanitizer test legs → reference/testing_verification_manifest.md
section T8. Where identity surfaces in reports → reference/error_tracing_contract_manifest.md
section E8, reference/observability_flightring_manifest.md section O7. Short forms (G3, T8, H5,
R4, K5, M8, …) always resolve against this map and the hub.

---

## B1. TU classes × configurations — the flag model

Two axes, one matrix, zero exceptions. Every translation unit belongs to exactly one **class**;
every build is exactly one **configuration**; a TU's flags are the pure function
`flags(class, config, leg)` — nothing else contributes. [ESTABLISHED: booklet section 10.2]

### The four TU classes

| class | contents (directory law, booklet section 5.5) | what the class buys | may include |
|---|---|---|---|
| `core-kernel` | `core/kernels/**` — DSP inner loops, the schedule executor's hot path | `-O3`, ISA floor, remark gates (B8) | `core/`, `ports/`, compiler port only |
| `core` | rest of `core/**`, `ports/**` — graph compiler, parameter system, channels | `-O2`, full determinism rows | `core/`, `ports/`, compiler port only |
| `shell-adapter` | `adapters/**`, `shell/**` — ALSA/WASAPI, thread/clock/residency adapters, composition root | `-O2`; the only class that may include OS headers | ports + its own leg's OS headers |
| `test-tool` | `test/**`, `tools/**` — suites, offline renderer, bench harness | `-O2` + instrumentation freedom (sanitizers, coverage, profiling) | anything |

Class membership is a **target property, set from the directory**: one CMake target never mixes
classes; `AUDIO_TU_CLASS` names it per target and B5 shows the consuming mechanics.
[OPEN ASSUMED: property name is this package's convention; the model itself is booklet law]

### The four configurations

| config | intent | optimization | asserts | RT guards (reference/rt_plane_rules_manifest.md section R4) | LTO/PGO |
|---|---|---|---|---|---|
| `dev` | edit-compile-run speed | `-O1` all classes | on | on | off |
| `test` | the host suite's build | `-O2` all classes | on | on | off; sanitizer legs ride here (T8, hub H5) |
| `perf` | bench + profiling truth | class levels (kernels `-O3`, rest `-O2`) | field-policy [OPEN] | off | ThinLTO; PGO when profile present |
| `ship` | the artifact | class levels | field-policy [OPEN NEEDS-INPUT] | compiled out | ThinLTO + PGO |

[ESTABLISHED: booklet section 10.2 — "perf: ship's optimization plus profiling hooks"]

### Rules

| RULE | route | tag |
|---|---|---|
| **Nobody flags ad hoc.** A TU's flags come from its class row; a kernel that "just needs" one special flag is a new canon row (reviewed, dated) or a design smell | build-catchable — G3 audits `compile_commands.json` against the canon (`CMAKE_EXPORT_COMPILE_COMMANDS=ON` is in every preset) | [ESTABLISHED: booklet section 10.2] |
| A target that cannot name its class does not build; class comes from directory, never from a per-file override | build-catchable — CMakeLists refuses targets without `AUDIO_TU_CLASS` | [OPEN ASSUMED: enforcement spelling] |
| OS headers outside `shell-adapter` fail the include audit | build-catchable — config/audit_includes.py per booklet section 15.3 | [ESTABLISHED: booklet sections 5.5, 15.3] |
| Bare `__attribute__`/`__builtin` outside the compiler-port header fails the extension audit | analysis-catchable — grep audit in config/check.sh (G3) | [ESTABLISHED: booklet section 5.6] |

---

## B2. The flag canon

Exact spellings. Presets carry these as cache strings (config/CMakePresets.json); this section is
the law the presets transcribe.

### The everywhere row — all classes, all configs, both legs

| flag | why (one clause) | tag |
|---|---|---|
| `-std=c17` | language pin | [MEASURED 2026-08-12: flag battery below] |
| warning canon of B3 + `-Werror` | one warning law, promoted | [MEASURED 2026-08-12] |
| `-g` | debug info always generated; split/archived per B9 | [MEASURED 2026-08-12] |
| `-march=x86-64-v3` | ISA floor; the floor **value** is the hub's | [MEASURED 2026-08-12] compile+vectorize; value [VERSION-DEPENDENT - hub H8] |
| `-ffp-contract=fast` | contraction pinned on, both legs, identically — FMA is the class's arithmetic advantage; last-ulp difference vs a no-FMA build is documented and harmless because it is pinned inside the golden-master conditions | [ESTABLISHED: booklet section 9.6]; compiles [MEASURED 2026-08-12] |
| `-fvisibility=hidden` | export nothing by default (B9) | [MEASURED 2026-08-12] |
| `-ffunction-sections -fdata-sections` | per-symbol sections: `--gc-sections`, layout control, map-file audits | [MEASURED 2026-08-12] |
| link: `-fuse-ld=lld` | one linker family both legs (B9) | [MEASURED 2026-08-12] |
| link: `-Wl,--gc-sections` | drop unreferenced sections | [MEASURED 2026-08-12] |

Scope note: putting the ISA floor and contraction on **every** class and config keeps numerics
config-invariant — a `dev` render and a `ship` render disagree only where optimization level
legally reorders nothing; golden masters stay comparable across configs. [OPEN ASSUMED: booklet
section 10.2 names the floor only on the kernel row; extending it everywhere is this package's
reading, consistent with booklet section 9.6's "pinned globally" contraction rule]

The flag battery (this file's own; every row above rode one of these two commands):

```
clang -std=c17 -fsyntax-only -Werror=unknown-warning-option -Wall -Wextra -Wconversion \
  -Wsign-conversion -Wshadow -Wdouble-promotion -Wfloat-conversion -Wimplicit-fallthrough \
  -Wvla -Wswitch-enum probe.c                                          # accepted, clean
clang -std=c17 -O3 -march=x86-64-v3 -ffp-contract=fast -fvisibility=hidden \
  -ffunction-sections -fdata-sections -g -flto=thin -fuse-ld=lld \
  -Wl,--gc-sections -Wl,-Map=probe.map probe.c -o probe.exe            # built, ran, map emitted
```

### Class × config matrix (added to the everywhere row)

| class \ config | dev | test | perf | ship |
|---|---|---|---|---|
| `core-kernel` | `-O1` | `-O2` + SAN | `-O3` + REMARK + LTO | `-O3` + REMARK + LTO + PGO |
| `core` | `-O1` | `-O2` + SAN | `-O2` + LTO | `-O2` + LTO + PGO |
| `shell-adapter` | `-O1` | `-O2` + SAN | `-O2` + LTO | `-O2` + LTO + PGO |
| `test-tool` | `-O1` | `-O2` + SAN | `-O2` + LTO | `-O2` + LTO + PGO |

where SAN = `AUDIO_SAN_FLAGS` (`-fsanitize=address,undefined` default — [MEASURED 2026-08-12:
hub battery, both link and run clean on CLANG64]; the Linux TSan lane overrides — hub H5, T8);
REMARK = B8's kernel remark rows; LTO = `-flto=thin` (B6); PGO = `-fprofile-use=` (B7). Sanitizer
flags must appear at compile **and** link [CC-FACT]. CI failure hygiene: add
`-fno-sanitize-recover=all` on sanitizer lanes so UBSan halts instead of printing-and-continuing
[CC-FACT verify-before-use; default UBSan behavior observed print-and-continue in the hub battery].

### Per-leg rows — the only flag divergence allowed (B4)

| leg | row | why | tag |
|---|---|---|---|
| Linux compile | `-fno-plt` | direct calls to DSO-external functions; pairs with now-binding | [CC-FACT; ESTABLISHED intent: booklet section 10.2] |
| Linux link | `-Wl,-z,relro -Wl,-z,now` | ELF hardening + eager binding (no lazy-PLT fault on the RT path) | [CC-FACT; ESTABLISHED intent: booklet sections 10.2, 8.1] |
| Windows | configure-time triple assertion `x86_64-w64-windows-gnu` + CLANG64-shell guard | refuse mixed environments / wrong CRT | [MEASURED 2026-08-12: `clang -print-target-triple` → `x86_64-w64-windows-gnu`; guard in config/toolchain-clang64-windows.cmake] |
| Windows | UCRT is the CRT; winpthreads present | CLANG64 baseline | [MEASURED 2026-08-12: hub battery, pacman -Q — versions are hub H3 rows] |

A Linux row leaking into the Windows leg is caught by the canon itself:
`clang: error: argument unused during compilation: '-fno-plt' [-Werror,-Wunused-command-line-argument]`
[MEASURED 2026-08-12: `clang -std=c17 -c -fno-plt -Werror probe.c` on the Windows leg → exit 1].
Route: compiler-catchable.

### Never — banned flags in `core` and `core-kernel`

| never | why | route | tag |
|---|---|---|---|
| `-ffast-math`, `-Ofast` | value-changing relaxations break determinism (invariant 11) and the NaN/Inf semantics the FP regime relies on | build-catchable — G3 greps `compile_commands.json` | [ESTABLISHED: booklet section 9.6] |
| `-fassociative-math`, `-freciprocal-math`, `-ffinite-math-only`, `-funsafe-math-optimizations` | same, piecewise; a wanted reassociation is written into the algebra or granted per-loop (B8) | build-catchable | [ESTABLISHED: booklet section 9.6; flag spellings CC-FACT] |
| `-march=native` | binary's ISA becomes machine-of-the-day; floor is pinned (hub H8) | build-catchable | [CC-FACT flag; ESTABLISHED intent: booklet section 1.2] |
| `-DNDEBUG` via CMake build-type defaults | assert policy is a canon row, not a CMake side effect; custom build types Dev/Test/Perf/Ship keep CMake's per-type defaults empty | build-catchable | [CC-FACT: CMake defines `CMAKE_C_FLAGS_<TYPE>` only for its known types] |
| per-file `COMPILE_OPTIONS` overrides | B1's first rule | build-catchable — G3 | [ESTABLISHED: booklet section 10.2] |
| inline assembly | intrinsics keep the compiler's scheduler and the analyzers' eyes open | analysis-catchable — grep audit | [ESTABLISHED: booklet section 9.7] |

Shell/control-plane TUs may take relaxed-math rows only as a **new documented canon row with a
measurement attached** — that is a canon amendment, not a flag. [ESTABLISHED: booklet section 9.6]

### Canon governance

| RULE | route | tag |
|---|---|---|
| The canon lives in exactly two artifacts — config/CMakePresets.json (values) and this file (law + tags); a disagreement between them is a build defect | build-catchable — G3 diffs presets against this section | [OPEN ASSUMED: house convention] |
| **The canon is diffed per toolchain bump**: new clang major or OS baseline re-runs remark gates, bench suite, golden masters (full exact matrix) *before* the hub row advances | build-catchable end to end | [ESTABLISHED: booklet sections 10.2, 14.6; triggers live in hub H9] |
| Flag-hash of the resolved canon is embedded in every binary (B10) so an artifact can prove which canon built it | build-catchable + host-test-catchable | [OPEN ASSUMED: mechanism this package's] |

---

## B3. The warning canon

### The list — explicit, promoted, identical on both legs

All ten accepted in one invocation with `-Werror=unknown-warning-option`
[MEASURED 2026-08-12: first flag-battery command in B2].

| flag | catches (one clause) | tag |
|---|---|---|
| `-Wall -Wextra` | the base set; never assumed sufficient alone | [MEASURED 2026-08-12] |
| `-Wconversion` | implicit narrowing/value-changing conversions — sample/index arithmetic | [MEASURED 2026-08-12] |
| `-Wsign-conversion` | signed↔unsigned implicit conversion (listed explicitly; do not rely on group membership) | [MEASURED 2026-08-12] |
| `-Wshadow` | inner declaration hides outer — state-struct fields vs locals in kernels | [MEASURED 2026-08-12] |
| `-Wdouble-promotion` | silent `float`→`double` promotion — kills lanes and doubles bandwidth on the stream path (booklet section 9.6 width policy) | [MEASURED 2026-08-12] |
| `-Wfloat-conversion` | implicit `double`→`float` truncation | [MEASURED 2026-08-12] |
| `-Wimplicit-fallthrough` | unannotated switch fallthrough — dispatch switches | [MEASURED 2026-08-12] |
| `-Wvla` | variable-length arrays — unbounded RT stack use (memory M7) | [MEASURED 2026-08-12] |
| `-Wswitch-enum` | switch over enum missing a case even with `default:` — op-kind and fault-verb switches stay total | [MEASURED 2026-08-12] |
| `-Werror` | the promotion; also promotes **driver** warnings (see the `-fno-plt` measurement, B2) | [MEASURED 2026-08-12] |

### Suppression hygiene

| RULE | route | tag |
|---|---|---|
| Suppression is a **local pragma pair with an inline justification**; never a global or per-target `-Wno-*`, never a canon edit to dodge one site | analysis-catchable — check.sh greps for `clang diagnostic ignored` lacking a `JUSTIF:` tail (G2) | [OPEN ASSUMED: house convention; pragma mechanics CC-FACT] |
| Vendored/third-party headers are demoted with `-isystem`, not with `-Wno-*` | build-catchable | [CC-FACT] |

```c
/* the only sanctioned shape: */
#pragma clang diagnostic push
#pragma clang diagnostic ignored "-Wdouble-promotion" /* JUSTIF: varargs printf promotes; log-only TU */
  log_write("gain=%f", g);
#pragma clang diagnostic pop
```

### Candidate extensions — not yet canon [OPEN NEEDS-INPUT]

`-Wmissing-prototypes` (extern function without prior prototype — API hygiene),
`-Wstrict-prototypes` (K&R declarations), `-Wundef` (undefined macro in `#if`), `-Wcast-qual`,
`-Wpointer-arith` — all [CC-FACT, not battery-verified this session]. Adoption check, one line
per flag: `clang -std=c17 -fsyntax-only -Werror=unknown-warning-option -W<flag> probe.c`.
Adopting any of them is a canon amendment (B2 governance).

---

## B4. Per-leg parity

### The parity table — what MAY differ, and nothing else

| may differ | exactly what | documented where |
|---|---|---|
| adapter TU sets | `adapters/alsa/`+`adapters/posix/` vs `adapters/wasapi/`+`adapters/win32/` | booklet section 5.5; reference/device_adapter_manifest.md sections D2/D5 |
| per-leg flag rows | the B2 per-leg table, only | B2; presets `AUDIO_FLAGS_LEG`/`AUDIO_LDFLAGS_LEG` |
| verification-tool availability | TSan Linux-only; BOLT Linux-only; everything else both legs | [MEASURED 2026-08-12: hub battery] — hub H5 |
| nothing else | sources, canon, warning law, linker, C standard, block quantum, golden masters: identical | booklet section 5.5 |

| RULE | route | tag |
|---|---|---|
| A change that compiles on one leg only is a **broken build**, not a porting task for later; CI builds and tests both legs per commit | build-catchable — G5 matrix | [ESTABLISHED: booklet sections 5.5, 14.6] |
| Cross-leg **exact** golden comparison runs per merge (one leg renders, the other byte-compares) | host-test-catchable — G6 | [ESTABLISHED: booklet section 14.6] |

### Environment purity — Windows leg

The leg builds **in CLANG64**: its toolchain, its UCRT headers and import libraries; mixing MSYS2
subsystems (MINGW64/UCRT64/MSYS) or MSVC objects is the ecosystem's classic self-inflicted wound.
[ESTABLISHED: booklet section 10.1] Enforced twice at configure time
(config/toolchain-clang64-windows.cmake): `MSYSTEM` must equal `CLANG64`, and
`clang -print-target-triple` must equal `x86_64-w64-windows-gnu` [MEASURED 2026-08-12]. Route:
build-catchable.

Purity check, run when anything smells wrong:

```
echo $MSYSTEM                 # CLANG64
which clang cmake ninja       # every hit under /clang64/bin
clang -print-target-triple    # x86_64-w64-windows-gnu   [MEASURED 2026-08-12]
pacman -Qs mingw-w64-clang-x86_64- | head   # the package set; versions are hub H3 rows
```

Paths: Windows spelling `C:/msys64/clang64/bin/...`, POSIX-in-shell spelling `/clang64/bin/...` —
same binaries. CMake and toolchain files use the Windows spelling. [MEASURED 2026-08-12: compiler
invoked as `C:\msys64\clang64\bin\clang.exe` throughout the battery]

### Environment purity — Linux leg

Same family, same major as the Windows leg; the hub pins source and floor (H4)
[ESTABLISHED: booklet section 10.1]. The toolchain file asserts
`x86_64-<vendor>-linux-gnu` and forces lld; deployment replaces the skeleton's PATH-`clang` with
an absolute versioned pin [OPEN NEEDS-INPUT: distro clang vs upstream; hub H4 owns the answer].
Not battery-verified on a Linux host this session [UNVERIFIED on-host; hub H9 re-check row].

---

## B5. CMake + Ninja

### Install — Windows leg

```
pacman -S mingw-w64-clang-x86_64-cmake mingw-w64-clang-x86_64-ninja
```

[MEASURED 2026-08-12: hub battery — repo has cmake 4.3.4-1 and ninja 1.13.2-1; **NOT currently
installed** on the reference machine. Versions are hub H3 rows.] Never install a differently
prefixed cmake/ninja into this leg — B4 purity. Linux leg: distro/upstream cmake ≥ 3.25 (presets
schema v6) [CC-FACT].

### The presets model — config/CMakePresets.json

Eight concrete configurePresets = leg × config, composed from hidden building blocks
(conflict-free by construction; on conflicts, earlier `inherits` entries win [CC-FACT]):

| hidden preset | contributes |
|---|---|
| `base` | Ninja generator, `build/${presetName}` binary dir, `CMAKE_EXPORT_COMPILE_COMMANDS=ON`, `AUDIO_FLAGS_COMMON`, `AUDIO_LDFLAGS_COMMON` |
| `leg-windows` / `leg-linux` | `toolchainFile` binding (config/toolchain-clang64-windows.cmake / config/toolchain-linux-clang.cmake), host-OS condition, `AUDIO_LEG`, per-leg flag rows |
| `cfg-dev` / `cfg-test` / `cfg-perf` / `cfg-ship` | `CMAKE_BUILD_TYPE` (custom names — see below), `AUDIO_CONFIG`, the class flag strings, SAN/LTO/PGO/guards/asserts knobs |

Concrete: `win-dev win-test win-perf win-ship linux-dev linux-test linux-perf linux-ship`, plus
matching buildPresets and testPresets (JSON validated 2026-08-12: 15 configure / 8 build / 8 test
presets parse [MEASURED: `ConvertFrom-Json` round-trip]). The presets file is a **skeleton the
project adapts** — target wiring, PGO paths, sanitizer-lane overrides are project decisions
[OPEN].

### Commands — from a CLANG64 shell (Windows) or any shell (Linux), repo root

```
cmake --preset win-dev            # configure
cmake --build --preset win-dev    # build
ctest --preset win-test           # run the suite (outputOnFailure preset-pinned)
cmake --list-presets              # what exists on this host (condition-filtered)
```

[CC-FACT: cmake/ctest `--preset` command forms — could not be MEASURED this session because
cmake is not installed (hub row); first install runs these once and upgrades this tag — hub H9
re-check trigger.]

### How CMakeLists consumes the flag variables

```cmake
# per target, from its class (B1); the ONLY place flags attach to targets
separate_arguments(_kflags NATIVE_COMMAND
  "${AUDIO_FLAGS_COMMON} ${AUDIO_FLAGS_LEG} ${AUDIO_FLAGS_CORE_KERNEL} \
   ${AUDIO_KERNEL_REMARK_FLAGS} ${AUDIO_SAN_FLAGS}")
target_compile_options(core_kernels PRIVATE ${_kflags})
if(AUDIO_LTO STREQUAL "thin")
  target_compile_options(core_kernels PRIVATE -flto=thin)
  target_link_options(product_exe PRIVATE -flto=thin)
endif()
separate_arguments(_ldflags NATIVE_COMMAND
  "${AUDIO_LDFLAGS_COMMON} ${AUDIO_LDFLAGS_LEG} ${AUDIO_LTO_REMARK_LDFLAGS} ${AUDIO_SAN_FLAGS}")
target_link_options(product_exe PRIVATE ${_ldflags})
```

[CC-FACT: `separate_arguments(... NATIVE_COMMAND ...)` and `target_link_options` mechanics.]
Sanitizer flags reach compile and link both — the snippet is the reason `AUDIO_SAN_FLAGS` appears
twice.

### Build-type mechanics

`CMAKE_BUILD_TYPE` is bound per preset to the **custom** names `Dev`/`Test`/`Perf`/`Ship`:
CMake's built-in types (Debug/Release/...) would inject their own `-O`/`-DNDEBUG` defaults under
the canon's feet; unknown type names have no `CMAKE_C_FLAGS_<TYPE>` defaults, so the AUDIO_*
strings are total [CC-FACT]. NDEBUG/assert policy is therefore a canon decision (B2), never a
CMake side effect.

---

## B6. ThinLTO

On for `perf`/`ship`, both legs, Thin form; fat LTO stays a measured per-release experiment.
[ESTABLISHED: booklet section 10.3]

**What it buys here** (booklet section 10.3, not re-argued): the schedule executor and built-in
kernels fuse — the enum-switch dispatch inlines its small ops, constants propagate across the op
boundary, the block loop's shape survives into the optimizer whole.

| item | exact row | tag |
|---|---|---|
| compile | `-flto=thin` per TU (objects carry bitcode; codegen deferred to link) | [MEASURED 2026-08-12: `clang -c -flto=thin` object linked through the LTO backend; deferral proven by the remark timing measurement in B8]; mechanism [CC-FACT] |
| link | `-flto=thin` on the driver link line; lld runs the ThinLTO backend on both legs | [MEASURED 2026-08-12 Windows leg]; Linux [CC-FACT] |
| incremental cache | `-Wl,--thinlto-cache-dir=build/<preset>/ltocache` | [MEASURED 2026-08-12: cache entries appear, MinGW lld driver]; ELF spelling same [CC-FACT] |
| parallelism | `-Wl,--thinlto-jobs=N` | [CC-FACT verify-before-use] |
| per-ISA kernel TUs (reference/dsp_kernel_patterns_manifest.md section K5, rung 3) | target attributes survive LTO; attribute-carrying functions do not merge across ISA boundaries; init-time dispatch binding unaffected | [ESTABLISHED: booklet section 10.3] |
| PGO | combines with ThinLTO (B7 flags ride the same build) | [CC-FACT] |

| RULE | route | tag |
|---|---|---|
| Bench and remark gates **re-run under LTO** — inlining changes both; a kernel gated only in a non-LTO build is ungated in the artifact | build-catchable (B8's link-time remark rows) + host-test-catchable (bench lane T10) | [ESTABLISHED: booklet section 10.3] |
| LTO stays off in `dev`/`test` (edit-cycle latency; sanitizer-stack legibility) | build-catchable — preset values | [OPEN ASSUMED] |

---

## B7. PGO — IR-level workflow, fed by the offline renderer

The workload is the point: the offline render harness
(reference/testing_verification_manifest.md section T3) drives the real schedule
executor over real sessions at full speed — a deterministic, representative profile by
construction. [ESTABLISHED: booklet section 10.5]

### The workflow — commands measured end to end on the Windows leg

```
# 1. instrumented build (ship flags, PGO flipped to generate)
cmake --preset win-ship -DAUDIO_PGO=generate         # CMakeLists maps to -fprofile-generate
cmake --build --preset win-ship
# 2. run the profile corpus through the offline renderer (no device, full speed)
LLVM_PROFILE_FILE='build/win-ship/pgo/%p.profraw' \
  tools/offline_render --corpus profiles/corpus.lock   # corpus is versioned — rule below
# 3. merge
llvm-profdata merge -o profiles/current.profdata build/win-ship/pgo/*.profraw
# 4. optimized rebuild
cmake --preset win-ship -DAUDIO_PGO=use -DAUDIO_PROFDATA=profiles/current.profdata
cmake --build --preset win-ship
```

[MEASURED 2026-08-12 at flag level: `clang -O3 -fprofile-generate probe.c` → run with
`LLVM_PROFILE_FILE=...%p.profraw` → `llvm-profdata merge -o probe.profdata *.profraw` →
`clang -O3 -fprofile-use=probe.profdata` — full cycle clean on CLANG64. The cmake/tool wrappers
are the package's skeleton, CC-FACT until the project wires them.] `%p` (pid) measured; `%m`
(module signature) also available for multi-process merges [CC-FACT].

### Rules

| RULE | route | tag |
|---|---|---|
| **The profile corpus is versioned with the build system** — which sessions, which parameter sweeps; a stale or toy profile quietly *mis*-lays the binary | build-catchable — corpus lockfile hashed into build identity (B10 `profdata_id`) | [ESTABLISHED: booklet section 10.5] |
| Stale-profile and unprofiled-function diagnostics are promoted on ship CI: `-Werror=profile-instr-out-of-date -Werror=profile-instr-unprofiled` | compiler-catchable | [MEASURED 2026-08-12: both flags accepted on a `-fprofile-use` build] |
| A ship binary built without PGO is legal but must say so in its identity (B10) and release notes | contract-only | [OPEN ASSUMED; skeleton default is `AUDIO_PGO=off` so fresh checkouts build] |
| Which sessions constitute the corpus, refresh cadence | — | [OPEN NEEDS-INPUT] |
| BOLT post-link layout: Linux leg only, absent from CLANG64 | build-catchable — preset has no Windows row to misuse | [MEASURED 2026-08-12: hub battery — llvm-bolt ABSENT on CLANG64]; operations → P8 |

---

## B8. Remark gates

Invariant 15 operationalized: the build fails when a listed hot kernel stops vectorizing.
[ESTABLISHED: booklet sections 9.7, 10.5] Wiring lives in config/check.sh via quality gates G4;
this section pins the flags and the grep anchors.

### Where remarks fire — the LTO timing trap

| build kind | vectorizer runs at | remark row that works | tag |
|---|---|---|---|
| non-LTO (`dev`/`test`, or a dedicated kernel-remark compile) | compile | `-Rpass=loop-vectorize -Rpass-missed=loop-vectorize -Rpass-analysis=loop-vectorize` | [MEASURED 2026-08-12] |
| ThinLTO (`perf`/`ship`) | **link** (LTO backend) — compile-time `-Rpass` is SILENT | `-Wl,-mllvm,-pass-remarks=loop-vectorize -Wl,-mllvm,-pass-remarks-missed=loop-vectorize` on the link line | [MEASURED 2026-08-12: compile with `-flto=thin -Rpass=loop-vectorize` emitted nothing; the link-time row emitted the remark] |

The gate must therefore read the **link** step's stderr on `perf`/`ship` — a compile-scraping
gate silently passes an unvectorized ship kernel. ELF lld accepts the same `-mllvm` pass-through
[CC-FACT verify on the Linux leg — hub H9].

### Output formats — grep anchors (verbatim from the battery)

```
# compile-time (-Rpass), file:line:col prefix, bracketed source:
probe.c:14:3: remark: vectorized loop (vectorization width: 8, interleaved count: 4) [-Rpass=loop-vectorize]
# link-time (-Wl,-mllvm,-pass-remarks), NO "remark:" tag, NO bracket suffix:
probe.c:14:3: vectorized loop (vectorization width: 8, interleaved count: 4)
probe.c:5:3: loop not vectorized
```

[MEASURED 2026-08-12] Gate regex accepts both shapes: match on
`vectorized loop \(vectorization width: <N>` anchored to the kernel's file, and require width ≥
the floor's lane count for `float` (8 at x86-64-v3 [VERSION-DEPENDENT - hub H8]). Machine-readable
alternative: `-fsave-optimization-record -foptimization-record-file=<tu>.opt.yaml` — YAML records
with `Pass`, `Name`, `DebugLoc {File, Line, Column}`, `Function` [MEASURED 2026-08-12] — the
self-locating form (doctrine: the artifact names WHAT/WHERE/WHY); under ThinLTO the YAML route
needs the link-time equivalent [CC-FACT verify: lld `--lto-*` record options differ per driver —
prefer the stderr rows above until verified].

### The FP-reduction lesson — why a kernel "stops vectorizing" with legal code

The canon bans value-changing math (B2), so a float accumulator loop does not auto-vectorize;
the compiler says exactly why, self-locating:

```
probe.c:7:9: remark: loop not vectorized: cannot prove it is safe to reorder floating-point
operations; allow reordering by specifying '#pragma clang loop vectorize(enable)' before the
loop or by providing the compiler option '-ffast-math' [-Rpass-analysis=loop-vectorize]
```

[MEASURED 2026-08-12] The sanctioned fix is the **per-loop pragma** — booklet section 9.7 rung 2,
never the global flag:

```c
float acc = 0.0f;
#pragma clang loop vectorize(enable) /* grants THIS loop reassociation; reason documented here */
for (int i = 0; i < n; ++i)
  acc += x[i] * y[i];
```

[MEASURED 2026-08-12: with the pragma the reduction vectorizes, width 8, interleave 4, no
fast-math flag.] The grant changes this loop's summation order — visible in code, identical on
both legs (one compiler family), inside the golden-master conditions. [ESTABLISHED: booklet
sections 9.6, 9.7]

### Gate wiring

| RULE | route | tag |
|---|---|---|
| The hot-kernel list is a versioned file (`tools/kernels_hot.list`); every listed kernel must produce a vectorized-loop remark in the gated build, else the build fails | build-catchable — G4, config/check.sh | [ESTABLISHED: booklet invariant 15, section 10.5] |
| Remark diffs are CI artifacts per build and re-run per toolchain bump | build-catchable | [ESTABLISHED: booklet sections 10.5, 14.6] |
| A gate failure's artifact is the remark itself — file:line:col plus the vectorizer's reason — enough for the agent to patch without a rerun | (the doctrine, enforced by using `-Rpass-missed`/`-Rpass-analysis` output in the failure message) | [MEASURED format 2026-08-12] |

---

## B9. Linking — lld, static policy, maps, visibility, split debug

### lld and the static policy

| item | row | tag |
|---|---|---|
| linker | lld on both legs, forced by `-fuse-ld=lld` in both toolchain files; one map format, one section-semantics vocabulary | [MEASURED 2026-08-12 Windows: links+runs; hub battery's `--wrap` probe names the lld MinGW driver]; Linux [CC-FACT] |
| product libraries | **static** into the executable: RT path crosses no PLT/IAT, one text region to lock (reference/memory_residency_manifest.md sections M5/M6), one artifact to version | [ESTABLISHED: booklet section 10.4] |
| OS runtimes | UCRT / glibc+loader stay **dynamic**; pinning them is deployment's business | [ESTABLISHED: booklet section 10.4] |
| symbol audit | `llvm-nm` over the linked core library; undefined set must be within the blessed list (CRT math/memory primitives + port symbols; no OS import) | [ESTABLISHED: booklet section 15.3]; llvm-nm present [MEASURED 2026-08-12: hub battery]; script config/audit_symbols.py (G3) |

### Map files

`-Wl,-Map=<target>.map` on every link, archived on ship links.
[MEASURED 2026-08-12: emitted through the MinGW lld driver; header format
`Address  Size  Align Out  In  Symbol`.] Consumers: the map-file audit (section discipline —
RT-hot code/data in their collected sections; booklet section 15.3, G3) and the working-set
budget sanity check (reference/memory_residency_manifest.md section M8). Route: build-catchable.

### Visibility and exports

`-fvisibility=hidden` everywhere (B2) + the executable exports nothing. Explicit export lists
become real only if a shared-library surface ever appears — that seam is OPEN in the booklet
(section 10.4: plugin surfaces are a grandchild's problem); mechanisms when it opens:
ELF `--version-script`, PE `.def`/`__declspec(dllexport)` [CC-FACT]. Until then the enforcement
is the symbol audit above.

### Split debug — DWARF on both legs, lldb the one debugger

`-g` always (B2); ship binaries strip to a sidecar:

```
llvm-objcopy --only-keep-debug app.exe app.dbg
llvm-objcopy --strip-debug app.exe app_stripped.exe
llvm-objcopy --add-gnu-debuglink=app.dbg app_stripped.exe
```

[MEASURED 2026-08-12 on the PE binary: 89,088 B exe → 24,064 B stripped + 73,728 B .dbg; stripped
exe runs.] Linux spelling identical with `objcopy` or `llvm-objcopy` [CC-FACT]. DWARF-in-PE is
the CLANG64 debug format and lldb consumes it (lldb 22.1.8 installed — hub H3)
[CC-FACT format; presence MEASURED 2026-08-12: hub battery]. ELF extra: `-Wl,--build-id`
[CC-FACT].

| RULE | route | tag |
|---|---|---|
| Every ship link archives map + `.dbg` keyed by build identity (B10) — the decoder half of a field crash record, years later | build-catchable — release rung G7 refuses an unarchived ship link | [ESTABLISHED: booklet section 10.4, invariant 17] |

### `--wrap` and link-level guards

`-Wl,--wrap=malloc` works through the lld MinGW driver [MEASURED 2026-08-12: hub battery].
Measured gotcha that shapes the guard (rt_plane_rules R4): `__wrap_malloc` also intercepts
**CRT-internal startup allocations — 3 hits before `main` in a trivial exe** — so the allocation
guard must arm only after the RT plane starts (a flag flipped at plane start), not at process
birth. Unresolved `__wrap_*`/`__real_*` at link means the shim TU is missing from that target
(B11 row).

---

## B10. Build identity

Every binary states what built it; an artifact that cannot is not evidence (the doctrine: failure
artifacts are self-locating, and identity is the WHERE of the whole binary).

### What is embedded

| field | content | source |
|---|---|---|
| `git_rev` | `git describe --always --dirty` output | [CC-FACT command] |
| `flag_hash` | SHA-256 over the resolved `AUDIO_*` cache values + both toolchain files, canonically serialized | CMake `string(SHA256 ...)` [CC-FACT] |
| `schema_hash` | SHA-256 of config/session_report.schema.json | ties reports to their schema (E8) |
| `profdata_id` | corpus lock hash when `AUDIO_PGO=use`, `""` otherwise | B7 |
| `leg` / `config` | `AUDIO_LEG` / `AUDIO_CONFIG` preset values | B5 |
| `compiler` | `clang --version` first line + triple | [MEASURED 2026-08-12: `clang version 22.1.8`, `x86_64-w64-windows-gnu`] |

### The generated TU

```c
/* build_identity.h — hand-written API; build_identity.c is GENERATED per build, never edited */
typedef struct AudioBuildId {
  const char *git_rev;
  const char *flag_hash;
  const char *schema_hash;
  const char *profdata_id;
  const char *leg;
  const char *config;
  const char *compiler;
} AudioBuildId;
const AudioBuildId *audio_build_id(void);
```

Generation: a CMake script target writes `build_identity.c` from the fields above; the git-rev
step hangs off an always-outdated custom target so the TU regenerates when HEAD moves
[CC-FACT: `add_custom_command`/`add_custom_target` mechanics; skeleton is the project's to wire,
OPEN].

### Where it surfaces

| surface | who reads it |
|---|---|
| `--version` of every executable incl. tools | humans, CI logs |
| session report header | reference/error_tracing_contract_manifest.md section E8; generation reference/observability_flightring_manifest.md section O7 |
| crash capture header | reference/error_tracing_contract_manifest.md section E9 |
| bench JSON records | reference/optimization_microarch_manifest.md section P2 (a perf claim without identity is not evidence) |
| test-run banner | reference/testing_verification_manifest.md section T2 |
| ship archive key for map + `.dbg` | B9 |

| RULE | route | tag |
|---|---|---|
| A host test asserts every identity field non-empty and `git_rev` matches the checkout | host-test-catchable | [OPEN ASSUMED: house convention] |
| Two binaries with equal `flag_hash`+`git_rev`+`leg` are the same build for triage purposes; any comparison across differing identity is labeled as such | contract-only | [OPEN ASSUMED] |

---

## B11. Build-failure troubleshooting — agent-facing

### The agent loop for a build failure

1. The compiler/linker diagnostic is self-locating (file:line:col + flag name in brackets) — read
   it before anything else.
2. Reproduce with the exact failing command from `build/<preset>/compile_commands.json`
   (`CMAKE_EXPORT_COMPILE_COMMANDS=ON` is preset-pinned) [CC-FACT].
3. Match the symptom below; fix at the named layer — **never** by deleting the flag, widening a
   suppression, or leaving the environment (those are canon amendments, B2 governance).

### Symptom → cause → fix

| symptom (exact text where measured) | cause | fix | refs |
|---|---|---|---|
| `error: attempt to use a poisoned identifier` | an RT-plane TU (includes config/rt_prelude_poison.h) calls `malloc`/banned API — the ban is **working** | fix the call site (preallocate, use the arena); if the TU is genuinely control-plane, its classification is wrong — move the TU, never the header | [MEASURED 2026-08-12: hub battery, `#pragma GCC poison`]; reference/rt_plane_rules_manifest.md section R2, reference/memory_residency_manifest.md section M1 |
| `undefined reference to __wrap_malloc` (or `__real_*`) | target takes the `--wrap` row but does not link the guard shim TU | link the shim library into every wrapped target | B9; reference/rt_plane_rules_manifest.md section R4 |
| `clang: error: argument unused during compilation: '-fno-plt' [-Werror,-Wunused-command-line-argument]` | Linux-leg flag row leaked into the Windows leg | per-leg rows live only in `leg-linux` preset vars | [MEASURED 2026-08-12]; B2/B4 |
| configure fails: `Windows leg builds ONLY from a CLANG64 shell` / triple assertion | wrong shell, PATH pollution, or wrong package set | launch the CLANG64 shell; run the B4 purity check; reinstall `mingw-w64-clang-x86_64-*` set | B4; config/toolchain-clang64-windows.cmake; hub H3 |
| link errors against CRT symbols (`__imp_*` mismatches, duplicate/missing runtime bits) after "it configured fine" | stale objects from another MSYS2 subsystem or MSVC mixed into the build tree | delete `build/<preset>/` wholesale and rebuild inside CLANG64; inspect suspect objects with `llvm-objdump -f` / `llvm-nm` | [UNVERIFIED symptom text — varies; mechanism ESTABLISHED: booklet section 10.1]; B4 |
| `cmake: command not found` in CLANG64 | not installed (verified state of the reference machine) | `pacman -S mingw-w64-clang-x86_64-cmake mingw-w64-clang-x86_64-ninja` | [MEASURED 2026-08-12: hub battery]; B5 |
| `cmake --preset linux-dev` on Windows: preset not found / not usable | presets carry a host-OS `condition`; the other leg's presets are filtered out by design | use the leg's own presets; cross-building legs is out of scope | B5 [CC-FACT] |
| remark gate reports zero vectorization remarks on `perf`/`ship` while kernels are fine | ThinLTO defers the vectorizer to link; compile-time `-Rpass` is silent | gate the **link** stderr via `AUDIO_LTO_REMARK_LDFLAGS` (`-Wl,-mllvm,-pass-remarks=loop-vectorize`) | [MEASURED 2026-08-12]; B8 |
| `remark: loop not vectorized: cannot prove it is safe to reorder floating-point operations ...` on a reduction kernel | canon bans fast-math; FP reductions need an explicit per-loop grant | `#pragma clang loop vectorize(enable)` with a justification comment; never a `-ffast-math` row | [MEASURED 2026-08-12]; B8, reference/dsp_kernel_patterns_manifest.md section K5 |
| ASan-built exe dies at startup unable to load the ASan runtime DLL | run outside the CLANG64 PATH — the dynamic runtime lives in `clang64/bin` | run from a CLANG64 shell, or ship the runtime DLL beside the exe for CI harnesses | [MEASURED 2026-08-12: hub battery — asan dynamic runtime present in clang64/bin]; T8 |
| `-fsanitize=thread` fails to link on the Windows leg | TSan runtime ABSENT on CLANG64 | TSan lanes are Linux-leg only; route the suite there | [MEASURED 2026-08-12: hub battery]; hub H5, T8 |
| `error: unknown warning option` after a toolchain bump | a canon warning was renamed/removed by the new major | toolchain-bump ritual: diff the canon, re-run remark gates + bench + goldens, then advance the hub row | [ESTABLISHED: booklet section 14.6]; B2 governance, hub H9 |
| `error: always_inline function '...' requires target feature ...` under LTO with per-ISA kernel TUs | an `always_inline` helper crossed an ISA-attribute boundary during LTO inlining | keep ISA-specific helpers `static` inside their per-ISA TU; cross-TU access only via the init-time dispatch table | [CC-FACT — diagnostic text approximate]; B6, reference/dsp_kernel_patterns_manifest.md section K5 |
| Ninja rebuilds everything / stale-cache weirdness after editing toolchain or preset files | configure-level inputs changed under an existing build dir | wipe `build/<preset>/` — per-preset binary dirs exist precisely so this is cheap and isolated | B5 [CC-FACT] |
| ship link fine, but archive step rejects the artifact | map or `.dbg` sidecar missing, or identity fields empty | B9 archive rule + B10 identity test point at the exact missing artifact | B9, B10; reference/quality_gates_ci_manifest.md section G7 |

### Decisions you must not invent (OPEN register)

- **Ship/field assert policy** — which asserts survive in `perf`/`ship` (`AUDIO_ASSERTS=field-policy`
  placeholder). NEEDS-INPUT.
- **PGO profile corpus** — which sessions/sweeps, refresh cadence, where the lockfile lives.
  NEEDS-INPUT (B7).
- **Linux leg pin** — distro clang vs upstream, absolute compiler path, hardening rows beyond
  relro/now. NEEDS-INPUT (hub H4; booklet section 11.6 owns deployment hardening).
- **Archive location + retention** for ship maps/`.dbg`/identity. NEEDS-INPUT (B9).
- **ISA floor scope** — floor flag on all classes (this file's ASSUMED default) vs kernels only.
  ASSUMED, revisit if shell build cost ever matters.
- **Test-config LTO off**; **guards off in perf**; `-fno-sanitize-recover=all` on CI sanitizer
  lanes; `.clang-format` IndentWidth 2; `AUDIO_TU_CLASS` property name; identity-TU wiring.
  All ASSUMED — reverse any of them only as a documented canon amendment (B2 governance).
