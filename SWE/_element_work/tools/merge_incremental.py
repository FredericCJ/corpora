# Incremental merge: fold sweeps/gaps/*.json into merged_design.json; report genuinely-new count.
import json, io, sys, os, re
from collections import Counter
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
SCRATCH = os.path.dirname(os.path.abspath(__file__))
GAPS = os.path.join(SCRATCH, "sweeps", sys.argv[1] if len(sys.argv) > 1 else "gaps")

STOP_SUFFIX = {"pattern", "idiom", "mechanism"}
def norm(s):
    s = re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()
    toks = [t for t in s.split() if t]
    if toks and toks[0] == "the":
        toks = toks[1:]
    if len(toks) > 1 and toks[-1] in STOP_SUFFIX:
        toks = toks[:-1]
    if toks and len(toks[-1]) > 3 and toks[-1].endswith("s") and not toks[-1].endswith("ss"):
        toks = toks[:-1] + [toks[-1][:-1]]
    return " ".join(toks)

with open(os.path.join(SCRATCH, "merged_design.json"), encoding="utf-8") as f:
    data = json.load(f)
els = data["elements"]
keymap = {}
for e in els:
    for n in [e["name"]] + (e.get("aka") or []):
        keymap.setdefault(norm(n), e)

work_ids = {l.split("\t")[0] for l in open(os.path.join(SCRATCH, "work_ids.tsv"), encoding="utf-8")}
existing_ids = {e["id"] for e in els}
new, folded, parked_new, excl_new = [], [], [], []
for fn in sorted(os.listdir(GAPS)):
    if not fn.endswith(".json"):
        continue
    with open(os.path.join(GAPS, fn), encoding="utf-8") as f:
        d = json.load(f)
    scout = d.get("scout", fn[:-5])
    for x in d.get("elements", []):
        if isinstance(x.get("aka"), str):
            x["aka"] = [a.strip() for a in x["aka"].split(",") if a.strip()]
        hit = None
        for n in [x["name"]] + (x.get("aka") or []):
            if norm(n) in keymap:
                hit = keymap[norm(n)]
                break
        if hit:
            for a in [x["name"]] + (x.get("aka") or []):
                if norm(a) not in {norm(z) for z in [hit["name"]] + hit["aka"]}:
                    hit["aka"].append(a)
            hit["sources_all"].append({"src": x["named_in"], "corpus_id": x.get("named_in_corpus_id")})
            if scout not in hit["scouts"]:
                hit["scouts"].append(scout)
            folded.append(f"{x['id']} -> {hit['id']}")
            continue
        eid = x["id"]
        if eid in existing_ids or eid in work_ids:
            eid = eid + "-2"
        m = {"id": eid, "name": x["name"], "aka": x.get("aka") or [], "kind": x["kind"],
             "what": x["what"], "problem": x["problem"], "named_in": x["named_in"],
             "named_in_corpus_id": x.get("named_in_corpus_id"), "tags": x.get("tags") or [],
             "borderline": x.get("borderline"), "confidence": x.get("confidence", "established"),
             "scouts": [scout], "kind_votes": {x["kind"]: 1},
             "sources_all": [{"src": x["named_in"], "corpus_id": x.get("named_in_corpus_id")}]}
        els.append(m)
        existing_ids.add(eid)
        for n in [m["name"]] + m["aka"]:
            keymap.setdefault(norm(n), m)
        new.append(eid)
    for p in d.get("parked_architecture", []) or []:
        if isinstance(p, str):
            p = {"name": p, "why": ""}
        p.setdefault("name", p.get("candidate", str(p)[:60]))
        p["_scout"] = scout
        data["parked_architecture"].append(p)
        parked_new.append(p["name"])
    for xx in d.get("excluded_notable", []) or []:
        if isinstance(xx, str):
            xx = {"name": xx, "why": ""}
        xx.setdefault("name", xx.get("candidate", str(xx)[:60]))
        xx["_scout"] = scout
        data["excluded_notable"].append(xx)
        excl_new.append(xx["name"])

els.sort(key=lambda m: (m["kind"], m["id"]))
with open(os.path.join(SCRATCH, "merged_design.json"), "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=1)
with open(os.path.join(SCRATCH, "elements_index.txt"), "w", encoding="utf-8") as f:
    for e in sorted(els, key=lambda x: x["id"]):
        f.write(f"{e['id']} | {e['name']} | aka: {', '.join(e['aka'])} | {e['kind']}\n")
print(f"NEW elements: {len(new)}")
for n in new:
    print("  +", n)
print(f"folded into existing: {len(folded)}")
for fo in folded:
    print("  ~", fo)
print(f"parked added: {len(parked_new)}  excluded added: {len(excl_new)}")
print(f"total elements: {len(els)}")
print("axes:", dict(sorted(Counter(e['kind'] for e in els).items())))
