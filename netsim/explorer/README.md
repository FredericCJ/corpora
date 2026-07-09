# Network M&S Corpus Explorer

A single-page, single-viewport explorer of a **unified network modeling-and-simulation corpus** —
two research passes merged into one fact layer and navigable through **five relational models**.

- **240 entries + the 2015 anchor volume** · GEN corpus 158 + 15 quarantined
  (`MS_networks_systems_corpus_v1_0.md`) · MAT corpus 61 + 8 quarantined
  (`MATLAB_Simulink_network_MS_corpus_v1_0.md`) · 2 cross-corpus merges (grounded by shared
  identifiers) · 144 verified[WEB] / 75 verified[TRAIN] / 22 unverified · 46 living docs/tools.
- Built in the style + rule set of `web_manifests/` (raw HTML/CSS/JS, no framework, no build step
  at view time) for **one 16:9 4K / 27" display, fullscreen, landscape** — a single viewport with
  no page scroll.

## The five models

1. **Anchor map** — the anchor's six parts vs the routes that expand, supersede, or post-date
   them, relation phrases quoted from the section headers; part verdicts quote the coverage
   summary ("Part 2 most durable; Parts 4–5 most superseded").
2. **Facets** — the tag lattice both reports enforce scope with: corpus × subfield/paradigm ×
   type/stratum × recency, with live counts.
3. **Chronology** — strata around the 2015 anchor datum; continuously-maintained docs/tools are
   their own LIVING stratum; undated entries wear their report-stated recency tag.
4. **MATLAB lens** — the intersection corpus by its six paradigms, stratum-coded, with the
   load-bearing packaging-migration note as a persistent banner.
5. **Triage** — the verification discipline made first-class: the three-grade split with the
   legend verbatim, the quarantine sections as cards, and the coverage self-assessments whole.

A persistent inspector dock shows the active model's method + full legend, or — when you select an
entry — its citation verbatim, tags, route, relevance note, derived references, and a
**"cite downstream?"** guidance line quoting the reports' own verification legend.

## Open it

- **Simplest:** double-click `index.html` — runs from `file://` with zero dependencies.
- **Over HTTP:** `python -m http.server 8096 --directory .`, then open `http://localhost:8096/`.

## Use it

- **Tabs `1–5`** switch models · **`/`** search · **`v`** cycles verification · **`c`** cycles
  corpus · **`Esc`** clears.
- Click any entry anywhere for its full record; the **verification** and **corpus** selectors
  filter every model at once; state round-trips through the URL hash.

## Rebuild the data

The build **parses the two reports directly** — no hand transcription; the markdown files in
`netsim/` stay the single source of truth:

```
python build/build.py     # parses ../..*.md -> data/*.js + *.json + corpus_report.md
```

The build is also the verifier: entry counts and numbering (158+15 / 61+8, contiguous), tag
vocabularies, the two cross-corpus merges (each requires an explicit `[GEN-CORPUS]` flag AND a
shared hard identifier), derived-edge grounding (flags, item-number references, identifier
matches — no semantic inference), and quarantine placement are all machine-checked; the log ships
as [data/corpus_report.md](data/corpus_report.md).

## Checker & tests (committed contract)

`tsconfig.json` (strict `checkJs` over the raw `.js` via JSDoc) and `package.json` pin the mid-2026
toolchain — `typescript` 6.0.x as a checker, `vitest` 4.1.x + `playwright`, `fast-check` for the
pure-core property tests (`core.js` visible-set/facets/strata/buckets are all pure).

```
npm run check     # tsc --noEmit
npm test          # vitest run
```

> Node was unavailable where this was authored, so `check`/`test` are the committed contract, not
> a verified run. The app ships **zero runtime dependencies** and was verified in-browser over
> HTTP at 1600×900: single viewport, no page scroll, all five models rendering, filters/keyboard/
> hash round-trip working (including the rapid-keys-then-type race the calculus explorer fixed in
> `state.js`), strata summing to the full corpus, zero console errors.

## Layout & provenance

- Architecture, the parse-the-report build, and the manifest-compliance map:
  [ARCHITECTURE.md](ARCHITECTURE.md).
- The five models, their computations, and the anti-fabrication discipline:
  [MODELS.md](MODELS.md).
- Source reports: `../MS_networks_systems_corpus_v1_0.md`,
  `../MATLAB_Simulink_network_MS_corpus_v1_0.md` (collected 2026-07-09).
