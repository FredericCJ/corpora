# SWE Corpus — Pass 7 (`swe-process`) Expansion Report — 2026-07-10

Added a seventh research pass, **Engineering Process & Workflow**, to the unified SWE corpus: the
PROCESS layer of architecture/design/implementation — coding standards, documentation, version
control & review, CI/CD & delivery, project organization & build, and process frameworks — held
across two axes, **language-agnostic canon** and **language-specific instantiation** (MATLAB /
Python / C / C++), made legible by a new `lang` facet.

## Headline counts

| | before | after | delta |
|---|---|---|---|
| nodes | 421 | **468** | **+47 new** |
| corpora | 6 | **7** | +1 (`swe-process`) |
| swe-process memberships (nodes tagged into the pass) | — | **95** | 47 new + 36 full memberships + 12 lead memberships |
| cross-corpus (graft) nodes | 44¹ | **82** | +38 |
| typed edges | 204¹ | **261** | +57 (49 `report:proc` + 8 `editorial`) |
| verified / unverified | 308 / 113 | **354 / 114** | +46 verified, +1 unverified (smitconventions) |

¹ the README's pre-existing "44 / 84 UNRESOLVED / 204" figures were stale from an earlier corpus
state; the build is authoritative (82 cross-corpus, 65 UNRESOLVED, 204→261 edges).

**Merged-vs-new discipline.** The corpus already carried a large slice of the process literature,
so most of R1's standards, the documentation tools, the review classics, the Simulink CI/merge
tooling, and the modularity roots are **memberships** (they REUSE the exact existing id; PHASE 1
merges by id and logs it), not new nodes. Only genuinely absent works became new nodes — almost the
entire Python, git-workflow, CI/CD-canon, and process-framework literature.

## Per-route yield

| Route | new nodes | full memberships | lead memberships | key gap |
|---|---|---|---|---|
| **R1 standards & style** | 8 (PEP 8/20/257, Black, Ruff, Pylint, checkcode, PEP8-eyetracking) | 17 (misrac, misracpp2023, autosarcpp14, barrc, certc/cpp, coreguidelines, googlestyle, kernelstyle, jplstd, boogerdmoonen, martincleancode, mcconnell, johnsonbook, mab, jmaab, uncrustify) | 6 (misracpp2008, johnsonguide, mwcodingguide, osstyleguides, hicpp, jsfav) | no C++ or MATLAB style-*effectiveness* study |
| **R2 documentation** | 7 (Diátaxis, Etter, arc42, C4, ADR/Nygard, Sphinx, MATLAB publish) | 2 (doxygen, parnasclements) | 4 (breathe, exhale, hawkmoth, gtkdoc) | doc *practice* is agnostic; C/C++ = tooling only; MATLAB = vendor-locked |
| **R3 version control & review** | 11 (Pro Git, git-flow, trunk-based, GitHub/GitLab flow, Conventional Commits, SemVer, monorepo, Rigby-Bird, Google eng-practices, Cohen) | 6 (fagan, wiegers, bacchellibird, sadowskigoogle, modelcompare, mergedocs) | 1 (guyblog) | no per-language *review research*; only MATLAB diff/merge tooling |
| **R4 CI/CD & delivery** | 6 (Fowler CI, Continuous Delivery, Accelerate, DORA, GitLab CI, MATLAB CI) | 5 (cipart1, cipart2, precommit, buildtool, matlabtest) | 1 (sltest) | canon agnostic; strongest language-specific slice is MATLAB/Simulink |
| **R5 project org & build** | 8 (Lakos Vol I, Pitchfork, Professional CMake, PyPA guide, PEP 517/518/621, IEEE 828) | 6 (parnas72, lakoslsc, martincleanarch, cmake, matlabpkg, projects) | 0 | **C** has no C-first layout/build anchor (real hole) |
| **R6 process frameworks** | 6 (SWEBOK v4, ISO 12207, Agile Manifesto, XP Explained, Scrum Guide, Humphrey PSP/TSP) | 0 | 0 | kept lean; periphery (PSP/TSP) tagged `advanced` |
| **Quarantine** | 1 unverified (smitconventions, TR11-06) | — | — | effectiveness-study identifier unconfirmed |

Total: **47 new** + **36 full memberships** + **12 leads** = **95** swe-process members. Every new
work was verified against a primary or authoritative page loaded live this session (five parallel
route scouts + direct fetches for R6); the one node whose identifier could not be primary-confirmed
(smitconventions) is `unverified` with `UNRESOLVED: report-number` and quarantined in the report.

## Edge additions (57) by kind

`companion` 16 · `prerequisite-of` 7 · `refines` 6 · `applies-method-of` 6 · `references` 5 ·
`critiques` 5 · `part-of` 5 · `surveys` 4 · `evaluates` 3. By provenance: **49 `report:proc`**
(relations the pass's report states) + **8 `editorial`** (reasoned judgment, rendered dotted).
Representative wirings, per the mission's spine:

- `trunkbased` **critiques** `gitflow` (and `githubflow`/`gitlabflow` critique it too — the CD-era branching argument).
- `accelerate` **evaluates** `contdeliv` + `fowlerci`; `dora` **companion** `accelerate` (the empirical DevOps engine).
- `coreguidelines` **companion** `misracpp2023` (parallel modern-C++ guideline lineage).
- `parnas72` **prerequisite-of** `lakosvol1` + `martincleanarch`; `lakoslsc` **prerequisite-of** `lakosvol1` (the modularity → physical-design spine).
- `swebok` **surveys** `iso12207`, `ieee828`, `agilemanifesto`, `contdeliv`; `scrumguide`/`xpexplained` **refine** `agilemanifesto`.
- `cipart1/cipart2/sltest/buildtool/matlabtest` **part-of** `matlabci`; `cipart1` **applies-method-of** `fowlerci` — binding the MATLAB CI cluster to the agnostic CI canon.

## Area × language coverage matrix (with honest gaps)

| area \ lang | agnostic | c | cpp | python | matlab |
|---|---|---|---|---|---|
| **standards** | martincleancode, mcconnell, uncrustify; *eff:* smitconventions(U) | misrac, barrc, certc, kernelstyle, jplstd; *eff:* boogerdmoonen | coreguidelines, misracpp2023, autosarcpp14, certcpp, googlestyle; *eff:* **GAP** | pep8/20/257, black, ruff, pylint; *eff:* pep8eyetracking | johnsonbook, mab, jmaab, checkcode; *eff:* **GAP** |
| **documentation** | diataxis, arc42, c4model, nygardadr, ettermtw, parnasclements | doxygen (+leads) | doxygen (+leads) | sphinx | matlabpublish |
| **vcs-review** | progit, gitflow, trunkbased, githubflow, gitlabflow, convcommits, semver, potvinmonorepo, fagan, wiegers, bacchellibird, sadowskigoogle, rigbybird, googleeng, cohenreview | **GAP** (subject only) | **GAP** | **GAP** | modelcompare, mergedocs (diff/merge) |
| **ci-cd** | fowlerci, contdeliv, accelerate, dora, gitlabci | GAP | GAP | precommit | matlabci, cipart1/2, buildtool, matlabtest |
| **org-build** | parnas72, martincleanarch, ieee828 | **GAP (real hole)** | lakoslsc, lakosvol1, cmake, pitchfork, profcmake | pypackaging, pep517/518/621 | matlabpkg, projects |
| **process** | swebok, iso12207, agilemanifesto, xpexplained, scrumguide, humphreypsp | — | — | — | — |

**The structural finding:** process knowledge is overwhelmingly **agnostic-method + language-specific-tooling**. Empirical *effectiveness* evidence exists only for C (Boogerd-Moonen), Python (eye-tracking), and Java/agnostic (Smit, unverified) — **C++ and MATLAB have none**. *Code review* has no per-language research (languages appear only as study subjects). **C is the real org-build hole** (no C-first layout/build anchor). **Python** carries the language-specific weight — the one language with native practice leadership *and* rich tooling. Full gap analysis in `swe_process_corpus_v1_0.md` §Coverage summary.

## Top-10 reading list — "set up process for a mixed MATLAB/Python/C/C++ team"

Ordered as a setup sequence; the shared agnostic backbone first, then the per-language instantiations (the transposition in action).

1. **SWEBOK v4.0** (`swebok`) — orient: the field map that tells you which process areas exist and how they interlock.
2. **Pro Git** (`progit`) — the one substrate the whole mixed team shares; establish fluency before choosing a workflow.
3. **Trunk-Based Development** (`trunkbased`) vs **git-flow** (`gitflow`) — pick a branching model deliberately; for CI/CD, trunk-based (git-flow's own author now defers to lighter flows).
4. **Continuous Delivery** (`contdeliv`) + **Accelerate** (`accelerate`) — the delivery pipeline and the evidence that these practices actually predict performance.
5. **Google Code Review Developer Guide** (`googleeng`) — a concrete, language-agnostic review practice the team can adopt on day one.
6. **Diátaxis** (`diataxis`) + **Documenting Architecture Decisions / ADRs** (`nygardadr`) — how to structure docs and capture decisions, independent of language.
7. **Conventional Commits** (`convcommits`) + **Semantic Versioning** (`semver`) — release discipline that mechanizes versioning across every repo.
8. **Coding standards, transposed** — **BARR-C / MISRA C** (`barrc`/`misrac`) for C, **C++ Core Guidelines** (`coreguidelines`) for C++, **PEP 8 + Ruff** (`pep8`/`ruff`) for Python, **Elements of MATLAB Style + Code Analyzer** (`johnsonbook`/`checkcode`) for MATLAB — one standard per language, all enforced in review/CI.
9. **Project organization, transposed** — **PyPA Packaging Guide + pyproject PEPs** (`pypackaging`/`pep518`) for Python, **Lakos Vol I + Professional CMake** (`lakosvol1`/`profcmake`) for C++, **MATLAB Projects + toolbox packaging** (`projects`/`matlabpkg`) for MATLAB. (C has no first-class anchor — use CMake + Pitchfork.)
10. **IEEE 828** (`ieee828`) — the configuration-management umbrella that ties versioning, build, and release into an auditable process (essential if any of the C/C++/MATLAB work is safety- or compliance-bound).

## Files touched

- **Report:** `SWE/swe_process_corpus_v1_0.md` (deliverable 1).
- **Build:** `build/records_proc.py` (new; 84 records), `build/build.py` (SOURCES, CORPUS_LABELS, PHASE-2 `swe-process` branch + new `lang` facet, 12 MERGE_MEMBERSHIP leads, adjustments-log line, report header), `build/edges.py` (57 edges, `report:proc` + editorial). Regenerates `data/*.{json,js}` + `corpus_report.md` + `adjustments.md` clean (no new warnings/conflicts).
- **Presentation:** `styles/tokens.css` (`--c-proc` rose-magenta hue), `styles/app.css` (`.cc-proc` chip), `logic/util.js` (4 corpus maps), `logic/views/facets.js` (new `language` facet rail — mirrors `lane`, zero core.js change needed since `valuesOf` is generic), `logic/inspector.js` (`report:proc` provenance label, `language` reconciled tag, "Six→Seven research passes"). `logic/parse.js` needed no change (it does not hard-code corpus keys); `logic/views/anchors.js` needed no `NO_ANCHOR` entry because the pass **asserts 30 anchors**.
- **Docs:** `README.md`, `MODELS.md` (corpora table + provenance + census), `index.html` (meta/title/eyebrow).

## Verification

`python build/build.py` runs clean. Served at `http://localhost:8098` (config `swe-explorer`): **zero console errors**; all five models mount (`Reading graph / Facets / Chronology / Overlap / Anchors` all ok); the graph **gains an 86-node swe-process band**; the corpus selector lists **`corpus: proc`**; the new **`language` facet** counts agnostic 37 · matlab 14 · python 11 · cpp 10 · c 6 · multi 5; the Anchors column shows **30 swe-process anchors**; Overlap shows the graft signatures (simulink+proc = 15, emb-c+proc = 14, …). The merged node **`misrac`** shows all three memberships (`emb-arch`, `emb-c`, `swe-process`) with per-report raw tags (`swe-process: {area: standards, lang: c, role: anchor}`) and reconciled `branches: [design, process]`.
