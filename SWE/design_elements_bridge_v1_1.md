# Design ↔ Architecture bridge & element relations — v1.1 (atlas enrichment)

**Supersedes** `design_elements_bridge_v1_0.md` (1132 edges). This version adds the **within-realm
relational fabric** that WS1 of the atlas endeavour researched, so the element graph is dense and
navigable enough to form a map. The cross-realm bridge (the v1.0 mission deliverable) is carried
forward unchanged; what is new is design↔design and architecture↔architecture relations.

The relation set now holds **2811 edges** over the 1083 elements (709 design + 374 architecture).

## What changed from v1.0

| | v1.0 | v1.1 | Δ |
|---|---|---|---|
| total typed edges | 1132 | **2811** | +1679 |
| cross-realm (realizes/enables/constrains) | 878 | 878 | 0 (carried forward) |
| within-**design** (implements/specializes/composes-with/alternative-to/**uses**) | 252 | **1267** | +1015 |
| within-**architecture** (specializes/composes-with/alternative-to/uses) | 2 | **666** | +664 |
| design elements with **no** sibling relation | 332 | **0** | −332 |
| architecture elements with **no** sibling relation | 370 | **0** | −370 |
| overall mean degree | 2.1 | **5.19** | +3.1 |
| community modularity | 0.79 | **0.73** | still islandy (not a hairball) |

A new edge kind, **`uses`** (a directional dependency: A needs B as a part/subroutine/mechanism,
distinct from the symmetric `composes-with`), was introduced for this pass; the vocabulary is now 8
kinds. 488 of the new edges are `uses`.

## Method (WS1 — parallel research fan-out)

The 1083 elements were partitioned into **25 coherent research groups** (15 design by topic, 10
architecture by tactic quality-attribute / pattern domain / style / connector / deployment). Each group
ran a **harvest → adversarial-verify** pipeline: a researcher proposed source-grounded relations from
the canonical literature, then a second agent verified every citation, dropped unsupported or
mis-directed edges, and filled the gaps for still-relationless elements. Sources mined include GoF
*Related Patterns*, POSA relationship sections, Refactoring.Guru "Relations with Other Patterns",
Bass–Clements–Kazman tactic trees, Shaw–Garlan / Taylor–Medvidović–Dashofy style and connector
taxonomies, Hohpe–Woolf EIP, Fowler PoEAA, Nygard *Release It!*, Preschern *Fluent C*, Kleppmann DDIA,
and Douglass real-time patterns.

The proposed edges were merged with strict validation: endpoint + realm/kind legality, exact and
symmetric de-duplication (against the existing 1132 and among themselves), symmetric/directional
conflict resolution, and a per-node degree cap (14) to prevent hub hairballs. 71 duplicates, 2
degree-capped, and 2 symmetric conflicts were dropped.

## Provenance (anti-fabrication discipline preserved)

Every new edge is tagged `sourced` (a citable source states the relation — cited) or `editorial` (a
sound technical judgment, marked, never dressed as a fact). Of the 1679 new edges, **695 are sourced :
984 editorial** (41 % sourced). Across all 2811 edges: **1023 sourced : 1788 editorial**. A computed
`derived` co-realization backbone was available as a safety net for any architecture element the
research left disconnected; **it was not needed** — the research connected all 374 architecture
elements directly, so 0 derived edges were added.

## Edge-kind census (2811 edges)

| kind | count | direction |
|---|---|---|
| composes-with | 727 | within-realm, symmetric |
| realizes | 544 | design → architecture |
| uses | 488 | within-realm, directional (new) |
| alternative-to | 416 | within-realm, symmetric |
| enables | 324 | design → architecture |
| specializes | 249 | within-realm, directional |
| implements | 53 | design → design |
| constrains | 10 | architecture → design |

## Bridging rule (unchanged)

The mission's bridging rule still holds: **703 / 709 design elements carry ≥1 cross-realm edge**; the
same **6** design elements remain honestly unbridged (listed in v1.0). WS1 enriches within-realm
structure only; it did not change the cross-realm mapping.

## Where the data lives

The enriched relation set is the canonical `explorer/build/element_src/bridge.json`;
`python explorer/build/build.py` re-audits (completeness + bridging) and re-emits
`data/elements.{json,js}`, then builds the atlas layer (PHASE 5) on top. The full derivation
(per-group research files, merge script, stats) is under `SWE/_atlas_work/`.
