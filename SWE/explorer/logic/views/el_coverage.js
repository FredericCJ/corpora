// views/el_coverage.js — Element view 4: element↔works coverage (shell). Pure inputs from
// CE.coverageBuckets (gap/thin/covered among design elements) and idx.elementsByWork (work→elements
// density); this shell only projects to DOM + wires selection. Two honest signals: where element
// coverage is thin or absent, and which works are element-dense. Page/inner scroll is authorized.
window.SWE = window.SWE || {}; SWE.views = SWE.views || {};
SWE.views['el-coverage'] = (function () {
  'use strict';
  const U = SWE.util, CE = SWE.coreEl;
  const CHUNK = 40;          // work-density page size
  const THIN = 40;           // thin-element page size

  function mount(root, ctx) {
    const idx = ctx.elIndex;
    const meta = CE.VIEWS['el-coverage'];
    let shownWorks = CHUNK, shownThin = THIN;

    const vp = U.el('div', { class: 'vp' });
    vp.appendChild(U.el('div', { class: 'vp-head' },
      U.el('h2', { text: 'Element coverage — where works teach elements' }),
      U.el('p', { class: 'note', text: meta.semantic + ' ' + meta.computed })));
    const body = U.el('div', { class: 'vp-body' });
    const scroll = U.el('div', { class: 'el-scroll' });
    body.appendChild(scroll); vp.appendChild(body); root.appendChild(vp);

    // an element row: name .nm + realm chip + work-count chip; selects the element on click.
    function elLine(n, curSel) {
      const wc = (n.works || []).length;
      const line = U.el('div', { class: 'el-line' + (n.id === curSel ? ' sel' : ''), tabindex: '0', role: 'button', 'data-id': n.id,
        onclick: () => SWE.state.set({ sel: n.id }),
        onkeydown: (ev) => { if (ev.key === 'Enter' || ev.key === ' ') { ev.preventDefault(); SWE.state.set({ sel: n.id }); } } });
      if (n.id === curSel) line.style.outline = '2px solid var(--ink)';
      line.appendChild(U.el('span', { class: 'nm', text: U.shortTitle(n.name, 54) }));
      line.appendChild(U.elChips(n)[0]);
      line.appendChild(U.el('span', { class: 'chip', text: wc + ' work' + (wc === 1 ? '' : 's') }));
      return line;
    }

    function render() {
      const vis = CE.visible(idx, SWE.state.get().q);
      const curSel = SWE.state.get().sel;
      const b = CE.coverageBuckets(idx);
      const gap = b.gap.filter((n) => vis.has(n.id));
      const thin = b.thin.filter((n) => vis.has(n.id));
      const covCount = b.covered.length;
      scroll.replaceChildren();

      // ---- (1) coverage health -------------------------------------------------
      const health = U.el('div', { class: 'el-group' });
      health.appendChild(U.el('h3', { text: 'coverage health' },
        U.el('span', { class: 'sub', text: 'design elements by number of teaching works' })));
      const stats = U.el('div', { class: 'el-legend' });
      const stat = (num, lab) => U.el('span', {}, U.el('span', { class: 'el-count', text: String(num) }), ' ' + lab);
      stats.appendChild(stat(b.gap.length, 'gap · 0 works'));
      stats.appendChild(stat(b.thin.length, 'thin · 1 work'));
      stats.appendChild(stat(covCount, 'covered · ≥2 works'));
      health.appendChild(stats);
      scroll.appendChild(health);

      const two = U.el('div', { class: 'el-two' });
      // gap group (the honest signal — 3 design elements no work teaches)
      const gg = U.el('div', { class: 'el-group' });
      gg.appendChild(U.el('h3', { text: 'gap — no work teaches these' },
        U.el('span', { class: 'sub', text: gap.length + (SWE.state.get().q ? ' matching' : '') })));
      if (gap.length) gap.forEach((n) => gg.appendChild(elLine(n, curSel)));
      else gg.appendChild(U.el('p', { class: 'empty', text: 'none' }));
      two.appendChild(gg);
      // thin group (single-work coverage)
      const tg = U.el('div', { class: 'el-group' });
      tg.appendChild(U.el('h3', { text: 'thin — a single work' },
        U.el('span', { class: 'sub', text: thin.length + (SWE.state.get().q ? ' matching' : '') })));
      if (thin.length) {
        thin.slice(0, shownThin).forEach((n) => tg.appendChild(elLine(n, curSel)));
        if (thin.length > shownThin) tg.appendChild(U.el('button', { class: 'morebtn',
          text: 'show ' + Math.min(THIN, thin.length - shownThin) + ' more (of ' + (thin.length - shownThin) + ')',
          onclick: () => { shownThin += THIN; render(); } }));
      } else tg.appendChild(U.el('p', { class: 'empty', text: 'none' }));
      two.appendChild(tg);
      scroll.appendChild(two);

      // ---- (2) work density ----------------------------------------------------
      const dens = Object.keys(idx.elementsByWork)
        .map((wid) => ({ wid, count: idx.elementsByWork[wid].length }))
        // honour search: a work is visible if any element it teaches matches the query
        .filter((d) => idx.elementsByWork[d.wid].some((eid) => vis.has(eid)))
        .sort((a, b2) => b2.count - a.count || ((idx.works[a.wid] || {}).title || a.wid).localeCompare((idx.works[b2.wid] || {}).title || b2.wid));

      const wg = U.el('div', { class: 'el-group' });
      wg.appendChild(U.el('h3', { text: 'work density — which works teach the most elements' },
        U.el('span', { class: 'sub', text: dens.length + ' works' + (SWE.state.get().q ? ' matching' : '') + ' · corpus works are clickable, ·p8 works are Phase-2 only' })));
      if (!dens.length) wg.appendChild(U.el('p', { class: 'empty', text: 'no works match' }));
      dens.slice(0, shownWorks).forEach((d) => {
        const w = idx.works[d.wid] || {};
        const clickable = w.corpusNode === true;
        const line = U.el('div', { class: 'el-line' + (d.wid === curSel ? ' sel' : '') });
        if (clickable) {
          line.setAttribute('tabindex', '0'); line.setAttribute('role', 'button'); line.setAttribute('data-id', d.wid);
          line.addEventListener('click', () => SWE.state.set({ sel: d.wid }));
          line.addEventListener('keydown', (ev) => { if (ev.key === 'Enter' || ev.key === ' ') { ev.preventDefault(); SWE.state.set({ sel: d.wid }); } });
          if (d.wid === curSel) line.style.outline = '2px solid var(--ink)';
          line.appendChild(U.el('span', { class: 'nm', text: U.shortTitle(w.title || d.wid, 62) }));
        } else {
          const nm = U.el('span', { class: 'nm', text: U.shortTitle(w.title || d.wid, 62) });
          nm.appendChild(U.el('span', { class: 'prov-e', text: ' ·p8' }));
          line.appendChild(nm);
          line.style.cursor = 'default';
        }
        line.appendChild(U.el('span', { class: 'chip', text: d.count + ' element' + (d.count === 1 ? '' : 's') }));
        line.appendChild(U.el('span', { class: 'badge ' + (w.verification === 'verified' ? 'ver' : 'unres'),
          text: w.verification === 'verified' ? 'verified' : 'unverified' }));
        wg.appendChild(line);
      });
      if (dens.length > shownWorks) wg.appendChild(U.el('button', { class: 'morebtn',
        text: 'show ' + Math.min(CHUNK, dens.length - shownWorks) + ' more (of ' + (dens.length - shownWorks) + ')',
        onclick: () => { shownWorks += CHUNK; render(); } }));
      scroll.appendChild(wg);
    }

    render();
    return {
      applyFilters: () => { shownWorks = CHUNK; shownThin = THIN; render(); },
      onSelect: () => render(),
      destroy: () => {},
    };
  }
  return { label: 'Element coverage', mount };
})();
