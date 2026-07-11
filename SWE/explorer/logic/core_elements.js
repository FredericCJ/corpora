// core_elements.js — FUNCTIONAL CORE for the element layer (design + architecture realms). Pure
// computations for the four element semantic views: the search/visible set, realm×kind×tag facet
// counts (reuses SWE.core.facetCount), the typed element adjacency + cycle-safe closure, the
// design↔architecture bridge grouping, and the element↔works coverage inversion. No DOM.
window.SWE = window.SWE || {};
SWE.coreEl = (function () {
  'use strict';
  const CROSS = new Set(['realizes', 'enables']);        // design -> architecture
  const CROSS_REV = new Set(['constrains']);             // architecture -> design
  const WITHIN = new Set(['specializes', 'composes-with', 'alternative-to', 'uses']);
  const IMPL = new Set(['implements']);                  // design -> design

  // The four element views' semantics (single source for headers + inspector overview + MODELS.md).
  const VIEWS = {
    'el-taxonomy': { label: 'Element taxonomy',
      semantic: 'The realm × kind × tag lattice over both element catalogs, with live counts.',
      question: 'What implementation- and architecture-level vocabulary exists, and how is it distributed?',
      computed: 'Pure filtering/counting over element tags (realm, kind, confidence, quality-attribute); honours the global search.' },
    'el-bridge': { label: 'Design↔Arch bridge',
      semantic: 'The mission-critical map: which architecture elements anchor which design elements, and the unbridged tail.',
      question: 'How does implementation vocabulary map onto architecture — and what has no architectural counterpart?',
      computed: 'Cross-realm realizes/enables/constrains edges grouped by architecture target; the 6 unbridged design elements listed explicitly.' },
    'el-graph': { label: 'Element relations',
      semantic: 'The typed element relation graph (realizes/enables/constrains/implements/specializes/…); hover traces closure.',
      question: 'What realizes, specializes, composes-with, or is an alternative to what?',
      computed: 'Adjacency over the 1132 edges; cycle-safe forward/back closure from a focused element.' },
    'el-coverage': { label: 'Element coverage',
      semantic: 'Which works teach which elements (Phase 2), and where coverage is thin.',
      question: 'Where do I read about this element; which works are element-dense; what is thinly covered?',
      computed: 'The element→works coverage inverted both ways; thin (single-work) and gap (zero-work) elements surfaced.' },
  };

  /** Build the reusable index. Pure over the parsed element payload. */
  function buildIndex(E) {
    const byId = {}, hay = {};
    for (const n of E.nodes) {
      byId[n.id] = n;
      hay[n.id] = (n.id + ' ' + n.name + ' ' + (n.aka || []).join(' ') + ' ' + n.what).toLowerCase();
    }
    const out = {}, inn = {};
    for (const e of E.edges) {
      (out[e.from] = out[e.from] || []).push(e);
      (inn[e.to] = inn[e.to] || []).push(e);
    }
    const elementsByWork = {};
    for (const n of E.nodes) for (const w of (n.works || [])) (elementsByWork[w] = elementsByWork[w] || []).push(n.id);
    const design = E.nodes.filter((n) => n.realm === 'design');
    const arch = E.nodes.filter((n) => n.realm === 'architecture');
    return { byId, hay, out, inn, elementsByWork, design, arch, nodes: E.nodes, edges: E.edges,
             unbridged: E.unbridged || [], works: E.works || {}, meta: E.meta || {} };
  }

  /** @returns {Set<string>} element ids whose id/name/aka/what contains the query (empty q → all). */
  function visible(idx, q) {
    q = (q || '').trim().toLowerCase();
    const out = new Set();
    for (const n of idx.nodes) if (!q || idx.hay[n.id].includes(q)) out.add(n.id);
    return out;
  }

  /** Cycle-safe closure over the typed edges in one direction ('out'|'in'|'both'). Pure. */
  function closure(id, idx, dir) {
    const seen = new Set([id]), st = [id];
    while (st.length) {
      const c = st.pop();
      const nb = [];
      if (dir !== 'in') for (const e of idx.out[c] || []) nb.push(e.to);
      if (dir !== 'out') for (const e of idx.inn[c] || []) nb.push(e.from);
      for (const x of nb) if (!seen.has(x)) { seen.add(x); st.push(x); }
    }
    return seen;
  }

  /** Group the cross-realm bridge by architecture target: archId -> [{from,kind,provenance,note}]. Pure. */
  function bridgeByArch(idx) {
    const g = {};
    for (const e of idx.edges) {
      if (CROSS.has(e.kind)) (g[e.to] = g[e.to] || []).push({ from: e.from, kind: e.kind, provenance: e.provenance, note: e.note });
      else if (CROSS_REV.has(e.kind)) (g[e.from] = g[e.from] || []).push({ from: e.to, kind: e.kind, provenance: e.provenance, note: e.note });
    }
    return g;
  }

  /** Coverage buckets: gap (0 works), thin (1), covered (>=2) among design elements. Pure. */
  function coverageBuckets(idx) {
    const gap = [], thin = [], covered = [];
    for (const n of idx.design) (n.works.length === 0 ? gap : n.works.length === 1 ? thin : covered).push(n);
    return { gap, thin, covered };
  }

  const isCross = (k) => CROSS.has(k) || CROSS_REV.has(k);
  return { VIEWS, buildIndex, visible, closure, bridgeByArch, coverageBuckets,
           CROSS, CROSS_REV, WITHIN, IMPL, isCross };
})();
