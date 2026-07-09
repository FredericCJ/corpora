// views/matlab.js — Model 4: the MATLAB/Simulink lens (shell). The intersection corpus organized
// by its six paradigms; stratum rides every card; the load-bearing packaging-migration note is a
// persistent banner. Cross-corpus entries link back into the general corpus via their chips.
window.NET = window.NET || {}; NET.views = NET.views || {};
NET.views.matlab = (function () {
  'use strict';
  const U = NET.util, C = NET.core;

  function mount(root, ctx) {
    const corpus = ctx.corpus;
    const vp = U.el('div', { class: 'vp' });
    vp.appendChild(U.el('div', { class: 'vp-head' },
      U.el('h2', { text: 'MATLAB lens — where MATLAB/Simulink is a real network-M&S vehicle' }),
      U.el('p', { class: 'note', text: 'The intersection corpus by its six paradigms. Its own verdict: a minority tool whose value is paradigm-specific — hybrid control+network, coexistence, standards-based wireless KPIs, satellite scenarios — rather than general-purpose packet simulation. Multi-paradigm entries appear in each of their columns.' })));
    const banner = U.el('div', { class: 'banner' });
    banner.appendChild(U.el('b', { text: 'Packaging note (anti-fabrication, verified live): ' }));
    banner.appendChild(document.createTextNode(corpus.corpora.mat.packagingNote));
    vp.appendChild(banner);
    const body = U.el('div', { class: 'vp-body' });
    const cols = U.el('div', { class: 'cols-x' });
    body.appendChild(cols); vp.appendChild(body); root.appendChild(vp);

    const cardEls = {};

    function render() {
      const buckets = C.paradigmBuckets(corpus.nodes, corpus.paradigms);
      cols.replaceChildren();
      const curSel = NET.state.get().sel;
      for (const p of corpus.paradigms) {
        const list = buckets[p];
        const col = U.el('div', { class: 'colv' });
        col.style.borderTopColor = U.parStroke(p);
        const h = U.el('div', { class: 'h' });
        h.appendChild(U.el('div', { class: 'k', text: p + ' · ' + list.length }));
        col.appendChild(h);
        const scroll = U.el('div', { class: 'colv-scroll' });
        for (const n of list) {
          const card = U.el('div', { class: 'card' + (n.quarantined ? ' quar' : ''), tabindex: '0', role: 'button',
            'data-id': n.id, onclick: () => NET.state.set({ sel: n.id }),
            onkeydown: (ev) => { if (ev.key === 'Enter' || ev.key === ' ') { ev.preventDefault(); NET.state.set({ sel: n.id }); } } });
          card.style.borderLeftColor = U.parStroke(p);
          if (n.id === curSel) card.style.outline = '2px solid var(--ink)';
          card.appendChild(U.el('h4', { text: U.shortTitle(n.title, 56) }));
          card.appendChild(U.el('p', { text: U.shortTitle(n.cite, 80) }));
          const b = U.el('p');
          if (n.stratum) b.appendChild(U.el('span', { class: 'badge plain', text: n.stratum }));
          U.badges(n).slice(0, 1).forEach((x) => b.appendChild(x));
          if (n.corpus.length > 1) b.appendChild(U.el('span', { class: 'badge plain', text: '↔ gen item ' + n.item.gen }));
          card.appendChild(b);
          scroll.appendChild(card);
          (cardEls[n.id] = cardEls[n.id] || []).push(card);
        }
        if (!list.length) scroll.appendChild(U.el('p', { class: 'empty', text: 'no entries' }));
        col.appendChild(scroll); cols.appendChild(col);
      }
      applyFilters();
    }

    function applyFilters() {
      const vis = C.visibleIds(corpus, NET.state.get());
      for (const id in cardEls) for (const c of cardEls[id]) c.classList.toggle('dimmed', !vis.has(id));
    }
    function onSelect(sel) {
      for (const id in cardEls) for (const c of cardEls[id]) c.style.outline = id === sel ? '2px solid var(--ink)' : '';
    }
    render();
    return { applyFilters, onSelect, destroy: () => {} };
  }
  return { label: 'MATLAB lens', mount };
})();
