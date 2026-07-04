// detail.js — node detail drawer: full citation, per-corpus raw tags, edges with provenance.
window.SWE = window.SWE || {};
SWE.detail = (function () {
  'use strict';
  const U = SWE.util;
  let byId = null, inE = null, outE = null, lastFocus = null;
  function index() {
    byId = {}; inE = {}; outE = {};
    SWE.corpus.nodes.forEach(n => { byId[n.id] = n; });
    SWE.relations.edges.forEach(e => {
      (outE[e.s] = outE[e.s] || []).push(e);
      (inE[e.t] = inE[e.t] || []).push(e);
    });
  }
  function kindChip(kind) {
    return U.el('span', { class: 'kt', text: kind });
  }
  function provBadge(src) {
    if (src === 'editorial') return U.el('span', { class: 'badge edi', text: 'EDITORIAL' });
    return U.el('span', { class: 'badge surv', text: src });
  }
  function edgeRow(e, dir) {
    const other = byId[dir === 'out' ? e.t : e.s];
    const row = U.el('div', { class: 'edge' });
    row.appendChild(kindChip(dir === 'out' ? e.kind : 'is ' + e.kind + ' of'));
    row.appendChild(U.el('span', { class: 'lnk', text: other ? other.title : '?', tabindex: '0',
      onclick: () => show(other.id),
      onkeydown: ev => { if (ev.key === 'Enter') show(other.id); } }));
    row.appendChild(provBadge(e.src));
    if (e.cycle) row.appendChild(U.el('span', { class: 'badge unv', text: 'cycle ' + e.cycle }));
    if (e.note) row.appendChild(U.el('div', { class: 'ov', text: e.note }));
    return row;
  }
  function show(id) {
    if (!byId) index();
    const n = byId[id]; if (!n) return;
    lastFocus = document.activeElement;
    SWE.state.set({ sel: id });
    const d = document.getElementById('drawer');
    d.innerHTML = '';
    d.appendChild(U.el('button', { class: 'close', text: 'Esc ✕', 'aria-label': 'Close detail',
      onclick: hide }));
    d.appendChild(U.el('h2', { text: n.title }));
    const cite = U.el('p', { class: 'cite' });
    cite.appendChild(U.el('span', { text: n.authors + ' · ' }));
    cite.appendChild(U.el('b', { text: n.year }));
    if (n.ident) cite.appendChild(U.el('span', { text: ' · ' + n.ident }));
    d.appendChild(cite);
    const bl = U.el('div'); U.badges(n).forEach(b => bl.appendChild(b));
    (n.role || []).filter(r => r === 'core' || r === 'advanced')
      .forEach(r => bl.appendChild(U.el('span', { class: 'badge surv', text: r })));
    if (n.lane) bl.appendChild(U.el('span', { class: 'badge surv', text: 'lane: ' + n.lane }));
    if (n.access) bl.appendChild(U.el('span', { class: 'badge ' + (n.access === 'open' ? 'ver' : 'surv'), text: 'oa: ' + n.access }));
    d.appendChild(bl);
    if (n.note) d.appendChild(U.el('p', { class: 'cite', text: n.note }));
    d.appendChild(U.el('div', { class: 'sec', text: 'corpora (memberships)' }));
    const cw = U.el('div'); U.corpusChips(n).forEach(c => cw.appendChild(c)); d.appendChild(cw);
    d.appendChild(U.el('div', { class: 'sec', text: 'reconciled tags (phase 2)' }));
    const dl = U.el('dl');
    const add = (k, v) => { if (v && v.length) { dl.appendChild(U.el('dt', { text: k })); dl.appendChild(U.el('dd', { text: Array.isArray(v) ? v.join(', ') : v })); } };
    add('type', n.type); add('branches', n.branches); add('themes', n.themes);
    add('scope', n.scope); d.appendChild(dl);
    d.appendChild(U.el('div', { class: 'sec', text: 'raw tags as each report stated them' }));
    const dl2 = U.el('dl');
    for (const c in n.per) {
      dl2.appendChild(U.el('dt', { text: U.CORPUS_SHORT[c] }));
      dl2.appendChild(U.el('dd', { text: JSON.stringify(n.per[c]) }));
    }
    d.appendChild(dl2);
    const outs = outE[id] || [], ins = inE[id] || [];
    d.appendChild(U.el('div', { class: 'sec', text: 'relates to (' + outs.length + ')' }));
    outs.length ? outs.forEach(e2 => d.appendChild(edgeRow(e2, 'out')))
                : d.appendChild(U.el('p', { class: 'ov cite', text: 'no outgoing relations' }));
    d.appendChild(U.el('div', { class: 'sec', text: 'related from (' + ins.length + ')' }));
    ins.length ? ins.forEach(e2 => d.appendChild(edgeRow(e2, 'in')))
               : d.appendChild(U.el('p', { class: 'ov cite', text: 'no incoming relations' }));
    d.hidden = false;
    d.querySelector('.close').focus();
  }
  function hide() {
    const d = document.getElementById('drawer');
    d.hidden = true;
    SWE.state.set({ sel: null });
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }
  return { show, hide, isOpen: () => !document.getElementById('drawer').hidden };
})();
