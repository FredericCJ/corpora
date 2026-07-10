# ELEMENT-layer mission — resume state (halted 2026-07-10, ~22:40)

Mission spec: `SWE/MISSION_design_elements_v1.md`. Expansion log so far:
`SWE/EXPANSION_REPORT_2026-07-10_elements.md`. This directory is the durable working state —
the session scratchpad it was copied from will not exist in a future session.

## Where the mission stands

| phase | status |
|---|---|
| **Phase 1 — design-element catalog** | **COMPLETE.** `SWE/design_elements_catalog_v1_0.md` — 708 elements, 22 axes, 158 borderline, 203 parked-to-architecture, 316 notable exclusions, 32-entry decision log. Saturation rule satisfied (713 raw → +105 → +25 with adversarial verdict SATURATED). Expansion-report Phase 1 section written. |
| **Phase 2 — pass-8 resource report** | **IN PROGRESS, halted mid-fleet.** The 11-route verification workflow was stopped ~13 min in; **no route output landed** (`p2out/` empty). All inputs are preserved; the fleet re-runs cleanly from them. |
| Phase 3 — architecture catalog + bridge | not started. Intake ready: 203 parked candidates live in the catalog's decision log (also `merged_design.json.parked_architecture` with per-scout provenance). |
| Phase 4 — explorer integration | not started. |

## What is in this directory

- `merged_design.json` — **the master working set**: all 708 elements with full fields incl.
  `sources_all` (per-element source provenance beyond `named-in` — Phase 2's raw material),
  `parked_architecture` (Phase 3a intake), `excluded_notable`, scout notes.
  The catalog `.md` is generated FROM this; treat this JSON as source of truth for tooling,
  the `.md` as the human/deliverable form (they are in sync as of the halt).
- `decisions_design.json` — the 32-entry decision log (also rendered in the catalog).
- `elements_index.txt` — one-line-per-element index (id | name | aka | kind) used by hunter agents.
- `work_ids.tsv` — corpus work ids (id, year, type, title) extracted from
  `SWE/explorer/data/corpus.json` (468 works) for membership lookup + id-collision checks.
- `phase2_sources.json` — aggregation of element naming sources: 56 membership-candidate corpus
  works + 385 raw new-title clusters (pre-curation).
- `p2/r1.json … r11.json` — **the 11 route payloads for the Phase 2 fleet** (each: the route's
  elements with id/name/kind/named_in/corpus-id/other-sources). Route map:
  r1 oo+construction+testing (105) · r2 communication (43) · r3 embedded+scheduling+numeric (51) ·
  r4 execution (37) · r5 synchronization (57) · r6 data+persistence+caching (97) ·
  r7 idioms+functional+data-rep (70) · r8 error+robustness-security (90) ·
  r9 parsing+serialization (41) · r10 flow+state/UI/games (61) · r11 resource-management (56).
- `p2out/` — route-fleet output dir (**empty**: nothing finished before the halt).
- `sweeps/` — full raw provenance: 19 scout files + `gaps/` (round-2 hunters) + `gaps2/`
  (round-3 hunters incl. the adversarial-final verdict and `gap2-editor.json`).
- `tools/` — the pipeline scripts. All Python scripts locate their data via
  `os.path.dirname(__file__)`, so **run them from a copy placed in the directory that holds the
  data files** (or copy the data next to them):
  - `merge.py` (round-1 union-find merge — already applied; kept for provenance)
  - `merge_incremental.py <gapsdir>` (folds a hunter round into `merged_design.json`)
  - `fixup1.py`, `fixup2.py` (adjudications — already applied; DO NOT re-run)
  - `emit_catalog.py` (merged_design.json → `SWE/design_elements_catalog_v1_0.md`)
  - `aggregate_sources.py` (→ `phase2_sources.json`)
  - `assemble_pass8.py` (p2out/*.json → `pass8_works.json` + reachability audit — not yet run)
  - `emit_pass8.py` (pass8_works.json → `SWE/design_elements_corpus_v1_0.md`; reads optional
    `pass8_summary_prose.md` for the honest-gaps section — write that prose after assembly)
  - `pass8_routes_workflow.js` — the exact Workflow script that was running when halted.

## How to resume Phase 2

1. Copy this directory's contents into the new session's scratchpad (or point the tools at it).
2. Edit `tools/pass8_routes_workflow.js`: replace the old scratchpad path constant
   (`C:/Users/frede/AppData/Local/Temp/claude/E--dev-corpora/af68f286-…/scratchpad`) with the new
   working location. The old run cannot be workflow-resumed across sessions — relaunch it fresh
   (11 agents, effort high, ~15–25 min; each writes `p2out/<route>.json` and returns a summary).
3. `python assemble_pass8.py` — dedups works across routes (memberships by corpus id, new works by
   normalized title), checks proposed ids against work ids AND element ids, audits that all 708
   elements are covered or explicitly gapped. Fix flagged problems (bogus element ids, membership
   ids not in `work_ids.tsv`).
4. Write `pass8_summary_prose.md` (honest-gaps coverage summary, house style — see
   `SWE/swe_process_corpus_v1_0.md` §Coverage summary for the register), then
   `python emit_pass8.py` → `SWE/design_elements_corpus_v1_0.md`.
5. Append the Phase 2 section to `SWE/EXPANSION_REPORT_2026-07-10_elements.md` (counts: works,
   memberships vs new, verified vs unverified, coverage, gaps) and mark task #2 complete.

Phase 2 discipline reminders (from the mission): memberships REUSE exact existing ids; `verified`
only on a live-loaded primary page THIS session (old sessions' loads do not carry over — the
route fleet must re-verify, which the relaunch does anyway); no fabricated identifiers; every
element reachable or an explicit gap.

## Then Phases 3–4 (not started)

- **3a** architecture catalog: same pipeline shape as Phase 1 (scouts → merge → gap hunt →
  saturation → emit `SWE/architecture_elements_catalog_v1_0.md`, realm: architecture). Intake:
  the 203 parked candidates (in `merged_design.json.parked_architecture` with scout provenance +
  rationales) PLUS canonical sweeps (Bass–Clements–Kazman tactics, POSA1 styles, Shaw–Garlan,
  Taylor–Medvidovic–Dashofy incl. connector taxonomy, ISO/IEC/IEEE 42010, embedded reference
  architectures — most naming sources are already corpus works, cite their ids).
- **3b** bridge: define the minimal edge-kind vocabulary, then fan out per design-axis agents
  (each gets its axis's design elements + the full architecture index) to propose typed,
  provenance-tagged (sourced|editorial) edges; mechanical audit: every design element ≥1 edge to a
  specific architecture element or on the unbridged list; report sourced:editorial ratio.
  Emit `SWE/design_elements_bridge_v1_0.md`.
- **4** explorer: read `SWE/explorer/ARCHITECTURE.md` + `MODELS.md` + `build/build.py` first;
  elements enter as a new node kind in two realms; build parses the three deliverable `.md` files
  (entry format is machine-parseable by design — `### <id> — <Name>` + fixed bullet keys, and
  pass-8 `elements:` lines); build must audit completeness (built counts == catalog headers) and
  the bridging rule; 3–5 semantic element views documented in MODELS.md; page scroll authorized
  for element views only (record the deviation); verify with `python build/build.py` clean +
  served smoke test; update README/MODELS/index.html; final expansion-report section.

## Workflow run ids from the halted session (for the record only — not resumable cross-session)

- Phase 1 scouts: `wf_fdd73800-53b` · gap round 2: `wf_6a58d284-ba0` · round 3: `wf_7a9662e3-5c1`
- Phase 2 routes (halted): `wf_c8411cad-de9` / task `wd3mj7to0`

Catalog invariants to preserve when regenerating: element ids are STABLE (they become Phase 4
node ids); one element per mechanism (aliases in `aka`); GoF/POSA names canonical; `corpus:<id>`
named-in prefix means the work is already in `explorer/data/corpus.json`; borderline entries
always carry an inline rationale; kind axes are scaffolding, not ontology.
