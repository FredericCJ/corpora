// views/graph.js — Model 1: the prerequisite DAG (shell). Consumes core.dagLayout / closure.
// Tiers are horizontal bands top→bottom; the SVG scales to fill the pane via viewBox (the layout
// has a fixed natural size, so it is built once — no ResizeObserver needed). Hover traces the
// full ancestor + descendant closure; dashed amber edges are JUDGMENT; the ghost node is N18.
window.CALC = window.CALC || {}; CALC.views = CALC.views || {};
CALC.views.graph = (function () {
  'use strict';
  const U = CALC.util, C = CALC.core;

  function mount(root, ctx) {
    const corpus = ctx.corpus, relations = ctx.relations, log = ctx.log || CALC.log.NOOP;
    const byId = {}; corpus.nodes.forEach((n) => { byId[n.id] = n; });
    const adj = C.adjacency(relations.edges);

    const vp = U.el('div', { class: 'vp' });
    vp.appendChild(U.el('div', { class: 'vp-head' },
      U.el('h2', { text: 'Prerequisite DAG — nine tiers, source to sinks' }),
      U.el('p', { class: 'note', text: 'Rows are tiers (colour = depth); within-row order is computed, not meaningful. Hover or focus a text to trace everything it builds on and everything it unlocks. Solid edges are EVIDENCED seams; dashed amber edges are JUDGMENT calls. Dashed enclosures are parallel sets — alternatives, not sequences. The grey dashed ghost is N18 Woods, dropped by the quality gate. Click any node for its citation and seams.' })));
    const body = U.el('div', { class: 'vp-body' });
    const board = U.el('div', { class: 'board' });
    body.appendChild(board); vp.appendChild(body); root.appendChild(vp);

    let nodeEls = {}, edgeEls = [];

    function build() {
      const L = C.dagLayout(corpus.nodes, relations.edges, corpus.tiers, relations.parallelSets);
      const NW = L.box.NW, NH = L.box.NH, pos = L.positions;
      log.debug('dag layout', { w: Math.round(L.width), h: Math.round(L.height) });

      const svg = U.svg('svg', { viewBox: `0 0 ${L.width} ${L.height}`, preserveAspectRatio: 'xMidYMid meet',
        role: 'img', 'aria-label': `Prerequisite DAG of ${corpus.nodes.length} texts across ${L.rows.length} tiers` });
      const defs = U.svg('defs');
      const mk = U.svg('marker', { id: 'calc-arr', viewBox: '0 0 10 10', refX: '9', refY: '5', markerWidth: '6.5', markerHeight: '6.5', orient: 'auto-start-reverse' });
      mk.appendChild(U.svg('path', { d: 'M1.5 1.5 L9 5 L1.5 8.5', fill: 'none', stroke: 'context-stroke', 'stroke-width': '1.6', 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }));
      defs.appendChild(mk); svg.appendChild(defs);
      const gB = U.svg('g'), gPS = U.svg('g'), gE = U.svg('g'), gN = U.svg('g');
      svg.appendChild(gB); svg.appendChild(gPS); svg.appendChild(gE); svg.appendChild(gN);

      for (const r of L.rows) {
        gB.appendChild(U.svg('rect', { x: r.bandX, y: r.bandY, width: r.bandW, height: r.bandH, rx: 10,
          fill: U.tierFill(r.tier), 'fill-opacity': 0.42, stroke: U.tierStroke(r.tier), 'stroke-opacity': 0.14 }));
        const lg = U.svg('g', { class: 'row-label' });
        const tno = U.svg('text', { x: r.bandX + 12, y: r.bandY + 22, class: 'tno', 'font-size': 13 });
        tno.textContent = 'TIER ' + r.tier;
        tno.style.fill = U.tierStroke(r.tier);
        lg.appendChild(tno);
        U.wrapLabel(r.name, 26, 3).forEach((ln, i) => {
          const t = U.svg('text', { x: r.bandX + 12, y: r.bandY + 37 + i * 12.5, class: 'tnm', 'font-size': 10.5 });
          t.textContent = ln; lg.appendChild(t);
        });
        const rg = U.svg('text', { x: r.bandX + 12, y: r.bandY + r.bandH - 8, class: 'trg', 'font-size': 9 });
        rg.textContent = r.rigor;
        lg.appendChild(rg);
        gB.appendChild(lg);
      }

      for (const b of L.psBoxes) {
        gPS.appendChild(U.svg('rect', { x: b.x, y: b.y, width: b.w, height: b.h, rx: 9, class: 'ps-box' }));
        const t = U.svg('text', { x: b.x + 7, y: b.y + 11, class: 'ps-tag', 'font-size': 9 });
        t.textContent = b.id + ' · ' + b.label;
        gPS.appendChild(t);
      }

      edgeEls = [];
      relations.edges.forEach((e, i) => {
        const a = pos[e.s], b = pos[e.t];
        const sx = a.x + NW / 2, sy = a.y + NH, tx = b.x + NW / 2, ty = b.y;
        const span = byId[e.t].tier - byId[e.s].tier;
        const bow = span >= 2 ? ((i % 5) - 2) * 16 : 0;
        const k = Math.max(24, (ty - sy) * 0.42);
        const d = `M${sx} ${sy} C ${sx + bow} ${sy + k}, ${tx + bow} ${ty - k}, ${tx} ${ty}`;
        const path = U.svg('path', { d, class: 'gedge' + (e.tag === 'JUDGMENT' ? ' jd' : ''), 'marker-end': 'url(#calc-arr)' });
        path.style.stroke = U.evStroke(e.tag);
        path.dataset.s = e.s; path.dataset.t = e.t;
        const tip = U.svg('title');
        tip.textContent = e.s + ' → ' + e.t + ' [' + e.tag + ']\n' + e.seam;
        path.appendChild(tip);
        gE.appendChild(path); edgeEls.push(path);
      });

      nodeEls = {};
      for (const id in pos) {
        const n = byId[id], p = pos[id];
        const special = n.flags.includes('source') || n.flags.includes('sink');
        const g = U.svg('g', { class: 'gnode' + (n.status === 'dropped' ? ' ghost' : '') + (special ? ' special' : ''),
          tabindex: '0', role: 'button',
          'aria-label': `${n.id} ${n.title}, ${n.authors}, ${n.year}, tier ${n.tier}${n.status === 'dropped' ? ', dropped' : ''}` });
        const r = U.svg('rect', { x: p.x, y: p.y, width: NW, height: NH, rx: 8 });
        if (n.status === 'dropped') { r.style.stroke = 'var(--faint)'; }
        else { r.style.fill = U.tierFill(n.tier); r.style.stroke = special ? 'var(--accent)' : U.tierStroke(n.tier); }
        g.appendChild(r);
        const lines = U.wrapLabel(n.title, 24, 2);
        lines.forEach((ln, i) => { const tx = U.svg('text', { x: p.x + 9, y: p.y + 16 + i * 12.5, class: 'nm', 'font-size': 10.5 }); tx.textContent = ln; g.appendChild(tx); });
        const au = U.svg('text', { x: p.x + 9, y: p.y + (lines.length > 1 ? 42 : 30), class: 'au', 'font-size': 9 });
        au.textContent = U.shortTitle(n.authors, 28); g.appendChild(au);
        const yr = U.svg('text', { x: p.x + 9, y: p.y + NH - 8, class: 'yr', 'font-size': 8.5 });
        const marks = n.flags.map((f) => (U.FLAG_MARK[f] || '').split(' ')[0]).join(' ');
        yr.textContent = n.id + ' · ' + n.year + (marks ? ' · ' + marks : '') + (n.status === 'dropped' ? ' · ✕ dropped' : '');
        g.appendChild(yr);
        const tip = U.svg('title'); tip.textContent = n.id + ' — ' + n.title + ' · ' + n.authors + ' (' + n.year + ')';
        g.appendChild(tip);
        g.addEventListener('mouseenter', () => highlight(id));
        g.addEventListener('mouseleave', restore);
        g.addEventListener('focus', () => highlight(id));
        g.addEventListener('blur', restore);
        g.addEventListener('click', (ev) => { ev.stopPropagation(); CALC.state.set({ sel: id }); });
        g.addEventListener('keydown', (ev) => { if (ev.key === 'Enter' || ev.key === ' ') { ev.preventDefault(); CALC.state.set({ sel: id }); } });
        gN.appendChild(g); nodeEls[id] = g;
      }
      board.replaceChildren(svg);
      applyFilters(); onSelect(CALC.state.get().sel);
    }

    function highlight(id) {
      const keep = new Set([...C.closure(id, adj.up), ...C.closure(id, adj.down)]);
      for (const nid in nodeEls) nodeEls[nid].classList.toggle('dim', !keep.has(nid));
      for (const p of edgeEls) { const on = keep.has(p.dataset.s) && keep.has(p.dataset.t); p.classList.toggle('hl', on); p.classList.toggle('dim', !on); }
    }
    function clearHl() { for (const nid in nodeEls) nodeEls[nid].classList.remove('dim'); for (const p of edgeEls) p.classList.remove('hl', 'dim'); }
    function restore() { const sel = CALC.state.get().sel; if (sel && nodeEls[sel]) highlight(sel); else clearHl(); }

    function applyFilters() {
      const vis = C.visibleIds(corpus, CALC.state.get());
      for (const nid in nodeEls) nodeEls[nid].classList.toggle('off', !vis.has(nid));
      for (const p of edgeEls) p.classList.toggle('off', !vis.has(p.dataset.s) || !vis.has(p.dataset.t));
    }
    function onSelect(sel) { for (const nid in nodeEls) nodeEls[nid].classList.toggle('sel', nid === sel); restore(); }

    board.addEventListener('click', () => { if (CALC.state.get().sel) CALC.state.set({ sel: null }); });
    build();
    return { applyFilters, onSelect, destroy: () => {} };
  }
  return { label: 'DAG', mount };
})();
