# -*- coding: utf-8 -*-
"""Build pipeline for the Calculus → Analysis curriculum explorer.
PHASE 1: node facts (nodes.py)            -> validated fact layer
PHASE 2: edges + editorial spine (edges.py) -> validated inference layer
PHASE 3: structural verification            -> acyclicity proof + cross-checks -> data/corpus_report.md
PHASE 4: emission                           -> data/{corpus,relations}.{json,js}
Run:  python build.py   (from the build/ directory)  or  python build/build.py
The data ships as classic <script>s assigning into window.CALC because fetch() of JSON is blocked
on file://; the JSON twins are the inspectable phase artifacts.
"""
import json, os, sys, io, collections

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
DATA = os.path.normpath(os.path.join(HERE, '..', 'data'))
os.makedirs(DATA, exist_ok=True)

import nodes as N
import edges as R

report = []


def log(line=''):
    report.append(line)
    print(line)


def fail(msg):
    log('FATAL: ' + msg)
    with open(os.path.join(DATA, 'corpus_report.md'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(report) + '\n')
    sys.exit(1)


log('# corpus_report.md — build + structural verification log')
log('')
log(f'Source: `{N.SOURCE_DOC}` (bibliography access date {N.ACCESS_DATE}; compiled {N.COMPILED}).')
log('')

# ---------------- PHASE 1 — fact layer ----------------
log('## PHASE 1 — fact layer (nodes)')
ids = [n['id'] for n in N.NODES]
if len(ids) != len(set(ids)):
    fail('duplicate node ids')
byid = {n['id']: n for n in N.NODES}
kept = [n for n in N.NODES if n['status'] == 'kept']
dropped = [n for n in N.NODES if n['status'] == 'dropped']
for n in N.NODES:
    for field in ('title', 'authors', 'edition', 'year', 'publisher', 'rigor', 'role', 'bib'):
        if not n.get(field):
            fail(f"{n['id']}: missing {field}")
    if n['verification'] != 'verified':
        fail(f"{n['id']}: catalogue rows are all [VERIFIED]")
    if not any(t['tier'] == n['tier'] for t in N.TIERS):
        fail(f"{n['id']}: unknown tier {n['tier']}")
log(f"- {len(N.NODES)} nodes carried ({len(kept)} kept + {len(dropped)} dropped: "
    f"{', '.join(n['id'] for n in dropped)}); all fields present; all [VERIFIED].")
tier_pop = collections.Counter(n['tier'] for n in N.NODES)
log('- tier population: ' + ', '.join(f"T{t}:{tier_pop.get(t, 0)}" for t in range(9)) + '.')
log('')

# ---------------- PHASE 2 — inference layer ----------------
log('## PHASE 2 — inference layer (edges + editorial spine)')
pairs = [(s, t) for s, t, _, _, _ in R.EDGES]
if len(pairs) != len(set(pairs)):
    fail('duplicate edges in the table')
for s, t, seam, tag, _ in R.EDGES:
    if s not in byid or t not in byid:
        fail(f'edge endpoint not a node: {s}->{t}')
    if byid[s]['status'] != 'kept' or byid[t]['status'] != 'kept':
        fail(f'edge touches a dropped node: {s}->{t}')
    if tag not in ('EVIDENCED', 'JUDGMENT'):
        fail(f'edge {s}->{t}: bad tag {tag}')
    if not seam:
        fail(f'edge {s}->{t}: empty seam')
n_ev = sum(1 for e in R.EDGES if e[3] == 'EVIDENCED')
n_jd = len(R.EDGES) - n_ev
log(f'- {len(R.EDGES)} edges ({n_ev} EVIDENCED + {n_jd} JUDGMENT); endpoints exist; no edge touches N18.')

# §3 table vs §6 DOT cross-check
if set(pairs) != R.DOT_EDGES:
    only_tab = set(pairs) - R.DOT_EDGES
    only_dot = R.DOT_EDGES - set(pairs)
    fail(f'edge table vs DOT mismatch — table-only {sorted(only_tab)}, dot-only {sorted(only_dot)}')
log('- §3 edge table and §6 DOT rendering state the SAME 46-edge set (independent transcriptions agree).')

for ps in R.PARALLEL_SETS:
    tiers = {byid[m]['tier'] for m in ps['members']}
    if len(tiers) != 1:
        fail(f"{ps['id']}: members span tiers {tiers}")
    if any(byid[m]['status'] != 'kept' for m in ps['members']):
        fail(f"{ps['id']}: contains a dropped member")
log(f"- {len(R.PARALLEL_SETS)} parallel sets; each set's members share one tier; no dropped members.")

edge_set = set(pairs)
for ln in R.LINEAGES:
    for a, b in zip(ln['path'], ln['path'][1:]):
        if (a, b) not in edge_set:
            fail(f"lineage {ln['id']}: hop {a}->{b} is not an edge")
    for st in ln['steps']:
        if (st['frm'], st['to']) not in edge_set:
            fail(f"lineage {ln['id']}: step {st['frm']}->{st['to']} is not an edge")
log('- both lineages walk actual edges hop-by-hop (main 8 nodes / variant 5 nodes).')

gate_ids = [i for g in R.GATE for i in g['ids']]
if sorted(gate_ids) != sorted(ids):
    fail(f'gate ledger does not cover every node exactly once: {collections.Counter(gate_ids)}')
for g in R.GATE:
    for i in g['ids']:
        if byid[i]['status'] != g['status']:
            fail(f"gate row '{g['candidate']}' says {g['status']} but {i} is {byid[i]['status']}")
log(f'- quality-gate ledger: {len(R.GATE)} rows cover all {len(ids)} nodes exactly once; '
    'kept/dropped agrees with the catalogue.')
log('')

# ---------------- PHASE 3 — structural verification ----------------
log('## PHASE 3 — structural verification')

# Kahn topological sort over kept nodes = machine acyclicity proof.
indeg = {n['id']: 0 for n in kept}
down = collections.defaultdict(list)
up = collections.defaultdict(list)
for s, t in pairs:
    indeg[t] += 1
    down[s].append(t)
    up[t].append(s)
queue = sorted([i for i, d in indeg.items() if d == 0])
topo = []
indeg2 = dict(indeg)
while queue:
    cur = queue.pop(0)
    topo.append(cur)
    for nxt in sorted(down[cur]):
        indeg2[nxt] -= 1
        if indeg2[nxt] == 0:
            queue.append(nxt)
    queue.sort()
if len(topo) != len(kept):
    fail(f'cycle detected — topological sort placed only {len(topo)}/{len(kept)} nodes')
log(f'- ACYCLIC (machine-checked): Kahn topological sort places all {len(kept)} kept nodes.')
log('  topological order: ' + ' '.join(topo))

# Tier monotonicity: every edge is tier-non-decreasing; within-tier edges enumerated.
within = [(s, t) for s, t in pairs if byid[s]['tier'] == byid[t]['tier']]
if any(byid[s]['tier'] > byid[t]['tier'] for s, t in pairs):
    fail('an edge points to a LOWER tier')
log(f'- tier-monotone: every edge satisfies tier(s) ≤ tier(t); within-tier edges: '
    + (', '.join(f'{s}→{t}' for s, t in within) or 'none')
    + ' (the report allows “forward within a tier boundary from a prerequisite to a strict extension”).')

# Degree analysis vs the report's designations.
sources = [i for i in indeg if indeg[i] == 0]
terminals = sorted(i for n in kept for i in [n['id']] if not down[i])
designated_sinks = sorted(n['id'] for n in kept if 'sink' in n['flags'])
leaves = sorted(n['id'] for n in kept if 'terminal-leaf' in n['flags'])
log(f"- degrees: source nodes (in-degree 0) = {', '.join(sorted(sources))} — matches the report's "
    "single SOURCE designation (N01)." if sources == ['N01'] else
    f'- WARNING: unexpected source set {sources}')
log(f"- graph-terminal nodes (out-degree 0) = {', '.join(terminals)}; the report designates "
    f"{', '.join(designated_sinks)} as SINKS, {', '.join(leaves)} as terminal leaves of the complex "
    'lineage, and N16 as a supporting terminal — the sets agree.')
if set(terminals) != set(designated_sinks) | set(leaves) | {'N16'}:
    fail('terminal-node set does not match the designations')

# Parallel-set shared-edge audit: stated 'siblings inherit the same edges' vs the drawn edge list.
log('- parallel-set shared-edge audit (stated: siblings inherit the same in/out edges):')
ps_audit = {}
for ps in R.PARALLEL_SETS:
    mem = set(ps['members'])
    ins = {m: set(up[m]) - mem for m in mem}
    outs = {m: set(down[m]) - mem for m in mem}
    shared_in = set.intersection(*ins.values()) if ins else set()
    shared_out = set.intersection(*outs.values()) if outs else set()
    part_in = {x: sorted(m for m in mem if x in ins[m]) for x in (set.union(*ins.values()) - shared_in)}
    part_out = {x: sorted(m for m in mem if x in outs[m]) for x in (set.union(*outs.values()) - shared_out)}
    ps_audit[ps['id']] = dict(sharedIn=sorted(shared_in), sharedOut=sorted(shared_out),
                              partialIn={k: v for k, v in sorted(part_in.items())},
                              partialOut={k: v for k, v in sorted(part_out.items())})
    line = f"  - {ps['id']} {{{', '.join(sorted(mem))}}}: shared-in {sorted(shared_in) or '—'}, " \
           f"shared-out {sorted(shared_out) or '—'}"
    if part_in:
        line += f"; PARTIAL in {part_in}"
    if part_out:
        line += f"; PARTIAL out {part_out}"
    log(line)
log('  NOTE: PS-2 is stated to share outgoing edges to N08/N09, but the drawn edge list gives N09 '
    'only to N05 — carried as a partial edge, not smoothed over. PS-6 shares only N25 downstream '
    '(N26/N27 reachable from two of three members); also carried as partial.')

# Exact path count for the finder's default (DP over the DAG).
count = {i: 0 for i in indeg}
count['N27'] = 1
for i in reversed(topo):
    if i != 'N27':
        count[i] = sum(count[t] for t in down[i])
log(f"- path finder default: N01 → N27 has exactly {count['N01']} directed paths (DP over the topo order).")
log('')

# ---------------- PHASE 4 — emission ----------------
log('## PHASE 4 — emission')
corpus = dict(
    phase='fact layer — hand-transcribed from the report, structurally verified by build.py',
    meta=dict(title='Book-Anchored Progressive Curriculum: Calculus → Analysis',
              source=N.SOURCE_DOC, access_date=N.ACCESS_DATE, compiled=N.COMPILED),
    tldr=N.TLDR,
    tiers=N.TIERS,
    nodes=N.NODES,
)
relations = dict(
    kinds=['prerequisite-of'],
    evidence=['EVIDENCED', 'JUDGMENT'],
    edges=[dict(s=s, t=t, seam=seam, tag=tag, note=note) for s, t, seam, tag, note in R.EDGES],
    parallelSets=[dict(ps, audit=ps_audit[ps['id']]) for ps in R.PARALLEL_SETS],
    lineages=R.LINEAGES,
    gate=R.GATE,
    register=R.REGISTER,
    caveats=R.CAVEATS,
    views=R.VIEWS,
)


def emit(name, ns, obj):
    js = json.dumps(obj, ensure_ascii=False, separators=(', ', ': '))
    with open(os.path.join(DATA, name + '.json'), 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
        f.write('\n')
    with open(os.path.join(DATA, name + '.js'), 'w', encoding='utf-8') as f:
        f.write(f'// GENERATED by build/build.py — do not hand-edit. JSON twin: {name}.json\n')
        f.write('window.CALC = window.CALC || {};\n')
        f.write(f'CALC.{ns} = {js};\n')
    log(f'- wrote data/{name}.json + data/{name}.js')


emit('corpus', 'corpus', corpus)
emit('relations', 'relations', relations)

log('')
log(f'Totals: {len(N.NODES)} nodes ({len(kept)} in the DAG + {len(dropped)} dropped) · '
    f'{len(R.EDGES)} edges ({n_ev} EVIDENCED / {n_jd} JUDGMENT) · {len(N.TIERS)} tiers · '
    f'{len(R.PARALLEL_SETS)} parallel sets · {len(R.LINEAGES)} lineages · {len(R.GATE)} ledger rows.')
with open(os.path.join(DATA, 'corpus_report.md'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(report) + '\n')
print('\nOK — build complete.')
