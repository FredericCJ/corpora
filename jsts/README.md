# General JavaScript/TypeScript Safety & Maintainability — Deep-Research Prompt Program

**What this is.** A coordinated set of **deep-research prompts**. Each, when run through a research
harness, produces one *ground-truth manifest* — a citable, decision-grade document in the house
style of `../web_manifests/`. Together they answer one question:

> **How do you make general-purpose, TypeScript-first JavaScript codebases — with a build step,
> running on Node and beyond, dependency-rich, and potentially large-scale, full-stack, or
> published as libraries — safe and maintainable, and mechanically enforce it?**

**Distinct from the `../js/` program — on purpose.** The `../js/` program targets a deliberately
narrow niche: raw browser JS, no build step, JSDoc-as-types, minimal dependencies, small single-realm
apps. **This program is its complement**: the professional, tooling-rich, TS-first mainstream where a
compiler and bundler are normal, `node_modules` is large, code spans packages and runtimes, and the
"mess" lives in places the narrow program never has to face — ESM/CJS interop, `exports` maps,
bundler configuration, the supply chain, monorepo boundaries, and type-safety across the network and
database boundaries where types are erased.

The two programs share conventions (version anchor **mid-2026**, the ESTABLISHED/VERSION-DEPENDENT/
OPEN tag legend, the epistemic protocol, the output house style) and deliberately **do not duplicate**
each other: where a topic is language-level and already covered narrowly, this program references
`../js/` rather than re-deriving it.

## The throughline

The same escalation the `../js/` program follows — **type → lint → practice → ENFORCE** — but scaled
to the general domain and preceded by the substrate the mainstream cannot ignore: **the module
system, the build pipeline, and the dependency graph**. Advice that isn't mechanically enforced still
decays to zero; the difference here is that there is far more to enforce, across far more surface.

## The files

| File | Role |
|---|---|
| `00_master_research_brief.md` | **Read first.** Mission, the general target definition, the contrast with `../js/`, shared epistemic protocol + house style, the sub-prompt boundary map, researcher pitfalls. |
| `01_typescript_type_system_prompt.md` | **Types.** Authored TypeScript wielded well: the strict config, the full type-system spectrum, and the *type-design discipline* that separates leverage from over-engineering. |
| `02_modules_packages_runtime_prompt.md` | **Substrate I.** ESM/CJS interop, `package.json` `exports`/`imports`, module resolution, and the Node/Deno/Bun/edge runtime landscape. |
| `03_build_bundle_compile_prompt.md` | **Substrate II.** The build pipeline: transpile-≠-typecheck, bundlers/compilers, tree-shaking, source maps, targets, determinism, and build performance. |
| `04_dependencies_supply_chain_prompt.md` | **Substrate III.** Package managers, lockfile discipline, dependency hygiene and minimization, and the supply-chain threat surface (provenance, scripts, audit, SBOM). |
| `05_boundary_runtime_type_safety_prompt.md` | **Where types lie.** Schema-first validation (Zod/Valibot/ArkType/…), end-to-end type safety (tRPC/GraphQL/OpenAPI/typed DB), typed env, illegal-states-unrepresentable. |
| `06_linting_static_analysis_prompt.md` | **Lint & quality.** Type-aware linting at scale, framework plugins, formatting, dead-code/duplication analysis, and the TS coding-practice deltas — each routed to its enforcement mechanism. |
| `07_architecture_monorepo_enforcement_prompt.md` | **Enforcement (the payoff).** Enforced module boundaries, monorepo tooling, project references, library-publishing discipline, and the CI gate stack — reproducible, ratchetable, at scale. |

## How to use

- **Each prompt is self-contained.** It inlines the essentials and points to
  `00_master_research_brief.md` for the shared protocol. Feed any one to a deep-research tool.
- **Or run the whole program** in order `01 → 07`. Later prompts may cite earlier outputs.
- **Outputs** are manifest-style `.md` documents intended to sit beside `../web_manifests/` and the
  `../js/` outputs; suggested filenames are in each prompt's output contract.

## Relationship to the other corpora

Extends `../web_manifests/` (the browser-native ground-truth collection) and complements `../js/`
(the no-build narrow program). Shared version hub for platform/edition/toolchain facts:
`../web_manifests/web_platform_baseline_manifest.md`. This program adds the general-JS/TS tooling and
runtime facts (bundlers, package managers, monorepo tools, schema libraries).
