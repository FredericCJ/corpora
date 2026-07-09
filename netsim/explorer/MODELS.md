# MODELS.md — the five relational models

One fact layer (`data/corpus.json`), one inference layer (`data/relations.json`), five ways to
stand in it. Every model states its **semantic**, its **question**, and its **computation** (what
the app derives vs what it merely carries). The governing rule: the reports collect under
*collect-don't-exclude* with scope enforced by tags — so the app **filters and arranges**, it
never ranks, weights, or invents relations.

## Provenance discipline

Three verification grades ride the data end-to-end, exactly as the reports tag them:

- **verified[WEB]** — confirmed live on 2026-07-09 via search/primary source.
- **verified[TRAIN]** — high-confidence training-derived knowledge of existence; *re-verify
  identifiers before downstream citation*. Amber, everywhere it appears.
- **unverified** — plausible but unconfirmed, quarantined in the reports' own §16 (GEN) / §8
  (MAT); *do not cite downstream without live verification*. Dotted borders + QUARANTINED badge.

Qualifiers survive verbatim ("verified[WEB] (draft); RFC status unverified",
"verified[WEB]-single-source", GEN U12's recency `?` — an honest recall-gap marker). Derived
edges exist only where the text grounds them: an explicit `[GEN-CORPUS]` flag, a literal
"item N" reference, or one entry's DOI/arXiv/ISBN appearing in another's text. Each edge carries
its grounding quote in the inspector.

## Model 1 — Anchor map (`views/anchor.js`)

- **Semantic.** The GEN report's own organizing scheme: every route is a stated relation to one
  of the 2015 anchor's six parts — or to none ("did not exist at anchor time").
- **Question.** What happened to each part of the 2015 book, and what exists now that it could
  not contain?
- **Computed.** Membership assembly only (`core.anchorColumns`): part columns ← the hardcoded
  section→part table whose relation phrases quote the section headers; part verdicts quote §17
  ("Part 2 most durable"; "Parts 4 and 5 the most superseded"). Chips are entry item numbers
  coloured by subfield.

## Model 2 — Facets (`views/facets.js`)

- **Semantic.** The tag lattice the reports enforce scope with: corpus × subfield (GEN legend) ×
  paradigm/stratum (MAT legend) × type × recency.
- **Question.** What exists about X, and how much of it can I actually cite?
- **Computed.** Pure filtering with live counts (`core.facetCount`); facets a report never asserts
  are simply absent for its entries. Multi-valued tags ("link-phy-level→wireless-system-level",
  "paper+dataset") are split for faceting and shown raw in the inspector.

## Model 3 — Chronology (`views/timeline.js`)

- **Semantic.** Publication strata around the 2015 anchor datum; living documentation and tools
  (ns-3 releases, MathWorks doc trees, annual venues) are a real stratum of this literature.
- **Question.** What is pre-anchor canon, post-anchor frontier, maintained, or undatable?
- **Computed.** Year parsed from each citation string (a "c. 2016–2018" takes its first year);
  LIVING detected from continuous/maintained/annual wording; unparseable years land in UNDATED
  wearing the entry's own recency tag — no guessed dates.

## Model 4 — MATLAB lens (`views/matlab.js`)

- **Semantic.** The intersection corpus: MATLAB/Simulink *actually applied* to network/system
  M&S, in its six paradigms. Its own verdict: a minority tool whose value is paradigm-specific.
- **Question.** Where is MATLAB/Simulink a real network-M&S vehicle, and on whose word (vendor
  stratum vs peer-reviewed)?
- **Computed.** Paradigm buckets (multi-paradigm entries appear in each of their columns —
  labelled behavior, not double-counting); stratum badges on every card; cross-corpus entries
  link back into GEN. The packaging-migration note — the report calls it *load-bearing for
  anti-fabrication* — is a persistent banner, not a footnote.

## Model 5 — Triage (`views/triage.js`)

- **Semantic.** The reports' citation discipline made first-class, plus their self-assessment.
- **Question.** What may I cite as-is, what must I re-verify, what is quarantined — and where
  does recall thin?
- **Computed.** The three-grade split (counts live; legend verbatim). Carried verbatim: every
  quarantine entry with its "to confirm" note, and the coverage summaries whole — routes swept,
  where recall thins, what has moved on since the anchor, open forks.

## The inspector

Selecting any entry shows: title, corpus membership chips with per-report item numbers, honesty
badges (verification with qualifier, quarantine, living, recency), the citation string verbatim
(both strings for the two merged entries), tags, route (section) per corpus, the relevance note
verbatim, a "cite downstream?" line quoting the verification legend, and every derived reference
with its grounding quote. With nothing selected it explains the active model, the corpus stats,
the full hue/verification legend, and links the build's parse + verification log.
