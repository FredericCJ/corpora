// util.js — DOM helpers, runtime-contract primitives, and the subfield/paradigm/verification
// presentation maps. No data, no view logic. Colours live in tokens.css; JS names CSS variables.
window.NET = window.NET || {};
NET.util = (function () {
  'use strict';

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
  const SVGNS = 'http://www.w3.org/2000/svg';
  function svg(tag, attrs, ...kids) {
    const n = document.createElementNS(SVGNS, tag);
    if (attrs) for (const k in attrs) if (attrs[k] != null) n.setAttribute(k, String(attrs[k]));
    for (const c of kids) if (c != null) n.appendChild(c);
    return n;
  }

  const SUBF_KEY = { 'protocols-services': 'ps', 'performance-evaluation': 'pe', 'modeling-approaches': 'ma',
    'simulation-methodology': 'sm', 'next-gen-wireless': 'ngw', 'security': 'sec', 'digital-twin': 'dt',
    'ml-for-simulation': 'ml', 'cloud-datacenter': 'cd', 'sdn-nfv-p4': 'sdn',
    'parallel-distributed-sim': 'pads', 'emulation-tooling': 'emu' };
  const PAR_KEY = { 'discrete-event': 'de', 'wireless-system-level': 'wsl', 'link-phy-level': 'phy',
    'analytical-control-fluid': 'acf', 'co-simulation-interop': 'csi', 'academic-simulators': 'acad' };
  const subfStroke = (s) => `var(--s-${SUBF_KEY[s] || 'oth'})`;
  const subfFill = (s) => `var(--s-${SUBF_KEY[s] || 'oth'}-bg)`;
  const parStroke = (p) => `var(--p-${PAR_KEY[p] || 'de'})`;
  const parFill = (p) => `var(--p-${PAR_KEY[p] || 'de'}-bg)`;
  /** A node's hue: GEN nodes by first subfield, MAT-only nodes by first paradigm. */
  const hueStroke = (n) => n.subfield.length ? subfStroke(n.subfield[0])
    : (n.paradigm.length ? parStroke(n.paradigm[0]) : 'var(--s-oth)');
  const hueFill = (n) => n.subfield.length ? subfFill(n.subfield[0])
    : (n.paradigm.length ? parFill(n.paradigm[0]) : 'var(--s-oth-bg)');

  const VER_CLS = { 'verified-web': 'web', 'verified-train': 'train', 'unverified': 'unv' };
  const VER_SHORT = { 'verified-web': 'verified[WEB]', 'verified-train': 'verified[TRAIN]', 'unverified': 'unverified' };

  function shortTitle(t, max) { t = String(t); return t.length > max ? t.slice(0, max - 1) + '…' : t; }

  /** Greedy word-wrap into ≤maxLines of ~budget chars; final line ellipsised. */
  function wrapText(text, budget, maxLines) {
    const words = String(text).split(/\s+/); const lines = []; let cur = '';
    for (const w of words) {
      const cand = cur ? cur + ' ' + w : w;
      if (cand.length > budget && cur) { lines.push(cur); cur = w; if (lines.length === maxLines - 1) break; }
      else cur = cand;
    }
    if (cur && lines.length < maxLines) lines.push(cur);
    const used = lines.join(' ').length;
    if (lines.length && used < String(text).length) {
      let tail = lines[lines.length - 1];
      lines[lines.length - 1] = tail.length > budget ? tail.slice(0, budget - 1) + '…' : tail + '…';
    }
    return lines.length ? lines : [String(text)];
  }

  /** Corpus membership chips with the entry's per-report item number. */
  function corpusChips(node) {
    return node.corpus.map((c) => {
      const chip = el('span', { class: 'tchip', text: c + ' · ' + (node.item[c] === 'anchor' ? 'anchor' : 'item ' + node.item[c]) });
      chip.style.color = `var(--c-${c})`; chip.style.borderColor = `var(--c-${c})`; chip.style.background = `var(--c-${c}-bg)`;
      return chip;
    });
  }
  /** Honesty badges — verification (with qualifier), quarantine, living, recency. */
  function badges(node) {
    const out = [];
    out.push(el('span', { class: 'badge ' + VER_CLS[node.verification], text: node.verRaw }));
    if (node.quarantined) out.push(el('span', { class: 'badge quar', text: 'QUARANTINED' }));
    if (node.living) out.push(el('span', { class: 'badge liv', text: 'living' }));
    out.push(el('span', { class: 'badge plain', text: node.recencyRaw }));
    return out;
  }
  /** Small id chip coloured by the node's hue. */
  function idChip(node, onclick) {
    const c = el('button', { class: 'idchip' + (node.quarantined ? ' quar' : ''), 'data-id': node.id,
      text: node.item[node.corpus[0]] === 'anchor' ? '★' : node.item[node.corpus[0]],
      title: node.title + ' — ' + node.cite.slice(0, 90), onclick });
    c.style.color = hueStroke(node); c.style.borderColor = hueStroke(node); c.style.background = hueFill(node);
    return c;
  }

  return { InvariantError, invariant, assertNever, el, svg,
           SUBF_KEY, PAR_KEY, subfStroke, subfFill, parStroke, parFill, hueStroke, hueFill,
           VER_CLS, VER_SHORT, shortTitle, wrapText, corpusChips, badges, idChip };
})();
