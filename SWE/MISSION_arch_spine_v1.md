# MISSION — The ARCHITECTURE SPINE: stakeholder needs → running system (pass 9, 6 phases)

You are working in the repo at `E:\dev\corpora`. **Unlimited web research (search + fetching primary
pages) is authorized and expected** — the verification discipline below requires it. Parallel
research scouts per stage and per domain are encouraged (house precedent: pass 7 ran five parallel
route scouts; pass 8 ran eleven).

## What exists (read before starting)

The SWE corpus (`E:\dev\corpora\SWE`) is a unified body of knowledge: 8 research passes over **468
works** with 261 typed edges, plus a two-realm **element layer** (709 design + 374 architecture
elements, 2811 typed relations, 21 named atlas islands), browsable in `SWE/explorer/` (browser-native,
no framework, single-viewport for the work models). Read first:

- `SWE/explorer/README.md` + `SWE/explorer/MODELS.md` — the system, the eleven views, the
  edge/provenance discipline.
- `SWE/swe_process_corpus_v1_0.md` — **the house format of a pass report** (tag legend, entry format,
  membership discipline). This pass follows it.
- `SWE/MISSION_design_elements_v1.md` — the house method precedent (phasing, ground rules, saturation).
- `SWE/EXPANSION_REPORT_2026-07-11_bok.md` — precedent for how an expansion lands in the explorer.
- `SWE/simulink-matlab-large-projects-r2.md` and `../embedded-c-architecture-and-design-r1.md` — the
  house doctrine already written for domains D6/D7; the pass must not contradict them silently.

**Coverage probe, 2026-09-19** (run before writing this mission; re-run and extend in Phase 0):

| territory | probe | corpus state |
|---|---|---|
| architecture foundations, 42010, ATAM/CBAM | held | memberships expected |
| MISRA (29 hits), AUTOSAR (14 + 62 element refs), DO-178/331, ISO 26262, IEC 61508 | held | memberships expected |
| views & viewpoints (4+1, C4, V&B), AADL, SysML/MBSE, ADRs | thinly held (1 hit each) | extend |
| ISO/IEC/IEEE 29148, 15288, 15939 · architecture drivers · ASRs · utility tree · QAW | **absent (0)** | new ground |
| SQALE · design structure matrix · propagation cost · Attribute-Driven Design | **absent (0)** | new ground |
| back-to-back / equivalence testing · tool qualification | **absent (0)** | new ground |
| Cynefin · complex adaptive systems · systems-of-systems | **absent (0)** | new ground |
| observability · OpenTelemetry · SRE / error budgets · incident management | **absent (0)** | new ground |

**The gap this mission fills:** the corpus is strong on *architecture as a body of knowledge* and on
*embedded implementation*, and has nothing on the **derivation chain that connects them** — how a
stakeholder need becomes a binding obligation, becomes a testable architecture requirement, becomes a
design, becomes a toolchain and a running, measured, governed system. This pass adds that chain, in
both embedded realizations (handwritten C and model-generated C), with its governance, measurement,
and runtime-operations rings.

## Object of study

**The spine**: the derivation chain from stakeholder need to running system, and the works that define
and teach each link — harvested across seven domains. Two axes held in tension throughout, as in
pass 7: the **stage** a work speaks to, and the **domain** it speaks about. Every entry is tagged on
both; the matrix is how coverage is judged.

### The five stages (`stage:`)

**S1 `needs` — stakeholder needs.** Who the stakeholders are and what they require of the system,
before the answer is solution-shaped: stakeholder identification and analysis, concerns, system
context and boundary, ConOps/OpsCon, mission and business goals, scenarios and use cases, and the
needs-vs-requirements distinction itself (ISO/IEC/IEEE 29148 draws it explicitly).

**S2 `obligations` — architecture obligations.** The binding **must-holds that shrink the solution
space** before any solution is described. Per the 2026-09-19 ruling, this stage is the **union of five
near-but-not-identical vocabularies**, all in scope:
  1. ISO/IEC/IEEE 42010 **concerns** and the viewpoint machinery that answers them;
  2. SEI **architectural drivers** (quality-attribute requirements, primary functionality,
     constraints, concerns);
  3. **architecturally significant requirements** (ASRs);
  4. **constraints** — technical, platform, legacy, organizational, contractual;
  5. **certification and regulatory duties** — DO-178C/DO-331, ISO 26262, IEC 61508, IEC 62304 and
     their mandated work products.

These are not synonyms and the literature does not unify them. Phase 3b delivers the reconciliation
as a first-class artefact.

**S3 `requirements` — architecture requirements.** The obligations made **testable, prioritized, and
allocated**: quality-attribute scenarios (source / stimulus / artifact / environment / response /
response measure), utility trees, the Quality Attribute Workshop, ISO/IEC 25010 as the quality
vocabulary, trade-off and prioritization method (ATAM, CBAM), allocation of requirements to
architectural elements, and requirement specification standards (29148).

**S4 `design` — architecture design.** Deciding structure against those requirements: Attribute-Driven
Design and other design methods, tactic and pattern selection, views and viewpoints (Views & Beyond,
4+1, C4, 42010 viewpoints), architecture description languages and modelling (AADL, SysML/MBSE,
System Composer, AUTOSAR), decomposition and allocation, decision capture (ADRs), and architecture
evaluation.

**S5 `tools-process` — tools and process.** The enabling layer: requirements and traceability tooling,
ALM, modelling and code-generation toolchains, static analysis and verification tooling, tool
qualification, configuration management, CI for code *and* models, and the lifecycle-process
frameworks that bind them (ISO/IEC/IEEE 15288/12207, the safety standards' process requirements).
**This stage is both a terminal link and a substrate**: tag a work `stage:tools-process` when tooling
or process *is* its subject, and additionally tag the stage it serves.

### The seven domains (`domain:`)

**D1 `complex-scale`** — complexity as **scale and structure**: large, long-lived, multi-team,
high-coupling industrial systems; systems-of-systems; the architecture-of-complexity lineage (Simon,
Brooks, Parnas, Baldwin–Clark); modularity and dependency structure; architectural erosion and drift;
evolution and modernization at scale; Conway's law and sociotechnical structure.

**D2 `complex-science`** — complexity as a **property of the system and its context**: complex adaptive
systems, emergence and nonlinearity, the complicated-vs-complex distinction, Cynefin and decision
frameworks under uncertainty, resilience engineering and Safety-II, sociotechnical complexity.
**Altitude guard:** a work is IN when it is applied to — or directly applicable to — software/systems
architecture practice. Pure complexity theory with no architectural application is OUT; without this
guard the domain swallows the pass.

**D3 `governance`** — how architecture decisions are made, held, enforced, and revisited: governance
bodies and operating models, decision records, conformance checking and fitness functions, technical
debt as a managed liability, architecture review processes, standards-compliance management,
architecture risk management.

**D4 `measurement`** — metrics **of the system and its architecture**: ISO/IEC 25010 quality model,
ISO/IEC 15939 measurement process, coupling / cohesion / instability / abstractness, design structure
matrices and propagation cost, modularity metrics, maintainability indices, technical-debt
quantification (SQALE and successors), metric tooling, delivery metrics (DORA), reliability and safety
measures.

**D5 `runtime-ops`** — managing the system **while it runs**: observability (logs, metrics, traces,
OpenTelemetry), SRE practice and error budgets, operability as a design concern, incident management
and postmortems, deployment / rollout / rollback and feature flags, health monitoring — and the
embedded counterpart: on-target diagnostics and DTCs, field data and telemetry from deployed devices,
over-the-air update architecture, remote logging under resource constraints. The embedded leg is
expected to be the thinnest in the literature and the most valuable harvest.

**D6 `hand-c`** — embedded software as **handwritten C**: module and file structure, MISRA C and
coding standards, manual review, unit and integration test, static analysis, resource-constrained
design, RTOS integration, requirement→function traceability.

**D7 `model-c`** — embedded software as **C generated from MATLAB/Simulink/Stateflow models**: model
architecture (referenced models, atomic subsystems, data dictionaries, variants), modelling standards
(MAAB/JMAAB, MISRA-compliant modelling), model review and Model Advisor, code-generation configuration
and Embedded Coder, SIL/PIL and back-to-back equivalence testing, model- and code-level coverage,
requirement→block→generated-code traceability, tool qualification and certification kits, model
version control / merge / diff, integration of generated with handwritten code and the scheduler,
System Composer and AUTOSAR workflows.

## The coverage matrix (7 domains × 5 stages = 35 cells)

|  | needs | obligations | requirements | design | tools-process |
|---|---|---|---|---|---|
| **complex-scale** | | | | | |
| **complex-science** | | | | | |
| **governance** | | | | | |
| **measurement** | | | | | |
| **runtime-ops** | | | | | |
| **hand-c** | | | | | |
| **model-c** | | | | | |

Each cell is a **coverage question**, not a quota. Every non-empty cell names ≥1 **anchor** — its entry
point. A thin or empty cell is a finding, and **every thin cell must be adjudicated**: *literature-thin*
(the field has not written it) or *sweep-thin* (we did not find it). The distinction is recorded per
cell; guessing between them is not allowed.

## Scope rules

INCLUDE:
- Books, standards (ISO/IEC/IEEE, DO-xxx, IEC-xxxxx), peer-reviewed papers, authoritative tool
  documentation (MathWorks, AUTOSAR, vendor qualification kits), living web standards, and canonical
  practitioner references.
- **Standards as first-class works** — they are the primary sources of the obligations stage.
- Both the language-agnostic canon and its domain-specific instantiations — the transposition axis of
  pass 7. A method that is domain-neutral is tagged across the domains it serves.
- Requirements engineering canon, for stages S1–S3, where it teaches the needs→obligations→requirements
  thread.
- Works already in the corpus that speak to a spine cell — claimed as **memberships**, never
  re-cited.

EXCLUDE (with the rulings that produced each):
- **Project and program management** — estimation (COCOMO, function points *used for estimation*),
  planning, scheduling, team and agile process management. *Ruling 2026-09-19: management covers
  governance and measurement only.* **Boundary test:** if the work's purpose is to plan or estimate
  *the project*, it is OUT; if it governs or measures *the system and its architecture*, it is IN.
- **Pure complexity theory** with no architectural application (D2 altitude guard above).
- **Pass 7 process mechanics** — git workflow, CI plumbing, formatting — unless the work speaks to a
  spine stage; then it is a membership under this pass.
- **Functional-requirement elicitation technique catalogs** beyond their anchors. The pass tracks the
  *architectural* thread, not the whole of RE.
- **Minting new catalog elements** (design or architecture realms) — adjacent work, out of scope
  unless requested. Park candidates in the decision log rather than discarding them.

**Adjacent, not in scope — flagged for a later call.** The architecture-element catalog carries exactly
**1 manageability tactic** and 8 testability tactics, while `runtime-ops` is now a first-class domain.
The element layer is very likely under-built here. Record the observation in the expansion report; do
not act on it without instruction.

## Ground rules (all phases — the house discipline)

1. **Verification gate (anti-fabrication).** `verified` only when a primary or authoritative page was
   loaded live this session confirming the exact identifier; else `unverified` plus an `UNRESOLVED:`
   note naming the soft field. **No fabricated ISBN / DOI / year / standard part number — omit sooner
   than guess.** Standards are especially prone to this: part numbers and edition years must be
   confirmed against the issuing body.
2. **Membership-by-id merge.** A work already in `explorer/data/corpus.json` REUSES its exact existing
   id and is logged as a membership carrying only the pass-9 tags and the reason the spine claims it.
   Never create a second node for a work the corpus holds.
3. **Collect-don't-exclude; scope enforced by tags.** Correctly-tagged over-inclusion beats silent
   exclusion. A short list is a failure.
4. **Sourced vs editorial.** Any claim *about the chain* — that stage X obligates stage Y, that a
   practice in D6 corresponds to one in D7 — is either `sourced` (cited) or `editorial` (reasoned
   judgment, marked as such). Never present editorial reasoning as fact.
5. **Saturation stopping rule.** Sweep by three lenses: **stage × domain × source-kind**
   (book / standard / paper / tool-doc / living-web). Stop when a full sweep across all three yields
   fewer than ~5 new works — then run one adversarial gap hunt ("which cell is thin, and is it
   literature-thin or sweep-thin?") and stop.
6. **Durable state.** Write to disk incrementally, after every sweep, not at the end. Context
   compaction is expected; the files are the memory. Each phase is independently resumable and ends
   with its deliverable complete plus a dated expansion-report entry.
7. **Scale expectation.** O(250–400) pass-9 members. Expect heavy membership reuse in the
   `design` / `hand-c` cells and mostly new nodes in `needs`, `obligations`, `measurement`,
   `runtime-ops`, and `complex-science`.

---

## PHASE 0 — Calibration & merge map (cheap; one session)

**Deliverables:** `SWE/_spine_work/id_index.txt`, `SWE/_spine_work/matrix_v0.json`.

1. Build the id index from `explorer/data/corpus.json` (468 ids, title + authors + year) so scouts can
   resolve memberships to exact ids without guessing.
2. Freeze the tag legend: `stage:` (5 values), `domain:` (7 values), plus one new `lang:` value
   `generated-c` for works about code generated from models. Existing facets (`role`, `verification`,
   `type`, `branch`, `theme`) are unchanged.
3. Seed all 35 cells from what the corpus already holds — the 2026-09-19 probe table above is the
   starting point; extend it.

**Acceptance:** every one of the 35 cells carries either a seed work (by existing id) or an explicit
`empty-at-seed` marker.

## PHASE 1 — The spine (five stage scouts)

**Deliverable:** `SWE/_spine_work/harvest/stage_<s>.json` × 5.

Five parallel scouts, one per stage, sweeping the **language- and domain-agnostic canon** of that
stage. Each find is tagged with its stage *and* every domain it serves — the matrix fills from both
directions, and Phase 2 deduplicates by id.

**Acceptance:** each stage names ≥1 anchor; saturation reported per stage; every entry carries a
verification status and, when `unverified`, the named soft field.

## PHASE 2 — The domains (seven domain scouts)

**Deliverable:** `SWE/_spine_work/harvest/domain_<d>.json` × 7, plus `matrix_v1.json` (the filled grid).

Seven parallel scouts, one per domain, each sweeping that domain's literature **across all five
stages** and tagging accordingly. D7 (`model-c`) is the pass's center of gravity and gets the deepest
sweep: MathWorks primary documentation, certification-kit documentation, and the automotive/aerospace
process literature are all in play.

**Acceptance:** the 35-cell fill report; every thin cell adjudicated *literature-thin* or *sweep-thin*;
saturation rule satisfied across the stage × domain × source-kind lenses.

## PHASE 3 — The two deltas (the reasoning artefacts)

**Deliverable:** `SWE/arch_spine_deltas_v1_0.md`.

**3a — The hand↔model delta.** A stage-by-stage comparison of handwritten-C and model-generated-C
practice (D6 vs D7): for each of the five stages, what is **the same**, what is **different**, and what
has **no counterpart** on one side. This is the artefact the literature does not write down in one
place; it is the reason the two embedded legs are in one pass rather than two. Every row cited or
marked editorial.

**3b — The obligations primer.** Reconcile the five S2 vocabularies — 42010 concerns, SEI architectural
drivers, ASRs, constraints, certification duties. For each: who uses the term, what it covers, which
source defines it, where it overlaps the others, and where it does not. Close with **one worked example
carried through all five vocabularies** so the mapping is concrete. This exists because the vocabulary
is genuinely unaligned across the sources, and the pass makes the alignment explicit rather than
pretending it exists.

**Acceptance:** every claim in both artefacts either cited or explicitly marked editorial.

## PHASE 4 — The pass report (pass 9: `arch-spine`)

**Deliverable:** `SWE/arch_spine_corpus_v1_0.md`, in the house pass format
(`swe_process_corpus_v1_0.md` is the template).

Header carries: scope, collection date, tag legend, and a **census** — total members = memberships +
new nodes, verified / unverified split, per-cell counts over the 35-cell matrix, and the explicit gap
list with each thin cell's adjudication. Entries follow the house format: **Title** — authors/body,
year. Venue. Identifier. `{stage | domain | lang | role | verification}` — relevance note. Memberships
prefixed `[MEMBERSHIP id=…]`.

**Acceptance:** every harvested work appears exactly once; every membership id resolves against
`corpus.json`; no fabricated identifiers; the census arithmetic checks.

## PHASE 5 — Explorer integration

**Deliverables:** `SWE/explorer/` view 12, updated build + docs, `SWE/EXPANSION_REPORT_<date>_spine.md`.

- **View 12 — Spine.** The 7 × 5 matrix with live counts; click a cell → its works; a stage rail and a
  domain rail as independent filters; thin cells visually marked with their adjudication. The tab
  spine becomes **Body of Knowledge · Elements · Atlas · Spine** = *the literature · the concepts · the
  map · the chain*.
- The work inspector gains `stage` / `domain` badges; the Facets view (model 2) gains both new facets.
- **Build self-audit:** every pass-9 work reachable from view 12; every cell count matches the Phase 4
  report; zero console errors; `file://` still opens.
- **Stretch, only if cheap:** view 13 rendering the 3a delta as a five-row comparison.
- Update `README.md`, `MODELS.md`, and `index.html` counts and labels.

---

## Execution

Phases run in order; each is a self-contained work unit whose deliverable is written to disk and
verified before the next begins — running phases in separate sessions is fine, the deliverables carry
all needed state (Phases 1 and 2 are the largest; each may span several sessions). If scale forces
prioritization, prioritize **cell coverage over prose polish**.

**Model dispatch (standing house directive).** Research scouts dispatch on the **cheapest model able to
do the sweep**; verify the end result, not every scout step.

Write `SWE/_spine_work/RESUME_STATE.md` at every phase boundary, in the house format: deliverable
table, where the canonical data lives, and rebuild/verify-from-clean instructions.

At each phase boundary, write the expansion-report entry with counts, gaps, and decisions.
**Committing is the user's call** — stop and report rather than commit unless instructed otherwise.
