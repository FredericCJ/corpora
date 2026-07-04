# MODELS.md — the relational models (INFERENCE layer)

This file documents every navigation semantic the explorer offers. It is deliberately
separate from the fact layer: `data/corpus.json` / `data/corpus.js` contain only what the
six reports assert; everything here is computed or reasoned **on top of** those facts, and
every typed edge carries a provenance tag.

Corpora unified (superseding directive: everything in `E:\dev\corpora\SWE`):

| key | report |
|---|---|
| swa-science | Software Architecture as a Science (typed reading-graph corpus) |
| emb-arch | Architecture and Design of Embedded Software |
| emb-c | Design of Embedded Software Written in C |
| emb-cpp | Design of Embedded Software Written in C++ |
| emb-ops | Operational Use of C and C++ in Embedded Contexts |
| simulink | Architecture, Design & Management of Large Simulink/MATLAB Projects |

## Edge provenance discipline (anti-fabrication)

- `report:swa` — an entry of the swa-science report's numbered Typed Edge List (edge number kept in the note).
- `report:sim` — an entry of the simulink report's DAG Edge List. That list is directed
  *detail → abstraction*; the report's own rationale ("reasoning about higher-order
  abstraction requires first understanding the underlying detail") makes this exactly a
  prerequisite semantics, so these edges carry kind `prerequisite-of`.
- `derived` — mechanically derivable from an explicit sentence inside a report entry
  (the quoted basis is in the edge note), e.g. "BARR-C … fully harmonized with MISRA C:2012"
  → `companion`; "MISRA C++:2023 … merges the AUTOSAR C++14 guidelines" → `subsumes`.
- `editorial` — my reasoned judgment, never presented as report fact; rendered with an
  explicit **[EDITORIAL]** marker in the edge catalog and a distinct dash pattern in the graph.

Current census: 204 edges = 86 report:swa + 57 report:sim + 50 derived + 11 editorial.

Kind vocabulary (12, union of the swa report's 9-relation vocabulary plus three kinds needed
by report-stated facts): `prerequisite-of, refines, formalizes, surveys, applies-method-of,
companion, subsumes, evaluates, critiques, supersedes, part-of, references`.
`critiques` covers the swa report's "critiques / feeds-back-into" (its cycle-forming relation);
`supersedes` and `part-of` encode standards lineage ("supersedes the first edition", "Part 6 of…",
"Supplement to DO-178C"); `references` encodes stated traceability ("traceable to HIC++ 4.0, JSF…").

## Model 1 — Reading graph (view: `graph`)

- **Semantic.** Typed, directed, *cyclic-capable* relations between works — the reference
  pages' reading-graph pattern scaled to a computed layout.
- **Question answered.** "What should I read before / after / alongside this work, and why?"
- **Computation.** Node set = every node with ≥1 edge (~170 of 421). Layout is fully
  data-driven (hand layout is impossible at this scale): nodes are grouped into corpus
  bands, packed into a grid per band ordered by (theme, year). Hover traces the full
  ancestor+descendant closure (cycle-safe visited-set walk); the per-edge catalog below the
  board lists every edge with kind, provenance and its one-line justification.
- **Cycles.** The four cycles documented by the swa report (C1–C4) are preserved and tagged
  on their edges; `critiques` edges render dashed red.

## Model 2 — Facet browser (view: `facets`)

- **Semantic.** Classification lattice over the PHASE-2 reconciled vocabulary:
  corpus × branch (architecture | design | process | evaluation | operations | management)
  × theme × type (+ verification, role, ops lane, automotive band).
- **Question answered.** "What exists about X — and how much of it is verified?"
- **Computation.** Pure filtering/counting over node tags; no inference. Facet values that a
  source never asserts are simply absent for that node (not UNRESOLVED — see adjustments.md);
  UNRESOLVED appears only where a report itself flags the value unknown.

## Model 3 — Chronology (view: `timeline`)

- **Semantic.** Ordering by *year of last publication* (the citation rule shared by all six
  reports), with living/continuously-revised documents as their own stratum — a real feature
  of this corpus (toolchain manuals, vendor docs) rather than a data defect.
- **Question answered.** "How did this literature accumulate? What is maintained vs frozen?"
- **Computation.** Leading 4-digit year parsed from the year field; strata ≤1979, 1980s …
  2020s, LIVING, UNRESOLVED. No interpolation: unparseable years land in UNRESOLVED.

## Model 4 — Cross-corpus overlap (view: `overlap`)

- **Semantic.** The graft points: works claimed by ≥2 research passes. The reports required
  overlap to be *preserved and tagged, not dropped* — this view is that requirement made navigable.
- **Question answered.** "Which works bind the passes together; where do the corpora agree?"
- **Computation.** Nodes with |corpora| ≥ 2 (44 today), grouped by exact membership signature,
  plus a pairwise corpus×corpus count matrix. Membership added by merge (a report listing a
  work as an unverified lead that another report verified) is marked "lead" in the detail panel.

## Model 5 — Anchors & spine (view: `anchors`)

- **Semantic.** Curated entry points per corpus — the union of the reports' own emphasis
  marks: swa ★ target/canonical anchors, simulink TARGET designations, ops KEY /
  ABSOLUTELY KEY flags.
- **Question answered.** "Where do I start in each corpus?"
- **Computation.** role contains `anchor` — a fact carried from the reports, not my ranking.
  emb-arch, emb-c and emb-cpp assert no anchor facet, so they contribute none (stated in-view
  rather than silently absent).

## Cross-cutting lenses (not separate models)

- **Verification lens** — verified | unverified is preserved on every node from its report,
  is filterable everywhere, and is always visible as a badge. Any-verified-wins on merge is
  logged per node in `data/corpus_report.md`.
- **Search** — substring match over title/authors/id/ident, applied within whichever view is active.

## Why this set

The six reports natively use *different* organizing logics: a typed cyclic reading graph
(swa), a bottom-up prerequisite DAG (simulink), flat tag sorts (emb-c, emb-cpp, emb-ops) and
a two-branch shelf (emb-arch). The model set above keeps each native logic navigable
(models 1, 2), adds the two orderings every bibliography benefits from (3, 5), and makes the
one property unique to a *unified* corpus — cross-pass overlap — a first-class view (4).
Nothing in the set requires an unstated relation: models 2–5 are pure computations over
facts, and model 1's edges carry provenance per edge.
