# Deep-Research Prompt 03 — The Build, Bundle & Compile Pipeline

**Part of** the General JS/TS Safety & Maintainability program. **Apply `00_master_research_brief.md`**
for the general target, version anchor (mid-2026), epistemic protocol, source priority, and output
house style. This file adds only the mission-specific brief.

---

## Mission (the one question)

**How do you assemble a safe, maintainable, reproducible build pipeline for TS-first JavaScript — the
correct separation of transpilation from type-checking, the bundler/compiler landscape and when each
fits, and the tree-shaking, source-map, target, determinism, and performance concerns — as of
mid-2026?**

## The mess this addresses

The build is where a project silently trades safety for convenience: bundlers **strip types without
checking them**, so a green build can ship type errors; misconfigured targets downlevel modern code
into slow polyfilled sludge or ship syntax an old runtime can't parse; broken source maps make
production errors untraceable; non-deterministic builds make "works on my machine" a debugging tax;
and config sprawl across esbuild/SWC/Rollup/webpack becomes its own unmaintainable subsystem. The
narrow `../js/` program avoids all of this by having no build — a valid special case this prompt
references but does not adopt.

## Scope

- **In:** the transpile-≠-typecheck doctrine; the bundler + compiler/transformer landscape;
  tree-shaking/DCE; source maps; targets/downleveling/polyfilling; minification & code-splitting;
  build determinism/reproducibility; build performance; app-build vs library-build differences.
- **Out / defer:** the *module contract* the build must honor (`exports`, ESM/CJS) → prompt 02
  (consumed here); *dependency installation* → prompt 04; *CI orchestration / caching across a
  monorepo* → prompt 07 (this prompt owns single-project build correctness; 07 owns orchestration);
  *type-system* settings → prompt 01.
- **Do NOT duplicate** prompt 02's `package.json`/resolution rules; reference them.

## Research decomposition (find answers to these)

### A. The transpile-≠-typecheck doctrine (the load-bearing separation)
- Why fast transpilers (**esbuild**, **SWC**, oxc, Babel) and bundlers **erase types without checking
  them** — and therefore **`tsc --noEmit` must run as a separate, independent gate** (owned by prompt
  07's CI, defined by prompt 01's config). The consequences for authoring: **`isolatedModules`** (each
  file transpiled alone) forbids const-enum cross-file use and certain type-only re-exports →
  **`verbatimModuleSyntax`** (cross-ref 01/02). State this as a firm doctrine.

### B. The bundler landscape (survey + when-each, VERSION-DEPENDENT)
- **Vite** (dev: native-ESM + esbuild; prod: Rollup — and the **Rolldown** Rust-bundler transition,
  status at anchor) — the mainstream app default; **esbuild** (fast, simpler, fewer guarantees);
  **Rollup** (library-grade output, plugin ecosystem); **webpack** (legacy incumbent, max ecosystem);
  **Rspack**/**Turbopack** (Rust webpack-compatible / Next's bundler); **tsup** (zero-config library
  bundling over esbuild); **Parcel**. For each: what it's good at, the guarantees it makes, and the
  target project shape it fits.
- **App bundling vs library bundling** — different jobs: apps optimize for the browser (splitting,
  hashing, asset handling); libraries preserve modules, externalize deps, emit types and dual/ESM
  output (ties to 07's publishing).

### C. Tree-shaking & dead-code elimination
- The ESM requirement; the **`sideEffects`** field; `/*#__PURE__*/` annotations; why CJS and certain
  patterns (dynamic access, re-export barrels) defeat shaking; measuring what actually shipped.

### D. Source maps (traceability into production)
- Map types and quality; **hidden source maps** uploaded to an error-tracking service (ties to the
  observability discipline) so production stack traces resolve to source without shipping maps to
  users; the security caveat (don't expose source maps publicly if the source is sensitive).

### E. Targets, downleveling & polyfilling
- **`target`/`lib`** and **browserslist**; the "**don't downlevel more than the runtime needs**"
  performance point (over-downleveling bloats and slows); polyfilling strategy (core-js, targeted vs
  global) vs assuming a modern Baseline (cross-ref `../web_manifests/web_platform_baseline_manifest.md`
  §2–3); the interaction between TS `target` and the bundler's own target.

### F. Determinism & reproducibility (a build you can't reproduce isn't trustworthy)
- Pinned tool versions + committed lockfile (cross-ref 04); deterministic output (stable hashing,
  stable chunk names); avoiding non-determinism sources (timestamps, ordering, ambient env); the
  reproducible-build goal and how close the JS toolchain gets.

### G. Build performance
- Where build time goes; native-speed transformers (esbuild/SWC/oxc/Rolldown); caching (persistent/
  incremental); the dev-server (HMR) vs production-build split; the "type-check in parallel, not in
  the hot path" pattern (fork-ts-checker-style / separate `tsc` job).

## Controversies to resolve (positions first, then a recommendation)

- **Bundle vs no-bundle** for apps in 2026 (native ESM + HTTP/2 vs bundling) — when is a build still
  worth it (reference `../js/` and `../web_manifests/` §4)?
- **Vite/Rolldown vs esbuild-direct vs Rollup/tsup** for libraries.
- **Betting on Rust-based tooling** (Rolldown, Rspack, oxc, SWC) maturity vs the established JS/Go
  incumbents at the anchor.
- **Babel's** residual role (or obsolescence).
- **ESM-only library output** vs dual — the build-complexity side of prompt 02's controversy.

## Sources to prioritize

Docs + changelogs for **Vite/Rolldown, esbuild, Rollup, webpack, Rspack, Turbopack, tsup, SWC, oxc,
Parcel**; the TypeScript handbook on `isolatedModules`/`verbatimModuleSyntax`/emit; browserslist docs;
source-map spec + error-tracking-service upload docs; reproducible-builds discussions (as opinion).
Separate each tool's *claims* from *demonstrated* benchmarks and limitation sets (master brief §10.5).

## Output contract

Produce a ground-truth manifest (suggested filename `js_build_pipeline_manifest.md`): TL;DR (the
transpile-≠-typecheck doctrine + the bundler-selection thesis); the **transpile-vs-typecheck**
doctrine and its authoring constraints; the **bundler/compiler landscape** table (tool → strength →
guarantees → fits); **app-vs-library build** guidance; tree-shaking, source-map, target/downlevel,
determinism, and performance sections each with decision-grade recommendations; a version matrix; an
anti-pattern checklist (green-build-ships-type-errors, over-downleveling, public source maps,
non-deterministic output, barrel-defeated shaking, config sprawl); sources; cross-references.

## Cross-references

Emits the module contract prompt 02 defines and prompt 07 gates (publint/attw); runs the type gate
prompt 01 configures as a *separate* step (wired by prompt 07); its determinism depends on prompt 04's
lockfile. References `../js/` and `../web_manifests/web_platform_baseline_manifest.md` §4 for the valid
no-build special case.
