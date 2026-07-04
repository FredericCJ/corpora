// views/anchors.js — Model 5: per-corpus anchors & spine (shell). One column per corpus; each
// scrolls internally. Anchors are report-flagged fact (core.anchorsFor), not our ranking.
window.SWE = window.SWE || {}; SWE.views = SWE.views || {};
SWE.views.anchors = (function () {
  'use strict';
  const U = SWE.util, C = SWE.core;
  const NO_ANCHOR = {
    'emb-arch': 'Asserts no anchor/tier facet — it recommends its “verified list as the corpus spine”; use Facets with corpus = arch.',
    'emb-c': 'Asserts no anchor facet — its Recommendations name per-theme anchors in prose (BARR-C; MISRA C + Hatton + Holzmann + Frama-C; Doxygen + Knuth; Grenning + Unity; Preschern + Hanson + Samek).',
    'emb-cpp': 'Asserts no anchor facet — its Details single out ISO/IEC TR 18015 as “the single most important cost-model foundation” and the EC++ → MISRA C++:2008 → AUTOSAR C++14 → MISRA C++:2023 arc.',
  };

  function mount(root, ctx) {
    const corpus = ctx.corpus;
    const vp = U.el('div', { class: 'vp' });
    vp.appendChild(U.el('div', { class: 'vp-head' },
      U.el('h2', { text: 'Anchors & spine — where each corpus tells you to start' }),
      U.el('p', { class: 'note', text: 'The union of the reports’ own emphasis marks: swa ★ target/canonical anchors, Simulink TARGET designations, emb-ops KEY / ABSOLUTELY KEY flags. Carried fact, not our ranking. Corpora asserting no anchor facet say so explicitly.' })));
    const body = U.el('div', { class: 'vp-body' });
    const cols = U.el('div', { class: 'anchor-cols' });
    body.appendChild(cols); vp.appendChild(body); root.appendChild(vp);

    function render() {
      const vis = C.visibleIds(corpus, SWE.state.get());
      const base = corpus.nodes.filter((n) => vis.has(n.id));
      cols.replaceChildren();
      const curSel = SWE.state.get().sel;
      for (const c of U.CORPUS_ORDER) {
        const anchors = C.anchorsFor(base, c);
        const col = U.el('div', { class: 'anchor-col' });
        const h = U.el('div', { class: 'h', text: U.CORPUS_SHORT[c] + (anchors.length ? ' · ' + anchors.length : '') });
        h.style.borderBottomColor = U.corpusStroke(c); h.style.color = U.corpusStroke(c);
        col.appendChild(h);
        const scroll = U.el('div', { class: 'anchor-scroll' });
        if (!anchors.length) {
          scroll.appendChild(U.el('p', { class: 'empty', text: NO_ANCHOR[c] || 'no anchors match the current filters' }));
        } else {
          anchors.forEach((n) => {
            const card = U.el('div', { class: 'card', tabindex: '0', role: 'button', 'data-id': n.id,
              onclick: () => SWE.state.set({ sel: n.id }), onkeydown: (ev) => { if (ev.key === 'Enter') SWE.state.set({ sel: n.id }); } });
            card.style.borderLeftColor = U.corpusStroke(c);
            if (n.id === curSel) card.style.outline = '2px solid var(--ink)';
            card.appendChild(U.el('h4', { text: U.shortTitle(n.title, 52) }));
            card.appendChild(U.el('p', { text: n.authors + ' · ' + n.year }));
            const b = U.el('p'); U.badges(n).slice(0, 2).forEach((x) => b.appendChild(x)); card.appendChild(b);
            scroll.appendChild(card);
          });
        }
        col.appendChild(scroll); cols.appendChild(col);
      }
    }
    render();
    return { applyFilters: render, onSelect: () => render(), destroy: () => {} };
  }
  return { label: 'Anchors', mount };
})();
