# Collect thin-cell adjudications from both adversarial critic panels into thin_cells.json,
# normalising the separators the critics used ("a x b", "a|b") to one canonical "domain x stage".
# Where panels disagree the LATER (better-informed) round wins and the disagreement is recorded.
import json, os, sys, re, collections

W = r'E:\dev\corpora\SWE\_spine_work'
STAGES = ['needs','obligations','requirements','design','tools-process']
DOMAINS = ['complex-scale','complex-science','governance','measurement','runtime-ops','hand-c','model-c']

def canon(cell):
    # NOTE: the separator must not be a bare 'x' without surrounding whitespace — that also
    # matches the x inside "complex-scale"/"complex-science" and silently drops those cells.
    parts = [p.strip() for p in re.split(r'\s*×\s*|\s+x\s+|\s*\|\s*', (cell or '').strip()) if p.strip()]
    d = next((p for p in parts if p in DOMAINS), None)
    s = next((p for p in parts if p in STAGES), None)
    return (d + ' x ' + s) if (d and s) else None

def panels(path, round_no):
    """Yield (cell, adjudication, why) from a workflow output file."""
    if not os.path.exists(path):
        return
    d = json.loads(open(path, encoding='utf-8').read())
    r = d.get('result', d)
    if isinstance(r, str):
        r = json.loads(r)
    for key in ('critics', 'audits'):
        for c in (r.get(key) or []):
            for t in (c.get('thin_cells') or []):
                k = canon(t.get('cell'))
                if k and t.get('adjudication'):
                    yield k, t['adjudication'], (t.get('why') or '').strip(), round_no

if len(sys.argv) < 2:
    print('usage: thin_cells.py <round1.output> [round2.output]'); sys.exit(1)

votes = collections.defaultdict(list)
for i, path in enumerate(sys.argv[1:], start=1):
    for k, adj, why, rnd in panels(path, i):
        votes[k].append((rnd, adj, why))

out, disagreed = {}, []
for k, vs in votes.items():
    top = max(v[0] for v in vs)
    late = [v for v in vs if v[0] == top]
    adjs = set(v[1] for v in late)
    if len(adjs) > 1:
        # inside one round the panel split: sweep-thin is the weaker claim and wins, because
        # calling a cell literature-thin asserts the field never wrote it, which needs consensus.
        adj = 'sweep-thin'
        disagreed.append(k + ' (panel split: ' + ', '.join(sorted(adjs)) + ' -> sweep-thin)')
    else:
        adj = late[0][1]
    why = max((v[2] for v in late if v[1] == adj), key=len, default='')
    earlier = set(v[1] for v in vs if v[0] < top)
    if earlier and adj not in earlier:
        disagreed.append(k + ' (round ' + str(top) + ' overturned ' + ', '.join(sorted(earlier)) + ' -> ' + adj + ')')
    out[k] = {'adjudication': adj, 'why': why[:260]}

json.dump(out, open(os.path.join(W, 'thin_cells.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
print('thin_cells.json: %d adjudicated cells' % len(out))
for k in sorted(out):
    print('   %-34s %-16s %s' % (k, out[k]['adjudication'], out[k]['why'][:70]))
if disagreed:
    print('\npanel disagreements resolved (%d):' % len(disagreed))
    for d in disagreed:
        print('   -', d)
