# ROUND 2c - the repairs the three-lens audit panel made blocking conditions for ingestion.
# Deterministic and logged. merged_v3.json -> merged_v4.json
import json, os, re, collections

W = r'E:\dev\corpora\SWE\_spine_work'
STAGES = ['needs','obligations','requirements','design','tools-process']
DOMAINS = ['complex-scale','complex-science','governance','measurement','runtime-ops','hand-c','model-c']

def norm(s):
    s = re.sub(r'[^a-z0-9]+', ' ', (s or '').lower())
    return re.sub(r'\s+', ' ', s).strip()

works = json.load(open(os.path.join(W, 'merged_v3.json'), encoding='utf-8'))
log = collections.defaultdict(list)

# ── 1. verification: only primary-page evidence may claim 'verified' ──────────────────────
# The panel found three new costumes of round 1's error: iso.org SEARCH SNIPPETS, retail
# listings (Amazon), and aggregator metadata (dblp / Semantic Scholar / RePEc). The house rule
# is that verification means a primary page was loaded. Demoting a truly-verified entry costs
# nothing (it stays in the corpus, honestly tagged); keeping a falsely-verified one poisons it.
WEAK = re.compile(r'search|snippet|amazon|repec|dblp|semantic scholar|listing|secondary|'
                  r'wikipedia|not re-verified|reused corpus|bibbase|archive\.org|google books', re.I)
for w in works:
    if w.get('verification') != 'verified':
        continue
    ev = (w.get('evidence') or '').strip()
    if WEAK.search(ev) or len(ev) < 25:
        w['verification'] = 'unverified'
        w['unresolved'] = (w.get('unresolved') or '') or 'verified on non-primary evidence (search snippet / retail or aggregator listing); identifier unconfirmed'
        log['demoted'].append((w.get('title') or '')[:64])

# ── 2. identifiers the panel proved wrong ────────────────────────────────────────────────
# Checked against the Crossref API this session, not taken on the panel's word:
#   10.1109/ECRTS.2004.35      -> HTTP 404, no record            (TLSF)
#   10.5555/257734.257788      -> 10.5555 is ACM's non-DOI id    (Software Aging)
#   10.1145/503209.503224      -> RESOLVES, Sullivan et al. 2001 (modularity) - CORRECT, kept
BAD_IDENT = {
    '10.1109/ECRTS.2004.35': 'DOI returns 404 from the Crossref API (checked 2026-09-19); identifier unconfirmed',
    '10.5555/257734.257788': 'the 10.5555 prefix is an ACM Digital Library internal id, not a resolvable DOI; identifier unconfirmed',
}
for w in works:
    idt = w.get('ident') or ''
    for bad, why in BAD_IDENT.items():
        if bad in idt:
            w['ident'] = re.sub(r'\s*(doi[: ]*)?' + re.escape(bad), '', idt, flags=re.I).strip(' ;,.')
            w['verification'] = 'unverified'
            w['unresolved'] = why
            log['bad-ident'].append('%s -> stripped %s' % ((w.get('title') or '')[:46], bad))

# ── 3. version contradictions inside one harvest ─────────────────────────────────────────
for w in works:
    t = (w.get('title') or '')
    if re.search(r'archimate', t, re.I) and re.search(r'\b3\.1\b', t + ' ' + (w.get('ident') or '')):
        w['verification'] = 'unverified'
        w['unresolved'] = 'this harvest asserts two incompatible current versions of ArchiMate (3.1 here vs 4 / Open Group doc C260 elsewhere); version unconfirmed'
        log['version-conflict'].append('ArchiMate 3.1 entry flagged')
    if re.search(r'\bDlt\b|Diagnostic Log and Trace', t, re.I) and 'R24-11' in (w.get('ident') or ''):
        w['verification'] = 'unverified'
        w['unresolved'] = 'pinned to AUTOSAR R24-11 while sibling entries and autosar.org carry R25-11; release unconfirmed'
        log['version-conflict'].append('AUTOSAR Dlt R24-11 flagged')

# ── 4. duplicates that survived the title merge ──────────────────────────────────────────
# Only genuine same-document pairs. Distinct revisions (ARP4761 vs ARP4761A) and distinct
# annexes (AS5506/1A vs AS5506/3) are NOT duplicates and are deliberately left apart.
DESIG = re.compile(r'\b(arp\s*4754[ab]?|arp\s*4761[a]?)\b', re.I)
groups = collections.defaultdict(list)
for w in works:
    m = DESIG.search((w.get('title') or '') + ' ' + (w.get('ident') or ''))
    if m:
        groups['desig:' + re.sub(r'[^a-z0-9]', '', m.group(1).lower())].append(w)
for w in works:
    groups['title:' + norm(w.get('title'))].append(w)

drop = set()
for key, members in groups.items():
    if len(members) < 2:
        continue
    live = [m for m in members if id(m) not in drop]
    if len(live) < 2:
        continue
    # keep the best-evidenced record; fold the others' tags into it
    live.sort(key=lambda x: (x.get('verification') != 'verified', -len(x.get('ident') or ''), -len(x.get('evidence') or '')))
    keep, rest = live[0], live[1:]
    for r in rest:
        keep['stages'] = sorted(set((keep.get('stages') or []) + (r.get('stages') or [])))
        keep['domains'] = sorted(set((keep.get('domains') or []) + (r.get('domains') or [])))
        if not (keep.get('ident') or '').strip():
            keep['ident'] = r.get('ident') or ''
        drop.add(id(r))
        log['deduped'].append('%s  <=  %s' % ((keep.get('title') or '')[:44], (r.get('title') or '')[:44]))
works = [w for w in works if id(w) not in drop]

# ── 5. anchor deflation ──────────────────────────────────────────────────────────────────
# 'anchor' means "a first stop for this cell". At 34% of the corpus the tag carried no
# information and would have corrupted the Phase-4 census and the Anchors view. Rule: within
# each of the 35 cells keep at most 4 anchors, ranked verified-first then by focus (a work
# tagged into fewer cells is a more specific entry point); a work keeps 'anchor' if it
# survives in ANY cell it serves. Everything else is demoted to 'core'.
def has(w, r):
    return r in (w.get('role') or '')
cells = collections.defaultdict(list)
for w in works:
    if not has(w, 'anchor'):
        continue
    for d in (w.get('domains') or []):
        for s in (w.get('stages') or []):
            cells[(d, s)].append(w)
survive = set()
for k, lst in cells.items():
    lst.sort(key=lambda x: (x.get('verification') != 'verified',
                            len(x.get('stages') or []) * len(x.get('domains') or []),
                            (x.get('title') or '')))
    for w in lst[:4]:
        survive.add(id(w))
deflated = 0
for w in works:
    if has(w, 'anchor') and id(w) not in survive:
        parts = [p for p in re.split(r'[;,]', w.get('role') or '') if p.strip() and p.strip() != 'anchor']
        w['role'] = ';'.join(parts) if parts else 'core'
        deflated += 1
log['anchors'].append('demoted %d of %d anchors to core (per-cell cap of 4)' % (deflated, len(cells) and sum(1 for w in works if has(w,'anchor')) + deflated))

# ── report ───────────────────────────────────────────────────────────────────────────────
ver = sum(1 for w in works if w.get('verification') == 'verified')
mem = sum(1 for w in works if (w.get('membership_id') or '').strip())
anch = sum(1 for w in works if has(w, 'anchor'))
grid = collections.Counter()
for w in works:
    for d in w['domains']:
        for s in w['stages']:
            grid[(d, s)] += 1

print('REPAIR v4')
for k in ('demoted', 'bad-ident', 'version-conflict', 'deduped', 'anchors'):
    print('  %-16s %d' % (k, len(log[k])))
print()
for k in ('bad-ident', 'version-conflict', 'deduped'):
    for x in log[k][:8]:
        print('   [%s] %s' % (k, x))
print()
print('AFTER: %d works | %d memberships | %d new | %d verified (%.0f%%) | %d anchors (%.0f%%)'
      % (len(works), mem, len(works) - mem, ver, 100.0*ver/len(works), anch, 100.0*anch/len(works)))
print()
print('%-16s' % '' + ''.join('%13s' % s for s in STAGES))
for d in DOMAINS:
    print('%-16s' % d + ''.join('%13d' % grid[(d, s)] for s in STAGES))

json.dump(works, open(os.path.join(W, 'merged_v4.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
open(os.path.join(W, 'repair_v4_log.txt'), 'w', encoding='utf-8').write(
    '\n'.join('[%s] %s' % (k, x) for k in log for x in log[k]))
print()
print('wrote merged_v4.json (%d works) + repair_v4_log.txt' % len(works))
