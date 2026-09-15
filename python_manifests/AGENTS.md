# Python Ground — agent entry point

**You are building Python that must be testable, diagnosable, maintainable, modular, and safe to
extend incrementally.** This package is the grounding for that. It is **GROUNDING, not a rulebook**:
cite a rule when it materially shapes a decision; reason past it when the situation genuinely differs —
and say which you are doing.

**Facts verified 2026-08-08.** Version-dependent claims decay. Anything dated routes through
`reference/python_platform_baseline_manifest.md` (the hub). **If any file disagrees with the hub about a
version, the hub wins and that file is stale.**

## How to use this package — do not read it all

Three layers. Loading the whole set is ~425k tokens and is never correct.

| layer | what | when |
|---|---|---|
| **this file** | non-negotiables + router | always, ~2.8k tokens |
| `cards/*.md` | one compact card per task | load the **one** that matches your task, ~2–4k tokens |
| `reference/*.md` | the full manifests | **only** the section a card names. Never a whole file. |
| `config/*` | ready-made config artifacts | copy verbatim; do not re-derive |
| `INDEX.json` | 647 indexed sections | query with `jq`/`grep`; **never read into context** |

Operating at full competence costs **this file plus one card**: ~4.7k tokens, **1.1%** of the
425k-token reference corpus. Depth stays one hop away and fully cited.

## The task router

| your task | load this card |
|---|---|
| scaffold a new project, pick versions, first `pyproject.toml` | `cards/start-project.md` |
| write or change application code | `cards/write-code.md` |
| review a diff, or check your own work before finishing | `cards/review-code.md` |
| add or split a module, package it, deprecate a public name | `cards/module-boundaries.md` |
| write or fix tests | `cards/write-tests.md` |
| design error handling, exceptions, validation | `cards/handle-errors.md` |
| add logging, metrics, traces | `cards/observability.md` |
| debug a hung, crashed, leaking or slow **running** process | `cards/diagnose-runtime.md` |
| add threads, `asyncio`, processes, subinterpreters | `cards/concurrency.md` |
| set up or tighten CI, lint, type-check, coverage gates | `cards/gates-and-ci.md` |
| write a spec before implementing | `cards/write-spec.md` |
| work on unfamiliar existing code with no spec | `reference/spec_recovery_reverse_engineering_manifest.md` |

## How to read a claim — the tag protocol

Every factual claim in `reference/` is tagged. The tag tells you how much weight it bears.

| tag | means | what you do |
|---|---|---|
| **ESTABLISHED** | normative and stable in the cited primary source | rely on it |
| **VERSION-DEPENDENT** | true of the named version only | check the version you are on |
| **MEASURED** | established by *running* the tool; version and command named | strongest tag for tool behaviour |
| **OPEN** | no authoritative source — a decision the project must make | **surface it; do not improvise silently** |
| **FLAGGED-SECONDARY** | only secondary evidence found | verify before it becomes load-bearing |
| **UNVERIFIED** | asserted by a source, not confirmed against a primary page | treat as a lead |
| **CC-FACT** | Claude Code harness mechanics, not language facts | bound to the harness |

An **untagged factual claim in `reference/` is a defect** — report it rather than trusting it.

## Enforcement routes — the package's organising idea

> Static typing is a good start. A pedantic linter is very nice. A set of coding practices is also
> nice. **A way of enforcing all of it is the point** — advice that isn't mechanically enforced decays
> to zero.

So every rule here names what enforces it, or admits that nothing does:

`type-catchable` (a checker at a named strictness) · `lint-catchable` (a named rule code) ·
`feature-eliminated` (a modern construct removes the hazard class) · `test-catchable` (name the test
kind) · `fitness-function` (a structural CI check) · `runtime-catchable` (a process-start configuration
turns silence into an exception) · **`contract-only`** (nothing mechanical catches it — an honest
admission, not a gap to paper over).

**A rule you cannot route is a preference.** When you add one, route it or label it `contract-only`.
Canonical route table: `reference/python_language_hazards_manifest.md` §0.1; the `[on]`/`[off]`/`[?]`
default-status markers beside every rule code are defined in §0.2 — **read those markers before you
copy a code into a config.**

## The twenty non-negotiables

These hold for every Python task. Everything else is in a card.

**Toolchain**
1. **Pin every tool version, and write the rule set out explicitly.** An implicit default set is not a
   standard: ruff 0.16.0 moved its default from 59 rules to 413 *and silently dropped 18*, two of which
   (`E711`, `E712`) were the only check for `== None` / `== True`. → `config/pyproject.toml`
2. **`target-version` must equal your `requires-python` floor**, never the newest release — ruff treats
   it as a *minimum*, so a value above the floor makes `UP` autofixes emit syntax that is a
   `SyntaxError` on the interpreter you publish for.
3. **Never run bulk autofix you have not reviewed.** Some fixes are marked unsafe by the tool itself and
   change runtime behaviour where dunder methods are overridden.

**Contracts**
4. **`assert` enforces nothing** — it is stripped under `-O`. Never validate input, enforce an
   invariant, or check a security property with it. `lint-catchable`: `S101` in `src`, exempted only in
   the test tree.
5. **Annotations carry nothing at runtime.** `cast` is a no-op, `Final`/`Protocol`/`Annotated` are
   checker- or metadata-only. Runtime enforcement is a separate, explicit act.
6. **Parse at the boundary, then trust the typed value inside.** Validation is a boundary event, not a
   habit sprinkled through the core.

**Errors**
7. **Failures that are part of the contract → a typed in-band result** the checker forces callers to
   handle. **Genuinely exceptional or programmer-error → raise.** Never use exceptions for routine
   expected outcomes.
8. **Never bare `except`, never `except BaseException`, never catch-and-ignore.** Suppress explicitly
   and narrowly with `contextlib.suppress`. `lint-catchable`: `BLE`, `S110`, `S112`.
9. **Wrap at boundaries: `raise Domain(...) from low`.** Never leak a library exception across your own
   API, and never use `from None` by default — it deletes the real source from the traceback.

**Code**
10. **No mutable default arguments** (`B006`) and **no late-binding closures in loops** (`B023`). The
    documented fix for one is the construct the other forbids — the resolution is in the write-code card.
11. **Timezone-aware datetimes only.** A naive `datetime` is a latent bug. `lint-catchable`: `DTZ`.
12. **No module-level mutable state and no import-time side effects.** A module is not a singleton.
    Largely `contract-only` — which is exactly why it needs saying.

**Observability**
13. **A library calls `logging.getLogger(__name__)`, adds `NullHandler`, and configures nothing.** Only
    the application configures handlers, and it does so once.
14. **Log once, at the handling boundary.** Not at every level on the way up. Use lazy `%`-style args,
    and **never log secrets or PII** — redact in a `Filter` at the logger, not in the formatter.

**Concurrency**
15. **Hold a reference to every task; prefer `TaskGroup` to bare `create_task`.** `CancelledError`
    derives from `BaseException`, so `except Exception` does not catch it — and must not.
16. **Every queue declares a `maxsize` and an overflow policy.** An unbounded queue is a deferred
    out-of-memory failure.
17. **Never `sleep` to synchronise.** Inject the clock, the seed, the executor and the event loop; that
    injection is what makes concurrent code testable at all.

**Process**
18. **A boundary that is not machine-checked is a preference.** `__all__` is documentation; an
    `import-linter` or `Tach` contract is enforcement. → `config/importlinter.toml`
19. **Coverage is a diagnostic, never a target.** Gate on the absence of assertion-free tests, not on a
    percentage.
20. **An `OPEN` is a decision to surface, not licence to improvise.** Split it the way
    `reference/software_spec_discipline_manifest.md` §G5 does — **ASSUMED** (you proceeded on a stated
    default) or **NEEDS-INPUT** (you need the owner) — and say which, where the next reader will see it.

## Two rules about your own conduct

- **Where a claim is about what a tool *does*, run the tool.** Documentation states intent; resolved
  settings are the fact. Both config-breaking defects found in this package's own audit were
  doc-derived: a rule code that does not exist (`D216`) and a rule wrongly listed as enabled-by-default
  (`LOG004`). If you measure, record the **tool version and the exact command** beside the result.
- **Never invent an identifier.** A fabricated rule code, flag or version gets pasted into a config and
  silently disables a check. If you cannot verify it, say so and leave it out.

## The reference shelf

Load a **section**, not a file. `python_*` files own Python facts; the two agnostic files own reasoning.

| file | pillar |
|---|---|
| `python_platform_baseline_manifest.md` | **version hub** — every CPython date, phase, PEP status, build variant, `-X` switch |
| `python_typing_contract_manifest.md` | maintainable — checkers, contract vocabulary, what types cannot express |
| `python_language_hazards_manifest.md` | maintainable — 13 hazard classes, 103 routed rows, the safe modern subset |
| `python_linting_practices_manifest.md` | maintainable — the rule set, fix safety, suppression hygiene, idiom catalogue |
| `python_testing_tooling_manifest.md` | testable — pytest surface, doubles, testability tactics, determinism |
| `error_tracing_contract_manifest.md` | diagnosable — channels, chaining, `except*`, errors as a versioned contract |
| `logging_observability_manifest.md` | diagnosable — severity, architecture, structure, correlation, redaction |
| `python_runtime_diagnostics_manifest.md` | diagnosable — attach, dumps, memory, profiling, design-for-diagnosis |
| `python_module_boundaries_manifest.md` | modular — layout, packaging, imports as contract, enforced direction |
| `python_quality_gates_manifest.md` | incremental — the gate ledger, the ratchet, supply chain, measurement |
| `python_concurrency_determinism_manifest.md` | cross-cutting — four models, structured concurrency, determinism |
| `architecture_manifest_default.md` | *agnostic reasoning* — vocabulary, paradigm menu, tradeoffs. No versions, no tags, by design |
| `software_spec_discipline_manifest.md` | *agnostic reasoning* — contract-not-computation, traceability, the `OPEN` split |
| `spec_recovery_reverse_engineering_manifest.md` | adjunct — recovering a spec from code |
| `uml25_ocl_conformance_manifest.md` | adjunct — UML/OCL conformance when a model is required |
| `claude_code_agent_teams_manifest.md` | adjunct — Claude Code agent-team mechanics; not part of the Python spine |

Provenance, the audit record and the 12 house rules these files were written against are in `_work/`.
