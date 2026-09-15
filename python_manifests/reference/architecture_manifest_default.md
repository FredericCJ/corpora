# Software Architecture Manifest — Default (Domain-Agnostic)

## Purpose

This manifest is grounding context, not a rulebook. It establishes shared
vocabulary, lays out the paradigm menu with accepted tradeoffs, and names
common patterns for cross-cutting concerns. It does not prescribe answers.

The architect reasons from first principles. The manifest exists to make
that reasoning legible, check priors against accumulated practice, and
surface tradeoffs that are easy to forget in the moment.

---

## 1. Vocabulary

- **Component.** A unit with a single stated responsibility, a defined
  interface, and an independent lifecycle in testing.
- **Interface / contract.** The observable surface of a component:
  inputs, outputs, invariants, error modes, ordering constraints.
- **Invariant.** A property that must always hold at a named boundary
  (entry, exit, between calls). Invariants are design artifacts;
  they are checked, asserted, or enforced by types.
- **Seam.** A point in existing code where behavior can be altered
  without editing it — typically an interface, a dispatch, a parameter.
  Seams are the primary lever for refactoring and testing legacy code.
- **Coupling.** The degree to which two components depend on each
  other's internals. Lower is usually better, but not always — some
  couplings are necessary, and making them implicit is worse than
  making them direct.
- **Cohesion.** The degree to which a component's contents serve one
  purpose. High cohesion tends to correlate with low coupling but is
  not the same property.
- **State ownership.** Which component has authority to mutate a piece
  of state. Unclear ownership is a recurring source of bugs that are
  hard to localize.
- **Pure function.** Same inputs → same outputs, no side effects.
  Trivially testable, trivially debuggable, trivially parallelizable.
- **Side effect.** Any interaction with state outside the function's
  return value: I/O, mutation of shared state, exceptions that skip
  the return path.
- **Observability.** The degree to which a running component's
  behavior can be inspected from outside — logs, traces, exposed
  metrics, typed return values that carry diagnostic context.

---

## 2. The Paradigm Menu

Each paradigm has conditions where it fits and conditions where it
degrades. The menu is not exhaustive and not exclusive — components
within one system can use different paradigms.

### Structured / procedural

- **Fit:** Linear transformations, command-line tools, scripts with a
  clear beginning and end. Code that reads top-to-bottom.
- **Degrades when:** The problem has non-trivial state that must
  persist across calls; when multiple entry points share logic.
- **Watch for:** Deep nesting; implicit shared state via module-level
  variables.

### Modular

- **Fit:** Any non-trivial system. The baseline discipline.
- **Degrades when:** Module boundaries are drawn along technology lines
  (controllers / services / models) rather than responsibility lines
  (features, subdomains, capabilities).
- **Watch for:** God-modules; circular imports; utility modules that
  accumulate unrelated helpers.

### Ports and adapters (hexagonal)

- **Fit:** A core worth protecting from the technologies around it;
  more than one driver for the same use case (a command line, an HTTP
  surface, a batch job, a test); infrastructure expected to be
  replaced. The arrangement — named by Alistair Cockburn — is one
  core, ports the core declares in its own vocabulary, and adapters
  outside that satisfy them. The observation that earns the style its
  keep: the test suite is one of the adapters, so a test that has to
  reach past a port to drive the core has found a misplaced port, not
  a testing inconvenience.
- **Degrades when:** Ports outnumber the implementations that will
  ever exist — a port with exactly one adapter forever is indirection
  bought and never used; or effects leak inward and the core performs
  I/O anyway, at which point the diagram is the only hexagonal thing
  about the system.
- **Watch for:** Ports written in the vendor's vocabulary rather than
  the core's; a core that only forwards; a core package that imports
  an adapter package. Its named alternative is layering, which orders
  dependencies top-to-bottom rather than inside-out and pays for it
  in pass-through cost.

### Object-oriented

- **Fit:** Domains with natural entity identity; behavior bound to
  data; polymorphism over a closed set of variants; frameworks that
  demand it.
- **Degrades when:** Data is anemic and logic lives elsewhere;
  inheritance is used for code reuse rather than subtyping; every
  verb becomes a class.
- **Watch for:** Deep inheritance hierarchies; "manager" and "service"
  classes that mostly hold static-ish methods; implicit state via
  long-lived instance fields.

### Functional

- **Fit:** Transformation pipelines, data processing, concurrency
  without shared mutable state, business rules expressible as pure
  functions.
- **Degrades when:** The problem is fundamentally stateful or
  side-effect-heavy and forcing purity produces elaborate plumbing
  without commensurate benefit.
- **Watch for:** Cleverness in the name of purity; currying and
  point-free style that obscures intent.

### Contract-based / design-by-contract

- **Fit:** Components with non-trivial invariants; inter-module
  boundaries where violations must be caught immediately; safety- or
  security-relevant code.
- **Degrades when:** Contracts are aspirational rather than checked at
  runtime or enforced by types — they become comments.
- **Watch for:** Contracts that duplicate the type system; contracts
  that leak implementation details.

### Event-driven

- **Fit:** Asynchronous integration; loose coupling between producers
  and consumers; domains with genuine temporal semantics (user actions,
  external signals, long-running processes).
- **Degrades when:** Control flow matters but is hidden by dispatch;
  event ordering is important but not enforced; handlers silently drop
  events.
- **Watch for:** "Event storms" where one logical operation spawns
  many events; debugging by grep across handler files.

### Actor / message-passing

- **Fit:** Concurrent systems with independent units of state;
  isolation of failure domains; distributed systems where location
  transparency matters.
- **Degrades when:** The problem does not need isolation and message
  passing introduces latency and ceremony for no gain.
- **Watch for:** Request-response encoded as two one-way messages;
  back-pressure ignored; mailboxes that grow unbounded.

### Dataflow / pipeline

- **Fit:** Problems naturally expressed as stages over streaming data;
  signal processing, compiler-style transformations, analyzers.
- **Degrades when:** Stages have backward dependencies or need to
  share state; the graph becomes too large to reason about as a whole.
- **Watch for:** Stages that mutate shared state as a side channel;
  implicit ordering constraints not expressed in the graph.

### Type-driven / declarative

- **Fit:** Parsers, validators, schema-governed code; domains where
  "illegal states unrepresentable" is achievable and valuable.
- **Degrades when:** Types become load-bearing for logic they cannot
  actually encode; the type system's expressiveness limits dominate
  the design.
- **Watch for:** Phantom types and type-level programming that makes
  signatures unreadable; over-reliance on structural typing where
  nominal typing would prevent real bugs.

---

## 3. Cross-Cutting Concerns

### 3.1 Coupling and cohesion

Draw module boundaries by responsibility, not by technology. A "database"
module that every feature touches has low cohesion and couples everyone
to a shared implementation. A "billing" module that owns its own
persistence has high cohesion and localizes change.

Coupling is not uniformly bad. A type explicitly imported is better than
a type implicitly shared via duck typing, even though both create a
dependency. Direct, visible coupling is easier to reason about than
diffuse, implicit coupling.

"Reduce coupling" is not one move but several, each with a different
cost — they are named under Modifiability tactics below. An agent
told to pick one of them by name can act; an agent told that lower is
better cannot.

### 3.2 State and ownership

For any piece of state, one component owns mutation; others observe.
The owner is named. Shared ownership is an anti-pattern that surfaces
as reproducibility problems and non-local bugs.

Prefer immutable data for anything that crosses a boundary; mutability
is an ownership statement.

Global state (module-level mutables, singletons, "environment" objects
populated at startup) defeats unit-testability because test isolation
becomes an infrastructure problem rather than a parameter-passing
problem.

### 3.3 Error handling

Four consistent styles; pick one per module boundary and hold it.

- **Exceptions.** Natural in Python; fine for truly exceptional
  conditions. Poor for control flow; poor across process / RPC
  boundaries.
- **Typed results** (`Result<T, E>`, `Either`, tagged unions,
  `Optional` with explicit handling). Forces callers to acknowledge
  failure modes at the type level; reads as normal control flow.
- **Error codes.** Common in C and in cross-language boundaries.
  Requires discipline: every call site checks, or a linter enforces it.
- **Panic / abort.** For invariant violations the program cannot
  recover from. Not for recoverable conditions.

Mixing styles within a module hides the contract. Converting at module
boundaries is fine and often necessary.

### 3.4 Concurrency

Choose a concurrency model before choosing primitives.

- **Shared-memory, locks.** Highest performance, lowest debuggability.
  Reserve for hot paths where other models measured slower.
- **Message-passing.** Each unit of state is owned by one task; others
  send messages. Easier to reason about, easier to test.
- **Single-threaded event loop.** One thread, many pending I/O
  operations. Simplest; limited by the single thread.
- **Parallel pure transformations.** No shared state;
  embarrassingly parallel. Use when the problem shape allows.

Locks without a documented lock order are a recurring source of
deadlocks that take weeks to find. If locks are necessary, the lock
order is part of the design.

Whichever model is chosen, keep it at the edge. Schedulers, worker
pools, queues, timers and clocks belong to the imperative shell — the
outer layer that talks to the world. The core inside it is a
synchronous transformation that neither starts work nor waits for it,
and is therefore deterministic by construction. A module that both
computes and schedules can be tested for neither, because its result
depends on when it ran. As a rule: the core decides, the shell
dispatches — which keeps the concurrency model an edge decision that
can be revisited rather than a commitment spread through every module.

### 3.5 Interfaces and contracts

An interface is the decision the component has frozen. Everything else
is implementation and may change.

- Small interfaces with tight contracts are easier to test, substitute,
  and double than large ones.
- A function with five parameters is an interface with five coupling
  surfaces; consider whether some belong together.
- Error modes are part of the interface. A function that can fail in
  three ways but declares none fails its contract as soon as the
  caller gets one of them wrong.
- Invariants should be stated at the interface, even when not enforced
  in the language — a docstring invariant is better than an unstated
  one.

### 3.6 Observability

A component is observable if its behavior can be understood from
outside during a failure. Design for this; do not retrofit.

- Return values carry diagnostic context when they can. "Found / not
  found" beats silently returning `None`; a typed error beats an
  exception message that loses structure.
- Logging is structured and correlated; unstructured logs do not
  survive production.
- State transitions are loggable events. A state machine that does
  not log transitions is a debugging hazard.

### 3.7 Modifiability tactics

Bass, Clements and Kazman, in *Software Architecture in Practice*,
name the moves that make a system cheaper to change. The naming is
the value: "reduce coupling" becomes a choice among mechanisms with
different prices, and a decision recorded by name can be reviewed.

- **Encapsulate.** Put the internals behind an explicit interface so
  callers depend on the interface only. Cost: the interface is now a
  thing to keep honest, and whatever it fails to expose becomes a
  reason to reach past it.
- **Restrict dependencies.** Forbid the edge outright — this module
  may not depend on that one. Cost: a rule someone has to check, and
  a legitimate future need the rule will refuse.
- **Use an intermediary.** Route the dependency through a mediator, a
  queue, or an event, so neither side names the other. Cost, in the
  source's own terms, is performance — per-event processing the direct
  call did not pay — and control flow that no longer reads in one
  place.
- **Abstract common services.** Replace several near-copies with one
  shared implementation behind an interface. Cost: every later
  divergence between callers argues with the abstraction. Its named
  alternative is worth keeping in view — conform to a published
  standard rather than invent a shared service.
- **Split module.** Divide a module that does two things. Cost: the
  split pays only if it follows responsibility; a bisection by line
  count yields two modules that change together.
- **Redistribute responsibilities.** Move functions so that one likely
  change touches one module. Cost: churn, and a vocabulary the team
  has to relearn. The operational test is the useful part —
  responsibilities are misallocated when one likely change touches
  many modules, or when a module holds parts no change scenario
  touches.
- **Defer binding.** Decide later — at build, at start-up, or per
  request — which implementation is used. Cost is the source's own
  model: up-front mechanism traded against per-change cost, paid
  whether or not the variation arrives.

Encapsulate, restrict dependencies and use an intermediary are named
alternatives to one another, not a sequence: hide it, forbid it, or
route it. The three costs above are how the choice is made.

Two questions hide inside the word "coupling": which modules may
*depend* on which, and which components may *talk* to which at run
time. The graphs diverge as soon as dependencies are injected,
resolved from configuration, or reached through a queue, so a design
that states the first has said nothing about the second.

A dependency rule is only real when a machine checks it. In prose it
is a preference, and preferences lose to the next deadline; as a
contract the build evaluates, it is a boundary. Few languages have a
visibility mechanism strong enough to carry it, so the check is
something the project adds deliberately — and a project unwilling to
maintain that check does not have module boundaries, it has module
intentions. The Python instantiation, including what such a contract
can and cannot express, lives in
`python_module_boundaries_manifest.md`.

---

## 4. Testability Patterns

### 4.1 The test pyramid, in architectural terms

- **Unit tests** verify a component against its own contract. They
  require the component to be instantiable in isolation — a design
  property, not a testing property.
- **Integration tests** verify that two or more components compose
  correctly. They require each component's interface to be honest
  about what it needs and what it promises.
- **System tests** verify end-to-end behavior. They are the last line
  of defense; if they are the first line, the unit and integration
  levels are under-designed.

### 4.2 Seams

Seams are where test doubles substitute for real collaborators. A
component without seams is a component without testability. Common
seams:

- Dependency injection via constructor parameter.
- Higher-order functions (pass the collaborator as a parameter).
- Protocol / interface types that have multiple implementations.

An object that constructs its own collaborators via direct
instantiation is a testing obstacle.

A seam is a property, not a thing. There is nothing in the code to
point at, and "we have a seam here" is not a reviewable claim — so the
discipline that pays is naming the mechanism that creates one:

- A collaborator passed in as a parameter.
- An explicit interface type with more than one implementation.
- That interface declared in the consumer's own package, so the
  implementation depends inward and a substitute needs no third
  package.
- A plugin resolved from configuration at start-up.
- A gateway that owns the whole conversation with a foreign system,
  so there is one thing to replace rather than many call sites.
- A humble object holding no logic at all, with the logic moved to
  something callable directly.
- A lookup point that a test can reseed.

The last is the odd one out: it keeps the dependency out of the
signature, which is precisely the cost that passing it in buys away.
Fowler weighs the two against each other rather than dismissing
either, but note what changes — test isolation moves from
parameter-passing to global manipulation.

"We injected the clock" is reviewable. "We have a seam" is not.

### 4.3 Test doubles

- **Stub.** Returns canned data. Use when the collaborator's behavior
  does not matter, only its presence.
- **Fake.** A working implementation suitable only for tests (in-memory
  store, null logger). Use for collaborators whose real
  implementations are slow or stateful.
- **Mock.** An object that asserts it was called in a specific way.
  Use sparingly; mock-heavy tests become brittle and change-averse.

### 4.4 Determinism

Flaky tests erode trust. Common sources of flakiness:

- Time (`now()`, sleep, timeouts) — inject time.
- Randomness — seed it or inject it.
- Concurrency — test pure logic sequentially; test concurrency
  explicitly at specific seams.
- I/O ordering (file system, network) — fake or isolate.

Nondeterminism that cannot be removed is the graded case, not an
exception to the rule. Eliminate it first. Where it is irreducible —
concurrent responses to genuinely unpredictable events — record what
crossed the interface and replay the recording; that is the tactic's
own stated escape, not a workaround. Quarantine and retry last, with
the cost admitted: a retry is containment, not a fix, and it turns a
known-unreliable signal into a slower unreliable signal.

### 4.5 The testability tactics, named

Bass, Clements and Kazman, in *Software Architecture in Practice*,
name the testability tactics, and the naming is again the value:
"make it testable" becomes a choice among distinct moves. It also
supplies the better justification for a testing construct — a double,
a fixture, a table of cases or a recorded output is chosen for the
tactic it realizes.

- **Abstract data sources.** Put the data behind an interface so the
  system can be repointed from production data to fixture data
  without touching functional code. That repointing is itself a late
  binding; see Defer binding above.
- **Executable assertions.** Put the oracle in the code, where the
  data is referenced or modified, so a bad state is caught where it is
  produced rather than where it is finally noticed. Know the lifetime
  of the assertions you write: many languages and build modes strip
  them, so "checked by an assertion" names more than one guarantee and
  only the strongest reaches production. When one fires, read the
  blame — a failed precondition indicts the caller, a failed
  postcondition indicts the callee — because that is what says which
  test is missing.
- **Limit nondeterminism.** Remove the sources of variance: clock,
  randomness, scheduling, arrival order. Determinism, above.
- **Limit structural complexity.** Cut coupling, break cycles, shrink
  the reachable state space. The testability argument is separate from
  the modifiability one: a large state space makes a component hard to
  *drive to* the state a failure needs, and re-entering that state is
  the expensive half of debugging.
- **Localize state storage.** Keep mutable state in one place, so a
  test can construct the state it needs instead of driving the system
  there. Its named realization is a state-machine object — the same
  thing that makes transitions loggable.
- **Record/playback.** Capture what crosses an interface and replay it
  to re-enter a state. Not the same as capturing output: output says a
  result changed, a recorded interaction lets you re-enter the
  situation. It works only at a declared boundary — record inside the
  component and the recording encodes your test harness rather than
  the component's environment.
- **Specialized interfaces.** A test-only surface for control and
  observation, kept apart from the functional interface. The source
  states its cost — shipping code that differs from tested code — and
  assumes the interface can be left out of the shipped build. Where
  the language offers no way to remove it, the honest consequence is
  that test hooks ship, so they are public contract: name them openly
  rather than hide them behind a convention, keep them read-only where
  possible, and review the mutating ones as production API.
- **Sandbox.** Virtualize the resources you cannot control — clock,
  network, filesystem, anything whose real use has consequences — so a
  test can drive them and reverse them. The same pattern serves
  security by limiting what code can reach; both readings are correct,
  which is a reason to build it once and well.

### 4.6 Three reasons to substitute, three exit criteria

A substitution with no stated reason has no finish line: it grows
until the double is a second implementation of the collaborator and
the test is a model of the system. There are three reasons, from
three different tactics:

- **To virtualize a resource you do not control** (sandbox). Done
  when a test can put the resource in any state it needs and using it
  has no consequence outside the test.
- **To remove behavioral variance** (limit nondeterminism). Done when
  repeated runs agree — that, and nothing beyond it.
- **To supply controlled inputs** (abstract data sources). Done when
  the input partitions the contract distinguishes are covered.

Filing all three under one heading is what makes a suite accumulate
doubles indefinitely: the reason is what says when to stop.

---

## 5. Debuggability Patterns

Debuggability at integration and system level is a design outcome,
not an afterthought.

### 5.1 Fault isolation topology

Every failure mode should have a component it can be localized to.

- Ask of every component: "if this component is broken, how does the
  system present?" If the answer is "many different symptoms," the
  component has too many responsibilities or its failure modes leak
  upward without structure.
- Circuit breakers, bulkheads, and timeouts are topology decisions,
  not infrastructure concerns. They determine whether a component's
  failure stays local or propagates.

### 5.2 Observable boundaries

Between components, log the boundary crossing:

- Inputs (post-validation, so the value the component actually got is
  visible).
- Outputs (return value or outgoing message).
- Duration (enough to correlate slow paths with failures).

Debugging an integration failure means reconstructing what crossed
the boundary. If the boundary is opaque, the investigation starts by
adding the observability that should have been there.

### 5.3 Error propagation discipline

Errors should acquire context as they propagate, not lose it.

- Re-raising `except Exception: raise` loses the call site.
- Re-raising with context (`raise X from Y`, or wrapping a typed
  error with a containing one) preserves the chain.
- Errors that cross process boundaries need to carry their origin —
  a stringified traceback on one side, a typed error code on the
  other is a common pattern.

### 5.4 State transition tracing

For components with non-trivial state machines, log transitions
unconditionally in debug mode. The "how did we get here?" question
is the most common integration-debugging question; it is answered
cheaply in advance.

### 5.5 Design for diagnosis

The sections above make a failure legible once someone is watching.
Diagnosis has a design half that has to exist before the failure: the
component can say whether its own assumptions hold, it can be
interrogated without being modified, and its failures can be
reproduced by someone who does not have the machine they happened on.

- **A self-check at start-up.** Borrowed from hardware and firmware,
  where a built-in self-test verifies integrity on power-up. The full
  form — scheduled tests coupled to a watchdog, covering the
  substrate — is over-engineering at single-process scale. The
  transferable residue is narrow and cheap: check at start-up only
  what cannot be checked statically and would otherwise fail late and
  confusingly — every declared dependency present at the expected
  version, every configured path writable, every configured endpoint
  resolvable, the configuration schema and the code in agreement. It
  replaces no test; it converts a mid-run failure into a start-up
  failure, which is far cheaper. How far to take it is a judgment with
  no authority behind it — make it deliberately, not by accretion.
- **A separable maintenance interface.** One read-only surface
  reporting the same facts the diagnostics already produce, rather
  than a parallel truth maintained by hand: build and runtime
  identity, effective configuration, current log levels, resource
  counters, a snapshot of what each thread or task is doing. Keep it
  apart from the functional interface, and gate anything that mutates
  state separately — a probe that changes the behavior it observes is
  a different feature with a different risk, and enabling it is a
  decision, not a detail.
- **Reproducible from artifacts alone.** The standard worth designing
  against: a failure is reproducible when four things are recoverable
  without the developer's machine — the exact runtime and build, the
  effective configuration including anything in the environment that
  changed runtime behavior, the inputs identified by content rather
  than by name, and a stack. Each is cheap to emit at start-up and
  expensive to reconstruct afterwards. A system that cannot produce
  all four is debugged by guesswork, however good its logs are.

The instruments — attaching to a live process, crash and hang dumps,
memory attribution, profiling, post-mortem inspection — are platform
facts rather than design principles, and the Python ones live in
`python_runtime_diagnostics_manifest.md`.

---

## 6. Refactoring Patterns

In order of increasing invasiveness:

- **Rename / extract / inline.** Local, reversible, cheap. Should be
  automated by tooling.
- **Extract seam.** Introduce an interface between two components
  that were previously directly coupled, without changing behavior.
  Enables testing and subsequent substitution.
- **Parallel change.** Introduce the new API alongside the old;
  migrate callers incrementally; remove the old. The only safe way
  to change a widely-used interface.
- **Branch by abstraction.** For large internal refactors: introduce
  an abstraction layer, migrate uses to it, replace the
  implementation behind it, collapse the abstraction if no longer
  needed.
- **Strangler fig.** For replacing an entire subsystem: route new
  functionality to the replacement, migrate old functionality piece
  by piece, decommission the original when empty.
- **Characterization tests.** For legacy code without tests: write
  tests that capture current behavior (correct or not), then
  refactor with those tests as a safety net.

Rewrites from scratch are occasionally the right call but are
structurally risky. They discard production knowledge encoded in the
current code. Prefer incremental paths until the evidence for a
rewrite is overwhelming.

---

## 7. Common Tradeoff Axes

Architectural decisions rarely have a single "right" answer; they live
on axes. Naming the axis is half the decision.

- **Generality vs. specificity.** A general solution handles more
  cases but carries more cognitive load. Specific solutions are
  cheaper now, more expensive to change later.
- **Consistency vs. contextual fit.** A pattern applied uniformly is
  learnable; a pattern bent to each context is optimal locally but
  costly system-wide.
- **Explicit vs. convention.** Explicit wiring is verbose but
  discoverable. Convention is compact but depends on the reader
  knowing the convention.
- **Flexibility vs. constraint.** A flexible design accommodates more
  futures but is harder to reason about. Constrained designs are
  easier to understand but cannot be bent when requirements shift.
- **Performance vs. readability.** Usually overstated. In hot paths,
  real. Elsewhere, optimize the readable version and measure.
- **Early abstraction vs. concrete duplication.** Abstracting from two
  examples usually produces the wrong abstraction. Three is the
  common threshold. Duplication with differences is more honest than
  an abstraction with exceptions.
- **Binding time.** Every variation point binds somewhere: at build,
  at start-up, or per request. Later binding buys change without a
  redeployment and costs mechanism up front — up-front mechanism
  traded against per-change cost, paid whether or not the variation
  ever arrives. Default: bind as early as the rate of change allows.
- **Enforcement cost vs. flexibility.** A rule a machine checks costs
  setup, maintenance, and the occasional refusal of a legitimate
  exception. A rule written in prose costs nothing and decays to
  nothing. Prefer the checked rule for anything load-bearing; where
  nothing can check it, say so rather than imply the rule holds.
- **Modifiability vs. per-event cost.** Distinct from performance vs.
  readability, and more often real. Intermediaries, indirection and
  separation of concerns are bought for modifiability and paid for in
  per-event processing and communication. This is the axis that
  decides whether a boundary becomes a function call, a queue, or a
  separate process — not taste.

Each tradeoff has a default; none has a universal answer. Name the
axis, name the default, name why the current decision deviates (or
does not).

---

## 8. Where This File Is Instantiated

This file names principles and withholds prescriptions, so it cannot
be complied with on its own. The mechanisms — the types, the
checkers, the rule sets, the runtime instruments, and the enforcement
that decides whether any of it survives a deadline — live in the
language-specific manifests beside it.

The Python instantiation lives in:

- `python_module_boundaries_manifest.md` — the unit of change, the
  import graph as a boundary, and the machine-checked dependency rule
  that Modifiability tactics says a boundary needs.
- `python_typing_contract_manifest.md` — contracts carried as types,
  and what the type system cannot carry.
- `python_language_hazards_manifest.md` and
  `python_linting_practices_manifest.md` — the hazards worth
  designing around, and the rule set that catches them.
- `python_testing_tooling_manifest.md` — the testability tactics of
  section 4 as concrete constructs, with the double taxonomy.
- `python_concurrency_determinism_manifest.md` — the execution models
  of section 3.4, and how a shell keeps a core deterministic.
- `error_tracing_contract_manifest.md`,
  `logging_observability_manifest.md` and
  `python_runtime_diagnostics_manifest.md` — diagnosability split
  three ways: the error contract, the emission side, and the live or
  crashed process.
- `python_quality_gates_manifest.md` — where the rules above are
  enforced, and how a standard is adopted without a rewrite.
- `software_spec_discipline_manifest.md` — how to write the
  specification this reasoning produces.

The browser-native instantiation lives in `../web_manifests/`, whose
`web_architecture_manifest.md` is this file's counterpart for that
target.

This file carries no version-dependent facts, on purpose. Where a
Python fact has a version attached, the Python set routes it through
`python_platform_baseline_manifest.md`, the single version hub.