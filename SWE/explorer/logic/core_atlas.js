// core_atlas.js — FUNCTIONAL CORE for the atlas layer (the "graph as map"). Pure computations over the
// precomputed geography in SWE.atlas: the island index, element→island lookup, search→island locate
// (wayfinding), route thresholding/aggregation, and SVG-path helpers for hulls and bundled sea-routes.
// The browser NEVER runs the heavy full-graph layout — coordinates ship precomputed in data/atlas.json;
// this core only indexes, locates, and projects. No DOM.
window.SWE = window.SWE || {};
SWE.coreAtlas = (function () {
  'use strict';

  /** Build the reusable atlas index. Pure over the parsed atlas payload. */
  function buildIndex(atlas) {
    const islandById = {}, memberIsland = {}, memberById = {};
    for (const isl of atlas.islands) {
      islandById[isl.id] = isl;
      for (const m of isl.members) { memberIsland[m.id] = isl.id; memberById[m.id] = m; }
    }
    const familyHex = {}; for (const f of atlas.meta.families) familyHex[f.id] = f.hex;
    const familyName = {}; for (const f of atlas.meta.families) familyName[f.id] = f.name;
    // route adjacency (island -> [{island,weight}]) — symmetric, from the precomputed routes
    const routeAdj = {};
    for (const r of atlas.routes || []) {
      (routeAdj[r.from] = routeAdj[r.from] || []).push({ island: r.to, weight: r.weight });
      (routeAdj[r.to] = routeAdj[r.to] || []).push({ island: r.from, weight: r.weight });
    }
    for (const k in routeAdj) routeAdj[k].sort((a, b) => b.weight - a.weight);
    return { atlas, islandById, memberIsland, memberById, familyHex, familyName, routeAdj,
             islands: atlas.islands, routes: atlas.routes || [], families: atlas.meta.families,
             bridgeFlow: atlas.bridgeFlow || { families: [], anchors: [], flows: [] } };
  }

  /** Island containing an element id (or null). Pure. */
  function islandOf(id, idx) { return idx.memberIsland[id] ? idx.islandById[idx.memberIsland[id]] : null; }

  /** Wayfinding: rank islands by how well the query matches their members (id/name substring).
   * Returns [{island, hits, sample}], best first. Empty query → []. Pure. */
  function locate(query, idx) {
    const q = (query || '').trim().toLowerCase();
    if (!q) return [];
    const score = {};
    for (const isl of idx.islands) {
      let hits = 0, sample = null;
      for (const m of isl.members) {
        if (m.id.includes(q) || m.name.toLowerCase().includes(q)) { hits++; if (!sample) sample = m; }
      }
      // island name match is a strong signal too
      const nameHit = isl.name.toLowerCase().includes(q) ? 3 : 0;
      if (hits + nameHit > 0) score[isl.id] = { island: isl, hits: hits + nameHit, sample };
    }
    return Object.values(score).sort((a, b) => b.hits - a.hits);
  }

  /** First element across all islands whose id/name matches (for teleport-to-node). Pure. */
  function findMember(query, idx) {
    const q = (query || '').trim().toLowerCase();
    if (!q) return null;
    for (const isl of idx.islands) for (const m of isl.members)
      if (m.id === q || m.id.includes(q) || m.name.toLowerCase().includes(q)) return { member: m, island: isl };
    return null;
  }

  /** Keep only the strongest routes (top `frac` by weight, min weight `minW`) so the L0 sea doesn't
   * hairball. Deterministic (stable sort by weight then id). Pure. */
  function topRoutes(idx, frac, minW) {
    const rs = idx.routes.filter((r) => r.weight >= (minW || 1)).slice()
      .sort((a, b) => b.weight - a.weight || (a.from + a.to).localeCompare(b.from + b.to));
    const keep = Math.max(0, Math.round(rs.length * (frac == null ? 1 : frac)));
    return rs.slice(0, keep);
  }

  /** SVG polygon path from [[x,y]...] normalized points, projected by (proj) to pixel space. Pure. */
  function hullPath(points, proj) {
    if (!points || !points.length) return '';
    return points.map((p, i) => (i ? 'L' : 'M') + proj(p[0], p[1])).join(' ') + ' Z';
  }

  /** Members of an island matching a query, as a Set of ids (for L1 highlight). Pure. */
  function matchMembers(island, query) {
    const q = (query || '').trim().toLowerCase(); const out = new Set();
    if (!q) return out;
    for (const m of island.members) if (m.id.includes(q) || m.name.toLowerCase().includes(q)) out.add(m.id);
    return out;
  }

  /** Level implied by the navigation state. Pure. */
  function levelOf(st, idx) {
    if (st.sel && idx.memberById[st.sel]) return 'L2';
    if (st.island && idx.islandById[st.island]) return 'L1';
    return 'L0';
  }

  return { buildIndex, islandOf, locate, findMember, topRoutes, hullPath, matchMembers, levelOf };
})();
