// views/overlap.js — Model 4: cross-corpus overlap (graft points between the passes).
window.SWE = window.SWE || {}; SWE.views = SWE.views || {};
SWE.views.overlap = (function () {
  'use strict';
  const U = SWE.util;
  const ORDER = ['swa-science', 'emb-arch', 'emb-c', 'emb-cpp', 'emb-ops', 'simulink'];
  function mount(root) {
    root.appendChild(U.el('h2', { text: 'Cross-corpus overlap — the graft points' }));
    root.appendChild(U.el('p', { class: 'viewnote', text:
      'The reports required overlap between passes to be preserved and tagged, not dropped. These are the works ' +
      'claimed by two or more corpora after merging — including memberships added because one report listed as an ' +
      'unverified lead a work another report verified (marked “lead” on the chip).' }));
    const host = U.el('div'); root.appendChild(host);
    function render() {
      const vis = SWE.search.visibleIds();
      host.innerHTML = '';
      const multi = SWE.corpus.nodes.filter(n => n.corpora.length > 1 && vis.has(n.id));
      // pairwise matrix
      const pair = {};
      for (const n of multi)
        for (let i = 0; i < n.corpora.length; i++)
          for (let j = i + 1; j < n.corpora.length; j++) {
            const k = [n.corpora[i], n.corpora[j]].sort().join('|');
            pair[k] = (pair[k] || 0) + 1;
          }
      const tbl = U.el('table', { class: 'matrix' });
      const hr = U.el('tr', {}, U.el('th', { text: '∩' }));
      ORDER.forEach(c => hr.appendChild(U.el('th', { text: U.CORPUS_SHORT[c] })));
      tbl.appendChild(hr);
      for (const a of ORDER) {
        const tr = U.el('tr', {}, U.el('th', { text: U.CORPUS_SHORT[a] }));
        for (const b of ORDER) {
          if (a === b) { tr.appendChild(U.el('td', { text: '—' })); continue; }
          const v = pair[[a, b].sort().join('|')] || 0;
          tr.appendChild(U.el('td', { text: String(v), class: v >= 4 ? 'hot' : '' }));
        }
        tbl.appendChild(tr);
      }
      host.appendChild(U.el('p', { class: 'meta', text: multi.length + ' works span ≥ 2 corpora (of the currently visible set)' }));
      host.appendChild(tbl);
      // signature groups
      const groups = {};
      for (const n of multi) {
        const sig = ORDER.filter(c => n.corpora.includes(c)).join(' + ');
        (groups[sig] = groups[sig] || []).push(n);
      }
      Object.entries(groups)
        .sort((a, b) => b[1].length - a[1].length || b[0].split('+').length - a[0].split('+').length)
        .forEach(([sig, list]) => {
          host.appendChild(U.el('h3', { text: sig.split(' + ').map(c => U.CORPUS_SHORT[c]).join(' + ') + ' · ' + list.length }));
          const ul = U.el('ul', { class: 'rows' });
          list.sort((a, b) => a.title.localeCompare(b.title)).forEach(n => {
            const li = U.el('li', { class: 'row', tabindex: '0', role: 'button',
              onclick: () => SWE.detail.show(n.id),
              onkeydown: ev => { if (ev.key === 'Enter') SWE.detail.show(n.id); } });
            const l1 = U.el('div');
            l1.appendChild(U.el('span', { class: 't', text: n.title }));
            U.badges(n).forEach(b => l1.appendChild(b));
            li.appendChild(l1);
            li.appendChild(U.el('div', { class: 'a', text: n.authors + ' · ' + n.year }));
            const l3 = U.el('div'); U.corpusChips(n).forEach(c => l3.appendChild(c)); li.appendChild(l3);
            ul.appendChild(li);
          });
          host.appendChild(ul);
        });
      if (!multi.length) host.appendChild(U.el('p', { class: 'empty', text: 'nothing matches the current filters' }));
    }
    render();
    return { applyFilters: render };
  }
  return { label: 'Overlap', mount };
})();
