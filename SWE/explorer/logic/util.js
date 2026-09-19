// util.js — DOM/SVG helpers, runtime-contract primitives, and the corpus/kind presentation maps.
// No data, no view logic. Colours live in tokens.css; JS only names the CSS variables.
window.SWE = window.SWE || {};
SWE.util = (function () {
  'use strict';
  const SVGNS = 'http://www.w3.org/2000/svg';

  class InvariantError extends Error { constructor(m) { super(m); this.name = 'InvariantError'; } }
  /** Enforcement = an explicit throw; console.assert never throws (error manifest §9).
   * @param {unknown} cond @param {string} msg @returns {asserts cond} */
  function invariant(cond, msg) { if (!cond) throw new InvariantError(msg); }
  /** @param {never} x @returns {never} */
  function assertNever(x) { throw new InvariantError('unreachable: ' + JSON.stringify(x)); }

  function el(tag, attrs, ...kids) {
    const n = document.createElement(tag);
    if (attrs) for (const k in attrs) {
      if (attrs[k] == null) continue;
      if (k === 'class') n.className = attrs[k];
      else if (k === 'text') n.textContent = attrs[k];
      else if (k === 'html') n.innerHTML = attrs[k];        // only ever fed literal strings here
      else if (k.startsWith('on') && typeof attrs[k] === 'function') n.addEventListener(k.slice(2), attrs[k]);
      else n.setAttribute(k, attrs[k]);
    }
    for (const c of kids) if (c != null) n.appendChild(typeof c === 'string' ? document.createTextNode(c) : c);
    return n;
  }
  function svg(tag, attrs, ...kids) {
    const n = document.createElementNS(SVGNS, tag);
    if (attrs) for (const k in attrs) if (attrs[k] != null) n.setAttribute(k, String(attrs[k]));
    for (const c of kids) if (c != null) n.appendChild(c);
    return n;
  }

  const CORPUS_ORDER = ['swa-science', 'emb-arch', 'emb-c', 'emb-cpp', 'emb-ops', 'simulink', 'swe-process', 'arch-spine'];
  const CORPUS_CLS = { 'swa-science': 'cc-swa', 'emb-arch': 'cc-arch', 'emb-c': 'cc-c', 'emb-cpp': 'cc-cpp', 'emb-ops': 'cc-ops', 'simulink': 'cc-sim', 'swe-process': 'cc-proc', 'arch-spine': 'cc-spine' };
  const CORPUS_SHORT = { 'swa-science': 'swa', 'emb-arch': 'arch', 'emb-c': 'c', 'emb-cpp': 'c++', 'emb-ops': 'ops', 'simulink': 'simulink', 'swe-process': 'proc', 'arch-spine': 'spine' };
  const CORPUS_KEY = { 'swa-science': 'swa', 'emb-arch': 'arch', 'emb-c': 'c', 'emb-cpp': 'cpp', 'emb-ops': 'ops', 'simulink': 'sim', 'swe-process': 'proc', 'arch-spine': 'spine' };
  const corpusFill = (c) => `var(--c-${CORPUS_KEY[c]}-bg)`;
  const corpusStroke = (c) => `var(--c-${CORPUS_KEY[c]})`;
  const kindColor = (k) => `var(--k-${k})`;
  const KIND_DASH = { 'surveys': '2 4', 'companion': '6 4', 'critiques': '7 4', 'part-of': '1 3' };

  /** Leading 4-digit year; null for living/unparseable. @param {{year:string}} n */
  function yearNum(n) {
    if (n.year === 'living') return null;
    const m = /(\d{4})/.exec(n.year || '');
    return m ? +m[1] : null;
  }
  function shortTitle(t, max) { t = String(t); return t.length > max ? t.slice(0, max - 1) + '…' : t; }

  /** Greedy word-wrap into ≤maxLines of ~budget chars; final line ellipsised. */
  function wrapLabel(name, budget, maxLines) {
    const words = String(name).split(/\s+/); const lines = []; let cur = '';
    for (const w of words) {
      const cand = cur ? cur + ' ' + w : w;
      if (cand.length > budget && cur) { lines.push(cur); cur = w; if (lines.length === maxLines - 1) break; }
      else cur = cand;
    }
    if (cur && lines.length < maxLines) lines.push(cur);
    const used = lines.join(' ').length;
    if (lines.length && used < String(name).length) {
      let tail = lines[lines.length - 1];
      lines[lines.length - 1] = tail.length > budget ? tail.slice(0, budget - 1) + '…' : tail + '…';
    }
    return lines.length ? lines : [String(name)];
  }

  function corpusChips(node) {
    return node.corpora.map((c) => el('span', { class: 'chip ' + CORPUS_CLS[c], title: c,
      text: CORPUS_SHORT[c] + (node.per && node.per[c] && node.per[c].lead ? ' (lead)' : '') }));
  }
  /** Honesty badges — verification, UNRESOLVED, anchor, survey, automotive. */
  function badges(node) {
    const out = [];
    out.push(el('span', { class: 'badge ' + (node.verification === 'verified' ? 'ver' : 'unv'), text: node.verification }));
    if (node.unresolved && node.unresolved.length) out.push(el('span', { class: 'badge unres', text: 'UNRESOLVED: ' + node.unresolved.join(', ') }));
    if ((node.role || []).includes('anchor')) out.push(el('span', { class: 'badge anch', text: '★ anchor' }));
    if ((node.role || []).includes('survey')) out.push(el('span', { class: 'badge surv', text: '¶ survey' }));
    if (node.automotive) out.push(el('span', { class: 'badge auto', text: '◆ automotive' }));
    return out;
  }

  // ── element layer (design + architecture realms) ──
  const REALM_CLS = { design: 're-design', architecture: 're-arch' };
  const REALM_SHORT = { design: 'design', architecture: 'arch' };
  const EL_KIND_DASH = { 'specializes': '', 'composes-with': '6 4', 'alternative-to': '2 4', 'implements': '1 3' };
  /** realm chip + kind chip for an element node. */
  function elChips(n) {
    return [
      el('span', { class: 'chip ' + (REALM_CLS[n.realm] || ''), title: 'realm: ' + n.realm, text: REALM_SHORT[n.realm] || n.realm }),
      el('span', { class: 'chip', text: n.kind }),
    ];
  }
  /** honesty badges for an element: confidence, borderline, quality-attribute tags. */
  function elBadges(n) {
    const out = [];
    out.push(el('span', { class: 'badge ' + (n.confidence === 'established' ? 'ver' : 'surv'), text: n.confidence }));
    if (n.borderline) out.push(el('span', { class: 'badge unres', text: '~ borderline' }));
    for (const q of (n.qa || [])) out.push(el('span', { class: 'badge auto', text: 'qa: ' + q }));
    return out;
  }

  return { SVGNS, InvariantError, invariant, assertNever, el, svg,
           CORPUS_ORDER, CORPUS_CLS, CORPUS_SHORT, CORPUS_KEY, corpusFill, corpusStroke,
           kindColor, KIND_DASH, yearNum, shortTitle, wrapLabel, corpusChips, badges,
           REALM_CLS, REALM_SHORT, EL_KIND_DASH, elChips, elBadges };
})();
