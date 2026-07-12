# Deep-Research Prompt 06 — Linting, Static Analysis & Coding Practice at Scale

**Part of** the General JS/TS Safety & Maintainability program. **Apply `00_master_research_brief.md`**
for the general target, version anchor (mid-2026), epistemic protocol, source priority, and output
house style. This file adds only the mission-specific brief.

---

## Mission (the one question)

**What is the maximally-pedantic-yet-defensible static-analysis and coding-practice layer for a
TS-first, framework-using, potentially large codebase — type-aware linting that stays fast at scale,
the framework-specific rule sets, formatting, dead-code/duplication analysis, and the TS-specific
practice deltas — each routed to the mechanism that enforces it, as of mid-2026?**

## The mess this addresses

The narrow `../js/03_pedantic_linter_prompt.md` establishes the base linting doctrine — division of
labor with the type-checker and formatter, the curated rule taxonomy, suppression hygiene. The general
domain adds what that program never faces: **type-aware linting on a real multi-project TS codebase
where lint performance becomes a gating problem**, **framework footguns** (React hook-dependency bugs,
missing a11y attributes, Vue/Svelte reactivity traps) that only framework-specific rules catch,
**monorepo config sharing**, and a larger surface of dead code, duplication, and cross-package
practice drift. This prompt covers those deltas — and folds in the TS-specific coding-practice layer,
each practice tagged with its enforcement mechanism.

## Scope

- **In:** typescript-eslint type-aware linting at scale (the project-service model, performance);
  flat-config sharing across a monorepo; **framework plugins**; formatting at scale; the fast
  alternatives (Biome/oxlint) for TS; **static analysis beyond lint** (dead-code, duplication,
  dependency graph as *measurement*); and the **TS coding-practice deltas** with an enforceability
  mapping.
- **Out / defer:** the base rule taxonomy, division-of-labor doctrine, suppression hygiene, custom-AST-
  rule cookbook → `../js/03_pedantic_linter_prompt.md` (reference, extend the deltas only); the
  general practice/anti-pattern catalogue and its enforceability-mapping *method* →
  `../js/04_coding_practices_conventions_prompt.md` (reference); the maintainability *metric
  catalogue* → `../js/06_maintainability_metrics_prompt.md`; *architectural boundary enforcement as a
  gate* → prompt 07 (this prompt measures/lints; 07 gates).
- **Do NOT duplicate** the `../js/` base doctrine; state the deltas.

## Research decomposition (find answers to these)

### A. Type-aware linting at scale
- **typescript-eslint** type-checked rules on a real `.ts` project: the **`projectService`** model vs
  legacy `parserOptions.project`; **performance** as the scaling problem (type info is expensive) and
  the mitigations (project service, caching, running on **affected** files only — cross-ref 07,
  scoping type-aware rules to a separate slower job); the tseslint **recommended / strict /
  stylistic** tiers and their **`*-type-checked`** variants; the `tseslint.config()` helper.
- **Flat-config sharing across a monorepo** — a shared config *package*, per-package overrides,
  keeping one source of truth.

### B. Framework-specific rule sets (the footgun-catchers the base set can't)
- **React**: `eslint-plugin-react` + **`react-hooks`** (rules-of-hooks, **exhaustive-deps** — the
  stale-closure bug catcher), `jsx-a11y`, the React-Compiler-era lint story (verify at anchor).
- **Vue** (`eslint-plugin-vue`), **Svelte** (`eslint-plugin-svelte`), **Angular**
  (`@angular-eslint`), **Solid**, **Astro**, framework meta-configs (e.g. `eslint-config-next`). For
  each: the class of framework-specific bug it prevents. Keep framework-specific advice **clearly
  marked** as such (master brief §10.1).

### C. Formatting at scale
- **Prettier** vs the **Biome** formatter as the org-wide standard; determinism; the "format is not
  lint" boundary (disable conflicting stylistic rules — reference `../js/03` §D); running format-check
  as a gate (cross-ref 07); config as a shared package.

### D. The fast alternatives for TS (maturity assessment — claim vs demonstrated)
- **Biome** and **oxlint** for TS: rule coverage vs typescript-eslint, **whether they do type-aware
  rules** at the anchor (the decisive limitation), framework-plugin coverage, and the realistic
  pattern (fast pre-filter/format via Biome/oxlint; typescript-eslint for the type-aware depth).
  Report the demonstrated limitation set.

### E. Static analysis beyond lint (measurement side)
- **knip** (unused files/exports/deps — supersedes ts-prune-style tools); **jscpd** (copy-paste
  duplication); **dependency-cruiser/madge** (dependency graph, cycles — *measurement* here; the
  *gate* is prompt 07); **SonarJS/SonarQube** at scale; **type-coverage** (cross-ref `../js/02`).
  Which fit an in-CI lightweight stack vs a heavyweight platform.

### F. The TS coding-practice deltas (with enforceability mapping)
- Practices distinct to authored TS: the **`any`/`unknown`/assertion** discipline in practice
  (enforced by `no-unsafe-*`/`no-explicit-any`); **error handling** (Result-type vs `throw` in TS;
  typed errors; `unknown` in catch); **async** patterns (`no-floating-promises` needs type info);
  **immutability** (`readonly`/`Readonly<T>`/`as const`, and the Immer question); **exhaustiveness**
  (`switch`/`assertNever` — enforceable via `switch-exhaustiveness-check`); import hygiene at scale
  (`import type`, no-cycles, ordering). For each: **enforced by types / a named lint rule / a fitness
  function / review-only** — the routing table (reusing `../js/04`'s method).

## Controversies to resolve (positions first, then a recommendation)

- **Type-aware lint cost vs value** at scale — worth the CI minutes, or reserve for a nightly job?
- **typescript-eslint vs Biome/oxlint** for a serious pedantic TS config in 2026.
- **Prettier vs Biome** formatter org-wide.
- How much **framework-plugin** pedantry (esp. `exhaustive-deps` autofix) is signal vs noise.
- **Result-type error handling vs idiomatic `throw`** in TS.

## Sources to prioritize

typescript-eslint docs (project service, type-checked configs, performance); ESLint flat-config docs;
the framework plugin docs (`react-hooks`, `jsx-a11y`, `eslint-plugin-vue/svelte`, `@angular-eslint`,
`eslint-config-next`); Prettier/Biome/oxlint docs + benchmarks; **knip/jscpd/dependency-cruiser/
SonarJS** docs; changelogs (VERSION-DEPENDENT). Reference `../js/03`, `../js/04`, `../js/06`, `../js/02`.

## Output contract

Produce a ground-truth manifest (suggested filename `ts_linting_static_analysis_manifest.md`): TL;DR
(the type-aware-at-scale + framework-plugins + fold-in-practices thesis, and the deltas-over-`../js/03`
framing); the **type-aware-lint-at-scale** guidance (project service, perf, affected-only, monorepo
config sharing); the **framework rule-set** table (framework → plugin → bug class prevented); the
**formatter** decision; the **Biome/oxlint TS maturity** verdict (claim vs demonstrated); the
**static-analysis-beyond-lint** toolset; the **TS practice-delta enforceability table**; a version
matrix; an anti-pattern checklist (type-aware-lint-in-hot-path, framework-rule-disable-blindness,
format-in-lint, knip-not-run, `any`-tolerated, non-exhaustive-switch); sources; cross-references.

## Cross-references

Extends `../js/03` (base linting) and `../js/04` (practice enforceability method); *measures* what
prompt 07 *gates* (dead code, cycles); consumes prompt 01 (the type rules it enforces) and prompt 05
(schema/boundary practices). Feeds thresholds from `../js/06` (complexity) and reports coverage from
`../js/02`.
