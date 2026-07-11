# ATLAS PLAN — Visual navigation of the element corpus (atlases & archipelagos)

**Status:** planning. **Author:** drafted 2026-07-11, endorsed design. **Prereq:** the ELEMENT-layer
mission is complete (`MISSION_design_elements_v1.md`, `EXPANSION_REPORT_2026-07-10_elements.md`):
709 design + 374 architecture elements, 1132 typed bridge edges, four element views in
`explorer/` (views 6–9). This plan adds a **visual, semantic-zoom map** — the *Atlas* — as view 10+.

The endorsed model (recap): a "graph as map" / semantic-zoom system (academic touchstone: **GMap**).
Three discrete zoom levels with a breadcrumb — **L0 Atlas** (an archipelago of ~15–25 islands, nodes
not readable, sea-routes = aggregated bridge) → **L1 Island** (one community, hub-and-spoke, readable,
ports to neighbours) → **L2 Node** (the existing ego-graph + inspector). Islands are **emergent
communities** (modularity Q≈0.79 in the probe), coloured by a ~7-way **family** roll-up of the kinds.

This plan has **three workstreams in a mandatory order** — you cannot cluster well on a sparse graph,
and you cannot freeze geography before it is connected:

> **WS1 Enrich the relations → WS2 Consolidate the archipelago → WS3 Implement the views.**

---

## Empirical baseline (measured, not assumed)

The atlas design rests on these facts about the current 1083-node / 1132-edge element graph:

| metric | value | implication |
|---|---|---|
| connected components | 809-node giant + 205 small/singleton | one continent + a scatter of dust |
| mean degree | **2.1** | too sparse for rich islands |
| within-**design** (sibling) edges | **252** (composes-with 89, alternative-to 65, specializes 59, implements 39) | islands are near-pure **stars** |
| design elements with **zero** sibling relation | **332 / 709** | half of design has no lateral structure |
| within-**architecture** edges | **2** | the architecture realm has **no fabric** |
| **disconnected architecture** elements | **163 / 374** (pattern 61, tactic 37, style 22, deploy 18, desc 15, ref-arch 6, conn 4) | the arch realm is unnavigable as a graph |
| emergent community modularity Q | **0.79** (inter-cluster edges 19%) | clean islands *do* emerge — the archipelago is real |
| clustering by kind / realm | Q=0.14 / Q=−0.30 | facets are **colour/label**, never geography |
| cross-realm design→arch edges | 868 onto 210 arch targets (top-10 = 29%) | hub-and-spoke; a legible bipartite Bridge-Flow exists |

**Reading:** the graph already clusters into coherent, nameable islands, but each island is a star
(a hub tactic + design spokes) with almost no lateral tissue, and the architecture realm is 44%
disconnected. WS1 fixes the tissue; WS2 freezes the islands; WS3 draws the map.

---

## WS1 — Realize the missing relations (research)

**Goal.** Densify the element graph with **real, source-verified** relations that "can be sensed but
are missing", so islands are internally navigable and the architecture realm becomes a connected
fabric. Same anti-fabrication discipline as the mission: every edge is `sourced` (a citable source
states the relation — cite it) or `editorial` (reasoned judgment, marked, never dressed as fact);
provenance is tagged; the sourced:editorial ratio is reported.

### Two tracks (the gap is two-shaped)

- **1A · Design sibling fabric** — design↔design relations *within each island*. The pattern/idiom
  literature is explicit about these: GoF "Related Patterns", POSA relationship sections, Refactoring
  .Guru "Relations with Other Patterns", Nystrom cross-references, EIP pattern relationships,
  domain books (Kleppmann, Gregory, Douglass, Preschern). Target the 332 sibling-less design elements
  first.
  - *Example edges to recover:* `thread-pool` **uses** `work-queue`; `memoization` **specializes**
    `caching`; `ring-buffer` **alternative-to** `double-buffer`; `RAII` **specializes** `scope-guard`;
    `circuit-breaker` **composes-with** `retry`; `LSM-tree` **uses** `write-ahead-log`.
- **1B · Architecture relational fabric** — arch↔arch relations. **Biggest single win** (2 → hundreds;
  connects 163 disconnected nodes). Three sub-shapes, each with a canonical source already in corpus:
  - **Tactic trees** — Bass–Clements–Kazman (`bck`) organizes each QA's tactics into a
    detection/recovery/prevention hierarchy: the tree *is* the edge set (`specializes` /
    `refines`). Connects the 37 disconnected tactics and relates all 109.
  - **Style family tree** — Shaw–Garlan / Taylor–Medvidović–Dashofy boxology: dataflow → pipes-and-
    filters; call-return → layers / OO; the style taxonomy is a `specializes`/`alternative-to` forest.
  - **Pattern → style / connector → style** — each architecture *pattern* realizes or refines a
    *style*; connectors bind styles. (POSA, TMD connector taxonomy.)
- **1C · (optional) Derived co-realization backbone** — *computed, not researched*: link two
  architecture elements when ≥k design elements realize both (and same-QA tactics). Off by default,
  clearly tagged `derived`. Decide in WS2; it is a cheap safety net for any arch element the research
  leaves unconnected.

### Edge-kind vocabulary (decision — see Open Decisions §1)

Keep the existing 7 (`realizes`,`enables`,`constrains`; `implements`; `specializes`,`composes-with`,
`alternative-to`) and **add one**: `uses` (directional dependency: A needs B as a part/subroutine,
distinct from the symmetric `composes-with`). Final set = **8**. `refines` (arch tactic/pattern
refining a parent) folds into `specializes` unless a distinct kind proves necessary.

### Method — parallel research fan-out (multi-agent; needs the `ultracode` opt-in to run)

1. **Scope map (pre-work, inline):** compute per-island member lists and per-kind/per-QA arch groups;
   list the 332 sibling-less design elements and 163 disconnected arch elements as the priority set.
2. **Fan out ~24 research agents:** ~15 by design island (1A) + ~9 by arch group (1B: one per QA
   cluster of tactics, one for styles, one for patterns→styles, one for connectors/deployment/desc/
   ref-arch). Each agent: reads its members' definitions, researches the relations among them from the
   sources above (live-verify obscure ones), proposes typed edges with `provenance` + `cite`, and
   avoids duplicating any of the existing 1132 edges.
3. **Merge / validate / audit (inline):** dedup by (from,kind,to) and by symmetric equivalence for the
   symmetric kinds; validate endpoints + realm/kind legality (e.g. `uses` stays within a realm);
   cap per-node degree (~12) to prevent hairballs; re-run connectivity + modularity.
4. **Integrate:** append to the relations set; rebuild; regenerate the bridge/relations deliverable.

### Sources to mine (concrete)

GoF *Design Patterns* (`gof`, Related Patterns) · POSA 1–3 (`posa1/2/3`, relationship sections) ·
Refactoring.Guru / SourceMaking (relations blocks) · Nystrom *Game Programming Patterns* · Hohpe–Woolf
EIP · Bass–Clements–Kazman (`bck`, tactic trees) · Shaw–Garlan (`shawgarlan96`, `garlanshaw93`) ·
Taylor–Medvidović–Dashofy (`tmd`, connector taxonomy) · Kleppmann DDIA · Douglass · Preschern *Fluent C*
· Fowler PoEAA (pattern relationships).

### Acceptance metrics (checkable)

| metric | now | target |
|---|---|---|
| within-architecture edges | 2 | **≥ 250** |
| within-design (sibling) edges | 252 | **≥ 700** |
| disconnected architecture elements | 163 | **≤ 15** |
| sibling-less design elements | 332 | **≤ 100** |
| mean degree | 2.1 | **≥ 4.5** |
| modularity after enrichment | 0.79 | **≥ 0.55** (still islandy — not a hairball) |
| provenance | — | every new edge tagged; sourced:editorial ratio reported; 0 duplicates |

### Deliverable

`SWE/design_elements_bridge_v1_1.md` (the bridge/relations report, extended with the enriched
within-realm relations, counts + sourced:editorial ratio updated) **or** a companion
`SWE/element_relations_v1_0.md` (decision §7). The enriched edges land in
`explorer/build/element_src/bridge.json`; `python build/build.py` re-audits and re-emits
`data/elements.{json,js}`. An expansion-report section logs the pass.

### Risks

Over-connection → hairball (mitigate: degree cap, high-confidence-first, modularity floor). Editorial
dominance (mitigate: the relationship literature is rich → sourced should lead; report the ratio).
Symmetric-edge double counting (mitigate: canonical ordering + symmetric dedup in the merge).

---

## WS2 — Consolidate the atlases & archipelagos

**Goal.** Turn the (now-enriched) graph into a **frozen, named, deterministic geography** the views
render — and lock the conceptual model. Two deliverables: a **spec** (the definitive model) and a
**data artifact** (the consolidated islands + coordinates).

### 2.1 The definitive model (terminology frozen)

- **Atlas** = a top-level map of the whole element space. There are **two**:
  - **The Archipelago** (default) — emergent community islands; the "explore the terrain" map.
  - **The Bridge-Flow** — a bipartite design-family → architecture map; the 868 cross edges as flows;
    the faithful "big picture" of the realize/enable mapping, and the natural home for arch elements.
- **Island** = one community (L1). **Region/family** = the ~7-way colour grouping of kinds.
- **Level** = L0 Atlas · L1 Island · L2 Node (ego-graph, already built). Breadcrumb across all three;
  full state in the URL hash (`#view=el-atlas&atlas=archipelago&island=…&node=…`) for deep links.

### 2.2 Resolve the open decisions (recommendations; user confirms — see §Open Decisions)

1. **Island scheme:** Archipelago (emergent) default + Bridge-Flow as a second atlas. ✔
2. **Disconnected arch:** WS1 removes most; residual ≤15 → the optional 1C co-realization overlay
   (off by default) + taxonomy hand-off. ✔
3. **Polish:** ship **sized bubbles + convex-hull tints** first; GMap coastlines are a later polish.
4. **Scope:** elements only now; the 468-work reading graph gets the same machinery later (optional).

### 2.3 Consolidation as a data task

1. **Cluster the enriched graph** with a deterministic modularity method (Louvain-style greedy;
   deterministic tie-breaks by id) — better/fewer islands than the probe's label-prop.
2. **Curate & freeze:** merge sub-threshold islands into their nearest neighbour or a labelled
   **"fringe"**; split any island >~70 into sub-islands (L1 sub-clustering); **name** each island (from
   its dominant kinds + hub, e.g. "Events, messaging & concurrency"); assign a **family** (colour);
   record hub + 3 representative members + neighbour islands + internal cohesion. Every element lands
   in exactly one island.
3. **Precompute deterministic layouts** at build time (seed positions from a hash of the id; fixed
   iteration count; **no `Math.random`**) so the map is spatially stable across sessions — users build
   spatial memory. Meta-graph layout (islands) + per-island radial layout + hull polygons.

### Deliverables

- `SWE/ATLAS_SPEC.md` — the frozen model (levels, atlases, families, palette, interaction contract).
- `explorer/build/element_src/atlas.json` (or computed in-build) — the canonical islands: id, name,
  family, members[], hub, representatives[], neighbours[], and precomputed coordinates + hull.

### Acceptance

~15–25 named islands; every element assigned; family roll-up + palette defined; deterministic layout
present and stable across two builds (byte-identical coordinates); the model doc is complete.

---

## WS3 — Implement the atlas & archipelago views

**Goal.** Land the Atlas as view 10 (+ Bridge-Flow as view 11 or a scheme toggle), reusing the house
architecture (pure core + thin SVG shells, `window.SWE`, `file://`-safe, zero deps, honesty markers).
Page/inner scroll is already authorized for element views. The five work models and the four element
views must not regress.

### 3.0 Data layer

`build/build_atlas.py` (or a PHASE 5 in `build.py`): consumes the enriched `bridge.json` + the
consolidated `atlas.json`, validates (every element in exactly one island; coords present; meta-edges
reference real islands), and emits `data/atlas.{json,js}` (`SWE.atlas`: islands, families, meta-graph,
coords, hulls). Self-audit fails loud on any unplaced element.

### 3.1 Pure core (`core_atlas.js`, additions to `core_elements.js`)

`metaGraph(islands, edges)`, `forceLayout(nodes, edges, {seed, iters, aspect})`, `radialLayout(hub,
spokes)`, `hull(points)`, `locate(query, islands)` (search→island). All pure, deterministic, testable;
consume precomputed coords where shipped (the browser never runs the heavy full-graph layout).

### 3.2 Sub-phases (each verified before the next)

- **A · L0 Archipelago + drill.** View 10: island bubbles (size = members, tint = family) laid out by
  the meta-graph; sea-routes = aggregated bridge (thresholded/bundled to avoid a route hairball); hover
  → routes + top hubs; **click → L1**. Breadcrumb + hash. *Milestone M3.*
- **B · L1 Island + L2 hand-off.** Radial island layout (hub centre, spokes around); labelled **ports**
  to neighbour islands (click → hop); big islands show **sub-islands** first; **click a node → L2**,
  which reuses the existing ego-graph (view 8) + inspector. Inspector gains **island detail** (name,
  family, members, hubs, neighbours). *Milestone M4.*
- **C · Wayfinding + Bridge-Flow.** Minimap (a tiny Archipelago showing "you are here"), **search-
  teleport** (query highlights islands + flies you in), hover-preview, animated zoom (respect
  `prefers-reduced-motion`); the **Bridge-Flow** bipartite atlas (view 11 or scheme toggle). *M5.*
- **D · Polish (optional).** GMap-style coastline regions; the works-corpus atlas over the 261-edge
  reading graph. *M6.*

### 3.3 Verification (Node unavailable → headless Chrome, per the mission)

`python build/build.py` clean, all audits green (element/edge completeness, bridging, atlas placement).
Headless Chrome `--dump-dom` + `--enable-logging=stderr` over `file://` and a served
`http://localhost:8098`: all view tabs mount with **zero boot/runtime errors**; L0→L1→L2 navigation,
breadcrumb, ports, search-teleport, and deep-link hashes all work; **the 9 existing views are
unregressed** (occurrence-count checks).

### 3.4 File-touch surface

New: `build/build_atlas.py`, `element_src/atlas.json`, `logic/core_atlas.js`,
`logic/views/el_atlas.js` (+ `el_bridgeflow.js`), `data/atlas.{json,js}`. Extended: `build/build.py`
(PHASE 5), `logic/app.js` (view registry → 10/11, keys), `logic/inspector.js` (island detail),
`index.html` (scripts + counts), `styles/app.css` (island/region/route/minimap classes), `README.md`,
`MODELS.md`, `ARCHITECTURE.md`. Log: `EXPANSION_REPORT_<date>_atlas.md`.

---

## Cross-cutting rules (all workstreams)

- **House discipline:** pure functional core + thin shells; `window.SWE` classic scripts; runs from
  `file://`; zero runtime deps; strict-JSDoc typing contract; global error backstops. Honesty markers
  stay visible (sourced vs `editorial`/`derived` edges; unbridged/gap honesty carries into the map).
- **Determinism is non-negotiable** for a map: every layout seeds from id hashes with fixed iteration
  counts — **never `Math.random`** — so the archipelago looks identical every session.
- **Anti-fabrication:** WS1 edges are sourced-or-editorial with provenance; no invented relations.
- **Durable + resumable:** each workstream writes results to disk incrementally; a `RESUME_STATE`
  under `SWE/_atlas_work/` mirrors the element-mission pattern; committing stays the user's call.
- **Orchestration:** WS1 and WS3-A/B are multi-agent-parallelizable (research fan-out; view shells
  against a verified template) and should be run under `ultracode`; merges/audits/integration stay
  inline for coherence, exactly as the element mission ran.

---

## Sequencing & milestones

```
WS1 enrich ──▶ WS2 consolidate ──▶ WS3-A L0 ──▶ WS3-B L1+L2 ──▶ WS3-C wayfind+flow ──▶ WS3-D polish
   M1              M2                 M3            M4               M5                    M6
(WS2 spec §2.1–2.2 can be drafted in parallel with WS1; WS2 §2.3 data needs WS1 output.)
```

- **M1** WS1 done — enriched relations, audits green, bridge v1.1, rebuild clean.
- **M2** WS2 done — `ATLAS_SPEC.md` + `atlas.json` (named islands + stable coords).
- **M3** L0 Archipelago clickable into L1.
- **M4** L1 islands + ports + L2 ego-graph + island inspector.
- **M5** minimap + search-teleport + Bridge-Flow atlas.
- **M6** polish (GMap / works atlas) + docs + expansion report.

Hard dependency chain: **WS1 → WS2 → WS3**. Do not cluster (WS2) before enrichment (WS1) lands, or the
geography freezes on a star-forest.

---

## Open decisions for you (confirm before WS1 starts)

1. **Edge vocabulary** — add `uses` (directional dependency)? *(rec: yes; keeps the set at 8.)*
2. **Co-realization backbone (1C)** — include the optional computed `derived` overlay, off by default?
   *(rec: yes — cheap safety net for stragglers.)*
3. **Research depth/budget for WS1** — exhaustive (chase every island to the acceptance targets) vs
   a first sourced-only sweep? *(rec: exhaustive to the metrics; the literature supports it.)*
4. **Bridge-Flow** — a separate view (11) or a scheme toggle inside view 10? *(rec: separate view.)*
5. **GMap coastlines** — now or as M6 polish? *(rec: later; bubbles+hulls first.)*
6. **Works atlas** — in scope or a future endeavour? *(rec: future; identical machinery on 261 edges.)*
7. **Enriched-relations deliverable** — bump `design_elements_bridge` to v1.1, or a new
   `element_relations_v1_0.md`? *(rec: bridge v1.1 — keep the relation layer in one place.)*

---

## Deliverables checklist — COMPLETE (2026-07-11)

- [x] WS1: enriched `bridge.json` (+666 arch / +1015 design edges — targets exceeded); `design_elements_bridge_v1_1.md` (2811 relations); audits green.
- [x] WS2: `ATLAS_SPEC.md`; `atlas.json` (**21** named islands, 7 families, deterministic byte-identical coords).
- [x] WS3: `build_atlas.py` + PHASE 5; `core_atlas.js`; `el_atlas.js` + `el_bridgeflow.js`; `data/atlas.{json,js}`.
- [x] Views 10 + 11 mount, L0→L1→L2 nav + ports + minimap + search-teleport work, zero console errors, 9 existing views unregressed (headless-Chrome verified).
- [x] Docs updated (README, MODELS, ARCHITECTURE); `EXPANSION_REPORT_2026-07-11_atlas.md`.
- [x] `_atlas_work/RESUME_STATE.md` durable state; **nothing committed** (the user's call).
