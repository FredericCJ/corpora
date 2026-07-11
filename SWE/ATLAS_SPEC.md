# ATLAS SPEC — the frozen model for the element atlas

**Status:** frozen model (WS2 §2.1–2.2). The island **census** (§4) is filled by the consolidation
run (WS2 §2.3) once WS1 enrichment lands. **Companion:** `ATLAS_PLAN.md` (the workstream plan),
`EXPANSION_REPORT_<date>_atlas.md` (the build log). This document is the single source of truth for
the atlas's *concepts, geography rules, palette, and interaction contract* — the views (WS3) implement
exactly what is written here.

The atlas is a **"graph as map"** with **semantic zoom** (academic touchstone: *GMap*, Gansner et al.).
The 1083-element graph is too large to read at once, so we render it at three fixed zoom levels and
let the reader drill. Geography is **emergent** (communities the graph forms on its own), **named**,
and **deterministic** (identical every session, so the reader builds spatial memory).

---

## 1. Atlases (top-level maps)

There are **two** complementary atlases over the same element set. The reader toggles between them; each
answers a different question.

| Atlas | Question it answers | Topology | Default |
|---|---|---|---|
| **The Archipelago** | "What *is* the terrain — what clusters exist and how do they sit?" | emergent community **islands** on a sea; sea-routes = aggregated relations | ✔ default |
| **The Bridge-Flow** | "How does *design* realize *architecture*?" | bipartite: design **families** (left) → architecture **anchors** (right); ribbons = `realizes`/`enables` flows | view 11 |

The Archipelago is the explore-the-space map (WS3-A/B). The Bridge-Flow is the faithful big-picture of
the cross-realm mapping — the natural home of the 868 cross-realm edges and of architecture elements as
*destinations* (WS3-C).

---

## 2. Levels (semantic zoom)

One breadcrumb spans all three. Full navigation state lives in the URL hash for deep links:
`#view=el-atlas&atlas=archipelago&island=<id>&node=<id>`.

- **L0 — Atlas.** The whole space as ~15–25 **island bubbles** on a sea. Node labels are *not* shown
  (not the point at this zoom). Bubble **size** = member count; bubble **tint** = family (§3).
  **Sea-routes** connect islands whose members relate across island boundaries, thickness = aggregated
  edge count (thresholded + bundled so the sea doesn't become a hairball). Hover → routes + the island's
  top hubs. **Click an island → L1.**
- **L1 — Island.** One community, now **readable**. Radial layout: the island's **hub** (highest within-
  island degree) at centre, members around it, intra-island edges drawn. Around the rim sit labelled
  **ports** — one per neighbouring island — click a port to **hop** to that island. Islands larger than
  ~70 members show **sub-islands** first (one more drill). **Click a node → L2.**
- **L2 — Node.** The existing **ego-graph** (view 8) + the persistent inspector, unchanged: the focused
  element, its typed neighbours (design-left / architecture-right), cross-realm bridge edges with
  provenance, covering works. This is where the atlas hands back to the element layer already shipped.

---

## 3. Regions / families (colour)

Islands are tinted by **family** — a **7-way** semantic roll-up of the 29 element kinds, so the whole map
reads in seven colours. An island's family = the **dominant family of its members**. Each element's
family derives from its `kind` (and, for architecture tactics/patterns, its quality-attribute / domain
tag). Palette is **Okabe–Ito** (colourblind-safe) so families stay distinguishable in light and dark.

| # | Family | Covers (design kinds · architecture kinds) | Colour | Hex |
|---|---|---|---|---|
| 1 | **Concurrency & Coordination** | synchronization-coordination, execution-concurrency, scheduling-time · performance/scalability tactics of a timing nature | blue | `#0072B2` |
| 2 | **Data & Storage** | data-structures, persistence-durability, caching-memoization, data-representation, serialization-framing · data/database patterns | green | `#009E73` |
| 3 | **Communication & Distribution** | communication · distributed/messaging/integration patterns, connectors | sky | `#56B4E9` |
| 4 | **Structure & Creation** | oo-patterns, construction-api, code-structure, state-management · styles, enterprise patterns, description | purple | `#CC79A7` |
| 5 | **Reliability & Safety** | error-handling, robustness-security · availability/security/safety tactics, reliability patterns | vermillion | `#D55E00` |
| 6 | **Resource & Runtime** | resource-management, data-flow-buffering, embedded-systems, numeric-precision · deployment, performance/energy tactics | orange | `#E69F00` |
| 7 | **Foundations & Types** | functional-type-idioms, parsing-text, testing-constructs · reference-architecture | neutral | `#949494` |

The palette is used at three opacities: solid for bubbles/labels, ~0.18 alpha for L1 island hull tints,
and a faint wash for the L0 family legend. A neutral family (grey) is deliberate — it reads as the
substrate/foundation rather than competing for attention.

---

## 4. Island census (consolidated 2026-07-11)

Deterministic Louvain over the WS1-enriched graph (all 2811 edges — islands span realms via the bridge)
yielded **21 named islands**, modularity Q ≈ 0.70, every one of the 1083 elements placed in exactly one.
Names are the naming pass's; family is the dominant family of the members; d/a = design/architecture split.

| Island | Family | Size | d/a | Hub |
|---|---|---:|---:|---|
| Object-Oriented Design Patterns | structure | 114 | 92/22 | defer-binding |
| Memory Management & Caching | resource | 92 | 78/14 | exception-prevention |
| Security, Auth & Cryptography | reliability | 73 | 30/43 | authenticate-actors |
| Transactions & Durable Storage | data | 71 | 46/25 | transactions |
| Fault Tolerance & Recovery | reliability | 66 | 39/27 | monitor |
| Concurrent Execution & Messaging | communication | 62 | 37/25 | thread-pool |
| Exceptions, Contracts & Testing | reliability | 61 | 45/16 | exception-handling |
| Data Structures & Encoding | data | 60 | 57/3 | increase-resource-usage-efficiency |
| Real-Time Scheduling & Interrupts | concurrency | 50 | 35/15 | limit-event-response |
| Dataflow & Reactive Streams | structure | 46 | 27/19 | streaming-dataflow-architecture |
| Parsing, Compilers & Interpreters | foundations | 45 | 35/10 | multi-pass-compiler-pipeline |
| Event Notification & Pub-Sub | communication | 45 | 16/29 | event-connector |
| Domain Modeling & Persistence | data | 43 | 34/9 | domain-model |
| Distributed Communication & Remoting | communication | 43 | 26/17 | broker |
| Locks, Atomics & Lock-Free | concurrency | 42 | 38/4 | arbitrator-connector |
| Microservices & API Gateways | structure | 41 | 11/30 | shared-database |
| Layering & Platform Abstraction | resource | 37 | 25/12 | hardware-abstraction-layer-arch |
| State Machines & Numeric Precision | structure | 32 | 24/8 | state-transition-system |
| Deployment, Scaling & Release | resource | 31 | 3/28 | load-balancer |
| Commands & Iteration | structure | 15 | 11/4 | undo |
| Architecture Description & Views | foundations | 14 | 0/14 | architecture-view |

Each island in `atlas.json` additionally carries a one-line `blurb`, `representatives[3]`, `neighbours[]`
(weighted, → ports + sea-routes), `cohesion`, precomputed `cx/cy/r` (L0 bubble) + `hull` (L1 coastline),
and per-member `x/y` (L1 radial) — all deterministic (verified byte-identical across two builds).

---

## 5. Determinism contract (non-negotiable for a map)

A map must look **identical every session** or spatial memory is impossible. Therefore:

- **No `Math.random`, anywhere.** Every layout seeds positions from a hash of the element/island **id**
  and runs a **fixed** iteration count. Same input graph → byte-identical coordinates across builds.
- Layouts are **precomputed at build time** (`build_atlas.py`) and shipped in `data/atlas.json`; the
  browser never runs the heavy full-graph force layout — it renders shipped coordinates and only does
  cheap local work (hover, highlight, zoom transitions).
- Community detection is **deterministic** (greedy modularity / Louvain with id-ordered tie-breaks).

---

## 6. Data model — `atlas.json` (emitted by the build; consumed by the views)

```
{
  "meta":   { "atlas": "archipelago", "islandCount", "elementCount", "edgeCount",
              "families": [ { "id","name","hex" } ] },
  "islands":[ { "id", "name", "family", "size", "hub",
                "representatives": [id,id,id], "cohesion": <0..1>,
                "members":   [ { "id","name","realm","kind","family","x","y","deg" } ],
                "hull":      [ [x,y], ... ],           // island polygon at L0
                "cx","cy","r",                         // bubble centre + radius at L0
                "neighbours":[ { "island","weight" } ] // for ports + sea-routes
              } ],
  "routes": [ { "from": islandId, "to": islandId, "weight" } ],   // aggregated cross-island edges
  "bridgeFlow": { "families":[...], "anchors":[...], "flows":[ {from,to,weight} ] }  // view 11
}
```

Coordinates live in a normalized `[0,1]×[0,1]` space; the view maps them to the SVG viewport (and its
aspect) at render time. Every element appears in exactly one island's `members`; the build **fails loud**
if any element is unplaced or any route/neighbour references a missing island.

---

## 7. Interaction contract

- **Breadcrumb** `Atlas ▸ <Island> ▸ <Node>` across L0→L1→L2; each crumb is a back-target.
- **Hash state** carries atlas + island + node, so any view state is a shareable deep link and the
  browser Back button walks the zoom history.
- **Ports** (L1): one labelled marker per neighbour island; click hops (updates island crumb).
- **Minimap** (WS3-C): a tiny always-visible Archipelago with a "you are here" marker.
- **Search-teleport** (WS3-C): a query highlights matching islands at L0 and flies into the best match;
  reuses the element search index (`coreEl`).
- **Motion**: zoom/pan transitions animate, but honour `prefers-reduced-motion` (snap, no animation).
- **Honesty markers** carry into the map: edges keep their `sourced` / `editorial` / `derived`
  provenance; the L2 ego-graph already renders editorial as dotted; `derived` (computed 1C backbone)
  edges render distinctly and are toggleable. Gaps/unbridged honesty from the element layer is preserved.

---

## 8. House rules (inherited, unchanged)

Pure functional core (`core_atlas.js`) + thin SVG shell (`el_atlas.js`, `el_bridgeflow.js`); `window.SWE`
classic scripts; runs from `file://`; zero runtime dependencies; strict-JSDoc typing; global error
backstops. Page/inner scroll is authorized for element/atlas views; the five work models keep their
strict single 16:9 viewport and must not regress.
