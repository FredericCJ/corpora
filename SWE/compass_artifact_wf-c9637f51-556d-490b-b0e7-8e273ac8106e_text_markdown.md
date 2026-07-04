# Resource Corpus: Architecture, Design & Management of Large Simulink/MATLAB Projects

## TL;DR
- This corpus organizes ~55 verified resources into three explicit branches — **Architecture**, **Design**, **Management** — plus a clearly-marked automotive specialization band; anchor documents are confirmed: MAB Modeling Guidelines (v5.0, March 2020; MathWorks doc later renumbered to a date-based scheme, 23.2/R2023b), JMAAB v5.1 and v6.0 (v6.0 tool support R2023b), MISRA AC SLSF:2023 (2nd ed., "supersedes the first edition (published in 2009)"), and Roger Aarenstrup's *Managing Model-Based Design* (The MathWorks, 2015).
- The DAG is **BOTTOM-UP**: atomic detail-level roots (MAAB naming rules, signal typing, single-file structure, basic Git-for-Simulink mechanics) point UPWARD toward abstraction (governance frameworks, program-scale MBD management, safety lifecycle).
- Key verification correction: "MAAB" was renamed "MAB" (MathWorks Advisory Board) at v5.0 in March 2020; the MathWorks-hosted MAB PDF **never used a "6.0" label** (it moved to date-based numbering — 23.2 for R2023b — in September 2023), whereas "Version 6.0" **is** genuinely a JMAAB guideline version whose Model Advisor support arrived in R2023b (2023).

## Bottom-Up Rationale (quotable, for inclusion in the final corpus)
"Reasoning about higher-order abstraction requires first understanding the underlying detail. One cannot meaningfully evaluate a model-governance framework, a componentization strategy, or a program-level Model-Based Design rollout without first understanding the block-level and file-level mechanics it governs. Therefore this corpus is ordered bottom-up: the root nodes are the most atomic, practical, detail-level resources — specific modeling conventions, block-level practices, naming and interface standards, and basic configuration-management mechanics — and every edge points upward from these detail-level prerequisites to the higher-level material that abstracts them away."

## Key Findings
- **Openness split:** MathWorks documentation, MAB/JMAAB guidelines PDFs, MATLAB community style guides, and most technical articles are free/open. MISRA AC documents are paid (amendments and MISRA AC INT:2025 are free). ISO 26262 parts and SAE technical papers are paywalled (a MathWorks-hosted free PDF of SAE 2010-01-0938 exists). Academic papers vary; author-hosted/arXiv/CEUR copies noted.
- **The DESIGN branch holds the most roots** (naming/layout atoms, block/Stateflow patterns, data typing/fixed-point). The **ARCHITECTURE branch** bridges componentization mechanics up to System Composer/AUTOSAR. The **MANAGEMENT branch** spans version-control mechanics up to program-scale MBD and safety/certification.
- The richest academic sub-area is empirical Simulink study — clone detection, model smells, and curated corpora (SLNET, Boll et al., Chowdhury et al.).
- The automotive layer is genuinely cross-cutting: it appears as specialized nodes inside each branch rather than as a single isolated cluster, and should be rendered as a distinct visual lane over the domain-neutral core.

## Details

### BRANCH 2 — DESIGN (holds most roots; ordered bottom-up)

**Cluster D1 — Naming, layout & style atoms (ROOTS)**
- **MAB Control Algorithm Modeling Guidelines** (MathWorks Advisory Board). v5.0, March 2020 (R2020a); the MathWorks-hosted document was later renumbered (23.2 for R2023b, September 2023, then a date-based scheme 24.1/24.2/25.1…). Free PDF. **TARGET / CORE.** Naming conventions, diagram appearance, signal/block/subsystem naming, Simulink/Stateflow/MATLAB-Function rule sets.
- **JMAAB Control Algorithm Modeling Guidelines**, v5.1 and v6.0 (v6.0 Model Advisor check support in R2023b, 2023). Free. **CORE.** Automotive-originated but supplies domain-neutral core rules; feeds MAB.
- **Richard K. Johnson, *The Elements of MATLAB Style*, Cambridge University Press, 2010** (ISBN 978-0-521-73258-1; 182 pp.). Paid book. **TARGET (MATLAB code).** Formatting, naming, documentation, programming, testing.
- **Richard Johnson, "MATLAB Style Guidelines 2.0" and "MATLAB Programming Style Guidelines,"** MATLAB Central File Exchange (living, retrieved 2026). Free. **CORE.** Community-canonical predecessor to the book.
- **mathworks/MATLAB-Coding-Guidelines,** GitHub (MathWorks; published ~2024–2025, living). Free. **CORE.** Rules + Best Practices with a `codeAnalyzerConfiguration.json` enforced by the MATLAB Code Analyzer; explicitly aimed at "large organizations or teams of MATLAB developers."

**Cluster D2 — Block-level & Stateflow patterns**
- **MathWorks "MAB Modeling Guidelines" documentation sections** (Simulink, Stateflow, MATLAB Function rule sets) — living, tracks latest MATLAB release. Free. **CORE.**
- **MISRA AC SLSF:2023 — "Modelling design and style guidelines for the application of Simulink and Stateflow,"** MISRA Consortium, 2nd edition, June 2023 (ISBN 978-1-911700-06-7). Per MISRA: "Updated in June 2023, this second edition is the current version of MISRA AC SLSF. This document supersedes the first edition (published in 2009)." Plus **MISRA AC SLSF:2023 Amendments 1–4** — named "Amendment 1 Revisions for MATLAB Release R2023b" and "Amendment 2 Revisions for MATLAB Release R2024a June 2024," continuing to R2025a. Document paid; amendments and MISRA AC INT:2025 free. **TARGET (safety-critical design).**
- **MISRA AC GMG:2023 — "Generic Modelling Design and Style Guidelines,"** MISRA, June 2023 (ISBN 978-1-911700-04-3), likewise "supersedes the first edition (published in 2009)." Paid. Required companion when SLSF is used.

**Cluster D3 — Data typing & fixed point**
- **Fixed-Point Designer** (MathWorks product). Free docs. **CORE.** Per product description: "provides data types and tools for optimizing and implementing fixed-point and floating-point algorithms on embedded hardware… target-aware simulation that is bit-true for fixed point… test and debug quantization effects such as overflows and precision loss."
- **Simulink signal naming/typing guidance** (MAB signal rules; data type propagation). **CORE.**

**Cluster D4 — Design for code generation**
- **Embedded Coder documentation + production-code modeling patterns.** Free docs. **CORE.**
- **dSPACE "Modeling Guidelines for MATLAB/Simulink/Stateflow and TargetLink,"** dSPACE GmbH (v1.0 era, ~2006; living). Free PDF (~162 pp.). **CORE (automotive-adjacent).** Covers model structure for TargetLink code gen, Stateflow code, fixed-point code generation, MISRA C compliance; explicitly recommends using the MAAB/MAB guide alongside it.

**Cluster D5 — Design quality: smells, clones, complexity (SURVEY-heavy)**
- **Deissenboeck, Hummel, Jürgens, Schätz, Wagner, Girard, Teuchert, "Clone Detection in Automotive Model-Based Development,"** ICSE 2008, pp. 603–612 (ACM/IEEE). Paid; author copies free. **TARGET (clones).**
- **Alalfi, Cordy, Dean, Stephan, Stevenson, "Models are Code Too: Near-miss Clone Detection for Simulink Models,"** ICSM 2012, pp. 295–304. Free author copy (Queen's University). **ADVANCED.**
- **Gerlitz, Tran, Dziobek, "Detection and Handling of Model Smells for MATLAB/Simulink Models,"** MASE@MoDELS 2015, pp. 13–22 (CEUR Vol-1487). Free (CEUR). **TARGET (smells).** Catalog of anti-patterns collected with an automotive OEM.
- **Stephan & Cordy, "Identification of Simulink Model Antipattern Instances Using Model Clone Detection,"** MODELS 2015, pp. 276–285. **ADVANCED.**

### BRANCH 1 — ARCHITECTURE (bottom-up)

**Cluster A1 — Componentization mechanics (ROOTS of this branch)**
- **MathWorks "Component-Based Modeling in Simulink" / "Model Reference Behavior and Capabilities" / "Model References"** docs — living. Free. **TARGET.** Subsystems vs. libraries vs. model reference vs. subsystem reference; SLX-per-component; parallel/incremental builds.
- **"Reference Existing Models" and related model-reference docs** — parallel independent development, isolated verification. Free. **CORE.**

**Cluster A2 — Interfaces & data contracts**
- **Simulink.Bus / Bus objects docs** ("Specify Bus Properties with Bus Objects," "When to Use Bus Objects"). Free. **TARGET.** Per docs: "A Simulink.Bus object specifies only the architectural properties of a bus… analogous to a structure definition in C… By specifying a bus object with the same hierarchy and properties at both sides of the interface, you enforce consistency at the interface between the two components."
- **Simulink Data Dictionary docs** ("What Is a Data Dictionary?") — `.sldd` files; Design Data + Architectural Data ("port interfaces, data types, and system wide constants"); introduced R2015a. Free. **CORE (interface contract).**

**Cluster A3 — Model architecture strategies**
- **"Large-Scale Modeling" documentation chapter** (Simulink) — componentization, projects, reuse. Free. **TARGET / SURVEY (¶).**
- **"Applying Best Practices for Building Large Simulink Models,"** MathWorks technical article (based on the MathWorks Automotive Conference talk "Best Practices for Building Large Models from Components to Complex Systems"). Free. **SURVEY (¶).**
- **"Large-Scale Modeling for Embedded Applications,"** SAE Technical Paper **2010-01-0938** (MathWorks). Paid (SAE); free MathWorks-hosted PDF exists. **ADVANCED.** Recommends partitioning top-level components as model reference in Accelerator mode and blending with atomic subsystem libraries at lower levels; virtual buses except at model-reference boundaries.
- **"Best Practices for Large-Scale Architecture Modeling,"** System Composer doc. Free. **CORE.**

**Cluster A4 — System-level architecture**
- **System Composer documentation** (MathWorks MBSE add-on) — components, ports, connectors, interfaces; model-to-model allocations; live views; code gen for software/AUTOSAR architectures. Free docs. **TARGET.**
- **AUTOSAR Blockset documentation + "Software Architecture Modeling"** (Classic/Adaptive platforms; ARXML import/export; compositions and components; requires System Composer for architecture models). Free docs. **CORE (automotive).**

**MATLAB code architecture (shared/bridging within Architecture)**
- **MATLAB packages/namespaces, classes/OOP guide, toolbox packaging docs** — living. Free. **CORE.** Bridges to Design cluster D1.

### BRANCH 3 — MANAGEMENT (bottom-up)

**Cluster M1 — Version-control mechanics (ROOTS)**
- **MathWorks "Model Comparison" docs** (Comparison Tool, `visdiff`, Three-Way Merge Tool). Free. **TARGET.**
- **"Resolve Conflicts in Project Using Simulink Three-Way Merge" and "Customize External Source Control to Use MATLAB for Diff and Merge"** (Git, SVN, Perforce, SourceTree; `git difftool -t mlDiff`, `mlMerge`, `mlAutoMerge`). Free. **CORE.**
- **Simulink Projects / MATLAB Projects docs** (organize files, source-control integration, dependency analysis). Free. **CORE.**
- **"Three-Way Model Merge and Git,"** Guy on Simulink blog (2016). Free. **CORE (practitioner).**
- **dSPACE "Model Compare"** (Diff & Merge for Simulink/Stateflow/TargetLink; three-way analysis; Git/CLI/CI integration). Vendor page free. **ADVANCED (automotive tooling).**

**Cluster M2 — Verification & CI mechanics**
- **"Continuous Integration for Verification of Simulink Models" (Part 1),** MathWorks technical article (Jenkins + GitLab + Simulink Test), circa 2020, living. Free. **TARGET.** Companion example repo: `mathworks/Continuous-Integration-Verification-Simulink-Models`.
- **"Continuous Integration for Verification of Simulink Models Using GitLab" (Part 2)** (GitLab for both version control and CI). Free. **CORE.**
- **Simulink Test docs + "Continuous Integration"** (MATLAB Unit Test plugins; CI-compatible results). Free. **CORE.**
- **Simulink Coverage docs** (model coverage including MC/DC). Free. **CORE.**
- **MATLAB build tool** ("Overview of MATLAB Build Tool"; `buildtool`; **introduced R2022b**). Free. **CORE.**
- **MATLAB Test** (distinct product, **released R2023a, March 2023**; condition/decision/MC-DC coverage of MATLAB code, project quality dashboard). Free docs. **CORE.**
- **"Set Up Simulink Diff and Merge in CI/CD Pipeline"** (auto-merge; attach comparison reports to GitHub/GitLab merge/pull requests). Free. **CORE.**

**Cluster M3 — Traceability & requirements**
- **Requirements Toolbox** (formerly Simulink Requirements) docs — author/link/validate requirements; digital thread across requirements, models, code, tests, data dictionaries; Requirements Table for formal requirements. Free docs. **TARGET.**
- **"Working with IBM DOORS Requirements," "Link and Trace Requirements with IBM DOORS Next,"** and surrogate-module synchronization docs (bidirectional traceability, ReqIF, Jama/Polarion). Free. **CORE.**

**Cluster M4 — Quality governance & metrics**
- **Simulink Check docs** — Model Advisor, MAB/JMAAB checks, Modeling Standards. Free docs. **TARGET.**
- **"Metrics Dashboard"** — per docs: "widgets that visualize metric data in these categories: size, modeling guideline compliance, and architecture." Free. **CORE.**
- **"Model Maintainability Dashboard"** — project-level metric collection across MATLAB code, Simulink models, Stateflow charts; per docs the metrics "help you determine if parts of a design are too complex and need to be refactored." Free. **CORE.**

**Cluster M5 — Team-scale & program-scale management (ABSTRACTION APEX)**
- **Roger Aarenstrup, *Managing Model-Based Design*, The MathWorks, Inc., 2015** (ISBN 978-1512036138; CreateSpace print; copyright 2015–2025). Free ebook PDF hosted by MathWorks. **TARGET / SURVEY (¶).** Automotive/aerospace/communications case studies; makes the business/organizational case for MBD adoption and management of complexity.
- **Empirical corpora & studies (SURVEY band, feed governance):**
  - **Shrestha, Chowdhury, Csallner, "SLNET: A Redistributable Corpus of 3rd-party Simulink Models," MSR 2022** (arXiv 2203.17112). Free. **SURVEY (¶).** Per the paper: "Removing 112 potentially duplicate plus 10 dummy projects yielded 2,837 projects and their 9,117 Simulink models in SLNET" — "8 times larger than the largest previous corpus of Simulink models."
  - **Chowdhury et al., "A Curated Corpus of Simulink Models for Model-Based Empirical Studies," SEsCPS@ICSE 2018.** Paid (ACM). **ADVANCED.** Presents "a corpus of over 1,000 freely available MathWorks Simulink models."
  - **Boll, Brokhausen, Amorim, Kehrer, Vogelsang, "Characteristics, potentials, and limitations of open-source Simulink projects for empirical research," *Software & Systems Modeling* 20:2111–2130, 2021.** Free full text available. **SURVEY (¶).** Per the paper: "we investigate a set of 1,734 freely available Simulink models from 194 projects and analyze their suitability for empirical research."
  - **Shrestha, Chowdhury, Csallner, "Replicability Study: Corpora For Understanding Simulink Models & Projects," 2023** (arXiv 2308.01978). Free. **ADVANCED.**

**Cluster M6 — Safety & certification management (AUTOMOTIVE + aerospace specialization)**
- **ISO 26262-6:2018, "Road vehicles — Functional safety — Part 6: Product development at the software level,"** ISO, 2018 (2nd ed., revised from 2011). Paywalled. **TARGET (automotive safety).** The 2018 revision added model-based-development guidance; covers software architectural design, unit design/implementation/verification, and integration/testing under ASILs.
- **RTCA DO-331 / EUROCAE ED-218, "Model-Based Development and Verification Supplement to DO-178C and DO-278A,"** RTCA, dated December 13, 2011. Paid. **TARGET (aerospace).** Adds model coverage analysis and rules for when models serve as requirements, design, or source code.
- **IEC Certification Kit** (ISO 26262 & IEC 61508) and **DO Qualification Kit** (DO-178C/DO-331) — MathWorks tool-qualification products. Free docs. **CORE.**
- **dSPACE TargetLink** — production code generator from Simulink/Stateflow; ISO 26262-, ISO 25119-, and IEC 61508-certified; AUTOSAR support. Vendor docs free. **CORE (automotive).**

### Automotive specialization band (cross-cutting, clearly marked)
Nodes forming the automotive layer: JMAAB v5.1/v6.0 (D1), MISRA AC SLSF:2023 / MISRA AC GMG:2023 (D2), dSPACE TargetLink guidelines (D4) and dSPACE Model Compare / TargetLink (M1/M6), AUTOSAR Blockset + System Composer AUTOSAR composition (A4), ISO 26262-6, IEC Certification Kit / DO Qualification Kit (M6), and SAE 2010-01-0938 bridging architecture. DO-331 sits in a certification cluster that is aerospace-flavored but adjacent to the automotive safety band. The **domain-neutral core** (MathWorks docs, MATLAB style guides, Simulink Test/Check/Coverage/Requirements, Projects, CI articles, Aarenstrup, empirical corpora) serves any industry and should render as the visually primary layer.

## DAG Edge List (detail → abstraction; "D" = drawn, "N" = not-drawn prose edge)

**Design branch internal**
1. [D] MAB naming/layout atoms → MAB Modeling Guidelines doc sections. *Shared: naming conventions, diagram appearance.*
2. [D] JMAAB v5.1/v6.0 → MAB doc sections. *Shared: JMAAB feeds MAB rule lineage.*
3. [D] Johnson *Elements of MATLAB Style* → MATLAB-Coding-Guidelines (GitHub). *Shared: naming, formatting, function design.*
4. [N] MATLAB Style Guidelines 2.0 → *Elements of MATLAB Style*. *Shared: same author, superset content.*
5. [D] MAB Modeling Guidelines doc → MISRA AC SLSF:2023. *Shared: block/Stateflow style rules, allowable-block criteria.*
6. [D] MISRA AC GMG:2023 → MISRA AC SLSF:2023. *Shared: generic modeling-rule subset (required companion).*
7. [D] Fixed-Point Designer → Embedded Coder design-for-codegen. *Shared: fixed-point types, quantization for target code.*
8. [D] MAB signal typing → Fixed-Point Designer. *Shared: data-typing atoms.*
9. [D] MAB Modeling Guidelines doc → Design-smells/clones cluster (Gerlitz; Deissenboeck). *Shared: readability/complexity criteria the smells operationalize.*
10. [D] Deissenboeck 2008 → Alalfi 2012 → Stephan/Cordy 2015. *Shared: clone-detection lineage.*

**Architecture branch internal**
11. [D] Component-Based Modeling / Model Reference docs → Large-Scale Modeling chapter. *Shared: componentization mechanics.*
12. [D] Bus objects docs → Data Dictionary docs. *Shared: interface definition, type consistency.*
13. [D] Data Dictionary docs → Large-Scale Modeling chapter. *Shared: centralized interface repository.*
14. [D] Large-Scale Modeling chapter → SAE 2010-01-0938. *Shared: model-reference partitioning strategy.*
15. [D] Large-Scale Modeling → "Applying Best Practices for Building Large Simulink Models." *Shared: componentization at scale.*
16. [D] Best Practices article + SAE 2010-01-0938 → System Composer / Best Practices for Large-Scale Architecture Modeling. *Shared: component reuse, interfaces.*
17. [D] Bus objects + Data Dictionary → System Composer. *Shared: interfaces as architecture contracts.*
18. [D] System Composer → AUTOSAR Blockset / Software Architecture Modeling. *Shared: composition/component authoring, ARXML.*
19. [N] MATLAB packages/OOP/toolbox packaging → MATLAB-Coding-Guidelines. *Shared: code organization (bridges to Design D1).*

**Cross-branch (Design/Architecture → Management)**
20. [D] MAB Modeling Guidelines doc → Simulink Check / Model Advisor (M4). *Shared: checks enforce MAB/JMAAB rules.*
21. [D] Component-Based Modeling (A1) → Version-control mechanics (M1). *Shared: componentization for CM — SLX-per-component enables clean diff/merge.*
22. [D] Model Reference docs (A1) → CI for Verification article (M2). *Shared: independent component testing in CI.*

**Management branch internal**
23. [D] Model Comparison / Three-Way Merge → Simulink/MATLAB Projects. *Shared: source-control workflow.*
24. [D] Projects → CI for Verification (Part 1). *Shared: project as CI unit, Git integration.*
25. [D] Simulink Test + Coverage → CI for Verification. *Shared: automated requirements-based testing in pipeline.*
26. [D] MATLAB build tool + MATLAB Test → CI for Verification / Set Up Diff-Merge in CI/CD. *Shared: build/test automation.*
27. [D] CI Part 1 → CI Part 2 (GitLab). *Shared: same workflow, different CI host.*
28. [D] Simulink Check / Model Advisor → Metrics Dashboard → Model Maintainability Dashboard. *Shared: metric collection escalating to governance.*
29. [D] Requirements Toolbox → DOORS traceability docs. *Shared: external-tool linking.*
30. [D] Requirements Toolbox (M3) + Simulink Test (M2) → Aarenstrup *Managing MBD* (M5). *Shared: traceability & V&V as managed process.*
31. [D] Metrics/Maintainability Dashboards (M4) → Aarenstrup / empirical corpora (M5). *Shared: model-quality governance evidence.*
32. [D] SLNET → Replicability Study 2023; Boll 2021 → Replicability Study 2023. *Shared: corpus lineage.*
33. [D] Empirical corpora (M5) → governance apex (M4/M5). *Shared: empirical basis for quality metrics/thresholds.*
34. [D] Simulink Check + Requirements Toolbox + Simulink Test → IEC Certification Kit / DO Qualification Kit (M6). *Shared: qualified V&V evidence.*
35. [D] ISO 26262-6 + DO-331 → Aarenstrup / program-scale management (apex). *Shared: safety lifecycle governs program management.*
36. [D] dSPACE TargetLink guidelines (D4) → TargetLink / Model Compare (M6/M1). *Shared: production code-gen toolchain.*
37. [D] AUTOSAR Blockset (A4) → ISO 26262-6 workflow (M6). *Shared: automotive production ECU software.*

**Not-drawn prose edges (limit clutter):** 4, 19; plus transitive shortcuts implied by chains (e.g., MAB atoms → System Composer via Large-Scale Modeling need not be drawn directly).

## Target / Core / Advanced / Survey designations
- **TARGETS (cluster anchors):** MAB Guidelines (D1); MISRA AC SLSF:2023 (D2); Fixed-Point Designer (D3); Embedded Coder (D4); Deissenboeck 2008 + Gerlitz 2015 (D5); Model Reference docs (A1); Bus objects (A2); Large-Scale Modeling chapter (A3); System Composer (A4); Model Comparison/Three-Way Merge (M1); CI for Verification article (M2); Requirements Toolbox (M3); Simulink Check (M4); Aarenstrup (M5); ISO 26262-6 + DO-331 (M6).
- **SURVEY / overview (¶):** Large-Scale Modeling chapter; "Applying Best Practices…" article; Aarenstrup; SLNET; Boll 2021; Replicability Study 2023.
- **ADVANCED:** SAE 2010-01-0938; Alalfi 2012; Stephan/Cordy 2015; dSPACE Model Compare; Chowdhury 2018; Replicability Study 2023.
- **CORE:** remaining MathWorks docs, community style guides, and guidelines.

## Recommendations
1. **Seed the graph** with three root anchors — one per branch: D1 (MAB naming atoms), M1 (Model Comparison / diff-merge mechanics), A1 (Model Reference / component-based modeling). These are the most atomic and have the highest out-degree.
2. **Render the transitive-reduction rendering** by drawing edges 1–3, 5–18, 20–37; list edges 4 and 19 plus transitive shortcuts as prose-only.
3. **Mark the automotive band** as a distinct color/lane spanning all three branches; keep the domain-neutral core visually primary.
4. **Treat the three apexes explicitly:** Aarenstrup + the empirical-corpus cluster as the Management abstraction apex; System Composer/AUTOSAR as the Architecture apex; MISRA AC SLSF:2023 as the Design apex.
5. **Staging/threshold to change the render:** if the drawn graph is too dense, promote edges 9, 28, 31, and 33 to prose-only first — they are governance escalations that remain safely inferable. If node count must be cut, drop ADVANCED academic nodes (Alalfi 2012, Stephan/Cordy 2015, Chowdhury 2018, Replicability 2023) before any CORE MathWorks doc, since the TARGET academic anchors (Deissenboeck 2008, Gerlitz 2015, SLNET, Boll 2021) preserve the sub-area's lineage.

## Caveats & Verification Uncertainties
- **MAAB→MAB rename:** Confirmed — renamed at v5.0, March 2020: "MAAB guidelines revised and reintroduced as the MathWorks Advisory Board (MAB) Modeling Guidelines, Version 5.0 (Release 2020a)."
- **"MAB v6.0" does NOT exist** in MathWorks' own numbering. The MathWorks MAB PDF revision history goes 5.0 (2020a) → held through R2023a → 23.2 (R2023b, September 2023) → date-based (24.1, 24.2, 25.1…). "Version 6.0" is a genuine **JMAAB** version (Model Advisor support R2023b/2023). JMAAB v5.1 confirmed. Treat the task's hypothesized "MAB 6.0 (2022)" as incorrect.
- **MISRA AC SLSF:** current = 2023 2nd edition (ISBN 978-1-911700-06-7), "supersedes the first edition (published in 2009)"; Amendments 1–4 track R2023b–R2025a. **MISRA AC TL** (TargetLink) and **MISRA AC AGC** are historical — MISRA no longer maintains code-generator-specific guidelines (AGC folded into MISRA C); the maintained line is MISRA AC GMG → MISRA AC SLSF. Flag MISRA AC TL as "historical/legacy" if included.
- **Aarenstrup:** confirmed 2015, ISBN 978-1512036138, published by The MathWorks (CreateSpace print); free ebook PDF hosted by MathWorks (copyright 2015–2025).
- **SAE 2010-01-0938** ("Large-Scale Modeling for Embedded Applications") confirmed; free MathWorks-hosted PDF exists alongside the paywalled SAE copy.
- **Deissenboeck year:** the paper is in the ICSE 2008 proceedings (pp. 603–612); some citations mislabel it 2009. Cite as ICSE 2008.
- **MATLAB build tool (R2022b) and MATLAB Test (R2023a)** confirmed via targeted verification.
- **Excluded/optional (unverified for large-project content):** Higham & Higham *MATLAB Guide* (SIAM, 3rd ed. 2017) and Nicolescu & Mosterman (eds.) *Model-Based Design for Embedded Systems* (CRC, 2009) — recommend EXCLUDE unless a specific chapter is confirmed to carry Simulink large-project or model-architecture material; both are otherwise general and risk violating the corpus's independence from control-theory/general-SE literature.
- **Free-copy availability** of paywalled academic papers (ACM/IEEE) and SAE papers varies over time; author-hosted PDFs (Queen's, arXiv, CEUR, ResearchGate) and the MathWorks tag-team PDF were the free sources located at time of research.
- **Independence maintained:** no general software-architecture texts (Bass–Clements–Kazman, Perry–Wolf) or control-theory texts are included; every node is Simulink/MATLAB/MBD-specific or generic tooling applied to Simulink/MATLAB (e.g., Git-with-Simulink docs rather than a generic Git book).