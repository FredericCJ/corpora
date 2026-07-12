# Deep-Research Prompt 07 — Architecture, Monorepos, Publishing & Enforcement at Scale

**Part of** the General JS/TS Safety & Maintainability program. **Apply `00_master_research_brief.md`**
for the general target, version anchor (mid-2026), epistemic protocol, source priority, and output
house style. This file adds only the mission-specific brief. **This is the program's payoff** — the
enforcement layer that makes everything upstream non-optional, at scale.

---

## Mission (the one question)

**How do you mechanically enforce type-safety, linting, boundaries, and release correctness across a
large, possibly-monorepo, possibly-published TS/JS codebase — enforced module boundaries, monorepo
task orchestration and project references, library-publishing gates, and a reproducible, ratchetable
CI gate stack — as of mid-2026?**

## The mess this addresses

Every upstream discipline (types 01, modules 02, build 03, deps 04, boundaries 05, lint 06) is inert
unless something makes it non-optional — and at scale the enforcement problem itself becomes hard:
type-checking and linting a monorepo is slow, module boundaries erode without a gate, a published
package ships a broken `exports` map that no local test caught, and a large legacy codebase can't have
maximal strictness switched on without ten thousand errors. `../js/05_enforcement_quality_gates_prompt.md`
establishes the base model (layered defense, fitness functions, ratcheting, reproducibility, "make the
right thing the only easy thing"). This prompt covers the deltas that only appear at scale: **monorepo
orchestration, project references, enforced package boundaries, library-publishing correctness, and
affected/cached CI**.

## Scope

- **In:** enforced module/package boundaries at scale; monorepo tooling & task orchestration; TS
  project references; library-publishing discipline and its gates; the CI gate stack with affected/
  incremental/cached execution; ratcheting a large legacy TS codebase; reproducibility at scale.
- **Out / defer:** the base layered-defense model, git-hook/staged/commitlint tooling, mutation
  testing, the fitness-function *concept*, and the ratchet *philosophy* → `../js/05` (reference,
  extend the scale deltas only); the *checks themselves* → prompts 01/03/06 (defined there, *wired*
  here); *test strategy* → deferred to the optional testing mission (tests are run as a *gate* here,
  not designed).
- **Do NOT duplicate** `../js/05`; state what changes at scale.

## Research decomposition (find answers to these)

### A. Enforced module & package boundaries (architecture as an executable gate)
- Encoding boundaries mechanically: **eslint-plugin-boundaries** / import restrictions,
  **dependency-cruiser** forbidden-dependency + no-cycle rules, and **monorepo tag/boundary rules**
  (Nx module boundaries; Turborepo/pnpm conventions). Enforcing layering (core↛shell, feature↛feature),
  a **public API per package** (no deep cross-package imports — ties to prompt 02 `exports`
  encapsulation), and **no dependency cycles** at both file and package granularity. (The
  *fitness-function* concept is `../js/05`; here it is applied at package scale.)

### B. Monorepo tooling & orchestration (survey + when-each, VERSION-DEPENDENT)
- **Nx** vs **Turborepo** vs **pnpm/Yarn workspaces + changesets alone** vs **Rush/Bazel**: task
  graph, **affected/incremental** execution, **local + remote caching**, project graph, code-sharing,
  generators. **When a monorepo is worth it** vs polyrepo (scale the recommendation — the master
  brief's anti-default-heavy-tooling pitfall); the "start with workspaces, add Nx/Turbo when task
  orchestration hurts" path.

### C. TypeScript project references
- **Composite projects / `references` / `--build`** for incremental, ordered type-checking across a
  monorepo; the perf story and its sharp edges; when project references vs a bundler-native / single-
  tsconfig approach; interaction with `tsgo`/TS 7 (cross-ref 01); the "type-check is a separate gate
  from build" doctrine (cross-ref 03) applied across packages.

### D. Library-publishing discipline (correctness for packages consumed by others)
- The publishing gates: **publint** and **`@arethetypeswrong/cli` (attw)** as required checks (they
  enforce prompt 02's `exports`/`types`/dual-package rules); **`.d.ts` emit** + **api-extractor**
  (`.d.ts` rollup + **API report** for reviewable public-surface changes); **semver discipline** and
  **changesets** (versioning + changelog automation across a monorepo); **npm provenance** on publish
  (cross-ref 04); `files`/`.npmignore`, `prepublishOnly`/`publish` gates; **API surface stability** as
  a reviewed artifact.

### E. The CI gate stack at scale
- The stages — install (**frozen lockfile**, corepack-pinned PM — cross-ref 04) → typecheck
  (`tsc --noEmit` / project-reference `--build`) → lint (type-aware, `--max-warnings 0`) →
  format-check → test (as a gate) → **attw/publint** (for libs) → build → fitness functions →
  dead-code (**knip**). **Affected-only** execution + **remote cache** for monorepo speed; **required
  status checks / branch protection**; the **"green means green"** rule (no `|| true`); the single
  aggregate **`check`** task humans and CI share (local↔CI parity).

### F. Ratcheting a large legacy TS codebase (the adoption key at scale)
- You cannot switch on maximal strictness/lint across a big codebase at once. The scale playbook:
  **per-package strictness** (strict new packages, grandfather old); **strict-flag-at-a-time** (cross-
  ref 01/`../js/02`); **`betterer`** to ratchet arbitrary checks (types, lint, complexity); ESLint
  baseline/warn→error migration; boundary rules added as warn then error; **hotspot-first** cleanup
  order (cross-ref `../js/06` churn×complexity). Gate on **"no new debt,"** burn down over time.

### G. Reproducibility & the golden path at scale
- Pin the **entire toolchain** (package manager via corepack, Node via `.nvmrc`/Volta/`engines`, all
  tools in the lockfile — cross-ref 03/04); deterministic checks; **local↔CI parity** via shared
  config packages and one `check` script; the **golden path** — generators/scaffolding (Nx generators,
  templates) that produce compliant packages, shared configs *as packages*, defaults over docs; and
  avoiding **gate-bankruptcy** at scale (slow/noisy gates get bypassed — affected+cache is what keeps
  a big gate fast enough to stay green).

## Controversies to resolve (positions first, then a recommendation)

- **Monorepo vs polyrepo**; and within monorepo, **Nx vs Turborepo vs workspaces-only** — keyed to
  team/repo scale.
- **TS project references vs single-tsconfig vs bundler-native** type-checking at scale.
- **Dual ESM/CJS vs ESM-only** publishing (the release side of prompt 02/03's controversy).
- **Remote build cache** (esp. hosted/proprietary) — speed vs trust/lock-in.
- How strict a gate a large org can keep **green** without bypass culture.

## Sources to prioritize

**Nx**, **Turborepo**, **pnpm/Yarn workspaces**, **Rush** docs; TypeScript **project references** /
`--build` docs; **publint**, **attw**, **api-extractor**, **changesets** docs; GitHub Actions branch-
protection / required-status-check docs; **betterer** docs; **dependency-cruiser** / **eslint-plugin-
boundaries** docs; Neal Ford et al. *Building Evolutionary Architectures* (fitness functions — the
source concept, via `../js/05`). Changelogs for all (VERSION-DEPENDENT). Reference `../js/05`, `../js/06`,
and prompts 01–06.

## Output contract

Produce a ground-truth manifest (suggested filename `ts_architecture_monorepo_enforcement_manifest.md`):
TL;DR (the enforce-boundaries + affected/cached-gate + publishing-correctness + ratchet-at-scale
thesis, framed as deltas over `../js/05`); the **enforced-boundary** cookbook (tool → boundary rule);
the **monorepo tooling** decision table (tool → orchestration → caching → fits → when-worth-it); the
**project-references** guidance; the **library-publishing gate** stack (publint/attw/api-extractor/
changesets/provenance); the **CI gate stack at scale** (stages + affected/cache + the aggregate `check`
task); the **legacy-ratchet-at-scale** playbook; the **reproducibility + golden-path** checklist; a
version matrix; a **gate-smell** anti-pattern checklist (`|| true`, unpinned PM, no affected/cache →
bypass, broken-`exports`-shipped, no-API-report, boundary-rules-never-promoted-to-error); sources;
cross-references.

## Cross-references

**Wires** prompts 01 (type gate + project references), 03 (build gate, separate from typecheck), 06
(lint/dead-code gate), 05 (shared-contract packages, contract tests), and 04 (frozen-lockfile install,
provenance). Enforces prompt 02's `exports` correctness via publint/attw. Extends `../js/05` (base
enforcement model) and consumes `../js/06` (hotspot-ordered ratcheting). The convergence point of the
whole program.
