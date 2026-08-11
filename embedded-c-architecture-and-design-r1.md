# Architecture and Design of Complex Embedded C Programs

**The parent booklet — r1**

Principles for building embedded C systems that are maximally modular, maintainable, observable,
testable, and decoupled — stated once, target-agnostic, architecture-agnostic, compiler-agnostic,
with or without memory protection.

---

## What this booklet is

This is the **parent of the specializations**. It states the principles that hold for any complex
embedded C program — a motor controller, a battery-management system, a radio stack, an instrument,
a vehicle ECU — regardless of which core executes it, which vendor sold the silicon, which compiler
translated it, and whether a memory management unit exists to catch anyone who strays. Everything
that depends on a *particular* target, toolchain, RTOS, or standard baseline is deliberately absent
and explicitly delegated: chapter 15 defines the contract a specialization must fulfil, and the
closing register lists every decision this booklet surfaces but refuses to make.

It is **grounding, not a rulebook**. Cite a principle when it materially shapes a decision; reason
past it when the situation genuinely differs — and say which you are doing. The architect reasons
from first principles; the booklet exists to make that reasoning legible, to check priors against
accumulated practice, and to surface the tradeoffs that are easy to forget at two in the morning
with a logic analyzer on the bench.

It carries **no version-dependent facts, on purpose**. No compiler flags, no rule codes, no
standard-edition numbers, no vendor names as normative content. Facts of that kind decay; when a
specialization needs one, it pins it in its own version hub and dates it. What this file carries
instead is the part that does not decay: the shape of the problem, the named moves, their costs,
and the obligation to enforce.

Its intellectual footing is the house corpus: the software-engineering element catalogs (709 design
elements, 374 architecture elements, and the typed relations between them), the process corpus, and
the manifest families that already instantiate the same discipline for Python and for the browser.
Catalog element identifiers appear in `this-face`; C keywords, code, and file names unavoidably
share that face, and chapter 16 resolves any name in doubt. The works behind the identifiers are
recorded in chapter 16 exactly as the corpus records them, including which records the corpus could
not verify. Where this booklet makes a judgment the corpus does not source, it is marked *editorial*.

## How to read it

Part I establishes what an embedded program actually is and derives the five goals from one
discipline. Parts II–VI develop the discipline by subject: structure, behavior, memory, failure,
verification. Part VII handles change in a fielded system, then binds the family together: what a
specialization must pin, and where every name used here comes from. A reader with one hour reads chapter 1, the invariants at the end of
Part I, and chapter 15. A reader designing a system reads it whole, once, and then argues with it.

---

# Part I — The Ground

## 1. The machine you are actually programming

An embedded program is a machine that turns events into effects under budgets.

Every clause of that sentence does work. *Events*: interrupts, arriving frames, expired timers,
edges on pins, conversions completing — the program does not run so much as it is provoked.
*Effects*: the point of the program is to change the world outside it — energize a coil, shape a
waveform, persist a record, transmit a frame. A desktop program's side effects are incidental to a
computation; an embedded program's side effects **are the product**. *Budgets*: cycles, bytes of
RAM and flash, microamps, and — the one that separates this domain from most others — deadlines.
An answer that arrives late is not a slow answer; in a control loop it is a wrong answer.

Four consequences follow, and the whole booklet is downstream of them.

**Effects cannot be avoided, so they must be placed.** A design culture built on minimizing side
effects has nothing to say to a program whose purpose is side effects. The productive move is not
purity but *placement*: every effect gets exactly one home, every home has a name, and the logic
that decides an effect is separated from the mechanism that performs it. Chapter 4 builds this
boundary; it is the single highest-leverage structure in the book.

**The program is only partially observable.** There is no attached terminal, often no debugger in
the field, sometimes no way to reach the device at all after it ships. Whatever visibility exists
is visibility that was *designed in* — a trace buffer, a persisted crash record, a reset-cause
autopsy — and it competes for the same bytes and cycles as the product function. Observability is
therefore an architecture chapter (11), not an operations afterthought.

**The program outlives its authors and its hardware.** Field lifetimes of ten or twenty years are
ordinary. The silicon will be discontinued and substituted; the compiler will be upgraded under
qualification pressure; the team will turn over entirely. Maintainability in this domain means the
program survives the replacement of *everything around it* — which is why target-agnosticism is not
a portability nicety but a survival trait, and why it is treated structurally (chapter 5) rather
than as a porting guide.

**Failure is a normal operating mode.** Sensors glitch, supplies brown out, cosmic rays flip bits,
watchdogs bite. A program that treats failure as exceptional has no plan for its most predictable
input. Failure handling gets the same architectural standing as the happy path (chapter 10), and
recovery is designed as a ladder that ends, legitimately, in reset.

### What the agnosticisms mean, operationally

The booklet's scope line — target-agnostic, architecture-agnostic, compiler-agnostic, MMU or not —
is not a disclaimer. Each clause is a design obligation this booklet discharges structurally:

- **Target-agnostic** means *the target is a port*: every register, peripheral, and board fact sits
  behind an interface the application owns, so the application text contains no knowledge of which
  silicon runs it. Chapter 5 gives the layering; the test suite plugging in where the hardware was
  is the proof it worked.
- **Architecture-agnostic** means the program's correctness argument never rests on a particular
  core's width, endianness, alignment tolerance, or memory ordering. Where such properties matter
  they are named as explicit assumptions, checked where checkable (a static assertion on a layout,
  a startup self-test on a behavior), and confined to the adapter layer.
- **Compiler-agnostic** means the program is written against the ISO C contract, and every use of
  anything beyond it — extensions, intrinsics, attributes, pragmas, inline assembly — is quarantined
  behind the same kind of named adapter surface as the hardware. The compiler is a port too
  (chapter 5). What the standard leaves undefined the program does not do; what it leaves
  implementation-defined the program either avoids or names as a pinned, checked assumption.
- **With or without an MMU** means memory protection is treated as *depth of enforcement, never as
  structure*. Ownership rules, static allocation, and boundary discipline must make the program
  correct on a flat address space where any pointer can reach anything; an MMU or MPU, where
  present, is then configured to *catch violations earlier* — the same boundaries, enforced harder.
  A design that is only safe because hardware traps the mistake is not a design; it is a trap
  handler with a program attached. Chapter 9 carries this through memory; chapter 13 places
  protection hardware on the enforcement ladder alongside the other checkers.

One more agnosticism is implied and worth stating: **RTOS or not is a shell decision.** Superloop,
cyclic executive, time-triggered scheduler, preemptive kernel — these are execution shells around
the same event-driven, run-to-completion core, and chapter 6 is written so that the core's design
does not change when the shell does.

## 2. First principles

### 2.1 Information hiding is the root

Parnas's criterion (1972) remains the sharpest single sentence in the field: decompose the system
so that each module hides a decision likely to change, behind an interface that would survive the
change. Not steps of processing — *secrets*. In embedded work the secrets are concrete and
enumerable: which silicon, which pin map, which sensor, which protocol version, which scheduling
policy, which memory layout, which compiler. Each of those will change across the fielded life;
each therefore names a module boundary. The element catalogs carry the operational form as the
`encapsulate` tactic — other elements depend only on the interface — and the whole of Part II is
the C instantiation of it.

The test for a proposed decomposition is not elegance but **change scenarios**: list the likely
changes (new board rev, second sensor vendor, compiler upgrade, feature variant), and count how
many modules each change touches. One likely change touching many modules means responsibilities
are misallocated; a module no scenario touches is dead weight. The corpus states both halves as the
`redistribute-responsibilities` tactic's operational test, and it is runnable against a repository
history, not just against intuition.

### 2.2 A contract is a decision that has been frozen

An interface is the set of decisions a module has frozen; everything else is implementation and may
change. Contracts in this booklet always have five parts: **inputs, outputs, invariants, error
modes, and ordering/timing constraints** — the last given equal rank because in this domain *when*
is part of *what*. "Returns the filtered sample" is not a contract; "returns the filtered sample,
computed from the last N samples, within the same tick in which the conversion completed, or the
sentinel with a fault code if saturation persisted" is one. Error modes are part of the interface:
a function that can fail three ways and declares none has already failed, in the caller's hands, at
a time of the field's choosing.

### 2.3 The enforcement thesis

The house thesis, which this booklet inherits and instantiates:

> A set of principles is a good start. A named pattern vocabulary is very nice. A design document
> is also nice. **A way of enforcing all of it is the point** — advice that is not mechanically
> enforced decays to zero.

A dependency rule stated in prose is a preference, and preferences lose to the next deadline. A
boundary is real when a machine refuses its violation. Accordingly, every rule in this booklet
routes to one of seven enforcement routes, or admits that nothing mechanical catches it:

| route | meaning |
|---|---|
| `compiler-catchable` | a diagnostic the build promotes to a hard error, or a property the type system refuses (an incomplete type cannot be dereferenced) |
| `analysis-catchable` | a static-analysis rule class; the specialization pins the tool, version, and rule set |
| `build-catchable` | a structural fact of the build the pipeline checks: include-graph shape, link-time symbol visibility, image size, section placement |
| `host-test-catchable` | a test that runs in the host build, per commit |
| `target-test-catchable` | a test that runs on the target or hardware-in-the-loop rig, at the child's pinned cadence per rung — smoke per merge through HIL per release (§12.5) |
| `runtime-catchable` | a mechanism in the shipped program that turns a silent fault into a detected one: assertion, sanity check, CRC, canary, watermark, watchdog, MPU trap |
| `contract-only` | nothing mechanical catches it — an honest admission that this rule lives in review, and must be reviewed for deliberately |

The last route is load-bearing. A substantial fraction of what matters in design has no mechanical
enforcer; the discipline is to *say so* rather than imply coverage that does not exist. And the
routes are ordered by preference: a fault caught by the compiler costs seconds; the same fault
caught by the watchdog costs a field return. Chapter 13 is the ladder in full.

### 2.4 The five goals are one discipline

The booklet's commission names five maximals — modularity, maintainability, observability,
testability, decoupling. They are not five programs of work. Each is the same underlying property
photographed from a different side: **decisions expressed as contracts at named boundaries, with
every contract enforced by a machine somewhere.**

- **Modularity** is having the boundaries: units with single stated responsibilities, interfaces
  that hide one secret each, dependencies that point one way.
- **Decoupling** is what the boundaries deny: the user asked for decoupling *of components, of
  targets, and of effects from logic*, and Part II dedicates one chapter to each — components
  (chapter 3), effects-from-logic (chapter 4), targets (chapter 5).
- **Testability** is the boundaries exercised by a machine: a unit is testable exactly when it can
  be instantiated against doubles at its declared seams — a design property, not a test-tooling
  property (chapter 12).
- **Observability** is the boundaries reporting: what crossed, when, in what state — designed with
  the same seriousness as the product function, because the observer arrives after the failure
  (chapter 11). The corpus files control-and-observe tactics under *testability*; this booklet
  adopts the identification: **testability and observability are one family, differing only in
  whether the observer is a test or an engineer with a field return on the bench.**
- **Maintainability** is the boundaries surviving time: change scenarios landing inside single
  modules, contracts outliving their implementations, and the enforcement machinery keeping all of
  it true after the original authors are gone.

Maximizing them is therefore not balancing five dials. It is one investment — boundary discipline
plus enforcement — amortized five ways. Where they *do* trade off against something, the price is
named in the corpus and repeated here: indirection and pass-through cost at every intermediary, RAM
and cycles for every recorder, mechanism paid up front for every deferred binding. Those are real
prices, and this booklet's position is that in a system built to outlive its authors they are the
cheapest insurance on the invoice — but they are stated, every time, so a hard-real-time inner loop
can decline them *by name* rather than by erosion.

## The invariants — Part I distilled, the rest of the book in one page

Twenty-five statements that hold for every system this booklet governs. Each is developed in a
chapter; each carries its enforcement route inline. A reader who adopts nothing else should adopt
these — and route them.

**Structure** *(chapters 3–5)*

1. **One module, one secret, one header.** The header is the interface; everything not declared in
   it is private, spelled `static` or hidden behind an incomplete type. A name that leaks is a
   boundary lost. *(compiler + build + analysis-catchable)*
2. **Hide state behind opaque types wherever the interface allows;** where it cannot, hide it
   behind functions. C's incomplete type is the compiler's own enforcement of representation
   hiding — the one mechanism that hides a shared name's contents while its handle stays
   public. Spend it. *(compiler-catchable)*
3. **The include graph is the architecture.** It is acyclic, levelized, and machine-checked; a new
   cycle is a broken build, not a code smell. *(build-catchable)*
4. **Dependencies point from policy to mechanism.** The core never includes an adapter or vendor
   header; adapters include the core's port headers. One direction, no exceptions without an ADR.
   *(build-catchable)*
5. **Every variation point has a named binding time** — compile, link, initialization, or run time —
   and conditional-compilation variation is confined to dedicated adaptation files, never scattered
   through logic. *(analysis + contract-only)*

**Effects** *(chapters 4–6)*

6. **Logic decides; the shell does.** Decision code returns effect *values*; only the shell
   executes them. A function that both computes and touches a register can be tested for neither.
   *(host-test-catchable — the core builds and runs off-target)*
7. **The target is a port.** Every register, peripheral, and board fact sits behind an interface
   the application owns; the test double is just another target. *(build-catchable)*
8. **Time is injected.** No core code reads a clock, waits, or sleeps; ticks, timestamps, and
   deadlines arrive as data through a port. *(build + host-test-catchable)*
9. **ISRs are couriers, not workers:** capture, timestamp, enqueue, return. Decisions happen in
   task context, under run-to-completion semantics. *(analysis-catchable + contract-only)*
10. **Every ISR↔task exchange crosses one named channel** with a stated overflow policy, and every
    queue in the system is bounded. An unbounded queue is a deferred out-of-memory failure; an
    unstated overflow policy is data loss with no witness. *(runtime-catchable — overflow counters)*

**Memory** *(chapter 9)*

11. **Memory is claimed at initialization.** Static allocation first, pools for populations, the
    general heap only behind a recorded decision — and after init, allocation failure from
    demand the design controls is a design error. Exhaustion of a pool fed by *external*
    arrivals is invariant 10 wearing its memory face: a stated shed policy and a counted drop.
    *(build + analysis-catchable)*
12. **Every object has one owner.** Every buffer that crosses a boundary — DMA included — states
    who may write it, who frees or reuses it, and when. *(contract-only, stated in the header)*
13. **Budgets are enforced, not hoped:** stack bounded by analysis where the call graph permits
    — trapped by guard and trended by watermark where it does not — RAM and flash by link-map
    gate, queue depths by counter, deadlines by measurement where hard. A budget nothing
    measures is a wish. *(build + runtime-catchable)*

**Failure** *(chapter 10)*

14. **Errors are values in the signature.** Every fallible call's result is checked or explicitly,
    visibly discarded. *(analysis-catchable)*
15. **Detect, decide, act — split.** Detect everywhere, decide per the contract, act only at the
    designated recovery owner. Error-handling code scattered at every call site is the smell of a
    missing owner. *(contract-only)*
16. **Two kinds of wrong, two mechanisms.** Expected conditions get error paths and tests;
    contract violations get assertions — loud stop in development, safe-state plus evidence in the
    field. Never validate external input with an assertion. *(analysis + runtime-catchable)*
17. **Define the safe state before you need it,** and recover on a ladder — retry, reset the unit,
    restart the task, reboot — with the watchdog as the ladder's enforcement of last resort, kicked
    only by proven progress, never from a timer that proves only that timers work.
    *(runtime-catchable)*
18. **Every reset tells its story.** Reset cause, a persisted crash record naming the firmware
    that wrote it, and the trace tail
    survive into the next boot. A failure that leaves no evidence will be fixed by guesswork,
    twice. *(runtime-catchable)*

**Observability** *(chapter 11)*

19. **Trace is a port with a budget.** Structured events with identifiers — not format strings —
    timestamped from the injected clock, in a bounded buffer whose drops are counted, never silent.
    *(build + runtime-catchable)*
20. **State machines log transitions; boundaries log crossings.** "How did we get here?" is
    answered by the recorder, not by the debugger you will not have. *(host-test-catchable — the
    trace is asserted in tests, which keeps it honest)*
21. **The maintenance surface is separate from the functional surface** — and in C it is genuinely
    removable, so the shipping decision (in or out) is explicit, recorded, and tested in the
    configuration that ships. *(build-catchable)*

**Verification** *(chapters 12–13)*

22. **Two targets from day one.** The host build is a first-class product: all
    hardware-independent logic runs there per commit; the cross build proves the same contracts on
    the metal at release cadence. *(host + target-test-catchable)*
23. **Name the seam mechanism.** Link substitution, function pointer, include-path override —
    "it's testable" without a named seam is a claim, not a property. *(contract-only, reviewable)*
24. **Fault injection is designed in at the ports,** and error paths are tested with the same
    seriousness as success paths — in this domain the error paths are the product.
    *(host-test-catchable)*

**Security** *(sections 5.5, 11.5, and chapter 14)*

25. **Every surface that can change the device authenticates its counterpart** — update,
    maintenance, configuration — rollback is protected, secrets never enter the trace, and
    secret lifetimes end in enforced zeroization. The threat model itself belongs to the
    specialization; these attachment points do not. *(host/target-test for the authentication
    paths; analysis-catchable + contract-only for zeroization)*

And over all twenty-five, the meta-invariant of chapter 13: **a rule with no enforcer is a
preference.** Route it, or label it `contract-only` and review for it on purpose.

---

# Part II — Structure: the three decouplings

The commission asks for decoupling three times over: of components from components, of effects from
logic, of programs from targets. These are the three chapters of Part II, and they are ordered by
dependency: component boundaries (3) are the mechanism, the effect boundary (4) is the most
important single use of that mechanism, and target independence (5) is what falls out when both are
held.

## 3. Modules in a language without modules

C has no module system. It has translation units, headers, external linkage, and a preprocessor —
and from these a module system is *built, by discipline*. That sentence, which the corpus records
as the problem statement of `organizing-files-in-modular-c-programs`, sets the tone for the whole
chapter: every property that a language with modules grants for free is, in C, a construction —
which means it is also a choice, and a thing that erodes unless enforced.

### 3.1 The module: one secret, one header, one implementation

The unit of design is the **module**: one `.h` file that *is* the contract, one (or more) `.c`
file(s) that are nobody's business. The corpus's `self-contained-component` gives the shape: a
component exposes exactly one public surface, and its dependencies point only toward more
fundamental components. Concretely:

- The header contains the minimum that callers need: the exported types (opaque where possible),
  the function declarations, the constants of the contract, and the contract itself in prose —
  invariants, error modes, ownership statements, timing constraints (§2.2).
- Everything else is private: file-scope `static` functions and data. Internal linkage is the
  module's `private` keyword; a definition with external linkage that appears in no header is a
  defect the compiler's require-a-declaration diagnostic class or an analysis rule can find —
  the linker never sees headers. *(compiler/analysis-catchable)*
- A module that needs several implementation files keeps *one* public header and moves shared
  internals to a private header in the implementation's own directory, never on the public include
  path. The include path expresses the intent; the quoted-include form can path around it, so
  the enforcement is §3.3's audit of resolved dependencies plus an analysis rule forbidding
  path-traversing includes and out-of-header `extern` declarations. *(build + analysis-catchable)*

Two module shapes exist for state, and the corpus prices them rather than banning either
(Preschern, *Fluent C*): the `stateless-software-module` — no state between calls, every resource
passed in, reentrant by construction — and the `software-module-with-global-state` — one
file-scope state blob behind the function interface, trading reentrancy for a single shared
context. The stateless shape is the default because it is the testable and concurrency-safe one;
the stateful shape is legitimate for genuine singletons (there is one power controller), and when
chosen it is *declared*: an explicit `init`/`deinit` pair, a stated owner task, and a stated scope.
What is banned is not module state but **implicit** module state — the accidental `static` that
makes call order matter and tests interfere. A third shape is the instance module: the state struct
is the first parameter of every function (`motor_step(motor_t *m, ...)`), which is the stateless
shape applied to N instances and the natural C spelling of an object. Prefer it the moment a
"singleton" grows a twin.

### 3.2 The opaque type: the one enforcement C gives away

Internal linkage hides *names*; C grants exactly one mechanism that hides a shared name's
*representation*, and it is excellent: the
**incomplete type**. Declare `typedef struct motor motor_t;` in the header, define `struct motor`
only in the implementation, and hand out pointers. Callers can hold, pass, and store the handle;
they *cannot* dereference it, size it, or copy it — not by convention but because the compiler
refuses. The corpus records `opaque-pointer` with exactly this note: C has no access control, but
the incomplete type makes information hiding compiler-enforced. *(compiler-catchable)*

Its cost is real and must be stated: an opaque type cannot be allocated by the caller (its size is
unknown), which collides with the static-allocation discipline of chapter 9. The domain has three
honest resolutions, in order of preference, each with its price named:

1. **The module owns a static pool of its own instances**, and the constructor hands out
   handles from it (`motor_t *motor_claim(void)`). Priced: instance count and placement migrate
   from the caller into the module's configuration, and the pool's whole footprint is paid by
   every image that links it.
2. **The header exports an opaque *storage* type** of pinned size and alignment. Its hazard has
   a name: the obvious implementation — caller-declared storage, cast to the real struct inside
   the module — violates ISO C's effective-type rules, exactly the undefined behavior §5.2
   forbids. The module therefore accesses the storage only by `memcpy` to and from its own
   struct, or completes the type through a union in a restricted-visibility header, or records
   a pinned toolchain aliasing guarantee in the compiler port as a named extension reliance.
   The size-and-alignment static assertion remains necessary; it is not the proof.
3. **The struct is published but marked non-contract**, its fields prefixed as private, with an
   analysis rule forbidding access outside the owning module — for where neither stronger form
   fits.

The first keeps full enforcement and is the default; the last is the weakest and says so.
*(compiler → analysis, weakening in steps, each named)*

### 3.3 The include graph is the architecture

In C the dependency structure is not a diagram; it is the **include graph**, and it is machine
readable. What Lakos built for large-scale C++ transposes directly and is the corpus's
`limit-structural-complexity` tactic wearing physical-design clothes: **levelization**. Every
module has a level — level 0 depends on nothing but the language and the pinned platform contract;
level N includes only headers of level < N. Cycles are forbidden absolutely: a cyclic include pair
is one module wearing two names, and it defeats independent testing, independent understanding, and
independent replacement in one stroke.

This is the five-rung enforcement ladder of the house, instantiated for C:

1. **Encapsulate** — the boundary exists as a header; nothing yet stops a caller reaching past it.
2. **Explicit interface** — the header is honest: opaque types, no leaked internals; the compiler
   now refuses dereference of secrets. *(compiler-catchable)*
3. **Separated interface** — the *port* header lives with the consumer, not the provider: the
   application owns `spi_port.h`; the vendor adapter implements it and includes it. The dependency
   arrow reverses at the file-system level (§4.4). *(build-catchable)*
4. **Restrict dependencies** — the include graph itself is checked: a small script or the build
   system's dependency output asserts the layer rules ("core includes no adapter header", "no
   module includes a vendor header except adapters") and fails the build on violation. In prose
   this rule is a preference; as a build gate it is a boundary. *(build-catchable)*
5. **Contract as build input** — the strongest rung: interface definitions that *generate* code —
   register descriptions, message schemas, configuration tables — so that violating the contract
   fails code generation before compilation begins (§3.6).

The include path is part of the mechanism, not a convenience: what a module *may* see is expressed
by what is *on its path*. Public headers live in an exported include directory; private headers do
not. A private header off the path must be *reached for* — and the reach, a path-traversing
include or an out-of-header `extern`, is what the rung-4 audit and the analysis rules refuse.
*(build + analysis-catchable)*

Two graphs, not one: the include graph is the *compile-time* dependency truth, and the corpus is
explicit that `restrict-dependencies` (who may depend) and `restrict-communication-paths` (who may
talk at run time) are different tactics. In C the second graph is the call-and-callback structure —
who holds whose function pointers, who posts to whose queue — and it routinely diverges from the
first the moment dependency inversion is used. State both: the layer rules govern includes; the
runtime topology (chapter 6's active objects and channels) governs conversation.

### 3.4 Coupling is three decisions, not one dial

"Reduce coupling" is unactionable; the corpus supplies three named moves with three costs, recorded
as sourced alternatives of one another:

- **Encapsulate** — hide the internals behind an interface. Cost: the interface is now a thing to
  keep honest, and whatever it fails to expose becomes a reason to reach past it.
- **Restrict dependencies** — forbid the edge outright. Cost: a rule to maintain, and the
  legitimate future need it will refuse until amended.
- **Use an intermediary** — route the dependency through a queue, a dispatcher, a callback
  registry, so neither side names the other. Cost, stated in the source and doubly true here:
  per-event processing the direct call did not pay, and control flow that no longer reads in one
  place — in a hard loop, that price is measured in microseconds and must be measured.

An agent told "pick a vertex of the triangle, and pay its price knowingly" can act; an agent told
"lower coupling is better" cannot. And the modifiability/performance axis this exposes is *the*
canonical embedded tradeoff: an intermediary bought for decoupling is paid for in latency and
jitter. The rule of this booklet is not "never pay it" but "price it": the decision that turns a
function call into a queued message is an architecture decision, recorded with its measured cost.

### 3.5 Naming is ownership

With no namespaces, the global symbol space is a commons, and commons degrade. The discipline:
every module owns a prefix (`motor_`, `log_`, `hal_spi_`); every external symbol and public macro
carries its module's prefix; unprefixed external names are a defect. This is simultaneously a
collision defense, a readability device (call sites name their module), and — because prefixes are
mechanically checkable — a cheap analysis gate. *(analysis-catchable)* The linker's visibility is
part of the same commons: everything not deliberately exported is `static`; where the toolchain
family supports it, the specialization pins a symbol-visibility or link-time check that the
module's actual exports equal its header's declarations. *(build-catchable, pinned by the child)*

### 3.6 Contracts that are build inputs

The top rung of the ladder deserves its own note because embedded work is unusually rich in
contracts that *should* be generated rather than written: register maps, bitfield layouts, message
and frame schemas, calibration and configuration tables, state-machine tables. Hand-maintained
twins of an external truth (a datasheet, an ICD, a protocol spec) drift; a generator makes the
external truth the single source and turns drift into a build failure. The corpus pairs the tactic
(`interface-definition-language`) with its survival rule, `generation-gap`: generated files are
build outputs, never edited — hand-written code subclasses or wraps them in a sibling module, so
regeneration never eats a human's work. Where a generator is too much machinery, the honest C
fallback is the `x-macro`: one table, expanded several ways — enum, string table, dispatch table —
so the single source of truth lives in the repository itself. It is ugly and it is one truth —
though only the table is greppable: token-pasted products never appear as text anywhere in the
repository, so the discipline is pasted names predictable from the table row. The corpus
records the x-macro as a coding-level DRY mechanism with no architectural pretensions, which is
exactly how to use it. *(build-catchable)*

### 3.7 What this chapter refuses

Boundaries drawn by technology rather than responsibility — a `utils` module, a `helpers` module, a
`common` module — accumulate unrelated secrets and couple everyone to everything; the change
scenarios of §2.1 will indict them, and the levelization check makes them visible as the
high-fan-in low-cohesion nodes they are. And boundaries *asserted but not checked* are refused by
the whole chapter: `__attribute__`-guarded intentions, comment-declared privacy, "please don't
include this" headers on the public path. If the build accepts it, it will happen; move the rule
into the build.

### 3.8 The boundary, documented

Three artifacts describe the structure this chapter builds, and they are three *different*
artifacts because they answer three different questions — the corpus carries the partition as
the view types of *Documenting Software Architectures* (`module-view`,
`component-and-connector-view`, `allocation-view`), governed by the standard's rule that each
view follows the conventions of a single viewpoint:

- The **module view** answers "what may depend on what": it is the layer contract of §3.3 —
  hand-written, machine-checked — plus a picture *generated* from the include graph. The
  contract is the source of truth; the picture is a rendering. A diagram is not a constraint:
  generate the picture from the code, keep the contract hand-written, and never let the picture
  become the thing reviews argue with.
- The **component-and-connector view** answers "what talks to what at run time": the activity,
  ISR, queue, and channel topology of chapters 6–7. It diverges from the module view the moment
  a function pointer binds or a queue interposes — which is exactly why it is a second artifact
  rather than a second reading of the first (§3.3's two-graphs rule).
- The **allocation view** answers "where things live": the memory map (chapter 9), the build
  variants (§5.4), and ownership by team where more than one team exists.

Two registers complete the description. Every forbidden edge, ladder descent, and binding-time
choice records its *why* as an `architecture-decision-record` — cross-referenced from the
contract that enforces it, because the corpus's own problem statement for ADRs is what happens
otherwise: later maintainers either cargo-cult the decision or blindly reverse it. And where
this system meets foreign ones — the vendor SDK, the peer controller, the cloud backend — a
`context-map` names the *kind* of each seam (who conforms to whom; where an anti-corruption
adapter stands), which no dependency rule can express. *(views regenerated in CI:
build-catchable freshness; ADR linkage and map upkeep: contract-only, on the review checklist)*

Decisions this chapter leaves to the specialization: the concrete include-graph checker and its
invocation; the symbol-visibility mechanism; the prefix registry; the generator toolchain and which
contracts it owns; the view-generation tooling and regeneration cadence. *(the OPEN register,
chapter 15)*

## 4. The effect boundary: decoupling logic from effects

This chapter is the center of the book. Everything before it supplies the mechanism; everything
after it is an application of it to one class of effect — time, memory, failure, evidence.

### 4.1 Name the effects

An embedded program's effects are enumerable, and the enumeration should be written down per
system, because it is the port list in embryo. The recurring catalog:

- **Peripheral and register access** — the direct manipulation of hardware state.
- **Interrupts** — effects that happen *to* the program; concurrency that arrives uninvited.
- **DMA** — effects performed by third-party hardware on the program's own memory, on its own
  schedule; aliasing and lifetime made physical.
- **Time** — reading clocks, setting timers, waiting; and its shadow, the deadline.
- **Power and reset** — mode transitions, brownout, the watchdog, the reset line itself.
- **Nonvolatile memory** — writes that survive the program, with erase cycles as a budget.
- **Communication** — frames in, frames out, with the far side's clock and failures attached.
- **The build** — conditional compilation and link-time selection are effects on program *text*;
  they belong in the catalog because they too must be confined (chapter 5).

Nothing on this list can be removed; every item can be *placed*.

### 4.2 The core decides; the shell does

The organizing pattern is the corpus's `functional-core-imperative-shell` (named by Bernhardt,
2012), reinforced at component scale by `humble-object` (Meszaros, 2007), and at architecture
scale it *realizes* `hexagonal-architecture` (Cockburn, 2005). One rule, three altitudes:

> **Decision code computes what should happen and returns it as data. Shell code makes it happen.**

In C this is concrete and unceremonious. A decision function takes the relevant state and the event,
and returns a result — new state plus *effect values*:

```c
/* core: pure, host-testable, no hardware headers on its include path */
charge_decision_t charger_step(const charger_state_t *s, const charger_event_t *ev);
```

The decision type is plain data — a tagged struct or a small array of effect records ("set PWM to
x", "open contactor", "emit fault F_OVERVOLT"). The shell — the task loop, at the edge — passes
events in, receives decisions, and executes each effect through a port (§4.3). The corpus's
`defunctionalization` (Reynolds, 1972) names exactly this move: behavior turned into data so it can
be stored, inspected, logged, and replayed. What a functional language does with closures, C does
with tagged structs — and gains something the closure never had: **the decision is loggable and
comparable**. The trace of decisions *is* the test oracle, the flight-recorder payload, and the
replay input, all in one representation.

Why this earns its indirection, in this domain specifically:

- **Testability**: the core builds on the host with no doubles at all — pure functions need no
  mocks, only inputs and expected decisions. The expensive half of embedded testing (the hardware)
  is simply absent from the majority of the code.
- **Determinism**: the core is deterministic by construction; given the same state and event
  sequence it produces the same decisions on the host, on the target, and in replay — stated
  with its conditions. For integer and fixed-point cores it holds wherever the arithmetic is
  width-explicit and promotion-safe, so the pinned implementation-defined properties cannot
  reach a result (§12.1 names the classic breach; the safe-subset analysis genre of §13.1
  checks for it). For a floating-point core it holds only under a pinned FP discipline in the
  platform contract (evaluation width, contraction, library, subnormal policy — §5.2's
  territory). This is what makes field failures reproducible from a recorded event log
  (chapter 12).
- **Analyzability**: WCET and stack analysis of straight-line decision code is tractable; the same
  analysis across an I/O-entangled function is not.
- **Failure containment**: the corpus's `error-kernel` reading — irreplaceable state lives in the
  small, simple core that does no I/O; risky work happens in expendable shell units that may be
  reset without losing the state that matters (chapter 10).

The costs, named so they can be declined by name: one copy of the effect data per step, one
dispatch per effect, and — the honest one — the design work of defining the decision vocabulary. In
the tightest control loops the dispatch cost is real; the resolution is not to break the pattern
but to shrink it: the loop's core is still a pure function, its shell is ten lines of register
writes, and both fit in one page a reviewer can hold. What is *not* accepted is the middle-ground
function that reads a sensor, filters it, decides, and actuates in one body — the corpus's
paradigm-menu warning made literal: a module that both computes and schedules can be tested for
neither.

### 4.3 Ports: the shape of an effect interface

A **port** is an interface the *core* owns, written in the core's vocabulary, describing an effect
the core needs — not a wrapper around a vendor API written in the vendor's vocabulary. The
distinction, from the corpus's hexagonal entry, decides whether the architecture is real: a port
named `pwm_set_duty(channel, permille)` belongs to the core; a port named after a vendor's timer
peripheral is an adapter wearing a port's clothes, and the vendor has just colonized the
application.

In C a port is one of two things, and the choice is the binding-time decision of §5.4:

- **A header of free functions** (`charger_pwm.h`), bound at link time to whichever adapter the
  build selects. Zero indirection, one implementation per image — the seam is the linker — and
  one residual price: the call is an optimizer barrier across the seam unless link-time
  optimization is on.
- **A struct of function pointers** (`pwm_port_t`), bound at initialization, allowing several
  implementations to coexist in one image (two identical buses, production driver plus recorder,
  the built-in-self-test wrapping the real driver). The cost is one indirection per call, one
  pointer table in RAM, and one the verification story pays: an indirect call is opaque to
  static stack and timing analysis until its target set is enumerated — init-bound tables keep
  that set finite and known, and the specialization feeds it to the analyzer (§13.1). Priced,
  and often worth it precisely where flexibility lives.

Both forms carry the same obligations: the port's contract states units, ranges, error modes,
timing (may it block? for how long?), and ownership of every buffer that crosses it. And the port
set is the *whole* effect surface: the corpus's testability tactics become mechanical when they
have a boundary to operate at — `sandbox` (virtualize the uncontrollable resource), `record-playback`
(capture what crossed), `abstract-data-sources` (repoint the input) all attach at ports and only
at ports.

### 4.4 The dependency arrow points inward

The `separated-interface` rung of §3.3 does the load-bearing work here: **the port header lives
with the core** (the consumer), and the adapter *includes it* — never the reverse. The core's
directory compiles with no adapter, no vendor SDK, no RTOS header on its include path; that
property is checked by the build (§3.3, rung 4) and re-proven every time the host test suite links
the core against fakes. Cockburn's observation, quoted in the house architecture manifest and
doubly true on the bench: **the test suite is just another adapter.** If a test must reach past a
port to drive the core, the port is misplaced — that is a design finding, not a testing
inconvenience.

The same arrow governs callbacks. When an adapter must call the core (an ISR delivering a frame),
it does so through a core-owned callback type registered at initialization — the adapter still
depends on the core's vocabulary, never the reverse.

### 4.5 What the boundary is not

It is not a promise that the core is large. In a driver-heavy system the shell may be most of the
code; the boundary still pays, because the part that *decides* — mode logic, protocol state,
fault policy, control law — is exactly the part whose defects are expensive, and it is now the
cheap-to-test part. It is not layering by another name: layers order dependencies top-to-bottom
and pay pass-through cost at every level; ports-and-adapters is symmetric — everything outside,
hardware and test rig alike, plugs into the same inside. The corpus records them as alternatives
(`hexagonal-architecture --alternative-to--> layers`), and chapter 5 uses both: hexagonal for the
effect boundary, thin layering inside the adapter stack where it genuinely buys exchangeability.
And it is not a license for a port per peripheral register: a port with exactly one conceivable
adapter, forever, is indirection bought and never used — the arch manifest's own degradation
clause. Ports follow *decisions that can change* (§2.1): the sensor vendor, the bus, the storage
technology, the transport — not every twiddle of every bit.

### 4.6 The composition root

Every port binding of §4.3 happens somewhere, and the discipline is that it happens in exactly
one place: the **composition root** — the code that runs between reset and the first pumped
event, where the system is assembled. C grants this design a quiet blessing: objects with
static storage duration have no user-written initializers to run behind your back, so —
provided constructor-attribute extensions stay quarantined per §5.2 — *nothing happens before
the root says so*, and initialization is a readable, ordered sequence of explicit calls in one
file.

The root's order is architecture, not accident — and the watchdog frames it: where the
hardware allows, the watchdog is armed first or arrives armed from reset, with the startup
budget as its window, so a hang anywhere in bring-up resets and *counts* (§11.1) rather than
parking the unit forever; arming late is a recorded decision with a named substitute, never a
default. Then: platform first (clocks, memory, protection regions), with the *destructive*
half of §10.5's self-test — the RAM march — run here, before anything lives in RAM, and
sequenced against §11.1's evidence: reset cause read, the persisted record validated and
harvested before the march touches its region. Adapters next; then port tables bound
(link-time bindings resolved already, §5.4's init-time bindings filled now); then
configuration loaded from its nonvolatile home and *validated* — a bad configuration meets the
fail-fast pole of §10.4 and the refuse-to-start safe state, never a best-effort limp into
service. Then the *non-destructive* remainder of the self-test gate — peripheral and loopback
checks, against adapters that now exist; then every state machine initialized to its named
initial state; the harvested evidence emitted as the new life's first trace events; and only
then does the shell begin to pump. Two rules keep the root honest. **No effects before their owner
exists**: modules do not touch hardware from helpers called early; they are initialized by the
root, in the root's order, or they wait. **Only the root knows the whole inventory**:
everything else receives its collaborators through ports — the root is the one sanctioned
place where "which adapter" is spelled out, which is what makes ambient lookup everywhere else
unnecessary and therefore forbidden. The host build has its own root binding fakes — the second
composition proves the first one's design — and the init sequence itself is host-tested: order
violations are cheap to assert when the order is a table. *(analysis-catchable for the
quarantined-extension rule; host-test-catchable for the order; startup-to-operational time is a
budget, §13.1)*

## 5. Decoupling from the target: the port called "hardware", the port called "compiler"

Target independence is the previous chapter applied to two specific outsiders — the silicon and
the toolchain — plus the discipline for the one place variation is allowed to bind early: the
build.

### 5.1 The layered target stack, named

The corpus carries the embedded layering as first-class elements, and the names are worth using
because each is a different *unit of replacement*:

- **`hardware-abstraction-layer-arch`** (named in Beningo, *Reusable Firmware Development*, 2017):
  the hardware-independent interface set for peripheral and processor access — in this booklet's
  terms, the union of the core's hardware-facing ports. Its unit of replacement is *the silicon*.
- **`board-support-package`** (named in Simmonds, *Mastering Embedded Linux Programming*): boot
  code, clock and pin configuration, memory maps, device wiring for one *board* — the adapter
  bundle beneath the HAL. Its unit of replacement is *the board revision*.
- **Drivers** sit between: peripheral-specific mechanism, exposed only through ports. The catalog
  deliberately has no "driver architecture" element — the booklet's rule is simply that a driver
  is an adapter like any other: it implements ports, it does not invent policy.
- Above all of it, the **application core** from chapter 4, which names none of them.

Reference stacks — Douglass's `five-layer-architecture-rtdp` (application / UI / communication /
abstract OS / abstract hardware) and the AUTOSAR layered architecture with its generated RTE — are
worked examples of the same shape at two ceremony levels. The AUTOSAR case is worth one more
sentence: its RTE is a *generated* port layer (§3.6's top rung industrialized), and its "complex
device drivers" escape hatch is the honest admission every layered stack needs — a sanctioned,
*named* bypass for the cases the abstraction cannot serve, so the bypass is visible in review
rather than smuggled.

Two warnings keep the stack honest. **Leaky vocabulary**: a HAL whose port signatures mention
vendor register fields has already failed; the test is whether the port header could be read by
someone who has never seen this silicon's datasheet. **Pass-through bloat**: a layer that only
forwards is cost without hiding; collapse it. The layering exists to hide *decisions* — which
silicon, which board — not to add floors.

### 5.2 The compiler is a target too

Compiler-agnosticism is achieved the same way, and the corpus's catalog for C modularity applies
directly. The program is written against ISO C. Everything beyond ISO C — extension keywords,
attributes, intrinsics, pragmas, inline assembly, linker-section placement — is an *adapter
concern*, quarantined in a small set of headers the specialization owns (`compiler_port.h`,
`sections_port.h`, and peers), exactly as hardware access is quarantined behind the HAL. Core code
includes the port header and uses its named macros and types; it never spells a vendor extension
inline. The payoffs are the same as for silicon: the toolchain can be replaced (qualification
pressure will eventually force it), diagnostics can be compared across compilers — a second
*opinion* that exists only when the host compiler family differs from the cross family, so
choose it to differ — and the host build stops being a porting project.

Undefined behavior deserves its sentence: what ISO C leaves undefined, this booklet's programs do
not do — not "do carefully", do not do — because every agnosticism promise dissolves where UB
begins. Implementation-defined behavior is handled by name: each reliance (integer widths,
representation, alignment, bitfield layout, endianness where protocols meet memory) is either
avoided, or pinned in the specialization's platform contract and checked by a static assertion or
a startup self-test. *(compiler + runtime-catchable; the rule-set that polices UB is
analysis-catchable and pinned by the child.)*

### 5.3 Variant management: escaping ifdef hell

Conditional compilation is the domain's native variation mechanism and its native pathology. The
corpus names the cure `escaping-ifdef-hell`: **confine variant selection to dedicated files behind
a common interface** — never scatter `#ifdef TARGET_X` through logic. The discipline:

- Feature and target selection happens in *one place* (a configuration header the build generates
  or selects), and what it selects is *whole implementations*: which adapter file is compiled,
  which port binding is linked — the corpus's `facade-backend-module-pattern`, where "the seam is
  moved to the build."
- Inside logic files, `#if` appears only for compile-time contracts (static assertions) — not for
  behavior. A function whose body interleaves three targets' register writes under conditionals is
  three functions filed in one grave.
- Every `#ifdef`'d variation point is a *binding-time decision* (§5.4) that could instead bind at
  link or init time; compile-time binding is chosen for its zero cost, and the choice is recorded.
  The corpus states the axis as a sourced pair: `escaping-ifdef-hell` is the compile-time
  alternative to the runtime `feature-flag`.

*(analysis-catchable for confinement — conditional-inclusion location audits are mechanical;
the selection judgment behind each variation point is contract-only and reviewed, §13.1.)*

### 5.4 The binding-time ladder

Every variation point binds somewhere, and C offers four rungs, each later, each costlier, each
more flexible — the corpus's `defer-binding` tactic with its cost model attached ("up-front
mechanism cost traded against per-change cost"):

1. **Compile time** — `#ifdef`, configuration headers, x-macro tables. Zero runtime cost;
   variation invisible in the shipped image; every variant is a separate build to test.
2. **Link time** — same header, different object files; the `facade-backend-module-pattern`
   move. Zero runtime
   cost; variants differ only in link inputs; the seam of choice for target substitution and for
   test doubles (chapter 12).
3. **Initialization time** — function-pointer ports and configuration read from nonvolatile
   storage (`resource-files`, in corpus terms) bound once at startup, immutable after. One
   indirection per call; one image serves many configurations; startup must validate what it read.
4. **Run time** — mode switches, `feature-toggle` kill switches, calibration updates. Full
   flexibility; full obligation: every runtime-variable behavior multiplies the state space the
   tests and the analysis must cover.

Default: **bind as early as the rate of change allows** — and record the rung. A booklet-level
warning attaches to rung 1: a variant that exists only under a rarely-built `#ifdef` is untested
code by definition; the build matrix must build what ships, or the variant is fiction
(chapter 13).

### 5.5 Protection hardware, placed

The MMU-or-not clause resolves here cleanly. Boundaries are designed as if no protection hardware
exists: ownership, static allocation, the effect boundary — structure first, always. Where the
part provides an MPU or MMU, the specialization maps the *already-existing* boundaries onto it —
task stacks and their guard regions, peripheral windows per adapter, read-only text and tables,
no-execute data — so violations that would have been silent corruption become immediate faults
with evidence attached. That is `runtime-catchable` enforcement at protection-domain
granularity — ownership, stacks, and effect surfaces; module privacy *inside* a domain remains
the compiler's and the analyzers' business — and it is the
strongest rung available at run time. The corpus's `time-and-space-partitioning` (ARINC 653)
is the fully industrialized form: statically allocated memory regions and fixed execution windows,
enforced by the platform, per partition. A program that is *only* safe under that enforcement was
never safe; a program that is safe without it becomes *diagnosable* with it.

Decisions this Part leaves to the specialization: the HAL port list and its naming; the pinned
platform contract (widths, alignment, endianness assumptions and their checks); the compiler-port
header set and the extension inventory it may contain; the variant matrix the build must actually
build; the MPU/MMU region map where hardware exists. *(chapter 15)*

---

# Part III — Behavior: events, interrupts, and time

## 6. Events, state machines, and the execution shell

### 6.1 The reactive core: run-to-completion event processing

The behavioral heart of an embedded program is a set of **state machines consuming events from
queues**, and the semantics that makes them analyzable has a name the corpus sources to Samek
(*Practical UML Statecharts*, 2008): **`run-to-completion-event-processing`**. Each event is
processed fully — every transition, every entry and exit action — before the next event is
dequeued, so the machine is never observed mid-transition. The consequence is the cheapest
atomicity guarantee in the field: code between two event boundaries needs no lock against its own
task, because nothing of its own task can interleave. Allowing a new event to interrupt in-progress
transition processing creates unanalyzable interleavings; run-to-completion is what rules them out.

The event-driven statechart discipline follows, all of it cataloged with sources:

- **`finite-state-machine`**, and for nontrivial mode logic **`hierarchical-state-machine`**
  (Harel's statecharts, implemented in C by Samek's and Douglass's pattern families): hierarchy
  for shared transitions, orthogonal regions for independent concerns, history for resumable
  modes, and the supporting mini-catalog — `deferred-event` (park what this state cannot handle),
  `reminder` (post to self), `ultimate-hook` (parent handles what children decline).
- **`state-transition-table`** (Douglass) as the data-driven implementation: the machine as a
  table is inspectable, generatable (§3.6), and traceable row by row.
- **Explicit state, one place**: the corpus's `localize-state-storage` tactic names the payoff —
  a machine whose whole state lives in one struct can be *constructed* at any state by a test
  instead of driven there, and *dumped* whole by the recorder. This single property serves
  chapters 11 and 12 more than any tooling will.
- **Transitions are logged events**, always (chapter 11): a state machine that does not log
  transitions is a debugging hazard — "how did we get here?" is the most common integration
  question and it is answered cheaply in advance.

Why state machines rather than flags and nested conditionals: a machine makes the state space
*enumerable* — reviewable against the spec, coverable by tests state-by-state and
transition-by-transition, checkable at runtime (an illegal-transition branch is a built-in
`sanity-check`), and analyzable for WCET per transition. A tangle of booleans is a state machine
that refuses to say how many states it has.

### 6.2 Active objects: concurrency without shared state

Scaled up, the same discipline becomes the corpus's **`actor-based-architecture`** (Hewitt's
formalism; in embedded practice the QP-style active object, and the corpus records the enabling
edge as sourced to Samek: run-to-completion is what lets an actor process messages without
reentrant state corruption). Each concurrent activity is an **active object**: a private state
machine, a private event queue, and *no other way in*. (*Activity* is this booklet's word for
the design-level unit; *task* names its realization on a preemptive shell.) Callers post
events; they never call across
into another activity's state. One writer per datum, by construction — which dissolves, rather
than solves, most locking problems (chapter 7 handles the residue).

This is the booklet's default concurrency architecture, chosen over shared-state threading for
stated reasons: it composes with run-to-completion (atomicity without locks), it makes the
message log the system's own trace (chapter 11), it gives each activity a stack and a queue whose
budgets are measurable (chapter 9), and it isolates failure (an activity can be reset alone —
`units-of-mitigation`, chapter 10). Its price, stated: every interaction pays a queue hop and
at least an event envelope — a payload copy too, unless the event carries an owned buffer under
invariant 12's transfer contract, which is how the zero-copy actor frameworks run — and control
flow no longer reads top-to-bottom in one function — the modifiability-for-
per-event-cost axis again. Where a hard loop cannot pay it, that loop runs as a synchronous
chain inside one activity, and the decision is recorded.

### 6.3 The execution shells, named

What runs the state machines is a *shell decision*, and the corpus catalogs the whole menu as
architecture elements — which means the choice can be made by name, with each option's cost sheet:

- **`superloop-architecture`** (Pont's naming): no OS; one endless loop services everything,
  interrupts as the foreground feeding flags and buffers to the background. Simplest possible
  audit; response time is the sum of everything ahead of you in the loop.
- **Cyclic executive / `time-triggered-co-operative-scheduler`** (Pont; Kopetz's
  `time-triggered-architecture` at system scale): activation instants planned statically against
  a time base; determinism by construction, at the price of a schedule that must be re-planned
  when anything grows. The strongest analyzability story this list has.
- **`function-queue-scheduling-architecture`** (Simon, *An Embedded Software Primer*): interrupts
  enqueue work; the loop runs it to completion in priority order — priority-ordered response
  without a kernel, worst case bounded by the longest queued function, and preemption-grade
  only insofar as every function is kept short.
- **`rtos-based-architecture`** (Simon): prioritized preemptive tasks on a kernel, response times
  set by priority rather than loop position; buys schedulability analysis (chapter 8) and costs
  per-task stacks, kernel objects, and the full shared-state discipline of chapter 7.
- **`event-triggered-architecture` vs `time-triggered-architecture`** (Kopetz, both directions):
  react to occurrences vs act on the clock — the axis underneath the whole menu, and a
  per-subsystem choice, not a religion.

The parent-level law is the one the corpus states as its rare `constrains` edge (architecture
constraining design): **the shell removes options from the design layer beneath it.** A
cooperative shell forbids blocking waits anywhere — long activities must decompose into stepwise
state machines (`multi-state-task`, Pont; `protothread` is the pattern family's mechanized form).
A preemptive shell permits blocking and charges for it in stacks, priorities, and shared-state
hazards. What the core state machines must never do is *know which shell runs them*: they consume
events and return decisions (chapter 4), and the shell — superloop today, RTOS after the redesign
— is an adapter. That is the RTOS-agnosticism promised in chapter 1, made structural.

Two shell obligations regardless of choice: **every queue is bounded with a stated overflow
policy** (`bound-queue-sizes`, Bass's tactic: an unbounded queue is not load-leveling, it is a
deferred out-of-memory failure; and overflow handling — drop-oldest, drop-newest, count-and-flag
— is policy, decided per queue, never left to accident); and **event arrival is managed at the
edge** (`manage-event-arrival`, `manage-sampling-rate`, `prioritize-events`): the shell owns
admission — rates, priorities, coalescing — so bursts are absorbed where they enter, not
discovered as missed deadlines three modules deep.

### 6.4 The idle architecture

Idle is a designed mode, not the absence of work, and it belongs to the shell. The cataloged
mechanisms give it structure: the `idle-task-hook` runs what must cost only otherwise-idle
cycles — the patrol scans of §10.5, the watermark checks of §9.4, the trace drain of §11.2 —
and `tickless-idle` is the deeper form: suppress the periodic tick, program a one-shot wake for
the next deadline, and sleep the processor in a low-power state.

Three disciplines keep power
from leaking into logic. **Wake sources are events**: the core learns "the button woke us" the
same way it learns everything, through a port, so power states never appear in decision code.
**Power states are states**: the power domain is a state machine under this chapter's own rules
— transitions logged, illegal transitions checked — and entering sleep is an effect *value* the
core decides and the shell executes, like any other. **Energy is a budget**: the Bass energy
tactics (`metering` to know, `reduce-usage` to act) make consumption a measured, trended number
with an alarm, not a hope — and the sleep-versus-slow decision (race to idle at full clock, or
run slower and longer) is made on that measurement, per mode, and recorded. At architecture
scale the corpus carries `chained-processors` (White): a small always-on processor fronting a
large one it wakes on demand — the same decision at silicon granularity.

The watchdog and sleep
are designed as a pair: a kick map that does not know the sleep states will either reset a
sleeping system or force it awake just to be kicked — the child's watchdog topology (§8.4,
ch. 15) states which states pause, window, or excuse it. *(build-catchable — the energy budget
is a rung-4 fitness function, §13.1; traced transitions per §11.3)*

## 7. Interrupts and shared state

### 7.1 The ISR is a courier

An interrupt is the one concurrency no design can decline; it arrives on the hardware's schedule,
mid-anything. The discipline the corpus carries (ISR coding rules are sourced to the BARR-C
standard; the receive-livelock literature supplies the systemic argument) is uniform:

> **The ISR captures, timestamps, enqueues, and returns.** Decisions happen in task context.

Everything else follows. Work done in the ISR is work done at the highest priority in the system,
outside the scheduler's control — it cannot be deprioritized, and in chapter 8's analysis it
appears only as interference charged to everything below it — and invisible to the state
machines; so it is kept to the minimum the hardware demands (acknowledge, move the datum, note
the time). The deferred half —
`deferred-interrupt-processing`, the top/bottom-half split — runs as an ordinary event through
the ordinary queues, where it is schedulable, traceable, and testable. Two systemic hazards get
named defenses: **receive livelock** (interrupt load starving the work it feeds — the
Mogul-Ramakrishnan result) is countered by interrupt coalescing and by falling back to polling
under load, an *admission* decision belonging to the shell; and **priority inversion through the
ISR's data** is avoided by making the ISR-to-task handoff lock-free (§7.3).

The ISR is also a *port user like any other*: it is registered through the adapter layer, its
vector placement is an adapter fact, and the core never knows which line fired. On the way in it
performs the one conversion that must never be skipped: hardware fact → timestamped event.

### 7.2 Sharing rules: ownership before mechanism

Chapter 6 removed most sharing by construction (one writer per datum, queues between). What
remains — the ISR touching a buffer a task reads, two tasks genuinely sharing a table — is
governed by ownership *stated first*, mechanism second:

- Every shared object names its writer(s), its readers, and the mechanism that makes their
  overlap safe. Unstated sharing is the defect class; the mechanism is almost secondary.
- **`interrupt-masking-critical-section`** is the baseline mechanism where masking is cheap and
  sections are provably short — and every section's length is part of the system's interrupt-
  latency budget, so it is measured, not vibes (chapter 13's budgets).
- On preemptive shells, kernel-object sharing inherits the classic hazards with classic, named
  answers: bounded priority inversion via `priority-inheritance-protocol` or
  `priority-ceiling-protocol` (Sha, Rajkumar & Lehoczky; the ceiling form bounds blocking to one
  critical section and prevents deadlock, and is this booklet's default where the shell offers
  it); deadlock prevention by `ordered-locking` where multiple locks are unavoidable — the lock
  order is design, written down, reviewed.
- **`volatile` is a contract keyword, not a concurrency tool.** The corpus files the discipline
  under `memory-mapped-register-access`: volatile-qualified access is what keeps the compiler
  from reordering or eliding device reads and writes *relative to other volatile accesses*; it
  provides no atomicity, no ordering against non-volatile code, and no guarantee of *when* a
  write reaches the device — write buffers and posted bus bridges defer it even on one core,
  and the canonical defect is the interrupt source cleared as the ISR's last act, still in
  flight at return, re-entering the handler spuriously. Atomicity comes from the mechanisms
  above; completion and system-level ordering — the read-back or barrier after that clearing
  store, single-master included, and everything multi-master (DMA, a second core) — come from
  the platform's barrier operations, which are, per §5.2, adapter vocabulary behind the
  compiler port, never bare in logic. The miscompilation literature the
  corpus flags (volatile handling has historically been miscompiled) is one more argument for
  confining these accesses to small adapter files where an object-code review is feasible.

### 7.3 The canonical channel: single-producer single-consumer

The ISR-to-task handoff deserves its own named structure because it is the one place where
lock-free is the *simple* option: the **single-producer/single-consumer ring buffer**
(`spsc-lock-free-ring-buffer`; White's *Making Embedded Systems* treats the circular buffer as
the canonical interrupt-to-mainline channel). One writer, one reader; each index written by one
side only, read and written through accesses the compiler is obliged to perform at the boundary
— volatile- or atomic-qualified, never plain, or the consumer's poll legally collapses into a
single load; and publication *ordered* — data written before the index that publishes it, the
slot copied out before the index that releases it — by compiler barrier at minimum, by the
platform's acquire/release pair whenever the peer is another master. Correct without locks
*only* under exactly those roles and that ordering, which is why both are stated in the type's
contract and everything stronger (multi-producer, multi-consumer) routes through a kernel queue
instead. Its sibling for
state-shaped (latest-value-wins) data is the **`double-buffer`** swap: writer fills the
inactive bank and flips — coherent for the reader only while the protocol keeps the writer out
of a bank a reader still holds, by time control, by handshake, or by a third bank where both
sides free-run. The flip itself is a published index carrying this section's ordering
obligations. The corpus's `temporal-firewall` (Kopetz) is this idea promoted to an
architectural connector — a unidirectional, time-controlled data-only interface with no control
signals crossing — and it is also the cleanest DMA handoff shape.
Overflow on any such channel is counted and visible (invariant 10); a dropped sample with no
counter is a lie the system tells its own recorder.

### 7.4 The second master

Everything above assumed one processor and its interrupts. Most systems now have more masters:
the DMA controller (whose ownership story §9.3 carries) and, increasingly, a second core. The
parent's default for inter-core design is the one chapter 6 already established: **message
passing over owned memory** — per-direction SPSC channels or hardware mailboxes, payloads
immutable after publish, each datum owned by exactly one core — the actor discipline stretched
across the silicon.

Genuinely shared state between cores is the exception, and it imports the
platform's memory model wholesale: publish/consume built on `acquire-release-ordering`,
explicit `memory-barrier` operations where the model demands them, and
`false-sharing-avoidance-via-cache-line-padding` where independently written data would share a
line — all of it adapter vocabulary behind the platform port per §5.2, never spelled bare in
logic, with the concrete model pinned by the child (ch. 15). The distinction §7.3 draws now
sharpens: on a single core, the SPSC channel's ordering can be discharged by compiler barriers
and preemption reasoning; across cores the same structure requires the hardware ordering pair
at its indices — same shape, stronger contract — so every channel states which environment it
is built for. Cache maintenance at the handoff points is the owning adapter's job, like DMA's.

And one disambiguation, because the name invites confusion: `dual-core-lockstep` is not a
programming model — it is safety hardware executing one instruction stream redundantly and
comparing, invisible to software; a chapter-10 mechanism wearing a core count. *(the
per-channel environment contract: contract-only; the ordering primitives themselves:
compiler/analysis-catchable inside the platform port)*

## 8. Time as a dependency

### 8.1 Injected time

No core code reads a clock. Time arrives as data: the tick event carries the tick count; sampled
events carry capture timestamps stamped at the ISR (Bass's `timestamp` tactic — assign clock
state at the event, immediately, so ordering disputes are decidable later); deadlines and
timeouts are parameters. The `system-tick` element and the timer-wheel literature the corpus
carries (hashed and hierarchical timing wheels) live in the shell as the timer service behind a
port; the core sees only "this deadline expired" as one more event. What this buys is everything
chapter 12 needs: on the host, simulated time runs as fast as the test wants and as slow as a
breakpoint needs; in replay, recorded timestamps reproduce the field's interleaving exactly. A
hidden wall-clock read in the core is the determinism leak nothing mechanical detects —
contract-only, reviewed for by name.

Two time-quality rules from the domain's canon: a timestamp's *source and resolution* are part of
its contract (tick count vs free-running counter vs calendar time — never mixed silently, and
calendar time, which can jump, never sequences anything); and duration arithmetic uses the
platform's monotonic base with wraparound-safe comparison — serial-number arithmetic, which the
corpus records by its RFC — under its condition, made part of the timestamp contract: width and
resolution sized so no compared span reaches half the counter's range. That is what makes a
rollover a non-event instead of a once-per-49-days field mystery; unsized, the comparison does
not fail, it silently answers wrong.

### 8.2 Deadlines and the scheduling canon

Hard timing claims are calculated, not hoped. The canon is compact and the house corpus carries
it end to end: Liu & Layland's utilization bound for rate-monotonic priorities (sufficient, quick,
conservative); **response-time analysis** (Joseph & Pandya; Audsley et al.) as the exact test —
worst-case response per task from its cost, its blocking, and higher-priority interference,
iterated to fixpoint against the deadline; deadline-monotonic ordering where deadlines are
shorter than periods (Leung & Whitehead). Blocking terms are bounded by the ceiling protocol
(Sha, Rajkumar & Lehoczky — the Mars Pathfinder reset is the domain's standing reminder of what
unbounded inversion does), and ISRs are modeled as top-priority periodic load. Buttazzo is the textbook
spine. All of it is the single-scheduling-domain canon — one processor, fixed priorities; a
specialization that schedules across cores (§7.4) pins its own analysis and locking protocol,
because none of these bounds transfers unchanged.

What the booklet fixes as *architecture* is not the algebra but its inputs' discipline:
every hard-deadline task states its period, deadline, and measured or analyzed worst-case cost;
those budgets live with the code, and the analysis re-runs when they change (chapter 13 makes
this a gate). `bound-execution-times` (Bass) is the per-task tactic — bounded loops, bounded
work per event — that keeps the numbers analyzable at all; it is also the reason the
Power-of-Ten-genre rules bound loops statically.

### 8.3 Timeouts, and the two poles of impatience

Every wait *within work* has a bound — acquisitions, responses, hardware flags. The one exempt
wait is the activity blocked at the top of its loop for its next event: that idleness is
legitimate, and its liveness belongs to the watchdog's check-in map (§8.4), never to a timeout
whose expiry path would check in on its behalf. A blocking acquisition without a timeout is a
hang wearing a semaphore's
clothing; a busy-wait on a hardware flag without a `loop-timeout` (Pont's name) is the same hang
one layer down. And when the bound expires, the two named poles of §10.4 apply — fail fast, or
ride over the transient with a counted budget — chosen per wait, never defaulted. Deadlines
compose down call chains by *propagation* (the SRE-sourced `deadline-propagation` rule): pass the
absolute deadline, not per-hop timeouts, so a deep chain stops working the moment the answer
stopped mattering.

### 8.4 The watchdog is not a timer

The watchdog closes Part III because it is the shell's last time-shaped obligation and the most
misused device in the domain. The corpus carries both halves: the design-realm `watchdog` element
(Koopman's chapter is the naming source: correct kicking discipline, and what a watchdog can and
cannot detect) and the architecture-realm `watchdog-architecture-pattern` (Douglass: an
independent supervisor, ideally with its own time base, that receives liveness evidence and
initiates recovery). The discipline in four sentences: **the kick attests progress, not
existence** — it is issued from one place, only when every activity *expected active in the
current mode* has proven a completed cycle (a per-activity check-in bitmask with a mode-owned
expected set is the minimal honest form; an idle activity is excused by the map, never by
checking in from a timed wake); a kick from a
timer ISR proves only that timer interrupts still fire, and Koopman's red flag is exactly that.
The watchdog is the *enforcement* of chapter 10's recovery ladder, not a recovery strategy
itself. Its firing is a designed event with evidence attached (chapter 11's persisted record),
not an embarrassment. And the `sanity-check` twin (Douglass: plausibility of outputs) covers the
failure class the watchdog cannot — a system confidently computing nonsense on schedule — which
is why the corpus records them as complementary, liveness and correctness, two monitors.

Decisions Part III leaves to the specialization: the shell itself and its schedulability
analysis format; the queue inventory with depths and overflow policies; the lock inventory and
ordering where locks exist; the tick source, resolution, and timestamp format; the watchdog
topology (internal, external, windowed) and its check-in map. *(chapter 15)*

---

# Part IV — Memory

## 9. Memory as architecture

On a desktop, memory management is an implementation concern. On a target with sixty-four
kilobytes of RAM, no protection hardware, and a decades-long service life, **memory is
architecture**: where every byte lives, who owns it, and when it moves are design decisions with
failure modes attached, and the catalog of named mechanisms here is among the richest the corpus
holds — almost all of it sourced to the embedded canon (Douglass's real-time patterns, Noble &
Weir's *Small Memory Software*, Preschern's *Fluent C*, Hanson's interfaces).

### 9.1 The allocation ladder

Allocation strategies form a ladder from most analyzable to most flexible. The booklet's rule is
to **claim memory at initialization and descend the ladder only behind a recorded decision**:

1. **`static-allocation`** (Douglass): objects and buffers fixed at link time or claimed once at
   startup; the heap is never consulted afterwards. Worst-case memory *is* the link map —
   analyzable by inspection, immune to fragmentation, and the reason the safety-critical rule
   sets ban post-init dynamic allocation. The corpus records the bridge outright:
   static allocation *realizes* exception prevention — the whole class of allocation-failure and
   fragmentation faults cannot arise.
2. **`pool-allocation`** and **`fixed-sized-buffer`** (Douglass): populations of same-shaped
   objects drawn from pre-sized pools, O(1) and deterministic, returning to the pool whole. Pools
   are the static answer to "N of them at once", and the pool's high-water mark is a designed
   observable (chapter 11). One scoping rule keeps invariant 11 honest here: exhaustion of a
   pool sized against demand the design controls is a design error, but exhaustion of a pool
   fed by *external* arrivals — receive frames, event bursts — is invariant 10's overflow case
   wearing its memory face, met with a stated shed policy and a counted drop, never an assert.
3. **`memory-arena` / `memory-discard`** (Hanson; Noble & Weir): bump-allocate through a scratch
   region, reset it wholesale at a phase boundary — the right shape for per-cycle or per-frame
   working memory with no per-object bookkeeping to get wrong.
4. **Heap at initialization only**: general allocation while the system assembles itself, frozen
   before operation begins. All flexibility of layout at boot, none of the fragmentation risk in
   service.
5. **General heap in operation** — the rung that requires a written justification. Where a
   genuinely dynamic workload forces it, the domain's own literature supplies the honest form: a
   real-time-suitable allocator (the corpus carries TLSF, constant-time by construction), an
   **`allocation-wrapper`** (Preschern) so every allocation crosses one instrumented, budgeted
   choke point, and a stated policy for exhaustion — because on rung 5, exhaustion is back to
   being a runtime condition, and chapter 10 owns it.

Two supporting disciplines whatever the rung: **`memory-limit`** (Noble & Weir) — explicit
per-component budgets, so exhaustion indicts a component rather than the system; and
**`read-only-memory`** placement — everything constant lives in flash/ROM by construction,
reserving RAM for state that actually mutates. `eager-acquisition` (the POSA resource patterns,
which the catalog notes as central to real-time design) is the ladder's generalization beyond
memory: acquire *every* scarce resource up front, hand out from the pre-acquired set.

### 9.2 Ownership is stated, always

C's memory model is a trust exercise; the corpus's Preschern cluster turns the trust into
contract vocabulary, and this booklet adopts it as mandatory interface language:

- **`dedicated-ownership`**: every allocation has exactly one owner responsible for its release;
  ownership transfer happens only at API boundaries and only explicitly.
- **`caller-owned-buffer`**: the default parameter-passing shape — caller allocates, callee
  fills, pointer plus size, lifetime never leaves the caller. It composes with every rung of the
  ladder, which is why it is the default.
- **`callee-allocates`**: the exception shape, for results only the callee can size — always
  paired with the releasing function in the same header, so the contract names both ends.
- **`out-parameters` and `aggregate-instance`**: results by caller-supplied pointer (keeping the
  return value for status, chapter 10), and related values bundled in a returned-by-value struct
  rather than scattered out-parameters.

An interface that takes or returns a pointer and does not say which of these shapes it is, is not
an interface yet. *(contract-only in the header text; partially analysis-catchable where the
specialization's rule set carries ownership annotations)*

Cleanup in C has named shapes too, and they are the language's substitute for scope-bound
release: **`goto-cleanup`** (the kernel-style single exit ladder, releasing in reverse
acquisition order) and **`cleanup-record`** (Preschern: a record of which acquisitions succeeded
drives one conditional teardown path). Both exist to make the error path *structurally* mirror
the success path — which is what makes it testable (chapter 12) rather than a copy-paste liability.

### 9.3 Lifetime across the machine boundary: DMA and ISRs

Ownership contracts earn their keep where a non-CPU party holds the pointer. A buffer handed to
DMA (`direct-memory-access-dma-transfer`, with `scatter-gather-dma` as the descriptor-chained
form) is *owned by the controller* until completion: the contract states when ownership
transfers (submit), how return is signaled (the completion event, through the ordinary channels
of chapter 7), and what the CPU may do meanwhile (nothing, for that buffer). The
`ping-pong-buffer` — two buffers alternating between filler and drainer — is the canonical
resolution, and cache-coherence maintenance around the handoff is adapter vocabulary behind the
platform port (§5.2). The same ownership language covers ISR-shared buffers: the SPSC channel of
§7.3 is, seen from this chapter, an ownership-transfer protocol with indices as the deed.

### 9.4 Stacks, and the budgets that make memory honest

Every task's stack is a budget, and the domain's instrument for it is cataloged:
**`stack-painting-watermarking`** — fill stacks with a pattern at boot, read the high-water
mark in service. The watermark is the deepest use *achieved* — a floor under the worst case,
never the worst case, which lives on the path no observed run took. The budget's ceiling comes
from static call-depth analysis where the call graph permits (§13.1, indirect-call target sets
supplied), otherwise from measurement plus a named margin with the residual risk on record; the
watermark is the in-service monitor that the margin is holding (chapters 11 and 13). Around it sit the defenses graded by hardware: `guard-page` or MPU guard
regions where protection exists; `stack-canary` values checked at boundaries where it does not;
`memory-poisoning` of freed and uninitialized storage so stale use surfaces as a recognizable
pattern instead of a haunting. The no-MMU clause of §5.5 lands concretely here: painting,
canaries, poisoning, and `pointer-check` (null on init and free, check before dereference —
Preschern) are the flat-address-space substitutes for the trap the hardware cannot give, all
`runtime-catchable`, all cheap, all reporting into chapter 11's evidence chain.

Alignment, padding, and layout (`packed-data` where space wins; explicit padding where layout is
contract) are stated per boundary-crossing type and checked by static assertion — layout is part
of the interface the moment a struct meets a wire, a flash page, or a DMA engine, and chapter 14
owns its evolution.

### 9.5 Nonvolatile memory is a component, not a heap

Flash and EEPROM carry budgets RAM does not — erase cycles, page granularity, partial-write
hazards across power loss — so persistent state is owned by a storage module with a port, never
scattered writes. The corpus carries the named mechanisms: `eeprom-emulation-in-flash`
(journaled records over paged flash), `flash-wear-leveling`, `log-structured-storage`
(append-only with compaction — the shape that *reduces* power-loss atomicity to the integrity
of the last append, provable only against a stated device model: an interrupted program can
leave marginal cells that read differently on different reads, so read-back after program, a
commit mark written last, and durable invalidation of a once-torn tail are part of the proof,
not decoration), CRC-guarded
records (chapter 10's integrity vocabulary applied at rest). The persistence module's contract
states write endurance spent per year at design time — a budget like any other, reviewed like
any other. The boot-and-update cluster (`bootloader-application-split`,
`a-b-firmware-image-update` with fallback, `secure-boot-image-verification`) belongs to chapter
14, but its memory-map consequences — slots, golden image, persisted-record regions that survive
update — are drawn here, in the map the specialization pins.

Decisions Part IV leaves to the specialization: the memory map itself; the ladder rung per
component with justifications on record; the allocator choice where rung 5 exists; the stack
budget table and watermark thresholds; the flash technology's endurance arithmetic; the
MPU/MMU region map where present. *(chapter 15)*

---

# Part V — Failure and evidence

## 10. The error contract

### 10.1 Two kinds of wrong, three dispositions

Every failure design starts by separating **expected conditions** (the sensor times out, the
frame fails CRC, the bus NAKs — environment behaving as environments do) from **contract
violations** (the pointer is null, the state is impossible, the invariant broke — the program
being wrong). The first class is handled; the second class is *stopped*, because code that
continues past its own broken invariants is manufacturing corruption downstream. Every mechanism
in this chapter serves one class or the other, never both.

C has no exception channel, and this booklet treats that as a feature to exploit: **the entire
handleable failure surface of a function is visible in its signature** — what a signature
cannot carry, the trap and the asserted stop, is exactly what §10.2 and §10.4 route to
safe-state and evidence. Within that constraint the corpus
gives three dispositions:

- **Return it, typed.** The default for expected conditions: `return-status-code` (Preschern —
  status returned, results through out-parameters) as the ambient C convention, and `result-type`
  — a tagged struct carrying value-or-error — where the payload earns it. In-band
  `special-return-value` and `sentinel-value` conventions (the NULL, the −1) are legacy surface:
  tolerated at the platform boundary where APIs impose them, converted to the typed convention at
  the adapter, never propagated inward. One convention per boundary, held (the arch manifest's
  rule); the adapter converts.
- **Absorb and mark.** For data-shaped work — a stream with a bad sample, a record set with a
  corrupt row — the corpus's CHECKS lineage (`exceptional-value`, `marked-data`): a distinguished
  value flows through the computation, is rejected at the output boundary, and the rejection is
  *recorded*. `saturation-arithmetic` is this disposition's absorb half, native to signal
  paths — honest only when paired with a sticky flag or a counter, per the rule that follows.
  The absolute
  rule from the house error contract: **absorbing with no rejects record is `try/continue` with
  extra steps** — the mark and the counter are what make the disposition honest.
- **Stop the world.** For contract violations: the assertion family. Preschern's
  `samurai-principle` names the C form — for errors the caller cannot meaningfully handle, do
  not return an error code; fail at the point of failure — because propagating an unhandleable
  error buries the fault and corrupts state downstream.

Every fallible call's result is **checked or visibly discarded** — the highest-value
`analysis-catchable` rule in the C repertoire, and the reason the typed-return discipline works
at all. And error codes are *architecture*: one system-wide identifier scheme, stable across
releases (they end up in logs, test assertions, field reports, and customer tickets — chapter
14 owns their evolution), each code carrying its origin module in its structure.

### 10.2 Assertions: one name, three lifetimes

"Checked by an assertion" names three different guarantees, and the design states which one it
means. **Development asserts** — dense, free to be expensive — die in the release build.
**Field assertions** — the subset guarding invariants whose violation would corrupt effects —
survive into release and route to §10.4's machinery; they are explicit checks, never anything a
build flag can silently strip. **`sanity-check`** (Douglass — the catalog's canonical name for
the family) is the third kind: a plausibility monitor on *outputs* — is the commanded duty cycle
physically possible, is the computed temperature on Earth — catching gross faults cheaply where
full verification is infeasible. Design-by-contract (Meyer) supplies the discipline that makes
all three diagnostic rather than decorative: a failed precondition indicts the caller, a failed
postcondition indicts the callee — **blame assignment is what turns an assertion failure into
the name of the missing test** (chapter 12). Assertions never validate external input — input
is expected-condition territory, disposition one — and the boundary between the two is exactly
the port surface of chapter 4.

### 10.3 Detect, decide, act — and who owns recovery

The corpus's fault-tolerance spine (Hanmer's pattern language, with Bass's tactic taxonomy
overhead) separates three responsibilities the untrained design fuses: **detection** happens
everywhere and is cheap (checks, CRCs, timeouts, watermarks); **deciding** what a failure means
belongs to the component whose contract it violates; **acting** — recovery — belongs to one
designated owner per containment unit, Hanmer's `someone-in-charge`. Error-handling code
smeared across every call site is the visible symptom of a missing owner; the `error-handler`
element names the concentration move. Detection reports *upward* through the typed channel;
recovery flows *downward* from the owner. The two graphs are different, and drawing them is one
page of architecture documentation that pays for itself at the first field return.

### 10.4 The recovery ladder, and the state you go to

Recovery is a ladder, not a reflex — `escalation` (Hanmer; Preschern gives the C form):
**retry** the operation (bounded, and only where idempotent — the retry composes with the
timeout of §8.3 or it is a hang); **reset the unit** — reinitialize the module, re-init the
peripheral (`restart`, and the corpus's `units-of-mitigation` defines the granularity: the unit
you can restart without restarting the world); **restart the task** — the active object rebuilt
from its initial state, its queue drained-and-marked; **reboot** — reset as a *designed* system
state, not an admission of defeat. Climbing is gated by evidence, and the gate is cataloged:
`riding-over-transients` with a `leaky-bucket-counter` — tolerate a *rate* of self-clearing
faults, escalate when the bucket overflows — against `fail-fast` for faults that indict
integrity. The two poles are both correct somewhere; a design names which applies per failure
class, or the field will improvise.

Two structural allies from the corpus complete the ladder. The **`error-kernel`** (the reactive
lineage, agreeing exactly with chapter 4): irreplaceable state lives where failures are not
processed — the pure core — so the expendable shell can be reset cheaply; crashing is
affordable precisely because of where the state does not live. And **`safe-state`** (ISO
26262's vocabulary): every failure path *ends in a named state* — outputs de-energized,
actuators parked, degraded mode with its capability list, or reboot — designed before it is
needed, reachable from anywhere, testable on the bench. "An unhandled fault" is not a state.
`degradation` and `abort` (Bass) are safe-state's two flavors — keep the critical functions,
or terminate before damage — and Douglass's safety patterns (`monitor-actuator`,
`protected-single-channel`, `safety-executive`) are the architecture-realm forms the
specialization reaches for when the hazard analysis demands independent supervision.

### 10.5 Integrity: trusting your own memory

Between detection and recovery sits a class the desktop never meets: the data may be lying. The
corpus's integrity kit, all element-backed: `cyclic-redundancy-check` on images at boot, on
persistent records at read, on long-lived RAM tables on a patrol schedule
(`correcting-audits` — scan and repair, or scan and quarantine). Douglass's
`one-s-complement-data-storage` covers the safety-relevant scalars, and
`program-sequence-monitoring` (IEC 61508's technique vocabulary) covers the hazard analyses
that require detecting *execution* going wrong, not just data. Last, `built-in-self-test`
exercises the hardware at startup — RAM march, ROM checksum, peripheral loopback — gated so
that a failed self-test lands in safe-state, not in service (the corpus records the composition
explicitly). The self-test is also ordered against the evidence chain: the march test and
chapter 11's reset-survivable region share the RAM map, so the test spares that region or runs
only after the record is harvested — the map states which. `brown-out-handling` closes the set: power is an input with failure modes, and
declining to run on sagging volts is a detection, not an outage.

### 10.6 What this chapter refuses

Heavyweight fault-tolerance machinery imported without its preconditions: `n-version-programming`
and `recovery-blocks` presuppose independent implementations and an adjudicator — safety-process
territory the specialization adopts only under its standard's demands. `setjmp-longjmp-error-handling`
— the C exception emulation — is refused as ambient convention (non-local control flow that
skips every cleanup contract of §9.2) and admitted only as a quarantined framework-internal
mechanism where a component genuinely needs unwind semantics, wrapped, documented, and never
crossing a port. And silent tolerance of anything: every ignored fault is a counted, visible
decision (`ignore-faulty-behavior` is a tactic with a name precisely so its use is deliberate).

### 10.7 The arithmetic contract

One more contract belongs to this chapter, because its violations are silent and its silence is
the domain's top numeric defect class. **Every arithmetic boundary — control law, accumulator,
protocol counter — states its overflow policy: wrap, saturate, or check.** The default in
decision code is checked (`checked-arithmetic`, the C23-lineage anchor) or saturating
(`saturation-arithmetic`, with §10.1's sticky mark); wrap is chosen only where modular algebra
*is* the contract, as in §8.1's serial-number timestamps — and then it is unsigned by
construction, because signed overflow is undefined behavior and §5.2's absolute already forbids
it. Representation is part of the port contract (§4.3): a fixed-point value's format and
scaling travel with its units and range, and a conversion is an explicit, named operation,
never a cast that hopes. *(analysis-catchable for signed overflow and the essential-type
discipline — the safe-subset genre's home ground; host-test + property-based for ranges and
saturation behavior, §12.4)*

## 11. Observability: the flight recorder principle

### 11.1 Postmortem-first

The observer arrives after the failure. Design for the reader of evidence, not the watcher of
consoles: the organizing question is not "what shall we print?" but **"when this comes back
from the field dead, what will the unit itself be able to tell us?"** The corpus carries the
pieces — `core-dump` (White: on fatal fault, serialize registers, stack, fault status to
persistent storage or a host channel), reset-cause reading, `log-errors` at the failure site
(Preschern: detail on a diagnostic channel where it exists, because the caller needs an
actionable error and the debugger of record needs everything). The booklet binds those pieces
into one obligation, stated in invariant 18: **every reset tells its story.**

Concretely, a
reset-survivable region holds the crash record (cause, fault registers, active state
identifiers, trace tail, and the identity — version and build id — of the firmware that wrote
it); boot *validates* the record — magic and checksum, §10.5's vocabulary
at rest, because after a power-on the region holds garbage that is not a record — then reads
the reset cause, emits both as the first trace events of the new life, and lets the recovery
ladder of §10.4 consult the *validated* escalation counter, so a boot loop converges to
safe-state instead of cycling forever and a first power-up never parks healthy hardware there. The
corpus's own gap register admits no flight-recorder element exists at architecture altitude;
this section is the booklet's editorial synthesis of the cataloged parts, and says so.

### 11.2 Trace is a port with a budget

The trace facility is designed like every other port: the core and shell emit **structured
events — identifiers plus small fixed payloads, never format strings** — into a bounded ring
buffer, timestamped from §8.1's injected time. Transports — debug link, UART, radio, flash,
nothing — are adapters bound per §5.4, and the house law transposes verbatim: **components
emit, the application routes.** Emission is cheap enough to leave on (an ID and two words, not
printf), drops under pressure are counted rather than silent, and severity exists but is not
the design: the load-bearing decisions are *which boundaries emit* (§11.3) and *what survives
where* — the live tail in RAM, the error-weighted summary in the persisted record, the full
stream only where a transport exists. The corpus notes the ring-buffer-plus-logging composition
carries no established element name; the parts (`ring-buffer`, `diagnostic-logger`,
`wire-tap` as the tap-without-disturbing shape) are cataloged, the composition is this
booklet's editorial default. What is *not* editorial: never log secrets, and treat the trace
format as a versioned contract — the decoder on the bench is a consumer like any other
(chapter 14).

### 11.3 What emits, mandatorily

Three emission sites are structural, not discretionary, because each answers the standing
diagnostic question of its chapter. **State machines log transitions**: "how did we get here"
is answered by the recorder (§6.1). **Boundaries log crossings** — at ports, the event in, the
decision out, post-validation — so what the component actually saw is on the record; that is
the arch manifest's observable-boundaries rule, and the decision log of §4.2 makes it nearly
free. **Counters cover rates** — queue high-water marks, drops, retries, bucket levels, pool
and stack watermarks — because a counter read periodically answers the counting questions a
log line per event answers expensively; the house observability law transposes verbatim: that
is a metric implemented in the most expensive medium available. `heartbeat` and the health surface report
liveness per activity, feeding the watchdog check-in map of §8.4 — one mechanism, two
consumers: the recorder trends it, the watchdog enforces it.

### 11.4 The maintenance interface

Hanmer's `maintenance-interface`, which the architecture catalog carries with its rationale:
administration and diagnosis travel on a channel *distinct from* the functional interface,
because mixing them obscures both and blocks maintenance exactly when the service path is
congested or broken. In embedded practice: the debug CLI, the diagnostic protocol endpoint, the
engineering-mode screen — read-only by default, with `specialized-interfaces` (Bass: the
set/dump/reset surfaces) behind it, and the mutating members gated and reviewed as production
API. C's compilation model grants what the tactic asks as a matter of course:
the surface is *genuinely removable* — compiled out by build configuration — so the shipping
decision is explicit, per variant, and the shipped configuration is the tested configuration
(invariant 21). Bass's own cost note — shipping code that differs from tested code is
problematic in exactly this domain — is the reason the decision is a recorded one, not a
default. `built-in-self-test` reports here; `correcting-audits` run from here; the crash record
of §11.1 is retrieved through here.

### 11.5 The hostile reader

The surfaces this Part builds — trace, persisted records, a maintenance channel that can dump
and mutate state — assume a friendly reader. Ship enough units for enough years and the reader
is eventually hostile, and the update path of chapter 14 is the most valuable door on the
device. Security is not a separate structure in this booklet because it is not a separate
structure in the system: it is the *same boundaries under a threat model*, and the threat model
belongs to the specialization. What the parent owns is where the controls attach.

The update
path authenticates what it boots (`secure-boot-image-verification`, with rollback protection —
chapter 14). The maintenance surface authenticates and authorizes before anything mutating, and
its ship/no-ship matrix (§11.4) is a security decision, not only a size one. The trace and the
crash record never carry secrets — keys, credentials, personal data — and the enforcement is
structural, never-emitted rather than filtered later. Secrets end their lives through
`secure-zeroization` — an erase the optimizer must not elide, which ordinary C cannot express,
so it lives in the compiler port — and are compared in constant time
(`constant-time-comparison`) at cryptographic boundaries.

Protection hardware adds depth in the
§5.5 sense — MPU regions, `privilege-separation-arch` between the critical and the convenient,
a `trusted-execution-environment` where the silicon offers one — layered per
`defense-in-depth`, never load-bearing alone. *(image authentication including its rejection
paths: host- and target-test-catchable; a canary secret driven through the trace pipeline:
host-test-catchable; zeroization: analysis-catchable + contract-only — the optimizer is the
adversary there, and
the booklet says so rather than pretending a rule catches it)*

Decisions Part V leaves to the specialization: the error-code registry and its structure; the
assert policy per build variant; the safe-state definitions per hazard; the escalation gates
and their thresholds; the trace event schema, buffer sizes, transports, and retention; the
persisted-record format and its region; the maintenance surface's transport, protocol, and
ship/no-ship matrix. *(chapter 15)*

---

# Part VI — Verification

## 12. Testability as a structural property

### 12.1 Two targets from day one

The single practice that most changes an embedded project's trajectory is the one Grenning's
*Test-Driven Development for Embedded C* built its method on: **the code runs on the host before
it runs on the target, and forever after runs on both.** The host build is a first-class product
of the repository — same core sources, adapters swapped for fakes, executed per commit in
milliseconds — and the cross build proves the same contracts on the metal at release cadence.
What makes this possible is not tooling but the structure already built: chapter 4's core has no
hardware on its include path *by construction*, so the "port to the host" is not a port at all;
it is the second adapter set, and the first proof that the target really is a port.

The dual-target discipline also quietly delivers a second compilation environment and a second
word size — a second diagnostic *opinion* when the host compiler family differs from the cross
family (choose it so it differs; §13.1) and a standing rebuke to accidental
implementation-defined assumptions (§5.2). Its honest cost: the host cannot test timing,
register behavior, the compiler's target codegen, or core semantics that legally follow the
target's pinned implementation-defined properties — integer promotions on a sixteen-bit-`int`
target being the classic, and the breach §4.2's determinism condition exists to exclude —
which is the residue the target-test rungs exist for (§12.5), and
the reason neither rung substitutes for the other.

### 12.2 Seams, named by mechanism

A seam is where a test substitutes a collaborator without editing the code. The corpus is
deliberate here in a way the booklet preserves: there is no "seam" element — a seam is a
*property*, and the reviewable claim is the **mechanism** that creates one. The C repertoire,
each with its binding time from §5.4:

- **The link seam** — same header, different object file; the test links the fake. This is C's
  native seam, it costs nothing at runtime, and the corpus's `facade-backend-module-pattern`
  records it as a first-class pattern whose own problem statement says the quiet part: *the seam
  is moved to the build.* Default for whole-subsystem substitution (the HAL under test, the fake
  transport).
- **The function-pointer seam** — the port-struct form of §4.3, substituted at initialization.
  Default where two implementations must coexist (recorder wrapping driver; per-instance
  doubles), and the C spelling of `dependency-injection` — the corpus's element, whose C forms
  are exactly these tables plus `callback-with-context-pointer`.
- **The preprocessing seam** — include-path override or macro substitution. The weakest and most
  dangerous form (it changes the text, not the binding); reserved for taming vendor headers at
  the outermost adapter fringe, never used inward of a port.
- **The hardware seam** — `hardware-proxy` and `hardware-adapter` (Douglass) are the catalog's
  names for the register-facing module shaped so a double can stand where the silicon was; the
  test double for hardware is just the third implementation of a port that already had two.

"We inject the clock through the time port, bound at init" is reviewable; "this module is
testable" is not. Every module's spec names its seams by mechanism. *(contract-only, and
reviewed as such)*

### 12.3 Doubles with a discipline

The corpus collapses dummy/fake/stub/spy/mock into **one element on one dial — behavioral
sophistication — and the rule is to take the least behavior that still asserts the contract.**
Three consequences for embedded practice. First, the workhorse is the *fake*: a small honest
implementation of the port (the RAM flash, the scripted bus, the recorded sensor) — and a fake
earns the word only if the **same contract test suite runs against the fake and the real
adapter** — partitioned honestly: the nominal-and-reachable cases run against both; the fault
cases (§12.5) run against the fake by construction, and against silicon only where a rig can
produce the condition, with the partition recorded per port. Host-run against the fake,
target-run against the silicon-backed adapter, this is precisely how the host/target split of
§12.1 is kept honest, and the sharpest use of the target-test budget there is.

Second, substitution has **three reasons with three exit
criteria** (the corpus's testability-tactic mapping): virtualize an uncontrollable resource
(`sandbox` — done when the resource is consequence-free and drivable to any state); remove
behavioral variance (`limit-nondeterminism` — done when reruns agree); supply controlled inputs
(`abstract-data-sources` — done when the contract's input partitions are covered). A double with
no stated reason has no finish line and grows into a second implementation.

Third, mock-style
call-verification is reserved for the rare port whose *interaction is* the contract (command
ordering on a bus); everywhere else, assert on decisions and state, not on choreography.

### 12.4 The shape of the suite

The suite's shape is derived from the architecture, not from a pyramid diagram: **the functional
core gets many fast unit tests; the shell gets fewer integration tests** — because the core is
pure (no doubles needed at all: inputs in, decisions compared) and the shell is thin *in
logic* even where it is large in lines (§4.5): its bulk is adapters, adapter verification
lives in §12.3's per-port contract suites, and the "fewer" refers to cross-component
integration tests, not to that tier. The
constructs are cataloged and carry their tactic: `four-phase-test` (setup, exercise, verify,
teardown — one behavior per test); `test-data-builder` over `object-mother` for state
construction (make the significant values explicit, default the rest — and §6.1's
localize-state-storage is what makes "construct the state" possible at all);
`parameterized-test` tables for protocol and boundary matrices; `property-based-testing` on the
pure core for the properties tables cannot enumerate — round-trips (encode/decode, the framing
vocabulary of §9.5's records), invariants (the state machine never leaves its legal set),
oracles (the fixed-point filter against a floating reference). Numeric assertions name their
tolerance, epsilon-or-ULP, because a fixed absolute epsilon is wrong across magnitudes
(the corpus carries the Dawson/Goldberg lineage for exactly this).

Regression has a domain-native form: **golden-master testing over the decision log.** Chapter
4's effect values and chapter 11's trace are canonical, replayable records; a scenario's
recorded event sequence is fed to the core, and the emitted decision/trace stream is compared
against an approved master — with the corpus's stated precondition honored (canonical
serialization: stable ordering, normalized timestamps) and the approve-the-diff step explicit,
because a snapshot suite with auto-approval is a change-recorder that can never fail. This is
`record-playback` (Bass) and `golden-master-testing` (Feathers' characterization lineage)
composed — record at the ports, replay into the core, diff the decisions — and it is the
mechanism that turns a field trace into tomorrow's regression test. `deterministic-lockstep`
(the corpus's strongest determinism claim) is reachable *because* the core is pure and time is
injected. Seed plus ordered input log yields a bit-identical run, on the bench, of what
happened in the field — across platforms exactly under §4.2's conditions, promotion-safe
integer arithmetic and a pinned FP discipline; otherwise the replay claim is scoped to
same-platform runs, and the suite says so rather than assuming it.

### 12.5 Fault injection, and the ladder above the host

Error paths are the product (chapter 10), so they are tested as the product: every port's fake
**injects faults by design** — timeouts, NAKs, corrupt frames, exhausted pools, brown-out
mid-write — driven by the same scripting that drives nominal data; every escalation rung of
§10.4 is exercised on the host (the reset "reboot" faked at the shell); the persisted-record
path is tested by killing and rebooting the host process.

The corpus's element layer is
deliberately silent here — fault injection is practice, not mechanism, and its exclusion
register says so — so this section is booklet-editorial, grounded in the port structure that
makes it mechanical rather than heroic.

Above the host sit the rungs the host cannot reach,
each with its distinct residue: **simulation** (instruction-set or peripheral simulation, where
the specialization has one) for timing-shaped logic without hardware scarcity; **target smoke**
— boot, self-test, port liveness — per merge; **hardware-in-the-loop** for the closed loop
against real or simulated plant physics, per release; and the field itself, whose recorder
(chapter 11) is the last test harness, permanently deployed. Coverage is read as a diagnostic
and never gated as a target (unexecuted code is a fact; executed code is not verified code) —
where a safety standard demands structural coverage evidence, the specialization pins the
criterion and the tooling, and the corpus carries the MC/DC lineage for when that day comes.

## 13. The enforcement ladder

### 13.1 The build is the law

Chapter 2 stated the thesis; this chapter is its machinery. Everything the booklet has ruled is
enforced somewhere on a ladder ordered by cost-of-catch, and the specialization's first
deliverable is this ladder, pinned and dated. What follows names each rung's *class* and what
rides on it; the concrete tools, versions, flag sets, and rule codes are child facts by
definition — with two house meta-rules inherited verbatim: **where a claim is about what a tool
does, run the tool** (documentation states intent; the resolved behavior is the fact), and
**never invent an identifier** — a fabricated rule code or flag pasted into a build silently
disables a check.

1. **The compiler, promoted.** Diagnostics are policy: the build runs at the toolchain's serious
   diagnostic level with warnings fatal, and every suppression is local, justified, and visible.
   The dual-target rule doubles this rung when the host family differs from the cross family —
   choose it so it differs, and two frontends disagree productively at near-zero cost.
2. **Static analysis, pinned.** Three genres, adopted by name in the child: the
   *safe-subset genre* (MISRA-C-shaped rule sets — with the compliance discipline the corpus
   records alongside: a pinned baseline, and **deviation records** rather than silent
   suppressions, because the corpus also carries the contested-effectiveness evidence, and
   cargo-cult compliance is not the goal; the rules are a vocabulary for *decisions*); the
   *flight-rules genre* (Power-of-Ten-shaped: bounded loops, bounded stack, no post-init
   allocation — each rule mirroring an invariant this booklet already states structurally); the
   *security genre* (CERT-C-shaped) where the attack surface warrants. Plus the mechanical
   checkers of this booklet's own rules: unchecked returns, prefix discipline, `#ifdef`
   confinement to designated files (the *selection* judgment behind each variation point stays
   contract-only, §5.3), ownership annotations where supported.
3. **The build graph.** Include-graph levelization and layer rules (§3.3); symbol-visibility
   audit (exports equal headers); the variant matrix actually built — every shipped `#ifdef`
   combination compiles and tests, or it is fiction (§5.4).
4. **Budgets as fitness functions.** The link map gated against the RAM/flash budget; stack
   bounds by static analysis where the toolchain gives it, indirect-call target sets supplied
   (§4.3) — and where it does not, a trapped guard to catch the excursion, with the watermark
   trend as drift warning, never as the bound; queue high-water marks and WCET measurements
   trended across builds with alarms on
   regression; and the budgets the body declares, collected here — startup-to-operational time
   (§4.6), interrupt-masking latency (§7.2), energy per mode (§6.4). A budget checked once is a snapshot; a budget trended is an early-warning system.
5. **The host suite** (chapter 12), per commit — including the sanitizer families the host
   toolchain offers (address, undefined-behavior): running the core under a UB sanitizer on the
   host is the cheapest UB detection the C world has, and one more dividend of dual-target.
6. **The target rungs**, per cadence: smoke, contract-on-target, HIL, with their budgets
   (§12.5).
7. **Runtime enforcement in the field** — field asserts, CRCs, canaries, watermarks, the
   watchdog, MPU traps where hardware exists (§5.5) — the last rung, whose firings are not
   failures of the ladder but its final, instrumented net, feeding chapter 11's evidence chain.

### 13.2 The contract-only register

What no machine checks is reviewed *by name* — the booklet's honest list, gathered from its own
chapters: responsibility boundaries drawn by secrets (§2.1); port vocabulary staying the core's,
not the vendor's (§4.3); ownership statements present and true in every header (§9.2);
detect/decide/act placement (§10.3); seam mechanisms named in specs (§12.2); the decision to
descend the allocation ladder (§9.1) or bind late (§5.4); message and effect vocabularies
staying honest as the system grows; the hidden wall-clock read the injected-time rule forbids
(§8.1); each channel's declared execution environment (§7.4); ADR linkage and context-map
upkeep (§3.8). Review is not the weak rung; it is the rung for what only
judgment can see — but it is *scheduled, chartered* judgment: each item above appears on the
review checklist as a question, so the contract-only register is maintained the way the
machine-checked rules are maintained, and additions to it are as deliberate as additions to the
rule set. A rule that is on neither list — no enforcer, no checklist — does not exist.

---

# Part VII — Evolution and the family

## 14. Changing a system that is awake

Twenty years of service means the program is changed more often than it is written. Three change
surfaces carry almost all of the risk, and each has named machinery.

**Interfaces change by parallel phases.** The expand/migrate/contract shape (the house's module
manifest states it; the arch manifest's parallel-change entry is its refactoring-catalog form):
introduce the new alongside the old, migrate callers incrementally with both alive, remove the
old when its callers are provably gone — "provably" meaning the deprecation is *visible*: a
compile-time deprecation marking through the compiler port, an analysis rule making new uses
fatal in CI, and a stated removal release. A deprecation nobody's build fails on is not a
deprecation. The error-code registry (§10.1) and the trace schema (§11.2) are interfaces under
this rule — their consumers are just further away.

**Data outlives code.** Everything persistent or wire-crossing carries a version: the flash
records of §9.5, the frames of the protocol vocabulary, the persisted crash record, the
calibration tables. The corpus supplies the wire-level machinery (TLV encodings that skip the
unknown, length-prefix framing, `tolerant-reader` as the consumer's posture) and the update
cluster makes the requirement concrete: after an A/B swap, the *new* firmware reads the *old*
firmware's persisted state — or migrates it explicitly, or declares it lost by design. That
sentence is tested on the bench before every release that touches a persistent layout
(host-testable, §12.5's kill-and-reboot machinery).

**The image changes under supervision.** Firmware update is architecture, not afterthought, and
the corpus carries it whole: `bootloader-application-split` (the rarely-changed boot stage that
validates, selects, and jumps), `a-b-firmware-image-update` (write inactive slot, verify,
atomic switch, old image as instant fallback), `secure-boot-image-verification` where the
threat model demands, and the deployment vocabulary — staged rollout, the update that can
always roll back, the golden image — inherited from `deployment-pipeline` thinking with the
fleet in place of the server pool. The recovery ladder's last rung (§10.4) and the update
system share the bootloader; designing them together is what makes "reboot" a safe verb.
Two identity obligations ride with the image. Every shipped image carries its own identity —
version, build id — where the crash record and the maintenance surface can read it (§11.1).
And every shipped image remains reconstructible, or its decode artifacts archived, for as long
as the fleet lives — a recorder whose output can no longer be read against its build is a
flight recorder without a decoder; the mechanism is the child's (ch. 15).

The boot stage itself is a system under this booklet — it decides, it writes flash, it can
hang — so the rules recurse: it gets evidence (§11.1's region is often all it has), a safe
state (refusing to boot a bad image beats booting it), and watchdog coverage (§4.6). It
survives the recursion by being deliberately minimal, small enough that most chapters
discharge trivially; and its own update is the riskiest decision a fielded fleet faces —
named, child-pinned, defaulting to immutable-plus-golden-image.

For code that predates its tests, the legacy playbook transposes unchanged: characterization
via the golden-master machinery of §12.4 (record what crosses the ports of the code as it *is*,
pin it, then refactor inside the pinned behavior), seams introduced at the least-invasive
mechanism first (link seams cost nothing), and the strangler shape at subsystem scale — route
new work through the new module, drain the old. The change-scenario test of §2.1 is re-run
periodically against the repository's actual co-change history; where one likely change touches
many modules, the boundaries have drifted, and the finding is an ADR-worthy event, not a
failing.

## 15. The specialization contract

This booklet is the parent. A **specialization** is a child document set that binds these
principles to named, dated facts for one context — a company, a product line, a target family,
a certification regime. The relationship is a contract with three clauses.

**What the parent owns and children must not weaken.** The invariants of Part I; the enforcement
thesis (every rule routed or registered contract-only); the effect boundary; the ownership
language; the evidence chain. A child may *tighten* any of these (a safety profile forbidding
the allocation ladder below rung 2; a certification regime mandating MC/DC) and may extend the
vocabulary; a child that relaxes an invariant is not a specialization but a fork, and says so
honestly or is wrong.

**What children must pin.** The chapters have surfaced their open decisions as they went;
gathered here and reconciled against each chapter-end register, they are the child's table of
contents:

| child owns | the decisions |
|---|---|
| **platform contract** | target family; widths, alignment, endianness assumptions and their checks; memory map; MPU/MMU region policy; the compiler-port header set and extension inventory |
| **toolchain baseline** | compilers and versions; the promoted diagnostic set; analysis tools, rule baselines, and the deviation record; build system; the include-graph checker; the prefix registry and symbol-visibility mechanism; the contract-generator toolchain and the view-generation tooling with its cadence; build identity, reproducibility, and artifact-archival policy |
| **execution shell** | superloop / time-triggered / RTOS choice and version; the task and queue inventory with depths, priorities, overflow policies; the lock inventory and ordering where locks exist; the schedulability analysis and its inputs; tick source and timestamp format; the composition-root init order and startup budget; the idle/power mode map and energy budget |
| **HAL & ports** | the port list with naming and contracts; the adapter inventory per board; the variant matrix the build must build |
| **memory plan** | allocation rung per component; pool and stack budget tables; allocator choice if any; flash endurance arithmetic |
| **failure policy** | error-code registry; assert policy per variant; safe-states per hazard; escalation gates; watchdog topology — boot-phase coverage included — and check-in map; the arithmetic overflow policy per subsystem |
| **observability plan** | trace schema and budgets; transports; persisted-record format; maintenance-surface protocol and ship matrix |
| **verification plan** | host and target suites' scope; the contract-suite inventory per port; simulation/HIL rigs; coverage criterion where mandated; CI shape and cadences |
| **security posture** | the threat model; image-signing and rollback-protection scheme; maintenance-surface authentication and authorization; secret storage, the zeroization inventory, and the debug-port lockdown policy; the inter-core memory model where cores share state |
| **process bindings** | the certification standard's mapping onto these chapters, where one applies; review checklist for the contract-only register; the update/rollout policy |

**How children stay honest.** Three rules inherited from the house families, stated here as
obligations. *One version hub per family*: every dated fact (tool versions, standard editions,
silicon errata) lives in a single child document with a verification date and re-check triggers;
sibling documents state behavior and defer — if a version fact elsewhere disagrees with the hub,
the hub wins and that document is stale. *Epistemic tags on claims*: a child asserting a tool
behavior marks it measured (with the command), documented, or assumed — and an OPEN decision is
surfaced, never improvised silently. *Specs before code where reuse or risk warrants*: child
specifications follow the house spec discipline — contract not computation, atomic verifiable
requirements, falsification before acceptance, decisions logged with dissent preserved.

The genealogy, for orientation: the house's domain-agnostic architecture manifest is this
booklet's parent in spirit — its vocabulary, tactic catalog, and tradeoff axes are assumed
here, instantiated for this domain rather than repeated. This booklet stands to a future
`embedded_manifests/` family as the web and Python grounds' architecture files stand to
theirs: the reasoning root its children cite instead of re-arguing.

## 16. Lineage

### 16.1 How this register works

Names in `this-face` throughout the booklet are element identifiers from the house element
catalogs — 709 design elements and 374 architecture elements, joined by 2,811 typed relations
(1,023 of them sourced to literature, 1,788 marked editorial judgments; the booklet uses both
and trusts the corpus's marking). The works below are recorded **as the corpus records them**:
"verified" means a primary or publisher page was loaded live during corpus compilation
confirming the identifier — it does not attest page numbers or quotations. **UNVERIFIED** is
the corpus's own flag and travels with the work here; those entries are real leads whose
bibliographic records could not be confirmed against a primary page, and a specialization that
leans on one re-verifies it first. Where this booklet asserts something the corpus does not
carry, §16.3 says so.

### 16.2 The works

**Roots and architecture canon.**

| work | corpus id | standing here |
|---|---|---|
| Parnas, *On the Criteria To Be Used in Decomposing Systems into Modules* (1972); Parnas & Clements, *A Rational Design Process* (1986) | `parnas72` · `parnasclements` | verified — the information-hiding root (ch. 2) and the documented-rationality ideal behind the ADR discipline |
| Bass, Clements & Kazman, *Software Architecture in Practice*, 4th ed. (2021) | `bck` | verified — the tactic vocabulary used throughout: modifiability, testability, performance, availability, energy |
| Cockburn, *Hexagonal Architecture* (2005) | `hexagonalarch` | verified — the ports-and-adapters frame of ch. 4 |
| Buschmann et al., *POSA Vol. 1* (1996); Schmidt et al., *POSA Vol. 2*; Kircher & Jain, *POSA Vol. 3* (2004); Buschmann, Henney & Schmidt, *POSA Vol. 4* (2007) | `posa1` · `posa2` · `posa3` · `posa4` | posa1/posa4 verified; **posa2 and posa3 UNVERIFIED** (posa2's year unresolved) — active object, reactor, half-sync/half-async, wrapper facade, strategized/scoped locking, pooling, and eager acquisition ride on them; re-verify before load-bearing use |
| Gamma, Helm, Johnson & Vlissides, *Design Patterns* (1994); Fowler, *PoEAA* (2002) & *DI article* (2004); Evans, *DDD* (2003); Hohpe & Woolf, *EIP* (2003) | `gof` · `poeaa` · `fowlerdi` · `evansddd` · `hohpe` | verified — gateway, separated interface, plugin, mediator, correlation identifier, message vocabulary |
| Clements et al., *Documenting Software Architectures: Views and Beyond*, 2nd ed. (2010); ISO/IEC/IEEE 42010:2022; Nygard, *Documenting Architecture Decisions* (2011) | `vab` · `iso42010` · `nygardadr` | verified — module/C&C/allocation views, viewpoint discipline, ADRs (§3.3, §10.3, ch. 14) |
| Bernhardt, *Functional Core, Imperative Shell* (2012); Reynolds, *Definitional Interpreters* (1972); Candea & Fox, *Crash-Only Software* (2003) | `bernhardtfcis` · `reynolds72` · `candeafox` | verified — the effect boundary's naming (ch. 4), defunctionalized decisions, reset as recovery |

**The embedded canon.**

| work | corpus id | standing here |
|---|---|---|
| Kopetz & Steiner, *Real-Time Systems: Design Principles for Distributed Embedded Applications* (2022) | `kopetz` | verified — event- vs time-triggered, temporal firewall, fault-containment regions (chs. 6, 7, 10) |
| Samek, *Practical UML Statecharts in C/C++*, 2nd ed. (2008), course & QP framework | `samekbook` · `samekcourse` · `qpc` | verified — run-to-completion, HSMs, active objects: the spine of ch. 6 |
| Douglass, *Design Patterns for Embedded Systems in C* (2011; the C-pass record dates it 2010); *Real-Time Design Patterns* corpus (2002) | `douglasspatternsc` · `douglassrtcorpus` | verified — event receptors, critical regions, ceiling protocol, static/pool allocation, sanity check, watchdog, safety patterns (chs. 6–11) |
| White, *Making Embedded Systems*, 2nd ed. (2024) | `white` | verified — ring buffers, DMA, system tick, core dump, chained processors (chs. 7, 9, 11); note: two catalog entries carry an unexpanded `named-in: white` data defect |
| Koopman, *Better Embedded System Software* (2010) | `koopmanbess` | verified — the watchdog chapter (kick discipline, what it cannot detect) and the reset chapter behind §8.4 and §11.1 |
| Grenning, *Test-Driven Development for Embedded C* (2011) | `grenningtdd` | verified — dual-target discipline, doubles in C, design-for-test (ch. 12); the corpus files the practice at process layer, deliberately |
| Preschern, *Fluent C* (2022); EuroPLoP pattern papers | `preschern` · `preschernplop` | book verified; **papers UNVERIFIED** — module shapes, ownership vocabulary, cleanup, status returns, samurai principle, escalation, `#ifdef` escape (chs. 3, 9, 10) |
| Hanson, *C Interfaces and Implementations* (1996); Schreiner, *OOP with ANSI-C* (1993/2011); Kernighan & Ritchie, 2nd ed. (1988) | `hanson` · `schreiner` · `kandr` | verified — opaque pointer, arenas, setjmp exception frames; OO-in-C; function-pointer dispatch (§3.2, §4.3, §9.1) |
| Noble & Weir, *Small Memory Software* (2000) | `noblesmallmem` | verified — memory limits, discard, packing, ROM placement, Captain Oates (ch. 9) |
| Beningo, *Reusable Firmware Development* (2017); Simmonds, *Mastering Embedded Linux Programming*, 3rd ed. (2021); Corbet et al., *LDD3* (2005); Yiu, Cortex-M guide (2013); Arm CMSIS | `beningofw` · `simmonds` · `ldd3` · `yiu` · `cmsis` | verified — HAL and BSP naming (ch. 5), drivers, `container_of`, vector tables, nested interrupts |
| Simon, *An Embedded Software Primer* (1999); Pont, *Patterns for Time-Triggered Embedded Systems* (2001); Labrosse (µC/OS-III; *Embedded Systems Building Blocks*); *Mastering the FreeRTOS Real-Time Kernel* | `dsimonprimer` · `pont` · `labrosse` · `freertosbook` | **all four UNVERIFIED as bibliographic records** — yet they are the named-in sources for the shell menu, interrupt-masking sections, multi-state tasks, loop timeouts, mailboxes, event groups, software timers, stack painting, tickless idle and the idle hook (chs. 6–9); the highest-value re-verification targets this booklet has |
| Memfault, *From Zero to main()* series (2019); *Device Firmware Update Cookbook* | `zerotomain` · `memfaultea` | zerotomain verified; **memfaultea UNVERIFIED** — bootloader handoff and A/B update (ch. 14) |
| Saks, memory-mapped-device columns; Smith, *C++ Hardware Register Access Redux* (2010); Eide & Regehr, *Volatiles Are Miscompiled* (2008) | `sakscolumns` · `kensmith` · `eideregehr` | kensmith verified; **sakscolumns, eideregehr UNVERIFIED** — the register-access discipline and its hazard literature (§7.2) |

**Standards and rule sets** (all verified as records; editions are child-hub facts, not booklet facts): MISRA C and the MISRA Compliance framework with its deviation records (`misrac` · `misracompliance`), BARR-C (`barrc`), NASA/JPL institutional standard embedding the Power of Ten (`jplstd` · `holzmannp10`), CERT C (`certc`), ISO 26262 (`iso26262` — safe state), IEC 61508 incl. the Part-7 technique catalog (`iec61508` — program-sequence monitoring, BIST, MooN), DO-178C (`do178c`), ARINC 653 (`arinc653` — time and space partitioning), AUTOSAR Classic/Adaptive (`autosarclassic` · `autosaradaptive` — the generated-RTE worked example), ISO/IEC TR 18015 (`tr18015` — the C++ performance cost model and `iohw` register abstraction), ISO/IEC 9899 (the C standard; C23's checked arithmetic is the catalog's `checked-arithmetic` anchor). The corpus also carries the *contested* effectiveness evidence for rule-set compliance (`boogerdmoonen` 2009; `hattonsubset` 2004; `hatton95`) — imported in §13.1 as the reason baselines are pinned with deviations rather than worshipped.

**Real-time scheduling.** Liu & Layland (1973, `liulayland`, verified); Buttazzo (4th ed. 2023, `buttazzo`, verified); Sha, Rajkumar & Lehoczky (1990 — the ceiling/inheritance source, named-in for the design elements); and — recorded in the sibling netsim corpus's scheduling keystones rather than SWE — Joseph & Pandya (1986) and Audsley et al. (1993) for response-time analysis, Leung & Whitehead (1982) for deadline-monotonic ordering (§8.2). Timer machinery: Varghese & Lauck timing wheels (1987, verified); Pont, Kurian & Bautista-Quintero sandwich delays (2009, verified); Ganssle's debounce guide (2004, verified); Mogul & Ramakrishnan receive livelock (1996, verified); RFC 1982 serial-number arithmetic (verified); Wescott, *PID Without a PhD* (2000, verified). Deadline propagation (§8.3) is sourced to the
SRE volume — Beyer, Jones, Petoff & Murphy, eds. (2016, `googlesre`, verified).

**Inter-core and memory-ordering mechanics** (§7.4): `memory-barrier` (the kernel
memory-barriers document), `acquire-release-ordering` (Preshing, 2012),
`false-sharing-avoidance-via-cache-line-padding` (Drepper, 2007 — **the corpus record is
UNVERIFIED**), `dual-core-lockstep` (Arm Cortex-R technical reference). **Security attachments**
(§11.5): `secure-boot-image-verification` (MCUboot/verified-boot documentation lineage),
`secure-zeroization` (Seacord's CERT C treatment — `certc` above), `constant-time-comparison`
(named-in: Pornin's BearSSL constant-time documentation), `privilege-separation-arch` (Provos,
Friedl & Honeyman, 2003), `defense-in-depth` (Schumacher et al., 2006), and
`trusted-execution-environment` (the GlobalPlatform TEE system architecture, living) — recorded
as the catalogs record them; the security *process* canon is deliberately absent from this
booklet and child-owned.

**Fault tolerance and errors.** Hanmer, *Patterns for Fault Tolerant Software* — the architecture catalog dates it 2007; **the design-corpus bibliographic record is UNVERIFIED with year unresolved**, and it is the naming source for a large slice of ch. 10 (escalation, restart, riding-over-transients, leaky bucket, marked data, quarantine, maintenance interface, units of mitigation, someone-in-charge) — first in line for re-verification. Nygard, *Release It!* — **UNVERIFIED, year unresolved** (timeout, fail-fast, let-it-crash, steady state, bulkhead). Cunningham's CHECKS (1994, verified — exceptional value, deferred validation); Meyer's design-by-contract (the element's named-in cites the 1988 edition; the corpus work record is the 1997 second edition — carry the discrepancy); Kuhn, Hanafee & Allen (2017, verified — error kernel); Erlang/OTP design principles (verified — supervision); Hamming (1950 — ECC); Cowan et al., StackGuard (1998 — stack canary); Atmel/Microchip AVR180 (brown-out); ST AN2594 (EEPROM emulation; **url unresolved** in the corpus record).

**Testing and verification.** Meszaros (2007, verified — doubles, four-phase, humble object, fixtures); Feathers (2004, verified — characterization/golden master; also the seam concept the catalogs deliberately hold as a property, not an element); Freeman & Pryce (2009) and Pryce's builder-vs-object-mother tradeoff; Claessen & Hughes' QuickCheck (2000, verified); Dawson (2012) and Goldberg (1991) for float comparison; Unity/CMock/Ceedling (verified — the C xUnit lineage the specialization will pin or reject); Chilenski & Miller (1994) and the NASA MC/DC tutorial (2001), both verified, held in reserve for certification-grade coverage; Lamport (1977) for the SPSC correctness lineage.

**Memory and systems.** TLSF (Masmano et al., 2004, verified); Knuth TAOCP (buddy systems, sentinels); Levine, *Linkers and Loaders* (1999) and the linker/ELF/DWARF tooling shelf of the emb-ops pass (the mechanics behind §13.1's build-graph and budget gates); Lakos's physical design (`lakosvol1` 2019 verified; `lakoslsc` **UNVERIFIED, year unresolved** — cited in ch. 3 for levelization as a works-layer anchor; the catalogs carry no physical-design elements, see §16.3).

### 16.3 Where the corpus is silent, and this booklet is the source

Honest accounting of the booklet's editorial layer — claims grounded in the corpus's *parts* but
composed here, or explicitly absent from the catalogs:

- **The flight-recorder composition** (§11.1–11.2): ring buffer + structured events + persisted
  crash record + reset-cause autopsy. The corpus carries every part and its own gap notes
  ("missing a postmortem-diagnostics arch element"; ring-buffer logging "has no established
  mechanism name independent of products"). The composition and its obligations are editorial.
- **Fault injection as a designed port property** (§12.5): the catalogs deliberately exclude
  fault injection, fuzzing, and mutation testing from the element layer (two with empty
  rationale fields — unadjudicated, not rejected). The obligation stated here is editorial,
  standing on the port structure and on Grenning's practice layer.
- **MPU/MMU boundary mapping** (§5.5, §9.4): the design catalog's own exclusion note — MPU task
  isolation is "real practice with no single established element name across vendors." The
  enforcement-depth framing is editorial; `time-and-space-partitioning` (ARINC 653) is its
  industrialized, cataloged endpoint.
- **Practice-layer obligations the catalogs route to process**: reset-cause handling, interrupt
  latency budgeting, watchdog kick placement, linker-script discipline, dual-target testing
  itself — all appear in the catalogs' exclusion registers as practices, not mechanisms. This
  booklet states them as obligations anyway, because a parent of specializations is exactly the
  document practices belong in; their absence from the element layer is by that layer's charter,
  not evidence against them.
- **Vocabulary this booklet declined**: coupling metrics and connascence (no corpus vocabulary);
  the test pyramid as a shape (absent from the ontology; the two-tier core/shell shape is the
  house testing manifest's committed form and is used instead); "seam" as a noun-artifact
  (refused by the catalog's strictness round; §12.2 names mechanisms instead).

### 16.4 Colophon

*Architecture and Design of Complex Embedded C Programs — the parent booklet*, revision r1.5,
compiled 2026-08-11, revised through 2026-08-12, against: SWE element catalogs v1.0 (709 + 374 elements), element bridge
v1.1 (2,811 relations), SWE process corpus v1.0 (pass 7), design-elements corpus v1.0 (pass 8),
the six SWE research-pass reports, the house manifest families (`manifests/` python-agent-ground
2026.08.08; `web_manifests/` mid-2026), and the netsim scheduling keystones. Element identifiers
resolve in `SWE/explorer/data/elements.json`; work records in `SWE/explorer/data/corpus.json`.
Judgments not carried by those sources are marked editorial in place or registered in §16.3.
This file carries no version-dependent facts, on purpose; the specialization contract (ch. 15)
says where such facts must live. Verify before trusting; route before relying; and when a rule
here meets a situation it does not fit — reason past it, and say so.

**Revision history.** The booklet's own audit gate is
`_embedded_booklet_work/audit.py` — element ids, work ids and their verification stances, and
all internal cross-references are machine-checked against the corpus data before each revision
is sealed.

- **r1.0** (2026-08-11) — initial edition.
- **r1.1** (2026-08-11) — ground-truth audit mechanized and run: 144 element ids and 79 work
  ids verified against `elements.json`/`corpus.json`; fixed one truncated element id
  (`facade-backend-module-pattern`), corrected POSA Vol. 3's verification stance to UNVERIFIED,
  recorded the Douglass 2010/2011 pass discrepancy, and narrowed the front matter's claim about
  what backticks denote.
- **r1.2** (2026-08-12) — adversarial technical review: three independent reviewers (real-time
  and concurrency; memory, failure, and observability; modularity, toolchain, and verification)
  chartered to refute. 33 findings, all accepted: 3 critical (the SPSC channel's visibility and
  publication-ordering obligations, previously omitted; the volatile/barrier partition, which
  wrongly confined completion hazards to multi-master; the opaque-storage technique's
  effective-type violation — undefined behavior by §5.2's own absolute, now carrying its
  discharges), 7 major (bare double-buffer coherence, external-arrival pool exhaustion vs
  invariant 11, watermark-as-worst-case, "provable" flash atomicity, unconditional
  floating-point determinism, include-path-as-enforcement, same-family "second compiler"),
  23 precision fixes. Adjudication record:
  `_embedded_booklet_work/reviews/r1.2_adjudication.md`.
- **r1.3** (2026-08-12) — coverage: five sections the first edition lacked. §3.8 the boundary
  documented (three views, ADRs, context map); §4.6 the composition root (ordered bring-up, the
  one place that knows the inventory); §6.4 the idle architecture (tickless idle, power states
  as states, energy as a budget); §7.4 the second master (inter-core message-passing default,
  the imported memory model, lockstep disambiguated); §11.5 the hostile reader (security as the
  same boundaries under a child-owned threat model). Invariant 25 added; specialization table
  gains the security-posture row; lineage extended accordingly.
- **r1.4** (2026-08-12) — coherence: the activity/task vocabulary fixed at first use; the §3.2
  resolutions restructured into a priced list; the densest sentences split (§5.1, §7.3, §8.2,
  §10.5, §11.1–11.3, §12.4) and the new sections paragraphed; the "twenty years" leitmotif
  thinned to its two load-bearing occurrences; residual double-conjunctions from the r1.2
  surgery smoothed.
- **r1.5** (2026-08-12) — cold-read convergence: one fresh-eyes architect over the whole text,
  twelve findings, all applied. The integer half of the determinism claim conditioned on
  promotion-safe arithmetic (it had contradicted §12.1); the composition root's bring-up order
  rewritten — watchdog framed first, destructive self-test before RAM is live, evidence
  harvested before the march; the chapter-15 table and chapter-13 registers reconciled against
  the chapter-end registers they claim to gather; route tags normalized to the seven names;
  firmware identity added to the crash record and the image obligations; §10.7 added (the
  arithmetic overflow contract); the boot stage brought under the booklet's own rules. Reviewer
  verdict before the fixes: "would adopt; would not seal as-is"; the seal includes the fixes.






