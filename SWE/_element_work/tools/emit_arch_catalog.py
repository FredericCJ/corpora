# Emit SWE/architecture_elements_catalog_v1_0.md from merged_arch.json (house format, realm: architecture).
import json, io, sys, os
from collections import Counter
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
SCRATCH = os.path.dirname(os.path.abspath(__file__))

KIND_ORDER = ["style", "pattern", "tactic", "connector", "deployment", "reference-architecture", "description"]
KIND_LABEL = {
    "style": "Architectural styles",
    "pattern": "Architecture patterns",
    "tactic": "Architectural tactics (Bass-style quality-attribute primitives)",
    "connector": "Connector types",
    "deployment": "Deployment, release & scaling structures",
    "reference-architecture": "Reference architectures",
    "description": "Architecture-description constructs",
}

d = json.load(open(os.path.join(SCRATCH, "merged_arch.json"), encoding="utf-8"))
els, rejected = d["elements"], d["rejected"]
dec_path = os.path.join(SCRATCH, "decisions_arch.json")
decisions = json.load(open(dec_path, encoding="utf-8"))["log"] if os.path.exists(dec_path) else []

counts = Counter(e["kind"] for e in els)
conf = Counter(e["confidence"] for e in els)
n_border = sum(1 for e in els if e.get("borderline"))
qa = Counter(t.split(":")[1] for e in els for t in e.get("tags", []) if t.startswith("qa:"))

def named_in_str(m):
    return (f"corpus:{m['named_in_corpus_id']} — {m['named_in']}" if m.get("named_in_corpus_id") else m["named_in"])

L = []
L.append("# SWE Corpus — Architecture-Element Catalog v1.0 (`architecture-elements`, realm: architecture)\n\n")
L.append("**Object.** Named, recurring, architecture-level constructs — styles, patterns, tactics, connector types, ")
L.append("deployment structures, reference architectures, and description constructs: the realm ABOVE the 708-element design catalog ")
L.append("(`design_elements_catalog_v1_0.md`), built to the same ground rules (establishedness gate, canonical naming & dedup, ")
L.append("borderline honesty, stable kebab ids). Compiled 2026-07-11 from the canonical vocabularies the corpus already carries ")
L.append("(Bass–Clements–Kazman tactic trees, POSA1, Shaw–Garlan, Taylor–Medvidović–Dashofy styles + connector taxonomy, ISO/IEC/IEEE 42010, ")
L.append("Kopetz/AUTOSAR/ARINC 653 embedded reference structures) plus demand-driven growth from the 203 candidates Phase 1 parked upward — ")
L.append("every one of the 203 is adjudicated (admitted, folded, or dropped) in the intake log below.\n\n")
L.append("**Same-name, two realms.** Some names live in both realms (heartbeat, event sourcing, bulkhead …). They are cataloged in each realm ")
L.append("where sources establish them — ids disambiguated by kind suffix — and Phase 3b bridges the pairs; the realms are never collapsed.\n\n")
L.append(f"**Census.** **{len(els)} elements** · kinds: " + " · ".join(f"{k} {counts[k]}" for k in KIND_ORDER if counts[k]) + " · ")
L.append(f"confidence: {conf.get('established',0)} established / {conf.get('spot-checked',0)} spot-checked / {conf.get('needs-check',0)} needs-check · {n_border} borderline")
if qa:
    L.append(" · tactic coverage by quality attribute: " + ", ".join(f"{k} {v}" for k, v in sorted(qa.items())))
L.append(".\n\n**Per-kind counts.**\n\n| kind | n |\n|---|---|\n")
for k in KIND_ORDER:
    if counts[k]:
        L.append(f"| {k} | {counts[k]} |\n")
L.append(f"| **total** | **{len(els)}** |\n\n---\n")

for k in KIND_ORDER:
    sub = [e for e in els if e["kind"] == k]
    if not sub:
        continue
    L.append(f"\n## {KIND_LABEL[k]} — `{k}` ({len(sub)})\n\n")
    for m in sorted(sub, key=lambda x: x["id"]):
        aka = ", ".join(m["aka"]) if m["aka"] else "—"
        tags = [t for t in m["tags"] if t != "borderline"]
        if m.get("borderline"):
            tags.append(f"borderline — {m['borderline']}")
        L.append(f"### {m['id']} — {m['name']}\n")
        L.append(f"- aka: {aka}\n- kind: {m['kind']}\n- what: {m['what']}\n- problem: {m['problem']}\n")
        L.append(f"- named-in: {named_in_str(m)}\n- tags: {', '.join(tags) if tags else '—'}\n\n")

L.append("\n---\n\n# Decision log\n\n## Granularity, merge & altitude decisions\n\n")
for x in decisions:
    L.append(f"- {x}\n")
L.append("\n## Parked-candidate intake (the Phase 1 → Phase 3a audit)\n\n")
L.append("Disposition of candidates parked upward by Phases 1–2: admissions appear as catalog entries above; folds and drops are recorded here.\n\n")
for r in sorted(rejected, key=lambda x: (x.get("decision", ""), x.get("name", "").lower())):
    into = f" → {r['into']}" if r.get("into") else ""
    L.append(f"- **{r.get('name','?')}** — {r.get('decision','?')}{into}: {r.get('why','')}\n")

out = r"E:\dev\corpora\SWE\architecture_elements_catalog_v1_0.md"
open(out, "w", encoding="utf-8", newline="\n").write("".join(L))
print(f"wrote {out}: {len(els)} elements; kinds {dict(counts)}; {len(rejected)} intake dispositions")
