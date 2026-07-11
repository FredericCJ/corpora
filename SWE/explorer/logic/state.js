// state.js — single shared state + pub/sub + URL-hash (de)serialization. No DOM, no data.
// One mutation entry point (`set`); unidirectional flow: event -> set -> notify -> render. The
// DOM is never read back as a source of truth. Full state round-trips through location.hash, so
// any screen (view + filters + selection) is a shareable URL even on file://.
window.SWE = window.SWE || {};
SWE.state = (function () {
  'use strict';
  /**
   * @typedef {object} State
   * @property {string} view 'graph'|'facets'|'timeline'|'overlap'|'anchors'|'el-*'
   * @property {string} q @property {string} ver @property {string} corpus @property {string|null} sel
   * @property {string} atlas atlas mode for the atlas view (''→archipelago)
   * @property {string} island focused island id at atlas L1 ('' → L0)
   * @property {string} tlmode Chronology mode ('' | 'bok' → literature; 'elements' → element years)
   */
  const KEYS = ['view', 'q', 'ver', 'corpus', 'sel', 'atlas', 'island', 'tlmode'];
  /** @type {State} */
  const s = { view: 'graph', q: '', ver: '', corpus: '', sel: null, atlas: '', island: '', tlmode: '' };
  /** @type {Array<(s:State,changed:string[])=>void>} */
  const subs = [];

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
    location.hash = toHash();       // self-write; the hashchange it triggers re-parses to the same state → no-op
    emit(changed);
  }
  // hashchange fires ASYNCHRONOUSLY (after set() returns), so a mute-flag cannot span the gap — it would be
  // reset before the event runs, and every set() would re-emit ALL keys (remounting the active view). Instead
  // the handler diffs the parsed hash against current state: a self-write emits nothing; a genuine back/forward
  // navigation emits only the keys that actually changed.
  window.addEventListener('hashchange', () => {
    const before = {}; for (const k of KEYS) before[k] = s[k];
    fromHash();
    const changed = KEYS.filter((k) => s[k] !== before[k]);
    if (changed.length) emit(changed);
  });
  fromHash();
  return { get: () => s, set, on: (fn) => subs.push(fn), KEYS };
})();
