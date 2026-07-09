# corpus_report.md — build + verification log (netsim explorer)

Sources parsed directly (no hand transcription): `MS_networks_systems_corpus_v1_0.md`, `MATLAB_Simulink_network_MS_corpus_v1_0.md`. Collection date stated in both: 2026-07-09.

## PHASE 1 — parse
- GEN: 176 numbered entries + 18 quarantined across 18 sections.
- MAT: 81 numbered entries + 8 quarantined across 10 sections.
- numbering contiguous in both reports (GEN 1..176, MAT 1..81).

## PHASE 2 — normalize tags, resolve identifiers, merge overlaps
- tag vocabularies validated; 15 verification qualifiers carried verbatim (e.g. “(draft); RFC status unverified”, “-single-source”).
- MERGED m33 into g106 (shared identifier 10.1109/COMST.2023.3344671; flag '[GEN-CORPUS overlap: item 106 there]'); both citation strings carried.
- MERGED m61 into g1 (shared identifier 978-0-471-26983-0; flag '[GEN-CORPUS item 1]'); both citation strings carried.
- derived edges: 32 (Counter({'mentions': 26, 'overlaps': 5, 'named-in': 1})) — from explicit flags, item-number references, and shared hard identifiers only; no semantic inference.

## PHASE 3 — structural verification
- verification split: 179 verified[WEB] / 78 verified[TRAIN] / 24 unverified; 26 entries live in the quarantine sections (§17 GEN / §9 MAT).
- chronology: 214 entries with a parsed year, 57 living (continuous/maintained), 10 undated (fall back to their recency tag in the timeline).
- multi-paradigm MAT entries (split of “+/→” tags): ['m29', 'm34'].
- all edge endpoints resolve; merged aliases rewritten.

## PHASE 3.5 — editorial overlays
- didactic: 61 members / 60 edges — ACYCLIC (Kahn over all members), level-monotone; per level: d0:4, d1:7, d2:8, d3:16, d4:13, d5:13; same-level edges: m19→m2, m19→m24, m7→m2, g19→g18, g9→g5, m3→m73, m5→m74, g166→g168, m62→m63, m65→m66, m18→m16, m73→m16, g35→g36, g36→g38, g167→g170, g171→g170, g170→m39, g163→g164, g26→g173, g173→m81, g176→m80, g64→g66, g74→g78, g66→g87.
- specialization: 65 members / 56 edges — ACYCLIC (Kahn over all members), level-monotone; per level: s0:11, s1:18, s2:16, s3:20; same-level edges: g171→g170, m39→m40, g162→g175, g159→g162, m37→m38, g36→g38, g41→m80.
- provenance stamped on both overlays: 'EDITORIAL overlay — maintainer-curated 2026-07-10; not stated in the source reports. Every edge carries its rationale; treat as reading guidance, not corpus fact.'

## PHASE 4 — emission
- coverage summaries carried verbatim: GEN 5 blocks, MAT 2 block(s).
- wrote data/corpus.json + data/corpus.js
- wrote data/relations.json + data/relations.js

Totals: 282 nodes (1 anchor + 281 entries after 2 merges) · 32 derived edges · 18+10 sections · 179/78/24 web/train/unverified.
