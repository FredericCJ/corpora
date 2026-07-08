// core.js — FUNCTIONAL CORE (web_architecture_manifest §4 / F1). Every model computation lives
// here as a pure function of (data, state): the visible set, the tier-layered DAG layout with
// barycenter ordering + parallel-set enclosures, reachability closures, exact path counting and
// capped path enumeration, and tier buckets. No DOM, no globals mutated — this is the
// unit-testable half; the view shells only project it.
window.CALC = window.CALC || {};
CALC.core = (function () {
  'use strict';

  // ── search / visible set ────────────────────────────────────────────────────────────
  /** @type {Record<string,string>|null} */ let hay = null;
  function buildIndex(corpus) {
    hay = {};
    for (const n of corpus.nodes)
      hay[n.id] = (n.id + ' ' + n.title + ' ' + n.authors + ' ' + n.publisher + ' ' + n.edition).toLowerCase();
  }
  /** @returns {Set<string>} ids passing search + rigor + tier filters. Pure. */
  function visibleIds(corpus, state) {
    if (!hay) buildIndex(corpus);
    const q = (state.q || '').trim().toLowerCase();
    const out = new Set();
    for (const n of corpus.nodes) {
      if (state.rigor && n.rigor !== state.rigor) continue;
      if (state.tier !== '' && String(n.tier) !== state.tier) continue;
      if (q && !hay[n.id].includes(q)) continue;
      out.add(n.id);
    }
    return out;
  }

  // ── adjacency + closure (DAG; the walk is still guarded against revisits) ───────────
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

  // ── tier-layered DAG layout ─────────────────────────────────────────────────────────
  // Tiers are horizontal bands top→bottom (the curriculum descends into depth); within a band the
  // order is a pure barycenter relaxation (down, up, down sweeps) with parallel-set members kept
  // contiguous so their enclosure can be drawn. The drawing has a fixed natural size; the SVG
  // scales it into the pane via viewBox (no per-resize recomputation needed).
  const NW = 176, NH = 62, GX = 22, GY = 60, GUTTER = 196, MARGIN = 26, PSPAD = 10, PSTOP = 18;

  /** @returns {{positions:Record<string,{x:number,y:number}>, rows:any[], psBoxes:any[],
   *            width:number, height:number, box:{NW:number,NH:number}}} */
  function dagLayout(nodes, edges, tiers, psets) {
    const byId = {}; nodes.forEach((n) => { byId[n.id] = n; });
    const adj = adjacency(edges);
    const psOf = {};
    for (const ps of psets) for (const m of ps.members) psOf[m] = ps.id;

    /** @type {Record<number,string[]>} tier -> ordered ids (catalogue order initially) */
    const order = {};
    for (const t of tiers) order[t.tier] = [];
    for (const n of nodes) order[n.tier].push(n.id);
    const tierIds = tiers.map((t) => t.tier);

    const rowY = {}; tierIds.forEach((t, i) => { rowY[t] = MARGIN + PSTOP + i * (NH + GY); });
    /** @type {Record<string,number>} id -> x center (relative, before row centring) */
    const cx = {};

    function placeRow(t) {
      let x = 0, prevPs = null;
      for (const id of order[t]) {
        const ps = psOf[id] || null;
        if (ps !== prevPs) { if (prevPs) x += PSPAD; if (ps) x += PSPAD; }
        cx[id] = x + NW / 2; x += NW + GX; prevPs = ps;
      }
      return x - GX + (prevPs ? PSPAD : 0);
    }
    function sortRow(t, neighborsOf) {
      const val = {};
      for (const id of order[t]) {
        const nb = (neighborsOf[id] || []).filter((x) => cx[x] !== undefined);
        val[id] = nb.length ? nb.reduce((a, b) => a + cx[b], 0) / nb.length : cx[id];
      }
      const groupVal = {};
      for (const ps of psets) {
        const here = ps.members.filter((m) => order[t].includes(m));
        if (here.length) groupVal[ps.id] = here.reduce((a, m) => a + val[m], 0) / here.length;
      }
      order[t] = order[t].slice().sort((a, b) => {
        const ka = psOf[a] ? groupVal[psOf[a]] : val[a], kb = psOf[b] ? groupVal[psOf[b]] : val[b];
        return (ka - kb) || ((psOf[a] || '').localeCompare(psOf[b] || '')) || (val[a] - val[b]) || a.localeCompare(b);
      });
    }

    const widths = {};
    for (const t of tierIds) widths[t] = placeRow(t);
    for (const t of tierIds.slice(1)) { sortRow(t, adj.up); widths[t] = placeRow(t); }
    for (const t of tierIds.slice(0, -1).reverse()) { sortRow(t, adj.down); widths[t] = placeRow(t); }
    for (const t of tierIds.slice(1)) { sortRow(t, adj.up); widths[t] = placeRow(t); }

    const maxW = Math.max.apply(null, tierIds.map((t) => widths[t]));
    const positions = {};
    for (const t of tierIds) {
      const off = GUTTER + (maxW - widths[t]) / 2;
      for (const id of order[t]) positions[id] = { x: off + cx[id] - NW / 2, y: rowY[t] };
    }

    const rows = tiers.map((t) => ({
      tier: t.tier, name: t.name, rigor: t.rigor, count: order[t.tier].length,
      y: rowY[t.tier], bandY: rowY[t.tier] - PSTOP - 4, bandH: NH + PSTOP + 4 + 16,
      bandX: 10, bandW: GUTTER + maxW + MARGIN - 10,
    }));
    const psBoxes = [];
    for (const ps of psets) {
      const xs = ps.members.map((m) => positions[m].x);
      const x0 = Math.min.apply(null, xs) - PSPAD, x1 = Math.max.apply(null, xs) + NW + PSPAD;
      const y = positions[ps.members[0]].y;
      psBoxes.push({ id: ps.id, label: ps.label, x: x0, y: y - PSTOP + 3, w: x1 - x0, h: NH + PSTOP + 4 });
    }
    return { positions, rows, psBoxes,
             width: GUTTER + maxW + MARGIN, height: rowY[tierIds[tierIds.length - 1]] + NH + MARGIN + 14,
             box: { NW, NH } };
  }

  // ── tier buckets ─────────────────────────────────────────────────────────────────────
  function tierBuckets(nodes, tiers) {
    const b = {}; for (const t of tiers) b[t.tier] = [];
    for (const n of nodes) b[n.tier].push(n);
    for (const t in b) b[t].sort((x, y) => x.id.localeCompare(y.id));
    return b;
  }

  // ── path counting + capped enumeration (the DAG makes both safe) ─────────────────────
  /** Exact count by memoised DP + enumeration capped at `cap` (capped flag says so — no silent
   * caps). Pruned by reverse reachability so the DFS never walks a dead branch. Pure. */
  function pathsBetween(from, to, adj, cap) {
    if (from === to) return { count: 1, paths: [[from]], capped: false };
    const canReach = closure(to, adj.up);
    if (!canReach.has(from)) return { count: 0, paths: [], capped: false };
    const memo = new Map();
    function cnt(x) {
      if (x === to) return 1;
      if (memo.has(x)) return memo.get(x);
      let c = 0; for (const nx of adj.down[x] || []) if (canReach.has(nx)) c += cnt(nx);
      memo.set(x, c); return c;
    }
    const count = cnt(from);
    const paths = []; let capped = false;
    (function dfs(cur, acc) {
      if (paths.length >= cap) { capped = true; return; }
      acc.push(cur);
      if (cur === to) paths.push(acc.slice());
      else for (const nx of adj.down[cur] || []) { if (canReach.has(nx)) dfs(nx, acc); if (capped) break; }
      acc.pop();
    })(from, []);
    paths.sort((a, b) => a.length - b.length || a.join().localeCompare(b.join()));
    return { count, paths, capped };
  }

  // ── overview stats ───────────────────────────────────────────────────────────────────
  function stats(corpus, relations) {
    const kept = corpus.nodes.filter((n) => n.status === 'kept');
    const ev = relations.edges.filter((e) => e.tag === 'EVIDENCED').length;
    return {
      nodes: corpus.nodes.length, kept: kept.length, dropped: corpus.nodes.length - kept.length,
      edges: relations.edges.length, ev, jd: relations.edges.length - ev,
      tiers: corpus.tiers.length, psets: relations.parallelSets.length,
      sources: kept.filter((n) => n.flags.includes('source')).length,
      sinks: kept.filter((n) => n.flags.includes('sink')).length,
    };
  }

  return { buildIndex, visibleIds, adjacency, closure, dagLayout, tierBuckets, pathsBetween, stats };
})();
