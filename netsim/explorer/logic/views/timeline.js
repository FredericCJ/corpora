// views/timeline.js — Model 3: chronology around the 2015 anchor datum (shell). Strata become
// columns that fill the pane; each scrolls internally. Living docs/tools are a real stratum;
// undated entries show their own recency tag instead of a guessed year.
window.NET = window.NET || {}; NET.views = NET.views || {};
NET.views.timeline = (function () {
  'use strict';
  const U = NET.util, C = NET.core;

  function mount(root, ctx) {
    const corpus = ctx.corpus;
    const vp = U.el('div', { class: 'vp' });
    vp.appendChild(U.el('div', { class: 'vp-head' },
      U.el('h2', { text: 'Chronology — strata around the 2015 anchor' }),
      U.el('p', { class: 'note', text: 'Years parsed from the citation strings (a “c. 2016–2018” takes its first year). Continuous/maintained documentation and tools are LIVING — a real stratum of this literature, not a defect. Entries whose year could not be parsed sit in UNDATED wearing their report-stated recency tag.' })));
    const body = U.el('div', { class: 'vp-body' });
    const tl = U.el('div', { class: 'cols-x' });
    body.appendChild(tl); vp.appendChild(body); root.appendChild(vp);
    let chipEls = {};

    function render() {
      const vis = C.visibleIds(corpus, NET.state.get());
      const buckets = C.strataBuckets(corpus.nodes.filter((n) => vis.has(n.id)));
      tl.replaceChildren(); chipEls = {};
      const curSel = NET.state.get().sel;
      let any = false;
      for (const s of C.STRATA) {
        const list = buckets[s]; if (!list || !list.length) continue;
        any = true;
        const col = U.el('div', { class: 'colv' });
        col.style.borderTopColor = s === '2015 · anchor' ? 'var(--accent)' : 'var(--faint)';
        const h = U.el('div', { class: 'h' });
        h.appendChild(U.el('div', { class: 'k', text: s + ' · ' + list.length }));
        col.appendChild(h);
        const scroll = U.el('div', { class: 'colv-scroll' });
        for (const n of list) {
          const chip = U.el('button', { class: 'nodechip' + (n.quarantined ? ' quar' : ''), 'data-id': n.id,
            title: n.title + ' — ' + n.cite.slice(0, 90), onclick: () => NET.state.set({ sel: n.id }) });
          chip.style.borderLeftColor = U.hueStroke(n);
          if (n.id === curSel) chip.style.outline = '2px solid var(--ink)';
          chip.appendChild(U.el('span', { text: U.shortTitle(n.title, 38) }));
          chip.appendChild(U.el('span', { class: 'yy',
            text: n.living ? 'living' : (n.year != null ? String(n.year) : n.recencyRaw) }));
          if (n.verification !== 'verified-web') chip.appendChild(U.el('span', {
            class: 'badge ' + U.VER_CLS[n.verification], text: n.verification === 'unverified' ? 'unv' : 'train' }));
          scroll.appendChild(chip); chipEls[n.id] = chip;
        }
        col.appendChild(scroll); tl.appendChild(col);
      }
      if (!any) tl.appendChild(U.el('p', { class: 'empty', text: 'nothing matches the current filters' }));
    }
    function onSelect(sel) {
      for (const id in chipEls) chipEls[id].style.outline = id === sel ? '2px solid var(--ink)' : '';
    }
    render();
    return { applyFilters: render, onSelect, destroy: () => {} };
  }
  return { label: 'Chronology', mount };
})();
