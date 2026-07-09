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

## PHASE 4 — emission
- coverage summaries carried verbatim: GEN 5 blocks, MAT 2 block(s).
- wrote data/corpus.json + data/corpus.js
- wrote data/relations.json + data/relations.js

Totals: 282 nodes (1 anchor + 281 entries after 2 merges) · 32 derived edges · 18+10 sections · 179/78/24 web/train/unverified.
