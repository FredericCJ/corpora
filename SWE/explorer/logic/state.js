// state.js — single shared state + pub/sub + hash (de)serialization. No DOM, no data.
window.SWE = window.SWE || {};
SWE.state = (function () {
  'use strict';
  const s = { view: 'graph', q: '', ver: '', corpus: '', sel: null };
  const subs = [];
  let muted = false;
  function toHash() {
    const p = new URLSearchParams();
    for (const k of ['view', 'q', 'ver', 'corpus', 'sel']) if (s[k]) p.set(k, s[k]);
    return '#' + p.toString();
  }
  function fromHash() {
    const p = new URLSearchParams(location.hash.slice(1));
    for (const k of ['view', 'q', 'ver', 'corpus', 'sel']) if (p.has(k)) s[k] = p.get(k);
  }
  function emit(changed) { subs.forEach(fn => fn(s, changed)); }
  function set(patch) {
    const changed = [];
    for (const k in patch) if (s[k] !== patch[k]) { s[k] = patch[k]; changed.push(k); }
    if (!changed.length) return;
    muted = true; location.hash = toHash(); muted = false;
    emit(changed);
  }
  window.addEventListener('hashchange', () => {
    if (muted) return;
    fromHash(); emit(['view', 'q', 'ver', 'corpus', 'sel']);
  });
  fromHash();
  return { get: () => s, set, on: fn => subs.push(fn) };
})();
