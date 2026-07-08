// views/tiers.js — Model 2: the tier ladder (shell). Nine columns, one per tier of the scheme,
// each carrying the scheme's own name/focus/rigor; nodes bucketed by catalogue tier. Columns
// scroll internally; the ladder fills the pane.
window.CALC = window.CALC || {}; CALC.views = CALC.views || {};
CALC.views.tiers = (function () {
  'use strict';
  const U = CALC.util, C = CALC.core;

  function mount(root, ctx) {
    const corpus = ctx.corpus;
    const vp = U.el('div', { class: 'vp' });
    vp.appendChild(U.el('div', { class: 'vp-head' },
      U.el('h2', { text: 'Tier ladder — the nine-level maturity scheme' }),
      U.el('p', { class: 'note', text: 'The scheme is the report’s own, derived from stated prerequisites, series placement, and reviews — column headers quote it verbatim. Colour deepens with tier. N18 sits in its tier greyed out: catalogued, verified, dropped.' })));
    const body = U.el('div', { class: 'vp-body' });
    const tl = U.el('div', { class: 'tl' });
    body.appendChild(tl); vp.appendChild(body); root.appendChild(vp);
    let chipEls = {};

    function render() {
      const vis = C.visibleIds(corpus, CALC.state.get());
      const buckets = C.tierBuckets(corpus.nodes, corpus.tiers);
      tl.replaceChildren(); chipEls = {};
      const curSel = CALC.state.get().sel;
      for (const t of corpus.tiers) {
        const col = U.el('div', { class: 'tl-col' });
        col.style.borderTopColor = U.tierStroke(t.tier);
        const h = U.el('div', { class: 'h' });
        h.appendChild(U.el('div', { class: 'tno', text: 'TIER ' + t.tier }));
        h.appendChild(U.el('div', { class: 'tnm', text: t.name }));
        h.appendChild(U.el('div', { class: 'trg', text: t.rigor }));
        h.appendChild(U.el('div', { class: 'tfo', text: t.focus }));
        col.appendChild(h);
        const scroll = U.el('div', { class: 'tl-scroll' });
        let shown = 0;
        for (const n of buckets[t.tier]) {
          const chip = U.el('button', { class: 'nodechip', 'data-id': n.id, title: n.title + ' — ' + n.authors,
            onclick: () => CALC.state.set({ sel: n.id }) });
          chip.style.borderLeftColor = U.tierStroke(n.tier);
          if (n.status === 'dropped') chip.style.opacity = '.45';
          if (n.id === curSel) chip.style.outline = '2px solid var(--ink)';
          chip.appendChild(U.el('span', { text: n.id + ' ' + U.shortTitle(n.title, 30) }));
          chip.appendChild(U.el('span', { class: 'yy', text: n.year }));
          if (n.status === 'dropped') chip.appendChild(U.el('span', { class: 'badge dropped', text: 'dropped' }));
          if (!vis.has(n.id)) chip.classList.add('hidden'); else shown++;
          scroll.appendChild(chip); chipEls[n.id] = chip;
        }
        if (!shown) scroll.appendChild(U.el('p', { class: 'empty', text: 'nothing matches' }));
        col.appendChild(scroll); tl.appendChild(col);
      }
    }
    function onSelect(sel) {
      for (const id in chipEls) chipEls[id].style.outline = id === sel ? '2px solid var(--ink)' : '';
    }
    render();
    return { applyFilters: render, onSelect, destroy: () => {} };
  }
  return { label: 'Tiers', mount };
})();
