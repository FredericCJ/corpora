// views/graph.js — Model 6: EDITORIAL typed-relation overlays (shell). Two maintainer-curated
// overlays over a curated subset — a didactic ground-up reading order and theory→applied
// specialization chains. Levels are horizontal bands; hover traces the transitive closure along
// overlay edges; every edge tooltip carries its rationale and the EDITORIAL provenance. The
// layout has a fixed natural size (core.overlayLayout) and scales via viewBox — built per overlay
// switch, not per resize.
window.NET = window.NET || {}; NET.views = NET.views || {};
NET.views.graph = (function () {
  'use strict';
  const U = NET.util, C = NET.core;

  function mount(root, ctx) {
    const corpus = ctx.corpus, relations = ctx.relations, log = ctx.log || NET.log.NOOP;
    const byId = {}; corpus.nodes.forEach((n) => { byId[n.id] = n; });
    const overlays = relations.overlays;
    const ovOf = (id) => overlays.find((o) => o.id === id) || overlays[0];

    const vp = U.el('div', { class: 'vp' });
    const head = U.el('div', { class: 'vp-head' });
    const h2 = U.el('h2', { text: 'Overlays' });
    const sw = U.el('span', { class: 'ovsw', role: 'group', 'aria-label': 'Overlay picker' });
    const note = U.el('p', { class: 'note' });
    const hrow = U.el('div', { class: 'ovrow' }); hrow.appendChild(h2); hrow.appendChild(sw);
    head.appendChild(hrow); head.appendChild(note); vp.appendChild(head);
    const body = U.el('div', { class: 'vp-body' });
    const board = U.el('div', { class: 'board' });
    body.appendChild(board); vp.appendChild(body); root.appendChild(vp);

    let nodeEls = {}, edgeEls = [], adj = { up: {}, down: {} }, current = null;

    function syncSwitch() {
      sw.replaceChildren();
      for (const o of overlays)
        sw.appendChild(U.el('button', { class: 'ovbtn', 'aria-pressed': String(o.id === current.id),
          text: o.label, onclick: () => NET.state.set({ ov: o.id }) }));
    }

    function build() {
      current = ovOf(NET.state.get().ov || 'didactic');
      adj = C.overlayAdjacency(current);
      h2.textContent = 'Overlays — ' + current.label + ' (EDITORIAL)';
      note.textContent = current.semantic + ' ' + relations.overlayProvenance +
        ' Hover a work to trace its transitive closure; dashed node borders are verified[TRAIN].';
      syncSwitch();

      const L = C.overlayLayout(current);
      const NW = L.box.NW, NH = L.box.NH, pos = L.positions;
      log.debug('overlay layout', { ov: current.id, w: Math.round(L.width), h: Math.round(L.height) });

      const svg = U.svg('svg', { viewBox: `0 0 ${L.width} ${L.height}`, preserveAspectRatio: 'xMidYMid meet',
        role: 'img', 'aria-label': current.label + ' overlay of ' + Object.keys(current.members).length + ' works' });
      const defs = U.svg('defs');
      const mk = U.svg('marker', { id: 'net-arr', viewBox: '0 0 10 10', refX: '9', refY: '5',
        markerWidth: '6.5', markerHeight: '6.5', orient: 'auto-start-reverse' });
      mk.appendChild(U.svg('path', { d: 'M1.5 1.5 L9 5 L1.5 8.5', fill: 'none', stroke: 'context-stroke',
        'stroke-width': '1.6', 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }));
      defs.appendChild(mk); svg.appendChild(defs);
      const gB = U.svg('g'), gE = U.svg('g'), gN = U.svg('g');
      svg.appendChild(gB); svg.appendChild(gE); svg.appendChild(gN);

      L.bands.forEach((b, bi) => {
        gB.appendChild(U.svg('rect', { x: b.x, y: b.y, width: b.w, height: b.h, rx: 10,
          fill: 'var(--panel-2)', 'fill-opacity': bi % 2 ? 0.55 : 0.9, stroke: 'var(--line)', 'stroke-opacity': 0.7 }));
        const lg = U.svg('g', { class: 'row-label' });
        const tno = U.svg('text', { x: b.x + 12, y: b.y + 22, class: 'tno', 'font-size': 12.5 });
        tno.textContent = b.key.toUpperCase() + ' · ' + b.label + ' · ' + b.count;
        lg.appendChild(tno);
        U.wrapText(b.note, 34, 3).forEach((ln, i) => {
          const t = U.svg('text', { x: b.x + 12, y: b.y + 38 + i * 12, class: 'tnm', 'font-size': 9.5 });
          t.textContent = ln; lg.appendChild(t);
        });
        gB.appendChild(lg);
      });

      const lvIx = {}; current.levels.forEach((lv, i) => { lvIx[lv.key] = i; });
      edgeEls = [];
      current.edges.forEach((e, i) => {
        const a = pos[e.s], b = pos[e.t];
        const sameBand = current.members[e.s] === current.members[e.t];
        let d;
        if (sameBand) {
          const sx = a.x + NW / 2, tx = b.x + NW / 2, sy = a.y, ty = b.y;
          const lift = 20 + (i % 3) * 7;
          d = `M${sx} ${sy} C ${sx} ${sy - lift}, ${tx} ${ty - lift}, ${tx} ${ty}`;
        } else {
          const sx = a.x + NW / 2, sy = a.y + NH, tx = b.x + NW / 2, ty = b.y;
          const span = lvIx[current.members[e.t]] - lvIx[current.members[e.s]];
          const bow = span >= 2 ? ((i % 5) - 2) * 18 : 0;
          const k = Math.max(22, (ty - sy) * 0.42);
          d = `M${sx} ${sy} C ${sx + bow} ${sy + k}, ${tx + bow} ${ty - k}, ${tx} ${ty}`;
        }
        const path = U.svg('path', { d, class: 'gedge', 'marker-end': 'url(#net-arr)' });
        path.dataset.s = e.s; path.dataset.t = e.t;
        const tip = U.svg('title');
        tip.textContent = e.s + ' → ' + e.t + ' [' + current.edgeKind + ' · EDITORIAL]\n' + e.why;
        path.appendChild(tip);
        gE.appendChild(path); edgeEls.push(path);
      });

      nodeEls = {};
      for (const id in pos) {
        const n = byId[id], p = pos[id];
        const g = U.svg('g', { class: 'gnode' + (n.verification === 'verified-train' ? ' train' : ''),
          tabindex: '0', role: 'button',
          'aria-label': `${id} ${n.title}, ${current.members[id]}, ${n.verRaw}` });
        const r = U.svg('rect', { x: p.x, y: p.y, width: NW, height: NH, rx: 8 });
        r.style.fill = U.hueFill(n); r.style.stroke = U.hueStroke(n);
        g.appendChild(r);
        const lines = U.wrapText(n.title, 26, 2);
        lines.forEach((ln, i) => { const tx = U.svg('text', { x: p.x + 9, y: p.y + 15 + i * 12, class: 'nm', 'font-size': 9.8 }); tx.textContent = ln; g.appendChild(tx); });
        const yr = U.svg('text', { x: p.x + 9, y: p.y + NH - 7, class: 'yr', 'font-size': 8.2 });
        yr.textContent = id + (n.year ? ' · ' + n.year : (n.living ? ' · living' : ''));
        g.appendChild(yr);
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
    function onOverlay() { build(); }

    board.addEventListener('click', () => { if (NET.state.get().sel) NET.state.set({ sel: null }); });
    build();
    return { applyFilters, onSelect, onOverlay, destroy: () => {} };
  }
  return { label: 'Overlays', mount };
})();
