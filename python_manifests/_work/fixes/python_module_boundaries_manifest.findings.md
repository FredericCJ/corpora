# Audit findings for `python_module_boundaries_manifest.md`

8 findings: MAJOR 3, MINOR 5

Each finding was produced by an adversarial auditor that verified the claim against a
primary source or by running the tool itself. Line numbers were correct at audit time and
will shift as you edit - locate by the quoted text, not the number.

---

## 1. [MAJOR] around line 693

**Quoted text being challenged:**

> | `protected` | nothing outside the allow-list may import the protected modules | `protected_modules`, `allowed_importers`, `as_packages` |

**What is actually true:**

import-linter's `protected` contract checks **direct** imports only: "Protected contracts prevent modules from being *directly* imported, except by modules in an allow-list" and "no module other than `green` (and its descendants) will be allowed to import `blue` (and its descendants) *directly*." The three neighbouring rows in this same table are all explicit about transitivity (`layers`: "This includes indirect imports"; `forbidden`: "transitively"; `independence`: "even indirectly"), so dropping the qualifier on `protected` reads as a deliberate statement that it is transitive too. It is not: `a → b → protected` passes a `protected` contract. §7.4's trap list (line 733 onward, "each one produces a green build that checks nothing") covers `protected` only for the `as_packages` case, so nothing else in the file corrects it. This is exactly the green-build-that-checks-nothing failure the section warns about — and §5 (line 535) and §9 recommend `protected` as the enforcement route for internal-module hiding.

**Source the auditor checked:**

https://raw.githubusercontent.com/seddonym/import-linter/master/docs/contract_types/protected.md — opening two paragraphs. Accessed 8 Aug 2026.

**Prescribed fix:**

Change the asserts cell to: "nothing outside the allow-list may **directly** import the protected modules — `protected` does not check indirect imports, so `a → b → protected` passes". Add to §7.4 as a new trap: "**`protected` is direct-only.** Unlike `layers`, `forbidden` and `independence`, it does not follow import chains; a re-export in an allowed module launders access to a protected internal. Pair it with a `layers` or `forbidden` contract if the indirect path matters."

---

## 2. [MAJOR] around line 1310

**Quoted text being challenged:**

> 8. **`deptry .` in CI** (§7.6) — catches the undeclared-dependency break that no internal contract

**What is actually true:**

This is item 8 of the nine "Adopt on day one" items in §12, the collection's day-one boundary checklist. `grep -n deptry python_quality_gates_manifest.md` returns ZERO hits: deptry is absent from the 34-row gate ledger (§2.1), absent from the pinned-tool version table (lines 38-58), and therefore has no stage, no exit-code contract, no cost class and no version pin anywhere in the file that PLAN.md line 106-108 says "Owns `ruff`/`pre-commit`/CI matrix/supply-chain gates/metrics". The consequence is symmetric and both directions are wrong: an agent building CI from the ledger (which claims at line 166 to be sufficient alone) drops a day-one gate; an agent following §12 adds an unpinned tool to CI with no failure contract, which the same collection's own anti-pattern "**Pinning nothing**" (quality_gates line 1748) rejects.

**Source the auditor checked:**

Internal: `grep -n deptry python_quality_gates_manifest.md` → no output; python_module_boundaries_manifest.md lines 675, 833-850, 1310; _work/PLAN.md lines 106-108 (ownership); python_quality_gates_manifest.md lines 38-58, 166, 1748

**Prescribed fix:**

Add a row to the §2.1 ledger: `| 12a | undeclared/unused dependencies | `deptry .` | C M | required | non-zero | no | seconds | VERSION-DEPENDENT (deptry <pin>) |`, add deptry with its verified version to the pinned-tool table at lines 38-58, and add the note "inline suppression is `# deptry: ignore[DEP001,DEP003]` and does not cover DEP002 (`python_module_boundaries_manifest.md` §7.6)".

---

## 3. [MAJOR] around line 1303

**Quoted text being challenged:**

> 4. **`requires-python` with a floor and no ceiling** (§5.1); the floor is

**What is actually true:**

The `requires-python` floor — the first number an agent must write into a new pyproject.toml — is deferred in a circle. This line and line 407 ("State a floor, never a ceiling; the floor is the hub's policy") both send the reader to the hub. The hub then declines: §3b is tagged "**OPEN — the project must state three separate numbers**", §3d is "ESTABLISHED (the policies); **OPEN (which one this project follows)**", and its Open questions list carries "**The floor (OPEN, §3e).** Which `requires-python` value..." and "**The policy behind the floor (OPEN, §3d)**". No file names a recommended starting floor. The hub does state the consequences of each choice (§3e table), which is the honest half — but the practical result is that the only concrete interpreter number an agent can find anywhere in the collection is `py314` in the ruff block at python_linting_practices_manifest.md:347, which the hub's own §3c argues against. The cold-start exercise stalls on step one or silently inherits 3.14.

**Source the auditor checked:**

Internal: python_module_boundaries_manifest.md lines 407, 1303 ; python_platform_baseline_manifest.md lines 190-197 (§3b OPEN), 219-238 (§3d), 240-254 (§3e), 890-896 (Open questions)

**Prescribed fix:**

Add a default with its escape hatch to python_platform_baseline_manifest.md §3e, immediately after the floor table: "**Starting point if the project has not chosen a policy: `requires-python = \">=3.12\"`.** It matches SPEC 0's window today, sits inside CPython's, and unlocks PEP 695 generics, `sys.monitoring`, `@override` and `Unpack[TypedDict]` (§4a) that the rest of this collection uses. Revisit at Q4 2026, when SPEC 0 drops 3.12. Record the policy, not just the number (§3d)." Then change module_boundaries lines 407 and 1303 from "the floor is the hub's policy/call" to "the floor comes from the hub §3e (default `>=3.12` absent a stated policy)".

---

## 4. [MINOR] around line 195

**Quoted text being challenged:**

> Declarations are the exact strings the PyPA tutorial publishes; the pins are theirs.

**What is actually true:**

True for four of the five rows (hatchling >= 1.26, setuptools >= 77.0.3, flit_core >= 3.12.0 <4, pdm-backend >= 2.4.0 — all verified verbatim), but not for the `uv_build` row at line 203, which reads `["uv_build>=0.12.3,<0.13"]`. The PyPA tutorial publishes `requires = ["uv_build >= 0.12.1, <0.13.0"]`. The string in the manifest is uv's own — docs.astral.sh/uv/concepts/build-backend/ publishes exactly `"uv_build>=0.12.3,<0.13"`, and that is where the pack sourced it (_work/facts/r07_packaging_modularity.md:88, whose source line is the astral URL, not packaging.python.org). So the pin is real but the attribution sentence is false for that row, and a reader diffing the table against the tutorial finds a mismatch and cannot tell which is stale.

**Source the auditor checked:**

https://packaging.python.org/en/latest/tutorials/packaging-projects/ (uv-build block) vs https://docs.astral.sh/uv/concepts/build-backend/ . Both accessed 8 Aug 2026.

**Prescribed fix:**

Either use the tutorial's string (`["uv_build >= 0.12.1, <0.13.0"]`) for consistency with the header sentence, or keep uv's own pin and qualify the header: "Declarations are the exact strings the PyPA tutorial publishes; the pins are theirs — except `uv_build`, whose pin is the one uv's own build-backend docs publish (the tutorial currently shows `>= 0.12.1, <0.13.0`)."

---

## 5. [MINOR] around line 1443

**Quoted text being challenged:**

> This collection's most load-bearing word (used in `architecture_manifest_default.md` §1, §4.2 and §6) has **no element in the SWE corpus**

**What is actually true:**

"seam" does not occur anywhere in architecture_manifest_default.md §1 (Vocabulary, lines 15-47). Its only occurrences in that file are lines 354, 355, 364, 365, 386 and 405 — all inside §4.2 Seams (lines 351-387) and the §4.3/§4.4 that follow — plus line 588 ("**Extract seam.**") inside §6 Refactoring Patterns. The §1 half of the citation is wrong, which matters because the sentence's whole point is that the word is load-bearing and uncited.

**Source the auditor checked:**

grep -n "seam" architecture_manifest_default.md → 354,355,364,365,386,405,588; heading map: §1 = lines 15-47, §4.2 = 351-387, §6 = 582-611

**Prescribed fix:**

Change "§1, §4.2 and §6" to "§4.2 and §6".

---

## 6. [MINOR] around line 1064

**Quoted text being challenged:**

> The default filter list, in precedence order, is `default::DeprecationWarning:__main__`, `ignore::DeprecationWarning`, `ignore::PendingDeprecationWarning`, `ignore::ImportWarning`, `ignore::ResourceWarning`.

**What is actually true:**

The same five-entry list is stated in three files. python_platform_baseline_manifest.md §6c (lines 637-644) is the owner — PLAN.md gives the hub "interpreter switches", and only the hub's copy adds the debug-build exception ("In a debug build, the list of default warning filters is empty") that the other two omit — and error_tracing_contract_manifest.md:261 carries a third copy. The same pattern affects the build-conditional defaults of `-X context_aware_warnings` / `-X thread_inherit_context`: stated in hub §5c (lines 486-492), in python_concurrency_determinism_manifest.md at :624, :944 and :962, and in error_tracing_contract_manifest.md at :268 and :380 — five statements of one interpreter-switch default across three files.

**Source the auditor checked:**

python_platform_baseline_manifest.md:637-644 (§6c) and :486-492 (§5c); error_tracing_contract_manifest.md:261, :268, :380; python_concurrency_determinism_manifest.md:624, :944, :962; _work/PLAN.md house rule 4

**Prescribed fix:**

In module_boundaries §9.3 and error_tracing §17a replace the enumerated filter list with "`DeprecationWarning` is invisible by default outside `__main__`; the exact default filter list and the debug-build exception are in `python_platform_baseline_manifest.md` §6c." In concurrency and error_tracing, state the `context_aware_warnings` consequence for `catch_warnings` and cite hub §5c for the default rather than re-quoting it.

---

## 7. [MINOR] around line 124

**Quoted text being challenged:**

> **Named vocabulary.** `explicit-interface` (posa4 2007) → `typing.Protocol` (PEP 544) for structural

**What is actually true:**

elements.json records `explicit-interface`.named_in as "Explicit Interface and Object Manager: Two Patterns from a Pattern Language for Distributed Computing - Buschmann, Henney, Schmidt (EuroPLoP 2003)", with POSA4 only as the *covering work* (works = ['posa4']) and confidence 'spot-checked'. So "posa4 2007" cites the covering work as though it were the naming work. The evidence base caught this and recorded it: _work/seed/s1_testing_verification.md:225 reads "Buschmann, Henney & Schmidt. 'Explicit Interface and Object Manager: Two Patterns from a Pattern Language for Distributed Computing'. EuroPLoP 2003. (`explicit-interface` naming source; the corpus carries POSA4 2007 instead.)" — a correction the manifest drops. Mitigating: SWE/design_elements_corpus_v1_0.md:80-81 does list Explicit Interface under the POSA4 entry, so the citation is defensible against the file house rule 10 names; the defect is the missing caveat, which this collection carries elsewhere for comparable corpus data problems (see error_tracing_contract_manifest.md:596 on `built-in-self-test` and `core-dump`). Same wording at lines 96 and 1446; the Sources entry at line 1605 also cites only POSA4.

**Source the auditor checked:**

E:/dev/corpora/SWE/explorer/data/elements.json (node `explicit-interface`); E:/dev/corpora/manifests/_work/seed/s1_testing_verification.md:225; E:/dev/corpora/SWE/design_elements_corpus_v1_0.md:80-81

**Prescribed fix:**

Add the caveat once, e.g. at line 124: "`explicit-interface` (posa4 2007 as the corpus's covering work; the *naming* paper is Buschmann, Henney & Schmidt, 'Explicit Interface and Object Manager', EuroPLoP 2003 — the corpus records POSA4 instead, FLAGGED-SECONDARY) → `typing.Protocol` (PEP 544) for structural", and mirror it in the Sources entry at line 1605.

---

## 8. [MINOR] around line 111

**Quoted text being challenged:**

> `ports` package *is* the contract; an IDL only pays across process or language" (§8.6).

**What is actually true:**

§8 has subsections 8.1 (L884), 8.2 (L903), 8.3 (L943), 8.4 (L964) and 8.5 (L1005) only — there is no §8.6. The `interface-definition-language` content this sentence is sourcing is in §8.5 'Adapting at the seam, and contracts that are build inputs' (the IDL block is at L1012). This is the only dangling internal § reference in the file; the §5.1–§5.6 references that look dangling all resolve to bolded numbered sub-blocks inside §5 (L403, L409, L417, L429, L437, L446), and the §3.5/§4.2 references at L1443 and L1646 are cross-file pointers into architecture_manifest_default.md, which does have §4.2 Seams.

**Source the auditor checked:**

E:/dev/corpora/manifests/python_module_boundaries_manifest.md (grep -n '^#\{2,4\} ' → 8.1–8.5 at 884/903/943/964/1005; sed -n '1005,1027p' shows the IDL block at L1012)

**Prescribed fix:**

Change `(§8.6)` to `(§8.5)` on line 111.

---
