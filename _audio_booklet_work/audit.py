"""Ground-truth auditor for the realtime-audio child booklet.

Checks, against the SWE corpus data files and the PARENT booklet:
  1. every backticked kebab-case token that looks like an element id exists in
     elements.json (or is on the known non-element allowlist);
  2. every work id the lineage chapter names exists in elements.json works /
     corpus.json, and the booklet's verified/UNVERIFIED claims match the record;
  3. every internal cross-reference resolves: `section x.y`, `chapter N`,
     `invariant N` — with parent-directed references ("parent §x.y",
     "parent invariant N") validated against the PARENT booklet instead;
  4. structural counts (chapters, invariants) match the front matter's claims.

Run from repo root:  python _audio_booklet_work/audit.py
Exit code 0 = clean (warnings allowed), 1 = findings.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MD = ROOT / "realtime-audio-pc-architecture-and-design-r1.md"
PARENT = ROOT / "embedded-c-architecture-and-design-r1.md"

text = MD.read_text(encoding="utf-8")
parent_text = PARENT.read_text(encoding="utf-8")
elements = json.loads((ROOT / "SWE/explorer/data/elements.json").read_text(encoding="utf-8"))
corpus = json.loads((ROOT / "SWE/explorer/data/corpus.json").read_text(encoding="utf-8"))

el_ids = {n["id"] for n in elements["nodes"]}
work_recs = dict(elements["works"])  # id -> record with verification
for n in corpus["nodes"]:
    work_recs.setdefault(n["id"], n)

findings = []
warnings = []

# ---------------------------------------------------------------- backticks
# Tokens that are legitimately backticked but are NOT element ids: routes,
# booklet-local vocabulary, ISA level names, TU-class names.
ALLOW = {
    # enforcement routes (the parent's seven, inherited)
    "compiler-catchable", "analysis-catchable", "build-catchable",
    "host-test-catchable", "target-test-catchable", "runtime-catchable",
    "contract-only",
    # booklet-local phrases
    "this-face",
    # corpus relation kinds quoted in prose
    "alternative-to", "composes-with", "realizes", "constrains",
    # pinned ISA level names (x86-64 psABI micro-architecture levels)
    "x86-64-v3", "x86-64-v2", "x86-64-v4",
    # this booklet's TU-class names (flag canon, §10.2)
    "core-kernel", "shell-adapter", "test-tool",
}
ticks = re.findall(r"`([^`\n]+)`", text)
kebab = sorted({t for t in ticks if re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)+", t)})
used_elements = []
used_workticks = []
for t in kebab:
    if t in el_ids:
        used_elements.append(t)
    elif t in ALLOW:
        pass
    elif t in work_recs:
        used_workticks.append(t)
    else:
        findings.append(f"ELEMENT? backticked kebab token not in catalogs: `{t}`")

# single-word backticked tokens that happen to be catalog ids (informational)
single = sorted({t for t in ticks if re.fullmatch(r"[a-z0-9]{3,}", t)})
single_hits = [t for t in single if t in el_ids or t in work_recs]

# ------------------------------------------------------------------- works
# Work ids the lineage chapter claims, with the booklet's verification stance.
# Stance: 'v' = presented as verified, 'u' = presented as UNVERIFIED.
lineage_claims = {
    # concurrency and the memory model
    "herlihyshavit": "v", "perfbook": "v", "kernelsyncdoc": "v",
    "preshing": "v", "sharajkumar90": "v", "drepperfutex": "v",
    "posa2": "u",
    # parallel execution
    "mattsonppp": "v", "mccoolspp": "v", "blumofeleiserson": "v",
    # mechanical sympathy
    "hennessypatterson": "v", "dreppermem": "u",
    "lmaxdisruptor": "v", "lmaxfowler": "v",
    # platform and toolchain
    "kerrisktlpi": "v", "drepperlibs": "v", "levine": "v",
    "thinlto": "v", "thinltoblog": "v",
    "clangdocs": "v", "clangtidy": "v", "clangformat": "v",
    "lld": "v", "godbolt": "v", "asan": "v",
    # real-time canon (inherited backdrop)
    "liulayland": "v", "buttazzo": "v", "kopetz": "v",
}
for wid, stance in lineage_claims.items():
    rec = work_recs.get(wid)
    if rec is None:
        findings.append(f"WORK missing from corpus data: {wid}")
        continue
    ver = (rec.get("verification") or "").lower()
    if stance == "v" and ver and ver != "verified":
        findings.append(f"WORK {wid}: booklet presents as verified, record says {ver!r}")
    if stance == "u" and ver == "verified":
        findings.append(f"WORK {wid}: booklet flags UNVERIFIED, record says verified")

# every work id actually backticked in the text must be claimed in the table
for t in used_workticks:
    if t not in lineage_claims:
        findings.append(f"WORK backticked in text but absent from lineage_claims: {t}")

# ------------------------------------------------------------------- xrefs
subsecs = set(re.findall(r"^### (\d+\.\d+)", text, re.M))
chapters = set(int(m) for m in re.findall(r"^## (\d+)\.", text, re.M))
parent_subsecs = set(re.findall(r"^### (\d+\.\d+)", parent_text, re.M))
parent_chapters = set(int(m) for m in re.findall(r"^## (\d+)\.", parent_text, re.M))
parent_invs = set(
    int(m) for m in re.findall(r"^(\d+)\. \*\*", parent_text, re.M) if int(m) <= 40
)

# parent-directed section references: "parent §x.y", "parent's §x.y",
# "parent booklet §x.y", "(§x.y there)" is NOT used; keep to explicit forms.
parent_sec_refs = re.findall(r"[Pp]arent(?:'s)?(?: booklet)? §(\d+\.\d+)", text)
for ref in set(parent_sec_refs):
    if ref not in parent_subsecs:
        findings.append(f"XREF dangling PARENT section reference: parent §{ref}")

# strip parent-directed forms, then validate remaining §refs against the child
stripped = re.sub(r"[Pp]arent(?:'s)?(?: booklet)? §\d+\.\d+", "", text)
for ref in set(re.findall(r"§(\d+\.\d+)", stripped)):
    if ref not in subsecs:
        findings.append(f"XREF dangling section reference: §{ref}")

# parent-directed invariant references, incl. "parent invariants 4 and 7"
for m in re.finditer(r"[Pp]arent(?:'s)? invariants? (\d+)(?:(?:,| and) (\d+))*", text):
    for g in m.groups():
        if g and int(g) not in parent_invs:
            findings.append(f"XREF dangling PARENT invariant reference: {g}")
stripped_inv = re.sub(r"[Pp]arent(?:'s)? invariants? \d+(?:(?:,| and) \d+)*", "", text)

inv_items = set(int(m) for m in re.findall(r"^(\d+)\. \*\*", text, re.M))
for ref in set(re.findall(r"[Ii]nvariant (\d+)", stripped_inv)):
    if int(ref) not in inv_items:
        findings.append(f"XREF dangling invariant reference: invariant {ref}")

# chapter references (child-directed; "parent ch. N" forms excluded first)
stripped_ch = re.sub(r"[Pp]arent(?:'s)?(?: booklet)? ch(?:apter)?s?\.? \d+", "", text)
for ref in set(re.findall(r"[Cc]hapters? (\d+)", stripped_ch)):
    if int(ref) not in chapters:
        findings.append(f"XREF dangling chapter reference: chapter {ref}")
for m in re.finditer(r"[Pp]arent(?:'s)?(?: booklet)? ch(?:apter)?s?\.? (\d+)", text):
    if int(m.group(1)) not in parent_chapters:
        findings.append(f"XREF dangling PARENT chapter reference: {m.group(1)}")

# ------------------------------------------------------------- struct claims
n_chap = len(chapters)
if n_chap != 17:
    warnings.append(f"STRUCT chapter count is {n_chap} (front matter implies 17)")
m = re.search(r"Twenty(?:-(\w+))? statements", text)
declared = None
if m:
    declared = {None: 20, "one": 21, "two": 22, "five": 25}.get(m.group(1), None)
inv_in_range = [i for i in inv_items if 1 <= i <= 40]
if declared and max(inv_in_range) != declared:
    findings.append(
        f"STRUCT invariants declared {declared}, list max is {max(inv_in_range)}"
    )

# ------------------------------------------------------------------ report
print(f"element ids used and resolved (kebab): {len(set(used_elements))}")
print(f"single-word catalog ids also present: {len(single_hits)}")
print(f"work ids checked: {len(lineage_claims)}")
print(
    f"subsections: {len(subsecs)}  chapters: {n_chap}  "
    f"invariant-list max: {max(inv_in_range) if inv_in_range else 0}"
)
print(f"parent xrefs: {len(set(parent_sec_refs))} sections validated against parent")
for w in warnings:
    print("WARN ", w)
if findings:
    print(f"\n{len(findings)} FINDINGS:")
    for f in findings:
        print("  -", f)
    sys.exit(1)
print("\nCLEAN")
