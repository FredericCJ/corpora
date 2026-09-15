# Real-Time Audio on the Unconstrained Machine

**Architecture, design, and mechanical sympathy for PC-class real-time audio in C — a specialization
booklet, child of *Architecture and Design of Complex Embedded C Programs* (r1.5)**

Principles for building real-time audio signal-processing programs that run on ordinary personal
computers under ordinary — non-real-time — operating systems, and still meet their deadlines: one
codebase for the Linux kernel and the Windows NT kernel, one toolchain family (clang/LLVM), and one
discipline from the architecture down through the cache line.

---

## What this booklet is

This is the **first child** of the house's embedded C parent booklet, and it inherits that book's
frame before adding a word of its own: an embedded program is a machine that turns events into
effects under budgets, and its side effects **are the product**. A real-time audio program is that
machine wearing unusual clothes. The product is a pressure wave leaving a converter at a fixed
rate; the program's one non-negotiable effect is *the next buffer of samples, delivered before the
device exhausts the last one*. Late is not slow — late is a click, a dropout, a ruined take. By the
parent's own definition (parent ch. 1) this is an embedded program, whatever the size of the
machine it runs on.

What changes is the machine — and the change cuts both ways. The targets of this booklet are
**PC-class**: multi-core, out-of-order, superscalar processors with deep cache hierarchies,
gigabytes of RAM, an MMU always present, and a general-purpose operating system in charge. The
constraints that shape classic embedded work — bytes, microamps, missing hardware — are gone.
In their place stands a subtler adversary: **an execution environment optimized for throughput
and fairness, mediated by a kernel you do not control, on hardware whose every acceleration is
statistical.** Caches, branch predictors, out-of-order windows, frequency scaling, and the
scheduler all make the *average* case fast by making the *worst* case wild — and real-time audio
is a worst-case discipline. The parent's budgets were bytes and cycles; this booklet's budget is
almost purely the **tail of a latency distribution**.

So this is a book about two disciplines that must be held at once. The first is the parent's:
boundaries, contracts, effects placed behind ports, evidence designed in, every rule routed to an
enforcer. The second is this domain's own: the craft of extracting *quasi-real-time* behavior
from a non-real-time stack — the elimination of every unbounded operation from the signal path,
the pinning of memory, priorities, and cores, and the mechanical sympathy (cache locality, branch
discipline, instruction-level parallelism, pipeline-hazard management) that keeps the per-buffer
cost so far below the deadline that the tail the OS adds cannot reach it.

**The commission.** This booklet exists to scaffold one class of programs, and its requirements
are recorded here so every chapter can be audited against them:

| # | requirement | where discharged |
|---|---|---|
| R1 | real-time audio signal processing on non-real-time operating systems | chs. 1, 2, 11 |
| R2 | targets run a Linux kernel or a Windows NT kernel; guidelines apply to both | chs. 1, 5, 11 |
| R3 | one single codebase builds for both machines | chs. 5, 10, 14; invariant 9 |
| R4 | architecture and design guidelines with rationales and decision trees for concurrent designs | Parts II–III; DT-1…DT-7 |
| R5 | bound to the clang/LLVM toolchain | chs. 10, 16 |
| R6 | bound to MSYS2 CLANG64 with every component available, as the Windows development toolchain | chs. 10, 16 |
| R7 | optimization techniques, not only architecture | Part V |
| R8 | techniques for quasi-real-time behavior on a non-real-time OS | chs. 2, 6, 8, 11 |
| R9 | compiler, linker, and memory-layout optimization in service of quasi-real-time | chs. 8, 10 |
| R10 | hardware-level optimization: cache locality, branch prediction, out-of-order execution, superscalar pipelining, pipeline-flush limits, and hazard management (data, structural, control) | ch. 9 |
| R11 | the application class remains embedded: the product is the side effect | chs. 1, 2 |

**What it pins and what it keeps agnostic.** The parent is target-, architecture-, and
compiler-agnostic; a child exists to pin. This booklet pins the platform class (PC-class x86-64,
pinned at the `x86-64-v3` ISA level), the two kernels, the language (C17), and the toolchain
family (clang/LLVM; on Windows, the MSYS2 CLANG64 environment). It stays deliberately agnostic
one level down: **correctness never rests on the pinned microarchitecture** — concurrent code is
written against the C11 memory model, not against x86's strong ordering, so the pin is a
performance floor, not a correctness assumption (§6.6). And it refuses, as the parent refuses,
every fact that decays: exact tool versions, package inventories, API generations, and kernel
baselines are *version-hub facts* (ch. 16), dated and re-checkable, never normative prose.

**Its grounding.** Like the parent, this booklet stands on the house corpus: element identifiers
appear in `this-face` and resolve in the SWE element catalogs; the works behind them are recorded
in chapter 17 exactly as the corpus records them, UNVERIFIED flags included. The domain layer —
audio subsystems, scheduler interfaces, microarchitectural behavior, toolchain mechanics — has
**no corpus behind it**: the house catalogs deliberately carry no audio, no SIMD, and no
OS-scheduler elements. Chapter 17 therefore keeps two honest registers: the *editorial* register
(compositions this booklet makes from cataloged parts) and the *external* register (domain
sources outside the corpus, named in plain text, never dressed as corpus identifiers). Facts
verified on the reference machine during compilation are marked **measured**, with the date; the
rest of the domain layer says plainly what it is.

## How to read it

Part I establishes the machine, the deadline, and the twenty invariants. Parts II–III give the
structure (the core as a compiled graph; ports over two operating systems) and the execution
architecture (the two planes, the channel menu, the decision trees). Part IV is memory; Part V is
the mechanical-sympathy core of the commission — microarchitecture, toolchain, and the operating
system itself as an optimization surface. Part VI is failure and evidence; Part VII is proof and
constitution: tests, enforcement, the compliance contract with the parent, and the lineage. A
reader with one hour reads chapter 2, the invariants, and chapter 16. A reader building a system
reads it whole, once, and then argues with it — the parent's standing instruction, inherited:
this is grounding, not a rulebook; cite it when it shapes a decision, reason past it when the
situation genuinely differs, and say which you are doing.

---
# Part I — The Ground, Again

## 1. The machine you are actually programming

### 1.1 What "unconstrained" buys, and how it lies

Call the target what it is: a personal computer. Eight or more cores, gigahertz clocks, tens of
megabytes of cache, gigabytes of RAM, an MMU always on duty, storage measured in terabytes. Against
a microcontroller this is not a bigger budget; it is the *end* of most classic embedded budgets.
RAM ceases to be scarce. Flash endurance is someone else's problem. Cycles per buffer number in the
millions. A designer arriving from the parent booklet's world should feel the temptation
immediately: with this much machine, why would any discipline be needed at all?

Because everything that makes this machine fast is a bet, and the bets are settled per run, not
per design. The cache hierarchy makes a load cost four cycles *usually* — and three hundred when
the line is cold. The branch predictor makes a conditional free *usually* — and a fifteen-cycle
pipeline flush when it guesses wrong. Out-of-order execution hides latency *usually* — behind a
window that stalls the moment a dependency chain grows longer than the hardware can see past.
Frequency scaling delivers the marketing clock *usually* — and a fraction of it in the
milliseconds after a wake from idle, or under thermal pressure, or on the small cores of a hybrid
part. The operating system schedules your thread promptly *usually*. Every one of those
mechanisms was engineered to raise **throughput** — the average over billions of operations — and
every one of them raises the average precisely by borrowing from the worst case.

Real-time audio is a worst-case discipline. The device consumes samples at an exact, physical
rate; the program's obligation recurs every few milliseconds, forever; and a single miss is
audible. Nobody hears your average. **The unconstrained machine is therefore not an easier
target than the microcontroller — it is a different one**: the parent's scarcity of bytes and
cycles is replaced by a scarcity of *determinism*, and the whole of this booklet is the
discipline of buying determinism back — architecturally (Parts II–III), from the memory system
(Part IV), from the microarchitecture and the toolchain (Part V), and from the operating system
itself (ch. 11) — while spending the abundance freely everywhere the deadline cannot see.

That last clause deserves its own sentence, because it is the license the parent could never
grant: **off the real-time path, this booklet's programs are ordinary desktop software.** They
may allocate, block, log, parse, and call libraries like anyone else — the discipline
concentrates entirely on the small set of threads the device clock paces, and on the boundary
around them (ch. 2 draws it; ch. 6 polices it). Spending the machine's abundance *there*, to keep
the real-time plane austere, is the design.

### 1.2 The reference class

The parent forbids itself hardware facts; a child exists to pin them. This booklet pins a
**hardware class**, not a part number — the class is what survives shopping decisions — and keeps
one live exemplar as the *reference machine* on which every **measured** claim in this booklet
was verified (ch. 16 dates them).

| property | class floor (pinned) | reference machine (measured 2026-08-12) |
|---|---|---|
| ISA | x86-64 at the `x86-64-v3` level: AVX2, FMA, BMI2 | 12th-gen Intel Core i9-12900K |
| cores | ≥ 8 hardware threads; hybrid topologies expected | 8 P-cores (2-way SMT) + 8 E-cores = 24 threads |
| L1d | ≥ 32 KiB per core, 64-byte lines | 48 KiB per P-core, 32 KiB per E-core |
| L2 | ≥ 512 KiB per core or cluster | 1.25 MiB per P-core; 2 MiB per 4-E-core cluster |
| last-level cache | ≥ 8 MiB shared | 30 MiB shared L3 |
| RAM | ≥ 16 GiB, virtual memory always on, 4 KiB pages | 32 GiB |
| timekeeping | constant/invariant TSC; OS monotonic clock | present |
| clocking | dynamic frequency and idle states, always assumed | turbo + deep C-states, hybrid asymmetry |

Three consequences of the class are load-bearing enough to state here and use everywhere.

**The topology is asymmetric.** Hybrid parts — performance cores and efficiency cores in one
socket — are the class norm now, not an exotic. A real-time thread scheduled onto an efficiency
core silently loses a large fraction of its budget; a bench result taken on one core class does
not transfer to the other. Core *placement* is therefore a first-class architectural concern
(§11.2), not a deployment detail, and every latency figure carries the core class it was measured
on.

**The memory hierarchy is the cost model.** Four cycles to L1, roughly a dozen to L2, tens to the
shared cache, hundreds to DRAM — the exact numbers are hub facts, the *ratios* are the class. A
working set that fits in the per-core caches is the difference between a kernel that meets its
budget and one that gambles; chapter 8 budgets working sets against this table, and chapter 9
spends it line by line.

**Correctness is pinned one level above the silicon.** The class pins x86-64, whose hardware
memory ordering is famously strong — and §6.6 forbids leaning on it anyway. Concurrent code is
written against the C11 memory model, with the ordering each operation needs stated in the code;
the strong hardware then makes the stated orderings cheap, instead of making unstated ones
accidentally correct. The pin buys performance floors (vector width, FMA, cache-line size for
padding); it is never the correctness argument. A future port to a weakly-ordered class (ARM64 is
the obvious candidate, and chapter 16 leaves it OPEN) should find its work already done in the
code and confined to re-measurement.

### 1.3 The operating system is a peer, not a servant

The second half of the machine is software you did not write and cannot schedule around by
inspection: a general-purpose kernel — Linux or Windows NT — plus its driver population. The
parent's targets ran your program and nothing else; here **your program is a tenant**, and the
landlord's incentives are throughput, fairness, and battery life, none of which is your deadline.

What the kernel gives, on both sides of the portability line:

- **preemptive multitasking** whose default scheduling classes are *fair* rather than *urgent*
  (CFS-lineage scheduling on Linux, the NT dispatcher's priority-plus-boost regime on Windows);
- **demand-paged virtual memory** in which any byte you have not touched recently is a candidate
  for a millisecond-class stall;
- **timers** whose default granularity is coarser than an audio period;
- **elevated scheduling classes** — SCHED_FIFO/SCHED_RR on Linux, the NT real-time priority band
  and the multimedia class scheduler (MMCSS) on Windows — that are *requests*: granted or refused
  per machine policy, revocable, and in Linux's case throttled by default so that a runaway
  real-time thread cannot brick the box.

Chapter 11 works through all of it; what belongs in the ground chapter is the posture:

- **Nothing the kernel promises is a bound.** Priorities shorten the tail; they do not cut it
  off. A page fault, a driver's interrupt storm, a firmware System Management Interrupt — each
  can and eventually will land inside your period. The design assumes *rare, bounded-damage*
  misses (ch. 2, ch. 12), never zero.
- **The kernel's mechanisms are ports, not ambient facts.** Thread creation, priority elevation,
  memory locking, clocks, and the audio devices themselves all arrive through adapter code
  (ch. 5), because they differ per kernel — and because the test suite needs to stand where the
  kernel was.
- **The kernel is also the instrument.** The same OS that jitters your wakeups will, asked
  properly, tell you exactly what happened — page-fault counts, context-switch counts, scheduler
  traces (ETW on NT, perf/ftrace on Linux). Chapter 11's autopsy discipline and chapter 13's
  evidence chain lean on this: on this platform, unlike the parent's, the observer's tooling is
  rich — what remains scarce is the *right to use it on the real-time path*.

One more tenant shares the machine and deserves early naming: **other software**. A browser, a
compile job, an antivirus scan — the design cannot assume a quiet machine, and the headroom
invariant (invariant 6) plus the degrade ladder (ch. 12) are sized for a noisy one. Deployment
hardening for dedicated machines (CPU isolation, kernel preemption builds) exists and is real —
§11.6 prices it — but it is a *deployment* rung, never a design assumption.

### 1.4 The audio path, on both kernels

The program's prime effect flows through a stack the OS owns. The shapes differ per kernel; the
contract this booklet extracts from them does not.

**On Linux**, the kernel-side boundary is ALSA: per-device ring buffers the driver and the
hardware share, divided into *periods*; the application (or a sound server standing in for it —
PulseAudio, JACK, PipeWire are user-space tenants above ALSA, and PipeWire increasingly fronts
the other two) maps or writes frames and receives period-boundary wakeups. **On Windows NT**, the
boundary is WASAPI atop the audio engine: in *shared* mode the engine mixes all clients at an
engine-owned period and format; in *exclusive* mode the application deals with the device
directly at a device-native format and the engine steps aside. Vendor-SDK paths (ASIO) exist
outside the OS stack entirely; this booklet excludes them from the shipped set and chapter 16
records the exclusion and its licensing reason, with the port left open for a grandchild.

Beneath both stacks sits the same physics, and it is the fact the whole booklet orbits: **the
device consumes frames on its own crystal.** The DAC's clock — not the OS scheduler, not your
thread — decides when the next sample is needed. The parent's ch. 7 called hardware-paced
concurrency "the concurrency no design can decline," and its second-master discipline transposes
here whole: the audio device is a master issuing a hard-deadline demand every period, and the OS
merely relays it (an interrupt, a handle signal, a poll readiness) with jitter added in transit.

Extracted contract, common to both kernels and pinned as the device port's shape (§5.2): the
adapter owns a **device-paced loop** — block on the device's own signal; wake; learn how many
frames the device wants; hand the core exactly that much work; submit; block again. Everything
kernel-specific — how the signal arrives, how buffers are acquired, how the stream is recovered
after a fault — lives inside the adapter, behind a port whose vocabulary is frames, periods, and
sample formats, never handles and events.

One mapping from the parent must be made explicit, because it is the largest single difference in
the transposition. On the microcontroller, the parent's rule was **"ISRs are couriers, not
workers"** (parent invariant 9): capture, timestamp, enqueue, return — decisions happen in task
context. On this platform the hardware interrupt is the kernel's property; what the program gets
is a *thread* the kernel wakes per period — already "task context," already schedulable. The
courier rule therefore lands one level up, with its spirit intact and its letter adapted: **the
device-paced thread does the signal work, the whole signal work, and nothing but the signal
work.** It is simultaneously the parent's ISR (paced by hardware, highest effective urgency,
forbidden to block) and the parent's highest-priority task (it runs the actual computation). What
it couriers *away* is everything else: control, telemetry, persistence, UI — across the wait-free
channels of chapter 6, exactly as the parent's ISR enqueues toward its task plane.

### 1.5 Still an embedded program

The parent opened with four consequences of its definition; each survives the change of machine,
and their survival is why this booklet is a child rather than a cousin.

**Effects cannot be avoided, so they must be placed.** The product is the effect. The decision
half (what the next buffer should contain — the DSP) is separated from the mechanism half (device
negotiation, thread pacing, submission) exactly as the parent's ch. 4 demands; chapter 4 here
gives the domain form: a functional core over sample blocks, compiled into a schedule the
real-time shell executes.

**The program is only partially observable.** Not because a terminal is missing — because the
real-time plane cannot afford one. A `printf` in the device-paced thread is a lock, an
allocation, and a syscall wearing a debugging aid's clothes (ch. 6 forbids all three). Whatever
visibility the real-time plane has is visibility *designed in* — the wait-free event ring, the
duration histograms, the counters of chapter 13 — the parent's flight-recorder principle,
translated to a machine with disk space.

**The program outlives its surroundings.** Kernels version, audio subsystems are replaced
(PipeWire's rise is recent history), toolchains roll, silicon generations shift the cost model
under a fixed ISA. The port discipline of chapter 5 plus the class pin of §1.2 are what let the
program cross those transitions as a recompile-and-remeasure, not a rewrite.

**Failure is a normal operating mode.** Devices disappear mid-stream (a USB interface unplugged,
a default device switched by the user), formats change under renegotiation, the OS declines an
elevation request, a neighbor process eats the machine. Chapter 12 gives every one of those a
designed path, and the terminal rung everywhere is the domain's safe state: **fade to silence,
keep the device healthy, keep the evidence.**

## 2. The prime contract

### 2.1 The arithmetic of the deadline

Everything in this domain reduces to one recurring transaction. The device drains a buffer of
*N* frames at sample rate *f*; every *N/f* seconds it needs the next one; the program's real-time
plane must produce those *N* frames — every channel, every time — before the drain completes.
That quotient is **the period**, and it is the only deadline this booklet has:

| frames @ 48 kHz | period | the shape of life there |
|---|---|---|
| 32 | 0.67 ms | competitive-grade monitoring; every microsecond audited, OS jitter a peer of the work itself |
| 64 | 1.33 ms | low-latency tracking and virtual instruments; tight but routinely achievable with this booklet's full discipline |
| 128 | 2.67 ms | the workhorse: live effects, instruments, interactive mixing |
| 256 | 5.33 ms | comfortable interactive use; the discipline still applies, the margins stop being heroic |
| 512–1024 | 10.7–21.3 ms | playback, mixdown, streaming; robustness dominates latency |

(At 44.1 kHz the periods stretch ~9%; at 96 kHz they halve — same table, same reasoning, scaled.)

Two derived quantities matter more than the period itself. The **budget** is the fraction of the
period the signal work may consume; the remainder is the reserve that absorbs what the OS and the
hardware add — wakeup latency, frequency-ramp lag, cache refill after preemption, the odd page
that wasn't as locked as believed. Invariant 6 pins the shipped floor: worst observed callback
cost at or below half the period on the reference class, and chapter 14's soak rig is what makes
the number evidence instead of hope. The **latency** the user experiences is a *sum* the period
only contributes to — device ring depth in and out, resampler and mixing stages, the stack's own
plumbing — and §7.3 does that accounting; conflating latency with period is the domain's most
common sizing error, in both directions.

### 2.2 The two regimes

Draw one line through the process: on one side, every thread the device clock paces — the
**real-time plane**; on the other, everything else — the **control plane**. This line is the
single most load-bearing cut in the booklet. The parent's central boundary was effects-from-logic;
that boundary survives intact *inside* each plane (the core stays pure, ch. 4) — but the plane
boundary is the one this domain adds, and every chapter after this one is, at bottom, doing one
of two jobs: **keeping the real-time plane bounded, or moving data across the line without
poisoning it.**

On the real-time plane the regime is austere, and invariant 1 states it as law: no lock, no
allocation, no blocking system call, no I/O, no unbounded loop — bounded work, wait-free
communication, pre-claimed memory, nothing else. Not because locks are slow — because on a
general-purpose kernel a lock's worst case is *unbounded in your terms*: the holder can be
preempted, paged, or throttled, and no priority-inheritance story on either kernel makes that
bound tight enough to put inside a millisecond deadline (§6.2 does the full argument). The control
plane, by deliberate contrast, is ordinary software — it blocks, allocates, parses, logs, talks to
the UI and the disk and the network — and the asymmetry is the design: austerity is affordable
precisely because it is confined.

Membership in each plane is *declared, named, and enforced* — the RT thread inventory is a
composition-root fact (§4.5), the guard machinery of ch. 15 polices the austerity in development
builds, and a thread's plane is part of its name and its documentation. A thread whose plane
nobody stated is a real-time defect that hasn't happened yet.

### 2.3 Quasi-real-time, defined honestly

The commission asks for "quasi-real-time behavior on non-real-time operating systems," and this
section defines the term so every later claim can be audited against it.

**What is off the table.** A hard guarantee — *no deadline is ever missed, by construction* —
requires bounding every stage from interrupt to instruction: WCET-analyzable code on a core
without statistical acceleration, under a scheduler with admission control, over drivers with
serviced-latency contracts. A stock Linux or NT kernel on PC-class hardware offers none of those
bounds, and firmware (System Management Interrupts arriving below the kernel's own feet) denies
the last one to everyone. Any claim of hard real-time on this platform is marketing.

**What is achievable — and is this booklet's actual product** — is a system whose misses are
*engineered to be rare and bounded in damage*:

- **Eliminate every unbounded operation from the real-time plane** (invariants 1, 2, 3): what
  cannot block cannot be blocked. This is structure, not tuning, and it is the bulk of the win.
- **Buy down the scheduler's contribution**: elevated class, locked memory, placement on
  performance cores, C-state and frequency floors — chapter 11's inventory, each item verified at
  go-live (invariant 14).
- **Buy down the work's own variance**: the mechanical sympathy of Part V — working sets inside
  the cache budget, branches predictable, dependency chains short, denormals flushed — so the
  compute cost is a tight distribution, not a long-tailed one.
- **Hold headroom against what remains** (invariant 6): the reserve is the design's admission
  that the tail is not zero.
- **Measure forever** (invariant 5): every callback, histogrammed, in production, always — with
  the xrun counters as the product's own scoreboard. A quasi-real-time claim without a live
  histogram behind it is a wish.
- **Design the miss** (ch. 12): when the budget is blown anyway, a designed ladder degrades
  gracefully toward silence, the event is counted and attributed, and the stream recovers.

Call the result what it is: **statistical real-time with designed failure** — service-level
objectives (misses per day at a stated period, on stated hardware) rather than proofs. The number
is a *product* decision: a live-performance rig, a studio DAW, and a casual player draw the line
in different places, and chapter 16 makes the target SLO one of the facts a deployment pins. What
this booklet guarantees is not the SLO itself but the machinery that makes an SLO honest:
elimination, mitigation, headroom, evidence, and a designed miss.

### 2.4 The xrun taxonomy

The domain's word for the failed transaction is the **xrun** (underrun on output — the device
reached for frames that were not there; overrun on input — samples arrived and nowhere to put
them). One name, four distinguishable causes, and the distinction is the first thing the autopsy
machinery (§11.5, §13.4) is built to make:

1. **Self-overrun** — the signal work itself exceeded the budget: a pathological parameter
   combination, a denormal storm, a working set that outgrew the cache. The program's own fault;
   the degrade ladder's home case.
2. **Late wakeup** — the work was cheap but started late: scheduler latency, a C-state exit, a
   frequency ramp, priority not actually granted. The OS's contribution; chapter 11's territory.
3. **External stall** — the work was interrupted mid-flight: page fault, interrupt storm, SMI,
   another tenant on the core. Partially mitigable (locking, placement), partially the platform's
   irreducible noise.
4. **Device-side fault** — the stream itself broke: device unplugged, format change forced,
   server restarted underneath the adapter. Not a timing failure at all; a designed event with a
   recovery path (invariant 19).

Every xrun is counted, classified as far as the platform allows, and stamped into the flight
ring with the callback's own measurements around it. An xrun with no witness is the domain's
version of the parent's silent dropped sample: a lie the system tells its own recorder.

### 2.5 DT-1 — choosing the period

The first decision tree, because every budget downstream inherits from it. Sizing runs on three
questions:

- **Is the path interactive?** A musician hears themselves through the program (tracking,
  virtual instruments, live effects) → round-trip latency budget 3–12 ms → period 32–128 frames;
  proceed with the full austerity of this booklet and expect to spend Part V. A listener consumes
  output the program paces (playback, mixdown, streaming) → latency is nearly free → period 512+
  frames; the architecture still applies (the austerity is cheap once built), the heroics do not.
- **What does the rest of the chain already cost?** The period is one term in the end-to-end sum
  (§7.3). If converters, wireless links, or a shared-mode engine already spend 15 ms, shrinking
  the period from 128 to 64 buys 1.3 ms of a 15 ms problem — measure the chain before spending
  the margin where it is most expensive to hold.
- **What machine population ships?** The reference class floor (§1.2) is what invariant 6's
  headroom is proven on. A product shipping to unknown consumer machines holds double the
  headroom or doubles the period; a product for known hardware (an installation, a rig the vendor
  controls) may run at the class's edge with the soak evidence to show for it.

And one standing output of the tree, whatever it decides: **the period is a product parameter,
not a constant** (invariant 16). It is negotiated with the device at the composition root, it is
user-visible where the product is a tool for audio professionals, its supported range is part of
the test matrix (ch. 14's sweep), and the robustness curve — xruns per hour as a function of
period, on the reference class — is a published, regenerated artifact, because it is the honest
form of the marketing question "how low does it go?"

### 2.6 The economics of the tail

A last framing device before the invariants, because it inverts desktop instinct so thoroughly
that every design review in this domain eventually re-litigates it. Throughput engineering buys
average-case improvements and sells them by the benchmark mean; this domain's accounting is
different: **the mean is nearly worthless, and the maximum is nearly everything.** A kernel that
runs 20% faster on average but stalls for two milliseconds once an hour is not an optimization —
it is a defect with good marketing. Every technique in Part V is therefore judged twice: once for
its average cost, once for its variance — and a change that trades a little mean for a lot of
tail (pre-touching a table, hoisting a branch, splitting a hot lock-free index onto its own cache
line) is *good* here even though a throughput profile calls it a loss.

The same accounting explains this domain's testing shape (ch. 14): correctness suites prove the
output right, but the performance suite's assertions are about *distributions* — percentiles and
maxima over long soaks — because that is where the product lives. And it explains the
observability shape (ch. 13): the histogram, not the log line, is the primary instrument, because
the question that matters — "how bad is the worst, how often" — is a question only a distribution
answers.

## 3. The invariants

Twenty statements that hold for every program this booklet governs, each carrying its enforcement
route inline, each developed in a chapter. They stand **in addition to the parent's twenty-five**,
which this booklet inherits wholesale and re-states only where the domain tightens them; a reader
should hold the parent's list and this one as a single constitution. The routes are the parent's
seven, unchanged: `compiler-catchable`, `analysis-catchable`, `build-catchable`,
`host-test-catchable`, `target-test-catchable`, `runtime-catchable`, `contract-only` — with
"target" meaning, on this platform, a real machine of the reference class with a real audio
device and the real kernel (§14.6).

**The real-time plane** *(chapters 2, 6)*

1. **The real-time thread does bounded work and nothing else.** No lock, no allocation, no
   blocking system call, no file or console I/O, no unbounded loop — from the device wakeup to
   the submission, every operation completes in bounded time by construction. *(analysis +
   runtime-catchable — poisoned symbols and development-build guards, §15.2; the boundedness of
   loops: contract-only, reviewed)*
2. **Every channel that crosses the plane boundary is wait-free on the real-time side, bounded,
   and declares its overflow policy — with drops counted, never silent.** [tightens parent
   invariant 10: "lock-free" is not enough; the RT side never waits on the peer at all]
   *(host-test-catchable contract suites + runtime counters)*
3. **All memory the real-time plane can touch is allocated, locked, and faulted in before the
   stream goes live — and none is allocated after.** [tightens parent invariant 11 for a paged
   platform: claimed-at-init is not enough; it must be resident] *(runtime-catchable — go-live
   asserts verify lock and residency; development guards trap the violation)*
4. **Every real-time thread runs with denormals flushed (FTZ/DAZ), and a denormal or NaN
   emitted by the core in nominal operation is a defect, not a curiosity.** *(runtime-catchable
   development scans + host-test-catchable properties, §9.6, §14.3)*

**Evidence** *(chapters 11, 13)*

5. **The deadline monitor is always on:** every callback's cost lands in a histogram, every xrun
   in a classified counter — in production, at negligible cost, as product features.
   *(runtime-catchable)*
6. **Shipped configurations demonstrate a headroom floor on the reference class:** worst observed
   callback cost ≤ 50% of period, evidenced by soak runs, re-proven per release.
   *(target-test-catchable)*
7. **Overload runs a designed degrade ladder whose terminal rung is fade-to-silence with the
   device kept healthy** — overload never blocks, never corrupts, never rides silently.
   *(host-test-catchable fault injection + runtime counters, ch. 12)*

**One codebase, one toolchain** *(chapters 5, 10)*

8. **The core is OS-free: no operating-system header on its include path, no OS symbol among its
   imports.** [parent invariants 4 and 7, instantiated for the OS-as-target] *(build-catchable —
   include audit + link-time symbol audit, §15.3)*
9. **One codebase: kernel-specific text lives only in adapters, and every commit builds and
   tests both legs — Linux and Windows — from the same sources.** *(build-catchable — the CI
   matrix is the proof)*
10. **One toolchain family: clang/LLVM on both legs, one warning canon promoted to errors, flag
    parity across legs except the documented per-OS rows.** *(build-catchable)*
11. **The floating-point regime is pinned per translation-unit class:** core kernels build with
    contraction pinned and value-changing fast-math off, and determinism-relevant paths call no
    system math library. *(build-catchable flags + host-test-catchable exact golden masters on
    both legs, §9.6)*
12. **Every SIMD kernel has a scalar twin; their equivalence is tested at a pinned tolerance;
    and kernel dispatch binds once, at initialization.** [parent invariant 5's binding-time
    discipline, instantiated] *(host-test-catchable, §9.7)*
13. **Nothing on the real-time plane formats, logs, or prints.** Real-time evidence is
    structured events in the wait-free ring, drained and rendered elsewhere. [tightens parent
    invariant 19] *(analysis + runtime-catchable guards)*

**The operating system** *(chapter 11)*

14. **Elevation is verified, and its denial is a mode.** Scheduling class, memory locking, and
    core placement are requested at go-live, verified to have been granted, and a refusal is a
    reported, user-visible degraded mode — never a silent hope. *(runtime-catchable)*

**Performance as a contract** *(chapters 9, 10, 14)*

15. **Performance claims carry measurements from the pinned bench protocol, and hot-kernel
    vectorization is asserted by compiler remarks in CI** — an optimization nobody measured is
    folklore; one the compiler quietly stopped performing is a regression nobody filed.
    *(build-catchable remark gates + host/target-test-catchable benches, §10.6, §14.5)*
16. **The latency dial is a product parameter with a tested robustness curve** — the supported
    period range is swept in CI, and the xrun-vs-period curve on the reference class is a
    published artifact. *(host-test-catchable sweep + target-test-catchable soak)*

**Identity and evidence at rest** *(chapters 13, 14)*

17. **Every artifact embeds its build identity** — source revision, toolchain and flag
    fingerprint, kernel schema hash — and every session report and crash record carries it.
    [parent invariant 18's identity clause, industrialized] *(build + runtime-catchable)*
18. **Crash and exit preserve the flight ring, and an overrun autopsy can distinguish
    self-overrun from late wakeup from external stall in diagnosis mode.** *(runtime-catchable,
    §11.5, §13.4)*
19. **Device loss, format change, and elevation denial are designed events with tested recovery
    paths** — not exceptional conditions discovered in the field. *(host-test-catchable per-port
    fault suites, §14.4)*
20. **The core's output is invariant to callback-size partitioning** within its declared block
    quantum: processing a span as one call or as any legal sequence of smaller calls yields
    identical output. The property that makes period a free variable — and the regression net
    that catches hidden per-callback state. *(host-test-catchable property, §14.3)*

**Tightened, inherited, and the meta-invariant.** Where this chapter tightens the parent, it says
so inline above (invariants 2, 3, 13); everywhere else the parent's twenty-five apply unchanged —
the include-graph law, the effect boundary, the ownership language, error dispositions, the
composition-root discipline, the two-kinds-of-wrong split. A child may tighten and must not
weaken; chapter 16 walks the compliance row by row. And over all of it, the parent's
meta-invariant, inherited verbatim: **a rule with no enforcer is a preference** — route it, or
register it `contract-only` and review for it by name (§15.5).

---
# Part II — Structure

## 4. The core is a compiled graph

### 4.1 The functional core, in this domain

The parent's central boundary — decision code computes what should happen and returns it as data;
shell code makes it happen (`functional-core-imperative-shell`) — lands in this domain with
unusual grace, because the domain's decision code already *wants* to be a pure function. A signal
processor is a transform: previous state, parameters, and an input block in; next state and an
output block out. Written that way — and only that way — the core needs no operating system, no
clock, no allocation, and no device to run: the whole DSP engine builds and executes on any
machine, at any speed, under any test harness, which is the property every later chapter spends
(offline rendering in ch. 14, deterministic replay in §13.3, dual-OS portability in ch. 5).

The architectural genre is cataloged: the core is a `dataflow-architecture` — computation driven
by data availability along explicit arcs — in its `streaming-dataflow-architecture` form, a
long-running graph over an unbounded stream; `pipes-and-filters` is its simplest degenerate
shape. This booklet's rules for the core, stated once:

- **The core's only time is the sample count.** No wall clock, no OS ticks — position in the
  stream is the clock (parent invariant 8, trivially honored: time arrives as the block's
  starting sample index and length). Anything periodic in the core — an LFO, an envelope, a
  meter window — is derived from sample arithmetic.
- **The core's only memory is what it was handed.** State blocks, scratch arenas, lookup tables —
  all allocated by the composition root (§4.5), owned per the parent's ownership vocabulary,
  sized before go-live (invariant 3). The core never calls an allocator, which is why it can run
  on the real-time plane at all.
- **The core is deterministic under the pinned regime.** Same state, same parameters, same input
  block, same kernel selection → bit-identical output, on both legs (invariant 11; §9.6 states
  the conditions). Randomness, where the DSP wants it (dither, noise generators), flows from a
  seeded `pseudorandom-number-generator` owned by the state — never from entropy the shell did
  not inject.
- **The core is OS-free by construction and by audit** (invariant 8): its translation units
  include core and port headers only, and its compiled objects import no OS symbol — a property
  the build checks, not a hope (§15.3).

### 4.2 Decisions as data, twice

The parent's `defunctionalization` move — behavior turned into inspectable data — appears here
twice, at two altitudes, and naming both is what keeps the concurrency chapter sane.

**The edit model** is the control plane's graph: nodes, connections, parameter values, the thing
the user edits and the session file persists. It is ordinary mutable software, owned by the
control plane, with no real-time obligations at all.

**The execution schedule** is what the real-time plane actually runs, and it is *compiled*, not
interpreted from the edit model: whenever the graph changes, a **graph compiler** — control-plane
code, free to allocate and take its time — flattens the current edit model into a fixed program:

```c
/* the execution schedule: what the RT plane runs — data, not code */
typedef struct {
    op_code_t     op;        /* which kernel: an enum, dispatch-table index */
    uint16_t      state_off; /* this op's state block, offset into the state arena */
    uint16_t      param_off; /* this op's parameter block */
    uint8_t       in[MAX_IN], out[MAX_OUT]; /* buffer-pool slot indices */
} sched_op_t;

typedef struct {
    uint32_t      n_ops;
    sched_op_t    ops[];     /* topologically ordered; executed 0..n_ops-1, every block */
} schedule_t;
```

The real-time loop over this structure is ten lines: for each op, look up the kernel, hand it its
state, parameters, and buffer slots, run it. This is the corpus's `bytecode-virtual-machine`
shape — compile to a compact linear encoding, then execute — with the audio graph as the source
language; `threaded-code` and `function-pointer-dispatch-table` are the dispatch spellings, and
§9.4 weighs them against the enum-plus-switch spelling on branch-prediction grounds. What the
compilation buys, each item load-bearing:

- **Topology decided off the plane.** Ordering, fan-out, feedback detection, latency compensation
  — all resolved where blocking and allocation are legal. The RT plane never walks a mutable
  graph; it executes a frozen program, and swapping programs is one pointer publication (§6.4).
- **Buffer assignment as register allocation.** The compiler assigns op inputs and outputs to
  slots in a small scratch-buffer pool by liveness analysis — the same move a code generator
  makes — minimizing the working set the cache must hold (§8.4). A naive graph walk keeps every
  edge's buffer alive; a compiled schedule reuses a handful.
- **Precomputation lands at edit time.** Filter coefficients, wavetables, gain curves — every
  `lookup-table` derivable from parameters is computed by the compiler or the parameter system,
  never inside a kernel (§9.3's division discipline depends on this).
- **The schedule is evidence.** It can be printed, diffed, hashed (its hash is part of the build
  and session identity, invariant 17), replayed, and unit-tested — the parent's promise that
  defunctionalized decisions are loggable and comparable, kept at graph scale.
- **Specialization happens at compile time, not per sample.** Where a node has modes (bypass,
  mono/stereo, quality tiers), the graph compiler emits the specialized op variant, hoisting the
  mode branch out of the per-sample loop entirely (§9.4's first branch rule).

### 4.3 Parameters are a dataflow, not calls

Nothing may call across the plane boundary, so "set the filter cutoff" cannot be a function call
into the DSP. Parameters are a **dataflow**: the control plane writes *targets* (through the
channels of §6.3 — an atomic scalar per independent parameter, a small command ring for grouped
or ordered changes); the real-time plane *consumes* targets at block boundaries and interpolates
toward them across the block — because a parameter that jumps at a block edge is audible as the
zipper artifact this domain names, and smoothing is therefore part of the parameter's contract
(ramp shape and duration), not a nicety. Sample-accurate events — note-on at frame 37 — travel
as timestamped events in the command ring, and the block loop splits at event boundaries (§4.4).

Two disciplines keep this honest. **Every parameter states its update semantics** — smoothed
(with ramp), stepped-at-block, or sample-accurate-event — in the port contract; unstated
smoothing is how two implementations of one plugin disagree audibly. And **parameters never
carry pointers** — they are values; anything structural (a new impulse response, a new wavetable)
is a *resource swap* through the snapshot machinery of §6.4, because a pointer smuggled through a
parameter channel is an ownership transfer nobody contracted (parent invariant 12).

### 4.4 The block quantum

The device dictates the period; the core should not have to care. This booklet's default is a
**fixed internal block quantum**: the core processes in blocks of its own declared size (a small
power of two — commonly 16 to 64 frames), and the shell's callback assembles device periods from
core blocks. The quantum decouples three pressures that would otherwise fight: the *device's*
period (a negotiation outcome, possibly odd-sized, possibly changing per callback on some paths),
the *parameter system's* update rate (one target-consume-and-ramp per quantum), and the
*microarchitecture's* appetite (a quantum sized so the working set of one op over one block sits
in L1/L2 — §8.4, §9.2 — and so per-op dispatch overhead amortizes across enough samples, which
is the same economics the corpus's `vectorized-execution` records for batch-at-a-time query
engines).

The costs, named: up to one quantum of added latency where the period is not a multiple of the
quantum (account it in §7.3's budget), and a rule the tests enforce rather than the prose:
**invariant 20** — output is invariant to how a span is partitioned into callbacks, given the
quantum contract. That property is what makes the period a free product variable (invariant 16),
and it is the regression net that catches the classic defect family of hidden per-callback state
(a filter that resets per callback, a ramp that restarts, a meter that decays per call rather
than per sample).

### 4.5 The composition root

The parent's §4.6 transposes with its order rewritten for this platform's hazards. Between
process start and the first device callback there is exactly one sanctioned sequence, in one
file, and it is architecture:

1. **Read and validate configuration** (control plane; fail-fast on nonsense — parent §10.4).
2. **Enumerate and negotiate the device** through the audio port: sample rate, channel count,
   sample format, period size — the outcome is *the* platform contract for this run, and every
   downstream size derives from it.
3. **Compile the graph** against the negotiated format (§4.2).
4. **Allocate everything** the real-time plane will ever touch: state arena, parameter blocks,
   buffer pool, channel storage, the flight ring, RT thread stacks — sized from the schedule and
   the negotiated period, by the allocation classes of §8.3.
5. **Lock and prefault**: lock the address space (residency port), touch every page just
   allocated, prefault the RT thread stacks to their sized depth (§8.2). From here on,
   invariant 3 holds or go-live fails.
6. **Spawn the real-time threads** through the thread port; each requests elevation, placement,
   and FTZ/DAZ, and reports what it got (invariant 14). Denials are decided *here* — proceed
   degraded with the user told, or refuse to start — per the product's recorded policy.
7. **Warm up**: run the schedule once or twice against silence into a discard buffer — faulting
   in every code page and table the hot path will touch, settling frequency, verifying no
   denormal/NaN emerges from the initial state (invariant 4's first checkpoint).
8. **Arm the monitor** (deadline histogram, xrun counters, heartbeat — ch. 13), then open the
   gate: a `latch` releases the device loop, and the stream is live.

Teardown mirrors the root in reverse under `two-phase-termination`: signal intent, let the
real-time plane fade to silence (ch. 12's terminal rung used as the *orderly* exit too), stop the
device loop, join threads, then and only then free. Two parent rules carry over verbatim: **no
effects before their owner exists** — nothing touches the device or spawns threads from module
init; and **only the root knows the whole inventory** — everything else receives its
collaborators through ports (`dependency-injection`, spelled in C as the parent spells it), and
ambient lookup (`service-locator` and friends) stays forbidden. The root's order is host-tested
(the fake device makes it cheap), and go-live time is a budget (§15.4). *(runtime-catchable
go-live asserts; host-test-catchable order)*

### 4.6 What the boundary is not

The parent's honesty clause, restated for this domain's temptations. The boundary is not a
promise that the core is the majority of the code — a shipping audio product's bulk is control
plane: UI, session management, file I/O, device juggling. The boundary's claim is that the part
whose defects are *audible* — the DSP, the scheduling of it, the parameter semantics — is the
cheap-to-test part. It is not a license for a "thin" core that queries the OS "just once" — the
first `gettimeofday` in a kernel is the determinism leak the parent already named, and the
include/symbol audits exist because *just once* never stays once. And it is not the claim that
the graph must be static forever — §6.4 gives live rewiring its safe mechanism; what is refused
is the RT plane *discovering* structure at runtime rather than *receiving* it compiled.

## 5. Ports, and the two operating systems

### 5.1 The port list

The parent demands the effect inventory be written down as the port list in embryo; here it is
for this domain — the core and shell's entire view of the outside world, each port owned by this
codebase, named in its vocabulary (`hexagonal-architecture`, with `wrapper-facade` as the
adapter idiom over raw OS APIs):

| port | carries | plane | blocking contract |
|---|---|---|---|
| **audio device** | the stream: negotiated format, the device-paced loop, frames in/out, stream faults | RT | the *one* sanctioned block: waiting on the device's own pacing signal |
| **thread** | creation with plane, stack size, priority/placement *requests*, and the grant report | control creates; RT runs | create/join block; nothing else does |
| **clock** | monotonic now; paired (device-position, monotonic) timestamps for §7.2's drift math | both | never blocks |
| **residency** | address-space locking, prefault, working-set floor | root only | blocks at root, never after |
| **telemetry sink** | drained flight-ring events, histograms, session reports outbound | control | blocks off-plane only |
| **storage/stream** | sample/session I/O, staged through the streaming worker | control/worker | blocks off-plane only |
| **control surface** | the product's own control protocol (UI, remote, automation) | control | blocks off-plane only |

Ports the parent lists that this domain *retires*: no nonvolatile-endurance port (disks and SSDs
are the OS's problem; session persistence is ordinary file I/O on the control plane), no
power/reset port (the OS owns power; §11.4's power *requests* ride the residency and thread
adapters), no interrupt port (the kernel keeps the vectors; §1.4's mapping stands). The test
suite remains what the parent says it is: the other adapter set for every port on this list.

### 5.2 The audio-device port

The prime port, and the only place the two operating systems are allowed to look different. Its
contract, in the core-owned vocabulary the parent requires (frames, channels, sample formats —
never handles, events, or engine names):

- **Negotiation** (root only): request rate/format/channels/period; receive the grant — which
  may differ; the grant is final for the stream's life. Format conversion, if the product accepts
  a non-native grant, is an adapter concern at the boundary, never a kernel concern (§9.1 pins
  the core's internal format: 32-bit float, deinterleaved planes).
- **The paced loop** (RT): the adapter owns the real-time thread and the loop — *block on the
  device signal; wake; obtain the period's buffers; call the shell's render entry with exactly
  the frames demanded and the pair of timestamps (§7.2); submit; repeat*. The render entry is the
  plane's single doorway, and the deadline monitor wraps it (invariant 5).
- **Fault verbs** (invariant 19): the stream can report *underrun-recovered* (counted, stream
  continues), *device-lost*, and *format-invalidated* — each an event to the control plane, each
  with a designed recovery (§12.4), none a surprise.

**The ALSA adapter** (Linux) realizes the loop against the kernel's period-ring model: configure
hardware and software parameters to the grant, then block per period — on the device's poll
descriptors or in the blocking write path — and recover the documented error states (the
underrun errno, the suspend state) through the port's fault verbs rather than leaking errno
upward. Direct hardware access (`hw:`-class device selection) is the default for the exclusive
low-latency products; routing through the system mixer or a sound server (PipeWire and friends
present themselves as ALSA devices) is the compatible default for the rest — a *product* choice
the adapter takes as configuration. The memory-mapped transfer variant is an optimization row
(§10.7): same port, one fewer copy, adapter-internal. *(external-register facts: the ALSA
project's API documentation; §17.3)*

**The WASAPI adapter** (Windows) realizes the same loop event-driven: an audio client in
event-callback mode, a waitable event the engine signals per period, exclusive mode for the
low-latency products and shared mode for the compatible default — the engine's own period then
bounds the floor, a fact the negotiation surfaces honestly to the product rather than hiding.
COM is confined *inside* the adapter as an `anti-corruption-layer`: initialized on the threads
the adapter owns, never visible in any port signature, its reference-counting discipline
wrapped so the core never learns Windows has objects. The adapter registers its real-time
thread with the OS's multimedia scheduling service (§11.1) as part of thread start, and
device-invalidation notifications arrive on a control-plane thread, converted to the port's
fault verbs. *(external-register facts: Microsoft's WASAPI/MMCSS documentation; §17.3)*

Excluded from the shipped set, recorded here and in ch. 16: vendor-SDK paths (ASIO's
redistribution licensing disqualifies it from a clean-room open codebase; the port is designed
so a grandchild adds that adapter without touching the core), and native sound-server protocols
(JACK, PipeWire's own API) — legitimate future adapters, same port, left OPEN.

### 5.3 The thread port

Threading cannot be portable C by itself: C11's `<threads.h>` has no vocabulary for priority,
scheduling class, affinity, or stack pre-sizing — every one of which this domain's correctness
budget depends on. So threads are a port like any other, and the two adapters spell the same
contract natively:

- **Creation carries the whole request**: entry point, argument, *plane* (RT or control), stack
  size (pre-sized, guard-paged, prefaulted for RT — §8.2), priority class request, placement
  hint (P-core preference for RT on hybrid parts — §11.2).
- **The grant is reported, not assumed** (invariant 14): the adapter returns what the OS actually
  granted — class, priority, affinity — and the composition root decides policy on any shortfall.
  On Linux that means the scheduling class actually set (the elevation dance of §11.1, including
  the case where a session manager grants it on the thread's behalf); on Windows, the
  characteristics-handle actually obtained from the multimedia class scheduler.
- **RT threads never appear or vanish mid-stream**: the RT thread population is fixed between
  go-live and teardown (worker pools included — §6.5); thread creation after go-live is a
  control-plane-only act. This is the parent's static-allocation instinct applied to threads.

### 5.4 The remaining ports, briefly

The **clock port** returns the OS monotonic clock (never the calendar clock — the parent's
time-quality rules apply verbatim) and stamps the paired readings §7.2's drift estimator
consumes. The **residency port** wraps address-space locking and working-set guarantees —
`mlockall`-style on Linux, locked pages plus a raised working-set floor on Windows — with the
honest per-OS semantics documented in the adapter, because the two kernels' promises differ in
exactly the ways §8.2 has to care about. The **telemetry sink** and **storage/stream** ports are
ordinary control-plane citizens; their only domain rule is *where they may be called from*
(never the RT plane — invariant 13), which the guard machinery enforces rather than the prose.

### 5.5 One codebase: the mechanics

Invariant 9's structure, concretely:

- **Layout**: `core/` (kernels, graph compiler, schedule executor, parameter system — OS-free),
  `ports/` (the headers of §5.1 — owned by the core side, per the parent's separated-interface
  rung), `adapters/alsa/`, `adapters/wasapi/`, `adapters/posix/`, `adapters/win32/` (thread,
  clock, residency adapters), `shell/` (composition root, control plane), `test/`, `tools/`
  (offline renderer, bench harness).
- **Selection at build time**: each leg compiles the same `core/`, `ports/`, `shell/`, `test/`
  sources and *links* the leg's adapter set — the parent's link-time binding rung
  (`facade-backend-module-pattern`; `defer-binding` says bind as early as the rate of change
  allows, and "which kernel is this OS" changes never). No `#ifdef` selects behavior inside
  logic; the conditional-inclusion audit inherited from the parent (§5.3 there) polices the
  residue, which should be a handful of lines in adapter-adjacent glue at most.
- **The parity table**: what may differ per leg is enumerated — the adapter directories, a
  documented per-OS row set in the flag canon (§10.2), and nothing else. CI builds and tests
  both legs from every commit (§14.6); a change that compiles on one leg only is a broken build,
  not a porting task for later.

### 5.6 The compiler port, narrowed

The parent treats the compiler as a target and quarantines everything beyond ISO C behind a
compiler port. The child pins one compiler family (invariant 10) — and *keeps the port anyway*,
narrowed: a single header set owns the attribute and builtin spellings the codebase may use
(alignment, branch-likelihood annotation, prefetch, assumption/unreachable markers, the
vector-kernel attribute set of §9.7), each with its ISO-C-facing name and its documented intent.
Keeping the port with one compiler costs a page of macros and buys three things: the flag
classes of §10.2 can be reasoned about per translation-unit class instead of per file; the
extension inventory stays enumerable (an audit greps for bare `__attribute__`/`__builtin`
outside the port and fails — the parent's rule, mechanized); and the day the family must widen —
a second compiler for a new platform, a future ARM64 leg — the port is the diff, not the
codebase. *(build + analysis-catchable)*

---
# Part III — Execution

## 6. Concurrency: the two planes and the channels between them

### 6.1 The two-plane architecture, formalized

Chapter 2 drew the line; this chapter builds along it. The process's thread population is a
closed, named inventory — a composition-root fact, not an emergent property — and every thread
belongs to exactly one plane:

| role | plane | created | waits on | may block? |
|---|---|---|---|---|
| device loop (per stream) | RT | root | the device's pacing signal only | only there |
| RT workers (fixed pool, §6.5) | RT | root | the fork-join gate | only there |
| control (UI, session, device juggling) | control | root | anything | freely |
| streaming worker (disk prefetch/spool) | control | root | its request queue | freely |
| telemetry drain | control | root | the flight ring's drain cadence | freely |

The shape has a pedigree worth citing: it is `half-sync-half-async` — an asynchronous layer and
a synchronous layer meeting at a queueing boundary — with the asymmetry sharpened (the "async"
side here is the *paced* side); and its operational law is `non-stop-forwarding`: the data plane
keeps rendering when the control plane stalls, hangs, or restarts. A frozen UI must produce
frozen *meters*, never frozen *audio* — that sentence is this architecture's acceptance test,
and it is testable (ch. 14 injects a stalled control plane and asserts the stream).

Isolation between planes is the point, and it is the corpus's `bulkhead` — capacity partitioned
so one compartment's exhaustion cannot drown the other — enforced by construction: the planes
share **no locks** (there are none to share, §6.2), **no allocators** (the RT plane doesn't
allocate, invariant 3), and **no unbounded anything** (invariant 2). Within the RT plane itself,
data ownership follows `thread-confinement`: each datum has one writing thread, ever; what must
cross threads crosses one of §6.3's channels. The parent's one-writer-per-datum actor instinct
survives whole — what changes is that the channels are now the *entire* interaction surface,
because on this platform even a briefly-shared lock is a hazard (next section).

### 6.2 Why the real-time plane holds no locks

The rule is invariant 1's harshest clause and the domain's most-relitigated one, so the argument
is spelled out once, here, in full.

A mutex is a *bet on the holder's promptness*. When the RT thread contends a lock, its wait is
bounded by what the holder does while holding — and on a general-purpose kernel the holder (a
control-plane thread, by construction of the sharing) can be **preempted** by the fair scheduler
for a full timeslice, **paged** (a millisecond-class stall, §8.1), throttled, or migrated. The
classic name for the hazard is priority inversion, and the classic cures do not rescue it here.
`priority-inheritance-protocol` exists on this platform only in specific corners (the Linux
PI-futex machinery that `sharajkumar90`'s lineage reached), is absent from ordinary NT
synchronization primitives, and even where present converts the wait into "bounded by the
holder's *elevated* critical section" — which still includes the page fault the holder can take
while elevated. `priority-ceiling-protocol` — the parent's default where shells offer it —
requires a closed, analyzable task set and a cooperating scheduler; a desktop OS offers neither.
The conclusion is structural, not stylistic: **a lock's worst case on this platform cannot be
made small enough to sit inside a millisecond budget, so the RT plane simply never takes one.**

Spinlocks fail differently and just as hard: an elevated RT thread spinning on a lock held by a
preempted ordinary thread can spin for the holder's entire descheduled life — with the RT
thread's own elevated priority *keeping* lower-priority threads (possibly the holder, on a
saturated machine) off the core. `spinlock` and its scalable relatives (`ticket-lock`,
`mcs-queue-lock`) are built for kernels and for threads that cannot be preempted mid-hold;
userspace RT audio is neither. And the try-lock-with-fallback idiom — admissible in principle
because it never waits — is refused as ambient policy anyway: it turns every access into a
branch between two behaviors, and §6.3's channels cover every legitimate need without one.

What the plane uses instead is the wait-free subset of the lock-free spectrum. The distinction
is Herlihy's and it is load-bearing (`herlihyshavit`): *lock-free* guarantees somebody makes
progress; *wait-free* guarantees **this thread** completes **this operation** in a bounded
number of its own steps, regardless of what every other thread is doing — including being dead.
The RT side of every channel in §6.3 is wait-free in exactly that per-operation sense: a push
onto a full ring *completes* (by returning "full", counted — the overflow policy), a snapshot
acquire *completes* (it is one load), a parameter read *completes*. Retry loops that can be
starved by a peer (`compare-and-swap-loop` against a contended word) belong to the control
plane's side of the boundary, if anywhere. *(analysis + runtime-catchable: the guard machinery
of §15.2 traps lock and syscall entry on RT threads in development builds; the wait-free claim
per channel: host-test-catchable contract suites)*

### 6.3 The channel menu

Five shapes cover the boundary; each carries its contract, its cost, and its home use. Nothing
else crosses.

**(a) The atomic parameter.** One independent value, one writer, any readers: a lock-free
atomic scalar written with release, read with acquire (or relaxed where the value pairs with
nothing — §6.6), never torn on this class for naturally-aligned scalars up to pointer width.
The domain twist: the RT side treats what it reads as a *target*, interpolating per §4.3, so
control-rate writes and audio-rate consumption decouple cleanly. Cost: nothing measurable.
Limit: the moment two values must be seen *together*, this shape is wrong — coherence across
values is what (c) and (d) are for. The publication idiom is the corpus's `safe-publication`,
and the write-target/consume-at-quantum protocol is this booklet's own (editorial).

**(b) The SPSC ring.** The parent's canonical channel (`spsc-lock-free-ring-buffer`), inherited
with its whole contract — one named producer, one named consumer, indices each written by one
side, acquire/release pairing on the index publication, bounded capacity, declared overflow
policy, counted drops (invariant 2). Three platform tightenings apply. The head and tail
indices live on **separate cache lines** (`false-sharing-avoidance-via-cache-line-padding` — on
one line, every push invalidates every pop's cached index and the channel's cost triples).
Capacity is a power of two, so wrap is a mask. And each side keeps a **cached copy of the
peer's index**, refreshing it only when the cached value says full/empty — the batching
observation the `disruptor` lineage (`lmaxdisruptor`) made famous, which drops the common-case
crossing cost to one uncontended load-and-store pair. Home uses: commands and sample-accurate events inward;
lossy meter/analysis frames and the flight ring outward. Cost: a few nanoseconds per element
uncontended; capacity × element size resident forever (invariant 3).

**(c) The snapshot swap.** For structure — the compiled schedule, a new impulse response, a
resource table — the shape is publish-and-retire: the control plane **builds the new object
completely, off-plane**, in its own arena; publishes it with one release-store of a pointer;
the RT plane acquires the pointer **once per block** (never mid-block — one coherent world per
block) and uses it without copying. This is the reader's half of `read-copy-update` — readers
proceed at full speed, updaters publish then wait for a grace period — with the grace protocol
made trivial by the plane structure: the RT thread stamps a relaxed **generation counter** at
each block boundary; the control plane retires the old object only after observing a stamp
proving the RT plane has moved past it. That is `epoch-based-reclamation` reduced to its
single-reader special case, and the immutability of the published object (`immutable-value`) is
what makes the whole shape correct — a "snapshot" anyone mutates after publication is a data
race wearing a design pattern's name. Cost: double-buffering the structure (old and new alive
across the swap window) — RAM this platform has; a retire latency of one block — inaudible by
construction. Hazards, named because each is a real defect class: publish-before-complete
(missing release/acquire — `safe-publication` violated), retire-too-early (grace protocol
skipped), and mutation-after-publish. All three are host-testable with a stress harness, and
the Linux leg's race detector (§14.6) catches what the tests provoke.

**(d) The latest-value mailbox.** For bulk state where only the newest matters — a meter frame,
an analysis spectrum, a control-surface state block — a three-slot exchange covers both
directions: writer fills a free slot and atomically exchanges it for the "latest" slot index;
reader atomically exchanges "latest" for its previously-held slot and reads. Both sides are
wait-free (one atomic exchange each), no value is ever torn (slots exchange whole), and
intermediate values drop by design — the policy *is* latest-wins, and unlike (b) it never
reports full. The catalogs carry `double-buffer` and `ping-pong-buffer`, whose protocols keep
the writer out of the reader's bank by turn-taking; the third slot is exactly what removes the
turn-taking so both sides free-run — the corpus has no element for the three-slot form, so this
paragraph is the booklet's editorial statement of it, contract included. Cost: three copies of
the payload, resident forever.

**(e) The sequence lock.** For a small, mixed, read-mostly snapshot published *by* the RT plane
(current stream position, transport state, a few gauges read at UI rate), `sequence-lock`
inverts the usual asymmetry perfectly: the writer (RT) is wait-free — bump the sequence odd,
write the fields, bump it even, all plain stores between two releases — and the *reader*
(control) retries if it observed a torn window. Reader starvation is structurally bounded by
the write rate (once per block at most). Home use: the cheap always-on "where is the stream"
surface every UI wants, without dedicating a channel per field.

**What crosses where** — the standing assignment, so reviews argue about deviations rather than
rediscovering the menu:

| traffic | channel |
|---|---|
| independent parameter targets | (a) atomic parameters |
| grouped/ordered commands; sample-accurate events | (b) SPSC ring inward |
| new schedule, resource tables, impulse responses | (c) snapshot swap |
| meter/analysis frames outward | (d) mailbox, or (b) outward where *every* frame matters and loss must be counted |
| flight-ring events, histograms | (b) outward (drops counted — invariant 13's transport) |
| stream position / transport gauges | (e) seqlock |

### 6.4 DT-2 and DT-3 — crossing the boundary

**DT-2: data INTO the real-time plane.** Walk the questions in order; the first yes decides.

- **Is it one independent scalar value (or a few, each independently consistent)?** → channel
  (a), one atomic per value, RT-side smoothing per its contract.
- **Must changes arrive in order, or grouped atomically, or timed to a sample?** → channel (b),
  a command ring: the group travels as one message; sample-accurate events carry timestamps and
  the block splits on them (§4.3). Size the ring for the worst legitimate burst (a
  control-surface sweep, an automation dump), declare the overflow policy — for commands,
  overflow means *reject and report*, never silently drop half a group.
- **Is it structural — anything with internal pointers, anything whose consistency spans many
  words, anything sized in kilobytes?** → channel (c), snapshot swap, built off-plane, published
  whole. The graph rewire is the canonical case: the compiler emits a new schedule (with state
  *migration* for surviving nodes resolved at build time — new schedule entries point into the
  same state arena slots where the node survives), the swap lands at a block boundary, the old
  schedule retires on the generation protocol.
- **Is it "the newest wins, history worthless"?** → channel (d).
- **None of the above fits** → the design is trying to make the RT plane *ask* for something —
  and pull is the wrong direction across this boundary. Restate the need as data the control
  plane can push, or as work the RT plane shouldn't be doing (streaming a file belongs to the
  worker + a ring of filled buffers, §6.5's last paragraph).

**DT-3: data OUT of the real-time plane.**

- **Is loss acceptable if counted?** (meters, spectra, debug taps) → (d) if latest-only, (b)
  outward with drop counters if the consumer wants the sequence.
- **Must every record survive?** (the flight ring's events, xrun records) → (b) outward, sized
  so overflow is a design-error signal, drops counted and *alarmed* rather than merely counted
  (invariant 13; §13.2 sizes it).
- **Is it a tiny always-current gauge cluster?** → (e).
- **Is it big and must it survive?** (a captured buffer, a full-resolution analysis) → the RT
  plane writes into pool-allocated blocks handed to it in advance (ownership transferred inward
  through (b), returned outward through (b) — the parent's buffer-ownership contract, invariant
  12 there), so the bulk never copies and the RT plane never allocates. The streaming worker's
  record path is this shape.

### 6.5 DT-4 — parallelizing the graph

One core of the reference class renders a very large graph inside a 128-frame budget; reach for
parallelism when the *measured* schedule cost (§10.6's bench, §13.2's histogram) crowds the
headroom floor, not when the graph merely looks big. Then walk:

- **First: can the work shrink?** The cheapest parallelism is the work you stop doing — §9's
  ladder (algorithmic change, precomputation, SIMD) usually buys more than a second core, at
  lower risk. Exhaust DT-7's earlier rungs first.
- **Second: can the product pay with latency instead?** Doubling the period halves the pressure
  with zero new failure modes (invariant 16's dial exists for this). A non-interactive path
  (mixdown, streaming) should *always* take this branch.
- **Pipeline the graph** (`pipeline-parallelism`) when the graph has long serial chains with
  natural stage cuts: stage k renders block n while stage k+1 renders block n−1 — throughput
  multiplies by the stage count, **latency grows by one block per added stage** (accounted in
  §7.3), and the stages communicate by exactly the channels of §6.3 (per-stage SPSC of filled
  block buffers). Choose it for throughput-bound offline/streaming paths; refuse it where the
  added latency lands on a musician's fingers.
- **Fork-join inside the block** (`fork-join`; `loop-parallelism` over voices/channels;
  `parallel-reduction` for the mix-down sum) when latency cannot grow: the device-loop thread
  forks the block's independent subgraphs (voices are the classic — `data-parallel-architecture`
  at graph grain) across a **fixed pool of RT worker threads** created at the root, elevated and
  placed like their master (§5.3, §11.2), and joins before submit. The join is the hard part and
  gets its own paragraph below.
- **Never** hand signal work to control-plane threads, a system thread pool, or anything whose
  scheduling class the design does not own. A "worker" that renders audio at fair-share priority
  is a random-latency generator wired into the product.

**The join, priced.** Fork-join's cost on this platform is concentrated in waking and gathering
the workers inside a fraction of a millisecond. Three mechanisms, in cost order. **Blocking
wake**: a futex or event per worker (`futex`, `drepperfutex`) — microseconds each, and
tail-risky under load, because every wake is a scheduler visit. **Bounded spin**: workers
busy-poll a go-word for at most the block's duration — lowest latency, but it burns a core per
worker while idle, hostile on laptops and shared boxes. And the **hybrid** the corpus records
as `eventcount` — spin briefly, then park on the OS primitive; the lock-free fast path with a
blocking slow path — which is this booklet's default: it meets the common case at spin speed
and bounds the idle burn. Two further
rules keep the pool honest: **work assignment is static per schedule** — the graph compiler
partitions the ops at compile time (§4.2), because `work-stealing` deques, for all their genius
at irregular workloads (`blumofeleiserson`), buy their load balance with CAS traffic and
unbounded steal attempts that have no place inside a deadline; and **the pool never exceeds the
physical P-cores available to the process** (§11.2) — oversubscribed RT threads do not overlap,
they *queue*, and elevated queuing is priority inversion against yourself. Amdahl closes the
tree honestly: the serial spine (the join itself, the final mix, the submit) bounds the speedup,
so measure the parallel schedule's *tail*, not its mean, before shipping the complexity —
`mattsonppp` and `mccoolspp` carry the pattern language this paragraph compresses.

**The streaming exception.** Disk-fed sources (samplers, players) look like a parallelism
problem and are not one: the streaming worker is a *control-plane* thread filling pool buffers
ahead of the play cursor through channel (b), with the RT plane consuming filled buffers
wait-free and a designed underrun behavior (the degrade ladder's "bypass the starved voice"
rung, §12.2) when the disk loses the race. Prefetch depth is a product parameter; the shape is
`queue-based-load-leveling` with the queue's emptiness as a counted, designed event.

### 6.6 The memory-ordering discipline

Concurrent correctness in this codebase is written in exactly one language: the C11 memory
model — `stdatomic.h`, explicit orderings — regardless of the strong x86-TSO hardware the class
pins. The reasons are the parent's compiler-agnosticism argument transposed: the *compiler*
reorders what the hardware would not (the optimizer is bound only by the abstract machine), so
"x86 is strongly ordered" defends against the wrong adversary; and the model is the only
portable statement of intent an ARM64 port or a race detector can audit. House rules:

- **Four blessed idioms** cover this codebase: release-store/acquire-load publication (channels
  a, b, c — `acquire-release-ordering`, `safe-publication`); relaxed counters (statistics,
  generation stamps — anything read for *trend*, not for *ordering*); acquire-release
  read-modify-write on the exchange slots (channel d); and the seqlock's paired
  sequence-number protocol (channel e). Each use cites its idiom in a comment; a bare atomic
  with default (sequentially-consistent) ordering is treated as unreviewed code — not because
  seq_cst is wrong but because it is *unstated intent* that also buys the x86 fence cost on
  every store.
- **Fences are exceptional.** A standalone `memory-barrier` appears only inside the channel
  implementations, never in kernels or shell logic; the channels *are* the concurrency API.
- **`volatile` is not a concurrency tool here either** — the parent's §7.2 rule survives with
  its MMIO justification removed: there is no MMIO in userspace audio, so volatile in this
  codebase is simply a defect flagged by review, with the single traditional exception of
  signal/exception-context flags where the platform demands it, quarantined in adapters.
- The reasoning canon behind these rules is carried whole by the corpus: `kernelsyncdoc` (the
  kernel's memory-barriers document), `preshing`'s acquire/release series, `perfbook` for the
  why-this-is-hard, `herlihyshavit` for the progress taxonomy. When a new channel shape is
  proposed, the review standard is a written happens-before argument in those terms —
  `contract-only`, and scheduled review is the enforcement (§15.5), with the stress suites and
  the Linux race-detector leg as the mechanical net under it.

### 6.7 DT-5 — the waiting policy

Every thread's wait behavior is declared at creation; the tree is short because the planes
decide most of it:

- **Device-loop thread** → blocks in exactly one place (the device signal). Everything else it
  touches is wait-free. It never sleeps, never yields, never polls.
- **RT workers** → the `eventcount` hybrid of §6.5, tuned by the product (spin budget ≈ the
  fork latency it must hide), parked blocking when the stream stops.
- **Control-plane threads** → ordinary blocking waits with timeouts per the parent's §8.3
  (every wait bounded, the two poles chosen per wait). The UI thread obeys its framework.
- **Nobody, anywhere** sleeps-to-poll a condition another thread could signal, and nobody
  yields as a synchronization primitive — a yield is a scheduler donation with no contract on
  either kernel (who runs next is not yours to know), and every legitimate use in this codebase
  is better spelled as a blocking wait or a bounded spin. *(analysis-catchable: the sleep/yield
  symbol set is on the RT-plane poison list; contract-only elsewhere)*

### 6.8 Stopping, and changing shape

Reconfiguration that changes the *stream contract* (rate, format, period, device) is not a swap
— it is a **stop-and-restart of the composition root's tail**: fade out (ch. 12's ramp), stop
the device loop, join RT workers, rebuild what the negotiation changed, relock, re-elevate,
restart. The machinery exists and is tested because device loss forces it anyway (invariant
19); voluntary reconfiguration just calls it politely. Reconfiguration that changes only the
*graph* rides §6.4's snapshot swap without stopping. And full shutdown is `two-phase-termination`
end to end: signal intent (a command in-ring), fade, stop the pacing, join in reverse creation
order, drain and persist the flight ring's tail, free. A teardown path that can hang (a worker
parked on an eventcount nobody signals, a drain waiting on a ring nobody fills) is a designed
defect class the shutdown tests target by name (§14.4).

## 7. Two clocks

### 7.1 The device's clock and the machine's

Two clocks pace this program and they agree on nothing but the long run. The **device clock** —
the converter's crystal — defines *stream time*: sample position, the only time the core knows
(§4.1). The **OS monotonic clock** defines *machine time*: wakeups, timeouts, timestamps,
histogram buckets. Neither is the other: the device's 48000 Hz is 48000-and-a-bit, drifting
with temperature; the monotonic clock is the machine's TSC-backed timebase dressed by the
kernel. The parent's rule that a timestamp's source and resolution are part of its contract
(parent §8.1) does its first real work right here: every time-touching interface in this
codebase says *which* clock, and the calendar clock is banned from both planes for anything
but display (it jumps; nothing sequences on it).

The two clocks meet in exactly one data structure: at every device wakeup, the adapter captures
the pair *(stream position, monotonic now)* — hardware-reported position where the API offers
it, loop-counted position where it does not — and publishes it through channel (e). That pair
stream is the whole basis of cross-timeline reasoning: everything else derives.

### 7.2 Drift, and who resamples

From the pair stream, a small filtered estimator (editorial mechanism; a first-order low-pass
over the position-vs-time slope is the domain's workhorse) yields the device's *actual* rate
against machine time. It matters exactly where two rate domains meet:

- **One device, self-paced product** (the common case): drift is irrelevant to the audio path —
  the device paces everything — and the estimator's only consumers are diagnostics and display.
- **External timelines** (sync to video, MIDI clock, a network session): convert *positions*
  through the pair stream; never schedule audio against machine time directly. The estimator's
  smoothed rate is what keeps derived positions from jittering at the callback granularity —
  the `jitter-buffer` shape (buffer briefly, release on a steady clock) applied to time itself.
- **Two audio devices** (in one process, unsynchronized crystals): the honest solutions are one
  clock master plus **asynchronous sample-rate conversion** on the other stream (a resampler
  whose ratio tracks the drift estimator), or hardware word-clock sync outside the program. What
  is refused is the folklore alternative — occasional sample drops/duplicates to "catch up" —
  which is an uncounted, audible glitch generator wearing a scheduler's clothes. Multi-device
  topologies beyond one-master-one-slave are left OPEN for a grandchild (ch. 16).

### 7.3 Latency, accounted end to end

The user's "latency" is a sum, and this booklet requires the sum be *computed, carried, and
reported* rather than folklore-estimated: input converter and device ring; period assembly
(§4.4's quantum remainder); **the graph's own latency** — lookahead limiters, linear-phase
filters, FFT-block processors each declare their samples of delay in the op contract, and the
graph compiler folds the schedule's total (it is a longest-path computation over the compiled
graph) into a per-run latency report alongside the schedule hash; the output ring; the output
converter. Where the platform reports its stack's contribution (both device APIs expose stream
latency queries), the adapter captures it into the same report. The computed sum is then
**verified physically** at target-test cadence — a loopback cable and an impulse: measured
round-trip minus computed round-trip is the stack's unaccounted remainder, trended per release
(§14.6) — because a latency figure nobody measured is marketing, and this domain's users buy
on it. *(build-catchable: the per-op latency declaration is schedule-compiler input;
target-test-catchable: the loopback check)*

### 7.4 Timers, for the plane that may have them

The control plane uses ordinary OS timers through the clock/timer adapter (high-resolution
waitable timers on NT, timer file descriptors folded into the control loop's wait on Linux) for
UI-rate work: meter decay, autosave, watchdog-style liveness checks on the RT plane's heartbeat
(§13.2). Two rules close the chapter: **no timer ever paces the RT plane** — the device is the
metronome, and a timer-paced render loop free-runs against the device's true rate, guaranteeing
periodic over/underrun by construction (the folklore "just render every 2.9 ms" design defect,
named so reviews can kill it on sight). And **timer resolution is a queried fact, not an
assumption** — the legacy NT global-resolution knob is explicitly not part of this design (the
event-driven audio path never needs it), so the control plane's timers take the resolution the
OS grants and the design tolerates coarseness there by construction. *(host-test-catchable: the
control loop runs against the fake clock port per the parent's injected-time rule)*

---
# Part IV — Memory

## 8. Memory as architecture, on a machine that has plenty

The parent's memory chapter fought scarcity; this one fights **virtuality**. RAM is abundant,
but every byte of it is a *promise* — demand-paged, copy-on-write, reclaimable, compressible —
and a promise the kernel redeems at its own pace. The RT plane cannot afford the redemption:
a minor fault (the page exists but isn't mapped in) costs microseconds; a major fault (the page
is on disk, or was never materialized) costs milliseconds — one page fault can outspend an
entire period. So this chapter's law is invariant 3 restated as mechanism: **everything the RT
plane can touch is materialized, locked, and warm before go-live** — and its craft is the layout
discipline that makes what the plane touches *small and close* (§8.4), because the cache
hierarchy is the second, subtler landlord.

### 8.1 Residency: making the promise real

Allocation is not residency. A successful allocation on either kernel returns *address space*;
the pages arrive on first touch, and can leave again under pressure. The residency port (§5.4)
closes the gap at the composition root, and its adapter semantics are documented per OS because
the kernels' promises genuinely differ:

- **Linux**: lock the whole address space, current and future, through the standard locking
  interface (`kerrisktlpi` carries the API's exact semantics); the lock limit is a per-user
  resource limit the deployment must raise (the audio-group convention every Linux audio
  deployment inherits — a hub fact with a config row, ch. 16). Locking prevents *reclaim*; it
  does not populate — so the root still **touches every page** it allocated (one write per page,
  §4.5 step 5), and the warm-up pass (§4.5 step 7) faults in the code and read-only tables the
  locked-future clause already covers.
- **Windows**: per-region locking plus a raised working-set floor — the adapter documents the
  honest nuance that locked pages are guaranteed resident *while the process is scheduled*,
  which is the guarantee this design actually needs, and sizes the working-set minimum above
  the locked total so the lock requests cannot fail against the default quota.
- **Both**: the *code path* is part of the working set. Lazy symbol binding is resolved at load
  time on the Linux leg (bind-now linking — `drepperlibs` is the canonical treatment of PLT
  mechanics and why lazy resolution is a first-call fault), and the Windows leg ships no
  delay-loaded imports on any RT-reachable path. Shared-library count on RT paths is kept
  near zero anyway by the static-linking preference of §10.4.
- **Failure is at the root, loudly** (invariant 14): a lock refusal or quota failure is a
  go-live decision — degrade (run unlocked, tell the user, expect stalls) or refuse — per the
  product's recorded policy, never a silent fallback discovered as an xrun in the field.

One honesty row closes the section: locking defends against *reclaim*, not against **commit
exhaustion** at allocation time (the NT commit charge, Linux's overcommit-then-OOM regime — two
different failure shapes with the same design answer): the root allocates everything up front
precisely so that memory exhaustion is a *startup* failure with a clean message, never a
mid-stream event (parent §10.4's fail-fast pole, applied to the whole memory plan).

### 8.2 Real-time stacks

Each RT thread's stack is created by the thread port pre-sized (a generous fixed budget — this
platform's abundance, spent on certainty), **guard-paged** below (`guard-page` — the MMU is
always present here, so the parent's no-MMU substitutes retire and the trap is real), locked and
prefaulted to its full depth at creation (a touch-down-the-stack loop before the thread enters
its plane). Development builds paint and watermark it (`stack-painting-watermarking`) so the
soak rig reports actual depth against budget (§14.6). The code rules that keep the budget
meaningful are inherited analysis rows: no recursion on the RT plane, no variable-length
arrays, no dynamic stack allocation — each is an unbounded stack in disguise, and the analysis
gate refuses them in RT-marked translation units (§15.2). *(runtime + analysis-catchable)*

### 8.3 DT-6 — the allocation classes

The parent's allocation ladder survives with its rungs re-priced: on this platform the ladder's
lower rungs cost nothing to refuse, so the RT plane simply never descends it. Every object in
the process belongs to one of five named classes, chosen by one question — **when does it die?**

- **Immortal** (lives to teardown): the state arena, buffer pool, channel storage, flight ring,
  lookup tables. One `memory-arena` bump-allocated at the root, locked, never freed
  (`lazy-cleanup` is the honest name for deliberate never-freeing; teardown releases the arena
  wholesale). This class is 90% of the RT plane's bytes.
- **Epoch** (lives until the next structural change): the compiled schedule and its derived
  tables. Its own arena per epoch, built control-side, retired whole through §6.3(c)'s grace
  protocol — the arena *is* the `memory-discard` unit, so the swap frees everything at once and
  fragmentation is structurally impossible.
- **Pooled populations** (N alive at once, churning): voices, in-flight events, streaming
  blocks. Fixed-size pools (`pool-allocation`, `fixed-sized-buffer`) with `free-list` recycling;
  where stale-handle bugs are a risk (a voice released and reused while a command still names
  it), the pool's handles carry generations — the corpus's `slot-map` — so a stale handle is a
  *detected* error, not a corruption (the parent's memory-poisoning instinct, typed). Pool
  exhaustion is the parent's invariant-11 scoping verbatim: sized-against-design overflow is a
  defect; overflow fed by external demand (voices under a MIDI flood) is the degrade ladder's
  business (§12.2), counted and shed by policy (`load-shedding`, voice-stealing being its
  domain name).
- **Block scratch** (lives one block): the per-block workspace some kernels want beyond their
  slots. A per-thread scratch arena reset every block — pointer rewound, nothing freed — the
  cheapest allocator that exists and the only one legal on the plane.
- **Control-plane general** (everything else): the ordinary heap, used ordinarily. One
  discipline imported anyway: allocation flows through an `allocation-wrapper` in development
  builds so the guard machinery can *prove* the RT plane allocates nothing (§15.2) and the
  leak/pressure counters exist product-wide. Where a control-plane component genuinely needs
  bounded-time allocation (rare — it has no deadline), the cataloged constant-time allocator
  family (`two-level-segregated-fit-allocator-tlsf`) is the named option; the default remains
  the system heap.

The class is declared where the object is created, the root's memory plan enumerates every
immortal and pooled region with its size derivation (from the negotiated format and the
schedule — §4.5), and `memory-limit` budgets per subsystem make exhaustion indict a component
rather than the process. *(build-catchable: the plan's sizes are asserted at root;
runtime-catchable: pool watermarks and wrapper counters, §13.2)*

### 8.4 Layout: the cache is the fast path's landlord

Correct residency makes memory *exist*; layout makes it *cheap*. Four disciplines, each a
mechanical answer to the hierarchy of §1.2:

**Budget the working set per block.** Sum what one block's execution actually touches — state
blocks of the scheduled ops, their parameter blocks, the live buffer-pool slots, the schedule
itself — and hold the hot sum inside the per-core budget (L1d for the innermost voice loop's
per-iteration state; L2 for the block's whole footprint is the workhorse target on the
reference class). The graph compiler's liveness-based buffer assignment (§4.2) exists for this
number; the bench harness prints it (§10.6) and the review gate is a comparison, not a feeling.
Working set, not instruction count, is the first thing to interrogate when a kernel's measured
cost disappoints — on this class a cache-resident O(n log n) routinely beats a DRAM-touching
O(n).

**Structure-of-arrays for the populations.** Voice state is laid out as parallel arrays per
field (`data-locality` — arrange data contiguously in the order the processing walks it), not
as an array of voice structs: the per-sample loop over N voices then walks N contiguous
elements per field it actually uses — no dead bytes in the lines, and the layout *is* the
vectorization enabler §9.7 assumes (lane k = voice k). The corpus carries the shape from two
independent lineages — `column-oriented-storage` (with the catalogs' one explicit SIMD note)
and `entity-component-system` — converging on the same mechanics this domain reinvented as
"SoA voice engines." Hot/cold splitting rides along: per-sample-touched fields in the SoA
arrays; per-block and per-event fields (envelope stage, note id) in a separate cooler array;
config-rate data elsewhere entirely — so the innermost loop's lines carry nothing it does not
read. `packed-data`'s trade is declined for hot state (natural alignment beats saved bytes
here) and taken for cold config.

**Alignment and padding are contracts.** Every SIMD-touched array aligns to the vector width,
every per-thread and cross-thread structure pads to the cache line (the channel indices of
§6.3(b) being the canonical case — `false-sharing-avoidance-via-cache-line-padding`, with
`perfbook` as the mechanism's standing reference), and both spellings live in the compiler
port (§5.6), asserted by static assertion where layout is a contract. One platform-specific
pothole is named because it recurs in exactly this domain: allocating many same-sized buffers
at page-aligned strides puts their same-indexed elements in the same cache sets and defeats
store-forwarding disambiguation on same-page-offset accesses — the classic 4 KiB-aliasing
stall family — so the buffer pool staggers its slot strides by one cache line past the page
multiple (editorial mechanism; the microarchitectural background is external-register
material, §17.3).

**Streams stay streams.** Delay lines, convolution histories, and recording tails are written
and read sequentially by construction, which is the access pattern the hardware prefetchers
reward with DRAM latency effectively hidden; software `prefetching` is a measured-only,
last-resort tool for the genuinely irregular walks (modulated delay taps, granular clouds) —
inserted only where the bench shows the stall today and re-measured every toolchain bump,
because a stale prefetch distance quietly becomes pollution. Non-temporal (cache-bypassing)
stores earn a sentence of honesty: at audio block sizes almost nothing this program writes is
truly write-once-never-reread soon, so the technique stays off the default menu and behind a
measurement (§10.6) where someone reaches for it.

### 8.5 Pages, TLB, and the large-page option

A working set that fits L2 still walks the TLB, and a scatter of small mappings can miss there.
Two cheap disciplines come first: the immortal arena is *one* large mapping (one lock call, one
contiguous range, minimal TLB entries), and hot tables live inside it rather than as a
constellation of individual allocations. Beyond that, both kernels offer large/huge pages
(explicit or transparent — mechanisms and their deployment knobs are hub facts, ch. 16), which
collapse the arena's TLB footprint further; this booklet files large pages as an **optional,
measured row** — worth taking for multi-hundred-megabyte sample sets and convolution libraries,
noise for small graphs — with the standing caveat that transparent variants can move latency
*into* the fault path if enabled machine-wide without thought. Editorial throughout; the
mechanism inventory belongs to the hub. *(target-test-catchable where adopted: the soak compares)*

### 8.6 What this platform retires, and what replaces it

The parent's memory chapter carried flash endurance, EEPROM emulation, memory maps, and
MPU-region planning; all retire here — persistent state is ordinary files on the control plane
(the session, the config, the flight-ring dump), and the MMU is not an optional enforcement
depth but the standing fact the whole chapter negotiates with. What replaces them as *this*
child's memory-plan deliverables (ch. 16): the residency inventory (every locked region, its
size derivation, its lock verification), the allocation-class assignment per subsystem, the
per-block working-set budget with its measured actual, the stack budgets with watermarks, and
the pool sizing table with overflow policies. Same discipline, new landlords.

---
# Part V — Mechanical Sympathy

## 9. The core loop and the microarchitecture

The term of art this Part borrows — *mechanical sympathy* — entered software through a trading
system built on exactly this booklet's bet: that a design shaped to how the hardware actually
works beats a design that abstracts the hardware away (`lmax-architecture`, `lmaxfowler`; their
ring, §6.3(b), came from the same program). The vocabulary of this chapter — latency versus
throughput, dependency chains, the three hazard families, speculation and its flushes — is the
standing architecture literature's (`hennessypatterson`); the catalogs carry no
microarchitecture elements (ch. 17 registers the gap), so where this chapter names a mechanism
the catalogs lack, it is editorial, grounded in that literature and in measurements on the
reference machine.

Two oracles govern everything here, and they outrank intuition **and this chapter**: the bench
harness (§10.6) — measured cycles, on the reference class, tail included — and the static
pipeline analyzer shipped with the pinned toolchain (llvm-mca on this booklet's leg inventory),
which explains *why* a loop costs what it costs. The standing law: **no optimization lands
without its before/after measurement** (invariant 15), and no measurement outlives a toolchain
bump unverified.

### 9.1 The shape of a kernel

The unit of optimization is the **kernel**: one op's transform of one block (§4.4). Every rule
in this chapter assumes — and the code review enforces — the canonical kernel shape:

- **Planar `float` blocks in, planar `float` blocks out** (§5.2 pinned the core's format):
  contiguous per-channel arrays, aligned per §8.4, restrict-qualified so the compiler may
  assume what the buffer-pool discipline already guarantees (distinct slots do not alias —
  the schedule compiler's slot assignment makes the qualifier *true*, not hopeful).
- **Counted loops with block-constant bounds**: the frame count arrives as a parameter, loop
  bounds derive from it arithmetically, and nothing inside the loop changes it. This is what
  makes the loop analyzable — by the vectorizer, by the pipeline analyzer, and by the reviewer.
- **Parameters resolved before the loop**: targets consumed, coefficients fetched, ramps set up
  block-side (§4.3); the per-sample body reads only locals and streams. A parameter fetch
  inside the sample loop is a load the register allocator should have owned.
- **No calls in the body** except the compiler port's intrinsic spellings: the math is inline
  by construction (§9.6 covers the library question), because an opaque call is an optimization
  barrier and a stack the analyzer cannot see past.

### 9.2 Instruction-level parallelism: feeding the out-of-order engine

A reference-class core retires multiple floating-point operations per cycle — but only when the
instruction stream offers it *independent* work. The gap between a kernel's arithmetic count and
its measured cycles is usually one thing: a **dependency chain** — each operation waiting on the
last, the whole out-of-order window idling behind a serial spine.

**The accumulator rule.** The canonical case is the reduction — a mix bus, a dot product, an
energy sum. One accumulator serializes on the FMA's latency: each add waits ~4–5 cycles while
the core could issue two per cycle — an eightfold-idle machine. The cure is the corpus's
`parallel-reduction` shape at instruction grain: **as many independent accumulators as the
latency-throughput product** (latency ≈ 4–5 cycles × 2 issue ports ⇒ 8–10 chains on the
reference class; the exact product is a hub fact per microarchitecture generation, the *rule*
is the class's), combined once at block end. With the SoA layout of §8.4, the accumulators are
simply vector lanes plus unroll — the vectorizer often builds this from a clean counted loop by
itself, and the remark gate (§10.5) plus the pipeline analyzer confirm it did.

**Recursive filters are honestly serial.** An IIR filter's next output needs its last — a true
data dependency no window can hide; a biquad chain's cost is its latency chain, nearly
independent of issue width. The domain's honest mitigations, in preference order. **Go wide
across instances**: the dependency is per-voice, so eight voices in eight SoA lanes run eight
chains in parallel and the machine is full again — the first-choice answer, because it changes
no numerics. **Shorten the chain**: transposed filter forms trade the chain's shape (a hub of
same-cost variants; measure). **Restructure the algebra**: a high-order cascade re-derived as
a parallel filter bank sums independent sections (classic DSP decomposition; editorial), buying
ILP at the price of re-derived coefficients and different rounding. And **block-level
reformulations** (state-space over the block) — real, published, and *priced*: numerics and
complexity both, taken only with an oracle test at tolerance (§14.3). What is refused is the
folklore of "optimizing" the serial chain by hand-scheduling its instructions — the out-of-order
engine already does that; the win is structural or absent.

**Chain-shortening pays everywhere**, not only in filters: a long expression re-associated into
a balanced tree, a running max computed as a tournament rather than a scan — but floating-point
re-association changes results, so it is done *in the source, explicitly* (the algebra is the
contract), never delegated to a fast-math flag (§9.6). Where summation error matters at the
re-association (long mix accumulations), `kahan-summation` is the cataloged compensation, priced
at ~4× the adds and usually reserved for offline/mastering paths.

### 9.3 Structural hazards: the units you contend for

Some costs are not dependencies but **contention for hardware**: the machine has few dividers,
limited load/store ports, and finite line-fill buffers (`hennessypatterson`'s structural-hazard
family). The domain's standing offenders and their standing answers:

- **Division and square root** are order-of-magnitude outliers (tens of cycles, poorly
  pipelined). The graph already owns the cure: anything derivable from parameters — 1/f, gain
  curves, normalization factors — is computed at *edit rate* by the parameter system or baked
  by the graph compiler (`lookup-table`, §4.2), never at sample rate. Residual per-sample
  divisions become reciprocal-multiplies hoisted per block; where a root or reciprocal is
  genuinely per-sample, the ISA's approximation-plus-refinement idiom (via the compiler port)
  is taken **with its tolerance written into the kernel's contract** and tested at that
  tolerance — an approximation nobody contracted is a drifting golden master (§14.3).
- **Memory ports**: interleaving/deinterleaving (the device boundary's format conversion) is
  store-heavy and lives only at the adapters (§5.2); inside the core, planar layout keeps
  loads/stores unit-stride and gather/scatter out of the instruction stream entirely (SoA again
  — the layout decision of §8.4 *is* the structural-hazard decision here).
- **The front-end**: a kernel bloated past the µop cache re-fetches and re-decodes in its
  hottest loop. The cure is restraint in unrolling (the vectorizer's defaults are near-right on
  this class; forced aggressive unroll is a measured-only override) and the cold-path hygiene
  of §9.4 keeping rare code out of the hot lines.

### 9.4 Control hazards: branches, and where decisions are allowed to live

A mispredicted branch flushes the pipeline — a mid-teens-cycle hole on the class — and the
predictor's accuracy is a resource the design spends. The discipline is a hierarchy of *where a
decision may live*, mirroring §4.2:

1. **Edit time** (free): mode decisions — bypass, mono/stereo, quality tier, modulation
   topology — are compiled *out* by the graph compiler emitting the specialized op variant. The
   per-sample loop of the shipped schedule contains no branch that the edit model already
   decided. This is `defunctionalization` earning cycles: the decision became data, the data
   became the op code, the branch became dispatch.
2. **Block rate** (cheap): per-block branches — is this ramp active, did an event land in this
   block — run once per quantum, predict near-perfectly (they rarely change), and gate straight
   runs of branch-free samples (the block-splitting of §4.3).
3. **Sample rate** (the scarce budget): what remains per-sample is selection, not control —
   clamps, min/max, crossfade selects, waveshaper segment picks — and it compiles to
   **branchless** forms: conditional moves and vector blends the predictor never sees. The
   clean C spelling (ternaries over arithmetic, explicit min/max idioms) reliably lowers to
   these on the pinned toolchain; kernels verify it in review with the disassembler when the
   bench flags an outlier, and only then reach for the compiler port's select intrinsics.
   Data-*dependent* per-sample branches (an if on the signal's value — gates, transient
   detectors) are the one legitimately unpredictable class: restructure to compute-both-blend
   where cheap, accept the mispredict where the taken path is genuinely rare and expensive, and
   say which in the kernel comment.

**Dispatch, measured.** The schedule loop's own branch — *which kernel next* — has two honest
spellings: the enum-switch, which the optimizer can inline small ops into (and LTO across the
schedule executor makes that real, §10.3), and the `function-pointer-dispatch-table`
(`threaded-code`'s descendant, whose catalog entry carries exactly this predictor discussion).
On a *stable* schedule the indirect predictor learns the call sequence either way; the switch
wins when ops are small (inlining erases the call), the table wins for an open op set (plugin
grandchildren). This booklet defaults to the switch for the built-in set, the table at the
extension seam — and files the choice under "measured, revisit per toolchain major" (§10.6).

**Branch hygiene around the loop**: error and rare paths are annotated cold through the
compiler port and outlined so the hot loop's fall-through is the common case and the i-cache
lines carry no exception prose. The corpus's `fast-path` names the shape; §10.5's PGO and
ordering then physically separate hot from cold text.

### 9.5 The flush-and-stall inventory

The commission asks for pipeline-flush limits by name, so the inventory is stated once, as a
review checklist — each entry with its owner:

| flush/stall source | owned by |
|---|---|
| branch mispredicts | §9.4's hierarchy |
| denormal assists (microcoded FP on tiny values) | §9.6 — FTZ/DAZ plus algorithmic hygiene |
| page faults | ch. 8 — residency; zero tolerated on-plane |
| false sharing (cross-core line ping) | §6.3/§8.4 padding |
| contended/locked RMW, seq_cst fences | §6.6 — the blessed idioms only |
| store-forwarding and 4 KiB-aliasing stalls | §8.4's stride staggering |
| frequency and C-state transitions (macro-stalls) | ch. 11 — floors and warm-up |
| µop-cache overflow, i-cache misses | §9.3 front-end restraint, §10.5 layout |
| self-modifying/JIT code | none: refused outright in this codebase |

The inventory's use is diagnostic: when the histogram (§13.2) grows a tail the bench cannot
reproduce, the autopsy (§11.5) walks this table — most entries have a counter or a trace event
that convicts or acquits them.

### 9.6 The floating-point regime

Invariants 4 and 11 land here as mechanism. Audio is the denormal literature's favorite victim
— decaying tails and feedback paths glide *asymptotically into* the denormal range and sit
there, where each operation takes a microcode assist costing tens-to-hundreds of cycles: a
reverb that idles at 2% CPU suddenly costing 40% on silence is this exact mechanism. The regime:

- **FTZ/DAZ on, per RT thread, at thread start** (the thread adapter sets the FP-control state;
  the mechanism is per-OS/per-ISA hub fact, the obligation is invariant 4), re-verified by the
  development-build patrol at block edges — because a library call on the wrong plane can
  silently restore precise mode, and the failure is a *performance* cliff no correctness test
  sees.
- **Algorithmic hygiene anyway**: feedback structures inject the domain's standard hygiene (a
  sub-audible dither/offset at the feedback point, or periodic explicit flush of decayed state)
  so kernel cost does not *depend* on the FP mode — the mode is then defense in depth, not a
  correctness input. Editorial, standard practice in the field (§17.3).
- **No NaN in nominal operation** — a NaN in a feedback path is permanent and spreading — but
  kernels do **not** test per sample; the development patrol scans block edges and state
  snapshots (§14.3's properties prove the kernels cannot generate one from legal input), and
  parameter validation at the boundary (parent's expected-condition discipline) keeps illegal
  input out.
- **Contraction pinned on, everywhere, both legs** (§10.2): FMA is the class's whole arithmetic
  advantage, so this booklet pins `-ffp-contract=fast` globally and *documents* the consequence
  — results differ from a no-FMA build in the last ulp — which is harmless precisely because it
  is pinned identically on both legs and inside the golden-master conditions (§14.3).
- **Value-changing fast-math is off in the core.** Re-association, reciprocal substitution,
  finite-math assumptions — each breaks either determinism (invariant 11) or the NaN/Inf
  semantics the previous rules rely on. Where a fast-math-style win is wanted, it is written
  into the algebra by hand (§9.2), where it is visible, tested, and pinned. Shell and
  control-plane TUs may take the relaxed classes if a measurement justifies it; the flag canon
  (§10.2) draws the TU-class line.
- **The math library is not deterministic across legs** — the two kernels' libm
  implementations legitimately differ in ulp — so determinism-relevant paths (anything a golden
  master covers) call the codebase's **own vendored kernels** (polynomial/table approximations
  with contracted tolerances, tested against a high-precision oracle per §14.3;
  `epsilon-ulp-float-comparison` supplies the comparison discipline). The control plane uses
  the system library freely.
- **Width policy**: `float` is the stream and state default (bandwidth, lanes — §8.4); `double`
  is taken *by named exception* where conditioning demands it (the classic: low-frequency
  biquad coefficients/state at 32-bit precision go unstable near DC — a hub-documented
  pattern), recorded in the op's contract with its cost (half the lanes, twice the bytes).

### 9.7 The SIMD ladder

The class floor guarantees 8-wide single-precision FMA; a kernel that leaves it unused leaves
7/8ths of the machine idle. The ladder, in strictly this order:

1. **Auto-vectorization, verified.** The canonical kernel shape (§9.1) plus SoA (§8.4) is
   *designed* to auto-vectorize; the pinned toolchain's optimization remarks are wired into the
   build (§10.5), and invariant 15's gate fails the build when a listed hot kernel stops
   vectorizing — the silent regression this rung otherwise suffers per toolchain bump. Rung 1
   is where kernels should live and die; it is portable, readable, and free.
2. **Pragma-assisted.** Where the vectorizer balks for a stated, understood reason (an assumed
   dependence the design knows is false, a profitability misjudgment on a short loop), the
   compiler port's loop annotations (vectorize-enable, width and interleave hints) encode the
   *fact the human knows*, in place, with the reason in a comment. Still portable; still one
   source.
3. **Intrinsic kernels, as adapters.** Where the algorithm itself is lane-shaped in ways no
   vectorizer will find (cross-lane shuffles in an FFT butterfly, polyphase interleaves,
   horizontal reductions in a compressor's link stage), the kernel gets a hand-written
   per-ISA implementation — quarantined like every other platform fact: its own TU, compiled
   with that ISA's target attributes, selected by the **init-time dispatch table** (invariant
   12; parent binding-time rung 3 — never per-call detection, never IFUNC magic across the
   portability line), and paired with its scalar `twin`, the corpus's own name for a parallel
   test-visible implementation. The twin is the contract: equivalence at the kernel's pinned
   tolerance is a per-commit host test (§14.3), the twin serves as the fallback tier and the
   readable specification, and a twin that drifts fails the build, not the listener.
   **No inline assembly, at all**: intrinsics keep the compiler's scheduler and allocator in
   play and the analyzers' eyes open; the day an intrinsic cannot express it is the day to file
   the toolchain issue, not to write the escape hatch.
4. **Wider tiers by dispatch, not by floor.** The 512-bit tier (and whatever follows) is an
   *additional dispatch entry* built from the same twin-tested pattern, taken where the bench
   and the soak — not the datasheet — justify it on the deployed population; the floor stays
   `x86-64-v3` (§1.2), and frequency-behavior caveats of wider tiers are exactly the kind of
   generation-specific hub fact this booklet refuses to hard-code.

Two lane rules stop the classic self-inflicted wounds: **lanes are instances** (voices,
channels — §8.4's SoA) wherever the choice exists, because horizontal single-signal
vectorization spends its gains on shuffles; and **the block quantum is a multiple of the widest
lane count** (§4.4), so kernels have no scalar tail loop to maintain, test, and mispredict.

### 9.8 DT-7 — where an optimization lives

The chapter closes with the tree that orders all of Part V. Walk it top-down; **each rung's
gate is a measurement** (bench delta on the kernel, soak-tail delta on the system — §10.6,
§14.6), and the exit condition is invariant 6's headroom floor, *not* "as fast as possible" —
unspent engineering is a budget too.

- **0 — Measure and attribute.** Histogram tail or bench outlier? Compute-bound, memory-bound,
  or OS-induced (counters and the §9.5 inventory decide)? An optimization aimed at the wrong
  bound is pure risk.
- **1 — Don't do the work.** Algorithm, precomputation, edit-time specialization (§4.2), lower
  quality tier where the product allows. Nothing downstream competes with absent work — but
  the domain's classic trap is priced here: *silence-gating* a kernel trades constant cost for
  a data-dependent branch plus a denormal-tail cliff (§9.6) plus a block-size-variant behavior
  — gate at *block* granularity with hysteresis, or not at all.
- **2 — Fix the memory** (ch. 8): working set inside budget, SoA, alignment, stride hygiene.
  Memory wins are usually the largest and always the most durable across toolchain bumps.
- **3 — Shape the instructions** (§9.2–9.5): accumulators, chain structure, hoisted division,
  branch hierarchy. Verify with the pipeline analyzer, not vibes.
- **4 — Vectorize** (§9.7), in ladder order.
- **5 — Let the toolchain at it** (ch. 10): LTO, PGO, layout. Cheap, global, and last among
  code-level rungs because it amplifies whatever shape the code already has.
- **6 — Parallelize** (DT-4, §6.5) — after the single-core story is told, because cores
  multiply the good and the bad alike.
- **7 — Buy it from the OS or the deployment** (ch. 11, §11.6): placement, floors, isolation.
  Real, and last, because it is the rung the program controls least.

---
## 10. The toolchain is a port — and this booklet pins it

### 10.1 One family, two legs

The commission binds the toolchain: **clang/LLVM on both legs** (invariant 10). On Windows that
means the MSYS2 **CLANG64** environment — a full native toolchain producing ordinary PE
binaries against the Universal C Runtime: clang with lld as its linker, compiler-rt, libc++
(for C++ dependencies; the product itself is C17), libunwind, and the LLVM tool suite
(clang-tidy, clang-format, the static analyzer, llvm-profdata/llvm-cov, llvm-nm/llvm-objdump,
llvm-mca, lldb) — the component inventory was verified present on the reference machine
2026-08-12, clang 22.1.8, and lives as a dated row in the version hub (ch. 16), not as prose
anyone should trust undated. On Linux the same family arrives as the distribution's or
upstream's clang; the hub pins the floor version per release, and the two legs track the same
major.

What pinning one family buys, in this domain specifically: **one warning canon** promoted to
errors and identical on both legs; **one vectorizer** whose remarks the build can gate
(invariant 15); **one flag vocabulary** so the per-TU-class canon (§10.2) is a single table;
and — the quiet prize — **one code generator**, which is what makes bit-exact cross-leg golden
masters (invariant 11) achievable at all. The parent prized a *differing* host compiler as a
second opinion; the child spends that diversity deliberately and buys it back elsewhere: two
CRTs and two kernels already disagree productively (a UCRT build flushes out glibc assumptions
and vice versa), and the analyzer, clang-tidy, and the sanitizer suite (§10.8) supply the
independent eyes the second frontend used to.

The environment boundary is part of the pin: the Windows leg builds *in* CLANG64 (its
toolchain, its UCRT headers and import libraries), and the build refuses to mix environments —
mixed-runtime binaries are the MSYS2 ecosystem's classic self-inflicted wound, and the check is
one build-time assertion on the target triple and CRT linkage (`build-catchable`). Package
identities (the `mingw-w64-clang-x86_64-*` set) and their versions are hub rows.

### 10.2 The flag canon

Flags are the law of the build, so they are stated as law: one table, owned in one place (the
build system's single toolchain file per leg), organized by **TU class × configuration**, with
every deviation from parity across legs written as its own documented row. The canon's shape —
exact spellings live with the build, and the hub dates them:

| axis | classes | the rules |
|---|---|---|
| TU class | `core-kernel` / `core` / `shell-adapter` / `test-tool` | kernels: `-O3`, ISA floor `-march=x86-64-v3`, vectorize-remarks on, no value-changing math relaxations; core: `-O2`; adapters/shell: `-O2`, OS headers allowed; tests/tools: `-O2` plus instrumentation freedom |
| configuration | `dev` / `test` / `perf` / `ship` | dev: `-O1 -g`, asserts and guards on; test: `-O2 -g`, asserts on, sanitizer legs (§10.8); perf: ship's optimization plus profiling hooks; ship: `-O3` + ThinLTO + PGO, asserts per the parent's field-assert policy, guards compiled out |
| everywhere | — | `-std=c17`; the promoted warning canon with `-Werror`; `-ffp-contract=fast` (§9.6's pinned contraction); `-fvisibility=hidden`; `-ffunction-sections -fdata-sections`; debug info always generated, split/archived per §10.4 |
| per-leg rows | Linux | `-fno-plt` and now-binding at link (§8.1); relro; the ELF hardening set per deployment policy |
| per-leg rows | Windows | UCRT linkage assertions; the PE hardening set per deployment policy |

Two rules police the canon. **Nobody flags ad hoc**: a translation unit's flags come from its
class, and a kernel that "just needs" one special flag is either a new row in the canon
(reviewed, dated) or a design smell. And **the canon is diffed per toolchain bump**: a new
compiler major re-runs the remark gates, the bench suite, and the golden masters *before* the
hub row advances — the parent's run-the-tool rule, industrialized (§14.6). *(build-catchable
end to end)*

### 10.3 ThinLTO

Link-time optimization is on for `perf`/`ship` on both legs, in its Thin form: whole-program
inlining reach at tractable link cost, and the specific prize here is **the schedule executor
and the built-in kernels fusing** — the enum-switch dispatch of §9.4 inlines its small ops,
constants propagate across the op boundary, and the block loop's shape survives into the
optimizer whole. Per-ISA kernel TUs (§9.7 rung 3) keep their target attributes through LTO —
attribute-carrying functions do not merge across ISA boundaries — and the dispatch table's
init-time binding is unaffected. Full (fat) LTO stays available as a measured experiment per
release; the default is Thin. The mechanism's own documentation is corpus-carried
(`thinlto`, `thinltoblog`), a rare comfort in this chapter. *(build-catchable; the bench and
remark gates re-run under LTO because inlining changes both)*

### 10.4 Linking, runtimes, and the binary as an artifact

**lld links both legs** — one linker family, one map-file format habit, one set of section
semantics in the team's head. The product's own libraries link **statically** into the
executable: the RT plane's code path then crosses no PLT/IAT indirection, loads as one text
region (locked with everything else, §8.1), and versions as one artifact (invariant 17). The
OS-provided runtimes (UCRT; glibc and the loader) stay dynamic — pinning those is the
deployment's business, not the linker's. Shared-library plugin surfaces are a grandchild's
problem (ch. 16 leaves the seam OPEN) — and when they arrive they arrive as *control-plane
loaded, RT-executed only after the residency and warm-up rites* (§8.1 applied to foreign code).

Every ship link emits and archives its **map file** and split **debug artifacts** (DWARF on
both legs — one debugger story, lldb, matching the pinned family; the archive is what turns a
field crash record's addresses back into names years later — invariant 17's decoder half,
parent ch. 14's reconstructibility obligation transposed). The map file is also an audit input:
§15.3's section and symbol checks read it, and the working-set plan of ch. 8 sanity-checks
against its text/data sizes. `drepperlibs` and `levine` carry the linkage mechanics this
section leans on; the flags themselves are hub rows.

### 10.5 Layout: PGO, ordering, and the Linux-only post-linker

Code layout is memory layout (§8.4) applied to text, and the toolchain does it better than
hands do — *when fed*:

- **Profile-guided optimization, fed by the offline renderer.** The IR-level PGO workflow —
  instrumented build, representative runs, profile merge, optimized rebuild — has, in this
  codebase, something PGO deployments rarely enjoy: a **deterministic, representative workload
  by construction**, the offline render harness of §14.2 driving the real schedule executor
  over real sessions at full speed. The profile teaches the compiler the block loop's true
  branch biases, the dispatch's hot ops, and the hot/cold split of every rare path §9.4
  outlined — and the cold text moves out of the hot lines wholesale. The profile corpus (which
  sessions, which parameter sweeps) is versioned with the build system, because a PGO build is
  only as honest as its inputs; a stale or toy profile quietly *mis*-lays the binary.
- **The remark gates ride the same build**: the kernel list's vectorization remarks
  (invariant 15) and the missed-optimization remarks on the hot set are CI artifacts per
  build, diffed per toolchain bump — the mechanized form of "the compiler is a dependency
  whose behavior is verified, not assumed" (`godbolt` is the corpus's standing witness that
  what the compiler did is a thing you look at).
- **BOLT is a Linux-leg technique.** The LLVM post-link optimizer rearranges a *linked* binary
  from sampled production profiles and pays off on large instruction footprints; it is
  ELF-only — its absence from the CLANG64 toolchain was verified on the reference machine
  (2026-08-12), so the booklet says plainly: **the Windows leg's layout story is PGO +
  function-sections + the linker's ordering facilities; the Linux leg may add BOLT** where the
  product's text is large enough to care, as a measured, hub-documented row. Cross-leg
  determinism (invariant 11) is unaffected either way — layout moves code, not results.

### 10.6 The bench protocol

Invariant 15 keeps saying "the pinned bench protocol"; here it is — the measurement half of the
whole Part, and the reason two engineers' numbers can disagree without a fistfight:

- **Environment declared**: pinned to one named P-core, elevated like the RT plane, warm-up
  iterations first, machine identified (CPU model, governor/power state, SMT state), and — the
  rule that catches the most nonsense — **frequency policy stated**: either the deployment-real
  governor with the distribution reported, or a pinned-frequency diagnostic run, *labeled as
  which*.
- **Timebase serialized**: cycle-accurate timestamps through the clock port's bench mode, with
  serialization at the measurement edges so the out-of-order engine cannot smear work across
  the boundaries (mechanism per ISA in the compiler port; editorial).
- **Distribution reported, never a scalar**: minimum (the machine's honest capability), median,
  p99, max over N≥1000 iterations, plus spread; kernels normalize to **cycles per frame** so
  results compare across block sizes and clocks.
- **Cache state declared**: hot-cache (steady-state streaming, the default) and cold-start
  variants are different benchmarks; the suite runs both for anything the composition root or
  a graph swap touches.
- **The sink is real**: outputs written to a `volatile`-qualified or otherwise
  optimizer-opaque sink through the compiler port, because a benchmarked kernel the optimizer
  deleted measures the empty loop (the classic).
- **Artifacts are JSON, versioned, compared**: CI gates on same-machine baselines with
  tolerance bands; cross-machine comparisons only as *ratios* against a fixed reference kernel
  measured in the same session (editorial technique — it cancels the machine out of the
  comparison without pretending machines agree).

The catalogs carry no benchmarking-methodology element or work (ch. 17 registers it); this
protocol is the booklet's editorial synthesis, and it is itself code in `tools/`, versioned
with everything else.

### 10.7 Adapter-level optimization rows

Two rows live outside the core but inside the commission's "leverage the toolchain and
platform" clause, both **measured-only options** wired as adapter configuration, never as core
knowledge: the ALSA adapter's memory-mapped transfer mode (one fewer copy per period — §5.2),
and the WASAPI adapter's exclusive-mode/raw paths (bypassing engine processing where the
product owns the device). Each earns its keep through §10.6's protocol on the target rig, or
stays off.

### 10.8 The verification toolchain: sanitizers, analyzers, fuzzers

The same toolchain that builds the product polices it, and the matrix is pinned with the same
honesty about per-leg reality (component presence verified on the reference machine 2026-08-12;
versions are hub rows):

- **ASan + UBSan** run on *both* legs' test builds — the host suite of ch. 14 executes under
  them per commit (the parent's cheapest-UB-detection dividend, `asan` carrying the mechanism's
  paper). UBSan's trap-on-arithmetic classes back the parent's §10.7 arithmetic contract in
  every test run.
- **TSan is Linux-only** — verified absent on the Windows toolchain — so the concurrency stress
  suites (§14.4: channel torture, swap/retire races, shutdown storms) *live on the Linux leg's
  CI lane* and the booklet says so as a structural fact of the verification plan, not a
  footnote. The C11-model discipline of §6.6 is what makes single-leg race detection meaningful
  for both legs: the code under test is identical, and the model — not the hardware — is what
  TSan checks.
- **libFuzzer is present on both legs**; everything that parses bytes it did not write —
  session files, sample/media containers, control-protocol frames — gets a fuzz target as part
  of its definition of done (§14.4), run continuously at whatever budget CI affords.
- **clang-tidy and the clang static analyzer** are the `analysis-catchable` route's
  instantiation: the check set is pinned and dated in the hub with the parent-mandated
  deviation records; the RT-plane rules of §15.2 (banned-call lists, RT-TU restrictions) ride
  partly here and partly on the poison-header mechanism.

## 11. The operating system you don't control

Everything in this chapter is a **request** — the kernel may refuse, revoke, or quietly degrade
any of it — so the chapter's one absolute is invariant 14: *ask, verify what was granted, treat
refusal as a designed, reported mode*. Mechanisms are named by role; their exact spellings,
privileges, and version floors are hub rows (ch. 16), because this is precisely the layer that
decays.

### 11.1 Scheduling elevation

**Linux.** The RT plane requests the fixed-priority real-time class (SCHED_FIFO; the
round-robin variant adds nothing between threads that never yield). Getting it is a deployment
fact with three sanctioned shapes — a raised real-time resource limit for the audio user/group
(the classic distro convention), a session broker granting it on request (the rtkit path most
desktop audio takes), or a granted capability — and the adapter tries them in the product's
recorded order. Three system facts are designed around, not against. The kernel's **RT
throttling** reserves a slice for non-RT work by default — a correctly-built stream (bounded
work, §2.2's budget) never approaches it, and *disabling it is a deployment choice, never a
product requirement*. Brokers attach an **RT-time budget with a kill semantic**: a runaway RT
thread is killed, by design — our deadline monitor and degrade ladder keep the budget
unreachable, and the kill is one more reason invariant 1 is law. And priorities **within** the
band are ours: device loop above workers, workers above nothing else (only the plane is
elevated — a control thread at RT priority is a design defect by definition). `kerrisktlpi`
carries the API layer's canonical treatment.

**Windows.** The sanctioned elevation is the **multimedia class scheduler** (MMCSS): the
device-paced thread and the RT workers register under the Pro Audio task class as part of
thread start (§5.3), receiving scheduling in the real-time band *calibrated by the OS* — with a
reserved slice for the rest of the system playing the same role as Linux's throttle. Raw
real-time process priority is refused as ambient policy: it requires elevation rights, starves
the system's own machinery, and buys nothing MMCSS does not already grant more safely.
*(external-register facts: Microsoft's MMCSS documentation; §17.3)*

**Both**: the grant is read back and reported (class, priority, task handle), the shortfall
policy is the composition root's recorded decision (§4.5 step 6), and the *achieved* scheduling
is continuously evidenced by the histogram anyway — the only elevation that counts is the one
the tail distribution shows.

### 11.2 Placement: hybrid cores, SMT, and affinity as a request

The reference class is heterogeneous (§1.2), and the scheduler's default calculus — efficiency,
fairness, thermal spreading — will happily park an audio thread on an efficiency core whose
budget arithmetic is a different machine's. The design responds with **declared placement
intent, per thread, through the thread port** (§5.3):

- **RT threads prefer performance cores.** On Windows the intent is expressed by disabling
  power-throttling/EcoQoS classification for the RT threads and process so the scheduler's QoS
  machinery keeps them on the performance tier; on Linux, by an affinity mask over the
  performance cores where the deployment discovers the topology (or by trusting a
  correctly-configured scheduler where the distribution handles hybrid placement — a hub-dated
  judgment per kernel generation). Verified, reported, degraded-mode on refusal — as ever.
- **Two RT threads never share a physical core.** SMT siblings share execution ports and the
  L1/L2 — co-residency is §9.3's structural hazards imposed by scheduling; the worker pool's
  size and masks respect physical topology (§6.5's pool rule), and the device loop gets a
  physical core to itself in the deployment's ideal.
- **Affinity is a scalpel, not a default.** Pinning the RT plane hard buys determinism on a
  controlled rig and *removes* the scheduler's freedom to route around noise on a consumer box;
  the default is intent (QoS/preference), the hard mask is a deployment row (§11.6). The
  control plane is never pinned — it belongs to the scheduler.

### 11.3 Power: the frequency you get and the sleep you pay for

Two power mechanisms tax the deadline directly. **Idle-state exit latency**: a core that
napped deeply takes up to hundreds of microseconds to answer the device's wakeup — at a
1.33 ms period that is the budget's whole reserve — so, while streaming, the process holds the
platform's *latency floor* request (the character-device latency hold on Linux that desktop
audio infrastructure already uses; the corresponding execution/power request on Windows),
released when the stream stops, and the honesty rows say what it costs: battery, on laptops,
for the stream's duration — scoped exactly to it. **Frequency ramping**: the first
milliseconds after wake run below the marketing clock while the governor decides you are real;
the composition root's warm-up (§4.5 step 7) exists partly to arrive at go-live already
credible to the governor, and the bench protocol's frequency-policy declaration (§10.6) exists
because this mechanism otherwise falsifies measurements. Governor and power-plan selection are
deployment rows (§11.6) — the *product* must remain acceptable on the stock plan, with the
histogram as the judge.

### 11.4 The syscall-free plane, kept honest

Chapters 6 and 8 built the plane that needs nothing from the kernel per block; this section
keeps it true operationally. The development-build guard (§15.2) traps syscall-classed entries
on RT threads; the diagnosis mode (§11.5) counts what production cannot trap; and one
platform-specific honesty is recorded: some "function calls" are syscalls in disguise per
configuration (a monotonic clock read is user-space fast-path on both legs *normally* — a
hub-dated fact the clock adapter asserts at init rather than assumes forever). The rule of
thumb the review applies: on the RT plane, any call whose implementation the team cannot name
is treated as blocking until proven otherwise.

### 11.5 The autopsy

When the histogram grows a tail or an xrun lands, the platform can say why — if the program
asked in advance. Diagnosis mode (a build/runtime flag, off in ship-default, free of RT-plane
cost when off) arms three layers:

- **Per-callback deltas, sampled on-plane at block edges** (cheap counters through the thread
  adapter): minor/major fault counts, voluntary/involuntary context-switch counts, and the
  wakeup-to-start gap versus start-to-end duration split — enough to classify §2.4's taxonomy
  on the spot: late wakeup (gap grew), external stall (involuntary switches or faults mid-work),
  self-overrun (duration grew, counters quiet).
- **System-tracer correlation, off-plane**: the OS's own schedulers-eye view (ETW on NT; perf
  and the scheduler tracepoints on Linux) captured by the control plane during a diagnosis
  session, correlated to the flight ring by monotonic timestamps (§7.1's pair stream) — this is
  where "which driver's interrupt storm ate my period" gets answered, in the OS's evidence, not
  the program's guess.
- **The irreducible residue, named**: firmware-level stalls (SMIs) are invisible to both layers
  except as unattributed gaps; dedicated-rig diagnosis on Linux has a tracer for exactly that
  hunt (a hub row), and the booklet's posture stays §2.3's — minimize exposure, bound damage,
  keep the evidence honest rather than pretend completeness.

Autopsy findings attach to the xrun's flight-ring event (§13.2), so a field report carries its
own diagnosis as far as the platform allowed. *(runtime-catchable in diagnosis mode;
target-test-catchable: the soak rig runs with the first layer armed always)*

### 11.6 Deployment hardening: the rows above the product

A product that *requires* any row below is misdesigned (the stock machine is the requirement —
invariant 6 is proven there); a deployment that *wants* headroom can buy it, each row priced:

| row | buys | costs |
|---|---|---|
| dedicated/isolated cores for the RT plane (kernel boot isolation on Linux; reserved CPU sets on Windows) | the scheduler's noise removed from the plane | cores gone from the system; per-machine configuration |
| the real-time-preemption Linux kernel flavor (mainlined lineage; availability per distro is a hub row) | scheduler/IRQ-path tails shrink dramatically | a kernel decision the deployment owns; SMIs untouched |
| IRQ affinity steered off the RT cores (Linux) | driver interrupt storms miss the plane | configuration fragility across reboots/devices |
| SMT disabled in firmware | sibling interference gone, worst-case sharper | throughput for the rest of the machine |
| governor/power-plan pinned to performance | frequency floors, no ramp tax | watts, heat, battery |
| audio-group limits preconfigured (memlock, rtprio) | the elevation dance always succeeds | distribution packaging work |

Each adopted row is recorded in the deployment's own hub section with its verification command
— the parent's measured-claim discipline applied to machine configuration.

### 11.7 What this chapter refuses

Kernel modules or drivers shipped to win priority disputes (a support catastrophe wearing a
performance costume); undocumented scheduler tunables cargo-culted from forums (unverifiable,
version-fragile — if it cannot be a dated hub row with a command, it does not exist); disabling
OS security mitigations as a tuning tip (the measured wins on this workload do not justify the
posture, and the booklet will not normalize it); and the global timer-resolution squeeze as a
substitute for event-driven pacing (§7.4 already buried it — the event-driven design never
needed it, and the squeeze taxes the whole machine to hide a design defect). Each refusal is a
review checklist line (§15.5), because each is re-proposed annually with fresh enthusiasm.

---
# Part VI — Failure and Evidence

## 12. Errors, overload, and the safe state

### 12.1 The dispositions, mapped onto the planes

The parent's three dispositions survive intact and acquire a plane assignment, which is most of
what this domain adds to error architecture:

- **The control plane returns it, typed** — the parent's convention verbatim: status returns
  and result types, every fallible call checked or visibly discarded, adapter boundaries
  converting the platform's error vocabulary (errno, HRESULTs) to the codebase's one convention
  at the port, never propagating it inward raw.
- **The real-time plane absorbs and marks — and does nothing else.** It cannot return errors
  upward mid-block (to whom?), cannot block, cannot log (invariant 13), cannot stop; so every
  fault it detects follows the CHECKS lineage the parent carries (`exceptional-value`,
  `marked-data`): substitute the safe value (silence for a starved voice, the clamped sample
  for an over), **mark the event into the flight ring, count it**, and keep rendering. The
  parent's absolute holds with its teeth showing: absorbing with no record is `try/continue`
  with extra steps — on this plane the mark *is* the error handling.
- **Stop-the-world is a control-plane verb.** Development builds assert densely everywhere
  (the parent's samurai discipline, `samurai-principle`). In ship builds, a *contract violation
  detected on the RT plane* — an impossible state, a poisoned handle (§8.3's generation check
  failing) — does not abort the process mid-callback: it routes to the **stream's** safe state
  (§12.5): mark, fade, park the stream, hand the control plane the evidence and the decision.
  Process-fatal remains reserved for violations that indict process-wide integrity, decided by
  the control plane holding the evidence — the parent's escalation discipline (`escalation`,
  `units-of-mitigation`: the stream is this domain's restartable unit).

### 12.2 The degrade ladder

Overload is this domain's expected condition number one — a parameter storm, a pathological
patch, a neighbor process, a thermal downclock — and invariant 7 requires the response be a
*designed ladder*, entered and exited on the deadline monitor's measured headroom (with
hysteresis, so the system does not flap), every rung counted and visible:

1. **Shed the deferrable** (`deferrable-work`): meters, analysis taps, spectral displays —
   consumers of channel (d) simply get staler data. Inaudible by construction.
2. **Drop quality tiers** (`degradation`): the graph compiler already emits tier variants of
   the expensive ops (§4.2) — oversampling steps down, the convolution tail truncates, the
   cheaper interpolator engages. Audible under scrutiny, designed to be the *least* audible
   cycles available.
3. **Steal voices** (`load-shedding`, wearing its domain name): the population manager frees
   the least-audible members (quietest, oldest-in-release — the policy is named per product,
   never emergent). The corpus's `fresh-work-before-stale` states the general overload
   principle; voice stealing is its inversion — newest-work-wins — because a fresh note-on is
   the musician's *intent* and a decaying tail is history.
4. **Bypass by policy**: nodes marked bypassable (per-node product decision) drop out with
   their dry path intact.
5. **Fade to silence, stream alive** — the terminal rung and the domain's safe state (§12.5):
   the output ramps to silence over a designed interval, but the device loop *keeps running
   and keeps submitting* (silence is a valid buffer; a stopped submission is the xrun the
   ladder exists to prevent). Recovery walks back up the rungs as measured headroom returns.

The ladder is configuration — which rungs a product enables, their thresholds, their orders —
and it is *tested by fault injection as a matter of routine* (§14.4): CI drives synthetic
overload through the fake clock and asserts each rung engages, disengages, and counts.
*(host-test-catchable + runtime counters; the rung policies: contract-only, product-recorded)*

### 12.3 The xrun, lived through

When prevention fails, the failure is *managed*: the device adapter recovers the stream by the
platform's own protocol (the underrun-recovery verbs of §5.2), the first buffers after
recovery **ramp in from silence** (a resume click is a second defect on top of the first —
editorial, the domain's standard practice), the xrun event lands in the flight ring with its
autopsy attachment (§11.5), and the counters tick. Repeated xruns are a *trend* the control
plane watches (the parent's `riding-over-transients` with a `leaky-bucket-counter` — tolerate
a rate, escalate on overflow): escalation offers the user the honest trade — a larger period
(invariant 16's dial), a lighter session, a diagnosis capture — rather than silently suffering.
The one forbidden response is the folklore one: quietly growing hidden buffering until the
product's stated latency is fiction.

### 12.4 Device loss and format change

Invariant 19's designed events, walked once. **Device lost** (unplugged, claimed exclusively
by another process, server restarted): the stream's safe state engages (fade is moot — the
sink is gone — but the state machine's transition is identical), the control plane runs a
bounded, backed-off reopen loop against the configured device (or falls to the product's
fallback-device policy), the session and edit model are untouched (they live on the control
plane by construction), and the user is told the truth immediately. **Format invalidated**
(rate or layout changed under the stream by the OS or the user): full renegotiation through
§6.8's stop-and-restart tail — the composition root's steps from negotiation onward re-run,
the graph recompiles against the new format, and the stream resumes. Both paths are ordinary,
tested code (§14.4 injects both through the fake device per commit) — the difference between a
product that shrugs off a USB cable and one that dies to it is exactly whether these paths
were designed or discovered.

### 12.5 The safe state of this domain

The parent demands every failure path end in a named state; this domain's is **ramped silence
with the stream healthy**: output faded over a designed interval (a hard cut *is* a click —
the safe state must not manufacture the failure class it exists to contain), the device still
fed, evidence flowing, control plane deciding what next. Around it, one always-on guard earns
its cycles at the final bus: the **output sentinel** — the parent's `sanity-check` in domain
dress, a plausibility monitor on the actuator path (`monitor-actuator` is the architecture-
realm shape): clamp to full scale, replace NaN/Inf with silence, count and mark every
intervention (invariant 4 makes an intervention a defect *upstream* — the sentinel is
containment, not tolerance). It protects the listener's ears, the monitors' drivers, and the
product's reputation from the one buffer that should never have happened — and its counter is
on the front page of the session report because a nonzero value is a filed bug by definition.
The process may die; the *session* must not: the edit model autosaves on the control plane's
schedule, so the worst outcome of the worst failure is a restart into the last autosave — the
parent's error-kernel reading (`error-kernel`), with the session as the irreplaceable state
kept out of the blast radius.

### 12.6 The watchdog, translated

No hardware watchdog exists here, and the OS is not going to reboot for us. The parent's
watchdog architecture (`watchdog-architecture-pattern`) translates to a **control-plane
supervisor of the RT plane's progress**: the device loop publishes its block counter through
channel (e) as its heartbeat (`heartbeat` — proof of *progress*, not existence: the counter
only advances when blocks actually render, honoring Koopman's kick discipline by
construction). The supervisor — an ordinary control-plane timer consumer (§7.4) — alarms when
the stream claims to be live but the counter stalls: the hang class invariant 1 makes rare and
this monitor makes *visible*. Its response is the parent's `escalating-restart`, scoped to
this platform's restartable units: capture diagnosis, tear down and rebuild the stream (§6.8),
then the engine, then — where the product splits engine from UI across processes — let the
engine process die and be respawned (`let-it-crash`, `crash-only-software`: the posture is
available exactly because §12.5 keeps the session out of the engine's blast radius; the
process split itself is a grandchild's architecture row, ch. 16). Every rung leaves its story
in the flight ring first — the supervisor's kill is designed to be *readable* in the next
session's harvest (§13.4).

## 13. Observability: the flight recorder at 48 kHz

### 13.1 Postmortem-first, still

The parent's organizing question — *when this comes back from the field dead, what will it be
able to tell us?* — survives the platform upgrade untouched, because the observer is still not
there when it matters: the failure is on a stranger's machine, in a session you will never
see, reported as "it glitched during the second chorus." The answer is the same architecture
the parent binds: **evidence designed in, recorded always, harvested after** — with this
platform's twist that the recorder is nearly free (RAM is abundant, disks exist) while the
*recording* is nearly forbidden (nothing on the RT plane may block or format — invariant 13).
The resolution is the ring: the RT plane emits fixed-size structured events — an id, a
timestamp from the pair stream (§7.1), a few payload words, never a string — into §6.3(b)'s
wait-free channel; the telemetry drain renders, persists, and ships them on the control
plane's time. Emission costs nanoseconds and is always on; the *transport* has all the time in
the world. `ring-buffer`, `diagnostic-logger`, `log-errors` are the cataloged parts; the
composition is the parent's editorial flight-recorder synthesis, inherited and re-registered
(§17.2).

### 13.2 What is always on

Invariant 5's concrete inventory — the always-on set, each with one writer on the plane and
readers off it:

- **The callback histogram**: every render's cost (and separately, the wakeup gap — §11.5's
  split) into fixed log-spaced bins, updated by one relaxed increment; the whole distribution
  §2.6 demands, for the cost of an add. Percentile extraction happens off-plane.
- **The headroom gauge**: cost over budget, smoothed, published through channel (e) — the
  number the degrade ladder (§12.2) switches on and the UI's performance meter shows.
- **The counters**: xruns by class (§2.4), degrade-rung entries and exits, channel drops per
  ring (invariant 2's witnesses), pool high-water marks and steal counts (§8.3), output-
  sentinel interventions (§12.5), denormal/NaN patrol trips (§9.6), guard trips in development.
  A counter is one relaxed add; there is no budget argument against any of them.
- **The event stream**: stream state-machine transitions (the parent's *state machines log
  transitions*, applied to the stream/device/elevation state machines of chs. 5, 11, 12),
  boundary crossings at the ports (negotiation outcomes, grants and denials, device faults),
  every xrun with its autopsy attachment, every degrade-rung change. The parent's rule that
  boundaries log crossings and counters cover rates transposes with its economics improved —
  and its discipline unchanged: identifiers and words, never format strings (invariant 13).

### 13.3 The session report, and the replay dividend

Every run can end in an artifact: the **session report** — build identity (invariant 17),
machine class and negotiated format, the histograms, every counter, the degrade and xrun
event history with autopsies — serialized by the drain as structured data (JSON in `tools/`
convention), written on exit or on demand. Its consumers, deliberately identical in format:
the *user's bug report* (attach the file), the *soak rig's evidence* (invariant 6 gates on
exactly these fields — §14.6), and the *fleet view* where a product opts into telemetry
(local-first, upload explicit and consented — the posture is the parent's hostile-reader
clause wearing privacy clothes: nothing in the report identifies content, and the report never
carries audio).

The second dividend is **replay**: the command ring's inbound traffic (§6.3(b)) and the event
stream, recorded, are — because the core is deterministic under the pinned regime (§4.1,
invariant 11) — a *complete reproduction recipe*: the offline harness (§14.2) re-renders the
session's decision path bit-exactly, on the developer's machine, at file-write speed. That is
the parent's golden-master-over-the-decision-log machinery (`record-playback`,
`deterministic-lockstep`) with this domain's payoff attached: the field glitch that survived
§11.5's autopsy becomes tomorrow's regression test as a matter of *workflow*, not heroics.

### 13.4 Crash capture

When the process dies anyway: the OS's native postmortem machinery (minidumps on NT, core
dumps on Linux — `core-dump` is the cataloged shape; the capture configuration is a hub row)
carries the state, and the design's one obligation is to make the dump *worth reading*: the
flight ring and counters live in one contiguous, known, named region (§8.3's immortal arena)
so every dump contains the recorder by construction; the build identity is embedded in the
image (invariant 17) so the dump names its decoder (§10.4's archived symbols). The in-process
crash handler does the minimum the platform permits safely — stamp the crash event, flush
what can be flushed, hand off to the OS writer (async-signal-safety discipline on the Linux
leg; editorial) — and the *next* start detects the dirty exit, harvests the previous ring's
tail and counters from the persisted report-or-dump, and emits them as the new session's
first events: the parent's *every reset tells its story*, verbatim, with "reset" spelled
"relaunch." *(runtime-catchable; the dirty-exit harvest is host-tested by killing the process
under test — §14.4)*

### 13.5 Logs, and everything else

The control plane logs like the ordinary software it is — structured, leveled, rotated,
boring; the only domain rules are placement (never on the RT plane — invariant 13; the guard
traps it) and hygiene inherited from the parent: no secrets, no PII, the trace schema treated
as a versioned contract for whatever downstream tooling parses it (parent ch. 14's
expand/contract applies to event ids too — ids are stable, retired ids stay reserved). The
diagnosis-mode tool ecosystem — the OS tracers of §11.5, frame profilers, the vendor tools of
the trade — stays *outside* the product: external-register material (§17.3), correlated to the
product's evidence by the monotonic timestamps everything already carries. The maintenance
surface the parent mandates (`maintenance-interface`) exists here too, grown-up: the session
report on demand, the diagnosis-mode toggle, the counters' live view — read-only by default,
mutating members (degrade-rung forcing, period override) gated behind the product's own
control-surface authorization, and the whole surface compiled out per build variant exactly as
the parent requires (parent invariant 21).

---
# Part VII — Proof and Constitution

## 14. Testability: the offline machine

### 14.1 The dividend collected

Every structural decision since chapter 4 was secretly a testing decision, and this chapter
cashes them in. Because the core is a pure transform over data (§4.1), because the schedule is
data (§4.2), because time is the sample count and every OS touchpoint is a port (ch. 5), the
entire signal engine runs **headless, deterministic, and faster than real time** on any
developer machine and any CI box — no audio device, no elevated privileges, no kernel in the
loop. The parent's dual-target discipline arrives here with its cost inverted: the parent's
host build was an *approximation* of the target awaiting the metal's verdict; this child's
offline build **is the product's own core, bit for bit** (invariant 11), and the "target" rungs
exist to prove the *shell* — the OS negotiation, the elevation, the tail behavior — not the
math.

The instrument is the **offline renderer** in `tools/`: the second composition root the parent
demands, binding the fake device and fake clock adapters, driving the real schedule executor
over scripted sessions at file-write speed. It is the test suite's engine, the golden-master
generator, the PGO workload (§10.5), the replay consumer (§13.3), and the profiling target —
one artifact, five duties, which is exactly why it is maintained as a product, not a script.

### 14.2 The harness inventory

The suite's shape follows the parent's derivation — many fast tests against the pure parts,
fewer against the shell — with the port fakes carrying the domain's whole controllability
story (`test-double` in its fake grade; the parent's discipline that a fake earns the word
only by passing the same contract suite as the real adapter):

- **The fake device** is scriptable in exactly the dimensions the real one varies: period
  sequences (fixed, alternating, the legal jitter of shared-mode engines), format grants
  (including refusals and downgrades), fault-verb injection (underrun-recovered, device-lost,
  format-invalidated — §5.2), and pacing (as-fast-as-possible for rendering, real-time-shaped
  for soak-style host runs).
- **The fake clock** replays recorded pair streams (§7.1) or synthesizes drift and jitter to
  order — the drift estimator and latency accounting (§7.2–7.3) are tested entirely against
  synthetic clocks, which is the only way to test a ppm-scale estimator in milliseconds.
- **The contract suites per port** run nominal cases against fake *and* real adapters
  (device-in-loop, §14.6), fault cases against the fake by construction — the parent's
  partition, recorded per port.
- **Channel and state constructibility**: the schedule's state arena is constructible at any
  state by tests (the parent's `localize-state-storage` dividend — a filter mid-decay, a voice
  mid-release, a ladder mid-rung are all *values*, built directly rather than driven to), which
  is what makes property tests over state spaces tractable at all.

### 14.3 The numeric suite

The DSP's correctness net, in four layers:

- **Golden masters, two regimes** (`golden-master-testing`): the **exact** regime — bit-identical
  output, enforced per commit across *both legs* for the pinned-kernel path (the determinism
  conditions of §9.6/invariant 11 make cross-OS bit-equality a *test*, and its failure a
  toolchain-or-discipline regression by definition); and the **tolerance** regime — ULP- or
  dB-floor-bounded comparison (`epsilon-ulp-float-comparison`) for everything legitimately
  variant: SIMD tier versus scalar `twin` (invariant 12), approximation kernels versus their
  high-precision oracles (§9.6's vendored math, §9.3's contracted approximations), cross-tier
  dispatch equivalence. Masters are approved artifacts under the parent's approve-the-diff
  rule — a snapshot suite with auto-approval is a change recorder, not a test.
- **Properties** (`property-based-testing`, on the pure core where it is cheap): silence in →
  silence out (with the denormal patrol asserting the *state* also decays clean — §9.6);
  bounded in → bounded out for the sentinel-guarded bus; tail decay below the floor within the
  op's declared constant; no NaN/denormal generation from any legal input under full-range
  parameter fuzz; linearity where the op claims it; and **the block-partition property**
  (invariant 20) — every op and the whole schedule, rendered as one span versus every
  interesting partition of it, byte-compared — the single highest-yield regression net this
  domain has.
- **Tables** (`parameterized-test`): per-op boundary matrices — parameter extremes, denormal-
  adjacent inputs, full-scale and DC inputs, every sample rate in the support matrix — the
  boring grid that catches the boring bugs.
- **State-machine suites** for the stream/device/elevation/ladder machines (chs. 5, 11, 12):
  transition coverage plus illegal-transition assertions, host-run against the fakes.

### 14.4 Fault injection and the concurrency suites

Error paths are the product (parent ch. 12's stance, inherited whole), so per commit, on the
fakes: device loss mid-block, format invalidation mid-session, elevation denial at go-live and
revocation mid-stream (§11.1's degraded modes), residency-lock refusal, pool exhaustion under
event floods (§8.3's shed policies), disk starvation against the streaming worker (§6.5), and
synthetic overload sweeps that walk the degrade ladder up and down asserting every rung
engages, counts, and exits with hysteresis (§12.2). The dirty-exit story is tested the parent's
way: kill the process under test, relaunch, assert the harvest (§13.4).

Concurrency gets its own lane because its failures do not reproduce politely: **channel
torture** (full/empty boundary races on every ring, swap/retire generation races on the
snapshot path, seqlock read-retry storms, mailbox exchange storms) runs as stress suites under
the Linux leg's race detector (§10.8's TSan placement — the C11-model discipline of §6.6 is
what makes one leg's detection speak for both), and **shutdown storms** (§6.8) assert the
teardown cannot hang under adversarial timing. The fuzz targets (§10.8) cover every parser of
foreign bytes with the fuzzer the pinned toolchain ships. *(host-test-catchable, all of it —
that is the point)*

### 14.5 Performance regression

Correctness suites prove the output right; this lane proves the *cost* stays inside the
architecture: per-kernel benches under §10.6's protocol, gated against same-machine baselines
with tolerance bands; whole-schedule renders (cycles per frame, offline) trended per commit;
the vectorization-remark gate (invariant 15) failing the build when a hot kernel silently
de-vectorizes; and the working-set report (§8.4) diffed so a layout regression is a review
event, not a field discovery. The gates alarm on *regression*, not on absolute numbers —
absolute truth belongs to the soak rig (§14.6), machines being what they are.

### 14.6 The CI matrix and the target rungs

The cadence ladder, with the two-leg matrix as its spine (invariant 9's proof):

- **Per commit** (both legs, always): build at the full warning canon; unit, property, table,
  and tolerance-golden suites; fault-injection suites on the fakes; ASan+UBSan legs; TSan
  stress lane on Linux; remark gates; bench comparisons.
- **Per merge**: the cross-leg **exact** golden comparison (one leg renders, the other
  byte-compares — the determinism contract enforced as a gate); whole-schedule bench trends;
  the conditional-inclusion and symbol audits of §15.3.
- **Per release** (the target-test rungs — "target" meaning real machines of the reference
  class, real devices, both OSes): the **soak** — hours-long real-device runs at the shipped
  period matrix with the always-on monitors as the witness, gating invariant 6's headroom
  floor and producing the session reports the release notes cite; the **buffer sweep**
  regenerating invariant 16's robustness curve; the **loopback latency check** against §7.3's
  computed sum; and the device-matrix smoke (the deployment's supported interface list, hub-
  enumerated). A release that skips a rung says so in its notes — the parent's honesty rule,
  because a skipped rung is a risk decision, not an oversight.

The toolchain-bump ritual closes the chapter (§10.2's law, operationalized): a new clang major
or a new OS baseline re-runs *everything above* plus the full golden-exact matrix before the
hub row moves — the codebase treats its platform the way it treats its code, because the
platform is a dependency that ships inside every binary.

## 15. The enforcement ladder, instantiated

### 15.1 The routes, made concrete

The parent's seven routes, with this domain's machinery on each rung — the child deliverable
chapter 13 of the parent demands, pinned here at mechanism level (tool names and versions:
hub):

| route | this booklet's instantiation |
|---|---|
| `compiler-catchable` | the promoted warning canon, `-Werror`, both legs, one table (§10.2); static assertions on every layout contract (§8.4); the poison headers of §15.2 making banned symbols *compile errors* in RT translation units |
| `analysis-catchable` | clang-tidy + clang static analyzer at pinned check sets with deviation records (§10.8); the RT-TU rule pack: no recursion, no VLA/alloca, no banned-family calls (§8.2, §15.2); prefix and visibility discipline inherited from the parent |
| `build-catchable` | the include audit (core sees core+ports only) and link-time symbol audit (invariant 8, §15.3); the dual-leg matrix (invariant 9); triple/CRT assertions (§10.1); remark gates (invariant 15); map-file audits; conditional-inclusion confinement |
| `host-test-catchable` | the entire ch. 14 host inventory: properties, goldens, contract suites, fault injection, channel torture, sanitizer legs |
| `target-test-catchable` | the release rungs of §14.6: soak with headroom gate, buffer sweep, loopback latency, device matrix — on real reference-class machines, both OSes |
| `runtime-catchable` | go-live asserts (locks, residency, elevation, FTZ — invariants 3, 4, 14); the always-on monitor set (invariant 5); the output sentinel (§12.5); the RT guard in development builds (§15.2); pool generations (§8.3); the heartbeat supervisor (§12.6) |
| `contract-only` | §15.5's register — reviewed by name, on a checklist, per the parent's law |

### 15.2 The RT guard

The development build's centerpiece, and this child's sharpest new enforcement tool. Three
cooperating mechanisms make invariant 1 *mechanical* in development and test builds:

- **The plane tag**: every thread carries its plane (set by the thread adapter at creation); a
  thread-local flag, nothing more.
- **The interposition net**: the allocator family routes through the `allocation-wrapper`
  anyway (§8.3); development builds wrap, additionally, the lock/wait families and the
  known-blocking syscall wrappers of each leg (the linker's wrap facility on both legs' lld —
  same mechanism, one list). Every wrapped entry checks the plane tag: RT plane → trap — log
  the callsite into the flight ring, break if a debugger is attached, fail the test otherwise.
  The overload of §12.2 cannot fire it; only a rule violation can.
- **The poison headers**: RT-class translation units include (via the build system, not
  politeness) a prelude poisoning the banned symbol families outright — allocation, stdio,
  locale, formatting — so the *call cannot compile* in core TUs, catching at the cheapest rung
  what the interposition net would catch at runtime. The two overlap by design: poison catches
  direct spelling at compile time; the net catches what arrives through function pointers and
  third-party objects at run time.

The guard's honest residue: a syscall reached through a leg's opaque library cannot be wrapped
by name if the name is unknown — which is §11.4's review rule (*any call whose implementation
the team cannot name is blocking until proven otherwise*) and the reason the RT plane's
third-party surface is kept near-nil. Ship builds compile the net out; the poison headers stay
(they cost nothing). *(compiler + runtime-catchable, jointly)*

### 15.3 The build-graph gates

The parent's rung-3/rung-4 machinery, with this codebase's specifics: the **include audit**
walks the dependency output asserting `core/` includes only `core/` and `ports/` (and the
compiler port), adapters include ports but never each other across legs, and nothing includes
an adapter save the composition roots — the parent's arrow, mechanized. The **symbol audit**
runs the toolchain's nm over the linked core library asserting the undefined-symbol set is
within the blessed list (the C runtime's math/memory primitives and the port symbols — no OS
import passes; invariant 8's second half). The **map-file audit** (§10.4) asserts section
discipline (RT-hot code and data in their collected sections, guard-page symbols where the
plan says) and feeds the size trends. The **conditional-inclusion audit** inherited from the
parent polices `#ifdef` confinement (§5.5). Every gate is a script in `tools/`, versioned,
run in CI, failing the build — prose made law. *(build-catchable)*

### 15.4 Budgets as fitness functions

The numbers the architecture committed to, collected and trended per the parent's rung 4 —
each with its source and its alarm: go-live time (§4.5; a budget because a user is waiting);
per-block working set versus the cache budget (§8.4; from the schedule compiler's report);
stack watermarks versus stack budgets (§8.2; from the soak); ring depths versus capacities
(invariant 2; high-water counters); cycles-per-frame per kernel and per schedule versus
baseline (§14.5); headroom floor on the reference class (invariant 6; from the soak's
histograms); computed-versus-measured latency remainder (§7.3; from the loopback rung). A
budget checked once is a snapshot; trended with an alarm it is an early-warning system — the
parent's sentence, unimproved because it cannot be.

### 15.5 The contract-only register

What no machine here checks, reviewed by name — the honest list, gathered from this booklet's
own chapters: the boundedness argument for every RT-plane loop (invariant 1's residue); the
written happens-before argument for any new channel shape (§6.6); the wait-free claim of each
channel implementation (§6.2 — the stress suites hunt violations; the *claim* is an argument);
the per-op latency declarations feeding §7.3 (a wrong declaration miscomputes the product's
headline number); the degrade ladder's policy choices and their audibility ordering (§12.2);
the profile corpus's representativeness (§10.5 — a PGO build is an argument about workloads);
the bench protocol's environment honesty (§10.6); the SMI/firmware exposure acknowledged and
not hidden (§2.3, §11.5); the refusals of §11.7 staying refused; and the plane assignment of
every new thread (§2.2 — one line in review, catastrophic when skipped). Each is a checklist
question in the review template, per the parent's rule that the contract-only register is
maintained with the same deliberateness as the rule set — a rule on neither list does not
exist.

---
## 16. The compliance chapter: this child, against the parent's contract

### 16.1 The contract, honored

The parent's chapter 15 binds every specialization by three clauses; this chapter is the child
standing for inspection.

**Nothing weakened.** The parent's twenty-five invariants hold in every program this booklet
governs — including the ones this platform makes cheap (the include-graph law, the effect
boundary) and the ones it makes hard (budgets enforced, not hoped — harder here, and answered
with the monitor-and-soak machinery rather than excuses). Where a parent rule speaks of
hardware this platform abstracts away (flash endurance, MPU regions, ISR vector placement),
§8.6 and §1.4 record the *transposition*, not an exemption: the obligation's owner changed,
the obligation did not.

**Tightened, by name.** Invariant 2 tightens parent invariant 10 (wait-free on the RT side,
not merely lock-free with a policy); invariant 3 tightens parent invariant 11 (claimed *and
resident*, on a paged platform); invariant 13 tightens parent invariant 19 (no formatting at
all on the plane — the structured-event ring is the only voice); invariant 9 tightens the
parent's dual-target cadence (both legs build and test *per commit* — this platform makes the
"cross build" cheap enough to demand always); and the FP regime of §9.6 tightens the parent's
pinned-FP-discipline clause from "pin one" to *this specific pin, both legs, with cross-leg
bit-equality as a standing gate*.

**Pinned, where the parent demands agnosticism of itself.** The parent is target-, compiler-,
and architecture-agnostic *so that* children can pin; this child pins the platform class
(§1.2), the two kernels, C17, and the clang/LLVM family — and honors the spirit of the
agnosticisms it narrows by keeping their machinery: the compiler port survives the single
compiler (§5.6), correctness stays one level above the pinned ISA (§6.6), and the OS is a port
even though exactly two adapters ship (ch. 5). The execution shell — the parent's superloop/
RTOS menu — gains this domain's entry: **the device-paced loop plus control plane on a
general-purpose kernel**, an event-triggered shell whose "scheduler" is the OS and whose
timebase is the device, slotting under the parent's law that the shell is an adapter the core
never knows.

### 16.2 The pin table, filled

The parent's ten rows, answered — what this booklet pins for the family, what it delegates to
the product/deployment, and what lives only in the hub (§16.3):

| parent's row | this child's answer |
|---|---|
| **platform contract** | x86-64 at `x86-64-v3`, 64-bit, little-endian, 64 B lines, 4 KiB pages, invariant TSC, hybrid topologies expected (§1.2); Linux and Windows NT kernels; MMU always present; correctness bound to the C11/C17 memory model, never the ISA (§6.6); widths/alignment asserted statically per §8.4 |
| **toolchain baseline** | clang/LLVM, one major on both legs; Windows = MSYS2 CLANG64 (UCRT, lld); Linux = distro/upstream clang + lld; the flag canon by TU class × config (§10.2); versions, package sets, and check sets: hub rows, dated |
| **execution shell** | the two-plane shell (§2.2, ch. 6): device-paced RT plane (device loop + fixed RT worker pool), control plane, streaming worker, telemetry drain; the channel menu of §6.3 as the only crossings; thread inventory fixed between go-live and teardown (§5.3) |
| **HAL & ports** | the port list of §5.1; shipped adapters: ALSA + WASAPI (audio), POSIX + Win32 (thread/clock/residency); adapter parity table §5.5; excluded-with-reason: ASIO; OPEN: JACK/PipeWire-native, others (§16.4) |
| **memory plan** | the five allocation classes of §8.3 with DT-6; residency at the root (§8.1); per-block working-set budget (§8.4); stack budgets with watermarks (§8.2); pool tables with overflow policies; the plan's sizes derived from the negotiated format and the compiled schedule (§4.5) |
| **failure policy** | dispositions by plane (§12.1); the degrade ladder with fade-to-silence terminal (§12.2); safe state = ramped silence, stream healthy, session preserved (§12.5); xrun taxonomy and recovery (§2.4, §12.3); heartbeat supervision with escalating restart (§12.6); the arithmetic contract inherited from parent §10.7 with UBSan backing (§10.8) |
| **observability plan** | the always-on set of §13.2 (histograms, counters, event ring); the session report as the universal evidence artifact (§13.3); crash capture with ring preservation and relaunch harvest (§13.4); build identity everywhere (invariant 17); replay from the recorded decision path (§13.3) |
| **verification plan** | the offline machine (§14.1–14.2); the numeric suite with two golden regimes and the block-partition property (§14.3); fault-injection and concurrency lanes with TSan on Linux (§14.4); the bench protocol (§10.6) and perf-regression lane (§14.5); the CI matrix and release rungs with the soak as invariant 6's evidence (§14.6) |
| **security posture** | narrow by scope and stated: no elevated privileges beyond the granted scheduling/locking requests; parsers of foreign bytes fuzzed as their definition of done (§10.8); telemetry local-first, upload consented (§13.3); no secrets in trace by construction (nothing secret enters the engine); the full product threat model (plugins, sessions from strangers, network surfaces) is each product's own row, OPEN here |
| **process bindings** | the parent's honesty rules adopted whole: one version hub (§16.3), epistemic tags (measured/documented/assumed — used throughout this text), OPEN surfaced never improvised (§16.4); review checklist = §15.5's register; the toolchain-bump ritual (§14.6) as the standing re-verification trigger |

### 16.3 The version hub, declared

Every dated fact this booklet mentions lives — per the parent's one-hub law — in the family's
version hub, to be established as `audio_manifests/` beside this booklet (mirroring the house's
existing manifest families), and until that package exists, the hub's founding inventory is
recorded here so nothing is improvised in the gap. Hub rows this text has already levied:
toolchain versions per leg (clang 22.1.8 on the reference machine, measured 2026-08-12; the
CLANG64 package set); sanitizer availability per leg (ASan/UBSan both, TSan Linux-only,
libFuzzer both — measured 2026-08-12); BOLT availability (Linux-leg only — measured absent in
CLANG64 2026-08-12); kernel and audio-API baselines per leg (ALSA/WASAPI generations, session-
broker conventions, the audio-group limits convention); per-microarchitecture latency/port
tables and the FMA latency-throughput products of §9.2; large-page mechanisms; the C-state
hold mechanisms of §11.3; the deployment-hardening spellings of §11.6. Re-check triggers, per
the parent's discipline: every toolchain major, every OS/API baseline bump, every new
microarchitecture generation admitted to the reference class — each re-runs §14.6's ritual and
re-dates its rows.

### 16.4 The OPEN register

Decisions this booklet surfaces and deliberately does not make — the grandchildren's table of
contents, each inheriting every invariant here: **plugin hosting** (VST3/CLAP/AU wrapping —
brings foreign code onto the RT plane and therefore the residency/warm-up rites of §8.1 and a
guard story of its own); **the engine/UI process split** (§12.6's strongest restart rung);
**GUI framework and control-surface protocols**; **session/media file formats** (each new
parser joining the fuzz roster); **MIDI and control protocols**; **network audio** (a new
clock domain per §7.2 and a new threat model); **the ASIO adapter** (licensing recorded in
§5.2); **JACK/PipeWire-native adapters**; **multi-device topologies** beyond one-master
(§7.2); **the ARM64 leg** (the memory-model discipline of §6.6 is its down payment; the class
pin of §1.2 is what it renegotiates); **FFT/resampler library selection** (bound already by
the plan-at-init and no-allocation rules — any candidate that cannot plan off-plane
disqualifies itself); and **the per-product SLO** (§2.3) with its shipped period matrix.

## 17. Lineage

### 17.1 How this register works

The conventions are the parent's §16.1, inherited whole: names in `this-face` are element
identifiers resolving in the house catalogs; works are recorded **exactly as the corpus
records them**, UNVERIFIED flags traveling with the ids; editorial claims are marked in place
and gathered in §17.3. Two register mechanics are this child's own. First, the house data
carries **two work registries** — the element catalogs' own works index and the works corpus —
overlapping only partly; ids below resolve in at least one, and the audit script checks both
(the parent's auditor already merged them; this booklet's does the same). Second, because the
catalogs carry **no audio, DSP, SIMD, microarchitecture, OS-scheduler, or benchmarking
elements at all** (verified by sweep during compilation, 2026-08-12), this chapter adds a
third register the parent never needed: §17.3's **external sources** — the domain literature
this booklet leans on that the corpus does not record, named in plain text, never dressed in
`this-face`, each with the claims that rest on it. A future corpus pass may promote them;
until then they are honestly outside the provenance machine.

### 17.2 The works

**Inherited spine.** This booklet stands on the parent booklet (r1.5) and through it on the
whole register of the parent's chapter 16 — the modularity, effect-boundary, error, and
testing canons are cited *there* and re-argued nowhere here. Works below are the ones this
child leans on directly, in its own text.

**Concurrency and the memory model.**

| work | corpus id | standing here |
|---|---|---|
| Herlihy, Shavit, Luchangco & Spear, *The Art of Multiprocessor Programming*, 2nd ed. (2020) | `herlihyshavit` | verified — the wait-free/lock-free progress taxonomy §6.2 builds on |
| McKenney (ed.), *Is Parallel Programming Hard…* (living) | `perfbook` | verified — false sharing, RCU, per-CPU reasoning (§6.3, §8.4) |
| Linux kernel locking/RCU/memory-barrier documentation (living) | `kernelsyncdoc` | verified — the barrier-pairing discipline behind §6.6 |
| Preshing, lock-free and memory-ordering series (living) | `preshing` | verified — the acquire/release pedagogy §6.6 assigns as review canon |
| Sha, Rajkumar & Lehoczky, *Priority Inheritance Protocols* (1990) | `sharajkumar90` | verified — the inversion-protocol lineage §6.2 measures this platform against |
| Drepper, *Futexes Are Tricky* (2011) | `drepperfutex` | verified — the parking mechanics under §6.5's hybrid join |
| Buschmann et al., *POSA Vol. 2* | `posa2` | **UNVERIFIED** (carried from the parent's register) — the naming source of `half-sync-half-async` (§6.1); the element stands, the record awaits re-verification |

**Parallel execution.**

| work | corpus id | standing here |
|---|---|---|
| Mattson, Sanders & Massingill, *Patterns for Parallel Programming* (2004) | `mattsonppp` | verified — the pattern language §6.5 compresses |
| McCool, Robison & Reinders, *Structured Parallel Programming* (2012) | `mccoolspp` | verified — same duty |
| Blumofe & Leiserson, *Scheduling Multithreaded Computations by Work Stealing* (1999) | `blumofeleiserson` | verified — cited exactly where §6.5 declines its subject |

**Mechanical sympathy.**

| work | corpus id | standing here |
|---|---|---|
| Hennessy & Patterson, *Computer Architecture: A Quantitative Approach*, 6th ed. (2017) | `hennessypatterson` | verified — the hazard taxonomy, latency/throughput vocabulary, and speculation model of ch. 9 |
| Drepper, *What Every Programmer Should Know About Memory* (2007) | `dreppermem` | **UNVERIFIED** (the corpus's own flag, inherited from the parent's register) — the standing tutorial behind ch. 8's hierarchy reasoning; also the named-in source of `false-sharing-avoidance-via-cache-line-padding` |
| Thompson et al., *Disruptor* technical paper (2011); Fowler, *The LMAX Architecture* (2011) | `lmaxdisruptor` · `lmaxfowler` | verified — the mechanical-sympathy lineage named at ch. 9's head; the cached-index batching of §6.3(b) |

**Platform and toolchain.**

| work | corpus id | standing here |
|---|---|---|
| Kerrisk, *The Linux Programming Interface* (2010) | `kerrisktlpi` | verified — the Linux API semantics behind §8.1 and §11.1 |
| Drepper, *How To Write Shared Libraries* (2011) | `drepperlibs` | verified — PLT/binding mechanics (§8.1) and visibility discipline (§10.4) |
| Levine, *Linkers and Loaders* (1999) | `levine` | verified — the linkage mechanics of §10.4 |
| LLVM: ThinLTO documentation; Johnson, Amini & Li's paper | `thinlto` · `thinltoblog` | verified — §10.3's mechanism |
| Clang tool documentation: user's manual, clang-tidy, clang-format | `clangdocs` · `clangtidy` · `clangformat` | verified — the analysis-route instantiation of §10.8 |
| LLD, the LLVM linker (living) | `lld` | verified — §10.4's one-linker pin |
| Godbolt, *What Has My Compiler Done for Me Lately?* (2017) | `godbolt` | verified — the look-at-the-output discipline behind §10.5's remark gates |
| Serebryany et al., *AddressSanitizer* (2012) | `asan` | verified — §10.8's mechanism paper |

**Real-time scheduling canon** — inherited from the parent's register and cited here only as
the backdrop §2.3 measures the platform against: `liulayland`, `buttazzo`, `kopetz` (all
verified), with the response-time-analysis lineage recorded in the netsim corpus's scheduling
keystones as the parent's chapter 16 describes. This booklet deliberately makes no
schedulability claim those works would license: the non-real-time kernel breaks their
admission-control premise, which is exactly §2.3's honesty.

### 17.3 The registers: editorial, and external

**Editorial** — composed here from cataloged parts, or stated here without element backing,
per the parent's §16.3 discipline:

- **The three-slot latest-wins mailbox** (§6.3(d)): the catalogs carry `double-buffer` and
  `ping-pong-buffer`; the third-slot free-running form and its contract are stated by this
  booklet.
- **The write-target/consume-and-ramp parameter protocol** (§4.3, §6.3(a)), the **block
  quantum** rule and its invariant 20, and the **graph-compiler-as-register-allocator**
  framing of §4.2 — compositions over `defunctionalization`, `bytecode-virtual-machine`, and
  the channel elements.
- **The drift estimator and pair-stream discipline** (§7.1–7.2), the **ramp-in/fade-out**
  practices (§12.3, §12.5), and the **output sentinel** composition (§12.5).
- **The FTZ/DAZ regime and denormal hygiene** (§9.6), the **4 KiB-stride staggering** (§8.4),
  the **bench protocol** (§10.6), the **RT guard** (§15.2), and the **autopsy composition**
  (§11.5) — mechanisms whose parts are external or platform facts and whose assembly is this
  booklet's.
- **The flight-recorder composition** (§13.1–13.4) remains the parent's editorial synthesis,
  inherited and extended (session report, replay workflow).
- **Catalog gaps this booklet worked around, for the record** (sweep of 2026-08-12): no SIMD,
  ILP, branch-prediction, or microarchitecture elements; no audio/DSP elements or works; no
  triple-buffer, wait-free, composition-root, fault-injection, flight-recorder, or
  benchmarking-methodology entries; no WCET, NUMA, TLB, or huge-page vocabulary; no Agner
  Fog, Butenhof, or systems-performance works. Each gap is a candidate for a future corpus
  pass, not evidence against the practices.

**External** — domain sources outside the corpus entirely; plain names, never `this-face`;
verify before load-bearing use, and promote into the corpus before a future revision leans
harder:

- **ISO/IEC 9899 (C17) and its memory model** — the correctness substrate of §6.6; cited
  through the standard itself and the catalogs' atomics elements.
- **The ALSA project's API documentation** — §5.2's Linux adapter facts (period/ring model,
  recovery states, transfer modes).
- **Microsoft's WASAPI, MMCSS, and thread-QoS documentation** — §5.2's and §11.1–11.3's
  Windows adapter facts (shared/exclusive modes, event-driven pacing, Pro Audio class,
  power-throttling controls).
- **The MSYS2 project's environment documentation** — §10.1's CLANG64 anatomy (UCRT linkage,
  package taxonomy); the component inventory itself was *measured* on the reference machine
  2026-08-12 and dated in the hub.
- **LLVM project documentation beyond the corpus-carried pages** — BOLT, the PGO workflow's
  current flag surfaces, llvm-mca — §10.5, §9's oracles.
- **Intel's Software Developer's Manual and Optimization Reference Manual** (and AMD's
  equivalents) — the MXCSR FTZ/DAZ mechanics (§9.6), denormal-assist costs, 4 KiB-aliasing
  and store-forwarding behavior (§8.4), per-generation port maps (§9.3).
- **Agner Fog's optimization manuals and instruction tables** — the field's standing
  microarchitecture reference, used as the cross-check for §9's cost claims; absent from the
  corpus (registered above).
- **Ross Bencina, "Real-time audio programming 101: time waits for nothing"** — the domain's
  canonical statement of the no-locks/no-allocation/no-blocking discipline this booklet
  systematizes; named as intellectual lineage for ch. 6's iron rule.
- **The real-time Linux and desktop-audio infrastructure documentation** (rtkit, the
  audio-group limits convention, PipeWire/JACK deployment guides) — §11.1's and §11.6's
  deployment shapes.

### 17.4 Colophon

*Real-Time Audio on the Unconstrained Machine — architecture, design, and mechanical sympathy
for PC-class real-time audio in C*, revision r1.0, compiled 2026-08-12, as the first child of
*Architecture and Design of Complex Embedded C Programs* r1.5, against: the SWE element
catalogs v1.0 (709 + 374 elements; both work registries), element bridge v1.1, the parent
booklet's own register and auditor, the house manifest families' conventions
(python-agent-ground 2026.08.08), and measurements taken on the reference machine (12th-gen
hybrid x86-64, Windows 11 Pro; MSYS2 CLANG64 at clang 22.1.8) dated 2026-08-12 throughout.
Element identifiers resolve in `SWE/explorer/data/elements.json`; work records in that file's
works registry and in `SWE/explorer/data/corpus.json`; the booklet's own audit gate is
`_audio_booklet_work/audit.py` — element ids, work ids and their verification stances, every
internal and parent-directed cross-reference, and the structural counts are machine-checked
before any revision is sealed. Version-dependent facts live in the version hub this booklet
declares (§16.3) and nowhere else. Verify before trusting; route before relying; measure
before optimizing — and when a rule here meets a situation it does not fit, reason past it,
and say so.

**Revision history.**

- **r1.0** (2026-08-12) — initial edition: seventeen chapters, twenty invariants, seven
  decision trees, the parent's pin table answered in full.
