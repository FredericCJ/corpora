# JavaScript Safety & Maintainability — Deep-Research Prompt Program

**What this is.** A coordinated set of **deep-research prompts**. Each, when run through a
research harness, produces one *ground-truth manifest* — a citable, decision-grade document in the
exact house style of the sibling collection `../web_manifests/`. Together they answer one question:

> **How do you make raw, browser-native JavaScript safe and maintainable — and mechanically
> enforce it — under a no-build, reuse-first, small-scale posture?**

**Why it exists.** The seven manifests in `../web_manifests/` establish architecture, typing
*foundations*, testing, error-tracing, observability, spec discipline, and the platform baseline.
They deliberately **defer** the "make it stick" layer — the typing manifest leaves the lint stack
and the `any`/assertion CI gate OPEN; the error and observability manifests say "adopt a lint rule
banning X" without saying which or how. This program closes those gaps and extends the collection
along the axis the user named: **static typing → pedantic linting → coding practices →
enforcement**, plus the diagnosis and measurement that bracket them.

## The escalation ladder (the throughline)

Static typing is a *good start*. A pedantic linter is *very nice*. A set of coding practices is
*also nice*. **A way of enforcing all of it is the point** — advice that isn't mechanically
enforced decays to zero. Two more missions bracket the ladder: a **diagnosis** of what is
intrinsically messy about JS (so the middle layers target real hazards), and a **measurement**
layer (so "maintainable" is observed, not asserted).

## The files

| File | Role |
|---|---|
| `00_master_research_brief.md` | **Read first.** Shared mission, version anchor, epistemic protocol, source-priority rules, output house style, the sub-prompt boundary map, and researcher pitfalls. Every prompt inherits this. |
| `01_language_safety_subset_prompt.md` | **Diagnosis.** The intrinsic JS footguns and the maximal-safety modern subset; each hazard classified as type-catchable / lint-catchable / feature-eliminated / contract-only. |
| `02_static_typing_enforcement_prompt.md` | **Typing.** *Deepens* the typing manifest along enforcement: type-coverage measurement + gating, `any`/assertion/`@ts-expect-error` debt ratcheting, the full strictness dial, untyped-→-strict migration, the JSDoc-vs-TS-vs-TC39 decision. |
| `03_pedantic_linter_prompt.md` | **Linting.** ESLint flat config + typescript-eslint, the maximal-defensible rule set + plugin ecosystem, custom AST rules, Biome/oxlint, the lint/typecheck/format division of labor, suppression hygiene. |
| `04_coding_practices_conventions_prompt.md` | **Practices.** The idiom + anti-pattern catalogue at function/module/expression altitude, each tagged with *how it is mechanically enforced* (types / a named rule / a fitness function / review-only). |
| `05_enforcement_quality_gates_prompt.md` | **Enforcement (the payoff).** The layered pipeline (editor → pre-commit → CI → merge gate), git-hook + staged-lint + commit-lint tooling, architectural fitness functions, mutation testing, ratcheting for legacy code, reproducibility. |
| `06_maintainability_metrics_prompt.md` | **Measurement.** What to measure to know it's maintainable (cognitive complexity, size, coupling, churn×complexity hotspots), the tool landscape, metric validity, and honest budget-setting under Goodhart. |

## How to use

- **Each prompt is self-contained.** It inlines the essentials and points to
  `00_master_research_brief.md` for the shared protocol. Feed any one to a deep-research tool to
  produce that single manifest.
- **Or run the whole program** in order `01 → 06` (diagnosis → typing → lint → practices →
  enforcement → measurement). Run as a program, later prompts may cite earlier outputs.
- **Outputs** are manifest-style `.md` documents intended to slot beside `../web_manifests/`
  (suggested names are in each prompt's output contract).

## Relationship to `../web_manifests/`

This program **extends, never duplicates** that collection. Every prompt names the sibling
manifest(s) it must reference-and-build-on rather than re-derive. Same version anchor (**mid-2026**),
same tag legend (**ESTABLISHED / VERSION-DEPENDENT / OPEN**), same output discipline. The shared
version hub for platform and toolchain facts remains `../web_manifests/web_platform_baseline_manifest.md`.
