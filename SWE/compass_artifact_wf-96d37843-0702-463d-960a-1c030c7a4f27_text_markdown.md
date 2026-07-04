# Maximum-Recall Reference Corpus: Design of Embedded Software Written in C++

## TL;DR
- Assembled a broad, tagged corpus of ~90 verified real works spanning seven themes; every entry carries theme/level/type/verification tags for downstream human curation, with deliberate overlap kept (not dropped).
- The richest, best-verified veins are coding standards/subsetting (MISRA C++, AUTOSAR C++14, JSF AV, HIC++, EC++, CERT, DO-332), WG21 freestanding/exceptions/safety papers, and register-abstraction/metaprogramming works.
- Recall thins on individual academic theses (HU Utrecht/RWTH), some embedded.com columns, and several vendor tooling-doc versions — all flagged in the Unverified section for the user's final curation pass.

## Key Findings
The corpus below is organized by primary theme. Every entry carries four tags: **theme | level | type | verification**. Overlap with the prior embedded-C and embedded-architecture corpora is expected and preserved — architecture-realization entries are tagged `arch-realization` so they can later be routed to the architecture branch rather than dropped.

---
### THEME 1: coding-style

- **Real-Time C++: Efficient Object-Oriented and Template Microcontroller Programming**, Christopher Kormanyos, 4th ed., Springer, 2021, ISBN 978-3-662-62995-6 (C++20-based; earlier eds 2013/2015/2018; companion code at github.com/ckormanyos/real-time-cpp). [coding-style | design | book | verified-exists] — Canonical modern-C++-on-MCU text.
- **Hands-On Embedded Programming with C++17**, Maya Posch, Packt, 2019, ISBN 9781788629300. [coding-style | design | book | verified-exists]
- **Embedded Programming with Modern C++ Cookbook**, Igor Viarheichyk, Packt, 2020. [coding-style | design | book | verified-exists] — Linux-targeted embedded C++.
- **Hands-On RTOS with Microcontrollers (FreeRTOS, STM32, SEGGER)**, Brian Amos, Packt, 2020. [coding-style | design | book | verified-exists]
- **A Tour of C++**, Bjarne Stroustrup, 3rd ed. (C++20), Addison-Wesley, 2022. [coding-style | design | book | verified-exists]
- **Effective Modern C++**, Scott Meyers, O'Reilly, 2014. [coding-style | design | book | verified-exists]
- **Effective C++**, Scott Meyers, 3rd ed., Addison-Wesley, 2005. [coding-style | design | book | verified-exists]
- **Effective C++ in an Embedded Environment (Presentation Materials)**, Scott Meyers, Artima Press, last revised April 2, 2015, 320 pp. (course page aristeia.com/c++-in-embedded.html). [coding-style | design | course/lecture | verified-exists] — Costs of language features, ROMing, ISRs, MMIO modeling, safety-critical considerations.
- **Embedded C++ Guide** and **C++ style guide**, Google Pigweed, living docs (pigweed.dev/embedded_cpp_guide.html; pigweed.dev/style/cpp.html). [coding-style | design | tooling-doc | verified-exists] — Constexpr discipline, no-heap/no-exceptions subset, C++17 baseline; extends Google style with embedded restrictions.
- **Google C++ Style Guide**, Google, living document. [coding-style | design | tooling-doc | verified-exists] — Famous exceptions ban.
- **The Definitive Guide to ARM Cortex-M3 and Cortex-M4 Processors**, Joseph Yiu, 3rd ed., Newnes, 2013. [coding-style | design | book | verified-exists] — C-centric MCU text with C++ relevance (collect tagged).

### THEME 2: feature-caveats

- **ISO/IEC TR 18015:2006 — Technical Report on C++ Performance**, ISO/IEC JTC1/SC22/WG21 (project editor Lois Goldthwaite; participants incl. Stroustrup, Saks, the Embedded C++ Technical Committee), 2006, reviewed/confirmed 2013 (draft free at open-std.org/jtc1/sc22/wg21/docs/18015.html; also CSA/ANSI reissue). [feature-caveats | design | standard | verified-exists] — KEY cost model: EH/RTTI/virtual-dispatch overhead, ROMability/predictability, EC++ discussion, dedicated chapter on C/C++ hardware interfaces (<iohw.h>).
- **Low-cost deterministic C++ exceptions for embedded systems**, James Renwick, Tom Spink, Björn Franke, Proc. 28th Int'l Conf. on Compiler Construction (CC '19), Feb 2019, pp. 76–86, DOI 10.1145/3302516.3307346. [feature-caveats | design | paper | verified-exists]
- **P0709 Zero-overhead deterministic exceptions: Throwing values**, Herb Sutter, WG21, R0 (2018) through R4 (2019) (open-std.org). [feature-caveats | design | paper | verified-exists]
- **P2232 Zero-Overhead Deterministic Exceptions: Catching Values**, WG21, 2021. [feature-caveats | design | paper | verified-exists] — Counterpoint arguing the existing zero-overhead-on-happy-path ABI tradeoff.
- **P1028 SG14 status_code and standard error object**, Niall Douglas, WG21, R3 2020. [feature-caveats | design | paper | verified-exists] — Freestanding-compatible error object; potential P0709 implementation.
- **Embedded Template Library (ETL)**, John Wellbelove (Aster Consulting Ltd.), etlcpp.com / github.com/ETLCPP/etl, MIT, maintained since 2014, current v20.44.2 (Dec 2025). [feature-caveats | design | tooling-doc | verified-exists] — No-heap fixed-capacity STL alternative; C++03-compatible with later-standard backports.
- **EASTL — Electronic Arts Standard Template Library (WG21 N2271)**, Paul Pedriana, 2007 (open-std.org); code at github.com/electronicarts/EASTL. [feature-caveats | design | paper | verified-exists] — Rationale for game/embedded-style allocator and memory constraints.
- **Boost.Outcome documentation** (incl. experimental status_code and P1095 simulation), Niall Douglas, living doc (boostorg.github.io/outcome). [feature-caveats | design | tooling-doc | verified-exists] — Error-handling alternative to exceptions.
- **Bloaty McBloatface binary-size profiler**, Google, github.com/google/bloaty, living. [feature-caveats | design | tooling-doc | verified-exists] — Bloat/map-file analysis.
- **pw_bloat memory-report module**, Google Pigweed, pigweed.dev, living. [feature-caveats | design | tooling-doc | verified-exists] — Per-change binary size impact.

### THEME 3: feature-subsetting

- **MISRA C++:2023**, The MISRA Consortium, published October 2023, based on ISO/IEC 14882:2017 (C++17); **179 guidelines = 4 Directives + 175 Rules** (confirmed verbatim by Parasoft: "There are 179 MISRA C++ 2023 guidelines, four Directives, and 175 Rules"); merges the AUTOSAR C++14 guidelines into a single MISRA-led standard (merger announced Jan 2019); compliance governed by MISRA Compliance:2020. [feature-subsetting | design | standard | verified-exists] — Supersedes MISRA C++:2008.
- **MISRA C++:2008**, MISRA, 2008, based on C++ ISO/IEC 14882:2003 (C++03); **228 rules** (confirmed by Perforce: "MISRA C++:2008 was published in 2008. It was written for C++03. There are 228 coding rules"). [feature-subsetting | design | standard | verified-exists] — Predecessor.
- **Guidelines for the use of the C++14 language in critical and safety-related systems (AUTOSAR C++14)**, AUTOSAR, Document ID 839, ~510 pp.; official release **AP 18-10, dated 2018-10-31**; Release 19-03 (March 2019) added only document updates, no rule changes (later marked obsolete as it was folded into MISRA C++:2023). [feature-subsetting | design | standard | verified-exists] — ~342–397 rules; traceable to HIC++ 4.0, JSF, CERT, Core Guidelines, MISRA C++:2008.
- **JSF Air Vehicle C++ Coding Standards**, Lockheed Martin, Doc. 2RDU00001 Rev C, December 2005 (free at stroustrup.com/JSF-AV-rules.pdf); **Rev D, June 2007 also exists** (confirmed via embedded.com); 221 rules; Stroustrup involvement. [feature-subsetting | design | standard | verified-exists] — Bans C++ exceptions entirely; adds coding-style and metric rules absent from MISRA.
- **High Integrity C++ Coding Standard v4.0**, Programming Research Ltd / PRQA (now Perforce), October 3, 2013; **155 rules (consolidated down from 202), categorised against ISO C++ 2011 (C++11)** (confirmed by PRQA/SD Times). [feature-subsetting | design | standard | verified-exists] — First published Oct 2003.
- **SEI CERT C++ Coding Standard (2016 Edition)**, Aaron Ballman (ed.), Carnegie Mellon Software Engineering Institute, 2016, 435 pp., free PDF (resources.sei.cmu.edu). [feature-subsetting | design | standard | verified-exists] — Builds on the SEI CERT C Coding Standard.
- **The Embedded C++ (EC++) specification, version WP-AM-003**, Embedded C++ Technical Committee (chair Hiroshi Monden, NEC; members Toshiba, Fujitsu, Hitachi, Matsushita, Mitsubishi, Motorola Japan), October 1999, based on ISO/IEC 14882:1998 (C++98) (caravan.net/ec2plus). [feature-subsetting | design | standard | verified-exists] — Historical/obsolete; removed templates, exceptions, RTTI, multiple inheritance, namespaces; Stroustrup FAQ: "EC++ is dead (2004), and if it isn't it ought to be."
- **C++ Core Guidelines**, Bjarne Stroustrup & Herb Sutter (eds.), living document (github.com/isocpp/CppCoreGuidelines) + profiles. [feature-subsetting | design | tooling-doc | verified-exists]
- **DO-332 Object-Oriented Technology and Related Techniques Supplement to DO-178C and DO-278A**, RTCA, dated December 13, 2011 (EUROCAE ED-217; recognized by FAA AC 20-115D). [feature-subsetting | design | standard | verified-exists] — OO/C++ verification concerns (inheritance, polymorphism, dynamic memory, exceptions) in avionics.
- **P0829 Freestanding Proposal**, Ben Craig, WG21, R4 dated 2019-01-12. [feature-subsetting | design | paper | verified-exists] — Maximal freestanding library subset for kernel/embedded (no OS, no space overhead).
- **P1105 Leaving no room for a lower-level language: A C++ Subset**, Ben Craig & Ben Saks, WG21, 2018–2019. [feature-subsetting | design | paper | verified-exists] — Removes/modifies core features unusable in freestanding environments.
- **P2198 Freestanding Feature-Test Macros and Implementation-Defined Extensions**, Ben Craig, WG21. [feature-subsetting | design | paper | verified-exists]
- **P2338 Freestanding Library: Character primitives and the C library**, WG21. [feature-subsetting | design | paper | verified-exists]
- **P2268 Freestanding Roadmap**, Ben Craig, WG21. [feature-subsetting | design | paper | verified-exists]
- **P0568 Towards Better Embedded programming support for C++**, WG21 SG14, 2017. [feature-subsetting | design | paper | verified-exists] — SG14 rejection of the EC++ approach; embedded needs survey.
- **P2739 A call to action: Think seriously about "safety"; then do something sensible about it**, Bjarne Stroustrup, WG21, 2022-12-06. [feature-subsetting | design | paper | verified-exists]
- **P2816 Safety Profiles: Type-and-resource safe programming in ISO standard C++**, Bjarne Stroustrup & Gabriel Dos Reis, WG21, 2023-02-16. [feature-subsetting | design | paper | verified-exists]
- **P3081 Core safety Profiles: Specification, adoptability, and impact**, Herb Sutter, WG21, R1 2025-01-06. [feature-subsetting | design | paper | verified-exists]

### THEME 4: documentation

- **Doxygen documentation**, Dimitri van Heesch, doxygen.nl, living. [documentation | design | tooling-doc | unverified] — Primary automated doc generator; not directly re-verified this session.
- **Pigweed reference-documentation conventions for C++** (reST/Sphinx-based; "How to structure reference documentation for C++ code"), Google Pigweed, pigweed.dev, living. [documentation | design | tooling-doc | verified-exists].

### THEME 5: quality-goals

- **Test-Driven Development for Embedded C**, James W. Grenning, Pragmatic Bookshelf, 2011 (CppUTest-based; C++-relevant; code at github.com/jwgrenning/tddec-code). [quality-goals | design | book | verified-exists].
- **CppUTest / CppUMock**, cpputest.github.io / github.com/cpputest/cpputest, current v4.0. [quality-goals | design | tooling-doc | verified-exists] — Official site names Grenning as author of the TDD-for-embedded-C book.
- **GoogleTest / GoogleMock**, Google, google.github.io/googletest, living. [quality-goals | design | tooling-doc | verified-exists]
- **Catch2**, original author Phil Nash; current lead maintainer Martin Hořeňovský, github.com/catchorg/Catch2, v3.x (multi-header; Boost Software License 1.0). [quality-goals | design | tooling-doc | verified-exists]
- **doctest**, Viktor Kirilov, github.com/doctest/doctest (formerly onqtam/doctest), MIT, single-header, fast-compile. [quality-goals | design | tooling-doc | verified-exists]
- **trompeloeil**, Björn Fahller, github.com/rollbear/trompeloeil, Boost Software License 1.0, header-only C++14 mocking framework. [quality-goals | design | tooling-doc | verified-exists] — Companion talk "Using Trompeloeil, a Mocking Framework for Modern C++," ACCU 2017 (also NDC Oslo 2017).
- **pw_unit_test**, Google Pigweed, pigweed.dev, living. [quality-goals | design | tooling-doc | verified-exists] — GoogleTest-compatible, built on embedded-friendly primitives, no dynamic allocation.
- **A Practical Tutorial on Modified Condition/Decision Coverage**, Kelly J. Hayhurst, Dan S. Veerhusen, John J. Chilenski, Leanna K. Rierson, NASA/TM-2001-210876 (L-18088), NASA, May 2001. [quality-goals | design | report | verified-exists] — Free, language-agnostic MC/DC report applicable to C++.
- **Applicability of modified condition/decision coverage to software testing**, John J. Chilenski & Steven P. Miller, Software Engineering Journal, Vol. 9, No. 5, Sept 1994, pp. 193–200, DOI 10.1049/sej.1994.0025. [quality-goals | design | journal | verified-exists] — MC/DC origin paper.
- **clang-tidy** (incl. cppcoreguidelines-*, cert-* check groups), LLVM, clang.llvm.org, living. [quality-goals | design | tooling-doc | verified-exists] — Static analysis / style enforcement.
- **cppcheck (with MISRA addon)**, Daniel Marjamäki et al., cppcheck.sourceforge.io, living. [quality-goals | design | tooling-doc | unverified] — Real project; not directly re-verified this session.

### THEME 6: collaboration

- **Pigweed SDK / build-system integrations (Bazel, GN, CMake)**, Google, pigweed.dev, living (Developer Preview announced Aug 2024). [collaboration | arch-realization | tooling-doc | verified-exists] — Hermetic, reproducible embedded build/toolchain; facade/backend module pattern; shipped in Pixel, Nest, satellites, drones.
- **clang-format documentation**, LLVM, clang.llvm.org, living. [collaboration | design | tooling-doc | verified-exists] — Automated style enforcement (Pigweed formats all C++ with it).
- **CMake documentation / build organization for embedded C++**, Kitware, cmake.org, living. [collaboration | design | tooling-doc | unverified] — Not directly re-verified this session.
- **Guideline Support Library (GSL)**, Microsoft/isocpp, github.com/microsoft/GSL, living. [collaboration | design | tooling-doc | unverified] — Not directly re-verified this session.

### THEME 7: design-patterns

- **C++ Software Design: Design Principles and Patterns for High-Quality Software**, Klaus Iglberger, O'Reilly, October 25, 2022, ISBN 978-1-098-11316-2, 435 pp. [design-patterns | design | book | verified-exists] — KEY: type erasure, CRTP, external polymorphism, value semantics, small-buffer optimization.
- **Embracing Modern C++ Safely**, John Lakos, Vittorio Romeo, Rostislav Khlebnikov, Alisdair Meredith, Addison-Wesley, December 2021, ISBN 978-0-13-738035-0, ~1,376 pp. [design-patterns | design | book | verified-exists] — Safe / Conditionally-Safe / Unsafe C++11/14 feature taxonomy (KEY safe-adoption guidance; secondary theme: feature-caveats).
- **Practical UML Statecharts in C/C++: Event-Driven Programming for Embedded Systems**, Miro Samek, 2nd ed., Newnes/Elsevier, 2008, ISBN 978-0-7506-8706-5. [design-patterns | design | book | verified-exists] — Hierarchical state machines, state-machine coding patterns, active-object framework.
- **QP/C++ Real-Time Embedded Framework** + QM modeler, Quantum Leaps (Miro Samek), state-machine.com, living. [design-patterns | arch-realization | tooling-doc | verified-exists] — Active objects in C++ on bare metal or over an RTOS.
- **Kvasir register-abstraction library**, Odin Holmes, kvasir.io / github.com/kvasir-io/Kvasir, living. [design-patterns | design | tooling-doc | verified-exists] — DSL wrapping special-function-register access via metaprogramming with compile-time checking (kvasir::mpl, brigand).
- **"Hey C, This Is What Performance Looks Like"**, Odin Holmes, C++Now 2019 (slides/video at cppnow.org). [design-patterns | design | course/lecture | verified-exists] — Register-access DSL for ARM Cortex SoCs.
- **"Objects? No Thanks!"**, Wouter van Ooijen, Meeting C++ 2014 (reprised Belgian C++ UG 2016, CoreHard Spring 2018). [design-patterns | design | course/lecture | verified-exists] — Compile-time static polymorphism via class templates for very small MCUs.
- **hwlib**, Wouter van Ooijen (Hogeschool Utrecht; SG14), github.com/wovo/hwlib, living. [design-patterns | design | tooling-doc | verified-exists] — Also maintains a list of C++ MCU libraries at voti.nl.
- **C++ Hardware Register Access Redux**, Ken Smith, self-published whitepaper, February 2010 (PDF at yogiken.files.wordpress.com/2010/02/c-register-access.pdf). [design-patterns | design | report | verified-exists] — Influential on later register-abstraction libraries.
- **Typesafe Register Access in C++**, Niklas Hauser, blog.salkinium.com, 2015. [design-patterns | design | other | verified-exists] — Surveys register-access approaches incl. Ken Smith's; author of modm.
- **modm HAL / lbuild generator**, Niklas Hauser et al., modm.io, living. [design-patterns | arch-realization | tooling-doc | verified-exists] — Successor of xpcc.
- **Making things do stuff (register access using C++ templates), Parts 1–8**, Glennan Carnie, Feabhas "Sticky Bits" blog, 2017 (blog.feabhas.com). [design-patterns | design | other | verified-exists] — Template register abstraction, trait classes, tag dispatch, proxy objects, zero-overhead codegen.
- **The Rule of The Big Four (and a half) — Move Semantics and Resource Management** (and companion "Rule of the Big Three (and a half)"), Glennan Carnie, Feabhas "Sticky Bits" blog, 2014–2015. [design-patterns | design | other | verified-exists] — RAII/ownership and copy/move policy for embedded C++.
- **Boost.SML ([Boost::ext].SML) — C++14 State Machine library**, Kris Jusiak, github.com/boost-ext/sml (boost-ext.github.io/sml), header-only. [design-patterns | design | tooling-doc | verified-exists] — Compile-time state machines.
- **"State Machines Battlefield - Naive vs STL vs Boost"** and **"[Boost].DI - Inject all the things!"**, Kris Jusiak, CppCon 2018. [design-patterns | design | course/lecture | verified-exists] — Dependency injection and state-machine design.
- **"What Has My Compiler Done for Me Lately? Unbolting the Compiler's Lid"**, Matt Godbolt, CppCon 2017 keynote; Compiler Explorer at godbolt.org. [design-patterns | design | course/lecture | verified-exists] — KEY codegen-verification method.
- **"Rich Code for Tiny Computers: A Simple Commodore 64 Game in C++17"**, Jason Turner, CppCon 2016. [design-patterns | design | course/lecture | verified-exists] — Zero-overhead demonstration.

## Details
This corpus prioritizes verifiable primary sources. Standards were confirmed against publisher/standards bodies (ISO, RTCA/FAA, AUTOSAR, Perforce, SEI/CMU, MISRA) and WG21 papers against open-std.org; books against publisher/retailer pages. The coding-standards/subsetting theme is the most complete and reliable because those documents are well-catalogued and stable.

The single most important cost-model foundation remains **ISO/IEC TR 18015:2006**, which the C++ committee produced partly in response to EC++: it models the time/space overhead of exceptions, RTTI, and virtual dispatch, addresses ROMability and predictability, and includes a dedicated chapter on C/C++ hardware interfaces. Read alongside it, the arc of **EC++ (1999, obsolete) → MISRA C++:2008 (C++03) → AUTOSAR C++14 (2018) → MISRA C++:2023 (C++17, absorbing AUTOSAR)** captures the entire history of "which C++ features to restrict in embedded/safety-critical contexts," and the WG21 freestanding papers (P0829/P1105/P2198/P2338/P2268) plus the safety-profiles debate (P2739/P2816/P3081) represent the still-live standardization front.

Per the open forks in the brief: (1) overlapping entries with the prior corpora (Samek, register-access blogs, Pigweed, Godbolt/Turner talks) were **kept and tagged**, not de-duplicated, so the corpora merge cleanly; (2) no graph structure was imposed — this is a flat tagged list. Architecture-realization entries (Pigweed SDK, QP/C++, modm) are tagged `arch-realization` so they can be routed to the architecture branch later.

## Recommendations
- **Stage 1 (now):** Treat the seven-theme verified list as the spine. Merge with the prior embedded-C and embedded-architecture corpora by tag, not by cut. Keep overlaps.
- **Stage 2 (short):** Resolve the Unverified section with direct publisher/vendor lookups before promoting to `verified-exists`. Highest priority: the commercial coverage/static-analysis tool doc pages (VectorCAST, LDRA, Polyspace, Coverity, PVS-Studio, Parasoft, Axivion, Bullseye, PC-lint Plus) and Doxygen/cppcheck/CMake/GSL.
- **Stage 3 (scope-dependent):** For safety-critical work, anchor on **MISRA C++:2023** (current) and retain MISRA C++:2008 and AUTOSAR C++14 as superseded/merged references; pair with **DO-332** (avionics) or **ISO 26262-6** (automotive) depending on domain.
- **Benchmark to change approach:** If the user narrows scope to a single domain (automotive vs. avionics vs. bare-metal hobbyist) or a single toolchain, down-weight the non-matching subsetting standards and vendor tools rather than deleting them.

## Caveats
Several entries are living documents whose version numbers drift (Catch2, trompeloeil, ETL, Boost.SML, Kvasir, modm, hwlib) — cite the repository directly rather than a pinned version. A few widely-used tooling docs (Doxygen, cppcheck, CMake, Microsoft GSL) are real but were **not re-verified in this session** and are tagged `unverified`. Commercial testing/coverage/static-analysis tools named in the brief are real products, but their individual documentation pages were not fetched this session and should be confirmed before publication. Conference talks are cited by title/venue/year; exact recording URLs on YouTube were not individually re-fetched. Where the brief supplied pre-verified facts (MISRA C++, Kormanyos, Posch, Viarheichyk, Amos, Renwick et al., Ken Smith, Hauser, Meyers, van Ooijen, Holmes), those were carried through as `verified-exists` and, where possible, independently re-confirmed (MISRA counts, AUTOSAR release/ID, HIC++ rule count, JSF Rev D all re-checked against named vendor/publisher sources).

## Unverified / to confirm
- **Doxygen, cppcheck (+MISRA addon), CMake docs, Microsoft GSL** — real, but not re-verified this session. [various themes | tooling-doc | unverified]
- **Commercial static-analysis/coverage tools** — real vendors/products, individual doc pages not fetched: VectorCAST (Vector), LDRA Testbed, Cantata (QA Systems), Polyspace (MathWorks), Coverity (Synopsys/Black Duck), Klocwork (Perforce), Axivion Suite (Qt Group), PVS-Studio, Parasoft C/C++test, Bullseye Coverage, PC-lint Plus (Vector). [quality-goals | tooling-doc | unverified]
- **Elecia White, "Making Embedded Systems: Design Patterns for Great Software," 2nd ed.** — subagent reports O'Reilly, April 9, 2024, ISBN 978-1-098-15154-6, 425 pp.; retained here as a strong lead pending a direct publisher-page confirmation. [coding-style | design | book | unverified]
- **Daniele Lacamera, "Embedded Systems Architecture," 2nd ed.** — subagent reports Packt, January 13, 2023, ISBN 9781803239545; retained as a strong lead pending direct confirmation (C-oriented, arch-realization relevance). [coding-style | arch-realization | book | unverified]
- **HU Utrecht / RWTH Aachen embedded-C++ HAL/metaprogramming theses** (hwlib/xpcc-related student work) — could not confirm individual theses. [design-patterns | thesis | unverified]
- **Dan Saks embedded.com columns on memory-mapped devices in C++** ("Representing and Manipulating Hardware in Standard C and C++"; possible "Mapping memory efficiently" / "Alternative models for memory-mapped devices") — exact titles/dates not confirmed. [design-patterns | other | unverified]
- **Michael Caisse "Modern C++ in an Embedded World"** and **Ben/Dan Saks "Back to Basics" CppCon talks** — plausible but exact venue/year not confirmed this session. [design-patterns | course/lecture | unverified]

### Coverage summary
This sweep covered, and largely verified via primary sources, the following source types: international standards and technical reports (ISO/IEC, RTCA/EUROCAE), industry coding standards (MISRA, AUTOSAR, JSF AV, HIC++, EC++, SEI CERT), WG21 committee papers (freestanding, exceptions, safety profiles), peer-reviewed papers (CC '19, Software Engineering Journal), NASA technical reports, mainstream and self-published books (Springer, O'Reilly, Addison-Wesley, Packt, Newnes, Artima), open-source libraries and their docs (ETL, EASTL, Kvasir, modm, hwlib, Boost.SML, Boost.Outcome, Pigweed, GoogleTest, CppUTest, Catch2, doctest, trompeloeil), and recorded conference talks (CppCon, C++Now). Recall is strongest in coding-standards/subsetting, feature-caveats, and design-patterns; it thins for (a) individual university theses, (b) specific embedded.com column titles, (c) exact conference-talk recording metadata, and (d) commercial tool documentation versions — all of which are enumerated above as `unverified` for the user's final curation.