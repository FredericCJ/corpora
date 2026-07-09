// state.js — single shared state + pub/sub + URL-hash (de)serialization. No DOM, no data.
// One mutation entry point (`set`); unidirectional flow: event -> set -> notify -> render. The
// DOM is never read back as a source of truth. Full state round-trips through location.hash, so
// any screen (view + filters + selection) is a shareable URL even on file://.
window.NET = window.NET || {};
NET.state = (function () {
  'use strict';
  /**
   * @typedef {object} State
   * @property {string} view 'anchor'|'facets'|'timeline'|'matlab'|'triage'
   * @property {string} q @property {string} ver @property {string} corpus @property {string|null} sel
   */
  const KEYS = ['view', 'q', 'ver', 'corpus', 'sel'];
  /** @type {State} */
  const s = { view: 'anchor', q: '', ver: '', corpus: '', sel: null };
  /** @type {Array<(s:State,changed:string[])=>void>} */
  const subs = [];

  function toHash() {
    const p = new URLSearchParams();
    for (const k of KEYS) if (s[k]) p.set(k, s[k]);
    const q = p.toString(); return q ? '#' + q : '#';
  }
  function fromHash() {
    const p = new URLSearchParams(location.hash.slice(1));
    for (const k of KEYS) s[k] = p.has(k) ? p.get(k) : (k === 'sel' ? null : (k === 'view' ? 'anchor' : ''));
  }
  function emit(changed) { for (const fn of subs) fn(s, changed); }

  /** @param {Partial<State>} patch */
  function set(patch) {
    const changed = [];
    for (const k in patch) if (s[k] !== patch[k]) { s[k] = patch[k]; changed.push(k); }
    if (!changed.length) return;
    location.hash = toHash();
    emit(changed);
  }
  // hashchange fires ASYNCHRONOUSLY even for our own programmatic writes (a mute flag reset
  // synchronously cannot suppress it). A self-echo is recognised by value instead: if the hash
  // already serialises the current state, there is nothing to apply — only genuinely external
  // navigation (back/forward, hand-edited URL) re-enters through fromHash.
  window.addEventListener('hashchange', () => {
    if ((location.hash || '#') === toHash()) return;
    fromHash(); emit(KEYS.slice());
  });
  fromHash();
  return { get: () => s, set, on: (fn) => subs.push(fn), KEYS };
})();
