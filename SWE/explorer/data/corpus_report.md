# Corpus report — PHASE 1 (scrutiny of the six SWE reports)

Raw records transcribed: **451** -> merged into **421** unique nodes.
Verification: 308 verified / 113 unverified (state preserved from reports; any-verified wins on merge).

## Nodes per corpus (after merge; a node may belong to several)
- swa-science — Software architecture as a science: 77
- emb-arch — Embedded architecture & design: 140
- emb-c — Embedded C design: 68
- emb-cpp — Embedded C++ design: 80
- emb-ops — Embedded C/C++ operational use: 53
- simulink — Large Simulink/MATLAB projects: 53

## Cross-corpus works: 44 nodes appear in >=2 corpora

- parnas72 (swa-science, emb-arch, emb-c): On the Criteria To Be Used in Decomposing Systems into Modules
- white (emb-arch, emb-cpp, emb-c): Making Embedded Systems: Design Patterns for Great Software
- samekbook (emb-arch, emb-c, emb-cpp): Practical UML Statecharts in C/C++: Event-Driven Programming for Embedded Systems, 2nd ed.
- samekcourse (emb-arch, emb-c, emb-ops): Modern Embedded Systems Programming video course + QP framework docs
- grenningtdd (emb-arch, emb-c, emb-cpp): Test-Driven Development for Embedded C
- yiu (emb-arch, emb-c, emb-cpp): The Definitive Guide to ARM Cortex-M3 and Cortex-M4 Processors, 3rd ed.
- shawgarlan96 (swa-science, emb-arch): Software Architecture: Perspectives on an Emerging Discipline
- tmd (swa-science, emb-arch): Software Architecture: Foundations, Theory, and Practice
- bck (swa-science, emb-arch): Software Architecture in Practice, 4th ed.
- iso42010 (swa-science, emb-arch): ISO/IEC/IEEE 42010:2022 — Software, systems and enterprise — Architecture description
- vab (swa-science, emb-arch): Documenting Software Architectures: Views and Beyond, 2nd ed.
- kruchten (swa-science, emb-arch): Architectural Blueprints — The 4+1 View Model of Software Architecture
- rozanski (swa-science, emb-arch): Software Systems Architecture: Working with Stakeholders Using Viewpoints and Perspectives
- feilergluch (swa-science, emb-arch): Model-Based Engineering with AADL: An Introduction to the SAE Architecture Analysis & Desi
- lacamera (emb-arch, emb-cpp): Embedded Systems Architecture
- beningodesign (emb-arch, emb-c): Embedded Software Design: A Practical Approach to Architecture, Processes, and Coding Tech
- beningofw (emb-arch, emb-c): Reusable Firmware Development: A Practical Approach to APIs, HALs and Drivers
- douglasspatternsc (emb-arch, emb-c): Design Patterns for Embedded Systems in C: An Embedded Software Engineering Toolkit
- barrc (emb-arch, emb-c): Embedded C Coding Standard (BARR-C:2018)
- barrmassa (emb-arch, emb-ops): Programming Embedded Systems: With C and GNU Development Tools, 2nd ed.
- misrac (emb-arch, emb-c): MISRA C (C:2012 3rd ed. 2013; +AMD1-3; consolidated C:2023; C:2025)
- misracpp2008 (emb-arch, emb-cpp): MISRA C++:2008
- misracpp2023 (emb-arch, emb-cpp): MISRA C++:2023
- holzmannp10 (emb-arch, emb-c): The Power of Ten: Rules for Developing Safety-Critical Code
- koopmanbess (emb-arch, emb-c): Better Embedded System Software
- noblesmallmem (emb-arch, emb-c): Small Memory Software: Patterns for Systems with Limited Memory
- simmonds (emb-arch, emb-ops): Mastering Embedded Linux Programming, 3rd ed.
- bootlin (emb-arch, emb-ops): Bootlin embedded-Linux training slides
- martincleanarch (emb-arch, emb-c): Clean Architecture
- lakoslsc (emb-arch, emb-c): Large-Scale C++ Software Design
- jplstd (emb-c, emb-arch): JPL Institutional Coding Standard for the C Programming Language
- doxygen (emb-c, emb-cpp): Doxygen (manual, current)
- mcdcchilenski (emb-c, emb-cpp): Applicability of Modified Condition/Decision Coverage to Software Testing
- mcdcnasa (emb-c, emb-cpp): A Practical Tutorial on Modified Condition/Decision Coverage
- drepperlibs (emb-c, emb-ops): How To Write Shared Libraries
- clangformat (emb-c, emb-cpp): clang-format
- clangtidy (emb-c, emb-cpp): clang-tidy
- kormanyos (emb-cpp, emb-ops): Real-Time C++: Efficient Object-Oriented and Template Microcontroller Programming, 4th ed.
- meyerseffmod (emb-cpp, emb-arch): Effective Modern C++
- meyerseffcpp (emb-cpp, emb-arch): Effective C++, 3rd ed.
- bloaty (emb-cpp, emb-ops): Bloaty McBloatface binary-size profiler
- cmake (emb-cpp, emb-ops): CMake documentation / build organization for embedded C++
- godbolt (emb-cpp, emb-ops): What Has My Compiler Done for Me Lately? + Compiler Explorer
- sakscolumns (emb-cpp, emb-c): Dan Saks embedded.com columns on memory-mapped devices in C and C++

## Merges & promotions performed

- feilergluch: merged emb-arch record into existing node (swa-science)
- iso42010: merged emb-arch record into existing node (swa-science)
- bck: merged emb-arch record into existing node (swa-science)
- barrc: merged emb-c record into existing node (emb-arch)
- misrac: merged emb-c record into existing node (emb-arch)
- yiu: merged emb-c record into existing node (emb-arch)
- koopmanbess: merged emb-c record into existing node (emb-arch)
- holzmannp10: merged emb-c record into existing node (emb-arch)
- grenningtdd: merged emb-c record into existing node (emb-arch)
- douglasspatternsc: merged emb-c record into existing node (emb-arch)
- samekbook: merged emb-c record into existing node (emb-arch)
- samekcourse: merged emb-c record into existing node (emb-arch)
- yiu: merged emb-cpp record into existing node (emb-arch+emb-c)
- misracpp2023: merged emb-cpp record into existing node (emb-arch)
- misracpp2008: merged emb-cpp record into existing node (emb-arch)
- doxygen: merged emb-cpp record into existing node (emb-c)
- grenningtdd: merged emb-cpp record into existing node (emb-arch+emb-c)
- mcdcnasa: merged emb-cpp record into existing node (emb-c)
- mcdcchilenski: merged emb-cpp record into existing node (emb-c)
- clangtidy: merged emb-cpp record into existing node (emb-c)
- clangformat: merged emb-cpp record into existing node (emb-c)
- samekbook: merged emb-cpp record into existing node (emb-arch+emb-c)
- barrmassa: merged emb-ops record into existing node (emb-arch)
- simmonds: merged emb-ops record into existing node (emb-arch)
- samekcourse: merged emb-ops record into existing node (emb-arch+emb-c)
- godbolt: merged emb-ops record into existing node (emb-cpp)
- kormanyos: merged emb-ops record into existing node (emb-cpp)
- bloaty: merged emb-ops record into existing node (emb-cpp)
- bootlin: merged emb-ops record into existing node (emb-arch)
- cmake: merged emb-ops record into existing node (emb-cpp)
- shawgarlan96: +emb-arch membership — general-classics lead in emb-arch (unverified there; verified by swa-science)
- tmd: +emb-arch membership — general-classics lead in emb-arch
- kruchten: +emb-arch membership — general-classics lead in emb-arch
- rozanski: +emb-arch membership — general-classics lead in emb-arch
- vab: +emb-arch membership — general-classics lead in emb-arch
- parnas72: +emb-arch membership — Parnas modularity papers lead in emb-arch
- parnas72: +emb-c membership — modularization-roots lead in emb-c
- meyerseffcpp: +emb-arch membership — general-classics lead in emb-arch (verified by emb-cpp)
- meyerseffmod: +emb-arch membership — general-classics lead in emb-arch (verified by emb-cpp)
- white: +emb-cpp membership — 2nd-ed lead in emb-cpp (verified by emb-arch)
- white: +emb-c membership — lead in emb-c
- lacamera: +emb-cpp membership — 2nd-ed lead in emb-cpp (verified by emb-arch)
- beningodesign: +emb-c membership — lead in emb-c (verified by emb-arch)
- beningofw: +emb-c membership — lead in emb-c (verified by emb-arch)
- noblesmallmem: +emb-c membership — lead in emb-c (verified by emb-arch, 2000)
- jplstd: +emb-arch membership — flight-software-standard lead in emb-arch (verified by emb-c)
- drepperlibs: +emb-ops membership — ops unverified lead (verified by emb-c)
- sakscolumns: +emb-c membership — embedded.com column lead in emb-c (also emb-cpp lead)
- lakoslsc: +emb-c membership — physical-design-roots lead in emb-c
- martincleanarch: +emb-c membership — lead in emb-c

## Conflicts / discrepancies

- yiu: year differs across reports (2013 vs 2020 in emb-c); kept 2013, noted
- koopmanbess: year differs across reports (2010 vs 2022 in emb-c); kept 2010, noted
- douglasspatternsc: year differs across reports (2011 vs 2010 in emb-c); kept 2011, noted

## Tag coverage & gaps
- swa-science: cluster/branch/tier/OA on all nodes.
- emb-arch: branch/embedded_relevance/hw_sw_boundary on all; NO theme facet stated (filled in PHASE 2 from report section headings).
- emb-c / emb-cpp: theme/level on all; no tier facet.
- emb-ops: tier(trunk|c-leaf|cpp-leaf)/theme/KEY on all.
- simulink: branch/cluster/role/automotive on all.
- Access/openness only systematically recorded by swa-science (OA flags); elsewhere present in notes only — NOT lifted into a facet (would require re-verification).
- Fields the source flags as unknown carry UNRESOLVED (years of some leads; two swa anchor papers).
