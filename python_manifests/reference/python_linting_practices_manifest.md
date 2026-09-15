# Lint Rule Set & Practice Catalogue - Ground-Truth Manifest

**Purpose.** The **lint-and-practise rung** of the enforcement ladder for **small-to-mid-scale,
strictly-typed, single-process Python** built as a functional core inside an imperative shell. It
grounds six decisions: (1) which lint families are enabled, at which pinned version, and how the set
is kept from drifting; (2) how work divides between formatter, linter, type checker, test and
fitness function - including which rules must be **disabled** because another layer owns the defect;
(3) how autofixes may be applied without changing semantics; (4) how suppressions are written,
audited and ratcheted down; (5) what to write at function, module and expression altitude, and which
data shape to reach for; (6) which named anti-patterns are rejected on sight and what actually
catches each. **This file is GROUNDING, not a rulebook: cite a principle when it materially shapes a
decision; reason past it when the situation does not match.** Every practice carries an
**enforcement route** - `type-catchable` (checker + flag), `lint-catchable` (exact code),
`feature-eliminated` (a modern construct removes the class), `test-catchable`, `fitness-function` (a
structural CI check), `contract-only` (nothing mechanical catches it). An unrouted practice is a
defect: a preference dressed as grounding. `contract-only` stated plainly is the honest answer, not
a gap.

**Tag legend.** `ESTABLISHED` = normative and stable in the cited primary source.
`VERSION-DEPENDENT` = bound to the named version; re-verify on upgrade. `OPEN` = no authoritative
source; the project pins it. `CC-FACT` = Claude Code mechanics (none arise here).
`FLAGGED-SECONDARY` inline = the only evidence was secondary. `MEASURED` inline = established by
executing the tool in this environment rather than by reading its documentation, and it **names the
tool version** it is pinned to; for tool behaviour it is strictly stronger than `ESTABLISHED`, and
where page and binary disagreed the measurement wins and the disagreement is stated. One caveat that
this file learned the hard way (§6.1): a measurement only outranks a page when it exercises the
**right surface** - a `ruff check` run says nothing about what `ruff format` warns about, and
reading an absence of output as an absence of the feature is how a correct documentation
claim came to be overridden here by a wrong measurement.

**Deferred to siblings, not repeated.** Versions and support:
`python_platform_baseline_manifest.md`. The hazard diagnosis this file routes:
`python_language_hazards_manifest.md`. The type system, `cast`/`Any` discipline, docstring style
menu: `python_typing_contract_manifest.md`. CI wiring, pre-commit, ratchet mechanism, metrics:
`python_quality_gates_manifest.md`. Layout, the import system as a boundary, public-API contract,
`import-linter`/`Tach`: `python_module_boundaries_manifest.md`. Exception policy:
`error_tracing_contract_manifest.md`. Logging policy: `logging_observability_manifest.md`. Test
kinds: `python_testing_tooling_manifest.md`.

**Version anchor.** Python version, support-phase and PEP-status facts: see
`python_platform_baseline_manifest.md` (verified 2026-08-08). This file owns its tool pins, all
verified 2026-08-08: **ruff 0.16.2** (PyPI dates it 2026-08-07, the CHANGELOG 2026-08-06 - reported,
not resolved), the behaviour-defining release **ruff 0.16.0** (2026-07-23), **pylint 4.0.6**
(2026-06-14) with **astroid 4.0.4**, **mypy 2.3.0**, **flake8 7.3.0** (2025-06-20), **black 26.5.1**
(release date unresolved), **pydoclint 0.9.1** (2026-07-03), **interrogate 1.7.0** (2024-04-07).
pyright was verified from its `main` docs with **no version pinned**; semgrep's version and licence
tier were **not** confirmed. Every code, default and preview flag below is bound to **ruff 0.16.2**
and must be re-verified on any bump: patch releases may include "Bugs are fixed, including behavior
changes that fix bugs" - VERSION-DEPENDENT (ruff 0.16.x).

---

## TL;DR

- **Write `lint.select` explicitly and pin ruff exactly.** ruff 0.16.0 raised the default-enabled
  set from **59 rules to 413** and *removed* 18 codes from it. A project with no explicit `select`
  had its coding standard rewritten by a routine lock-file bump - VERSION-DEPENDENT (ruff 0.16.0).
- **Commit `ruff rule --all --output-format json` as a baseline and diff it on every bump.** 968
  rules exist (830 stable, 138 preview), 413 are on by default, ~49% are autofixable at all -
  MEASURED.
- **`--fix` in CI, `--unsafe-fixes` never unattended.** `RUF015` turns `IndexError` into
  `StopIteration`; `B905` inserts `strict=False` and preserves the bug it flagged; `B006` widens a
  public annotation to `| None` - VERSION-DEPENDENT (ruff 0.16.2).
- **One defect, one owner, one message.** Disable the formatter-owned layout rules; drop `ANN`
  except `ANN401`, which restates nothing mypy `--strict` already reports (§6).
- **`select` replaces, so it must name every family you want - including the boring ones.** A
  `select` written from taste alone switches off default-on families nobody argued about; `ASYNC` is
  the expensive one, because it carries the **only** mechanical check for blocking I/O inside a
  coroutine. §4.3's block is measured to leave no default-on code unaccounted for - MEASURED
  (0.16.2).
- **`target-version` must equal the `requires-python` floor**, never the newest release: ruff
  defines it as the *minimum* and `UP` fixes obey it, so setting it high emits syntax that is a
  `SyntaxError` on the floor you publish. The floor itself is `python_platform_baseline_manifest.md`
  §3e's - ESTABLISHED (ruff 0.16.2).
- **Rules an agent will assume are on but are not:** `G001`-`G004` (f-string/`%`/`.format` inside
  logging calls), `S101` (bare `assert`), `B904` (lost exception cause), `LOG004` (`.exception()`
  outside a handler - stable since 0.16.0 but never added to the default set), `PGH003`/`PGH004`
  (blanket suppressions), every `A00x` builtin-shadowing rule, all `ANN`, all `D` except `D419`,
  `FBT001`/`FBT002`, and every `TC` code except `TC004`/`TC005`/`TC007`/`TC010` - MEASURED.
- **A suppression names a code and a reason - and nothing enforces the reason.** No ruff rule
  requires justification text (searched across all 968 explanations). Codes are enforceable; reasons
  are contract-only plus a project-owned check (§8.4).
- **Roughly a third of the practice catalogue (§11-§16) terminates in `contract-only`.** Read the
  route before assuming a practice is enforced.

---

## 1. The five layers, and the routing vocabulary

A defect class has exactly **one** owning layer. A second layer reporting the same defect is noise,
not defence in depth (§6).

| layer | owns | mechanism | does NOT own |
|---|---|---|---|
| **Formatter** | layout: breaks, indentation, quotes, trailing commas, blank lines | `ruff format`, one `line-length`, `--check` in CI | anything semantic; it has no per-project style debate (§7) |
| **Linter** | single-file AST patterns the type system cannot express; idiom modernisation; suppression hygiene | `ruff check` with an explicit `select`, pinned | cross-file structure, value ranges, arity, attribute existence |
| **Type checker** | shape, arity, attribute existence, override compatibility, re-export, narrowing | mypy `--strict` (13 flags) plus named optional codes; pyright modes | values, timing, state (`python_typing_contract_manifest.md` §4) |
| **Test** | values, sequencing, state, error paths; every route marked `test-catchable` | pytest | structural properties that must hold for all inputs |
| **Fitness function** | cross-file structure: dependency direction, cycles, suppression census, import-time budget | `import-linter`, an `ast`-walking pytest, a `--statistics` ratchet | per-file idiom |

**The routing rule.** A practice is grounded only when it names its layer and its mechanism.
`contract-only` must be *written down* rather than implied; that row then becomes a candidate for
the mechanisation ladder (§10.3).

**The layers measurably differ - MEASURED (ruff 0.16.2 / mypy 2.3.0 / pylint 4.0.6).** On one probe
carrying an incompatible override, a non-existent attribute and a call missing an argument, `ruff
check --select ALL` reported only `ANN001`, `ANN201`, `CPY001`, `D100`-`D103`, `F841` - **none** of
the three real defects. `mypy --strict` reported all three (`[override]`, `[attr-defined]`,
`[call-arg]`) *even on the untyped version*. `pylint` reported the same three (`W0221`, `E1101`,
`E1120`). On a two-module import cycle, mypy printed "Success: no issues found in 3 source files",
ruff said nothing, and only pylint reported `R0401 cyclic-import`. The linter is not a weak type
checker, the type checker is not a strong linter, and one defect class escapes both (§9).

**Scale discipline.** One formatter, one linter with an explicit set, one type checker, one test
runner is the whole toolchain a project this size should carry. A second full linter (§9), a
policy-as-code engine (§10.2) and per-module legacy ratchets (`python_quality_gates_manifest.md`)
are named and then kept off the default path: they pay at larger scale or under specific pressure,
not here.

---

## 2. The rule set is a committed artefact

### 2.1 The 0.16.0 default-set rupture

**VERSION-DEPENDENT (ruff 0.16.0).** Before 0.16.0 the default `select` was effectively `["E4",
"E7", "E9", "F"]` = **59 rules**. From 0.16.0 (2026-07-23) the default is **413 rules**. Astral list
it first among breaking changes and note the default set "was last modified in v0.1.0"; the release
post gives `select = ["E4", "E7", "E9", "F"]` as the way back.

The lesson is not about ruff. **An implicit default set is not a standard.** A project that never
wrote a `select` had its coding standard replaced - 354 rules added, 18 removed - by a dependency
bump containing no code changes. Three binding consequences:

1. **Write `lint.select` explicitly.** The rule set is a reviewed artefact under version control.
2. **Pin the tool exactly.** ruff's versioning policy: a MINOR bump may change the behaviour of a
   stable rule, add stable rules to the default set, or promote a safe fix; a PATCH bump may change
   behaviour to fix bugs. Ruff "does not yet have a stable API" - ESTABLISHED. `ruff>=0.16,<0.17` is
   not a reproducible gate.
3. **Diff the rule inventory on every bump.** `ruff rule --all --output-format json` emits per rule:
   `code`, `name`, `linter`, `summary`, `explanation`, `message_formats`, `fix`, `fix_availability`,
   `preview`, `status`, `source_location` - MEASURED. Commit it; the upgrade diff is the exact delta
   to your standard. `ruff check --show-settings` prints the *resolved* enabled set - the only
   trustworthy answer to "is this rule on?". The gate that runs the diff belongs to
   `python_quality_gates_manifest.md`.

### 2.2 The 18 codes removed from the default set

**VERSION-DEPENDENT (ruff 0.16.0).** Removed as too opinionated: `E401`, `E402`, `E701`, `E702`,
`E703`, `E711`, `E712`, `E713`, `E714`, `E721`, `E731`, `E741`, `E742`, `E743`, `F403`, `F405`,
`F406`, `F722`. Read the list before upgrading: if the codebase relied on `E711`/`E712` (`== None` /
`== True`), `E731` (lambda bound to a name), `E741` (`l`/`O`/`I` as a name) or `F403`/`F405` (star
import and the undefined names it hides), those checks silently left the default. Re-add by exact
code. The `E711`/`E712` fixes are marked **unsafe** - they "may alter runtime behavior when used
with libraries that override `==`/`__eq__`".

### 2.3 `select` replaces; `extend-select` adds

**ESTABLISHED.** `lint.select` **replaces** the default set; `lint.extend-select` **adds** to
whatever is selected. `select = ["E", "F"]` on 0.16.x silently discards ~400 default rules including
every `DTZ` rule, `B006`, `BLE001` and `RUF100`. Resolution: the highest-priority `select` becomes
the basis, then `extend-select` and `ignore` apply; CLI beats `pyproject.toml`, and the current file
beats inherited ones. Prefer `select` **because** it replaces: an explicit total set is a standard;
an additive patch on an unknown base is not.

**MEASURED.** The default set is a list of **individual codes, not prefixes**: from isort only
`I001`; from pydocstyle only `D419`; from flake8-bandit only `S102`, `S110`, `S112`; from
pycodestyle only `E722`, `E902`, `W605`. Reading the Default Rules page's per-linter headings as
"isort, pydocstyle and bandit are on by default" is wrong. Prefix distribution of the 413: `PYI` 47,
`UP` 42, `F` 39, `RUF` 36, `PLE` 33, `B` 29, `SIM` 21, `PLW` 20, `C4` 17, `FURB` 17, `PLR` 13,
`ASYNC` 10, `DTZ` 10, `YTT` 10, `PLC` 8, `PIE` 8, `PT` 6, `LOG` 5, `TRY` 5, `EXE` 4, `G` 4, `TC` 4,
`PERF` 3, `S` 3, `INT` 3, `E` 2, `FA` 2, `PTH` 2, `BLE` 1, `D` 1, `I` 1, `ISC` 1, `N` 1, `PGH` 1,
`RET` 1, `T` 1, `W` 1, `FLY` 1.

### 2.4 Configuration surface, and stating `target-version`

**ESTABLISHED / VERSION-DEPENDENT (ruff 0.16.2).** Config lives in `[tool.ruff]`,
`[tool.ruff.lint]`, `[tool.ruff.format]` in `pyproject.toml`, or in `ruff.toml`/`.ruff.toml` with
the `[tool.ruff]` header dropped. Precedence in one directory: `.ruff.toml` > `ruff.toml` >
`pyproject.toml`. Ruff uses the **closest** config and ignores ancestors unless `extend` is used.
Codes are a one-to-three-letter prefix plus three digits; any prefix is a valid selector; `ALL`
selects everything.

`line-length` defaults to **88**, `target-version` to **`"py310"`**. With a config discovered on the
filesystem, ruff infers a missing `target-version` from `requires-python` in a `pyproject.toml` **in
the same directory as the found config**; a config passed via `--config` is **not** inferred.
`--target-version` accepts `py37`..`py315` - MEASURED. **State it explicitly:** rules whose fixes
depend on the language floor - the `UP` family above all - change behaviour silently when inference
resolves differently than assumed.

**`target-version` is a MINIMUM, and it must equal the `requires-python` floor - not the newest
release.** Ruff's settings page defines it as the version ruff assumes the code targets: "Ruff will
not propose changes using features that are not available in the given version", and it treats
`requires-python = ">=3.8"` as identical to `target-version = "py38"` - ESTABLISHED (ruff 0.16.2).
Setting it *above* the published floor inverts the safety property: `UP` fixes then rewrite code
into syntax the declared floor cannot parse, which is a `SyntaxError` for every user who installs at
that floor, discovered after the wheel is published. Setting it *below* the floor is merely wasteful
- ruff declines modernisations the project could take - and `FA102` is the rule that reports the
mismatch, which it can only do if `target-version` is right in the first place (§3.2). The floor
itself is a policy decision the hub owns - `python_platform_baseline_manifest.md` §3e, whose
recommended default is `requires-python = ">=3.13"`, hence `target-version = "py313"` in §4.3.
Change one and change the other in the same commit: the two values are one fact written twice.

Other defaults, for reading someone else's config: `lint.ignore =
[]`, `lint.extend-select = []`, `lint.per-file-ignores = {}` (a leading `!` negates the pattern),
`lint.fixable = ["ALL"]`, `lint.unfixable = []`, `lint.extend-safe-fixes = []`,
`lint.extend-unsafe-fixes = []`, `lint.external = []`.

### 2.5 Preview mode - a rule you cannot select is a rule you only think you have

**ESTABLISHED / VERSION-DEPENDENT (ruff 0.16.2).** Preview is opt-in via `--preview` or `preview =
true` under `[tool.ruff.lint]`/`[tool.ruff.format]`; resolved defaults are `linter.preview =
disabled`, `formatter.preview = disabled`, `analyze.preview = disabled`,
`linter.explicit_preview_rules = false` - MEASURED. A preview rule **cannot be selected at all**
while preview is off - not by code, not by prefix, not by `ALL` - and *how loudly that fails depends
on how it was selected*. **MEASURED (ruff 0.16.2):** selection by **exact code** prints `warning:
Selection <code> has no effect because preview is not enabled.` - identically for `select`,
`extend-select` and `--select` on the CLI, and for `DOC501`, `PLR0904`, `B909`, `RUF105` and `E111`
alike. It is a warning, not a failure: the run still exits 0, so it survives a green CI step and
dies in log noise. Selection by **prefix** (`select = ["PLR"]`, which contains preview members)
emits **nothing at all** - that case is genuinely silent. Either way `select = ["DOC501"]` with
preview off is a config line an agent will read as "enforced" and be wrong about. Conversely `select
= ["ALL"]` with `preview = true` drags in all 138 preview rules; `lint.explicit-preview-rules =
true` makes
that survivable by restricting prefix selection to stable rules. Promotion is real churn. 0.16.0
stabilised `AIR303`, `CPY001`, `FURB164`, `FURB192`, `ISC004`, `LOG004`, `PLE0304`, `PLR0917`,
`PLR1708`, `RUF036`, `RUF063`, `RUF068`, and widened detection in `BLE001`, `FA102`,
`INT001`-`INT003`, `S310`, `S508`, `S509`, `UP019`. Still preview in 0.16.2: `E111`, `E114`, `E117`,
`DOC201`, `DOC501`, `FURB101`, `RUF105`, `RUF106` - MEASURED. **Stabilisation is a different event
from joining the default set, and the release notes list them under different headings.** Of those
twelve stabilised rules, six are default-on at 0.16.2 (`FURB192`, `ISC004`, `PLE0304`, `PLR1708`,
`RUF063`, `RUF068`) and six are not (`AIR303`, `CPY001`, `FURB164`, `LOG004`, `PLR0917`, `RUF036`) -
MEASURED. "Stabilised" means the rule can now be selected without `preview`; it says nothing about
whether it is selected for you. `LOG004` is the trap here (§4.2). The two rules an agent most wants
for structural review, `PLR0904 too-many-public-methods` and `PLR6301 no-self-use`, are also
preview.
**Stance: `preview = false`.** Where a preview rule is genuinely wanted (`DOC501` is the strongest
candidate - §15.2), enable preview *with* `lint.explicit-preview-rules = true`, name exact codes,
and accept that a bump may rename or re-scope them.

---

## 3. The family map, and a verdict for each family

### 3.1 What ruff consolidated

**MEASURED.** `ruff linter` prints **59 families**; the binary carries **968 rules** (830 stable,
138 preview). A rule's tradition predicts its noise profile: pycodestyle rules are layout-era,
bugbear rules are semantic, tryceratops rules are opinionated about shape.

| prefix | upstream | prefix | upstream | prefix | upstream |
|---|---|---|---|---|---|
| `E`,`W` | pycodestyle | `EM` | flake8-errmsg | `ARG` | flake8-unused-arguments |
| `F` | Pyflakes | `FBT` | flake8-boolean-trap | `PTH` | flake8-use-pathlib |
| `I` | isort | `ISC` | flake8-implicit-str-concat | `ERA` | eradicate |
| `N` | pep8-naming | `ICN` | flake8-import-conventions | `PL` | Pylint |
| `D` | pydocstyle | `G` | flake8-logging-format | `TRY` | tryceratops |
| `DOC` | pydoclint | `LOG` | flake8-logging | `FLY` | flynt |
| `UP` | pyupgrade | `INP` | flake8-no-pep420 | `PERF` | Perflint |
| `ANN` | flake8-annotations | `PIE` | flake8-pie | `FURB` | refurb |
| `ASYNC` | flake8-async | `PT` | flake8-pytest-style | `C90` | mccabe |
| `S` | flake8-bandit | `Q` | flake8-quotes | `PGH` | pygrep-hooks |
| `B` | flake8-bugbear | `RET` | flake8-return | `SLF` | flake8-self |
| `A` | flake8-builtins | `SIM` | flake8-simplify | `BLE` | flake8-blind-except |
| `C4` | flake8-comprehensions | `TID` | flake8-tidy-imports | `COM` | flake8-commas |
| `DTZ` | flake8-datetimez | `TC` | flake8-type-checking | `PYI` | flake8-pyi |
| `T20` | flake8-print | | | `RUF` | Ruff-specific |

Domain families: `AIR` (Airflow), `FAST` (FastAPI), `NPY` (NumPy-specific), `PD` (pandas-vet).
The prefixes left unattributed by an earlier pass carry their upstream in ruff's own rule metadata,
so that OPEN is **resolved - MEASURED (ruff 0.16.2, `ruff rule --all --output-format json`, field
`linter`)**: `YTT` flake8-2020, `CPY` flake8-copyright, `T10` flake8-debugger, `DJ` flake8-django,
`EXE` flake8-executable, `FIX` flake8-fixme, `FA` flake8-future-annotations, `INT` flake8-gettext,
`RSE` flake8-raise, `SLOT` flake8-slots, `TD` flake8-todos.

### 3.2 Per-family verdict for a small strictly-typed project

A judgement built on the verified facts, not a measurement (see Honest limits, §16). "Contested"
means the family generates substantial noise on ordinary correct code and the project must record a
decision.

| family | verdict | reason |
|---|---|---|
| `F` | **enable** | undefined names, unused imports and variables - the irreducible core |
| `E`,`W` | **enable-with-exceptions** | keep the semantic members (`E722`, `E902`, `W605`); the layout members are formatter-owned (§6.1) |
| `I` | **enable** | `I001` is default-on with a fix; import order is a pure merge-conflict tax |
| `UP` | **enable** | one typing vocabulary per codebase; requires an explicit `target-version` |
| `B` | **enable** | highest semantic yield per rule: `B006`, `B008`, `B019`, `B023`, `B905` |
| `C4` | **enable** | removes needless materialisation; mostly autofixable |
| `SIM` | **enable-with-exceptions** | real simplification value, but `SIM108`'s own page calls it "an opinionated style rule" |
| `DTZ` | **enable** | all ten default-on; naive datetimes are invisible to the type system (§4.1) |
| `G` | **enable** | the four rules that matter (`G001`-`G004`) are **off by default** (§4.2) |
| `LOG` | **enable** (by prefix) | root-logger calls, hand-built `Logger`, `exc_info=` outside a handler; the `.exception()`-outside-a-handler check is `LOG004`, which is stable but **off by default** - the prefix is what picks it up (§4.2) |
| `TRY` | **enable-with-exceptions, partly contested** | take `TRY002`/`TRY004`/`TRY201`/`TRY203`/`TRY400`/`TRY401`; `TRY003`/`TRY300`/`TRY301` are contested |
| `BLE` | **enable** | `BLE001` default-on; the process boundary needs one coded suppression, not a global disable |
| `S` | **enable-with-exceptions** | exempt `S101` for the test tree via `per-file-ignores`, never globally |
| `PGH` | **enable** | `PGH003`/`PGH004` are the blanket-suppression detectors, both off by default (§8.2) |
| `RUF` | **enable** | carries the suppression-hygiene family plus `RUF012`/`RUF022` |
| `PT` | **enable** (test tree) | fixture and `raises` shape; the practice is `python_testing_tooling_manifest.md`'s |
| `T20` | **enable** | `T201`/`T203` off by default; CLI entry points get a scoped `per-file-ignores` |
| `PTH` | **enable-with-exceptions** | ignore `PTH123`: its own page concedes a performance cost and the fix is unsafe when it drops comments |
| `FLY` | **enable** | flynt's f-string conversion; one rule is default-on. The individual codes were not verified this session - check with `ruff rule` |
| `PERF` | **enable-with-exceptions** | mostly taste at this scale; `PERF401` is off by default |
| `N` | **enable** | only `N999` is default-on; the mechanical half of §12.4 |
| `A` | **enable** | **no `A` rule is default-on**; builtin shadowing is real and silent |
| `ICN`,`INP`,`PIE`,`RSE`,`SLF`,`TID` | **enable** | small and low-noise; `TID251` is the one project-specific rule engine ruff has (§10.1) |
| `PYI` | **enable** | 47 rules default-on; free unless the project ships `.pyi`, where it is the standard |
| `ASYNC` | **enable** | the highest-stakes omission a hand-written `select` makes. 15 stable rules, **10 default-on** - MEASURED. `ASYNC210`/`ASYNC230`/`ASYNC251` (blocking HTTP, blocking `open`, `time.sleep`) plus non-default `ASYNC212`/`ASYNC240`/`ASYNC250` are the **only mechanical check for blocking I/O inside a coroutine**; nothing in `python_concurrency_determinism_manifest.md` is enforced without them |
| `FURB` | **enable** | 22 stable rules, **17 default-on** - MEASURED. `FURB162`, `FURB168`, `FURB169`, `FURB188` are semantic; the five stable non-default members (`FURB110`, `FURB116`, `FURB164`, `FURB171`, `FURB187`) are modernisation taste and are the first candidates for `ignore` if they prove noisy |
| `YTT` | **enable** | all **10 default-on** - MEASURED. `sys.version` slicing and `sys.version_info` comparisons that break on a two-digit minor: pure correctness, zero style |
| `EXE` | **enable** | 5 stable, **4 default-on** - MEASURED; shebang/executable-bit mismatches. Free, and the one family a Windows-developed repo gets wrong |
| `INT` | **enable** | all **3 default-on** - MEASURED; gettext calls whose message is f-string-formatted before translation. Inert unless the project uses gettext, so keeping it costs nothing and losing it costs a silent regression if gettext arrives later |
| `FA` | **enable** | both **default-on** - MEASURED. `FA` is the family that binds annotations to `target-version`: `FA102` reports an annotation that needs a newer Python than the declared floor - the static form of the `SyntaxError`-on-your-own-floor failure - and it can only do that if `target-version` equals the floor (§2.4) |
| `RET` | **enable-with-exceptions** | 8 stable, **only `RET501` default-on** - MEASURED, so the prefix is a deliberate widening. Take `RET501`-`RET503` (`RET503 implicit-return` is the one §11.4 routes); `ignore` `RET504` and the `RET505`-`RET508` superfluous-else set - contested early-return style |
| `T10` | **enable** | `T100 debugger` (flake8-debugger) is **default-on and the whole family** - MEASURED. A committed `breakpoint()` hangs CI; no other layer sees it |
| `D` | **enable-with-configuration** | `lint.pydocstyle.convention` **must** be set; `null` is not neutral (§6.3) |
| `PL` | **enable-with-configuration** | every threshold is a project decision; `PLR0913` is off by default |
| `C90` | **enable-with-configuration** | `C901` is off by default; the threshold is a coordination device (§11.1) |
| `TC` | **enable-with-configuration** | `TC001`-`TC003` plus autofix can break pydantic/attrs at runtime unless the exemption lists are filled (§5.2) |
| `ANN` | **reject except `ANN401`** | `ANN001`/`ANN201` duplicate mypy `--disallow-untyped-defs` (§6.2) |
| `Q`,`COM` | **reject** | formatter-owned: quotes and trailing commas (§6.1) |
| `ISC` | **enable the prefix, `ignore` `ISC002` and `ISC003`** | one position, taken once - the file previously said three different things. `ISC001` is **not** on ruff's formatter-conflict list; `ISC002` is, *and only when `ISC001` is off* - so selecting `ISC001` is what makes the pair formatter-safe, and `ISC002` is then redundant (§6.1). `ISC003` flags ordinary explicit `+` concatenation. Only `ISC004` is default-on - MEASURED |
| `EM` | **contested** | `EM101`/`EM102`/`EM103` push every message into an exception class; many teams reject the ceremony |
| `ERA` | **contested** | `ERA001` has the highest false-positive rate in the set - it fires on prose that happens to parse |
| `ARG` | **contested** | interface stubs and callbacks legitimately ignore arguments; tune `lint.dummy-variable-rgx` first |
| `FBT` | **contested, recommended - so §4.3 selects it** | `FBT001`-`FBT003` catch a design defect the checker cannot see (§11.3); none is default-on and none has a fix - MEASURED. `FBT001`/`FBT002` are yours to fix, so they are selected; `FBT003` fires at call sites into third-party APIs you cannot change, so it is in `ignore`. A verdict of "recommended" that the shipped config does not implement is not a decision |
| `DOC` | **preview - opt in deliberately** | `DOC201`/`DOC501` are the only mechanical enforcement of a documented `Raises:`/`Returns:` (§15.2) |
| `AIR`,`FAST`,`NPY`,`PD`,`DJ` | **reject** unless the framework is a dependency | dead configuration otherwise |
| `CPY`,`FIX`,`TD` | **project decision** | copyright headers and TODO hygiene; `lint.task-tags` defaults to `["TODO", "FIXME", "XXX"]` |

**Stale configuration is loud, not silent - and the failure modes differ.** **MEASURED (ruff
0.16.2).** `TRY200`, `PGH001` and `PGH002` are **redirects**, not dead codes: selecting one prints
`warning: TRY200 has been remapped to B904.` (likewise `PGH001` -> `S307`, `PGH002` -> `G010`) **and
enables the successor rule** - `--select TRY200` really does report `B904` findings - so the config
is not inert either; it enforces a rule the config file never names. `PT004` was **fully removed**
and ruff refuses to run: `ruff failed / Cause: Rule PT004 was removed and cannot be selected.` A
selector that never existed fails the same hard way (`Cause: Unknown rule selector D216 in select
from the CLI`, §6.3). So a stale `select` either warns or aborts; the genuinely silent case is not a
removed code at all but a *preview* code pulled in by prefix (§2.5). `RUF101`/`RUF102` catch stale
codes inside `noqa` comments but nothing checks the config file. Audit `select` against the
committed `ruff rule --all` baseline (§2.1).

---

## 4. The high-value subset: rules that catch what a type checker cannot

`python_typing_contract_manifest.md` §4 establishes what the type system cannot express - value
ranges, cross-field invariants, ordering and temporal constraints, units, typestate. This section is
the other side of that boundary: hazards in the blind spot for which an exact code exists.
`python_language_hazards_manifest.md` owns the diagnosis; the codes are here because a config file
needs them.

### 4.1 Already on by default - do not re-add, do not lose

**MEASURED (ruff 0.16.2).** `select = ["E", "F"]` throws all of this away (§2.3).

| code | name | fix | what the checker cannot see |
|---|---|---|---|
| `B006` | mutable-argument-default | Sometimes (**unsafe**) | a well-typed `list[int]` default that is one object shared by every call |
| `B008` | function-call-in-default-argument | none | one frozen value for the process lifetime |
| `B023` | function-uses-loop-variable | none | every closure resolving to the final loop value |
| `E722` | bare-except | none | `except:` swallowing `KeyboardInterrupt`/`SystemExit` |
| `BLE001` | blind-except | none | `except Exception:` used as control flow |
| `S110`,`S112` | try-except-pass, try-except-continue | none | a failure that leaves no trace |
| `S102` | exec-builtin | none | arbitrary code execution |
| `DTZ001`-`DTZ007`, `DTZ011`, `DTZ012`, `DTZ901` | the naive-datetime family (all ten) | none | a naive `datetime` is perfectly typed and silently wrong across zones and DST |
| `TRY002`,`TRY004`,`TRY201`,`TRY203`,`TRY401` | vanilla raise, type-check without TypeError, verbose raise, useless try-except, verbose log message | `TRY201` Always | handler shapes the checker has no opinion about |
| `LOG001`,`LOG002`,`LOG009`,`LOG014`,`LOG015` | direct-logger-instantiation, invalid-get-logger-argument, undocumented-warn, exc-info-outside-except-handler, root-logger-call | Sometimes (all but `LOG015`) | `exc_info=True` outside a handler attaches `None`; a module-level `logging.info()` configures the root logger as a side effect. **These five are the whole default-on `LOG` set** - matching the measured `LOG` 5 in §2.3; `LOG004` is *not* among them (§4.2) |
| `G010`,`G101`,`G201`,`G202` | logging-warn, extra-attr-clash, exc-info misuse | `G010` Always | an `extra=` key colliding with a `LogRecord` attribute raises at log time, in production, on the error path |
| `I001` | unsorted-imports | Sometimes | merge-conflict surface |
| `RUF100`,`RUF101` | unused-noqa, redirected-noqa | Always | suppression debt (§8) |
| `TC004`,`TC005`,`TC007`,`TC010` | runtime-import-in-type-checking-block and siblings | - | a `TYPE_CHECKING` import that is needed at runtime |
| `RUF028` | invalid-formatter-suppression-comment | Always | a `# fmt:` comment that does nothing |

### 4.2 Off by default - and an agent will assume otherwise

**MEASURED (ruff 0.16.2), each verified individually as absent from the 413.** The most useful list
here for writing a `select`.

| code | name | why it matters / note |
|---|---|---|
| `G001`,`G002`,`G003`,`G004` | logging-string-format, logging-percent-format, logging-string-concat, logging-f-string | eager formatting even when the level is disabled, and the structured-logging message key is destroyed. **The four highest-value logging rules are all off.** `G004`'s fix is Sometimes-available and rewrites the call - read the diff. Policy: `logging_observability_manifest.md` |
| `LOG004` | log-exception-outside-except-handler | `.exception()` outside a handler attaches `None` as the exception info and logs `NoneType: None`. **Stabilised in 0.16.0 - which is not the same fact as being added to the default set.** MEASURED (0.16.2): stable, no preview badge, and **absent from the 413**, so `--select LOG` or the exact code is required to get it. `logging_observability_manifest.md` routes "exception logging belongs inside an `except` handler" to this code, so silently losing it breaks that route. Fix is Sometimes-available. `LOG007 exception-without-exc-info` is off by default on the same footing - MEASURED: the whole `LOG` family is seven codes and only five are default-on |
| `S101` | assert | `assert` vanishes under `python -O`. Exempt the **test tree** via `per-file-ignores`; a global `ignore` re-permits assert-as-validation in production |
| `B904` | raise-without-from-inside-except | the traceback loses the original cause; no autofix, and nothing detects a *wrong* `from` target |
| `B905` | zip-without-explicit-strict | silent data loss; **the fix inserts `strict=False` and preserves the bug** (§5.2) |
| `PGH003`,`PGH004` | blanket-type-ignore, blanket-noqa | a blanket suppression hides every present *and future* diagnostic; `PGH004`'s message is "Use specific rule codes when using `noqa`" |
| `A001`-`A006` | builtin shadowing (variable, argument, attribute, import, lambda arg) and `A005` stdlib-module-shadowing | `list`/`id`/`type`/`input` shadowed locally, or a local `json.py`; no `A` rule appears in the measured default distribution |
| all `ANN*` | annotation rules | keep `ANN401` only (§6.2) |
| all `D*` except `D419` | docstring rules | `D419 empty-docstring` is the only default-on `D` rule (§15) |
| `TRY300`,`TRY301`,`TRY400` | try-consider-else, raise-within-try, error-instead-of-exception | `TRY400` recovers a lost traceback; its fix is safe for `logging.error` and unsafe for anything ruff cannot prove is a `logging.Logger` - set `lint.logger-objects`, which §4.3 spells out with its `[]` default visible rather than leaving it to prose. `TRY300`/`TRY301` are contested and noisy, so §4.3 selects `TRY` by prefix and puts those two in `ignore`: a recorded rejection, not an accident |
| `TC001`-`TC003` | typing-only import families | dangerous with autofix (§5.2) |
| `C901`,`PLR0913` | complex-structure, too-many-arguments | thresholds default to 10 and 5 (§11.1) |
| `T201`,`T203` | print, p-print | `print()` bypassing the logging contract |
| `FBT001`,`FBT002` | boolean type hint / default in positional position | the boolean trap (§11.3) |
| `RUF102`,`RUF103`,`RUF104` | invalid-rule-code, invalid-suppression-comment, unmatched-suppression-comment | adopting `# ruff: disable[...]` blocks **obliges** selecting `RUF103`+`RUF104` in the same commit (§8.2) |
| `EM101`,`ERA001`,`RET504`,`PERF401`,`ARG001`,`PTH123`,`N802`,`SIM105` | see §3.2 | contested or taste |
| `E501`,`COM812`,`Q000` | line length, trailing comma, quotes | formatter-owned; that they are off is correct, not an oversight (§6.1). `ISC001` is **not** in this group - it is absent from ruff's formatter-conflict list, and §4.3 selects it precisely so that `ISC002` cannot conflict (§3.2) |

### 4.3 The rule set as a config block

```toml
[tool.ruff]
line-length = 88
target-version = "py313"          # MUST equal the requires-python floor (hub §3e), never the newest
                                  # release: it is a MINIMUM, and `UP` fixes obey it (§2.4)

[tool.ruff.lint]
select = [
  "F", "E", "W", "I", "UP", "B", "C4", "SIM", "DTZ", "G", "LOG", "TRY", "BLE", "S",
  "PGH", "RUF", "PT", "T20", "PTH", "FLY", "PERF", "N", "A",
  "ICN", "INP", "PIE", "RSE", "SLF", "TID", "PYI",
  "ASYNC", "FURB", "YTT", "EXE", "INT", "FA", "RET", "ISC", "T10",   # default-on families that
                                  # `select` would otherwise switch OFF - it replaces (§2.3, §3.2)
  "FBT",                          # contested-but-recommended; the boolean trap (§11.3)
  "D", "PL", "C90",               # each configured below
  "TC004", "TC005", "TC007", "TC010",   # the four default-on TC codes; TC001-TC003 only after the
                                  # runtime-evaluated-* lists below are filled (§5.2)
  "ANN401",                       # the one ANN rule that is not the checker's job
]
ignore = [
  "W191", "E111", "E114", "E117", "D206", "D300", "D203",
  "Q000", "Q001", "Q002", "Q003", "Q004", "COM812", "COM819",
  "E501",                         # line length is the formatter's (§6.1)
  "PTH123",                       # taste, and the fix drops comments
  "ISC002", "ISC003",             # ISC002 is formatter-adjacent, and safe only because ISC001 stays
                                  # on; ISC003 flags ordinary explicit `+` concatenation (§6.1)
  "FBT003",                       # fires at call sites into third-party APIs you cannot change
  "RET504",                       # a named intermediate is often the documentation
  "RET505", "RET506", "RET507", "RET508",   # superfluous-else: early-return style, contested
  "TRY300", "TRY301",             # contested and noisy - flip these deliberately, not by prefix
]
logger-objects = []               # name project logger wrappers here before trusting TRY400's fix,
                                  # which is unsafe on any receiver ruff cannot prove is a Logger
preview = false

[tool.ruff.lint.per-file-ignores]
"tests/**" = ["S101", "PLR2004", "D103"]
"**/__main__.py" = ["T201"]

[tool.ruff.lint.pydocstyle]
convention = "google"             # NEVER leave at null (§6.3)

[tool.ruff.lint.mccabe]
max-complexity = 10

[tool.ruff.lint.pylint]
max-args = 5
max-positional-args = 5

[tool.ruff.lint.flake8-type-checking]
runtime-evaluated-base-classes = []   # fill before enabling TC001-TC003 (§5.2)
runtime-evaluated-decorators = []

[tool.ruff.lint.flake8-tidy-imports.banned-api]
"datetime.datetime.utcnow".msg = "Use datetime.now(tz=UTC) instead."

[tool.ruff.format]
quote-style = "double"
```

Every default asserted there is documented or MEASURED at ruff 0.16.2: `line-length` 88,
`mccabe.max-complexity` 10, `pylint.max-args` 5, `pylint.max-positional-args` 5,
`pydocstyle.convention` `null`, `flake8-type-checking.runtime-evaluated-base-classes` and
`runtime-evaluated-decorators` `[]`, `formatter.quote_style` `double`,
`formatter.docstring_code_format` `disabled`, `lint.logger-objects` `[]`,
`lint.flake8-bandit.check-typed-exception` `false`, `lint.dummy-variable-rgx`
`"^(_+|(_+[a-zA-Z0-9_]*[a-zA-Z0-9]+?))$"`. The `TID251` block is the exact configuration verified
working in §10.1.

**The block is MEASURED as a whole, not drafted - MEASURED (ruff 0.16.2).** Written to a
`pyproject.toml` and resolved with `ruff check --show-settings`, it loads with **no unknown-selector
abort, no "has no effect because preview is not enabled" warning, and no formatter-conflict warning
from `ruff format --check`**. It resolves to **708 enabled rules**, and the diff against the 413
defaults is empty in the dangerous direction: **every default-on code is either selected or named in
`ignore` with a reason.** That property, not the length of the list, is what makes it a standard -
`select` **replaces** (§2.3), so any family a hand-written `select` forgets is a family the project
silently turned off. Re-run that diff after every edit to the block and on every ruff bump (§2.1).

---

## 5. Fix safety is a semantics contract, not a convenience

### 5.1 The split

**ESTABLISHED (ruff's own definition) / VERSION-DEPENDENT (0.16.2).** A **safe** fix means "The
meaning and intent of your code will be retained", and safe fixes "will only remove comments when
deleting entire statements or expressions". An **unsafe** fix "could lead to a change in runtime
behavior, the removal of comments, or both". Only safe fixes apply by default: resolved settings
show `unsafe_fixes = hint`, i.e. ruff *reports* a hidden fix and will not apply it - MEASURED.
Flags: `--fix`/`--no-fix`, `--unsafe-fixes`/`--no-unsafe-fixes`, `--fix-only`, `--diff` (implies
`--fix-only`, writes nothing, exits 0 when there are no diffs), `--show-fixes`; config
`unsafe-fixes`. Per-rule re-grading is `lint.extend-safe-fixes` / `lint.extend-unsafe-fixes`, both
accepting prefixes - so **"safe" is a per-repository claim**. Read the repo config; never trust a
grading from memory.

**Fix availability across the 968 rules: 494 none, 251 always, 223 sometimes** - MEASURED. Under
half the set is autofixable at all; among the 413 defaults it is 198 / 116 / 99. **Most of a
linter's value is diagnosis, not repair.** And gradings move: in 0.16.1 alone `PT022` and `FURB105`
fixes became unsafe and `PT018` became safe by default (unsafe only with comments present) -
VERSION-DEPENDENT (0.16.1). An unpinned ruff is an unpinned definition of "safe to autofix".

### 5.2 The five autofixes that change meaning while looking harmless

| rule | the fix | the semantic change |
|---|---|---|
| `RUF015` | `list(xs)[0]` -> `next(iter(xs))` | empty input raises `StopIteration`, not `IndexError`. MEASURED: plain `--fix` leaves the file alone and prints `No fixes available (1 hidden fix can be enabled with the --unsafe-fixes option).`; `--unsafe-fixes --fix` rewrites it. Any upstream `except IndexError:` stops working |
| `B905` | inserts `strict=False` | the rule exists because silent truncation loses data; the fix **satisfies the rule and keeps the bug**. Its page admits it "can obscure situations where the iterables are of unequal length". Insert `strict=True` by hand |
| `B006` | `def f(x: list[int] = [])` -> `None` default plus in-body init | changes the **public annotation** from `list[int]` to `list[int] \| None`. Under `--unsafe-fixes` an agent can widen a dozen APIs in one pass |
| `TC001`-`TC003` | moves imports into `TYPE_CHECKING` | breaks any class whose annotations are introspected at runtime (pydantic, attrs). Both exemption lists default to `[]`, so protection is **off until configured**; `TC004` notices only *after* the fix lands |
| `TRY400` | `logging.error` -> `logging.exception` | safe for `logging.error`, **unsafe for other logger-like receivers**, because ruff cannot prove the receiver is a `logging.Logger`. Set `lint.logger-objects` |

`E711`/`E712` belong on the same list (§2.2).

### 5.3 Fix policy

**OPEN - house convention, built on the verified mechanics of §5.1-§5.2. Record it once and enforce
it.**

1. **`--fix` (safe only) may run in a hook and in CI**; a hook that fixes must fail the run
   (`--exit-non-zero-on-fix`; wiring is `python_quality_gates_manifest.md`'s).
2. **`--unsafe-fixes` is a human, interactive operation**, one rule family at a time, `--diff`
   first, diff read line by line. Never in a hook, never unattended, never tree-wide.
3. **Re-run the type checker and the tests after any autofix pass.** `B006` and `TC001`-`TC003`
   change what the checker sees; `RUF015` and `B905` change what the tests would have caught.
4. **A safe fix still deletes comments** when it deletes the statement they attach to. Review the
   diff, not the exit code.

---

## 6. Rules that must be disabled because another layer owns the defect

### 6.1 Formatter-owned - and ruff warns about only two of them

**VERSION-DEPENDENT (ruff 0.16.2).** The formatter docs name these lint rules as conflicting:
`W191`, `E111`, `E114`, `E117`, `D206`, `D300`, `D203`, `Q000`-`Q004`, `COM812`, `COM819`, plus
`ISC002` in the stated configuration; `E501` appears on the same list with the caveat that the
formatter "only makes a best-effort attempt to wrap lines at the configured line-length". Two
verification passes read that page differently on `E501` - one unconditional, one conditional.
**Boundary call taken here: leave `E501` off.** A finding the formatter deliberately declines to fix
(a long URL inside a string) is a permanent, unactionable diagnostic. Set `line-length` once, in
`[tool.ruff]`. Five isort settings also conflict at non-default values: `force-single-line`,
`force-wrap-aliases`, `lines-after-imports`, `lines-between-types`, `split-on-trailing-comma`.

**MEASURED (ruff 0.16.2) - the guard rail exists, but it is partial and it lives in the wrong
subcommand.** With `select = ["D203", "ISC001", "COM812", "E501", "W191", "Q000"]`, `ruff format`
and `ruff format --check` print `warning: The following rules may cause conflicts when used with the
formatter: COM812, D203. To avoid unexpected behavior, we recommend disabling these rules, either by
removing them from the lint.select or lint.extend-select configuration, or adding them to the
lint.ignore configuration.` - which is the docs' promise that "When an incompatible lint rule or
setting is enabled, `ruff format` will emit a warning" - ESTABLISHED. But it fires for only **two**
of the fifteen conflicting codes that page bullets: `W191`, `D206`, `D300`, `Q000`-`Q004`, `COM819`
and `ISC002` produce nothing at all - nor does `E501`, which the page names separately with the
best-effort caveat - and `E111`/`E114`/`E117` cannot be selected outside preview anyway (§2.5). Two
*settings* also warn - `isort.lines-after-imports` at a value other than `-1`/`1`/`2`,
and `flake8-implicit-str-concat.allow-multiline = false` without `ISC001` - and no other isort
setting on the list does. **`ruff check` with the identical config prints nothing**, so a lint-only
CI step never sees the warning; run `ruff format --check` in the same job if the warning is to be
seen at all. An earlier pass in this file recorded "the guard rail does not exist" and overrode a
fact pack that had the docs right; that measurement was taken from `ruff check` and is
**withdrawn**. Ruff does separately warn, from `check`, about *mutually* incompatible lint rules
(`D203`/`D211`, `D212`/`D213`).

**MEASURED - `D203` versus the formatter is a genuine non-terminating loop.** With `--select D203
--fix`, a class whose docstring immediately follows the `class` line gains a blank line; `ruff
format` removes it; forever. `D203`'s fix is "always available", so two subcommands of the same
binary undo each other - and only `ruff format` names the conflict; `ruff check --fix`, the
subcommand that opens the loop, says nothing. `D203`'s own page: "We recommend against using this
rule alongside the formatter."

### 6.2 Type-checker-owned

**VERSION-DEPENDENT (mypy 2.3.0).** `ANN001` and `ANN201` report exactly what mypy
`--disallow-untyped-defs` and `--disallow-incomplete-defs` report - both inside `--strict`. Running
both means every missing annotation is two findings in two vocabularies with two suppression
syntaxes. **Keep `ANN401 any-type` and drop the rest of `ANN`:** it flags `Any` on *arguments*,
which mypy `--strict` alone permits. The blunter checker-side alternative is
`--disallow-any-explicit`; pick one. `SLF001` versus pyright strict's `reportPrivateUsage` is the
same overlap in the other direction - pick the linter rule, which runs regardless of checker
configuration.

`--strict` is a fixed set of thirteen named flags, of which `--disallow-untyped-defs`,
`--disallow-incomplete-defs`, `--warn-unused-ignores`, `--warn-redundant-casts` and
`--no-implicit-reexport` are the ones this file's overlap arguments turn on - ESTABLISHED (mypy
2.3.0). The full list and all checker configuration are `python_typing_contract_manifest.md`'s.

### 6.3 `lint.pydocstyle.convention` defaults to `null`, and `null` is not neutral

**VERSION-DEPENDENT (ruff 0.16.2).** Allowed: `"google"`, `"numpy"`, `"pep257"`; default **`null`**.
**MEASURED:** `--select D` with no convention prints `warning: 'incorrect-blank-line-before-class'
(D203) and 'no-blank-line-before-class' (D211) are incompatible. Ignoring
'incorrect-blank-line-before-class'.` plus the equivalent for `D212`/`D213`. Left at `null`, ruff
silently picks a winner for you. The mechanism is **subtractive**: a convention *disables* the `D`
rules that contradict it rather than adding checks - and the three lists are not variations on one
theme. **MEASURED (ruff 0.16.2)**,
by resolving `select = ["D"]` under each convention with `ruff check --show-settings` and diffing
against the **46 stable `D` codes** (48 exist; `D420` and `D421` are preview):

| convention | codes it disables | stable `D` rules left enabled |
|---|---|---|
| `"google"` | `D203`, `D204`, `D213`, `D215`, `D400`, `D401`, `D404`, `D406`, `D407`, `D408`, `D409`, `D413` | 34 |
| `"numpy"` | `D107`, `D203`, `D212`, `D213`, `D402`, `D413`, `D415`, `D416`, `D417` | 37 |
| `"pep257"` | `D203`, `D212`, `D213`, `D214`, `D215`, `D404`, `D405`, `D406`, `D407`, `D408`, `D409`, `D410`, `D411`, `D413`, `D415`, `D416`, `D417` - plus preview `D420`, visible only under `preview = true` | 29 |

Three consequences an inherited disable list will get wrong. **`"google"` and `"pep257"` are not the
same list**: `"google"` drops `D400`/`D401` (the "first line ends in a period / is in imperative
mood" pair) and keeps `D212`, `D415`, `D416`, `D417`, while `"pep257"` does the reverse.
**`"pep257"` subtracts the most, not the least** - 17 of 46, leaving the fewest `D` rules running of
the three - and `"numpy"` is the only convention that drops `D107` (`__init__` docstring). And
**there is no `D216`.** A stale list naming it does not degrade quietly: ruff aborts with `ruff
failed / Cause: Unknown rule selector D216 in select from <config path>` - MEASURED (0.16.2), the
same hard stop a fully removed code gives (§3.2). Only `D203` and `D213` are disabled under all
three conventions, and ruff drops those two anyway when no convention is set, by resolving the
`D203`/`D211` and `D212`/`D213` conflicts itself. So `select = ["D"]` with `convention = "..."` is
the correct spelling, and re-adding one of those codes via `extend-select` re-enables exactly the
rule the convention was chosen to silence.

**A reported internal inconsistency, not smoothed over:** `ruff rule D211` names the rule
`blank-line-before-class` while the warning text spells it `no-blank-line-before-class` - MEASURED.
Treat `ruff rule` output as canonical.

---

## 7. Formatting is not negotiable and is not a code-review topic

**VERSION-DEPENDENT (ruff 0.16.2 / black 26.5.1).** `ruff format` is documented as "designed as a
drop-in replacement for Black", adhering to Black's stable style, with Astral's own measurement that
"> 99.9% of lines are formatted identically" over Black-formatted Django and Zulip - a vendor claim
about two codebases, not an independent audit, and **the docs name no target Black version**, so the
compatibility claim cannot be pinned to a Black release. Documented deviations: ruff formats
expressions inside f-string `{...}` braces, and a preview "fluent layout" for method chains. Black
26.5.1 requires Python 3.10+, has a written Stability Policy and a year-named stable style (2026 in
26.1.0, 2025 in 25.1.0), and states "you should not expect large formatting changes in the future".

**Pinned choice: `ruff format`** - same binary, same config file as the linter, one fewer pin and
one fewer version-skew failure mode. `line-length = 88`. Resolved defaults: `indent_style = space`,
`quote_style = double`, `nested_string_quote_style = alternating`, `docstring_code_format =
disabled`, `docstring_code_line_width = dynamic` - MEASURED. Suppression is `# fmt: off`/`# fmt:
on`/`# fmt: skip`, and `RUF028` (default-on) flags a malformed one.

**Three authorities give three line lengths** - PEP 8 says **79** for code (72 for comments and
docstrings, 99 permitted by explicit team decision), the Google guide says **80**, ruff defaults to
**88** - ESTABLISHED (the conflict) / VERSION-DEPENDENT (the 88). Only the tool enforces, so the
tool's number is the real one. The argument for 88 is coordination, not correctness. **A claim that
a codebase is "PEP 8 compliant" is unverifiable in general; what is verifiable is that it passes a
named rule set at a named version.** Two operational notes, both VERSION-DEPENDENT (ruff 0.16.0).
`check` and `format --check` now show fixes as diffs by default, and the same release made ruff's
JSON `filename`, `location`, `end_location` and `fix.edits[].location` **nullable** - any CI script
parsing ruff JSON must be re-tested. And `ruff format` now formats Python code blocks inside
Markdown by default (info strings `python`, `py`, `python3`, `py3`, `pyi`, `pycon`), suppressible
with `<!-- fmt: off -->` / `<!-- fmt: on -->`: a repo whose docs contain deliberately-broken example
code will find it silently corrected.

---

## 8. Suppression hygiene as a contract

A suppression is an amendment to the standard, written by one person, at one line, forever. It
**names a code** and it **states a reason**. The first half is mechanically enforceable; the second
is not, and this section says so.

### 8.1 Every suppression channel

**VERSION-DEPENDENT (ruff 0.16.0 introduced the native forms; 0.16.2 verified).**

| scope | syntax | notes |
|---|---|---|
| line, legacy | `# noqa` / `# noqa: F401` | the bare form suppresses **everything** on the line; ruff also honours flake8's `# flake8: noqa` |
| line, native | `# ruff: ignore[F401]` at end of line **or** on the preceding line, optionally with free text: `# ruff: ignore[F401] Allow unused imports` | MEASURED: an unused `import re` carrying it produced no `F401`; can suppress a diagnostic spanning a whole logical line |
| range | `# ruff: disable[N803]` ... `# ruff: enable[N803]`, own-line comments | codes, order and indentation must match; an unterminated `disable` runs to the end of the enclosing scope - at module level, the rest of the file |
| file | `# ruff: noqa`, `# ruff: noqa: F841`, `# ruff: file-ignore[F401] <reason>` | valid from anywhere in the file; the bare form disables **everything** and is easy to leave behind after debugging |
| type checker | `# type: ignore[code]`, `# pyright: ignore[rule]` | §8.3 |
| pylint (if present) | `# pylint: disable=<name>` | a fourth vocabulary (§9) |

**ESTABLISHED (MEASURED).** `noqa` matching is **per-code and non-transitive**: `import io # noqa:
E501` does **not** suppress `F401` on that line. An agent appending a code to an existing `noqa`
must append the *right* one. `--add-noqa[=<REASON>]` and `--add-ignore[=<REASON>]` bulk-insert
suppressions and optionally append free text; under `--preview`, `--add-ignore` writes rule *names*
rather than codes.

**Ruff is steering away from `noqa`.** Two preview rules encode the end state: `RUF105
noqa-comments` ("`noqa` comment used instead of `ruff: ignore`", fix Sometimes) and `RUF106
rule-codes-in-suppression-comments` ("Rule code used instead of name in suppression comment", fix
Always), both preview since 0.15.22 - MEASURED. **Recommendation:** standardise on `# ruff:
ignore[CODE] <reason>` now. It is the form ruff is moving toward, it carries a reason slot natively,
and it keeps the eventual migration to rule names mechanical.

### 8.2 The hygiene rule family - only three are default-on

**MEASURED (ruff 0.16.2).**

| code | name | fix | default | catches |
|---|---|---|---|---|
| `RUF100` | unused-noqa | Always | **on** | a suppression that no longer suppresses anything |
| `RUF101` | redirected-noqa | Always | **on** | a `noqa` naming a renamed/redirected code |
| `RUF028` | invalid-formatter-suppression-comment | Always | **on** | a malformed `# fmt:` comment |
| `RUF102` | invalid-rule-code | Always | off | a `noqa` naming a code that does not exist |
| `RUF103` | invalid-suppression-comment | Always | off | a malformed `# ruff: disable[...]`/`enable[...]` |
| `RUF104` | unmatched-suppression-comment | none | off | an unterminated range suppression |
| `PGH003` | blanket-type-ignore | none | off | `# type: ignore` with no code |
| `PGH004` | blanket-noqa | Sometimes | off | bare `# noqa` |

**Adopt `# ruff: disable[...]` blocks and you must select `RUF103` + `RUF104` in the same commit.**
Neither is default-on, and `RUF104`'s page describes the failure: an unmatched range can
"inadvertently suppress violations over larger sections of code than intended, particularly at
module scope".

**`RUF100` reports two distinguishable states and the wording is load-bearing** - MEASURED. With
`E501` *not* selected: `Unused 'noqa' directive (non-enabled: 'E501')` - a **configuration smell**,
someone is suppressing a rule you never enabled. With `E501` selected but not triggered: `Unused
'noqa' directive (unused: 'E501')` - **dead debt**, delete it. One code, two problems; the counts
are not interchangeable.

**Coexisting with another tool's codes.** `RUF102` on an unknown code emits "Add non-Ruff rule codes
to the `lint.external` configuration option" and "Remove the rule code"; setting `lint.external =
["ABC"]` suppresses `RUF102` for `ABC123` - MEASURED.

### 8.3 The type-checker mirror, including one silent hole

| mechanism | status | note |
|---|---|---|
| mypy `--warn-unused-ignores` | **inside `--strict`** | a `# type: ignore` on a line that generates no error |
| mypy `--warn-redundant-casts` | **inside `--strict`** | removable casts |
| mypy `ignore-without-code` | **NOT in `--strict`** | "Warn when a `# type: ignore` comment does not specify any error codes." Enable via `--enable-error-code`, `enable_error_code =`, or `# mypy: enable-error-code="ignore-without-code"`. **Stronger than `PGH003`**: checker-aware, not textual |
| pyright `enableTypeIgnoreComments` | `true` in all four modes | pyright honours PEP 484 `# type: ignore`; `# pyright: ignore` is unaffected by the switch |
| pyright `reportUnnecessaryTypeIgnoreComment` | **`"none"` in ALL four modes, including strict** | a pyright-only project detects **no** stale ignores unless it turns this on by hand |
| pylint `useless-suppression` / `I0021` | **disabled by default** | add to `enable`; fail with `--fail-on=I0021` or `--fail-on=I` |

The pyright rows come from the repository's `main` docs with **no version pinned** - **OPEN**, and
re-verification on any pyright adoption is a rule, not a nicety. Other mypy optional codes to decide
at the same time, each a suppression channel or detector: `redundant-expr`, `truthy-bool`,
`truthy-iterable`, `possibly-undefined`, `explicit-override`, `mutable-override`,
`exhaustive-match`, `deprecated`, `unused-awaitable`, `unimported-reveal` - VERSION-DEPENDENT (mypy
2.3.0). Which to enable is `python_typing_contract_manifest.md`'s decision.

### 8.4 The reason requirement is contract-only

**MEASURED (ruff 0.16.2).** **No ruff rule requires a reason on a suppression** - all 968
explanations were searched. `--add-noqa=<REASON>` can *write* one; nothing checks that one is
present.

- **code named** -> lint-catchable: `PGH004`, mypy `ignore-without-code`.
- **reason stated** -> **contract-only**, mechanisable only by project-owned code: a regex test over
  the suppression form, or a semgrep rule (§10.2). Either can check that text exists; **neither can
  check that the reason is true.** That residual is permanent.

House rule: `# ruff: ignore[CODE] <why, and what would let us remove this>`. If the project wants it
enforced, the check lands on day one - retrofitting means auditing every existing suppression at
once.

### 8.5 Census and ratchet

**MEASURED (ruff 0.16.2).** `--statistics` prints a count per triggered rule, code and name, one per
line, tab-separated. `--ignore-noqa` makes ruff **disregard every `# noqa` in the tree**; the delta
between a normal run and `--ignore-noqa --statistics` is the exact size of the suppression debt.
`--output-format` accepts `concise`, `full`, `json`, `json-lines`, `junit`, `grouped`, `github`,
`gitlab`, `pylint`, `rdjson`, `azure`, `sarif`. Exit codes: `0` clean or fully fixed, `1` violations
remain, `2` abnormal termination; `--exit-zero` forces 0 except for 2, `--exit-non-zero-on-fix`
returns 1 when files were modified.

**The ratchet mechanism - where the number lives, how CI enforces monotonic decrease, who owns the
ceiling - belongs to `python_quality_gates_manifest.md`.** Two constraints this file contributes:
(1) **the count is meaningless without the pin** - a total that falls after an upgrade may mean the
code improved or that a rule left the enabled set, so compare only across an identical ruff version
and an identical `select`; (2) **ratchet the `--ignore-noqa` delta, not the visible findings** -
visible findings can be driven to zero by adding suppressions; the delta cannot be gamed that way.

---

## 9. Is pylint worth it at this scale? A measured answer

**ESTABLISHED.** Pylint infers values through astroid; its docs give `import logging as argparse`
followed by `argparse.error(...)` as a case where it still knows the call is a logging call, and
quote a user calling inference "the killer feature that keeps us using [pylint] in our project
despite how painfully slow it is". Ruff's FAQ concedes the gap: "Pylint does more type inference
than Ruff (e.g., Pylint can validate the number of arguments in a function call)."

**MEASURED (the probe in §1).** Pylint found all three real defects; ruff found none; **and `mypy
--strict` found all three on the untyped version too**. For a strictly-typed project pylint's
advantage over *ruff* is genuine; its advantage over *the stack that already includes `mypy
--strict`* is largely redundant. The genuine residue is two defect classes:

| defect | pylint | cheaper substitute | caveat |
|---|---|---|---|
| Import cycle | `R0401 cyclic-import` - MEASURED as the only one of the three tools that reported a two-module cycle | `ruff analyze graph <path>` emits a JSON module -> imports adjacency map; post-process it in a project-owned pytest | the subcommand prints `warning: 'ruff analyze graph' is experimental and may change without warning` and does not itself detect cycles. The stronger answer is `import-linter`, owned by `python_module_boundaries_manifest.md` |
| Copy-pasted logic across modules | `R0801 duplicate-code` | **none - ruff has no equivalent** | the only defect class here where pylint is the sole mechanical option |

**The cost - ESTABLISHED.** A second rule vocabulary, config file, suppression syntax (`# pylint:
disable=`), unused-suppression audit (`I0021`, off by default) and set of false-positive fights; its
own docs quote the slowness rather than deny it. Pylint 4.0.6 requires Python >= 3.10 and supports
3.10-3.14.

**Verdict: do not run pylint by default at this scale.** Take the cycle residue via `import-linter`
and the duplication residue via review plus the size budgets of §11.1. Reconsider only for a heavily
dynamic codebase (metaclasses, `__getattr__` dispatch, untyped third-party dependencies) - and note
the verdict rests on **one small probe**, a defensible inference from a demonstration, not a
benchmark.

If pylint is adopted anyway, its categories are `C` convention, `R` refactor, `W` warning, `E`
error, `F` fatal, `I` information, and the codes this manifest relies on elsewhere are `E1101`
no-member, `E1120` no-value-for-parameter, `E1310` bad-str-strip-call, `W0102`
dangerous-default-value, `W0135` contextmanager-generator-missing-cleanup, `W0212` protected-access,
`W0221` arguments-differ, `W0602` global-variable-not-assigned, `W0603` global-statement, `W0621`
redefined-outer-name, `W0718` broad-exception-caught, `W0719` broad-exception-raised, `R0401`
cyclic-import, `R0801` duplicate-code, `R0901` too-many-ancestors, `R0902`
too-many-instance-attributes, `R0904` too-many-public-methods, `R0911` too-many-return-statements,
`R0912` too-many-branches, `R0915` too-many-statements, `R1702` too-many-nested-blocks, `R1710`
inconsistent-return-statements, `R1721` unnecessary-comprehension, `R1732` consider-using-with,
`C0103` invalid-name, `C0200` consider-using-enumerate, `C0209` consider-using-f-string, `I0021`
useless-suppression - VERSION-DEPENDENT (pylint 4.0.6). Whether `no-self-use` (reported as `R6301`)
now lives only in the optional `pylint.extensions.no_self_use` extension was **not resolvable** -
**OPEN**.

---

## 10. Extensibility: what you can actually mechanise

### 10.1 `TID251 banned-api` - the one project-specific rule engine ruff has

**MEASURED (ruff 0.16.2).** The `[tool.ruff.lint.flake8-tidy-imports.banned-api]` block in §4.3 was
verified working: `datetime.utcnow()` produces `TID251 'datetime.datetime.utcnow' is banned: Use
datetime.now(tz=UTC) instead.` It matches **fully-qualified member paths**, not just modules, and
carries a custom message - which covers a large share of what teams actually write custom rules for:
a deprecated internal helper, a dangerous stdlib entry point, a library being migrated off, a direct
HTTP call that must go through the project's client. **Residual risk:** it matches the qualified
path, so aliasing through an intermediate name defeats it.

### 10.2 Ruff accepts no plugins - do not propose one

**VERSION-DEPENDENT (ruff 0.16.2).** Ruff's FAQ: "Ruff does not yet support third-party plugins,
though a plugin system is within-scope for the project", tracked as issue #283; the
Flake8-comparison section repeats "Ruff does not support custom lint rules". **FLAGGED-SECONDARY:**
a ruff discussion (#20652) is reported to record that as of September 2025 the maintainers had held
design discussions but "haven't actively started any work on it" and were "still far from reaching
consensus" - that came from a search summary, the thread was not loaded, so the *status* is OPEN
while the FAQ sentence is solid. An agent that proposes writing a ruff plugin has invented a
mechanism.

### 10.3 The ladder, in ascending cost

| option | expresses | cost | verdict here |
|---|---|---|---|
| `TID251` ban-list | "this symbol is forbidden, here is the replacement" | one config block | **first reach.** Nearly free |
| an `ast`-walking pytest | any structural property of the tree: a naming rule, an import-time budget, "every suppression has a reason" | ~40 lines of project code inside the existing gate | **second reach.** One toolchain, one failure surface |
| `libcst` visitor/codemod | the same, plus mechanical rewriting with formatting preserved | a dependency and a real learning curve | one-off migrations only |
| semgrep YAML rule | `pattern`, `patterns`, `pattern-either`, `pattern-not`, `metavariable-pattern`, and `mode: taint` with `pattern-sources`/`pattern-sinks`; `--pattern`/`-e` for a CLI one-liner | a second tool, suppression syntax and CI step | **conditional.** Syntax verified; version, licence tier and whether taint mode is in the OSS CLI **not confirmed** - OPEN. Justified when the rule is a policy (a security boundary), not a style preference |
| pylint plugin | a checker with **astroid inference** - the only option needing inferred types | the whole pylint toolchain (§9) | only if pylint already runs |
| flake8 plugin | a working third-party ecosystem via the `flake8.extension` / `flake8.formatting` entry points | flake8 7.3.0's last release was 2025-06-20, over a year before this pass | only if flake8 already runs. **Do not add flake8 to get plugins** |

Any `contract-only` row in §11-§16 is a candidate for this ladder. Climb it sparingly - each rung
adds a tool, a config, a suppression vocabulary and a failure mode. **"We agreed on this in review"
is a row that should shrink over time, not one to delete by pretending a rule covers it.**

---

# Half two: the practice and anti-pattern catalogue

Two framing facts, so nothing below is over-claimed. **ESTABLISHED:** PEP 8 is Status *Active*, Type
*Process*; its vocabulary is "should"/"prefer"/"recommended", and *must* appears only where it
restates a rule of the standard library or the language. It ships escape hatches - ignore a
guideline when applying it reduces readability, when surrounding code already breaks it, when the
code predates it, or when older-Python compatibility forbids the newer construct - plus "do not
break backwards compatibility just to comply with this PEP!", and it ranks consistency: with the PEP
< within a project < within a module or function. **ESTABLISHED:** PEP 20 is Informational and
carries no binding force. **The project's real style authority is whatever `ruff` is configured to
reject** (§2). PEP 257 is the exception that proves the rule: it *does* enumerate what a docstring
must contain (§15.1), which is why docstring-as-contract can be grounded rather than asserted.
Version floors named below are stated as behaviour; `python_platform_baseline_manifest.md` owns
*when*.

---

## 11. Function altitude

### 11.1 Sizing: a proxy is not a measure

**Composed Method** (Kent Beck, *Smalltalk Best Practice Patterns*, 1996) is the named pattern
behind "each method performs one identifiable task, with all operations at the same level of
abstraction" - **FLAGGED-SECONDARY**: the attribution is solid, no authoritative page carrying the
pattern text was loaded, so cite the name and the work, never a quotation.

| budget | ruff mechanism | default | pylint |
|---|---|---|---|
| cyclomatic complexity ("one plus the number of decision points in the function") | `C901 complex-structure`, `lint.mccabe.max-complexity` | **10**, rule **off by default** | `R0915`, `R0912` |
| statements / branches / returns per function | `lint.pylint.max-statements` / `max-branches` / `max-returns` | **50** / **12** / **6** | `R0915` / `R0912` / `R0911` |
| public methods per class | `lint.pylint.max-public-methods`; rule `PLR0904` is **preview** | **20** | `R0904` |
| nested blocks | **no ruff setting** (`max-nested-blocks` is absent from ruff's settings page) | - | `R1702` |

Route: **lint-catchable (proxy) + contract-only.** These metrics proxy size, not cohesion: a
six-line function can still do two things, and no rule distinguishes an essential 12-branch dispatch
from accidental complexity. **No measurement backs any of the numbers** - they are tool defaults and
none of the publishing pages cites a study. Treat them as coordination devices and as ratchet
ceilings that stop a function getting worse, never as quality scores. Metric evidence is
`python_quality_gates_manifest.md`'s subject.

### 11.2 Parameters: count, and the two symbols that fix it

**VERSION-DEPENDENT (ruff 0.16.2).** `PLR0913 too-many-arguments`, default **5** via
`lint.pylint.max-args`: "Functions with many arguments are harder to understand, maintain, and
call." `PLR0917 too-many-positional-arguments`, added in **0.16.0** and **not** preview, default
**5** via `lint.pylint.max-positional-args`; its own text names the remedies - "refactoring
functions with many arguments into smaller functions with fewer arguments, using objects to group
related arguments, or migrating to keyword-only arguments". **OPEN:** whether `PLR0913` counts
keyword-only parameters is not stated on the rule page, and it determines whether the bare-`*`
remedy actually satisfies the rule.

**Feature-eliminated remedies, ESTABLISHED.** PEP 3102 (3.0): keyword-only parameters come after
`*args` or a bare `*`, may be required or defaulted, and extra positionals raise `TypeError` - **a
bare `*` is the cheapest mechanical fix for both the boolean trap and the long-argument-list
smell**. PEP 570 (3.8): `/` marks positional-only parameters, motivated by freedom to **rename**
later without breaking callers, parity with C-implemented signatures, removal of `**kwargs`
collisions, and faster argument handling. Order: positional-only -> positional-or-keyword ->
keyword-only. Fowler's named remedies: **Introduce Parameter Object**, **Preserve Whole Object**.
Residual: a parameter object that is itself a bag of twelve fields passes the rule -
**contract-only**.

### 11.3 The boolean trap

**VERSION-DEPENDENT (ruff 0.16.2).** Three rules, **none default-on, none with a fix**: `FBT001
boolean-type-hint-positional-argument` (fires on `bool` and on unions containing bool - `bool |
int`, `Optional[bool]` - in positional position; its page cites Adam Johnson's "How to Avoid 'The
Boolean Trap'"), `FBT002 boolean-default-value-positional-argument`, `FBT003
boolean-positional-value-in-call` (the call site, with
`lint.flake8-boolean-trap.extend-allowed-calls`).

**ESTABLISHED.** Fowler names the smell **Flag Argument** (bliki, 23 June 2011): "A flag argument is
a kind of function argument that tells the function to carry out a different operation depending on
its value", and "My general reaction to flag arguments is to avoid them." The catalog refactoring is
**Remove Flag Argument**. Three nuances stop it becoming dogma: keep the flag-taking function
*private* when the implementation genuinely interleaves both behaviours; derive the flag internally
from caller data; and it has "some justification" when the value comes straight from a UI checkbox
or a data source.

Route: **lint-catchable** for the boolean-typed subset, **feature-eliminated** by a bare `*` or an
`Enum` that replaces a two-valued domain with a named one, **contract-only** in general - a `str`-
or `Enum`-typed mode parameter is invisible to every linter. The checker accepts `f(True)` and
`f(False)` identically; only the linter objects.

### 11.4 Guard clauses, early return, and return-shape consistency

**ESTABLISHED.** The citable name is Fowler's **Replace Nested Conditional with Guard Clauses**
(catalog, 2nd ed. 2018), whose page shows nested `if/else` collapsing into sequential early returns
to make the flow linear. Cite that, not "guard clause" as folklore. Adjacent: **Decompose
Conditional**, **Replace Conditional with Polymorphism**.

Route: **lint-catchable (partial) + contract-only.** `RET505 superfluous-else-return` and pylint
`R1702 too-many-nested-blocks`; `SIM103 needless-bool` is a third fragment - **FLAGGED-SECONDARY**
on its code-to-name pairing, read from ruff's rules index rather than the rule page; verify with
`ruff rule SIM103` first. Flattening an `if/else` is not the same as extracting a guard, and
`RET505`'s fix is cosmetic.

Return shape: `RET503 implicit-return` (**fix always available**, and it writes `return None`, which
may be the wrong contract), `RET504 unnecessary-assign` (off by default), `RET505`; pylint `R1710
inconsistent-return-statements` is the direct "some paths return a value, some do not" check. Route:
**type-catchable (primary)** via a declared return type under mypy `--disallow-untyped-defs`, with
those codes as backstops. **The residual risk an agent walks into:** declaring `X | None` silences
every rule listed here while leaving the design flaw - one function with two unrelated outcomes -
intact. `error_tracing_contract_manifest.md` owns the typed-result alternative.

### 11.5 Magic values, and purity

`PLR2004 magic-value-comparison` - "readers will have to infer the meaning of the value from the
context"; configured by `lint.pylint.allow-magic-value-types`; **no autofix, because naming a
constant is a human decision**; off by default and contested (it fires readily in tests, hence the
§4.3 carve-out)
- VERSION-DEPENDENT (ruff 0.16.2). Route: **lint-catchable**, contested.

Purity: **contract-only, permanently.** There is no `pure`/`const` qualifier in Python's type
system, so a purity claim is runtime-checked by a design-by-contract library (`deal.pure`) or it is
convention - `python_typing_contract_manifest.md` §6 establishes this. What *is* mechanical is the
neighbourhood: `B006`, `B008`, `RUF012`, `PLW0603` catch the shared-state constructs that make
purity impossible (§16). A cached impure function is a correctness bug no tool sees (§13.6).

---

## 12. Module altitude: the liftable unit

**The *enforced* boundary is not this file's.** `python_module_boundaries_manifest.md` owns layout,
packaging metadata, the import system as a boundary, the public-API and deprecation contract, plugin
seams, and machine enforcement of dependency direction - including the `import-linter` contract
vocabulary (`layers` with `exhaustive`, `forbidden`, `independence`, `protected`,
`acyclic_siblings`). This section covers only what a module *author* writes and which rule or flag
sees it.

### 12.1 What belongs in `__init__.py`

**ESTABLISHED / OPEN.** The only PEP statement about `__init__.py` *content* is PEP 257's: the
package docstring there "should list the modules and subpackages exported by the package". **No PEP
says what code may live there** - that is convention the project must pin. The defensible convention
here: a docstring, an `__all__`, and re-export statements, nothing else, because everything in
`__init__.py` runs on every import of anything inside the package (§12.4).

**VERSION-DEPENDENT (ruff 0.16.2) - a genuine trapdoor.** `F401 unused-import` is
`__init__.py`-aware: there it "will suggest a safe fix to export first-party imports with either a
redundant alias or, if already present in the file, an `__all__` entry", and it documents the
convention - "Consider using a 'redundant' import alias, which instructs Ruff (and other tools) to
respect the re-export". Fixes that *remove* an unused import are safe **everywhere except**
`__init__.py`, where the removal fix is preview and unsafe for third-party and stdlib imports
"because the module's interface changes". Settings: `lint.ignore-init-module-imports`,
`lint.pyflakes.allowed-unused-imports`. **An agent running `--fix` broadly can still amputate a
re-export surface** - run `--diff` over `__init__.py` specifically.

### 12.2 Explicit re-export, `__all__`, and the underscore

Route: **type-catchable.** mypy `--no-implicit-reexport` (inside `--strict`): by default "imported
values to a module are treated as exported and mypy allows other modules to import them"; the flag
"changes the behavior to not re-export unless the item is imported using from-as or is included in
`__all__`". Exactly **two spellings** are accepted: `from foo import bar as bar`, or `bar` in
`__all__` - VERSION-DEPENDENT (mypy 2.3.0). This is one of the few module-shape practices that is
genuinely checker-enforced.

**ESTABLISHED.** PEP 8's public/internal doctrine is the citable API rule: documented interfaces are
public unless marked provisional or internal; undocumented interfaces are to be assumed internal;
**a namespace containing internal elements is itself internal**; imported names are an
implementation detail and callers must not rely on indirect access unless documented (`os.path` is
the named exception); `__all__` declares the public API and an empty `__all__` declares "no public
API"; and backwards-compatibility guarantees apply only to public interfaces.

`__all__` hygiene: `RUF022 unsorted-dunder-all` (isort-style ordering; fix sometimes available, and
**unsafe** when whole-line comments sit inside the literal or several items share a line with a
trailing comment) - VERSION-DEPENDENT (ruff 0.16.2). Ruff's `PL` family also carries
invalid-`__all__`-format and invalid-`__all__`-object checks and pyflakes flags an undefined name in
`__all__`, but **their exact codes were not verified on their own pages and are therefore omitted
rather than guessed** (see the quarantine list). Verify with `ruff rule <code>` first.

**ESTABLISHED - the underscore is the whole of Python's visibility story.** `_name` is a weak
"internal use" marker whose **only** runtime effect is exclusion from `from M import *`; `name_`
avoids keyword clashes (`class_`); `__name` in a class body triggers mangling to `_ClassName__name`;
`__dunder__` names are reserved and "never invent such names". PEP 8 prescribes a **single** leading
underscore for non-public members, reserving the double form for deliberate subclass-collision
avoidance, and warns that mangling complicates debugging and `__getattr__()`. `__all__` makes
nothing private at runtime. **Any sentence implying enforced privacy is false:** nothing prevents
`from pkg._impl import thing`. Route: **contract-only at the definition site, lint-catchable at the
use site** (`SLF001 private-member-access`, off by default; pylint `W0212 protected-access`),
**fitness-function** via an `import-linter` `forbidden`/`protected` contract - the only mechanism
that actually stops the import, and it is `python_module_boundaries_manifest.md`'s. The Google guide
adds the public/internal column PEP 8 omits, including `_CapWords` for internal classes and
`_CAPS_WITH_UNDER` for internal constants - ESTABLISHED (corporate guide, not a PEP).

### 12.3 Naming: what PEP 8 fixes, and what the project must pin

**ESTABLISHED.** PEP 8's complete set: modules short all-lowercase (underscores allowed); packages
all-lowercase (underscores discouraged); C/C++ extension modules a leading underscore; classes
`CapWords`; exceptions the class convention plus an `Error` suffix *for actual errors* (a non-error
exception used for flow control needs no suffix); functions and variables `lower_with_under`;
constants `UPPER_WITH_UNDER`; type variables `CapWords`, short, with `_co`/`_contra` for covariance
and contravariance; `self`/`cls` first; a single trailing underscore to dodge a keyword; never `l`,
`O` or `I` alone.

Route: **lint-catchable (partial).** `N801 invalid-class-name`, `N802 invalid-function-name`, `N803
invalid-argument-name`, `N806 non-lowercase-variable-in-function`, `N818
error-suffix-on-exception-name`; **none has a fix and only `N999 invalid-module-name` is
default-on** - MEASURED. pylint's equivalent is `C0103 invalid-name`; note pylint 4.0.0 changed
module-scope naming so "Module-level constants that are reassigned are treated as variables and
checked against `--variable-rgx` rather than `--const-rgx`" - VERSION-DEPENDENT (pylint 4.x).

**OPEN - PEP 8 is silent, so the project pins these:** boolean names, predicate names,
factory-function names, private-helper naming beyond the underscore, and **test names**. The only
citable test-naming convention found is the Google guide's `test_<method_under_test>_<state>` -
ESTABLISHED (corporate guide). `python_testing_tooling_manifest.md` owns the decision; it is
recorded here because nothing else in the collection carries a citable source for it.

### 12.4 No work at import time

Route: **contract-only + test-catchable.** **No linter detects expensive or effectful work at import
time.** The only first-party instrument is `python -X importtime` (3.7), with `-X importtime=2`
(**3.14**) additionally tracing already-loaded modules and printing `cached` in both time columns;
the environment variable is `PYTHONPROFILEIMPORTTIME` (`1`/`2`) - ESTABLISHED / VERSION-DEPENDENT
(3.14). The mechanisation is a project-owned test asserting an import-time budget. Measurement
technique is `python_runtime_diagnostics_manifest.md`'s.

**The tension must be recorded, not resolved silently.** `PLC0415 import-outside-top-level` flags
deferred imports and **names the legitimate reasons in its own text**: "An import statement would
typically be placed within a function only to avoid a circular dependency, to defer a costly module
load, or to avoid loading a dependency altogether in a certain runtime environment." `PLC0415` and
"module import must be free" cannot both be satisfied; the project chooses and writes it down, and
**an agent must not "fix" either direction unilaterally**. Defensible split: top-level imports
everywhere, `PLC0415` selected, and a coded, reasoned suppression at each of the few deferred
imports that exist for one of the three reasons the rule itself legitimises.

### 12.5 Structuring a module so it can be lifted

**OPEN - the property "liftable" has no primary-source definition; the mechanisms named below are
each verified, their sufficiency is not.** Route: **contract-only at module altitude,
fitness-function at project altitude.** The properties that make a module liftable - imports only
downward, no import-time side effects, a declared public surface, dependencies inverted at every
side-effect boundary - are stated as design rules by `software_spec_discipline_manifest.md` (C2/C3
reusability and the dependency surface, F1 pure core / imperative shell, F2 dependency inversion)
and `architecture_manifest_default.md` (coupling and cohesion); the mechanical check is an
`import-linter` contract in `python_module_boundaries_manifest.md`. What this file adds: **at the
altitude a module author works at, the only mechanical signals are `F401`, `RUF022`, mypy
`--no-implicit-reexport`, `PLC0415` and `SLF001`** - and those five do not add up to a boundary. Do
not mistake a clean lint run for a modular design.

---

## 13. Expression altitude

Only idioms with a defect behind them, not a taste. Where the hazard is owned by
`python_language_hazards_manifest.md`, the row gives the practice and the code and stops.

### 13.1 Comprehensions, generators, and one honest gap

**ESTABLISHED (Google guide) / OPEN (the enforcement gap).** The Google guide forbids comprehensions
with "multiple `for` clauses or filter expressions", restricts lambdas to one line, and allows
conditional expressions only when each part fits on one line. **No linter limits comprehension
nesting:** `C901` counts decision points across the enclosing function, and `max-nested-blocks` is
absent from ruff's settings (pylint's `R1702` counts statement blocks, not comprehensions). Route:
**contract-only** - a consequential row, because a three-clause comprehension is exactly the
construct with nowhere to put a breakpoint.

Generator versus list is **lint-catchable** through ruff's `C4` family and pylint `R1721
unnecessary-comprehension`. **FLAGGED-SECONDARY on the individual pairings** `C400`, `C404`, `C416`,
`C417`: read from ruff's rules index, which demonstrably mis-paired other rows during verification.
The family is confirmed; verify each code with `ruff rule <code>` before writing it into a config.
Residual for review: rewriting a list comprehension to a generator changes re-iterability and moves
when exceptions are raised.

The `dict.get(key, default)` / `setdefault` idiom over a `try`/`except KeyError` or a membership
test plus subscript is sound and partly covered by `SIM`. **No exact `SIM` code for it was verified
this session, so none is asserted** - route: **lint-catchable in principle, contract-only until the
code is verified**. This is the standard in practice: a plausible code is worse than an admitted
gap, because a wrong code in a `select` list silently disables a check the project believes it has.

### 13.2 `zip`, `enumerate`, and the fix that preserves the bug

**ESTABLISHED / VERSION-DEPENDENT (ruff 0.16.2).** `zip()` truncates silently to the shortest
iterable. PEP 618 (3.10) added `strict=True`, raising `ValueError` on differing lengths; strict is
not the default because truncation is legitimately useful ("extremely useful, for example, when
dealing with infinite iterators"). Route: **feature-eliminated (`strict=True`) + lint-catchable
(`B905`)** - but B905's always-available fix is unsafe and inserts `strict=False` (§5.2). Insert
`strict=True` by hand and treat the `ValueError` path as a tested path. Index arithmetic instead of
`enumerate` is pylint `C0200 consider-using-enumerate` - **lint-catchable, pylint-only**.

### 13.3 `pathlib` is not a drop-in replacement

**ESTABLISHED.** The docs say exactly that and name the differences: `os`/`os.path` are C and
faster; `os.path.abspath()` eliminates `".."` segments while `Path.absolute()` preserves them "for
greater safety"; `Path("my_folder/")` normalises away the trailing slash, "which may change behavior
with OS APIs"; `Path("./my_program")` normalises to `Path("my_program")`, changing PATH lookup. A
"Corresponding tools" mapping table is provided (`os.path.dirname` -> `PurePath.parent`,
`os.path.join` -> `PurePath.joinpath`, `os.walk` -> `Path.walk`).

Route: **lint-catchable with one exception.** `PTH118 os-path-join` is verified; **`PTH123
builtin-open` flags every `open()` call** in favour of `Path.open()`, and its own page concedes that
pathlib "can be less performant than working directly with strings, especially on older versions of
Python", with the fix unsafe when it would drop comments. **`PTH123` is taste, not a defect rule** -
§4.3 ignores it. Version floors for the `pathlib` API surface (a minimum-target input) are the
hub's.

### 13.4 f-strings, and the one place the advice inverts

**VERSION-DEPENDENT (ruff 0.16.2).** The general idiom prefers f-strings, and the `FLY` family
(flynt) carries ruff's f-string conversion rules, one of which is default-on. **Inside a logging
call the advice reverses:** `G001`-`G004` exist because a formatted string is built eagerly even
when the level is disabled and because it destroys the structured-logging message key, and **all
four are off by default** (§4.2). **The trap:** a blanket "modernise to f-strings" pass deoptimises
every log call and breaks the house rule. `logging_observability_manifest.md` owns the policy and
already records that mypy/pyright/ruff may push the rewrite the wrong way; this file supplies the
codes - `G001`-`G004` for formatting, `TRY400`/ `LOG004`/`LOG007`/`LOG014` for the traceback
channel, `G101` for the `extra=` key collision, and `lint.logger-objects` so the rules recognise the
project's own logger wrapper.

`str.removeprefix`/`removesuffix` (PEP 616, 3.9) return the original unchanged when the affix is
absent. The motivation is a documented, repeated user error: `lstrip`/`rstrip` take a **character
set**, not a substring - "There have been repeated issues on Python-Ideas, Python-Dev, the Bug
Tracker, and StackOverflow related to user confusion about the existing str.lstrip and str.rstrip
methods" - ESTABLISHED. Route: **feature-eliminated + lint-catchable** via pylint `E1310
bad-str-strip-call` (ruff carries the same check in its Pylint family), which flags only provably
wrong calls.

### 13.5 `contextlib` helpers and their two documented traps

**ESTABLISHED / VERSION-DEPENDENT (3.12).** Both traps are **contract-only**: a `@contextmanager`
generator is **single-use** - "These single use context managers must be created afresh each time
they're used - attempting to use them a second time will trigger an exception" (`RuntimeError:
generator didn't yield`); and an exception from the `with` body "is reraised inside the generator at
the point where the yield occurred", so **a generator that traps an exception merely to log it "must
reraise that exception"** or the `with` statement treats it as handled and execution silently
continues. Reentrancy is documented and is **not** thread safety: `suppress`, `redirect_stdout`,
`redirect_stderr` and `chdir` are reentrant, and the docs note `redirect_stdout` is reentrant but
**not** thread-safe. In 3.12 `suppress` can strip suppressed exceptions out of a
`BaseExceptionGroup`.

Adjacent lint fragments, both pylint: `W0135 contextmanager-generator-missing-cleanup` and `R1732
consider-using-with`. `contextlib.suppress` as the only sanctioned explicit silencing is
`error_tracing_contract_manifest.md`'s.

### 13.6 `functools` caching, and what it retains

**ESTABLISHED / VERSION-DEPENDENT (3.12).** The docs' own words: "The cache keeps references to the
arguments and return values until they age out of the cache or until the cache is cleared", and "If
a method is cached, the `self` instance argument is included in the cache." They also state it
"doesn't make sense to cache functions with side-effects, functions that need to create distinct
mutable objects on each call (such as generators and async functions), or impure functions such as
time() or random()", and that all arguments must be hashable. `functools.cache` (3.9) is
`lru_cache(maxsize=None)` - **unbounded, never evicting**. `typed=False` (the default) treats `1`
and `1.0` as the same key, and typing applies only to the immediate arguments, not their contents.

Route: **lint-catchable for the leak, contract-only for the rest.** `B019 cached-instance-method` -
"Using the `functools.lru_cache` and `functools.cache` decorators on methods can lead to memory
leaks, as the global cache will retain a reference to the instance, preventing it from being garbage
collected." No autofix; the remedy is structural. `B019` does **not** catch a module-level cache
keyed on an object you pass in, and **nothing catches a cache over an impure function.**

`cached_property` (3.8) requires a mutable `__dict__`, so it fails on metaclasses and on `__slots__`
classes without `__dict__` (**test-catchable** - any test that touches the property); it "interferes
with the operation of PEP 412 key-sharing dictionaries", enlarging instance dicts; **the
undocumented per-property lock was removed in 3.12** and the docs now state "The getter function
could run more than once on the same instance, with the latest run setting the cached value" -
**contract-only**, and code written against 3.11 semantics becomes racy on upgrade with no
diagnostic (`python_concurrency_determinism_manifest.md` owns the analysis). Invalidation is `del
instance.attr`, and unlike `@property` it permits writes.

### 13.7 The `match` statement: five ways it silently does nothing

**ESTABLISHED (PEP 634, 3.10).** Every claim is PEP 634 text.

1. **A bare name is a capture pattern**: it "always succeeds" and binds - never a value comparison.
   `case RED:` binds `RED` and matches everything. A value comparison requires a **dotted** name
   (`Color.RED`), resolved by normal name resolution and compared with `==`.
2. `_` is the wildcard: always succeeds, "binds no name". And "In a given pattern, a given name may
   be bound only once".
3. **"Although `str`, `bytes`, and `bytearray` are usually considered sequences, they are not
   included in the above list and do not match sequence patterns."** `case [x]:` never matches
   `"a"`; the branch is dead and silent.
4. A **mapping pattern** succeeds if every key *in the pattern* is present in the subject - extra
   subject keys are fine and `**name` captures them. Class patterns convert positional sub-patterns
   via `__match_args__` (auto-generated for namedtuples and dataclasses; for builtins a single
   positional pattern matches the whole subject). Guards run *after* the pattern succeeds and may
   have side effects. There is **no fallthrough**.
5. **"If no case blocks qualify the match statement is complete"** - **no error is raised.**
   Exhaustiveness is not a language guarantee.

Route: **type-catchable, but only if you write the arm.** A final `case _:` calling
`typing.assert_never(value)` makes the checker error when a new variant appears; mypy's
`exhaustive-match` optional code is the checker-side equivalent. Without that arm there is **no
diagnostic at any level**. Item 1 is **contract-only + test-catchable**: the program runs, silently
takes the first branch, and no linter is obliged to complain. `assert_never` entered `typing` in
3.11; `error_tracing_contract_manifest.md` §5 owns the exhaustiveness pattern. **OPEN:** the exact
CPython `typing` docs wording for `assert_never` was not captured (the page truncated on fetch) -
the technique is ESTABLISHED, the quotation is unavailable.

### 13.8 Walrus discipline, and `itertools` hazards

**ESTABLISHED (PEP 572, 3.8).** The illegal shapes are compile-time errors: unparenthesised at
statement level, as the right side of an assignment statement, as a keyword-argument value, as a
function default, in an annotation, in an unparenthesised lambda body, in an f-string format-spec
position, and in a comprehension's *iterable* expression. Inside a comprehension the target **binds
in the containing scope** (honouring `nonlocal`/`global`) and may not collide with a `for` target of
that comprehension. `:=` binds more tightly than a comma and less tightly than every other operator.
Route: **contract-only** - the PEP's own advice is the whole enforcement (prefer a statement when
both forms work; restructure if evaluation order becomes ambiguous), and the comprehension-scope
leak is *specified* behaviour, not a bug. House convention: no walrus in comprehensions, and none in
an expression a reader must evaluate twice. One adjacent fragment: `RUF018 assignment-in-assert`,
whose binding vanishes with the assert under `-O`.

**ESTABLISHED.** `itertools` hazards worth routing, all **contract-only** except the last: `tee`
"may require significant auxiliary storage" and tee iterators "are not threadsafe. A RuntimeError
may be raised when simultaneously using iterators returned by the same tee() call"; `product`
"completely consumes the input iterables, keeping pools of values in memory"; `cycle` may require
significant auxiliary storage; `groupby` requires input **already sorted on the same key function**;
and `batched` gained a `strict` parameter that raises `ValueError` if the final batch is short. The
one shape a rule sees is `B031 reuse-of-groupby-generator` - **lint-catchable**. `tee`'s
thread-unsafety is `python_concurrency_determinism_manifest.md`'s subject.

---

## 14. Data-shape decisions

`python_typing_contract_manifest.md` §2 owns the typing vocabulary - `Protocol` versus `abc.ABC`,
`@dataclass`, `TypedDict` with `Required`/`NotRequired`/`ReadOnly`, `NamedTuple`, `Enum` plus
`Literal`, `NewType`, generics, `Self`, `Final`/`@final`, `Annotated`, `Never`/`NoReturn`. **None of
that is restated.** This section adds the decision rule and the sharp edges a practice catalogue
must carry.

| you need | reach for | why |
|---|---|---|
| a named record with behaviour and identity | `@dataclass` | the default; `eq`/`repr`/`init` free, and it can grow methods |
| the same, immutable and hashable | `@dataclass(frozen=True)` | freeze is **shallow** and bypassable - `python_typing_contract_manifest.md` §6 owns that caveat |
| a tuple-shaped value that must stay tuple-compatible (unpacking, indexing, an existing API) | `NamedTuple` | positional compatibility is the *only* reason to prefer it |
| a description of a dict you do **not** own - a JSON payload, a config blob | `TypedDict` | types an existing dict at a boundary; creates no class, validates nothing |
| a genuinely open key space (user-supplied keys, a cache) | `dict[K, V]` | if the keys are known and closed, you wanted a row above |
| a closed set of named alternatives | `Enum` | the default enum; the docs prescribe nothing further |
| a closed set that must interoperate with existing `str`/`int` constants | `StrEnum` (3.11) / `IntEnum` | **interoperability tools, not the default** (14.2) |
| a distinct domain type over a primitive (`UserId` over `str`) | `NewType` | the primitive-obsession remedy at near-zero cost, and **zero validation** |
| a validated value parsed at the shell boundary | a validating model | "parse, don't validate" - `python_typing_contract_manifest.md` §5 |

Route for the table: **type-catchable** once the shape is declared. Route for *choosing correctly*:
**contract-only** - nothing tells you that a `dict[str, Any]` threaded through nine functions should
have been a dataclass.

### 14.1 Dataclass sharp edges

**ESTABLISHED / VERSION-DEPENDENT (3.14).** Defaults: `init=True, repr=True, eq=True, order=False,
unsafe_hash=False, frozen=False, match_args=True, kw_only=False, slots=False, weakref_slot=False`
(`match_args`/`kw_only`/`slots` from 3.10, `weakref_slot` 3.11, `field(..., doc=)` 3.14).

- **`slots=True` returns a different class object**: "`__slots__` attribute will be generated and
  **new class will be returned instead of the original one**". Anything that captured the class
  before decoration - a registry, a decorator chain, a closure - points at a stale object; and
  "Passing parameters to a base class `__init_subclass__()` when using `slots=True` will result in a
  `TypeError`". Route: **test-catchable** (a registry test), contract-only otherwise.
- **Mutable-default rejection is hashability-based since 3.11**, not type-based: "unhashable objects
  are now not allowed as default values. Unhashability is used to approximate mutability", raising
  `ValueError`. **A custom mutable-but-hashable default still slips through** - the residue is
  contract-only.
- **`dataclasses.KW_ONLY` (3.10)** is a sentinel *annotation*: every field after a pseudo-field
  annotated `KW_ONLY` becomes keyword-only, the pseudo-field is otherwise ignored (including its
  name), only one is permitted per class, and "By convention, a name of `_` is used". Route:
  **feature-eliminated** for §11.2's long-argument-list smell.
- **`asdict()`/`astuple()` deep-copy**: they recurse dataclasses, dicts, lists and tuples and
  **`copy.deepcopy()` everything else** - a hidden cost and an identity break, and a bad default for
  logging or serialisation. `fields()` omits `ClassVar` and `InitVar`. Route: **contract-only**.
- **A mutable class attribute on a non-dataclass** is `RUF012 mutable-class-default`: "Mutable
  default values share state across all instances of the class, while not being obvious", with
  `typing.ClassVar` named as a remedy - VERSION-DEPENDENT (ruff 0.16.2). Residual: adding the
  `ClassVar` annotation *silences the rule while keeping the shared mutable*.

### 14.2 Enum sharp edges

**ESTABLISHED / VERSION-DEPENDENT (3.11).** `StrEnum`, `ReprEnum`, `EnumCheck` + `@verify`,
`@member`/ `@nonmember` and `@global_enum` all arrived in 3.11.

- **`StrEnum` members *are* strings.** `str()` and `__format__()` return the **value**, not the
  name; `auto()` produces the lower-cased member name; any string operation returns a plain `str`,
  leaving the enumeration. Documented interop caveat: some stdlib code tests `type(x) == str` rather
  than `isinstance`, so an explicit `str(MyStrEnum.MEMBER)` is sometimes required.
- **`IntEnum` members are ints**: `Number.THREE == 3` is `True`, and any integer operation returns a
  plain `int`. In 3.11 `IntEnum.__str__` became `int.__str__` "to better support the replacement of
  existing constants use-case". The docs position `IntEnum`/`StrEnum`/`IntFlag` as "drop-in
  replacements for existing integer- and string-based values" - **interoperability tools**. Plain
  `Enum` is the default and the docs do not prescribe when to use which - **OPEN**, a project
  decision.
- **The consequence an agent misses:** because members compare equal to plain values, a "migration
  to enums" can stay half-finished forever without one failing test, and swapping a plain constant
  for a `StrEnum` **changes log output** the moment `str()` or `format()` touches it.
- **The only runtime enum invariants the stdlib offers:** `@unique` raises `ValueError` on aliases;
  `@verify(UNIQUE)` is the same check; `@verify(CONTINUOUS)` rejects gaps between the lowest and
  highest member; `@verify(NAMED_FLAGS)` rejects flag aliases including unnamed values. Route:
  **feature-eliminated**, but per class - nothing forces the decorator onto a new enum.

### 14.3 Typed wrappers against primitive obsession

**ESTABLISHED / VERSION-DEPENDENT (3.11).** `NewType` costs almost nothing: "these checks are
enforced only by the static type checker. At runtime, the statement `Derived = NewType('Derived',
Base)` will make `Derived` a callable that immediately returns whatever parameter you pass it." It
became a class in 3.10 (extra call cost), with 3.9-level performance restored in 3.11. **It adds no
validation**, and arithmetic between two `NewType`s over `int` is unchecked -
`python_typing_contract_manifest.md` §4 owns that ceiling.

Fowler's name for the failure is **Primitive Obsession**; the catalog remedies are **Replace
Primitive with Object**, **Introduce Parameter Object**, **Preserve Whole Object**, **Replace Type
Code with Subclasses**; the adjacent smells are **Data Clumps** and **Data Class** - ESTABLISHED for
the refactoring names, from Fowler's own online catalog. Route: **type-catchable** for the wrapper,
**contract-only** for noticing you needed one.

---

## 15. Docstrings as contracts

`python_typing_contract_manifest.md` §7 owns the **style menu** (Google, NumPy, reST, Napoleon,
"pick ONE style") and the signature-versus-docstring split. This section adds what PEP 257 makes
normative and what mechanically checks it.

### 15.1 What PEP 257 actually requires

**ESTABLISHED.** A docstring is "a string literal that occurs as the **first statement** in a
module, function, class, or method definition" and becomes that object's `__doc__`. **A multi-line
function or method docstring MUST document: the behaviour summary, the arguments, the return
value(s), the side effects, the exceptions raised, and any restriction on when it can be called** -
plus which arguments are optional and whether keyword arguments are part of the interface. That list
is the primary-source warrant for docstring-as-contract; it is not this collection's invention.

One-line rules: triple quotes even for a one-liner (so it can grow); closing quotes on the same
line; no blank line before or after; ends in a period; **phrased as a command** ("Return the ...")
not a description ("Returns the ..."); and it must **not restate the signature** - that form "is
only appropriate for C functions". At other altitudes: a class docstring summarises behaviour and
lists public methods and instance variables, documenting `__init__` separately, and a subclass
docstring must state whether a method **overrides** (replaces without calling) or **extends** (calls
plus adds) the superclass method; a module docstring lists the classes, exceptions and functions
exported with a one-line summary each; a package docstring in `__init__.py` lists the modules and
subpackages exported; a script docstring is its usage message. **PEP 257 deliberately mandates no
markup** - it standardises "the high-level structure of docstrings ... without touching on any
markup syntax within docstrings", so Google, NumPy and reST are third-party conventions layered on a
silent PEP.

**PEP 727 is WITHDRAWN** - ESTABLISHED. It proposed `typing.Doc` inside `Annotated` so per-parameter
documentation could live in the signature; the resolution records that "The reception of this PEP
was mostly negative, with concerns raised about verbosity and readability." **There is no
standardised machine-readable per-parameter documentation.** A docstring microsyntax is the only
option, and advice to emit `Annotated[str, Doc("...")]` as "the modern way" is wrong.

**Two conventions disagree on duplication.** The Google guide states that **types need not be
repeated in the docstring when they are in the signature**, and mandates a docstring "for every
function that has one or more of the following properties: being part of the public API, nontrivial
size, [or] non-obvious logic", with `Args:` / `Returns:` (or `Yields:`) / `Raises:` sections -
ESTABLISHED. numpydoc specifies **15 ordered sections** (Short summary, Deprecation warning,
Extended Summary, Parameters, Returns, Yields, Receives, Other Parameters, Raises, Warns, Warnings,
See Also, Notes, References, Examples), writes parameters as `name : type` with a space *before* the
colon, uses `x : int, optional`, braces for a closed set, `x1, x2 : array_like` for shared types,
keeps the stars on `*args`/`**kwargs` while omitting their type, and treats `Raises` as optional and
"used judiciously, i.e., only for errors that are non-obvious or have a large chance of getting
raised" - ESTABLISHED. **numpydoc gives no rule about omitting types when annotations are present**,
so a "numpydoc + annotations" duplication policy is a project decision - **OPEN**.

### 15.2 The enforcement ladder: presence -> convention -> coverage -> agreement -> truth

Every mechanism in the table is VERSION-DEPENDENT on the pin in the Version anchor (ruff 0.16.2,
interrogate 1.7.0, pydoclint 0.9.1); the *ordering* of the rungs is the analyst's synthesis - OPEN.

| rung | mechanism | proves | cannot |
|---|---|---|---|
| **presence** | `D103 undocumented-public-function` and the rest of `D1xx`; `lint.pydocstyle.ignore-decorators` exempts decorated functions | a docstring exists | `"""Do the thing."""` passes |
| **convention** | `lint.pydocstyle.convention` = `"google"`/`"numpy"`/`"pep257"`, **subtractive** (§6.3) | one style across the tree | choosing a convention silently *disables* the incompatible `D` rules |
| **coverage** | `interrogate 1.7.0` `--fail-under` (default **80.0**), with `--ignore-init-method`, `--ignore-nested-functions`, `--ignore-private`, `--omit-covered-files`, and a pre-commit hook | the presence rate does not regress | presence only - 100% coverage of empty docstrings is achievable. **Conflict resolved:** `--fail-under` and the config default of **80** are confirmed from interrogate's own README - see `python_quality_gates_manifest.md` §11.2, which adjudicated the two fact packs that disagreed. Wire it |
| **agreement** | ruff's `DOC` family (pydoclint, **all preview**): `DOC102 docstring-extraneous-parameter` (preview since 0.14.1), `DOC201 docstring-missing-returns` (0.5.6), `DOC501 docstring-missing-exception` (0.5.5); or standalone `pydoclint 0.9.1` over NumPy/Google/Sphinx styles | that a documented section corresponds to a fact in the code | only *explicitly raised* exceptions; anything a callee raises stays undocumented. Preview status means codes may move (§2.5) |
| **truth** | **nothing** | - | **contract-only, permanently.** Nothing verifies the preconditions paragraph, the side-effect sentence or the calling restriction PEP 257 demands. Those become runtime contracts (`python_typing_contract_manifest.md` §5) or they are unverified |

`DOC501` is the mechanical enforcement of the `Raises:` mandate PEP 257 states and
`error_tracing_contract_manifest.md` relies on - the strongest argument for enabling preview here,
and it must be enabled with `lint.explicit-preview-rules = true`. Coverage-gate wiring is
`python_quality_gates_manifest.md`'s.

### 15.3 doctest: executable documentation, not a test suite

**ESTABLISHED.** `python -m doctest file [-v] [-o OPTION] [-f]` (runs `testmod()` for `.py`,
`testfile()` otherwise); `doctest.testmod()` / `testfile()` return `(failure_count, test_count)`;
unittest integration is `DocTestSuite`/`DocFileSuite`. The brittleness is documented, not folklore:
"doctest is serious about requiring exact matches in expected output. If even a single character
doesn't match, the test fails." Expected output cannot contain an all-whitespace line - use
`<BLANKLINE>`; hard tabs expand to 8-column stops; set and dict ordering is not guaranteed; float
output varies because "Python defers to the platform C library for some floating-point
calculations"; the default `repr()` embeds an address and needs `+ELLIPSIS`. Flags include
`ELLIPSIS`, `NORMALIZE_WHITESPACE`, `SKIP`, `IGNORE_EXCEPTION_DETAIL`, `FAIL_FAST`, `REPORT_NDIFF`,
`REPORT_ONLY_FIRST_FAILURE`, with directive syntax `# doctest: +FLAG, +FLAG2`. In exception examples
the traceback *stack* is ignored, so `...` in place of the frames is the idiom - and
**`IGNORE_EXCEPTION_DETAIL` matches only the exception type**, ignoring message and module
qualification, so a doctest can keep passing while the error message it documents rots. The docs
state their own limit - "Filling your docstrings with obscure test cases makes for bad
documentation" and "Regression testing is best confined to dedicated objects or files". Route:
**test-catchable for the examples only**; `python_testing_tooling_manifest.md` owns the real suite.

**One interpreter consequence, ESTABLISHED:** `-O` removes `assert` statements and code conditional
on `__debug__`; **`-OO` additionally discards docstrings.** A docstring contract is absent under
`-OO`, doctests cannot run there, and any `assert`-expressed invariant vanishes under `-O`. If
anything reads `__doc__` at runtime - an `argparse` help text, a plugin description - run the suite
once under `-OO` in CI; no linter models this. It is also exactly why `S101` must be enforced in
`src` and exempted only in the test tree (§4.2).

---

## 16. Named anti-patterns: the name, the source, the route

**ESTABLISHED.** "Code smell" is Fowler's (bliki, 9 February 2006) - "A code smell is a surface
indication that usually corresponds to a deeper problem in the system" - and he credits **Kent
Beck** with coining the term. Every entry names a published source; where the naming source is weak
the entry says so.

| anti-pattern | named by | route | mechanism |
|---|---|---|---|
| **God object / The Blob** | "The Blob" in *AntiPatterns* (Brown, Malveau, McCormick, Mowbray; Wiley 1998); earlier "god class/object" attributed to Riel (1996) - **FLAGGED-SECONDARY**, bibliographic record verified, neither book read | lint (proxy) | `PLR0904 too-many-public-methods` (**preview**, default 20); pylint `R0904`, `R0902`. A 19-method god object passes |
| **Long Function** | Fowler, *Refactoring* 2nd ed. (2018) | lint (proxy) + contract-only | `C901`, `lint.pylint.max-statements`; remedy **Extract Function** (§11.1) |
| **Long Parameter List** | Fowler | lint | `PLR0913`, `PLR0917`; remedies **Introduce Parameter Object**, **Preserve Whole Object** (§11.2) |
| **Flag Argument** | Fowler, bliki, 23 June 2011 | lint (boolean subset only) | `FBT001`-`FBT003`; remedy **Remove Flag Argument**. A `str`/`Enum` mode switch is invisible to every linter - contract-only |
| **The boolean trap** | Adam Johnson, "How to Avoid 'The Boolean Trap'", cited on ruff's `FBT001` page | lint | `FBT001`-`FBT003` (§11.3) |
| **Primitive Obsession** | Fowler | type | `NewType`, `Enum`, `Literal` (§14.3) |
| **Data Clumps** | Fowler | contract-only | **Introduce Parameter Object**; `PLR0913` sees the count, never the clump |
| **Data Class** (all data, no behaviour) | Fowler | contract-only | nothing; naming the smell is the whole mechanism |
| **Global Data / Mutable Data** | Fowler | lint | `PLW0603 global-statement` ("global mutable state is a common source of bugs and confusing behavior"), `RUF012`, `B006`, `B008` (both tunable via `lint.flake8-bugbear.extend-immutable-calls`); pylint `W0102`, `W0603`, `W0602`. **Residual: a module-level mutable mutated *without* `global` - `CACHE[k] = v` - is flagged by nothing** |
| **Refused Bequest** (inheritance where composition was meant) | Fowler | contract-only + type (partial) | remedy **Replace Superclass with Delegate** (catalog alias "Replace Inheritance with Delegation"); `typing.override` (PEP 698, 3.12) catches the two *refactor* failure modes - an orphaned override and a subclass method that silently becomes one - and PEP 698 cites "several production outages in multiple typed codebases caused by such incorrect refactors". Depth is not the defect; pylint `R0901` is a weak proxy. **The `__override__ = True` runtime attribute is best-effort only** - do not build on it |
| **Shotgun Surgery / Divergent Change** | Fowler | fitness (proxy) | `import-linter` contracts to keep the change surface inside a boundary; pylint `R0801` as a weak proxy. "One change, N files" is measured by nothing |
| **Feature Envy** | Fowler | contract-only | remedy **Move Function**; pylint `W0212` catches only underscore access - dataclass field access is public and invisible |
| **Stringly typed** | FOLDOC, crediting **Mark Simpson**; popularised via The Daily WTF - **FLAGGED-SECONDARY**, a dictionary entry is the strongest naming source found | type | `Enum`/`StrEnum`/`Literal` at the boundary; `LiteralString` (3.11) where injection is the risk. **`StrEnum` members compare equal to plain strings, so old call sites keep working** (§14.2) |
| **Exception as control flow** | practitioner vocabulary; the rules carry their own rationale | lint | `TRY300 try-consider-else` ("The `try`-`except` statement has an `else` clause for code that should run only if no exceptions were raised"), `TRY301`, `BLE001`; pylint `W0718`, `W0719`. `TRY300` is a shape rule, not a semantics rule |
| **Catch-log-rethrow** | **no primary or standards source names it** - **FLAGGED-SECONDARY**, practitioner literature only | contract-only (+1 fragment) | `TRY400 error-instead-of-exception` ("`logging.exception` logs the exception and the traceback, while `logging.error` only logs the exception"); **nothing detects the duplication itself**. Policy is `error_tracing_contract_manifest.md`'s |
| **The "utils" module** | **no citable authority exists** - **FLAGGED-SECONDARY / OPEN**; the argument (no cohesion criterion -> unrelated code accumulates -> a dependency bottleneck -> a breeding ground for circular imports) appears only in practitioner essays | contract-only + fitness | a naming ban in review plus an `import-linter` `independence`/`layers` contract. **No rule code exists** |
| **`staticmethod` as a namespace** | Google guide: "**Never use `staticmethod`** unless forced to in order to integrate with an API defined in an existing library. Write a module-level function instead." | lint (preview) + contract-only | `PLR6301 no-self-use` ("Unused `self` parameters are usually a sign of a method that could be replaced by a function, class method, or static method"), **preview**, exempting `@staticmethod`, `@classmethod` and `@typing.override` - the last specifically to avoid pushing a Liskov violation |
| **`classmethod` as a factory grab-bag** | Google guide: use it "**only** when writing a named constructor, or a class-specific routine that modifies necessary global state such as a process-wide cache" | contract-only | **no rule code exists** |
| **Mutable default argument** | Google guide ("Default arguments are evaluated once at module load time"); Fowler's Mutable Data | lint | `B006` (fix **unsafe** - §5.2); pylint `W0102` |
| **`assert` as validation** | Google guide: `assert` "must not be critical to the application logic" and must not validate preconditions (pytest asserts excepted) | lint | `S101`, exempted in the test tree only (§4.2, §15.3) |
| **Over-complex comprehension** | Google guide forbids "multiple `for` clauses or filter expressions" | contract-only | no rule counts comprehension nesting (§13.1) |
| **"Power features"** (metaclasses, bytecode access, `__del__`, reflection) | Google guide forbids them outright | contract-only | individual hazards are `python_language_hazards_manifest.md`'s; the *prohibition* is a review rule |
| **Comment drifted from the code** | Fowler lists **Comments** as a smell | contract-only (+2 fragments) | doctest for examples; `ERA001 commented-out-code` for the dead-code subset (highest false-positive rate in the set). **Prose comments cannot be checked, ever - the honest floor of this rung** |

**FLAGGED-SECONDARY on the smell enumeration.** The 24-item Fowler list (Mysterious Name, Duplicated
Code, Long Function, Long Parameter List, Global Data, Mutable Data, Divergent Change, Shotgun
Surgery, Feature Envy, Data Clumps, Primitive Obsession, Repeated Switches, Loops, Lazy Element,
Speculative Generality, Temporary Field, Message Chains, Middle Man, Insider Trading, Large Class,
Alternative Classes with Different Interfaces, Data Class, Refused Bequest, Comments) was assembled
from secondary summaries; Fowler's own 2nd-edition page gives *refactoring* names and does not
enumerate the smells. Quote the name and the work, never a sentence.

**Honest limits of half two.** Roughly a third of the routes in §11-§16 terminate in
`contract-only`, and several lint-routed rows are *proxies* - a statement count standing in for
cohesion, an ancestor count for a bad inheritance relation. Single responsibility, feature envy,
shotgun surgery, "utils", catch-log-rethrow, comment drift, comprehension complexity, purity and the
`classmethod` rule have **no mechanical enforcement at all**. That is the state of the art, not a
gap in this file. **The recommended rule set is a judgement, not a measurement:** no study
establishes that any ruff family reduces defect density. The defensible claim is narrower - these
rules encode hazards the type system provably cannot express, and a mechanised rule outlives the
reviewer who would otherwise have to remember it.

---

## Anti-patterns checklist

Reject on sight. Each names the section it violates - which is where its tag and its citation live;
the design-level anti-patterns are in §16.

- **No explicit `lint.select`** - the standard is whatever the pinned version defaults to (§2.1).
- **An unpinned ruff or a range specifier** - "safe fix", "default set" and "preview" are
  version-bound (§2.1, §5.1).
- **`select = ["E", "F"]` written as a tightening** - it discards ~400 default rules (§2.3).
- **A code in `select` no one verified with `ruff rule`** - a removed code either warns and enables
  a successor you never chose, or aborts the run outright (§3.2).
- **A `select` that drops a default-on family** - `select` replaces, so the families you forget to
  list are families you switched off; `ASYNC` is the one that costs most (§2.3, §3.2, §4.3).
- **`target-version` above the `requires-python` floor** - `UP` fixes then emit syntax that is a
  `SyntaxError` on the floor you publish (§2.4, hub §3e).
- **A preview rule selected by prefix without `preview = true`** - it never runs and ruff says
  nothing; selected by exact code it warns, which a green CI step still swallows (§2.5).
- **`preview = true` with `select = ["ALL"]` and no `explicit-preview-rules`** - 138 unstable rules
  enter by accident (§2.5).
- **`--unsafe-fixes` in a hook, in CI, or tree-wide** - it changes semantics behind harmless-looking
  diffs (§5.2, §5.3).
- **An accepted `B905` autofix** - `strict=False` satisfies the rule and keeps the silent truncation
  (§5.2, §13.2).
- **`TC001`-`TC003` enabled with empty `runtime-evaluated-*` lists** - the autofix can break a model
  at runtime (§5.2).
- **`D203` enabled alongside the formatter** - a non-terminating loop between two subcommands; only
  `ruff format` warns about it, and a lint-only CI step never runs that subcommand (§6.1).
- **`E501` enabled alongside a formatter** - permanent unfixable findings on lines the formatter
  left long (§6.1).
- **`ANN001`/`ANN201` next to mypy `--strict`** - every missing annotation reported twice (§6.2).
- **`lint.pydocstyle.convention` left at `null`** - ruff resolves the `D` conflicts for you (§6.3).
- **A convention-disabled `D` code re-added via `extend-select`** - it re-enables the rule the
  convention silenced (§6.3).
- **A bare `# noqa`, or `# type: ignore` with no code** - invisible unless `PGH004` /
  `ignore-without-code` are on (§8.2).
- **A suppression with no stated reason** - permitted by every tool, prohibited here (§8.4).
- **`# ruff: disable[...]` blocks without `RUF103` + `RUF104`** - an unterminated block suppresses
  the file tail (§8.2).
- **A global `ignore = ["S101"]`** - re-permits assert-as-validation in production, which vanishes
  under `-O` (§4.2).
- **A suppression census compared across two ruff versions** - meaningless without an identical pin
  and `select` (§8.5).
- **A proposal to write a ruff plugin** - the extension point does not exist (§10.2).
- **pylint added "for completeness"** - `mypy --strict` already finds its inference wins (§9).
- **A line-length debate in review** - the formatter ended it; only the configured number exists
  (§7).
- **A `bool` in a positional parameter** - a bare `*` or an `Enum` fixes it (§11.3).
- **`X | None` added to silence `RET503`/`R1710`** - it silences the tool and keeps the design flaw
  (§11.4).
- **Work at import time - I/O, network, a config read, a registry mutation** - only a budget test
  sees it (§12.4).
- **"Fixing" `PLC0415`, or the deferred import, unilaterally** - the project must have recorded
  which wins (§12.4).
- **`--fix` run broadly over `__init__.py`** - removing an "unused" import narrows the public
  interface (§12.1).
- **A re-export spelled `from x import y`** - only `from x import y as y` or an `__all__` entry
  counts (§12.2).
- **A claim that the underscore makes something private** - it excludes the name from `import *`,
  nothing else (§12.2).
- **A bare name in a `match` case used as a constant** - it is a capture pattern and always matches
  (§13.7).
- **A `match` over a closed domain with no `case _: assert_never(x)`** - no diagnostic at any level
  (§13.7).
- **`case [x]:` expected to match a string** - `str`/`bytes`/`bytearray` are excluded by spec
  (§13.7).
- **`lru_cache`/`cache` on a method, or over anything impure** - the cache retains `self`; impurity
  is unchecked (§13.6).
- **A blanket "modernise to f-strings" pass** - it deoptimises every logging call (§13.4).
- **`asdict()` in a hot path or a log call** - it `deepcopy`s every non-container field (§14.1).
- **A `@dataclass(slots=True)` captured by a registry before decoration** - the decorator returns a
  different class (§14.1).
- **`Annotated[str, Doc("...")]` as per-parameter documentation** - PEP 727 is withdrawn (§15.1).
- **A docstring that restates the signature** - PEP 257 reserves that form for C functions (§15.1).
- **doctest used as the regression suite** - the docs confine regression testing to dedicated files
  (§15.3).

---

## Open questions to resolve before building

Each is a decision the project must make and record, per `software_spec_discipline_manifest.md` §G5.

1. **OPEN - the `select` list itself, and who owns it.** §4.3 is a recommendation, not a finding.
   Adopt or amend it, commit it, name a reviewer for future changes, and decide whether the
   committed `ruff rule --all` baseline diff is advisory or blocking (mechanism:
   `python_quality_gates_manifest.md`).
2. **OPEN - exception messages at the raise site or in the exception class?** `TRY003` plus
   `EM101`-`EM103` push every message into a custom class, which many teams reject as ceremony.
   Genuinely contested; interacts with `error_tracing_contract_manifest.md`.
3. **OPEN - one recorded decision per contested family:** `TRY300`, `TRY301`, `ERA001`, `ARG*`,
   `FBT*`, `RET504`-`RET508`, `PLR2004`, and the `D1xx` "everything needs a docstring" rules. An
   inherited default is not a decision. §4.3 now takes a position on each of these in `select` or
   `ignore` with the reason inline; the project's job is to **ratify or amend** that position, not
   to leave the family unmentioned - an unmentioned contested family is the same defect as an
   inherited default.
4. **OPEN - the docstring convention value** (`"google"`/`"numpy"`/`"pep257"`), remembering the
   setting is subtractive and that the three disable lists are materially different, not variations
   on one theme - `"pep257"` leaves 29 stable `D` rules running, `"google"` 34, `"numpy"` 37, and
   they disagree about `D400`/`D401`/`D415`/`D107` (§6.3, measured table); and, if numpydoc,
   **whether types already in annotations are repeated** - Google says omit, numpydoc is silent.
5. **OPEN - `PLC0415` versus "no work at import time".** These cannot both be satisfied; decide
   which wins and how the exceptions the rule itself legitimises are marked (§12.4).
6. **OPEN - is `preview` enabled to obtain `DOC201`/`DOC501`/`DOC102`?** They are the only
   mechanical enforcement of a documented `Raises:`/`Returns:`, and they are unstable. If yes, set
   `lint.explicit-preview-rules = true` and pin ruff exactly (§2.5, §15.2).
7. **OPEN - the suppression form, and whether a reason is mandatory.** `# noqa: CODE` today, or `#
   ruff: ignore[CODE] <reason>` (the form ruff is migrating toward)? If reasons are mandatory the
   check lands on day one (§8.1, §8.4).
8. **OPEN - does pylint run at all?** If not, choose the substitute for `R0401 cyclic-import`
   (`import-linter`, or a pytest over the experimental `ruff analyze graph` JSON) and accept that
   `R0801 duplicate-code` has none (§9).
9. **OPEN - does `PLR0913` count keyword-only parameters?** The rule page does not say, and it
   decides whether the bare-`*` remedy satisfies the rule. Verify against the pinned ruff and record
   it (§11.2).
10. **OPEN - formatter choice and line length.** `ruff format` (recommended - one binary, one
    config) or `black`; and the number, given PEP 8's 79, Google's 80 and ruff's 88 (§7). **black
    26.5.1's release date could not be established**, so a black adoption should re-verify it.
11. **OPEN - the test-naming convention.** The only citable source is the Google guide's
    `test_<method_under_test>_<state>`; pin it, or something else, in
    `python_testing_tooling_manifest.md` (§12.3).
12. **OPEN - if pyright is used instead of or alongside mypy**, `reportUnnecessaryTypeIgnoreComment`
    must be turned on by hand: it is `"none"` in **every** mode including strict, so a pyright-only
    project has no stale-ignore signal. **No pyright version was pinned this session** (§8.3).
13. **OPEN - a project-specific rule beyond `TID251`:** which rung of the §10.3 ladder? A semgrep
    adoption must first confirm semgrep's version, licence tier, and whether taint mode is in the
    open-source CLI - none of which was verified here.
14. **OPEN - the `__all__`-validation codes and a `SIM` code for the `dict.get` idiom.** The
    families exist; the exact codes were not verified and are deliberately absent from §4.3 (§12.2,
    §13.1).

**Codes and claims deliberately quarantined as unverified**, recorded so a later author does not
mistake absence for oversight: the ruff codes for `too-many-branches` and
`too-many-return-statements` (the settings keys and pylint `R0912`/`R0911` are verified, the ruff
codes are not); the ruff `PL` codes for invalid-`__all__`-format and invalid-`__all__`-object, and
the pyflakes undefined-name-in-`__all__` code; any `SIM` code for `dict.get`/`setdefault`; the ruff
codes for the dataclass mutable-default and dataclass-call-default rules (the language-level
`ValueError` and `RUF012` are verified, the `RUF0xx` dataclass pairings are not); a ruff code for
`PLW0602` (only pylint `W0602` is asserted); whether pylint's `no-self-use` (`R6301`) still requires
the `pylint.extensions.no_self_use` extension; the code-to-name pairings for `C400`, `C404`, `C416`,
`C417`, `SIM103`, `SIM110` (families confirmed, pairings read from an index that mis-paired other
rows); numpydoc's validation check codes (they belong to `python_quality_gates_manifest.md`);
black 26.5.1's release date; pyright's version; semgrep's version and licence
tier; the ruff plugin-system status beyond the FAQ sentence; the CPython `typing` docs wording for
`assert_never`; and any quotation of Beck's Composed Method or of Fowler's smell list.

---

## Sources (accessed 8 Aug 2026)

- ruff 0.16.2 released 2026-08-07 - https://pypi.org/project/ruff/ . Accessed 8 Aug 2026.
- ruff 0.16.0, released 2026-07-23: "Ruff now enables 413 rules by default, up from 59 in previous
  versions"; the default set "was last modified in v0.1.0"; the 18 removed codes; `# ruff:
  ignore[...]`, `# ruff: disable[]`/`enable[]`, `# ruff: file-ignore[...]`; `--add-ignore` and rule
  names under preview; fixes shown as diffs; the nullable-JSON break; the 12 stabilised rules;
  Markdown code-block formatting - https://astral.sh/blog/ruff-v0.16.0 , confirmed independently at
  https://github.com/astral-sh/ruff/releases/tag/0.16.0 . Accessed 8 Aug 2026.
- ruff CHANGELOG: 0.16.2 dated 2026-08-06; 0.16.1 (2026-07-30) reclassified `PT022` and `FURB105`
  fixes unsafe and `PT018` safe - https://raw.githubusercontent.com/astral-sh/ruff/main/CHANGELOG.md
  . Accessed 8 Aug 2026.
- ruff linter docs - `select`/`extend-select`/`ignore` semantics and resolution priority; the
  safe-versus-unsafe fix definitions and the `RUF015` example; `--fix`, `--unsafe-fixes`,
  `lint.extend-safe-fixes`/`extend-unsafe-fixes`; all three suppression scopes;
  `--add-noqa`/`--add-ignore`; `RUF100`; exit codes 0/1/2, `--exit-zero`, `--exit-non-zero-on-fix` -
  https://docs.astral.sh/ruff/linter/ . Accessed 8 Aug 2026.
- ruff rules index - the prefix-to-upstream-tool table for all 59 families; "Ruff supports over 900
  lint rules" - https://docs.astral.sh/ruff/rules/ . Accessed 8 Aug 2026.
- ruff default-rules page - the default `select` is a list of individual codes, with the exact
  isort/pydocstyle/bandit/pycodestyle entries (`I001`; `D419`; `S102`, `S110`, `S112`; `E722`,
  `E902`, `W605`), and the `LOG` entries being exactly `LOG001`, `LOG002`, `LOG009`, `LOG014`,
  `LOG015` - `LOG004` is absent - https://docs.astral.sh/ruff/default-rules/ . Accessed 8 Aug 2026.
- ruff formatter docs - "drop-in replacement for Black"; "> 99.9% of lines are formatted
  identically" on Django and Zulip; the formatter-conflicting list (`W191`, `E111`, `E114`, `E117`,
  `D206`, `D300`, `D203`, `Q000`-`Q004`, `COM812`, `COM819`, `ISC002`, `E501`) and the conflicting
  isort settings; the `E501` best-effort caveat; "When an incompatible lint rule or setting is
  enabled, `ruff format` will emit a warning"; `ISC002` listed only "when used without `ISC001` and
  `flake8-implicit-str-concat.allow-multiline = false`"; the f-string and fluent-chain deviations;
  `# fmt: off`/`on`/`skip` - https://docs.astral.sh/ruff/formatter/ . Accessed 8 Aug 2026.
- ruff FAQ - "Ruff does not yet support third-party plugins, though a plugin system is within-scope
  for the project" (issue #283); "Ruff does not support custom lint rules"; "Pylint does more type
  inference than Ruff (e.g., Pylint can validate the number of arguments in a function call)" -
  https://docs.astral.sh/ruff/faq/ . Accessed 8 Aug 2026.
- ruff preview docs - "If a rule is marked as preview, it can only be selected if preview mode is
  enabled"; `explicit-preview-rules` - https://docs.astral.sh/ruff/preview/ . Accessed 8 Aug 2026.
- ruff settings reference - every default quoted in §2.4, §4.3, §6.3 and §11.1, including
  `target-version` "The minimum Python version to target ... Ruff will not propose changes using
  features that are not available in the given version", its default `"py310"`, the recommendation
  to use `project.requires-python` instead, and `requires-python = ">=3.8"` being treated as
  equivalent to `target-version = "py38"` (with `target-version` winning if both are given);
  `lint.pydocstyle.convention` `null` - the per-convention disable lists in §6.3 are stated from
  measurement of the pinned binary rather than from this page, because a prose list is exactly what
  went stale; the `lint.pylint.*` and `lint.mccabe` thresholds, `lint.dummy-variable-rgx`,
  `lint.task-tags`, `lint.logger-objects`, `lint.flake8-bandit.check-typed-exception`, the
  `flake8-type-checking` exemption lists, and the absence of `max-nested-blocks` -
  https://docs.astral.sh/ruff/settings/ . Accessed 8 Aug 2026.
- ruff configuration docs - `pyproject.toml` versus `ruff.toml` precedence, `extend` inheritance and
  "closest config wins", `target-version` inference from `requires-python`, the flag and subcommand
  lists
  - https://docs.astral.sh/ruff/configuration/ . Accessed 8 Aug 2026.
- ruff versioning policy - what MINOR and PATCH bumps may change, and "Ruff does not yet have a
  stable API" - https://docs.astral.sh/ruff/versioning/ . Accessed 8 Aug 2026.
- Individual ruff rule pages at `https://docs.astral.sh/ruff/rules/<slug>/`, each verified for its
  code-to-name pairing, default status, fix grading or quoted rationale: `mutable-argument-default`
  (B006), `function-call-in-default-argument` (B008), `cached-instance-method` (B019),
  `zip-without-explicit-strict` (B905), `boolean-type-hint-positional-argument` (FBT001),
  `boolean-default-value-positional-argument` (FBT002), `boolean-positional-value-in-call` (FBT003),
  `too-many-arguments` (PLR0913), `too-many-positional-arguments` (PLR0917),
  `too-many-public-methods` (PLR0904), `complex-structure` (C901), `magic-value-comparison`
  (PLR2004), `implicit-return` (RET503), `superfluous-else-return` (RET505),
  `if-else-block-instead-of-if-exp` (SIM108), `global-statement` (PLW0603), `mutable-class-default`
  (RUF012), `unsorted-dunder-all` (RUF022), `unused-import` (F401), `import-outside-top-level`
  (PLC0415), `os-path-join` (PTH118), `builtin-open` (PTH123), `try-consider-else` (TRY300),
  `raise-vanilla-args` (TRY003), `error-instead-of-exception` (TRY400), `no-self-use` (PLR6301),
  `any-type` (ANN401), `undocumented-public-function` (D103), `docstring-missing-returns` (DOC201),
  `docstring-missing-exception` (DOC501), `docstring-extraneous-parameter` (DOC102),
  `incorrect-blank-line-before-class` (D203), `blanket-type-ignore` (PGH003), `blanket-noqa`
  (PGH004), `redirected-noqa` (RUF101), `invalid-rule-code` (RUF102), `invalid-suppression-comment`
  (RUF103), `unmatched-suppression-comment` (RUF104). Accessed 8 Aug 2026.
- MEASURED with `uvx ruff@0.16.2`, 2026-08-08: `ruff linter` (59 families); `ruff rule --all
  --output-format json` (968 rules; 830 stable / 138 preview; fix availability 494 none / 251 always
  / 223 sometimes; every code, name, fix grading and preview status quoted above); `ruff check
  --isolated --show-settings` (413 default rules and their prefix distribution, `linter.line_length
  = 88`, `unsafe_fixes = hint`, `linter.preview = disabled`, `formatter.quote_style = double`,
  `formatter.docstring_code_format = disabled`); `ruff check --help` / `ruff format --help`; `ruff
  rule D211`; the `RUF015` safe-versus-unsafe walkthrough; the `D203`/`ruff format` ping-pong; the
  absence of any formatter-conflict warning; the `D203`/`D211` and `D212`/`D213` warnings appearing
  only when `convention` is unset; `noqa` and `ruff: ignore` behaviour with `PGH004`, `RUF100`
  (`non-enabled` versus `unused`) and `RUF102` plus `lint.external`; and the working `TID251
  banned-api` configuration for `datetime.datetime.utcnow`.
- MEASURED with `uvx --from pylint==4.0.6 pylint` and `uvx mypy` (2.3.0), 2026-08-08: the
  three-defect probe (`W0221`/`E1101`/`E1120`/`W0612` from pylint;
  `[override]`/`[attr-defined]`/`[call-arg]`/ `[no-untyped-def]`/`[no-untyped-call]` from `mypy
  --strict`; nothing from `ruff check --select ALL`) and the two-module cycle (`R0401` from pylint
  only).
- pylint 4.0.6 released 2026-06-14, requires Python >=3.10, supports 3.10-3.14; astroid inference
  with the `import logging as argparse` example and the quoted "killer feature ... despite how
  painfully slow it is" - https://pypi.org/project/pylint/ . Accessed 8 Aug 2026.
- pylint message overview - the C/R/W/E/F/I categories and every pylint code-to-name pairing used
  here - https://pylint.readthedocs.io/en/latest/user_guide/messages/messages_overview.html ;
  `useless-suppression`/`I0021` disabled by default, enabled via `enable`, failed on via
  `--fail-on=I0021` -
  https://pylint.readthedocs.io/en/stable/user_guide/messages/information/useless-suppression.html ;
  plugins via `load-plugins`, with AST/token/raw checker kinds and astroid inference -
  https://pylint.readthedocs.io/en/latest/development_guide/how_tos/plugins.html . Accessed 8 Aug
  2026.
- mypy - `--warn-unused-ignores`, `--warn-redundant-casts`, `--disallow-untyped-defs`,
  `--disallow-any-explicit`, `--no-implicit-reexport` and its two accepted spellings,
  `--enable-error-code`, and the exact 13-flag composition of `--strict` -
  https://mypy.readthedocs.io/en/stable/command_line.html ; the optional error codes including
  `ignore-without-code` ("Warn when a `# type: ignore` comment does not specify any error codes") -
  https://mypy.readthedocs.io/en/stable/error_code_list2.html . Accessed 8 Aug 2026.
- pyright (repository `main`, **no version pinned**) - `enableTypeIgnoreComments` true in all four
  modes; `reportUnnecessaryTypeIgnoreComment` "none" in off/basic/standard/strict;
  `reportPrivateUsage` "error" only in strict -
  https://raw.githubusercontent.com/microsoft/pyright/main/docs/configuration.md . Accessed 8 Aug
  2026.
- black 26.5.1 - Python 3.10+, a written Stability Policy, the 2026 stable style in 26.1.0 and 2025
  in 25.1.0, "you should not expect large formatting changes in the future"; the page shows no
  release date and https://pypi.org/pypi/black/json returned an implausible timestamp, recorded as
  OPEN - https://pypi.org/project/black/ . Accessed 8 Aug 2026.
- flake8 7.3.0 released 2025-06-20, requires Python >=3.9, "extendable through flake8.extension and
  flake8.formatting entry points" - https://pypi.org/project/flake8/ . Accessed 8 Aug 2026.
- semgrep rule syntax - `id`, `pattern`, `patterns`, `pattern-either`, `pattern-not`,
  `metavariable-pattern`, `languages`, `severity`, `message`, `fix`, `--pattern`/`-e`, and taint
  mode with `pattern-sources`/`pattern-sinks`; version and licence tier not confirmed -
  https://docs.semgrep.dev/writing-rules/pattern-syntax . Accessed 8 Aug 2026.
- PEP 8 - Status Active / Type Process; the foolish-consistency escape hatches and "do not break
  backwards compatibility just to comply with this PEP!"; the 79/72/99 line limits; the complete
  naming table; underscore and name-mangling semantics; the public-versus-internal doctrine and
  `__all__` - https://peps.python.org/pep-0008/ . Accessed 8 Aug 2026.
- PEP 257 - the docstring definition and `__doc__`; the one-line rules; the normative list of what a
  multi-line function docstring must document; the class/module/package/script rules; the refusal to
  mandate markup - https://peps.python.org/pep-0257/ . Accessed 8 Aug 2026.
- The remaining PEPs, each for the facts attributed to it above: PEP 20 (Active/Informational, no
  normative force) https://peps.python.org/pep-0020/ ; PEP 3102 (keyword-only)
  https://peps.python.org/pep-3102/ ; PEP 570 (`/` positional-only and its four motivations)
  https://peps.python.org/pep-0570/ ; PEP 572 (the walrus prohibition list, comprehension binding,
  the restraint advice) https://peps.python.org/pep-0572/ ; PEP 616 (`removeprefix`/`removesuffix`
  and the `lstrip` character-set confusion) https://peps.python.org/pep-0616/ ; PEP 618 (`zip`
  truncation and `strict=True`) https://peps.python.org/pep-0618/ ; PEP 634 (capture versus value
  patterns, `_`, sequence-pattern exclusion of `str`/`bytes`/`bytearray`, mapping partiality,
  `__match_args__`, guards, no fallthrough, no error when nothing matches)
  https://peps.python.org/pep-0634/ ; PEP 698 (`@override`, the two refactor failure modes,
  best-effort `__override__`) https://peps.python.org/pep-0698/ ; PEP 727 **Withdrawn** ("mostly
  negative ... verbosity and readability") https://peps.python.org/pep-0727/ . All accessed 8 Aug
  2026.
- Google Python Style Guide - the 80-column limit; the docstring mandate criteria and
  `Args:`/`Returns:`/`Raises:`; types need not be repeated when annotated; the mutable-default,
  comprehension, power-features, mutable-global-state and `assert` prohibitions; "Never use
  `staticmethod` unless forced to" and the `classmethod` restriction; the public/internal naming
  table; `test_<method_under_test>_<state>` - https://google.github.io/styleguide/pyguide.html .
  Accessed 8 Aug 2026.
- numpydoc - the 15 ordered sections, `name : type` formatting, the optional/default/brace
  conventions, `Raises` "used judiciously", Examples as doctest, and its silence on annotations -
  https://numpydoc.readthedocs.io/en/latest/format.html . Accessed 8 Aug 2026.
- CPython library and command-line docs, each for the behaviour quoted in §13-§15: `functools`
  (cache retention, `self` in the key, the impure-function warning, `cached_property`'s `__dict__`
  requirement, the PEP 412 note, the 3.12 lock removal)
  https://docs.python.org/3/library/functools.html ; `dataclasses` (parameter defaults, `slots=True`
  returning a new class, hashability-based mutable-default rejection, `KW_ONLY`, `asdict`
  deep-copying) https://docs.python.org/3/library/dataclasses.html ; `enum` (`StrEnum`/`IntEnum`
  value semantics, `Number.THREE == 3`, drop-in-replacement positioning, `@unique`/`@verify`)
  https://docs.python.org/3/library/enum.html ; `itertools` (`tee` storage and thread-unsafety,
  `product` consumption, `cycle` storage, `groupby` sortedness, `batched(strict=)`)
  https://docs.python.org/3/library/itertools.html ; `contextlib` (single-use `@contextmanager`, the
  must-reraise rule, reentrancy versus thread safety)
  https://docs.python.org/3/library/contextlib.html ; `pathlib` ("not a drop-in replacement", the
  enumerated differences, the "Corresponding tools" table)
  https://docs.python.org/3/library/pathlib.html ; `doctest` (exact-match strictness, `<BLANKLINE>`,
  the flake sources, the flag list, `IGNORE_EXCEPTION_DETAIL`, the Soapbox position)
  https://docs.python.org/3/library/doctest.html ; `typing` (`NewType` runtime behaviour and the
  3.10/3.11 performance notes; the page truncated before the `assert_never` entry)
  https://docs.python.org/3/library/typing.html ; and `-X importtime` / `-X importtime=2`,
  `PYTHONPROFILEIMPORTTIME`, `-O` removing asserts, `-OO` discarding docstrings -
  https://docs.python.org/3/using/cmdline.html . All accessed 8 Aug 2026.
- The typing spec's `@override` rule, describing only the static requirement and mentioning no
  runtime attribute - https://typing.python.org/en/latest/spec/class-compat.html . Accessed 8 Aug
  2026.
- pydoclint 0.9.1 (2026-07-03), NumPy/Google/Sphinx styles, `DOC` prefix -
  https://pypi.org/project/pydoclint/ ; interrogate 1.7.0 (2024-04-07), `--fail-under` default 80.0,
  the ignore flags, the pre-commit hook, presence-only checking -
  https://interrogate.readthedocs.io/ . Accessed 8 Aug 2026.
- import-linter 2.7 contract types `forbidden`, `layers` (with `exhaustive`), `independence`,
  `protected`, `acyclic_siblings` - named only to point at `python_module_boundaries_manifest.md`,
  which owns them - https://import-linter.readthedocs.io/en/v2.7/contract_types.html . Accessed 8
  Aug 2026.
- Fowler - "A code smell is a surface indication that usually corresponds to a deeper problem in the
  system", credited to Kent Beck, 9 Feb 2006 https://martinfowler.com/bliki/CodeSmell.html ; the
  Flag Argument definition, "My general reaction to flag arguments is to avoid them", and its three
  nuances, 23 June 2011 https://martinfowler.com/bliki/FlagArgument.html ; the refactoring names
  used above, verbatim from the *Refactoring* 2nd ed. catalog including the "Replace Inheritance
  with Delegation" alias https://refactoring.com/catalog/ and
  https://refactoring.com/catalog/replaceNestedConditionalWithGuardClauses.html ; and the
  2nd-edition page, which gives refactoring names and does **not** enumerate the smells
  https://martinfowler.com/articles/refactoring-2nd-ed.html . All accessed 8 Aug 2026.
- FLAGGED-SECONDARY naming sources, recorded so a later author does not mistake them for primary:
  the bibliographic record for *AntiPatterns* (Brown, Malveau, McCormick, Mowbray; Wiley 1998)
  naming "The Blob" and the attribution of "god object" to Riel (1996) -
  https://dl.acm.org/doi/10.5555/280487 and https://en.wikipedia.org/wiki/AntiPatterns ; "stringly
  typed" credited to Mark Simpson - https://foldoc.org/stringly+typed ; catch-log-rethrow -
  https://www.theserverside.com/tip/Troubleshooting-Java-Code-Log-or-Re-Throw-but-Dont-Do-Both ; the
  "utils" module - https://breadcrumbscollector.tech/stop-naming-your-python-modules-utils/ and
  https://www.moderndescartes.com/essays/noutils/ . All accessed 8 Aug 2026.

### Sibling manifests (cross-referenced, not duplicated)

- `python_platform_baseline_manifest.md` - the single version anchor: CPython releases, support
  phases, EOL dates, PEP status, interpreter switches, minimum-target policy. This file states tool
  behaviour and cites the hub for *when*.
- `python_language_hazards_manifest.md` - the hazard diagnosis and the maximal-safety modern subset.
  Every code here that guards a language footgun exists because that file names the footgun.
- `python_typing_contract_manifest.md` - the typing vocabulary for data shapes (§2), `cast`/`Any`/
  `# type: ignore` discipline (§3), what the type system cannot express (§4), runtime contract
  libraries (§5), immutability and `Final` (§6), the docstring style menu (§7), and the checker flag
  lists.
- `python_quality_gates_manifest.md` - the ratchet and the wiring: which checks run where, hook ids,
  the CI matrix, exit-code handling, `--statistics` as a ratchet source, the committed
  rule-inventory diff, incremental adoption over a legacy tree, supply-chain gates and metrics. This
  file defines the rule set; that file makes it fail a build.
- `python_module_boundaries_manifest.md` - project layout, packaging metadata, the import system as
  a boundary, the public-API and deprecation contract, plugin seams, and machine enforcement of
  dependency direction (`import-linter`, `Tach`). It owns the cycle and layering checks this file
  can only proxy.
- `error_tracing_contract_manifest.md` - the error contract: propagation channels, chaining,
  exhaustiveness, custom hierarchies, `contextlib.suppress` as the only sanctioned silencing,
  message anatomy. This file supplies the `TRY`/`BLE`/`EM`/`B904` codes that mechanise it.
- `logging_observability_manifest.md` - the severity model, logger/handler/formatter architecture,
  library-versus-application discipline, structured logging, the lazy-argument stance. This file
  supplies `G001`-`G004`, `G101`, the `LOG` family, `TRY400` and `lint.logger-objects`.
- `python_testing_tooling_manifest.md` - test kinds, the double taxonomy, fixtures, property-based
  testing, test naming. It owns every route marked `test-catchable`, the `PT` family in practice,
  and the test-tree `per-file-ignores` carve-out.
- `python_runtime_diagnostics_manifest.md` - inspecting a running or crashed process, including the
  measurement side of `-X importtime` and of retained-object growth from a cache.
- `python_concurrency_determinism_manifest.md` - execution models, structured concurrency,
  cancellation, determinism under test. It owns the `cached_property` 3.12 lock removal and
  `itertools.tee` thread-unsafety as concurrency facts.
- `software_spec_discipline_manifest.md` - epistemic tagging, contracts as public API (G2), the open
  questions convention (§G5), reusability earned by boundaries (C2/C3), and the pure core /
  imperative shell (F1/F2) that the module-altitude practices implement.
- `architecture_manifest_default.md` - coupling and cohesion, state and ownership, interfaces and
  contracts, and the refactoring patterns adjacent to Fowler's vocabulary in §16.
