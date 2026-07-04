// views/timeline.js — Model 3: chronology (shell). Strata become columns that fill the pane; each
// column scrolls internally. Buckets from core.strataBuckets (year of last publication).
window.SWE = window.SWE || {}; SWE.views = SWE.views || {};
SWE.views.timeline = (function () {
  'use strict';
  const U = SWE.util, C = SWE.core;

  function mount(root, ctx) {
    const corpus = ctx.corpus;
    const vp = U.el('div', { class: 'vp' });
    vp.appendChild(U.el('div', { class: 'vp-head' },
      U.el('h2', { text: 'Chronology — year of last publication' }),
      U.el('p', { class: 'note', text: 'Every report cites the year of last publication. Living, continuously-revised documents (toolchain manuals, vendor docs, MAB guidelines) are a real stratum of this literature, not a defect; leads whose year the reports could not pin land in UNRESOLVED.' })));
    const body = U.el('div', { class: 'vp-body' });
    const tl = U.el('div', { class: 'tl' });
    body.appendChild(tl); vp.appendChild(body); root.appendChild(vp);
    let chipEls = {};

    function render() {
      const vis = C.visibleIds(corpus, SWE.state.get());
      const buckets = C.strataBuckets(corpus.nodes.filter((n) => vis.has(n.id)));
      tl.replaceChildren(); chipEls = {};
      const curSel = SWE.state.get().sel;
      let any = false;
      for (const s of C.STRATA) {
        const list = buckets[s]; if (!list || !list.length) continue;
        any = true;
        const col = U.el('div', { class: 'tl-col' });
        col.appendChild(U.el('div', { class: 'h' }, U.el('b', { text: s }), U.el('span', { text: ' · ' + list.length })));
        const scroll = U.el('div', { class: 'tl-scroll' });
        for (const n of list) {
          const chip = U.el('button', { class: 'nodechip' + (n.id === curSel ? ' sel' : ''), 'data-id': n.id, title: n.title + ' — ' + n.authors,
            onclick: () => SWE.state.set({ sel: n.id }) });
          chip.style.borderLeftColor = U.corpusStroke(n.corpora[0]);
          if (n.id === curSel) chip.style.outline = '2px solid var(--ink)';
          chip.appendChild(U.el('span', { text: U.shortTitle(n.title, 40) }));
          chip.appendChild(U.el('span', { class: 'yy', text: s === 'LIVING' ? 'living' : n.year }));
          if (n.verification === 'unverified') chip.appendChild(U.el('span', { class: 'badge unv', text: 'unv' }));
          scroll.appendChild(chip); chipEls[n.id] = chip;
        }
        col.appendChild(scroll); tl.appendChild(col);
      }
      if (!any) tl.appendChild(U.el('p', { class: 'empty', text: 'nothing matches the current filters' }));
    }
    function onSelect(sel) {
      for (const id in chipEls) { const on = id === sel; chipEls[id].classList.toggle('sel', on); chipEls[id].style.outline = on ? '2px solid var(--ink)' : ''; }
    }
    render();
    return { applyFilters: render, onSelect, destroy: () => {} };
  }
  return { label: 'Chronology', mount };
})();
