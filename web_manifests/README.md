# Browser-Native Web Application Manifests — Collection Overview

**Target use case.** Entire applications built with **raw HTML, CSS, and JavaScript**, running
**entirely client-side** in the browser, with API calls to remote endpoints only where truly
unavoidable. No framework, no mandatory build step. These manifests are GROUNDING, not rulebooks:
cite a principle when it materially shapes a decision; reason beyond it when the situation does
not match.

**Version anchor.** All version-dependent facts are anchored to **mid-2026** (see
`web_platform_baseline_manifest.md`, the shared version hub). Re-verify at every toolchain or
Baseline-target bump.

## The files

| File | Role | Python sibling it translates |
|---|---|---|
| `web_platform_baseline_manifest.md` | Version hub: ECMAScript editions, Baseline targets, module system, platform capability facts | (no direct sibling — replaces the per-manifest "version anchor" headers) |
| `web_architecture_manifest.md` | Architecture principles for browser-native apps: paradigms, state, DOM boundary, concurrency, testability, debuggability | `architecture_manifest_default.md` |
| `js_typing_contract_manifest.md` | Static checking of raw JS (tsc + JSDoc), runtime contract enforcement, what the checker cannot express | `python_typing_contract_manifest.md` |
| `web_testing_tooling_manifest.md` | Test runners, browser vs simulated DOM, doubles, property-based testing, coverage | `python_testing_tooling_manifest.md` |
| `js_error_tracing_contract_manifest.md` | Error propagation channels, `Error.cause` chaining, async failure surfaces, assertions | `error_tracing_contract_manifest.md` |
| `browser_observability_manifest.md` | Console semantics, the missing logger architecture and how to build the seam, telemetry, privacy | `logging_observability_manifest.md` |
| `web_spec_discipline_manifest.md` | Specification discipline adapted to the web target | `software_spec_discipline_manifest.md` |

## Translation map — which Python principles carry over

### Translate DIRECTLY (language-independent)
- The entire **vocabulary** (component, contract, invariant, seam, coupling, cohesion, state
  ownership, pure function, observability) and the **tradeoff axes**.
- **Functional core / imperative shell** — arguably fits the browser *better* than Python: the DOM,
  `fetch`, storage, and timers form a natural imperative shell around pure state-transition logic.
- **Parse, don't validate** at the boundary; trust typed data internally.
- **Test doubles taxonomy** (dummy/fake/stub/spy/mock), fakes-over-mocks, seams via dependency
  injection, determinism rules (inject time/randomness/network).
- **Coverage as diagnostic, not target** (Fowler / Goodhart).
- **Spec discipline** wholesale: contract-not-computation, epistemic tagging, requirement atomicity,
  traceability, reusability ledger, YAGNI.
- **Error-handling asymmetry**: no checked exceptions in JS either, so the "typed in-band result vs
  raised exception" split and the exhaustiveness discipline translate one-to-one.
- **Log once at the handling boundary; never pass silently; never log secrets.**

### Translate WITH ADAPTATION (same principle, different mechanics)
- **Strict static typing** → there is one dominant checker (tsc) instead of two (mypy/pyright), and
  it checks *raw* `.js` files via `checkJs` + JSDoc annotations. "Pin the checker version and commit
  the flag set" survives intact; the mypy-vs-pyright cross-conformance problem largely disappears.
- **`typing.cast`** → JSDoc/TS type assertions (`/** @type {X} */ (expr)`) — same "unchecked promise"
  hazard, same confinement discipline. `querySelector` results are the most common cast site.
- **`frozen=True` dataclass** → `Object.freeze` — same *shallow*, bypass-adjacent immutability caveat.
- **`raise X from Y`** → `new Error(msg, { cause: err })` (ES2022) — same chaining semantics, same
  display in stack traces (engine-dependent rendering).
- **`ExceptionGroup`** → `AggregateError` + `Promise.any`/`allSettled` — same "use selectively" rule.
- **Context managers** → explicit resource management (`using`, ES2026) — new, version-gate it.
- **Concurrency menu** → the browser *forces* the single-threaded event loop as the default model;
  Web Workers are the message-passing option; shared memory exists only behind COOP/COEP headers.
- **Module boundaries** → native ES modules; "no module-level mutable state" matters *more* because
  a module instance is shared across the whole page realm.

### Do NOT translate (drop or replace)
- **The stdlib `logging` architecture** (logger hierarchy, handlers, formatters, `NullHandler`,
  propagation) — no browser equivalent exists. The *goal* (components emit, applications route)
  survives; the *mechanism* must be designed as an explicit injected-logger seam
  (`browser_observability_manifest.md` §4).
- **`assert` stripped under `-O`** — JS has no optimize-strips-asserts mode, but the hazard mutates:
  `console.assert` **never throws**, so it is even more dangerous as a pseudo-enforcement tool.
  The rule becomes: enforcement = explicit `throw`; `console.assert` is logging only.
- **pytest fixtures/conftest machinery** — replaced by runner-specific mechanics (Vitest fixtures,
  Playwright fixtures); the DI *principle* stays, the mechanism differs.
- **pydantic as the default boundary parser** — no equivalent dominance; hand-rolled parse functions
  are idiomatic for zero-dependency apps, with Zod/Valibot as the opt-in library tier.
- **GIL/threading concerns, `-O`/bytecode facts, PEP-numbered governance details** — Python-specific;
  replaced by TC39 stages, WHATWG living standards, and Baseline availability tiers.
