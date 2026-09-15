# Modularity, maintainability and incremental build - seed pack (mined 2026-08-08)

**Key question answered up front.** *What named, citable vocabulary lets an agent state a module
boundary as an enforceable contract rather than a preference?*

The SWE corpus supplies a five-rung ladder, and the rungs are separately citable. Each rung moves the
boundary from prose into something a machine can refuse:

1. **`encapsulate`** (bck 2021) - the boundary exists as an *explicit interface*, so "other elements
   depend only on the interface." Still a preference: nothing stops a caller reaching past it.
2. **`explicit-interface`** (posa4 2007) - the contract is a *first-class type*, "explicitly separated
   from any implementation class." Now a type checker can refuse. Python: `typing.Protocol` / `abc.ABC`.
3. **`separated-interface`** (poeaa 2002) - the interface lives *in a different package from its
   implementation*, "so clients depend only on the interface package." Now the boundary is a fact about
   the import graph, not about intent. This is the rung most Python codebases skip.
4. **`restrict-dependencies`** (bck 2021) - "Restrict which modules a given module may interact with or
   depend on, **in practice via interface visibility and authorization**." bck names the enforcement
   mechanism, not just the goal. Python has no visibility mechanism, so this rung must be bought
   externally: an import-linter contract file, ruff `flake8-tidy-imports` banned-api, a `grimp`
   assertion in the test suite. That contract file *is* the enforceable statement.
5. **`interface-definition-language`** (corbaspec 1991) - "a language-neutral contract ... from which
   stubs, skeletons and serializers are generated." The strongest rung: the contract is a *build input*,
   so violating it fails the build rather than a lint. Pair with **`generation-gap`** (vlissideshatching
   1998) so regeneration never eats hand-written code.

Two supporting rungs make the statement auditable rather than merely enforced:
**`module-view`** (vab 2010) records the permitted "uses" relation as a documented artifact, and
**`architecture-decision-record`** (nygardadr 2011) records *why* an edge is forbidden, so the next
agent neither cargo-cults nor silently reverses it. **`limit-structural-complexity`** (bck 2021) names
the measurable version ("avoid or resolve cyclic dependencies ... propagation cost, decoupling level"),
which is what turns a boundary into a CI gate.

The honest Python caveat, stated once and reused: **`__all__` is not enforcement.** It governs
`from x import *` and nothing else; `_private` is a convention the interpreter ignores. Every rung above
rung 2 is therefore *tooling you must add*, and a Python module-boundaries manifest that says "keep
modules decoupled" without naming the contract file has stated a preference.

---

## Import table

Only elements the existing manifest family genuinely lacks. All ids verified against
`SWE/explorer/data/elements.json` (1083 nodes) this session.

| element id | realm/kind | catalog name | named-in (citable) | Python instantiation | destination manifest + section |
|---|---|---|---|---|---|
| `restrict-dependencies` | architecture/tactic | Restrict Dependencies | bck (Bass, Clements & Kazman, *Software Architecture in Practice* 4th ed., 2021) - "via interface visibility and authorization" | `import-linter` contracts (`[tool.importlinter]`: `layers`, `forbidden`, `independence`) backed by `grimp`; ruff `flake8-tidy-imports` `banned-api` + `ban-relative-imports`; a test asserting the import graph. **Not** `__all__`. | NEW python_module_boundaries_manifest.md :: The dependency rule |
| `restrict-communication-paths` | architecture/tactic | Restrict Communication Paths | bck 2021 | The *runtime* half: the collaborators a component may call are exactly its injected `Protocol`-typed parameters; no imports inside function bodies to dodge the graph. | NEW python_module_boundaries_manifest.md :: The dependency rule |
| `separated-interface` | design/oo-patterns | Separated Interface | poeaa (Fowler, *Patterns of Enterprise Application Architecture*, 2002) - confidence: spot-checked | `myapp/ports/storage.py` holds the `Protocol`; `myapp/adapters/postgres.py` implements it; `ports` imports nothing from `adapters`. Reverses the import-time dependency. | NEW python_module_boundaries_manifest.md :: Where the interface lives |
| `explicit-interface` | design/construction-api | Explicit Interface | posa4 (Buschmann, Henney & Schmidt, 2007) - confidence: spot-checked | `typing.Protocol` (PEP 544) for structural contracts; `abc.ABC` + `abstractmethod` when nominal enforcement or subclass registration is wanted. | NEW python_module_boundaries_manifest.md :: Where the interface lives |
| `self-contained-component` | architecture/pattern | Self-Contained Component | preschern (*Fluent C*, 2022) | One package per component; `__init__.py` is the single public surface (explicit re-exports); dependencies point only toward more fundamental packages. The C "one header" maps exactly to the package's public module. | NEW python_module_boundaries_manifest.md :: Component shape |
| `split-module` | architecture/tactic | Split Module | bck 2021 - "not an arbitrary bisection, but a principled separation of responsibilities" | Split by responsibility, never by line count. Evidence: `git log --name-only` co-change clusters. | NEW python_module_boundaries_manifest.md :: Restructuring moves |
| `redistribute-responsibilities` | architecture/tactic | Redistribute Responsibilities | bck 2021 (3rd-ed name: *increase semantic coherence*) | Move functions so one change scenario touches one package. bck's test: "a module contains parts untouched by any scenario" = misallocated. | NEW python_module_boundaries_manifest.md :: Restructuring moves |
| `abstract-common-services` | architecture/tactic | Abstract Common Services | bck 2021 | One shared module behind the variants: a `Protocol` + `functools.singledispatch`, or a registry keyed by type - instead of N near-copies. | NEW python_module_boundaries_manifest.md :: Restructuring moves |
| `use-an-intermediary` | architecture/tactic | Use an Intermediary | bck 2021 - "at some performance cost" | A mediator module, `blinker` signals, or a `queue.Queue`/`asyncio.Queue` between two packages that must not import each other. Import the *cost statement* with it. | architecture_manifest_default.md :: 3.1 Coupling and cohesion |
| `defer-binding` | architecture/tactic | Defer Binding | bck 2021 | The binding-time ladder, named: build (optional extras, `importlib`), deploy/startup (env + TOML, `importlib.metadata.entry_points`), runtime (`Protocol` + dict dispatch, toggle router). bck's cost model: "trading up-front mechanism cost against per-change cost." | NEW python_module_boundaries_manifest.md :: Binding time is a decision |
| `plugin` | design/construction-api | Plugin | poeaa 2002 - confidence: spot-checked | `[project.entry-points."myapp.plugins"]` in `pyproject.toml` (PEP 621) + `importlib.metadata.entry_points(group="myapp.plugins")`. | NEW python_module_boundaries_manifest.md :: Binding time is a decision |
| `discover` | architecture/tactic | Discover | bck 2021 | In-process, `importlib.metadata.entry_points` *is* the discovery service; `pkgutil.iter_modules` for namespace-package scanning. The distributed sense (service registry, client/server-side discovery) does not apply in-process - say so. | NEW python_module_boundaries_manifest.md :: Binding time is a decision |
| `tailor-interface` | architecture/tactic | Tailor Interface | bck 2021 | An adapter module owned by *your* side of the boundary; `functools.partial`/`wraps` wrappers. Never monkey-patch the foreign library - that deletes the boundary. | NEW python_module_boundaries_manifest.md :: Adapting at the seam |
| `interface-definition-language` | architecture/description | Interface Definition Language | corbaspec (OMG, *The Common Object Request Broker: Architecture and Specification*, 1991) | `.proto` + `grpcio-tools`/`betterproto`; JSON Schema / OpenAPI + `datamodel-code-generator` to pydantic models. Generated modules are build output, never edited. **When not to:** for a pure-Python in-process boundary a `Protocol` in a `ports` package *is* the contract; an IDL only pays across process or language. | NEW python_module_boundaries_manifest.md :: Contracts that are build inputs |
| `generation-gap` | design/code-structure | Generation Gap | vlissideshatching (Vlissides, *Pattern Hatching*, 1998) | Never edit `*_pb2.py` or generated pydantic models; subclass or wrap in a hand-written sibling module. The corpus states `generation-gap --enables--> interface-definition-language`. | NEW python_module_boundaries_manifest.md :: Contracts that are build inputs |
| `module-view` | architecture/description | Module View | vab (Clements et al., *Documenting Software Architectures: Views and Beyond* 2nd ed., 2010) | The import-linter contract file plus a generated graph (`grimp`, `pydeps`) *is* the module view: decomposition, uses, layering. Serves "construction, modification-impact analysis, and work assignment." | NEW python_module_boundaries_manifest.md :: Documenting the boundary |
| `component-and-connector-view` | architecture/description | Component-and-Connector View | vab 2010 | The *runtime* graph: asyncio tasks, processes, queues, HTTP clients. In Python this routinely diverges from the import graph - two artifacts, not one. | NEW python_module_boundaries_manifest.md :: Documenting the boundary |
| `allocation-view` | architecture/description | Allocation View | vab 2010 | src-layout mapping of packages to directories (PyPA src-vs-flat), plus `CODEOWNERS` as the work-assignment allocation. | NEW python_module_boundaries_manifest.md :: Documenting the boundary |
| `architecture-decision-record` | architecture/description | Architecture Decision Record | nygardadr (Nygard, *Documenting Architecture Decisions*, 2011) | `docs/adr/NNNN-*.md` (MADR), one per boundary decision, cross-referenced from the import-linter contract that enforces it. Catalog's problem statement: later maintainers "either cargo-cult the decision or blindly reverse it." | NEW python_module_boundaries_manifest.md :: Documenting the boundary |
| `context-map` | architecture/description | Context Map | evansddd (Evans, *Domain-Driven Design*, 2003) | A table naming the relationship type at each package seam (partnership, customer-supplier, conformist, anti-corruption layer) - the boundary's *kind*, which an import rule alone cannot express. | NEW python_module_boundaries_manifest.md :: Documenting the boundary |
| `stateless-software-module` | design/code-structure | Stateless Software-Module | preschern (*Fluent C*, 2022) + preschernplop (**unverified**) | A module of functions with no module-level mutable state; every resource acquired and released inside the call (`with` inside the function). Stated cost: "rules out cross-call caching or context." | NEW python_module_boundaries_manifest.md :: Module state |
| `limit-structural-complexity` | architecture/tactic | Limit Structural Complexity | bck 2021 | `grimp`/import-linter for cycles; `radon`/`wily` for per-unit complexity. bck names the metrics to gate on: "response-of-class, propagation cost, and decoupling level." | NEW python_quality_gates_manifest.md :: What the gates measure |
| `specialized-interfaces` | architecture/tactic | Specialized Interfaces | bck 2021 | Test-only set/get/report/reset surfaces kept separate and removable. Carries bck's hazard verbatim: "shipping code different from tested code is problematic in performance- and safety-critical systems." | NEW python_quality_gates_manifest.md :: Test access without shipping test code |
| `adhere-to-standards` | architecture/tactic | Adhere to Standards | bck 2021 | PEP 8 / PEP 257 (style, docstrings), PEP 517 / 518 / 621 (build, metadata), PEP 484 / 544 (typing). Conformance is *what makes a gate mechanical*; a house style with no published standard cannot be linted. | NEW python_quality_gates_manifest.md :: Why standards, not preferences |
| `deployment-pipeline` | architecture/deployment | Deployment Pipeline | contdeliv (Humble & Farley, *Continuous Delivery*, 2010, ch. 5 "Anatomy of the Deployment Pipeline") | One wheel built once (PEP 517) and *promoted* through stages; `nox`/`tox` sessions define stages, CI executes them. Catalog: "each gating promotion of the same artifact." | NEW python_quality_gates_manifest.md :: The pipeline is a structure |
| `script-deployment-commands` | architecture/tactic | Script Deployment Commands | bck 2021 | `nox`/`tox`/`make` targets plus the CI YAML, all "documented, reviewed, tested, version-controlled." Kills the runbook. | NEW python_quality_gates_manifest.md :: The pipeline is a structure |
| `package-dependencies` | architecture/tactic | Package Dependencies | bck 2021 | PEP 621 `[project.dependencies]` for ranges + a lockfile (`uv.lock`, `poetry.lock`, `pip-compile` output) for exactness + an image for interpreter and OS libs. Problem it solves: code that "behaves correctly in development can fail in production when the surrounding dependency versions differ." | NEW python_quality_gates_manifest.md :: Reproducible environments |
| `executable-assertions` | architecture/tactic | Executable Assertions | bck 2021 (`same-name:design-realm` with `sanity-check`) | `assert` for internal invariants (**disabled under `-O`/`PYTHONOPTIMIZE` - never for input validation**); `icontract`/`deal` for pre/postconditions; pydantic validators at the boundary. | NEW python_quality_gates_manifest.md :: Assertions as gates |
| `feature-flag` + `feature-toggle` | design/code-structure + architecture/tactic | Feature Flag / Feature Toggle | hodgsontoggles (Hodgson, *Feature Toggles (aka Feature Flags)*, 2017) for the design element; bck 2021 for the tactic | Toggle point + toggle router reading external config (env, TOML, or a flag service). The design element names the parts: toggle point, toggle router, toggle configuration. | NEW python_quality_gates_manifest.md :: Decoupling deploy from release |
| `scale-rollouts` | architecture/tactic | Scale Rollouts | bck 2021 | The tactic; its named realizations are `blue-green-deployment` and `rolling-deployment` (both *sourced* `specializes` edges) and `canary-release`. bck's requirement: "an architectural mechanism **outside** the service that routes each user's requests to the new or old version." | NEW python_quality_gates_manifest.md :: Decoupling deploy from release |
| `rollback-deployment` | architecture/tactic | Rollback (Deployment) | bck 2021 | Distinct from the availability `rollback-tactic` (checkpoint restore) - the corpus keeps them separate. Python: re-promote the previous wheel/image; migrations must be independently reversible. | NEW python_quality_gates_manifest.md :: Decoupling deploy from release |
| `manage-service-interactions` | architecture/tactic | Manage Service Interactions | bck 2021 | Version coexistence during a rolling deploy. Enabled by `tolerant-reader` (Fowler bliki, 2011) and `schema-evolution-via-field-tags`: consumers read only what they need and ignore unknown fields. | architecture_manifest_default.md :: 3.5 Interfaces and contracts |
| `immutable-infrastructure` | architecture/deployment | Immutable Infrastructure | immutableserver (Kief Morris, *ImmutableServer* bliki, 2013; also *Infrastructure as Code*, 2016) | Pinned base image, wheel built once, config injected. Never `pip install` into a running container. Catalog: "rollback [is] a redeploy of the previous image." | NEW python_quality_gates_manifest.md :: Reproducible environments |

---

## Fold table

Vocabulary the manifest family already states under another name. Fold, keep the manifest's word, and
carry the citation so the rule stops being an assertion.

| element id | catalog name | the manifest already calls this | note |
|---|---|---|---|
| `encapsulate` | Encapsulate | arch manifest 1 "Interface / contract"; 3.5 "An interface is the decision the component has frozen." | Exact synonym; bck's aka is literally "introduce explicit interface." Fold, but import the *measurable* clause: it reduces "the strength of coupling and the syntactic/semantic distance to be bridged" - two axes the manifest collapses into one word. |
| `dependency-injection` | Dependency Injection | arch manifest 4.2 Seams: "Dependency injection via constructor parameter" | Same thing; the corpus supplies the naming source (fowlerdi, Fowler 2004) and the full aka set (constructor / setter / interface injection). The manifest omits the *sourced* edge `service-locator --alternative-to--> dependency-injection` - "Fowler explicitly weighs them against each other." |
| `test-double`, `service-stub` | Test Double / Service Stub | arch manifest 4.3 "Stub / Fake / Mock" | Fold; naming source is meszaros (*xUnit Test Patterns*, 2007). `service-stub` (poeaa) is the distinct boundary-level construct the manifest's three-way split has no slot for. |
| `golden-master-testing` | Golden Master Testing | arch manifest 6 "Characterization tests" | The corpus's canonical id; "characterization testing (legacy-code framing)" is an *aka*, alongside approval and snapshot testing. Naming source welc (Feathers, *Working Effectively with Legacy Code*, 2004). The manifest is missing the construct's third part: "an explicit approve-the-diff step when change is intended." |
| `strangler-fig` | Strangler Fig | arch manifest 6 "Strangler fig" | Present and correctly used. Provenance caveat: the corpus's `named_in` is the Azure Cloud Design Patterns catalog with **year unresolved**; "StranglerFigApplication (Fowler 2004)" is recorded only as an aka. Cite accordingly. |
| `layer-supertype` | Layer Supertype | arch manifest 2 Object-oriented, degrades when "inheritance is used for code reuse rather than subtyping" | poeaa names the construct the manifest warns against. Fold as a named anti-target and carry the corpus's alternative: `layer-supertype --alternative-to--> mixin`. Python's answer is a `Protocol` plus free functions. |
| `registry`, `service-locator` | Registry / Service Locator | arch manifest 3.2 "Global state (module-level mutables, singletons, 'environment' objects populated at startup)" | These *are* what the manifest bans. Fold, but see REFINE 5: the corpus records them as a stated tradeoff with DI, not a prohibition, and `registry`'s entry insists the scope (process / thread / session) be "explicit" - which in Python is `contextvars`, not a module global. |
| `facade` | Facade | arch manifest 3.1 / 3.5 (small interfaces, subsystem boundaries) | GoF name. Fold with one sharpening: a facade "shields clients from subsystem internals **without forbidding direct access**" - it is a convenience, not a boundary. `restrict-dependencies` is the boundary. |
| `composed-method`, `method-object` | Composed Method / Method Object | arch manifest 6 "Rename / extract / inline"; 2 Structured "Watch for: deep nesting" | Beck, *Smalltalk Best Practice Patterns* (1997) names both; Fowler's *Refactoring* names the move "Replace Method with Method Object." Corpus records them as `alternative-to` each other - "extract intention-named calls in place vs. reify it as its own class." |
| `software-module-with-global-state` | Software-Module with Global State | arch manifest 3.2 "Global state ... defeats unit-testability" | Fold - but the corpus does **not** ban it: Preschern names it a legitimate pattern "trading simplicity for a single shared context," with `stateless-software-module` as its named alternative. See REFINE 5. |
| `humble-object` | Humble Object | arch manifest 4.2 (seams), 5.x (thin glue) | meszaros 2007. Fold; the manifest describes the technique without the name. Corpus pairs it with `functional-core-imperative-shell` (Bernhardt 2012), which the manifest also describes namelessly in 2 Functional. |
| `limit-nondeterminism` | Limit Nondeterminism | arch manifest 4.4 Determinism | bck 2021. Exact fold, including the manifest's remedy list. |
| `abstract-data-sources` | Abstract Data Sources | arch manifest 4.4 "I/O ordering ... fake or isolate" | bck 2021. Fold; adds the deploy-time framing - "repointing the system from a production customer database to test databases ... without changing functional code." |
| `modular-monolith`, `bounded-context` | Modular Monolith / Bounded Context | arch manifest 3.1 "A 'billing' module that owns its own persistence has high cohesion" | The manifest's worked example *is* a bounded context inside a modular monolith. Fold the example onto the two names (evansddd 2003; monolith2micro - **unverified**). |

---

## Relations worth stating

Edges taken verbatim from `elements.json`. `[sourced]` = a citable source states the relation;
`[editorial]` = a marked editorial judgment in the corpus. Both are usable; only `[sourced]` should be
presented as literature.

### The coupling-reduction triangle - three named ways, not one rule

- `restrict-dependencies --alternative-to--> use-an-intermediary` **[sourced]** - "Both cut coupling:
  forbid a dependency outright vs. route it through an intermediary."
- `use-an-intermediary --alternative-to--> encapsulate` **[sourced]** - "Reduce-coupling siblings:
  interpose a mediator vs. hide internals behind an explicit interface."
- `restrict-communication-paths --alternative-to--> use-an-intermediary` **[sourced]** -
  "Limit-dependencies siblings: forbid direct communication vs. route it through an intermediary."
- `restrict-communication-paths --composes-with--> restrict-dependencies` [editorial] - "Both shrink an
  element's interaction surface - runtime communication partners vs. module-level dependencies."

This is the manifest's biggest single gain: "reduce coupling" is three distinct decisions (forbid /
mediate / hide), each with a different cost, and the runtime and import-time versions are separate
tactics. State the triangle and make the agent pick a vertex.

### The interface-placement chain - why `Protocol` alone is not a boundary

- `explicit-interface --realizes--> encapsulate` [editorial] - "clients depend only on the interface, not
  internals."
- `separated-interface --specializes--> explicit-interface` [editorial] - "refines the explicit-interface
  idea by placing the interface in a **different package** from its implementation."
- `separated-interface --realizes--> restrict-dependencies` [editorial] - "so clients depend only on it."
- `separated-interface --composes-with--> dependency-injection` **[sourced]** - "DI wires the concrete
  implementation to a client that depends only on the separated interface."
- `gateway --composes-with--> separated-interface` [editorial] - "A Gateway's interface is often defined as
  a Separated Interface **so clients can be tested against a stub**."
- `self-contained-component --uses--> restrict-dependencies` [editorial] - "Dependencies may point only
  toward more fundamental components - an explicit restrict-dependencies rule."
- `sealed-trait --realizes--> restrict-dependencies` [editorial] - "Visibility-based sealing restricts
  which modules may implement an interface, controlling the dependency/extension surface."

### Cohesion restructuring has an order

- `split-module --composes-with--> redistribute-responsibilities` [editorial] - "split a non-cohesive
  module, **then** move related responsibilities together into one module."
- `redistribute-responsibilities --alternative-to--> abstract-common-services` [editorial] - "Both gather
  scattered similar functionality into one place to cut duplication - move responsibilities vs. abstract a
  shared service."
- `adhere-to-standards --alternative-to--> abstract-common-services` **[sourced]** - "conform to shared
  standards vs. factor a shared abstract service." (Use the published standard before inventing a shared
  service - the PEP argument.)
- `split-module --composes-with--> limit-structural-complexity` [editorial], and
  `limit-structural-complexity --composes-with--> restrict-dependencies` **[sourced]** - "Reducing
  inter-component coupling and breaking cyclic dependencies is how structural complexity is limited for
  test." *This edge is the justification for putting a cycle check in CI.*
- `limit-structural-complexity --uses--> encapsulate` **[sourced]** - "includes isolating and encapsulating
  environmental dependencies."
- `composed-method --realizes--> limit-structural-complexity` [editorial]; `method-object --realizes-->
  split-module` [editorial] - "Method-scale analog of the modifiability tactic." The same tactic applies at
  two scales; one vocabulary covers both.

### Why a mechanism is chosen: binding time

- `plugin --realizes--> defer-binding` [editorial] - "Selecting behavior per deployment via configuration
  binds the implementation late (deployment-time)."
- `resource-files --realizes--> defer-binding` **[sourced]** - "Configuration and read-only resources in
  external files bind values at startup instead of compile time."
- `configure-behavior --uses--> defer-binding` [editorial]; `feature-toggle --uses--> defer-binding`
  [editorial] - "A runtime kill switch binds the feature-enabled choice at runtime - **the latest binding
  time**."
- `facade-backend-module-pattern --alternative-to--> plugin` [editorial] - "Both pick an implementation per
  deployment; the facade/backend binds at build/link time, Plugin binds at config/runtime."
- `escaping-ifdef-hell --alternative-to--> feature-flag` [editorial] - "Select variation at compile time via
  isolated #ifdef abstractions vs at runtime via a toggle."
- `abstract-data-sources --composes-with--> defer-binding` [editorial] - "Repointing to test data without
  code change relies on binding the concrete data source late (deploy/test time)."

Together these make one statable rule: *every variation point has a binding time; name it, and pay bck's
cost model - "trading up-front mechanism cost against per-change cost."*

### Obtaining a dependency: the tradeoff the manifest turns into a ban

- `service-locator --alternative-to--> dependency-injection` **[sourced]** - "Two competing ways to obtain a
  dependency; Fowler explicitly weighs them against each other."
- `registry --alternative-to--> dependency-injection` **[sourced]** - "Looking services up in a
  Registry/Service Locator vs having them injected are competing ways to obtain collaborators."
- `plugin --composes-with--> service-locator` **[sourced]** - "Plugin uses a Service Locator (a registry
  seeded by config) to resolve the configured implementation at runtime."
- `registry --composes-with--> singleton` [editorial] - "most commonly made globally reachable as a
  Singleton."
- `abstract-session --alternative-to--> registry` [editorial] - "Handing each client an opaque session handle
  keeps per-client state off a shared global Registry lookup."

### Release: deploy and release are different acts

- `deployment-pipeline --composes-with--> feature-flag-driven-release` **[sourced]** - "Pipeline deploys dark
  code; flags decouple release from deployment."
- `feature-flag --realizes--> feature-toggle` **[sourced]** - the explicit same-name-two-realms bridge
  (design mechanism to architecture tactic).
- `feature-flag --composes-with--> strategy` **[sourced]** - "Long-lived toggles are best realized by
  selecting a Strategy implementation **rather than inline conditionals**." A directly enforceable rule.
- `feature-toggle --alternative-to--> rollback-deployment` [editorial] - "flip its runtime kill switch with
  no redeploy vs. roll the whole deployment back."
- `blue-green-deployment --specializes--> scale-rollouts` **[sourced]**; `rolling-deployment --specializes-->
  scale-rollouts` **[sourced]**; `canary-release --specializes--> scale-rollouts` [editorial]. One tactic,
  three named realizations.
- `blue-green-deployment --alternative-to--> canary-release` **[sourced]** - "whole-environment switch vs
  incremental slice"; `canary-release --alternative-to--> rolling-deployment` [editorial] - "Observe a small
  slice before widening vs replace instances a few at a time."
- `scale-rollouts --uses--> rollback-deployment` **[sourced]** - "Gradual rollout monitors effects and rolls
  back the release if a problem appears." *Gradual rollout without automated rollback is incomplete by the
  corpus's own relation.*
- `schema-evolution-via-field-tags --enables--> rolling-deployment` **[sourced]** - "Mixed-version fleets
  require encodings both sides can read."
- `tolerant-reader --enables--> manage-service-interactions` [editorial] - consumers that "extract only what
  they need and ignore unknown content let multiple service versions serve traffic simultaneously."
- `package-dependencies --composes-with--> rollback-deployment` [editorial] - "Immutable, self-contained
  packaged versions make rollback a clean revert to the prior image."
- `deployment-pipeline --uses--> script-deployment-commands` [editorial]; `rollback-deployment --uses-->
  script-deployment-commands` [editorial] - "Automated rollback executes the **same** scripted,
  version-controlled deployment commands to reach the prior state."

### Description artifacts compose into an auditable whole

- `module-view --specializes--> architecture-view` **[sourced]**; `component-and-connector-view
  --specializes--> architecture-view` **[sourced]**; `allocation-view --specializes--> architecture-view`
  **[sourced]**.
- `allocation-view --uses--> module-view` [editorial] - "Allocation views map software elements from module
  (and C&C) views onto environmental structures."
- `architecture-view --uses--> architecture-viewpoint` **[sourced]** - "Each view is constructed following
  the conventions of, and governed by, a **single** viewpoint" (iso42010).
- `architecture-decision-record --composes-with--> architecture-description` [editorial] - "ADRs capture the
  decisions and rationale that accompany and justify an architecture description."
- `context-map --uses--> bounded-context` **[sourced]**; `context-map --uses--> anti-corruption-layer`
  **[sourced]** - "Anti-Corruption Layer is one of the seam relationship types recorded on a context map."
- `procedure-call-connector --uses--> interface-definition-language` **[sourced]** - "RPC/method-invocation
  connectors are defined by an IDL contract that generates stubs and skeletons."
- `generation-gap --enables--> interface-definition-language` [editorial] - IDL toolchains "depend on the
  generated-base-class vs hand-written-subclass split to survive regeneration of stubs."

### Layering styles: which discipline, and its stated alternative

- `clean-architecture --specializes--> layers` **[sourced]**; `clean-architecture --composes-with-->
  hexagonal-architecture` **[sourced]** - "Clean Architecture explicitly synthesizes Ports & Adapters
  (hexagonal) with Onion layering."
- `hexagonal-architecture --alternative-to--> layers` [editorial] - "Ports-and-adapters replaces top-down
  abstraction layering with a **symmetric inside/outside** core boundary." The sharpest available statement
  of the choice.
- `repository --enables--> hexagonal-architecture` [editorial] - "the canonical persistence port";
  `gateway --enables--> hexagonal-architecture` [editorial] - "the canonical outbound adapter."
- `functional-core-imperative-shell --realizes--> hexagonal-architecture` [editorial] - "Pure decision core
  with a thin IO shell realizes the ports-and-adapters dependency direction **at component scale**."
- `modular-monolith --alternative-to--> microservices` [editorial] - "Enforced module boundaries within one
  deployable unit as an alternative to distributing services."
- `plugin --realizes--> microkernel` [editorial] - the plugin is the extension mechanism microkernel /
  plug-in architectures are built from.

### Module state

- `software-module-with-global-state --alternative-to--> stateless-software-module` [editorial] - "The two
  Fluent C module shapes: shared file-scope state vs no state between calls."
- `software-module-with-global-state --realizes--> encapsulate` [editorial] - "File-scope static state behind
  a function interface is the C realization of the encapsulate tactic."
- `stateless-software-module --enables--> introduce-concurrency` [editorial] - "Functions keeping no state
  between calls are reentrant."
- `defensive-copy --realizes--> encapsulate` [editorial] - "Copying mutable inputs/outputs closes the
  aliasing hole in encapsulation, making the interface **the only way** to affect internals." Directly
  relevant to Python, where returning a mutable internal list silently deletes the boundary.
- `module-pattern --realizes--> encapsulate` [editorial]; `opaque-pointer --realizes--> encapsulate`
  [editorial] - the JS and C realizations. Python has neither; note the gap rather than pretend.

---

## Do-not-transpose

| element id | why not |
|---|---|
| `include-guard` | The language already does this. Python caches modules in `sys.modules`, so import is idempotent by construction; there is no multiple-inclusion failure mode to guard against. |
| `x-macro` | C preprocessor code generation. Python's answer is `enum.Enum` plus a dict, or runtime introspection - one source of truth without text substitution. The corpus itself lists `x-macro` among only **6 honestly unbridged** elements: "a coding-level DRY mechanism no specific architecture element deploys." |
| `escaping-ifdef-hell` | C/embedded concern - Python has no conditional compilation. The transposable residue ("confine variant selection to dedicated modules behind a common interface") is already `separated-interface` + `defer-binding`; the `#ifdef` pathology does not arise. |
| `organizing-files-in-modular-c-programs` | The catalog's own problem statement is "C offers no module system." Python has packages. The *rule* transposes (see `self-contained-component`); the header/implementation file patterns do not. Confidence spot-checked; co-source preschernplop is **unverified**. |
| `opaque-pointer` | C/embedded concern: "C has no access control; the incomplete type makes information hiding **compiler-enforced**." Python has no equivalent - no forward declaration, no separate compilation, no ABI. Do not promise Python an enforced-hiding mechanism it lacks; buy enforcement with tooling instead. |
| `hot-code-reload` | Does not transpose as a production mechanism. Erlang/OTP `code_change` keeps old and new versions coexistent under a supervision tree and migrates state; `importlib.reload` rebinds the module object but leaves every existing reference pointing at the old classes and functions, so state handover is unachievable. Python's honest answer is process replacement (`rolling-deployment`, `blue-green-deployment`, `immutable-infrastructure`). Reload is a dev-loop convenience (`uvicorn --reload`, Django autoreload) only. |
| `method-object` | Largely "the language already does this": a closure over locals, `functools.partial`, or a `@dataclass` with `__call__` gets there without a ceremony class. Keep the *name* for the case where the reified computation needs its own tests; do not import it as a recommended refactoring step. |
| `layer-supertype` | Transposes, but should not be imported: it is inheritance-for-reuse, which the arch manifest already flags as an OO degradation. The corpus's own alternative (`mixin`) and the Python answer (`Protocol` + free functions, or a shared dataclass) are both better. |
| `manage-resources-integrability` | Interposes an explicit resource manager so independently developed components can share memory, threads, devices. In Python this collapses into `contextlib` context managers plus a single owning module - the mediator has no work to do at in-process scale. Keep for genuinely multi-tenant or embedded contexts only. |
| `orchestrate`; `discover` (distributed sense) | Cross-process / distributed integrability tactics. `discover`'s in-process residue is real and worth importing (`importlib.metadata.entry_points`); its service-registry sense, and `orchestrate` entirely, belong to a services manifest, not to module boundaries. |

---

## Citable works to add to Sources

Recorded exactly as the corpus records them. **Verification is copied from the bibliographic record
(`explorer/data/corpus.json` and the `works` map in `elements.json`), not from the prose tag** - see the
four discrepancies flagged at the end.

### Process layer - `swe-process` (Pass 7), `lang:python`

| corpus id | author / body, title, year | identifier | area / role | verification |
|---|---|---|---|---|
| `pep8` | G. van Rossum, B. Warsaw & A. Coghlan, *Style Guide for Python Code (PEP 8)*, living (created 2001) | PEP 8; peps.python.org/pep-0008/ | standards / anchor | verified |
| `pep20` | T. Peters, *The Zen of Python (PEP 20)*, living (2004) | PEP 20; peps.python.org/pep-0020/ | standards / core | verified |
| `pep257` | D. Goodger & G. van Rossum, *Docstring Conventions (PEP 257)*, living (2001) | PEP 257; peps.python.org/pep-0257/ | standards / core | verified |
| `black` | Python Software Foundation, *Black - The Uncompromising Code Formatter*, living | black.readthedocs.io | standards / core | verified |
| `ruff` | Astral, *Ruff - an extremely fast Python linter and formatter*, living | docs.astral.sh/ruff | standards / core | verified |
| `pylint` | pylint-dev, *Pylint*, living | pylint.readthedocs.io | standards / core | verified |
| `pep8eyetracking` | P. Roberto, R. Gheyi, J. A. Silva da Costa & M. Ribeiro, *Assessing Python Style Guides: An Eye-Tracking Study with Novice Developers*, 2024 | arXiv:2408.14566 | standards / advanced | verified |
| `pypackaging` | PyPA, *Python Packaging User Guide*, living | packaging.python.org | org-build / anchor | verified |
| `pep517` | N. J. Smith & T. Kluyver, *PEP 517 - A build-system independent format for source trees*, 2015 | PEP 517; peps.python.org/pep-0517/ | org-build / core | verified |
| `pep518` | B. Cannon, N. J. Smith & D. Stufft, *PEP 518 - Specifying Minimum Build System Requirements*, 2016 | PEP 518; peps.python.org/pep-0518/ | org-build / anchor | verified |
| `pep621` | B. Cannon et al., *PEP 621 - Storing project metadata in pyproject.toml*, 2020 | PEP 621; peps.python.org/pep-0621/ | org-build / core | verified |

The corpus's own coverage finding, worth carrying: for Python, `vcs-review` is an explicit **GAP** ("no
language-specific *research*"), and `ci-cd` has no Python-specific anchor - the cell holds only
`precommit`, tagged `lang:multi`. Python's process weight sits in `standards` and `org-build`.

### Process layer - `swe-process` (Pass 7), `lang:agnostic` / `lang:multi`

| corpus id | author / body, title, year | identifier | area / role | verification |
|---|---|---|---|---|
| `mcconnell` | S. McConnell, *Code Complete, 2nd ed.*, 2004 | Microsoft Press, ISBN 978-0-7356-1967-8 | standards / anchor | verified |
| `martincleancode` | R. C. Martin, *Clean Code* | (none recorded) | standards / anchor | **unverified** - record carries `unresolved: [year]`; the R1 membership tag says "verified". Do not present as verified. |
| `smitconventions` | M. Smit, B. Gergel, H. J. Hoover & E. Stroulia, *Maintainability and Source Code Conventions: An Analysis of Open Source Projects*, 2011 | Univ. of Alberta TR11-06 | standards / survey | **unverified** (explicit quarantine; `unresolved: [report-number]`) |
| `uncrustify` | uncrustify project, *Uncrustify (source beautifier)*, living | github.com/uncrustify/uncrustify | standards / core (`multi`) | verified |
| `diataxis` | D. Procida, *Diataxis - a systematic framework for technical documentation*, living | diataxis.fr | documentation / anchor | verified |
| `arc42` | G. Starke & P. Hruschka, *arc42 - architecture documentation template*, living | arc42.org | documentation / core | verified |
| `c4model` | S. Brown, *The C4 model for visualising software architecture*, living | c4model.com | documentation / anchor | verified |
| `nygardadr` | M. Nygard, *Documenting Architecture Decisions*, 2011 | cognitect.com/blog/2011/11/15/documenting-architecture-decisions | documentation / anchor | verified |
| `ettermtw` | A. Etter, *Modern Technical Writing*, 2016 | ASIN B01A2QL9SS | documentation / anchor | verified |
| `parnasclements` | D. L. Parnas & P. C. Clements, *A Rational Design Process: How and Why to Fake It*, 1986 | IEEE TSE SE-12(2):251-257 | documentation / anchor | verified |
| `sphinx` | Sphinx team, *Sphinx documentation generator*, living | sphinx-doc.org | documentation / core (`multi`) | verified |
| `progit` | S. Chacon & B. Straub, *Pro Git, 2nd ed.*, 2014 | ISBN 978-1-4842-0076-6; git-scm.com/book | vcs-review / anchor | verified |
| `gitflow` | V. Driessen, *A successful Git branching model (git-flow)*, 2010 | nvie.com/posts/a-successful-git-branching-model/ | vcs-review / anchor | verified |
| `trunkbased` | P. Hammant et al., *Trunk-Based Development*, living | trunkbaseddevelopment.com | vcs-review / core | verified |
| `githubflow` | GitHub, *GitHub flow*, living | docs.github.com | vcs-review / core | verified |
| `gitlabflow` | GitLab, *GitLab flow*, living | about.gitlab.com/topics/version-control/what-is-gitlab-flow/ | vcs-review / core | verified |
| `convcommits` | Conventional Commits community, *Conventional Commits (v1.0.0)*, living | conventionalcommits.org | vcs-review / core | verified |
| `semver` | T. Preston-Werner, *Semantic Versioning (SemVer 2.0.0)*, living | semver.org | vcs-review / anchor | verified |
| `potvinmonorepo` | R. Potvin & J. Levenberg, *Why Google Stores Billions of Lines of Code in a Single Repository*, 2016 | DOI 10.1145/2854146; CACM 59(7):78-87 | vcs-review / survey | verified |
| `rigbybird` | P. C. Rigby & C. Bird, *Convergent Contemporary Software Peer Review Practices*, 2013 | DOI 10.1145/2491411.2491444 | vcs-review / survey | verified |
| `googleeng` | Google, *Code Review Developer Guide (eng-practices)*, living | google.github.io/eng-practices/review/ | vcs-review / core | verified |
| `cohenreview` | J. Cohen (ed.) et al., *Best Kept Secrets of Peer Code Review*, 2006 | ISBN 978-1-59916-067-2 | vcs-review / core | verified |
| `fagan` | M. E. Fagan, *Design and Code Inspections to Reduce Errors in Program Development*, 1976 | IBM Systems Journal 15(3):182-211 | vcs-review / anchor | verified |
| `wiegers` | K. E. Wiegers, *Peer Reviews in Software: A Practical Guide*, 2002 | Addison-Wesley, ISBN 978-0201734850 | vcs-review / core | verified |
| `bacchellibird` | A. Bacchelli & C. Bird, *Expectations, Outcomes, and Challenges of Modern Code Review*, 2013 | ICSE 2013 pp.712-721; DOI 10.1109/ICSE.2013.6606617 | vcs-review / core | verified |
| `sadowskigoogle` | C. Sadowski, E. Soderberg, L. Church, M. Sipko & A. Bacchelli, *Modern Code Review: A Case Study at Google*, 2018 | ICSE-SEIP 2018; DOI 10.1145/3183519.3183525 | vcs-review / core | verified |
| `fowlerci` | M. Fowler, *Continuous Integration*, living (2000; rewritten 2006; rev. 2024) | martinfowler.com/articles/continuousIntegration.html | ci-cd / anchor | verified |
| `contdeliv` | J. Humble & D. Farley, *Continuous Delivery*, 2010 | ISBN 978-0-321-60191-9 | ci-cd / anchor | verified |
| `accelerate` | N. Forsgren, J. Humble & G. Kim, *Accelerate: The Science of Lean Software and DevOps*, 2018 | ISBN 978-1-942788-33-1 | ci-cd / core | verified |
| `dora` | DORA (Google Cloud), *DevOps Research and Assessment / State of DevOps*, living | dora.dev | ci-cd / core | verified |
| `gitlabci` | GitLab, *GitLab CI/CD documentation*, living | docs.gitlab.com/ci/ | ci-cd / core (`multi`) | verified |
| `precommit` | A. Sottile, *pre-commit (hook framework)*, living | pre-commit.com | ci-cd / core (`multi`) | verified |
| `ieee828` | IEEE, *IEEE 828-2012 - Configuration Management in Systems and Software Engineering*, 2012 | IEEE 828-2012; ISBN 978-0-7381-7134-0 | org-build / anchor | verified |
| `parnas72` | D. L. Parnas, *On the Criteria To Be Used in Decomposing Systems into Modules*, 1972 | CACM 15(12):1053-1058 | org-build / anchor | verified |
| `martincleanarch` | R. C. Martin, *Clean Architecture*, 2017 | (none recorded) | org-build / core | **unverified** - the R5 membership tag says "verified". Do not present as verified. |
| `lakosvol1` | J. Lakos, *Large-Scale C++ Volume I: Process and Architecture*, 2019 | ISBN 978-0-201-71706-8 | org-build / anchor (`cpp`) | verified |
| `lakoslsc` | J. Lakos, *Large-Scale C++ Software Design* | (none recorded) | org-build / anchor (`cpp`) | **unverified** - `unresolved: [year]`; the R5 membership tag says "verified". |

### Element layer - naming sources for the imported elements

| work id | author, title, year | identifier as recorded | verification |
|---|---|---|---|
| `bck` | L. Bass, P. Clements & R. Kazman, *Software Architecture in Practice, 4th ed.*, 2021 | Addison-Wesley SEI, ISBN 978-0-13-688609-9 | verified |
| `vab` | P. Clements, F. Bachmann, L. Bass, D. Garlan, J. Ivers, R. Little, P. Merson, R. Nord & J. Stafford, *Documenting Software Architectures: Views and Beyond, 2nd ed.*, 2010 | Addison-Wesley | verified |
| `iso42010` | ISO/IEC/IEEE, *42010:2022 - Software, systems and enterprise - Architecture description*, 2022 | (no identifier recorded beyond the standard number) | verified |
| `kruchten` | P. Kruchten, *Architectural Blueprints - The 4+1 View Model of Software Architecture*, 1995 | IEEE Software 12(6):42-50 | verified |
| `poeaa` | Martin Fowler (with Rice, Foemmel, Hieatt, Mee, Stafford), *Patterns of Enterprise Application Architecture*, 2002 | martinfowler.com/books/eaa.html - **ISBN deliberately omitted** ("not shown on page, omitted") | verified |
| `posa4` | Buschmann, Henney & Schmidt, *Pattern-Oriented Software Architecture Vol. 4: A Pattern Language for Distributed Computing*, 2007 | Wiley, ISBN 0-470-05902-8 | verified |
| `posa1` | Buschmann, Meunier, Rohnert, Sommerlad & Stal, *Pattern-Oriented Software Architecture Vol. 1: A System of Patterns*, 1996 | Wiley - record notes `UNRESOLVED: isbn/authors` (publisher pages 403); title and year 1996 confirmed live | verified, with an unresolved ISBN field |
| `corbaspec` | Object Management Group, *The Common Object Request Broker: Architecture and Specification*, 1991 | OMG standard (CORBA 1.0, Aug 1991; current 3.4, 2021) | verified |
| `evansddd` | Eric Evans, *Domain-Driven Design: Tackling Complexity in the Heart of Software*, 2003 | Addison-Wesley, ISBN 978-0-321-12521-7 | verified |
| `preschern` | C. Preschern, *Fluent C: Principles, Practices, and Patterns*, 2022 | O'Reilly, 2022-11-22, ISBN 978-1492097334 | verified |
| `preschernplop` | C. Preschern, EuroPLoP/PLoP pattern-paper series | (none) | **unverified**, `unresolved: [year]` - co-source for `stateless-software-module`, `software-module-with-global-state`, `organizing-files-in-modular-c-programs` |
| `vlissideshatching` | John Vlissides, *Pattern Hatching: Design Patterns Applied*, 1998 | Addison-Wesley, ISBN 978-0-201-43293-0 | verified |
| `hodgsontoggles` | Pete Hodgson, *Feature Toggles (aka Feature Flags)*, 2017 | martinfowler.com/articles/feature-toggles.html | verified |
| `immutableserver` | Kief Morris, *ImmutableServer*, 2013 | martinfowler.com bliki (13 June 2013) | verified |
| `k8sdeploy` | The Kubernetes Authors (CNCF), *Kubernetes Documentation - Deployments*, living | kubernetes.io (RollingUpdate; maxSurge/maxUnavailable) | verified |
| `fowlerdi` | Martin Fowler, *Inversion of Control Containers and the Dependency Injection pattern*, 2004 | martinfowler.com/articles/injection.html | verified |
| `meszaros` | Gerard Meszaros, *xUnit Test Patterns: Refactoring Test Code*, 2007 | Addison-Wesley, ISBN 978-0-13-149505-0 | verified |
| `welc` | Michael Feathers, *Working Effectively with Legacy Code*, 2004 | Prentice Hall, ISBN 978-0-13-117705-5 | verified |
| `beckbpp` | Kent Beck, *Smalltalk Best Practice Patterns*, 1997 | Prentice Hall, ISBN 978-0-13-476904-2 | verified |
| `gof` | Gamma, Helm, Johnson & Vlissides, *Design Patterns: Elements of Reusable Object-Oriented Software*, 1994 | Addison-Wesley, ISBN 978-0-201-63361-0 | verified |
| `hexagonalarch` | Alistair Cockburn, *Hexagonal Architecture (Ports and Adapters)*, 2005 | HaT Technical Report 2005.02; alistair.cockburn.us/hexagonal-architecture/ | verified |
| `tolerantreader` | Martin Fowler, *Tolerant Reader (bliki)*, 2011 | martinfowler.com/bliki/TolerantReader.html (9 May 2011) | verified |
| `burnshotcloud` | Brendan Burns & David Oppenheimer, *Design Patterns for Container-based Distributed Systems*, 2016 | USENIX HotCloud 2016 | verified |
| `azurepatterns` | Microsoft (Azure Architecture Center), *Cloud Design Patterns*, living | learn.microsoft.com/azure/architecture/patterns/ | verified - **but caveat**: the work record's title is specifically "Cloud Design Patterns: **Cache-Aside**" while it serves as the naming source for `strangler-fig` and `external-configuration-store`. Cite the per-pattern page, not this record. |
| `monolith2micro` | Sam Newman, *Monolith to Microservices*, 2019 | ISBN 9781492047841 | **unverified** - "O'Reilly publisher page 403; ISBN/year corroborated via OpenLibrary only" |
| `martincleanarch` | R. C. Martin, *Clean Architecture*, 2017 | (none) | **unverified** - naming source for the `clean-architecture` style and a co-source for `humble-object` |
| `fowlerref` | M. Fowler, *Refactoring* | (none) | **unverified**, `unresolved: [year]` - **yet** `method-object` records year 1999 and names "Fowler, Refactoring (1999)". Treat the year as unconfirmed. |
| `meyersxmacros` | Randy Meyers, *The New C: X Macros*, 2001 | C/C++ Users Journal 19(5) | **unverified** (CUJ defunct; archived text only) |
| `erlangcodereplace` | Ericsson AB, *Erlang/OTP System Documentation - Compilation and Code Loading*, living | erlang.org/doc/system/code_loading.html | verified |
| `bernhardtfcis` | Gary Bernhardt, *Functional Core, Imperative Shell*, 2012 | Destroy All Software screencast | verified |

**Four verification discrepancies to carry forward.** `swe_process_corpus_v1_0.md` tags the memberships
`martincleancode`, `lakoslsc`, `martincleanarch` and `cmake` as `verified`, but the merged bibliographic
records in `corpus.json` record all four as **unverified** (three with `unresolved` fields). The corpus's
own rule says memberships "carry only the swe-process tags ... their citation lives in the corpus
already," so the bibliographic record wins. Do not present these four as verified in a manifest Sources
list.

---

## Where the catalogs REFINE or CONTRADICT the manifest's framing

**1. "Reduce coupling" is not one rule - it is three tactics with different costs, and the manifest
states none of them.** The arch manifest (3.1) says "Coupling is not uniformly bad ... Direct, visible
coupling is easier to reason about than diffuse, implicit coupling." True but unactionable. bck names
three distinct moves - `encapsulate` (hide internals), `restrict-dependencies` (forbid the edge),
`use-an-intermediary` (route it) - and the corpus records all three as *sourced* `alternative-to` pairs.
It also splits coupling into two orthogonal axes the manifest fuses: "the **strength** of coupling and
the **syntactic/semantic distance** to be bridged." An agent given the three names can pick; an agent
given "lower is usually better" cannot.

**2. Import-time and run-time dependency are separate tactics.** bck keeps `restrict-dependencies`
(qa:modifiability, "which modules a given module may depend on") apart from
`restrict-communication-paths` (qa:integrability, "the set of elements with which a given element can
communicate"), and the corpus explicitly notes they were "kept separate as bck names both." Python needs
this distinction more than most languages: the import graph and the runtime call graph diverge whenever
DI, entry points, or async tasks are involved. The manifest's single word "coupling" cannot express
"package A may import B but must never call into B at request time."

**3. The manifest's most load-bearing term - "seam" - has no element and no citation.** `seam` appears in
arch manifest 1 (Vocabulary), 4.2 (a whole subsection), and 6 ("Extract seam"), and the testability
argument rests on it. **There is no `seam` element in the corpus** (verified by search over all 1083 ids,
names, akas and `what` fields; the only hits are unrelated - `context-map`, `a-b-firmware-image-update`).
The nearest citable substitutes are `specialized-interfaces` (bck 2021: dedicated, removable test
interfaces), `explicit-interface` (posa4), `dependency-injection` (fowlerdi 2004) and `humble-object`
(meszaros 2007). Either cite Feathers directly for "seam" or rebuild the subsection on those four names -
do not leave the manifest's central lever uncited.

**4. Two named refactorings the manifest recommends do not exist in the corpus at all.**
`branch-by-abstraction` and `parallel-change` (arch manifest 6) return **zero** matches. This is a real
absence, not a search failure: both are process moves, and the element charter admits mechanisms. The
closest citable substitutes are structural - for branch-by-abstraction, `defer-binding` + `feature-flag`
behind a `separated-interface`; for parallel change, `manage-service-interactions` ("multiple versions ...
deployed and executed simultaneously") plus `tolerant-reader`. Also absent: `information-hiding` has **no
element**, even though `parnas72` is a verified corpus work claimed by `org-build`. The element layer has
`encapsulate` instead. Say "encapsulate (bck)" and cite Parnas as the origin of the *criterion*, not of
an element.

**5. The manifest bans global state; the corpus prices it.** Arch manifest 3.2 is flat: "Global state
(module-level mutables, singletons, 'environment' objects populated at startup) **defeats**
unit-testability." The corpus disagrees in three places. (a) `software-module-with-global-state` is a
*named pattern* (Preschern, *Fluent C*) whose stated tradeoff is "one module-internal state blob serves
all callers, trading simplicity for a single shared context," and the corpus explicitly refuses to fold
it into Singleton/Monostate. (b) `registry`'s entry says some objects "cannot sensibly be threaded
through every call chain; a known lookup point provides access **while keeping scope (process, thread,
session) explicit**" - the requirement is explicit scoping, which in Python is `contextvars`, not
abolition. (c) The corpus records `registry --alternative-to--> dependency-injection` and
`service-locator --alternative-to--> dependency-injection` as **sourced** ("Fowler explicitly weighs them
against each other"). Recommended reframing: default to `stateless-software-module`; permit module-level
state as a *declared* exception with an explicit init/cleanup pair and a stated scope; ban only
*implicit* scope.

**6. "Three is the common threshold" for abstraction is asserted without its counterweight.** Arch
manifest 7 says "Abstracting from two examples usually produces the wrong abstraction. Three is the
common threshold." The corpus supplies the opposing tactic with its own cost model:
`abstract-common-services` - "Duplicate similar services multiply **both** modification cost (each copy
changes) **and** integration surface; one abstraction localizes both." And it records a *sourced*
alternative the manifest never considers: `adhere-to-standards --alternative-to-->
abstract-common-services` - conform to a published standard instead of inventing a shared abstraction.
For Python that is the PEP argument: prefer PEP 621 metadata, `Protocol`, `Iterator`, over a house
abstraction. The rule of three should be stated as a *default on an axis with two named exits*, not as a
threshold.

**7. Modularity's real cost is not readability - it is per-event overhead, and bck names it.** Arch
manifest 7 says "Performance vs. readability. Usually overstated." The corpus's
`reduce-computational-overhead` states the actual tradeoff: "Intermediaries and separation of concerns -
valuable for modifiability - add per-event processing and communication cost; **this is the classic
modifiability/performance trade-off**." `use-an-intermediary` repeats it ("at some performance cost"),
and `layers` prices layering as "indirection and pass-through overhead." The manifest is missing the axis
entirely, and it is the axis that decides whether a boundary becomes an in-process call, a queue, or a
service.

**8. Documentation is three artifacts, not one diagram - and the manifest has none of them.** vab's
viewtype triple is a hard partition by *concern*: `module-view` for "construction,
modification-impact analysis, and work assignment"; `component-and-connector-view` for runtime structure,
because "static module structure says little about runtime behavior, concurrency, or data flow";
`allocation-view` for the mapping to files, machines and **teams**. iso42010 adds the governing rule: each
view "is constructed following the conventions of, and governed by, a **single** viewpoint." The manifest
has no documentation section at all, so `python_module_boundaries_manifest.md` should introduce all three -
and in Python the module/C&C divergence is the norm, not an edge case.

**9. Refactoring in the manifest is a *list*; in the corpus it is an *ordered composition*.** The corpus
states `split-module --composes-with--> redistribute-responsibilities`: "split a non-cohesive module,
**then** move related responsibilities together." And it gives bck's operational criterion the manifest
lacks: responsibilities are misallocated when "one likely change touches many modules, **or** a module
contains parts untouched by any scenario." That second clause is a test an agent can actually run against
a git history. It also scales down: `method-object --realizes--> split-module` makes the same tactic apply
at method scale, so one vocabulary covers both.

**10. Gradual rollout without automated rollback is incomplete by the corpus's own relation.** The corpus
records `scale-rollouts --uses--> rollback-deployment` as **sourced**. It also keeps two same-name
mechanisms apart: `rollback-deployment` ("revert a defective ... deployment to its prior state, tracking
or being able to reverse the coordinated updates to multiple services **and their data**") versus the
availability `rollback-tactic` (revert runtime state to a checkpoint). A quality-gates manifest that says
"roll back on failure" without naming which one, and without the data clause, is underspecified. The
corpus also supplies the cheaper alternative explicitly: `feature-toggle --alternative-to-->
rollback-deployment`.

**11. "Feature flag" is two elements, deliberately.** The corpus's same-name rule keeps `feature-flag`
(design/code-structure: "a toggle point whose path is selected at runtime by a toggle router reading
external toggle configuration") separate from `feature-toggle` (architecture/tactic: the kill switch) and
from `feature-flag-driven-release` (deployment: "release becomes a configuration act"), bridged by
`feature-flag --realizes--> feature-toggle`. Three decisions, three names: *do I need a toggle point*, *do
I need a kill switch*, *is release now a config change*. And one enforceable rule straight from a
**sourced** edge: `feature-flag --composes-with--> strategy` - "Long-lived toggles are best realized by
selecting a Strategy implementation **rather than inline conditionals**."

**12. The corpus deliberately has no process elements - so a quality-gates manifest must cite works, not
elements.** Verified by search: there is no element for code review, trunk-based development, semantic
versioning, monorepo, pre-commit, or linting. `deployment-pipeline` is the sole crossover, and it carries
a `borderline` note admitting exactly this: "Practice-adjacent (CI/CD is pass-7 territory), but the
pipeline itself is a named, recurring structure - stages, gates, artifact promotion - not just a
practice." `immutable-infrastructure` carries the same admission. Consequence for
`python_quality_gates_manifest.md`: its vocabulary comes from Pass 7 works (PEP 8/257, Ruff, Black,
Pylint, pre-commit, Conventional Commits, SemVer, Trunk-Based Development, Google eng-practices,
Continuous Delivery, DORA) plus the *structural* elements (`deployment-pipeline`,
`script-deployment-commands`, `package-dependencies`, `limit-structural-complexity`,
`specialized-interfaces`, `executable-assertions`). Do not go looking for a "code-review" element - the
absence is deliberate and load-bearing.

**13. `layers` and `hexagonal-architecture` are alternatives, not a progression.** The manifest's paradigm
menu (2) lists "Modular" and "Object-oriented" but never states the layering choice. The corpus does,
sharply: `hexagonal-architecture --alternative-to--> layers` - "Ports-and-adapters replaces top-down
abstraction layering with a **symmetric inside/outside** core boundary" - while `clean-architecture
--specializes--> layers` and `--composes-with--> hexagonal-architecture` (both **sourced**) show Clean
Architecture as the synthesis, not a third option. `layers`' own entry names the price: layered
dependencies buy "exchangeability, portability, and independent evolution at the cost of indirection and
pass-through overhead." For Python, `functional-core-imperative-shell` (Bernhardt 2012) is recorded as
realizing hexagonal "at component scale" - the cheap version that needs no framework. Note the citation
asymmetry: `hexagonal-architecture` is verified (Cockburn 2005) while `clean-architecture`'s naming work
`martincleanarch` is **unverified**.

**14. Undated and spot-checked elements to handle carefully.** Of the elements imported above,
`rolling-deployment` and `strangler-fig` have `year: null` (the corpus has 89 undated elements overall);
`separated-interface`, `explicit-interface`, `plugin`, `layer-supertype`, `registry`, `facade`,
`feature-flag`, `service-stub`, `golden-master-testing`, `organizing-files-in-modular-c-programs` and
`modular-monolith` carry `confidence: spot-checked` rather than `established`. Neither weakens the name;
both mean "do not attach a firm date or claim canonical status in prose."
