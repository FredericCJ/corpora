// detail.js — the persistent inspector dock. Overview when nothing is selected; full node
// citation + typed relations when one is. Subscribes to DS.state.sel only. Logger injected.
window.DS = window.DS || {};
DS.detail = (function () {
  'use strict';
  const U = DS.util;

  const KIND_GLOSS = {
    refines: 'sharpens / optimises within the same interface',
    specializes: 'a restricted or more specific case',
    generalizes: 'a broader form',
    encodes: 'represents / implements one structure via another',
    hybridizes: 'merges two lineages into one structure',
    influences: 'design inspiration, not genealogical descent',
  };
  const PROV_LABEL = { 'report:topology': 'report', 'derived': 'derived', 'editorial': 'EDITORIAL' };

  /** @param {HTMLElement} host @param {{corpus:any,relations:any,log?:any}} ctx */
  function mount(host, ctx) {
    const corpus = ctx.corpus, relations = ctx.relations, log = ctx.log || DS.log.NOOP;
    const byId = {}; corpus.nodes.forEach((n) => { byId[n.id] = n; });
    const outE = {}, inE = {};
    for (const e of relations.edges) { (outE[e.s] = outE[e.s] || []).push(e); (inE[e.t] = inE[e.t] || []).push(e); }

    function famChip(f) {
      const c = U.el('span', { class: 'chip-fam', text: corpus.families[f] || f });
      c.style.color = U.familyStroke(f); c.style.borderColor = U.familyStroke(f);
      c.style.background = U.familyFill(f);
      return c;
    }
    function provBadge(src) {
      return U.el('span', { class: 'badge ' + (src === 'editorial' ? 'edi' : 'rep'), text: PROV_LABEL[src] || src });
    }

    function edgeRow(e, dir) {
      const other = byId[dir === 'out' ? e.t : e.s];
      const row = U.el('div', { class: 'edge' });
      row.appendChild(U.el('span', { class: 'kt', text: dir === 'out' ? e.kind : 'is ' + e.kind + ' of' }));
      row.appendChild(document.createTextNode(' '));
      row.appendChild(U.el('span', { class: 'lnk', text: other ? other.name : e.t, tabindex: '0',
        role: 'link', onclick: () => DS.state.set({ sel: other.id }),
        onkeydown: (ev) => { if (ev.key === 'Enter' || ev.key === ' ') { ev.preventDefault(); DS.state.set({ sel: other.id }); } } }));
      row.appendChild(document.createTextNode(' '));
      row.appendChild(provBadge(e.src));
      if (e.cycle) row.appendChild(U.el('span', { class: 'badge cycle', text: 'cycle ' + e.cycle }));
      if (e.note) row.appendChild(U.el('span', { class: 'ov', text: e.note }));
      return row;
    }

    function renderNode(id) {
      const n = byId[id]; if (!n) { renderOverview(); return; }
      host.replaceChildren();
      host.appendChild(U.el('div', { class: 'sec', text: U.TIER_LABEL[n.tier] + ' · ' + (corpus.families[n.family] || n.family) }));
      host.appendChild(U.el('h2', { text: n.name }));

      const badges = U.el('div');
      badges.appendChild(U.el('span', { class: 'badge ' + (n.verification === 'verified' ? 'ver' : 'flag'), text: n.verification }));
      if (n.verdict) badges.appendChild(U.el('span', { class: 'badge verdict', text: 'audit: ' + n.verdict }));
      if (n.tier !== 'modern') badges.appendChild(U.el('span', { class: 'badge tier', text: '★ ' + U.TIER_LABEL[n.tier] }));
      host.appendChild(badges);

      host.appendChild(U.el('div', { class: 'sec', text: 'origin' }));
      host.appendChild(U.el('p', { class: 'cite', text: n.origin }));
      if (n.note) host.appendChild(U.el('p', { class: 'muted', text: n.note }));

      if (n.flags && n.flags.length) {
        host.appendChild(U.el('div', { class: 'sec', text: 'honesty flags' }));
        const fl = U.el('div');
        n.flags.forEach((f) => fl.appendChild(U.el('span', { class: 'badge flag', text: U.FLAG_LABEL[f] || f })));
        host.appendChild(fl);
      }

      host.appendChild(U.el('div', { class: 'sec', text: 'appears in' }));
      const rep = U.el('div');
      n.reports.forEach((r) => rep.appendChild(U.el('span', { class: 'badge rep', text: corpus.sources[r] || r })));
      host.appendChild(rep);

      const ins = inE[id] || [], outs = outE[id] || [];
      host.appendChild(U.el('div', { class: 'sec', text: 'descends from (' + ins.length + ')' }));
      if (ins.length) ins.forEach((e) => host.appendChild(edgeRow(e, 'in')));
      else host.appendChild(U.el('p', { class: 'empty', text: 'a foundational root — nothing upstream' }));

      host.appendChild(U.el('div', { class: 'sec', text: 'gives rise to (' + outs.length + ')' }));
      if (outs.length) outs.forEach((e) => host.appendChild(edgeRow(e, 'out')));
      else host.appendChild(U.el('p', { class: 'empty', text: 'a leaf — nothing downstream' }));

      log.debug('inspect', { id });
    }

    function legendBlock() {
      const wrap = U.el('div');
      wrap.appendChild(U.el('div', { class: 'sec', text: 'relation kinds (root → modern)' }));
      const lk = U.el('div', { class: 'legend-full' });
      for (const k of relations.kinds) {
        const sw = U.el('span', { class: 'swatch' });
        sw.style.borderTopColor = U.kindColor(k);
        if (k === 'hybridizes' || k === 'influences') sw.style.borderTopStyle = 'dashed';
        lk.appendChild(U.el('span', { class: 'row' }, sw,
          U.el('span', {}, U.el('b', { text: k }), U.el('span', { class: 'muted', text: ' — ' + KIND_GLOSS[k] }))));
      }
      wrap.appendChild(lk);

      wrap.appendChild(U.el('div', { class: 'sec', text: 'provenance & honesty' }));
      const pr = U.el('div', { class: 'legend-full' });
      pr.appendChild(U.el('span', { class: 'row' }, U.el('span', { class: 'badge rep', text: 'report' }),
        U.el('span', { class: 'muted', text: 'stated in the topology report’s typed edge list' })));
      pr.appendChild(U.el('span', { class: 'row' }, U.el('span', { class: 'badge rep', text: 'derived' }),
        U.el('span', { class: 'muted', text: 'mechanically implied by a quoted report sentence' })));
      pr.appendChild(U.el('span', { class: 'row' }, U.el('span', { class: 'badge edi', text: 'EDITORIAL' }),
        U.el('span', { class: 'muted', text: 'my reasoned link (dotted edges)' })));
      pr.appendChild(U.el('span', { class: 'row' }, U.el('span', { text: '★', style: 'color:var(--accent)' }),
        U.el('span', { class: 'muted', text: 'foundational / back-filled root (accent border)' })));
      pr.appendChild(U.el('span', { class: 'row' }, U.el('span', { text: '⚠', style: 'color:var(--flag)' }),
        U.el('span', { class: 'muted', text: 'flagged: folklore / theory-only / uncited / ambiguous (dashed border)' })));
      wrap.appendChild(pr);

      wrap.appendChild(U.el('div', { class: 'sec', text: 'families' }));
      const ff = U.el('div');
      corpus.familyOrder.forEach((f) => ff.appendChild(famChip(f)));
      wrap.appendChild(ff);
      return wrap;
    }

    function renderOverview() {
      host.replaceChildren();
      const nodes = corpus.nodes;
      const ver = nodes.filter((n) => n.verification === 'verified').length;
      const flag = nodes.length - ver;
      const roots = nodes.filter((n) => n.tier !== 'modern').length;

      const ov = U.el('div', { class: 'overview' });
      ov.appendChild(U.el('div', { class: 'sec', text: relations.model.label }));
      ov.appendChild(U.el('p', { class: 'muted', text: relations.model.semantic }));

      const grid = U.el('div', { class: 'statgrid' });
      const stat = (k, v) => { grid.appendChild(U.el('div', {}, U.el('div', { class: 'k', text: k }), U.el('div', { class: 'v', text: String(v) }))); };
      stat('structures', nodes.length);
      stat('relations', relations.edges.length);
      stat('foundational roots', roots);
      stat('families', corpus.familyOrder.length);
      stat('verified', ver);
      stat('flagged', flag);
      ov.appendChild(grid);

      ov.appendChild(U.el('p', { class: 'muted', html:
        'Hover or focus a structure to trace its full ancestor + descendant closure (cycles are ' +
        'followed and terminate). Click for its origin citation and every typed relation. ' +
        'Nothing is invented: uncited structures are flagged, never dropped.' }));

      ov.appendChild(legendBlock());

      ov.appendChild(U.el('div', { class: 'sec', text: 'genuine cycles (topology §4)' }));
      const cy = U.el('div', { class: 'legend-full' });
      for (const c in relations.cycles) {
        cy.appendChild(U.el('span', { class: 'row' }, U.el('span', { class: 'badge cycle', text: c }),
          U.el('span', { class: 'muted', text: relations.cycles[c] })));
      }
      ov.appendChild(cy);

      ov.appendChild(U.el('div', { class: 'sec', text: 'keyboard' }));
      ov.appendChild(U.el('p', { class: 'muted' },
        U.el('span', { class: 'kbd', text: '/' }), ' search · ',
        U.el('span', { class: 'kbd', text: 'Esc' }), ' clear · ',
        U.el('span', { class: 'kbd', text: 'Tab' }), ' move · ',
        U.el('span', { class: 'kbd', text: 'Enter' }), ' inspect'));

      const foot = U.el('p', { class: 'foot-note' });
      foot.appendChild(document.createTextNode('Built from two research reports — '));
      foot.appendChild(U.el('a', { href: '../compass_artifact_wf-1f7348c0-2fd2-4c3e-8dc6-ef2676bcdc86_text_markdown.md', text: 'the 17-structure audit' }));
      foot.appendChild(document.createTextNode(' and '));
      foot.appendChild(U.el('a', { href: '../compass_artifact_wf-95789e49-d1d5-4548-952c-f4eca1023de5_text_markdown.md', text: 'the topology lineage graph' }));
      foot.appendChild(document.createTextNode('. Method: '));
      foot.appendChild(U.el('a', { href: 'MODELS.md', text: 'MODELS.md' }));
      foot.appendChild(document.createTextNode(' · '));
      foot.appendChild(U.el('a', { href: 'ARCHITECTURE.md', text: 'ARCHITECTURE.md' }));
      foot.appendChild(document.createTextNode(' · data: '));
      foot.appendChild(U.el('a', { href: 'data/corpus.json', text: 'corpus.json' }));
      foot.appendChild(document.createTextNode(' / '));
      foot.appendChild(U.el('a', { href: 'data/relations.json', text: 'relations.json' }));
      ov.appendChild(foot);

      host.appendChild(ov);
    }

    function render() {
      const sel = DS.state.get().sel;
      if (sel) renderNode(sel); else renderOverview();
    }
    DS.state.on((s, changed) => { if (changed.includes('sel')) render(); });
    render();
    return { render };
  }

  return { mount };
})();
