# MODELS.md — the relational model (INFERENCE layer)

This explorer offers **one** navigation semantic: a typed, directed **lineage graph** of data
structures. The fact layer (`data/corpus.js` — what the two reports assert about each structure)
is kept strictly separate from the inference layer (`data/relations.js` — the typed edges between
them). Every edge carries a provenance tag; nothing at the presentation layer is authored by hand.

## The two source reports (and what each contributes)

| key | report | contributes |
|---|---|---|
| `audit` | *Audit of ChatGPT's Foundational Source Answers for 17 Data Structures* | the **corrected foundational citations** for the 17 roots, plus each root's **CONFIRM / FIX / ENUMERATE** verdict |
| `topology` | *Topology of Data Structures: A Modern-Anchored, Bottom-Up Lineage Graph* | the **modern inventory** (§2 — 8 back-filled roots + ~85 modern structures) and the **typed edge list** (§3) with its **cycles** (§4) |

The 17 foundational roots appear in **both** reports — a cross-pass overlap surfaced as an
"appears in" section in each node's inspector, exactly the way the reference SWE explorer surfaces
its cross-corpus overlap.

## The model — Lineage graph (the whole app)

- **Semantic.** Typed, directed, *cyclic-capable* relations between structures, presented
  root → modern (ancestor → descendant), exactly as the topology report presents §3.
- **Question answered.** "What does this structure descend from, what descends from it, and how?"
- **Computation.** Node set = every structure with ≥1 edge (all 110). Layout is fully data-driven
  (hand layout is impossible at this scale): nodes are grouped into **family bands**; the bands are
  **shelf-packed** to best match the viewport's aspect so the whole graph fits one screen; within a
  band, nodes sort by (tier, year) so roots sit at the top. Hover/focus traces the **cycle-safe**
  ancestor+descendant closure and dims the rest; every edge in the inspector carries kind +
  provenance + a one-line basis.
- **Cycles.** The four genuine relation-typed cycles the topology report documents (§4) are
  preserved and tagged on their edges (`cycle C1..C4`), and explained in the overview panel.

## Edge kind vocabulary (topology §3)

`refines`, `specializes`, `generalizes`, `encodes`, `hybridizes`, `influences` — six relations,
root → modern. `hybridizes` and `influences` render dashed (cross-lineage / design-inspiration);
`influences` is deliberately reserved for conceptual inspiration rather than genealogical descent.

## Edge provenance discipline (anti-fabrication)

Mirrors the reference explorer's discipline — every edge declares where it came from:

- `report:topology` — an entry of the topology report's typed edge list (§3) or cycle set (§4);
  the §-number is kept in the note. **103 edges.**
- `derived` — mechanically implied by an explicit sentence *elsewhere* in a report, with the basis
  quoted in the note (e.g. the report naming a "Treiber **stack**" implies `stack specializes
  treiber`; the audit's deque "input-/output-restricted variants" implies `deque generalizes
  queue/stack`). **10 edges.**
- `editorial` — my reasoned structural judgment, never presented as report fact; rendered
  **[EDITORIAL]** with dotted edges (e.g. `record influences linkedlist`, the augmented-BST
  attachments of the geometric query trees). **8 edges.**

## Node fact semantics

- **tier** — `root` (the audit's 17), `backfill` (topology's 8 [F-NEW] back-filled roots), or
  `modern`. Roots and back-fills draw with an accent border and a ★.
- **verification** — `verified` (an origin paper with named authors + venue is confirmed, the
  topology report's §6 rigor threshold) or `flagged`. **Flagged is never dropped**, only marked
  (dashed border + ⚠), with the reason in `flags`:
  - `folklore` — no origin paper (gap buffer, piece table, ring buffer)
  - `theory-only` — a theory root but no single implementation paper (bit array, multiset)
  - `diffuse-origin` — no single foundational paper (queue, deque, dynamic array)
  - `reference-not-origin` — a canonical reference stands in for a diffuse origin (binary tree)
  - `origin-not-in-report` — the source report names it without a citation (many variants)
  - `ambiguous-date` / `ambiguous-name` / `soft-attribution` / `dual-priority` — surfaced caveats
- **verdict** — the audit's own label for the 17 roots (`CONFIRM` / `FIX` / `ENUMERATE`), shown as
  an `audit:` badge.

## Why one model (not five)

The reference SWE explorer needed five models because its six reports used six different organizing
logics. Here both reports already speak the *same* logic — a typed root→modern lineage graph — so
the honest, faithful representation is that one graph, made navigable and fitted to a single
viewport. Facets/timeline would be derivable (family, year are on every node) but would fracture
the one thing the reports actually assert: the descent relations.
