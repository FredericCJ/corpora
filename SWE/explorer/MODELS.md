# MODELS.md — the relational models (INFERENCE layer)

**Nine** navigation semantics over **two** fact layers: five **work models** over the seven-pass
work corpus (`data/corpus.json`), and four **element views** over the two-realm element layer
(`data/elements.json` — 709 design + 374 architecture elements wired by 1132 typed bridge edges).
Everything here is computed **on top of** the asserted facts, and every typed edge carries a
provenance tag. The work models are unchanged from the original design — the single-viewport rebuild
changed how each is *rendered* (noted per model), not what it *means*. Pure computations live in
`logic/core.js` (work models) and `logic/core_elements.js` (element views); the view shells only
project them.

Corpora unified (superseding directive: everything in `E:\dev\corpora\SWE`):

| key | report |
|---|---|
| swa-science | Software Architecture as a Science (typed reading-graph corpus) |
| emb-arch | Architecture and Design of Embedded Software |
| emb-c | Design of Embedded Software Written in C |
| emb-cpp | Design of Embedded Software Written in C++ |
| emb-ops | Operational Use of C and C++ in Embedded Contexts |
| simulink | Architecture, Design & Management of Large Simulink/MATLAB Projects |
| swe-process | Engineering Process & Workflow: standards, documentation, versioning, review, delivery, project organization |

## Edge provenance discipline (anti-fabrication)

- `report:swa` — an entry of the swa-science report's numbered Typed Edge List (edge number in the note).
- `report:sim` — an entry of the simulink report's DAG (directed detail → abstraction ⇒ `prerequisite-of`).
- `report:proc` — a relation stated in the swe-process (pass 7) report (branching critiques, CI/CD evaluation, modularity prerequisites, framework surveys).
- `derived` — mechanically derivable from an explicit report sentence (the quoted basis is in the note).
- `editorial` — my reasoned judgment, never presented as report fact; rendered **EDITORIAL** with a distinct dotted edge in the graph.

Census: 261 edges = 86 `report:swa` + 57 `report:sim` + 50 `derived` + 19 `editorial` +
49 `report:proc`. Kind vocabulary (12, unchanged): `prerequisite-of, refines, formalizes, surveys,
applies-method-of, companion, subsumes, evaluates, critiques, supersedes, part-of, references`.

## Model 1 — Reading graph (`graph`)

- **Semantic.** Typed, directed, *cyclic-capable* relations between works.
- **Question.** "What should I read before / after / alongside this work, and why?"
- **Computation (`core.graphLayout` + `closure`).** Node set = every work with ≥1 edge; corpus
  bands are **shelf-packed to fit the pane's aspect** (was: laid out horizontally with a scroll);
  within a band, nodes sort by (theme, year). Hover traces the cycle-safe closure both directions.
- **Single-viewport rendering.** SVG scales to fill; the per-edge catalog that used to sit below
  the board is now per-node in the inspector, and the four documented cycles (C1–C4) are tagged on
  their edges and explained in the inspector overview.

## Model 2 — Facet browser (`facets`)

- **Semantic.** Classification lattice: corpus × branch × theme × type (+ verification, role, ops
  lane, emb-arch scope).
- **Question.** "What exists about X — and how much of it is verified?"
- **Computation (`core.facetCount` / `passLocal`).** Pure filtering/counting over node tags; facet
  values a source never asserts are simply absent (not UNRESOLVED); UNRESOLVED appears only where a
  report flags a value unknown.
- **Rendering.** A facet rail (live counts, click to narrow) above an internally-scrolling,
  two-column result list.

## Model 3 — Chronology (`timeline`)

- **Semantic.** Ordering by *year of last publication*, with living/continuously-revised documents
  as their own stratum — a real feature of this corpus, not a defect.
- **Question.** "How did this literature accumulate; what is maintained vs frozen?"
- **Computation (`core.strataBuckets`).** Leading 4-digit year → strata ≤1979, 1980s … 2020s,
  LIVING, UNRESOLVED (unparseable years land in UNRESOLVED — no interpolation).
- **Rendering.** One column per stratum, filling the pane; each column scrolls internally.

## Model 4 — Cross-corpus overlap (`overlap`)

- **Semantic.** The graft points: works claimed by ≥2 research passes (the property unique to a
  *unified* corpus). The reports required overlap to be preserved and tagged, not dropped.
- **Question.** "Which works bind the passes together; where do the corpora agree?"
- **Computation (`core.overlapPairs` / `signatureGroups`).** Nodes with |corpora| ≥ 2, grouped by
  exact membership signature, plus a pairwise corpus × corpus count matrix. `lead` memberships
  (a work another report verified) are marked on the chip.
- **Rendering.** The matrix (hot cells ≥ 4) beside internally-scrolling signature groups.

## Model 5 — Anchors & spine (`anchors`)

- **Semantic.** Curated per-corpus entry points — the union of the reports' own emphasis marks
  (swa ★ anchors, Simulink TARGET, ops KEY / ABSOLUTELY KEY). Carried fact, not our ranking.
- **Question.** "Where do I start in each corpus?"
- **Computation (`core.anchorsFor`).** `role` contains `anchor`, non-lead in that corpus. Corpora
  whose reports assert no anchor facet say so explicitly in-column rather than being silently absent.
- **Rendering.** One column per corpus, filling the pane; each column scrolls internally.

## Cross-cutting lenses (not separate models)

- **Verification** — `verified | unverified`, filterable everywhere, always a visible badge.
- **Search** — substring over title/authors/id/ident, applied within whichever model is active.
- **Corpus filter** — narrows every model to one pass.

## The element layer — two realms and the bridge (views 6–9)

A distinct node kind added by the ELEMENT-layer mission: the *concepts themselves*, in two realms —
**design** (implementation-level mechanisms, below software architecture and above raw syntax) and
**architecture** (styles, tactics, patterns, connectors, deployment/reference structures, description
constructs). The realms are wired by a typed, provenance-tagged **bridge** (`realizes`, `enables`,
`constrains` cross-realm; `implements`, `specializes`, `composes-with`, `alternative-to`). Pure
computations live in `logic/core_elements.js` (`SWE.coreEl`). Page/inner scroll is authorized for
these four views (element-scale navigability); the five work models keep the strict single-viewport
form.

### View 6 — Element taxonomy (`el-taxonomy`)
- **Semantic.** The realm × kind × tag lattice over both element catalogs, with live counts.
- **Question.** "What implementation- and architecture-level vocabulary exists, and how is it distributed?"
- **Computation (`core.facetCount` over element nodes).** Pure filtering/counting over element tags
  (realm, kind, confidence, quality-attribute, tag); honours the global search. Every element is
  reachable here and through search.

### View 7 — Design↔Architecture bridge (`el-bridge`)
- **Semantic.** The mission-critical map: which architecture elements anchor which design elements, plus the unbridged tail.
- **Question.** "How does implementation vocabulary map onto architecture — and what has no architectural counterpart?"
- **Computation (`coreEl.bridgeByArch`).** Cross-realm `realizes`/`enables`/`constrains` edges grouped
  by architecture target (busiest anchors first); the 6 unbridged design elements listed explicitly.
  Provenance (sourced : editorial) shown per edge.

### View 8 — Element relations (`el-graph`)
- **Semantic.** The typed element relation graph; a focused ego-network with cycle-safe closure.
- **Question.** "What realizes, specializes, composes-with, or is an alternative to what?"
- **Computation (`coreEl.closure` over the 1132-edge adjacency).** A focus element's direct
  neighbourhood laid out design-left / architecture-right; click any neighbour to re-focus. (A full
  1083-node graph is unreadable; the ego-graph is the scale-appropriate form.)

### View 9 — Element coverage (`el-coverage`)
- **Semantic.** Which works teach which elements (Phase 2), and where coverage is thin.
- **Question.** "Where do I read about this element; which works are element-dense; what is thinly covered?"
- **Computation (`coreEl.coverageBuckets` + the element→works inversion).** Coverage buckets
  (gap = 0 works, thin = 1, covered ≥ 2) and works ranked by element density; the 3 gap elements
  surfaced honestly.

## Cross-cutting lenses (not separate models)

- **Verification** — `verified | unverified` on works; **confidence** (`established | spot-checked`) on
  elements — always a visible badge.
- **Search** — substring over title/authors/id (works) or id/name/aka/what (elements), within the active view.
- **Corpus filter** — narrows the work models to one pass (element views are realm-filtered in-view instead).

## The persistent inspector

Not a model — the always-present right dock. With nothing selected it shows the **active view's**
semantic/question/computation (work models from `relations.views`; element views from
`coreEl.VIEWS`), the stat block, and the legend. With a **work** selected it shows the full citation,
corpus memberships, phase-2 reconciled tags, the raw per-report tags, both edge directions — and now
the **elements it teaches** (work → element navigation). With an **element** selected it shows the
definition, aliases, kind, realm, `named-in`, tags, the **covering works** (Phase 2, linking back to
the work corpus), and every typed relation including the cross-realm bridge edges with provenance.
