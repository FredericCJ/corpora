# Expansion report — typed relations + corpus breadth for the Network M&S explorer

**Date:** 2026-07-12 · **Model:** Opus 4.8 (ultrathink + ultracode) · **Plan:** `netsim/NETSIM_RELATIONS_PLAN.md`
**Status:** delivered & verified. **Nothing committed — the user's call (standing repo rule).**

## What this endeavour did

The netsim explorer previously wired its resources with only **mechanical cross-references** (32
`overlaps/mentions/named-in` edges) plus two banded EDITORIAL overlays. This endeavour gave it the
**SWE-parity typed relation layer** the user asked for — a directed, cyclic-capable, **twelve-kind**
reading graph with a per-resource edge catalog — and **grew the corpus** to feed it. Tab spine now:

> **1 Anchor · 2 Reading graph · 3 Overlays · 4 Facets · 5 Chronology · 6 MATLAB lens · 7 Triage**
> (seven relational models; the Reading graph is the new typed layer.)

## Headline numbers

- **Corpus:** 282 → **344 nodes** (+62 net-new). GEN numbered **176 → 238**; MAT unchanged (81+8);
  quarantine unchanged (GEN 18 / MAT 8); 2 cross-corpus merges. Verification split
  **179/78/24 → 241/78/24** web/train/unverified (all 62 new entries are `verified[WEB]`).
- **Typed relations:** **320 edges over 235 of 344 resources**, across all twelve kinds
  (`prerequisite-of` 70, `applies-method-of` 90, `companion` 44, `references` 46, `surveys` 29,
  `refines` 14, `supersedes` 8, `part-of` 7, `evaluates` 6, `critiques` 3, `subsumes` 2,
  `formalizes` 1). Provenance **derived 29 / editorial 291** — honestly editorial-heavy (these reports
  carry no edge list; see §3.3 of the plan). **8 cycles** tagged.

## Workstreams

- **NR0 — foundation.** SWE edge schema `{s,t,kind,src,note,cycle}` + the 12 kinds; `build/relations_typed.py`
  (overlay re-expression map + authored-edge lists); **PHASE 3.6** assembles/validates/cycle-tags the typed
  layer and prints a per-kind × per-grade census; 12 `--k-*` hues in `tokens.css`; `util.kindColor`; `parse.js`
  validates `src`.
- **NRX — breadth (+62).** Eight **web-grounded scout clusters** (emulation, systems-boundary, cloud/DC,
  learned-sim, NTN/satellite, PADS, rare-event/fluid methodology, formal methods) proposed **103** candidate
  works — every one web-verified with a real identifier. Merged as **8 new GEN sections §17–§24** (quarantine →
  §25, coverage → §26); a new **`formal-methods`** subfield opened the deferred model-checking fork lightly.
- **NR1 — typed edges.** Six per-lane authoring agents connected **every new node** into the graph and added
  cross-lineage edges (surveys→tools, later→earlier, applied→theory): **170** authored edges, all twelve kinds
  populated.
- **NR2 — Reading-graph view.** `core.graphLayout`/`typedAdjacency` (ported from SWE, pure/deterministic,
  aspect-fitted shelf-pack) + `views/reading.js` (kind-hued edges, editorial dotted, cycle-safe closure on
  hover, `ResizeObserver`, strict single viewport). Registered as view 2 (7 views; keys `1–7`).
- **NR3 — inspector.** A per-resource **typed-relations catalog** (kind hue-chip · provenance · rationale ·
  cycle tag, both directions) + a 12-kind legend and typed-edge stat.
- **Docs.** README / MODELS / ARCHITECTURE / index.html updated (seven models, the typed layer, the two-grade
  provenance model, the honest "editorial-heavy, no report edge-list" note, new counts).

## Method (ultracode)

Foundation (schema, `graphLayout`, `relations_typed.py`, the Reading-graph view + inspector — the shared-file
pieces) in the main context; then **three background workflows** — (1) an 8-agent breadth scout with web
verification, (2) a 6-lane edge-authoring fan-out (structured output), and (3) a 6-agent adversarial
edge-soundness pass — with all report/data merges done centrally to avoid file-write races.

## Verification

- **Build green** — `python build/build.py` all phases pass; the two-key count gate + section-map ritual updated
  (GEN 238+18); PHASE 3.6 census printed; deterministic output.
- **Headless-Chrome smoke: 8/8 PASS** (`_relations_work/verify_relations.ps1`) — all 7 views mount, **zero
  console errors**, no backstop, the reading graph renders + hovers + filters, the typed-edge deeplink resolves,
  hash round-trips; 4K screenshots confirm the strict single 16:9 viewport.
- **Duplicate remediation (integrity catch).** The scouts, not given the existing corpus, re-proposed **22 works
  already present** (Mininet, gem5, SST, BookSim, SimGrid, ROSS, CODES, CloudSim/Plus, iFogSim, EdgeCloudSim,
  LEAF, RouteNet-Erlang/Fermi, ns3-gym/ai, Jefferson Virtual-Time, …). Detected by identifier/title match,
  **removed**, and the NR1 edges **remapped** onto the canonical existing ids (the agents had helpfully authored
  edges to both). Net breadth honestly settled at **+62**, not +84.
- **Adversarial edge review.** All **178** authored editorial edges checked for kind/direction soundness:
  **13 flagged, all `wrong-kind` (0 drops, 0 reversals)** — every authored edge is a real relation; the 13 were
  retyped for precision (e.g. Sionna→wirelessNetworkSimulator `supersedes`→`companion` since Sionna is
  link-level not system-level; a 1990 survey can't `survey` a 2004 paper → `prerequisite-of`; Rubino-Tuffin book
  `subsumes`→`surveys` RESTART). Re-built green after fixes.
- **State discipline.** `logic/state.js` already uses the diff-based hashchange guard (self-write emits nothing;
  only external nav re-enters) — verified, not assumed.

## View integration (follow-up)

A follow-up pass ensured **all seven views surface the new elements**. The five data-driven views (Anchor map,
Facets, Chronology, Triage split, Reading graph) already did so automatically — confirmed by 4K screenshots (new
§17–24 render as Anchor cards; `formal-methods` and the new subfields appear in Facets; new entries populate the
result lists). MATLAB lens correctly excludes them (no new MAT). Two gaps were closed: **Triage** stale quarantine
labels (`§16`/`§8` → `§25`/`§9`) plus a "2026-07 expansion" block appended to the GEN coverage summary; and the two
**EDITORIAL overlays**, which are a curated subset and contained none of the new elements — an overlay-extension
workflow (6 lane agents) wove all **62/62** new nodes into the reading maps as level-monotone, acyclic chains
(**didactic 61→83, specialization 65→127 members**; PHASE 3.5-validated). Because the overlays seed the Reading
graph, typed edges grew **320 → 395**. Smoke re-run **8/8 PASS**.

## Anti-fabrication discipline

Every new resource is `verified[WEB]` (a real, fetched work with a real identifier) — nothing fabricated; the
duplicate sweep further guarantees no phantom entries. Every typed edge is `derived` (a real quoted
cross-reference) or `editorial` (a substantive rationale, rendered dotted + EDITORIAL); the build **fails loud**
on ungrounded/unknown-kind/unresolved edges and on any editorial edge touching a quarantined node; the
derived:editorial ratio is disclosed by the census. Honesty markers preserved and extended: verified grades,
quarantine badges, `EDITORIAL` dotted edges, per-edge notes, cycle tags.

## Build & rebuild

`cd explorer/build && python build.py` — all phases green. UI verify: `pwsh -File
netsim/_relations_work/verify_relations.ps1` → **ALL PASS (8)**. Resume/rebuild details in
`netsim/_relations_work/RESUME_STATE.md`.
