# Python intrinsic hazards & the maximal-safety modern subset - fact pack (verified 2026-08-08)

**Diagnosis layer.** This pack names what is genuinely treacherous about Python-as-a-language, so that
the typing, lint and practice layers of the manifest set aim at real hazard classes rather than style
preferences. Every hazard is routed to the mechanism that mechanically catches it, or is honestly
recorded as `contract-only`. Tag legend: **ESTABLISHED** (normative in the cited primary source) ·
**VERSION-DEPENDENT (x.y)** (behaviour bound to a version) · **OPEN** (not confirmable this session).
`FLAGGED-SECONDARY` appears inline where the only evidence loaded was non-primary.

## Version table

| thing | current version | released (ISO) | source URL | tag |
|---|---|---|---|---|
| CPython stable | 3.14.7 | 2026-08-05 | task baseline; corroborated in-session by `docs.python.org/3` canonical links resolving to `www.python.org/3.14.7/...` | VERSION-DEPENDENT (3.14) |
| CPython prerelease | 3.15 (for 2026-10-01) | n/a | task baseline (devguide/python.org, pre-verified) | VERSION-DEPENDENT (3.15) |
| ruff rule index | version not printed on the index page | n/a | https://docs.astral.sh/ruff/rules/ | OPEN - pin `ruff==x.y.z` in-repo; individual rule pages carry "Stable since vX" markers (DTZ family: "Stable since v0.0.188") |
| pylint (docs "stable") | 4.0.6 | not stated on page | https://pylint.readthedocs.io/en/stable/user_guide/messages/messages_overview.html | VERSION-DEPENDENT (4.0.6) |
| mypy (docs "stable") | 2.3.0 | not stated on page | https://mypy.readthedocs.io/en/stable/error_code_list2.html | VERSION-DEPENDENT (2.3.0) |
| pyright config reference | `main` branch docs, no version stamp in raw markdown | n/a | https://raw.githubusercontent.com/microsoft/pyright/main/docs/configuration.md | OPEN - read the version-matched build |
| Import Linter | 2.3 | not stated on page | https://import-linter.readthedocs.io/en/v2.3/contract_types.html | VERSION-DEPENDENT (2.3) |
| PyYAML `load` deprecation | warning introduced in PyYAML 5.1+ | not stated | https://github.com/yaml/pyyaml/wiki/PyYAML-yaml.load(input)-Deprecation | VERSION-DEPENDENT (5.1) |
| pickle default protocol | protocol 5 | ships with CPython 3.14 | https://docs.python.org/3/library/pickle.html | VERSION-DEPENDENT (3.14) |
| int-to-str conversion limit | 4300 digits default | introduced in CPython 3.11 | https://docs.python.org/3/whatsnew/3.11.html | VERSION-DEPENDENT (3.11) |
| `decimal` default context | `prec=28`, `ROUND_HALF_EVEN` | long-stable | https://docs.python.org/3/library/decimal.html | ESTABLISHED |

---

## Facts

### Binding-time and default-argument hazards

1. Default values are evaluated **once, at function-definition time**, not per call: "Default values are
   created exactly once, when the function is defined. If that object is changed, like the dictionary in
   this example, subsequent calls to the function will refer to this changed object." The documented fix
   is `def foo(mydict=None): if mydict is None: mydict = {}` - ESTABLISHED
2. The same once-only evaluation makes any *function call* in a default argument a shared-state hazard,
   not only a literal `[]` or `{}` - ESTABLISHED
3. Closures capture **names, not values**: five lambdas built in `for x in range(5)` all return `16`,
   because "`x` is not local to the lambdas, but is defined in the outer scope, and it is accessed when
   the lambda is called - not when it is defined." The docs add: "this behaviour is not peculiar to
   lambdas, but applies to regular functions too." - ESTABLISHED
4. The documented workaround is a default-argument capture (`lambda n=x: n**2`), which "creates a new
   variable `n` local to the lambda and computed when the lambda is defined" - i.e. the mutable-default
   mechanism of fact 1, used deliberately - ESTABLISHED
5. `for` loops and `with` statements **do not create a scope**; the target name outlives the loop, and a
   nested loop reusing the name mutates the same variable, so "the value from the last iteration will
   'leak out' into the remainder of the enclosing loop" (ruff PLW2901 rationale) - ESTABLISHED
6. Rebinding a class-level ("static") attribute through an instance silently creates an unrelated
   instance attribute: "within a method of C, an assignment like `self.count = 42` creates a new and
   unrelated instance named 'count' in `self`'s own dict. Rebinding of a class-static data name must
   always specify the class" - ESTABLISHED
7. A mutable object bound in the class body is shared by every instance. ruff RUF012 states it plainly:
   "Mutable default values share state across all instances of the class, while not being obvious." -
   ESTABLISHED
8. `[[None] * 2] * 3` produces three references to **one** inner list: "replicating a list with `*`
   doesn't create copies, it only creates references to the existing objects" - ESTABLISHED

### Scoping rules agents get wrong

9. Binding anywhere in a block makes the name local for the **whole** block: "If a name binding operation
   occurs anywhere within a code block, all uses of the name within the block are treated as references
   to the current block. This can lead to errors when a name is used within a block before it is bound."
   - ESTABLISHED
10. A local name read before binding raises `UnboundLocalError`, which "is a subclass of `NameError`"; a
    name absent everywhere raises `NameError` - ESTABLISHED
11. Free-variable resolution happens **at call time, not definition time**; the docs' own example prints
    `42` for a function closing over `i`, where `i = 10` precedes the definition and `i = 42` follows it -
    ESTABLISHED
12. Class-block names are invisible to nested scopes, *including comprehensions*: "The scope of names
    defined in a class block is limited to the class block; it does not extend to the code blocks of
    methods. This includes comprehensions and generator expressions, but it does not include annotation
    scopes." The documented failing example is `class A: a = 42; b = list(a + i for i in range(10))` -
    ESTABLISHED
13. `nonlocal` binds to "the nearest enclosing function scope" and raises `SyntaxError` **at compile
    time** if no such binding exists; `global` redirects to the module namespace and "must precede all
    uses of the listed names" - ESTABLISHED
14. A comprehension runs in an implicit nested scope "aside from the iterable expression in the leftmost
    `for` clause", which "is evaluated directly in the enclosing scope and then passed as an argument to
    the implicitly nested scope" - so the leftmost iterable is the one place where enclosing-scope
    evaluation still applies - ESTABLISHED
15. The walrus operator is the deliberate hole in that isolation: "An assignment expression occurring in a
    list, set or dict comprehension or in a generator expression binds the target in the containing
    scope" (PEP 572, Final, 3.8) - ESTABLISHED
16. PEP 572 makes several walrus-in-comprehension shapes a `SyntaxError`: reusing the `for` target
    (`[i := i+1 for i in range(5)]`), unpacking-target collisions (`[i := 0 for i, j in stuff]`), and any
    named expression inside the iterable ("Named expressions are disallowed entirely as part of
    comprehension iterable expressions"). A walrus that would bind into a **class** scope is also a
    `SyntaxError` - VERSION-DEPENDENT (3.8)
17. PEP 709 (Final, 3.12) inlines list/dict/set comprehensions. Observable consequences: "A comprehension
    will no longer have its own dedicated frame in a stack trace"; `locals()` inside a comprehension now
    includes all locals of the containing function; `sys.settrace`/`sys.setprofile` no longer observe a
    call and return. Iteration-variable isolation is preserved - VERSION-DEPENDENT (3.12)

### Identity, equality and truthiness

18. Identity is guaranteed in exactly three documented circumstances: after `new = old`; after `s[0] = x`
    for a reference-storing container; and for singletons such as `None` - ESTABLISHED
19. Identity tests "should not be used to check constants such as `int` and `str` which aren't guaranteed
    to be singletons"; the docs' own examples show `10_000_000 is (5_000_000 + 5_000_000)` and
    `'Python' is ('Py' + 'thon')` both evaluating `False` - ESTABLISHED
20. The small-int cache is an explicitly labelled **CPython implementation detail**: "CPython keeps an
    array of integer objects for all integers between `-5` and `256`." Nothing in the language guarantees
    it, and no primary source guarantees string interning either - ESTABLISHED (as an implementation
    detail)
21. CPython emits a `SyntaxWarning` for `is` against a literal: `SyntaxWarning: "is" with 'int' literal.
    Did you mean "=="?` - ESTABLISHED
22. PEP 8's `is None` preference is documented as an *identity* argument, not a style one: it "avoids
    confusion with other objects that may have boolean values that evaluate to false" - ESTABLISHED
23. `bool` is a subtype of `int`: "The Boolean type is a subtype of the integer type, and Boolean values
    behave like the values 0 and 1, respectively, in almost all contexts, the exception being that when
    converted to a string, the strings `"False"` or `"True"` are returned" - ESTABLISHED
24. Truthiness is decided by `__bool__` or `__len__`; an object defining neither is always true, which is
    why a forgotten call (`if my_func:`) silently passes. mypy ships a **default-enabled** error code for
    exactly this: `truthy-function` - "Functions will always evaluate to true in boolean contexts." -
    VERSION-DEPENDENT (mypy 2.3.0)
25. mypy's `truthy-bool` and `truthy-iterable` cover the wider empty-vs-None conflation but are **opt-in**
    (`--enable-error-code=truthy-bool`, `--enable-error-code=truthy-iterable`) - VERSION-DEPENDENT
    (mypy 2.3.0)
26. Hash randomization is on by default and "affects the `__hash__()` values of str and bytes objects";
    values "remain constant within an individual Python process" but "are not predictable between
    repeated invocations of Python". `PYTHONHASHSEED=0` disables it - ESTABLISHED
27. Hashability requires a hash "which never changes during its lifetime" plus `__eq__`, and "Hashable
    objects which compare equal must have the same hash value" - so a mutable object used as a dict key is
    a latent corruption bug, and `bool`/`int` key collapse (fact 23) follows from the same contract -
    ESTABLISHED

### Copying and aliasing

28. "A *shallow copy* constructs a new compound object and then (to the extent possible) inserts
    *references* into it to the objects found in the original"; a deep copy "recursively, inserts
    *copies*". Slice-copy (`l[:]`) and `dict.copy()` are shallow - ESTABLISHED
29. `deepcopy` has two documented failure modes of its own: recursive objects "may cause a recursive
    loop", and "because deep copy copies everything it may copy too much, such as data which is intended
    to be shared between copies" - ESTABLISHED
30. `copy` silently does *not* copy "module, method, stack trace, stack frame, file, socket, window, or
    any similar types", and it returns functions and classes unchanged - ESTABLISHED
31. `copy.replace()` is the typed structural alternative for namedtuples, dataclasses, and classes
    defining `__replace__` - VERSION-DEPENDENT (3.13)

### Iteration, ordering and generators

32. An exhausted iterator stays exhausted and, critically, **looks empty rather than failing**: "any
    further calls to its `__next__()` method just raise `StopIteration` again ... Attempting this with an
    iterator will just return the same exhausted iterator object used in the previous iteration pass,
    making it appear like an empty container." - ESTABLISHED
33. `dict` insertion-order preservation is a **language guarantee**, not a CPython detail: "the
    insertion-order preservation nature of `dict` objects has been declared to be an official part of the
    Python language spec" - VERSION-DEPENDENT (3.7+)
34. No equivalent guarantee exists for `set`. Set iteration order interacts with hash randomization
    (fact 26), so any test depending on it is seed-dependent - ESTABLISHED (by documented absence)
35. Mutating a container while iterating it is a distinct hazard class with dedicated rules: ruff B909
    `loop-iterator-mutation`; pylint W4701/W4702/W4703 `modified-iterating-list`/`-dict`/`-set` -
    ESTABLISHED
36. Free-threaded CPython weakens iterator guarantees further: "free-threaded CPython does not guarantee
    thread-safe behavior of iterator operations" - VERSION-DEPENDENT (3.13+ free-threaded builds)

### Numeric hazards

37. `round()` is round-half-to-even: "if two multiples are equally close, rounding is done toward the even
    choice (so, for example, both `round(0.5)` and `round(-0.5)` are `0`, and `round(1.5)` is `2`)" -
    ESTABLISHED
38. The docs also warn this compounds with binary representation: "`round(2.675, 2)` gives `2.67` instead
    of the expected `2.68`. This is not a bug" - ESTABLISHED
39. `0.1` is not representable; the stored value is `3602879701896397 / 2 ** 55`. Since 3.1, `repr()`
    prints the shortest round-tripping form, which **hides** the discrepancy at the REPL -
    VERSION-DEPENDENT (3.1)
40. Float addition is not associative in practice: `0.1` added ten times `== 1.0` is `False`, while
    `sum([0.1] * 10) == 1.0` is `True` (extended precision), and `math.fsum()` "tracks all of the 'lost
    digits'". The documented comparison tool is `math.isclose()` - ESTABLISHED
41. `Decimal(0.1)` inherits the float's error exactly -
    `Decimal('0.1000000000000000055511151231257827021181583404541015625')` - whereas `Decimal('0.1')` is
    exact. Passing a float into `Decimal` is the most common decimal bug - ESTABLISHED
42. The default decimal context is `prec=28`, `rounding=ROUND_HALF_EVEN`, with traps for `Overflow`,
    `DivisionByZero`, `InvalidOperation` only: "All traps are enabled (treated as exceptions) except
    `Inexact`, `Rounded`, and `Subnormal`." Silent rounding is therefore the default - ESTABLISHED
43. `decimal` offers a *runtime* guard against accidental float mixing: "If the `FloatOperation` signal is
    trapped, accidental mixing of decimals and floats in constructors or ordering comparisons raises an
    exception" - ESTABLISHED
44. `Decimal('NaN') == Decimal('NaN')` is `False`: "A test for equality where one of the operands is a
    quiet or signaling `NaN` always returns `False`" - ESTABLISHED
45. `int`<->`str` conversion in bases other than 2/4/8/16/32 is capped: default limit **4300 digits**;
    exceeding it raises **`ValueError`**; the cap is a mitigation for CVE-2020-10735. Configurable via
    `sys.set_int_max_str_digits()` / `sys.get_int_max_str_digits()`, `-X int_max_str_digits`, and
    `PYTHONINTMAXSTRDIGITS`; `sys.int_info.default_max_str_digits` and
    `sys.int_info.str_digits_check_threshold` expose the default and the minimum settable non-zero value -
    VERSION-DEPENDENT (3.11)
46. Integer-division semantics for negative operands were **not** confirmed against a primary source this
    session - OPEN (load `library/stdtypes.html` numeric-operations table before any manifest asserts
    floor-toward-negative-infinity)

### Exception-handling hazards

47. Handler search stops at the first match: "This search inspects the `except` clauses in turn until one
    is found that matches the exception." A broad clause placed before a narrow one makes the narrow one
    dead code - ESTABLISHED
48. The `as` target is **deleted** at the end of the clause: "When an exception has been assigned using
    `as target`, it is cleared at the end of the `except` clause", implemented as an implicit
    `finally: del N`. Code that reads the name after the block raises `NameError`/`UnboundLocalError` -
    ESTABLISHED
49. `return`/`break`/`continue` in a `finally` clause silently destroys the in-flight exception: "If the
    `finally` clause executes a `return`, `break` or `continue` statement, the saved exception is
    discarded." As of 3.14 the compiler "emits a `SyntaxWarning` when a `return`, `break` or `continue`
    appears in a `finally` block (see PEP 765)" - VERSION-DEPENDENT (3.14)
50. A bare `except:` catches `BaseException`, "which includes `KeyboardInterrupt`, `SystemExit`, and
    others" (ruff E722 rationale) - ESTABLISHED
51. A bare `raise` outside a handler "will generate an error due to the lack of an active exception"
    (ruff PLE0704 rationale) - ESTABLISHED
52. Exception objects caught into a local are a documented reference-cycle source: "A common cause of
    reference cycles is when an exception has been caught in a local variable. The frame's locals then
    reference the exception, which references its own traceback, which references the locals of all frames
    caught in the traceback." - ESTABLISHED (CPython implementation detail, as labelled)

### assert, `-O` and `__debug__`

53. `-O` will "Remove assert statements and any code conditional on the value of `__debug__`"; `-OO` also
    "discard[s] docstrings". `PYTHONOPTIMIZE` is equivalent to `-O` - ESTABLISHED
54. `sys.flags.optimize` reports the level, so a runtime self-check can refuse to start under `-O` -
    ESTABLISHED
55. `assert (cond, "msg")` - a tuple, from a stray comma - always passes: "Non-empty tuples are always
    `True`, so an `assert` statement with a non-empty tuple as its test condition will always pass"
    (ruff F631; pylint W0199 `assert-on-tuple`, whose documented fix is to unpack and assert separately) -
    ESTABLISHED
56. A walrus inside an `assert` disappears under `-O` together with the assert: "the named assignment will
    also be ignored, which may result in unexpected behavior (e.g., undefined variable accesses)"
    (ruff RUF018) - ESTABLISHED

### Imports, module state and initialisation order

57. `sys.modules` is consulted first and is authoritative: "During import, the module name is looked up in
    `sys.modules` and if present, the associated value is the module satisfying the import, and the
    process completes. However, if the value is `None`, then a `ModuleNotFoundError` is raised." -
    ESTABLISHED
58. A module is registered **before** its body runs: "The module will exist in `sys.modules` before the
    loader executes the module code. This is crucial because the module code may (directly or indirectly)
    import itself; adding it to `sys.modules` beforehand prevents unbounded recursion." This is precisely
    why a circular import yields a *partially initialised* module rather than a clean failure -
    ESTABLISHED
59. Importing a submodule binds it as an attribute of the parent package, so `import spam` can expose
    `spam.foo` as a side effect of some other module's import - ESTABLISHED
60. `__init__.py` "is implicitly executed" on package import, and importing `parent.one` "will implicitly
    execute `parent/__init__.py` and `parent/one/__init__.py`" - import-time side effects are transitive -
    ESTABLISHED
61. A module *is* the language's singleton: "using a module is also the basis for implementing the
    singleton design pattern, for the same reason" - there is only one module object, so module-level
    mutable state is process-global state with no owner and no lifecycle - ESTABLISHED
62. `-X importtime` measures per-module import cost ("module name, cumulative time ... and self time"),
    and `-X importtime=2` marks already-cached modules - the cheapest mechanical probe for import-time
    side effects - ESTABLISHED

### Dynamic attribute access and object lifetime

63. `__getattribute__` "is called unconditionally for every attribute access"; `__getattr__` is called
    only when default lookup fails with `AttributeError`. Anything reachable only through those hooks is
    invisible to a static checker unless a stub declares it - ESTABLISHED
64. `__del__` is not a cleanup contract: "It is not guaranteed that `__del__()` methods are called for
    objects that still exist when the interpreter exits", exceptions inside it "are ignored, and a warning
    is printed to `sys.stderr`", and during shutdown "the global variables it needs to access (including
    other modules) may already have been deleted or set to `None`". The docs point at `weakref.finalize`
    instead - ESTABLISHED
65. `with` is the only structural guarantee: "The `with` statement guarantees that if the `__enter__()`
    method returns without an error, then `__exit__()` will always be called." - ESTABLISHED
66. A `@contextmanager` generator without `try`/`finally` skips its own cleanup on exception, because the
    exception "is reraised inside the generator at the point where the yield occurred"; and a generator
    that traps without re-raising silently **suppresses** the exception: "the generator context manager
    will indicate to the `with` statement that the exception has been handled" - ESTABLISHED
67. Context managers are not uniformly reusable: "Most context managers ... can only be used effectively
    in a `with` statement once", and reusable-but-not-reentrant managers "will fail ... if the specific
    context manager instance has already been used in a containing with statement" (`threading.Lock`,
    `ExitStack`) - ESTABLISHED
68. `functools.lru_cache`/`cache` on a method leaks instances: "the global cache will retain a reference
    to the instance, preventing it from being garbage collected" (ruff B019) - ESTABLISHED
69. Python Development Mode (`-X dev` / `PYTHONDEVMODE=1`) is equivalent to
    `PYTHONMALLOC=debug PYTHONASYNCIODEBUG=1 python -W default -X faulthandler`, and specifically surfaces
    `ResourceWarning` (plus `DeprecationWarning`, `ImportWarning`, `PendingDeprecationWarning`), enables
    faulthandler, logs `io.IOBase` destructor `close()` exceptions, and checks `encoding`/`errors`
    arguments - ESTABLISHED
70. `NamedTemporaryFile(delete=True, delete_on_close=False)` relies on finalisation and says so:
    "Deletion is not always guaranteed in this case (see `object.__del__()`)" - VERSION-DEPENDENT
    (`delete_on_close` added 3.12)

### Dataclass-specific hazards

71. `@dataclass` rejects a mutable default by *hashability*, not by type: it "will raise a `ValueError` if
    it detects an unhashable default parameter. The assumption is that if a value is unhashable, it is
    mutable." Before 3.11 the check was a hard-coded `list`/`dict`/`set` blocklist -
    VERSION-DEPENDENT (3.11)
72. `field(default_factory=...)` "must be a zero-argument callable"; "It is an error to specify both
    *default* and *default_factory*"; the docs' own assertion is `assert D().x is not D().x` - ESTABLISHED
73. A *function call* as a dataclass default is the residual hole the `ValueError` misses if the result is
    hashable: "Function calls are only performed once, at definition time. The returned value is then
    reused by all instances of the dataclass" (ruff RUF009) - ESTABLISHED
74. Hashability is derived, not chosen: `eq` and `frozen` both true generates `__hash__`; `eq` true and
    `frozen` false sets `__hash__ = None` (unhashable); `eq` false leaves the superclass `__hash__`, which
    for `object` means **id-based hashing** - the silent path to "equal objects that hash differently" -
    ESTABLISHED
75. `unsafe_hash=True` combined with an explicit `__hash__` raises `TypeError`; `order=True` with
    `eq=False` raises `ValueError`; `order=True` over a class already defining any of `__lt__`/`__le__`/
    `__gt__`/`__ge__` raises `TypeError` - ESTABLISHED
76. `__post_init__` is called by the generated `__init__` and also receives `InitVar` fields. On
    `frozen=True` the generated `__init__` "cannot use simple assignment ... and must use
    `object.__setattr__()`", which is exactly what user code must do to set derived fields - ESTABLISHED
77. A non-default field after a defaulted one raises `TypeError`, "whether this occurs in a single class,
    or as a result of class inheritance" - so adding a defaulted field to a base class can break unrelated
    subclasses - ESTABLISHED
78. Generated `__eq__` semantics changed: from 3.13 it "compares each field individually (e.g.,
    `self.a == other.a and self.b == other.b`)", where "In Python 3.12 and earlier, the comparison was
    performed by creating tuples of the fields" - VERSION-DEPENDENT (3.13)
79. `slots=True` and `kw_only=True` were both added in 3.10; from 3.11 a slot already present in a base
    class `__slots__` is omitted from the generated one - VERSION-DEPENDENT (3.10/3.11)
80. Mixing `frozen` and non-`frozen` dataclasses in one inheritance chain raises `TypeError` ("cannot
    inherit non-frozen dataclass from a frozen one" / the converse) - FLAGGED-SECONDARY: the
    `library/dataclasses.html` page loaded this session did not state this rule; evidence was CPython/
    project issue trackers and discuss.python.org only. Confirm against the `dataclasses` source or a
    docs section before asserting it in a manifest.

### Security-adjacent hazards

81. `eval()` and `exec()` each carry the identical documented warning: "This function executes arbitrary
    code. Calling it with untrusted user-supplied input will lead to security vulnerabilities." -
    ESTABLISHED
82. `pickle` "is not secure": "It is possible to construct malicious pickle data which will execute
    arbitrary code during unpickling." The docs recommend `hmac` signing if tamper-evidence is needed, and
    `json` for untrusted data - ESTABLISHED
83. `subprocess` does not use a shell unless asked: "this library will not implicitly choose to call a
    system shell. This means that all characters, including shell metacharacters, can safely be passed to
    child processes." With `shell=True`, "it is the application's responsibility to ensure that all
    whitespace and metacharacters are quoted appropriately", optionally via `shlex.quote()` -
    ESTABLISHED
84. Windows inverts the usual advice for batch files: `*.bat`/`*.cmd` "may be launched by the operating
    system in a system shell regardless of the arguments passed to this library ... consider passing
    `shell=True` to allow Python to escape special characters" - ESTABLISHED
85. `subprocess.run` does **not** raise on non-zero exit unless `check=True` is passed - ESTABLISHED
86. `tempfile.mktemp()` is deprecated since 2.3 and is a documented TOCTOU hole: "By the time you get
    around to doing anything with the file name it returns, someone else may have beaten you to the
    punch." Replacement: `mkstemp()` or `NamedTemporaryFile(delete=False)` - ESTABLISHED
87. `yaml.load` is unsafe by construction: "Running the `yaml.load` function over untrusted YAML files is
    insecure, as `yaml.load` allows for the creation of arbitrary Python objects, which can then be used
    to execute arbitrary code" (ruff S506). PyYAML's own wiki: `load` "has been unsafe since the first
    release in May 2006"; loader taxonomy is `BaseLoader` / `SafeLoader` (recommended for untrusted input)
    / `FullLoader` / `UnsafeLoader` (alias `Loader`) - ESTABLISHED
88. Audit hooks are telemetry, not a sandbox, and the docs say so: "They are not suitable for implementing
    a 'sandbox'. In particular, malicious code can trivially disable or bypass hooks added using this
    function." Security-sensitive hooks "must be added using the C API `PySys_AddAuditHook()` before
    initialising the runtime" - VERSION-DEPENDENT (3.8+)
89. `sys.addaudithook` can fail silently: "If any existing hook raises an exception derived from
    `RuntimeError`, the new hook will not be added and the exception is suppressed" - ESTABLISHED
90. `sys.remote_exec()` (PEP 768) adds a new in-process execution surface in 3.14, gated by
    `PYTHON_DISABLE_REMOTE_DEBUG`, `-X disable-remote-debug`, and `--without-remote-debug` -
    VERSION-DEPENDENT (3.14)

### Concurrency assumptions visible from single-threaded code

91. The GIL guarantees only bytecode-level atomicity: "Python offers to switch among threads only between
    bytecode instructions ... Each bytecode instruction and therefore all the C implementation code
    reached from each instruction is therefore atomic from the point of view of a Python program." -
    ESTABLISHED
92. The docs enumerate what is atomic (`L.append(x)`, `L1.extend(L2)`, `x = L[i]`, `x = L.pop()`,
    `L1[i:j] = L2`, `L.sort()`, `x = y`, `x.field = y`, `D[x] = y`, `D1.update(D2)`, `D.keys()`) and what
    is not (`i = i+1`, `L.append(L[-1])`, `L[i] = L[j]`, `D[x] = D[x] + 1`), and close with "When in
    doubt, use a mutex!" - ESTABLISHED
93. Even the atomic list is conditional: "Operations that replace other objects may invoke those other
    objects' `__del__()` method when their reference count reaches zero, and that can affect things." -
    ESTABLISHED
94. Signal handlers run only in one place: "Python signal handlers are always executed in the main Python
    thread of the main interpreter, even if the signal was received in another thread", and only that
    thread may install them (`ValueError` otherwise) - ESTABLISHED
95. Handler execution is deferred: "the low-level signal handler sets a flag which tells the virtual
    machine to execute the corresponding Python signal handler at a later point (for example, at the next
    bytecode instruction)", so "A long-running calculation implemented purely in C ... may run
    uninterrupted for an arbitrary amount of time, regardless of any signals received" - ESTABLISHED
96. Therefore `KeyboardInterrupt` can land anywhere: "a `KeyboardInterrupt` may appear at any point during
    execution. Most Python code, including the standard library, cannot be made robust against this"; the
    docs name the exact hole - "a context manager's `__exit__` method may not be called if
    `KeyboardInterrupt` occurs between `__enter__` and the return statement" - ESTABLISHED
97. `threading.Lock` "should not be used within signal handlers. Doing so can lead to unexpected
    deadlocks." - ESTABLISHED
98. Free-threaded builds change the ground under facts 91-93: PEP 703 free threading is "officially
    supported" in 3.14 with a stated "~5-10%" single-threaded penalty - VERSION-DEPENDENT (3.14)
99. `asyncio.create_task` results must be retained: "The event loop only keeps weak references to tasks. A
    task that isn't referenced elsewhere may get garbage collected at any time, even before it's done."
    `TaskGroup` is the documented fix because it "keeps strong references to each task" - VERSION-DEPENDENT
    (`TaskGroup`, `asyncio.timeout`: 3.11)

### Hazard-eliminating modern constructs (the subset question)

100. `match` bare names do not compare, they bind: "Capture patterns always succeed ... In simple terms
     `NAME` will always succeed and it will set `NAME = <subject>`." Only a **dotted** value pattern
     compares: "The dotted name in the pattern is looked up using standard Python name resolution rules.
     The pattern succeeds if the value found compares equal to the subject value" - VERSION-DEPENDENT
     (3.10)
101. At most one irrefutable case block is allowed and "it must be last" - so a stray bare-name case
     legitimately shadows everything after it and the compiler will say so - ESTABLISHED
102. Class patterns with positional sub-patterns depend on `__match_args__`, obtained as
     `getattr(cls, "__match_args__", ())` - dataclasses supply it, ad-hoc classes do not (and `kw_only`
     fields "are not included in `__match_args__`") - ESTABLISHED
103. `enum` supplies mechanical closure of value domains: duplicate values silently become **aliases**
     unless `@enum.unique` raises "`ValueError` ... with the details", or `@enum.verify(...)` enforces
     `UNIQUE` / `CONTINUOUS` / `NAMED_FLAGS` - VERSION-DEPENDENT (`verify`, `member`, `nonmember`,
     `StrEnum`: 3.11)
104. `IntEnum`/`IntFlag`/`StrEnum` are drop-in-compatible on purpose and therefore leak: `Number.THREE == 3`
     is `True`, and "`__str__` uses the value and not the name of the enum member", as does `__format__`.
     Plain `Enum` is the safer default - ESTABLISHED
105. `zip()` silently truncates to the shortest input unless `strict=` is passed; ruff carries a family for
     this: B905 `zip-without-explicit-strict` (fix available), B911 `batched-without-explicit-strict`,
     B912 `map-without-explicit-strict` - ESTABLISHED
106. 3.14 headline changes relevant to safety: PEP 649/749 deferred annotation evaluation is **now the
     default** with the new `annotationlib` module (`VALUE`/`FORWARDREF`/`STRING` formats); PEP 750
     template strings (`t'...'` producing `string.templatelib.Template` with separated static and
     interpolated parts, rather than an already-concatenated `str`); PEP 758 parenthesis-free
     `except A, B:`; PEP 765 `finally` `SyntaxWarning`; PEP 779 supported free threading; PEP 734
     `concurrent.interpreters` plus `concurrent.futures.InterpreterPoolExecutor`; PEP 768
     `sys.remote_exec` - VERSION-DEPENDENT (3.14)
107. `contextlib` supplies the composition primitives that remove finaliser reliance: `closing` (wraps a
     `close()`-bearing object), `ExitStack` ("designed to make it easy to programmatically combine other
     context managers and cleanup functions, especially those that are optional or otherwise driven by
     input data"), and `suppress` (explicit, narrow, greppable suppression) - ESTABLISHED
108. Ruff distinguishes fix *safety*: "The meaning and intent of your code will be retained when applying
     safe fixes, but the meaning could change when applying unsafe fixes." Only safe fixes run by
     default; `--unsafe-fixes` (or `unsafe-fixes` in config) opts in, and
     `lint.extend-safe-fixes`/`lint.extend-unsafe-fixes` re-classify per rule - ESTABLISHED
109. Import Linter 2.3 provides three contract types usable as architectural fitness functions:
     `type = forbidden` ("check that one set of modules are not imported by another set of modules"),
     `type = independence` ("check that a set of modules do not depend on each other"), and
     `type = layers` ("enforce a 'layered architecture', where higher layers may depend on lower layers,
     but not the other way around") - VERSION-DEPENDENT (2.3)
110. pytest turns warning classes into failures via the `filterwarnings` ini option (`filterwarnings =
     error` plus targeted `ignore::` lines) or `-W error::UserWarning`; and it already shows
     `DeprecationWarning`/`PendingDeprecationWarning` by default per PEP 565 - ESTABLISHED
111. pyright's default `typeCheckingMode` is `standard`, and several hazard-relevant rules are `"none"`
     even in strict: `reportUninitializedInstanceVariable` and `reportImplicitOverride` are `"none"` in
     all four modes. `reportUnnecessaryComparison`, `reportUnnecessaryIsInstance`,
     `reportUnnecessaryContains`, `reportUnnecessaryCast`, `reportUnusedVariable`,
     `reportUnknownMemberType`, `reportUntypedFunctionDecorator` are `"error"` only in strict;
     `reportPossiblyUnboundVariable` is `"error"` from **standard**; `reportUnhashable` is `"error"` from
     **basic**; `reportUnusedExpression` is `"warning"` from basic and `"error"` in strict -
     VERSION-DEPENDENT (pyright `main` docs; re-read the version-matched build)

---

## The routing table

Every mechanism below was verified this session against the tool's own rule page, index, or the CPython
docs. `contract-only` means nothing mechanical catches it and the manifest must say so.

| hazard / practice | why it bites | enforcement route | exact mechanism (rule code / flag / checker / test kind) | residual risk |
|---|---|---|---|---|
| Mutable default argument | default object created once at def time and mutated across calls | lint-catchable | ruff **B006** `mutable-argument-default` (fix available); pylint **W0102** `dangerous-default-value` | detects literal/known-mutable defaults; a mutable instance returned from a call is B008's job |
| Function call in a default argument | evaluated once at def time | lint-catchable | ruff **B008** `function-call-in-default-argument` (no fix) | intentional sentinel factories need per-call `noqa`; B008 has a configurable allowlist |
| Mutable default on a dataclass field | shared across all instances | feature-eliminated + lint-catchable | `@dataclass` raises **`ValueError`** for an unhashable default (3.11+: hashability, not a type blocklist); ruff **RUF008** `mutable-dataclass-default` (safe fix to `field(default_factory=...)`) | a *hashable* mutable (custom class with `__hash__`) slips past the ValueError |
| Function call as a dataclass default | one shared return value for every instance | lint-catchable | ruff **RUF009** `function-call-in-dataclass-default-argument` | none material; the rule names the `default_factory` fix |
| Mutable class attribute (non-dataclass) | "share state across all instances of the class, while not being obvious" | lint-catchable | ruff **RUF012** `mutable-class-default` | needs `ClassVar` annotations to avoid false positives on genuinely class-level constants |
| Mutable `ContextVar` default | same object shared across all contexts | lint-catchable | ruff **B039** `mutable-contextvar-default` | none material |
| Late-binding closure over a loop variable | name resolved at call time; all closures see the last value | lint-catchable | ruff **B023** `function-uses-loop-variable` (no fix); pylint **W0640** `cell-var-from-loop` | both are heuristic; a closure stored via an intermediate helper can evade them |
| Loop variable read after the loop / possibly unbound | `for`/`with` do not scope; empty iterable leaves it unbound | type-catchable | pyright `reportPossiblyUnboundVariable` (**error from `standard`**); mypy `--enable-error-code=possibly-undefined`; mypy default `used-before-def`; pylint **E0601** `used-before-assignment`, **E0606** `possibly-used-before-assignment` | mypy's version is opt-in, so a mypy-only shop must enable it explicitly |
| Unused loop control variable | signals a misread loop | lint-catchable | ruff **B007** `unused-loop-control-variable` (fix available) | cosmetic on its own |
| Loop target shadows the iterator | iterating a name the body rebinds | lint-catchable | ruff **B020** `loop-variable-overrides-iterator` | none material |
| Loop variable rebound inside the body | value leaks into the rest of the enclosing loop | lint-catchable | ruff **PLW2901** `redefined-loop-name` | flags deliberate normalisation-in-place too |
| Mutating a container while iterating it | skipped elements / `RuntimeError` | lint-catchable | ruff **B909** `loop-iterator-mutation`; pylint **W4701/W4702/W4703** `modified-iterating-list`/`-dict`/`-set` | aliased mutation through a second name is invisible |
| Class-body name used inside a comprehension in the class body | class scope does not reach nested scopes | test-catchable | raises `NameError` at class-creation time, so any import of the module fails; cover with a smoke-import test | none - it is a hard failure, not a silent one |
| Walrus in a comprehension binding into the enclosing scope | deliberate leak, easily unintended | contract-only | documented in PEP 572; the illegal shapes are compile-time `SyntaxError`, the legal leak is not diagnosed | review only; keep walrus out of comprehensions by convention |
| `global` mutable module state | process-global state with no owner or lifecycle | lint-catchable | ruff **PLW0603** `global-statement`; pylint **W0603** `global-statement`, **W0602** `global-variable-not-assigned` | catches the `global` keyword, not mutation of an already-module-level container |
| `is` against an int/str/collection literal | identity is not value; interning is an implementation detail | lint-catchable + interpreter | ruff **F632** `is-literal` (**safe** fix); CPython `SyntaxWarning: "is" with 'int' literal`; escalate with `-W error::SyntaxWarning` / pytest `filterwarnings = error` | `is` against a *variable* holding a small int is undiagnosed |
| `== None` instead of `is None` | `__eq__` may be overridden; PEP 8 identity argument | lint-catchable | ruff **E711** `none-comparison` (fix marked **UNSAFE** - "may alter runtime behavior when used with libraries that override `==`/`__eq__`") | the unsafe fix is precisely the semantic change you may not want auto-applied |
| `== True` / `== False` | conflates truthiness with identity | lint-catchable | ruff **E712** `true-false-comparison` (fix always available, marked **UNSAFE**, same rationale) | as above |
| Truthiness standing in for an explicit test; empty-vs-`None` conflation | `0`, `""`, `[]`, `None` all falsy | type-catchable | mypy `--enable-error-code=truthy-bool`, `--enable-error-code=truthy-iterable`; pyright `reportUnnecessaryComparison` (error in **strict** only) | both are opt-in; neither expresses "empty is not the same as absent" as a domain rule |
| Forgotten call in a boolean context (`if fn:`) | function objects are always truthy | type-catchable | mypy **`truthy-function`** - enabled **by default** | none material where mypy runs |
| `bool` is an `int` subtype; `{1: a, True: b}` collapses | hash/eq contract makes them the same key | type-catchable (partial) | pyright `reportUnhashable` (**error from `basic`**) covers unhashable keys, not bool/int collapse | bool/int key collapse is contract-only; use `Literal`/`Enum` keys |
| Statement with no effect (forgotten call, stray comparison) | silently does nothing | lint + type-catchable | ruff **B018** `useless-expression`, **B015** `useless-comparison`; pylint **W0104** `pointless-statement`, **W0133** `pointless-exception-statement`; pyright `reportUnusedExpression` (warning from basic, error in strict) | expressions with real side effects are excluded by design |
| Builtin shadowing (`list`, `id`, `type`, `input`) | later code silently uses the shadow | lint-catchable | ruff **A001** `builtin-variable-shadowing`, **A002** `builtin-argument-shadowing`, **A003** `builtin-attribute-shadowing`, **A004** `builtin-import-shadowing`, **A006** `builtin-lambda-argument-shadowing`; pylint **W0622** `redefined-builtin` | the A-family is off by default in ruff; it must be selected explicitly |
| Local module shadowing a stdlib module name | `import json` resolves to your file | lint-catchable | ruff **A005** `stdlib-module-shadowing` | only catches names it knows as stdlib for the configured target version |
| Fixture/parameter shadowing an outer name | test reads the wrong object | lint-catchable | pylint **W0621** `redefined-outer-name` | noisy under pytest's fixture idiom; scope it to non-test packages |
| Shallow copy / slice-copy false confidence | nested objects remain aliased | contract-only | no rule verified; `copy.deepcopy` / `copy.replace` (3.13) are the constructs | test-catchable in practice: mutate the copy, assert the original is unchanged |
| `[[x] * w] * h` row aliasing | `*` replicates references | contract-only | documented in the FAQ; no rule verified | test-catchable by the same mutate-and-assert pattern |
| Generator/iterator consumed twice, appearing empty | exhausted iterators keep raising `StopIteration` | type-catchable (at the boundary) | annotate the *contract*: `Sequence[T]`/`list[T]` when re-iteration is required, `Iterable[T]`/`Iterator[T]` only when single-pass is intended; a checker then rejects the second pass over an `Iterator` parameter | a function annotated `Iterable[T]` that internally iterates twice is still legal to the checker |
| `itertools.groupby` group reused after advancing | groups are shared iterators | lint-catchable | ruff **B031** `reuse-of-groupby-generator` | none material |
| `return <value>` inside a generator | value is unreachable to callers except via `StopIteration.value` | lint-catchable | ruff **B901** `return-in-generator` | legitimate `yield from` delegation uses it deliberately |
| Depending on `set` iteration order | no language guarantee; interacts with hash randomization | test-catchable | run the suite under varying `PYTHONHASHSEED` (and once with `PYTHONHASHSEED=0` for reproduction); assert on `sorted(...)` or on sets, never on list order | a single-seed CI run hides the dependency indefinitely |
| Depending on `dict` order | legitimate from 3.7 - this is *not* a hazard | feature-eliminated | language guarantee since 3.7 | applies to `dict` only; `set` and `**kwargs`-of-a-set are different questions |
| Float `==` comparison | binary representation; `repr` hides the error | contract-only + test-catchable | `math.isclose()` in code; `pytest.approx` in tests; no ruff/pylint rule verified for float equality | reviewer discipline is the only pre-commit gate |
| `round()` half-to-even surprise | documented behaviour, not a bug | feature-eliminated (in the money domain) | `decimal.Decimal` + `quantize(..., rounding=ROUND_HALF_UP)`; default context is `prec=28`/`ROUND_HALF_EVEN` | choosing `decimal` is a design decision no linter can make for you |
| `Decimal(float)` inheriting float error | float is converted losslessly, i.e. exactly wrongly | runtime-catchable | trap the `FloatOperation` signal in the decimal context: "accidental mixing of decimals and floats in constructors or ordering comparisons raises an exception" | must be installed at process start; nothing enforces that it is |
| Silent decimal rounding | `Inexact`, `Rounded`, `Subnormal` are untrapped by default | runtime-catchable | enable those traps in the `Context` explicitly | changes behaviour of existing arithmetic; adopt at a boundary |
| `NaN != NaN` | IEEE semantics; equality is always `False` | lint-catchable | pylint **W0177** `nan-comparison` | does not catch NaN arriving from data at runtime |
| Huge `int(str)` / `str(int)` raising | 4300-digit cap since 3.11 | test-catchable + runtime config | `ValueError`; configure with `sys.set_int_max_str_digits()`, `-X int_max_str_digits`, `PYTHONINTMAXSTRDIGITS`; test the boundary explicitly | raising a limit to accommodate real data re-opens the DoS the cap exists to prevent |
| Broad `except` before a narrow one (dead handler) | first matching clause wins | lint-catchable | pylint **E0701** `bad-except-order`, **W0705** `duplicate-except`; ruff **B014** `duplicate-handler-exception` (fix), **B025** `duplicate-try-block-exception`, **B030** `except-with-non-exception-classes`, **B029** `except-with-empty-tuple` | pylint's ordering check works on the static class hierarchy; a dynamically built tuple of types is opaque |
| Bare `except:` / catching `BaseException` | swallows `KeyboardInterrupt`/`SystemExit` | lint-catchable | ruff **E722** `bare-except`; pylint **W0718** `broad-exception-caught` (legacy **W0703** `broad-except`), **W0719** `broad-exception-raised` | a broad catch that logs and re-raises is legitimate and will be flagged |
| Reading the `except ... as e` name after the block | the target is deleted (`finally: del e`) | test-catchable | raises `NameError`/`UnboundLocalError`; pylint **E0601** `used-before-assignment` catches the common shape | assign to a separate name before leaving the handler; nothing forces you to |
| `return`/`break`/`continue` in `finally` | "the saved exception is discarded" | feature-eliminated (3.14) + lint-catchable | 3.14 compiler `SyntaxWarning` (PEP 765), escalated by `-W error::SyntaxWarning`; ruff **B012** `jump-statement-in-finally`; pylint **W0150** `lost-exception` | on <3.14 the warning does not exist - the lint rule is the only gate |
| `try/except/pass` (swallow and continue) | failure disappears | lint-catchable | ruff **S110** `try-except-pass`, **S112** `try-except-continue` | `contextlib.suppress` is the explicit, greppable form and is *not* flagged |
| Bare `raise` outside a handler | no active exception to re-raise | lint-catchable | ruff **PLE0704** `misplaced-bare-raise`; pylint **E0704** `misplaced-bare-raise` | none material |
| Exception caught into a local creating a reference cycle | frame -> exception -> traceback -> frames | contract-only | documented CPython behaviour; `gc` collects the cycle later | the implicit `del` on the `as` target is the language's own mitigation - do not defeat it by re-binding |
| `assert` enforcing anything | stripped under `-O`/`PYTHONOPTIMIZE` | lint-catchable | ruff **S101** `assert` ("Assertions are removed when Python is run with optimization requested"); guard the deployment with a `sys.flags.optimize` self-check | S101 is blanket - it also flags legitimate internal invariants and must be per-directory configured |
| `assert (cond, "msg")` - tuple always true | non-empty tuple is truthy | lint-catchable | ruff **F631** `assert-tuple`; pylint **W0199** `assert-on-tuple` | none - this is a clean catch |
| Walrus inside `assert` | binding vanishes with the assert under `-O` | lint-catchable | ruff **RUF018** `assignment-in-assert` | none material |
| Import-time side effects | transitive `__init__.py` execution; cost and order coupling | fitness-function | `-X importtime` / `-X importtime=2` in CI with a budget assertion; pylint **C0415** `import-outside-toplevel` governs the inverse (deferred imports) | measures cost and ordering, not purity; "no side effects at import" stays contract-only |
| Circular import / partially initialised module | module enters `sys.modules` before its body runs | fitness-function | Import Linter 2.3 contracts `type = layers`, `type = independence`, `type = forbidden`, run in CI | detects the *dependency* that permits the cycle; the runtime `ImportError`/`AttributeError` remains the last line of defence |
| Module-level mutable state; module-as-accidental-singleton | one module object per process, no lifecycle | contract-only | the FAQ names it explicitly ("using a module is also the basis for implementing the singleton design pattern"); PLW0603 covers only the `global` keyword | this is the highest-value contract-only row in the table - state it, do not pretend a linter covers it |
| `getattr`/`setattr` with a constant string | needlessly dynamic; invisible to checkers | lint-catchable | ruff **B009** `get-attr-with-constant` (fix), **B010** `set-attr-with-constant` (fix), **B043** `del-attr-with-constant` (fix) | dynamic names built at runtime are the real hazard and are not covered |
| Attribute created outside `__init__` | object shape varies by code path | lint + type-catchable | pylint **W0201** `attribute-defined-outside-init`; pyright `reportUninitializedInstanceVariable` (**`"none"` in every mode - must be enabled by hand**) | the pyright rule is off even in strict; teams assume strict covers it |
| `__getattr__`/`__setattr__`/monkeypatching defeating static checks | attribute access is satisfied at runtime by a hook | contract-only (+ partial lint) | pylint **E1101** `no-member` catches missing members on statically known classes; declare the real surface with `Protocol`/explicit attributes/stubs instead of a hook | anything reachable only through `__getattr__` is unchecked by construction; this is a design prohibition, not a lint |
| Monkeypatching leaking between tests | global state mutated for the process | test-catchable | pytest `monkeypatch` fixture (undoes at teardown) | hand-rolled `setattr` in a test body does not undo |
| Relying on `__del__` for cleanup | "not guaranteed that `__del__()` methods are called"; exceptions ignored | feature-eliminated + test-catchable | `with` (guaranteed `__exit__`), `contextlib.closing`/`ExitStack`, `weakref.finalize`; pylint **R1732** `consider-using-with`; detect leaks with `-X dev` + pytest `filterwarnings = error` turning `ResourceWarning` into a failure | `-X dev` must actually be on in CI; a leak with no `ResourceWarning` implementation stays invisible |
| `@contextmanager` generator without `try/finally` | cleanup skipped when the body raises | lint-catchable | pylint **W0135** `contextmanager-generator-missing-cleanup` | a generator that catches and does not re-raise silently *suppresses* the exception - not covered |
| Reusing a single-use context manager instance | "will fail ... if the specific context manager instance has already been used" | contract-only | documented in `contextlib`; no rule verified | test-catchable only if the second use is exercised |
| `lru_cache`/`cache` on a method | global cache pins `self` | lint-catchable | ruff **B019** `cached-instance-method` | `cached_property` and explicit per-instance caches are the alternatives |
| `asyncio.create_task` result discarded | event loop holds only weak references | lint-catchable + feature-eliminated | ruff **RUF006** `asyncio-dangling-task`; `asyncio.TaskGroup` (3.11) keeps strong references and aggregates failures | RUF006's "stored in a variable" heuristic can be satisfied without keeping the reference alive |
| `eval` / `exec` | "executes arbitrary code" | lint-catchable | ruff **S307** `suspicious-eval-usage`, **S102** `exec-builtin`; pylint **W0123** `eval-used`, **W0122** `exec-used` | `__import__`, `compile`, and `getattr`-driven dispatch reach similar power and are not all covered |
| `pickle` on untrusted data | arbitrary code execution during unpickling | lint-catchable | ruff **S301** `suspicious-pickle-usage`, **S403** `suspicious-pickle-import`, **S302** `suspicious-marshal-usage` | the rule cannot know whether the input is trusted - the boundary decision is yours |
| `subprocess(..., shell=True)` | shell metacharacter injection | lint-catchable | ruff **S602** `subprocess-popen-with-shell-equals-true`, **S604** `call-with-shell-equals-true`, **S605** `start-process-with-a-shell`, **S606** `start-process-with-no-shell`, **S607** `start-process-with-partial-path`, **S609** `unix-command-wildcard-injection`; **S603** `subprocess-without-shell-equals-true` covers the residue | Windows `.bat`/`.cmd` inverts the advice - the docs recommend `shell=True` there so Python performs the escaping |
| `subprocess.run` without `check=` | non-zero exit silently ignored | lint-catchable | pylint **W1510** `subprocess-run-check` | none material |
| `tempfile.mktemp()` / hard-coded `/tmp` paths | TOCTOU between name generation and use | lint-catchable | ruff **S306** `suspicious-mktemp-usage`, **S108** `hardcoded-temp-file` | `NamedTemporaryFile(delete=True, delete_on_close=False)` still says "Deletion is not always guaranteed" |
| `yaml.load` | arbitrary object construction | lint-catchable | ruff **S506** `unsafe-yaml-load` | `Loader=yaml.FullLoader` is not `SafeLoader`; only `safe_load`/`SafeLoader` is right for untrusted input |
| Insecure hash / weak randomness for security | wrong primitive for the job | lint-catchable | ruff **S324** `hashlib-insecure-hash-function`, **S303** `suspicious-insecure-hash-usage`, **S311** `suspicious-non-cryptographic-random-usage` | flags the call, not the purpose - non-security uses of `random` are false positives |
| Treating audit hooks as a sandbox | "malicious code can trivially disable or bypass hooks" | contract-only | the docs state the limit; C-API `PySys_AddAuditHook()` before runtime init is the only stronger form | do not build a security boundary on Python-level hooks |
| Naive `datetime` | local-vs-UTC ambiguity; `utcnow()` is a trap | lint-catchable | ruff **DTZ001**-**DTZ007**, **DTZ011**, **DTZ012**, **DTZ901** (`call-datetime-utcnow`, `call-datetime-now-without-tzinfo`, `call-date-today`, `datetime-min-max`, ...) | DTZ is off by default in ruff and must be selected |
| `open()` without `encoding=` | platform-dependent decoding | lint-catchable | pylint **W1514** `unspecified-encoding` | binary-mode false positives; `-X dev` also checks `encoding`/`errors` arguments |
| Drawing atomicity from the GIL | only bytecode boundaries are atomic; `i = i+1` is not | contract-only | the FAQ's explicit atomic/non-atomic lists and "When in doubt, use a mutex!" | free threading (3.14, PEP 779) invalidates informal reasoning built on the GIL |
| Signal-handler assumptions; `KeyboardInterrupt` anywhere | handlers run only in the main thread, deferred to a bytecode boundary; "`__exit__` may not be called if `KeyboardInterrupt` occurs between `__enter__` and the return statement" | contract-only | documented; install an explicit `SIGINT` handler for graceful shutdown rather than relying on `KeyboardInterrupt` | untestable in practice; a genuine residual risk to state, not to hide |
| `zip()` silently truncating | shortest input wins | lint-catchable | ruff **B905** `zip-without-explicit-strict` (fix), **B911** `batched-without-explicit-strict`, **B912** `map-without-explicit-strict` | `strict=True` converts a silent bug into a runtime `ValueError` - it must be a tested path |
| `match case Foo:` binding instead of comparing | bare names are capture patterns and always succeed | contract-only + test-catchable | the compiler rejects only the *ordering* consequence (at most one irrefutable block, and it must be last); use dotted `Enum`/`Final` value patterns so the intent is a value pattern | a bare-name case as the *last* block is legal and silently matches everything |
| Non-exhaustive `match` over a closed domain | new variant silently unhandled | type-catchable | mypy `--enable-error-code=exhaustive-match`; plus `typing.assert_never` in the fallthrough | requires the domain to be closed (`Enum`/`Literal`/discriminated union) in the first place |
| Enum value duplicated into a silent alias | duplicate values become aliases | feature-eliminated | `@enum.unique` (raises `ValueError` naming the alias) or `@enum.verify(EnumCheck.UNIQUE)`; also `CONTINUOUS`, `NAMED_FLAGS` | must be applied per class; nothing forces the decorator |
| `IntEnum`/`StrEnum` comparing equal to raw `int`/`str` | designed as drop-in replacements | contract-only | prefer plain `Enum`; the limitation is documented (`__str__`/`__format__` use the value) | choosing the mixin type is a design decision, not a lint |
| Mutable attribute narrowed in an override | subtype breaks the base contract | type-catchable | mypy `--enable-error-code=mutable-override` | opt-in |
| Override without `@override` | silent typo creates a new method | type-catchable | mypy `--enable-error-code=explicit-override` (PEP 698); pyright `reportImplicitOverride` (**`"none"` in every mode**) | both opt-in; pyright strict does not cover it |
| Calling a deprecated API | removal breaks later | type-catchable | mypy `--enable-error-code=deprecated` (reads PEP 702 `warnings.deprecated`); `-W error::DeprecationWarning` / pytest `filterwarnings = error` at runtime | only as good as the library's deprecation markers |
| Blanket `# type: ignore` | hides an unknown class of error | type-catchable | mypy `--enable-error-code=ignore-without-code` | forces a code onto the ignore; does not reduce their number |
| Unreachable / always-true branch | dead guard that looks protective | type-catchable | mypy `--warn-unreachable` (code `unreachable`), `--enable-error-code=redundant-expr`; pyright `reportUnnecessaryComparison`/`reportUnnecessaryIsInstance`/`reportUnnecessaryContains` (error in strict) | narrowing differences between checkers produce disagreement on which branch is dead |
| Frozen dataclass treated as deeply immutable | freeze is shallow and bypassable | contract-only | already owned by `python_typing_contract_manifest.md` §6 | - |

**Row count: 83 hazard rows.** Route tallies (rows may name a primary and a backstop, so these sum above 83): lint-catchable 46, contract-only 14, type-catchable 13, test-catchable 8, feature-eliminated 7, runtime-catchable 2, fitness-function 2, interpreter-warning 1.

---

## What the existing manifests already cover

Do not restate these; cite them.

- **`python_typing_contract_manifest.md` §5** already owns the `assert`/`-O`/`__debug__` mechanism and the
  "never use `assert` for validation, auth, or input checks" rule, plus `PYTHONOPTIMIZE`.
- **`python_typing_contract_manifest.md` §6** already owns `frozen=True` shallowness, `object.__setattr__`
  bypass, `Final` being checker-only, `Mapping` vs `MutableMapping` as a static-only promise, and the
  explicit statement that "It is not possible to create truly immutable Python objects."
- **`python_typing_contract_manifest.md` §3** already owns `typing.cast` having no runtime effect,
  `--strict-equality` as the anti-silent-coercion flag, and one sentence of the truthiness rule ("do not
  rely on truthiness as a stand-in for an explicit boolean test or count").
- **`python_typing_contract_manifest.md` §4** already owns what the type system cannot express (ranges,
  cross-field invariants, ordering/temporal constraints, units, typestate) and the `Annotated`/
  `annotated-types` metadata-is-inert fact.
- **`python_typing_contract_manifest.md` §1** already owns the `mypy --strict` flag list, the pyright
  four-mode table, and the "strict is not portable" argument - so this pack's routing table should cite
  §1 rather than re-derive it, and contribute only the *hazard-specific* opt-in codes.
- **`python_typing_contract_manifest.md` §5** already owns `dataclasses.__post_init__` as the validation
  seam and the `FrozenInstanceError`/`object.__setattr__` caveat.
- **`error_tracing_contract_manifest.md` §12** already owns catch-narrowly, bare `except`,
  `except BaseException`, and the `else`/`finally` roles.
- **`error_tracing_contract_manifest.md` §13** already owns EAFP vs LBYL and the TOCTOU caveat, quoting
  the glossary.
- **`error_tracing_contract_manifest.md` §14** already owns the full `assert` mechanism (`if __debug__:`
  desugaring, FOR/NOT-FOR lists) and §21 flags "assertions in production" as an open decision.
- **`error_tracing_contract_manifest.md` §8, §9, §10, §18, §19** own chaining (`from`, `__cause__`/
  `__context__`), `from None`, re-raise/wrap/suppress, `ExceptionGroup`/`except*`, and `add_note`.
- **`error_tracing_contract_manifest.md` §22** is the existing anti-pattern list; new hazard rows must be
  appended there in its one-line-per-rejection form rather than duplicated elsewhere.
- **`python_testing_tooling_manifest.md`** already covers pytest, `monkeypatch` as a double, and property
  testing - the natural home for "test-catchable" hazard rows.
- **`architecture_manifest_default.md`** mentions circular imports in passing (reasoning register, no
  version anchors) - do not retro-fit tags onto it.
- **Not covered anywhere today** (grep-verified across all nine files): mutable defaults, late binding,
  interning/identity, `is` vs `==`, `deepcopy`/aliasing, generator exhaustion, dict/set ordering, float
  and decimal traps, name shadowing, LEGB/comprehension scope, walrus, import-time side effects,
  partially initialised modules, `__del__`, `pickle`, `shell=True`, `tempfile`, `yaml.load`, audit hooks,
  GIL atomicity, and every ruff/pylint rule code except a single `ruff` mention in
  `logging_observability_manifest.md`.

---

## New content the manifest set should carry

### 1. `python_language_hazards_manifest.md` - the diagnosis layer
**NEW: `python_language_hazards_manifest.md`**

The owning file for this pack. Structure it as *hazard classes*, not as a tip list: binding-time hazards
(defaults, closures, class vs instance attributes), identity and truthiness, aliasing and copying,
iteration and ordering, numeric representation, exception mechanics not already owned by
`error_tracing_contract_manifest.md`, module initialisation, dynamic access, and object lifetime. Each
hazard gets three lines: the mechanism (quoted from the primary source), why an agent produces it, and
the routing verdict. The routing table above is the spine of the file. Cross-reference rather than
restate the typing and error manifests, whose overlaps are itemised in the section above.

### 2. The routing table as a first-class artifact
**Destination: `python_language_hazards_manifest.md`** (the table), with the CI wiring in
`python_quality_gates_manifest.md` (planned NEW)

Ship the hazard -> mechanism table as the file's centrepiece and derive the ruff `select`/`extend-select`
list *from it*, so every enabled rule traces to a named hazard and every hazard traces to a rule or to an
honest `contract-only`. This makes the ruff configuration reviewable: a rule with no hazard is noise, and
a hazard with no rule is a documented residual risk. The gates manifest owns *where* the checks run; this
manifest owns *why* each is selected.

### 3. The maximal-safety modern subset for a new 3.14 project
**Destination: `python_language_hazards_manifest.md`**, with version facts deferred to
`python_platform_baseline_manifest.md` (planned NEW)

State the subset as prohibitions plus their replacements, each tied to a hazard class it eliminates:
`with`/`ExitStack` instead of finaliser reliance; frozen dataclasses or `Enum` instead of ad-hoc mutable
records and string constants; `pathlib` instead of string paths; `match` over closed domains with
`assert_never`; `TaskGroup`/`asyncio.timeout` instead of loose `create_task`; `tomllib` instead of
hand-rolled config parsing; f-strings (and 3.14 t-strings where interpolation is *data*, since a
`Template` keeps static and interpolated parts separate); keyword-only parameters for booleans and
optionals; `zip(strict=True)`; typed protocols instead of duck typing. Say plainly which prohibitions are
mechanically enforced and which are review-only.

### 4. Silently-ineffective constructs
**Destination: `python_language_hazards_manifest.md`** (new subsection), with one-line rejections appended
to `error_tracing_contract_manifest.md` §22

The narrow class of code that *looks* like it enforces something and enforces nothing: `assert (cond,
"msg")`, `assert` under `-O`, walrus inside `assert`, `except` after a broader clause, `return` in
`finally`, `zip()` without `strict=`, `cast()` (already in the typing manifest), `Final`/`Protocol` at
runtime, `@enum.unique` omitted, `frozen=True` on a dataclass holding a list, and audit hooks used as a
sandbox. Each with the rule code that catches it, or an explicit "nothing catches this".

### 5. Import-time and module-state discipline
**Destination: `python_module_boundaries_manifest.md`** (planned NEW; per `_work/PLAN.md` it owns the
import system as a boundary)

The mechanism half of the module-boundary story: a module enters `sys.modules` before its body executes,
so a cycle yields a partially initialised module; submodule import binds attributes on the parent
package; `__init__.py` execution is transitive. Then the enforcement: Import Linter 2.3 `layers` /
`independence` / `forbidden` contracts in CI, `-X importtime` with a budget, and pylint C0415 as the
governor of deferred imports. Close with the honest part: "no side effects at import" and "no
module-level mutable state" are contract-only.

### 6. Determinism hazards a test suite must pin
**Destination: `python_testing_tooling_manifest.md`** (augment), cross-referenced from
`python_concurrency_determinism_manifest.md` (planned NEW)

The mechanical settings that convert latent hazards into failures: `filterwarnings = error` (with a
narrow `ignore::` allowlist), `-X dev` in CI so `ResourceWarning` fires on unclosed resources,
`-W error::SyntaxWarning` so `is`-with-literal and 3.14 `finally` warnings fail the build, and varying
`PYTHONHASHSEED` to expose set-ordering dependence. Note that these are additive and cheap, and that
each one maps to a specific row of the routing table.

### 7. Numeric-domain selection
**Destination: `python_language_hazards_manifest.md`**

A short decision section: `float` for measurement, `Decimal` for money and anything a human will audit,
`Fraction` for exact ratios, `int` where exactness is total. Give the three mechanical guards -
`FloatOperation` trapped in the decimal context, explicit `quantize` with a named rounding mode, and
`math.isclose`/`pytest.approx` in tests - and state that the default decimal context leaves `Inexact` and
`Rounded` untrapped, so silent rounding is the out-of-the-box behaviour.

---

## Traps for coding agents

1. **`E711`/`E712` autofixes are marked UNSAFE, and correctly so.** Ruff's own pages say the fix "may
   alter runtime behavior when used with libraries that override the `==`/`__eq__` or `!=`/`__ne__`
   operators". An agent running `ruff check --fix --unsafe-fixes` across a codebase using numpy, pandas,
   SQLAlchemy, or Django `Q` objects can silently change query and array semantics. Default `--fix` is
   safe-only; never add `--unsafe-fixes` to a blanket command.
2. **`S101` fights the testing manifest.** Ruff's `assert` rule flags every `assert`, including the ones
   pytest is built on. Enabling `S` globally without a per-directory exemption for tests produces hundreds
   of findings and trains agents to add blanket `noqa`. Configure `S101` off for the test tree.
3. **`assert (cond, "message")` always passes.** A single stray comma converts an assertion into a
   truthiness test on a non-empty tuple. Agents produce this when converting `assert cond, msg` to a
   multi-line form. F631 / W0199 catch it; nothing else will, and the test suite will look green.
4. **`-O` deletes more than asserts.** It removes "assert statements *and any code conditional on the
   value of `__debug__`*", and RUF018 exists because a walrus inside an assert vanishes with it, leaving
   later code referencing an undefined name. Any construct written for its side effect inside an `assert`
   is a latent `NameError` in an optimised deployment.
5. **pyright strict does not enable everything.** `reportUninitializedInstanceVariable` and
   `reportImplicitOverride` are `"none"` in **all four** modes, including strict. An agent that writes
   "we run pyright strict, so attribute initialisation is covered" is wrong. Conversely
   `reportPossiblyUnboundVariable` is already `"error"` at `standard`, and `reportUnhashable` at `basic` -
   so some hazards are covered before strict.
6. **mypy's hazard codes are mostly opt-in, but `truthy-function` is not.** `truthy-bool`,
   `truthy-iterable`, `possibly-undefined`, `redundant-expr`, `mutable-override`, `explicit-override`,
   `exhaustive-match`, `deprecated`, and `ignore-without-code` all require `--enable-error-code`;
   `truthy-function` and `used-before-def` are on by default. Do not claim `--strict` covers the opt-ins -
   it does not (see `python_typing_contract_manifest.md` §1 for the actual `--strict` list).
7. **The `A` (builtins) and `DTZ` (timezone) families are not on by default in ruff.** Ruff enables `F`,
   `E`, `B`, `UP`, `RUF` by default per its FAQ; builtin shadowing and naive-datetime hazards are simply
   unchecked until `extend-select` names them. An agent inspecting a clean `ruff check` run will conclude
   the code has no shadowing problems.
8. **`B023` and `W0640` are heuristic, and the correct fix is the mutable-default mechanism.** The
   documented remedy for late binding is a default-argument capture (`lambda n=x: ...`) - i.e. the very
   construct B006 exists to forbid. An agent applying both rules mechanically will fight itself. The
   resolution: default-argument capture of an *immutable* loop value is correct; B006 targets *mutable*
   defaults. Use `functools.partial` where the distinction is unclear.
9. **`zip(strict=True)` converts silence into an exception.** Adding it via B905's fix is a behaviour
   change on any path where the inputs genuinely differ in length. It is the right change, but it must be
   accompanied by a test for the mismatch path, not applied as a bulk autofix on unreviewed code.
10. **`case SOME_CONSTANT:` is a capture pattern, not a comparison.** A bare name always matches and binds.
    Because "A match statement may have at most one irrefutable case block, and it must be last", the
    compiler catches this only when other cases follow. As the final case it is legal and silently
    swallows every subject. Value patterns require a dotted name - use `Color.RED`, never `RED`.
11. **`yaml.FullLoader` is not the safe loader.** It "avoids arbitrary code execution" but still loads the
    full YAML language; `SafeLoader`/`safe_load` is what the project recommends for untrusted input. S506
    flags `yaml.load` regardless of loader, so an agent silencing S506 by adding
    `Loader=yaml.FullLoader` has satisfied the linter without satisfying the threat model.
12. **`dict` order is guaranteed; `set` order is not.** Agents frequently over-generalise the 3.7 dict
    guarantee to sets and to `dict` *comparison*. Set iteration order interacts with `PYTHONHASHSEED`, so
    a set-ordering dependence passes CI for months and then fails on one runner.
13. **`dataclass`'s mutable-default guard is a hashability test, not a type test.** From 3.11, "unhashable
    objects are now not allowed as default values. Unhashability is used to approximate mutability." A
    custom mutable class that defines `__hash__` passes the guard and is shared across every instance.
    RUF008/RUF009 are the backstop.
14. **`eq=False` gives you id-based hashing, silently.** With `eq` false, `__hash__` is left untouched and
    falls back to `object`'s. An agent adding `eq=False` for performance converts value equality into
    identity equality for dict/set membership without any diagnostic.
15. **Generated dataclass `__eq__` changed in 3.13.** Field-by-field comparison replaced tuple comparison,
    which changes behaviour around `NotImplemented` for non-identical types. Code that relied on
    cross-type comparison semantics behaves differently on 3.12 vs 3.13+.
16. **`NamedTemporaryFile` cleanup is not guaranteed in one configuration.** With `delete=True,
    delete_on_close=False` the docs say deletion happens "on context manager exit only, or else when the
    file-like object is finalized. Deletion is not always guaranteed in this case".
17. **`-X importtime` output "may be broken in multi-threaded application"** - the docs say so. Do not
    build a CI budget assertion on it for a threaded startup path without pinning single-threaded import.
18. **`sys.addaudithook` can fail silently.** If an existing hook raises a `RuntimeError` subclass, "the
    new hook will not be added and the exception is suppressed". An agent asserting "auditing is enabled"
    after calling it has no evidence.
19. **PEP 649 deferred annotations (default in 3.14) move annotation errors to first use.** An annotation
    that would previously have raised at import time now raises when something introspects it. Code that
    reads `__annotations__` directly should move to `annotationlib.get_annotations(...)` with an explicit
    `Format`.
20. **The 3.14 `finally` `SyntaxWarning` is a warning, not an error.** PEP 765 makes the hazard visible but
    still permits the code. It only fails a build under `-W error::SyntaxWarning` - and on <3.14 the
    warning does not exist at all, so B012 / W0150 are the portable gate.
21. **Comprehension inlining (3.12) removed the `<listcomp>` frame from tracebacks.** Diagnostic tooling,
    log parsers, and error-fingerprinting heuristics keyed on that frame name silently stop matching.
22. **Fixing an unclosed-resource `ResourceWarning` requires `-X dev` to be on.** Without development
    mode `ResourceWarning` is filtered by default, so `filterwarnings = error` alone does not surface
    unclosed files. Both settings are needed.

---

## Honest limits

- **Nothing mechanical enforces "no module-level mutable state" or "no import-time side effects."**
  Import Linter enforces *dependency direction*; `-X importtime` measures *cost*. Purity at import remains
  a review convention, and it is the single most consequential contract-only row in this pack.
- **Aliasing and copy-depth are contract-only.** No verified ruff or pylint rule distinguishes a
  correct shallow copy from an incorrect one, because the answer depends on ownership intent the code does
  not express. The mutate-the-copy test is the only mechanical check, and it only covers paths a test
  exercises.
- **`__getattr__`-based designs are unverifiable by construction, not merely unverified.** Advising
  against them is a design prohibition backed by no diagnostic. Any claim that a checker "handles"
  dynamic attributes is false unless a stub declares the surface statically.
- **Float and decimal discipline rests on domain judgement.** No linter can decide that a given quantity
  is money. The mechanical guards (trapped `FloatOperation`, explicit `quantize`, `math.isclose`) only
  work once a human has chosen the numeric domain.
- **`KeyboardInterrupt` robustness is explicitly declared out of reach by CPython itself**: "Most Python
  code, including the standard library, cannot be made robust against this." Any claim of
  interrupt-safe cleanup in ordinary Python is unfounded; the documented mitigation is a custom `SIGINT`
  handler, not more `try`/`finally`.
- **Rule-code stability is a real risk and this pack does not eliminate it.** The ruff index page carries
  no version stamp, so the codes here are pinned to *this session's* pages. Ruff has renamed and
  deprecated codes before (`A003` remains listed but attribute shadowing has been contentious). Any
  manifest built on these codes must pin `ruff`, `pylint`, `mypy`, and `pyright` versions in
  `pyproject.toml` and re-verify on upgrade.
- **The RUF section of the ruff index could not be read reliably.** A whole-section extraction returned
  rule names that individual rule pages contradicted, and one asserted rule (`mutable-frozen-dataclass`)
  returned HTTP 404. Only RUF006, RUF008, RUF009, RUF012, and RUF018 are asserted here, each verified on
  its own page. Do not import any other RUF code from this pack without re-verifying it.
- **Two facts remain unconfirmed.** Integer-division semantics for negative operands (fact 46) and the
  frozen/non-frozen dataclass inheritance `TypeError` (fact 80) were not established from a primary page
  loaded this session. Both are tagged accordingly; neither should be asserted in a manifest until
  verified.
- **"Which hazards agents actually produce most" is unmeasured.** The ordering and emphasis in this pack
  reflect the author's reading of the hazard mechanics and the density of dedicated lint rules (a decent
  proxy for community-observed frequency), not telemetry from agent-generated code. Treated as a
  hypothesis, not a finding.

---

## Sources (accessed 2026-08-08)

- https://docs.python.org/3/faq/programming.html - mutable defaults created once at def time and the
  `None`-sentinel fix; late-binding lambdas returning 16 and the `n=x` workaround; the three guaranteed
  identity circumstances and the `10_000_000`/`'Python'` non-singleton examples; PEP 8 `is None`
  rationale; `[[None]*2]*3` row aliasing; `self.count = 42` creating an unrelated instance attribute; the
  config-module/singleton equivalence; `copy.copy`/`copy.deepcopy` and slice-copy shortcuts.
- https://docs.python.org/3/reference/executionmodel.html - block definition; binding-anywhere-makes-local
  rule; `UnboundLocalError` as a `NameError` subclass; class-block scope not reaching nested scopes
  including comprehensions, with the failing `class A` example; call-time free-variable resolution;
  `global`/`nonlocal` exact effects and the compile-time `SyntaxError` for `nonlocal`.
- https://docs.python.org/3/reference/expressions.html - comprehension implicit nested scope and the
  leftmost-iterable exception; `is`/`is not` identity semantics; the `SyntaxWarning` for `is` with an
  `int` literal; cross-type comparison rules; generator `StopIteration` on exhaustion.
- https://docs.python.org/3/reference/compound_stmts.html - first-matching-`except` rule; the `as` target
  cleared at end of clause with the `finally: del N` desugaring; `finally` `return`/`break`/`continue`
  discarding the saved exception plus the 3.14 `SyntaxWarning` (PEP 765); `match` capture patterns always
  succeeding and binding; value patterns requiring a dotted name; at-most-one-irrefutable-block-and-last;
  `__match_args__` via `getattr(cls, "__match_args__", ())`; the `with`/`__exit__` guarantee.
- https://docs.python.org/3/reference/datamodel.html - `bool` as a subtype of `int`; `__getattribute__`
  called unconditionally vs `__getattr__` only on lookup failure; `__del__` not guaranteed at interpreter
  exit, exceptions ignored, shutdown globals possibly `None`, `weakref.finalize` as the alternative; the
  exception-in-a-local reference-cycle explanation.
- https://docs.python.org/3/reference/import.html - `sys.modules` checked first and `None` meaning
  `ModuleNotFoundError`; module present in `sys.modules` *before* the loader executes its code; submodule
  binding on the parent package; transitive `__init__.py` execution.
- https://docs.python.org/3/library/copy.html - shallow vs deep copy definitions; recursive-object and
  copies-too-much failure modes; the list of types not copied; `copy.replace()` added 3.13.
- https://docs.python.org/3/library/dataclasses.html - `ValueError` on unhashable defaults and the 3.11
  hashability-approximates-mutability change; `default_factory` semantics and
  `assert D().x is not D().x`; the full `eq`/`frozen`/`unsafe_hash` -> `__hash__` rules including
  `__hash__ = None` and the id-based fallback; `order`/`eq` `ValueError` and the `TypeError` on existing
  comparison methods; `__post_init__` and `InitVar`; the `object.__setattr__` requirement under `frozen`;
  non-default-after-default `TypeError` including via inheritance; the 3.13 field-by-field `__eq__`
  change; `slots`/`kw_only` added 3.10.
- https://docs.python.org/3/library/stdtypes.html - attempted for the integer-string-conversion section;
  the page truncated before that section, which is why fact 45 cites `whatsnew/3.11` and `sys` instead
  (recorded here as a limitation, not a citation).
- https://docs.python.org/3/library/sys.html - `set_int_max_str_digits`/`get_int_max_str_digits` (3.11),
  `int_info.default_max_str_digits` and `int_info.str_digits_check_threshold`; `addaudithook`/`audit`
  (3.8) including "not suitable for implementing a 'sandbox'", "malicious code can trivially disable or
  bypass hooks", the `PySys_AddAuditHook()` requirement, and silent failure on a `RuntimeError` subclass;
  `sys.flags.optimize` and `sys.flags.dev_mode`.
- https://docs.python.org/3/library/functions.html - `round()` round-half-to-even with `round(0.5)==0`,
  `round(-0.5)==0`, `round(1.5)==2`, and the `round(2.675, 2) -> 2.67` note; identical arbitrary-code
  warnings on `eval()` and `exec()`; `getattr`/`setattr` semantics and the private-name-mangling note.
- https://docs.python.org/3/library/decimal.html - `Decimal(0.1)` full expansion vs exact `Decimal('0.1')`;
  default context `prec=28` / `ROUND_HALF_EVEN`; traps `Overflow`/`DivisionByZero`/`InvalidOperation`
  enabled and `Inexact`/`Rounded`/`Subnormal` not; `FloatOperation` trap behaviour; `NaN` equality always
  `False`.
- https://docs.python.org/3/tutorial/floatingpoint.html - `1/10` as an infinitely repeating binary
  fraction and the `3602879701896397 / 2**55` stored value; shortest-repr since 3.1; ten-times-`0.1`
  vs `sum()` vs `math.fsum()`; `math.isclose()`; `decimal`/`fractions` alternatives.
- https://docs.python.org/3/library/contextlib.html - `@contextmanager` exception re-raised at the `yield`
  and the try/except/finally requirement, plus the suppression trap if the generator does not re-raise;
  `suppress`; `ExitStack`; `closing`; single-use vs reusable vs reentrant context managers.
- https://docs.python.org/3/library/asyncio-task.html - `TaskGroup` (3.11) cancellation and
  `ExceptionGroup` semantics including the `KeyboardInterrupt`/`SystemExit` special case; the
  weak-reference warning on `create_task` and the strong-reference-set idiom; `asyncio.timeout` (3.11).
- https://docs.python.org/3/library/signal.html - handlers always run in the main thread of the main
  interpreter and only it may install them; deferral to a bytecode boundary and the long-running-C-call
  consequence; `KeyboardInterrupt` may appear at any bytecode instruction and the `__enter__`/return
  window where `__exit__` may not run; `threading.Lock` in handlers causing deadlock; SIGINT ->
  `KeyboardInterrupt`.
- https://docs.python.org/3/library/subprocess.html - the Security Considerations section (no implicit
  shell; caller-owned quoting under `shell=True`; `shlex.quote`); the Windows `.bat`/`.cmd` inversion;
  sequence-preferred-over-string guidance; POSIX `/bin/sh -c` expansion; `check=` raising
  `CalledProcessError`.
- https://docs.python.org/3/library/pickle.html - the full security warning ("execute arbitrary code
  during unpickling", `hmac` signing, `json` for untrusted data); protocol 5 as the default from 3.14.
- https://docs.python.org/3/library/tempfile.html - `mktemp()` deprecated since 2.3 with the TOCTOU
  warning and `NamedTemporaryFile(delete=False)` replacement; `delete`/`delete_on_close` semantics and
  "Deletion is not always guaranteed in this case"; `delete_on_close` added 3.12.
- https://docs.python.org/3/library/enum.html - duplicate values becoming aliases and `@enum.unique`
  raising `ValueError`; `verify` + `EnumCheck.UNIQUE`/`CONTINUOUS`/`NAMED_FLAGS` (3.11); `IntEnum`/
  `IntFlag`/`StrEnum` comparing equal to raw values and `__str__`/`__format__` using the value;
  `StrEnum`, `member`, `nonmember` (3.11); `_ignore_` (3.7).
- https://docs.python.org/3/library/devmode.html - development mode equals
  `PYTHONMALLOC=debug PYTHONASYNCIODEBUG=1 python -W default -X faulthandler`; displays
  `DeprecationWarning`/`ImportWarning`/`PendingDeprecationWarning`/`ResourceWarning`; allocator debug
  hooks; faulthandler; asyncio debug; encoding/errors checks; `io.IOBase` destructor logging.
- https://docs.python.org/3/using/cmdline.html - `-O` removing asserts and `__debug__`-conditional code,
  `-OO` also discarding docstrings; `PYTHONOPTIMIZE`; `-X dev`/`PYTHONDEVMODE`; `-X int_max_str_digits`
  and `PYTHONINTMAXSTRDIGITS`; `-W` action list including `error`; `PYTHONWARNINGS`; `-X importtime` and
  `=2` plus the multi-threaded caveat; `PYTHONHASHSEED` semantics and what randomization affects.
- https://docs.python.org/3/glossary.html - GIL definition and `--disable-gil`/`-X gil=0`/`PYTHON_GIL=0`;
  free threading; hashable contract; immutable; the iterator-exhaustion "appear like an empty container"
  passage and the free-threaded iterator caveat; generator; duck-typing; EAFP; LBYL with the TOCTOU
  example; provisional API.
- https://docs.python.org/3/faq/library.html - "What kinds of global value mutation are thread-safe?": the
  bytecode-boundary atomicity model, the explicit atomic and non-atomic operation lists, the `__del__`
  caveat on replacing objects, and "When in doubt, use a mutex!".
- https://docs.python.org/3/whatsnew/3.7.html - dict insertion order "declared to be an official part of
  the Python language spec".
- https://docs.python.org/3/whatsnew/3.11.html - the 4300-digit default int/str conversion limit, the
  affected bases, `ValueError` on exceeding it, and CVE-2020-10735 as the motivation.
- https://docs.python.org/3/whatsnew/3.14.html - PEP 649/749 deferred annotations as the default plus
  `annotationlib` formats; PEP 750 t-strings producing `string.templatelib.Template`; PEP 758
  bracketless `except`; PEP 765 `finally` `SyntaxWarning`; PEP 779 free threading officially supported
  with the ~5-10% single-threaded note; PEP 734 `concurrent.interpreters` and
  `InterpreterPoolExecutor`; PEP 768 `sys.remote_exec` and its disable switches.
- https://docs.python.org/3/c-api/long.html - "CPython keeps an array of integer objects for all integers
  between `-5` and `256`", explicitly labelled a CPython implementation detail.
- https://peps.python.org/pep-0572/ - Final, 3.8; walrus in a comprehension binding in the containing
  scope; the `SyntaxError` cases including `for`-target reuse, unpacking collisions, and named expressions
  in the iterable; the class-scope `SyntaxError`.
- https://peps.python.org/pep-0709/ - Final, 3.12; comprehension inlining; no dedicated frame in
  stack traces; `locals()` now including containing-function locals; `settrace`/`setprofile` no longer
  seeing a call/return; iteration-variable isolation preserved.
- https://docs.astral.sh/ruff/rules/ - the flake8-bugbear (B) table (B002-B043, B901, B903, B904, B905,
  B909, B911, B912, with fix markers), the flake8-builtins (A001-A006) table, the full flake8-bandit (S)
  table (S101-S704), and the flake8-datetimez (DTZ001-DTZ012, DTZ901) table.
- https://docs.astral.sh/ruff/rules/mutable-class-default/ - RUF012, "Mutable default values share state
  across all instances of the class, while not being obvious."
- https://docs.astral.sh/ruff/rules/mutable-dataclass-default/ - RUF008, safe fix to
  `field(default_factory=...)`.
- https://docs.astral.sh/ruff/rules/function-call-in-dataclass-default-argument/ - RUF009, "Function calls
  are only performed once, at definition time."
- https://docs.astral.sh/ruff/rules/none-comparison/ - E711 (pycodestyle), fix marked **unsafe** because
  it "may alter runtime behavior when used with libraries that override the `==`/`__eq__` or `!=`/`__ne__`
  operators".
- https://docs.astral.sh/ruff/rules/true-false-comparison/ - E712, fix always available and marked
  **unsafe** for the same reason.
- https://docs.astral.sh/ruff/rules/function-uses-loop-variable/ - B023, "The loop variable is not bound
  in the function definition, so it will always have the value it had in the last iteration".
- https://docs.astral.sh/ruff/rules/jump-statement-in-finally/ - B012, `break`/`continue`/`return` in
  `finally` silencing exceptions.
- https://docs.astral.sh/ruff/rules/global-statement/ - PLW0603, `global` as mutable global state.
- https://docs.astral.sh/ruff/rules/redefined-loop-name/ - PLW2901, and the statement that `for` loops and
  `with` statements "don't define their own scopes".
- https://docs.astral.sh/ruff/rules/assert/ - S101, assertions "removed when Python is run with
  optimization requested".
- https://docs.astral.sh/ruff/rules/assert-tuple/ - F631, non-empty tuples always true.
- https://docs.astral.sh/ruff/rules/is-literal/ - F632, **safe** fix, `is` against literals and the 3.8+
  `SyntaxWarning`.
- https://docs.astral.sh/ruff/rules/assignment-in-assert/ - RUF018, named assignment ignored under `-O`
  leading to "undefined variable accesses".
- https://docs.astral.sh/ruff/rules/asyncio-dangling-task/ - RUF006, event loop retains only a weak
  reference.
- https://docs.astral.sh/ruff/rules/cached-instance-method/ - B019, `lru_cache`/`cache` on methods
  retaining the instance.
- https://docs.astral.sh/ruff/rules/misplaced-bare-raise/ - PLE0704, bare `raise` outside a handler.
- https://docs.astral.sh/ruff/rules/bare-except/ - E722 (pycodestyle), bare `except` catching
  `BaseException`.
- https://docs.astral.sh/ruff/rules/unsafe-yaml-load/ - S506, `yaml.load` allowing arbitrary object
  creation and arbitrary code execution.
- https://docs.astral.sh/ruff/rules/mutable-frozen-dataclass/ - **HTTP 404**; this is the evidence that the
  bulk RUF-section extraction was unreliable (see Honest limits).
- https://docs.astral.sh/ruff/linter/ - fix-safety definitions ("the meaning could change when applying
  unsafe fixes"), safe-only by default, `--unsafe-fixes`, the `unsafe-fixes` setting, and
  `lint.extend-safe-fixes`/`lint.extend-unsafe-fixes`.
- https://pylint.readthedocs.io/en/stable/user_guide/messages/messages_overview.html - pylint 4.0.6;
  confirmed symbolic names for W0102, W0640, W0622, W0621, E0601, E0602, W0603, W0602, E0701, W0705,
  W0212, W0123, W0122, W1510, W0107, W0703, W0718, W0719, E1120, W0611, W0612, W0613, R0902, W0201,
  E0203, W1514, W0231, W0246, W0133, E0704, W0150, W0143, W0177, R1732, W1508, W0104, E0110, C0415,
  W0642, E1101, W4701, W4702, W4703, E0606, W0135. (W0623 is not present.)
- https://pylint.readthedocs.io/en/stable/user_guide/messages/warning/assert-on-tuple.html - W0199
  `assert-on-tuple`, pylint 4.0.6, with the problematic/correct code pair.
- https://mypy.readthedocs.io/en/stable/error_code_list.html - `truthy-function` ("Functions will always
  evaluate to true in boolean contexts"), `used-before-def`, and `str-bytes-safe` are **enabled by
  default**.
- https://mypy.readthedocs.io/en/stable/error_code_list2.html - mypy 2.3.0; opt-in codes `truthy-bool`,
  `truthy-iterable`, `redundant-expr`, `possibly-undefined`, `exhaustive-match`, `mutable-override`,
  `deprecated`, `unused-awaitable`, `explicit-override`, `redundant-self`, `ignore-without-code`,
  `unimported-reveal`, plus `unreachable` via `--warn-unreachable`, `comparison-overlap` via
  `--strict-equality`, and `no-any-return` via `--warn-return-any`. `truthy-function` and
  `narrowed-type-not-subtype` are **not** on this page.
- https://raw.githubusercontent.com/microsoft/pyright/main/docs/configuration.md - default
  `typeCheckingMode` is `standard`; per-mode defaults confirming `reportUninitializedInstanceVariable` and
  `reportImplicitOverride` are `"none"` in all four modes, `reportPossiblyUnboundVariable` `"error"` from
  standard, `reportUnhashable` `"error"` from basic, `reportUnusedExpression` `"warning"` from basic and
  `"error"` in strict, and `reportUnnecessaryComparison`/`reportUnnecessaryIsInstance`/
  `reportUnnecessaryContains`/`reportUnnecessaryCast`/`reportUnusedVariable`/`reportUnknownMemberType`/
  `reportUntypedFunctionDecorator` `"error"` in strict only.
- https://docs.pytest.org/en/stable/how-to/capture-warnings.html - `filterwarnings = error` ini syntax
  with `ignore::` lines, `-W error::UserWarning`, `pytest.warns`, and PEP 565 default display of
  `DeprecationWarning`/`PendingDeprecationWarning`.
- https://import-linter.readthedocs.io/en/v2.3/contract_types.html - Import Linter 2.3; contract types
  `forbidden`, `independence`, `layers` with their verbatim descriptions, plus custom contract types.
- https://github.com/yaml/pyyaml/wiki/PyYAML-yaml.load(input)-Deprecation - `load` "has been unsafe since
  the first release in May 2006"; the `BaseLoader`/`SafeLoader`/`FullLoader`/`UnsafeLoader` taxonomy;
  warning introduced in 5.1+; `yaml.safe_load(input)` recommended for untrusted input.
- https://import-linter.readthedocs.io/en/latest/contract_types.html and
  https://import-linter.readthedocs.io/en/stable/contract_types.html - both returned **HTTP 404**; the
  versioned `v2.3` URL is the citable one.
