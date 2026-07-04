// views/graph.js — Model 1: typed reading graph. Data-driven SVG; no hand layout.
window.SWE = window.SWE || {}; SWE.views = SWE.views || {};
SWE.views.graph = (function () {
  'use strict';
  const U = SWE.util, NS = 'http://www.w3.org/2000/svg';
  const NW = 140, NH = 42, GX = 16, GY = 14, BANDGAP = 46, TOP = 46;
  const ORDER = ['swa-science', 'emb-arch', 'emb-c', 'emb-cpp', 'emb-ops', 'simulink'];

  function svgEl(tag, attrs) {
    const n = document.createElementNS(NS, tag);
    for (const k in attrs || {}) n.setAttribute(k, attrs[k]);
    return n;
  }
  function primary(node) { for (const c of ORDER) if (node.corpora.includes(c)) return c; return node.corpora[0]; }

  function mount(root) {
    const nodesById = {}; SWE.corpus.nodes.forEach(n => nodesById[n.id] = n);
    const E = SWE.relations.edges;
    const inGraph = new Set(); E.forEach(e => { inGraph.add(e.s); inGraph.add(e.t); });
    const gnodes = SWE.corpus.nodes.filter(n => inGraph.has(n.id));

    root.appendChild(U.el('h2', { text: 'Reading graph — typed relations with provenance' }));
    root.appendChild(U.el('p', { class: 'viewnote', text:
      gnodes.length + ' of ' + SWE.corpus.nodes.length + ' nodes participate in ' + E.length +
      ' typed edges (report-stated, derived, or marked EDITORIAL). Bands are corpora; layout is computed ' +
      '(theme, then year). Hover or focus a node to trace its full closure — cycles are followed and terminate. ' +
      'Click for the full citation and per-edge justifications. Dashed node borders = unverified.' }));

    // kind legend
    const leg = U.el('div', { class: 'facetbar' }, U.el('span', { class: 'lab', text: 'edge kinds' }));
    for (const k of SWE.relations.kinds) {
      const sw = U.el('span');
      sw.style.cssText = 'display:inline-block;width:22px;height:0;border-top:2px ' +
        (U.KIND_DASH[k] ? 'dashed ' : 'solid ') + U.KIND_COLOR[k] + ';margin-right:4px;vertical-align:middle';
      leg.appendChild(U.el('span', { class: 'chip plain' }, sw, k));
    }
    leg.appendChild(U.el('span', { class: 'chip plain', text: '⋯ dotted = EDITORIAL provenance' }));
    root.appendChild(leg);

    // ---- layout ----
    const pos = {}; let bandX = 20, maxY = 0;
    const bandMeta = [];
    for (const c of ORDER) {
      const list = gnodes.filter(n => primary(n) === c)
        .sort((a, b) => ((a.themes[0] || '') + '').localeCompare(b.themes[0] || '') ||
                        (U.yearNum(a) || 9999) - (U.yearNum(b) || 9999));
      if (!list.length) continue;
      const ncols = Math.max(2, Math.round(Math.sqrt(list.length / 1.9)));
      list.forEach((n, i) => {
        pos[n.id] = { x: bandX + (i % ncols) * (NW + GX), y: TOP + Math.floor(i / ncols) * (NH + GY) };
        maxY = Math.max(maxY, pos[n.id].y + NH);
      });
      bandMeta.push({ c, x: bandX, w: ncols * (NW + GX) - GX, n: list.length });
      bandX += ncols * (NW + GX) - GX + BANDGAP;
    }
    const W = bandX - BANDGAP + 20, H = maxY + 26;

    const board = U.el('div', { class: 'board' });
    const svg = svgEl('svg', { viewBox: '0 0 ' + W + ' ' + H, width: W, height: H, role: 'img',
      'aria-label': 'Typed reading graph of ' + gnodes.length + ' works' });
    const defs = svgEl('defs');
    const mk = svgEl('marker', { id: 'garr', viewBox: '0 0 10 10', refX: '8', refY: '5',
      markerWidth: '5', markerHeight: '5', orient: 'auto-start-reverse' });
    mk.appendChild(svgEl('path', { d: 'M2 1.5L8 5L2 8.5', fill: 'none', stroke: 'context-stroke',
      'stroke-width': '1.7', 'stroke-linecap': 'round' }));
    defs.appendChild(mk); svg.appendChild(defs);
    const gB = svgEl('g'), gE = svgEl('g'), gN = svgEl('g');
    svg.appendChild(gB); svg.appendChild(gE); svg.appendChild(gN);

    for (const b of bandMeta) {
      const r = svgEl('rect', { x: b.x - 8, y: 12, width: b.w + 16, height: H - 22, rx: 10,
        fill: U.CORPUS_COLOR[b.c], 'fill-opacity': '0.045' });
      gB.appendChild(r);
      const t = svgEl('text', { x: b.x, y: 32, class: 'bandlab' });
      t.textContent = (SWE.corpus.corpora[b.c] || b.c).toUpperCase() + ' · ' + b.n;
      gB.appendChild(t);
    }

    // edges (endpoint trimmed to node boundary so arrowheads stay visible)
    function anchorPt(from, to) {
      const dx = to.x - from.x, dy = to.y - from.y;
      const sc = Math.max(Math.abs(dx) / (NW / 2 + 5), Math.abs(dy) / (NH / 2 + 5), 1e-6);
      return { x: to.x - dx / sc, y: to.y - dy / sc };
    }
    const edgeEls = [];
    for (const e of E) {
      const a = pos[e.s], b = pos[e.t]; if (!a || !b) continue;
      const c1 = { x: a.x + NW / 2, y: a.y + NH / 2 }, c2 = { x: b.x + NW / 2, y: b.y + NH / 2 };
      const p1 = anchorPt(c2, c1), p2 = anchorPt(c1, c2);
      const mx = (p1.x + p2.x) / 2, my = (p1.y + p2.y) / 2 - Math.min(70, Math.hypot(p2.x - p1.x, p2.y - p1.y) / 4);
      const path = svgEl('path', { d: 'M' + p1.x + ' ' + p1.y + ' Q ' + mx + ' ' + my + ', ' + p2.x + ' ' + p2.y,
        class: 'gedge' + (e.src === 'editorial' ? ' edi' : ''), 'marker-end': 'url(#garr)' });
      path.style.stroke = U.KIND_COLOR[e.kind];
      if (U.KIND_DASH[e.kind] && e.src !== 'editorial') path.style.strokeDasharray = U.KIND_DASH[e.kind];
      path.dataset.s = e.s; path.dataset.t = e.t;
      gE.appendChild(path); edgeEls.push(path);
    }

    // adjacency + cycle-safe closure
    const up = {}, down = {};
    E.forEach(e => { (down[e.s] = down[e.s] || []).push(e.t); (up[e.t] = up[e.t] || []).push(e.s); });
    function closure(id, adj) {
      const seen = new Set([id]), q = [id];
      while (q.length) { const c = q.pop(); (adj[c] || []).forEach(x => { if (!seen.has(x)) { seen.add(x); q.push(x); } }); }
      return seen;
    }
    const nodeEls = {};
    function highlight(id) {
      const keep = new Set([...closure(id, up), ...closure(id, down)]);
      for (const nid in nodeEls) nodeEls[nid].classList.toggle('dim', !keep.has(nid));
      for (const p of edgeEls) {
        const hl = keep.has(p.dataset.s) && keep.has(p.dataset.t);
        p.classList.toggle('hl', hl); p.classList.toggle('dim', !hl);
      }
    }
    function clearHl() {
      for (const nid in nodeEls) nodeEls[nid].classList.remove('dim');
      for (const p of edgeEls) p.classList.remove('hl', 'dim');
    }

    for (const n of gnodes) {
      const p = pos[n.id], c = primary(n);
      const g = svgEl('g', { class: 'gnode' + (n.verification === 'unverified' ? ' unvN' : ''), tabindex: '0',
        role: 'button', 'aria-label': n.title + ', ' + n.verification });
      const rect = svgEl('rect', { x: p.x, y: p.y, width: NW, height: NH, rx: 7 });
      rect.style.fill = U.CORPUS_BG[c]; rect.style.stroke = U.CORPUS_COLOR[c];
      if ((n.role || []).includes('anchor')) { rect.style.stroke = 'var(--accent)'; rect.style.strokeWidth = '2'; }
      g.appendChild(rect);
      const t1 = svgEl('text', { x: p.x + 7, y: p.y + 17, class: 'nt' });
      t1.textContent = U.shortTitle(n.title, 24); g.appendChild(t1);
      const t2 = svgEl('text', { x: p.x + 7, y: p.y + 33, class: 'ny' });
      t2.textContent = n.year + ((n.role || []).includes('survey') ? ' ¶' : '') + (n.automotive ? ' ◆' : '');
      g.appendChild(t2);
      const tip = svgEl('title'); tip.textContent = n.title + ' — ' + n.authors + ' (' + n.year + ')';
      g.appendChild(tip);
      g.addEventListener('mouseenter', () => highlight(n.id));
      g.addEventListener('mouseleave', clearHl);
      g.addEventListener('focus', () => highlight(n.id));
      g.addEventListener('blur', clearHl);
      g.addEventListener('click', () => SWE.detail.show(n.id));
      g.addEventListener('keydown', ev => { if (ev.key === 'Enter' || ev.key === ' ') { ev.preventDefault(); SWE.detail.show(n.id); } });
      gN.appendChild(g); nodeEls[n.id] = g;
    }
    board.appendChild(svg); root.appendChild(board);
    root.appendChild(U.el('p', { class: 'hint',
      text: 'hover / focus — trace closure (cycle-safe) · click / Enter — full citation & edges · scroll the board horizontally' }));

    // apply global filters as dimming
    function applyFilters() {
      const vis = SWE.search.visibleIds();
      for (const nid in nodeEls) nodeEls[nid].classList.toggle('off', !vis.has(nid));
    }
    applyFilters();

    // ---- per-edge catalog, grouped by provenance ----
    root.appendChild(U.el('h3', { text: 'Edge catalog — every relation with its justification' }));
    const groups = [
      ['report:swa', 'Report-stated — software-architecture-as-science typed edge list'],
      ['report:sim', 'Report-stated — Simulink bottom-up DAG (detail → abstraction ⇒ prerequisite-of)'],
      ['derived', 'Derived — mechanically from explicit report statements (quoted basis)'],
      ['editorial', 'EDITORIAL — reasoned judgment, not report fact']];
    for (const [src, label] of groups) {
      const list = E.filter(e => e.src === src);
      const det = U.el('details', { class: 'cat' }, U.el('summary', { text: label + ' (' + list.length + ')' }));
      const ul = U.el('ul', { class: 'elist' });
      for (const e of list) {
        const a = nodesById[e.s], b = nodesById[e.t];
        const li = U.el('li');
        li.appendChild(U.el('span', { class: 'lnk', text: U.shortTitle(a.title, 60), tabindex: '0',
          onclick: () => SWE.detail.show(a.id) }));
        li.appendChild(U.el('span', { class: 'kt', text: e.kind }));
        li.appendChild(U.el('span', { class: 'lnk', text: U.shortTitle(b.title, 60), tabindex: '0',
          onclick: () => SWE.detail.show(b.id) }));
        if (e.note) li.appendChild(U.el('span', { class: 'ov', text: ' — ' + e.note }));
        if (e.cycle) li.appendChild(U.el('span', { class: 'badge unv', text: 'cycle ' + e.cycle }));
        ul.appendChild(li);
      }
      det.appendChild(ul); root.appendChild(det);
    }
    return { applyFilters };
  }
  return { label: 'Reading graph', mount };
})();
