# corpus_report.md — build + verification log (netsim explorer)

Sources parsed directly (no hand transcription): `MS_networks_systems_corpus_v1_0.md`, `MATLAB_Simulink_network_MS_corpus_v1_0.md`. Collection date stated in both: 2026-07-09.

## PHASE 1 — parse
- GEN: 238 numbered entries + 18 quarantined across 26 sections.
- MAT: 81 numbered entries + 8 quarantined across 10 sections.
- numbering contiguous in both reports (GEN 1..176, MAT 1..81).

## PHASE 2 — normalize tags, resolve identifiers, merge overlaps
- tag vocabularies validated; 15 verification qualifiers carried verbatim (e.g. “(draft); RFC status unverified”, “-single-source”).
- MERGED m33 into g106 (shared identifier 10.1109/COMST.2023.3344671; flag '[GEN-CORPUS overlap: item 106 there]'); both citation strings carried.
- MERGED m61 into g1 (shared identifier 978-0-471-26983-0; flag '[GEN-CORPUS item 1]'); both citation strings carried.
- derived edges: 32 (Counter({'mentions': 26, 'overlaps': 5, 'named-in': 1})) — from explicit flags, item-number references, and shared hard identifiers only; no semantic inference.

## PHASE 3 — structural verification
- verification split: 241 verified[WEB] / 78 verified[TRAIN] / 24 unverified; 26 entries live in the quarantine sections (§25 GEN / §9 MAT).
- chronology: 275 entries with a parsed year, 58 living (continuous/maintained), 10 undated (fall back to their recency tag in the timeline).
- multi-paradigm MAT entries (split of “+/→” tags): ['m29', 'm34'].
- all edge endpoints resolve; merged aliases rewritten.

## PHASE 3.5 — editorial overlays
- didactic: 83 members / 88 edges — ACYCLIC (Kahn over all members), level-monotone; per level: d0:4, d1:7, d2:10, d3:23, d4:16, d5:23; same-level edges: m19→m2, m19→m24, m7→m2, g19→g18, g9→g5, m3→m73, m5→m74, g166→g168, m62→m63, m65→m66, m18→m16, m73→m16, g35→g36, g36→g38, g167→g170, g171→g170, g170→m39, g163→g164, g26→g173, g173→m81, g176→m80, g64→g66, g74→g78, g66→g87, g41→g177, g177→g179, g179→g180, m18→g181, g64→g183, g64→g210, g64→g217, g210→g216, g64→g216, g66→g211, g66→g212, g74→g199, g74→g196, g199→g196, g44→g203, g35→g209, g16→g218, g9→g236.
- specialization: 127 members / 129 edges — ACYCLIC (Kahn over all members), level-monotone; per level: s0:15, s1:32, s2:51, s3:29; same-level edges: g171→g170, m39→m40, g162→g175, g159→g162, m37→m38, g36→g38, g41→m80, g41→g178, g177→g178, g177→g179, g179→g180, g41→g211, g41→g212, g186→g187, g41→g190, g41→g197, g41→g200, g41→g204, g44→g203, g203→g208, g44→g208, m29→g202, g200→g205, g200→g207, g16→g218, g218→g223, g218→g226, g11→g221, g221→g219, g221→g220, g220→g222, g221→g225, g225→g227, g36→g228, g229→g230, g229→g232, g231→g234.
- provenance stamped on both overlays: 'EDITORIAL overlay — maintainer-curated 2026-07-10; not stated in the source reports. Every edge carries its rationale; treat as reading guidance, not corpus fact.'

## PHASE 3.6 — typed reading relations
- typed edges: 395 over 235 resources (178 extra-editorial + 188 overlay-editorial + 29 derived).
- by kind: prerequisite-of:95, refines:14, subsumes:2, formalizes:1, surveys:29, applies-method-of:140, companion:44, evaluates:6, critiques:3, supersedes:8, part-of:7, references:46.
- by provenance: derived 29 / editorial 366; 13 cycle(s) tagged: C1(2), C2(6), C3(50), C4(2), C5(4), C6(2), C7(3), C8(4), C9(8), C10(3), C11(4), C12(7), C13(2).

## PHASE 4 — emission
- coverage summaries carried verbatim: GEN 6 blocks, MAT 2 block(s).
- wrote data/corpus.json + data/corpus.js
- wrote data/relations.json + data/relations.js

Totals: 344 nodes (1 anchor + 343 entries after 2 merges) · 395 typed edges (32 mechanical cross-refs) · 26+10 sections · 241/78/24 web/train/unverified.
