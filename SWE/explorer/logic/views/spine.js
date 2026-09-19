// views/spine.js — Model 12: the architecture spine (shell). The pass-9 coverage matrix:
// seven domains x five derivation stages, live counts over real node tags. Pure counting via
// core.facetCount/passLocal on the `stages` / `domains` array facets — no inference, no synthetic
// node fields. Thin-cell adjudications come from the build (relations.views.spine.thin), never
// from a guess made here.
window.SWE = window.SWE || {}; SWE.views = SWE.views || {};
SWE.views.spine = (function () {
  'use strict';
  const U = SWE.util, C = SWE.core;

  const STAGES = ['needs', 'obligations', 'requirements', 'design', 'tools-process'];
  const DOMAINS = ['complex-scale', 'complex-science', 'governance', 'measurement', 'runtime-ops', 'hand-c', 'model-c'];
  const STAGE_LABEL = { 'tools-process': 'tools & process' };
  const CHUNK = 120;

  function mount(root, ctx) {
    const corpus = ctx.corpus;
    const viewDef = (ctx.relations && ctx.relations.views && ctx.relations.views.spine) || {};
    const THIN = viewDef.thin || {};            // "domain x stage" -> {adjudication, why}
    let selStage = null, selDomain = null, shown = CHUNK;

    const vp = U.el('div', { class: 'vp' });
    vp.appendChild(U.el('div', { class: 'vp-head' },
      U.el('h2', { text: 'The spine — stakeholder needs → obligations → requirements → design → tools' }),
      U.el('p', { class: 'note', text: 'Pass 9. Seven domains against the five derivation stages: 35 cells, each a coverage question. Counts are live over the works’ own stage/domain tags and honour the global search, verification and corpus filters. A thin cell is a finding, not a gap in the reading — hover one to see whether it was adjudicated literature-thin (the field never wrote that intersection) or sweep-thin (the sweep looked in the wrong vocabulary).' })));

    const grid = U.el('div', { class: 'spine-grid' });
    const body = U.el('div', { class: 'vp-body' });
    const results = U.el('div', { class: 'results' });
    body.appendChild(results);
    vp.appendChild(grid); vp.appendChild(body); root.appendChild(vp);

    /** Works carrying at least one spine tag, after the global filters. */
    function spineNodes() {
      const vis = C.visibleIds(corpus, SWE.state.get());
      return corpus.nodes.filter((n) => vis.has(n.id) && (n.stages || []).length);
    }
    const inCell = (n, d, s) => (n.domains || []).includes(d) && (n.stages || []).includes(s);

    function render() {
      const base = spineNodes();
      grid.replaceChildren();

      if (!base.length) {
        grid.appendChild(U.el('p', { class: 'note', text: 'No works carry spine tags in the current filter. Pass 9 may not be built into this data layer yet — run build/build.py.' }));
        results.replaceChildren();
        return;
      }

      // counts first, so the density ramp is scaled to what is actually on screen
      const count = {}; let peak = 0;
      for (const d of DOMAINS) for (const s of STAGES) {
        const k = d + ' x ' + s;
        count[k] = base.filter((n) => inCell(n, d, s)).length;
        if (count[k] > peak) peak = count[k];
      }

      const table = U.el('div', { class: 'spine-table', role: 'grid', 'aria-label': 'Coverage matrix: seven domains by five stages' });
      // header row — the chain reads left to right, with the derivation arrow between stages
      const head = U.el('div', { class: 'spine-row spine-head', role: 'row' });
      head.appendChild(U.el('div', { class: 'spine-corner', role: 'columnheader' }));
      STAGES.forEach((s, i) => {
        const cell = U.el('div', { class: 'spine-colhead' + (selStage === s ? ' sel' : ''), role: 'columnheader' });
        if (i) cell.appendChild(U.el('span', { class: 'spine-arrow', 'aria-hidden': 'true', text: '→' }));
        cell.appendChild(U.el('button', {
          class: 'spine-hbtn', text: STAGE_LABEL[s] || s,
          title: 'filter to the ' + s + ' stage',
          onclick: () => { selStage = selStage === s ? null : s; shown = CHUNK; render(); },
        }));
        head.appendChild(cell);
      });
      table.appendChild(head);

      for (const d of DOMAINS) {
        const row = U.el('div', { class: 'spine-row', role: 'row' });
        row.appendChild(U.el('button', {
          class: 'spine-rowhead' + (selDomain === d ? ' sel' : ''), role: 'rowheader', text: d,
          title: 'filter to the ' + d + ' domain',
          onclick: () => { selDomain = selDomain === d ? null : d; shown = CHUNK; render(); },
        }));
        for (const s of STAGES) {
          const k = d + ' x ' + s, n = count[k], thin = THIN[k];
          const on = (!selStage || selStage === s) && (!selDomain || selDomain === d);
          const heat = peak ? Math.min(1, n / peak) : 0;
          const cell = U.el('button', {
            class: 'spine-cell' + (on ? '' : ' dim') + (thin ? ' thin-' + thin.adjudication : '') + (n === 0 ? ' empty' : ''),
            role: 'gridcell',
            'data-cell': k,
            title: k + ' — ' + n + ' work' + (n === 1 ? '' : 's') + (thin ? '\n' + thin.adjudication + ': ' + thin.why : ''),
            onclick: () => {
              const already = selStage === s && selDomain === d;
              selStage = already ? null : s; selDomain = already ? null : d;
              shown = CHUNK; render();
            },
          });
          cell.style.setProperty('--heat', heat.toFixed(3));
          cell.appendChild(U.el('span', { class: 'spine-n', text: String(n) }));
          if (thin) cell.appendChild(U.el('span', { class: 'spine-flag', 'aria-hidden': 'true', text: thin.adjudication === 'literature-thin' ? '○' : '△' }));
          row.appendChild(cell);
        }
        table.appendChild(row);
      }
      grid.appendChild(table);

      const legend = U.el('div', { class: 'spine-legend' },
        U.el('span', { class: 'chip', text: base.length + ' works carry a spine tag' }),
        U.el('span', { class: 'lgd', text: '△ sweep-thin — the material exists, the sweep missed it' }),
        U.el('span', { class: 'lgd', text: '○ literature-thin — the field has not written this intersection' }));
      if (selStage || selDomain) {
        legend.appendChild(U.el('button', {
          class: 'chip clickable', text: 'clear cell selection',
          onclick: () => { selStage = null; selDomain = null; shown = CHUNK; render(); },
        }));
      }
      grid.appendChild(legend);

      // ── result list ──────────────────────────────────────────────────────────────
      const rows = base
        .filter((n) => (!selStage || (n.stages || []).includes(selStage)) && (!selDomain || (n.domains || []).includes(selDomain)))
        .sort((a, b) => a.title.localeCompare(b.title));
      results.replaceChildren();
      const what = selStage && selDomain ? selDomain + ' × ' + selStage
        : selStage ? 'stage: ' + selStage
        : selDomain ? 'domain: ' + selDomain
        : 'the whole spine';
      const head2 = U.el('p', { class: 'rescount', text: rows.length + ' work' + (rows.length === 1 ? '' : 's') + ' — ' + what });
      const thinNow = (selStage && selDomain) ? THIN[selDomain + ' x ' + selStage] : null;
      if (thinNow) head2.appendChild(U.el('span', { class: 'reach', text: ' · ' + thinNow.adjudication + ' — ' + thinNow.why }));
      results.appendChild(head2);

      const ul = U.el('ul', { class: 'rows' });
      const curSel = SWE.state.get().sel;
      rows.slice(0, shown).forEach((n) => {
        const li = U.el('li', {
          class: 'row' + (n.id === curSel ? ' sel' : ''), tabindex: '0', role: 'button', 'data-id': n.id,
          onclick: () => SWE.state.set({ sel: n.id }),
          onkeydown: (ev) => { if (ev.key === 'Enter' || ev.key === ' ') { ev.preventDefault(); SWE.state.set({ sel: n.id }); } },
        });
        if (n.id === curSel) li.style.outline = '2px solid var(--ink)';
        const l1 = U.el('div');
        l1.appendChild(U.el('span', { class: 't', text: U.shortTitle(n.title, 70) }));
        U.badges(n).slice(0, 3).forEach((b) => l1.appendChild(b));
        li.appendChild(l1);
        li.appendChild(U.el('div', { class: 'a', text: n.authors + ' · ' + n.year + (n.ident ? ' · ' + n.ident : '') }));
        const l3 = U.el('div');
        U.corpusChips(n).forEach((c) => l3.appendChild(c));
        (n.stages || []).forEach((s) => l3.appendChild(U.el('span', { class: 'chip stage-chip' + (s === selStage ? ' sel' : ''), text: STAGE_LABEL[s] || s })));
        (n.domains || []).forEach((d) => l3.appendChild(U.el('span', { class: 'chip domain-chip' + (d === selDomain ? ' sel' : ''), text: d })));
        li.appendChild(l3);
        ul.appendChild(li);
      });
      results.appendChild(ul);
      if (rows.length > shown) results.appendChild(U.el('button', {
        class: 'morebtn',
        text: 'show ' + Math.min(CHUNK, rows.length - shown) + ' more (of ' + (rows.length - shown) + ')',
        onclick: () => { shown += CHUNK; render(); },
      }));
    }

    render();
    return { applyFilters: render, onSelect: () => render(), destroy: () => {} };
  }

  return { label: 'Spine', mount };
})();
