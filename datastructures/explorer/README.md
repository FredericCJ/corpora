# Data-Structure Lineage Explorer

A single-page, single-viewport **lineage graph** of ~110 data structures — from the 17 foundational
roots to the modern research frontier — with every typed relation between them, drawn from two
research reports in the parent folder.

- **110 structures · 121 typed relations · 24 roots · 9 families · 4 genuine cycles.**
- Built in the visual + architectural style of `SWE/explorer`, under the rule set in
  `web_manifests/` (raw HTML/CSS/JS, no framework, no build step at view time).
- Designed for **one 16:9 4K / 27" display, fullscreen, landscape** — the whole app is a single
  viewport with no page scroll; the graph SVG scales to fill.

## Open it

- **Simplest:** double-click `index.html` — it runs from `file://` with zero dependencies.
- **Over HTTP** (also serves the two report `.md`s the inspector links to):
  ```
  python -m http.server 8099 --directory .
  # then open http://localhost:8099/
  ```

## Use it

- **Hover / focus** a structure → its full ancestor + descendant closure lights up (cycles are
  followed and terminate); everything else dims.
- **Click / Enter** a structure → the right dock shows its origin citation, honesty flags, which
  report(s) name it, and every typed relation (kind + provenance + one-line basis + cycle tag).
- **Search** (`/`) narrows by name / author / origin; the **family**, **verification**, and
  **relation** selectors filter; **reset** clears. `Esc` clears the selection then the search.
- The **inspector overview** (nothing selected) is the full legend: relation kinds, provenance &
  honesty markers, families, and the four cycles.

## Rebuild the data

The graph is generated from transcribed report facts (the only place the reports are read):

```
python build/build.py     # build/nodes.py + build/edges.py → data/*.js + *.json + corpus_report.md
```

`build.py` fails loud on any unknown edge endpoint, duplicate id, out-of-vocabulary kind, dangling
cycle tag, or orphan node — the build-time half of the "parse, don't validate" discipline.

## Checker & tests (committed contract)

`tsconfig.json` (strict `checkJs` over the raw `.js` via JSDoc) and `package.json` pin the mid-2026
toolchain — `typescript` 6.0.x as a checker, `vitest` 4.1.x + `playwright` for tests, `fast-check`
for the pure-core property tests (layout/closure are pure and property-testable).

```
npm run check     # tsc --noEmit   (type-check raw JS + JSDoc)
npm test          # vitest run
```

> Node was not available in the environment where this was authored, so `check`/`test` are the
> committed contract, not a verified run. The app itself ships **zero runtime dependencies** and
> was verified in-browser at 3840×2160 (single viewport, no scroll, all 110 nodes / 121 edges
> rendered, hover-closure + inspect + filters working, no console errors).

## Layout & provenance

- Architecture, the single-viewport layout engine, and the full manifest-compliance map:
  [ARCHITECTURE.md](ARCHITECTURE.md).
- The relational model, node/edge semantics, and the anti-fabrication provenance discipline:
  [MODELS.md](MODELS.md).
- Sources: `../compass_artifact_wf-1f7348c0-…md` (the 17-structure audit) and
  `../compass_artifact_wf-95789e49-…md` (the topology lineage graph).
