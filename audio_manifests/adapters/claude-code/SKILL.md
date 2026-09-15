---
name: audio-rt-ground
description: Grounding for writing, reviewing, testing, diagnosing and optimizing real-time audio C17 on Linux and Windows NT with the clang/LLVM toolchain (MSYS2 CLANG64 on Windows). Use when implementing or changing DSP kernels or audio ops, writing real-time audio callbacks or anything on the RT plane, building WASAPI or ALSA device adapters, adding lock-free/wait-free audio threading (SPSC rings, snapshot swap, seqlock, atomic parameters), diagnosing xruns, glitches, underruns, denormal storms or audio latency problems, tuning latency or buffer/period sizes, choosing build flags, CMake toolchains or sanitizers for CLANG64/Linux clang, writing tests or golden masters for DSP code, handling device loss or format change, adding counters/events/session reports to an audio engine, benchmarking or SIMD-optimizing kernels, or setting up CI gates for a real-time audio codebase. Also use when asked which allocator, lock, or syscall is legal on an audio thread, or how to verify FTZ/DAZ, MMCSS, or SCHED_FIFO elevation.
---

# Audio RT Ground

Layered grounding for real-time audio engineering in C17 on Linux and Windows (clang/LLVM, MSYS2
CLANG64). **Load progressively — never the whole package**; you need a few thousand tokens, not
the corpus.

Set `$PKG` to wherever the package is vendored — typically `.agent/audio-rt-ground/`. If you
cannot find it, look for a directory containing `AGENTS.md` alongside `cards/` and `reference/`.

## Step 1 — always

Read **`$PKG/AGENTS.md`**. It carries the non-negotiables (the two planes, the invariants in
force), the epistemic tag protocol, the seven enforcement routes, and the task router.

## Step 2 — load exactly one card

From `$PKG/cards/`, matched to the task:

| task | card |
|---|---|
| new project, repo layout, toolchain and CMake choices | `start-project.md` |
| build flags, TU classes, warnings, LTO/PGO, linking | `build-and-flags.md` |
| writing or changing a DSP kernel / audio op | `write-dsp-kernel.md` |
| any code that runs on the RT plane (callbacks, RT workers) | `write-rt-code.md` |
| cross-plane communication: rings, mailboxes, atomics, shutdown | `concurrency-channels.md` |
| ALSA/WASAPI adapters, device setup, negotiation, recovery | `device-adapters.md` |
| tests: harness, goldens, properties, fault injection | `write-tests.md` |
| **any red artifact**: failed test, sanitizer hit, golden diff, bench regression, xrun, guard trip, crash, CI gate | `diagnose-failure.md` |
| error handling: codes, results, adapter conversion, checks | `handle-errors.md` |
| events, counters, histograms, session report, logging | `observability.md` |
| performance work of any kind | `optimize-performance.md` |
| CI, gates, check.sh, ratchets, release rungs | `gates-and-ci.md` |
| reviewing a diff, or final-checking your own work | `review-code.md` |

If two apply, load the one matching what you are about to *do*, not what the code is *about*.
Finishing a code change always ends with `review-code.md`.

## Step 3 — reference sections, only as named

Cards name sections by letter+number id (`R2`, `T11`, `P7`, hub `H5`). Open **that section**, not
the file:

```sh
grep -n '^## ' $PKG/reference/rt_plane_rules_manifest.md      # find the "## R2. ..." line
sed -n '140,190p' $PKG/reference/rt_plane_rules_manifest.md   # read the slice
```

`$PKG/INDEX.json` maps every section id to its file and line (`jq`/`grep` it; do not read it
whole). Version-dependent facts live in one place:
`reference/audio_platform_baseline_manifest.md` — **the hub**. If any file disagrees with the
hub, the hub wins and that file is stale.

## Step 4 — config, copied not derived

For any configuration artifact, **copy from `$PKG/config/`**, then adapt minimally:

`toolchain-clang64-windows.cmake` · `toolchain-linux-clang.cmake` · `CMakePresets.json` ·
`.clang-format` · `.clang-tidy` · `rt_prelude_poison.h` · `check.sh` · `ci-github.yml` ·
`session_report.schema.json` · `audit_includes.py` · `audit_symbols.py`

Composing a toolchain file or a tidy check set from prose is how a flag that does not exist ends
up in a real build. The poison prelude and the audit scripts are enforcement machinery — wire
them, do not re-derive them.

## Non-negotiable conduct

- **Never invent an identifier.** A fabricated compiler flag, API name, HRESULT, pacman package,
  tidy check, or version gets pasted into a build and silently disables a control. If you cannot
  verify it, leave it out and say so.
- **Where a claim is about what the toolchain does, run the tool** — `clang -Rpass=loop-vectorize`,
  `llvm-mca`, `llvm-nm`, the audit scripts — and record the command and version. House rule: run
  the tool, do not read its docs. Documentation states intent; the tool's output is the fact.
- **`OPEN` means decide and say so**, split as **ASSUMED** (you took the stated default) or
  **NEEDS-INPUT** (you need the owner). Never resolve one silently.
- **Version facts route to the hub** (`reference/audio_platform_baseline_manifest.md`); per-leg
  tool availability (TSan, BOLT, fuzzer) is a hub matrix, not folklore.
- These are **grounding, not rules**. Cite one when it shapes a decision; reason past it when the
  situation genuinely differs — and say which you did.

## Facts expire

Verified **2026-08-12** on the reference machine (CLANG64 clang 22.1.8, Windows 11; hub section
H2). The hub's section H9 lists its re-verification triggers — toolchain majors, MSYS2 package
moves, OS baseline changes. If today is materially later, say so before presenting a version fact
as current.
