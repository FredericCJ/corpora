// core.js — FUNCTIONAL CORE (web_architecture_manifest §4 / F1). Every model computation lives
// here as a pure function of (data, state): the visible set, facet counts, chronology strata,
// anchor-map assembly, paradigm buckets, triage split, and overview stats. No DOM, no globals
// mutated — the unit-testable half; the view shells only project it.
window.NET = window.NET || {};
NET.core = (function () {
  'use strict';

  // ── search / visible set ────────────────────────────────────────────────────────────
  /** @type {Record<string,string>|null} */ let hay = null;
  function buildIndex(corpus) {
    hay = {};
    for (const n of corpus.nodes)
      hay[n.id] = (n.id + ' ' + Object.values(n.item).join(' ') + ' ' + n.title + ' ' + n.cite).toLowerCase();
  }
  /** @returns {Set<string>} ids passing search + verification + corpus filters. Pure. */
  function visibleIds(corpus, state) {
    if (!hay) buildIndex(corpus);
    const q = (state.q || '').trim().toLowerCase();
    const out = new Set();
    for (const n of corpus.nodes) {
      if (state.ver && n.verification !== state.ver) continue;
      if (state.corpus && !n.corpus.includes(state.corpus)) continue;
      if (q && !hay[n.id].includes(q)) continue;
      out.add(n.id);
    }
    return out;
  }

  // ── facets (SWE fashion: counts honour the other local selections) ───────────────────
  function valuesOf(n, key) {
    const v = n[key];
    return v == null ? [] : (Array.isArray(v) ? v : [v]);
  }
  function passLocal(n, localSel, exceptKey) {
    for (const k in localSel) {
      if (!localSel[k] || k === exceptKey) continue;
      if (!valuesOf(n, k).includes(localSel[k])) return false;
    }
    return true;
  }
  /** @returns {Map<string,number>} value -> count for one facet. */
  function facetCount(nodes, key, localSel) {
    const m = new Map();
    for (const n of nodes) if (passLocal(n, localSel, key)) for (const v of valuesOf(n, key)) m.set(v, (m.get(v) || 0) + 1);
    return m;
  }

  // ── chronology strata around the 2015 anchor datum ────────────────────────────────────
  const STRATA = ['≤ 1989', '1990s', '2000s', '2010–2014', '2015 · anchor', '2016–2020', '2021–2026', 'LIVING', 'UNDATED'];
  function stratumOf(n) {
    if (n.living) return 'LIVING';
    const y = n.year;
    if (y == null) return 'UNDATED';
    if (y <= 1989) return '≤ 1989';
    if (y <= 1999) return '1990s';
    if (y <= 2009) return '2000s';
    if (y <= 2014) return '2010–2014';
    if (y === 2015) return '2015 · anchor';
    if (y <= 2020) return '2016–2020';
    return '2021–2026';
  }
  function strataBuckets(nodes) {
    const b = {};
    for (const n of nodes) (b[stratumOf(n)] = b[stratumOf(n)] || []).push(n);
    for (const s in b) b[s].sort((x, y) => (x.year || 9999) - (y.year || 9999) || x.title.localeCompare(y.title));
    return b;
  }

  // ── anchor map: parts × sections × member entries (membership only, no inference) ────
  function anchorColumns(corpus, relations) {
    const bySec = {};
    for (const n of corpus.nodes) {
      if (n.corpus.includes('gen') && n.id !== 'anchor')
        (bySec[n.section] = bySec[n.section] || []).push(n);
    }
    const secTitle = {};
    for (const s of corpus.sections.gen) secTitle[s.no] = s.title;
    const partLabel = {};
    for (const p of corpus.anchorParts) partLabel[p.key] = 'Part ' + p.no + ' — ' + p.label;
    partLabel.beyond = 'Beyond the anchor';
    partLabel.meta = 'Meta routes';
    partLabel.quarantine = 'Quarantine';
    return relations.anchorMap.map((col) => ({
      part: col.part, label: partLabel[col.part] || col.part, verdict: col.verdict || null,
      sections: col.sections.map((s) => ({
        no: s.no, relation: s.relation, title: secTitle[s.no] || ('§' + s.no),
        members: (bySec[s.no] || []).slice(),
      })),
    }));
  }

  // ── paradigm buckets (MAT lens) ───────────────────────────────────────────────────────
  function paradigmBuckets(nodes, paradigms) {
    const b = {};
    for (const p of paradigms) b[p] = [];
    for (const n of nodes) {
      if (!n.corpus.includes('mat')) continue;
      for (const p of n.paradigm) if (b[p]) b[p].push(n);
    }
    for (const p in b) b[p].sort((x, y) => x.section - y.section ||
      (parseInt(x.item.mat || x.item.gen, 10) || 999) - (parseInt(y.item.mat || y.item.gen, 10) || 999));
    return b;
  }

  // ── triage split ─────────────────────────────────────────────────────────────────────
  function triage(nodes) {
    const by = { 'verified-web': [], 'verified-train': [], 'unverified': [] };
    const quarantine = { gen: [], mat: [] };
    for (const n of nodes) {
      by[n.verification].push(n);
      if (n.quarantined) quarantine[n.corpus[0]].push(n);
    }
    return { by, quarantine };
  }

  // ── overview stats ───────────────────────────────────────────────────────────────────
  function stats(corpus, relations) {
    const t = triage(corpus.nodes);
    return {
      nodes: corpus.nodes.length,
      gen: corpus.nodes.filter((n) => n.corpus.includes('gen')).length,
      mat: corpus.nodes.filter((n) => n.corpus.includes('mat')).length,
      merged: corpus.nodes.filter((n) => n.corpus.length > 1).length,
      web: t.by['verified-web'].length, train: t.by['verified-train'].length,
      unv: t.by.unverified.length,
      quarantined: t.quarantine.gen.length + t.quarantine.mat.length,
      edges: relations.edges.length, living: corpus.nodes.filter((n) => n.living).length,
    };
  }

  return { buildIndex, visibleIds, valuesOf, passLocal, facetCount,
           STRATA, stratumOf, strataBuckets, anchorColumns, paradigmBuckets, triage, stats };
})();
