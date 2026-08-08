# Spec Recovery & Reverse-Engineering — Ground-Truth Manifest

**Purpose.** A citable ground-truth reference for an agent that (a) RECOVERS a design/architecture
specification FROM implemented Python code, and (b) TRACKS the DIVERGENCE between an upfront spec and
that code, using git as evidence. This is **grounding, not a rulebook**: cite a principle only when it
materially shapes a recovery or classification decision; reason past it when the situation does not
match. Every factual claim is tagged **ESTABLISHED** (settled in the literature), **VERSION-DEPENDENT**
(tie to a tool/standard version), **OPEN** (no authoritative bar found — a project judgment call), or
**CC-FACT** (Claude-Code / this-repo mechanics). Primary sources are inline-cited; the **## Sources**
list carries access dates.

This manifest does NOT duplicate its siblings. For **code→model mapping and Python static-analysis
traps** (duck typing, decorators, async, MRO, `setattr`) cross-reference
`uml25_ocl_conformance_manifest.md §4` — do not re-derive them. For the **spec boundary, the
traceability spine, and the decision-log/dissent discipline** cross-reference
`software_spec_discipline_manifest.md` (§A1–A2, §G1–G2, §B2/§G4, §B3, §E2). For **typing and testing
tooling facts** see `python_typing_contract_manifest.md` and `python_testing_tooling_manifest.md`.

---

## 0. Scope & relationship to the sibling manifests

This manifest serves the team's NEW-FEATURE work in two situations: when an implementation exists but
its design spec was never written or has gone stale (RECOVER it), and when an upfront spec exists and
the code may have wandered from it (MEASURE the drift). The two are **phases of one loop, not separate
tasks** (§11) **[OPEN — the end-to-end loop is a synthesis, not a single cited authority]**.

What lives elsewhere and is assumed, not repeated:
- The implementation-agnostic spec boundary, signature-level/body-free contracts, the SR-n → component
  → design-spec → verification spine, and "record contested decisions, do not erase dissent" —
  `software_spec_discipline_manifest.md`.
- Faithful Python-construct→UML mapping and the catalogue of Python constructs with no clean static
  representation — `uml25_ocl_conformance_manifest.md §4`.

A recovered spec REUSES the repo's existing format (§4); it never invents a new one.

---

## 1. Terms of art & taxonomy

**Reverse engineering, design recovery, redocumentation are distinct — ESTABLISHED.** Chikofsky &
Cross (IEEE Software, 1990) define reverse engineering as "analyzing a subject system to identify its
components and their interrelationships and create representations of the system in another form or at
a higher level of abstraction." Two subareas matter here:
- **Redocumentation** recreates lost documentation at the *same* abstraction level as the code.
- **Design recovery** "recreates design abstractions from a combination of code, existing design
  documentation (if available), personal experience, and general knowledge about problem and
  application domains."

**The load-bearing consequence — ESTABLISHED.** Design recovery, *by definition*, draws on information
that is NOT in the code (domain knowledge, human reasoning). Therefore **every such inference must be
tagged `[INFERRED]` and never presented as a code-derived fact.** The honesty of a recovered spec is
exactly the reader's ability to tell read-off-code from reasoned-by-recoverer (§4). The six stated
reverse-engineering objectives (cope with complexity, generate alternate views, recover lost
information, detect side effects, synthesize higher abstractions, facilitate reuse) are the goals a
recovery effort serves. (Chikofsky & Cross 1990.)

**Prescriptive/intended vs descriptive/as-built architecture — ESTABLISHED.** The upfront spec (SR-n
contracts, `02_architecture.md`) is the **prescriptive / intended** architecture; what the code
actually realizes is the **descriptive / as-built** architecture. The gap between them is the object of
study. The 2024 ICSA developer-perspective study confirms the field still uses this prescriptive-vs-
descriptive pair (Perry & Wolf 1992; "We're Drifting Apart," ICSA 2024).

**Drift vs erosion — ESTABLISHED.** Perry & Wolf (1992) distinguish architectural **drift** (deviation
by *insensitivity to / neglect of* the architecture — it was not consulted) from architectural
**erosion** (deviation by *violation* — it was consulted and broken). This is the causal axis the
divergence classification (§6) sits on.

**Tag legend (reconciled with the repo).** This manifest's recovery tags map onto the repo's existing
epistemic legend (`software_spec_discipline_manifest.md §D2: [STATED]/[INFERRED]/[ASSUMED]/
[ARCHITECTURAL-DECISION]/[UNRESOLVED]`) **[CC-FACT]**:
- **`[RECOVERED]`** — read directly off the code (signature, type, import, explicit inheritance, raised
  exception, statically resolvable call edge). Highest confidence; corresponds to a code FACT, not a
  `[STATED]` user need.
- **`[INFERRED]`** — reasoned from the code plus domain knowledge (precondition, responsibility, error
  semantics). Same word, same epistemic weight as the repo's `[INFERRED]`.
- **`[UNRESOLVED]`** — a seam the static analyzer could not resolve (dynamic dispatch, `getattr`,
  monkeypatching, decorator); identical to the repo's `[UNRESOLVED]`. Treated as "not statically
  observed," NOT "absent" (§2, §3).
- **`[LOST]`** — never in the code (rationale, rejected alternatives, intent). This is the
  redocumentation/decision-log gap; nothing in the source can recover it.

A `[RECOVERED]` clause is a defensible artifact; an `[INFERRED]` clause is a hypothesis; an `[LOST]`
item is an admission. Mislabeling an inference as recovered is the cardinal sin of design recovery.

---

## 2. What is RECOVERABLE vs INFERRED vs LOST — the three confidence tiers

The split is clean and load-bearing — **ESTABLISHED** (Ernst et al. / Daikon 2001; "Inferring Concise
Specifications of APIs," arXiv:1905.06847).

**Tier 1 — RECOVERABLE by static reading (high confidence).** Read directly, no reasoning:
component/module boundaries; public signatures (argument and return types from annotations); explicit
inheritance / realization edges; raised-exception sites; the import-dependency graph; statically
resolvable call edges. These are code FACTS and tag `[RECOVERED]`.

**Tier 2 — INFERRED (lower confidence, must be tagged).** Preconditions, postconditions, invariants,
intended responsibilities, error-mode semantics, and every "why." A crucial asymmetry **— ESTABLISHED**:
- **Static analysis recovers PREconditions far better than POSTconditions.** Preconditions and
  exception-triggering conditions are reachable via abstract interpretation and symbolic execution;
  POSTconditions and cross-field invariants are largely NOT statically inferable.
- **Dynamic invariants are HYPOTHESES, not facts.** Daikon discovers *likely* invariants from
  execution traces (Ernst et al., IEEE TSE 2001). A trace-derived invariant holds over the *observed*
  runs only; it must be tagged `[INFERRED]` (or `[HYPOTHESIS]`) and confirmed, never asserted as a
  recovered fact. The recoverer who promotes a Daikon output to `[RECOVERED]` has manufactured fiction.

**Tier 3 — LOST entirely.** Rationale, rejected alternatives, requirement intent. These never existed
in the code; no analysis recovers them. They are the province of the decision log / ADR (§10) and tag
`[LOST]` when absent.

This tiering IS the manifest's `[RECOVERED]`/`[INFERRED]`/`[UNRESOLVED]`(+`[LOST]`) tagging and aligns
with the repo's `[STATED]/[INFERRED]/[ASSUMED]/[UNRESOLVED]` legend (§1).

---

## 3. The design/architecture recovery METHOD

**Symphony provides the process skeleton — ESTABLISHED.** Symphony (van Deursen, Hofmeister, Koschke,
Moonen, Riva; WICSA 2004) is a view-driven, problem-driven reconstruction process. Its constructs map
directly onto this problem:
- **Source view** — built from source artifacts (imports, call graph, signatures): the as-built
  concrete view.
- **Target view** — the view the stakeholder needs (here, a signature-level design spec + an
  architecture-altitude dependency/boundary view).
- **Mapping rules** — how source entities become target entities.
- **HYPOTHETICAL view** — "the architect's expected/idealized architecture." Symphony states it serves
  either as a guide for reconstruction OR "as a baseline to compare with the system's current
  architecture." **In this manifest the upfront spec (SR-n contracts + `02_architecture.md`) IS the
  hypothetical view / baseline; the gap between it and the recovered concrete view IS the drift.**
Symphony names the motivating problem directly: cumulative maintenance causes architectural drift and
"a widening of the gap between requirements and code." Use Symphony's source-view / target-view /
mapping-rule structure as the recovery procedure's skeleton, and the reflexion model (§5) as the diff
engine over it.

**Altitude span.** Recover at two altitudes: architecture (component boundaries, dependency graph,
ports/seams) and detailed design (signatures, contracts, error modes). The static reading procedure:
extract type signatures, the import graph, and the call graph with a NAMED tool at a NAMED version;
read explicit inheritance and raised exceptions directly; then infer responsibilities and pre/post
contracts as Tier-2 `[INFERRED]` clauses.

**Python static recovery is intrinsically incomplete — VERSION-DEPENDENT.** PyCG (the reference static
Python call-graph generator; Salis et al., ICSE 2021) is flow-INsensitive and misses built-in-type
method calls (a large share of missing callees, e.g. `"abc".strip()`) and `super().method()` edges; HeaderGen/
JARVIS improve precision but none fully resolve dynamic dispatch, monkeypatching, `getattr`, or
decorators. Static type tools (mypy/pyright/pytype) only infer within the bounds of existing
annotations and stubs — an unannotated dynamic codebase yields a thin recovered model. Three
consequences **bind the recovery effort**:
1. **State which analyzer + version produced the source model.** "PyCG 0.x" is part of the recovered
   spec's provenance, not a footnote.
2. **Mark dynamically-dispatched or reflective seams `[UNRESOLVED]`** rather than asserting an edge is
   absent.
3. **Treat "no static call edge" as "not statically observed," NOT "does not happen."** Mistagging an
   unobserved edge as an absence manufactures a false divergence (§13, an OPEN question).

This is the SAME incompleteness the UML/OCL manifest catalogues (duck typing, decorators, async, MRO,
`setattr`). **Cross-reference `uml25_ocl_conformance_manifest.md §4` rather than re-deriving it.**

---

## 4. Writing the recovered detailed-design spec

**Reuse the repo's format; do not invent one — CC-FACT.** The target shape already exists:
`software_spec_discipline_manifest.md §A1–A2` (specify the contract not the computation; type-level
scaffolding allowed, bodies not), `§G2` (contracts signature-level and complete: typed contract,
invariants, error modes, nomenclature), `§G1` (one traceable spine SR-n → component → design spec →
verification). The worked exemplar is `resources/example-specs/mouse-jiggler/03_design_specs.md`: each component
gives a typed signature + docstring Preconditions/Postconditions/Error-modes/Purity + a Unit-test
design, with no algorithm.

A RECOVERED detailed-design spec emits that same structure with **two additions**:
1. **Per-clause provenance tags.** Every clause tagged `[RECOVERED]` (read off the code) vs `[INFERRED]`
   (reasoned) vs `[UNRESOLVED]` (seam the analyzer could not resolve). A signature is `[RECOVERED]`; a
   postcondition is almost always `[INFERRED]`; a `getattr`-dispatched call site is `[UNRESOLVED]`.
2. **A back-link from each recovered contract to the originating SR-n it appears to satisfy.** A
   recovered contract with **no SR found is an ORPHAN — itself a divergence** (it violates the
   allocation-completeness invariant, `software_spec_discipline_manifest.md §B3`: every component
   justifies itself by ≥1 requirement). An orphan is a DIVERGENCE verdict (§5) awaiting a ledger row.

**The honesty rule (the whole point).** The recovered spec is honest precisely when a reader can tell
which clauses are read off the code and which are the recoverer's reasoning. A spec without per-clause
provenance tags is a redrawing, not a recovery.

---

## 5. The reflexion model as the diff engine

**The Software Reflexion Model is the canonical drift-measuring technique — ESTABLISHED.** Murphy &
Notkin (FSE 1995; extended Murphy, Notkin & Sullivan, IEEE TSE 2001). An engineer (1) posits a
high-level model, (2) extracts a source model (call/dependency graph) from code, (3) declares a mapping
from source entities to model entities; a tool then computes where the two agree and differ. The output
is **EXACTLY three verdict categories** — adopt this vocabulary verbatim for the divergence ledger:

- **CONVERGENCE** — a relationship present in BOTH the hypothesized model and the source. *spec-says ==
  code-does.* The spec and code agree.
- **DIVERGENCE** — a relationship in the SOURCE but NOT the model. *code-does something the spec did not
  call for* — an extra dependency, undocumented behavior, an orphan contract (§4).
- **ABSENCE** — a relationship in the MODEL but NOT the source. *spec-says something the code does not
  do* — an unimplemented requirement, a dropped SR.

**Mapping.** Map spec elements (SR-n, components, contracts) to source elements (modules, classes,
call/import edges, signatures). The reflexion computation then labels each mapped relationship
convergence / divergence / absence.

**Iterative — ESTABLISHED.** Refine the model and mapping and recompute until the residual drift is
*understood* (not necessarily zero — §13 OPEN). The method "exploits, rather than removes, the drift
between design and implementation": a divergence is information, not merely an error to erase.

**Scalability.** Reflexion has been computed over 250 KLOC (NetBSD) in hours, so it scales to real
systems (Murphy & Notkin).

---

## 6. Classifying divergence — INTENDED / UNINTENDED / UNDOCUMENTED

A reflexion verdict says WHAT diverged; classification says WHY — and only the why tells you what to do
about it. The causal axis is Perry & Wolf's drift-vs-erosion **— ESTABLISHED**:

- **INTENDED** — the divergence has a documented decision behind it (an ADR / decision-log entry). A
  deliberate choice, correctly recorded. (Maps to a consulted-and-decided deviation.)
- **UNINTENDED** — the divergence contradicts the spec by accident or bug: Perry & Wolf **erosion** (the
  architecture was consulted and *violated*).
- **UNDOCUMENTED** — the divergence was introduced silently, with no record: Perry & Wolf **drift** (the
  architecture was *neglected* / not consulted). **The most dangerous class** — the spec and code
  disagree and *nobody decided that they should.*

**The promotion rule — ESTABLISHED.** An ADR / decision-log link **promotes UNDOCUMENTED → INTENDED.** A
divergence whose git evidence (§7) points to a commit that cites a DL-/ADR entry is reclassified from
UNDOCUMENTED to INTENDED. One with no such link stays UNDOCUMENTED until a decision is *written* — which
is the corrective action, NOT a silent edit (§8). The 2024 ICSA study confirms the field still splits
deviation into intended (deliberate, often-undocumented) vs unintended (accidental).

---

## 7. Git as evidence

Git turns "when/why did this drift happen" from opinion into evidence. Four primitives — **ESTABLISHED**:

- **`git blame`** — attributes each current line to the revision + author that last changed it
  (rename-following is automatic). Answers **WHO / WHEN** a divergent line entered.
- **`git log -S<string>` (pickaxe)** — finds commits that changed the NUMBER of occurrences of a string;
  locates the commit that *introduced or removed* a contract element (a Protocol name, a parameter, an
  exception type).
- **`git log -G<regex>`** — finds commits whose DIFF matches a regex; catches *modifications*, not just
  add/remove (e.g. a changed default, a narrowed type).
- **`git log --follow`** — tracks a file across renames/moves so the evidence trail survives refactors.
- **`git diff` against a TAGGED spec baseline** — the anchor that makes every other primitive
  meaningful: the divergence is *relative to* the baseline the spec was tagged at.

**The commit MESSAGE is the classification evidence — ESTABLISHED.** The commit at which a divergence
appears, plus its message, classifies it (§6): a message citing a decision (e.g. "DL-7: rename to
`PointerMotionSink`") ⇒ INTENDED; a message like "fix bug" that silently changed a contract ⇒
UNINTENDED; no message / an unrelated message ⇒ UNDOCUMENTED. The **Git Forensics** tradition (Tornhill,
*Code as a Crime Scene*; the `git-forensics` plugin) formalizes mining blame/log as analysis input.

**PREREQUISITE — VERSION-DEPENDENT / CC-FACT.** This entire discipline requires the implementation to be
committed against a **tagged spec baseline**, so the diff has an anchor. **The target implementation
repo must be under git with a tagged spec baseline** — re-verify this against the actual repo the team
runs on (in the sibling `bootstrap-kits/mouse-jiggler-implementation/` worked example it was not yet a git repo), so until that
holds this discipline is *prospective*.
The manifest mandates, before any git-evidenced drift tracking is meaningful: (1) put the implementation
under version control; (2) tag the commit that corresponds to the spec revision being recovered against
(the baseline); (3) stabilize the spec path (CLAUDE.md references `spec_mouse_jiggler/` while the spec
actually lives at `resources/example-specs/mouse-jiggler/` — fix before anchoring). Without a tagged baseline,
"the code drifted" has no fixed point to be measured from.

---

## 8. The divergence ledger

The required artifact. **One row per contract element (or per SR-n).** Columns:

| Column | Content |
|---|---|
| **SR-n** | the requirement / contract element under examination (or "orphan" if the code has a contract with no SR) |
| **spec-says** | what the upfront spec calls for |
| **code-does** | what the recovered as-built spec shows |
| **reflexion-verdict** | CONVERGENCE / DIVERGENCE / ABSENCE (§5) |
| **git-evidence** | commit SHA + `blame` (who/when) + commit message (§7) |
| **classification** | INTENDED / UNINTENDED / UNDOCUMENTED (§6) |
| **resolution** | fix-code / fix-spec / accept-as-decision (write the ADR) / leave-open |

**"Report, never silently reconcile" — ESTABLISHED + CC-FACT.** This follows from the reflexion model's
stance ("exploit, rather than remove, the drift") and from the repo's own discipline — it echoes
`software_spec_discipline_manifest.md §G4` ("record contested decisions, do not erase dissent") and
`§B2` ("silent assent is a failure"). Silently "fixing" the spec to match the code **destroys the
evidence that a requirement was dropped**; silently "fixing" the code **hides that the spec may have
been wrong.** Both are exactly the failure mode the discipline exists to prevent. Every divergence
surfaces as a tagged ledger row; the resolution is a *recorded decision*, never a quiet edit on either
side.

**Resolution options.** *fix-code* (the code is wrong, bring it to spec); *fix-spec* (the spec is wrong/
stale, bring it to code WITH a recorded decision); *accept-as-decision* (the divergence is fine — write
the ADR that makes it INTENDED, per §6's promotion rule); *leave-open* (under-determined; carry it as an
open item, `software_spec_discipline_manifest.md §G5`).

---

## 9. Executable conformance for the structural subset

**Structure is mechanizable; behavior is not — ESTABLISHED.** Fitness functions (Ford/Parsons/Kua,
*Building Evolutionary Architectures*) and tools like ArchUnit (Java) and Python's **import-linter**
encode architectural rules as automated tests run in CI. Import-linter's `layers`, `forbidden`, and
`independence` contract types check the import graph against declared rules and catch erosion *the moment
it is committed*.

For the mouse-jiggler architecture this **directly encodes AD-2 (functional core / imperative shell) and
AD-3 (dependency inversion at seams)** as CI gates: a contract that the pure core (`WaypointPolicy`,
`TrajectorySampler`, `ActivityDetector`, `ControlArbiter`) imports **no** adapter/OS module is
mechanically enforceable (`forbidden`/`layers`); the inverted seams (Protocols) are checked with
`independence`.

**The hard boundary — ESTABLISHED.** These tools verify **STRUCTURE only** (who-imports-whom, layering,
cycles). They **cannot** verify behavioral contracts: SR-2 (human-likeness), SR-3 (Fitts move-duration
band), SR-9 (reclaim timing) are *not* import-graph properties. Those remain **property/integration
tests** (the obligations the repo already specifies in `01_system_requirements.md` and the testing
manifest). So executable conformance covers the architecture-altitude *structural* spec; the detailed
*behavioral* spec still needs its test obligations. Do not claim a green import-linter run as evidence of
behavioral conformance — it is a category error (§13 OPEN: there may be no automated drift-detector for
SR-2/SR-3/SR-9 beyond re-running the property/integration suite).

---

## 10. Traceability & the decision log

**Bidirectional traceability per ISO/IEC/IEEE 29148 is the spine the ledger plugs into — ESTABLISHED.**
ISO/IEC/IEEE 29148:2018 formalizes the requirements traceability matrix as linking requirements both UP
(to needs) and DOWN (to design, code, verification), so "nothing is approved without evidence behind it"
and V&V links lead from test cases back to requirements. The recovery spine SR-n → component → design →
verification (`software_spec_discipline_manifest.md §G1`) IS a 29148-style bidirectional trace. **The
divergence ledger is what that trace produces when a downstream link is BROKEN (absence) or has an EXTRA
endpoint (divergence)** (§5).

**The ADR is the bridge from UNDOCUMENTED to INTENDED — ESTABLISHED.** An Architectural Decision Record
captures a single decision + rationale + rejected alternatives; the collection is the decision log.
ADRs are the standard mechanism for making intent auditable and tracing decisions back to requirements
— the *upstream-of-git* layer of evidence (git shows WHAT changed and WHEN; the ADR shows WHY it was
allowed to change). The repo's `05_decision_log.md` (DL-1..DL-9) is exactly an ADR set, already linked
to SR-n and AD-n.

**KNOWN GAP — cite honestly, ESTABLISHED.** Research notes ADRs are "often disconnected from the actual
system artifacts they influence — source code, models — which limits change-impact analysis and
conformance checking." So the divergence-tracking process must **actively MAINTAIN** the
`SR-n ↔ DL-n ↔ commit-SHA` links; they do not exist for free. A lightweight convention (a commit-message
trailer naming the DL-/ADR, parsed into the ledger) is the candidate for automating the
UNDOCUMENTED→INTENDED promotion — flagged OPEN (§13).

**26515 caution — ESTABLISHED.** ISO/IEC/IEEE 26515:2018 ("Developing information for users in an agile
environment") aligns user/help documentation with iterative/CI-CD delivery. It is relevant *only* as the
standard for keeping recovered documentation in sync under continuous change — it is **NOT** a standard
about reverse-engineering specs from code. **Do not cite 26515 as authority for the recovery METHOD;**
cite it (if at all) only for agile-doc-maintenance cadence.

---

## 11. The recovery + divergence loop (end to end)

**Two phases of one iterative loop — OPEN (synthesis, no single end-to-end authority).** No single cited
source prescribes this exact loop for THIS problem (recover-from-code + git-evidenced drift ledger +
INTENDED/UNINTENDED/UNDOCUMENTED). It is a synthesis: Chikofsky-Cross (recover) + Symphony (view +
hypothetical baseline) + reflexion model (diff into convergence/divergence/absence) + Perry-Wolf
(classify by cause) + git forensics (evidence) + ADR/decision-log (intent) + 29148 (traceability spine).
The team must own and defend the loop as a synthesis. The seven steps:

1. **Extract** the source model — imports, call graph, signatures — with a NAMED tool at a NAMED version
   (§3). Mark unresolved seams `[UNRESOLVED]`.
2. **Recover** an as-built design spec, every clause tagged `[RECOVERED]`/`[INFERRED]`/`[UNRESOLVED]`,
   each contract back-linked to an SR-n (orphan = divergence) (§4).
3. **Reflexion** — compute convergence/divergence/absence against the upfront SR-n / architecture
   (§5).
4. **Evidence** — for each divergence/absence, pull git evidence (blame + pickaxe/`-G` + commit
   message) and an ADR if one exists (§7).
5. **Classify** — INTENDED / UNINTENDED / UNDOCUMENTED, applying the ADR-link promotion rule (§6).
6. **Ledger + resolve** — record one row per element; propose a resolution (fix-code / fix-spec /
   accept-as-decision / leave-open). **Never silently reconcile** (§8).
7. **Iterate** — refine the model/mapping and recompute until residual drift is understood (§5; the
   acceptance bar is OPEN, §13).

Tag the full loop **OPEN / synthesis** wherever it is invoked as authority.

---

## 12. Worked anchor — `spec_mouse_jiggler`

Apply the loop to the mouse-jiggler spec (`resources/example-specs/mouse-jiggler/`). The spec's components are
the pure core `WaypointPolicy`, `TrajectorySampler`, `ActivityDetector`, `ControlArbiter` plus the
seam Protocols `PointerMotionSink`, `InputMonitor`, and the shell `Orchestrator` **[CC-FACT — read from
`01_system_requirements.md` / `03_design_specs.md`]**. Recover the as-built spec for the pure-core
components and the Protocol seams, then reflexion against SR-1..SR-11. Illustrative ledger rows
(template, not a measured result — the implementation is not yet under git, §7):

| SR-n | spec-says | code-does | verdict | git-evidence | classification | resolution |
|---|---|---|---|---|---|---|
| SR-2r | realizer Protocol named `PointerMotionSink`, method `move` | code exposes `PointerMotionSink.move` | CONVERGENCE (after rename) | `git log -S MouseEmulationSink` → the rename commit; message "DL-7: rename realizer Protocol, `emit`→`move`" | **INTENDED** (commit cites DL-7) | none — accept (documented) |
| SR-4 (removed) | (Rev A) USB-HID emulation realizer | code retains no HID-specific realizer | CONVERGENCE | `git log -S DeviceId` / `-S MouseEmulationSink` → removal commit citing **DL-6** | **INTENDED** (DL-6 drops SR-4) | none — spec already updated |
| SR-9 | while yielded, reclaim after `reclaim_timeout = 10 s` quiet | (e.g.) code uses a 5 s constant | DIVERGENCE | `git blame` on the constant → author/date; pickaxe `-G "reclaim_timeout|=\s*5"` → introducing commit; message "tune" | **UNDOCUMENTED** (no DL link) | leave-open → write DL or fix-code |
| SR-1 | continuous emission while DRIVING | (e.g.) `Orchestrator` has no driving-loop emit edge | ABSENCE | reflexion: model edge with no source edge; `git log --follow` on orchestrator file | **UNINTENDED** (erosion) | fix-code |
| orphan | (no SR) | a recovered helper Protocol with no SR back-link | DIVERGENCE | `git blame` → introducing commit | UNDOCUMENTED until classified | fix-spec (add SR or remove) |

Note how the DL-7 rename produces a **CONVERGENCE-after-rename** that is only visible because pickaxe
followed the old string (`MouseEmulationSink`) to the rename commit, and the commit message's `DL-7`
citation is what makes it INTENDED rather than UNDOCUMENTED. A dropped SR (SR-4 via DL-6) is an
*intended absence-that-became-convergence* — the spec was updated, so there is nothing to reconcile. An
SR with a model edge and no source edge (SR-1 example) is an **ABSENCE** ⇒ fix-code.

---

## 13. Open questions & caveats

- **Residual-drift acceptance bar — OPEN.** What residual divergence (count, or severity-weighted) is
  tolerable before the recovered spec or the implementation is declared non-conformant? No authoritative
  threshold exists; reflexion is iterated until drift is *understood*, not necessarily zero (§5). A
  project judgment call the manifest must flag as such.
- **INFERRED budget — OPEN.** At what ratio of `[INFERRED]` to `[RECOVERED]` clauses does a "recovered
  design spec" stop being recovery and become the recoverer's fiction? Chikofsky-Cross *legitimizes*
  domain-knowledge inference but gives no limit (§1, §2). Track the ratio; treat a high `[INFERRED]`
  fraction as a quality smell, not a hard fail.
- **Static-analysis floor for dynamic Python — VERSION-DEPENDENT.** Given PyCG/mypy incompleteness
  (dynamic dispatch, `getattr`, decorators, monkeypatching), distinguish "edge provably absent" from
  "edge not statically observed." Mistagging the latter as ABSENCE creates **false divergences** (§3).
  Cross-ref `uml25_ocl_conformance_manifest.md §4`.
- **Baseline anchoring — CC-FACT.** `bootstrap-kits/mouse-jiggler-implementation/` is not yet a git repo, and CLAUDE.md references
  `spec_mouse_jiggler/` while the spec lives at `resources/example-specs/mouse-jiggler/`. Mandate a tagged
  spec-baseline commit and a stable spec path before any git-evidenced drift tracking (§7).
- **Behavioral-contract conformance — OPEN.** Structural rules (imports/layers) are mechanizable via
  import-linter, but SR-2 (human-likeness), SR-3 (Fitts band), SR-9 (reclaim timing) are not. Whether
  any automated drift-detector exists for these beyond re-running the property/integration suite — or
  whether human reflexion is the only option — is unresolved (§9).
- **ADR-to-artifact linkage — OPEN.** ADRs are commonly disconnected from code. What lightweight
  convention (a parsed commit-message trailer naming the DL-/ADR?) reliably ties a DL-n/ADR to the
  implementing commit(s), so UNDOCUMENTED→INTENDED promotion is automatable rather than manual? (§6,
  §10.)
- **Round-trip authority — OPEN.** There is no single standard prescribing the full recover→reflexion→
  classify→ledger loop for spec-vs-code drift; this manifest's loop is necessarily a synthesis the team
  must own and defend (§11).

---

## Sources

- Chikofsky & Cross, "Reverse Engineering and Design Recovery: A Taxonomy," IEEE Software 7(1), 1990 —
  https://ieeexplore.ieee.org/document/43044 ; CMU copy
  https://www.cs.cmu.edu/~aldrich/courses/654-sp05/ReengineeringTaxonomy.pdf . Accessed 17 Jun 2026.
- Murphy, Notkin & Sullivan, "Software Reflexion Models: Bridging the Gap between Source and High-Level
  Models," ACM SIGSOFT FSE 1995 — https://www.cs.ubc.ca/~murphy/papers/rm/fse95.html ;
  https://dl.acm.org/doi/10.1145/222132.222136 ; extended IEEE TSE 2001. ReflexML —
  https://link.springer.com/chapter/10.1007/978-3-642-23798-0_37 . Accessed 17 Jun 2026.
- Perry & Wolf, "Foundations for the Study of Software Architecture," ACM SIGSOFT SEN 17(4), 1992 —
  https://www.researchgate.net/publication/2815761 . "We're Drifting Apart: Architectural Drift from the
  Developers' Perspective," ICSA 2024 — https://rebekkaa.github.io/files/2024_ICSA.pdf ; survey
  arXiv:2112.10934. Accessed 17 Jun 2026.
- Ernst et al., "Dynamically Discovering Likely Program Invariants" (Daikon), IEEE TSE 2001 —
  https://homes.cs.washington.edu/~mernst/pubs/invariants-tse2001.pdf . "Inferring Concise
  Specifications of APIs," arXiv:1905.06847 — https://arxiv.org/pdf/1905.06847 . Accessed 17 Jun 2026.
- Salis et al., "PyCG: Practical Call Graph Generation in Python," ICSE 2021 —
  https://github.com/vitsalis/PyCG . HeaderGen/JARVIS — https://pythonjarvis.github.io/ . Accessed
  17 Jun 2026.
- van Deursen, Hofmeister, Koschke, Moonen & Riva, "Symphony: View-Driven Software Architecture
  Reconstruction," WICSA 2004 — http://www.win.tue.nl/ipa/archive/springdays2005/Deursen2.pdf ;
  https://ieeexplore.ieee.org/document/1310696 . Accessed 17 Jun 2026.
- git-blame — https://git-scm.com/docs/git-blame ; pickaxe (`-S`/`-G`) —
  https://arestless.rest/blog/underrated-git-flag-pickaxe/ ; Tornhill, *Code as a Crime Scene* /
  git-forensics — https://github.com/jenkinsci/git-forensics-plugin . Accessed 17 Jun 2026.
- Import Linter contract types — https://import-linter.readthedocs.io/en/latest/contract_types.html ;
  ArchUnit — https://www.archunit.org/userguide/html/000_Index.html ; Ford, Parsons & Kua, *Building
  Evolutionary Architectures* (fitness functions). Accessed 17 Jun 2026.
- ADR — https://adr.github.io/ ; MS Azure WAF "Maintain an ADR" —
  https://learn.microsoft.com/en-us/azure/well-architected/architect-role/architecture-decision-record ;
  ADR trace-link gap —
  https://sdq.kastel.kit.edu/wiki/Trace_Link_Recovery_for_Architecture_Decision_Records_(ADRs) .
  Accessed 17 Jun 2026.
- ISO/IEC/IEEE 29148:2018 — https://www.iso.org/standard/72089.html ; RTM overview —
  https://www.reqview.com/blog/requirements-traceability-matrix/ ; ISO/IEC/IEEE 26515:2018 —
  https://www.iso.org/standard/70880.html . Accessed 17 Jun 2026.
- Local / repo (CC-FACT): `software_spec_discipline_manifest.md` (§A1–A2, §B2, §B3, §D2, §E2, §G1–G2,
  §G4, §G5); `uml25_ocl_conformance_manifest.md §4` (Python static-analysis traps);
  `resources/example-specs/mouse-jiggler/` (`01_system_requirements.md`, `03_design_specs.md`,
  `05_decision_log.md` DL-1..DL-9); `bootstrap-kits/mouse-jiggler-implementation/` verified NOT under git. Accessed 17 Jun 2026.
