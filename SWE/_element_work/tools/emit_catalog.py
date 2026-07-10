# Emit the Phase 1 catalog markdown from merged_design.json (house entry format, machine-parseable).
import json, sys, io, os
from collections import Counter, OrderedDict

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
SCRATCH = os.path.dirname(os.path.abspath(__file__))

AXIS_ORDER = ["data-representation", "data-flow-buffering", "execution-concurrency",
              "synchronization-coordination", "state-management", "resource-management",
              "caching-memoization", "error-handling", "robustness-security", "communication",
              "scheduling-time", "oo-patterns", "construction-api", "functional-type-idioms",
              "data-structures", "persistence-durability", "parsing-text", "serialization-framing",
              "numeric-precision", "code-structure", "testing-constructs", "embedded-systems"]
AXIS_LABEL = {
    "data-representation": "Data representation",
    "data-flow-buffering": "Data flow & buffering",
    "execution-concurrency": "Execution & concurrency",
    "synchronization-coordination": "Synchronization & coordination",
    "state-management": "State management",
    "resource-management": "Resource management",
    "caching-memoization": "Caching & memoization",
    "error-handling": "Error handling",
    "robustness-security": "Robustness & security",
    "communication": "Communication",
    "scheduling-time": "Scheduling & time",
    "oo-patterns": "OO design patterns",
    "construction-api": "Construction & API shape",
    "functional-type-idioms": "Functional & type-level idioms",
    "data-structures": "Data structures & algorithms (design-building-block granularity)",
    "persistence-durability": "Persistence & durability",
    "parsing-text": "Parsing & text processing",
    "serialization-framing": "Serialization, framing & encoding",
    "numeric-precision": "Numeric & precision",
    "code-structure": "Code structure & variant management",
    "testing-constructs": "Testing constructs",
    "embedded-systems": "Embedded / systems",
}

def named_in_str(m):
    if m.get("named_in_corpus_id"):
        return f"corpus:{m['named_in_corpus_id']} — {m['named_in']}"
    return m["named_in"]

def entry_md(m):
    aka = ", ".join(m["aka"]) if m["aka"] else "—"
    tags = [t for t in m["tags"] if t != "borderline"]
    if m.get("borderline"):
        tags.append(f"borderline — {m['borderline']}")
    tag_s = ", ".join(tags) if tags else "—"
    return (f"### {m['id']} — {m['name']}\n"
            f"- aka: {aka}\n"
            f"- kind: {m['kind']}\n"
            f"- what: {m['what']}\n"
            f"- problem: {m['problem']}\n"
            f"- named-in: {named_in_str(m)}\n"
            f"- tags: {tag_s}\n")

def main():
    with open(os.path.join(SCRATCH, "merged_design.json"), encoding="utf-8") as f:
        data = json.load(f)
    els = data["elements"]
    dec_path = os.path.join(SCRATCH, "decisions_design.json")
    decisions = []
    if os.path.exists(dec_path):
        with open(dec_path, encoding="utf-8") as f:
            decisions = json.load(f).get("log", [])

    axes = [a for a in AXIS_ORDER if any(e["kind"] == a for e in els)]
    extra = sorted({e["kind"] for e in els} - set(axes))
    axes += extra
    counts = Counter(e["kind"] for e in els)
    conf = Counter(e["confidence"] for e in els)
    n_border = sum(1 for e in els if e.get("borderline"))

    # dedup parked/excluded by normalized name
    def dedup(items):
        seen, out = set(), []
        for p in items:
            k = p["name"].strip().lower()
            if k not in seen:
                seen.add(k)
                out.append(p)
        return out
    parked = dedup(data.get("parked_architecture", []))
    excluded = dedup(data.get("excluded_notable", []))

    L = []
    L.append("# SWE Corpus — Design-Element Catalog v1.0 (`design-elements`, realm: design)\n")
    L.append("**Object.** Named, recurring, implementation-level building blocks and mechanisms of software design — ")
    L.append("the mid-level vocabulary below software architecture and above raw language syntax. ")
    L.append("Compiled 2026-07-10 by coverage-driven enumeration: corpus seed-mining (GoF, POSA 1–3, Douglass, Samek, White, Koopman, Pont, Noble–Weir, Hanmer, Hanson/Schreiner/Tornhill/Preschern, Nygard …), ")
    L.append("web sweeps of the established catalogs (PLoP/Hillside, Nystrom, EIP, Fowler, wikis, language idiom collections), and per-axis gap hunts to saturation ")
    L.append("(stopping rule: a full kind × source × domain sweep yielding <5 new elements, then one adversarial gap hunt).\n\n")
    L.append("**Entry contract.** One element per mechanism (synonyms folded into `aka`); GoF/POSA names canonical for their patterns; ")
    L.append("every element is named in at least one citable published source (`named-in`; `corpus:<id>` = the work is already in `explorer/data/corpus.json`); ")
    L.append("`borderline` tags carry a one-line altitude rationale. ids are kebab-case, unique, stable — they become node ids in Phase 4.\n\n")
    L.append(f"**Census.** **{len(els)} elements** across {len(axes)} kind axes · confidence: "
             f"{conf.get('established',0)} established / {conf.get('spot-checked',0)} spot-checked / {conf.get('needs-check',0)} needs-check · "
             f"{n_border} borderline · {len(parked)} candidates parked to the architecture realm (Phase 3 input) · {len(excluded)} notable exclusions.\n\n")
    L.append("**Per-axis counts.**\n\n| kind | n |\n|---|---|\n")
    for a in axes:
        L.append(f"| {a} | {counts[a]} |\n")
    L.append(f"| **total** | **{len(els)}** |\n\n")
    L.append("Kind axes are scaffolding for coverage and readability only — no structural or ontological commitment.\n\n---\n")

    for a in axes:
        sub = [e for e in els if e["kind"] == a]
        L.append(f"\n## {AXIS_LABEL.get(a, a)} — `{a}` ({len(sub)})\n\n")
        for m in sub:
            L.append(entry_md(m) + "\n")

    L.append("\n---\n\n# Decision log\n")
    L.append("\n## Granularity, merge & altitude decisions\n\n")
    if decisions:
        for d in decisions:
            L.append(f"- {d}\n")
    L.append("\n## Parked to the architecture realm (Phase 3 input)\n\n")
    L.append("Candidates the altitude test rejected upward; they enter the Phase 3 architecture catalog (or are dropped there with rationale).\n\n")
    for p in sorted(parked, key=lambda x: x["name"].lower()):
        L.append(f"- **{p['name']}** — {p.get('why','')}\n")
    L.append("\n## Notable exclusions (not elements)\n\n")
    for x in sorted(excluded, key=lambda x: x["name"].lower()):
        L.append(f"- **{x['name']}** — {x.get('why','')}\n")

    out = os.path.join(os.path.dirname(SCRATCH) if False else r"E:\dev\corpora\SWE", "design_elements_catalog_v1_0.md")
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write("".join(L))
    print(f"wrote {out}: {len(els)} elements, {len(axes)} axes, {len(parked)} parked, {len(excluded)} excluded")

if __name__ == "__main__":
    main()
