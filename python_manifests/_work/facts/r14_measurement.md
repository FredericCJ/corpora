# Measuring maintainability in Python (and the honest limits of doing so) - fact pack (verified 2026-08-08)

**Scope.** The final rung of the governing thesis: *maintainable must be observed, not asserted.* This
pack establishes which numbers exist, which tool emits each one, what the empirical literature says the
number does and does not predict, and which numbers are safe as **gates** versus **diagnostics** versus
**not safe at all**. Version anchor for the interpreter: see `python_platform_baseline_manifest.md`
(CPython 3.14.7, 2026-08-05). Destination file: **NEW: `python_quality_gates_manifest.md`**.

## Version table

| thing | current version | released (ISO) | source URL | tag |
|---|---|---|---|---|
| ruff (C901, PL* complexity rules, `analyze graph`) | 0.16.2 | 2026-08-07 | https://pypi.org/pypi/ruff/json | VERSION-DEPENDENT (0.16.2) |
| pylint (design + `symilar` duplicate-code checkers) | 4.0.6 | 2026-06-14 | https://pypi.org/pypi/pylint/json | VERSION-DEPENDENT (4.0.6) |
| mypy (annotation-coverage reports) | 2.3.0 | 2026-07-13 | https://pypi.org/pypi/mypy/json | VERSION-DEPENDENT (2.3.0) |
| pyright (`--verifytypes` completeness score) | 1.1.411 | 2026-06-25 | https://pypi.org/pypi/pyright/json | VERSION-DEPENDENT (1.1.411) |
| coverage.py (line/branch, `fail_under`) | 7.15.4 | 2026-08-06 | https://pypi.org/pypi/coverage/json | VERSION-DEPENDENT (7.15.4) |
| pytest-cov | 7.1.0 | 2026-03-21 | https://pypi.org/pypi/pytest-cov/json | VERSION-DEPENDENT (7.1.0) |
| diff-cover (coverage on the diff) | 10.4.2 | 2026-08-07 | https://pypi.org/pypi/diff-cover/json | VERSION-DEPENDENT (10.4.2) |
| mutmut (mutation testing) | 3.7.0 | 2026-07-31 | https://pypi.org/pypi/mutmut/json | VERSION-DEPENDENT (3.7.0) |
| cosmic-ray (mutation testing, alt.) | 8.4.6 | 2026-04-02 | https://pypi.org/pypi/cosmic-ray/json | VERSION-DEPENDENT (8.4.6) |
| import-linter (6 contract types) | 2.13 | 2026-07-03 | https://pypi.org/pypi/import-linter/json | VERSION-DEPENDENT (2.13) |
| grimp (import graph library under import-linter) | 3.15 | 2026-07-03 | https://pypi.org/pypi/grimp/json | VERSION-DEPENDENT (3.15) |
| Tach (module/interface enforcement, Rust) | 0.35.0 | 2026-05-12 | https://pypi.org/pypi/tach/json | VERSION-DEPENDENT (0.35.0) |
| pydeps (graph + `--show-cycles`) | 3.0.7 | 2026-08-03 | https://pypi.org/pypi/pydeps/json | VERSION-DEPENDENT (3.0.7) |
| vulture (dead code) | 2.16 | 2026-03-25 | https://pypi.org/pypi/vulture/json | VERSION-DEPENDENT (2.16) |
| complexipy (cognitive complexity, Rust) | 6.2.0 | 2026-07-23 | https://pypi.org/pypi/complexipy/json | VERSION-DEPENDENT (6.2.0) |
| mypy-baseline (type-error ratchet) | 0.7.4 | 2026-04-13 | https://pypi.org/pypi/mypy-baseline/json | VERSION-DEPENDENT (0.7.4) |
| interrogate (docstring coverage) | 1.7.0 | 2024-04-07 | https://pypi.org/pypi/interrogate/json | VERSION-DEPENDENT (1.7.0) |
| radon (CC, raw, Halstead, MI) | 6.0.1 | **2023-03-26** | https://pypi.org/pypi/radon/json | VERSION-DEPENDENT (6.0.1) - stale |
| xenon (radon-based CI gate) | 0.9.3 | **2024-10-21** | https://pypi.org/pypi/xenon/json | VERSION-DEPENDENT (0.9.3) - stale |
| wily (metrics over git history) | 1.25.0 stable; 2.0.0a1 prerelease | 2023-10-11; **2026-04-26** | https://pypi.org/pypi/wily/json | VERSION-DEPENDENT (1.25.0) - see Fact 24 |
| Cognitive Complexity white paper | Version 1.7 | 2023-08-29 | https://www.sonarsource.com/docs/CognitiveComplexity.pdf | ESTABLISHED |
| SonarPython S3776 default threshold | 15 | n/a (source constant) | https://raw.githubusercontent.com/SonarSource/sonar-python/master/python-checks/src/main/java/org/sonar/python/checks/CognitiveComplexityFunctionCheck.java | ESTABLISHED |
| SonarPython "Sonar way" profile | 393 rule keys | n/a | https://raw.githubusercontent.com/SonarSource/sonar-python/master/python-checks/src/main/resources/org/sonar/l10n/py/rules/python/Sonar_way_profile.json | VERSION-DEPENDENT (master) |
| NIST SP 500-235 (structured testing / CC limit) | 1996 edition | 1996-08 | https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication500-235.pdf | ESTABLISHED |
| DORA delivery metrics | five-metric model | current as of fetch | https://dora.dev/guides/dora-metrics-four-keys/ | VERSION-DEPENDENT (2026-08 page state) |

## Facts

### A. Cyclomatic complexity - what it is, and what the evidence says

1. **McCabe cyclomatic complexity counts decision points plus one.** Ruff's own definition of C901:
   McCabe complexity measures "the complexity of the control flow graph of the function", computed by
   "add[ing] one to the number of decision points in the function" - ESTABLISHED.
2. **The limit of 10 is a NIST-endorsed convention, not a validated threshold.** NIST SP 500-235
   (Watson & McCabe, 1996) states verbatim: "The precise number to use as a limit, however, remains
   somewhat controversial. The original limit of 10 as proposed by McCabe has significant supporting
   evidence, but limits as high as 15 have been used successfully as well. Limits over 10 should be
   reserved for projects that have several operational advantages over typical projects, for example
   experienced staff, formal design, a modern programming language, structured programming, code
   [walkthroughs]" - ESTABLISHED.
3. **Shepperd (1988) is the canonical refutation and it is blunt.** *A critique of cyclomatic complexity
   as a software metric*, Software Engineering Journal 3(2):30-36. Abstract, verbatim: the metric "is
   based upon poor theoretical foundations and an inadequate model of software development. The argument
   that the metric provides the developer with a useful engineering approximation is not borne out by the
   empirical evidence. Furthermore, it would appear that for a large class of software it is no more than
   a proxy for, and in many cases is outperformed by, lines of code." His survey table records CC-to-LOC
   Pearson coefficients of 0.84-0.92 across studies, and he reports "the out-performing of v(G) by a
   straightforward LOC metric in over a third of the studies considered" - ESTABLISHED.
4. **Shepperd's structural objection matters for refactoring gates:** he notes CC can increase when
   applying generally accepted techniques to improve program structure, and concludes "the only possible
   role for cyclomatic complexity is as an intra-modular complexity metric", since how to modularise "is
   better resolved by considerations of `coupling' and `cohesion' ... which are not adequately captured by
   the metric" - ESTABLISHED.
5. **The "CC is just LOC" claim is contested, not settled.** Jay/Hale/Smith/Hale/Kraft/Ward (2009), *J.
   Software Engineering & Applications* 2:137-143, reported a stable linear CC-LOC relationship -
   FLAGGED-SECONDARY (the SciRP article page returned HTTP 403 this session; bibliographic details
   confirmed via search metadata only). Against it, Landman, Serebrenik & Vinju (ICSME 2014; extended in
   *J. Software: Evolution and Process*, 2016) analysed **17.6 million Java methods and 6.3 million C
   functions** and state on the authors' own site: "the observed linear correlation between CC and SLOC of
   Java methods or C functions is not strong enough to conclude that CC is redundant with SLOC", noting
   "linear correlation between SLOC and CC is only moderate as caused by increasingly high variance", and
   that "aggregating CC and SLOC as well as performing a power transform improves the correlation" -
   ESTABLISHED (that this is the authors' claim).
6. **Consequence for the manifest:** the honest position is *unit-of-measurement dependent*. At
   file/package aggregate level CC tracks size closely - SonarSource's own white paper concedes "it is
   widely acknowledged that the Cyclomatic Complexity scores of applications correlate to their lines of
   code totals. In other words, Cyclomatic Complexity is of little use above the method level." At
   *function* level the redundancy claim does not hold up at scale. So: gate CC per function; never report
   project-average CC as a maintainability figure - ESTABLISHED.

### B. Cognitive complexity - the SonarSource specification, read directly

7. **Provenance.** *{Cognitive Complexity} a new way of measuring understandability*, by G. Ann Campbell,
   Copyright SonarSource S.A., Switzerland; the copy fetched is **Version 1.7, 29 August 2023**. Its
   stated motive: Cyclomatic Complexity "excels at measuring" testability but "its underlying
   mathematical model is unsatisfactory at producing a value that measures" maintainability; CC "cries
   wolf" by "over-valuing some structures, while under-valuing others"; and being "[f]ormulated in a
   Fortran environment in 1976, it doesn't include modern language structures like try/catch, and
   lambdas" - ESTABLISHED.
8. **The three rules, verbatim:** "1. Ignore structures that allow multiple statements to be readably
   shorthanded into one. 2. Increment (add one) for each break in the linear flow of the code. 3.
   Increment when flow-breaking structures are nested." Four increment types: **Nesting**, **Structural**
   (subject to a nesting increment and increases the nesting count), **Fundamental** (not subject to a
   nesting increment), **Hybrid** (not subject to a nesting increment but does increase the nesting
   count) - ESTABLISHED.
9. **Appendix B specification - what increments (one point each):** `if`, `else if`, `else`, ternary
   operator; `switch`; `for`, `foreach`; `while`, `do while`; `catch`; `goto LABEL` / `break LABEL` /
   `continue LABEL` / `break NUMBER` / `continue NUMBER`; sequences of binary logical operators; each
   method in a recursion cycle - ESTABLISHED.
10. **What increments the nesting LEVEL:** `if`, `else if`, `else`, ternary; `switch`; `for`, `foreach`;
    `while`, `do while`; `catch`; **and nested methods / method-like structures such as lambdas**. What
    receives a nesting increment: `if`, ternary, `switch`, `for`, `foreach`, `while`, `do while`, `catch`
    - i.e. `else`/`else if` increment but take **no** nesting increment "because the mental cost has
    already been paid when reading the if" - ESTABLISHED.
11. **Deliberate discounts.** Methods themselves do not increment ("Cognitive Complexity does not
    increment for methods"); null-coalescing operators are ignored; `try` and `finally` blocks "are
    ignored altogether"; a `catch` "only adds one point to the Cognitive Complexity score, no matter how
    many exception types are caught"; "A switch and all its cases combined incurs a single structural
    increment"; boolean-operator *sequences* of like operators cost one point each, so `a && b && c && d`
    costs 1 but `a || b && c || d` costs 3 - ESTABLISHED.
12. **The white paper states NO threshold.** Grepping the full extracted text for "threshold", "limit",
    "recommend" and "default value" returns nothing. The widely-quoted **15** is a *tool* default:
    `sonar-python`'s `CognitiveComplexityFunctionCheck` declares `private static final int
    DEFAULT_THRESHOLD = 15;`, exposed as `@RuleProperty(key = "threshold", description = "The maximum
    authorized complexity.")` - ESTABLISHED. Anyone citing "15" as the metric's own recommendation is
    citing the SonarQube default, not Campbell - ESTABLISHED.
13. **S3776 economics.** Rule metadata: title "Cognitive Complexity of functions should not be too high",
    type `CODE_SMELL`, defaultSeverity `Critical`, code attribute `FOCUSED`, impact `MAINTAINABILITY:
    HIGH`, `quickfix: infeasible`, tag `brain-overload`, remediation "linear with offset" = 5 minutes base
    + 1 minute per point over threshold. The Python implementation calls `.withCost(complexity -
    threshold)` and **skips inner functions** (`if (isInnerFunction(functionDef) || isGeneratedFile(ctx))
    return;`) - ESTABLISHED.
14. **Cognitive complexity has real, if modest, empirical support - unlike MI.** Muñoz Barón, Wyrich &
    Wagner, *An Empirical Validation of Cognitive Complexity as a Measure of Source Code
    Understandability*, ESEM 2020 (arXiv 2007.12520): meta-analysis of **~24,000 understandability
    evaluations across 427 code snippets** gathered by systematic literature review. Finding: "Cognitive
    Complexity positively correlates with comprehension time and subjective ratings of understandability",
    with "mixed results for the correlation with the correctness of comprehension tasks and with
    physiological measures" - ESTABLISHED.

### C. Halstead and the Maintainability Index - provenance and why not to gate on them

15. **Halstead, as radon implements it:** from h1 (distinct operators), h2 (distinct operands), N1, N2 -
    vocabulary `h = h1 + h2`; length `N = N1 + N2`; calculated length `h1*log2(h1) + h2*log2(h2)`; volume
    `V = N*log2(h)`; difficulty `D = (h1/2)*(N2/h2)`; effort `E = D*V`; time `T = E/18` seconds; delivered
    bugs `B = V/3000` - ESTABLISHED (radon docs). The `T = E/18` and `B = V/3000` constants are Halstead's
    own 1977 calibration and have no modern validation - OPEN.
16. **Two different Maintainability Indices are both called "the MI".** Microsoft's (Visual Studio,
    learn.microsoft.com) is `MAX(0,(171 - 5.2 * ln(Halstead Volume) - 0.23 * (Cyclomatic Complexity) -
    16.2 * ln(Lines of Code))*100 / 171)` with bands 0-9 Red "Low maintainability of code", 10-19 Yellow
    "Moderate", 20-100 Green "Good". Radon's is `MI = max[0, 100 * (171 - 5.2 ln V - 0.23 G - 16.2 ln L +
    50 sin(sqrt(2.4 C))) / 171]` where C is comment percentage - i.e. radon adds a comment-density term
    Microsoft does not have, and radon's docs say it "combines both SEI derivative and Visual Studio one".
    Radon's ranks are A = 100-20, B = 19-10, C = 9-0 - ESTABLISHED, and **the two numbers are not
    comparable** - ESTABLISHED.
17. **The MI is uncalibrated since 1994.** Arie van Deursen, "Think Twice Before Using the Maintainability
    Index" (2014-08-29): the index came from Oman & Hagemeister (ICSM 1992), refined by Coleman, Ash,
    Lowther & Oman (IEEE Computer, 1994), derived from "systems from Hewlett-Packard (written in C and
    Pascal in the late 80s, ranging in size from 1000 to 10,000 lines of code)"; "Tool smiths and vendors
    used the exact same formula and coefficients as the 1994 experiments, without any recalibration"; on
    Visual Studio's 20/10 cutoffs, "I have not been able to find a justification for these thresholds". He
    also names the aggregation defect: the index averages per file, but "these metrics follow a power law,
    and taking the average tends to mask the presence of high-risk parts". His recommendation: "Most
    likely, you'll be better off looking at lines of code" - ESTABLISHED that this is his documented
    position; FLAGGED-SECONDARY for the HP-dataset detail (a blog post, though by a primary authority on
    the critique).
18. **Therefore MI is not gate material.** Its inputs are Halstead volume (uncalibrated constants),
    cyclomatic complexity (§A) and LOC; it collapses three weakly-validated signals into one number with
    unexplained coefficients, then averages over a power-law distribution - OPEN (no primary source
    validates MI thresholds for modern Python).

### D. The Python complexity-tool landscape, with exact codes

19. **ruff 0.16.2 - the codes, with stability status read off the rules table.** Stable: **C901**
    `complex-structure` (mccabe; stable since v0.0.127), **PLR0911** `too-many-return-statements`,
    **PLR0912** `too-many-branches`, **PLR0913** `too-many-arguments`, **PLR0915** `too-many-statements`,
    **PLR0917** `too-many-positional-arguments` (**stable since 0.16.0** - preview before that),
    **PGH003** `blanket-type-ignore`, **PGH004** `blanket-noqa`, **RUF100** `unused-noqa`, **ERA001**
    `commented-out-code`. **Preview only** (require `--preview`): **PLR0904** `too-many-public-methods`
    (preview since v0.0.290), **PLR0914** `too-many-locals` (preview since v0.1.9), **PLR0916**
    `too-many-boolean-expressions` (preview since v0.1.1), **PLR1702** `too-many-nested-blocks` (preview
    since v0.1.15) - VERSION-DEPENDENT (0.16.2).
20. **ruff thresholds, from `crates/ruff_linter/src/rules/pylint/settings.rs`:** `max_args: 5`,
    `max_positional_args: 5`, `max_returns: 6`, `max_bool_expr: 5`, `max_branches: 12`,
    `max_statements: 50`, `max_statements_in_try: 5`, `max_public_methods: 20`, `max_locals: 15`,
    `max_nested_blocks: 5`; plus `lint.mccabe.max-complexity` default **10** ("The McCabe complexity
    threshold for flagging violations"). `max_positional_args` falls back to `max_args` when unset -
    VERSION-DEPENDENT (ruff main / 0.16.x).
21. **pylint 4.0.6 design-checker defaults, from `pylint/checkers/design_analysis.py`:** `max-args` 5,
    `max-positional-arguments` 5, `max-locals` 15, `max-returns` 6, `max-branches` 12, `max-statements`
    50, `max-parents` 7, `max-attributes` 7, `min-public-methods` 2, `max-public-methods` 20,
    `max-bool-expr` 5. Codes: R0901 `too-many-ancestors`, R0902 `too-many-instance-attributes`, R0903
    `too-few-public-methods`, R0904 `too-many-public-methods`, R0911 `too-many-return-statements`, R0912
    `too-many-branches`, R0913 `too-many-arguments`, R0914 `too-many-locals`, R0915
    `too-many-statements`, R0916 `too-many-boolean-expressions`, R0917 `too-many-positional-arguments`,
    R1702 `too-many-nested-blocks` - VERSION-DEPENDENT (4.0.6).
22. **pylint has NO cyclomatic-complexity message.** The messages overview contains no
    cyclomatic-complexity code; R0912 `too-many-branches` counts branches, a related but different
    quantity - ESTABLISHED. If you want CC you must use ruff C901 or radon.
23. **pylint duplicate-code is R0801, and its module was renamed.** The checker now lives at
    `pylint/checkers/symilar.py` (`similar.py` returns 404 on main), with constant
    `DEFAULT_MIN_SIMILARITY_LINE = 4` and option defaults `min-similarity-lines` 4, `ignore-comments`
    True, `ignore-docstrings` True, `ignore-imports` True, `ignore-signatures` True - VERSION-DEPENDENT
    (pylint main, 4.1.0-dev0; re-verify against 4.0.6).
24. **radon 6.0.1 (2023-03-26) is the only maintained-enough source of Halstead/MI in Python, and it is
    three years stale.** Its classifiers advertise Python 2.7 and 3.6-3.9 only; `requires_python` is
    empty. xenon 0.9.3 (2024-10-21) wraps it for CI with `--max-absolute/-b`, `--max-modules/-m`,
    `--max-average/-a` (letter grades A-F) plus `--exclude/-e`, `--ignore/-i`, and "will fail (i.e. it
    will exit with a non-zero exit code) when any of these requirements is not met". wily's last stable is
    1.25.0 (2023-10-11) but a **2.0.0a1 prerelease landed 2026-04-26**, so it is not abandoned -
    VERSION-DEPENDENT; treat all three as at-risk dependencies - OPEN (no primary statement of Python 3.14
    support for radon, xenon or wily).
25. **radon CC ranks:** 1-5 A "low - simple block"; 6-10 B "low - well structured and stable block"; 11-20
    C "moderate - slightly complex block"; 21-30 D "more than moderate - more complex block"; 31-40 E
    "high - complex block, alarming"; 41+ F "very high - error-prone, unstable block". Subcommands
    `radon cc | mi | raw | hal`; flags `--min/-n`, `--max/-x`, `--average/-a`, `--total-average`,
    `--show-complexity/-s`, `--json/-j` - ESTABLISHED.
26. **complexipy 6.2.0 is the maintained cognitive-complexity implementation for Python.** Rust-based:
    `complexipy . --max-complexity-allowed 10`, `--output-format json|csv`, `--top N`, `--failed
    --suggest-refactors`, `--plain`. Its docs state plainly that it "is an independent project inspired by
    G. Ann Campbell's research, but it's not affiliated with or endorsed by SonarSource" -
    VERSION-DEPENDENT (6.2.0). ruff implements **no** cognitive-complexity rule - ESTABLISHED (its rules
    table contains none).
27. **SonarPython does not ship a cyclomatic-complexity rule at all.** `S1541` and `S1067` have no Python
    rule metadata (HTTP 404 in the `l10n/py/rules/python` tree). What exists is **S3776** cognitive
    complexity (Critical), **S134** "Control flow statements `if`, `for`, `while`, `try` and `with` should
    not be nested too deeply" (Critical), **S138** "Functions should not have too many lines of code"
    (Major), **S104** "Files should not have too many lines of code" (Major), **S4144** "Functions and
    methods should not have identical implementations" (Major). The `Sonar way` default profile carries
    **393** rule keys - VERSION-DEPENDENT (sonar-python master).
28. **SonarQube metric definitions, verbatim where they bind:** complexity = "Cyclomatic complexity = 1 +
    number of conditional branches"; cognitive complexity = "A qualification of how hard it is to
    understand the code's control flow"; duplication for non-Java languages triggers on "at least 100
    successive and duplicated tokens" spread over 10 lines (20 for ABAP, 30 for COBOL), while Java uses
    "at least 10 successive and duplicated statements", and "Differences in indentation and in string
    literals are ignored"; `duplicated_lines_density = duplicated_lines / lines * 100`;
    `line_coverage = LC / EL`; `branch_coverage = (CT + CF) / (2*B)`; overall
    `coverage = (CT + LC)/(B + EL)`; `sqale_debt_ratio = technical debt / (cost to develop one line *
    lines of code)` with a **default development cost of 30 minutes per line**; maintainability (SQALE)
    rating bands A <=5%, B >=5% to <10%, C >=10% to <20%, D >=20% to <50%, E >=50% - ESTABLISHED.
29. **vulture 2.16 is maintained and honest about its limits.** Python >=3.9 (classifiers through 3.14).
    Confidence values 60-100: 100% for unused function/method/class *arguments* and unreachable code, 90%
    for unused imports, 60% for attributes, classes, functions, methods, properties and variables. Filter
    with `--min-confidence`; generate suppression lists with `--make-whitelist`. Documented caveat: "Due
    to Python's dynamic nature, static code analyzers like Vulture are likely to miss some dead code.
    Also, code that is only called implicitly may be reported as unused" - ESTABLISHED.

### E. Coupling and structure - what can actually be measured

30. **import-linter 2.13 now has SIX contract types**, each with an exact `type` string: `forbidden`
    (`source_modules`, `forbidden_modules`, `as_packages`), `protected` (`protected_modules`,
    `allowed_importers`, `as_packages`), `layers` (`layers`, `containers`, `exhaustive`,
    `exhaustive_ignores`), `independence` (`modules`), `acyclic_siblings` (`ancestors`, `depth` -
    **default 10**, `skip_descendants`), plus custom contract types. All share `ignore_imports` and
    `unmatched_ignore_imports_alerting`. `layers` and `forbidden` check **indirect** import chains, not
    only direct edges - ESTABLISHED. Note for the existing manifest set: only `layers`, `forbidden` and
    `independence` are named anywhere in `manifests/` today.
31. **`acyclic_siblings` is the mechanism for "no package dependency cycles".** It "forbids dependency
    cycles between siblings", drilling down generations to `depth` (default 10). Documented sharp edge:
    "neither the `depth` or `skip_descendants` options prevent deeper imports from being considered when
    analyzing children in earlier generations" - ESTABLISHED.
32. **grimp 3.15 gives you fan-in and fan-out directly**, so module-coupling numbers need no new tool:
    `ImportGraph.find_modules_directly_imported_by(module)` (fan-out),
    `find_modules_that_directly_import(module)` (fan-in), `count_imports()`, `find_downstream_modules` /
    `find_upstream_modules`, `find_shortest_chain(s)`, `chain_exists`,
    `find_illegal_dependencies_for_layers(layers, containers)`, and `nominate_cycle_breakers(package)`.
    `build_graph(..., include_external_packages=, exclude_type_checking_imports=)` controls graph scope -
    ESTABLISHED.
33. **ruff can emit the import graph itself, but it is experimental.** `ruff analyze graph` - "Generate a
    map of Python file dependencies or dependents" - prints JSON
    (`serde_json::to_string_pretty(&import_map)`), with `--direction dependents` for the fan-in view,
    `--detect-string-imports` / `--min-dots`, `--type-checking-imports`, `--python <venv>`. If preview is
    disabled it emits ``warn_user!("`ruff analyze graph` is experimental and may change without
    warning")`` - VERSION-DEPENDENT (ruff 0.16.x); do not build a gate on it yet.
34. **Tach 0.35.0 enforces three things and can be adopted incrementally:** "Imports only come from
    declared dependencies", "Cross-module calls use the public interface", "No cycles in the dependency
    graph". Workflow `tach init` then `tach check`; a violation prints e.g. `tach/check.py[L8]: Cannot use
    'tach.filesystem'. Module 'tach' cannot depend on 'tach.filesystem'.` Config in `tach.toml` with
    `depends_on` and a `deprecated` marker for soft-failing edges - ESTABLISHED. Interface enforcement is
    the capability import-linter lacks.
35. **pydeps 3.0.7 is the visual/cycle tool, not a gate.** `--show-cycles` "show only import cycles"; "any
    cycles in the dependency graph are highlighted as blue boxes by default"; `--max-bacon INT` "exclude
    nodes that are more than n hops away (default=2, 0 -> infinite)"; `--reverse` "draw arrows to (instead
    of from) imported modules"; `--externals` "create list of direct external dependencies". Requires
    Graphviz `dot` on PATH - ESTABLISHED.
36. **Martin's package metrics are well-defined but have no verified Python tool.** *OO Design Quality
    Metrics - An Analysis of Dependencies*, Robert C. Martin, October 28 1994: `Ca` afferent couplings =
    "The number of classes outside this category that depend upon classes within this category"; `Ce`
    efferent couplings; **`I : Instability : (Ce / (Ca+Ce))`, range [0,1], I=0 maximally stable, I=1
    maximally instable**; `A : Abstractness` = abstract classes / total classes, range [0,1]; the "Main
    Sequence" is the A-I line from (0,1) to (1,0); **`D : Distance : |(A+I-1)/sqrt(2)|`** - ESTABLISHED.
    **The 1994 paper contains no cycles/acyclic-dependencies material** (grep for "cycle"/"acyclic"
    returns nothing) - do not cite it for the Acyclic Dependencies Principle - ESTABLISHED. No maintained
    Python implementation of I/A/D was verified this session - OPEN.

### F. Type coverage and ignore-debt as first-class numbers

37. **mypy 2.3.0 emits annotation-coverage reports; these are the measurement, not `--strict`.**
    `--any-exprs-report` produces "a text file report documenting how many expressions of type `Any` are
    present within your codebase"; `--linecount-report` "documenting the functions and lines that are
    typed and untyped within your codebase"; `--lineprecision-report` "a flat text file report with
    per-module statistics of how many lines are typechecked etc.";
    `--html-report`/`--txt-report`/`--cobertura-xml-report` require lxml (`mypy[reports]`) - ESTABLISHED.
38. **The strictness flags that create the debt are separate.** `--disallow-untyped-defs` errors "whenever
    it encounters a function definition without type annotations or with incomplete type annotations";
    `--disallow-incomplete-defs`; `--disallow-any-expr` "disallows all expressions in the module that have
    type `Any`"; and `--strict`, which currently enables exactly `--disallow-any-generics`,
    `--disallow-subclassing-any`, `--disallow-untyped-calls`, `--disallow-untyped-defs`,
    `--disallow-incomplete-defs`, `--check-untyped-defs`, `--disallow-untyped-decorators`,
    `--warn-redundant-casts`, `--warn-unused-ignores`, `--warn-return-any`, `--no-implicit-reexport`,
    `--strict-equality`, `--extra-checks` - VERSION-DEPENDENT (mypy 2.3.0).
39. **Ignore-debt is directly countable and directly gateable.** `--warn-unused-ignores` "will make mypy
    report an error whenever your code uses a `# type: ignore` comment on a line that is not actually
    generating an error message"; **ruff PGH003** `blanket-type-ignore` forces the `# type: ignore[code]`
    form (its docs explicitly cross-reference mypy's `ignore-without-code` error code); **ruff PGH004**
    `blanket-noqa` flags bare `# noqa` and fixes malformed `# noqa F401` -> `# noqa: F401`; **RUF100**
    `unused-noqa` "Checks for `noqa` directives that are no longer applicable" and is always fixable -
    ESTABLISHED. The count of PGH003/PGH004/RUF100 hits plus `type: ignore` occurrences *is* the
    suppression-debt number.
40. **For a library, pyright gives a single defensible type number.** `pyright --verifytypes <IMPORT>` -
    "Verify completeness of types in py.typed package". The **type completeness score** is "the percentage
    of symbols with known types". A symbol counts as unknown/ambiguous when class or instance variables or
    methods lack annotations or refer to unknown types, parameters or return types lack annotations,
    generic classes lack type arguments, or a type alias references partially specified generics.
    `--ignoreexternal` means "any incomplete types that are imported from other external packages are
    ignored"; `--outputjson` makes it machine-readable - ESTABLISHED. It applies only to a `py.typed`
    package's public surface, not to application code.
41. **mypy-baseline 0.7.4 is the ratchet for existing type debt.** `mypy | mypy-baseline sync` records
    current errors to `mypy-baseline.txt`; `mypy | mypy-baseline filter` reports only new ones. It "works
    exclusively with the stdout of mypy" - no plugin, no patching - and claims the baseline is "carefully
    crafted to avoid merge conflicts" and human-readable so reviewers see exactly what was resolved and
    introduced - ESTABLISHED (the project's own claims).
42. **Docstring coverage is a separate, cheaper number.** interrogate 1.7.0 gates with `--fail-under`
    (config default `fail-under = 80`) and has `ignore-*` switches for init/magic/private/nested/
    overloaded/property/setter, plus `ignore-regex`, `whitelist-regex`, `omit-covered-files`,
    `--generate-badge` - VERSION-DEPENDENT (1.7.0). Last release 2024-04-07.

### G. Test-side measurement

43. **coverage.py 7.15.4 branch coverage is opt-in and structurally partial by design.** `coverage run
    --branch` / `[run] branch = True` (default False); it "flags lines that haven't visited all of their
    possible destinations"; partial branches render yellow in HTML "with an annotation at the far right
    showing branch destination line numbers that were not exercised". Documented limits: for constructs
    "such as `while True:` and `if 0:`, coverage.py understands what is going on", but "there are many
    ways in your own code to write intentionally partial branches" that it cannot recognise, and generator
    expressions that never raise `StopIteration` produce false partials - requiring `# pragma: no branch`
    or `[report] partial_branches` regexes - ESTABLISHED.
44. **The coverage gate is exactly one flag and one exit code.** `[report] fail_under` = "A target
    coverage percentage. If the total coverage measurement is under this value, then exit with a status
    code of 2"; the source confirms `OK, ERR, FAIL_UNDER = 0, 1, 2` and a precision-aware
    `should_fail_under(total, fail_under, precision)`. The `coverage report --format` help string reads
    "Output format, either text (default), markdown, or total." - so `--format=total` is the scriptable
    single-number output. Sibling commands: `coverage json | lcov | xml | html | annotate | combine` -
    ESTABLISHED.
45. **Coverage does not measure test quality, and the largest study says so explicitly.** Inozemtseva &
    Holmes, *Coverage Is Not Strongly Correlated with Test Suite Effectiveness*, ICSE 2014: **31,000
    generated test suites over five Java systems of up to 724,000 SLOC**, effectiveness measured by
    mutation kill. Ignoring suite size, Kendall's tau between coverage and non-normalized effectiveness
    was 0.81-0.95 across statement/decision/modified-condition coverage (all significant at the 99.9%
    level). Normalizing effectiveness by covered mutants collapsed it to 0.50-0.83 with HSQLDB at
    **-0.35**. Their conclusion, verbatim: "We found that there is a low to moderate correlation between
    coverage and effectiveness when the number of test cases in the suite is controlled for. In addition,
    we found that stronger forms of coverage do not provide greater insight into the effectiveness of the
    suite. Our results suggest that coverage, while useful for identifying under-tested parts of a
    program, should not be used as a quality target" - ESTABLISHED.
46. **Mutation score is a better signal than coverage - and its own literature is split.** Just, Jalali,
    Inozemtseva, Ernst, Holmes & Fraser, FSE 2014, using **357 real faults in 5 open-source applications
    totalling 321,000 lines**: real faults are "coupled to mutants for **73%** of real faults", and they
    found a "statistically significant correlation between mutant detection and real fault detection,
    independently of code coverage" that is "stronger than the correlation between statement coverage and
    real fault detection" - ESTABLISHED. **Against:** Papadakis, Shin, Yoo & Bae, *Are Mutation Scores
    Correlated with Real Fault Detection?*, ICSE 2018, on CoreBench and Defects4J: "we ... provide
    evidence that all correlations between mutation scores and real fault detection are weak when
    controlling for test suite size", because Just et al. "did not control for the size of the test suites,
    which is a strong confounding factor". Their own reconciliation, verbatim: "By measuring the fault
    detection capability of the top ranked, according to mutation score, test suites (opposed to randomly
    selected test suites of the same size), we find that achieving higher mutation scores improves
    significantly the fault detection. Taken together, our data suggest that mutants provide good guidance
    for improving the fault detection of test suites, but their correlation with fault detection are weak"
    - ESTABLISHED. **Operational reading: mutants are excellent as a targeting diagnostic and poor as a
    scalar KPI.**
47. **mutmut 3.7.0 has an explicit CI gate and a status vocabulary worth knowing.** Statuses: `killed`,
    `survived`, `timeout`, `suspicious`, `skipped`, `no tests`, `not checked`, `segfault`, `check was
    interrupted by user`, and - notably - **`caught by type check`** (exit code 37), meaning the mutant
    was rejected by the type checker before tests ran. `mutmut export-cicd-stats` writes
    `mutants/mutmut-cicd-stats.json`; the source comment states its purpose verbatim: "exports CI/CD stats
    to block pull requests from merging if mutation score is too low". Config lives in `[tool.mutmut]`
    with `paths_to_mutate`, `source_paths`, `tests_dir`, `only_mutate`, `do_not_mutate`,
    `do_not_mutate_patterns`, `also_copy`, `max_stack_depth` (default -1), `mutate_only_covered_lines` -
    ESTABLISHED. Requires `fork`: "if you want to run on windows, you must run inside WSL" - ESTABLISHED.
48. **`caught by type check` is direct evidence for the manifest's thesis.** A mutation the type checker
    rejects is a fault class the type system already forecloses; that bucket is the measured overlap
    between the typing rung and the testing rung - ESTABLISHED (as a mechanism). The *size* of that bucket
    for any given project is OPEN.
49. **Test-suite runtime is measurable with a stdlib-grade flag.** `pytest --durations=N` and
    `--durations-min=THRESHOLD`; documented example "pytest --durations=10 --durations-min=1.0"; and "By
    default, pytest will not show test durations that are too small (<0.005s) unless `-vv` is passed on
    the command-line" - ESTABLISHED.
50. **Flake rate: the honest state of the public evidence.** Google's 2017 post analysing **4.2 million
    tests** reports "larger tests are more flaky" (bucketed by binary size) and that "when a stable test
    became flaky, and we could track it to a specific code change, the problem was a bug in production
    code 1/6th of the time" - ESTABLISHED. The frequently-quoted "1.5% of tests are flaky" figure could
    **not** be confirmed in either the 2016 or the 2017 Google Testing Blog post fetched this session; the
    2016 post is qualitative and a commenter notes they had "nothing publishable" on developer cost -
    OPEN. Do not cite a specific industry flake percentage.

### H. Process signals - and which have evidence

51. **Process metrics beat static code metrics for defect prediction, at scale.** Rahman & Devanbu, "How,
    and why, process metrics are better", ICSE 2013, pp. 432-441, DOI 10.1109/ICSE.2013.6606589 -
    bibliographic record confirmed; findings FLAGGED-SECONDARY (paywalled, not fetched). Independently
    confirmed at scale by Majumder, Mody & Menzies, *Revisiting Process versus Product Metrics: a Large
    Scale Analysis* (arXiv 2008.09569; Empirical Software Engineering, 2022) using "722,471 commits from
    700 Github projects": "process metrics are better predictors for defects than product metrics (best
    process/product-based learners respectively achieve recalls of 98%/44% and AUCs of 95%/54%, median
    values)" - ESTABLISHED. Their own caveat: metric-importance conclusions from small-scale studies shift
    at scale, and they recommend using predictions from multiple models - ESTABLISHED.
52. **Change coupling / temporal coupling is a behavioural, not structural, measure.** CodeScene's docs:
    two or more modules that "change together over time"; "Change coupling isn't possible to calculate
    from code alone", so dependencies are treated "as dynamic and temporal by analyzing developer behavior
    patterns"; hotspots combine "a code health perspective with temporal and organizational data" -
    FLAGGED-SECONDARY (surfaced via search summaries of the versioned CodeScene docs rather than a direct
    page fetch). This is the one coupling signal `import-linter`/`grimp`/`Tach` structurally cannot see,
    which is exactly why it is worth computing from `git log`.
53. **The strongest business-level evidence for code quality is Tornhill & Borg 2022.** *Code Red: The
    Business Impact of Code Quality - A Quantitative Study of 39 Proprietary Production Codebases* (arXiv
    2203.04374, TechDebt 2022), **30,737 files across 39 proprietary production codebases**: low-quality
    code contains **15x more defects**, issue resolution takes **124% more time** on average, and involves
    **9x longer maximum cycle times** (i.e. uncertainty in completion time). Quality was measured with
    **CodeScene**, "a combination of source code analysis, version-control mining, and issue information
    from Jira" - ESTABLISHED. Caveat to state plainly: the independent variable is a proprietary composite
    ("Code Health"), so the result is not reproducible with radon or ruff - ESTABLISHED.
54. **DORA is now FIVE metrics, not four.** dora.dev states the current model as "Change lead time" (from
    committed to version control to deployed in production), "Deployment frequency", "Failed deployment
    recovery time" (**not** "MTTR"), "Change fail rate", and "Deployment rework rate" ("the ratio of
    deployments that are unplanned but happen as a result of an incident in production"). The page says
    the metrics "have evolved alongside the technology landscape: shifting from the original four keys to
    the current five-metric model" - VERSION-DEPENDENT (page state 2026-08-08). Any manifest text saying
    "the four DORA keys" is now out of date.
55. **DORA's performance bands and methodology could not be confirmed from a primary page this session.**
    Neither `dora.dev/guides/dora-metrics-four-keys/` nor `dora.dev/research/` published the
    elite/high/medium/low numeric thresholds or a statement on survey methodology in the fetched content -
    OPEN. Widely-repeated 2024 figures (elite: on-demand deploys, lead time <1 day, change fail ~5%,
    recovery <1 hour) are FLAGGED-SECONDARY. Do not print a DORA band table without fetching the current
    report.

### I. Ratcheting mechanisms that exist and were verified

56. **The canonical ratchet is a new-code quality gate, and SonarQube's default is exactly six conditions,
    all scoped to new code:** no new bugs (Reliability rating A), no new vulnerabilities (Security rating
    A), new code has limited technical debt (Maintainability rating A), all new Security Hotspots
    reviewed, **new code test coverage >= 80.0%**, **duplication in new code <= 3.0%** - ESTABLISHED.
    "New code" is definable as previous version, last X days, a specific analysis, or a reference branch.
    The documented rationale for why this converges: "When you add new code to your projects, you usually
    touch a portion of the old code in the process. As a consequence, analyzing and cleaning new code
    allows you to fix issues in your old code and gradually improve the overall quality of your codebase"
    - ESTABLISHED.
57. **diff-cover 10.4.2 is the self-hosted equivalent for the coverage half.** "Diff coverage is the
    percentage of new or modified lines that are covered by tests. This provides a clear and achievable
    standard for code review: If you touch a line of code, that line should be covered." It compares an
    XML (Cobertura/Clover/JaCoCo) or LCov report against `git diff`, requires git, and can also report
    violations from pycodestyle, pyflakes, flake8 or pylint - ESTABLISHED.
58. **ruff's own ratchet levers.** `ruff check --statistics` (per-rule counts, for tracking a number over
    time); `--add-noqa[=reason]` "Enable automatic additions of `noqa` directives to failing lines.
    Optionally provide a reason to append after the codes."; `--add-ignore[=reason]` for `ruff: ignore`
    range suppressions; file-level `# ruff: noqa` / `# ruff: noqa: {code}` must be on its own line; ruff
    also honours `# flake8: noqa` as equivalent to `# ruff: noqa`. Range suppressions "do not support
    'blanket' suppression" - VERSION-DEPENDENT (ruff 0.16.x).

## The routing table

| hazard / practice | why it bites | enforcement route | exact mechanism (rule code / flag / checker / test kind) | residual risk |
|---|---|---|---|---|
| Function control flow too tangled to test | Basis-path count grows past any feasible test set | lint-catchable | `ruff` **C901** `complex-structure`, `lint.mccabe.max-complexity` (default **10**); `radon cc -n C`; CI gate `xenon --max-absolute B` | Passing C901 says nothing about understandability (Shepperd; Campbell). CC is a testability proxy only |
| Function does too many things (branch count) | Change lands in the wrong branch | lint-catchable | `ruff` **PLR0912** / `pylint` **R0912** `too-many-branches`, `max-branches` **12** | Splitting to pass the gate can raise total system complexity (Shepperd's structural objection) |
| Function too long | Reviewers stop reading before the end | lint-catchable | `ruff` **PLR0915** / `pylint` **R0915** `too-many-statements`, `max-statements` **50**; Sonar **S138** | Statement count is a size proxy; a 49-statement function is not thereby good |
| Too many parameters | Call sites become positional soup | lint-catchable | `ruff` **PLR0913** / `pylint` **R0913** `too-many-arguments`, `max-args` **5** | Encourages smuggling params into a dict or config object, which no linter can see |
| Positional-argument ambiguity at call sites | Silent argument transposition, same types | feature-eliminated + lint-catchable | Keyword-only marker `*` in the signature; enforced by `ruff` **PLR0917** (stable since ruff **0.16.0**) / `pylint` **R0917**, `max-positional-args` **5** | Callers can still pass the wrong same-typed keyword; only `NewType`/distinct types close that |
| Too many exits | Post-conditions unprovable by reading | lint-catchable | `ruff` **PLR0911** / `pylint` **R0911** `too-many-return-statements`, `max-returns` **6** | Early return is often the *fix* for nesting; this gate and the nesting gate pull against each other |
| Deep nesting | Reader must hold N conditions in working memory | lint-catchable (preview) | `ruff` **PLR1702** `too-many-nested-blocks` (**PREVIEW**, needs `--preview`), `max-nested-blocks` **5**; `pylint` **R1702**; Sonar **S134** | Preview rules can change or be renamed without a major bump - pin ruff exactly if you gate on it |
| Boolean condition nobody can evaluate | Mixed `and`/`or` precedence bugs | lint-catchable (preview) | `ruff` **PLR0916** `too-many-boolean-expressions` (**PREVIEW**), `max-bool-expr` **5**; `pylint` **R0916** | Extracting to a named predicate moves the complexity, does not remove it |
| God class | Every change touches it | lint-catchable (preview) | `ruff` **PLR0904** `too-many-public-methods` (**PREVIEW**), `max-public-methods` **20**; `pylint` **R0902** `too-many-instance-attributes` (**7**), **R0903**/**R0904** | Counting methods cannot detect a class with 3 methods and 8 responsibilities |
| Code that is legal, small, and still unreadable | CC scores it as fine | external checker | Cognitive complexity: `complexipy 6.2.0 --max-complexity-allowed N`; or SonarQube/SonarPython **S3776** (default threshold **15**, `Critical`, `MAINTAINABILITY: HIGH`) | Only moderate empirical validation (ESEM 2020: correlates with comprehension *time* and subjective ratings; mixed for correctness). ruff has no cognitive-complexity rule |
| Maintainability Index used as a gate | Unvalidated constants; averages a power law | **contract-only - reject the gate** | `radon mi` may be *reported*; nothing should fail on it. If a number is demanded, gate CC and SLOC separately | Two incompatible MI formulas share the name (radon adds a comment term Microsoft's lacks); scores are not portable |
| Dead code accumulating | Readers pay attention tax on code that cannot run | lint-catchable, partial | `vulture 2.16 --min-confidence 100` in CI, lower tiers as diagnostic; `ruff` **F401** unused import, **F841** unused local; `ruff` **ERA001** `commented-out-code` | Vulture's docs concede dynamic dispatch and implicit calls yield both misses and false positives. Only the 100% tier is gate-safe |
| Copy-paste divergence | Fix applied to one clone only | lint-catchable | `pylint` **R0801** `duplicate-code`, `min-similarity-lines` **4**; Sonar **S4144** identical implementations; SonarQube `duplicated_lines_density` (100 tokens over 10 lines) | Token/line similarity misses semantic duplication; `ignore-signatures=True` by default hides some real clones |
| Layer inversion (low imports high) | Dependency direction rots silently | fitness-function | `import-linter 2.13` `type = layers` with `layers`/`containers`/`exhaustive`; run `lint-imports` in CI | Checks the import graph only. A green run proves nothing about behaviour - claiming otherwise is a category error |
| Two features must not know each other | Hidden coupling via a shared helper | fitness-function | `import-linter` `type = independence`, `modules = [...]` (catches indirect chains) | `ignore_imports` entries silently accumulate; pair with `unmatched_ignore_imports_alerting` |
| Internal module imported past its front door | The public API contract is fictional | fitness-function | `import-linter` `type = protected` with `protected_modules` / `allowed_importers`; or `Tach` interface enforcement | Import-level only: nothing stops `getattr`, plugin loading, or `importlib` access |
| Package dependency cycles | No module can be understood or tested alone | fitness-function | `import-linter` `type = acyclic_siblings` (`ancestors`, `depth` default **10**, `skip_descendants`); `Tach` "No cycles in the dependency graph"; `pydeps --show-cycles` as the diagnostic view | Documented sharp edge: `depth`/`skip_descendants` do not stop deeper imports contributing to a shallower cycle |
| Undeclared cross-module dependency | Architecture drifts one import at a time | fitness-function | `Tach 0.35.0`: `tach.toml` `depends_on` + `tach check`; `deprecated` marker for soft-fail during migration | Module granularity is whatever you declared; one giant module passes trivially |
| Fan-in / fan-out drift | The module everything imports becomes unchangeable | fitness-function (custom script) | `grimp 3.15`: `find_modules_that_directly_import()` (fan-in), `find_modules_directly_imported_by()` (fan-out), `count_imports()`, `nominate_cycle_breakers()`. Preview alternative: `ruff analyze graph --direction dependents` (JSON) | No tool ships a fan-in threshold; you must pick and defend one. `ruff analyze graph` self-declares "experimental and may change without warning" |
| Instability / abstractness off the Main Sequence | Stable-and-concrete packages block change | **contract-only in Python** | Martin 1994 defines `I = Ce/(Ca+Ce)`, `A`, `D = |(A+I-1)/sqrt(2)|`; computable from `grimp` if wanted | No maintained Python implementation verified. `A` needs an "abstract class" definition Python does not enforce (ABC? Protocol? both?) |
| Untyped code re-entering a typed codebase | Contracts stop being contracts | type-catchable | `mypy --disallow-untyped-defs` / `--disallow-incomplete-defs` / `--strict`; measure with `--linecount-report`, `--lineprecision-report`, `--any-exprs-report` | `Any` propagates silently through inference; `--disallow-any-expr` is usually unusable in practice |
| A library ships incomplete public types | Downstream users silently get `Any` | type-catchable | `pyright --verifytypes <pkg> --ignoreexternal --outputjson` -> **type completeness score** = "the percentage of symbols with known types" | Applies only to a `py.typed` package's public surface; says nothing about internals or correctness |
| Blanket `# type: ignore` | Suppresses the next, unrelated, real error | lint-catchable | `ruff` **PGH003** `blanket-type-ignore`; `mypy --enable-error-code=ignore-without-code` | A *coded* ignore still hides that specific error forever unless paired with the next row |
| Stale suppressions never removed | Debt count stops falling even as code improves | lint-catchable | `ruff` **RUF100** `unused-noqa` (always fixable); `mypy --warn-unused-ignores` (inside `--strict`) | RUF100 ignores codes unknown to ruff; with `--fix` alongside other linters you must separate directives with a second `#` or they are deleted |
| Blanket `# noqa` | Whole-line lint blindness | lint-catchable | `ruff` **PGH004** `blanket-noqa` (fixes `# noqa F401` -> `# noqa: F401`) | Ruff also honours `# flake8: noqa` as a file-level blanket - easy to miss in review |
| Type-error debt not monotonically shrinking | "We'll type it later" never arrives | fitness-function | `mypy-baseline 0.7.4`: `mypy \| mypy-baseline sync` then `mypy \| mypy-baseline filter` in CI | The baseline can be re-synced upward by anyone; the ratchet is social unless CI forbids growth of the file |
| Untested lines and unexercised branches | Error paths are precisely the untested ones | test-catchable | `coverage 7.15.4` with `[run] branch = True`; `[report] fail_under` -> **exit code 2**; `coverage report --format=total` for the scalar | Branch coverage is structurally partial: `while True:` is understood, generator-expression non-exhaustion is a false partial needing `# pragma: no branch` |
| New code lands untested | Legacy debt becomes the excuse for all new debt | fitness-function | `diff-cover 10.4.2` against a Cobertura/LCov report + `git diff`; SonarQube new-code gate (coverage **>=80.0%**, duplication **<=3.0%**) | Diff coverage rewards touching few lines; a large honest refactor can score worse than a one-line hack |
| Assertion-free or shallow tests passing the coverage gate | The coverage number is fully gameable | test-catchable | `mutmut 3.7.0 run`; `mutmut export-cicd-stats` -> `mutants/mutmut-cicd-stats.json` ("to block pull requests from merging if mutation score is too low"); `cosmic-ray 8.4.6` as alternative | Mutation score correlates with real-fault detection only weakly once suite size is controlled (Papadakis 2018). Requires `fork` (WSL on Windows). Runtime is the real blocker |
| Fault classes the type checker already forecloses | Tests written for what mypy already proves | measurement of the overlap | `mutmut` status **`caught by type check`** (exit code 37) | Bucket size is project-specific and unmeasured in the literature - report it, never target it |
| Flaky tests | Every red build becomes "just re-run it" | test-catchable | Quarantine plus repeated execution; measure per-test pass rate over N CI runs; `pytest --durations` to find timeout-prone tests | No verified public base rate to compare against (Fact 50). Re-running to green destroys the signal being measured |
| Test suite too slow to run per-change | Feedback loop collapses; people stop running it | test-catchable | `pytest --durations=N --durations-min=1.0`; track wall-clock as a budgeted number | Suite time can be "improved" by deleting slow integration tests - pair the budget with a test-count floor |
| Undocumented public API | Readers reverse-engineer intent from bodies | lint-catchable | `interrogate 1.7.0 --fail-under 95` (config default **80**); `ruff` pydocstyle (`D`) rules for shape | Presence of a docstring is not correctness of a docstring. Purely a shape check |
| Hotspots: complex code that also changes constantly | The intersection is where cost concentrates | **diagnostic only** | `git log` churn per file x `radon cc`; `wily` for the historical series; CodeScene for the commercial version | Tornhill & Borg's 15x/124% result used proprietary "Code Health"; it does **not** transfer to a radon-based reimplementation |
| Delivery health (are we actually shipping?) | Every code metric can be green on a team that ships nothing | process metric, never a code gate | DORA's five: change lead time, deployment frequency, failed deployment recovery time, change fail rate, deployment rework rate | Bands and methodology unconfirmed from primary sources (Fact 55). Team-level only; per-developer use is an abuse |
| "Is this the right abstraction / do the names mean what they say / is the domain model right" | The actual determinant of maintainability | **contract-only** | Human review. No mechanism verified, none exists | This is the largest residual risk in the whole table and must be stated as such |

## What the existing manifests already cover

- **`python_testing_tooling_manifest.md` §"Coverage tooling", Key Findings, and Recommendation 5** already
  owns: coverage.py mechanics (line and branch, `coverage run` / `report -m` / `html`, `pytest-cov`
  optionality, the "sysmon" measurement core default on Python 3.14+), Fowler's *TestCoverage* quotes, the
  explicit Goodhart framing, "upper 80s or 90s ... suspicious of anything like 100%", and the "flashlight
  not target" recommendation. **Do not restate any of this.** The delta is: branch coverage's *documented
  structural limits*, the `fail_under` -> exit-code-2 mechanism, `--format=total`, diff coverage as the
  ratchet, mutation score with **both** sides of its literature, flake rate, and suite runtime. Also a
  version delta to reconcile: that manifest pins coverage.py **7.14.1**; current is **7.15.4**
  (2026-08-06).
- **`python_testing_tooling_manifest.md` §2 and §5** own the unit/integration boundary and "specify
  obligations, not tests". Measurement text should defer to them rather than re-argue that behaviour, not
  structure, is what is being verified.
- **`spec_recovery_reverse_engineering_manifest.md` §9 "Executable conformance for the structural
  subset"** already owns: fitness functions (Ford/Parsons/Kua), ArchUnit as the Java analogue,
  import-linter's `layers`/`forbidden`/`independence` contract types, and - importantly - the hard
  boundary that these verify **structure only**, with the verbatim rule "Do not claim a green
  import-linter run as evidence of behavioral conformance - it is a category error". The delta is:
  import-linter **2.13**'s two additional contract types (`protected`, `acyclic_siblings`), `grimp` as the
  measurable graph API, `Tach`'s interface enforcement, `ruff analyze graph`, and boundary-violation
  **counts as a tracked number** rather than a boolean.
- **`spec_recovery_reverse_engineering_manifest.md` §6-§7** already cite Tornhill's *Code as a Crime
  Scene* and the Git Forensics tradition for classifying divergence from commit messages. The delta is the
  *quantitative* behavioural-code-analysis result (Code Red, 2022) and change coupling as a metric.
- **`python_typing_contract_manifest.md` §1** owns checker strict modes; §4 owns "What the type system
  CANNOT express". The delta is purely measurement: annotation-coverage reports, the ignore-debt count,
  `pyright --verifytypes`, and the ratchet.
- **`architecture_manifest_default.md` §3.1** owns coupling and cohesion as reasoning vocabulary
  (reasoning register - do not retrofit metrics or epistemic tags into it). At most add one
  cross-reference line pointing at the new gates file for the mechanised versions.
- **Nothing in `manifests/` currently mentions** radon, xenon, wily, vulture, complexipy, mutmut,
  diff-cover, interrogate, grimp, Tach, pydeps, mypy-baseline, Halstead, McCabe, the Maintainability
  Index, cognitive complexity, cyclomatic complexity, C901, any `PLR09xx` code, `PGH003`, `PGH004`,
  `RUF100`, annotation coverage, mutation score, churn, flake rate, DORA, or ratcheting. The measurement
  rung is effectively greenfield.

## New content the manifest set should carry

**1. "Two questions, two metrics: testability vs understandability"** -> NEW:
`python_quality_gates_manifest.md`
Establish the split up front so agents stop conflating them. Cyclomatic complexity answers *how many
paths must a test suite cover* - McCabe's own framing, NIST's limit of 10 carrying its verbatim "remains
somewhat controversial" hedge. Cognitive complexity answers *how hard is this to read* - Campbell's three
rules, the four increment types, the deliberate discounts (methods free, `switch` one point, like-operator
sequences one point, `try`/`finally` ignored). State that the white paper contains no threshold and that
15 is SonarQube's `DEFAULT_THRESHOLD`. Close with the ESEM 2020 validation and its mixed findings, so the
agent knows which of the two has any human-subject support at all.

**2. "What complexity does not predict - the sceptical record"** -> NEW:
`python_quality_gates_manifest.md`
Four paragraphs, each anchored. Shepperd 1988's verbatim "no more than a proxy for, and in many cases is
outperformed by, lines of code", plus "over a third of the studies". The contested CC-vs-SLOC question:
Graylin et al. 2009 (FLAGGED-SECONDARY) against Landman et al.'s 17.6M methods and their conclusion that
the correlation "is not strong enough to conclude that CC is redundant with SLOC". The unit-of-analysis
resolution: gate per function, never report project-average CC. Then the MI takedown: two incompatible
formulas under one name, a 1994 HP calibration never redone, averaging over a power-law distribution, no
published justification for the 20/10 cutoffs. Verdict line: *report MI if you like; never fail a build on
it.*

**3. "The gate/diagnostic register" (the Goodhart section)** -> NEW:
`python_quality_gates_manifest.md`
A three-column table whose third column is "what this threshold is NOT evidence of" - the column that
stops the number becoming the goal. Gate-safe: per-function C901 <= 10; PLR0912/PLR0913/PLR0915 at
defaults; import-linter/Tach violation count == 0; `mypy --strict` clean on new modules; new-code coverage
via diff-cover; suppression count non-increasing. Diagnostic-only: total and average CC, MI, Halstead,
mutation score, vulture below 100% confidence, hotspots, fan-in. Forbidden as gates: MI, project-average
anything, total coverage percentage as a rising target, mutation score as a KPI. Include the reasoning: a
gate must be (a) per-unit not aggregate, (b) monotone under genuine improvement, (c) not satisfiable by
deletion, (d) cheap enough to run on every commit.

**4. "The starter set: seven numbers for a small project"** -> NEW:
`python_quality_gates_manifest.md`
The concrete recommendation, each item with a defensible threshold and an explicit disclaimer. (i) C901
<= 10 per function - *not* evidence of readability. (ii) Cognitive complexity <= 15 per function via
complexipy - *not* evidence of correct decomposition. (iii) import-linter/Tach violations == 0 - *not*
evidence of behavioural conformance. (iv) Branch coverage with `fail_under` pinned to the current floor,
plus diff-cover >= 80% on changed lines - *not* evidence of test quality (cite Inozemtseva verbatim). (v)
Suppression debt (`type: ignore` + `noqa` + baseline lines) monotonically non-increasing - *not* evidence
of type soundness. (vi) Suite wall-clock under a stated budget - *not* evidence of adequate testing. (vii)
Mutation score on the functional core, reviewed quarterly, never gated. State that seven is already a lot
and that adding an eighth needs a written reason.

**5. "Ratcheting: how to adopt a standard without a rewrite"** -> NEW:
`python_quality_gates_manifest.md`
The mechanism inventory, with the concept named from SonarQube's Clean as You Code and its verbatim
rationale about touching old code as you add new. `mypy-baseline sync`/`filter`; `diff-cover`;
`ruff --statistics` as the tracked count and `--add-noqa=<reason>` as the one-time baseline (with the
warning that it is a debt-*creation* tool); coverage `fail_under` pinned to the current floor and raised
only once already exceeded; Tach's `deprecated` marker for soft-failing an edge during migration. The rule
to state: a ratchet is a *floor that only moves up*, and CI must fail on regression, not on absolute
badness.

**6. "Coupling as a number, not a feeling"** -> `python_module_boundaries_manifest.md` (owner of
import-linter/Tach per PLAN.md), with the tracked-number framing cross-referenced from the gates file
All six import-linter 2.13 contract types with exact `type` strings and options, including
`acyclic_siblings` (`depth` default 10) and `protected`, plus the documented sharp edge about `depth` not
stopping deeper imports. `grimp`'s fan-in/fan-out API as the way to compute a coupling number without a
new dependency. Tach's three enforcements including public-interface checking, which import-linter does
not do. `pydeps --show-cycles` and `--max-bacon` as the diagnostic view. `ruff analyze graph --direction
dependents` with its experimental warning quoted. Martin's I/A/D definitions as vocabulary, tagged OPEN
for lack of a Python implementation, with the explicit note that the 1994 paper says nothing about cycles.

**7. "Type coverage and ignore-debt"** -> NEW: `python_quality_gates_manifest.md`, deferring contract
semantics to `python_typing_contract_manifest.md`
mypy's four report flags and exactly what each contains; the distinction between *strictness* (creates
errors) and *coverage* (counts annotations). The suppression-debt formula: `type: ignore` occurrences +
`noqa` occurrences + mypy-baseline lines, tracked as one monotone number. The three ruff rules that keep
it honest (PGH003, PGH004, RUF100) plus `--warn-unused-ignores`. `pyright --verifytypes` for libraries
only, with the completeness-score definition quoted and the scope caveat stated.

**8. "Test-side measurement beyond coverage"** -> `python_testing_tooling_manifest.md` (extends its
existing coverage section; do not duplicate the Fowler/Goodhart material)
Branch coverage's documented structural limits and the `# pragma: no branch` / `partial_branches` escape
hatches. The `fail_under` -> exit 2 mechanism and `--format=total`. Then mutation testing with both sides
on the record: Just et al.'s 73% coupling and "stronger than statement coverage", Papadakis et al.'s "all
correlations ... are weak when controlling for test suite size" together with their reconciliation that
top-mutation-score suites do detect significantly more faults. mutmut's status vocabulary including
`caught by type check` as the measured typing/testing overlap. `pytest --durations` and suite runtime as a
maintainability property in its own right. Flake rate with the honest OPEN on base rates.

**9. "Process signals: what git knows that the AST does not"** -> NEW:
`python_quality_gates_manifest.md`, cross-referencing
`spec_recovery_reverse_engineering_manifest.md` §6-§7
Change coupling as the coupling that structural tools cannot see, quoting "Change coupling isn't possible
to calculate from code alone". Churn x complexity hotspots as prioritisation, not as a gate. The evidence
tier: Majumder/Mody/Menzies' 700 projects and 98%/44% recall as the strong result for process over product
metrics; Tornhill & Borg's 15x defects / 124% time / 9x cycle-time with the explicit caveat that the
independent variable was proprietary. DORA's **five** metrics with the correct current names, and the
honest note that bands and methodology were not confirmable from primary sources.

**10. "What cannot be measured"** -> NEW: `python_quality_gates_manifest.md`, final section before
anti-patterns
Named, one line each, as a review checklist: is the abstraction at the right level; do the names mean what
they say; is the domain model right; is this the simplest thing that could work; is the error message
actionable to the person reading it at 3am; is the test asserting behaviour or implementation; does the
module boundary fall on a real seam of change; is the concurrency model justified. State plainly that
every mechanised gate above is a *lower bound on badness*, not evidence of any of these, and that a fully
green pipeline over an incoherent design is the normal case, not an anomaly.

## Traps for coding agents

1. **`radon cc` and `ruff C901` give different numbers for the same function - thresholds are not
   portable.** Read from source: radon (`radon/visitors.py`) counts `Try` as `len(node.handlers) +
   bool(node.orelse)`, **`BoolOp` as `len(node.values) - 1`**, `If`/`IfExp` as 1, `Match` as `len(cases)`
   minus a wildcard case, `For`/`While`/`AsyncFor` as `1 + bool(orelse)`, **`comprehension` as
   `len(node.ifs) + 1`**, and **`assert` as 1** (unless `no_assert`); lambdas are deliberately not counted
   (radon issue #68). Ruff's `function_is_too_complex.rs` walks **statements only**: `If` +1 (+1 per
   `elif`/`else` clause), `For`/`While` +1 (ignoring their `else`), `Match` +1 per case, `Try` +1 per
   handler, **nested `FunctionDef` +1**, `With` +0, `ClassDef` +0 - and **no `BoolOp`, no comprehension,
   no `assert`**. A function full of `and`/`or` and comprehensions therefore scores high in radon and low
   in ruff. Never migrate a threshold between the two without re-measuring.
2. **Four of the most-wanted "too-many-*" ruff rules are preview-only and silently do nothing without
   `--preview`:** PLR0904, PLR0914, PLR0916, PLR1702. An agent that adds them to `select`, sees a clean
   run, and reports success has learned nothing. Conversely PLR0917 **became stable in ruff 0.16.0**, so
   config written against an older ruff may start failing on upgrade.
3. **`ruff --add-noqa` is a debt-creation tool wearing a fix's clothing.** It writes suppressions for
   *every* current violation. Used once, deliberately, with `=<reason>` and committed as an explicit
   baseline, it is a ratchet. Used because CI was red, it deletes the signal.
4. **`RUF100 --fix` will delete other tools' directives.** Ruff's own docs: when running RUF100 with
   `--fix` alongside pylint or mypy, "separate their directives with a second `#` character to prevent
   removal". An agent running `ruff check --fix --select RUF100` over a repo with `# noqa` comments meant
   for flake8 plugins ruff does not implement can strip working suppressions. RUF100 also ignores codes
   unknown to ruff by design - use the `invalid-rule-code` rule if you want those flagged.
5. **`PGH004 --fix` "may introduce additional diagnostics".** Turning `# noqa F401` into `# noqa: F401`
   makes a previously-blanket suppression specific, which un-suppresses everything else on that line.
   That is correct behaviour and a surprising build break.
6. **`ruff analyze graph` requires preview and self-declares instability.** With preview off it emits
   ``"`ruff analyze graph` is experimental and may change without warning"``. Its JSON shape is not a
   stable contract. Do not build a CI gate on it in 2026; use `grimp` for anything load-bearing.
7. **Radon's MI is not Visual Studio's MI even though radon calls it "the one used in Visual Studio".**
   Radon adds `+ 50 sin(sqrt(2.4 C))` for comment percentage; Microsoft's published formula has no comment
   term. A file can be rank A in radon and Yellow in Visual Studio. Radon's ranks (A 100-20, B 19-10, C
   9-0) also collapse Microsoft's three bands differently.
8. **radon 6.0.1, xenon 0.9.3 and wily 1.25.0 all predate current Python.** radon's `requires_python` is
   empty and its classifiers stop at 3.9. They may work (radon's CC uses the host interpreter's `ast`),
   but no primary source claims Python 3.14 support. Verify on the target interpreter before making any of
   them a required CI step - and note that wily's `2.0.0a1` (2026-04-26) is a **prerelease**, so a plain
   `pip install wily` will not pick it up.
9. **Coverage's `fail_under` exits 2, not 1.** `OK, ERR, FAIL_UNDER = 0, 1, 2`. A CI script testing
   `if [ $? -eq 1 ]` to distinguish "tests failed" from "coverage too low" has it backwards. The
   comparison is also precision-aware (`should_fail_under(total, fail_under, precision)`), so
   `fail_under = 90` with `precision = 0` passes at 89.5%.
10. **Branch coverage produces false partials that require annotation, not test-writing.** Generator
    expressions that never exhaust, and deliberately partial branches, report as missed. An agent that
    "fixes" these by adding tests is writing tests for nothing; the correct fix is `# pragma: no branch` or
    a `[report] partial_branches` regex. Coverage's docs say it understands only a few idioms such as
    `while True:` and `if 0:`.
11. **SonarPython has no cyclomatic-complexity rule, so "enable Sonar's complexity rule" is ambiguous.**
    `S1541` and `S1067` do not exist for Python. What exists is S3776 (cognitive), S134 (nesting depth),
    S138 (function lines), S104 (file lines), S4144 (identical implementations).
12. **S3776 skips inner functions.** The Python check returns early on `isInnerFunction(functionDef)`. A
    deeply nested closure inside a simple outer function is not reported separately - its complexity is
    attributed to the enclosing function, or missed. `complexipy` and ruff do not share this behaviour, so
    the three tools disagree on closure-heavy code.
13. **`mypy --strict` is not a coverage measurement and does not report one.** It creates errors; it does
    not tell you what fraction of your code is annotated. That needs `--linecount-report` /
    `--lineprecision-report` / `--any-exprs-report`, and the lxml-dependent formats need `mypy[reports]`
    installed or they fail at runtime.
14. **`pyright --verifytypes` measures a *package's public API*, not your application.** Run on an
    application package it yields a number that means very little; without `--ignoreexternal` it also
    penalises you for your dependencies' missing types.
15. **pylint's duplicate-code checker ignores signatures and imports by default** (`ignore-signatures`
    True, `ignore-imports` True, `ignore-comments` True, `ignore-docstrings` True,
    `min-similarity-lines` 4). Two near-identical functions can go unreported. The module was also renamed
    to `symilar.py`, so any code or doc referring to `pylint/checkers/similar.py` is stale.
16. **`vulture` at default confidence is not gate material.** Only the 100% tier (unused arguments,
    unreachable code) is reliable; the 60% tier covers attributes, classes, functions, methods, properties
    and variables, where dynamic access, plugin registries and framework hooks generate false positives.
    Vulture's own docs concede errors in both directions. Gate at `--min-confidence 100`; diagnose below.
17. **Read tool defaults from source, not from summaries.** `lint.pylint.max-locals` is **15** in ruff's
    `settings.rs` and in the `too-many-locals` rule prose ("up to fifteen locals"), matching pylint's 15 -
    not 5. A settings table read carelessly can produce a wrong default that then propagates into config.
    Verify against `settings.rs` / `design_analysis.py`.
18. **Extracting a function to satisfy a complexity gate can make the system worse and the metric
    better.** Shepperd's documented objection: CC can increase when applying accepted structuring
    techniques, and inter-modular complexity - coupling and cohesion - is "not adequately captured by the
    metric". A gate that rewards fragmentation produces forty three-line functions with a tangled call
    graph, and every metric will be green.
19. **PLR0911 (too-many-returns) and PLR1702 (too-many-nested-blocks) fight each other.** Early return is
    the standard remedy for nesting; nesting is the standard consequence of forbidding returns. Pick one
    and disable the other, or the agent will oscillate between them across commits.
20. **Mutation testing on Windows silently is not an option.** mutmut "must be run on a system with `fork`
    support ... if you want to run on windows, you must run inside WSL". Adding `mutmut run` to a Windows
    CI matrix adds a guaranteed failure.
21. **"DORA four keys" is stale vocabulary.** dora.dev now documents five metrics and renamed MTTR to
    "failed deployment recovery time", adding "deployment rework rate". Writing "the four DORA metrics
    (MTTR ...)" in 2026 is a datable error.
22. **Do not reimplement Tornhill's result with radon and claim it.** The 15x-defects / 124%-time figures
    come from CodeScene's proprietary "Code Health", not from cyclomatic complexity. A churn x CC hotspot
    list is a legitimate diagnostic; it is not the measured construct from *Code Red*.
23. **Citing "15" as the cognitive-complexity limit and attributing it to Campbell is a fabrication.** The
    white paper (v1.7, 2023-08-29) states no threshold anywhere. 15 is
    `CognitiveComplexityFunctionCheck.DEFAULT_THRESHOLD` in sonar-python.
24. **Citing Martin 1994 for the Acyclic Dependencies Principle is wrong.** *OO Design Quality Metrics*
    defines Ca, Ce, I, A, D and the Main Sequence, and contains no cycle material at all.

## Honest limits

- **No metric in this pack has been validated against maintenance effort in Python.** Every empirical
  study cited used Java, C, or a proprietary multi-language tool. The Landman corpus is Java and C; the
  Inozemtseva, Just and Papadakis studies are Java (plus C for CoreBench); the MI calibration is C and
  Pascal from the late 1980s at Hewlett-Packard; Campbell's validation meta-analysis is language-mixed but
  not Python-specific. Transferring thresholds to Python is an assumption, not a finding - OPEN.
- **The single most-repeated claim about complexity - that it is redundant with lines of code - is
  contested and depends on the unit of aggregation.** Shepperd (1988) and SonarSource's own white paper
  both say CC tracks LOC above the method level; Landman et al. say the correlation at function level is
  "only moderate" and insufficient to call CC redundant. The manifest must state both and pick a unit of
  analysis, not pick a side.
- **Cyclomatic complexity's canonical threshold is a convention with a published hedge.** NIST SP 500-235
  says 10 has "significant supporting evidence" *and* that the number "remains somewhat controversial",
  and that 15 has been used successfully. Any project's chosen number is therefore a decision to be
  recorded, not a fact to be cited - OPEN, addressed to the project (cf.
  `software_spec_discipline_manifest.md` §G5).
- **The Maintainability Index rests on constants nobody has re-derived in thirty years**, is computed by
  averaging over a power-law-distributed population, and is published under one name with at least two
  different formulas. Van Deursen could find no justification for Visual Studio's 20/10 thresholds; this
  session found none either - OPEN.
- **Cognitive complexity's specification is a set of rules chosen to match programmer intuition, not a
  derived model.** The white paper says so openly: it "breaks from the use of mathematical models". Its
  strongest validation (ESEM 2020) found correlation with comprehension *time* and *subjective ratings*,
  but "mixed results" for comprehension correctness and physiological measures. It is the best-supported
  complexity metric available, and that support is moderate.
- **Coverage and mutation score are both weaker than their reputations, in opposite directions.** Coverage
  "should not be used as a quality target" (Inozemtseva & Holmes, verbatim). Mutation score's correlation
  with real-fault detection is "weak when controlling for test suite size" (Papadakis et al.), yet
  deliberately raising mutation score "improves significantly the fault detection" (same paper). Both are
  true; a manifest reporting only one is misleading.
- **Structural architecture checks verify the import graph and nothing else.** This is already stated in
  `spec_recovery_reverse_engineering_manifest.md` §9 and remains the sharpest limit: a green
  import-linter/Tach run is evidence about who-imports-whom, not about layering *intent*, not about
  runtime coupling through `importlib`/`getattr`/plugin registries, and not about behaviour.
- **Martin's instability and abstractness are definable but not currently measurable in Python by any
  verified tool**, and `A` (abstract classes / total classes) has no unambiguous Python meaning - ABC?
  `Protocol`? both? - OPEN; a definition the project must pin before the number means anything.
- **No public flake-rate base rate was confirmable.** The circulated "1.5% of tests are flaky" figure is
  not in the Google Testing Blog posts fetched this session - OPEN. A project's own flake rate is
  measurable but not benchmarkable.
- **DORA's performance bands and survey methodology were not obtainable from primary pages this session** -
  OPEN. The five metric *names and definitions* are confirmed; the numbers people quote are
  FLAGGED-SECONDARY.
- **Process metrics outperform product metrics for defect prediction, which is uncomfortable for this
  whole document.** The strongest large-scale result (700 projects, 722,471 commits) puts process-metric
  recall at 98% against 44% for static code metrics. If the goal is finding where defects will be, git
  history beats the AST. Static gates remain worth having - they are cheap, per-commit, and prevent
  specific defect classes outright - but they must not be sold as the best available predictor.
- **The economically strongest code-quality result is not reproducible with open tools.** Tornhill &
  Borg's 15x / 124% / 9x findings used CodeScene's proprietary composite. No verified open-source path to
  that measurement exists - OPEN.
- **Every mechanism in the routing table is a lower bound on badness.** Passing all of them means no
  listed hazard was detected. It does not mean the abstraction is right, the names are honest, the domain
  model is coherent, the error messages are actionable, the tests assert behaviour rather than
  implementation, or the module boundaries fall on real seams of change. Those are contract-only, they are
  the actual determinants of maintainability, and no tool in this pack touches them. Say so in the
  manifest, in those words.

## Sources (accessed 2026-08-08)

- https://pypi.org/pypi/{ruff,pylint,mypy,pyright,coverage,pytest-cov,diff-cover,mutmut,cosmic-ray,import-linter,grimp,tach,pydeps,vulture,complexipy,mypy-baseline,interrogate,radon,xenon,wily}/json - PyPI JSON API: current version, release date and `requires_python` for every tool in the version table; wily's release history confirming 1.25.0 (2023-10-11) stable and 2.0.0a1 (2026-04-26) prerelease.
- https://pypi.org/project/radon/ - radon 6.0.1, released "Mar 26, 2023"; computes "McCabe's complexity", raw metrics, "Halstead metrics (all of them)", "Maintainability Index (the one used in Visual Studio)"; classifiers stop at Python 3.9.
- https://radon.readthedocs.io/en/latest/intro.html - radon's MI formula including the `50 sin(sqrt(2.4 C))` comment term and the "combines both SEI derivative and Visual Studio one" statement; the full Halstead formula set; raw-metric definitions.
- https://radon.readthedocs.io/en/latest/commandline.html - the CC rank table A-F with risk labels; the MI rank table (A 100-20, B 19-10, C 9-0); `cc`/`mi`/`raw`/`hal` subcommands and flags.
- https://raw.githubusercontent.com/rubik/radon/master/radon/visitors.py - radon's exact CC accounting: Try = handlers + orelse; BoolOp = len(values)-1; If/IfExp = 1; Match = cases minus wildcard; For/While/AsyncFor = 1 + orelse; comprehension = ifs + 1; assert = 1 unless no_assert; lambdas excluded (issue #68).
- https://pypi.org/project/xenon/ - xenon 0.9.3 (Oct 21, 2024); `--max-absolute/-b`, `--max-modules/-m`, `--max-average/-a`, `--exclude/-e`, `--ignore/-i`; non-zero exit on threshold breach.
- https://pypi.org/project/wily/ - wily 1.25.0 ("Oct 11, 2023"), Python 3.6-3.12 classifiers, per-commit metric tracking.
- https://docs.astral.sh/ruff/rules/complex-structure/ - C901 `complex-structure`, mccabe origin, "add[ing] one to the number of decision points", `lint.mccabe.max-complexity`.
- https://docs.astral.sh/ruff/rules/ - the full rule table: exact preview/stable status and introducing version for C901, PLR0904/0911/0912/0913/0914/0915/0916/0917, PLR1702, PGH003, PGH004, RUF100, ERA001; confirmation that no cognitive-complexity rule exists.
- https://docs.astral.sh/ruff/settings/ - `lint.mccabe.max-complexity` default "10" and its description.
- https://docs.astral.sh/ruff/rules/too-many-locals/ - PLR0914's preview notice verbatim and the "up to fifteen locals" default.
- https://docs.astral.sh/ruff/rules/too-many-public-methods/ - PLR0904 preview status, default 20.
- https://docs.astral.sh/ruff/rules/blanket-type-ignore/ - PGH003, the `type: ignore[attr-defined]` requirement, and the cross-reference to mypy's `ignore-without-code`.
- https://docs.astral.sh/ruff/rules/blanket-noqa/ - PGH004, that it flags bare `# noqa`, its partial fix, and the "may introduce additional diagnostics" caution.
- https://docs.astral.sh/ruff/rules/unused-noqa/ - RUF100, always-fixable, stable since v0.0.155, the second-`#` guidance for other linters' directives, and the `invalid-rule-code` alternative.
- https://raw.githubusercontent.com/astral-sh/ruff/main/crates/ruff_linter/src/rules/pylint/settings.rs - authoritative ruff pylint defaults: max_args 5, max_positional_args 5, max_returns 6, max_bool_expr 5, max_branches 12, max_statements 50, max_statements_in_try 5, max_public_methods 20, max_locals 15, max_nested_blocks 5.
- https://raw.githubusercontent.com/astral-sh/ruff/main/crates/ruff_workspace/src/options.rs - the option surface including `max_statements_in_try` and the `max_positional_args` fallback to `max_args`.
- https://raw.githubusercontent.com/astral-sh/ruff/main/crates/ruff_linter/src/rules/mccabe/rules/function_is_too_complex.rs - exactly which statements ruff's C901 counts: If (plus clauses), For, While, Match per case, Try per handler, nested FunctionDef; With and ClassDef contribute 0; no BoolOp, comprehension or assert.
- https://raw.githubusercontent.com/astral-sh/ruff/main/crates/ruff/src/args.rs - the `ruff analyze graph` subcommand ("Generate a map of Python file dependencies or dependents"), `--direction dependents`, `--detect-string-imports`, `--min-dots`, `--type-checking-imports`; plus `ruff check --statistics`, `--add-noqa[=reason]`, `--add-ignore[=reason]`.
- https://raw.githubusercontent.com/astral-sh/ruff/main/crates/ruff/src/commands/analyze_graph.rs - the experimental warning emitted when preview is disabled, and JSON output via `serde_json::to_string_pretty`.
- https://raw.githubusercontent.com/astral-sh/ruff/main/docs/linter.md - noqa syntax rules, file-level `# ruff: noqa`, `# flake8: noqa` equivalence, range suppressions not supporting blanket form, `--add-noqa`.
- https://pylint.readthedocs.io/en/latest/user_guide/messages/messages_overview.html - the R09xx/R17xx/R0801 code-to-symbol mapping and the absence of any cyclomatic-complexity message.
- https://raw.githubusercontent.com/pylint-dev/pylint/main/pylint/checkers/design_analysis.py - pylint design-checker defaults (max-args 5, max-positional-arguments 5, max-locals 15, max-returns 6, max-branches 12, max-statements 50, max-parents 7, max-attributes 7, min-public-methods 2, max-public-methods 20, max-bool-expr 5).
- https://raw.githubusercontent.com/pylint-dev/pylint/main/pylint/checkers/symilar.py - `DEFAULT_MIN_SIMILARITY_LINE = 4` and the ignore-comments/docstrings/imports/signatures defaults (all True); the rename from `similar.py`.
- https://www.sonarsource.com/docs/CognitiveComplexity.pdf - Cognitive Complexity white paper, G. Ann Campbell, SonarSource S.A., Version 1.7, 29 August 2023: the CC critique, the three basic rules, the four increment types, the ignore-shorthand / catch / switch / logical-operator / recursion / label rules, the nesting-increment rules, Appendix B specification, and the absence of any recommended threshold.
- https://raw.githubusercontent.com/SonarSource/sonar-python/master/python-checks/src/main/java/org/sonar/python/checks/CognitiveComplexityFunctionCheck.java - `DEFAULT_THRESHOLD = 15`, the `threshold` RuleProperty, `withCost(complexity - threshold)`, and the early return on inner functions and generated files.
- https://raw.githubusercontent.com/SonarSource/sonar-python/master/python-checks/src/main/resources/org/sonar/l10n/py/rules/python/S3776.json - S3776 metadata: CODE_SMELL, Critical, FOCUSED, MAINTAINABILITY HIGH, quickfix infeasible, linear-with-offset remediation of 5 min + 1 min per point, tag brain-overload.
- https://raw.githubusercontent.com/SonarSource/sonar-python/master/python-checks/src/main/resources/org/sonar/l10n/py/rules/python/S3776.html - the rule's Python worked example and the "Method calls are free" / recursion exception.
- Probes of `.../l10n/py/rules/python/{S1541,S1067,S134,S138,S104,S4144}.json` - S1541 and S1067 return HTTP 404 for Python; S134, S138, S104 and S4144 exist with the titles and severities quoted in Fact 27.
- https://raw.githubusercontent.com/SonarSource/sonar-python/master/python-checks/src/main/resources/org/sonar/l10n/py/rules/python/Sonar_way_profile.json - the "Sonar way" profile contains 393 rule keys.
- https://docs.sonarsource.com/sonarqube-server/user-guide/code-metrics/metrics-definition.md - SonarQube definitions and numbers: complexity = 1 + conditional branches; cognitive complexity; duplication thresholds (100 tokens / 10 lines, 20 ABAP, 30 COBOL, 10 statements for Java) with the indentation/string-literal exclusion; the coverage, line_coverage and branch_coverage formulas; sqale_debt_ratio with 30-minutes-per-line development cost; maintainability rating bands A-E.
- https://docs.sonarsource.com/sonarqube-cloud/standards/managing-quality-gates/introduction-to-quality-gates.md - the six "Sonar way" conditions, all scoped to new code, including coverage >= 80.0% and duplication <= 3.0%.
- https://docs.sonarsource.com/sonarqube-server/user-guide/about-new-code.md - the definition of new code, the four new-code definitions, and the Clean as You Code rationale quoted in Fact 56.
- https://docs.sonarsource.com/sitemap.md - used to locate the quality-gate and new-code pages after the `latest/` paths returned 404.
- https://arxiv.org/abs/2007.12520 - Muñoz Barón, Wyrich & Wagner, ESEM 2020: ~24,000 understandability evaluations over 427 snippets; positive correlation of Cognitive Complexity with comprehension time and subjective ratings; mixed results for correctness and physiological measures.
- https://www.cs.du.edu/~snarayan/sada/teaching/COMP3705/lecture/p1/cycl-1.pdf - Shepperd, *A critique of cyclomatic complexity as a software metric*, Software Engineering Journal 3(2):30-36, 1988: full text - the abstract's "no more than a proxy for ... lines of code", the CC-LOC Pearson table (0.84-0.92), "out-performing of v(G) by a straightforward LOC metric in over a third of the studies", the intra- versus inter-modular argument, and the Conclusions section.
- https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication500-235.pdf - NIST SP 500-235, *Structured Testing* (Watson & McCabe, 1996): "The precise number to use as a limit, however, remains somewhat controversial. The original limit of 10 as proposed by McCabe has significant supporting evidence, but limits as high as 15 have been used successfully as well."
- https://www.rascal-mpl.org/blog/2016/01/01/empirical-analysis-of-the-relationship-between-CC-and-SLOC/ - the authors' own summary of Landman/Serebrenik/Vinju: 17.6M Java methods, 6.3M C functions, "linear correlation between SLOC and CC is only moderate as caused by increasingly high variance", and "not strong enough to conclude that CC is redundant with SLOC".
- https://www.scirp.org/journal/paperinformation?paperid=779 - Graylin Jay et al., *Cyclomatic Complexity and Lines of Code: Empirical Evidence of a Stable Linear Relationship*, J. Software Engineering & Applications 2:137-143 (2009): **HTTP 403 this session**; cited FLAGGED-SECONDARY on bibliographic metadata only.
- https://avandeursen.com/2014/08/29/think-twice-before-using-the-maintainability-index/ - van Deursen's MI critique: Oman & Hagemeister ICSM 1992, Coleman et al. 1994, the HP C/Pascal calibration set, "without any recalibration", the power-law averaging objection, and "I have not been able to find a justification for these thresholds".
- https://learn.microsoft.com/en-us/visualstudio/code-quality/code-metrics-maintainability-index-range-and-meaning - the exact Visual Studio MI formula (no comment term) and the 0-9 Red / 10-19 Yellow / 20-100 Green bands.
- https://learn.microsoft.com/en-us/visualstudio/code-quality/code-metrics-values - Visual Studio's metric set: Maintainability Index, Cyclomatic Complexity, Depth of Inheritance, Class Coupling, Lines of Source/Executable code.
- https://raw.githubusercontent.com/seddonym/import-linter/master/docs/contract_types/{index,layers,forbidden,independence,acyclic_siblings,protected}.md - all six contract types with their exact `type` strings and configuration keys, the `depth` default of 10 for `acyclic_siblings`, the documented sharp edge about `depth`/`skip_descendants`, and `as_packages` overlap semantics for `forbidden`.
- https://raw.githubusercontent.com/seddonym/grimp/master/docs/usage.rst - the ImportGraph API: `find_modules_that_directly_import`, `find_modules_directly_imported_by`, `count_imports`, `find_downstream_modules`, `find_upstream_modules`, `find_shortest_chain(s)`, `chain_exists`, `find_illegal_dependencies_for_layers`, `nominate_cycle_breakers`, and `build_graph` options.
- https://raw.githubusercontent.com/gauge-sh/tach/main/README.md - Tach's three enforcements (declared dependencies, public interface, no cycles), `tach init` / `tach check`, the violation message format, `tach.toml` `depends_on` and the `deprecated` marker.
- https://raw.githubusercontent.com/thebjorn/pydeps/master/README.rst - `--show-cycles`, `--max-bacon INT` (default 2, 0 = infinite), `--reverse`, `--externals`, blue-box cycle highlighting, and the Graphviz `dot` requirement.
- https://linux.ime.usp.br/~joaomm/mac499/arquivos/referencias/oodmetrics.pdf - Robert C. Martin, *OO Design Quality Metrics - An Analysis of Dependencies*, October 28 1994: Ca, Ce, `I = Ce/(Ca+Ce)`, A, the Main Sequence, `D = |(A+I-1)/sqrt(2)|`; grep confirms no cycle or acyclic content.
- https://mypy.readthedocs.io/en/stable/command_line.html - `--warn-unused-ignores`, `--disallow-untyped-defs`, `--disallow-incomplete-defs`, `--disallow-any-expr`, `--enable-error-code`, the exact `--strict` flag set, and all report flags (`--any-exprs-report`, `--linecount-report`, `--lineprecision-report`, `--html-report`, `--txt-report`, `--cobertura-xml-report`) with the lxml requirement.
- https://raw.githubusercontent.com/microsoft/pyright/main/docs/command-line.md - `--verifytypes <IMPORT>` "Verify completeness of types in py.typed package", `--ignoreexternal`, `--outputjson`, `--level`, `--stats`, `--threads`.
- https://raw.githubusercontent.com/microsoft/pyright/main/docs/typed-libraries.md - type completeness score = "the percentage of symbols with known types"; the enumeration of what makes a symbol's type unknown; the `--ignoreexternal` behaviour.
- https://raw.githubusercontent.com/orsinium-labs/mypy-baseline/master/README.md - `mypy | mypy-baseline sync` / `filter`, `mypy-baseline.txt`, stdout-only operation, and the merge-conflict-resistant baseline claim.
- https://coverage.readthedocs.io/en/latest/branch.html - branch coverage definition, `--branch`, partial-branch reporting, `# pragma: no branch`, and the documented limits including generator expressions and `while True:` / `if 0:`.
- https://coverage.readthedocs.io/en/latest/config.html - `[run] branch` (default False), `[report] fail_under` "exit with a status code of 2", `precision`, `show_missing`, `skip_covered`, `skip_empty`, `exclude_lines`, `partial_branches`.
- https://raw.githubusercontent.com/nedbat/coveragepy/master/coverage/cmdline.py - the `--format` help string "Output format, either text (default), markdown, or total."; `OK, ERR, FAIL_UNDER = 0, 1, 2`; the precision-aware `should_fail_under` call.
- https://coverage.readthedocs.io/en/latest/commands/index.html - the command list (`run`, `combine`, `erase`, `report`, `html`, `xml`, `json`, `lcov`, `annotate`, `debug`).
- https://raw.githubusercontent.com/Bachmann1234/diff_cover/main/README.rst - the diff-coverage definition ("If you touch a line of code, that line should be covered"), the git requirement, and the supported Cobertura/Clover/JaCoCo/LCov inputs.
- https://www.cs.ubc.ca/~rtholmes/papers/icse_2014_inozemtseva.pdf - Inozemtseva & Holmes, ICSE 2014: 31,000 suites, five Java systems up to 724,000 SLOC, the Kendall's tau tables (0.81-0.95 uncontrolled; 0.50-0.83 normalized with HSQLDB at -0.35, all significant at 99.9%), and the verbatim conclusion that coverage "should not be used as a quality target".
- https://homes.cs.washington.edu/~rjust/publ/mutants_real_faults_fse_2014.pdf - Just et al., FSE 2014: 357 real faults, 5 applications, 321,000 lines; "coupled to mutants for 73% of real faults"; a correlation "stronger than the correlation between statement coverage and real fault detection", independent of code coverage.
- https://coinse.github.io/publications/pdfs/Papadakis2018hi.pdf - Papadakis, Shin, Yoo & Bae, ICSE 2018: "all correlations between mutation scores and real fault detection are weak when controlling for test suite size", the suite-size confound argument against Just et al., and the reconciling finding that top-mutation-score suites detect significantly more faults than equal-size random suites.
- https://raw.githubusercontent.com/boxed/mutmut/main/src/mutmut/__main__.py - the full status vocabulary including `caught by type check` (exit code 37), and `export_cicd_stats` with the verbatim comment "exports CI/CD stats to block pull requests from merging if mutation score is too low", writing `mutants/mutmut-cicd-stats.json`.
- https://raw.githubusercontent.com/boxed/mutmut/main/src/mutmut/configuration.py - `[tool.mutmut]` keys: `paths_to_mutate`, `source_paths`, `tests_dir`, `only_mutate`, `do_not_mutate`, `do_not_mutate_patterns`, `also_copy`, `max_stack_depth` (default -1), `mutate_only_covered_lines`, `debug`.
- https://raw.githubusercontent.com/boxed/mutmut/main/README.rst - `mutmut run` / `browse` / `apply`, incremental restart, and the verbatim `fork`/WSL requirement.
- https://mutmut.readthedocs.io/en/latest/ - the `max_stack_depth=8` performance note ("Incidentally tested functions lead to slow mutation testing").
- https://pypi.org/project/vulture/ - vulture 2.16 (March 25, 2026), Python >=3.9 with a 3.14 classifier, the 60/90/100 confidence tiers, `--min-confidence`, `--make-whitelist`, and the verbatim false-positive/false-negative admission.
- https://raw.githubusercontent.com/rohaquinlop/complexipy/main/README.md - complexipy's cognitive-complexity implementation, `--max-complexity-allowed`, `--output-format json|csv`, `--top`, `--failed --suggest-refactors`, `--plain`, and its explicit non-affiliation with SonarSource.
- https://raw.githubusercontent.com/econchick/interrogate/master/README.rst - `--fail-under` (config default 80), the `ignore-*` option set, `ignore-regex`, `whitelist-regex`, `omit-covered-files`, `--generate-badge`.
- https://docs.pytest.org/en/stable/how-to/usage.html - `--durations=N`, `--durations-min=THRESHOLD`, the documented example, and the "<0.005s hidden unless -vv" default.
- https://testing.googleblog.com/2017/04/where-do-our-flaky-tests-come-from.html - 4.2 million tests analysed; "larger tests are more flaky"; "when a stable test became flaky, and we could track it to a specific code change, the problem was a bug in production code 1/6th of the time".
- https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html - checked for the circulated "1.5% of tests are flaky" figure; the post is qualitative and contains no such statistic (basis for the OPEN tag in Fact 50).
- https://arxiv.org/abs/2203.04374 - Tornhill & Borg, *Code Red: The Business Impact of Code Quality*, TechDebt 2022: 30,737 files across 39 proprietary production codebases; 15x more defects; 124% more development time; 9x longer maximum cycle times; measured with CodeScene (source analysis + version-control mining + Jira).
- https://arxiv.org/abs/2008.09569 - Majumder, Mody & Menzies, *Revisiting Process versus Product Metrics: a Large Scale Analysis*: 722,471 commits from 700 GitHub projects; process versus product recalls 98%/44% and AUCs 95%/54% (medians); the caveat about small-scale metric-importance conclusions.
- https://doi.org/10.1109/ICSE.2013.6606589 - Rahman & Devanbu, "How, and why, process metrics are better", ICSE 2013, pp. 432-441: bibliographic record confirmed; findings not fetched, so cited FLAGGED-SECONDARY and carried by the Majumder replication instead.
- https://dora.dev/guides/dora-metrics-four-keys/ - the current five-metric model with exact names and definitions (change lead time, deployment frequency, failed deployment recovery time, change fail rate, deployment rework rate) and the statement that the metrics shifted "from the original four keys to the current five-metric model".
- https://dora.dev/research/ - checked for performance bands and survey methodology; neither is published on the page (basis for the OPEN tag in Fact 55).
- CodeScene documentation (Temporal Coupling and Hotspots guides, docs.enterprise.codescene.io) - change coupling and temporal coupling definitions, including "Change coupling isn't possible to calculate from code alone", and hotspots as code health combined with temporal and organizational data. FLAGGED-SECONDARY: surfaced via search-result summaries of the versioned docs pages rather than a direct page fetch.
