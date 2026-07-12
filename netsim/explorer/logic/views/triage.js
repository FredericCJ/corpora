// views/triage.js — Model 5: the verification triage (shell). The reports' citation discipline
// made first-class: the three-grade split with the legend verbatim, the quarantine sections as
// cards with their "to confirm" notes, and the coverage self-assessments quoted whole.
window.NET = window.NET || {}; NET.views = NET.views || {};
NET.views.triage = (function () {
  'use strict';
  const U = NET.util, C = NET.core;

  function mount(root, ctx) {
    const corpus = ctx.corpus, relations = ctx.relations;

    const vp = U.el('div', { class: 'vp' });
    vp.appendChild(U.el('div', { class: 'vp-head' },
      U.el('h2', { text: 'Triage — what may be cited, what must be re-verified, what is quarantined' }),
      U.el('p', { class: 'note', text: 'The reports’ own discipline, not ours: every entry carries a verification grade, and the unverified sit in explicit quarantine sections with per-item “to confirm” notes. The coverage summaries — including where recall thins and what has moved on since the anchor — are quoted whole.' })));
    const body = U.el('div', { class: 'vp-body' });
    const scroll = U.el('div', { class: 'triage' });
    body.appendChild(scroll); vp.appendChild(body); root.appendChild(vp);

    const cardEls = {};

    function render() {
      scroll.replaceChildren();
      const t = C.triage(corpus.nodes);
      const vstats = U.el('div', { class: 'vstats' });
      for (const [k, cls, col] of [['verified-web', 'web', 'var(--v-web)'],
                                   ['verified-train', 'train', 'var(--v-train)'],
                                   ['unverified', 'unv', 'var(--v-unv)']]) {
        const vs = U.el('div', { class: 'vstat' });
        vs.style.borderTopColor = col;
        vs.appendChild(U.el('div', { class: 'n', text: String(t.by[k].length) }));
        vs.appendChild(U.el('div', { class: 'k', text: U.VER_SHORT[k] }));
        vs.appendChild(U.el('div', { class: 'd', text: relations.verificationLegend[k] }));
        vstats.appendChild(vs);
      }
      scroll.appendChild(vstats);

      const cols = U.el('div', { class: 'cols' });
      const left = U.el('div');
      const curSel = NET.state.get().sel;
      for (const [ck, label] of [['gen', 'GEN §25 — unverified / to confirm'], ['mat', 'MAT §9 — unverified / to confirm']]) {
        left.appendChild(U.el('div', { class: 'pssec', text: label + ' · ' + t.quarantine[ck].length }));
        for (const n of t.quarantine[ck]) {
          const card = U.el('div', { class: 'card', tabindex: '0', role: 'button', 'data-id': n.id,
            onclick: () => NET.state.set({ sel: n.id }),
            onkeydown: (ev) => { if (ev.key === 'Enter' || ev.key === ' ') { ev.preventDefault(); NET.state.set({ sel: n.id }); } } });
          card.style.borderLeftColor = 'var(--v-unv)';
          if (n.id === curSel) card.style.outline = '2px solid var(--ink)';
          const h = U.el('h4', { text: n.item[ck] + ' — ' + U.shortTitle(n.title, 60) });
          card.appendChild(h);
          card.appendChild(U.el('p', { text: U.shortTitle(n.note || n.cite, 160) }));
          const b = U.el('p'); U.badges(n).slice(0, 2).forEach((x) => b.appendChild(x)); card.appendChild(b);
          left.appendChild(card); cardEls[n.id] = card;
        }
      }
      cols.appendChild(left);

      const right = U.el('div');
      right.appendChild(U.el('div', { class: 'pssec', text: 'GEN coverage summary (verbatim)' }));
      relations.coverage.gen.forEach((p, i) => right.appendChild(
        U.el('div', { class: 'covblock' + (i === 1 ? ' gap' : ''), text: p })));
      right.appendChild(U.el('div', { class: 'pssec', text: 'MAT coverage summary (verbatim)' }));
      relations.coverage.mat.forEach((p) => right.appendChild(U.el('div', { class: 'covblock', text: p })));
      cols.appendChild(right);
      scroll.appendChild(cols);
      applyFilters();
    }

    function applyFilters() {
      const vis = C.visibleIds(corpus, NET.state.get());
      for (const id in cardEls) cardEls[id].classList.toggle('dimmed', !vis.has(id));
    }
    function onSelect(sel) {
      for (const id in cardEls) cardEls[id].style.outline = id === sel ? '2px solid var(--ink)' : '';
    }
    render();
    return { applyFilters, onSelect, destroy: () => {} };
  }
  return { label: 'Triage', mount };
})();
