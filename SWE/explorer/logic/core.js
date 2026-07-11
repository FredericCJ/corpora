// core.js — FUNCTIONAL CORE (web_architecture_manifest §4 / F1). Every model computation lives
// here as a pure function of (data, state): the visible set, the graph layout + cycle-safe
// closure, facet counts, chronology strata, the overlap matrix, and per-corpus anchors. No DOM,
// no globals mutated — this is the unit-testable half; the view shells only project it.
window.SWE = window.SWE || {};
SWE.core = (function () {
  'use strict';
  const U = SWE.util;

  // ── search / visible set ────────────────────────────────────────────────────────────
  /** @type {Record<string,string>|null} */ let hay = null;
  function buildIndex(corpus) {
    hay = {};
    for (const n of corpus.nodes)
      hay[n.id] = (n.title + ' ' + n.authors + ' ' + n.id + ' ' + (n.ident || '')).toLowerCase();
  }
  /** @returns {Set<string>} ids passing search + verification + corpus filters. Pure. */
  function visibleIds(corpus, state) {
    if (!hay) buildIndex(corpus);
    const q = (state.q || '').trim().toLowerCase();
    const out = new Set();
    for (const n of corpus.nodes) {
      if (state.ver && n.verification !== state.ver) continue;
      if (state.corpus && !n.corpora.includes(state.corpus)) continue;
      if (q && !hay[n.id].includes(q)) continue;
      out.add(n.id);
    }
    return out;
  }

  // ── graph: adjacency, cycle-safe closure, aspect-fitted band layout ───────────────────
  function adjacency(edges) {
    const up = {}, down = {};
    for (const e of edges) { (down[e.s] = down[e.s] || []).push(e.t); (up[e.t] = up[e.t] || []).push(e.s); }
    return { up, down };
  }
  function closure(id, adj) {
    const seen = new Set([id]), st = [id];
    while (st.length) { const c = st.pop(); for (const x of adj[c] || []) if (!seen.has(x)) { seen.add(x); st.push(x); } }
    return seen;
  }

  const NW = 162, NH = 52, GX = 16, GY = 12, PADX = 10, PADY = 8, LABELH = 28, BANDGAP = 40, SHELFGAP = 50, MARGIN = 26;
  const clamp = (v, lo, hi) => Math.max(lo, Math.min(hi, v));
  const primaryCorpus = (n, order) => { for (const c of order) if (n.corpora.includes(c)) return c; return n.corpora[0]; };

  function bandGrid(key, list) {
    const ncols = clamp(Math.round(Math.sqrt(list.length * 0.9)), 2, 7);
    const rows = Math.ceil(list.length / ncols);
    return { key, list, ncols, rows, w: ncols * (NW + GX) - GX + 2 * PADX, h: rows * (NH + GY) - GY + LABELH + 2 * PADY };
  }
  function pack(bands, targetW) {
    let x = 0, y = 0, shelfH = 0, maxW = 0; const placed = [];
    for (const b of bands) {
      if (x > 0 && x + BANDGAP + b.w > targetW) { y += shelfH + SHELFGAP; x = 0; shelfH = 0; }
      const bx = x === 0 ? 0 : x + BANDGAP;
      placed.push({ band: b, x: bx, y }); x = bx + b.w; shelfH = Math.max(shelfH, b.h); maxW = Math.max(maxW, x);
    }
    return { placed, W: maxW, H: y + shelfH };
  }
  /** Shelf-pack corpus bands to best match opts.aspect so the SVG fills its pane. Pure.
   * @returns {{positions:Record<string,{x:number,y:number}>,bands:any[],width:number,height:number,box:{NW:number,NH:number}}} */
  function graphLayout(nodes, edges, corpusOrder, opts) {
    const target = (opts && opts.aspect) || 1.4;
    const inGraph = new Set(); for (const e of edges) { inGraph.add(e.s); inGraph.add(e.t); }
    const drawn = nodes.filter((n) => inGraph.has(n.id));
    const byBand = {};
    for (const n of drawn) { const c = primaryCorpus(n, corpusOrder); (byBand[c] = byBand[c] || []).push(n); }
    const bands = [];
    for (const c of corpusOrder) {
      const list = byBand[c]; if (!list || !list.length) continue;
      list.sort((a, b) => ((a.themes && a.themes[0] || '') + '').localeCompare(b.themes && b.themes[0] || '') ||
        ((U.yearNum(a) || 9999) - (U.yearNum(b) || 9999)) || a.title.localeCompare(b.title));
      bands.push(bandGrid(c, list));
    }
    const widths = bands.map((b) => b.w);
    const minT = Math.max.apply(null, widths), maxT = widths.reduce((a, b) => a + b, 0) + BANDGAP * (bands.length - 1);
    let best = null;
    for (let i = 0; i <= 28; i++) {
      const t = minT + (maxT - minT) * (i / 28), packed = pack(bands, t);
      const score = Math.abs(packed.W / packed.H - target);
      if (!best || score < best.score) best = Object.assign({ score }, packed);
    }
    const positions = {}, outBands = [];
    for (const p of best.placed) {
      const b = p.band, bx = p.x + MARGIN, by = p.y + MARGIN;
      outBands.push({ key: b.key, x: bx, y: by, w: b.w, h: b.h, count: b.list.length, labelX: bx + PADX, labelY: by + PADY + 14 });
      b.list.forEach((n, i) => { positions[n.id] = { x: bx + PADX + (i % b.ncols) * (NW + GX), y: by + PADY + LABELH + Math.floor(i / b.ncols) * (NH + GY) }; });
    }
    return { positions, bands: outBands, width: best.W + 2 * MARGIN, height: best.H + 2 * MARGIN, box: { NW, NH } };
  }

  // ── facets ────────────────────────────────────────────────────────────────────────
  function valuesOf(n, key) { const v = n[key]; return v == null ? [] : (Array.isArray(v) ? v : [v]); }
  function passLocal(n, localSel, exceptKey) {
    for (const k in localSel) { if (!localSel[k] || k === exceptKey) continue; if (!valuesOf(n, k).includes(localSel[k])) return false; }
    return true;
  }
  /** @returns {Map<string,number>} value -> count for one facet, honouring the other selections. */
  function facetCount(nodes, key, localSel) {
    const m = new Map();
    for (const n of nodes) if (passLocal(n, localSel, key)) for (const v of valuesOf(n, key)) m.set(v, (m.get(v) || 0) + 1);
    return m;
  }

  // ── chronology ──────────────────────────────────────────────────────────────────────
  const STRATA = ['≤ 1979', '1980s', '1990s', '2000s', '2010s', '2020s', 'LIVING', 'UNRESOLVED'];
  function stratumOf(n) {
    if (n.year === 'living') return 'LIVING';
    const y = U.yearNum(n); if (y == null) return 'UNRESOLVED';
    return y < 1980 ? '≤ 1979' : (Math.floor(y / 10) * 10 + 's');
  }
  function strataBuckets(nodes) {
    const b = {}; for (const n of nodes) (b[stratumOf(n)] = b[stratumOf(n)] || []).push(n);
    for (const s in b) b[s].sort((x, y) => (U.yearNum(x) || 0) - (U.yearNum(y) || 0) || x.title.localeCompare(y.title));
    return b;
  }
  // element chronology (WV3 Elements mode): decade strata over the build-derived element year
  // (`year`/`yearSource`, build_elements.py). No LIVING stratum — an element is dated by when its
  // concept was named, not by document upkeep. UNRESOLVED holds the 89 the waterfall could not date.
  const ELEMENT_STRATA = ['≤ 1979', '1980s', '1990s', '2000s', '2010s', '2020s', 'UNRESOLVED'];
  function elementStratumOf(el) {
    const y = el.year;
    if (typeof y !== 'number' || !y) return 'UNRESOLVED';
    return y < 1980 ? '≤ 1979' : (Math.floor(y / 10) * 10 + 's');
  }
  function elementStrataBuckets(nodes) {
    const b = {}; for (const n of nodes) (b[elementStratumOf(n)] = b[elementStratumOf(n)] || []).push(n);
    for (const s in b) b[s].sort((x, y) => (x.year || 0) - (y.year || 0) || x.name.localeCompare(y.name));
    return b;
  }

  // ── overlap ─────────────────────────────────────────────────────────────────────────
  function overlapPairs(multi) {
    const pair = {};
    for (const n of multi) for (let i = 0; i < n.corpora.length; i++) for (let j = i + 1; j < n.corpora.length; j++) {
      const k = [n.corpora[i], n.corpora[j]].sort().join('|'); pair[k] = (pair[k] || 0) + 1;
    }
    return pair;
  }
  function signatureGroups(multi, order) {
    const g = {};
    for (const n of multi) { const sig = order.filter((c) => n.corpora.includes(c)).join(' + '); (g[sig] = g[sig] || []).push(n); }
    return Object.entries(g).sort((a, b) => b[1].length - a[1].length || b[0].split('+').length - a[0].split('+').length);
  }

  // ── anchors ───────────────────────────────────────────────────────────────────────
  function anchorsFor(nodes, corpus) {
    return nodes.filter((n) => n.corpora.includes(corpus) && (n.role || []).includes('anchor') && n.per[corpus] && !n.per[corpus].lead)
      .sort((a, b) => (U.yearNum(a) || 9999) - (U.yearNum(b) || 9999));
  }

  return { buildIndex, visibleIds, adjacency, closure, graphLayout, NW, NH,
           valuesOf, passLocal, facetCount, STRATA, stratumOf, strataBuckets,
           ELEMENT_STRATA, elementStratumOf, elementStrataBuckets,
           overlapPairs, signatureGroups, anchorsFor, primaryCorpus };
})();
