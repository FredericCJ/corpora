# BOK PLAN — modernizing the historic work-model views (the "Body of Knowledge")

**Status:** planning. **Author:** drafted 2026-07-11. **Prereqs:** the ELEMENT-layer mission and the
ATLAS endeavour are complete — the explorer now carries three layers: the **works** (5 historic views,
tabs 1–5), the **elements** (views 6–9), and the **atlas** (views 10–11). This endeavour modernizes the
five historic views and wires them to everything since built (1083 elements, 2811 relations).

---

## 0. The group's name — **Body of Knowledge** (BoK)

The five historic views (Reading graph · Facets · Chronology · Overlap · Anchors) all navigate the
**referenced literature** — the books, papers, standards and documents that constitute the field's
*body of knowledge*. The user already uses "BoK" for the chronology's book mode, so the name is native
to the material. It gives the tab bar a clean tripartite spine:

> **Body of Knowledge** (1–5) · **Elements** (6–9) · **Atlas** (10–11)

= *the literature · the concepts · the map*. Implementation: a tab-group divider labelled
`body of knowledge` before view 1 (mirroring the existing `elements` / `atlas` dividers), plus copy
updates in the header eyebrow and docs. (Alternatives if you prefer shorter: "The Library", "The
Canon", "Works", or the compact divider "BoK". The user listed a 4-view subset [graph, facets,
chronology, overlap]; this plan treats all **five** contiguous tabs as one named group and folds
Anchors in — flag if you want Anchors split out.)

---

## 1. Empirical baseline (measured, not assumed)

| fact | value | implication |
|---|---|---|
| works in corpus (passes 1–7) | **468** · 261 typed edges · 12 kinds · 7 corpora | the historic dataset |
| works drawn in the reading graph (have ≥1 edge) | **258**; **210 are edgeless** → invisible | the graph shows barely half the corpus |
| reading-graph band sizes (drawn, by primary corpus) | swa 74 · sim 51 · proc 47 · cpp 27 · arch 24 · ops 18 · c 17 | **max 74 < 100** — the ≤100/group cap is a *ceiling*, not a cut |
| "major work" signals (role) | **anchor 92 · core 102 · advanced 52 · survey 21** | a defensible "major pieces" definition already in the data |
| facet-thin works (no branch AND no theme) | **0** | every work is already reachable in Facets (empty selection + paging) |
| chronology (BoK) year status | 260 dated · 145 living · 63 UNRESOLVED | BoK mode data is healthy (current behaviour) |
| elements | **1083** (709 design + 374 arch) | the Elements-mode dataset |
| **elements datable** (named_in "(YYYY)" → corpus-id → earliest covering work) | **977 / 1083 = 90 %**, range **1950–2026**, 106 undated | Elements chronology is very feasible (106 → an honest UNRESOLVED stratum) |
| element decade curve | 1960:14 · 70:23 · 80:30 · 90:176 · 2000:377 · 2010:178 · 2020:178 | a real history of the field's concepts |
| works referenced by elements | **417**; only **81 in the 468 corpus**, **336 element-only (pass-8)** | the *full* body of knowledge is ~**804** works; the historic views see only 468 |

**Reading.** The historic views are structurally sound but (a) the reading graph hides 210 works, (b)
nothing references the element layer, (c) the chronology is single-mode, and (d) the "body of knowledge"
is really ~804 works, not 468. This endeavour fixes coverage, adds the element bridge, and gives the
chronology its two modes.

---

## 2. Workstreams

### WV0 — Group identity (small)
Add the `body of knowledge` tab-group divider before view 1 (`app.js`, like the `elements`/`atlas`
dividers); refresh the header eyebrow copy to name the three layers; document the group in
`README.md` / `MODELS.md` / `ARCHITECTURE.md`. **Acceptance:** the tab bar reads BoK · Elements · Atlas;
docs name the group.

### WV1 — Reading graph → "the major works in software architecture & design"
- **Define "major"** (decision §D2): recommend **works with ≥1 typed reading relation** (the 258 that
  *have* a place in the reading structure) **with anchor/core/survey emphasized**, so the graph is the
  map of works-that-relate rather than an index. Optionally tighten to anchor∪core∪survey (~194) if you
  want a sparser canon.
- **Grouping & cap:** keep the **7 corpus bands** (the domain grouping); enforce a **≤100 per band**
  guard (currently non-binding; curate by significance if a band ever exceeds it) — surface the guard so
  a future overflow is visible, not silently truncated.
- **Element bridge:** annotate each node with the count of **elements it teaches** (pass-8), and let
  selection drive the existing work→elements inspector path. Optionally size/tint by element-density.
- **Keep** the typed edges, cycle-safe closure on hover, provenance styling, single-viewport SVG.
- **Acceptance:** every band ≤100; major works visibly emphasized; a node's element-teach count shown;
  208-ish edges render; the 210 edgeless works are reachable elsewhere (Facets/Chronology/search) and
  that is stated in the header; zero console errors.

### WV2 — Facets — completeness + the element bridge
- **Verify reachability:** confirm all 468 works are reachable (0 facet-thin already; the paging
  "show more" walks the full match set). Add an explicit **"N of 468 reachable"** assurance and make
  sure no facet combination can strand a work that has the value.
- **Freshen vocab:** confirm branches/themes/lang/type/role/lane/scope reflect the current build (incl.
  pass-7 `swe-process` `lang` facet).
- **Element bridge (decision §D5):** add a per-row **"teaches N elements"** chip (click → inspector),
  and optionally a facet **"teaches: design / architecture / none"** so the literature is filterable by
  whether (and what) it grounds in the element layer.
- **Acceptance:** result count reads against 468; every work reachable; element-teach surfaced per row;
  zero console errors.

### WV3 — Chronology → two modes (**BoK** / **Elements**)
- **Mode toggle** in the view head (segmented control; state in the hash, e.g. `tlmode=bok|elements`).
- **BoK mode** — chronology of the referenced literature. **Scope (decision §D3):** recommend the
  **full ~804 referenced works** (468 corpus + 336 element-defining pass-8), pass-8-only works clearly
  marked (`·p8`), so it is faithful to "documents referenced in the SWE corpus"; fall back to 468-only
  if you prefer. Decade strata + LIVING + UNRESOLVED (unchanged mechanics).
- **Elements mode** — chronology of the **1083 design & architecture elements** by their derived year
  (**build emits `year` + `yearSource` per element**, decision §D4: `named_in` "(YYYY)" → `named_in_
  corpus_id` year → earliest covering-work year → UNRESOLVED). Chips tinted by realm (design/arch),
  click → the element inspector detail; 106 undated → an honest UNRESOLVED column.
- **Single viewport:** decade columns with internal scroll (Elements 2000s ≈ 377 → a tall scroll column,
  same pattern as today). **Acceptance:** both modes render; toggle + hash deep-link work; Elements mode
  shows ~977 dated across decades + 106 UNRESOLVED; clicking an element opens its detail; zero errors.

### WV4 — Overlap — verify & refresh
- Confirm the cross-corpus matrix + signature groups reflect the current merge (multi-corpus works, the
  `lead`-membership chips). **Optional element lens (decision §D5):** a small note / toggle for works
  that co-teach elements. Keep the view work-centric.
- **Acceptance:** matrix totals match the current build; signatures current; zero errors.

### WV5 — Anchors — verify & refresh
- Confirm per-corpus anchors (role:anchor, non-lead) and the explicit `NO_ANCHOR` explanations are
  current. **Optional bridge:** a pointer from the anchors view to the **atlas island hubs** ("element
  anchors") as the concept-layer analogue. **Acceptance:** anchor counts match the build; explanations
  current; zero errors.

### WVX — Cross-cutting: "reference the relations and elements across the corpus"
- **Build emit:** element `year`/`yearSource` (WV3) in `build_elements.py`; if BoK spans 804, emit a
  unified/mergeable works list (or union in-view from `corpus` + `elements.works`).
- **Consistent work identity:** the 81 works shared between the corpus and the element layer must show
  identical title/year/authors; reconcile any drift.
- **Cross-layer nav everywhere:** every BoK view that shows a work surfaces its element-teach count and
  routes through the existing inspector (work→elements→atlas). The inspector already does the detail;
  the views add the entry points.

### WV-verify — verification (Node unavailable → headless Chrome)
`python build/build.py` clean, all phases green. Headless-Chrome `--dump-dom`/`--enable-logging` over a
served copy: all views mount, **zero console errors**; reading-graph bands ≤100 with element counts;
Facets reaches 468; Chronology both modes + toggle + deep-link; Overlap/Anchors current; **the element &
atlas views (6–11) unregressed**; the five BoK views keep the strict single 16:9 viewport (no page
scroll).

---

## 3. Sequencing & milestones

```
WV0 identity ─▶ WVX build/data (element years, work reconcile) ─▶ WV3 chronology 2-mode ─▶ WV1 reading graph
                                                                └▶ WV2 facets ─▶ WV4 overlap ─▶ WV5 anchors ─▶ verify
```
- **M1** BoK group named + build emits element years + work identity reconciled.
- **M2** Chronology two modes (the largest change) land and verify.
- **M3** Reading graph "major works" + element counts.
- **M4** Facets completeness + element bridge; Overlap & Anchors refreshed.
- **M5** Docs + expansion report; full headless-Chrome verification; `_bok_work/RESUME_STATE.md`.

WVX (build/data) gates WV3's Elements mode and any 804-scope BoK, so it goes first after naming.

## 4. Decisions (locked 2026-07-11)

1. **Group name** — ✅ **Body of Knowledge** (divider `body of knowledge`; compact `BoK` if space is tight).
2. **Reading-graph "major" set** — ✅ the **258 works with a reading relation**, anchor/core/survey emphasized; the 210 edgeless works reachable via Facets/Chronology/search (stated in the header).
3. **BoK chronology scope** — ✅ the **full ~804 referenced works** (468 corpus + 336 pass-8, pass-8 marked `·p8`).
4. **Element date source** — ✅ (default) named_in year → corpus-id year → earliest covering-work year → UNRESOLVED (90 % coverage; 106 undated).
5. **Element integration depth in Facets/Overlap/Anchors** — ✅ (default) add element-teach counts + click-through everywhere; keep the views work-centric (full element facets stay in view 6).
6. **Anchors in the group** — ✅ (default) all five tabs are one BoK group (Anchors folded in).

## 5. Deliverables checklist

- [ ] WV0: `body of knowledge` tab divider; header/eyebrow copy; docs name the three layers.
- [ ] WVX: `build_elements.py` emits `year`/`yearSource`; work-identity reconciled; (opt) unified 804-work BoK source.
- [ ] WV3: Chronology two modes (BoK / Elements) + toggle + hash deep-link.
- [ ] WV1: Reading graph major-works framing, ≤100/band guard, element-teach counts.
- [ ] WV2: Facets 468-reachability assurance + element-teach per row (+ opt facet).
- [ ] WV4 / WV5: Overlap & Anchors verified current (+ opt element pointers).
- [ ] Views 1–5 keep single-viewport; views 6–11 unregressed; zero console errors (headless-Chrome verified).
- [ ] Docs (README, MODELS, ARCHITECTURE) updated; `EXPANSION_REPORT_<date>_bok.md`; `_bok_work/RESUME_STATE.md`.

## 6. Cross-cutting rules (unchanged)

House discipline (pure core + thin shells, `window.SWE`, `file://`-safe, zero deps, strict-JSDoc,
global error backstops); **the five BoK views keep the strict single 16:9 4K viewport, no page scroll**
(only internal column scroll); determinism (no `Math.random`); honesty markers (verification, UNRESOLVED,
`lead`, sourced/editorial, `·p8`) stay visible; durable/resumable under `SWE/_bok_work/`; **committing
stays the user's call** — nothing committed unless you say so.
