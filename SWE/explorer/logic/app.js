// app.js — bootstrap: view registry wiring, toolbar, keyboard, hash routing.
(function () {
  'use strict';
  const U = SWE.util, S = SWE.state;
  const VIEW_ORDER = ['graph', 'facets', 'timeline', 'overlap', 'anchors'];
  let current = null, currentId = null;

  // meta line
  const nodes = SWE.corpus.nodes, E = SWE.relations.edges;
  const ver = nodes.filter(n => n.verification === 'verified').length;
  const multi = nodes.filter(n => n.corpora.length > 1).length;
  const unres = nodes.filter(n => n.unresolved && n.unresolved.length).length;
  const edi = E.filter(e => e.src === 'editorial').length;
  document.getElementById('meta').innerHTML =
    '<b>' + nodes.length + '</b> resources · <b>6</b> corpora · <b>' + E.length + '</b> typed edges (' +
    edi + ' editorial) · <b>' + ver + '</b> verified / <b>' + (nodes.length - ver) + '</b> unverified · <b>' +
    multi + '</b> cross-corpus works · <b>' + unres + '</b> nodes with UNRESOLVED fields';

  // corpus filter options
  const fc = document.getElementById('fcorpus');
  for (const c in SWE.corpus.corpora)
    fc.appendChild(U.el('option', { value: c, text: 'corpus: ' + U.CORPUS_SHORT[c] }));

  // tabs
  const tabs = document.getElementById('tabs');
  VIEW_ORDER.forEach((id, i) => {
    tabs.appendChild(U.el('button', { role: 'tab', id: 'tab-' + id,
      'aria-selected': 'false', text: (i + 1) + ' · ' + SWE.views[id].label,
      onclick: () => S.set({ view: id }) }));
  });
  tabs.addEventListener('keydown', ev => {
    if (ev.key !== 'ArrowRight' && ev.key !== 'ArrowLeft') return;
    const i = VIEW_ORDER.indexOf(S.get().view);
    const j = (i + (ev.key === 'ArrowRight' ? 1 : VIEW_ORDER.length - 1)) % VIEW_ORDER.length;
    S.set({ view: VIEW_ORDER[j] });
    document.getElementById('tab-' + VIEW_ORDER[j]).focus();
  });

  function mountView(id) {
    const root = document.getElementById('view-root');
    root.innerHTML = '';
    currentId = id;
    current = SWE.views[id].mount(root);
    VIEW_ORDER.forEach(v => document.getElementById('tab-' + v)
      .setAttribute('aria-selected', v === id ? 'true' : 'false'));
  }

  // toolbar inputs
  const q = document.getElementById('q'), fv = document.getElementById('fver');
  let qTimer = null;
  q.addEventListener('input', () => {
    clearTimeout(qTimer);
    qTimer = setTimeout(() => S.set({ q: q.value.trim() }), 220);
  });
  fv.addEventListener('change', () => S.set({ ver: fv.value }));
  fc.addEventListener('change', () => S.set({ corpus: fc.value }));

  // state reactions
  S.on((st, changed) => {
    if (changed.includes('view')) mountView(st.view);
    else if (['q', 'ver', 'corpus'].some(k => changed.includes(k)) && current && current.applyFilters)
      current.applyFilters();
    if (changed.includes('sel') && !st.sel && SWE.detail.isOpen()) SWE.detail.hide();
  });

  // keyboard
  document.addEventListener('keydown', ev => {
    if (ev.target.matches('input,select,textarea')) {
      if (ev.key === 'Escape') ev.target.blur();
      return;
    }
    if (ev.key === '/') { ev.preventDefault(); q.focus(); }
    else if (ev.key === 'Escape' && SWE.detail.isOpen()) SWE.detail.hide();
    else if (ev.key === 'v') {
      fv.value = fv.value === '' ? 'verified' : fv.value === 'verified' ? 'unverified' : '';
      S.set({ ver: fv.value });
    } else if (/^[1-5]$/.test(ev.key)) S.set({ view: VIEW_ORDER[+ev.key - 1] });
  });

  // initial render from hash
  const st = S.get();
  if (!VIEW_ORDER.includes(st.view)) st.view = 'graph';
  q.value = st.q; fv.value = st.ver; fc.value = st.corpus;
  mountView(st.view);
  if (st.sel) SWE.detail.show(st.sel);
})();
