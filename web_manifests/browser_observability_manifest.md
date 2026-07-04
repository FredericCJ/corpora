# Logging & Observability — Ground-Truth Manifest (Browser-Native Applications)

**Purpose.** Citable ground truth for designing LOGGING and OBSERVABILITY into small-scale,
strictly-checked, **reuse-first** browser-native applications. Same three goals as the Python
sibling: **goal1** — debugging aid for contributors and downstream reusers; **goal2** —
monitoring the software in action; **goal3** — per-component reusability, so a component drops
into a consuming application without dragging logging policy with it. GROUNDING, not a rulebook.
Tags: **ESTABLISHED**, **VERSION-DEPENDENT**, **OPEN**. Error-side propagation contract lives in
`js_error_tracing_contract_manifest.md`; this file owns routing, formatting, and transport.

---

## 1. The structural fact everything follows from

**ESTABLISHED — the browser has no logging architecture.** There is no logger hierarchy, no
handlers, no formatters, no filters, no propagation, no `getLogger(__name__)`, no `NullHandler`.
There is one global `console` shared by the application, every library, and every browser
extension, writing to a developer-only surface. **Consequently, the Python manifest's goal3
mechanism does not translate — but its goal does.** "Components emit richly and configure
nothing; applications configure once and own all routing" must be *built* as an explicit seam
(§4) rather than inherited from a stdlib.

A second structural fact shapes goal2: **the program runs on machines you do not operate.**
Console output is visible only in the end user's DevTools; *you* never see it. Operational
monitoring therefore requires an explicit transport of selected events back to an endpoint you
own (§6) — which collides with this project's "API calls only where unavoidable" stance and is
an architectural decision, not a default (OPEN).

## 2. The console API: severity semantics

**ESTABLISHED (WHATWG Console Standard; MDN):**

| Method | Semantics (adopted mapping) | DevTools behavior |
|---|---|---|
| `console.error` | operation failed; a function could not be performed | Error level; stack in most browsers |
| `console.warn` | unexpected but still working; not the caller's bug to fix | Warning level |
| `console.info` / `console.log` | confirmation of normal operation | Info level (`info`/`log` are near-synonyms across engines) |
| `console.debug` | developer diagnostics | **Verbose level — hidden by default in Chrome DevTools** |

The mapping of *meaning* onto these methods is convention (the Console Standard specifies
behavior, not usage doctrine) — adopt the Python severity semantics verbatim as **OPEN/convention**:
error ≈ ERROR, warn ≈ WARNING, info/log ≈ INFO, debug ≈ DEBUG. There is no CRITICAL tier; a
would-be-critical failure is `error` + the app's failure rendering.

**Supporting facts (ESTABLISHED):** `console` takes multiple arguments and **live object
references** (objects are inspected lazily — log a *snapshot* (`structuredClone` or spread) when
logging mutable state, or the inspected value can show post-mutation state);
`console.group`/`table`/`count`/`time` exist for interactive debugging; `console.assert(cond, …)`
logs-if-false and **never throws** (error manifest §9). There is no lazy `%`-args
performance idiom worth importing: the cost concern instead is *argument construction* — gate
expensive debug payloads behind the logger's own level check (§4).

**`print()` analogue:** a client-side app's "ordinary user-facing output" is the **DOM**, not the
console. Anything a user should see is rendered; the console is never a user channel.

## 3. What replaces `warnings.warn`

**OPEN/convention.** Python's caller-should-fix-their-usage channel has no browser stdlib
equivalent. For a reusable component, misuse by the consuming developer is signaled by:
**throwing a typed error** for contract violations (preferred — it is checkable and loud), or a
one-time `console.warn` for deprecations/soft misuse (guard with a "warn once" set). Never
silently tolerate contract misuse (PEP-20 doctrine, imported).

## 4. The reusable-component discipline (goal3 — the load-bearing part)

The `NullHandler` rules translate as follows (**OPEN — designed convention, since no stdlib
mandates it; the *direction* is inherited from the official Python library guidance**):

- **A reusable component never calls `console.*` directly.** The console is the browser's root
  logger; writing to it from library code is exactly the "logging to the root logger" violation —
  it gives the consuming application no way to route, silence, or level-filter the component.
- **Components accept an injected logger** at their contract: a minimal structural interface
  `{ debug(msg, data?), info(msg, data?), warn(msg, data?), error(msg, data?) }` (typed as a
  JSDoc typedef — the `Protocol` analogue), taken as a constructor/factory parameter or a
  custom-element property.
- **The default is a no-op logger** — the `NullHandler` analogue: a frozen object of empty
  functions. A component with no logger injected is **silent**, not chatty.
- **Alternative/complement — emit events:** a component may dispatch a non-bubbling
  `CustomEvent('componentname:log', { detail })` and let the application decide; this keeps even
  the logger dependency out of the contract. Pick one mechanism per project (OPEN).
- **No logging side effects at import.** A module may create its no-op default at import;
  it must not write to the console, install global handlers, or monkey-patch `console` at import.
- **Level semantics at seams (goal1):** `info` when a component begins/ends a meaningful unit of
  work or crosses its public boundary; `debug` for internal decisions/inputs/branch points —
  identical mapping to the Python manifest.

**Best-effort, not absolute (inherited caveat):** nothing stops a component from calling
`console.log`; the discipline is review-enforced (a lint rule banning `console` outside the
designated app modules is the cheap mechanization — OPEN, adopt it).

## 5. Application-side configuration (the consumer)

The application owns policy, configured **once at bootstrap** (the `dictConfig` analogue is a
small hand-rolled router — OPEN design, ~30 lines):
- One **app logger factory** produces named child loggers (`makeLogger('billing')`) so origin is
  obvious from a name field — recovering the `getLogger(__name__)` property by construction.
- **Level threshold** held by the router; per-sink levels for fan-out: console sink at
  `debug`/`info` during development, a buffer/transport sink (§6) at `warn`+ in production.
  Default production threshold decision mirrors Python's WARNING default (OPEN — pin it).
- The router is also where **structured shape** is enforced: every entry
  `{ ts, level, logger, msg, data?, correlationId? }` — structured objects, not interpolated
  strings, so sinks can serialize (JSON) or render.
- **Log-once discipline:** exceptions are logged exactly once, at the handling boundary, with
  the full `cause` chain — the global `error`/`unhandledrejection` backstops (error manifest §10)
  log-and-render; interior layers propagate, never re-log.

## 6. Operational telemetry (goal2) — an explicit decision

**Mechanisms (ESTABLISHED):**
- **`navigator.sendBeacon(url, data)`** — small, reliable, non-blocking POST that survives page
  unload; the canonical error/metric egress. Pair with buffering + `visibilitychange` flush.
- **Global handlers** (`error`, `unhandledrejection`) as the crash-report source.
- **Performance API** — `performance.mark`/`measure`, `PerformanceObserver` (long tasks,
  layout shifts, event timing) for Core-Web-Vitals-style field data.
- **Reporting API** (`ReportingObserver`; CSP/deprecation reports) — VERSION-DEPENDENT
  coverage; check Baseline per report type.
**Decision (OPEN).** For this project's "API calls only where unavoidable" posture, the honest
default is **no telemetry endpoint**: goal2 is served by the structured console sink plus the
user's ability to copy diagnostics. If operational monitoring is genuinely required, the beacon
endpoint is an *unavoidable* API and enters the spec as one — with a documented payload schema,
sampling policy, and the §7 privacy gate. Third-party error services (Sentry-class) are the
buy-option; record the dependency tradeoff.

## 7. Security & privacy: stricter than the server-side rule

**OPEN/best-practice (OWASP-cited, as in the Python manifest) — with two browser amplifiers
(ESTABLISHED facts):** (1) console output is readable by anyone at the user's machine *and by
browser extensions*; (2) any telemetry beacon ships user data off-device, engaging GDPR-class
consent obligations. Rules: never log credentials, tokens, or PII in messages or `data`;
redact centrally in the router (the Filter-analogue seam — one place, not per call site);
telemetry payloads carry error name/code/message/stack and app state *identifiers*, never
content; correlation IDs are random per-session (`crypto.randomUUID()`), never derived from user
identity.

## 8. Correlation

**ESTABLISHED mechanics, OPEN policy.** Single page, single thread: a module-level
`sessionId = crypto.randomUUID()` plus a per-user-action `actionId` stamped by the router covers
the "stitch one logical operation across components" need — `contextvars` machinery is
unnecessary at this scale. Propagate the id outward on unavoidable API calls via a header if the
server participates; adopt W3C Trace Context (`traceparent`) **only if** the backend is actually
distributed — the do-not-adopt-OTel-for-a-single-process rule, imported unchanged.

## 9. Checklists

**Component author:** no direct `console.*`; accept injected logger (or emit log events);
no-op default; no import-time side effects; `info` at boundaries, `debug` at decisions; throw
for caller misuse; log nothing secret; log snapshots, not live mutable objects.

**Application author:** build/adopt the ~30-line router once at bootstrap; named child loggers;
structured entries; per-sink levels; wire the two global handlers to log-once + render; central
redaction; decide the telemetry question explicitly (default: none); lint-ban stray `console`
calls; pin the production threshold.

## Open questions
1. Injected logger vs log-events (or both) as the component seam — pin one (§4).
2. Production console threshold and whether a production build strips `debug` calls (§5).
3. Telemetry endpoint: none / own beacon / third-party service — with payload schema and consent
   posture if adopted (§6, §7).
4. Redaction allow/deny field lists (§7).
5. Lint mechanization of the no-`console`-in-components rule (§4).

## Sources
- WHATWG Console Standard — https://console.spec.whatwg.org/ . Accessed Jul 2026.
- MDN — `console` (levels; `debug`→Verbose visibility), `navigator.sendBeacon`, Performance API
  / `PerformanceObserver`, `ReportingObserver`, `crypto.randomUUID` —
  https://developer.mozilla.org/ .
- W3C — Trace Context — https://www.w3.org/TR/trace-context/ .
- OWASP — Logging Cheat Sheet (secrets/PII) —
  https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html .
- Python `logging` HOWTO — cited as the *source of the translated discipline* (library/app
  split), not as a browser authority — https://docs.python.org/3/howto/logging.html .
