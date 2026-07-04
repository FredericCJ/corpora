# ARCHITECTURE.md — PHASE 4

## Constraints honored

Raw JavaScript, no framework, no bundler, no build step at *view* time; opens from `file://`.
Because `fetch()` of JSON is blocked on `file://`, both data layers ship as JS modules that
assign into a single namespace (`window.SWE`); the JSON twins exist purely as inspectable
phase artifacts. Hard separation: **data carries no behavior, logic carries no resources,
presentation carries no data.**

## File tree

```
explorer/
├─ index.html                 static shell: header, toolbar, view mount points, <script> order
├─ MODELS.md  ARCHITECTURE.md
├─ build/                     build-time parsing (Python) — the only place report text is read
│  ├─ records_{sa,arch,c,cpp,ops,sim}.py   PHASE-1 transcribed fact records (per report)
│  ├─ edges.py                             PHASE-3 typed edges with provenance
│  └─ build.py                             merge -> normalize -> emit (all data/ files)
├─ data/                      DATA (generated; no behavior)
│  ├─ corpus.js  corpus.json               fact layer  (SWE.corpus)
│  ├─ relations.js  relations.json         inference layer (SWE.relations)
│  ├─ corpus_report.md                     PHASE-1 report (counts, merges, gaps)
│  └─ adjustments.md                       PHASE-2 log (every vocabulary change)
├─ logic/                     LOGIC (runtime; no hard-coded resources)
│  ├─ util.js                 DOM helper, badge builders, year parsing, text utils
│  ├─ state.js                single state object + pub/sub + location.hash (de)serialization
│  ├─ search.js               lowercase index over title/authors/id/ident; query -> id set
│  ├─ detail.js               node detail drawer (citation, tags, memberships, edge lists)
│  ├─ views/graph.js          model 1 — reading graph (SVG, computed layout, edge catalog)
│  ├─ views/facets.js         model 2 — facet browser (chips + result list, chunked render)
│  ├─ views/timeline.js       model 3 — chronology strata
│  ├─ views/overlap.js        model 4 — overlap signatures + pair matrix
│  ├─ views/anchors.js        model 5 — per-corpus anchors
│  └─ app.js                  bootstrap: view registry, toolbar, keyboard, hash routing
└─ styles/                    PRESENTATION (no data)
   ├─ tokens.css              design tokens: palette, type stack, spacing, corpus/kind colors
   └─ app.css                 layout + component styles for all views
```

## View-switching architecture

`app.js` owns a registry `{id -> {label, mount(el, ctx), destroy()}}` populated by each view
module at load (`SWE.views.register(...)`). The toolbar tabs and keys `1..5` set
`state.view`; state emits, the shell destroys the outgoing view and mounts the incoming one
into `#view-root`. Views are pure functions of `(SWE.corpus, SWE.relations, state)` — they
never write to the data namespace. Cross-view invariants (search query, verification filter,
corpus filter, selected node) live in the shared state so switching views preserves context;
the full state round-trips through `location.hash`, so any screen is a shareable/bookmarkable
URL even on `file://`.

## Rendering strategy at scale

421 nodes / 204 edges is far past hand-layout; everything is generated:

- **Graph** — only nodes participating in edges are drawn (~170). Deterministic layout:
  corpus bands laid horizontally; inside a band, nodes sort by (theme, year) and pack into a
  grid whose column count is derived from the band's population; band x-offsets accumulate.
  SVG is built via `createElementNS` in two passes (edges under nodes). Hover/focus computes
  the cycle-safe reachability closure both directions and dims the rest; the edge *catalog*
  is DOM below the board (one `<details>` per provenance class), giving every edge its
  justification line — the reference pages' pattern, generated instead of hand-authored.
- **Lists** (facets/timeline/overlap/anchors) — chunked rendering: first 150 rows, then a
  "show N more" continuation; keeps first paint fast without a virtual-scroll dependency.
  At 10× corpus growth the same seams take over (graph band pagination + list chunking);
  nothing assumes a fixed node count.

## Shared state model

```
state = { view, q, filters: {corpus, branch, theme, type, verification, role, lane, auto},
          sel /* selected node id or null */ }
```
Single mutation entry point `state.set(patch)` → recompute derived `state.visible`
(the filtered id set, produced by logic/search.js + filter predicates) → notify subscribers.
No view mutates another view's DOM; the detail drawer subscribes to `sel` only.

## Search / filter / detail behavior

Search narrows the *current* view (dim in graph, filter in lists). Filters are global chips
in the toolbar (verification, corpus) plus per-view facet panels (facets view exposes the
full lattice). Clicking any node anywhere sets `sel`; the drawer shows the full citation
(title, authors, year of last publication, identifier), per-corpus raw tags exactly as each
report stated them, membership provenance (including "lead" memberships added by merge),
UNRESOLVED flags, and both edge directions with kind + provenance + justification.

## Accessibility & keyboard

- Toolbar tabs: `role=tablist/tab`, `aria-selected`, arrow-key traversal.
- Every node representation is focusable (`tabindex=0`); Enter/Space opens the drawer;
  Escape closes it and returns focus.
- Keys: `1..5` switch views, `/` focuses search, `v` cycles the verification filter.
- Color never carries meaning alone: verification and provenance are also text badges;
  edges are distinguished by dash pattern as well as hue. Focus states are visible;
  `prefers-reduced-motion` disables transitions.

## Honesty affordances

`verified | unverified` renders as an explicit badge on every node row/box; UNRESOLVED
fields render the literal token in the drawer and get a ⚠ mark in lists. Editorial edges
show **[EDITORIAL]** in the catalog and drawer. The About panel links the four generated
documents (corpus report, adjustments log, MODELS, this file).
