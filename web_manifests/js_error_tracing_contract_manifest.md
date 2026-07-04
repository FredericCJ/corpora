# Error-Tracing & Exception-Handling Contract — Ground-Truth Manifest (Browser JS)

**Purpose.** Citable ground truth for error propagation, exception handling, traceable messages,
and assertion placement in **strictly-checked raw JavaScript** organized as functional core /
imperative shell, running in the browser. GROUNDING, not a rulebook. Tags: **ESTABLISHED**
(ECMAScript/WHATWG-normative or long-stable), **VERSION-DEPENDENT** (spec-edition or
engine-bound), **OPEN** (design synthesis the team must pin). Language mechanics not repeated
from siblings: type-level union/narrowing facts → `js_typing_contract_manifest.md`; logging
policy → `browser_observability_manifest.md`; platform versions →
`web_platform_baseline_manifest.md`.

---

## 1. The framing asymmetry (identical to Python's)

**ESTABLISHED.** JavaScript has **no checked exceptions** — a `throw` is invisible to the static
checker and absent from every signature. An in-band result *can* be a discriminated union the
checker forces callers to handle exhaustively. The whole design follows: **contract-level
outcomes are typed and in-band; genuinely exceptional ones are thrown.** Operating slogan
unchanged: **fail loud, fail typed.** Two JS-specific aggravations:
- **Anything can be thrown** (`throw 42`, `throw "oops"`) — which is why strict mode types
  `catch (e)` as `unknown` and every handler must narrow (ESTABLISHED).
- **Failure has multiple surfaces** (§10): synchronous throws, promise rejections, and
  event-handler exceptions each escape through a *different* top-level channel; "errors never
  pass silently" requires wiring all of them.

## 2. Two propagation channels

- **In-band typed value (ESTABLISHED).** `{ kind:'ok', value } | { kind:'err', error }` (or
  per-domain variants). Narrow on `kind`; after all arms, the residual type is `never`; a final
  `assertNever(x)` type-checks only when nothing remains. Adding a variant breaks every
  non-exhaustive consumer at check time — errors become a *checked* public contract. No stdlib
  `Result` exists; hand-rolled union vs a library (`neverthrow`, `true-myth`, or the TC39
  `Try`-style proposals still in committee) is **OPEN** — dependency-vs-control, same as Python.
- **Thrown exception (ESTABLISHED).** For: truly exceptional conditions, unrecoverable-at-this-
  layer failures, programmer error. Never for outcomes callers routinely branch on.

**`assertNever` (ESTABLISHED pattern).** JS ships no `assert_never`; write the four-liner:
`function assertNever(x) { throw new InvariantError(\`unreachable: ${x}\`); }` typed
`(x: never) => never` via JSDoc. Compile-time exhaustiveness, runtime backstop — same dual role
as Python's.

## 3. Error classes and hierarchy

**ESTABLISHED** (ECMA-262; MDN):
- **Root at `Error`.** Built-ins: `TypeError`, `RangeError`, `SyntaxError` (what `JSON.parse`
  throws), plus DOM's `DOMException` (with `.name` codes like `'AbortError'`,
  `'QuotaExceededError'` — the platform's own error taxonomy; branch on `.name`).
- **Subclass with `class AppError extends Error`**, set `this.name = 'AppError'` (otherwise the
  name renders as `Error`), carry **structured fields as own properties** (offending id, stable
  `code`) — string-only errors are not machine-consumable; same 5-part message anatomy as the
  Python manifest (operation context, expected vs actual, offending value, remediation hint,
  stable code) — **OPEN convention, adopt it**.
- **One package base** (`class LibError extends Error`) + narrow subclasses: callers catch the
  whole component with one `instanceof`, distinguish specifics. Reuse built-ins where the
  meaning already fits.
- **Cross-realm caveat (VERSION-DEPENDENT).** `instanceof Error` fails for errors from another
  realm (iframe, some worker paths). **`Error.isError(x)` (ES2026)** is the robust check —
  version-gate it; until then, `instanceof` plus duck-check fallback.

## 4. Chaining: `cause` — the `raise from` of JS

**ESTABLISHED (ES2022).** `new DomainError('saving profile failed', { cause: lowLevelErr })`
attaches the original as `.cause`; DevTools and modern engines render the chain ("Caused by:").
Use exactly where Python uses `raise X from Y`: wrapping a low-level error in a domain error at
an abstraction boundary, preserving the origin for tracing. There is no implicit-`__context__`
equivalent — **if you don't pass `cause`, the origin is gone (ESTABLISHED)** — so wrapping
without `cause` is the JS spelling of the `from None` anti-pattern: legitimate only with a
written justification. Re-throwing unchanged (`catch (e) { …; throw e; }`) preserves the
original stack (the bare-`raise` analogue). There is no `add_note`; attach context either by
wrapping-with-`cause` or by appending to a custom `.notes` array property (OPEN convention).

## 5. try/catch/finally discipline

**ESTABLISHED.** Catch narrowly *by re-throwing what you don't handle* — JS has no typed catch
clauses, so the idiom is: `catch (e) { if (!(e instanceof QuotaError)) throw e; …handle… }`.
Keep the protected region minimal (the tutorial-`else` rationale, achieved by scoping the `try`
tightly). `finally` for cleanup — or, once the Baseline target allows, **`using` /
`DisposableStack` (ES2026)**, the context-manager analogue, which also fixes the
multi-resource-cleanup footguns `finally` chains have. Never swallow-and-continue; explicit
narrow suppression only, with a comment (PEP-20's "unless explicitly silenced" is
language-independent).

## 6. Async failure semantics

**ESTABLISHED** (ECMA-262; WHATWG HTML):
- Inside `async` functions, `try/catch` catches awaited rejections; a rejection nobody awaits or
  `.catch`es becomes an **unhandled rejection**.
- **Fire-and-forget async calls are silent failure factories** — an un-awaited
  `void doAsyncThing()` swallows its rejection path unless it has its own `.catch`. Rule: every
  promise is awaited, returned, or explicitly `.catch`-terminated (lint rule
  `no-floating-promises` — enforce in CI).
- **Event handlers are their own failure domain:** a throw inside a DOM handler does not
  propagate to the dispatching code; it goes to the global `error` event. Handler bodies at the
  shell therefore need their own boundary (wrap, convert, log-once).
- **Async stack traces** are engine-reconstructed and lose frames across some gaps —
  another reason context is attached at boundaries via `cause` rather than read off the stack.

## 7. Aggregation

**ESTABLISHED.** `AggregateError` (ES2021) is the `ExceptionGroup` analogue: thrown natively by
`Promise.any` when all inputs reject; construct it yourself for batch validation
(`new AggregateError(errors, msg)`); `.errors` holds the members. `Promise.allSettled` is the
collect-don't-throw alternative for concurrent fan-out. Same restraint rule as PEP 654: use
selectively, at genuinely concurrent/multi-failure sites; single-error flow otherwise.

## 8. The functional-core / imperative-shell seam

**OPEN — convention; tag the exact seam in the spec** (same obligation as the Python manifest §6):
- The **pure core** returns typed results for expected domain outcomes; throws only for
  can't-happen invariants (via `invariant()`, typing manifest §6).
- The **shell** (DOM handlers, fetch client, storage adapter, app bootstrap) catches and
  converts: platform exceptions → typed results inward; typed errors → user-facing rendering +
  one log outward. Every user-visible failure has a defined rendering — a client-side app has no
  server error page to fall back on; the unhandled default is a broken widget or a blank screen.

## 9. Assertions

**ESTABLISHED facts:** JS has no `assert` statement and no `-O` stripping mode;
**`console.assert(cond, msg)` logs and continues — it never throws** and is therefore never an
enforcement mechanism. **Decision:** internal can't-happen invariants use a throwing
`invariant()` helper (raising `InvariantError extends Error`); boundary/untrusted input uses
real parsing with typed `ValidationError`s (typing manifest §5) — the parse-don't-validate
chain: parse at the shell → typed objects inward → invariants guard what the parser already
proved. If a build/minify step ever strips `invariant` calls in production, audit first — the
`-O` audit obligation, imported.

## 10. Top-level handlers: the last line

**ESTABLISHED (WHATWG HTML).** The shell wires, once, at bootstrap:
- `window.addEventListener('error', h)` — uncaught synchronous throws and handler exceptions
  (also resource-load errors in the capture phase);
- `window.addEventListener('unhandledrejection', h)` — unhandled promise rejections
  (`event.reason` carries the value; `rejectionhandled` fires for late handling);
- worker `error`/`messageerror` events per worker.
These are the *backstop*, not the strategy: their firing in development is a bug report
(a failure escaped every designed boundary). They log once (observability manifest §5) and
render the generic failure state.

## 11. Version matrix

**VERSION-DEPENDENT.**

| Feature | Edition | Notes |
|---|---|---|
| `Error` `cause` option | ES2022 | chaining primitive |
| `AggregateError`, `Promise.any` | ES2021 | grouping |
| `Promise.allSettled` | ES2020 | collect-not-throw |
| `Promise.try` | ES2025 | sync-or-async unification into the rejection channel |
| `Error.isError` | ES2026 | cross-realm check — gate on engine support |
| `using` / `DisposableStack` | ES2026 | context-manager analogue — gate on engine support |
| `unknown` in catch | tsc strict | checker, not runtime |

## 12. The fetch boundary — the highest-traffic error site

**ESTABLISHED (WHATWG Fetch) — the most-missed contract in client-side code:**
- `fetch` **rejects only on network failure / CORS block / abort**; HTTP 4xx/5xx **resolves**
  with `response.ok === false`. Not checking `ok` is swallow-and-continue by omission.
- `response.json()` throws `SyntaxError` on malformed bodies — a second, distinct failure branch.
- Aborts surface as `DOMException` with `name === 'AbortError'` — usually *not* an error to
  report (an intentional cancellation); branch on it explicitly.
**Decision-grade pattern:** one fetch-client module converts all of this into the app's typed
result union — `NetworkError | HttpError(status, body) | ParseError | Aborted | Ok(T)` — so the
distinctions cannot be lost downstream. Storage adapters do the same for
`QuotaExceededError`/absence.

## 13. Anti-patterns checklist

- Unchecked `response.ok` (§12). — Floating promises / fire-and-forget async (§6). —
  Empty `catch {}` (swallow-and-continue). — Catch-all without re-throwing the unhandled
  remainder (§5). — Wrapping without `cause` (§4). — `console.assert` as enforcement (§9). —
  Throwing non-`Error` values. — String-only errors without `name`/`code`/fields (§3). —
  Exceptions for routine contract outcomes / non-exhaustive union handling without `assertNever`
  (§2). — No global `error`/`unhandledrejection` handlers (§10). — Raising the package base
  error directly instead of a narrow subclass (§3).

## 14. Decision flowchart

```
Expected, recoverable, contract-level DOMAIN outcome the caller must branch on?
  YES → typed discriminated union; exhaustiveness via assertNever.        [§2]
  NO ↓
Truly exceptional / unrecoverable here / programmer error?
  YES → throw a narrow subclass of your AppError (Error root),
        structured fields + stable code.                                  [§3,§9]
Crossing an abstraction boundary while throwing?
  → wrap: new DomainError(msg, { cause: low }).                           [§4]
Multiple independent concurrent failures?
  → AggregateError / Promise.allSettled; use selectively.                 [§7]
Untrusted input (fetch body, storage, URL, postMessage)?
  → parse, don't validate: typed parse fn raising ValidationError —
    never console.assert, never unchecked JSON.parse.                     [§9,§12]
Always: message = context + expected/actual + offending value +
remediation + code; log ONCE at the handling boundary; wire the two
global handlers as backstop.                                              [§3,§10]
```

## Sources
- ECMA-262 (ES2022 `cause`; ES2021 `AggregateError`; ES2025 `Promise.try`; ES2026 `Error.isError`,
  explicit resource management) — https://tc39.es/ecma262/ . Accessed Jul 2026.
- MDN — `Error` (incl. `cause`, custom subclassing), `AggregateError`, `DOMException` names,
  `console.assert` (non-throwing), `try...catch` — https://developer.mozilla.org/ .
- WHATWG Fetch — rejection semantics vs HTTP status — https://fetch.spec.whatwg.org/ .
- WHATWG HTML — error handling, `unhandledrejection`/`rejectionhandled` events —
  https://html.spec.whatwg.org/ .
- Alexis King — "Parse, don't validate."
- Sibling manifests: typing (unions, narrowing, invariant()), observability (log-once),
  platform hub (edition gating).
