// inspector.js — the persistent inspector dock (shell). Model-aware overview when nothing is
// selected; full citation + tags + memberships + derived references when an entry is. The
// downstream-citation guidance line quotes the reports' own verification legend.
window.NET = window.NET || {};
NET.inspector = (function () {
  'use strict';
  const U = NET.util;

  /** @param {HTMLElement} host @param {{corpus:any,relations:any,log?:any}} ctx */
  function mount(host, ctx) {
    const corpus = ctx.corpus, relations = ctx.relations, log = ctx.log || NET.log.NOOP;
    const byId = {}; corpus.nodes.forEach((n) => { byId[n.id] = n; });
    const outE = {}, inE = {};
    for (const e of relations.edges) { (outE[e.s] = outE[e.s] || []).push(e); (inE[e.t] = inE[e.t] || []).push(e); }
    const secTitle = { gen: {}, mat: {} };
    for (const c of ['gen', 'mat']) for (const s of corpus.sections[c]) secTitle[c][s.no] = s.title;

    function edgeRow(e, dir) {
      const other = byId[dir === 'out' ? e.t : e.s];
      const row = U.el('div', { class: 'edge' });
      row.appendChild(U.el('span', { class: 'badge plain', text: dir === 'out' ? e.kind : 'is ' + e.kind + ' by' }));
      row.appendChild(document.createTextNode(' '));
      row.appendChild(U.el('span', { class: 'lnk', text: other.id + ' ' + U.shortTitle(other.title, 60),
        tabindex: '0', role: 'link', onclick: () => NET.state.set({ sel: other.id }),
        onkeydown: (ev) => { if (ev.key === 'Enter' || ev.key === ' ') { ev.preventDefault(); NET.state.set({ sel: other.id }); } } }));
      if (e.quote) row.appendChild(U.el('span', { class: 'ov', text: 'grounded by: ' + e.quote }));
      return row;
    }

    function renderNode(id) {
      const n = byId[id]; if (!n) { renderOverview(); return; }
      host.replaceChildren();
      host.appendChild(U.el('button', { class: 'close', text: 'Esc ✕', 'aria-label': 'Close detail', onclick: () => NET.state.set({ sel: null }) }));
      host.appendChild(U.el('h2', { text: n.title }));
      const cw = U.el('div'); U.corpusChips(n).forEach((c) => cw.appendChild(c)); host.appendChild(cw);
      const bl = U.el('div'); U.badges(n).forEach((b) => bl.appendChild(b)); host.appendChild(bl);

      host.appendChild(U.el('div', { class: 'sec', text: 'citation (verbatim)' }));
      host.appendChild(U.el('p', { class: 'cite', text: n.cite }));
      if (n.matTwin) {
        host.appendChild(U.el('p', { class: 'muted', text: 'MAT-corpus twin record (merged; §' + n.matTwin.section + '): ' + n.matTwin.cite }));
      }

      host.appendChild(U.el('div', { class: 'sec', text: 'tags' }));
      const dl = U.el('dl', { class: 'dl' });
      const add = (k, v) => { if (v && v.length) { dl.appendChild(U.el('dt', { text: k })); dl.appendChild(U.el('dd', { text: Array.isArray(v) ? v.join(', ') : v })); } };
      add('subfield', n.subfield); add('paradigm', n.paradigm); add('type', n.type);
      add('stratum', n.stratum); add('recency', n.recencyRaw); add('identifiers', n.idents);
      host.appendChild(dl);

      host.appendChild(U.el('div', { class: 'sec', text: 'route (section)' }));
      for (const c of n.corpus) {
        const sec = c === 'mat' && n.matTwin ? n.matTwin.section : n.section;
        host.appendChild(U.el('p', { class: 'muted', text: c + ' §' + sec + ' — ' + (secTitle[c][sec] || '') }));
      }

      if (n.note) {
        host.appendChild(U.el('div', { class: 'sec', text: 'relevance note (verbatim)' }));
        host.appendChild(U.el('p', { text: n.note }));
        if (n.matTwin && n.matTwin.note) host.appendChild(U.el('p', { class: 'muted', text: 'MAT twin note: ' + n.matTwin.note }));
      }

      host.appendChild(U.el('div', { class: 'sec', text: 'cite downstream?' }));
      host.appendChild(U.el('p', { class: 'muted', text: relations.verificationLegend[n.verification] +
        (n.quarantined ? ' — this entry sits in the report’s quarantine section.' : '') }));

      const outs = outE[id] || [], ins = inE[id] || [];
      if (outs.length || ins.length) {
        host.appendChild(U.el('div', { class: 'sec', text: 'derived references (' + (outs.length + ins.length) + ')' }));
        outs.forEach((e) => host.appendChild(edgeRow(e, 'out')));
        ins.forEach((e) => host.appendChild(edgeRow(e, 'in')));
      }
      log.debug('inspect', { id });
    }

    function legendBlock() {
      const wrap = U.el('div');
      wrap.appendChild(U.el('div', { class: 'sec', text: 'corpora' }));
      const cf = U.el('div');
      for (const c of ['gen', 'mat']) {
        const chip = U.el('span', { class: 'tchip', text: corpus.corpora[c].label });
        chip.style.color = `var(--c-${c})`; chip.style.borderColor = `var(--c-${c})`; chip.style.background = `var(--c-${c}-bg)`;
        cf.appendChild(chip);
      }
      wrap.appendChild(cf);

      wrap.appendChild(U.el('div', { class: 'sec', text: 'verification discipline (legend, verbatim)' }));
      const lv = U.el('div', { class: 'legend-full' });
      for (const [k, cls] of [['verified-web', 'web'], ['verified-train', 'train'], ['unverified', 'unv']]) {
        lv.appendChild(U.el('div', { class: 'lrow' },
          U.el('span', { class: 'badge ' + cls, text: U.VER_SHORT[k] }),
          U.el('span', { class: 'muted', text: relations.verificationLegend[k] })));
      }
      wrap.appendChild(lv);

      wrap.appendChild(U.el('div', { class: 'sec', text: 'subfields (GEN hues)' }));
      const ls = U.el('div', { class: 'legend-full' });
      for (const s of corpus.subfields.filter((x) => x !== 'other(systems)')) {
        const box = U.el('span', { class: 'cbox' });
        box.style.background = U.subfFill(s); box.style.borderColor = U.subfStroke(s);
        ls.appendChild(U.el('div', { class: 'lrow' }, box, U.el('span', { class: 'muted', text: s })));
      }
      wrap.appendChild(ls);

      wrap.appendChild(U.el('div', { class: 'sec', text: 'paradigms (MAT hues)' }));
      const lp = U.el('div', { class: 'legend-full' });
      for (const p of corpus.paradigms) {
        const box = U.el('span', { class: 'cbox' });
        box.style.background = U.parFill(p); box.style.borderColor = U.parStroke(p);
        lp.appendChild(U.el('div', { class: 'lrow' }, box, U.el('span', { class: 'muted', text: p })));
      }
      wrap.appendChild(lp);
      return wrap;
    }

    function renderOverview() {
      host.replaceChildren();
      const st = NET.core.stats(corpus, relations);
      const view = NET.state.get().view, model = relations.views[view];
      host.appendChild(U.el('div', { class: 'sec', text: 'active model — ' + (model ? model.label : view) }));
      if (model) {
        host.appendChild(U.el('p', { class: 'muted', text: model.semantic }));
        host.appendChild(U.el('p', {}, U.el('b', { text: 'Q. ' }), U.el('span', { text: model.question })));
        host.appendChild(U.el('p', { class: 'muted', text: model.computed }));
      }

      host.appendChild(U.el('div', { class: 'sec', text: 'corpus' }));
      const grid = U.el('div', { class: 'statgrid' });
      const stat = (k, v) => grid.appendChild(U.el('div', {}, U.el('div', { class: 'k', text: k }), U.el('div', { class: 'v', text: String(v) })));
      stat('entries + anchor', st.nodes); stat('cross-corpus', st.merged);
      stat('gen corpus', st.gen); stat('mat corpus', st.mat);
      stat('verified[WEB]', st.web); stat('verified[TRAIN]', st.train);
      stat('unverified', st.unv); stat('quarantined', st.quarantined);
      stat('living docs/tools', st.living); stat('derived refs', st.edges);
      host.appendChild(grid);
      host.appendChild(U.el('p', { class: 'muted', text: 'Both reports were parsed directly by the build — no hand transcription. Counts, numbering, tag vocabularies and the two cross-corpus merges are machine-checked; the log ships as data/corpus_report.md.' }));

      host.appendChild(legendBlock());

      host.appendChild(U.el('div', { class: 'sec', text: 'keyboard' }));
      host.appendChild(U.el('p', { class: 'muted' },
        U.el('span', { class: 'kbd', text: '1–5' }), ' views · ',
        U.el('span', { class: 'kbd', text: '/' }), ' search · ',
        U.el('span', { class: 'kbd', text: 'v' }), ' verification · ',
        U.el('span', { class: 'kbd', text: 'c' }), ' corpus · ',
        U.el('span', { class: 'kbd', text: 'Esc' }), ' close'));

      const foot = U.el('p', { class: 'foot-note' });
      foot.appendChild(document.createTextNode('Sources: ' + corpus.meta.sources.gen + ' · ' + corpus.meta.sources.mat +
        ' (collected ' + corpus.meta.collected + '). Method: '));
      foot.appendChild(U.el('a', { href: 'MODELS.md', text: 'MODELS.md' }));
      foot.appendChild(document.createTextNode(' · '));
      foot.appendChild(U.el('a', { href: 'ARCHITECTURE.md', text: 'ARCHITECTURE.md' }));
      foot.appendChild(document.createTextNode(' · data: '));
      foot.appendChild(U.el('a', { href: 'data/corpus.json', text: 'corpus.json' }));
      foot.appendChild(document.createTextNode(' / '));
      foot.appendChild(U.el('a', { href: 'data/relations.json', text: 'relations.json' }));
      foot.appendChild(document.createTextNode(' · build log: '));
      foot.appendChild(U.el('a', { href: 'data/corpus_report.md', text: 'corpus_report.md' }));
      host.appendChild(foot);
    }

    function render() { const s = NET.state.get(); if (s.sel) renderNode(s.sel); else renderOverview(); }
    NET.state.on((s, changed) => { if (changed.includes('sel') || (!s.sel && changed.includes('view'))) render(); });
    render();
    return { render };
  }
  return { mount };
})();
