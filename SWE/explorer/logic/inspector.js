// inspector.js — the persistent inspector dock (shell). Model-aware overview when nothing is
// selected; full citation + typed relations when a node is. Subscribes to state.sel and state.view.
window.SWE = window.SWE || {};
SWE.inspector = (function () {
  'use strict';
  const U = SWE.util;
  const PROV = { 'report:swa': 'report · swa', 'report:sim': 'report · sim', 'report:proc': 'report · proc', 'derived': 'derived', 'editorial': 'EDITORIAL' };

  /** @param {HTMLElement} host @param {{corpus:any,relations:any,elIndex?:any,log?:any}} ctx */
  function mount(host, ctx) {
    const corpus = ctx.corpus, relations = ctx.relations, log = ctx.log || SWE.log.NOOP;
    const EL = ctx.elIndex || null, CE = SWE.coreEl, AT = ctx.atlasIndex || null;
    const ATLAS_VIEWS = new Set(['el-atlas', 'el-bridgeflow']);
    const byId = {}; corpus.nodes.forEach((n) => { byId[n.id] = n; });
    const outE = {}, inE = {};
    for (const e of relations.edges) { (outE[e.s] = outE[e.s] || []).push(e); (inE[e.t] = inE[e.t] || []).push(e); }

    // ── element layer (design + architecture realms) ──
    function selLink(id, label) {
      return U.el('span', { class: 'lnk', text: label, tabindex: '0', role: 'link',
        onclick: () => SWE.state.set({ sel: id }),
        onkeydown: (ev) => { if (ev.key === 'Enter' || ev.key === ' ') { ev.preventDefault(); SWE.state.set({ sel: id }); } } });
    }
    function elEdgeRow(e, dir) {
      const otherId = dir === 'out' ? e.to : e.from, other = EL.byId[otherId];
      const row = U.el('div', { class: 'edge' });
      row.appendChild(U.el('span', { class: 'kt', text: dir === 'out' ? e.kind : 'is ' + e.kind + ' of' }));
      row.appendChild(document.createTextNode(' '));
      row.appendChild(selLink(otherId, other ? other.name : otherId));
      if (other) row.appendChild(U.el('span', { class: 'chip ' + (U.REALM_CLS[other.realm] || ''), text: U.REALM_SHORT[other.realm] }));
      row.appendChild(document.createTextNode(' '));
      row.appendChild(U.el('span', { class: 'badge ' + (e.provenance === 'sourced' ? 'rep' : e.provenance === 'derived' ? 'cycle' : 'edi'),
        text: e.provenance === 'sourced' ? 'sourced' : e.provenance === 'derived' ? 'derived' : 'EDITORIAL' }));
      if (e.cite) row.appendChild(U.el('span', { class: 'ov', text: e.cite }));
      if (e.note) row.appendChild(U.el('span', { class: 'ov', text: e.note }));
      return row;
    }
    function workChip(wid) {
      const w = EL.works[wid];
      if (w && w.corpusNode) return selLink(wid, (w.title || wid).slice(0, 46));   // -> full corpus detail
      return U.el('span', { class: 'chip', title: w ? (w.authors + ' · ' + w.year) : wid, text: (w ? w.title : wid).slice(0, 46) + (w && !w.corpusNode ? ' ·p8' : '') });
    }
    function renderElement(id) {
      const n = EL.byId[id]; if (!n) { renderOverview(); return; }
      host.replaceChildren();
      host.appendChild(U.el('button', { class: 'close', text: 'Esc ✕', 'aria-label': 'Close detail', onclick: () => SWE.state.set({ sel: null }) }));
      host.appendChild(U.el('h2', { text: n.name }));
      const bl = U.el('div');
      bl.appendChild(U.el('span', { class: 'chip ' + (U.REALM_CLS[n.realm] || ''), text: 'realm: ' + n.realm }));
      bl.appendChild(U.el('span', { class: 'chip', text: 'kind: ' + n.kind }));
      U.elBadges(n).forEach((b) => bl.appendChild(b));
      host.appendChild(bl);
      if (n.aka && n.aka.length) host.appendChild(U.el('p', { class: 'muted', text: 'aka: ' + n.aka.join(', ') }));
      host.appendChild(U.el('p', { text: n.what }));
      if (n.problem) host.appendChild(U.el('p', { class: 'muted', text: n.problem }));
      if (n.borderline) { host.appendChild(U.el('div', { class: 'sec', text: 'borderline (altitude)' })); host.appendChild(U.el('p', { class: 'muted', text: n.borderline })); }

      host.appendChild(U.el('div', { class: 'sec', text: 'named in' }));
      const ni = U.el('p', {});
      if (n.named_in_corpus_id && EL.works[n.named_in_corpus_id] && EL.works[n.named_in_corpus_id].corpusNode) ni.appendChild(selLink(n.named_in_corpus_id, n.named_in));
      else ni.appendChild(U.el('span', { text: n.named_in }));
      host.appendChild(ni);
      if (n.tags && n.tags.length) { const tw = U.el('div'); n.tags.forEach((t) => tw.appendChild(U.el('span', { class: 'chip', text: t }))); host.appendChild(tw); }

      host.appendChild(U.el('div', { class: 'sec', text: 'covering works — pass 8 (' + n.works.length + ')' }));
      if (n.works.length) { const cw = U.el('div'); n.works.forEach((w) => cw.appendChild(workChip(w))); host.appendChild(cw); }
      else host.appendChild(U.el('p', { class: 'empty', text: 'no catalog-grade covering work (explicit gap)' }));

      const outs = EL.out[id] || [], ins = EL.inn[id] || [];
      const crossOut = outs.filter((e) => CE.isCross(e.kind)), otherOut = outs.filter((e) => !CE.isCross(e.kind));
      host.appendChild(U.el('div', { class: 'sec', text: (n.realm === 'design' ? 'bridges to architecture' : 'realized by / constrains') + ' (' + crossOut.length + ')' }));
      crossOut.length ? crossOut.forEach((e) => host.appendChild(elEdgeRow(e, 'out'))) : host.appendChild(U.el('p', { class: 'empty', text: 'none' }));
      if (otherOut.length) { host.appendChild(U.el('div', { class: 'sec', text: 'relates to (' + otherOut.length + ')' })); otherOut.forEach((e) => host.appendChild(elEdgeRow(e, 'out'))); }
      if (ins.length) { host.appendChild(U.el('div', { class: 'sec', text: 'related from (' + ins.length + ')' })); ins.forEach((e) => host.appendChild(elEdgeRow(e, 'in'))); }
      log.debug('inspect element', { id });
    }

    // pass-8 referenced work (BoK chronology ·p8) — outside the reading corpus, but grounds elements.
    function renderWork(wid) {
      const w = EL.works[wid]; if (!w) { renderOverview(); return; }
      host.replaceChildren();
      host.appendChild(U.el('button', { class: 'close', text: 'Esc ✕', 'aria-label': 'Close detail', onclick: () => SWE.state.set({ sel: null }) }));
      host.appendChild(U.el('h2', { text: w.title || wid }));
      const cite = U.el('p', { class: 'cite' });
      cite.appendChild(U.el('span', { text: (w.authors || 'authors unrecorded') + ' · ' }));
      cite.appendChild(U.el('b', { text: w.year || '—' }));
      host.appendChild(cite);
      const bl = U.el('div');
      bl.appendChild(U.el('span', { class: 'badge ' + (w.verification === 'verified' ? 'ver' : 'unv'), text: w.verification || 'unverified' }));
      bl.appendChild(U.el('span', { class: 'chip', text: 'referenced work · pass 8' }));
      if (w.type && w.type !== 'other') bl.appendChild(U.el('span', { class: 'chip', text: w.type }));
      host.appendChild(bl);
      host.appendChild(U.el('p', { class: 'muted', text: 'Referenced by the element layer but outside the seven-pass reading corpus (·p8) — it grounds one or more design/architecture elements without itself being part of the reading graph.' }));
      const taught = (EL && EL.elementsByWork[wid]) || [];
      host.appendChild(U.el('div', { class: 'sec', text: 'defines elements — pass 8 (' + taught.length + ')' }));
      if (taught.length) {
        const tw = U.el('div');
        taught.forEach((eid) => { const en = EL.byId[eid]; const c = selLink(eid, (en ? en.name : eid).slice(0, 40)); c.classList.add('chip'); tw.appendChild(c); });
        host.appendChild(tw);
      } else host.appendChild(U.el('p', { class: 'empty', text: 'none' }));
      log.debug('inspect pass-8 work', { id: wid });
    }

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

      // work -> element navigation: elements this work defines/teaches (pass 8)
      const taught = (EL && EL.elementsByWork[id]) || [];
      if (taught.length) {
        host.appendChild(U.el('div', { class: 'sec', text: 'teaches elements — pass 8 (' + taught.length + ')' }));
        const tw = U.el('div');
        taught.slice(0, 40).forEach((eid) => {
          const en = EL.byId[eid];
          const chip = selLink(eid, (en ? en.name : eid).slice(0, 40));
          chip.classList.add('chip'); tw.appendChild(chip);
        });
        if (taught.length > 40) tw.appendChild(U.el('span', { class: 'chip', text: '+' + (taught.length - 40) + ' more' }));
        host.appendChild(tw);
      }
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

    function renderElementOverview(view) {
      host.replaceChildren();
      const m = EL.meta, model = CE.VIEWS[view];
      host.appendChild(U.el('div', { class: 'sec', text: 'active view — ' + (model ? model.label : view) }));
      if (model) {
        host.appendChild(U.el('p', { class: 'muted', text: model.semantic }));
        host.appendChild(U.el('p', {}, U.el('b', { text: 'Q. ' }), U.el('span', { text: model.question })));
        host.appendChild(U.el('p', { class: 'muted', text: model.computed }));
      }
      host.appendChild(U.el('div', { class: 'sec', text: 'element layer' }));
      const grid = U.el('div', { class: 'statgrid' });
      const stat = (k, v) => grid.appendChild(U.el('div', {}, U.el('div', { class: 'k', text: k }), U.el('div', { class: 'v', text: String(v) })));
      stat('design elements', m.designCount); stat('architecture', m.archCount);
      stat('bridge edges', m.edgeCount); stat('cross-realm', m.crossRealm);
      stat('bridged', m.bridged + '/' + m.designCount); stat('unbridged', m.unbridgedCount);
      stat('sourced edges', m.sourced); stat('editorial', m.editorial);
      host.appendChild(grid);
      host.appendChild(U.el('p', { class: 'muted', text: 'Two realms below and above software architecture, wired by a typed, provenance-tagged bridge. ' + m.designCovered + '/' + m.designCount + ' design elements reach a catalog-grade work (pass 8); ' + m.unbridgedCount + ' design elements have no architectural counterpart (listed in the bridge view). Click any element for its definition, covering works, and typed relations.' }));
      host.appendChild(U.el('div', { class: 'sec', text: 'realms' }));
      const rf = U.el('div');
      rf.appendChild(U.el('span', { class: 'chip re-design', text: 'design — implementation-level mechanisms' }));
      rf.appendChild(U.el('span', { class: 'chip re-arch', text: 'architecture — styles · tactics · patterns' }));
      host.appendChild(rf);
      host.appendChild(U.el('div', { class: 'sec', text: 'keyboard' }));
      host.appendChild(U.el('p', { class: 'muted' },
        U.el('span', { class: 'kbd', text: '1–9' }), ' views · ',
        U.el('span', { class: 'kbd', text: '/' }), ' search · ',
        U.el('span', { class: 'kbd', text: 'Esc' }), ' close'));
    }

    // ── atlas layer (islands) ──
    function renderIsland(islId) {
      const isl = AT.islandById[islId]; if (!isl) { renderAtlasOverview(); return; }
      host.replaceChildren();
      host.appendChild(U.el('button', { class: 'close', text: '↑ Archipelago', 'aria-label': 'Back to the archipelago', onclick: () => SWE.state.set({ island: '', sel: null }) }));
      host.appendChild(U.el('h2', { text: isl.name }));
      const bl = U.el('div');
      const fam = AT.familyName[isl.family] || isl.family;
      const sw = U.el('span', { class: 'chip' }); sw.style.borderColor = AT.familyHex[isl.family]; sw.style.color = AT.familyHex[isl.family];
      sw.textContent = 'family: ' + fam; bl.appendChild(sw);
      bl.appendChild(U.el('span', { class: 'chip', text: isl.size + ' elements' }));
      bl.appendChild(U.el('span', { class: 'chip', text: (isl.realm_split.design || 0) + ' design · ' + (isl.realm_split.architecture || 0) + ' arch' }));
      host.appendChild(bl);
      host.appendChild(U.el('p', { class: 'muted', text: 'An emergent community — a topic that clusters on its own from the relation graph. Cohesion ' + isl.cohesion + ' edges/element.' }));

      host.appendChild(U.el('div', { class: 'sec', text: 'hub' }));
      const hub = EL.byId[isl.hub];
      host.appendChild(U.el('p', {}, selLink(isl.hub, hub ? hub.name : isl.hub),
        U.el('span', { class: 'chip ' + (U.REALM_CLS[hub && hub.realm] || ''), text: hub ? U.REALM_SHORT[hub.realm] : '' })));

      if (isl.representatives && isl.representatives.length) {
        host.appendChild(U.el('div', { class: 'sec', text: 'representative members' }));
        const rw = U.el('div');
        isl.representatives.forEach((rid) => { const rn = EL.byId[rid]; const c = selLink(rid, (rn ? rn.name : rid).slice(0, 40)); c.classList.add('chip'); rw.appendChild(c); });
        host.appendChild(rw);
      }
      host.appendChild(U.el('div', { class: 'sec', text: 'composition (top kinds)' }));
      const kw = U.el('div');
      (isl.top_kinds || []).forEach((kv) => kw.appendChild(U.el('span', { class: 'chip', text: kv[0] + ' · ' + kv[1] })));
      host.appendChild(kw);

      if (isl.neighbours && isl.neighbours.length) {
        host.appendChild(U.el('div', { class: 'sec', text: 'neighbouring islands (ports)' }));
        const nw = U.el('div');
        isl.neighbours.slice(0, 8).forEach((nb) => {
          const other = AT.islandById[nb.island]; if (!other) return;
          const c = U.el('span', { class: 'chip clickable', text: U.shortTitle(other.name, 26) + ' · ' + nb.weight, tabindex: '0', role: 'link',
            onclick: () => SWE.state.set({ island: other.id, sel: null }),
            onkeydown: (ev) => { if (ev.key === 'Enter' || ev.key === ' ') { ev.preventDefault(); SWE.state.set({ island: other.id, sel: null }); } } });
          c.style.borderColor = AT.familyHex[other.family]; nw.appendChild(c);
        });
        host.appendChild(nw);
      }
      host.appendChild(U.el('p', { class: 'muted', text: 'Click a node in the island for its full detail; a rim port hops to a neighbour.' }));
    }

    function renderAtlasOverview() {
      host.replaceChildren();
      const a = AT.atlas, m = a.meta;
      host.appendChild(U.el('div', { class: 'sec', text: 'active view — ' + (SWE.state.get().view === 'el-bridgeflow' ? 'Bridge-Flow' : 'Atlas — the archipelago') }));
      host.appendChild(U.el('p', { class: 'muted', text: 'A map of the whole element space at three zoom levels: the archipelago of islands, one island, then a node. Geography is emergent and deterministic — the same map every visit.' }));
      host.appendChild(U.el('div', { class: 'sec', text: 'atlas' }));
      const grid = U.el('div', { class: 'statgrid' });
      const stat = (k, v) => grid.appendChild(U.el('div', {}, U.el('div', { class: 'k', text: k }), U.el('div', { class: 'v', text: String(v) })));
      stat('islands', m.islandCount); stat('elements', m.elementCount);
      stat('relations', m.edgeCount); stat('families', m.families.length);
      host.appendChild(grid);
      host.appendChild(U.el('div', { class: 'sec', text: 'families' }));
      const fw = U.el('div');
      m.families.forEach((f) => { const c = U.el('span', { class: 'chip', text: f.name }); c.style.borderColor = f.hex; c.style.color = f.hex; fw.appendChild(c); });
      host.appendChild(fw);
      host.appendChild(U.el('div', { class: 'sec', text: 'largest islands' }));
      const iw = U.el('div');
      a.islands.slice().sort((x, y) => y.size - x.size).slice(0, 8).forEach((isl) => {
        const c = U.el('span', { class: 'chip clickable', text: U.shortTitle(isl.name, 24) + ' · ' + isl.size, tabindex: '0', role: 'link',
          onclick: () => SWE.state.set({ view: 'el-atlas', island: isl.id, sel: null }) });
        c.style.borderColor = AT.familyHex[isl.family]; iw.appendChild(c);
      });
      host.appendChild(iw);
      host.appendChild(U.el('p', { class: 'muted', text: 'Click an island to fly in, or search to teleport to a match.' }));
    }

    function render() {
      const s = SWE.state.get();
      if (s.sel && EL && EL.byId[s.sel]) { renderElement(s.sel); return; }
      if (s.sel && byId[s.sel]) { renderNode(s.sel); return; }
      if (s.sel && EL && EL.works[s.sel] && !EL.works[s.sel].corpusNode) { renderWork(s.sel); return; }
      if (s.sel) { renderNode(s.sel); return; }
      if (AT && ATLAS_VIEWS.has(s.view)) { s.island && AT.islandById[s.island] ? renderIsland(s.island) : renderAtlasOverview(); return; }
      if (EL && CE.VIEWS[s.view]) { renderElementOverview(s.view); return; }
      renderOverview();
    }
    SWE.state.on((s, changed) => { if (changed.includes('sel') || changed.includes('island') || (!s.sel && changed.includes('view'))) render(); });
    render();
    return { render };
  }
  return { mount };
})();
