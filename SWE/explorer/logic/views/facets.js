// views/facets.js — Model 2: classification lattice (shell). Pure counts from core.facetCount;
// facet rail + internally-scrolling result list, fitted to the pane.
window.SWE = window.SWE || {}; SWE.views = SWE.views || {};
SWE.views.facets = (function () {
  'use strict';
  const U = SWE.util, C = SWE.core;
  const FACETS = [['branches', 'branch'], ['themes', 'theme'], ['lang', 'language'], ['type', 'type'], ['role', 'role'], ['lane', 'ops lane'], ['scope', 'scope']];
  const CHUNK = 160;

  function mount(root, ctx) {
    const corpus = ctx.corpus;
    const sel = {}; let shown = CHUNK;

    const vp = U.el('div', { class: 'vp' });
    vp.appendChild(U.el('div', { class: 'vp-head' },
      U.el('h2', { text: 'Facet browser — corpus × branch × theme × type' }),
      U.el('p', { class: 'note', text: 'Pure filtering over the phase-2 reconciled tags — no inference. Facets a report never asserts are simply absent for its nodes; UNRESOLVED appears only where a report flags a value unknown. Combines with the global search / verification / corpus filters.' })));
    const rail = U.el('div', { class: 'facet-rail' });
    const body = U.el('div', { class: 'vp-body' });
    const results = U.el('div', { class: 'results' });
    body.appendChild(results); vp.appendChild(rail); vp.appendChild(body); root.appendChild(vp);

    function render() {
      const vis = C.visibleIds(corpus, SWE.state.get());
      const base = corpus.nodes.filter((n) => vis.has(n.id));
      rail.replaceChildren();
      for (const [key, label] of FACETS) {
        const counts = C.facetCount(base, key, sel);
        if (!counts.size) continue;
        const bar = U.el('div', { class: 'facetbar' }, U.el('span', { class: 'lab', text: label }));
        [...counts.entries()].sort((a, b) => b[1] - a[1]).forEach(([v, c]) => {
          const chip = U.el('button', { class: 'chip clickable' + (sel[key] === v ? ' sel' : '') + (v === 'UNRESOLVED' ? ' unres' : ''),
            text: v + ' · ' + c, onclick: () => { sel[key] = sel[key] === v ? null : v; shown = CHUNK; render(); } });
          bar.appendChild(chip);
        });
        rail.appendChild(bar);
      }
      const rows = base.filter((n) => C.passLocal(n, sel, null)).sort((a, b) => a.title.localeCompare(b.title));
      results.replaceChildren();
      results.appendChild(U.el('p', { class: 'rescount', text: rows.length + ' resources match' }));
      const ul = U.el('ul', { class: 'rows' });
      const curSel = SWE.state.get().sel;
      rows.slice(0, shown).forEach((n) => {
        const li = U.el('li', { class: 'row' + (n.id === curSel ? ' sel' : ''), tabindex: '0', role: 'button', 'data-id': n.id,
          onclick: () => SWE.state.set({ sel: n.id }), onkeydown: (ev) => { if (ev.key === 'Enter' || ev.key === ' ') { ev.preventDefault(); SWE.state.set({ sel: n.id }); } } });
        if (n.id === curSel) li.style.outline = '2px solid var(--ink)';
        const l1 = U.el('div'); l1.appendChild(U.el('span', { class: 't', text: U.shortTitle(n.title, 70) }));
        U.badges(n).slice(0, 3).forEach((b) => l1.appendChild(b));
        li.appendChild(l1);
        li.appendChild(U.el('div', { class: 'a', text: n.authors + ' · ' + n.year + (n.ident ? ' · ' + n.ident : '') }));
        const l3 = U.el('div'); U.corpusChips(n).forEach((c) => l3.appendChild(c));
        (n.themes || []).slice(0, 3).forEach((t) => l3.appendChild(U.el('span', { class: 'chip', text: t })));
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
