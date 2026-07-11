# Expansion report — the "Body of Knowledge" (historic work-model views modernized)

**Date:** 2026-07-11 · **Model:** Opus 4.8 (ultrathink + ultracode) · **Plan:** `SWE/BOK_PLAN.md`
**Status:** delivered & verified. **Nothing committed — the user's call (standing repo rule).**

## What this endeavour did

The explorer carried three layers built in prior endeavours: the **works** (5 historic views), the
**elements** (views 6–9), and the **atlas** (views 10–11). This endeavour modernized the five historic
views, gave them a name — **Body of Knowledge** — and wired them to everything since built (1083
elements, 2811 relations). Tab spine now:

> **Body of Knowledge** (1 Reading graph · 2 Facets · 3 Chronology · 4 Overlap · 5 Anchors) · **Elements** (6–9) · **Atlas** (10–11)
> = *the literature · the concepts · the map*.

## Workstreams

- **WV0 — group identity.** A `body of knowledge` tab-group divider before view 1 (mirroring the
  `elements`/`atlas` dividers, flush at the strip start); eyebrow now reads "body of knowledge → elements → atlas".
- **WVX — build/data foundation.** `build/build_elements.py` derives a per-element `year` + `yearSource`
  via the waterfall **named_in "(YYYY)" → named_in_corpus_id year → earliest covering-work year → UNRESOLVED**,
  and emits new `meta` (datable, undated, yearSources, decadeHist, worksReferenced, worksCorpus, worksPass8Only).
  Result: **994 / 1083 datable** (959 named_in · 32 earliest-work · 3 corpus-id), **89 UNRESOLVED**; the
  81 works shared between the corpus and element layers reconcile with **0 year discrepancies** (corpus authoritative).
- **WV3 — Chronology → two modes** (the largest change). A segmented control (`state.tlmode`, hash deep-link):
  - **Body of Knowledge** — the whole referenced literature: **468** reading-corpus works ∪ **336**
    pass-8-only works (marked **·p8**, dashed stripe) = **804**, by year of last publication (LIVING +
    UNRESOLVED strata). Columns self-verify: 29+26+96+148+173+62+205+65 = **804**.
  - **Elements** — the **1083** design & architecture elements by derived concept year, realm-tinted
    stripe, no LIVING stratum. Columns: 38+35+177+395+169+180+89 = **1083** (994 datable + 89 UNRESOLVED).
  Clicking a `·p8` chip opens a new inspector **pass-8 work card** listing the elements it grounds →
  element → atlas, closing the work→elements→atlas loop.
- **WV1 — Reading graph → "the major works."** The **258** works standing in a typed reading relation
  (of 468); anchors (★, accent border) + core/survey emphasized; **◇N** marks the **81** works that ground
  N elements (max 109 = *Software Architecture in Practice, 4th ed.*). A deterministic **≤100-per-band guard**
  (surfaced, never silent; non-binding today — max band 76). The 210 edgeless works are reachable via
  Chronology, Facets, and search (stated in the header).
- **WV2 — Facets.** Per-row **"teaches N"** chip → inspector; **"N of 468 match"** + an explicit
  reachability assurance; a view-level **teaches: design / architecture / none** facet (no core mutation).
- **WV4 — Overlap.** Matrix + signatures verified current (82 multi-corpus works); **◇N** element marker
  on multi-corpus rows. Matrix semantics unchanged.
- **WV5 — Anchors.** Per-corpus anchors verified current; a footer bridges to the **atlas island hubs**
  as the concept-layer analogue of anchors (guarded by `ctx.atlas`).
- **Docs.** README / MODELS / ARCHITECTURE updated (BoK group, two chronology modes, major-works, build emit).

Every Body-of-Knowledge view now surfaces element-teach counts and routes into the element/atlas layers,
while staying work-centric (full element facets remain in view 6).

## Method (ultracode)

Foundation (build emit, core helpers, state key, WV0, and the two hard views WV1/WV3 + inspector) done in
the main context; then **two workflows**: (1) a 4-agent **implement** fan-out for the independent lighter
views + docs (each owned one file, returned its CSS, merged centrally — zero file conflicts), and (2) a
5-lens **adversarial verify** fan-out that tried to break correctness/discipline. Headless-Chrome smoke +
4K screenshots done centrally (Node unavailable).

## Verification

- **Headless-Chrome smoke: 11/11 PASS** — every view mounts, **zero console errors**, no failure backstop,
  the two chronology modes + a `tlmode=elements&sel=…` deep-link resolve, and the prior element/atlas views
  6–11 are unregressed. 4K screenshots confirm the strict single 16:9 viewport on all five BoK views.
- **Adversarial review (5 lenses).** WV3+year foundation and WV1 graph passed **clean**. Three defects were
  found and **fixed**:
  1. **MAJOR — `state.js` mute-flag was ineffective.** `hashchange` fires *asynchronously*, so the
     synchronous `muted=false` reset let every `set()` re-emit **all** keys → the active view remounted and
     the inspector re-rendered on every filter/selection/toggle (losing graph hover/pan, column scroll).
     Reproduced empirically (`set({q})` emitted `["q"]` **then** the full key set). Replaced the flag with a
     **diff-based hashchange handler** (a self-write diffs to nothing; back/forward emits only changed keys).
     Re-tested: self-write → one `["q"]` emit; external nav → `["q|view"]` only. *(Pre-existing bug; it
     degraded the new views too, so it was fixed.)*
  2. **MINOR — Space-key activation** missing on `role="button"` rows/cards in Overlap & Anchors (Enter-only). Fixed.
  3. **DOC accuracy** — corrected stale/wrong figures (README 399→417 works & census 1132→2811; MODELS
     "Nine…two layers"→"Eleven…three layers" & 1132→2811; ARCHITECTURE 421→468 & 204→261).

## Build & rebuild

`cd explorer/build && python build.py` — all 5 phases green (self-audits fail loud). PHASE 4 now prints
`element chronology: 994/1083 datable …`. UI verify: `pwsh -File SWE/_bok_work/verify_bok.ps1` → **ALL PASS (11)**.

## House discipline

Pure core + thin shells, `window.SWE` classic scripts, `file://`-safe, zero deps, strict-JSDoc, global error
backstops, determinism (no `Math.random`/`Date.now`). Honesty markers preserved and extended (UNRESOLVED,
**·p8**, sourced/editorial, ★ anchor, ◇N teach, `yearSource`). The five BoK views keep the strict single
16:9 viewport; views 6–11 unregressed. Durable/resumable under `SWE/_bok_work/`.
