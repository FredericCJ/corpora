# Web Platform & Language Baseline — Ground-Truth Manifest

**Purpose.** The shared **version hub** for the browser-native manifest collection. Every
VERSION-DEPENDENT claim in the sibling manifests resolves against this file. Anchored to
**mid-2026 stable releases**; re-verify at every Baseline-target or toolchain bump.
Tag legend: **ESTABLISHED** = stable, documented in a primary source; **VERSION-DEPENDENT** =
bound to a spec edition, browser release, or Baseline tier; **OPEN** = no authoritative source
or a project-policy call.

---

## TL;DR

- **Pin a Baseline target, not a browser list.** "Runs in modern browsers" is not a portable
  meaning. Commit the target — *Baseline Widely available* (conservative) or *Baseline Newly
  available as of <date>* (progressive) — to the spec, exactly as a Python spec pins its checker
  flags.
- **The language baseline is ES2025** (approved 25 June 2025, 16th edition); ES2026 features
  (`Array.fromAsync`, `Error.isError`, `using`) are landing but must be individually
  version-gated.
- **The platform is the framework.** Native ES modules, import maps, Web Components, `<dialog>`,
  popover, container queries, `:has()`, nesting, and `@layer` are all interoperable — a
  browser-native app in 2026 needs no build step and no framework to have real architecture.

---

## 1. Governance: who defines "current"

**ESTABLISHED.** Three bodies, three cadences:
- **TC39 / Ecma** — ECMAScript (the JS language). Annual editions; proposals advance through
  Stages 0–4; Stage 4 ("finished") features ship in the next yearly edition
  (https://tc39.es/process-document/). Engines ship features *before* the edition is stamped,
  so "in the spec" and "usable" are different questions.
- **WHATWG** — HTML, DOM, Fetch, Storage: **living standards** with no editions. There is no
  "HTML6"; there is only the current spec plus per-browser support.
- **W3C CSS WG** — CSS as independently-leveled modules. There is no meaningful "CSS4" version;
  availability is per-feature.

**Consequence (ESTABLISHED).** Because HTML/CSS/DOM have no versions, the only honest
compatibility statement is per-feature support — which is what **Baseline** standardizes.

## 2. Baseline: the availability contract

**ESTABLISHED** (https://web.dev/baseline; defined by the WebDX Community Group):
- **Limited availability** — not yet supported in all core browsers (Chrome, Edge, Firefox,
  Safari).
- **Baseline Newly available** — interoperable across all core browsers as of a dated moment.
- **Baseline Widely available** — 30 months past the newly-interoperable date; usable "by most
  sites without worrying about support."

**Decision — pin the target (OPEN, project policy).** A spec must state its Baseline target and
date, e.g. "Baseline Widely available as of 2026-07" or "Newly available, accepting the tail-risk
of older installed browsers." Tooling can enforce it: Baseline queries exist in **Browserslist**,
**ESLint** (including CSS linting), and VS Code hover cards show Baseline status
(https://web.dev/baseline). Treat a feature outside the pinned target as a spec violation unless
wrapped in explicit feature detection / progressive enhancement.

## 3. ECMAScript editions (the language baseline)

**VERSION-DEPENDENT.**

| Edition | Approved | Headline features |
|---|---|---|
| ES2022 | Jun 2022 | class fields & `#private` members, `Error.cause`, top-level `await`, `.at()` |
| ES2023 | Jun 2023 | change-by-copy arrays (`toSorted`, `toReversed`, `with`), `findLast`, hashbang |
| ES2024 | Jun 2024 | `Object.groupBy`/`Map.groupBy`, `Promise.withResolvers`, resizable ArrayBuffer, regex `v` flag, `Atomics.waitAsync` |
| **ES2025** | **25 Jun 2025** (16th ed.) | **Iterator helpers, Set methods (`union`, `intersection`, …), duplicate named capture groups, regex pattern modifiers, `RegExp.escape`, import attributes + JSON modules, `Promise.try`, `Float16Array`, `Intl.DurationFormat`** (https://tc39.es/ecma262/2025/) |
| ES2026 | ~Jun 2026 | `Array.fromAsync`, `Error.isError`, explicit resource management (`using`, `DisposableStack`) — reached Stage 4 in 2025; verify engine support per feature before relying on them |

**Notably NOT in the language (VERSION-DEPENDENT/OPEN):** decorators (Stage 3 since 2022, native
only via transpilers); Records & Tuples (withdrawn; smaller "Composites" successor in committee);
pipeline operator (stalled). **Temporal** is shipping in engines (Chrome early 2026) but is **not
Baseline** — keep a polyfill or avoid.

**Decision.** For a no-build raw-JS app, the safe language floor in mid-2026 is **ES2022 syntax +
feature-detect anything newer**, or ES2024/ES2025 if the pinned Baseline target is Newly
available. State the floor in the spec.

## 4. Modules: the native dependency system

- **ES modules (ESM) — ESTABLISHED.** `<script type="module">` gives deferred-by-default
  execution, strict mode, per-module scope (no accidental globals), and static `import`/`export`.
  Modules are **singletons per realm**: every importer shares one instance — which is why
  module-level mutable state is a shared-state hazard (see `web_architecture_manifest.md` §3.2).
- **Import maps — ESTABLISHED (Baseline 2023).** `<script type="importmap">` maps bare specifiers
  (`"lodash"`) to URLs, enabling dependency management without a bundler.
- **Dynamic `import()` — ESTABLISHED.** Lazy loading and code-splitting without a build step.
- **Import attributes / JSON modules — VERSION-DEPENDENT (ES2025).**
  `import config from './config.json' with { type: 'json' };` — check the pinned Baseline target;
  CSS module scripts are still Limited availability.
- **No build step is a legitimate architecture (OPEN, decision).** ESM + import maps + HTTP/2
  multiplexing make bundling an optimization, not a requirement, for small-scale apps. If a build
  step is introduced later, ESM-first code ports without rewrite. Record the no-build choice as
  an architectural decision with its tradeoff (more requests, no minification, no
  dead-code elimination).

## 5. Component & UI platform capabilities (mid-2026 status)

**VERSION-DEPENDENT — the Baseline status is the fact; the digest pages are the source
(https://web.dev/baseline, monthly digests).**

- **Web Components** — Custom Elements, Shadow DOM, `<template>`/`<slot>`: Widely available.
  Declarative Shadow DOM: Newly available Feb 2024.
- **`<dialog>`**: Widely available. **Popover API**: Newly available Jan 2025. Both replace
  whole categories of hand-rolled overlay JS.
- **CSS**: container queries and `:has()` (Widely available since 2023-era + 30 months), subgrid,
  `color-mix()`, native nesting, `@layer` (Widely available), `@scope` (Newly available Jan 2026),
  `contrast-color()` (Newly available Apr 2026), scrollbar styling (`scrollbar-color` Newly
  available Dec 2025). View transitions (same-document): check current tier before relying on it —
  design as progressive enhancement.
- **Form platform**: Constraint Validation API, `:user-valid`/`:user-invalid`, `inert`,
  ElementInternals for form-associated custom elements — all interoperable; prefer them over
  custom validation JS.

**Principle (ESTABLISHED direction, OPEN phrasing): use the platform before writing JS.** Every
capability above deletes a class of custom code. The architecture manifest's "declarative
paradigm" row (§2) is this principle generalized.

## 6. The network, storage, and worker capability facts

- **`fetch` — ESTABLISHED (WHATWG).** The one HTTP boundary. Critical contract fact: **fetch
  rejects only on network failure; an HTTP 4xx/5xx resolves successfully with `response.ok ===
  false`** — checking `response.ok` is the caller's job (see error manifest §12).
  `AbortController` is the cancellation primitive.
- **Storage — ESTABLISHED.** `localStorage`/`sessionStorage`: synchronous, string-only,
  ~5 MB-order quotas, blocks the main thread. **IndexedDB**: async, structured data, the correct
  choice for anything non-trivial. All storage is per-origin, user-clearable, and **untrusted
  input on read** (another parse boundary).
- **Workers — ESTABLISHED.** Web Workers = message passing via structured clone; no DOM access.
  `SharedArrayBuffer` + `Atomics` exist but require cross-origin isolation (COOP/COEP headers).
  Service Workers add offline/caching (a whole subsystem — treat adopting one as an
  architectural decision, not a default).
- **Security platform — ESTABLISHED.** Same-origin policy and CORS govern the API boundary;
  Content-Security-Policy and Trusted Types (Baseline Newly available Feb 2026) govern injection
  sinks. `innerHTML` with untrusted data is the canonical XSS sink; `textContent` is the safe
  default.

## 7. Toolchain versions (mid-2026)

**VERSION-DEPENDENT — pin exact versions in `package.json` even for a no-build app (the tools run
in CI, not in the browser):**
- **TypeScript (as a *checker* for raw JS)** — 6.0.x stable (Mar 2026; strict-by-default, ESM
  default, `target: es2025` default); 7.0 RC (18 Jun 2026, Go-based, ~10× faster, same checking
  semantics). See `js_typing_contract_manifest.md`.
- **Vitest 4.1.x** (browser mode stable since 4.0, Oct 2025); **Playwright ~1.60** (Jun 2026).
  See `web_testing_tooling_manifest.md`.
- **ESLint** with Baseline-aware rules; **Browserslist** Baseline queries. (Exact versions OPEN —
  pin at adoption time.)

## 8. Open questions / caveats

- Baseline tiers move monthly; the tables in §5 are a snapshot. The durable habit is checking the
  MDN Baseline badge per feature, not memorizing lists (OPEN/process).
- ES2026's formal approval date and final feature list must be confirmed against
  https://tc39.es/ecma262/ before citing it as "the" baseline (VERSION-DEPENDENT).
- fast-check, ESLint, and Browserslist exact versions were not pinned in this snapshot — pin them
  in `package.json` at adoption (OPEN).

## Sources
- TC39 — ECMAScript 2025 spec and process document — https://tc39.es/ecma262/2025/ ;
  https://tc39.es/process-document/ . Accessed Jul 2026.
- web.dev — Baseline definition, yearly and monthly digests (Jan–May 2026) —
  https://web.dev/baseline ; https://web.dev/baseline/2026 . Accessed Jul 2026.
- InfoQ — TC39 Stage-4 advancements Jun 2025 (`Array.fromAsync`, `Error.isError`, `using`).
- Microsoft TypeScript blog — TS 6.0 GA (Mar 2026), TS 7.0 RC (Jun 2026) —
  https://devblogs.microsoft.com/typescript/ . Accessed Jul 2026.
- WHATWG — HTML/Fetch/DOM living standards — https://html.spec.whatwg.org/ ;
  https://fetch.spec.whatwg.org/ .
- MDN Web Docs — per-feature Baseline badges — https://developer.mozilla.org/ .
