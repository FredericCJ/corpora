# ARCHITECTURE.md

## Constraints honored

Raw HTML, CSS and JavaScript. **No framework, no bundler, no build step at *view* time**; the page
opens directly from `file://`. Because `fetch()` of JSON is blocked on `file://`, the two data
layers ship as classic `<script>`s that assign into a single namespace (`window.DS`); the JSON
twins exist purely as inspectable phase artifacts. Hard separation of the three concerns:
**data carries no behavior, logic carries no resources, presentation carries no data.**

**Target device.** One 16:9 4K / 27" display, fullscreen, landscape — a *single viewport, no page
scroll*. The whole application is `100dvh`; only the inspector column scrolls internally. The graph
is an SVG whose `viewBox` scales to fit its pane, so the composition is resolution-independent
(verified filling 96%×90% of the board at 3840×2160 with no body scroll).

## File tree

```
explorer/
├─ index.html                 static shell: header/controls, graph + inspector mounts, <script> order
├─ ARCHITECTURE.md  MODELS.md  README.md
├─ package.json  tsconfig.json committed toolchain: pinned tsc (checker) + vitest/playwright/fast-check
├─ build/                     PHASE 1/3 — the ONLY place the two reports are read (Python)
│  ├─ nodes.py                transcribed node facts (citations + audit verdicts + honesty flags)
│  ├─ edges.py                typed edges + cycles, each with provenance
│  └─ build.py                merge → fail-loud validate → emit all data/ files
├─ data/                      DATA (generated; no behavior)
│  ├─ corpus.js  corpus.json          fact layer   (DS.corpus)
│  ├─ relations.js  relations.json     inference layer (DS.relations)
│  └─ corpus_report.md                 build census (counts, verification, flags)
├─ logic/                     LOGIC (runtime; no hard-coded resources)
│  ├─ log.js                  injected no-op logger seam + console router (observability manifest §4)
│  ├─ util.js                 DOM/SVG helpers, invariant(), assertNever(), presentation maps
│  ├─ parse.js                boundary parsing: unknown → typed corpus/relations, or ValidationError
│  ├─ state.js                single state object + pub/sub + location.hash (de)serialization
│  ├─ search.js               pure visible-id-set derivation (search + family + verification)
│  ├─ graph.js                FUNCTIONAL CORE — pure layout + cycle-safe closure (no DOM)
│  ├─ render.js               IMPERATIVE SHELL — SVG projection + interaction
│  ├─ detail.js               the persistent inspector dock (overview / node detail)
│  └─ app.js                  bootstrap: global handlers, parse boundary, mount, toolbar, keyboard
└─ styles/                    PRESENTATION (no data)
   ├─ tokens.css              design tokens: palette, family + relation-kind hues, type, spacing
   └─ app.css                 single-viewport layout (100dvh grid), node/edge/inspector styles
```

## The single-viewport layout engine

Hand layout of 110 nodes / 121 edges is impossible; everything is generated. `graph.js`
(`computeLayout`) is a **pure function** of `(nodes, edges, familyOrder, {aspect})`:

1. group the drawn nodes into **family bands**; within a band sort by `(tier, year)` so roots lead;
2. size each band's grid (`ncols ≈ √(count·1.25)`, clamped 2–6);
3. **shelf-pack** the bands left→right, wrapping to a new shelf past a target width;
4. sweep ~28 candidate target widths and keep the packing whose aspect best matches the pane's —
   so the board fills with minimal letterboxing at whatever the actual pane aspect is.

`render.js` (the shell) projects that geometry to SVG via `createElementNS`, draws edges under
nodes, and lets `preserveAspectRatio="xMidYMid meet"` scale the whole board to the pane. On pane
resize a `ResizeObserver` re-runs the pure layout (aspect changes) and re-projects — no timers.

## Shared state model

```
state = { q, family, ver, kind, sel }
```

One mutation entry point `state.set(patch)` → writes `location.hash` → notifies subscribers.
Unidirectional flow: **event → set → notify → render**. The DOM is a *projection*; state is never
read back out of it. Full state round-trips through the hash, so any screen (a filter, a selected
node) is a shareable URL even on `file://`. Search/family/verification narrow which nodes are "on"
(the graph dims the rest — it never relays out); the relation-kind filter dims edges.

## Manifest compliance map

| Manifest principle | Where honored |
|---|---|
| Functional core / imperative shell | `graph.js` (pure layout + closure) vs `render.js` (SVG + events) |
| State in JS, DOM is a projection; never read state from the DOM | `state.js`; renderer subscribes and re-projects |
| Parse, don't validate — parse once at every inward boundary | `parse.js` turns the data modules into typed values or throws `ValidationError`; the build re-checks endpoints |
| `console.assert` never enforces — use an explicit throw | `util.invariant()` / `InvariantError`; exhaustiveness via `assertNever` |
| No browser logging architecture — inject a logger, default no-op | `log.js` (`NOOP` + `consoleLogger`); components take `log`, never call `console.*` |
| Errors never pass silently — wire the two global backstops | `app.js` `window` `error` + `unhandledrejection`; bootstrap `try/catch` renders a load-error state |
| Use the platform before writing JS | native `<svg>`, `ResizeObserver`, `URLSearchParams`, `<details>`-free single-viewport chrome; no overlay-JS libraries |
| Strict typing of raw JS via tsc + JSDoc | `tsconfig.json` (strict family, `checkJs`) + JSDoc typedefs (`DSNode`, `DSEdge`, `Corpus`, `State`, `Logger`, …) |
| Accessibility is first-class | nodes are `role=button tabindex=0` with `aria-label`; Enter/Space inspect; `/` search, `Esc` clear; color never sole channel (dashes + ★/⚠ + text badges); `prefers-reduced-motion` disables transitions |
| Record the architectural decisions | below |

## Architectural decisions (recorded, per the spec manifest)

- **Baseline target: Widely available as of 2026-07.** Everything used (ES modules-free classic
  scripts, `<svg>`, `ResizeObserver`, `URLSearchParams`, CSS grid / custom properties / `dvh`) is
  Widely available. Language floor ES2022. No ES2026 feature is relied on.
- **No build step at view time** (tradeoff: more requests, no minification) — legitimate at this
  scale; the Python `build/` step is offline data generation only, never shipped.
- **Classic scripts + `window.DS`, not ES modules** — chosen because native `import` from `file://`
  is CORS-blocked in browsers; this is the `file://`-safe form of modularity. Load order is fixed
  in `index.html`.
- **Telemetry: none.** The honest default under an "API calls only where unavoidable" posture
  (observability manifest §6). Operational visibility is the structured console sink only.
- **Injected-logger seam vs log-events** — chose the injected logger (§4 pick-one).

## Honesty affordances

`verified | flagged` renders as a badge on every node and a dashed border in the graph; the
specific flag (folklore / theory-only / diffuse-origin / uncited-in-source / ambiguous) renders in
the inspector. Editorial edges show **[EDITORIAL]** and dotted lines; derived edges quote their
basis. The audit's `CONFIRM/FIX/ENUMERATE` verdict rides on each of the 17 roots. Nothing is
invented to fill a gap — a missing citation is surfaced, never smoothed over.
