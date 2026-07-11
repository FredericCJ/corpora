// views/el_bridgeflow.js — Element view 11: THE BRIDGE-FLOW (shell). The faithful big picture of the
// cross-realm mapping: seven design FAMILIES on the left flow into the busiest ARCHITECTURE ANCHORS on
// the right, each ribbon a realizes/enables bundle whose thickness is how many design elements of that
// family land on that anchor. Hover a family or anchor to isolate its flows; click an anchor for its
// full detail in the inspector. Consumes the precomputed SWE.atlas.bridgeFlow; pure projection here.
window.SWE = window.SWE || {}; SWE.views = SWE.views || {};
SWE.views['el-bridgeflow'] = (function () {
  'use strict';
  const U = SWE.util, S = SWE.state;
  const W = 1000, LX = 232, RX = 792;               // viewBox width; family column x; anchor column x

  function mount(root, ctx) {
    const idx = ctx.atlasIndex, EL = ctx.elIndex;
    const bf = idx.bridgeFlow;
    const famHex = idx.familyHex, famName = idx.familyName;

    const vp = U.el('div', { class: 'vp' });
    const head = U.el('div', { class: 'vp-head' });
    head.appendChild(U.el('h2', { text: 'Bridge-Flow — design families → architecture anchors' }));
    head.appendChild(U.el('p', { class: 'note', text: 'Every ' +
      'design family (left) flows into the architecture elements it realizes or enables (right), busiest ' +
      'anchors first. Ribbon thickness = number of realizing design elements. Hover to isolate; click an ' +
      'anchor for its detail. This is the honest shape of the ' + bf.flows.reduce((a, f) => a + f.weight, 0) +
      '-edge realize/enable mapping.' }));
    const body = U.el('div', { class: 'vp-body' });
    const board = U.el('div', { class: 'board' });
    body.appendChild(board);
    vp.appendChild(head); vp.appendChild(body); root.appendChild(vp);

    const anchors = bf.anchors.slice();               // already sorted by total desc
    const H = Math.max(560, anchors.length * 18 + 40);
    const famTotal = {};
    for (const f of bf.flows) famTotal[f.from] = (famTotal[f.from] || 0) + f.weight;
    const fams = idx.families.filter((f) => famTotal[f.id]);      // only families that actually flow

    // y positions
    const famY = {}; fams.forEach((f, i) => { famY[f.id] = 40 + (H - 80) * (i + 0.5) / fams.length; });
    const ancY = {}; anchors.forEach((a, i) => { ancY[a.id] = 24 + (H - 48) * (i + 0.5) / anchors.length; });
    const maxFlow = Math.max(1, ...bf.flows.map((f) => f.weight));

    const svg = U.svg('svg', { viewBox: `0 0 ${W} ${H}`, preserveAspectRatio: 'xMidYMid meet',
      class: 'atlas-svg', role: 'img', 'aria-label': `Bridge-flow: ${fams.length} families into ${anchors.length} anchors` });
    const gRib = U.svg('g'), gFam = U.svg('g'), gAnc = U.svg('g');
    svg.appendChild(gRib); svg.appendChild(gFam); svg.appendChild(gAnc);

    // ribbons
    const ribs = [];
    for (const fl of bf.flows) {
      if (!(fl.from in famY) || !(fl.to in ancY)) continue;
      const y1 = famY[fl.from], y2 = ancY[fl.to];
      const d = `M${LX} ${y1} C ${(LX + RX) / 2} ${y1}, ${(LX + RX) / 2} ${y2}, ${RX} ${y2}`;
      const p = U.svg('path', { d, class: 'bf-ribbon', 'stroke-width': (1 + 4 * fl.weight / maxFlow).toFixed(2) });
      p.style.stroke = famHex[fl.from];
      p.dataset.fam = fl.from; p.dataset.anc = fl.to;
      gRib.appendChild(p); ribs.push(p);
    }
    function isolate(pred) { for (const p of ribs) { const on = pred(p); p.classList.toggle('hl', on); p.classList.toggle('mute', !on); } }
    function clearIso() { for (const p of ribs) p.classList.remove('hl', 'mute'); }

    // family nodes (left)
    for (const f of fams) {
      const y = famY[f.id];
      const g = U.svg('g', { class: 'bf-fam', tabindex: '0', role: 'button', 'aria-label': `${famName[f.id]} family, ${famTotal[f.id]} outgoing` });
      const r = U.svg('rect', { x: LX - 150, y: y - 13, width: 150, height: 26, rx: 6 });
      r.style.fill = f.hex; g.appendChild(r);
      const t = U.svg('text', { x: LX - 142, y: y + 4, class: 'bf-flabel' });
      t.textContent = U.shortTitle(famName[f.id], 22); g.appendChild(t);
      const c = U.svg('text', { x: LX - 6, y: y + 4, class: 'bf-fcount', 'text-anchor': 'end' });
      c.textContent = famTotal[f.id]; g.appendChild(c);
      const on = () => isolate((p) => p.dataset.fam === f.id), off = clearIso;
      g.addEventListener('mouseenter', on); g.addEventListener('mouseleave', off);
      g.addEventListener('focus', on); g.addEventListener('blur', off);
      gFam.appendChild(g);
    }

    // anchor nodes (right)
    for (const a of anchors) {
      const y = ancY[a.id];
      const g = U.svg('g', { class: 'bf-anc', tabindex: '0', role: 'button', 'aria-label': `${a.name}, ${a.kind}, ${a.total} realizing elements` });
      g.__id = a.id;
      const dot = U.svg('circle', { cx: RX, cy: y, r: 3.4 }); dot.style.fill = 'var(--re-arch, #6D4AA6)'; g.appendChild(dot);
      const t = U.svg('text', { x: RX + 9, y: y + 3.5, class: 'bf-alabel' });
      t.textContent = U.shortTitle(a.name, 34) + '  ·' + a.total; g.appendChild(t);
      const tip = U.svg('title'); tip.textContent = `${a.name} — architecture ${a.kind} · ${a.total} realizing design elements`; g.appendChild(tip);
      const on = () => isolate((p) => p.dataset.anc === a.id), off = clearIso;
      g.addEventListener('mouseenter', on); g.addEventListener('mouseleave', off);
      g.addEventListener('focus', on); g.addEventListener('blur', off);
      const go = (ev) => { ev.stopPropagation(); S.set({ sel: a.id }); };
      g.addEventListener('click', go);
      g.addEventListener('keydown', (e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); go(e); } });
      gAnc.appendChild(g);
    }

    board.replaceChildren(svg);
    // Selecting an anchor highlights it; its full detail surfaces in the persistent inspector.
    function onSelect(sel) { for (const g of gAnc.children) g.classList.toggle('sel', g.__id === sel); }
    onSelect(S.get().sel);
    return { applyFilters: () => {}, onSelect, destroy: () => {} };
  }
  return { label: 'Bridge-Flow', mount };
})();
