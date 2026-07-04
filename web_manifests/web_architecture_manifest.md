# Software Architecture Manifest — Browser-Native Web Applications

## Purpose

Grounding context, not a rulebook, for architecting applications built with raw HTML, CSS, and
JavaScript, running entirely client-side, with API calls only where unavoidable. It adapts the
domain-agnostic architecture manifest to the browser: the vocabulary, paradigm menu, and
tradeoff axes carry over; this file states what the browser changes. Version-dependent platform
facts live in `web_platform_baseline_manifest.md` and are not repeated.

The architect reasons from first principles. The manifest exists to make that reasoning legible
and to surface the browser-specific tradeoffs that are easy to forget.

---

## 1. Vocabulary — browser mapping

All terms from the domain-agnostic manifest apply unchanged (component, contract, invariant,
seam, coupling, cohesion, state ownership, pure function, side effect, observability). The
browser adds concrete referents:

- **Component.** An ES module with a stated responsibility — optionally packaged as a **custom
  element** when it owns a DOM subtree. A custom element is a component whose interface is
  attributes/properties (in), events (out), and slots (composition).
- **Seam.** In browser JS, the cheapest seams are: a function parameter (pass `fetch`, the
  clock, the storage object in), a custom-element attribute/property, a dispatched event, and an
  import-map entry (swap a module URL without touching importers).
- **Side effect.** The dominant side effects are **DOM mutation**, `fetch`, storage writes,
  timers, and navigation. "Pure" in the browser means: touches none of these.
- **The three languages are three concerns (ESTABLISHED web doctrine).** HTML carries structure
  and semantics; CSS carries presentation; JS carries behavior. Violations (layout constants in
  JS, semantics faked with styled `<div>`s, behavior in inline attributes) are coupling across
  concern boundaries and cost accessibility, cacheability, and testability.

## 2. The paradigm menu, re-read for the browser

The menu from the default manifest applies; the browser shifts the fits:

- **Declarative (HTML/CSS first).** *The browser-specific paradigm.* Fit: anything the platform
  already does — dialogs, popovers, form validation, container-responsive layout, transitions.
  Degrades when: the declarative feature is below the pinned Baseline target (then it becomes a
  progressive enhancement, not the mechanism). Watch for: JS re-implementations of platform
  features; they are the web's god-classes.
- **Event-driven.** *Native, not optional.* The DOM is an event system; user input arrives as
  events. Fit: all UI wiring; component-boundary signaling via `CustomEvent` (bubbling +
  `composed` are design decisions). Degrades exactly as the default manifest warns: hidden
  control flow, event storms, ordering assumptions. Watch for: components that communicate by
  *listening to each other's internals* instead of a declared event contract.
- **Functional.** Fit: the state core — reducers/transitions as pure functions
  `(state, event) → state`, formatting, validation, derivations. This is the unit-testable half
  of the app.
- **Modular.** ES modules are the baseline discipline. Boundaries by responsibility
  (feature/subdomain folders), not technology (`utils/`, `helpers/`). Module-level `let` is
  global mutable state in disguise (§3.2).
- **Object-oriented.** Fit: custom elements (the platform demands classes), and entities with
  identity + lifecycle. Degrades: inheritance for reuse; deep element hierarchies. Prefer
  composition (slots) over subclassing elements.
- **Dataflow / pipeline.** Fit: streams (`ReadableStream`), iterator-helper chains (ES2025),
  render pipelines `state → vdom-less DOM patch`.
- **Actor / message-passing.** Fit: Web Workers for heavy compute; each worker owns its state,
  communicates by structured-clone messages. Reserve `SharedArrayBuffer` for measured hot paths
  (requires cross-origin isolation).

## 3. Cross-cutting concerns

### 3.1 State and the DOM: the single most important decision

- **State lives in JS; the DOM is a projection (OPEN — convention, but the load-bearing one).**
  One plain-data application/component state object is the source of truth; rendering derives the
  DOM from it. **Never read state back out of the DOM** (parsing `textContent`, checking
  classlists to know a mode) — that makes the DOM a second, unsynchronized source of truth and is
  the browser's version of shared mutable ownership.
- **Unidirectional flow.** Events → pure transition → new state → render. Debugging becomes
  "which event, which transition" instead of "which of 14 handlers mutated this node."
- **Ownership is named.** Each piece of state has exactly one owning module/component; others
  observe via events or read-only accessors. Form elements are a deliberate exception: the
  browser owns transient input state until you commit it (read on `change`/`submit`).
- **Persistence is a boundary.** localStorage/IndexedDB reads are *untrusted input* — parse and
  validate on the way in (schema may be from an old app version), exactly like an API response.

### 3.2 Global state and the realm

A page is one realm: module-level mutables, properties hung on `window` or
`document`, and singleton custom-element registries are all global state shared by everything on
the page. The default manifest's warning applies with more force: test isolation in the browser
means a fresh realm, which is expensive. Prefer constructor/parameter injection; keep
module-level bindings `const` and immutable.

### 3.3 Error handling

Pick one style per module boundary (see `js_error_tracing_contract_manifest.md`): typed
discriminated-union results for expected domain outcomes; thrown `Error` subclasses (with
`cause`) for exceptional ones. The async surfaces — rejected promises, event-handler exceptions —
make "errors never pass silently" require explicit top-level handlers
(`window` `error` / `unhandledrejection`) wired at the shell.

### 3.4 Concurrency

The model is chosen for you: **single-threaded event loop** on the main thread. Consequences:
- Long synchronous work **freezes the UI** — the main thread is a latency budget, not a compute
  resource. Chunk with `await`/`scheduler.yield`-style patterns or move to a **worker**
  (message-passing model).
- There are no data races on the main thread, but there are **interleaving hazards**: two awaited
  operations touching the same state can interleave at every `await`. Re-check invariants after
  each `await`; treat `async` boundaries the way threaded code treats lock releases.
- Stale-response races (`fetch` A resolves after newer `fetch` B) are the canonical bug: use
  `AbortController` or request-id checks.

### 3.5 Interfaces and contracts

A component's frozen surface in the browser is: its **module exports** (typed via JSDoc — see
typing manifest), and for custom elements its **attributes/properties, emitted events (names +
`detail` shape), slots, and CSS custom properties / `part`s**. Everything else — internal DOM
structure, class names inside a shadow root — is implementation. Document the event contract
with the same rigor as a return type: an undeclared bubbling event is an undeclared error mode.

### 3.6 CSS architecture

CSS is code with global scope by default; architect it:
- **`@layer`** for explicit cascade ordering (reset → base → components → utilities) instead of
  specificity wars.
- **Custom properties** as the theming/parameterization contract — the CSS equivalent of
  dependency injection; a reusable component consumes `--component-*` variables and documents
  them.
- **Scoping**: shadow DOM (hard boundary, style isolation both ways — a tradeoff, not a free
  win), `@scope` (Newly available 2026 — check target), or a naming convention. Pick one per
  project.
- A reusable component **must not require global CSS** to function; its styles travel with it
  (shadow styles, or a documented single stylesheet import).

### 3.7 The network boundary (API calls "only where unavoidable")

Treat every endpoint as a component with a contract: URL, method, request/response schema, error
modes, timeout/abort policy. Confine all `fetch` calls to a thin client module (the imperative
shell's outer edge); the rest of the app consumes typed parsed results and can be developed and
tested against a fake client. Offline/latency behavior is part of the contract — the network is
optional in a client-side app, so every call needs a defined failure rendering.

### 3.8 Observability

Design in, don't retrofit (details: `browser_observability_manifest.md`): state transitions are
loggable events; boundary crossings (fetch in/out, storage read/write) are logged at the shell;
components emit through an injected logger seam, never `console.*` directly.

## 4. Testability patterns (browser deltas)

The pyramid, seams, doubles, and determinism rules translate intact
(`web_testing_tooling_manifest.md` for tooling facts). Browser-specific:
- **The pure core needs no browser.** Reducers/derivations run in any JS runtime — the cheapest,
  fastest test tier. Maximize it.
- **DOM-touching units** run against a real browser (Vitest browser mode) or a simulated DOM
  (jsdom/happy-dom) — the simulation gap (no layout, partial APIs) is a known false-confidence
  source; anything layout- or focus-sensitive needs a real engine.
- **Inject the platform**: `fetch`, `Storage`, the clock, `crypto.getRandomValues` — pass them
  in; a component that calls the globals directly has no seam.
- **Custom elements are integration-shaped**: registered globally, lifecycle driven by the
  browser. Keep their logic in importable pure functions; test the element itself as a thin
  integration layer (attributes in → DOM/events out).

## 5. Debuggability patterns (browser deltas)

- **Fault isolation**: "if this component breaks, how does the page present?" A blank page means
  an unhandled top-level failure; design for partial rendering (one failed widget ≠ dead app).
- **Observable boundaries**: log post-parse inputs and emitted events at component seams; DevTools'
  event-listener and `monitorEvents` tooling replaces nothing — structure beats grep here too.
- **Error propagation**: chain with `cause`; async gaps eat stack traces, so context must be
  attached at the boundary (error manifest §8–§9).
- **State-transition tracing**: with a single reducer, one debug-mode log line per transition
  answers "how did we get here" for the whole app.

## 6. Refactoring patterns

All default-manifest patterns apply (rename/extract, extract seam, parallel change, branch by
abstraction, strangler fig, characterization tests). Browser-specific levers: **import maps** as
a substitution point (point a bare specifier at the new implementation), **custom-element
renaming** for parallel change (`x-widget-v2` alongside `x-widget`), and CSS `@layer`
introduction as the non-breaking path out of specificity debt.

## 7. Tradeoff axes — browser-specific additions

The default axes (generality/specificity, explicit/convention, etc.) apply. Add:
- **Platform feature vs. custom implementation.** Default: platform. Deviate only when the
  feature is below the Baseline target or measurably insufficient — and record it.
- **Shadow DOM vs. light DOM.** Isolation and slot composition vs. global-CSS themability and
  simpler testing/a11y tooling. Per-component decision; name it.
- **No-build vs. build step.** Zero-tooling simplicity vs. minification/bundling/type-stripping.
  Default for small apps: no build (ESM + import maps); revisit at measured load-time cost.
- **Progressive enhancement vs. JS-required.** A client-side app is JS-required by definition,
  but *within* it: HTML-first (works before/without a given script) vs. fully script-rendered.
  Cheaper resilience than it looks; decide per feature.
- **Network chattiness vs. client complexity.** Every avoided API call is client-side state to
  own (caching, staleness, sync). Name which side each feature lands on.
