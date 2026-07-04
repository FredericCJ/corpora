// views/facets.js — Model 2: classification lattice with live counts + chunked result list.
window.SWE = window.SWE || {}; SWE.views = SWE.views || {};
SWE.views.facets = (function () {
  'use strict';
  const U = SWE.util;
  const FACETS = [
    ['branches', 'branch'], ['themes', 'theme'], ['type', 'type'],
    ['role', 'role'], ['lane', 'ops lane'], ['scope', 'scope (emb-arch)']];
  const CHUNK = 150;
  const sel = {};   // local facet selections: facetKey -> value

  function valuesOf(n, key) {
    const v = n[key];
    if (v == null) return [];
    return Array.isArray(v) ? v : [v];
  }
  function passLocal(n, exceptKey) {
    for (const k in sel) {
      if (!sel[k] || k === exceptKey) continue;
      if (!valuesOf(n, k).includes(sel[k])) return false;
    }
    return true;
  }
  function mount(root) {
    root.appendChild(U.el('h2', { text: 'Facet browser — corpus × branch × theme × type' }));
    root.appendChild(U.el('p', { class: 'viewnote', text:
      'Pure filtering over the PHASE-2 reconciled tags — no inference. Facets a report never asserts are simply ' +
      'absent for its nodes; UNRESOLVED appears only where a report itself flags a value unknown. Combine with the ' +
      'global search / verification / corpus filters in the toolbar.' }));
    const facetHost = U.el('div');
    const listHost = U.el('div');
    root.appendChild(facetHost); root.appendChild(listHost);
    let shown = CHUNK;

    function render() {
      const vis = SWE.search.visibleIds();
      const base = SWE.corpus.nodes.filter(n => vis.has(n.id));
      facetHost.innerHTML = '';
      for (const [key, label] of FACETS) {
        const counts = new Map();
        for (const n of base) if (passLocal(n, key))
          for (const v of valuesOf(n, key)) counts.set(v, (counts.get(v) || 0) + 1);
        if (!counts.size) continue;
        const bar = U.el('div', { class: 'facetbar' }, U.el('span', { class: 'lab', text: label }));
        [...counts.entries()].sort((a, b) => b[1] - a[1]).forEach(([v, c]) => {
          const chip = U.el('button', { class: 'chip plain clickable' + (sel[key] === v ? ' sel' : ''),
            text: v + ' · ' + c,
            onclick: () => { sel[key] = sel[key] === v ? null : v; shown = CHUNK; render(); } });
          if (v === 'UNRESOLVED') chip.classList.add('unres');
          bar.appendChild(chip);
        });
        facetHost.appendChild(bar);
      }
      const rows = base.filter(n => passLocal(n, null))
        .sort((a, b) => a.title.localeCompare(b.title));
      listHost.innerHTML = '';
      listHost.appendChild(U.el('p', { class: 'meta', text: rows.length + ' resources match' }));
      const ul = U.el('ul', { class: 'rows' });
      rows.slice(0, shown).forEach(n => {
        const li = U.el('li', { class: 'row', tabindex: '0', role: 'button',
          onclick: () => SWE.detail.show(n.id),
          onkeydown: ev => { if (ev.key === 'Enter') SWE.detail.show(n.id); } });
        const line1 = U.el('div');
        line1.appendChild(U.el('span', { class: 't', text: n.title }));
        U.badges(n).forEach(b => line1.appendChild(b));
        li.appendChild(line1);
        const line2 = U.el('div', { class: 'a', text: n.authors + ' · ' + n.year + (n.ident ? ' · ' + n.ident : '') });
        li.appendChild(line2);
        const line3 = U.el('div');
        U.corpusChips(n).forEach(c => line3.appendChild(c));
        (n.themes || []).slice(0, 4).forEach(t =>
          line3.appendChild(U.el('span', { class: 'chip plain', text: t })));
        li.appendChild(line3);
        ul.appendChild(li);
      });
      listHost.appendChild(ul);
      if (rows.length > shown)
        listHost.appendChild(U.el('button', { class: 'morebtn',
          text: 'show ' + Math.min(CHUNK, rows.length - shown) + ' more (of ' + (rows.length - shown) + ')',
          onclick: () => { shown += CHUNK; render(); } }));
    }
    render();
    return { applyFilters: render };
  }
  return { label: 'Facets', mount };
})();
