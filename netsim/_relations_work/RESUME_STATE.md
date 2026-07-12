# netsim "typed relations + breadth" endeavour — RESUME STATE

**What:** gave the netsim explorer the SWE-parity **typed twelve-kind reading graph** over its resources, and
grew the corpus to feed it. Per `netsim/NETSIM_RELATIONS_PLAN.md`, executed 2026-07-12 under Opus 4.8
(ultrathink + ultracode). **Nothing committed — the user's call (standing rule).**

## Tab spine now
`1 Anchor · 2 Reading graph · 3 Overlays · 4 Facets · 5 Chronology · 6 MATLAB lens · 7 Triage` (keys 1–7).

## Final numbers
- **344 nodes** (was 282): GEN 238 numbered + 18 quarantine, MAT 81 + 8, 2 merges. Verification **241/78/24**
  web/train/unverified. `+62` net-new (after removing **22** scout duplicates of existing entries).
- **320 typed edges** over 235 resources, 12 kinds; **derived 29 / editorial 291**; **8 cycles**.
  Census baselines (must reconcile if you touch edges): by kind `prerequisite-of 70, refines 14, subsumes 2,
  formalizes 1, surveys 29, applies-method-of 90, companion 44, evaluates 6, critiques 3, supersedes 8,
  part-of 7, references 46`.

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

## Adversarial-review fixes (2026-07-12)
178 authored editorial edges checked: **13 flagged, all wrong-kind (0 drops, 0 reversals)**, retyped for
precision (subsumes→supersedes edition lineage; supersedes→companion for cross-level tools like Sionna vs the
system-level simulator; a 1990 survey → prerequisite-of a 2004 paper; book subsumes→surveys RESTART; MaxiNet
refines→applies-method-of Mininet; …). Re-built green. If you re-author edges, keep the kind/direction precise.
