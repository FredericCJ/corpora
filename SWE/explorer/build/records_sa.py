# -*- coding: utf-8 -*-
# PHASE 1 fact records — corpus: swa-science
# Source report: "Software Architecture as a Science: A Clustered, Typed Reading-Graph Corpus"
# (compass_artifact_wf-4b680b52-...). Tags transcribed RAW as stated by the report.
# tier flags: t=target/anchor(star), c=core, a=advanced, s=survey(pilcrow)
R = []
C = 'swa-science'
def n(id, title, au, yr, typ, cluster, tier, oa, note='', ident='', ver='verified', unresolved=None):
    R.append(dict(id=id, corpus=C, title=title, authors=au, year=yr, rtype=typ,
                  verification=ver, note=note, ident=ident,
                  unresolved=unresolved or [],
                  raw=dict(cluster=cluster, branch=cluster[0], tier=tier, oa=oa)))

# A1 — Foundations of the discipline
n('perrywolf','Foundations for the Study of Software Architecture','D.E. Perry & A.L. Wolf','1992','paper','A1','tc','yes','', 'ACM SIGSOFT SEN 17(4):40-52')
n('shawgarlan96','Software Architecture: Perspectives on an Emerging Discipline','M. Shaw & D. Garlan','1996','book','A1','tc','no','','Prentice Hall')
n('garlanshaw93','An Introduction to Software Architecture','D. Garlan & M. Shaw','1993','paper','A1','c','yes','CMU tech-report version open','Adv. SE & KE Vol.1, World Scientific')
n('tmd','Software Architecture: Foundations, Theory, and Practice','R.N. Taylor, N. Medvidovic & E.M. Dashofy','2010','book','A1','tc','no','Only edition; no 2nd edition exists (report-verified)','Wiley, ISBN 978-0470167748')
n('bck','Software Architecture in Practice, 4th ed.','L. Bass, P. Clements & R. Kazman','2021','book','A1','c','no','','Addison-Wesley SEI, ISBN 978-0-13-688609-9')
n('shaw01','The Coming-of-Age of Software Architecture Research','M. Shaw','2001','paper','A1','as','yes','','Proc. ICSE 2001')
n('garlan14','Software Architecture: a Travelogue','D. Garlan','2014','paper','A1','as','yes','','Proc. FOSE 2014')
# A2 — Views & description frameworks
n('iso42010','ISO/IEC/IEEE 42010:2022 — Software, systems and enterprise — Architecture description','ISO/IEC/IEEE','2022','standard','A2','tc','no','2nd ed. 2022-11-07; cancels/replaces 42010:2011')
n('vab','Documenting Software Architectures: Views and Beyond, 2nd ed.','P. Clements, F. Bachmann, L. Bass, D. Garlan, J. Ivers, R. Little, P. Merson, R. Nord & J. Stafford','2010','book','A2','tc','no','','Addison-Wesley')
n('kruchten','Architectural Blueprints — The 4+1 View Model of Software Architecture','P. Kruchten','1995','paper','A2','c','yes','','IEEE Software 12(6):42-50')
n('rozanski','Software Systems Architecture: Working with Stakeholders Using Viewpoints and Perspectives, 2nd ed.','N. Rozanski & E. Woods','2011','book','A2','c','no','BORDERLINE on science bar (report flag)','Addison-Wesley')
n('hofmeister00','Applied Software Architecture','C. Hofmeister, R. Nord & D. Soni','2000','book','A2','c','no','','Addison-Wesley')
n('emeryhilliard','Every Architecture Description Needs a Framework: Expressing Architecture Frameworks Using ISO/IEC 42010','D. Emery & R. Hilliard','2009','paper','A2','a','yes','','Proc. WICSA/ECSA 2009')
n('medvidovicuml','Modeling Software Architectures in the Unified Modeling Language','N. Medvidovic, D.S. Rosenblum, D.F. Redmiles & J.E. Robbins','2002','paper','A2','a','partial','','ACM TOSEM 11(1):2-57')
# A3 — ADLs & formal semantics
n('medtay','A Classification and Comparison Framework for Software Architecture Description Languages','N. Medvidovic & R.N. Taylor','2000','paper','A3','tcs','yes','','IEEE TSE 26(1):70-93')
n('wright','A Formal Basis for Architectural Connection (Wright, CSP semantics)','R. Allen & D. Garlan','1997','paper','A3','ta','partial','','ACM TOSEM 6(3):213-249')
n('rapide','Specification and Analysis of System Architecture Using Rapide','D.C. Luckham, J.J. Kenney, L.M. Augustin, J. Vera, D. Bryan & W. Mann','1995','paper','A3','a','no','','IEEE TSE 21(4):336-355')
n('darwin','Dynamic Structure in Software Architectures (Darwin)','J. Magee & J. Kramer','1996','paper','A3','a','partial','','Proc. FSE-4; ACM SIGSOFT SEN 21(6):3-14')
n('acme','Acme: An Architecture Description Interchange Language','D. Garlan, R.T. Monroe & D. Wile','1997','paper','A3','a','yes','Reprinted 2010, CASCON First Decade','Proc. CASCON 97 pp.169-183')
n('moriconi','Correct Architecture Refinement','M. Moriconi, X. Qian & R.A. Riemenschneider','1995','paper','A3','a','no','','IEEE TSE 21(4):356-372')
n('piadl','pi-ADL: an ADL based on the higher-order typed pi-calculus for dynamic and mobile architectures','F. Oquendo','2004','paper','A3','a','partial','Report corrects stray 28(8) citations','ACM SIGSOFT SEN 29(3):1-14')
n('feilergluch','Model-Based Engineering with AADL: An Introduction to the SAE Architecture Analysis & Design Language','P.H. Feiler & D.P. Gluch','2012','book','A3','a','no','','Addison-Wesley SEI')
n('abowd','Formalizing Style to Understand Descriptions of Software Architecture','G.D. Abowd, R. Allen & D. Garlan','1995','paper','A3','a','yes','','ACM TOSEM 4(4):319-364')
n('sfm','Formal Methods for Software Architectures (SFM 2003)','M. Bernardo & P. Inverardi (eds.)','2003','book','A3','a','no','','Springer LNCS 2804')
n('aldini','A Process Algebraic Approach to Software Architecture Design','A. Aldini, M. Bernardo & F. Corradini','2010','book','A3','a','no','','Springer')
n('malavolta','What Industry Needs from Architectural Languages: A Survey','I. Malavolta, P. Lago, H. Muccini, P. Pelliccione & A. Tang','2013','paper','A3','as','yes','','IEEE TSE 39(6):869-891')
# A4 — Model checking & formal verification
n('zhang','A Classification and Comparison of Model Checking Software Architecture Techniques','P. Zhang, H. Muccini & B. Li','2010','paper','A4','tas','no','','JSS 83(5):723-744')
n('mismatch95','Architectural Mismatch: Why Reuse Is So Hard','D. Garlan, R. Allen & J. Ockerbloom','1995','paper','A4','a','yes','','IEEE Software 12(6):17-26')
n('mismatch09','Architectural Mismatch: Why Reuse Is Still So Hard','D. Garlan, R. Allen & J. Ockerbloom','2009','paper','A4','a','yes','','IEEE Software 26(4):66-69')
# A5 — Dynamic / self-adaptive
n('oreizy','Architecture-Based Runtime Software Evolution','P. Oreizy, N. Medvidovic & R.N. Taylor','1998','paper','A5','ta','yes','','Proc. ICSE 98 pp.177-186')
n('rainbow','Rainbow: Architecture-Based Self-Adaptation with Reusable Infrastructure','D. Garlan, S.-W. Cheng, A.-C. Huang, B. Schmerl & P. Steenkiste','2004','paper','A5','a','yes','','IEEE Computer 37(10):46-54')
n('kramermagee','Self-Managed Systems: an Architectural Challenge','J. Kramer & J. Magee','2007','paper','A5','a','yes','','Proc. FOSE 2007')
n('weyns','An Introduction to Self-Adaptive Systems: A Contemporary Software Engineering Perspective','D. Weyns','2020','book','A5','a','no','BORDERLINE — advanced consolidation node (report flag)','Wiley/IEEE')
# A6 — Architecture evolution
n('breivold','A Systematic Review of Software Architecture Evolution Research','H.P. Breivold, I. Crnkovic & M. Larsson','2012','paper','A6','tas','no','','IST 54(1):16-40')
n('barnes','Evolution Styles: foundations and models for software architecture evolution','J.M. Barnes, D. Garlan & B. Schmerl','2014','paper','A6','a','yes','','SoSyM 13(2):649-678')
# A7 — Reference architectures & product lines
n('angelov','A framework for analysis and design of software reference architectures','S. Angelov, P. Grefen & D. Greefhorst','2012','paper','A7','ta','no','','IST 54(4):417-431')
n('galster','Empirically-grounded reference architectures: a proposal','M. Galster & P. Avgeriou','2011','paper','A7','a','yes','','Proc. QoSA/ISARCS 2011')
n('sple','Software Product Lines: Practices and Patterns','P. Clements & L. Northrop','2001','book','A7','c','no','BORDERLINE on science bar (report flag)','Addison-Wesley')
# B1 — Design-process roots / design science
n('parnas72','On the Criteria To Be Used in Decomposing Systems into Modules','D.L. Parnas','1972','paper','B1','tc','yes','','CACM 15(12):1053-1058')
n('parnas74',"On a 'Buzzword': Hierarchical Structure",'D.L. Parnas','1974','paper','B1','c','partial','','Proc. IFIP Congress 74')
n('parnas79','Designing Software for Ease of Extension and Contraction','D.L. Parnas','1979','paper','B1','c','partial','','IEEE TSE SE-5(2):128-138')
n('parnasclements','A Rational Design Process: How and Why to Fake It','D.L. Parnas & P.C. Clements','1986','paper','B1','tc','yes','','IEEE TSE SE-12(2):251-257')
n('simon96','The Sciences of the Artificial, 3rd ed.','H.A. Simon','1996','book','B1','a','no','','MIT Press')
n('rittelwebber','Dilemmas in a General Theory of Planning','H.W.J. Rittel & M.M. Webber','1973','paper','B1','a','yes','','Policy Sciences 4(2):155-169')
# B2 — Design methods & the general design model
n('gendesign','A General Model of Software Architecture Design Derived from Five Industrial Approaches','C. Hofmeister, P. Kruchten, R.L. Nord, H. Obbink, A. Ran & P. America','2007','paper','B2','tcs','partial','','JSS 80(1):106-126')
n('cervanteskazman','Designing Software Architectures: A Practical Approach, 2nd ed.','H. Cervantes & R. Kazman','2024','book','B2','tc','no','Published 2024-06-14; ADD method core unchanged','Addison-Wesley SEI, ISBN 9780138108021')
n('bosch00','Design and Use of Software Architectures: Adopting and Evolving a Product-Line Approach','J. Bosch','2000','book','B2','c','no','','Addison-Wesley')
n('jansenbosch','Software Architecture as a Set of Architectural Design Decisions','A. Jansen & J. Bosch','2005','paper','B2','c','yes','','Proc. WICSA 2005 pp.109-120')
n('boschmolin','Software architecture design: evaluation and transformation','J. Bosch & P. Molin','1999','paper','B2','a','no','','Proc. IEEE ECBS 99')
# B3 — Design rationale & architectural knowledge
n('ibis','Issues as Elements of Information Systems (IBIS)','W. Kunz & H.W.J. Rittel','1970','paper','B3','tc','yes','','Working Paper 131, IURD, UC Berkeley')
n('qoc','Questions, Options, and Criteria: Elements of Design Space Analysis (QOC)','A. MacLean, R.M. Young, V.M.E. Bellotti & T.P. Moran','1991','paper','B3','c','no','','HCI 6(3-4):201-250')
n('drl',"What's in Design Rationale? (DRL)",'J. Lee & K.-Y. Lai','1991','paper','B3','c','partial','','HCI 6(3-4):251-280')
n('dutoit','Rationale Management in Software Engineering','A.H. Dutoit, R. McCall, I. Mistrik & B. Paech (eds.)','2006','book','B3','c','no','','Springer')
n('burge','Rationale-Based Software Engineering','J.E. Burge, J.M. Carroll, R. McCall & I. Mistrik','2008','book','B3','a','no','','Springer')
n('tangjinhan','A rationale-based architecture model for design traceability and reasoning','A. Tang, Y. Jin & J. Han','2007','paper','B3','a','partial','','JSS 80(6):918-934')
n('zimmermann','Reusable Architectural Decision Models for Enterprise Application Development','O. Zimmermann et al.','2007','paper','B3','a','partial','Line of papers (QoSA 2007 - WICSA 2015); anchor to be finalized per report','Proc. QoSA 2007', unresolved=['anchor'])
n('capilla','10 years of software architecture knowledge management: Practice and future','R. Capilla, A. Jansen, A. Tang, P. Avgeriou & M.A. Babar','2016','paper','B3','tcs','yes','','JSS 116:191-205')
n('weinreich','Software architecture knowledge management approaches and their support for knowledge management activities: A systematic literature review','R. Weinreich & I. Groher','2016','paper','B3','as','no','','IST 80:265-286')
n('tangsurvey06','A survey of architecture design rationale','A. Tang, M.A. Babar, I. Gorton & J. Han','2006','paper','B3','a','yes','','JSS 79(12):1792-1804')
n('vanvliettang','Decision making in software architecture','H. van Vliet & A. Tang','2016','paper','B3','a','partial','','JSS 117:638-644')
# B4 — Empirical studies of design reasoning
n('falessi','Decision-making techniques for software architecture design: A comparative survey','D. Falessi, G. Cantone, R. Kazman & P. Kruchten','2011','paper','B4','tas','partial','','ACM Computing Surveys 43(4) Art.33')
n('zannier','A model of design decision making based on empirical results of interviews with software designers','C. Zannier, M. Chiasson & F. Maurer','2007','paper','B4','a','no','','IST 49(6):637-653')
n('tangrazavian','Empirical studies on software design reasoning and reflection','A. Tang, M. Razavian et al.','UNRESOLVED','paper','B4','a','partial','Cluster of papers; anchor to be selected per report','', unresolved=['anchor','year'])
# S1 — Evaluation canon
n('esa','Evaluating Software Architectures: Methods and Case Studies','P. Clements, R. Kazman & M. Klein','2001','book','S1','tc','no','','Addison-Wesley')
n('atam','ATAM: Method for Architecture Evaluation','R. Kazman, M. Klein & P. Clements','2000','report','S1','tc','yes','','SEI CMU/SEI-2000-TR-004')
n('saam','SAAM: A Method for Analyzing the Properties of Software Architectures','R. Kazman, G. Abowd, L. Bass & M. Webb','1994','paper','S1','c','yes','','Proc. ICSE 94')
n('dobrica','A Survey on Software Architecture Analysis Methods','L. Dobrica & E. Niemela','2002','paper','S1','tcs','no','','IEEE TSE 28(7):638-653')
n('babar04','A Framework for Classifying and Comparing Software Architecture Evaluation Methods','M.A. Babar, L. Zhu & R. Jeffery','2004','paper','S1','as','partial','','Proc. ASWEC 2004 pp.309-318')
n('alma','Architecture-level modifiability analysis (ALMA)','P. Bengtsson, N. Lassing, J. Bosch & H. van Vliet','2004','paper','S1','a','no','','JSS 69(1-2):129-147')
# S2 — Quality-attribute models
n('iso25010','ISO/IEC 25010:2023 — SQuaRE — Product quality model','ISO/IEC','2023','standard','S2','tc','no','2nd ed. 2023-11-15; Safety added; Usability/Portability replaced')
n('barbacci','Quality Attributes','M. Barbacci, M.H. Klein, T.A. Longstaff & C.B. Weinstock','1995','report','S2','c','yes','','SEI CMU/SEI-95-TR-021')
n('abas','Attribute-Based Architectural Styles (ABAS)','M. Klein & R. Kazman','1999','report','S2','a','yes','','SEI CMU/SEI-99-TR-022')
n('tactics','Deriving Architectural Tactics: A Step Toward Methodical Architectural Design','F. Bachmann, L. Bass & M. Klein','2003','report','S2','a','yes','','SEI CMU/SEI-2003-TR-004')
# S3 — Economics & technical debt
n('cbam','Quantifying the Costs and Benefits of Architectural Decisions (CBAM)','R. Kazman, J. Asundi & M. Klein','2001','paper','S3','tc','yes','Extended in SEI/2002 CBAM work','Proc. ICSE 2001')
n('techdebt19','Managing Technical Debt: Reducing Friction in Software Development','P. Kruchten, R. Nord & I. Ozkaya','2019','book','S3','c','no','','Addison-Wesley SEI, ISBN 9780135645932')
n('dagstuhl16','Managing Technical Debt in Software Engineering','P. Avgeriou, P. Kruchten, I. Ozkaya & C. Seaman','2016','report','S3','a','yes','','Dagstuhl Reports 6(4):110-138')
n('rcda','RCDA: Architecting as a risk- and cost management discipline','E.R. Poort & H. van Vliet','2012','paper','S3','a','yes','Report corrects a vol.95 typo seen in one portal','JSS 85(9):1995-2013')
