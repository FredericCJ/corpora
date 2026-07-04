// render.js — IMPERATIVE SHELL. Projects the pure layout (graph.js) into SVG and owns the DOM
// side effects + interaction. State is never read back out of the DOM; the renderer subscribes
// to DS.state and re-projects. Logger is injected (defaults to the no-op).
window.DS = window.DS || {};
DS.render = (function () {
  'use strict';
  const U = DS.util, G = DS.graph;

  /** @param {HTMLElement} board @param {{corpus:any,relations:any,log?:any}} ctx */
  function mount(board, ctx) {
    const corpus = ctx.corpus, relations = ctx.relations, log = ctx.log || DS.log.NOOP;
    const byId = {}; corpus.nodes.forEach((n) => { byId[n.id] = n; });
    const adj = G.adjacency(relations.edges);

    let nodeEls = {}, edgeEls = [], layout = null, rafPending = false;

    function anchor(from, to, NW, NH) {
      const dx = to.x - from.x, dy = to.y - from.y;
      const sc = Math.max(Math.abs(dx) / (NW / 2 + 6), Math.abs(dy) / (NH / 2 + 6), 1e-6);
      return { x: to.x - dx / sc, y: to.y - dy / sc };
    }

    function build() {
      const rect = board.getBoundingClientRect();
      const aspect = rect.width > 0 && rect.height > 0 ? rect.width / rect.height : 1.4;
      layout = G.computeLayout(corpus.nodes, relations.edges, corpus.familyOrder, { aspect });
      const NW = layout.box.NW, NH = layout.box.NH, pos = layout.positions;
      log.debug('layout computed', { w: Math.round(layout.width), h: Math.round(layout.height),
        aspect: +aspect.toFixed(2), nodes: Object.keys(pos).length });

      const svg = U.svg('svg', { viewBox: `0 0 ${layout.width} ${layout.height}`,
        preserveAspectRatio: 'xMidYMid meet', role: 'img',
        'aria-label': `Lineage graph of ${Object.keys(pos).length} data structures across ${layout.bands.length} families` });

      const defs = U.svg('defs');
      const mk = U.svg('marker', { id: 'ds-arr', viewBox: '0 0 10 10', refX: '9', refY: '5',
        markerWidth: '6.5', markerHeight: '6.5', orient: 'auto-start-reverse' });
      mk.appendChild(U.svg('path', { d: 'M1.5 1.5 L9 5 L1.5 8.5', fill: 'none', stroke: 'context-stroke',
        'stroke-width': '1.6', 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }));
      defs.appendChild(mk); svg.appendChild(defs);

      const gB = U.svg('g'), gE = U.svg('g'), gN = U.svg('g');
      svg.appendChild(gB); svg.appendChild(gE); svg.appendChild(gN);

      for (const b of layout.bands) {
        gB.appendChild(U.svg('rect', { x: b.x, y: b.y, width: b.w, height: b.h, rx: 12,
          class: 'band-bg', fill: U.familyFill(b.family), 'fill-opacity': 0.55,
          stroke: U.familyStroke(b.family), 'stroke-opacity': 0.16 }));
        const t = U.svg('text', { x: b.labelX, y: b.labelY, class: 'band-label', 'font-size': 13 });
        t.textContent = (corpus.families[b.family] || b.family) + ' · ' + b.count;
        gB.appendChild(t);
      }

      edgeEls = [];
      for (const e of relations.edges) {
        const a = pos[e.s], b = pos[e.t]; if (!a || !b) continue;
        const c1 = { x: a.x + NW / 2, y: a.y + NH / 2 }, c2 = { x: b.x + NW / 2, y: b.y + NH / 2 };
        const p1 = anchor(c2, c1, NW, NH), p2 = anchor(c1, c2, NW, NH);
        const my = (p1.y + p2.y) / 2 - Math.min(80, Math.hypot(p2.x - p1.x, p2.y - p1.y) / 4);
        const path = U.svg('path', { d: `M${p1.x} ${p1.y} Q ${(p1.x + p2.x) / 2} ${my}, ${p2.x} ${p2.y}`,
          class: 'gedge ' + e.kind + (e.src === 'editorial' ? ' editorial' : ''), 'marker-end': 'url(#ds-arr)' });
        path.style.stroke = U.kindColor(e.kind);
        path.dataset.s = e.s; path.dataset.t = e.t; path.dataset.kind = e.kind;
        gE.appendChild(path); edgeEls.push(path);
      }

      nodeEls = {};
      for (const id in pos) {
        const n = byId[id], p = pos[id];
        const g = U.svg('g', { class: 'gnode ' + n.tier + (n.verification === 'flagged' ? ' flagged' : ''),
          tabindex: '0', role: 'button',
          'aria-label': `${n.name}, ${U.TIER_LABEL[n.tier]}, ${n.verification}` });
        const r = U.svg('rect', { x: p.x, y: p.y, width: NW, height: NH, rx: 8 });
        r.style.fill = U.familyFill(n.family);
        r.style.stroke = (n.tier === 'root' || n.tier === 'backfill') ? 'var(--accent)' : U.familyStroke(n.family);
        g.appendChild(r);
        const lines = U.wrapLabel(n.name, 22, 2);
        lines.forEach((ln, i) => {
          const tx = U.svg('text', { x: p.x + 9, y: p.y + (lines.length === 1 ? 19 : 15) + i * 13,
            class: 'nm', 'font-size': 11 });
          tx.textContent = ln; g.appendChild(tx);
        });
        const marks = (n.tier === 'root' || n.tier === 'backfill' ? ' ★' : '') + (n.verification === 'flagged' ? ' ⚠' : '');
        const yr = U.svg('text', { x: p.x + 9, y: p.y + NH - 7, class: 'yr', 'font-size': 9 });
        yr.textContent = (n.year == null ? '—' : n.year) + marks;
        g.appendChild(yr);
        const tip = U.svg('title'); tip.textContent = n.name + ' — ' + n.origin;
        g.appendChild(tip);

        g.addEventListener('mouseenter', () => highlight(id));
        g.addEventListener('mouseleave', restore);
        g.addEventListener('focus', () => highlight(id));
        g.addEventListener('blur', restore);
        g.addEventListener('click', (ev) => { ev.stopPropagation(); DS.state.set({ sel: id }); });
        g.addEventListener('keydown', (ev) => {
          if (ev.key === 'Enter' || ev.key === ' ') { ev.preventDefault(); DS.state.set({ sel: id }); }
        });
        gN.appendChild(g); nodeEls[id] = g;
      }

      board.replaceChildren(svg);
      applyFilters();
      reflectSelection();
    }

    function highlight(id) {
      const keep = new Set([...G.closure(id, adj.up), ...G.closure(id, adj.down)]);
      for (const nid in nodeEls) nodeEls[nid].classList.toggle('dim', !keep.has(nid));
      for (const p of edgeEls) {
        const on = keep.has(p.dataset.s) && keep.has(p.dataset.t);
        p.classList.toggle('hl', on); p.classList.toggle('dim', !on);
      }
    }
    function clearHighlight() {
      for (const nid in nodeEls) nodeEls[nid].classList.remove('dim');
      for (const p of edgeEls) p.classList.remove('hl', 'dim');
    }
    /** revert to whatever the selection implies (hover ended). */
    function restore() {
      const sel = DS.state.get().sel;
      if (sel && nodeEls[sel]) highlight(sel); else clearHighlight();
    }

    function applyFilters() {
      const s = DS.state.get();
      const vis = DS.search.visibleIds(corpus, s);
      for (const nid in nodeEls) nodeEls[nid].classList.toggle('off', !vis.has(nid));
      for (const p of edgeEls) {
        const kindOff = s.kind && p.dataset.kind !== s.kind;
        const endOff = !vis.has(p.dataset.s) || !vis.has(p.dataset.t);
        p.classList.toggle('off', Boolean(kindOff || endOff));
      }
    }

    function reflectSelection() {
      const sel = DS.state.get().sel;
      for (const nid in nodeEls) nodeEls[nid].classList.toggle('sel', nid === sel);
      restore();
    }

    // deselect when clicking empty board
    board.addEventListener('click', () => { if (DS.state.get().sel) DS.state.set({ sel: null }); });

    DS.state.on((s, changed) => {
      if (changed.some((k) => k === 'q' || k === 'family' || k === 'ver' || k === 'kind')) applyFilters();
      if (changed.includes('sel')) reflectSelection();
    });

    // recompute layout on pane resize (aspect-dependent); coalesce via rAF, no timers
    const ro = new ResizeObserver(() => {
      if (rafPending) return; rafPending = true;
      requestAnimationFrame(() => { rafPending = false; build(); });
    });
    ro.observe(board);

    build();
    log.info('graph mounted', { nodes: corpus.nodes.length, edges: relations.edges.length });
    return { rebuild: build };
  }

  return { mount };
})();
