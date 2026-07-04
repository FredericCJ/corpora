# Software Architecture as a Science: A Clustered, Typed Reading-Graph Corpus

## TL;DR
- This corpus assembles ~60 methodologically rigorous nodes organized into two explicit branches — **software architecture as artifact/discipline (Branch A)** and **architecture design as process (Branch B)** — plus **shared bridging infrastructure**, each node carrying a verified citation (year of last publication), a core/advanced/target/survey tier, and an open-access flag.
- Critical edition/standard verifications for the graph: **ISO/IEC/IEEE 42010:2022** (2nd ed., published 2022‑11‑07); **ISO/IEC 25010:2023** (2nd ed., published 2023‑11‑15); **Bass–Clements–Kazman 4th ed. (Aug 3, 2021)**; **Cervantes–Kazman 2nd ed. (Jun 14, 2024)**; **Documenting Software Architectures 2nd ed. (2010)**. **Taylor–Medvidovic–Dashofy has NO second edition — the Wiley first edition (©2010, printed 2009) is the only one**, contradicting the task's hypothesis.
- A directed **cyclic** graph over a fixed 9‑relation vocabulary connects the nodes with **four documented genuine cycles** (ADL‑research↔42010↔industry‑needs; architectural‑mismatch 1995↔2009; design‑rationale↔decision‑centric architecture↔AKM; ADD↔quality‑attribute scenarios/ATAM).

---

## Relation Vocabulary (edge tags — fixed set of 9)
1. **prerequisite-of** — source must be understood before target (conceptual dependency).
2. **refines** — target elaborates/operationalizes a concept from source at finer granularity.
3. **evaluates / is-evaluated-by** — one node supplies a method for assessing artifacts produced under another (directional pair).
4. **formalizes** — target supplies formal semantics/mathematics to an informal notion in source.
5. **surveys** — target is a survey/classification/tutorial that catalogs and compares source(s).
6. **applies-method-of** — target reuses a method/technique defined in source as an internal step.
7. **complements** — mutually reinforcing; neither subsumes the other.
8. **subsumes** — target generalizes/absorbs source's scope.
9. **critiques / feeds-back-into** — target challenges or empirically re‑scopes source, changing subsequent work (the relation used to form cycles).

---

## Two-Branch + Cluster Organization

**BRANCH A — Architecture as Artifact/Discipline**
- A1 Foundations of the discipline (CANONICAL)
- A2 Views & description frameworks (CANONICAL)
- A3 ADLs & formal semantics (COMPREHENSIVENESS)
- A4 Model checking & formal verification of architectures (COMPREHENSIVENESS)
- A5 Dynamic / self-adaptive architectures (COMPREHENSIVENESS)
- A6 Architecture evolution (COMPREHENSIVENESS)
- A7 Reference architectures & product lines (COMPREHENSIVENESS)

**BRANCH B — Architecture Design as Process**
- B1 Design-process roots / design science (CANONICAL)
- B2 Design methods & the general design model (CANONICAL)
- B3 Design rationale & architectural knowledge (COMPREHENSIVENESS)
- B4 Empirical studies of design reasoning (COMPREHENSIVENESS)

**SHARED / BRIDGING INFRASTRUCTURE**
- S1 Evaluation canon (CANONICAL) — bridges artifact (what is evaluated) and process (evaluation feeds design)
- S2 Quality-attribute models (bridging)
- S3 Economics & technical debt (bridging)

---

## Full Verified Citations by Cluster
Tier legend: **★** = target/canonical anchor for its cluster; **C** = core tier; **A** = advanced tier; **¶** = survey/tutorial admitted as a first‑class node. OA = open-access status (yes / partial = repository or ResearchGate copy exists but no confirmed rights‑clean publisher/author PDF / no).

### Cluster A1 — Foundations of the discipline (Branch A · CANONICAL)
- **★C Perry, D.E. & Wolf, A.L. (1992).** "Foundations for the Study of Software Architecture." *ACM SIGSOFT Software Engineering Notes* 17(4):40–52. OA-yes.
- **★C Shaw, M. & Garlan, D. (1996).** *Software Architecture: Perspectives on an Emerging Discipline.* Prentice Hall. OA-no.
- **C Garlan, D. & Shaw, M. (1993).** "An Introduction to Software Architecture." In *Advances in Software Engineering and Knowledge Engineering*, Vol. 1, World Scientific, pp. 1–39. OA-yes (CMU tech-report version).
- **★C Taylor, R.N., Medvidovic, N. & Dashofy, E.M. (2010).** *Software Architecture: Foundations, Theory, and Practice.* John Wiley & Sons, ©2010, 736 pp. ISBN‑13 978‑0470167748. **Only edition; no 2nd edition exists** (ACM DL lists ©2010; AbeBooks records label the Wiley printing "1st Edition, 2009‑01‑09"). OA-no.
- **C Bass, L., Clements, P. & Kazman, R. (2021).** *Software Architecture in Practice*, 4th ed. Addison-Wesley (SEI Series). Published **Aug 3, 2021**; print ISBN 978‑0‑13‑688609‑9, e‑ISBN 978‑0‑13‑688567‑2. OA-no.
- **A¶ Shaw, M. (2001).** "The Coming-of-Age of Software Architecture Research." *Proc. ICSE 2001.* OA-yes.
- **A¶ Garlan, D. (2014).** "Software Architecture: a Travelogue." *Proc. FOSE 2014 (Future of Software Engineering).* OA-yes (CMU-hosted).

### Cluster A2 — Views & description frameworks (Branch A · CANONICAL)
- **★C ISO/IEC/IEEE 42010:2022.** *Software, systems and enterprise — Architecture description.* 2nd ed., **published 2022‑11‑07** (IEEE‑SA board approval 2022‑09‑21; WG chair Richard Hilliard). Cancels/replaces 42010:2011 (which fast‑tracked IEEE 1471:2000); key changes include "system of interest"→"entity of interest" and "architecture framework"→"architecture description framework (ADF)." OA-no (standard).
- **★C Clements, P., Bachmann, F., Bass, L., Garlan, D., Ivers, J., Little, R., Merson, P., Nord, R. & Stafford, J. (2010).** *Documenting Software Architectures: Views and Beyond*, 2nd ed. Addison-Wesley. OA-no.
- **C Kruchten, P. (1995).** "Architectural Blueprints — The '4+1' View Model of Software Architecture." *IEEE Software* 12(6):42–50. OA-yes.
- **C Rozanski, N. & Woods, E. (2011).** *Software Systems Architecture: Working with Stakeholders Using Viewpoints and Perspectives*, 2nd ed. Addison-Wesley. **BORDERLINE on the science bar** — admitted as a viewpoint‑framework reference, not as formal theory. OA-no.
- **C Hofmeister, C., Nord, R. & Soni, D. (2000).** *Applied Software Architecture.* Addison-Wesley. OA-no.
- **A Emery, D. & Hilliard, R. (2009).** "Every Architecture Description Needs a Framework: Expressing Architecture Frameworks Using ISO/IEC 42010." *Proc. WICSA/ECSA 2009.* OA-yes.
- **A Medvidovic, N., Rosenblum, D.S., Redmiles, D.F. & Robbins, J.E. (2002).** "Modeling Software Architectures in the Unified Modeling Language." *ACM TOSEM* 11(1):2–57. OA-partial.

### Cluster A3 — ADLs & formal semantics (Branch A · COMPREHENSIVENESS)
- **★C¶ Medvidovic, N. & Taylor, R.N. (2000).** "A Classification and Comparison Framework for Software Architecture Description Languages." *IEEE TSE* 26(1):70–93. OA-yes (HAL hal‑00444077).
- **★A Allen, R. & Garlan, D. (1997).** "A Formal Basis for Architectural Connection" (Wright, CSP semantics). *ACM TOSEM* 6(3):213–249. OA-partial.
- **A Luckham, D.C., Kenney, J.J., Augustin, L.M., Vera, J., Bryan, D. & Mann, W. (1995).** "Specification and Analysis of System Architecture Using Rapide." *IEEE TSE* 21(4):336–355. OA-no.
- **A Magee, J. & Kramer, J. (1996).** "Dynamic Structure in Software Architectures" (Darwin). *Proc. FSE‑4; ACM SIGSOFT SEN* 21(6):3–14. OA-partial.
- **A Garlan, D., Monroe, R.T. & Wile, D. (1997).** "Acme: An Architecture Description Interchange Language." *Proc. CASCON '97*, pp. 169–183 (reprinted in *CASCON First Decade High Impact Papers*, 2010, pp. 159–173). OA-yes (CMU/DTIC).
- **A Moriconi, M., Qian, X. & Riemenschneider, R.A. (1995).** "Correct Architecture Refinement." *IEEE TSE* 21(4):356–372. OA-no.
- **A Oquendo, F. (2004).** "π‑ADL: an Architecture Description Language based on the higher‑order typed π‑calculus for specifying dynamic and mobile software architectures." *ACM SIGSOFT SEN* 29(3):1–14. OA-partial.
- **A Feiler, P.H. & Gluch, D.P. (2012).** *Model-Based Engineering with AADL: An Introduction to the SAE Architecture Analysis & Design Language.* Addison-Wesley (SEI Series). OA-no.
- **A Abowd, G.D., Allen, R. & Garlan, D. (1995).** "Formalizing Style to Understand Descriptions of Software Architecture." *ACM TOSEM* 4(4):319–364. OA-yes (CMU TR CMU‑CS‑95‑111).
- **A Bernardo, M. & Inverardi, P. (eds.) (2003).** *Formal Methods for Software Architectures* (SFM 2003). Springer LNCS 2804. OA-no.
- **A Aldini, A., Bernardo, M. & Corradini, F. (2010).** *A Process Algebraic Approach to Software Architecture Design.* Springer. OA-no.
- **A¶ Malavolta, I., Lago, P., Muccini, H., Pelliccione, P. & Tang, A. (2013).** "What Industry Needs from Architectural Languages: A Survey." *IEEE TSE* 39(6):869–891. OA-yes (author-hosted).

### Cluster A4 — Model checking & formal verification (Branch A · COMPREHENSIVENESS)
- **★A¶ Zhang, P., Muccini, H. & Li, B. (2010).** "A Classification and Comparison of Model Checking Software Architecture Techniques." *JSS* 83(5):723–744. OA-no.
- **A Garlan, D., Allen, R. & Ockerbloom, J. (1995).** "Architectural Mismatch: Why Reuse Is So Hard." *IEEE Software* 12(6):17–26. OA-yes.
- **A Garlan, D., Allen, R. & Ockerbloom, J. (2009).** "Architectural Mismatch: Why Reuse Is Still So Hard." *IEEE Software* 26(4):66–69. OA-yes (CMU-hosted).

### Cluster A5 — Dynamic / self-adaptive architectures (Branch A · COMPREHENSIVENESS)
- **★A Oreizy, P., Medvidovic, N. & Taylor, R.N. (1998).** "Architecture-Based Runtime Software Evolution." *Proc. ICSE '98*, pp. 177–186. OA-yes.
- **A Garlan, D., Cheng, S.-W., Huang, A.-C., Schmerl, B. & Steenkiste, P. (2004).** "Rainbow: Architecture-Based Self-Adaptation with Reusable Infrastructure." *IEEE Computer* 37(10):46–54. OA-yes.
- **A Kramer, J. & Magee, J. (2007).** "Self-Managed Systems: an Architectural Challenge." *Proc. FOSE 2007.* OA-yes.
- **A Weyns, D. (2020).** *An Introduction to Self-Adaptive Systems: A Contemporary Software Engineering Perspective.* Wiley/IEEE. **BORDERLINE — admitted as advanced consolidation node.** OA-no.

### Cluster A6 — Architecture evolution (Branch A · COMPREHENSIVENESS)
- **★A¶ Breivold, H.P., Crnkovic, I. & Larsson, M. (2012).** "A Systematic Review of Software Architecture Evolution Research." *Information and Software Technology* 54(1):16–40. OA-no.
- **A Barnes, J.M., Garlan, D. & Schmerl, B. (2014).** "Evolution Styles: foundations and models for software architecture evolution." *Software & Systems Modeling* 13(2):649–678. OA-yes.

### Cluster A7 — Reference architectures & product lines (Branch A · COMPREHENSIVENESS)
- **★A Angelov, S., Grefen, P. & Greefhorst, D. (2012).** "A framework for analysis and design of software reference architectures." *Information and Software Technology* 54(4):417–431. OA-no.
- **A Galster, M. & Avgeriou, P. (2011).** "Empirically-grounded reference architectures: a proposal." *Proc. QoSA/ISARCS 2011.* OA-yes.
- **C Clements, P. & Northrop, L. (2001).** *Software Product Lines: Practices and Patterns.* Addison-Wesley. **BORDERLINE on the science bar** — admitted as a product‑line reference. OA-no.

### Cluster B1 — Design-process roots / design science (Branch B · CANONICAL)
- **★C Parnas, D.L. (1972).** "On the Criteria To Be Used in Decomposing Systems into Modules." *CACM* 15(12):1053–1058. OA-yes (readable via CACM).
- **C Parnas, D.L. (1974).** "On a 'Buzzword': Hierarchical Structure." *Proc. IFIP Congress 74.* OA-partial.
- **C Parnas, D.L. (1979).** "Designing Software for Ease of Extension and Contraction." *IEEE TSE* SE‑5(2):128–138. OA-partial.
- **★C Parnas, D.L. & Clements, P.C. (1986).** "A Rational Design Process: How and Why to Fake It." *IEEE TSE* SE‑12(2):251–257. OA-yes.
- **A Simon, H.A. (1996).** *The Sciences of the Artificial*, 3rd ed. MIT Press. OA-no.
- **A Rittel, H.W.J. & Webber, M.M. (1973).** "Dilemmas in a General Theory of Planning." *Policy Sciences* 4(2):155–169. OA-yes.

### Cluster B2 — Design methods & the general design model (Branch B · CANONICAL)
- **★C¶ Hofmeister, C., Kruchten, P., Nord, R.L., Obbink, H., Ran, A. & America, P. (2007).** "A General Model of Software Architecture Design Derived from Five Industrial Approaches." *JSS* 80(1):106–126. OA-partial.
- **★C Cervantes, H. & Kazman, R. (2024).** *Designing Software Architectures: A Practical Approach*, 2nd ed. Addison-Wesley (SEI Series). Published **Jun 14, 2024**; print ISBN 9780138108021, eTextbook ISBN 9780138108151. (Adds chapters on API‑centric design, deployability, cloud, and technical debt; ADD method core unchanged.) OA-no.
- **C Bosch, J. (2000).** *Design and Use of Software Architectures: Adopting and Evolving a Product-Line Approach.* Addison-Wesley. OA-no.
- **C Jansen, A. & Bosch, J. (2005).** "Software Architecture as a Set of Architectural Design Decisions." *Proc. WICSA 2005*, pp. 109–120. OA-yes.
- **A Bosch, J. & Molin, P. (1999).** "Software architecture design: evaluation and transformation." *Proc. IEEE ECBS '99.* OA-no.

### Cluster B3 — Design rationale & architectural knowledge (Branch B · COMPREHENSIVENESS)
- **★C Kunz, W. & Rittel, H.W.J. (1970).** "Issues as Elements of Information Systems." Working Paper No. 131, IURD, UC Berkeley (IBIS). OA-yes.
- **C MacLean, A., Young, R.M., Bellotti, V.M.E. & Moran, T.P. (1991).** "Questions, Options, and Criteria: Elements of Design Space Analysis" (QOC). *Human–Computer Interaction* 6(3–4):201–250. OA-no.
- **C Lee, J. & Lai, K.-Y. (1991).** "What's in Design Rationale?" (DRL). *Human–Computer Interaction* 6(3–4):251–280. OA-partial.
- **C Dutoit, A.H., McCall, R., Mistrík, I. & Paech, B. (eds.) (2006).** *Rationale Management in Software Engineering.* Springer. OA-no.
- **A Burge, J.E., Carroll, J.M., McCall, R. & Mistrík, I. (2008).** *Rationale-Based Software Engineering.* Springer. OA-no.
- **A Tang, A., Jin, Y. & Han, J. (2007).** "A rationale-based architecture model for design traceability and reasoning." *JSS* 80(6):918–934. OA-partial.
- **A Zimmermann, O., et al. (2007/2009).** Reusable architectural decision models (e.g., "Reusable Architectural Decision Models for Enterprise Application Development," QoSA 2007; "Architectural Decision Guidance Across Projects," WICSA 2015 for the extended line). OA-partial. *(Anchor paper to be finalized — see uncertainties.)*
- **★C¶ Capilla, R., Jansen, A., Tang, A., Avgeriou, P. & Babar, M.A. (2016).** "10 years of software architecture knowledge management: Practice and future." *JSS* 116:191–205. OA-yes (RUG repository).
- **A¶ Weinreich, R. & Groher, I. (2016).** "Software architecture knowledge management approaches and their support for knowledge management activities: A systematic literature review." *Information and Software Technology* 80:265–286. OA-no.
- **A Tang, A., Babar, M.A., Gorton, I. & Han, J. (2006).** "A survey of architecture design rationale." *JSS* 79(12):1792–1804. OA-yes.
- **A van Vliet, H. & Tang, A. (2016).** "Decision making in software architecture." *JSS* 117:638–644. OA-partial.

### Cluster B4 — Empirical studies of design reasoning (Branch B · COMPREHENSIVENESS)
- **★A¶ Falessi, D., Cantone, G., Kazman, R. & Kruchten, P. (2011).** "Decision-making techniques for software architecture design: A comparative survey." *ACM Computing Surveys* 43(4), Art. 33:1–28. OA-partial.
- **A Zannier, C., Chiasson, M. & Maurer, F. (2007).** "A model of design decision making based on empirical results of interviews with software designers." *Information and Software Technology* 49(6):637–653. OA-no.
- **A Tang, A., Razavian, M., et al.** Empirical studies on software design reasoning and reflection. OA-partial. *(Cluster of papers; anchor to be selected — see uncertainties.)*

### Cluster S1 — Evaluation canon (SHARED · CANONICAL)
- **★C Clements, P., Kazman, R. & Klein, M. (2001).** *Evaluating Software Architectures: Methods and Case Studies.* Addison-Wesley. OA-no.
- **★C Kazman, R., Klein, M. & Clements, P. (2000).** "ATAM: Method for Architecture Evaluation." SEI Technical Report **CMU/SEI‑2000‑TR‑004** (ESC‑TR‑2000‑004). OA-yes (SEI/DTIC ADA382629).
- **C Kazman, R., Abowd, G., Bass, L. & Webb, M. (1994).** "SAAM: A Method for Analyzing the Properties of Software Architectures." *Proc. ICSE '94.* OA-yes.
- **★C¶ Dobrica, L. & Niemelä, E. (2002).** "A Survey on Software Architecture Analysis Methods." *IEEE TSE* 28(7):638–653. OA-no.
- **A¶ Babar, M.A., Zhu, L. & Jeffery, R. (2004).** "A Framework for Classifying and Comparing Software Architecture Evaluation Methods." *Proc. Australian Software Engineering Conf. (ASWEC)*, pp. 309–318. OA-partial.
- **A Bengtsson, P., Lassing, N., Bosch, J. & van Vliet, H. (2004).** "Architecture-level modifiability analysis (ALMA)." *JSS* 69(1–2):129–147. OA-no.

### Cluster S2 — Quality-attribute models (SHARED · bridging)
- **★C ISO/IEC 25010:2023.** *Systems and software Quality Requirements and Evaluation (SQuaRE) — Product quality model.* 2nd ed., **published 2023‑11‑15**; cancels/replaces 25010:2011. Defines nine product‑quality characteristics — **Safety was added** as a characteristic, and **Usability and Portability were replaced by Interaction Capability and Flexibility** respectively; quality‑in‑use content moved to ISO/IEC 25019:2023 and overview to ISO/IEC 25002. OA-no (standard).
- **C Barbacci, M., Klein, M.H., Longstaff, T.A. & Weinstock, C.B. (1995).** "Quality Attributes." SEI Technical Report **CMU/SEI‑95‑TR‑021.** OA-yes (SEI).
- **A Klein, M. & Kazman, R. (1999).** "Attribute-Based Architectural Styles (ABAS)." SEI Technical Report **CMU/SEI‑99‑TR‑022.** OA-yes (SEI).
- **A Bachmann, F., Bass, L. & Klein, M. (2003).** "Deriving Architectural Tactics: A Step Toward Methodical Architectural Design." SEI TR **CMU/SEI‑2003‑TR‑004.** OA-yes (SEI).

### Cluster S3 — Economics & technical debt (SHARED · bridging)
- **★C Kazman, R., Asundi, J. & Klein, M. (2001).** "Quantifying the Costs and Benefits of Architectural Decisions" (CBAM). *Proc. ICSE 2001.* OA-yes. (Extended in SEI/2002 CBAM work.)
- **C Kruchten, P., Nord, R. & Ozkaya, I. (2019).** *Managing Technical Debt: Reducing Friction in Software Development.* Addison-Wesley (SEI Series), published Apr/Jun 2019; ISBN 9780135645932. OA-no.
- **A Avgeriou, P., Kruchten, P., Ozkaya, I. & Seaman, C. (2016).** "Managing Technical Debt in Software Engineering." *Dagstuhl Reports* 6(4):110–138. OA-yes (Dagstuhl).
- **A Poort, E.R. & van Vliet, H. (2012).** "RCDA: Architecting as a risk- and cost management discipline." *JSS* 85(9):1995–2013. OA-yes (Zenodo accepted version).

---

## Typed Edge List (with one-line justifications; cycles documented)

1. Perry–Wolf (1992) **prerequisite-of** Shaw–Garlan (1996) — elements/form/rationale model underlies the perspectives volume.
2. Shaw–Garlan (1996) **prerequisite-of** Taylor–Medvidovic–Dashofy (2010) — canonical textbook consolidates the perspectives.
3. Garlan–Shaw (1993) **refines** Perry–Wolf (1992) — introduces architectural styles as concrete "form."
4. Kruchten (1995) **refines** Perry–Wolf (1992) — operationalizes concerns into 4+1 views.
5. ISO/IEC/IEEE 42010:2022 **subsumes** Kruchten (1995) — standard generalizes views/viewpoints beyond 4+1.
6. Clements et al. *Views & Beyond* (2010) **applies-method-of** ISO/IEC/IEEE 42010:2022 — instantiates the viewpoint framework for documentation.
7. Emery–Hilliard (2009) **refines** ISO/IEC/IEEE 42010:2022 — formal treatment of architecture frameworks under the standard.
8. Medvidovic–Taylor (2000) **surveys** Allen–Garlan (1997), Luckham et al. (1995), Magee–Kramer (1996), Garlan–Monroe–Wile (1997), Moriconi et al. (1995) — classification framework catalogs these ADLs.
9. Allen–Garlan (1997) **formalizes** Perry–Wolf (1992) — CSP semantics formalizes "connecting elements."
10. Abowd–Allen–Garlan (1995) **formalizes** Garlan–Shaw (1993) — Z-based formal semantics for architectural styles.
11. Moriconi et al. (1995) **refines** Allen–Garlan (1997) — correctness-preserving refinement of formal architectures.
12. Oquendo (2004) **refines** Magee–Kramer (1996) — π‑calculus ADL extends Darwin's dynamic structure.
13. Malavolta et al. (2013) **critiques/feeds-back-into** Medvidovic–Taylor (2000) — industry-needs survey re‑scopes ADL research priorities. **[CYCLE 1a]**
14. Malavolta et al. (2013) **critiques/feeds-back-into** ISO/IEC/IEEE 42010 — industry findings shape the standard's ADL requirements. **[CYCLE 1b]**
15. ISO/IEC/IEEE 42010 **feeds-back-into** ADL research (Medvidovic–Taylor lineage) — closing **CYCLE 1**.
16. Zhang–Muccini–Li (2010) **surveys** Allen–Garlan (1997), Bernardo–Inverardi (2003) — classifies model-checking techniques over formal models.
17. Bernardo–Inverardi (2003) **prerequisite-of** Aldini–Bernardo–Corradini (2010) — lecture volume precedes the full PA design method.
18. Aldini–Bernardo–Corradini (2010) **applies-method-of** Allen–Garlan (1997) — PA design uses connector-formalization lineage.
19. Garlan et al. Mismatch (1995) **prerequisite-of** Garlan et al. retrospective (2009) — explicit 14‑year retrospective. **[CYCLE 2 seed]**
20. Garlan et al. (2009) **critiques/feeds-back-into** Garlan et al. (1995) — re‑evaluates whether the original problem persists. **[CYCLE 2]**
21. Oreizy–Medvidovic–Taylor (1998) **refines** Magee–Kramer (1996) — runtime evolution operationalizes dynamic structure.
22. Garlan et al. Rainbow (2004) **applies-method-of** Oreizy et al. (1998) — self-adaptation builds on architecture-based runtime evolution.
23. Kramer–Magee (2007) **complements** Rainbow (2004) — parallel self-managed-systems agenda.
24. Weyns (2020) **subsumes** Rainbow (2004), Kramer–Magee (2007) — textbook consolidates self-adaptive systems.
25. Breivold–Crnkovic–Larsson (2012) **surveys** Oreizy et al. (1998) and evolution research — systematic review.
26. Barnes–Garlan–Schmerl (2014) **refines** themes in Breivold et al. (2012) — formal evolution-path/style models.
27. Angelov–Grefen–Greefhorst (2012) **complements** Clements–Northrop (2001) — reference-architecture analysis parallels product-line practice.
28. Galster–Avgeriou (2011) **refines** Angelov et al. (2012) — empirical grounding of reference architectures.
29. Parnas (1972) **prerequisite-of** Parnas (1979) — information hiding underlies extension/contraction.
30. Parnas (1974) **complements** Parnas (1972) — hierarchical structure clarifies decomposition semantics.
31. Parnas–Clements (1986) **subsumes** Parnas (1972), Parnas (1979) — synthesizes the decomposition lineage into a process ideal.
32. Simon (1996) **prerequisite-of** Parnas–Clements (1986) — sciences-of-the-artificial framing underlies "faking" a rational process.
33. Rittel–Webber (1973) **complements** Kunz–Rittel (1970) — wicked-problems theory motivates issue-based rationale.
34. Kunz–Rittel (1970) **prerequisite-of** MacLean et al. QOC (1991) — IBIS is the ancestor of QOC design-space analysis.
35. Kunz–Rittel (1970) **prerequisite-of** Lee–Lai DRL (1991) — IBIS ancestor of DRL.
36. MacLean et al. (1991) **complements** Lee–Lai (1991) — two rationale representations, same special issue.
37. Dutoit et al. (2006) **subsumes** MacLean et al. (1991), Lee–Lai (1991) — rationale-management volume consolidates rationale models.
38. Burge et al. (2008) **applies-method-of** Dutoit et al. (2006) — rationale-based SE operationalizes rationale management.
39. Jansen–Bosch (2005) **refines** Perry–Wolf (1992) rationale component — recasts architecture as a set of decisions. **[CYCLE 3 seed]**
40. Tang–Jin–Han (2007) **refines** Jansen–Bosch (2005) — adds traceability/reasoning to decisions.
41. Tang–Jin–Han (2007) **applies-method-of** Lee–Lai (1991) — decision-rationale model reuses DRL-style capture. **[CYCLE 3]**
42. Capilla et al. (2016) **surveys** Jansen–Bosch (2005), Tang–Jin–Han (2007), Zimmermann et al. (2007) — 10‑year AKM retrospective.
43. Capilla et al. (2016) **feeds-back-into** Jansen–Bosch (2005) — retrospective redirects AK research. **[CYCLE 3 closure]**
44. Weinreich–Groher (2016) **surveys** AKM approaches (Capilla lineage) — SLR of AK management activities.
45. van Vliet–Tang (2016) **complements** Falessi et al. (2011) — decision-making editorial framing complements the technique survey.
46. Falessi et al. (2011) **surveys** CBAM (2001) and ATAM (2000) as decision techniques.
47. Zannier–Chiasson–Maurer (2007) **critiques/feeds-back-into** Parnas–Clements (1986) — empirical evidence that real design decision-making is naturalistic, not rational-faked.
48. Hofmeister et al. (2007) **subsumes** ADD (Bass–Clements–Kazman), 4+1 (Kruchten 1995), Applied SA (Hofmeister–Nord–Soni 2000) — general model derived from five methods.
49. Cervantes–Kazman (2024) **refines** Hofmeister et al. (2007) — ADD 3.0 operationalizes the analysis/synthesis/evaluation loop.
50. Cervantes–Kazman (2024) **applies-method-of** ATAM (2000) — ADD uses quality-attribute scenarios/evaluation as steps. **[CYCLE 4 seed]**
51. Bass–Clements–Kazman (2021) **prerequisite-of** Cervantes–Kazman (2024) — SAIP supplies quality-attribute scenarios and tactics.
52. Clements–Kazman–Klein (2001) **evaluates** architectures produced under Bass–Clements–Kazman (2021) (reciprocal **is-evaluated-by**) — evaluation book operationalizes ATAM on SAIP artifacts.
53. ATAM TR (2000) **refines** SAAM (1994) — extends single-attribute SAAM to multi-attribute tradeoffs.
54. ATAM (2000) **applies-method-of** Barbacci et al. Quality Attributes (1995) — uses quality-attribute characterizations.
55. Bachmann–Bass–Klein (2003) **refines** Klein–Kazman ABAS (1999) — tactics derive from attribute-based styles.
56. Cervantes–Kazman ADD (2024) **applies-method-of** Bachmann–Bass–Klein (2003) tactics; tactic/scenario refinement **feeds-back-into** ATAM. **[CYCLE 4 closure]**
57. Dobrica–Niemelä (2002) **surveys** SAAM (1994), ATAM (2000), ALMA (2004) — evaluation-method survey.
58. Babar–Zhu–Jeffery (2004) **critiques** Dobrica–Niemelä (2002) — proposes new classification criteria for evaluation methods.
59. Bengtsson et al. ALMA (2004) **applies-method-of** SAAM (1994) — scenario-based modifiability analysis specializes scenario evaluation.
60. CBAM (Kazman–Asundi–Klein 2001) **refines** ATAM (2000) — adds an economic cost‑benefit layer atop ATAM tradeoffs.
61. Poort–van Vliet (2012) **complements** CBAM (2001) — risk/cost-driven architecting as an economics discipline.
62. Kruchten–Nord–Ozkaya (2019) **refines** Avgeriou et al. Dagstuhl (2016) — book consolidates the technical-debt agenda.
63. Avgeriou et al. (2016) **complements** Poort–van Vliet (2012) — debt economics complements risk/cost architecting.
64. ISO/IEC 25010:2023 **subsumes** Barbacci et al. (1995) — standardized quality model generalizes the SEI quality-attribute taxonomy.
65. Bass–Clements–Kazman (2021) **applies-method-of** ISO/IEC 25010:2023 — quality-attribute scenarios reference the standardized quality model.
66. Medvidovic et al. UML (2002) **complements** Medvidovic–Taylor (2000) — assesses UML as an architecture-modeling notation against ADL criteria.
67. Rozanski–Woods (2011) **applies-method-of** ISO/IEC/IEEE 42010 — viewpoint/perspective catalog instantiates the standard.
68. Bosch (2000) **prerequisite-of** Jansen–Bosch (2005) — design-and-use framing precedes the decisions view.
69. Bosch–Molin (1999) **prerequisite-of** Bengtsson et al. ALMA (2004) — evaluation-and-transformation precedes modifiability analysis.
70. Shaw (2001) **complements** Garlan (2014) — reflective state-of-field companion pieces bridging both branches.

**Documented genuine cycles (required):**
- **CYCLE 1 (Branch A):** Medvidovic–Taylor ADL classification → ISO/IEC/IEEE 42010 → Malavolta et al. industry‑needs → back to ADL research (edges 8 → 14/15 → 13 → 8).
- **CYCLE 2 (Branch A):** Architectural Mismatch 1995 ↔ 2009 retrospective (edges 19 ↔ 20).
- **CYCLE 3 (Branch B):** Design‑rationale models (DRL/IBIS) → decision‑centric architecture (Jansen–Bosch → Tang et al.) → refined rationale capture → AKM retrospective feeds back (edges 39 → 40 → 41 → 42 → 43 → 39).
- **CYCLE 4 (Shared):** ADD design method → quality‑attribute scenarios/ATAM evaluation → refined tactics/scenarios → back into ADD (edges 50 → 56).

---

## Core / Advanced / Target / Survey Designations
- **Target/canonical anchors (★, one or more per cluster):** Perry–Wolf 1992; Shaw–Garlan 1996; Taylor–Medvidovic–Dashofy 2010; ISO/IEC/IEEE 42010:2022; Documenting Software Architectures 2010; Medvidovic–Taylor 2000; Allen–Garlan 1997; Zhang et al. 2010; Oreizy et al. 1998; Breivold et al. 2012; Angelov et al. 2012; Parnas 1972; Parnas–Clements 1986; Hofmeister et al. 2007; Cervantes–Kazman 2024; Kunz–Rittel 1970; Capilla et al. 2016; Falessi et al. 2011; Clements–Kazman–Klein 2001; ATAM TR 2000; Dobrica–Niemelä 2002; ISO/IEC 25010:2023; CBAM 2001.
- **Survey/tutorial first-class nodes (¶):** Medvidovic–Taylor 2000; Malavolta et al. 2013; Zhang et al. 2010; Breivold et al. 2012; Hofmeister et al. 2007; Capilla et al. 2016; Weinreich–Groher 2016; Falessi et al. 2011; Dobrica–Niemelä 2002; Babar–Zhu–Jeffery 2004; Shaw 2001; Garlan 2014.
- **Core tier:** the CANONICAL-cluster books/papers everyone must read (A1, A2, B1, B2, S1, plus the quality-model/economics core in S2/S3).
- **Advanced tier:** formal ADLs, model checking, self-adaptive, evolution, reference architectures, economics/debt, and the empirical-reasoning studies.

---

## Recommendations (staged reading + build guidance)

**Stage 1 — Establish the shared vocabulary (read first, both branches).** Perry–Wolf 1992 → Garlan–Shaw 1993 → Shaw–Garlan 1996 → Kruchten 1995 → ISO/IEC/IEEE 42010:2022. These fix the elements/form/rationale ontology and the views/viewpoints framing that every later node presupposes. *Threshold to proceed:* you can articulate the difference between an architecture and an architecture description, and between a view and a viewpoint.

**Stage 2 — Split by branch.**
- *Branch A (artifact):* Taylor–Medvidovic–Dashofy 2010 (textbook spine) → Medvidovic–Taylor 2000 (ADL map) → then depth via Allen–Garlan 1997, Abowd–Allen–Garlan 1995, Zhang et al. 2010.
- *Branch B (process):* Parnas 1972 → Parnas–Clements 1986 → Hofmeister et al. 2007 → Cervantes–Kazman 2024 (ADD 3.0). Read Simon 1996 and Rittel–Webber 1973 as the design-science backdrop.

**Stage 3 — Bridge through evaluation and quality (shared).** Clements–Kazman–Klein 2001 + ATAM TR 2000 + Dobrica–Niemelä 2002 (survey), anchored by Barbacci et al. 1995 and ISO/IEC 25010:2023. This is where the two branches meet: evaluation both assesses artifacts (A) and drives design (B).

**Stage 4 — Advanced specialization by interest.** Choose among A4 (model checking), A5 (self-adaptive), A6 (evolution), A7 (reference architectures/product lines), B3 (rationale/AKM), B4 (empirical reasoning), and S3 (economics/technical debt). Each is entered via its ¶ survey node first.

**For the HTML graph build:** render the two branches as color bands with the shared infrastructure as a central spine; tint the ★ target anchors with the purple-border treatment; mark ¶ survey nodes with a distinct glyph; draw the four cycles with a visually distinct (e.g., dashed, red) edge style so the feedback loops are legible. Use the OA flags to add a "free PDF" badge on ~30 of the ~60 nodes.

**Benchmarks that would change these recommendations:** (a) if a verified 2nd edition of Taylor–Medvidovic–Dashofy surfaces, promote it as the A1 spine and re‑date edge 2; (b) if the reviewer decides Rozanski–Woods, Clements–Northrop, or Weyns fail the strict science bar, demote them to an appendix rather than graph nodes; (c) if the graph is meant for practitioners rather than researchers, elevate S1/S2 to Stage‑1 status.

---

## Caveats & Verification Uncertainties (flag in the final document)
- **Taylor–Medvidovic–Dashofy edition:** Verified that **only one edition exists** (Wiley, ©2010, some listings 2009). The task's hypothesis of a ~2010 2nd edition/successor is **not supported** by ACM DL, Wiley's product page, or bookseller records.
- **Borderline "science bar" admissions (reviewer decision needed):** *Rozanski–Woods 2011* (viewpoints/perspectives — practitioner-leaning but structured), *Clements–Northrop 2001* (product lines — practices/patterns framing), and *Weyns 2020* (self-adaptive textbook). All three are admitted here as reference/consolidation nodes, **not** as formal-theory nodes; each could be moved to an appendix if strictness is prioritized.
- **π‑ADL (Oquendo):** correct citation is *ACM SIGSOFT SEN* **29(3):1–14 (2004)**; reject the stray "28(8)" citations seen in some secondary sources.
- **RCDA (Poort–van Vliet):** correct is *JSS* **85(9):1995–2013 (2012)**; one institutional portal prints "vol. 95," which is a typo.
- **Acme (Garlan–Monroe–Wile):** CASCON '97, pp. **169–183** (reprinted 2010, pp. 159–173); some indexes show a single-page stub — the range 169–183 is authoritative.
- **Zimmermann reusable architectural decision models:** this is a *line* of papers (QoSA 2007; SHARK/ICSE workshops; WICSA 2015) rather than one canonical node — pin the single anchor before rendering.
- **Tang/Razavian empirical design-reasoning:** a cluster of empirical-reasoning/reflection papers rather than one node — select and cite the specific anchor paper (e.g., the controlled reasoning/reflection studies) before finalizing node B4‑3.
- **CBAM:** the ICSE 2001 paper is the canonical anchor; a fuller SEI/IEEE Software 2002 treatment exists and may be preferred as the "year of last publication" node if the build wants the most complete version.
- **Open-access "partial" flags** mean a repository or ResearchGate copy exists but no confirmed rights‑clean publisher/author PDF was located; treat these as "likely findable free" rather than officially open. SEI technical reports (ATAM TR 2000, Barbacci 1995, ABAS 1999, Bachmann 2003) and the Dagstuhl technical-debt report are genuinely, officially free.
- **Standards are paywalled** (42010:2022, 25010:2023); only their scope/abstract text is openly readable.
- **Edge directionality for cycles** is deliberate: the *feeds-back-into*/*critiques* edges are what make the graph cyclic rather than a DAG; if a downstream tool requires acyclicity, these four edges are the ones to cut, but doing so loses the intellectual feedback the corpus is designed to represent.