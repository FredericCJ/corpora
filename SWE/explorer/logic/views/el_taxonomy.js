// views/el_taxonomy.js — Element view 1: the realm × kind × tag lattice (shell). Pure counts from
// SWE.core.facetCount over element nodes; facet rail + internally-scrolling result list. Every
// element is reachable here (and through search). Page scroll is authorized for element views;
// this one keeps the house internal-scroll form since it fits.
window.SWE = window.SWE || {}; SWE.views = SWE.views || {};
SWE.views['el-taxonomy'] = (function () {
  'use strict';
  const U = SWE.util, C = SWE.core, CE = SWE.coreEl;
  const FACETS = [['realm', 'realm'], ['kind', 'kind'], ['confidence', 'confidence'], ['qa', 'quality attribute'], ['tags', 'tag']];
  const CHUNK = 140;

  function mount(root, ctx) {
    const idx = ctx.elIndex;
    const sel = {}; let shown = CHUNK;
    const meta = CE.VIEWS['el-taxonomy'];

    const vp = U.el('div', { class: 'vp' });
    vp.appendChild(U.el('div', { class: 'vp-head' },
      U.el('h2', { text: 'Element taxonomy — realm × kind × tag' }),
      U.el('p', { class: 'note', text: meta.semantic + ' ' + meta.computed })));
    const rail = U.el('div', { class: 'facet-rail' });
    const body = U.el('div', { class: 'vp-body' });
    const results = U.el('div', { class: 'results' });
    body.appendChild(results); vp.appendChild(rail); vp.appendChild(body); root.appendChild(vp);

    function render() {
      const vis = CE.visible(idx, SWE.state.get().q);
      const base = idx.nodes.filter((n) => vis.has(n.id));
      rail.replaceChildren();
      for (const [key, label] of FACETS) {
        const counts = C.facetCount(base, key, sel);
        if (!counts.size) continue;
        const bar = U.el('div', { class: 'facetbar' }, U.el('span', { class: 'lab', text: label }));
        const entries = [...counts.entries()].sort((a, b) => b[1] - a[1]);
        (key === 'tags' ? entries.slice(0, 24) : entries).forEach(([v, c]) => {
          bar.appendChild(U.el('button', { class: 'chip clickable' + (sel[key] === v ? ' sel' : '') + (v === 'design' ? ' re-design' : v === 'architecture' ? ' re-arch' : ''),
            text: v + ' · ' + c, onclick: () => { sel[key] = sel[key] === v ? null : v; shown = CHUNK; render(); } }));
        });
        if (key === 'tags' && entries.length > 24) bar.appendChild(U.el('span', { class: 'chip', text: '+' + (entries.length - 24) + ' more tags (search)' }));
        rail.appendChild(bar);
      }
      const rows = base.filter((n) => C.passLocal(n, sel, null)).sort((a, b) => a.realm.localeCompare(b.realm) || a.kind.localeCompare(b.kind) || a.name.localeCompare(b.name));
      results.replaceChildren();
      results.appendChild(U.el('p', { class: 'rescount', text: rows.length + ' elements match' }));
      const ul = U.el('ul', { class: 'rows' });
      const curSel = SWE.state.get().sel;
      rows.slice(0, shown).forEach((n) => {
        const li = U.el('li', { class: 'row' + (n.id === curSel ? ' sel' : ''), tabindex: '0', role: 'button', 'data-id': n.id,
          onclick: () => SWE.state.set({ sel: n.id }), onkeydown: (ev) => { if (ev.key === 'Enter' || ev.key === ' ') { ev.preventDefault(); SWE.state.set({ sel: n.id }); } } });
        if (n.id === curSel) li.style.outline = '2px solid var(--ink)';
        const l1 = U.el('div'); l1.appendChild(U.el('span', { class: 't', text: U.shortTitle(n.name, 60) }));
        U.elChips(n).forEach((c) => l1.appendChild(c));
        li.appendChild(l1);
        li.appendChild(U.el('div', { class: 'a', text: U.shortTitle(n.what, 118) }));
        const l3 = U.el('div'); U.elBadges(n).slice(0, 4).forEach((b) => l3.appendChild(b));
        if (n.works && n.works.length) l3.appendChild(U.el('span', { class: 'chip', text: n.works.length + ' work' + (n.works.length > 1 ? 's' : '') }));
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
  return { label: 'Element taxonomy', mount };
})();
