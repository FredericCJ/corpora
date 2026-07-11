# BoK endeavour — RESUME STATE

**What:** modernization of the five historic work-model views into the named **"Body of Knowledge"** group,
per `SWE/BOK_PLAN.md`. Built on the ELEMENT mission + ATLAS endeavour (see those RESUME_STATEs). Executed
2026-07-11 under Opus 4.8 (ultrathink + ultracode). **Nothing committed — the user's call (standing rule).**

## Tab spine now
`body of knowledge` (1 Reading graph · 2 Facets · 3 Chronology · 4 Overlap · 5 Anchors) · `elements` (6–9) · `atlas` (10–11).

## What changed (by workstream)
- **WV0 identity** — `logic/app.js` adds the `body of knowledge` tab-sep before view 1 (+ `.tabs .tab-sep:first-child`
  flush rule in `app.css`); `index.html` eyebrow now reads "body of knowledge → elements → atlas".
- **WVX build/data** — `build/build_elements.py` derives a per-element `year` + `yearSource` via the waterfall
  `named_in "(YYYY)"` → `named_in_corpus_id` year → earliest covering-work year → UNRESOLVED, and emits new
  `meta` fields (`datable`, `undated`, `yearSources`, `decadeHist`, `worksReferenced`, `worksCorpus`, `worksPass8Only`).
  Result: **994/1083 datable**, 89 UNRESOLVED; **0 work-year discrepancies** (corpus authoritative over pass-8).
- **WV3 Chronology → two modes** — `logic/views/timeline.js` rewritten. `bok` (default) unions the 468 reading-corpus
  works with the **336 pass-8-only** works (`·p8`, dashed stripe) → **804** by year of last publication (LIVING +
  UNRESOLVED strata). `elements` buckets the **1083** elements by derived year (realm-tinted stripe, no LIVING).
  Mode round-trips through `state.tlmode` (hash deep-link). `core.js` gained `ELEMENT_STRATA` / `elementStratumOf`
  / `elementStrataBuckets`. `state.js` KEYS gained `tlmode`. `app.js` dispatch re-renders on `tlmode` change.
- **WV1 Reading graph** — `logic/views/graph.js`: reframed as "the major works" (the **258** with a typed reading
  relation; **210** edgeless reachable via Chronology/Facets/search — stated in the header). Anchors (★, accent) +
  core/survey emphasized; `◇N` marks the **81** works that ground N elements (max 109 = Software Architecture in
  Practice). Per-band **≤100 guard** (`capBands`, deterministic, surfaced; non-binding today — max band 76).
- **WV2 Facets** — `logic/views/facets.js`: per-row **"teaches N"** chip (→ inspector), **"N of 468 match"** +
  reachability assurance, and a view-level **teaches: design/architecture/none** facet (no core mutation).
- **WV4 Overlap** — `logic/views/overlap.js`: matrix/signatures verified current (82 multi-corpus); `◇N` element
  marker on multi-corpus rows.
- **WV5 Anchors** — `logic/views/anchors.js`: verified current; a footer bridges to the **atlas island hubs** as the
  concept-layer analogue of anchors (guarded by `ctx.atlas`).
- **Cross-layer nav** — `logic/inspector.js` gained `renderWork(wid)`: clicking a `·p8` chip now opens a pass-8 work
  card listing the elements it grounds → element → atlas. New render() branch orders element → corpus → pass-8 work.
- **Docs** — `README.md`, `MODELS.md`, `ARCHITECTURE.md` updated (BoK group, two chronology modes, major-works, build emit).

## Rebuild
```
cd E:\dev\corpora\SWE\explorer\build
python build.py          # 5 phases; PHASE 4 now prints "element chronology: 994/1083 datable …"
```
All phases must be green (self-audits fail loud). Data emitted to `explorer/data/*.js|json`; view/CSS/doc edits need no rebuild.

## Verify UI (Node unavailable → headless Chrome)
```
pwsh -File E:\dev\corpora\SWE\_bok_work\verify_bok.ps1
```
Must print **ALL PASS (11 cases)**: 11 views mount, zero console errors, no backstop, the two chronology modes +
deep-link resolve, prior element/atlas views 6–11 unregressed. NB the two Windows gotchas baked into the harness
(Start-Process not `&`; isolated `--user-data-dir`). Screenshots: same flags with `--screenshot=<png> --window-size=3840,2160`.

## Decisions (locked, from BOK_PLAN.md §4)
Body of Knowledge name · reading-graph = 258 relation-works (majors emphasized) · BoK chronology = full 804 (·p8) ·
element date = named_in→corpus-id→earliest-work→UNRESOLVED · element-teach counts everywhere, views stay work-centric ·
Anchors folded into the group.

## Baselines that self-verify
BoK strata sum = 804 (29+26+96+148+173+62+205+65). Elements strata sum = 1083 (38+35+177+395+169+180+89 = 994 + 89).
worksReferenced 417 = 81 corpus + 336 pass-8-only.

## Verification & adversarial-review fixes
Headless-Chrome smoke **11/11 PASS** (zero console errors, no backstop, views 6–11 unregressed, both
chronology modes + deep-link). A 5-lens adversarial review passed WV3+years and WV1 graph **clean** and
surfaced 3 defects, all fixed + re-verified:
- **MAJOR `state.js`** — the `muted` re-entrancy flag was ineffective (`hashchange` is async; the flag was
  reset synchronously before it fired), so every `set()` re-emitted ALL keys → the active view remounted on
  every change. Replaced with a **diff-based hashchange handler** (self-write → no emit; back/forward → only
  changed keys). Empirically re-tested via `scratchpad/test_state*.html` (self-write → `["q"]`; external nav
  → `["q|view"]`). If you touch state dispatch, keep this property.
- **MINOR** Space-key activation added to `role=button` rows/cards in overlap.js & anchors.js (were Enter-only).
- **DOCS** stale figures fixed: README 399→417 & census 1132→2811; MODELS "Nine/two"→"Eleven/three" & 1132→2811;
  ARCHITECTURE 421→468 & 204→261 (×2).
