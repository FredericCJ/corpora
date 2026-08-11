# Embedded C parent booklet — endeavour state

**Status: COMPLETE r1, 2026-08-11.** Single-session write (Fable 5, effort max).
**Nothing committed — user's call, standing house rule.**

## Deliverables

- `E:\dev\corpora\embedded-c-architecture-and-design-r1.md` — the booklet (121 KB, ~19k words).
- `E:\dev\corpora\embedded-c-architecture-and-design-r1.html` — house-styled rendering (143 KB).
- `_embedded_booklet_work\build_html.py` — regenerates the .html from the .md (stdlib-only;
  handles exactly the markdown subset the booklet uses: h1–h3, tables, ul/ol with preserved
  numbering via `value=`, blockquotes, one code fence, inline bold/italic/code).

## What it is

The **parent of the embedded specializations**: principles for complex embedded C —
target/architecture/compiler-agnostic, MMU-optional — maximizing modularity, maintainability,
observability, testability, decoupling. 7 parts / 16 chapters / 24 routed invariants /
7 enforcement routes (`compiler` / `analysis` / `build` / `host-test` / `target-test` /
`runtime` / `contract-only`). Ch. 15 is the specialization contract (what children must pin:
platform hub, toolchain baseline, shell, HAL, memory plan, failure policy, observability plan,
verification plan, process bindings); ch. 16 is the lineage register with the corpus's own
verification flags carried through, plus §16.3 the editorial-claims register.

## Grounding (what was mined)

- SWE element catalogs v1.0 (709 design + 374 arch; ids used verbatim; 191 embedded-tagged
  design elements; kind axes + exclusion registers honored — no invented element names).
- `design_elements_bridge_v1_1.md` (2,811 edges; sourced vs editorial provenance respected).
- `swe_process_corpus_v1_0.md` + `explorer/build/records_{arch,c,cpp,ops,proc}.py` (work ids +
  verification status; emb-arch 140 / emb-c 68 / emb-cpp 80 / emb-ops 53 works).
- `manifests/_work/seed/s1–s4` (element ladders: 5-rung boundary ladder, coupling triangle,
  binding-time ladder, 3-reasons-to-substitute, RTC/superloop constrains edges).
- `manifests/reference/architecture_manifest_default.md` (genre model; not duplicated —
  instantiated), error/logging/testing/module-boundaries manifests (contract skeletons →
  10 cross-file parent laws), `web_manifests/README.md` (translation-map device).
- `netsim/scheduler_prompt/reference_card.md` (RTA / DM / ceiling-protocol keystones, §8.2).

## Re-verification queue (carried in §16.2, flagged UNVERIFIED per corpus)

`hanmer` (year unresolved; names much of ch. 10) · `nygard` (year unresolved; 2007-vs-2018
inconsistency across catalogs) · `posa2` (backs active-object/reactor family) ·
`dsimonprimer` · `pont` · `labrosse` · `freertosbook` (shell + RTOS-mechanism sources) ·
`memfaultea` · `sakscolumns` · `eideregehr` · `preschernplop` · `lakoslsc` · `harel87` ·
`kopetzbauer` · `room` · `embeddedrust`.

## Known corpus data defects noted in the booklet

`core-dump` / `system-tick` carry unexpanded `named-in: white` + char-split tags (7 nodes
affected, see design catalog miner report); Meyer DbC 1988-vs-1997 edition discrepancy;
`azurepatterns` record title is the Cache-Aside page.

## If resuming / extending

Likely next moves: (a) spawn the `embedded_manifests/` child family per ch. 15's table
(platform hub first — the version-hub rule); (b) re-verify the UNVERIFIED queue and bump to r2;
(c) index the booklet's element usage into the SWE explorer as a reading-layer view (the
booklet cites ids that resolve in `SWE/explorer/data/elements.json`). Edit the .md, then run
`python _embedded_booklet_work/build_html.py` to refresh the .html.
