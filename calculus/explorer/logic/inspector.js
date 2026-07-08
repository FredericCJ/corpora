// inspector.js — the persistent inspector dock (shell). Model-aware overview when nothing is
// selected; full citation + tier context + memberships + typed relations when a node is.
// Subscribes to state.sel and state.view.
window.CALC = window.CALC || {};
CALC.inspector = (function () {
  'use strict';
  const U = CALC.util;

  /** @param {HTMLElement} host @param {{corpus:any,relations:any,log?:any}} ctx */
  function mount(host, ctx) {
    const corpus = ctx.corpus, relations = ctx.relations, log = ctx.log || CALC.log.NOOP;
    const byId = {}; corpus.nodes.forEach((n) => { byId[n.id] = n; });
    const tierOf = {}; corpus.tiers.forEach((t) => { tierOf[t.tier] = t; });
    const outE = {}, inE = {};
    for (const e of relations.edges) { (outE[e.s] = outE[e.s] || []).push(e); (inE[e.t] = inE[e.t] || []).push(e); }
    const psOf = {}; relations.parallelSets.forEach((ps) => ps.members.forEach((m) => { psOf[m] = ps; }));
    const gateOf = {}; relations.gate.forEach((g) => g.ids.forEach((i) => { gateOf[i] = g; }));

    const jump = (id) => () => CALC.state.set({ sel: id });

    function edgeRow(e, dir) {
      const other = byId[dir === 'out' ? e.t : e.s];
      const row = U.el('div', { class: 'edge' });
      row.appendChild(U.el('span', { class: 'lnk', text: other.id + ' ' + other.title, tabindex: '0', role: 'link',
        onclick: jump(other.id),
        onkeydown: (ev) => { if (ev.key === 'Enter' || ev.key === ' ') { ev.preventDefault(); CALC.state.set({ sel: other.id }); } } }));
      row.appendChild(document.createTextNode(' '));
      row.appendChild(U.evBadge(e.tag));
      row.appendChild(U.el('span', { class: 'ov', text: 'seam: ' + e.seam + (e.note ? ' — ' + e.note : '') }));
      return row;
    }

    function renderNode(id) {
      const n = byId[id]; if (!n) { renderOverview(); return; }
      host.replaceChildren();
      host.appendChild(U.el('button', { class: 'close', text: 'Esc ✕', 'aria-label': 'Close detail', onclick: () => CALC.state.set({ sel: null }) }));
      host.appendChild(U.el('h2', { text: n.id + ' — ' + n.title }));
      const cite = U.el('p', { class: 'cite' });
      cite.appendChild(U.el('span', { text: n.authors + ' · ' + n.edition + ' ed. · ' }));
      cite.appendChild(U.el('b', { text: n.year }));
      cite.appendChild(U.el('span', { text: ' · ' + n.publisher }));
      host.appendChild(cite);
      if (n.isbn) host.appendChild(U.el('p', { class: 'muted', text: 'ISBN ' + n.isbn }));

      const bl = U.el('div');
      bl.appendChild(U.tierChip(n.tier, 'T' + n.tier));
      bl.appendChild(U.el('span', { class: 'badge plain', text: n.rigor }));
      U.badges(n).forEach((b) => bl.appendChild(b));
      host.appendChild(bl);
      host.appendChild(U.el('p', { text: n.role }));
      if (n.note) host.appendChild(U.el('p', { class: 'muted', text: n.note }));

      host.appendChild(U.el('div', { class: 'sec', text: 'tier ' + n.tier + ' — ' + tierOf[n.tier].name }));
      host.appendChild(U.el('p', { class: 'muted', text: tierOf[n.tier].focus + ' (' + tierOf[n.tier].rigor + ')' }));

      const ps = psOf[id];
      if (ps) {
        host.appendChild(U.el('div', { class: 'sec', text: 'parallel set ' + ps.id + ' — ' + ps.label }));
        host.appendChild(U.el('p', { class: 'muted', text: ps.note + ' Siblings are alternatives, not prerequisites.' }));
        const sw = U.el('p');
        for (const m of ps.members) {
          if (m === id) continue;
          sw.appendChild(U.idChip(byId[m], jump(m)));
          sw.appendChild(document.createTextNode(' '));
        }
        host.appendChild(sw);
      }

      const lins = relations.lineages.filter((l) => l.path.includes(id));
      if (lins.length) {
        host.appendChild(U.el('div', { class: 'sec', text: 'lineage membership' }));
        for (const l of lins)
          host.appendChild(U.el('p', { class: 'muted',
            text: l.label + ' — step ' + (l.path.indexOf(id) + 1) + ' of ' + l.path.length + '.' }));
      }

      const g = gateOf[id];
      host.appendChild(U.el('div', { class: 'sec', text: 'quality gate — ' + g.status }));
      host.appendChild(U.el('p', { class: 'muted', text: g.reason }));

      const ins = inE[id] || [], outs = outE[id] || [];
      host.appendChild(U.el('div', { class: 'sec', text: 'builds on (' + ins.length + ')' }));
      ins.length ? ins.forEach((e) => host.appendChild(edgeRow(e, 'in')))
        : host.appendChild(U.el('p', { class: 'empty', text: n.status === 'dropped' ? 'no edges — dropped by the quality gate' : 'none — this is the source node' }));
      host.appendChild(U.el('div', { class: 'sec', text: 'prerequisite for (' + outs.length + ')' }));
      outs.length ? outs.forEach((e) => host.appendChild(edgeRow(e, 'out')))
        : host.appendChild(U.el('p', { class: 'empty', text: n.status === 'dropped' ? 'no edges — dropped by the quality gate' : 'none — terminal in the graph' }));

      host.appendChild(U.el('div', { class: 'sec', text: 'bibliography (§9, verbatim)' }));
      host.appendChild(U.el('p', { class: 'bib', text: n.bib }));
      log.debug('inspect', { id });
    }

    function legendBlock() {
      const wrap = U.el('div');
      wrap.appendChild(U.el('div', { class: 'sec', text: 'tiers (colour = curriculum depth)' }));
      const lt = U.el('div', { class: 'legend-full' });
      for (const t of corpus.tiers) {
        const box = U.el('span', { class: 'cbox' });
        box.style.background = U.tierFill(t.tier); box.style.borderColor = U.tierStroke(t.tier);
        lt.appendChild(U.el('div', { class: 'lrow' }, box,
          U.el('span', {}, U.el('b', { text: 'T' + t.tier + ' ' }), U.el('span', { class: 'muted', text: t.name }))));
      }
      wrap.appendChild(lt);

      wrap.appendChild(U.el('div', { class: 'sec', text: 'evidence & honesty' }));
      const pr = U.el('div', { class: 'legend-full' });
      const swatch = (color, dashed) => {
        const sw = U.el('span', { class: 'swatch' });
        sw.style.borderTopColor = color; if (dashed) sw.style.borderTopStyle = 'dashed';
        return sw;
      };
      const row = (lead, txt) => U.el('div', { class: 'lrow' }, lead, U.el('span', { class: 'muted', text: txt }));
      pr.appendChild(row(swatch('var(--ev)', false), 'EVIDENCED — ToCs, stated prerequisites, published reviews'));
      pr.appendChild(row(swatch('var(--jd)', true), 'JUDGMENT — reasoned pedagogical judgment (dashed)'));
      pr.appendChild(row(swatch('var(--faint)', true), 'dashed enclosure — parallel set (shared, not sequenced)'));
      pr.appendChild(row(U.el('span', { class: 'badge flag', text: '● source' }), 'minimal-prerequisite entry (N01)'));
      pr.appendChild(row(U.el('span', { class: 'badge flag', text: '■ sink' }), 'research-level sink (N26, N27)'));
      pr.appendChild(row(U.el('span', { class: 'badge flag', text: '◇ terminal leaf' }), 'complex trio — parallel specialization, not a dead end'));
      pr.appendChild(row(U.el('span', { class: 'badge dropped', text: 'dropped' }), 'failed the quality gate; kept visible as a ghost (N18)'));
      pr.appendChild(row(U.el('span', { class: 'badge ver', text: 'verified' }), 'every catalogue row is [VERIFIED] in the report'));
      wrap.appendChild(pr);
      return wrap;
    }

    function renderOverview() {
      host.replaceChildren();
      const st = CALC.core.stats(corpus, relations);
      const view = CALC.state.get().view, model = relations.views[view];
      host.appendChild(U.el('div', { class: 'sec', text: 'active model — ' + (model ? model.label : view) }));
      if (model) {
        host.appendChild(U.el('p', { class: 'muted', text: model.semantic }));
        host.appendChild(U.el('p', {}, U.el('b', { text: 'Q. ' }), U.el('span', { text: model.question })));
        host.appendChild(U.el('p', { class: 'muted', text: model.computed }));
      }

      host.appendChild(U.el('div', { class: 'sec', text: 'corpus' }));
      const grid = U.el('div', { class: 'statgrid' });
      const stat = (k, v) => grid.appendChild(U.el('div', {}, U.el('div', { class: 'k', text: k }), U.el('div', { class: 'v', text: String(v) })));
      stat('texts catalogued', st.nodes); stat('in the DAG', st.kept);
      stat('edges', st.edges); stat('dropped', st.dropped);
      stat('evidenced', st.ev); stat('judgment', st.jd);
      stat('tiers', st.tiers); stat('parallel sets', st.psets);
      stat('source', st.sources); stat('sinks', st.sinks);
      host.appendChild(grid);
      host.appendChild(U.el('p', { class: 'muted', text: 'Acyclicity is machine-checked at build time (Kahn topological sort over all ' + st.kept + ' kept nodes); every edge is tier-monotone. Hover a node in the DAG to trace its full closure; click any text anywhere for its citation and every seam.' }));

      host.appendChild(legendBlock());

      host.appendChild(U.el('div', { class: 'sec', text: 'keyboard' }));
      host.appendChild(U.el('p', { class: 'muted' },
        U.el('span', { class: 'kbd', text: '1–5' }), ' views · ',
        U.el('span', { class: 'kbd', text: '/' }), ' search · ',
        U.el('span', { class: 'kbd', text: 'r' }), ' rigor · ',
        U.el('span', { class: 'kbd', text: 't' }), ' tier · ',
        U.el('span', { class: 'kbd', text: 'Esc' }), ' close'));

      const foot = U.el('p', { class: 'foot-note' });
      foot.appendChild(document.createTextNode('Source: ' + corpus.meta.source + ' (access date ' + corpus.meta.access_date + '). Method: '));
      foot.appendChild(U.el('a', { href: 'MODELS.md', text: 'MODELS.md' }));
      foot.appendChild(document.createTextNode(' · '));
      foot.appendChild(U.el('a', { href: 'ARCHITECTURE.md', text: 'ARCHITECTURE.md' }));
      foot.appendChild(document.createTextNode(' · data: '));
      foot.appendChild(U.el('a', { href: 'data/corpus.json', text: 'corpus.json' }));
      foot.appendChild(document.createTextNode(' / '));
      foot.appendChild(U.el('a', { href: 'data/relations.json', text: 'relations.json' }));
      foot.appendChild(document.createTextNode(' · verification: '));
      foot.appendChild(U.el('a', { href: 'data/corpus_report.md', text: 'corpus_report.md' }));
      host.appendChild(foot);
    }

    function render() { const s = CALC.state.get(); if (s.sel) renderNode(s.sel); else renderOverview(); }
    CALC.state.on((s, changed) => { if (changed.includes('sel') || (!s.sel && changed.includes('view'))) render(); });
    render();
    return { render };
  }
  return { mount };
})();
