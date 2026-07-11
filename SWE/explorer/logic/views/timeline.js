// views/timeline.js — Model 3: Chronology (shell), TWO MODES (WV3 of the Body-of-Knowledge group):
//   • BoK      — the whole referenced literature: the 468 reading-corpus works ∪ the 336 works
//                referenced only by the element layer (marked ·p8), by year of last publication.
//                Living, continuously-revised documents are their own stratum; unpinnable → UNRESOLVED.
//   • Elements — the 1083 design & architecture elements by the build-derived year each concept was
//                named (core.elementStrata*). No LIVING stratum; the undatable tail → UNRESOLVED.
// A segmented control switches modes; the choice round-trips through state.tlmode (hash deep-link).
// Strata become columns that fill the pane; each column scrolls internally (single viewport).
window.SWE = window.SWE || {}; SWE.views = SWE.views || {};
SWE.views.timeline = (function () {
  'use strict';
  const U = SWE.util, C = SWE.core;

  function mount(root, ctx) {
    const corpus = ctx.corpus;
    const works = (ctx.elements && ctx.elements.works) || {};
    const elements = (ctx.elements && ctx.elements.nodes) || [];
    const emeta = (ctx.elements && ctx.elements.meta) || {};
    const p8count = Object.keys(works).reduce((a, w) => a + (works[w].corpusNode ? 0 : 1), 0);

    const vp = U.el('div', { class: 'vp' });
    const head = U.el('div', { class: 'vp-head' });
    const h2 = U.el('h2', {});
    const seg = U.el('div', { class: 'tl-modes', role: 'tablist', 'aria-label': 'Chronology mode' });
    const btnBok = U.el('button', { class: 'seg', type: 'button', role: 'tab', text: 'Body of Knowledge',
      onclick: () => SWE.state.set({ tlmode: 'bok', sel: null }) });
    const btnEl = U.el('button', { class: 'seg', type: 'button', role: 'tab', text: 'Elements',
      onclick: () => SWE.state.set({ tlmode: 'elements', sel: null }) });
    seg.appendChild(btnBok); seg.appendChild(btnEl);
    head.appendChild(U.el('div', { class: 'tl-headrow' }, h2, seg));
    const note = U.el('p', { class: 'note' });
    head.appendChild(note);
    vp.appendChild(head);
    const body = U.el('div', { class: 'vp-body' });
    const tl = U.el('div', { class: 'tl' });
    body.appendChild(tl); vp.appendChild(body); root.appendChild(vp);
    let chipEls = {};

    const curMode = () => (SWE.state.get().tlmode === 'elements' ? 'elements' : 'bok');

    // ── BoK dataset: reading-corpus works (search/ver/corpus filtered) ∪ pass-8-only works (·p8) ──
    function bokNodes() {
      const st = SWE.state.get(), q = (st.q || '').trim().toLowerCase();
      const vis = C.visibleIds(corpus, st);
      const out = corpus.nodes.filter((n) => vis.has(n.id));
      if (!st.corpus) {                                   // pass-8-only works carry no corpus membership
        for (const wid in works) {
          const w = works[wid]; if (w.corpusNode) continue;
          if (st.ver && w.verification !== st.ver) continue;
          if (q && !((w.title + ' ' + w.authors + ' ' + w.id).toLowerCase().includes(q))) continue;
          out.push({ id: w.id, title: w.title || w.id, authors: w.authors || '', year: w.year || '',
                     verification: w.verification || 'unverified', corpora: [], p8: true });
        }
      }
      return out;
    }
    // ── Elements dataset: every element (search-filtered) placed by its derived year ──
    function elementNodes() {
      const q = (SWE.state.get().q || '').trim().toLowerCase();
      if (!q) return elements;
      return elements.filter((n) => (n.id + ' ' + n.name + ' ' + (n.aka || []).join(' ') + ' ' + (n.what || '')).toLowerCase().includes(q));
    }

    function render() {
      const mode = curMode(), curSel = SWE.state.get().sel;
      btnBok.classList.toggle('on', mode === 'bok'); btnBok.setAttribute('aria-selected', mode === 'bok');
      btnEl.classList.toggle('on', mode === 'elements'); btnEl.setAttribute('aria-selected', mode === 'elements');
      tl.replaceChildren(); chipEls = {};
      if (mode === 'elements') {
        h2.textContent = 'Chronology — when the field named its concepts';
        note.textContent = 'The ' + elements.length + ' design & architecture elements, placed by the year each concept was named '
          + '(build-derived: named_in year → corpus id → earliest covering work). ' + (emeta.undated || 0)
          + ' the waterfall could not date sit in UNRESOLVED; there is no “living” stratum. Left stripe marks realm (design / architecture).';
        renderStrata(C.elementStrataBuckets(elementNodes()), C.ELEMENT_STRATA, true, curSel);
      } else {
        h2.textContent = 'Chronology — the body of knowledge by year';
        note.textContent = 'The whole referenced literature — ' + corpus.nodes.length + ' reading-corpus works together with ' + p8count
          + ' works referenced only by the element layer (marked ·p8) — by year of last publication. Living, continuously-revised '
          + 'documents (toolchains, vendor docs, guidelines) are a real stratum, not a defect; years the reports could not pin land in UNRESOLVED.';
        renderStrata(C.strataBuckets(bokNodes()), C.STRATA, false, curSel);
      }
    }

    function renderStrata(buckets, strata, isEl, curSel) {
      let any = false;
      for (const s of strata) {
        const list = buckets[s]; if (!list || !list.length) continue;
        any = true;
        const col = U.el('div', { class: 'tl-col' });
        col.appendChild(U.el('div', { class: 'h' }, U.el('b', { text: s }), U.el('span', { text: ' · ' + list.length })));
        const scroll = U.el('div', { class: 'tl-scroll' });
        for (const n of list) { const chip = isEl ? elementChip(n, curSel) : workChip(n, s, curSel); scroll.appendChild(chip); chipEls[n.id] = chip; }
        col.appendChild(scroll); tl.appendChild(col);
      }
      if (!any) tl.appendChild(U.el('p', { class: 'empty', text: 'nothing matches the current filters' }));
    }

    function workChip(n, stratum, curSel) {
      const chip = U.el('button', { class: 'nodechip' + (n.p8 ? ' p8' : '') + (n.id === curSel ? ' sel' : ''), 'data-id': n.id,
        title: n.title + (n.authors ? ' — ' + n.authors : ''), onclick: () => SWE.state.set({ sel: n.id }) });
      chip.style.borderLeftColor = n.p8 ? 'var(--faint)' : U.corpusStroke(n.corpora[0]);
      if (n.id === curSel) chip.style.outline = '2px solid var(--ink)';
      chip.appendChild(U.el('span', { text: U.shortTitle(n.title, 40) }));
      const yr = stratum === 'LIVING' ? 'living' : (U.yearNum(n) != null ? String(U.yearNum(n)) : (n.year || '—'));
      chip.appendChild(U.el('span', { class: 'yy', text: yr }));
      if (n.p8) chip.appendChild(U.el('span', { class: 'yy p8tag', text: '·p8' }));
      else if (n.verification === 'unverified') chip.appendChild(U.el('span', { class: 'badge unv', text: 'unv' }));
      return chip;
    }
    function elementChip(n, curSel) {
      const chip = U.el('button', { class: 'nodechip el' + (n.id === curSel ? ' sel' : ''), 'data-id': n.id,
        title: n.name + (n.named_in ? ' — ' + n.named_in : ''), onclick: () => SWE.state.set({ sel: n.id }) });
      chip.style.borderLeftColor = n.realm === 'architecture' ? '#6D4AA6' : '#0F6D5B';
      if (n.id === curSel) chip.style.outline = '2px solid var(--ink)';
      chip.appendChild(U.el('span', { text: U.shortTitle(n.name, 40) }));
      chip.appendChild(U.el('span', { class: 'yy', text: n.year != null ? String(n.year) : '—' }));
      if (n.yearSource && n.yearSource !== 'named_in') chip.appendChild(U.el('span', { class: 'yy dsrc', text: n.yearSource === 'earliest_work' ? '≈' : (n.yearSource === 'named_in_corpus_id' ? '·id' : '') }));
      return chip;
    }

    function onSelect(sel) {
      for (const id in chipEls) { const on = id === sel; chipEls[id].classList.toggle('sel', on); chipEls[id].style.outline = on ? '2px solid var(--ink)' : ''; }
    }
    render();
    return { applyFilters: render, onSelect, destroy: () => {} };
  }
  return { label: 'Chronology', mount };
})();
