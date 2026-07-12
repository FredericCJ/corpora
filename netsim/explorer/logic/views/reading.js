// views/reading.js — the typed reading graph (shell). Consumes core.graphLayout / typedAdjacency /
// closure. Directed, cyclic-capable relations between resources, hued by the twelve kinds; editorial
// edges are dotted, derived solid. SVG scales to fill the pane (strict single viewport); hover traces
// the cycle-safe closure both directions. This is the SWE-parity relation view (distinct from the
// banded EDITORIAL Overlays in views/graph.js).
window.NET = window.NET || {}; NET.views = NET.views || {};
NET.views.reading = (function () {
  'use strict';
  const U = NET.util, C = NET.core;

  /** Per-band cap (≤130): keep the highest-degree resources, return the edge subset among them.
   *  Deterministic, surfaced in `capped`, no-op while every band ≤130 (non-binding at current scale). */
  function capBands(nodes, edges, capped) {
    const inGraph = new Set(); edges.forEach((e) => { inGraph.add(e.s); inGraph.add(e.t); });
    const deg = {}; edges.forEach((e) => { deg[e.s] = (deg[e.s] || 0) + 1; deg[e.t] = (deg[e.t] || 0) + 1; });
    const byBand = {};
    for (const n of nodes) if (inGraph.has(n.id)) { const c = C.primaryCorpus(n, U.CORPUS_ORDER); (byBand[c] = byBand[c] || []).push(n); }
    let trimmed = false; const keep = new Set();
    for (const c of U.CORPUS_ORDER) {
      const list = (byBand[c] || []).slice();
      if (list.length <= 130) { list.forEach((n) => keep.add(n.id)); continue; }
      list.sort((a, b) => (deg[b.id] || 0) - (deg[a.id] || 0) || a.id.localeCompare(b.id));
      list.slice(0, 130).forEach((n) => keep.add(n.id)); capped.push(U.CORPUS_SHORT[c] + ' +' + (list.length - 130)); trimmed = true;
    }
    return trimmed ? edges.filter((e) => keep.has(e.s) && keep.has(e.t)) : edges;
  }

  function mount(root, ctx) {
    const corpus = ctx.corpus, relations = ctx.relations, log = ctx.log || NET.log.NOOP;
    const byId = {}; corpus.nodes.forEach((n) => { byId[n.id] = n; });
    const capped = [];
    const drawnEdges = capBands(corpus.nodes, relations.edges, capped);
    const adj = C.typedAdjacency(drawnEdges);
    const deg = {}; drawnEdges.forEach((e) => { deg[e.s] = (deg[e.s] || 0) + 1; deg[e.t] = (deg[e.t] || 0) + 1; });
    const drawnIds = new Set(); drawnEdges.forEach((e) => { drawnIds.add(e.s); drawnIds.add(e.t); });
    const nEd = relations.edges.length, nEdit = relations.edges.filter((e) => e.src === 'editorial').length;

    const vp = U.el('div', { class: 'vp reading' });
    const headNote = 'Typed reading relations between resources — ' + drawnIds.size + ' of ' + corpus.nodes.length
      + ' stand in ≥1 relation (' + nEd + ' edges: ' + (nEd - nEdit) + ' derived, ' + nEdit + ' editorial·dotted). '
      + 'Bands are corpora (order: subfield/paradigm, then year); edge colour is the relation kind (legend in the inspector); '
      + 'hover or focus traces the full cycle-safe closure. The ' + (corpus.nodes.length - drawnIds.size)
      + ' resources with no typed relation are reachable in Anchor, Facets, Chronology, and search.'
      + (capped.length ? ' · capped to 130/band: ' + capped.join(', ') : '');
    vp.appendChild(U.el('div', { class: 'vp-head' },
      U.el('h2', { text: 'Reading graph — how the resources relate' }),
      U.el('p', { class: 'note', text: headNote })));
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
      const L = C.graphLayout(corpus.nodes, drawnEdges, U.CORPUS_ORDER, { aspect });
      const NW = L.box.NW, NH = L.box.NH, pos = L.positions;
      log.debug('reading layout', { w: Math.round(L.width), h: Math.round(L.height), aspect: +aspect.toFixed(2) });

      const svg = U.svg('svg', { viewBox: `0 0 ${L.width} ${L.height}`, preserveAspectRatio: 'xMidYMid meet',
        role: 'img', 'aria-label': `Reading graph of ${Object.keys(pos).length} resources in ${L.bands.length} corpora` });
      const defs = U.svg('defs');
      const mk = U.svg('marker', { id: 'net-rarr', viewBox: '0 0 10 10', refX: '9', refY: '5', markerWidth: '6', markerHeight: '6', orient: 'auto-start-reverse' });
      mk.appendChild(U.svg('path', { d: 'M1.5 1.5 L9 5 L1.5 8.5', fill: 'none', stroke: 'context-stroke', 'stroke-width': '1.6', 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }));
      defs.appendChild(mk); svg.appendChild(defs);
      const gB = U.svg('g'), gE = U.svg('g'), gN = U.svg('g');
      svg.appendChild(gB); svg.appendChild(gE); svg.appendChild(gN);

      for (const b of L.bands) {
        gB.appendChild(U.svg('rect', { x: b.x, y: b.y, width: b.w, height: b.h, rx: 12, fill: U.corpusFill(b.key), 'fill-opacity': 0.5, stroke: U.corpusStroke(b.key), 'stroke-opacity': 0.18 }));
        const t = U.svg('text', { x: b.labelX, y: b.labelY, class: 'band-label', 'font-size': 13 });
        t.textContent = (corpus.corpora[b.key] ? corpus.corpora[b.key].label : b.key).toUpperCase() + ' · ' + b.count;
        gB.appendChild(t);
      }

      edgeEls = [];
      for (const e of drawnEdges) {
        const a = pos[e.s], b = pos[e.t]; if (!a || !b) continue;
        const c1 = { x: a.x + NW / 2, y: a.y + NH / 2 }, c2 = { x: b.x + NW / 2, y: b.y + NH / 2 };
        const p1 = anchorPt(c2, c1, NW, NH), p2 = anchorPt(c1, c2, NW, NH);
        const my = (p1.y + p2.y) / 2 - Math.min(78, Math.hypot(p2.x - p1.x, p2.y - p1.y) / 4);
        const path = U.svg('path', { d: `M${p1.x} ${p1.y} Q ${(p1.x + p2.x) / 2} ${my}, ${p2.x} ${p2.y}`,
          class: 'gedge' + (e.src === 'editorial' ? ' editorial' : ''), 'marker-end': 'url(#net-rarr)' });
        path.style.stroke = U.kindColor(e.kind);
        if (U.KIND_DASH[e.kind] && e.src !== 'editorial') path.style.strokeDasharray = U.KIND_DASH[e.kind];
        const tip = U.svg('title');
        tip.textContent = e.s + ' → ' + e.t + ' [' + e.kind + ' · ' + e.src + (e.cycle ? ' · ' + e.cycle : '') + ']\n' + (e.note || '');
        path.appendChild(tip);
        path.dataset.s = e.s; path.dataset.t = e.t;
        gE.appendChild(path); edgeEls.push(path);
      }

      nodeEls = {};
      for (const id in pos) {
        const n = byId[id], p = pos[id];
        const isMajor = (deg[id] || 0) >= 5;
        const g = U.svg('g', { class: 'gnode' + (n.verification === 'verified-train' ? ' train' : '') + (n.verification === 'unverified' ? ' unv' : '') + (isMajor ? ' major' : ''),
          tabindex: '0', role: 'button', 'aria-label': `${id} ${n.title}, ${n.year || n.recency}, ${n.verRaw}, ${deg[id] || 0} relations` });
        const r = U.svg('rect', { x: p.x, y: p.y, width: NW, height: NH, rx: 8 });
        r.style.fill = U.hueFill(n); r.style.stroke = U.hueStroke(n);
        g.appendChild(r);
        U.wrapText(n.title, 24, 2).forEach((ln, i) => { const tx = U.svg('text', { x: p.x + 9, y: p.y + 15 + i * 12, class: 'nm', 'font-size': 9.8 }); tx.textContent = ln; g.appendChild(tx); });
        const yr = U.svg('text', { x: p.x + 9, y: p.y + NH - 7, class: 'yr', 'font-size': 8.2 });
        yr.textContent = id + (n.year ? ' · ' + n.year : (n.living ? ' · living' : ''));
        g.appendChild(yr);
        if ((deg[id] || 0) >= 5) {
          const dm = U.svg('text', { x: p.x + NW - 7, y: p.y + NH - 7, class: 'degm', 'text-anchor': 'end', 'font-size': 8.2 });
          dm.textContent = '↔' + (deg[id] || 0); g.appendChild(dm);
        }
        const tip = U.svg('title'); tip.textContent = id + ' — ' + n.title + '\n' + U.shortTitle(n.cite, 110);
        g.appendChild(tip);
        g.addEventListener('mouseenter', () => highlight(id));
        g.addEventListener('mouseleave', restore);
        g.addEventListener('focus', () => highlight(id));
        g.addEventListener('blur', restore);
        g.addEventListener('click', (ev) => { ev.stopPropagation(); NET.state.set({ sel: id }); });
        g.addEventListener('keydown', (ev) => { if (ev.key === 'Enter' || ev.key === ' ') { ev.preventDefault(); NET.state.set({ sel: id }); } });
        gN.appendChild(g); nodeEls[id] = g;
      }
      board.replaceChildren(svg);
      applyFilters(); onSelect(NET.state.get().sel);
    }

    function highlight(id) {
      const keep = new Set([...C.closure(id, adj.up), ...C.closure(id, adj.down)]);
      for (const nid in nodeEls) nodeEls[nid].classList.toggle('dim', !keep.has(nid));
      for (const p of edgeEls) { const on = keep.has(p.dataset.s) && keep.has(p.dataset.t); p.classList.toggle('hl', on); p.classList.toggle('dim', !on); }
    }
    function clearHl() { for (const nid in nodeEls) nodeEls[nid].classList.remove('dim'); for (const p of edgeEls) p.classList.remove('hl', 'dim'); }
    function restore() { const sel = NET.state.get().sel; if (sel && nodeEls[sel]) highlight(sel); else clearHl(); }

    function applyFilters() {
      const vis = C.visibleIds(corpus, NET.state.get());
      for (const nid in nodeEls) nodeEls[nid].classList.toggle('off', !vis.has(nid));
      for (const p of edgeEls) p.classList.toggle('off', !vis.has(p.dataset.s) || !vis.has(p.dataset.t));
    }
    function onSelect(sel) { for (const nid in nodeEls) nodeEls[nid].classList.toggle('sel', nid === sel); restore(); }

    board.addEventListener('click', () => { if (NET.state.get().sel) NET.state.set({ sel: null }); });
    const ro = new ResizeObserver(() => { if (rafPending) return; rafPending = true; requestAnimationFrame(() => { rafPending = false; build(); }); });
    ro.observe(board);
    build();
    return { applyFilters, onSelect, destroy: () => ro.disconnect() };
  }
  return { label: 'Reading graph', mount };
})();
