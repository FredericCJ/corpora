# Expansion report — PASS 9, the architecture spine (`arch-spine`)

**Dates.** Specced and harvested 2026-09-19; repaired, ingested and verified 2026-09-20.
**Mission.** `MISSION_arch_spine_v1.md`. **Working state.** `_spine_work/` (+ `RESUME_STATE.md`).

The corpus was strong on *architecture as a body of knowledge* and on *embedded implementation*, and
held nothing on the **derivation chain that connects them**. This pass adds that chain: how a
stakeholder need becomes a binding obligation, becomes a testable architecture requirement, becomes a
design, becomes a toolchain and a running, measured, governed system — in both embedded realizations,
handwritten C and C generated from Simulink models.

## Headline

| | before | after |
|---|---|---|
| corpus nodes | 468 | **922** |
| research passes | 7 (+ element layer) | **8** |
| cross-corpus works | 82 | **357** |
| verified / unverified | 354 / 114 | 585 / 337 |
| explorer views | 11 | **12** |

**Pass 9 itself: 796 works** — **454 new nodes** (231 verified / 223 unverified, 51%) plus **342
memberships** reclaiming works the corpus already held. Two new array facets, `stage` and `domain`,
over a **7 × 5 = 35-cell** coverage matrix; **20 cells** carry a thin-cell adjudication.

## How it was harvested

Three fan-outs, 46 agents, ~5.9M subagent tokens, zero agent errors.

**Round 1 — broad sweep (16 scouts + 4 gap-fill + 3 critics).** Multi-modal by design: ten
domain-side scouts, five stage-side scouts and one source-kind scout doing nothing but confirming
standards designations against their issuing bodies. 585 raw claims → 438 unique works.

**Round 2a — deterministic repair.** No agents. The round-1 critic panel had found that scouts were
claiming `verified` on the strength of an `id_index.tsv` grep, which establishes *membership*, not
bibliography. 82 such entries demoted. Bundle rows adjudicated individually rather than by rule:
three split into constituents, one converted to the `osstyleguides` membership the corpus already
held, four unbounded vendor catch-alls dropped, and one kept intact because *General Principles of
Software Validation; Final Guidance for Industry and FDA Staff* is a single FDA document whose title
contains a semicolon. 10 schema-corrupt tag arrays repaired.

**Round 2b — recall + targeted gaps (8 + 12 + 3 audits).** Eight agents judged **all 468** existing
corpus works against the spine (no web); twelve web scouts worked the vocabularies the critics named
as missing. Gap scouts verified **177 of 220 (80%)** against primary pages and resolved **80 of the
103** critic-named works.

**Round 2c — audit-mandated repair.** The three-lens audit panel returned **NOT READY TO INGEST** with
specific blockers. All were fixed before any id was minted (below).

## Decisions taken, and why

1. **Verification means a primary page, and nothing else.** Beyond the membership-grep rule, round 2
   produced three new costumes of the same error: `iso.org` *search-result snippets*, retail listings,
   and aggregator metadata (dblp / Semantic Scholar / RePEc). A further **88** entries were demoted.
   Final verification for the pass's own new nodes is **51%**, down from a claimed 80% — the lower
   number is the true one. Demoting a genuinely-verified work costs nothing; it stays in the corpus,
   honestly tagged. Keeping a falsely-verified one is permanent damage.
2. **Anchor deflation.** `role:anchor` had reached 34% of the pass, which makes the tag meaningless
   and would have corrupted the census and the Anchors view. Rule applied: within each of the 35
   cells keep at most four anchors, ranked verified-first then by focus (a work tagged into fewer
   cells is a more specific entry point); a work keeps `anchor` if it survives in any cell it serves.
   272 → **92 anchors (12%)**.
3. **Three disputed DOIs settled against the Crossref API, not against an agent's word.**
   `10.1109/ECRTS.2004.35` (TLSF) returns 404 — stripped. `10.5555/257734.257788` (*Software Aging*)
   is an ACM internal id, not a resolvable DOI — stripped. Two scouts asserted *different* DOIs for
   the modularity paper; `10.1145/503209.503224` resolves correctly to Sullivan, Griswold, Cai &
   Hallen, ESEC/FSE 2001, and the competing one was wrong.
4. **Version contradictions inside one harvest are not silently resolved.** Two files asserted
   incompatible current versions of ArchiMate, and one pinned an AUTOSAR document to R24-11 against
   its siblings' R25-11. Both entries are kept and marked unverified with the conflict named.
5. **Duplicates.** Four genuine same-document pairs merged (ARP4754A and ARP4761A each arrived under
   two spellings). Distinct revisions (ARP4761 vs ARP4761A) and distinct annexes (AS5506/1A vs
   AS5506/3) were deliberately **left apart** — they are different documents.
6. **An id collision is a missed membership, not a clash.** When a minted id matched an existing
   corpus node the generator claimed the node instead of minting a duplicate. This caught the
   *Software Systems Architecture* companion site, which collapsed into `rozanski`.

## Where it landed

`corpus.json` is **generated**, so the ingest is a build source, not a patch: `build/records_spine.py`
(generated from `_spine_work/merged_v4.json` by `_spine_work/tools/gen_records.py`) registered in
`build/build.py` behind a `try: import records_spine` guard, so the first eight passes build with or
without it.

The two new facets follow the pass-7 `lang` precedent exactly: set only for `arch-spine` nodes,
**absent — never `UNRESOLVED`** — elsewhere, because the other passes never asserted them. `stage` is
also projected into the shared `theme` vocabulary as `spine-<stage>`, prefixed against collision, so
the Facets and Chronology views surface the spine without knowing pass 9 exists. `core.valuesOf`
already treated an array field as a multi-valued facet, so **the functional core needed no change**.

**View 12 — Spine**: the 35-cell matrix, the chain reading left to right through the column headers,
counts live over real tags, click-to-filter on cell / stage / domain, and thin cells flagged with the
panel's adjudication (△ sweep-thin, ○ literature-thin) sourced from the build, never decided in the
view. Tab spine is now **Body of Knowledge · Elements · Atlas · Spine**.

**Verified in-browser** (no Node runtime on this machine, so the committed tsc/vitest toolchain could
not be run): all 12 views mount, **zero console errors or warnings** on load, every view holds the
single-viewport no-page-scroll invariant, view switching is 7–23 ms, both new facets render with live
counts, cell filtering works (796 → 140 for `model-c × tools-process`), and the inspector carries
both facets. The element and atlas self-audits still pass unchanged (709 + 374 elements, 2811 edges,
21 islands).

## Gaps — explicit, not padded

- **24 of the 103 critic-named works remain absent.** Two clusters account for most: the entire
  runtime-ops wire-protocol and observability seed set (RFC 5424, MQTT / ISO 20922, LwM2M, CoAP,
  Gregg, Limoncelli) and the entire complexity-science set (FRAM, *Resilience Engineering in
  Practice*, *Out of the Tar Pit*, Curtis et al.). Both rounds exhausted a 200-call web-search budget
  before reaching them — these are **sweep-thin, not literature-thin**.
- **ISO/IEC 9899 (the C standard itself) is absent** from the whole corpus, which an auditor called
  out as conspicuous for a corpus with two C-realization domains.
- **The 15 ISO-family entries from the `b3` scout are all unverified**, because `iso.org` returns 403
  to programmatic fetches. Their designations are probably right; nothing confirms them.
- **The cross-product grid over-counts.** A work occupies every stage × domain product of its tags,
  and mean fan-out is 2.84 cells/work. Restricted to unambiguously-tagged works (≤2 stages and ≤2
  domains) the honest grid is materially thinner — recorded in the audit output.
- **Thin cells: 20 adjudicated**, 5 literature-thin and 15 sweep-thin. The panels disagreed on five
  cells; the later, better-informed round won, and where a single panel split, `sweep-thin` won
  because calling a cell literature-thin asserts the field never wrote it and needs consensus.
- **Not done: Phase 3 of the mission** — the hand↔model delta table and the obligations primer
  reconciling the five S2 vocabularies. The harvest that feeds both is now in place.

## Adjacent findings

- **`elements.json` is non-deterministic across builds** — structurally identical, different hash,
  from set-iteration ordering in `build_elements.py`. Pre-existing (`corpus.json` is fully
  deterministic), but it puts a ~5000-line phantom diff on the element layer at every rebuild, which
  hides real changes in review.
- **The architecture-element catalog still carries exactly one manageability tactic** while
  `runtime-ops` is now a first-class domain with 209 works. The element layer is very likely
  under-built there. Flagged in the mission as adjacent; still not acted on.
