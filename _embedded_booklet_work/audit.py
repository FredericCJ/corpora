"""Ground-truth auditor for the embedded C parent booklet.

Checks, against the SWE corpus data files:
  1. every backticked kebab-case token that looks like an element id exists in
     elements.json (or is on the known non-element allowlist);
  2. every work id the lineage chapter names exists in elements.json works /
     corpus.json, and the booklet's verified/UNVERIFIED claims match the record;
  3. every internal cross-reference resolves: `section x.y`, `chapter N`,
     `invariant N`, and part headings;
  4. structural counts (chapters, invariants) match the front matter's claims.

Run from repo root:  python _embedded_booklet_work/audit.py
Exit code 0 = clean (warnings allowed), 1 = findings.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MD = ROOT / "embedded-c-architecture-and-design-r1.md"

text = MD.read_text(encoding="utf-8")
elements = json.loads((ROOT / "SWE/explorer/data/elements.json").read_text(encoding="utf-8"))
corpus = json.loads((ROOT / "SWE/explorer/data/corpus.json").read_text(encoding="utf-8"))

el_ids = {n["id"] for n in elements["nodes"]}
work_recs = dict(elements["works"])  # id -> record with verification
for n in corpus["nodes"]:
    work_recs.setdefault(n["id"], n)

findings = []
warnings = []

# ---------------------------------------------------------------- backticks
# Tokens that are legitimately backticked but are NOT element ids: C syntax,
# file names, route names, and booklet-local vocabulary.
ALLOW = {
    # enforcement routes
    "compiler-catchable", "analysis-catchable", "build-catchable",
    "host-test-catchable", "target-test-catchable", "runtime-catchable",
    "contract-only",
    # booklet-local phrases
    "this-face",
    # corpus relation kinds quoted in prose
    "alternative-to", "composes-with", "realizes", "constrains",
}
ticks = re.findall(r"`([^`\n]+)`", text)
kebab = sorted(
    {
        t
        for t in ticks
        if re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)+", t)
    }
)
used_elements = []
for t in kebab:
    if t in el_ids:
        used_elements.append(t)
    elif t in ALLOW:
        pass
    elif t in work_recs:
        pass  # work id in backticks
    else:
        findings.append(f"ELEMENT? backticked kebab token not in catalogs: `{t}`")

# ------------------------------------------------------------------- works
# Work ids the lineage chapter claims, with the booklet's verification stance.
# Stance: 'v' = presented as verified, 'u' = presented as UNVERIFIED.
lineage_claims = {
    "parnas72": "v", "parnasclements": "v", "bck": "v", "hexagonalarch": "v",
    "posa1": "v", "posa2": "u", "posa3": "u", "posa4": "v",
    "gof": "v", "poeaa": "v", "fowlerdi": "v", "evansddd": "v", "hohpe": "v",
    "vab": "v", "iso42010": "v", "nygardadr": "v",
    "bernhardtfcis": "v", "reynolds72": "v", "candeafox": "v",
    "kopetz": "v", "samekbook": "v", "samekcourse": "v", "qpc": "v",
    "douglasspatternsc": "v", "douglassrtcorpus": "v", "white": "v",
    "koopmanbess": "v", "grenningtdd": "v",
    "preschern": "v", "preschernplop": "u",
    "hanson": "v", "schreiner": "v", "kandr": "v", "noblesmallmem": "v",
    "beningofw": "v", "simmonds": "v", "ldd3": "v", "yiu": "v", "cmsis": "v",
    "dsimonprimer": "u", "pont": "u", "labrosse": "u", "freertosbook": "u",
    "zerotomain": "v", "memfaultea": "u",
    "sakscolumns": "u", "kensmith": "v", "eideregehr": "u",
    "misrac": "v", "misracompliance": "v", "barrc": "v", "jplstd": "v",
    "holzmannp10": "v", "certc": "v", "iso26262": "v", "iec61508": "v",
    "do178c": "v", "arinc653": "v", "autosarclassic": "v",
    "autosaradaptive": "v", "tr18015": "v",
    "boogerdmoonen": "v", "hattonsubset": "v", "hatton95": "v",
    "liulayland": "v", "buttazzo": "v",
    "hanmer": "u", "nygard": "u",
    "meszaros": "v", "welc": "v", "quickcheck": "v",
    "mcdcchilenski": "v", "mcdcnasa": "v", "unity": "v", "cmock": "v",
    "ceedling": "v", "tlsf": "v",
    "lakosvol1": "v", "lakoslsc": "u", "googlesre": "v",
}
for wid, stance in lineage_claims.items():
    rec = work_recs.get(wid)
    if rec is None:
        findings.append(f"WORK missing from corpus data: {wid}")
        continue
    ver = (rec.get("verification") or "").lower()
    if stance == "v" and ver and ver != "verified":
        findings.append(
            f"WORK {wid}: booklet presents as verified, record says {ver!r}"
        )
    if stance == "u" and ver == "verified":
        findings.append(
            f"WORK {wid}: booklet flags UNVERIFIED, record says verified"
        )

# ------------------------------------------------------------------- xrefs
headings = re.findall(r"^#{2,3} (?:(\d+)\.(\d+)?|(\d+))[. ]", text, re.M)
subsecs = set(re.findall(r"^### (\d+\.\d+)", text, re.M))
chapters = set(int(m) for m in re.findall(r"^## (\d+)\.", text, re.M))

for ref in set(re.findall(r"§(\d+\.\d+)", text)):
    if ref not in subsecs:
        findings.append(f"XREF dangling section reference: §{ref}")
for ref in set(re.findall(r"[Cc]hapters? (\d+)", text)):
    if int(ref) not in chapters:
        findings.append(f"XREF dangling chapter reference: chapter {ref}")
inv_items = set(
    int(m) for m in re.findall(r"^(\d+)\. \*\*", text, re.M)
)
for ref in set(re.findall(r"[Ii]nvariant (\d+)", text)):
    if int(ref) not in inv_items:
        findings.append(f"XREF dangling invariant reference: invariant {ref}")

# ------------------------------------------------------------- struct claims
n_chap = len(chapters)
if n_chap != 16:
    warnings.append(f"STRUCT chapter count is {n_chap} (front matter implies 16)")
inv_count = len([i for i in inv_items if 1 <= i <= 40])
m = re.search(r"Twenty-(\w+) statements", text)
declared = {"four": 24, "five": 25, "six": 26, "seven": 27, "eight": 28}.get(
    m.group(1) if m else "", None
)
if declared and declared not in inv_items:
    warnings.append("STRUCT invariant count claim vs list mismatch")
if declared and max(i for i in inv_items if i <= 40) != declared:
    findings.append(
        f"STRUCT invariants declared {declared}, list max is "
        f"{max(i for i in inv_items if i <= 40)}"
    )

# ------------------------------------------------------------------ report
print(f"element ids used and resolved: {len(set(used_elements))}")
print(f"work ids checked: {len(lineage_claims)}")
print(f"subsections: {len(subsecs)}  chapters: {n_chap}  invariant items: {len(inv_items)}")
for w in warnings:
    print("WARN ", w)
if findings:
    print(f"\n{len(findings)} FINDINGS:")
    for f in findings:
        print("  -", f)
    sys.exit(1)
print("\nCLEAN")
