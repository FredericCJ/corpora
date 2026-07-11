// views/el_graph.js — Element view 3: the typed element relation graph (shell). A focused ego-graph:
// the focus element (state.sel, else first search match, else the busiest design hub) sits centred,
// its direct neighbours fan out — design realm on the LEFT, architecture realm on the RIGHT — each
// joined by a .gedge (dotted when the edge is editorial). Clicking a neighbour re-focuses. All heavy
// computation stays in SWE.coreEl; this shell only projects the ego-graph to SVG and wires clicks.
window.SWE = window.SWE || {}; SWE.views = SWE.views || {};
SWE.views['el-graph'] = (function () {
  'use strict';
  const U = SWE.util, CE = SWE.coreEl;
  const CAP = 16;                                   // neighbours drawn per side
  const W = 1000, NW = 210, NH = 50, SLOT = 66;     // viewBox width + node box + vertical pitch
  const FILL = { design: '#E9F4EE', architecture: '#F1EAFB' };
  const STROKE = { design: '#0F6D5B', architecture: '#6D4AA6' };

  /** Pick the focus element id: current selection (if an element), else first search match, else the
   * design element with the most outgoing edges. Pure over idx + state. */
  function pickFocus(idx, st) {
    if (st.sel && idx.byId[st.sel]) return st.sel;
    const q = (st.q || '').trim();
    if (q) { const vis = CE.visible(idx, q); const hit = idx.nodes.find((n) => vis.has(n.id)); if (hit) return hit.id; }
    let best = null, bestN = -1;
    for (const n of idx.design) { const d = (idx.out[n.id] || []).length; if (d > bestN) { bestN = d; best = n.id; } }
    return best || (idx.nodes[0] && idx.nodes[0].id) || null;
  }

  function mount(root, ctx) {
    const idx = ctx.elIndex;
    const meta = CE.VIEWS['el-graph'];

    const vp = U.el('div', { class: 'vp' });
    vp.appendChild(U.el('div', { class: 'vp-head' },
      U.el('h2', { text: 'Element relations — focused ego-graph' }),
      U.el('p', { class: 'note', text: meta.semantic + ' ' + meta.computed }
        )));
    const toolbar = U.el('div', { class: 'el-legend', style: 'padding:.45rem .9rem .35rem;border-bottom:1px solid var(--line-2);flex:none;align-items:baseline' });
    const body = U.el('div', { class: 'vp-body' });
    const boardHost = U.el('div', { class: 'board' });
    body.appendChild(boardHost);
    vp.appendChild(toolbar); vp.appendChild(body); root.appendChild(vp);

    function render() {
      const st = SWE.state.get();
      const focusId = pickFocus(idx, st);
      const focus = focusId && idx.byId[focusId];
      toolbar.replaceChildren();
      if (!focus) { boardHost.replaceChildren(U.el('div', { class: 'empty', text: 'No element to focus.' })); return; }

      // Collect direct neighbours (out ∪ inn), deduped; keep connecting edges for prov + kind tally.
      const nb = new Map();                                  // neighbourId -> {edges:[]}
      const tally = {};
      const note = (e, other) => {
        tally[e.kind] = (tally[e.kind] || 0) + 1;
        if (other === focusId) return;
        (nb.get(other) || nb.set(other, { edges: [] }).get(other)).edges.push(e);
      };
      for (const e of idx.out[focusId] || []) note(e, e.to);
      for (const e of idx.inn[focusId] || []) note(e, e.from);

      // Toolbar: focus name, realm chip, edge-kind counts.
      toolbar.appendChild(U.el('span', { class: 'el-count', text: U.shortTitle(focus.name, 54) }));
      U.elChips(focus).forEach((c) => toolbar.appendChild(c));
      const kinds = Object.keys(tally).sort();
      if (kinds.length) kinds.forEach((k) => toolbar.appendChild(U.el('span', { class: 'chip', text: k + ' · ' + tally[k] })));
      else toolbar.appendChild(U.el('span', { class: 'chip', text: 'no relations' }));

      if (!nb.size) {
        boardHost.replaceChildren(U.el('div', { class: 'empty', text: focus.name + ' has no typed element relations.' }));
        return;
      }

      // Split neighbours by realm; design LEFT, architecture RIGHT; deterministic name sort; cap per side.
      const left = [], right = [];
      for (const [id, rec] of nb) {
        const node = idx.byId[id]; if (!node) continue;
        (node.realm === 'design' ? left : right).push({ node, rec });
      }
      const byName = (a, b) => a.node.name.localeCompare(b.node.name);
      left.sort(byName); right.sort(byName);
      const leftMore = Math.max(0, left.length - CAP), rightMore = Math.max(0, right.length - CAP);
      const leftShown = left.slice(0, CAP), rightShown = right.slice(0, CAP);

      const maxSide = Math.max(leftShown.length, rightShown.length, 1);
      const H = Math.max(440, maxSide * SLOT + 80);
      const cy = H / 2;
      const leftX = 40, leftEdge = leftX + NW;              // right edge of a left node
      const rightX = W - 40 - NW, rightEdge = rightX;       // left edge of a right node
      const fX = W / 2 - NW / 2, fL = fX, fR = fX + NW;

      const svg = U.svg('svg', { viewBox: `0 0 ${W} ${H}`, preserveAspectRatio: 'xMidYMid meet',
        role: 'img', 'aria-label': `Ego-graph of ${focus.name}: ${leftShown.length} design and ${rightShown.length} architecture neighbours` });
      const gE = U.svg('g'), gN = U.svg('g');
      svg.appendChild(gE); svg.appendChild(gN);

      // Vertical layout for a column of c centres, centred on cy.
      const centreY = (i, c) => cy - (c * SLOT) / 2 + SLOT / 2 + i * SLOT;

      function drawColumn(items, x, side, more) {
        items.forEach((it, i) => {
          const yc = centreY(i, items.length), ny = yc - NH / 2;
          const rep = it.rec.edges[0] || {};
          const editorial = rep.provenance === 'editorial';
          const ax = side === 'left' ? fL : fR, bx = side === 'left' ? leftEdge : rightEdge;
          const line = U.svg('line', { x1: ax, y1: cy, x2: bx, y2: yc, class: 'gedge' + (editorial ? ' editorial' : '') });
          line.style.stroke = STROKE[it.node.realm];
          gE.appendChild(line);
          gN.appendChild(nodeG(it.node, x, ny, false));
        });
        if (more > 0) {
          const yb = centreY(items.length - 1, items.length) + SLOT / 2 + 8;
          const t = U.svg('text', { x: x + NW / 2, y: yb, class: 'yr', 'font-size': 12, 'text-anchor': 'middle' });
          t.textContent = '+' + more + ' more (search / select to explore)';
          gN.appendChild(t);
        }
      }

      function nodeG(node, x, y, isFocus) {
        const g = U.svg('g', { class: 'gnode' + (isFocus ? ' sel' : ''), tabindex: '0', role: 'button',
          'aria-label': `${node.name}, ${node.realm} ${node.kind}` });
        const r = U.svg('rect', { x, y, width: NW, height: NH, rx: 8 });
        r.style.fill = FILL[node.realm] || 'var(--panel)';
        r.style.stroke = STROKE[node.realm] || 'var(--ink)';
        if (isFocus) r.style.strokeWidth = '3';
        g.appendChild(r);
        const lines = U.wrapLabel(node.name, 30, 2);
        lines.forEach((ln, i) => { const tx = U.svg('text', { x: x + 10, y: y + 17 + i * 13, class: 'nm', 'font-size': 11 }); tx.textContent = ln; g.appendChild(tx); });
        const kd = U.svg('text', { x: x + 10, y: y + NH - 7, class: 'yr', 'font-size': 9 });
        kd.textContent = U.REALM_SHORT[node.realm] + ' · ' + node.kind;
        g.appendChild(kd);
        const tip = U.svg('title'); tip.textContent = node.name + ' — ' + node.realm + ' / ' + node.kind + (isFocus ? ' (focus)' : ''); g.appendChild(tip);
        const go = (ev) => { ev.stopPropagation(); SWE.state.set({ sel: node.id }); };
        g.addEventListener('click', go);
        g.addEventListener('keydown', (ev) => { if (ev.key === 'Enter' || ev.key === ' ') { ev.preventDefault(); go(ev); } });
        return g;
      }

      drawColumn(leftShown, leftX, 'left', leftMore);
      drawColumn(rightShown, rightX, 'right', rightMore);
      gN.appendChild(nodeG(focus, fX, cy - NH / 2, true));   // focus last => on top
      boardHost.replaceChildren(svg);
    }

    render();
    return { applyFilters: render, onSelect: () => render(), destroy: () => {} };
  }
  return { label: 'Element relations', mount };
})();
