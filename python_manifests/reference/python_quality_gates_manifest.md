# Python Quality Gates & the Incremental Ratchet — Ground-Truth Manifest

**Purpose.** A citable ground-truth reference for the **enforcement rung** of the collection: which
checks run, where they run, how they fail, how a standard is adopted without a big-bang rewrite, and
which numbers are defensible as gates rather than as decoration. Target: **small-to-mid-scale,
strictly-typed, single-process Python**, reuse-first, functional core inside an imperative shell. It
grounds six decisions: (1) the gate ledger — every check, its exact command, its stage and its exit
contract; (2) local/CI parity — how one command becomes three invocations of the same artefact; (3)
the incremental-adoption ratchet and the arithmetic that makes it hold; (4) which supply-chain and
release gates are real and which are aspirational; (5) how a backward-incompatible change is
delivered incrementally (trunk, toggles, expand/migrate/contract, deprecation windows, the version
matrix); and (6) which measurements are gate-safe, which are diagnostic-only, and which must be
refused. The governing claim of the whole collection lands here: **advice that is not mechanically
enforced decays to zero, and a gate that cannot be adopted incrementally will be turned off.** This
file is **GROUNDING, not a rulebook**: cite a principle when it materially shapes a decision; reason
past it when the situation does not match. Every factual claim is tagged **ESTABLISHED** (normative
and stable in the cited primary source), **VERSION-DEPENDENT** (bound to the named version),
**OPEN** (no authoritative source — a decision the project must pin), **CC-FACT** (Claude Code
mechanics; none arise here), **MEASURED** (established by running the tool in this environment
rather
than by reading its documentation — strictly stronger than ESTABLISHED for tool behaviour, and it
always names the version it was measured against) or **UNVERIFIED** (asserted by a source but not
confirmed against a primary page this pass), with **FLAGGED-SECONDARY** inline wherever the
underlying evidence was a search summary rather than a rendered primary page.

**Scope.** This file **gates**; it does not re-teach what it gates. The type system itself is
`python_typing_contract_manifest.md`. The rule set, idiom catalogue and suppression *policy* are
`python_linting_practices_manifest.md`. Test *design* is `python_testing_tooling_manifest.md`.
Import contracts, packaging metadata and the deprecation *contract* are
`python_module_boundaries_manifest.md`. Hazard diagnosis is `python_language_hazards_manifest.md`.
Release dates and support windows are `python_platform_baseline_manifest.md`. See the closing
**Sibling manifests** block for the full split.

**Version anchor.** Interpreter, release-date and support-window facts: see
`python_platform_baseline_manifest.md` (verified 2026-08-08). Tool versions are this file's own
subject and are pinned below; every one was confirmed against the tool's PyPI JSON endpoint or its
own documentation on **2026-08-08**.

| tool | pinned version | released | tool | pinned version | released |
|---|---|---|---|---|---|
| ruff | 0.16.2 | 2026-08-07 | pip-audit | 2.10.1 | 2026-06-10 |
| ruff (release that changed defaults) | 0.16.0 | 2026-07-23 | bandit | 1.9.4 | 2026-02-25 |
| pre-commit | 4.6.1 | 2026-07-21 | semgrep | 1.172.0 | 2026-07-28 |
| uv | 0.12.3 | 2026-08-07 | zizmor | 1.29.0 | 2026-08-01 |
| nox | 2026.7.11 | 2026-07-12 | cyclonedx-bom | 7.3.1 | 2026-07-23 |
| tox | 4.58.0 | 2026-07-21 | vulture | 2.16 | 2026-03-25 |
| mypy | 2.3.0 | 2026-07-13 | complexipy | 6.2.0 | 2026-07-23 |
| pyright | 1.1.411 | 2026-06-25 | radon | 6.0.1 | 2023-03-26 (stale) |
| ty | 0.0.69 | 2026-08-06 | xenon | 0.9.3 | 2024-10-21 (stale) |
| mypy-baseline | 0.7.4 | 2026-04-13 | wily | 1.25.0 / 2.0.0a1 | 2023-10-11 / 2026-04-26 |
| pytest | 9.1.1 | 2026-06-19 | interrogate | 1.7.0 | 2024-04-07 |
| coverage.py | 7.15.4 | 2026-08-06 | import-linter | 2.13 | 2026-07-03 |
| pytest-cov | 7.1.0 | 2026-03-21 | grimp | 3.15 | 2026-07-03 |
| pytest-xdist | 3.8.0 | 2025-07-01 | Tach | 0.35.0 | 2026-05-12 |
| diff-cover | 10.4.2 | 2026-08-07 | pydeps | 3.0.7 | 2026-08-03 |
| mutmut | 3.7.0 | 2026-07-31 | pylint | 4.0.6 | 2026-06-14 |
| cosmic-ray | 8.4.6 | 2026-04-02 | flake8 | 7.3.0 | 2025-06-20 (14 months old) |
| Sphinx | 9.1.0 | 2025-12-31 | MkDocs | 1.6.1 | 2024-08-30 (23 months old) |
| | | | deptry | 0.25.1 | 2026-03-18 |

**VERSION-DEPENDENT (every row, as at 2026-08-08).** Standards this file depends on: PEP 751
(`pylock.toml`) Final; PEP 740 (index support for digital attestations) Final; PEP 770 (SBOMs inside
Python packages) Final; PEP 702 (`warnings.deprecated`) Final; PEP 257 (docstring conventions)
Active; CycloneDX 1.7, published as ECMA-424; SPDX 3.0 — **ESTABLISHED**.

---

## TL;DR

- **Pin every gate tool to an exact version and commit the resolved rule set.** ruff 0.16.0
  (2026-07-23) raised its default-enabled rule count from **59 to 413** and *removed* 18 codes from
  the defaults. A project that never wrote an explicit `select` had its coding standard rewritten by
  a routine version bump. An implicit default set is not a standard — **VERSION-DEPENDENT (ruff
  0.16.0)**.
- **Write down every gate's exit contract, because the tools disagree violently:** ruff `1`,
  coverage.py `2`, semgrep `1` only with `--error`, vulture `3`, zizmor `11`–`14`, pip-audit `1`.
  Any gate wired to `== 1` by assumption is silently disabled — **ESTABLISHED** (§1.3).
- **A gate exists exactly once and is invoked identically from the shell, the hook and CI.** The CI
  form of the hook runner is `pre-commit run --all-files`; the CI form of the environment is `uv run
  --locked` (`--frozen` skips the freshness check and is the *loose* flag) — **ESTABLISHED /
  VERSION-DEPENDENT (uv 0.12.x)** (§3).
- **Adopt incrementally with a ratchet, and make the ratchet mechanical rather than social.** A
  committed baseline compared against itself is not a ratchet: CI must compare HEAD's number against
  the *merge base's* number and fail on growth. Per-module strictness, baseline files and
  suppression budgets each have a stated cost and a documented way to rot — **ESTABLISHED
  (mechanism)** (§4).
- **Coverage detects unexecuted code; it cannot detect unverified code.** `fail_under` is one global
  number, exits **`2`**, and is compared at `[report] precision` — so 89.6% passes `fail_under = 90`
  at the default `precision = 0`. Gate changed lines, not the project average — **ESTABLISHED**
  (§6.1 for the wiring; `python_testing_tooling_manifest.md` §5a for the arithmetic).
- **Complexity metrics predict size, and defect-proneness only insofar as size does.** Gate
  cyclomatic complexity **per function** as a review trigger; never publish a project-average
  complexity and never fail a build on the Maintainability Index — **ESTABLISHED** as a
  characterisation of the cited evidence (§9.2).
- **Every mechanised gate in this file is a lower bound on badness.** A fully green pipeline over an
  incoherent design is the normal case, not an anomaly. §10.2 names what only a human can check.

---

## 1. What a gate is

### 1.1 Definition, and the four properties of a gate-safe check

A **gate** is a command with three committed properties: an exact invocation, a stage at which it
runs, and an exit contract that a machine reads. Anything missing one of the three is a suggestion.

A check or number is **gate-safe** only if all four of these hold — **OPEN** (the analyst's
criterion, composed from the tool semantics in §6 and §9; no primary source states it as a set):

1. **Per-unit, not aggregate.** It binds to a function, a module or a changed line, so a good part
   of the codebase cannot pay for a bad part.
2. **Monotone under genuine improvement.** Fixing the code moves the number the right way, always.
3. **Not satisfiable by deletion.** Removing code must not improve the score — or the measure must
   be paired with a counter-measure that deletion breaks (§10.1).
4. **Cheap enough to run at its stage.** A gate that costs more than the patience available at its
   stage acquires `continue-on-error: true` within a month.

### 1.2 Why standards, not preferences

**Adhere to Standards** (`adhere-to-standards`, an architecture tactic named in Bass, Clements &
Kazman, *Software Architecture in Practice*, 4th ed., 2021) is what makes a gate mechanical at all:
a house style with no published standard cannot be linted. In Python the standards gates attach to
are PEP 8 and PEP 257 (style, docstrings), PEP 517/518/621 (build, metadata) and PEP 484/544
(typing) — **ESTABLISHED** (vocabulary and citation carried from the SWE corpus seed pack). The
operational consequence: when a rule has no published referent it is a project convention, and it
must either be written down as one *and* given a mechanical form (a `ruff` code, a fitness-function
script) or dropped. Advice with neither a standard nor a mechanism is precisely what this collection
exists to eliminate.

### 1.3 Required versus advisory is an exit-code decision, not a sentiment

**ESTABLISHED** (composed from the per-tool exit semantics below). Required gates block the merge on
a non-zero exit. Advisory gates are neutered **explicitly and visibly** — `ruff check --exit-zero`,
`pip-audit` without `--strict`, `semgrep scan` without `--error`, a GitHub Actions step or job
carrying `continue-on-error: true`, or a SARIF upload with no failure branch. Every gate must be
labelled one or the other in configuration and never left ambiguous. A gate labelled nowhere is
"required by accident" or "off by accident", and which one you got is decided by the tool's default
rather than by you.

**The exit-code contract table.** Each row was read off the tool's own documentation on 2026-08-08.

| tool / command | success | the failure you care about | other codes | tag |
|---|---|---|---|---|
| `ruff check` | `0` = no violations **or all violations were auto-fixed** | `1` = violations remain | `2` = abnormal termination (invalid configuration, CLI error, internal error). `--exit-zero` forces `0`; `--exit-non-zero-on-fix` returns `1` even when every violation was fixed | ESTABLISHED |
| `coverage report --fail-under=N` | `0` | **`2`** = total under the threshold | `1` = error. Source constants: `OK, ERR, FAIL_UNDER = 0, 1, 2` | ESTABLISHED |
| `pip-audit` | `0` = "No known vulnerabilities were detected" | `1` = "One or more known vulnerabilities were found" | `--strict` fails the audit when *dependency collection* fails — it is not about findings | VERSION-DEPENDENT (2.10.x) |
| `semgrep scan` | `0` | `1` **only with `--error`** | `2` semgrep failed, `3` invalid syntax of the scanned language (**only under `--strict`**), `4` invalid pattern, `5` config not valid YAML, `7` invalid rule, `8` unknown language, `13` invalid API key | VERSION-DEPENDENT (1.172.x) |
| `semgrep ci` | `0` | non-zero on findings **by default** | as above | VERSION-DEPENDENT (1.172.x) |
| `zizmor` | `0` = audit ran, no findings | **`11`–`14`** = findings by highest severity (`11` informational → `14` high) | `1` = error *during* the audit, `2` = argument-parsing failure, `3` = no inputs collected | VERSION-DEPENDENT (1.29.0) |
| `vulture` | `0` = no dead code | **`3`** = dead code found | `1` = invalid input, `2` = invalid command-line arguments | VERSION-DEPENDENT (2.16) |
| `deptry .` | `0` = "Success! No dependency issues found." | `1` = one or more `DEP*` violations | none observed; deptry's usage page documents no exit code, so this row was measured rather than read | MEASURED (deptry 0.25.1) |
| `xenon` | `0` | non-zero "when any of these requirements is not met" (no specific code documented) | — | VERSION-DEPENDENT (0.9.3) |
| `radon` | always `0` | **there is none** — radon reports, it never fails | — | VERSION-DEPENDENT (6.0.1) |
| pre-commit hook contract | `0` **and** no file modified | "The hook must exit nonzero on failure **or modify files**" | a formatter that rewrites a file and exits `0` still fails the run | ESTABLISHED |
| `uv sync --locked` / `uv run --locked` | `0` | "If the lockfile is not up-to-date, uv will raise an error instead of updating the lockfile" | `--frozen` **skips the check** and therefore cannot detect a stale lockfile | VERSION-DEPENDENT (uv 0.12.x) |
| `pytest`, `mypy`, `bandit`, `interrogate`, `complexipy`, `diff-cover`, `lint-imports`, `tach check`, `mutmut` | non-zero on failure | — | **their exact code tables were not verified this pass** | OPEN |

**The rule this table encodes:** never write `if [ $? -eq 1 ]` after a gate. Test `-ne 0`, and where
the tool publishes a semantic code table (semgrep, zizmor, vulture, coverage.py) read the code and
branch on it explicitly. Three named inversions, each **ESTABLISHED**: coverage.py signals a
threshold failure with **`2`**, so a script testing `1` treats every failure as success; zizmor
signals findings with **`11`– `14`** and uses `1` for "the audit itself errored", so logic that
reads `1` as "findings" inverts every run; vulture signals dead code with **`3`** and uses `1` for
invalid input.

---

## 2. The gate ledger

### 2.1 The ledger

An agent should be able to build the pipeline from this table alone.

**Stage legend.** `E` editor / on save · `P` pre-commit hook · `U` pre-push hook · `C` CI on every
pull request · `M` merge gate (a required status check) · `R` release job only.

**Cost class** is an engineering estimate for a small-to-mid single-process repository and is tagged
**OPEN** — no runtime was measured for this file. What is *structural* rather than estimated: the
Rust-implemented single-pass tools (`ruff`, `zizmor`, `ty`, `complexipy`, Tach) are cheap enough for
`P`, while the whole-program Python tools (`mypy`, `pylint`, `pytest`, `mutmut`) belong at `C` or
later. Measure before placing anything, and re-place it when the measurement moves.

| # | gate | exact command | stage | req/adv | fails on | rewrites files? | cost class | tag |
|---|---|---|---|---|---|---|---|---|
| 1 | format | `ruff format` (pre-commit hook id `ruff-format`, `entry: ruff format --force-exclude`) | E P C | required | pre-commit: file modified | **yes** | trivial | VERSION-DEPENDENT (ruff 0.16.x) |
| 2 | lint | `ruff check` (hook id `ruff-check`, `entry: ruff check --force-exclude`) | E P C M | required | exit `1` | no (without `--fix`) | trivial | VERSION-DEPENDENT (ruff 0.16.x) |
| 3 | lint, inference-deep | `pylint <pkg> --fail-on=I0021` | C | advisory → required | non-zero; `--fail-on` forces failure on the named message | no | seconds–minutes | VERSION-DEPENDENT (pylint 4.0.6) |
| 4 | type check | `mypy <pkg>` (config in `[tool.mypy]`) | E C M | required | non-zero | no | seconds–minutes | VERSION-DEPENDENT (mypy 2.3.0) |
| 5 | type ratchet | `mypy <pkg> \| mypy-baseline filter` | C M | required during migration | any error absent from `mypy-baseline.txt` | no | as #4 | VERSION-DEPENDENT (0.7.4) |
| 6 | type check, 2nd opinion | the `ty` CLI (**subcommand name not verified this pass — OPEN**) | C | **advisory only** | non-zero | no | trivial | VERSION-DEPENDENT (ty 0.0.69 — still `0.0.x`) |
| 7 | library type completeness | `pyright --verifytypes <pkg> --ignoreexternal --outputjson` | C R | required for published libraries | completeness score below the committed floor (compare in a script) | no | seconds | VERSION-DEPENDENT (pyright 1.1.411) |
| 8 | tests | `pytest` | P (fast subset) C M | required | non-zero | no | seconds–minutes | VERSION-DEPENDENT (pytest 9.1.1) |
| 9 | coverage floor | `coverage run --branch -m pytest` then `coverage report --fail-under=<floor>` | C M | required | **exit `2`** | no | as #8 | ESTABLISHED |
| 10 | changed-line coverage | `diff-cover <coverage.xml>` against `git diff` | C M | required | threshold flag name **not verified** — OPEN | no | seconds | VERSION-DEPENDENT (10.4.2) / OPEN |
| 11 | mutation sample | `mutmut run`, then `mutmut export-cicd-stats` | scheduled, off the PR path | **never a gate** | — | writes `mutants/` | minutes–hours | VERSION-DEPENDENT (mutmut 3.7.0) |
| 12 | import contracts | `lint-imports` | P C M | required | any contract broken | no | seconds | VERSION-DEPENDENT (import-linter 2.13) |
| 13 | module interfaces + cycles | `tach check` | P C M | required (alternative to #12) | any violation | no | trivial | VERSION-DEPENDENT (Tach 0.35.0) |
| 13a | declared dependencies vs actual imports | `deptry .` | C M | required | any `DEP001`–`DEP005` violation — **exit `1`** | no | seconds | MEASURED (deptry 0.25.1) |
| 14 | cyclomatic complexity | `ruff check` with `C901` selected and `lint.mccabe.max-complexity` (default **10**) | P C | required | exit `1` | no | trivial | VERSION-DEPENDENT (ruff 0.16.x) |
| 15 | cognitive complexity | `complexipy . --max-complexity-allowed <N>` | C | advisory, then required | over threshold | no | trivial | VERSION-DEPENDENT (complexipy 6.2.0) |
| 16 | complexity, letter-grade | `xenon --max-absolute B --max-modules A --max-average A` | C | advisory | any rank requirement unmet | no | seconds | VERSION-DEPENDENT (xenon 0.9.3 + radon 6.0.1 — both stale) |
| 17 | dead code, gate tier | `vulture <pkg> --min-confidence 100` | C M | required | **exit `3`** | no | seconds | VERSION-DEPENDENT (vulture 2.16) |
| 18 | dead code, wide tier | `vulture <pkg> --min-confidence 60` plus a committed whitelist | C | advisory | exit `3` | no | seconds | VERSION-DEPENDENT (vulture 2.16) |
| 19 | security, code | `bandit -c pyproject.toml -r <pkg>` | C | advisory → required | non-zero | no | seconds | VERSION-DEPENDENT (bandit 1.9.4) |
| 20 | security, patterns | `semgrep scan --error --config <rules>` locally; `semgrep ci` in CI | C | required if adopted | `1` (see §1.3) | no | seconds–minutes | VERSION-DEPENDENT (semgrep 1.172.x) |
| 21 | workflow security | `zizmor --offline .github/workflows` (`--persona pedantic` when tightening) | P C | required | `11`–`14` | no | trivial | VERSION-DEPENDENT (zizmor 1.29.0) |
| 22 | lockfile freshness | `uv lock --check` (or `uv sync --locked`) | P C M R | required | lockfile out of date | no (with `--check`) | trivial | VERSION-DEPENDENT (uv 0.12.x) |
| 23 | dependency audit | `pip-audit --strict` | C R | required | `1` | no (without `--fix`) | seconds (network) | VERSION-DEPENDENT (2.10.x) |
| 24 | docstring shape | `ruff check` with `D` selected and `lint.pydocstyle.convention` set | P C | required | exit `1` | no | trivial | VERSION-DEPENDENT (ruff 0.16.x) |
| 25 | docstring content | `numpydoc lint` (pre-commit hook id `numpydoc-validation`) with an explicit `checks` allowlist | C | advisory → required | non-zero | no | seconds | ESTABLISHED |
| 26 | docstring presence | `interrogate --fail-under <N>` (config default `fail-under = 80`) | C | **advisory (diagnostic only — never required; §11.2)** | below threshold | no | trivial | VERSION-DEPENDENT (1.7.0) |
| 27 | executable examples | `python -m doctest -o ELLIPSIS -o NORMALIZE_WHITESPACE <files>` | C | required if you ship examples | any output mismatch | no | seconds | ESTABLISHED |
| 28 | docs build | your generator's build command, warnings treated as errors (**the `sphinx-build` / `mkdocs build` invocations were not verified against a primary page this pass — OPEN**) | C R | required | build error | writes build output | seconds–minutes | VERSION-DEPENDENT (Sphinx 9.1.0 / MkDocs 1.6.1) |
| 29 | suppression budget | `ruff check --statistics`; census via `ruff check --ignore-noqa --statistics` | C M | required (non-increasing) | committed budget exceeded (project script) | no | trivial | VERSION-DEPENDENT (ruff 0.16.2) |
| 30 | build | a PEP 517 build — one wheel, built once | C R | required | build error | writes `dist/` | seconds | ESTABLISHED |
| 31 | reproducible build | build twice with `SOURCE_DATE_EPOCH` set; compare digests | R | advisory → required | digest mismatch | writes `dist/` | seconds | ESTABLISHED (mechanism) / OPEN (exact `SOURCE_DATE_EPOCH` semantics) |
| 32 | SBOM | `cyclonedx-bom` 7.3.1, or `pip-audit --format cyclonedx-json` | R | advisory for an app; required if a consumer asks | generation error | writes the SBOM | seconds | VERSION-DEPENDENT (7.3.1) |
| 33 | publish | `uses: pypa/gh-action-pypi-publish@release/v1` with `permissions: id-token: write` | R | required | upload rejected (the index verifies attestations) | no | seconds | ESTABLISHED |
| 34 | version matrix | rows 2/4/8 re-run per interpreter leg | C | required | any leg non-zero | no | multiplies #8 | ESTABLISHED |

Notes bound to specific rows, each **ESTABLISHED** unless marked otherwise:

- **Rows 1–2, `--force-exclude` is not optional.** `respect-gitignore` is enabled by default and
  `force-exclude` is required to "Enforce exclusions, even for paths passed to Ruff directly on the
  command-line". pre-commit hands hooks explicit filenames, which otherwise bypass `exclude` — which
  is exactly why the official hook `entry` lines hard-code it. A hand-rolled ruff hook without it
  lints vendored and generated code. The same repo also exposes a bare `ruff` hook that the repo
  itself labels a **legacy alias** running `ruff check`; use `ruff-check`. All three hooks declare
  `types_or: [python, pyi, jupyter]` — **VERSION-DEPENDENT (ruff 0.16.x)**.
- **Row 6, ty is advisory by construction.** ty 0.0.69 is still on a `0.0.x` line: defensible as a
  second opinion, not as a required check, until it leaves `0.0.x` — **VERSION-DEPENDENT**.
- **Row 11, mutation testing is not a PR gate.** mutmut requires `fork`: "if you want to run on
  windows, you must run inside WSL". Adding `mutmut run` to a Windows matrix leg is a guaranteed
  failure.
- **Rows 12–13 are the CI wiring only.** Contract types, their options and their semantics belong to
  `python_module_boundaries_manifest.md`. This file owns one thing about them: **violations == 0 is
  a required gate, and the violation count is a tracked number rather than a boolean** (§9.5).
- **Row 13a is a different axis, not a third alternative.** deptry checks *declarations against
  imports*, so it neither replaces an import contract nor is replaced by one; the five `DEP*` rules,
  the declaration sources it reads and its `[tool.deptry]` options belong to
  `python_module_boundaries_manifest.md` §7.6, which lists `deptry .` among its day-one gates and
  notes it needs no configuration to start. Two facts a gate needs: it exits **`1`** on any
  violation
  and `0` when clean — **MEASURED (deptry 0.25.1)**, run against a package importing an undeclared
  dependency, since deptry's usage page documents no exit code; and its inline `# deptry: ignore` is
  a sixth suppression vocabulary that the §4.5 budget has to count.
- **Rows 16–18, staleness is a risk accepted explicitly.** radon 6.0.1 (2023-03-26) has an empty
  `requires_python` and classifiers stopping at Python 3.9; xenon is 0.9.3 (2024-10-21); wily's last
  stable is 1.25.0 (2023-10-11) with a `2.0.0a1` prerelease on 2026-04-26, so a plain install will
  not pick the prerelease up. No primary source claims Python 3.14 support for any of the three —
  verify on your target interpreter before making one of them required — **OPEN**.
- **Row 19, bandit will not find your config.** `[tool.bandit]` is supported but only when passed
  explicitly (`bandit -c pyproject.toml -r .`); bare `bandit -r .` ignores it. `exclude_dirs` exists
  in "YAML and TOML only", not in the INI `.bandit` file — **VERSION-DEPENDENT (bandit 1.9.x)**.
- **Row 23, `--strict` is about collection, not vulnerabilities.** Without it a dependency pip-audit
  could not resolve is skipped and the audit still exits `0`. Read pip-audit's own limits with it:
  "pip-audit is not a static code analyzer", and users "must not assume that pip-audit will defend
  you against malicious packages".

### 2.2 Stage assignment rules

Four rules decide a gate's stage — **OPEN** (composed from the stage and cost semantics above):

1. **Anything that rewrites a file runs at `P` (and `E`), never at `C`.** §3.5 gives the mechanism.
2. **Anything whose input is a single file runs at `P`; anything whose input is the whole program**
   (`mypy`, `pytest`, `lint-imports`, `vulture`) **runs at `C`** — promote it to `P` only after
   measuring.
3. **Anything needing the network or a credential runs at `C` or `R`,** and must have an offline
   local form (§3.4) or it will never be run before the push.
4. **`M` is a deliberately chosen subset of `C`.** A gate that runs at `C` but is not a required
   status check is advisory whatever the YAML implies.

### 2.3 What each gate may rewrite

**ESTABLISHED.** Exactly three gates may write to the working tree: the formatter (row 1); an
explicitly invoked autofix (`ruff check --fix`, run by a human or a hook, never in CI); and the
build (rows 30–32, which write only to `dist/` or the SBOM path). Everything else is read-only.
Ruff's fix machinery is a first-class axis with four settings — `lint.fixable`, `lint.unfixable`,
`lint.extend-safe-fixes` (promote unsafe to safe) and `lint.extend-unsafe-fixes` (demote safe to
unsafe) — and `--fix` applies **only safe fixes**, with unsafe fixes requiring `--unsafe-fixes`.
*Which* fixes a project promotes or demotes is a `python_linting_practices_manifest.md` decision;
that the promotion list is **committed** is a gate decision.

---

## 3. Local/CI parity — one command, three places

### 3.1 The failure mode, and the contract

**The failure mode.** CI enforces a different standard from the editor. Symptoms in order of
appearance: a red build for something that was green locally; a developer who stops running the
checks because they "don't match anyway"; and finally a second, divergent configuration maintained
inside the CI YAML. At that point the repository has two coding standards and the authoritative one
is whichever file the reviewer happened to read.

**The contract — OPEN** (the analyst's rule, built on the mechanisms below): a gate is defined
**exactly once**, in a file committed to the repository, and every stage *invokes that definition*
rather than restating it. Concretely: the tool's configuration lives in `pyproject.toml` (or the
tool's own dotfile); the *composition* of gates lives in `.pre-commit-config.yaml` and/or a
`noxfile.py`; and the CI YAML contains no tool flags at all — only the stage command. If a flag
appears in the CI YAML that does not appear locally, parity is already broken.

### 3.2 The three invocations

**ESTABLISHED** (pre-commit CLI surface, verified 2026-08-08):

| place | invocation | what it sees |
|---|---|---|
| developer, ad hoc | `pre-commit run --all-files` | every file in the repository |
| git hook | `pre-commit run` (installed) | **staged files only** |
| CI | `pre-commit run --all-files --show-diff-on-failure` | every file, and prints the diff the hooks produced |
| CI, changed-files mode | `pre-commit run --from-ref <base> --to-ref <head>` | only files changed between two refs |
| gates parked out of the default set | `pre-commit run --hook-stage manual` | hooks scoped `stages: [manual]` |

`--show-diff-on-failure` is what makes a CI formatter failure actionable: the log contains the exact
patch the developer must apply. **VERSION-DEPENDENT (pre-commit 4.6.1)** for the flag set.

**Four named traps in the wiring**, each **ESTABLISHED**:

1. **`pre-commit install` writes only the `pre-commit` git hook.** A hook declared `stages:
   [pre-push]` never runs unless `--hook-type pre-push` was installed or
   `default_install_hook_types` includes it. The gate looks configured and is inert.
   `--install-hooks` also builds the environments; `pre-commit install-hooks` builds environments
   without writing hook scripts.
2. **The stage names were renamed in pre-commit 3.2.0.** `commit`, `push` and `merge-commit` became
   `pre-commit`, `pre-push` and `pre-merge-commit`. The eleven valid stages are exactly
   `pre-commit`, `pre-push`, `pre-merge-commit`, `prepare-commit-msg`, `commit-msg`,
   `post-checkout`, `post-commit`, `post-merge`, `post-rewrite`, `pre-rebase`, `manual`. `pre-commit
   migrate-config` rewrites a legacy config — **VERSION-DEPENDENT (pre-commit >= 3.2.0)**.
3. **A hook fails when it modifies files, even at exit `0`.** "The hook must exit nonzero on failure
   or modify files." This is the design, not a bug: it is what makes an in-place formatter a gate.
4. **pre-commit passes explicit filenames, which defeats a tool's own `exclude`.** Hence
   `--force-exclude` on the ruff hooks (§2.1) and hence the need to check the same property for any
   hand-rolled hook.

**Pinning the hooks.** `pre-commit autoupdate` bumps `rev` pins; `--freeze` records the resolved
**commit hash** instead of the tag, which is the reproducible form (a tag can be moved).
`--bleeding-edge` follows the default branch, `--repo` narrows the update, `-j/--jobs` parallelises.
`pre-commit gc` prunes unused cached repos; `pre-commit try-repo` tests a hook repo before it enters
the config — **ESTABLISHED**.

### 3.3 The runner choice, honestly

The runner is the thing CI calls. Four options, and the honest verdict for the target scale:

| option | what it gives you | what it costs | verdict at small-to-mid scale | tag |
|---|---|---|---|---|
| `uv run --locked <cmd>` | the locked environment, no extra abstraction; `uv run` locks and syncs before invoking so "the project environment is always up-to-date" | no multi-interpreter matrix of its own; you write the loop in CI | **the default.** For a single-interpreter application this is the whole runner | VERSION-DEPENDENT (uv 0.12.x) |
| `pre-commit` | file-scoped gate composition, per-hook isolated environments, `--from-ref`/`--to-ref` | not a test runner; hooks with heavy dependencies fight the isolation | **use it for the file-scoped gates** (format, lint, workflow audit, docstrings) | ESTABLISHED |
| `nox` (2026.7.11) | sessions as **executable Python** in `noxfile.py`; `@nox.session(python=[...])`; `venv_backend` accepts `"uv"`, `"virtualenv"`, `"venv"`, `"conda"`, `"mamba"`, `"micromamba"`, `"none"`, chainable with `\|` to express fallbacks; `nox.options` carries `sessions`, `default_venv_backend`, `reuse_existing_virtualenvs`, `error_on_external_run`, `error_on_missing_interpreters`; `session.install`, `session.run(..., external=True)`, `session.notify`, `@nox.parametrize` | a `noxfile.py` is code, so it can grow logic nobody reviews | **the choice when you need a real matrix** — a library across interpreters | VERSION-DEPENDENT (nox 2026.7.11) |
| `tox` (4.58.0) | four config layouts: `tox.toml`; `pyproject.toml` `[tool.tox]` as native TOML; `[tool.tox]` holding a `legacy_tox_ini` string; legacy `tox.ini` | four layouts is four ways to be wrong; the native-TOML arrival version reached this pass only through search results citing tox's own changelog anchor, not a rendered page — **FLAGGED-SECONDARY / OPEN** | defensible, especially where a team already knows it; prefer one layout and say which | VERSION-DEPENDENT (tox 4.58.0) |

**The matrix-strictness switch is the discriminator.** nox's `error_on_missing_interpreters` is the
switch between a matrix gate that **fails** when an interpreter is absent and one that silently
skips — confirmed on nox's own configuration page. tox's counterpart could not be confirmed on a
primary page this pass — **OPEN**. This matters more than the config-format debate: a matrix that
skips a missing interpreter reports green for a leg it never ran.

**Scale note.** For a single-process application with one supported interpreter, `pre-commit` plus a
handful of `uv run --locked` commands is the entire runner story, and adding nox or tox is
over-engineering. Introduce a session runner at the moment you have a second interpreter leg or a
release-only job that must be reproduced locally.

### 3.4 Gates that cannot run locally, and the one exception

**OPEN** (the analyst's rule). Every required gate must have a local invocation. Where a tool's
default mode is CI-only, name the local form explicitly:

- `semgrep ci` is the pipeline form; `semgrep scan --error --config <file>` is the local one. Their
  failure semantics differ (§1.3), so pin the local form in the runner and let CI call it —
  otherwise the two modes drift — **VERSION-DEPENDENT (semgrep 1.172.x)**.
- zizmor performs online audits by default. `--offline` disables all online actions;
  `--no-online-audits` fetches inputs online but runs only offline audits; `--gh-token` supplies an
  API token. Gate on `--offline` so the check is runnable without a credential, and run the online
  audits as a scheduled advisory job — **VERSION-DEPENDENT (zizmor 1.29.0)**.
- **The one legitimate exception is publishing.** PyPI Trusted Publishing exchanges an OIDC token
  minted by the CI provider; there is no local equivalent by design. Release gates (ledger rows
  31–33) may be CI-only. Nothing else may be — **ESTABLISHED**.

### 3.5 The pipeline is a structure

**Deployment Pipeline** (Humble & Farley, *Continuous Delivery*, 2010, ch. 5 "Anatomy of the
Deployment Pipeline") names the shape: **one artefact, built once, promoted through stages**, where
each stage is a gating promotion of *the same* artefact — **ESTABLISHED** (vocabulary and citation
from the SWE corpus seed pack). In Python that artefact is one PEP 517 wheel; nox sessions or tox
environments define the stages and CI executes them. The rule that follows: **CI must never rebuild
the artefact between stages.** A test stage that installs from source while the release stage
installs a wheel is testing a different program.

**Script Deployment Commands** (a tactic named in Bass, Clements & Kazman, 2021) is the companion:
the runner targets plus the CI YAML are "documented, reviewed, tested, version-controlled" — which
is to say, the runbook is deleted and replaced by a committed command — **ESTABLISHED** (seed-pack
vocabulary).

**Autofix in CI is the parity anti-pattern with a mechanism.** `ruff check --fix` exits **`0`**
after rewriting files, because exit `0` covers "all violations were auto-fixed". A CI job that runs
`--fix` and trusts the exit code passes while leaving the tree dirty, and the fixes are discarded
when the runner is destroyed. Two correct forms: run `ruff check` without `--fix` in CI, or add
`--exit-non-zero-on-fix` — **ESTABLISHED**.

---

## 4. The incremental-adoption ratchet

This is the section that decides whether any of the rest gets adopted. A gate switched on at full
strength over an existing codebase produces thousands of findings, and the observed response is not
a cleanup — it is `--exit-zero`, a blanket ignore, or a deleted job.

### 4.1 The arithmetic that makes a ratchet hold

A ratchet is a pair: a **measure** `N` and a **committed bound** `B`, with CI failing when `N`
crosses `B` in the bad direction, and `B` moving only in the good direction. Five arithmetic
conditions — **OPEN** (the analyst's synthesis; the mechanisms cited under each are ESTABLISHED):

1. **Compare against the merge base, not against HEAD.** This is the condition most ratchets fail.
   If `B` lives in a committed file and CI compares `N(HEAD)` against `B(HEAD)`, then a pull request
   that regenerates the file passes trivially — the baseline *is* the head value. The mechanical fix
   is to read the bound from the base branch: compute `B_base` from the merge base's copy of the
   file (for example `git show "$(git merge-base origin/main HEAD):mypy-baseline.txt" | wc -l`) and
   fail when `N(HEAD) > B_base`. Without this step the ratchet is social: `mypy-baseline`'s own
   residual risk is precisely that "the baseline can be re-synced upward by anyone".
2. **`B` is committed, diffable and owned.** A bound stored in CI configuration or in a dashboard is
   not reviewable in the change that moves it. Put the number in the repository, and name an owner
   for each bound in the same file.
3. **Improving `B` is a separate, reviewable commit.** Never let the gate command regenerate its own
   bound as a side effect of a normal build.
4. **`B` moves in one direction and has a floor** — a stated terminal value (`0` suppressions,
   `--strict` everywhere, coverage floor `F`). A ratchet with no terminal value is an infinite
   tightening that eventually cannot be satisfied, and the response to an unsatisfiable gate is to
   disable it (see Anti-patterns).
5. **The step size and cadence are written down.** "Raise the coverage floor to the current value,
   rounded down, at each release" is a rule. "Raise it when it feels safe" is not, and produces
   either no movement or a surprise red build.

**The lie a rounded threshold tells** — the arithmetic is `python_testing_tooling_manifest.md`
§5a's;
the ratchet consequence is this file's. coverage.py compares `fail_under` at `[report] precision`,
whose default is `0`, so a real 89.6% is reported and compared as 90% and **passes** `fail_under =
90`. A ratchet whose step size is smaller than the rounding it is compared at does not move. Set
`precision = 2` so the number you committed is the number compared, and pin coverage.py to an exact
patch because `precision` participates in the comparison — **ESTABLISHED**.

### 4.2 Mechanism inventory: what each costs, and how it rots

| mechanism | exact form | what it costs | how it rots | tag |
|---|---|---|---|---|
| **Per-module strictness** | `[[tool.mypy.overrides]]` with `module = [...]` in `pyproject.toml`, or `[mypy-pattern1,pattern2]` in `mypy.ini` | one config block per legacy module; a precedence model you must know (§4.3) | override blocks accumulate and are never deleted; nobody notices that new modules were added to an existing loose pattern | ESTABLISHED |
| **Error baseline** | `mypy \| mypy-baseline sync` writes `mypy-baseline.txt`; `mypy \| mypy-baseline filter` reports only new errors | a large committed file, and a tool that "works exclusively with the stdout of mypy" — so a mypy output-format change invalidates it | re-`sync` on a red build silently raises the bound; fix with condition 1 of §4.1 | VERSION-DEPENDENT (0.7.4) |
| **Suppression budget** | committed integer; census with `ruff check --statistics` and `ruff check --ignore-noqa --statistics` | a project script and a number to maintain | debt migrates from inline comments into config (`per-file-ignores`, `ignore_errors`) where a comment census cannot see it (§4.5) | VERSION-DEPENDENT (ruff 0.16.2) |
| **Changed-lines gate** | `diff-cover` against a Cobertura/Clover/JaCoCo or LCov report plus `git diff` | requires an XML/LCov artefact and git history in CI (shallow clones break it) | rewards touching few lines: a large honest refactor scores worse than a one-line hack | VERSION-DEPENDENT (10.4.2) |
| **Coverage floor pinned to current** | `[report] fail_under` at the current value, `precision = 2` | nothing beyond discipline | the floor is raised to an aspiration instead of to the measured value, and then lowered again | ESTABLISHED |
| **Bulk suppression as a one-time baseline** | `ruff check --add-noqa[=<REASON>]` or `--add-ignore[=<REASON>]` | writes a suppression on **every** current violation | it is a debt-*creation* tool: used because CI was red, it deletes the signal permanently | VERSION-DEPENDENT (ruff 0.16.2) |
| **Soft-fail edge marker** | Tach's `deprecated` marker on a declared dependency edge | none | the marker is permanent; nothing expires it | ESTABLISHED |
| **Advisory-then-required promotion** | `continue-on-error: true`, or `ruff check --exit-zero`, with a dated removal | nothing | the date passes and nobody removes it — the single most common ratchet failure | ESTABLISHED |
| **`ignore_errors` per module** | `[[tool.mypy.overrides]] ignore_errors = true` (config-file only) | the module is unchecked, wholesale | it is *also* the honest form: one reviewable marker beats ignores scattered through source | ESTABLISHED |
| **`follow_imports = "skip"`** | mypy per-module | **do not use as a ratchet.** It makes the module `Any` and erases errors at the boundary instead of reporting them | silent and total; `ignore_missing_imports` and `silent` are the narrower tools | ESTABLISHED |

### 4.3 Per-module strictness, and the precedence that surprises people

**ESTABLISHED.** mypy's documented precedence, highest first: (1) inline configuration in the source
file; (2) sections with concrete module names (`foo.bar`); (3) unstructured wildcard patterns
(`foo.*.baz`), later sections overriding earlier; (4) well-structured wildcard patterns
(`foo.bar.*`), more specific overriding more general; (5) **command-line options**; (6) top-level
configuration-file options.

Two consequences an agent must internalise:

- **The command line loses to a per-module section.** `mypy --strict` does **not** override
  `[[tool.mypy.overrides]] disallow_untyped_defs = false`; the override wins. A CI job that adds
  `--strict` to a repository with loose overrides has changed nothing for those modules.
- **`strict` cannot be set per-module.** `strict` is documented as "Enable all optional error
  checking flags" and the configuration reference shows no per-module support. A "strict for new
  code, loose for legacy" ratchet must therefore **enumerate the individual flags** in each override
  block. Writing `strict = true` inside `[[tool.mypy.overrides]]` does not do what it looks like.

**The per-module flag list**, which is what a ratchet actually writes — the canonical `--strict` set
is `python_typing_contract_manifest.md` §1's, and what this list adds is which members of it have
per-module support: `disallow_untyped_defs`,
`disallow_incomplete_defs`, `disallow_untyped_calls`, `disallow_any_generics`,
`disallow_subclassing_any`, `disallow_untyped_decorators`, `check_untyped_defs`, `warn_return_any`,
`no_implicit_reexport`, `strict_equality`, `warn_unused_ignores` — **VERSION-DEPENDENT (mypy 2.3)**.
`warn_redundant_casts` is **global-only** (it appears on mypy's global-only list alongside
`python_version`, `platform`, `files`, `exclude`, `namespace_packages`, `plugins`, `num_workers`,
`warn_unused_configs`, `incremental`, `cache_dir` and every reporting flag), and per-module support
for `extra_checks` was not confirmed this pass — **OPEN**. So a per-module block reproduces eleven
of the thirteen flags `--strict` enables; the remaining two must be set globally or accepted as
absent.

**Set `warn_unused_configs` globally.** It is the check that tells you an override block matches no
module — the mechanism by which a stale ratchet entry becomes visible — **ESTABLISHED**.

### 4.4 Baseline files

**VERSION-DEPENDENT (mypy_baseline 0.7.x).** `mypy_baseline` 0.7.4 records existing errors in a
committed baseline the project describes as "carefully crafted to avoid merge conflicts" and
"human-readable", reports only newly introduced errors, and regenerates the file with `mypy-baseline
sync`. It works exclusively with mypy's stdout — no plugin, no patching — which is both its virtue
(nothing to break on a mypy upgrade except the output format) and its limit.

Three rules for using it as a ratchet rather than as a permanent amnesty — **OPEN** (the analyst's
rules):

1. CI compares the baseline's size against the **merge base's** size and fails on growth (§4.1,
   condition 1). Without this the ratchet does not exist.
2. A `sync` that grows the file is a separate commit with a written reason in the message, reviewed
   as a policy change rather than as a build fix.
3. The baseline has a stated end date or a stated shrink rate. "Shrinks by at least N lines per
   release, terminal value 0" is a ratchet; "we'll get to it" is a file that grows.

**The reviewability property is the point.** Because the baseline is human-readable and committed,
reviewers see exactly which errors were resolved and which were introduced in each change. That
property is destroyed by any process that regenerates the file automatically.

### 4.5 The suppression budget

Suppression debt is the one number in this file that is both trivially countable and genuinely
diagnostic. A repository running the ledger of §2.1 carries **six** distinct suppression
vocabularies
simultaneously — ruff (`# noqa: CODE`, and since 0.16.0 `# ruff: ignore[CODE]` / `# ruff:
file-ignore[CODE]`), mypy (`# type: ignore[code]`), bandit (`# nosec B602, B607`), semgrep
(`nosem`),
zizmor (`# zizmor: ignore[audit-name]`) and deptry (`# deptry: ignore[DEP001,DEP003]`, which must
sit
on the `import` line and cannot silence `DEP002` or `DEP005` —
`python_module_boundaries_manifest.md`
§7.6) — **ESTABLISHED / VERSION-DEPENDENT (ruff 0.16.0, deptry 0.25.1)**. A budget that counts only
one of them measures nothing.

**The census mechanism is exact, not approximate.** `--ignore-noqa` makes ruff disregard every `#
noqa` in the tree; the delta between a normal `--statistics` run and an `--ignore-noqa --statistics`
run **is** the ruff-side suppression debt, per rule. `--statistics` prints a count per triggered
rule, code and name, one per line, tab-separated — **VERSION-DEPENDENT (ruff 0.16.2)**.

**The budget definition — OPEN** (a project convention; nothing computes it for you):

```
S = count("# type: ignore")            # mypy, inline
  + count("# noqa") + count("ruff: ignore") + count("ruff: file-ignore")
  + count("# nosec") + count("nosem") + count("zizmor: ignore")
  + count("deptry: ignore")
  + lines(mypy-baseline.txt)
  + entries(lint.per-file-ignores)     # config-level, or the budget is gameable
  + blocks([[tool.mypy.overrides]] with ignore_errors = true)
  + entries([tool.deptry] ignore, per_rule_ignores)
```

The **config-level** terms — the last three — are what make it honest: without them, the cheapest
way
to reduce `S` is to move a line suppression into `lint.per-file-ignores` — where `"An initial '!'
negates the file pattern"`, so a single entry can cover most of a tree — or into an `ignore_errors`
override, or into `[tool.deptry] per_rule_ignores`. Counting only inline comments rewards laundering
debt into configuration.

**The rules that keep the suppressions themselves honest are required gates, not preferences** — but
their exact rule codes, each one's default status and fix class, and the per-checker mirror are
owned
by `python_linting_practices_manifest.md` §8.2–§8.3. This section gates the census those rules
produce, and adds the two obligations the rule set alone does not carry: **all of them are enabled,
including the ones that are off by default**, and where a textual rule and a checker-computed rule
overlap, **both** are on — the lint rule is what catches the comment in files the checker is not
covering yet. One is inert without a CI flag: pylint's stale-disable message must be made fatal with
`--fail-on=I0021` (ledger row 3) or the run still exits `0` — **VERSION-DEPENDENT (pylint 4.0.6)**.

**Two fix hazards, both ESTABLISHED.** `RUF100 --fix` deletes directives it believes unnecessary,
and ruff's own guidance is that when running it alongside pylint or mypy you must "separate their
directives with a second `#` character to prevent removal" — otherwise a `# noqa` meant for a
checker ruff does not implement is stripped. And `PGH004 --fix` "may introduce additional
diagnostics", because turning `# noqa F401` into `# noqa: F401` makes a previously blanket
suppression specific and therefore un-suppresses everything else on that line. Both are correct
behaviour and both are surprising build breaks.

**No ruff rule requires a *reason* on a suppression.** `--add-noqa[=<REASON>]` and
`--add-ignore[=<REASON>]` can write one; nothing checks that one is present — a search of all rule
explanations found no rule mandating justification text. "Every suppression carries a reason" is
therefore **contract-only** unless the project adds a grep-based fitness function; say which you
chose — **VERSION-DEPENDENT (ruff 0.16.2)** for the absence, **OPEN** for the convention.

**Ruff is steering away from `noqa`.** Two preview rules encode the intended end state: `RUF105`
`noqa-comments` ("`noqa` comment used instead of `ruff: ignore`") and `RUF106`
`rule-codes-in-suppression-comments` ("Rule code used instead of name in suppression comment"). Both
are preview. A project standardising its suppression vocabulary today should know which direction
the tool is moving, and should not adopt preview rules as required gates — **VERSION-DEPENDENT (ruff
0.16.2)**.

### 4.6 The new-code gate — the ratchet that converges on its own

**ESTABLISHED.** The canonical industrial form of this ratchet scopes every condition to *new* code.
SonarQube's default quality gate is exactly six conditions, all so scoped: no new bugs (Reliability
rating A), no new vulnerabilities (Security rating A), new code has limited technical debt
(Maintainability rating A), all new Security Hotspots reviewed, **new-code test coverage >= 80.0%**,
and **duplication in new code <= 3.0%**. "New code" is definable as the previous version, the last X
days, a specific analysis, or a reference branch. The documented rationale for why this converges is
worth quoting, because it is the argument for the whole section: "When you add new code to your
projects, you usually touch a portion of the old code in the process. As a consequence, analyzing
and cleaning new code allows you to fix issues in your old code and gradually improve the overall
quality of your codebase."

**The self-hosted equivalents**, per gate family: `diff-cover` for the coverage half ("Diff coverage
is the percentage of new or modified lines that are covered by tests. This provides a clear and
achievable standard for code review: If you touch a line of code, that line should be covered") —
**ESTABLISHED**; `pre-commit run --from-ref <base> --to-ref <head>` for the file-scoped lint half —
**ESTABLISHED**; `semgrep --baseline-commit <hash>`, which shows "only results that are not found in
this commit hash" — **VERSION-DEPENDENT (semgrep 1.172.x)**; and per-module strictness plus a
baseline for the typing half (§4.3–4.4).

**The known weakness of any changed-lines gate — ESTABLISHED.** It rewards touching few lines. A
large, honest refactor can score worse than a one-line hack, and a developer who learns this
optimises for small diffs. Pair it with review, and never make the changed-lines percentage the only
test gate.

### 4.7 Which mechanisms rot, and what replaces them

**OPEN** (the analyst's judgement, from the cost/rot column of §4.2). In order of rot speed:
`continue-on-error: true` with no removal date (indistinguishable from no gate); bulk `--add-noqa`
(instant and permanent — the signal is gone); per-module override blocks (slow and invisible, which
is why `warn_unused_configs` is not optional); a baseline file (decays exactly as fast as reviewers
stop reading its diff). The mechanisms that do **not** rot are those where CI recomputes the bound
from the merge base every run — there is no artefact for entropy to act on.

---

## 5. Type checking as a gate

The type system is `python_typing_contract_manifest.md`. This section is only about making a checker
into a gate: which error codes are on, how ignores stay honest, and how the ratchet applies.

### 5.1 Error-code selection — what `--strict` does not give you

The exact `--strict` flag set and the full optional-error-code inventory are owned by
`python_typing_contract_manifest.md` §1 — **thirteen** flags as of mypy 2.3. This file does not
reproduce either list, because mypy's own documentation warns that "the exact list of flags enabled
by running `--strict` may change over time", and a list transcribed into two files disagrees with
itself on the next bump. What a gate needs *from* that list is gate content rather than typing
content, and it stays here.

**Some optional error codes arrive *indirectly*,** switched on by their governing strictness flag
rather than by `--enable-error-code`: `--disallow-untyped-defs` yields `no-untyped-def`,
`--warn-return-any` yields `no-any-return`, `--strict-equality` yields `comparison-overlap`,
`--warn-redundant-casts` yields `redundant-cast`, `--warn-unused-ignores` yields `unused-ignore`.
That is why `--strict` appears to produce some of them, and why a gate cannot be fully specified by
listing error codes alone — **VERSION-DEPENDENT (mypy 2.3)**.

**The high-value codes `--strict` does NOT give you, and which a gate must request explicitly:**
`unreachable`, `possibly-undefined`, `redundant-expr`, `ignore-without-code`, `explicit-override`,
`mutable-override`, `truthy-bool`, `explicit-any`, `exhaustive-match` — **VERSION-DEPENDENT (mypy
2.3)**. "We run `--strict`" is therefore *not* the same claim as "we check for unreachable code".
The
inventory these nine are drawn from is in the owning file; select from it there, and commit the
resolved `enable_error_code` list here.

`disable_error_code` and `enable_error_code` take comma-separated code lists, and **enable wins**:
the option "will override disabled error codes from the `disable_error_code` option" —
**ESTABLISHED**. Two codes carry gate obligations from other sections: `deprecated` closes the
deprecation loop (§8.4) and `exhaustive-match` is the checked form of the exhaustiveness discipline
that `error_tracing_contract_manifest.md` owns.

**mypy 2.0 changed defaults, which is a gate event.** `--local-partial-types` is now on by default;
`--strict-bytes` is on by default, so "mypy no longer treats `bytearray` and `memoryview` values as
assignable to the `bytes` type"; `--allow-redefinition` now behaves like `--allow-redefinition-new`;
targeting Python 3.9 was dropped; and parallel checking arrived as `--num-workers`. A configuration
written against mypy 1.x that relied on `bytearray` being assignable to `bytes` starts failing on
upgrade with no config change — **VERSION-DEPENDENT (mypy 2.0+)**.

### 5.2 Ignore hygiene as a gate

Three primitives, all **ESTABLISHED**: `warn_unused_ignores` (default `False`) "Warns about unneeded
`# type: ignore` comments"; the optional code `ignore-without-code` rejects a bare `# type: ignore`
and forces `# type: ignore[error-code]`; `unused-ignore` is the code form of the stale-ignore
diagnostic. `ignore_errors` (default `False`, configuration-file only) "Ignores all non-fatal
errors" for matched modules — which makes it the *reviewable* marker for a not-yet-migrated module,
unlike ignores scattered through source.

**`follow_imports` is the hazard.** It has exactly four values — `normal` (default), `silent`,
`skip`, `error` — and governs an imported `.py` module not named on the command line. **`skip` makes
that module effectively `Any`,** erasing errors at the boundary instead of reporting them. Reached
for as a quick fix for a noisy dependency, it silently deletes type checking across that boundary;
`ignore_missing_imports` and `silent` are the narrower tools — **ESTABLISHED**.

**pyright does not police stale ignores unless told to.** `enableTypeIgnoreComments` defaults to
`true` in off/basic/standard/strict, so pyright honours PEP 484 `# type: ignore`; but
`reportUnnecessaryTypeIgnoreComment` defaults to `"none"` in **all four** modes, including strict.
If pyright is the gate, that switch is a required config line — **VERSION-DEPENDENT (pyright, `main`
docs; version not pinned this pass — OPEN)**.

### 5.3 The typing ratchet, in order

**OPEN** (the analyst's sequence; each mechanism is cited above). The order matters because each
step is green before the next begins:

1. **Turn the checker on with zero strictness and make it required.** The gate is "mypy runs and
   exits `0`", nothing more. Fix crashes and missing stubs only.
2. **Add the codes that find bugs rather than demand annotations** — `unreachable`,
   `possibly-undefined`, `redundant-expr`. These usually produce a small, real finding list.
3. **Enforce ignore shape before reducing ignore count:** `ignore-without-code` and `PGH003`, then
   `warn_unused_ignores` and `RUF100`. Shape first, because a coded ignore can be counted and a bare
   one cannot.
4. **Baseline the remainder** (§4.4) and wire the merge-base comparison.
5. **Ratchet strictness per module** (§4.3), newest and most-central modules first, enumerating
   flags.
6. **Terminal state:** every override block deleted, `strict` global, baseline file removed. Write
   that end state down at step 1 — it is the floor required by §4.1 condition 4.

### 5.4 Type coverage as a number, not a feeling

**ESTABLISHED.** Strictness and coverage are different measurements: strictness *creates errors*,
coverage *counts annotations*. `mypy --strict` does not report what fraction of the code is
annotated. The reports that do: `--any-exprs-report` produces "a text file report documenting how
many expressions of type `Any` are present within your codebase"; `--linecount-report` documents
"the functions and lines that are typed and untyped within your codebase"; `--lineprecision-report`
gives "per-module statistics of how many lines are typechecked". `--html-report`, `--txt-report` and
`--cobertura-xml-report` require lxml, i.e. `mypy[reports]`, or they fail at runtime.

**For a published library there is one defensible scalar.** `pyright --verifytypes <IMPORT>`
verifies "completeness of types in py.typed package"; the **type completeness score** is "the
percentage of symbols with known types". A symbol counts as unknown or ambiguous when class or
instance variables or methods lack annotations or refer to unknown types, when parameters or return
types lack annotations, when generic classes lack type arguments, or when a type alias references
partially specified generics. `--ignoreexternal` ignores incomplete types imported from other
external packages; `--outputjson` makes it scriptable — **ESTABLISHED**. Two limits: it measures a
`py.typed` package's **public surface** only, so run on an application package it yields a number
that means very little; and without `--ignoreexternal` it penalises you for your dependencies'
missing types.

---

## 6. Test gates

Test *design* — the unit/integration boundary, what to assert, fixtures, property-based testing — is
`python_testing_tooling_manifest.md`. This section is only about turning a suite into a gate.

### 6.1 Coverage as a gate: the commands, the exit contract, the required config

The measurement semantics every value below depends on — how `fail_under` compares, what `precision`
does to that comparison, why there is no per-file threshold, what branch coverage actually counts,
which `[run]` core is in use, and how `exclude_lines`, `parallel`, `relative_files` and `[paths]`
behave — are owned by `python_testing_tooling_manifest.md` §5a. This section only wires them.

**The commands — ESTABLISHED:**

```
coverage run --branch -m pytest        # measure
coverage report --fail-under=<floor>   # gate
coverage report --format=total         # the scriptable scalar
coverage xml                           # or `coverage lcov` — diff-cover's input
diff-cover coverage.xml                # the changed-lines gate (threshold flag OPEN, §2.1 row 10)
```

`--format` reads "Output format, either text (default), markdown, or total"; the sibling report
commands are `coverage json`, `coverage lcov`, `coverage xml`, `coverage html`, `coverage annotate`
and `coverage combine` — **ESTABLISHED**.

**The exit contract — ESTABLISHED.** A `fail_under` breach exits **`2`**, not `1`: "If the total
coverage measurement is under this value, then exit with a status code of 2", and the source
constants are `OK, ERR, FAIL_UNDER = 0, 1, 2`. A script branching on `1` treats every threshold
failure as a pass. §1.3 is the general form of the trap.

**The required config values.** Each setting and its default is **ESTABLISHED** in the owning file;
the *required value* is this file's gate decision, and the floor itself is **OPEN**:

| setting | value a gate requires | why it is not optional |
|---|---|---|
| `[run] branch` | `true` | it is off by default, so an ungated "90%" is 90% of *statements* |
| `[report] precision` | `2` | it defaults to `0` and participates in the `fail_under` comparison |
| `[report] fail_under` | the current measured floor, raised only after it has been exceeded | it is one global number, and there is no per-file form |
| `[report] exclude_also` / `partial_also` | these, never `exclude_lines` / `partial_branches` | the replacing forms delete the built-ins, `pragma: no cover` among them |
| `[run] parallel`, `[run] relative_files`, `[paths]` | all three, whenever the run is sharded or containerised | without them `coverage combine` reports a fraction of the true number |
| a changed-lines gate | `diff-cover` against the merge base | the project average cannot fail on a 0%-covered new module |

**One gate obligation that follows from the semantics rather than from a setting — ESTABLISHED.**
Some partial branches are not defects: coverage.py cannot recognise every intentionally partial
construct, and a generator expression that never raises `StopIteration` reports a false partial. The
remedy is `# pragma: no branch` or a `[report] partial_branches` regex, **not** a test. An agent
that
"fixes" a false partial by adding a test has written a test for nothing.

### 6.2 What coverage is and is not evidence of

**ESTABLISHED, and this is the largest study available.** Inozemtseva & Holmes, *Coverage Is Not
Strongly Correlated with Test Suite Effectiveness* (ICSE 2014), generated **31,000 test suites**
over five Java systems of up to 724,000 SLOC and measured effectiveness by mutation kill. Ignoring
suite size, Kendall's tau between coverage and non-normalised effectiveness was 0.81–0.95 across
statement, decision and modified-condition coverage (all significant at the 99.9% level).
Normalising effectiveness by covered mutants collapsed it to 0.50–0.83, with HSQLDB at **−0.35**.
Their conclusion, verbatim: "We found that there is a low to moderate correlation between coverage
and effectiveness when the number of test cases in the suite is controlled for. In addition, we
found that stronger forms of coverage do not provide greater insight into the effectiveness of the
suite. Our results suggest that coverage, while useful for identifying under-tested parts of a
program, should not be used as a quality target."

The mechanical statement of the same point — **ESTABLISHED**, derived from the coverage semantics
owned by `python_testing_tooling_manifest.md` §5a:
`fail_under` is one global number computed from executed lines, and execution is not verification. A
suite of assertion-free tests raises the number without adding a single obligation. **The gate
detects unexecuted code; it cannot detect unverified code.**

**So the coverage gate is:** branch coverage on, `precision = 2`, `fail_under` pinned to the current
measured floor and raised only after being exceeded, plus a changed-lines gate. It is a required
gate because a *falling* number is real information. It is not a target, and the number itself is
not reported as a quality figure. Goodhart's exposure here is covered in §10.1.

### 6.3 The ban on assertion-free tests

**OPEN — and this is a gap, stated as one.** No first-party pytest option and no maintained, widely
used plugin that **fails** a test containing no assertion was confirmed this pass. The survey behind
that absence, and the two mechanisms that remain — a project-local `pytest_collection_modifyitems`
AST check in `conftest.py`, or mutation testing as the oracle for assertion strength — are owned by
`python_testing_tooling_manifest.md` §5b; §6.6 owns the scheduling of the second.

**The gate consequence is the whole of this section.** Neither mechanism is wired by any tool in the
ledger, so the rule is **contract-only** until the project writes one of them. State which you
chose,
in the repository, as open question 7. "We ban assertion-free tests" with neither mechanism in place
is exactly the kind of unenforced advice this file exists to reject.

**pytest gate hardening that *is* verified — ESTABLISHED.** `xfail_strict` defaults to **`False`**,
so a test marked `xfail` that starts passing is reported as `xpass` and the suite stays green — a
fixed bug never removes its own marker. Set it to `True`. `--strict-markers` makes unregistered
marks errors; `--strict-config` makes configuration errors failures; `required_plugins` and
`minversion` fail closed when the environment is not the intended one; `filterwarnings` promotes
warnings to errors (§8.4); `testpaths`, `norecursedirs` and `--import-mode` fix what is collected
and how; `-x`/`--maxfail` bound the run; `--durations` reports slow tests (§6.5). All confirmed in
pytest's reference — **VERSION-DEPENDENT (pytest 9.1.1)**.

### 6.4 Flakes: the doctrine, and quarantine

**ESTABLISHED — pytest's own framing, which is a diagnosis and not a mitigation.** "A flaky test
indicates that the test relies on some system state that is not being appropriately controlled — the
test environment is not sufficiently isolated." Also: "Tests that modify global state typically
cannot be run in parallel." Rerunning is framed explicitly as mitigation only: "Rerunning any failed
tests can mitigate the negative effects of flaky tests by giving them additional chances to pass."
The plugins the official page names are `pytest-rerunfailures`, `pytest-replay`,
`pytest-flakefinder`, `pytest-random-order` and `pytest-randomly`; the other remedies listed are
splitting the suite, deleting or rewriting tests, quarantining, and screenshots on failure.

**The gate policy — OPEN** (a project convention; no primary source prescribes it):

- **An automatic retry in the default CI path is forbidden.** It converts a signal into noise, and
  once present, every red build becomes "just re-run it". If reruns are used at all they are used to
  *identify* flakes in a dedicated job, never to turn a red merge green.
- **Quarantine is a marker plus a deadline plus an owner.** A quarantined test is deselected from
  the required gate (`-m "not quarantine"` or `--deselect`), is listed in a committed file with a
  date and an owner, and the quarantine list is a ratchet under §4.1 — it may only shrink.
- **Measure per-test pass rate over N CI runs** to identify flakes rather than arguing about them.
- **Do not benchmark your flake rate against an industry figure.** Google's 2017 analysis of **4.2
  million tests** reports that "larger tests are more flaky" and that "when a stable test became
  flaky, and we could track it to a specific code change, the problem was a bug in production code
  1/6th of the time" — **ESTABLISHED**. The frequently quoted "1.5% of tests are flaky" figure could
  **not** be confirmed in the Google Testing Blog posts fetched this pass — **OPEN**. Your own rate
  is measurable; it is not benchmarkable.

**doctest is a named flake source, and it is documented as such.** "doctest is serious about
requiring exact matches in expected output. If even a single character doesn't match, the test
fails." Expected exception output must begin `Traceback (most recent call last):` (or `Traceback
(innermost last):`); blank lines must be written `<BLANKLINE>`; and set and dict ordering, object
reprs containing addresses (`<C object at 0x...>`, needing `+ELLIPSIS`) and float repr are the named
hazards. Hard tabs are expanded to 8-column stops in the source but not in actual output.
`+ELLIPSIS` and `+NORMALIZE_WHITESPACE` are the standing mitigations — **ESTABLISHED** (§11.3).

### 6.5 Sharding, and what it breaks

**VERSION-DEPENDENT (pytest-xdist 3.8.0).** Distribution modes: `--dist load` (default) "Sends
pending tests to any worker that is available, without any guaranteed order"; `--dist loadscope`
groups "by module for test functions and by class for test methods"; `--dist loadfile` groups by
containing file; `--dist loadgroup` groups by the `xdist_group` mark and "Guarantees that all tests
with same `xdist_group` name run in the same worker"; `--dist worksteal` rebalances by stealing
queued tests; `--dist no` is sequential. Worker counts: `-n auto` uses physical CPU cores, `-n
logical` uses logical cores (requires psutil), `-n N` is explicit. `--max-worker-restart` bounds
crash recovery.

**Two consequences that break suites — ESTABLISHED.** The default mode gives no ordering guarantee,
so order-dependent tests become nondeterministic under `-n auto`; and a session-scoped fixture is
constructed **once per worker process**, not once per run, so anything assuming a single global
setup breaks. The remedy is `--dist loadgroup` with an explicit `xdist_group` for tests that must
share a worker — which is a design statement about shared state, and therefore belongs in the
test-design manifest; the gate's obligation is only to declare the mode it runs in and to keep local
and CI on the same one (§3).

**Suite runtime is a maintainability property with a stdlib-grade measurement.** `pytest
--durations=N` and `--durations-min=THRESHOLD`, documented example `pytest --durations=10
--durations-min=1.0`; "By default, pytest will not show test durations that are too small (<0.005s)
unless `-vv` is passed on the command-line" — **ESTABLISHED**. Budget the wall clock, and pair the
budget with a test-count floor, because suite time is trivially "improved" by deleting slow
integration tests (§10.1).

### 6.6 Mutation testing: the oracle, run off the PR path

**Both sides of the literature, because reporting one is misleading — both ESTABLISHED.** *For:*
Just, Jalali, Inozemtseva, Ernst, Holmes & Fraser (FSE 2014), using **357 real faults across 5
open-source applications totalling 321,000 lines**, found real faults "coupled to mutants for
**73%** of real faults" and a "statistically significant correlation between mutant detection and
real fault detection, independently of code coverage" that is "stronger than the correlation between
statement coverage and real fault detection". *Against:* Papadakis, Shin, Yoo & Bae (ICSE 2018), on
CoreBench and Defects4J, "provide evidence that all correlations between mutation scores and real
fault detection are weak when controlling for test suite size", arguing Just et al. "did not control
for the size of the test suites, which is a strong confounding factor". Their own reconciliation:
"By measuring the fault detection capability of the top ranked, according to mutation score, test
suites (opposed to randomly selected test suites of the same size), we find that achieving higher
mutation scores improves significantly the fault detection. Taken together, our data suggest that
mutants provide good guidance for improving the fault detection of test suites, but their
correlation with fault detection are weak."

**The operational reading:** mutants are excellent as a *targeting diagnostic* and poor as a *scalar
KPI*. Run them on the functional core, review the surviving mutants, never gate on the score.

**mutmut 3.7.0 mechanics — ESTABLISHED.** Statuses: `killed`, `survived`, `timeout`, `suspicious`,
`skipped`, `no tests`, `not checked`, `segfault`, `check was interrupted by user`, and — notably —
**`caught by type check`** (exit code 37), meaning the mutant was rejected by the type checker
before tests ran. `mutmut export-cicd-stats` writes `mutants/mutmut-cicd-stats.json`, and the source
comment states its purpose verbatim: "exports CI/CD stats to block pull requests from merging if
mutation score is too low". Configuration lives in `[tool.mutmut]` with `paths_to_mutate`,
`source_paths`, `tests_dir`, `only_mutate`, `do_not_mutate`, `do_not_mutate_patterns`, `also_copy`,
`max_stack_depth` (default `-1`), `mutate_only_covered_lines`. It requires `fork`: "if you want to
run on windows, you must run inside WSL". `cosmic-ray` 8.4.6 is the alternative.

**`caught by type check` is direct evidence for this collection's thesis** — it is the measured
overlap between the typing rung and the testing rung: a mutation the type checker rejects is a fault
class the type system already forecloses. Report the size of that bucket; never target it. Its size
for any given project is **OPEN** — no literature measures it.

---

## 7. Supply-chain and release gates

### 7.1 Reproducible environments: the lock file is the gate

**Package Dependencies** (a tactic named in Bass, Clements & Kazman, 2021) states the problem this
gate solves: code that "behaves correctly in development can fail in production when the surrounding
dependency versions differ." Its three-part answer maps exactly onto Python: PEP 621
`[project.dependencies]` for ranges, a lock file for exactness, and an image for the interpreter and
OS libraries — **ESTABLISHED** (seed-pack vocabulary and citation). **Immutable Infrastructure**
(Kief Morris, *ImmutableServer*, 2013) is the companion for the third part: pinned base image, wheel
built once, configuration injected, never `pip install` into a running container, and "rollback is a
redeploy of the previous image" — **ESTABLISHED** (seed-pack vocabulary). For a single-process
application distributed as a wheel, the image half is optional; the lock file is not.

**The mechanics, and the flag whose name reads backwards — VERSION-DEPENDENT (uv 0.12.x).** `uv run`
locks and syncs before invoking the command so "the project environment is always up-to-date".
`--locked`: "If the lockfile is not up-to-date, uv will raise an error instead of updating the
lockfile" — **this is the CI form**. `--frozen`: use "the lockfile without checking if it is
up-to-date" — this **cannot** detect a stale lock file. `uv lock --check` checks the lock file
against project metadata. `uv sync --inexact` retains extraneous packages while `uv run --exact`
removes packages absent from the lock file; `--upgrade` and `--upgrade-package` bound the refresh
scope. The name `--frozen` reads stricter than `--locked` to most people and is the looser flag; CI
wired with `--frozen` installs happily from a stale lock file.

**The interchange format is standardised — ESTABLISHED.** PEP 751, "A file format to record Python
dependencies for installation reproducibility", is **Final**. It standardises the filename
`pylock.toml`, or a variant matching `r"^pylock\.([^.]+)\.toml$"`. Required top-level keys:
`lock-version` (value `"1.0"`), `created-by`, and the `[[packages]]` array. Optional:
`environments`, `requires-python`, `extras`, `dependency-groups`, `default-groups`. Per package:
`name` (required), `version`, `marker`, `requires-python`, `dependencies` (informational only),
`index`, exactly one of `wheels` / `sdist` / `directory` / `vcs` / `archive`, and
`attestation-identities`. It is a format for **installers to consume**, not a section of
`pyproject.toml`. A tool's native lock file (`uv.lock`) remains the working artefact; `pylock.toml`
is what you publish or hand to a different installer.

### 7.2 Audit tooling

**VERSION-DEPENDENT (pip-audit 2.10.x).** pip-audit "is a tool for scanning Python environments for
packages with known vulnerabilities" and "uses the Python Packaging Advisory Database via the PyPI
JSON API as a source of vulnerability reports". `--vulnerability-service` accepts `osv`, `pypi`,
`esms`; `--format` accepts `columns`, `json`, `cyclonedx-json`, `cyclonedx-xml`, `markdown`. Exit
`0` = "No known vulnerabilities were detected", `1` = "One or more known vulnerabilities were
found". Other flags worth committing: `--require-hashes` ("require a hash to check each requirement
against, for repeatable audits"), `--ignore-vuln` (with a written reason, and treated as suppression
debt under §4.5), `--no-deps`, `-r REQUIREMENT`, `--local`, `--output`, `--timeout`.

**Use `--strict`, and know what it means:** it fails the entire audit if dependency collection fails
on any dependency. Without it, an unresolvable dependency is skipped and the audit can still exit
`0` — a clean report over an incompletely scanned environment.

**Two limits stated by the tool itself — ESTABLISHED:** "pip-audit is not a static code analyzer",
and users "must not assume that pip-audit will defend you against malicious packages". A
vulnerability audit is not a supply-chain-attack defence, and a manifest that implies otherwise is
misleading.

**Code scanners are a separate axis.** bandit 1.9.4 is the Python-specific security linter (§2.1,
row 19), with suppression via a bare `# nosec` — "any results associated with it will not be
reported" for that line — or the scoped form naming tests, e.g. `# nosec B602, B607`, where "Full
test names rather than the test ID may also be used" — **ESTABLISHED**. semgrep 1.172.0 is the
pattern engine, with `nosem` as its suppression comment and `--baseline-commit` as its ratchet
(§4.6) — **VERSION-DEPENDENT**. At the target scale, ruff's `S` (flake8-bandit) family inside the
existing lint gate is usually the right first step, and adding bandit *and* semgrep before ruff's
`S` rules are clean is buying overlap; that ordering is a `python_linting_practices_manifest.md`
matter, but the gate cost is this file's.

### 7.3 Workflow-security scanning: audit the pipeline itself

**VERSION-DEPENDENT (zizmor 1.29.0).** "zizmor is a static analysis tool for your CI/CD", covering
GitHub Actions, Dependabot and pre-commit configurations. Its audits include `template-injection`,
`artipacked`, `dangerous-triggers`, `excessive-permissions`, `impostor-commit`,
`known-vulnerable-actions`, `ref-confusion`, `self-hosted-runner`, `unpinned-uses`,
`use-trusted-publishing`, `cache-poisoning`, `bot-conditions`, `overprovisioned-secrets`,
`secrets-inherit`, `github-env`, `unredacted-secrets`, `obfuscation`, `forbidden-uses`,
`stale-action-refs`, `unsound-contains`, `anonymous-definition`.

Personas set the noise floor: `regular` (default) — "the user wants high-signal, low-noise,
actionable security findings"; `pedantic` — "code smells in addition to regular, actionable security
findings"; `auditor` — "everything flagged by zizmor, including findings that are likely to be false
positives". `--min-severity` and `--min-confidence` filter on the levels findings carry; `--format`
takes `plain` (default), `json`/`json-v1`, `sarif`, `github`. Suppression is `# zizmor:
ignore[audit-name]`, comma-separated for several — and counts toward the suppression budget (§4.5).

**Why this gate is not optional at any scale.** The pipeline is the thing with the credentials. Two
of zizmor's audits — `unpinned-uses` and `use-trusted-publishing` — are the mechanical form of two
rules this section states in prose (§7.4, and "pinning nothing" in the anti-patterns). Remember the
exit codes: findings are **`11`–`14`**, and `1` means the audit errored — **VERSION-DEPENDENT
(zizmor 1.29.0)**.

### 7.4 Trusted Publishing and attestations

**ESTABLISHED.** PyPI Trusted Publishing exchanges an OIDC token for "a short-lived API token" valid
for **15 minutes**. The motivation is stated plainly: "PyPI's normal API tokens are long-lived,
meaning that an attacker who compromises a package's release token can use it until its legitimate
user notices and manually revokes it." The GitHub Actions form requires `permissions: id-token:
write`, recommends `uses: pypa/gh-action-pypi-publish@release/v1`, and the `environment:` setting is
"optional, but strongly encouraged".

**Attestations come for free, and one input silently turns everything off — VERSION-DEPENDENT
(action v1).** `pypa/gh-action-pypi-publish` generates PEP 740 attestations **by default** in the
Trusted Publishing flow; `attestations: false` disables them. **Supplying `password:` disables
Trusted Publishing entirely** — and therefore also the default attestations. Other inputs:
`repository-url`, `packages-dir` (default `dist/`), `verify-metadata`, `skip-existing`, `verbose`,
`print-hash`, `user` (default `__token__`). Adding a separate signing step duplicates work the
action already did.

**What an attestation is — ESTABLISHED.** PEP 740, "Index support for digital attestations", is
**Final**. An attestation object carries `version` (always 1), `verification_material`, and
`envelope` (a base64-encoded statement plus signature); the statement is an in-toto v1 Statement
whose single subject is the distribution filename with a SHA-256 digest. Provenance groups
`attestation_bundles`, each holding a `publisher` object (`kind` plus `claims`) and an
`attestations` array. Exactly **two** predicate types are
permitted: `https://slsa.dev/provenance/v1` (SLSA Provenance) and
`https://docs.pypi.org/attestations/publish/v1` (PyPI Publish Attestation). An index MUST accept
`attestations` as a multipart form field on upload, MUST verify all attestations and reject the
upload if verification fails, and MUST support `data-provenance` attributes.

**Do not claim attestations block installation.** Whether any current pip or uv release can be
configured to **require** attestations before installing was not confirmed against a pip or uv page
this pass — **OPEN**. Today they are audit evidence a consumer can record, and the upload-side gate
is the index's own verification.

### 7.5 SBOM formats

**ESTABLISHED.** PEP 770, "Improving measurability of Python packages with Software
Bill-of-Materials", is **Final**. It reserves the `.dist-info/sboms/` subdirectory for SBOM
documents stored as **opaque files**, deliberately adds **no new core metadata field**, tells
producers to "use a widely-accepted SBOM standard, such as CycloneDX or SPDX" and to "use
UTF-8-encoded JSON when available", and requires that "any files in this directory MUST be copied
from wheels by install tools". Inventing a metadata key for this (an `Sbom-File` field, say) will
not validate anywhere.

Formats: CycloneDX's current specification version is **1.7**, with JSON, XML and Protobuf
encodings, and it was published as **ECMA-424** — **ESTABLISHED**. spdx.dev lists **3.0** as the
current SPDX document version and states "The SPDX specification is an international open standard
(ISO/IEC 5962:2021)"; that ISO number was assigned to SPDX 2.2.1, and **no ISO designation for SPDX
3.x was shown** — **ESTABLISHED** for the version, **OPEN** for an ISO number covering SPDX 3.x. Do
not write "SPDX 3.0 (ISO/IEC 5962)".

Generation: `cyclonedx-bom` 7.3.1 is the "CycloneDX Software Bill of Materials (SBOM) generator for
Python projects and environments"; `pip-audit` can also emit `cyclonedx-json` / `cyclonedx-xml`
directly, which means a project already running the audit gate gets the SBOM without a new
dependency — **VERSION-DEPENDENT**.

**Scale verdict.** For an application nobody redistributes, an SBOM is a compliance artefact with no
internal consumer, and generating one is over-engineering. It becomes required the moment a consumer
asks, or the moment you publish a wheel others vendor.

### 7.6 Reproducible builds

**ESTABLISHED (flit's documentation of the mechanism).** A wheel is a zip archive that embeds "the
modification timestamp from each file. This will probably be different on each computer, because it
indicates when your local copy of the file was written, not when it was changed in version control",
and those timestamps "can be overridden by the environment variable `SOURCE_DATE_EPOCH`". Flit
additionally "normalises the permission bits of files copied into a wheel to either 755 (executable)
or 644". So the gate is: set `SOURCE_DATE_EPOCH`, build twice, compare digests.

**The normative specification of `SOURCE_DATE_EPOCH` was not fetched this pass**, so its exact
required semantics — clamping rules, precedence when a file is newer than the epoch — are **OPEN**.
Treat reproducibility as advisory until you have read that specification and confirmed your
backend's behaviour. Note also that a build backend other than flit may not normalise permission
bits.

### 7.7 The release chain, in order

**OPEN** (the assembly is the analyst's; each step is cited above). One artefact, promoted:

1. `uv lock --check` — the lock file matches `pyproject.toml`.
2. `pip-audit --strict` — no known vulnerability, and nothing silently skipped.
3. `zizmor --offline .github/workflows` — the pipeline that is about to hold a publishing credential
   is itself audited.
4. PEP 517 build **once**, with `SOURCE_DATE_EPOCH` set. Nothing downstream rebuilds.
5. Every gate at `M` re-run against **the built wheel**, installed — not against the source tree.
6. SBOM generated from the built artefact if a consumer requires one.
7. `pypa/gh-action-pypi-publish@release/v1` with `permissions: id-token: write`, `environment:` set,
   no `password:`, attestations left at their default.

---

## 8. Incremental delivery

### 8.1 Trunk-based development

**ESTABLISHED** (trunkbaseddevelopment.com; site attribution "2017-2020: Paul Hammant, with
contributions from friends"). Trunk-based development is "A source-control branching model, where
developers collaborate on code in a single branch called 'trunk' and resist any pressure to create
other long-lived development branches by employing documented techniques." The two accepted shapes
are "a direct to trunk commit/push (v small teams)" or "a Pull-Request workflow as long as those
feature branches are short-lived". "Trunk- Based Development is a key enabler of Continuous
Integration and by extension Continuous Delivery." Release branches, where used, "are cut from the
trunk on a just-in-time basis, are 'hardened' before a release ... and those branches are deleted
some time after release".

**The numeric ceiling people quote is not in the source.** The site states that short-lived branches
should be "the product of a single dev-workstation" but publishes **no numeric maximum lifetime**;
the commonly repeated "one or two days" was not found on the primary page — **OPEN**. Pin your own
number and record it as a convention rather than citing it as a fact.

**Why this section sits in the gates file.** The gate design and the branching model are the same
decision: a required status check on `M` is only meaningful if branches are short enough that the
check runs against something close to trunk. A long-lived branch defers every gate to a merge nobody
wants to do.

### 8.2 Feature toggles: four categories, four lifetimes

**ESTABLISHED** (Pete Hodgson, *Feature Toggles (aka Feature Flags)*, martinfowler.com, 09 October
2017 — the work the SWE corpus records as the naming source for the **`feature-flag`** element,
realm
design, kind code-structure). There are exactly four categories, positioned on axes of **dynamism**
and **longevity**. `feature-flag` names the parts: a **toggle point**, a **toggle router**, and
**toggle configuration** — **ESTABLISHED** (seed-pack vocabulary). Distinguish it from the
architecture *tactic* `feature-toggle` (Bass, Clements & Kazman, 2021 — the kill switch), which
`feature-flag` *realizes* through a sourced corpus edge: the corpus holds these as a deliberate
same-name-two-realms pair, and collapsing them loses the 2017 naming source for the parts named
above.

| category | Hodgson's definition | typical lifetime | removal obligation | configuration home |
|---|---|---|---|---|
| **Release toggle** | "allow incomplete and un-tested codepaths to be shipped to production as latent code which may never be turned on" | days to weeks — as long as the change is in flight | **mandatory and dated.** The toggle and both branches of the code are deleted when the feature ships | source control + redeploy |
| **Experiment toggle** | cohort-based A/B routing | the length of the experiment, then immediately | **mandatory**, and the losing branch is deleted with it. Its removal is a *result*, not cleanup | runtime configuration (cohorts must be dynamic) |
| **Ops toggle** | "used to control operational aspects of our system's behavior" | can be long-lived, some permanent (a kill switch) | none if deliberately permanent — but it must be *declared* permanent, or it is release-toggle debt | runtime configuration |
| **Permissioning toggle** | "used to change the features or product experience that certain users receive" | longest-lived; often a product feature in its own right | none — it is not debt, it is behaviour | runtime configuration / per-user |

**Configuration guidance, verbatim — ESTABLISHED:** "Managing toggle configuration via source
control and re-deployments is preferable, if the nature of the feature flag allows it." For a
release toggle it does allow it, so a release toggle should be a committed constant, not a runtime
lookup. That single choice removes the flag-service dependency for the most common category.

**The debt discipline, verbatim — ESTABLISHED:** treat toggles "as inventory which comes with a
carrying cost and seek to keep that inventory as low as possible". The enforcement options Hodgson
names: a removal task created *with* the toggle, an expiry date, a **"time bomb"** that fails tests
after expiry, and a hard cap on the number of live toggles. **The time bomb is the only one of the
four that is mechanical** — a test that reads the toggle's declared expiry date and fails once it
passes. Everything else is a convention that decays. Two of the four are also ratchet-shaped under
§4.1: the live-toggle count is a committed number that may not grow, and the expiry dates live in a
committed file.

**Feature-flag platforms — FLAGGED-SECONDARY.** OpenFeature is a CNCF vendor-neutral specification
with SDKs and pluggable providers (Unleash, Flagsmith, GrowthBook and LaunchDarkly among them), and
Flipt takes a GitOps approach in which flag definitions live in the repository and are reviewed in
pull requests. This reached this pass through search results summarising vendor documentation;
neither openfeature.dev nor any Python SDK project page was fetched, and **version numbers for every
Python feature-flag SDK are OPEN**. Do not pin one from memory.

### 8.3 Expand / migrate / contract is the shape of a safe change

**ESTABLISHED** (Danilo Sato, *ParallelChange*, martinfowler.com, 13 May 2014). Parallel change is
"also known as expand and contract" and is "a pattern to implement backward-incompatible changes to
an interface in a safe manner, by breaking the change into three distinct phases: expand, migrate,
and contract."

Mapped onto the gates, **OPEN** (the mapping is the analyst's):

| phase | what changes | what the gates must show |
|---|---|---|
| **expand** | the new interface is added beside the old; both work | every existing test still passes unmodified; the new surface has its own tests; no consumer changed |
| **migrate** | consumers move one at a time | each consumer's migration is its own reviewable change; the deprecation warning is *emitted* but not yet fatal (§8.4) |
| **contract** | the old interface is deleted | the deprecation window has expired; `vulture --min-confidence 100` and the import graph show no remaining reference |

The reason this belongs in a gates file: **each of the three phases is independently mergeable and
independently green**, which is precisely what makes a backward-incompatible change compatible with
trunk- based development. A change that cannot be split this way is a change that will live on a
branch.

### 8.4 Deprecation windows, enforced rather than announced

The deprecation *contract* — what may change, what the public surface is, how versions are numbered
—
and the **four-part visibility contract** that makes a window real are owned by
`python_module_boundaries_manifest.md` §9.3, whose table is the canonical enumeration: (1) producer,
runtime — `@warnings.deprecated` (PEP 702) on the deprecated member; (2) producer, test — the
project's own suite promoting `DeprecationWarning` to an error, so it sees its own deprecations; (3)
consumer, static — the type checker reporting a *use* of a `@deprecated` member; (4) consumer, test
—
the consumer's suite promoting `DeprecationWarning` to an error. Part 1 is source. Parts 2–4 are
gates, and wiring them is this section's whole job.

| part | which job | the wiring | tag |
|---|---|---|---|
| 2 — producer, test | this project's `pytest` (ledger row 8) | `-W error::DeprecationWarning` on the invocation, or `filterwarnings` promoting it in the pytest configuration (§6.3) | ESTABLISHED |
| 3 — consumer, static | the consumer's `mypy` (ledger row 4) | the `deprecated` error code, enabled explicitly — it is one of the optional codes `--strict` does not give you (§5.1) | ESTABLISHED |
| 4 — consumer, test | the consumer's `pytest` | `filterwarnings` promoting `DeprecationWarning` to an error, so the consumer's suite fails while the symbol still exists rather than after it is deleted | ESTABLISHED |

**Availability is a floor decision, not a wiring decision.** `@warnings.deprecated` is native from
Python 3.13 and needs `typing_extensions.deprecated` below that; the floor itself is
`python_platform_baseline_manifest.md` §3e's call — **VERSION-DEPENDENT**.

Part 1 announces the window; parts 2 and 4 enforce it against code that already exists; part 3
enforces it against code being written now. Announcing part 1 alone is how deprecations reach their
removal date with consumers still calling them — the marker without part 3 is a comment, and the
marker without parts 2 and 4 is a warning that no CI job reads.

### 8.5 The supported-version CI matrix

Release dates, support phases and end-of-life are owned by `python_platform_baseline_manifest.md`
§1a; this section owns only the matrix that consumes them, and deliberately restates no date. Two
things are read off the hub before a leg is written: which branches are still in the bugfix phase,
and
which release is next. A matrix written from a template a few months old is stale in **both**
directions at once — it gates a leg that is about to leave support and has no leg for the version
about to ship. The standing rules, **OPEN** (project conventions built on the hub's calendar): the
oldest leg is the `requires-python` floor and is dropped on the hub's EOL date for that branch, not
before; the newest leg is the next release's prerelease, advisory until that release is final and
required thereafter.

**GitHub Actions matrix semantics — ESTABLISHED.** `jobs.<job_id>.strategy.matrix` declares axes as
arrays. `include` entries are applied in order, adding properties to combinations they match,
creating additional combinations when they match nothing, and later `include` entries can overwrite
earlier ones; `exclude` removes matching combinations. `fail-fast` controls cancellation — when it
fires, "all jobs that are in progress or queued will be cancelled". `max-parallel` caps concurrency.
**The documented maximum number of jobs a single matrix may generate was not shown on the page
fetched, and the widely repeated figure of 256 is unverified here — OPEN.**

**Two gate decisions the matrix forces — OPEN** (project conventions): (a) `fail-fast: false` for a
supported-version matrix, because you need to know whether the failure is one leg or all of them, at
the cost of runner minutes; and (b) which leg is the *required* status check. Making all legs
required multiplies flake exposure by the number of legs; making one required and the rest advisory
means a version-specific break can merge. Pick, and write down which.

**The missing-interpreter trap belongs here too:** a matrix leg whose interpreter is absent must
fail, not skip (§3.3). nox's `error_on_missing_interpreters` is the verified switch; tox's
counterpart is **OPEN**.

### 8.6 What of this is over-engineering for a small project

Stated plainly, because restraint is content. **OPEN** (scale judgements, not facts):

| mechanism | verdict at small-to-mid single-process scale |
|---|---|
| Trunk plus short-lived PR branches | **adopt.** It is cheaper than the alternative at every size |
| Release toggles as committed constants | **adopt.** They are what makes trunk work |
| Expand / migrate / contract | **adopt** for any published interface. Skip it for internals with a single caller you can change atomically |
| The four-part deprecation-visibility contract (§8.4) | **adopt.** One decorator plus three lines of configuration for an enforced window |
| Deployment pipeline as multiple promoted stages | **thin it.** Build once and run the gates once; a five-stage promotion chain for a wheel with one consumer is ceremony |
| A feature-flag service (OpenFeature, Flipt, a vendor SDK) | **over-engineering** below the point where you need cohort-based experiments or runtime kill switches. Env vars and TOML read at startup cover ops toggles |
| Blue-green, canary and rolling deployment (`scale-rollouts`) | **over-engineering** for a single process. bck's own requirement is "an architectural mechanism **outside** the service that routes each user's requests to the new or old version" — if you do not have that router, you do not have the tactic |
| SBOM generation | **over-engineering** until a consumer asks (§7.5) |
| Mutation testing in the PR path | **over-engineering.** Scheduled and reviewed, yes; gated, no (§6.6) |
| DORA dashboards | **over-engineering.** Two of the five metrics are countable from your own git and deploy logs; a dashboard is not the gate (§9.6) |
| Per-developer metrics of any kind | **never.** This is an abuse of team-level signals, not a scale question |
| An SBOM/attestation/reproducibility chain for an internal CLI | **over-engineering**, except `uv lock --check` and `pip-audit --strict`, which are cheap and pay immediately |

**Two seed-pack tactics that are cheap enough to keep at any scale**, both **ESTABLISHED**
(seed-pack vocabulary): **Specialized Interfaces** (test-only set/get/report/reset surfaces, kept
separate and removable) carries its own hazard verbatim — "shipping code different from tested code
is problematic in performance- and safety-critical systems" — so the gate obligation is that the
test-only surface is excluded from the shipped wheel and that its exclusion is checked. And
**Executable Assertions**: `assert` is for internal invariants and is **disabled under `-O` /
`PYTHONOPTIMIZE`**, so an assertion is never a gate and never an input validator; placement and the
pre/postcondition libraries are `error_tracing_contract_manifest.md`'s.

---

## 9. Measurement, with the evidence stated honestly

### 9.1 Two questions, two metrics — do not conflate them

**ESTABLISHED.** Cyclomatic complexity and cognitive complexity answer different questions, and
treating them as interchangeable is the most common measurement error.

**Cyclomatic complexity answers: how many paths must a test suite cover?** Ruff's own definition of
`C901`: McCabe complexity measures "the complexity of the control flow graph of the function",
computed by "add[ing] one to the number of decision points in the function". SonarQube's definition
of the same metric is "Cyclomatic complexity = 1 + number of conditional branches". It is a
**testability** proxy.

**The canonical limit of 10 is a convention that ships with a published hedge.** NIST SP 500-235
(Watson & McCabe, 1996), verbatim: "The precise number to use as a limit, however, remains somewhat
controversial. The original limit of 10 as proposed by McCabe has significant supporting evidence,
but limits as high as 15 have been used successfully as well. Limits over 10 should be reserved for
projects that have several operational advantages over typical projects, for example experienced
staff, formal design, a modern programming language, structured programming, code [walkthroughs]" —
**ESTABLISHED**. Your chosen number is a decision to record, not a fact to cite.

**Cognitive complexity answers: how hard is this to read?** G. Ann Campbell's white paper
(*Cognitive Complexity — a new way of measuring understandability*, SonarSource S.A., **Version 1.7,
29 August 2023**) states its motive: cyclomatic complexity "excels at measuring" testability but
"its underlying mathematical model is unsatisfactory at producing a value that measures"
maintainability; it "cries wolf" by "over-valuing some structures, while under-valuing others"; and
being "[f]ormulated in a Fortran environment in 1976, it doesn't include modern language structures
like try/catch, and lambdas" — **ESTABLISHED**.

The three rules, verbatim: "1. Ignore structures that allow multiple statements to be readably
shorthanded into one. 2. Increment (add one) for each break in the linear flow of the code. 3.
Increment when flow-breaking structures are nested." Four increment types: **Nesting**;
**Structural** (subject to a nesting increment and increases the nesting count); **Fundamental**
(not subject to a nesting increment); **Hybrid** (not subject to a nesting increment but does
increase the nesting count) — **ESTABLISHED**. The deliberate discounts matter as much as the
increments: methods themselves do not increment; null-coalescing operators are ignored; `try` and
`finally` blocks "are ignored altogether"; a `catch` "only adds one point to the Cognitive
Complexity score, no matter how many exception types are caught"; "A switch and all its cases
combined incurs a single structural increment"; and sequences of *like* boolean operators cost one
point each, so `a && b && c && d` costs 1 while `a || b && c || d` costs 3 — **ESTABLISHED**.

**The white paper states no threshold.** Grepping the full extracted text for "threshold", "limit",
"recommend" and "default value" returns nothing. The widely quoted **15** is a *tool* default:
`sonar-python`'s `CognitiveComplexityFunctionCheck` declares `private static final int
DEFAULT_THRESHOLD = 15;`, exposed as `@RuleProperty(key = "threshold", description = "The maximum
authorized complexity.")` — **ESTABLISHED**. **Citing "15" as Campbell's recommendation is a
fabrication.** Cite it as the SonarQube default, which is what it is.

**Which of the two has human-subject support — ESTABLISHED.** Muñoz Barón, Wyrich & Wagner, *An
Empirical Validation of Cognitive Complexity as a Measure of Source Code Understandability* (ESEM
2020, arXiv:2007.12520): a meta-analysis of roughly **24,000 understandability evaluations across
427 code snippets** gathered by systematic literature review, finding that "Cognitive Complexity
positively correlates with comprehension time and subjective ratings of understandability", with
"mixed results for the correlation with the correctness of comprehension tasks and with
physiological measures". That is the best evidence any complexity metric in this file has, and it is
moderate.

### 9.2 What complexity does not predict — the sceptical record

**ESTABLISHED — the canonical refutation, and it is blunt.** Shepperd, *A critique of cyclomatic
complexity as a software metric* (Software Engineering Journal 3(2):30–36, 1988). Abstract,
verbatim: the metric "is based upon poor theoretical foundations and an inadequate model of software
development. The argument that the metric provides the developer with a useful engineering
approximation is not borne out by the empirical evidence. Furthermore, it would appear that for a
large class of software it is no more than a proxy for, and in many cases is outperformed by, lines
of code." His survey table records CC-to-LOC Pearson coefficients of **0.84–0.92** across studies,
and he reports "the out-performing of v(G) by a straightforward LOC metric in over a third of the
studies considered".

**Shepperd's structural objection is the one that matters for a refactoring gate — ESTABLISHED.** He
notes that CC can *increase* when applying generally accepted techniques to improve program
structure, and concludes "the only possible role for cyclomatic complexity is as an intra-modular
complexity metric", since how to modularise "is better resolved by considerations of `coupling' and
`cohesion' ... which are not adequately captured by the metric". A gate that rewards fragmentation
produces forty three-line functions with a tangled call graph, and every metric is green.

**The redundancy claim is contested, and the resolution is the unit of analysis.** *For* redundancy:
Jay, Hale, Smith, Hale, Kraft & Ward (2009, *J. Software Engineering & Applications* 2:137–143)
reported a stable linear CC–LOC relationship — **FLAGGED-SECONDARY** (the publisher page returned
HTTP 403 this pass; bibliographic details from search metadata only). *Against* it: Landman,
Serebrenik & Vinju (ICSME 2014, extended in *J. Software: Evolution and Process*, 2016) analysed
**17.6 million Java methods and 6.3 million C functions** and state on the authors' own site that
"the observed linear correlation between CC and SLOC of Java methods or C functions is not strong
enough to conclude that CC is redundant with SLOC", noting the correlation "is only moderate as
caused by increasingly high variance" — **ESTABLISHED** (that this is the authors' claim).
SonarSource's own white paper concedes the aggregate side: "it is widely acknowledged that the
Cyclomatic Complexity scores of applications correlate to their lines of code totals. In other
words, Cyclomatic Complexity is of little use above the method level" — **ESTABLISHED**.

**The resolution, and it is the operative rule: gate CC per function; never report project-average
CC as a maintainability figure** — **ESTABLISHED** as a characterisation of the cited evidence.

**The Maintainability Index is not gate material, for four independent reasons — ESTABLISHED except
as noted.** (i) **Two different formulas share the name.** Microsoft's is `MAX(0,(171 - 5.2 *
ln(Halstead Volume) - 0.23 * (Cyclomatic Complexity) - 16.2 * ln(Lines of Code)) * 100 / 171)` with
bands 0–9 Red, 10–19 Yellow, 20–100 Green; radon's is `MI = max[0, 100 * (171 - 5.2 ln V - 0.23 G -
16.2 ln L + 50 sin(sqrt(2.4 C))) / 171]` where `C` is comment percentage — radon adds a
comment-density term Microsoft's has not, and radon's ranks are A = 100–20, B = 19–10, C = 9–0.
**The two numbers are not comparable**, and a file can be rank A in radon and Yellow in Visual
Studio. (ii) **The constants have not been recalibrated since 1994.** Van Deursen's "Think Twice
Before Using the Maintainability Index" (2014-08-29) traces the index to Oman & Hagemeister (ICSM
1992), refined by Coleman, Ash, Lowther & Oman (IEEE Computer, 1994), derived from "systems from
Hewlett-Packard (written in C and Pascal in the late 80s, ranging in size from 1000 to 10,000 lines
of code)", and notes "Tool smiths and vendors used the exact same formula and coefficients as the
1994 experiments, without any recalibration" — **FLAGGED-SECONDARY** for the HP-dataset detail (a
blog post, though by a primary authority on the critique). (iii) **The thresholds are unjustified**:
on Visual Studio's 20/10 cutoffs, "I have not been able to find a justification for these
thresholds"; this pass found none either — **OPEN**. (iv) **It averages a power-law distribution**:
the index averages per file, but "these metrics follow a power law, and taking the average tends to
mask the presence of high-risk parts". Van Deursen's own recommendation: "Most likely, you'll be
better off looking at lines of code."

**radon says so itself — ESTABLISHED:** "Maintainability Index is still a very experimental metric,
and should not be taken into account as seriously as the other metrics." **Verdict: report MI if you
like; never fail a build on it.** Halstead's derived constants are in the same category — `T = E/18`
seconds and `B = V/3000` delivered bugs are Halstead's own 1977 calibration with no modern
validation — **OPEN**.

**For calibration only, radon's CC rank table — ESTABLISHED:** 1–5 = A "low - simple block"; 6–10 =
B "low - well structured and stable block"; 11–20 = C "moderate - slightly complex block"; 21–30 = D
"more than moderate - more complex block"; 31–40 = E "high - complex block, alarming"; 41+ = F "very
high - error- prone, unstable block".

### 9.3 Thresholds are not portable between tools

**VERSION-DEPENDENT (ruff 0.16.x / radon 6.0.1), read from source.** radon and ruff compute
*different numbers* for the same function. radon counts `Try` as `len(node.handlers) +
bool(node.orelse)`, **`BoolOp` as `len(node.values) - 1`**, `If`/`IfExp` as 1, `Match` as
`len(cases)` minus a wildcard case, `For`/`While`/`AsyncFor` as `1 + bool(orelse)`,
**`comprehension` as `len(node.ifs) + 1`**, and **`assert` as 1** (unless `no_assert`); lambdas are
deliberately not counted. Ruff's `C901` walks **statements only**: `If` +1 (plus 1 per `elif`/`else`
clause), `For`/`While` +1 (ignoring their `else`), `Match` +1 per case, `Try` +1 per handler,
**nested `FunctionDef` +1**, `With` +0, `ClassDef` +0 — and **no `BoolOp`, no comprehension, no
`assert`**. A function full of `and`/`or` and comprehensions therefore scores high in radon and low
in ruff. **Never migrate a threshold between the two without re-measuring.**

A third disagreement, for cognitive complexity: SonarPython's S3776 **skips inner functions** (the
check returns early on `isInnerFunction(functionDef)`), so a deeply nested closure's complexity is
attributed to its enclosing function or missed; `complexipy` and ruff do not share that behaviour —
**VERSION-DEPENDENT (sonar-python master / complexipy 6.2.0)**. And `complexipy`'s own documentation
states plainly that it "is an independent project inspired by G. Ann Campbell's research, but it's
not affiliated with or endorsed by SonarSource" — **VERSION-DEPENDENT (complexipy 6.2.0)**.

**The threshold-bearing lint codes, with their exact defaults and stability — VERSION-DEPENDENT
(ruff 0.16.2, pylint 4.0.6).** Stable in ruff: `C901` `complex-structure`
(`lint.mccabe.max-complexity` = **10**), `PLR0911` `too-many-return-statements` (`max_returns`
**6**), `PLR0912` `too-many-branches` (`max_branches` **12**), `PLR0913` `too-many-arguments`
(`max_args` **5**), `PLR0915` `too-many-statements` (`max_statements` **50**), `PLR0917`
`too-many-positional-arguments` (`max_positional_args` **5**, and **stable only since ruff 0.16.0**
— preview before that). **Preview-only, and therefore silently inert without `--preview`:**
`PLR0904` `too-many-public-methods` (**20**), `PLR0914` `too-many-locals` (**15**), `PLR0916`
`too-many-boolean-expressions` (**5**), `PLR1702` `too-many-nested-blocks` (**5**). Also from ruff's
settings source: `max_statements_in_try` **5**. pylint's design checker carries the same numbers
under `R0911`, `R0912`, `R0913`, `R0914`, `R0915`, `R0916`, `R0917`, `R1702`, plus `R0901`
`too-many-ancestors` (`max-parents` **7**), `R0902` `too-many-instance-attributes` (**7**), `R0903`
`too-few-public-methods` (`min-public-methods` **2**), `R0904` `too-many-public-methods` (**20**).
**pylint has no cyclomatic-complexity message at all** — `R0912` counts branches, a related but
different quantity — so "use pylint's complexity rule" is a null instruction; use ruff `C901` or
radon — **ESTABLISHED**.

Two gate hazards in that list, both **VERSION-DEPENDENT (ruff 0.16.2)**: adding a preview rule to
`select`, seeing a clean run and reporting success teaches you nothing, because the rule never ran;
and `PLR0917` becoming stable in 0.16.0 means config written against an older ruff can start
*failing* on upgrade. And one design hazard, **ESTABLISHED**: `PLR0911` (too many returns) and
`PLR1702` (too many nested blocks) pull against each other, because early return is the standard
remedy for nesting and nesting is the standard consequence of forbidding returns. Pick one and
disable the other, or an agent will oscillate between them across commits.

### 9.4 The starter set: seven numbers for a small project

Seven is already a lot. Adding an eighth needs a written reason. Each row states what the number is
evidence of, what it is **not** evidence of, and whether it is safe as a gate.

| # | number | how measured (exact) | evidence of | **NOT** evidence of | gate or diagnostic | tag |
|---|---|---|---|---|---|---|
| 1 | cyclomatic complexity per function <= 10 | `ruff check` with `C901`, `lint.mccabe.max-complexity = 10` | a function whose path count is within reach of a test suite | readability; correct decomposition; anything at all above function level | **GATE** (per-unit, monotone, cheap) | VERSION-DEPENDENT (ruff 0.16.x) |
| 2 | cognitive complexity per function <= 15 | `complexipy . --max-complexity-allowed 15` | correlation with human comprehension *time* and subjective ratings (ESEM 2020) | comprehension *correctness*; that the abstraction is right; 15 is SonarQube's default, not Campbell's recommendation | **GATE**, advisory first | VERSION-DEPENDENT (complexipy 6.2.0) |
| 3 | import-contract violations == 0 | `lint-imports` or `tach check` | who imports whom, right now | behavioural conformance — claiming otherwise is a category error; nothing about `importlib`, `getattr` or plugin registries | **GATE** | VERSION-DEPENDENT (import-linter 2.13 / Tach 0.35.0) |
| 4 | branch coverage floor + changed-line coverage | `coverage run --branch`, `[report] fail_under` at the measured floor with `precision = 2`; `diff-cover` on the diff | which lines and branches were never executed | test quality — "coverage ... should not be used as a quality target" (Inozemtseva & Holmes, verbatim) | **GATE** as a floor; **never** a rising target | ESTABLISHED |
| 5 | suppression debt, monotonically non-increasing | §4.5 formula; census via `ruff check --ignore-noqa --statistics` | how much checking the project has switched off | type soundness; that the remaining suppressions are justified (no rule requires a reason) | **GATE** (non-increasing, merge-base compared) | VERSION-DEPENDENT (ruff 0.16.2) |
| 6 | suite wall-clock under a stated budget | `pytest --durations=10 --durations-min=1.0`; total run time | whether the feedback loop is short enough to be used | adequate testing — and it is improved by *deleting* tests, so pair it with a test-count floor | **GATE** on the budget; diagnostic per test | ESTABLISHED |
| 7 | mutation score on the functional core | `mutmut run`, `mutmut export-cicd-stats` | where assertions are missing or weak — the strongest available targeting signal | fault-detection capability as a scalar: correlations are "weak when controlling for test suite size" (Papadakis et al.) | **DIAGNOSTIC ONLY.** Reviewed on a cadence; never gated | VERSION-DEPENDENT (mutmut 3.7.0) |

Two numbers deliberately **excluded** from the starter set, with reasons: **docstring coverage**
(§11.2) is cheap and fine to add, but it measures presence rather than content and buys less than
any row above; and **dead code** (`vulture --min-confidence 100`) is worth having as a gate but is
narrow — its 100% tier covers only unused arguments and unreachable code, which ruff's `F` and `ARG`
families already largely cover inside a single file. Vulture's unique contribution is cross-module
unused public functions, classes and attributes, which no per-file linter can see — **ESTABLISHED**
— and that is a real reason to add it as an eighth. Below 100% confidence it is not gate material:
the 60% tier covers attributes, classes, functions, methods, properties and variables, where dynamic
access, plugin registries and framework hooks generate false positives, and vulture's own
documentation concedes errors in both directions ("Due to Python's dynamic nature, static code
analyzers like Vulture are likely to miss some dead code. Also, code that is only called implicitly
may be reported as unused") — **ESTABLISHED**.

### 9.5 The structural numbers — the ones that genuinely ratchet

**OPEN** (the framing is the analyst's; each mechanism is cited). Structural counts are the best
ratchet material in this file because they satisfy all four properties of §1.1: they are per-unit,
monotone, deletion-resistant (deleting a module removes its violations *and* its value, which review
catches) and cheap.

| number | mechanism | terminal value | tag |
|---|---|---|---|
| import-contract violations | `lint-imports` / `tach check` — contracts owned by `python_module_boundaries_manifest.md` | **0** | VERSION-DEPENDENT (2.13 / 0.35.0) |
| package dependency cycles | import-linter's cycle contract, or Tach's "No cycles in the dependency graph"; `pydeps --show-cycles` as the diagnostic view | **0** | VERSION-DEPENDENT (2.13 / 0.35.0 / pydeps 3.0.7) |
| suppression debt | §4.5 | **0**, or a declared permanent allowance | VERSION-DEPENDENT (ruff 0.16.2) |
| type-error baseline size | `mypy-baseline.txt` line count, merge-base compared | **0**, then delete the file | VERSION-DEPENDENT (0.7.4) |
| annotation coverage | `mypy --linecount-report` / `--lineprecision-report` / `--any-exprs-report` | project-defined; for a library, `pyright --verifytypes` completeness | ESTABLISHED |
| fan-in / fan-out of a module | `grimp`: `find_modules_that_directly_import()` (fan-in), `find_modules_directly_imported_by()` (fan-out), `count_imports()` | **no tool ships a threshold — you must pick and defend one** | VERSION-DEPENDENT (grimp 3.15) |

Two cautions. **No tool ships a fan-in threshold**, so any number you gate on is your invention;
track it as a diagnostic first and expect the "god module" to be obvious without a threshold —
**OPEN**. And **do not build a gate on `ruff analyze graph`**: it emits JSON but self-declares
"`ruff analyze graph` is experimental and may change without warning", and its JSON shape is not a
stable contract. Use `grimp` for anything load-bearing — **VERSION-DEPENDENT (ruff 0.16.x)**.

**Martin's package metrics are vocabulary, not measurement, in Python.** *OO Design Quality Metrics
— An Analysis of Dependencies* (Robert C. Martin, 28 October 1994) defines `Ca` afferent couplings,
`Ce` efferent couplings, `I : Instability : (Ce / (Ca+Ce))` in [0,1], `A : Abstractness` = abstract
classes / total classes, the Main Sequence as the A–I line from (0,1) to (1,0), and `D : Distance`
as the absolute value of `(A+I-1)/sqrt(2)` — **ESTABLISHED**. No maintained Python implementation
was verified this pass — **OPEN** — and `A` has no unambiguous Python meaning (ABC? `Protocol`?
both?), which the project would have to pin before the number means anything. Two related traps:
**the 1994 paper contains no cycles or acyclic-dependencies material at all**, so citing it for the
Acyclic Dependencies Principle is wrong — **ESTABLISHED**; and `limit-structural-complexity` (a
tactic named in Bass, Clements & Kazman, 2021) names "response-of-class, propagation cost, and
decoupling level" as its metrics — vocabulary worth knowing, with **no verified Python
implementation of any of the three** — **OPEN** (seed-pack vocabulary).

### 9.6 Process signals — real evidence, used as diagnostics

This is the uncomfortable part of the section, and it is stated because omitting it would be
dishonest.

**Process metrics beat static code metrics for defect prediction, at scale — ESTABLISHED.**
Majumder, Mody & Menzies, *Revisiting Process versus Product Metrics: a Large Scale Analysis* (arXiv
2008.09569; Empirical Software Engineering, 2022), using "722,471 commits from 700 Github projects":
"process metrics are better predictors for defects than product metrics (best process/product-based
learners respectively achieve recalls of 98%/44% and AUCs of 95%/54%, median values)". Their own
caveat is also on the record: metric-importance conclusions from small-scale studies shift at scale,
and they recommend using predictions from multiple models. The earlier result in the same direction
— Rahman & Devanbu, "How, and why, process metrics are better" (ICSE 2013, pp. 432–441, DOI
10.1109/ICSE.2013.6606589) — has a confirmed bibliographic record but was paywalled and not fetched,
so it is **FLAGGED-SECONDARY** and carried by the Majumder replication.

**What follows for this file:** if the goal is finding where defects will be, git history beats the
AST. Static gates remain worth having — they are cheap, they run per-commit, and they prevent
specific defect classes outright — but they must not be sold as the best available predictor.

**Three process signals worth computing, all diagnostics, never gates:**

1. **Change coupling / temporal coupling** — two or more modules that "change together over time".
   CodeScene's documentation states the load-bearing point: "Change coupling isn't possible to
   calculate from code alone", so dependencies are treated "as dynamic and temporal by analyzing
   developer behavior patterns" — **FLAGGED-SECONDARY** (surfaced via search summaries of the
   versioned CodeScene docs, not a direct page fetch). This is the one coupling signal
   `import-linter`, `grimp` and Tach structurally cannot see, which is exactly why it is worth
   computing from `git log`. Cross-reference: `spec_recovery_reverse_engineering_manifest.md` §6–§7
   already own the Git-forensics tradition.
2. **Churn × complexity hotspots** — the intersection of "changes constantly" and "is complex" is
   where cost concentrates. `wily` tracks metrics over git history (1.25.0 stable, `2.0.0a1`
   prerelease). **The strongest business-level result here is not reproducible with open tools:**
   Tornhill & Borg, *Code Red: The Business Impact of Code Quality* (arXiv 2203.04374, TechDebt
   2022), across **30,737 files in 39 proprietary production codebases**, found low-quality code
   contains **15× more defects**, issue resolution takes **124% more time** on average, and involves
   **9× longer maximum cycle times** — **ESTABLISHED**. But quality was measured with CodeScene, "a
   combination of source code analysis, version-control mining, and issue information from Jira", so
   the independent variable is a proprietary composite. A churn × cyclomatic-complexity list is a
   legitimate diagnostic; **it is not the measured construct from *Code Red* and must not be
   presented as such** — **ESTABLISHED**.
3. **Delivery metrics** — DORA now documents **five**, not four: "Change lead time" (from committed
   to version control to deployed in production), "Deployment frequency", "Failed deployment
   recovery time" (**not** "MTTR"), "Change fail rate", and "Deployment rework rate" ("the ratio of
   deployments that are unplanned but happen as a result of an incident in production"). The page
   states the metrics "have evolved alongside the technology landscape: shifting from the original
   four keys to the current five-metric model" — **VERSION-DEPENDENT (dora.dev page state
   2026-08-08)**. Writing "the four DORA metrics (MTTR ...)" in 2026 is a datable error. **Do not
   print a DORA band table:** the elite/high/ medium/low numeric thresholds and the survey
   methodology were not published on the pages fetched this pass — **OPEN** — and the widely
   repeated 2024 figures are **FLAGGED-SECONDARY**. Delivery metrics are team-level only;
   per-developer use is an abuse of the instrument.

**SonarQube's aggregate ratings, quoted only so an agent asked to "match SonarQube" knows what the
numbers mean — ESTABLISHED.** `sqale_debt_ratio` = technical debt / (cost to develop one line ×
lines of code), with a **default development cost of 30 minutes per line** — a modelling choice, not
a measurement — and maintainability (SQALE) bands A <= 5%, B >= 5% to < 10%, C >= 10% to < 20%, D >=
20% to < 50%, E >= 50%. Duplication for non-Java languages triggers on "at least 100 successive and
duplicated tokens" over 10 lines, with "Differences in indentation and in string literals are
ignored"; `duplicated_lines_density = duplicated_lines / lines * 100`. The self-hosted equivalent is
pylint `R0801` `duplicate-code`, whose defaults are `min-similarity-lines` **4** with
`ignore-comments`, `ignore-docstrings`, `ignore-imports` and `ignore-signatures` **all True** — so
two near-identical functions can go unreported — and whose module is now
`pylint/checkers/symilar.py` (a reference to `similar.py` is stale) — **VERSION-DEPENDENT (pylint
main; re-verify against 4.0.6)**.

---

## 10. Goodhart, explicitly

### 10.1 The metrics that invite gaming, and the counter-move

Every number in §9 can be satisfied without improving anything. Naming the specific move is what
makes the counter possible. **OPEN** (the gaming moves are the analyst's enumeration; each
counter-mechanism is cited in the section named).

| number | the gaming move | the counter | tag |
|---|---|---|---|
| total coverage % | write assertion-free tests; sprinkle `# pragma: no cover`; add one custom `exclude_lines` pattern, which silently drops the built-ins; **delete the untested module** — the percentage rises | branch coverage on; `exclude_also` never `exclude_lines`; `precision = 2`; changed-line gate; mutation sampling on the core; treat the floor as a floor, never a target | ESTABLISHED (§6.1, §6.2) |
| suppression count | move inline suppressions into `lint.per-file-ignores` (where an initial `!` negates the pattern, so one entry can cover most of a tree) or into an `ignore_errors` override; or narrow `select` so the rule never fires | count config-level suppressions in the budget; commit the **resolved** rule set and diff it (`ruff check --show-settings`, `ruff rule --all` — both confirmed by running ruff 0.16.2 in the fact-gathering pass, not from a documentation page); require a reason (contract-only — no rule enforces it) | VERSION-DEPENDENT (ruff 0.16.2) (§4.5) |
| complexity per function | extract forty three-line functions with a tangled call graph — every per-function metric goes green while the system gets worse (Shepperd's structural objection) | pair with the cycle and import-contract gates; review the call graph, not the histogram; never treat a metric improvement as evidence a refactor helped | ESTABLISHED (§9.2) |
| mutation score | mutate only trivial modules; grow `do_not_mutate` / `do_not_mutate_patterns`; set `mutate_only_covered_lines` and then reduce coverage | never gate it; review surviving mutants, not the ratio; keep `paths_to_mutate` under review as a committed decision | VERSION-DEPENDENT (mutmut 3.7.0) (§6.6) |
| suite wall-clock budget | delete the slow integration tests | pair the time budget with a test-count floor and a changed-line coverage gate | ESTABLISHED (§6.5) |
| docstring coverage | one-line "Does X." docstrings on every symbol | it is a shape check and must be described as one; content checks (numpydoc) are a separate, narrower gate | ESTABLISHED (§11.2) |
| dead-code count | add a dynamic reference (`getattr`, a registry entry) so the analyser stops seeing it as dead | gate only the 100% tier; keep the whitelist committed and reviewed | VERSION-DEPENDENT (vulture 2.16) (§9.4) |
| type-error baseline size | re-`sync` the baseline on a red build | merge-base comparison (§4.1 condition 1) — without it the ratchet does not exist | VERSION-DEPENDENT (0.7.4) |
| delivery metrics | split changes into more, smaller deployments to raise deployment frequency; reclassify incidents to lower change fail rate | team-level only, never per-developer; read the five together, never one alone; never make them a target | VERSION-DEPENDENT (dora.dev 2026-08-08) (§9.6) |
| Maintainability Index | add comments — radon's formula includes a comment-percentage term Microsoft's does not | do not gate on it at all | ESTABLISHED (§9.2) |

### 10.2 What cannot be measured, and must be reviewed by a human

**Every mechanised gate in this file is a lower bound on badness.** Passing all of them means no
listed hazard was detected. It does not mean any of the following, and no tool in this collection
touches them — **contract-only, and this is the largest residual risk in the whole document**:

- Is the abstraction at the right level?
- Do the names mean what they say?
- Is the domain model right?
- Is this the simplest thing that could work?
- Is the error message actionable to the person reading it at 3am?
- Is the test asserting **behaviour** or **implementation**?
- Does the module boundary fall on a real seam of change?
- Is the concurrency model justified, or is it there because it was interesting?

**A fully green pipeline over an incoherent design is the normal case, not an anomaly.** State that
in the review checklist, in those words. The gates buy attention: they remove the mechanical
objections from review so the reviewer's whole budget goes on the eight questions above. That is the
entire value proposition, and it is a large one — but it is not "quality assured".

**No metric in this file has been validated against maintenance effort in Python — OPEN.** Every
empirical study cited used Java, C, or a proprietary multi-language tool: the Landman corpus is Java
and C; the Inozemtseva, Just and Papadakis studies are Java (plus C for CoreBench); the MI
calibration is C and Pascal from the late 1980s at Hewlett-Packard; Campbell's validation
meta-analysis is language-mixed but not Python-specific. Transferring thresholds to Python is an
assumption, not a finding.

---

## 11. Documentation gates that are actually checkable

### 11.1 Structure is standardised; style is not, and the project must choose

PEP 257's normative content, the subtractive `lint.pydocstyle.convention` mechanism and the exact
disabled-code list for each convention are owned by `python_linting_practices_manifest.md` §6.3 and
§15.1. PEP 257 standardises the high-level structure of a docstring and explicitly declines to
choose
a markup syntax, so the numpydoc-versus-Google decision sits above it and must be made by the
project rather than inherited — **ESTABLISHED**.

**The gate obligations are two, and both are one-line configuration decisions.** (a) `select =
["D"]` **together with** an explicit `convention`: the convention setting only *subtracts*, so it
selects nothing on its own, and it filters a *prefix* selection only — a code re-added by exact code
through `extend-select` re-enables precisely the rule the convention was chosen to suppress
(**MEASURED (ruff 0.16.2)**: `uvx ruff@0.16.2 check --config <cfg> --show-settings <file>`,
comparing
`linter.rules.enabled` with and without the convention set). (b) numpydoc validation with an
explicit
`checks` allowlist, for the reason below.

**Content, as opposed to shape, is numpydoc's validation layer — ESTABLISHED.** Configured under
`[tool.numpydoc_validation]` with `checks`, `exclude` (regular expressions for objects to skip) and
`override_SS05`, exposed as `numpydoc lint` and as the pre-commit hook id `numpydoc-validation`. Its
check codes are `GL01`, `GL02`, `GL03`, `GL05`, `GL06`, `GL07`, `GL08`, `GL09`, `GL10`;
`SS01`–`SS06`; `ES01`; `PR01`–`PR10`; `RT01`–`RT05`; `YD01`; `SA01`–`SA04`; `EX01`.

**`checks = ["all"]` is an indefensible required gate on most projects.** Three of the codes demand
prose on every documented object regardless of whether it warrants any: `ES01` "No extended summary
found", `SA01` "See Also section not found", `EX01` "No examples section found". The defensible form
is an explicit allowlist, or `"all"` minus those three — **ESTABLISHED** (from the code list; the
judgement is the analyst's).

### 11.2 Presence is a separate, cheaper number

**VERSION-DEPENDENT (interrogate 1.7.0).** interrogate "Interrogate a codebase for docstring
coverage" and gates with `--fail-under` (configuration default `fail-under = 80`), with `ignore-*`
switches for init/magic/private/nested/overloaded/property/setter plus `ignore-regex`,
`whitelist-regex`, `omit-covered-files` and `--generate-badge`. It measures **presence, not
quality** — the same job ruff's `D1xx` family does inside the linter, which is why most projects do
not need both. Last release 2024-04-07. **Conflict noted and resolved:** one fact pack left
interrogate's threshold flag name unverified; the flag `--fail-under` and the default of 80 were
confirmed from interrogate's own README in the other pass, and that is what is stated here.

**Presence is a diagnostic, not a gate — OPEN** (the judgement is the analyst's; the tool facts
above
are not). `D1xx` inside the linter is the gate, because it is already required at `P` and `C` by
ledger row 24 and it fails per object rather than against a project-wide percentage. Running
interrogate *as well* double-counts the same property and adds a second threshold to argue about, so
ledger row 26 is advisory and stays advisory: keep it for the number and the badge, never as a
required status check.

### 11.3 Executable examples

**ESTABLISHED.** doctest is invoked as `python -m doctest [-v] [-o OPTION] [-f] file [file ...]`
(`-f` is shorthand for `-o FAIL_FAST`), or programmatically via `doctest.testmod(...)` and
`doctest.testfile(...)`, both returning `(failure_count, test_count)`. Directives are per-example
comments of the form `# doctest: +OPTION_NAME, -OTHER_OPTION`. Option flags:
`DONT_ACCEPT_TRUE_FOR_1`, `DONT_ACCEPT_BLANKLINE`, `NORMALIZE_WHITESPACE`, `ELLIPSIS`,
`IGNORE_EXCEPTION_DETAIL`, `SKIP`, `COMPARISON_FLAGS`; reporting flags `REPORT_UDIFF`,
`REPORT_CDIFF`, `REPORT_NDIFF`, `REPORT_ONLY_FIRST_FAILURE`, `FAIL_FAST`, `REPORTING_FLAGS`.
unittest integration is via `doctest.DocTestSuite`, `doctest.DocFileSuite` and a `load_tests`
function, with `doctest.set_unittest_reportflags()` for report flags.

Its fragility is documented rather than incidental (§6.4), so the standing gate configuration is
`+ELLIPSIS` and `+NORMALIZE_WHITESPACE`, and any example printing a set, a dict, a float repr or an
object address needs one of them explicitly. **The pytest flags for collecting doctests (the
`--doctest-modules` / `--doctest-glob` family) were not verified against a primary page this pass —
OPEN.** Use `python -m doctest` until they are, or verify them yourself before writing them into
`addopts`.

**A second, quieter formatting gate interacts with documentation.** Since ruff 0.16.0, `ruff format`
formats Python code blocks inside Markdown files **by default** (info strings `python`, `py`,
`python3`, `py3`, `pyi`, `pycon`), suppressible with `<!-- fmt: off -->` / `<!-- fmt: on -->`. A
repository whose docs contain deliberately broken example code will find it silently corrected —
**VERSION-DEPENDENT (ruff 0.16.0)**. Relatedly, `format.docstring-code-format` defaults to `false`
with `docstring-code-line-length` defaulting to `dynamic`; turning the first on formats code inside
docstrings, which is usually what you want if you gate doctests — **VERSION-DEPENDENT (ruff
0.16.x)**.

### 11.4 The docs tree, and the build as a gate

**ESTABLISHED.** Diataxis organises documentation on two axes. Action versus cognition: "tutorials
and how-to guides are concerned with what the user does (action)" while "reference and explanation
are about what the user knows (cognition)". Acquisition versus application: "tutorials and
explanation serve the acquisition of skill (the user's study)" whereas "how-to guides and reference
serve the application of skill (the user's work)". The four one-line definitions: "A tutorial is a
lesson that takes a student by the hand through a learning experience." "A how-to guide addresses a
real-world goal or problem by providing practical directions." "Reference guides contain the
technical description - facts - that a user needs in order to do things correctly." "Explanatory
guides provide context and background to help answer the question why?"

**What is mechanically checkable about Diataxis is the tree, not the writing.** A CI check that the
four top-level sections exist and that no page sits outside them is a fitness function a project can
write in ten lines; whether a given page is really a how-to guide is **contract-only**.

**The generator choice is about liveness and input format, not aesthetics — VERSION-DEPENDENT.**
Sphinx 9.1.0 (2025-12-31) requires Python `>=3.12` and is reST-first with an autodoc pipeline that
can extract and check API documentation from source. MkDocs 1.6.1 (2024-08-30) requires `>=3.8` and
has had no release in roughly 23 months; it is Markdown-first. Which Sphinx extension renders
numpydoc/Google-style docstrings was not re-verified on a primary page this pass — **OPEN**
(`python_typing_contract_manifest.md` cites `sphinx.ext.napoleon` from its earlier pass). Either
way, the gate is the same: **the docs build is a required CI job and warnings are errors**, because
a broken cross-reference is the documentation equivalent of a type error.

### 11.5 The ADR is the decision record

**ESTABLISHED** (adr.github.io). An **Architectural Decision (AD)** is "A justified design choice
that addresses a functional or non-functional requirement that is architecturally significant"; an
**Architecturally Significant Requirement (ASR)** is "A requirement that has a measurable effect on
the architecture and quality of a software and/or hardware system"; an **ADR** "Captures a single AD
and its rationale". Michael Nygard's 2011 post *Documenting Architecture Decisions* is credited with
popularising the concept, and the Y-statement form is attributed to Zdun et al., *Sustainable
Architectural Decisions*. **The current version of the MADR template, and the names of the seven
templates compared in the WICSA 2015 paper referenced by adr.github.io, could not be confirmed —
OPEN.** Cite MADR as a template family; do not pin a version you have not read.

**Why an ADR is a gate concern and not just a documentation concern.** Every ratchet in §4 involves
a committed number whose *reason* is nowhere in the number. The bound belongs in the repository; the
argument for it belongs in an ADR next to it. The corpus's own problem statement for the element is
the failure mode: without the record, later maintainers "either cargo-cult the decision or blindly
reverse it" — **ESTABLISHED** (seed-pack vocabulary, naming source Nygard 2011).

**Three checkable properties, and one that is not — OPEN** (project conventions): that every ADR
file matches the naming scheme; that every ADR has a status field drawn from a fixed vocabulary; and
that every gate bound in configuration cites an ADR number in a comment — all three are greppable
fitness functions. Whether the decision recorded was a *good* decision is contract-only, which puts
it in §10.2 with everything else that matters most.

---

## Anti-patterns checklist

Reject on sight.

- **A coverage number as the goal.** Any sentence of the form "raise coverage to N%" — violates
  §6.2. The floor exists to detect a *fall*; a rising target buys assertion-free tests.
- **A gate nobody can run locally.** A flag in the CI YAML that appears nowhere in the repository's
  tool configuration — violates §3.1. Release-time publishing is the only permitted exception
  (§3.4).
- **An advisory gate that stays advisory forever.** `continue-on-error: true`, `--exit-zero`, or
  `semgrep scan` without `--error`, with no dated removal — violates §1.3 and §4.7.
- **A ratchet with no floor.** A bound that only tightens, with no stated terminal value, step size,
  cadence or owner — violates §4.1 conditions 4 and 5. It ends as a disabled gate.
- **A ratchet compared against itself.** CI reading the committed baseline at HEAD instead of at the
  merge base — violates §4.1 condition 1. This is not a weak ratchet; it is not a ratchet.
- **Autofix in CI.** `ruff check --fix` in a CI job — violates §3.5. It exits `0` after rewriting
  files and the rewrites are thrown away.
- **Pinning nothing.** `ruff>=0.16,<0.17`, an unpinned pre-commit `rev` tag, no lock file, or `uv
  run --frozen` in CI — violates §3.2, §4.1 and §7.1. Ruff's own policy admits behaviour changes
  into PATCH releases; a range is not a reproducible gate.
- **`select` used to "tighten" the rule set.** Writing `select = ["E", "F"]` on ruff 0.16.x discards
  the ~413-code default; `extend-select` is the additive form — violates §2 and the linting
  manifest's ownership of the rule set.
- **Branching on `$? -eq 1`.** Violates §1.3. coverage.py fails with `2`, vulture with `3`, zizmor
  with `11`–`14`.
- **Preview rules as required gates.** `PLR0904`, `PLR0914`, `PLR0916`, `PLR1702`, `RUF105`,
  `RUF106` are preview and are silently inert without `--preview` — violates §9.3.
- **`strict = true` inside `[[tool.mypy.overrides]]`.** Does nothing; and `mypy --strict` on the
  command line loses to a per-module section — violates §4.3.
- **`follow_imports = "skip"` as a migration tool.** It makes the module `Any` and deletes checking
  at the boundary — violates §5.2.
- **"We run `--strict`" offered as a claim about unreachable code.** Nine high-value codes are
  outside `--strict` — violates §5.1.
- **A suppression budget that counts only inline comments.** Debt launders into
  `lint.per-file-ignores` and `ignore_errors` — violates §4.5.
- **`ruff check --add-noqa` run because CI was red.** It is a debt-creation tool; it deletes the
  signal — violates §4.2.
- **`RUF100 --fix` run over a repo carrying other tools' directives** without the second `#` guard —
  it deletes working suppressions — violates §4.5.
- **Mutation score, docstring coverage or the Maintainability Index as a required gate.** Violates
  §6.6, §11.2 and §9.2 respectively — `interrogate` is ledger row 26 and is advisory there for
  exactly this reason. MI is not gate material at all.
- **A project-average complexity figure reported as a maintainability score.** Violates §9.2 — above
  the method level, complexity is a size proxy.
- **A complexity threshold migrated between radon and ruff without re-measuring.** They count
  different constructs — violates §9.3.
- **Citing "15" as Campbell's cognitive-complexity limit,** or Martin 1994 for the Acyclic
  Dependencies Principle, or "the four DORA metrics (MTTR ...)". Each is a datable fabrication —
  violates §9.1, §9.5 and §9.6.
- **A green `lint-imports` or `tach check` run presented as behavioural conformance.** It is a
  category error — violates §9.4 row 3.
- **Per-developer delivery metrics.** Violates §9.6 and §8.6.
- **`numpydoc checks = ["all"]` as a required gate.** `ES01`, `SA01` and `EX01` fail almost every
  real codebase on day one — violates §11.1.
- **A `[tool.flake8]` table in `pyproject.toml`.** flake8 reads only `setup.cfg`, `tox.ini` or
  `.flake8`; the gate runs with defaults and nobody notices — violates §1.1 (ESTABLISHED: flake8 has
  no `pyproject.toml` support).
- **`bandit -r .` with configuration in `pyproject.toml`.** It is ignored unless passed with `-c` —
  violates §2.1 row 19.
- **A pre-commit hook scoped `stages: [pre-push]` with only the `pre-commit` hook type installed.**
  The gate is inert — violates §3.2.
- **`xfail_strict` left at its default `False`.** A fixed bug never removes its own marker —
  violates §6.3.
- **An automatic test retry in the default CI path.** It destroys the signal it appears to fix —
  violates §6.4.
- **`mutmut run` in a Windows CI leg.** It requires `fork`; use WSL or do not run it — violates
  §6.6.
- **A CI matrix that skips a missing interpreter.** A leg that never ran reports green — violates
  §3.3 and §8.5.
- **A matrix whose oldest leg has left support, or with no leg for the next release.** Stale in both
  directions at once — violates §8.5; the dates are `python_platform_baseline_manifest.md` §1a's.
- **A release toggle with no expiry and no removal task.** Toggles are inventory with a carrying
  cost — violates §8.2.
- **Rebuilding the artefact between pipeline stages.** The later stages test a different program —
  violates §3.5.
- **`password:` in `pypa/gh-action-pypi-publish`.** It silently disables Trusted Publishing *and*
  the default attestations — violates §7.4.
- **A sentence claiming attestations block installation, or that SPDX 3.0 is ISO/IEC 5962, or an
  invented SBOM metadata field.** Each is unverified or false — violates §7.4 and §7.5.

---

## Open questions to resolve before building

Each is a decision the project must make and record. Cross-reference:
`software_spec_discipline_manifest.md` §G5 (open items split into ASSUMED versus NEEDS-INPUT).

1. **OPEN — Which runner is the single definition of a gate?** `uv run --locked` alone, `pre-commit`
   for file-scoped gates, or a `noxfile.py`/tox environment set. Decide before the second
   interpreter leg exists, because retrofitting a runner rewrites every CI step (§3.3).
2. **OPEN — Which gates are required at `M`, and which are advisory with a dated removal?** Write
   the date. An advisory gate with no removal date is the most common way a standard evaporates
   (§1.3, §4.7).
3. **OPEN — What is each ratchet's terminal value, step size, cadence and owner?** Suppression
   budget, baseline size, coverage floor, per-module strictness. A bound without these four is not a
   ratchet (§4.1).
4. **OPEN — Is the merge-base comparison implemented?** Name the script and the ref it reads.
   Without it every baseline in the repository is decorative (§4.1 condition 1).
5. **OPEN — Which cyclomatic-complexity limit, and on which tool's counting?** NIST publishes 10
   with the hedge that the number "remains somewhat controversial" and that 15 has been used
   successfully; radon and ruff compute different values for the same function (§9.1, §9.3).
6. **OPEN — Which cognitive-complexity threshold, given that the white paper states none?** 15 is
   SonarQube's default. Record the number as a decision, not as a citation (§9.1).
7. **OPEN — How is the ban on assertion-free tests enforced?** A `conftest.py` AST check, mutation
   testing as the oracle, or neither — in which case delete the rule rather than pretending it is
   enforced (§6.3).
8. **OPEN — Does a suppression require a written reason, and what checks it?** No ruff rule mandates
   justification text; a grep-based fitness function is the only mechanical route (§4.5).
9. **OPEN — What is the flake policy?** Quarantine marker, deadline, owner, and whether reruns are
   permitted anywhere. Do not adopt an industry flake-rate benchmark; none was confirmable (§6.4).
10. **OPEN — Which matrix legs are required and is `fail-fast` on?** And on what date does the
    next-release prerelease leg promote from advisory to required (§8.5, against the hub's
    calendar)?
11. **OPEN — Which toggle categories will this project actually use, and where does toggle
    configuration live?** Release toggles as committed constants is the cheap default; anything
    dynamic implies a flag service, whose Python SDK versions are unverified (§8.2).
12. **OPEN — Is an SBOM required, by whom, and in which format?** CycloneDX 1.7 or SPDX 3.0. If
    nobody has asked, the answer is no (§7.5).
13. **OPEN — Is reproducibility a required release gate?** The normative `SOURCE_DATE_EPOCH`
    specification was not read this pass, and non-flit backends may not normalise permission bits
    (§7.6).
14. **OPEN — Which docstring convention, and which numpydoc checks?** `lint.pydocstyle.convention`
    is subtractive; `checks = ["all"]` is indefensible. Both are one-line decisions with large blast
    radius (§11.1).
15. **OPEN — Where do ADRs live, and does every gate bound cite one?** The greppable form is a
    comment naming an ADR number beside each committed threshold (§11.5).

**Re-verification obligations — treat each as a rule, not a note.** Several facts in this file were
read from unversioned documentation pages during a single session (2026-08-08) and must be
re-checked on any upgrade of the tool concerned: the `lint.pydocstyle.convention` behaviour measured
in §11.1 — that the convention filters *prefix* selections only, so an exact-code selection survives
it — which is measured against ruff 0.16.2 and is nowhere promised as stable (the disabled-code
lists
themselves are `python_linting_practices_manifest.md` §6.3's to re-verify); the ruff `PLR*` defaults
and preview statuses (§9.3),
which were read from ruff's source tree on `main` rather than from the 0.16.2 tag; pylint's
`symilar.py` defaults, read from `main` and to be re-verified against 4.0.6 (§9.6); pyright's
configuration defaults, read from `main` with no version pin (§5.2); tox's native-TOML arrival
version, which reached this pass only through search results (§3.3); and the DORA metric set, whose
page state is dated but unversioned (§9.6). **Rule: on any minor upgrade of ruff, mypy, pylint or
pyright, re-read the settings page before trusting a default stated here.**

---

## Sources (accessed 8 Aug 2026)

**Version pins.** Current version, release date and `requires_python` for every tool in the
Version-anchor
table were read from the PyPI JSON API —
`https://pypi.org/pypi/{ruff,pylint,flake8,pre-commit,uv,nox,tox,mypy,pyright,ty,mypy_baseline,pytest,pytest-cov,pytest-xdist,coverage,diff-cover,mutmut,cosmic-ray,pip-audit,bandit,semgrep,zizmor,cyclonedx-bom,vulture,complexipy,radon,xenon,wily,interrogate,import-linter,grimp,tach,pydeps,deptry,sphinx,mkdocs}/json`
(and the per-version endpoints for the pinned releases). Accessed 8 Aug 2026.

**Linting, formatting and suppression as gates**

- ruff 0.16.0: release date, "413 rules by default, up from 59", the 18 removed E/F codes, `ruff:
  ignore[...]` / `ruff: file-ignore[...]`, Markdown code-block formatting —
  https://astral.sh/blog/ruff-v0.16.0 , confirmed independently at
  https://github.com/astral-sh/ruff/releases/tag/0.16.0 . Accessed 8 Aug 2026.
- ruff linter: `select`/`extend-select`/`ignore`/`fixable`/`unfixable` semantics, resolution
  priority, `ALL`, noqa and range suppression, `RUF100`, exit codes 0/1/2, `--exit-zero`,
  `--exit-non-zero-on-fix`, `--add-noqa`, `# flake8: noqa` equivalence —
  https://docs.astral.sh/ruff/linter/ and
  https://raw.githubusercontent.com/astral-sh/ruff/main/docs/linter.md . Accessed 8 Aug 2026.
- ruff formatter: Black compatibility, the formatter-conflicting rule list (`W191`, `E111`, `E114`,
  `E117`, `Q000`–`Q004`, `COM812`, `COM819`), `docstring-code-format` —
  https://docs.astral.sh/ruff/formatter/ . Accessed 8 Aug 2026.
- ruff configuration and settings: `line-length = 88`, file precedence, `extend`, `target-version`
  fallback to `requires-python`, `respect-gitignore`, `force-exclude`, `lint.pydocstyle.convention`
  values, `lint.per-file-ignores` with its `!` negation, `lint.mccabe.max-complexity` default 10,
  `lint.pylint.max-args` default 5, preview defaults — https://docs.astral.sh/ruff/configuration/
  and https://docs.astral.sh/ruff/settings/ . Accessed 8 Aug 2026.
- ruff versioning policy: what MINOR and PATCH bumps may change, the pre-1.0 stability statement,
  preview-first for new rules — https://docs.astral.sh/ruff/versioning/ . Accessed 8 Aug 2026.
- ruff rules index: the prefix-to-origin table, "over 900 lint rules", and the preview/stable status
  and introducing version for `C901`, `PLR0904`/`0911`/`0912`/`0913`/`0914`/`0915`/`0916`/`0917`,
  `PLR1702`, `PGH003`, `PGH004`, `RUF100`, `ERA001` — https://docs.astral.sh/ruff/rules/ . Accessed
  8 Aug 2026.
- the individual per-rule pages for `C901` ("the complexity of the control flow graph of the
  function", "add[ing] one to the number of decision points"), `PGH003` (and its cross-reference to
  mypy's `ignore-without-code`), `PGH004` (bare `# noqa`, partial fix, "may introduce additional
  diagnostics") and `RUF100` (always-fixable, the second-`#` guidance, the `invalid-rule-code`
  alternative) — https://docs.astral.sh/ruff/rules/complex-structure/ ,
  https://docs.astral.sh/ruff/rules/blanket-type-ignore/ ,
  https://docs.astral.sh/ruff/rules/blanket-noqa/ , https://docs.astral.sh/ruff/rules/unused-noqa/ .
  Accessed 8 Aug 2026.
- ruff source, for defaults and counting rules that no page states: the pylint thresholds
  (`max_args` 5, `max_positional_args` 5, `max_returns` 6, `max_bool_expr` 5, `max_branches` 12,
  `max_statements` 50, `max_statements_in_try` 5, `max_public_methods` 20, `max_locals` 15,
  `max_nested_blocks` 5); exactly which statements `C901` counts; `ruff analyze graph` and its
  "experimental and may change without warning" notice; `ruff check --statistics`,
  `--add-noqa[=reason]`, `--add-ignore[=reason]` —
  https://raw.githubusercontent.com/astral-sh/ruff/main/crates/ruff_linter/src/rules/pylint/settings.rs
  ,
  https://raw.githubusercontent.com/astral-sh/ruff/main/crates/ruff_linter/src/rules/mccabe/rules/function_is_too_complex.rs
  , https://raw.githubusercontent.com/astral-sh/ruff/main/crates/ruff/src/args.rs ,
  https://raw.githubusercontent.com/astral-sh/ruff/main/crates/ruff/src/commands/analyze_graph.rs .
  **Read from `main`, not from the 0.16.2 tag — re-verify on upgrade.** Accessed 8 Aug 2026.
- ruff-pre-commit hook ids `ruff-check` / `ruff-format` / the legacy `ruff` alias, their `entry`
  lines with `--force-exclude`, and `types_or` —
  https://raw.githubusercontent.com/astral-sh/ruff-pre-commit/main/.pre-commit-hooks.yaml . Accessed
  8 Aug 2026.
- pylint 4.0: astroid 4.0.0, Python 3.14 support, the module-level-constant naming change —
  https://pylint.pycqa.org/en/stable/whatsnew/4/4.0/index.html . Accessed 8 Aug 2026.
- pylint messages: the R09xx / R17xx / R0801 code-to-symbol mapping, `useless-suppression` /
  `I0021`, and the absence of any cyclomatic-complexity message —
  https://pylint.readthedocs.io/en/latest/user_guide/messages/messages_overview.html . Accessed 8
  Aug 2026.
- pylint source, for defaults: the design-checker numbers (`max-args` 5, `max-positional-arguments`
  5, `max-locals` 15, `max-returns` 6, `max-branches` 12, `max-statements` 50, `max-parents` 7,
  `max-attributes` 7, `min-public-methods` 2, `max-public-methods` 20, `max-bool-expr` 5) and
  duplicate-code's `DEFAULT_MIN_SIMILARITY_LINE = 4` with all four `ignore-*` options True, in the
  renamed `symilar.py` —
  https://raw.githubusercontent.com/pylint-dev/pylint/main/pylint/checkers/design_analysis.py and
  https://raw.githubusercontent.com/pylint-dev/pylint/main/pylint/checkers/symilar.py . **Read from
  `main` — re-verify against 4.0.6.** Accessed 8 Aug 2026.
- flake8 reads only `setup.cfg`, `tox.ini` or `.flake8`, always an INI `[flake8]` section, with no
  `pyproject.toml` support; CLI > project config > defaults —
  https://flake8.pycqa.org/en/latest/user/configuration.html . Accessed 8 Aug 2026.

**Gate composition and parity**

- pre-commit: the full config schema with defaults, the eleven valid stage names and the 3.2.0
  rename, and the CLI surface (`install`, `install-hooks`, `run
  --all-files`/`--from-ref`/`--to-ref`/`--hook-stage`/`--show-diff-on-failure`, `autoupdate
  --freeze`/`--bleeding-edge`, `migrate-config`, `try-repo`, `gc`) — https://pre-commit.com/ .
  Accessed 8 Aug 2026.
- the `.pre-commit-hooks.yaml` author contract with every key and default, and "The hook must exit
  nonzero on failure or modify files." — https://pre-commit.com/#new-hooks . Accessed 8 Aug 2026.
- uv: `uv lock` / `uv sync` / `uv run` semantics; `--locked` raises on a stale lockfile; `--frozen`
  skips the check; `uv lock --check`; `--exact`/`--inexact`; `--upgrade-package` —
  https://docs.astral.sh/uv/concepts/projects/sync/ . Accessed 8 Aug 2026.
- nox: `@nox.session` parameters, the seven `venv_backend` values and `|` chaining, `nox.options`
  including `error_on_missing_interpreters`, `session.install`/`run(external=True)`/`notify`,
  `@nox.parametrize` — https://nox.thea.codes/en/stable/config.html . Accessed 8 Aug 2026.
- GitHub Actions matrices: `strategy.matrix`, `include` ordering and overwrite semantics, `exclude`,
  `fail-fast` cancelling in-progress and queued jobs, `max-parallel`; the maximum job count is
  **not** stated on the page —
  https://docs.github.com/en/actions/using-jobs/using-a-matrix-for-your-jobs . Accessed 8 Aug 2026.

**Type checking as a gate**

- mypy configuration: `[mypy-PATTERN]` and `[[tool.mypy.overrides]]`, the six-level precedence
  order, the global-only option list, `strict` having no per-module form, `follow_imports`' four
  values, `warn_unused_ignores`, `ignore_errors`, and `disable_error_code`/`enable_error_code` with
  enable winning — https://mypy.readthedocs.io/en/stable/config_file.html . Accessed 8 Aug 2026.
- mypy command line: the count of flags `--strict` enables (13) and the standing caveat "the exact
  list of flags enabled by running `--strict` may change over time" — which is why §5.1 cites
  `python_typing_contract_manifest.md` §1 for the members rather than transcribing them;
  `--disallow-untyped-defs`/`--disallow-incomplete-defs`/`--disallow-any-expr`; the report flags
  `--any-exprs-report`, `--linecount-report`, `--lineprecision-report`, `--html-report`,
  `--txt-report`, `--cobertura-xml-report`, with the lxml requirement —
  https://mypy.readthedocs.io/en/stable/command_line.html . Accessed 8 Aug 2026.
- the optional error codes this file selects as gates — `ignore-without-code`, `unused-ignore`,
  `explicit-override`, `mutable-override`, `explicit-any`, `exhaustive-match`, `deprecated`,
  `unreachable`, `possibly-undefined`, `redundant-expr`, `truthy-bool` —
  https://mypy.readthedocs.io/en/stable/error_code_list2.html . Accessed 8 Aug 2026. The complete
  inventory is `python_typing_contract_manifest.md` §1's (§5.1).
- mypy 2.0 default flips (`--local-partial-types`, `--strict-bytes`, `--allow-redefinition-new`, the
  3.9 target dropped, `--num-workers`); 2.2's PEP 728 / PEP 696 work; 2.3's runtime-read-only
  `Final` — https://raw.githubusercontent.com/python/mypy/master/CHANGELOG.md . Accessed 8 Aug 2026.
- pyright: `--verifytypes <IMPORT>` "Verify completeness of types in py.typed package",
  `--ignoreexternal`, `--outputjson`; the type completeness score as "the percentage of symbols with
  known types" and what makes a symbol's type unknown; `enableTypeIgnoreComments` default `true` and
  `reportUnnecessaryTypeIgnoreComment` default `"none"` in **all four** modes —
  https://raw.githubusercontent.com/microsoft/pyright/main/docs/command-line.md ,
  https://raw.githubusercontent.com/microsoft/pyright/main/docs/typed-libraries.md ,
  https://raw.githubusercontent.com/microsoft/pyright/main/docs/configuration.md . **Read from
  `main` with no version pin.** Accessed 8 Aug 2026.
- mypy-baseline: `sync` / `filter`, stdout-only operation, and the merge-conflict-resistant,
  human-readable baseline claim —
  https://raw.githubusercontent.com/orsinium-labs/mypy-baseline/master/README.md . Accessed 8 Aug
  2026.

**Test gates**

- pytest reference: `addopts`, `filterwarnings`, `xfail_strict` default `False`, `required_plugins`,
  `minversion`, `testpaths`, `markers`, `norecursedirs`; `--strict-markers`, `--strict-config`,
  `-W`, `--import-mode`, `--maxfail`, `--durations`, `--deselect` —
  https://docs.pytest.org/en/stable/reference/reference.html . Accessed 8 Aug 2026.
- `--durations=N`, `--durations-min=THRESHOLD`, the documented example, and the "<0.005s hidden
  unless `-vv`" default — https://docs.pytest.org/en/stable/how-to/usage.html . Accessed 8 Aug 2026.
- the isolation framing of flakiness, "Tests that modify global state typically cannot be run in
  parallel", rerunning as mitigation, and the named plugins —
  https://docs.pytest.org/en/stable/explanation/flaky.html . Accessed 8 Aug 2026.
- coverage.py configuration: `[report] fail_under` (exit status 2; `precision` participates; 100
  fails anything under 100), `precision`, `exclude_lines` versus `exclude_also`, `partial_branches`
  versus `partial_also`, `[run] branch`/`parallel`/`relative_files`/`source`, `[paths]`, and the
  absence of any per-file threshold — https://coverage.readthedocs.io/en/latest/config.html .
  Accessed 8 Aug 2026.
- "If you provide a `--fail-under` value ... the command will exit with a status code of 2" —
  https://coverage.readthedocs.io/en/latest/commands/cmd_reporting.html . Accessed 8 Aug 2026.
- branch-coverage definition, `--branch`, partial-branch reporting, `# pragma: no branch`, and the
  documented limits including generator expressions and `while True:` / `if 0:` —
  https://coverage.readthedocs.io/en/latest/branch.html . Accessed 8 Aug 2026.
- coverage.py source: the `--format` help string "Output format, either text (default), markdown, or
  total."; `OK, ERR, FAIL_UNDER = 0, 1, 2`; the precision-aware `should_fail_under` —
  https://raw.githubusercontent.com/nedbat/coveragepy/master/coverage/cmdline.py . Accessed 8 Aug
  2026.
- pytest-xdist: `--dist load`/`loadscope`/`loadfile`/`loadgroup`/`worksteal`/`no`; `-n
  auto`/`logical`/`N`; `--max-worker-restart`; the `xdist_group` guarantee —
  https://pytest-xdist.readthedocs.io/en/stable/distribution.html . Accessed 8 Aug 2026.
- diff-cover: the diff-coverage definition ("If you touch a line of code, that line should be
  covered"), the git requirement, and the Cobertura/Clover/JaCoCo/LCov inputs —
  https://raw.githubusercontent.com/Bachmann1234/diff_cover/main/README.rst . Accessed 8 Aug 2026.
- mutmut: the status vocabulary including `caught by type check` (exit code 37); `export_cicd_stats`
  with the verbatim comment "exports CI/CD stats to block pull requests from merging if mutation
  score is too low"; the `[tool.mutmut]` keys; the `fork`/WSL requirement —
  https://raw.githubusercontent.com/boxed/mutmut/main/src/mutmut/__main__.py ,
  https://raw.githubusercontent.com/boxed/mutmut/main/src/mutmut/configuration.py ,
  https://raw.githubusercontent.com/boxed/mutmut/main/README.rst . Accessed 8 Aug 2026.
- Inozemtseva & Holmes, *Coverage Is Not Strongly Correlated with Test Suite Effectiveness* (ICSE
  2014): 31,000 suites over five Java systems to 724,000 SLOC, the Kendall's tau tables (0.81–0.95
  uncontrolled; 0.50–0.83 normalised, HSQLDB at −0.35), and the verbatim conclusion that coverage
  "should not be used as a quality target" —
  https://www.cs.ubc.ca/~rtholmes/papers/icse_2014_inozemtseva.pdf . Accessed 8 Aug 2026.
- Just et al., FSE 2014: 357 real faults across 5 applications totalling 321,000 lines; "coupled to
  mutants for 73% of real faults"; a correlation "stronger than the correlation between statement
  coverage and real fault detection" —
  https://homes.cs.washington.edu/~rjust/publ/mutants_real_faults_fse_2014.pdf . Accessed 8 Aug
  2026.
- Papadakis, Shin, Yoo & Bae, ICSE 2018: "all correlations between mutation scores and real fault
  detection are weak when controlling for test suite size", the suite-size confound argument, and
  the reconciling top-ranked-suite finding —
  https://coinse.github.io/publications/pdfs/Papadakis2018hi.pdf . Accessed 8 Aug 2026.
- Google 2017: 4.2 million tests, "larger tests are more flaky", "a bug in production code 1/6th of
  the time" — https://testing.googleblog.com/2017/04/where-do-our-flaky-tests-come-from.html . And
  checked for the circulated "1.5% of tests are flaky" figure, which is **not** in the qualitative
  2016 post — https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html .
  Accessed 8 Aug 2026.

**Supply chain and release**

- pip-audit: the PyPI-JSON-API default service; `--vulnerability-service osv,pypi,esms`; `--format
  columns,json,cyclonedx-json,cyclonedx-xml,markdown`; `--strict` as a dependency-collection switch;
  `--require-hashes`; exit codes 0/1; "pip-audit is not a static code analyzer" and the
  malicious-package disclaimer — https://raw.githubusercontent.com/pypa/pip-audit/main/README.md .
  Accessed 8 Aug 2026.
- bandit: `.bandit` INI auto-detected with `-r`; YAML and `pyproject.toml [tool.bandit]` only via
  `-c`; `exclude_dirs` "YAML and TOML only"; `# nosec` and `# nosec B602, B607` —
  https://bandit.readthedocs.io/en/latest/config.html . Accessed 8 Aug 2026.
- semgrep: `semgrep scan` not failing on findings by default versus `semgrep ci` which does; the
  exit-code table (0,1,2,3,4,5,7,8,13); `--error`, `--baseline-commit`, `--sarif`, `--severity`,
  `--include`/`--exclude`; `nosem` — https://docs.semgrep.dev/cli-reference . Accessed 8 Aug 2026.
- zizmor: the audit-name list and the scope over GitHub Actions, Dependabot and pre-commit configs — https://docs.zizmor.sh/ ; and `--persona regular|pedantic|auditor` with their definitions, `--min-severity`/`--min-confidence`, `--format`, exit codes 0/1/2/3 and 11–14, `--offline`, `--no-online-audits`, `--gh-token`, `# zizmor: ignore[audit-name]` — https://docs.zizmor.sh/usage/ . Accessed 8 Aug 2026.
- PEP 751 Final: `pylock.toml` and its variant pattern, the required and optional keys, the
  per-package fields including `attestation-identities`, and the installers-only scope —
  https://peps.python.org/pep-0751/ . Accessed 8 Aug 2026.
- PEP 740 Final: `version`/`verification_material`/`envelope`, the in-toto v1 statement,
  `attestation_bundles` with `publisher`, the two permitted predicate types, the index MUST duties —
  https://peps.python.org/pep-0740/ . Accessed 8 Aug 2026.
- PEP 770 Final: `.dist-info/sboms/`, no new core metadata field, the CycloneDX-or-SPDX and UTF-8
  JSON guidance, "MUST be copied from wheels by install tools" — https://peps.python.org/pep-0770/ .
  Accessed 8 Aug 2026.
- PEP 702 Final: the status used in the version-anchor block, and the marker's static half — "Type
  checkers should produce a diagnostic whenever they encounter a usage of an object marked as
  deprecated." — https://peps.python.org/pep-0702/ . Accessed 8 Aug 2026. The `@deprecated()`
  signature and its runtime semantics are `python_module_boundaries_manifest.md` §9.3's, not
  restated here (§8.4).
- Trusted Publishing: the OIDC exchange, the 15-minute short-lived token, the long-lived-API-token
  threat statement, `permissions: id-token: write`, `uses: pypa/gh-action-pypi-publish@release/v1`,
  and `environment:` as "optional, but strongly encouraged" —
  https://docs.pypi.org/trusted-publishers/ and
  https://docs.pypi.org/trusted-publishers/using-a-publisher/ . Accessed 8 Aug 2026.
- the publish action: attestations on by default with `attestations: false` to disable; `password:`
  disabling Trusted Publishing; `repository-url`, `packages-dir` default `dist/`, `verify-metadata`,
  `skip-existing`, `print-hash`, `user` default `__token__` —
  https://raw.githubusercontent.com/pypa/gh-action-pypi-publish/unstable/v1/README.md . Accessed 8
  Aug 2026.
- "Current Version: 1.7", the JSON/XML/Protobuf encodings, and ECMA-424 —
  https://cyclonedx.org/specification/overview/ . Accessed 8 Aug 2026.
- SPDX 3.0 as the current document version, and "The SPDX specification is an international open
  standard (ISO/IEC 5962:2021)" — https://spdx.dev/use/specifications/ . Accessed 8 Aug 2026.
- wheel zip entries carrying per-file mtimes, `SOURCE_DATE_EPOCH` overriding them, and flit's
  permission-bit normalisation to 755 or 644 — https://flit.pypa.io/en/stable/reproducible.html .
  Accessed 8 Aug 2026.

**Incremental delivery**

- trunk-based development: the definition, the direct-to-trunk versus short-lived-PR variants, "key
  enabler of Continuous Integration and by extension Continuous Delivery", just-in-time release
  branches, and the absence of any numeric branch-lifetime ceiling —
  https://trunkbaseddevelopment.com/ . Accessed 8 Aug 2026.
- Pete Hodgson, 09 October 2017: the four toggle categories on the dynamism/longevity axes, the
  source-control configuration preference, and toggles as inventory with a carrying cost, expiry
  dates and time bombs — https://martinfowler.com/articles/feature-toggles.html . Accessed 8 Aug
  2026.
- Danilo Sato, 13 May 2014: parallel change, "also known as expand and contract", and the expand /
  migrate / contract phases — https://martinfowler.com/bliki/ParallelChange.html . Accessed 8 Aug
  2026.
- SonarQube: the six default "Sonar way" conditions, all scoped to new code, including coverage >=
  80.0% and duplication <= 3.0% —
  https://docs.sonarsource.com/sonarqube-cloud/standards/managing-quality-gates/introduction-to-quality-gates.md
  ; the definition of new code, its four forms, and the Clean as You Code rationale —
  https://docs.sonarsource.com/sonarqube-server/user-guide/about-new-code.md . Accessed 8 Aug 2026.

**Measurement**

- radon: the MI formula including its comment term, the "combines both SEI derivative and Visual
  Studio one" statement, the Halstead formula set, the raw-metric definitions, and "Maintainability
  Index is still a very experimental metric" — https://radon.readthedocs.io/en/latest/intro.html ;
  the CC rank table (1–5 A through 41+ F), the MI rank table (A 100–20, B 19–10, C 9–0), the
  `cc`/`mi`/`raw`/`hal` subcommands, and the absence of any threshold-failing flag —
  https://radon.readthedocs.io/en/latest/commandline.html ; and radon's exact CC accounting (Try,
  BoolOp, If/IfExp, Match, For/While, comprehension, assert; lambdas excluded) —
  https://raw.githubusercontent.com/rubik/radon/master/radon/visitors.py . Accessed 8 Aug 2026.
- xenon: `-b/--max-absolute`, `-m/--max-modules`, `-a/--max-average`, `-e/--exclude`, `-i/--ignore`,
  and "It will fail (i.e. it will exit with a non-zero exit code) when any of these requirements is
  not met." — https://raw.githubusercontent.com/rubik/xenon/master/README.rst . Accessed 8 Aug 2026.
- complexipy: `--max-complexity-allowed`, `--output-format`, `--top`, `--failed
  --suggest-refactors`, and the explicit non-affiliation with SonarSource —
  https://raw.githubusercontent.com/rohaquinlop/complexipy/main/README.md . Accessed 8 Aug 2026.
- vulture: the 60/90/100 confidence tiers, `--min-confidence`, `--make-whitelist`,
  `--ignore-decorators`, `--ignore-names`, exit codes 0/1/2/3, and the verbatim
  false-positive/false-negative admission —
  https://raw.githubusercontent.com/jendrikseipp/vulture/main/README.md . Accessed 8 Aug 2026.
- Cognitive Complexity white paper, G. Ann Campbell, SonarSource S.A., **Version 1.7, 29 August
  2023**: the CC critique, the three rules, the four increment types, the discounts, Appendix B, and
  the absence of any recommended threshold —
  https://www.sonarsource.com/docs/CognitiveComplexity.pdf . Accessed 8 Aug 2026.
- `DEFAULT_THRESHOLD = 15`, the `threshold` RuleProperty, and the early return on inner functions —
  https://raw.githubusercontent.com/SonarSource/sonar-python/master/python-checks/src/main/java/org/sonar/python/checks/CognitiveComplexityFunctionCheck.java
  . Accessed 8 Aug 2026.
- SonarQube metric definitions: complexity = 1 + conditional branches; cognitive complexity; the
  duplication thresholds with the indentation/string-literal exclusion; `duplicated_lines_density`;
  `sqale_debt_ratio` with its 30-minutes-per-line development cost; the maintainability rating bands
  — https://docs.sonarsource.com/sonarqube-server/user-guide/code-metrics/metrics-definition.md .
  Accessed 8 Aug 2026.
- Muñoz Barón, Wyrich & Wagner, ESEM 2020: ~24,000 understandability evaluations over 427 snippets;
  positive correlation with comprehension time and subjective ratings; mixed results for correctness
  and physiological measures — https://arxiv.org/abs/2007.12520 . Accessed 8 Aug 2026.
- Shepperd, *A critique of cyclomatic complexity as a software metric*, Software Engineering Journal
  3(2):30–36, 1988: the abstract's "no more than a proxy for ... lines of code", the CC–LOC Pearson
  table (0.84–0.92), "over a third of the studies", and the intra- versus inter-modular argument —
  https://www.cs.du.edu/~snarayan/sada/teaching/COMP3705/lecture/p1/cycl-1.pdf . Accessed 8 Aug
  2026.
- NIST SP 500-235, *Structured Testing* (Watson & McCabe, 1996): "The precise number to use as a
  limit, however, remains somewhat controversial ..." —
  https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication500-235.pdf . Accessed 8 Aug
  2026.
- Landman, Serebrenik & Vinju as summarised by the authors: 17.6M Java methods, 6.3M C functions,
  "only moderate" correlation, "not strong enough to conclude that CC is redundant with SLOC" —
  https://www.rascal-mpl.org/blog/2016/01/01/empirical-analysis-of-the-relationship-between-CC-and-SLOC/
  . Accessed 8 Aug 2026.
- Graylin Jay et al. (2009), *Cyclomatic Complexity and Lines of Code: Empirical Evidence of a
  Stable Linear Relationship* — **HTTP 403 this session; cited FLAGGED-SECONDARY on bibliographic
  metadata only** — https://www.scirp.org/journal/paperinformation?paperid=779 . Accessed 8 Aug
  2026.
- van Deursen's MI critique: Oman & Hagemeister 1992, Coleman et al. 1994, the HP C/Pascal
  calibration set, "without any recalibration", the power-law averaging objection, and "I have not
  been able to find a justification for these thresholds" —
  https://avandeursen.com/2014/08/29/think-twice-before-using-the-maintainability-index/ . Accessed
  8 Aug 2026.
- the exact Visual Studio MI formula (no comment term) and the 0–9 Red / 10–19 Yellow / 20–100 Green
  bands —
  https://learn.microsoft.com/en-us/visualstudio/code-quality/code-metrics-maintainability-index-range-and-meaning
  . Accessed 8 Aug 2026.
- grimp's ImportGraph API: `find_modules_that_directly_import`, `find_modules_directly_imported_by`,
  `count_imports`, `find_shortest_chain(s)`, `nominate_cycle_breakers`, and the `build_graph`
  options — https://raw.githubusercontent.com/seddonym/grimp/master/docs/usage.rst . Accessed 8 Aug
  2026.
- Tach's three enforcements (declared dependencies, public interface, no cycles), `tach init` /
  `tach check`, `tach.toml` `depends_on`, and the `deprecated` marker —
  https://raw.githubusercontent.com/gauge-sh/tach/main/README.md . Accessed 8 Aug 2026.
- deptry: the `deptry .` invocation, the inline `# deptry: ignore[...]` scope (it must sit on the
  `import` line, and `DEP002` / `DEP005` cannot be suppressed that way), and the `[tool.deptry]`
  `ignore` / `per_rule_ignores` options — https://deptry.com/usage/ . Accessed 8 Aug 2026. The page
  documents **no** exit code, so §1.3's and §2.1's exit contract for it is **MEASURED** (deptry
  0.25.1) rather than read; the five `DEP*` rules are `python_module_boundaries_manifest.md` §7.6's.
- pydeps: `--show-cycles`, `--max-bacon`, `--reverse`, `--externals`, and the Graphviz `dot`
  requirement — https://raw.githubusercontent.com/thebjorn/pydeps/master/README.rst . Accessed 8 Aug
  2026.
- Robert C. Martin, *OO Design Quality Metrics — An Analysis of Dependencies*, 28 October 1994: Ca, Ce, `I = Ce/(Ca+Ce)`, A, the Main Sequence, `D = |(A+I-1)/sqrt(2)|`; and the confirmed absence of any cycle or acyclic-dependencies content — https://linux.ime.usp.br/~joaomm/mac499/arquivos/referencias/oodmetrics.pdf . Accessed 8 Aug 2026.
- Majumder, Mody & Menzies, *Revisiting Process versus Product Metrics: a Large Scale Analysis*:
  722,471 commits from 700 GitHub projects; recalls 98%/44% and AUCs 95%/54% (medians); the
  small-scale caveat — https://arxiv.org/abs/2008.09569 . Accessed 8 Aug 2026.
- Rahman & Devanbu, "How, and why, process metrics are better", ICSE 2013, pp. 432–441 —
  bibliographic record confirmed, findings not fetched, cited **FLAGGED-SECONDARY** —
  https://doi.org/10.1109/ICSE.2013.6606589 . Accessed 8 Aug 2026.
- Tornhill & Borg, *Code Red: The Business Impact of Code Quality*, TechDebt 2022: 30,737 files
  across 39 proprietary codebases; 15× defects; 124% more time; 9× longer maximum cycle times;
  measured with CodeScene — https://arxiv.org/abs/2203.04374 . Accessed 8 Aug 2026.
- the current five-metric DORA model with exact names and definitions, and the shift "from the
  original four keys to the current five-metric model" —
  https://dora.dev/guides/dora-metrics-four-keys/ ; and checked for performance bands and survey
  methodology, neither of which is published — https://dora.dev/research/ . Accessed 8 Aug 2026.
- CodeScene documentation (Temporal Coupling and Hotspots guides): change and temporal coupling,
  including "Change coupling isn't possible to calculate from code alone" — **FLAGGED-SECONDARY**,
  surfaced via search-result summaries of the versioned docs rather than a direct page fetch.
  Accessed 8 Aug 2026.

**Documentation gates**

- PEP 257 Active: the structural scope of the PEP and its explicit refusal to specify a markup
  syntax — https://peps.python.org/pep-0257/ . Accessed 8 Aug 2026. Its normative content is quoted
  in `python_linting_practices_manifest.md` §15.1, not here.
- the complete numpydoc GL/SS/ES/PR/RT/YD/SA/EX check-code list; `[tool.numpydoc_validation]` with
  `checks`, `exclude`, `override_SS05`; `numpydoc lint`; the pre-commit hook id
  `numpydoc-validation` — https://numpydoc.readthedocs.io/en/latest/validation.html . Accessed 8 Aug
  2026.
- interrogate: `--fail-under` with configuration default 80, the `ignore-*` option set,
  `ignore-regex`, `whitelist-regex`, `omit-covered-files`, `--generate-badge` —
  https://raw.githubusercontent.com/econchick/interrogate/master/README.rst . Accessed 8 Aug 2026.
- doctest: `python -m doctest` and `-f`; `testmod`/`testfile` return values; the directive syntax;
  the full option-flag list; traceback matching; "doctest is serious about requiring exact matches
  in expected output"; `<BLANKLINE>`; the set/dict, address and float caveats;
  `DocTestSuite`/`DocFileSuite`/`load_tests` — https://docs.python.org/3/library/doctest.html .
  Accessed 8 Aug 2026.
- the four Diataxis types, the action/cognition and acquisition/application axes, and the one-line
  definition of each type — https://diataxis.fr/ and https://diataxis.fr/start-here/ . Accessed 8
  Aug 2026.
- the AD, ASR and ADR definitions; Nygard's 2011 post as the popularising source; the Y-statement
  attribution to Zdun et al. — https://adr.github.io/ . Accessed 8 Aug 2026.

**Named vocabulary imported from the SWE corpus.** Each carries its naming work and year as recorded
in `SWE/design_elements_corpus_v1_0.md`; these are print sources and no URL is asserted for them.
**Deployment Pipeline** — Humble & Farley, *Continuous Delivery*, 2010, ch. 5 "Anatomy of the
Deployment Pipeline" (§3.5). **Feature Toggle / Feature Flag** — Hodgson, *Feature Toggles (aka
Feature Flags)*, 2017, for the design element `feature-flag` and its parts, with the architecture
tactic `feature-toggle` from Bass, Clements & Kazman, *Software Architecture in Practice*, 4th ed.,
2021 (§8.2). **Package
Dependencies**, **Script Deployment Commands**, **Adhere to Standards**, **Limit Structural
Complexity**, **Specialized Interfaces**, **Executable Assertions**, **Scale Rollouts** —
architecture tactics named in Bass, Clements & Kazman, 2021 (§1.2, §3.5, §7.1, §8.6, §9.5).
**Immutable Infrastructure** — Kief Morris, *ImmutableServer*, 2013 (§7.1). **Architecture Decision
Record** — Nygard, *Documenting Architecture Decisions*, 2011 (§11.5).

### Sibling manifests (cross-referenced, not duplicated)

- **`python_platform_baseline_manifest.md`** — the single version anchor: CPython release dates,
  support phases and end-of-life, PEP status, interpreter switches, build variants and the
  minimum-target policy. This file states gate *behaviour* and cites the hub for *when*; the
  interpreter legs in §8.5 are consumed from it, not restated.
- **`python_typing_contract_manifest.md`** — the type system itself: unions, narrowing, protocols,
  `Never`, generics, what the type system cannot express, and checker strict modes as *semantics*.
  This file owns only their gate form: error-code selection, ignore hygiene, and the typing ratchet
  (§5).
- **`python_linting_practices_manifest.md`** — which ruff and pylint families to enable and why, the
  formatter/linter/checker division of labour, suppression *policy*, and the
  function/module/expression altitude catalogue. This file owns the *count* of suppressions as a
  budget (§4.5) and the exit contract of the lint command (§1.3) — not the rule set.
- **`python_language_hazards_manifest.md`** — the diagnosis: intrinsic Python footguns and the
  maximal-safety modern subset, each routed to its enforcement mechanism. The routes point here; the
  hazards live there.
- **`python_testing_tooling_manifest.md`** — test design: the unit/integration boundary, what to
  assert, fixtures, property-based testing, and coverage tooling mechanics. This file owns coverage
  *as a gate* — the commands, the exit contract, the required config values and the changed-lines
  ratchet (§6.1–6.2) — and defers the measurement semantics behind them to that file's §5a, the
  assertion-free-test tooling survey to its §5b, and everything about what a good test is.
- **`python_module_boundaries_manifest.md`** — project layout, packaging metadata, the import system
  as a boundary, the public-API and deprecation *contract*, plugin seams, and the import-contract
  types themselves (`import-linter`, Tach) and deptry's `DEP*` rules. This file owns their CI wiring
  (ledger rows 12, 13, 13a) and their violation
  counts as tracked numbers (§9.5), and the *enforcement* of a deprecation window (§8.4).
- **`error_tracing_contract_manifest.md`** — the error contract: propagation channels, typed
  results, exception chaining, exhaustiveness, and where runtime assertions belong. §8.6's note that
  `assert` is disabled under `-O` points there for placement.
- **`logging_observability_manifest.md`** — severity model, logger/handler/formatter architecture,
  structured logging, correlation IDs, and what must never be logged. Nothing in a gate emits
  telemetry; that file owns all of it.
- **`python_runtime_diagnostics_manifest.md`** — everything that inspects a running or crashed
  process: attach, monitoring, `faulthandler`, `tracemalloc`, profilers, post-mortem, health
  surfaces. A gate is static and pre-merge; that file is live and post-deploy.
- **`python_concurrency_determinism_manifest.md`** — the four execution models, structured
  concurrency, cancellation, and keeping concurrent code deterministic under test. §6.5's sharding
  modes are a gate concern; the shared-state design that makes sharding safe is that file's.
- **`architecture_manifest_default.md`** — the reasoning frame: coupling and cohesion as vocabulary,
  seams, functional core / imperative shell. Reasoning register; it names tradeoffs and refuses to
  prescribe. §9.5's mechanised coupling numbers are the measurable shadow of its §3.1.
- **`software_spec_discipline_manifest.md`** — spec discipline, and §G5's split of open items into
  ASSUMED versus NEEDS-INPUT, which is the destination for every OPEN above.
- **`spec_recovery_reverse_engineering_manifest.md`** — fitness functions (Ford/Parsons/Kua), the
  Git-forensics tradition behind §9.6's process signals, and the standing rule that a green
  structural check is evidence about structure only.
- **`uml25_ocl_conformance_manifest.md`**, **`claude_code_agent_teams_manifest.md`** — out of this
  file's scope; no gate here depends on either.
