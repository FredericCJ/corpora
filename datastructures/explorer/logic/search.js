// search.js — pure derivation of the visible node-id set from (corpus, state). No DOM.
// Search + family + verification narrow which nodes are "on"; the graph dims the rest (it
// never relays out — single viewport). The relation-kind filter acts on edges and is applied
// by the renderer directly from state.kind.
window.DS = window.DS || {};
DS.search = (function () {
  'use strict';
  /** @type {Record<string,string>} */
  let hay = null;

  /** @param {import('./parse.js').Corpus} corpus */
  function index(corpus) {
    hay = {};
    for (const n of corpus.nodes) {
      hay[n.id] = (n.name + ' ' + n.id + ' ' + n.origin + ' ' + (n.verdict || '')).toLowerCase();
    }
  }

  /**
   * @param {import('./parse.js').Corpus} corpus
   * @param {import('./state.js').State} state
   * @returns {Set<string>} ids that pass search + family + verification filters
   */
  function visibleIds(corpus, state) {
    if (!hay) index(corpus);
    const q = (state.q || '').trim().toLowerCase();
    const out = new Set();
    for (const n of corpus.nodes) {
      if (state.family && n.family !== state.family) continue;
      if (state.ver && n.verification !== state.ver) continue;
      if (q && !hay[n.id].includes(q)) continue;
      out.add(n.id);
    }
    return out;
  }

  return { index, visibleIds };
})();
