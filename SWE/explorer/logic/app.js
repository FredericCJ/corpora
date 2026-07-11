// app.js — bootstrap (the imperative shell's outer edge). Wires the two global failure backstops,
// parses the data boundary once (fail loud), builds the one console logger, mounts the persistent
// inspector, and dispatches state changes to the active view. Loaded last.
(function () {
  'use strict';
  const U = SWE.util, S = SWE.state;
  const log = SWE.log.consoleLogger('swe', 'debug');
  const WORK_VIEWS = ['graph', 'facets', 'timeline', 'overlap', 'anchors'];
  const EL_VIEWS = ['el-taxonomy', 'el-bridge', 'el-graph', 'el-coverage'];
  const VIEW_ORDER = WORK_VIEWS.concat(EL_VIEWS);

  window.addEventListener('error', (ev) => log.error('uncaught error escaped every boundary', { message: ev.message, src: ev.filename, line: ev.lineno }));
  window.addEventListener('unhandledrejection', (ev) => log.error('unhandled promise rejection', { reason: String(ev.reason) }));

  const $ = (id) => document.getElementById(id);

  function fail(err) {
    log.error('bootstrap failed', { error: String(err && err.message || err) });
    const vr = $('view-root'), insp = $('inspector');
    if (vr) vr.replaceChildren(U.el('div', { class: 'empty', style: 'padding:2rem', text: 'The data failed to load or validate. See the console for the parse error.' }));
    if (insp) insp.replaceChildren(U.el('h2', { text: 'Load error' }), U.el('p', { class: 'cite', text: String(err && err.message || err) }),
      U.el('p', { class: 'muted', text: 'Re-run `python build/build.py` to regenerate data/, then reload.' }));
  }

  function boot() {
    const corpus = SWE.parse.parseCorpus(window.SWE && window.SWE.corpus);
    const ids = new Set(corpus.nodes.map((n) => n.id));
    const relations = SWE.parse.parseRelations(window.SWE && window.SWE.relations, ids);
    SWE.core.buildIndex(corpus);
    const elements = SWE.parse.parseElements(window.SWE && window.SWE.elements);
    const elIndex = SWE.coreEl.buildIndex(elements);
    log.info('data parsed', { nodes: corpus.nodes.length, edges: relations.edges.length,
      elements: elements.nodes.length, elementEdges: elements.edges.length });

    const ctx = { corpus, relations, elements, elIndex, log };

    // corpus filter options
    const fc = $('fcorpus');
    for (const c of U.CORPUS_ORDER) fc.appendChild(U.el('option', { value: c, text: 'corpus: ' + U.CORPUS_SHORT[c] }));

    // tabs — five work models, a divider, then the four element views
    const tabs = $('tabs');
    VIEW_ORDER.forEach((id, i) => {
      if (id === EL_VIEWS[0]) tabs.appendChild(U.el('span', { class: 'tab-sep', 'aria-hidden': 'true', text: 'elements' }));
      tabs.appendChild(U.el('button', { role: 'tab', id: 'tab-' + id, 'aria-selected': 'false',
        text: (i + 1) + ' · ' + SWE.views[id].label, onclick: () => S.set({ view: id }) }));
    });
    tabs.addEventListener('keydown', (ev) => {
      if (ev.key !== 'ArrowRight' && ev.key !== 'ArrowLeft') return;
      const i = VIEW_ORDER.indexOf(S.get().view);
      const j = (i + (ev.key === 'ArrowRight' ? 1 : VIEW_ORDER.length - 1)) % VIEW_ORDER.length;
      S.set({ view: VIEW_ORDER[j] }); $('tab-' + VIEW_ORDER[j]).focus();
    });

    // persistent inspector
    SWE.inspector.mount($('inspector'), ctx);

    // view lifecycle
    let current = null;
    function mountView(id) {
      if (!VIEW_ORDER.includes(id)) id = 'graph';
      if (current && current.destroy) current.destroy();
      const vr = $('view-root'); vr.replaceChildren();
      current = SWE.views[id].mount(vr, ctx);
      VIEW_ORDER.forEach((v) => $('tab-' + v).setAttribute('aria-selected', v === id ? 'true' : 'false'));
      log.debug('view mounted', { view: id });
    }

    // toolbar -> state
    const q = $('q'), fv = $('fver');
    let qTimer = null;
    q.addEventListener('input', () => { clearTimeout(qTimer); qTimer = setTimeout(() => S.set({ q: q.value.trim() }), 200); });
    fv.addEventListener('change', () => S.set({ ver: fv.value }));
    fc.addEventListener('change', () => S.set({ corpus: fc.value }));
    $('reset').addEventListener('click', () => S.set({ q: '', ver: '', corpus: '', sel: null }));

    // state -> toolbar + view dispatch
    function syncControls(s) { if (q.value !== s.q) q.value = s.q; if (fv.value !== s.ver) fv.value = s.ver; if (fc.value !== s.corpus) fc.value = s.corpus; }
    S.on((s, changed) => {
      if (changed.includes('view')) mountView(s.view);
      if (['q', 'ver', 'corpus'].some((k) => changed.includes(k))) { syncControls(s); if (current && current.applyFilters) current.applyFilters(); }
      if (changed.includes('sel') && current && current.onSelect) current.onSelect(s.sel);
    });

    // keyboard
    document.addEventListener('keydown', (ev) => {
      if (ev.target.matches('input,select,textarea')) { if (ev.key === 'Escape') ev.target.blur(); return; }
      if (ev.key === '/') { ev.preventDefault(); q.focus(); q.select(); }
      else if (ev.key === 'Escape') { if (S.get().sel) S.set({ sel: null }); }
      else if (ev.key === 'v') { const nx = fv.value === '' ? 'verified' : fv.value === 'verified' ? 'unverified' : ''; S.set({ ver: nx }); }
      else if (/^[1-9]$/.test(ev.key) && +ev.key <= VIEW_ORDER.length) S.set({ view: VIEW_ORDER[+ev.key - 1] });
    });

    // initial render from hash
    const s = S.get(); syncControls(s);
    mountView(s.view);
    log.info('ready', { view: s.view });
  }

  try { boot(); } catch (err) { fail(err); }
})();
