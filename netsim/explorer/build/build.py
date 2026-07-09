# -*- coding: utf-8 -*-
"""Build pipeline for the Network M&S corpus explorer.
PHASE 1: parse the two corpus reports (../..*.md) — the ONLY place report text is read.
         Unlike SWE/calculus, these reports are machine-regular entry lists, so the build parses
         them directly instead of hand-transcribing: zero transcription drift, and the reports
         stay the single source of truth.
PHASE 2: normalize tags, resolve identifiers, merge cross-corpus identity overlaps, derive
         reference edges (only from explicit flags, item-number citations, and identifier matches).
PHASE 3: structural verification (counts, vocabularies, section maps, edge endpoints).
PHASE 4: emission -> data/{corpus,relations}.{json,js} + data/corpus_report.md
Run:  python build.py   (from build/)  or  python build/build.py
"""
import json, os, re, sys, io, collections

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..'))
DATA = os.path.normpath(os.path.join(HERE, '..', 'data'))
os.makedirs(DATA, exist_ok=True)

GEN_MD = os.path.join(ROOT, 'MS_networks_systems_corpus_v1_0.md')
MAT_MD = os.path.join(ROOT, 'MATLAB_Simulink_network_MS_corpus_v1_0.md')

sys.path.insert(0, HERE)
import overlays as OV  # EDITORIAL overlay layer (maintainer-curated; validated in PHASE 3.5)

report = []
def log(line=''):
    report.append(line)
    print(line)
def fail(msg):
    log('FATAL: ' + msg)
    with open(os.path.join(DATA, 'corpus_report.md'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(report) + '\n')
    sys.exit(1)

# ─────────────────────────── fixed facts stated in the reports ───────────────────────────
# The anchor volume (GEN header, verbatim fields).
ANCHOR = dict(
    id='anchor', corpus=['gen'], item={'gen': 'anchor'}, section=0, quarantined=False,
    title='Modeling and Simulation of Computer Networks and Systems: Methodologies and Applications',
    cite='eds. M. S. Obaidat, F. Zarai, P. Nicopolitidis. Morgan Kaufmann/Elsevier, 2015. '
         'ISBN 978-0-12-800887-4. 964 pp. ACM GB 10.5555/2815512; ScienceDirect book DOI 10.1016/C2013-0-19024-1.',
    note='The anchor volume. Verification: VERIFIED [WEB 2026-07-09]. Six parts: (1) protocols & services, '
         '(2) performance evaluation, (3) modeling approaches, (4) simulation methodology, '
         '(5) next-gen wireless evaluation, (6) M&S for system security.',
    subfield=['other'], paradigm=[], type=['edited-volume'], stratum=None,
    recency='foundational', recencyRaw='foundational (2015, the corpus datum)',
    verification='verified-web', verRaw='verified[WEB]', year=2015, living=False,
    idents=['978-0-12-800887-4', '10.5555/2815512', '10.1016/C2013-0-19024-1'], overlapFlags=[],
)
ANCHOR_PARTS = [
    dict(key='p1', no=1, label='Protocols & services'),
    dict(key='p2', no=2, label='Performance evaluation'),
    dict(key='p3', no=3, label='Modeling approaches'),
    dict(key='p4', no=4, label='Simulation methodology'),
    dict(key='p5', no=5, label='Next-gen wireless evaluation'),
    dict(key='p6', no=6, label='M&S for system security'),
]
# §17 verdicts, quoted from the GEN coverage summary.
PART_VERDICTS = {
    'p2': 'Most durable — "the queueing/NC analytical core is intact, with TSN/deterministic '
          'networking as its most active current application."',
    'p4': 'Among the most superseded — "simulation tooling (ns-2 → ns-3/OMNeT++-INET ecosystems '
          'with dedicated annual venues)"; emulation now "a co-equal methodology rather than an afterthought."',
    'p5': 'Among the most superseded — "GPU-native, ML-integrated wireless simulation (Sionna) '
          'displacing MATLAB link-level tools."',
}
# GEN section -> (anchor-map column, relation phrase drawn from the section header).
GEN_SECTION_MAP = {
    1: ('meta', 'anchor citation neighborhood & editor lineage (PEOPLE route)'),
    2: ('p3', 'expansion axis: anchor Part 3'),
    3: ('p2', 'expansion axis: anchor Part 2'),
    4: ('p2', 'modern analytical frontier'),
    5: ('p4', 'expansion axis: anchor Part 4'),
    6: ('p4', "supersedes the anchor's ns-2 era"),
    7: ('p4', 'emulation vs simulation frontier'),
    8: ('p4', 'PADS at scale'),
    9: ('beyond', 'did not exist at anchor time'),
    10: ('beyond', 'entire subfield post-dates anchor'),
    11: ('p5', 'expansion axis: anchor Part 5'),
    12: ('beyond', 'expansion of "systems" scope'),
    13: ('p1', 'expansion axis: anchor Part 1 + post-2015 shift'),
    14: ('p6', 'expansion axis: anchor Part 6'),
    15: ('meta', "recall multipliers — sweep these, don't cite as single works"),
    16: ('beyond', 'joint network + per-station task/resource scheduling; systems-scope expansion'),
    17: ('quarantine', 'unverified / to confirm'),
}
SUBFIELDS = ['protocols-services', 'performance-evaluation', 'modeling-approaches',
             'simulation-methodology', 'next-gen-wireless', 'security', 'digital-twin',
             'ml-for-simulation', 'cloud-datacenter', 'sdn-nfv-p4', 'parallel-distributed-sim',
             'emulation-tooling', 'other', 'other(systems)']
PARADIGMS = ['discrete-event', 'wireless-system-level', 'link-phy-level',
             'analytical-control-fluid', 'co-simulation-interop', 'academic-simulators']
STRATA = ['mathworks-official', 'peer-reviewed', 'book', 'community', 'thesis', 'other']
RECENCIES = ['foundational', 'contemporary', 'current']
TYPES = ['book', 'edited-volume', 'survey/review', 'paper', 'standard', 'simulator-tool/doc',
         'dataset', 'course/lecture', 'thesis', 'other', 'paper+dataset']

VIEWS = {
    'anchor': dict(label='Anchor map',
                   semantic='The 2015 anchor volume’s six parts mapped against the corpus routes that '
                            'expand, supersede, or post-date them — the GEN report’s own organizing scheme.',
                   question='What happened to each part of the 2015 book — and what exists now that it could not contain?',
                   computed='Columns are the six anchor parts plus “beyond the anchor” and the meta routes; '
                            'section cards carry the headers’ own relation phrases; part verdicts quote the '
                            'coverage summary. Membership only — no inferred relations.'),
    'facets': dict(label='Facets',
                   semantic='The tag lattice both reports enforce scope with: subfield/paradigm × type/stratum '
                            '× recency × section.',
                   question='What exists about X, and how much of it can I actually cite?',
                   computed='Pure filtering over parsed tags; counts computed live. Combines with the global '
                            'search / verification / corpus filters.'),
    'timeline': dict(label='Chronology',
                     semantic='Publication strata around the 2015 anchor datum; living documentation and tools '
                              'form their own stratum.',
                     question='What is pre-anchor canon, what is post-anchor frontier, what is maintained?',
                     computed='Year parsed from each citation string (c.-years take the first year; ranges take '
                              'the start); continuous/maintained docs detected as LIVING; unparseable years fall '
                              'back to the entry’s own recency tag, labelled as such.'),
    'matlab': dict(label='MATLAB lens',
                   semantic='The tool-family intersection corpus: MATLAB/Simulink actually applied to network/'
                            'system M&S, organized by its six paradigms.',
                   question='Where is MATLAB/Simulink a real network-M&S vehicle — and where is it a minority tool?',
                   computed='Paradigm columns with stratum-coded cards; cross-corpus overlaps link into the '
                            'general corpus; the load-bearing packaging-migration note is carried verbatim.'),
    'triage': dict(label='Triage',
                   semantic='The reports’ verification discipline: verified[WEB] vs verified[TRAIN] vs the '
                            'unverified quarantine, plus coverage self-assessment.',
                   question='What may I cite downstream as-is, what must I re-verify, what is quarantined — '
                            'and where does recall thin?',
                   computed='Verification split computed from tags; quarantine cards carried verbatim with their '
                            '“to confirm” notes; coverage summaries quoted whole.'),
    'graph': dict(label='Overlays',
                  semantic='EDITORIAL typed-relation overlays over a curated subset: a didactic ground-up '
                           'reading order, and theory→applied transitive-specialization chains. Maintainer '
                           'judgment, not report fact — every edge carries its rationale.',
                  question='In what order do I read — and how does each theory become a runnable '
                           'multi-station model?',
                  computed='Levels/stages are hand-assigned in build/overlays.py; within-band order is a pure '
                           'barycenter pass; acyclicity and level-monotonicity are machine-checked at build '
                           'time; hover traces the transitive closure along overlay edges.'),
}

# ─────────────────────────── PHASE 1 — parse the reports ───────────────────────────
ENTRY_RE = re.compile(r'^(U?\d+)\.\s+\*\*(.+?)\*\*\s*—\s*(.*)$')
SECTION_RE = re.compile(r'^##\s+(\d+)\.\s+(.*)$')
TAG_RE = re.compile(r'`\{(.+?)\}`')
YEAR_RE = re.compile(r'\b(19[5-9]\d|20[0-2]\d)\b')
LIVING_RE = re.compile(r'continuous|ongoing|maintained|current release|current\.|annual', re.I)
DOI_RE = re.compile(r'\b10\.\d{4,9}/[^\s,;)\]]+')
ARXIV_RE = re.compile(r'arXiv:\d{4}\.\d{4,5}', re.I)
ISBN_RE = re.compile(r'ISBN[ :]*([\d][\d-]{8,})')

def parse_report(path, corpus_key):
    with open(path, encoding='utf-8') as f:
        lines = f.read().splitlines()
    sections, entries = [], []
    sec_no, sec_title = None, None
    for ln in lines:
        sm = SECTION_RE.match(ln)
        if sm:
            sec_no, sec_title = int(sm.group(1)), sm.group(2).strip()
            sections.append(dict(corpus=corpus_key, no=sec_no, title=sec_title))
            continue
        em = ENTRY_RE.match(ln)
        if not em or sec_no is None:
            continue
        item, title, rest = em.group(1), em.group(2), em.group(3)
        tm = TAG_RE.search(rest)
        if not tm:
            fail(f'{corpus_key} item {item}: no tag block')
        tags = [t.strip() for t in tm.group(1).split('|')]
        if len(tags) != 4:
            fail(f'{corpus_key} item {item}: expected 4 tag fields, got {len(tags)}: {tags}')
        cite = rest[:tm.start()].strip()
        note = rest[tm.end():].strip()
        note = re.sub(r'^—\s*', '', note)
        # strip markdown emphasis markers for display (content untouched; logged once in PHASE 1)
        title, cite, note = (s.replace('*', '').replace('`', '') for s in (title, cite, note))
        entries.append(dict(corpus=corpus_key, item=item, section=sec_no, title=title,
                            cite=cite, note=note, tags=tags))
    return sections, entries

def norm_verification(raw):
    if raw.startswith('verified[WEB]'):
        base = 'verified-web'
    elif raw.startswith('verified[TRAIN]'):
        base = 'verified-train'
    elif raw.startswith('unverified'):
        base = 'unverified'
    else:
        return None, raw
    qual = raw[len({'verified-web': 'verified[WEB]', 'verified-train': 'verified[TRAIN]',
                    'unverified': 'unverified'}[base]):].strip(' ,;-')
    return base, qual

def norm_recency(raw):
    # GEN U12 carries the report's own recall-gap marker '?' — an honest unknown, not an error.
    found = [r for r in RECENCIES if r in raw]
    return (found[0] if found else ('unknown' if raw.strip() == '?' else None)), raw

def split_multi(raw):
    return [p.strip() for p in re.split(r'\s*(?:\+|→)\s*', raw) if p.strip()]

def extract_idents(text):
    ids = []
    ids += [m.rstrip('.') for m in DOI_RE.findall(text)]
    ids += [m for m in ARXIV_RE.findall(text)]
    ids += ISBN_RE.findall(text)
    return ids

def extract_year(cite, title):
    if LIVING_RE.search(cite):
        return None, True
    m = YEAR_RE.search(cite) or YEAR_RE.search(title)
    return (int(m.group(1)) if m else None), False

log('# corpus_report.md — build + verification log (netsim explorer)')
log('')
log('Sources parsed directly (no hand transcription): `MS_networks_systems_corpus_v1_0.md`, '
    '`MATLAB_Simulink_network_MS_corpus_v1_0.md`. Collection date stated in both: 2026-07-09.')
log('')
log('## PHASE 1 — parse')
gen_sections, gen_entries = parse_report(GEN_MD, 'gen')
mat_sections, mat_entries = parse_report(MAT_MD, 'mat')
gen_n = [e for e in gen_entries if not e['item'].startswith('U')]
gen_u = [e for e in gen_entries if e['item'].startswith('U')]
mat_n = [e for e in mat_entries if not e['item'].startswith('U')]
mat_u = [e for e in mat_entries if e['item'].startswith('U')]
log(f'- GEN: {len(gen_n)} numbered entries + {len(gen_u)} quarantined across {len(gen_sections)} sections.')
log(f'- MAT: {len(mat_n)} numbered entries + {len(mat_u)} quarantined across {len(mat_sections)} sections.')
if len(gen_n) != 176 or len(gen_u) != 18:
    fail(f'GEN counts changed: expected 176+18, got {len(gen_n)}+{len(gen_u)} — reconcile with the report')
if len(mat_n) != 81 or len(mat_u) != 8:
    fail(f'MAT counts changed: expected 81+8, got {len(mat_n)}+{len(mat_u)}')
seq = [int(e['item']) for e in gen_n]
if seq != sorted(seq) or seq != list(range(1, 177)):
    fail('GEN numbering is not the contiguous 1..176 sequence')
if [int(e['item']) for e in mat_n] != list(range(1, 82)):
    fail('MAT numbering is not the contiguous 1..81 sequence')
log('- numbering contiguous in both reports (GEN 1..176, MAT 1..81).')
log('')

# ─────────────────────────── PHASE 2 — normalize + resolve ───────────────────────────
log('## PHASE 2 — normalize tags, resolve identifiers, merge overlaps')
nodes = []
qualifiers = []
for e in gen_entries + mat_entries:
    corpus = e['corpus']
    tags = e['tags']
    if corpus == 'gen':
        subf_raw, rec_raw, type_raw, ver_raw = tags
        paradigm, stratum = [], None
        subfield = split_multi(subf_raw)
        for s in subfield:
            if s not in SUBFIELDS and not s.startswith('other'):
                fail(f'gen {e["item"]}: unknown subfield {s!r}')
        typ = split_multi(type_raw)
    else:
        par_raw, strat_raw, rec_raw, ver_raw = tags
        paradigm = split_multi(par_raw)
        for p in paradigm:
            if p not in PARADIGMS and p != 'other':
                fail(f'mat {e["item"]}: unknown paradigm {p!r}')
        stratum = strat_raw
        if stratum not in STRATA:
            fail(f'mat {e["item"]}: unknown stratum {stratum!r}')
        subfield, typ = [], []
    ver, ver_qual = norm_verification(ver_raw)
    if ver is None:
        fail(f'{corpus} {e["item"]}: unparseable verification {ver_raw!r}')
    rec, rec_qual = norm_recency(rec_raw)
    if rec is None:
        fail(f'{corpus} {e["item"]}: unparseable recency {rec_raw!r}')
    if ver_qual:
        qualifiers.append(f'{corpus}{e["item"]}: verification qualifier “{ver_qual}”')
    quarantined = (corpus == 'gen' and e['section'] == 17) or (corpus == 'mat' and e['section'] == 9)
    year, living = extract_year(e['cite'], e['title'])
    overlap_flags = re.findall(r'\[GEN-CORPUS[^\]]*\]', e['cite'] + ' ' + e['note'])
    nodes.append(dict(
        id=('g' if corpus == 'gen' else 'm') + e['item'], corpus=[corpus],
        item={corpus: e['item']}, section=e['section'], title=e['title'], cite=e['cite'],
        note=e['note'], subfield=subfield, paradigm=paradigm, type=typ, stratum=stratum,
        recency=rec, recencyRaw=rec_raw, verification=ver, verRaw=ver_raw,
        year=year, living=living, quarantined=quarantined,
        idents=extract_idents(e['title'] + ' ' + e['cite']), overlapFlags=overlap_flags,
    ))
log(f'- tag vocabularies validated; {len(qualifiers)} verification qualifiers carried verbatim '
    '(e.g. “(draft); RFC status unverified”, “-single-source”).')

byid = {n['id']: n for n in nodes}

# Cross-corpus identity merges: an explicit [GEN-CORPUS item N] flag AND a shared hard identifier.
ident_index = collections.defaultdict(list)
for n in nodes:
    for i in n['idents']:
        ident_index[i].append(n['id'])
merges = []
for n in [x for x in nodes if x['corpus'] == ['mat']]:
    m_ids = set(n['idents'])
    for flag in n['overlapFlags']:
        im = re.search(r'item (\d+)', flag)
        if not im:
            continue
        g = byid.get('g' + im.group(1))
        if g and m_ids & set(g['idents']):
            merges.append((g['id'], n['id'], sorted(m_ids & set(g['idents']))[0], flag))
for gid, mid, ident, flag in merges:
    g, m = byid[gid], byid[mid]
    g['corpus'] = ['gen', 'mat']
    g['item']['mat'] = m['item']['mat']
    g['matTwin'] = dict(section=m['section'], cite=m['cite'], note=m['note'],
                        paradigm=m['paradigm'], stratum=m['stratum'])
    g['paradigm'] = m['paradigm']
    g['stratum'] = m['stratum']
    nodes.remove(m)
    del byid[mid]
    log(f'- MERGED {mid} into {gid} (shared identifier {ident}; flag {flag!r}); '
        'both citation strings carried.')
alias = {mid: gid for gid, mid, _, _ in merges}

# Derived edges — three explicit, groundable kinds only.
edges = []
def add_edge(s, t, kind, quote):
    s, t = alias.get(s, s), alias.get(t, t)
    if s == t or s not in byid or t not in byid:
        return
    if any(e for e in edges if e['s'] == s and e['t'] == t and e['kind'] == kind):
        return
    edges.append(dict(s=s, t=t, kind=kind, quote=quote))

ITEMREF_RE = re.compile(r'\bitems?\s+(\d+)(?:\s*[–-]\s*(\d+))?')
for n in list(byid.values()):
    text = n['note'] + ' ' + n['cite']
    own = n['corpus'][0]
    # (a) explicit overlap flags with item numbers -> overlaps edge (unless merged)
    for flag in n['overlapFlags']:
        for im in ITEMREF_RE.finditer(flag):
            add_edge(n['id'], 'g' + im.group(1), 'overlaps', flag)
    # (b) plain “item N” references -> mentions (resolved within the referencing corpus,
    #     except numbers beyond MAT's 61 items, which can only be GEN); overlap-flag text is
    #     removed first so a flag does not also count as a mention
    for flag in n['overlapFlags']:
        text = text.replace(flag, ' ')
    for im in ITEMREF_RE.finditer(text):
        lo = int(im.group(1)); hi = int(im.group(2)) if im.group(2) else lo
        if hi - lo > 12:
            continue
        for k in range(lo, hi + 1):
            pref = 'g' if (own == 'gen' or k > 61) else 'm'
            add_edge(n['id'], pref + str(k), 'mentions', im.group(0))
    # (c) an identifier of another entry appearing in this entry's text -> named-in
    for ident, owners in ident_index.items():
        if len(ident) < 10:
            continue
        if ident in text and n['id'] not in owners:
            for o in owners:
                add_edge(n['id'], o, 'named-in', ident)
log(f'- derived edges: {len(edges)} '
    f"({collections.Counter(e['kind'] for e in edges)}) — from explicit flags, item-number "
    'references, and shared hard identifiers only; no semantic inference.')
log('')

# ─────────────────────────── PHASE 3 — structural verification ───────────────────────────
log('## PHASE 3 — structural verification')
for sec in gen_sections:
    if sec['no'] not in GEN_SECTION_MAP and sec['no'] <= 17:
        fail(f'GEN section {sec["no"]} missing from the anchor map')
vc = collections.Counter(n['verification'] for n in nodes)
qc = sum(1 for n in nodes if n['quarantined'])
log(f"- verification split: {vc['verified-web']} verified[WEB] / {vc['verified-train']} verified[TRAIN] "
    f"/ {vc['unverified']} unverified; {qc} entries live in the quarantine sections (§17 GEN / §9 MAT).")
bad_q = [n['id'] for n in nodes if n['quarantined'] and n['verification'] != 'unverified'
         and 'single-source' not in n['verRaw'] and 'unverified' not in n['verRaw']]
if bad_q:
    log(f'- NOTE: quarantined entries carrying a verified tag: {bad_q} (the reports themselves '
        'do this for single-source/detail cases; carried as stated).')
year_ok = sum(1 for n in nodes if n['year'])
living = sum(1 for n in nodes if n['living'])
log(f'- chronology: {year_ok} entries with a parsed year, {living} living (continuous/maintained), '
    f'{len(nodes) - year_ok - living} undated (fall back to their recency tag in the timeline).')
multi_par = [n['id'] for n in nodes if len(n['paradigm']) > 1]
log(f'- multi-paradigm MAT entries (split of “+/→” tags): {multi_par}.')
for e in edges:
    if e['s'] not in byid or e['t'] not in byid:
        fail(f'edge endpoint missing: {e}')
log('- all edge endpoints resolve; merged aliases rewritten.')
log('')

# ─────────────────── PHASE 3.5 — EDITORIAL overlays (validated, never inferred) ───────────────────
log('## PHASE 3.5 — editorial overlays')
overlays_out = []
for ov in OV.OVERLAYS:
    level_ix = {lv['key']: i for i, lv in enumerate(ov['levels'])}
    members = ov['members']
    for nid, lv in members.items():
        if nid not in byid:
            fail(f"overlay {ov['id']}: member {nid} is not a corpus node (check post-merge ids)")
        if lv not in level_ix:
            fail(f"overlay {ov['id']}: member {nid} has unknown level {lv}")
        if byid[nid]['quarantined']:
            fail(f"overlay {ov['id']}: member {nid} is quarantined — overlays may not launder "
                 'unverified entries into reading maps')
    indeg = {nid: 0 for nid in members}
    down = collections.defaultdict(list)
    seen_pairs = set()
    same_level = []
    for s, t, why in ov['edges']:
        if s not in members or t not in members:
            fail(f"overlay {ov['id']}: edge {s}->{t} endpoint not a member")
        if (s, t) in seen_pairs:
            fail(f"overlay {ov['id']}: duplicate edge {s}->{t}")
        seen_pairs.add((s, t))
        if not why:
            fail(f"overlay {ov['id']}: edge {s}->{t} missing its rationale")
        if level_ix[members[s]] > level_ix[members[t]]:
            fail(f"overlay {ov['id']}: edge {s}->{t} points to an EARLIER level")
        if members[s] == members[t]:
            same_level.append(f'{s}→{t}')
        indeg[t] += 1
        down[s].append(t)
    queue = sorted([n for n, d in indeg.items() if d == 0])
    topo, indeg2 = [], dict(indeg)
    while queue:
        cur = queue.pop(0)
        topo.append(cur)
        for nxt in sorted(down[cur]):
            indeg2[nxt] -= 1
            if indeg2[nxt] == 0:
                queue.append(nxt)
        queue.sort()
    if len(topo) != len(members):
        fail(f"overlay {ov['id']}: CYCLE — topological sort placed only {len(topo)}/{len(members)} members")
    orphans = [n for n in members if not down[n] and indeg[n] == 0]
    if orphans:
        fail(f"overlay {ov['id']}: members with no edges at all: {orphans}")
    per_level = collections.Counter(members.values())
    log(f"- {ov['id']}: {len(members)} members / {len(ov['edges'])} edges — ACYCLIC (Kahn over all "
        f"members), level-monotone; per level: "
        + ', '.join(f"{lv['key']}:{per_level.get(lv['key'], 0)}" for lv in ov['levels'])
        + (f"; same-level edges: {', '.join(same_level)}" if same_level else '') + '.')
    overlays_out.append(dict(id=ov['id'], label=ov['label'], edgeKind=ov['edgeKind'],
                             semantic=ov['semantic'], question=ov['question'], levels=ov['levels'],
                             members=members,
                             edges=[dict(s=s, t=t, why=why) for s, t, why in ov['edges']]))
log(f'- provenance stamped on both overlays: {OV.PROVENANCE!r}')
log('')

# ─────────────────────────── PHASE 4 — emission ───────────────────────────
log('## PHASE 4 — emission')
# coverage summaries: carried as verbatim paragraph blocks
def tail_section(path, header):
    with open(path, encoding='utf-8') as f:
        txt = f.read()
    m = re.search(r'^##\s+\d+\.\s+' + re.escape(header) + r'\s*$(.*)\Z', txt, re.M | re.S)
    if not m:
        fail(f'coverage section {header!r} not found in {os.path.basename(path)}')
    paras = [p.strip().replace('*', '') for p in m.group(1).split('\n\n')
             if p.strip() and not p.strip().startswith('---')]
    return paras
gen_cov = tail_section(GEN_MD, 'Coverage summary')
mat_cov = tail_section(MAT_MD, 'Coverage summary')
log(f'- coverage summaries carried verbatim: GEN {len(gen_cov)} blocks, MAT {len(mat_cov)} block(s).')

nodes_out = [ANCHOR] + nodes
corpus_obj = dict(
    phase='fact layer — parsed directly from the two corpus reports by build.py',
    meta=dict(title='Modeling & Simulation of Computer Networks and Systems — unified corpus',
              collected='2026-07-09', compiled='2026-07',
              sources={'gen': 'MS_networks_systems_corpus_v1_0.md',
                       'mat': 'MATLAB_Simulink_network_MS_corpus_v1_0.md'}),
    corpora=dict(
        gen=dict(label='Networks & systems M&S (anchor corpus)',
                 rule='collect-don’t-exclude; scope enforced by tags'),
        mat=dict(label='MATLAB/Simulink tool-family (intersection corpus)',
                 rule='intersection corpus; overlaps flagged [GEN-CORPUS]',
                 packagingNote='Product-packaging note (verified live, load-bearing for anti-fabrication): '
                     'the multinode wireless network simulation capability has migrated across packagings. '
                     'It shipped as the Communications Toolbox Wireless Network Simulation Library add-on '
                     '(File Exchange, compatible R2023a–R2025b), whose functionality the '
                     'wirelessNetworkSimulator reference page now describes as previously add-on-delivered; '
                     'MathWorks currently also markets a dedicated Wireless Network Toolbox product. Cite '
                     'the doc pages rather than asserting any “since RXXXXx” claim.')),
    anchorParts=ANCHOR_PARTS,
    subfields=SUBFIELDS, paradigms=PARADIGMS, strata=STRATA, recencies=RECENCIES,
    sections=dict(gen=gen_sections, mat=mat_sections),
    nodes=nodes_out,
)
relations_obj = dict(
    kinds=['overlaps', 'mentions', 'named-in'],
    edges=edges,
    anchorMap=[dict(part=p, sections=[dict(no=no, relation=rel) for no, (pp, rel) in
                                      sorted(GEN_SECTION_MAP.items()) if pp == p],
                    verdict=PART_VERDICTS.get(p))
               for p in ['p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'beyond', 'meta', 'quarantine']],
    coverage=dict(gen=gen_cov, mat=mat_cov),
    overlays=overlays_out,
    overlayProvenance=OV.PROVENANCE,
    verificationLegend={
        'verified-web': 'confirmed live on 2026-07-09 via search/primary source',
        'verified-train': 'high-confidence training-derived knowledge of existence — re-verify '
                          'identifiers before downstream citation',
        'unverified': 'plausible but unconfirmed; quarantined — do not cite downstream without '
                      'live verification',
    },
    views=VIEWS,
)

def emit(name, ns, obj):
    js = json.dumps(obj, ensure_ascii=False, separators=(', ', ': '))
    with open(os.path.join(DATA, name + '.json'), 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
        f.write('\n')
    with open(os.path.join(DATA, name + '.js'), 'w', encoding='utf-8') as f:
        f.write(f'// GENERATED by build/build.py — do not hand-edit. JSON twin: {name}.json\n')
        f.write('window.NET = window.NET || {};\n')
        f.write(f'NET.{ns} = {js};\n')
    log(f'- wrote data/{name}.json + data/{name}.js')

emit('corpus', 'corpus', corpus_obj)
emit('relations', 'relations', relations_obj)
log('')
log(f'Totals: {len(nodes_out)} nodes (1 anchor + {len(nodes)} entries after {len(merges)} merges) · '
    f'{len(edges)} derived edges · {len(gen_sections)}+{len(mat_sections)} sections · '
    f"{vc['verified-web']}/{vc['verified-train']}/{vc['unverified']} web/train/unverified.")
with open(os.path.join(DATA, 'corpus_report.md'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(report) + '\n')
print('\nOK — build complete.')
