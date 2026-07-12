# Network M&S Corpus Explorer

A single-page, single-viewport explorer of a **unified network modeling-and-simulation corpus** —
two research passes merged into one fact layer and navigable through **seven relational models**,
including a **typed twelve-kind reading graph** (SWE-parity) over the resources.

- **343 entries + the 2015 anchor volume** · GEN corpus 238 + 18 quarantined
  (`MS_networks_systems_corpus_v1_0.md`) · MAT corpus 81 + 8 quarantined
  (`MATLAB_Simulink_network_MS_corpus_v1_0.md`) · 2 cross-corpus merges (grounded by shared
  identifiers) · 241 verified[WEB] / 78 verified[TRAIN] / 24 unverified.
- A **typed relation layer**: ~320 provenance-tagged edges across twelve reading-relation kinds
  (`prerequisite-of, refines, subsumes, formalizes, surveys, applies-method-of, companion,
  evaluates, critiques, supersedes, part-of, references`), each `derived` (grounded in report text)
  or `editorial` (maintainer rationale). Built 2026-07 (the "typed relations + breadth" expansion).
- Built in the style + rule set of `web_manifests/` (raw HTML/CSS/JS, no framework, no build step
  at view time) for **one 16:9 4K / 27" display, fullscreen, landscape** — a single viewport with
  no page scroll.

## The seven models

1. **Anchor map** — the anchor's six parts vs the routes that expand, supersede, or post-date
   them, relation phrases quoted from the section headers; part verdicts quote the coverage
   summary ("Part 2 most durable; Parts 4–5 most superseded").
2. **Reading graph** — the **typed twelve-kind, directed, cyclic-capable** relation graph between
   resources (the SWE-parity layer): nodes = every resource in ≥1 relation, shelf-packed into
   corpus bands to fit one viewport; edges hued by kind, **editorial dotted / derived solid**; hover
   traces the cycle-safe closure. The per-resource typed-edge catalog (kind · provenance · rationale)
   lives in the inspector.
3. **Overlays (EDITORIAL)** — two maintainer-curated typed-relation graphs over a curated
   subset: **Didactic — ground up** (D0 first contact → D5 frontier; edges = read-before) and
   **Theory → applied** (THEORY → METHODOLOGY → TOOLS → APPLIED specialization chains). Every
   edge is dashed, provenance-stamped, and carries its rationale; hover traces the transitive
   closure. Build-validated: no quarantined members, acyclic, level-monotone. *(These overlays
   seed the Reading graph's editorial edges, re-expressed into the twelve kinds.)*
4. **Facets** — the tag lattice both reports enforce scope with: corpus × subfield/paradigm ×
   type/stratum × recency, with live counts.
5. **Chronology** — strata around the 2015 anchor datum; continuously-maintained docs/tools are
   their own LIVING stratum; undated entries wear their report-stated recency tag.
6. **MATLAB lens** — the intersection corpus by its six paradigms, stratum-coded, with the
   load-bearing packaging-migration note as a persistent banner.
7. **Triage** — the verification discipline made first-class: the three-grade split with the
   legend verbatim, the quarantine sections as cards, and the coverage self-assessments whole.

A persistent inspector dock shows the active model's method + full legend, or — when you select an
entry — its citation verbatim, tags, route, relevance note, derived references, and a
**"cite downstream?"** guidance line quoting the reports' own verification legend.

## Open it

- **Simplest:** double-click `index.html` — runs from `file://` with zero dependencies.
- **Over HTTP:** `python -m http.server 8096 --directory .`, then open `http://localhost:8096/`.

## Use it

- **Tabs `1–7`** switch models · **`o`** jumps to / toggles the overlay · **`/`** search ·
  **`v`** cycles verification · **`c`** cycles corpus · **`Esc`** clears.
- Click any entry anywhere for its full record; the **verification** and **corpus** selectors
  filter every model at once; state round-trips through the URL hash.

## Rebuild the data

The build **parses the two reports directly** — no hand transcription; the markdown files in
`netsim/` stay the single source of truth:

```
python build/build.py     # parses ../..*.md -> data/*.js + *.json + corpus_report.md
```

The build is also the verifier: entry counts and numbering (238+18 / 81+8, contiguous), tag
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
> HTTP at 1600×900: single viewport, no page scroll, all seven models rendering, filters/keyboard/
> hash round-trip working (including the rapid-keys-then-type race the calculus explorer fixed in
> `state.js`), strata summing to the full corpus, zero console errors.

## Layout & provenance

- Architecture, the parse-the-report build, and the manifest-compliance map:
  [ARCHITECTURE.md](ARCHITECTURE.md).
- The seven models, their computations, and the anti-fabrication discipline:
  [MODELS.md](MODELS.md).
- Source reports: `../MS_networks_systems_corpus_v1_0.md`,
  `../MATLAB_Simulink_network_MS_corpus_v1_0.md` (collected 2026-07-09).
