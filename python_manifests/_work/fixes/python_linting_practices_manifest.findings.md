# Audit findings for `python_linting_practices_manifest.md`

13 findings: CRITICAL 4, MAJOR 5, MINOR 4

Each finding was produced by an adversarial auditor that verified the claim against a
primary source or by running the tool itself. Line numbers were correct at audit time and
will shift as you edit - locate by the quoted text, not the number.

---

## 1. [CRITICAL] around line 311

**Quoted text being challenged:**

> | `LOG001`,`LOG002`,`LOG004`,`LOG009`,`LOG014`,`LOG015` | logging API misuse | `LOG004` Sometimes | ...

**What is actually true:**

LOG004 (log-exception-outside-except-handler) is NOT default-enabled at ruff 0.16.2. It was stabilised in 0.16.0 (left preview), which is a different fact from being added to the default set. This row is in §4.1, headed "Already on by default - do not re-add, do not lose", so a reader who trusts it will omit LOG004 from `select` and lose the check that catches `.exception()` outside a handler. The file contradicts itself: its own MEASURED prefix distribution at line 153 says `LOG` 5, and its own fact pack `_work/facts/r12_lint_depth.md:82` and `:411` list only the five. (r12:455 carries the contrary error — the manifest took the wrong branch of a self-contradictory pack.)

**Source the auditor checked:**

ruff Default Rules page https://docs.astral.sh/ruff/default-rules/ — the LOG entries in the default `select` are exactly LOG001, LOG002, LOG009, LOG014, LOG015. Confirmed by live measurement: `uvx ruff@0.16.2 check --isolated --show-settings` lists G010 G101 G201 G202 LOG001 LOG002 LOG009 LOG014 LOG015 and NO LOG004. ruff 0.16.0 release notes list LOG004 under "Stabilization", not under the default-set expansion.

**Prescribed fix:**

Change the row to `| `LOG001`,`LOG002`,`LOG009`,`LOG014`,`LOG015` | logging API misuse | none | ...` and add `LOG004` to the §4.2 "Off by default" table with the note "stabilised in 0.16.0 but not default-enabled".

---

## 2. [CRITICAL] around line 500

**Quoted text being challenged:**

> `"google"` and `"pep257"` disable `D203`, `D213`, `D214`, `D215`, `D404`, `D405`, `D406`, `D407`, `D408`, `D409`, `D410`, `D411`; `"numpy"` disables that set plus `D212` and `D216`.

**What is actually true:**

Same defect as python_quality_gates_manifest.md:1618, repeated in the file that OWNS the rule set per PLAN.md. google and pep257 are not identical; numpy disables almost none of the listed codes; D216 does not exist. This file's §4.3 recommended config sets `convention = "google"`, so the wrong disable-list is attached directly to the config a reader will copy.

**Source the auditor checked:**

https://docs.astral.sh/ruff/settings/#lint_pydocstyle_convention plus live measurement (see the quality-gates finding above). D216 is rejected by ruff 0.16.2 as an unknown rule selector.

**Prescribed fix:**

Same replacement as above: google = D203, D204, D213, D215, D400, D401, D404, D406, D407, D408, D409, D413; numpy = D107, D203, D212, D213, D402, D413, D415, D416, D417; pep257 = D203, D212, D213, D214, D215, D404–D411, D413, D415, D416, D417, D420; drop D216.

---

## 3. [CRITICAL] around line 347

**Quoted text being challenged:**

> target-version = "py314"          # state it; never rely on requires-python inference

**What is actually true:**

This is the collection's ONLY copy-paste ruff config block, and it hard-codes py314 with no instruction that the value must equal the project's `requires-python` floor. Ruff's own settings doc defines target-version as the MINIMUM version: "Ruff will not propose changes using features that are not available in the given version", and treats `requires-python = ">=3.8"` as identical to `target-version = "py38"`. Meanwhile python_platform_baseline_manifest.md §3c is titled "Why the newest release is rarely the right floor" and its §3d floor table gives 3.10 (CPython window) or 3.12 (SPEC 0) as the defensible floors. An agent that follows the hub to a 3.11/3.12 floor and then pastes this block gets `"UP"` fixes that rewrite code into 3.13/3.14-only syntax — a SyntaxError on its own declared floor, published in a wheel that installs there. `target-version` occurs 6 times in the file (159, 168-171, 245, 347) and NEVER with the instruction to bind it to the floor; it is absent from the TL;DR (48-70) and from the 40-item anti-patterns checklist (1396-1470).

**Source the auditor checked:**

https://docs.astral.sh/ruff/settings/ (target-version: default "py310"; "Ruff will not propose changes using features that are not available in the given version"; requires-python treated identically) — fetched 8 Aug 2026; cross-read against python_platform_baseline_manifest.md §3c-3e lines 198-254

**Prescribed fix:**

Change line 347 to `target-version = "py312"        # MUST equal your requires-python floor (hub §3e); NOT the newest release` and add to the anti-patterns checklist: "- **`target-version` above the `requires-python` floor** — `UP` fixes then emit syntax that is a SyntaxError on the floor you publish (§2.4, hub §3e)."

---

## 4. [CRITICAL] around line 354

**Quoted text being challenged:**

> "D", "PL", "C90", "TC",         # each configured below

**What is actually true:**

The same config block leaves both exemption lists empty at lines 380-381 (`runtime-evaluated-base-classes = []   # fill before enabling TC001-TC003 (§5.2)` / `runtime-evaluated-decorators = []`). So the block ENABLES TC001-TC003 in exactly the state its own comment forbids. This is verbatim the file's own reject-on-sight anti-pattern at line 1414 ("**`TC001`-`TC003` enabled with empty `runtime-evaluated-*` lists** - the autofix can break a model at runtime"), its §3.2 verdict at line 269 ("enable-with-configuration ... can break pydantic/attrs at runtime unless the exemption lists are filled"), and its §5.2 row ("Both exemption lists default to `[]`, so protection is **off until configured**; `TC004` notices only *after* the fix lands"). The canonical artefact an agent will paste violates the file's own rejection list.

**Source the auditor checked:**

Internal: python_linting_practices_manifest.md lines 269, 380-381, 428, 1414 read against line 354. Confirmed mechanism at https://docs.astral.sh/ruff/rules/ (flake8-type-checking, runtime-evaluated-base-classes) — 8 Aug 2026

**Prescribed fix:**

Remove `"TC"` from `select` at line 354 and replace with `"TC004", "TC005", "TC007", "TC010",   # TC001-TC003 only after the runtime-evaluated-* lists below are filled (§5.2)`. Keep the two `runtime-evaluated-*` keys with the existing comment so the upgrade path is visible.

---

## 5. [MAJOR] around line 282

**Quoted text being challenged:**

> **Dead configuration nothing warns about.** `TRY200`, `PGH001`, `PGH002` were removed in v0.2.0 and `PT004` was removed - MEASURED. A removed code in `select` is **silently inert**

**What is actually true:**

Refuted for all four codes, and the label is MEASURED. TRY200/PGH001/PGH002 are redirects, not dead codes: ruff prints a warning AND enables the successor rule (so the config is not inert either — it silently enables B904/S307/G010). PT004 is a hard configuration error that stops ruff. The only genuinely silent case is a *preview* code selected by prefix.

**Source the auditor checked:**

Live measurement, ruff 0.16.2: `select = ["TRY200"]` → `warning: `TRY200` has been remapped to `B904`.`; `select = ["PGH001"]` → `warning: `PGH001` has been remapped to `S307`.`; `select = ["PGH002"]` → `warning: `PGH002` has been remapped to `G010`.`; `select = ["PT004"]` → `ruff failed / Cause: Rule `PT004` was removed and cannot be selected.`

**Prescribed fix:**

Rewrite as: "`TRY200`, `PGH001`, `PGH002` are redirects — ruff warns (`has been remapped to B904/S307/G010`) and enables the successor rule; `PT004` was fully removed and ruff refuses to run (`Rule PT004 was removed and cannot be selected`). Removed codes are therefore loud, not silent — MEASURED (0.16.2)."

---

## 6. [MAJOR] around line 184

**Quoted text being challenged:**

> A preview rule **cannot be selected at all** while preview is off - not by code, not by prefix, not by `ALL` - and selecting it is **silently ineffective**: no error, no warning, the rule never runs. `select = ["DOC501"]` with preview off is a config line an agent will read as "enforced" and be wrong about.

**What is actually true:**

The 'cannot be selected' half is correct; the 'no error, no warning' half is false for exact-code selection — ruff prints `Selection `X` has no effect because preview is not enabled.` It IS silent only when the preview rule is pulled in by *prefix* (`select = ["PLR"]` produced no warning). The claim is ESTABLISHED-tagged in the hazards file to ruff docs that do not support it. Same error at line 1407 ("it never runs; no error, no warning"), python_language_hazards_manifest.md:197-199, and python_quality_gates_manifest.md:1755 ("silently inert without `--preview`").

**Source the auditor checked:**

Live measurement, ruff 0.16.2, using the manifest's own example: `select = ["DOC501"]` → `warning: Selection `DOC501` has no effect because preview is not enabled.` Same warning for `extend-select` and for `--select DOC501` on the CLI, and for PLR0904, B909, RUF105, E111. https://docs.astral.sh/ruff/preview/ confirms the "not by code, not by prefix, not by ALL" half but says nothing about diagnostics.

**Prescribed fix:**

Rewrite as: "...and selecting it by exact code produces `warning: Selection `X` has no effect because preview is not enabled.` — a warning, not a failure, so it dies in CI log noise; selection by *prefix* is genuinely silent — MEASURED (0.16.2)." Apply the same correction at line 1407, python_language_hazards_manifest.md:197-199 and python_quality_gates_manifest.md:1755.

---

## 7. [MAJOR] around line 464

**Quoted text being challenged:**

> **MEASURED - the guard rail does not exist.** Selecting `D203, ISC001, COM812, E501, W191, Q000` alongside the formatter produced **no warning of any kind**. Ruff warns only about *mutually* incompatible lint rules (`D203`/`D211`, `D212`/`D213`), never about rules that fight the formatter.

**What is actually true:**

The guard rail exists and fires — but only from the `ruff format` subcommand, and only for COM812 and D203 (measured silent for W191, Q000, Q001-Q004, D206, D300, ISC001, ISC002, E501). The manifest's blanket refutation is wrong, and it explicitly overrode a fact pack that had the docs right ("the measurement wins") — the measurement was evidently taken from `ruff check`. The section heading at line 452 ("Formatter-owned - and ruff will not warn you") and line 473 ("two subcommands of the same binary undo each other and **neither warns**") are false on the same grounds: D203 is one of the two codes ruff format does warn about.

**Source the auditor checked:**

https://docs.astral.sh/ruff/formatter/#conflicting-lint-rules : "When an incompatible lint rule or setting is enabled, ruff format will emit a warning." Live measurement, ruff 0.16.2, with exactly that select list: `ruff format` (and `format --check`) prints `warning: The following rules may cause conflicts when used with the formatter: `COM812`, `D203`. To avoid unexpected behavior, we recommend disabling these rules...`. `ruff check` with the same config prints nothing.

**Prescribed fix:**

Rewrite as: "**MEASURED - the guard rail is partial and lives in the wrong subcommand.** `ruff format` warns `The following rules may cause conflicts when used with the formatter: COM812, D203` — but only for those two of the fourteen documented conflicts (W191, E111/E114/E117, D206, D300, Q000-Q004, COM819, ISC002 produce no warning), and `ruff check` never warns at all, so a lint-only CI step sees nothing." Retitle §6.1 to "Formatter-owned - and ruff warns about only two of them" and fix line 473.

---

## 8. [MAJOR] around line 351

**Quoted text being challenged:**

> "F", "E", "W", "I", "UP", "B", "C4", "SIM", "DTZ", "G", "LOG", "TRY", "BLE", "S",

**What is actually true:**

Diffing this `select` (lines 351-357) against the file's own MEASURED default-set prefix distribution (line 154-157) shows 8 default-on prefixes silently dropped: `ASYNC` (10 rules), `FURB` (17), `YTT` (10), `EXE` (4), `INT` (3), `FA` (2), `RET` (1), `ISC` (1). Because `select` REPLACES (the file's own §2.3, line 141-152: "`select = [\"E\", \"F\"]` on 0.16.x silently discards ~400 default rules"), pasting this block turns all ~48 of them off. The §3.2 per-family verdict table (lines 240-278) gives a verdict for 40 families but has NO ROW for ASYNC, FURB, YTT, EXE, FA, INT or RET — so the agent has no stated basis for the omission and no way to know it happened. The highest-stakes case is `ASYNC`: flake8-async carries the blocking-call-in-async-function family, and `grep -n 'ASYNC[0-9]' python_concurrency_determinism_manifest.md` returns ZERO hits, so a collection that ships a 1678-line concurrency manifest also ships a lint config that disables the only mechanical check for blocking I/O inside a coroutine.

**Source the auditor checked:**

Internal: python_linting_practices_manifest.md line 154-157 (MEASURED prefix distribution of the 413 defaults) diffed against lines 351-357; `grep -n 'ASYNC[0-9]' python_concurrency_determinism_manifest.md` → empty. Rule existence confirmed at https://docs.astral.sh/ruff/rules/blocking-sleep-in-async-function/ (ASYNC251, flake8-async) — 8 Aug 2026

**Prescribed fix:**

Add `"ASYNC", "FURB", "YTT", "EXE", "INT", "FA", "RET",` to the `select` list at line 356 (moving any individually contested code such as `RET504` into `ignore`), and add rows to the §3.2 table for ASYNC (**enable** — the only mechanical check for blocking calls in a coroutine; python_concurrency_determinism_manifest.md §-), FURB, YTT, EXE, INT, FA and RET so every default-on family carries a recorded verdict.

---

## 9. [MAJOR] around line 272

**Quoted text being challenged:**

> | `ISC` | **enable `ISC001`**; treat `ISC002` as formatter-adjacent | §6.1 |

**What is actually true:**

The file takes three incompatible positions on one rule. §3.2 line 272 says enable ISC001. §4.2 line 340 says the opposite: "| `E501`,`COM812`,`ISC001`,`Q000` | ... | formatter-owned; that they are off is correct, not an oversight (§6.1) |". And §4.3's config block neither selects `ISC` nor ignores it, so ISC001 is off. The same split hits `FBT`: §3.2 line 276 marks it "**contested, recommended**", §4.2 line 336 lists FBT001/FBT002 as high-value ("the boolean trap (§11.3)"), §11.3 (lines 807-828) is a whole section routing it **lint-catchable**, and the anti-patterns list carries "**A `bool` in a positional parameter**" — yet `FBT` is absent from `select`. In both cases the reviewer's verdict and the shippable config disagree, and the config is what gets pasted.

**Source the auditor checked:**

Internal: python_linting_practices_manifest.md lines 272, 276, 336, 340, 351-357, 807-828, 1436. ruff formatter-conflict list at https://docs.astral.sh/ruff/formatter/#conflicting-lint-rules (ISC001/ISC002 listed) — 8 Aug 2026

**Prescribed fix:**

Resolve to one position. Recommended: delete `ISC001` from the §4.2 row at line 340 (leaving E501/COM812/Q000), add `"ISC", "FBT",` to `select` at line 356, and add `"ISC002"` plus `"FBT003"` to the `ignore` list at line 359-364 with the reasons already given at §6.1 and §3.2.

---

## 10. [MINOR] around line 72

**Quoted text being challenged:**

> ## 1. The four layers, and the routing vocabulary

**What is actually true:**

The table immediately below (lines 77-83) has five rows: Formatter, Linter, Type checker, Test, Fitness function. "Fitness function" is not an aside — it is one of the six routing values the collection's enforcement ladder is built on (README.md:41-47 lists `fitness-function` as a first-class route, as does _work/PLAN.md's enforcement-route list), and this section is the file that defines the routing vocabulary. The heading undercounts the taxonomy it introduces.

**Source the auditor checked:**

python_linting_practices_manifest.md:77-83 (five-row table); README.md:41-47 (route table listing fitness-function as a peer route)

**Prescribed fix:**

Retitle "## 1. The five layers, and the routing vocabulary" and adjust the opening sentence if it depends on the count.

---

## 11. [MINOR] around line 1306

**Quoted text being challenged:**

> **Conflict noted:** a second verification pass could not confirm the threshold flag name from a primary page; re-verify before wiring

**What is actually true:**

The conflict was resolved, in the opposite direction, by the sibling and by the evidence base. python_quality_gates_manifest.md:1645-1648: "**Conflict noted and resolved:** one fact pack left interrogate's threshold flag name unverified; the flag `--fail-under` and the default of 80 were confirmed from interrogate's own README in the other pass, and that is what is stated here." The evidence base agrees: _work/facts/r14_measurement.md:866 cites interrogate's README.rst for "`--fail-under` (config default 80)"; only r10_quality_gates.md:186 left it OPEN. So the docstring-coverage rung's owning file carries a stale "do not wire this" hedge for a flag the collection has verified. The mirror-image case also exists: python_quality_gates_manifest.md:1664-1666 says the `--doctest-modules`/`--doctest-glob` family "were not verified against a primary page this pass — OPEN. Use `python -m doctest` until they are", while python_testing_tooling_manifest.md:432 cites the pytest 9.1.0 changelog entry for a `--doctest-modules` autouse-fixture regression, i.e. the flag is attested from a primary pytest page inside the collection (also _work/facts/r04_testing.md:60, :260).

**Source the auditor checked:**

python_quality_gates_manifest.md:1645-1648 and :1664-1666; python_testing_tooling_manifest.md:432; _work/facts/r14_measurement.md:866 vs _work/facts/r10_quality_gates.md:186 and :189; _work/facts/r04_testing.md:60

**Prescribed fix:**

In linting §15.2 replace the hedge with "`--fail-under` and the config default of 80 are confirmed from interrogate's README (see `python_quality_gates_manifest.md` §11.2, which resolved the conflicting fact packs)." In gates §11.3 replace the doctest-flag OPEN with "`--doctest-modules` is attested in pytest's changelog (see `python_testing_tooling_manifest.md`, which records the 9.1.0 autouse-fixture regression under it); the remaining unverified item is `--doctest-glob`'s pattern semantics."

---

## 12. [MINOR] around line 311

**Quoted text being challenged:**

> | `LOG001`,`LOG002`,`LOG004`,`LOG009`,`LOG014`,`LOG015` | logging API misuse | `LOG004` Sometimes | `.exception()` outside a handler logs `NoneType: None`; ...

**What is actually true:**

This row is in §4.1 "Already on by default - do not re-add, do not lose" and lists SIX LOG codes. The file's own MEASURED prefix distribution of the 413 defaults at line 155 says "`LOG` 5", and ruff's Default Rules page lists LOG001, LOG002, LOG009, LOG014, LOG015 — LOG004 is not among them (it exists and is not preview, "Added in 0.16.0", but is not default-enabled). One of the two tables is wrong about the exact fact §4.1 exists to establish. The config damage is contained because the recommended `select` uses the `"LOG"` prefix, but an agent building a `select` by copying §4.1's "do not re-add" list against §4.2's "off by default" list will classify LOG004 wrongly, and the internal contradiction weakens every other MEASURED default claim in the file.

**Source the auditor checked:**

https://docs.astral.sh/ruff/default-rules/ — LOG codes in the default set: LOG001, LOG002, LOG009, LOG014, LOG015 (fetched 8 Aug 2026); https://docs.astral.sh/ruff/rules/log-exception-outside-except-handler/ — LOG004 exists, "Added in 0.16.0", no preview badge, no default badge. Cross-read against python_linting_practices_manifest.md line 155

**Prescribed fix:**

Move `LOG004` out of the §4.1 row at line 311 (leaving `LOG001`,`LOG002`,`LOG009`,`LOG014`,`LOG015` = 5, matching line 155) and add it to the §4.2 off-by-default table with the note "`LOG004 log-exception-outside-except-handler` — added 0.16.0, stable but NOT default-enabled; the `.exception()`-outside-a-handler check that `logging_observability_manifest.md` §12a relies on, so it must be named or covered by the `LOG` prefix."

---

## 13. [MINOR] around line 333

**Quoted text being challenged:**

> `TRY400` recovers a lost traceback; its fix is safe for `logging.error` and unsafe for anything ruff cannot prove is a `logging.Logger` - set `lint.logger-objects`. `TRY300`/`TRY301` are contested and noisy

**What is actually true:**

The §4.3 config block selects the whole `"TRY"` prefix (line 351) and never sets `lint.logger-objects`; its default `[]` is mentioned only in the prose beneath the block (line 393). It also enables `TRY300` and `TRY301`, which this row and §3.2 line 252 both call contested/noisy, and which §Open-questions line 1480 lists as requiring "one recorded decision per contested family" — the block records no decision and no `ignore` entry for them. Same class as findings 2 and 5: the block does not implement the file's own reservations.

**Source the auditor checked:**

Internal: python_linting_practices_manifest.md lines 252, 333, 351, 359-364, 393, 1480. TRY400 fix safety per https://docs.astral.sh/ruff/rules/error-instead-of-exception/ — 8 Aug 2026

**Prescribed fix:**

In the config block, add `logger-objects = []                   # add project logger wrappers before trusting TRY400's fix (§4.2)` under a `[tool.ruff.lint]` line, and add `"TRY300", "TRY301",   # contested and noisy (§3.2); flip deliberately, not by prefix` to the `ignore` list at line 359-364.

---
