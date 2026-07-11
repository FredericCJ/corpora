// views/overlap.js — Model 4: cross-corpus overlap (shell). Pairwise matrix + signature groups
// from core.overlapPairs / signatureGroups. Matrix left, groups scroll on the right.
window.SWE = window.SWE || {}; SWE.views = SWE.views || {};
SWE.views.overlap = (function () {
  'use strict';
  const U = SWE.util, C = SWE.core;

  function mount(root, ctx) {
    const corpus = ctx.corpus;
    const elByWork = (ctx.elIndex && ctx.elIndex.elementsByWork) || {};
    const vp = U.el('div', { class: 'vp' });
    vp.appendChild(U.el('div', { class: 'vp-head' },
      U.el('h2', { text: 'Cross-corpus overlap — the graft points' }),
      U.el('p', { class: 'note', text: 'Works claimed by two or more passes after merging — the property unique to a unified corpus. Includes memberships added because one report listed as an unverified lead a work another report verified (marked “lead” on the chip).' })));
    const body = U.el('div', { class: 'vp-body' });
    const wrap = U.el('div', { class: 'overlap' });
    const mx = U.el('div', { class: 'mx' });
    const sig = U.el('div', { class: 'sig-scroll' });
    wrap.appendChild(mx); wrap.appendChild(sig); body.appendChild(wrap); vp.appendChild(body); root.appendChild(vp);

    function render() {
      const vis = C.visibleIds(corpus, SWE.state.get());
      const multi = corpus.nodes.filter((n) => n.corpora.length > 1 && vis.has(n.id));
      const pair = C.overlapPairs(multi);
      mx.replaceChildren();
      mx.appendChild(U.el('p', { class: 'rescount', text: multi.length + ' works span ≥ 2 corpora' }));
      const tbl = U.el('table', { class: 'matrix' });
      const hr = U.el('tr', {}, U.el('th', { text: '∩' }));
      U.CORPUS_ORDER.forEach((c) => hr.appendChild(U.el('th', { text: U.CORPUS_SHORT[c] })));
      tbl.appendChild(hr);
      for (const a of U.CORPUS_ORDER) {
        const tr = U.el('tr', {}, U.el('th', { text: U.CORPUS_SHORT[a] }));
        for (const b of U.CORPUS_ORDER) {
          if (a === b) { tr.appendChild(U.el('td', { text: '—' })); continue; }
          const v = pair[[a, b].sort().join('|')] || 0;
          tr.appendChild(U.el('td', { text: String(v), class: v >= 4 ? 'hot' : '' }));
        }
        tbl.appendChild(tr);
      }
      mx.appendChild(tbl);

      sig.replaceChildren();
      const curSel = SWE.state.get().sel;
      const groups = C.signatureGroups(multi, U.CORPUS_ORDER);
      const holder = U.el('div', { class: 'sig' });
      groups.forEach(([s, list]) => {
        holder.appendChild(U.el('h3', { text: s.split(' + ').map((c) => U.CORPUS_SHORT[c]).join(' + ') + ' · ' + list.length }));
        const ul = U.el('ul', { class: 'rows' });
        list.sort((a, b) => a.title.localeCompare(b.title)).forEach((n) => {
          const li = U.el('li', { class: 'row' + (n.id === curSel ? ' sel' : ''), tabindex: '0', role: 'button',
            onclick: () => SWE.state.set({ sel: n.id }), onkeydown: (ev) => { if (ev.key === 'Enter' || ev.key === ' ') { ev.preventDefault(); SWE.state.set({ sel: n.id }); } } });
          if (n.id === curSel) li.style.outline = '2px solid var(--ink)';
          const l1 = U.el('div'); l1.appendChild(U.el('span', { class: 't', text: U.shortTitle(n.title, 64) }));
          U.badges(n).slice(0, 2).forEach((b) => l1.appendChild(b));
          const teaches = (elByWork[n.id] || []).length;
          if (teaches) l1.appendChild(U.el('span', { class: 'teach', text: '◇' + teaches,
            title: 'grounds ' + teaches + ' element' + (teaches > 1 ? 's' : '') }));
          li.appendChild(l1);
          li.appendChild(U.el('div', { class: 'a', text: n.authors + ' · ' + n.year }));
          const l3 = U.el('div'); U.corpusChips(n).forEach((c) => l3.appendChild(c)); li.appendChild(l3);
          ul.appendChild(li);
        });
        holder.appendChild(ul);
      });
      if (!multi.length) holder.appendChild(U.el('p', { class: 'empty', text: 'nothing matches the current filters' }));
      sig.appendChild(holder);
    }
    render();
    return { applyFilters: render, onSelect: () => render(), destroy: () => {} };
  }
  return { label: 'Overlap', mount };
})();
