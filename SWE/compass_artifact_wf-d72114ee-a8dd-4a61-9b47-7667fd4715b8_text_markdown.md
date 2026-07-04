# Maximum-Recall Reference Corpus: The Design of Embedded Software Written in C

**Scope:** Language-and-context specialization (C, embedded) of a prior embedded software architecture/design corpus. Overlap with the prior corpus is expected and welcome; entries are scoped by tags, not by exclusion. Each entry carries four tags: **theme** (coding-style | safety-caveats | documentation | quality-goals | collaboration | design-patterns), **level** (design | arch-realization), **type**, and **verification**. Compiled July 4, 2026. A short list is a failure; correctly-tagged over-inclusion is not.

## TL;DR
- This corpus collects 60+ individually-verified core resources plus a quarantined lead list across all six themes; the strongest verified clusters are **safety-caveats** (MISRA/CERT/UB literature) and **design-patterns-in-C** (Preschern, Hanson, Schreiner, Douglass, Samek).
- Every book, standard, paper, and tool in the verified sections was checked against publisher pages, DOIs, or official project sites; leads that could not be confirmed within the research budget are isolated in the "Unverified / to confirm" section — none are fabricated.
- The corpus is deliberately over-inclusive: general-C works, general-design works, and architecture-realization works are tagged and kept, not dropped, so the two corpora merge cleanly later.

## Key Findings
- **Current standard versions confirmed.** MISRA C:2025 (published March 2025) is the latest; per Perforce it "covers C90, C99, and C11/C18; rationalizes and reorganizes existing guidelines… and adds new guidelines… to give a total of 225 active guidelines" (Grokipedia adds it introduces four new rules, removes two, modifies 13 for clarity, and renumbers three). MISRA C:2023 (the "Third Edition, second revision," 221 guidelines) is the prior consolidated edition; MISRA Compliance:2020 is the mandatory compliance framework. CERT C is at its 2nd edition (2014). BARR-C:2018 is current.
- **Design-patterns-in-C literature is unusually deep and specific** (opaque types, error-handling, memory pools, hierarchical state machines, OO-in-C), anchored by Preschern's *Fluent C* (O'Reilly, Nov 22 2022, 304 pp., ISBN 978-1492097334), Hanson's *C Interfaces and Implementations* (1996), Schreiner's free *OOP with ANSI-C* (1993/2011), Douglass (2010), and Samek (2008).
- **Empirical evidence on coding standards is genuinely contested.** Boogerd & Moonen (2009) state "We find that 10 rules in the standard are significant predictors of fault location" (of 89 MISRA C:2004 rules studied across two commercial embedded C projects), and warn that whole-standard compliance "can actually result in an increase in faults, as any modification has a non-zero probability of introducing a fault." Hatton reached a consistent conclusion. This tension is flagged, not smoothed over.

## Details

### Theme 1 — coding-style

**Standards / style guides**
- **Embedded C Coding Standard (BARR-C:2018)**, Michael Barr / Barr Group, 2018. Free PDF + HTML + print (ISBN 978-1721127986). type: standard; level: design; verification: verified-exists. First published 2008 (descends from Netrino-C); fully harmonized with MISRA C:2012. Covers naming, headers, module/source templates, fixed-width integers, ISR rules.
- **MISRA C:2025**, The MISRA Consortium, March 2025 (225 active guidelines; covers C90/C99/C11/C18). type: standard; level: design; verification: verified-exists. Primary theme safety-caveats; carries stylistic directives too. Architecturally-relevant predecessors: MISRA C:2023, C:2012, C:2004, C:1998.
- **The C Programming Language, 2nd ed.**, Brian W. Kernighan & Dennis M. Ritchie, Prentice Hall, 1988 (ISBN 978-0131103627). type: book; level: design; verification: verified-exists. Foundational general-C; §5.11 function-pointer dispatch is directly design-patterns-relevant. Collected with general tag.
- **Linux kernel coding style** (Documentation/process/coding-style.rst), Linux kernel community. type: tooling-doc; level: design; verification: verified-exists. Canonical corporate/community C style; source of the goto-cleanup idiom (secondary: design-patterns, collaboration).

**Books (MCU-centric, C-idiom)**
- **The Definitive Guide to ARM Cortex-M3/M4/M0** series, Joseph Yiu, Newnes (multiple editions 2013–2020). type: book; level: arch-realization; verification: verified-exists. C-centric MCU programming; route to architecture branch if grafting.

### Theme 2 — safety-caveats

**Standards & compliance**
- **MISRA C:2025 / C:2023 / C:2012 (+AMD1–4, TC1–TC2)**, MISRA Consortium. type: standard; level: design; verification: verified-exists. C:2012 AMD4 (2023) adds multithreading (Rules 22.11–22.20) and atomics; AMD1 (2016) security; AMD2 (2020) C11 core; AMD3 (2022) C11/C18 features. Addenda map coverage to CERT C 2nd ed., ISO/IEC 17961, and ISO/IEC 24772 (Parts 1 & 3).
- **MISRA Compliance:2020**, MISRA Consortium, 2020. type: standard; level: design; verification: verified-exists. Defines Guideline Enforcement Plan (GEP), Guideline Compliance Summary (GCS), Deviation Records/Permits; mandatory framework from MISRA C:2023 onward.
- **The CERT C Coding Standard, 2nd ed. (98 Rules for Developing Safe, Reliable, and Secure Systems)**, Robert C. Seacord, Addison-Wesley, 2014 (ISBN 978-0321984043; e-ISBN 978-0133805277). type: standard/book; level: design; verification: verified-exists. C11/C99 secure coding; 1st ed. 2008.
- **Secure Coding in C and C++, 2nd ed.**, Robert C. Seacord, Addison-Wesley, 2013. type: book; level: design; verification: verified-exists.

**Books**
- **Safer C: Developing Software for High-Integrity and Safety-Critical Systems**, Les Hatton, McGraw-Hill (International Series in Software Engineering), 1995 (ISBN 978-0077076405, 229 pp.). type: book; level: design; verification: verified-exists. KEY: empirical critique of C, safer subsets, commercial-C fault-density measurement.
- **Better Embedded System Software**, Philip Koopman, self-published; 1st ed. 2010, paperback reissue 2021 (ISBN 979-8596008050), e-book v1.1 Dec 2022. type: book; level: design; verification: verified-exists. Per author site, "distills the experience of more than 90 design reviews on real embedded systems… Each of the 29 chapters is self-sufficient." Primary safety/quality; secondary collaboration.
- **Effective C, 2nd ed.**, Robert C. Seacord, No Starch Press, 2024 (1st ed. 2020, ISBN 978-1718501041). type: book; level: design; verification: verified-exists. Covers C23; undefined/implementation-defined behavior for professional C.

**Papers / reports**
- **"The Power of 10: Rules for Developing Safety-Critical Code"**, Gerard J. Holzmann, *IEEE Computer* 39(6):95–99, 2006. DOI 10.1109/MC.2006.212. type: paper; level: design; verification: verified-exists. Also the expanded JPL "Guidelines for Safety-Critical Software: The Power of Ten" writeup (spinroot.com/p10).
- **"Understanding Integer Overflow in C/C++"**, Will Dietz, Peng Li, John Regehr, Vikram Adve, ICSE 2012, pp. 760–770. DOI 10.1109/ICSE.2012.6227142 (ACM SIGSOFT Distinguished Paper). Expanded as *ACM TOSEM* 25(1), 2015, DOI 10.1145/2743019. type: paper; level: design; verification: verified-exists.
- **JPL Institutional Coding Standard for the C Programming Language**, NASA/JPL Laboratory for Reliable Software, 2009. type: standard/report; level: design; verification: verified-exists.

**Formal tools**
- **"Frama-C: A Software Analysis Perspective"**, Pascal Cuoq, Florent Kirchner, Nikolai Kosmatov, Virgile Prevosto, Julien Signoles, Boris Yakobowski, SEFM 2012, LNCS 7504, pp. 233–247, DOI 10.1007/978-3-642-33826-7_16; journal version in *Formal Aspects of Computing* 27:573–609, 2015, DOI 10.1007/s00165-014-0326-7. type: paper/tooling-doc; level: design; verification: verified-exists. ACSL specification language; WP (deductive) and EVA/Value (abstract-interpretation) plugins.

### Theme 3 — documentation

- **Doxygen** (manual, current), Dimitri van Heesch, 1997–present (© 1997–2026). https://www.doxygen.nl/manual/. type: tooling-doc; level: design; verification: verified-exists. De facto C/C++ documentation generator; extracts from `/**`…`*/` and `///` comment blocks; HTML/LaTeX/RTF/XML/man output; include/collaboration graphs via Graphviz.
- **Breathe** (Doxygen-XML → Sphinx reST bridge), breathe-doc project. https://www.breathe-doc.org/. type: tooling-doc; level: design; verification: verified-exists.
- **Exhale** (automatic C/C++ API docs via Doxygen + Sphinx + Breathe), Stephen McDowell (svenevs). https://github.com/svenevs/exhale. type: tooling-doc; level: design; verification: verified-exists.
- **Hawkmoth** (Sphinx C/C++ autodoc via Clang Python bindings), Jani Nikula. https://github.com/jnikula/hawkmoth. type: tooling-doc; level: design; verification: verified-exists.
- **GTK-Doc** (GNOME C API documentation tool). https://gitlab.gnome.org/GNOME/gtk-doc. type: tooling-doc; level: design; verification: verified-exists. KEY for C API docs (handles GObject signals/properties).
- **kernel-doc** (Linux kernel documentation system), Linux kernel community. Documentation/doc-guide/kernel-doc.rst; https://docs.kernel.org/doc-guide/kernel-doc.html. type: tooling-doc; level: design; verification: verified-exists.
- **Natural Docs**, Greg Valure, since 2003 (v2 rewritten in C#, AGPL). https://www.naturaldocs.org/. type: tooling-doc; level: design; verification: verified-exists.
- **Literate Programming** (book), Donald E. Knuth, CSLI Lecture Notes No. 27, CSLI Publications, 1992 (ISBN 0-937073-80-6). Original paper: "Literate Programming," *The Computer Journal* 27(2):97–111, 1984, DOI 10.1093/comjnl/27.2.97. type: book/paper; level: design; verification: verified-exists. Documentation-theme root; note also that Hanson's *C Interfaces and Implementations* is presented as literate programs.

### Theme 4 — quality-goals

**Books**
- **Test-Driven Development for Embedded C**, James W. Grenning, Pragmatic Bookshelf, 2011 (print ISBN 978-1934356623; e-book ISBN 978-1680504880). type: book; level: design; verification: verified-exists. KEY: dual-target host/target testing, test doubles/spies/mocks, CppUTest & Unity, adding tests to legacy code; author also promotes the ZOMBIES unit-test heuristic.

**Tooling**
- **Unity** (xUnit-style unit-test framework for C; single C file + two headers), ThrowTheSwitch.org. https://github.com/ThrowTheSwitch/Unity. type: tooling-doc; level: design; verification: verified-exists.
- **CMock** (mock/stub generator that parses C headers into mockable interfaces), ThrowTheSwitch.org. https://github.com/throwtheswitch/cmock. type: tooling-doc; level: design; verification: verified-exists.
- **Ceedling** (test/build manager, now v1.0; bundles Unity + CMock + CException, adds coverage/CI plugins), ThrowTheSwitch.org. https://github.com/throwtheswitch/ceedling. type: tooling-doc; level: design; verification: verified-exists.

**Coverage papers/reports**
- **"Applicability of Modified Condition/Decision Coverage to Software Testing"**, John J. Chilenski & Steven P. Miller, *Software Engineering Journal* 9(5):193–200, 1994, DOI 10.1049/sej.1994.0025. type: paper; level: design; verification: verified-exists. MC/DC origins (avionics DO-178B/C exit criterion).
- **A Practical Tutorial on Modified Condition/Decision Coverage**, Kelly J. Hayhurst, Dan S. Veerhusen, John J. Chilenski, Leanna K. Rierson, NASA/TM-2001-210876, 2001. type: report; level: design; verification: verified-exists. KEY free MC/DC tutorial.

### Theme 5 — collaboration

**Code-review literature**
- **"Expectations, Outcomes, and Challenges of Modern Code Review"**, Alberto Bacchelli & Christian Bird, ICSE 2013, pp. 712–721, DOI 10.1109/ICSE.2013.6606617. type: paper; level: design; verification: verified-exists.
- **"Modern Code Review: A Case Study at Google"**, Caitlin Sadowski, Emma Söderberg, Luke Church, Michal Sipko, Alberto Bacchelli, ICSE-SEIP 2018, pp. 181–190, DOI 10.1145/3183519.3183525. type: paper; level: design; verification: verified-exists.
- **"Design and Code Inspections to Reduce Errors in Program Development"**, Michael E. Fagan, *IBM Systems Journal* 15(3):182–211, 1976, DOI 10.1147/sj.153.0182. type: paper; level: design; verification: verified-exists. Foundational inspection method. (Note: a common secondary-source citation of vol. 38, pp. 258–287 is erroneous; use vol. 15.)
- **Peer Reviews in Software: A Practical Guide**, Karl E. Wiegers, Addison-Wesley, 2002 (ISBN 978-0201734850). type: book; level: design; verification: verified-exists.

**API/ABI design & style-enforcement tooling**
- **How To Write Shared Libraries**, Ulrich Drepper, free PDF, current version dated 2011-12-10. type: report; level: design; verification: verified-exists. KEY for C library interface/ABI discipline (no persistent DOI; mirrored widely).
- **The Little Manual of API Design**, Jasmin Blanchette, Trolltech/Nokia, June 19 2008, free PDF (~30 pp.). type: report; level: design; verification: verified-exists. KEY concise API-design guidance.
- **"How to Design a Good API and Why it Matters"**, Joshua Bloch, OOPSLA 2006 Companion, pp. 506–507, DOI 10.1145/1176617.1176622. type: paper; level: design; verification: verified-exists.
- **clang-format** & **clang-tidy** (LLVM/Clang project). https://clang.llvm.org/docs/ClangFormat.html and https://clang.llvm.org/extra/clang-tidy/. type: tooling-doc; level: design; verification: verified-exists.
- **Uncrustify** (C/C++/… source beautifier, GPL-2.0). https://github.com/uncrustify/uncrustify. type: tooling-doc; level: design; verification: verified-exists.
- **EditorConfig** (cross-editor style consistency). https://editorconfig.org. type: tooling-doc; level: design; verification: verified-exists.
- **pre-commit** (multi-language pre-commit hook framework), Anthony Sottile. https://pre-commit.com/. type: tooling-doc; level: design; verification: verified-exists.

**Empirical coding-standard studies (contested — flag when citing)**
- **"Assessing the Value of Coding Standards: An Empirical Study,"** Cathal Boogerd & Leon Moonen, ICSM 2008; and **"Evaluating the Relation Between Coding Standard Violations and Faults Within and Across Software Versions,"** Boogerd & Moonen, 2009. type: paper; level: design; verification: verified-exists. Verbatim finding: "We find that 10 rules in the standard are significant predictors of fault location" (of 89 MISRA C:2004 rules across two commercial embedded C projects), and whole-standard compliance "can actually result in an increase in faults."
- **"Language subsetting in an industrial context: a comparison of MISRA C 1998 and MISRA C 2004"** and **"Safer language subsets: an overview and a case history, MISRA C"** (*Information & Software Technology* 46(7):465–472, 2004), Les Hatton. type: paper; level: design; verification: verified-exists. Argues both MISRA C versions are "too noisy to be of any real use" — corroborates Boogerd & Moonen.

### Theme 6 — design-patterns

**Books**
- **Fluent C: Principles, Practices, and Patterns**, Christopher Preschern, O'Reilly Media, November 22 2022 (ISBN 978-1492097334, 304 pp.). type: book; level: design; verification: verified-exists. KEY: error handling (guard clause, samurai principle, goto error handling, cleanup record, object-based error handling), returning error info, memory management (stack first, eternal memory, dedicated ownership, memory pool), returning data from functions, data lifetime/ownership, flexible APIs, cursor iterators, organizing files in modular programs, "escaping #ifdef Hell." Author: PhD, industrial C at ABB.
- **C Interfaces and Implementations: Techniques for Creating Reusable Software**, David R. Hanson, Addison-Wesley (Professional Computing Series), 1996 (ISBN 978-0201498417). type: book; level: design; verification: verified-exists. KEY: interface-based design separating interface from implementation, opaque/abstract data types, exceptions & assertions, memory management, 24 reusable APIs (secondary: collaboration, quality-goals).
- **Object-Oriented Programming with ANSI-C**, Axel-Tobias Schreiner, 1993; free PDF maintained through 2011 (ooc v1.3c). type: book; level: design; verification: verified-exists. KEY OO-in-C: information hiding for ADTs, generic functions via dynamic linkage, inheritance by structure extension, class hierarchy, the `ooc` preprocessor, dynamic type checking, delegates/callbacks, exceptions.
- **Design Patterns for Embedded Systems in C: An Embedded Software Engineering Toolkit**, Bruce Powel Douglass, Newnes, 2010 (ISBN 978-1856177078; e-ISBN 978-0080959719, 472 pp.). type: book; level: design; verification: verified-exists. KEY: UML-plus-ANSI-C patterns addressing concurrency, communication, speed, and memory usage.
- **Practical UML Statecharts in C/C++, 2nd ed.: Event-Driven Programming for Embedded Systems**, Miro Samek, Newnes/Elsevier, 2008 (ISBN 978-0750687065). 1st ed. *Practical Statecharts in C/C++*, CMP Books, 2002. type: book; level: design; verification: verified-exists. KEY: hierarchical state machines, state-machine coding techniques/patterns, active objects (actors), the QP framework; ARM Cortex-M worked examples.

**Framework docs / courses**
- **QP/C real-time embedded framework** (Quantum Leaps), Miro Samek. https://www.state-machine.com. type: tooling-doc; level: arch-realization; verification: verified-exists. Active-object / inversion-of-control realization in C; bare-metal or over an RTOS. Route to architecture branch if grafting.
- **Modern Embedded Systems Programming** video course, Miro Samek, YouTube (free, 50+ lessons). type: course/lecture; level: design; verification: verified-exists.

## Recommendations
1. **Import flat, keep tags, don't de-duplicate yet.** Load every verified entry with its four tags intact. Because Open Fork #1 (independent corpus vs. graft onto the prior design branch) is deliberately unresolved, retain overlapping entries; route only the `arch-realization`-tagged items (Yiu, QP/C) to the architecture branch if and when the user chooses the graft option. Impose no graph structure (Open Fork #2 unresolved) — these are flat tagged rows.
2. **Use these verified anchors for any curated shortlist:** BARR-C:2018 (coding-style); MISRA C:2025 + Hatton + Holzmann + Frama-C (safety-caveats); Doxygen + Knuth + GTK-Doc/kernel-doc (documentation); Grenning + Unity/Ceedling + Chilenski–Miller + Hayhurst MC/DC tutorial (quality-goals); Bacchelli & Bird + Fagan + Drepper + Blanchette (collaboration); Preschern + Hanson + Schreiner + Douglass + Samek (design-patterns).
3. **Always flag the contested MISRA-effectiveness evidence** (Boogerd & Moonen; Hatton) so downstream readers do not over-claim that standard adherence reduces defects; the data supports rule-subset selection, not blanket compliance.
4. **Next-pass expansion targets (benchmark: keep searching until new queries surface no new works).** Prioritize the Unverified list below, plus: vendor/OS coding standards (Zephyr, FreeRTOS, ESP-IDF, CMSIS API conventions); the undefined-behavior literature (Lattner's LLVM blog series 2011, Regehr's UB guide, Wang et al. SOSP 2013 STACK, Eide & Regehr EMSOFT 2008 on volatile); Dan Saks / Nigel Jones / Michael Barr embedded.com column sets; and additional testing/coverage tools (CppUTest, cmocka, gcov/lcov/gcovr, VectorCAST, LDRA, Cantata). These are where recall currently thins.

## Caveats
- The web-search budget was exhausted before several named leads could be individually verified (*Making Embedded Systems* 2nd ed.; Beningo titles; Preschern's EuroPLoP pattern papers; Gustedt *Modern C*; the Lattner/Regehr UB series; vendor coding standards). They appear below as **unverified**, never as fabricated verified entries.
- Some retail/aggregator pages conflate editions and dates; publisher pages, DOIs, and official project sites were preferred over reseller listings. The Fagan 1976 citation in particular is frequently mis-cited by secondary sources.
- Recall thins most in **Theme 5 (collaboration)** — specifically firmware-specific code-review checklists — and in **vendor/OS documentation** (ARM CMSIS, STM32 HAL, NXP, TI, Zephyr, FreeRTOS). These are the recommended first targets for the next collection pass.

## Unverified / to confirm (verification: unverified)
- *Making Embedded Systems*, Elecia White, O'Reilly — 1st ed. (2011) exists; 2nd ed. (2024) not individually verified this pass. Likely theme: design-patterns/coding-style.
- *Reusable Firmware Development* (2017) and *Embedded Software Design* (2022), Jacob Beningo — not individually verified. Likely themes: quality-goals, arch-realization.
- Christopher Preschern, EuroPLoP/PLoP "Patterns for…" series (2019–2021, e.g., organizing files, returning error information) — exact titles/years unconfirmed. Theme: design-patterns.
- Adam Tornhill, *Patterns in C* (Leanpub, ~2014–2015) — unverified.
- Jens Gustedt, *Modern C* (3rd ed. covering C23; free) — unverified this pass. Theme: safety-caveats/coding-style.
- Chris Lattner, "What Every C Programmer Should Know About Undefined Behavior" (LLVM blog, 2011); John Regehr, "A Guide to Undefined Behavior in C and C++" (blog series) — unverified this pass. Theme: safety-caveats.
- Eide & Regehr, "Volatiles Are Miscompiled, and What to Do about It" (EMSOFT 2008) — unverified this pass. Theme: safety-caveats.
- Noble & Weir, *Small Memory Software: Patterns for Systems with Limited Memory* (Addison-Wesley, 2001) — not verified this pass. Theme: design-patterns.
- Zephyr Project / FreeRTOS / Apache NuttX / ESP-IDF coding guidelines; ARM CMSIS docs; SQLite "How SQLite Is Tested" — unverified this pass. Themes: collaboration/quality-goals/arch-realization.
- Dan Saks, Nigel Jones ("A 'C' Test: The 0x10 Best Questions…"), and Michael Barr ("Top 10 Causes of Nasty Firmware Bugs") embedded.com column sets — unverified this pass. Themes: safety-caveats/coding-style.
- Parnas, "On the Criteria To Be Used in Decomposing Systems into Modules" (CACM 1972); Lakos, *Large-Scale C++ Software Design* (1996/2019); Martin, *Clean Architecture* (2017) — modularization/physical-design roots frequently used by C teams; collect tagged general/arch-realization but not re-verified this pass.

*Coverage summary:* This pass swept embedded-C textbooks/monographs; coding standards and their secondary literature; formal/static-analysis tooling; testing/coverage frameworks and TDD; documentation generators; design-patterns-in-C books; collaboration/code-review literature; API/ABI design; and peer-reviewed empirical studies — verifying each entry via publisher pages, DOIs, WorldCat/retail cross-checks, and official project sites. Recall is strongest in safety-caveats and design-patterns and thinnest in vendor/OS documentation, firmware-specific code-review checklists, the undefined-behavior blog/paper corpus, and named-columnist embedded.com material, all of which are queued in the Unverified section and the next-pass recommendations.