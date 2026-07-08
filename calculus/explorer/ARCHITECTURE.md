# ARCHITECTURE.md — single-viewport curriculum explorer

## What this is

`calc-analysis.md` (repo root) is a research report: a book-anchored curriculum from intermediate
algebra to research-level analysis, stated as a 26-node DAG with evidence-tagged edges, a tier
scheme, parallel sets, a recommended lineage, and a quality-gate ledger. This app makes that report
**navigable** without changing a word of its claims. It follows the `SWE/explorer` rebuild's
architecture and the `web_manifests/` principles (functional core / imperative shell,
injected-logger seam, parse-at-boundary, single-source state, global failure backstops,
strict-JSDoc typing) for **one 16:9 4K / 27" fullscreen viewport with no page scroll**.

## Constraints honored

Raw HTML/CSS/JS. **No framework, no bundler, no build step at *view* time**; opens from `file://`.
Because `fetch()` of JSON is blocked on `file://`, the data ships as classic `<script>`s assigning
into `window.CALC`; the JSON twins are inspectable phase artifacts. Hard separation:
**data carries no behavior, logic carries no resources, presentation carries no data.**

**Single viewport.** The whole app is `100dvh`, `overflow:hidden`. The stage is a two-column grid —
the active model on the left, a **persistent inspector dock** on the right. Every model fits its
pane: the DAG SVG scales via `viewBox`; the tier/lineage/parallel/gate panes use internal scroll
regions. Verified over HTTP at 1600×900: `body.scrollHeight === innerHeight`, all five models
rendering, zero console errors.

## File tree

```
explorer/
├─ index.html                 shell: header + model tabs, view mount, inspector dock, <script> order
├─ ARCHITECTURE.md  MODELS.md  README.md
├─ package.json  tsconfig.json committed checker (tsc) + test (vitest/playwright/fast-check) toolchain
├─ build/                     PHASE 1–4 (Python) — the only place the report text is read
│  ├─ nodes.py                fact records: tier scheme, 27 node rows, bibliography, TL;DR
│  ├─ edges.py                inference records: 46 edges, DOT cross-check set, parallel sets,
│  │                          lineages, gate ledger, register, caveats, view definitions
│  └─ build.py                validation gauntlet + emission (see "The build is the verifier")
├─ data/                      DATA (generated; no behavior)
│  ├─ corpus.js  corpus.json            fact layer   (CALC.corpus)
│  ├─ relations.js  relations.json      inference layer (CALC.relations: edges + editorial spine)
│  └─ corpus_report.md                  the build's structural-verification log
├─ logic/                     LOGIC (runtime; no hard-coded resources)
│  ├─ log.js                  injected no-op logger seam + console router (observability §4)
│  ├─ util.js                 DOM/SVG helpers, invariant(), tier/evidence presentation maps
│  ├─ parse.js                boundary parse: unknown → typed corpus/relations, or ValidationError
│  ├─ state.js                single state + pub/sub + location.hash (view,q,rigor,tier,sel)
│  ├─ core.js                 FUNCTIONAL CORE — layout, closure, path DP, buckets, stats
│  ├─ inspector.js            persistent dock (model-aware overview / node detail) [shell]
│  ├─ views/graph.js          Model 1 — tier-layered prerequisite DAG [shell]
│  ├─ views/tiers.js          Model 2 — tier ladder [shell]
│  ├─ views/lineage.js        Model 3 — lineages + path finder [shell]
│  ├─ views/parallel.js       Model 4 — parallel sets + shared-edge audit [shell]
│  ├─ views/gate.js           Model 5 — quality gate / register / caveats [shell]
│  └─ app.js                  bootstrap: global handlers, parse, registry, toolbar, keyboard
└─ styles/                    PRESENTATION (no data)
   ├─ tokens.css              palette (9 tier hues, 2 evidence hues), type, spacing
   └─ app.css                 single-viewport layout + per-view internal layouts
```

## The build is the verifier

The report *claims* its graph is a DAG and tier-monotone; `build/build.py` **checks** rather than
trusts: Kahn topological sort over the 26 kept nodes (fails the build on any cycle), tier
monotonicity per edge (the two legal within-tier edges are enumerated), set-equality of the §3
edge table against an independent transcription of the §6 DOT rendering, lineage hops resolving to
actual edges, quality-gate ledger covering every node exactly once with statuses agreeing with the
catalogue, and a shared-vs-partial audit of each parallel set's neighborhoods. The full proof log
ships as `data/corpus_report.md` and is linked from the inspector. Discrepancies found are
**carried, not smoothed** — e.g. PS-2's stated shared N09 edge is drawn only from N05, and the
views say so.

## Functional core / imperative shell

`core.js` is a **pure** function library — the whole model computation surface with no DOM:
`visibleIds` (search + rigor + tier), `dagLayout` (tier-layered bands with barycenter ordering and
parallel-set contiguity), `closure` (reachability), `pathsBetween` (exact count by memoised DP over
the DAG + enumeration with a **stated** cap), `tierBuckets`, `stats`. Every view under `views/` is
a thin **shell**: it calls the core, projects the result to DOM/SVG, and wires interaction.

## The layout engine (DAG)

`core.dagLayout(nodes, edges, tiers, psets)` is pure: tiers become horizontal bands top→bottom
(the curriculum descends into depth); within a band, node order comes from three barycenter sweeps
(down, up, down) with parallel-set members kept contiguous via group-averaged sort keys so their
dashed enclosure can be drawn around an unbroken run. The natural size (~1428×1122, aspect ≈ 1.27)
is close to the pane's, so the SVG scales via `preserveAspectRatio="xMidYMid meet"` with modest
letterboxing — and because the layout is size-independent, it is **built once**: no
ResizeObserver, no relayout on resize (a deliberate simplification relative to `SWE/explorer`,
whose corpus-band packing was aspect-driven). Long edges (tier span ≥ 2) get a small deterministic
horizontal bow, indexed by edge position — no randomness anywhere.

## State & view lifecycle

```
state = { view, q, rigor, tier, sel }   // one mutation entry point; round-trips through location.hash
```

Unidirectional: **event → set → notify → render**. `app.js` holds one subscription and dispatches:
`view` change tears down the current view and mounts the next; `q/rigor/tier` call the view's
`applyFilters()`; `sel` calls its `onSelect()`. The inspector is a separate persistent shell with
its own `sel`/`view` subscription. The DOM is a projection — state is never read back out of it.

## Manifest compliance map

| Principle | Where |
|---|---|
| Functional core / imperative shell | `core.js` (pure) vs `views/*` + `inspector.js` (shell) |
| State in JS; DOM is a projection; never read state from the DOM | `state.js`; views re-project on notify |
| Parse, don't validate at every inward boundary | `parse.js` → typed corpus/relations or `ValidationError`; build re-checks structure |
| `console.assert` never enforces — explicit throw | `util.invariant()` / `assertNever` |
| No browser logging architecture — inject a logger, default no-op | `log.js`; views take `log`, never call `console.*` |
| Errors never pass silently — two global backstops | `app.js` `window` `error` + `unhandledrejection`; bootstrap `try/catch` renders a load-error state |
| No silent caps | the path finder states its enumeration cap and the exact DP count |
| Use the platform before writing JS | native `<svg>`, `URLSearchParams`, CSS grid / `dvh` |
| Strict typing of raw JS via tsc + JSDoc | `tsconfig.json` (strict `checkJs`) + JSDoc typedefs |
| Accessibility first-class | tablist with arrow-key traversal + `aria-selected`; nodes/chips `role=button tabindex=0`; `1–5 / r t Esc` keys; colour never sole channel (evidence also dashes, tiers also numbered, flags also symbols) |

## Architectural decisions (recorded)

- **Baseline target: Widely available as of 2026-07.** Language floor ES2022; nothing newer relied on.
- **No build step at view time** — the Python `build/` is offline data generation + verification only.
- **Classic scripts + `window.CALC`, not ES modules** — native `import` from `file://` is
  CORS-blocked; this is the `file://`-safe form of modularity, load order fixed in `index.html`.
- **Tier-layered top→bottom layout, built once** — the graph's shape is data-determined (nine
  fixed bands), unlike SWE's aspect-swept shelf packing; a resize only rescales the viewBox.
- **The dropped node ships** — N18 renders as an edge-less ghost in its tier; hiding it would
  misstate the report, which catalogued and verified it before dropping it.
- **Five models, one at a time in the stage; persistent inspector** — the report's §7 lineage
  prose, §5 ledger, and §8/caveat registers are first-class views, not footnotes.
- **Telemetry: none** (observability §6 honest default).

## Honesty affordances

Evidence tags ride every edge (solid `EVIDENCED` vs dashed amber `JUDGMENT`) in the graph, the
finder's hop arrows, and the inspector's seam rows. The ghost node wears `✕ dropped`; its
inspector detail leads with the gate's one-line reason. Parallel-set cards print the **computed**
shared/partial neighborhoods next to the stated claim. The finder never truncates silently. The
caveats are a view of their own, and the build's verification log is linked from the inspector
overview. Nothing is smoothed over.
