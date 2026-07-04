# -*- coding: utf-8 -*-
# PHASE 1 fact records — corpus: emb-c (Design of Embedded Software Written in C)
# Source report: compass_artifact_wf-d72114ee-... Raw tags: theme | level | type | verification.
R = []
C = 'emb-c'
def n(id, title, au, yr, typ, theme, level='design', ver='verified', note='', ident=''):
    R.append(dict(id=id, corpus=C, title=title, authors=au, year=yr, rtype=typ,
                  verification=ver, note=note, ident=ident, unresolved=[],
                  raw=dict(theme=theme, level=level)))

# Theme 1 — coding-style
n('barrc','Embedded C Coding Standard (BARR-C:2018)','M. Barr / Barr Group','2018','standard','coding-style','design','verified','Descends from Netrino-C (2008); harmonized with MISRA C:2012; shared node','ISBN 978-1721127986')
n('misrac','MISRA C:2025 (with C:2023, C:2012 +AMD1-4/TC1-TC2, C:2004, C:1998 predecessors)','MISRA Consortium','2025','standard','coding-style','design','verified','225 active guidelines; covers C90/C99/C11/C18; themes coding-style + safety-caveats; shared node')
n('kandr','The C Programming Language, 2nd ed.','B.W. Kernighan & D.M. Ritchie','1988','book','coding-style','design','verified','Sec. 5.11 function-pointer dispatch design-patterns-relevant; general tag','Prentice Hall, ISBN 978-0131103627')
n('kernelstyle','Linux kernel coding style','Linux kernel community','living','tooling-doc','coding-style','design','verified','Source of the goto-cleanup idiom','Documentation/process/coding-style.rst')
n('yiu','The Definitive Guide to ARM Cortex-M3/M4/M0 series','J. Yiu','2020','book','coding-style','arch-realization','verified','Multiple editions 2013-2020; shared node','Newnes')
# Theme 2 — safety-caveats
n('misracompliance','MISRA Compliance:2020','MISRA Consortium','2020','standard','safety-caveats','design','verified','GEP/GCS, deviation records; mandatory from MISRA C:2023 onward')
n('certc','The CERT C Coding Standard, 2nd ed. (98 Rules)','R.C. Seacord','2014','standard','safety-caveats','design','verified','1st ed. 2008','Addison-Wesley, ISBN 978-0321984043')
n('seacordsecure','Secure Coding in C and C++, 2nd ed.','R.C. Seacord','2013','book','safety-caveats','design','verified','','Addison-Wesley')
n('hatton95','Safer C: Developing Software for High-Integrity and Safety-Critical Systems','L. Hatton','1995','book','safety-caveats','design','verified','KEY empirical critique of C','McGraw-Hill, ISBN 978-0077076405')
n('koopmanbess','Better Embedded System Software','P. Koopman','2022','book','safety-caveats','design','verified','1st ed. 2010; reissue 2021; e-book v1.1 Dec 2022; shared node','ISBN 979-8596008050')
n('seacordeffc','Effective C, 2nd ed.','R.C. Seacord','2024','book','safety-caveats','design','verified','Covers C23; UB/IB for professional C','No Starch Press')
n('holzmannp10','The Power of 10: Rules for Developing Safety-Critical Code','G.J. Holzmann','2006','paper','safety-caveats','design','verified','Shared node; expanded JPL writeup at spinroot.com/p10','IEEE Computer 39(6):95-99')
n('dietzintoverflow','Understanding Integer Overflow in C/C++','W. Dietz, P. Li, J. Regehr & V. Adve','2015','paper','safety-caveats','design','verified','ICSE 2012 pp.760-770; expanded ACM TOSEM 25(1) 2015','DOI 10.1145/2743019')
n('jplstd','JPL Institutional Coding Standard for the C Programming Language','NASA/JPL Laboratory for Reliable Software','2009','standard','safety-caveats','design','verified','Also an emb-arch lead (flight-software standard) — merged')
n('framac','Frama-C: A Software Analysis Perspective','P. Cuoq, F. Kirchner, N. Kosmatov, V. Prevosto, J. Signoles & B. Yakobowski','2015','paper','safety-caveats','design','verified','SEFM 2012 LNCS 7504; journal FAoC 27:573-609 (2015); ACSL, WP, EVA','DOI 10.1007/s00165-014-0326-7')
# Theme 3 — documentation
n('doxygen','Doxygen (manual, current)','D. van Heesch','living','tooling-doc','documentation','design','verified','(c)1997-2026; de facto C/C++ doc generator; shared node','doxygen.nl/manual')
n('breathe','Breathe (Doxygen-XML to Sphinx bridge)','breathe-doc project','living','tooling-doc','documentation','design','verified','','breathe-doc.org')
n('exhale','Exhale (automatic C/C++ API docs via Doxygen + Sphinx + Breathe)','S. McDowell (svenevs)','living','tooling-doc','documentation','design','verified','','github.com/svenevs/exhale')
n('hawkmoth','Hawkmoth (Sphinx C/C++ autodoc via Clang)','J. Nikula','living','tooling-doc','documentation','design','verified','','github.com/jnikula/hawkmoth')
n('gtkdoc','GTK-Doc (GNOME C API documentation tool)','GNOME project','living','tooling-doc','documentation','design','verified','KEY for C API docs','gitlab.gnome.org/GNOME/gtk-doc')
n('kerneldoc','kernel-doc (Linux kernel documentation system)','Linux kernel community','living','tooling-doc','documentation','design','verified','','docs.kernel.org/doc-guide/kernel-doc.html')
n('naturaldocs','Natural Docs','G. Valure','living','tooling-doc','documentation','design','verified','Since 2003; v2 AGPL','naturaldocs.org')
n('knuthlit','Literate Programming','D.E. Knuth','1992','book','documentation','design','verified','Orig. paper The Computer Journal 27(2):97-111, 1984','CSLI Lecture Notes 27, ISBN 0-937073-80-6')
# Theme 4 — quality-goals
n('grenningtdd','Test-Driven Development for Embedded C','J.W. Grenning','2011','book','quality-goals','design','verified','Dual-target testing; CppUTest & Unity; ZOMBIES; shared node','Pragmatic Bookshelf, ISBN 978-1934356623')
n('unity','Unity (xUnit-style unit-test framework for C)','ThrowTheSwitch.org','living','tooling-doc','quality-goals','design','verified','','github.com/ThrowTheSwitch/Unity')
n('cmock','CMock (mock/stub generator for C headers)','ThrowTheSwitch.org','living','tooling-doc','quality-goals','design','verified','','github.com/throwtheswitch/cmock')
n('ceedling','Ceedling (test/build manager, v1.0; bundles Unity + CMock + CException)','ThrowTheSwitch.org','living','tooling-doc','quality-goals','design','verified','','github.com/throwtheswitch/ceedling')
n('mcdcchilenski','Applicability of Modified Condition/Decision Coverage to Software Testing','J.J. Chilenski & S.P. Miller','1994','paper','quality-goals','design','verified','MC/DC origins; shared node','SEJ 9(5):193-200')
n('mcdcnasa','A Practical Tutorial on Modified Condition/Decision Coverage','K.J. Hayhurst et al.','2001','report','quality-goals','design','verified','KEY free MC/DC tutorial; shared node','NASA/TM-2001-210876')
# Theme 5 — collaboration
n('bacchellibird','Expectations, Outcomes, and Challenges of Modern Code Review','A. Bacchelli & C. Bird','2013','paper','collaboration','design','verified','','ICSE 2013 pp.712-721, DOI 10.1109/ICSE.2013.6606617')
n('sadowskigoogle','Modern Code Review: A Case Study at Google','C. Sadowski, E. Soderberg, L. Church, M. Sipko & A. Bacchelli','2018','paper','collaboration','design','verified','','ICSE-SEIP 2018, DOI 10.1145/3183519.3183525')
n('fagan','Design and Code Inspections to Reduce Errors in Program Development','M.E. Fagan','1976','paper','collaboration','design','verified','Report flags common mis-citation (use vol. 15)','IBM Systems Journal 15(3):182-211')
n('wiegers','Peer Reviews in Software: A Practical Guide','K.E. Wiegers','2002','book','collaboration','design','verified','','Addison-Wesley, ISBN 978-0201734850')
n('drepperlibs','How To Write Shared Libraries','U. Drepper','2011','report','collaboration','design','verified','Version dated 2011-12-10; also an emb-ops lead — merged','Free PDF')
n('blanchette','The Little Manual of API Design','J. Blanchette','2008','report','collaboration','design','verified','2008-06-19, ~30 pp.','Trolltech/Nokia')
n('bloch','How to Design a Good API and Why it Matters','J. Bloch','2006','paper','collaboration','design','verified','','OOPSLA 2006 Companion, DOI 10.1145/1176617.1176622')
n('clangformat','clang-format','LLVM/Clang project','living','tooling-doc','collaboration','design','verified','Shared node','clang.llvm.org/docs/ClangFormat.html')
n('clangtidy','clang-tidy','LLVM/Clang project','living','tooling-doc','collaboration','design','verified','Shared node','clang.llvm.org/extra/clang-tidy')
n('uncrustify','Uncrustify (source beautifier)','uncrustify project','living','tooling-doc','collaboration','design','verified','GPL-2.0','github.com/uncrustify/uncrustify')
n('editorconfig','EditorConfig','EditorConfig project','living','tooling-doc','collaboration','design','verified','','editorconfig.org')
n('precommit','pre-commit (hook framework)','A. Sottile','living','tooling-doc','collaboration','design','verified','','pre-commit.com')
n('boogerdmoonen','Assessing the Value of Coding Standards: An Empirical Study / Evaluating the Relation Between Coding Standard Violations and Faults','C. Boogerd & L. Moonen','2009','paper','collaboration','design','verified','Contested evidence: 10 of 89 MISRA C:2004 rules predict faults; compliance can increase faults','ICSM 2008; 2009')
n('hattonsubset','Language subsetting in an industrial context: MISRA C 1998 vs 2004 / Safer language subsets: MISRA C','L. Hatton','2004','paper','collaboration','design','verified','Argues both MISRA C versions too noisy','IST 46(7):465-472')
# Theme 6 — design-patterns
n('preschern','Fluent C: Principles, Practices, and Patterns','C. Preschern','2022','book','design-patterns','design','verified','KEY: error handling, memory pools, #ifdef-hell escape','OReilly, 2022-11-22, ISBN 978-1492097334')
n('hanson','C Interfaces and Implementations: Techniques for Creating Reusable Software','D.R. Hanson','1996','book','design-patterns','design','verified','Opaque types; 24 reusable APIs; literate programs','Addison-Wesley, ISBN 978-0201498417')
n('schreiner','Object-Oriented Programming with ANSI-C','A.-T. Schreiner','2011','book','design-patterns','design','verified','1993; free PDF maintained through 2011 (ooc v1.3c)')
n('douglasspatternsc','Design Patterns for Embedded Systems in C','B.P. Douglass','2010','book','design-patterns','design','verified','Shared node (emb-arch cites 2011 printing; report years differ — see adjustments)','Newnes, ISBN 978-1856177078')
n('samekbook','Practical UML Statecharts in C/C++, 2nd ed.','M. Samek','2008','book','design-patterns','design','verified','Shared node','Newnes, ISBN 978-0750687065')
n('qpc','QP/C real-time embedded framework','Quantum Leaps (M. Samek)','living','tooling-doc','design-patterns','arch-realization','verified','Active objects in C','state-machine.com')
n('samekcourse','Modern Embedded Systems Programming video course','M. Samek','living','course','design-patterns','design','verified','50+ lessons, free; shared node')
# Unverified leads
def U(id,t,a,y,typ,theme,note=''):
    n(id,t,a,y,typ,theme,'design','unverified',note)
U('preschernplop','Patterns for... EuroPLoP/PLoP pattern-paper series (organizing files; returning error information)','C. Preschern','UNRESOLVED','paper','design-patterns','2019-2021; exact titles/years unconfirmed')
U('tornhill','Patterns in C','A. Tornhill','UNRESOLVED','book','design-patterns','Leanpub, ~2014-2015')
U('gustedt','Modern C (3rd ed., C23)','J. Gustedt','UNRESOLVED','book','safety-caveats','Free; unverified this pass')
U('lattnerub','What Every C Programmer Should Know About Undefined Behavior','C. Lattner','2011','blog','safety-caveats','LLVM blog series')
U('regehrub','A Guide to Undefined Behavior in C and C++','J. Regehr','UNRESOLVED','blog','safety-caveats','Blog series')
U('eideregehr','Volatiles Are Miscompiled, and What to Do about It','E. Eide & J. Regehr','2008','paper','safety-caveats','EMSOFT 2008')
U('osstyleguides','Zephyr / FreeRTOS / Apache NuttX / ESP-IDF coding guidelines; ARM CMSIS API conventions','Various projects','living','tooling-doc','collaboration')
U('sqlitetesting','How SQLite Is Tested','SQLite project','living','other','quality-goals')
U('nigeljones',"A 'C' Test: The 0x10 Best Questions for Would-be Embedded Programmers",'N. Jones','UNRESOLVED','blog','coding-style','embedded.com column set')
U('barrbugs','Top 10 Causes of Nasty Firmware Bugs','M. Barr','UNRESOLVED','blog','safety-caveats','embedded.com column set')
# white/beningo/noblesmallmem/parnas72/lakoslsc/martincleanarch leads merged into verified nodes — see build.py.
