// util.js — DOM/SVG helpers, runtime-contract primitives, and the tier/evidence presentation
// maps. No data, no view logic. Colours live in tokens.css; JS only names the CSS variables.
window.CALC = window.CALC || {};
CALC.util = (function () {
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

  const TIER_IDS = [0, 1, 2, 3, 4, 5, 6, 7, 8];
  const tierFill = (t) => `var(--t${t}-bg)`;
  const tierStroke = (t) => `var(--t${t})`;
  const evStroke = (tag) => tag === 'JUDGMENT' ? 'var(--jd)' : 'var(--ev)';
  const RIGORS = ['computational', 'mixed', 'mixed→proof', 'proof-based'];
  const FLAG_MARK = { source: '● source', sink: '■ sink', 'sink-adjacent': '◪ sink-adjacent',
    'terminal-leaf': '◇ terminal leaf', supporting: '＋ supporting' };

  /** Leading 4-digit year; null when unparseable. @param {{year:string}} n */
  function yearNum(n) { const m = /(\d{4})/.exec(n.year || ''); return m ? +m[1] : null; }
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

  /** Tier chip with the tier's hue. @param {number} t @param {string} [label] */
  function tierChip(t, label) {
    const c = el('span', { class: 'tchip', text: label || ('T' + t) });
    c.style.color = tierStroke(t); c.style.borderColor = tierStroke(t); c.style.background = tierFill(t);
    return c;
  }
  /** Node id chip coloured by the node's tier (used in path rows). @param {{id:string,tier:number,title:string}} n */
  function idChip(n, onclick) {
    const c = el('button', { class: 'pchip', text: n.id, title: n.title + ' — ' + n.authors + ' (' + n.year + ')',
      onclick });
    c.style.color = tierStroke(n.tier); c.style.borderColor = tierStroke(n.tier); c.style.background = tierFill(n.tier);
    return c;
  }
  /** Honesty badges — verification, kept/dropped, structural flags, open access. */
  function badges(node) {
    const out = [];
    out.push(el('span', { class: 'badge ver', text: node.verification }));
    out.push(el('span', { class: 'badge ' + node.status, text: node.status }));
    for (const f of node.flags || []) out.push(el('span', { class: 'badge flag', text: FLAG_MARK[f] || f }));
    if (node.access === 'open') out.push(el('span', { class: 'badge oa', text: 'open access' }));
    return out;
  }
  /** Evidence badge for an edge tag. @param {string} tag */
  function evBadge(tag) { return el('span', { class: 'badge ' + (tag === 'JUDGMENT' ? 'jd' : 'ev'), text: tag }); }

  return { SVGNS, InvariantError, invariant, assertNever, el, svg,
           TIER_IDS, tierFill, tierStroke, evStroke, RIGORS, FLAG_MARK,
           yearNum, shortTitle, wrapLabel, tierChip, idChip, badges, evBadge };
})();
