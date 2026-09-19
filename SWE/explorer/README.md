# Embedded Software Corpus Explorer

A single-page explorer of a **unified embedded-software research corpus** — eight research passes of
*works* merged into one fact layer (five relational models), plus a two-realm layer of the *concepts
themselves* — the **design + architecture elements** — wired to the works and to each other,
navigable through **four element views** and a **two-view atlas** that maps the whole element space,
and a **derivation spine** that runs from stakeholder need to running system.
Twelve views over two fact layers.

- **Works:** 922 resources · 8 corpora · 261 typed edges (86 swa + 57 sim + 50 derived + 19 editorial + 49 proc) ·
  585 verified / 337 unverified · 357 cross-corpus works.
- **The spine (pass 9, `arch-spine`):** **796 works** — 454 new nodes + 342 memberships reclaiming works the
  corpus already held — tagged on two new array facets, `stage` (needs · obligations · requirements · design ·
  tools-process) and `domain` (complex-scale · complex-science · governance · measurement · runtime-ops ·
  hand-c · model-c). 35 cells; 20 carry an adversarial panel's thin-cell adjudication. See
  `../MISSION_arch_spine_v1.md` and `../EXPANSION_REPORT_2026-09-20_spine.md`.
- **Elements (the ELEMENT-layer mission + atlas enrichment):** **709 design + 374 architecture = 1083
  elements**, wired by **2811 typed relations** (v1.1): the 878 cross-realm bridge edges (703/709 design
  elements bridged, 6 unbridged) plus a dense within-realm fabric (1267 design-sibling + 666
  architecture-sibling edges) researched by the atlas endeavour; 1023 sourced : 1788 editorial.
  Element→work coverage from **pass 8** (417 works; 706/709 design elements reach a catalog-grade work).
- **Atlas:** the enriched graph consolidated into **21 named emergent islands** (`../ATLAS_SPEC.md`),
  drawn as a semantic-zoom map. Deliverables: `../design_elements_catalog_v1_0.md`,
  `../architecture_elements_catalog_v1_0.md`, `../design_elements_corpus_v1_0.md`,
  `../design_elements_bridge_v1_1.md`, `../ATLAS_SPEC.md`.
- Pass 7 (`swe-process`) adds 47 nodes + 48 memberships on a `language` facet. See `../swe_process_corpus_v1_0.md`.
- Raw HTML/CSS/JS, no framework, no build step at view time, opens from `file://`. The five work
  models keep the strict **single 16:9 4K viewport, no page scroll**; the four element views
  **authorize page/inner scroll** (element-scale navigability) — the one relaxation of the
  single-viewport rule, per the mission (target display unchanged; the work models are not degraded).

## Body of Knowledge — the five work models

The five historic work models are now the named group **Body of Knowledge**, the first stop on the
tab spine **Body of Knowledge · Elements · Atlas** = *the literature · the concepts · the map*. Every
Body-of-Knowledge view now surfaces per-work **element-teach counts** ("◇N" — a work grounds N
elements) and routes into the element and atlas layers (work → elements → atlas), while staying
work-centric.

1. **Reading graph — the major works** — the ~258 works standing in a typed reading relation, with
   anchors (★) / core / survey emphasized and "◇N" marking works that ground N elements; the ~210
   edgeless works remain reachable via Chronology, Facets, and search.
2. **Facets** — corpus × branch × theme × type lattice with live counts.
3. **Chronology** — two modes: **Body of Knowledge**, the ~804 referenced works (468 reading-corpus
   works ∪ 336 works referenced only by the element layer, marked "·p8") by year of last publication;
   and **Elements**, the 1083 design & architecture elements by build-derived concept year (994
   datable, 89 UNRESOLVED). Living + UNRESOLVED strata as before.
4. **Overlap** — the graft points: works claimed by ≥2 passes (pairwise matrix + signatures).
5. **Anchors** — each corpus's own report-flagged entry points.

## The four element views (6–9)

6. **Element taxonomy** — the realm × kind × tag lattice over both catalogs, live counts.
7. **Design↔Arch bridge** — which architecture elements anchor which design elements; the 6 unbridged shown.
8. **Element relations** — a focused ego-graph over the typed edges; click a neighbour to re-focus.
9. **Element coverage** — which works teach which elements (pass 8); thin/gap coverage surfaced.

## The atlas (10–11) — a map of the element space

10. **Atlas** — the archipelago: ~21 emergent islands with semantic zoom (L0 map → L1 island → L2 node),
    coloured by family, joined by aggregated relations; breadcrumb, rim ports, minimap, search-teleport.
11. **Bridge-Flow** — a bipartite flow map: seven design families → the busiest architecture anchors,
    ribbon thickness = realizing-element count.

A persistent inspector dock shows the active view's method + legend, or — when you select a **work**
— its citation, memberships, tags, relations, and the elements it teaches; when you select an
**element** — its definition, aliases, realm, kind, covering works, and every typed relation
(including cross-realm bridge edges with provenance). Selection flows across layers: an element's
covering work links to the work corpus, and a work links back to the elements it teaches.

## The spine (12) — the derivation chain

12. **Spine** — the pass-9 coverage matrix: seven domains against the five derivation stages, the chain
    reading left to right through the column headers. Counts are live over the works' own `stage`/`domain`
    tags (no inference); click a cell, a stage or a domain to filter. Thin cells are flagged with the
    adjudication the adversarial critic panels reached — **△ sweep-thin** (the material exists, the sweep
    looked in the wrong vocabulary) or **○ literature-thin** (the field has not written that intersection).
    The distinction is a finding the corpus records, never a guess made in the view.

## Open it

- **Simplest:** double-click `index.html` — runs from `file://` with zero dependencies.
- **Over HTTP:** `python -m http.server 8098 --directory .`, then open `http://localhost:8098/`.

## Use it

- **Tabs `1–9`** switch the first nine views (1–5 work models · 6–9 element views); the **atlas** (10),
  **Bridge-Flow** (11) and **Spine** (12) are reached by the tab bar or **←/→**. **`/`** search (and atlas teleport) · **`v`** cycles verification · **`Esc`** clears.
- Hover/focus a node in the graph to trace its closure; click any resource or element anywhere for its detail.
- The **verification** and **corpus** selectors filter the work models; the element views filter by realm/kind in-view; **reset** clears all.

## Rebuild the data

The fact + inference layers are generated by the Python `build/` (the only place report text is read):

```
python build/build.py     # records_*.py + edges.py → corpus/relations; build_elements.py → elements
```

`build.py` runs four phases: the seven work passes (unchanged) then **PHASE 4**, which encodes the
element layer. `build/build_elements.py` consumes `build/element_src/` (the committed encoded form of
the four Phase 1–3 deliverables — as `records_*.py` are the encoded form of the pass reports) and
**self-audits, failing loud** on any mismatch: (a) **completeness** — built design/architecture/edge
counts must equal the deliverable `.md` census headers (709 / 374 / 2811); (b) the **bridging rule**
— every design element carries ≥1 cross-realm edge or is on the unbridged list, and that list must
match the bridge report's. It emits `data/elements.{json,js}`. `build_elements.py` also emits a
per-element **year / yearSource** (waterfall: `named_in` year → `named_in_corpus_id` year → earliest
covering-work year → UNRESOLVED), and the `elements.json` meta gained `datable`, `undated`,
`yearSources`, `decadeHist`, `worksReferenced` (417), `worksCorpus` (81), and `worksPass8Only` (336)
— the fields the Chronology **Elements** mode and the ·p8 Body-of-Knowledge stratum are built from.

## Checker & tests (committed contract)

`tsconfig.json` (strict `checkJs` over the raw `.js` via JSDoc) and `package.json` pin the mid-2026
toolchain — `typescript` 6.0.x as a checker, `vitest` 4.1.x + `playwright`, `fast-check` for the
pure-core property tests (`core.js` layout/closure/facet/strata are all pure).

```
npm run check     # tsc --noEmit
npm test          # vitest run
```

> Node was unavailable where this was authored, so `check`/`test` are the committed contract, not a
> verified run. The app ships **zero runtime dependencies**. The five work models were verified
> in-browser at 3840×2160 (single viewport, no page scroll, hover-closure + inspect + filters, no
> console errors); the element layer was verified via headless Chrome (`--dump-dom`): `build.py`
> audits pass, all nine view tabs mount with zero boot errors, element detail + cross-layer
> navigation (element ↔ covering work) render, and the work models are unregressed.

## Layout & provenance

- Architecture, the single-viewport layout engine, and the manifest-compliance map:
  [ARCHITECTURE.md](ARCHITECTURE.md).
- The five models, their computations, and the anti-fabrication provenance discipline:
  [MODELS.md](MODELS.md).
- Phase logs: [data/corpus_report.md](data/corpus_report.md) (extraction & merges),
  [data/adjustments.md](data/adjustments.md) (vocabulary reconciliation).
