// state.js — single shared state + pub/sub + URL-hash (de)serialization. No DOM, no data.
// One mutation entry point (`set`); unidirectional flow: event -> set -> notify -> render. The
// DOM is never read back as a source of truth. Full state round-trips through location.hash, so
// any screen (view + filters + selection) is a shareable URL even on file://.
window.CALC = window.CALC || {};
CALC.state = (function () {
  'use strict';
  /**
   * @typedef {object} State
   * @property {string} view 'graph'|'tiers'|'lineage'|'parallel'|'gate'
   * @property {string} q @property {string} rigor @property {string} tier @property {string|null} sel
   */
  const KEYS = ['view', 'q', 'rigor', 'tier', 'sel'];
  /** @type {State} */
  const s = { view: 'graph', q: '', rigor: '', tier: '', sel: null };
  /** @type {Array<(s:State,changed:string[])=>void>} */
  const subs = [];
  let muted = false;

  function toHash() {
    const p = new URLSearchParams();
    for (const k of KEYS) if (s[k]) p.set(k, s[k]);
    const q = p.toString(); return q ? '#' + q : '#';
  }
  function fromHash() {
    const p = new URLSearchParams(location.hash.slice(1));
    for (const k of KEYS) s[k] = p.has(k) ? p.get(k) : (k === 'sel' ? null : (k === 'view' ? 'graph' : ''));
  }
  function emit(changed) { for (const fn of subs) fn(s, changed); }

  /** @param {Partial<State>} patch */
  function set(patch) {
    const changed = [];
    for (const k in patch) if (s[k] !== patch[k]) { s[k] = patch[k]; changed.push(k); }
    if (!changed.length) return;
    muted = true; location.hash = toHash(); muted = false;
    emit(changed);
  }
  window.addEventListener('hashchange', () => { if (muted) return; fromHash(); emit(KEYS.slice()); });
  fromHash();
  return { get: () => s, set, on: (fn) => subs.push(fn), KEYS };
})();
