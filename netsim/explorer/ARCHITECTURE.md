# ARCHITECTURE.md — single-viewport corpus explorer

## What this is

`netsim/` holds two research-corpus reports: a general **networks & systems M&S** corpus anchored
on the 2015 Obaidat/Zarai/Nicopolitidis volume, and a **MATLAB/Simulink tool-family intersection**
corpus. Both are entry lists under a strict tag + verification discipline. This app makes them
navigable without changing a word of their claims. It follows the `SWE/explorer` and
`calculus/explorer` architecture and the `web_manifests/` principles (functional core / imperative
shell, injected-logger seam, parse-at-boundary, single-source state, global failure backstops,
strict-JSDoc typing) for **one 16:9 4K / 27" fullscreen viewport with no page scroll**.

## Constraints honored

Raw HTML/CSS/JS. **No framework, no bundler, no build step at *view* time**; opens from `file://`.
Because `fetch()` of JSON is blocked on `file://`, the data ships as classic `<script>`s assigning
into `window.NET`; the JSON twins are inspectable phase artifacts. Hard separation:
**data carries no behavior, logic carries no resources, presentation carries no data.**

**Single viewport.** The whole app is `100dvh`, `overflow:hidden`. The stage is a two-column grid —
the active model on the left, a **persistent inspector dock** on the right. Every model fits its
pane through internal scroll regions. Verified over HTTP at 1600×900:
`body.scrollHeight === innerHeight`, all five models rendering, zero console errors.

## File tree

```
explorer/
├─ index.html                 shell: header + model tabs, view mount, inspector dock, <script> order
├─ ARCHITECTURE.md  MODELS.md  README.md
├─ package.json  tsconfig.json committed checker (tsc) + test (vitest/playwright/fast-check) toolchain
├─ build/
│  └─ build.py                PHASE 1–4 (Python) — the only place report text is read
├─ data/                      DATA (generated; no behavior)
│  ├─ corpus.js  corpus.json            fact layer   (NET.corpus)
│  ├─ relations.js  relations.json      inference layer (NET.relations)
│  └─ corpus_report.md                  the build's parse + verification log
├─ logic/                     LOGIC (runtime; no hard-coded resources)
│  ├─ log.js                  injected no-op logger seam + console router (observability §4)
│  ├─ util.js                 DOM helpers, invariant(), subfield/paradigm/verification maps
│  ├─ parse.js                boundary parse: unknown → typed corpus/relations, or ValidationError
│  ├─ state.js                single state + pub/sub + location.hash (view,q,ver,corpus,sel)
│  ├─ core.js                 FUNCTIONAL CORE — visible set, facets, strata, anchor map, triage
│  ├─ inspector.js            persistent dock (model-aware overview / entry detail) [shell]
│  ├─ views/anchor.js         Model 1 — anchor map [shell]
│  ├─ views/facets.js         Model 2 — tag lattice [shell]
│  ├─ views/timeline.js       Model 3 — chronology strata [shell]
│  ├─ views/matlab.js         Model 4 — MATLAB/Simulink lens [shell]
│  ├─ views/triage.js         Model 5 — verification triage [shell]
│  └─ app.js                  bootstrap: global handlers, parse, registry, toolbar, keyboard
└─ styles/                    PRESENTATION (no data)
   ├─ tokens.css              palette (13 subfield + 6 paradigm + 3 verification hues), type, spacing
   └─ app.css                 single-viewport layout + per-view internal layouts
```

## The build parses the reports — and is the verifier

Unlike `SWE/explorer` (whose sources were prose reports, hand-transcribed into `records_*.py`)
these corpora are **machine-regular entry lists**, so `build.py` parses the markdown directly:
zero transcription drift, and the reports in `netsim/` remain the single source of truth. The
parse is defensive and fails loud: exact entry counts (158+15 GEN, 61+8 MAT) and contiguous
numbering are asserted; every tag block must split into exactly four fields against the reports'
own legends; verification/recency values normalize to closed vocabularies with qualifiers carried
verbatim (including GEN U12's honest `?` recency — the report's own recall-gap marker).

Cross-corpus merging is deliberately conservative: a MAT entry merges into its GEN twin **only**
when an explicit `[GEN-CORPUS …]` flag *and* a shared hard identifier (DOI/ISBN/arXiv) agree —
exactly two nodes qualify (Obaidat/Boudriga 2010; the NYUSIM COMST tutorial). Family-level
overlaps (the Vienna simulators) stay separate nodes joined by `overlaps` edges. Derived edges
come from three groundable sources only — overlap flags, literal "item N" references, and one
entry's identifier appearing in another's text — never semantic inference. The full log ships as
`data/corpus_report.md`.

## Functional core / imperative shell

`core.js` is a **pure** function library — no DOM: `visibleIds` (search + verification + corpus),
`facetCount`/`passLocal`, `strataBuckets` (year/living/undated), `anchorColumns` (membership
assembly for the anchor map), `paradigmBuckets`, `triage`, `stats`. Every view under `views/` is a
thin **shell**: it calls the core, projects the result to DOM, and wires interaction.

## State & view lifecycle

```
state = { view, q, ver, corpus, sel }   // one mutation entry point; round-trips through location.hash
```

Unidirectional: **event → set → notify → render**. `state.js` uses the value-compared
`hashchange` self-echo guard (first shipped in `calculus/explorer`): programmatic hash writes fire
`hashchange` asynchronously, so self-echoes are recognized by comparing the hash against the
serialized current state rather than with a mute flag — no phantom re-emits, no lost keystrokes.

## Manifest compliance map

| Principle | Where |
|---|---|
| Functional core / imperative shell | `core.js` (pure) vs `views/*` + `inspector.js` (shell) |
| State in JS; DOM is a projection; never read state from the DOM | `state.js`; views re-project on notify |
| Parse, don't validate at every inward boundary | build-time: the markdown parse gauntlet; view-time: `parse.js` |
| `console.assert` never enforces — explicit throw | `util.invariant()` / `assertNever` |
| No browser logging architecture — inject a logger, default no-op | `log.js`; views take `log`, never call `console.*` |
| Errors never pass silently — two global backstops | `app.js` `window` `error` + `unhandledrejection`; bootstrap `try/catch` renders a load-error state |
| Use the platform before writing JS | `URLSearchParams`, CSS grid / `dvh`, native scroll regions |
| Strict typing of raw JS via tsc + JSDoc | `tsconfig.json` (strict `checkJs`) + JSDoc typedefs |
| Accessibility first-class | tablist with arrow-key traversal + `aria-selected`; chips/cards `role=button tabindex=0`; `1–5 / v c Esc` keys; colour never sole channel (verification also badges + dotted borders, corpus also chips) |

## Architectural decisions (recorded)

- **Baseline target: Widely available as of 2026-07.** Language floor ES2022.
- **Parse-the-report build** — the entry format is regular enough that transcription would only
  add drift; the reports stay authoritative, and a report edit + rebuild flows through.
- **No node-link graph view** — the corpora state no edge list; drawing one would fabricate
  structure. The anchor map (parts × routes × entries) is the structural centerpiece instead, and
  the 17 derived reference edges surface in the inspector only.
- **Conservative merging** — two identity merges, both double-grounded; everything else stays
  separate with typed `overlaps` edges. Collect-don't-exclude is the reports' own rule.
- **Verification is a global filter, not just a badge** — the three-grade discipline is the
  corpora's most load-bearing property; it cuts across every model.
- **Telemetry: none** (observability §6 honest default).

## Honesty affordances

Every entry wears its verification grade verbatim (qualifiers included — "(draft); RFC status
unverified", "-single-source"); quarantined entries render dotted and carry a QUARANTINED badge;
the inspector's "cite downstream?" line quotes the reports' own legend; the MAT packaging-
migration note (explicitly "load-bearing for anti-fabrication") is a persistent banner; derived
edges show the exact flag/reference/identifier that grounds them; the coverage summaries —
including where recall thins — are quoted whole in Triage. Nothing is smoothed over.
