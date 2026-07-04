// views/anchors.js — Model 5: per-corpus anchors & spine (report-flagged entry points).
window.SWE = window.SWE || {}; SWE.views = SWE.views || {};
SWE.views.anchors = (function () {
  'use strict';
  const U = SWE.util;
  const ORDER = ['swa-science', 'emb-arch', 'emb-c', 'emb-cpp', 'emb-ops', 'simulink'];
  const NO_ANCHOR_FACET = {
    'emb-arch': 'This report asserts no anchor/tier facet — it recommends its “verified list as the corpus spine”; use the Facets view with corpus=emb-arch instead.',
    'emb-c': 'This report asserts no anchor facet — its Recommendations name per-theme anchors in prose (BARR-C, MISRA C + Hatton + Holzmann + Frama-C, Doxygen + Knuth, Grenning + Unity, Bacchelli & Bird + Fagan, Preschern + Hanson + Schreiner + Douglass + Samek).',
    'emb-cpp': 'This report asserts no anchor facet — its Details single out ISO/IEC TR 18015 as “the single most important cost-model foundation” and the EC++ → MISRA C++:2008 → AUTOSAR C++14 → MISRA C++:2023 arc.'
  };
  function mount(root) {
    root.appendChild(U.el('h2', { text: 'Anchors & spine — where each corpus tells you to start' }));
    root.appendChild(U.el('p', { class: 'viewnote', text:
      'The union of the reports’ own emphasis marks: swa-science ★ target/canonical anchors, Simulink TARGET ' +
      'designations, and emb-ops KEY / ABSOLUTELY KEY flags. This is carried fact, not our ranking. Corpora whose ' +
      'reports assert no anchor facet say so explicitly below rather than being silently absent.' }));
    const host = U.el('div'); root.appendChild(host);
    function render() {
      const vis = SWE.search.visibleIds();
      host.innerHTML = '';
      for (const c of ORDER) {
        const anchors = SWE.corpus.nodes.filter(n =>
          vis.has(n.id) && n.corpora.includes(c) && (n.role || []).includes('anchor') &&
          n.per[c] && !n.per[c].lead);
        host.appendChild(U.el('h3', { text: SWE.corpus.corpora[c] + (anchors.length ? ' · ' + anchors.length + ' anchors' : '') }));
        if (!anchors.length && NO_ANCHOR_FACET[c]) {
          host.appendChild(U.el('p', { class: 'viewnote', text: NO_ANCHOR_FACET[c] }));
          continue;
        }
        const grid = U.el('div', { class: 'cards' });
        anchors.sort((a, b) => (U.yearNum(a) || 9999) - (U.yearNum(b) || 9999)).forEach(n => {
          const card = U.el('div', { class: 'card', tabindex: '0', role: 'button',
            onclick: () => SWE.detail.show(n.id),
            onkeydown: ev => { if (ev.key === 'Enter') SWE.detail.show(n.id); } });
          card.style.borderLeftColor = U.CORPUS_COLOR[c];
          card.appendChild(U.el('h4', { text: n.title }));
          card.appendChild(U.el('p', { text: n.authors + ' · ' + n.year }));
          const b = U.el('p'); U.badges(n).forEach(x => b.appendChild(x)); card.appendChild(b);
          grid.appendChild(card);
        });
        host.appendChild(grid);
      }
    }
    render();
    return { applyFilters: render };
  }
  return { label: 'Anchors', mount };
})();
