// app.js — bootstrap (the imperative shell's outer edge). Wires the two global failure
// backstops, parses the data boundary once (fail loud), builds the one console logger, mounts
// the graph + inspector, and owns the toolbar + keyboard. Loaded last.
(function () {
  'use strict';
  const U = DS.util;
  const log = DS.log.consoleLogger('app', 'debug');

  // ── the last line: global handlers (js_error_tracing_contract_manifest §10) ──
  window.addEventListener('error', (ev) =>
    log.error('uncaught error escaped every boundary', { message: ev.message, src: ev.filename, line: ev.lineno }));
  window.addEventListener('unhandledrejection', (ev) =>
    log.error('unhandled promise rejection', { reason: String(ev.reason) }));

  const $ = (id) => document.getElementById(id);

  function fail(err) {
    log.error('bootstrap failed', { error: String(err && err.message || err) });
    const board = $('board'), insp = $('inspector');
    if (board) board.replaceChildren(U.el('div', { class: 'empty', style: 'padding:2rem',
      text: 'The data failed to load or validate. See the console for the parse error.' }));
    if (insp) insp.replaceChildren(
      U.el('h2', { text: 'Load error' }),
      U.el('p', { class: 'cite', text: String(err && err.message || err) }),
      U.el('p', { class: 'muted', text: 'Re-run `python build/build.py` to regenerate data/, then reload.' }));
  }

  function boot() {
    // parse the inward boundary — a stale/old-shape data file must fail here, not flow inward
    const corpus = DS.parse.parseCorpus(window.DS && window.DS.corpus);
    const ids = new Set(corpus.nodes.map((n) => n.id));
    const relations = DS.parse.parseRelations(window.DS && window.DS.relations, ids);
    DS.search.index(corpus);
    log.info('data parsed', { nodes: corpus.nodes.length, edges: relations.edges.length });

    // masthead meta
    const roots = corpus.nodes.filter((n) => n.tier !== 'modern').length;
    const flagged = corpus.nodes.filter((n) => n.verification === 'flagged').length;
    $('meta').replaceChildren(document.createTextNode(
      `${corpus.nodes.length} structures · ${relations.edges.length} typed relations · ` +
      `${roots} roots · ${flagged} flagged · ${relations.edges.filter((e) => e.cycle).length} cycle edges`));

    // toolbar: populate selects
    const famSel = $('f-family');
    corpus.familyOrder.forEach((f) => famSel.appendChild(U.el('option', { value: f, text: corpus.families[f] })));
    const kindSel = $('f-kind');
    relations.kinds.forEach((k) => kindSel.appendChild(U.el('option', { value: k, text: k })));

    // compact strip legend (data-driven from the relation vocabulary)
    const legend = $('legend');
    relations.kinds.forEach((k) => {
      const sw = U.el('span', { class: 'swatch' });
      sw.style.borderTopColor = `var(--k-${k})`;
      if (k === 'hybridizes' || k === 'influences') sw.style.borderTopStyle = 'dashed';
      legend.appendChild(U.el('span', { class: 'lg' }, sw, k));
    });
    const star = U.el('span', { class: 'tiermark' }); star.style.background = 'var(--accent)';
    legend.appendChild(U.el('span', { class: 'lg' }, star, 'root ★'));
    legend.appendChild(U.el('span', { class: 'lg', text: '⚠ flagged' }));

    // toolbar -> state (unidirectional; controls are inputs to state, never read back as truth)
    const q = $('q'), ver = $('f-ver');
    q.addEventListener('input', () => DS.state.set({ q: q.value }));
    famSel.addEventListener('change', () => DS.state.set({ family: famSel.value }));
    ver.addEventListener('change', () => DS.state.set({ ver: ver.value }));
    kindSel.addEventListener('change', () => DS.state.set({ kind: kindSel.value }));
    $('reset').addEventListener('click', () =>
      DS.state.set({ q: '', family: '', ver: '', kind: '', sel: null }));

    // state -> toolbar (reflect hash-restored / programmatic changes)
    function syncControls(s) {
      if (q.value !== s.q) q.value = s.q;
      if (famSel.value !== s.family) famSel.value = s.family;
      if (ver.value !== s.ver) ver.value = s.ver;
      if (kindSel.value !== s.kind) kindSel.value = s.kind;
    }
    DS.state.on(syncControls);
    syncControls(DS.state.get());

    // keyboard: / focus search, Esc clears selection then search
    document.addEventListener('keydown', (ev) => {
      if (ev.key === '/' && document.activeElement !== q) { ev.preventDefault(); q.focus(); q.select(); }
      else if (ev.key === 'Escape') {
        if (DS.state.get().sel) DS.state.set({ sel: null });
        else if (document.activeElement === q) q.blur();
      }
    });

    DS.detail.mount($('inspector'), { corpus, relations, log });
    DS.render.mount($('board'), { corpus, relations, log });
    log.info('ready');
  }

  try { boot(); } catch (err) { fail(err); }
})();
