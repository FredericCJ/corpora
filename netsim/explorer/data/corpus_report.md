# corpus_report.md — build + verification log (netsim explorer)

Sources parsed directly (no hand transcription): `MS_networks_systems_corpus_v1_0.md`, `MATLAB_Simulink_network_MS_corpus_v1_0.md`. Collection date stated in both: 2026-07-09.

## PHASE 1 — parse
- GEN: 158 numbered entries + 15 quarantined across 17 sections.
- MAT: 61 numbered entries + 8 quarantined across 9 sections.
- numbering contiguous in both reports (GEN 1..158, MAT 1..61).

## PHASE 2 — normalize tags, resolve identifiers, merge overlaps
- tag vocabularies validated; 14 verification qualifiers carried verbatim (e.g. “(draft); RFC status unverified”, “-single-source”).
- MERGED m33 into g106 (shared identifier 10.1109/COMST.2023.3344671; flag '[GEN-CORPUS overlap: item 106 there]'); both citation strings carried.
- MERGED m61 into g1 (shared identifier 978-0-471-26983-0; flag '[GEN-CORPUS item 1]'); both citation strings carried.
- derived edges: 17 (Counter({'mentions': 12, 'overlaps': 4, 'named-in': 1})) — from explicit flags, item-number references, and shared hard identifiers only; no semantic inference.

## PHASE 3 — structural verification
- verification split: 143 verified[WEB] / 75 verified[TRAIN] / 22 unverified; 23 entries live in the quarantine sections (§16 GEN / §8 MAT).
- chronology: 184 entries with a parsed year, 46 living (continuous/maintained), 10 undated (fall back to their recency tag in the timeline).
- multi-paradigm MAT entries (split of “+/→” tags): ['m29', 'm34'].
- all edge endpoints resolve; merged aliases rewritten.

## PHASE 4 — emission
- coverage summaries carried verbatim: GEN 4 blocks, MAT 1 block(s).
- wrote data/corpus.json + data/corpus.js
- wrote data/relations.json + data/relations.js

Totals: 241 nodes (1 anchor + 240 entries after 2 merges) · 17 derived edges · 17+9 sections · 143/75/22 web/train/unverified.
