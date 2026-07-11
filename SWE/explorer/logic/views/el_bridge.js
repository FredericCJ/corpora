// views/el_bridge.js — Element view 2: the design↔architecture bridge map (shell). The mission-
// critical projection: which architecture elements anchor which design elements (cross-realm
// realizes/enables/constrains, grouped by architecture target via CE.bridgeByArch), busiest anchors
// first, plus the honest tail of 6 unbridged design elements. All grouping is pure in SWE.coreEl;
// this shell only projects to DOM, honours the global search, and wires selection. Internal scroll
// (.el-scroll) is authorized for element views.
window.SWE = window.SWE || {}; SWE.views = SWE.views || {};
SWE.views['el-bridge'] = (function () {
  'use strict';
  const U = SWE.util, CE = SWE.coreEl;

  function mount(root, ctx) {
    const idx = ctx.elIndex;
    const meta = CE.VIEWS['el-bridge'];
    const bridge = CE.bridgeByArch(idx);

    // stable, pre-sorted groups (busiest architecture anchors first); filtered per render.
    const groups = Object.keys(bridge)
      .map((archId) => ({ archId, node: idx.byId[archId], anchors: bridge[archId] }))
      .filter((g) => g.node)
      .sort((a, b) => b.anchors.length - a.anchors.length || a.node.name.localeCompare(b.node.name));

    const vp = U.el('div', { class: 'vp' });
    vp.appendChild(U.el('div', { class: 'vp-head' },
      U.el('h2', { text: 'Design↔Arch bridge' }),
      U.el('p', { class: 'note', text: meta.semantic + ' ' + meta.computed })));
    const body = U.el('div', { class: 'vp-body' });
    const scroll = U.el('div', { class: 'el-scroll' });
    body.appendChild(scroll); vp.appendChild(body); root.appendChild(vp);

    function selectFn(id) { return () => SWE.state.set({ sel: id }); }
    function keySelect(id) { return (ev) => { if (ev.key === 'Enter' || ev.key === ' ') { ev.preventDefault(); SWE.state.set({ sel: id }); } }; }
    function provSpan(p) { return U.el('span', { class: p === 'sourced' ? 'prov-s' : 'prov-e', text: p === 'sourced' ? 'sourced' : 'editorial' }); }

    function render() {
      const st = SWE.state.get();
      const q = st.q, sel = st.sel;
      const filtering = !!(q && q.trim());
      const vis = CE.visible(idx, q);
      scroll.replaceChildren();

      const m = idx.meta;
      scroll.appendChild(U.el('p', { class: 'el-legend',
        text: m.bridged + '/' + m.designCount + ' design elements bridged · ' + m.unbridgedCount
          + ' unbridged · ' + m.sourced + ' sourced : ' + m.editorial + ' editorial' }));

      const two = U.el('div', { class: 'el-two' });
      let shownGroups = 0;
      for (const g of groups) {
        const archMatch = vis.has(g.archId);
        const lines = (filtering && !archMatch) ? g.anchors.filter((a) => vis.has(a.from)) : g.anchors;
        if (filtering && !archMatch && lines.length === 0) continue;
        shownGroups++;

        const grp = U.el('div', { class: 'el-group' });
        const h3 = U.el('h3', { role: 'button', tabindex: '0', title: 'select architecture element',
          onclick: selectFn(g.archId), onkeydown: keySelect(g.archId) });
        h3.style.cursor = 'pointer';
        h3.appendChild(U.el('span', { class: 'nm', text: U.shortTitle(g.node.name, 46) }));
        U.elChips(g.node).forEach((c) => h3.appendChild(c));
        h3.appendChild(U.el('span', { class: 'chip', text: g.anchors.length + ' design' }));
        if (g.archId === sel) h3.style.outline = '2px solid var(--ink)';
        grp.appendChild(h3);

        for (const a of lines) {
          const dn = idx.byId[a.from];
          const line = U.el('div', { class: 'el-line', role: 'button', tabindex: '0', title: a.note || '',
            onclick: selectFn(a.from), onkeydown: keySelect(a.from) });
          if (a.from === sel) line.style.outline = '2px solid var(--ink)';
          line.appendChild(U.el('span', { class: 'nm', text: dn ? U.shortTitle(dn.name, 40) : a.from }));
          line.appendChild(U.el('span', { class: 'chip', text: a.kind }));
          line.appendChild(provSpan(a.provenance));
          grp.appendChild(line);
        }
        two.appendChild(grp);
      }
      scroll.appendChild(two);
      if (shownGroups === 0) scroll.appendChild(U.el('p', { class: 'empty', text: 'No bridged architecture anchors match the search.' }));

      // honest tail: the unbridged design elements, always visible (filtered by search).
      const ub = idx.unbridged.filter((u) => !filtering || vis.has(u.id));
      if (ub.length) {
        const grp = U.el('div', { class: 'el-group' });
        grp.appendChild(U.el('h3', {}, U.el('span', { class: 'nm', text: 'unbridged design elements (' + idx.unbridged.length + ')' })));
        for (const u of ub) {
          const dn = idx.byId[u.id];
          const line = U.el('div', { class: 'el-line', role: 'button', tabindex: '0',
            onclick: selectFn(u.id), onkeydown: keySelect(u.id) });
          if (u.id === sel) line.style.outline = '2px solid var(--ink)';
          line.appendChild(U.el('span', { class: 'nm', text: dn ? dn.name : u.id }));
          line.appendChild(U.el('span', { class: 'sub', text: u.why }));
          grp.appendChild(line);
        }
        scroll.appendChild(grp);
      }
    }

    render();
    return { applyFilters: render, onSelect: () => render(), destroy: () => {} };
  }
  return { label: 'Design↔Arch bridge', mount };
})();
