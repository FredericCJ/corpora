// util.js — DOM/SVG helpers, runtime-contract primitives, presentation maps. No data, no views.
window.DS = window.DS || {};
DS.util = (function () {
  'use strict';
  const SVGNS = 'http://www.w3.org/2000/svg';

  /** Enforcement = an explicit throw. `console.assert` never throws, so it is never an
   *  enforcement mechanism (js_error_tracing_contract_manifest §9). */
  class InvariantError extends Error {
    constructor(msg) { super(msg); this.name = 'InvariantError'; }
  }
  /** @param {unknown} cond @param {string} msg @returns {asserts cond} */
  function invariant(cond, msg) { if (!cond) throw new InvariantError(msg); }
  /** Compile-time exhaustiveness + runtime backstop. @param {never} x @returns {never} */
  function assertNever(x) { throw new InvariantError('unreachable: ' + JSON.stringify(x)); }

  /** createElement with a tiny attribute/child DSL. */
  function el(tag, attrs, ...kids) {
    const n = document.createElement(tag);
    if (attrs) for (const k in attrs) {
      if (attrs[k] == null) continue;
      if (k === 'class') n.className = attrs[k];
      else if (k === 'text') n.textContent = attrs[k];
      else if (k === 'html') n.innerHTML = attrs[k];         // only ever fed literal strings here
      else if (k.startsWith('on') && typeof attrs[k] === 'function') n.addEventListener(k.slice(2), attrs[k]);
      else n.setAttribute(k, attrs[k]);
    }
    for (const c of kids) if (c != null) n.appendChild(typeof c === 'string' ? document.createTextNode(c) : c);
    return n;
  }
  /** createElementNS('svg') with attributes. */
  function svg(tag, attrs, ...kids) {
    const n = document.createElementNS(SVGNS, tag);
    if (attrs) for (const k in attrs) if (attrs[k] != null) n.setAttribute(k, String(attrs[k]));
    for (const c of kids) if (c != null) n.appendChild(c);
    return n;
  }

  /** Leading 4-digit year for sort/label; null when unknown. @param {{year:number|null}} n */
  function yearNum(n) { return typeof n.year === 'number' ? n.year : null; }

  /** Greedy word-wrap into at most `maxLines` lines of ~`budget` chars; last line ellipsised. */
  function wrapLabel(name, budget, maxLines) {
    const words = String(name).split(/\s+/);
    const lines = []; let cur = '';
    for (const w of words) {
      const cand = cur ? cur + ' ' + w : w;
      if (cand.length > budget && cur) { lines.push(cur); cur = w; if (lines.length === maxLines - 1) break; }
      else cur = cand;
    }
    if (cur && lines.length < maxLines) lines.push(cur);
    // fold any overflow words into the final line
    const used = lines.join(' ').length;
    if (used < String(name).length && lines.length) {
      let tail = lines[lines.length - 1];
      if (tail.length > budget) tail = tail.slice(0, budget - 1) + '…';
      else if (String(name).length > used) tail = tail + '…';
      lines[lines.length - 1] = tail;
    }
    return lines.length ? lines : [String(name)];
  }

  /** Presentation maps — colours live in tokens.css; JS only references the CSS variables. */
  const familyFill = (f) => `var(--f-${f}-bg)`;
  const familyStroke = (f) => `var(--f-${f})`;
  const kindColor = (k) => `var(--k-${k})`;

  const TIER_LABEL = { root: 'foundational root', backfill: 'back-filled root', modern: 'modern' };
  const FLAG_LABEL = {
    'folklore': 'folklore — no origin paper',
    'theory-only': 'theory only — no implementation paper',
    'diffuse-origin': 'diffuse origin — no single foundational paper',
    'reference-not-origin': 'canonical reference, not the origin',
    'origin-not-in-report': 'origin not stated in the source report',
    'ambiguous-date': 'genuinely ambiguous date',
    'ambiguous-name': 'known naming confusion',
    'soft-attribution': 'attribution verified-but-soft',
    'dual-priority': 'independent-invention priority dispute',
    'adt-layer': 'abstract-data-type layer',
    'from-edge': 'referenced only by the edge list',
  };

  return { SVGNS, InvariantError, invariant, assertNever, el, svg, yearNum, wrapLabel,
           familyFill, familyStroke, kindColor, TIER_LABEL, FLAG_LABEL };
})();
