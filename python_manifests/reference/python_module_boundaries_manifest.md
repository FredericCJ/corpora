# Module Boundaries, Packaging & the Unit of Change — Ground-Truth Manifest

**Purpose.** A citable ground-truth reference for making **small-to-mid-scale, strictly-typed,
single-process Python** modular and incrementally buildable — reuse-first, functional core inside an
imperative shell. It grounds six decisions: (1) what the *unit of change* is and where its public
surface lives; (2) which build backend and project layout to commit to; (3) how dependencies and
metadata are declared, and for whom; (4) which import-graph edges are legal and **what mechanically
refuses the illegal ones**; (5) how a plugin seam and a composition root are wired; (6) what a
version bump, a deprecation and a module split oblige you to do. This file is **GROUNDING, not a
rulebook**: cite a principle when it materially shapes a decision; reason past it when the situation
does not match. The organising claim every section serves: **a module boundary that is not
machine-checked is a preference, and preferences decay.** Every factual claim is tagged
**ESTABLISHED** (normative and stable in the cited primary source), **VERSION-DEPENDENT** (bound to
the exact version named), **OPEN** (no authoritative source — a convention this project must pin),
or **CC-FACT** (Claude Code mechanics; none arise here); **FLAGGED-SECONDARY** marks a claim whose
only evidence was secondary. Sibling manifests are cross-referenced by filename and never
duplicated; the deferral list closes the file.

**Version anchor.** Behaviour here is stated for CPython as pinned in
`python_platform_baseline_manifest.md` (verified 2026-08-08); per-feature interpreter gates and
per-tool version gates are tagged inline (`VERSION-DEPENDENT (3.15)`, `VERSION-DEPENDENT
(import-linter >= 2.6)`). This file asserts no release dates, support phases or minimum-target
policy of its own.

---

## TL;DR

- **src layout, always.** The interpreter prepends the script or current directory to `sys.path`, so
  under a flat layout the test suite imports the working tree and never the artefact that ships.
  `python -P -c "import pkg; print(pkg.__file__)"` from the repo root is the proof. ESTABLISHED;
  `-P` is VERSION-DEPENDENT (3.11+) — §3.
- **Write one `[tool.importlinter]` contract on day one**, even if it holds a single `layers`
  contract. `__all__` and a leading underscore are documentation; a contract checked by
  `lint-imports` in CI is enforcement. ESTABLISHED — §6.4, §7.
- **Four dependency tables, four audiences.** `dependencies` ships; `optional-dependencies` ships as
  consumer-selectable extras; `[dependency-groups]` (PEP 735) **never** ships and owns
  test/lint/type tooling; `pylock.toml` (PEP 751) is the machine-generated install record.
  ESTABLISHED — §4.
- **Cycles are a mechanism, not a smell.** A module is in `sys.modules` before its body runs, so a
  cycle yields a *partially initialised* module: `import a.b` survives what `from a.b import thing`
  cannot. Fix the import form; never wrap the import in `try/except ImportError`. ESTABLISHED —
  §6.1.
- **A deprecation nobody sees is not a deprecation.** `DeprecationWarning` is filtered everywhere
  except `__main__`, so the window exists only if all four parts of §9.3's visibility contract hold:
  `@warnings.deprecated`, `-W error::DeprecationWarning` in your own suite, a consumer-side checker
  rule, and `filterwarnings` in the consumer's suite. ESTABLISHED; decorator is VERSION-DEPENDENT
  (3.13+) — §9.2–§9.3.
- **For a single-package project most of §7–§11 is over-engineering.** §12 lists exactly what to
  adopt on day one and what to skip until a stated trigger fires.

---

## 1. The unit of change

### 1.1 Three nested units

**ESTABLISHED.** Every enforcement tool in §7 operates on exactly one of these, and casual prose
fuses them:

| unit | what it is | named by | changed by |
|---|---|---|---|
| module | one `.py` (or extension) file, executed once and cached in `sys.modules` | dotted import name (`myapp.ports.storage`) | an edit |
| import package | a directory with `__init__.py` (regular) or without one (PEP 420 namespace portion) | dotted import path | adding, removing or moving a module |
| distribution | the sdist/wheel a resolver installs | `[project] name`, normalized | a release |

**ESTABLISHED.** The names need not agree: "In Python packaging there is no requirement that a
project name match the name(s) that you can import for that project" — hence PEP 794 (Accepted) and
its `Import-Name` / `Import-Namespace` fields (§5.5). **The unit of change is the import package** —
the granularity §7 can name and a reviewer can hold. The distribution is the unit of *release* (§9);
the module is the unit of *edit*.

### 1.2 One package, one public surface

**Named vocabulary: `self-contained-component`** — Preschern, *Fluent C*, 2022. The corpus records
one package per component with dependencies pointing only toward more fundamental components; the C
"one header per component" maps onto the package's public module. The seed pack's Python
instantiation: `__init__.py` is the single public surface, holding explicit re-exports. Vocabulary
ESTABLISHED (naming source cited); the mapping onto `__init__.py` is project policy — **OPEN**
unless §7 enforces it. The recorded edge `self-contained-component --uses--> restrict-dependencies`
(editorial) is this manifest in one line: the component shape becomes real only once the dependency
rule is written where a machine reads it.

**Consequence (ESTABLISHED as language behaviour; the rule itself is OPEN).** Every cross-package
import should name a package, not a module inside it — `from myapp.storage import Store`, never
`from myapp.storage.postgres.pool import _Conn`. Nothing in Python enforces that; a Tach
`[[interfaces]]` `expose` list or an import-linter `protected` contract does.

### 1.3 The five-rung ladder from preference to refusal

Each rung moves the boundary from prose into something a machine can refuse. Quoted clauses are as
the seed pack records them.

| rung | element | naming source | what it buys | what refuses a violation |
|---|---|---|---|---|
| 1 | `encapsulate` | bck 2021 | "other elements depend only on the interface" | nothing — a caller can reach past it |
| 2 | `explicit-interface` | posa4 2007 (spot-checked) | the contract is a first-class type, "explicitly separated from any implementation class" | a type checker |
| 3 | `separated-interface` | poeaa 2002 (spot-checked) | the interface lives in a *different package* from its implementation, "so clients depend only on the interface package" | the import graph itself |
| 4 | `restrict-dependencies` | bck 2021 | "Restrict which modules a given module may interact with or depend on, **in practice via interface visibility and authorization**" | an import-linter / Tach contract file |
| 5 | `interface-definition-language` | corbaspec 1991 | "a language-neutral contract … from which stubs, skeletons and serializers are generated" | the build |

**ESTABLISHED, and it is why rung 4 must be bought externally.** Python has no visibility mechanism:
`__all__` governs `from x import *` and nothing else; a single leading underscore is a convention
the interpreter ignores (§6.4). bck names *interface visibility and authorization* as the
enforcement for rung 4 — Python supplies neither, so rung 4 is a file you add. **That contract file
is the enforceable statement.**

**Rung 3 is the rung Python codebases skip — ESTABLISHED.** A `Protocol` declared beside its only
implementation buys a type-checkable shape and zero graph structure; moving it one package over
converts intent into a fact about the import graph, which is the only thing §7's tools see. **Rung 5
is over-engineering at this scale** — "for a pure-Python in-process boundary a `Protocol` in a
`ports` package *is* the contract; an IDL only pays across process or language" (§8.5).

Two supporting rungs make the result auditable rather than merely enforced: `module-view` (vab 2010)
records the permitted "uses" relation; `architecture-decision-record` (nygardadr 2011) records *why*
an edge is forbidden — §11.

**Naming caveat carried forward.** `information-hiding` has **no element** in the SWE corpus even
though Parnas 1972 is a verified corpus work; the element layer has `encapsulate`. Say "encapsulate
(bck 2021)" and cite Parnas 1972 as the origin of the *criterion*, not of an element — OPEN as
element vocabulary.

### 1.4 Where the interface lives

**Named vocabulary.** `explicit-interface` (posa4 2007) → `typing.Protocol` (PEP 544) for structural
contracts, `abc.ABC` + `abstractmethod` when nominal enforcement or subclass registration is wanted.
**FLAGGED-SECONDARY on that citation:** posa4 2007 is the corpus's *covering* work; the naming paper
is Buschmann, Henney & Schmidt, "Explicit Interface and Object Manager", EuroPLoP 2003, which the
element record carries as its `named_in`. Cite whichever the claim needs, and say which.
`separated-interface` (poeaa 2002) → `myapp/ports/storage.py` holds the `Protocol`,
`myapp/adapters/postgres.py` implements it, and `ports` imports nothing from `adapters`. Recorded
edges: `separated-interface --specializes--> explicit-interface` (editorial); `separated-interface
--composes-with--> dependency-injection` (**sourced**) — "DI wires the concrete implementation to a
client that depends only on the separated interface"; `gateway --composes-with-->
separated-interface` (editorial) — "A Gateway's interface is often defined as a Separated Interface
**so clients can be tested against a stub**" (naming source for `gateway` not recorded in the seed
pack — OPEN as vocabulary).

`Protocol` mechanics belong to `python_typing_contract_manifest.md`. The rule that belongs *here* is
**OPEN** — a convention, mechanically checkable once written: **the interface module must be
importable without importing any implementation** — checkable as a `layers` contract with `ports`
below `adapters`, or `independence` between adapter siblings.

### 1.5 Module state is part of the boundary

**Named vocabulary: `stateless-software-module`** (Preschern, *Fluent C*, 2022; the corpus's
co-source `preschernplop` is **unverified** — do not present it as verified). A module of functions
with no module-level mutable state, every resource acquired and released inside the call. The corpus
carries its cost verbatim: it "rules out cross-call caching or context", and records
`stateless-software-module --enables--> introduce-concurrency` (editorial) — no state between calls
means reentrant.

**Its named alternative is not a sin.** `software-module-with-global-state` (same naming source) is
a *named pattern* trading "simplicity for a single shared context", and `registry` (spot-checked)
requires that the scope "(process, thread, session)" stay **explicit**. Policy for this collection —
**OPEN**, a synthesis over corpus records rather than a primary-source rule, so pin it per
`software_spec_discipline_manifest.md` §G5: default to `stateless-software-module`; permit
module-level state as a *declared* exception with an explicit init/cleanup pair and a stated scope
(`contextvars` for per-task scope, never a bare module global); ban only *implicit* scope.

**The Python-specific hole.** `defensive-copy --realizes--> encapsulate` (editorial; naming source
not recorded — OPEN as vocabulary): copying mutable inputs/outputs "closes the aliasing hole in
encapsulation, making the interface **the only way** to affect internals." Returning a mutable
internal `list` from a public function silently deletes the boundary — ESTABLISHED as language
behaviour, and invisible to §7 because it is not an import. A frozen dataclass or a
`Sequence`/`Mapping` return annotation is the only route; `python_typing_contract_manifest.md` owns
the immutability types. Python has no compiler-enforced hiding at all — no forward declaration, no
separate compilation, no ABI (ESTABLISHED). Note the gap; buy enforcement with tooling.

---

## 2. The build-system contract

### 2.1 `[build-system]` is the only portable contract between a source tree and an installer

**ESTABLISHED.** PEP 517 (Final) fixes three keys: `requires` (build-time dependencies),
`build-backend` (a `module:object` string), `backend-path` (in-tree directories, relative to the
project root, which MUST refer to a location inside the source tree). PEP 518 (Final) fixes
`pyproject.toml` itself and `[build-system] requires`. PEP 621 (Final) fixes the `[project]` table.

**ESTABLISHED.** A backend must implement exactly two hooks — `build_wheel(wheel_directory,
config_settings=None, metadata_directory=None)` and `build_sdist(sdist_directory,
config_settings=None)`, each returning the produced file's basename. `get_requires_for_build_wheel`,
`prepare_metadata_for_build_wheel`, `get_requires_for_build_sdist` and PEP 660's three editable
hooks are all optional (§10.1).

**ESTABLISHED.** Frontends isolate builds by default — a frontend "SHOULD, by default, create an
isolated environment for each build, containing only the standard library and any explicitly
requested build-dependencies". `pip install --no-build-isolation` is therefore an opt-out of the
contract and requires the PEP 518 build dependencies preinstalled, not a speed knob.

**ESTABLISHED, and it invalidates a decade of advice.** pip removed the legacy `setup.py develop`
editable method, the deprecated `setup.py bdist_wheel` mechanism and `--global-option` /
`--build-option`: **no supported non-PEP-517 install path remains** — VERSION-DEPENDENT (pip >=
25.3). Any instruction that invokes `setup.py` is now actively wrong.

### 2.2 Backend decision table

Declarations are the exact strings the PyPA tutorial publishes and the pins are theirs — except
`uv_build`, whose pin is the one uv's own build-backend documentation publishes; the tutorial
currently shows `["uv_build >= 0.12.1, <0.13.0"]` (ESTABLISHED — both pages loaded 8 Aug 2026).

| backend | declaration | choose when | cost |
|---|---|---|---|
| hatchling | `["hatchling >= 1.26"]` / `"hatchling.build"` | default for pure Python; the tutorial's own default | file selection lives under `[tool.hatch.build.targets.*]` |
| setuptools | `["setuptools >= 77.0.3"]` / `"setuptools.build_meta"` | C extensions, or an existing setuptools project | auto-discovery has silent behaviours (§3.4) |
| flit_core | `["flit_core >= 3.12.0, <4"]` / `"flit_core.buildapi"` | one small pure-Python package | that published pin is flit 3; flit 4.0.x removed `[tool.flit.metadata]`, VCS-based sdist selection and `--setup-py` — VERSION-DEPENDENT (flit >= 4.0) |
| pdm-backend | `["pdm-backend >= 2.4.0"]` / `"pdm.backend"` | already using PDM | another toolchain to know |
| `uv_build` | `["uv_build>=0.12.3,<0.13"]` / `"uv_build"` | uv-managed pure Python | "currently only supports pure Python code"; discovers `src/<package_name>/__init__.py`, `module-root` defaults to `src`, name normalized to lowercase with `.`/`-` → `_`; `[tool.uv.build-backend]` `namespace` **disables the safety checks** — VERSION-DEPENDENT (uv 0.12.x) |
| maturin / scikit-build-core / meson-python | per that project | Rust / CMake / Meson extension | a non-Python toolchain enters the build |

**ESTABLISHED.** The tutorial states its own neutrality: it "will work identically with Setuptools,
Flit, PDM, and others that support the `[project]` table for metadata". The backend is a
*reversible* decision exactly as long as metadata stays in `[project]` — the strongest argument
against backend-specific metadata tables.

**ESTABLISHED.** `wheel` must never appear in `[build-system] requires`: `setuptools.build_meta`
declares what it needs via `get_requires_for_build_wheel`, and the `wheel` project is the legacy
`bdist_wheel` implementation.

**Named vocabulary: `adhere-to-standards`** (bck 2021), recorded with the **sourced** edge
`adhere-to-standards --alternative-to--> abstract-common-services`: conform to a published standard
instead of factoring a shared abstract service. For Python that is the PEP argument — prefer PEP 621
`[project]`, `Protocol`, `Iterator` over a house abstraction, because a published standard is what
makes a gate mechanical. `python_quality_gates_manifest.md` owns the gate.

### 2.3 Dynamic metadata, and what it costs

**ESTABLISHED.** "If the core metadata specification lists a field as 'Required', then the metadata
MUST specify the key statically or list it in `dynamic`." `name` can **never** be dynamic ("A build
back-end MUST raise an error if the metadata specifies `name` in `dynamic`"); `version` may be,
supporting "use cases such as filling the version from a `__version__` attribute or a Git tag".

**ESTABLISHED, and it is the rule most agents get wrong.** PEP 621 says a backend "MUST raise an
error if the metadata specifies a field statically as well as being listed in `dynamic`". PEP 808
(Accepted, drove Core Metadata 2.6) relaxes exactly that for a named set of *appendable* list/table
keys, which may be static **and** in `dynamic`, with the backend then only inserting or extending —
it "must not remove, reorder, or modify existing entries". The appendable keys are exactly
`authors`, `maintainers`, `classifiers`, `dependencies`, `entry-points`, `scripts`, `gui-scripts`,
`keywords`, `license-files`, `optional-dependencies`, `urls`, `import-names`, `import-namespaces`.
`name`, `version`, `requires-python`, `description`, `readme` and `license` remain strictly
static-or-dynamic.

**The cost, stated plainly — ESTABLISHED.** A dynamic field cannot be read from the source tree
without executing the backend, so every consumer that wants your version or dependencies — resolver,
scanner, monorepo tool, reviewer, agent — must run a build. Default to static.

### 2.4 `python -m build` is the packaging test

**ESTABLISHED.** `python -m build` produces an sdist and then builds the wheel *from that sdist* —
the only routine that catches "the sdist is missing a file the wheel build needs". A wheel-only
build from the working tree can pass while the published sdist is unbuildable. Two adjacent facts
with misleading locations: twine 7.0.0 "no longer allows metadata version 2.0", so an old backend
fails at *upload* rather than build (VERSION-DEPENDENT, twine >= 7.0); and Core Metadata is at
**2.6**, so a hardcoded `Metadata-Version: 2.1` inherited from a `setup.py` template discards
`License-Expression`, `Import-Name` and PEP 808 `Dynamic` semantics.
`python_quality_gates_manifest.md` owns where these run.

---

## 3. Layout is a boundary

### 3.1 The mechanism, not the preference

**ESTABLISHED.** "The 'src layout' deviates from the flat layout by moving the code that is intended
to be importable … into a subdirectory", and "The src layout requires installation of the project to
be able to run its code, and the flat layout does not." **That requirement is the entire
mechanism.** It matters because of the interpreter's `sys.path` prepend rules:

| invocation | prepended to `sys.path` |
|---|---|
| `python script.py` | "the directory containing that file is added to the start of `sys.path`" |
| `python -c code` | "the current directory will be added to the start of `sys.path`" |
| `python -m module` | same as `-c` |
| interactive REPL | "the current directory will be added to the start of `sys.path`" |

### 3.2 The four documented failure modes src layout prevents

**ESTABLISHED**, each quoted from the PyPA discussion page:

1. **Shadowing** — "if an import package exists in the current working directory with the same name
   as an installed import package, the variant from the current working directory will be used."
   Under a flat layout a test run from the repository root imports the working tree, never the
   installed distribution.
2. **A wheel broken in a way tests cannot see** — the documented consequence of (1): "This can lead
   to subtle misconfiguration of the project's packaging tooling, which could result in files not
   being included in a distribution." Tests pass; the published wheel is missing a module.
3. **Imports that work editable and not installed** — a flat layout puts `README.md`, `tox.ini`,
   `setup.py` and `noxfile.py` on the import path, which "would make certain imports work in
   editable installations but not regular installations".
4. **Editable installs importing what was never meant to be importable** — "The src layout helps
   enforce that an editable installation is only able to import files that were meant to be
   importable."

This is the highest-value structural decision in this territory (editorial judgement — OPEN),
because failure mode 2 stays invisible until a user files a bug against a released artefact.

### 3.3 The verification nobody runs

**ESTABLISHED.** `-P` and `PYTHONSAFEPATH` suppress exactly that prepend — "`python -m module`
command line: Don't prepend the current working directory. `python script.py` command line: Don't
prepend the script's directory… `python -c code` and `python` (REPL) command lines: Don't prepend an
empty string" — VERSION-DEPENDENT (3.11+). `-I` (isolated mode) "implies `-E`, `-P` and `-s`", and
in it "`sys.path` contains neither the script's directory nor the user's site-packages directory.
All `PYTHON*` environment variables are ignored, too" — ESTABLISHED, and the strongest available
form.

```
python -P -c "import mypkg; print(mypkg.__file__)"   # must print a site-packages path (3.11+)
python -I -c "import mypkg; print(mypkg.__file__)"   # the strict, version-portable form
```

Run it from the repository root. If the printed path is inside the working tree, the package is
shadowed and every conclusion the test suite reached is about code that may never ship.

### 3.4 setuptools auto-discovery: three silent behaviours

**ESTABLISHED**, and each one makes a flat layout *look* like it works:

- Automatic discovery "will **only** be enabled if you **don't** provide any configuration for
  `packages` and `py_modules`". Override with `[tool.setuptools.packages.find]` keys `where`,
  `include`, `exclude`, `namespaces` — where **namespace scanning is enabled by default**.
- Flat-layout auto-discovery silently excludes a long reserved directory list — `ci, bin, debian,
  doc, docs, documentation, manpages, news, changelog, test, tests, unit_test(s), example(s),
  scripts, tools, util(s), python, build, dist, venv, env, requirements, tasks, fabfile, site_scons,
  benchmark(s), exercise(s), htmlcov` plus anything starting with `.` or `_` — and reserved
  top-level *module* names `setup, conftest, test(s), example(s), build, toxfile, noxfile, pavement,
  dodo, tasks, fabfile, conanfile, manage, benchmark(s), exercise(s)`.
- With flat layout plus auto-discovery, "setuptools will refuse to create distribution archives with
  multiple top-level packages or modules."

**Corollary — ESTABLISHED.** Because `namespaces` defaults on, a stray `tests/` or `scripts/`
directory with no `__init__.py` can be picked up as a PEP 420 namespace portion and shipped (§8.3).
A missing `__init__.py` does not mean "not a package"; it means "namespace package".

---

## 4. Dependency declaration: four tables, four audiences

| table | audience | ships in wheel metadata? | installed by | use for |
|---|---|---|---|---|
| `[project] dependencies` | every consumer | yes, as `Requires-Dist` | any installer, always | what the code cannot import without |
| `[project.optional-dependencies]` | a consumer opting into a feature | yes, as `Provides-Extra` + gated `Requires-Dist` | `pip install proj[gui]` | consumer-selectable features |
| `[dependency-groups]` (PEP 735) | **this checkout only** | **no — never** | `pip install --group dev`, `uv sync --group dev` | test, lint, type-check, docs, release tooling |
| `pylock.toml` (PEP 751) | a machine reproducing an environment | n/a — not project metadata | `pip install -r pylock.toml` (experimental), `uv sync` | exact reproducible installs |

**ESTABLISHED.** Each `dependencies` entry "MUST be formatted as a valid dependency specifier" (PEP
508 grammar, PEP 440 versions — §9.1). `optional-dependencies` keys "MUST be valid values for the
`Provides-Extra` core metadata. Each value in the array thus becomes a corresponding `Requires-Dist`
entry for the matching `Provides-Extra` metadata."

**ESTABLISHED.** PEP 735 (Final) fixes `[dependency-groups]`. A group's list may hold PEP 508
specifier **strings** and **tables**, and the only legal table is a Dependency Group Include — "a
table with exactly one key, `include-group`, whose value is a string, the name of another Dependency
Group". Names are normalized before comparison, duplicates after normalization are an error, and
includes "MUST NOT include cycles, and tools SHOULD report an error if they detect a cycle."

**ESTABLISHED — the property that makes groups the right home for dev dependencies.** "Build
backends MUST NOT include Dependency Group data in built distributions as package metadata." Groups
are invisible to anyone installing the wheel. PEP 735 separates them from extras on two axes: groups
work for non-package projects, and "installation of a Dependency Group does not imply installation
of a package's dependencies (or the package itself)."

**ESTABLISHED.** There is deliberately "no syntax or specification-defined interface for installing
or referring to dependency groups. Tools are expected to provide dedicated interfaces for this
purpose." So `pip --group` and `uv --group` are *tool conventions*, and `pip install proj[dev]`
cannot install a group — it silently resolves to "no such extra".

**ESTABLISHED.** PEP 751 (Final, resolution 31-Mar-2025) settles the lock-file question: the file
MUST be named `pylock.toml`, or match `r"^pylock\.([^.]+)\.toml$"` when named or when several exist
(e.g. `pylock.dev.toml`). Mandatory top-level fields are `lock-version` (currently `"1.0"`),
`created-by` and the `[[packages]]` array of tables; `requires-python`, `environments`, `extras`,
`dependency-groups` and `default-groups` are optional. It is machine-generated and install-oriented
— "Installers consuming the file should be able to calculate what to install without the need for
dependency resolution at install-time" — so **hand-editing is not the intended use.**

| command | what it does | tag |
|---|---|---|
| `pip install --group <[path:]group>` | installs a PEP 735 group; "If a path is given, the name of the file must be `pyproject.toml`" | VERSION-DEPENDENT (pip 25.1+) |
| `pip lock` | writes `pylock.toml`; documented as "a new, _experimental_, `pip lock` command" | VERSION-DEPENDENT (pip 25.1+) |
| `pip install -r <file>` | accepts "pip's requirements.txt format, or pylock.toml format"; "pylock.toml support is experimental" | VERSION-DEPENDENT (pip 26.1+) |
| `uv export --format pylock.toml` | emits the standard format; uv's primary lockfile stays `uv.lock`; the only other `--format` is `requirements.txt` | VERSION-DEPENDENT (uv 0.12.x) |
| `uv sync --locked` | fails when the lockfile is out of date — **the CI form** | VERSION-DEPENDENT (uv 0.12.x) |
| `uv sync --frozen` | uses the lockfile *without* checking it against `pyproject.toml`; a hand-edited dependency is silently ignored | VERSION-DEPENDENT (uv 0.12.x) |

**Library versus application — OPEN, a policy split this project must adopt explicitly.** A library
writes wide ranges (every bound propagates into every downstream resolution), never an upper bound
on `requires-python` (§5.1), and treats its lock file as CI hygiene rather than a consumer contract.
An application pins narrowly and commits the lock file, because the lock file *is* the deployable.
Both put dev tooling in `[dependency-groups]`. **Named vocabulary: `package-dependencies`** (bck
2021), whose stated problem is code that "behaves correctly in development can fail in production
when the surrounding dependency versions differ" and whose three-part answer is ranges in
`[project.dependencies]` + exactness in a lock file + an image for interpreter and OS libraries.
`python_quality_gates_manifest.md` owns that gate.

**ESTABLISHED.** For a single-file tool the unit of change is smaller than a package: PEP 723
(Final) inline script metadata is the fenced comment `# /// script` … `# ///` carrying
`dependencies` (PEP 508 strings) and `requires-python`, plus an optional `[tool]` table.
Supply-chain metadata is a boundary too and is not this file's: PEP 740 (Final) index attestations
and PEP 770 (Final) `.dist-info/sboms/` are named here only so nobody re-invents them.

---

## 5. Metadata fields that change behaviour

Interpreter-version and support-phase questions route to `python_platform_baseline_manifest.md`;
this section states only what each field *does*.

**5.1 `requires-python` — the one field whose blast radius is other people's projects.**
ESTABLISHED: it is "The Python version requirements of the project", and PyPA warns "Think twice
before applying an upper bound like `requires-python = "<= 3.10"`". An upper bound propagates into
every downstream resolution and the consumer cannot override you. State a floor, never a ceiling;
the floor comes from `python_platform_baseline_manifest.md` §3e — default `>=3.13` absent a stated
policy.

**5.2 `entry-points` — a public surface that is not an import.** ESTABLISHED: `[project.scripts]`
"corresponds to the `console_scripts` group; key is entry point name, value is object reference";
`[project.gui-scripts]` "corresponds to the `gui_scripts` group"; and backends MUST raise an error
if `[project.entry-points.console_scripts]` or `[project.entry-points.gui_scripts]` is declared, "as
they would be ambiguous". In `[project.entry-points]`, "Each sub-table's name is an entry point
group; users MUST NOT create nested sub-tables" — `[project.entry-points."myapp.plugins"]` is one
group. Runtime side: §8.2.

**5.3 `license` and `license-files` (PEP 639, Final, Core Metadata 2.4).** ESTABLISHED: `license`
becomes a single SPDX expression **string** — `license = "GPL-3.0-or-later"`, `license = "MIT AND
(Apache-2.0 OR BSD-2-Clause)"`, custom identifiers as `LicenseRef-[idstring]`; `license-files` is
"An array specifying paths in the project source tree relative to the project root directory to
file(s) containing licenses and other legal notices", and an empty array means none are included.
Deprecated: the `license` table subkeys `text` and `file`, the unstructured `License` core-metadata
field, and `License ::` trove classifiers. "Tools which generate Core Metadata MUST NOT create both
these fields" (`License` and `License-Expression`), and PyPI must reject an upload declaring both.
The rule that bites mid-migration: if `license-files` is present, build tools must error if
`license` has any value other than a single top-level string. Globs allow `*`, `?`, `**` and `[]`
ranges, use forward slashes only, and MUST NOT contain `..`.

**5.4 `py.typed` (PEP 561, Final).** ESTABLISHED: a distribution opts into being type-checked by
shipping a `py.typed` marker **inside the package**; a stub-only distribution MUST be named
`foopkg-stubs` for the package `foopkg`; a partial stub distribution "MUST include `partial\n` in a
`py.typed` file". **The packaging half is the half that breaks:** the marker must be *included in
the wheel* by the backend (hatchling file selection, setuptools package data). A project with
perfect annotations and no shipped `py.typed` is untyped to every consumer's checker. What the
checker then does with it is `python_typing_contract_manifest.md`'s territory.

**5.5 `import-names` / `import-namespaces` (PEP 794, Accepted).** VERSION-DEPENDENT (Core Metadata
2.5, and only backends implementing PEP 794): arrays of valid Python identifiers answering "which
distribution provides `import PIL`", where `import-names` entries may be empty or carry a `";
private"` modifier while `import-namespaces` entries "cannot be empty". Do **not** depend on the
runtime alternative: `importlib.metadata.packages_distributions()` (VERSION-DEPENDENT 3.10+) returns
"a mapping from top-level module and import package names to lists of distribution package names
that provide them" with the documented caveat "Not reliable with editable installs that do not
supply top-level names".

**5.6 Fields to not emit at all.** ESTABLISHED: PEP 771 (Draft) proposes
`default-optional-dependency-keys` and `Default-Extra`; PEP 777 (Draft) proposes `Wheel-Version` and
a `.whlx` extension. Also Draft and unsafe to depend on: PEP 725, 780, 804, 817, 825 (Wheel
Variants), 819, 694, 710, 807; PEP 778 is Deferred; PEP 491 (Wheel 1.9) is Deferred and never
shipped. And the confusion that trips agents constantly: PEP 752 (Accepted, resolution 29-Jun-2026)
is **repositories reserving package-name prefixes** — it has nothing to do with PEP 420 import
namespace packages and changes nothing about how `import` behaves. PEP 755, its PyPI policy
implementation, is still Draft.

---

## 6. The import system as architecture

Everything in §7 is a check over the graph this section describes.

### 6.1 A module is in `sys.modules` before its body runs

**ESTABLISHED — this single fact explains every circular-import symptom.** "The module will exist in
`sys.modules` before the loader executes the module code. This is crucial because the module code
may (directly or indirectly) import itself; adding it to `sys.modules` beforehand prevents unbounded
recursion in the worst case and multiple loading in the best." The message CPython emits, from
`Python/ceval.c`: `cannot import name %R from partially initialized module %R (most likely due to a
circular import)`, with a variant appending the module's origin in parentheses.

**ESTABLISHED — the mechanical difference between the two forms.** `import a.b` binds the *module
object* and tolerates a cycle as long as no attribute is touched at import time; `from a.b import
thing` performs an attribute lookup on a possibly-partial module and is the form that raises. The
standard fixes: convert to `import a.b` plus deferred attribute access, or move the import into the
function body.

**ESTABLISHED — the failure that survives the traceback.** "If loading fails, the failing module —
and only the failing module — gets removed from `sys.modules`. Any module already in the
`sys.modules` cache, and any module that was successfully loaded as a side-effect, must remain in
the cache." A failed import leaves half-initialised *collaborators* cached, so a retry inside the
same process sees a state that never existed on a clean start.

Two more edge behaviours to know before writing a shim, both ESTABLISHED: if `sys.modules[name]`
exists but is `None`, `ModuleNotFoundError` is raised (a distinct failure from a missing entry); and
loading a submodule by any mechanism binds it on the parent — "if you have `sys.modules['spam']` and
`sys.modules['spam.foo']` … the latter must appear as the `foo` attribute of the former", so `import
spam.foo` executed *anywhere* in the process makes `spam.foo` resolvable everywhere afterwards. That
is an invisible ordering dependency and a favourite source of "it works when the tests run in this
order".

**VERSION-DEPENDENT (3.15).** The import system "now acquires per-module locks in hierarchical order
(parent packages before their submodules)", fixing a deadlock "where one thread importing `pkg.sub`
and another importing `pkg.sub.mod` could each block the other when `pkg/sub/__init__.py` imports
`pkg.sub.mod`". Below 3.15 that deadlock is real; consequences belong to
`python_concurrency_determinism_manifest.md`. No include guard is ever needed: Python caches modules
in `sys.modules`, so import is idempotent by construction and the corpus's `include-guard` does not
transpose — ESTABLISHED.

### 6.2 Absolute versus relative imports

**ESTABLISHED.** "A single leading dot indicates a relative import, starting with the current
package. Two or more leading dots indicate a relative import to the parent(s) of the current
package, one level per dot after the first." Relative imports may only use the `from X import Y`
form, because "`import XXX.YYY.ZZZ` should expose `XXX.YYY.ZZZ` as a usable expression, but
`.moduleY` is not a valid expression".

**ESTABLISHED — and this is what breaks entry points.** "Since the main module does not have a
package, modules intended for use as the main module of a Python application must always use
absolute imports." `python src/pkg/cli.py` and `python -m pkg.cli` are **not** interchangeable, and
a console-script entry point always takes the module-import path.

**House rule (OPEN — a convention, not a language rule): absolute imports everywhere.** Relative
imports are legal and sometimes tidier, but they make a module's dependencies un-greppable, defeat
plain-text review of the import graph, and break the moment a file runs as `__main__`. ruff's
`flake8-tidy-imports` carries a `ban-relative-imports` setting to enforce it — the setting name is
recorded in the seed pack, but the exact rule code was **not** verified in this pass, so treat the
code as OPEN and take it from `python_linting_practices_manifest.md`, which owns rule selection.

### 6.3 `__init__.py` re-export policy and `__all__`

**ESTABLISHED.** In a package `__init__.py`, `__all__` "is taken to be the list of module names that
should be imported when `from package import *` is encountered". Without it, `from pkg.sub import *`
"does _not_ import all submodules from the package"; it imports "whatever names are defined in the
package … This includes any names defined (and submodules explicitly loaded) by `__init__.py`. It
also includes any submodules of the package that were explicitly loaded by previous `import`
statements" — so star-import contents depend on unrelated earlier imports elsewhere in the program.
And a re-export can hide a submodule of the same name: adding a `reverse` function to
`sound/effects/__init__.py` means `from sound.effects import *` "would only import the two
submodules `echo` and `surround`, but _not_ the `reverse` submodule, because it is shadowed by the
locally defined `reverse` function".

**Re-export policy — OPEN; pin it, then let §7 enforce the consequence:**

| policy | `__init__.py` holds | consumers may import | enforcement |
|---|---|---|---|
| **explicit surface** (recommended) | explicit imports of the public names + `__all__` listing exactly them | only the names in `__all__` | Tach `[[interfaces]]` `expose`, or import-linter `protected` on the internals |
| empty `__init__.py` | nothing | any module path | none — the whole tree is public by default |
| star re-export | `from .impl import *` | whatever `impl` defines today | none, and the surface changes silently with `impl` |

The explicit surface is what makes `self-contained-component` (§1.2) real. Its cost is ESTABLISHED
too: every re-export executes at package-import time, so the package's import cost becomes the sum
of its parts.

### 6.4 The underscore convention is Python's only visibility mechanism, and it is not one

**ESTABLISHED.** `__all__` governs star-import only: it makes nothing private, does not affect
`import pkg.mod` or attribute access, and is not enforced at runtime. The single-leading-underscore
convention is the only "private" signal and is likewise unenforced. Neither stops `from pkg.mod
import _thing`.

**Therefore `__all__` is documentation and a contract file is enforcement.** Only an import-linter
`protected` contract, a Tach `visibility` / `[[interfaces]]` declaration, or a ruff ban-list refuses
the reach-past, and only at lint time (§7). The corpus records `sealed-trait --realizes-->
restrict-dependencies` (editorial) — "Visibility-based sealing restricts which modules may implement
an interface" — precisely the mechanism Python lacks (naming source not recorded — OPEN as
vocabulary).

### 6.5 Import-time side effects

**ESTABLISHED.** A module body runs exactly once, at first import, in whatever order the program
happens to import it. Anything that body does — registering a signal handler, mutating `warnings`
filters, building a registry, setting a `multiprocessing` start method, opening a connection —
becomes an ordering dependency between modules that no tool in §7 can see, because it is not an
edge. And `-O` / `PYTHONOPTIMIZE` "Remove assert statements and any code conditional on the value of
`__debug__`" — so an import-time invariant check or "this plugin must be registered" guard written
with `assert` is removed from the bytecode.

**Rule (OPEN — a convention this collection adopts, and nothing mechanical enforces it):** module
bodies define names and nothing else; all side effects belong to a function the composition root
calls (§8.4). This is the single practice that makes PEP 810 and `-X lazy_imports` safe to adopt
later. `error_tracing_contract_manifest.md` owns what assertions are for.

### 6.6 Deliberate laziness, and what each mechanism costs

**ESTABLISHED.** PEP 562 (Final, 3.7) lets a module define `__getattr__(name: str) -> Any` and
`__dir__() -> List[str]`. Module `__getattr__` is consulted only after normal lookup "on a module
object through the normal lookup (i.e. `object.__getattribute__`)" fails, and must raise
`AttributeError` for names it cannot supply; `__dir__` "overrides the standard `dir()` search on a
module". **The caveat that breaks naive shims:** "Looking up a name as a module global will bypass
module `__getattr__`. This is intentional, otherwise calling `__getattr__` for builtins will
significantly harm performance." Code *inside* the module never goes through that module's own
`__getattr__`, and any name written into the module's `__dict__` — including one resolved once and
cached there — never reaches `__getattr__` again. **The correct lazy-attribute pattern is therefore:
compute, assign into `globals()`, then return.**

**VERSION-DEPENDENT (3.15).** PEP 810 (Final, Python-Version 3.15) adds the soft keyword `lazy` for
module-scope imports: `lazy import json`, `lazy import foo.bar.baz`, `lazy from json import dumps`,
`lazy from . import name`, `lazy from .. import name`. "Lazy imports are only permitted at module
scope; using `lazy` inside a function, class body, or `try`/`except`/`finally` block raises a
`SyntaxError`. Neither star imports nor future imports can be lazy". Controls: `-X
lazy_imports=<mode>` and `PYTHON_LAZY_IMPORTS=<mode>` (What's New documents `all` and `normal`; the
PEP also documents `none`), plus `sys.set_lazy_imports()` / `sys.get_lazy_imports()` and
`sys.set_lazy_imports_filter(func)` where `func(importing, imported, fromlist)` returns `True` to
allow laziness and `False` to force eager loading; precedence is `sys.set_lazy_imports()` > `-X` >
environment variable > default. A deferred `ImportError` surfaces at *first use*, and CPython chains
the exception so the traceback shows both the `lazy import` site and the access site. For a library
that must also run on 3.14 and earlier, a module-level `__lazy_modules__` container of fully
qualified module-name strings makes ordinary `import` statements for those modules lazy on 3.15+
"with the same semantics as the `lazy` keyword", and is ignored by older interpreters.

| mechanism | portability | cost |
|---|---|---|
| plain `import` at module top | everywhere | import cost paid every run, in whatever order modules load |
| import inside a function body | everywhere | hides the edge from a human reading the header; §7's tools still parse it statically |
| PEP 562 module `__getattr__` | 3.7+ | code inside the module bypasses it; a name cached in `globals()` never fires it again |
| PEP 810 `lazy` keyword | 3.15+ only | `SyntaxError` on older interpreters; defers `ImportError` to first use |
| `__lazy_modules__` | forward-compatible | inert below 3.15, so behaviour differs by interpreter |
| `-X lazy_imports=all` | 3.15+ | **not free** — every module-body side effect (§6.5) defers to first attribute access, which may be never |

**ESTABLISHED diagnostics.** `-X importtime` "shows module name, cumulative time (including nested
imports) and self time (excluding nested imports)"; `-X importtime=2` "enables additional output
that indicates when an imported module has already been loaded. In such cases, the string `cached`
will be printed in both time columns" — VERSION-DEPENDENT (3.7 for the flag, 3.14 for `=2`); other
values are reserved. Measure before making anything lazy; `python_runtime_diagnostics_manifest.md`
owns profiling. One more 3.15 change that affects plugin code: `importlib.metadata`'s `metadata()`
and `Distribution.metadata` previously "would return an empty `PackageMetadata` object as if the
file was present but empty"; now "a `MetadataNotFound` exception is raised" — VERSION-DEPENDENT
(3.15).

---

## 7. The dependency rule, enforced

Everything above declares a boundary; this section is what refuses to merge a violation.

### 7.1 Name the tactic, then name the file that enforces it

**`restrict-dependencies`** (bck 2021) — "Restrict which modules a given module may interact with or
depend on, **in practice via interface visibility and authorization**." Python has neither (§6.4),
so the tactic is realized by a contract file. **`restrict-communication-paths`** (bck 2021) is the
*runtime* half — "the set of elements with which a given element can communicate". The corpus keeps
the two apart deliberately, and Python needs the distinction more than most languages because the
import graph and the call graph diverge the moment DI, entry points or async tasks appear. The seed
pack's instantiation: the collaborators a component may call are exactly its injected
`Protocol`-typed parameters. "Package `A` may import `B` but must never call into `B` at request
time" is a `restrict-communication-paths` statement and **no tool below can check it** — it is
contract-only, enforced by the composition root's shape (§8.4) and by review.

**The coupling triangle — three named moves, not one rule**, all recorded as **sourced**
`alternative-to` pairs (`restrict-dependencies --alternative-to--> use-an-intermediary`;
`use-an-intermediary --alternative-to--> encapsulate`; `restrict-communication-paths
--alternative-to--> use-an-intermediary`):

| move | element (bck 2021) | cost |
|---|---|---|
| forbid the edge | `restrict-dependencies` | the forbidden collaboration has to go somewhere — usually a new module |
| route it through a mediator | `use-an-intermediary` | "at some performance cost": per-event processing and communication overhead |
| hide internals behind an interface | `encapsulate` | a facade "shields clients from subsystem internals **without forbidding direct access**" — a convenience, not a boundary |

The corpus also splits coupling into two axes the single word fuses: "the **strength** of coupling
and the **syntactic/semantic distance** to be bridged". Coupling and cohesion as a reasoning frame
belong to `architecture_manifest_default.md` §3.1; what belongs here is that **choosing a vertex is
a decision the spec must record**, because only one of the three is machine-checkable.

**The cost axis nobody states.** `reduce-computational-overhead` (bck 2021) names the real price:
intermediaries and separation of concerns "add per-event processing and communication cost; **this
is the classic modifiability/performance trade-off**", and `layers` costs "indirection and
pass-through overhead". Modularity costs per-event work, not readability — and that axis decides
whether a boundary is an in-process call, a queue or a service. At this scale it is an in-process
call; a queue between two packages of one program is over-engineering.

**`limit-structural-complexity`** (bck 2021) is the measurable version — "avoid or resolve cyclic
dependencies" — and the corpus records `limit-structural-complexity --composes-with-->
restrict-dependencies` as **sourced**: "Reducing inter-component coupling and breaking cyclic
dependencies is how structural complexity is limited for test." **That edge is the justification for
putting a cycle check in CI.** The metrics bck names to gate on ("response-of-class, propagation
cost, and decoupling level") and whether any is defensible as a gate belong to
`python_quality_gates_manifest.md`.

### 7.2 Tool division of labour — none substitutes for another

| tool | axis it checks | config | invocation | fails a build? |
|---|---|---|---|---|
| import-linter | *internal* import graph against declared contracts | `setup.cfg` / `.importlinter` / `pyproject.toml` `[tool.importlinter]` | `lint-imports` (alias `import-linter lint`) | yes, non-zero exit; the exact numeric code is not stated in the documentation — **OPEN** |
| Tach | internal modules, interfaces and layers | `tach.toml` | `tach check` | yes — "will exit with a non-zero code" on violation |
| deptry | *declared dependencies* versus actual imports | `[tool.deptry]` or CLI flags | `deptry .` | yes, non-zero exit |
| pydeps | nothing — it draws | CLI flags | `pydeps --show-cycles --no-show` | **no** — a visualiser with no pass/fail contract |

**ESTABLISHED.** The shape that works: `lint-imports` **or** `tach check` for internal structure,
`deptry .` for declaration/import agreement, `pydeps --show-cycles --no-show` for a human artefact.
Where they run and how they ratchet belongs to `python_quality_gates_manifest.md`; this file owns
what each one *checks*.

### 7.3 import-linter: five contract types

**VERSION-DEPENDENT (import-linter >= 2.6).** Five built-in contract types; `protected` arrived in
2.5 and `acyclic_siblings` in 2.6. Semantics below were read against the current release, **2.13**
(2026-07-03, PyPI); pin the tool, because contract types arrive in minor releases.

| type | asserts | options that matter |
|---|---|---|
| `layers` | an ordered stack, **highest first**; higher may depend on lower, never the reverse, and "This includes indirect imports (i.e. chains of imports via other modules)"; applies to all descendants | `containers`, `exhaustive`, `exhaustive_ignores`; **no wildcards** |
| `forbidden` | named sources may not import named targets, transitively | `source_modules`, `forbidden_modules`, `ignore_imports`, `allow_indirect_imports`, `as_packages` (default `True`) |
| `independence` | "that there are no imports in any direction between the modules, even indirectly" | `modules` |
| `protected` | nothing outside the allow-list may **directly** import the protected modules — **direct imports only**, so `a → b → protected` passes (§7.4) | `protected_modules`, `allowed_importers`, `as_packages` |
| `acyclic_siblings` | children of the named ancestors form no cycles | `ancestors`, `depth` (>= 0, **default 10**; 0 = direct children only), `skip_descendants` |

**ESTABLISHED.** Top-level options: `root_package` (single) or `root_packages` (list, required when
layering several top-level packages); `include_external_packages` ("Whether to include external
packages when building the import graph"); `exclude_type_checking_imports` ("any import made under
an `if TYPE_CHECKING:` statement will not be added to the graph"). Config search order: `setup.cfg`
(INI), `.importlinter` (INI), `pyproject.toml` (TOML, `[tool.importlinter]` and
`[[tool.importlinter.contracts]]`). CLI: `lint-imports`, alias `import-linter lint` (group command
added in 2.10), with `--config`, `--contract` (repeatable), `--cache-dir` (default
`.import_linter_cache`), `--no-cache`, `--show-timings`, `--verbose`, `--version`. The documented
pre-commit integration "must use `language: system` to allow Import Linter to analyze your packages
from within a virtual environment"; a remote hook with id `import-linter` also exists.

```toml
[tool.importlinter]
root_package = "myapp"
include_external_packages = true

[[tool.importlinter.contracts]]
name = "Shell may see core; core may never see shell"   # ADR-0007
type = "layers"
layers = [
    "myapp.cli | myapp.web",   # independent siblings: neither may import the other
    "myapp.adapters", "myapp.services", "myapp.ports", "myapp.domain",
]

[[tool.importlinter.contracts]]
name = "Domain imports no I/O library"
type = "forbidden"
source_modules = ["myapp.domain", "myapp.services"]
forbidden_modules = ["httpx", "sqlalchemy", "boto3"]     # root-level external names only

[[tool.importlinter.contracts]]
name = "Only the composition root may import concrete adapters"
type = "protected"
protected_modules = ["myapp.adapters"]
allowed_importers = ["myapp.composition"]
```

### 7.4 The import-linter traps — each one produces a green build that checks nothing

All ESTABLISHED, all documented behaviour:

1. **`layers` is ordered highest-first and supports no wildcards** — reversing the list inverts the
   architecture with no error.
2. **Sibling separators are semantic.** On one `layers` line, `|` means siblings are independent and
   "not allowed to import from each other"; `:` means they may; mixing `|` and `:` on one line is an
   **invalid contract**; `(medium)` "will be ignored if [it is] not present in the file system".
3. **`containers` scopes the stack, and different containers are unconstrained relative to each
   other:** "it will allow `mypackage.foo.low` to import `mypackage.bar.high`, as they are in
   different containers."
4. **A `layers` contract ignores new modules unless `exhaustive = true`**, and "Exhaustive contracts
   are only supported for layers that define containers" (`exhaustive_ignores` is the escape hatch).
   This is the only setting that catches "someone added a package and nobody classified it".
5. **`forbidden` with overlapping source and forbidden modules can do nothing.** Defaults are
   package-wide and transitive ("Indirect imports will also be checked"), but with `as_packages =
   True` overlapping modules that share descendants are *allowed* — so `source_modules =
   ["pkg.one"]` with `forbidden_modules = ["pkg.one.**"]` has **no effect** unless `as_packages =
   false`.
6. **A third-party name in `forbidden` needs `include_external_packages = True`**, and only
   root-level names are permitted: `django`, "but not `django.db.models`".
7. **`protected` checks *direct* imports only.** Unlike `layers`, `forbidden` and `independence` —
   each of which documents transitivity explicitly — protected contracts "prevent modules from
   being directly imported, except by modules in an allow-list", so `a → b → protected` passes
   and a re-export in an allowed module launders access to a protected internal. Pair it with a
   `layers` or `forbidden` contract wherever the indirect path matters. Separately,
   `as_packages = True` (the default) lets descendants of a protected module import each other —
   usually wanted, occasionally not.
8. **`acyclic_siblings`' `depth` and `skip_descendants` are not filters:** "neither the `depth` or
   `skip_descendants` options prevent deeper imports from being considered when analyzing children
   in earlier generations … If you want to ignore an import altogether, use `ignore_imports`
   instead."
9. **Wildcards are structural.** `*` "stands in for a module name, without including subpackages";
   `**` includes subpackages; `mypackage.foo*` is "not a valid expression. (The wildcard must
   replace a whole module name.)"
10. **The ignore list is kept honest by a default — do not change it.** Entries are written
    `mypackage.foo.importer -> mypackage.bar.imported`, and `unmatched_ignore_imports_alerting` is
    `error` (**default**), `warn` or `none`. A stale ignore that matches no import *fails* the run,
    so speculative ignore lines break CI once the underlying import disappears. That is the feature.

### 7.5 Tach: the same job, a different default

**ESTABLISHED.** Tach is "a Python tool to enforce dependencies and interfaces, written in Rust",
installed with `pip install tach`, configured by `tach.toml` at the project root, checked with `tach
check`, and meant to run "like a linter or test runner, e.g. in pre-commit hooks, on-save hooks, and
in CI pipelines".

**ESTABLISHED — defaults are the whole story.** Top-level keys: `modules`, `interfaces`, `layers`,
`exclude`, `source_roots`, `exact` (default **false**; "causes `tach check` to fail if any declared
dependencies are found to be unused"), `forbid_circular_dependencies` (default **false**),
`ignore_type_checking_imports` (default **true** — silences failures from imports under
`TYPE_CHECKING`), `layers_explicit_depends_on` (default **false**), `respect_gitignore` (default
**true**, also `"if_git_repo"`), `root_module`, `rules`, plus `[cache]` and `[external]`. Per-module
keys: `path` (globs allowed, e.g. `"libs.**"`; `paths` is shorthand for a group), `depends_on`,
`cannot_depend_on` (which "takes precedence over `depends_on`"), `layer`, `visibility`, `utility`
(default false — "all other modules may import from it without declaring an explicit dependency"),
`unchecked` (default false).

**ESTABLISHED — Tach's most dangerous default.** "Omitting the `depends_on` field means the module
will be allowed to import from any other module. However, it will still be subject to those modules'
public interfaces." An unlisted `depends_on` is **"all dependencies"**, not "none". The strict form
is `depends_on = []`.

**ESTABLISHED — interfaces are what Tach adds that import-linter does not.** `[[interfaces]]` takes
`expose` ("a list of regex patterns which define the public interface"), optional `from` (regex list
of adopting modules; "If an interface entry does not specify `from`, all modules will adopt the
interface"), `visibility`, and `exclusive` (default false, which "requires that matching modules use
_only_ this interface"); "A module can match multiple interface entries — if an import matches _any_
of the entries, it will be considered valid." This is the closest thing Python has to the visibility
mechanism §6.4 says it lacks. Layers: an ordered top-level list, first entry highest — "Higher
layers may import from lower layers, but lower layers may NOT import from higher layers";
cross-layer dependencies need no `depends_on` unless `layers_explicit_depends_on = true`, and
utility modules "remain accessible without explicit declaration".

```toml
# tach.toml
source_roots = ["src"]
layers = ["shell", "service", "port", "domain"]   # first entry is the highest layer
exact = true                                      # unused declared dependencies fail the check
forbid_circular_dependencies = true
# ignore_type_checking_imports defaults to true: TYPE_CHECKING edges are NOT checked

[[modules]]
path = "myapp.domain"
layer = "domain"
depends_on = []          # explicit: the empty list is strict, an omitted key is permissive

[[interfaces]]
expose = ["Store", "StoreError"]
from = ["myapp.ports.storage"]
exclusive = true
```

**ESTABLISHED — two commands with consequences.** `tach sync` **without `--add` removes modules that
no longer exist in the source roots**; `tach show [--web] [--mermaid]` emits the §11 artefact. The
rest of the surface is `tach init`, `tach mod`, `tach check [--exact] [--dependencies]
[--interfaces]`, `tach check-external`, `tach report`, `tach map`, `tach test` (with a pytest
plugin) and `tach install`.

**Choosing (OPEN — a project decision).** import-linter has richer *layering* vocabulary and a
stricter stale-ignore default; Tach's `[[interfaces]]` is the only mechanism here that constrains
*which names* may be imported rather than which modules, and `tach show --mermaid` produces the §11
artefact for free. Running both is redundant — pin one.

### 7.6 deptry: a different axis entirely

**ESTABLISHED.** deptry checks *dependency declarations against actual imports*, not internal
structure. Its five rules: **DEP001** "Project should not contain missing dependencies"; **DEP002**
"Project should not contain unused dependencies"; **DEP003** "Project should not use transitive
dependencies"; **DEP004** "Project should not use development dependencies in non-development code";
**DEP005** "Project should not contain dependencies that are in the standard library". It reads
declarations from PEP 621 `dependencies` and `optional-dependencies`, PEP 735 `[dependency-groups]`,
Poetry, PDM, uv and `requirements.txt`; configuration lives under `[tool.deptry]` or in
`--ignore/-i`, `--per-rule-ignores/-pri`, `--extend-exclude/-ee`, `--known-first-party/-kf`,
`--requirements-files/-rt`, `--requirements-files-dev/-rtd`, `--experimental-namespace-package`.
Inline suppression `import foo # deptry: ignore` / `# deptry: ignore[DEP001,DEP003]` "must appear on
the line containing the `import` or `from` keyword" and applies "only to import-level rules (DEP001,
DEP003, DEP004), not dependency definition violations" — so DEP002 can never be silenced inline.
DEP003 matters for boundaries: importing something you did not declare, because a transitive edge
dragged it in, makes your dependency table a lie — the packaging-layer analogue of reaching past
`__init__.py`.

### 7.7 pydeps, and the honest limits of pictures

**ESTABLISHED.** pydeps is "Python module dependency visualization", requires Graphviz's `dot` on
`PATH`, and has **no pass/fail contract** — it cannot gate CI however good the picture looks. Flags:
`--max-bacon INT`, `--cluster`, `--show-cycles` (displays only cyclic relations), `--no-show`,
`--only`, `--exclude`, `-T <svg|png>`, `--reverse`; from 3.0.0 cycles are always shown.

### 7.8 What none of these tools can see

State this in the spec, because a green `lint-imports` invites the belief that the graph is fully
constrained:

| invisible to the contract | why | what covers it instead |
|---|---|---|
| `importlib.import_module(name)` with a computed name | the edge is not in the AST | the plugin seam is *meant* to be dynamic (§8.2); keep it in one module and review that module |
| entry-point resolution | `EntryPoint.load()` imports by string at runtime | that is the point — it is what keeps the graph acyclic (§8.4) |
| `TYPE_CHECKING`-only imports | import-linter's `exclude_type_checking_imports` is **off** by default; Tach's `ignore_type_checking_imports` is **on** | decide deliberately — a type-only edge is still an architectural edge |
| attribute reach-past a re-export (`pkg.internal_thing`) | it is attribute access, not an import | Tach `[[interfaces]]` `expose`, or review |
| runtime call paths | the import graph is not the call graph | `restrict-communication-paths` is contract-only (§7.1); the C&C view documents it (§11) |
| mutable state escaping through a return value | not an import | typing — §1.5 |
| an import-time guard removed by `-O` | the guard is gone from the bytecode | never write a load-bearing `assert` (§6.5) |

**A third route to the same check.** The seed pack records import-linter's graph as built with
`grimp`, and "a `grimp` assertion in the test suite" as an alternative realization of
`restrict-dependencies` — useful when a rule is too project-specific for a contract type. Recorded
in the seed pack's instantiation table; the import-linter documentation pages read for this pass do
not name the library, so treat the test-suite route as a design option rather than a documented API
— **OPEN**.

---

## 8. Plugin seams and the composition root

### 8.1 Binding time is a decision

**`defer-binding`** (bck 2021), carrying bck's cost model verbatim: "trading up-front mechanism cost
against per-change cost."

| binding time | mechanism | earns its cost when |
|---|---|---|
| build | optional extras; a facade/backend module chosen at packaging time | the variant set is known and closed |
| deploy / startup | environment + TOML config; `importlib.metadata.entry_points` | third parties must add variants without your release |
| runtime | `Protocol` + dict dispatch; a toggle router | the choice changes per request or must be reversible without a deploy |

Recorded edges, all pointing the same way: `plugin --realizes--> defer-binding` and `feature-toggle
--uses--> defer-binding` (editorial — a runtime kill switch is "**the latest binding time**"),
`resource-files --realizes--> defer-binding` (**sourced**), and `facade-backend-module-pattern
--alternative-to--> plugin` (editorial) for the build-time alternative. Toggle and release mechanics
belong to `python_quality_gates_manifest.md`. **The rule: every variation point has a binding time —
name it.** An unnamed one defaults to "whenever the import happened to run", which is §6.5's failure
mode.

### 8.2 Entry points, end to end

**`plugin`** (poeaa 2002, spot-checked) — entry points are the only dependency-inversion seam that
survives packaging. All ESTABLISHED:

- **Declaration:** `[project.entry-points."myapp.plugins"]`, one sub-table per group, no nesting
  (§5.2).
- **On disk:** `entry_points.txt` "in the `*.dist-info` directory of the distribution", contents "in
  INI format, as read by Python's configparser module".
- **Object reference:** `importable.module` or `importable.module:object.attr`, resolved exactly as
  `modname, sep, qualname = object_ref.partition(':')`, then `importlib.import_module(modname)`,
  then `getattr` down the dotted `qualname`; "If extras are used, they are a comma-separated list
  inside square brackets."
- **Group naming:** "To avoid clashes, consumers defining a new group should use names starting with
  a PyPI name owned by the consumer project, followed by `.`" — so `myapp.plugins`, never bare
  `plugins`.
- **Runtime:** `importlib.metadata.entry_points(group='myapp.plugins')` returns an `EntryPoints`
  collection with `.groups`, `.names`, `.select(...)`; each `EntryPoint` exposes `name`, `value`,
  `group`, `module`, `attr`, `extras`, `dist` and `.load()`.

**VERSION-DEPENDENT (3.12, 3.13) — the history that kills copied snippets.** Pre-3.10
`entry_points()` took no parameters and always returned a dict. Changed in 3.12: "`entry_points()`
always returns an `EntryPoints` object (previously returned a dict keyed by group)". Changed in
3.13: "`EntryPoint` objects no longer present a tuple-like interface (`__getitem__()`)".
`entry_points()['console_scripts']` is dead on 3.12+; the portable form is
`entry_points(group=...)`, with the `importlib_metadata` backport below 3.10.

**ESTABLISHED — the fragility tutorials omit.** For an *installed* project, `.dist-info/` may hold
`METADATA` (mandatory — "All other files may be omitted at the installing tool's discretion"),
`RECORD`, `INSTALLER`, `entry_points.txt` and `direct_url.json`. An installer is therefore
*permitted* to omit `entry_points.txt`. A plugin system must degrade to "no plugins found" rather
than crash, and must never be the only route to core functionality.

**ESTABLISHED.** `pkg_resources` was removed from setuptools in v82.0.0 — VERSION-DEPENDENT
(setuptools >= 82): "Most common uses of `pkg_resources` have been superseded by the
`importlib.resources` and `importlib.metadata` projects." Code using
`pkg_resources.iter_entry_points`, `resource_filename` or `pkg_resources`-style declarative
namespace packages must move to `importlib.metadata` / `importlib.resources` / PEP 420, or pin an
ancient setuptools.

### 8.3 PEP 420 namespace packages and their traps

**ESTABLISHED.** PEP 420 (Final, Python-Version 3.3): a namespace package is created by the
**absence** of `__init__.py`, and "Namespace packages cannot contain an `__init__.py`". Resolution,
per `sys.path` entry **in order**: if `<dir>/foo/__init__.py` exists, import a regular package and
return; else if `<dir>/foo.{py,pyc,so,pyd}` exists, import a module and return; else if `<dir>/foo`
exists as a directory, **record it and continue scanning**; otherwise continue — a namespace package
is created from the recorded directories only if the whole scan found no regular package or module.
Its `__path__` is a `_NamespacePath`, "a read-only iterable of strings", and "The import machinery
will behave as if a namespace package's `__path__` is recomputed before each portion is loaded"; PEP
420 notes regular packages have "a performance advantage" because a namespace package cannot be
created until every path entry has been scanned.

**ESTABLISHED — PyPA's own warning, which settles the design question.** "It's not recommended to
make your project's main top-level package a namespace package for the purpose of plugins, as one
bad plugin could cause the entire namespace to break", and "Namespace packages are a complex feature
and there are several different ways to create them." Of PyPA's three listed discovery mechanisms —
naming convention (`pkgutil.iter_modules()` over a prefix), namespace packages, and package metadata
(entry points) — **default to entry points**: it is the only one that survives an installed wheel
without a `sys.path` scan or a shared top-level name.

### 8.4 The composition root

**ESTABLISHED.** No framework is required: entry points give a name-to-callable table and
`EntryPoint.load()` is the only place a plugin module is imported, "which keeps the import graph
acyclic by construction — core defines the protocol, plugins import core, core never imports
plugins."

Four clauses, three of them checkable:

1. Core declares the `Protocol` in a `ports` package (§1.4) — checkable by a `layers` contract.
2. Plugins import core; core never imports a plugin — checkable by `forbidden` or `protected`.
3. Exactly one module resolves names to implementations (`myapp/composition.py`) — checkable as
   `protected_modules = ["myapp.adapters"]`, `allowed_importers = ["myapp.composition"]`.
4. Everything else receives its collaborators as parameters — this is `restrict-communication-paths`
   and is **contract-only**; no tool checks it.

```python
# myapp/composition.py — the only module that imports concrete adapters
from importlib.metadata import entry_points
from myapp.ports.storage import Store            # the Protocol (separated interface)

def load_stores() -> dict[str, Store]:
    return {ep.name: ep.load()() for ep in entry_points(group="myapp.stores")}
```

**`dependency-injection`** (fowlerdi — Fowler, *Inversion of Control Containers and the Dependency
Injection pattern*, 2004), aka constructor / setter / interface injection. The corpus records what
DI is chosen *against* as **sourced** edges — `service-locator --alternative-to-->
dependency-injection` ("Fowler explicitly weighs them against each other") and `registry
--alternative-to--> dependency-injection` — plus `plugin --composes-with--> service-locator`
(**sourced**): a Plugin resolves the configured implementation through "a registry seeded by
config". (`registry` and `service-locator` are spot-checked and their naming works are not recorded
in the seed pack — OPEN as vocabulary.)

**So state the choice, not a ban — OPEN, this collection's policy.** A composition root *is* a
service locator called exactly once, at startup, in one module — the difference that matters is that
the lookup is not ambient. Ambient lookup, any function reaching into a module-level registry
mid-call, is what defeats unit-testability, and that is what is banned here (§1.5). **A DI container
is over-engineering at this scale:** a function that builds objects and passes them down is the
whole mechanism.

### 8.5 Adapting at the seam, and contracts that are build inputs

**`tailor-interface`** (bck 2021): an adapter module owned by *your* side of the boundary,
`functools.partial` / `functools.wraps` wrappers — and **never** monkey-patch the foreign library. A
monkey-patch deletes the boundary instead of adapting it, and is invisible to every tool in §7
because it changes behaviour without changing an edge.

**`interface-definition-language`** (corbaspec — OMG, 1991): "a language-neutral contract … from
which stubs, skeletons and serializers are generated" — rung 5 of §1.3, and the only rung where a
violation fails the *build*. Python realizations the seed pack records: `.proto` +
`grpcio-tools`/`betterproto`; JSON Schema / OpenAPI + `datamodel-code-generator` producing pydantic
models; recorded edge `procedure-call-connector --uses --> interface-definition-language`
(**sourced**). Pair it with **`generation-gap`** (vlissideshatching — Vlissides, *Pattern Hatching*,
1998; `generation-gap --enables--> interface-definition-language`, editorial): never edit `*_pb2.py`
or generated models — subclass or wrap them in a hand-written sibling module so regeneration never
eats hand-written code. Generated modules are build output. **When not to:** for a pure-Python
in-process boundary a `Protocol` in a `ports` package *is* the contract. Adopting protobuf inside a
single-process application is over-engineering — a code-generation step, a second type system and a
build-order dependency, to buy a guarantee mypy already gives.

---

## 9. The change contract

### 9.1 PEP 440 versions, and four specifier traps

**ESTABLISHED.** PEP 440 (Final) canonical public version form:
`[N!]N(.N)*[{a|b|rc}N][.postN][.devN]`, optionally with `+<local version label>`. Pre-release
spellings normalize: `a`/`alpha` → `a`, `b`/`beta` → `b`, `rc`/`c`/`pre`/`preview` → `rc`.

| trap | the actual rule |
|---|---|
| `~=1.4.5` is not caret | "the compatible release clause is approximately equivalent to the pair of comparison clauses: `>= V.N, == V.*`" — so `~= 1.4.5` means `>= 1.4.5, < 1.5.0`. Caret behaviour is written `>=1.4.5,<2` |
| `== 1.1.*` includes pre-releases | prefix matching matches `1.1`, `1.1.post1` **and `1.1a1`** |
| bare specifiers exclude them | "Pre-releases of any kind, including developmental releases, are implicitly excluded from all version specifiers, _unless_ they are already present on the system, explicitly requested by the user, or if the only available version that satisfies the version specifier is a pre-release"; and "The exclusive ordered comparison `>V` MUST NOT allow a pre-release of the specified version unless the specified version is itself a pre-release" |
| `===` is string equality | "simple string equality operations which do not take into account any of the semantic information such as zero padding or local versions" |

SemVer (Preston-Werner, *Semantic Versioning 2.0.0*, living) is the *policy* most projects layer on
top; PEP 440 is the *grammar* the resolver implements. Only the grammar is enforced — the policy
choice is **OPEN**.

### 9.2 A deprecation policy needs a stated window

**ESTABLISHED.** PEP 387 "Backwards Compatibility Policy" is **Active** — CPython's own policy and
the de-facto library template: "Wait for the warning to appear in at least two minor Python versions
of the same major version, or one minor version in an older major version", with the stated
preference "to wait 5 years before removal (e.g., warn starting in Python 3.10, removal in 3.15)".
The warning message "should include the release the incompatibility is expected to become the
default and a link to an issue that users can post feedback to", and `PendingDeprecationWarning`
"may be used in special cases where the old and new versions of the API will coexist for many
releases".

**Your window is a number you must write down — OPEN.** PEP 387 is CPython's schedule, not yours.
Pin: how many of *your* releases a deprecation must survive; whether the unit is releases or months;
who may shorten it. Cross-reference `software_spec_discipline_manifest.md` §G5. An unstated window
makes every removal a judgement call at the worst moment.

### 9.3 Making a deprecation visible — the part that is always missing

**ESTABLISHED, and it invalidates most deprecation practice.** `DeprecationWarning` is **invisible
by default** except when raised from `__main__`. The exact default filter list, its precedence
order and the empty-list debug-build exception are `python_platform_baseline_manifest.md` §6c's;
what `-X dev` changes is its §6b. A library deprecation nobody sees is not a deprecation.

**VERSION-DEPENDENT (3.13+; `typing_extensions.deprecated` from 4.5.0 below that).** PEP 702 is
Final, Python-Version 3.13, and the decorator lives in `warnings`, **not** `typing`:
`@warnings.deprecated(message, /, *, category=DeprecationWarning, stacklevel=1)`. Runtime semantics:
"The warning specified by _category_ will be emitted at runtime on use of deprecated objects. For
functions, that happens on calls; for classes, on instantiation and on creation of subclasses. If
the _category_ is `None`, no warning is emitted at runtime." `stacklevel=1` (the default) emits "at
the direct caller of the deprecated object", and "Static type checker behavior is not affected by
the _category_ and _stacklevel_ arguments." The message is stored in a `__deprecated__` attribute;
on an `@overload` "the decorator must be after the `@typing.overload` decorator for the attribute to
exist on the overload as returned by `typing.get_overloads()`".

**ESTABLISHED.** For a hand-rolled shim, `warnings.warn(message, DeprecationWarning, stacklevel=2)`
is the correct call: "This makes the warning refer to `deprecated_api`'s caller, rather than to the
source of `deprecated_api` itself (since the latter would defeat the purpose of the warning
message)." `stacklevel=1` points at your own library; more wrapping layers need a higher number.

**The four-part visibility contract — all four, or the window is fiction. This table is the
collection's canonical statement of it; `python_quality_gates_manifest.md` §8.4 cites it rather
than restating it:**

| part | mechanism | tag |
|---|---|---|
| producer, runtime | `@warnings.deprecated("…; removed in 4.0; see <issue>")` | VERSION-DEPENDENT (3.13+) |
| producer, test | `-W error::DeprecationWarning` in your own test run, so *your* code stops using its own deprecated internals | ESTABLISHED |
| consumer, static | mypy's optional `deprecated` error code turns a use of a deprecated symbol into a type error | VERSION-DEPENDENT (mypy 2.3) |
| consumer, test | pytest `filterwarnings` promoting `DeprecationWarning` to an error in the *consumer's* suite — without it the default filters above swallow the warning and the window elapses unnoticed | ESTABLISHED |

The `filterwarnings` syntax and where it is configured belong to
`python_testing_tooling_manifest.md`; CI wiring and the ratchet to
`python_quality_gates_manifest.md`. The *contract* — that a deprecation must be simultaneously a
runtime warning, a static diagnostic and a test failure on both sides of the boundary — is this
file's.

### 9.4 Deprecating a module-level name

**ESTABLISHED, and the obvious approach silently does nothing.** To deprecate a module-level
*symbol* so callers see it, **remove the name from the module globals** and re-expose it through a
PEP 562 `__getattr__` that issues the warning. Because module globals bypass `__getattr__` (§6.6),
leaving the old name assigned disables the warning forever.

```python
# myapp/api.py
from typing import Any
import warnings

def renamed_thing() -> None: ...            # the new name, exported normally

def __getattr__(name: str) -> Any:          # reached only because `thing` is NOT a module global
    if name == "thing":
        warnings.warn(
            "myapp.api.thing is deprecated; use renamed_thing. Removed in 4.0. See <issue url>.",
            DeprecationWarning,
            stacklevel=2,
        )
        return renamed_thing
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
```

### 9.5 Expand / migrate / contract is the migration shape

**ESTABLISHED.** Parallel change, per Danilo Sato (martinfowler.com, 13 May 2014), is "also known as
expand and contract" and is "a pattern to implement backward-incompatible changes to an interface in
a safe manner, by breaking the change into three distinct phases: expand, migrate, and contract."

| phase | what you do | what enforces it |
|---|---|---|
| expand | add the new name/signature/module alongside the old; both work | tests for both paths |
| migrate | move internal callers; mark the old path with `@warnings.deprecated`; name the removal release in the message | `-W error::DeprecationWarning` in your own suite fails the build while an internal caller remains |
| contract | delete the old path in the release the message named | the version bump (§9.1) and the changelog |

**Vocabulary caveat carried forward.** `parallel-change` and `branch-by-abstraction` return **zero**
matches in the SWE element corpus — a real absence, not a search failure. Cite Sato (2014) directly,
as above; for branch-by-abstraction the closest citable structural substitutes are `defer-binding`
plus a toggle behind a `separated-interface`. Do not attach an element id to either — **OPEN**.

---

## 10. Incremental build

### 10.1 Editable installs: what they actually are

**ESTABLISHED.** PEP 660 (Final) adds three optional hooks — `build_editable(wheel_directory,
config_settings=None, metadata_directory=None)`,
`get_requires_for_build_editable(config_settings=None)`,
`prepare_metadata_for_build_editable(metadata_directory, config_settings=None)`. If
`prepare_metadata_for_build_editable` is absent the frontend should call `build_editable` and read
the metadata from the result; if `get_requires_for_build_editable` is absent the default "is
equivalent to `return []`". The constraint people violate by caching wheels in CI: the editable
wheel "must not be exposed to end users, nor cached, nor distributed."

**ESTABLISHED.** `direct_url.json` "MUST be created by installers when installing a distribution
from a requirement specifying a direct URL reference (including a VCS URL)" and "MUST NOT be created
when installing a distribution from an other type of requirement". Its presence distinguishes a
local or editable install from an index install — the check to run when a test result cannot be
reproduced from a released artefact (§3.3 is the faster version).

### 10.2 uv workspaces for a multi-package repository

**ESTABLISHED.** A workspace is "a collection of one or more packages, called _workspace members_,
that are managed together", declared by `[tool.uv.workspace]` with `members` (glob patterns,
required) and optional `exclude`; "Every workspace requires a root, which is also itself a workspace
member." It shares "a single lockfile, ensuring that the workspace operates with a consistent set of
dependencies" and a single virtual environment. `uv run` / `uv sync` operate on the root by default;
`--package <name>` targets one member, `--all-packages` targets all. A sibling dependency is
`[tool.uv.sources]` with `bird-feeder = { workspace = true }`; `[tool.uv.sources]` also supports
`path`, `git`, `url` and `index`, and `editable = true` for path and workspace dependencies.

**ESTABLISHED — uv's own "when not to".** Do not use a workspace when members "have conflicting
requirements or need separate virtual environments"; the alternative is a path dependency —
`bird-feeder = { path = "packages/bird-feeder" }` — accepting that "`uv run --package` becomes
unavailable".

**ESTABLISHED — sync behaviour that surprises people building images.** "uv will install the project
(and other workspace members) as _editable_ packages, such that re-syncing is not necessary for
changes to be reflected in the environment"; "To opt-out of this behavior, use the `--no-editable`
option"; "If the project does not define a build system, it will not be installed." The `dev` group
"is special-cased and synced by default", with `--dev` / `--only-dev` / `--no-dev` "equivalent to
`--group dev`, `--only-group dev`, and `--no-group dev` respectively"; the default set is
`tool.uv.default-groups`, which also accepts the literal `"all"`, and `--no-default-groups` disables
them all. CI wants `--locked`, not `--frozen` (§4).

**VERSION-DEPENDENT (uv >= 0.12.0) — scaffolding changed.** "Projects created with `uv init` now
declare a build system and are packaged by default" using `uv_build`; opt out with `--no-package`.
Also in 0.12.0: sdists must be `.tar.gz` ("Previously, uv also accepted legacy formats such as
`.tar.bz2` and `.tar.xz`"), wheels may not use bzip2/LZMA/XZ compression, the default pre-release
mode changed from `if-necessary-or-explicit` to `if-necessary` (so a lock refresh across that
boundary can legitimately drop a pre-release — it looks like a regression and is not), hash-checking
"requires at least one secure digest for every requirement", and `uv run project/script.py` now
"discovers its project from the script's directory" rather than the current working directory.

**Is a workspace over-engineering? OPEN — a scale judgement.** For a single deployable with one
public surface, yes: one package with internal sub-packages plus one import-linter contract gives
the same boundary at a fraction of the ceremony. A workspace earns its cost when two members have
genuinely different *release* cadences or different consumers, because the distribution is the unit
of release (§1.1).

### 10.3 Splitting a module without breaking importers

**`split-module`** (bck 2021) is "not an arbitrary bisection, but a principled separation of
responsibilities" — split by responsibility, never by line count, with `git log --name-only`
co-change clusters as the evidence. **`redistribute-responsibilities`** (bck 2021; 3rd-edition name
*increase semantic coherence*) is the move that follows — `split-module --composes-with-->
redistribute-responsibilities` (editorial): "split a non-cohesive module, **then** move related
responsibilities together into one module." bck's criterion is runnable against a git history:
responsibilities are misallocated when one likely change touches many modules, **or** a module
contains parts untouched by any scenario. The alternative to redistributing is
**`abstract-common-services`** (bck 2021) — one shared module behind the variants (a `Protocol` plus
`functools.singledispatch`, or a registry keyed by type) rather than N near-copies — whose own
**sourced** alternative is `adhere-to-standards` (§2.2). The rule of three is a default on an axis
with two named exits, not a threshold.

**The mechanical procedure, all ESTABLISHED from §6:**

1. Create the new module(s), move the code, leave the old module in place.
2. In the old module re-expose the moved names through a PEP 562 `__getattr__` (§9.4) — never by
   plain re-assignment, because a module global bypasses `__getattr__` and the warning never fires.
3. Emit `DeprecationWarning` with `stacklevel=2` and a message naming the removal release (§9.3).
4. Keep `import old.module` working — the submodule binding on the parent is created by any import
   of the submodule anywhere in the process, so do not delete the file until the window closes.
5. Update the §7 contract in the same commit. A `layers` contract with `exhaustive = true` fails on
   the new, unclassified module — that failure is the feature.
6. Run `python -m build` (§2.4): a moved module is the classic way an sdist stops containing a file
   the wheel build needs.

**Hot reload does not transpose, so do not design around it.** The corpus's `hot-code-reload`
(naming source `erlangcodereplace` — Ericsson AB, *Erlang/OTP System Documentation: Compilation and
Code Loading*, living) keeps old and new versions coexistent under a supervision tree and migrates
state; `importlib.reload` rebinds the module object but leaves every existing reference pointing at
the old classes and functions, so state handover is unachievable — ESTABLISHED. Python's honest
answer is process replacement; reload is a dev-loop convenience only.

---

## 11. Documenting the boundary

**Three views, three concerns — not one diagram.** All vab 2010 (Clements et al., *Documenting
Software Architectures: Views and Beyond*, 2nd ed.), each recorded as `--specializes-->
architecture-view` (**sourced**):

| view | concern it serves | the Python artefact |
|---|---|---|
| `module-view` | "construction, modification-impact analysis, and work assignment" | the §7 contract file **plus** a generated graph (`tach show --mermaid`, `pydeps`) |
| `component-and-connector-view` | runtime structure — "static module structure says little about runtime behavior, concurrency, or data flow" | asyncio tasks, processes, queues, HTTP clients |
| `allocation-view` | the mapping to files, machines and **teams** | the src-layout directory mapping (§3) plus `CODEOWNERS` |

**ESTABLISHED as a documented convention** (ISO/IEC/IEEE 42010:2022): each view "is constructed
following the conventions of, and governed by, a **single** viewpoint". Mixing runtime and import
structure in one picture produces a diagram that is wrong in both readings — and **in Python the
module/C&C divergence is the norm**: entry points, DI and async tasks create runtime edges with no
import edge, while `TYPE_CHECKING` creates import edges with no runtime edge. Two artefacts, not
one; `restrict-communication-paths` (§7.1) is documented by the second because no tool checks it.

**Recording *why* an edge is forbidden.** `architecture-decision-record` (nygardadr — Nygard,
*Documenting Architecture Decisions*, 2011), whose problem statement is exactly the agent failure
mode: later maintainers "either cargo-cult the decision or blindly reverse it." One
`docs/adr/NNNN-*.md` per boundary decision (MADR shape), cross-referenced *from the contract that
enforces it* — a comment naming the ADR beside the `[[tool.importlinter.contracts]]` block, as in
§7.3. Recorded edge: `architecture-decision-record --composes-with--> architecture-description`
(editorial). **`context-map`** (evansddd — Evans, *Domain-Driven Design*, 2003; `context-map
--uses--> bounded-context` and `--uses--> anti-corruption-layer`, both **sourced**) adds what an
import rule cannot express: the relationship *kind* at each seam — partnership, customer-supplier,
conformist, anti-corruption layer. `A` may import `B`, but is `A` conforming to `B`'s model or
defending against it? An anti-corruption layer is `tailor-interface` (§8.5) with a name for its
intent.

**A diagram is not a constraint.** A picture, a `module-view` and an ADR record *intent*; they
refuse nothing. `tach show --mermaid` and `pydeps --show-cycles` are **derived from** the code, so
they are always true and never binding — ESTABLISHED for the tool behaviours. Generate the picture
from the code, keep the contract hand-written, and never let the picture be the source of truth (the
practice rule is OPEN).

**The layering style is a choice the corpus states sharply.** `hexagonal-architecture
--alternative-to--> layers` (editorial) — "Ports-and-adapters replaces top-down abstraction layering
with a **symmetric inside/outside** core boundary"; `clean-architecture --specializes--> layers` and
`--composes-with--> hexagonal-architecture` (both **sourced**) make Clean Architecture the
synthesis, not a third option; `functional-core-imperative-shell` (Bernhardt 2012) realizes
hexagonal "at component scale" — the framework-free version, and this collection's default. Citation
asymmetry: `hexagonal-architecture` is verified (Cockburn 2005) while `clean-architecture`'s naming
work `martincleanarch` is **unverified** in the corpus's bibliographic record. Paradigm reasoning
belongs to `architecture_manifest_default.md`; what belongs here is that whichever style you pick
becomes a `layers` contract or it is not real.

---

## 12. The minimum viable boundary contract for a single-package project

**Scale discipline — OPEN as policy; every underlying fact is tagged in its own section.** Most of
§7–§11 is over-engineering for one package with one public surface and one deployable. What follows
is the whole boundary contract at that size.

**Adopt on day one:**

1. **src layout, one distribution, one top-level import package** (§3) — the only item here that
   cannot be retrofitted cheaply, because the failure it prevents is invisible.
2. **`[build-system]` with hatchling and all metadata in `[project]`** (§2.2), `version` static
   unless a single source of truth forces otherwise (§2.3).
3. **`[dependency-groups]` for every dev dependency** (§4) — never an `optional-dependencies.dev`
   extra, which publishes your test tooling as a permanent `Provides-Extra`.
4. **`requires-python` with a floor and no ceiling** (§5.1); the floor comes from
   `python_platform_baseline_manifest.md` §3e — default `>=3.13` absent a stated policy.
5. **`py.typed` shipped inside the package and verified present in the built wheel** (§5.4).
6. **Absolute imports; `__init__.py` holds an explicit public surface with `__all__`** (§6.2, §6.3).
7. **One import-linter `layers` contract with three or four layers, in CI** (§7.3) — the item that
   converts every preference above into a check. Add one `forbidden` contract if a domain/IO
   separation is worth stating.
8. **`deptry .` in CI** (§7.6) — catches the undeclared-dependency break that no internal contract
   sees, and needs no configuration to start.
9. **`python -m build` in CI** (§2.4).

**Skip until the trigger fires:**

| skip | adopt when |
|---|---|
| import-linter *and* Tach together | never — pick one (§7.5) |
| `exhaustive = true` + `containers` | the package has enough sub-packages that "somebody added one and nobody classified it" is plausible |
| an entry-point plugin system | a third party must add a variant without your release (§8.1); until then a dict in `composition.py` is the same mechanism without the packaging surface |
| PEP 420 namespace packages | you are splitting a namespace across distributions you do not all own — and read §8.3 first |
| a DI container | never at this scale (§8.4) |
| an IDL / codegen | a process or language boundary exists (§8.5) |
| a uv workspace | two members have different release cadences or consumers (§10.2) |
| PEP 810 `lazy` / `-X lazy_imports` | `-X importtime` shows a measured import-cost problem (§6.6) |
| a committed `pylock.toml` | you deploy the project — applications yes, libraries no (§4) |
| maintained module/C&C/allocation diagrams | more than one team touches the code; before that, generate on demand (§11) |
| an ADR per decision | the decision is one a future agent would plausibly reverse — a low bar for boundary decisions, so this is the one item worth adopting early (§11) |

**The sentence to carry out of this file:** the boundary is whatever `lint-imports` (or `tach
check`) refuses; everything else in your architecture document is a wish.

---
## Anti-patterns checklist

Each is a violation of the section named. Reject on sight.

- **Flat layout for anything that ships** — tests import the working tree, not the artefact
  (§3.1–§3.2).
- **Never running `python -P -c "import pkg; print(pkg.__file__)"` from the repo root** (§3.3).
- **A missing `__init__.py` read as "not a package"** — PEP 420 imports it as a namespace portion,
  and setuptools' `namespaces` discovery is on by default (§3.4, §8.3).
- **`wheel` in `[build-system] requires`**, or any instruction that invokes `setup.py` (§2.1).
- **A wheel-only build as the packaging check** — `build` builds the wheel *from the sdist* (§2.4).
- **Metadata in a backend-specific table when `[project]` has a key for it** (§2.2).
- **`dynamic` used for convenience** — consumers must now run a build to learn your dependencies
  (§2.3).
- **Hardcoded `Metadata-Version: 2.1`** — Core Metadata is at 2.6 (§2.4).
- **`license = { text = "MIT" }` or a `License ::` classifier** — deprecated (§5.3).
- **An upper bound on `requires-python`** — it propagates downstream and cannot be overridden
  (§5.1).
- **Annotations shipped without `py.typed` in the wheel** — the package is untyped to consumers
  (§5.4).
- **Emitting a Draft PEP's fields** (`Default-Extra`, `Wheel-Version`, `.whlx`, variant filenames)
  (§5.6).
- **Confusing PEP 752 repository namespaces with PEP 420 import namespaces** (§5.6).
- **Test/lint dependencies in `[project.optional-dependencies.dev]`** — that publishes dev tooling
  as a permanent `Provides-Extra`; groups never ship (§4).
- **`pip install proj[dev]` to install a dependency group** — extras cannot address a group (§4).
- **Writing "Python has no standard lock file"**, or hand-editing `pylock.toml` (§4).
- **`uv sync --frozen` in CI** — it does not check the lockfile against `pyproject.toml` (§4).
- **`~=1.4.5` to mean caret** (it means `>=1.4.5,<1.5.0`), or `== 1.1.*` believed to exclude `1.1a1`
  (§9.1).
- **`try: import x / except ImportError: pass` as a cycle fix** — it hides the cycle and converts it
  into an `AttributeError` later; change the import form (§6.1).
- **Relative imports in a module that can run as `__main__`**, or treating `python src/pkg/cli.py`
  and `python -m pkg.cli` as interchangeable (§6.2).
- **`from pkg import *` as a public surface** — order-dependent without `__all__`, enforcing nothing
  with it (§6.3–§6.4); and a re-export sharing a submodule's name shadows that submodule (§6.3).
- **Treating `__all__` or a leading underscore as access control** (§6.4).
- **Side effects in a module body** — invisible ordering dependencies, deferred to never when lazy
  (§6.5).
- **A load-bearing `assert` at import time** — `-O` removes it from the bytecode (§6.5).
- **A lazy shim that assigns nothing into `globals()`, or leaves the old global bound** (§6.6,
  §9.4).
- **`lazy import` below 3.15**, or inside a function, class body or `try`/`except`/`finally` (§6.6).
- **A boundary that exists only in a diagram, a docstring or a code review** (§1.3, §11).
- **An import-linter `layers` list written lowest-first**, or `|` and `:` mixed on one line (§7.4).
- **A `forbidden` contract whose source and forbidden modules overlap at default `as_packages`**
  (§7.4).
- **Relying on a `protected` contract to stop an *indirect* import** — it checks direct imports
  only, so a re-export in an allowed module launders access (§7.3–§7.4).
- **A growing package with no `exhaustive = true`** — new unclassified packages pass forever (§7.4).
- **`unmatched_ignore_imports_alerting = "none"`** — the `error` default keeps the ignore list
  honest (§7.4).
- **A third-party name in `forbidden` without `include_external_packages = True`, or a submodule
  name like `django.db.models`** (§7.4).
- **A Tach module with `depends_on` omitted** — that means "may import anything" (§7.5).
- **Assuming Tach checks `TYPE_CHECKING` imports** — `ignore_type_checking_imports` defaults true
  (§7.5).
- **`# deptry: ignore` on a DEP002 finding** — inline suppression covers DEP001/003/004 only (§7.6).
- **Treating `pydeps` output as a gate**, or running both import-linter and Tach (§7.5, §7.7).
- **Claiming the contract constrains the runtime call graph** — it constrains imports only (§7.1,
  §7.8).
- **`entry_points()['console_scripts']`** — dead since 3.12; the tuple interface went in 3.13
  (§8.2).
- **Any use of `pkg_resources`** — removed in setuptools 82.0.0 (§8.2).
- **A plugin system that crashes when no plugins are found** — an installer may omit
  `entry_points.txt`, and making your main top-level package a namespace package to host them risks
  the whole namespace (§8.2–§8.3).
- **Ambient service lookup mid-call** — a composition root resolves once, at startup, in one module
  (§8.4).
- **Monkey-patching a third-party library instead of writing an adapter** — it changes behaviour
  without changing an edge, so nothing in §7 sees it (§8.5).
- **An IDL or protobuf inside a single-process pure-Python app**, or editing generated code (§8.5).
- **`@deprecated` imported from `typing`** (it lives in `warnings`), placed above `@overload`, or
  `warnings.warn(..., stacklevel=1)` in a shim (§9.3).
- **A deprecation without `-W error::DeprecationWarning` in your own suite**, or with no stated
  window and no removal release in the message (§9.2–§9.3).
- **Caching or distributing a PEP 660 editable wheel** (§10.1).
- **Designing around `importlib.reload` for a running process** (§10.3).
- **Splitting a module by line count** — `split-module` is "a principled separation of
  responsibilities" (§10.3).

---

## Open questions to resolve before building

Decisions this project must make; none has an authoritative source. Record each as ASSUMED or
NEEDS-INPUT per `software_spec_discipline_manifest.md` §G5.

1. **OPEN — the layer stack.** Write the ordered layer names for this codebase (highest first) and
   which siblings are `|` versus `:`. Until that list exists, §7 is unusable and "keep it modular"
   is a preference.
2. **OPEN — import-linter or Tach.** import-linter has richer layering vocabulary and a stricter
   stale-ignore default; Tach has `[[interfaces]]` (name-level visibility) and `--mermaid`. Running
   both is redundant (§7.5).
3. **OPEN — are `TYPE_CHECKING` edges part of the architecture?** The two tools default opposite
   ways, so the answer must be explicit (§7.8).
4. **OPEN — the re-export policy** (explicit surface with `__all__`, empty `__init__.py`, or star
   re-export) and, if explicit, which mechanism enforces it (§6.3).
5. **OPEN — module-level state policy:** the default, the exception procedure (declared init/cleanup
   pair, stated scope, `contextvars` for per-task scope) and who approves an exception (§1.5).
6. **OPEN — the deprecation window:** how many of *your* releases a deprecation must survive, in
   releases or months, who may shorten it, and whether error codes and exception types carry the
   same guarantee (§9.2; `error_tracing_contract_manifest.md` owns the error contract).
7. **OPEN — versioning policy on top of PEP 440:** SemVer or date-based; what counts as breaking for
   a consumer who reached past `__init__.py`; whether `0.x` licence to break is claimed (§9.1).
8. **OPEN — one distribution or several**, and therefore whether a workspace exists. Decide before
   publishing: splitting later means new distribution names on PyPI (§10.2, §12).
9. **OPEN — is there a plugin seam at all?** If no third party must add a variant without your
   release, a dict in `composition.py` is the same mechanism without the packaging surface (§8.1,
   §12).
10. **OPEN — "seam" has no citation.** This collection's most load-bearing word (used in
    `architecture_manifest_default.md` §1, §4.2 and §6) has **no element in the SWE corpus**,
    verified by search over all 1083 element ids, names, akas and `what` fields. Either cite
    Feathers, *Working Effectively with Legacy Code*, 2004 directly, or rebuild the vocabulary on
    `specialized-interfaces` (bck 2021), `explicit-interface` (posa4 2007), `dependency-injection`
    (fowlerdi 2004) and `humble-object` (Meszaros, *xUnit Test Patterns*, 2007) — do not leave it
    uncited (§8).
11. **OPEN — import-linter's numeric exit code** is not stated in the documentation loaded for this
    pass (only Tach's non-zero exit is explicit). Verify empirically before a CI script
    distinguishes "violations found" from "tool crashed" (§7.2).
12. **OPEN — the ruff rule code for banning relative imports.** The `flake8-tidy-imports` setting
    name `ban-relative-imports` is recorded; the code was not verified this pass. `TID251`
    (`banned-api`) *is* verified. Take codes from `python_linting_practices_manifest.md` (§6.2).
13. **OPEN — will `-X lazy_imports` ever be enabled?** It changes *when* import errors and
    module-body side effects occur, so if the answer is "maybe later", §6.5's no-side-effects rule
    must be adopted now (§6.6).

---

## Sources (accessed 8 Aug 2026)

PEP statuses were read from the canonical `Status:` / `Created:` / `Resolution:` headers.

- Packaging PEP index with per-PEP status, and the canonical headers for PEPs 517, 518, 621, 639,
  660, 735, 740, 751, 752, 755, 771, 777, 794, 808, 810, 508, 440, 427, 491, 561, 420, 562, 702,
  723, 770 and 387 — https://peps.python.org/topic/packaging/ and
  https://raw.githubusercontent.com/python/peps/main/peps/pep-0517.rst (same path per PEP number).
  Accessed 8 Aug 2026.
- The build and metadata contract — `[build-system]` keys, hook signatures, the isolated-environment
  SHOULD, `backend-path`; the static-versus-`dynamic` prohibition, `Provides-Extra` mapping and the
  `console_scripts` error rule; PEP 808's thirteen appendable keys and its insert/extend-only rule;
  the three PEP 660 editable hooks and "must not be exposed to end users, nor cached, nor
  distributed" — https://peps.python.org/pep-0517/ , https://peps.python.org/pep-0621/ ,
  https://peps.python.org/pep-0808/ , https://peps.python.org/pep-0660/ . Accessed 8 Aug 2026.
- Dependency declaration and licensing — `[dependency-groups]`, `include-group`, normalization, the
  never-ships rule and the groups/extras distinction; `pylock.toml` naming, mandatory fields and
  machine-generated intent; SPDX `license`, `license-files` globs, Core Metadata 2.4 and the
  mutual-exclusivity rules — https://peps.python.org/pep-0735/ , https://peps.python.org/pep-0751/ ,
  https://peps.python.org/pep-0639/ . Accessed 8 Aug 2026.
- Distribution identity and supply chain — `Import-Name`/`Import-Namespace` and Metadata 2.5;
  `.dist-info/sboms/`; index attestations; `py.typed`, `foopkg-stubs` and `partial\n`; PEP 723
  inline script metadata — https://peps.python.org/pep-0794/ , https://peps.python.org/pep-0770/ ,
  https://peps.python.org/pep-0740/ , https://peps.python.org/pep-0561/ ,
  https://peps.python.org/pep-0723/ . Accessed 8 Aug 2026.
- Draft PEPs whose fields must not be emitted — https://peps.python.org/pep-0771/ ,
  https://peps.python.org/pep-0777/ , https://peps.python.org/pep-0825/ ,
  https://peps.python.org/pep-0819/ . Accessed 8 Aug 2026.
- Import-system PEPs — namespace-package creation, the four-step scan, `_NamespacePath` and the
  performance note; module `__getattr__`/`__dir__` and the module-globals bypass; the `lazy` forms,
  restrictions, `-X lazy_imports`, `sys.set_lazy_imports_filter`, `__lazy_modules__` and
  deferred-exception chaining — https://peps.python.org/pep-0420/ ,
  https://peps.python.org/pep-0562/ , https://peps.python.org/pep-0810/ . Accessed 8 Aug 2026.
- Versions and deprecation — the PEP 440 grammar, `~=` equivalence, `.*` prefix matching, `===` and
  the implicit pre-release exclusion; PEP 387's window and warning-content requirement; PEP 702
  `@deprecated` semantics and `category=None` — https://peps.python.org/pep-0440/ ,
  https://peps.python.org/pep-0387/ , https://peps.python.org/pep-0702/ . Accessed 8 Aug 2026.
- src layout versus flat layout — the current-directory-first import path, the shadowing failure
  mode, "requires installation" and the editable-only-imports argument —
  https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/ . Accessed 8 Aug
  2026.
- PyPA specifications — every `[project]` key with required/optional/appendable status and the
  `dynamic` rules; dependency groups (includes, normalization, no cycles, no specification-defined
  install interface); the PEP 508 specifier grammar; `entry_points.txt`, INI format, the
  object-reference resolution code and the group-name convention; Core Metadata 2.1–2.6;
  installed-project `.dist-info` contents with the "may be omitted at the installing tool's
  discretion" rule and the `direct_url.json` MUST/MUST NOT —
  https://packaging.python.org/en/latest/specifications/pyproject-toml/ , `/dependency-groups/`,
  `/dependency-specifiers/`, `/entry-points/`, `/core-metadata/` and
  `/recording-installed-packages/` on the same host. Accessed 8 Aug 2026.
- PyPA guides — the packaging tutorial (src layout, four backend blocks with exact pins, hatchling
  as default, `python3 -m build`); writing `pyproject.toml` (the `requires-python` upper-bound
  warning, SPDX examples, `dynamic = ["version"]`); creating and discovering plugins (the three
  mechanisms, `entry_points(group=...)`, "one bad plugin could cause the entire namespace to break")
  — https://packaging.python.org/en/latest/tutorials/packaging-projects/ ,
  https://packaging.python.org/en/latest/guides/writing-pyproject-toml/ ,
  https://packaging.python.org/en/latest/guides/creating-and-discovering-plugins/ . Accessed 8 Aug
  2026.
- Interpreter and standard library — `sys.modules` insertion before execution, the failed-import
  cache semantics, `None` in `sys.modules`, submodule binding on the parent and relative-import dot
  semantics; `__all__` behaviour and the submodule-shadowing example; `-P`/`PYTHONSAFEPATH`, `-I`,
  `-X importtime` and `importtime=2`, `-O` removing asserts and the exact `sys.path` prepend rules;
  `entry_points()` returning `EntryPoints` with the 3.12/3.13 changes and
  `packages_distributions()`'s editable caveat; `DeprecationWarning`'s default invisibility outside
  `__main__` (the filter list itself is the hub's, §6c) and `stacklevel=2` semantics —
  https://docs.python.org/3/reference/import.html ,
  https://docs.python.org/3/tutorial/modules.html , https://docs.python.org/3/using/cmdline.html ,
  https://docs.python.org/3/library/importlib.metadata.html ,
  https://docs.python.org/3/library/warnings.html . Accessed 8 Aug 2026.
- Python 3.15 behaviour — PEP 810 controls, the `importlib.metadata` `MetadataNotFound` change and
  the hierarchical per-module import-lock deadlock fix; and the verbatim circular-import message
  from CPython — https://docs.python.org/3.15/whatsnew/3.15.html and
  https://raw.githubusercontent.com/python/cpython/main/Python/ceval.c . Accessed 8 Aug 2026.
- setuptools — auto-discovery preconditions, the flat-layout reserved name lists, the
  multiple-top-level refusal, `namespaces` on by default, and `pkg_resources` removed in v82.0.0 —
  https://setuptools.pypa.io/en/latest/userguide/package_discovery.html and
  https://setuptools.pypa.io/en/latest/history.html . Accessed 8 Aug 2026.
- pip — the 25.3 removal of `setup.py develop` and `setup.py bdist_wheel`, 25.1 `--group` and
  experimental `pip lock`, 26.1 experimental `-r pylock.toml`, plus the `--group <[path:]group>`,
  `--no-build-isolation` and `--config-settings` semantics — https://pip.pypa.io/en/stable/news/ and
  https://pip.pypa.io/en/stable/cli/pip_install/ . Accessed 8 Aug 2026.
- uv — workspace definition and members, one lockfile and environment, `{ workspace = true }`,
  editable-by-default sync, `dev` special-casing, `uv_build`'s pure-Python limitation and
  `[tool.uv.build-backend]` keys, `uv export --format` values, and the 0.12.0 breaking changes —
  https://docs.astral.sh/uv/concepts/projects/workspaces/ , `/sync/`, `/dependencies/`,
  https://docs.astral.sh/uv/concepts/build-backend/ , https://docs.astral.sh/uv/reference/cli/ and
  https://github.com/astral-sh/uv/blob/main/CHANGELOG.md . Accessed 8 Aug 2026.
- Other backends and the publisher — `[tool.hatch.build.targets.*]` with `packages` as a collapsing
  `only-include`; flit 4.0's removals; twine 7.0.0 disallowing metadata 2.0 —
  https://hatch.pypa.io/latest/config/build/ , https://flit.pypa.io/en/stable/history.html ,
  https://twine.readthedocs.io/en/stable/changelog.html . Accessed 8 Aug 2026.
- Import Linter — the five contract types, `lint-imports` and the `import-linter lint` alias, CLI
  options, config search order, `root_package(s)`, `include_external_packages`,
  `exclude_type_checking_imports`, the pre-commit `language: system` requirement, and the
  2.5/2.6/2.10 release notes — https://import-linter.readthedocs.io/en/stable/ with its
  `/contract_types/`, `/get_started/configure/`, `/get_started/run/` and `/release_notes/` pages.
  The current release, 2.13 (uploaded 2026-07-03) — https://pypi.org/pypi/import-linter/json .
  Accessed 8 Aug 2026.
- Import Linter contract semantics, verbatim — `layers` ordering and the `|` / `:` / `(x)` syntax,
  `containers`, `exhaustive`/`exhaustive_ignores`, the `as_packages` overlap rules,
  `protected_modules`/`allowed_importers` and `protected`'s direct-only scope,
  `ancestors`/`depth`/`skip_descendants`, the shared `ignore_imports` and
  `unmatched_ignore_imports_alerting` defaults, and the wildcard rules —
  https://raw.githubusercontent.com/seddonym/import-linter/master/docs/contract_types/index.md plus
  `layers.md`, `forbidden.md`, `independence.md`, `protected.md` and `acyclic_siblings.md` on that
  path. Accessed 8 Aug 2026.
- Tach — `tach.toml` top-level and per-module keys with defaults, interfaces, layers, the "omitting
  `depends_on`" rule, the command set, "written in Rust", and non-zero exit on violation —
  https://raw.githubusercontent.com/tach-org/tach/main/docs/usage/configuration.md plus
  `/docs/usage/commands.md` and `/README.md` on that path. Accessed 8 Aug 2026.
- deptry — the five DEP rules with exact titles, the declaration sources, the CLI and
  `[tool.deptry]` options, and the inline `# deptry: ignore[...]` scope — https://deptry.com/ ,
  https://deptry.com/rules-violations/ , https://deptry.com/usage/ . Accessed 8 Aug 2026.
- pydeps as a visualiser with no pass/fail contract, and its Graphviz `dot` requirement —
  https://pypi.org/project/pydeps/ . Accessed 8 Aug 2026.
- mypy's optional `deprecated` error code, one of the two consumer-side parts of a deprecation
  window — https://mypy.readthedocs.io/en/stable/error_code_list2.html . The other, pytest's
  `filterwarnings` ini option taking filters such as `error` and `ignore::UserWarning` —
  https://docs.pytest.org/en/stable/how-to/capture-warnings.html (configuration owned by
  `python_testing_tooling_manifest.md`). Accessed 8 Aug 2026.

**Named practices and vocabulary**, recorded as the SWE corpus records them. Where the corpus's
bibliographic record marks a work **unverified**, this file says so at the point of use and never
presents it as verified.

- Parallel change (expand / migrate / contract) — Danilo Sato, 13 May 2014 —
  https://martinfowler.com/bliki/ParallelChange.html . Accessed 8 Aug 2026.
- Dependency injection, and Service Locator as the alternative it is weighed against — Martin
  Fowler, *Inversion of Control Containers and the Dependency Injection pattern*, 2004 —
  https://martinfowler.com/articles/injection.html . Accessed 8 Aug 2026.
- Architecture Decision Record — Michael Nygard, *Documenting Architecture Decisions*, 2011 —
  https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions . Accessed 8 Aug 2026.
- Hexagonal Architecture (Ports and Adapters) — Alistair Cockburn, HaT Technical Report 2005.02 —
  https://alistair.cockburn.us/hexagonal-architecture/ . Accessed 8 Aug 2026.
- Erlang/OTP code loading, the mechanism `importlib.reload` does not provide — Ericsson AB —
  https://erlang.org/doc/system/code_loading.html . Accessed 8 Aug 2026.
- Semantic Versioning 2.0.0, the policy layered on PEP 440's grammar — https://semver.org . Accessed
  8 Aug 2026.
- Separated Interface, Plugin, Registry, Service Stub — Martin Fowler et al., *Patterns of
  Enterprise Application Architecture*, 2002 — https://martinfowler.com/books/eaa.html . Accessed 8
  Aug 2026.
- `restrict-dependencies`, `restrict-communication-paths`, `encapsulate`, `use-an-intermediary`,
  `defer-binding`, `split-module`, `redistribute-responsibilities`, `abstract-common-services`,
  `tailor-interface`, `limit-structural-complexity`, `reduce-computational-overhead`,
  `adhere-to-standards` and `package-dependencies` — L. Bass, P. Clements & R. Kazman, *Software
  Architecture in Practice*, 4th ed., 2021 (Addison-Wesley SEI, ISBN 978-0-13-688609-9).
- `module-view`, `component-and-connector-view`, `allocation-view` — P. Clements, F. Bachmann, L.
  Bass, D. Garlan, J. Ivers, R. Little, P. Merson, R. Nord & J. Stafford, *Documenting Software
  Architectures: Views and Beyond*, 2nd ed., 2010 (Addison-Wesley). The single-viewpoint rule —
  ISO/IEC/IEEE 42010:2022.
- `explicit-interface` — the corpus's *covering* work is F. Buschmann, K. Henney & D. Schmidt,
  *Pattern-Oriented Software Architecture Vol. 4*, 2007 (Wiley, ISBN 0-470-05902-8); the element
  record's `named_in` is the earlier paper, Buschmann, Henney & Schmidt, "Explicit Interface and
  Object Manager: Two Patterns from a Pattern Language for Distributed Computing", EuroPLoP 2003 —
  cite whichever the claim needs, and say which (FLAGGED-SECONDARY, §1.4).
  `interface-definition-language` — Object Management Group, *The Common Object Request Broker:
  Architecture and Specification*, 1991. `generation-gap` — John Vlissides, *Pattern Hatching:
  Design Patterns Applied*, 1998 (Addison-Wesley, ISBN 978-0-201-43293-0).
- `self-contained-component`, `stateless-software-module`, `software-module-with-global-state` — C.
  Preschern, *Fluent C: Principles, Practices, and Patterns*, 2022 (O'Reilly, ISBN 978-1492097334).
  The corpus's co-source `preschernplop` is **unverified**.
- `context-map`, `bounded-context` — Eric Evans, *Domain-Driven Design*, 2003 (Addison-Wesley, ISBN
  978-0-321-12521-7). `functional-core-imperative-shell` — Gary Bernhardt, *Functional Core,
  Imperative Shell*, 2012. The decomposition criterion behind `encapsulate` — D. L. Parnas, *On the
  Criteria To Be Used in Decomposing Systems into Modules*, 1972 (CACM 15(12):1053-1058).
- `clean-architecture`, used only to state the layering choice — R. C. Martin, *Clean Architecture*,
  2017. **Unverified** in the corpus's bibliographic record, as is `monolith2micro` (Newman,
        *Monolith to Microservices*). Do not present either as verified.

### Sibling manifests (cross-referenced, not duplicated)

- `python_platform_baseline_manifest.md` — **the version hub**: release dates, support phases,
  PEP-status-by-version, interpreter switches and the minimum-target policy. Every "when" routes
  here.
- `python_quality_gates_manifest.md` — where §7's checks run, how they fail, incremental adoption,
  supply-chain gates (PEP 740, PEP 770), and which structural numbers are defensible as gates. This
  file owns *what* a contract asserts; that one owns *where it runs*.
- `python_typing_contract_manifest.md` — `Protocol` versus `ABC`, variance, frozen dataclasses and
  immutable return types, and what a checker does with `py.typed` and `partial`.
- `python_linting_practices_manifest.md` — ruff/pylint rule selection and codes (including `TID251`
  `banned-api` and the relative-import ban) and suppression hygiene.
- `python_testing_tooling_manifest.md` — pytest configuration, including `filterwarnings` promoting
  `DeprecationWarning` to an error, and test obligations for a deprecation window.
- `error_tracing_contract_manifest.md` — the exception contract, what assertions are for, and
  whether error codes carry deprecation guarantees.
- `logging_observability_manifest.md` — logging configuration and the library-versus-application
  split; the only overlap here is that a library must not configure logging at import time (§6.5).
- `python_runtime_diagnostics_manifest.md` — profiling and live-process inspection; `-X importtime`
  appears here as a boundary diagnostic, but measurement discipline lives there.
- `python_concurrency_determinism_manifest.md` — consequences of the pre-3.15 import deadlock and
  why statelessness matters for reentrancy.
- `python_language_hazards_manifest.md` — the hazard catalogue and its enforcement routes, including
  the `-O`-strips-`assert` hazard referenced at §6.5.
- `architecture_manifest_default.md` — coupling and cohesion (§3.1), state and ownership (§3.2),
  interfaces and contracts (§3.5), seams (§4.2) and refactoring moves (§6); this file supplies the
  citable names and the mechanical enforcement for those sections.
- `software_spec_discipline_manifest.md` — §G5 ASSUMED/NEEDS-INPUT discipline, where every OPEN
  lands.
