# Emit SWE/design_elements_bridge_v1_0.md from bridge.json (vocabulary + machine-parseable edges + audit).
import json, io, sys, os
from collections import Counter
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
SCRATCH = os.path.dirname(os.path.abspath(__file__))

B = json.load(open(os.path.join(SCRATCH, "bridge.json"), encoding="utf-8"))
edges, unbridged = B["edges"], B["unbridged"]
design = {e["id"] for e in json.load(open(os.path.join(SCRATCH, "merged_design.json"), encoding="utf-8"))["elements"]}
CROSS = {"realizes", "enables"}
kc = Counter(e["kind"] for e in edges)
pc = Counter(e["provenance"] for e in edges)
bridged = {e["from"] for e in edges if e["kind"] in CROSS} | {e["to"] for e in edges if e["kind"] == "constrains"}
unb_ids = sorted({u["id"] for u in unbridged} - bridged)
cross_n = sum(kc[k] for k in ("realizes", "enables", "constrains"))

L = []
L.append("# SWE Corpus — Design ↔ Architecture Bridge v1.0 (`element-bridge`)\n\n")
L.append("**Scope.** The typed, provenance-tagged relation layer between the two element realms — ")
L.append(f"`design_elements_catalog_v1_0.md` ({len(design)} elements) and `architecture_elements_catalog_v1_0.md` — ")
L.append("plus within-realm element relations and idiom→element realization edges. Compiled 2026-07-11.\n\n")
L.append("**Bridging rule (mission-critical).** Every design-realm element carries ≥1 typed relation to ≥1 *specific* ")
L.append("architecture-realm element, or appears on the explicit unbridged list with a rationale. Audited mechanically below.\n\n")
L.append("## Edge-kind vocabulary\n\n")
L.append("| kind | direction | semantics |\n|---|---|---|\n")
L.append("| `realizes` | design → architecture | the design element is an implementation-level realization of the architecture element (Observer → publish-subscribe style; retry-with-backoff → retry tactic) |\n")
L.append("| `enables` | design → architecture | the design element is a load-bearing mechanism the architecture element depends on (event loop → event-driven architecture) |\n")
L.append("| `constrains` | architecture → design | the architecture element constrains the choice/shape of the design element (ARINC 653 partitioning → static allocation) |\n")
L.append("| `implements` | design → design | a language idiom/mechanism realizing a more abstract design element (signals-and-slots → observer) |\n")
L.append("| `specializes` | within one realm | the source is a more specific form of the target |\n")
L.append("| `composes-with` | within one realm | the pair is characteristically composed (symmetric; stored once, direction not meaningful) |\n")
L.append("| `alternative-to` | within one realm | competing solutions to the same forces (symmetric; stored once) |\n\n")
L.append("**Provenance.** `sourced` = the relation is stated in a citable source (cited per edge); `editorial` = reasoned judgment, ")
L.append("marked as such, never presented as fact.\n\n")
L.append(f"**Census.** **{len(edges)} edges** — cross-realm {cross_n} (realizes {kc.get('realizes',0)} · enables {kc.get('enables',0)} · constrains {kc.get('constrains',0)}), ")
L.append(f"implements {kc.get('implements',0)}, within-realm {kc.get('specializes',0)+kc.get('composes-with',0)+kc.get('alternative-to',0)} ")
L.append(f"(specializes {kc.get('specializes',0)} · composes-with {kc.get('composes-with',0)} · alternative-to {kc.get('alternative-to',0)}). ")
L.append(f"Provenance: **{pc.get('sourced',0)} sourced : {pc.get('editorial',0)} editorial** ({pc.get('sourced',0)/max(1,len(edges)):.0%} sourced). ")
L.append(f"Bridging rule: **{len(bridged)}/{len(design)}** design elements bridged; **{len(unb_ids)} unbridged** (list below).\n\n")
L.append("**Edge grammar** (machine-parseable; Phase 4 ingests): ``- `from` kind `to` — provenance[: cite] — note``\n\n---\n")

ORDER = ["realizes", "enables", "constrains", "implements", "specializes", "composes-with", "alternative-to"]
for k in ORDER:
    sub = [e for e in edges if e["kind"] == k]
    if not sub:
        continue
    L.append(f"\n## `{k}` ({len(sub)})\n\n")
    for e in sorted(sub, key=lambda x: (x["from"], x["to"])):
        prov = e["provenance"] + (f": {e['cite']}" if e.get("cite") else "")
        note = e.get("note") or ""
        L.append(f"- `{e['from']}` {k} `{e['to']}` — {prov}{' — ' + note if note else ''}\n")

L.append(f"\n---\n\n## Unbridged design elements ({len(unb_ids)})\n\n")
if unb_ids:
    why = {u["id"]: u.get("why", "") for u in unbridged}
    for i in unb_ids:
        L.append(f"- `{i}` — {why.get(i,'')}\n")
else:
    L.append("None — every design element carries ≥1 cross-realm edge.\n")

out = r"E:\dev\corpora\SWE\design_elements_bridge_v1_0.md"
open(out, "w", encoding="utf-8", newline="\n").write("".join(L))
print(f"wrote {out}: {len(edges)} edges, {len(bridged)}/{len(design)} bridged, {len(unb_ids)} unbridged, sourced {pc.get('sourced',0)}:{pc.get('editorial',0)} editorial")
