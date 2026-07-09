# MODELS.md — the five relational models

One fact layer (`data/corpus.json`), one inference layer (`data/relations.json`), five ways to
stand in it. Every model states its **semantic** (what the relation means), its **question** (what
a user asks it), and its **computation** (what the app derives vs what it merely carries). The
governing rule, inherited from the report's own caveats: *overlap is structural, never numeric* —
the app computes structure (reachability, path counts, shared neighborhoods) but never invents
weights, percentages, or rankings the report does not state.

## Provenance discipline

Two epistemic grades ride the data end-to-end, exactly as the report tags them:

- **EVIDENCED** — seams inferred from tables of contents, stated prerequisites, published reviews.
  Drawn solid, ink-grey.
- **JUDGMENT** — reasoned pedagogical judgment where evidence underdetermines the call (the
  Ashlock→Apostol edges, calculus→Velleman maturity edges, Pugh/Loomis→RCA). Drawn dashed, amber,
  everywhere they appear: graph, finder arrows, inspector seam rows.

Three seams the source table states as “same” (ditto rows) are expanded to the preceding row's
text and carry a transcription note saying so. The one dropped node (N18) is carried with its
edges **absent** — the report's edge list never cites it — and its gate verdict attached.

## Model 1 — Prerequisite DAG (`views/graph.js`)

- **Semantic.** `s → t`: s is prerequisite reading for t, with the named seam of shared topics.
- **Question.** What must I read before this text, and what does it unlock?
- **Computed.** Tier bands from the catalogue; within-band order by barycenter relaxation
  (`core.dagLayout` — presentation only, no meaning); hover closure = ancestors ∪ descendants
  (`core.closure`); parallel-set enclosures around contiguous members. Carried: every edge, its
  evidence tag, its seam (hover any edge). Acyclicity is not assumed from the prose — the build
  proves it by topological sort before the data ships.

## Model 2 — Tier ladder (`views/tiers.js`)

- **Semantic.** The report's §1 maturity scheme: nine levels from computational algebra readiness
  to research-level sinks.
- **Question.** What does each level contain; which texts sit at my level?
- **Computed.** Buckets by catalogue tier only. The scheme's name / focus / rigor strings are
  quoted verbatim in the column headers — the app adds no levels and re-grades no text.

## Model 3 — Lineages & paths (`views/lineage.js`)

- **Semantic.** A lineage is an ordered walk along edges — a reading order, not a new relation.
- **Question.** In what order do I actually read; what are my alternatives?
- **Computed.** The two §7 presets are carried verbatim (path + per-seam justification steps; the
  build asserts every hop is a real edge). The finder computes, for any (from, to): the **exact**
  number of directed paths (memoised DP over the DAG) and an enumeration sorted shortest-first,
  capped at 400 **with the cap stated in the meta line** (N01→N27 = 136 paths, uncapped in
  practice). Hop arrows inherit the underlying edge's evidence tag.

## Model 4 — Parallel sets (`views/parallel.js`)

- **Semantic.** §4: equivalent-scope siblings — *shared, not sequenced*; no A→B inside a set.
- **Question.** Which texts are alternatives to each other rather than prerequisites?
- **Computed.** Membership and set notes are carried. The **shared vs partial neighborhood audit**
  is computed at build time from the edge list: a neighbor is *shared* if every member has the
  edge, *partial* otherwise (annotated with which members carry it). This makes the report's
  "siblings inherit the same edges" caveat checkable — and where it only partially holds (PS-2's
  N09, PS-6's sinks), the card says so instead of smoothing.

## Model 5 — Quality gate (`views/gate.js`)

- **Semantic.** The report's editorial spine: why each candidate is in (or out), what remains
  open, and what bounds every claim.
- **Question.** Why should I trust this graph — and where should I not over-trust it?
- **Computed.** Nothing. The TL;DR, the 22-row ledger (build-checked to cover all 27 nodes exactly
  once, statuses agreeing with the catalogue), the open register, and the six caveats are carried
  verbatim. The caveats are placed as a first-class pane because they constrain the other four
  models' interpretation.

## The inspector

Selecting any text anywhere shows: full citation (authors, edition, year, publisher, ISBN),
verification + kept/dropped badges, structural flags (source / sink / sink-adjacent / terminal
leaf / supporting), its tier's scheme entry, parallel-set siblings (linked), lineage memberships
with step position, the gate verdict, every incoming and outgoing seam with evidence tags, and the
§9 bibliography line verbatim. With nothing selected it explains the active model, the corpus
stats, the full legend, and links the machine-verification log (`data/corpus_report.md`).
