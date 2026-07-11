# -*- coding: utf-8 -*-
"""PHASE 4 (element layer) of the SWE corpus explorer build.

Consumes the committed element sources under build/element_src/ (the encoded form of the four
Phase 1-3 deliverables, exactly as records_*.py are the encoded form of the seven pass reports):
  design.json         <- design_elements_catalog_v1_0.md   (709 design elements)
  architecture.json   <- architecture_elements_catalog_v1_0.md (374 architecture elements)
  bridge.json         <- design_elements_bridge_v1_0.md      (1132 typed edges + unbridged list)
  pass8_works.json    <- design_elements_corpus_v1_0.md      (element -> work coverage)
and emits data/elements.json + data/elements.js (window.SWE.elements).

Two mechanical audits are printed and enforced:
  (a) COMPLETENESS  - built design/arch/edge counts must equal the deliverable .md census headers.
  (b) BRIDGING RULE - every design element carries >=1 cross-realm edge, or is on the unbridged
                      list; the without-list must be identical to the bridge report's.
"""
import json, os, io, sys, re, collections

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'element_src')
REPORTS = os.path.normpath(os.path.join(HERE, '..', '..'))   # SWE/  (the deliverable .md live here)

CROSS = {'realizes', 'enables'}          # design -> architecture
CROSS_REV = {'constrains'}               # architecture -> design
WITHIN = {'specializes', 'composes-with', 'alternative-to', 'uses'}   # within-realm ('uses' added in the atlas enrichment)
IMPL = {'implements'}                     # design -> design
EDGE_KINDS = CROSS | CROSS_REV | WITHIN | IMPL
REALM_LABEL = {'design': 'Design elements', 'architecture': 'Architecture elements'}


def _census(path, unit):
    """Pull the '**N elements**' / '**N edges**' figure from a deliverable header. None if absent."""
    try:
        txt = open(path, encoding='utf-8').read()
    except OSError:
        return None
    m = re.search(r'\*\*(\d+) ' + unit + r'\*\*', txt)
    return int(m.group(1)) if m else None


def run(DATA):
    load = lambda f: json.load(open(os.path.join(SRC, f), encoding='utf-8'))
    design = load('design.json')['elements']
    arch = load('architecture.json')['elements']
    bridge = load('bridge.json')
    pass8 = load('pass8_works.json')['works']

    # explorer corpus ids (works already carried as full corpus nodes)
    corpus_meta, corpus_ids = {}, set()
    try:
        for n in json.load(open(os.path.join(DATA, 'corpus.json'), encoding='utf-8'))['nodes']:
            corpus_ids.add(n['id'])
            corpus_meta[n['id']] = dict(id=n['id'], title=n['title'], authors=n.get('authors', ''),
                                        year=n.get('year', ''), verification=n.get('verification', 'unverified'),
                                        type=n.get('type', 'other'), corpusNode=True)
    except OSError:
        pass  # corpus.json not built yet — coverage still works, corpusNode flags default False

    # pass-8 work metadata + element -> works coverage (works' `elements` lists span both realms)
    work_meta, coverage = {}, collections.defaultdict(set)
    for w in pass8:
        work_meta[w['id']] = dict(id=w['id'], title=w.get('title', w['id']), authors=w.get('authors', ''),
                                  year=str(w.get('year', '')), verification=w.get('verification', 'unverified'),
                                  type=w.get('type', 'other'), corpusNode=w['id'] in corpus_ids)
        for eid in (w.get('elements') or []):
            coverage[eid].add(w['id'])

    def node_of(e, realm):
        works = set(coverage.get(e['id'], set()))
        if e.get('named_in_corpus_id'):
            works.add(e['named_in_corpus_id'])
        qa = [t.split(':', 1)[1] for t in (e.get('tags') or []) if t.startswith('qa:')]
        return dict(id=e['id'], name=e['name'], realm=realm, kind=e['kind'],
                    aka=e.get('aka') or [], what=e.get('what', ''), problem=e.get('problem', ''),
                    named_in=e.get('named_in', ''), named_in_corpus_id=e.get('named_in_corpus_id'),
                    tags=[t for t in (e.get('tags') or []) if not t.startswith('qa:')],
                    qa=qa, borderline=e.get('borderline'), confidence=e.get('confidence', 'established'),
                    works=sorted(works))

    nodes = [node_of(e, 'design') for e in design] + [node_of(e, 'architecture') for e in arch]
    node_ids = set()
    for n in nodes:
        if n['id'] in node_ids:
            raise SystemExit('FATAL: duplicate element id across realms: ' + n['id'])
        node_ids.add(n['id'])

    # edges (validate endpoints + kinds against the built node set)
    edges, bad = [], []
    for e in bridge['edges']:
        f, k, t = e.get('from'), e.get('kind'), e.get('to')
        if k not in EDGE_KINDS or f not in node_ids or t not in node_ids:
            bad.append(e); continue
        edges.append(dict(**{'from': f}, kind=k, to=t, provenance=e.get('provenance', 'editorial'),
                          cite=e.get('cite'), note=e.get('note', '')))
    if bad:
        raise SystemExit('FATAL: %d bridge edges reference unknown ids/kinds: %s' % (len(bad), bad[:5]))
    unbridged = [dict(id=u['id'], why=u.get('why', '')) for u in bridge.get('unbridged', [])]

    # works map (every work any element points at)
    referenced = set()
    for n in nodes:
        referenced.update(n['works'])
    works = {}
    for wid in referenced:
        works[wid] = corpus_meta.get(wid) or work_meta.get(wid) or dict(
            id=wid, title=wid, authors='', year='', verification='unverified', type='other', corpusNode=False)

    design_ids = {n['id'] for n in nodes if n['realm'] == 'design'}
    arch_ids = {n['id'] for n in nodes if n['realm'] == 'architecture'}
    designKinds = collections.Counter(n['kind'] for n in nodes if n['realm'] == 'design')
    archKinds = collections.Counter(n['kind'] for n in nodes if n['realm'] == 'architecture')
    sourced = sum(1 for e in edges if e['provenance'] == 'sourced')
    cross = [e for e in edges if e['kind'] in CROSS or e['kind'] in CROSS_REV]

    # ---- audit (a) COMPLETENESS: built counts vs deliverable .md census headers ----
    cens = {
        'design': _census(os.path.join(REPORTS, 'design_elements_catalog_v1_0.md'), 'elements'),
        'arch': _census(os.path.join(REPORTS, 'architecture_elements_catalog_v1_0.md'), 'elements'),
        'edges': _census(os.path.join(REPORTS, 'design_elements_bridge_v1_1.md'), 'edges'),
    }
    print('PHASE 4 (elements): %d design + %d architecture = %d elements; %d edges; %d works referenced.'
          % (len(design_ids), len(arch_ids), len(nodes), len(edges), len(works)))
    problems = []
    if cens['design'] is not None and cens['design'] != len(design_ids):
        problems.append('design %d built vs %d in catalog header' % (len(design_ids), cens['design']))
    if cens['arch'] is not None and cens['arch'] != len(arch_ids):
        problems.append('architecture %d built vs %d in catalog header' % (len(arch_ids), cens['arch']))
    if cens['edges'] is not None and cens['edges'] != len(edges):
        problems.append('edges %d built vs %d in bridge header' % (len(edges), cens['edges']))
    if problems:
        raise SystemExit('FATAL completeness mismatch: ' + '; '.join(problems))
    print('  completeness: built counts match the deliverable headers (design=%s, arch=%s, edges=%s).'
          % (cens['design'], cens['arch'], cens['edges']))

    # ---- audit (b) BRIDGING RULE ----
    bridged = {e['from'] for e in edges if e['kind'] in CROSS} | {e['to'] for e in edges if e['kind'] in CROSS_REV}
    unb_ids = {u['id'] for u in unbridged}
    missing = sorted(design_ids - bridged - unb_ids)
    false_unb = sorted(unb_ids & bridged)
    if missing:
        raise SystemExit('FATAL bridging: %d design elements neither bridged nor on the unbridged list: %s'
                         % (len(missing), missing[:15]))
    if false_unb:
        raise SystemExit('FATAL bridging: declared unbridged but has a cross edge: ' + ', '.join(false_unb))
    print('  bridging rule: %d/%d design elements have >=1 cross-realm edge; %d unbridged:'
          % (len(bridged), len(design_ids), len(unb_ids)))
    for u in unbridged:
        print('    - %s: %s' % (u['id'], u['why'][:90]))

    design_cov = sum(1 for n in nodes if n['realm'] == 'design' and n['works'])
    arch_cov = sum(1 for n in nodes if n['realm'] == 'architecture' and n['works'])
    meta = dict(designCount=len(design_ids), archCount=len(arch_ids), total=len(nodes),
                edgeCount=len(edges), crossRealm=len(cross), sourced=sourced, editorial=len(edges) - sourced,
                bridged=len(bridged), unbridgedCount=len(unb_ids),
                designCovered=design_cov, archCovered=arch_cov,
                designKinds=dict(designKinds), archKinds=dict(archKinds))

    out = dict(realms=REALM_LABEL, nodes=nodes, edges=edges, unbridged=unbridged, works=works, meta=meta)
    os.makedirs(DATA, exist_ok=True)
    with open(os.path.join(DATA, 'elements.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
    js = ('// GENERATED by build/build_elements.py - element layer (design + architecture realms).\n'
          'window.SWE = window.SWE || {};\nSWE.elements = ' + json.dumps(out, ensure_ascii=False) + ';\n')
    open(os.path.join(DATA, 'elements.js'), 'w', encoding='utf-8').write(js)
    print('  emitted data/elements.json + data/elements.js (%d nodes, %d edges, %d works; %d sourced : %d editorial).'
          % (len(nodes), len(edges), len(works), sourced, len(edges) - sourced))
    return out


if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    run(os.path.normpath(os.path.join(HERE, '..', 'data')))
