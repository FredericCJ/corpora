# Child booklet outline — real-time audio on PC-class hardware

Deliverable: `E:\dev\corpora\realtime-audio-pc-architecture-and-design-r1.md` (+ `.html`).
One unified guideline book. Child of `embedded-c-architecture-and-design-r1.md` (r1.5) per its ch. 15.
Language C17. Toolchain clang/LLVM (MSYS2 CLANG64 on Windows; clang on Linux). Dual-kernel: Linux + NT.

## Commission (user requirements, normalized)

- R1 dual-kernel applicability (Linux, NT) — chs. 1, 5, 11
- R2 one single codebase for both — chs. 5, 10, 14; invariant 9
- R3 architecture + design + rationales + decision trees for concurrent designs — Parts II–III, DT-1..7
- R4 bound to clang/LLVM — ch. 10, 16
- R5 bound to MSYS2 CLANG64, all components — ch. 10 (verified inventory 2026-08-12)
- R6 optimization techniques included — Part V
- R7 quasi-real-time techniques on a non-RT OS — chs. 2, 6, 11
- R8 compiler/linker/memory-layout optimization — chs. 8, 10
- R9 hardware-level optimization: cache locality, branch prediction, OoO, superscalar pipelining, pipeline-flush limits, hazards (data/structural/control) — ch. 9
- R10 remains embedded-class: the product IS the side effect (parent ch. 1) — ch. 2
- R11 architecture/compiler-agnostic *within* the pinned class: correct by C11/C17 memory model; fast by x86-64-v3 class — chs. 6, 9

## Parts and chapters (7 parts, 17 chapters)

- Part I — The ground, again: 1 the machine (hybrid i9-12900K reference class, non-RT OS, audio stacks, device clock = second master) · 2 the prime contract (deadline math, xrun taxonomy, quasi-RT honesty, DT-1 latency dial) · 3 the invariants (20, routed; parent's 25 inherited, tightenings named)
- Part II — Structure: 4 the core is a compiled graph (decisions-as-data schedule; composition root order) · 5 ports and the two operating systems (port list; ALSA/WASAPI adapter sets; single-codebase layout; thread port refuses C11 threads)
- Part III — Execution: 6 the two-plane concurrency architecture (iron rule; channel menu; DT-2 into-RT, DT-3 out-of-RT, DT-4 parallelize, DT-5 waiting) · 7 two clocks (device vs monotonic, drift, timestamping, end-to-end latency accounting)
- Part IV — Memory: 8 memory architecture (lock+prefault; DT-6 allocation classes; layout for locality; 4K-aliasing; guard pages)
- Part V — Mechanical sympathy: 9 the microarchitecture (ILP, branches, hazards, flush limits, SIMD ladder, FP regime, FTZ/DAZ, llvm-mca, DT-7 optimization ladder) · 10 the toolchain, pinned (flag canon, ThinLTO, IR-PGO, BOLT=Linux-only, layout control, sanitizer matrix, CLANG64 anatomy) · 11 the operating system you don't control (elevation, power/C-states, hybrid P/E placement, affinity, page-fault elimination, autopsy, SMI honesty)
- Part VI — Failure and evidence: 12 errors, overload, and the safe state (degrade ladder → fade-to-silence; xrun as designed event; RT watchdog analog) · 13 the flight recorder at 48 kHz (wait-free ring, histogram canon, session report, crash capture, build identity)
- Part VII — Proof and constitution: 14 testability (offline render, golden masters exact+tolerance, block-size invariance, port fault suites, dual-OS CI, fuzz, soak, bench protocol) · 15 enforcement ladder instantiated (incl. RT-guard interposition, nm audit, remark gates; contract-only register) · 16 the specialization compliance (parent's 10 pin rows filled; tightened invariants; OPEN register for grandchildren; version-hub declaration) · 17 lineage (works; editorial register; EXTERNAL register — domain sources not in corpus; colophon)

## Child invariants (1–20, routes inline) — drafted

1 RT thread bounded work only (no lock/alloc/blocking syscall/unbounded loop/IO) — analysis + runtime(dev-guard) + contract-only residue
2 RT-crossing channels wait-free on the RT side, bounded, declared overflow, counted drops — host-test + runtime [tightens parent 10]
3 RT-reachable memory allocated+locked+prefaulted before go-live — runtime(init assert + guard) [tightens parent 11]
4 FTZ/DAZ on every RT thread; denormal/NaN emission is a defect — runtime(dev scan) + host-test
5 deadline monitor always on; histogram + xrun counters are product features — runtime [parent 13 instance]
6 headroom floor demonstrated: p99.99 ≤ 50% of period on reference class, by soak — target-test
7 overload runs the designed ladder; terminal rung fade-to-silence; never blocks/crashes — host-test(fault inj) + runtime
8 core OS-free: no OS header, no OS symbol — build (nm + include audits) [parent 4/7 instance]
9 one codebase: OS text only in adapters; both legs built+tested per commit — build
10 one toolchain family (clang/LLVM), one warning canon -Werror, flag parity except documented rows — build
11 FP regime pinned per TU class; no system libm on determinism paths — build + host-test (exact golden both legs)
12 every SIMD kernel has a scalar twin, equivalence-tested; dispatch binds at init — host-test [parent 5 instance]
13 no formatting/logging/printing on RT path; events → wait-free ring — analysis + runtime guard [tightens parent 19]
14 elevation/locking/placement verified at go-live; denial = reported degraded mode — runtime
15 perf claims carry bench-protocol measurements; kernel vectorization asserted by compiler remarks in CI — build + host-test
16 the latency dial is a product parameter with a tested robustness curve — host-test sweep + contract
17 build identity embedded and carried in every artifact/report/crash record — build + runtime [parent 18 instance]
18 crash/exit preserves the flight ring; overrun autopsy classifies cause in diagnosis mode — runtime [parent 18 instance]
19 device loss, format change, elevation denial: designed events with tested recovery — host-test contract suites
20 core output invariant to callback-size partitioning within the block quantum — host-test property

## Decision trees

DT-1 (ch 2) choosing the period/latency dial · DT-2 (ch 6) data into RT · DT-3 (ch 6) data out of RT ·
DT-4 (ch 6) parallelizing the graph · DT-5 (ch 6) waiting strategy per role · DT-6 (ch 8) allocation class ·
DT-7 (ch 9) where an optimization lives (ordering by leverage, measurement gates between rungs)

## Verified machine facts (2026-08-12, this machine = reference class exemplar)

- CPU 12th Gen i9-12900K: 8 P-cores (2-way SMT) + 8 E-cores = 24 threads; L1d 48K/P-core, 32K/E-core;
  L2 1.25M/P-core, 2M per 4-E-core cluster (14 MB total); L3 30 MB shared; 64B lines; hybrid topology
- RAM 32 GB; Windows 11 Pro; 4 KiB pages
- MSYS2 CLANG64: clang 22.1.8 (x86_64-w64-windows-gnu, UCRT), ld.lld + lld-link, clang-tidy, clang-format,
  llvm-profdata, llvm-cov, llvm-nm, llvm-objdump, llvm-mca, lldb present; clang-analyzer, compiler-rt,
  libc++, libunwind, winpthreads, openmp packages installed
- ABSENT on CLANG64: llvm-bolt (BOLT is ELF/Linux-leg only), TSan runtime (Linux-leg only), cmake/ninja
  (packages exist in repo, not installed here)
- Sanitizer runtimes present on CLANG64: ASan(dynamic), UBSan, profile(PGO), libFuzzer, stats

## Corpus grounding rules (inherited)

Element ids in backticks must resolve in SWE/explorer/data/elements.json; work ids + stances vs corpus.json;
UNVERIFIED travels; editorial marked; EXTERNAL register for domain sources not in corpus (plain text, never
backticked); never invent an identifier; audit.py CLEAN before any commit.
