# ARCHITECTURE.md — single-viewport rebuild

## What changed and why

The original explorer was a **scrolling, multi-page** app: each of the five models mounted into a
tall `<main>`, the graph board scrolled horizontally, the edge catalog lived below it, and detail
opened in an overlay drawer. This rebuild re-architects it for **one 16:9 4K / 27" fullscreen
viewport with no page scroll**, and brings the code into line with the `web_manifests` principles
(functional core / imperative shell, injected-logger seam, parse-at-boundary, single-source state,
global failure backstops, strict-JSDoc typing). The **data layer and Python `build/` are
unchanged** — 421 hand-transcribed resources and 204 provenance-tagged edges are the substance and
were kept verbatim; only the presentation and logic layers were rewritten.

## Constraints honored

Raw HTML/CSS/JS. **No framework, no bundler, no build step at *view* time**; opens from `file://`.
Because `fetch()` of JSON is blocked on `file://`, the data ships as classic `<script>`s assigning
into `window.SWE`; the JSON twins are inspectable phase artifacts. Hard separation:
**data carries no behavior, logic carries no resources, presentation carries no data.**

**Single viewport.** The whole app is `100dvh`, `overflow:hidden`. The stage is a two-column grid —
the active model on the left, a **persistent inspector dock** on the right. Every model fits its
pane: the graph SVG scales via `viewBox`; the facet/timeline/overlap/anchor panes use internal
scroll regions (the manifest's "wide/tall content scrolls inside its own container"). Verified at
3840×2160: header 96px, graph fills 95%×90% of its pane, `body.scrollHeight === innerHeight`.

## File tree

```
explorer/
├─ index.html                 shell: header + model tabs, view mount, inspector dock, <script> order
├─ ARCHITECTURE.md  MODELS.md  README.md
├─ package.json  tsconfig.json committed checker (tsc) + test (vitest/playwright/fast-check) toolchain
├─ build/                     PHASE 1–4 (Python) — the only place report text is read (UNCHANGED)
├─ data/                      DATA (generated; no behavior — UNCHANGED)
│  ├─ corpus.js  corpus.json            fact layer   (SWE.corpus)
│  ├─ relations.js  relations.json      inference layer (SWE.relations: edges + view defs)
│  ├─ corpus_report.md  adjustments.md  phase-1/2 logs
├─ logic/                     LOGIC (runtime; no hard-coded resources) — REWRITTEN
│  ├─ log.js                  injected no-op logger seam + console router (observability §4)
│  ├─ util.js                 DOM/SVG helpers, invariant(), assertNever(), corpus/kind maps
│  ├─ parse.js                boundary parse: unknown → typed corpus/relations, or ValidationError
│  ├─ state.js                single state + pub/sub + location.hash (view,q,ver,corpus,sel)
│  ├─ core.js                 FUNCTIONAL CORE — all five models' pure computations + closure
│  ├─ inspector.js            persistent dock (model-aware overview / node detail) [shell]
│  ├─ views/graph.js          Model 1 — SVG reading graph [shell]
│  ├─ views/facets.js         Model 2 — facet rail + result list [shell]
│  ├─ views/timeline.js       Model 3 — chronology columns [shell]
│  ├─ views/overlap.js        Model 4 — pairwise matrix + signature groups [shell]
│  ├─ views/anchors.js        Model 5 — per-corpus anchor columns [shell]
│  └─ app.js                  bootstrap: global handlers, parse, registry, toolbar, keyboard
└─ styles/                    PRESENTATION (no data) — REWRITTEN
   ├─ tokens.css              palette (6 corpus hues, 12 edge-kind hues), type, spacing
   └─ app.css                 single-viewport layout + per-view internal layouts
```

## Functional core / imperative shell

`core.js` is a **pure** function library — the whole model computation surface with no DOM:
`visibleIds` (search + verification + corpus), `graphLayout` (aspect-fitted shelf-packing of
corpus bands) + `closure` (cycle-safe reachability), `facetCount`, `strataBuckets`, `overlapPairs`
/ `signatureGroups`, `anchorsFor`. Every view under `views/` is a thin **shell**: it calls the
core, projects the result to DOM/SVG, and wires interaction. This is the unit-testable split the
manifest asks for — the core runs in any JS runtime; the shells own the side effects.

## The single-viewport layout engine (graph)

Hand layout of ~200 connected nodes / 204 edges is impossible. `core.graphLayout(nodes, edges,
corpusOrder, {aspect})` is pure: it groups drawn nodes into corpus bands, sizes each band's grid,
**shelf-packs** the bands, and sweeps ~28 target widths to pick the packing whose aspect best
matches the pane — so the SVG fills with minimal letterboxing. `views/graph.js` projects it and
lets `preserveAspectRatio="xMidYMid meet"` scale the board; a `ResizeObserver` re-runs the pure
layout on pane resize (coalesced through `requestAnimationFrame`, no timers).

## State & view lifecycle

```
state = { view, q, ver, corpus, sel }   // one mutation entry point; round-trips through location.hash
```

Unidirectional: **event → set → notify → render**. `app.js` holds one subscription and dispatches:
`view` change tears down the current view (`destroy()` — e.g. disconnecting the graph's
ResizeObserver) and mounts the next; `q/ver/corpus` call the view's `applyFilters()`; `sel` calls
its `onSelect()`. The inspector is a separate persistent shell with its own `sel`/`view`
subscription. The DOM is a projection — state is never read back out of it.

## Manifest compliance map

| Principle | Where |
|---|---|
| Functional core / imperative shell | `core.js` (pure) vs `views/*` + `inspector.js` (shell) |
| State in JS; DOM is a projection; never read state from the DOM | `state.js`; views re-project on notify |
| Parse, don't validate at every inward boundary | `parse.js` → typed corpus/relations or `ValidationError`; build re-checks endpoints |
| `console.assert` never enforces — explicit throw | `util.invariant()` / `assertNever` |
| No browser logging architecture — inject a logger, default no-op | `log.js`; views take `log`, never call `console.*` |
| Errors never pass silently — two global backstops | `app.js` `window` `error` + `unhandledrejection`; bootstrap `try/catch` renders a load-error state |
| Use the platform before writing JS | native `<svg>`, `ResizeObserver`, `URLSearchParams`, CSS grid / `dvh` |
| Strict typing of raw JS via tsc + JSDoc | `tsconfig.json` (strict `checkJs`) + JSDoc typedefs |
| Accessibility first-class | tablist with arrow-key traversal + `aria-selected`; nodes/rows `role=button tabindex=0`; `1–5 / v Esc` keys; colour never sole channel (dash patterns, ★/badges); `prefers-reduced-motion` |

## Architectural decisions (recorded)

- **Baseline target: Widely available as of 2026-07.** Language floor ES2022; nothing newer relied on.
- **No build step at view time** — the Python `build/` is offline data generation only.
- **Classic scripts + `window.SWE`, not ES modules** — native `import` from `file://` is CORS-blocked; this is the `file://`-safe form of modularity, load order fixed in `index.html`.
- **Five models, one at a time in the stage; persistent inspector** — the single-viewport form of the original's tabbed views + overlay drawer. The per-provenance edge catalog that used to sit below the board is now reachable per-node in the inspector (every edge is visible via its endpoints), and the global edge-kind legend lives in the inspector overview.
- **Telemetry: none** (observability §6 honest default).

## Honesty affordances

`verified | unverified` is a badge on every resource and a dashed border in the graph; UNRESOLVED
fields render the literal token; editorial edges show **EDITORIAL** and dotted lines; the audit's
provenance (`report·swa / report·sim / derived / editorial`) rides on every edge. `lead`
memberships (added by merge) are marked on the corpus chip. Nothing is smoothed over.
