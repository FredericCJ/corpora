# SWE Corpus — ELEMENT-Layer Expansion Report — 2026-07-10

The element-layer mission (`MISSION_design_elements_v1.md`) adds the *concept* layer to a corpus
that until now cataloged only *works*: a design-element catalog (Phase 1), the pass-8 resource
pass wiring elements to works (Phase 2), an architecture-element realm plus the typed cross-realm
bridge (Phase 3), and total explorer integration (Phase 4). One section per phase, written at each
phase boundary.

---

## Phase 1 — Design-element catalog (`design_elements_catalog_v1_0.md`) — COMPLETE

**Deliverable.** `SWE/design_elements_catalog_v1_0.md` — **708 elements** across **22 kind axes**
(the mission's 20 plus `code-structure` and `testing-constructs`, both added when coherent
clusters emerged), machine-parseable house entry format, per-axis counts in the header.

### Headline counts

| | |
|---|---|
| elements | **708** |
| kind axes | 22 (20 mission + 2 discovered) |
| confidence | 456 established · 252 spot-checked (live page loaded this session) · 0 needs-check |
| borderline (altitude-contested, rationale inline) | 158 |
| parked to the architecture realm (Phase 3 input) | 203 |
| notable exclusions (recorded, not silently dropped) | 316 |
| naming sources already corpus works (`corpus:<id>`) | ~200 entries |
| decision-log entries | 32 |

### Method actually used

1. **Round 1 — 19 parallel scouts** (source-catalog × kind-axis × domain lenses): GoF, POSA 1–5,
   Douglass+Samek, embedded-mech (White/Koopman/Pont/Noble–Weir/Beningo), Nystrom+games, EIP,
   concurrency (JCiP/Lea/Grand/Mattson), lock-free (perfbook/Herlihy–Shavit), DSA-blocks,
   db-internals, C/C++/Rust/Java idioms, PoEAA+DDD, functional, resilience (Nygard/Hanmer),
   parsing+serialization, wiki/c2/PLoP long tail, OS/network, UI/reactive, corpus-seed (the
   corpus's own seven reports). Yield: 713 raw → 577 after union-find merge on normalized
   names+aliases.
2. **Round 2 — 10 gap hunters** on the thin spots the scouts self-reported: +105 net (security
   patterns and PLoPD long tail were whole missed veins; VM internals, stream processing, netcode,
   game AI opened here).
3. **Round 3 — 5 strict lens hunters + the mandated adversarial closer**: +25 net. Lens yields
   collapsed to 2–4 each (mostly checked-and-rejected records); the closer found 9 (4 borderline;
   its 5 non-borderline finds all land in the pre-identified thin axes) and returned verdict
   **SATURATED**. Trajectory 713 → +105 → +25 with a rising strictness bar; frozen at 708.
4. **Merge discipline**: canonical-name priority (GoF/POSA names canonical), aliases folded
   (`aka`), per-cluster provenance kept (`sources_all` retained for Phase 2). Transitive-alias
   fusion was the recurring failure mode; every case found was split and logged (see below).

### Notable decisions (full log in the catalog's Decision log)

- **Fusion bugs found and split**: superloop/game-loop/event-loop/Message-Dispatcher (chained via
  "main loop"); GoF Decorator↔Adapter (shared GoF alias "Wrapper"); GoF Prototype↔Factory Method
  ("Virtual Constructor"); Test Double↔Null Object ("stub"); ABA-mitigation↔Reference Counting
  ("version counter"); Stream Windowing↔UI list-virtualization ("windowing"); Expression
  Builder↔Semantic Model (tooling bug). A citation audit then caught 6 miscited corpus ids
  (works that teach-but-do-not-name an element); fixed.
- **Keep-both calls** recorded for every near-miss pair that names genuinely different mechanisms
  (wrapper-facade vs facade, loop-timeout vs timeout, leaky-bucket vs leaky-bucket-counter,
  lru-cache vs cache-eviction-policy, reactive-programming vs FRP vs reactive-signals, …).
- **Anchor coverage**: "semantic data types" is not a published element name anywhere checked —
  covered by newtype (Whole Value folded, Cunningham CHECKS 1994), value-object, quantity,
  units-of-measure-types. "Asynchronous programming models" covered by async-await-model +
  coroutine + future/promise + event-loop + proactor, not an umbrella entry.
- **Crypto-primitive band** (hash, MAC, AEAD, CSPRNG, nonce, salted hashing) kept
  borderline-tagged: designer-reachable building blocks the catalog already presupposed.
- **203 parked candidates** carry one-line rationales and are the Phase 3a intake (MV* family,
  POSA1 styles, EIP topologies, DDD strategic, cloud topology patterns, safety executives, …).

### Honest gaps

- MPU-based task isolation and power-management disciplines beyond tickless idle: real practice,
  no established element names — recorded, not padded.
- EWMA/median smoothing and the DSP filter family: established but declined under the
  algorithm-zoo rule (numerics territory; cross-referenced to the sibling corpora).
- Pont's ~65 remaining PTTES patterns: 8051-hardware-specific, below the design band (spot-checked
  sample, not exhaustively enumerated).
- Phase 2 must add the missing naming-source works: Meszaros, Hohpe–Woolf, Goetz, Lea, Herlihy–
  Shavit, Kleppmann, Petrov, Fowler PoEAA/DSL, Nystrom, CLRS, Okasaki, Gregory, plus the paper
  tail (Woolf, Cunningham, Beck SBPP, LMAX, Dataflow Model, …) — flagged per element in the
  working set.

**Verification.** Establishedness gate held: every entry carries a title-level naming source; 252
were live-verified this session; the citation audit cross-checked all `corpus:` ids against work
titles. Zero id collisions with `corpus.json` work ids; ids kebab-case and unique (mechanically
asserted).

---

## Phase 2 — Pass 8: the design-element resource pass (`design_elements_corpus_v1_0.md`) — COMPLETE

**Deliverable.** `SWE/design_elements_corpus_v1_0.md` — the pass-8 report: the works that define
and teach the 708 elements, mapped many-to-many onto element ids in the house pass format.
Collection date 2026-07-11 (fleet re-run after the 2026-07-10 halt; all verification re-done live
in the collecting session).

### Headline counts

| | |
|---|---|
| pass-8 members | **348** |
| memberships (existing corpus works reclaimed; exact-id reuse) | **63** |
| new nodes | **285** (233 verified / 52 unverified-quarantined) |
| element coverage | **705 / 708** reachable from ≥1 catalog-grade work |
| explicit gaps (never padded) | 3 — `multiton`, `servant`, `shadow-register` |
| coverage multiplicity | 472 ×1 · 178 ×2 · 55 ×≥3 |

### Method

Eleven route agents (element-domain slices r1–r11, 37–105 elements each) ran in parallel, each:
membership-first lookup against the 468-work corpus, live primary-page verification for every new
node (publisher / standards body / official project site / author page), catalog-grade coverage
assignment (mere mention ≠ coverage), and explicit-gap reporting. Central assembly deduplicated
across routes — 121 raw membership claims → 63 unique works; 339 raw new-work claims → 285 after
six same-work merges (PLoPD3 ×2, React docs ×2, RFC 791 ×2, Gregory GEA ×2, Tanenbaum CN 5th/6th
ed., Fowler eaaDev ×2) — checked all proposed ids against work ids AND element ids, and audited
reachability mechanically (route-declared gaps exactly match the uncovered set; zero stray element
ids).

### Findings & decisions

- **Membership layer confirms the corpus's center of gravity**: the heaviest reclaimed works are
  the embedded canon (douglasspatternsc, noblesmallmem, posa2/3, white, koopmanbess, pont,
  freertosbook, samekbook, hanmer, preschern, hanson, tornhill, iglberger, coreguidelines).
- **New-node shape**: missing catalog anchors (PoEAA, EIP, Meszaros, JCiP, Lea, Mattson,
  Herlihy–Shavit, perfbook, CLRS, DDIA, Petrov, Nystrom ×2, Gregory, GC Handbook, Dragon, Evans)
  plus the canonical naming-paper tail, kept only where no treatment covers the element or the
  paper is canon.
- **Systematic verification hole, named honestly**: ACM DL / IEEE / USENIX / Elsevier / Wiley /
  O'Reilly bot-blocked fetches all session — the 52 quarantined nodes are almost all canonical
  papers corroborated via dblp/Crossref/author pages with the soft field flagged per entry; no
  identifier fabricated. Most exposed: `huangrejuv` (sole cover of software-rejuvenation).
- **Living docs are load-bearing** for UI/reactive and RTOS mechanism vocabulary (React/Microsoft
  Learn/Qt/TC39/ReactiveX; FreeRTOS) — the pass-7 finding (knowledge lives in tooling docs)
  recurs at the framework-mechanism level.
- Wikipedia-only naming sources were **upgraded** where possible (event-loop → Node.js docs,
  green-threads → JEP 444, zero-copy → LWN, magic-number → file/libmagic, REPL → Crafting
  Interpreters, bit-banging → Ganssle 1991…); the three that could not be upgraded are the
  explicit gaps.

---

## Phase 3 — Architecture realm + the design↔architecture bridge — COMPLETE

Two coupled deliverables plus a pass-8 addendum, all landed 2026-07-11.

### 3a — Architecture-element catalog (`architecture_elements_catalog_v1_0.md`)

**374 elements**, realm: architecture, same entry contract and ground rules as Phase 1.

| kind | n |
|---|---|
| tactic (Bass-style QA primitives) | 109 |
| pattern | 133 |
| style | 66 |
| deployment | 26 |
| description (views/viewpoints/ADLs) | 16 |
| connector | 14 |
| reference-architecture | 10 |

- Confidence 359 established / 15 spot-checked. Tactic coverage spans **14 quality attributes**
  (availability, deployability, energy-efficiency, integrability, manageability, modifiability,
  performance, reliability, resource-efficiency, safety, scalability, security, testability,
  usability) — the full Bass–Clements–Kazman 4th-ed. trees, live-verified.
- **Canonical floor**: Bass tactics, POSA1, Shaw–Garlan boxology, Taylor–Medvidović–Dashofy styles +
  the 8-type connector taxonomy, ISO/IEC/IEEE 42010 description constructs, Kopetz/AUTOSAR/ARINC 653
  embedded reference structures — naming sources cite existing corpus/pass-8 ids.
- **Parked-intake audit closed**: all 203 Phase-1 parked candidates adjudicated —
  **143 dispositions** (92 folds into a produced element, 51 drops with rationale), the rest admitted
  as catalog entries. Mechanically audited to zero unaccounted.
- **Same-name, two realms** honored: 23 names live in both realms (heartbeat/heartbeat-tactic,
  event-sourcing/event-sourcing-style, bulkhead/bulkhead-arch, monitor, pipes-and-filters …),
  disambiguated by kind suffix and bridged as pairs — never collapsed.
- **Demand-driven growth**: four elements added from Phase 3b bridge feedback
  (event-driven-architecture, master-worker, data-parallel-architecture/SPMD, service-registry),
  each from a work already in the verified set.

### Pass-8 addendum (route r12)

The architecture catalog's naming sources that were in neither the corpus nor the pass-8 set were
verified and added under the Phase 2 discipline: **+51 new works** (40 verified live / 11
quarantined) + 1 matched to an existing node, bringing pass 8 to **399 works**. Digital-library
bot-blocking (ACM/IEEE/USENIX/Wiley/O'Reilly) again forced dblp/Crossref corroboration for the
quarantined tail; no identifier fabricated.

### 3b — The bridge (`design_elements_bridge_v1_0.md`)

**1132 typed, provenance-tagged edges.** Edge-kind vocabulary (7): cross-realm `realizes` /
`enables` (design→architecture) + `constrains` (architecture→design); `implements` (design→design,
idiom→mechanism); within-realm `specializes` / `composes-with` / `alternative-to`.

| kind | n |
|---|---|
| realizes | 544 |
| enables | 324 |
| implements | 39 |
| constrains | 10 |
| specializes | 61 |
| composes-with | 89 |
| alternative-to | 65 |

- **Bridging rule audited mechanically**: **703 / 709 design elements** carry ≥1 cross-realm edge to
  a *specific* architecture element; **MISSING = 0** (every element is bridged or on the explicit
  unbridged list). The **6 unbridged** are all genuinely sub-architectural idioms —
  `nifty-counter` (static-init order), `kahan-summation` (numeric accuracy), `erase-remove` &
  `zipper` (container/FP idioms), `x-macro` (preprocessor codegen), `empty-base-optimization`
  (compiler layout) — none has a defensible architecture counterpart, recorded rather than faked.
- **Provenance**: **328 sourced : 804 editorial** (29% sourced). Sourced edges are anchored in Bass
  tactic chapters, EIP relations, POSA "See Also", DDIA prose, Fowler/Evans; the editorial majority
  reflects that most design→architecture realizations (especially GoF-pattern → style) are
  analytically standard but not stated verbatim in a single fetched page — marked honestly rather
  than dressed as fact.
- **Method**: 11 per-axis bridge agents (design-element groups g1–g11) each given its elements + the
  full 374-element architecture index; central assembly validated every edge against the realm id
  sets (12 malformed cross-realm/within-kind edges rejected; 8 recovered as valid `realizes`/
  `constrains` in a curated pass, the rest confirmed redundant), deduped, and ran the bridging
  audit. Target spread: 210/374 architecture elements receive ≥1 cross edge; the busiest targets are
  specific named Bass tactics (increase-resource-efficiency, exception-prevention, defer-binding),
  not catch-alls.

**Acceptance (Phase 3):** architecture catalog passes the adapted Phase-1 bar (per-kind counts,
naming sources, decision log, stable ids); bridging rule mechanically audited (703 bridged +
6 unbridged = 709, without-list ≡ unbridged list); per-kind edge counts and the 328:804 sourced:
editorial ratio reported.

---

## Phase 4 — Explorer integration of the element layer — COMPLETE

The element layer lands in `SWE/explorer/` as a new node kind spanning two realms, browsable
alongside the 468-work corpus. `python build/build.py` regenerates everything and self-audits.

### What shipped

- **Build (`build/build_elements.py`, wired as `build.py` PHASE 4).** Consumes the committed encoded
  sources in `build/element_src/` (the four Phase 1-3 deliverables as JSON, analogous to how
  `records_*.py` encode the pass reports) and emits `data/elements.{json,js}` (`SWE.elements`:
  1083 nodes, 1132 edges, 417 referenced works). Two mechanical audits, **failing loud**:
  (a) **completeness** - built design/architecture/edge counts equal the deliverable `.md` census
  headers (709 / 374 / 1132); (b) the **bridging rule** - 703/709 design elements carry a
  cross-realm edge, the 6-element unbridged list printed and matching the bridge report's. The seven
  work passes are untouched (468 nodes, 261 edges regenerate identically).
- **Runtime.** A second pure core `logic/core_elements.js` (`SWE.coreEl`: search, cycle-safe element
  closure, `bridgeByArch`, `coverageBuckets`); boundary parse `parse.parseElements`; element
  presentation helpers in `util.js`; the persistent inspector extended to render **element detail**
  (definition, aliases, realm, kind, covering works, all typed relations incl. cross-realm bridge
  edges with provenance) and **work->element** navigation (a work now lists the elements it teaches).
- **Four semantic views** (documented in `MODELS.md`, computations in the pure core):
  6 **Element taxonomy** (realm x kind x tag lattice, live counts) - 7 **Design<->Arch bridge** (the
  mission map: architecture anchors -> design elements, busiest first, the 6 unbridged shown, 328
  sourced : 804 editorial) - 8 **Element relations** (a focused ego-graph - design-left /
  architecture-right - since 1083 nodes cannot render at once) - 9 **Element coverage** (gap/thin/
  covered buckets + works ranked by element density). Every element is reachable through a view and
  through search.

### Deviation recorded (the mission's one relaxation)

Page/inner scroll is **authorized for the four element views** (element-scale navigability); the five
work models keep the strict single 16:9 4K viewport with no page scroll, and are not degraded. Noted
in `README.md` and `MODELS.md`.

### Verification

`python build/build.py` runs clean, both audits green. Node was unavailable (as when the explorer
was first authored), so the UI was verified with **headless Chrome** (`--dump-dom` +
`--enable-logging=stderr`), over both `file://` and a served `http://localhost:8098`:
- all **9 view tabs mount with zero boot errors**; the element separator renders between the work
  models and the element views;
- each element view renders its content in quantity (bridge: 212 anchor groups + 884 edge lines +
  the unbridged tail; taxonomy: 1083 elements, 5 facet bars; ego-graph: focus + typed neighbours;
  coverage: gap/thin/density with pass-8 works flagged);
- **bidirectional cross-layer navigation** works - a design element's detail links to its covering
  works (e.g. RAII -> its pass-8 works), and a work's detail lists the elements it teaches
  (e.g. GoF -> 27 elements);
- **zero runtime JS errors** across all element views with an active selection (only the app's own
  INFO logging via its injected-logger seam);
- the five work models are **unregressed** (graph 258 nodes, facets 180 rows).

### Files touched

New: `build/build_elements.py`, `build/element_src/` (design/architecture/bridge/pass8 JSON +
`VIEW_SPEC.md`), `logic/core_elements.js`, `logic/views/el_taxonomy.js` + `el_bridge.js` +
`el_graph.js` + `el_coverage.js`, `data/elements.{json,js}`. Extended: `build/build.py` (PHASE 4),
`logic/parse.js` (`parseElements`), `logic/util.js` (element chips/badges), `logic/inspector.js`
(element detail + work->element), `logic/app.js` (parse elements, 9-view registry, tab divider,
`1-9` keys), `index.html` (scripts + counts), `styles/app.css` (realm chips, element-view layouts),
`README.md`, `MODELS.md`.

---

## Mission complete

All four phases delivered and verified: a **709-element design catalog**, a **399-work pass-8**
mapping (706/709 covered), a **374-element architecture realm** with a **1132-edge typed bridge**
(703 bridged, 6 honestly unbridged, 328 sourced : 804 editorial), and **total explorer integration**
(nine views, both audits green, zero console errors). Committing is the user's call.
