// views/lineage.js — Model 3: lineages & the path finder (shell). Left: the report's recommended
// source→sink lineage with its per-seam justifications, plus the proof-novice variant. Right: a
// finder that enumerates every directed path between two chosen nodes (exact count from
// core.pathsBetween's DP; enumeration capped and the cap stated — no silent truncation).
window.CALC = window.CALC || {}; CALC.views = CALC.views || {};
CALC.views.lineage = (function () {
  'use strict';
  const U = CALC.util, C = CALC.core;
  const CAP = 400;

  function mount(root, ctx) {
    const corpus = ctx.corpus, relations = ctx.relations;
    const byId = {}; corpus.nodes.forEach((n) => { byId[n.id] = n; });
    const adj = C.adjacency(relations.edges);
    const seamOf = {}; relations.edges.forEach((e) => { seamOf[e.s + '>' + e.t] = e; });
    const pick = { from: 'N01', to: 'N27' };

    const vp = U.el('div', { class: 'vp' });
    vp.appendChild(U.el('div', { class: 'vp-head' },
      U.el('h2', { text: 'Lineages & paths — reading orders through the DAG' }),
      U.el('p', { class: 'note', text: 'The presets are the report’s §7 recommendations, seam justifications verbatim. The finder enumerates directed paths between any two texts; hover an arrow for that hop’s seam, click a chip for the citation. Amber arrows are JUDGMENT hops.' })));
    const body = U.el('div', { class: 'vp-body' });
    const wrap = U.el('div', { class: 'lin' });
    const presets = U.el('div', { class: 'lin-presets' });
    const finder = U.el('div', { class: 'lin-finder' });
    wrap.appendChild(presets); wrap.appendChild(finder); body.appendChild(wrap); vp.appendChild(body); root.appendChild(vp);

    function chipRow(path) {
      const row = U.el('div', { class: 'pathrow' });
      path.forEach((id, i) => {
        if (i) {
          const e = seamOf[path[i - 1] + '>' + id];
          const arr = U.el('span', { class: 'parr' + (e && e.tag === 'JUDGMENT' ? ' jd' : ''), text: '→',
            title: e ? path[i - 1] + ' → ' + id + ' [' + e.tag + ']\nseam: ' + e.seam : '' });
          row.appendChild(arr);
        }
        row.appendChild(U.idChip(byId[id], () => CALC.state.set({ sel: id })));
      });
      return row;
    }

    // left: preset lineage cards (built once — data, not state)
    for (const ln of relations.lineages) {
      const card = U.el('div', { class: 'lincard' });
      card.appendChild(U.el('h3', { text: ln.label }));
      card.appendChild(U.el('p', { class: 'note', text: ln.note }));
      card.appendChild(chipRow(ln.path));
      if (ln.steps.length) {
        const ol = U.el('ol', { class: 'steps' });
        for (const st of ln.steps) {
          const li = U.el('li');
          li.appendChild(U.el('span', { class: 'hop', text: st.frm + ' → ' + st.to + ' ' }));
          li.appendChild(U.el('span', { class: 'why', text: st.note }));
          ol.appendChild(li);
        }
        card.appendChild(ol);
      }
      presets.appendChild(card);
    }

    // right: the finder
    const bar = U.el('div', { class: 'lin-pick' });
    const mkSel = (key) => {
      const s = U.el('select', { 'aria-label': key === 'from' ? 'Path start' : 'Path end' });
      const nodes = corpus.nodes.filter((n) => n.status === 'kept')
        .slice().sort((a, b) => a.tier - b.tier || a.id.localeCompare(b.id));
      for (const n of nodes)
        s.appendChild(U.el('option', { value: n.id, text: 'T' + n.tier + ' · ' + n.id + ' ' + U.shortTitle(n.title, 34) }));
      s.value = pick[key];
      s.addEventListener('change', () => { pick[key] = s.value; renderPaths(); });
      return s;
    };
    bar.appendChild(U.el('label', { text: 'from' })); bar.appendChild(mkSel('from'));
    bar.appendChild(U.el('label', { text: 'to' })); bar.appendChild(mkSel('to'));
    const meta = U.el('span', { class: 'findmeta' }); bar.appendChild(meta);
    finder.appendChild(bar);
    const list = U.el('div', { class: 'lin-paths' });
    finder.appendChild(list);

    function renderPaths() {
      const r = C.pathsBetween(pick.from, pick.to, adj, CAP);
      meta.textContent = r.count === 0 ? 'no directed path'
        : r.count + ' path' + (r.count === 1 ? '' : 's')
          + (r.capped ? ' — showing the first ' + r.paths.length + ' (enumeration capped)' : '')
          + ' · sorted shortest first';
      list.replaceChildren();
      if (!r.count) {
        list.appendChild(U.el('p', { class: 'empty',
          text: 'No directed path from ' + pick.from + ' to ' + pick.to + ' — try the reverse direction, or a common ancestor.' }));
        applyFilters();
        return;
      }
      for (const p of r.paths) list.appendChild(chipRow(p));
      applyFilters();
    }

    function applyFilters() {
      const vis = C.visibleIds(corpus, CALC.state.get());
      for (const chip of vp.querySelectorAll('.pchip'))
        chip.classList.toggle('dim', !vis.has(chip.textContent || ''));
    }
    renderPaths();
    return { applyFilters, onSelect: () => {}, destroy: () => {} };
  }
  return { label: 'Lineages', mount };
})();
