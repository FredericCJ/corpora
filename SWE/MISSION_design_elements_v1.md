# MISSION — The ELEMENT layer: a design-element catalog for the SWE corpus (4 phases)

You are working in the repo at `E:\dev\corpora`. **Unlimited web research (search + fetching
primary pages) is authorized and expected** — the verification discipline below requires it.
Parallel research scouts per axis are encouraged (house precedent: pass 7 ran five parallel route
scouts).

## What exists (read before starting)

The SWE corpus (`E:\dev\corpora\SWE`) is a unified body of knowledge: 7 research passes over ~468
**works** (books, papers, standards, tools) with 261 typed edges, browsable in `SWE/explorer/`
(browser-native, no framework, single-viewport). Read first:

- `SWE/explorer/README.md` + `SWE/explorer/MODELS.md` — the system, the five models, the
  edge/provenance discipline.
- `SWE/EXPANSION_REPORT_2026-07-10.md` — precedent for how an expansion lands (file-touch surface,
  merge discipline, verification).
- `SWE/swe_process_corpus_v1_0.md` — the house format of a pass report (tag legend, entry format,
  membership discipline).
- The TL;DRs of the six `SWE/compass_artifact_*.md` reports — know what the corpus already covers.
- Skim `E:\dev\corpora\datastructures\` (sibling corpus, own explorer) — Phase 1 overlaps it
  deliberately; see scope rules.

**The gap this mission fills:** the corpus catalogs *works about* software; it has no layer for the
*concepts themselves*. This mission adds that layer — the **design elements** — then wires it to
works (Phase 2), grows the **architecture realm** and bridges the levels (Phase 3), and lands both
realms in the explorer (Phase 4).

## Object of study

**Software design elements**: named, recurring, implementation-level building blocks and mechanisms
of software design — the mid-level vocabulary sitting **below software architecture and above raw
language syntax**. Calibration anchors, one per kind, chosen to show the breadth of the band
(granularity, not emphasis):

| kind | anchors |
|---|---|
| Data representation | semantic data types; tagged union |
| Data flow & buffering | circular buffer; ping-pong buffering; backpressure |
| Execution & concurrency | asynchronous programming models; thread pool; event loop |
| State management | finite state machine; dirty flag |
| Resource management | RAII; object pool; memory arena |
| Error handling | retry with exponential backoff; sentinel value |
| Communication | message queue; mailbox |
| OO design patterns | Observer; Strategy |
| Data structures & algorithms | hash table; ring-buffer-backed queue |
| Embedded / systems | ISR with deferred work; double-buffered DMA |

## Scope rules

INCLUDE:
- Object-oriented design patterns — the full GoF and POSA catalogs.
- Language-tied idioms when they are the established realization of a mechanism (RAII, pimpl,
  typestate, …); tag with the language.
- Data structures & algorithms **at design-building-block granularity**: the named structures and
  mechanisms a designer reaches for by role (containers, indexes, caches, queues, probabilistic
  sketches, lock-free structures) — included even though `datastructures/` partially covers them;
  everything centralizes under SWE. Do NOT enumerate the algorithmics research zoo (exhaustive
  algorithm variants stay in the datastructures corpus; cross-reference it instead).
- Domain-neutral weighting with **embedded/systems explicitly first-class** (the corpus's center of
  gravity) — but harvest every domain's implementation-level vocabulary (games, databases,
  networking, OS, UI, distributed) wherever an element passes the altitude test.

EXCLUDE:
- Architecture-level constructs and architectural tactics (layered architecture, microservices,
  broker topology, availability tactics) — OUT of the *design* catalog: they form their own realm,
  cataloged in Phase 3 and bridged to every design element. Park upward-borderline candidates in
  the decision log; Phase 3 ingests them.
- Raw language syntax and single-keyword features (`for` loops, `virtual`).
- Process/practice items (code review, TDD, CI) — pass 7's territory.

**Altitude test** (apply to every candidate): an element is IN if it is (a) a mechanism or
construct you can implement *inside one program or component*, (b) *named and recurring* across
codebases, and (c) not primarily a statement about system-level structure. Example borderline call:
"message queue" as an in-process/inter-thread mechanism is IN; "message broker as system topology"
is OUT. Record borderline decisions in the catalog's decision log — over-inclusion with an honest
tag beats silent exclusion. Candidates that fail the test *upward* (too architectural) are parked
in the decision log for Phase 3's architecture catalog, never silently discarded.

## Ground rules (all phases — the house discipline)

1. **Establishedness gate (anti-fabrication).** Every element must be *named in at least one
   citable published source* (pattern catalog, textbook, standard, canonical paper/wiki). No
   invented or merely-plausible names. Phase 1 requires the naming source at title level (live-load
   spot-checks for obscure ones); Phase 2 verifies bibliographically.
2. **Canonical naming & dedup.** One element per mechanism: fold synonyms into `aka` (circular
   buffer = ring buffer). GoF/POSA names are canonical for their patterns. Two entries only when
   the mechanisms genuinely differ (double buffering vs ping-pong buffering: decide, document).
3. **Coverage rule.** A short list is a failure; correctly-tagged over-inclusion is not. Expect
   O(300–600) elements. "Comprehensive" = coverage-driven exhaustive enumeration of established,
   nameable elements — not a curated shortlist.
4. **Saturation stopping rule.** Sweep by three lenses: kind axis × source catalog × domain. Stop
   only when a full sweep across all three lenses yields fewer than ~5 new elements — then run one
   adversarial gap hunt ("which kind/domain/source is thin?") and stop.
5. **Durable state.** Write results to disk incrementally (after every sweep, not at the end).
   Context compaction is expected; the files are the memory. Each phase is independently resumable
   and ends with its deliverable complete plus a dated expansion-report entry.

---

## PHASE 1 — The element catalog

**Deliverable:** `SWE/design_elements_catalog_v1_0.md`

**Method.**
1. **Seed-mine the corpus first.** It already carries the canonical catalogs — GoF *Design
   Patterns*, POSA vols 2–3, Douglass *Design Patterns for Embedded Systems in C*
   (`douglasspatternsc`), Douglass's real-time patterns, White's *Making Embedded Systems*, and
   more across the 7 reports. Extract every element these works name.
2. **Web-sweep the established catalogs** (extend freely): POSA 1–5; PLoP proceedings; Nystrom
   *Game Programming Patterns*; Enterprise Integration Patterns (its mid-level messaging subset);
   concurrency catalogs (Lea, Schmidt, *Java Concurrency in Practice*); Fowler's catalogs (only
   entries passing the altitude test); the c2 wiki; Refactoring.Guru / SourceMaking; Wikipedia's
   pattern and data-structure category lists; Hillside Group catalogs; database-internals
   mechanisms (WAL, LSM tree, B-tree, bloom filter); OS/embedded mechanism literature; language
   idiom collections (C++ Core Guidelines, Rust idioms, effective-X books).
3. **Sweep by kind axis.** Start from the ten anchor kinds plus these extension axes, adding axes
   as discovered: caching & memoization; synchronization & coordination primitives; scheduling &
   time (debounce, throttle, watchdog, timer wheel); parsing & text processing; serialization,
   framing & encoding; persistence & durability; numeric & precision (fixed-point, saturation
   arithmetic); construction & API shape (builder, fluent interface, dependency injection);
   functional & type-level idioms; robustness & security mechanisms. **Grouping is scaffolding for
   coverage and readability only — no structural or ontological commitment.**

**Entry format** (uniform and machine-parseable — Phase 4 parses this file):

### <id> — <Canonical Name>
- aka: <aliases | —>
- kind: <axis>
- what: <1 sentence — the mechanism>
- problem: <1–2 sentences — the problem/forces it addresses>
- named-in: <source that names it; use the corpus id when the work is already in corpus.json>
- tags: <language(s) if language-tied; domain hints; `borderline` + one-line rationale if altitude-contested>

ids: kebab-case, unique, stable — they become node ids in Phase 4; check they do not collide with
existing `SWE/explorer/data/corpus.json` work ids.

**Acceptance:** every kind axis populated; embedded/systems richly represented; every entry carries
a real naming source; borderline decision log included; saturation rule satisfied; per-axis counts
reported in the file header.

## PHASE 2 — The resource pass (pass 8: `design-elements`)

Extend the corpus with the **works** that define and teach the elements, in the house pass format
(`swe_process_corpus_v1_0.md` is the template).

**Deliverable:** `SWE/design_elements_corpus_v1_0.md` — the pass-8 report.

- **Merge discipline:** works already in the corpus become **memberships** (reuse the exact
  existing id); only genuinely absent works become new nodes. Expect heavy membership reuse — GoF,
  POSA, Douglass, White et al. are already there.
- **Many-to-many mapping:** one work covers many elements; tag each pass-8 entry with the element
  ids (or element clusters) it covers. **Every catalog element must be reachable from ≥1
  catalog-grade work**; report unreachable elements as explicit gaps, never pad.
- **Verification discipline:** `verified` only when a primary/authoritative page was loaded live
  this session confirming the exact identifier; else `unverified` plus `UNRESOLVED:` naming the
  soft field. No fabricated ISBN/DOI/year — omit sooner than guess.
- Include the best modern treatments, not only naming sources (an element named in 1994 may have a
  living doc as its current canonical treatment).

## PHASE 3 — The architecture realm + the bridge

Two coupled deliverables: grow an **architecture-element catalog** (a second realm of elements,
built with the same rigor as Phase 1) and populate the **typed bridge** between the realms. The
driver:

**Bridging rule.** Every design-realm element ends Phase 3 with **at least one typed relation to
at least one architecture-realm element**. Specific links only — connect to the most specific
applicable architecture element; an edge to a catch-all node ("software architecture") counts for
nothing. If, after a real attempt, no defensible link exists, do not fabricate one: record the
element in an explicit **unbridged list** with a one-line rationale. That list is a report
deliverable and should be short.

### 3a — The architecture-element catalog

**Deliverable:** `SWE/architecture_elements_catalog_v1_0.md` — same entry format and ground rules
as Phase 1 (establishedness gate, canonical naming & dedup, decision log, machine-parseable stable
ids), marked `realm: architecture`.

- **Canonical floor, then demand-driven growth.** Sweep the canonical architecture vocabularies
  first — the corpus already carries the literature (swa-science + emb-arch passes:
  Bass–Clements–Kazman tactics catalogs, POSA 1 styles, Shaw–Garlan, Taylor–Medvidovic–Dashofy
  styles and connector taxonomy, ISO/IEC/IEEE 42010 concepts, embedded reference architectures) —
  then extend wherever the bridging rule needs a more specific endpoint. Expect O(100–250)
  elements: architectural styles/patterns, tactics, connector types, deployment and structuring
  constructs.
- **Ingest Phase 1's parked candidates.** Candidates the altitude test rejected upward sit in the
  Phase 1 decision log; they enter this catalog here (or are dropped with rationale).
- **Same name, two realms.** Some names live in both realms (*heartbeat* is a Bass availability
  tactic and an implementable mechanism). Catalog the name in each realm where sources establish
  it and bridge the pair — never collapse the realms to dodge the duplication.
- Naming sources are usually already corpus works — cite their corpus ids. A naming source not yet
  in the corpus is added to the pass-8 report as a new node/membership under the Phase 2
  discipline.

### 3b — The bridge

Typed, provenance-tagged relations:

- **design ↔ architecture** — the mission-critical set; the bridging rule lives here. Which
  architecture elements deploy, are realized by, or constrain a design element. Calibration:
  Observer (design) **realizes** publish–subscribe (architecture style); retry with exponential
  backoff (design) **realizes** the retry availability tactic (architecture); event loop (design)
  **enables** event-driven architecture (architecture).
- **element ↔ element within a realm** — e.g. `specializes`, `composes-with`, `alternative-to`.
- **element ↔ implementation** — the language idioms/mechanisms that realize an element (Observer ←
  signals/slots; deterministic reclamation ← RAII), connecting to the emb-c / emb-cpp / emb-ops
  passes' territory. The corpus already stratifies works by branch/level facets — reuse those works
  as endpoints where the facets fit.
- element → work links already exist as Phase 2 tags; do not duplicate them as edges.

Propose and document a **minimal edge-kind vocabulary** (reuse the existing 12 work-edge kinds only
where the semantics genuinely fit; elements likely need their own small set — keep the cross-realm
kinds few and sharply defined so the bridging rule stays mechanically checkable). Every edge
carries provenance in the house sense: **sourced** (the relation is stated in a citable source —
cite it) vs **`editorial`** (reasoned judgment, marked as such, never presented as fact). Prefer
sourced; editorial edges may satisfy the bridging rule, but report the sourced : editorial ratio.

**Deliverable:** `SWE/design_elements_bridge_v1_0.md` — vocabulary definition + the typed relation
list, machine-parseable.

**Acceptance (Phase 3):** the architecture catalog passes the Phase 1 acceptance bar (adapted); the
bridging rule is audited mechanically — design elements with ≥1 architecture edge counted, the
without-list identical to the unbridged list; per-kind edge counts and the sourced : editorial
ratio reported.

## PHASE 4 — Explorer integration

Land the element layer in `SWE/explorer/` so elements are browsable alongside works. **Integration
is total: every element of both catalogs ships into the explorer — no sampling, no top-N curation;
built counts must match the catalog headers.**

- **Read first:** `explorer/ARCHITECTURE.md`, `MODELS.md`, and the file-touch surface in
  `EXPANSION_REPORT_2026-07-10.md`. Pass 7 was a *work-layer* expansion; the element layer adds a
  **new node kind spanning two realms (design + architecture)** — expect a larger surface (a `records_elements`-style build source or a
  parallel `elements.json`, plus the element semantic views — see below). Follow the build pattern: reports are the source of truth; `build/` encodes them;
  `python build/build.py` regenerates `data/`.
- **Requirements (not UI prescriptions):** elements of both realms are searchable and browsable,
  with realm always visible and filterable; an element shows its definition, aliases, kind, realm,
  covering works (Phase 2), and typed relations including cross-realm edges (Phase 3), each with
  provenance; work → element navigation also works; the existing five models and filters keep
  functioning.
- **Semantic views.** Hundreds of elements need more than a list: organize a set of **semantic
  views** in the house pattern — each with a stated *semantic*, the *question it answers*, and a
  pure *computation*, documented in `MODELS.md`, computations in the pure core, view shells only
  projecting. Aim for 3–5 views; candidates (calibration, not prescription — the final set is the
  implementer's call): a **taxonomy/facet view** (realm × kind × tag lattice, live counts); the
  **bridge view** (the design ↔ architecture map: which architecture elements anchor which design
  elements, unbridged list visible); an **element relation graph** (typed edges, hover closure); an
  **element ↔ works coverage view** (which works teach which elements; thin coverage visible).
  **Every element must be reachable through at least one semantic view and through search.**
- **Constraints (house rules, one relaxed):** raw HTML/CSS/JS, zero runtime dependencies, no build
  step at view time, runs from `file://`; obey the `web_manifests/` rule set; `editorial` /
  `unverified` honesty markers stay visible in the UI. **Relaxation: page scroll is authorized**
  where element-scale navigability needs it — the single-viewport/no-scroll rule does not bind the
  element views (target display stays 16:9 4K landscape; do not degrade the existing five work
  models). Record the deviation in `README.md` and the expansion report.
- **Verification:** `python build/build.py` runs clean and mechanically audits **(a) completeness**
  — every catalog element of both realms is present in the built data, counts matching the catalog
  headers — and **(b) the Phase 3 bridging rule** (every design-realm element has ≥1 typed relation
  to an architecture-realm element), printing the unbridged list, which must match the Phase 3
  report's. Serve (`python -m http.server 8098` or the `swe-explorer` launch config) and confirm
  zero console errors, all work models and element views mount, and element browsing + cross-realm
  navigation work end to end. Update `README.md`, `MODELS.md`, `index.html` counts/labels, and
  write `SWE/EXPANSION_REPORT_<date>.md`.

---

## Execution

Phases run in order; each is a self-contained work unit whose deliverable is written to disk and
verified before the next begins — running phases in separate sessions is fine, the deliverables
carry all needed state (Phases 1 and 3 are the largest; each may span several sessions). If scale forces prioritization, prioritize catalog *coverage* over prose
polish. At each phase boundary, write the expansion-report entry with counts, gaps, and decisions;
committing is the user's call — stop and report rather than commit unless instructed otherwise.
