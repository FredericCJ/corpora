# Testability and verification - seed pack (mined 2026-08-08)

**Corpus mined:** `SWE/explorer/data/elements.json` (1083 nodes / 2811 edges / 417 work records),
`design_elements_catalog_v1_0.md` (including its *Granularity/altitude decisions* and *Notable
exclusions* registers), `architecture_elements_catalog_v1_0.md`, `design_elements_corpus_v1_0.md`,
`explorer/data/corpus.json`, `design_elements_bridge_v1_1.md`.

**Targets:** `manifests/python_testing_tooling_manifest.md` (PY), `manifests/architecture_manifest_default.md` §4 (ARCH).

**Slice census.** 11 `design/testing-constructs` elements (all verified present); 7 `qa:testability`
architecture tactics + `sandbox` (pattern, `qa:[testability, security]`); 9 seam-creating
`construction-api`/`oo-patterns` elements; `functional-core-imperative-shell`; `humble-object`.
The graph-wide sweep for `what`/`problem` text mentioning testing, doubles, determinism, or
observability-under-test returned 155 nodes; 26 were read in full and 9 non-slice ones earned a row below.

**Realizer census (the load-bearing number).** Design-realm `realizes` edges into each testability tactic:
`limit-nondeterminism` 6 · `limit-structural-complexity` 4 · `abstract-data-sources` 3 ·
`executable-assertions` 3 · `sandbox` 2 · `localize-state-storage` 1 · `record-playback` 1 ·
**`specialized-interfaces` 0**. The last is an honest hole in a 709-element catalog: nothing at code
level is named for test-only control/observation interfaces (see Refine, point 7).

---

## Import table

| element id | realm/kind | catalog name | named-in (citable) | Python instantiation | destination manifest + section |
|---|---|---|---|---|---|
| `four-phase-test` | design / testing-constructs | Four-Phase Test | Meszaros, *xUnit Test Patterns* (2007), ISBN 978-0-13-149505-0; xunitpatterns.com "Four Phase Test" | The four phases map to: fixture arg-injection (`@pytest.fixture` requested by parameter name) → the single call under test → `assert` / `pytest.raises` → teardown after `yield` in the fixture or `request.addfinalizer`. `monkeypatch` and `tmp_path` make phase 4 automatic. Rule: one behavior per test, teardown never in the test body. | PY — new §3 subsection "Test shape", ahead of the double taxonomy |
| `test-data-builder` | design / testing-constructs | Test Data Builder | Nat Pryce, "Test Data Builders: an alternative to the Object Mother pattern" (2007); book form in Freeman & Pryce, *GOOS* (2009), ISBN 978-0-321-50362-6 | A frozen `@dataclass` plus `dataclasses.replace(default_order, total=Money(0))`, or a `with_*` fluent builder, or `hypothesis.strategies.builds(Order, total=...)`. `polyfactory` / `factory_boy` are the library forms. Catalog's rule transposes verbatim: "a builder makes the significant values explicit while defaulting the rest". | PY — new §6 subsection "Constructing test data" |
| `object-mother` | design / testing-constructs | Object Mother | Schuh & Punke, "ObjectMother: Easing Test Object Creation in XP" (XP Universe 2001) — **naming source has no corpus work record**; corpus covering work is Meszaros (2007) | A `conftest.py` module of fixtures or plain functions returning canonical exemplars (`overdue_invoice()`, `standard_customer()`). Import it as the *named alternative you are rejecting* (see the sourced `alternative-to` edge), not as a recommendation. | PY — same subsection, as the alternative |
| `golden-master-testing` | design / testing-constructs | Golden Master Testing | Feathers, *Working Effectively with Legacy Code* (2004), ISBN 978-0-13-117705-5 ("characterization test"); ApprovalTests; Jest "snapshot testing" (both aka-only, no corpus record) | Write observed output to a versioned file under `tests/golden/`, compare on rerun, gate regeneration behind an explicit `--approve` / `--snapshot-update` flag registered via `pytest_addoption`. Library forms: `syrupy`, `pytest-regressions`, `approvaltests`. **Requires** `canonical-serialization` (next row) or it flakes. | PY — new §6 subsection "Recorded-output tests" |
| `canonical-serialization` | design / serialization-framing | Canonical Serialization | ITU-T X.690 DER (02/2021); RFC 8785 JSON Canonicalization Scheme (2020) | `json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":"))`; normalize timestamps, uuids, paths and float formatting before writing the master. Imported only because it is the precondition the golden-master edge names. | PY — same subsection |
| `humble-object` | design / testing-constructs | Humble Object | Meszaros, *xUnit Test Patterns* (2007) | The framework touchpoint keeps zero logic: a Click/argparse `main()` that only parses and calls one function; a FastAPI route body that is one call; a thread / `asyncio` task wrapper that only awaits. The extracted collaborator is what tests import. The *local, retrofittable* form of the FCIS the manifest already recommends. | PY — §7, beside functional-core/imperative-shell |
| `page-object` | design / testing-constructs | Page Object | Fowler, bliki "PageObject" (2013) — records that it was first described as Window Driver at eaaDev and popularized by Selenium | A test-side class wrapping an application surface behind intention-revealing methods: Playwright/Selenium page wrappers, or `httpx.ASGITransport` / `TestClient` wrappers (`api.place_order(...)` rather than `client.post("/orders", json=...)`). Import only if the project drives a UI or HTTP surface. | PY — §6, integration-layer subsection |
| `gateway` | design / communication | Gateway | Fowler, *PoEAA* (2002) | One application-owned class per external system, with the method set shaped for the caller rather than the vendor API (`class PaymentGateway: def charge(self, amount: Money) -> ChargeId`). This is the object the manifest's "substitute a fake client" advice presupposes but never names. Catalog wording worth quoting: external APIs are "awkward, unstable, and hard to fake". | PY — §6, "Fakes / test harnesses" (rename the heading to name the gateway) |
| `separated-interface` | design / oo-patterns | Separated Interface | Fowler, *PoEAA* (2002) | The `Protocol` lives in the *consumer's* module (`billing/ports.py`), the implementation in `billing/adapters/stripe.py`. Consequence in Python: no import from consumer → adapter, so the test fake needs no third package and `mypy` checks both sides against one declaration. Answers the question the manifest's "Protocol-typed seams" leaves open — *where does the Protocol live*. | PY — §7, under Protocol-typed dependencies |
| `service-locator` | design / construction-api | Service Locator | Alur, Crupi & Malks, *Core J2EE Patterns* (2001) — **naming source has no corpus work record**; corpus covering works are Fowler (2004) and Nystrom (2014) | The Python forms are ordinary: a module-level singleton, `get_settings()`, `current_app`, `django.conf.settings`, a `REGISTRY` dict. Import it *as the named alternative DI is chosen against* — the locator keeps the dependency out of the signature, so tests must `monkeypatch` a global instead of passing an argument. | PY — §7, as the rejected alternative to DI |
| `plugin` | design / construction-api | Plugin | Fowler, *PoEAA* (2002) | `importlib.metadata.entry_points(group=...)`; pytest's own `pytest11` entry point and `conftest.py`; a `--backend=fake\|real` option registered with `pytest_addoption` selecting the implementation at collection time. The catalog's problem statement lists "test doubles" among the things Plugin exists to substitute. | PY — §1 (config) and §6 (choosing the real-vs-fake edge) |
| `design-by-contract` | design / construction-api | Design by Contract | Meyer, *Object-Oriented Software Construction* (element cites the 1988 1st ed.; corpus work record is the 1997 2nd ed.) | `__post_init__` invariant checks on frozen dataclasses; explicit `if not cond: raise ValueError` for contracts that must survive `-O`; `icontract` / `deal` decorators; `typing.assert_never` for exhaustiveness. The half the manifest lacks entirely is **blame assignment**: a failed precondition indicts the caller, a failed postcondition indicts the callee, and that decides which test is missing. | PY — §5 (obligations) |
| `smart-constructor` | design / construction-api | Smart Constructor | "Smart constructors", Haskell wiki (living) | One `@classmethod parse()` / `NewType` plus validating factory / `pydantic` model as the only exported way to build the value; the raw `__init__` stays private by convention. Testability payoff: obligations that would have been error-path tests on every consumer collapse into one construction test. | PY — §5, beside error-path obligations |
| `pseudorandom-number-generator` | design / numeric-precision | Pseudorandom Number Generator | Knuth, *TAOCP Vol. 2*, 3rd ed. (1997), ISBN 0-201-89684-2, ch. 3 "Random Numbers" | Inject a `random.Random(seed)` instance (never module-level `random.*`); `numpy.random.default_rng(seed)`; set `PYTHONHASHSEED` for iteration-order stability; Hypothesis's own seed is what makes `@reproduce_failure` work. Catalog wording: the seed makes randomness "exactly reproducible for replay and debugging". | PY — §4 and §6 (determinism) |
| `epsilon-ulp-float-comparison` | design / numeric-precision | Epsilon/ULP Floating-Point Comparison | Bruce Dawson, "Comparing Floating Point Numbers, 2012 Edition" (2012); ULP framing also Knuth TAOCP v2 and Goldberg (1991) | `pytest.approx(expected, rel=..., abs=...)`, `math.isclose` (PEP 485), `numpy.testing.assert_allclose`. The catalog's point is the one that bites: "a fixed absolute epsilon is wrong across magnitudes" — so a bare `abs=1e-9` gate is a latent flake, and near-zero needs the absolute term stated explicitly. | PY — §5, expected-observable rules |
| `structured-concurrency` | design / execution-concurrency | Structured Concurrency | Nathaniel J. Smith, "Notes on structured concurrency, or: Go statement considered harmful" (vorpus.org, 2018); Trio nurseries; JEP 453 | `asyncio.TaskGroup` (3.11+) and `asyncio.timeout`; trio nurseries. Cited realizer of `limit-nondeterminism`: no detached tasks means no test that passes because a stray task had not run yet. Ban bare `asyncio.create_task` outside a scope in test-covered code. | PY — §6 (isolation); ARCH §4.4 |
| `abstract-data-sources` | architecture / tactic | Abstract Data Sources | Bass, Clements & Kazman, *SAIP* 4th ed. (2021), ISBN 978-0-13-688609-9 | A `DataSource` Protocol behind which sit "real DB" and "fixture file"; `pytest_generate_tests` / `parametrize` over data files under `tests/data/`; `tmp_path` plus a fixture-written file. Tactic wording: repoint "from a production customer database to test databases or data files without changing functional code". | ARCH §4 (new §4.5) + PY §6 |
| `executable-assertions` | architecture / tactic | Executable Assertions | Bass, Clements & Kazman, *SAIP* 4th ed. (2021) | Placed "wherever the data is referenced or modified". Python has three different lifetimes the manifest must distinguish: pytest-rewritten `assert` (test modules only), plain `assert` (**vanishes under `-O`**), explicit `raise` (survives). The tactic's framing is the useful import: assertions "embed the test oracle in the code". | ARCH §4 (new §4.5) + PY §5 |
| `localize-state-storage` | architecture / tactic | Localize State Storage | Bass, Clements & Kazman, *SAIP* 4th ed. (2021) | One frozen dataclass (or one `State` enum plus explicit transition function) holding all mutable state, threaded explicitly; tests construct it at *any* value with `dataclasses.replace` instead of driving the system there. Sole cataloged realizer is `finite-state-machine`, and the tactic text itself names "a state machine object" as the mechanism. | ARCH §4 (new §4.5); cross-ref ARCH §3.2 |
| `record-playback` | architecture / tactic | Record/Playback | Bass, Clements & Kazman, *SAIP* 4th ed. (2021) | Cassette recording at a Protocol boundary: `vcrpy` / `betamax` for HTTP, `responses` / `respx` for replay-only, or a hand-rolled decorator writing JSONL of `(call, args, result)` that a fake replays. Distinct from golden-master: golden-master records the *output*, record/playback records what *crossed the interface*, so the fault-inducing state can be re-entered. | ARCH §4 (new §4.5) + PY §6 |
| `specialized-interfaces` | architecture / tactic | Specialized Interfaces | Bass, Clements & Kazman, *SAIP* 4th ed. (2021) | `debug_state() -> Mapping[str, object]`, `reset_for_test()`, a `verbose=` / instrumentation switch, `__getstate__`. The tactic's own stated cost is the import-worthy part; and see Refine point 7 — its "clearly separated so they can be removed" half does **not** transpose to Python. | ARCH §4 (new §4.5) |
| `sandbox` | architecture / pattern | Sandbox | Bass, Clements & Kazman, *SAIP* 4th ed. (2021) | The *resource-virtualization* half is the Python test answer: `tmp_path`, `monkeypatch.setenv`, `pyfakefs`, `freezegun` / `time-machine`, `pytest-socket` to block the network, `sqlite3` `:memory:`, subprocess isolation via `sys.executable -I`. The OS-confinement half (seccomp/jail) is out of scope for a test suite. Catalog wording names the motivating case exactly: "waiting for a real time boundary". | ARCH §4 (new §4.5) + PY §6 |
| `hexagonal-architecture` | architecture / style | Hexagonal Architecture (Ports and Adapters) | Alistair Cockburn, "Hexagonal Architecture" (2005), HaT Technical Report 2005.02 | `app/ports.py` (Protocols) + `app/adapters/*` + a pure core; the test suite is *one of the adapters*, which is the whole point of the citation. Absent from the ARCH paradigm menu (§2) even though `functional-core-imperative-shell` **realizes** it and `gateway` / `repository` / `effect-handler` all **enable** it. | ARCH §2 (paradigm menu), with a pointer from §4.2 |

---

## Fold table

| element id | catalog name | the manifest already calls this | note |
|---|---|---|---|
| `test-double` | Test Double | PY §3 "Test doubles, precisely" — the full dummy/fake/stub/spy/mock taxonomy; ARCH §4.3 | Fold, but the catalog's fold is the sharper claim: it collapses all five into **one element** ("Folded mock/stub/fake/spy/dummy into one element per charter"). See Refine point 1 — the five are settings on one axis, not five mechanisms. |
| `test-fixture` | Test Fixture | PY §1 (pytest fixtures, five scopes) and §6 ("fixtures … are version-controlled code") | Fold the word; the catalog's `aka` carries **Fresh Fixture / Shared Fixture** and its `problem` calls fixture strategy "the named design decision". The manifest has the tooling and not the decision — Refine point 5. |
| `parameterized-test` | Parameterized Test | PY §1 `@pytest.mark.parametrize` | Fold. Synonyms to record: table-driven test (Go), data-driven test, row test. The catalog notes Meszaros's "Data-Driven Test" as the externalized-data variation — that is the `abstract-data-sources` route. |
| `property-based-testing` | Property-Based Testing | PY §4 (whole section, Hypothesis) | Fold the concept; **add the naming source** — Claessen & Hughes, "QuickCheck" (ICFP 2000) is absent from the manifest's Sources even though §4 is entirely about its descendant. |
| `service-stub` | Service Stub | PY §6 "substitute a fake client" / "fakes for external systems" | Fold, with the synonym "mock service". The half worth keeping is that a service stub "implements the same gateway interface" — hence `gateway` is imported and this one is not. |
| `dependency-injection` | Dependency Injection | PY §7 "Dependency injection in Python" | Fold. Aka to record: constructor / setter / interface injection. What is missing is the *competitor* — `service-locator`, imported above. |
| `explicit-interface` | Explicit Interface | PY §7 "Protocol-typed dependencies (typing.Protocol / PEP 544)" | Fold — `typing.Protocol` *is* this element in Python. `separated-interface` is imported separately because it answers a different question (packaging, not typing). |
| `functional-core-imperative-shell` | Functional Core, Imperative Shell | PY §6 (host-side testing) and §7 (whole bullet, Bernhardt) | Fold, but record the aka **"impureim sandwich"** and the sourced `alternative-to monad` edge — both absent from the manifest. |
| `limit-nondeterminism` | Limit Nondeterminism | ARCH §4.4 "Determinism" (time / randomness / concurrency / I/O ordering) | Fold the name onto §4.4 — it is the same tactic. But §4.4 is missing the tactic's own escape clause (`uses record-playback`): Refine point 4. |
| `limit-structural-complexity` | Limit Structural Complexity | ARCH §3.1 (coupling/cohesion) and §4.1 ("instantiable in isolation — a design property") | Fold. §3.1 argues coupling for modifiability and never states the testability rationale the tactic gives: large operational state spaces make recreating an exact state — and so reproducing a failure — hard. |
| `finite-state-machine` | Finite State Machine | ARCH §5.4 "state transition tracing"; §3.2 state ownership | Fold the noun. Worth stating: it is the **only** cataloged realizer of `localize-state-storage`, and that edge is `sourced` to the tactic text naming "a state machine object". |
| `thread-confinement` | Thread Confinement | ARCH §3.4 "Message-passing. Each unit of state is owned by one task" | Fold. Cited realizer of `limit-nondeterminism` (Goetz et al., *JCiP* 2006). Python forms: single-threaded event loop, `threading.local`, `contextvars`. |

---

## Relations worth stating

### The mapping that turns a tool list into an architecture rule

Every `design/testing-constructs` element carries exactly one `realizes` edge into a `qa:testability`
architecture element. That is the sentence the PY manifest is missing: *a testing construct is chosen
because of the tactic it realizes.*

| construct | realizes | edge note (verbatim) | prov |
|---|---|---|---|
| `test-double` | `limit-nondeterminism` | "Replacing a production dependency with a controlled double removes a source of behavioral nondeterminism from the test." | editorial |
| `test-fixture` | `sandbox` | "An arranged, controlled pre-test state isolates the SUT in a known environment for repeatable experimentation." | editorial |
| `service-stub` | `sandbox` | "Substituting an in-process stand-in for a problematic external service isolates the SUT from the real world for testing." | editorial |
| `object-mother` | `abstract-data-sources` | "A factory of ready-made canonical example objects supplies substitutable test data to tests." | editorial |
| `test-data-builder` | `abstract-data-sources` | "A defaulting fluent builder constructs substitutable, easily-varied test data for tests." | editorial |
| `parameterized-test` | `abstract-data-sources` | "Running one test body per row of an input/expected table abstracts test inputs into a substitutable data source." | editorial |
| `four-phase-test` | `executable-assertions` | "The result-verification phase of the four-phase structure is where executable assertions on the SUT's output live." | editorial |
| `property-based-testing` | `executable-assertions` | "Checking a universally-quantified property over many generated inputs is executable assertions over drawn data." | editorial |
| `golden-master-testing` | `record-playback` | "Capturing the full observed output as a stored reference and asserting equality is record/playback applied to test verification." | editorial |
| `humble-object` | `limit-structural-complexity` | "Stripping hard-to-test glue to a trivial shell isolates and encapsulates the environmental dependency away from testable logic." | editorial |
| `page-object` | `limit-structural-complexity` | "Wrapping a UI page behind an application-specific API isolates the volatile UI structure behind a stable test interface." | editorial |

**Rule the PY manifest should state outright:** there are three reasons to substitute, not one.
Substitute to *virtualize an uncontrollable resource* (`sandbox`: clock, network, filesystem, battery);
to *remove behavioral variance* (`limit-nondeterminism`: a collaborator that could answer differently);
to *supply controlled inputs* (`abstract-data-sources`: the data itself). Different exit criteria follow.
The manifest files all three under one §6 heading, so it cannot say when a substitution is *done*.

### Sourced edges that decide a design question

- `limit-nondeterminism` **uses** `record-playback` — *sourced*, cite: Bass, Clements & Kazman, SAIP 4e,
  Testability ch., Limit Nondeterminism tactic. Note: "Where nondeterminism is unavoidable, the tactic says
  to manage it with tactics like record/playback." **The escape clause the PY manifest lacks.**
- `test-data-builder` **alternative-to** `object-mother` — *sourced*, cite: Nat Pryce, "Test Data Builders:
  an alternative to the Object Mother pattern" (2007). The tradeoff is in the title.
- `service-locator` **alternative-to** `dependency-injection` — *sourced*, cite: Fowler, "Inversion of
  Control Containers and the Dependency Injection pattern" — "Fowler explicitly weighs them against each
  other." The same article the manifest already leans on for DI.
- `registry` **alternative-to** `dependency-injection` — *sourced*, same article: "Looking services up in a
  Registry/Service Locator vs having them injected are competing ways to obtain collaborators."
- `separated-interface` **composes-with** `dependency-injection` — *sourced*, Fowler PoEAA: "DI wires the
  concrete implementation to a client that depends only on the separated interface." The two-part rule for
  a Python seam: Protocol in the consumer package, wiring at the edge.
- `gateway` **composes-with** `service-stub` — *sourced*, Fowler PoEAA, Gateway: "Code behind a Gateway is
  tested by substituting a Service Stub for the external resource." The manifest's §6 advice with its
  missing subject supplied.
- `property-based-testing` **uses** `pseudorandom-number-generator` — *sourced*, Claessen & Hughes (ICFP
  2000): "Generators draw inputs from a seeded PRNG; the seed makes failing cases reproducible/shrinkable."
- `four-phase-test` **uses** `test-fixture` — *sourced*, Meszaros, "Four-Phase Test" / "Fixture Setup":
  "Phase 1 (setup) constructs the test fixture the exercise phase runs against."
- `plugin` **uses** `separated-interface` and **composes-with** `service-locator` — both *sourced*, Fowler
  PoEAA, Plugin. Config-time substitution needs a declared interface plus a resolution point; pytest is the
  worked example of both.
- `finite-state-machine` **realizes** `localize-state-storage` — *sourced*: "the tactic text itself names
  the state machine as its realization."
- `functional-core-imperative-shell` **alternative-to** `monad` — *sourced*, cite: Mark Seemann, "Impureim
  sandwich" (ploeh blog, 2020) — **cited on the edge only; no corpus work record exists for it.**
- `limit-structural-complexity` **composes-with** `limit-nondeterminism` / **uses** `encapsulate` /
  **composes-with** `restrict-dependencies` — all *sourced* to SAIP 4e's Testability chapter. The
  architecture rule: cutting coupling and removing nondeterminism are the *same* limit-complexity move.
- `page-object` **specializes** `humble-object` — cite: Fowler, "PageObject": "A Page Object is a Humble
  Object for the UI: assertion-free wrapper delegating to test logic."

### Editorial edges worth stating anyway (marked as judgments, not facts)

- `golden-master-testing` **uses** `canonical-serialization` — "The recorded output must be canonicalized
  (stable ordering, normalized noise) so reruns match the stored master." *The single most common cause of
  flaky snapshot suites, derivable from one edge.*
- `functional-core-imperative-shell` **realizes** `hexagonal-architecture` — "Pure decision core with a thin
  IO shell realizes the ports-and-adapters dependency direction at component scale." Also **composes-with**
  `humble-object` — the same move at two altitudes.
- `design-by-contract` **realizes** `executable-assertions`; `smart-constructor` **composes-with**
  `design-by-contract` ("where the class invariant assumed by later contracts is first established and
  guaranteed") and **realizes** `exception-prevention`. Chain to state: validate once at construction → later
  contracts may assume it → whole error-path test families disappear.
- `epsilon-ulp-float-comparison` **composes-with** `property-based-testing` — "Numeric properties are
  asserted with approximate (epsilon/ULP) equality rather than exact ==." Directly applicable to the
  manifest's §4 round-trip and oracle property classes.
- `parameterized-test` **alternative-to** `property-based-testing`, and `golden-master-testing`
  **alternative-to** `property-based-testing` — three ways to stop hand-writing expected values (table rows
  / universal properties / approved recording). The manifest names one.
- `abstract-data-sources` **composes-with** `defer-binding` ("repointing to test data without code change
  relies on binding the concrete data source late (deploy/test time)") and **uses** `encapsulate`.
- `executable-assertions` **composes-with** `record-playback` — "Assertions detect the moment state goes
  bad; record/playback replays the recorded state to reproduce that fault." The two halves of a
  reproducible-failure workflow.
- `specialized-interfaces` **composes-with** `localize-state-storage`, and `record-playback`
  **composes-with** `localize-state-storage` — both control-and-observe tactics read and write the single
  state store. Together with `finite-state-machine realizes localize-state-storage`, that is a four-element
  rule: put state in one object, expose it, record it, replay it.
- `sandbox` **specializes** `limit-access` — the same pattern serves `qa:testability` and `qa:security`; the
  ARCH manifest should note the dual reading rather than pick one.

---

## Do-not-transpose

| element id | reason not to import |
|---|---|
| `functional-options` | Python has keyword arguments with defaults; the pattern's whole problem ("constructors with many optional parameters degenerate into config structs or telescoping overloads") does not exist. A Go/C++ answer to a Python non-problem. |
| `static-factory-method` | `@classmethod` alternate constructors are the language's own form, and Python constructors can already be named, cached, and covariant. Its one testability-bearing refinement, `smart-constructor`, is imported instead. |
| `marker-interface` | Depends on compile-time membership checks Python does not have; `@runtime_checkable` Protocols check member *existence* only (PY §7 already states this correctly). Do not import as a "type-level test hook". |
| `effect-handler` | No delimited-control primitive in Python; algebraic effects are an OCaml 5 / Koka construct. Its claimed payoff — "testing without mocks" — is delivered in Python by `separated-interface` plus DI, already imported. |
| `free-monad` | Expressible but not idiomatic in Python and unreadable in practice; its payoff ("multiple interpreters — production, test, dry-run, logging — over one program value") is what a Protocol with several implementations already gives. |
| `built-in-self-test`, `self-test` | Firmware and hardware integrity: RAM march tests, ROM CRC, peripheral loopbacks, `composes-with watchdog`. An availability tactic, not a test-suite construct. |
| `hardware-proxy`, `hardware-abstraction-layer` | Register-level embedded seams; the facade-backend variant moves the seam to the *build*, which Python has no analogue for. |
| `fixed-timestep`, `deterministic-lockstep` | Cited realizers of `limit-nondeterminism`, but the domain is game loops and netcode. The transferable residue is one sentence — advance simulated time by a fixed injected step rather than reading a clock — which `sandbox` plus an injected clock already covers. |
| `comparand` | Cheap identity testing via a dedicated value; Python has object identity and `__eq__` / `__hash__`. Not a testing element despite the word "testing" in its `what`. |
| `record-playback` — **caveat, not an exclusion** | Imported above, but read the small print: the tactic records "information as it crosses interfaces". Recording *inside* a Python process usually means monkeypatching, which records the patch rather than the boundary. Record only at a declared Protocol/gateway boundary, or the cassette encodes your test harness. |

---

## Citable works to add to Sources

Identifiers exactly as recorded in `SWE/design_elements_corpus_v1_0.md` and
`explorer/data/elements.json`. "Corpus-verified" means a primary or publisher page was loaded live during
corpus compilation confirming the *identifier*; it does not attest quotations or page numbers.

**Verified in the corpus:**

- Gerard Meszaros. *xUnit Test Patterns: Refactoring Test Code*. 2007. Addison-Wesley. **ISBN 978-0-13-149505-0.** (verified; InformIT page loaded live.) — Upgrades the PY manifest, which currently reaches Meszaros only "via Fowler's articles".
- Michael Feathers. *Working Effectively with Legacy Code*. 2004. Prentice Hall. **ISBN 978-0-13-117705-5.** (verified.) — The corpus reads it as the naming source for characterization / golden-master testing, a use the manifest does not make.
- Steve Freeman & Nat Pryce. *Growing Object-Oriented Software, Guided by Tests*. 2009. Addison-Wesley. **ISBN 978-0-321-50362-6.** (verified.)
- Koen Claessen & John Hughes. "QuickCheck: A Lightweight Tool for Random Testing of Haskell Programs". 2000. ICFP 2000 / official QuickCheck page, Chalmers. https://www.cse.chalmers.se/~rjmh/QuickCheck/ (verified; **DOI omitted in the corpus** — ACM DL returned 403.)
- L. Bass, P. Clements & R. Kazman. *Software Architecture in Practice*, 4th ed. 2021. Addison-Wesley / SEI. **ISBN 978-0-13-688609-9.** (verified.) — Source of all seven testability tactics and of `sandbox`.
- Martin Fowler (with Rice, Foemmel, Hieatt, Mee, Stafford). *Patterns of Enterprise Application Architecture*. 2002. Addison-Wesley. https://martinfowler.com/books/eaa.html (verified; **ISBN not shown on the page and omitted rather than guessed**.) — Gateway, Separated Interface, Plugin, Service Stub, Repository.
- Martin Fowler. "Inversion of Control Containers and the Dependency Injection pattern". 2004. https://martinfowler.com/articles/injection.html (verified, 23 Jan 2004.)
- Martin Fowler. "PageObject" (bliki). 2013. https://martinfowler.com/bliki/PageObject.html (verified, 10 Sep 2013.)
- Bertrand Meyer. *Object-Oriented Software Construction*, 2nd ed. 1997. Prentice Hall. https://bertrandmeyer.com/oosc2/ (verified; **ISBN not shown on the author's page and omitted**.) — Note the discrepancy: the element's `named-in` says "Meyer (1988)" (1st ed.) while the corpus work record is the 1997 2nd ed.
- Haskell wiki contributors. "Smart constructors". Living. https://wiki.haskell.org/Smart_constructors (verified.)
- Alistair Cockburn. "Hexagonal Architecture (Ports and Adapters)". 2005. HaT Technical Report 2005.02. https://alistair.cockburn.us/hexagonal-architecture/ (verified, dated 2005-09-04.)
- Buschmann, Henney & Schmidt. *Pattern-Oriented Software Architecture Vol. 4: A Pattern Language for Distributed Computing*. 2007. Wiley. **ISBN 0-470-05902-8.** (verified.) — Covering work for Explicit Interface.
- Joshua Bloch. *Effective Java*, 3rd ed. 2018. Addison-Wesley. **ISBN 978-0-13-468599-1.** (verified.)
- Donald E. Knuth. *The Art of Computer Programming, Volume 2: Seminumerical Algorithms*, 3rd ed. 1997. Addison-Wesley. **ISBN 0-201-89684-2.** (verified.) — ch. 3, "Random Numbers".
- Bruce Dawson. "Comparing Floating Point Numbers, 2012 Edition". 2012. randomascii.wordpress.com (verified.) Companion: David Goldberg, "What Every Computer Scientist Should Know About Floating-Point Arithmetic", 1991 (verified.)
- Nathaniel J. Smith. "Notes on structured concurrency, or: Go statement considered harmful". 2018. vorpus.org (verified; title/author/date 2018-04-25 confirmed live.)
- Goetz, Peierls, Bloch, Bowbeer, Holmes & Lea. *Java Concurrency in Practice*. 2006. Addison-Wesley Professional. **ISBN 978-0-321-34960-6.** (verified.) — Thread Confinement.
- Robert Nystrom. *Game Programming Patterns*. 2014. Genever Benning / gameprogrammingpatterns.com (verified.) — Corpus covering work for Service Locator.
- Gary Bernhardt. "Functional Core, Imperative Shell". 2012. Destroy All Software screencast, **Classic Season 4**. https://www.destroyallsoftware.com/screencasts/catalog/functional-core-imperative-shell (verified — *episode confirmed in the live catalog*, i.e. existence, not content.) — Gives the manifest a precise episode locator; its OPEN flag on the paywalled content still stands.
- RFC 8785, *JSON Canonicalization Scheme (JCS)*. Rundgren, Jordan & Erdtman. 2020. Informational (verified.) · ITU-T Recommendation **X.690 (02/2021)**, *ASN.1 Encoding Rules: BER, CER and DER* (verified.)
- J.W. Grenning. *Test-Driven Development for Embedded C*. 2011. Pragmatic Bookshelf. **ISBN 978-1-934356-62-3.** (verified.) — Secondary teaching work for `test-double`, `test-fixture`, `four-phase-test`.

**Marked UNVERIFIED in the corpus — do not present as verified:**

- R.C. Martin. *Clean Architecture*. 2017. — corpus record `martincleanarch`, `verification: unverified`, **no identifier recorded**. It is a covering work for `humble-object`.
- Eric Evans & Martin Fowler. "Specifications". 1997. PLoP workshop paper hosted at martinfowler.com. — `verification: unverified`; corpus note: the hosted PDF "downloaded live but is password-protected and unreadable this session"; **UNRESOLVED: year/venue**.

**Naming sources with NO corpus work record — cite as `named-in` strings only, or verify first:**

- Peter Schuh & Stephanie Punke. "ObjectMother: Easing Test Object Creation in XP". XP Universe 2001. (`object-mother` naming source; corpus covering work is Meszaros.)
- Alur, Crupi & Malks. *Core J2EE Patterns: Best Practices and Design Strategies*. 2001. (`service-locator` naming source.)
- Nat Pryce. "Test Data Builders: an alternative to the Object Mother pattern". 2007. (`test-data-builder` naming source *and* the sourced `alternative-to` edge; the corpus carries only the 2009 GOOS book.)
- Buschmann, Henney & Schmidt. "Explicit Interface and Object Manager: Two Patterns from a Pattern Language for Distributed Computing". EuroPLoP 2003. (`explicit-interface` naming source; the corpus carries POSA4 2007 instead.)
- Rob Pike. "Self-referential functions and the design of options". commandcenter blog, 2014. (`functional-options` co-naming source.)
- ApprovalTests / approvaltests.com; Jest snapshot-testing documentation; xunitpatterns.com. (aka-level naming for `golden-master-testing` and `four-phase-test`; the corpus notes these were "verified via live search this session" but they did not become work records.)
- Mark Seemann. "Impureim sandwich". ploeh blog, 2020. (Cited on the `functional-core-imperative-shell alternative-to monad` edge; no work record.)

---

## Where the catalogs REFINE or CONTRADICT the manifest's framing

**1. The five-way double taxonomy is one element, and the real axis is behavioral sophistication.**
PY §3 presents dummy / fake / stub / spy / mock as five kinds and hangs its recommendation on one
distinction ("only mocks insist upon behavior verification"). The catalog deliberately folds all five into
a single element with the note *"Folded mock/stub/fake/spy/dummy into one element per charter"*, and its
`what` states the axis: the family "spans dummy, fake, stub, spy, and mock **by increasing behavioral
sophistication**". That reframes the manifest's rule — "prefer fakes over mocks" is not a choice among five
species but a *position on one dial*: take the least behavior that still lets you assert the contract.
Corroboration from the same catalog: the only family member kept as its own element is `service-stub`, and
it is individuated not by verification style but by the **boundary it sits at** ("implements the same
gateway interface"). Sharper rule for PY §3: substitutes are individuated first by the seam they occupy,
and only then by how much behavior they carry.

**2. "Seam" is deliberately not an element — and PY §2 makes it load-bearing.**
The design catalog's *Notable exclusions* register (`design_elements_catalog_v1_0.md:6177`) rejects it
explicitly: *"Legacy Seam / Seam (Feathers WELC 2004; Fowler bliki LegacySeam) — Analytical concept naming
where behavior can be substituted without editing source (object/link/preprocessing seams) — a testability
property of code plus legacy-work practice, not a recurring implementable mechanism; strictness round
excludes."* PY §2 uses the seam as *the* definition of the unit/integration boundary; ARCH §1 and §4.2
define it as vocabulary with three examples. The corpus's position is sharper and more actionable: a seam is
a **property**, and the mechanisms that produce one are named separately — `dependency-injection`,
`explicit-interface`, `separated-interface`, `plugin`, `gateway`, `humble-object`, `service-locator`, and
`facade-backend-module-pattern` (where, in the catalog's words, "the seam is moved to the build"). Both
manifests should stop saying "the seam" as though it were an artifact and require naming *which mechanism*
creates it. "We injected the clock" is reviewable; "we have a seam" is not.

**3. Three different reasons to substitute, which the manifest merges into one heading.**
PY §6 files clock, network, filesystem and subprocess substitution under a single bullet list. The graph
splits them by *tactic*: substituting an uncontrollable resource realizes `sandbox` ("virtualizing
uncontrollable resources (system clock, memory, battery, network)"); replacing a collaborator that could
answer differently realizes `limit-nondeterminism`; supplying controlled input data realizes
`abstract-data-sources`. Different exit criteria follow — a sandbox is adequate when the resource is
consequence-free, a determinism substitution is adequate when reruns agree, a data-source abstraction is
adequate when the input partition is covered. As written, the manifest cannot say when a substitution is
finished.

**4. The tactic has an escape clause the manifest asserts away.**
PY §6 and ARCH §4.4 both treat nondeterminism as something to eliminate ("inject time", "seed it", "fake or
isolate"). The `limit-nondeterminism` element says eliminate it "where possible", and *"where unavoidable
(e.g. multithreaded response to unpredictable events), manage it with tactics like record/playback"* —
carried as a **sourced** `uses` edge to `record-playback` citing SAIP 4e directly. Neither manifest has any
vocabulary for the irreducible case, so in practice such tests get quarantined or retried. State the graded
rule: eliminate → if not eliminable, record at the interface and replay → only then retry.

**5. Fixture strategy is a design decision; the manifest ships only its Python spelling.**
PY §1 verifies pytest's five scopes with quoted docs — a good tooling fact, and no decision. The
`test-fixture` element's `problem` names the decision outright: tests need a start state "cheap to build,
isolated enough to prevent inter-test coupling, and expressive enough to read; **fixture strategy is the
named design decision governing that trade-off**", with `Fresh Fixture` / `Shared Fixture` as its `aka`. So
`scope=` is the *encoding* of a Fresh-vs-Shared choice, and a `session`-scoped mutable fixture is a Shared
Fixture decision made by accident. Related gap: `four-phase-test uses test-fixture` is **sourced** to
Meszaros ("Phase 1 (setup) constructs the test fixture the exercise phase runs against"), yet the manifest
never names the phase structure at all — so it has no place to say "teardown belongs to the fixture, not
the test body".

**6. Test-data construction: a sourced tradeoff the manifest has neither side of.**
PY §6's only statement is "treat fixtures and test data as version-controlled code" — no construction
mechanism at all. The corpus carries two named ones and the tradeoff between them as a **sourced** edge
(`test-data-builder alternative-to object-mother`, Pryce 2007). The catalog even states each side's cost:
Object Mother "centralizes canonical test fixtures, **at the cost of coupling tests to shared exemplars**";
builders exist because "Object Mothers proliferate variants and obscure which attributes matter to a test".
This is the same shape of argument as the manifest's own "prefer fakes over mocks" and deserves the same
treatment as a stated default with a named alternative.

**7. `specialized-interfaces` has zero realizers, and its Python form breaks the tactic's own premise.**
No design element among 709 realizes it — the corpus names no code-level construct for test-only control
and observation. Both manifests share the hole: ARCH §4.2 only warns that a self-constructing object is
"a testing obstacle", and neither has a rule for test hooks. Import the tactic *and* record the
Python-specific contradiction: the tactic requires test interfaces "clearly separated from functional
interfaces **so they can be removed**", and it names its own cost — "shipping code different from tested
code is problematic in performance- and safety-critical systems". In Python nothing is removable: no
conditional compilation, no dead-code stripping, and an underscore prefix does not prevent import. The
manifest must therefore draw the consequence the source cannot: **test hooks ship, so they are part of the
public contract**. Name them honestly (`debug_state()`, not `_debug_state()`), keep them read-only where
possible, and give the mutating ones (`reset_for_test()`) the same review discipline as production API.

**8. `assert` has three lifetimes and both manifests flatten them.**
ARCH §1 says invariants "are checked, asserted, or enforced by types", and ARCH §2 warns contracts become
comments when "aspirational rather than checked at runtime or enforced by types". The
`executable-assertions` tactic is more specific about placement ("wherever the data is referenced or
modified") and purpose (assertions "embed the test oracle in the code"). Python then imposes a distinction
neither manifest makes: pytest-rewritten `assert` exists only in collected test modules; a plain `assert` in
production code **disappears under `-O`**; only an explicit `raise` survives optimization. So "enforced by
assertion" names three different guarantees. `design-by-contract` adds what is missing from both: **blame
assignment** — "with blame assigned by which side's clause failed" — which is exactly how you decide
whether a failure means "add a caller test" or "add a callee test".

**9. Humble Object is the graded version of the manifest's all-or-nothing FCIS recommendation.**
PY §7 and Recommendation 6 tell the reader to adopt functional-core / imperative-shell — an
architecture-of-the-whole move, unavailable in code you cannot re-architect. `humble-object` is the local
form, and the graph ties them together: `functional-core-imperative-shell composes-with humble-object`
("The thin imperative shell mirrors Humble Object: push hard-to-test IO to the edge, test the pure core"),
`humble-object realizes limit-structural-complexity`, and `page-object specializes humble-object` (cited to
Fowler). Naming both converts "adopt FCIS" into a ladder: strip the untestable touchpoint to glue (Humble
Object) → push all effects into one shell (FCIS) → make the shell an adapter set
(`hexagonal-architecture`, which FCIS **realizes**). Related ARCH gap: the paradigm menu in §2 has no
Ports-and-Adapters entry although three cataloged elements enable or realize it.

**10. Golden master / characterization / snapshot / approval are one thing, and it has a stated precondition.**
Neither manifest mentions any of the four names. The catalog folds all of them into
`golden-master-testing` ("approval testing, snapshot testing, characterization testing (legacy-code
framing), reference-output testing, golden file testing") and states the mechanism precisely: stored
reference artifact + comparator + **explicit approve-the-diff step**. The precondition arrives as an edge —
`uses canonical-serialization`, "the recorded output must be canonicalized (stable ordering, normalized
noise) so reruns match the stored master" — which is the diagnosis for most flaky snapshot suites and
appears in no snapshot library's quickstart. It also connects to ARCH §6, whose "characterization tests"
bullet is the *only* item in that section with an element id behind it.

**11. Coverage's natural completion is a corpus gap, not an oversight to fill.**
PY §5 lands the Fowler/Goodhart argument well ("coverage is a diagnostic, not a target") and Recommendation
5 pairs a mandated gate with "a ban on assertion-free tests". The obvious next move — mutation score, which
answers *do the assertions discriminate* — has **no element**, and `Mutation testing` appears in the
exclusion register (`:6209`) **with an empty rationale field**. The same is true of `Fuzzing / fuzz harness`
(`:6134`) and `Fake clock / virtual time` (`:6115`). So the corpus neither supplies these nor justifies
their absence. Do not import them; do not cite the register as authority against them either. Record as an
open corpus question.

**12. The exclusion register contradicts the shipped catalog on test-structure patterns.**
Register entry at `:6339` — *"xUnit test-organization patterns (Four-Phase Test, Fresh Fixture, Testcase
Class per Class, etc.) — Meszaros patterns about test structure/process, not code-level constructs; **only
the code-construct subset (Test Double, Humble Object) taken**"* — and the AXES note at `:5794` lists five
testing constructs ("test double, service stub, object mother, test data builder, humble object"). The
shipped catalog has **eleven**, including `four-phase-test` and `test-fixture`, each carrying a borderline
note that admits the tension (`four-phase-test`: "test-code structuring pattern near the practice boundary;
included on Meszaros catalog establishedness and the composed-method altitude precedent"). Reading: the
altitude line moved during compilation and the register was not updated. A later author should treat
`four-phase-test` and `test-fixture` as **admitted-but-contested** elements, and must not cite the exclusion
register against them.

**13. Explicitly-excluded practices that the manifest states as unsourced principles — with their real sources.**
Three of the manifest's principles are named, citable practices that the corpus deliberately kept out of the
*element* layer. Fixing the citations costs nothing and settles why they have no element ids:
- PY §6 bullet 1 ("a fake used in unit tests and the real implementation in integration tests should satisfy
  the *same* contract test suite", currently marked "principle; consistent with Fowler/Feathers") is
  **Contract Test** — register at `:6074`: *"Testing strategy verifying a test double (or provider) matches
  the real contract (consumer-driven contracts, Pact) — cross-component testing practice rather than an
  in-program construct; excluded at strictness peak."* Primary source: Fowler bliki "Contract Test" (2011).
- PY §6's clock bullet is **Clock Wrapper** — register at `:6064`: *"Injectable abstraction over the ambient
  time source for testability — application of dependency-injection + test-double to one dependency (time);
  fold, optionally as aka ('fake/virtual clock') on test-double."* The refinement is that there is no clock
  pattern: it is DI plus a double, and the *same derivation* covers network, filesystem, subprocess and
  randomness. Stating the rule once is shorter and more general than the manifest's four-bullet list.
- PY §3's canonical Fake example is **In Memory Test Database** — register at `:6154`: excluded as a
  "test-environment substitution technique — practice, plus covered conceptually by
  test-double/service-stub territory". Consistent with the manifest; worth knowing there is no id to cite.
- Vocabulary caution: **Test Harness** is itself an excluded entry (`:6309`, "Nygard stability pattern, but
  it is testing infrastructure/practice, not a runtime design mechanism") — so PY §6's phrase "test
  harnesses" names something the corpus rejected, not an element.

**14. ARCH §6's refactoring list is practice-layer content by the corpus's own lights.**
`Branch By Abstraction` (`:6055`) and `Parallel Change / Expand-Contract` are both in the exclusion register
as change-sequencing *practices*, not mechanisms; "Extract seam" inherits point 2's problem. Only the last
bullet, characterization tests, has an element (`golden-master-testing`). This is not a contradiction —
different layers — but a later author should not hunt for element ids for §6, and the section should be
marked as practice-layer, exactly as PY §5's obligation vocabulary must be (next point).

**15. PY §5's obligation vocabulary has no element-layer counterpart, by design.**
Verified absent from all 1083 nodes: `equivalence-partitioning`, `boundary-value-analysis`, `test-oracle`,
`metamorphic-testing`, `test-pyramid`, `contract-test`, `mutation-testing`, `characterization-test`, `seam`,
`injected-clock` / `virtual-clock` / `time-provider`, `in-memory-database`, `fault-injection`,
`consumer-driven-contract`, `test-container`. The catalog's charter puts these on the practice side of the
line. What the element layer *does* give §5 is narrow and useful: `executable-assertions` (the tactic that
"embeds the test oracle in the code"), `design-by-contract` (blame assignment), `smart-constructor`
(obligations removed by construction), and `epsilon-ulp-float-comparison` (how an expected observable is
compared at all). The manifest should mark which of its sections are element-backed and which are
practice-backed, rather than letting both read as equally grounded. Note also that the SWE process corpus
(`swe_process_corpus_v1_0.md`) covers standards, docs, VCS and CI/CD only — a grep for `pytest`,
`hypothesis`, `coverage.py` and `unittest` across it returns nothing. **The corpus contributes vocabulary
and architecture rules to this manifest; it contributes no tool facts, so PY §1's version claims remain
sourced solely from the manifest's own live verification.**

**16. Two citation upgrades and one that does not move.**
PY currently FLAGS Feathers as secondary (an InformIT chapter excerpt) and reaches Meszaros "via Fowler's
articles". The corpus supplies verified publisher identifiers for both (ISBN 978-0-13-117705-5;
ISBN 978-0-13-149505-0), which upgrades the *bibliographic* citation while leaving the manifest's honest
caveat about page numbers and exact wording exactly where it is. The Bernhardt OPEN flag does **not** move:
the corpus verified that the screencast episode exists in the live catalog (Classic Season 4), not its
content. What is new there is a second name for the same element — aka **"impureim sandwich"** — and a
sourced `alternative-to monad` edge (Seemann, 2020) giving the manifest a stated alternative to FCIS that it
currently does not acknowledge.
