// app.js — bootstrap (the imperative shell's outer edge). Wires the two global failure backstops,
// parses the data boundary once (fail loud), builds the one console logger, mounts the persistent
// inspector, and dispatches state changes to the active view. Loaded last.
(function () {
  'use strict';
  const U = CALC.util, S = CALC.state;
  const log = CALC.log.consoleLogger('calc', 'debug');
  const VIEW_ORDER = ['graph', 'tiers', 'lineage', 'parallel', 'gate'];

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
    const corpus = CALC.parse.parseCorpus(window.CALC && CALC.corpus);
    const byId = new Map(corpus.nodes.map((n) => [n.id, n]));
    const relations = CALC.parse.parseRelations(window.CALC && CALC.relations, byId);
    CALC.core.buildIndex(corpus);
    log.info('data parsed', { nodes: corpus.nodes.length, edges: relations.edges.length });

    const ctx = { corpus, relations, log };

    // filter options (rigor from util's fixed vocabulary; tiers from the scheme)
    const fr = $('frigor');
    for (const r of U.RIGORS) fr.appendChild(U.el('option', { value: r, text: 'rigor: ' + r }));
    const ft = $('ftier');
    for (const t of corpus.tiers) ft.appendChild(U.el('option', { value: String(t.tier), text: 'T' + t.tier + ' · ' + t.name }));

    // tabs
    const tabs = $('tabs');
    VIEW_ORDER.forEach((id, i) => tabs.appendChild(U.el('button', { role: 'tab', id: 'tab-' + id, 'aria-selected': 'false',
      text: (i + 1) + ' · ' + CALC.views[id].label, onclick: () => S.set({ view: id }) })));
    tabs.addEventListener('keydown', (ev) => {
      if (ev.key !== 'ArrowRight' && ev.key !== 'ArrowLeft') return;
      const i = VIEW_ORDER.indexOf(S.get().view);
      const j = (i + (ev.key === 'ArrowRight' ? 1 : VIEW_ORDER.length - 1)) % VIEW_ORDER.length;
      S.set({ view: VIEW_ORDER[j] }); $('tab-' + VIEW_ORDER[j]).focus();
    });

    // persistent inspector
    CALC.inspector.mount($('inspector'), ctx);

    // view lifecycle
    let current = null;
    function mountView(id) {
      if (!VIEW_ORDER.includes(id)) id = 'graph';
      if (current && current.destroy) current.destroy();
      const vr = $('view-root'); vr.replaceChildren();
      current = CALC.views[id].mount(vr, ctx);
      VIEW_ORDER.forEach((v) => $('tab-' + v).setAttribute('aria-selected', v === id ? 'true' : 'false'));
      log.debug('view mounted', { view: id });
    }

    // toolbar -> state
    const q = $('q');
    let qTimer = null;
    q.addEventListener('input', () => { clearTimeout(qTimer); qTimer = setTimeout(() => S.set({ q: q.value.trim() }), 200); });
    fr.addEventListener('change', () => S.set({ rigor: fr.value }));
    ft.addEventListener('change', () => S.set({ tier: ft.value }));
    $('reset').addEventListener('click', () => S.set({ q: '', rigor: '', tier: '', sel: null }));

    // state -> toolbar + view dispatch
    function syncControls(s) { if (q.value !== s.q) q.value = s.q; if (fr.value !== s.rigor) fr.value = s.rigor; if (ft.value !== s.tier) ft.value = s.tier; }
    S.on((s, changed) => {
      if (changed.includes('view')) mountView(s.view);
      if (['q', 'rigor', 'tier'].some((k) => changed.includes(k))) { syncControls(s); if (current && current.applyFilters) current.applyFilters(); }
      if (changed.includes('sel') && current && current.onSelect) current.onSelect(s.sel);
    });

    // keyboard
    document.addEventListener('keydown', (ev) => {
      if (ev.target instanceof Element && ev.target.matches('input,select,textarea')) { if (ev.key === 'Escape') ev.target.blur(); return; }
      if (ev.key === '/') { ev.preventDefault(); q.focus(); q.select(); }
      else if (ev.key === 'Escape') { if (S.get().sel) S.set({ sel: null }); }
      else if (ev.key === 'r') { const i = U.RIGORS.indexOf(S.get().rigor); S.set({ rigor: i === U.RIGORS.length - 1 ? '' : U.RIGORS[i + 1] }); }
      else if (ev.key === 't') { const cur = S.get().tier; S.set({ tier: cur === '' ? '0' : (+cur === 8 ? '' : String(+cur + 1)) }); }
      else if (/^[1-5]$/.test(ev.key)) S.set({ view: VIEW_ORDER[+ev.key - 1] });
    });

    // initial render from hash
    const s = S.get(); syncControls(s);
    mountView(s.view);
    log.info('ready', { view: s.view });
  }

  try { boot(); } catch (err) { fail(err); }
})();
