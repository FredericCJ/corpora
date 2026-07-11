# Emit SWE/design_elements_corpus_v1_0.md (pass-8 report) from pass8_works.json.
import json, io, sys, os
from collections import defaultdict, Counter
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
SCRATCH = os.path.dirname(os.path.abspath(__file__))

ROUTE_LABEL = {
    "r1": "R1. OO, construction & testing canon",
    "r2": "R2. Communication & messaging",
    "r3": "R3. Embedded, scheduling & numeric",
    "r4": "R4. Execution & concurrency",
    "r5": "R5. Synchronization & lock-free",
    "r6": "R6. Data structures, persistence & caching",
    "r7": "R7. Language idioms, functional & data representation",
    "r8": "R8. Error handling, robustness & security",
    "r9": "R9. Parsing, text & serialization",
    "r10": "R10. Data flow, state & UI/games",
    "r11": "R11. Resource management & memory",
    "r12": "R12. Phase 3 addendum — architecture-catalog naming sources (element ids in this route refer to `architecture_elements_catalog_v1_0.md`)",
}
ROUTE_ORDER = ["r1", "r2", "r3", "r4", "r5", "r6", "r7", "r8", "r9", "r10", "r11", "r12"]

data = json.load(open(os.path.join(SCRATCH, "pass8_works.json"), encoding="utf-8"))
eldata = json.load(open(os.path.join(SCRATCH, "merged_design.json"), encoding="utf-8"))
KIND = {e["id"]: e["kind"] for e in eldata["elements"]}
works = data["works"]

n_m = sum(1 for w in works if w["action"] == "membership")
n_new = len(works) - n_m
n_ver = sum(1 for w in works if w["action"] == "new" and w.get("verification") == "verified")
n_unv = sum(1 for w in works if w["action"] == "new" and w.get("verification") != "verified")
covered = defaultdict(list)
for w in works:
    for e in w["elements"]:
        if e in KIND:
            covered[e].append(w["id"])
uncov = sorted(set(KIND) - set(covered))
mult = Counter(len(v) for v in covered.values())

L = []
L.append("# SWE Corpus — Pass 8: The Design-Element Resource Pass (`design-elements`)\n\n")
L.append("**Scope.** The works that *define and teach* the 708 elements of `design_elements_catalog_v1_0.md` — ")
L.append("naming sources plus best modern treatments, mapped many-to-many onto element ids. ")
L.append("This pass merges into the existing 7-pass unified corpus by record id: works already carried by another pass are **memberships** ")
L.append("(they REUSE the exact existing id), only genuinely absent works are new nodes.\n\n")
L.append("**Collection date:** 2026-07-11 (elements catalog frozen 2026-07-10). **Mapping rule:** every catalog element must be reachable from ≥1 catalog-grade work; ")
L.append("a work claims an element only when it defines or teaches it at catalog grade (mere mention is not coverage); unreachable elements are explicit gaps, never padded.\n\n")
L.append("## Tag legend\n\n")
L.append("- `route:` r1–r11 — the element-domain route that claimed the work (a work can serve several; it is listed under its primary route with the others noted).\n")
L.append("- `role:` anchor | core | advanced | survey — the route's own emphasis.\n")
L.append("- `verification:` **verified** = a primary or authoritative page (publisher / ACM–IEEE DL / standards body / official project site) was loaded live this session confirming the exact identifier; **unverified** = recall/search-index only, soft field named in `UNRESOLVED`. No ISBN/DOI/year is fabricated — omitted sooner than guessed.\n")
L.append("- `elements:` the many-to-many payload — catalog element ids this work defines/teaches (machine-parseable; Phase 4 ingests it).\n\n")
L.append(f"**Census.** **{len(works)} pass-8 members** = **{n_m} memberships** (existing corpus works reclaimed under the element lens) + **{n_new} new nodes** ({n_ver} verified / {n_unv} unverified-quarantined). ")
L.append(f"Element coverage: **{len(covered)}/{len(KIND)}** elements reachable from ≥1 work; multiplicity: {mult.get(1,0)}×1, {mult.get(2,0)}×2, {sum(c for k,c in mult.items() if k>=3)}×≥3. Uncovered: {len(uncov)} (listed in the audit section).\n\n---\n")

num = 0
for r in ROUTE_ORDER:
    sub = [w for w in works if w["routes"][0] == r]
    if not sub:
        continue
    L.append(f"\n## {ROUTE_LABEL[r]}\n")
    for action, title in (("new", "New"), ("membership", "Membership (existing works, reclaimed under the element lens)")):
        ss = [w for w in sub if w["action"] == action]
        if not ss:
            continue
        L.append(f"\n### {title}\n\n")
        for w in sorted(ss, key=lambda x: (x.get("role", "core") != "anchor", x["id"])):
            num += 1
            xr = [x for x in w["routes"] if x != r]
            xrs = f" (also serves {', '.join(xr)})" if xr else ""
            if action == "membership":
                head = f"{num}. **[MEMBERSHIP id={w['id']}]**"
                cite = ""
            else:
                head = f"{num}. **{w['title']}**"
                bits = [w.get("authors") or "", str(w.get("year") or "")]
                cite = " — " + ", ".join(b for b in bits if b) + "."
                if w.get("venue"):
                    cite += f" {w['venue']}."
                if w.get("ident"):
                    cite += f" {w['ident']}."
            unres = f" **UNRESOLVED:** {w['unresolved']}." if w.get("unresolved") else ""
            L.append(f"{head}{cite} `{{{r} | {w.get('role','core')} | {w.get('verification','verified' if action=='membership' else 'unverified')}}}` — {w.get('note','')}{unres}{xrs}\n")
            L.append(f"   - elements: {', '.join(sorted(w['elements']))}\n")

L.append("\n---\n\n## Unverified quarantine\n\n")
q = [w for w in works if w["action"] == "new" and w.get("verification") != "verified"]
if q:
    L.append("Real, on-scope, but not primary-confirmed this session — do not cite the soft field downstream without live verification.\n\n")
    for w in q:
        L.append(f"- **{w['title']}** — {w.get('authors','')}, {w.get('year','?')}. **UNRESOLVED:** {w.get('unresolved') or 'identifier'}. elements: {', '.join(sorted(w['elements']))}\n")
else:
    L.append("Empty — every new node was primary-confirmed live this session.\n")

L.append("\n## Element-coverage audit\n\n")
L.append("| axis | elements | covered | avg works/element |\n|---|---|---|---|\n")
per_axis = defaultdict(lambda: [0, 0, 0])
for e, k in KIND.items():
    per_axis[k][0] += 1
    if e in covered:
        per_axis[k][1] += 1
        per_axis[k][2] += len(covered[e])
for k in sorted(per_axis):
    n, c, s = per_axis[k]
    L.append(f"| {k} | {n} | {c} | {s/max(1,c):.1f} |\n")
L.append(f"| **total** | **{len(KIND)}** | **{len(covered)}** | **{sum(len(v) for v in covered.values())/max(1,len(covered)):.1f}** |\n")
L.append("\n### Unreachable elements (explicit gaps)\n\n")
if uncov:
    for e in uncov:
        gap = next((g for g in data["route_gaps"] if g["element"] == e), None)
        L.append(f"- `{e}` ({KIND[e]}) — {gap['why'] if gap else 'no catalog-grade covering work established this session'}\n")
else:
    L.append("None — every catalog element is reachable from at least one pass-8 work.\n")

prose = os.path.join(SCRATCH, "pass8_summary_prose.md")
if os.path.exists(prose):
    L.append("\n## Coverage summary — where recall thins (honest gaps)\n\n")
    L.append(open(prose, encoding="utf-8").read())

out = r"E:\dev\corpora\SWE\design_elements_corpus_v1_0.md"
open(out, "w", encoding="utf-8", newline="\n").write("".join(L))
print(f"wrote {out}: {len(works)} works ({n_m} memberships, {n_new} new: {n_ver}v/{n_unv}u), {len(covered)}/{len(KIND)} covered, {len(uncov)} gaps")
