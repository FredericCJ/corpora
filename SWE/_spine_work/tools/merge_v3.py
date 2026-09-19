# Merge round 1 (repaired) + round 2 gap harvest + membership recall -> merged_v3.json
# Applies the same honesty rules to round-2 output that round 1 had to be repaired for.
import json, os, re, glob, collections

SWE = r'E:\dev\corpora\SWE'
W = os.path.join(SWE, '_spine_work')
STAGES = ['needs','obligations','requirements','design','tools-process']
DOMAINS = ['complex-scale','complex-science','governance','measurement','runtime-ops','hand-c','model-c']
MEMEV = re.compile(r'id_index|membership:|grepped this session|present in .*\.tsv', re.I)

def norm(s):
    s = (s or '').lower()
    s = re.sub(r'[^a-z0-9]+', ' ', s)
    return re.sub(r'\s+', ' ', s).strip()

# valid corpus ids, for membership validation
IDX = {}
for line in open(os.path.join(W, 'id_index.tsv'), encoding='utf-8').read().splitlines()[1:]:
    p = line.split('\t')
    if len(p) >= 4:
        IDX[p[0]] = dict(id=p[0], year=p[1], title=p[2], authors=p[3])

notes = []
def clean(e, src):
    """Normalise one harvest entry: legal tags, honest verification."""
    st = [s for s in (e.get('stages') or [])]
    dm = [d for d in (e.get('domains') or [])]
    e['stages'] = sorted(set([s for s in st if s in STAGES] + [d for d in dm if d in STAGES]))
    e['domains'] = sorted(set([d for d in dm if d in DOMAINS] + [s for s in st if s in DOMAINS]))
    if e.get('verification') == 'verified':
        ev = (e.get('evidence') or '').strip()
        if MEMEV.search(ev):
            e['verification'] = 'unverified'
            e['unresolved'] = 'verification rested on a membership grep, not a bibliographic check'
            notes.append('demoted (membership-grep evidence): %s [%s]' % ((e.get('title') or '')[:58], src))
        elif len(ev) < 25:
            e['verification'] = 'unverified'
            e['unresolved'] = e.get('unresolved') or 'marked verified with no usable evidence'
            notes.append('demoted (no evidence): %s [%s]' % ((e.get('title') or '')[:58], src))
    mid = (e.get('membership_id') or '').strip()
    if mid and mid not in IDX:
        notes.append('DROPPED bogus membership_id %r on %r [%s]' % (mid, (e.get('title') or '')[:48], src))
        e['membership_id'] = None
    e['_src'] = src
    return e

entries = []
# 1. round 1, already repaired
for e in json.load(open(os.path.join(W, 'merged_v2.json'), encoding='utf-8')):
    entries.append(clean(e, e.get('_src', 'round1')))
r1 = len(entries)

# 2. round 2 gap harvest
g2 = 0
for path in sorted(glob.glob(os.path.join(W, 'harvest2', '*.json'))):
    try:
        d = json.load(open(path, encoding='utf-8'))
    except Exception as ex:
        notes.append('PARSE FAIL %s: %s' % (os.path.basename(path), str(ex)[:70])); continue
    for e in (d if isinstance(d, list) else []):
        if isinstance(e, dict) and (e.get('title') or e.get('membership_id')):
            entries.append(clean(e, os.path.basename(path))); g2 += 1

# 3. membership recall over the existing 468
rec, rec_claimed = 0, 0
for path in sorted(glob.glob(os.path.join(W, 'recall', '*.json'))):
    try:
        d = json.load(open(path, encoding='utf-8'))
    except Exception as ex:
        notes.append('PARSE FAIL %s: %s' % (os.path.basename(path), str(ex)[:70])); continue
    for r in (d if isinstance(d, list) else []):
        if not isinstance(r, dict):
            continue
        rec += 1
        if not r.get('claimed'):
            continue
        cid = (r.get('id') or '').strip()
        if cid not in IDX:
            notes.append('recall names unknown id %r' % cid); continue
        rec_claimed += 1
        base = IDX[cid]
        entries.append(clean(dict(
            title=base['title'], authors=base['authors'], year=base['year'], venue='', ident='',
            type='other', stages=r.get('stages') or [], domains=r.get('domains') or [],
            role=r.get('role') or 'core', verification='unverified', evidence='',
            unresolved='', membership_id=cid, note=(r.get('why') or '')), os.path.basename(path)))

# ---------- dedup ----------
merged = {}
for e in entries:
    mid = (e.get('membership_id') or '').strip()
    key = 'id:' + mid if mid else 'ti:' + norm(e.get('title'))
    if key in ('ti:', 'id:'):
        continue
    if key not in merged:
        e['_srcs'] = [e['_src']]; merged[key] = e
    else:
        m = merged[key]
        m['_srcs'].append(e['_src'])
        for f in ('stages', 'domains'):
            m[f] = sorted(set((m.get(f) or []) + (e.get(f) or [])))
        if e.get('verification') == 'verified' and m.get('verification') != 'verified':
            for f in ('verification','evidence','ident','year','venue','authors','type'):
                if e.get(f): m[f] = e[f]
        for f in ('ident', 'venue', 'authors', 'year'):
            if not (m.get(f) or '').strip() and (e.get(f) or '').strip():
                m[f] = e[f]
        if (m.get('type') or 'other') == 'other' and (e.get('type') or '') not in ('', 'other'):
            m['type'] = e['type']

works = [w for w in merged.values() if (w.get('stages') or []) and (w.get('domains') or [])]
dropped_untagged = len(merged) - len(works)

ver = sum(1 for w in works if w.get('verification') == 'verified')
mem = sum(1 for w in works if (w.get('membership_id') or '').strip())
grid = collections.Counter()
for w in works:
    for d in w['domains']:
        for s in w['stages']:
            grid[(d, s)] += 1

print('round 1 (repaired) : %d' % r1)
print('round 2 gap harvest: %d claims from %d files' % (g2, len(glob.glob(os.path.join(W, 'harvest2', '*.json')))))
print('recall             : %d corpus works judged, %d claimed' % (rec, rec_claimed))
print('-' * 62)
print('MERGED v3          : %d unique works (%d dropped for missing stage/domain tags)' % (len(works), dropped_untagged))
print('  memberships      : %d   new nodes: %d' % (mem, len(works) - mem))
print('  verified         : %d (%.0f%%)   unverified: %d' % (ver, 100.0*ver/max(1,len(works)), len(works)-ver))
print()
print('%-16s' % '' + ''.join('%13s' % s for s in STAGES))
for d in DOMAINS:
    print('%-16s' % d + ''.join('%13d' % grid[(d, s)] for s in STAGES))
print()
thin = sorted([(grid[(d,s)], d, s) for d in DOMAINS for s in STAGES])
print('thinnest cells:', ', '.join('%s x %s (%d)' % (d, s, n) for n, d, s in thin[:6]))
print()
print('normalisation notes: %d' % len(notes))
for nt in notes[:18]:
    print('   -', nt)

json.dump(works, open(os.path.join(W, 'merged_v3.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
open(os.path.join(W, 'merge_v3_log.txt'), 'w', encoding='utf-8').write('\n'.join(notes))
print()
print('wrote merged_v3.json (%d works)' % len(works))
