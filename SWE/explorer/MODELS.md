# MODELS.md — the relational models (INFERENCE layer)

Five navigation semantics over one fact layer. `data/corpus.json` holds only what the seven reports
assert; everything here is computed **on top of** those facts, and every typed edge carries a
provenance tag. The models are unchanged from the original design — the single-viewport rebuild
changed how each is *rendered* (noted per model), not what it *means*. The pure computations live
in `logic/core.js`; the view shells only project them.

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

## The persistent inspector

Not a model — the always-present right dock. With nothing selected it shows the **active model's**
semantic/question/computation (from `relations.views`), the corpus stat block, and the full legend
(corpora, 12 edge kinds with dash patterns, provenance & honesty markers). With a work selected it
shows the full citation, corpus memberships, phase-2 reconciled tags, the raw per-report tags
exactly as each report stated them, and both edge directions with kind + provenance + justification.
