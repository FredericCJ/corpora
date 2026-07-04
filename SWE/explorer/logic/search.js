// search.js — substring index over the fact layer + global filter predicate.
window.SWE = window.SWE || {};
SWE.search = (function () {
  'use strict';
  let idx = null;
  function build() {
    idx = SWE.corpus.nodes.map(n => ({
      id: n.id,
      text: (n.title + ' ' + n.authors + ' ' + n.id + ' ' + (n.ident || '') + ' ' +
             (n.themes || []).join(' ')).toLowerCase()
    }));
  }
  function matches(q) {
    if (!idx) build();
    const terms = q.toLowerCase().split(/\s+/).filter(Boolean);
    const out = new Set();
    for (const r of idx) if (terms.every(t => r.text.includes(t))) out.add(r.id);
    return out;
  }
  // visibleIds: nodes passing the GLOBAL filters (search text, verification, corpus)
  function visibleIds() {
    const st = SWE.state.get();
    const qset = st.q ? matches(st.q) : null;
    const out = new Set();
    for (const n of SWE.corpus.nodes) {
      if (qset && !qset.has(n.id)) continue;
      if (st.ver && n.verification !== st.ver) continue;
      if (st.corpus && !n.corpora.includes(st.corpus)) continue;
      out.add(n.id);
    }
    return out;
  }
  return { matches, visibleIds };
})();
