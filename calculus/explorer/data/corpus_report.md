# corpus_report.md — build + structural verification log

Source: `calc-analysis.md` (bibliography access date 8 July 2026; compiled 2026-07).

## PHASE 1 — fact layer (nodes)
- 27 nodes carried (26 kept + 1 dropped: N18); all fields present; all [VERIFIED].
- tier population: T0:2, T1:5, T2:2, T3:1, T4:4, T5:4, T6:6, T7:1, T8:2.

## PHASE 2 — inference layer (edges + editorial spine)
- 46 edges (38 EVIDENCED + 8 JUDGMENT); endpoints exist; no edge touches N18.
- §3 edge table and §6 DOT rendering state the SAME 46-edge set (independent transcriptions agree).
- 6 parallel sets; each set's members share one tier; no dropped members.
- both lineages walk actual edges hop-by-hop (main 8 nodes / variant 5 nodes).
- quality-gate ledger: 22 rows cover all 27 nodes exactly once; kept/dropped agrees with the catalogue.

## PHASE 3 — structural verification
- ACYCLIC (machine-checked): Kahn topological sort places all 26 kept nodes.
  topological order: N01 N02 N03 N04 N05 N06 N07 N08 N09 N10 N11 N12 N13 N14 N15 N16 N17 N19 N20 N21 N22 N23 N24 N25 N26 N27
- tier-monotone: every edge satisfies tier(s) ≤ tier(t); within-tier edges: N01→N02, N10→N12 (the report allows “forward within a tier boundary from a prerequisite to a strict extension”).
- degrees: source nodes (in-degree 0) = N01 — matches the report's single SOURCE designation (N01).
- graph-terminal nodes (out-degree 0) = N16, N21, N22, N23, N26, N27; the report designates N26, N27 as SINKS, N21, N22, N23 as terminal leaves of the complex lineage, and N16 as a supporting terminal — the sets agree.
- parallel-set shared-edge audit (stated: siblings inherit the same in/out edges):
  - PS-1 {N06, N07}: shared-in ['N02'], shared-out ['N08', 'N09']
  - PS-2 {N03, N04, N05}: shared-in ['N02'], shared-out ['N08']; PARTIAL out {'N09': ['N05']}
  - PS-3 {N11, N12}: shared-in ['N09'], shared-out ['N14', 'N15']; PARTIAL in {'N10': ['N12']}
  - PS-4 {N14, N15}: shared-in ['N11', 'N12'], shared-out ['N19', 'N20', 'N24']; PARTIAL in {'N08': ['N14'], 'N10': ['N14']}; PARTIAL out {'N22': ['N14'], 'N23': ['N14'], 'N21': ['N14']}
  - PS-5 {N21, N22, N23}: shared-in ['N14'], shared-out —
  - PS-6 {N19, N20, N24}: shared-in ['N14', 'N15'], shared-out ['N25']; PARTIAL in {'N17': ['N19']}; PARTIAL out {'N27': ['N19', 'N24'], 'N26': ['N20']}
  NOTE: PS-2 is stated to share outgoing edges to N08/N09, but the drawn edge list gives N09 only to N05 — carried as a partial edge, not smoothed over. PS-6 shares only N25 downstream (N26/N27 reachable from two of three members); also carried as partial.
- path finder default: N01 → N27 has exactly 136 directed paths (DP over the topo order).

## PHASE 4 — emission
- wrote data/corpus.json + data/corpus.js
- wrote data/relations.json + data/relations.js

Totals: 27 nodes (26 in the DAG + 1 dropped) · 46 edges (38 EVIDENCED / 8 JUDGMENT) · 9 tiers · 6 parallel sets · 2 lineages · 22 ledger rows.
