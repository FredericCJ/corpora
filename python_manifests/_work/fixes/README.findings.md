# Audit findings for `README.md`

4 findings: CRITICAL 1, MINOR 3

Each finding was produced by an adversarial auditor that verified the claim against a
primary source or by running the tool itself. Line numbers were correct at audit time and
will shift as you edit - locate by the quoted text, not the number.

---

## 1. [CRITICAL] around line 102

**Quoted text being challenged:**

> | **Start a new project** | `python_platform_baseline_manifest.md` → `python_module_boundaries_manifest.md` → `python_typing_contract_manifest.md` → `python_quality_gates_manifest.md` |

**What is actually true:**

The cold-start reading order omits `python_linting_practices_manifest.md`, which is the ONLY file in the collection containing a `[tool.ruff]` block, an explicit `select` list, the `per-file-ignores`, the formatter/linter division of labour and the pydocstyle convention (§4.3, lines 344-397). `grep -n 'select = \['` returns hits in python_linting_practices_manifest.md only — quality_gates mentions `select` twice and both times to defer (line 1749: "violates §2 and the linting manifest's ownership of the rule set"). quality_gates row 2 makes `ruff check` a REQUIRED merge gate (line 179) and the linting manifest's own first anti-pattern is "**No explicit `lint.select`**" (line 1401). So an agent that follows the stated reading order literally cannot produce the artefact the collection insists on, and will ship the implicit default set the collection calls "not a standard". Same omission for the formatter config.

**Source the auditor checked:**

Internal cross-check: `grep -n 'lint.select|select = \[' python_quality_gates_manifest.md python_module_boundaries_manifest.md python_typing_contract_manifest.md python_platform_baseline_manifest.md` → no config block; python_linting_practices_manifest.md:344-397 is the sole source

**Prescribed fix:**

Rewrite line 102 as: `| **Start a new project** | `python_platform_baseline_manifest.md` → `python_module_boundaries_manifest.md` → `python_typing_contract_manifest.md` → `python_linting_practices_manifest.md` §2-§6 (the `[tool.ruff]` block) → `python_quality_gates_manifest.md` |`

---

## 2. [MINOR] around line 57

**Quoted text being challenged:**

> | `python_platform_baseline_manifest.md` | CPython release/support matrix, PEP status index, interpreter switches, build variants (free-threaded, JIT), deprecation timeline, minimum-target policy. The only file that owns dates. |

**What is actually true:**

"The only file that owns dates" is contradicted by every ground-truth sibling, each of which owns and dates its own tool releases by explicit design: python_quality_gates_manifest.md:35-56 is a 40-row table of tool versions with release dates; python_linting_practices_manifest.md:37-43 pins ruff 0.16.2 (2026-08-07), pylint 4.0.6 (2026-06-14), flake8 7.3.0 (2025-06-20); python_language_hazards_manifest.md:42-48 does the same; python_typing_contract_manifest.md:5 dates mypy 2.3.0 (13 Jul 2026), pyright 1.1.411 (25 Jun 2026) and eleven more. The hub owns *CPython* dates only.

**Source the auditor checked:**

python_quality_gates_manifest.md:35-56; python_linting_practices_manifest.md:35-43; python_typing_contract_manifest.md:5; _work/PLAN.md house rule 3

**Prescribed fix:**

Change to "The only file that owns **CPython** dates; each pillar file dates the third-party tools that are its own subject matter."

---

## 3. [MINOR] around line 119

**Quoted text being challenged:**

> | Tag | Meaning | How to treat it |

**What is actually true:**

The tag table (lines 119-126) lists ESTABLISHED, VERSION-DEPENDENT, OPEN, CC-FACT and FLAGGED-SECONDARY, under the claim "Every factual claim in a ground-truth manifest is tagged. The tag tells you how much weight it bears." It omits **MEASURED**, which appears 38 times in python_linting_practices_manifest.md and 18 times in python_language_hazards_manifest.md and is declared load-bearing in both — linting:22-24 "`MEASURED` inline = from executing the pinned tool during the 2026-08-08 pass rather than from a documentation page; **where page and binary disagreed, MEASURED wins** and the disagreement is stated"; hazards:19-21 "for default-rule-set questions that is the *stronger* evidence". An agent handed README as the epistemic protocol meets an undocumented tag that outranks the documented ones.

**Source the auditor checked:**

python_linting_practices_manifest.md:22-24; python_language_hazards_manifest.md:19-21; grep -c MEASURED across the set (56 occurrences in 2 files)

**Prescribed fix:**

Add a row: "| **MEASURED** | Obtained by executing the pinned tool during the verification pass rather than from a documentation page. Where docs and binary disagreed, MEASURED wins and the disagreement is stated. | Rely on it for the pinned version only; re-measure on every tool bump. |" and note that it currently appears in the linting and hazards manifests.

---

## 4. [MINOR] around line 38

**Quoted text being challenged:**

> | route | meaning |
|---|---|
| **type-catchable** | a named checker, at a named strictness, rejects it |

**What is actually true:**

README's route table (L38–L46) enumerates six routes: type-catchable, lint-catchable, feature-eliminated, test-catchable, fitness-function, contract-only. This matches PLAN.md's list, but python_language_hazards_manifest.md §0.1 (L84–L95) declares **seven**, adding `runtime-catchable` ('a process-start configuration turns silence into an exception'), which it uses six times (L93, L502, L503, L787, L968, L1004) and counts separately in its §19 tally ('runtime-catchable 3'). README is the collection entry point and the place an agent learns the route vocabulary, so a route it does not list reads as an error in the hazards file rather than a seventh member of the set.

**Source the auditor checked:**

E:/dev/corpora/manifests/README.md L36-46 vs python_language_hazards_manifest.md L84-95 and L1001-1005; grep -n 'runtime-catchable' python_*.md

**Prescribed fix:**

Add a row to README's table between **test-catchable** and **fitness-function**: `| **runtime-catchable** | a process-start configuration turns silence into an exception — install it in the entry point, and test that it is installed |`. Optionally add the same row to _work/PLAN.md's route list so the three lists agree.

---
