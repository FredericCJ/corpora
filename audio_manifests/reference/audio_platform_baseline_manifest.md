# Audio Platform Baseline — Version Hub

**Purpose.** The single dated-fact registry of audio-rt-ground: toolchain versions and package identities per leg, sanitizer/fuzzer/BOLT availability, OS and audio-API baselines, privilege conventions, ISA floor and microarchitecture anchors — every version-dependent claim anywhere in the package routes to a row here.

Facts verified 2026-08-12. Version-dependent claims route to reference/audio_platform_baseline_manifest.md (the hub); if any file disagrees with the hub, the hub wins. This file IS the hub: routes terminate here, and every dated row below is addressable as "hub H\<n\>" (section) or by its row id (e.g. `h3-clang`).

Reasoning root: the child booklet `realtime-audio-pc-architecture-and-design-r1.md` (repo root). This file fulfils the hub the booklet declares in booklet section 16.3 — it operationalizes the booklet and never re-argues it.

---

## H1. Identity and scope

### What this hub is

- The package's one version hub, per the parent's one-hub law as instantiated by booklet section 16.3 [ESTABLISHED: booklet section 16.3].
- A hub row = row id + fact + evidence tag + verification date + re-verify command. A row without a re-verify command is a defect in this file [OPEN: ASSUMED — house convention carried from the manifests family].
- Tag semantics inside this file: sibling files cite rows as `[VERSION-DEPENDENT - hub H<n>]`; inside the hub the rows themselves carry the terminal evidence tag ([MEASURED ...], [ESTABLISHED: ...], [CC-FACT], [OPEN: ...], [UNVERIFIED]). VERSION-DEPENDENT resolves *to* a row; it never appears as a row's own tag here.

### The hub-wins rules

| id | rule | enforcement route |
|---|---|---|
| h1-wins | If any package file states a version, date, availability, or package-identity fact that disagrees with this file, this file wins; the fix is an edit to the other file — or a re-verification here that re-dates the row. | contract-only |
| h1-route | Any version literal outside this file must carry a `- hub H<n>` pointer; a bare version number in a sibling file is a defect. Structural audit candidate: grep for `\d+\.\d+\.\d+` outside hub pointers in config/check.sh. | build-catchable (config/check.sh, reference/quality_gates_ci_manifest.md section G3) [OPEN: ASSUMED — audit regex not yet wired] |
| h1-redate | A row's date advances only by re-running the row's recorded re-verify command on the machine the row describes — never by assertion. | contract-only |
| h1-gap | A fact needed by a sibling file with no hub row: the sibling adds the row here first (tagged UNVERIFIED or OPEN if need be), then cites it. No improvised facts in the gap [ESTABLISHED: booklet section 16.3]. | contract-only |

### Scope: two legs

| id | leg | OS | toolchain | status |
|---|---|---|---|---|
| h1-leg-win | Windows | Windows 11 Pro, build 10.0.26200 [MEASURED 2026-08-12: host env report] | MSYS2 CLANG64, clang 22.1.8, target `x86_64-w64-windows-gnu`, UCRT [MEASURED 2026-08-12] | reference machine; every MEASURED row in this file ran here |
| h1-leg-linux | Linux | distro unpinned [OPEN: NEEDS-INPUT — the Linux leg's reference deployment (second box, dual boot, or CI container) is not chosen] | distro/upstream clang, same major as Windows leg (22.x) [ESTABLISHED: booklet section 10.1] | declared; per-deployment rows in H4 |

### What lives here vs. elsewhere

| fact class | owner |
|---|---|
| versions, availability, package identity, OS/API baselines, privilege conventions, microarch anchors | this file |
| flag spellings and the flag canon table | reference/toolchain_build_manifest.md section B2 (enforced by config/toolchain-clang64-windows.cmake, config/toolchain-linux-clang.cmake) |
| RT-plane bans, guard machinery, FTZ/DAZ *policy* | reference/rt_plane_rules_manifest.md sections R2/R4/R5 (the measured MXCSR fact is hub row h8-mxcsr) |
| device setup/loop/recovery sequences | reference/device_adapter_manifest.md (availability baselines are hub H6) |
| which CI lane runs which sanitizer | reference/testing_verification_manifest.md section T8 (availability matrix is hub H5) |
| bench and microarch measurement protocol | reference/optimization_microarch_manifest.md sections P2/P3 (class anchors are hub H8) |
| residency mechanics per OS | reference/memory_residency_manifest.md sections M5/M6 (privilege facts are hub H7) |

### How to cite a hub row (the package's one citation shape)

In any sibling file, a version-bound fact is stated once, tagged, and routed:

```markdown
ASan runs on the Windows leg's per-commit lane [VERSION-DEPENDENT - hub H5].
The kernel TU class compiles -march=x86-64-v3 [VERSION-DEPENDENT - hub H8, row h8-march].
```

Row-level ids are optional precision; the section-level `hub H<n>` is the minimum. A failing gate's
message uses the same shape, which is what makes environment-drift failures self-locating (next
subsection).

### Row-id index (for row-level citations and failure messages)

| section | row ids |
|---|---|
| H1 | h1-wins, h1-route, h1-redate, h1-gap, h1-leg-win, h1-leg-linux |
| H2 | h2-cpu, h2-topo, h2-l1d, h2-l2, h2-l3, h2-ram, h2-os, h2-tc, h2-cpumap, h2-lat-l1, h2-lat-l2, h2-lat-l3, h2-lat-dram |
| H3 | h3-root, h3-bin, h3-shell, h3-script, h3-clang, h3-lld, h3-llvm, h3-cte, h3-analyzer, h3-crt-rt, h3-libcxx, h3-lldb, h3-make, h3-python, h3-crt, h3-cmake, h3-ninja, h3-update-gate, h3-group, h3-pure-1…5, h3-cap-poison, h3-cap-wrap, h3-cap-atomics, h3-cap-vecremark |
| H4 | h4-clang, h4-upstream, h4-lld, h4-libc, h4-kernel, h4-glibc-ver |
| H5 | h5-asan, h5-ubsan, h5-tsan, h5-fuzzer, h5-bolt, h5-msan |
| H6 | h6-alsa-layers, h6-alsa-lineage, h6-alsa-build, h6-alsa-ver, h6-alsa-dev, h6-alsa-shape, h6-wasapi-1, h6-wasapi-2, h6-wasapi-3, h6-wasapi-modes, h6-wasapi-floor, h6-wasapi-c, h6-wasapi-mixfmt, h6-wasapi-com, h6-wasapi-minper, h6-wasapi-default |
| H7 | h7-limits, h7-rtkit, h7-cap, h7-order, h7-throttle, h7-throttle-posture, h7-memlock, h7-mmcss, h7-mmcss-prio, h7-sysresp, h7-tasks, h7-noadmin-rule, h7-vlock, h7-largepage, h7-cstate-linux, h7-cstate-win |
| H8 | h8-floor, h8-avx512, h8-line, h8-pages, h8-tsc, h8-march, h8-no-native, h8-parity, h8-saxpy, h8-mxcsr, h8-mca, h8-fma, h8-dispatch, h8-latency-tables |
| H9 | h9-gate, h9-cadence |

Renaming or deleting a row id is a breaking change to every citing file; ids are append-only [OPEN: ASSUMED — house convention].

### The hub in the agent feedback loop

Testability and traceability doctrine, applied to versions: a failure caused by environment drift must be self-locating to a hub row.

- Build identity (reference/toolchain_build_manifest.md section B10) embeds compiler version + triple; session reports (config/session_report.schema.json, reference/error_tracing_contract_manifest.md section E8) carry it, so any failure artifact is diffable against rows h3-clang / h4-clang.
- config/check.sh prints this file's verification date at the top of every run; a gate failing after `pacman -Syu` names the drift candidate instead of leaving the agent to guess. Route: build-catchable (reference/quality_gates_ci_manifest.md section G2).
- When a re-check trigger (H9) fires, the re-verification is a recorded command run, and the diff of this file is the evidence.

## H2. Reference machine and class floor

### The reference machine

All rows [MEASURED 2026-08-12] unless noted. Re-verify: CPU/cache/RAM via any of `wmic cpu`, CPU-Z, or `lscpu` on the Linux leg; OS via `winver`.

| id | property | value |
|---|---|---|
| h2-cpu | CPU | Intel Core i9-12900K, 12th gen (Alder Lake), hybrid |
| h2-topo | topology | 8 P-cores × 2-way SMT + 8 E-cores = 24 hardware threads |
| h2-l1d | L1d | 48 KiB per P-core; 32 KiB per E-core |
| h2-l2 | L2 | 1.25 MiB per P-core; 2 MiB per 4-E-core cluster |
| h2-l3 | L3 | 30 MiB, shared |
| h2-ram | RAM | 32 GiB |
| h2-os | OS | Windows 11 Pro, build 10.0.26200 [MEASURED 2026-08-12: host env report] |
| h2-tc | toolchain | clang 22.1.8, MSYS2 CLANG64, `x86_64-w64-windows-gnu`, UCRT |
| h2-cpumap | logical CPU enumeration | Alder Lake parts typically enumerate P-cores first as SMT pairs (LP 0–15, pair = 2n/2n+1), E-cores after (LP 16–23) [CC-FACT — **verify before any affinity mask**: Sysinternals `coreinfo -c -s`, `GetLogicalProcessorInformationEx`, or `lscpu -e` on the Linux leg; consumed by reference/optimization_microarch_manifest.md section P9] |

### The class floor

The package pins a hardware **class**, not a part number; the class is what survives shopping decisions [ESTABLISHED: booklet section 1.2]. Floor column [ESTABLISHED: booklet section 1.2]; reference column [MEASURED 2026-08-12].

| property | class floor (pinned) | reference machine |
|---|---|---|
| ISA | x86-64 at `x86-64-v3`: AVX2, FMA, BMI2 | i9-12900K (v3-capable; AVX-512 fused off, see h8-avx512) |
| cores | ≥ 8 hardware threads; hybrid topologies expected | 24 threads, hybrid P/E |
| L1d | ≥ 32 KiB per core, 64-byte lines | 48 KiB P / 32 KiB E |
| L2 | ≥ 512 KiB per core or cluster | 1.25 MiB P / 2 MiB per E-cluster |
| last-level cache | ≥ 8 MiB shared | 30 MiB |
| RAM | ≥ 16 GiB, virtual memory always on, 4 KiB pages | 32 GiB |
| timekeeping | constant/invariant TSC; OS monotonic clock | present |
| clocking | dynamic frequency + idle states, always assumed | turbo + deep C-states, hybrid asymmetry |

Load-bearing consequences — argued in the booklet, only cited here:

- **Topology is asymmetric**: an RT thread on an E-core silently loses a large budget fraction; placement is architecture, and every latency figure carries its core class [ESTABLISHED: booklet section 1.2, 11.2]. Operational rows: reference/optimization_microarch_manifest.md section P9, cards/optimize-performance.md.
- **The memory hierarchy is the cost model**: ratios are the class, exact latencies are hub rows (below) [ESTABLISHED: booklet section 1.2]. Budgeting: reference/memory_residency_manifest.md section M8.
- **Correctness pins one level above silicon**: C11/C17 memory model, never x86-TSO [ESTABLISHED: booklet section 1.2, 6.6]. Rules: reference/rt_plane_rules_manifest.md section R6.

### Cost-model anchor rows

| id | level | class ratio [ESTABLISHED: booklet section 1.2] | typical figure, Alder Lake P-core [CC-FACT — not yet measured on this machine] |
|---|---|---|---|
| h2-lat-l1 | L1d hit | ~4 cycles | ~5 cycles load-to-use |
| h2-lat-l2 | L2 hit | ~a dozen cycles | ~15 cycles |
| h2-lat-l3 | L3 hit | tens of cycles | ~50–70 cycles |
| h2-lat-dram | DRAM | hundreds of cycles | ~80–120 ns |

Re-verify: run a pointer-chase microbench per reference/optimization_microarch_manifest.md section P3 and replace the CC-FACT column with MEASURED rows; until then any per-cycle argument uses the ratio column. E-core figures differ and are [UNVERIFIED — measure before budgeting E-core work].

Working-set implication: portable per-block budgets target the **class floor** caches (32 KiB L1d, 512 KiB L2), not the reference machine's larger ones — budget against the class, measure on the machine [ESTABLISHED: booklet section 1.2]. Budget tables live in reference/memory_residency_manifest.md section M8.

## H3. CLANG64 environment, packages, install

### What CLANG64 is

- One of MSYS2's mutually-exclusive build environments: a full native toolchain producing ordinary PE binaries against the Universal C Runtime (UCRT) — clang with lld as its linker, compiler-rt, libc++ (for C++ dependencies; the product is C17), libunwind, and the LLVM tool suite [ESTABLISHED: booklet section 10.1].
- Target triple `x86_64-w64-windows-gnu` [MEASURED 2026-08-12]. Re-verify: `clang -dumpmachine` [CC-FACT: command].
- lld drives linking via its MinGW driver (`-Wl,...` GNU-style flags accepted) [MEASURED 2026-08-12: `-Wl,--wrap=malloc` link succeeded, noted "lld MinGW driver"].
- No MSVC, no msvcrt: the produced binaries import UCRT (`api-ms-win-crt-*.dll`), not `msvcrt.dll` [CC-FACT — verify with `llvm-objdump -p app.exe | grep -i dll`].

### The four environments you will see (and the three you must not build in)

[ESTABLISHED: MSYS2 docs (environments page)] — the disambiguation that env-purity rules police:

| environment | CRT | compiler | C++ runtime | role here |
|---|---|---|---|---|
| MSYS | `msys-2.0.dll` (POSIX emulation) | gcc | libstdc++ | shell + scripts only; its binaries never ship (h3-pure-3) |
| MINGW64 | msvcrt | gcc | libstdc++ | legacy; not used |
| UCRT64 | UCRT | gcc | libstdc++ | not used — same CRT as CLANG64, different compiler/objects: still never mixed |
| **CLANG64** | **UCRT** | **clang** | **libc++** | **the Windows leg** [ESTABLISHED: booklet section 10.1] |

### Paths and environment entry

| id | item | value | tag |
|---|---|---|---|
| h3-root | environment root | `C:/msys64/clang64` | [CC-FACT — default MSYS2 install root; verify `cygpath -w /clang64`] |
| h3-bin | binaries | `C:/msys64/clang64/bin` (contains clang, lld, llvm-*, and the ASan dynamic runtime DLL) | [MEASURED 2026-08-12: asan dynamic runtime present in clang64/bin on PATH] |
| h3-shell | interactive entry | `C:\msys64\clang64.exe` launcher; env selects itself via `MSYSTEM=CLANG64` | [CC-FACT] |
| h3-script | scripted entry | `C:\msys64\msys2_shell.cmd -clang64 -defterm -no-start -c '<cmd>'` | [CC-FACT] |

### Installed package inventory

[MEASURED 2026-08-12: `pacman -Q`]. All toolchain packages carry the `mingw-w64-clang-x86_64-` prefix (elided below). Re-verify: `pacman -Q | grep mingw-w64-clang-x86_64`.

| id | package | version | provides |
|---|---|---|---|
| h3-clang | clang | 22.1.8-1 | the compiler |
| h3-lld | lld | 22.1.8-1 | the linker (default for the driver) |
| h3-llvm | llvm | 22.1.8-1 | llvm-mca, llvm-profdata, llvm-cov, llvm-nm, llvm-objdump — all present [MEASURED 2026-08-12] |
| h3-cte | clang-tools-extra | 22.1.8-1 | clang-tidy (analysis-catchable route's instrument) |
| h3-analyzer | clang-analyzer | 22.1.8-1 | the static analyzer driver |
| h3-crt-rt | compiler-rt | 22.1.8-1 | sanitizer + fuzzer + profile runtimes (availability matrix: H5) |
| h3-libcxx | libc++ | 22.1.8 | C++ runtime for C++ dependencies only |
| h3-lldb | lldb | 22.1.8 | debugger |
| h3-make | make | 4.4.1 | build scripting [MEASURED 2026-08-12; package origin (msys vs clang64 prefix) not recorded — verify `pacman -Qo $(which make)`] |
| h3-python | python | 3.14.6 | runs config/audit_includes.py, config/audit_symbols.py |
| h3-crt | crt (mingw-w64 UCRT CRT) + winpthreads | 14.0.0.r150 | CRT startup objects, import libs, winpthreads [MEASURED 2026-08-12; exact package names via `pacman -Qs 'crt\|winpthreads'`] |

### Not yet installed — required by config/

| id | package | repo version | status |
|---|---|---|---|
| h3-cmake | mingw-w64-clang-x86_64-cmake | 4.3.4-1 | **NOT installed** [MEASURED 2026-08-12: repo query] |
| h3-ninja | mingw-w64-clang-x86_64-ninja | 1.13.2-1 | **NOT installed** [MEASURED 2026-08-12: repo query] |

Install row (run before first configure; config/CMakePresets.json assumes both — reference/toolchain_build_manifest.md section B5):

```sh
pacman -S mingw-w64-clang-x86_64-cmake mingw-w64-clang-x86_64-ninja
```

### Install and update commands

```sh
# full baseline (idempotent; --needed skips present packages)
pacman -S --needed \
  mingw-w64-clang-x86_64-clang mingw-w64-clang-x86_64-lld \
  mingw-w64-clang-x86_64-llvm mingw-w64-clang-x86_64-clang-tools-extra \
  mingw-w64-clang-x86_64-clang-analyzer mingw-w64-clang-x86_64-compiler-rt \
  mingw-w64-clang-x86_64-lldb mingw-w64-clang-x86_64-python \
  mingw-w64-clang-x86_64-cmake mingw-w64-clang-x86_64-ninja

# rolling update — MSYS2 has no versioned releases; this moves EVERY hub row in H3
pacman -Syu        # may ask to close the shell and re-run once more [CC-FACT: MSYS2 update mechanics]
```

Rule rows:

| id | rule | enforcement route |
|---|---|---|
| h3-update-gate | `pacman -Syu` is a hub event: after any update, re-run the H9 toolchain-drift block before trusting a build. A green gate run on an unrecorded toolchain is not evidence. | build-catchable (config/check.sh prints toolchain identity; gates re-run per reference/quality_gates_ci_manifest.md section G7) |
| h3-group | The `mingw-w64-clang-x86_64-toolchain` pacman group exists and pulls a superset [CC-FACT]; installing it is fine, but the inventory above is the accountable set. | contract-only |

Never rows (package management):

- **Never `pacman -Sy <pkg>`** (refresh-then-install without full upgrade): partial upgrades are unsupported on the rolling model and produce mixed-ABI trees [ESTABLISHED: MSYS2 docs]. Install against a current database (`pacman -Syu`, then `pacman -S ...`) or with a stale-but-consistent one (`pacman -S ...` alone).
- **Never install unprefixed or wrong-prefix packages as build deps** — `cmake` (MSYS prefix) is not `mingw-w64-clang-x86_64-cmake`; the former configures against the POSIX-emulation world. Route: build-catchable (h3-pure-2 triple assert fails downstream) plus contract-only at install time.
- **Never update mid-endeavour without re-running the H9 drift block** (h3-update-gate).

### Environment purity rules

MSYS2 ships several environments (MSYS, MINGW64, UCRT64, CLANG64...); mixed-runtime binaries are the ecosystem's classic self-inflicted wound [ESTABLISHED: booklet section 10.1].

| id | rule | enforcement route |
|---|---|---|
| h3-pure-1 | Never mix objects/libs across MSYS, MINGW64, UCRT64, CLANG64 — one environment per build tree; dependencies come only from `mingw-w64-clang-x86_64-*` packages. | build-catchable (toolchain file asserts compiler path prefix `/clang64/`) |
| h3-pure-2 | Assert the triple at configure time: `clang -dumpmachine` == `x86_64-w64-windows-gnu`. A gcc-flavored triple or an `-msvc` triple aborts the configure. | build-catchable (config/toolchain-clang64-windows.cmake) |
| h3-pure-3 | Shipped/test PE binaries must not import `msys-2.0.dll` (the POSIX-emulation runtime — MSYS-env leakage) and must import UCRT, not `msvcrt.dll`. | build-catchable (config/audit_symbols.py over `llvm-objdump -p` output; wired per reference/quality_gates_ci_manifest.md section G3) |
| h3-pure-4 | Never run configure from a shell with MSVC `vcvars` or a stray MinGW-gcc on PATH ahead of `/clang64/bin`. | contract-only (plus h3-pure-2 catches the common damage) |
| h3-pure-5 | Do not pass FILE*, heap pointers, or locales across DLL boundaries into modules built against a different CRT. | contract-only [CC-FACT: mixed-CRT hazard mechanics] |

### First-time bootstrap (fresh Windows box → buildable leg)

1. Install MSYS2 from msys2.org → root `C:\msys64` [CC-FACT].
2. Open the **CLANG64** shell (`C:\msys64\clang64.exe`) — never the MSYS shell for builds.
3. `pacman -Syu`; if it asks to close the shell, reopen and run it once more [CC-FACT: MSYS2 update mechanics].
4. Run the full-baseline `pacman -S --needed ...` block above (includes h3-cmake/h3-ninja).
5. Verify: `clang -dumpmachine` → `x86_64-w64-windows-gnu`; `clang --version` against row h3-clang — mismatch means the hub re-dates before anything builds (h1-redate).
6. Run the H9 drift block; commit the hub diff if any row moved.
7. Continue at cards/start-project.md (project scaffold, config/CMakePresets.json, first gate run).

### Toolchain capability rows (measured on this clang; siblings cite, don't re-test)

| id | capability | result | consumer |
|---|---|---|---|
| h3-cap-poison | `#pragma GCC poison malloc` → compile error "attempt to use a poisoned identifier" | works [MEASURED 2026-08-12] | config/rt_prelude_poison.h; reference/rt_plane_rules_manifest.md section R4 (compiler-catchable route) |
| h3-cap-wrap | `-Wl,--wrap=malloc` links; `__wrap_malloc` also intercepts CRT-internal startup allocations (3 hits observed before `main` in a trivial exe) | works, with pre-main hits [MEASURED 2026-08-12] | guard must arm per-thread/per-phase, not abort on any hit — design owned by reference/rt_plane_rules_manifest.md section R4 |
| h3-cap-atomics | C17 `stdatomic.h` acquire/release + `_Alignas(64)` compile clean | works [MEASURED 2026-08-12] | reference/concurrency_channels_manifest.md; reference/rt_plane_rules_manifest.md section R6 |
| h3-cap-vecremark | `-Rpass=loop-vectorize` remarks emitted at `-O3 -march=x86-64-v3` | works [MEASURED 2026-08-12; exact remark text at h8-saxpy] | remark gates, reference/toolchain_build_manifest.md section B8 |

## H4. Linux leg baseline

### The declared baseline

| id | item | value | tag |
|---|---|---|---|
| h4-clang | clang major | same major as the Windows leg: **22.x** (Windows leg is 22.1.8, row h3-clang); source = distro packages or upstream (apt.llvm.org / LLVM releases) | [ESTABLISHED: booklet section 10.1 — "the two legs track the same major"] |
| h4-upstream | upstream path when the distro lags 22.x | apt.llvm.org for Debian-lineage (its `llvm.sh` convenience script installs a pinned major), or LLVM release binaries — keeps both legs on one major | [CC-FACT — verify script/URL at deployment] |
| h4-lld | linker | lld, same major; GNU ld is not a substitute (map files, `--wrap`, ThinLTO parity with h3-lld) | [ESTABLISHED: booklet section 10.1] + [CC-FACT: feature parity reasoning] |
| h4-libc | libc | glibc, dynamically linked; musl out of scope | [OPEN: ASSUMED — glibc; revisit only if a musl deployment appears] |
| h4-kernel | kernel floor | any maintained LTS of the last ~5 years suffices: the consumed surfaces (ALSA PCM, SCHED_FIFO, mlockall, futex, timerfd) are decades-stable [CC-FACT] | [OPEN: ASSUMED — no exact floor pinned until a deployment exists] |
| h4-glibc-ver | glibc floor version | unpinned | [OPEN: NEEDS-INPUT — pin when the deployment distro is chosen] |

### Packages typically needed

Names are distro-lineage-typical [CC-FACT — verify per deployment; do not trust these spellings unqueried]:

| need | Debian/Ubuntu lineage | Fedora lineage | verify |
|---|---|---|---|
| compiler | `clang-22` (apt.llvm.org) or distro `clang` | `clang` | `clang --version` |
| linker | `lld-22` / `lld` | `lld` | `ld.lld --version` |
| tidy/format/analyzer | `clang-tidy-22`, `clang-format-22`, `clang-tools-22` | `clang-tools-extra` | `clang-tidy --version` |
| sanitizer/fuzzer runtimes | `libclang-rt-22-dev` (or bundled with the compiler package) | `compiler-rt` | H5 re-verify block |
| BOLT | package name varies (`bolt-22` on apt.llvm.org lineage) | `llvm-bolt` | `llvm-bolt --version` |
| ALSA headers | `libasound2-dev` | `alsa-lib-devel` | `pkg-config --modversion alsa` |
| perf | `linux-perf` (kernel-matched) | `perf` | `perf --version` |

### Per-deployment OPEN register (H4)

All [OPEN: NEEDS-INPUT] until the Linux reference deployment (row h1-leg-linux) is chosen: distro identity and release; exact clang/lld/glibc/alsa-lib versions; rtkit presence (desktop yes, container/headless usually no); `/etc/security/limits.d` content; whether the distro's default scheduler handles hybrid placement (booklet section 11.2 defers this to a "hub-dated judgment per kernel generation" — that judgment cannot be made before a kernel is pinned).

## H5. Sanitizer / fuzzer / BOLT availability

### The matrix

| id | component | Windows leg (CLANG64) | Linux leg | evidence |
|---|---|---|---|---|
| h5-asan | ASan | **PRESENT** — links and runs clean; dynamic runtime DLL in `clang64/bin` | PRESENT | Win: [MEASURED 2026-08-12]; Linux: [ESTABLISHED: booklet section 10.8] + [CC-FACT — standard compiler-rt; re-verify at Linux bring-up] |
| h5-ubsan | UBSan | **PRESENT** — runs and prints `p12_ubsan.c:2:34: runtime error: signed integer overflow: 2147483647 + 1 cannot be represented in type int` + SUMMARY line | PRESENT | Win: [MEASURED 2026-08-12]; Linux: as h5-asan |
| h5-tsan | TSan | **ABSENT** — no tsan in the clang runtime libs | PRESENT, Linux-only | Win: [MEASURED 2026-08-12]; Linux: [ESTABLISHED: booklet section 10.8] |
| h5-fuzzer | libFuzzer | **PRESENT** — `libclang_rt.fuzzer*` runtime libs shipped | PRESENT | Win: [MEASURED 2026-08-12]; Linux: [ESTABLISHED: booklet section 10.8] |
| h5-bolt | llvm-bolt | **ABSENT** from CLANG64 | Linux-only lane | Win: [MEASURED 2026-08-12]; Linux: [ESTABLISHED: booklet section 16.3] |
| h5-msan | MSan | not adopted | not adopted (Linux-only in general; requires instrumented world) | [CC-FACT]; no lane exists — saying so beats implying coverage |

### Consequences — which lane runs what

| component | lane | wiring |
|---|---|---|
| ASan + UBSan | per-commit host-test lane on **both** legs | reference/testing_verification_manifest.md section T8; matrix reference/quality_gates_ci_manifest.md section G5; config/ci-github.yml |
| TSan | concurrency torture suites (channel torture, swap/retire races, shutdown storms) run on the **Linux lane only** — a structural fact of the verification plan, not a footnote [ESTABLISHED: booklet section 10.8]. Single-leg race detection is meaningful for both legs because the code is identical and TSan checks the C11 model, not the hardware [ESTABLISHED: booklet section 10.8]. | reference/testing_verification_manifest.md sections T7/T8 |
| libFuzzer | fuzz targets for every parser of foreign bytes, both legs, continuous at CI budget | reference/testing_verification_manifest.md section T9 |
| BOLT | post-link layout rung, Linux leg only; Windows ships without it and the bench gate sizes budgets accordingly | reference/optimization_microarch_manifest.md section P8 |

### Windows ASan runtime note

The ASan runtime is a **dynamic** DLL living in `clang64/bin` [MEASURED 2026-08-12]. Consequence: an ASan test binary launched outside a CLANG64 shell (IDE, task scheduler, CI runner) must have `C:/msys64/clang64/bin` on PATH or the process dies at load with a missing-DLL error, not a sanitizer report — a self-location trap worth pre-empting in the test runner. Route: host-test-catchable (runner smoke-test asserts one ASan-positive canary fails as expected — reference/testing_verification_manifest.md section T8).

### Re-verify commands (both legs)

```sh
# runtime libraries present for this compiler
ls "$(clang -print-resource-dir)/lib/windows" | grep -Ei 'asan|ubsan|fuzzer|tsan'   # Windows leg
ls "$(clang -print-resource-dir)/lib/linux"   | grep -Ei 'asan|ubsan|fuzzer|tsan'   # Linux leg
# expected on CLANG64 (2026-08-12): asan+ubsan+fuzzer hits, NO tsan hit
# smoke: -fsanitize=address and -fsanitize=undefined must link AND run
llvm-bolt --version   # expected on CLANG64: command not found
```

## H6. Audio API baselines: ALSA and WASAPI

### ALSA (Linux leg)

| id | fact | tag |
|---|---|---|
| h6-alsa-layers | Two layers: the kernel ALSA PCM interface, and user-space **alsa-lib** (`libasound`) which applications link — the adapter programs alsa-lib, never raw ioctls | [ESTABLISHED: alsa-lib docs] |
| h6-alsa-lineage | Stable lineage: kernel audio API since Linux 2.6 (2003); additive evolution, no WASAPI-style generational interfaces | [CC-FACT] |
| h6-alsa-build | `#include <alsa/asoundlib.h>`, link `-lasound`, discover via `pkg-config alsa` | [CC-FACT — verify: `pkg-config --modversion alsa`] |
| h6-alsa-ver | alsa-lib version: 1.2.x lineage current for years [CC-FACT]; exact version per deployment | [OPEN: NEEDS-INPUT — pin with the distro, H4 register] |
| h6-alsa-dev | Device naming: `"default"` routes through the deployment's plugin/server chain; `"hw:N,M"` is the direct hardware PCM. Which the adapter opens, and the latency each costs, is adapter business | reference/device_adapter_manifest.md sections D2/D9 [CC-FACT for the naming] |
| h6-alsa-shape | Contract shape the package extracts: per-device ring shared with the driver, divided into periods; period-boundary wakeups pace the device loop | [ESTABLISHED: booklet section 1.4] |

### PipeWire / JACK presence note

- PulseAudio, JACK, PipeWire are user-space tenants **above** ALSA, and PipeWire increasingly fronts the other two [ESTABLISHED: booklet section 1.4]. On a stock desktop, `"default"` is usually a server-owned virtual device; the ALSA adapter still works but inherits the server's period/latency policy [CC-FACT].
- Native PipeWire/JACK adapters: **not shipped**; explicitly OPEN as grandchild adapters [ESTABLISHED: booklet section 16.4] → [OPEN: NEEDS-INPUT — decide only when a product needs server-native routing].

### WASAPI (Windows leg)

Generations (all interfaces from the same `audioclient.h`):

| id | interface | introduced | gives | tag |
|---|---|---|---|---|
| h6-wasapi-1 | `IAudioClient` | Windows Vista | Initialize/Start/Stop, shared + exclusive modes, event-driven mode (`AUDCLNT_STREAMFLAGS_EVENTCALLBACK` + `SetEventHandle`) | [ESTABLISHED: MS WASAPI docs] |
| h6-wasapi-2 | `IAudioClient2` | Windows 8 | `SetClientProperties` (stream categories, hardware offload query) | [ESTABLISHED: MS WASAPI docs] |
| h6-wasapi-3 | `IAudioClient3` | Windows 10 | `GetSharedModeEnginePeriod` / `GetCurrentSharedModeEnginePeriod` / `InitializeSharedAudioStream` — **low-latency shared mode** at small engine periods | [ESTABLISHED: MS WASAPI docs — minimum supported client Windows 10] |

| id | fact | tag |
|---|---|---|
| h6-wasapi-modes | Shared mode: the engine mixes all clients at an engine-owned period and format. Exclusive mode: device-native format, engine steps aside | [ESTABLISHED: booklet section 1.4] |
| h6-wasapi-floor | Package OS floor: Windows 10+ (for IAudioClient3); reference machine is Windows 11 Pro (h2-os) | [OPEN: ASSUMED — floor Windows 10 21H2+/Windows 11; no older-SKU support requested] |
| h6-wasapi-c | Pure-C COM works: `#define COBJMACROS` + `CINTERFACE`, include `mmdeviceapi.h` + `audioclient.h`; `IMMDeviceEnumerator_GetDefaultAudioEndpoint` and `IAudioClient3_GetSharedModeEnginePeriod` macros resolve | [MEASURED 2026-08-12] — mechanics owned by reference/device_adapter_manifest.md section D5 |
| h6-wasapi-mixfmt | Shared-mode format is engine-owned: query it via `IAudioClient::GetMixFormat` and negotiate from there; exclusive mode negotiates device-native formats instead | [ESTABLISHED: MS WASAPI docs]; negotiation/conversion owned by reference/device_adapter_manifest.md section D9 |
| h6-wasapi-com | COM apartment initialization (`CoInitializeEx`) is per-thread and precedes any device enumeration; the adapter owns which threads initialize and how | [CC-FACT]; mechanics reference/device_adapter_manifest.md section D5 |
| h6-wasapi-minper | Actual minimum shared-mode engine period on the reference machine | [UNVERIFIED — not yet queried; measure via the D6 probe (`GetSharedModeEnginePeriod`) and record here] |
| h6-wasapi-default | Default adapter path (IAudioClient3 shared low-latency vs exclusive) | [OPEN: ASSUMED — shared low-latency default, exclusive as a deployment row; recorded in reference/device_adapter_manifest.md section D6] |

### Exclusions and OPEN adapters

- **ASIO: excluded** from the shipped set (vendor SDK outside the OS stack; licensing recorded by the booklet); port left open for a grandchild [ESTABLISHED: booklet sections 1.4, 16.4].
- JACK/PipeWire-native, multi-device topologies, network audio: OPEN per booklet section 16.4 — none of them may be improvised into the device port [contract-only].

## H7. Privilege conventions

### Linux: the three sanctioned grant shapes

The RT plane requests SCHED_FIFO; getting it has exactly three sanctioned shapes, tried in the product's recorded order [ESTABLISHED: booklet section 11.1]:

| id | shape | mechanics | tag |
|---|---|---|---|
| h7-limits | raised resource limits for the audio user/group | `/etc/security/limits.d/` convention shipped by distro audio packages: `@audio - rtprio 95` and `@audio - memlock unlimited`; check with `ulimit -r` (rtprio) and `ulimit -l` (memlock) | [CC-FACT — the classic distro convention; exact file content per deployment, H4 register] |
| h7-rtkit | rtkit session broker | D-Bus service (`org.freedesktop.RealtimeKit1`); grants a bounded RT priority per its policy and attaches an `RLIMIT_RTTIME` budget **with a kill semantic** — a runaway RT thread is killed by design | broker existence + kill semantic [ESTABLISHED: booklet section 11.1]; D-Bus name and mechanics [CC-FACT — verify against rtkit source/docs at deployment] |
| h7-cap | granted capability | `CAP_SYS_NICE` on the binary (`setcap cap_sys_nice+ep`) allows `sched_setscheduler` without limits.d; file capabilities can be silently stripped by copies/updates — re-verify post-install | [CC-FACT] |
| h7-order | attempt order | limits.d-direct first, rtkit fallback, capability as deployment-managed last resort | [OPEN: ASSUMED — recorded at the composition root; revisit per product] |

### Linux: RT throttling

| id | fact | tag |
|---|---|---|
| h7-throttle | Default throttle: `/proc/sys/kernel/sched_rt_runtime_us` = 950000 of `sched_rt_period_us` = 1000000 — RT class capped at 95%, 5% reserved for non-RT work | [CC-FACT — verify: `cat /proc/sys/kernel/sched_rt_runtime_us`] |
| h7-throttle-posture | A correctly built stream never approaches the throttle; disabling it (-1) is a deployment choice, **never** a product requirement | [ESTABLISHED: booklet section 11.1] — route for the "never require" rule: contract-only |
| h7-memlock | Residency needs `RLIMIT_MEMLOCK` ≥ locked set; the audio-group convention is `memlock unlimited` (h7-limits) | [CC-FACT]; mechanics reference/memory_residency_manifest.md section M5 |

### Windows: MMCSS

| id | fact | tag |
|---|---|---|
| h7-mmcss | `AvSetMmThreadCharacteristicsW(L"Pro Audio", &idx)` returns a non-null handle (observed task index 418); link `-lavrt`; `AvRevertMmThreadCharacteristics` works; ran from an ordinary **unelevated** shell — no admin needed | [MEASURED 2026-08-12] |
| h7-mmcss-prio | Within the task, `AvSetMmThreadPriority` selects the band (up to `AVRT_PRIORITY_CRITICAL`) | [ESTABLISHED: MS MMCSS docs] |
| h7-sysresp | Registry `HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\SystemResponsiveness` default **20** (percent reserved for non-multimedia work — the NT analogue of h7-throttle); verify: `reg query ... /v SystemResponsiveness` | [CC-FACT] |
| h7-tasks | Task-class definitions (including "Pro Audio") live as subkeys under `...\SystemProfile\Tasks\`; a machine missing the key makes `AvSetMmThreadCharacteristicsW` fail — treat as a degraded-mode input, not an error exit | key layout [CC-FACT]; disposition reference/error_tracing_contract_manifest.md section E2 |
| h7-noadmin-rule | Raw `REALTIME_PRIORITY_CLASS` process priority is refused as ambient policy — it needs elevation rights, starves system machinery, and buys nothing MMCSS does not grant more safely | [ESTABLISHED: booklet section 11.1] — route: contract-only, backed by analysis-catchable ban of `SetPriorityClass(REALTIME_PRIORITY_CLASS)` in shipped code (clang-tidy banned-symbol list, reference/rt_plane_rules_manifest.md section R2) |

### Windows: memory-locking privileges

| id | fact | tag |
|---|---|---|
| h7-vlock | `VirtualLock` succeeds (returns 1) on a 64 KiB committed region after `SetProcessWorkingSetSizeEx(min+16 pages, max+64 pages, QUOTA_LIMITS_HARDWS_MIN_ENABLE \| QUOTA_LIMITS_HARDWS_MAX_DISABLE)` — no privilege, no elevation | [MEASURED 2026-08-12]; sequence owned by reference/memory_residency_manifest.md section M6 |
| h7-largepage | Large pages (`MEM_LARGE_PAGES`) are the one residency feature needing a privilege: `SeLockMemoryPrivilege` ("Lock pages in memory" policy), granted per machine — a deployment row, never assumed | [CC-FACT — verify: `GetLargePageMinimum()` for size, privilege via secpol]; decision reference/memory_residency_manifest.md section M6 |

### Latency-floor / power requests (booklet section 11.3 levy)

| id | leg | mechanism | tag |
|---|---|---|---|
| h7-cstate-linux | Linux | hold `/dev/cpu_dma_latency` open with a written bound while streaming — the character-device latency hold desktop audio infrastructure already uses; released at stream stop | [ESTABLISHED: booklet section 11.3 for the posture] + [CC-FACT for the device path] |
| h7-cstate-win | Windows | the corresponding execution/power request; exact mechanism (power-plan processor-idle policy vs. a power availability request) | [UNVERIFIED — decide and measure in reference/optimization_microarch_manifest.md section P9; booklet section 11.3 names the obligation, not the spelling] |

### Both legs: the grant is evidence

Read back the achieved class/priority/task handle, report it, and let the wakeup-latency histogram be the judge — the only elevation that counts is the one the tail shows [ESTABLISHED: booklet section 11.1]. Wiring: reference/observability_flightring_manifest.md sections O4/O5; shortfall policy is the composition root's recorded decision (reference/error_tracing_contract_manifest.md section E2). Route: runtime-catchable (read-back check at go-live) + target-test-catchable (histogram assertions in the soak, reference/quality_gates_ci_manifest.md section G7).

## H8. ISA floor and flag anchors

### The floor

| id | fact | tag |
|---|---|---|
| h8-floor | ISA floor: **`x86-64-v3`** — AVX, AVX2, FMA, BMI1, BMI2, F16C, LZCNT, MOVBE, OSXSAVE per the psABI microarchitecture levels | [ESTABLISHED: x86-64 psABI, microarchitecture levels] + [ESTABLISHED: booklet section 1.2] |
| h8-avx512 | AVX-512 is **out of the class**: not in v3, and the reference part fuses it off with E-cores enabled | [CC-FACT]; any ladder rung above v3 is runtime-dispatch business, reference/dsp_kernel_patterns_manifest.md section K5 |
| h8-line | cache line 64 B (pads and false-sharing math assume it) | [ESTABLISHED: booklet section 1.2] |
| h8-pages | page 4 KiB; large page 2 MiB (Linux: THP/hugetlbfs; Windows: `MEM_LARGE_PAGES`, size via `GetLargePageMinimum`) | 4 KiB [ESTABLISHED: booklet section 1.2]; 2 MiB mechanisms [CC-FACT]; adoption reference/memory_residency_manifest.md sections M5/M6 |
| h8-tsc | invariant TSC required by the class; Linux check: `constant_tsc nonstop_tsc` in `/proc/cpuinfo` flags; Windows: QPC rides the invariant TSC on such hardware | class requirement [ESTABLISHED: booklet section 1.2]; check commands [CC-FACT] |

### Flag anchors

Spellings are owned by reference/toolchain_build_manifest.md section B2 and enforced by config/toolchain-clang64-windows.cmake / config/toolchain-linux-clang.cmake; the hub owns the facts they must encode:

| id | rule | enforcement route |
|---|---|---|
| h8-march | Kernel TU class compiles `-march=x86-64-v3` — the floor's one spelling, identical on both legs | build-catchable (toolchain files) [ESTABLISHED: booklet section 10.2] |
| h8-no-native | `-march=native` is banned everywhere: it silently raises the floor above the class and breaks the cross-leg exact-golden gate | build-catchable (toolchain file rejects); gate reference/quality_gates_ci_manifest.md section G6 |
| h8-parity | `-march` and `-ffp-contract` spellings must be leg-identical — one code generator + one flag set is what makes bit-exact cross-leg golden masters achievable | build-catchable [ESTABLISHED: booklet section 10.1] |

### Measured codegen anchors (this machine, this clang)

| id | anchor | result |
|---|---|---|
| h8-saxpy | `clang -c -O3 -march=x86-64-v3 -Rpass=loop-vectorize` on a restrict-qualified float saxpy | `remark: vectorized loop (vectorization width: 8, interleaved count: 4)` [MEASURED 2026-08-12] — width 8 × f32 = 256-bit YMM, confirming AVX2 codegen; the remark-gate baseline (reference/toolchain_build_manifest.md section B8) |
| h8-mxcsr | `_MM_SET_FLUSH_ZERO_MODE(_MM_FLUSH_ZERO_ON)` + `_MM_SET_DENORMALS_ZERO_MODE(_MM_DENORMALS_ZERO_ON)` | MXCSR = **0x9fc0** (FTZ\|DAZ set) [MEASURED 2026-08-12] — the per-RT-thread FP regime's check value. MXCSR is per-thread state: every RT thread sets it at start and a guard can assert `_mm_getcsr() == 0x9fc0` on entry [CC-FACT]; policy reference/rt_plane_rules_manifest.md section R5, hygiene reference/dsp_kernel_patterns_manifest.md section K7 |
| h8-mca | `llvm-mca -mcpu=alderlake` on `clang -S` output | works; reports `Dispatch Width: 6` [MEASURED 2026-08-12] — static-analysis lane of reference/optimization_microarch_manifest.md section P3. The `alderlake` model is the P-core; E-core analysis needs a different `-mcpu` [CC-FACT — check `llvm-mca -mcpu=help`] |

### Class-level microarchitecture anchors

| id | anchor | value | tag |
|---|---|---|---|
| h8-fma | FMA latency × throughput on the class | latency 4–5 cycles, throughput 2/cycle (two FMA-capable ports) → ~8–10 independent accumulator chains to saturate | [CC-FACT — verify per kernel with llvm-mca (h8-mca)]; the reasoning that consumes it is booklet section 9.2; recipes reference/optimization_microarch_manifest.md section P4 |
| h8-dispatch | P-core dispatch width | 6 (llvm-mca alderlake model) | [MEASURED 2026-08-12 via h8-mca] |
| h8-latency-tables | full per-instruction latency/port tables | **not curated here** — generated per kernel by llvm-mca at analysis time; the hub pins only the anchors above | [OPEN: ASSUMED — curating a static table would rot; llvm-mca is the living source, per reference/optimization_microarch_manifest.md section P3] |

## H9. Re-check triggers

### Trigger table

Each trigger re-runs the named checks **before** the affected hub rows advance their dates — the booklet's toolchain-bump ritual, industrialized [ESTABLISHED: booklet sections 10.2, 14.6, 16.3].

| trigger | what re-runs | hub rows re-dated | wiring |
|---|---|---|---|
| clang major bump (either leg) | remark gates, bench suite, golden masters, sanitizer smoke, capability rows (poison/wrap/atomics) | H3 inventory, H4-clang, H5 matrix, h8-saxpy/h8-mca | reference/quality_gates_ci_manifest.md sections G4/G7; reference/testing_verification_manifest.md section T12; reference/toolchain_build_manifest.md section B8 |
| MSYS2 rolling update (`pacman -Syu`) | `pacman -Q` inventory diff; triple check; ASan/UBSan/fuzzer runtime presence; one full gate run | all of H3, H5 Windows column | h3-update-gate; config/check.sh |
| Windows feature update / servicing baseline change | MMCSS row (h7-mmcss), VirtualLock row (h7-vlock), WASAPI period probe (h6-wasapi-minper), SystemResponsiveness read | H2-os, H6 WASAPI, H7 Windows rows | reference/testing_verification_manifest.md section T6 (port contract suite on real device) |
| Linux kernel/distro bump | ALSA open/negotiate probe, rtkit presence, limits.d read, throttle read | H4, H6 ALSA, H7 Linux rows | reference/testing_verification_manifest.md section T6; deployment checklist reference/quality_gates_ci_manifest.md section G7 |
| new microarchitecture admitted to the class | cost-model anchors (h2-lat-*), FMA/dispatch anchors, `-mcpu` model availability, bench baselines re-established per core class | H2, H8 | reference/optimization_microarch_manifest.md sections P2/P3; class floor table review per booklet section 1.2 |
| new audio-API generation (WASAPI interface, ALSA behavior change) | device adapter port-contract suites + fault-injection lane on real hardware | H6 | reference/testing_verification_manifest.md section T6; reference/device_adapter_manifest.md section D8 |
| component appears/disappears in a leg (e.g. TSan lands on Windows, BOLT in CLANG64) | H5 matrix re-run; CI lanes re-wired | H5 | reference/quality_gates_ci_manifest.md section G5; config/ci-github.yml |

### The re-verification command set

The drift check, runnable as one block in a CLANG64 shell (Linux analogues inline):

```sh
clang --version && clang -dumpmachine            # h3-clang / h3-pure-2 (expect 22.x / x86_64-w64-windows-gnu)
pacman -Q | grep mingw-w64-clang-x86_64          # H3 inventory diff
ls "$(clang -print-resource-dir)/lib/windows" | grep -Ei 'asan|ubsan|fuzzer|tsan'   # H5 (lib/linux on Linux)
llvm-mca --version && llvm-bolt --version        # h8-mca present; h5-bolt expect absent on Windows
pkg-config --modversion alsa                     # h6-alsa-ver (Linux leg)
cat /proc/sys/kernel/sched_rt_runtime_us         # h7-throttle (Linux leg, expect 950000)
ulimit -r; ulimit -l                             # h7-limits (Linux leg)
cmd //c ver                                      # h2-os build number
reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile" //v SystemResponsiveness  # h7-sysresp
```

The doubled slashes (`//v`, `//c`) are deliberate: MSYS2 shells rewrite single-slash switches as POSIX paths before the Windows tool sees them; `//` escapes the conversion [CC-FACT — MSYS2 path-conversion mechanics]. From cmd/PowerShell, use single slashes.

Rule row:

| id | rule | enforcement route |
|---|---|---|
| h9-gate | A release rung (reference/quality_gates_ci_manifest.md section G7) does not pass with a hub verification date older than the toolchain identity embedded in the candidate's build id (reference/toolchain_build_manifest.md section B10) | build-catchable (check.sh compares dates) [OPEN: ASSUMED — comparison not yet implemented] |
| h9-cadence | Update cadence: `pacman -Syu` + drift block monthly and before every release rung; never mid-endeavour without re-running gates | contract-only [OPEN: ASSUMED — cadence is a project convention, adjust when CI reality arrives] |

### The OPEN register (decisions this hub refuses to invent)

NEEDS-INPUT — someone must decide: Linux reference deployment and distro (h1-leg-linux, H4 register); glibc/alsa-lib exact pins (h4-glibc-ver, h6-alsa-ver); PipeWire/JACK-native adapter adoption (H6). ASSUMED — provisional, revisit on contact with reality: Windows OS floor 10 21H2+/11 (h6-wasapi-floor); WASAPI shared-low-latency default path (h6-wasapi-default); Linux grant attempt order (h7-order); glibc-not-musl (h4-libc); kernel floor "maintained LTS" (h4-kernel); update cadence (h9-cadence); version-literal audit regex (h1-route); hub-date gate comparison (h9-gate).

---

Maintenance: this file changes only via the h1-redate procedure (re-run the row's command, then edit); every edit is followed by a config/check.sh run, and the file's git history is the drift log the H9 triggers append to.
