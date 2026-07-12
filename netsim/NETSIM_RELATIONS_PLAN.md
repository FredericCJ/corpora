# NETSIM_RELATIONS_PLAN.md — typed relations + corpus expansion for the Network M&S explorer

**Endeavour.** Bring the netsim body of knowledge up to the SWE corpus's **typed-relation standard**: a
first-class, provenance-tagged, **twelve-kind** typed relation layer between the resources, **visualized**
as a SWE-style reading graph with a per-resource edge catalog — and **grow the corpus** to feed it.

**Model:** authored under Opus 4.8 (ultrathink). **Execution** (later, on the user's word) is intended
"ultracode" — parallel author/derive + adversarial-verify workflows, exactly as the SWE BoK endeavour ran.

**Standing constraints (carried, always in effect).**
- **Nothing is committed to git unless the user explicitly instructs it.** This plan does not commit.
- **Anti-fabrication gate.** Every resource and every edge needs a citable ground: a report sentence
  (`derived`) or a maintainer rationale (`editorial`). Provenance is tagged and visible. Never fabricate a
  citation, DOI, ISBN, arXiv id, venue, or item number. Unconfirmed material is quarantined, never laundered
  into the graph.
- **House discipline.** Raw HTML/CSS/JS, zero deps, `file://`-safe, `window.NET` classic scripts; functional
  core (`core.js`, pure) + thin view shells; determinism (no `Math.random`/`Date.now`/`new Date`); global error
  backstops; strict-JSDoc. The work-model views keep the **strict single 16:9 4K viewport** (internal column
  scroll only). Both source reports remain the **single source of truth** — parsed directly by the build.

---

## 1. What exists today (grounded audit)

The explorer at `netsim/explorer/` carries **one fact layer** and **one thin inference layer** over two
directly-parsed reports. Ground truth as of this plan:

**Corpus — 282 nodes.** `1 anchor + 176 GEN(§1–16) + 18 GEN-quarantine(§17) + 81 MAT(§1–8) + 8 MAT-quarantine(§9)
− 2 cross-corpus merges`. Sources:
- `MS_networks_systems_corpus_v1_0.md` (GEN — networks & systems M&S, anchored on the 2015 Obaidat/Zarai/
  Nicopolitidis volume; 18 sections incl. §16 multi-station scheduling, §17 quarantine, §18 coverage summary).
- `MATLAB_Simulink_network_MS_corpus_v1_0.md` (MAT — the MATLAB/Simulink intersection corpus; 10 sections).
- Entry grammar (machine-regular, parsed by `ENTRY_RE`): `N. **Title** — citation \`{a | b | c | d}\` — note`,
  four tag fields (GEN `{subfield | recency | type | verification}`, MAT `{paradigm | stratum | recency |
  verification}`). Verification ∈ `verified[WEB] | verified[TRAIN] | unverified`.

**Relations — the gap.** `data/relations.js` (`NET.relations`) carries only:
- `edges`: **32** mechanical cross-references, `kinds = ["overlaps","mentions","named-in"]`, schema
  `{s,t,kind,quote}` — grounded *only* by literal `item N` references, `[GEN-CORPUS]` overlap flags, and shared
  hard identifiers. **No semantic typing** (no "supersedes", "surveys", "refines", …).
- `overlays`: **two EDITORIAL leveled reading-maps** (`build/overlays.py`) over a curated ~60-node subset each:
  **Didactic — ground up** (`edgeKind: read-before`, levels D0→D5) and **Theory → applied**
  (`edgeKind: specialized-by`, stages S0→S3). ~116 rationaled edges total, machine-validated acyclic + level-
  monotone. These are genuine typed judgment edges — but banded reading-maps, **not** a flat typed relation
  graph, and they use only **two bespoke edge kinds**.

**Views — six.** `anchor · graph(=Overlays) · facets · timeline · matlab · triage` (tab spine `1–6`, key `o`
toggles the overlay). The `graph` view renders the *overlays* (banded barycenter layout), **not** a SWE-style
typed graph. `core.js` has `visibleIds/facetCount/strataBuckets/anchorColumns/paradigmBuckets/overlayAdjacency/
closure/overlayLayout/triage/stats` — **there is no `graphLayout` shelf-packer** (that is SWE-only). The
inspector already renders per-node overlay memberships + edges (with rationale) and the 32 "derived references"
(with grounding quote) — so it is **already edge-aware**; a typed-edge catalog slots in naturally.

**Build — a direct parser with a two-key count gate.** `build/build.py`: PHASE 1 parse (fails loud if GEN≠176+18
or MAT≠81+8, or numbering non-contiguous) → PHASE 2 normalize/merge/derive-mechanical-edges → PHASE 3 structural
verify → PHASE 3.5 validate overlays → PHASE 4 emit `{corpus,relations}.{json,js}` + `corpus_report.md`.

---

## 2. The gap, and the target (SWE parity)

| Dimension | netsim now | SWE (template) | This endeavour |
|---|---|---|---|
| Typed relation vocabulary | 0 (only mechanical `overlaps/mentions/named-in`) | **12 kinds** | adopt the **same 12 kinds** |
| Edge schema | `{s,t,kind,quote}` | `{s,t,kind,src,note,cycle}` | adopt SWE's schema verbatim |
| Provenance grades | — | `report:swa/sim/proc`, `derived`, `editorial` (86/57/49/50/19) | **`derived` + `editorial`** (see §3.3) |
| Typed edge count | 32 mechanical | 261 | **~180–240** typed (density ≈ SWE's 0.56/node) |
| Relation view | Overlays (banded) | Reading graph (shelf-packed, cyclic, edge catalog) | **add a Reading-graph view** |
| Kind hues | 0 | 12 `--k-*` | carry the 12 `--k-*` hues |
| Corpus size | 282 nodes | 468 works (+1083 elements) | **grow to ~350–370** (gap-driven) |

**Explicitly out of scope** (an honest reading of the request): netsim gets **no concept/"element" layer and no
atlas.** In netsim the *resources are the elements* of the body of knowledge, and "the same relation types as
SWE" denotes SWE's **work-level 12-kind graph** — not SWE's separate element-relation set
(`realizes/enables/constrains/…`). A concept layer would triple the scope and is not what was asked; it is
recorded here as a possible **future** endeavour, not part of this one.

---

## 3. The relation-kind system for netsim (the intellectual core)

### 3.1 The twelve kinds, carried verbatim, mapped to M&S

The directed reading semantics `s → t` are SWE's, re-grounded in this corpus. Every example below is a **real
pair of existing nodes**; the plan's NR1 workstream is precisely the disciplined enumeration of such pairs.

| Kind | `s → t` means | Grounded netsim example (illustrative) |
|---|---|---|
| **prerequisite-of** | understand *s* before *t* | `g19` Intro to Probability → `g18` queueing pedagogy; `g166` Liu&Layland → `g168` Buttazzo |
| **refines** | *s* adds detail/rigor to *t*'s idea | `g27` algorithmic network calculus → `g26` network calculus; `m40` transient-perf → `m39` jitter toolbox |
| **subsumes** | *s* consolidates/generalizes *t* | `g5` ToMS 3rd ed → `g6` ToMS 2nd ed; `g9` Cassandras DES textbook → `g10` Petri-net survey |
| **formalizes** | *s* gives formal semantics to *t* | `g5` DEVS formalism → `g7` practitioner DES; `g10` Petri nets → discrete-event modeling |
| **surveys** | *s* is a survey cataloging *t* | `g2` ns-3 SLR → `g41` ns-3; `g159` Hespanha NCS survey → the NCS lineage; `g14` DEVS-tools eval → `g5/g7` |
| **applies-method-of** | *s* instantiates *t*'s method | `m4` SimEvents M/M/1 → `g16` Kleinrock; `m74` TrueTime → `g168` Buttazzo; `m81` RTC Toolbox → `g173` RTC |
| **companion** | *s* and *t* are sibling works | `g18`/`g19` Harchol-Balter pair; `m39`/`m40`; the two ToMS editions |
| **evaluates** | *s* empirically evaluates *t* | `g104` calibration study → `g103` NR simulator; `g33` TSN fidelity → `g44` OMNeT++ |
| **critiques** | *s* challenges *t* | credibility/validity works (`g35`/`g36`) → naive simulation practice; learned-sim → packet-level DES cost |
| **supersedes** | *s* replaces/obsoletes *t* | `g41` ns-3 → the anchor's ns-2 era; `g105` Sionna → MATLAB link-level tools ("displacing", report text) |
| **part-of** | *s* is a component/supplement of *t* | INET → OMNeT++; a specific 5G example → the `wirelessNetworkSimulator` stack; ITU-T/IETF DT specs → the DT effort |
| **references** | *s* cites/traceable to *t* | `g174` SymTA/S → `g173` RTC; `m80` ns3-fmi → `m41–45`; every existing `named-in`/shared-identifier edge |

Note the direct correspondences that make this a **re-expression, not an invention**:
- the Didactic overlay's **`read-before`** edges are exactly **`prerequisite-of`**;
- the Theory→applied overlay's **`specialized-by`** edges are **`applies-method-of`** / **`refines`** /
  **`subsumes`** (the finer kind chosen per pair);
- the anchor-map's literal section relations ("supersedes the anchor's ns-2 era", "modern analytical frontier",
  "did not exist at anchor time") are **report-grounded `supersedes` / `refines`** sources;
- the 32 mechanical edges become **`references`** (and a few **`part-of`**), keeping their exact grounding quote.

### 3.2 Direction, cycles, reciprocals

Directed, **cyclic-capable** (unlike the acyclic overlays). Cycles are legitimate (e.g. a
`supersedes`/`critiques` retrospective loop) and are **detected and tagged** `C1…` like SWE's four documented
cycles. Reciprocal phrasing (`evaluates` ⇄ *is-evaluated-by*) is stored one-directional and rendered both ways
in the inspector (SWE convention).

### 3.3 Provenance — the honest structural difference from SWE

SWE's edges are mostly `report:*` because the SWA/Simulink/process reports **contain typed edge lists / DAGs**.
**netsim's two reports contain no edge list** — they are collect-don't-exclude corpora of tagged entries with
prose notes. Therefore netsim's typed edges carry exactly **two grades** (a third only where a report sentence
literally states the relation):

- **`derived`** — mechanically grounded in report text: the note/citation literally states the relation
  ("3rd ed. post-dates…", "supersedes the anchor's ns-2 era", "surveys the ns-3 literature", "calibrates
  against 3GPP references"), OR a literal `item N` reference / shared hard identifier. The **grounding quote is
  stored in `note`**. This subsumes and re-types today's 32 mechanical edges.
- **`editorial`** — maintainer judgment carrying a one-line **rationale** in `note`; rendered **EDITORIAL** with a
  dotted edge, never presented as report fact. This is the class the ~116 overlay edges already live in; they are
  re-expressed into the 12-kind vocabulary, and new editorial edges complete the spine.

**Consequence, owned up front:** netsim's typed graph will be **editorial-heavier than SWE's**. The discipline
that keeps this honest: (1) maximize `derived` — mine every note the prose actually grounds before reaching for
editorial; (2) every editorial edge carries a substantive rationale and is visibly dotted/labelled EDITORIAL;
(3) the build emits a **provenance census** (per kind × per grade) so the derived:editorial ratio is always
legible; (4) **quarantined nodes may be edge endpoints only for `derived` `references` edges that the text
grounds — never for editorial reading edges** (overlays already forbid quarantined members; typed editorial
edges inherit that ban). The build machine-checks all of this.

---

## 4. Workstreams

Prefix **NR** (netsim relations). Ordered by dependency; NRX (breadth) can run in parallel with NR0.

### NR0 — Relation-model foundation *(schema · vocabulary · provenance · hues)*
- **`data` schema.** Introduce a single typed layer matching SWE: `relations.kinds = [12]`, `relations.edges`
  with `{s, t, kind, src, note, cycle}`, and `relations.cycles = [{id, note}]`. Keep the mechanical
  `overlaps/mentions/named-in` derivation **as an input** that emits `references`/`part-of` typed edges (so
  those stay grounded by their quote); the standalone mechanical block is retired in favour of the typed layer.
- **`styles/tokens.css`.** Add the 12 `--k-*` edge-kind hues (carry SWE's palette verbatim for cross-explorer
  consistency).
- **Identity (minor).** Optionally name the relational views a group in the eyebrow/README ("the literature ·
  its relations"), mirroring SWE's "Body of Knowledge" touch. Low priority; not load-bearing.
- **Deliverable:** the schema + palette exist and the build emits an (initially small) typed layer.

### NRX — Corpus expansion *(breadth; parallel with NR0/NR1)*
- **Target:** **~+70–90 resources → ~350–370 nodes**, *gap-driven, not count-driven* — stop at the natural
  ceiling per the existing wave stop-rule (the 2026-07-09 wave halted after Wave 1 at ~40 finds). Priorities from
  the reports' own coverage summaries (the thin spots they name):
  1. **hybrid fluid/packet & rare-event simulation** (GEN U12 — technique known, current survey not located);
  2. **NTN / satellite simulators** beyond SatEdgeSim/ISTN;
  3. **emulation & testbeds** at scale (Mininet/Containernet/Kathará/virtual-time correction) — thickens §7;
  4. **commercial tooling** (Riverbed Modeler, NetSim, EXata) — currently only lightly covered;
  5. **ML-for-simulation** depth (RouteNet family, MimicNet/DeepQueueNet/SplitSim line) — strong relation hub;
  6. **systems-boundary** resolution (gem5, SST, BookSim, SimGrid, CODES, AstraSim — already tagged `other(systems)`);
  7. **WSC/MASCOTS/WODES** per-paper picks where they anchor a relation (not blanket enumeration);
  8. a **light `formal-methods` cluster** (a handful of anchor works — PRISM/Storm/UPPAAL probabilistic model
     checking of protocols/schedulers), added as its own subfield (**confirmed** — see §5).
- **Method:** the same disciplined web-crawl waves as the last expansion — scout clusters, hop-limit-2 from
  seeds, first-hand keystone fetches, `verified[WEB]` where confirmed live, `verified[TRAIN]` for high-confidence
  training knowledge (identifiers flagged for re-check), **quarantine** the unconfirmed. New entries appended to
  the two reports **in the existing grammar**; new subfields added to `SUBFIELDS` only if a locked decision opens
  one. **Every new entry chosen because it also earns typed edges** (a survey, a supersession, a tool lineage) —
  breadth in service of the relation graph, not breadth for its own sake.
- **Build:** update the two-key **count gate** (`176+18 / 81+8` → the new totals) and the numbering ranges; the
  `GEN_SECTION_MAP` / quarantine-section constants shift if new sections land (the report documents this exact
  ritual).
- **Deliverable:** the corpus grows with full provenance; the build stays green and self-auditing.

### NR1 — The typed edge corpus *(the headline: author + derive the edges)*
- **New module `build/relations_typed.py`** (sibling to `overlays.py`), holding:
  - `DERIVE_RULES`: an ordered verb→kind table applied to each node's note/citation, emitting **`derived`** edges
    with the matched sentence as `note`. Sketch: `supersed|replac|displac|obsolet → supersedes`;
    `builds on|extends|refines|hardened → refines`; `survey|review|catalog|maps the … literature → surveys`;
    `consolidat|generaliz|subsumes|merges → subsumes`; `formaliz|formal semantics|calculus of → formalizes`;
    `evaluat|benchmark|calibrat|compares → evaluates`; `critiqu|argues against|too noisy|fails → critiques`;
    `applies|uses the … method|instantiat|implements the … of → applies-method-of`;
    `companion|parallel|sibling|same special issue|same author programme → companion`;
    `supplement to|part of|module of|under the … umbrella → part-of`; `precedes|underlies|foundation for →
    prerequisite-of`; item-N / shared-identifier / `[GEN-CORPUS]` → `references`. Each rule fires **only** when
    both endpoints resolve and the quote is real — no bare keyword guessing without a grounded sentence.
  - `EDITORIAL_EDGES`: hand-authored `(s, t, kind, note)` list. Seeded by **re-expressing the two overlays'
    ~116 edges** into the 12 kinds (carrying their existing rationale), then extended to complete the spine:
    the anchor's six-part lineage, the scheduling method-spine (Liu&Layland→Buttazzo→TrueTime; SimEvents→multicore
    examples), the tool families (ns-3/OMNeT++/INET; wirelessNetworkSimulator stack; DEVS lineage; NC→RTC→SymTA/S).
- **build.py — new PHASE 3.6 "typed relations"** (mirrors 3.5): merge derived + editorial + report-grounded
  edges, **alias-rewrite** through the cross-corpus merges, **dedup**, validate endpoints ∈ `byid`,
  `kind ∈ KINDS12`, `src ∈ {derived, editorial, report}`, enforce the **quarantine policy** (§3.3), **detect
  cycles** (tag `C1…`), and print the **census** (per kind, per grade, cycle count). Emits `relations.edges/kinds/
  cycles/typedViews`.
- **Target density:** **~180–240 edges**; provenance ratio surfaced (aim to keep `derived` a real share, not a
  rounding error — the derive pass is what earns that).
- **Deliverable:** a grounded, provenance-tagged, cyclic 12-kind typed relation corpus.

### NR2 — Reading-graph view *(visualization)*
- **`core.js`:** add **`graphLayout(nodes, edges, corpusOrder, {aspect})`** — port SWE's pure shelf-packing
  aspect-fit layout (group drawn nodes into `gen`/`mat` bands, size each band's grid, shelf-pack, sweep ~28
  target widths to best-match the pane aspect). Add **`typedAdjacency(edges)`** (up/down maps) and reuse the
  existing `closure`. All pure, deterministic.
- **New view `views/reading.js`** (label **"Reading graph"**): typed, directed, **cyclic-capable** SVG graph;
  node set = every resource with ≥1 typed edge (edgeless resources remain reachable via Anchor/Facets/Chronology/
  search — stated in the header, SWE's honest framing); `viewBox`-scaled to fill; `ResizeObserver` re-runs the
  pure layout (coalesced via `requestAnimationFrame`). Edges colored by kind (12 `--k-*` hues); **editorial
  dotted, derived solid**; verified[TRAIN] dashed node borders. Hover traces the cycle-safe closure both
  directions. Honors the global search/verification/corpus filters. **Strict single 16:9 viewport** (this view
  joins the work-model discipline; no page scroll).
- **`app.js` + `index.html`:** register `reading`; **VIEW_ORDER** → `['anchor','reading','graph','facets',
  'timeline','matlab','triage']` (Reading graph adjacent to Overlays — the two relation views together);
  keyboard `1–7`; keep `o` for the overlay toggle within the Overlays view.
- **Deliverable:** a 7th view rendering the typed graph in one viewport, zero console errors.

### NR3 — Inspector + cross-view wiring
- **`inspector.js`:** add a **"typed relations (N)"** catalog per selected node — kind **hue-chip** (12 colors),
  provenance grade (`derived` quote / `editorial` rationale, `EDITORIAL` marked), both directions
  (`kind` out / `is kind by` in), cycle tags. This supersedes the old "derived references" block (the mechanical
  edges now appear here as `references`). **Keep** the overlay-membership block (the leveled reading-maps remain a
  valid, distinct affordance). Overview gains a **typed-edge stat** (count + derived:editorial split) and a
  **12-kind hue legend**.
- **Anchor / Timeline / MATLAB / Triage:** unchanged (they carry no relations). Optional light touch: the Anchor
  map's section "relation" phrases could link to the typed edges they ground — deferred, not required.
- **Deliverable:** every typed edge is reachable and legible from its endpoints, with provenance visible.

### NR-verify — Verification, adversarial review, docs *(gate to "done")*
- **Build green:** `python build/build.py` all phases pass; new count gate holds; PHASE 3.6 prints the typed-edge
  census; JSON/JS twins byte-deterministic across two runs.
- **Headless-Chrome smoke** (the two Windows gotchas baked in — `Start-Process -Wait -RedirectStandardOutput`,
  isolated `--user-data-dir`): all **7** views mount, **zero console errors**, no failure backstop; the reading
  graph renders + hovers (closure) + respects filters; hash round-trips; **single 16:9 viewport** confirmed at
  3840×2160 on the work-model views (reading graph included); prior views unregressed.
- **State-discipline check:** confirm `netsim/logic/state.js` uses a **diff-based hashchange handler** (the
  property SWE's BoK fix established — self-write emits only changed keys, external nav diffs). If it still relies
  on a mute-flag, fix it (this bug silently remounts the active view). *(The README claims netsim inherited the
  calculus state fix — verify, don't assume.)*
- **Adversarial review (mirror SWE's 5 lenses):** (1) **anti-fabrication** — every edge grounded or rationaled;
  no fabricated citation/identifier in new resources; quarantine policy holds; (2) **kind-soundness** — does the
  quote/rationale actually support the assigned kind and direction? spot-check derived-rule false positives;
  (3) **determinism** — no forbidden time/random; stable output; (4) **single-viewport** — reading graph fits,
  no page scroll; (5) **provenance honesty** — the derived:editorial ratio is disclosed and not gamed.
- **Docs:** `README.md` (7 views, typed relation layer, new counts), `MODELS.md` (the Reading-graph model + the
  §3 kind system + provenance grades), `ARCHITECTURE.md` (schema, `graphLayout`, PHASE 3.6). An
  `EXPANSION_REPORT_<date>_relations.md` + `netsim/_relations_work/RESUME_STATE.md` + a durable
  `verify_relations.ps1` harness (SWE pattern).

---

## 5. Locked decisions & open forks

**Locked (my recommendation — the user may veto any before "execute"):**
1. **Scope = typed relations + breadth only.** No concept/element layer, no atlas. netsim resources *are* the
   elements; SWE's "relation types" are its 12-kind work-graph. (See §2.)
2. **Provenance = `derived` + `editorial`** (plus report-grounded `derived` from the anchor-map/coverage
   sentences). **No `report:*` grade** — netsim's reports carry no edge list. Owned honestly (§3.3).
3. **Carry all 12 SWE kinds verbatim** (even rare ones like `critiques`), for cross-explorer parity.
4. **Keep the two editorial overlays as their own leveled view; ADD a flat typed Reading-graph view** (6 → 7
   views). The overlays seed NR1's editorial edges but are not discarded — leveled reading-maps are a distinct,
   valuable affordance.
5. **One typed edge layer** (`relations.edges`, SWE schema) — the mechanical `mentions/overlaps/named-in` become
   grounded `references`/`part-of` typed edges, not a separate block.
6. **Breadth is gap-driven** (§NRX priority list), halting at the natural ceiling per the wave stop-rule.

**Confirmed by the user (2026-07-12):**
7. **Breadth = Substantial, ~+80 → ~350–370 nodes.** Close the named coverage gaps *and* thicken the relation
   graph (surveys, supersession chains, tool lineages) — depth-per-cost over raw count.
8. **Open the `formal-methods` fork lightly.** Add a small anchor cluster (PRISM/Storm/UPPAAL probabilistic
   model checking of protocols/schedulers) as its own `formal-methods` subfield — a coherent group that earns
   typed edges, without turning formal verification into a first-class expansion axis.

**Remaining open fork (my call unless you say otherwise):**
- **C. Identity polish.** Name the relational views a group (SWE-style eyebrow/tab divider) — cosmetic; *default:
  a light touch, decided at execution time.*

---

## 6. Method (ultracode, when executed)

Mirror the SWE BoK structure: **foundation in the main context** (NR0 schema/palette; `core.graphLayout`;
`relations_typed.py` scaffolding + the derive pass; the Reading-graph view + inspector — the two hard, shared-file
pieces), then **two workflows**:
1. **Author/derive fan-out** — parallel agents each owning a *cluster* of the corpus (scheduling spine, tool
   lineages, DEVS/queueing canon, wireless stack, DT/ML frontier), proposing grounded typed edges **as structured
   output** `{s,t,kind,src,note}`; a central merge dedups and validates (no file-write races — edges return as
   data, the build owns emission). NRX breadth crawls run as their own scout clusters in the same fan-out.
2. **Adversarial-verify fan-out** — the 5 lenses of NR-verify, each an agent trying to break a property
   (fabricated ground, wrong kind/direction, non-determinism, viewport, provenance gaming). Findings fixed +
   re-verified centrally. Headless-Chrome smoke + 4K screenshots done centrally (Node unavailable).

Scale to the ask: a thorough typed-relation build over a ~360-node corpus warrants a real finder pool + a
3–5-vote adversarial pass on the editorial edges (the fabrication-risk surface). Determinism and the single
source-of-truth reports make the whole thing resumable.

---

## 7. Verification plan (what "done" means)

- `python build/build.py` — all phases green, count gate holds, PHASE 3.6 census printed, output deterministic.
- `pwsh -File netsim/_relations_work/verify_relations.ps1` — **ALL PASS**: 7 views mount, zero console errors,
  reading graph renders/hovers/filters, hash round-trips, single 16:9 viewport, prior views unregressed.
- Adversarial review clean or all findings fixed + re-verified. Anti-fabrication: **0 ungrounded edges**, **0
  fabricated identifiers**, quarantine policy intact, derived:editorial ratio disclosed.
- Docs updated and accurate (counts self-verify against the build census).

---

## 8. Anti-fabrication discipline (the non-negotiable)

Every edge is either `derived` (a real quoted report sentence / real `item N` / real shared identifier in `note`)
or `editorial` (a substantive maintainer rationale in `note`, rendered EDITORIAL + dotted). Every **new resource**
is `verified[WEB]` (fetched live), `verified[TRAIN]` (high-confidence, identifiers flagged for re-check), or
**quarantined** — never a fabricated citation. The build **fails loud** on ungrounded edges, unknown kinds,
unresolved endpoints, quarantine-policy violations, and count-gate drift. Honesty markers are preserved and
extended: `verified[WEB]/[TRAIN]/unverified`, quarantine badges, `EDITORIAL` dotted edges, per-edge grounding
quotes/rationales, the provenance census.

---

## 9. Deliverables & resume artifacts

- Grown corpus in the two reports (full provenance); regenerated `data/{corpus,relations}.{json,js}` +
  `corpus_report.md`.
- `build/relations_typed.py`; `core.graphLayout`/`typedAdjacency`; `views/reading.js`; 12 `--k-*` hues; typed-edge
  inspector catalog; `app.js`/`index.html` wiring for 7 views.
- Updated `README.md` / `MODELS.md` / `ARCHITECTURE.md`.
- `netsim/EXPANSION_REPORT_<date>_relations.md`, `netsim/_relations_work/RESUME_STATE.md`,
  `netsim/_relations_work/verify_relations.ps1`.
- A memory-state file mirroring the SWE endeavour states.
- **Nothing committed** — the user's call.

## 10. Dependency sketch

```
NR0 (schema+hues) ─┬─► NR1 (typed edges) ─► NR2 (reading view) ─► NR3 (inspector) ─► NR-verify
                   │                          ▲
NRX (breadth) ─────┴──────────────────────────┘   (more nodes → more edges; run in parallel, reconcile at NR1)
```
