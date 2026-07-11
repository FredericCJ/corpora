// views/el_atlas.js — Element view 10: THE ARCHIPELAGO (the "graph as map", shell). Semantic zoom over
// the whole 1083-element graph at three levels, with one breadcrumb and full state in the URL hash:
//   L0 Atlas   — ~20 island bubbles on a sea; size = members, tint = family; sea-routes = aggregated
//                cross-island relations. Not readable by design; click an island to drill.
//   L1 Island  — one community, readable: hub centred, members on their precomputed radial coords, the
//                WS1-enriched intra-island edges drawn; labelled PORTS around the rim hop to neighbours
//                (a port points toward where that island actually sits on the L0 map).
//   L2 Node    — select a member; it lights its ego edges and the persistent inspector shows full
//                detail (definition, covering works, every typed relation). Reuses the element layer.
// All geography is PRECOMPUTED and deterministic (data/atlas.json). This shell only projects + wires.
window.SWE = window.SWE || {}; SWE.views = SWE.views || {};
SWE.views['el-atlas'] = (function () {
  'use strict';
  const U = SWE.util, CA = SWE.coreAtlas, S = SWE.state;
  const VB = 1000;                                   // square viewBox; layout is square-native ([0,1]^2)
  const PAD = 0.04;                                  // inner padding so bubbles/nodes never touch the edge
  const proj = (x, y) => [(PAD + (1 - 2 * PAD) * x) * VB, (PAD + (1 - 2 * PAD) * y) * VB];
  const projStr = (x, y) => { const p = proj(x, y); return p[0].toFixed(1) + ' ' + p[1].toFixed(1); };

  function mount(root, ctx) {
    const idx = ctx.atlasIndex, EL = ctx.elIndex;
    const vp = U.el('div', { class: 'vp' });
    const head = U.el('div', { class: 'vp-head' });
    const h2 = U.el('h2', { text: 'Atlas — the element archipelago' });
    const crumb = U.el('div', { class: 'atlas-crumb' });
    head.appendChild(h2); head.appendChild(crumb);
    head.appendChild(U.el('p', { class: 'note', text: 'A map of all 1083 elements: ~' + idx.islands.length +
      ' emergent islands, coloured by family, joined by aggregated relations. Click an island to zoom in; ' +
      'inside, click a node for its detail, or a rim port to hop to a neighbour. Search flies you to a match.' }));
    const body = U.el('div', { class: 'vp-body' });
    const board = U.el('div', { class: 'board atlas-board' });
    body.appendChild(board);
    vp.appendChild(head); vp.appendChild(body); root.appendChild(vp);

    // ---- breadcrumb ----
    function drawCrumb() {
      const st = S.get(); crumb.replaceChildren();
      const step = (label, patch, active) => U.el('span', { class: 'atlas-step' + (active ? ' active' : ''),
        text: label, tabindex: '0', role: 'link',
        onclick: () => S.set(patch), onkeydown: (e) => { if (e.key === 'Enter') S.set(patch); } });
      crumb.appendChild(step('Archipelago', { island: '', sel: null }, !st.island));
      const isl = st.island && idx.islandById[st.island];
      if (isl) {
        crumb.appendChild(U.el('span', { class: 'atlas-sep', text: '▸' }));
        crumb.appendChild(step(isl.name, { island: isl.id, sel: null }, !st.sel));
      }
      const m = st.sel && idx.memberById[st.sel];
      if (m) { crumb.appendChild(U.el('span', { class: 'atlas-sep', text: '▸' })); crumb.appendChild(step(m.name, {}, true)); }
    }

    function famHex(f) { return idx.familyHex[f] || 'var(--mut)'; }

    // ---------- L0 : the archipelago ----------
    function renderL0() {
      const st = S.get();
      const hi = CA.locate(st.q, idx);                 // search-teleport highlight
      const hiSet = new Set(hi.map((h) => h.island.id));
      const svg = U.svg('svg', { viewBox: `0 0 ${VB} ${VB}`, preserveAspectRatio: 'xMidYMid meet',
        class: 'atlas-svg', role: 'img', 'aria-label': `Archipelago of ${idx.islands.length} element islands` });
      const gR = U.svg('g'), gI = U.svg('g');
      svg.appendChild(gR); svg.appendChild(gI);

      // sea-routes (keep the stronger half to avoid a hairball; bundle as gentle quadratics)
      const routes = CA.topRoutes(idx, 0.55, 2);
      for (const r of routes) {
        const a = idx.islandById[r.from], b = idx.islandById[r.to]; if (!a || !b) continue;
        const [ax, ay] = proj(a.cx, a.cy), [bx, by] = proj(b.cx, b.cy);
        const mx = (ax + bx) / 2, my = (ay + by) / 2 - Math.hypot(bx - ax, by - ay) / 7;
        const path = U.svg('path', { d: `M${ax} ${ay} Q ${mx} ${my}, ${bx} ${by}`, class: 'atlas-route',
          'stroke-width': (0.6 + Math.min(3.2, Math.log2(r.weight))).toFixed(2) });
        path.dataset.a = r.from; path.dataset.b = r.to;
        gR.appendChild(path);
      }

      // island bubbles
      for (const isl of idx.islands) {
        const [cx, cy] = proj(isl.cx, isl.cy), r = isl.r * (1 - 2 * PAD) * VB;
        const g = U.svg('g', { class: 'atlas-island', tabindex: '0', role: 'button',
          'aria-label': `${isl.name}: ${isl.size} elements, ${isl.family} family` });
        if (st.q && hiSet.size) g.classList.add(hiSet.has(isl.id) ? 'hit' : 'dim');
        const circ = U.svg('circle', { cx, cy, r: r.toFixed(1) });
        circ.style.fill = famHex(isl.family); circ.style.stroke = famHex(isl.family);
        g.appendChild(circ);
        const label = U.wrapLabel(isl.name, 18, 2);
        label.forEach((ln, i) => {
          const t = U.svg('text', { x: cx, y: cy - (label.length - 1) * 7 + i * 14, class: 'atlas-ilabel', 'text-anchor': 'middle' });
          t.textContent = ln; g.appendChild(t);
        });
        const cnt = U.svg('text', { x: cx, y: cy + r + 13, class: 'atlas-icount', 'text-anchor': 'middle' });
        cnt.textContent = isl.size; g.appendChild(cnt);
        const tip = U.svg('title');
        tip.textContent = `${isl.name} — ${isl.size} elements · family: ${idx.familyName[isl.family]} · hub: ${(EL.byId[isl.hub] || {}).name || isl.hub}`;
        g.appendChild(tip);
        const enter = () => { for (const p of gR.children) { const on = p.dataset.a === isl.id || p.dataset.b === isl.id; p.classList.toggle('hl', on); } };
        const leave = () => { for (const p of gR.children) p.classList.remove('hl'); };
        g.addEventListener('mouseenter', enter); g.addEventListener('mouseleave', leave);
        g.addEventListener('focus', enter); g.addEventListener('blur', leave);
        const go = () => S.set({ island: isl.id, sel: null });
        g.addEventListener('click', go);
        g.addEventListener('keydown', (e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); go(); } });
        gI.appendChild(g);
      }
      board.replaceChildren(svg);
      addLegend(); addMinimap(null);
      if (st.q && hi.length) addTeleportHint(hi[0].island);
    }

    // ---------- L1 : one island (also L2 when a node is selected) ----------
    function renderL1(isl) {
      const st = S.get();
      const mset = new Set(isl.members.map((m) => m.id));
      const svg = U.svg('svg', { viewBox: `0 0 ${VB} ${VB}`, preserveAspectRatio: 'xMidYMid meet',
        class: 'atlas-svg', role: 'img', 'aria-label': `Island ${isl.name}: ${isl.size} elements` });
      const gH = U.svg('g'), gE = U.svg('g'), gP = U.svg('g'), gN = U.svg('g');
      svg.appendChild(gH); svg.appendChild(gE); svg.appendChild(gP); svg.appendChild(gN);

      // island hull (family-tinted landmass)
      if (isl.hull && isl.hull.length >= 3) {
        const hp = U.svg('path', { d: CA.hullPath(isl.hull, projStr), class: 'atlas-hull' });
        hp.style.fill = famHex(isl.family); hp.style.stroke = famHex(isl.family);
        gH.appendChild(hp);
      }

      // intra-island edges (the WS1-enriched fabric), drawn once per unordered pair via out-edges
      const posOf = {}; isl.members.forEach((m) => { posOf[m.id] = proj(m.x, m.y); });
      const egoSet = st.sel && mset.has(st.sel) ? new Set([st.sel]) : null;
      const seen = new Set();
      for (const m of isl.members) {
        for (const e of (EL.out[m.id] || [])) {
          if (!mset.has(e.to)) continue;
          const key = m.id < e.to ? m.id + '|' + e.to : e.to + '|' + m.id;
          if (seen.has(key)) continue; seen.add(key);
          const [x1, y1] = posOf[m.id], [x2, y2] = posOf[e.to];
          const edi = e.provenance === 'editorial' || e.provenance === 'derived';
          const ln = U.svg('line', { x1, y1, x2, y2, class: 'atlas-edge' + (edi ? ' soft' : '') });
          if (egoSet && (egoSet.has(m.id) || egoSet.has(e.to))) ln.classList.add('ego');
          else if (egoSet) ln.classList.add('faded');
          gE.appendChild(ln);
        }
      }

      // ports to neighbour islands — placed on the rim toward the neighbour's real L0 position
      const ports = (isl.neighbours || []).slice(0, 8);
      for (const nb of ports) {
        const other = idx.islandById[nb.island]; if (!other) continue;
        const ang = Math.atan2(other.cy - isl.cy, other.cx - isl.cx);
        const [px, py] = [(PAD + (1 - 2 * PAD) * (0.5 + 0.47 * Math.cos(ang))) * VB,
                          (PAD + (1 - 2 * PAD) * (0.5 + 0.47 * Math.sin(ang))) * VB];
        const g = U.svg('g', { class: 'atlas-port', tabindex: '0', role: 'button', 'aria-label': `Hop to ${other.name}` });
        const dot = U.svg('circle', { cx: px, cy: py, r: 7 }); dot.style.fill = famHex(other.family);
        g.appendChild(dot);
        const anchor = px < VB / 2 ? 'start' : 'end';
        const t = U.svg('text', { x: px + (anchor === 'start' ? 11 : -11), y: py + 4, class: 'atlas-plabel', 'text-anchor': anchor });
        t.textContent = U.shortTitle(other.name, 24); g.appendChild(t);
        const go = () => S.set({ island: other.id, sel: null });
        g.addEventListener('click', go);
        g.addEventListener('keydown', (e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); go(); } });
        gP.appendChild(g);
      }

      // member nodes
      const hiSet = CA.matchMembers(isl, st.q);
      for (const m of isl.members) {
        const [x, y] = posOf[m.id];
        const isHub = m.id === isl.hub, isSel = m.id === st.sel;
        const g = U.svg('g', { class: 'atlas-node' + (isHub ? ' hub' : '') + (isSel ? ' sel' : ''),
          tabindex: '0', role: 'button', 'aria-label': `${m.name}, ${m.realm} ${m.kind}` });
        if (st.q) g.classList.toggle('dim', hiSet.size > 0 && !hiSet.has(m.id));
        if (egoSet && !isSel) {
          const linked = (EL.out[st.sel] || []).some((e) => e.to === m.id) || (EL.inn[st.sel] || []).some((e) => e.from === m.id);
          g.classList.toggle('faded', !linked);
        }
        const rad = isHub ? 9 : 5.5;
        const dot = U.svg('circle', { cx: x, cy: y, r: rad });
        dot.style.fill = famHex(m.family); dot.style.stroke = famHex(m.family);
        g.appendChild(dot);
        if (isHub || isSel || m.deg >= 6) {
          const t = U.svg('text', { x: x + rad + 3, y: y + 3.5, class: 'atlas-nlabel' + (isHub ? ' hub' : '') });
          t.textContent = U.shortTitle(m.name, 26); g.appendChild(t);
        }
        const tip = U.svg('title'); tip.textContent = `${m.name} — ${m.realm} / ${m.kind}` + (isHub ? ' (island hub)' : ''); g.appendChild(tip);
        const go = (ev) => { ev.stopPropagation(); S.set({ sel: m.id }); };
        g.addEventListener('click', go);
        g.addEventListener('keydown', (e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); go(e); } });
        gN.appendChild(g);
      }
      board.replaceChildren(svg);
      board.addEventListener('click', bgClear, { once: true });
      addLegend(); addMinimap(isl.id);
    }

    function bgClear() { if (S.get().sel) S.set({ sel: null }); }

    // ---- overlays: family legend, minimap, teleport hint ----
    function addLegend() {
      const leg = U.el('div', { class: 'atlas-legend' });
      for (const f of idx.families) {
        const sw = U.el('span', { class: 'atlas-swatch' }); sw.style.background = f.hex;
        leg.appendChild(U.el('span', { class: 'atlas-legrow' }, sw, U.el('span', { text: f.name })));
      }
      board.appendChild(leg);
    }
    function addMinimap(activeId) {
      const mm = U.svg('svg', { viewBox: `0 0 ${VB} ${VB}`, class: 'atlas-minimap', role: 'img', 'aria-label': 'Minimap' });
      for (const isl of idx.islands) {
        const [cx, cy] = proj(isl.cx, isl.cy);
        const c = U.svg('circle', { cx, cy, r: (isl.r * (1 - 2 * PAD) * VB * 0.8).toFixed(1) });
        c.style.fill = famHex(isl.family);
        c.style.opacity = activeId === isl.id ? '1' : '0.4';
        if (activeId === isl.id) { c.style.stroke = 'var(--ink)'; c.style.strokeWidth = '18'; }
        c.addEventListener('click', () => S.set({ island: isl.id, sel: null }));
        c.classList.add('atlas-mmdot');
        mm.appendChild(c);
      }
      board.appendChild(mm);
    }
    function addTeleportHint(isl) {
      const hint = U.el('div', { class: 'atlas-teleport', role: 'button', tabindex: '0',
        text: '↵ fly to “' + U.shortTitle(isl.name, 28) + '”', onclick: () => S.set({ island: isl.id, sel: null }),
        onkeydown: (e) => { if (e.key === 'Enter') S.set({ island: isl.id, sel: null }); } });
      board.appendChild(hint);
    }

    // ---- render dispatch ----
    function render() {
      drawCrumb();
      const st = S.get();
      const isl = st.island && idx.islandById[st.island];
      if (isl) renderL1(isl); else renderL0();
    }

    render();
    return {
      applyFilters: render,                // search-teleport / highlight
      onSelect: () => render(),            // L2 node selection re-renders with ego highlight
      onNav: () => render(),               // atlas/island hash changes
      destroy: () => {},
    };
  }
  return { label: 'Atlas', mount };
})();
