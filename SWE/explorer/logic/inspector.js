// inspector.js — the persistent inspector dock (shell). Model-aware overview when nothing is
// selected; full citation + typed relations when a node is. Subscribes to state.sel and state.view.
window.SWE = window.SWE || {};
SWE.inspector = (function () {
  'use strict';
  const U = SWE.util;
  const PROV = { 'report:swa': 'report · swa', 'report:sim': 'report · sim', 'report:proc': 'report · proc', 'derived': 'derived', 'editorial': 'EDITORIAL' };

  /** @param {HTMLElement} host @param {{corpus:any,relations:any,log?:any}} ctx */
  function mount(host, ctx) {
    const corpus = ctx.corpus, relations = ctx.relations, log = ctx.log || SWE.log.NOOP;
    const byId = {}; corpus.nodes.forEach((n) => { byId[n.id] = n; });
    const outE = {}, inE = {};
    for (const e of relations.edges) { (outE[e.s] = outE[e.s] || []).push(e); (inE[e.t] = inE[e.t] || []).push(e); }

    function provBadge(src) { return U.el('span', { class: 'badge ' + (src === 'editorial' ? 'edi' : 'rep'), text: PROV[src] || src }); }

    function edgeRow(e, dir) {
      const other = byId[dir === 'out' ? e.t : e.s];
      const row = U.el('div', { class: 'edge' });
      row.appendChild(U.el('span', { class: 'kt', text: dir === 'out' ? e.kind : 'is ' + e.kind + ' of' }));
      row.appendChild(document.createTextNode(' '));
      row.appendChild(U.el('span', { class: 'lnk', text: other ? other.title : e.t, tabindex: '0', role: 'link',
        onclick: () => SWE.state.set({ sel: other.id }),
        onkeydown: (ev) => { if (ev.key === 'Enter' || ev.key === ' ') { ev.preventDefault(); SWE.state.set({ sel: other.id }); } } }));
      row.appendChild(document.createTextNode(' '));
      row.appendChild(provBadge(e.src));
      if (e.cycle) row.appendChild(U.el('span', { class: 'badge cycle', text: 'cycle ' + e.cycle }));
      if (e.note) row.appendChild(U.el('span', { class: 'ov', text: e.note }));
      return row;
    }

    function renderNode(id) {
      const n = byId[id]; if (!n) { renderOverview(); return; }
      host.replaceChildren();
      host.appendChild(U.el('button', { class: 'close', text: 'Esc ✕', 'aria-label': 'Close detail', onclick: () => SWE.state.set({ sel: null }) }));
      host.appendChild(U.el('h2', { text: n.title }));
      const cite = U.el('p', { class: 'cite' });
      cite.appendChild(U.el('span', { text: n.authors + ' · ' }));
      cite.appendChild(U.el('b', { text: n.year }));
      if (n.ident) cite.appendChild(U.el('span', { text: ' · ' + n.ident }));
      host.appendChild(cite);

      const bl = U.el('div'); U.badges(n).forEach((b) => bl.appendChild(b));
      (n.role || []).filter((r) => r === 'core' || r === 'advanced').forEach((r) => bl.appendChild(U.el('span', { class: 'badge surv', text: r })));
      if (n.lane) bl.appendChild(U.el('span', { class: 'badge surv', text: 'lane: ' + n.lane }));
      if (n.access) bl.appendChild(U.el('span', { class: 'badge ' + (n.access === 'open' ? 'ver' : 'surv'), text: 'oa: ' + n.access }));
      host.appendChild(bl);
      if (n.note) host.appendChild(U.el('p', { class: 'muted', text: n.note }));

      host.appendChild(U.el('div', { class: 'sec', text: 'corpora (memberships)' }));
      const cw = U.el('div'); U.corpusChips(n).forEach((c) => cw.appendChild(c)); host.appendChild(cw);

      host.appendChild(U.el('div', { class: 'sec', text: 'reconciled tags (phase 2)' }));
      const dl = U.el('dl', { class: 'dl' });
      const add = (k, v) => { if (v && v.length) { dl.appendChild(U.el('dt', { text: k })); dl.appendChild(U.el('dd', { text: Array.isArray(v) ? v.join(', ') : v })); } };
      add('type', n.type); add('branches', n.branches); add('themes', n.themes); add('language', n.lang); add('scope', n.scope);
      host.appendChild(dl);

      host.appendChild(U.el('div', { class: 'sec', text: 'raw tags as each report stated them' }));
      const dl2 = U.el('dl', { class: 'dl' });
      for (const c in n.per) { dl2.appendChild(U.el('dt', { text: U.CORPUS_SHORT[c] })); dl2.appendChild(U.el('dd', { text: JSON.stringify(n.per[c]) })); }
      host.appendChild(dl2);

      const outs = outE[id] || [], ins = inE[id] || [];
      host.appendChild(U.el('div', { class: 'sec', text: 'relates to (' + outs.length + ')' }));
      outs.length ? outs.forEach((e) => host.appendChild(edgeRow(e, 'out'))) : host.appendChild(U.el('p', { class: 'empty', text: 'no outgoing relations' }));
      host.appendChild(U.el('div', { class: 'sec', text: 'related from (' + ins.length + ')' }));
      ins.length ? ins.forEach((e) => host.appendChild(edgeRow(e, 'in'))) : host.appendChild(U.el('p', { class: 'empty', text: 'no incoming relations' }));
      log.debug('inspect', { id });
    }

    function legendBlock() {
      const wrap = U.el('div');
      wrap.appendChild(U.el('div', { class: 'sec', text: 'corpora' }));
      const cf = U.el('div');
      U.CORPUS_ORDER.forEach((c) => {
        const chip = U.el('span', { class: 'chip-fam', text: corpus.corpora[c] });
        chip.style.color = U.corpusStroke(c); chip.style.borderColor = U.corpusStroke(c); chip.style.background = U.corpusFill(c);
        cf.appendChild(chip);
      });
      wrap.appendChild(cf);

      wrap.appendChild(U.el('div', { class: 'sec', text: 'edge kinds (' + relations.kinds.length + ')' }));
      const lk = U.el('div', { class: 'legend-full' });
      for (const k of relations.kinds) {
        const sw = U.el('span', { class: 'swatch' });
        sw.style.borderTopColor = U.kindColor(k);
        if (U.KIND_DASH[k]) sw.style.borderTopStyle = 'dashed';
        lk.appendChild(U.el('div', { class: 'row' }, sw, U.el('b', { text: k })));
      }
      wrap.appendChild(lk);

      wrap.appendChild(U.el('div', { class: 'sec', text: 'provenance & honesty' }));
      const pr = U.el('div', { class: 'legend-full' });
      const row = (badge, txt) => U.el('div', { class: 'row' }, badge, U.el('span', { class: 'muted', text: txt }));
      pr.appendChild(row(U.el('span', { class: 'badge rep', text: 'report' }), 'stated in a report’s typed edge list'));
      pr.appendChild(row(U.el('span', { class: 'badge rep', text: 'derived' }), 'from a quoted report sentence'));
      pr.appendChild(row(U.el('span', { class: 'badge edi', text: 'EDITORIAL' }), 'reasoned judgment (dotted edges)'));
      pr.appendChild(row(U.el('span', { class: 'badge ver', text: 'verified' }), 'confirmed by its report'));
      pr.appendChild(row(U.el('span', { class: 'badge unv', text: 'unverified' }), 'carried as an unverified lead'));
      pr.appendChild(row(U.el('span', { class: 'badge unres', text: 'UNRESOLVED' }), 'a field the report itself flags unknown'));
      pr.appendChild(row(U.el('span', { text: '★', style: 'color:var(--accent)' }), 'report-flagged anchor (accent border)'));
      wrap.appendChild(pr);
      return wrap;
    }

    function renderOverview() {
      host.replaceChildren();
      const nodes = corpus.nodes, E = relations.edges;
      const ver = nodes.filter((n) => n.verification === 'verified').length;
      const multi = nodes.filter((n) => n.corpora.length > 1).length;
      const unres = nodes.filter((n) => n.unresolved && n.unresolved.length).length;
      const edi = E.filter((e) => e.src === 'editorial').length;
      const cyc = E.filter((e) => e.cycle).length;

      const view = SWE.state.get().view, model = relations.views[view];
      host.appendChild(U.el('div', { class: 'sec', text: 'active model — ' + (model ? model.label : view) }));
      if (model) {
        host.appendChild(U.el('p', { class: 'muted', text: model.semantic }));
        host.appendChild(U.el('p', {}, U.el('b', { text: 'Q. ' }), U.el('span', { text: model.question })));
        host.appendChild(U.el('p', { class: 'muted', text: model.computed }));
      }

      host.appendChild(U.el('div', { class: 'sec', text: 'corpus' }));
      const grid = U.el('div', { class: 'statgrid' });
      const stat = (k, v) => grid.appendChild(U.el('div', {}, U.el('div', { class: 'k', text: k }), U.el('div', { class: 'v', text: String(v) })));
      stat('resources', nodes.length); stat('typed edges', E.length);
      stat('corpora', U.CORPUS_ORDER.length); stat('editorial', edi);
      stat('verified', ver); stat('unverified', nodes.length - ver);
      stat('cross-corpus', multi); stat('UNRESOLVED', unres);
      host.appendChild(grid);
      host.appendChild(U.el('p', { class: 'muted', text: cyc + ' edges close one of the four documented cycles. Hover a node in the graph to trace its full closure; click any resource anywhere for its citation and every typed relation.' }));

      host.appendChild(legendBlock());

      host.appendChild(U.el('div', { class: 'sec', text: 'keyboard' }));
      host.appendChild(U.el('p', { class: 'muted' },
        U.el('span', { class: 'kbd', text: '1–5' }), ' views · ',
        U.el('span', { class: 'kbd', text: '/' }), ' search · ',
        U.el('span', { class: 'kbd', text: 'v' }), ' verification · ',
        U.el('span', { class: 'kbd', text: 'Esc' }), ' close'));

      const foot = U.el('p', { class: 'foot-note' });
      foot.appendChild(document.createTextNode('Seven research passes, one fact layer. Method: '));
      foot.appendChild(U.el('a', { href: 'MODELS.md', text: 'MODELS.md' }));
      foot.appendChild(document.createTextNode(' · '));
      foot.appendChild(U.el('a', { href: 'ARCHITECTURE.md', text: 'ARCHITECTURE.md' }));
      foot.appendChild(document.createTextNode(' · data: '));
      foot.appendChild(U.el('a', { href: 'data/corpus.json', text: 'corpus.json' }));
      foot.appendChild(document.createTextNode(' / '));
      foot.appendChild(U.el('a', { href: 'data/relations.json', text: 'relations.json' }));
      host.appendChild(foot);
    }

    function render() { const s = SWE.state.get(); if (s.sel) renderNode(s.sel); else renderOverview(); }
    SWE.state.on((s, changed) => { if (changed.includes('sel') || (!s.sel && changed.includes('view'))) render(); });
    render();
    return { render };
  }
  return { mount };
})();
