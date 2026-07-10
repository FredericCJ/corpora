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
