# Phase 2 prep: aggregate naming sources across elements -> candidate work list with element coverage.
import json, io, sys, os, re
from collections import defaultdict
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
SCRATCH = os.path.dirname(os.path.abspath(__file__))

def title_key(src):
    # normalize a "Title - Author (year)" citation to a title-ish key
    t = src.split(" - ")[0].split(" — ")[0].strip().lower()
    t = re.sub(r"[^a-z0-9 ]+", "", t)
    return re.sub(r"\s+", " ", t)[:70]

with open(os.path.join(SCRATCH, "merged_design.json"), encoding="utf-8") as f:
    data = json.load(f)

by_corpus = defaultdict(list)   # corpus_id -> [element ids]  (membership candidates)
by_title = defaultdict(lambda: {"srcs": set(), "els_naming": [], "els_extra": []})  # new-work candidates

for e in data["elements"]:
    if e.get("named_in_corpus_id"):
        by_corpus[e["named_in_corpus_id"]].append(e["id"])
    else:
        k = title_key(e["named_in"])
        by_title[k]["srcs"].add(e["named_in"][:120])
        by_title[k]["els_naming"].append(e["id"])
    for s in e.get("sources_all", [])[1:]:
        if s.get("corpus_id"):
            if e["id"] not in by_corpus[s["corpus_id"]]:
                by_corpus[s["corpus_id"]].append(e["id"])
        else:
            k = title_key(s["src"])
            by_title[k]["srcs"].add(s["src"][:120])
            if e["id"] not in by_title[k]["els_naming"]:
                by_title[k]["els_extra"].append(e["id"])

out = {
    "memberships": {k: sorted(v) for k, v in sorted(by_corpus.items(), key=lambda x: -len(x[1]))},
    "new_work_candidates": [
        {"key": k, "citations": sorted(v["srcs"]), "naming_for": sorted(set(v["els_naming"])),
         "also_source_for": sorted(set(v["els_extra"]))}
        for k, v in sorted(by_title.items(), key=lambda x: -(len(x[1]["els_naming"]) + len(x[1]["els_extra"])))
    ],
}
with open(os.path.join(SCRATCH, "phase2_sources.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print(f"membership candidate works: {len(out['memberships'])}")
print(f"new-work candidate titles: {len(out['new_work_candidates'])}")
print("top memberships:", {k: len(v) for k, v in list(out['memberships'].items())[:12]})
print("top new works:")
for w in out["new_work_candidates"][:15]:
    print(f"  [{len(w['naming_for']) + len(w['also_source_for'])}] {w['citations'][0][:90]}")
