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

  // ── editorial overlays: adjacency + banded barycenter layout ─────────────────────────
  function overlayAdjacency(overlay) {
    const up = {}, down = {};
    for (const e of overlay.edges) { (down[e.s] = down[e.s] || []).push(e.t); (up[e.t] = up[e.t] || []).push(e.s); }
    return { up, down };
  }
  function closure(id, adj) {
    const seen = new Set([id]), st = [id];
    while (st.length) { const c = st.pop(); for (const x of adj[c] || []) if (!seen.has(x)) { seen.add(x); st.push(x); } }
    return seen;
  }

  // ── typed reading graph: directed adjacency + aspect-fitted shelf-packed band layout ──────────
  // Ported from the SWE explorer's core.graphLayout: pure, deterministic, no DOM. Groups the drawn
  // nodes into corpus bands (gen/mat), sizes each band's grid, shelf-packs the bands, and sweeps 28
  // target widths to pick the packing whose aspect best matches the pane — the SVG then fills via
  // viewBox with minimal letterboxing. Cyclic-capable (unlike the acyclic overlays).
  function typedAdjacency(edges) {
    const up = {}, down = {};
    for (const e of edges) { (down[e.s] = down[e.s] || []).push(e.t); (up[e.t] = up[e.t] || []).push(e.s); }
    return { up, down };
  }
  const GNW = 162, GNH = 52, GGX = 16, GGY = 12, GPADX = 10, GPADY = 8, GLABELH = 28, GBANDGAP = 40, GSHELFGAP = 50, GMARGIN = 26;
  const gclamp = (v, lo, hi) => Math.max(lo, Math.min(hi, v));
  function primaryCorpus(n, order) { for (const c of order) if (n.corpus.includes(c)) return c; return n.corpus[0]; }
  const bandSortKey = (n) => (n.subfield && n.subfield[0]) || (n.paradigm && n.paradigm[0]) || '';
  function bandGrid(key, list) {
    const ncols = gclamp(Math.round(Math.sqrt(list.length * 0.9)), 2, 7);
    const rows = Math.ceil(list.length / ncols);
    return { key, list, ncols, rows, w: ncols * (GNW + GGX) - GGX + 2 * GPADX, h: rows * (GNH + GGY) - GGY + GLABELH + 2 * GPADY };
  }
  function packBands(bands, targetW) {
    let x = 0, y = 0, shelfH = 0, maxW = 0; const placed = [];
    for (const b of bands) {
      if (x > 0 && x + GBANDGAP + b.w > targetW) { y += shelfH + GSHELFGAP; x = 0; shelfH = 0; }
      const bx = x === 0 ? 0 : x + GBANDGAP;
      placed.push({ band: b, x: bx, y }); x = bx + b.w; shelfH = Math.max(shelfH, b.h); maxW = Math.max(maxW, x);
    }
    return { placed, W: maxW, H: y + shelfH };
  }
  /** @returns {{positions:Record<string,{x:number,y:number}>, bands:any[], width:number, height:number, box:{NW:number,NH:number}}} */
  function graphLayout(nodes, edges, corpusOrder, opts) {
    const target = (opts && opts.aspect) || 1.4;
    const inGraph = new Set(); for (const e of edges) { inGraph.add(e.s); inGraph.add(e.t); }
    const drawn = nodes.filter((n) => inGraph.has(n.id));
    const byBand = {};
    for (const n of drawn) { const c = primaryCorpus(n, corpusOrder); (byBand[c] = byBand[c] || []).push(n); }
    const bands = [];
    for (const c of corpusOrder) {
      const list = byBand[c]; if (!list || !list.length) continue;
      list.sort((a, b) => bandSortKey(a).localeCompare(bandSortKey(b)) || ((a.year || 9999) - (b.year || 9999)) || a.title.localeCompare(b.title));
      bands.push(bandGrid(c, list));
    }
    if (!bands.length) return { positions: {}, bands: [], width: 2 * GMARGIN, height: 2 * GMARGIN, box: { NW: GNW, NH: GNH } };
    const widths = bands.map((b) => b.w);
    const minT = Math.max.apply(null, widths), maxT = widths.reduce((a, b) => a + b, 0) + GBANDGAP * (bands.length - 1);
    let best = null;
    for (let i = 0; i <= 28; i++) {
      const t = minT + (maxT - minT) * (i / 28), packed = packBands(bands, t);
      const score = Math.abs(packed.W / packed.H - target);
      if (!best || score < best.score) best = Object.assign({ score }, packed);
    }
    const positions = {}, outBands = [];
    for (const p of best.placed) {
      const b = p.band, bx = p.x + GMARGIN, by = p.y + GMARGIN;
      outBands.push({ key: b.key, x: bx, y: by, w: b.w, h: b.h, count: b.list.length, labelX: bx + GPADX, labelY: by + GPADY + 14 });
      b.list.forEach((n, i) => { positions[n.id] = { x: bx + GPADX + (i % b.ncols) * (GNW + GGX), y: by + GPADY + GLABELH + Math.floor(i / b.ncols) * (GNH + GGY) }; });
    }
    return { positions, bands: outBands, width: best.W + 2 * GMARGIN, height: best.H + 2 * GMARGIN, box: { NW: GNW, NH: GNH } };
  }

  // Levels are horizontal bands top→bottom; within a band, a grid of ≤MAXC columns whose order
  // comes from three barycenter sweeps over the overlay edges. Fixed natural size; the SVG
  // scales it via viewBox — built once, no resize recomputation.
  const ONW = 168, ONH = 52, OGX = 14, OGY = 14, OBGAP = 46, OGUT = 196, OMARG = 26, OPAD = 14, MAXC = 7;

  /** @returns {{positions:Record<string,{x:number,y:number}>, bands:any[], width:number,
   *            height:number, box:{NW:number,NH:number}}} */
  function overlayLayout(overlay) {
    const adj = overlayAdjacency(overlay);
    const order = {};
    for (const lv of overlay.levels) order[lv.key] = [];
    for (const id in overlay.members) order[overlay.members[id]].push(id);
    const keys = overlay.levels.map((lv) => lv.key);

    const grid = (n) => { const c = Math.min(MAXC, Math.max(1, n)); return { cols: c, rows: Math.ceil(n / c) }; };
    const cx = {};
    function placeRow(k) {
      const g = grid(order[k].length);
      order[k].forEach((id, i) => { cx[id] = (i % g.cols) * (ONW + OGX) + ONW / 2; });
      return g.cols * (ONW + OGX) - OGX;
    }
    function sortRow(k, nb) {
      const val = {};
      for (const id of order[k]) {
        const xs = (nb[id] || []).filter((x) => cx[x] !== undefined).map((x) => cx[x]);
        val[id] = xs.length ? xs.reduce((a, b) => a + b, 0) / xs.length : cx[id];
      }
      order[k] = order[k].slice().sort((a, b) => (val[a] - val[b]) || a.localeCompare(b));
    }
    const widths = {};
    for (const k of keys) widths[k] = placeRow(k);
    for (const k of keys.slice(1)) { sortRow(k, adj.up); widths[k] = placeRow(k); }
    for (const k of keys.slice(0, -1).reverse()) { sortRow(k, adj.down); widths[k] = placeRow(k); }
    for (const k of keys.slice(1)) { sortRow(k, adj.up); widths[k] = placeRow(k); }

    const maxW = Math.max.apply(null, keys.map((k) => widths[k]));
    const positions = {}, bands = [];
    let y = OMARG;
    for (const lv of overlay.levels) {
      const k = lv.key, g = grid(order[k].length);
      const bandH = g.rows * (ONH + OGY) - OGY + 2 * OPAD;
      const off = OGUT + (maxW - widths[k]) / 2;
      order[k].forEach((id, i) => {
        positions[id] = { x: off + (i % g.cols) * (ONW + OGX),
                          y: y + OPAD + Math.floor(i / g.cols) * (ONH + OGY) };
      });
      bands.push({ key: k, label: lv.label, note: lv.note, count: order[k].length,
                   x: 10, y, w: OGUT + maxW + OMARG - 10, h: bandH });
      y += bandH + OBGAP;
    }
    return { positions, bands, width: OGUT + maxW + 2 * OMARG, height: y - OBGAP + OMARG,
             box: { NW: ONW, NH: ONH } };
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
           STRATA, stratumOf, strataBuckets, anchorColumns, paradigmBuckets,
           overlayAdjacency, closure, overlayLayout, triage, stats,
           typedAdjacency, graphLayout, primaryCorpus };
})();
