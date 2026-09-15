# Audio RT Ground — agent entry point

**You are building real-time audio processing in C17 that must hit its deadline on a non-real-time
OS — Linux or Windows NT, one codebase, clang/LLVM (MSYS2 CLANG64 on Windows) — and stay testable
and traceable enough that a failing artifact alone tells you what to patch.** This package is the
grounding for that. It is **GROUNDING, not a rulebook**: cite a rule when it materially shapes a
decision; reason past it when the situation genuinely differs — and say which you are doing.

**Facts verified 2026-08-12.** Version-dependent claims decay. Anything dated routes through
`reference/audio_platform_baseline_manifest.md` (the hub). **If any file disagrees with the hub
about a version, the hub wins and that file is stale.** The reasoning root behind this package is
the booklet `E:\dev\corpora\realtime-audio-pc-architecture-and-design-r1.md` (child of the house
embedded-C parent): the package operationalizes it and never re-argues it —
`reference/booklet_map.md` maps topics to its chapters.

## Why this package is shaped the way it is

**Testability and traceability are your feedback loop.** You will patch this codebase by reading
error traces, logs, and test reports — so every rule here conspires to make failure artifacts
**self-locating and machine-parseable**: test ids name the module and the contract; check failures
print expected/actual/seed/build-id on one parseable line; xruns carry autopsies; the session
report is schema-versioned JSON. **The failure→patch loop**: red artifact → read its fields → the
id names the contract → the contract names the owning module and reference section → patch → rerun
the named gate. `cards/diagnose-failure.md` is the dispatch table. Never patch without reading the
artifact's fields; never call it fixed without rerunning the named gate.

## How to use this package — do not read it all

| layer | what | when |
|---|---|---|
| **this file** | non-negotiables + router | always, ~3k tokens |
| `cards/*.md` | one compact card per task | load the **one** that matches your task, ~2k tokens |
| `reference/*.md` | the full manifests | **only** the section a card names. Never a whole file. |
| `config/*` | ready-made artifacts | copy verbatim; do not re-derive |
| `INDEX.json` | every indexed section | query with `grep`/`jq`; **never read into context** |

## The task router

| your task | load this card |
|---|---|
| scaffold the project, install toolchain, first build | `cards/start-project.md` |
| build system, flags, presets, toolchain trouble | `cards/build-and-flags.md` |
| write or change a DSP kernel / op | `cards/write-dsp-kernel.md` |
| write or change code on the real-time plane | `cards/write-rt-code.md` |
| share data across threads, add a channel, workers | `cards/concurrency-channels.md` |
| ALSA/WASAPI device work, negotiation, stream faults | `cards/device-adapters.md` |
| write or fix tests, golden masters, properties | `cards/write-tests.md` |
| **any red artifact: test, sanitizer, xrun, crash, CI** | `cards/diagnose-failure.md` |
| error handling, error codes, fault verbs | `cards/handle-errors.md` |
| events, counters, histograms, session report | `cards/observability.md` |
| performance work, benches, SIMD, PGO | `cards/optimize-performance.md` |
| CI, gates, audits, what blocks a merge | `cards/gates-and-ci.md` |
| review a diff, or final-check your own work | `cards/review-code.md` |

Finishing any code change ends with `cards/review-code.md`.

## How to read a claim — the tag protocol

| tag | means | what you do |
|---|---|---|
| **ESTABLISHED** | normative in the named primary source | rely on it |
| **VERSION-DEPENDENT** | true of the named version only — routes to a hub row | check yours |
| **MEASURED** | established by *running* it; command and date named | strongest tag |
| **OPEN** | a project decision — **ASSUMED** (stated default) or **NEEDS-INPUT** | surface it; never improvise silently |
| **FLAGGED-SECONDARY** | secondary evidence only | verify before load-bearing use |
| **UNVERIFIED** | asserted by a source, unconfirmed | treat as a lead |
| **CC-FACT** | model/tool knowledge without a named primary source | verify before it becomes load-bearing; expected for API mechanics |

An **untagged factual claim in `reference/` is a defect** — report it rather than trusting it.

## Enforcement routes

Every rule names what enforces it, or admits nothing does. This family uses the booklet's seven
routes (the python ground's six map onto them; same law, different toolchain):
`compiler-catchable` · `analysis-catchable` · `build-catchable` · `host-test-catchable` ·
`target-test-catchable` (real machine, real audio device) · `runtime-catchable` ·
**`contract-only`** (nothing mechanical catches it — an honest admission, reviewed by name).
**A rule you cannot route is a preference.**

## The twenty non-negotiables

**Toolchain**
1. **One toolchain family, both legs**: clang/LLVM, one warning canon at `-Werror`, and flags come
   from the TU-class canon — never ad hoc per file. → `reference/toolchain_build_manifest.md` §B2
2. **Environment purity on Windows**: build in CLANG64 only; never mix objects across MSYS2
   environments; assert the `x86_64-w64-windows-gnu` triple and UCRT linkage. → hub §H3
3. **Version facts live only in the hub** — tools, packages, API generations, kernel baselines.

**The real-time plane**
4. **The RT plane does bounded work only**: no lock, no allocation, no blocking syscall, no I/O,
   no formatting, no unbounded loop. The development guard traps violations — the trap firing **is
   the feedback loop working**, not an obstacle to code around. → `rt_plane_rules` §R2
5. **Everything crossing the plane boundary uses one of the five channels** — wait-free on the RT
   side, bounded, overflow counted, never silent. → `concurrency_channels` §C1
6. **All RT-reachable memory is allocated, locked, and faulted in before go-live** — none after.
   → `memory_residency` §M5/§M6
7. **FTZ/DAZ set on every RT thread**; a denormal or NaN in nominal operation is a defect. → §R5
8. **Concurrency is written in the C11 memory model** — the four blessed idioms; a bare
   sequentially-consistent atomic is unreviewed code; `volatile` is not a concurrency tool. → §R6

**Structure**
9. **The core is OS-free** — no OS header on its include path, no OS symbol in its objects;
   enforced by the include and symbol audits, not by intention. → `quality_gates_ci` §G3
10. **One codebase**: kernel-specific text lives only in adapters; every commit builds and tests
    both legs. → §G5
11. **Ports own their vocabulary** (frames, periods, formats); adapters convert native errors and
    handles at the boundary, once, preserving the native value for forensics. → `device_adapter`
    §D1, `error_tracing_contract` §E5

**Testability**
12. **Every change owes tests per the what-a-change-owes matrix** — a new op without its golden,
    properties, and twin does not merge. → `testing_verification` §T11
13. **Tests are self-locating**: stable ids (`suite.module.contract.case`), machine-parseable
    failure output carrying expected/actual, repro seed, artifact path, and build identity. A
    failing test names the module and the contract. → §T2
14. **The offline renderer is the harness**: deterministic, seeded, faster than real time; field
    sessions replay through it; goldens, PGO, and CI all drive it. → §T3

**Traceability**
15. **No failure without an artifact; no artifact without build identity.** → `error_tracing` §E7
16. **Error codes and event ids come from registries** — module-prefixed, stable, never reused,
    generated from one table each. → §E3, `observability_flightring` §O2
17. **The check-failure line is a frozen, machine-parseable contract**
    (`CHECK-FAIL id=… expected=… actual=… build=…`) — it is what you parse to patch. → §E6
18. **The session report is the universal evidence artifact** — schema-versioned JSON; CI gates,
    soak rigs, and bug reports all read the same file. → §E8, `config/session_report.schema.json`

**Process**
19. **A rule with no enforcement route is a preference** — route it, or register it
    `contract-only` and review for it by name.
20. **Run the tool** (record version and command). **Never invent an identifier** — a fabricated
    flag, API name, rule code, or version silently disables a check or breaks a build. **An OPEN
    is surfaced** — ASSUMED or NEEDS-INPUT — never resolved silently.

## The reference shelf

Load a **section**, not a file. Section ids are stable (`§H3`, `§T11`); `INDEX.json` maps them all.

| file | pillar |
|---|---|
| `audio_platform_baseline_manifest.md` | **the version hub** — machine class, CLANG64 inventory, sanitizer matrix, API baselines, privileges, re-check triggers |
| `toolchain_build_manifest.md` | build — TU classes, flag canon, CMake/Ninja, ThinLTO, PGO, remark gates, linking |
| `rt_plane_rules_manifest.md` | the iron rules — banned ops, guard machinery, FTZ, ordering idioms |
| `concurrency_channels_manifest.md` | the five channels with reference implementations; workers; shutdown |
| `device_adapter_manifest.md` | ALSA + WASAPI recipes, fault verbs, negotiation |
| `testing_verification_manifest.md` | **testable** — suites, naming, goldens, properties, fault injection, what-a-change-owes |
| `error_tracing_contract_manifest.md` | **traceable** — failure→patch loop, code registry, check-line contract, evidence chain, session report |
| `observability_flightring_manifest.md` | evidence — event schema, flight ring, histograms, counters, diagnosis mode |
| `memory_residency_manifest.md` | allocation classes, locking per leg, stacks, layout budgets |
| `dsp_kernel_patterns_manifest.md` | kernel shape, add-an-op walkthrough, SIMD ladder + twins, FP regime |
| `optimization_microarch_manifest.md` | the ladder, bench protocol, stall dispatch table, PGO/BOLT, OS techniques |
| `quality_gates_ci_manifest.md` | the gate ledger, check.sh parity, audits, dual-leg CI, the ratchet |
| `booklet_map.md` | topic → booklet chapter map (the reasoning root, one hop away) |

Provenance, the build plan, and the audit gate are in `_work/`.
