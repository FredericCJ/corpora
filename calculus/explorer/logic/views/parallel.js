// views/parallel.js — Model 4: parallel sets (shell). Six cards of equivalent-scope siblings.
// Each card shows the stated §4 semantics AND the build-time audit of what the edge list actually
// shares — shared vs partial neighborhoods carried honestly (PS-2's stated N09 edge is partial).
window.CALC = window.CALC || {}; CALC.views = CALC.views || {};
CALC.views.parallel = (function () {
  'use strict';
  const U = CALC.util, C = CALC.core;

  function mount(root, ctx) {
    const corpus = ctx.corpus, relations = ctx.relations;
    const byId = {}; corpus.nodes.forEach((n) => { byId[n.id] = n; });

    const vp = U.el('div', { class: 'vp' });
    vp.appendChild(U.el('div', { class: 'vp-head' },
      U.el('h2', { text: 'Parallel sets — alternatives, not sequences' }),
      U.el('p', { class: 'note', text: 'Within a set no A→B ordering is implied; siblings are meant to inherit the same incoming and outgoing edges (report caveat). The shared/partial lists below are computed from the actual edge list at build time, so the stated claim is checkable — partial rows name which siblings carry the edge.' })));
    const body = U.el('div', { class: 'vp-body' });
    const wrap = U.el('div', { class: 'pswrap' });
    const grid = U.el('div', { class: 'psgrid' });
    wrap.appendChild(grid); body.appendChild(wrap); vp.appendChild(body); root.appendChild(vp);

    const cardEls = {};

    function neighborRow(id, kind) {
      const n = byId[id];
      const row = U.el('div', { class: 'psrow' });
      row.appendChild(U.idChip(n, () => CALC.state.set({ sel: id })));
      row.appendChild(U.el('span', { text: ' ' + U.shortTitle(n.title, 44) + ' ' }));
      if (kind) row.appendChild(U.el('span', { class: 'who', text: kind }));
      return row;
    }

    function render() {
      grid.replaceChildren();
      const curSel = CALC.state.get().sel;
      for (const ps of relations.parallelSets) {
        const card = U.el('div', { class: 'pscard' });
        const h = U.el('h3');
        h.appendChild(U.el('span', { class: 'psid', text: ps.id }));
        h.appendChild(document.createTextNode(ps.label));
        card.appendChild(h);
        card.appendChild(U.el('p', { class: 'note', text: ps.note }));

        const mem = U.el('div', { class: 'psmembers' });
        for (const m of ps.members) {
          const n = byId[m];
          const mc = U.el('div', { class: 'card', tabindex: '0', role: 'button', 'data-id': m,
            onclick: () => CALC.state.set({ sel: m }),
            onkeydown: (ev) => { if (ev.key === 'Enter' || ev.key === ' ') { ev.preventDefault(); CALC.state.set({ sel: m }); } } });
          mc.style.borderLeftColor = U.tierStroke(n.tier);
          if (m === curSel) mc.style.outline = '2px solid var(--ink)';
          mc.appendChild(U.el('h4', { text: n.id + ' — ' + U.shortTitle(n.title, 52) }));
          mc.appendChild(U.el('p', { text: n.authors + ' · ' + n.edition + ' ed. · ' + n.year + ' · ' + n.publisher }));
          mem.appendChild(mc); cardEls[m] = mc;
        }
        card.appendChild(mem);

        const a = ps.audit;
        card.appendChild(U.el('div', { class: 'pssec', text: 'shared prerequisites (all members)' }));
        a.sharedIn.length ? a.sharedIn.forEach((x) => card.appendChild(neighborRow(x, '')))
          : card.appendChild(U.el('p', { class: 'empty', text: 'none shared' }));
        for (const x in a.partialIn) card.appendChild(neighborRow(x, 'only into ' + a.partialIn[x].join(', ')));

        card.appendChild(U.el('div', { class: 'pssec', text: 'shared continuations (all members)' }));
        a.sharedOut.length ? a.sharedOut.forEach((x) => card.appendChild(neighborRow(x, '')))
          : card.appendChild(U.el('p', { class: 'empty', text: 'none shared — terminal set' }));
        for (const x in a.partialOut) card.appendChild(neighborRow(x, 'only from ' + a.partialOut[x].join(', ')));

        grid.appendChild(card);
      }
      applyFilters();
    }

    function applyFilters() {
      const vis = C.visibleIds(corpus, CALC.state.get());
      for (const id in cardEls) cardEls[id].classList.toggle('dimmed', !vis.has(id));
    }
    function onSelect(sel) {
      for (const id in cardEls) cardEls[id].style.outline = id === sel ? '2px solid var(--ink)' : '';
    }
    render();
    return { applyFilters, onSelect, destroy: () => {} };
  }
  return { label: 'Parallel sets', mount };
})();
