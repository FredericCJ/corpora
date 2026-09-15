# Audit findings for `python_testing_tooling_manifest.md`

5 findings: CRITICAL 1, MAJOR 3, MINOR 1

Each finding was produced by an adversarial auditor that verified the claim against a
primary source or by running the tool itself. Line numbers were correct at audit time and
will shift as you edit - locate by the quoted text, not the number.

---

## 1. [CRITICAL] around line 387

**Quoted text being challenged:**

> a support matrix written today that still lists 3.10 will be claiming support for an end-of-life interpreter within months, so 3.11 is the defensible floor for new work.

**What is actually true:**

error_tracing_contract_manifest.md:385 explicitly retires exactly this recommendation: "assume **3.13+, and prefer 3.14** ... **The former 3.11+ recommendation is behind the support calendar**: on 2026-08-08 only 3.13 and 3.14 are in the bugfix phase." The hub, which PLAN.md assigns "the minimum-target policy", declares the floor OPEN and takes no position (python_platform_baseline_manifest.md:219-238 §3d: "ESTABLISHED (the policies); OPEN (which one this project follows)", giving 3.10 under CPython's window and 3.12 under SPEC 0). The collection therefore gives three different answers to the most consequential pin in pyproject.toml, and the testing file asserts its answer flatly, untagged as OPEN, in a file that does not own the policy. An agent reading testing_tooling writes `requires-python = ">=3.11"` and thereby loses every construct error_tracing's own rules depend on (`@warnings.deprecated`, group-aware `suppress`, callable `split`/`subgroup`, `exc_type_str`).

**Source the auditor checked:**

error_tracing_contract_manifest.md:385 and :390; python_platform_baseline_manifest.md:219-254 (§3d/§3e); _work/PLAN.md scope-boundary line "python_platform_baseline_manifest.md — only version/support/schedule/PEP-status facts, interpreter switches, build variants, and the minimum-target policy"

**Prescribed fix:**

Replace "so 3.11 is the defensible floor for new work" with "so the lowest CI leg must be re-cut; the minimum-target recommendation itself is owned by `python_platform_baseline_manifest.md` §3d–§3e (currently OPEN), and `error_tracing_contract_manifest.md` §21 records the behaviour-driven case for 3.13+/prefer 3.14." Then reconcile once: either the hub states one collection-wide recommendation that both files cite, or error_tracing §21 is re-tagged as an error-contract-local preference. Do not leave two files naming different floors.

---

## 2. [MAJOR] around line 387

**Quoted text being challenged:**

> CPython version, phase and schedule facts are **not** restated here — see `python_platform_baseline_manifest.md`. Two consequences a test suite must act on: pytest requires Python >= 3.10 (9.0.0 dropped 3.9), and Python 3.10 leaves security support in October 2026

**What is actually true:**

The sentence cedes hub ownership and then restates a hub-owned support-phase date in the same breath. The identical pattern occurs three more times: python_quality_gates_manifest.md:1192-1194 ("Version dates and support phases are owned by `python_platform_baseline_manifest.md`" followed immediately by "**Python 3.10 leaves support around 2026-10**, and **3.15's first release is dated 2026-10-01**"); logging_observability_manifest.md:321-323 ("Which interpreters are supported when is owned by `python_platform_baseline_manifest.md`" followed by "On a **3.10** floor — the oldest branch still receiving fixes"); error_tracing_contract_manifest.md:385 ("on 2026-08-08 only 3.13 and 3.14 are in the bugfix phase"). PLAN.md house rule 3 is explicit: "Other files state *behaviour* and cite the hub for *when*; they do not re-assert release dates." All four are consistent with the hub today, which is exactly why they will drift silently after 2026-10 when 3.10 goes EOL and 3.13 leaves bugfix — four files will then be wrong and only the hub right.

**Source the auditor checked:**

_work/PLAN.md house rule 3; python_platform_baseline_manifest.md:60-67 (§1a support matrix, the owning table)

**Prescribed fix:**

Strip the dates. testing:387 → "…pytest requires Python >= 3.10 (9.0.0 dropped 3.9), and the lowest leg of most existing CI matrices is about to become unsupported — see `python_platform_baseline_manifest.md` §1a for the phase and EOL of every branch." gates:1193-1194 → "Two consequences, whose dates live in the hub §1a: the lowest supported leg is about to retire and 3.15 is about to ship, so a pre-June-2026 matrix template is stale in both directions." logging:323 → "On the lowest floor the hub still shows as supported (§1a) …". error_tracing:385 → "…is behind the support calendar (see the hub §1a for which branches are in bugfix)."

---

## 3. [MAJOR] around line 406

**Quoted text being challenged:**

> ## Recommendations

**What is actually true:**

This file has no anti-patterns / rejection-list section at all. Its full heading list runs `## TL;DR` (5), `## Key Findings` (13), `## Details` (26) with §1–§8, `## Recommendations` (406), `## Caveats` (418), `## Sources` (425), `### Sibling manifests` (513). `grep -in 'anti-pattern|antipattern|rejection list'` returns zero hits in the whole file. PLAN.md's ground-truth register spec says such a file 'Ends with anti-patterns, open questions, and sources', and house rule 8 says 'Anti-patterns section is a rejection list, one line each, each pointing at the section it violates. This is the part agents actually obey.' Every other ground-truth file carries one: platform-baseline 28 entries, typing 37, hazards 39, linting 39, error-tracing 42, logging 53, runtime-diagnostics 24, module-boundaries 48, quality-gates 35, concurrency 50 — 395 entries in total, every one of which carries a § pointer. The testing file's `## Recommendations` is a prescriptive stage ladder, not a rejection list, and `## Caveats` is about evidence quality; neither substitutes.

**Source the auditor checked:**

E:/dev/corpora/manifests/python_testing_tooling_manifest.md (grep -n '^#\{2,3\} ' + grep -in 'anti-pattern'); E:/dev/corpora/manifests/_work/PLAN.md, 'Two registers' section and house rule 8

**Prescribed fix:**

Add a `## Anti-patterns checklist` section immediately before `## Sources` (i.e. after L424), one line per entry, each naming the section it violates — the material is already in the file and only needs inverting, e.g.: `- **Writing "pytest 9" instead of `>= 9.1.0`** — 9.0.0–9.0.3 silently ignored `--strict-markers`/`--strict-config` from `addopts` (§1a).` / `- **A coverage percentage set as a target rather than read as a diagnostic** (§5a).` / `- **`fail_under` trusted without reading its arithmetic** — exit status is 2, and `[report] precision = 0` makes 89.6% pass a threshold of 90 (§5a).` / `- **A mock where a fake implementing the real contract was meant**, or a mock without `autospec=True`/`spec_set=True` (§3).` / `- **Calling a double a "fake" with no contract suite run against both it and the real implementation** (§6).` / `- **Assertion-free tests** — coverage rises, no obligation is added (§5a, §5b).` / `- **A suite that cannot reproduce a failure from its own printed seed** (§6c).` / `- **Mixing pytest-asyncio and AnyIO task semantics** — code correct under one is broken under the other (§6d).` / `- **Asserting on an exception message instead of the error contract** (§5c).` / `- **A substitution with no named testability tactic and therefore no exit criterion** (§7a).`

---

## 4. [MAJOR] around line 19

**Quoted text being challenged:**

> - **pytest's configuration surface is a precedence chain, not a merge.** `pytest.toml` / `.pytest.toml` > `pytest.ini` / `.pytest.ini` > `pyproject.toml` > `tox.ini` > `setup.cfg`

**What is actually true:**

No file in the collection states how the TEST TREE is laid out, and three coupled decisions are left with no default anywhere: (a) whether `tests/` carries `__init__.py`, (b) which pytest `--import-mode` to use, (c) how ruff's `INP001` interacts. `grep -n '__init__.py|importmode|import-mode|rootdir'` over python_testing_tooling_manifest.md returns ZERO hits; python_quality_gates_manifest.md mentions `--import-mode` once in passing (line 804, "`testpaths`, `norecursedirs` and `--import-mode` fix what is collected") with no recommendation; python_module_boundaries_manifest.md owns "project layout" per PLAN.md line 103 but covers only the importable tree (§3.1-§3.4) and never the tests tree. This is the single best-known breakage under the src layout the collection mandates (§12 item 1). It is not merely absent: the recommended ruff `select` includes `"INP"` (line 356) whose INP001 flags "packages that are missing an `__init__.py` file", while the `per-file-ignores` for `tests/**` (line 369) exempts only `S101`, `PLR2004`, `D103` — so the agent's first `ruff check` after wiring the mandated src layout may fail on its own test tree with no guidance on which way to resolve it.

**Source the auditor checked:**

`grep -n '__init__.py|importmode|import-mode|rootdir|conftest layout' python_testing_tooling_manifest.md` → no layout hits; python_quality_gates_manifest.md:804; _work/PLAN.md:103-105 (layout ownership); INP001 semantics at https://docs.astral.sh/ruff/rules/implicit-namespace-package/ ("packages that are missing an `__init__.py` file", setting `namespace-packages`) — 8 Aug 2026

**Prescribed fix:**

Add a short subsection to python_testing_tooling_manifest.md §1a stating the default and its consequence: "**Test-tree layout (OPEN — pin it).** Default for a src layout: `tests/` with **no** `__init__.py`, `--import-mode=importlib`, `testpaths = [\"tests\"]`, and every test module basename unique (prepend mode plus duplicate basenames is the classic collection error). The alternative — `__init__.py` in every test directory with the default prepend mode — permits duplicate basenames at the cost of making the test tree importable and shippable (`python_module_boundaries_manifest.md` §3.4: setuptools namespace scanning is on by default)." Then add `"INP001"` to the `tests/**` entry of `per-file-ignores` at python_linting_practices_manifest.md line 369.

---

## 5. [MINOR] around line 170

**Quoted text being challenged:**

> `characterization-test`, `seam`, injected/virtual clock, in-memory database, `fault-injection`, `consumer-driven-contract` and `test-container` are all **absent from the SWE element layer by charter** — they are practice-layer vocabulary, verified absent from all 1083 nodes.

**What is actually true:**

Thirteen of the fourteen listed names are genuinely absent from every node's name and aka (I checked all 1083 nodes for each term). Characterization testing is the exception: it IS in the element layer, folded into `golden-master-testing`, whose aka list contains "characterization testing (legacy-code framing)" and whose named_in is "Feathers, Working Effectively with Legacy Code (2004; 'characterization test')". The same file says so at §6b line 272: "`golden-master-testing` folds approval testing, snapshot testing, characterization testing (the legacy-code framing) ... named in Michael Feathers ... (as \"characterization test\")". So the census sentence — tagged ESTABLISHED (corpus census) — contradicts §6b, and an agent obeying §5 would conclude there is no citable element for characterization tests when in fact there is one.

**Source the auditor checked:**

E:/dev/corpora/SWE/explorer/data/elements.json (node `golden-master-testing`, fields `aka` and `named_in`); self-contradicted by python_testing_tooling_manifest.md:272

**Prescribed fix:**

Remove `characterization-test` from the absent list and redirect it: "`equivalence-partitioning`, `boundary-value-analysis`, `test-oracle`, `metamorphic-testing`, `test-pyramid`, `contract-test`, `mutation-testing`, `seam`, injected/virtual clock, in-memory database, `fault-injection`, `consumer-driven-contract` and `test-container` are all **absent from the SWE element layer by charter** — they are practice-layer vocabulary, verified absent from all 1083 nodes. (\"Characterization test\" is the exception: it is *present*, as an aka of `golden-master-testing` — see §6b.)"

---
