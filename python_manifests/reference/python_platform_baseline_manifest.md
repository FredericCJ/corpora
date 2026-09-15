# CPython Platform Baseline — Ground-Truth Manifest

**Purpose.** The shared **version hub** for the Python manifest collection. Every
VERSION-DEPENDENT claim in every sibling file resolves against this one, so that no other file
carries a release date that can drift silently. **Scope:** small-to-mid-scale, strictly-typed,
single-process Python. This file grounds six decisions: *which interpreter versions exist and are
still supported*, *what `requires-python` should say and what it does not mean*, *which language and
stdlib constructs are actually available at a chosen floor*, *which build variant an artefact was
produced by*, *which interpreter switches to turn on for development and diagnosis*, and *what is
being removed and when*. It contains **no design advice** — deliberately; where a decision needs
judgement, the owning sibling file is named. This file is **GROUNDING, not a rulebook**: cite a
principle when it materially shapes a decision; reason past it when the situation does not match.
Tag legend: **ESTABLISHED** = normative and stable in the cited primary source;
**VERSION-DEPENDENT** = bound to the named version; **OPEN** = no authoritative source, a convention
the project must pin; **CC-FACT** = Claude Code mechanics (none arise here); **FLAGGED-SECONDARY** =
the only evidence found was non-primary. An untagged factual claim in this file is a defect.

**Version anchor.** This file **is** the version anchor — the one exception to the collection's rule
that version facts route through the hub. Everything below was confirmed against a primary page
(`peps.python.org`, `docs.python.org`, `devguide.python.org`, `python.org` release pages,
`blog.python.org`, `packaging.python.org`, PyPI, `scientific-python.org`) on **2026-08-08**. Treat
the whole file as expiring: §8 gives the pages to reload and the events that invalidate it.

---

## TL;DR

- **The newest release is 3.14.7 (2026-08-05), not "3.14".** Pin patch versions in CI, not feature
  lines; `3.14.0` is ten months and roughly 2,000 bugfixes behind current — the sum of the
  per-release counts stated on the 3.14.1–3.14.7 release pages (558 + 18 + 299 + 337 + 154 + 179 +
  499 = 2,044). VERSION-DEPENDENT (3.14).
- **3.15 is at rc1 (2026-08-04), feature-frozen since 2026-05-07 and ABI-frozen from rc1**, with
  final scheduled 2026-10-01. Wheels built against the release candidates work on final 3.15, so add
  3.15 to the test matrix now rather than in October. VERSION-DEPENDENT (3.15).
- **3.16 has no downloadable artefact of any kind**; alpha 1 is scheduled 2026-10-13. Any claim
  about released 3.16 behaviour is fabrication. And **PEP 2026 (CalVer) was rejected** — there is no
  Python 3.26. VERSION-DEPENDENT (3.16) / ESTABLISHED.
- **Default to `requires-python = ">=3.13"`, and state the policy that produced it.** 3.13 is the
  lowest floor still in the bugfix phase and the first that makes `@warnings.deprecated` native
  (§3e); `">=3.12"` is the SPEC 0-aligned alternative and forfeits that. CPython's own window
  (5 years) currently permits 3.10; SPEC 0's window (36 months) puts the floor at 3.12.
  `requires-python` is a resolver exclusion filter, not a record of what CI ran (§3).
  ESTABLISHED (the windows) / OPEN (the choice, §3e).
- **The same version number is several different interpreters.** Free-threaded vs GIL, JIT on/off,
  tail-call vs computed-goto dispatch, frame pointers on/off — each changes behaviour, ABI or
  measurement. Record the build configuration in every performance and crash artefact (§5).
  VERSION-DEPENDENT (3.13+).
- **`DeprecationWarning` is invisible by default outside `__main__`**, so the removal calendar in §7
  will not announce itself. Making it visible is a CI decision, owned by
  `python_quality_gates_manifest.md`. ESTABLISHED.

---

## 1. The support matrix — which Pythons exist on 2026-08-08

### 1a. Branch, phase, artefact

**VERSION-DEPENDENT (all rows; verified 2026-08-08).** Phase and end-of-life columns come from
`devguide.python.org/versions/`; the per-branch schedule PEP is authoritative where the two differ.
**Dates marked (est.) are printed in italics on the devguide page, which means they are estimates,
not commitments.** Every "latest artefact" date below is a historical fact.

| Branch | Schedule PEP | Phase on 2026-08-08 | Latest artefact | First release | End of life | Installers? |
|---|---|---|---|---|---|---|
| `main` (= future 3.16) | PEP 826 | **feature** — the only branch accepting new features | none yet; alpha 1 scheduled **2026-10-13** (est.) | **2027-10-05** (est., PEP 826) | 2032-10 (est.) | n/a |
| 3.15 | PEP 790 | **prerelease** | **3.15.0rc1**, 2026-08-04 | **2026-10-01** (est., PEP 790) | 2031-10 (est.) | pre-release installers published |
| 3.14 | PEP 745 | **bugfix** | **3.14.7**, 2026-08-05 | 2025-10-07 | 2030-10 (est.) | yes |
| 3.13 | PEP 719 | **bugfix** (final bugfix release due around 3.15.0 final, i.e. ≈2026-10) | **3.13.15**, 2026-08-05 | 2024-10-07 | 2029-10 (est.) | yes, until the last bugfix release |
| 3.12 | PEP 693 | **security** | **3.12.13**, 2026-03-03 | 2023-10-02 | 2028-10 (est.) | **no — source only** |
| 3.11 | PEP 664 | **security** | **3.11.15**, 2026-03-03 | 2022-10-24 | 2027-10 (est.) | **no — source only** |
| 3.10 | PEP 619 | **security** | **3.10.20**, 2026-03-03 | 2021-10-04 | **2026-10 (est.) — ≈2 months out** | **no — source only** |
| 3.9 | PEP 596 | **end-of-life** | — | 2020-10-05 | **2025-10-31 (actual, not an estimate)** | no |

Release managers, per devguide: Savannah Ostrowski (3.16), Hugo van Kemenade (3.15, 3.14), Thomas
Wouters (3.13, 3.12), Pablo Galindo Salgado (3.11, 3.10), Łukasz Langa (3.9). VERSION-DEPENDENT.

**One divergence worth knowing.** For 3.16.0 the devguide matrix prints *2027-10-06* while PEP 826
schedules *2027-10-05*. Both are estimates; the schedule PEP is the authority, and a one-day
difference in an estimate a year out is not a fact worth propagating. VERSION-DEPENDENT (3.16).

### 1b. What each phase actually permits

**ESTABLISHED** (`devguide.python.org/developer-workflow/development-cycle/`):

| Phase | What lands | Artefact form |
|---|---|---|
| **feature** | new features, on `main` only | alphas/betas when scheduled |
| **prerelease** | during rc, "only reviewed code changes which are clear bug fixes" | rc installers |
| **bugfix** | bugfixes, roughly every 2 months | source + binary installers |
| **security** | only "issues exploitable by attackers such as crashes, privilege escalation and, optionally, other issues such as denial of service attacks" | **source-only**, "done only when actual security fixes have been applied" |
| **end-of-life** | nothing | nothing |

Three consequences an agent must not have to rediscover:

- **Security-phase Pythons have no binary installers.** The 3.12.13 release page states plainly that
  "Python 3.12 isn't receiving regular bug fixes anymore, and binary installers are no longer
  provided for it". CI that downloads a python.org installer for 3.12, 3.11 or 3.10 fails.
  VERSION-DEPENDENT (3.10, 3.11, 3.12).
- **Security-phase releases have no cadence.** The 2026-03-03 tri-release announcement: "As these
  Python versions are now in security-fix-only mode, these are source-only releases, and there is no
  pre-set release cadence." Pinning `3.11.15` is reproducible; it says nothing about how fast a CVE
  fix arrives. VERSION-DEPENDENT (3.10, 3.11, 3.12).
- **CVE eligibility follows phase.** devguide's security policy limits CVE IDs to branches in
  **bugfix** or **security** status; **feature** and **prerelease** branches are not eligible. A
  security finding against 3.15.0rc1 or a 3.16 alpha sits outside the CVE process. ESTABLISHED.

### 1c. Version strings and identity

**ESTABLISHED (the surfaces) / VERSION-DEPENDENT (`sys.abi_info` is 3.15+).** The reliable identity
surfaces: `sys.version_info` (the tuple to branch on),
`sys.version` and `python -VV` (which also carry build markers such as "free-threading build" — §5),
`sys.abiflags` (`t` for free-threaded, `d` for a debug build), and `sys.abi_info`, a namespace
describing the running build's ABI, **added in 3.15**. `python -m sysconfig` prints the full
configuration and is the correct way to answer "how was this interpreter built" (§5g).

---

## 2. Release-cycle mechanics an agent must not guess

### 2a. Annual features, bi-monthly fixes

**VERSION-DEPENDENT.** One feature release per year, landing in early October: 3.13.0 on 2024-10-07,
3.14.0 on 2025-10-07, 3.15.0 scheduled 2026-10-01, 3.16.0 scheduled 2027-10-05. During the bugfix
phase, micro releases arrive **approximately every two months** — PEP 719's wording for 3.13 is
"bugfix updates approximately every 2 months". The two most recent patch releases, 3.14.7 and
3.13.15, both shipped 2026-08-05.

### 2b. The two freeze points, and why rc matters more than "stable"

**VERSION-DEPENDENT (3.15, as the live example; the mechanism repeats every cycle).**

| Milestone | What it freezes | Verbatim source wording |
|---|---|---|
| **beta 1** (3.15: 2026-05-07) | the **feature set** | PEP 790: "3.15.0 beta 1: Thursday, 2026-05-07 (No new features beyond this point.)" |
| **rc1** (3.15: 2026-08-04) | the **ABI** | 3.15.0rc1: "There will be no ABI changes from this point forward in the 3.15 series"; "only reviewed code changes which are clear bug fixes are allowed between this release candidate and the final release" |
| **final** (3.15: 2026-10-01, est.) | nothing new — the rc plus bug fixes | PEP 790 schedule |

**The operational consequence, stated because it is routinely missed:** the rc1 announcement also
says "Any binary wheels built against Python 3.15.0 release candidates will work with future
versions of Python 3.15." Waiting for October before testing against 3.15 buys nothing except two
lost months. VERSION-DEPENDENT (3.15).

**A feature merged into CPython today ships in 3.16, not 3.15.** `main` is 3.16 and devguide states
it "is the only branch that accepts new features". A 3.15 feature request cannot be satisfied by
upstream at any speed. VERSION-DEPENDENT (3.15, 3.16).

### 2c. The support shape: bugfix inside a five-year total

**VERSION-DEPENDENT.** Total support is five years from the feature release, split into a bugfix
phase and a security phase. The bugfix phase was **extended from 18 to 24 months starting with
3.13**, which the schedule PEPs state directly:

- PEP 693 (3.12): "3.12 received bugfix updates approximately every 2 months for approximately 18
  months ... security updates (source only) will be released until 5 years after the release of
  3.12.0 final, so until approximately October 2028."
- PEP 719 (3.13): "3.13 will receive bugfix updates approximately every 2 months for approximately
  24 months. Around the time of the release of 3.15.0 final, the final 3.13 bugfix update will be
  released. After that ... security updates (source only) ... until approximately October 2029."
- PEP 745 (3.14): schedules bugfix releases through **3.14.14 (≈2027-10)**, described as "the final
  regular bugfix release with binary installers"; source-only security releases then run "until
  approximately October 2030".

**What this means for a project today:** 3.13 stops receiving bugfixes around October 2026 — far
nearer than its 2029 end-of-life, and the date that actually matters when deciding whether 3.13 is
still a comfortable production floor. VERSION-DEPENDENT (3.13).

### 2d. Numbering: no CalVer, no 3.26

**ESTABLISHED.** PEP 2026 ("Calendar versioning for Python", Python-Version 3.26) has status
**Rejected**. Numbering continues 3.15, 3.16, 3.17. An agent half-remembering the CalVer proposal
emits version numbers that do not exist: there is no Python 3.26 and no year-based scheme.

### 2e. Release-artefact verification changed at 3.14

**VERSION-DEPENDENT (3.14+).** Per PEP 761: "Python 3.14 and onwards no longer provides PGP
signatures for release artifacts. Instead, Sigstore is recommended for verifiers." A `gpg --verify`
step against a 3.14+ python.org tarball finds nothing to verify. Supply-chain gate design — what to
verify, where, and how failure behaves — is owned by `python_quality_gates_manifest.md`.

---

## 3. Choosing a minimum target

### 3a. What `requires-python` is

**ESTABLISHED** (PyPA core-metadata specification): `Requires-Python` is core metadata introduced in
metadata version 1.2, must be a version specifier per the PyPA version-specifiers spec, and "cannot
be followed by an environment marker". Installation tools "may look at this when picking which
version of a project to install". Three things follow:

- It is a **resolver exclusion filter** — it stops installation on interpreters outside the range.
- It is **not evidence of testing**. Nothing checks that CI ran on the versions it admits.
- It cannot be conditioned on platform, because environment markers are forbidden in the field.

### 3b. `requires-python` is not your test matrix

**OPEN — the project must state three separate numbers**, because one number cannot carry three
meanings: (1) the `requires-python` **floor**, (2) the **CI matrix** actually exercised, and (3) the
support **policy** that produced the floor (§3d). A spec that states only the floor has published a
promise it never tested. The CI matrix is owned by `python_quality_gates_manifest.md`; the metadata
declaration is owned by `python_module_boundaries_manifest.md`.

### 3c. Why the newest release is rarely the right floor

**VERSION-DEPENDENT.** Four facts, not a preference:

1. **The newest line may not be final.** On 2026-08-08 the newest feature line is 3.15 and it is at
   rc1 — testable and ABI-frozen, but not released. A floor of `>=3.15` today excludes every
   deployed interpreter.
2. **A floor excludes consumers; a CI matrix does not.** Raising the floor is a breaking change for
   anyone on an older interpreter; adding a newer version to the matrix costs only CI time.
3. **Ecosystem floors lag CPython.** Two data points verified this pass: pytest 9.1.1 declares
   `Requires-Python >= 3.10` with classifiers for 3.10–3.15; coverage.py 7.15.4 declares classifiers
   for 3.10–**3.16** plus `Programming Language :: Python :: Free Threading :: 3 - Stable`. (Tool
   selection and behaviour are owned by `python_testing_tooling_manifest.md`; only the declared
   interpreter ranges are hub facts.)
4. **A newer floor buys constructs, not correctness.** §4 is the ledger of exactly what each step up
   buys. If nothing in the ledger is load-bearing for the project, the step up buys nothing.

**Never publish an upper bound.** `requires-python = ">=3.11,<3.15"` or `"<4"` makes the
distribution uninstallable on the next interpreter, with no warning at publish time. ESTABLISHED
(the field is a resolver filter, so the exclusion is total and silent).

### 3d. The named support-window policies

**ESTABLISHED (the policies); OPEN (which one this project follows).** Two published windows
disagree, and they answer different questions:

| Policy | Window | Floor on 2026-08-08 | Source of authority |
|---|---|---|---|
| **CPython upstream support** | 5 years from the feature release | **3.10** (until ≈2026-10, then 3.11) | devguide + schedule PEPs |
| **SPEC 0** (Scientific Python, endorsed) | drop a Python version **36 months** after its release; drop a core package 24 months after its release | **3.12** | `scientific-python.org/specs/spec-0000/` |

SPEC 0's published drop schedule: 3.11 → Q4 2025 (already dropped), 3.12 → Q4 2026, 3.13 → Q4 2027,
3.14 → Q4 2028. A SPEC 0 follower today therefore supports 3.12, 3.13 and 3.14 — and drops 3.12
within months. SPEC 0 also notes that "core packages may or may not decide to provide bug fix
releases during the full 2 year period". ESTABLISHED.

**SPEC 0 supersedes NumPy's NEP 29** (42-month window vs SPEC 0's 36), so a project still citing NEP
29 is holding a *wider* window than the ecosystem it believes it tracks. SPEC 0's own numbers are
primary; the supersession relationship is **FLAGGED-SECONDARY** (NumPy issue discussion and
scientific-python discussions were the only evidence found). Neither policy binds a non-scientific
project: adopting one is an **OPEN** decision that must be recorded (§ open questions).

### 3e. Floor decision table — and the recommended default

**VERSION-DEPENDENT.** What each floor admits and costs. "Buys" lists only constructs verified in
§4; behaviour and usage guidance belong to the owning sibling files.

| Floor | Upstream status of the floor | Buys (native, no backport) | Costs / notes |
|---|---|---|---|
| `>=3.10` | security-only, **EOL ≈2026-10** | `X \| Y` unions, `TypeGuard`, `ParamSpec` | Below both policy windows within months; source-only interpreter; no `ExceptionGroup`, no `assert_never`, no `tomllib` |
| `>=3.11` | security-only until ≈2027-10 | `ExceptionGroup`/`except*`, `add_note`, `Never`/`assert_never`, `asyncio.TaskGroup`, `tomllib`, `Self`, `LiteralString`, `Required`/`NotRequired`, `TypeVarTuple`, `@dataclass_transform`, `int_max_str_digits` controls | Inside CPython's window; two versions below SPEC 0's floor |
| `>=3.12` | security-only until ≈2028-10 | PEP 695 generics + `type` statement, `sys.monitoring`, `**kwargs: Unpack[TypedDict]`, `@override` | Matches SPEC 0's floor today; SPEC 0 drops it Q4 2026. **The stated alternative to the default** — see below for what it forfeits |
| `>=3.13` | **bugfix until ≈2026-10**, then security | `@warnings.deprecated`, `ReadOnly`, `TypeIs`, type-parameter defaults; free-threaded build exists (experimental) | Loses 3.12 consumers. **The recommended default** — lowest floor still in the bugfix phase and the first with native `@warnings.deprecated`; see below |
| `>=3.14` | **bugfix**, EOL ≈2030-10 | PEP 649/749 deferred annotations + `annotationlib`, PEP 768 remote attach, `concurrent.interpreters`, `compression.zstd`, PEP 765 `finally` warning, `-X importtime=2`; free-threading **officially supported** | Excludes every older deployed interpreter; newest widely-installed line |
| `>=3.15` | **not released** until 2026-10-01 | UTF-8 default, `lazy` imports, builtin `sentinel`, `frozendict`, PEP 728 TypedDict, `TypeForm`, `profiling` package, frame pointers by default | Not a defensible floor before final; already a useful **CI matrix entry** |

#### The recommended default: `requires-python = ">=3.13"`

**The floor remains an OPEN policy choice — but it now has a starting point.** A project that has
not yet adopted a support policy (§3d) should write `>=3.13` and record why, rather than deferring
the question back to a table. The recommendation is **OPEN as policy** (this file cannot choose a
project's support obligations) and rests on two claims that are not matters of taste:

1. **Calendar. VERSION-DEPENDENT (2026-08-08).** Only **3.13 and 3.14 are in the bugfix phase**
   (§1a). 3.12 and below are security-only: source-only, no binary installers, and explicitly "no
   pre-set release cadence" (§1b). A floor of `>=3.12` therefore names as its *minimum* a branch
   whose upstream ships only crash and privilege-escalation fixes, and 3.10 leaves support
   altogether in ≈2 months.
2. **Behaviour. ESTABLISHED** (`docs.python.org`, per the Sources list). 3.13 is the first version
   on which three constructs the rest of this collection depends on are native:
   `@warnings.deprecated` ("Added in version 3.13: See PEP 702"); a callable *condition* for
   `BaseExceptionGroup.subgroup()` / `split()` ("Added in version 3.13: `condition` can be any
   callable which is not a type object"); and `traceback.TracebackException.exc_type_str` ("Added in
   version 3.13", with `exc_type` deprecated in the same version). Below 3.13, the
   deprecation-visibility contract owned by `python_module_boundaries_manifest.md` needs
   `typing_extensions.deprecated` instead of the stdlib decorator — a backport in the load-bearing
   position.

**Prefer `>=3.14` where nothing forces wider compatibility. VERSION-DEPENDENT (3.14).** It adds the
PEP 765 `SyntaxWarning` for `return` / `break` / `continue` leaving a `finally` block — which turns
that rule from a review convention into a diagnostic the compiler emits — plus PEP 768 remote attach
and PEP 649/749 deferred annotations. Its cost is the one in the table: it excludes every older
deployed interpreter.

**The alternative, stated rather than hidden: `>=3.12`. ESTABLISHED (SPEC 0, §3d).** This is the
right floor for a package inside the scientific ecosystem, because it is exactly what SPEC 0's
36-month window admits today, and a scientific dependant will not thank a library for being stricter
than the SPEC its neighbours follow. What it forfeits, precisely: the three 3.13 constructs above,
plus `ReadOnly`, `TypeIs` and type-parameter defaults (the table above) — so `@deprecated` comes
from `typing_extensions`, not `warnings`. It also inherits SPEC 0's own schedule, which drops 3.12
in Q4 2026: choosing `>=3.12` today is choosing to raise the floor again within months.

**A library that needs reach may legitimately go lower, and the cost is nameable.** `>=3.11` keeps
`ExceptionGroup` / `except*`, `add_note()`, `assert_never()`, `asyncio.TaskGroup` and `tomllib`, and
gives up PEP 695 generics, the `type` statement, `@override` and `sys.monitoring` — so the
low-overhead instrumentation in `python_runtime_diagnostics_manifest.md` is unavailable at the
floor. `>=3.10` additionally gives up `ExceptionGroup` and `tomllib` and sits below **both**
published policy windows within ≈2 months (§3d). Every step down is a set of backports to carry and
a set of §4 rows the project may no longer cite.

**What must be recorded either way. OPEN (§3b).** The floor is only one of the three numbers: write
down the floor, the CI matrix, and the policy that produced the floor. A `requires-python` value
with no recorded policy is not a decision — it is a default nobody owns, and the next agent will
move it.

---

## 4. Feature-availability ledger

The rest of the collection depends on these constructs existing. **Only rows verified this pass
appear.** "Since" is the CPython version that shipped the construct; behaviour and correct use are
owned by the file in the last column. **A security fix can add an API inside a bugfix release**, in
which case "Since" carries both numbers — the patch release that shipped it, and the feature line
whose docs record it (`os.path.ALLOW_MISSING` is the one such row here). Do not rely on the lower
number unless the floor excludes the earlier patch releases of that line:
`requires-python = ">=3.13"` admits 3.13.0, which does not have it.

### 4a. Language, runtime and stdlib constructs

| Construct | Since | PEP | Backport | Behaviour owned by |
|---|---|---|---|---|
| `X \| Y` union syntax | 3.10 | 604 | — | `python_typing_contract_manifest.md` |
| `ExceptionGroup` / `BaseExceptionGroup` / `except*` | **3.11** | 654 | `exceptiongroup` (named in `error_tracing_contract_manifest.md`; package version not re-verified this pass — OPEN) | `error_tracing_contract_manifest.md` |
| `BaseException.add_note()` / `__notes__` | **3.11** | 678 | as above (OPEN) | `error_tracing_contract_manifest.md` |
| `typing.Never`, `typing.assert_never()` | **3.11** | — | `typing_extensions` | `python_typing_contract_manifest.md` |
| `asyncio.TaskGroup` | **3.11** | — | — | `python_concurrency_determinism_manifest.md` |
| `tomllib` | **3.11** | 680 | third-party backport not re-verified this pass — OPEN | `python_module_boundaries_manifest.md` |
| `int_max_str_digits` controls (`sys.get_int_max_str_digits()` / `set_int_max_str_digits()`, `sys.flags.int_max_str_digits`) | **3.11**, backported to security branches | — | — | `python_language_hazards_manifest.md` |
| `sys.monitoring` (low-impact monitoring API) | **3.12** | 669 | — | `python_runtime_diagnostics_manifest.md` |
| PEP 695 generics: `class C[T]`, `def f[T]()`, `type` alias statement | **3.12** | 695 | — | `python_typing_contract_manifest.md` |
| `@warnings.deprecated` (**from `warnings`**, not `typing`) | **3.13** | 702 | `typing_extensions.deprecated` | `python_module_boundaries_manifest.md` |
| Free-threaded build exists (experimental) | **3.13** | 703 | — | §5, `python_concurrency_determinism_manifest.md` |
| Deferred annotation evaluation + `annotationlib` (`Format.VALUE` / `FORWARDREF` / `STRING`) | **3.14** | 649, 749 | — | `python_typing_contract_manifest.md` |
| Remote attach: `sys.remote_exec(pid, script_path)`, `python -m pdb -p PID` | **3.14** | 768 | — | `python_runtime_diagnostics_manifest.md` |
| `concurrent.interpreters`, `concurrent.futures.InterpreterPoolExecutor` | **3.14** | 734 | — | `python_concurrency_determinism_manifest.md` |
| `ProcessPoolExecutor.terminate_workers()` / `kill_workers()`; **default start method → `forkserver`** on Unix except macOS | **3.14** | — | — | `python_concurrency_determinism_manifest.md` |
| asyncio out-of-process introspection: `python -m asyncio ps PID`, `pstree PID`; in-process `asyncio.capture_call_graph()` / `print_call_graph()` | **3.14** | — | — | `python_runtime_diagnostics_manifest.md` |
| `faulthandler.enable(..., c_stack=True)` default and `faulthandler.dump_c_stack()` | **3.14** | — | — | `python_runtime_diagnostics_manifest.md` |
| `compression.zstd` plus the `compression` namespace over `gzip`/`bz2`/`lzma`/`zlib` | **3.14** | 784 | — | — |
| `SyntaxWarning` when `return`/`break`/`continue` leaves a `finally` block | **3.14** | 765 | — | `python_language_hazards_manifest.md` |
| Free-threading **officially supported** (still optional) | **3.14** | 779 | — | §5 |
| `os.path.realpath(strict=os.path.ALLOW_MISSING)` (shipped as part of the CVE-2025-4517 fix; the 3.13 docs say "Changed in version 3.13.4", the 3.14 docs say "Changed in version 3.14" and give the constant as "Added in version 3.14") | **3.13.4 / 3.14** | — | — | — |
| UTF-8 as the default encoding for files, stdio and pipes | **3.15** | 686 | — | `python_language_hazards_manifest.md` |
| `lazy` soft keyword for module-scope imports; `sys.set_lazy_imports()` family; `__lazy_modules__` | **3.15** | 810 | `__lazy_modules__` is inert (not an error) on older Pythons | `python_module_boundaries_manifest.md` |
| Builtin `sentinel(name, /, *, repr=None)` (`repr` is keyword-only) | **3.15** | 661 | `typing_extensions.sentinel` (4.16.0) | `python_typing_contract_manifest.md` |
| Builtin `frozendict` | **3.15** | 814 | — | `python_typing_contract_manifest.md` |
| Unpacking in comprehensions (`[*L for L in lists]`, `{**d for d in dicts}`) | **3.15** | 798 | — | — |
| `profiling` package: `profiling.tracing` (relocated `cProfile`) and `profiling.sampling` ("Tachyon") | **3.15** | 799 | — | `python_runtime_diagnostics_manifest.md` |
| Frame pointers in `BASECFLAGS` by default, propagated to extensions through `sysconfig` | **3.15** | 831 | — | §5, `python_runtime_diagnostics_manifest.md` |
| `sys.monitoring`: unwinding/exception events (`PY_THROW`, `PY_UNWIND`, `RAISE`, `EXCEPTION_HANDLED`, `RERAISE`) controllable per code object; returning `DISABLE` disables per code object instead of raising `ValueError` | **3.15** | — | — | `python_runtime_diagnostics_manifest.md` |
| `sys.abi_info` | **3.15** | — | — | §5 |
| `.start` package startup files plus the `site.StartupState` API | **3.15** | 829 | — | `python_module_boundaries_manifest.md` |
| `math.integer` | **3.15** | 791 | — | — |
| `pdb` uses the new interactive shell by default | **3.15** | — | — | `python_runtime_diagnostics_manifest.md` |
| C API: `PyBytesWriter`; interpreter guards and views, soft-deprecating `PyGILState_Ensure()` / `PyGILState_Release()` with no removal planned | **3.15** | 782, 788 | — | — |

### 4b. Typing PEP status ledger

**ESTABLISHED (statuses, verified against `peps.python.org` and its PEP API on 2026-08-08).** The
hub owns *status and version*; what each construct means, and which checker honours it at which
strictness, is owned by `python_typing_contract_manifest.md`.

| PEP | Construct | Status | Since |
|---|---|---|---|
| 484 | type hints, `TypeVar`/`Generic`, `Optional`, `# type: ignore`, `cast` | Final | 3.5 |
| 561 | `py.typed`; stub-only `-stubs` distributions | Final | 3.7 |
| 544 | `Protocol`, `@runtime_checkable` | Final | 3.8 |
| 585 | builtin generics (`list[int]`) | Final | 3.9 |
| 604 | `X \| Y` unions | Final | 3.10 |
| 612 | `ParamSpec`, `Concatenate` | Final | 3.10 |
| 647 | `TypeGuard` (narrows on True only) | Final | 3.10 |
| 646 | `TypeVarTuple`, `Unpack` | Final | 3.11 |
| 655 | `Required` / `NotRequired` | Final | 3.11 |
| 673 | `Self` | Final | 3.11 |
| 675 | `LiteralString` | Final | 3.11 |
| 681 | `@dataclass_transform` | Final | 3.11 |
| 692 | `**kwargs: Unpack[TypedDict]` | Final | 3.12 |
| 695 | type-parameter syntax, `type` statement | Final | 3.12 |
| 698 | `@override` | Final | 3.12 |
| 696 | type-parameter defaults | Final | 3.13 |
| 702 | `@warnings.deprecated` | Final | 3.13 |
| 705 | `ReadOnly[T]` for TypedDict items | Final | 3.13 |
| 742 | `TypeIs` (narrows in both branches) | Final | 3.13 |
| 649 / 749 | deferred annotations, `annotationlib` | Final | 3.14 |
| 661 | builtin `sentinel` | Final | **3.15** |
| 728 | `TypedDict(closed=True)` / `extra_items=T` | Final | **3.15** |
| 747 | `typing.TypeForm` | Final | **3.15** |
| 800 | `@typing.disjoint_base` | Final | **3.15** |
| 563 | postponed (string) annotations | **Superseded** | — |
| 677 | callable type syntax `(int) -> str` | **Rejected** | — |
| 724, 727 | — | **Withdrawn** | — |
| 729 | Typing Council governance | **Active** (Process) | — |

**PEP 728 runtime detail the hub owns because it is version-bound:** `extra_items=Never` is
equivalent to `closed=True` (the latter preferred); extra items are always non-required regardless
of `total=`; combining `extra_items` with `Required[]` / `NotRequired[]` is an error; introspection
is `__extra_items__` (holding `typing.NoExtraItems` when unset) and `__closed__` (holding `None`
when unset), both reflecting only what was passed and ignoring inheritance. VERSION-DEPENDENT
(3.15).

**PEP 661 runtime detail, same reason:** two `sentinel()` calls with the same name return **distinct
objects**; `copy.copy()` and `copy.deepcopy()` return the same object; sentinels importable by
module and name survive pickling while locals do not; sentinels are truthy and usable in `|` type
expressions (`value: int | MISSING = MISSING`). VERSION-DEPENDENT (3.15).

**`from __future__ import annotations` and PEP 649 are mutually exclusive**, not additive: with the
`__future__` import present, annotations remain strings and PEP 649's lazy model does not apply, so
leaving the import in a 3.14+ file forfeits the feature. PEP 563 is formally **Superseded**; the
`__future__` import is deprecated but its behaviour is unchanged, and removal "will not happen until
after Python 3.13 reaches its end of life in 2029". VERSION-DEPENDENT (3.14+).

**Backport channel.** `typing_extensions` 4.16.0 (2026-07-02) backports the 3.15 typing additions to
older runtimes, including `@typing_extensions.disjoint_base` (added 4.15.0) and
`typing_extensions.sentinel`; `typing_extensions.Sentinel` is now a soft-deprecated alias "following
the name that has been adopted for `builtins.sentinel` on Python 3.15", and the default repr of
`X = sentinel("X")` changed from `<X>` to `X`. VERSION-DEPENDENT (typing_extensions 4.16.0).

### 4c. Packaging and metadata standards — status only

**ESTABLISHED (statuses verified 2026-08-08 against the canonical `python/peps` sources and the
packaging PEP index).** Semantics, file layout and tool invocation are owned by
`python_module_boundaries_manifest.md`; this table exists so no agent has to guess whether a
standard is real.

| PEP | What it fixes | Status |
|---|---|---|
| 517 / 518 | `[build-system]` (`requires`, `build-backend`, `backend-path`); the existence of `pyproject.toml` | Final |
| 621 | the `[project]` table | Final |
| 639 | `License-Expression` + `license-files` (requires core metadata 2.4) | Final |
| 660 | editable-install hooks (`build_editable`, …) — all **optional** | Final |
| 735 | `[dependency-groups]` (never ships in metadata) | Final |
| 751 | `pylock.toml` lock-file format | Final (resolution 2025-03-31) |
| 740 | index attestations (in-toto statement bound to the file's SHA-256 digest) | Final |
| 770 | `.dist-info/sboms/`, deliberately with no new metadata field | Final |
| 723 | inline script metadata (`# /// script`) | Final |
| 508 / 440 / 427 | dependency specifiers; version identification; wheel 1.0 | Final |
| 420 | implicit namespace packages — created by the **absence** of `__init__.py` | Final (3.3) |
| 562 | module `__getattr__` / `__dir__` | Final (3.7) |
| 794 | `Import-Name` / `Import-Namespace` metadata (2.5) | **Accepted** (2025-09-05) |
| 808 | static values in dynamic metadata; drove core metadata **2.6** | **Accepted** (2026-05-19) |
| 752 | repository **name-prefix** reservation — unrelated to PEP 420 import namespaces | **Accepted** (2026-06-29) |
| 771 | `default-optional-dependency-keys` / `Default-Extra` | **Draft** |
| 777 | `Wheel-Version`, `.whlx` | **Draft** |
| 817 / 825 | wheel variants | **Draft** |
| 819 | `METADATA.json` / `WHEEL.json` | **Draft** |
| 694 / 710 / 807 / 725 / 780 / 804 / 755 | upload API 2.0; installed-package provenance; index Trusted Publishing; external dependencies; ABI-feature markers; external dependency registry; PyPI namespace policy | **Draft** |
| 491 / 778 | wheel 1.9; symlinks in wheels | **Deferred** |

### 4d. The hallucination set — PEPs that describe nothing available

**ESTABLISHED (status); OPEN (whether they ever ship).** These are the PEPs most likely to be
recalled as features because they read like natural extensions. None is available in any released
Python. Do not emit their syntax.

| PEP | Would add | Status |
|---|---|---|
| 718 | subscriptable functions (`f[int](...)`) | Draft, targeted 3.15 |
| 764 | inline TypedDicts | Draft, targeted 3.15 |
| 746 | type-checking `Annotated` metadata | Draft, targeted 3.15 |
| 767 | annotating read-only attributes | Draft, targeted 3.15 |
| 781 | `TYPE_CHECKING` as a builtin constant | Draft, targeted 3.15 |
| 821 | unpacking TypedDicts in `Callable` | Draft, targeted 3.15 |
| 827 | type manipulation | Draft, targeted 3.16 |
| 835 | shorthand syntax for `Annotated` metadata | Draft, targeted 3.16 |
| 744 | JIT compilation | **Draft** — §5d |
| 2026 | calendar versioning | **Rejected** — §2d |

---

## 5. Build variants — one version number, several interpreters

A CPython version does not determine the interpreter's behaviour, ABI or performance profile. Four
build axes vary independently, and three of them are invisible unless you look.

### 5a. Free-threaded builds: the phase model

**ESTABLISHED / VERSION-DEPENDENT.** PEP 703 ("Making the Global Interpreter Lock Optional in
CPython") is **Final** with Python-Version 3.13. Its build flag is `--disable-gil`, which per the
configure docs "Defines the `Py_GIL_DISABLED` macro and adds `\"t\"` to `sys.abiflags`". PEP 703
defines a three-phase rollout and states the free-threaded build "will not be ABI compatible with
the standard CPython build or with the stable ABI due to changes to the Python object header needed
to support biased reference counting".

| Phase | Meaning | Status |
|---|---|---|
| **Phase I** | experimental, two ABIs shipped | **3.13** — the 3.13 What's New reads "CPython now has experimental support for running in a free-threaded mode ... This is an experimental feature and therefore is not enabled by default"; `sys.version` and `python -VV` contain "experimental free-threading build" |
| **Phase II** | supported, still optional | **3.14** — PEP 779 ("Criteria for supported status for free-threaded Python", **Final**, accepted 2025-06-16) sets the bar at ≤15% single-threaded slowdown (≈10% measured at acceptance) and ≤20% higher memory on the pyperformance geometric mean; the 3.14 highlight line is "PEP 779: Free-threaded Python is officially supported" |
| **Phase III** | free-threading is the default build | **not scheduled** — no PEP defines Phase III and no version is committed. **OPEN** |

"Officially supported" still means **optional**: the GIL-enabled build remains the normal build.
PEP 779's own definition is "the design is finalised, the APIs are usable and stable, and we're
satisfied the performance and complexity cost is not prohibitive." VERSION-DEPENDENT (3.14).

**Single-threaded overhead — always quote the platform.** Two current primary figures disagree in
shape, not in kind: the 3.14 What's New says "The performance penalty on single-threaded code in
free-threaded mode is now roughly 5-10%, depending on the platform and C compiler used", while the
free-threading HOWTO gives about **1% on macOS aarch64** and about **8% on x86-64 Linux**
(pyperformance geometric mean). A bare "5-10%" or "1%" is a misquote of one of them.
VERSION-DEPENDENT (3.14).

### 5b. Detecting which build you are on

**VERSION-DEPENDENT (3.13+ unless noted).** Four different questions, four different APIs.
Conflating them produces wheel-selection bugs.

| Question | Correct surface | Notes |
|---|---|---|
| Was this interpreter **built** free-threaded? | `sysconfig.get_config_var("Py_GIL_DISABLED") == 1` | The build-time answer; use it for wheel and packaging decisions |
| Is the GIL **off right now**? | `sys._is_gil_enabled()` | **Private API**, reports *runtime* state — not build type |
| Which ABI is this? | `sys.abiflags` contains `t`; `python -VV` contains "free-threading build"; the interpreter installs with a `t` suffix (e.g. `python3.14t`) | |
| Full ABI description | `sys.abi_info` | **3.15+** only |
| How was it configured? | `python -m sysconfig` | Also the check for `HAVE_PERF_TRAMPOLINE` and `no-omit-frame-pointer` (§6) |

**Runtime toggle:** `-X gil=0|1` and `PYTHON_GIL=0|1` (both added 3.13) select the GIL at startup;
`-X gil=0` requires a `--disable-gil` build. VERSION-DEPENDENT (3.13+).

**Wheel tags.** The free-threaded ABI is separate: the verified tags are `cp314t` / `cp315t` (the
`cp31Xt` pattern; earlier free-threaded tags were not re-verified this pass — OPEN), and
`abi3` wheels do not apply to it. PEP 803 ("`abi3t`: Stable ABI for Free-Threaded Builds") is
**Final** with Python-Version 3.15 — extensions define `Py_TARGET_ABI3T=<version>` and declare the
compressed tag set `abi3.abi3t` — but the 3.15 What's New warns that "build tools like Setuptools,
meson-python, scikit-build-core, and Maturin do not support `abi3t`" at the time of writing, and
advises shipping `abi3` plus a version-specific `cp315t` wheel until tooling catches up. Migration
also requires PEP 697 APIs (negative `basicsize`, `PyObject_GetTypeData()`) instead of embedding
`PyObject`, plus the PEP 793 `PyModExport_*` export hook with the PEP 820 `PySlot` structure,
because `PyObject`, `PyVarObject` and `PyModuleDef` become opaque, `PyObject_HEAD` is unusable, and
`PyModuleDef` can no longer be statically allocated. VERSION-DEPENDENT (3.15).

### 5c. The silent GIL re-enablement

**VERSION-DEPENDENT (3.13+).** Importing a C extension that does not declare free-threading support
— via the `Py_mod_gil` slot or `PyUnstable_Module_SetGIL()` — **re-enables the GIL automatically**,
with a warning printed. The process keeps running; it simply is no longer free-threaded. A
"free-threaded" benchmark that shows no scaling is frequently just this. The only reliable check is
`sys._is_gil_enabled()` asserted at runtime, inside the process being measured.

Two further free-threading-only switches, both added in **3.14**:

- `-X tlbc=0|1` / `PYTHON_TLBC` (free-threaded builds only, default 1) controls **thread-local
  bytecode**; disabling it lowers memory at the cost of specialisation.
- `-X context_aware_warnings=0|1` and `-X thread_inherit_context=0|1` (with
  `PYTHON_CONTEXT_AWARE_WARNINGS` and `PYTHON_THREAD_INHERIT_CONTEXT`) **default to 1 on
  free-threaded builds and 0 on GIL builds**. Warning-filter state therefore becomes a `ContextVar`
  on free-threaded builds, which changes how `warnings.catch_warnings()` behaves across threads — a
  real source of flaky warning assertions.

Free-threading *hazards* (cross-thread `frame.f_locals`, shared iterators, container locking,
immortal objects, memory overhead) are behaviour, not version status, and are owned by
`python_concurrency_determinism_manifest.md`.

### 5d. The experimental JIT

**ESTABLISHED (status) / VERSION-DEPENDENT (3.13+).** PEP 744 ("JIT Compilation") is still status
**Draft** with Python-Version 3.13. It states "The JIT is currently not part of the default build
configuration, and it is likely to remain that way for the foreseeable future" and that the JIT "is
about as fast as the existing specializing interpreter on most platforms", with roughly 10–20%
higher memory use. **Do not cite PEP 744 as an accepted commitment to a default-on JIT.**

| Surface | Value | Notes |
|---|---|---|
| Build flag | `--enable-experimental-jit=[no\|yes\|yes-off\|interpreter]` (3.13, default `no`; bare flag means `=yes`) | `yes` = built enabled, disable with `PYTHON_JIT=0`; `yes-off` = built disabled, enable with `PYTHON_JIT=1`; `interpreter` = the tier-2 "JIT interpreter", useful only for debugging the JIT itself |
| Windows build | `PCbuild/build.bat --experimental-jit`, `--experimental-jit-interpreter` | |
| Runtime switch | `PYTHON_JIT=0\|1` (3.13) | **There is no `-X jit`.** `PYTHON_JIT` does nothing unless the interpreter was built with `--enable-experimental-jit` |
| 3.15 performance | "8-9% geometric mean performance improvement on x86-64 Linux **over the standard interpreter**, and 12-13% speedup on AArch64 macOS **over the tail-calling interpreter**" | From the 3.15.0rc1 announcement — **two different baselines**, so the two figures are not comparable to each other (§5e is the tail-calling interpreter). VERSION-DEPENDENT (3.15) |

### 5e. The tail-call interpreter

**VERSION-DEPENDENT (3.14+).** A separate, orthogonal mechanism from the JIT.
`--with-tail-call-interp` (added 3.14) "requires a C compiler with proper tail call support, and the
`preserve_none` calling convention. For example, Clang 19 and newer supports this feature", targets
x86-64 and AArch64, and PGO (`--enable-optimizations`) is "highly recommended". CPython documents "a
geometric mean of 3-5% faster on the standard `pyperformance` benchmark suite". A GCC toolchain
cannot produce this build, so "enable the tail-call interpreter" is not portable advice.

The widely circulated **10–15%** figure from early 2025 was inflated by an LLVM 19 codegen
regression in the *baseline* build rather than by the tail-call interpreter itself; the corrected
geometric mean is the 3–5% now in the CPython docs. **FLAGGED-SECONDARY** for the explanation
(blog.nelhage.com, fidget-spinner.github.io, lwn.net); the CPython docs' 3–5% is the primary anchor.
VERSION-DEPENDENT (3.14).

### 5f. What the official binaries actually are

**VERSION-DEPENDENT.** The shipped interpreter is not a neutral build, and this is where
version-to-version comparisons break:

- **3.14 macOS and Windows** official binaries "include an experimental JIT compiler" per the 3.14.7
  release page. Whether they were built `yes` or `yes-off` — that is, whether the JIT is live
  without `PYTHON_JIT=1` — **is not stated**. **OPEN**: test both settings rather than assuming.
- **3.15 Windows 64-bit** official binaries use the **tail-calling interpreter**, so the shipped
  Windows interpreter changes its C-level dispatch shape between 3.14 and 3.15.
- **3.15 macOS** official binaries install free-threading support by default (per the 3.15.0rc1
  release page).
- **3.15** turns frame pointers on by default (PEP 831, **Final**, 3.15): `-fno-omit-frame-pointer`
  and `-mno-omit-leaf-frame-pointer` join `BASECFLAGS` so third-party C extensions inherit them
  through `sysconfig`, with `--without-frame-pointers` as the opt-out (that option exists in 3.15
  and not in 3.14). Measured cost: 0.5% on Apple M2, 0.2–2.3% on AArch64, 1.5–1.9% on x86-64.

### 5g. Debug and trace builds

**ESTABLISHED.** `--with-pydebug` adds `d` to `sys.abiflags`, adds `sys.gettotalrefcount()`,
installs the allocator debug hooks, and **shows all warnings** (the default warning-filter list is
empty in a debug build — §6c). `--with-trace-refs` is required by `PYTHONDUMPREFS` (which carries no
version note on the cmdline page; it predates 3.11) and `PYTHONDUMPREFSFILE` (3.11), and adds
`sys.getobjects()`; since **3.13** the trace-refs build is ABI compatible with both release and
debug
builds. `-X showrefcount` (3.4) works on debug builds only.

### 5h. The build-configuration stamp

**OPEN — the project must decide where this is recorded, but the content is not a matter of taste.**
Because §5a–§5f each change instruction counts, stack shape or ABI, a performance or crash artefact
without its build configuration is not comparable to any other artefact. The minimum stamp, all from
verified surfaces above:

```
sys.version                                     # includes build markers, e.g. free-threading build
sys.version_info, sys.abiflags                  # 't' free-threaded, 'd' debug
sys._is_gil_enabled()                           # runtime GIL state (private API)
sysconfig.get_config_var("Py_GIL_DISABLED")     # build-time free-threading
os.environ.get("PYTHON_JIT")                    # JIT runtime toggle (no -X jit exists)
python -m sysconfig | grep -E "no-omit-frame-pointer|HAVE_PERF_TRAMPOLINE|TAIL_CALL"
sys.abi_info                                    # 3.15+
```

Profiling and measurement methodology is owned by `python_runtime_diagnostics_manifest.md`; what to
gate on a measurement is owned by `python_quality_gates_manifest.md`.

---

## 6. The interpreter switchboard

### 6a. `-X` options and `PYTHON*` variables that matter

**ESTABLISHED (the switch exists and does what is stated) / VERSION-DEPENDENT (the "added"
column).** Confirmed against `docs.python.org/3/using/cmdline.html`. Switches marked **[diag]** are
diagnosis instruments whose *use* is owned by `python_runtime_diagnostics_manifest.md`; this table
is the inventory and the version gate, not the method.

| `-X` option | Environment variable | Added | What it actually turns on |
|---|---|---|---|
| `-X dev` | `PYTHONDEVMODE=1` | — | Development Mode: the `default` warning filter, allocator debug hooks, `faulthandler`, asyncio debug mode, `open()`/`encode()`/`decode()` argument validation, `io.IOBase` destructor exception logging, `sys.flags.dev_mode = True` (§6b) |
| `-X faulthandler` | `PYTHONFAULTHANDLER` | — | **[diag]** Installs handlers for `SIGSEGV`, `SIGFPE`, `SIGABRT`, `SIGBUS`, `SIGILL` at startup |
| `-X tracemalloc=NFRAME` | `PYTHONTRACEMALLOC=NFRAME` | — | **[diag]** Allocation tracing from interpreter start with an NFRAME-deep traceback. Without it, tracemalloc-dependent warnings carry no allocation site |
| `-X importtime`, `-X importtime=2` | `PYTHONPROFILEIMPORTTIME` (`1` / `2`) | `=2` in **3.14** | Per-import timing; `=2` also traces already-cached imports |
| `-X perf` | `PYTHONPERFSUPPORT=1` | 3.12 | **[diag]** Linux `perf` trampoline so Python frames appear in `perf` output. Precedence: `sys` functions > `-X` > env var. In-process API: `sys.activate_stack_trampoline("perf")`, `sys.deactivate_stack_trampoline()`, `sys.is_stack_trampoline_active()`. Linux-only, selected architectures — verify with `python -m sysconfig \| grep HAVE_PERF_TRAMPOLINE` |
| `-X perf_jit` | `PYTHON_PERF_JIT_SUPPORT=1` | 3.13 | **[diag]** Emits unwind information on the fly for `perf record --call-graph dwarf` plus a `perf inject --jit` pass; needs perf v6.8+ (or v6.7.2+); higher overhead and slower post-processing |
| `-X int_max_str_digits=N` | `PYTHONINTMAXSTRDIGITS=N` | 3.11 | Integer↔string conversion limit; `0` disables (§6d) |
| `-X no_debug_ranges` | `PYTHON_NODEBUGRANGES` | 3.11 | **Drops the fine-grained location table** from code objects and `.pyc` files — the data that draws the `^^^^` carets (§6d) |
| `-X frozen_modules=on\|off` | `PYTHON_FROZEN_MODULES` | 3.11 / 3.13 | Whether frozen stdlib modules are used; default **on** in release builds, **off** in debug builds |
| `-X cpu_count=n` | `PYTHON_CPU_COUNT` | 3.13 | Overrides `os.cpu_count()` and `os.process_cpu_count()` |
| `-X pycache_prefix=PATH` | `PYTHONPYCACHEPREFIX` | 3.8 | Writes `.pyc` files under PATH instead of `__pycache__` |
| `-X warn_default_encoding` | `PYTHONWARNDEFAULTENCODING` | 3.10 | Emits `EncodingWarning` where an implicit locale encoding is used — the early-warning switch for the 3.15 UTF-8 flip |
| `-X utf8=0\|1` | `PYTHONUTF8=0\|1` | 3.7 | UTF-8 mode. `-X utf8=0` / `PYTHONUTF8=0` is the documented **revert** path for PEP 686 in 3.15; `encoding="locale"` and `locale.getencoding()` remain available |
| `-X gil=0\|1` | `PYTHON_GIL=0\|1` | 3.13 | Selects the GIL at startup; `0` requires a `--disable-gil` build (§5b) |
| `-X tlbc=0\|1` | `PYTHON_TLBC` | 3.14 | Thread-local bytecode; free-threaded builds only, default 1 |
| `-X context_aware_warnings=0\|1` | `PYTHON_CONTEXT_AWARE_WARNINGS` | 3.14 | Warning state as a `ContextVar`; **default 1 free-threaded, 0 GIL** |
| `-X thread_inherit_context=0\|1` | `PYTHON_THREAD_INHERIT_CONTEXT` | 3.14 | New threads inherit the creating context; same split defaults |
| `-X disable_remote_debug` | `PYTHON_DISABLE_REMOTE_DEBUG` | 3.14 | **[diag]** Disables the PEP 768 remote-attach interface for this process. Compiled in by default (`Py_REMOTE_DEBUG`); removable at build time with `--without-remote-debug` |
| `-X lazy_imports=normal\|all\|none` | `PYTHON_LAZY_IMPORTS` | **3.15** | PEP 810 lazy-import mode: `normal` honours the `lazy` keyword (default), `all` makes imports lazy where possible, `none` forces everything eager |
| `-X showrefcount` | — | 3.4 | Debug builds only |
| `-X presite=pkg.mod` | `PYTHON_PRESITE` | 3.13 | Imports a module before `site`; debug builds only |
| `-P` | `PYTHONSAFEPATH` | 3.11 | Does not prepend the script directory / cwd to `sys.path` |
| — | `PYTHONHASHSEED` | — | Integer 0–4294967295 (default `random`); `0` disables hash randomisation |
| — | `PYTHONMALLOC` | — | `debug` enables allocator debug hooks; `default` turns them off again even under `-X dev` (§6b) |
| — | `PYTHONWARNINGS`, `-W` | — | Warning filters, `action:message:category:module:lineno`; later filters take precedence; `-W error` raises (§6c) |
| — | `PYTHONBREAKPOINT` | 3.7 | Target of `breakpoint()`; defaults to `pdb.set_trace`; empty or `"0"` makes `breakpoint()` a no-op |
| — | `PYTHON_COLORS`, `NO_COLOR`, `FORCE_COLOR` | — | Colour output control |
| — | `PYTHON_BASIC_REPL` | 3.13 | Falls back from PyREPL to the basic REPL |
| — | `PYTHONDUMPREFS` (no version note; predates 3.11), `PYTHONDUMPREFSFILE` (3.11) | — | Requires a `--with-trace-refs` build (§5g) |
| — | `PYTHON_JIT=0\|1` | 3.13 | Only if built with `--enable-experimental-jit`; **no `-X jit` exists** (§5d) |

### 6b. What `-X dev` does — and the two things it does not

**ESTABLISHED** (`docs.python.org/3/library/devmode.html`). Development Mode enables exactly: the
`default` warning filter (surfacing `DeprecationWarning`, `ImportWarning`,
`PendingDeprecationWarning` and `ResourceWarning`, equivalent to `-W default`); the debug
memory-allocator hooks (equivalent to `PYTHONMALLOC=debug`, catching buffer under/overflow,
allocator-API violations and unsafe GIL usage); `faulthandler` (equivalent to `-X faulthandler`);
asyncio debug mode (equivalent to `PYTHONASYNCIODEBUG=1`); validation of the `encoding` and `errors`
arguments of `open()`, `str.encode()` and `bytes.decode()`; logging of exceptions raised in the
`io.IOBase` destructor; and it sets `sys.flags.dev_mode` to True.

It explicitly does **not**:

- **enable `tracemalloc`** — the overhead is judged too large. The `ResourceWarning` dev mode
  surfaces literally says "Enable tracemalloc to get the object allocation traceback"; you must add
  `-X tracemalloc=N` yourself.
- **protect `assert` from `-O`**, and it does not change `__debug__`. `-O` still strips assertions.

**Escape hatch:** `PYTHONMALLOC=default` alongside dev mode keeps dev mode while turning the
allocator debug hooks back off — the documented remedy when the hooks are too slow. ESTABLISHED.

### 6c. Default warning filters — why the removal calendar is silent

**ESTABLISHED** (`docs.python.org/3/library/warnings.html`). In a **release** build the default
filters are exactly, in precedence order:

```
default::DeprecationWarning:__main__
ignore::DeprecationWarning
ignore::PendingDeprecationWarning
ignore::ImportWarning
ignore::ResourceWarning
```

"In a debug build, the list of default warning filters is empty", so a debug interpreter shows
everything. The consequence that matters for §7: a library can add a deprecation warning, its own
test can assert the warning is raised, both pass, **and no user ever sees it**. Making deprecations
visible is a CI decision — the switches are `-W error::DeprecationWarning`, `-X dev`, and the test
runner's own filter configuration — owned by `python_quality_gates_manifest.md` and
`python_testing_tooling_manifest.md`. Which categories a project *emits* is owned by
`logging_observability_manifest.md`.

### 6d. Switches that change program behaviour, not just reporting

**VERSION-DEPENDENT.** Three switches in §6a are not diagnostics and must be set deliberately:

- **`-X int_max_str_digits` / `PYTHONINTMAXSTRDIGITS` (3.11+).** Default **4300**
  (`sys.int_info.default_max_str_digits`); minimum non-zero setting **640**
  (`sys.int_info.str_digits_check_threshold`); `0` disables the limit. Exceeding it raises
  **`ValueError`**, not `OverflowError`: `int('1'*5000)` produces `ValueError: Exceeds the limit
  (4300 digits) for integer string conversion: value has 5000 digits; use
  sys.set_int_max_str_digits() to increase the limit`. It applies to `int(str)`, `str(int)` and
  `repr(int)`; `hex()`, `oct()` and `bin()` are unaffected. (Constant values read from a live
  interpreter's `sys.int_info`; the fields are documented in `library/sys.html`.)
- **`-X no_debug_ranges` (3.11+).** Shrinks `.pyc` files by dropping the fine-grained location
  table — exactly the data that draws the `^^^^` carets in a traceback. Never set it in an
  environment you intend to debug.
- **`-X lazy_imports` (3.15).** Changes *when* imports execute, so it changes when import errors and
  import side effects appear. `all` is a global behaviour change, not an optimisation flag; PEP
  810's documented consequences (errors and side effects deferred to first use, the module absent
  from `sys.modules` until reification, a bound name that is a `types.LazyImportType` object until
  then) are owned as behaviour by `python_module_boundaries_manifest.md`.

---

## 7. Deprecation and removal calendar

### 7a. The policy that governs every row below

**ESTABLISHED.** PEP 387 ("Backwards Compatibility Policy", status **Active**) requires a
deprecation warning to "appear in at least two minor Python versions of the same major version"
before removal, prefers a five-year window (warn in 3.10, remove in 3.15), names
`DeprecationWarning` as the usual category with `PendingDeprecationWarning` reserved for long
coexistence, and defines **soft deprecation**: "A soft deprecation can be used when using an API
which should no longer be used to write new code, but it remains safe to continue using it in
existing code." **A soft deprecation schedules no removal.**

### 7b. Already removed

**VERSION-DEPENDENT.** PEP 594 ("Removing dead batteries from the standard library") is **Final**.

| Version | Removed |
|---|---|
| 3.12 | `asynchat`, `asyncore`, `smtpd` (PEP 594) |
| 3.13 | The 19 PEP 594 modules deprecated in 3.11: `aifc`, `audioop`, `cgi`, `cgitb`, `chunk`, `crypt`, `imghdr`, `mailcap`, `msilib`, `nis`, `nntplib`, `ossaudiodev`, `pipes`, `sndhdr`, `spwd`, `sunau`, `telnetlib`, `uu`, `xdrlib`. Also `2to3` and `lib2to3`, `tkinter.tix`, `locale.resetlocale()`, the `typing.io` and `typing.re` namespaces, `configparser.LegacyInterpolation`, `importlib.metadata.EntryPoint.__getitem__()`; chained `classmethod` descriptors stopped wrapping other descriptors |
| 3.14 | `argparse` `nargs=`/`required=` on mutually exclusive groups, `ast.PyCF_ALLOW_TOP_LEVEL_AWAIT`, `importlib.abc.ResourceReader`, `pkgutil.find_loader()`, `pty.spawn()`, sqlite3 implicit named-parameter binding, plus batches of deprecated `asyncio` and `email` APIs — **consult the "Removed" section of the 3.14 What's New for the exact list rather than reconstructing it** |
| **3.15** | `module.__cached__` and `module.__package__`; `ctypes.SetPointerType()`; `http.server.CGIHTTPRequestHandler` and `python -m http.server --cgi`; `importlib`'s `load_module()`; `pathlib.PurePath.is_reserved()`; `platform.java_ver()`; the `check_home` argument of `sysconfig.is_python_build()`; arguments to `threading.RLock()`; `types.CodeType.co_lnotab`; the undocumented keyword-argument syntax of `typing.NamedTuple`; the `typing.TypedDict` functional syntax with no fields or with `None`; `typing.no_type_check_decorator`; the `wave` mark methods (`getmark`, `setmark`, `getmarkers`); `zipimport.zipimporter.load_module()`; and **`sre_compile`, `sre_constants`, `sre_parse`** |

The 3.15 docs contain **no *Python-level* "Pending removal in Python 3.15" section**, and the 3.15
What's New "Removed" section has subsections for `ast`, `collections.abc`, `ctypes`, `datetime`,
`glob`, `http.server`, `importlib.resources`, `pathlib`, `platform`, `sre_*`, `sysconfig`,
`threading`, `types`, `typing`, `wave` and `zipimport` — everything the 3.14 docs listed as pending
for 3.15 has landed. **The C API half of the same page still has one**, so a C extension can be
depending on a name that is already scheduled to go: `PyImport_ImportModuleNoBlock()` (use
`PyImport_ImportModule()`), `PyWeakref_GetObject()` / `PyWeakref_GET_OBJECT()` (use
`PyWeakref_GetRef()`), `PyUnicode_AsDecodedObject()` / `PyUnicode_AsDecodedUnicode()` (use
`PyCodec_Decode()`), `PyUnicode_AsEncodedObject()` / `PyUnicode_AsEncodedUnicode()` (use
`PyCodec_Encode()`), the 3.13-deprecated initialization getters (`Py_GetPath()`, `Py_GetPrefix()`,
`Py_GetExecPrefix()`, `Py_GetProgramFullPath()`, `Py_GetProgramName()`, `Py_GetPythonHome()` — use
`PyConfig_Get()`), the 3.11-deprecated initialization setters (`PySys_SetArgv()`,
`PySys_SetArgvEx()`, `Py_SetProgramName()`, `Py_SetPythonHome()`, `PySys_ResetWarnOptions()` — use
`Py_InitializeFromConfig()` with `PyConfig`), and the global configuration variables. The C API is
otherwise out of this collection's scope; it is named here so the negative above is not read as
"nothing is pending removal in 3.15". VERSION-DEPENDENT (3.15).

### 7c. A private replacement is not a migration target

**VERSION-DEPENDENT (3.15).** `sre_compile`, `sre_constants` and `sre_parse` (deprecated in 3.11)
are removed in 3.15. Their replacements — `re._compiler`, `re._constants`, `re._parser` — are
**private and undocumented**. There is therefore *no supported migration target*, only a private
one. The rule this establishes, and it generalises: **when the only replacement for a removed public
API is a private one, the correct response is to remove the dependency, not to depend on the private
name.** Regex introspection and property-based generators that reach into `sre_*` are the usual
casualties.

### 7d. Pending removals, by enforcing version

**VERSION-DEPENDENT** (`docs.python.org/3.15/deprecations/index.html`). These are the page's
**Python-level** buckets, which run 3.16 → 3.20; the same page carries a separate set of **C API**
buckets starting at 3.15 (§7b).

| Removed in | What goes |
|---|---|
| **3.16** | Setting `__loader__` without `__spec__.loader`; the `array` `'u'` format code (`wchar_t`); `asyncio.iscoroutinefunction()`; **the entire event-loop-policy API** (`AbstractEventLoopPolicy`, `DefaultEventLoopPolicy`, `WindowsSelectorEventLoopPolicy`, `WindowsProactorEventLoopPolicy`, `get_event_loop_policy()`, `set_event_loop_policy()`); bitwise inversion of booleans (`~True`, `~False`); `functools.reduce()` with `function`/`sequence` as keywords; custom logging handlers taking a `strm` argument; `mimetypes.MimeTypes.add_type()` with undotted extensions; `shutil.ExecError`; `symtable.Class.get_methods()`; `sys._enablelegacywindowsfsencoding()`; `sysconfig.expand_makefile_vars()`; the `tarfile.TarFile.tarfile` attribute |
| **3.17** | `collections.abc.ByteString`, `typing.ByteString`, `typing._UnionGenericAlias`; **the `profile` module** (use `profiling.tracing`); `webbrowser.MacOSXOSAScript`; `datetime.strptime()` with `%e` and no year; non-ASCII names in `encodings.normalize_encoding()`; the `tkinter.Variable` trace methods (`trace_variable()`, `trace()`, `trace_vdelete()`, `trace_vinfo()`) |
| **3.18** | The `decimal.Decimal` `'N'` format specifier; accepting a boolean where a file descriptor is expected; `import` lines inside `<name>.pth` files (superseded by PEP 829 `.start` files) |
| **3.19** | Implicit MSVC struct layout from `_pack_` without `_layout_` on non-Windows; the `string` keyword argument of hashlib constructors; `http.cookies.Morsel.js_output()` / `BaseCookie.js_output()`; altering `imaplib.IMAP4.file` |
| **3.20** | `struct.Struct.__new__()` without the `format` argument, and `__init__()` on an already-initialised `Struct`; the `__version__` / `version` / `VERSION` attributes of 24 stdlib modules (`argparse`, `csv`, `ctypes`, `ctypes.macholib`, `decimal` (use `decimal.SPEC_VERSION`), `http.server`, `imaplib`, `ipaddress`, `json`, `logging` (`__date__` too), `optparse`, `pickle`, `platform`, `re`, `socketserver`, `tabnanny`, `tarfile`, `tkinter.font`, `tkinter.ttk`, `wsgiref.simple_server`, `xml.etree.ElementTree`, `xml.sax.expatreader`, `xml.sax.handler`, `zlib`), for which the replacement is `sys.version_info`; PEP 829 `.pth` deprecations (warnings for `import` lines in `<name>.pth` files, and such files no longer decoded in the locale encoding — they **must** be `utf-8-sig`); instantiating abstract `ast` nodes (e.g. `ast.AST`, `ast.expr`), which becomes an error; `isinstance()` / `issubclass()` on a protocol class that inherits runtime-checkability without its own `@runtime_checkable`, which becomes a `TypeError` — this last one interacts directly with the Protocol content in `python_typing_contract_manifest.md` |

**The `profile` → `profiling` transition is a three-step schedule, not a flag day** (PEP 799,
**Final**, 3.15): 3.15 emits `DeprecationWarning` on import of `profile`, 3.16 on all uses, removal
in 3.17. `cProfile` remains "an alias for backwards compatibility" for the relocated
`profiling.tracing`. VERSION-DEPENDENT (3.15–3.17).

### 7e. Deprecated with no deadline

**ESTABLISHED.** The following are listed under "pending removal in future versions", so
**warning-driven CI must not assume a deadline** for them: `datetime.datetime.utcnow()` and
`utcfromtimestamp()`; `logging.warn()`; the `threading` camelCase aliases (`notifyAll`, `isSet`,
`isDaemon`, `setDaemon`, `getName`, `setName`, `currentThread`, `activeCount`); `typing.Text`;
`codecs.open()`; `argparse.FileType` and nested argument / mutually-exclusive groups; the
`urllib.parse.split*` family and `to_bytes()`; the legacy `ssl` protocol constants and NPN methods;
the `onerror` parameter of `shutil.rmtree()`; `os.register_at_fork()` in a multi-threaded process;
`os.path.commonprefix()`; and `sys._clear_type_cache()`.

**Not deprecated, contrary to a common recollection:** `getopt`. Its 3.14 module page carries only a
feature-completeness note — "This module is considered feature complete. A more declarative and
extensible alternative to this API is provided in the `optparse` module. Further functional
enhancements for command line parameter processing are provided either as third party modules on
PyPI, or else as features in the `argparse` module." No deprecation version and no removal version
are stated. VERSION-DEPENDENT (3.14).

### 7f. Behaviour changes that are not removals

**VERSION-DEPENDENT.** Three flips move test *results* rather than version strings, and none of them
raises a deprecation warning first:

| Change | Version | Consequence |
|---|---|---|
| UTF-8 becomes the default encoding for files, stdio and pipes (PEP 686) | **3.15** | Code that passed only because the platform locale happened to be UTF-8, or that relied on locale encoding on Windows, changes behaviour. Early warning: `-X warn_default_encoding` (3.10+). Revert: `PYTHONUTF8=0` / `-X utf8=0`; `encoding="locale"` stays explicit |
| `ProcessPoolExecutor` default start method → `forkserver` on Unix except macOS | **3.14** | Code implicitly relying on `fork` inheriting module-level state, open handles or monkeypatches fails, often only under load |
| `faulthandler` dumps only the current thread when the GIL is disabled | **3.14** | A free-threaded crash dump is less complete than a GIL-build dump |

---

## 8. Re-verification protocol

### 8a. The pages to reload, in order

**ESTABLISHED (as a procedure).** Reloading these ten answers every fact in §1–§2; the rest of the
list covers §4–§7.

| Order | Page | Establishes |
|---|---|---|
| 1 | `devguide.python.org/versions/` | The whole §1a matrix: branch, schedule PEP, phase, first release, EOL, release manager. Remember the italics = estimate rule |
| 2 | `devguide.python.org/developer-workflow/development-cycle/` | Phase definitions (§1b) and the source-only rule |
| 3 | `www.python.org/downloads/` | Which patch release is current |
| 4 | The release page of each current patch release | Exact release date, installer availability, JIT note |
| 5 | `blog.python.org` (Python Insider) | Release announcements, ABI-freeze wording, benchmark claims |
| 6 | PEP 790 (3.15), PEP 826 (3.16), PEP 745 (3.14), PEP 719 (3.13), PEP 693 (3.12) | Schedules, freeze dates, bugfix/security window wording |
| 7 | `docs.python.org/3.15/whatsnew/3.15.html` and the 3.14 What's New | §4 ledger rows and §7f behaviour changes |
| 8 | `docs.python.org/3.15/deprecations/index.html` | §7d and §7e in full |
| 9 | `docs.python.org/3/using/cmdline.html` and `.../using/configure.html` | §6a switchboard and §5 build flags |
| 10 | `peps.python.org` (per-PEP pages; the PEP API for bulk status) | §4b–§4d statuses |

Also, when the relevant section is load-bearing: the free-threading HOWTO (§5a–§5c), the perf
profiling HOWTO (§6a `perf` rows), `library/devmode.html` (§6b), `library/warnings.html` (§6c),
`packaging.python.org` core metadata (§3a), and `scientific-python.org/specs/spec-0000/` (§3d).

### 8b. Triggers that invalidate this file

**VERSION-DEPENDENT.** Each of these events makes a specific claim above false. The first three are
scheduled within ten weeks of the verification date.

| Trigger | Expected | Invalidates |
|---|---|---|
| **3.15.0 final** | 2026-10-01 | Every "3.15 is at rc1 / not released" statement: §1a, §2b, §3c, §3e |
| **3.10 end of life** | ≈2026-10 | §1a row, §3d CPython floor, §3e first row |
| **Final 3.13 bugfix release** | ≈2026-10 (around 3.15.0 final) | §1a phase, §2c, §3e `>=3.13` row |
| **3.16 alpha 1** | 2026-10-13 | "3.16 has no artefact of any kind": TL;DR, §1a |
| **Any new patch release** | ≈2 months in the bugfix phase | §1a latest-artefact column (the fastest-decaying rows in the file) |
| **3.15.0rc2** | 2026-09-01 | §1a latest artefact for 3.15 |
| A PEP changes status | unscheduled | §4b, §4c, §4d — in particular PEP 744 leaving **Draft**, and any Draft in §4d becoming Final |
| A **Phase III** free-threading PEP appears | unscheduled | §5a's OPEN row and every "free-threading is optional" statement |
| `abi3t` gains build-tool support | unscheduled | §5b's wheel-tag advice |
| A new toolchain floor (build tools, checkers, runners) | unscheduled | §3c item 3 — and the owning pillar file's own version block |

### 8c. What "verified" means in this file

**ESTABLISHED (as a convention of this collection).** A claim here was read off a primary page on
2026-08-08 — not recalled, and not inferred from a changelog summary. Two deliberate consequences:

- **Where a primary page was silent, the row says OPEN** rather than filling the gap plausibly.
  §5f's JIT build mode, the pre-3.14 free-threaded wheel tags, and the `exceptiongroup` / TOML
  backport package versions are the OPENs in this file, and they are OPEN because nothing
  authoritative was found this pass — not because they are unknowable. An OPEN that the cited page
  answers is a defect, not caution: `-X utf8` was one (the cmdline reference states "Added in
  version 3.7" one line below the rows that were read) and is now resolved in §6a.
- **Where the only evidence was secondary, the claim is FLAGGED-SECONDARY** (§5e's tail-call
  benchmarking correction, §3d's NEP 29 supersession). Do not promote either to load-bearing without
  a primary source.

---

## Anti-patterns checklist

Each is a violation of a section above, and carries that section's epistemic tag by reference.
Reject on sight.

- **Writing "the latest Python is 3.14"** as if that named a build — the release is **3.14.7**; CI
  must pin patch versions (§1a).
- **Calling 3.15 "alpha" or "in beta"** — it is at rc1, feature-frozen since 2026-05-07, ABI-frozen
  from rc1 (§1a, §2b).
- **Deferring 3.15 testing until October** — rc-built wheels work on final 3.15; the trigger has
  already fired (§2b).
- **Asserting any released 3.16 behaviour** — no 3.16 artefact exists; alpha 1 is 2026-10-13 (§1a).
- **Emitting "Python 3.26" or any CalVer version** — PEP 2026 is Rejected (§2d).
- **Downloading a python.org installer for 3.12, 3.11 or 3.10 in CI** — security-phase releases are
  source-only (§1b).
- **Treating "3.11 is supported" as "fixes arrive promptly"** — security branches have no cadence
  (§1b).
- **`gpg --verify` on a 3.14+ python.org tarball** — PGP signatures ended with 3.14; Sigstore
  replaced them (§2e).
- **Publishing an upper bound in `requires-python`** (`<4`, `<3.15`) — silently uninstallable on the
  next interpreter (§3c).
- **Presenting `requires-python` as the tested matrix** — it is a resolver exclusion filter
  (§3a–§3b).
- **Citing a support policy without naming it** — CPython's 5-year window and SPEC 0's 36-month
  window give different floors (3.10 vs 3.12) (§3d).
- **Writing a `requires-python` floor with no recorded policy** — the hub's recommended default is
  `">=3.13"`; departing from it is allowed, leaving the departure unexplained is not (§3e, §3b).
- **Flooring on a security-only branch by default** — 3.12 and below get only security fixes,
  source-only, on no cadence; choose that floor deliberately (for SPEC 0 reach) or not at all
  (§1b, §3e).
- **Using a Draft PEP's syntax** — PEP 718, 764, 746, 767, 781, 821, 827, 835 describe nothing that
  exists (§4d).
- **Citing PEP 744 as a committed default-on JIT** — it is Draft and says the JIT "is likely to
  remain" outside the default build (§5d).
- **Writing `-X jit`** — it does not exist; the only runtime switch is `PYTHON_JIT`, and it is inert
  unless the interpreter was built with `--enable-experimental-jit` (§5d).
- **Claiming free-threading support because the project ships `abi3`** — the free-threaded ABI is
  separate (`t` in `sys.abiflags`, `cp31Xt` tags), and `abi3t` is unsupported by the major build
  backends (§5b).
- **Trusting a free-threaded benchmark without asserting `sys._is_gil_enabled()`** — one extension
  lacking `Py_mod_gil` silently re-enables the GIL (§5c).
- **Using `sys._is_gil_enabled()` for a build-time decision** — it reports runtime state; the
  build-time answer is `sysconfig.get_config_var("Py_GIL_DISABLED")` (§5b).
- **Comparing profiles or benchmarks across build configurations** — JIT, tail-call dispatch, frame
  pointers and free-threading all move the numbers, and 3.15 flips two of them by default (§5f,
  §5h).
- **Quoting a bare free-threading overhead percentage** — the primary sources give platform-specific
  figures that differ (§5a).
- **Assuming `-X dev` enables `tracemalloc` or protects `assert` from `-O`** — it does neither
  (§6b).
- **Relying on `DeprecationWarning` being visible** — it is ignored outside `__main__` by default
  (§6c).
- **Setting `-X no_debug_ranges` anywhere you intend to debug** — it deletes the caret data from
  tracebacks (§6d).
- **Expecting `OverflowError` from the integer-conversion limit** — it raises `ValueError`, at a
  default of 4300 digits (§6d).
- **Importing `sre_compile` / `sre_constants` / `sre_parse`** — removed in 3.15, with only private
  replacements (§7c).
- **Migrating to a private replacement** (`re._compiler` and friends) — remove the dependency
  instead (§7c).
- **Assuming a removal deadline for a soft-deprecated or "future versions" API** — PEP 387's soft
  deprecation schedules nothing (§7a, §7e).
- **Repeating "getopt is deprecated"** — the 3.14 docs state only that it is feature complete (§7e).
- **Reading "no Pending removal in Python 3.15" as covering the C API** — that is true of the
  Python-level half of the deprecations page only; the C API half has its own 3.15 bucket (§7b).
- **Treating `os.path.ALLOW_MISSING` as 3.15-only** — it shipped in **3.13.4** with the
  CVE-2025-4517 fix and is documented as 3.14 in the current stable docs; hand-rolling a symlink
  resolver on a 3.13/3.14 floor is unnecessary (§4a).
- **Restating a release date in another manifest** — every sibling file cites this hub instead (§
  the sibling block below).

---

## Open questions to resolve before building

Each is a decision this file cannot make for the project. Carry every one into the spec per
`software_spec_discipline_manifest.md` §G5.

- **The floor (OPEN, §3e).** Which `requires-python` value, and which constructs in §4 justify it?
  A floor chosen without naming a construct it unlocks is a floor chosen by habit. **This one has a
  recommended default:** `">=3.13"`, with `">=3.12"` as the SPEC 0-aligned alternative and lower
  floors permitted at a named cost (§3e). The decision to record is therefore *accept the default or
  depart from it, and why* — not the whole question from scratch.
- **The policy behind the floor (OPEN, §3d).** CPython's 5-year window, SPEC 0's 36-month window, or
  a project-specific rule? Whichever it is, the SPEC must name it, because the two give different
  answers today (3.10 vs 3.12).
- **The CI matrix, stated separately from the floor (OPEN, §3b).** Which interpreters actually run
  the suite — including whether 3.15 (rc, ABI-frozen) and free-threaded builds are in it? Wiring is
  owned by `python_quality_gates_manifest.md`.
- **Free-threading: gate or flag (OPEN, §5a–§5c).** Is a free-threaded build a supported
  configuration, an experiment, or out of scope? If supported, the project needs the runtime
  `sys._is_gil_enabled()` assertion and a `cp31Xt` wheel story.
- **The build-configuration stamp (OPEN, §5h).** Where is interpreter version *and* build
  configuration recorded in performance and crash artefacts, and what rejects an artefact that lacks
  it?
- **JIT and tail-call posture (OPEN, §5d–§5f).** Are official binaries accepted as-is (with the
  documented uncertainty about 3.14's JIT build mode), or does the project build its own interpreter
  for reproducible measurement?
- **Deprecation visibility (OPEN, §6c, §7).** Does CI run `-W error::DeprecationWarning` or `-X
  dev`, and on which interpreters? Without one of them the §7 calendar arrives as a production
  break.
- **The 3.15 UTF-8 audit (OPEN, §7f).** Which code paths depend on the locale encoding, and has
  `-X warn_default_encoding` been run over the suite before 3.15 becomes the floor?
- **Release-artefact verification (OPEN, §2e).** Does the pipeline verify interpreter downloads at
  all, and has it moved from PGP to Sigstore for 3.14+? Gate design belongs to
  `python_quality_gates_manifest.md`.
- **Re-verification ownership (OPEN, §8).** Who reloads §8a on each trigger in §8b, and where is the
  new verification date stamped? An unowned hub decays into exactly the drift it was created to
  stop.

---

## Sources (accessed 8 Aug 2026)

- CPython branch/phase/EOL/release-manager matrix; `main` = future 3.16 and "the only branch that
  accepts new features"; italicised dates are estimates; 3.9 EOL 2025-10-31 —
  https://devguide.python.org/versions/ . Accessed 8 Aug 2026.
- Definitions of the feature / prerelease / bugfix / security / end-of-life phases; security
  releases are source-only and issued only when security fixes land —
  https://devguide.python.org/developer-workflow/development-cycle/ . Accessed 8 Aug 2026.
- Current release pointer and the per-line release tables —
  https://www.python.org/downloads/ . Accessed 8 Aug 2026.
- 3.14.7 released 2026-08-05, seventh maintenance release, ≈499 bugfixes; official macOS/Windows
  binaries "include an experimental JIT compiler"; PGP signatures discontinued from 3.14 with
  Sigstore recommended — https://www.python.org/downloads/release/python-3147/ . Accessed 8 Aug
  2026.
- 3.14.7 and 3.13.15 both released 2026-08-05 (≈499 and ≈400 bugfixes) —
  https://blog.python.org/2026/08/python-3147-31315/ . Accessed 8 Aug 2026.
- The per-release bugfix counts behind the TL;DR's "roughly 2,000 behind current", each page stating
  its count *since the previous release*: 558 (3.14.1), 18 (3.14.2), 299 (3.14.3), 337 (3.14.4), 154
  (3.14.5), 179 (3.14.6), 499 (3.14.7) = 2,044 —
  https://www.python.org/downloads/release/python-3141/ through
  https://www.python.org/downloads/release/python-3147/ . Accessed 8 Aug 2026.
- 3.15.0rc1 released 2026-08-04; only clear bug fixes until final; rc2 2026-09-01; full 3.15 PEP
  list; macOS official binaries install free-threading support by default —
  https://www.python.org/downloads/release/python-3150rc1/ . Accessed 8 Aug 2026.
- "There will be no ABI changes from this point forward in the 3.15 series"; rc-built wheels work
  with future 3.15; JIT "8-9% geometric mean performance improvement on x86-64 Linux over the
  standard interpreter, and 12-13% speedup on AArch64 macOS over the tail-calling interpreter" — two
  different baselines — https://blog.python.org/2026/08/python-3150-rc1/ and
  https://www.python.org/downloads/release/python-3150rc1/ . Accessed 8 Aug 2026.
- 3.12.13 (2026-03-03) is "a security bugfix release for the legacy 3.12 series"; no binary
  installers; source-only until October 2028 —
  https://www.python.org/downloads/release/python-31213/ . Accessed 8 Aug 2026.
- 3.12.13 / 3.11.15 / 3.10.20 all 2026-03-03; "security-fix-only mode ... source-only releases, and
  there is no pre-set release cadence" — https://blog.python.org/2026/03/python-31213-31115-31020/ .
  Accessed 8 Aug 2026.
- Python 3.15 release schedule (Active): beta 1 2026-05-07 feature freeze, rc1 2026-08-04, rc2
  2026-09-01, final 2026-10-01, security to ≈October 2031 — https://peps.python.org/pep-0790/ .
  Accessed 8 Aug 2026.
- Python 3.16 release schedule (Active): development began 2026-05-07, alpha 1 2026-10-13, feature
  freeze 2027-05-04, final 2027-10-05, security to ≈October 2032; RM Savannah Ostrowski —
  https://peps.python.org/pep-0826/ . Accessed 8 Aug 2026.
- Python 3.14 release schedule (Active): 3.14.0 2025-10-07; 3.14.1–3.14.7 actual dates; 3.14.14
  (≈2027-10) "the final regular bugfix release with binary installers"; security to ≈October 2030 —
  https://peps.python.org/pep-0745/ . Accessed 8 Aug 2026.
- Python 3.13 release schedule (Active): 24-month bugfix phase, final bugfix around 3.15.0 final,
  security to ≈October 2029 — https://peps.python.org/pep-0719/ . Accessed 8 Aug 2026.
- Python 3.12 release schedule (Active): 18-month bugfix phase, security to ≈October 2028 —
  https://peps.python.org/pep-0693/ . Accessed 8 Aug 2026.
- Calendar versioning for Python, Python-Version 3.26, status **Rejected** —
  https://peps.python.org/pep-2026/ . Accessed 8 Aug 2026.
- Backwards Compatibility Policy (Active): two-minor-version warning requirement, five-year removal
  preference, `DeprecationWarning` vs `PendingDeprecationWarning`, the soft-deprecation definition —
  https://peps.python.org/pep-0387/ . Accessed 8 Aug 2026.
- Removing dead batteries (Final): the 3.12 and 3.13 removal sets and the per-module
  deprecation/removal table — https://peps.python.org/pep-0594/ . Accessed 8 Aug 2026.
- GIL-optional CPython (Final, 3.13): `--disable-gil`, the `t` ABI flag, ABI incompatibility with
  the standard build and the stable ABI, the three-phase rollout — https://peps.python.org/pep-0703/
  . Accessed 8 Aug 2026.
- Criteria for supported free-threading (Final, accepted 2025-06-16, targets 3.14): the ≤15%
  single-thread and ≤20% memory criteria, the meaning of "officially supported", Phase III deferred
  to a future PEP — https://peps.python.org/pep-0779/ . Accessed 8 Aug 2026.
- `abi3t` stable ABI for free-threaded builds (Final, 3.15): `Py_TARGET_ABI3T`, the `abi3.abi3t` tag
  set, opaque `PyObject`/`PyVarObject`/`PyModuleDef`, PEP 697 / 793 / 820 requirements —
  https://peps.python.org/pep-0803/ . Accessed 8 Aug 2026.
- JIT Compilation, status **Draft**, Python-Version 3.13; not in the default build and "likely to
  remain that way"; ≈parity with the specialising interpreter; 10-20% more memory —
  https://peps.python.org/pep-0744/ . Accessed 8 Aug 2026.
- UTF-8 mode as default (Final, 3.15); `PYTHONUTF8=0` / `-X utf8=0` revert; `encoding="locale"` and
  `locale.getencoding()` remain — https://peps.python.org/pep-0686/ . Accessed 8 Aug 2026.
- Explicit lazy imports (Final, 3.15): the `lazy` soft keyword and its allowed/disallowed
  placements, `-X lazy_imports` modes, `PYTHON_LAZY_IMPORTS`, `sys.set_lazy_imports*`,
  `__lazy_modules__`, `types.LazyImportType`, deferred errors and `sys.modules` timing —
  https://peps.python.org/pep-0810/ . Accessed 8 Aug 2026.
- A dedicated `profiling` package (Final, 3.15): `profiling.tracing` and `profiling.sampling`,
  `cProfile` kept as an alias, `profile` deprecation 3.15 → 3.16 → removal in 3.17 —
  https://peps.python.org/pep-0799/ . Accessed 8 Aug 2026.
- Frame Pointers Everywhere (Final, 3.15): the `BASECFLAGS` additions, `--without-frame-pointers`,
  propagation to extensions via `sysconfig`, the 0.2-2.3% cost range, and perf/eBPF dependence on
  frame-pointer chains — https://peps.python.org/pep-0831/ . Accessed 8 Aug 2026.
- TypedDict with typed extra items (Final, 3.15, resolved 2025-08-15): `closed=`, `extra_items=`,
  `extra_items=Never` equivalence, interaction with `total=`, `__extra_items__` / `__closed__`,
  `typing.NoExtraItems` — https://peps.python.org/pep-0728/ . Accessed 8 Aug 2026.
- Sentinel Values (Final, 3.15, resolved 2026-04-23): the builtin `sentinel`, distinct objects per
  call, copy/pickle behaviour, truthiness, use in `|` type expressions —
  https://peps.python.org/pep-0661/ . Accessed 8 Aug 2026. **Signature discrepancy:** PEP 661 writes
  `sentinel(name, /, repr=None)` while describing `repr` as keyword-only; the 3.15 builtins
  reference renders it `class sentinel(name, /, *, repr=None)`, which is the spelling §4a uses —
  https://docs.python.org/3.15/library/functions.html . Accessed 8 Aug 2026.
- `typing.TypeForm` (Final, 3.15, resolved 2026-02-20) — https://peps.python.org/pep-0747/ .
  Accessed 8 Aug 2026.
- `@typing.disjoint_base` (Final, 3.15) — https://peps.python.org/pep-0800/ . Accessed 8 Aug 2026.
- Typing Council governance (Active); the Council "has no direct authority over type checkers" —
  https://peps.python.org/pep-0729/ . Accessed 8 Aug 2026.
- Bulk PEP status and Python-Version for the §4b ledger (484, 544, 561, 585, 604, 612, 646, 647,
  649, 655, 673, 675, 681, 692, 695, 696, 698, 702, 705, 728, 742, 747, 749, 800, 661 Final; 718,
  746, 764, 767, 781, 821, 827, 835 Draft; 563 Superseded; 677 Rejected; 724, 727 Withdrawn; 729
  Active) — https://peps.python.org/api/peps.json . Accessed 8 Aug 2026.
- Packaging PEP index with statuses (Accepted: 458, 658, 714, 739, 752, 783, 794, 808; Draft: 480,
  694, 710, 711, 725, 755, 771, 777, 780, 804, 807, 817, 819, 825; Deferred: 423, 491, 778; Active:
  609, 772) — https://peps.python.org/topic/packaging/ . Accessed 8 Aug 2026.
- Canonical `Status:` / `Created:` / `Resolution:` headers for the §4c table (PEPs 517, 518, 621,
  639, 660, 735, 740, 751, 752, 770, 771, 777, 794, 808, 810, 819, 825, 508, 440, 427, 491, 561,
  420, 562, 702, 723) — https://raw.githubusercontent.com/python/peps/main/peps/pep-0517.rst and
  the same path for each other PEP number listed. Accessed 8 Aug 2026.
- 3.15 What's New (from the 3.15.0rc1 docs): the highlight list; lazy-import CLI and API surface;
  `frozendict`; builtin `sentinel`; the `profiling.sampling` CLI and output formats; PEP 831; PEP
  798; PEP 686; PEP 829; PEP 728 / 747 / 800; PEP 782 / 788 / 793 / 803 / 820; Unicode 17.0.0;
  `sys.abi_info`; the `sys.monitoring` unwinding-event changes; the Windows 64-bit tail-calling
  interpreter; the "Removed" section headings including `sre_*`; the `abi3t` build-tool warning —
  https://docs.python.org/3.15/whatsnew/3.15.html . Accessed 8 Aug 2026.
- Complete Python-level pending-removal lists for 3.16, 3.17, 3.18, 3.19, **3.20** and "future
  versions"; no Python-level "Pending removal in 3.15" section remains, while the page's **C API
  deprecations** half does still carry "Pending removal in Python 3.15"
  (`PyImport_ImportModuleNoBlock()`, `PyWeakref_GetObject()`/`PyWeakref_GET_OBJECT()`, the
  `PyUnicode_As{Decoded,Encoded}{Object,Unicode}()` family, the 3.13 initialization getters, the
  3.11 initialization setters, the global configuration variables) plus C API buckets for 3.16,
  3.18, 3.19 and 3.20 —
  https://docs.python.org/3.15/deprecations/index.html . Accessed 8 Aug 2026.
- The 3.14-era "Pending removal in Python 3.15" list, used to establish what landed in 3.15 —
  https://docs.python.org/3/deprecations/index.html . Accessed 8 Aug 2026.
- 3.14 What's New: PEP 649/749, 734, 765, 768, 784, 761, 779; `sys.remote_exec()` and `python -m pdb
  -p PID`; `annotationlib` formats; asyncio `ps`/`pstree`; `InterpreterPoolExecutor`; the
  `forkserver` default; `faulthandler.dump_c_stack`; the tail-call interpreter "3-5% faster" with
  "Clang 19 and newer"; the "roughly 5-10%" free-threading single-thread penalty; `-X
  context_aware_warnings` and `-X thread_inherit_context` defaults; the removals list —
  https://docs.python.org/3/whatsnew/3.14.html . Accessed 8 Aug 2026.
- 3.13 What's New: free-threading as "experimental support ... not enabled by default",
  `python3.13t`, `--disable-gil`, "experimental free-threading build" in `sys.version`,
  `sys._is_gil_enabled()`; the 19 removed dead-battery modules; `2to3`/`lib2to3`, `tkinter.tix`,
  `locale.resetlocale`, `typing.io`/`typing.re` removals; the new PyREPL and `PYTHON_BASIC_REPL`;
  the experimental-JIT build flags and `PYTHON_JIT` — https://docs.python.org/3/whatsnew/3.13.html .
  Accessed 8 Aug 2026.
- 3.12 What's New: PEP 669 `sys.monitoring`, PEP 695 type-parameter syntax and the `type` statement,
  PEP 692 `**kwargs` typing, PEP 698 `@override` — https://docs.python.org/3/whatsnew/3.12.html .
  Accessed 8 Aug 2026.
- 3.11 What's New: PEP 654 `ExceptionGroup`/`except*`, PEP 678 `add_note()`, PEP 680 `tomllib`,
  `asyncio.TaskGroup`, `typing.Never` and `typing.assert_never()`, PEP 673 `Self`, PEP 675
  `LiteralString`, PEP 655 `Required`/`NotRequired` — https://docs.python.org/3/whatsnew/3.11.html .
  Accessed 8 Aug 2026.
- Complete `-X` option list with added-in versions and the full `PYTHON*` environment-variable set,
  including `-X importtime=2` (3.14), `-X tlbc` (3.14), `-X gil` (3.13), `-X perf` / `-X perf_jit`,
  `-X cpu_count`, `-X presite`, `PYTHON_JIT`, `PYTHON_TLBC`, `PYTHON_DISABLE_REMOTE_DEBUG`,
  `PYTHON_FROZEN_MODULES`, `PYTHON_NODEBUGRANGES`; `-X utf8` / `-X utf8=0` with "Added in version
  3.7"; and the debug-mode pair where only `PYTHONDUMPREFSFILE` carries "Added in version 3.11"
  (`PYTHONDUMPREFS` has no version note) — https://docs.python.org/3/using/cmdline.html . Accessed 8
  Aug 2026.
- Build configuration options: `--enable-experimental-jit=[no|yes|yes-off|interpreter]` (3.13,
  default no), `--disable-gil` (3.13, `Py_GIL_DISABLED`, `t` in `sys.abiflags`),
  `--with-tail-call-interp` (3.14, Clang 19+, `preserve_none`), `--without-remote-debug` (3.14),
  `--with-pydebug`, `--with-trace-refs`, `--enable-optimizations`, `--with-lto`,
  `--without-frame-pointers` (3.15) — https://docs.python.org/3.15/using/configure.html . Accessed 8
  Aug 2026.
- The 3.14 wording of the same options, confirming `--without-frame-pointers` does not exist in 3.14
  — https://docs.python.org/3/using/configure.html . Accessed 8 Aug 2026.
- The exact contents of Python Development Mode; the explicit statement that `tracemalloc` is not
  enabled; the `PYTHONMALLOC=default` escape; the `ResourceWarning` "Enable tracemalloc" message —
  https://docs.python.org/3/library/devmode.html . Accessed 8 Aug 2026.
- The default warning-filter list and "In a debug build, the list of default warning filters is
  empty"; `PYTHONWARNINGS` filter form and precedence; `@warnings.deprecated(message, /, *,
  category=DeprecationWarning, stacklevel=1)` with "Added in version 3.13: See PEP 702" (the §3e
  behavioural argument for a 3.13 floor) — https://docs.python.org/3/library/warnings.html .
  Accessed 8 Aug 2026.
- `BaseExceptionGroup.subgroup()` / `split()` and "Added in version 3.13: `condition` can be any
  callable which is not a type object" (§3e) — https://docs.python.org/3/library/exceptions.html .
  Accessed 8 Aug 2026.
- `traceback.TracebackException.exc_type_str` "Added in version 3.13" and `exc_type` "Deprecated
  since version 3.13" (§3e) — https://docs.python.org/3/library/traceback.html . Accessed 8 Aug
  2026.
- `contextlib.suppress` group-awareness is **3.12**, not 3.13: "Changed in version 3.12: `suppress`
  now supports suppressing exceptions raised as part of a `BaseExceptionGroup`" — checked because a
  3.13 attribution was in circulation — https://docs.python.org/3/library/contextlib.html . Accessed
  8 Aug 2026.
- `os.path.realpath()` version notes: the 3.13 docs say "Changed in version 3.13.4: The
  `ALLOW_MISSING` value for the *strict* parameter was added" and `ALLOW_MISSING` "Added in version
  3.13.4", while the current stable (3.14) docs say "Changed in version 3.14" and "Added in version
  3.14" (§4a) — https://docs.python.org/3.13/library/os.path.html and
  https://docs.python.org/3/library/os.path.html . Accessed 8 Aug 2026.
- Free-threading build-vs-runtime detection (`sysconfig.get_config_var("Py_GIL_DISABLED")`,
  `sys._is_gil_enabled()`, `python -VV`, the `t` suffix); `PYTHON_GIL` and `-X gil`; the automatic
  GIL re-enable plus warning when a non-`Py_mod_gil` extension is imported; ≈1% macOS aarch64 and
  ≈8% x86-64 Linux single-thread overhead —
  https://docs.python.org/3/howto/free-threading-python.html . Accessed 8 Aug 2026.
- `-X perf` / `PYTHONPERFSUPPORT` / `sys.activate_stack_trampoline("perf")` with precedence order;
  the `HAVE_PERF_TRAMPOLINE` check; the frame-pointer requirement; the `-X perf_jit` DWARF path with
  perf 6.8+ and `perf inject --jit` — https://docs.python.org/3/howto/perf_profiling.html . Accessed
  8 Aug 2026.
- `sys.get_int_max_str_digits()` / `set_int_max_str_digits()`,
  `sys.int_info.default_max_str_digits`, `sys.int_info.str_digits_check_threshold`,
  `sys.flags.int_max_str_digits` (all 3.11) — https://docs.python.org/3/library/sys.html . Accessed
  8 Aug 2026.
- `faulthandler.enable(file, all_threads, c_stack=True)` with `c_stack` added in 3.14;
  `dump_c_stack()` added in 3.14; the signal list; the 3.14 single-thread dump when the GIL is
  disabled — https://docs.python.org/3/library/faulthandler.html . Accessed 8 Aug 2026.
- `getopt` carries no deprecation notice, only the "This module is considered feature complete" note
  — https://docs.python.org/3/library/getopt.html . Accessed 8 Aug 2026.
- `Requires-Python` semantics: core metadata from version 1.2, version-specifier format, "This field
  cannot be followed by an environment marker", consulted by installers when picking a version —
  https://packaging.python.org/en/latest/specifications/core-metadata/#requires-python . Accessed
  8 Aug 2026.
- SPEC 0 "Minimum Supported Dependencies" (endorsed): drop Python 36 months after release and core
  packages 24 months after release; the 3.11 Q4 2025 / 3.12 Q4 2026 / 3.13 Q4 2027 / 3.14 Q4 2028
  drop schedule — https://scientific-python.org/specs/spec-0000/ . Accessed 8 Aug 2026.
- pytest 9.1.1 (2026-06-19), `Requires-Python >= 3.10`, classifiers 3.10-3.15 —
  https://pypi.org/project/pytest/ . Accessed 8 Aug 2026.
- coverage.py 7.15.4 (2026-08-06), `Requires-Python >= 3.10`, classifiers 3.10-3.16 plus
  `Programming Language :: Python :: Free Threading :: 3 - Stable` —
  https://pypi.org/project/coverage/ . Accessed 8 Aug 2026.
- `typing_extensions` 4.16.0 (2026-07-02): the `Sentinel` → `sentinel` rename "following the name
  that has been adopted for `builtins.sentinel` on Python 3.15", `@typing_extensions.disjoint_base`
  added in 4.15.0, and the changed default sentinel repr —
  https://raw.githubusercontent.com/python/typing_extensions/main/CHANGELOG.md . Accessed 8 Aug
  2026.
- **FLAGGED-SECONDARY**, not used as primary evidence: the tail-call benchmarking correction (the
  10-15% figure was an LLVM 19 baseline regression) —
  https://blog.nelhage.com/post/cpython-tail-call/ ;
  https://fidget-spinner.github.io/posts/apology-tail-call.html ; https://lwn.net/Articles/1013581/
  . The CPython docs' own 3-5% geometric mean is the primary anchor. The NEP 29 → SPEC 0
  supersession relationship is likewise secondary. Accessed 8 Aug 2026.

### Sibling manifests (cross-referenced, not duplicated)

This file owns **only** version, support, schedule, PEP-status, build-variant and interpreter-switch
facts. Everything about what to *do* with them lives elsewhere:

- `python_typing_contract_manifest.md` — what each typing construct in §4b means, and which checker
  honours it at which strictness. The hub owns the PEP's status and shipping version; that file owns
  the contract.
- `python_language_hazards_manifest.md` — the hazards behind §6d and §7f (integer-conversion limits,
  the `finally` warning, encoding assumptions), each routed to its enforcement mechanism.
- `python_linting_practices_manifest.md` — lint rule codes; this file never cites one.
- `python_testing_tooling_manifest.md` — runner and coverage tool selection, versions and behaviour;
  the hub carries only their declared interpreter ranges (§3c).
- `error_tracing_contract_manifest.md` — the behaviour of `ExceptionGroup`, `except*`, `add_note`,
  chaining and exhaustiveness; the hub carries only the version each shipped in.
- `logging_observability_manifest.md` — severity policy and what a project emits; the hub carries
  only the default warning-filter facts that decide visibility (§6c).
- `python_runtime_diagnostics_manifest.md` — the *use* of every switch marked **[diag]** in §6a,
  plus `faulthandler`, `tracemalloc`, `sys.monitoring`, remote attach, the `profiling` package and
  post-mortem workflow. The hub is the inventory; that file is the method.
- `python_module_boundaries_manifest.md` — packaging-metadata semantics behind §4c, the import
  system, lazy imports as a boundary tool, and the public-API/deprecation contract.
- `python_quality_gates_manifest.md` — the CI matrix (§3b), warning-as-error policy (§6c),
  supply-chain verification (§2e), and what any measurement is allowed to gate.
- `python_concurrency_determinism_manifest.md` — free-threading and subinterpreter *behaviour* and
  hazards; the hub owns their version status and detection surfaces (§5a–§5c).
- `software_spec_discipline_manifest.md` §G5 — where every OPEN above is recorded as a decision.
- `architecture_manifest_default.md` — the reasoning frame; it carries no version facts by design.
