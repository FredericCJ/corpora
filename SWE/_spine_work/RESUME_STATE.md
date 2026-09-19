# PASS 9 — the architecture spine — INGESTED & VERIFIED (2026-09-20), NOT COMMITTED

Mission: `SWE/MISSION_arch_spine_v1.md`. Full narrative: `SWE/EXPANSION_REPORT_2026-09-20_spine.md`.

## What is done

| mission phase | state | headline |
|---|---|---|
| 0 · calibration | done | `id_index.tsv` — the 468 pre-existing works, greppable, for membership resolution |
| 1 · spine scouts | done | round 1: 16 scouts + 4 gap-fill + 3 adversarial critics → 438 unique works |
| 2 · domain scouts | done | round 2: 8 recall agents over all 468 existing works + 12 targeted gap scouts + 3 auditors |
| 3 · the two deltas | **NOT DONE** | hand↔model delta table + the obligations primer — the harvest that feeds them is ready |
| 4 · pass report | done | `EXPANSION_REPORT_2026-09-20_spine.md` (the census lives there, not in a separate pass file) |
| 5 · explorer | done | view 12 `Spine`; 12 views; zero console errors; single-viewport invariant held |

**Pass 9 = 796 works** (454 new nodes + 342 memberships). Corpus **468 → 922 nodes**, 7 → 8 corpora.

## Where the canonical data lives

- **Build source (regenerable, the thing that matters):** `explorer/build/records_spine.py`, generated
  from `_spine_work/merged_v4.json`. Registered in `explorer/build/build.py` behind a
  `try: import records_spine` guard, so the first eight passes build with or without it.
- **Generated:** `explorer/data/corpus.{json,js}` (922 nodes) and `relations.json`
  (`views.spine.thin` = the 20 thin-cell adjudications).
- **View:** `explorer/logic/views/spine.js`; wired in `index.html`, `logic/app.js` (registry + tab
  separator, gated on spine data existing), `logic/util.js` (8th corpus), `logic/views/facets.js`
  (two new facets), `logic/inspector.js`, `styles/tokens.css`, `styles/app.css`.

## The harvest chain (each step re-runnable, in order)

```
_spine_work/harvest/*.json      round 1, 20 files        585 raw claims
   -> merged_v1.json            (merge + dedup)          438 unique
   -> merged_v2.json            repair_spine.py          437  [82 false-verified demoted, bundles adjudicated]
_spine_work/harvest2/*.json     round 2 gaps, 12 files   220 claims (177 verified)
_spine_work/recall/*.json       round 2 recall, 8 files  468 judged, 334 claimed
   -> merged_v3.json            tools/merge_v3.py        801 unique
   -> merged_v4.json            tools/repair_v4.py       797  [88 more demoted, anchors 272->92, 4 dups, 2 dead DOIs]
   -> thin_cells.json           tools/thin_cells.py <round1.output> <round2.output>
   -> records_spine.py          tools/gen_records.py
   -> python explorer/build/build.py
```

The two workflow output files the thin-cell step needs are the task outputs of runs
`wf_f5a03326-854` (round 1) and `wf_79945bbf-4f7` (round 2); their per-agent journals are under
`~/.claude/projects/E--dev-corpora/<session>/subagents/workflows/<run>/journal.jsonl`.

## Verify from clean

```
cd explorer/build && python build.py          # expect: PHASE 1: 1330 records -> 922 nodes
cd .. && python -m http.server 8098           # then open http://localhost:8098/#view=spine
```
Expect 12 tabs, zero console errors, and the matrix row `model-c` reading 13 / 88 / 42 / 109 / 140.
`index.html` also opens directly from `file://` (the house constraint) — the HTTP server is only
needed because the Chrome extension refuses `file://`.

## What to pick up next, in priority order

1. **Mission Phase 3** — the hand↔model delta and the obligations primer. This is the pass's
   intellectual payload and the only mission phase not delivered.
2. **The 24 still-absent critic-named works**, chiefly two clusters that both rounds ran out of
   web-search budget before reaching: the runtime-ops wire-protocol/observability set (RFC 5424,
   MQTT/ISO 20922, LwM2M, CoAP, Gregg, Limoncelli) and the complexity-science set (FRAM, *Resilience
   Engineering in Practice*, *Out of the Tar Pit*, Curtis et al.). Both are **sweep-thin**. Also
   absent corpus-wide: **ISO/IEC 9899**, the C standard itself.
3. **Re-verify the 15 ISO-family entries** from the `b3` scout — `iso.org` 403s programmatic fetches,
   so their designations are unconfirmed. Needs a route that renders those pages.
4. **`elements.json` build non-determinism** — structurally identical, different hash every build,
   from set-iteration ordering in `build_elements.py`. Pre-existing; it masks real element-layer
   changes behind a ~5000-line phantom diff.
5. **Manageability tactics in the architecture-element catalog** — exactly 1, against a `runtime-ops`
   domain now carrying 209 works. Adjacent to this mission, never in its scope.

## Caveats a future session must not lose

- **Verification here means a primary page was loaded, full stop.** A membership grep is not
  verification (82 demoted in round 1); neither is an iso.org search snippet, a retail listing, or
  aggregator metadata (88 more demoted in round 2). Pass-9 new nodes are **51% verified** and that
  lower number is the honest one.
- **The cross-product grid over-counts.** Mean fan-out is 2.84 cells per work; restricted to works
  with ≤2 stages and ≤2 domains the grid is materially thinner. Use per-cell membership, not sums.
- **No Node runtime on this machine**, so the committed tsc / vitest / playwright toolchain has never
  been run against the spine view. Browser verification was done by hand instead.
- **Nothing is committed.** `git status` shows the build source, the generated data, the view, the
  docs and `_spine_work/` as pending.
