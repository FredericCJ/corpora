# Phase 4 element-view implementation spec (for el-bridge, el-graph, el-coverage)

Reference template (READ IT FIRST, match its structure/interaction exactly):
  logic/views/el_taxonomy.js   — a WORKING, browser-verified element view.
Core API it calls:  logic/core_elements.js  (SWE.coreEl, aliased CE)

## View interface (identical to el_taxonomy.js)
Register: `SWE.views['<id>'] = (function(){ ... return { label, mount }; })();`
`mount(root, ctx)` builds DOM under `root`, returns `{ applyFilters, onSelect, destroy }`.
- applyFilters(): re-render honouring the global search `SWE.state.get().q`.
- onSelect(sel): re-render to reflect the selected id (highlight).
- destroy(): tear down (disconnect any ResizeObserver; else `()=>{}`).
Select anything with `SWE.state.set({ sel: id })` — works for element ids AND work ids
(the inspector renders element detail or work detail accordingly).

## ctx.elIndex (idx) — the built index
- idx.byId[id] -> element node
- idx.out[id] / idx.inn[id] -> outgoing / incoming edges [{from,kind,to,provenance,cite,note}]
- idx.elementsByWork[workId] -> [elementId,...]
- idx.design[] / idx.arch[] / idx.nodes[] -> element nodes
- idx.unbridged -> [{id,why}]   (6 design elements)
- idx.works[workId] -> {id,title,authors,year,verification,type,corpusNode}
- idx.meta -> {designCount:709, archCount:374, edgeCount:1132, crossRealm, sourced:328, editorial:804, bridged:703, unbridgedCount:6, designCovered, archCovered, designKinds{}, archKinds{}}

element node = {id, name, realm:'design'|'architecture', kind, aka[], what, problem,
                named_in, named_in_corpus_id, tags[], qa[], borderline, confidence, works[workId]}
edge kinds: realizes, enables (design->arch); constrains (arch->design); implements (design->design);
            specializes, composes-with, alternative-to (within a realm).

## CE (SWE.coreEl) pure helpers — REUSE THESE (don't re-derive)
- CE.visible(idx, q) -> Set(ids) matching search over id/name/aka/what
- CE.closure(id, idx, 'out'|'in'|'both') -> Set(ids)  (cycle-safe)
- CE.bridgeByArch(idx) -> { archId: [{from:designId, kind, provenance, note}] }
- CE.coverageBuckets(idx) -> { gap:[nodes], thin:[nodes], covered:[nodes] }  (design only)
- CE.isCross(kind) -> bool ;  CE.VIEWS['<id>'] -> {label, semantic, question, computed}

## U (SWE.util) — DOM helpers
U.el(tag, attrs, ...kids), U.svg(tag, attrs, ...kids), U.shortTitle(s, max),
U.elChips(n) -> [realm chip, kind chip], U.elBadges(n) -> [confidence, borderline, qa badges],
U.REALM_CLS{design:'re-design',architecture:'re-arch'}, U.REALM_SHORT.

## CSS classes available (styles/app.css) — reuse, don't invent new ones
.vp .vp-head .vp-body   (view frame; put an <h2> + <p class=note> in vp-head)
.el-scroll  (absolute-inset scroll region — element views MAY scroll)
.el-two  (two-column grid)   .el-group (card, h3 header + .sub)   .el-line (clickable row, .nm)
.el-count  .el-legend   .prov-s (sourced) .prov-e (editorial)
.chip  .chip.re-design .chip.re-arch  .badge  .card  .rows .row  .morebtn  .empty  .rescount .facet-rail .facetbar
graph: .board (grid bg) + <svg> ; .gnode (rect+text, add .sel/.dim) ; .gedge (add .editorial for dotted)

## Self-verify before returning (Node is unavailable — use headless Chrome):
CHROME="/c/Program Files/Google/Chrome/Application/chrome.exe"
"$CHROME" --headless --disable-gpu --dump-dom --virtual-time-budget=4000 \
  "file:///E:/dev/corpora/SWE/explorer/index.html#view=<your-view-id>" 2>/dev/null > /tmp/dom.html
grep -c "data failed to load" /tmp/dom.html    # MUST be 0
# and grep for content your view is expected to render.
