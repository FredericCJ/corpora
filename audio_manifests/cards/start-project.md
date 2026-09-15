# Card: start a project

**Zero to a repo where both legs build, both legs test, and check.sh gates — before any DSP exists.**

Facts verified 2026-08-12. Version-dependent claims route to reference/audio_platform_baseline_manifest.md (the hub); if any file disagrees with the hub, the hub wins.
Reasoning root: the child booklet `realtime-audio-pc-architecture-and-design-r1.md` (repo root). This card operationalizes it; it never re-argues it.

**Load when:** creating a new real-time audio codebase under this package, or re-validating a scaffold that predates it.
**Depth:** reference/audio_platform_baseline_manifest.md sections H2–H4 (environment), reference/toolchain_build_manifest.md section B5 (CMake+Ninja), reference/quality_gates_ci_manifest.md section G2 (check.sh). Next cards: cards/build-and-flags.md, cards/write-tests.md.

## The standard this card serves

**The empty skeleton already passes every gate a shipping build must pass — gates first, DSP after.** A rule with no enforcer is a preference [ESTABLISHED: booklet ch. 3 meta-invariant], and the day-one registries are what make every later failure artifact self-locating.

## Step 0 — toolchain

Windows leg: all shell work happens inside the MSYS2 **CLANG64** environment — never another MSYS2 flavor; mixed-runtime binaries are the ecosystem's classic wound, and the build asserts the triple and CRT linkage (route: build-catchable) [ESTABLISHED: booklet section 10.1].

| act | command / fact | tag |
|---|---|---|
| verify compiler | `clang --version` → 22.1.8, target `x86_64-w64-windows-gnu`, UCRT | [MEASURED 2026-08-12] |
| install build drivers | `pacman -S mingw-w64-clang-x86_64-cmake mingw-w64-clang-x86_64-ninja` | [MEASURED 2026-08-12: repo carries 4.3.4-1 / 1.13.2-1; not preinstalled on the reference machine] |
| verify the rest | clang/lld/llvm/clang-tools-extra/clang-analyzer/compiler-rt 22.1.8-1; lldb; llvm-mca/profdata/cov/nm/objdump; make 4.4.1; python 3.14.6; winpthreads + UCRT crt 14.0.0.r150 (`pacman -Q`) | [MEASURED 2026-08-12] — the normative row set lives in the hub [VERSION-DEPENDENT - hub H3] |

Linux leg: same clang major, distro or upstream packages; floor and rows are hub facts [VERSION-DEPENDENT - hub H4].

## Step 1 — scaffold the layout

The layout is dictated, not chosen [ESTABLISHED: booklet section 5.5]:

```
core/            kernels, graph compiler, schedule executor, parameter system — OS-free (invariant 8)
ports/           port headers (audio device, thread, clock, residency, telemetry, storage, control)
adapters/alsa/   adapters/wasapi/   adapters/posix/   adapters/win32/
shell/           composition root + control plane
test/            suites — cards/write-tests.md
tools/           offline renderer, bench harness, project-authored map-file audit (G3)
config/          verbatim copies of this package's config artifacts (step 2)
```

Include-graph law the skeleton must already obey: `core/` includes only `core/` + `ports/` (+ the compiler port); adapters never include each other across legs; only composition roots include adapters (route: build-catchable — config/audit_includes.py) [ESTABLISHED: booklet section 15.3].

## Step 2 — copy config artifacts verbatim

Copy from this package's `config/`; do not retype, do not "improve" while copying.

| artifact | destination in new repo | forced by |
|---|---|---|
| config/CMakePresets.json | repo root | CMake preset lookup [CC-FACT] |
| config/toolchain-clang64-windows.cmake, config/toolchain-linux-clang.cmake | `config/` (paths the presets reference — keep as shipped) | preset file contents; reference/toolchain_build_manifest.md section B5 |
| config/.clang-format, config/.clang-tidy | repo root | clang tools search upward from the source file [CC-FACT] |
| config/rt_prelude_poison.h | `config/`; force-included into RT-class TUs by the build system, never by politeness | [ESTABLISHED: booklet section 15.2] |
| config/check.sh | repo root | [OPEN ASSUMED: root placement; the wiring contract is reference/quality_gates_ci_manifest.md section G2] |
| config/ci-github.yml | `.github/workflows/ci.yml` | GitHub Actions fixed path [CC-FACT] |
| config/session_report.schema.json | `config/` — the schema every session report validates against | reference/error_tracing_contract_manifest.md section E8 |
| config/audit_includes.py, config/audit_symbols.py | `config/` | reference/quality_gates_ci_manifest.md section G9 (config/check.sh hardcodes these paths) |
| config/.gitattributes | repo root | config/ci-github.yml header comment; quality_gates_ci G5 |

## Step 3 — first build, both presets

Preset ids are owned by config/CMakePresets.json — read them there; never guess [OPEN ASSUMED: ids follow a `<leg>-<config>` scheme; reference/toolchain_build_manifest.md section B5 is normative].

```
cmake --preset <leg>-dev && cmake --build --preset <leg>-dev
```

Run it for the Windows preset (inside CLANG64) and the Linux preset. A skeleton that builds on one leg only is a broken build, not a porting task for later [ESTABLISHED: booklet section 5.5, invariant 9].

## Step 4 — first test run

```
ctest --preset <leg>-test
```

Seed `test/` with one trivially-passing test per suite family (unit, property, golden, contract) so the harness plumbing — discovery, self-locating failure output per reference/testing_verification_manifest.md section T2 — is proven before it matters. Break one on purpose once: the failure text must already name WHAT/WHERE/WHY with a repro command; if it does not, fix the harness now [OPEN ASSUMED: house practice; the output contract is T2's].

## Step 5 — wire check.sh

`./check.sh` is the single local gate ladder: build both configs, run suites, run config/audit_includes.py + config/audit_symbols.py, run the remark gate. Contract (exit nonzero, machine-readable failure pointing at the failing gate): reference/quality_gates_ci_manifest.md section G2. CI (`.github/workflows/ci.yml`) runs the same ladder on the dual-leg matrix — reference/quality_gates_ci_manifest.md section G5.

## Step 6 — day-one registries

Created before any code needs them, because stable ids from commit 1 are what make failure artifacts self-locating and machine-patchable (the doctrine):

| registry | spec | day-one content |
|---|---|---|
| error-code registry | reference/error_tracing_contract_manifest.md section E3 | the registry file with its id scheme and zero-or-few seed codes |
| event-id registry (flight ring) | reference/observability_flightring_manifest.md section O2 | id scheme + the always-on core events |
| build identity stamp | reference/toolchain_build_manifest.md section B10 | revision + toolchain + flag fingerprint embedded in every artifact [ESTABLISHED: booklet ch. 3 invariant 17] |

## Step 7 — composition root skeleton

`shell/main.c` carries the sanctioned go-live order as numbered stubs from day one — the order is architecture [ESTABLISHED: booklet section 4.5]: (1) read+validate config, (2) negotiate device, (3) compile graph, (4) allocate everything RT will ever touch, (5) lock + prefault, (6) spawn RT threads — elevation/placement/FTZ requested, grants reported, (7) warm up against silence, (8) arm monitors, open the gate. Teardown mirrors it in reverse (two-phase termination). No effects before their owner exists: nothing touches the device or spawns threads from module init.

## Never

- Build the Windows leg outside CLANG64, or mix MSYS2 environments (route: build-catchable triple/CRT assert) [ESTABLISHED: booklet section 10.1].
- Add a TU without declaring its class — cards/build-and-flags.md (route: build-catchable).
- Let `core/` include an OS header, even in the skeleton (route: build-catchable — the include audit) [ESTABLISHED: booklet ch. 3 invariant 8].
- Start writing DSP before check.sh is green on both legs.
- Defer the registries "until there are errors" — retrofitted ids are unstable ids.
- Retype or edit config artifacts while copying; changes go through canon review (cards/build-and-flags.md).

## Decisions you must not invent

- Product/symbol prefix and binary name — [OPEN NEEDS-INPUT].
- Default device path per product: ALSA `hw:` direct vs mixer/server route; WASAPI shared vs exclusive — [OPEN NEEDS-INPUT; booklet section 5.2 makes it product configuration].
- Supported rate/period matrix and the period default (DT-1) — [OPEN NEEDS-INPUT].
- CI runner inventory for the dual-leg matrix and release soak rigs — [OPEN NEEDS-INPUT].
- License and third-party policy — [OPEN NEEDS-INPUT].
- Repo-relative destinations marked ASSUMED above — confirm against config/CMakePresets.json when it lands [OPEN ASSUMED].

## What you owe when done

The first commit already owes what every later change owes: check.sh green locally, both legs green in CI at the full warning canon, the trivially-passing suite skeleton running, registries and build-identity stamp in place. That is reference/testing_verification_manifest.md section T11 applied to a change whose diff is the whole repo, and the gate ledger of reference/quality_gates_ci_manifest.md section G1 starts life complete — every failure from here on is a self-locating artifact, not archaeology.

## Go deeper

| question | where |
|---|---|
| reference machine, environments, package rows | reference/audio_platform_baseline_manifest.md sections H2–H4 |
| CMake+Ninja wiring, presets, TU classes | reference/toolchain_build_manifest.md sections B5, B1 |
| build identity stamp mechanics | reference/toolchain_build_manifest.md section B10 |
| check.sh contract and the gate ledger | reference/quality_gates_ci_manifest.md sections G2, G1 |
| structural audits the skeleton must pass | reference/quality_gates_ci_manifest.md section G3 |
| error-code and event-id registries | reference/error_tracing_contract_manifest.md section E3; reference/observability_flightring_manifest.md section O2 |
| the composition-root order, argued | booklet section 4.5 |
