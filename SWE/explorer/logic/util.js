// util.js — DOM + formatting helpers. No data, no view logic.
window.SWE = window.SWE || {};
SWE.util = (function () {
  'use strict';
  function el(tag, attrs, ...kids) {
    const n = document.createElement(tag);
    if (attrs) for (const k in attrs) {
      if (k === 'class') n.className = attrs[k];
      else if (k === 'text') n.textContent = attrs[k];
      else if (k.startsWith('on')) n.addEventListener(k.slice(2), attrs[k]);
      else n.setAttribute(k, attrs[k]);
    }
    for (const k of kids) if (k != null) n.appendChild(typeof k === 'string' ? document.createTextNode(k) : k);
    return n;
  }
  const CORPUS_CLS = { 'swa-science': 'cc-swa', 'emb-arch': 'cc-arch', 'emb-c': 'cc-c',
                       'emb-cpp': 'cc-cpp', 'emb-ops': 'cc-ops', 'simulink': 'cc-sim' };
  const CORPUS_SHORT = { 'swa-science': 'swa', 'emb-arch': 'arch', 'emb-c': 'c',
                         'emb-cpp': 'c++', 'emb-ops': 'ops', 'simulink': 'simulink' };
  const CORPUS_COLOR = { 'swa-science': 'var(--c-swa)', 'emb-arch': 'var(--c-arch)', 'emb-c': 'var(--c-c)',
                         'emb-cpp': 'var(--c-cpp)', 'emb-ops': 'var(--c-ops)', 'simulink': 'var(--c-sim)' };
  const CORPUS_BG = { 'swa-science': 'var(--c-swa-bg)', 'emb-arch': 'var(--c-arch-bg)', 'emb-c': 'var(--c-c-bg)',
                      'emb-cpp': 'var(--c-cpp-bg)', 'emb-ops': 'var(--c-ops-bg)', 'simulink': 'var(--c-sim-bg)' };
  const KIND_COLOR = { 'prerequisite-of': 'var(--k-pre)', 'refines': 'var(--k-ref)', 'subsumes': 'var(--k-sub)',
                       'formalizes': 'var(--k-for)', 'surveys': 'var(--k-sur)', 'applies-method-of': 'var(--k-app)',
                       'companion': 'var(--k-com)', 'evaluates': 'var(--k-eva)', 'critiques': 'var(--k-cri)',
                       'supersedes': 'var(--k-sup)', 'part-of': 'var(--k-par)', 'references': 'var(--k-refs)' };
  const KIND_DASH = { 'surveys': '2 4', 'companion': '6 4', 'critiques': '7 4', 'part-of': '1 3' };
  function yearNum(n) {
    if (n.year === 'living') return null;
    const m = /(\d{4})/.exec(n.year || '');
    return m ? +m[1] : null;
  }
  function corpusChips(node) {
    return node.corpora.map(c => el('span', { class: 'chip ' + CORPUS_CLS[c], title: c,
      text: CORPUS_SHORT[c] + (node.per[c] && node.per[c].lead ? ' (lead)' : '') }));
  }
  function badges(node) {
    const out = [];
    out.push(el('span', { class: 'badge ' + (node.verification === 'verified' ? 'ver' : 'unv'),
      text: node.verification }));
    if (node.unresolved && node.unresolved.length)
      out.push(el('span', { class: 'badge unres', text: 'UNRESOLVED: ' + node.unresolved.join(', ') }));
    if ((node.role || []).includes('anchor')) out.push(el('span', { class: 'badge anch', text: '★ anchor' }));
    if ((node.role || []).includes('survey')) out.push(el('span', { class: 'badge surv', text: '¶ survey' }));
    if (node.automotive) out.push(el('span', { class: 'badge auto', text: '◆ automotive' }));
    return out;
  }
  function shortTitle(t, max) { return t.length > max ? t.slice(0, max - 1) + '…' : t; }
  return { el, CORPUS_CLS, CORPUS_SHORT, CORPUS_COLOR, CORPUS_BG, KIND_COLOR, KIND_DASH,
           yearNum, corpusChips, badges, shortTitle };
})();
