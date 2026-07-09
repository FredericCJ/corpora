// views/anchor.js — Model 1: the anchor map (shell). The 2015 anchor volume's six parts as
// columns, each holding the GEN sections that expand/supersede/post-date it (relation phrases
// quoted from the section headers), plus "beyond the anchor" and the meta routes. Membership
// only — core.anchorColumns does no inference.
window.NET = window.NET || {}; NET.views = NET.views || {};
NET.views.anchor = (function () {
  'use strict';
  const U = NET.util, C = NET.core;

  function mount(root, ctx) {
    const corpus = ctx.corpus, relations = ctx.relations;
    const anchor = corpus.nodes.find((n) => n.id === 'anchor');

    const vp = U.el('div', { class: 'vp' });
    vp.appendChild(U.el('div', { class: 'vp-head' },
      U.el('h2', { text: 'Anchor map — the 2015 volume vs everything since' }),
      U.el('p', { class: 'note', text: 'Columns are the anchor’s six parts plus what lies beyond them. Section cards quote each route’s own header relation (“expansion axis”, “supersedes the anchor’s ns-2 era”, “did not exist at anchor time”); part verdicts quote the coverage summary. Chips are entry item numbers, coloured by subfield — click any for the full record. The quarantine column lives in Triage.' })));
    const body = U.el('div', { class: 'vp-body' });
    const cols = U.el('div', { class: 'cols-x' });
    body.appendChild(cols); vp.appendChild(body); root.appendChild(vp);

    const chipEls = {};

    function render() {
      cols.replaceChildren();
      const curSel = NET.state.get().sel;

      // leading column: the anchor itself
      const ac = U.el('div', { class: 'colv' });
      ac.style.borderTopColor = 'var(--accent)';
      const ah = U.el('div', { class: 'h' });
      ah.appendChild(U.el('div', { class: 'k', text: 'the anchor · 2015' }));
      ah.appendChild(U.el('div', { class: 't', text: 'Modeling and Simulation of Computer Networks and Systems' }));
      ac.appendChild(ah);
      const asc = U.el('div', { class: 'colv-scroll' });
      const acard = U.el('div', { class: 'card', tabindex: '0', role: 'button',
        onclick: () => NET.state.set({ sel: 'anchor' }),
        onkeydown: (ev) => { if (ev.key === 'Enter' || ev.key === ' ') { ev.preventDefault(); NET.state.set({ sel: 'anchor' }); } } });
      if (curSel === 'anchor') acard.style.outline = '2px solid var(--ink)';
      acard.appendChild(U.el('h4', { text: 'Obaidat · Zarai · Nicopolitidis (eds.)' }));
      acard.appendChild(U.el('p', { text: 'Morgan Kaufmann/Elsevier, 2015 · 964 pp. · ISBN 978-0-12-800887-4 · VERIFIED [WEB 2026-07-09]' }));
      asc.appendChild(acard);
      asc.appendChild(U.el('p', { class: 'empty', text: 'Six parts; every column to the right is a stated relation to one of them — or to none.' }));
      ac.appendChild(asc); cols.appendChild(ac);

      for (const col of C.anchorColumns(corpus, relations)) {
        if (col.part === 'quarantine') continue; // triaged in model 5
        const cv = U.el('div', { class: 'colv' });
        cv.style.borderTopColor = col.part.startsWith('p') ? 'var(--c-gen)' : 'var(--faint)';
        const h = U.el('div', { class: 'h' });
        h.appendChild(U.el('div', { class: 'k', text: col.label }));
        if (col.verdict) h.appendChild(U.el('div', { class: 'v', text: col.verdict }));
        cv.appendChild(h);
        const scroll = U.el('div', { class: 'colv-scroll' });
        for (const sec of col.sections) {
          const card = U.el('div', { class: 'seccard' });
          card.appendChild(U.el('div', { class: 'sh', text: '§' + sec.no + ' ' + sec.title }));
          card.appendChild(U.el('div', { class: 'sr', text: sec.relation }));
          const grid = U.el('div', { class: 'chipgrid' });
          for (const n of sec.members) {
            const chip = U.idChip(n, () => NET.state.set({ sel: n.id }));
            if (n.id === curSel) chip.classList.add('sel');
            grid.appendChild(chip); chipEls[n.id] = chip;
          }
          card.appendChild(grid);
          scroll.appendChild(card);
        }
        if (!col.sections.length) scroll.appendChild(U.el('p', { class: 'empty', text: 'no routes' }));
        cv.appendChild(scroll); cols.appendChild(cv);
      }
      applyFilters();
    }

    function applyFilters() {
      const vis = C.visibleIds(corpus, NET.state.get());
      for (const id in chipEls) chipEls[id].classList.toggle('off', !vis.has(id));
    }
    function onSelect(sel) {
      for (const id in chipEls) chipEls[id].classList.toggle('sel', id === sel);
    }
    render();
    return { applyFilters, onSelect, destroy: () => {} };
  }
  return { label: 'Anchor map', mount };
})();
