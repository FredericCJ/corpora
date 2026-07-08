// views/gate.js — Model 5: the quality gate (shell). The report's own editorial spine carried
// verbatim: TL;DR, the kept/dropped ledger (every candidate, one line of evidenced reasoning),
// the open register, and the caveats that bound what every other view may claim.
window.CALC = window.CALC || {}; CALC.views = CALC.views || {};
CALC.views.gate = (function () {
  'use strict';
  const U = CALC.util, C = CALC.core;

  function mount(root, ctx) {
    const corpus = ctx.corpus, relations = ctx.relations;
    const byId = {}; corpus.nodes.forEach((n) => { byId[n.id] = n; });

    const vp = U.el('div', { class: 'vp' });
    vp.appendChild(U.el('div', { class: 'vp-head' },
      U.el('h2', { text: 'Quality gate — why each text is in (or out)' }),
      U.el('p', { class: 'note', text: 'Carried verbatim from the report: the TL;DR, the quality-gate ledger (22 candidates, one evidenced reason each — one drop), the open register, and the caveats. The caveats bound every claim the other views make.' })));
    const body = U.el('div', { class: 'vp-body' });
    const scroll = U.el('div', { class: 'gate' });
    body.appendChild(scroll); vp.appendChild(body); root.appendChild(vp);

    const rowEls = [];

    function render() {
      scroll.replaceChildren(); rowEls.length = 0;

      const tldr = U.el('div', { class: 'tldr' });
      tldr.appendChild(U.el('h3', { text: 'TL;DR (report)' }));
      const ul = U.el('ul');
      for (const t of corpus.tldr) ul.appendChild(U.el('li', { text: t }));
      tldr.appendChild(ul);
      scroll.appendChild(tldr);

      const cols = U.el('div', { class: 'cols' });

      const left = U.el('div');
      left.appendChild(U.el('div', { class: 'pssec', text: 'quality-gate ledger — ' + relations.gate.length + ' candidates' }));
      for (const g of relations.gate) {
        const row = U.el('div', { class: 'gaterow' + (g.status === 'dropped' ? ' dropped' : '') });
        const cand = U.el('div', { class: 'cand' });
        cand.appendChild(U.el('span', { text: g.candidate + ' ' }));
        cand.appendChild(U.el('span', { class: 'badge ' + g.status, text: g.status }));
        const ids = U.el('span', { class: 'ids' });
        for (const i of g.ids) { ids.appendChild(U.idChip(byId[i], () => CALC.state.set({ sel: i }))); ids.appendChild(document.createTextNode(' ')); }
        cand.appendChild(ids);
        row.appendChild(cand);
        row.appendChild(U.el('div', { class: 'why', text: g.reason }));
        left.appendChild(row); rowEls.push({ el: row, ids: g.ids });
      }
      cols.appendChild(left);

      const right = U.el('div');
      right.appendChild(U.el('div', { class: 'pssec', text: 'open register' }));
      for (const r of relations.register) {
        const card = U.el('div', { class: 'card static' });
        card.appendChild(U.el('h4', { text: r.title }));
        card.appendChild(U.el('p', { text: r.body }));
        right.appendChild(card);
      }
      right.appendChild(U.el('div', { class: 'pssec', text: 'caveats — what the views may not claim' }));
      for (const c of relations.caveats) {
        const card = U.el('div', { class: 'card static' });
        card.style.borderLeftColor = 'var(--jd)';
        card.appendChild(U.el('h4', { text: c.title }));
        card.appendChild(U.el('p', { text: c.body }));
        right.appendChild(card);
      }
      cols.appendChild(right);
      scroll.appendChild(cols);
      applyFilters();
    }

    function applyFilters() {
      const vis = C.visibleIds(corpus, CALC.state.get());
      for (const r of rowEls) r.el.classList.toggle('dimmed', !r.ids.some((i) => vis.has(i)));
    }
    render();
    return { applyFilters, onSelect: () => {}, destroy: () => {} };
  }
  return { label: 'Quality gate', mount };
})();
