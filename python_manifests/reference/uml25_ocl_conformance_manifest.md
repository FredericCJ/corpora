# UML 2.5 / OCL Reverse-Engineering — Ground-Truth Manifest

**Purpose.** A citable ground-truth reference for an agent reverse-engineering a Python codebase into a strict, multiview UML 2.5 model with OCL constraints. Every claim is version-qualified and tagged **ESTABLISHED** (normative and stable), **VERSION-DEPENDENT** (tie to a version/spec/tool), or **OPEN** (no authoritative source found). Metamodel element names, OCL operations, and tool features are verified against primary sources, not recalled.

---

## 1. The normative standards and their status

**UML — ESTABLISHED.** The current formal version is **UML 2.5.1, OMG document `formal/2017-12-05`, published December 2017** (https://www.omg.org/spec/UML/2.5.1/). It supersedes UML 2.5 (`formal/2015-03-01`, March 2015 — published May 2015 per the OMG record). `https://www.omg.org/spec/UML/Current` resolves to 2.5.1. UML 2.5 was "formally a minor revision to the UML 2.4.1 specification, having been substantially re-written as solicited by the UML Specification Simplification RFP ad/09-12-10," superseding the split `formal/2011-08-05` (Infrastructure) and `formal/2011-08-06` (Superstructure). 2.5.1 collapsed the former two-volume Infrastructure/Superstructure structure into one document.

**OCL — ESTABLISHED / VERSION-DEPENDENT alignment.** Current formal version is **OCL 2.4, OMG document `formal/2014-02-03`, February 2014** (https://www.omg.org/spec/OCL/2.4/). The spec states verbatim: "OCL version 2.4 is the latest version of OCL that is aligned with UML 2.4.1 and MOF 2.4.1." Its RTF report is `ptc/2013-09-01`. **There is no released OCL 2.5.** The OMG OCL issue tracker references a hypothetical "OCL 2.5" alignment with UML templates, but no such specification has been published.

**MOF — ESTABLISHED.** Current is **MOF (Meta Object Facility) Core 2.5.1** (https://www.omg.org/spec/MOF/2.5.1/). Note that the XMI 2.5.1 normative references cite **MOF Core 2.4.2** as `[MOF] ISO/IEC 19508:2014`; MOF 2.5.1 is the current OMG formal version.

**XMI — ESTABLISHED.** Current is **XMI (XML Metadata Interchange) 2.5.1, dated June 2015** (https://www.omg.org/spec/XMI/2.5.1/). Supersedes the 2.5 beta and the older 2.1.1 mapping (`formal/05-09-01`).

**UML DI — VERSION-DEPENDENT (stale).** **UML Diagram Interchange (UMLDI) 1.0**, formal version, **publication date May 2004** (https://www.omg.org/spec/UMLDI/1.0/). It predates UML 2.5; diagram-layout interchange in practice relies on the UMLDI XMI fragment shipped with the UML 2.5.1 machine-readable files (`https://www.omg.org/spec/UML/20161101/UMLDI.xmi`) rather than the 2004 document.

**ISO track.** UML 2.4.1 = ISO/IEC 19505-1/-2:2012; OCL 2.3.1 = ISO/IEC 19507:2012; MOF Core = ISO/IEC 19508:2014. The ISO editions lag the OMG formal versions: ISO publishes OCL 2.3.1, while OMG's current is 2.4.

### Compliance levels — ESTABLISHED (a required, often-misremembered finding)
The older formal compliance levels **L0/L1/L2/L3 (language units) were ELIMINATED in UML 2.5/2.5.1.** The spec states: "The compliance levels L0, L1, L2, and L3 have been eliminated, because they were not found to be useful in practice. A tool either complies with the whole of UML or it does not." The L0–L3 structure (L0 class structures; L1 use cases/interactions/structures/actions/activities; L2 deployment/state machines/profiles; L3 information flows/templates/model packaging) belongs to **UML 2.4.1 and earlier (ISO/IEC 19505)**. An agent targeting "strict UML 2.5" must NOT cite L1/L2/L3 conformance — that is a version error.

### The OCL-2.4-to-UML-2.5.1 alignment gap — REQUIRED FINDING
OCL 2.4 is normatively aligned with **UML 2.4.1 / MOF 2.4.1**, not 2.5.1. The seam:
- **No metamodel-structure breakage for class-level constraints.** UML 2.5 was a "minor revision" of 2.4.1 — the abstract-syntax classes OCL navigates (Class, Property, Association, Operation, StateMachine, etc.) are essentially unchanged in name and semantics, so OCL expressions over class structure remain valid.
- **The gap is in spec cross-references and the OCL/UML metamodel merge, not in everyday operators.** OCL 2.4 still references UML 2.0/2.4.1 alignment in Clause 12 ("The Use of OCL Expressions in UML Models," ExpressionInOcl). The compliance-level removal in 2.5 has no OCL analogue. OCL 2.4's template/reflection facilities lag UML 2.5 templates (acknowledged in the OMG issue tracker as deferred to a never-released "OCL 2.5").
- **Concrete recommendation:** Target **UML 2.5.1 (`formal/2017-12-05`) for the model + OCL 2.4 (`formal/2014-02-03`) for constraints**, and state explicitly that OCL 2.4 is consumed as the constraint language over a 2.5.1 abstract syntax. This is exactly what current tooling (Eclipse OCL, Papyrus) does in practice.

### What "strict conformance" can and cannot mean
- **Can mean:** every model element is a valid instance of a named UML 2.5.1 metaclass; multiplicities/visibilities/well-formedness rules (the spec's "Constraints" subclauses) hold; every OCL expression is type-correct under the OCL 2.4 type system; the model serializes to valid XMI 2.5.1.
- **Cannot mean:** a graded L-level claim (levels are gone); nor a single tool that perfectly round-trips both diagrams and OCL across vendors (the XMI interoperability gap, §8); nor that OCL is formally pinned to the 2.5.1 metamodel (it is pinned to 2.4.1, bridged in practice).

---

## 2. Structural modeling — abstract syntax and notation

UML 2.5.1 organizes structure under **Classification (Clause 9), Structured Classifiers (Clause 11), Packages (Clause 12), Components (Clause 11.6), and Common Structure (Clause 7)**. (Clause numbers per UML 2.5.1 `formal/2017-12-05`; verify exact subclause against the PDF, as some figures cited below come from secondary renderings of the spec.)

### Class diagram
**Metaclasses:** `Class`, `Classifier`, `Property` (attributes AND association ends), `Operation`, `Parameter`, `Association`, `Generalization`, `InterfaceRealization`, `Interface`, `DataType`, `Enumeration`, `EnumerationLiteral`, `Constraint`. A `Property` is the single metaclass underlying both attributes and member ends of associations.

**Association vs. aggregation vs. composition — ESTABLISHED.** Governed by `Property::aggregation : AggregationKind`, an enumeration with literals **`none`, `shared`, `composite`**.
- **Association (`aggregation = none`):** structural relationship; plain solid line. Member ends are Properties with multiplicity, navigability, and optional role names.
- **Shared aggregation (`aggregation = shared`):** hollow/white diamond at the aggregate end. UML 2.5.1 explicitly leaves its semantics open ("Precise semantics of shared aggregation varies by application area and modeler") — do NOT over-interpret a hollow diamond.
- **Composite aggregation / composition (`aggregation = composite`):** filled black diamond at the whole end. Strong ownership: a part instance belongs to at most one composite at a time, and deletion of the whole cascades to the parts. A diamond may not be attached to both ends of one association.

**Multiplicity & navigability.** `MultiplicityElement` supplies `lower`/`upper` (e.g., `0..1`, `1`, `*`, `1..*`); `isOrdered`, `isUnique` refine collection semantics. Navigability is shown by an open arrowhead on the navigable end; UML 2.5 notation also allows a small "x" on a non-navigable end. Navigable-end ownership has dot notation distinguishing ownership by the association vs. by the classifier.

**Visibility — ESTABLISHED.** `VisibilityKind` literals: **`public` (`+`), `private` (`-`), `protected` (`#`), `package` (`~`)**.

### Component diagram
**Metaclass `Component`** (a structured `Class`). Provided/required interfaces via `InterfaceRealization` (provided) and `Usage`/Dependency (required). **Ball-and-socket notation:** provided interface = "lollipop" (ball on a stick); required interface = "socket" (cup on a stick). **Assembly connector** = ball-and-socket joined: links a required interface of one component to a provided interface of another. **Delegation connector** = `«delegate»`-keyworded connector linking an external port to an internal part that realizes/requires the behavior.

### Composite-structure diagram
**Metaclasses:** `StructuredClassifier`, `Property` (as **part**, when composed by the classifier), `Port`, `Connector`, `ConnectorEnd`, `Collaboration`, `CollaborationUse`.
- **Port** (`Port`, a `Property` typed by an `EncapsulatedClassifier`): interaction point on the classifier boundary, drawn as a small square straddling the border. `isService`, `isConjugated` attributes. Provided/required interfaces attach to the port.
- **Part:** a Property with composite aggregation inside the containing classifier; drawn as a solid-outline box with `name:Type`.
- **Connector kind is DERIVED:** per the spec, "a connector with one or more ends connected to a port that is not on a part and that is not a behavior port is a delegation; otherwise it is an assembly." So `Connector::kind : ConnectorKind` (`delegation` | `assembly`) is computed, not free-chosen.

### Package & object (supporting)
- **Package diagram:** `Package`, `PackageImport`, `PackageMerge`, `Dependency`. Folder notation. `PackageMerge` is the mechanism the spec itself used to assemble the old compliance levels.
- **Object diagram:** `InstanceSpecification`, `Slot`, `Link` (an instance of an Association). Anonymous instances allowed (`:Type`). A snapshot of a system state — the natural target for OCL evaluation and for USE-style validation.

---

## 3. Behavioral modeling — abstract syntax and notation

### State machine (UML 2.5.1, Clause 14)
**Metaclasses:** `StateMachine`, `Region`, `State` (simple, composite, submachine), `Pseudostate`, `FinalState`, `Transition`, `Trigger`, `Event`, `Constraint` (guard), `Behavior` (entry/exit/doActivity, effect), `ConnectionPointReference`.

**Pseudostate kinds — ESTABLISHED.** `PseudostateKind` enumeration has exactly **ten** literals: **`initial`, `deepHistory`, `shallowHistory`, `join`, `fork`, `junction`, `choice`, `entryPoint`, `exitPoint`, `terminate`**. Constraints:
- **`initial`:** at most one per Region; source of at most one transition with optional effect but **no trigger and no guard**.
- **`shallowHistory` / `deepHistory`:** at most one per Region; "H" / "H*" circle. Deep restores the full nested configuration; shallow restores only the topmost substate.
- **`fork` / `join`:** split into / merge from orthogonal regions; transitions into a join and out of a fork **cannot have guards or triggers**. Heavy-bar notation.
- **`junction`:** static conditional branch/merge (guards evaluated before any path is taken); a default `else` guard is allowed.
- **`choice`:** **dynamic** conditional branch — guards evaluated after entering the choice. If no guard is true the model is ill-formed; use `else`.
- **`entryPoint` / `exitPoint`:** encapsulation points on a composite/submachine State boundary (circle / circle-with-cross).
- **`terminate`:** entering it halts the state machine's execution (no exit behaviors run other than the triggering transition's effect).

**Composite & submachine states.** A composite State contains one or more Regions; orthogonal (concurrent) states have ≥2 Regions. A submachine State references a reusable `StateMachine` and connects via ConnectionPointReferences to its entry/exit points.

**Transitions.** `Transition` has `kind ∈ {external, internal, local}`, a `trigger` (Event), a `guard` (Constraint), and an `effect` (Behavior). Notation: `trigger [guard] / effect`.

### Activity (UML 2.5.1, Clause 15)
**Metaclasses:** `Activity`, `Action` (incl. `CallBehaviorAction`, `CallOperationAction`, `SendSignalAction`, `AcceptEventAction`), `ControlNode`, `ObjectNode`, `ControlFlow`, `ObjectFlow`, `ActivityEdge`, `Pin` (`InputPin`/`OutputPin`), `ActivityParameterNode`, `ActivityPartition`, `DataStoreNode`, `CentralBufferNode`.

**Control nodes — ESTABLISHED (the full set):** **`InitialNode`, `ActivityFinalNode`, `FlowFinalNode`, `DecisionNode`, `MergeNode`, `ForkNode`, `JoinNode`.** Key distinctions:
- **`ActivityFinalNode`** stops the entire Activity (all flows); **`FlowFinalNode`** destroys only the tokens on its one incoming flow — a UML 2.0+ addition needed because of unrestricted parallelism.
- **`DecisionNode`** (diamond): one in, many guarded out; only one branch taken. **`MergeNode`** (diamond): many alternative in, one out — does NOT synchronize. They share diamond notation but are distinct metaclasses; a combined decision/merge symbol is allowed.
- **`ForkNode`** (bar): one in, many concurrent out — unrestricted parallelism. **`JoinNode`** (bar): many in, one out, synchronizes (waits for all incoming tokens); a join specification may modify the AND semantics.

**Control flow vs. object flow — ESTABLISHED.** `ControlFlow` carries control tokens only (sequences actions). `ObjectFlow` carries object/data tokens (must have an ObjectNode/Pin on at least one end); arrowed connector, optionally with Pins. Token type constrains which edges may connect.

**Partitions.** `ActivityPartition` (swimlanes) groups actions by responsible classifier/role — the natural mapping target for "which class/module performs this step."

### Sequence / interaction (UML 2.5.1, Clause 17)
**Metaclasses:** `Interaction`, `Lifeline`, `Message`, `MessageOccurrenceSpecification`, `ExecutionSpecification`, `ExecutionOccurrenceSpecification`, `CombinedFragment`, `InteractionOperand`, `InteractionConstraint`, `Gate`, `StateInvariant`, `InteractionUse`.

**Combined-fragment operators — ESTABLISHED (the full set of twelve).** `InteractionOperatorKind` enumeration literals: **`seq`, `alt`, `opt`, `break`, `par`, `strict`, `loop`, `critical`, `neg`, `assert`, `ignore`, `consider`** (twelve). **`ref` is the notation for an `InteractionUse`** (reference to another interaction) — it is NOT a literal of `InteractionOperatorKind`; do not list it as a combined-fragment operator. Semantics:
- `seq` weak sequencing (default); `strict` strict ordering; `alt` guarded alternatives; `opt` single guarded operand; `break` breaking scenario replacing the remainder; `par` parallel/interleaved operands; `loop` recursive seq application with guard/bounds; `critical` atomic region (cannot be interleaved); `neg` invalid traces; `assert` the only valid continuations; `ignore`/`consider` which message types are insignificant/significant.

**Message kinds.** `Message::messageSort ∈ {synchCall, asynchCall, asynchSignal, createMessage, deleteMessage, reply}`. Synchronous = filled arrowhead; asynchronous = open arrowhead; reply = dashed; create = dashed arrow to a lifeline head; lost/found messages use dots.

**Execution specifications & gates.** `ExecutionSpecification` = thin rectangle on a lifeline (activation bar). `Gate` = `MessageEnd` on a fragment/interaction boundary, connecting inner messages to the environment.

---

## 4. Faithful reverse mapping (code → model) — Python as source

**Principle of faithfulness:** map a construct to a UML element **only when the metaclass semantics actually hold**; otherwise OMIT it or annotate with a `Comment` or an applied stereotype rather than inventing notation. A reverse model that force-fits Python idioms into ill-fitting metaclasses is a redrawing, not a faithful reverse-engineering.

### Honest mappings (low distortion)
| Python construct | UML 2.5.1 target | Notes |
|---|---|---|
| Package (dir with `__init__.py`) / module | `Package`; or `Component` at architecture altitude | Module-as-Package is the literal mapping; Component when it has provided/required interfaces. |
| `class C:` | `Class` (a `Classifier`) | Methods → `Operation`; class/instance attributes → `Property`. |
| Base classes `class C(A, B)` | `Generalization` | One per base; see MRO trap below. |
| `abc.ABC` / `typing.Protocol` | `Interface` + `InterfaceRealization` | ABCs map cleanly; Protocols are structural (see duck-typing trap). |
| Attribute with container type | `Property` with multiplicity (`0..*`, etc.) | `list[X]` → `isOrdered=true`; `set[X]` → `isUnique=true`; `dict` → qualified association or Property typed by a Map datatype. |
| Reference to another class | `Association` (composite if owned/lifecycle-bound) | Use `composite` only when the owner controls the part's lifecycle. |
| Call graph among objects | `Interaction` / sequence diagram | Synchronous call → `synchCall`; `await` → see async trap. |
| Object lifecycle (explicit states) | `StateMachine` | Only when the code has a real state variable/transitions. |
| Function/method control flow | `Activity` | Branches → DecisionNode; loops → loop via control flow; `with` blocks → structured nodes. |

### Python-specific traps (constructs with no clean UML equivalent)
- **Free functions at module scope.** No first-class UML metaclass for a bare function. Options: model the module as a `Class` with the `«utility»` stereotype (UML Standard Profile) whose functions are static `Operation`s; OR represent as `Activity`/`Behavior` owned by the package. Do NOT invent a "function" notation. State the choice once and apply it uniformly.
- **Duck typing / structural typing (`typing.Protocol`).** UML interfaces are nominal (explicit realization). A Protocol satisfied structurally has no `InterfaceRealization` edge in the code. Represent the Protocol as an `Interface` and add realization edges **only** where statically inferable; annotate inferred-but-unstated conformance with a `Comment`. Mark residual cases OPEN.
- **Decorators.** No UML metaclass. If a decorator changes the contract, reflect the *effect* on the Operation/Property: `@property` → a derived/read-only Property; `@abstractmethod` → `isAbstract=true`; `@staticmethod`/`@classmethod` → static/owned scope. For behavioral decorators (caching, retry) annotate with a stereotype/Comment; do not draw the wrapper as a class unless it is reified.
- **async/await & coroutines.** UML has no native coroutine metaclass. Map `async def` to an `Operation` with an applied stereotype (e.g., `«async»`) or a Comment; model `await` points as asynchronous messages (`asynchCall`) in interactions and as AcceptEventAction in activities. Flag the impedance mismatch as OPEN — there is no normative UML coroutine construct.
- **Generics via `typing` (`Generic[T]`, `list[T]`).** Map to UML **templates**: `TemplateSignature`, `TemplateParameter`, and bound elements. Caveat: OCL 2.4 templates/reflection lag UML 2.5 (the deferred "OCL 2.5" issue), so generic constraints may not be fully expressible.
- **Mixins & MRO (method resolution order).** Multiple `Generalization`s capture the inheritance edges, but **C3 linearization/MRO is dynamic and has no UML representation.** Resolution order is not a metamodel concept. Record MRO in a `Comment` if it matters; never invent ordering notation on generalizations.
- **Message-passing concurrency (multiprocessing, queues).** Model processes/workers as `Component`s or active classes (`Class` with `isActive=true`), channels/queues as classes or `«datastore»`/CentralBufferNode in activities, and message exchange as asynchronous `Message`s. Process boundaries are best shown in composite-structure or deployment views.
- **Metaclasses (`type` subclasses, `__new__`).** UML's `«metaclass»` (from MOF/Profiles) concerns model-level metaclasses, not Python runtime metaclasses. Annotate with a stereotype/Comment; do not conflate with UML profile metaclasses.
- **Properties / descriptors (`__get__`/`__set__`).** `@property` → derived/read-only `Property` (`isDerived`/`isReadOnly`). General descriptors have no clean mapping — annotate.
- **Dynamic attribute creation (`setattr`, `__dict__`, `__getattr__`).** UML classes are statically featured. Attributes created at runtime cannot be faithfully enumerated; capture only statically determinable Properties and mark the class `{incomplete}` via a Comment. Do NOT fabricate Properties.

**Altitude span.** Architecture → `Package`/`Component` + composite structure; subsystem wiring → ports/connectors; class level → class diagrams + OCL invariants; behavior → state machines (lifecycle), activities (algorithms), sequences (call collaborations) down to implementation detail.

---

## 5. OCL — language and well-formedness (OCL 2.4, `formal/2014-02-03`)

### Constraint kinds and attachment — ESTABLISHED
Context declaration: `context <Classifier>` or `context <Type>::<op>(...)`. The constraint stereotypes:
- **`inv:`** invariant on a `Classifier` (Type). `context C inv [name]: <Boolean-expr>`.
- **`pre:` / `post:`** precondition/postcondition on an `Operation`/behavioral feature (`«precondition»`/`«postcondition»` Constraints). In `post`, `result` and `@pre` are available.
- **`body:`** the result of a query `Operation`: `context C::q(): T body: <expr>`.
- **`def:`** defines reusable helper attributes/operations (`«definition»` Constraint attached to a Classifier; features get `«OclHelper»`).
- **`derive:`** derivation rule for a derived `Property`.
- **`init:`** initial value of a `Property`.
- **`let … in …`** local definitions within a single expression.

### Type system & standard library — ESTABLISHED (names/signatures verified)
- **Primitive types:** `Boolean`, `Integer`, `Real`, `String`, `UnlimitedNatural` (with `*`). `Integer` conforms to `Real`.
- **Collection types (four):** **`Set`** (unordered, unique), **`OrderedSet`** (ordered, unique), **`Bag`** (unordered, duplicates), **`Sequence`** (ordered, duplicates). `Collection` is the abstract supertype. Navigation across a single-valued end yields the object; across a multi-valued end yields a Set (or Bag if `isUnique=false`; OrderedSet/Sequence if `isOrdered`).
- **Special types:** `OclAny` (supertype of all), `OclVoid` (`null`), `OclInvalid` (`invalid`), `OclMessage`, `OclType`/`OclState`.

**Iterator operations — verified names/signatures (OCL 2.4 Clause 11 standard library):** `select(expr)`, `reject(expr)`, `collect(expr)` (flattens; based on `collectNested`), `collectNested(expr)`, `forAll(expr)` (multi-iterator form allowed), `exists(expr)`, `one(expr)` (exactly one), `any(expr)` (one matching; its result when nothing matches is a known spec ambiguity in the issue tracker — null vs. invalid), `isUnique(expr)`, `sortedBy(expr)` (returns Sequence/OrderedSet), `closure(expr)` (transitive closure), and the universal accumulator **`iterate(elem; acc : T = init | expr)`** in terms of which the others are defined.

**Collection (non-iterator) operations include:** `size()`, `includes/excludes`, `includesAll/excludesAll`, `isEmpty/notEmpty`, `sum()`, `count()`, `including/excluding`, `union`, `intersection`, `asSet/asBag/asSequence/asOrderedSet`, `flatten()`, and for Sequence/OrderedSet `first()`, `last()`, `at(i)`, `append`, `prepend`, `insertAt`, `indexOf`, `subSequence`.

**Type operations on `OclAny` — verified signatures:** `oclIsKindOf(t : Classifier) : Boolean` (same type OR subtype), `oclIsTypeOf(t : Classifier) : Boolean` (exactly that type), `oclAsType(t : Classifier) : T` (downcast; undefined/invalid if not a subtype), `oclIsNew() : Boolean` (postcondition-only; true if created during the operation), `oclIsUndefined() : Boolean` (true for `null` or `invalid`), `oclIsInvalid() : Boolean`, `oclInState(s : OclState) : Boolean`, and the type-level `T.allInstances() : Set(T)`. **`@pre`** postfix in postconditions accesses the pre-execution value. Note: there is **no `oclAsSet()`** in the standard library — to wrap a single object as a set use `Set{obj}` or `->asSet()`; treat any reference to "oclAsSet" as **OPEN / not a standard operation**.

### No-side-effect / instantaneous-evaluation rule — ESTABLISHED
The spec states: "OCL is not a programming language… you cannot invoke processes or activate non-query operations within OCL… The evaluation of an OCL expression is instantaneous," and evaluation "cannot alter the state of the corresponding executing system." OCL is a *query-only*, side-effect-free, strongly typed language.

### What OCL expresses that diagrams cannot, and its limits
- **Adds:** invariants beyond multiplicity (e.g., `self.age >= 0`), inter-association constraints, derivation/initialization rules, pre/postconditions, guard semantics, uniqueness across navigation paths, recursive/closure queries.
- **Cannot:** specify control flow, side-effecting operations, real-time/temporal logic (no temporal operators in 2.4), or fully generic/templated metatype reasoning (deferred to the unreleased "OCL 2.5").

### Type-correctness rules an agent must satisfy
Every expression has a static type and must conform to type-conformance rules (e.g., cannot compare Integer with String); each Classifier in the model is a distinct OCL type; supertype conformance is transitive; `T(X)` conforms to `T(Y)` if `X` conforms to `Y`; navigation returns the multiplicity-appropriate collection type; collection operations must use `->` while object/feature access uses `.`; an invariant inherited by a subclass may be strengthened but not weakened.

---

## 6. Conformance checking — drawn vs. verifiable

**A model that merely renders** (PlantUML/Mermaid output) produces a picture. Nothing checks that an arrow is a valid `Association`, that multiplicities are consistent, or that an OCL string is type-correct. Conformance is **ASSERTED**, not verified.

**A model whose conformance is machine-checked** requires three things:
1. **A parseable model in a metamodel-grounded form** — typically EMF/UML2 (Ecore-backed UML 2.5.1) serialized as XMI, not a diagram script.
2. **A metamodel-aware well-formedness checker** — validates instances against UML 2.5.1 metaclasses and their Constraints (e.g., Eclipse UML2 + Papyrus validation).
3. **An OCL evaluator** — parses, type-checks, and (against a snapshot/instance model) evaluates OCL invariants (Eclipse OCL; USE).

**Pipelines that can only ASSERT:** PlantUML, Mermaid, Structurizr DSL, ZenUML, Kroki — they render text to images with no semantic UML validation and no OCL.
**Pipelines that can VERIFY:** Eclipse OCL / MDT-OCL (parse + type-check + evaluate on EMF models), Eclipse Papyrus (UML 2.5.1 well-formedness + OCL via Eclipse OCL), USE (UML-subset well-formedness + full OCL evaluation on snapshots), Dresden OCL (parse/interpret/codegen, though aging).

---

## 7. Text-based / diagram-as-code and OCL tooling — capability matrix

Release data current as of June 2026. **The load-bearing finding: only USE, Eclipse OCL/Papyrus, and (aging) Dresden OCL actually VALIDATE OCL against a model. PlantUML, Mermaid, Structurizr, ZenUML, Kroki, TextUML, and Umple RENDER or compile but do NOT evaluate OCL.**

| Tool | Latest (as of 2026) | UML 2.5 diagram types | Fidelity / divergence | Native OCL | XMI import/export | Renders vs. validates | License / maturity |
|---|---|---|---|---|---|---|---|
| **PlantUML** | v1.2026.4 (built 2026-05-23 per the plantuml.jar man page on mankier.com); plantuml.com/download lists v1.2026.6 as latest — VERSION-DEPENDENT, fast minor cadence | Class, object, component, deployment, sequence, activity, state, use case, timing | Convenience syntax; NOT metamodel-faithful (no formal abstract syntax); broad notation coverage | **None** | No native XMI (Ecore/Xcore import only) | **Renders only** | GPL/LGPL/MIT options; very mature, huge ecosystem |
| **Mermaid** | v11.15.0 stable (per npmjs.com/package/mermaid and Snyk); security backport v10.9.6 published 11 May 2026 | Class, sequence, state (+ ER) | UML-family subset; class diagram supports 8 relationship types; layout weaker at scale | **None** | None | **Renders only** | MIT; very mature, native GitHub/GitLab rendering |
| **Structurizr DSL** | actively maintained (C4-focused) | Not UML diagram types — C4 model; exports to PlantUML/Mermaid | Models C4 (context/container/component), not the UML metamodel | **None** | No (own model/JSON) | Renders (model-as-code; separates model from views) | Open-source DSL/CLI; mature for C4 |
| **TextUML Toolkit** | ~1.x; **dormant** (no releases in years; surveys note last version ~2015) | UML2 models; class-diagram visualization | Backed by Eclipse UML2 abstract syntax (faithful) but unmaintained | **None** (author deliberately avoided OCL; proprietary query language) | Eclipse UML2 models (XMI-compatible) | Validates (IDE) + visualizes | EPL; **abandoned/dormant** |
| **Umple** | v1.37.0 (18 Apr 2026), GitHub releases | Class, state machine, instance/object (+ feature/trait); Mermaid output added | Own textual semantics; faithful to its own metamodel, not full UML 2.5; compiles to code | **None** (own constraint mechanisms, not OMG OCL) — *OPEN: no explicit vendor "no OCL" statement* | Ecore + Papyrus generation; full XMI round-trip not documented (minor OPEN) | **Compiles/validates** (multiplicity checks; code gen Java/C++/PHP/Python) | MIT; actively maintained |
| **USE (UML-based Spec. Env.)** | **CONFLICT — VERSION-DEPENDENT/partly OPEN.** A subagent search reported v7.5.0 (2 Nov 2025) on GitHub releases; an independent check could NOT confirm it (useocl/use README still shows "Copyright (C) 1999-2024"; SourceForge's packaged tarball latest is use-5.2.0). Verify against github.com/useocl/use/releases before citing a version. | UML subset: class, object, sequence/communication views, state machines | High fidelity for the supported subset; purpose-built for OCL | **Yes — author, type-check, AND evaluate** (auto-checks invariants on snapshots; interactive `?` evaluation; Model Validator SAT plugin) | Limited/plugin; no strong native XMI (**OPEN**) | **Validates** (animation, snapshots, OCL evaluation) | GNU GPL; mature academic reference tool |
| **Eclipse OCL / MDT-OCL** | **v6.23.0** (`org.eclipse.ocl.master 6.23.0.v20260217-0639`, release site built 2026-02-21) | N/A (constraint engine for EMF Ecore/UML models) | OMG-compliant Pivot metamodel; UML-aligned; resolves many 2.4 spec issues | **Yes — parse, type-check, evaluate, code-gen, debug** | Operates on EMF/UML2 (XMI) | **Validates / evaluates** | EPL; mature; committers sit on the OMG OCL RTF |
| **Eclipse Papyrus** | **v7.0.0 ("Papyrus-Desktop"), released 11 June 2025** (projects.eclipse.org: "Major release (API breakage)… new version of the diagrams, based on the Eclipse Sirius framework"); a 7.1.x line tracks the 2025-09 train | **All UML diagram types** (targets 100% of spec); UML 2.5(.1), SysML, fUML, MARTE | High metamodel fidelity (EMF UML2); Sirius-based diagrams since 7.0 | **Yes** (full, via Eclipse OCL integration) | **Yes — native EMF/UML2 XMI** | **Validates** + simulation (Moka for fUML/PSCS/PSSM) | EPL; mature |
| **Dresden OCL** | OCL 2.2-era; **aging/largely inactive** | Works against UML2/Ecore/Java/XML models | OCL parser/interpreter/codegen; supports `closure`, `sortedBy`; OCL 2.2 + partial 2.3 | **Yes — parse, interpret, SQL/Java code-gen** | Imports UML2/Ecore (XMI) | **Validates / interprets** | Open source; **largely inactive** |
| **ZenUML** | actively maintained (web/plugins, repos updated Mar 2026); no semver release tag for the core engine | **Sequence diagrams only** (also embedded in Mermaid) | Dedicated sequence DSL (~5 elements) | **None** | None (PNG/SVG/PDF export) | **Renders only** | Core MIT; hosted freemium |
| **Kroki** | active unified-API service | Aggregates PlantUML, Mermaid, Structurizr, D2, etc. | Pass-through to underlying renderers; no metamodel of its own | **None** | None | **Renders only** (unified API) | Open source (gateway) |

Other current text/UML-adjacent tools noted in surveys: **StarUML** (commercial; its sequence editor exposes the twelve combined-fragment operators verbatim), **Visual Paradigm** (commercial; Python instant-reverse, OCL authoring), **Pynsource** and **pyreverse (Pylint)** (Python→class-diagram reverse engineering; pyreverse emits PlantUML/Mermaid).

---

## 8. Serialization and interchange

**XMI 2.5.1 (June 2015)** is the normative model-interchange format: a MOF→XML mapping with EBNF production rules, object identity via IDs/UUIDs, and **Canonical XMI** for reproducible output. **What round-trips:** the *model* (metaclass instances — classes, associations, state machines, OCL bodies stored as Constraint/OpaqueExpression). **What does not reliably round-trip:** *diagram layout/graphics* — that is the job of **UML DI** (the 2004 UMLDI 1.0 plus the `UMLDI.xmi` fragment in the 2.5.1 machine-readable files), which most tools implement partially or with proprietary extensions.

**Known XMI interoperability problems — ESTABLISHED.** The XMI spec itself notes that "it is impossible to rely solely on XML validation to verify that the information transferred satisfies all of a model's semantic constraints," and the MOF/XMI history records 150+ formal usage/implementation issues. In practice, tools (MagicDraw/Cameo, Papyrus, Enterprise Architect, RSA) diverge in: XMI version emitted, UML metamodel URIs (e.g., `http://www.eclipse.org/uml2/5.0.0/UML` vs. the OMG namespace), profile/stereotype serialization, and diagram-interchange handling — so cross-tool *model* exchange is frequently lossy, and *diagram* exchange more so.

**Practical path: diagram-as-code → tool-verifiable model.** PlantUML/Mermaid/Structurizr emit *images*, not XMI, so they are a dead end for verification. To get a verifiable model: author or generate **EMF/UML2 (Papyrus)** or a **USE `.use`** specification, validate well-formedness + OCL there, and export XMI 2.5.1 for downstream consumers — accepting that diagram layout may not survive the hop. For a reverse-engineering agent, treat the **EMF/UML2 + Eclipse OCL/Papyrus** stack (or USE for OCL-heavy validation) as the verification target, and any PlantUML/Mermaid rendering as a presentation-only projection.

---

## 9. High-quality reference examples

| Example / source | What it exemplifies | Authority / link |
|---|---|---|
| **UML 2.5.1 spec, per-clause "Examples" subclauses** (e.g., 11.2.5, 11.3.5) | Canonical notation figures for each metaclass, drawn by the spec authors | OMG `formal/2017-12-05`, https://www.omg.org/spec/UML/2.5.1/PDF — ESTABLISHED, resolves |
| **OCL 2.4 spec, Clause 7 + Royal/Loyalty example** | Worked OCL invariants, pre/post, def; the LoyaltyProgram class model | OMG `formal/2014-02-03`, https://www.omg.org/spec/OCL/2.4/PDF — ESTABLISHED; Clause 7 is notably readable |
| **USE example model set** (`.use` specs; the 3-class / 3-association / 4-invariant "quick tour") | Class + OCL invariants + snapshot animation; reference OCL evaluation | github.com/useocl/use — verified repo (confirm release version, §7) |
| **Eclipse OCL example projects** (OCLinEcore, Complete OCL, interactive console) | Embedding/validating OCL on EMF/UML models | help.eclipse.org / projects.eclipse.org/projects/modeling.ocl — current 6.23.0 |
| **Warmer & Kleppe, *The Object Constraint Language* (2nd ed., 2003)** | The standard OCL reference text; "getting your models ready for MDA" | Addison-Wesley; recommended by the Eclipse OCL FAQ — ESTABLISHED |
| **Rumbaugh, Jacobson, Booch, *The UML Reference Manual* (2nd ed., 2004 / UML 2.0)** | Authoritative element-by-element UML reference | Addison-Wesley — ESTABLISHED (note: predates 2.5.1; cross-check metaclass names) |
| **OMG normative machine-readable models** (`UML.xmi`, `PrimitiveTypes.xmi`, `StandardProfile.xmi`, `UMLDI.xmi`) | The metamodel itself as XMI — ground truth for valid metaclass names | https://www.omg.org/spec/UML/20161101/ — ESTABLISHED |

---

## 10. Open questions and version caveats

- **OCL/UML alignment gap (VERSION-DEPENDENT):** OCL 2.4 is normatively aligned with UML 2.4.1/MOF 2.4.1, not UML 2.5.1. No OCL 2.5 exists. Generic/template and reflective constraints are the main expressiveness casualties; class-structure constraints are unaffected. Recommended pairing: UML 2.5.1 + OCL 2.4, with OCL consumed over the 2.5.1 abstract syntax (as Eclipse OCL/Papyrus do).
- **Compliance levels (ESTABLISHED but commonly misstated):** L0–L3 were removed in UML 2.5; "strict UML 2.5" is whole-language or nothing. Any L-level conformance claim is a 2.4.1-era artifact.
- **UML DI (VERSION-DEPENDENT/stale):** UMLDI 1.0 dates to 2004; diagram-layout interchange is weakly standardized and a primary source of cross-tool loss.
- **`oclAsSet` (OPEN):** not a standard OCL 2.4 library operation; use `Set{x}` / `->asSet()`. Treat any reference to `oclAsSet` as unverified.
- **Python coroutine / async mapping (OPEN):** no normative UML metaclass for coroutines; representation via stereotype/Comment + asynchronous messages is a convention, not a standard.
- **MRO, dynamic attributes, descriptors, runtime metaclasses (OPEN):** no faithful UML representation; annotate via Comment/stereotype or omit — do not fabricate.
- **USE version (CONFLICT / partly OPEN):** sources disagree (GitHub-releases report of v7.5.0 vs. unconfirmed; README copyright "1999-2024"; SourceForge tarball 5.2.0). Resolve against github.com/useocl/use/releases before citing.
- **USE XMI capability (OPEN):** no strong native XMI import/export confirmed in USE core; it centers on its `.use` format.
- **Umple OCL (OPEN):** no native OMG-OCL support found and no explicit vendor statement; inferred from absence.
- **PlantUML/Mermaid exact latest versions (VERSION-DEPENDENT):** both release on a fast cadence; PlantUML latest is ~v1.2026.4–v1.2026.6 (May 2026), Mermaid ~v11.15.0 — confirm at point of use.
- **Exact UML 2.5.1 subclause numbers:** several clause references here were corroborated via secondary renderings of the spec (uOttawa mirror, vendor training material) rather than a direct read of the 2.5.1 PDF; verify subclause numbers against `formal/2017-12-05` before citing in a normative context.

---

## Sources
- OMG UML 2.5.1, `formal/2017-12-05`, Dec 2017 — https://www.omg.org/spec/UML/2.5.1/ (About + PDF). Accessed 16 Jun 2026.
- OMG UML 2.5, `formal/2015-03-01`, May 2015 — https://www.omg.org/spec/UML/2.5/ . Accessed 16 Jun 2026.
- OMG OCL 2.4, `formal/2014-02-03`, Feb 2014; RTF `ptc/2013-09-01` — https://www.omg.org/spec/OCL/2.4/ (About + PDF). Accessed 16 Jun 2026.
- OMG MOF Core 2.5.1 — https://www.omg.org/spec/MOF/2.5.1/ . Accessed 16 Jun 2026.
- OMG XMI 2.5.1, June 2015 — https://www.omg.org/spec/XMI/2.5.1/ (PDF). Accessed 16 Jun 2026.
- OMG UML Diagram Interchange (UMLDI) 1.0, May 2004 — https://www.omg.org/spec/UMLDI/1.0/ . Accessed 16 Jun 2026.
- ISO/IEC 19505-1/-2:2012 (UML 2.4.1); ISO/IEC 19507:2012 (OCL 2.3.1); ISO/IEC 19508:2014 (MOF) — iso.org; modeling-languages.com. Accessed 16 Jun 2026.
- UML 2.5 compliance-level removal — training-course-material.com "UML 2.5 Intro"; UML 2.4.1 L0–L3 — ISO/IEC 19505-2 (omg.org). Accessed 16 Jun 2026.
- PseudostateKind literals — Eclipse UML2 Javadoc (download.eclipse.org); Webel UML-2.5.1 reference card. Accessed 16 Jun 2026.
- InteractionOperatorKind (twelve operators) — StarUML docs; Sparx Enterprise Architect user guide; uml-diagrams.org; USPTO patents citing the UML 2.4 fragment set. Accessed 16 Jun 2026.
- Activity control nodes — uml-diagrams.org; Sparx UML2 activity tutorial; Visual Paradigm. Accessed 16 Jun 2026.
- Composite structure / connector kind / ball-and-socket — uOttawa UML 8.3.2 mirror; uml-diagrams.org; Sparx composite-structure tutorial; Martin Fowler "Ball And Socket." Accessed 16 Jun 2026.
- OCL iterator/type operations — OCL 2.4 PDF (omg.org); Eclipse Help Collection(T); Eclipse Acceleo/OCL Operations Reference; INRIA OCL memo; TU-Dresden OCL-by-Example; OMG OCL issue tracker. Accessed 16 Jun 2026.
- Association/aggregation/composition — uml-diagrams.org composition; Sparx; arXiv formalization papers. Accessed 16 Jun 2026.
- Tooling — PlantUML (plantuml.com/download; mankier.com man page, build 2026-05-23); Mermaid (npmjs.com/package/mermaid; Snyk; security backport 10.9.6, 11 May 2026); Eclipse OCL 6.23.0 (download.eclipse.org/modeling/mdt/ocl/builds/release, v20260217); Eclipse Papyrus 7.0.0 (projects.eclipse.org, released 11 Jun 2025); Umple 1.37.0 (github.com/umple/umple/releases, 18 Apr 2026); USE (github.com/useocl/use — version unresolved, see §7/§10); Dresden OCL (github.com/dresden-ocl); Structurizr (docs.structurizr.com); ZenUML (zenuml.com); Kroki (kroki.io); TextUML (openhub.net / marketplace.eclipse.org). Accessed 16 Jun 2026.
- Python reverse-engineering — Visual Paradigm instant-reverse docs; Pynsource (github.com/abulka/pynsource); pyreverse/Pylint; Real Python (mixins/MRO/Protocols). Accessed 16 Jun 2026.
- Warmer & Kleppe, *The Object Constraint Language* (2nd ed., 2003); Rumbaugh/Jacobson/Booch, *UML Reference Manual* (2nd ed., 2004). Cited via the Eclipse OCL FAQ and ScienceDirect bibliographies.