// views/graph.js — Model 1: typed reading graph (shell). Consumes core.graphLayout / closure.
// SVG scales to fill the pane (single viewport); hover traces the cycle-safe closure.
window.SWE = window.SWE || {}; SWE.views = SWE.views || {};
SWE.views.graph = (function () {
  'use strict';
  const U = SWE.util, C = SWE.core;

  function mount(root, ctx) {
    const corpus = ctx.corpus, relations = ctx.relations, log = ctx.log || SWE.log.NOOP;
    const byId = {}; corpus.nodes.forEach((n) => { byId[n.id] = n; });
    const adj = C.adjacency(relations.edges);

    const vp = U.el('div', { class: 'vp' });
    vp.appendChild(U.el('div', { class: 'vp-head' },
      U.el('h2', { text: 'Reading graph — typed relations with provenance' }),
      U.el('p', { class: 'note', text: 'Bands are corpora; layout is computed (theme, then year). Hover or focus a resource to trace its full ancestor + descendant closure — cycles are followed and terminate. Click for the full citation and per-edge justifications. Dashed border = unverified; ★ = report-flagged anchor.' })));
    const body = U.el('div', { class: 'vp-body' });
    const board = U.el('div', { class: 'board' });
    body.appendChild(board); vp.appendChild(body); root.appendChild(vp);

    let nodeEls = {}, edgeEls = [], rafPending = false;

    function anchorPt(from, to, NW, NH) {
      const dx = to.x - from.x, dy = to.y - from.y;
      const sc = Math.max(Math.abs(dx) / (NW / 2 + 6), Math.abs(dy) / (NH / 2 + 6), 1e-6);
      return { x: to.x - dx / sc, y: to.y - dy / sc };
    }

    function build() {
      const rect = board.getBoundingClientRect();
      const aspect = rect.width > 0 && rect.height > 0 ? rect.width / rect.height : 1.4;
      const L = C.graphLayout(corpus.nodes, relations.edges, U.CORPUS_ORDER, { aspect });
      const NW = L.box.NW, NH = L.box.NH, pos = L.positions;
      log.debug('graph layout', { w: Math.round(L.width), h: Math.round(L.height), aspect: +aspect.toFixed(2) });

      const svg = U.svg('svg', { viewBox: `0 0 ${L.width} ${L.height}`, preserveAspectRatio: 'xMidYMid meet',
        role: 'img', 'aria-label': `Reading graph of ${Object.keys(pos).length} works in ${L.bands.length} corpora` });
      const defs = U.svg('defs');
      const mk = U.svg('marker', { id: 'swe-arr', viewBox: '0 0 10 10', refX: '9', refY: '5', markerWidth: '6', markerHeight: '6', orient: 'auto-start-reverse' });
      mk.appendChild(U.svg('path', { d: 'M1.5 1.5 L9 5 L1.5 8.5', fill: 'none', stroke: 'context-stroke', 'stroke-width': '1.6', 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }));
      defs.appendChild(mk); svg.appendChild(defs);
      const gB = U.svg('g'), gE = U.svg('g'), gN = U.svg('g');
      svg.appendChild(gB); svg.appendChild(gE); svg.appendChild(gN);

      for (const b of L.bands) {
        gB.appendChild(U.svg('rect', { x: b.x, y: b.y, width: b.w, height: b.h, rx: 12, fill: U.corpusFill(b.key), 'fill-opacity': 0.5, stroke: U.corpusStroke(b.key), 'stroke-opacity': 0.16 }));
        const t = U.svg('text', { x: b.labelX, y: b.labelY, class: 'band-label', 'font-size': 13 });
        t.textContent = (corpus.corpora[b.key] || b.key).toUpperCase() + ' · ' + b.count;
        gB.appendChild(t);
      }

      edgeEls = [];
      for (const e of relations.edges) {
        const a = pos[e.s], b = pos[e.t]; if (!a || !b) continue;
        const c1 = { x: a.x + NW / 2, y: a.y + NH / 2 }, c2 = { x: b.x + NW / 2, y: b.y + NH / 2 };
        const p1 = anchorPt(c2, c1, NW, NH), p2 = anchorPt(c1, c2, NW, NH);
        const my = (p1.y + p2.y) / 2 - Math.min(78, Math.hypot(p2.x - p1.x, p2.y - p1.y) / 4);
        const path = U.svg('path', { d: `M${p1.x} ${p1.y} Q ${(p1.x + p2.x) / 2} ${my}, ${p2.x} ${p2.y}`,
          class: 'gedge' + (e.src === 'editorial' ? ' editorial' : ''), 'marker-end': 'url(#swe-arr)' });
        path.style.stroke = U.kindColor(e.kind);
        if (U.KIND_DASH[e.kind] && e.src !== 'editorial') path.style.strokeDasharray = U.KIND_DASH[e.kind];
        path.dataset.s = e.s; path.dataset.t = e.t;
        gE.appendChild(path); edgeEls.push(path);
      }

      nodeEls = {};
      for (const id in pos) {
        const n = byId[id], p = pos[id], c = C.primaryCorpus(n, U.CORPUS_ORDER);
        const isAnchor = (n.role || []).includes('anchor');
        const g = U.svg('g', { class: 'gnode' + (n.verification === 'unverified' ? ' unv' : '') + (isAnchor ? ' anchor' : ''),
          tabindex: '0', role: 'button', 'aria-label': `${n.title}, ${n.year}, ${n.verification}` });
        const r = U.svg('rect', { x: p.x, y: p.y, width: NW, height: NH, rx: 8 });
        r.style.fill = U.corpusFill(c); r.style.stroke = isAnchor ? 'var(--accent)' : U.corpusStroke(c);
        g.appendChild(r);
        const lines = U.wrapLabel(n.title, 22, 2);
        lines.forEach((ln, i) => { const tx = U.svg('text', { x: p.x + 9, y: p.y + 16 + i * 13, class: 'nm', 'font-size': 10.5 }); tx.textContent = ln; g.appendChild(tx); });
        const yr = U.svg('text', { x: p.x + 9, y: p.y + NH - 8, class: 'yr', 'font-size': 9 });
        yr.textContent = n.year + (isAnchor ? ' ★' : '') + (n.automotive ? ' ◆' : '');
        g.appendChild(yr);
        const tip = U.svg('title'); tip.textContent = n.title + ' — ' + n.authors + ' (' + n.year + ')';
        g.appendChild(tip);
        g.addEventListener('mouseenter', () => highlight(id));
        g.addEventListener('mouseleave', restore);
        g.addEventListener('focus', () => highlight(id));
        g.addEventListener('blur', restore);
        g.addEventListener('click', (ev) => { ev.stopPropagation(); SWE.state.set({ sel: id }); });
        g.addEventListener('keydown', (ev) => { if (ev.key === 'Enter' || ev.key === ' ') { ev.preventDefault(); SWE.state.set({ sel: id }); } });
        gN.appendChild(g); nodeEls[id] = g;
      }
      board.replaceChildren(svg);
      applyFilters(); onSelect(SWE.state.get().sel);
    }

    function highlight(id) {
      const keep = new Set([...C.closure(id, adj.up), ...C.closure(id, adj.down)]);
      for (const nid in nodeEls) nodeEls[nid].classList.toggle('dim', !keep.has(nid));
      for (const p of edgeEls) { const on = keep.has(p.dataset.s) && keep.has(p.dataset.t); p.classList.toggle('hl', on); p.classList.toggle('dim', !on); }
    }
    function clearHl() { for (const nid in nodeEls) nodeEls[nid].classList.remove('dim'); for (const p of edgeEls) p.classList.remove('hl', 'dim'); }
    function restore() { const sel = SWE.state.get().sel; if (sel && nodeEls[sel]) highlight(sel); else clearHl(); }

    function applyFilters() {
      const vis = C.visibleIds(corpus, SWE.state.get());
      for (const nid in nodeEls) nodeEls[nid].classList.toggle('off', !vis.has(nid));
      for (const p of edgeEls) p.classList.toggle('off', !vis.has(p.dataset.s) || !vis.has(p.dataset.t));
    }
    function onSelect(sel) { for (const nid in nodeEls) nodeEls[nid].classList.toggle('sel', nid === sel); restore(); }

    board.addEventListener('click', () => { if (SWE.state.get().sel) SWE.state.set({ sel: null }); });
    const ro = new ResizeObserver(() => { if (rafPending) return; rafPending = true; requestAnimationFrame(() => { rafPending = false; build(); }); });
    ro.observe(board);
    build();
    return { applyFilters, onSelect, destroy: () => ro.disconnect() };
  }
  return { label: 'Reading graph', mount };
})();
