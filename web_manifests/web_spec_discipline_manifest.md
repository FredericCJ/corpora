# Software Specification Discipline — Manifest (Browser-Native Web Target)

Scope: durable discipline for producing implementation-agnostic architectural and design
specifications for small-scale **browser-native web applications** (raw HTML/CSS/JS, client-side,
API calls only where unavoidable), optimized for component reusability. GROUNDING, not a
rulebook. **This discipline is ~90% language-independent**: the requirements cascade (B),
reusability doctrine (C), elicitation (D), requirements writing (E), and traceability (G) of the
Python sibling apply **verbatim** and are not restated. This file records only the clauses the
web target changes, keeping the sibling's numbering.

## A. The implementation-agnostic specification boundary — web deltas

A1. **Unchanged.** Specify the contract, not the computation.

A2. **Type-level scaffolding, web forms.** In scope: JSDoc typedefs and `.d.ts` declarations,
    discriminated-union shapes, branded types, custom-element contract blocks
    (attributes/properties/events/slots/CSS custom properties), event `detail` schemas, and
    boundary parse-function signatures (`unknown → T | ParseError`). Out of scope: function
    bodies, DOM-manipulation sequences, concrete rendering algorithms. **HTML structure sits on
    the boundary:** the *semantic contract* (landmark roles, heading hierarchy, form-control
    semantics, the accessibility tree the user must get) is spec; the concrete markup tree is
    implementation.

A3. **Implementation-agnostic is not platform-agnostic.** The spec targets the web platform and
    may rely on it: the checker (tsc, pinned version + committed config), the **pinned Baseline
    target** (`web_platform_baseline_manifest.md` §2), ES modules, and platform features within
    the target (dialog, popover, constraint validation, container queries). These are platform
    CONSTRAINTS the spec is entitled to assume, not implementation decisions. A feature *outside*
    the Baseline target used anyway is an architectural decision with a mandatory
    progressive-enhancement/fallback clause.

A4. **Test obligations, not test code — plus tier.** Each obligation additionally names its
    **execution tier** (pure / component / integration / E2E) and therefore its environment
    (Node / real-browser / simulated DOM), per `web_testing_tooling_manifest.md` §2 and §6.
    Accessibility obligations (keyboard operability, focus order, name/role/state) are
    first-class rows in the obligation table, not polish.

## B. The requirements cascade — one addition

B2 (falsification), web lens additions for the designer trying to break the architecture: a
component whose reuse requires global CSS; an event contract too loose to implement against
(undeclared bubbling/`detail` shape); a state read back out of the DOM; a seam that cannot be
faked because the component reaches for `fetch`/`Storage`/`Date` globals; a feature silently
below the Baseline target.

B4 addition: **the Baseline target, the no-build decision, and the telemetry decision are
architectural-decision requirements** — recorded with rationale, never buried in functional
requirements.

## C. Reusability — web deltas

C1–C5 unchanged in substance. Web-specific reuse tax items the dependency surface MUST declare
(per C3/C5, the reuse trace): required DOM environment (light vs shadow, expected container),
consumed CSS custom properties and any required stylesheet, injected platform dependencies
(fetch/storage/clock/logger), emitted and listened-for events, Baseline features assumed, and
bytes shipped (a browser component's payload is part of its reuse cost). A component that
mutates global state (`window`, `document` head, global styles) outside its declared surface
fails atomic reusability by definition.

## D–E. Elicitation and requirements writing — unchanged

Apply verbatim (stated-needs profiling; epistemic tagging STATED/INFERRED/ASSUMED/
ARCHITECTURAL-DECISION/UNRESOLVED; EARS syntax; INVEST/29148 review; negative space). One web
default worth naming (ASSUMED unless the user states otherwise): the runtime inputs of a
client-side app include **hostile or malformed data from every boundary** (URL, storage from old
versions, API responses) and **a user on a keyboard, a slow network, and a small screen** —
specify for what will arrive.

## F. Testability reasoning — web reading

F1. **Pure core, imperative shell:** the shell *is* the DOM + fetch + storage + timers; push all
    decisions into pure `(state, event) → state` and derivation functions.
F2. **Dependency inversion at every side-effect boundary:** components declare fetch/clock/
    storage/logger as typed injected dependencies (JSDoc-typed structural interfaces — the
    Protocol analogue).
F3. **Observable contracts over hidden state:** return values and dispatched events with typed
    `detail`, never internal DOM structure, as the assertion surface.
F4. **Fakes over mocks-on-mocks:** in-memory `Storage`, `Response`-returning fake fetch —
    `web_testing_tooling_manifest.md` §3.
F5. **Integration strategy owned at architecture altitude:** the architect names which seams run
    against real browser / real storage / mock server; the designer expresses them as contracts.
F6. **Property obligations** for parsers (round-trip on every boundary parse function) and
    reducers (validity-preservation over event sequences).

## G. Output and traceability — unchanged

SR-n → component → design spec → verification spine; reusability ledger (with the C-section web
surface items); decision log with preserved dissent; ASSUMED vs NEEDS-INPUT split. One addition:
the ledger's per-component row links its **custom-element/module contract block** (A2) — that
block is the "standalone contract" artifact C5 demands.
