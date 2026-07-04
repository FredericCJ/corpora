// state.js — single shared state + pub/sub + URL-hash (de)serialization. No DOM, no data.
// One mutation entry point (`set`); state emits; views subscribe. Unidirectional flow:
// event -> set(patch) -> notify -> render. The DOM is never read back as a source of truth
// (web_architecture_manifest §3.1). Full state round-trips through location.hash so any screen
// is shareable even on file://.
window.DS = window.DS || {};
DS.state = (function () {
  'use strict';
  /**
   * @typedef {object} State
   * @property {string} q       search query
   * @property {string} family  family filter ('' = all)
   * @property {string} ver     verification filter ('' | 'verified' | 'flagged')
   * @property {string} kind    relation-kind filter ('' = all)
   * @property {string|null} sel selected node id
   */
  const KEYS = ['q', 'family', 'ver', 'kind', 'sel'];
  /** @type {State} */
  const s = { q: '', family: '', ver: '', kind: '', sel: null };
  /** @type {Array<(s:State,changed:string[])=>void>} */
  const subs = [];
  let muted = false;

  function toHash() {
    const p = new URLSearchParams();
    for (const k of KEYS) if (s[k]) p.set(k, s[k]);
    const q = p.toString();
    return q ? '#' + q : '#';
  }
  function fromHash() {
    const p = new URLSearchParams(location.hash.slice(1));
    for (const k of KEYS) s[k] = p.has(k) ? p.get(k) : (k === 'sel' ? null : '');
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

  window.addEventListener('hashchange', () => {
    if (muted) return;
    fromHash(); emit(KEYS.slice());
  });
  fromHash();

  return { get: () => s, set, on: (fn) => subs.push(fn), KEYS };
})();
