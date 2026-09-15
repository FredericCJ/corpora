# Python idiom & anti-pattern catalogue (function / module / expression altitude) - fact pack (verified 2026-08-08)

Scope note: this pack covers the **practices rung** - what to write inside a function, a module and an
expression, and the named failure modes - with every item routed to the mechanism that catches it. It
deliberately does not re-derive type-system facts (owned by `python_typing_contract_manifest.md`), the
linter *configuration* story (owned by the planned `python_linting_practices_manifest.md`), the error
contract (owned by `error_tracing_contract_manifest.md`), or version/support schedules (owned by the
planned `python_platform_baseline_manifest.md`).

## Version table

| thing | current version | released (ISO) | source URL | tag |
|---|---|---|---|---|
| CPython (baseline for every version note below) | 3.14.7 | 2026-08-05 | given in brief; hub owns re-verification | VERSION-DEPENDENT (3.14) |
| PEP 8 - Style Guide for Python Code | Status **Active**, Type **Process** | n/a (living) | https://peps.python.org/pep-0008/ | ESTABLISHED |
| PEP 20 - The Zen of Python | Status **Active**, Type **Informational** | n/a | https://peps.python.org/pep-0020/ | ESTABLISHED |
| PEP 257 - Docstring Conventions | Status **Active**, Type **Informational** | n/a | https://peps.python.org/pep-0257/ | ESTABLISHED |
| PEP 3107 - Function Annotations | Status **Final**, Python 3.0 | n/a | https://peps.python.org/pep-3107/ | ESTABLISHED |
| PEP 3102 - Keyword-Only Arguments | Status **Final**, Python 3.0 | n/a | https://peps.python.org/pep-3102/ | ESTABLISHED |
| PEP 570 - Positional-Only Parameters | Status **Final**, Python 3.8 | n/a | https://peps.python.org/pep-0570/ | ESTABLISHED |
| PEP 572 - Assignment Expressions | Status **Final**, Python 3.8 | n/a | https://peps.python.org/pep-0572/ | ESTABLISHED |
| PEP 616 - removeprefix / removesuffix | Status **Final**, Python 3.9 | n/a | https://peps.python.org/pep-0616/ | ESTABLISHED |
| PEP 618 - zip(strict=) | Status **Final**, Python 3.10 | n/a | https://peps.python.org/pep-0618/ | ESTABLISHED |
| PEP 634 - Structural Pattern Matching: Specification | Status **Final**, Python 3.10 | n/a | https://peps.python.org/pep-0634/ | ESTABLISHED |
| PEP 698 - `@override` | Status **Final**, Python 3.12 | n/a | https://peps.python.org/pep-0698/ | ESTABLISHED |
| PEP 727 - Documentation in Annotated Metadata (`typing.Doc`) | Status **WITHDRAWN** | n/a | https://peps.python.org/pep-0727/ | ESTABLISHED |
| Google Python Style Guide | living document, no version stamp | n/a | https://google.github.io/styleguide/pyguide.html | ESTABLISHED (corporate guide, not a PEP) |
| numpydoc style specification | docs "latest" | n/a | https://numpydoc.readthedocs.io/en/latest/format.html | ESTABLISHED |
| ruff | **0.16.2** | 2026-08-07 | https://pypi.org/project/ruff/ | VERSION-DEPENDENT (0.16.2) |
| pylint (docs build read) | **4.0.6** | not shown on page | https://pylint.readthedocs.io/en/stable/user_guide/messages/messages_overview.html | VERSION-DEPENDENT (4.0.6) |
| mypy (docs build read) | **2.3.0** | not shown on page | https://mypy.readthedocs.io/en/stable/command_line.html | VERSION-DEPENDENT (2.3.0) |
| pydoclint | **0.9.1** | 2026-07-03 | https://pypi.org/project/pydoclint/ | VERSION-DEPENDENT (0.9.1) |
| interrogate (docstring coverage) | 1.7.0 released; docs show 1.8.0 unreleased | 2024-04-07 | https://interrogate.readthedocs.io/ | VERSION-DEPENDENT (1.7.0) |
| import-linter (docs build read) | **2.7** | not shown on page | https://import-linter.readthedocs.io/en/v2.7/contract_types.html | VERSION-DEPENDENT (2.7) |
| Refactoring (Fowler) online catalog | supports **2nd edition, 2018** | 2018 | https://refactoring.com/catalog/ | ESTABLISHED |

## Facts

### A. The canonical style baseline - and exactly how binding it is

1. PEP 8 carries Status **Active**, Type **Process**; its vocabulary is "should" / "prefer" /
   "recommended". The word *must* appears only where it restates a rule of the standard library ("All
   identifiers in the Python standard library MUST use ASCII-only identifiers") or of the language
   (future-imports must precede other code). Nothing in PEP 8 is machine-binding by itself -
   ESTABLISHED.
2. PEP 8 ships its own escape hatches in "A Foolish Consistency is the Hobgoblin of Little Minds":
   ignore a guideline when applying it reduces readability, when surrounding code already breaks it,
   when the code predates the guideline, or when older-Python compatibility forbids the newer
   construct - plus the flat instruction "do not break backwards compatibility just to comply with
   this PEP!". It also ranks consistency: with the PEP < within a project < within a module or
   function. A manifest may therefore override PEP 8 locally without being wrong, provided it says so
   once and enforces its own choice mechanically - ESTABLISHED.
3. PEP 8 line limits are **79 characters for code and 72 for docstrings and comments**, with an
   explicitly sanctioned team option to raise *code* to 99 while leaving comments and docstrings at
   72. Stated rationale: 80-column editors and side-by-side review - ESTABLISHED.
4. PEP 8's naming set, complete: modules short all-lowercase (underscores allowed); packages
   all-lowercase (underscores discouraged); C/C++ extension modules a leading underscore; classes
   `CapWords`; exceptions use the class convention plus an `Error` suffix *for actual errors* (a
   non-error exception used for flow control needs no suffix); functions and variables
   `lower_with_under`; constants `UPPER_WITH_UNDER`; type variables `CapWords`, short, with `_co` /
   `_contra` suffixes for covariance / contravariance; `self` and `cls` for the first argument; a
   single trailing underscore to dodge a keyword (`class_`); never `l`, `O` or `I` as a
   single-character name - ESTABLISHED.
5. PEP 8's underscore semantics are the *entirety* of Python's visibility mechanism: `_name` is a weak
   "internal use" marker whose only runtime effect is exclusion from `from M import *`; `name_` avoids
   keyword clashes; `__name` inside a class body triggers name mangling to `_ClassName__name`;
   `__dunder__` names are reserved and "never invent such names". PEP 8 prescribes a *single* leading
   underscore for non-public methods and attributes, reserving the double form for deliberate
   subclass-collision avoidance, and warns that mangling complicates debugging and `__getattr__()` -
   ESTABLISHED.
6. PEP 8's public/internal doctrine is the citable basis for a module API contract: documented
   interfaces are public unless marked provisional or internal; undocumented interfaces are to be
   assumed internal; **a namespace containing internal elements is itself internal**; imported names
   are an implementation detail and callers must not rely on indirect access unless it is documented
   (PEP 8 names `os.path` as the deliberate exception); `__all__` declares the public API and an empty
   `__all__` declares "no public API". Backwards-compatibility guarantees apply only to public
   interfaces - ESTABLISHED.
7. PEP 8 programming recommendations that map onto lint rules: compare to `None` with `is` / `is not`,
   never `==`; beware writing `if x` when you mean `if x is not None`; prefer `is not` over
   `not ... is`; use `isinstance()` rather than comparing types; never write a bare `except:` (it is
   `except BaseException:` and eats `SystemExit` / `KeyboardInterrupt`), with exactly two defensible
   uses named - a handler that prints or logs the traceback, and cleanup followed by a bare `raise`;
   keep the `try` body minimal so it cannot mask bugs; never bind a lambda to a name with `=` (use
   `def`, because the assignment throws away the only advantage of a lambda and loses the name in
   tracebacks) - ESTABLISHED.
8. PEP 8's annotation spacing is normative *style*, not typing content: `x: int` (space after colon,
   none before), spaces around `->`, no spaces around `=` for an unannotated default, spaces around
   `=` when an annotation and a default combine (`def f(x: int = 0)`). PEP 8 also states plainly that
   type checkers are optional separate tools and that interpreters ignore annotations by default -
   ESTABLISHED.
9. PEP 20 is Status **Active**, Type **Informational**, author Tim Peters: 19 aphorisms with no
   binding force. The lines a practices manifest can legitimately lean on: "Explicit is better than
   implicit", "Flat is better than nested", "Readability counts", "Special cases aren't special enough
   to break the rules / Although practicality beats purity", "Errors should never pass silently.
   Unless explicitly silenced.", "There should be one-- and preferably only one --obvious way to do
   it", "If the implementation is hard to explain, it's a bad idea", "Namespaces are one honking great
   idea" - ESTABLISHED.
10. PEP 257 is Status **Active**, Type **Informational**. A docstring is "a string literal that occurs
    as the **first statement** in a module, function, class, or method definition" and becomes that
    object's `__doc__` - ESTABLISHED.
11. PEP 257's one-line rules: triple quotes even for a one-liner (so it can grow); closing quotes on
    the same line; no blank line before or after; ends in a period; **phrased as a command** ("Return
    the ...") not a description ("Returns the ..."); and it must **not restate the signature** - that
    form "is only appropriate for C functions" where introspection is impossible - ESTABLISHED.
12. PEP 257's multi-line function/method docstring MUST document: the behaviour summary, the
    **arguments**, the **return value(s)**, the **side effects**, the **exceptions raised**, and any
    **restriction on when it can be called** - plus which arguments are optional and whether keyword
    arguments are part of the interface. This is the primary-source warrant for the
    docstring-as-contract rule; it is not an invention of this manifest set - ESTABLISHED.
13. PEP 257 at the other altitudes: a class docstring summarises behaviour and lists public methods and
    instance variables, documenting `__init__` separately, and a subclass docstring must state whether
    a method **overrides** (replaces without calling) or **extends** (calls plus adds) the superclass
    method; a module docstring lists the classes, exceptions and functions exported with a one-line
    summary each; a **package** docstring in `__init__.py` lists the modules and subpackages exported;
    a script docstring is its usage message (function, command-line syntax, environment variables,
    files) - ESTABLISHED.
14. PEP 257 deliberately **does not mandate any markup**: it standardises "the high-level structure of
    docstrings ... without touching on any markup syntax within docstrings". Google / NumPy / reST are
    third-party conventions layered on a PEP that is silent about them - ESTABLISHED.
15. PEP 3107 (Final, 3.0) gave the annotation *syntax* and `__annotations__` and nothing more: "By
    itself, Python does not attach any particular meaning or significance to annotations", and it
    "makes no attempt to introduce any kind of standard semantics, even for the built-in types. This
    work will be left to third-party libraries." Every typing convention descends from PEP 484, not
    from 3107 - ESTABLISHED.
16. **PEP 727 is WITHDRAWN.** It proposed `typing.Doc` inside `Annotated` so per-parameter
    documentation would live in the signature; the resolution records that "The reception of this PEP
    was mostly negative, with concerns raised about verbosity and readability." Consequence: there is
    **no standardised machine-readable per-parameter documentation**; a docstring microsyntax is the
    only option, and any manifest suggesting `Annotated[..., Doc(...)]` as the modern way is wrong -
    ESTABLISHED.
17. Google Python Style Guide (accessed 2026-08-08): line length **80** with named exceptions (long
    imports, URLs / paths / flags inside comments, long module-level string constants with no
    whitespace, pylint disable comments); "Do not use a backslash for explicit line continuation"; 4
    spaces, never tabs. It names **pylint** as the linter (and ships a `pylintrc`) and **pytype** as
    the type checker - ESTABLISHED.
18. Google guide docstring rule: "A docstring is mandatory for every function that has one or more of
    the following properties: being part of the public API, nontrivial size, [or] non-obvious logic";
    sections are `Args:` / `Returns:` (or `Yields:`) / `Raises:`; the summary is one physical line
    within 80 chars terminated by `.`, `?` or `!`; and **types need not be repeated in the docstring
    when they are in the signature** - the explicit answer to the annotation-vs-docstring duplication
    question, which numpydoc does not give - ESTABLISHED.
19. Google guide prohibitions worth importing verbatim: mutable objects as default values are forbidden
    ("Default arguments are evaluated once at module load time"); comprehensions with multiple `for`
    clauses or multiple filters are forbidden; lambdas one-line only; conditional expressions only when
    each part fits on one line; properties only for trivial computations and never hiding side effects;
    "power features" (metaclasses, bytecode access, `__del__`, reflection) forbidden; "Avoid mutable
    global state"; `assert` "must not be critical to the application logic" and must not validate
    preconditions (pytest asserts excepted) - ESTABLISHED.
20. Google guide on the two most-misused decorators: "**Never use `staticmethod`** unless forced to in
    order to integrate with an API defined in an existing library. Write a module-level function
    instead." and "Use `classmethod` **only** when writing a named constructor, or a class-specific
    routine that modifies necessary global state such as a process-wide cache." This is the citable
    source for the classmethod/staticmethod anti-pattern - ESTABLISHED.
21. Google guide naming adds what PEP 8 omits: a public/internal column pair for packages, modules,
    classes, exceptions, functions, global and class constants and instance variables (internal =
    single leading underscore, including `_CapWords` for internal classes and `_CAPS_WITH_UNDER` for
    internal constants), plus a **test naming convention**: "New unit test files follow PEP 8 compliant
    lower_with_under method names, for example, `test_<method_under_test>_<state>`" - ESTABLISHED. This
    is the only citable test-naming convention I could confirm from an authoritative guide.
22. numpydoc specifies **15 ordered sections**: Short summary, Deprecation warning, Extended Summary,
    Parameters, Returns, Yields, Receives, Other Parameters, Raises, Warns, Warnings, See Also, Notes,
    References, Examples. Parameters are `name : type` with a space *before* the colon (colon omitted
    when the type is absent), `x : int, optional` for optional, braces for a closed set
    (`order : {'C', 'F', 'A'}`), shared types written `x1, x2 : array_like`, and `*args` / `**kwargs`
    keep their stars and omit the type. `Raises` is optional and "used judiciously, i.e., only for
    errors that are non-obvious or have a large chance of getting raised". Examples are doctest format
    - ESTABLISHED.
23. numpydoc's format page gives **no** rule about omitting types when annotations are present, and
    documents **no** numpydoc-specific validation codes - it mentions only generic checkers (pylint,
    pyflakes, pycodestyle, flake8). A "numpydoc + annotations" duplication policy is therefore a
    project decision, not a spec - OPEN.

### B. Function altitude

24. PEP 3102 (Final, 3.0): keyword-only parameters come after `*args` or after a bare `*`; they may be
    required or defaulted; supplying extra positionals raises `TypeError`. The bare `*` is the cheapest
    mechanical fix for both the boolean trap and the long-argument-list smell - ESTABLISHED.
25. PEP 570 (Final, 3.8): `/` marks positional-only parameters. The PEP's own motivations are the ones
    to cite: freedom to **rename** a parameter later without breaking callers, parity with
    C-implemented signatures (PEP 399), removal of `**kwargs` name collisions, and faster argument
    handling. Legal order is positional-only -> positional-or-keyword -> keyword-only - ESTABLISHED.
26. ruff **PLR0913 too-many-arguments**, default limit **5**, configured by `lint.pylint.max-args`;
    rationale "Functions with many arguments are harder to understand, maintain, and call." The rule
    page does not state whether keyword-only parameters count toward the limit - VERSION-DEPENDENT
    (ruff 0.16.2); the keyword-only question is OPEN.
27. ruff **PLR0917 too-many-positional-arguments** (added in ruff v0.16.0, **not** preview), default
    **5**, configured by `lint.pylint.max-positional-args`. The rule text names its own remedies:
    "Consider refactoring functions with many arguments into smaller functions with fewer arguments,
    using objects to group related arguments, or migrating to keyword-only arguments." A linter that
    names the refactoring is the strongest available routing for this practice - VERSION-DEPENDENT
    (ruff 0.16.2).
28. The boolean trap is lint-catchable in three places, all flake8-boolean-trap, none with a fix:
    **FBT001** boolean-type-hint-positional-argument (fires on `bool` and on unions containing bool,
    e.g. `bool | int`, `Optional[bool]`, in positional position), **FBT002**
    boolean-default-value-positional-argument, **FBT003** boolean-positional-value-in-call (the call
    site; a default allowlist exists, extended via
    `lint.flake8-boolean-trap.extend-allowed-calls`). FBT001's page cites Adam Johnson, "How to Avoid
    'The Boolean Trap'" - VERSION-DEPENDENT (ruff 0.16.2).
29. Fowler names the smell **Flag Argument** (bliki, 23 June 2011): "A flag argument is a kind of
    function argument that tells the function to carry out a different operation depending on its
    value" and "My general reaction to flag arguments is to avoid them." Remedy: separate explicit
    functions; the catalog refactoring is **Remove Flag Argument**. His nuances stop the rule becoming
    dogma: keep the flag-taking function *private* when the implementation genuinely interleaves the
    two behaviours; derive the flag internally from caller data; and a flag argument has "some
    justification" when the value comes straight from a UI checkbox or a data source - ESTABLISHED.
30. The Fowler online catalog (2nd ed., 2018) contains, verbatim, the refactorings that are the named
    remedies for nearly everything in this pack: Extract Function, Inline Function, Introduce Parameter
    Object, Preserve Whole Object, Replace Primitive with Object, **Replace Nested Conditional with
    Guard Clauses**, Decompose Conditional, Replace Conditional with Polymorphism, Combine Functions
    into Class, Combine Functions into Transform, Split Phase, Encapsulate Variable, Encapsulate
    Collection, Replace Temp with Query, Remove Flag Argument, Parameterize Function, Separate Query
    from Modifier, Replace Function with Command, Replace Type Code with Subclasses, Replace Subclass
    with Delegate, Replace Superclass with Delegate (listed with the alias "Replace Inheritance with
    Delegation"), Extract Class, Move Function, Hide Delegate, Remove Middle Man, Split Variable.
    Fowler's own 2nd-edition page states "all but 10 are still present, and I've added 17 new ones" and
    that the examples moved to JavaScript - ESTABLISHED.
31. **Replace Nested Conditional with Guard Clauses** is the citable name for early-return discipline;
    the catalog page shows nested `if/else` collapsing into sequential early returns, motivated by
    making the flow linear. Cite this rather than "guard clause" as folklore - ESTABLISHED.
32. Return-shape mechanisms: ruff **RET503 implicit-return** (missing explicit `return` at the end of a
    function that can return non-`None`; fix always available), **RET504 unnecessary-assign** (fix
    available), **RET505 superfluous-else-return** (fix sometimes available); pylint **R1710
    inconsistent-return-statements** is the direct "some paths return a value, some do not" check -
    VERSION-DEPENDENT (ruff 0.16.2 / pylint 4.0.6).
33. Size and complexity gates, with the defaults a project silently inherits: ruff **C901
    complex-structure** (mccabe; "one plus the number of decision points in the function"),
    `lint.mccabe.max-complexity` default **10**; `lint.pylint.max-statements` default **50**;
    `lint.pylint.max-branches` default **12**; `lint.pylint.max-returns` default **6**;
    `lint.pylint.max-public-methods` default **20**. pylint's equivalents: R0915 too-many-statements,
    R0912 too-many-branches, R0911 too-many-return-statements, R0904 too-many-public-methods, R1702
    too-many-nested-blocks, R0902 too-many-instance-attributes, R0901 too-many-ancestors, R0903
    too-few-public-methods, R0801 duplicate-code - VERSION-DEPENDENT (ruff 0.16.2 defaults; pylint
    4.0.6 codes).
34. ruff **PLR0904 too-many-public-methods** exists but is **preview** (requires `--preview`), default
    20 via `lint.pylint.max-public-methods` - VERSION-DEPENDENT (ruff 0.16.2).
35. **Composed Method** (Kent Beck, *Smalltalk Best Practice Patterns*, 1996) is the named pattern
    behind "divide the program into methods that each perform one identifiable task, keeping all
    operations in a method at the same level of abstraction, which naturally yields many small
    methods" - FLAGGED-SECONDARY: I could not load an authoritative primary page for the pattern text
    this session (only vendor listings and a draft mirror), so cite the attribution, not a quotation.
36. Purity is not expressible: there is no `pure` / `const` qualifier in Python's type system, so a
    purity claim is either runtime-checked by a DbC library (`deal.pure`) or convention-only. The
    typing manifest already establishes this; the practices rung must not imply a checker enforces it
    - ESTABLISHED (contract-only).

### C. Module altitude

37. PEP 257 is the only PEP statement I could confirm about `__init__.py` *content*: the package
    docstring there "should list the modules and subpackages exported by the package". There is no PEP
    that says what code may live in `__init__.py` - that is convention - ESTABLISHED / OPEN.
38. mypy **`--no-implicit-reexport`** (included in `--strict`): by default "imported values to a module
    are treated as exported and mypy allows other modules to import them"; the flag "changes the
    behavior to not re-export unless the item is imported using from-as or is included in `__all__`".
    So the *explicit re-export* practice is genuinely type-catchable, in two accepted spellings:
    `from foo import bar as bar`, or listing `bar` in `__all__` - VERSION-DEPENDENT (mypy 2.3.0).
39. The full `--strict` set on the same page: `--disallow-any-generics`, `--disallow-subclassing-any`,
    `--disallow-untyped-calls`, `--disallow-untyped-defs`, `--disallow-incomplete-defs`,
    `--check-untyped-defs`, `--disallow-untyped-decorators`, `--warn-redundant-casts`,
    `--warn-unused-ignores`, `--warn-return-any`, `--no-implicit-reexport`, `--strict-equality`,
    `--extra-checks` - VERSION-DEPENDENT (mypy 2.3.0).
40. ruff **F401 unused-import** is `__init__.py`-aware: in `__init__.py` it "will suggest a safe fix to
    export first-party imports with either a redundant alias or, if already present in the file, an
    `__all__` entry", and it documents the redundant-alias convention explicitly - "Consider using a
    'redundant' import alias, which instructs Ruff (and other tools) to respect the re-export".
    Fixes that *remove* unused imports are safe **except** in `__init__.py`, where the fix is in
    preview and unsafe for third-party and stdlib imports "because the module's interface changes".
    Settings: `lint.ignore-init-module-imports`, `lint.pyflakes.allowed-unused-imports` -
    VERSION-DEPENDENT (ruff 0.16.2).
41. `__all__` hygiene has real rules: ruff **RUF022 unsorted-dunder-all** (isort-style ordering; fix
    sometimes available, and **unsafe** when whole-line comments sit inside the `__all__` literal or
    when several items share a line with a trailing comment). ruff's Pylint family additionally carries
    `invalid-all-format` and `invalid-all-object` and pyflakes carries the undefined-name-in-`__all__`
    check; I confirmed those exist on the rules index but did **not** verify each code-to-name pairing
    on its own page - FLAGGED-SECONDARY for the exact codes, VERSION-DEPENDENT otherwise.
42. `__all__` affects only `from M import *` and the re-export contract. It makes nothing private at
    runtime. Python's *only* visibility mechanisms are the underscore convention (fact 5) and
    class-body name mangling. Any manifest sentence implying enforced privacy is false - ESTABLISHED.
43. Import-time work has exactly one first-party instrument: **`python -X importtime`** (added 3.7)
    prints per-module cumulative and self time; **`-X importtime=2`** (added **3.14**) additionally
    traces already-loaded modules, printing `cached` in both time columns; the environment variable is
    `PYTHONPROFILEIMPORTTIME` (`1` / `2`). There is no linter that detects "expensive work at import
    time" - VERSION-DEPENDENT (3.14).
44. ruff **PLC0415 import-outside-top-level** flags deferred imports *and* names the legitimate reasons
    in its own text: "An import statement would typically be placed within a function only to avoid a
    circular dependency, to defer a costly module load, or to avoid loading a dependency altogether in
    a certain runtime environment." This rule and the "do no work at import time" practice are in
    direct tension; a project must choose and record which wins - VERSION-DEPENDENT (ruff 0.16.2).
45. **import-linter 2.7** contract types, exact `type` strings: `forbidden` (one set of modules must not
    import another), `layers` (higher layers may import lower, never the reverse, including
    indirectly; supports `exhaustive`), `independence` (a set of modules must not import each other in
    any direction), `protected` (direct imports of a module restricted to an allow-list),
    `acyclic_siblings` (no dependency cycles between sibling modules). Configuration:
    `[importlinter]` + `root_package` / `root_packages` + `[importlinter:contract:<name>]` in INI, or
    `[[tool.importlinter.contracts]]` in TOML. This is a real CI fitness function for module-shape
    practices that no per-file linter can express - VERSION-DEPENDENT (import-linter 2.7).
46. `Final`, `@final` and `ClassVar` are checker-only (the typing manifest already records "There is no
    runtime checking of these properties"). The adjacent mechanical rule is ruff **RUF012
    mutable-class-default**: "Mutable default values share state across all instances of the class,
    while not being obvious", with `typing.ClassVar` named as one remedy - VERSION-DEPENDENT.
47. `-O` / `-OO` / `PYTHONOPTIMIZE`: `-O` removes `assert` statements and any code conditional on
    `__debug__`; `-OO` additionally **discards docstrings**. Consequences for this rung: a
    docstring-as-contract is absent under `-OO`, doctests cannot run there, and any `assert`-expressed
    invariant vanishes under `-O` - ESTABLISHED.

### D. Expression altitude

48. Comprehension complexity: the Google guide forbids "multiple `for` clauses or filter expressions".
    I could find **no** linter that limits comprehension nesting: C901 counts decision points across
    the whole function, and `lint.pylint.max-nested-blocks` is **absent** from ruff's settings page
    (pylint has R1702 too-many-nested-blocks for statement blocks, not comprehensions). Comprehension
    complexity is therefore **contract-only** at expression altitude - OPEN.
49. `zip()` truncates silently to the shortest iterable. PEP 618 (Final, 3.10) added `strict=True`,
    which raises `ValueError` when the arguments are exhausted at differing lengths; strict is not the
    default because truncation is legitimately useful ("extremely useful, for example, when dealing
    with infinite iterators"). ruff **B905 zip-without-explicit-strict** has an *always available* fix
    that is marked **UNSAFE**, with the reason stated on the page: "While adding `strict=False`
    preserves the runtime behavior, it can obscure situations where the iterables are of unequal
    length." The autofix therefore *satisfies the linter while preserving the bug* - ESTABLISHED +
    VERSION-DEPENDENT (ruff 0.16.2).
50. `itertools` version and hazard facts: `pairwise` 3.10; `batched` 3.12 with a `strict` parameter
    added in **3.13** (raises `ValueError` if the final batch is short); `accumulate`'s `initial`
    3.8. Documented hazards to route: `tee` "may require significant auxiliary storage" and tee
    iterators "are not threadsafe. A RuntimeError may be raised when simultaneously using iterators
    returned by the same tee() call"; `product` "completely consumes the input iterables, keeping pools
    of values in memory"; `cycle` may require significant auxiliary storage; and `groupby` requires
    input already sorted on the same key function ("Generally, the iterable needs to already be sorted
    on the same key function") - VERSION-DEPENDENT (3.13).
51. `contextlib` version facts: `suppress` 3.4 (3.12: can strip suppressed exceptions out of a
    `BaseExceptionGroup`), `ExitStack` 3.3, `nullcontext` 3.7 (async 3.10), `aclosing` 3.10, `chdir`
    3.11, `AbstractContextManager` 3.6, `ContextDecorator` 3.2, `asynccontextmanager` 3.7 (usable as a
    decorator 3.10). Two documented traps: a `@contextmanager` generator is **single-use** - "These
    single use context managers must be created afresh each time they're used - attempting to use them
    a second time will trigger an exception" (`RuntimeError: generator didn't yield`); and an exception
    from the `with` body "is reraised inside the generator at the point where the yield occurred", so
    a generator that traps an exception merely to log it "must reraise that exception" or the `with`
    statement treats the exception as handled and execution silently continues -
    ESTABLISHED / VERSION-DEPENDENT (3.12).
52. `contextlib` reentrancy is documented and is not thread-safety: `suppress`, `redirect_stdout`,
    `redirect_stderr`, `chdir` are reentrant, and the docs note `redirect_stdout` is reentrant but
    **not** thread-safe - ESTABLISHED.
53. `functools.lru_cache` (3.2; `typed` 3.3; `cache_parameters()` 3.9) - the leak caveat in the docs'
    own words: "The cache keeps references to the arguments and return values until they age out of the
    cache or until the cache is cleared" and "If a method is cached, the `self` instance argument is
    included in the cache." The docs also state it "doesn't make sense to cache functions with
    side-effects, functions that need to create distinct mutable objects on each call (such as
    generators and async functions), or impure functions such as time() or random()", and that all
    arguments must be hashable. `functools.cache` (3.9) is `lru_cache(maxsize=None)` - unbounded, never
    evicting. `typed=False` (the default) treats `1` and `1.0` as the same key, and typing applies only
    to the immediate arguments, not their contents - ESTABLISHED.
54. The leak is lint-catchable: ruff **B019 cached-instance-method** - "Using the `functools.lru_cache`
    and `functools.cache` decorators on methods can lead to memory leaks, as the global cache will
    retain a reference to the instance, preventing it from being garbage collected." No autofix; the
    remedy is structural (extract a module-level function, or depend only on arguments) -
    VERSION-DEPENDENT (ruff 0.16.2).
55. `functools.cached_property` (3.8) caveats, all documented: it requires a mutable `__dict__`, so it
    fails on metaclasses and on classes with `__slots__` that do not include `__dict__`; it "interferes
    with the operation of PEP 412 key-sharing dictionaries", so instance dicts get larger; the
    undocumented per-property lock was **removed in 3.12**, and the docs now state "The getter function
    could run more than once on the same instance, with the latest run setting the cached value";
    invalidation is `del instance.attr`; and unlike `@property` it permits writes -
    VERSION-DEPENDENT (3.12).
56. `functools.partial` gained `Placeholder` in **3.14** (and `Placeholder` "cannot be passed to
    `partial()` as a keyword argument"). `@wraps` / `update_wrapper` copy `__module__`, `__name__`,
    `__qualname__`, `__annotations__`, `__type_params__` (3.12) and `__doc__`, and set `__wrapped__` -
    which is also how you reach the uncached function under `@lru_cache` - VERSION-DEPENDENT (3.14).
57. `str.removeprefix` / `removesuffix` (PEP 616, Final, 3.9) exist on `str`, `bytes`, `bytearray` and
    `collections.UserString`, and return the original unchanged when the affix is absent. The stated
    motivation is a documented, repeated user error: `lstrip` / `rstrip` take a **character set**, not
    a substring - "There have been repeated issues on Python-Ideas, Python-Dev, the Bug Tracker, and
    StackOverflow related to user confusion about the existing str.lstrip and str.rstrip methods." The
    lint route for the misuse is pylint **E1310 bad-str-strip-call** (ruff carries the same check under
    its Pylint family) - ESTABLISHED.
58. PEP 572 walrus (Final, 3.8) is prohibited: unparenthesised at statement level, as the right side of
    an assignment statement, as a keyword-argument value, as a function default, in an annotation, in
    an unparenthesised lambda body, in an f-string format-spec position, and in a comprehension's
    *iterable* expression. Inside a comprehension the target binds in the **containing** scope
    (honouring `nonlocal` / `global`), and it may not collide with a `for` target of that
    comprehension. `:=` binds more tightly than a comma and less tightly than every other operator.
    The PEP's own style advice: prefer a statement when both forms work, and restructure if the
    assignment expression makes evaluation order ambiguous - ESTABLISHED.
59. `match` (PEP 634, Final, 3.10) semantics that actually bite:
    (a) a bare name is a **capture pattern** that "always succeeds" and binds - it is *never* a value
    comparison; (b) a value comparison requires a **dotted** name (`Color.RED`), resolved by normal
    name resolution and compared with `==`; (c) `_` is the wildcard, always succeeds, "binds no name";
    (d) "In a given pattern, a given name may be bound only once"; (e) "Although `str`, `bytes`, and
    `bytearray` are usually considered sequences, they are not included in the above list and do not
    match sequence patterns"; (f) a mapping pattern succeeds if every key **in the pattern** is present
    in the subject - extra subject keys are fine (capture them with `**name`); (g) class patterns
    convert positional sub-patterns via `__match_args__` (auto-generated for namedtuples and
    dataclasses; for builtins a single positional pattern matches the whole subject); (h) guards run
    *after* the pattern succeeds and may have side effects; (i) there is **no fallthrough**; (j) "If no
    case blocks qualify the match statement is complete" - **no error is raised** - ESTABLISHED.
60. Because of 59(j), match exhaustiveness is not a language guarantee; the mechanical remedy is a
    `case _:` arm that calls `typing.assert_never(value)`, which makes the checker error when a new
    variant appears. `assert_never` entered `typing` in 3.11 (recorded in the typing manifest). I could
    not quote the exact docs sentence this session - the `typing` docs page truncated on fetch - so the
    technique is ESTABLISHED and the docs wording is OPEN.
61. **`pathlib` is not a drop-in replacement for `os.path`** - the docs say exactly that, and name the
    differences: `os` / `os.path` are C and faster; `os.path.abspath()` eliminates `".."` segments
    while `Path.absolute()` preserves them "for greater safety"; `Path("my_folder/")` normalises away
    the trailing slash, "which may change behavior with OS APIs"; and `Path("./my_program")` normalises
    to `Path("my_program")`, which changes PATH lookup. The docs carry a "Corresponding tools" mapping
    table (`os.path.dirname` -> `PurePath.parent`, `os.path.join` -> `PurePath.joinpath`,
    `os.walk` -> `Path.walk`, etc.) - ESTABLISHED.
62. `pathlib` version notes for a minimum-target decision: `read_text` / `write_text` / `read_bytes` /
    `write_bytes` 3.5 (`write_text(newline=)` 3.10, `read_text(newline=)` 3.13); `mkdir(exist_ok=)`
    3.5; `resolve(strict=)` 3.6; `unlink(missing_ok=)` 3.8; `is_relative_to` and `with_stem` 3.9;
    `hardlink_to` 3.10; `Path.walk`, `glob(case_sensitive=)` and `relative_to(walk_up=)` 3.12;
    `glob(recurse_symlinks=)` 3.13 - VERSION-DEPENDENT (3.13).
63. ruff **PTH** is flake8-use-pathlib; **PTH118 os-path-join** verified. **PTH123 builtin-open** flags
    *every* `open()` call in favour of `Path.open()`, and its own page concedes the cost: pathlib "can
    be less performant than working directly with strings, especially on older versions of Python", and
    the fix is unsafe when it would drop comments. Treat PTH123 as a taste rule, not a defect rule -
    VERSION-DEPENDENT (ruff 0.16.2).
64. Idiom rules with real codes: pylint **C0200 consider-using-enumerate**, **C0209
    consider-using-f-string**, **R1721 unnecessary-comprehension**, **R0205
    useless-object-inheritance**; ruff **SIM110 reimplemented-builtin**, **C416
    unnecessary-comprehension**, **C400 unnecessary-generator-list**, **C404
    unnecessary-list-comprehension-dict**, **C417 unnecessary-map** - the pylint codes verified on the
    pylint messages overview, the ruff C4xx code-to-name pairings taken from the rules index rather
    than individual pages - VERSION-DEPENDENT (pylint 4.0.6 / ruff 0.16.2), FLAGGED-SECONDARY on the
    C4xx pairings.
65. ruff **PLR2004 magic-value-comparison**: "The use of 'magic' values can make code harder to read
    and maintain, as readers will have to infer the meaning of the value from the context"; configured
    by `lint.pylint.allow-magic-value-types`; no autofix, because naming a constant is a human
    decision - VERSION-DEPENDENT (ruff 0.16.2).

### E. Data-shape decisions

66. `dataclasses` parameter set and defaults: `init=True, repr=True, eq=True, order=False,
    unsafe_hash=False, frozen=False, match_args=True, kw_only=False, slots=False, weakref_slot=False`.
    `match_args` / `kw_only` / `slots` added **3.10**, `weakref_slot` **3.11**, `field(..., doc=)`
    **3.14** - VERSION-DEPENDENT (3.14).
67. `slots=True` has a documented sharp edge: "`__slots__` attribute will be generated and **new class
    will be returned instead of the original one**". Anything holding a reference to the pre-decoration
    class (a decorator, a registry, a closure) then points at a different object; and "Passing
    parameters to a base class `__init_subclass__()` when using `slots=True` will result in a
    `TypeError`". Since 3.11 a field name already in a base class's `__slots__` is omitted from the
    generated `__slots__` - ESTABLISHED / VERSION-DEPENDENT (3.11).
68. Since **3.11** a dataclass mutable default is rejected by **hashability**, not by type: "Instead of
    looking for and disallowing objects of type list, dict, or set, unhashable objects are now not
    allowed as default values. Unhashability is used to approximate mutability", raising `ValueError`.
    So a custom mutable-but-hashable default still slips through - VERSION-DEPENDENT (3.11).
69. `dataclasses.KW_ONLY` (3.10) is a sentinel *type annotation*: every field after a pseudo-field
    annotated `KW_ONLY` becomes keyword-only, the pseudo-field is otherwise ignored (including its
    name), only one is permitted per class, and "By convention, a name of `_` is used". This is the
    dataclass-level answer to the long-argument-list smell - VERSION-DEPENDENT (3.10).
70. `asdict()` / `astuple()` recurse into dataclasses, dicts, lists and tuples and **`copy.deepcopy()`
    everything else** - a silent deep copy that is a real performance and identity hazard in a hot
    path. `fields()` omits `ClassVar` and `InitVar` pseudo-fields - ESTABLISHED.
71. `enum` version map: `Enum` / `IntEnum` 3.4; `Flag` / `IntFlag` / `auto` 3.6; `StrEnum`, `ReprEnum`,
    `EnumCheck` + `@verify`, `@member` / `@nonmember`, `@global_enum` all **3.11** - VERSION-DEPENDENT
    (3.11).
72. `StrEnum` (3.11) members **are** strings; `str()` and `__format__()` return the **value**, not the
    name; `auto()` produces the lower-cased member name; and any string operation on a member returns a
    plain `str`, leaving the enumeration. Documented interop caveat: some stdlib code tests
    `type(x) == str` rather than `isinstance`, so an explicit `str(MyStrEnum.MEMBER)` is sometimes
    required - ESTABLISHED.
73. `IntEnum` members are ints, `Number.THREE == 3` is `True`, and any integer operation returns a
    plain `int`. In **3.11** `IntEnum.__str__` became `int.__str__` "to better support the replacement
    of existing constants use-case", and `IntFlag` inversion became a positive union rather than a
    negative value. The docs position `IntEnum` / `StrEnum` / `IntFlag` as "drop-in replacements for
    existing integer- and string-based values" - i.e. *interoperability* tools; plain `Enum` is the
    default choice and the docs do not otherwise prescribe when to use which - ESTABLISHED / OPEN (the
    "when" is a project decision).
74. `@unique` raises `ValueError` if aliases exist; `@verify(UNIQUE)` is the same check; `@verify
    (CONTINUOUS)` rejects gaps between the lowest and highest member; `@verify(NAMED_FLAGS)` rejects
    flag aliases that include unnamed values. These are the only *runtime* enum invariants the stdlib
    offers - VERSION-DEPENDENT (3.11).
75. `NewType` is the typed-wrapper answer to primitive obsession and costs almost nothing: "these
    checks are enforced only by the static type checker. At runtime, the statement
    `Derived = NewType('Derived', Base)` will make `Derived` a callable that immediately returns
    whatever parameter you pass it." It became a class in 3.10 (extra call cost) and the 3.9-level
    performance was restored in 3.11. It adds **no validation** - ESTABLISHED / VERSION-DEPENDENT
    (3.11).
76. Fowler's name for the data-shape failure is **Primitive Obsession**; the catalog remedies are
    **Replace Primitive with Object**, **Introduce Parameter Object**, **Preserve Whole Object** and
    **Replace Type Code with Subclasses**. The adjacent smells are **Data Clumps** (arguments that
    always travel together) and **Data Class** (all data, no behaviour) - ESTABLISHED for the
    refactoring names from the catalog page; the full 24-smell enumeration is FLAGGED-SECONDARY
    (Fowler's own 2nd-edition page does not enumerate the smells).

### F. Docstrings as contracts, and executable documentation

77. `doctest` invocation surface: `python -m doctest file [-v] [-o OPTION] [-f]` (runs `testmod()` for
    `.py`, `testfile()` otherwise), `doctest.testmod()` (returns `(failure_count, test_count)`),
    `doctest.testfile()`, and unittest integration via `DocTestSuite` / `DocFileSuite` - ESTABLISHED.
78. `doctest`'s brittleness is documented, not folklore: "doctest is serious about requiring exact
    matches in expected output. If even a single character doesn't match, the test fails." Expected
    output cannot contain an all-whitespace line - use `<BLANKLINE>`; hard tabs expand to 8-column
    stops; set and dict ordering is not guaranteed (sort before printing); floating-point output varies
    because "Python defers to the platform C library for some floating-point calculations"; default
    `repr()` embeds an address, needing `+ELLIPSIS`. Flags: `ELLIPSIS`, `NORMALIZE_WHITESPACE`, `SKIP`,
    `IGNORE_EXCEPTION_DETAIL`, `FAIL_FAST`, `REPORT_NDIFF`, `REPORT_ONLY_FIRST_FAILURE`; directive
    syntax `# doctest: +FLAG, +FLAG2` - ESTABLISHED.
79. `doctest` exception matching: the traceback *stack* is optional and ignored, so `...` in place of
    the frames is the idiom; `IGNORE_EXCEPTION_DETAIL` matches only the exception **type** and ignores
    both the message and module qualification - which means a doctest can keep passing while the error
    message it documents rots - ESTABLISHED.
80. The doctest docs state their own limit: examples should be pedagogically valuable first and tests
    second - "Filling your docstrings with obscure test cases makes for bad documentation" - and
    "Regression testing is best confined to dedicated objects or files". doctest is therefore
    *executable documentation*, not a substitute for the test suite - ESTABLISHED.
81. Docstring **presence** is lint-catchable: ruff's **D** family is pydocstyle; **D103
    undocumented-public-function** verified, with `lint.pydocstyle.ignore-decorators` to exempt
    decorated functions. `lint.pydocstyle.convention` accepts `"google"`, `"numpy"`, `"pep257"`,
    default `null`, and selecting a convention **disables the rules incompatible with it** - so
    choosing the convention is the single most consequential docstring setting - VERSION-DEPENDENT
    (ruff 0.16.2).
82. Docstring **coverage** is gate-able: `interrogate` 1.7.0 (docs show an unreleased 1.8.0) with
    `--fail-under` (default **80.0**), `--ignore-init-method`, `--ignore-nested-functions`,
    `--ignore-private`, `--omit-covered-files`, and a pre-commit hook. It checks **presence only** and
    never content - VERSION-DEPENDENT (interrogate 1.7.0).
83. Docstring **agreement with the signature** is checkable, in preview: `pydoclint` 0.9.1 (2026-07-03)
    checks that the arguments / returns / yields / raises sections match the signature and body, over
    NumPy, Google and Sphinx styles, emitting `DOC` codes. Ruff has folded it in as the **DOC** family,
    all preview: **DOC102 docstring-extraneous-parameter** (preview since ruff 0.14.1) - "Checks for
    function docstrings that include parameters which are not in the function signature"; **DOC201
    docstring-missing-returns** (preview since 0.5.6) - "Checks for functions with `return` statements
    that do not have 'Returns' sections in their docstrings"; **DOC501 docstring-missing-exception**
    (preview since 0.5.5) - "Checks for function docstrings that do not document all explicitly raised
    exceptions" - VERSION-DEPENDENT (ruff 0.16.2 / pydoclint 0.9.1).
84. What nothing checks: whether the docstring's **prose** is true. DOC201 / DOC501 verify that a
    section exists corresponding to a fact in the code (a return exists, an exception is raised);
    doctest verifies the examples; nothing verifies the preconditions paragraph, the side-effect
    sentence, or the "restriction on when it can be called" that PEP 257 demands. Those become runtime
    contracts (icontract / `deal` / explicit raises, per the typing manifest) or they are unverified -
    ESTABLISHED by construction.

### G. Named anti-patterns and their citable sources

85. "Code smell" itself: Fowler's bliki (9 February 2006) - "A code smell is a surface indication that
    usually corresponds to a deeper problem in the system" - and he credits **Kent Beck** with coining
    the term - ESTABLISHED.
86. **God object / The Blob**: named as "The Blob" in *AntiPatterns: Refactoring Software,
    Architectures, and Projects in Crisis* (Brown, Malveau, McCormick, Mowbray; Wiley, 1998); the
    earlier "god class / god object" usage is attributed to Riel, *Object-Oriented Design Heuristics*
    (1996). I confirmed the bibliographic record (including the ACM Digital Library catalogue entry)
    but did not read either book - FLAGGED-SECONDARY.
87. Fowler 2nd-edition smells relevant to this rung: Mysterious Name, Duplicated Code, Long Function,
    Long Parameter List, Global Data, Mutable Data, Divergent Change, **Shotgun Surgery**, **Feature
    Envy**, Data Clumps, **Primitive Obsession**, Repeated Switches, Loops, Lazy Element, Speculative
    Generality, Temporary Field, Message Chains, Middle Man, Insider Trading, Large Class, Alternative
    Classes with Different Interfaces, Data Class, Refused Bequest, Comments - FLAGGED-SECONDARY on the
    enumeration (assembled from secondary summaries; Fowler's own pages give the refactoring names, not
    the smell list).
88. **Stringly typed**: FOLDOC defines it as a play on "strongly typed" for an implementation that uses
    strings where a more appropriate type exists, defeating compile-time checking, and credits **Mark
    Simpson**; the term was popularised through The Daily WTF - FLAGGED-SECONDARY (a dictionary entry
    is the best naming source I found; no standards or book source names it).
89. **Catch-log-rethrow**: no primary or standards source names it. The practitioner literature is
    unanimous - logging and re-raising the same exception duplicates the record at every layer and
    scatters the decision about who owns the failure. The only mechanical fragment is ruff **TRY400
    error-instead-of-exception** ("`logging.exception` logs the exception and the traceback, while
    `logging.error` only logs the exception"; fix safe for `logging.error`, unsafe for `logger.error`
    style calls). The rest is contract-only, and the *policy* belongs to
    `error_tracing_contract_manifest.md` - FLAGGED-SECONDARY.
90. **The "utils" module**: no citable authority exists. The argument (a name with no cohesion criterion
    -> unrelated code accumulates -> unbounded growth -> everything depends on everything through the
    utils bottleneck -> a breeding ground for circular imports -> eventual name collisions between
    multiple `utils` modules) appears only in practitioner essays. The mechanical route is an
    import-linter `independence` or `layers` contract plus a review ban, not a linter -
    FLAGGED-SECONDARY / OPEN.
91. **Exception as control flow** has real codes: ruff **TRY300 try-consider-else** ("The `try`-`except`
    statement has an `else` clause for code that should run only if no exceptions were raised"),
    **TRY301 raise-within-try**, **BLE001 blind-except**, **S101 assert**; pylint **W0718
    broad-exception-caught**, **W0719 broad-exception-raised** - VERSION-DEPENDENT (ruff 0.16.2 /
    pylint 4.0.6).
92. **Mutable global and shared state** has the densest mechanical coverage of any anti-pattern here:
    ruff **PLW0603 global-statement** ("global mutable state is a common source of bugs and confusing
    behavior"), **PLW0602 global-variable-not-assigned**, **RUF012 mutable-class-default**, **B006
    mutable-argument-default** ("Function defaults are evaluated once, when the function is defined.
    The same mutable object is then shared across all calls"), **B008
    function-call-in-default-argument** ("Any function call that's used in a default argument will only
    be performed once, at definition time"), both B006/B008 tunable via
    `lint.flake8-bugbear.extend-immutable-calls`; pylint **W0102 dangerous-default-value**, **W0603
    global-statement**, **W0602 global-variable-not-assigned**. Fowler's names are **Global Data** and
    **Mutable Data** - VERSION-DEPENDENT.
93. B006's fix is **UNSAFE** and the page says why: "This fix is marked as unsafe because it replaces
    the mutable default with `None` and initializes it in the function body, which may not be what the
    user intended". An agent running `--unsafe-fixes` on a codebase can silently change a signature's
    public type from `list[int]` to `list[int] | None` - VERSION-DEPENDENT (ruff 0.16.2).
94. **Deep or misapplied inheritance**: pylint **R0901 too-many-ancestors**, **R0903
    too-few-public-methods**, **R0205 useless-object-inheritance**. PEP 698's `@override` (3.12) makes
    the two refactor failure modes checkable - a renamed or deleted base method whose override is now
    orphaned, and a subclass method that silently *becomes* an override when a base class grows a
    method; the PEP notes "several production outages in multiple typed codebases caused by such
    incorrect refactors". Fowler's smell is **Refused Bequest**; the catalog remedy is **Replace
    Superclass with Delegate** (alias "Replace Inheritance with Delegation") - ESTABLISHED /
    VERSION-DEPENDENT (3.12).
95. `@override` enforcement is static. PEP 698 additionally states the decorator sets
    `__override__ = True` on a best-effort basis ("adding `__override__` may fail at runtime, in which
    case we will simply return the argument as-is"), while the typing specification's class-compat
    chapter describes only the static rule and mentions no runtime attribute. Do not build anything on
    the runtime attribute - VERSION-DEPENDENT (3.12) / OPEN on the runtime guarantee.
96. **A method that is not a method**: ruff **PLR6301 no-self-use** ("Unused `self` parameters are
    usually a sign of a method that could be replaced by a function, class method, or static method"),
    which is **preview** and exempts `@staticmethod`, `@classmethod` and `@typing.override` - the last
    exemption specifically to avoid pushing a Liskov violation. pylint's `no-self-use` is reported as
    **R6301** on the messages overview, but whether it now lives only in an optional extension
    (`pylint.extensions.no_self_use`) was not resolvable from that page - VERSION-DEPENDENT / OPEN.

### H. Enforcement machinery this rung depends on

97. ruff **0.16.2** (2026-08-07). Fix safety, verbatim: safe fixes mean "The meaning and intent of your
    code will be retained when applying safe fixes" and they "will only remove comments when deleting
    entire statements or expressions"; an unsafe fix "could lead to a change in runtime behavior, the
    removal of comments, or both". `--fix` applies safe fixes only; `--unsafe-fixes` opts in;
    `lint.extend-safe-fixes` / `lint.extend-unsafe-fixes` re-grade rules or whole prefixes. The
    documented example is **RUF015**, where rewriting `list(...)[0]` to `next(iter(...))` changes the
    empty-input exception from `IndexError` to `StopIteration` - VERSION-DEPENDENT (ruff 0.16.2).
98. ruff selection: `lint.select` / `lint.extend-select` / `lint.ignore`; a code is a one-to-three
    letter prefix plus three digits and **any prefix is a valid selector**; `ALL` selects everything
    and ruff then auto-disables mutually exclusive rules (the docs name the D203/D211 pair);
    **RUF100** flags `# noqa` directives that suppress nothing. In preview mode selectors also accept
    human-readable rule names - VERSION-DEPENDENT (ruff 0.16.2).
99. Formatter/linter conflicts, from ruff's formatter page - disable **W191, E111, E114, E117, D206,
    D300, D203, Q000, Q001, Q002, Q003, Q004, COM812, COM819**, and **ISC002** in the stated
    configuration; `E501` may stay, but "the formatter only makes a best-effort attempt to wrap lines
    at the configured line-length"; and the isort settings `force-single-line`, `force-wrap-aliases`,
    `lines-after-imports`, `lines-between-types`, `split-on-trailing-comma` conflict when set to
    non-default values. `format.docstring-code-format` defaults to **false**. Ruff targets >99.9% Black
    compatibility with deliberate deviations - VERSION-DEPENDENT (ruff 0.16.2).
100. **D203 incorrect-blank-line-before-class** is disabled by default under all three conventions
     (`google`, `numpy`, `pep257`), is mutually exclusive with **D211**, and ruff's own page recommends
     against it alongside the formatter: "The formatter removes blank lines before class docstrings,
     which conflicts with this rule's requirement to include them" - VERSION-DEPENDENT (ruff 0.16.2).
101. Three "authorities" give three different line lengths: PEP 8 says **79** (72 for comments and
     docstrings, 99 permitted for code by team decision), the Google guide says **80**, ruff's default
     `line-length` is **88**. Only the tool can enforce, so the tool's number is the real one; the
     project must pick once and state it - ESTABLISHED (the conflict) / VERSION-DEPENDENT (the 88).

## The routing table

Legend for the route column: **type** = a checker rejects it; **lint** = a rule code rejects it;
**feature** = a newer language construct eliminates the hazard class; **test** = a test kind catches
it; **fitness** = an architectural check in CI; **contract-only** = nothing mechanical catches it.

| hazard / practice | why it bites | enforcement route | exact mechanism (rule code / flag / checker / test kind) | residual risk |
|---|---|---|---|---|
| Function does more than one thing (Composed Method violation) | every caller pays for the parts it does not want; untestable without doubles | lint (proxy) + contract-only | ruff `C901` complex-structure (`lint.mccabe.max-complexity`, default 10); `lint.pylint.max-statements` 50; pylint `R0915`, `R0912` | metrics proxy size, not cohesion: a 6-line function can still do two things |
| Too many parameters | callers memorise positions; the signature hides a missing object | lint | ruff `PLR0913` (`lint.pylint.max-args`, default 5) | a parameter object that is itself a bag of 12 fields passes the rule |
| Too many *positional* parameters | positional calls are misread and mis-ordered silently | lint | ruff `PLR0917` (`lint.pylint.max-positional-args`, default 5) | says nothing about argument *order* or naming |
| Boolean trap in a signature | `f(x, True)` is unreadable and unextensible | lint + feature | ruff `FBT001`, `FBT002`; feature: PEP 3102 bare `*` makes it keyword-only; Enum replaces the two-valued domain | no autofix; `FBT001` cannot tell a genuinely two-valued domain from a hidden mode switch |
| Boolean literal at the call site | intent invisible at the point it matters | lint | ruff `FBT003` (+ `lint.flake8-boolean-trap.extend-allowed-calls`) | stdlib and third-party callees you cannot change generate noise |
| Flag argument (Fowler) as a mode switch | one function with two behaviours; conditionals metastasise | contract-only | review against Fowler's "Remove Flag Argument"; `FBT00x` catches only the boolean-typed subset | a `str`/Enum-typed mode parameter is invisible to every linter |
| Nested conditionals instead of guard clauses | reader must hold N conditions to understand the last line | lint (partial) | ruff `RET505` superfluous-else-return; `SIM103` needless-bool; pylint `R1702` too-many-nested-blocks | flattening `if/else` is not the same as extracting the guard; `RET505` fix is cosmetic |
| Inconsistent return type across paths | callers branch on `None` they were never told about | type + lint | mypy `--disallow-untyped-defs` + declared return type (via `--strict`); ruff `RET503` implicit-return; pylint `R1710` inconsistent-return-statements | a declared `X | None` return silences everything while keeping the design flaw |
| Implicit `return None` fall-through | the absent value is undeclared and untraceable | lint | ruff `RET503` (fix always available) | autofix writes `return None`, which may be the wrong contract |
| Mutable default argument | one shared object across all calls, forever | lint | ruff `B006` mutable-argument-default; pylint `W0102` dangerous-default-value | **fix is UNSAFE**: it rewrites the default to `None` and changes the public type |
| Function call in a default argument | evaluated once at definition time (a frozen clock, a shared connection) | lint | ruff `B008` (+ `lint.flake8-bugbear.extend-immutable-calls`) | a call that is genuinely constant must be allowlisted by hand |
| Impure function claimed pure | reuse and test assumptions silently false | contract-only | nothing: no `pure` qualifier exists; `deal.pure` is runtime-only | a docstring purity claim is unverified forever (typing manifest §6) |
| Magic value in a comparison | reader infers meaning; the same literal drifts apart in two places | lint | ruff `PLR2004` (`lint.pylint.allow-magic-value-types`) | no autofix; naming the constant is the human's job |
| Docstring absent on a public function | no contract to check the implementation against | lint | ruff `D103` (pydocstyle family; `lint.pydocstyle.ignore-decorators`) | presence, not content: `"""Do the thing."""` passes |
| Docstring omits the raised exceptions | callers cannot write handlers; PEP 257 requires it | lint (preview) | ruff `DOC501` docstring-missing-exception (preview since 0.5.6/0.5.5 family; `--preview` required) | only *explicitly raised* exceptions; anything a callee raises stays undocumented |
| Docstring omits the return value | contract incomplete per PEP 257 §multi-line | lint (preview) | ruff `DOC201` docstring-missing-returns (preview) | presence of a `Returns:` section, not truth of its text |
| Docstring documents a parameter that no longer exists | drift after a refactor; actively misleading | lint (preview) | ruff `DOC102` docstring-extraneous-parameter (preview since 0.14.1); standalone `pydoclint` 0.9.1 | preview status means the code may move or change |
| Docstring prose is simply wrong | the contract lies and everything downstream trusts it | test (partial) + contract-only | doctest for the examples; icontract / `deal` for the invariants (typing manifest §5) | prose preconditions and side-effect claims: unverifiable, permanently |
| Docstring coverage regresses over time | the standard decays silently | fitness | `interrogate --fail-under=<N>` (default 80.0) in CI, pre-commit hook available | coverage is presence-only; 100% coverage of empty docstrings is achievable |
| Mixed docstring styles in one codebase | tooling cannot parse; readers context-switch | lint | `lint.pydocstyle.convention = "google" \| "numpy" \| "pep257"` (default `null`) | choosing a convention silently *disables* the D-rules incompatible with it |
| Doctest as the test suite | brittle on ordering, floats and reprs; bad documentation | contract-only + test-design | doctest docs' own position ("Regression testing is best confined to dedicated objects or files"); pytest owns real tests | a passing doctest with `IGNORE_EXCEPTION_DETAIL` can hide a changed error message |
| Docstring relied on at runtime | `-OO` discards docstrings | contract-only | run the CI suite once under `-OO` if any code reads `__doc__` | no linter models `-OO`; an `argparse` help text built from `__doc__` vanishes |
| `assert` used as validation | `-O` strips it; the check silently disappears in production | lint | ruff `S101` assert (bandit family); Google guide forbids it for preconditions | `S101` must be exempted in tests, which is where asserts belong |
| Implicit re-export from `__init__.py` | callers depend on an accident; you cannot refactor imports | type | mypy `--no-implicit-reexport` (in `--strict`); satisfied by `from x import y as y` or `__all__` | pyright's equivalent behaviour differs; both must be pinned (typing manifest §8) |
| Unused import in `__init__.py` deleted by an autofix | the package's public interface silently narrows | lint (with care) | ruff `F401`: fixes are safe *except* in `__init__.py`, where they are preview and unsafe "because the module's interface changes"; `lint.ignore-init-module-imports` | an agent running `--fix` broadly can still amputate a re-export surface |
| `__all__` drifts from reality | `import *` and re-export contract silently wrong | lint | ruff `RUF022` unsorted-dunder-all; ruff's PL family carries invalid-`__all__`-object / -format; pyflakes flags undefined names in `__all__` | `RUF022`'s fix is unsafe when comments live inside the literal; ordering is not correctness |
| Private helper treated as public by a caller | the underscore is a convention with no teeth | contract-only + fitness | PEP 8 underscore convention; import-linter `forbidden` / `protected` contract to ban cross-package imports of internals; pylint `W0212` protected-access at the *use* site | nothing at runtime prevents `from pkg._impl import thing` |
| Module-level constant reassigned | a "constant" that is not | type | `typing.Final` (checker-only; typing manifest §6) | zero runtime enforcement; `Final` prevents rebinding, never mutation |
| Mutable class attribute as a default | state shared across all instances, invisibly | lint | ruff `RUF012` mutable-class-default (remedy: `typing.ClassVar` or a factory) | `ClassVar` annotation silences the rule while keeping the shared mutable |
| `global` mutation | untestable, order-dependent, unreasonable | lint | ruff `PLW0603` global-statement; `PLW0602` global-variable-not-assigned; pylint `W0603` / `W0602` | a module-level mutable object mutated *without* `global` (e.g. `CACHE[k] = v`) is not flagged |
| Work at import time (I/O, network, config read) | import order becomes semantics; tests get slow and coupled | contract-only + test | `python -X importtime` (3.7) / `-X importtime=2` (3.14) / `PYTHONPROFILEIMPORTTIME`; assert an import-time budget in a test | no linter detects it; the budget test is bespoke |
| Deferred (in-function) import used as a habit | dependencies invisible; failures surface late | lint (with judgement) | ruff `PLC0415` import-outside-top-level - whose own text legitimises three exceptions | directly contradicts the import-time-work practice above; the project must choose |
| Dependency direction violated (layering) | the module cannot be lifted into another project | fitness | import-linter 2.7 `layers` (with `exhaustive`), `forbidden`, `independence`, `protected`, `acyclic_siblings` contracts in CI | needs a hand-authored contract file; nothing infers the intended layering |
| "utils" grab-bag module | no cohesion criterion; becomes a dependency bottleneck | contract-only + fitness | naming ban in review; import-linter `independence` to stop everything importing it | no citable authority and no rule code; pure convention |
| God object / Blob | one class centralises behaviour, others become data holders | lint (proxy) | ruff `PLR0904` too-many-public-methods (**preview**, default 20); pylint `R0904`, `R0902` too-many-instance-attributes | a 19-method god object passes; "centralises behaviour" is not measurable by count |
| Primitive obsession | `str` for an id, `int` for money; nothing catches a swap | type | `NewType` per domain concept (checker-only, no runtime cost); `Enum` for closed domains; `Literal` for small closed sets | `NewType` adds no validation; arithmetic between two `NewType`s of `int` is unchecked (typing manifest §4) |
| Stringly-typed interface | invalid values representable; refactors invisible | type | `Enum` / `StrEnum` / `Literal` at the boundary; `LiteralString` (3.11) where injection is the risk | `StrEnum` members compare equal to plain strings, so the old stringly call sites keep working |
| Non-exhaustive `match` | a new variant silently falls through with no error (PEP 634) | type | `case _:` arm calling `typing.assert_never(x)` (3.11) so the checker errors on a new variant | without the `assert_never` arm there is no diagnostic at all, at any level |
| Bare name in a `match` case meant as a constant | it is a capture pattern; it always matches and silently binds | type (partial) + contract-only | use a dotted value pattern (`Color.RED`); a checker may report an unreachable following case, and ruff/pylint flag some unused bindings | the code runs and silently takes the first branch; PEP 634 makes this legal |
| `str` matched with a sequence pattern | `str`/`bytes`/`bytearray` are excluded by spec, so the case never fires | contract-only | read PEP 634 §sequence patterns; test the branch | no linter warns; the branch is simply dead |
| `zip()` length mismatch | silent data loss (the PEP cites a real stdlib bug) | feature + lint | `zip(..., strict=True)` (PEP 618, 3.10) raising `ValueError`; ruff `B905` zip-without-explicit-strict | **the B905 autofix inserts `strict=False`**, satisfying the linter and preserving the bug |
| Comprehension too complex | unreadable, undebuggable, no place to put a breakpoint | contract-only | Google guide's ban on multiple `for` clauses or filters, enforced by review | no rule counts comprehension nesting; `C901` counts the enclosing function |
| List built where a generator was meant | needless materialisation | lint | ruff C4xx family (`C400` unnecessary-generator-list, `C416`, `C417`); pylint `R1721` | rewriting to a generator changes re-iterability and exception timing |
| `os.path` string plumbing | separator and normalisation bugs; untyped path strings | lint | ruff `PTH` (flake8-use-pathlib): `PTH118` os-path-join, `PTH123` builtin-open, etc. | pathlib is **not** a drop-in replacement (`abspath` vs `absolute`, trailing-slash and `./` normalisation); `PTH123` is taste, and the docs concede a performance cost |
| `lstrip("prefix")` used to strip a prefix | it takes a character *set*; silently over-strips | feature + lint | `str.removeprefix` / `removesuffix` (PEP 616, 3.9); pylint `E1310` bad-str-strip-call | only flags provably wrong calls; `removeprefix` needs a 3.9+ floor |
| `lru_cache` / `cache` on a method | the cache holds `self` forever - a real leak | lint | ruff `B019` cached-instance-method | no autofix; the remedy is structural, and `B019` says nothing about caching *unhashable-adjacent* or impure functions |
| `lru_cache` on an impure or effectful function | wrong answers, cached | contract-only | the functools docs say it plainly; nothing checks it | a cached `now()`-dependent function is a correctness bug no tool sees |
| `cached_property` on a `__slots__` class | fails at runtime: no mutable `__dict__` | test | any test that touches the property; the docs state the requirement | no linter models it |
| `cached_property` under threads (3.12+) | the lock was removed in 3.12; the getter can run twice | contract-only | documented behaviour change; concurrency belongs to the planned concurrency manifest | code written against 3.11 semantics silently becomes racy on upgrade |
| Walrus used to compress a statement | evaluation order becomes non-obvious; comprehension targets leak to the enclosing scope | contract-only | PEP 572's own advice: prefer a statement when both work | no rule; the comprehension-scope leak is *specified* behaviour, not a bug |
| Exception used as control flow | flow invisible; costs and handlers both wrong | lint | ruff `TRY300` try-consider-else, `TRY301` raise-within-try; pylint `W0719` broad-exception-raised | `TRY300` is a shape rule, not a semantics rule |
| Blind `except Exception` | swallows the bug you needed to see | lint | ruff `BLE001` blind-except; pylint `W0718`; PEP 8's bare-except prohibition | the two defensible uses PEP 8 names (log-and-reraise, cleanup-then-`raise`) must be exempted by hand |
| Catch, log, re-raise at every layer | one failure, N log records, no owner | contract-only (+1 lint fragment) | ruff `TRY400` error-instead-of-exception (use `logging.exception`); policy lives in `error_tracing_contract_manifest.md` | nothing detects the duplication itself; `TRY400`'s fix is unsafe for `logger.error` calls |
| f-string inside a logging call | argument evaluated regardless of level | lint | already owned by `logging_observability_manifest.md` §12 (and it warns the autofix pushes the *wrong* way) | linters may "fix" lazy `%` args *into* f-strings - see traps |
| Inheritance where composition was meant | subclass bound to a parent it does not want | contract-only | Fowler "Refused Bequest" -> "Replace Superclass with Delegate"; pylint `R0901` too-many-ancestors as a weak proxy | depth is not the defect; the unwanted-bequest relation is invisible to tools |
| Override silently orphaned or accidentally created | renamed base method leaves a dead override; new base method captures a subclass method | type | `typing.override` (PEP 698, 3.12); checkers error when the decorated method overrides nothing | opt-in per method unless the checker is configured to require it; the `__override__` runtime attribute is best-effort only |
| `staticmethod` used as a namespace | a module-level function pretending to be a method | lint (preview) + contract-only | ruff `PLR6301` no-self-use (preview; exempts `@staticmethod`/`@classmethod`/`@override`); Google guide: "Never use `staticmethod` unless forced to" | preview status; and the rule cannot see intent behind an existing `@staticmethod` |
| `classmethod` used as a second constructor grab-bag | class becomes a factory zoo | contract-only | Google guide: `classmethod` only for a named constructor or a class-specific routine touching process-wide state | no rule code exists |
| Shotgun surgery / divergent change | one behaviour change touches N files | fitness (proxy) | import-linter contracts to keep the change surface inside a boundary; pylint `R0801` duplicate-code as a weak proxy | genuinely a design property; no tool measures "one change, N files" directly |
| Feature envy | a function reaches into another object's data | contract-only | review against Fowler's "Move Function"; pylint `W0212` protected-access catches only underscore access | dataclass field access is public and invisible to linters |
| Comment that has drifted from the code | actively misleading; worse than no comment | contract-only (+2 fragments) | doctest for examples; ruff `ERA001` commented-out-code for the dead-code subset | prose comments cannot be checked, ever; this is the honest floor of this rung |
| Line length / formatting bikeshedding | review noise displaces review substance | lint + formatter | one `line-length` (ruff default 88 vs PEP 8's 79 vs Google's 80) + `ruff format`; disable the conflicting rules in fact 99 | pick once, or the formatter and the linter fight every commit |

## What the existing manifests already cover

- `python_typing_contract_manifest.md` §2 "The typing vocabulary for contracts" - already owns the
  facts for `Protocol` vs `abc.ABC`, `@dataclass`, `TypedDict` (incl. `Required`/`NotRequired`/
  `ReadOnly` and the removed keyword-arg form), `NamedTuple`, `Enum` + `Literal`, `NewType`, generics,
  `Self`, `Final`/`@final`, `Annotated`, `Never`/`NoReturn`. **Do not restate these.** The delta this
  pack adds is the *decision rule* between the data shapes, plus the `StrEnum`/`IntEnum` interop
  semantics and the enum `@verify` checks, which §2 does not carry.
- `python_typing_contract_manifest.md` §4 "What the type system CANNOT express" - value ranges,
  cross-field invariants, ordering/temporal constraints, units, typestate; and the explicit finding
  that `Annotated` metadata is ignored by checkers. This is the ceiling for every "type-catchable"
  claim in the routing table.
- `python_typing_contract_manifest.md` §5 - pydantic/`__post_init__`/icontract/`deal`/`assert` and the
  `-O` strips-asserts caveat, plus the "parse, don't validate" boundary rule.
- `python_typing_contract_manifest.md` §6 - `frozen=True` shallowness, `Final` being checker-only,
  `Mapping` vs `MutableMapping` as a static promise, `@property` without a setter, and the flat
  statement that purity is not checker-enforceable.
- `python_typing_contract_manifest.md` §7 "Contract documentation conventions" - the
  signature-vs-docstring split rule, the three docstring styles with Napoleon, "pick ONE style per
  project", and doctest/icontract/`deal` as machine-checkable forms. **This is the nearest existing
  content to this pack's section F**; the delta is PEP 257's *normative list* of what a docstring must
  carry, the DOC/pydoclint rule codes, `interrogate`, the doctest failure modes, and PEP 727's
  withdrawal.
- `python_typing_contract_manifest.md` §8 + Recommendations - mypy `--strict` flag set, pyright mode
  divergence, and the "pin the literal flag list, never write 'use strict mode'" instruction.
- `error_tracing_contract_manifest.md` §2 - PEP 20 quoted as the error stance ("Errors should never
  pass silently. Unless explicitly silenced."), §10/§19 on never catch-and-ignore, `contextlib.suppress`
  as the only sanctioned silencing, and the anti-pattern list including swallow-and-continue. Exception
  *policy* stays there; this pack only routes the lint codes.
- `logging_observability_manifest.md` §12 and its checklist - lazy `%`-style logging args,
  `isEnabledFor`, f-strings discouraged in logging calls, and the standing warning that
  mypy/pyright/ruff may try to rewrite `%` args into f-strings. The f-string idiom row in the routing
  table defers to this file.
- `python_testing_tooling_manifest.md` §3/§5/§7 - double taxonomy, "specify obligations not test code",
  and the testability design facts; `tmp_path` fixtures. Test *naming* is not covered anywhere.
- `software_spec_discipline_manifest.md` A1/A2 (contract not computation; type-level scaffolding
  allowed, bodies not), C2/C3 (reusability earned by boundaries; the dependency surface is the reuse
  tax), F1 (pure core / imperative shell), F2 (dependency inversion at every side-effect boundary),
  G2 (contracts are signature-level and complete). This pack's function- and module-altitude practices
  are the *implementation* of those rules; cite them, do not re-argue them.
- `architecture_manifest_default.md` §3.1 coupling/cohesion, §3.2 state and ownership, §3.5 interfaces
  and contracts (including the line that a docstring invariant beats an unstated one), §6 refactoring
  patterns. Fowler's smell/refactoring vocabulary belongs adjacent to §6.
- Not covered anywhere in the set today (confirmed by grep across all nine files): PEP 8 itself, PEP
  257's content, comprehensions, walrus, `match`, `pathlib`, `functools` caching, `__all__`,
  keyword-only / positional-only parameters, `StrEnum`, guard clauses, single responsibility at
  function altitude, itertools, and every named anti-pattern (god object, primitive obsession, shotgun
  surgery, feature envy, flag argument, boolean trap, "utils"). This pack is nearly all delta.

## New content the manifest set should carry

**1. "The practices ladder: advice, rule, feature, gate"** - destination: **NEW:
`python_idioms_practices_manifest.md`** (opening section).
State the governing thesis in mechanism terms and fix the vocabulary used by every later row:
type-catchable / lint-catchable / feature-eliminated / test-catchable / fitness-function /
contract-only. Establish up front that PEP 8 (Process, advisory) and PEP 20 (Informational) carry no
mechanical force, that PEP 257 *does* enumerate what a docstring must contain, and that the project's
real style authority is whatever `ruff` is configured to reject. Name the three conflicting line
lengths (79/80/88) as the worked example of "advice that isn't enforced decays to zero". Defer all
rule-selection and CI-wiring detail to `python_linting_practices_manifest.md` and
`python_quality_gates_manifest.md`.

**2. "Function altitude: size, parameters, returns"** - destination: **NEW:
`python_idioms_practices_manifest.md`**.
Composed Method (Beck 1996) as the sizing rule, with the honest note that C901/max-statements are
proxies for cohesion, not measures of it. Parameter discipline: `PLR0913` (5) and `PLR0917` (5) with
the bare `*` of PEP 3102 as the mechanical remedy and `/` of PEP 570 as the API-evolution tool (rename
freedom, `**kwargs` collision, C parity). The boolean trap in all three positions (FBT001/002/003)
plus Fowler's Flag Argument and its three sanctioned exceptions. Return discipline: RET503/RET504/
RET505 and pylint R1710, and the warning that declaring `X | None` silences the linter without fixing
the design. Guard clauses cited as "Replace Nested Conditional with Guard Clauses", not folklore.

**3. "Module altitude: the liftable unit"** - destination: **NEW:
`python_module_boundaries_manifest.md`** (per PLAN, that file owns the import system and public-API
contract) with a one-paragraph pointer from the practices file.
PEP 8's public/internal doctrine as the *citable* API rule, including "a namespace containing internal
elements is itself internal" and "imported names are an implementation detail". `__all__` as the
re-export declaration plus mypy `--no-implicit-reexport` and the two accepted spellings. The
`F401`-in-`__init__.py` asymmetry (safe elsewhere, preview-and-unsafe there) as an agent hazard.
PEP 257's package-docstring rule as the only PEP statement about `__init__.py`. Import-time work with
`-X importtime` / `-X importtime=2` as the only instrument, and the PLC0415 tension stated openly.
Close with the import-linter contract vocabulary (`layers`, `forbidden`, `independence`, `protected`,
`acyclic_siblings`) as the fitness function that makes "liftable" testable.

**4. "Expression altitude: the idioms that are actually load-bearing"** - destination: **NEW:
`python_idioms_practices_manifest.md`**.
Only idioms with a defect (not a taste) behind them: `zip(strict=True)` with the PEP 618 data-loss
motivation and the B905-inserts-`strict=False` trap; `removeprefix`/`removesuffix` with the
documented `lstrip` character-set confusion; `pathlib` with the docs' own "not a drop-in replacement"
list; `enumerate`/`zip` over index arithmetic (pylint C0200); comprehension limits as contract-only
because no rule counts them; generator vs list with the C4xx codes; `contextlib` single-use and
must-reraise caveats; `itertools` hazards (`tee` storage and thread-unsafety, `groupby` sortedness,
`product` full consumption); walrus with PEP 572's own restraint advice.

**5. "match: the five ways it silently does nothing"** - destination: **NEW:
`python_idioms_practices_manifest.md`**.
Capture-vs-value patterns (bare name always binds; use a dotted name); `_` binds nothing; a name may
bind once per pattern; `str`/`bytes`/`bytearray` are excluded from sequence patterns; mapping patterns
are partial on the subject; `__match_args__` requirement for positional class patterns; no
fallthrough; and the specified no-match-no-error behaviour that makes `case _: assert_never(x)` the
only exhaustiveness mechanism. Every claim is PEP 634 text, so this section is unusually safe to state
flatly.

**6. "Caching: `lru_cache`, `cache`, `cached_property` and what they retain"** - destination: **NEW:
`python_idioms_practices_manifest.md`**.
The functools docs' own retention sentence, the `self`-in-the-key sentence, B019 as the enforcement,
the "never cache impure / effectful / distinct-mutable-returning functions" list, `cache` being
unbounded, `typed=False` conflating `1` and `1.0`, `cached_property`'s `__dict__` requirement and
PEP 412 cost, the 3.12 lock removal, and `del obj.attr` as the only invalidation. Cross-reference the
concurrency manifest for the race and the diagnostics manifest for measuring the retention.

**7. "Data shape: choosing between dataclass, NamedTuple, TypedDict, dict, Enum, StrEnum, NewType"** -
destination: **NEW: `python_idioms_practices_manifest.md`**, with every *runtime-enforcement* fact
cited to `python_typing_contract_manifest.md` §2 rather than repeated.
A single decision table plus the sharp edges this pack verified: `slots=True` returns a **new class**;
mutable defaults rejected by hashability since 3.11; `KW_ONLY`; `asdict()` deep-copying non-container
values; `StrEnum`/`IntEnum` as interop tools whose members compare equal to plain values (so they do
not force call-site migration); `@unique` / `@verify(UNIQUE|CONTINUOUS|NAMED_FLAGS)` as the only
runtime enum invariants; `NewType` as the primitive-obsession remedy with zero validation.

**8. "Naming: what PEP 8 fixes and what the project must pin"** - destination: **NEW:
`python_idioms_practices_manifest.md`**.
Reproduce PEP 8's fixed set (modules, packages, classes, exceptions + `Error` suffix, functions,
constants, TypeVars with `_co`/`_contra`, `self`/`cls`, trailing underscore, the `l`/`O`/`I` ban) and
the underscore semantics as the whole of Python's visibility story. Then state plainly what PEP 8
leaves open and must be pinned as project convention, tagged OPEN: boolean names, predicate names,
factory-function names, private-helper naming beyond the underscore, and test names - for which the
only citable convention found is the Google guide's `test_<method_under_test>_<state>`. Enforcement:
ruff's `N` (pep8-naming) family for the mechanical part, contract-only for the rest.

**9. "Docstrings as contracts, and what actually checks them"** - destination: extend
`python_typing_contract_manifest.md` §7 (it already owns the split rule and style menu) rather than
opening a rival section.
Add: PEP 257's normative content list (arguments, returns, side effects, exceptions, calling
restrictions) as the warrant for the contract docstring; the imperative-mood and no-signature-restatement
rules; the Google guide's explicit permission to omit types already in the signature versus numpydoc's
silence; **PEP 727 withdrawn**, so no `Annotated`-based per-parameter docs; the enforcement ladder
presence (`D103`) -> coverage (`interrogate --fail-under`) -> agreement (`DOC102`/`DOC201`/`DOC501`,
preview) -> truth (nothing); and doctest's documented brittleness plus the `-OO` docstring-stripping
consequence.

**10. "The anti-pattern rejection list, with sources and routes"** - destination: **NEW:
`python_idioms_practices_manifest.md`** (final section, in the house one-line-each rejection format).
Each entry: name, the work that named it, the route. God object / The Blob (AntiPatterns 1998, Riel
1996 - FLAGGED-SECONDARY; route: PLR0904 preview / R0904 / R0902); Primitive Obsession, Shotgun
Surgery, Feature Envy, Data Clumps, Global Data, Mutable Data, Refused Bequest, Long Function, Long
Parameter List (Fowler, catalog + 2nd ed.); Flag Argument (Fowler 2011); boolean trap (FBT rules,
citing Adam Johnson); stringly typed (FOLDOC, crediting Mark Simpson - FLAGGED-SECONDARY); exception
as control flow (TRY300/TRY301/BLE001); mutable global state (PLW0603/B006/B008/RUF012);
`staticmethod`/`classmethod` misuse (Google guide's "never"/"only"); inheritance where composition was
meant (Refused Bequest -> Replace Superclass with Delegate; `@override`); "utils" module
(FLAGGED-SECONDARY, no authority - route: import-linter + review); catch-log-rethrow
(FLAGGED-SECONDARY - route: TRY400 + `error_tracing_contract_manifest.md`).

**11. "Agent-specific hazards of autofix"** - destination: **NEW:
`python_linting_practices_manifest.md`** (that file owns fix policy), sourced from the traps section
below.
The five that matter: `--unsafe-fixes` is a semantic-change switch, not a convenience flag; `B905`
inserts `strict=False`; `B006` rewrites the public type; `RUF015` changes the exception type;
formatter-versus-lint rule conflicts (fact 99) turn CI into a loop. State the house rule: an agent may
apply safe fixes, must never pass `--unsafe-fixes` unattended, and must re-run the type checker after
any autofix pass.

## Traps for coding agents

1. **The `B905` autofix preserves the bug.** `zip-without-explicit-strict` has an always-available fix
   that inserts `strict=False`. The rule exists because silent truncation loses data; the fix silences
   the rule and keeps the truncation. Ruff's own page admits it "can obscure situations where the
   iterables are of unequal length". An agent clearing lint findings will convert a real defect into a
   documented one. Insert `strict=True` by hand unless truncation is intended and commented.
2. **The `B006` autofix changes the public signature.** It rewrites `def f(x: list[int] = [])` to a
   `None` default plus in-body initialisation - which changes the annotation the caller sees and the
   checker enforces. Ruff marks it unsafe for exactly this reason. Under `--unsafe-fixes` an agent can
   silently widen a dozen APIs to `| None`.
3. **`RUF015`'s fix changes the exception type.** `list(...)[0]` raises `IndexError` on empty input;
   `next(iter(...))` raises `StopIteration`. Ruff uses this as its canonical example of an unsafe fix.
   Any `except IndexError:` upstream stops working.
4. **`--fix` and `--unsafe-fixes` are different tools.** `--fix` applies safe fixes only; safe fixes
   still delete comments when they delete a whole statement. `lint.extend-safe-fixes` /
   `lint.extend-unsafe-fixes` let a repo re-grade rules, so "safe" is a per-project claim, not a
   universal one. Never assume the grading from memory - read the repo config.
5. **Lint rules that fight the formatter.** W191, E111, E114, E117, D206, D300, D203, Q000-Q004,
   COM812, COM819 and (conditionally) ISC002 must be disabled when `ruff format` runs; five isort
   settings conflict at non-default values. An agent that "fixes" D203 will watch the formatter undo it
   next commit, forever. `E501` may stay, but the formatter only makes a *best-effort* attempt to
   respect `line-length`, so E501 findings can survive a clean format.
6. **D203 and D211 are mutually exclusive**, and all three pydocstyle conventions disable D203 by
   default. Selecting `ALL` and then hand-picking D-rules is how a repo ends up with an unsatisfiable
   docstring standard; ruff auto-disables the conflicting pair under `ALL`, which means the effective
   rule set is *not* the literal selector list.
7. **Choosing `lint.pydocstyle.convention` silently disables rules.** The default is `null`. Setting
   `"google"` turns off the D-rules incompatible with Google style. An agent that adds a convention to
   fix noise has also changed which defects are detectable, invisibly.
8. **The DOC family is preview.** DOC102/DOC201/DOC501 require `--preview`; codes and behaviour may
   change between ruff releases. A CI gate built on them is a gate built on unstable ground - pin the
   ruff version if you rely on them.
9. **`PLR6301 no-self-use` and `PLR0904 too-many-public-methods` are also preview** - the two rules an
   agent most wants for "this class is a god object" and "this method is not a method" are exactly the
   ones not enabled by default.
10. **The three line lengths.** PEP 8 says 79, the Google guide says 80, ruff defaults to 88. An agent
    citing "PEP 8 compliance" while running default ruff is asserting two incompatible standards. Only
    the configured number exists.
11. **`f-string` advice inverts inside logging calls.** The general idiom prefers f-strings; the
    logging manifest requires lazy `%` args, and records that mypy/pyright/ruff may push a rewrite the
    wrong way. An agent applying a blanket "modernise to f-strings" pass will deoptimise every log
    call and break the documented house rule.
12. **`PLC0415` versus "no work at import time".** The linter wants imports at the top; the practice
    wants module import to be free. The rule's own text legitimises deferred imports for circular
    dependencies, costly loads and optional dependencies. These cannot both be satisfied; the project
    must record which wins, and an agent must not "fix" either direction unilaterally.
13. **`F401` in `__init__.py` is a trapdoor.** Removing an "unused" import there narrows the package's
    public interface. Ruff classifies that fix as unsafe *and* preview specifically in `__init__.py`.
    Re-export must be spelled `from x import y as y` or listed in `__all__` - and mypy
    `--no-implicit-reexport` only accepts those two spellings.
14. **A bare name in a `match` case is never a constant.** `case RED:` binds `RED` and matches
    everything; only `case Color.RED:` compares. The program runs, takes the first branch always, and
    no linter is obliged to complain. PEP 634 specifies this.
15. **`match` has no exhaustiveness error.** "If no case blocks qualify the match statement is
    complete." Adding an enum member breaks nothing loudly. Only `case _: assert_never(x)` turns it
    into a checker error.
16. **`str` never matches a sequence pattern.** `case [x]:` will not match `"a"` - `str`, `bytes` and
    `bytearray` are excluded by the spec. The branch is dead and silent.
17. **`slots=True` returns a different class object.** Anything that captured the class before the
    decorator - a registry, a decorator chain, an `isinstance` cache - now refers to a stale object,
    and a parameterised base `__init_subclass__` raises `TypeError`.
18. **Dataclass mutable-default detection is hashability-based since 3.11**, not type-based. A custom
    mutable class that defines `__hash__` sails through as a default value and is shared across every
    instance.
19. **`asdict()` deep-copies.** It recurses containers and `copy.deepcopy()`s everything else. Using it
    for logging or serialisation in a hot path is a hidden cost, and it breaks identity for
    non-container fields.
20. **`StrEnum`/`IntEnum` members compare equal to plain values**, so a "migration to enums" can be
    half-finished forever without a single failing test. `str()` and `format()` return the *value*,
    not the name - which changes log output the moment you swap a plain constant for a `StrEnum`.
21. **`cached_property` lost its lock in 3.12.** Code written against 3.11's accidental serialisation
    becomes racy on upgrade with no diagnostic: "The getter function could run more than once on the
    same instance".
22. **`lru_cache` on a method leaks by design**, because `self` is part of the key. `B019` catches the
    decorator form; it does not catch a module-level cache keyed on an object you pass in.
23. **`-O` strips asserts; `-OO` strips docstrings.** Any contract expressed as `assert`, and any
    contract expressed as a docstring read at runtime, evaporates under optimisation flags. This is
    also why `S101` must be exempted in tests but enforced in `src`.
24. **`IGNORE_EXCEPTION_DETAIL` makes a doctest lie by omission** - the type must match, the message
    need not. A doctest documenting an error message can keep passing after the message changes.
25. **`typing.cast` and `Final` are promises, not checks** (typing manifest §3/§6). Nothing in this
    practices rung is enforced at runtime by the type system; do not describe a `Final` constant as
    immutable.
26. **PEP 727 is withdrawn.** Do not emit `Annotated[str, Doc("...")]` as "the modern way to document a
    parameter". There is no standard for it.
27. **Rule codes are not stable knowledge.** Two separate summaries of ruff's own rules index in this
    session mis-paired codes with names - one offered `D100` for `undocumented-public-function` (the
    verified code is `D103`) and `PLR0914` for `too-many-statements` (pylint's `too-many-statements` is
    `R0915`, and `R0914` is `too-many-locals`). Every code an agent writes into a config or a manifest
    must be read from that rule's own page or from `ruff rule <code>`.

## Honest limits

- **The whole "practices" rung is mostly convention.** Counting the routing table: roughly a third of
  the rows terminate in `contract-only`, and several of the lint-routed rows are *proxies* (a
  statement count standing in for cohesion, an ancestor count standing in for a bad inheritance
  relation). Single responsibility, feature envy, shotgun surgery, "utils", catch-log-rethrow, comment
  drift and comprehension complexity have **no mechanical enforcement at all** at this altitude. That
  is the honest state of the art, not a gap in this research.
- **No measurement backs the numeric thresholds.** `max-args = 5`, `max-complexity = 10`,
  `max-statements = 50`, `max-branches = 12`, `max-returns = 6`, `max-public-methods = 20`,
  `--fail-under = 80.0` are tool defaults. None of the pages that publish them cites a study. Treat
  them as coordination devices - a shared number a team stops arguing about - not as thresholds with
  evidence behind them.
- **The two style authorities disagree with each other and with the tools.** PEP 8 is Process-type
  advice with built-in escape hatches; the Google guide is one company's rules (and names pytype and
  pylint, neither of which this manifest set uses); ruff's defaults are a third position. Any claim
  that a codebase is "PEP 8 compliant" is unverifiable in general - what is verifiable is that it
  passes a named rule set at a named version.
- **Anti-pattern names rest on books I did not read.** The Blob / god object (AntiPatterns 1998, Riel
  1996), the 24-smell enumeration from Refactoring 2nd ed., and Composed Method (Beck 1996) are all
  FLAGGED-SECONDARY here: I verified bibliographic facts and, for the refactorings, Fowler's own online
  catalog, but the smell *list* and the Composed Method wording came from secondary summaries. "Stringly
  typed" has only a dictionary entry and an attribution. Anyone quoting these in a manifest should
  quote the name and the work, never a sentence.
- **Docstring style is genuinely unresolved.** PEP 257 does not pick a markup; the Google guide and
  numpydoc give incompatible answers on whether to repeat types that are already in annotations
  (Google says omit, numpydoc is silent); PEP 727 tried to end the microsyntax era and was withdrawn.
  Any manifest position here is a project decision, and the only thing that makes it real is the
  `lint.pydocstyle.convention` setting.
- **Nothing checks whether a docstring tells the truth.** The strongest available stack - `D103`
  presence, `interrogate` coverage, `DOC201`/`DOC501` structural agreement, doctest for the examples -
  still leaves preconditions, side effects and calling restrictions (precisely the things PEP 257
  demands) unverified. A docstring contract is only as good as the runtime contract or test behind it.
- **Version-bound content will rot fastest.** Every ruff code, default and preview flag is pinned to
  0.16.2 (2026-08-07), pylint codes to 4.0.6, mypy flags to 2.3.0. Preview rules in particular
  (DOC1xx/DOC2xx/DOC5xx, PLR6301, PLR0904) can be renamed, promoted or dropped between minor releases.
- **Code-to-name pairings taken from ruff's rules index rather than the rule's own page** (and therefore
  FLAGGED-SECONDARY, because that index summary demonstrably mis-paired other rows): `C400`, `C404`,
  `C416`, `C417`, `SIM103`, `SIM110`, `TRY301`, `BLE001`, `S101`, `ERA001`, `PLW0602`, and the
  `__all__`-validation codes. The rule *families* are confirmed; verify each code with
  `ruff rule <code>` before writing it into a config.
- **Not verified this session, and deliberately omitted rather than guessed:** the exact ruff codes for
  `too-many-branches` / `too-many-return-statements` (the settings keys and pylint codes are verified;
  the ruff codes were only seen on an index summary that proved unreliable elsewhere); the individual
  code-to-name pairings for the C4xx and `__all__`-validation families; whether `PLR0913` counts
  keyword-only parameters; the exact CPython `typing` docs wording for `assert_never` and for
  `@override`'s runtime attribute (the page truncated on fetch, and PEP 698 and the typing spec differ
  in what they promise); whether pylint's `no-self-use` still requires the
  `pylint.extensions.no_self_use` extension; and numpydoc's own validation check codes.

## Sources (accessed 2026-08-08)

- https://peps.python.org/pep-0008/ - PEP 8 Status Active / Type Process; the foolish-consistency
  escape hatches and "do not break backwards compatibility just to comply with this PEP!"; 79/72/99
  line limits; the complete naming table; underscore and name-mangling semantics; the public-vs-internal
  doctrine and `__all__`; annotation spacing; `is`/`isinstance`/bare-except/lambda recommendations.
- https://peps.python.org/pep-0020/ - Status Active, Type Informational, author Tim Peters; the 19
  aphorisms verbatim; no normative force.
- https://peps.python.org/pep-0257/ - Status Active, Type Informational; docstring definition and
  `__doc__`; one-line rules (imperative mood, no signature restatement); the normative list of what a
  multi-line function docstring must document; class/module/package/script docstring rules; explicit
  refusal to mandate markup.
- https://peps.python.org/pep-3107/ - Final/3.0; "Python does not attach any particular meaning or
  significance to annotations"; no standard semantics even for builtins; `__annotations__`.
- https://peps.python.org/pep-3102/ - Final/3.0; keyword-only syntax after `*args` and after a bare `*`.
- https://peps.python.org/pep-0570/ - Final/3.8; `/` positional-only; rename freedom, C parity,
  `**kwargs` collisions, performance; parameter ordering.
- https://peps.python.org/pep-0572/ - Final/3.8; the full prohibition list; comprehension binding in the
  containing scope; the PEP's own restraint advice.
- https://peps.python.org/pep-0616/ - Final/3.9; `removeprefix`/`removesuffix`; the documented
  `lstrip`/`rstrip` character-set confusion.
- https://peps.python.org/pep-0618/ - Final/3.10; `zip` silent truncation, `strict=True` raising
  `ValueError`, and why strict is not the default.
- https://peps.python.org/pep-0634/ - Final/3.10; capture vs value patterns, dotted-name requirement,
  `_` binding nothing, str/bytes/bytearray excluded from sequence patterns, mapping-pattern partiality,
  `__match_args__`, guards, no fallthrough, no error when nothing matches.
- https://peps.python.org/pep-0698/ - Final/3.12; `@override`; the two refactor failure modes and the
  production-outage motivation; best-effort `__override__ = True`.
- https://peps.python.org/pep-0727/ - **Withdrawn**; `typing.Doc` in `Annotated`; withdrawal reason
  ("mostly negative ... verbosity and readability").
- https://google.github.io/styleguide/pyguide.html - 80-column limit and its exceptions; docstring
  mandate criteria and Args/Returns/Raises; types need not be repeated when annotated; mutable-default
  ban; comprehension restriction; power-features ban; mutable-global-state ban; assert restrictions;
  "Never use staticmethod unless forced" and the `classmethod` restriction; public/internal naming
  table; `test_<method_under_test>_<state>`; pylint + pytype.
- https://numpydoc.readthedocs.io/en/latest/format.html - the 15 ordered sections; `name : type`
  formatting; optional/default/brace conventions; Raises "used judiciously"; Examples as doctest;
  silence on annotations and on validation codes.
- https://docs.python.org/3/library/functools.html - `cache` 3.9 == `lru_cache(maxsize=None)`;
  "The cache keeps references to the arguments and return values..."; "If a method is cached, the
  `self` instance argument is included in the cache."; the impure/side-effecting/generator warning;
  hashability requirement; `cached_property` `__dict__` requirement, PEP 412 note, 3.12 lock removal
  and `del` invalidation; `partial` `Placeholder` in 3.14; `wraps` attribute list and `__wrapped__`.
- https://docs.python.org/3/library/dataclasses.html - full parameter defaults with 3.10/3.11/3.14
  version notes; `slots=True` returns a new class and the `__init_subclass__` TypeError;
  hashability-based mutable-default rejection since 3.11; `KW_ONLY`; `asdict`/`astuple` deepcopy;
  `fields()` excluding ClassVar/InitVar.
- https://docs.python.org/3/library/enum.html - version map incl. StrEnum/ReprEnum/@verify at 3.11;
  StrEnum and IntEnum value-based `str()`/`__format__()`; operations leaving the enumeration;
  `Number.THREE == 3`; 3.11 `IntEnum.__str__` change; drop-in-replacement positioning; `@unique` and
  `@verify(UNIQUE|CONTINUOUS|NAMED_FLAGS)`; the `type(x) == str` interop caveat.
- https://docs.python.org/3/library/itertools.html - `pairwise` 3.10, `batched` 3.12 with `strict` 3.13;
  `tee` storage cost and thread-unsafety; `product` full consumption; `cycle` storage; `groupby`
  sortedness requirement.
- https://docs.python.org/3/library/contextlib.html - version notes for suppress/ExitStack/nullcontext/
  aclosing/chdir/AbstractContextManager/ContextDecorator/asynccontextmanager; single-use
  `@contextmanager` and `RuntimeError: generator didn't yield`; exceptions reraised at the yield point
  and the must-reraise rule; suppress + BaseExceptionGroup in 3.12; reentrancy is not thread safety.
- https://docs.python.org/3/library/pathlib.html - "pathlib is not a drop-in replacement for os.path"
  and the enumerated differences; the "Corresponding tools" mapping table; version notes for
  read_text/write_text, walk, glob params, is_relative_to, with_stem, hardlink_to, resolve(strict),
  mkdir(exist_ok), unlink(missing_ok), relative_to(walk_up).
- https://docs.python.org/3/library/doctest.html - invocation forms; "doctest is serious about requiring
  exact matches"; `<BLANKLINE>`; dict/set ordering, float and repr fragility; the flag list and
  directive syntax; traceback stack ignored; `IGNORE_EXCEPTION_DETAIL` semantics; the Soapbox position
  on documentation vs regression testing.
- https://docs.python.org/3/library/typing.html - `NewType` runtime behaviour and the 3.10/3.11
  performance notes; `Final`/`ClassVar`/`TypedDict`/`NamedTuple`/`LiteralString` (3.11)/`Self` (3.11).
  (The page truncated before the `override`/`assert_never` entries - recorded as OPEN.)
- https://typing.python.org/en/latest/spec/class-compat.html - the typing spec's `@override` rule
  (checkers must error unless it overrides a compatible ancestor member); no runtime attribute
  mentioned.
- https://docs.python.org/3/using/cmdline.html - `-X importtime` (3.7) and `-X importtime=2` (3.14) with
  `PYTHONPROFILEIMPORTTIME`; `-O` removing asserts and `__debug__` code; `-OO` discarding docstrings;
  `PYTHONOPTIMIZE`; `-X dev`, `-W`, `-I`/`-P`/`PYTHONSAFEPATH`.
- https://mypy.readthedocs.io/en/stable/command_line.html - `--no-implicit-reexport` semantics and the
  from-as / `__all__` spellings; the complete `--strict` flag list; docs build 2.3.0.
- https://pypi.org/project/ruff/ - ruff 0.16.2, released 2026-08-07.
- https://docs.astral.sh/ruff/linter/ - safe vs unsafe fix definitions verbatim; `--fix` /
  `--unsafe-fixes`; `lint.extend-safe-fixes` / `extend-unsafe-fixes`; the RUF015 IndexError ->
  StopIteration example; select/extend-select/ignore and prefix semantics; `ALL` auto-disabling
  conflicting rules; RUF100 for unused noqa.
- https://docs.astral.sh/ruff/formatter/ - the complete list of formatter-incompatible lint rules
  (W191, E111, E114, E117, D206, D300, D203, Q000-Q004, COM812, COM819, ISC002) and conflicting isort
  settings; E501 best-effort caveat; `docstring-code-format` default false; Black compatibility claim.
- https://docs.astral.sh/ruff/settings/ - `line-length` default 88; `lint.mccabe.max-complexity` 10;
  `lint.pylint.max-args` 5, `max-positional-args` 5, `max-statements` 50, `max-branches` 12,
  `max-returns` 6, `max-public-methods` 20; `lint.pydocstyle.convention` default null with
  google/numpy/pep257; `max-nested-blocks` absent.
- https://docs.astral.sh/ruff/rules/ - the rules index (used for family/prefix identity only; two
  separate summaries of this page mis-paired codes with names, so every code cited above was verified
  on its own page except where marked FLAGGED-SECONDARY).
- https://docs.astral.sh/ruff/rules/mutable-argument-default/ - B006; "Function defaults are evaluated
  once, when the function is defined"; the unsafe-fix rationale; `extend-immutable-calls`.
- https://docs.astral.sh/ruff/rules/function-call-in-default-argument/ - B008; defaults performed once
  at definition time; `extend-immutable-calls`.
- https://docs.astral.sh/ruff/rules/cached-instance-method/ - B019; the memory-leak wording (global
  cache retains the instance).
- https://docs.astral.sh/ruff/rules/zip-without-explicit-strict/ - B905; always-available fix marked
  **unsafe** and the reason ("can obscure situations where the iterables are of unequal length").
- https://docs.astral.sh/ruff/rules/boolean-type-hint-positional-argument/ - FBT001; bool and
  bool-containing unions; cites Adam Johnson's boolean-trap article.
- https://docs.astral.sh/ruff/rules/boolean-default-value-positional-argument/ - FBT002.
- https://docs.astral.sh/ruff/rules/boolean-positional-value-in-call/ - FBT003 and
  `lint.flake8-boolean-trap.extend-allowed-calls`.
- https://docs.astral.sh/ruff/rules/too-many-arguments/ - PLR0913, default 5, `lint.pylint.max-args`.
- https://docs.astral.sh/ruff/rules/too-many-positional-arguments/ - PLR0917, added v0.16.0, not
  preview, default 5, and the rule's own remedy text naming keyword-only migration.
- https://docs.astral.sh/ruff/rules/too-many-public-methods/ - PLR0904, **preview**, default 20.
- https://docs.astral.sh/ruff/rules/complex-structure/ - C901, mccabe, "one plus the number of decision
  points", `lint.mccabe.max-complexity`.
- https://docs.astral.sh/ruff/rules/magic-value-comparison/ - PLR2004 and
  `lint.pylint.allow-magic-value-types`.
- https://docs.astral.sh/ruff/rules/implicit-return/ - RET503, fix always available.
- https://docs.astral.sh/ruff/rules/superfluous-else-return/ - RET505, flake8-return.
- https://docs.astral.sh/ruff/rules/if-else-block-instead-of-if-exp/ - SIM108 and its "opinionated
  style rule" caveat incl. the line-coverage note.
- https://docs.astral.sh/ruff/rules/global-statement/ - PLW0603; "global mutable state is a common
  source of bugs and confusing behavior".
- https://docs.astral.sh/ruff/rules/mutable-class-default/ - RUF012 and the ClassVar remedy.
- https://docs.astral.sh/ruff/rules/unsorted-dunder-all/ - RUF022 and its unsafe-fix conditions.
- https://docs.astral.sh/ruff/rules/unused-import/ - F401; `__init__.py` behaviour, redundant-alias
  convention, `__all__` entry, and the unsafe/preview status of fixes in `__init__.py`.
- https://docs.astral.sh/ruff/rules/import-outside-top-level/ - PLC0415 and its three legitimate
  exceptions (circular dependency, costly load, optional dependency).
- https://docs.astral.sh/ruff/rules/os-path-join/ - PTH118, flake8-use-pathlib.
- https://docs.astral.sh/ruff/rules/builtin-open/ - PTH123 and the page's own performance concession.
- https://docs.astral.sh/ruff/rules/try-consider-else/ - TRY300 (tryceratops) and the `else`-clause
  rationale.
- https://docs.astral.sh/ruff/rules/error-instead-of-exception/ - TRY400; `logging.exception` vs
  `logging.error`; fix safe for `logging.error`, unsafe for logger-like calls.
- https://docs.astral.sh/ruff/rules/no-self-use/ - PLR6301, **preview**, with the
  staticmethod/classmethod/`@typing.override` exemptions.
- https://docs.astral.sh/ruff/rules/undocumented-public-function/ - D103 and
  `lint.pydocstyle.ignore-decorators`.
- https://docs.astral.sh/ruff/rules/docstring-missing-returns/ - DOC201, pydoclint, preview since 0.5.6.
- https://docs.astral.sh/ruff/rules/docstring-missing-exception/ - DOC501, pydoclint, preview since
  0.5.5.
- https://docs.astral.sh/ruff/rules/docstring-extraneous-parameter/ - DOC102, preview since 0.14.1.
- https://docs.astral.sh/ruff/rules/incorrect-blank-line-before-class/ - D203; disabled by default under
  google/numpy/pep257; mutually exclusive with D211; recommended against alongside the formatter.
- https://pylint.readthedocs.io/en/stable/user_guide/messages/messages_overview.html - pylint 4.0.6
  codes: R0913/R0914/R0912/R0915/R0911/R0902/R0904/R0901/R0903/R1702/R0801/R1710/R1721/R0205/R0401,
  C0103/C0114/C0115/C0116/C0200/C0209, W0603/W0602/W0212/W0102/W0718/W0719/W0621/W0611, E1310; and the
  unresolved `no-self-use` (R6301) extension question.
- https://pypi.org/project/pydoclint/ - pydoclint 0.9.1 (2026-07-03), NumPy/Google/Sphinx styles, DOC
  code prefix.
- https://interrogate.readthedocs.io/ - docstring-coverage purpose; `--fail-under` default 80.0 and the
  ignore flags; pre-commit hook; presence-only checking.
- https://import-linter.readthedocs.io/en/v2.7/contract_types.html - contract types `forbidden`,
  `layers` (with `exhaustive`), `independence`, `protected`, `acyclic_siblings`; `[importlinter]`,
  `root_package(s)`, `[importlinter:contract:...]` / `[[tool.importlinter.contracts]]`.
- https://martinfowler.com/bliki/CodeSmell.html - "A code smell is a surface indication that usually
  corresponds to a deeper problem in the system"; term credited to Kent Beck; dated 9 Feb 2006.
- https://martinfowler.com/bliki/FlagArgument.html - the Flag Argument definition, "My general reaction
  to flag arguments is to avoid them", the separate-methods remedy and the three nuances; 23 June 2011.
- https://refactoring.com/catalog/ - the online catalog for Refactoring 2nd ed.; verbatim confirmation
  of the refactoring names used above, including the "Replace Inheritance with Delegation" alias on
  Replace Superclass with Delegate.
- https://refactoring.com/catalog/replaceNestedConditionalWithGuardClauses.html - the guard-clause
  refactoring and its nested-to-linear motivation.
- https://martinfowler.com/articles/refactoring-2nd-ed.html - 2nd edition 2018, JavaScript examples,
  "all but 10 are still present, and I've added 17 new ones"; the page does **not** enumerate the
  smells (hence the FLAGGED-SECONDARY tag on the 24-smell list).
- https://dl.acm.org/doi/10.5555/280487 and https://en.wikipedia.org/wiki/AntiPatterns - bibliographic
  record for *AntiPatterns* (Brown, Malveau, McCormick, Mowbray; Wiley 1998) naming "The Blob", and the
  attribution of the earlier "god object" usage to Riel's *Object-Oriented Design Heuristics* (1996) -
  FLAGGED-SECONDARY.
- https://foldoc.org/stringly+typed - "stringly typed" defined as a play on "strongly typed", credited
  to Mark Simpson - FLAGGED-SECONDARY.
- Practitioner sources consulted for the two anti-patterns with no authority
  (https://www.theserverside.com/tip/Troubleshooting-Java-Code-Log-or-Re-Throw-but-Dont-Do-Both for
  catch-log-rethrow; https://breadcrumbscollector.tech/stop-naming-your-python-modules-utils/ and
  https://www.moderndescartes.com/essays/noutils/ for the "utils" module) - FLAGGED-SECONDARY, recorded
  so a later author does not mistake them for primary sources.
