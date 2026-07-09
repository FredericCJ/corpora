# -*- coding: utf-8 -*-
# PHASE 1 fact records — corpus: swe-process (Engineering process & workflow: standards,
# documentation, versioning, review, delivery, project organization).
# Source report: ../../swe_process_corpus_v1_0.md (collected 2026-07-10).
# Raw tags: area | lang | role.  area: standards|documentation|vcs-review|ci-cd|org-build|process.
#           lang: agnostic|matlab|python|c|cpp|multi.  role: anchor|core|advanced|survey (';'-joinable).
# Verification: 'verified' only for works whose primary/authoritative page was loaded live this
# session (by me or a research scout reporting a fetched quote), confirming the exact identifier;
# else 'unverified' with the soft field named in `unres`. No identifier fabricated.
R = []
C = 'swe-process'

def n(id, title, au, yr, typ, area, lang, role, note='', ident='', ver='verified', unres=()):
    """A NEW node this pass grounds (first insertion)."""
    R.append(dict(id=id, corpus=C, title=title, authors=au, year=yr, rtype=typ,
                  verification=ver, note=note, ident=ident, unresolved=list(unres),
                  raw=dict(area=area, lang=lang, role=role)))

def m(id, area, lang, role):
    """MEMBERSHIP of an EXISTING corpus node — REUSES the exact id; PHASE 1 merges by id and
    logs the membership. title/authors/year/rtype/ident are placeholders ignored on merge;
    year='UNRESOLVED' avoids a spurious year-conflict; verification='unverified' can only be
    promoted by (never demote) the node's home-corpus verification."""
    R.append(dict(id=id, corpus=C, title='(membership — see home corpus)', authors='',
                  year='UNRESOLVED', rtype='other', verification='unverified', note='',
                  ident='', unresolved=[], raw=dict(area=area, lang=lang, role=role)))

# ─────────────────────── R1 · coding standards & style ───────────────────────
n('pep8','Style Guide for Python Code (PEP 8)','G. van Rossum, B. Warsaw & A. Coghlan','living','standard',
  'standards','python','anchor','De-facto canonical Python style standard; Active/Process PEP that evolves with the language.','PEP 8; peps.python.org/pep-0008/')
n('pep20','The Zen of Python (PEP 20)','T. Peters','living','standard',
  'standards','python','core','19 aphorisms encoding the design philosophy behind Python style.','PEP 20; peps.python.org/pep-0020/')
n('pep257','Docstring Conventions (PEP 257)','D. Goodger & G. van Rossum','living','standard',
  'standards','python','core','The documentation-string standard; docs-layer counterpart to PEP 8.','PEP 257; peps.python.org/pep-0257/')
n('black','Black — The Uncompromising Code Formatter','Python Software Foundation','living','tooling-doc',
  'standards','python','core','Dominant opinionated auto-formatter; operationalizes PEP 8.','black.readthedocs.io')
n('ruff','Ruff — an extremely fast Python linter and formatter','Astral','living','tooling-doc',
  'standards','python','core','Rust-based; consolidates Flake8/isort/pydocstyle/pyupgrade (+Black); current-generation Python toolchain.','docs.astral.sh/ruff')
n('pylint','Pylint','pylint-dev','living','tooling-doc',
  'standards','python','core','Deep static analyser (errors+style+smells) via astroid inference.','pylint.readthedocs.io')
n('checkcode','checkcode / Code Analyzer (formerly mlint)','MathWorks','living','tooling-doc',
  'standards','matlab','core','Living MATLAB static-analysis/style enforcer; codeIssues is its successor API.','mathworks.com/help/matlab/ref/checkcode.html')
n('pep8eyetracking','Assessing Python Style Guides: An Eye-Tracking Study with Novice Developers','P. Roberto, R. Gheyi, J.A. Silva da Costa & M. Ribeiro','2024','paper',
  'standards','python','advanced','Controlled eye-tracking experiment on four PEP 8 guidelines; mixed benefit — rare Python-specific style-effectiveness evidence.','arXiv:2408.14566')
m('misrac','standards','c','anchor'); m('misracpp2023','standards','cpp','core'); m('autosarcpp14','standards','cpp','core')
m('barrc','standards','c','core'); m('certc','standards','c','core'); m('certcpp','standards','cpp','core')
m('coreguidelines','standards','cpp','anchor'); m('googlestyle','standards','cpp','core'); m('kernelstyle','standards','c','core')
m('jplstd','standards','c','core'); m('boogerdmoonen','standards','c','survey'); m('martincleancode','standards','agnostic','anchor')
m('mcconnell','standards','agnostic','anchor'); m('johnsonbook','standards','matlab','anchor'); m('mab','standards','matlab','core')
m('jmaab','standards','matlab','core'); m('uncrustify','standards','multi','core')

# ─────────────────────── R2 · documentation ───────────────────────
n('diataxis','Diátaxis — a systematic framework for technical documentation','D. Procida','living','guide',
  'documentation','agnostic','anchor','Structures docs by user need: tutorials / how-to / reference / explanation. The documentation anchor.','diataxis.fr')
n('ettermtw','Modern Technical Writing','A. Etter','2016','book',
  'documentation','agnostic','anchor','Seminal concise statement of docs-as-code (lightweight markup, static generators, docs in version control/CI). Companion: Gentle, Docs Like Code (2022, ISBN 978-1-387-53149-3).','ASIN B01A2QL9SS')
n('arc42','arc42 — architecture documentation template','G. Starke & P. Hruschka','living','guide',
  'documentation','agnostic','core','The canonical fill-in architecture-doc template.','arc42.org')
n('c4model','The C4 model for visualising software architecture','S. Brown','living','guide',
  'documentation','agnostic','anchor','De-facto standard for architecture diagramming at layered abstraction (Context/Containers/Components/Code).','c4model.com')
n('nygardadr','Documenting Architecture Decisions','M. Nygard','2011','blog',
  'documentation','agnostic','anchor','Origin of Architecture Decision Records (Title/Context/Decision/Status/Consequences). Living ecosystem: MADR at adr.github.io/madr. Distinct from the Nygard book (id=nygard) already in corpus.','cognitect.com/blog/2011/11/15/documenting-architecture-decisions')
n('sphinx','Sphinx documentation generator','Sphinx team','living','tooling-doc',
  'documentation','multi','core','Keystone doc toolchain (reST/MyST → HTML/PDF/ePub); Python-born hub that C/C++ Breathe/Exhale/Hawkmoth plug into.','sphinx-doc.org')
n('matlabpublish','MATLAB Live Scripts & the publish workflow','MathWorks','living','official-doc',
  'documentation','matlab','core','Vendor-native literate/publishable MATLAB docs (.mlx Live Editor; publish markup → HTML/PDF/LaTeX). The substantive MATLAB doc practice.','mathworks.com/help/matlab/live-scripts-and-functions.html')
m('doxygen','documentation','multi','anchor'); m('parnasclements','documentation','agnostic','anchor')

# ─────────────────────── R3 · version control, branching & review ───────────────────────
n('progit','Pro Git, 2nd ed.','S. Chacon & B. Straub','2014','book',
  'vcs-review','agnostic','anchor','The canonical Git reference; living, community-corrected online edition.','ISBN 978-1-4842-0076-6; git-scm.com/book')
n('gitflow','A successful Git branching model (git-flow)','V. Driessen','2010','blog',
  'vcs-review','agnostic','anchor','Canonical heavyweight branching model; its 2020 note self-defers to GitHub flow for continuous delivery.','nvie.com/posts/a-successful-git-branching-model/')
n('trunkbased','Trunk-Based Development','P. Hammant et al.','living','guide',
  'vcs-review','agnostic','core','Single-branch model; explicitly critiques git-flow and long-lived branches. The CD-era counter-model.','trunkbaseddevelopment.com')
n('githubflow','GitHub flow','GitHub','living','official-doc',
  'vcs-review','agnostic','core','Lightweight PR-centric single-main workflow.','docs.github.com')
n('gitlabflow','GitLab flow','GitLab','living','official-doc',
  'vcs-review','agnostic','core','Environment-branch variant integrating feature development with issue tracking and CD.','about.gitlab.com/topics/version-control/what-is-gitlab-flow/')
n('convcommits','Conventional Commits (v1.0.0)','Conventional Commits community','living','standard',
  'vcs-review','agnostic','core','Commit-message convention that dovetails with SemVer to mechanize release versioning.','conventionalcommits.org')
n('semver','Semantic Versioning (SemVer 2.0.0)','T. Preston-Werner','living','standard',
  'vcs-review','agnostic','anchor','MAJOR.MINOR.PATCH versioning contract release tooling targets.','semver.org')
n('potvinmonorepo','Why Google Stores Billions of Lines of Code in a Single Repository','R. Potvin & J. Levenberg','2016','paper',
  'vcs-review','agnostic','survey','The definitive monorepo industry case; contrasts monorepo vs multi-repo, allied with trunk-based development.','DOI 10.1145/2854146; CACM 59(7):78-87')
n('rigbybird','Convergent Contemporary Software Peer Review Practices','P.C. Rigby & C. Bird','2013','paper',
  'vcs-review','agnostic','survey','Cross-project synthesis showing modern lightweight review converged across OSS + industry.','DOI 10.1145/2491411.2491444')
n('googleeng','Code Review Developer Guide (Google eng-practices)','Google','living','guide',
  'vcs-review','agnostic','core','The de-facto industry review practice guide (reviewer + author guides).','google.github.io/eng-practices/review/')
n('cohenreview','Best Kept Secrets of Peer Code Review','J. Cohen (ed.) et al.','2006','book',
  'vcs-review','agnostic','core','The SmartBear/Cisco review study; bridges Fagan inspection to modern tool-assisted review.','ISBN 978-1-59916-067-2')
m('fagan','vcs-review','agnostic','anchor'); m('wiegers','vcs-review','agnostic','core')
m('bacchellibird','vcs-review','agnostic','core'); m('sadowskigoogle','vcs-review','agnostic','core')
m('modelcompare','vcs-review','matlab','anchor'); m('mergedocs','vcs-review','matlab','core')

# ─────────────────────── R4 · CI/CD & delivery ───────────────────────
n('fowlerci','Continuous Integration','M. Fowler','living','guide',
  'ci-cd','agnostic','anchor','Foundational definition of CI as a practice (2000; rewritten 2006; rev. 2024).','martinfowler.com/articles/continuousIntegration.html')
n('contdeliv','Continuous Delivery','J. Humble & D. Farley','2010','book',
  'ci-cd','agnostic','anchor','Canonical CD text extending CI to the full deployment pipeline.','ISBN 978-0-321-60191-9')
n('accelerate','Accelerate: The Science of Lean Software and DevOps','N. Forsgren, J. Humble & G. Kim','2018','book',
  'ci-cd','agnostic','core','Statistically evaluates which delivery practices (CI, CD, trunk-based) predict performance; the empirical spine.','ISBN 978-1-942788-33-1')
n('dora','DORA — DevOps Research and Assessment / State of DevOps','DORA (Google Cloud)','living','report',
  'ci-cd','agnostic','core','The living research program and Four Keys metrics; Accelerate is its 2018 synthesis.','dora.dev')
n('gitlabci','GitLab CI/CD documentation','GitLab','living','tooling-doc',
  'ci-cd','multi','core','Living reference for a concrete CI/CD engine (.gitlab-ci.yml); companion platform GitHub Actions (docs.github.com/actions).','docs.gitlab.com/ci/')
n('matlabci','Continuous Integration (CI) for MATLAB and Simulink','MathWorks','living','official-doc',
  'ci-cd','matlab','anchor','Umbrella MATLAB-CI hub (Jenkins/GitLab/GitHub Actions/Azure) over the corpus Simulink-CI items.','mathworks.com/solutions/continuous-integration.html')
m('cipart1','ci-cd','matlab','anchor'); m('cipart2','ci-cd','matlab','core'); m('precommit','ci-cd','multi','core')
m('buildtool','ci-cd','matlab','core'); m('matlabtest','ci-cd','matlab','core')

# ─────────────────────── R5 · project organization & build ───────────────────────
n('lakosvol1','Large-Scale C++ Volume I: Process and Architecture','J. Lakos','2019','book',
  'org-build','cpp','anchor','Definitive modern C++ physical design (components/packages/package-groups); 2019 successor to the 1996 book (id=lakoslsc).','ISBN 978-0-201-71706-8')
n('pitchfork','The Pitchfork Layout (PFL)','C. Pike (vector-of-bool)','living','guide',
  'org-build','cpp','core','De-facto community C/C++ directory layout (src/ include/ tests/). Sibling proposal: WG21 P1204R0 Canonical Project Structure (Kolpackov 2018).','github.com/vector-of-bool/pitchfork')
n('profcmake','Professional CMake: A Practical Guide','C. Scott','living','book',
  'org-build','cpp','core','Comprehensive, continuously re-editioned CMake practitioner reference. Free complement: Schreiner, An Introduction to Modern CMake.','crascit.com/professional-cmake/')
n('pypackaging','Python Packaging User Guide','PyPA','living','official-doc',
  'org-build','python','anchor','Authoritative living hub for Python project structure/packaging; parent of src-vs-flat layout guidance and the pyproject PEPs.','packaging.python.org')
n('pep517','PEP 517 — A build-system independent format for source trees','N.J. Smith & T. Kluyver','2015','standard',
  'org-build','python','core','Build-backend hook API decoupling frontends from backends.','PEP 517; peps.python.org/pep-0517/')
n('pep518','PEP 518 — Specifying Minimum Build System Requirements','B. Cannon, N.J. Smith & D. Stufft','2016','standard',
  'org-build','python','anchor','Introduces pyproject.toml and [build-system].requires; the root of declarative Python builds.','PEP 518; peps.python.org/pep-0518/')
n('pep621','PEP 621 — Storing project metadata in pyproject.toml','B. Cannon et al.','2020','standard',
  'org-build','python','core','Standardizes the [project] metadata table across build backends.','PEP 621; peps.python.org/pep-0621/')
n('ieee828','IEEE 828-2012 — Configuration Management in Systems and Software Engineering','IEEE','2012','standard',
  'org-build','agnostic','anchor','Formal process backbone under build/release: CI identification, change control, status accounting, release engineering.','IEEE 828-2012; ISBN 978-0-7381-7134-0')
m('parnas72','org-build','agnostic','anchor'); m('lakoslsc','org-build','cpp','anchor'); m('martincleanarch','org-build','agnostic','core')
m('cmake','org-build','cpp','core'); m('matlabpkg','org-build','matlab','core'); m('projects','org-build','matlab','core')

# ─────────────────────── R6 · process frameworks (lean; periphery tagged) ───────────────────────
n('swebok','Guide to the Software Engineering Body of Knowledge (SWEBOK v4.0)','H. Washizaki (ed.)','2024','guide',
  'process','agnostic','anchor','Consensus field map (18 knowledge areas; v4.0 adds Software Architecture/Operations/Security). The surveying spine.','SWEBOK v4.0; IEEE Computer Society')
n('iso12207','ISO/IEC/IEEE 12207:2017 — Software life cycle processes','ISO/IEC/IEEE','2017','standard',
  'process','agnostic','core','Common framework of software life-cycle processes (acquisition to retirement).','ISO/IEC/IEEE 12207:2017; iso.org/standard/63712.html')
n('agilemanifesto','Manifesto for Agile Software Development','Beck, Fowler, Cunningham, Martin, Schwaber, Sutherland et al. (17 signatories)','2001','other',
  'process','agnostic','anchor','The four values that reframed process priorities; root of the agile lineage.','agilemanifesto.org')
n('xpexplained','Extreme Programming Explained: Embrace Change, 2nd ed.','K. Beck & C. Andres','2004','book',
  'process','agnostic','core','The engineering-practice-heavy agile method (CI, TDD, pairing) closest to this corpus practice focus.','ISBN 978-0-321-27865-4')
n('scrumguide','The Scrum Guide','K. Schwaber & J. Sutherland','living','guide',
  'process','agnostic','core','The canonical, immutable definition of the dominant agile framework (2020; CC BY-SA).','scrumguides.org')
n('humphreypsp','Introduction to the Personal Software Process','W.S. Humphrey','1997','book',
  'process','agnostic','advanced','Individual-discipline process (PSP); team counterpart Introduction to the TSP (1999). The plan-based/measurement periphery.','ISBN 978-0-201-54809-9')

# ─────────────────────── Unverified quarantine ───────────────────────
n('smitconventions','Maintainability and Source Code Conventions: An Analysis of Open Source Projects',
  'M. Smit, B. Gergel, H.J. Hoover & E. Stroulia','2011','report',
  'standards','agnostic','survey','Coding-convention effectiveness study (adherence metric; 71 conventions; four Java projects). Extends the effectiveness cell beyond C/Python.',
  'Univ. of Alberta TR11-06', ver='unverified', unres=['report-number'])
