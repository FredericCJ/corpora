// graph.js — FUNCTIONAL CORE (web_architecture_manifest §4 / F1). Pure layout + graph maths.
// No DOM, no SVG, no globals touched: (nodes, edges) -> geometry. Runs in any JS runtime and is
// the unit-testable half of the app. The imperative shell (render.js) projects this to SVG.
window.DS = window.DS || {};
DS.graph = (function () {
  'use strict';

  // node box + spacing, in SVG user units (the viewBox scales them to the pane)
  const NW = 152, NH = 48, GX = 16, GY = 12;
  const PADX = 10, PADY = 8, LABELH = 28, BANDGAP = 40, SHELFGAP = 50, MARGIN = 26;
  const TIER_RANK = { root: 0, backfill: 1, modern: 2 };

  const clamp = (v, lo, hi) => Math.max(lo, Math.min(hi, v));

  /** Directed adjacency (up = towards ancestors, down = towards descendants). Pure.
   * @param {import('./parse.js').DSEdge[]} edges */
  function adjacency(edges) {
    const up = {}, down = {};
    for (const e of edges) {
      (down[e.s] = down[e.s] || []).push(e.t);
      (up[e.t] = up[e.t] || []).push(e.s);
    }
    return { up, down };
  }

  /** Cycle-safe reachability closure from `id` along `adj`. Terminates on cycles. Pure.
   * @param {string} id @param {Record<string,string[]>} adj @returns {Set<string>} */
  function closure(id, adj) {
    const seen = new Set([id]), stack = [id];
    while (stack.length) {
      const c = stack.pop();
      for (const x of adj[c] || []) if (!seen.has(x)) { seen.add(x); stack.push(x); }
    }
    return seen;
  }

  function bandGrid(family, list) {
    const ncols = clamp(Math.round(Math.sqrt(list.length * 1.25)), 2, 6);
    const rows = Math.ceil(list.length / ncols);
    const w = ncols * (NW + GX) - GX + 2 * PADX;
    const h = rows * (NH + GY) - GY + LABELH + 2 * PADY;
    return { family, list, ncols, rows, w, h };
  }

  function pack(bands, targetW) {
    let x = 0, y = 0, shelfH = 0, maxW = 0;
    const placed = [];
    for (const b of bands) {
      if (x > 0 && x + BANDGAP + b.w > targetW) { y += shelfH + SHELFGAP; x = 0; shelfH = 0; }
      const bx = x === 0 ? 0 : x + BANDGAP;
      placed.push({ band: b, x: bx, y });
      x = bx + b.w; shelfH = Math.max(shelfH, b.h); maxW = Math.max(maxW, x);
    }
    return { placed, W: maxW, H: y + shelfH };
  }

  /**
   * Compute the whole board layout, shelf-packing family bands to best match `opts.aspect`
   * (so the SVG fills its pane with minimal letterboxing — single viewport, no scroll). Pure.
   * @param {import('./parse.js').DSNode[]} nodes
   * @param {import('./parse.js').DSEdge[]} edges
   * @param {string[]} familyOrder
   * @param {{aspect?:number}} [opts]
   */
  function computeLayout(nodes, edges, familyOrder, opts) {
    const target = (opts && opts.aspect) || 1.4;
    const inGraph = new Set();
    for (const e of edges) { inGraph.add(e.s); inGraph.add(e.t); }
    const drawn = nodes.filter((n) => inGraph.has(n.id));

    const byFam = {};
    for (const n of drawn) (byFam[n.family] = byFam[n.family] || []).push(n);
    const bands = [];
    for (const f of familyOrder) {
      const list = byFam[f];
      if (!list || !list.length) continue;
      list.sort((a, b) =>
        (TIER_RANK[a.tier] - TIER_RANK[b.tier]) ||
        ((a.year == null ? 9999 : a.year) - (b.year == null ? 9999 : b.year)) ||
        a.name.localeCompare(b.name));
      bands.push(bandGrid(f, list));
    }

    // search a target width that yields the aspect closest to the pane's
    const widths = bands.map((b) => b.w);
    const minT = Math.max.apply(null, widths);
    const maxT = widths.reduce((a, b) => a + b, 0) + BANDGAP * (bands.length - 1);
    let best = null;
    const STEPS = 28;
    for (let i = 0; i <= STEPS; i++) {
      const t = minT + (maxT - minT) * (i / STEPS);
      const packed = pack(bands, t);
      const score = Math.abs(packed.W / packed.H - target);
      if (!best || score < best.score) best = Object.assign({ score }, packed);
    }

    const positions = {}, outBands = [];
    for (const p of best.placed) {
      const b = p.band, bx = p.x + MARGIN, by = p.y + MARGIN;
      outBands.push({
        family: b.family, x: bx, y: by, w: b.w, h: b.h, count: b.list.length,
        labelX: bx + PADX, labelY: by + PADY + 14,
      });
      b.list.forEach((n, i) => {
        positions[n.id] = {
          x: bx + PADX + (i % b.ncols) * (NW + GX),
          y: by + PADY + LABELH + Math.floor(i / b.ncols) * (NH + GY),
        };
      });
    }
    return { positions, bands: outBands, width: best.W + 2 * MARGIN, height: best.H + 2 * MARGIN,
             box: { NW, NH } };
  }

  return { computeLayout, adjacency, closure, NW, NH };
})();
