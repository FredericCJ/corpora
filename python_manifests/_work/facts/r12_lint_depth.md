# The pedantic linter stack for Python - fact pack (verified 2026-08-08)

**Scope.** The rule set and the division of labour between formatter, linter, type checker and test.
Gate wiring (pre-commit, CI matrix, ratchets) belongs to `python_quality_gates_manifest.md` and is out
of scope here except where a rule's semantics force a wiring decision.

**Evidence tiers used below.** `DOC` = a primary documentation/changelog/PyPI page loaded this session.
`MEASURED` = observed by executing the tool locally this session (`uvx ruff@0.16.2`, `uvx --from
pylint==4.0.6 pylint`, `uvx mypy`) on purpose-built probe files. MEASURED outranks DOC when they
disagree, and where they disagreed this pack says so.

## Version table

| thing | current version | released (ISO) | source URL | tag |
|---|---|---|---|---|
| ruff | 0.16.2 | 2026-08-07 (PyPI) / 2026-08-06 (CHANGELOG) | https://pypi.org/project/ruff/ ; https://raw.githubusercontent.com/astral-sh/ruff/main/CHANGELOG.md | VERSION-DEPENDENT (0.16.2) |
| ruff - the release that changed defaults | 0.16.0 | 2026-07-23 | https://astral.sh/blog/ruff-v0.16.0 | VERSION-DEPENDENT (0.16.0) |
| ruff total rule count | 968 rules (830 stable / 138 preview) | n/a | MEASURED: `ruff rule --all --output-format json` | VERSION-DEPENDENT (0.16.2) |
| ruff default-enabled rule count | 413 | n/a | MEASURED: `ruff check --isolated --show-settings` | VERSION-DEPENDENT (0.16.2) |
| ruff linter families | 59 prefixes | n/a | MEASURED: `ruff linter` | VERSION-DEPENDENT (0.16.2) |
| pylint | 4.0.6 | 2026-06-14 | https://pypi.org/project/pylint/ | VERSION-DEPENDENT (4.0.6) |
| astroid (pylint's inference engine) | 4.0.4 | OPEN (not separately confirmed) | MEASURED: `pylint --version` | VERSION-DEPENDENT (4.0.4) |
| mypy | 2.3.0 | OPEN (not separately confirmed) | MEASURED: `mypy --version` | VERSION-DEPENDENT (2.3.0) |
| black | 26.5.1 | OPEN - PyPI page shows no date; the JSON API answer was implausible (2024) and is rejected rather than repeated | https://pypi.org/project/black/ | VERSION-DEPENDENT (26.5.1) |
| black stable style | 2026 stable style, introduced in 26.1.0 | OPEN | https://pypi.org/project/black/ | VERSION-DEPENDENT (26.1.0) |
| flake8 | 7.3.0 | 2025-06-20 | https://pypi.org/project/flake8/ | VERSION-DEPENDENT (7.3.0) |
| pyright | OPEN - config semantics verified from `main` docs, version not pinned this session | n/a | https://raw.githubusercontent.com/microsoft/pyright/main/docs/configuration.md | OPEN |
| semgrep | OPEN - rule syntax verified, version and licence not confirmed | n/a | https://docs.semgrep.dev/writing-rules/pattern-syntax | OPEN |

## Facts

### Ruff: shape of the tool

1. `ruff linter` prints 59 rule families. Each maps to one upstream tool: `E`/`W` pycodestyle, `F`
   Pyflakes, `I` isort, `N` pep8-naming, `D` pydocstyle, `UP` pyupgrade, `ANN` flake8-annotations,
   `ASYNC` flake8-async, `S` flake8-bandit, `B` flake8-bugbear, `A` flake8-builtins, `C4`
   flake8-comprehensions, `DTZ` flake8-datetimez, `T20` flake8-print, `EM` flake8-errmsg, `FBT`
   flake8-boolean-trap, `ISC` flake8-implicit-str-concat, `ICN` flake8-import-conventions, `G`
   flake8-logging-format, `LOG` flake8-logging, `INP` flake8-no-pep420, `PIE` flake8-pie, `PT`
   flake8-pytest-style, `Q` flake8-quotes, `RET` flake8-return, `SIM` flake8-simplify, `TID`
   flake8-tidy-imports, `TC` flake8-type-checking, `ARG` flake8-unused-arguments, `PTH`
   flake8-use-pathlib, `ERA` eradicate, `PL` Pylint, `TRY` tryceratops, `FLY` flynt, `PERF` Perflint,
   `FURB` refurb, `RUF` Ruff-specific, `C90` mccabe, `PGH` pygrep-hooks, `SLF` flake8-self, `BLE`
   flake8-blind-except, `COM` flake8-commas, `DOC` pydoclint, `PYI` flake8-pyi, plus AIR, FAST, YTT,
   CPY, T10, DJ, EXE, FIX, FA, INT, RSE, SLOT, TD, NPY, PD - VERSION-DEPENDENT (0.16.2)
2. Ruff states "Ruff supports over 900 lint rules" on its rules index; the v0.16.0 blog states 968
   (up from 708). `ruff rule --all --output-format json` returns exactly 968 objects. Use 968 - DOC +
   MEASURED - VERSION-DEPENDENT (0.16.2)
3. Of the 968 rules, 830 are stable and 138 are preview-gated - MEASURED - VERSION-DEPENDENT (0.16.2)
4. Fix availability across all 968 rules: 494 "Fix is not available", 251 "Fix is always available",
   223 "Fix is sometimes available". Slightly under half of all rules are autofixable at all -
   MEASURED - VERSION-DEPENDENT (0.16.2)
5. `ruff rule --all --output-format json` emits, per rule: `code`, `name`, `linter`, `summary`,
   `explanation`, `message_formats`, `fix`, `fix_availability`, `preview`, `status`,
   `source_location`. This is the census primitive - a project can diff its enabled set against this
   file on every ruff bump - MEASURED - VERSION-DEPENDENT (0.16.2)
6. Rule codes are a 1-3 letter prefix plus three digits (Flake8's scheme). Selectors accept a full
   code or any prefix; `ALL` selects everything - DOC - ESTABLISHED

### Ruff 0.16.0 changed the default rule set - the single most consequential fact in this pack

7. Before 0.16.0 the default select was effectively `["E4", "E7", "E9", "F"]` = 59 rules. From 0.16.0
   the default is 413 rules. The blog gives `select = ["E4", "E7", "E9", "F"]` as the incantation to
   restore the old behaviour - DOC - VERSION-DEPENDENT (0.16.0)
8. 18 rules were *removed* from the default set in 0.16.0: `E401`, `E402`, `E701`, `E702`, `E703`,
   `E711`, `E712`, `E713`, `E714`, `E721`, `E731`, `E741`, `E742`, `E743`, `F403`, `F405`, `F406`,
   `F722` - DOC - VERSION-DEPENDENT (0.16.0)
9. Measured distribution of the 413 default rules by prefix: PYI 47, UP 42, F 39, RUF 36, PLE 33, B 29,
   SIM 21, PLW 20, C4 17, FURB 17, PLR 13, ASYNC 10, DTZ 10, YTT 10, PLC 8, PIE 8, PT 6, LOG 5, TRY 5,
   EXE 4, G 4, TC 4, PERF 3, S 3, INT 3, E 2, FA 2, PTH 2, BLE 1, D 1, I 1, ISC 1, N 1, PGH 1, RET 1,
   T 1, W 1, FLY 1 - MEASURED - VERSION-DEPENDENT (0.16.2)
10. Rules a coding agent will assume are on but which are **NOT** in the 413-rule default set
    (measured individually): `E501`, `G001`, `G002`, `G003`, `G004`, `S101`, `B904`, `B905`, `TRY300`,
    `TRY301`, `TRY400`, `PGH003`, `PGH004`, `RUF102`, `RUF103`, `RUF104`, all `ANN*`, all `D*` except
    `D419`, `T201`, `EM101`, `ARG001`, `PTH123`, `ERA001`, `PLR0913`, `C901`, `N802`, `TC001`-`TC003`,
    `FBT001`, `SIM105`, `RET504`, `PERF401`, `COM812`, `ISC001`, `Q000` - MEASURED - VERSION-DEPENDENT
    (0.16.2)
11. Rules that **ARE** on by default and that carry real semantic weight: `E722` bare-except, `BLE001`
    blind-except, `S110` try-except-pass, `S112` try-except-continue, `S102` exec-builtin, `B006`
    mutable-argument-default, `B008` function-call-in-default-argument, `B023`
    function-uses-loop-variable, all ten DTZ rules, `TRY002`, `TRY004`, `TRY201`, `TRY203`, `TRY401`,
    `LOG001`, `LOG002`, `LOG009`, `LOG014`, `LOG015`, `G010`, `G101`, `G201`, `G202`, `I001`
    unsorted-imports, `RUF100` unused-noqa, `RUF101` redirected-noqa - MEASURED - VERSION-DEPENDENT
    (0.16.2)
12. `lint.select` **replaces** the default set; `lint.extend-select` **adds** to whatever is already
    selected. Writing `select = ["E", "F"]` therefore silently drops the other 400-odd defaults. The
    docs recommend `lint.select` for explicitness - DOC - ESTABLISHED
13. Defaults for selection settings: `lint.select` = see Default Rules; `lint.ignore` = `[]`;
    `lint.extend-select` = `[]`; `lint.per-file-ignores` = `{}`; `lint.fixable` = `["ALL"]`;
    `lint.unfixable` = `[]`; `lint.extend-safe-fixes` = `[]`; `lint.extend-unsafe-fixes` = `[]`;
    `lint.external` = `[]` - DOC - VERSION-DEPENDENT (0.16.2)
14. `line-length` default is `88`. Resolved settings show `linter.line_length = 88` and
    `linter.pycodestyle.max_line_length = 88` - DOC + MEASURED - VERSION-DEPENDENT (0.16.2)
15. `target-version` default is `"py310"`; when a config file is discovered on the filesystem, Ruff
    infers a missing `target-version` from `requires-python` in a `pyproject.toml` **in the same
    directory as the found config**. A config passed directly via `--config` is not auto-inferred.
    `--target-version` accepts py37..py315 - DOC + MEASURED - VERSION-DEPENDENT (0.16.2)
16. Config lives in `[tool.ruff]`, `[tool.ruff.lint]`, `[tool.ruff.format]` in `pyproject.toml`, or in
    `ruff.toml`/`.ruff.toml` with the `[tool.ruff]` header dropped (`[lint]`, `[format]`). Precedence
    in one directory: `.ruff.toml` > `ruff.toml` > `pyproject.toml`. Ruff uses the *closest* config
    and ignores ancestors unless `extend` is used - DOC - ESTABLISHED

### Fix safety - exact semantics

17. Safe fixes "preserve runtime behavior" and only remove comments when deleting the statement they
    attach to. Unsafe fixes may change behaviour or incidentally remove comments - DOC - ESTABLISHED
18. Only safe fixes are applied by default. Resolved settings show `unsafe_fixes = hint` - Ruff
    *reports* that a hidden fix exists but will not apply it - MEASURED - VERSION-DEPENDENT (0.16.2)
19. The flags are `--fix` / `--no-fix`, `--unsafe-fixes` / `--no-unsafe-fixes`, `--fix-only` (implies
    `--fix`), `--diff` (implies `--fix-only`, writes nothing, exits 0 when no diffs), `--show-fixes`.
    The config equivalent is `unsafe-fixes`. Per-rule reclassification is
    `lint.extend-safe-fixes` / `lint.extend-unsafe-fixes`, both of which accept prefixes -
    DOC + MEASURED (`ruff check --help`) - VERSION-DEPENDENT (0.16.2)
20. Worked example, MEASURED. `return list(xs)[0]` under `--select RUF015`: plain `--fix` leaves the
    file untouched and prints `No fixes available (1 hidden fix can be enabled with the
    --unsafe-fixes option).` Adding `--unsafe-fixes --fix` rewrites it to `return next(iter(xs))`.
    That rewrite changes the exception raised on an empty input from `IndexError` to `StopIteration` -
    a behaviour change that no test which only exercises the happy path will detect - DOC + MEASURED -
    VERSION-DEPENDENT (0.16.2)
21. `TRY400`'s fix is *conditionally* safe: safe for `logging.error`, unsafe for other logger-like
    calls, because Ruff cannot prove the receiver is a `logging.Logger` - DOC - VERSION-DEPENDENT
    (0.16.2)
22. Fix safety is reclassified between releases. In 0.16.1 `PT022` fixes became unsafe, `FURB105`
    fixes that remove unknown separators became unsafe, and `PT018` fixes became safe by default
    (unsafe only when comments are present). A pinned ruff version is therefore part of the fix
    contract, not a convenience - DOC - VERSION-DEPENDENT (0.16.1)
23. Among the 413 default rules: 198 have no fix, 116 always have one, 99 sometimes do - MEASURED -
    VERSION-DEPENDENT (0.16.2)

### Preview mode

24. Preview is enabled by `--preview` / `--no-preview`, or `preview = true` under `[tool.ruff.lint]`
    or `[tool.ruff.format]`. Resolved defaults: `linter.preview = disabled`,
    `formatter.preview = disabled`, `analyze.preview = disabled`,
    `linter.explicit_preview_rules = false` - DOC + MEASURED - VERSION-DEPENDENT (0.16.2)
25. A preview rule cannot be selected at all while preview is off - not by exact code, not by prefix,
    not by `ALL`. Selecting it is silently ineffective - DOC - ESTABLISHED
26. With `lint.explicit-preview-rules = true`, prefix selection stops pulling in preview rules; only
    exact codes do. This is the setting that makes `select = ["ALL"]` plus preview survivable - DOC -
    VERSION-DEPENDENT (0.16.2)
27. Preview promotion is a real churn source: 0.16.0 stabilised 12 rules - `AIR303`, `CPY001`,
    `FURB164`, `FURB192`, `ISC004`, `LOG004`, `PLE0304`, `PLR0917`, `PLR1708`, `RUF036`, `RUF063`,
    `RUF068` - and widened detection in `BLE001`, `FA102`, `INT001`-`INT003`, `S310`, `S508`, `S509`,
    `UP019` - DOC - VERSION-DEPENDENT (0.16.0)
28. Notable rules still preview-gated in 0.16.2: `E111`, `E114`, `E117` (indentation), `DOC201`
    docstring-missing-returns, `DOC501` docstring-missing-exception, `FURB101`, `RUF105`, `RUF106` -
    MEASURED - VERSION-DEPENDENT (0.16.2)

### Suppression comments - the full mechanism

29. Three suppression scopes exist. (a) line-level `# noqa` / `# noqa: F401`, and since 0.16.0 the
    equivalent `# ruff: ignore[F401]` at end of line or on the preceding line. (b) range-level
    `# ruff: disable[N803]` ... `# ruff: enable[N803]`, own-line comments whose codes, order and
    indentation must match. (c) file-level `# ruff: noqa`, `# ruff: noqa: F841`, or
    `# ruff: file-ignore[F401] Allow unused imports in this file`. Ruff also honours Flake8's
    `# flake8: noqa` - DOC - VERSION-DEPENDENT (0.16.0)
30. `# ruff: ignore[F401]` genuinely suppresses the diagnostic - MEASURED (an unused `import re`
    carrying it produced no `F401`) - VERSION-DEPENDENT (0.16.2)
31. `noqa` matching is per-code and non-transitive: `import io  # noqa: E501` does **not** suppress
    `F401` on that line - MEASURED - ESTABLISHED
32. The suppression-hygiene rule family, with exact codes, names, fix availability and default status
    (all MEASURED via `ruff rule --all`): `RUF100` unused-noqa (fix Always, **default-on**); `RUF101`
    redirected-noqa (fix Always, **default-on**); `RUF102` invalid-rule-code (fix Always, off);
    `RUF103` invalid-suppression-comment (fix Always, off); `RUF104` unmatched-suppression-comment (no
    fix, off); `RUF028` invalid-formatter-suppression-comment (fix Always, default-on); `PGH003`
    blanket-type-ignore (no fix, off); `PGH004` blanket-noqa (fix Sometimes, off) - VERSION-DEPENDENT
    (0.16.2)
33. `RUF100` reports two distinguishable states, and the wording matters operationally. With `E501`
    *not* selected: `Unused 'noqa' directive (non-enabled: 'E501')`. With `E501` selected but not
    triggered: `Unused 'noqa' directive (unused: 'E501')`. The first is a configuration smell, the
    second is dead debt - MEASURED - VERSION-DEPENDENT (0.16.2)
34. `RUF102` on an unknown code emits two help lines: "Add non-Ruff rule codes to the `lint.external`
    configuration option" and "Remove the rule code". Setting `lint.external = ["ABC"]` suppresses
    `RUF102` for `ABC123` - MEASURED. This is the mechanism for coexisting with a non-Ruff checker
    that writes its own `noqa` codes - VERSION-DEPENDENT (0.16.2)
35. `PGH004` fires on a bare `# noqa` with message "Use specific rule codes when using `noqa`", and
    only when explicitly selected - MEASURED - VERSION-DEPENDENT (0.16.2)
36. Ruff is steering away from `noqa`. Two preview rules encode the intended end state: `RUF105`
    noqa-comments - "`noqa` comment used instead of `ruff: ignore`" (fix Sometimes), and `RUF106`
    rule-codes-in-suppression-comments - "Rule code used instead of name in suppression comment" (fix
    Always). Both preview since 0.15.22. Under `--preview`, `--add-ignore` writes rule *names* rather
    than codes - MEASURED + DOC - VERSION-DEPENDENT (0.16.2)
37. `--add-noqa[=<REASON>]` and `--add-ignore[=<REASON>]` bulk-insert suppressions and optionally
    append a free-text reason after the codes - DOC + MEASURED (`ruff check --help`) -
    VERSION-DEPENDENT (0.16.2)
38. **No ruff rule requires a reason on a suppression.** Searching all 968 rule explanations for a
    rule that mandates justification text returns nothing. `--add-*=<REASON>` can write one; nothing
    checks that one is present - MEASURED - VERSION-DEPENDENT (0.16.2)
39. `--ignore-noqa` makes ruff disregard every `# noqa` in the tree. This is the census flag: the
    delta between a normal run and an `--ignore-noqa --statistics` run is the exact size of the
    suppression debt - DOC + MEASURED - VERSION-DEPENDENT (0.16.2)
40. `--statistics` prints a count per triggered rule with code and name, one per line, tab-separated -
    MEASURED. Combined with `--output-format json` (also: concise, full, json-lines, junit, grouped,
    github, gitlab, pylint, rdjson, azure, sarif) this is the ratchet's data source -
    VERSION-DEPENDENT (0.16.2)
41. Exit codes: `0` clean or fully fixed, `1` violations remain, `2` abnormal termination (bad config
    or CLI). `--exit-zero` forces 0 except for 2; `--exit-non-zero-on-fix` returns 1 when files were
    modified even though nothing remains - DOC + MEASURED - ESTABLISHED

### Type-checker-side suppression

42. mypy: `--warn-unused-ignores` reports a `# type: ignore` on a line that generates no error, and
    `--warn-redundant-casts` reports removable casts. Both are inside `--strict` - DOC - ESTABLISHED
43. mypy `--strict` is exactly: `--disallow-any-generics`, `--disallow-subclassing-any`,
    `--disallow-untyped-calls`, `--disallow-untyped-defs`, `--disallow-incomplete-defs`,
    `--check-untyped-defs`, `--disallow-untyped-decorators`, `--warn-redundant-casts`,
    `--warn-unused-ignores`, `--warn-return-any`, `--no-implicit-reexport`, `--strict-equality`,
    `--extra-checks` - DOC - VERSION-DEPENDENT (mypy 2.3.0)
44. mypy's `ignore-without-code` optional error code "Warn when a `# type: ignore` comment does not
    specify any error codes." It is **not** in `--strict`; enable it via
    `--enable-error-code ignore-without-code`, `enable_error_code =` in config, or
    `# mypy: enable-error-code="ignore-without-code"` inline. This is the mypy analogue of `PGH003`,
    and it is the stronger of the two because it is checker-aware rather than textual - DOC -
    ESTABLISHED
45. Other mypy optional codes worth the manifest's attention: `redundant-expr`, `truthy-bool`,
    `truthy-iterable`, `possibly-undefined`, `explicit-override`, `mutable-override`,
    `exhaustive-match`, `deprecated`, `unused-awaitable`, `unimported-reveal` - DOC -
    VERSION-DEPENDENT (mypy 2.3.0)
46. pyright: `enableTypeIgnoreComments` defaults to `true` in off/basic/standard/strict - pyright
    honours PEP 484 `# type: ignore`. `# pyright: ignore` comments are unaffected by that switch.
    `reportUnnecessaryTypeIgnoreComment` defaults to `"none"` in **all four** modes, including
    strict - so pyright does *not* detect stale ignores unless you turn it on by hand - DOC -
    VERSION-DEPENDENT (pyright main)
47. pyright strict does enable `reportUnnecessaryIsInstance`, `reportUnnecessaryCast`,
    `reportUnnecessaryComparison`, `reportUnusedImport`, `reportPrivateUsage`,
    `reportUnknownMemberType` (all `"error"` in strict, `"none"` in off/basic/standard).
    `reportUnusedCallResult` and `reportImplicitOverride` are `"none"` even in strict - DOC -
    VERSION-DEPENDENT (pyright main)
48. pylint's own analogue is `useless-suppression` / `I0021`, **disabled by default**; enable by adding
    `useless-suppression` to `enable`, and make it fail the build with `--fail-on=I0021` or
    `--fail-on=I` - DOC - VERSION-DEPENDENT (4.0.6)

### Pylint: what inference actually still buys - measured, not assumed

49. Pylint infers values through astroid: its own page gives `import logging as argparse` followed by
    `argparse.error(...)` as an example where it knows the call is a logging call. A quoted user calls
    inference "the killer feature that keeps us using [pylint] in our project despite how painfully
    slow it is" - DOC - ESTABLISHED
50. Ruff's FAQ concedes the gap: "Pylint implements many rules that Ruff does not, and vice versa. For
    example, Pylint does more type inference than Ruff (e.g., Pylint can validate the number of
    arguments in a function call)." Ruff has **not** closed this - DOC - VERSION-DEPENDENT (0.16.2)
51. MEASURED head-to-head on a probe with an incompatible override, a bogus attribute and a
    missing-argument call. `ruff check --select ALL` reported only `ANN001`, `ANN201`, `CPY001`,
    `D100`-`D103`, `F841` - it caught **none** of the three real defects. `pylint 4.0.6` reported
    `W0221` arguments-differ, `E1101` no-member ("Instance of 'str' has no 'nosuchmethod' member"),
    `E1120` no-value-for-parameter, `W0612` unused-variable - VERSION-DEPENDENT (ruff 0.16.2 /
    pylint 4.0.6)
52. **The finding that reframes the pylint question.** On the *same untyped* probe, `mypy --strict`
    reported `[override] Signature of "run" incompatible with supertype "Base"`,
    `[attr-defined] "str" has no attribute "nosuchmethod"`, and `[call-arg] Missing positional
    argument "b" in call to "run"` - all three of pylint's inference wins, plus
    `[no-untyped-def]`/`[no-untyped-call]`. On a fully annotated version it still caught
    `[attr-defined]` and `[call-arg]`. For a strictly-typed project, pylint's inference advantage over
    *ruff* is real but its advantage over *the stack* is largely redundant - MEASURED -
    VERSION-DEPENDENT (mypy 2.3.0)
53. **The genuine, measured residue is import cycles.** On a two-module cycle (`pkg.a` imports
    `pkg.b`, `pkg.b` imports `pkg.a`): `mypy --strict -p pkg` printed "Success: no issues found in 3
    source files"; `ruff check --select ALL` reported only `CPY001`/`D100`/`D103`/`D104`; `pylint`
    reported `R0401: Cyclic import (pkg.a -> pkg.b)`. No ruff rule and no type checker reports the
    cycle - MEASURED - VERSION-DEPENDENT (ruff 0.16.2 / mypy 2.3.0 / pylint 4.0.6)
54. `ruff analyze graph <path>` emits a JSON adjacency map of module -> imported modules, prefixed by
    `warning: 'ruff analyze graph' is experimental and may change without warning`. It does not
    detect cycles, but the map is a legitimate input to a project-owned cycle test - MEASURED -
    VERSION-DEPENDENT (0.16.2)
55. Pylint's second unique capability is `duplicate-code` / `R0801`, cross-file clone detection. Ruff
    has no equivalent - DOC - VERSION-DEPENDENT (4.0.6)
56. Pylint message categories: `C` convention, `R` refactor, `W` warning, `E` error, `F` fatal, `I`
    information. Verified code/name pairs: `E1101` no-member, `W0221` arguments-differ, `W0237`
    arguments-renamed, `R0401` cyclic-import, `R0913` too-many-arguments, `R0801` duplicate-code,
    `W0611` unused-import, `C0103` invalid-name, `C0116` missing-function-docstring, `I0021`
    useless-suppression, `E0012` bad-option-value, `E1120` no-value-for-parameter, `E1121`
    too-many-function-args, `E1136` unsubscriptable-object, `E1102` not-callable - DOC -
    VERSION-DEPENDENT (4.0.6)
57. Pylint 4.0.6 requires Python >= 3.10 and supports 3.10-3.14 on CPython and PyPy - DOC -
    VERSION-DEPENDENT (4.0.6)
58. The honest cost of pylint: its own docs quote the slowness rather than deny it, and running it
    means a second rule vocabulary, a second config file, a second suppression syntax
    (`# pylint: disable=`), a second unused-suppression audit (`I0021`) and a second set of
    false-positive fights - DOC - ESTABLISHED

### Formatter vs linter

59. Ruff's formatter is "designed as a drop-in replacement for Black", "adheres to Black's (stable)
    code style", and claims "> 99.9% of lines are formatted identically" when run over
    Black-formatted Django and Zulip. The docs do not name a specific target Black version - DOC -
    VERSION-DEPENDENT (0.16.2)
60. Documented deviations from Black: Ruff formats the expression parts inside f-string `{...}`
    braces; a "fluent layout" for method chains exists in preview - DOC - VERSION-DEPENDENT (0.16.2)
61. The formatter-conflicting rule list, verbatim from the formatter docs: `W191`, `E111`, `E114`,
    `E117`, `D203`, `D206`, `D300`, `Q000`, `Q001`, `Q002`, `Q003`, `Q004`, `COM812`, `COM819`,
    `ISC002`, `E501` - DOC - VERSION-DEPENDENT (0.16.2)
62. `D203`'s own rule page says outright: "We recommend against using this rule alongside the
    formatter. The formatter removes blank lines before class docstrings, which conflicts with this
    rule's requirement to include them." - DOC - VERSION-DEPENDENT (0.16.2)
63. MEASURED ping-pong. A class whose docstring immediately follows the `class` line, run with
    `--select D203 --fix`, gains a blank line before the docstring; `ruff format` immediately removes
    it; repeat forever. `D203`'s fix is "Fix is always available", so this is a genuine
    non-terminating loop between two subcommands of the same binary, and **neither command warns** -
    MEASURED - VERSION-DEPENDENT (0.16.2)
64. MEASURED: selecting `D203, ISC001, COM812, E501, W191, Q000` together with the formatter in play
    produces **no warning of any kind**. Ruff only warns about *mutually* incompatible lint rules, not
    about lint rules that fight the formatter - VERSION-DEPENDENT (0.16.2)
65. Formatter defaults, resolved: `formatter.indent_style = space`, `formatter.quote_style = double`,
    `formatter.nested_string_quote_style = alternating`, `formatter.docstring_code_format = disabled`,
    `formatter.docstring_code_line_width = dynamic` - MEASURED - VERSION-DEPENDENT (0.16.2)
66. `ruff format` flags include `--check`, `--diff`, `--range <RANGE>`, `--line-length`, `--preview`,
    `--respect-gitignore`. Suppression is `# fmt: off` / `# fmt: on` / `# fmt: skip` - DOC + MEASURED -
    VERSION-DEPENDENT (0.16.2)
67. From 0.16.0, `check` and `format --check` show fixes as diffs by default, and `format --check`
    supports every output format. Breaking JSON change: `filename`, `location`, `end_location` and
    `fix.edits[].location` may now be `null` - any CI script parsing ruff JSON must be re-checked -
    DOC - VERSION-DEPENDENT (0.16.0)
68. Black 26.5.1 requires Python 3.10+, is governed by a written Stability Policy, and ships a
    year-named stable style (2026 stable style in 26.1.0, 2025 in 25.1.0). "Now that we have become
    stable, you should not expect large formatting changes in the future." - DOC - VERSION-DEPENDENT
    (26.5.1)

### Docstrings, imports, naming

69. `lint.pydocstyle.convention` defaults to **`null`**. Allowed values: `"google"`, `"numpy"`,
    `"pep257"` - DOC - VERSION-DEPENDENT (0.16.2)
70. MEASURED consequence of that default: `--select D` with no convention prints
    `warning: 'incorrect-blank-line-before-class' (D203) and 'no-blank-line-before-class' (D211) are
    incompatible. Ignoring 'incorrect-blank-line-before-class'.` plus the same for `D212`/`D213`.
    Setting `convention = "google"` silences both warnings by disabling the conflicting members. Left
    at `null`, ruff silently picks a winner for you - VERSION-DEPENDENT (0.16.2)
71. `D203` canonical name is `incorrect-blank-line-before-class`; `D211` is `blank-line-before-class`
    per `ruff rule D211`. The incompatibility *warning text* spells D211 as
    `no-blank-line-before-class`. Reported as observed; the `ruff rule` output is treated as canonical
    - MEASURED (internal inconsistency) - VERSION-DEPENDENT (0.16.2)
72. Verified D codes: `D100` undocumented-public-module, `D101` undocumented-public-class, `D102`
    undocumented-public-method, `D103` undocumented-public-function, `D206`
    docstring-tab-indentation, `D212` multi-line-summary-first-line, `D213`
    multi-line-summary-second-line, `D300` triple-single-quotes, `D419` empty-docstring (the only D
    rule on by default) - MEASURED - VERSION-DEPENDENT (0.16.2)
73. Docstring *content* checking is a separate family: `DOC` (pydoclint), including `DOC201`
    docstring-missing-returns and `DOC501` docstring-missing-exception - both still preview. `DOC501`
    is the mechanical enforcement of "every public function documents its `Raises:`" - MEASURED -
    VERSION-DEPENDENT (0.16.2)
74. Import sorting is `I001` unsorted-imports (fix Sometimes, default-on) and `I002`
    missing-required-import (fix Always). isort settings live under `[tool.ruff.lint.isort]` -
    MEASURED + DOC - VERSION-DEPENDENT (0.16.2)
75. Naming is `N`: `N801` invalid-class-name, `N802` invalid-function-name, `N803`
    invalid-argument-name, `N806` non-lowercase-variable-in-function, `N818`
    error-suffix-on-exception-name. None have fixes; only `N999` invalid-module-name is on by default -
    MEASURED - VERSION-DEPENDENT (0.16.2)

### Extensibility - the honest answer

76. **Ruff cannot take custom rules today.** The FAQ: "Ruff does not yet support third-party plugins,
    though a plugin system is within-scope for the project", tracked as issue #283. The
    Flake8-comparison section repeats "Ruff does not support custom lint rules" - DOC -
    VERSION-DEPENDENT (0.16.2)
77. Plugin work is not underway. Ruff's own discussion #20652 records that as of September 2025 the
    maintainers had held design discussions but "haven't actively started any work on it" and were
    "still far from reaching consensus", deprioritised behind the type checker -
    FLAGGED-SECONDARY (search summary of a ruff discussion thread; thread not loaded directly) - OPEN
78. **The one project-specific rule ruff does offer is `TID251` banned-api.** MEASURED working config:
    `[lint.flake8-tidy-imports.banned-api]` with `"datetime.datetime.utcnow".msg = "Use
    datetime.now(tz=UTC) instead."` produced `TID251 'datetime.datetime.utcnow' is banned: Use
    datetime.now(tz=UTC) instead.` on `datetime.utcnow()`. It matches fully-qualified member paths,
    not just modules, and carries a custom message. This covers a large share of what teams actually
    write custom rules for - VERSION-DEPENDENT (0.16.2)
79. Flake8 7.3.0 remains "extendable through flake8.extension and flake8.formatting entry points" -
    the only mainstream Python linter with a working third-party plugin ecosystem. It requires Python
    >= 3.9 and its last release was 2025-06-20, i.e. over a year before this pack - DOC -
    VERSION-DEPENDENT (7.3.0)
80. Pylint plugins load via the `load-plugins` option; checkers are AST checkers, token checkers or
    raw checkers, and plugins get astroid inference. This is the option for a custom check that needs
    inferred types - DOC - VERSION-DEPENDENT (4.0.6)
81. Semgrep rules are written in YAML, not code: `id`, `pattern`, `patterns`, `pattern-either`,
    `pattern-not`, `metavariable-pattern`, `languages`, `severity`, `message`, `fix`, plus a
    `mode: taint` with `pattern-sources`/`pattern-sinks`. `--pattern`/`-e` runs a single pattern from
    the CLI. Metavariables unify *within* sources and *within* sinks but not *between* them by default
    - DOC. Licence/version/OSS-tier status not confirmed this session - OPEN
82. The realistic ladder for a project-specific AST check, in ascending cost: `TID251` ban-list ->
    semgrep YAML rule -> a `pytest` test that walks `ast.parse` over the package -> a `libcst`
    codemod/visitor -> a pylint plugin (only when inferred types are required) -> a flake8 plugin
    (only if a flake8 run already exists). Writing a ruff plugin is not on the ladder because the
    extension point does not exist - synthesis of facts 76-81 - VERSION-DEPENDENT (0.16.2)

### Exact codes for the hazards a type checker cannot catch

83. Mutable default: `B006` mutable-argument-default (fix Sometimes, default-on). Call in default:
    `B008` function-call-in-default-argument (no fix, default-on). Loop-variable capture: `B023`
    function-uses-loop-variable (no fix, default-on) - MEASURED - VERSION-DEPENDENT (0.16.2)
84. Bare and blind except: `E722` bare-except (no fix, default-on), `BLE001` blind-except (no fix,
    default-on), `S110` try-except-pass, `S112` try-except-continue (both default-on).
    `lint.flake8-bandit.check-typed-exception` (default `false`) controls whether `S110` also fires
    for typed exception clauses - MEASURED + DOC - VERSION-DEPENDENT (0.16.2)
85. Lost exception cause: `B904` raise-without-from-inside-except (no fix, **not** default-on) -
    MEASURED - VERSION-DEPENDENT (0.16.2)
86. Naive datetimes, all ten default-on and none with a fix: `DTZ001`
    call-datetime-without-tzinfo, `DTZ002` call-datetime-today, `DTZ003` call-datetime-utcnow,
    `DTZ004` call-datetime-utcfromtimestamp, `DTZ005` call-datetime-now-without-tzinfo, `DTZ006`
    call-datetime-fromtimestamp, `DTZ007` call-datetime-strptime-without-zone, `DTZ011`
    call-date-today, `DTZ012` call-date-fromtimestamp, `DTZ901` datetime-min-max - MEASURED + DOC -
    VERSION-DEPENDENT (0.16.2)
87. Assert in production: `S101` assert (no fix, not default-on). Tests must be exempted via
    `lint.per-file-ignores` - MEASURED - VERSION-DEPENDENT (0.16.2)
88. Logging call hazards, full `G` family: `G001` logging-string-format, `G002`
    logging-percent-format, `G003` logging-string-concat, `G004` logging-f-string (fix Sometimes),
    `G010` logging-warn (fix Always), `G101` logging-extra-attr-clash, `G201` logging-exc-info, `G202`
    logging-redundant-exc-info. Only `G010`, `G101`, `G201`, `G202` are default-on - the four that
    matter most for structured logging (`G001`-`G004`) are **off** - MEASURED + DOC -
    VERSION-DEPENDENT (0.16.2)
89. Logging API misuse, `LOG` family: `LOG001` direct-logger-instantiation, `LOG002`
    invalid-get-logger-argument, `LOG004` log-exception-outside-except-handler (fix Sometimes;
    stabilised in 0.16.0), `LOG007` exception-without-exc-info, `LOG009` undocumented-warn, `LOG014`
    exc-info-outside-except-handler, `LOG015` root-logger-call. `LOG001`, `LOG002`, `LOG009`,
    `LOG014`, `LOG015` are default-on. `lint.logger-objects` (default `[]`) tells ruff which project
    objects to treat as a `logging.Logger` - MEASURED + DOC - VERSION-DEPENDENT (0.16.2)
90. try/except antipatterns, full `TRY` family with default status: `TRY002` raise-vanilla-class (on),
    `TRY003` raise-vanilla-args (off), `TRY004` type-check-without-type-error (on), `TRY201`
    verbose-raise (fix Always, on), `TRY203` useless-try-except (on), `TRY300` try-consider-else
    (off), `TRY301` raise-within-try (off), `TRY400` error-instead-of-exception (fix Sometimes, off),
    `TRY401` verbose-log-message (on). `TRY200` reraise-no-cause was **removed** in v0.2.0 - selecting
    it is dead configuration - MEASURED - VERSION-DEPENDENT (0.16.2)
91. Other removed/dead codes a stale config may still carry: `PGH001` eval, `PGH002`
    deprecated-log-warn (both removed v0.2.0), `PT004` pytest-missing-fixture-name-underscore
    (removed). `RUF102`+`RUF101` are how you find these in `noqa` comments; nothing flags them in
    `select` lists - MEASURED - VERSION-DEPENDENT (0.16.2)
92. `TC` family and its runtime hazard: `TC001` typing-only-first-party-import, `TC002`
    typing-only-third-party-import, `TC003` typing-only-standard-library-import (all fix Sometimes,
    all off by default), `TC004` runtime-import-in-type-checking-block, `TC005`
    empty-type-checking-block, `TC006` runtime-cast-value, `TC007` unquoted-type-alias, `TC010`
    runtime-string-union. `TC004`, `TC005`, `TC007`, `TC010` are default-on. The escape hatches for
    runtime-introspected classes are `lint.flake8-type-checking.runtime-evaluated-base-classes` and
    `runtime-evaluated-decorators`, both defaulting to `[]` - MEASURED + DOC - VERSION-DEPENDENT
    (0.16.2)
93. Budget rules and their defaults: `lint.mccabe.max-complexity` = `10` (rule `C901`),
    `lint.pylint.max-args` = `5` (rule `PLR0913` too-many-arguments), plus `PLR0917`
    too-many-positional-arguments (stabilised 0.16.0). `C901` and `PLR0913` are **not** default-on -
    DOC + MEASURED - VERSION-DEPENDENT (0.16.2)
94. `lint.dummy-variable-rgx` defaults to `"^(_+|(_+[a-zA-Z0-9_]*[a-zA-Z0-9]+?))$"` - this is what
    makes `_`-prefixed names exempt from unused-variable rules, and it is the knob for `ARG*`
    friction. `lint.task-tags` defaults to `["TODO", "FIXME", "XXX"]` - DOC - VERSION-DEPENDENT
    (0.16.2)

## The routing table

| hazard / practice | why it bites | enforcement route | exact mechanism (rule code / flag / checker / test kind) | residual risk |
|---|---|---|---|---|
| Mutable default argument | the default object is created once at `def` time and shared by every call | lint-catchable | `B006` mutable-argument-default (default-on; fix Sometimes, unsafe - it rewrites the body) | the type checker sees a perfectly well-typed `list[int]`; only the linter sees the sharing |
| Callable evaluated in a default | `def f(t=now())` freezes one value for the process lifetime | lint-catchable | `B008` function-call-in-default-argument (default-on, no fix) | DI frameworks legitimately do this; the exemption needs a coded `noqa` that someone reviews |
| Closure captures the loop variable | every closure sees the final value | lint-catchable | `B023` function-uses-loop-variable (default-on, no fix) | flags some correct code that consumes the closure immediately |
| `except:` | swallows `KeyboardInterrupt` and `SystemExit` | lint-catchable | `E722` bare-except (default-on, no fix) | writing `except BaseException:` explicitly satisfies E722 while keeping the hazard |
| `except Exception:` as control flow | hides programming errors as if they were expected failures | lint-catchable | `BLE001` blind-except (default-on, no fix) | a top-level process boundary genuinely needs one; that single site must carry a coded, reasoned suppression |
| Silently swallowed exception | failure leaves no trace at all | lint-catchable | `S110` try-except-pass, `S112` try-except-continue (both default-on); widen with `lint.flake8-bandit.check-typed-exception = true` | `except X: logger.debug(...)` passes both rules and is still effectively silent - contract-only beyond this point |
| Exception chain broken on re-raise | the traceback loses the original cause | lint-catchable | `B904` raise-without-from-inside-except - **must be selected**, not default-on | no autofix; nothing detects a *wrong* `from` target |
| Handler that only re-raises | dead code pretending to be error handling | lint-catchable | `TRY203` useless-try-except (default-on), `TRY201` verbose-raise (default-on, fix Always) | none material |
| `return` inside `try` | the return value can be overridden by `except`/`finally`, or an exception silently suppressed | lint-catchable | `TRY300` try-consider-else - must be selected, no fix | contested: fires on a lot of idiomatic code; enable deliberately or not at all |
| `raise` deep inside a large `try` | the raise is caught by its own handler | lint-catchable | `TRY301` raise-within-try - must be selected, no fix | high false-positive rate; the most commonly disabled TRY rule |
| `logging.error` where the traceback is needed | the stack trace is lost at the exact moment it is needed | lint-catchable | `TRY400` error-instead-of-exception - must be selected; fix safe for `logging.error`, unsafe for other logger-like receivers | ruff cannot prove a custom object is a Logger; set `lint.logger-objects` |
| `.exception()` outside an except block | logs `NoneType: None` instead of a traceback | lint-catchable | `LOG004` log-exception-outside-except-handler (default-on since 0.16.0), `LOG014` exc-info-outside-except-handler (default-on) | none material |
| f-string / `%` / `.format` / `+` inside a logging call | formats eagerly even when the level is disabled, and destroys the structured-logging message key | lint-catchable | `G004` logging-f-string, `G001` logging-string-format, `G002` logging-percent-format, `G003` logging-string-concat - **none of the four is default-on**; all must be selected | `G004`'s fix is Sometimes-available and rewrites the call - read the diff; interacts with the lazy-args decision owned by `logging_observability_manifest.md` |
| `logger.warn()`, root-logger calls, hand-built Logger | deprecated API; a module-level `logging.info()` configures the root logger as a side effect | lint-catchable | `G010` logging-warn (fix Always), `LOG009` undocumented-warn, `LOG015` root-logger-call, `LOG001` direct-logger-instantiation, `LOG002` invalid-get-logger-argument - all default-on | none material |
| `extra=` key collides with a LogRecord attribute | raises at log time, in production, on the error path | lint-catchable | `G101` logging-extra-attr-clash (default-on, no fix) | detects literal dict keys only |
| Naive datetime | comparisons and arithmetic silently wrong across DST and zones | lint-catchable | all ten DTZ rules default-on: `DTZ001`-`DTZ007`, `DTZ011`, `DTZ012`, `DTZ901`; none has a fix | the rules catch *construction*, not later arithmetic between mismatched zones - that is test-catchable only |
| A deprecated `utcnow()`-style API used anywhere | one naive value poisons everything downstream | lint-catchable (project-specific) | `TID251` banned-api via `[lint.flake8-tidy-imports.banned-api]`, keyed on `"datetime.datetime.utcnow"` with a custom `msg` - verified working | matches fully-qualified paths only; aliasing through an intermediate name defeats it |
| `assert` used for validation | vanishes entirely under `python -O` | lint-catchable | `S101` assert - must be selected; tests exempted via `lint.per-file-ignores` | none, provided the exemption is scoped to the test tree and nothing else |
| Long line | unreviewable diffs | feature-eliminated by the formatter | `ruff format` with `line-length` (default `88`); `E501` line-too-long **must stay disabled** | a single unbreakable token (a URL, a long string) still overruns and no layer fixes it |
| Quote style, trailing commas, indentation, blank lines | endless review noise about nothing | feature-eliminated by the formatter | `ruff format`; disable `W191`, `E111`, `E114`, `E117`, `D203`, `D206`, `D300`, `Q000`-`Q004`, `COM812`, `COM819`, `ISC002`, `E501` per the formatter docs | ruff does **not** warn when you enable these anyway (measured) - the exclusion is config discipline, not a guard rail |
| Import order and grouping | merge conflicts, hidden duplicate imports | lint-catchable, autofixed | `I001` unsorted-imports (default-on, fix Sometimes), `I002` missing-required-import (fix Always) | `I001`'s fix is Sometimes-safe; it will not reorder across a `noqa`-bearing block |
| Legacy typing spellings (`List`, `Optional`, `Union`) | two vocabularies in one codebase | feature-eliminated by the language, enforced by lint | `UP006` non-pep585-annotation, `UP007` non-pep604-annotation-union, `UP045` non-pep604-annotation-optional, `UP035` deprecated-import - all default-on, all fix Sometimes | fixes are unsafe around `from __future__ import annotations` edge cases; state `target-version` explicitly rather than relying on inference |
| Missing annotations | implicit `Any` spreads silently | type-catchable (primary) | mypy `--disallow-untyped-defs` / `--disallow-incomplete-defs`, both inside `--strict` | `ANN*` duplicates this and reports it as lint noise - see the "disable" rows |
| `Any` as an escape hatch in a signature | defeats the checker at the boundary | lint-catchable (complementary) | `ANN401` any-type (no fix, must be selected) - flags `Any` on *arguments*, which mypy `--strict` alone permits | mypy's `--disallow-any-explicit` is the blunter checker-side alternative; pick one, not both |
| `print()` shipped to production | output bypasses the logging contract | lint-catchable | `T201` print, `T203` p-print - must be selected; fix Sometimes | CLI entry points need a scoped `per-file-ignores`, not a global disable |
| Boolean positional argument | `f(True)` is unreadable at the call site and silently reversible | lint-catchable | `FBT001` boolean-type-hint-positional-argument, `FBT002` boolean-default-value-positional-argument, `FBT003` boolean-positional-value-in-call - none default-on, none has a fix | the type checker accepts `f(True)` and `f(False)` identically; only the linter objects |
| Exception message built at the raise site | the exception class becomes non-reusable, messages drift | lint-catchable, contested | `EM101` raw-string-in-exception, `EM102` f-string-in-exception, `EM103` dot-format-in-exception (fix Sometimes); `TRY003` raise-vanilla-args (no fix) | genuinely contested - `TRY003` pushes every message into a custom class, which many teams reject as ceremony. Decide once, record the decision |
| Commented-out code | rots, misleads readers, hides intent | lint-catchable, noisy | `ERA001` commented-out-code (must be selected, no fix) | highest false-positive rate in the set; fires on prose comments that happen to parse |
| Function too complex / too many parameters | untestable unit | lint-catchable, threshold-based | `C901` with `lint.mccabe.max-complexity` (default `10`); `PLR0913` too-many-arguments with `lint.pylint.max-args` (default `5`); `PLR0917` too-many-positional-arguments | thresholds are conventions, not measurements; the rule cannot tell an essential 12-branch dispatch from accidental complexity |
| Reaching into another module's privates | couples to an implementation detail | lint-catchable | `SLF001` private-member-access (must be selected, no fix) | pyright strict's `reportPrivateUsage` (`"error"` in strict only) is the checker-side equivalent; running both doubles the noise |
| Import cycle | fragile import order, untestable modules, partial-initialisation bugs | fitness-function | **measured**: mypy `--strict` says "Success"; `ruff --select ALL` says nothing; `pylint` reports `R0401` cyclic-import. Either run pylint for `R0401`, or post-process `ruff analyze graph`'s JSON adjacency map in a CI test | `ruff analyze graph` self-declares as experimental; pylint costs a whole second toolchain. `import-linter`/`Tach` belong to `python_module_boundaries_manifest.md` |
| Wrong argument count, attribute that does not exist, incompatible override | crashes at runtime on a path the tests may not cover | type-catchable | **measured** mypy `--strict` on *untyped* code: `[call-arg]`, `[attr-defined]`, `[override]`. Pylint's `E1120`/`E1101`/`W0221` find the same three | ruff finds none of them; but for a strictly-typed project pylint here is largely redundant with mypy, which is the whole argument for not adding pylint |
| Copy-pasted logic across modules | divergent bug fixes | lint-catchable, pylint-only | `R0801` duplicate-code - no ruff equivalent exists | the only defect class in this table where pylint is the sole mechanical option |
| Blanket `# noqa` | suppresses every present and future diagnostic on that line | lint-catchable | `PGH004` blanket-noqa - must be selected; fix Sometimes | fixing it can surface new diagnostics, which is the point |
| Blanket `# type: ignore` | the same, for the type checker | lint-catchable + type-catchable | `PGH003` blanket-type-ignore (textual); mypy `--enable-error-code ignore-without-code` (checker-aware, **not** in `--strict`) | pyright has no equivalent requirement; a pyright-only project has no mechanism here |
| Stale `# noqa` accumulating | suppression debt becomes permanent and invisible | lint-catchable | `RUF100` unused-noqa (default-on, fix Always) - distinguishes `(unused: X)` from `(non-enabled: X)`; `RUF101` redirected-noqa (default-on); `RUF102` invalid-rule-code plus `lint.external` | `RUF100` cannot judge a code that is not enabled - a `noqa` for a rule you never turned on reports as `non-enabled`, not as wrong |
| Malformed or unterminated range suppression | silently suppresses a whole module tail | lint-catchable | `RUF103` invalid-suppression-comment (fix Always), `RUF104` unmatched-suppression-comment (no fix) - **neither is default-on** | if you adopt `# ruff: disable[...]` blocks you must select `RUF103`+`RUF104` in the same commit, or the feature is a footgun |
| Stale `# type: ignore` | hides a bug that has already been fixed elsewhere | type-catchable | mypy `--warn-unused-ignores` (inside `--strict`); pyright `reportUnnecessaryTypeIgnoreComment`, which is `"none"` in **every** mode including strict and must be set by hand | a pyright-only project that never sets this rule accumulates ignores with no signal at all |
| Stale `# pylint: disable=` | the same, in a third vocabulary | lint-catchable | pylint `useless-suppression` / `I0021`, disabled by default; add to `enable` and fail with `--fail-on=I0021` | only exists if pylint is in the stack at all |
| Suppression with no stated reason | future readers cannot tell whether it is still needed | **contract-only** | no ruff rule requires justification text (verified across all 968 rule explanations). `--add-noqa=<REASON>` / `--add-ignore=<REASON>` can *write* one; nothing checks presence. Mechanise with a semgrep rule or a regex test over the suppression form | a regex test is the only mechanical option, and it cannot judge whether the reason is *true* |
| Suppression count drifting upward | the standard quietly erodes | fitness-function | `ruff check --statistics` for triggered counts; `--ignore-noqa` for the true unsuppressed total; the delta is the debt. Ratchet on the delta in CI | gate wiring belongs to `python_quality_gates_manifest.md`; the numbers are only meaningful against a pinned ruff version |
| Rule set silently changing under you | a ruff upgrade adds or removes hundreds of rules | fitness-function | pin ruff exactly; check in `ruff rule --all --output-format json` as a baseline and diff it on every bump; `--show-settings` for the resolved enabled set | 0.16.0 moved the default from 59 to 413 rules - a project without an explicit `select` had its standard rewritten by an upgrade |
| Docstring convention drift | mixed Google/NumPy/reST in one tree | lint-catchable | the `D` family plus `lint.pydocstyle.convention` - **default is `null`**, which makes ruff pick a winner for the D203/D211 and D212/D213 conflicts and print a warning | choose `"google"`/`"numpy"`/`"pep257"` explicitly; `null` is not a neutral default |
| Undocumented `Raises:` on a public function | the error contract exists only in the code | lint-catchable, preview-gated | `DOC501` docstring-missing-exception (preview), `DOC201` docstring-missing-returns (preview) | preview-gated, so the whole preview surface comes with it unless `lint.explicit-preview-rules = true`; until then this is contract-only |
| Runtime-needed import hidden in `TYPE_CHECKING` | pydantic/dataclass/attrs classes fail at import time or lose validation | lint-catchable, needs configuration | `TC001`-`TC003` (off by default, fix Sometimes) move imports into `TYPE_CHECKING`; `lint.flake8-type-checking.runtime-evaluated-base-classes` and `runtime-evaluated-decorators` (both `[]` by default) exempt runtime-introspected classes; `TC004` runtime-import-in-type-checking-block (default-on) catches the resulting breakage | with the exemption lists empty, enabling `TC001`-`TC003` and autofixing can break a pydantic model at runtime. `TC004` catches it only after the fix has landed |
| Project-specific rule that no linter ships | the house convention has no teeth | lint-catchable (`TID251`) then fitness-function | `TID251` banned-api for banned symbols; otherwise a semgrep YAML rule, an `ast`-walking pytest, or a libcst visitor. **Ruff accepts no plugins** | every option outside `TID251` is a second tool with its own failure modes; a pytest AST walk is the cheapest and stays inside the existing gate |
| "We agreed on this in review" | advice that is not mechanised decays to zero | **contract-only** - say so | nothing | this row exists to be shrunk: anything left here is a candidate for the ladder in fact 82 |

## What the existing manifests already cover

Census method: `grep -c -iE "ruff|pylint|flake8|noqa"` over every file in `E:/dev/corpora/manifests/`.
Result: `logging_observability_manifest.md` 3 hits, `uml25_ocl_conformance_manifest.md` 2 hits, every
other file **0**. No existing manifest names a single ruff rule code. The linting layer is genuinely
absent, not merely thin.

- `python_typing_contract_manifest.md` §3 "Explicit conversion and cast discipline" - owns
  `typing.cast` having no runtime effect, `assert_type`, `reveal_type`, the sources of implicit `Any`,
  `--warn-redundant-casts`, `--strict-equality`, and the rule that a cast must sit on the smallest
  expression immediately after a real runtime check. **Do not restate any of this.** The delta this
  pack adds is `ANN401`, and the fact that `--warn-unused-ignores` has a linter-side counterpart
  (`RUF100`) and a blanket-form counterpart (`PGH003` plus mypy `ignore-without-code`).
- `python_typing_contract_manifest.md` §4 "What the type system CANNOT express" - owns value ranges,
  cross-field invariants, ordering/temporal constraints, units, typestate, and the
  `Literal`/`Enum`/`Annotated` partial mitigations. This is precisely the boundary this pack routes
  *to the linter*: §4 says the checker cannot see it, and this pack names which of those hazards a
  lint rule does catch (mutable defaults, naive datetimes, `assert` under `-O`, bare except) and which
  remain runtime contracts.
- `python_typing_contract_manifest.md` §7 "Contract documentation conventions" - already owns
  Google/NumPy/reST, PEP 257, PEP 287, "pick ONE style per project", `Raises:` as the canonical place
  for error modes, and doctest/icontract as machine-checkable forms. The delta is purely mechanical:
  the `D` family, `lint.pydocstyle.convention` and its `null` default, and `DOC501` as the enforcement
  of that manifest's `Raises:` mandate.
- `python_typing_contract_manifest.md` "Recommendations" Stage 1 and Stage 4 - already mandates pinning
  exact checker versions and literal flag lists rather than "use strict mode", and already treats
  `cast`/`# type: ignore`/`Any` as tracked debt gated by `--warn-redundant-casts`,
  `--warn-unused-ignores` and pyright `reportUnknown*`. The delta is the linter half of the same
  ratchet, and the pinning argument applied to ruff (fact 7: the default set moved by 354 rules in one
  minor release).
- `python_typing_contract_manifest.md` "Caveats" - already states that "Runtime tools enforce; the type
  system documents", that `assert` vanishes under `-O`, and that cross-checker conformance is
  empirical. The `S101` row in the routing table is the mechanical enforcement of the `-O` caveat.
- `logging_observability_manifest.md` (line ~376 and Open question 6 at line ~430) - already records
  that `%`-style lazy args "may be flagged or rewritten to f-strings" by mypy/pyright/ruff and asks
  the project to agree an explicit stance. It names ruff but **no rule code**. The delta is
  `G001`-`G004` with exact codes, the measured fact that none of the four is on by default, and the
  `TRY400` / `LOG004` / `LOG007` / `LOG014` / `G101` / `LOG015` set that manifest's guidance implies
  but never mechanises.
- `python_testing_tooling_manifest.md` - one incidental mypy mention (line ~147); owns test tooling.
  The delta needed from it: the `PT` family, and the `per-file-ignores` carve-out for `S101` in the
  test tree.
- `uml25_ocl_conformance_manifest.md` - mentions Pylint twice and black once as example tooling in a
  conformance context. Not a linting authority; leave alone.
- `_work/PLAN.md` already assigns `ruff`/`pre-commit`/CI-matrix ownership to
  `python_quality_gates_manifest.md` and dependency-direction enforcement to
  `python_module_boundaries_manifest.md`. The rule set itself is unassigned - which is the gap this
  pack fills.

## New content the manifest set should carry

**1. "The four layers and what each one owns" - NEW: `python_linting_practices_manifest.md`**
Open with the division of labour as a table, because every later section refers back to it. The
formatter owns layout and nothing else; it is not negotiable and has no per-project style. The linter
owns single-file AST patterns the type system cannot express. The type checker owns shape, arity,
attribute existence and override compatibility. Tests own values, sequencing and state. Fitness
functions own cross-file structure. State the routing rule the whole manifest follows: a practice is
grounded only when it names its layer and its mechanism, and "contract-only" is an allowed answer that
must be written down rather than implied. Close with the measured evidence that the layers really do
differ - on one probe ruff `--select ALL` found nothing, mypy `--strict` found three defects, pylint
found the same three, and only pylint found the import cycle.

**2. "Ruff: the shape of the tool" - NEW: `python_linting_practices_manifest.md`**
59 families, 968 rules, 830 stable / 138 preview, 413 on by default. The prefix-to-upstream-tool map,
so an agent reading a code can tell which tradition it comes from. `select` replaces, `extend-select`
adds. `pyproject.toml` sections versus `ruff.toml`, and the "closest config wins, ancestors ignored
unless `extend`" rule. `target-version` inference from `requires-python` and why the project should
still state it. That `--show-settings` prints the resolved enabled set, and that `ruff rule --all
--output-format json` is the artefact to check in as a baseline.

**3. "The 0.16.0 default-set discontinuity" - NEW: `python_linting_practices_manifest.md`**
This deserves its own short section because it is the strongest available argument for the manifest
set's own thesis. In one minor release the default went from 59 rules to 413, and 18 rules were removed
from the default set. A project with no explicit `select` had its standard rewritten by a routine lock
upgrade. The conclusion the section must state: write `select` explicitly, pin ruff exactly, and diff
the rule baseline on every bump. Name the 18 removed codes so a reader can tell whether they were
relying on them.

**4. "Fix safety is a semantics contract, not a convenience" - NEW: `python_linting_practices_manifest.md`**
Define safe versus unsafe in ruff's own words. Give the measured `RUF015` walkthrough: `--fix` refuses
and prints the hidden-fix hint; `--unsafe-fixes --fix` rewrites `list(xs)[0]` to `next(iter(xs))` and
changes `IndexError` to `StopIteration`. Draw the operational rule: `--fix` in CI, `--unsafe-fixes`
only interactively with the diff read line by line, never in a hook. Note that safety classifications
move between releases (`PT022`, `FURB105`, `PT018` in 0.16.1), so the pinned version is part of the
contract. Note that only about 48% of rules are autofixable at all, so most of the value is diagnosis,
not repair.

**5. "The defensible rule set for a small strictly-typed project" - NEW: `python_linting_practices_manifest.md`**
The core recommendation, organised as enable / enable-with-configuration / reject, one line of
justification each. Enable: `F`, `E` (minus the formatter-owned members), `I`, `UP`, `B`, `C4`, `SIM`,
`DTZ`, `G`, `LOG`, a named `TRY` subset, `BLE`, `S`, `PGH`, `RUF`, `PT`, `T20`, `PTH`, `FLY`, `PERF`,
`N`, `A`, `ICN`, `INP`, `PIE`, `RSE`, `SLF`, `TID`. Enable-with-configuration: `D` (convention must be
set), `PL` (thresholds are project decisions), `TC` (exemption lists for pydantic). Reject as
formatter-owned: `Q`, `COM`, `ISC002`, `W191`, `E111`/`E114`/`E117`, `E501`, `D203`, `D206`, `D300`.
Reject as type-checker-owned: `ANN` except `ANN401`. Flag as contested and requiring a recorded
decision: `TRY003` plus `EM*`, `TRY300`, `TRY301`, `ERA001`, `ARG*`, `FBT*`, `PLR2004`, and the `D1xx`
"everything needs a docstring" rules.

**6. "Rules that fight another layer and must be disabled" - NEW: `python_linting_practices_manifest.md`**
The formatter-conflict list verbatim from ruff's docs, then the measured finding that ruff issues no
warning when you enable them anyway, then the D203 ping-pong reproduction: `check --select D203 --fix`
adds the blank line, `format` removes it, forever, both fixes marked "always available". Then the
type-checker overlap: `ANN001`/`ANN201` restate `--disallow-untyped-defs`, so running both reports
every missing annotation twice in two vocabularies. State the rule: one defect, one owner, one
message.

**7. "Suppression hygiene and the ratchet" - NEW: `python_linting_practices_manifest.md`**
The three suppression scopes with exact syntax, including the 0.16.0 `# ruff: ignore[CODE]` form and
the `# ruff: disable[...]`/`enable[...]` block form. The full hygiene family - `RUF100`, `RUF101`,
`RUF102`, `RUF103`, `RUF104`, `PGH003`, `PGH004`, `RUF028` - with which are default-on (only `RUF100`,
`RUF101`, `RUF028`) and the rule that adopting block suppressions obliges you to select `RUF103` and
`RUF104` in the same commit. The `RUF100` `non-enabled` versus `unused` distinction. `lint.external`
for coexisting codes. The type-checker mirror: `--warn-unused-ignores`, `ignore-without-code`, and
pyright's `reportUnnecessaryTypeIgnoreComment` being `"none"` even in strict. The census recipe
(`--statistics`, `--ignore-noqa`, the delta) and the honest admission that no mechanism requires a
*reason*. Forward-looking note: `RUF105`/`RUF106` show ruff intends `ruff: ignore[rule-name]` to
replace `noqa`, so a project standardising today should expect one migration.

**8. "Extensibility: what you can and cannot mechanise" - NEW: `python_linting_practices_manifest.md`**
Lead with the blunt answer: ruff accepts no third-party rules, issue #283 is open, and no work is under
way. Then the ladder in ascending cost - `TID251` ban-list, semgrep YAML, an `ast`-walking pytest,
libcst, a pylint plugin when inferred types are genuinely needed, a flake8 plugin only if flake8
already runs. Include the verified `TID251` config for banning `datetime.datetime.utcnow` with a
custom message, because that single mechanism covers a large fraction of real house rules at near-zero
cost.

**9. "Is pylint worth it? - a measured answer" - NEW: `python_linting_practices_manifest.md`**
Present the probe honestly: pylint's `E1101`/`W0221`/`E1120` versus ruff finding none of them versus
mypy `--strict` finding all three *even on untyped code*. Conclude that for the target profile the
inference argument mostly dissolves, and the defensible residue is `R0401` cyclic-import and `R0801`
duplicate-code. Offer the cheaper substitute for the first - post-process `ruff analyze graph`'s JSON
in a test - and note that it is self-declared experimental. State the cost plainly: a second
vocabulary, config, suppression syntax and unused-suppression audit (`I0021`, off by default).

**10. "Formatting is not negotiable" - NEW: `python_linting_practices_manifest.md`**
Short and firm. `ruff format` targets Black's stable style and claims >99.9% line-identical output on
Black-formatted Django and Zulip; known deviations are f-string internals and preview fluent chains.
Black 26.5.1 has a written stability policy and a year-named stable style. Therefore: pick one, set
`line-length` once, delete every layout rule from the lint config, run `--check` in CI and the writer
locally. The argument is not that 88 is correct; it is that the debate has negative expected value and
a formatter ends it.

**11. "Docstrings, imports and names as mechanised conventions" - NEW: `python_linting_practices_manifest.md`**
Defer the style question to `python_typing_contract_manifest.md` §7 and cover only enforcement: the `D`
family, `lint.pydocstyle.convention` defaulting to `null` and what that silently does, the D203/D211
and D212/D213 incompatibility warnings, `DOC501` as the mechanical form of §7's `Raises:` mandate
(still preview), `I001`/`I002`, and the `N` family with the note that only `N999` is on by default.

**12. Cross-reference stubs - `python_quality_gates_manifest.md` (planned NEW)**
That file should carry the wiring only, and should link here rather than restate: the exact ruff and
pylint pins, `--exit-non-zero-on-fix` and why a hook that fixes must fail, `--statistics` as the
ratchet's data source, the checked-in `ruff rule --all` baseline diff, exit codes 0/1/2, and the
`--output-format` choice for the CI annotator. One paragraph, all links.

**13. Cross-reference stub - `logging_observability_manifest.md` (update)**
Answer its Open question 6 mechanically. Add the exact codes to the existing sentence: the lazy-args
stance is enforced by selecting `G001`-`G004` (none default-on), the traceback stance by `TRY400`,
`LOG004`, `LOG007` and `LOG014`, and the `extra=` collision hazard by `G101`. Add `lint.logger-objects`
so the rules recognise the project's own logger wrapper. Two or three sentences; do not import the rule
table.

**14. Cross-reference stub - `python_typing_contract_manifest.md` (update, Stage 4)**
Extend the escape-hatch ratchet with its linter half, one sentence each: `PGH003` plus mypy
`ignore-without-code` for blanket ignores, `RUF100` for stale ones, and the warning that pyright's
`reportUnnecessaryTypeIgnoreComment` is `"none"` in every mode including strict, so a pyright-only
project has no stale-ignore signal at all.

## Traps for coding agents

1. **`select` obliterates the defaults.** Writing `select = ["E", "F"]` after upgrading to 0.16.x
   silently discards ~400 default rules including every DTZ rule, `B006`, `BLE001` and `RUF100`. Use
   `extend-select` to add; use `select` only when you intend to define the whole set.
2. **The 0.16.0 upgrade rewrote the standard for anyone without an explicit `select`.** 59 -> 413
   rules. A "no code changes" dependency bump can turn a green build red for reasons unrelated to the
   commit. Pin ruff and diff the rule baseline.
3. **D203 versus the formatter is a genuine infinite loop.** Measured: `ruff check --select D203 --fix`
   inserts the blank line, `ruff format` deletes it, and both fixes are "always available". Two
   subcommands of the same binary undo each other forever, and neither prints a warning.
4. **Ruff does not warn about formatter-conflicting rules.** Measured: selecting `D203, ISC001,
   COM812, E501, W191, Q000` alongside the formatter produced no diagnostic at all. Ruff only warns
   about *mutually* incompatible lint rules (D203/D211, D212/D213). Excluding the formatter-owned list
   is unguarded config discipline.
5. **`lint.pydocstyle.convention` defaults to `null`, which is not neutral.** With `D` selected and no
   convention, ruff prints two incompatibility warnings and silently picks a winner for you. Set the
   convention explicitly, or the D family means something you did not choose.
6. **Preview rules are silently unselectable.** `select = ["DOC501"]` with preview off is not an error
   and produces no diagnostic - the rule simply never runs. An agent will read the config, believe the
   rule is enforced, and be wrong. Conversely `select = ["ALL"]` with `preview = true` drags in all
   138 preview rules; `lint.explicit-preview-rules = true` is the fix.
7. **The four highest-value logging rules are off by default.** `G001`, `G002`, `G003` and `G004` are
   all absent from the 413-rule default set. An agent that assumes "ruff catches f-strings in logging"
   is wrong unless someone selected them.
8. **`TRY300`, `TRY301`, `TRY400`, `B904`, `PGH003`, `PGH004`, `S101`, `E501`, all of `ANN`, and all of
   `D` except `D419` are likewise off by default.** Verify against `--show-settings`, never against
   intuition.
9. **Unsafe autofixes change semantics, and the diff looks harmless.** `RUF015`'s fix turns
   `IndexError` into `StopIteration`. `TRY400`'s fix is unsafe for anything ruff cannot prove is a
   `logging.Logger`. Never run `--unsafe-fixes` unattended; never put it in a hook.
10. **Fix safety is reclassified across releases.** 0.16.1 alone moved `PT022` and `FURB105` to unsafe
    and `PT018` to safe. An unpinned ruff means an unpinned definition of "safe to autofix".
11. **`TC001`-`TC003` plus autofix can break pydantic, dataclasses and attrs at runtime.** They move
    imports into `TYPE_CHECKING`, which is wrong for any class whose annotations are introspected at
    runtime. `runtime-evaluated-base-classes` and `runtime-evaluated-decorators` both default to `[]`,
    so the protection is off until you configure it. `TC004` catches the breakage only after the fix
    has landed.
12. **`RUF100` cannot judge a rule you never enabled.** It reports `(non-enabled: E501)` rather than
    calling the suppression wrong. Treat `non-enabled` as a config smell and `unused` as dead debt -
    two different problems behind one rule code.
13. **`# noqa` is per-code and non-transitive.** Measured: `import io  # noqa: E501` does not suppress
    `F401` on that line. An agent adding a code to an existing `noqa` must add the *right* code, and
    `RUF102` plus `lint.external` is what tells it when the code is bogus.
14. **Adopting `# ruff: disable[...]` blocks without selecting `RUF103` and `RUF104` is a footgun.** An
    unterminated `disable` implicitly runs to the end of the enclosing scope; at module level that is
    the rest of the file. Neither guard rule is default-on.
15. **A blanket `# noqa` is invisible unless `PGH004` is selected**, and a blanket `# type: ignore` is
    invisible unless `PGH003` is selected *or* mypy's `ignore-without-code` is enabled - and
    `ignore-without-code` is not part of `--strict`.
16. **pyright never reports stale ignores by default.** `reportUnnecessaryTypeIgnoreComment` is
    `"none"` in off, basic, standard **and** strict. A pyright-only project that assumes strict mode
    covers this accumulates ignores with zero signal.
17. **`ANN` fights the type checker rather than complementing it.** `ANN001`/`ANN201` report the same
    defect as mypy's `--disallow-untyped-defs`, in a second vocabulary. Keep `ANN401` (mypy `--strict`
    tolerates `Any` on arguments) and drop the rest; otherwise every missing annotation is two
    findings.
18. **`S101` must be exempted for tests, not disabled globally.** Use `lint.per-file-ignores` scoped to
    the test tree. A global `ignore = ["S101"]` re-permits `assert`-as-validation in production code,
    which vanishes under `-O`.
19. **Nothing requires a reason on a suppression.** Verified across all 968 rule explanations. The
    `--add-noqa=<REASON>` flag can write one; no rule checks that one exists. If the project wants
    reasons, that is a regex test or a semgrep rule, and it belongs in the gate config on day one.
20. **Do not write a ruff plugin.** There is no plugin API and none is being built. An agent that
    proposes one has invented a mechanism. Reach for `TID251`, semgrep, or an `ast`-walking test.
21. **Removed rule codes are dead configuration that nothing flags.** `TRY200`, `PGH001`, `PGH002` and
    `PT004` are removed; listing them in `select` is silently inert. `RUF101`/`RUF102` catch stale
    codes in `noqa` comments but not in the config file itself.
22. **`ruff analyze graph` self-declares as experimental** ("may change without warning") and does not
    detect cycles - it only emits an adjacency map. Any cycle check built on it is project-owned code
    whose input format is unstable.
23. **`E501` and the formatter both claim line length.** Enable both and you get diagnostics the
    formatter cannot fix, on lines it deliberately left long (a URL inside a string). Set
    `line-length` once, in `[tool.ruff]`, and leave `E501` off.
24. **0.16.0 changed ruff's JSON output shape**: `filename`, `location`, `end_location` and
    `fix.edits[].location` may now be `null`. Any CI script that parses ruff JSON must be re-tested
    after the bump.
25. **`# ruff: noqa` at file scope disables everything for the whole file** and is easy to leave behind
    after a debugging session. `--ignore-noqa` is how you find out how much of the codebase is
    currently exempt.

## Honest limits

- **The recommended rule set is a judgement, not a measurement.** No study loaded this session
  establishes that any ruff family reduces defect density. The defensible claim is narrower, and is the
  one the manifest should make: these rules encode hazards the type system provably cannot express
  (facts 83-92), and a mechanised rule outlives the reviewer who would otherwise have to remember it.
- **Contested families are contested on taste, and this pack does not resolve them.** `TRY003` versus
  `EM101`/`EM102` (message at the raise site or in the exception class), `TRY300`, `TRY301`, `ERA001`,
  `ARG*`, `FBT*`, `PLR2004` and the `D1xx` "everything needs a docstring" rules all generate
  substantial noise on ordinary correct code. The manifest's job is to force a recorded decision, not
  to pretend one answer is grounded.
- **Every threshold is a convention.** `max-complexity = 10`, `max-args = 5` and `line-length = 88` are
  defaults chosen by tool authors, not findings. Ruff's own default and Black's 88 are the only
  argument for 88, and it is an argument from coordination, not from evidence.
- **The pylint verdict rests on one probe.** Facts 51-53 were measured on small purpose-built files. A
  real codebase with heavy dynamic dispatch, metaclasses, or untyped third-party dependencies could
  shift the balance back toward astroid inference. The conclusion "largely redundant for a strictly
  typed project" is a defensible inference from a demonstration, not a benchmark.
- **"> 99.9% of lines identical" is Astral's own measurement on Django and Zulip.** It is a vendor
  claim about two codebases, not an independent audit, and the docs name no target Black version - so
  the compatibility statement cannot be pinned to a specific Black release.
- **Ruff's own rule count is stated three ways** - "over 900" in the docs, 968 in the 0.16.0 blog, 968
  from `ruff rule --all`. They are reconcilable, but it shows that even the tool's documentation lags
  its binary. Trust the binary; check it in.
- **Two small internal inconsistencies were observed and are reported rather than smoothed over.**
  PyPI dates ruff 0.16.2 to 2026-08-07 while the CHANGELOG says 2026-08-06. Ruff's incompatibility
  warning spells D211 as `no-blank-line-before-class` while `ruff rule D211` calls it
  `blank-line-before-class`.
- **Black's exact release date is unresolved.** The PyPI page shows no date and the JSON API answer
  returned an implausible 2024 timestamp for version 26.5.1; rather than repeat a figure that is
  probably wrong, this pack leaves it OPEN.
- **Semgrep's version, licence tier, and whether the taint mode used here is available in the
  open-source CLI were not confirmed.** The rule *syntax* is verified; treat the recommendation as
  conditional until a project actually adopts it.
- **The plugin-system status beyond the FAQ sentence is FLAGGED-SECONDARY.** Fact 76 is from ruff's own
  FAQ and is solid. Fact 77 (no work under way as of September 2025) came from a search summary of
  discussion #20652, which was not loaded directly.
- **pyright was verified from `main`, not a release.** The mode-by-mode defaults in facts 46-47 come
  from the repository's current `docs/configuration.md`; no pyright version was pinned this session.
- **Suppression census numbers are only comparable against a pinned linter.** A `--statistics` count
  that falls after a ruff upgrade may mean the code improved, or may mean a rule was demoted out of
  the default set. The ratchet is meaningless without the pin.

## Sources (accessed 2026-08-08)

- https://pypi.org/project/ruff/ - ruff 0.16.2, released 2026-08-07; "An extremely fast Python linter
  and code formatter, written in Rust"; requires Python >=3.7, states Python 3.14 compatibility.
- https://docs.astral.sh/ruff/rules/ - "Ruff supports over 900 lint rules"; the full
  prefix-to-upstream table (all 59 families); codes and names for the G, LOG, DTZ and BLE families and
  for B006, B008, B023, B904, B905, S101.
- https://docs.astral.sh/ruff/linter/ - `lint.select`/`extend-select`/`ignore` semantics; the safe vs
  unsafe fix definition and the RUF015 example; `--unsafe-fixes`, `unsafe-fixes`,
  `lint.extend-safe-fixes`, `lint.extend-unsafe-fixes`; all three suppression scopes including
  `# ruff: disable[...]`/`enable[...]` and `# ruff: file-ignore[...]`; `RUF100` and `RUF104`;
  `--add-noqa`/`--add-ignore`; exit codes 0/1/2, `--exit-zero`, `--exit-non-zero-on-fix`.
- https://docs.astral.sh/ruff/formatter/ - "drop-in replacement for Black", "> 99.9% of lines are
  formatted identically" on Django and Zulip; the 16-code formatter-conflict list (W191, E111, E114,
  E117, D203, D206, D300, Q000-Q004, COM812, COM819, ISC002, E501); the f-string and fluent-chain
  deviations; `ruff format --check`, `# fmt: off`/`on`/`skip`.
- https://docs.astral.sh/ruff/faq/ - "Ruff does not yet support third-party plugins, though a plugin
  system is within-scope for the project" (issue #283); "Ruff does not support custom lint rules";
  "Pylint does more type inference than Ruff (e.g., Pylint can validate the number of arguments in a
  function call)".
- https://docs.astral.sh/ruff/preview/ - preview is opt-in via `--preview` or `preview = true` under
  `[tool.ruff.lint]`/`[tool.ruff.format]`; "If a rule is marked as preview, it can only be selected if
  preview mode is enabled"; exact-code, prefix and `ALL` selection all fail without it;
  `explicit-preview-rules`.
- https://docs.astral.sh/ruff/settings/ - defaults: `line-length` 88, `target-version` "py310",
  `lint.ignore` `[]`, `lint.extend-select` `[]`, `lint.fixable` `["ALL"]`, `lint.unfixable` `[]`,
  `lint.extend-safe-fixes` `[]`, `lint.extend-unsafe-fixes` `[]`, `lint.per-file-ignores` `{}`,
  `lint.preview` false, `lint.explicit-preview-rules` false, `lint.external` `[]`,
  `lint.pydocstyle.convention` **null** (allowed: google/numpy/pep257), `lint.dummy-variable-rgx`,
  `lint.task-tags` `["TODO","FIXME","XXX"]`,
  `lint.flake8-type-checking.runtime-evaluated-base-classes` `[]`, `runtime-evaluated-decorators`
  `[]`, `strict` false, `quote-annotations` false, `lint.logger-objects` `[]`,
  `lint.flake8-bandit.check-typed-exception` false, `lint.mccabe.max-complexity` 10,
  `lint.pylint.max-args` 5, `lint.flake8-annotations.*` all false.
- https://docs.astral.sh/ruff/default-rules/ - the enumerated default rule set (per-family code
  listings).
- https://docs.astral.sh/ruff/configuration/ - `[tool.ruff]`/`[tool.ruff.lint]`/`[tool.ruff.format]`
  versus `ruff.toml`/`.ruff.toml` and their precedence; `extend` inheritance and "closest config wins,
  ancestors ignored"; `target-version` inference from `requires-python` in the same directory as the
  found config; the `ruff check` flag list; the subcommand list (check, rule, config, linter, clean,
  format, server, analyze, version, help).
- https://astral.sh/blog/ruff-v0.16.0 - released 2026-07-23; default set 59 -> 413; total rules 708 ->
  968; the 18 codes removed from the default set; `# ruff: ignore[F401]`,
  `# ruff: disable[]`/`enable[]`, `# ruff: file-ignore[]`; `--add-ignore` and rule names under
  preview; fixes shown as diffs by default; the JSON `null` breaking change; the 12 stabilised rules.
- https://raw.githubusercontent.com/astral-sh/ruff/main/CHANGELOG.md - 0.16.2 dated 2026-08-06; 0.16.1
  dated 2026-07-30, with `PT022` and `FURB105` fixes reclassified unsafe and `PT018` made safe by
  default.
- https://docs.astral.sh/ruff/rules/blanket-noqa/ - PGH004 `blanket-noqa`, from pygrep-hooks, fix
  sometimes available, "Suppressing all diagnostics can hide issues in the code."
- https://docs.astral.sh/ruff/rules/blanket-type-ignore/ - PGH003 `blanket-type-ignore`, from
  pygrep-hooks, no fix.
- https://docs.astral.sh/ruff/rules/try-consider-else/ - TRY300 `try-consider-else`, from tryceratops;
  returns in `try` blocks "may exhibit confusing or unwanted behavior".
- https://docs.astral.sh/ruff/rules/raise-vanilla-args/ - TRY003 `raise-vanilla-args`; formatting a
  message at the raise site makes the exception class "less reusable".
- https://docs.astral.sh/ruff/rules/error-instead-of-exception/ - TRY400
  `error-instead-of-exception`; fix safe for `logging.error`, unsafe for other logger-like calls.
- https://docs.astral.sh/ruff/rules/unmatched-suppression-comment/ - RUF104
  `unmatched-suppression-comment`, stable since 0.15.0; unmatched ranges "can inadvertently suppress
  violations over larger sections of code than intended, particularly at module scope".
- https://docs.astral.sh/ruff/rules/invalid-suppression-comment/ - RUF103
  `invalid-suppression-comment`, added 0.15.0, fix always available.
- https://docs.astral.sh/ruff/rules/invalid-rule-code/ - RUF102 `invalid-rule-code`, stable since
  0.15.0, fix always available.
- https://docs.astral.sh/ruff/rules/redirected-noqa/ - RUF101 `redirected-noqa`, stable, fix always
  available.
- https://docs.astral.sh/ruff/rules/any-type/ - ANN401 `any-type`, from flake8-annotations; `Any` as
  an "escape hatch only when it is really needed".
- https://docs.astral.sh/ruff/rules/incorrect-blank-line-before-class/ - D203
  `incorrect-blank-line-before-class`; disabled under the google, numpy and pep257 conventions; "We
  recommend against using this rule alongside the formatter."
- https://pypi.org/project/pylint/ - pylint 4.0.6, released 2026-06-14, requires Python >=3.10,
  supports 3.10-3.14; astroid inference described with the `import logging as argparse` example;
  "[inference] is the killer feature that keeps us using [pylint] in our project despite how painfully
  slow it is".
- https://pylint.readthedocs.io/en/latest/user_guide/messages/messages_overview.html - the C/R/W/E/F/I
  categories and the code/name pairs E1101 no-member, W0221 arguments-differ, W0237 arguments-renamed,
  R0401 cyclic-import, R0913 too-many-arguments, R0801 duplicate-code, W0611 unused-import, C0103
  invalid-name, C0116 missing-function-docstring, I0021 useless-suppression, E0012 bad-option-value,
  E1120 no-value-for-parameter, E1121 too-many-function-args, E1136 unsubscriptable-object, E1102
  not-callable.
- https://pylint.readthedocs.io/en/stable/user_guide/messages/information/useless-suppression.html -
  I0021 `useless-suppression`, disabled by default, enabled via the `enable` option, failed on via
  `--fail-on=I0021` or `--fail-on=I`.
- https://pylint.readthedocs.io/en/latest/development_guide/how_tos/plugins.html - plugins load via
  the `load-plugins` option; AST, token and raw checker kinds; astroid inference available to plugins.
- https://mypy.readthedocs.io/en/stable/command_line.html - `--warn-unused-ignores`,
  `--warn-redundant-casts`, `--disallow-untyped-defs`, `--disallow-any-explicit`,
  `--enable-error-code`, `--disable-error-code`, and the exact 13-flag composition of `--strict`.
- https://mypy.readthedocs.io/en/stable/error_code_list2.html - `ignore-without-code` ("Warn when a
  `# type: ignore` comment does not specify any error codes"), plus `redundant-expr`, `truthy-bool`,
  `truthy-iterable`, `possibly-undefined`, `explicit-override`, `mutable-override`,
  `exhaustive-match`, `deprecated`, `unused-awaitable`, `unimported-reveal`; enablement via
  `--enable-error-code`, `enable_error_code =`, or `# mypy: enable-error-code="..."`.
- https://raw.githubusercontent.com/microsoft/pyright/main/docs/configuration.md -
  `enableTypeIgnoreComments` true in all four modes; `# pyright: ignore` unaffected by it;
  `reportUnnecessaryTypeIgnoreComment` "none" in off/basic/standard/strict;
  `reportUnnecessaryIsInstance`, `reportUnnecessaryCast`, `reportUnnecessaryComparison`,
  `reportUnusedImport`, `reportPrivateUsage`, `reportUnknownMemberType` "error" only in strict;
  `reportUnusedCallResult` and `reportImplicitOverride` "none" even in strict.
- https://pypi.org/project/black/ - black 26.5.1, requires Python 3.10+, Stability Policy, 2026 stable
  style introduced in 26.1.0 and 2025 stable style in 25.1.0.
- https://pypi.org/pypi/black/json - `info.version` 26.5.1; the returned upload timestamp was
  implausible and is recorded as OPEN rather than asserted.
- https://pypi.org/project/flake8/ - flake8 7.3.0, released 2025-06-20, requires Python >=3.9,
  "extendable through flake8.extension and flake8.formatting entry points".
- https://docs.semgrep.dev/writing-rules/pattern-syntax - YAML rule fields `id`, `pattern`,
  `patterns`, `pattern-either`, `pattern-not`, `metavariable-pattern`, `languages`, `severity`,
  `message`, `fix`; `--pattern`/`-e` for a single CLI pattern; taint mode with
  `pattern-sources`/`pattern-sinks` and the metavariable-unification caveat.
- MEASURED, ruff 0.16.2 via `uvx ruff@0.16.2` - `ruff linter` (59 families); `ruff rule --all
  --output-format json` (968 rules, 830 stable / 138 preview, fix availability 494/251/223, and every
  code/name/fix/preview/status pair quoted in the Facts and the routing table); `ruff check --help`
  (the full flag list including `--add-noqa[=<REASON>]`, `--add-ignore[=<REASON>]`, `--ignore-noqa`,
  `--statistics`, `--unsafe-fixes`/`--no-unsafe-fixes`, the 11 `--output-format` values, and
  `--target-version py37..py315`); `ruff format --help` (`--check`, `--diff`, `--range`,
  `--line-length`, `--preview`); `ruff check --isolated --show-settings` (413 default rules and their
  per-prefix distribution, `linter.line_length = 88`, `unsafe_fixes = hint`,
  `linter.preview = disabled`, `formatter.quote_style = double`,
  `formatter.docstring_code_format = disabled`); `ruff rule D211` (`blank-line-before-class`); the
  RUF015 safe-versus-unsafe fix walkthrough; the D203/`ruff format` ping-pong; the absence of any
  formatter-conflict warning; the D203/D211 and D212/D213 incompatibility warnings appearing only when
  `convention` is unset; noqa and `ruff: ignore` suppression behaviour with PGH004, RUF100
  (`non-enabled` vs `unused`) and RUF102 plus `lint.external`; and the working `TID251` `banned-api`
  configuration for `datetime.datetime.utcnow`.
- MEASURED, pylint 4.0.6 with astroid 4.0.4 via `uvx --from pylint==4.0.6 pylint` - `W0221`
  arguments-differ, `E1101` no-member, `E1120` no-value-for-parameter and `W0612` unused-variable on a
  probe where `ruff check --select ALL` reported none of them; `R0401` cyclic-import on a two-module
  cycle that ruff and mypy both passed.
- MEASURED, mypy 2.3.0 via `uvx mypy` - `--strict` on the same untyped probe reported `[override]`,
  `[attr-defined]`, `[call-arg]`, `[no-untyped-def]` and `[no-untyped-call]`; on the annotated version
  `[attr-defined]` and `[call-arg]`; and on the cyclic package "Success: no issues found in 3 source
  files".
