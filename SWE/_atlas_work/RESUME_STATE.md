# ATLAS endeavour — COMPLETE (2026-07-11)

All three workstreams of `SWE/ATLAS_PLAN.md` are delivered and verified. Full narrative:
`SWE/EXPANSION_REPORT_2026-07-11_atlas.md`. Frozen model: `SWE/ATLAS_SPEC.md`.

## Deliverables (on disk)

| WS | deliverable | headline |
|---|---|---|
| 1 | `SWE/design_elements_bridge_v1_1.md` | **2811 relations** (was 1132); +1679 within-realm (695 sourced : 984 editorial); 0 disconnected arch, 0 sibling-less design; new `uses` kind |
| 2 | `SWE/ATLAS_SPEC.md` + `explorer/build/element_src/atlas.json` | **21 named emergent islands**, Q≈0.70, deterministic byte-identical geography |
| 3 | `explorer/` views 10 (Atlas) + 11 (Bridge-Flow) | build PHASE 5 self-audits; 11 views, zero console errors; 9 prior views unregressed |

## Canonical data now

- `explorer/build/element_src/bridge.json` — the enriched 2811-edge relation set (v1.1; replaced v1.0's 1132).
- `explorer/build/element_src/atlas.json` — the consolidated islands + precomputed geography (WS2 output).
- `python explorer/build/build.py` rebuilds everything (PHASE 4 elements + PHASE 5 atlas) and self-audits.

## The `_atlas_work/` pipeline (re-derivation, in run order)

1. `gen_scope.py` → `scope/*.json` (25 research groups) + `id_index*.txt` — the WS1 scope map.
2. **Workflow `ws1-relation-enrichment`** (50 agents) → `harvest/*.json` then `final/*.json` per group.
3. `merge_relations.py` → `bridge_v1_1.json` + `merge_stats.json` (validate/dedup/degree-cap/1C).
   Then copied to `explorer/build/element_src/bridge.json`.
4. `consolidate.py` (uses `families.py`) → `islands.json` — deterministic Louvain + curation.
5. naming agent → `island_names.json` (from `naming_brief.json`).
6. `layout_atlas.py` (uses `families.py`) → `explorer/build/element_src/atlas.json` — deterministic layout.

## Rebuild / verify from clean

```
python explorer/build/build.py        # 5 phases; P4+P5 self-audit, fail loud on mismatch
```
UI (Node unavailable): headless Chrome `--dump-dom --enable-logging=stderr` over a served
`python -m http.server` — all 11 tabs mount, L0→L1→L2 atlas nav + bridge-flow + teleport, zero JS
errors, nine prior views unregressed. (Harness used: `scratchpad/verify_atlas.sh`.)

To re-run only WS1 research with edited post-processing, resume the workflow from its runId (see the
expansion report / workflow script under the session's `workflows/scripts/`), or just re-run
`merge_relations.py` over the existing `final/*.json`.

## Not done (by design)

Committing is the user's call — nothing was committed. The working tree carries all deliverables, the
explorer changes, and this working dir.
