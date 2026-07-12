# netsim "typed relations + breadth" endeavour — RESUME STATE

**What:** gave the netsim explorer the SWE-parity **typed twelve-kind reading graph** over its resources, and
grew the corpus to feed it. Per `netsim/NETSIM_RELATIONS_PLAN.md`, executed 2026-07-12 under Opus 4.8
(ultrathink + ultracode). **Nothing committed — the user's call (standing rule).**

## Tab spine now
`1 Anchor · 2 Reading graph · 3 Overlays · 4 Facets · 5 Chronology · 6 MATLAB lens · 7 Triage` (keys 1–7).

## Final numbers
- **344 nodes** (was 282): GEN 238 numbered + 18 quarantine, MAT 81 + 8, 2 merges. Verification **241/78/24**
  web/train/unverified. `+62` net-new (after removing **22** scout duplicates of existing entries).
- **395 typed edges** over 235 resources, 12 kinds; **derived 29 / editorial 366**; **13 cycles**.
  Census baselines (must reconcile if you touch edges): by kind `prerequisite-of 95, refines 14, subsumes 2,
  formalizes 1, surveys 29, applies-method-of 140, companion 44, evaluates 6, critiques 3, supersedes 8,
  part-of 7, references 46`. (Was 320 before the overlays were extended — see the view-integration note below.)

## What changed (by workstream)
- **NR0** — `build/relations_typed.py` (KINDS12, `OVERLAY_TYPED` re-expression map, `EXTRA_EDGES` 8 seeds,
  `AUTHORED_EDGES` 170 from NR1); `build/build.py` **PHASE 3.6** (assemble derived + overlay-editorial + authored,
  alias-rewrite, dedup by (s,t), quarantine-guard editorial, cycle-tag via SCC, census); emits
  `relations.{kinds,edges,cycles}`; `styles/tokens.css` 12 `--k-*` hues + `--s-fm`; `logic/util.js`
  `kindColor/KIND_DASH/corpusFill/CORPUS_ORDER` + `formal-methods` SUBF_KEY; `logic/parse.js` validates `src`.
- **NRX** — 8 new GEN sections **§17–§24** (emulation, systems-boundary, cloud/DC, learned-sim, NTN/satellite,
  PADS, rare-event/methodology, formal-methods) with items **177–238**; quarantine → **§25**, coverage → **§26**;
  `formal-methods` added to `SUBFIELDS`; count gate → `238+18 / 81+8`, `GEN_SECTION_MAP` 17–24 added +
  quarantine→25, quarantine-section constant 17→25, section-map bound `≤25`.
- **NR1** — `AUTHORED_EDGES` connect every g177–g238 node into the graph + cross-lineage edges.
- **NR2** — `logic/core.js` `graphLayout`/`typedAdjacency`/`primaryCorpus` (+ constants, ported from SWE);
  `logic/views/reading.js` (new view); `logic/app.js` VIEW_ORDER inserts `reading` + keys `1–7`; `index.html`
  script tag + eyebrow/meta; `styles/app.css` `.reading .gedge` (derived solid / editorial dotted), `.band-label`,
  `.gnode.major/.unv`, `.degm`, `.badge.kind/.ed`.
- **NR3** — `logic/inspector.js` typed-relations catalog (kind hue-chip · provenance · rationale · cycle) +
  12-kind legend + typed-edge stat; keyboard hint `1–7`.
- **Docs** — README / MODELS / ARCHITECTURE / index.html updated (seven models, typed layer, provenance grades).

## Rebuild
```
cd E:\dev\corpora\netsim\explorer\build
python build.py          # all phases green; PHASE 3.6 prints "typed edges: 320 over 235 …"
```
Two-key count gate fails loud on any report entry-count/numbering drift. View/CSS/doc edits need no rebuild.

## Verify UI (Node unavailable → headless Chrome)
```
pwsh -File E:\dev\corpora\netsim\_relations_work\verify_relations.ps1
```
Must print **ALL PASS (8 cases)**: 7 views mount, zero console errors, no backstop, reading graph renders/hovers/
filters, `view=reading&sel=g166` typed-edge deeplink resolves. NB the two Windows gotchas baked in (Start-Process
not `&`; isolated `--user-data-dir`). Screenshots: same flags with `--screenshot=<png> --window-size=3840,2160`.

## Decisions (locked, from the plan §5)
Typed relations + breadth only (NO concept/atlas layer) · provenance = `derived` + `editorial` (no `report:*`) ·
all 12 SWE kinds carried · keep the 2 overlays AND add the flat Reading graph (6→7 views) · one typed edge layer ·
breadth Substantial (~+80 → settled at +62 after dedup) · `formal-methods` fork opened lightly.

## Watch-outs for future edits
- **Dedup against the existing corpus** before adding breadth entries — the scouts (blind to the corpus)
  duplicated 22 works; a future expansion must feed the existing titles/identifiers to the scouts or dedup after.
- Editorial edges may **not** touch quarantined nodes (build fails); derived may. New authored edges go in
  `relations_typed.AUTHORED_EDGES` (all editorial-grade) and override overlay defaults on shared (s,t).
- The corpus reports are the **single source of truth**; the build parses them (no hand-transcribed data).

## View integration (2026-07-12, follow-up "update all views with the new elements")
Audit found the **data-driven views already surface all 62 new resources** automatically: Anchor map (new
§17–24 render as section cards under their parts), Facets (new subfields incl. `formal-methods`), Chronology
(strata by year), Triage split, Reading graph. MATLAB lens correctly excludes them (no new MAT). Two gaps fixed:
- **Triage** — stale hardcoded quarantine labels `GEN §16`/`MAT §8` → **§25/§9** (`views/triage.js`); added a
  "Typed-relations + breadth expansion (2026-07 wave, §17–24)" block to the GEN report §26 coverage summary
  (Triage quotes it verbatim; GEN now 6 coverage blocks).
- **Overlays** — the curated reading-maps had **zero** new elements. An overlay-extension workflow (6 lane
  agents) wove them in via a re-runnable extension block appended to `build/overlays.py` (`_DID_ADD/_DID_EDGES/
  _SPEC_ADD/_SPEC_EDGES`, merged into OVERLAYS at import): **didactic 61→83 members / 60→88 edges**,
  **specialization 65→127 members / 56→129 edges**, both still **ACYCLIC + level-monotone** (Kahn, PHASE 3.5),
  all **62/62 new nodes in ≥1 overlay**. Because the overlays seed the Reading graph (PHASE 3.6 re-expression),
  typed edges grew **320→395** (the extra prerequisite-of/applies-method-of from the new reading-map chains).
  If you re-run: `python scratchpad merge_overlays.py <overlay_output.json>` replaces the extension block idempotently.

## Adversarial-review fixes (2026-07-12)
178 authored editorial edges checked: **13 flagged, all wrong-kind (0 drops, 0 reversals)**, retyped for
precision (subsumes→supersedes edition lineage; supersedes→companion for cross-level tools like Sionna vs the
system-level simulator; a 1990 survey → prerequisite-of a 2004 paper; book subsumes→surveys RESTART; MaxiNet
refines→applies-method-of Mininet; …). Re-built green. If you re-author edges, keep the kind/direction precise.
