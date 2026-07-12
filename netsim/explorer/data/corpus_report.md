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
- didactic: 61 members / 60 edges — ACYCLIC (Kahn over all members), level-monotone; per level: d0:4, d1:7, d2:8, d3:16, d4:13, d5:13; same-level edges: m19→m2, m19→m24, m7→m2, g19→g18, g9→g5, m3→m73, m5→m74, g166→g168, m62→m63, m65→m66, m18→m16, m73→m16, g35→g36, g36→g38, g167→g170, g171→g170, g170→m39, g163→g164, g26→g173, g173→m81, g176→m80, g64→g66, g74→g78, g66→g87.
- specialization: 65 members / 56 edges — ACYCLIC (Kahn over all members), level-monotone; per level: s0:11, s1:18, s2:16, s3:20; same-level edges: g171→g170, m39→m40, g162→g175, g159→g162, m37→m38, g36→g38, g41→m80.
- provenance stamped on both overlays: 'EDITORIAL overlay — maintainer-curated 2026-07-10; not stated in the source reports. Every edge carries its rationale; treat as reading guidance, not corpus fact.'

## PHASE 3.6 — typed reading relations
- typed edges: 320 over 235 resources (178 extra-editorial + 113 overlay-editorial + 29 derived).
- by kind: prerequisite-of:70, refines:14, subsumes:2, formalizes:1, surveys:29, applies-method-of:90, companion:44, evaluates:6, critiques:3, supersedes:8, part-of:7, references:46.
- by provenance: derived 29 / editorial 291; 8 cycle(s) tagged: C1(2), C2(18), C3(2), C4(2), C5(3), C6(4), C7(2), C8(2).

## PHASE 4 — emission
- coverage summaries carried verbatim: GEN 5 blocks, MAT 2 block(s).
- wrote data/corpus.json + data/corpus.js
- wrote data/relations.json + data/relations.js

Totals: 344 nodes (1 anchor + 343 entries after 2 merges) · 320 typed edges (32 mechanical cross-refs) · 26+10 sections · 241/78/24 web/train/unverified.
