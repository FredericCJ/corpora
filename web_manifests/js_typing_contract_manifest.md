# JavaScript Typing & Contract-Enforcement — Ground-Truth Manifest (Raw JS in the Browser)

**Version anchor:** mid-2026 (shared hub: `web_platform_baseline_manifest.md`). Checker:
**TypeScript 6.0.x** stable (23 Mar 2026; strict-by-default, `target: es2025` default), with
**TypeScript 7.0** at RC (18 Jun 2026; Go-based "Corsa" port, ~10× faster, **same checking
semantics** by design — a port, not a redesign). The constraint that shapes everything: the
deliverable is **raw `.js` files the browser executes directly** — the checker reads them; it
never transforms them. Tags: **ESTABLISHED**, **VERSION-DEPENDENT**, **OPEN**.

---

## TL;DR

- **"Strictly typed raw JS" has a precise, achievable meaning:** `tsc --noEmit` over `.js` files
  with `checkJs: true` and the strict flag family, types written as **JSDoc annotations** — full
  static checking with zero build step. Pin the tsc version and commit the exact `tsconfig.json`;
  "strict" changed meaning at the 6.0 boundary (strict became the default).
- **The type system checks shape, not values — and vanishes at runtime.** Value ranges,
  cross-field invariants, ordering, units, and typestate MUST become boundary parsing and runtime
  contracts. JSDoc type assertions are `typing.cast`-grade unchecked promises; `Object.freeze`
  is shallow; **`console.assert` never throws**.
- **Parse once at the boundary, then trust types internally.** The boundaries of a client-side
  app are: `fetch` responses, storage reads, URL/query params, `postMessage` payloads, and user
  input. Each gets a parse function returning a typed value or a typed error — never a raw
  `JSON.parse` result flowing inward as `any`.

---

## 1. The checker and what "strict" means

**One dominant checker (ESTABLISHED).** Unlike Python's mypy/pyright duality, tsc is the single
authority for JS type semantics (alternative checkers — e.g. flow — are niche in 2026; new native
tools like `tsgo` *are* tsc). The cross-conformance problem from the Python manifest collapses;
the version-pinning discipline does not.

**Checking raw JS (ESTABLISHED).** `tsconfig.json` with `"allowJs": true, "checkJs": true,
"noEmit": true` makes tsc type-check `.js` files. Types come from **JSDoc**:
`@param`, `@returns`, `@type`, `@typedef`, `@template`, `@callback`, `@satisfies`, plus
`@ts-expect-error` for tracked suppressions. Declaration files (`.d.ts`) may accompany the code
for complex shared types — they are type-level scaffolding, not implementation, and are in-scope
for a spec (cf. spec-discipline manifest A2).

**"Strict" is version-bound (VERSION-DEPENDENT).** The `strict` umbrella enables the strict flag
family (`strictNullChecks`, `noImplicitAny`, `strictFunctionTypes`, `strictBindCallApply`,
`strictPropertyInitialization`, `useUnknownInCatchVariables`, …); the family's membership grows
across releases. **TypeScript 6.0 flipped `strict`, ESM module resolution, and `target: es2025`
to defaults** — a 5.x-clean config can mean something different under 6.x. Therefore: never
write "use strict mode" in a spec; commit the literal `tsconfig.json` and the pinned tsc version.
Recommended additions beyond `strict` for contract work: `noUncheckedIndexedAccess` (indexing
returns `T | undefined` — the honest truth), `exactOptionalPropertyTypes`, `noImplicitOverride`,
`noFallthroughCasesInSwitch`.

**`useUnknownInCatchVariables` (ESTABLISHED, in strict).** `catch (e)` types `e` as `unknown`,
not `any` — correct, because **JS can throw any value**. Every catch block must narrow before
use (`instanceof Error`, or `Error.isError` — ES2026 — for cross-realm safety).

## 2. The typing vocabulary for contracts (JSDoc/TS ↔ Python mapping)

- **Structural typing is the default (ESTABLISHED).** TS is structurally typed; every
  object-shape `@typedef` is what `typing.Protocol` had to be opted into. Nominal distinction
  must be *added* when needed — see branding below.
- **Discriminated unions (ESTABLISHED).** `@typedef {{kind:'ok', value:T} | {kind:'err',
  error:E}}` — the workhorse for closed variant sets; the checker narrows on the `kind` literal
  and enforces exhaustiveness via `never` (error manifest §4–§5). Replaces `Enum`-as-variants.
- **Literal unions replace `Literal`/`Enum` (ESTABLISHED).** `'idle' | 'loading' | 'done'`. For a
  runtime-enumerable set, pair with a frozen constant object and derive the type from it
  (`/** @typedef {typeof STATES[keyof typeof STATES]} State */`) — one source of truth for both
  worlds.
- **Branded types replace `NewType` (ESTABLISHED pattern, OPEN spelling).**
  `/** @typedef {string & {readonly __brand: 'UserId'}} UserId */` — a checker-only distinct
  subtype with zero runtime cost; constructed only via a validating factory. Prevents
  UserId/OrderId mixing; the standard partial mitigation for units of measure.
- **`readonly`, `Readonly<T>`, `as const` (ESTABLISHED).** Checker-only immutability claims —
  the `Final` analogue: they forbid *your annotated code* from mutating; they do not change the
  object. Runtime immutability requires `Object.freeze` (§6).
- **Generics (ESTABLISHED).** `@template T` with constraints (`@template {Node} T`). Utility
  types (`Partial`, `Pick`, `ReturnType`, …) are usable from JSDoc.
- **`unknown` vs `any` (ESTABLISHED).** `unknown` is the honest top type (must narrow before
  use); `any` is contagion that disables checking. Strict flags catch *implicit* `any`; explicit
  `any` and untyped third-party modules are the residual leak — audit them like Python's
  `Any`-debt tracking.
- **`@satisfies` (VERSION-DEPENDENT, TS 5.0+ in JSDoc).** Checks a value against a type
  **without widening it** — the right tool for config objects: validation plus preserved literal
  inference.

## 3. Type assertions: the `typing.cast` of JS

**ESTABLISHED.** `/** @type {HTMLInputElement} */ (document.querySelector('#email'))` has **zero
runtime effect** — an unchecked promise the checker trusts blindly, exactly like `typing.cast`.
The DOM is the largest assertion factory: `querySelector` returns `Element | null`;
`event.target` is `EventTarget | null`; `JSON.parse` returns `any`.

**Confinement discipline (decision).** (1) Assert on the smallest expression, immediately after a
runtime check that validates the assumption (`instanceof HTMLInputElement`, null check); (2)
comment WHY it is safe; (3) never use an assertion to silence an error fixable structurally; (4)
prefer a tiny checked helper (`mustQuery(root, sel, HTMLInputElement)` that throws on mismatch)
over scattered raw assertions — it converts a lie into a contract. `@ts-expect-error` over
`@ts-ignore` always: it errors when the suppression becomes stale (the `--warn-unused-ignores`
analogue).

## 4. What the type system CANNOT express

Identical list to Python — value-range constraints, cross-field invariants, ordering/temporal
constraints (typestate), units of measure — **plus** browser-specific gaps (all ESTABLISHED):
- **DOM reality.** The checker cannot know that `#email` exists, is an `<input>`, or that your
  HTML and your JS agree. Every HTML↔JS touchpoint is an unchecked runtime contract; enforce
  with checked query helpers and (in tests) real-DOM assertions.
- **Event contracts.** `CustomEvent` `detail` payloads and event *names* are stringly-typed at
  dispatch/listen sites; a typed emitter/listener wrapper (or a `.d.ts` event map) restores
  checking — otherwise the event bus is an `any` channel.
- **Exceptions.** Not in signatures (no checked exceptions) — see the error manifest.
- **Purity/side-effect freedom.** No `pure` qualifier; convention + review only.
Partial mitigations mirror Python's: literal unions close domains; brands distinguish
representations; none express ranges or relations. Encode those at the boundary (§5) and as
runtime contracts (§6), and document them in the JSDoc prose (`@throws`, stated
pre/postconditions).

## 5. Boundary validation: parse, don't validate

**The boundaries of a client-side app (ESTABLISHED enumeration):** `fetch` responses; `local`/
`sessionStorage` and IndexedDB reads (old-version data!); URL, query string, and hash; form/user
input; `postMessage` payloads (workers, iframes — hostile by default across origins); imported
JSON. Everything crossing inward is untrusted.

**Mechanism (decision).** Each boundary gets a parse function: `unknown → T` (throwing a typed
`ValidationError`) or `unknown → Result<T, ParseError>`. Options, in dependency order:
- **Hand-rolled parsers (OPEN, default for zero-dependency apps).** Small typed functions using
  `typeof`/`Array.isArray`/`in` narrowing; tsc verifies the narrowing logic itself. Cost: your
  own error messages and maintenance.
- **Zod / Valibot (VERSION-DEPENDENT, opt-in tier).** Schema-first validation with **type
  inference from the schema** — schema and static type cannot drift (the pydantic analogue;
  Valibot's modular design suits browser payload budgets). Adding one is an architectural
  decision (dependency + bytes shipped to every user) — record it.
Never let a raw `JSON.parse` result (type `any`) flow past the boundary; immediately type it
`unknown` and parse.

## 6. Runtime contract enforcement

- **`Object.freeze` (ESTABLISHED).** Shallow, like `frozen=True`: nested objects stay mutable;
  in non-strict code mutation of frozen objects fails *silently* (modules are strict, so inside
  ESM it throws `TypeError`). Deep-freeze helpers exist; cost is per-object. Use for module-level
  constants and state snapshots handed across boundaries.
- **`#private` fields (ESTABLISHED, ES2022).** *Hard* encapsulation — genuinely inaccessible
  outside the class (stronger than Python's underscore convention). The enforcement half of a
  class invariant: private fields + validating methods + getters without setters.
- **Getter without setter (ESTABLISHED).** Read-only computed surface; in strict-mode code,
  assignment throws.
- **`invariant()` / explicit throws (decision — the assert replacement).** JS has no
  `assert` statement and **`console.assert` only logs — it never throws and never stops
  execution (ESTABLISHED)**. Therefore: define one tiny
  `function invariant(cond, msg) { if (!cond) throw new InvariantError(msg); }` and use it for
  can't-happen internal checks; use explicit typed errors for anything user-input-adjacent. If a
  minifier/build step is ever adopted, "strip invariant calls in production" becomes the `-O`
  question — decide it explicitly then (OPEN).
- **Where checks run (decision).** Boundary parse: once, at the edge (§5). Invariants: inside
  the core, guarding programmer error. Hot paths (per-frame render, input handlers): rely on
  types + boundary guarantees; do not re-validate.

## 7. Contract documentation conventions

**Signature vs prose (decision, unchanged principle).** JSDoc *types* carry what tsc can verify;
JSDoc *prose* carries what it cannot: preconditions (ranges, non-emptiness, relations),
postconditions, invariants, and **`@throws {ErrorType}` for every documented error mode** (the
`Raises:` analogue — unenforced, therefore mandatory as documentation). One JSDoc style
project-wide; `@example` blocks for critical contracts (executable via doctest-style test
extraction is OPEN tooling — treat examples as review-checked, not machine-checked, unless a
runner is adopted). For custom elements, the contract block additionally documents: observed
attributes, properties, emitted events + `detail` types, slots, and consumed CSS custom
properties (architecture manifest §3.5).

## 8. Version caveats and open items

- **VERSION-DEPENDENT:** the strict-family membership and compiler defaults changed at TS 6.0
  (strict/ESM/es2025 defaults); TS 7.0 (RC Jun 2026) preserves semantics but re-baseline CI at
  the major bump anyway. Pin exact versions.
- **VERSION-DEPENDENT:** `Error.isError` (ES2026) for cross-realm error checks; `using`
  (ES2026); both need engine-support verification before use in shipped raw JS.
- **OPEN:** TC39 type-annotations proposal (types as ignorable syntax in JS) remains early-stage —
  do not design for it; JSDoc is the raw-JS typing vehicle for the foreseeable window.
- **OPEN:** lint stack (ESLint + jsdoc plugin rules) exact configuration — pin at adoption; add a
  CI gate counting `@ts-expect-error`/`any` occurrences as tracked debt (the cast-audit
  analogue).

## Sources
- TypeScript handbook — JS projects & JSDoc reference; tsconfig strict-family reference —
  https://www.typescriptlang.org/docs/handbook/intro-to-js-ts.html ;
  https://www.typescriptlang.org/tsconfig/ . Accessed Jul 2026.
- Microsoft TypeScript blog — TS 6.0 GA (Mar 2026; defaults flipped), TS 7.0 RC (Jun 2026;
  Go port, identical semantics) — https://devblogs.microsoft.com/typescript/ .
- MDN — `Object.freeze` (shallow; silent failure in sloppy mode), private class fields,
  `console.assert` ("writes an error message… if the assertion is false" — logging only),
  `JSON.parse`, `structuredClone` — https://developer.mozilla.org/ .
- TC39 — ES2025 spec; Stage-4 list for ES2026 (`Error.isError`, `using`) — https://tc39.es/ .
- Alexis King — "Parse, don't validate" — https://lexi-lambda.github.io/blog/2019/11/05/parse-don-t-validate/ .
- Zod / Valibot documentation — https://zod.dev/ ; https://valibot.dev/ .
