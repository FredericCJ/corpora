# Master Research Brief — General JavaScript/TypeScript Safety & Maintainability

**Read this before running any prompt in this folder.** It is the shared preamble every sub-prompt
inherits. It defines the general target, contrasts it with the narrow `../js/` program, restates the
shared protocol compactly, and maps the seven prompts so they do not overlap. Sub-prompts state only
their mission-specific brief and say "apply the master brief."

The epistemic protocol, source-priority rules, and output house style below are **identical to
`../js/00_master_research_brief.md`** — that file is the canonical full statement; this section
summarizes them and then spends its detail on what is *different* about the general domain.

---

## 1. The mission

Produce a citable, decision-grade corpus answering: **how do you make general-purpose,
TypeScript-first JavaScript codebases safe and maintainable — and mechanically enforce it?** The
program follows the escalation ladder **type → lint → practice → ENFORCE**, but the general domain
forces three substrate concerns *ahead* of the ladder that the narrow program never faces: **the
module system, the build pipeline, and the dependency graph.** The load-bearing claim is unchanged:
*a control that can be skipped will be skipped, and unenforced advice decays to zero* — there is
simply far more to enforce here, over far more surface.

## 2. The general target (what "general JS/TS" means here)

Unless a prompt says otherwise, assume:

- **TypeScript is the authored language** (`.ts`/`.tsx`), compiled/emitted — *not* JSDoc-over-`.js`
  (that is the `../js/` program's world). A **build step is normal**, not a decision to justify.
- **Node.js is the primary runtime**, with **Deno, Bun, and edge runtimes** in scope as portability
  targets. Server-side, CLI, and full-stack code are all in scope, not just the browser.
- **Dependencies are real and numerous** — `node_modules`, transitive graphs, lockfiles, and the
  supply chain are first-class concerns (the narrow program explicitly deferred them).
- **Scale is open-ended** — from a single package up to **large codebases, teams, and monorepos**;
  **library publishing** (packages consumed by others) is in scope.
- **Full-stack contracts** — code that crosses the network and database boundaries, where types are
  erased and must be re-established, is in scope.

## 3. Contrast with the `../js/` program (extend, never duplicate)

| Axis | `../js/` (narrow) | This program (general) |
|---|---|---|
| Language form | raw `.js` + JSDoc, tsc as *checker* | authored `.ts`, tsc/bundler *emit* |
| Build | none (a decision to justify) | normal; the pipeline is a topic (03) |
| Runtime | the browser, one realm | Node + Deno/Bun/edge; server + client |
| Dependencies | minimal, hand-audited | many; supply chain is a topic (04) |
| Scale | small, single app | up to monorepo; publishing in scope |
| Boundaries | fetch/storage/URL/DOM, hand-parsed | + DB/env/RPC/GraphQL, schema-driven (05) |

Reference `../js/` (and `../web_manifests/`) wherever a topic is already covered and merely
*specializes* here — do **not** re-derive it:

- **Language-level footguns** (coercion, `this`, mutability, async traps) are largely runtime-shared;
  reference `../js/01_language_safety_subset_prompt.md`'s catalogue and cover only the TS-specific and
  Node-specific deltas.
- **The pedantic-linter base doctrine** (division of labor, suppression hygiene, the curated rule
  taxonomy) lives in `../js/03_pedantic_linter_prompt.md`; prompt 06 here covers the *scale, TS-authored,
  framework, and monorepo* deltas.
- **The maintainability-metric catalogue** (cognitive complexity, coupling, churn/hotspots) lives in
  `../js/06_maintainability_metrics_prompt.md`; reference it rather than restating the metrics.
- **The layered-defense + fitness-function model** lives in `../js/05_enforcement_quality_gates_prompt.md`;
  prompt 07 here covers the *monorepo, publishing, and scale* deltas.

## 4. Version anchor

**mid-2026.** Date every version-dependent fact, tag it **VERSION-DEPENDENT**, verify against a
**primary changelog**, and flag it for re-verification. The general-JS/TS toolchain moves *faster*
than the browser platform: TypeScript 6.0 GA / 7.0 "Corsa" RC, ESLint 9 flat config, typescript-eslint
majors, Vite/Rolldown, pnpm, Zod v4-era schema libraries, Nx/Turborepo, Node LTS lines, Deno 2 / Bun 1
— treat every version number as perishable and name-plus-verify rather than asserting from memory. The
shared version hub is `../web_manifests/web_platform_baseline_manifest.md` (§3 ES editions, §7
toolchain); this program adds the bundler/package-manager/monorepo/schema-library facts.

## 5. Epistemic protocol (summary — full statement in `../js/00_master_research_brief.md` §5)

Tag every material claim **ESTABLISHED** (spec-normative / long-stable / primary-sourced),
**VERSION-DEPENDENT** (edition/runtime/tool-version-bound; dated), or **OPEN** (no authority /
project-policy / genuinely contested). Distinguish spec-fact from convention from opinion; on
contested questions present the strongest case for each position *before* the decision-grade
recommendation; separate a tool's *claims* from what is *demonstrated* (report the limitation set);
prefer primary sources and changelogs; cite with URL + access date; empirical claims need empirical
sources.

## 6. Source priority (summary)

(1) Normative specs — TC39/ECMA-262, WHATWG, W3C, and the **Node.js API docs** + **`package.json`/
`exports` (Node) spec**. (2) Official tool docs + changelogs — TypeScript, the bundlers (Vite,
esbuild, Rollup, webpack, Rspack, tsup), SWC/oxc, the package managers (npm, pnpm, yarn), ESLint/
typescript-eslint, the schema libraries (Zod, Valibot, ArkType, TypeBox), the monorepo tools (Nx,
Turborepo), changesets, publint/attw. (3) MDN + web.dev/Baseline for platform features. (4) Named
practitioners as *opinion* (critique, don't canonize). (5) Empirical SE literature for empirical
claims (supply-chain incidence, metric validity).

## 7. Output house style (summary — full in `../js/00_master_research_brief.md` §7)

Every deliverable: a **TL;DR** (3–6 load-bearing decisions); numbered sections; the tag legend and
consistent tagging; **decision-grade recommendations** (do X, and here's the tradeoff); a **VERSION
MATRIX**; an **ANTI-PATTERN / smell checklist**; a **DECISION FLOWCHART/checklist** where apt; a
**"what this CANNOT do / residual risk"** section; a **Sources** list (URL + access date); and
**cross-references** by filename + section. Dense, decision-oriented prose; no filler.

## 8. The sub-prompt boundary map (read to avoid overlap)

- **01 — TypeScript & the type system.** Authored-TS type design: the strict config, the full
  type-system spectrum, and the *discipline* of rich-vs-over-engineered types. Owns type-level design;
  hands runtime validation to 05 and lint enforcement to 06.
- **02 — Modules, packages & runtime.** ESM/CJS interop, `package.json` `exports`/`imports`, module
  resolution, the multi-runtime landscape. The substrate the type checker and bundler both sit on.
- **03 — Build, bundle & compile.** The pipeline: transpile-≠-typecheck, the bundler/compiler
  landscape, tree-shaking, source maps, targets, determinism, performance. Consumes 02's module facts.
- **04 — Dependencies & supply chain.** Package managers, lockfiles, dependency hygiene/minimization,
  and the supply-chain threat surface. The `../js/` program's biggest deferral, owned here.
- **05 — Boundary & runtime type-safety.** Where erased types must be re-established: schema-first
  validation, end-to-end typing (RPC/GraphQL/OpenAPI/DB), typed env. Industrializes the narrow
  program's hand-rolled parse-don't-validate.
- **06 — Linting, static analysis & practice.** Type-aware linting at scale, framework plugins,
  formatting, dead-code/duplication analysis, and the TS coding-practice deltas — each routed to its
  mechanism. *Defines* checks; 07 *wires* them. References `../js/03`+`../js/04` for the shared base.
- **07 — Architecture, monorepo & enforcement (the payoff).** Enforced module boundaries, monorepo
  tooling, project references, library-publishing gates (publint/attw/api-extractor/changesets), and
  the reproducible, ratchetable CI gate stack at scale. References `../js/05` for the base model.

## 9. How to run

Each prompt is self-contained. Run one in isolation, or the whole program `01 → 07`. Run as a
program, later prompts cite earlier outputs (07 wires 01/06's checks; 03 consumes 02; 05 and 01 share
the schema↔type seam). Each output contract names the manifest to produce and a suggested filename.

## 10. Pitfalls for the researcher (general-domain failure modes)

1. **"Best practice" that assumes one framework.** Most content assumes React/Next; separate
   framework-agnostic doctrine from framework-specific advice, and mark which is which.
2. **Transpile/typecheck confusion.** Bundlers strip types without checking them; never imply the
   build validates types (03).
3. **ESM/CJS hand-waving.** The interop rules are exact and version-bound; get them right (02).
4. **Version drift, accelerated.** The general toolchain churns fast — changelog-verify everything.
5. **Tool marketing.** "Zero-config," "10× faster," "fully type-safe" are claims; find the
   demonstrated limitation set (esp. build tools and end-to-end-typing libraries).
6. **Supply-chain FUD vs evidence.** Cite incidence and mechanism, not fear (04).
7. **Recommending a monorepo/heavy tooling by default.** Scale the recommendation to the codebase;
   polyrepo + pnpm workspaces is often enough (07).
8. **Goodhart on metrics** — inherit the diagnostic-not-target discipline from `../js/06`.

## 11. Optional extensions (flag, don't assume)

If the program should grow: a dedicated **testing & verification** mission (Vitest/Jest/node:test,
unit→integration→e2e, typed testing, contract testing, coverage at scale) — this program treats tests
only as a *gate* (07), not a strategy; and a **performance & bundle-budget** mission (bundle analysis,
Core Web Vitals, runtime perf) if shipping size/latency is a first-class concern. Both are out of
scope for the core seven unless the target changes.
