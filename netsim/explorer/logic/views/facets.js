// views/facets.js — Model 2: the tag lattice (shell). Pure counts from core.facetCount;
// facet rail + internally-scrolling result list, fitted to the pane.
window.NET = window.NET || {}; NET.views = NET.views || {};
NET.views.facets = (function () {
  'use strict';
  const U = NET.util, C = NET.core;
  const FACETS = [['corpus', 'corpus'], ['subfield', 'subfield'], ['paradigm', 'paradigm'],
                  ['type', 'type'], ['stratum', 'stratum'], ['recency', 'recency']];
  const CHUNK = 120;

  function mount(root, ctx) {
    const corpus = ctx.corpus;
    const sel = {}; let shown = CHUNK;

    const vp = U.el('div', { class: 'vp' });
    vp.appendChild(U.el('div', { class: 'vp-head' },
      U.el('h2', { text: 'Facets — corpus × subfield/paradigm × type/stratum × recency' }),
      U.el('p', { class: 'note', text: 'Pure filtering over the tags the reports themselves enforce scope with — no inference. Subfields belong to the GEN legend, paradigms and strata to the MAT legend; entries carry only what their report asserts. Combines with the global search / verification / corpus filters.' })));
    const rail = U.el('div', { class: 'facet-rail' });
    const body = U.el('div', { class: 'vp-body' });
    const results = U.el('div', { class: 'results' });
    body.appendChild(results); vp.appendChild(rail); vp.appendChild(body); root.appendChild(vp);

    function render() {
      const vis = C.visibleIds(corpus, NET.state.get());
      const base = corpus.nodes.filter((n) => vis.has(n.id));
      rail.replaceChildren();
      for (const [key, label] of FACETS) {
        const counts = C.facetCount(base, key, sel);
        if (!counts.size) continue;
        const bar = U.el('div', { class: 'facetbar' }, U.el('span', { class: 'lab', text: label }));
        [...counts.entries()].sort((a, b) => b[1] - a[1]).forEach(([v, c]) => {
          bar.appendChild(U.el('button', { class: 'chip clickable' + (sel[key] === v ? ' sel' : ''),
            text: v + ' · ' + c, onclick: () => { sel[key] = sel[key] === v ? null : v; shown = CHUNK; render(); } }));
        });
        rail.appendChild(bar);
      }
      const rows = base.filter((n) => C.passLocal(n, sel, null))
        .sort((a, b) => a.title.localeCompare(b.title));
      results.replaceChildren();
      results.appendChild(U.el('p', { class: 'rescount', text: rows.length + ' entries match' }));
      const ul = U.el('ul', { class: 'rows' });
      const curSel = NET.state.get().sel;
      rows.slice(0, shown).forEach((n) => {
        const li = U.el('li', { class: 'row', tabindex: '0', role: 'button', 'data-id': n.id,
          onclick: () => NET.state.set({ sel: n.id }),
          onkeydown: (ev) => { if (ev.key === 'Enter' || ev.key === ' ') { ev.preventDefault(); NET.state.set({ sel: n.id }); } } });
        if (n.id === curSel) li.style.outline = '2px solid var(--ink)';
        const l1 = U.el('div'); l1.appendChild(U.el('span', { class: 't', text: U.shortTitle(n.title, 68) }));
        U.badges(n).slice(0, 2).forEach((b) => l1.appendChild(b));
        li.appendChild(l1);
        li.appendChild(U.el('div', { class: 'a', text: U.shortTitle(n.cite, 100) }));
        const l3 = U.el('div'); U.corpusChips(n).forEach((c) => l3.appendChild(c));
        [...n.subfield, ...n.paradigm].slice(0, 3).forEach((t) => l3.appendChild(U.el('span', { class: 'chip', text: t })));
        li.appendChild(l3);
        ul.appendChild(li);
      });
      results.appendChild(ul);
      if (rows.length > shown) results.appendChild(U.el('button', { class: 'morebtn',
        text: 'show ' + Math.min(CHUNK, rows.length - shown) + ' more (of ' + (rows.length - shown) + ')',
        onclick: () => { shown += CHUNK; render(); } }));
    }
    render();
    return { applyFilters: render, onSelect: () => render(), destroy: () => {} };
  }
  return { label: 'Facets', mount };
})();
