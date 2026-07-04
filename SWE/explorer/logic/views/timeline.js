// views/timeline.js — Model 3: chronological strata (year of last publication; living docs own stratum).
window.SWE = window.SWE || {}; SWE.views = SWE.views || {};
SWE.views.timeline = (function () {
  'use strict';
  const U = SWE.util;
  function stratum(n) {
    if (n.year === 'living') return 'LIVING';
    const y = U.yearNum(n);
    if (y == null) return 'UNRESOLVED';
    if (y < 1980) return '≤ 1979';
    return Math.floor(y / 10) * 10 + 's';
  }
  const ORDER = ['≤ 1979', '1980s', '1990s', '2000s', '2010s', '2020s', 'LIVING', 'UNRESOLVED'];
  function mount(root) {
    root.appendChild(U.el('h2', { text: 'Chronology — year of last publication' }));
    root.appendChild(U.el('p', { class: 'viewnote', text:
      'Every report applies the same citation rule: cite the year of last publication. Living, continuously ' +
      'revised documents (toolchain manuals, vendor docs, MAB guidelines) are a real stratum of this literature, ' +
      'not a data defect; leads whose year the reports could not pin land in UNRESOLVED.' }));
    const host = U.el('div', { class: 'strata' });
    root.appendChild(host);
    function render() {
      const vis = SWE.search.visibleIds();
      host.innerHTML = '';
      const buckets = {};
      for (const n of SWE.corpus.nodes) {
        if (!vis.has(n.id)) continue;
        (buckets[stratum(n)] = buckets[stratum(n)] || []).push(n);
      }
      for (const s of ORDER) {
        const list = (buckets[s] || []).sort((a, b) =>
          (U.yearNum(a) || 0) - (U.yearNum(b) || 0) || a.title.localeCompare(b.title));
        if (!list.length) continue;
        const div = U.el('div', { class: 'stratum' });
        div.appendChild(U.el('div', { class: 'shead',
          text: s + ' — ' + list.length + ' resources' +
                (s === 'UNRESOLVED' ? ' (year unknown to the source reports)' : '') }));
        for (const n of list) {
          const chip = U.el('button', { class: 'nodechip', title: n.title + ' — ' + n.authors,
            onclick: () => SWE.detail.show(n.id) });
          chip.style.borderLeft = '3px solid ' + U.CORPUS_COLOR[n.corpora[0]];
          chip.appendChild(U.el('span', { text: U.shortTitle(n.title, 46) }));
          chip.appendChild(U.el('span', { class: 'yy', text: s === 'LIVING' ? 'living' : n.year }));
          if (n.verification === 'unverified') chip.appendChild(U.el('span', { class: 'badge unv', text: 'unv.' }));
          div.appendChild(chip);
        }
        host.appendChild(div);
      }
      if (!host.children.length) host.appendChild(U.el('p', { class: 'empty', text: 'nothing matches the current filters' }));
    }
    render();
    return { applyFilters: render };
  }
  return { label: 'Chronology', mount };
})();
