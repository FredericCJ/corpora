# Web Testing & Verification — Ground-Truth Manifest (Raw HTML/CSS/JS)

**Scope.** Ground truth for defining TEST OBLIGATIONS and an integration-test strategy for
small-scale, browser-native applications (raw HTML/CSS/JS, client-side, minimal API calls).
Tags: **ESTABLISHED**, **VERSION-DEPENDENT** (versions as of mid-2026; hub:
`web_platform_baseline_manifest.md`), **OPEN**. The language-independent doctrine — obligations
not tests, equivalence classes + boundary values, doubles taxonomy, fakes over mocks, coverage as
diagnostic (Fowler), functional core / imperative shell (Bernhardt) — is inherited verbatim from
the Python testing manifest and not re-derived here; this file states the web-specific facts and
deltas.

## TL;DR
- Adopt **Vitest 4.1.x** as the runner: pure-core tests in Node for speed, **Browser Mode**
  (stable since 4.0, Oct 2025; Playwright provider) for DOM-touching units, **Playwright ~1.60**
  for end-to-end flows. `node:test` is the zero-dependency fallback.
- **The unit/integration line has a third axis in the browser: DOM fidelity.** Pure JS →
  no DOM; component logic → real browser or simulated DOM (jsdom/happy-dom — a known
  false-confidence source for layout, focus, and newer APIs); user flows → real browser via
  Playwright. Choose the cheapest tier that makes the obligation honest.
- **Inject the platform.** `fetch`, `Storage`, time, and randomness are the browser's
  non-determinism sources; a component that reaches for the globals has no seam. Fakes
  implementing the real Web-API contracts (in-memory `Storage`, a stub `fetch`
  returning `Response` objects) beat mock towers.

## 1. Runner landscape (VERSION-DEPENDENT)

- **Vitest 4.1.x** (4.0 released Oct 2025; 4.1.9 current Jun 2026). Default recommendation:
  plain-function tests, first-class ESM, fixtures via `test.extend` (the dependency-injection
  analogue of pytest fixtures), parametrization via `test.each`, built-in fake timers and
  `vi.fn`/`vi.spyOn`. **Browser Mode is stable in 4.x**: the same test API executed in a real
  browser via provider packages (`@vitest/browser-playwright` et al.), with visual-regression
  screenshots and Playwright trace generation. Rationale mirrors the pytest decision: minimal
  boilerplate, composable DI, incremental adoption.
- **Playwright ~1.60** (Jun 2026): the E2E layer — real Chromium/Firefox/WebKit, auto-waiting,
  fixtures, tracing. Use for user-visible flows and the API-boundary contract against a mock
  server (`page.route`) or a real staging endpoint in a small marked suite.
- **`node:test` (ESTABLISHED, stdlib).** Zero-dependency runner in Node itself
  (`node --test`), with `assert`, mocking, and coverage flags — the `unittest` analogue. Fits a
  hard "no dev-dependencies" constraint; pure-core only (no DOM).
- **@web/test-runner (OPEN/alternative).** Modern-Web's browser-native runner executing tests as
  real ES modules in real browsers with no transform — philosophically closest to "raw JS";
  smaller ecosystem than Vitest. Legitimate choice; record it as a decision if taken.

**Simulated DOM caveat (ESTABLISHED).** jsdom/happy-dom implement a subset of the platform:
**no layout** (all geometry reads are zero), partial focus/navigation semantics, and lag on newer
APIs. A green jsdom suite proves logic wiring, not rendering truth. Obligations touching layout,
visibility, focus order, or dialogs/popovers must run in a real engine (Browser Mode or
Playwright).

## 2. The unit–integration boundary in the browser

Feathers' definitions and the seam concept apply unchanged. The web-specific reading:
- **Unit (pure tier):** no DOM, no `fetch`, no storage, no timers, no real browser — reducers,
  parsers, formatters, derivations. This tier should dominate (functional core).
- **Unit (component tier):** one custom element / render module against a real or simulated DOM,
  all platform collaborators faked. Observable contract: attributes/properties in → DOM state +
  emitted events out.
- **Integration:** two or more components wired on a page, or a component against a *real*
  platform boundary (real IndexedDB, real `fetch` to a local test server).
- **System/E2E:** Playwright driving the full page. Last line of defense; if it is the first
  line, the lower tiers are under-designed.

**Web seams (ESTABLISHED catalogue):** function/constructor parameters (pass `fetch`, clock,
storage in); custom-element attributes/properties; dispatched events (assert on
`CustomEvent.detail` instead of internals); import-map/module substitution; and network
interception (Playwright `page.route`, MSW) as the seam of last resort when injection isn't
available.

## 3. Test doubles, precisely (web instances)

Taxonomy (dummy/fake/stub/spy/mock; only mocks insist on behavior verification) — inherited.
Concrete web doubles:
- **Fake `fetch` (decision-grade pattern).** An injected `async (url, init) => new Response(...)`
  — implementing the *real* `Response` contract (status, `ok`, `.json()`), so the code under test
  exercises its genuine parsing path. Prefer this over mocking your own API-client wrapper.
- **Fake `Storage` (ESTABLISHED pattern).** ~15 lines over a `Map` implementing
  `getItem/setItem/removeItem/clear/key/length` — a fake in the strict sense: a working
  implementation unsuitable for production.
- **Fake clock/timers.** Vitest `vi.useFakeTimers()` / `vi.setSystemTime()`; or inject
  `now: () => number` into the core and skip the machinery.
- **Spies:** `vi.fn()` for callback/event-handler verification.
- **Module mocking (`vi.mock`) — use sparingly (decision).** It patches the module graph — the
  monkeypatch analogue — coupling tests to import structure. A constructor-injected fake
  survives refactors; a module mock often does not. Over-mocking hazard (Fowler) unchanged.
- **Contract-test symmetry (inherited principle):** run one contract suite against both the fake
  and the real implementation (e.g. the fake fetch client vs. Playwright hitting the mock
  server) so the fake cannot drift.

## 4. Determinism sources in the browser

Inherited rule — inject or isolate every non-determinism source. The browser's list
(ESTABLISHED): time (`Date.now`, `performance.now`, timers, `requestAnimationFrame`); randomness
(`Math.random`, `crypto.getRandomValues`, `crypto.randomUUID`); network (never real in
unit/component tiers); **async scheduling** (microtask vs task ordering — await explicit
conditions/events, never `setTimeout`-sleep in tests); viewport/layout (pin viewport size in
browser tiers); storage (fresh fake or cleared origin per test); locale/timezone (pin in config —
`Intl` output differs per environment).

## 5. Property-based testing

**fast-check (VERSION-DEPENDENT — pin at adoption; OPEN exact version).** The Hypothesis
analogue: arbitraries (`fc.integer()`, `fc.string()`, `fc.record()`), `fc.assert(fc.property(...))`,
automatic **shrinking** to minimal counterexamples, and **model-based testing**
(`fc.commands`) as the stateful analogue of `RuleBasedStateMachine`. Property classes map
one-to-one: round-trip (serialize/parse — apply to every §5-boundary parser in the typing
manifest), invariant, oracle, metamorphic. Fit: the pure core. Weak for: DOM/effectful shells —
example-based there. One web-specific target worth naming: **reducer properties** (any event
sequence from a valid state yields a valid state) — cheap, high-yield.

## 6. Specifying obligations vs writing tests

Inherited framing: obligation = observable contract at a named seam + input partitioning +
expected observable + error-path coverage. Web addenda:
- Component obligations name the **event contract** ("dispatches `item-selected` with
  `detail: {id}` when…") and the **DOM observable** (role/name/state via accessible queries —
  `getByRole`-style — not class names or node paths, which are implementation).
- **Accessibility obligations are first-class (decision):** keyboard operability and
  focus behavior are observable contract, not polish; put them in the obligation table for every
  interactive component.
- Error paths include: network failure vs HTTP error (distinct branches — see error manifest
  §12), parse failure on malformed payloads, storage quota/absence, and aborted requests.

## 7. Coverage

**V8-native coverage (ESTABLISHED mechanism):** Vitest `@vitest/coverage-v8` (or Istanbul
provider); `node:test` has `--experimental-test-coverage`; Playwright exposes raw V8 coverage.
Fowler's rule inherited unchanged: a flashlight for untested branches — especially the error
paths of §6 — never a numeric target; upper-80s/90s is a smell-check range; ban assertion-free
tests before honoring any externally-mandated gate.

## 8. Recommendations

1. **Pin the toolchain:** Vitest 4.1.x (+ `@vitest/browser-playwright`), Playwright 1.60.x,
   fast-check (pin at adoption), coverage-v8 — exact versions in `package.json`; config in
   version control. Re-baseline at each major.
2. **Tier the obligations:** every obligation names its tier (pure / component / integration /
   E2E) and hence its runner environment; default each obligation to the cheapest honest tier.
3. **Architect the seams first:** constructor/parameter injection for `fetch`, clock, storage;
   event contracts as the component observable. If a test needs `vi.mock`, treat it as a seam
   smell.
4. **Contract-test the fakes** against real implementations in the small integration layer.
5. **Property-test the parsers and reducers;** example-test the DOM shell.
6. **Run the component tier in a real browser** for anything layout/focus/dialog-adjacent;
   confine simulated DOM to logic-wiring tests where its speed pays.

## Caveats
- Version facts are a mid-2026 snapshot (Vitest 4.1.9, Playwright ~1.60, TS 6.0/7.0-RC); verify
  against changelogs before adoption — the Python manifest's "prefer the changelog over lagging
  registry pages" warning applies to npm equally.
- The jsdom-gap list (no layout, partial focus) is drawn from project documentation and widely
  reproduced experience; the precise gap set moves per release — re-verify when a simulated-DOM
  test behaves suspiciously green (OPEN, moving target).
- Which seams to cut and the target test mix remain the team's strategy decisions; this file
  supplies definitions and tooling facts only.

## Sources
- Vitest — v4 announcement (Browser Mode stable, visual regression, Playwright traces; Oct 2025),
  browser-provider docs, `test.extend`/fixtures, fake timers — https://vitest.dev/ ;
  https://voidzero.dev/posts/announcing-vitest-4 . Accessed Jul 2026.
- Playwright — docs (fixtures, `page.route`, tracing); v1.60 current Jun 2026 —
  https://playwright.dev/ .
- Node.js — `node:test` runner and coverage — https://nodejs.org/api/test.html .
- fast-check — property-based testing and model-based (`fc.commands`) docs —
  https://fast-check.dev/ .
- Modern Web — @web/test-runner — https://modern-web.dev/docs/test-runner/overview/ .
- jsdom README (unimplemented parts: layout/navigation) — https://github.com/jsdom/jsdom .
- Martin Fowler — "Mocks Aren't Stubs", "Test Double", "TestCoverage"; Gary Bernhardt —
  "Boundaries" (functional core / imperative shell); Michael Feathers — *WELC* seams. (Same
  primary sources as the Python manifest.)
