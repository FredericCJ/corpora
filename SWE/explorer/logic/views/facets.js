// views/facets.js — Model 2: classification lattice (shell). Pure counts from core.facetCount;
// facet rail + internally-scrolling result list, fitted to the pane.
window.SWE = window.SWE || {}; SWE.views = SWE.views || {};
SWE.views.facets = (function () {
  'use strict';
  const U = SWE.util, C = SWE.core;
  const FACETS = [['branches', 'branch'], ['themes', 'theme'], ['stages', 'spine stage'], ['domains', 'spine domain'], ['lang', 'language'], ['type', 'type'], ['role', 'role'], ['lane', 'ops lane'], ['scope', 'scope']];
  const CHUNK = 160;

  function mount(root, ctx) {
    const corpus = ctx.corpus;
    const EL = ctx.elIndex;                 // element bridge (may be absent)
    const TOTAL = corpus.nodes.length;      // full BoK — every work reachable via empty selection
    const sel = {}; let teachSel = null; let shown = CHUNK;
    // teaches facet — realm(s) a work grounds, or 'none'; derived read-only from the element index
    // (no core hack, no synthetic node field), so C.facetCount/passLocal stay pure over real tags.
    const teachValues = (n) => {
      const els = (EL && EL.elementsByWork[n.id]) || [];
      if (!els.length) return ['none'];
      const out = [];
      if (els.some((eid) => EL.byId[eid] && EL.byId[eid].realm === 'design')) out.push('design');
      if (els.some((eid) => EL.byId[eid] && EL.byId[eid].realm === 'architecture')) out.push('architecture');
      return out.length ? out : ['none'];
    };
    const teachPass = (n) => !teachSel || teachValues(n).includes(teachSel);

    const vp = U.el('div', { class: 'vp' });
    vp.appendChild(U.el('div', { class: 'vp-head' },
      U.el('h2', { text: 'Facet browser — corpus × branch × theme × type' }),
      U.el('p', { class: 'note', text: 'Pure filtering over the phase-2 reconciled tags — no inference. Facets a report never asserts are simply absent for its nodes; UNRESOLVED appears only where a report flags a value unknown. Combines with the global search / verification / corpus filters.' })));
    const rail = U.el('div', { class: 'facet-rail' });
    const body = U.el('div', { class: 'vp-body' });
    const results = U.el('div', { class: 'results' });
    body.appendChild(results); vp.appendChild(rail); vp.appendChild(body); root.appendChild(vp);

    function render() {
      const state = SWE.state.get();
      const vis = C.visibleIds(corpus, state);
      const base = corpus.nodes.filter((n) => vis.has(n.id));
      const railBase = base.filter(teachPass);   // real-tag facets honour the teaches selection
      rail.replaceChildren();
      for (const [key, label] of FACETS) {
        const counts = C.facetCount(railBase, key, sel);
        if (!counts.size) continue;
        const bar = U.el('div', { class: 'facetbar' }, U.el('span', { class: 'lab', text: label }));
        [...counts.entries()].sort((a, b) => b[1] - a[1]).forEach(([v, c]) => {
          const chip = U.el('button', { class: 'chip clickable' + (sel[key] === v ? ' sel' : '') + (v === 'UNRESOLVED' ? ' unres' : ''),
            text: v + ' · ' + c, onclick: () => { sel[key] = sel[key] === v ? null : v; shown = CHUNK; render(); } });
          bar.appendChild(chip);
        });
        rail.appendChild(bar);
      }
      if (EL) {   // teaches facet — counts honour the real-tag selection (exceptKey = teaches itself)
        const tc = new Map();
        for (const n of base) if (C.passLocal(n, sel, null)) for (const v of teachValues(n)) tc.set(v, (tc.get(v) || 0) + 1);
        if (tc.size) {
          const bar = U.el('div', { class: 'facetbar' }, U.el('span', { class: 'lab', text: 'teaches' }));
          const ORDER = ['design', 'architecture', 'none'];
          [...tc.entries()].sort((a, b) => ORDER.indexOf(a[0]) - ORDER.indexOf(b[0])).forEach(([v, c]) => {
            const chip = U.el('button', { class: 'chip clickable' + (teachSel === v ? ' sel' : ''),
              text: v + ' · ' + c, onclick: () => { teachSel = teachSel === v ? null : v; shown = CHUNK; render(); } });
            bar.appendChild(chip);
          });
          rail.appendChild(bar);
        }
      }
      const rows = base.filter((n) => teachPass(n) && C.passLocal(n, sel, null)).sort((a, b) => a.title.localeCompare(b.title));
      results.replaceChildren();
      const localEmpty = !teachSel && Object.keys(sel).every((k) => !sel[k]);
      const globalActive = !!((state.q && state.q.trim()) || state.ver || state.corpus);
      const head = U.el('p', { class: 'rescount', text: rows.length + ' of ' + TOTAL + ' match' });
      if (localEmpty && !globalActive) head.appendChild(U.el('span', { class: 'reach',
        text: ' · no facet chosen — all ' + TOTAL + ' works reachable; “show more” pages the full set' }));
      results.appendChild(head);
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
        const teaches = ((EL && EL.elementsByWork[n.id]) || []).length;   // element bridge
        if (teaches > 0) l3.appendChild(U.el('button', { class: 'chip teach-chip', text: 'teaches ' + teaches,
          title: 'inspect the ' + teaches + ' elements this work grounds',
          onclick: (ev) => { ev.stopPropagation(); SWE.state.set({ sel: n.id }); } }));
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
