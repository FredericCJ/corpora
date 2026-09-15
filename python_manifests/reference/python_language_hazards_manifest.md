# Python Language Hazards — Ground-Truth Manifest

**Purpose.** The **diagnosis rung** of the enforcement ladder for small-to-mid-scale,
strictly-typed, single-process Python built as a functional core inside an imperative shell. It
names what is genuinely treacherous about the language and its stdlib — not what is unfashionable —
so the rungs above aim at real hazard classes: `python_typing_contract_manifest.md` **types** them,
`python_linting_practices_manifest.md` **lints** them, `python_quality_gates_manifest.md`
**enforces** them. It grounds five decisions: which constructs a new project prohibits and what
replaces each; which hazards earn a rule code and which are honestly `contract-only`; which rules an
agent assumes are on but must name explicitly in `select`; which numeric/temporal/textual domain
each quantity lives in; and what the maximal-safety modern subset for a 3.14 project is. **Scope.**
Hazards intrinsic to Python-the-language and the stdlib, at single-process scale. This file is
**GROUNDING, not a rulebook**: cite a principle when it materially shapes a decision; reason past it
when the situation does not match.

**Tag legend.** Every factual claim carries one: **ESTABLISHED** (normative and stable in the cited
primary source) · **VERSION-DEPENDENT (x.y)** (behaviour or default bound to a named version) ·
**OPEN** (no authoritative source; a convention this project must pin) · **CC-FACT** (Claude-Code
mechanics; none arise here). **FLAGGED-SECONDARY** appears inline where the only evidence was
non-primary. **MEASURED** marks a claim from running the tool rather than reading its docs — for
default-rule-set questions that is the *stronger* evidence, and §1.1 explains why. One blanket tag,
so the prose stays readable: **every "Why a competent agent produces it anyway" paragraph is
OPEN** — reasoned from the mechanics and from the density of dedicated lint rules, never
measured from telemetry on agent-written code (§19).

**Deferred to siblings, not duplicated.** Release dates and support phases →
`python_platform_baseline_manifest.md`. Type system, `--strict` flag lists, `cast`/`Final`/
`Protocol` runtime inertness, `frozen=True` shallowness → `python_typing_contract_manifest.md`.
Catch-narrowly, chaining, `ExceptionGroup`, EAFP/LBYL, the full `assert` doctrine →
`error_tracing_contract_manifest.md`. Rule-family config, suppression hygiene, idiom catalogue →
`python_linting_practices_manifest.md`. CI wiring, ratchets, metrics →
`python_quality_gates_manifest.md`. Import-boundary enforcement →
`python_module_boundaries_manifest.md`. Test kinds and fixtures →
`python_testing_tooling_manifest.md`. Execution models and determinism under test →
`python_concurrency_determinism_manifest.md`. `-X dev` as a diagnostic, faulthandler, post-mortem →
`python_runtime_diagnostics_manifest.md`. Logging-call rules → `logging_observability_manifest.md`.

**Version anchor.** CPython version, support-phase and PEP-status facts are owned by
`python_platform_baseline_manifest.md` (verified 2026-08-08); this file states *behaviour* and gates
it inline as `VERSION-DEPENDENT (3.x)`. Tool versions are this file's own subject, pinned
2026-08-08:

| tool | pinned version | note | tag |
|---|---|---|---|
| ruff | **0.16.2** (2026-08-07 PyPI / 2026-08-06 CHANGELOG) | the default rule set, fix-safety classes and every `[on]`/`[off]` marker below are that build's | VERSION-DEPENDENT (0.16.2) |
| ruff — the release that rewrote defaults | **0.16.0** (2026-07-23) | 59 → 413 default rules; 18 codes dropped (§1.1) | VERSION-DEPENDENT (0.16.0) |
| pylint | **4.0.6** (2026-06-14) | symbolic names verified against its message index | VERSION-DEPENDENT (4.0.6) |
| mypy | **2.3.0** | release date not separately confirmed — **OPEN** | VERSION-DEPENDENT (2.3.0) |
| pyright | **unpinned — OPEN** | per-mode defaults read from the unstamped `main`-branch `configuration.md`; re-read the version-matched build before trusting §1.3 | OPEN |
| Import Linter | **2.13** (2026-07-03) | version from PyPI; `latest` and `stable` docs URLs return HTTP 404, and 2.13's docs dropped the `.html` suffix, so cite the versioned directory path `/en/v2.13/contract_types/` | VERSION-DEPENDENT (2.13) |
| PyYAML | `yaml.load` deprecation warning from **5.1+** | loader taxonomy per the project wiki | VERSION-DEPENDENT (5.1) |

---

## TL;DR

- **An implicit default rule set is not a standard.** ruff 0.16.0 moved its default from 59 rules to
  **413** and *removed* 18, including `E711` and `E712` — the rules for `== None` and `== True`. A
  project with no explicit `select` had its standard rewritten by a version bump. Commit the rule
  set as an artefact; pin the tool. VERSION-DEPENDENT (ruff 0.16.0).
- **Route every hazard or delete the advice.** §2–§15 are the derivation source for the `select`
  list in `python_linting_practices_manifest.md`: a rule with neither a hazard row nor a recorded
  noise/consistency judgement (§0.3) is noise; a hazard with no rule is a documented residual risk.
  OPEN (house convention).
- **The asymmetries are the useful part.** Rules an agent expects to be running are off: ruff's `A`
  family, `S101` and `B905` are **not** default-on; mypy's hazard codes split between default-on
  (`truthy-function`, `used-before-def`) and `--enable-error-code`; pyright **strict** leaves
  `reportUninitializedInstanceVariable` and `reportImplicitOverride` at `"none"`. MEASURED (ruff
  0.16.2) / VERSION-DEPENDENT (mypy 2.3.0) / OPEN (pyright).
- **Never run `--unsafe-fixes` across code you have not reviewed.** Ruff marks fixes unsafe because
  "the meaning could change"; `E711`/`E712` fixes are unsafe precisely because a library may
  override `__eq__`. ESTABLISHED (ruff 0.16.2).
- **Prefer the construct that eliminates a class over the rule that flags it.** `with`/`ExitStack`
  over finalisers, frozen dataclasses and `Enum` over ad-hoc records and bare string constants,
  `TaskGroup` over loose `create_task`, `zip(strict=True)`, dotted value patterns in `match` (§18).
  VERSION-DEPENDENT (3.11–3.14 per construct).
- **Four classes are genuinely `contract-only`:** module-level mutable state and import purity,
  aliasing/copy depth, `__getattr__`-based designs, and `KeyboardInterrupt`-safe cleanup — the last
  declared out of reach by CPython's own docs (§19). ESTABLISHED.

---

## 0. How to read a routing verdict

### 0.1 The seven routes

| route | meaning | what it obliges the project to do |
|---|---|---|
| **type-catchable** | a named checker at a named strictness rejects it | enable the flag; record it in the checker config |
| **lint-catchable** | a named rule code rejects it | name the code in `select`/`extend-select`; never rely on a default |
| **feature-eliminated** | a modern construct removes the class outright | prohibit the old construct (§18); the rule becomes redundant |
| **test-catchable** | only a test observes it, and the test *kind* is named | write that test, or accept the risk in writing |
| **fitness-function** | a structural CI check (import contracts, budgets, seed sweeps) | wire it per `python_quality_gates_manifest.md` |
| **runtime-catchable** | a process-start configuration turns silence into an exception | install it in the entry point, and test that it is installed |
| **contract-only** | nothing mechanical catches it | say so in the spec and review for it; do not imply coverage |

An unrouted hazard is a defect in this file. `contract-only` stated honestly is a good answer;
implying coverage that does not exist is the failure. OPEN (house convention, `_work/PLAN.md`).

### 0.2 The `[on]` / `[off]` / `[?]` markers — read these before copying a code into a config

*Whether a rule runs by default* is a separate fact from *whether the rule exists*, and agents
conflate them. `[on]` = default-enabled in the named tool at the pinned version, evidence MEASURED
(`ruff check --isolated --show-settings`) or the tool's own error-code list. `[off]` = the rule
exists but is not default-enabled and must be named explicitly. `[?]` = **default status not
verified this session** — verify before relying on it. `[?]` is not padding: only a subset of the
ruff codes here had default status measured individually; the rest were confirmed only to *exist* on
their own rule page. Shipping a `[?]` code as if it were `[on]` is the failure this file exists to
prevent. The two-line check:

```
ruff check --isolated --show-settings                              # resolved enabled rule set
ruff rule --all --output-format json > .ruff-rule-baseline.json    # diff this on every bump
```

MEASURED (ruff 0.16.2): that JSON returns exactly **968** rule objects, **830** stable and **138**
preview-gated, of which **413** are default-enabled; of the 413, 198 have no fix, 116 always have
one, 99 sometimes do. VERSION-DEPENDENT (0.16.2).

Table-level tag, stated once so rows stay readable: **every mechanism named in a table below is
ESTABLISHED as existing in the named tool at the pinned version**; default-status markers are
VERSION-DEPENDENT (ruff 0.16.2 · pylint 4.0.6 · mypy 2.3.0 · pyright `main`); version-specific
*behaviour* inside a row is tagged inline.

### 0.3 The tables are a derivation source, not a reading list

`python_linting_practices_manifest.md` owns *which families to enable and how to configure them*.
This file owns *why any of them is enabled*. Read a hazard class here, take its codes, and the
`select` list writes itself with a traceable reason per entry. Reviewing a lint config then reduces
to two questions: **does every enabled rule trace to a hazard row here, to a hazard row in the
sibling that owns the topic (`LOG` → `logging_observability_manifest.md` §12a, `PT` →
`python_testing_tooling_manifest.md`, `D` → `python_linting_practices_manifest.md` §15 and §6.3),
or to an explicitly-recorded noise/consistency judgement in
`python_linting_practices_manifest.md` §3.2?** and **does every hazard row trace to a rule, a
construct, a test, or an explicit `contract-only`?** Ten of the 34 families in that file's
recommended
`select` (`UP`, `C4`, `LOG`, `FLY`, `ICN`, `INP`, `PIE`, `RSE`, `SLF`, `PYI`) name no code anywhere
in
this file: they are enabled on consistency or low-noise grounds, which is a *recorded judgement* and
a
legitimate answer — not a derivation from a hazard row. Do not read the first question as licence to
strip them. OPEN — a project convention, not a tool feature; pin it per
`software_spec_discipline_manifest.md` §G5.

### 0.4 pylint and pyright status caveats

pylint per-message default status was **not** enumerated this session, with one exception:
`useless-suppression` / **I0021** is disabled by default and must be added to `enable` (fail with
`--fail-on=I0021`). VERSION-DEPENDENT (pylint 4.0.6). Treat every other pylint code below as `[?]`;
the *symbolic names* are verified. pyright rows name the mode threshold inline, from an unversioned
`main`-branch document that must be re-read against the pinned build. OPEN.

---

## 1. Three asymmetries that make the routing tables worth reading

### 1.1 ruff 0.16.0: the default set is not a standard

**VERSION-DEPENDENT (ruff 0.16.0).** Before 0.16.0 the effective default `select` was
`["E4", "E7", "E9", "F"]` — **59** rules. From 0.16.0 the default is **413**, and eighteen codes
were
simultaneously *removed* from the default set. Two of those — **`E711`** (`== None`) and **`E712`**
(`== True`/`== False`) — are the enforcement route for an identity hazard documented in §4, so a
team
that upgraded without an explicit `select` lost them silently and gained ~370 other rules on the
same
commit. No diagnostic exists for either direction. **`lint.select` replaces the default set;
`lint.extend-select` adds to it** — `select = ["E", "F"]` on 0.16.x silently discards ~400 defaults,
including every `DTZ` rule, `B006`, `BLE001` and `RUF100`. ESTABLISHED (ruff docs).

**The full 18-code list, the measured prefix distribution of the 413, the per-family enable/disable
verdicts and the preview-selection trap are owned by `python_linting_practices_manifest.md`
§2.1–§2.5** and are not restated here; this file names the code a hazard routes to and moves on. Two
consequences that *are* this file's business:

1. **Default status is a measurement, not a documented fact.** One source asserted from ruff's FAQ
   prose that the `DTZ` (naive-datetime) family is *off* by default; direct measurement of 0.16.2
   puts **all ten `DTZ` rules inside the 413-rule default set**, while the `A` (builtin-shadowing)
   family is absent from it entirely. The measurement wins, and the rule generalises: **verify
   default status by measuring resolved settings (`ruff check --isolated --show-settings`), never by
   reading prose.** Every `[on]`/`[off]` marker below rests on that measurement. MEASURED (0.16.2)
   over FLAGGED-SECONDARY (FAQ).
2. **Pin the tool exactly**, because fix *safety* is reclassified between releases: 0.16.1 alone
   moved `PT022` and `FURB105` fixes to unsafe and `PT018` to safe. An unpinned ruff is an unpinned
   definition of "safe to autofix" (§17). VERSION-DEPENDENT (0.16.1).

### 1.2 mypy splits hazard codes between default-on and opt-in

**VERSION-DEPENDENT (mypy 2.3.0).** Two codes that catch hazards here are on by default:
**`truthy-function`** ("Functions will always evaluate to true in boolean contexts") and
**`used-before-def`**. Everything else needs `--enable-error-code` (or `enable_error_code =`, or a
`# mypy: enable-error-code="..."` file comment):

```
truthy-bool  truthy-iterable  possibly-undefined  redundant-expr  mutable-override
explicit-override  exhaustive-match  deprecated  ignore-without-code  unused-awaitable
unimported-reveal  redundant-self
```

None is inside `--strict`. `--strict` is a different list, owned by
`python_typing_contract_manifest.md` §1, and implies none of them; its members that matter here are
`--warn-redundant-casts`, `--warn-unused-ignores` and `--strict-equality` (which supplies
`comparison-overlap`). Separately `--warn-unreachable` supplies `unreachable`. **"We run `--strict`,
so the hazard codes are on" is false.**

### 1.3 pyright strict does not enable everything

**OPEN on version** (unstamped `main`-branch `configuration.md`; re-verify against the pinned
build). Default `typeCheckingMode` is `standard`.

| pyright rule | off | basic | standard | strict | hazard it routes |
|---|---|---|---|---|---|
| `reportUninitializedInstanceVariable` | none | none | none | **none** | attribute created outside `__init__` (§10) |
| `reportImplicitOverride` | none | none | none | **none** | a typo creates a new method instead of overriding (§12) |
| `reportUnnecessaryTypeIgnoreComment` | none | none | none | **none** | stale `# type: ignore` (§10) |
| `reportPossiblyUnboundVariable` | — | — | **error** | error | loop/branch variable read unbound (§2, §3) |
| `reportUnhashable` | — | **error** | error | error | unhashable dict/set key (§4) |
| `reportUnusedExpression` | — | warning | warning | **error** | statement with no effect (§4) |
| `reportUnnecessaryComparison` / `…IsInstance` / `…Contains` / `…Cast` | none | none | none | **error** | dead guard, always-true branch (§10) |
| `reportUnusedVariable` / `reportUnknownMemberType` / `reportUntypedFunctionDecorator` | none | none | none | **error** | — |

Three rules sit at `"none"` in **all four** modes, strict included: "we run pyright strict, so
attribute initialisation is covered" is wrong. Two hazards are covered *before* strict, so even a
`standard`-mode project has them.

### 1.4 Rule-code stability is a live risk, and this file does not eliminate it

**OPEN.** The ruff rule index carries no version stamp, so every code here is pinned to pages loaded
2026-08-08 plus a 0.16.2 measurement. Codes have been removed before: `TRY200`, `PGH001`, `PGH002`
and `PT004` are gone. Listing a removed code in `select` is **not** silent: the first three are
redirects that warn (`has been remapped to …`) and enable the successor, and `PT004` makes ruff
refuse to run (§15). MEASURED (0.16.2). One rule name asserted from a bulk index extraction
(`mutable-frozen- dataclass`) returned **HTTP 404** on its own page and is **quarantined out of this
file**. Of the `RUF` family only `RUF006`, `RUF008`, `RUF009`, `RUF012`, `RUF015`, `RUF018`,
`RUF028`, `RUF100`, `RUF101`, `RUF102`, `RUF103`, `RUF104` appear below — twelve codes, each
verified
on its own page or by measurement (`RUF015` by the §17 autofix demonstration). **Rule: re-verify
every code in `select` as part of every tool upgrade, not after it.**

---

## 2. Hazard class: binding time

**Mechanism.** Python evaluates some expressions once, when a `def` or `class` statement executes,
and resolves others on every call — and the split is not where intuition puts it. **ESTABLISHED:**
"Default values are created exactly once, when the function is defined. If that object is changed …
subsequent calls to the function will refer to this changed object"; the documented fix is the
`None` sentinel. The same rule makes *any function call* in a default a shared-state hazard, not
only a literal `[]`. **ESTABLISHED:** closures capture **names, not values** — five lambdas built in
`for x in range(5)` all return `16`, because `x` "is accessed when the lambda is called — not when
it is defined", and this "applies to regular functions too". **ESTABLISHED:** `for` and `with` do
not create a scope, so a loop target outlives its loop. **ESTABLISHED:** `self.count = 42` in a
method "creates a new and unrelated instance named 'count' in `self`'s own dict" — rebinding a
class-level datum "must always specify the class". **ESTABLISHED:** a mutable bound in a class body
is shared by every instance.

**Why a competent agent produces it anyway.** Each construct is the obvious spelling of the intent.
`def f(items=[])` is the shortest way to say "default to empty". A closure over the loop variable is
the shortest way to build callbacks — and it is *correct* whenever the callback fires before the
next iteration, so the same shape is sometimes right, which defeats pattern-matching. `self.x = ...`
is how instance state is normally created; the hazard appears only when a same-named class attribute
exists, which is invisible at the assignment site. A mutable class attribute is exactly how a
constant is declared, so the diagnosis depends on a `ClassVar` annotation the agent had no reason to
write. And **the documented remedy for late binding is a default-argument capture**
(`lambda n=x: n**2`), i.e. deliberately using the mechanism mutable-default rules forbid — §16.1
resolves that.

| hazard | why it bites | route | exact mechanism | residual risk |
|---|---|---|---|---|
| Mutable default argument | the default object is created once at `def` time and mutated across calls | lint-catchable | ruff **B006** `mutable-argument-default` `[on]` (fix Sometimes; it rewrites the body); pylint **W0102** `dangerous-default-value` `[?]` | detects literal/known mutables only; a mutable *returned from a call* is B008's job. The type checker sees a well-typed `list[int]` and objects to nothing |
| Function call in a default argument | `def f(t=now())` freezes one value for the process lifetime | lint-catchable | ruff **B008** `function-call-in-default-argument` `[on]` (no fix) | DI frameworks legitimately do this; the exemption needs a coded `noqa` someone reviews. B008 has a configurable allowlist |
| Mutable default on a dataclass field | one object shared by every instance | feature-eliminated + lint-catchable | `@dataclass` raises **`ValueError`**: `mutable default {type} for field {name} is not allowed: use default_factory`; ruff **RUF008** `mutable-dataclass-default` `[?]` (safe fix to `field(default_factory=...)`) | from 3.11 the guard is a **hashability** test, not a type test — VERSION-DEPENDENT (3.11). A custom mutable class defining `__hash__` slips through as a shared default |
| Function call as a dataclass default | "Function calls are only performed once, at definition time. The returned value is then reused by all instances" | lint-catchable | ruff **RUF009** `function-call-in-dataclass-default-argument` `[?]` | none material. `default_factory` "must be a zero-argument callable"; specifying both `default` and `default_factory` is an error |
| Mutable class attribute (non-dataclass) | "Mutable default values share state across all instances of the class, while not being obvious" | lint-catchable | ruff **RUF012** `mutable-class-default` `[?]` | needs `ClassVar` annotations to avoid firing on genuine class-level constants |
| Mutable `ContextVar` default | one object shared across every context | lint-catchable | ruff **B039** `mutable-contextvar-default` `[?]` | none material |
| Rebinding a class attribute through `self` | creates "a new and unrelated instance" attribute; the class datum is untouched | contract-only | no rule verified; the documented rule is "rebinding of a class-static data name must always specify the class" | review only. A test asserting the *class* attribute changed is the only mechanical check |
| Late-binding closure over a loop variable | the name resolves at call time, so every closure sees the final value | lint-catchable | ruff **B023** `function-uses-loop-variable` `[on]` (no fix); pylint **W0640** `cell-var-from-loop` `[?]` | both heuristic: they flag correct code that consumes the closure immediately, and miss a closure stored via an intermediate helper |
| Loop/branch variable read possibly-unbound | `for`/`with` do not scope; an empty iterable leaves the target unbound | type-catchable | pyright `reportPossiblyUnboundVariable` (**error from `standard`**); mypy `--enable-error-code=possibly-undefined` plus default `used-before-def`; pylint **E0601**, **E0606** `[?]` | mypy's version is opt-in, so a mypy-only shop must enable it |
| Unused loop control variable | signals a misread loop | lint-catchable | ruff **B007** `unused-loop-control-variable` `[?]` (fix available) | cosmetic alone; useful as a smell |
| Loop target shadows the iterator | iterating a name the body rebinds | lint-catchable | ruff **B020** `loop-variable-overrides-iterator` `[?]` | none material |
| Loop variable rebound inside the body | "the value from the last iteration will 'leak out' into the remainder of the enclosing loop" | lint-catchable | ruff **PLW2901** `redefined-loop-name` `[?]` | flags deliberate normalise-in-place too |
| `[[x] * w] * h` row aliasing | "replicating a list with `*` … only creates references to the existing objects" | contract-only | documented in the FAQ; no rule verified | test-catchable in practice: mutate one row, assert the others are unchanged |

---

## 3. Hazard class: scoping and shadowing

**Mechanism.** **ESTABLISHED:** "If a name binding operation occurs anywhere within a code block,
all uses of the name within the block are treated as references to the current block. This can lead
to errors when a name is used within a block before it is bound." The read raises
`UnboundLocalError`, "a subclass of `NameError`". Free-variable resolution happens at *call* time —
the docs' example prints `42` for a function closing over `i`, where `i = 10` precedes the
definition and `i = 42` follows it. Class-block names are invisible to nested scopes: "This includes
comprehensions and generator expressions, but it does not include annotation scopes"; the documented
failure is `class A: a = 42; b = list(a + i for i in range(10))`. A comprehension runs in an
implicit nested scope "aside from the iterable expression in the leftmost `for` clause", which "is
evaluated directly in the enclosing scope" — the one place enclosing-scope evaluation still applies.
**VERSION-DEPENDENT (3.8):** the walrus is the deliberate hole — "An assignment expression occurring
in a list, set or dict comprehension or in a generator expression binds the target in the containing
scope" (PEP 572, Final); several shapes are compile-time `SyntaxError` (reusing the `for` target,
unpacking collisions, any named expression inside the iterable, a bind into class scope).
**ESTABLISHED:** `nonlocal` binds "the nearest enclosing function scope" and raises `SyntaxError`
**at compile time** if none exists; `global` "must precede all uses of the listed names".

**VERSION-DEPENDENT (3.12):** PEP 709 inlines comprehensions. Consequences are diagnostic, not
semantic: "A comprehension will no longer have its own dedicated frame in a stack trace"; `locals()`
inside one now includes the containing function's locals; `settrace`/`setprofile` no longer see a
call and return. Iteration-variable isolation is preserved. Any log parser, error fingerprint or
traceback assertion keyed on a `<listcomp>` frame stopped matching at 3.12, silently.

**Why a competent agent produces it anyway.** The binding-anywhere rule is invisible at the *read*:
the code reads as a global lookup and the assignment fifty lines below changed its meaning.
Class-body comprehension scope is the most counter-intuitive rule in the language — the name is two
lines up, in the same block. Builtin shadowing happens because `list`, `type`, `id`, `input`,
`filter` and `format` are the most natural names for what they hold, and nothing marks them taken.
Shadowing a stdlib module name (`json.py`, `types.py`, `logging.py` in a package root) happens
because naming a file after the thing it wraps is good practice everywhere else.

| hazard | why it bites | route | exact mechanism | residual risk |
|---|---|---|---|---|
| Name bound later in the block, read earlier | binding anywhere makes the name local for the whole block; the read raises `UnboundLocalError` | type-catchable | mypy default `used-before-def`; pyright `reportPossiblyUnboundVariable` (**error from `standard`**); pylint **E0601**, **E0602** `[?]` | dynamic creation via `globals()[...]` defeats all three |
| Class-body name used inside a comprehension in the class body | class scope does not reach nested scopes | test-catchable | `NameError` at class-creation time, so any import of the module fails; a smoke-import test covers it | none — a hard failure, not a silent one |
| Walrus in a comprehension leaking into the enclosing scope | PEP 572 makes the leak deliberate; illegal shapes are `SyntaxError`, the legal leak is not diagnosed | contract-only | none verified | review only. Convention: no walrus inside a comprehension. VERSION-DEPENDENT (3.8) |
| Comprehension frame missing from a traceback | 3.12 inlining removed the dedicated frame | contract-only | documented in PEP 709 | tooling matching on `<listcomp>` fails silently. VERSION-DEPENDENT (3.12) |
| Builtin shadowing (`list`, `id`, `type`, `input`) | later code in the scope silently uses the shadow | lint-catchable | ruff **A001** `builtin-variable-shadowing` `[off]`, **A002** `builtin-argument-shadowing` `[off]`, **A003** `builtin-attribute-shadowing` `[off]`, **A004** `builtin-import-shadowing` `[off]`, **A006** `builtin-lambda-argument-shadowing` `[off]`; pylint **W0622** `redefined-builtin` `[?]` | **the whole `A` family is absent from ruff's 413-rule default set** — an agent inspecting a clean `ruff check` concludes there is no shadowing. MEASURED (0.16.2) |
| Local module shadowing a stdlib module name | `import json` resolves to your file | lint-catchable | ruff **A005** `stdlib-module-shadowing` `[off]` | only catches names it knows as stdlib for the configured `target-version` — so set `target-version` explicitly, never by inference |
| Fixture/parameter shadowing an outer name | the test reads the wrong object | lint-catchable | pylint **W0621** `redefined-outer-name` `[?]` | noisy under pytest's fixture idiom; scope it to non-test packages |
| `nonlocal` with no enclosing binding | compile-time failure | feature-eliminated | `SyntaxError` at compile time | none — cannot ship |

---

## 4. Hazard class: identity, equality and truthiness

**Mechanism.** **ESTABLISHED:** identity is guaranteed in exactly three documented circumstances —
after `new = old`; after `s[0] = x` for a reference-storing container; and for singletons such as
`None`. Identity tests "should not be used to check constants such as `int` and `str` which aren't
guaranteed to be singletons"; the docs' own examples show `10_000_000 is (5_000_000 + 5_000_000)`
and `'Python' is ('Py' + 'thon')` both **`False`**. The small-integer cache is a labelled CPython
**implementation detail** — "CPython keeps an array of integer objects for all integers between `-5`
and `256`" — and no primary source guarantees string interning at all. CPython emits
`SyntaxWarning: "is" with 'int' literal. Did you mean "=="?`. PEP 8's `is None` preference is an
*identity* argument: it "avoids confusion with other objects that may have boolean values that
evaluate to false". **ESTABLISHED:** `bool` is a subtype of `int` — Booleans "behave like the values
0 and 1 … in almost all contexts", the exception being their string conversion. With the hash
contract (a hash "which never changes during its lifetime", and "Hashable objects which compare
equal must have the same hash value"), `{1: a, True: b}` collapses to one key and a mutable dict key
is a latent corruption bug. Truthiness is decided by `__bool__` or `__len__`; an object defining
neither is always true, which is why a forgotten call (`if my_func:`) silently passes.

**Why a competent agent produces it anyway.** `is` reads as "equals" in English, is faster, and
*works* in the REPL for every small integer and identifier-like string — interning gives the wrong
code positive reinforcement on every ad-hoc check. `if not x:` is the idiomatic spelling and is
right whenever empty and absent should be treated alike; the hazard is that the call site does not
say whether they should. `if my_func:` is one dropped `()` from `if my_func():`, and both lines look
complete.

| hazard | why it bites | route | exact mechanism | residual risk |
|---|---|---|---|---|
| `is` against an int/str/collection literal | identity is not value; interning is an implementation detail | lint-catchable + interpreter | ruff **F632** `is-literal` `[on]`\* (**safe** fix); CPython `SyntaxWarning`, escalated with `-W error::SyntaxWarning` or pytest `filterwarnings = error` | `is` against a *variable* holding a small int is undiagnosed by every layer |
| `== None` instead of `is None` | `__eq__` may be overridden; the PEP 8 argument is identity | lint-catchable | ruff **E711** `none-comparison` **`[off]` — removed from the default set in 0.16.0**; fix marked **UNSAFE** ("may alter runtime behavior when used with libraries that override `==`/`__eq__`") | the unsafe fix is precisely the semantic change you may not want auto-applied. VERSION-DEPENDENT (0.16.0) |
| `== True` / `== False` | conflates truthiness with identity | lint-catchable | ruff **E712** `true-false-comparison` **`[off]` — also removed in 0.16.0**; fix always available, marked **UNSAFE**, same rationale | as above |
| Truthiness as a stand-in for an explicit test; empty-vs-`None` conflation | `0`, `""`, `[]`, `None` are all falsy | type-catchable | mypy `--enable-error-code=truthy-bool`, `--enable-error-code=truthy-iterable`; pyright `reportUnnecessaryComparison` (**error in strict only**) | both mypy codes are opt-in, and **neither expresses "empty is not the same as absent"** — that stays a domain rule |
| Forgotten call in a boolean context (`if fn:`) | function objects are always truthy | type-catchable | mypy **`truthy-function`** — **enabled by default** | none material wherever mypy runs. The one hazard code you get for free |
| `bool` is an `int` subtype; `{1: a, True: b}` collapses | one hash, one equality, therefore one key | contract-only (partial type route) | pyright `reportUnhashable` (**error from `basic`**) covers *unhashable* keys, not bool/int collapse | the collapse itself is contract-only; use `Literal` or `Enum` keys so the domain is closed |
| Mutable object as a dict/set key | the contract requires a hash that "never changes during its lifetime" | contract-only (partial) | pyright `reportUnhashable` (error from `basic`) for statically-known unhashables | a mutable-but-hashable custom class satisfies the checker and corrupts the mapping |
| Statement with no effect (forgotten call, stray comparison) | silently does nothing | lint + type-catchable | ruff **B018** `useless-expression` `[?]`, **B015** `useless-comparison` `[?]`; pylint **W0104** `pointless-statement` `[?]`, **W0133** `pointless-exception-statement` `[?]`; pyright `reportUnusedExpression` (warning from `basic`, error in strict) | expressions with real side effects are excluded by design, so a property with a side effect is not flagged |

\* `F632`'s `[on]` status is **derived**, not individually measured: the pre-0.16.0 default was
`["E4", "E7", "E9", "F"]` (all of `F`) and the published 18-code removal list touches only `F403`,
`F405`, `F406`, `F722`; the measured `F` count in the default set is 39. The same derivation covers
`F631` in §15. Confirm with `--show-settings`. MEASURED + derived (0.16.2).

---

## 5. Hazard class: aliasing and copy depth

**Mechanism.** **ESTABLISHED:** "A *shallow copy* constructs a new compound object and then (to the
extent possible) inserts *references* into it to the objects found in the original"; a deep copy
"recursively, inserts *copies*". Slice-copy (`l[:]`) and `dict.copy()` are shallow. `deepcopy` has
two documented failure modes of its own: recursive objects "may cause a recursive loop", and
"because deep copy copies everything it may copy too much, such as data which is intended to be
shared between copies". `copy` silently does *not* copy "module, method, stack trace, stack frame,
file, socket, window, or any similar types", and returns functions and classes unchanged — a copy
that appears to succeed may have shared exactly what you needed isolated. **VERSION-DEPENDENT
(3.13):** `copy.replace()` is the typed structural alternative for namedtuples, dataclasses and any
class defining `__replace__`.

**Why a competent agent produces it anyway.** There is no syntax for ownership. `list(xs)`, `xs[:]`,
`xs.copy()` and `dict(d)` all read as "make me a copy", and for a flat container of immutables they
*are* correct — which covers most cases an agent has seen. The failure surfaces one nesting level
down, in another function, later. And `deepcopy` is not the safe default: it is the other failure
mode, silently duplicating a shared cache the design intended to share.

| hazard | why it bites | route | exact mechanism | residual risk |
|---|---|---|---|---|
| Shallow/slice copy false confidence | nested objects stay aliased | contract-only | no rule verified. The constructs are `copy.deepcopy` and `copy.replace()` (**3.13**) | **test-catchable in practice: mutate the copy, assert the original is unchanged** — and only for paths a test exercises |
| `deepcopy` copying too much | "may copy … data which is intended to be shared between copies" | contract-only | documented; `__deepcopy__`/`__copy__` or an explicit constructor is the fix | the over-copy is silent and usually surfaces as a stale-cache or lost-identity bug |
| `deepcopy` on a recursive object | "may cause a recursive loop" | contract-only | documented | `RecursionError` if you are lucky; unbounded memory if the cycle is wide |
| Types `copy` silently does not copy | modules, methods, frames, files, sockets return as-is | contract-only | the documented list; functions and classes return unchanged | a "copied" object holding an open file shares the file. Prefer constructing a new value to copying one |
| `Mapping`/`Sequence` in a signature read as read-only | the annotation is a **static** promise; the object may be a `dict` | type-catchable (static only) | owned by `python_typing_contract_manifest.md` §6 | nothing at runtime prevents the callee casting and mutating |

---

## 6. Hazard class: iteration and ordering

**Mechanism.** **ESTABLISHED:** an exhausted iterator stays exhausted and **looks empty rather than
failing** — "any further calls to its `__next__()` method just raise `StopIteration` again … making
it appear like an empty container." **VERSION-DEPENDENT (3.7+):** `dict` insertion-order
preservation is a *language guarantee* — "declared to be an official part of the Python language
spec". **No equivalent guarantee exists for `set`** (ESTABLISHED by documented absence), and set
order interacts with hash randomization: it is on by default, "affects the `__hash__()` values of
str and bytes objects", values "remain constant within an individual Python process" but "are not
predictable between repeated invocations of Python"; `PYTHONHASHSEED=0` disables it. `zip()`
silently truncates to the shortest input unless `strict=` is passed. **VERSION-DEPENDENT (3.13+
free-threaded):** "free-threaded CPython does not guarantee thread-safe behavior of iterator
operations".

**Why a competent agent produces it anyway.** The generator/sequence distinction is invisible at the
call site: `for x in items:` compiles identically for a `list` and a `map` object, and the second
loop over an exhausted iterator does not raise — it runs zero times and every "no results" assertion
passes. Set-order dependence is worse: it is *stable within a process*, so it passes the developer's
run, passes CI on one runner, and fails months later on another. `zip(a, b)` is the obvious spelling
of "pair these up" and is correct whenever lengths match — exactly the case the tests cover.

| hazard | why it bites | route | exact mechanism | residual risk |
|---|---|---|---|---|
| Generator/iterator consumed twice, appearing empty | an exhausted iterator keeps raising `StopIteration`, so it reads as an empty container | type-catchable (at the boundary) | annotate the **contract**: `Sequence[T]`/`list[T]` where re-iteration is required, `Iterable[T]`/`Iterator[T]` only where single-pass is intended; a checker then rejects a second pass over an `Iterator` parameter | a function annotated `Iterable[T]` that iterates twice *internally* is still legal to the checker |
| `itertools.groupby` group reused after advancing | groups are shared iterators over one source | lint-catchable | ruff **B031** `reuse-of-groupby-generator` `[?]` | none material |
| `return <value>` inside a generator | unreachable to callers except via `StopIteration.value` | lint-catchable | ruff **B901** `return-in-generator` `[?]` | legitimate `yield from` delegation uses it deliberately |
| Mutating a container while iterating it | skipped elements, or `RuntimeError` | lint-catchable | ruff **B909** `loop-iterator-mutation` `[?]`; pylint **W4701** `modified-iterating-list` `[?]`, **E4702** `modified-iterating-dict` `[?]`, **E4703** `modified-iterating-set` `[?]` — note the categories: pylint classes the **dict and set** variants as *errors*, so `W4702`/`W4703` do not exist and naming them in `enable=`/`disable=` yields a `bad-option-value` and leaves the check unconfigured | aliased mutation through a second name is invisible to both |
| Depending on `set` iteration order | no language guarantee, and it interacts with hash randomization | test-catchable | run the suite under **varying `PYTHONHASHSEED`** (and once at `PYTHONHASHSEED=0` to reproduce); assert on `sorted(...)` or on sets, never on list order | a single-seed CI run hides the dependency indefinitely. Sweep wiring: `python_quality_gates_manifest.md` |
| Depending on `dict` order | **not** a hazard — a language guarantee from 3.7 | feature-eliminated | the 3.7 spec guarantee | `dict` only. `set`, and `**kwargs` built from a set, are different questions. VERSION-DEPENDENT (3.7) |
| `zip()` silently truncating | the shortest input wins, with no signal | lint-catchable | ruff **B905** `zip-without-explicit-strict` **`[off]`** (fix available), **B911** `batched-without-explicit-strict` `[?]`, **B912** `map-without-explicit-strict` `[?]` | `strict=True` converts a silent bug into a runtime `ValueError`, so it **must be a tested path** — never a bulk autofix. MEASURED: B905 is not default-on (0.16.2) |
| Iterator operations under free threading | no thread-safety guarantee for iterator operations | contract-only | documented; behaviour owned by `python_concurrency_determinism_manifest.md` | VERSION-DEPENDENT (3.13+ free-threaded builds) |

---

## 7. Hazard class: numeric, temporal and textual representation

**Mechanism — floats.** **ESTABLISHED:** `0.1` is not representable; the stored value is
`3602879701896397 / 2 ** 55`. **VERSION-DEPENDENT (3.1):** `repr()` prints the shortest
round-tripping form, which **hides** the discrepancy at the REPL. Float addition is not associative
in practice: `0.1` added ten times `== 1.0` is `False`, while `sum([0.1] * 10) == 1.0` is `True`
(extended precision), and `math.fsum()` "tracks all of the 'lost digits'". The documented comparison
tool is `math.isclose()`. `round()` is round-half-to-**even** — "both `round(0.5)` and `round(-0.5)`
are `0`, and `round(1.5)` is `2`" — and it compounds with binary representation: "`round(2.675, 2)`
gives `2.67` instead of the expected `2.68`. This is not a bug".

**Mechanism — decimals.** **ESTABLISHED:** `Decimal(0.1)` inherits the float's error exactly —
`Decimal('0.1000000000000000055511151231257827021181583404541015625')` — whereas `Decimal('0.1')` is
exact. The default context is `prec=28`, `ROUND_HALF_EVEN`, and "All traps are enabled (treated as
exceptions) except `Inexact`, `Rounded`, and `Subnormal`" — **silent rounding is the out-of-the-box
behaviour**. There is a runtime guard: "If the `FloatOperation` signal is trapped, accidental mixing
of decimals and floats in constructors or ordering comparisons raises an exception". And
`Decimal('NaN') == Decimal('NaN')` is `False`: equality with a quiet or signalling NaN "always
returns `False`".

**Mechanism — integers.** **VERSION-DEPENDENT (3.11):** `int`/`str` conversion in bases other than
2/4/8/16/32 is capped at a default **4300 digits**; exceeding it raises **`ValueError`**. The cap
mitigates CVE-2020-10735. Configurable via `sys.set_int_max_str_digits()`, `-X int_max_str_digits`
and `PYTHONINTMAXSTRDIGITS`; `sys.int_info.default_max_str_digits` and
`sys.int_info.str_digits_check_threshold` expose the default and the minimum settable non-zero
value.

**Why a competent agent produces it anyway.** `float` is the default literal type and every operator
accepts it, so choosing a numeric domain takes an act of will the syntax never prompts.
`Decimal(0.1)` looks like the careful choice — the agent reached for `Decimal` *because* it was
being careful, and passed in the one input that defeats it. `round` appears to be the rounding
function. And shortest-`repr` makes the interactive session actively reassuring.

### 7.1 Numeric-domain decision

| quantity | domain | why | the mechanical guard |
|---|---|---|---|
| Money; anything a human will audit or reconcile | `decimal.Decimal`, constructed from **`str` or `int` only** | exact decimal representation; rounding at a named point | trap `FloatOperation` in the context at process start; `quantize(..., rounding=ROUND_HALF_UP)` at each output boundary |
| Physical measurement, statistics, anything with instrument error | `float` | the error is already in the input; speed matters | `math.isclose()` in code, `pytest.approx` in tests. Never `==` |
| Exact ratios, unit-conversion factors | `fractions.Fraction` | no representation error at all | none needed; conversion out to `float`/`Decimal` is the boundary to guard |
| Counts, identifiers, indices | `int` | exactness is total; arbitrary precision | the 4300-digit `int`/`str` cap where values can be attacker-influenced |

**The rule no linter can apply for you:** deciding that a quantity is money is a domain judgement.
The three guards work only once a human has made it. OPEN — record it per quantity in the spec
(`software_spec_discipline_manifest.md` §G5).

### 7.2 Routing

| hazard | why it bites | route | exact mechanism | residual risk |
|---|---|---|---|---|
| Float `==` comparison | binary representation, and `repr` hides the error | contract-only + test-catchable | `math.isclose()` in code; `pytest.approx` in tests. **No ruff or pylint rule for float equality was verified** | reviewer discipline is the only pre-commit gate |
| `round()` half-to-even surprise | documented behaviour, not a bug | feature-eliminated (money domain) | `Decimal` + `quantize(..., rounding=ROUND_HALF_UP)` | choosing `decimal` is a design decision no linter makes |
| `Decimal(float)` inheriting float error | the float converts **losslessly**, i.e. exactly wrongly | runtime-catchable | trap `FloatOperation` in the decimal context | must be installed at process start, and **nothing enforces that it is**. Assert `FloatOperation in getcontext().traps` in a startup self-test |
| Silent decimal rounding | `Inexact`, `Rounded`, `Subnormal` untrapped by default | runtime-catchable | enable those traps explicitly in the `Context` | changes existing arithmetic; adopt at a boundary, not globally, in a live codebase |
| `NaN != NaN` | IEEE semantics: equality with a NaN operand is always `False` | lint-catchable | pylint **W0177** `nan-comparison` `[?]` | does not catch a NaN arriving from data at runtime |
| Huge `int(str)` / `str(int)` raising | the 4300-digit cap since 3.11 | test-catchable + runtime config | `ValueError`; `sys.set_int_max_str_digits()`, `-X int_max_str_digits`, `PYTHONINTMAXSTRDIGITS`; test the boundary | **raising the limit to accommodate real data re-opens the DoS the cap exists to prevent.** VERSION-DEPENDENT (3.11) |
| Naive `datetime` | local-vs-UTC ambiguity; `utcnow()` is a trap | lint-catchable | **all ten `DTZ` rules are `[on]`**, none with a fix: **DTZ001** `call-datetime-without-tzinfo`, **DTZ002** `call-datetime-today`, **DTZ003** `call-datetime-utcnow`, **DTZ004** `call-datetime-utcfromtimestamp`, **DTZ005** `call-datetime-now-without-tzinfo`, **DTZ006** `call-datetime-fromtimestamp`, **DTZ007** `call-datetime-strptime-without-zone`, **DTZ011** `call-date-today`, **DTZ012** `call-date-fromtimestamp`, **DTZ901** `datetime-min-max` | the rules catch **construction**, not later arithmetic between mismatched zones — that is test-catchable only. MEASURED (0.16.2) |
| A banned temporal API reached through an alias | one naive value poisons everything downstream | lint-catchable (project-specific) | ruff **TID251** `banned-api` `[?]` via `[lint.flake8-tidy-imports.banned-api]`, keyed on e.g. `"datetime.datetime.utcnow"` with a custom `msg` | matches fully-qualified paths only; an intermediate alias defeats it |
| `open()` without `encoding=` | platform-dependent decoding | lint-catchable | pylint **W1514** `unspecified-encoding` `[?]`; `-X dev` also checks `encoding`/`errors` arguments | binary-mode false positives |
| Integer floor-division semantics for negative operands | — | **OPEN — not verified** | the numeric-operations table in `library/stdtypes.html` was not loaded this session | **do not assert floor-toward-negative-infinity on the strength of this file.** Load the primary page first (see Open questions) |

---

## 8. Hazard class: exception mechanics

`error_tracing_contract_manifest.md` owns the *contract* (§8–§14, §22 there): propagation channels,
catch-narrowly, chaining, `from None`, `ExceptionGroup`/`except*`, `add_note`, EAFP/LBYL and the
full `assert` doctrine. This section carries only mechanics that **bite silently** and are not
stated there.

**Mechanism.** **ESTABLISHED:** handler search stops at the first match — "This search inspects the
`except` clauses in turn until one is found that matches the exception" — so a broad clause above a
narrow one makes the narrow one **dead code**. The `as` target is **deleted** at the end of the
clause: "When an exception has been assigned using `as target`, it is cleared at the end of the
`except` clause", implemented as an implicit `finally: del N`; reading the name afterwards raises
`NameError`/`UnboundLocalError`. `return`/`break`/`continue` in a `finally` clause silently destroys
the in-flight exception: "the saved exception is discarded." **VERSION-DEPENDENT (3.14):** the
compiler "emits a `SyntaxWarning` when a `return`, `break` or `continue` appears in a `finally`
block (see PEP 765)" — a *warning*, so the code still runs, and on <3.14 the warning does not exist
at all. **ESTABLISHED (labelled a CPython implementation detail):** an exception caught into a local
is a documented reference-cycle source — "The frame's locals then reference the exception, which
references its own traceback, which references the locals of all frames caught in the traceback."

**Why a competent agent produces it anyway.** Handler ordering is a *textual* property that reads
correctly in either order — nothing about `except Exception:` above `except ValueError:` looks
wrong, and both handlers are visibly present. The `as e` deletion is invisible because the variable
is right there and the failure is a `NameError` far from the cause. `return` in `finally` is the
natural way to say "whatever happened, return this", and it does exactly that — including swallowing
the exception you were not thinking about.

| hazard | why it bites | route | exact mechanism | residual risk |
|---|---|---|---|---|
| Broad `except` above a narrow one (dead handler) | the first matching clause wins | lint-catchable | pylint **E0701** `bad-except-order` `[?]`, **W0705** `duplicate-except` `[?]`; ruff **B014** `duplicate-handler-exception` `[?]` (fix), **B025** `duplicate-try-block-exception` `[?]`, **B030** `except-with-non-exception-classes` `[?]`, **B029** `except-with-empty-tuple` `[?]` | pylint's check works on the static class hierarchy; a dynamically built tuple of types is opaque |
| Bare `except:` / catching `BaseException` | catches `BaseException`, "which includes `KeyboardInterrupt`, `SystemExit`, and others" | lint-catchable | ruff **E722** `bare-except` `[on]`; ruff **BLE001** `blind-except` `[on]`; pylint **W0718** `broad-exception-caught` `[?]` (legacy **W0703**), **W0719** `broad-exception-raised` `[?]` | writing `except BaseException:` explicitly satisfies E722 while keeping the hazard. A broad catch that logs and re-raises is legitimate and will be flagged |
| Reading the `except … as e` name after the block | the target is deleted (`finally: del e`) | test-catchable | `NameError`/`UnboundLocalError`; pylint **E0601** `[?]` catches the common shape | assign to a separate name *inside* the handler; nothing forces you to |
| `return`/`break`/`continue` in `finally` | "the saved exception is discarded" | feature-eliminated (3.14) + lint-catchable | the 3.14 `SyntaxWarning` (PEP 765), escalated with `-W error::SyntaxWarning`; ruff **B012** `jump-statement-in-finally` `[?]`; pylint **W0150** `lost-exception` `[?]` | **on <3.14 the warning does not exist — the lint rule is the only gate**, and the 3.14 warning still permits the code. VERSION-DEPENDENT (3.14) |
| `try/except/pass` (swallow and continue) | the failure disappears with no trace | lint-catchable | ruff **S110** `try-except-pass` `[on]`, **S112** `try-except-continue` `[on]`; widen with `lint.flake8-bandit.check-typed-exception = true` | `except X: logger.debug(...)` passes both rules and is still effectively silent — contract-only beyond here. `contextlib.suppress` is the explicit, greppable form and is not flagged |
| Bare `raise` outside a handler | "will generate an error due to the lack of an active exception" | lint-catchable | ruff **PLE0704** `misplaced-bare-raise` `[?]`; pylint **E0704** `[?]` | none material |
| Broken exception chain on re-raise | the traceback loses the original cause | lint-catchable | ruff **B904** `raise-without-from-inside-except` **`[off]` — must be selected** | no autofix, and nothing detects a *wrong* `from` target. Contract owned by `error_tracing_contract_manifest.md` §8 |
| Exception caught into a local creating a reference cycle | frame → exception → traceback → frames | contract-only | documented CPython behaviour; `gc` collects the cycle later | the implicit `del` on the `as` target is the mitigation — do not defeat it by rebinding the exception to a longer-lived name |

---

## 9. Hazard class: module initialisation and module-level state

**Mechanism.** **ESTABLISHED:** `sys.modules` is consulted first and is authoritative; if the value
found is `None`, "a `ModuleNotFoundError` is raised". **ESTABLISHED and load-bearing:** a module is
registered **before** its body runs — "The module will exist in `sys.modules` before the loader
executes the module code. This is crucial because the module code may (directly or indirectly)
import itself; adding it to `sys.modules` beforehand prevents unbounded recursion." That single
design choice is *why* a circular import yields a **partially initialised module** rather than a
clean failure: the second importer gets a real module object holding only the names defined so far,
and fails later with `AttributeError` or `ImportError` at a site unrelated to the cycle. Importing a
submodule binds it as an attribute of the parent package, so `import spam` can expose `spam.foo` as
a side effect of some other module's import; `__init__.py` "is implicitly executed" on package
import, transitively. **ESTABLISHED:** a module *is* the language's singleton — "using a module is
also the basis for implementing the singleton design pattern, for the same reason" — so module-level
mutable state is process-global state with no owner and no lifecycle.

**Why a competent agent produces it anyway.** Import-time side effects are how the ecosystem's most
visible libraries work: registries populated by decorators, loggers configured at module scope,
`Enum`s and compiled regexes built at the top of a file. Good and bad cases are syntactically
identical — `_CACHE: dict[str, int] = {}` at module level is either a benign memo or unownable
global state, and only intent distinguishes them. Cycles arise from a reasonable desire for
bidirectional type references, and `if TYPE_CHECKING:` fixes the annotation half so convincingly
that the remaining runtime half looks safe.

| hazard | why it bites | route | exact mechanism | residual risk |
|---|---|---|---|---|
| Import-time side effects | transitive `__init__.py` execution; cost and ordering coupling | fitness-function | `-X importtime` / `-X importtime=2` in CI with a budget assertion (module name, cumulative and self time; `=2` marks cached modules); pylint **C0415** `import-outside-toplevel` `[?]` governs the inverse | it measures **cost and ordering, not purity** — "no side effects at import" stays contract-only. The docs warn `-X importtime` output "may be broken in multi-threaded application" |
| Circular import / partially initialised module | the module enters `sys.modules` before its body runs | fitness-function | Import Linter **2.13** contracts `type = layers`, `type = independence`, `type = forbidden` in CI; pylint **R0401** `cyclic-import` `[?]` detects the cycle itself | detects the *dependency* that permits the cycle; the runtime `ImportError`/`AttributeError` is the last line of defence. Enforcement owned by `python_module_boundaries_manifest.md`. VERSION-DEPENDENT (2.13) |
| Module-level mutable state; module-as-accidental-singleton | one module object per process, no lifecycle, no owner | **contract-only** | the FAQ names it explicitly. ruff **PLW0603** `global-statement` `[?]` and pylint **W0603** `[?]` / **W0602** `global-variable-not-assigned` `[?]` cover **only the `global` keyword**, not mutation of an already-module-level container | **the highest-value contract-only row in the file.** State it; do not pretend a linter covers it. The construct that removes it: pass state as a parameter, or own it in an object the shell constructs |
| A submodule appearing as a parent attribute | `import spam` can expose `spam.foo` because another module imported it | contract-only | documented import semantics | code reading `spam.foo` works until the unrelated import that created the binding is removed |
| `sys.modules[name] = None` | forces `ModuleNotFoundError` | contract-only | documented | only bites codebases that manipulate `sys.modules` — that manipulation is itself the thing to prohibit |

---

## 10. Hazard class: static invisibility (dynamic access and stale suppressions)

**Mechanism.** **ESTABLISHED:** `__getattribute__` "is called unconditionally for every attribute
access"; `__getattr__` is called only when default lookup fails with `AttributeError`. Anything
reachable *only* through those hooks is invisible to a static checker unless a stub declares it —
unverifiable **by construction**, not merely unverified. **VERSION-DEPENDENT (3.12):** two changes
moved runtime-checkable protocols under the same theme — `isinstance()` now uses
`inspect.getattr_static()` rather than `hasattr()`, so "some objects which used to be considered
instances of a runtime-checkable protocol may no longer be considered instances … and vice versa";
and protocol members are frozen at class creation, so "Monkey-patching attributes onto a
runtime-checkable protocol will still work, but will have no impact on `isinstance()` checks".
**VERSION-DEPENDENT (3.14):** PEP 649/749 deferred annotation evaluation is now the **default**,
with `annotationlib` (`VALUE`/`FORWARDREF`/`STRING` formats) — an annotation that previously raised
at import time now raises when something introspects it, and code reading `__annotations__` directly
should move to `annotationlib.get_annotations(...)` with an explicit `Format`.

**Why a competent agent produces it anyway.** `__getattr__` forwarding is the shortest way to write
a proxy, a lazy loader or a config object, and it produces beautifully small code.
`setattr(obj, name, v)` with a constant name is what an agent writes while generalising a loop, and
it works. A blanket `# type: ignore` is the fastest way to make a build green under deadline and is
indistinguishable in the diff from a targeted one. Stale suppressions accumulate because removing
one requires proving a negative.

| hazard | why it bites | route | exact mechanism | residual risk |
|---|---|---|---|---|
| `getattr`/`setattr`/`delattr` with a **constant** string | needlessly dynamic; invisible to checkers | lint-catchable | ruff **B009** `get-attr-with-constant` `[?]` (fix), **B010** `set-attr-with-constant` `[?]` (fix), **B043** `del-attr-with-constant` `[?]` (fix) | **names built at runtime are the real hazard and are not covered** |
| `__getattr__`/`__setattr__`/monkeypatching defeating static checks | attribute access is satisfied at runtime by a hook | **contract-only** (+ partial lint) | pylint **E1101** `no-member` `[?]` catches missing members on *statically known* classes. The construct: declare the surface with a `Protocol`, explicit attributes, or a stub — never a hook | anything reachable only through `__getattr__` is unchecked **by construction**. A design prohibition, not a lint |
| Attribute created outside `__init__` | the object's shape varies by code path | lint + type-catchable | pylint **W0201** `attribute-defined-outside-init` `[?]`; pyright `reportUninitializedInstanceVariable` (**`"none"` in every mode — enable by hand**) | teams assume strict covers it; it does not (§1.3) |
| Monkeypatching leaking between tests | global state mutated for the whole process | test-catchable | the pytest `monkeypatch` fixture, which undoes at teardown | a hand-rolled `setattr` in a test body does not undo. Owned by `python_testing_tooling_manifest.md` |
| Monkeypatching a `runtime_checkable` Protocol | members are frozen at class creation from 3.12 | contract-only | documented: the patch "will have no impact on `isinstance()` checks" | silently ineffective — the patch appears to work and the check does not see it. VERSION-DEPENDENT (3.12) |
| Blanket `# type: ignore` | hides an unknown class of error, present and future | type + lint-catchable | mypy `--enable-error-code=ignore-without-code` (checker-aware, **not** in `--strict`); ruff **PGH003** `blanket-type-ignore` **`[off]`** (textual) | forces a code onto the ignore; does not reduce their number. **pyright has no equivalent requirement** |
| Blanket `# noqa` | suppresses every present and future diagnostic on that line | lint-catchable | ruff **PGH004** `blanket-noqa` **`[off]`** (fix Sometimes) | fixing it surfaces new diagnostics, which is the point |
| Stale suppressions accumulating | suppression debt becomes permanent and invisible | lint + type-catchable | ruff **RUF100** `unused-noqa` `[on]` (fix Always), distinguishing `(unused: X)` from `(non-enabled: X)`; **RUF101** `redirected-noqa` `[on]`; **RUF102** `invalid-rule-code` `[off]` with `lint.external`; mypy `--warn-unused-ignores` (inside `--strict`); pylint **I0021** `useless-suppression` (**disabled by default**, `--fail-on=I0021`) | pyright's `reportUnnecessaryTypeIgnoreComment` is `"none"` in **all four** modes. `RUF100` cannot judge a code you never enabled — `non-enabled` is a config smell, `unused` is dead debt |
| Unreachable / always-true branch (a dead guard that looks protective) | narrowing already proved it cannot happen | type-catchable | mypy `--warn-unreachable` (code `unreachable`), `--enable-error-code=redundant-expr`; pyright `reportUnnecessaryComparison`/`reportUnnecessaryIsInstance`/`reportUnnecessaryContains` (**error in strict only**) | checkers disagree on which branch is dead, because their narrowing differs |
| Calling a deprecated API | removal breaks you later, silently until then | type-catchable | mypy `--enable-error-code=deprecated` (reads PEP 702 `warnings.deprecated`); at runtime `-W error::DeprecationWarning` or pytest `filterwarnings = error` | only as good as the library's deprecation markers |
| Reading `__annotations__` directly on 3.14 | annotations are lazily-evaluated `__annotate__` entries; errors move to first use | contract-only | `annotationlib.get_annotations(obj, format=...)` with an explicit `Format`. Owned by `python_typing_contract_manifest.md` | VERSION-DEPENDENT (3.14) |

---

## 11. Hazard class: object lifetime and resource release

**Mechanism.** **ESTABLISHED:** `__del__` is not a cleanup contract. "It is not guaranteed that
`__del__()` methods are called for objects that still exist when the interpreter exits"; exceptions
inside it "are ignored, and a warning is printed to `sys.stderr`"; during shutdown "the global
variables it needs to access (including other modules) may already have been deleted or set to
`None`". The docs point at `weakref.finalize`. `with` is the only structural guarantee: "The `with`
statement guarantees that if the `__enter__()` method returns without an error, then `__exit__()`
will always be called." A `@contextmanager` generator without `try`/`finally` skips its own cleanup
on exception, because the exception "is reraised inside the generator at the point where the yield
occurred"; and a generator that traps without re-raising silently **suppresses** the exception —
"the generator context manager will indicate to the `with` statement that the exception has been
handled". Context managers are not uniformly reusable: "Most context managers … can only be used
effectively in a `with` statement once", and reusable-but-not-reentrant managers "will fail … if the
specific context manager instance has already been used in a containing with statement"
(`threading.Lock`, `ExitStack`). `functools.lru_cache`/`cache` on a method leaks instances — "the
global cache will retain a reference to the instance, preventing it from being garbage collected".

**ESTABLISHED:** Python Development Mode (`-X dev` / `PYTHONDEVMODE=1`) equals
`PYTHONMALLOC=debug PYTHONASYNCIODEBUG=1 python -W default -X faulthandler`; it surfaces
`ResourceWarning` (plus `DeprecationWarning`, `ImportWarning`, `PendingDeprecationWarning`), enables
faulthandler, logs `io.IOBase` destructor `close()` exceptions, and checks `encoding`/`errors`
arguments. **It is the mechanism that turns a leak into a failure, and it needs both `-X dev` and
`filterwarnings = error`:** without development mode `ResourceWarning` is filtered by default, so
`filterwarnings = error` alone does not surface unclosed files.

**Why a competent agent produces it anyway.** `__del__` is spelled like a destructor in every other
language, and it *usually* runs — reference counting fires it promptly in the common case, so the
bug is a tail event at shutdown or inside a cycle. A `@contextmanager` without `try`/`finally` reads
correctly top-to-bottom and works on every happy path. `@lru_cache` on a method is the obvious
memoisation, and the leak is invisible until something profiles retained memory.

| hazard | why it bites | route | exact mechanism | residual risk |
|---|---|---|---|---|
| Relying on `__del__` for cleanup | not guaranteed to be called; exceptions inside it are ignored; shutdown globals may be `None` | feature-eliminated + test-catchable | `with` (guaranteed `__exit__`), `contextlib.closing`/`ExitStack`, `weakref.finalize`; pylint **R1732** `consider-using-with` `[?]`; detect leaks with **`-X dev` + pytest `filterwarnings = error`** turning `ResourceWarning` into a failure | `-X dev` must actually be on in CI; a leak with no `ResourceWarning` implementation stays invisible |
| `@contextmanager` generator without `try`/`finally` | cleanup is skipped when the body raises | lint-catchable | pylint **W0135** `contextmanager-generator-missing-cleanup` `[?]` | a generator that catches and does **not** re-raise silently *suppresses* the exception — no verified rule covers that |
| Reusing a single-use context manager instance | "will fail … if the specific context manager instance has already been used" | contract-only | documented in `contextlib`; no rule verified | test-catchable only if the second use is exercised. `ExitStack` and `threading.Lock` are the named cases |
| `lru_cache`/`cache` on a method | the global cache pins `self` for the process lifetime | lint-catchable | ruff **B019** `cached-instance-method` `[?]` | `functools.cached_property` and an explicit per-instance cache are the alternatives |
| `NamedTemporaryFile(delete=True, delete_on_close=False)` | deletion falls back to finalisation | contract-only | the docs say so: "Deletion is not always guaranteed in this case (see `object.__del__()`)" | use `delete=False` plus explicit removal, or `delete_on_close=True`. VERSION-DEPENDENT (`delete_on_close` added 3.12) |

---

## 12. Hazard class: records, immutability and subclassing

`python_typing_contract_manifest.md` §5–§6 owns `frozen=True` shallowness, the `object.__setattr__`
bypass, `Final` being checker-only, `Mapping` vs `MutableMapping` as a static-only promise, and the
statement that "It is not possible to create truly immutable Python objects." This section carries
only the derived-behaviour hazards not stated there.

**Mechanism.** **ESTABLISHED:** hashability is **derived, not chosen** — "If *eq* and *frozen* are
both true, by default `@dataclass` will generate a `__hash__()` method for you. If *eq* is true and
*frozen* is false, `__hash__()` will be set to `None`, marking it unhashable… If *eq* is false,
`__hash__()` will be left untouched meaning the `__hash__()` method of the superclass will be used"
— and for `object` that means **id-based hashing** on what the author intended as a value object.
`unsafe_hash=True` plus an explicit `__hash__` raises `TypeError`; defining
`__setattr__`/`__delattr__` on a class also decorated `frozen=True` raises `TypeError`; `order=True`
with `eq=False` raises `ValueError`; `order=True` over a class already defining any of
`__lt__`/`__le__`/`__gt__`/`__ge__` raises `TypeError`. `__post_init__` is called *by the generated
`__init__`*, so "If no `__init__()` method is generated, then `__post_init__()` will not
automatically be called" — a dataclass declared `init=False` and built by a factory silently skips
every validation placed there. Under `frozen=True` the generated `__init__` "cannot use simple
assignment … and must use `object.__setattr__()`", which is exactly what user code must do to set
derived fields: **the bypass is the documented implementation, not an exotic trick.** A non-default
field after a defaulted one raises `TypeError`, "whether this occurs in a single class, or as a
result of class inheritance" — so adding a defaulted field to a base class can break subclasses you
do not own.

**A cross-pack resolution recorded here.** That frozen-ness cannot be mixed across a dataclass
hierarchy was FLAGGED-SECONDARY in one source (the prose docs are silent). It is confirmed in
**CPython 3.14's `Lib/dataclasses.py`**, which raises `TypeError` with exactly these strings:
"cannot inherit non-frozen dataclass from a frozen one" and "cannot inherit frozen dataclass from a
non-frozen one". Promoted to **ESTABLISHED (source-verified; prose docs silent)**.

**Version gates.** **VERSION-DEPENDENT (3.13):** generated `__eq__` "compares each field
individually (e.g., `self.a == other.a and self.b == other.b`)", where "In Python 3.12 and earlier,
the comparison was performed by creating tuples of the fields" — changing behaviour around
`NotImplemented` for non-identical types across that boundary. **VERSION-DEPENDENT (3.10/3.11):**
`slots=True` and `kw_only=True` arrived in 3.10; from 3.11 a slot already present in a base
`__slots__` is omitted from the generated one. **VERSION-DEPENDENT (3.14):** `dataclasses` now reads
annotations via `annotationlib.get_annotations(cls, format=annotationlib.Format.FORWARDREF)`, so a
field annotated with an **undefined** name is accepted at class creation and its annotation is a
`ForwardRef`, not a type — the failure moves to whoever later resolves it. `ClassVar` detection
retains a documented textual blind spot for aliases bound inside the class body; the module's own
comment calls it a "fairly obscure corner case" whose fix "would involve a eval() penalty for every
single field of every dataclass that's defined. It was judged not worth it."

**Why a competent agent produces it anyway.** `eq=False` is a plausible micro-optimisation with no
visible consequence at the definition site — the class still works, dict membership still "works",
and it now compares by identity. `init=False` is reasonable for a factory-constructed record, and
nothing marks `__post_init__` as dead. And `@dataclass(frozen=True)` holding a `list` is the single
most common false confidence in typed Python: the annotation says the field cannot be *rebound*, and
the agent reads that as the value being immutable.

| hazard | why it bites | route | exact mechanism | residual risk |
|---|---|---|---|---|
| `eq=False` silently restoring id-based hashing | with `eq` false, `__hash__` is left untouched and falls back to `object`'s | contract-only | the docs' truth table; **no rule verified** | adding `eq=False` "for performance" converts value equality into identity equality for dict/set membership **with no diagnostic** |
| `eq=True, frozen=False` making the class unhashable | `__hash__` is set to `None` | test-catchable | `TypeError: unhashable type` at first use as a key | fails loudly, but only on a path a test reaches |
| Frozen dataclass treated as deeply immutable | freeze is shallow and bypassable; `object.__setattr__` is the generated `__init__`'s own mechanism | contract-only | owned by `python_typing_contract_manifest.md` §6. Only `tuple`, `frozenset`, `str`, `bytes` and numbers are genuinely immutable — and a `tuple` may hold mutable elements | see §15: a silently-ineffective construct, not a boundary |
| `init=False` skipping `__post_init__` | `__post_init__` is invoked by the *generated* `__init__` | contract-only | documented; no rule verified | every validation placed in `__post_init__` silently does not run |
| Mixing frozen and non-frozen in one hierarchy | `TypeError` at class creation | feature-eliminated | CPython raises `TypeError` with the two exact messages above | none — a hard failure at import. Common when wrapping a third-party frozen dataclass |
| Non-default field after a defaulted one, via inheritance | `TypeError` "whether this occurs in a single class, or as a result of class inheritance" | feature-eliminated | `TypeError` at class creation | adding a defaulted field to a base class breaks subclasses you do not own |
| Mutable attribute narrowed in an override | the subtype breaks the base contract | type-catchable | mypy `--enable-error-code=mutable-override` | opt-in |
| Override without `@override` | a silent typo creates a **new** method instead of overriding | type-catchable | mypy `--enable-error-code=explicit-override` (PEP 698); pyright `reportImplicitOverride` (**`"none"` in every mode**) | both opt-in; **pyright strict does not cover it** |
| Undefined field annotation accepted at class creation on 3.14 | `dataclasses` reads `Format.FORWARDREF` | contract-only | documented in the 3.14 source and porting notes | the failure surfaces in a validator or schema generator, far from the definition. VERSION-DEPENDENT (3.14) |

---

## 13. Hazard class: security-adjacent constructs

Read the default-status pattern first: **only `S102` is default-on among the codes in this table**
(`S110` and `S112` from §8 are the other two of ruff's three default-on `S` rules). Every other `S`
code below is `[off]`. MEASURED (0.16.2). A project that never selected `S` has **no** mechanical
check on `pickle`, `eval`, `shell=True`, `yaml.load`, `mktemp`, weak hashes or
`random`-for-security.

**The mechanisms, verbatim, all ESTABLISHED.** `eval()` and `exec()` carry the identical warning:
"This function executes arbitrary code. Calling it with untrusted user-supplied input will lead to
security vulnerabilities." `pickle` "is not secure": "It is possible to construct malicious pickle
data which will execute arbitrary code during unpickling" — the docs recommend `hmac` signing for
tamper-evidence and `json` for untrusted data. `subprocess` does **not** use a shell unless asked —
"this library will not implicitly choose to call a system shell … all characters, including shell
metacharacters, can safely be passed to child processes" — but with `shell=True` "it is the
application's responsibility to ensure that all whitespace and metacharacters are quoted
appropriately", optionally via `shlex.quote()`. **Windows inverts the advice for batch files:**
`*.bat`/`*.cmd` "may be launched by the operating system in a system shell regardless of the
arguments passed to this library … consider passing `shell=True` to allow Python to escape special
characters". `subprocess.run` does **not** raise on a non-zero exit unless `check=True`.
`tempfile.mktemp()` is deprecated since 2.3 and is a documented TOCTOU hole: "By the time you get
around to doing anything with the file name it returns, someone else may have beaten you to the
punch." PyYAML's own wiki says `load` "has been unsafe since the first release in May 2006"; the
loader taxonomy is `BaseLoader` / `SafeLoader` (recommended for untrusted input) / `FullLoader` /
`UnsafeLoader` (alias `Loader`).

**Audit hooks are telemetry, not a sandbox, and the docs say so:** "They are not suitable for
implementing a 'sandbox'. In particular, malicious code can trivially disable or bypass hooks added
using this function." Security-sensitive hooks "must be added using the C API `PySys_AddAuditHook()`
before initialising the runtime". And `sys.addaudithook` **can fail silently**: "If any existing
hook raises an exception derived from `RuntimeError`, the new hook will not be added and the
exception is suppressed" — so "auditing is enabled" is not assertable from Python. VERSION-DEPENDENT
(3.8+). **VERSION-DEPENDENT (3.14):** `sys.remote_exec()` (PEP 768) adds a new in-process execution
surface, gated by `PYTHON_DISABLE_REMOTE_DEBUG`, `-X disable-remote-debug` and
`--without-remote-debug`; its diagnostic use is owned by `python_runtime_diagnostics_manifest.md`,
the attack-surface fact is here.

**Why a competent agent produces it anyway.** `pickle` is the stdlib's own answer to "serialise this
object" and handles graphs `json` refuses. `shell=True` is what makes a copied one-liner work, and a
pipe or glob genuinely requires a shell. `yaml.load(f)` is the first example in most tutorials, and
`Loader=yaml.FullLoader` circulated widely as *the* fix — it satisfies the complaint about a missing
loader without satisfying the threat model. `mktemp()` returns a string, which composes with every
path API, where `mkstemp()` returns a descriptor the surrounding code must be restructured to use.

| hazard | why it bites | route | exact mechanism | residual risk |
|---|---|---|---|---|
| `eval` / `exec` | "executes arbitrary code" | lint-catchable | ruff **S307** `suspicious-eval-usage` `[off]`, **S102** `exec-builtin` **`[on]`**; pylint **W0123** `eval-used` `[?]`, **W0122** `exec-used` `[?]` | `__import__`, `compile` and `getattr`-driven dispatch reach similar power and are **not all covered** |
| `pickle` on untrusted data | arbitrary code execution during unpickling | lint-catchable | ruff **S301** `suspicious-pickle-usage` `[off]`, **S403** `suspicious-pickle-import` `[off]`, **S302** `suspicious-marshal-usage` `[off]` | the rule cannot know whether the input is trusted — **the boundary decision is yours**. Protocol 5 as the 3.14 default changes nothing about safety |
| `subprocess(..., shell=True)` | shell metacharacter injection | lint-catchable | ruff **S602** `subprocess-popen-with-shell-equals-true` `[off]`, **S604** `call-with-shell-equals-true` `[off]`, **S605** `start-process-with-a-shell` `[off]`, **S606** `start-process-with-no-shell` `[off]`, **S607** `start-process-with-partial-path` `[off]`, **S609** `unix-command-wildcard-injection` `[off]`; **S603** `subprocess-without-shell-equals-true` `[off]` covers the residue | **Windows `.bat`/`.cmd` inverts the advice** — the docs recommend `shell=True` there so Python performs the escaping, so a cross-platform codebase needs a platform branch and the lint rule will flag the correct one |
| `subprocess.run` without `check=` | a non-zero exit is silently ignored | lint-catchable | pylint **W1510** `subprocess-run-check` `[?]` | none material |
| `tempfile.mktemp()` / hard-coded `/tmp` paths | TOCTOU between name generation and use | lint-catchable | ruff **S306** `suspicious-mktemp-usage` `[off]`, **S108** `hardcoded-temp-file` `[off]` | replacement is `mkstemp()` or `NamedTemporaryFile(delete=False)`; see §11 for the `delete_on_close` caveat |
| `yaml.load` | arbitrary object construction, therefore arbitrary code | lint-catchable | ruff **S506** `unsafe-yaml-load` `[off]` | **`Loader=yaml.FullLoader` is not the safe loader.** S506 flags `yaml.load` regardless of loader, so silencing it with `FullLoader` satisfies the linter and not the threat model. Only `safe_load`/`SafeLoader` is right for untrusted input |
| Insecure hash / weak randomness for a security purpose | the wrong primitive for the job | lint-catchable | ruff **S324** `hashlib-insecure-hash-function` `[off]`, **S303** `suspicious-insecure-hash-usage` `[off]`, **S311** `suspicious-non-cryptographic-random-usage` `[off]` | flags the *call*, not the purpose — non-security uses of `random` are false positives needing a scoped exemption, not a global disable |
| Treating audit hooks as a sandbox | "malicious code can trivially disable or bypass hooks" | **contract-only** | the docs state the limit; C-API `PySys_AddAuditHook()` before runtime init is the only stronger form | **do not build a security boundary on Python-level hooks**, and do not assert that auditing is on |
| `sys.remote_exec()` as an unmanaged surface | a new in-process execution path in 3.14 | runtime-catchable | disable with `PYTHON_DISABLE_REMOTE_DEBUG`, `-X disable-remote-debug`, or build `--without-remote-debug` | VERSION-DEPENDENT (3.14). Decide the posture per deployment; the default is enabled |

---

## 14. Hazard class: concurrency assumptions visible from single-threaded code

Execution models, structured concurrency, cancellation and determinism under test are owned by
`python_concurrency_determinism_manifest.md`. This section carries only what a
**single-threaded-looking** file can encode wrongly.

**Mechanism.** **ESTABLISHED:** the GIL guarantees only bytecode-level atomicity — "Python offers to
switch among threads only between bytecode instructions … Each bytecode instruction and therefore
all the C implementation code reached from each instruction is therefore atomic from the point of
view of a Python program." The docs enumerate what is atomic (`L.append(x)`, `L1.extend(L2)`,
`x = L[i]`, `x = L.pop()`, `L1[i:j] = L2`, `L.sort()`, `x = y`, `x.field = y`, `D[x] = y`,
`D1.update(D2)`, `D.keys()`) and what is **not** (`i = i+1`, `L.append(L[-1])`, `L[i] = L[j]`,
`D[x] = D[x] + 1`), closing with "When in doubt, use a mutex!" Even the atomic list is conditional:
"Operations that replace other objects may invoke those other objects' `__del__()` method when their
reference count reaches zero, and that can affect things." **VERSION-DEPENDENT (3.14):** free
threading is officially supported (PEP 779, implementing PEP 703) with a stated "~5-10%"
single-threaded penalty — which **invalidates informal reasoning built on the GIL** rather than
merely relaxing it.

**ESTABLISHED:** signal handlers run in exactly one place — "always executed in the main Python
thread of the main interpreter, even if the signal was received in another thread" — and only that
thread may install them (`ValueError` otherwise). Execution is **deferred**: "the low-level signal
handler sets a flag which tells the virtual machine to execute the corresponding Python signal
handler at a later point (for example, at the next bytecode instruction)", so "A long-running
calculation implemented purely in C … may run uninterrupted for an arbitrary amount of time,
regardless of any signals received". Therefore `KeyboardInterrupt` can land anywhere: it "may appear
at any point during execution. Most Python code, including the standard library, cannot be made
robust against this" — and the docs name the exact hole: "a context manager's `__exit__` method may
not be called if `KeyboardInterrupt` occurs between `__enter__` and the return statement". Also
`threading.Lock` "should not be used within signal handlers. Doing so can lead to unexpected
deadlocks." **VERSION-DEPENDENT (3.11):** `asyncio.create_task` results must be retained — "The
event loop only keeps weak references to tasks. A task that isn't referenced elsewhere may get
garbage collected at any time, even before it's done"; `TaskGroup` is the documented fix because it
"keeps strong references to each task".

**Why a competent agent produces it anyway.** "The GIL makes it safe" is the most widely transmitted
piece of Python folklore and it is *almost* true — `list.append` really is atomic, so the mental
model gets reinforced until it meets `D[x] = D[x] + 1`. `create_task(coro())` without keeping the
handle is what "fire and forget" means in every other async ecosystem, and the task usually
completes before collection, so the bug is load-dependent.

| hazard | why it bites | route | exact mechanism | residual risk |
|---|---|---|---|---|
| Drawing atomicity from the GIL | only bytecode boundaries are atomic; `i = i+1` is not | **contract-only** | the FAQ's explicit atomic/non-atomic lists and "When in doubt, use a mutex!" | **free threading (3.14) invalidates informal GIL reasoning**, and no rule detects a reliance on it |
| Signal-handler assumptions; `KeyboardInterrupt` anywhere | handlers run only in the main thread, deferred to a bytecode boundary; `__exit__` may not run if the interrupt lands between `__enter__` and the return | **contract-only** | documented. Install an explicit `SIGINT` handler for graceful shutdown rather than relying on `KeyboardInterrupt` | untestable in practice; **CPython declares this out of reach** — a genuine residual risk to state, not to hide |
| `threading.Lock` inside a signal handler | documented deadlock source | contract-only | documented | no rule verified |
| `asyncio.create_task` result discarded | the event loop holds only weak references | lint-catchable + feature-eliminated | ruff **RUF006** `asyncio-dangling-task` `[?]`; **`asyncio.TaskGroup`** (3.11) keeps strong references and aggregates failures | RUF006's "stored in a variable" heuristic can be satisfied without keeping the reference *alive*. VERSION-DEPENDENT (3.11) |

---

## 15. Silently-ineffective constructs

**The highest-value section in this file.** Each item *looks* like it enforces something and
enforces nothing. No error, no warning, no failing test — the code reads as a guard and behaves as a
no-op. An agent reviewing a diff will approve every one of them.

| construct | what it looks like | what actually happens | caught by |
|---|---|---|---|
| `assert (cond, "msg")` — the stray-comma tuple | an assertion with a message | **always passes.** "Non-empty tuples are always `True`, so an `assert` statement with a non-empty tuple as its test condition will always pass" | ruff **F631** `assert-tuple` `[on]`\*; pylint **W0199** `assert-on-tuple` `[?]`, whose documented fix is to unpack and assert separately. **A clean catch — and nothing else finds it; the suite stays green** |
| `assert` enforcing anything, under `-O` | a runtime invariant check | **removed entirely.** `-O` will "Remove assert statements *and any code conditional on the value of `__debug__`*"; `-OO` also discards docstrings; `PYTHONOPTIMIZE` is equivalent | ruff **S101** `assert` **`[off]`**. Doctrine owned by `error_tracing_contract_manifest.md` §14. Backstop: refuse to start when `sys.flags.optimize` is non-zero |
| A walrus inside an `assert` | a binding plus a check | **the binding vanishes with the assert** under `-O`: "the named assignment will also be ignored, which may result in unexpected behavior (e.g., undefined variable accesses)" — a latent `NameError` in an optimised deployment | ruff **RUF018** `assignment-in-assert` `[?]` |
| Any side-effecting expression inside an `assert` | a check that also does the work | the work does not happen under `-O` | nothing beyond `S101`/`RUF018`. **Contract: an `assert` expression must be pure** |
| `zip(a, b)` without `strict=` | pairing two sequences | **silently truncates to the shorter.** A length mismatch — the bug you would want to hear about — produces a shorter result and no signal | ruff **B905** **`[off]`** (fix available); **B911** `[?]`; **B912** `[?]`. Adding `strict=True` is a **behaviour change** and must land with a test for the mismatch path |
| `case SOME_CONSTANT:` in a `match` | a comparison against a constant | **a capture pattern that always matches and rebinds the name.** "Capture patterns always succeed … `NAME` will always succeed and it will set `NAME = <subject>`." Only a **dotted** value pattern compares: the dotted name "is looked up using standard Python name resolution rules. The pattern succeeds if the value found compares equal to the subject value" | **partially.** "A match statement may have at most one irrefutable case block, and it must be last", so the compiler objects *only when other cases follow*. **As the final case it is legal and silently swallows every subject.** Rule: value patterns are always dotted — `Color.RED`, never `RED`. VERSION-DEPENDENT (3.10) |
| A `match` over a closed domain with no fallthrough assertion | exhaustive dispatch | a new variant is silently unhandled | mypy `--enable-error-code=exhaustive-match` **plus** `typing.assert_never` in the fallthrough. Requires the domain to be closed (`Enum`/`Literal`/discriminated union) first |
| An `Enum` with duplicated values and no `@enum.unique` | a set of distinct members | **the duplicate silently becomes an alias** of the first | `@enum.unique` raises "`ValueError` … with the details"; `@enum.verify(EnumCheck.UNIQUE)` (also `CONTINUOUS`, `NAMED_FLAGS`). **Nothing forces the decorator onto a class.** VERSION-DEPENDENT (`verify`: 3.11) |
| A class pattern with positional sub-patterns on an ad-hoc class | destructuring by position | depends on `__match_args__`, obtained as `getattr(cls, "__match_args__", ())`. Dataclasses supply it; ad-hoc classes do not, and `kw_only` fields "are not included in `__match_args__`" | `TypeError` at match time — loud, but only on the path that reaches it |
| `@dataclass(frozen=True)` wrapping a `list` | an immutable record | **the field cannot be rebound; the list can be mutated freely.** `frozen` is emulation: the generated `__init__` itself uses `object.__setattr__`, which is also the bypass | nothing. Owned by `python_typing_contract_manifest.md` §6. **Only `tuple`, `frozenset`, `str`, `bytes` and numbers are genuinely immutable — and a `tuple` may hold mutable elements** |
| `Final`, `@final`, `Protocol`, `cast`, `NewType` at runtime | enforced declarations | **checker-only.** Owned by `python_typing_contract_manifest.md` §3, §6 | the type checker, and nothing else. Listed so the hazard set is complete |
| `sys.addaudithook()` as a sandbox, or as confirmed | a security boundary | "malicious code can trivially disable or bypass hooks", **and the call can fail silently** if an existing hook raises a `RuntimeError` subclass | nothing (§13) |
| A preview-gated ruff rule pulled in by **prefix** with preview off | an enforced rule | **the rule never runs, and there is no diagnostic.** Naming the *exact* code instead is not silent — ruff prints ``warning: Selection `X` has no effect because preview is not enabled.`` — but a warning in a CI log is not a failure. Prefix selection, and `ALL`, produce nothing at all | nothing in ruff for the prefix case. `--show-settings` is the only way to see the resolved set. MEASURED (0.16.2) |

\* `F631`'s `[on]` status is derived, not individually measured — see the §4 footnote.

**One belief this table used to hold, and measurement removed.** A *removed* ruff rule code in
`select` is **not** silently inert. `TRY200`, `PGH001` and `PGH002` are **redirects**: ruff prints
``warning: `TRY200` has been remapped to `B904`.`` *and enables the successor rule*
(`TRY200`→`B904`,
`PGH001`→`S307`, `PGH002`→`G010`), so the config is neither silent nor inert — it enforces something
other than what it says. `PT004` was removed outright and ruff **refuses to run at all**:
``ruff failed / Cause: Rule `PT004` was removed and cannot be selected.`` Both outcomes are loud;
the
residual hazard is only that a redirect's warning is easy to scroll past while the successor rule
quietly changes what the build enforces. Treat a remap warning as a config defect to fix, not as
noise. MEASURED (0.16.2).

---

## 16. Rules that fight each other

### 16.1 `B023` (late-binding closures) versus `B006` (mutable defaults) — the real one

**The conflict.** The documented remedy for late binding is a default-argument capture
(`lambda n=x: n**2`), which "creates a new variable `n` local to the lambda and computed when the
lambda is defined". That is *precisely* the mechanism `B006` exists to forbid. Both rules are `[on]`
in ruff 0.16.2, so an agent obeying both rewrites the code back and forth. MEASURED (0.16.2) +
ESTABLISHED (docs).

**Resolution — the mutable/immutable distinction.** `B006` targets **mutable** defaults, because the
hazard is *shared state that outlives the call*. A default-argument capture of an **immutable** loop
value (`int`, `str`, `tuple`, frozen dataclass, `Enum` member) creates no shared state: the object
cannot change, so once-only evaluation is exactly the desired semantics. The rule:

> **Default-argument capture is permitted, and is the correct fix for late binding, if and only if
> the captured value is immutable.** Where the value is mutable, or where immutability is not
> obvious from the expression, use `functools.partial(fn, x)` — it binds a value without adding a
> caller-visible parameter and does not trip `B006`.

Secondary consequence: `B023` and pylint `W0640` are both **heuristic**. They flag correct code that
consumes the closure before the next iteration and miss a closure stored via an intermediate helper.
Neither is a coverage claim.

### 16.2 Four more, resolved briefly

- **`S101` versus the test suite.** `S101` flags **every** `assert`, including pytest's. Exempt it
  for the test tree via `lint.per-file-ignores` — never a global `ignore = ["S101"]`, which
  re-permits `assert`-as-validation in production code where it vanishes under `-O`.
  VERSION-DEPENDENT (0.16.2).
- **`E501` versus the formatter.** Both claim line length; enable both and you get diagnostics the
  formatter cannot fix on lines it deliberately left long (a URL in a string). Set `line-length`
  once (default `88`) and leave `E501` off — it is already `[off]`. Ruff does **not** warn about
  formatter-conflicting lint rules, so this exclusion is unguarded config discipline. MEASURED
  (0.16.2). Related and worse: `ruff check --select D203 --fix` inserts a blank line that
  `ruff format` deletes, both fixes "always available", neither warning — a genuine infinite loop.
- **`TC001`–`TC003` versus runtime annotation introspection.** Moving imports into `TYPE_CHECKING`
  is wrong for any class whose annotations are read at runtime (pydantic, validating adapters,
  attrs). `lint.flake8-type-checking.runtime-evaluated-base-classes` and
  `runtime-evaluated-decorators` both default to `[]`, so the protection is **off** until
  configured, and `TC004` `[on]` catches the breakage only *after* the fix has landed. If you enable
  `TC001`–`TC003` (`[off]`), configure both exemption lists in the same commit. VERSION-DEPENDENT
  (0.16.2).
- **`ANN` versus the type checker.** `ANN001`/`ANN201` report the same defect as
  `--disallow-untyped-defs` in a second vocabulary, doubling every finding. Keep `ANN401` `any-type`
  (mypy `--strict` tolerates `Any` on *arguments*, so it is complementary) and drop the rest. All
  `ANN*` are `[off]`, so this is a decision not to opt in. MEASURED (0.16.2).

---

## 17. Autofix is not safe by default

**ESTABLISHED (ruff 0.16.2).** Ruff classifies fixes by safety: "The meaning and intent of your code
will be retained when applying safe fixes, but the meaning could change when applying unsafe fixes."
Only safe fixes run by default; the resolved setting is `unsafe_fixes = hint`, so ruff *reports*
that a hidden fix exists and will not apply it. `--unsafe-fixes` (or `unsafe-fixes` in config) opts
in; `lint.extend-safe-fixes` / `lint.extend-unsafe-fixes` reclassify per rule and accept prefixes.
MEASURED (0.16.2).

Two cases that show why "unsafe" is not pedantry. **`E711`/`E712`:** the fixes "may alter runtime
behavior when used with libraries that override the `==`/`__eq__` or `!=`/`__ne__` operators" — a
codebase using numpy, pandas, SQLAlchemy or Django `Q` objects can have its array or query semantics
silently changed by a bulk rewrite of `== None` to `is None`. ESTABLISHED. **`RUF015`:** MEASURED —
`return list(xs)[0]` under plain `--fix` is left untouched with
`No fixes available (1 hidden fix can be enabled with the --unsafe-fixes option).`; adding
`--unsafe-fixes --fix` rewrites it to `return next(iter(xs))`, changing the exception on empty input
from `IndexError` to `StopIteration`. **No happy-path test detects it.** VERSION-DEPENDENT (0.16.2).

**Policy, phrased for a contributing guide:**

1. **Never run `--unsafe-fixes` across a codebase you have not reviewed, and never put it in a hook
   or a CI step.** Default `--fix` is safe-only; keep it that way.
2. Apply unsafe fixes **one rule at a time, on a reviewable diff**, with the test for the affected
   behaviour already in place — not added afterwards.
3. Treat any fix that changes which exception is raised, or that touches
   `__eq__`/`__ne__`/`__hash__` or any other dunder, as a behaviour change requiring a test,
   regardless of the tool's label.
4. **Pin the ruff version**, because fix safety is reclassified between releases (§1.1).
5. `zip(strict=True)` via `B905`'s fix is a correct change that is still a behaviour change — it
   lands with a test for the mismatch path (§15).

---

## 18. The maximal-safety modern subset for a new 3.14 project

Prohibitions plus replacements, each tied to the hazard class it eliminates. The "enforced?" column
is the honest part: some are mechanised, some are review-only, and an agent must know which.

| prohibit | use instead | class eliminated | enforced? |
|---|---|---|---|
| A mutable literal or any call as a default argument | `None` sentinel; `field(default_factory=...)` on a record | §2 | **yes** — `B006` `[on]`, `B008` `[on]`, `RUF008` `[?]`, `RUF009` `[?]` |
| A bare mutable bound in a class body | `ClassVar[...]` for a real constant; `field(default_factory=...)` for per-instance state | §2 | partly — `RUF012` `[?]`, accurate only with the `ClassVar` annotation |
| Reliance on `__del__` for cleanup | `with`, `contextlib.closing`, `ExitStack`, `weakref.finalize` | §11 | partly — pylint `R1732` `[?]`; leak detection needs **`-X dev` + `filterwarnings = error`** |
| A `@contextmanager` body without `try`/`finally` | `try`/`finally` around the `yield`, always | §11 | partly — pylint `W0135` `[?]`; the silent-suppression variant is uncovered |
| Ad-hoc mutable record classes | `@dataclass(frozen=True, slots=True, kw_only=True)`; `copy.replace()` (3.13) to derive a variant | §2, §12 | review-only for the choice; `RUF012` for the symptom |
| Bare string/int constants standing for a closed domain | plain `Enum` with `@enum.unique`; `Literal` for a small closed set | §4, §15 | review-only. **Prefer plain `Enum` over `IntEnum`/`IntFlag`/`StrEnum`:** those are drop-in-compatible on purpose and therefore leak — `Number.THREE == 3` is `True`, and `__str__`/`__format__` use the **value**, not the name |
| `is` for value comparison | `==` for values; `is` only for `None` and true singletons | §4 | partly — `F632` `[on]`\*, while `E711`/`E712` are **`[off]` since 0.16.0** and must be selected |
| Truthiness as a stand-in for an explicit test | `if x is None:`, `if len(xs) == 0:`, or whatever the domain actually means | §4 | opt-in — mypy `truthy-bool`, `truthy-iterable` |
| `zip(a, b)` | `zip(a, b, strict=True)`; `strict=` on `batched`/`map` where available | §6 | partly — `B905` is **`[off]`**; select it and test the mismatch path |
| String path manipulation | `pathlib.Path` | representation | partly — the `PTH` family (`PTH123` is `[off]`) |
| `float` for money | `Decimal` from `str`/`int`, `FloatOperation` trapped, explicit `quantize` | §7 | runtime-catchable, and **only if the trap is installed at process start** — assert it in a startup self-test |
| Naive `datetime`; `utcnow()` | timezone-aware `datetime` with explicit `tzinfo`; `datetime.now(UTC)` | §7 | **yes** — all ten `DTZ` rules `[on]`; add `TID251` `[?]` for project-banned symbols |
| `open()` without `encoding=` | explicit `encoding="utf-8"` | §7 | partly — pylint `W1514` `[?]`; `-X dev` also checks it |
| Bare-name `case` labels in `match` | dotted value patterns (`Color.RED`) plus `case _:` → `assert_never` | §15 | **no for the capture trap** — the compiler catches only the ordering consequence. Exhaustiveness needs mypy `exhaustive-match` (opt-in) |
| `assert` for validation, auth or input checks | explicit `if ...: raise`, or a parse function at the boundary | §15 | partly — `S101` is `[off]`; doctrine in `error_tracing_contract_manifest.md` §14 |
| Loose `asyncio.create_task` | `asyncio.TaskGroup` (3.11); `asyncio.timeout` (3.11) for deadlines | §14 | partly — `RUF006` `[?]`, heuristic |
| Hand-rolled config parsing | `tomllib` (stdlib) | §13, representation | review-only |
| `pickle` across any trust boundary | `json` or a typed decoder; `hmac` signing only where tamper-evidence is the requirement | §13 | partly — `S301`/`S403` are **`[off]`**; select them |
| `yaml.load` | `yaml.safe_load` / `SafeLoader` | §13 | partly — `S506` is **`[off]`**, and `FullLoader` does not satisfy it |
| `shell=True` | a sequence `argv` with no shell; `shlex.quote()` where a shell is unavoidable | §13 | partly — the `S6xx` block is **`[off]`**. Windows `.bat`/`.cmd` is the documented exception where `shell=True` is *safer* |
| `tempfile.mktemp()` | `mkstemp()`, or `NamedTemporaryFile(delete=False)` with explicit removal | §13 | partly — `S306`, `S108` are **`[off]`** |
| Boolean and optional parameters passed positionally | keyword-only parameters (`*,`) | call-site legibility | opt-in — the `FBT` family is `[off]`; the type checker accepts `f(True)` and `f(False)` identically |
| Duck typing across a module boundary | a `Protocol` with the surface declared explicitly | §10 | type-catchable once the `Protocol` exists |
| `__getattr__`/`__setattr__` hooks to synthesise API surface | explicit attributes, a generated class, or a stub declaring the surface | §10 | **no** — a design prohibition with no diagnostic |
| `eval`/`exec`/`compile` on any non-literal input | a dispatch `dict`, or `match` over a closed domain | §13 | partly — `S307` `[off]`, `S102` `[on]` |
| Module-level mutable state | state owned by an object the imperative shell constructs and passes in | §9 | **no** — the highest-value contract-only prohibition here |
| Import-time side effects beyond definitions | a `main()`/factory the shell calls explicitly | §9 | fitness-function only: `-X importtime` budget + Import Linter contracts |

**Two 3.14 constructs to adopt deliberately, not by default. VERSION-DEPENDENT (3.14):** PEP 750
template strings — `t'...'` produces a `string.templatelib.Template` that keeps static and
interpolated parts **separate** rather than an already-concatenated `str`. Where interpolation is
*data* crossing into another language (SQL, shell, HTML), that separation is the property an
f-string destroys, so a `Template` is the structurally safer carrier; adopt it at those boundaries
only. PEP 758 permits parenthesis-free `except A, B:` — a legibility gain with no hazard
consequence, and one more construct that will not parse on 3.13. Minimum-target policy is owned by
`python_platform_baseline_manifest.md`.

\* See the §4 footnote: `F632`'s default status is derived, not individually measured.

---

## 19. Route tallies and the honest residue

The hazard tables in §2–§14 carry **103 hazard rows, 102 of them routed** — the exception is the
integer floor-division row in §7.2, held `OPEN` pending a primary page (open question 10), and by
this file's own standard at §0.1 that single row is a known defect rather than a rounding error.
Counted by route over those 102 (a row naming a primary route and a backstop counts in both, so
these
sum to 107): **lint-catchable 43**, **contract-only 29**, **type-catchable 13**,
**feature-eliminated 9**, **test-catchable 8**, **runtime-catchable 3**, **fitness-function 2**. §15
adds 13 silently-ineffective constructs and §18 adds 27 prohibition/replacement pairs. The shape is
the finding: **most Python hazards do have a mechanical route, and the residue is dominated by four
classes.** OPEN — this is a property of
this file's own tables, not a measured property of Python.

**The four honest residues.** State them in the spec; never let a green build imply coverage.

1. **Import purity and module-level mutable state.** Nothing mechanical enforces "no side effects at
   import" or "no module-level mutable state". Import Linter enforces *dependency direction*;
   `-X importtime` measures *cost*. This is the most consequential contract-only row, because
   unownable global state is what makes a codebase untestable. ESTABLISHED (by documented absence).
2. **Aliasing and copy depth.** No verified rule distinguishes a correct shallow copy from an
   incorrect one, because the answer depends on **ownership intent the code does not express**. The
   mutate-the-copy test is the only mechanical check, and only for paths a test exercises.
   ESTABLISHED.
3. **`__getattr__`-based designs are unverifiable by construction, not merely unverified.** Any
   claim that a checker "handles" dynamic attributes is false unless a stub declares the surface
   statically. ESTABLISHED.
4. **`KeyboardInterrupt`-safe cleanup is declared out of reach by CPython itself**: "Most Python
   code, including the standard library, cannot be made robust against this." The documented
   mitigation is a custom `SIGINT` handler, not more `try`/`finally`. ESTABLISHED.

Two further honesty items. Numeric-domain discipline rests on domain judgement — no linter decides
that a quantity is money (§7.1). And **the ordering and emphasis of hazards here is a hypothesis,
not a measurement**: it reflects the mechanics plus the density of dedicated lint rules (a proxy for
community-observed frequency), not telemetry from agent-generated code. OPEN.

---

## Anti-patterns checklist

Each violates a section above. Reject on sight.

- **A lint config with no explicit `select` list** — the tool version owns your standard (§1.1).
- **`select = [...]` written where `extend-select` was meant** — discards ~400 defaults (§1.1).
- **An unpinned `ruff`/`pylint`/`mypy`/`pyright`** — unpinned rule set *and* unpinned fix safety
  (§1.1, §17).
- **"We run `mypy --strict`, so the hazard codes are on"** — none of the opt-ins is in `--strict`
  (§1.2). **"We run pyright strict, so attribute init and override typos are covered"** — three
  rules are `"none"` in every mode (§1.3).
- **A rule code copied from this file into a config without checking its `[?]` marker** (§0.2); **a
  preview-gated code pulled in by prefix with preview off** — silently unenforced (§1.1, §15); **a
  removed code in `select`** — loud, but it either redirects to a *different* rule or stops ruff
  running (§1.4, §15).
- **`ruff check --fix --unsafe-fixes` across an unreviewed codebase, or in a hook** (§17).
- **A mutable literal or a function call as a default argument** (§2).
- **A closure over a loop variable that outlives the iteration** — and **a *mutable*
  default-argument capture used to fix it** (§2, §16.1).
- **`self.x = ...` intended to update a class-level datum** — creates an unrelated attribute (§2).
- **`is` for value comparison; `== None`; `== True`** (§4).
- **`if x:` where the domain distinguishes empty from absent** (§4).
- **A mutable object as a dict/set key**, or `{1: ..., True: ...}` (§4).
- **`xs[:]` / `.copy()` / `dict(d)` relied on to isolate nested state** (§5).
- **Iterating a generator twice and treating the empty second pass as data** (§6).
- **Asserting on `set` iteration order, or on `list(some_set)`** (§6).
- **`zip(a, b)` without `strict=`** (§6, §15).
- **`float` for money; `Decimal(0.1)`; `round()` where a named rounding mode was required** (§7).
- **A naive `datetime` anywhere, `utcnow()` in particular; `open()` without `encoding=`** (§7).
- **A broad `except` clause above a narrow one** (§8).
- **Reading the `except ... as e` name after the block** (§8).
- **`return`/`break`/`continue` inside `finally`** (§8).
- **`try: ... except: pass`** — use `contextlib.suppress` with a named exception (§8).
- **Module-level mutable state, or a module used as an accidental singleton** (§9).
- **Import-time work beyond definitions** (§9).
- **`__getattr__`/`__setattr__` used to synthesise API surface** (§10).
- **A blanket `# noqa` or `# type: ignore`** (§10).
- **`__del__` relied on for cleanup; a `@contextmanager` with no `try`/`finally`; `@lru_cache` on a
  method** (§11).
- **`@dataclass(eq=False)` on a value object** — restores id-based hashing silently (§12).
- **A `frozen=True` dataclass described as immutable while it holds a `list`** (§12, §15).
- **`init=False` on a dataclass whose validation lives in `__post_init__`** (§12).
- **`pickle`, `eval`, `exec`, `shell=True`, `yaml.load`, `tempfile.mktemp()` anywhere near untrusted
  input** — remembering the `S` family is `[off]` (§13).
- **`Loader=yaml.FullLoader` used to silence `S506`** (§13).
- **Audit hooks described as a sandbox, or "auditing is enabled" asserted after `sys.addaudithook`**
  (§13).
- **Reasoning about thread safety from the GIL** (§14).
- **`asyncio.create_task(...)` with the result discarded** (§14).
- **`assert (cond, "msg")`** — the tuple always passes (§15).
- **`assert` enforcing a production invariant, or any side effect inside an `assert`** (§15).
- **`case SOME_CONSTANT:` with a bare name; an `Enum` with duplicate values and no `@enum.unique`**
  (§15).
- **`IntEnum`/`StrEnum` chosen where a plain `Enum` would do** (§18).

---

## Open questions to resolve before building

Each is a decision this project must make and record; all cross-referenced to
`software_spec_discipline_manifest.md` §G5 (open-decision ledger).

1. **OPEN — the committed rule set.** Which exact `select` list, derived from which hazard rows, at
   which pinned ruff version? Until it is written down, §1.1 says the tool owns the standard. Record
   the derivation so a reviewer can check both directions (§0.3).
2. **OPEN — the `[?]` codes.** Which `[?]`-marked ruff codes are actually default-on in the pinned
   build? Run `ruff check --isolated --show-settings`, record the answer beside the `select` list,
   and re-run on every bump. Do not ship a `[?]` code as enforced.
3. **OPEN — the second checker.** mypy, pyright, or both? §1.2 and §1.3 leave *different* hazards
   uncovered: a pyright-only project has no `ignore-without-code` equivalent and no stale-ignore
   signal at all; a mypy-only project must opt into `possibly-undefined`. Pick an authority and
   enumerate what the choice forfeits.
4. **OPEN — pylint or not.** pylint is the sole mechanical route for several rows here (`E0701`
   handler ordering, `W0177` NaN comparison, `W1514` missing encoding, `W0135` contextmanager
   cleanup, `R0401` cycles, `W0201` attribute-outside-`__init__`) at the cost of a second toolchain
   and a second suppression vocabulary. If yes, enable `I0021` `useless-suppression` on day one.
5. **OPEN — assertions in production.** Does this project ship `assert` statements, and does it
   refuse to start under `-O`? Also flagged by `error_tracing_contract_manifest.md` §21; decide once
   and put the `sys.flags.optimize` self-check in the entry point if asserts are internal invariants
   only.
6. **OPEN — numeric domain per quantity.** Which quantities are `Decimal`, `float`, `Fraction`,
   `int` (§7.1)? Is `FloatOperation` trapped at process start, with a startup assertion that it is?
7. **OPEN — `PYTHONHASHSEED` policy.** Does CI sweep seeds to expose set-ordering dependence, and
   pin one seed for reproduction? A single-seed pipeline hides the hazard indefinitely (§6).
8. **OPEN — `-X dev` in CI.** Is development mode on in the test job *together with*
   `filterwarnings = error`? Both are required for `ResourceWarning` to surface a leak (§11).
9. **OPEN — warning escalation set.** Which classes fail the build: `-W error::SyntaxWarning` (the
   `is`-with-literal and 3.14 `finally` warnings), `-W error::DeprecationWarning`,
   `ResourceWarning`? Escalate deliberately with a narrow `ignore::` allowlist, not wholesale.
10. **OPEN — integer floor-division semantics for negative operands.** Not verified this session.
    Before any rule, test or comment asserts floor-toward-negative-infinity, load the
    numeric-operations table in `library/stdtypes.html` and confirm it (§7.2).
11. **OPEN — the `RUF` family beyond the verified twelve.** Only `RUF006`, `RUF008`, `RUF009`,
    `RUF012`, `RUF015`, `RUF018`, `RUF028`, `RUF100`–`RUF104` are asserted here; a bulk index
    extraction proved unreliable and one asserted name 404'd. Verify each additional code on its own
    page first (§1.4).
12. **OPEN — pyright version.** §1.3 comes from an unstamped `main`-branch document. Pin a version
    and re-read its matched `configuration.md` before treating §1.3 as ground truth.
13. **OPEN — 3.14-only constructs.** Adopt `t'...'` templates (PEP 750) and parenthesis-free
    `except A, B:` (PEP 758)? Both set a hard 3.14 floor; minimum-target policy is owned by
    `python_platform_baseline_manifest.md`.
14. **OPEN — teeth for the review-only prohibitions.** For module-level state, import purity,
    `__getattr__` forwarding and cross-boundary duck typing, does the project accept review-only, or
    invest in a project-owned mechanism (an `ast`-walking pytest, a `semgrep` rule, `TID251` for
    banned symbols)? **Ruff accepts no plugins**, so any proposal to write one is an invented
    mechanism.

---

## Sources (accessed 8 Aug 2026)

**CPython — language reference, stdlib, FAQ.** All accessed 8 Aug 2026.

- Mutable defaults created once at `def` time; late-binding lambdas returning `16` and the `n=x`
  workaround; the three guaranteed identity circumstances and the non-singleton examples; PEP 8
  `is None` rationale; `[[None]*2]*3` aliasing; `self.count = 42`; module-as-singleton —
  https://docs.python.org/3/faq/programming.html
- Bytecode-boundary atomicity, the atomic/non-atomic lists, the `__del__`-on-replace caveat, "When
  in doubt, use a mutex!" — https://docs.python.org/3/faq/library.html
- Binding-anywhere-makes-local; `UnboundLocalError` as a `NameError` subclass; class-block scope not
  reaching nested scopes including comprehensions; call-time free-variable resolution;
  `global`/`nonlocal` — https://docs.python.org/3/reference/executionmodel.html
- Comprehension implicit nested scope and the leftmost-iterable exception; `is` semantics; the
  `SyntaxWarning` for `is` with an `int` literal; generator `StopIteration` —
  https://docs.python.org/3/reference/expressions.html
- First-matching-`except`; the `as` target cleared via `finally: del N`; `finally` jump statements
  discarding the exception plus the 3.14 `SyntaxWarning`; `match` capture patterns always
  succeeding; dotted value patterns; one-irrefutable-block-and-last; `__match_args__`; the
  `with`/`__exit__` guarantee — https://docs.python.org/3/reference/compound_stmts.html
- `bool` as an `int` subtype; `__getattribute__` vs `__getattr__`; `__del__` not guaranteed at exit,
  exceptions ignored, shutdown globals possibly `None`, `weakref.finalize`; the exception-in-a-local
  reference cycle — https://docs.python.org/3/reference/datamodel.html
- `assert` as `if __debug__:`; no code emitted under optimization —
  https://docs.python.org/3/reference/simple_stmts.html
- `sys.modules` consulted first, `None` yielding `ModuleNotFoundError`; the module registered
  *before* its body runs; submodule binding on the parent; transitive `__init__.py` —
  https://docs.python.org/3/reference/import.html
- Shallow vs deep copy; recursive-object and copies-too-much failure modes; the types not copied;
  `copy.replace()` (3.13) — https://docs.python.org/3/library/copy.html
- The mutable-default `ValueError` and the 3.11 hashability change; `default_factory`; the
  `eq`/`frozen`/`unsafe_hash` to `__hash__` rules; `order`/`eq` errors; `__post_init__`/`InitVar`;
  non-default-after-default `TypeError` including via inheritance; the 3.13 field-by-field `__eq__`;
  `slots`/`kw_only` (3.10) — https://docs.python.org/3/library/dataclasses.html
- "It is not possible to create truly immutable Python objects"; `FrozenInstanceError` as an
  `AttributeError` subclass; frozen `__init__` must use `object.__setattr__()`; `__post_init__` not
  called without a generated `__init__` —
  https://docs.python.org/3/library/dataclasses.html#frozen-instances
- The exact `TypeError` strings for mixed frozen inheritance; the exact mutable-default `ValueError`
  text; `annotationlib.get_annotations(cls, format=Format.FORWARDREF)`; the `ClassVar` textual blind
  spot — https://raw.githubusercontent.com/python/cpython/3.14/Lib/dataclasses.py
- `set_int_max_str_digits`/`get_int_max_str_digits` and the `int_info` fields;
  `addaudithook`/`audit` including the sandbox disclaimer, the `PySys_AddAuditHook()` requirement
  and silent failure; `sys.flags.optimize`/`dev_mode` — https://docs.python.org/3/library/sys.html
- `round()` half-to-even and `round(2.675, 2)` giving `2.67`; the arbitrary-code warnings on
  `eval()`/`exec()`; `getattr`/`setattr` — https://docs.python.org/3/library/functions.html
- `Decimal(0.1)` expansion vs exact `Decimal('0.1')`; default context `prec=28`/`ROUND_HALF_EVEN`;
  the enabled and un-enabled traps; `FloatOperation`; NaN equality always `False` —
  https://docs.python.org/3/library/decimal.html
- `1/10` as a repeating binary fraction and `3602879701896397 / 2**55`; shortest-`repr` since 3.1;
  ten-times-`0.1` vs `sum()` vs `math.fsum()`; `math.isclose()` —
  https://docs.python.org/3/tutorial/floatingpoint.html
- `@contextmanager` re-raise at the `yield`, the `try`/`finally` requirement and the suppression
  trap; `suppress`; `ExitStack`; `closing`; single-use vs reusable vs reentrant —
  https://docs.python.org/3/library/contextlib.html
- `TaskGroup` strong references; the `create_task` weak-reference warning; `asyncio.timeout` (3.11)
  — https://docs.python.org/3/library/asyncio-task.html
- Handlers only in the main thread; deferral to a bytecode boundary and the long-running-C
  consequence; `KeyboardInterrupt` anywhere and the `__enter__`/return window; `threading.Lock`
  deadlock in handlers — https://docs.python.org/3/library/signal.html
- Security Considerations (no implicit shell, caller-owned quoting, `shlex.quote`); the Windows
  `.bat`/`.cmd` inversion; `check=` raising `CalledProcessError` —
  https://docs.python.org/3/library/subprocess.html
- The pickle security warning, the `hmac`/`json` recommendations, protocol 5 default from 3.14 —
  https://docs.python.org/3/library/pickle.html
- `mktemp()` deprecated since 2.3 with the TOCTOU warning; `delete`/`delete_on_close` and "Deletion
  is not always guaranteed in this case" (3.12) — https://docs.python.org/3/library/tempfile.html
- Duplicate values becoming aliases; `@enum.unique`; `verify` plus the `EnumCheck` members (3.11);
  `IntEnum`/`IntFlag`/`StrEnum` comparing equal to raw values and `__str__` using the value —
  https://docs.python.org/3/library/enum.html
- Development mode's exact equivalence, the warning classes it displays, faulthandler, `io.IOBase`
  destructor logging, encoding/errors checks — https://docs.python.org/3/library/devmode.html
- `runtime_checkable` checking only presence; the two 3.12 changes (`inspect.getattr_static()`,
  frozen protocol members) — https://docs.python.org/3/library/typing.html
- `annotationlib.Format` members and `get_annotations()` —
  https://docs.python.org/3/library/annotationlib.html
- `-O`/`-OO`/`PYTHONOPTIMIZE`; `-X dev`/`PYTHONDEVMODE`; `-X int_max_str_digits` and
  `PYTHONINTMAXSTRDIGITS`; the `-W` action list; `-X importtime` and `=2` with its multi-threaded
  caveat; `PYTHONHASHSEED` — https://docs.python.org/3/using/cmdline.html
- The hashable contract; iterator exhaustion "appear like an empty container"; the free-threaded
  iterator caveat — https://docs.python.org/3/glossary.html
- `dict` insertion order "declared to be an official part of the Python language spec" —
  https://docs.python.org/3/whatsnew/3.7.html
- The 4300-digit `int`/`str` cap, the affected bases, `ValueError`, CVE-2020-10735 —
  https://docs.python.org/3/whatsnew/3.11.html
- PEP 649/749 deferred annotations as default; PEP 750 t-strings and `string.templatelib.Template`;
  PEP 758 bracketless `except`; PEP 765 `finally` `SyntaxWarning`; PEP 779 supported free threading
  with the ~5-10% note; PEP 768 `sys.remote_exec` and its disable switches —
  https://docs.python.org/3/whatsnew/3.14.html
- "Implications for readers of `__annotations__`" and the `Format.FORWARDREF` recommendation —
  https://docs.python.org/3.14/whatsnew/3.14.html#porting-to-python-3-14
- The `-5`..`256` integer cache, explicitly labelled a CPython implementation detail —
  https://docs.python.org/3/c-api/long.html

**PEPs.** All accessed 8 Aug 2026.

- PEP 572 (Final, 3.8) — the walrus binding into the containing scope from a comprehension, and the
  `SyntaxError` cases — https://peps.python.org/pep-0572/
- PEP 709 (Final, 3.12) — comprehension inlining; no dedicated stack-trace frame; the `locals()` and
  `settrace`/`setprofile` changes — https://peps.python.org/pep-0709/
- PEP 649 (Final, 3.14) — deferred evaluation of annotations — https://peps.python.org/pep-0649/
- PEP 749 (Final, 3.14) — `annotationlib`; four formats, `SOURCE` renamed `STRING` —
  https://peps.python.org/pep-0749/

**Tools — rule codes, default status, fix safety.** All accessed 8 Aug 2026.

- ruff v0.16.0 (2026-07-23): default set 59 to 413; the 18 removed codes; the
  `select = ["E4","E7","E9","F"]` restoration incantation — https://astral.sh/blog/ruff-v0.16.0
- ruff 0.16.2 version and release date — https://pypi.org/project/ruff/
- 0.16.1 fix-safety reclassifications (`PT022`, `FURB105` to unsafe; `PT018` to safe) —
  https://raw.githubusercontent.com/astral-sh/ruff/main/CHANGELOG.md
- The enumerated default rule set — https://docs.astral.sh/ruff/default-rules/
- Fix-safety definitions, safe-only by default, `--unsafe-fixes`, `lint.extend-safe-fixes` /
  `lint.extend-unsafe-fixes` — https://docs.astral.sh/ruff/linter/
- The rule index: the `B`, `A001`–`A006`, `S` and `DTZ` tables with fix markers —
  https://docs.astral.sh/ruff/rules/
- `RUF012` mutable-class-default — https://docs.astral.sh/ruff/rules/mutable-class-default/
- `RUF008` mutable-dataclass-default (safe fix to `field(default_factory=...)`) —
  https://docs.astral.sh/ruff/rules/mutable-dataclass-default/
- `RUF009`, "Function calls are only performed once, at definition time" —
  https://docs.astral.sh/ruff/rules/function-call-in-dataclass-default-argument/
- `E711` none-comparison, fix **unsafe** for `__eq__`-overriding libraries —
  https://docs.astral.sh/ruff/rules/none-comparison/
- `E712` true-false-comparison, fix always available and **unsafe** —
  https://docs.astral.sh/ruff/rules/true-false-comparison/
- `B023` function-uses-loop-variable —
  https://docs.astral.sh/ruff/rules/function-uses-loop-variable/
- `B012` jump-statement-in-finally — https://docs.astral.sh/ruff/rules/jump-statement-in-finally/
- `PLW0603` global-statement — https://docs.astral.sh/ruff/rules/global-statement/
- `PLW2901` redefined-loop-name, and that `for`/`with` "don't define their own scopes" —
  https://docs.astral.sh/ruff/rules/redefined-loop-name/
- `S101` assert, "removed when Python is run with optimization requested" —
  https://docs.astral.sh/ruff/rules/assert/
- `F631` assert-tuple — https://docs.astral.sh/ruff/rules/assert-tuple/
- `F632` is-literal, **safe** fix — https://docs.astral.sh/ruff/rules/is-literal/
- `RUF018` assignment-in-assert — https://docs.astral.sh/ruff/rules/assignment-in-assert/
- `RUF006` asyncio-dangling-task — https://docs.astral.sh/ruff/rules/asyncio-dangling-task/
- `B019` cached-instance-method — https://docs.astral.sh/ruff/rules/cached-instance-method/
- `PLE0704` misplaced-bare-raise — https://docs.astral.sh/ruff/rules/misplaced-bare-raise/
- `E722` bare-except — https://docs.astral.sh/ruff/rules/bare-except/
- `S506` unsafe-yaml-load — https://docs.astral.sh/ruff/rules/unsafe-yaml-load/
- pylint 4.0.6 message index — symbolic names for W0102, W0104, W0122, W0123, W0133, W0135, W0150,
  W0177, W0201, W0602, W0603, W0621, W0622, W0640, W0703, W0705, W0718, W0719, W1510, W1514, W4701,
  E4702, E4703, E0601, E0602, E0606, E0701, E0704, E1101, R0401, R1732, C0415, I0021 (the same page
  supplies each code's **category**: `modified-iterating-dict`/`-set` are `E`, not `W`) —
  https://pylint.readthedocs.io/en/stable/user_guide/messages/messages_overview.html
- pylint `W0199` assert-on-tuple with its problematic/correct pair —
  https://pylint.readthedocs.io/en/stable/user_guide/messages/warning/assert-on-tuple.html
- pylint 4.0.6 version and release date — https://pypi.org/project/pylint/
- mypy default-enabled `truthy-function` and `used-before-def` —
  https://mypy.readthedocs.io/en/stable/error_code_list.html
- mypy 2.3.0 opt-in codes requiring `--enable-error-code`, plus `unreachable` via
  `--warn-unreachable` and `comparison-overlap` via `--strict-equality` —
  https://mypy.readthedocs.io/en/stable/error_code_list2.html
- pyright per-mode defaults: `standard` as the default; the three rules `"none"` in all four modes;
  `reportPossiblyUnboundVariable` from standard; `reportUnhashable` and `reportUnusedExpression`
  from basic; the strict-only `reportUnnecessary*` group —
  https://raw.githubusercontent.com/microsoft/pyright/main/docs/configuration.md
- pytest `filterwarnings = error` with `ignore::` lines, `-W error::UserWarning`, and PEP 565
  default display of deprecation warnings —
  https://docs.pytest.org/en/stable/how-to/capture-warnings.html
- Import Linter 2.13 contract types `forbidden`, `independence`, `layers` (2.13's docs use directory
  URLs; `/contract_types.html`, `/en/latest/` and `/en/stable/` all return 404) —
  https://import-linter.readthedocs.io/en/v2.13/contract_types/
- Import Linter 2.13 as the current release, uploaded 2026-07-03 —
  https://pypi.org/pypi/import-linter/json
- PyYAML: `load` unsafe since May 2006; the loader taxonomy; the 5.1+ warning; `safe_load` for
  untrusted input — https://github.com/yaml/pyyaml/wiki/PyYAML-yaml.load(input)-Deprecation

**Measurements** (this session, `ruff 0.16.2`; commands, not URLs).
`ruff rule --all --output-format json` — 968 rules, 830 stable / 138 preview, and the
fix-availability split. `ruff check --isolated --show-settings` — 413 default-enabled rules and
their prefix distribution; individual default status for `B006`, `B008`, `B023`, `E722`, `BLE001`,
`S102`, `S110`, `S112`, all ten `DTZ` rules, `RUF100`, `RUF101`, `RUF028`, `TC004`, `I001`; and the
`[off]` status of `E501`, `E711`, `E712`, `S101`, `B904`, `B905`, `PGH003`, `PGH004`,
`RUF102`–`RUF104`, all `ANN*`, `TC001`–`TC003`. `ruff linter` — 59 families. Plus the `RUF015` and
`D203` autofix demonstrations quoted in §16.2 and §17.
`ruff check --isolated --select TRY200|PGH001|PGH002` — each prints a remap warning **and** enforces
the successor (`B904`, `S307`, `G010`); `--select PT004` — `ruff failed / Cause: Rule PT004 was
removed and cannot be selected` (§1.4, §15).
`ruff check --isolated --select ASYNC119` (a preview rule) — ``warning: Selection `ASYNC119` has no
effect because preview is not enabled.``; the same rule reached by prefix (`--select ASYNC11`,
`--select ASYNC`) or by `--select ALL` — **no such warning at all**, and the rule does not run
(§15).


### Sibling manifests (cross-referenced, not duplicated)

- `python_platform_baseline_manifest.md` — **owns every CPython version, release-date, support-phase
  and PEP-status fact.** This file states behaviour and tags it `VERSION-DEPENDENT (3.x)`.
- `python_typing_contract_manifest.md` — owns the type system: `mypy --strict`'s exact flag list,
  the pyright modes as a typing artefact, `cast`/`Final`/`Protocol`/`NewType` runtime inertness,
  `frozen=True` shallowness and the `object.__setattr__` bypass, `Mapping` vs `MutableMapping`,
  `Annotated` metadata inertness, and what types cannot express.
- `python_linting_practices_manifest.md` — owns the rule set as configuration: family selection,
  `select` vs `extend-select`, the 18 codes ruff 0.16.0 dropped from the default set, the prefix
  distribution of the 413, the preview-selection trap (§2.1–§2.5), per-file ignores, suppression
  mechanics, the formatter/linter/checker division of labour, and the altitude practice catalogue.
  **This file supplies its derivation source (§0.3); it does not enumerate its config.**
- `python_quality_gates_manifest.md` — owns where checks run and how they fail: pre-commit and CI,
  the adoption ratchet, the `PYTHONHASHSEED` sweep and `-X dev` job settings, warning-escalation
  gates, rule-baseline diffing, supply-chain gates, and which numbers are defensible.
- `python_module_boundaries_manifest.md` — owns the import system as an architectural boundary and
  the machine enforcement of dependency direction. §9 here states the mechanics; that file enforces
  them.
- `error_tracing_contract_manifest.md` — owns the error contract: propagation channels, `except`
  doctrine, chaining, re-raise/wrap/suppress, `ExceptionGroup`/`except*`, `add_note`, EAFP/LBYL, and
  the full `assert` FOR/NOT-FOR doctrine. §8 and §15 carry only the silent mechanics.
- `python_testing_tooling_manifest.md` — owns test kinds, fixtures, the `monkeypatch` double,
  property testing, and test-tree lint exemptions. Every `test-catchable` row names a kind it
  defines.
- `python_concurrency_determinism_manifest.md` — owns the four execution models, structured
  concurrency and cancellation, free threading and subinterpreters as behaviour, and determinism
  under test. §14 carries only what single-threaded-looking code encodes wrongly.
- `python_runtime_diagnostics_manifest.md` — owns `-X dev` as a diagnostic surface, faulthandler,
  tracemalloc, profilers, post-mortem, `sys.remote_exec` as a debugging mechanism, health surfaces.
- `logging_observability_manifest.md` — owns the `G`/`LOG` rule families, lazy formatting,
  structured logging, and what must never be logged.
- `architecture_manifest_default.md` — reasoning register: paradigms,
  functional-core/imperative-shell rationale, testability and debuggability pattern families. Do not
  retro-fit epistemic tags onto it.
- `software_spec_discipline_manifest.md` — §G5 is the open-decision ledger every OPEN item above is
  addressed to.
