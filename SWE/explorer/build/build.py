# -*- coding: utf-8 -*-
"""Build pipeline for the SWE corpus explorer.
PHASE 1: union + merge of per-report fact records -> data/corpus.json (raw) + data/corpus_report.md
PHASE 2: tag-vocabulary reconciliation (logged)   -> data/corpus.json (final) + data/adjustments.md
PHASE 3: typed edges + view definitions           -> data/relations.json + data/corpus.js + data/relations.js
Run:  python build.py   (from the build/ directory)
"""
import json, os, sys, collections, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, '..', 'data'))
os.makedirs(DATA, exist_ok=True)

import records_sa, records_arch, records_c, records_cpp, records_ops, records_sim
SOURCES = [('swa-science', records_sa.R), ('emb-arch', records_arch.R), ('emb-c', records_c.R),
           ('emb-cpp', records_cpp.R), ('emb-ops', records_ops.R), ('simulink', records_sim.R)]
CORPUS_LABELS = {
    'swa-science': 'Software architecture as a science',
    'emb-arch': 'Embedded architecture & design',
    'emb-c': 'Embedded C design',
    'emb-cpp': 'Embedded C++ design',
    'emb-ops': 'Embedded C/C++ operational use',
    'simulink': 'Large Simulink/MATLAB projects',
}
# Lead-memberships: reports list these works as (unverified) leads that merge into a node
# already carried verified by another corpus. (id, corpus-that-listed-the-lead, note)
MERGE_MEMBERSHIP = [
    ('shawgarlan96','emb-arch','general-classics lead in emb-arch (unverified there; verified by swa-science)'),
    ('tmd','emb-arch','general-classics lead in emb-arch'),
    ('kruchten','emb-arch','general-classics lead in emb-arch'),
    ('rozanski','emb-arch','general-classics lead in emb-arch'),
    ('vab','emb-arch','general-classics lead in emb-arch'),
    ('parnas72','emb-arch','Parnas modularity papers lead in emb-arch'),
    ('parnas72','emb-c','modularization-roots lead in emb-c'),
    ('meyerseffcpp','emb-arch','general-classics lead in emb-arch (verified by emb-cpp)'),
    ('meyerseffmod','emb-arch','general-classics lead in emb-arch (verified by emb-cpp)'),
    ('white','emb-cpp','2nd-ed lead in emb-cpp (verified by emb-arch)'),
    ('white','emb-c','lead in emb-c'),
    ('lacamera','emb-cpp','2nd-ed lead in emb-cpp (verified by emb-arch)'),
    ('beningodesign','emb-c','lead in emb-c (verified by emb-arch)'),
    ('beningofw','emb-c','lead in emb-c (verified by emb-arch)'),
    ('noblesmallmem','emb-c','lead in emb-c (verified by emb-arch, 2000)'),
    ('jplstd','emb-arch','flight-software-standard lead in emb-arch (verified by emb-c)'),
    ('drepperlibs','emb-ops','ops unverified lead (verified by emb-c)'),
    ('sakscolumns','emb-c','embedded.com column lead in emb-c (also emb-cpp lead)'),
    ('lakoslsc','emb-c','physical-design-roots lead in emb-c'),
    ('martincleanarch','emb-c','lead in emb-c'),
]
merge_log, conflict_log = [], []

# ---------------- PHASE 1 — union + merge ----------------
nodes = collections.OrderedDict()
raw_total = 0
for cname, recs in SOURCES:
    for r in recs:
        raw_total += 1
        rid = r['id']
        if rid not in nodes:
            nodes[rid] = dict(id=rid, title=r['title'], authors=r['authors'], year=r['year'],
                              rtype=r['rtype'], verification=r['verification'], note=r['note'],
                              ident=r['ident'], unresolved=list(r['unresolved']),
                              corpora=[r['corpus']], per={r['corpus']: r['raw']})
        else:
            nd = nodes[rid]
            nd['corpora'].append(r['corpus'])
            nd['per'][r['corpus']] = r['raw']
            merge_log.append(f"{rid}: merged {r['corpus']} record into existing node ({'+'.join(nd['corpora'][:-1])})")
            if r['verification'] == 'verified' and nd['verification'] == 'unverified':
                nd['verification'] = 'verified'
                merge_log.append(f"{rid}: verification promoted to verified (verified in {r['corpus']})")
            if r['year'] != nd['year'] and 'UNRESOLVED' not in (r['year'], nd['year']):
                conflict_log.append(f"{rid}: year differs across reports ({nd['year']} vs {r['year']} in {r['corpus']}); kept {nd['year']}, noted")
                nd['note'] = (nd['note'] + f" | Year cited as {r['year']} by {r['corpus']} report").strip(' |')
            if r['note'] and r['note'] not in nd['note']:
                nd['note'] = (nd['note'] + ' | ' + r['note']) if nd['note'] else r['note']
            if r['ident'] and not nd['ident']:
                nd['ident'] = r['ident']
for rid, cname, why in MERGE_MEMBERSHIP:
    if rid not in nodes:
        conflict_log.append(f"MERGE_MEMBERSHIP target missing: {rid}"); continue
    nd = nodes[rid]
    if cname not in nd['corpora']:
        nd['corpora'].append(cname)
        nd['per'][cname] = dict(lead=True)
        merge_log.append(f"{rid}: +{cname} membership — {why}")

multi = [n for n in nodes.values() if len(n['corpora']) > 1]
per_corpus = collections.Counter(c for n in nodes.values() for c in n['corpora'])
ver_count = collections.Counter(n['verification'] for n in nodes.values())

with open(os.path.join(DATA, 'corpus.json'), 'w', encoding='utf-8') as f:
    json.dump(dict(phase=1, nodes=list(nodes.values())), f, indent=1, ensure_ascii=False)

rep = ['# Corpus report — PHASE 1 (scrutiny of the six SWE reports)', '',
       f'Raw records transcribed: **{raw_total}** -> merged into **{len(nodes)}** unique nodes.',
       f'Verification: {ver_count["verified"]} verified / {ver_count["unverified"]} unverified (state preserved from reports; any-verified wins on merge).', '',
       '## Nodes per corpus (after merge; a node may belong to several)']
for c, label in CORPUS_LABELS.items():
    rep.append(f'- {c} — {label}: {per_corpus[c]}')
rep += ['', f'## Cross-corpus works: {len(multi)} nodes appear in >=2 corpora', '']
rep += [f"- {n['id']} ({', '.join(n['corpora'])}): {n['title'][:90]}" for n in sorted(multi, key=lambda x:-len(x['corpora']))]
rep += ['', '## Merges & promotions performed', ''] + [f'- {m}' for m in merge_log]
rep += ['', '## Conflicts / discrepancies', ''] + ([f'- {c}' for c in conflict_log] or ['- none'])
rep += ['', '## Tag coverage & gaps',
        '- swa-science: cluster/branch/tier/OA on all nodes.',
        '- emb-arch: branch/embedded_relevance/hw_sw_boundary on all; NO theme facet stated (filled in PHASE 2 from report section headings).',
        '- emb-c / emb-cpp: theme/level on all; no tier facet.',
        '- emb-ops: tier(trunk|c-leaf|cpp-leaf)/theme/KEY on all.',
        '- simulink: branch/cluster/role/automotive on all.',
        '- Access/openness only systematically recorded by swa-science (OA flags); elsewhere present in notes only — NOT lifted into a facet (would require re-verification).',
        '- Fields the source flags as unknown carry UNRESOLVED (years of some leads; two swa anchor papers).']
open(os.path.join(DATA, 'corpus_report.md'), 'w', encoding='utf-8').write('\n'.join(rep) + '\n')
print(f'PHASE 1: {raw_total} records -> {len(nodes)} nodes; {len(multi)} multi-corpus; report written.')

# ---------------- PHASE 2 — vocabulary reconciliation ----------------
adj = ['# Adjustments log — PHASE 2 (tag reconciliation)', '',
       'Rules: facts only; a gap is filled ONLY when unambiguously derivable from the record/report itself,',
       'else the field is UNRESOLVED (source says unknown) or absent (source never asserts the facet).', '']

TYPE_MAP = {'guide':'guide','technical-guide':'guide','course':'course','course/lecture':'course',
            'official-doc':'official-doc','tooling-doc':'tooling-doc','standard':'standard','book':'book',
            'paper':'paper','report':'report','blog':'blog','other':'other'}
SA_BRANCH = {'A':'architecture','B':'process','S':'evaluation'}
SA_THEME = {'A1':'foundations','A2':'views-description','A3':'adl-formal','A4':'model-checking',
            'A5':'self-adaptive','A6':'evolution','A7':'reference-architectures','B1':'design-science',
            'B2':'design-methods','B3':'rationale-akm','B4':'empirical-reasoning','S1':'evaluation-methods',
            'S2':'quality-models','S3':'economics-debt'}
SIM_THEME = {'D1':'modeling-style','D2':'block-patterns','D3':'data-typing','D4':'code-generation',
             'D5':'model-quality','A1':'componentization','A2':'interfaces','A3':'model-architecture',
             'A4':'system-architecture','A-shared':'code-architecture','M1':'version-control',
             'M2':'ci-verification','M3':'traceability','M4':'governance-metrics','M5':'program-management',
             'M6':'certification'}
# emb-arch has no theme facet; derived from the report's own section headings (logged below).
ARCH_THEME = {}
def at(theme, ids):
    for i in ids.split(): ARCH_THEME[i] = theme
at('system-architecture','kopetz leeseshia marwedel wolf5 noergaard lacamera ledin oshana beningodesign white tinyos vahidgivargis gajski peckol berger heath ball siewert bertolotti barrycrowley walls kopetzbauer henzingersifakis leecps svincentelli lakoslsc')
at('domain-architecture','staron broy pretschner fuerst schaeuffele omgspecs eastadl ros2design cloudiotref iira rami40 px4ardu')
at('scheduling','buttazzo burnswellings liulayland laplante janeliu cooling liyao fanrt wangrt')
at('safety-standards','iso26262 do178c iec61508 iec62304 en50128 ecss')
at('os-platform','autosarclassic autosaradaptive arinc653 sel4 l4liedtke contiki protothreads nesc riot freertosbook zephyrdocs qnxguide vxthreadx')
at('design-patterns','pont room hatleypirbhai wardmellor douglassagility douglassrtcorpus posa2 posa3 hanmer nygard gof fowlerref')
at('concurrency-design','gomaa')
at('memory-management','noblesmallmem')
at('safety-critical-dev','hobbs rierson marscode dvorak levesonesw levesonsafeware storey avizienis rushby')
at('drivers-os','ldd3 hallinan yaghmour molloy embeddedrust espidf nordicacademy labrosse dsimonprimer ganssle')
at('vendor-platform','cmsis furber sloss catsoulis')
at('empirical-practice','graaf ebertjones liggesmeyer')
at('foundations','richardsford martincleanarch ousterhout beningofw')
at('coding-style','mcconnell martincleancode pragprog')
ARCH_NO_THEME = ['memfaultea']  # grouped-lead bullet, no thematic section — stays UNRESOLVED

adj.append('## Vocabulary mappings applied (every application logged by class, not per-node, for readability)')
adj += ['- TYPE: technical-guide->guide; course/lecture->course; journal->paper (none present after transcription); all others kept.',
        '- BRANCH: swa A->architecture, B->process, S->evaluation; emb-arch architecture/design kept; '
        'emb-c/emb-cpp level design->design branch, arch-realization->architecture branch (per the reports’ own routing rule); '
        'emb-ops (all)->operations; simulink architecture/design/management kept.',
        '- THEME: swa clusters mapped A1..S3 -> named themes; simulink clusters D1..M6 -> named themes; '
        'emb-c/emb-cpp/emb-ops themes kept (names normalized); emb-arch themes FILLED from report section headings (gap-fill, logged per node below).',
        '- ROLE: swa tier flags (star/C/A/pilcrow) -> anchor/core/advanced/survey; simulink target/core/advanced/survey kept; '
        'emb-ops KEY flags -> anchor; emb-arch/emb-c/emb-cpp assert no tier -> role absent (NOT UNRESOLVED: never claimed).',
        '- LANE (emb-ops only): trunk | c-leaf | cpp-leaf kept as a dedicated facet.',
        '- SCOPE: only emb-arch asserts embedded_relevance; kept for those nodes only.',
        '- ACCESS: only swa-science asserts OA systematically; kept for those nodes only.', '']
adj.append('## emb-arch theme gap-fills (derived from the report’s section headings)')
for i, th in sorted(ARCH_THEME.items()):
    adj.append(f'- {i}: theme={th} (from section heading)')
adj.append('- memfaultea: theme UNRESOLVED (grouped bullet outside any thematic section)')
adj.append('')

for nd in nodes.values():
    branches, themes, role, lane, scope, access, auto = set(), set(), set(), None, None, None, False
    for c, raw in nd['per'].items():
        if raw.get('lead'): continue
        if c == 'swa-science':
            branches.add(SA_BRANCH[raw['branch']]); themes.add(SA_THEME[raw['cluster']])
            tf = raw['tier']
            if 't' in tf: role.add('anchor')
            if 's' in tf: role.add('survey')
            if 'c' in tf: role.add('core')
            if 'a' in tf: role.add('advanced')
            access = {'yes':'open','partial':'partial','no':'paywalled'}[raw['oa']]
        elif c == 'emb-arch':
            branches.add(raw['branch'])
            if nd['id'] in ARCH_THEME: themes.add(ARCH_THEME[nd['id']])
            elif nd['id'] in ARCH_NO_THEME: themes.add('UNRESOLVED')
            scope = raw['embedded_relevance']
        elif c in ('emb-c','emb-cpp'):
            branches.add('architecture' if raw['level']=='arch-realization' else 'design')
            themes.add(raw['theme'])
        elif c == 'emb-ops':
            branches.add('operations'); lane = raw['tier']
            for th in raw['theme'].split(';'): themes.add(th)
            if raw.get('key'): role.add('anchor')
        elif c == 'simulink':
            branches.add(raw['branch']); themes.add(SIM_THEME[raw['cluster']])
            for rr in raw['role'].split(';'):
                role.add({'target':'anchor'}.get(rr, rr))
            if raw.get('automotive'): auto = True
    nd['type'] = TYPE_MAP[nd['rtype']]
    nd['branches'] = sorted(branches); nd['themes'] = sorted(themes)
    nd['role'] = sorted(role); nd['lane'] = lane; nd['scope'] = scope
    nd['access'] = access; nd['automotive'] = auto
    if nd['year'] == 'UNRESOLVED' and 'year' not in nd['unresolved']:
        nd['unresolved'].append('year')
    del nd['rtype']

with open(os.path.join(DATA, 'corpus.json'), 'w', encoding='utf-8') as f:
    json.dump(dict(phase=2, corpora=CORPUS_LABELS, nodes=list(nodes.values())), f, indent=1, ensure_ascii=False)
unres = [n for n in nodes.values() if n['unresolved']]
adj += ['## UNRESOLVED inventory (source-flagged unknowns, rendered as such in the UI)', ''] + \
       [f"- {n['id']}: {', '.join(n['unresolved'])}" for n in unres] + \
       ['', '## Notable fact fixes carried from the reports themselves',
        '- Taylor-Medvidovic-Dashofy: single edition only (swa report verification).',
        '- Deissenboeck et al.: ICSE 2008, not 2009 (simulink report correction).',
        '- Fagan 1976: IBM Systems Journal vol. 15, not 38 (emb-c report correction).',
        '- pi-ADL: SIGSOFT SEN 29(3), not 28(8) (swa report correction).',
        '- MAB "v6.0" does not exist; v6.0 is a JMAAB version (simulink report correction).',
        '- Douglass Design Patterns for Embedded Systems in C: emb-arch cites 2011, emb-c cites 2010 — kept 2011 printing note (see conflicts).']
open(os.path.join(DATA, 'adjustments.md'), 'w', encoding='utf-8').write('\n'.join(adj) + '\n')
print(f'PHASE 2: normalized {len(nodes)} nodes; {len(unres)} carry UNRESOLVED fields; adjustments.md written.')

# ---------------- PHASE 3 — relations ----------------
import edges as edgemod
E = edgemod.E
bad = [ed for ed in E if ed['s'] not in nodes or ed['t'] not in nodes]
if bad:
    print('FATAL: edges reference unknown nodes:', [(b['s'],b['t']) for b in bad]); sys.exit(1)
kinds = sorted({ed['kind'] for ed in E})
srcs = collections.Counter(ed['src'] for ed in E)
views = dict(
    graph=dict(label='Reading graph', semantic='Typed directed relations between works (may contain cycles)',
               question='What should I read before/after/with this work, and why?',
               computed='All edges below; nodes = every node with >=1 edge; columns grouped by corpus, rows by year (living docs pinned to a top band); provenance per edge: report / derived / editorial.'),
    facets=dict(label='Facet browser', semantic='Classification lattice: corpus x branch x theme x type (+ verification, role, lane)',
                question='What exists about X, and how much of it is verified?',
                computed='Pure filtering over node tags produced in PHASE 2; counts computed live.'),
    timeline=dict(label='Chronology', semantic='Ordering by year of last publication; living documents form their own stratum',
                  question='How did the field accumulate; what is maintained vs frozen?',
                  computed='parse leading 4-digit year; UNRESOLVED and living pinned to labelled bands.'),
    overlap=dict(label='Cross-corpus overlap', semantic='Works claimed by more than one research pass',
                 question='Which works bind the corpora together (the graft points)?',
                 computed='nodes with |corpora| >= 2, grouped by membership signature.'),
    anchors=dict(label='Anchors & spine', semantic='Curated per-corpus entry points: anchor/target/KEY-flagged nodes',
                 question='Where do I start in each corpus?',
                 computed="nodes whose role includes 'anchor' (swa stars, simulink targets, ops KEY flags), grouped by corpus."))
with open(os.path.join(DATA, 'relations.json'), 'w', encoding='utf-8') as f:
    json.dump(dict(kinds=kinds, provenance=dict(srcs), edges=E, views=views), f, indent=1, ensure_ascii=False)

# ---------------- emit JS data modules (file:// friendly) ----------------
corpus_js = ('// GENERATED by build/build.py — fact layer. Do not hand-edit.\n'
             'window.SWE = window.SWE || {};\n'
             'SWE.corpus = ' + json.dumps(dict(corpora=CORPUS_LABELS, nodes=list(nodes.values())),
                                          ensure_ascii=False) + ';\n')
open(os.path.join(DATA, 'corpus.js'), 'w', encoding='utf-8').write(corpus_js)
rel_js = ('// GENERATED by build/build.py — inference layer (typed edges + view definitions).\n'
          'window.SWE = window.SWE || {};\n'
          'SWE.relations = ' + json.dumps(dict(kinds=kinds, edges=E, views=views), ensure_ascii=False) + ';\n')
open(os.path.join(DATA, 'relations.js'), 'w', encoding='utf-8').write(rel_js)
print(f'PHASE 3: {len(E)} edges ({dict(srcs)}); kinds={len(kinds)}; JS modules emitted.')
