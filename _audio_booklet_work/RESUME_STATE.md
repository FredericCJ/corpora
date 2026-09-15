# Real-time audio child booklet — endeavour state

**Status: WRITTEN r1.0, 2026-08-12. Audit gate CLEAN. NOT committed (not requested — house
default: commit only on request).**

## Deliverables

- `E:\dev\corpora\realtime-audio-pc-architecture-and-design-r1.md` — the booklet (~193 KB,
  7 parts, 17 chapters, 94 subsections, 20 invariants, 7 decision trees DT-1…DT-7).
  First child of `embedded-c-architecture-and-design-r1.md` (r1.5) per its ch. 15 contract;
  ch. 16 fills the parent's 10-row pin table; ch. 17 carries works + editorial + EXTERNAL
  registers (the corpus has no audio/DSP/SIMD/µarch/OS-scheduler material — verified by sweep).
- `realtime-audio-pc-architecture-and-design-r1.html` — house-styled render (222 KB, 26 TOC
  entries); regenerate with `python _audio_booklet_work/build_html.py`.
- `_audio_booklet_work/audit.py` — **the seal gate**; CLEAN required before any commit.
  Checks: 93 kebab + 40 single-word catalog ids vs `SWE/explorer/data/elements.json` (both
  work registries merged), 28 work stances vs records (dreppermem + posa2 carried UNVERIFIED),
  all §/chapter/invariant xrefs, **parent-directed refs validated against the parent booklet
  itself** (8 sections), structural counts (17 ch / 20 inv / "Twenty statements").
- `_audio_booklet_work/OUTLINE.md` — the writing map (commission R1–R11, invariant drafts,
  measured machine facts).

## Scope pins (the commission)

PC-class x86-64 (`x86-64-v3` floor; reference machine = i9-12900K hybrid 8P+8E/24T, 30 MB L3,
32 GB, Win11 Pro); Linux + Windows NT, one codebase; C17; clang/LLVM both legs — Windows =
MSYS2 CLANG64 (clang 22.1.8 measured 2026-08-12; ASan/UBSan/libFuzzer present, **no TSan, no
BOLT** → Linux-leg techniques); correctness = C11 memory model, never x86-TSO.

## Structure (17 chapters)

I: 1 machine (hybrid/caches/OS-as-peer/audio stacks, callback=courier-mapping) · 2 prime
contract (period math, two planes, quasi-RT honesty, xrun taxonomy, DT-1) · 3 twenty invariants.
II: 4 core=compiled graph (schedule as bytecode, composition root) · 5 ports (ALSA/WASAPI,
thread port refuses C11 threads, single-codebase mechanics, compiler port narrowed).
III: 6 concurrency (no-locks argument, 5-channel menu, DT-2/3/4/5, C11-ordering discipline) ·
7 two clocks (drift, latency accounting §7.3, timers §7.4).
IV: 8 memory (residency, RT stacks, DT-6 allocation classes, SoA/false-sharing/4K-stagger,
huge pages).
V: 9 microarchitecture (ILP/accumulators, IIR chains, structural+control hazards, flush
inventory, FTZ/DAZ + FP regime, SIMD ladder + scalar twins, DT-7) · 10 toolchain (CLANG64
anatomy, flag canon by TU class, ThinLTO, PGO-from-offline-renderer, BOLT Linux-only, bench
protocol, sanitizer matrix) · 11 OS (SCHED_FIFO/rtkit vs MMCSS, P/E placement, C-state holds,
autopsy, deployment-hardening table, refusals).
VI: 12 errors (dispositions per plane, degrade ladder→fade-to-silence, device loss, output
sentinel, watchdog analog) · 13 flight recorder (always-on histograms/counters, session report,
replay, crash harvest).
VII: 14 testability (offline renderer, exact+tolerance goldens cross-leg, block-partition
property, fault/concurrency suites, CI matrix + soak) · 15 enforcement (routes instantiated,
RT guard: poison headers + wrap interposition + plane tag; nm/include/map audits; budgets;
contract-only register) · 16 compliance (pin table filled, tightenings: inv 2,3,9,13; version
hub declared → future `audio_manifests/`; OPEN register for grandchildren) · 17 lineage.

## Works cited (28; stances audited)

New-to-child verified: hennessypatterson, herlihyshavit, perfbook, kernelsyncdoc, preshing,
sharajkumar90, drepperfutex, mattsonppp, mccoolspp, blumofeleiserson, lmaxdisruptor, lmaxfowler,
kerrisktlpi, drepperlibs, levine, thinlto, thinltoblog, clangdocs, clangtidy, clangformat, lld,
godbolt, asan. UNVERIFIED carried: dreppermem, posa2. Inherited backdrop: liulayland, buttazzo,
kopetz. NOTE: elements.json has its OWN works registry (417) beside corpus.json (468), only 81
shared — hennessypatterson/herlihyshavit/perfbook/sharajkumar90 exist ONLY in elements.json.

## If resuming / extending

Edit the .md → `python _audio_booklet_work/audit.py` (CLEAN required) →
`python _audio_booklet_work/build_html.py` → commit only on user request.
Natural next moves (not requested): (a) convergence iterations like the parent's r1.1–r1.5
program (adversarial review lenses: RT/concurrency correctness; µarch/toolchain claims;
OS-mechanics claims); (b) spawn `audio_manifests/` version hub (founding rows enumerated in
§16.3); (c) grandchildren per §16.4 (plugin hosting, engine/UI split, JACK/PipeWire adapters,
ARM64 leg); (d) corpus pass to promote the EXTERNAL register (Bencina, Agner Fog, Intel SDM,
WASAPI/ALSA/MMCSS docs) into works records.
