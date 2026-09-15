# Audit findings for `python_quality_gates_manifest.md`

8 findings: CRITICAL 1, MAJOR 7

Each finding was produced by an adversarial auditor that verified the claim against a
primary source or by running the tool itself. Line numbers were correct at audit time and
will shift as you edit - locate by the quoted text, not the number.

---

## 1. [CRITICAL] around line 1618

**Quoted text being challenged:**

> `"google"` disables `D203`, `D213`, `D214`, `D215`, `D404`, `D405`, `D406`, `D407`, `D408`, `D409`, `D410`, `D411`; `"numpy"` disables that same set **plus `D212` and `D216`**; `"pep257"` disables `D203`, `D213`, `D214`, `D215`, `D404`, `D405`, `D406`, `D407`, `D408`, `D409`, `D410`, `D411`.

**What is actually true:**

All three lists are wrong, and D216 is not a ruff rule at all. Authoritative exclusion lists: google = D203, D204, D213, D215, D400, D401, D404, D406, D407, D408, D409, D413. numpy = D107, D203, D212, D213, D402, D413, D415, D416, D417. pep257 = D203, D212, D213, D214, D215, D404, D405, D406, D407, D408, D409, D410, D411, D413, D415, D416, D417, D420. So D214/D405/D410/D411 are claimed disabled under google but are ENABLED; under numpy virtually the whole claimed set (D214, D215, D404–D411, D400, D401) is ENABLED; and the parenthetical hedge that google and pep257 are identical is false — they differ in 8 codes. A reader following this either gets an unexpected flood of D-diagnostics or, if they paste D216 anywhere, a hard ruff config failure.

**Source the auditor checked:**

ruff settings reference, `lint.pydocstyle.convention` — https://docs.astral.sh/ruff/settings/#lint_pydocstyle_convention . Verified by live measurement of the resolved rule set under each convention with `uvx ruff@0.16.2 check --show-settings` (select=["D"] + convention). Also: `ignore = ["D216"]` makes ruff 0.16.2 abort with `Cause: Unknown rule selector `D216``; D216 does not appear anywhere in https://docs.astral.sh/ruff/rules/ (D2xx runs D200–D215, then D251–D255).

**Prescribed fix:**

Replace with the three lists from ruff's settings page: `"google"` disables D203, D204, D213, D215, D400, D401, D404, D406, D407, D408, D409, D413; `"numpy"` disables D107, D203, D212, D213, D402, D413, D415, D416, D417; `"pep257"` disables D203, D212, D213, D214, D215, D404–D411, D413, D415, D416, D417, D420. Delete D216 entirely and delete the "google and pep257 lists are identical" hedge. Also correct `_work/facts/r10_quality_gates.md` fact 108 and honest-limit 33, which are the source of the error.

---

## 2. [MAJOR] around line 1620

**Quoted text being challenged:**

> `"google"` disables `D203`, `D213`, `D214`, `D215`, `D404`, `D405`, `D406`, `D407`, `D408`, `D409`, `D410`, `D411`; `"numpy"` disables that same set **plus `D212` and `D216`**; `"pep257"` disables `D203`, `D213`, `D214`, `D215`, `D404`, `D405`, `D406`, `D407`, `D408`, `D409`, `D410`, `D411`.

**What is actually true:**

python_linting_practices_manifest.md §6.3 (lines 492-506) already owns this exact mechanism with the same disable lists, plus a MEASURED observation gates lacks (ruff's own warning text when `convention` is left `null`). PLAN.md scopes gates to "which checks run, where, how they fail" and says it "does **not** re-teach typing or testing content — it gates them"; ruff `D`-rule configuration is squarely the linting file's. gates §11 carries no cross-reference to python_linting_practices_manifest.md at all (that filename appears only at lines 24, 265, 968 and 2006). The two copies already differ in posture: gates flags the google/pep257 identity as OPEN ("re-verify before relying on a difference between them"), linting §6.3 states it flatly.

**Source the auditor checked:**

python_linting_practices_manifest.md:492-506 (§6.3) and :1250-1290 (§15.1); _work/PLAN.md: "python_linting_practices_manifest.md — the *rule set* ... Does **not** own CI wiring or metrics" / "python_quality_gates_manifest.md ... Does **not** re-teach typing or testing content"

**Prescribed fix:**

Replace gates §11.1's PEP 257 recap and the convention disable lists with: "PEP 257's normative content and the subtractive `lint.pydocstyle.convention` mechanism (including the exact disabled-code lists) are owned by `python_linting_practices_manifest.md` §6.3 and §15.1. The gate obligations are: (a) `select = [\"D\"]` together with an explicit `convention`, (b) numpydoc validation with an explicit check allowlist — `checks = [\"all\"]` is indefensible because `ES01`/`SA01`/`EX01` demand prose on every object." Keep only the numpydoc-validation paragraph, which is genuinely gates-only.

---

## 3. [MAJOR] around line 717

**Quoted text being challenged:**

> ### 6.1 Coverage: the arithmetic that makes thresholds lie

**What is actually true:**

python_testing_tooling_manifest.md §5a is titled "Coverage measurement mechanics, and the arithmetic that makes thresholds lie" (line 176) and explicitly claims this ground: "Gate **wiring** — which check runs where, with what exit code, and how a standard is adopted incrementally — belongs to `python_quality_gates_manifest.md`; what follows is the measurement semantics that wiring depends on." gates §6.1 then re-teaches all of that measurement semantics: `fail_under` exits 2, `precision` participates in the comparison (89.6%→90%), no per-file threshold, branch off by default, `exclude_lines` replaces the built-ins, `parallel`/`relative_files`/`[paths]`. gates §6.3 (lines 781-806) likewise reproduces testing §5b's assertion-free-test finding almost sentence for sentence (`pytest-finer-verdicts` solves a different problem, `pytest-check` adds soft checks, the `pytest_collection_modifyitems` AST hook, mutation as the real oracle), and both files state the same derived conclusion verbatim ("execution is not verification").

**Source the auditor checked:**

python_testing_tooling_manifest.md:176-202 (§5a) and :204-226 (§5b); _work/PLAN.md scope boundary for python_quality_gates_manifest.md

**Prescribed fix:**

Reduce gates §6.1 to wiring only — the exact commands, the exit-code contract (`2`, not `1`), and the required config values (`branch = true`, `precision = 2`, `fail_under` at the measured floor, plus the changed-lines gate) — opening with "The measurement semantics behind each of these is owned by `python_testing_tooling_manifest.md` §5a." Delete the six-fact recap. In §6.3, keep the gate framing and "State which you chose", and cite `python_testing_tooling_manifest.md` §5b for the tool survey instead of repeating it.

---

## 4. [MAJOR] around line 530

**Quoted text being challenged:**

> | a `# noqa` that no longer applies | ruff **`RUF100`** `unused-noqa` (fix Always) | **on by default** | VERSION-DEPENDENT (ruff 0.16.2) |

**What is actually true:**

The suppression-hygiene rule table now exists in three files. python_linting_practices_manifest.md §8.2 (lines 578-596) is the owner and carries the identical table (RUF100/101/028/102/103/104/PGH003/PGH004 with fix class and default status), and §8.3 (lines 608-624) carries the identical checker mirror (mypy `--warn-unused-ignores`/`--warn-redundant-casts`/`ignore-without-code`, pyright `enableTypeIgnoreComments`/`reportUnnecessaryTypeIgnoreComment`, pylint `I0021`). python_language_hazards_manifest.md:619 carries a third copy in its §10 hazard table. Both gates (line 24 defers lint to the linting file) and hazards (lines 30-31, "suppression hygiene → python_linting_practices_manifest.md") formally cede this content and then restate it; gates §4.5 contains no cross-reference to linting §8.

**Source the auditor checked:**

python_linting_practices_manifest.md:578-640 (§8.2–§8.4); python_language_hazards_manifest.md:619 and its deferral block at :30-31; _work/PLAN.md house rule 4 ("Cross-reference, never duplicate. State the rule once in its owning file")

**Prescribed fix:**

In gates §4.5 keep only what is gates-only — the five-vocabulary point, the `S` budget formula with its `per-file-ignores`/`ignore_errors` terms, and the two `--fix` hazards — and replace the rule table and checker-mirror rows with "The rule codes, their default status and the per-checker mirror are owned by `python_linting_practices_manifest.md` §8.2–§8.3; this section gates the census they produce." In hazards §10, reduce the "Stale suppressions accumulating" cell to `RUF100` + mypy `--warn-unused-ignores` and drop the `(unused:)`/`(non-enabled:)` and `lint.external` detail.

---

## 5. [MAJOR] around line 613

**Quoted text being challenged:**

> **VERSION-DEPENDENT (mypy 2.3.0).** `--strict` enables exactly thirteen flags: `--disallow-any-generics`, `--disallow-subclassing-any`, `--disallow-untyped-calls`, `--disallow-untyped-defs`, `--disallow-incomplete-defs`, `--check-untyped-defs`, `--disallow-untyped-decorators`, `--warn-redundant-casts`, `--warn-unused-ignores`, `--warn-return-any`, `--no-implicit-reexport`, `--strict-equality`, `--extra-checks`.

**What is actually true:**

The same version-volatile 13-item list is enumerated in python_typing_contract_manifest.md:51 (the owning file, which additionally sources it to `strict_flag=True` in `mypy/main.py` at tag v2.3.0), summarised again in python_linting_practices_manifest.md:81 ("mypy `--strict` (13 flags)"), and the mypy opt-in error-code list appears a fourth time in python_language_hazards_manifest.md:204-215. mypy's docs warn "the exact list of flags enabled by running `--strict` may change over time", and python_typing_contract_manifest.md:349 lists "Reproducing the 15-flag `mypy --strict` list" as an anti-pattern — a rule the collection breaks against itself. On the next mypy bump three files must be edited in lockstep or they will disagree, with nothing marking which is authoritative.

**Source the auditor checked:**

python_typing_contract_manifest.md:51 and :349; python_language_hazards_manifest.md:204-215 (§1.2, which correctly says "`--strict` is a different list, owned by `python_typing_contract_manifest.md` §1"); _work/PLAN.md house rule 4

**Prescribed fix:**

In gates §5.1 delete the 13-flag enumeration and the 23-code optional-code list; open with "The exact `--strict` flag set and the full optional-code inventory are owned by `python_typing_contract_manifest.md` §1 (13 flags as of mypy 2.3)." Keep only the gate-relevant residue: the indirect-code mapping, `enable_error_code` beating `disable_error_code`, and the mypy 2.0 default flips as a re-baselining event.

---

## 6. [MAJOR] around line 1167

**Quoted text being challenged:**

> The deprecation *contract* — what may change, what the public surface is, how versions are numbered — belongs to `python_module_boundaries_manifest.md`. The *enforcement* is here, and it has three parts that must all be present or the window is theatre.

**What is actually true:**

Two files define a mandatory three-part deprecation contract with the same absolutist framing and different members. python_module_boundaries_manifest.md:1086-1091 gives: (1) producer runtime `@warnings.deprecated`, (2) **producer self-check** `-W error::DeprecationWarning` in your own test run, (3) consumer static mypy `deprecated` — "all three, or the window is fiction". gates §8.4 gives: (1) the marker, (2) consumer static mypy `deprecated`, (3) **consumer-side** pytest `filterwarnings` — "all three ... or the window is theatre". The producer self-check is absent from gates' triad; the consumer test gate is absent from module_boundaries'. An agent following either file believes it has a complete mechanism and is missing one end. The union is four mechanisms, not three, and neither file says so.

**Source the auditor checked:**

python_module_boundaries_manifest.md:1086-1096 (§9.3); python_quality_gates_manifest.md:1164-1188 (§8.4)

**Prescribed fix:**

Fix the vocabulary in one place. In module_boundaries §9.3 rename the table "The four-part visibility contract" and add the missing row "consumer, test | pytest `filterwarnings` promoting `DeprecationWarning` to error in the consumer's suite | ESTABLISHED". In gates §8.4 replace the three-part list with "The four parts of the contract are enumerated in `python_module_boundaries_manifest.md` §9.3; this section wires parts 2–4 into CI" and delete the duplicated `@warnings.deprecated` signature/semantics paragraph.

---

## 7. [MAJOR] around line 1111

**Quoted text being challenged:**

> 2017 — the same work the SWE corpus records as the naming source for the `feature-toggle` element).

**What is actually true:**

The corpus records BCK 2021 as the naming source for `feature-toggle`, not Hodgson 2017. elements.json holds TWO distinct elements: `feature-toggle` (realm architecture / kind tactic, named_in "Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)", works ['bck'], aka 'kill switch', 'feature flag (design-realm realization)') and `feature-flag` (realm design / kind code-structure, named_in "Hodgson, 'Feature Toggles (aka Feature Flags)', martinfowler.com, 2017 ... names toggle point, toggle router, toggle configuration", works ['hodgsontoggles']). The two are bridged by a sourced edge `feature-flag --realizes--> feature-toggle`. The next sentence of §8.2 then lists "a **toggle point**, a **toggle router**, and **toggle configuration**" — those are precisely `feature-flag`'s parts, so the section is describing `feature-flag` while naming `feature-toggle`. The manifest never mentions `feature-flag` at all (grep: only 'feature-flag SDK'/'feature-flag service' as English). The evidence base explicitly warned against this exact conflation: _work/seed/s3_modularity_maintainability.md:503 is headed "**11. \"Feature flag\" is two elements, deliberately.**" and s3:75 assigns "hodgsontoggles (Hodgson ... 2017) for the design element; bck 2021 for the tactic".

**Source the auditor checked:**

E:/dev/corpora/SWE/explorer/data/elements.json (nodes `feature-toggle`, `feature-flag`, `feature-flag-driven-release`; works `bck`, `hodgsontoggles`); E:/dev/corpora/manifests/_work/seed/s3_modularity_maintainability.md:75, 200, 503-507

**Prescribed fix:**

Replace with: "**ESTABLISHED** (Pete Hodgson, *Feature Toggles (aka Feature Flags)*, martinfowler.com, 09 October 2017 — the work the SWE corpus records as the naming source for the **`feature-flag`** element, design/code-structure). There are exactly four categories, positioned on axes of **dynamism** and **longevity**. `feature-flag` names the parts: a **toggle point**, a **toggle router**, and **toggle configuration**. Distinguish it from the architecture tactic `feature-toggle` (bck 2021 — the kill switch), which `feature-flag` *realizes* via a sourced corpus edge."

---

## 8. [MAJOR] around line 204

**Quoted text being challenged:**

> | 26 | docstring presence | `interrogate --fail-under <N>` (config default `fail-under = 80`) | C | required | below threshold | no | trivial | VERSION-DEPENDENT (1.7.0) |

**What is actually true:**

Line 166 of the same file promises "An agent should be able to build the pipeline from this table alone." An agent that does so wires interrogate as a required gate — and the same file's reject-on-sight list at line 1768 forbids it: "**Mutation score, docstring coverage or the Maintainability Index as a required gate.** Violates §6.6, §11.2 and §9.2 respectively." interrogate's own one-line description, quoted at line 1641, is "Interrogate a codebase for docstring coverage". Worse, the cited §11.2 (lines 1639-1648) says nothing of the kind — it is neutral, noting only that interrogate "measures **presence, not quality** — the same job ruff's `D1xx` family does inside the linter, which is why most projects do not need both." Yet ledger row 24 already makes `ruff check` with `D` selected a required gate at P and C. The collection therefore mandates both halves of a pair it says most projects should not both have, and rejects one of them on sight.

**Source the auditor checked:**

Internal: python_quality_gates_manifest.md lines 166, 204 (row 26), 202 (row 24), 1639-1648 (§11.2), 1768 (anti-pattern). interrogate description confirmed at https://pypi.org/project/interrogate/ — 8 Aug 2026

**Prescribed fix:**

Demote ledger row 26 to `advisory` and change its req/adv cell to `advisory (diagnostic only — see anti-patterns)`, or delete row 26 and rely on ledger row 24 (`D1xx` inside ruff). Then repoint the anti-pattern at line 1768 to the section that actually argues it, and add one sentence to §11.2: "Presence is a diagnostic, not a gate; `D1xx` inside the linter is the gate, and running interrogate as well double-counts."

---
