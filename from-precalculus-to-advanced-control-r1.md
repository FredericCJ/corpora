# Canonical Self-Study Literature for a Seven-Field Control-Theory DAG Expansion

## TL;DR
- **All seven target fields have a clear canonical "core" text and a distinct "advanced/monograph" tier**, and several of the single most important works are legally free from author/publisher sites: Rawlings-Mayne-Diehl MPC (UCSB), Boyd-El Ghaoui LMIs (SIAM/Berkeley), Ioannou-Sun Robust Adaptive Control (USC), Skogestad-Postlethwaite (NTNU), Åström-Murray Feedback Systems (fbsbook.org), Boyd-Vandenberghe Convex Optimization (Stanford), LaValle Planning Algorithms (lavalle.pl/UIUC), and Bertsekas RL & Optimal Control / Abstract DP (ASU/MIT).
- **The dominant prerequisite chain is: Khalil-level Lyapunov/nonlinear systems + Hespanha-level linear state-space theory + Boyd-Vandenberghe convex optimization.** Every field except pure trajectory generation assumes at least Lyapunov stability; MPC, robust, and NCS additionally assume convex optimization and LMIs; adaptive and sliding-mode lean hardest on Lyapunov/Barbalat; robust control assumes functional analysis (Hardy spaces) that the existing Luenberger node supports.
- **A few widely cited works are poorly suited to first-pass self-study and should be placed as reference-only nodes**, notably Utkin (1992), Narendra-Annaswamy (1989), and Chen-Francis (1995); better self-study entry points exist for each (Shtessel et al.; Ioannou-Sun; Åström-Wittenmark) and are named below.

## Key Findings

**Field-by-field canonical selections (core → advanced):**
- **MPC:** Core = Rawlings-Mayne-Diehl (2nd ed., free PDF) + Borrelli-Bemporad-Morari (author PDF). Advanced = Grüne-Pannek, Kouvaritakis-Cannon, plus the Mayne-Rawlings-Rao-Scokaert 2000 *Automatica* survey as the definitive stability paper.
- **Robust control:** Core = Skogestad-Postlethwaite (2nd ed., free PDF) + Zhou-Doyle "Essentials." Advanced = Zhou-Doyle-Glover (1996), Dullerud-Paganini, Boyd-El Ghaoui LMIs (free PDF), Liberzon switching. Doyle-Francis-Tannenbaum (Dover) is the gentlest entry.
- **Adaptive control:** Core = Ioannou-Sun (free PDF) + Åström-Wittenmark (Dover). Advanced = Krstic et al. backstepping, Hovakimyan-Cao L1, Lavretsky-Wise aerospace (2nd ed. 2024).
- **Sliding mode:** Core = Shtessel-Edwards-Fridman-Levant (2014). Advanced = Utkin (1992), Edwards-Spurgeon, Levant's IJC papers.
- **Advanced digital control:** Core = Åström-Wittenmark Computer-Controlled Systems (Dover). Advanced = Chen-Francis sampled-data, Zaccarian-Teel anti-windup, Bristow et al. ILC survey.
- **Networked control:** Core = Hespanha-Naghshtabrizi-Xu 2007 survey (free PDF) + Fridman time-delay text. Advanced = Costa et al. MJLS, Sinopoli/Schenato lossy-network papers, Tabuada/Heemels event-triggered.
- **Trajectory generation:** Core = LaValle Planning Algorithms (free PDF) + Kelly 2017 SIAM Review tutorial. Advanced = Betts (3rd ed. 2020), Biagiotti-Melchiorri, Garone reference-governor survey.

## Details

### Shared prerequisite / infrastructure nodes (verify first — these feed multiple fields)

- **Boyd & Vandenberghe, *Convex Optimization*, Cambridge University Press, 2004.** Official free PDF at stanford.edu/~boyd/cvxbook/ (publisher-sanctioned). Prerequisite: linear algebra (Lay/Axler level), multivariable calculus. The single most-used shared node — feeds MPC, robust (LMIs), trajectory optimization, and networked control. Assumes no prior optimization.
- **Boyd, El Ghaoui, Feron & Balakrishnan, *Linear Matrix Inequalities in System and Control Theory*, SIAM Studies in Applied Mathematics vol. 15, 1994.** Free PDF held by SIAM and hosted at people.eecs.berkeley.edu/~elghaoui/pubs_lmi_book.html. Prerequisite: linear systems state-space theory (Hespanha) + convex optimization basics. Terse monograph, not a course text; best as a reference node feeding robust control and NCS.
- **Nocedal & Wright, *Numerical Optimization*, 2nd ed., Springer Series in Operations Research and Financial Engineering, 2006** (ISBN 978-0-387-30303-1). No official free PDF. Prerequisite: multivariable calculus, linear algebra. Core numerical-optimization node feeding MPC and trajectory optimization.
- **Åström & Murray, *Feedback Systems: An Introduction for Scientists and Engineers*, 2nd ed., Princeton University Press, published February 2, 2021 (ISBN 978-0-691-19398-4).** Free electronic edition at fbsbook.org (copyedited PDF dated 24 Jul 2020; Python figure sources updated 16 Nov 2024). The license is not formally Creative Commons but publisher-permitted: per FBSwiki, "Copyright in this book is held by Princeton University Press, who have kindly agreed to allow us to keep the book available on the web." Prerequisite: ODEs + linear algebra only; an accessible bridge node before the graduate texts.
- **Bertsekas, *Dynamic Programming and Optimal Control*, Athena Scientific — Vol. I 4th ed. 2017; Vol. II 4th ed. 2012.** No free PDF of the main two volumes (sample chapters/slides only). **Bertsekas, *Reinforcement Learning and Optimal Control*, Athena Scientific, 2019.** **Bertsekas, *Abstract Dynamic Programming*, 2nd ed., Athena Scientific, 2018 — free PDF from the author's site.** Prerequisite: probability, analysis maturity. DP/RL node feeding MPC and stochastic estimation.
- **Goodwin & Sin, *Adaptive Filtering, Prediction and Control*, Dover reprint 2009 (orig. Prentice Hall 1984).** Feeds adaptive control and digital control; Dover reprint is inexpensive but not free.

### FIELD 1 — Model Predictive Control

**CORE:**
- **Rawlings, Mayne & Diehl, *Model Predictive Control: Theory, Computation, and Design*, 2nd ed., Nob Hill Publishing, Santa Barbara.** Precise printing history from the UCSB front matter: 1st printing October 2018; the February 2019 second (electronic-only) printing mainly corrected typographical errors; the third printing was produced as a paperback and made available electronically in October 2020, in which "Chapter 4 was revised significantly." The 2nd edition was reissued as "Nob Hill Publishing, LLC, 2nd edition, 2024" (XLVI + 623 pp., WorldCat OCLC 1146543936). Official free PDF from Rawlings's UCSB site (sites.engineering.ucsb.edu/~jbraw/mpc/). The definitive graduate MPC text. Prerequisites: linear systems state-space (Hespanha), Lyapunov stability (Khalil ch. 4), convex optimization (Boyd-Vandenberghe). Chapter 1 is self-contained for those without a prior systems course.
- **Borrelli, Bemporad & Morari, *Predictive Control for Linear and Hybrid Systems*, Cambridge University Press, 2017** (ISBN 9781107016880). A near-complete author PDF is hosted at Bemporad's IMT Lucca site (cse.lab.imtlucca.it/~bemporad/). Core for explicit MPC, multiparametric programming, and hybrid systems. Prerequisites: convex optimization, linear systems.

**ADVANCED:**
- **Grüne & Pannek, *Nonlinear Model Predictive Control: Theory and Algorithms*, 2nd ed., Communications and Control Engineering, Springer, 2017.** Advanced; rigorous treatment of NMPC stability without terminal constraints. Prerequisite: Khalil-level nonlinear systems + MPC basics.
- **Kouvaritakis & Cannon, *Model Predictive Control: Classical, Robust and Stochastic*, Springer, 2016.** Advanced; the standard entry to tube-based robust MPC and stochastic MPC. Prerequisite: core MPC + probability.
- **Maciejowski, *Predictive Control with Constraints*, Prentice Hall, 2002.** An applied/accessible bridge; lighter theory, good for a first MPC exposure but superseded by Rawlings et al. for theory.
- **Camacho & Bordons, *Model Predictive Control*, 2nd ed., Springer, 2004** (Advanced Textbooks in Control and Signal Processing). Applied/industrial emphasis; classify as supplementary.
- **Definitive survey paper:** Mayne, Rawlings, Rao & Scokaert, "Constrained model predictive control: Stability and optimality," *Automatica*, vol. 36, no. 6, pp. 789–814, 2000 (DOI 10.1016/S0005-1098(99)00214-9). The canonical stability/optimality reference. Robust/tube MPC key paper: Mayne, Seron & Raković, "Robust model predictive control of constrained linear systems with bounded disturbances," *Automatica* 41(2):219–224, 2005.

### FIELD 2 — Robust Control

**CORE:**
- **Skogestad & Postlethwaite, *Multivariable Feedback Control: Analysis and Design*, 2nd ed., Wiley, 2005 (reprinted Feb 2007 with corrections).** Free full-book PDF from Skogestad's NTNU site (folk.ntnu.no/skoge/book/). The most teachable graduate robust-control text; new 2nd-ed. chapter on LMIs. Prerequisites: classical control + linear systems state-space; multivariable linear algebra (SVD).
- **Zhou & Doyle, *Essentials of Robust Control*, Prentice Hall, 1998.** The abridged, more teachable companion to the 1996 monograph. Core-level; prerequisite: linear systems, some functional analysis.

**ADVANCED:**
- **Zhou, Doyle & Glover, *Robust and Optimal Control*, Prentice Hall, 1996** (596 pp., ISBN 0-13-456567-3). The comprehensive state-space H-infinity monograph; errata hosted at ece.lsu.edu/kemin/robust.htm. Advanced; heavier than "Essentials." Prerequisite: functional analysis (Hardy spaces), linear systems.
- **Dullerud & Paganini, *A Course in Robust Control Theory: A Convex Approach*, Springer (Texts in Applied Mathematics 36), 2000.** Advanced; LMI/convex route to robust control. Prerequisite: LMIs (Boyd et al.), functional analysis.
- **Doyle, Francis & Tannenbaum, *Feedback Control Theory*, Macmillan 1992; Dover reprint 2009.** The gentlest theoretical entry to H-infinity; long circulated as an author PDF and now inexpensive via Dover. Best first robust-control node.
- **Francis, *A Course in H-infinity Control Theory*, Lecture Notes in Control and Information Sciences vol. 88, Springer, 1987.** Historic advanced reference.
- **μ-synthesis survey:** Packard & Doyle, "The complex structured singular value," *Automatica*, vol. 29, no. 1, pp. 71–109, 1993 — the canonical structured-singular-value reference.
- **Switched systems / dwell-time (adjacent to robust):** **Liberzon, *Switching in Systems and Control*, Systems & Control: Foundations & Applications, Birkhäuser, 2003.** Requires only basic linear systems theory; the standard switched-systems monograph. Complement with the Lin-Antsaklis stability survey (IEEE, 2009) as a paper node.
- **Green & Limebeer, *Linear Robust Control*, Prentice Hall 1995; Dover reprint 2012.** Advanced reference-level.

### FIELD 3 — Adaptive Control

**CORE:**
- **Ioannou & Sun, *Robust Adaptive Control*, Prentice Hall, 1996; Dover reprint 2012** (ISBN 9780486498171). Official free PDF from Ioannou's USC site (viterbi-web.usc.edu/~ioannou/Robust_Adaptive_Control.htm). The most comprehensive continuous-time adaptive-control text; tutorial in style. Prerequisites: Lyapunov stability and Barbalat's lemma (Khalil ch. 4, 8), linear systems.
- **Åström & Wittenmark, *Adaptive Control*, 2nd ed., Addison-Wesley 1995; Dover reprint 2008.** Core; broad and readable, strong on self-tuning regulators and MRAC. Prerequisite: digital control basics, linear systems.

**ADVANCED:**
- **Krstic, Kanellakopoulos & Kokotovic, *Nonlinear and Adaptive Control Design*, Wiley-Interscience, 1995** (ISBN 0-471-12732-9). The canonical backstepping / tuning-functions monograph. Advanced; prerequisite: Khalil-level nonlinear systems.
- **Hovakimyan & Cao, *L1 Adaptive Control Theory: Guaranteed Robustness with Fast Adaptation*, Advances in Design and Control vol. 21, SIAM, 2010.** Advanced; decouples adaptation from robustness. Prerequisite: MRAC background, linear systems, Lyapunov.
- **Lavretsky & Wise, *Robust and Adaptive Control: With Aerospace Applications*, Springer (Advanced Textbooks in Control and Signal Processing).** 1st ed. 2013 (ISBN 978-1-4471-4395-6, XVII+454 pp.); **2nd ed. 2024** (hardcover ISBN 978-3-031-38313-7, published 21 February 2024; eBook ISBN 978-3-031-38314-4; softcover ISBN 978-3-031-38316-8, February 2025; DOI 10.1007/978-3-031-38314-4). Applied/aerospace advanced text; strong worked MRAC designs. Prerequisite: linear systems, Lyapunov.
- **Sastry & Bodson, *Adaptive Control: Stability, Convergence, and Robustness*, Prentice Hall 1989; Dover reprint 2011.** Advanced; rigorous on convergence/persistency-of-excitation. A free PDF has circulated (Sastry's Berkeley site historically hosted it). Prerequisite: real analysis maturity.
- **Narendra & Annaswamy, *Stable Adaptive Systems*, Prentice Hall 1989; Dover reprint 2005.** Classic but dense; **flag as reference-only for self-study** — Ioannou-Sun or Åström-Wittenmark are better first passes.

### FIELD 4 — Sliding Mode Control

**Entry points already in the graph:** Slotine-Li (1991) ch. 7 and Khalil *Nonlinear Systems* (3rd ed. 2002) ch. 14 are the natural prerequisites; a reader should complete Khalil-level Lyapunov theory before this field.

**CORE:**
- **Shtessel, Edwards, Fridman & Levant, *Sliding Mode Control and Observation*, Control Engineering series, Birkhäuser/Springer New York, 2014** (356 pp., ISBN 978-0-8176-4892-3; DOI 10.1007/978-0-8176-4893-0). The definitive modern textbook, spanning classical to higher-order SMC and observers; reasonably self-contained. Prerequisite: Khalil-level nonlinear systems, Lyapunov.

**ADVANCED:**
- **Utkin, *Sliding Modes in Control and Optimization*, Communications and Control Engineering, Springer, 1992.** Foundational monograph (Filippov solutions, equivalent control); **flag as advanced reference, not first self-study** — dated notation and terse.
- **Edwards & Spurgeon, *Sliding Mode Control: Theory and Applications*, Taylor & Francis, 1998.** Advanced; strong on output-feedback SMC and observers.
- **Utkin, Guldner & Shi, *Sliding Mode Control in Electro-Mechanical Systems*, 2nd ed., CRC Press, 2009** (Automation and Control Engineering). Applied electromechanical node; good for motor/power applications.
- **Levant's higher-order SMC papers:** Levant, "Sliding order and sliding accuracy in sliding mode control," *International Journal of Control*, vol. 58, no. 6, pp. 1247–1263, 1993; and Levant, "Higher-order sliding modes, differentiation and output-feedback control," *IJC*, 2003. Canonical paper nodes for the super-twisting/HOSM branch.

### FIELD 5 — Advanced Digital Control

**CORE:**
- **Åström & Wittenmark, *Computer-Controlled Systems: Theory and Design*, 3rd ed., Prentice Hall 1997; Dover reprint 2011** (ISBN 9780486486130, 576 pp.). The standard graduate sampled-data/digital-control text. Prerequisites: classical control, linear systems, z-transforms.

**ADVANCED:**
- **Chen & Francis, *Optimal Sampled-Data Control Systems*, Communications and Control Engineering, Springer, 1995** (ISBN 978-1-4471-3039-0). The definitive H2/H-infinity sampled-data monograph. **No official free PDF.** Advanced; prerequisite: robust control (Zhou et al.), functional analysis. **Flag: rigorous but demanding — a reference node, not a first digital-control course.**
- **Middleton & Goodwin, *Digital Control and Estimation: A Unified Approach*, Prentice Hall, 1990** (ISBN 0-13-211665-0). Advanced; delta-operator unified continuous/discrete treatment.
- **Goodwin, Graebe & Salgado, *Control System Design*, Prentice Hall, 2001** (ISBN 0-13-958653-9). Broad graduate design text; a full-text PDF is hosted on a UTFSM (Chile) course server (informally hosted, not a formal publisher OA release).
- **Landau & Zito, *Digital Control Systems: Design, Identification and Implementation*, Communications and Control Engineering, Springer, 2006** (ISBN 978-1-84628-055-9). Advanced; strong on identification-for-control.
- **Anti-windup:** **Zaccarian & Teel, *Modern Anti-windup Synthesis: Control Augmentation for Actuator Saturation*, Princeton Series in Applied Mathematics, Princeton University Press, 2011** (ISBN 978-0-691-14732-1). Advanced LMI-based anti-windup monograph. Prerequisite: LMIs, linear systems. (Note a publisher front-matter "Copyright © 2005" appears on some excerpts, but the actual publication year is 2011.)
- **Iterative Learning Control:** Bristow, Tharayil & Alleyne, "A survey of iterative learning control: a learning-based method for high-performance tracking control," *IEEE Control Systems Magazine*, vol. 26, no. 3, pp. 96–114, June 2006 (DOI 10.1109/MCS.2006.1636313) — the standard ILC survey/entry point. Complement with Moore, *Iterative Learning Control for Deterministic Systems* (Springer, 1993).
- **Quantized/networked-adjacent control:** Brockett-Liberzon and Nešić survey papers are the canonical paper nodes (bridge to Field 6).

### FIELD 6 — Networked Control Systems

This field is survey- and monograph-driven; the core "reading path" is built from surveys, with monographs as advanced nodes.

**CORE reading path (surveys/tutorials):**
- **Hespanha, Naghshtabrizi & Xu, "A Survey of Recent Results in Networked Control Systems," *Proceedings of the IEEE*, vol. 95, no. 1, pp. 138–162, Jan. 2007** (DOI 10.1109/JPROC.2006.887288). The canonical NCS survey and best single entry point; author PDF widely hosted. (Note: some citations erroneously give "IEEE TAC" — it is *Proceedings of the IEEE*.)
- **Zhang, Branicky & Phillips, "Stability of networked control systems," *IEEE Control Systems Magazine*, vol. 21, no. 1, pp. 84–99, Feb. 2001** (DOI 10.1109/37.898794). Foundational stability-under-delay/dropout tutorial.
- **Heemels, Johansson & Tabuada, "An introduction to event-triggered and self-triggered control," *Proc. 51st IEEE CDC*, pp. 3270–3285, 2012** (DOI 10.1109/CDC.2012.6425820). Free author PDF at heemels.tue.nl. The event-triggered-control tutorial entry.
- **Schenato, Sinopoli, Franceschetti, Poolla & Sastry, "Foundations of control and estimation over lossy networks," *Proceedings of the IEEE*, vol. 95, no. 1, pp. 163–187, Jan. 2007** (DOI 10.1109/JPROC.2006.887306). Free author PDF at dei.unipd.it/~schenato. Core estimation-over-networks node.

**ADVANCED (monographs and key papers):**
- **Fridman, *Introduction to Time-Delay Systems: Analysis and Control*, Systems & Control: Foundations & Applications, Birkhäuser, 2014** (ISBN 978-3-319-09392-5; DOI 10.1007/978-3-319-09393-2). The teachable time-delay-systems text; strong Lyapunov-Krasovskii/LMI methods that underlie NCS delay analysis. Prerequisite: linear systems, LMIs.
- **Michiels & Niculescu, *Stability, Control, and Computation for Time-Delay Systems: An Eigenvalue-Based Approach*, 2nd ed., Advances in Design and Control, SIAM, 2014** (ISBN 978-1-611973-62-4). Advanced eigenvalue-based companion.
- **Krstic, *Delay Compensation for Nonlinear, Adaptive, and PDE Systems*, Systems & Control: Foundations & Applications, Birkhäuser, 2009** (ISBN 978-0-8176-4876-3; DOI 10.1007/978-0-8176-4877-0). Advanced predictor-feedback monograph. Prerequisite: nonlinear + PDE backstepping.
- **Costa, Fragoso & Marques, *Discrete-Time Markov Jump Linear Systems*, Probability and Its Applications, Springer, 2005** (ISBN 1-85233-761-3; DOI 10.1007/b138575). The definitive MJLS monograph (models packet-dropout regimes). Prerequisite: probability, linear systems.
- **Bemporad, Heemels & Johansson (eds.), *Networked Control Systems*, Lecture Notes in Control and Information Sciences vol. 406, Springer, 2010** (ISBN 978-0-85729-032-8; DOI 10.1007/978-0-85729-033-5). Edited advanced survey volume.
- **Key papers:** Sinopoli, Schenato, Franceschetti, Poolla, Jordan & Sastry, "Kalman filtering with intermittent observations," *IEEE TAC*, vol. 49, no. 9, pp. 1453–1464, 2004 (DOI 10.1109/TAC.2004.834121); Tabuada, "Event-triggered real-time scheduling of stabilizing control tasks," *IEEE TAC*, vol. 52, no. 9, pp. 1680–1685, 2007 (DOI 10.1109/TAC.2007.904277).
- **Teleoperation (applied node):** Hokayem & Spong, "Bilateral teleoperation: An historical survey," *Automatica*, vol. 42, no. 12, pp. 2035–2057, 2006 (DOI 10.1016/j.automatica.2006.06.027).
- **Real-time systems foundation:** Kopetz, *Real-Time Systems: Design Principles for Distributed Embedded Applications*, 2nd ed., Springer, 2011 (ISBN 978-1-4419-8236-0). Supporting node for time-triggered scheduling.

### FIELD 7 — Trajectory Generation and Reference Management

**CORE:**
- **LaValle, *Planning Algorithms*, Cambridge University Press, 2006** (print edition ISBN 978-0521862059, published May 29, 2006; ~842–844 pp. depending on source). Official free full text at lavalle.pl/planning/ and msl.cs.uiuc.edu/planning/ ("Copyright Steven M. LaValle 2006, Available for downloading at http://planning.cs.uiuc.edu/, Published by Cambridge University Press"). The canonical motion-planning text (RRTs, PRMs, kinodynamic planning). Prerequisite: algorithms/data structures, basic dynamics; no heavy control theory needed.
- **Kelly, "An Introduction to Trajectory Optimization: How to Do Your Own Direct Collocation," *SIAM Review*, vol. 59, no. 4, pp. 849–904, 2017** (DOI 10.1137/16M1062569). The definitive tutorial entry to direct-collocation trajectory optimization; freely available via SIAM. Prerequisite: nonlinear programming basics, ODEs.

**ADVANCED:**
- **Betts, *Practical Methods for Optimal Control Using Nonlinear Programming*, 3rd ed., Advances in Design and Control, SIAM, 2020** (DOI 10.1137/1.9781611976199; the 2nd ed., 2010, is titled *...Optimal Control and Estimation...*). The definitive direct-transcription reference. Prerequisite: nonlinear programming (Nocedal-Wright), ODE/DAE numerics.
- **Biagiotti & Melchiorri, *Trajectory Planning for Automatic Machines and Robots*, Springer, 2008.** Core-to-advanced for spline/polynomial and jerk-limited trajectory generation in robotics/machining. Prerequisite: basic kinematics, splines.
- **Reference/command governors:** Garone, Di Cairano & Kolmanovsky, "Reference and command governors for systems with constraints: A survey on theory and applications," *Automatica*, vol. 75, pp. 306–328, 2017 (DOI 10.1016/j.automatica.2016.08.013). The definitive reference-management survey. Prerequisite: linear systems, invariant-set theory.
- **Input shaping:** Singhose, "Command shaping for flexible systems: A review of the first 50 years," *International Journal of Precision Engineering and Manufacturing*, 2009 — the canonical input-shaping survey node.

## Recommendations

**Stage 1 — build the shared prerequisite spine first.** Add Boyd-Vandenberghe *Convex Optimization* (free), Nocedal-Wright *Numerical Optimization*, and Boyd et al. *LMIs* (free) as prerequisite nodes before any of the seven fields, since MPC, robust, digital, NCS, and trajectory optimization all depend on them. Åström-Murray *Feedback Systems* (free) should sit as an on-ramp before the graduate texts for readers arriving from the Franklin/Boyce branch.

**Stage 2 — attach each field's single core text with edges from the existing graph.** Recommended primary edges: MPC ← Hespanha + Boyd-Vandenberghe (→ Rawlings-Mayne-Diehl); Robust ← Hespanha + functional analysis/Luenberger (→ Skogestad-Postlethwaite); Adaptive ← Khalil (→ Ioannou-Sun); Sliding mode ← Khalil ch. 14 / Slotine-Li ch. 7 (→ Shtessel et al.); Digital ← Franklin-Powell-Workman (→ Åström-Wittenmark Computer-Controlled); NCS ← Khalil + Hespanha (→ Hespanha survey + Fridman); Trajectory ← Boyd-Vandenberghe + Nocedal-Wright (→ Kelly 2017 + LaValle). Prioritize the free-PDF core texts to maximize accessibility.

**Stage 3 — layer advanced monographs behind each core node**, using the core-vs-advanced split above. Place the definitive survey papers (Mayne et al. 2000; Packard-Doyle 1993; Garone et al. 2017; Hespanha et al. 2007; Bristow et al. 2006) as lightweight terminal nodes off each field.

**Reference-only re-routing (do not use as first self-study):** route Utkin (1992) behind Shtessel et al.; Narendra-Annaswamy behind Ioannou-Sun; Chen-Francis behind both Åström-Wittenmark and Zhou-Doyle. Camacho-Bordons and Maciejowski are optional applied supplements to Rawlings-Mayne-Diehl, not replacements.

**Benchmarks that would change these choices:** if a reader lacks Lyapunov fluency, insert Khalil ch. 3–4, 8 before adaptive/sliding/NCS; if they lack Hardy-space/functional-analysis background, insert a functional-analysis node before Zhou-Doyle-Glover and Chen-Francis; if convex-optimization fluency is absent, MPC and trajectory-optimization nodes should be gated behind Boyd-Vandenberghe.

## Caveats
- **Edition/printing nuances:** The Rawlings-Mayne-Diehl 2nd edition is variously cited as 2017, 2019 (2nd, electronic-only printing), and 2020 (3rd paperback printing, revised Ch. 4), and was reissued in 2024. Treat "2nd edition (2020 3rd printing / 2024 reissue)" as the current reference. The Lavretsky-Wise 2nd edition is confirmed as 2024 (hardcover ISBN 978-3-031-38313-7).
- **Free-PDF legitimacy:** The confirmed publisher/author-sanctioned free PDFs are Rawlings-Mayne-Diehl (UCSB), Boyd-Vandenberghe and Boyd et al. LMIs (Stanford/SIAM/Berkeley), Skogestad-Postlethwaite (NTNU), Ioannou-Sun (USC), Åström-Murray (fbsbook.org, publisher-permitted), LaValle (lavalle.pl/UIUC), Bemporad's MPC PDF (IMT Lucca), and the Heemels and Schenato survey PDFs. The Goodwin-Graebe-Salgado full text on a Chilean university server is informally hosted — treat as convenience, not guaranteed OA. Sastry-Bodson and Doyle-Francis-Tannenbaum have historically circulated as author PDFs but are also cheaply available via Dover; verify current author-site availability.
- **"Zhou-Doyle-Glover vs Essentials" is a genuine distinction:** the 1996 *Robust and Optimal Control* (596 pp.) is the full monograph; the 1998 *Essentials of Robust Control* is the abridged teaching version — different books by overlapping author sets, both from Prentice Hall.
- **Bertsekas DP volumes have no free PDF** (only lecture slides and the freely downloadable *Abstract Dynamic Programming* and sample chapters); do not mark the main DP volumes as open-access.
- **Items warranting a final publisher-page check before the DAG goes live:** the Zaccarian-Teel 2005-vs-2011 copyright-year anomaly (use 2011), the current live host of the Sastry-Bodson PDF, and the exact page counts for LaValle (842 vs 844) and Chen-Francis. None of these affect the core-vs-advanced classifications.