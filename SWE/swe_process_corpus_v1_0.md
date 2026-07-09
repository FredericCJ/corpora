# SWE Corpus — Pass 7: Engineering Process & Workflow (`swe-process`)

**Scope.** The PROCESS layer of architecture/design/implementation: how teams define code standards, document, use git/GitLab, review, integrate/deliver, and organize projects. Two coverage axes held in tension throughout: **(a) language-agnostic canon** and **(b) language-specific instantiations** for MATLAB, Python, C, C++ (other languages admissible, tagged `multi`/`agnostic`). The knowledge is transposable; the `lang` tag makes the transposition legible and (in the explorer) filterable.

**Collection date:** 2026-07-10. **Rule:** collect-don't-exclude; scope enforced by tags. This pass merges into the existing 6-pass unified corpus by record id — works already carried by another pass are **memberships** (they REUSE the exact existing id; PHASE 1 logs the membership), not new nodes.

## Tag legend

- `area:` standards | documentation | vcs-review | ci-cd | org-build | process
- `lang:` agnostic | matlab | python | c | cpp | multi — the transposition axis. `agnostic` = language-independent method; `multi` = a tool/standard spanning several languages.
- `role:` anchor | core | advanced | survey — the report's own emphasis (anchors are the entry points surfaced in the Anchors model).
- `verification:` **verified** = a primary or authoritative page (publisher / standards body / project site / ACM/IEEE/python.org catalog) was loaded live this session (by me or a research scout reporting a fetched quote), confirming the exact identifier; **unverified** = recall/search-index only, with the soft field named in an `UNRESOLVED` note. No DOI/ISBN/year is fabricated — omitted sooner than guessed.

Entry format: **Title** — authors/body, year. Venue. Identifier. `{area | lang | role | verification}` — relevance note. Memberships are prefixed `[MEMBERSHIP id=…]` and carry only the swe-process tags + why the process lens claims them; their citation lives in the corpus already.

---

## R1. Coding standards & style

### New

1. **Style Guide for Python Code (PEP 8)** — G. van Rossum, B. Warsaw, A. Coghlan, living (created 2001). python.org. PEP 8 / https://peps.python.org/pep-0008/. `{standards | python | anchor | verified}` — The de-facto canonical Python style standard; "Active/Process" PEP that "evolves over time." The Python anchor for the standards cell.
2. **The Zen of Python (PEP 20)** — T. Peters, living (2004). python.org. PEP 20 / https://peps.python.org/pep-0020/. `{standards | python | core | verified}` — 19 aphorisms encoding the design philosophy behind Python style choices.
3. **Docstring Conventions (PEP 257)** — D. Goodger, G. van Rossum, living (2001). python.org. PEP 257 / https://peps.python.org/pep-0257/. `{standards | python | core | verified}` — The documentation-string standard; the docs-layer counterpart to PEP 8.
4. **Black — The Uncompromising Code Formatter** — Python Software Foundation, living. black.readthedocs.io. `{standards | python | core | verified}` — Dominant opinionated auto-formatter; operationalizes PEP 8 by removing style debate.
5. **Ruff — an extremely fast Python linter and formatter** — Astral, living. docs.astral.sh/ruff. `{standards | python | core | verified}` — Rust-based; "10–100× faster than existing linters," consolidating Flake8/isort/pydocstyle/pyupgrade and (optionally) Black — the current-generation Python toolchain.
6. **Pylint** — pylint-dev, living. pylint.readthedocs.io. `{standards | python | core | verified}` — Deep static analyser (errors + style + smells) via astroid inference; the thorough end of the Python linter spectrum.
7. **checkcode / Code Analyzer (formerly mlint)** — MathWorks, living. https://www.mathworks.com/help/matlab/ref/checkcode.html. `{standards | matlab | core | verified}` — The living MATLAB static-analysis/style enforcer ("report potential problems and opportunities for code improvement"); `codeIssues` is its successor API. The MATLAB tooling counterpart to the MATLAB style books.
8. **Assessing Python Style Guides: An Eye-Tracking Study with Novice Developers** — P. Roberto, R. Gheyi, J. A. Silva da Costa, M. Ribeiro, 2024. arXiv. arXiv:2408.14566. `{standards | python | advanced | verified}` — Controlled experiment (32 novices, eye-tracking) on four PEP 8 guidelines; finds mixed benefit (2 of 4 showed no/negative effect) — rare Python-specific empirical style-effectiveness evidence.

### Membership (existing works, reclaimed under the standards lens)

9. **[MEMBERSHIP id=misrac]** `{standards | c | anchor | verified}` — MISRA C: the reference safety-critical C rule set; the standards anchor for the C cell.
10. **[MEMBERSHIP id=misracpp2023]** `{standards | cpp | core | verified}` — MISRA C++:2023 (merges AUTOSAR C++14); the current C++ safety standard.
11. **[MEMBERSHIP id=autosarcpp14]** `{standards | cpp | core | verified}` — AUTOSAR C++14 guidelines; traceable to HIC++/JSF/CERT/Core Guidelines/MISRA lineage.
12. **[MEMBERSHIP id=barrc]** `{standards | c | core | verified}` — BARR-C:2018 embedded-C standard, harmonized with MISRA C.
13. **[MEMBERSHIP id=certc]** `{standards | c | core | verified}` — SEI CERT C secure-coding standard.
14. **[MEMBERSHIP id=certcpp]** `{standards | cpp | core | verified}` — SEI CERT C++ secure-coding standard (builds on CERT C).
15. **[MEMBERSHIP id=coreguidelines]** `{standards | cpp | anchor | verified}` — ISO C++ Core Guidelines (Stroustrup & Sutter); the modern C++ style anchor.
16. **[MEMBERSHIP id=googlestyle]** `{standards | cpp | core | verified}` — Google C++ Style Guide; the most-emulated corporate style.
17. **[MEMBERSHIP id=kernelstyle]** `{standards | c | core | verified}` — Linux kernel coding style; the archetypal project-scale C convention.
18. **[MEMBERSHIP id=jplstd]** `{standards | c | core | verified}` — NASA/JPL Institutional Coding Standard for C (embeds the Power of Ten rules).
19. **[MEMBERSHIP id=boogerdmoonen]** `{standards | c | survey | verified}` — Empirical study of coding-standard (MISRA C) effectiveness — the C-instantiated effectiveness anchor.
20. **[MEMBERSHIP id=martincleancode]** `{standards | agnostic | anchor | verified}` — Clean Code (Martin); the agnostic craftsmanship canon.
21. **[MEMBERSHIP id=mcconnell]** `{standards | agnostic | anchor | verified}` — Code Complete, 2nd ed. (McConnell); the construction-practice reference.
22. **[MEMBERSHIP id=johnsonbook]** `{standards | matlab | anchor | verified}` — The Elements of MATLAB Style (Johnson); the MATLAB style anchor.
23. **[MEMBERSHIP id=mab]** `{standards | matlab | core | verified}` — MAB Control Algorithm Modeling Guidelines; model-level "style" for Simulink/MATLAB.
24. **[MEMBERSHIP id=jmaab]** `{standards | matlab | core | verified}` — JMAAB guidelines feeding the MAB lineage.
25. **[MEMBERSHIP id=uncrustify]** `{standards | multi | core | verified}` — Multi-language source beautifier (C/C++/etc.); the agnostic-tooling formatter.

---

## R2. Documentation

### New

26. **Diátaxis — a systematic framework for technical documentation** — D. Procida, living. diataxis.fr. https://diataxis.fr. `{documentation | agnostic | anchor | verified}` — The dominant modern model for *structuring* docs by user need: tutorials, how-to guides, reference, explanation. The documentation anchor.
27. **Modern Technical Writing** — A. Etter, 2016. Self-published. ASIN B01A2QL9SS. `{documentation | agnostic | anchor | verified}` — The seminal concise statement of the *docs-as-code* philosophy (lightweight markup, static generators, version control, docs in CI). Practical companion: A. Gentle, *Docs Like Code*, 3rd ed. 2022 (ISBN 978-1-387-53149-3).
28. **arc42 — architecture documentation template** — G. Starke & P. Hruschka, living. arc42.org. https://arc42.org. `{documentation | agnostic | core | verified}` — The canonical fill-in architecture-doc template ("construct, communicate and document your software architecture").
29. **The C4 model for visualising software architecture** — S. Brown, living. c4model.com. https://c4model.com. `{documentation | agnostic | anchor | verified}` — The de-facto standard for architecture *diagramming* at layered abstraction (Context, Containers, Components, Code); pairs with arc42 (prose) and ADRs (decisions).
30. **Documenting Architecture Decisions** — M. Nygard, 2011. Cognitect/ThinkRelevance blog. https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions. `{documentation | agnostic | anchor | verified}` — The origin of Architecture Decision Records (Title/Context/Decision/Status/Consequences). Distinct node from the Nygard *Release It!* book already in corpus. Living ecosystem: MADR templates at adr.github.io/madr.
31. **Sphinx documentation generator** — Sphinx team, living. sphinx-doc.org. https://www.sphinx-doc.org. `{documentation | multi | core | verified}` — The keystone doc *toolchain* (reStructuredText + MyST → HTML/PDF/ePub); Python-born but the hub that C/C++ Breathe/Exhale/Hawkmoth plug into — the bridge from agnostic practice to language tooling.
32. **MATLAB Live Scripts & the `publish` workflow** — MathWorks, living. https://www.mathworks.com/help/matlab/live-scripts-and-functions.html. `{documentation | matlab | core | verified}` — The substantive MATLAB-specific documentation practice: vendor-native literate/publishable docs (`.mlx` Live Editor; `publish` markup → HTML/PDF/LaTeX).

### Membership

33. **[MEMBERSHIP id=doxygen]** `{documentation | multi | anchor | verified}` — Doxygen; the dominant C/C++ (and multi-language) API-doc generator.
34. **[MEMBERSHIP id=parnasclements]** `{documentation | agnostic | anchor | verified}` — "A Rational Design Process: How and Why to Fake It" (Parnas & Clements 1986) — the intellectual root of writing *design/decision* documentation after the fact; bridges R2 and R5.

---

## R3. Version control, branching & code review

### New

35. **Pro Git, 2nd ed.** — S. Chacon & B. Straub, 2014 (living online). Apress. ISBN 978-1-4842-0076-6 / git-scm.com/book. `{vcs-review | agnostic | anchor | verified}` — The canonical Git reference; the living, community-corrected edition. Anchor for the VCS route.
36. **A successful Git branching model (git-flow)** — V. Driessen, 2010. nvie.com. https://nvie.com/posts/a-successful-git-branching-model/. `{vcs-review | agnostic | anchor | verified}` — The canonical heavyweight branching model (master/develop/feature/release/hotfix). Its 2020 author's note self-critiques: for continuous delivery, "adopt a much simpler workflow (like GitHub flow)."
37. **Trunk-Based Development** — P. Hammant et al., living. trunkbaseddevelopment.com. `{vcs-review | agnostic | core | verified}` — Single-branch model that explicitly **critiques** git-flow ("do TBD instead of GitFlow… multiple long-running branches"); the CD-era counter-model.
38. **GitHub flow** — GitHub, living. docs.github.com. `{vcs-review | agnostic | core | verified}` — Lightweight PR-centric single-`main` workflow; the mainstream simplification git-flow's own note defers to.
39. **GitLab flow** — GitLab, living. about.gitlab.com/topics/version-control/what-is-gitlab-flow/. `{vcs-review | agnostic | core | verified}` — Environment-branch variant integrating feature-driven development with issue tracking and CD.
40. **Conventional Commits (v1.0.0)** — Conventional Commits community, living. conventionalcommits.org. `{vcs-review | agnostic | core | verified}` — Commit-message convention (fix→PATCH, feat→MINOR, BREAKING CHANGE→MAJOR) that "dovetails with SemVer" to mechanize release versioning.
41. **Semantic Versioning (SemVer 2.0.0)** — T. Preston-Werner, living. semver.org. `{vcs-review | agnostic | anchor | verified}` — The MAJOR.MINOR.PATCH versioning contract that release tooling and Conventional Commits target.
42. **Why Google Stores Billions of Lines of Code in a Single Repository** — R. Potvin & J. Levenberg, 2016. *Communications of the ACM* 59(7):78–87. DOI 10.1145/2854146. `{vcs-review | agnostic | survey | verified}` — The definitive monorepo industry case (~1B files, ~2B LOC); contrasts monorepo vs multi-repo, allied with trunk-based development.
43. **Convergent Contemporary Software Peer Review Practices** — P. C. Rigby & C. Bird, 2013. ESEC/FSE 2013, pp. 202–212. DOI 10.1145/2491411.2491444. `{vcs-review | agnostic | survey | verified}` — Cross-project synthesis showing modern lightweight review converged independently across OSS + industry; complements Bacchelli & Bird and the Google case study.
44. **Code Review Developer Guide (Google eng-practices)** — Google, living. google.github.io/eng-practices/review/. `{vcs-review | agnostic | core | verified}` — The de-facto industry practice guide (reviewer + author guides); operationalizes what the Google case study measures.
45. **Best Kept Secrets of Peer Code Review** — J. Cohen (ed.) et al., 2006. Smart Bear Inc. ISBN 978-1-59916-067-2. `{vcs-review | agnostic | core | verified}` — The SmartBear/Cisco "largest code review study" — the bridge from Fagan formal inspection to modern lightweight, tool-assisted review.

### Membership

46. **[MEMBERSHIP id=fagan]** `{vcs-review | agnostic | anchor | verified}` — Fagan, "Design and Code Inspections" (1976) — the root of software inspection/review.
47. **[MEMBERSHIP id=wiegers]** `{vcs-review | agnostic | core | verified}` — Peer Reviews in Software (Wiegers); the practitioner bridge from formal to lightweight review.
48. **[MEMBERSHIP id=bacchellibird]** `{vcs-review | agnostic | core | verified}` — "Expectations, Outcomes, and Challenges of Modern Code Review" (ICSE 2013).
49. **[MEMBERSHIP id=sadowskigoogle]** `{vcs-review | agnostic | core | verified}` — "Modern Code Review: A Case Study at Google" (ICSE-SEIP 2018).
50. **[MEMBERSHIP id=modelcompare]** `{vcs-review | matlab | anchor | verified}` — Simulink Comparison/Three-Way Merge tooling — the only genuinely language-specific slice (binary models need specialized diff/merge).
51. **[MEMBERSHIP id=mergedocs]** `{vcs-review | matlab | core | verified}` — Resolve Conflicts via Simulink Three-Way Merge / external source-control integration (`mlDiff`/`mlMerge`).

---

## R4. CI/CD & delivery

### New

52. **Continuous Integration** — M. Fowler, living (2000; rewritten 2006; rev. 2024). martinfowler.com. https://martinfowler.com/articles/continuousIntegration.html. `{ci-cd | agnostic | anchor | verified}` — The foundational definition of CI as a practice; the origin node of the delivery route.
53. **Continuous Delivery** — J. Humble & D. Farley, 2010. Addison-Wesley. ISBN 978-0-321-60191-9. `{ci-cd | agnostic | anchor | verified}` — Canonical CD text extending CI to the full deployment pipeline (2011 Jolt Award).
54. **Accelerate: The Science of Lean Software and DevOps** — N. Forsgren, J. Humble & G. Kim, 2018. IT Revolution. ISBN 978-1-942788-33-1. `{ci-cd | agnostic | core | verified}` — Statistically **evaluates** which delivery practices (CI, CD, trunk-based) predict performance; the empirical spine of the route.
55. **DORA — DevOps Research and Assessment / State of DevOps** — DORA (Forsgren/Humble/Kim → Google Cloud), living. dora.dev. `{ci-cd | agnostic | core | verified}` — The ongoing research program and Four Keys metrics (deployment frequency, lead time, change-fail rate, restore time); Accelerate is its 2018 synthesis.
56. **GitLab CI/CD documentation** — GitLab, living. docs.gitlab.com/ci/. `{ci-cd | multi | core | verified}` — Living reference for a concrete CI/CD engine (`.gitlab-ci.yml`); the platform the corpus's Simulink `cipart2` applies. Companion platform: GitHub Actions (docs.github.com/actions).
57. **Continuous Integration (CI) for MATLAB and Simulink** — MathWorks, living. https://www.mathworks.com/solutions/continuous-integration.html. `{ci-cd | matlab | anchor | verified}` — The umbrella MATLAB-CI hub (Jenkins/GitLab/GitHub Actions/Azure) under which the corpus's Simulink CI items sit; the language-specific CI anchor.

### Membership

58. **[MEMBERSHIP id=cipart1]** `{ci-cd | matlab | anchor | verified}` — CI for Verification of Simulink Models (Part 1).
59. **[MEMBERSHIP id=cipart2]** `{ci-cd | matlab | core | verified}` — CI for Simulink Models using GitLab (Part 2).
60. **[MEMBERSHIP id=precommit]** `{ci-cd | multi | core | verified}` — pre-commit hook framework; language-agnostic local quality gate.
61. **[MEMBERSHIP id=buildtool]** `{ci-cd | matlab | core | verified}` — MATLAB `buildtool` build/test automation (R2022b).
62. **[MEMBERSHIP id=matlabtest]** `{ci-cd | matlab | core | verified}` — MATLAB Test (MC/DC for MATLAB code).

---

## R5. Project organization & build

### New

63. **Large-Scale C++ Volume I: Process and Architecture** — J. Lakos, 2019. Addison-Wesley. ISBN 978-0-201-71706-8. `{org-build | cpp | anchor | verified}` — The definitive modern treatment of C++ physical design (components/packages/package-groups); the 2019 successor to Lakos's 1996 book (see membership id=lakoslsc, which this pass disambiguates to 1996).
64. **The Pitchfork Layout (PFL)** — C. Pike (vector-of-bool), living. github.com/vector-of-bool/pitchfork. `{org-build | cpp | core | verified}` — The de-facto community directory layout (`src/ include/ tests/…`) for native C/C++. Sibling/rival: WG21 **P1204R0** "Canonical Project Structure" (B. Kolpackov, 2018, open-std.org).
65. **Professional CMake: A Practical Guide** — C. Scott, living/editioned (1st ed. 2018 →). Crascit. crascit.com/professional-cmake/. `{org-build | cpp | core | verified}` — The comprehensive CMake practitioner reference, continuously re-editioned. Free complement: H. Schreiner, *An Introduction to Modern CMake* (cliutils.gitlab.io/modern-cmake).
66. **Python Packaging User Guide** — PyPA, living. packaging.python.org. `{org-build | python | anchor | verified}` — The authoritative living hub for Python project structure/packaging; parent of the src-vs-flat layout guidance and the pyproject PEP toolchain.
67. **PEP 517 — A build-system independent format for source trees** — N. J. Smith & T. Kluyver, 2015. python.org. PEP 517. `{org-build | python | core | verified}` — Defines the build-backend hook API decoupling frontends from backends.
68. **PEP 518 — Specifying minimum build system requirements** — B. Cannon, N. J. Smith, D. Stufft, 2016. python.org. PEP 518. `{org-build | python | anchor | verified}` — Introduces `pyproject.toml` and `[build-system].requires`; the root of declarative Python builds.
69. **PEP 621 — Storing project metadata in pyproject.toml** — B. Cannon et al., 2020. python.org. PEP 621. `{org-build | python | core | verified}` — Standardizes the `[project]` metadata table across build backends.
70. **IEEE 828-2012 — Configuration Management in Systems and Software Engineering** — IEEE, 2012. IEEE SA. IEEE 828-2012; ISBN 978-0-7381-7134-0. `{org-build | agnostic | anchor | verified}` — The formal process backbone under build/release: CI identification, change control, status accounting, build & release engineering.

### Membership

71. **[MEMBERSHIP id=parnas72]** `{org-build | agnostic | anchor | verified}` — Parnas, "On the Criteria To Be Used in Decomposing Systems into Modules" (1972) — the modularity/information-hiding root that the physical-design and clean-architecture literature builds on.
72. **[MEMBERSHIP id=lakoslsc]** `{org-build | cpp | anchor | verified}` — Large-Scale C++ Software Design (1996); the physical-design foundation (this pass grounds its year as 1996, distinct from Vol. I 2019).
73. **[MEMBERSHIP id=martincleanarch]** `{org-build | agnostic | core | verified}` — Clean Architecture (Martin); component principles/boundaries building on Parnas.
74. **[MEMBERSHIP id=cmake]** `{org-build | cpp | core | verified}` — CMake documentation; the dominant C/C++ build organizer.
75. **[MEMBERSHIP id=matlabpkg]** `{org-build | matlab | core | verified}` — MATLAB packages/namespaces + Toolbox (`.mltbx`) packaging.
76. **[MEMBERSHIP id=projects]** `{org-build | matlab | core | verified}` — MATLAB/Simulink Projects (project management + version-control integration).

---

## R6. Process frameworks (kept lean; periphery tagged as such)

### New

77. **Guide to the Software Engineering Body of Knowledge (SWEBOK v4.0)** — H. Washizaki (ed.), 2024. IEEE Computer Society. SWEBOK v4.0. `{process | agnostic | anchor | verified}` — The consensus field map (18 knowledge areas; v4.0 added Software Architecture, Operations, Security); the surveying spine of the whole corpus.
78. **ISO/IEC/IEEE 12207:2017 — Software life cycle processes** — ISO/IEC/IEEE, 2017. iso.org/standard/63712.html. `{process | agnostic | core | verified}` — The common framework of software life-cycle processes (acquisition→retirement); the standards backbone for process definition.
79. **Manifesto for Agile Software Development** — Beck, Fowler, Cunningham, Martin, Schwaber, Sutherland et al. (17 signatories), 2001. agilemanifesto.org. `{process | agnostic | anchor | verified}` — The four values that reframed process priorities; the root of the agile lineage (XP, Scrum below).
80. **Extreme Programming Explained: Embrace Change, 2nd ed.** — K. Beck & C. Andres, 2004. Addison-Wesley. ISBN 978-0-321-27865-4. `{process | agnostic | core | verified}` — The engineering-practice-heavy agile method (CI, TDD, pair programming, collective ownership) closest to this corpus's practice focus.
81. **The Scrum Guide** — K. Schwaber & J. Sutherland, 2020 (living). scrumguides.org. `{process | agnostic | core | verified}` — The canonical, immutable definition of the dominant agile framework (CC BY-SA).
82. **Introduction to the Personal Software Process** — W. S. Humphrey, 1997. Addison-Wesley / SEI. ISBN 978-0-201-54809-9. `{process | agnostic | advanced | verified}` — Individual-discipline process (PSP), with the team counterpart *Introduction to the Team Software Process* (1999); the measurement-driven, plan-based periphery of the agile spectrum.

---

## Unverified quarantine

Real, on-scope, but not primary-confirmed this session — do not cite the soft field downstream without live verification.

- **U1. Maintainability and Source Code Conventions: An Analysis of Open Source Projects** — M. Smit, B. Gergel, H. J. Hoover, E. Stroulia, 2011. Univ. of Alberta Tech. Report TR11-06. `{standards | agnostic | survey | unverified}` — A coding-convention effectiveness study (adherence metric; 71 conventions ranked; four Java projects). **UNRESOLVED:** exact report number/venue (search-index corroborated; direct PDF/SPA blocked). Would extend the effectiveness cell beyond C (Boogerd & Moonen) and Python (arXiv:2408.14566).

---

## Area × language coverage matrix

Cell content = where real literature exists; **GAP** = honestly empty (recorded, not padded). New nodes in **bold-ish**; others are memberships.

| area \ lang | agnostic | c | cpp | python | matlab |
|---|---|---|---|---|---|
| **standards** | martincleancode, mcconnell, uncrustify(multi); *effectiveness:* smitconventions(U) | misrac, barrc, certc, kernelstyle, jplstd; *eff:* boogerdmoonen | coreguidelines, misracpp2023, autosarcpp14, certcpp, googlestyle; *eff:* **GAP** | pep8, pep20, pep257 + black, ruff, pylint; *eff:* pep8eyetracking | johnsonbook, mab, jmaab + checkcode; *eff:* **GAP** |
| **documentation** | diataxis, arc42, c4model, nygardadr, ettermtw, parnasclements | doxygen, (breathe/hawkmoth/gtkdoc leads) | doxygen, (breathe/exhale leads) | sphinx (multi) | matlabpublish |
| **vcs-review** | progit, gitflow, trunkbased, githubflow, gitlabflow, convcommits, semver, potvinmonorepo, fagan, wiegers, bacchellibird, sadowskigoogle, rigbybird, googleeng, cohenreview | *review:* GAP (C appears only as study subject) | *review:* GAP | *review:* GAP | modelcompare, mergedocs (diff/merge tooling only) |
| **ci-cd** | fowlerci, contdeliv, accelerate, dora, gitlabci(multi) | GAP (generic pipeline) | GAP (generic pipeline) | precommit(multi, ecosystem-born) | matlabci, cipart1, cipart2, buildtool, matlabtest |
| **org-build** | parnas72, martincleanarch, ieee828 | GAP (real hole — no C-first layout/build anchor) | lakoslsc, lakosvol1, cmake, pitchfork, profcmake | pypackaging, pep517, pep518, pep621 | matlabpkg, projects |
| **process** | swebok, iso12207, agilemanifesto, xpexplained, scrumguide, humphreypsp | — | — | — | — |

## Coverage summary — where recall thins (honest gaps)

- **Process knowledge is overwhelmingly language-agnostic; language-specificity lives in tooling and org-build, not method.** Documentation *practice* (Diátaxis, arc42, C4, ADR, docs-as-code), code review, CI/CD concepts, and process frameworks carry no language binding. The transposition the mission asks for is therefore mostly **agnostic-method + language-specific-tooling**, and the tags say so.
- **Empirical style-effectiveness is language-skewed:** real evidence exists only for **C** (Boogerd & Moonen), **Python** (arXiv:2408.14566), and **agnostic/Java** (Smit, unverified). **C++ and MATLAB have no style-effectiveness study** despite the densest (C++) and a vendor-rich (MATLAB) prescriptive shelf — a genuine, unavoidable gap, not a search failure.
- **Code review has no MATLAB/Python/C/C++-specific *research*.** It is a human-factors discipline; language projects appear only as *subjects inside agnostic studies* (Rigby & Bird cover the Linux-kernel C email-review process; the Google studies describe a C++/Java codebase). The only language-specific *review* slice is MATLAB/Simulink **diff/merge tooling** (binary models can't use text diff).
- **C is the standout org-build hole:** no C-first project-layout/build anchor (Pitchfork/CMake bleed over from C++). Candidate fills for a future sweep: GNU Autotools/Automake, GNU Coding Standards (directory layout), pkg-config conventions.
- **Build-system *theory* is thin** across all languages (only CMake, C++-leaning). A future agnostic anchor candidate: Mokhov, Mitchell & Peyton Jones, "Build Systems à la Carte" (ICFP 2018).
- **MATLAB documentation and effectiveness are vendor-locked/absent:** the only MATLAB doc-practice is MathWorks' own (`publish`/Live Scripts); no independent MATLAB documentation-practice or style-effectiveness literature surfaced.
- **Python carries the language-specific weight**: it is the one language with native *practice* leadership (PEP culture; Diátaxis emerged there) **and** rich tooling (Sphinx, Black/Ruff/Pylint, PyPA/pyproject). If one language must instantiate "language-specific process," it is Python.
- **Routes stopped at the <3-in-scope-finds floor:** R6 was deliberately kept lean (periphery like PSP/TSP tagged `advanced`); no route was padded past genuine literature.
