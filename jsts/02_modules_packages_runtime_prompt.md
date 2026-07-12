# Deep-Research Prompt 02 — Modules, Package Boundaries & the Runtime Substrate

**Part of** the General JS/TS Safety & Maintainability program. **Apply `00_master_research_brief.md`**
for the general target, version anchor (mid-2026), epistemic protocol, source priority, and output
house style. This file adds only the mission-specific brief.

---

## Mission (the one question)

**How do you get the module system, the `package.json` package boundary, module resolution, and the
multi-runtime target right — so that ESM/CJS interop, `exports` maps, and runtime portability stop
being a source of build breakage and silent misresolution — as of mid-2026?**

## The mess this addresses

The module and package substrate is where general JS/TS wastes the most time on non-features:
dual-published packages that resolve to the wrong file, `exports` maps that break `types` resolution,
`ERR_REQUIRE_ESM` and default-interop surprises, `.js`-extension confusion under `nodenext`, and code
that runs on Node but not on the edge. None of this is business logic; all of it is avoidable with a
correct mental model and a few enforced settings. The narrow `../js/` program never faces it (one
realm, no packages, no build); the general program cannot avoid it.

## Scope

- **In:** ESM vs CJS and their interop; the `package.json` publishing/consumption fields
  (`type`/`main`/`module`/`browser`/`exports`/`imports`/`typesVersions`); TypeScript module settings
  (`module`, `moduleResolution`, `verbatimModuleSyntax`, extensions); the runtime landscape (Node/
  Deno/Bun/edge) and its portability tax; resolution debugging.
- **Out / defer:** the *bundler's* role in producing these outputs → prompt 03 (this prompt owns the
  *contract*, 03 owns *emitting* it); dependency *installation/management* → prompt 04; library
  *publishing correctness gates* (publint/attw) → prompt 07 (this prompt explains the rules they
  check); *type-system* semantics of `import type` → prompt 01.
- **Do NOT duplicate** prompt 03's bundler survey; reference it.

## Research decomposition (find answers to these)

### A. ESM vs CJS — the interop reality
- The two module systems' semantics (static `import`/`export` + live bindings + async graph vs
  `require`/`module.exports` + synchronous + dynamic); **the interop matrix**: importing CJS from ESM
  (default-interop, named-export detection via cjs-module-lexer), importing ESM from CJS
  (historically async-only; **Node's newer synchronous `require(esm)` support** — status/constraints
  at the anchor, VERSION-DEPENDENT), `__dirname`/`__filename` vs `import.meta.url`/`import.meta.dirname`.
- The **dual-package hazard** (a package loaded as both ESM and CJS → two instances, broken
  `instanceof`/singletons) and how `exports` + ESM-only publishing mitigate it.
- The stance: **ESM-first (or ESM-only) authoring**; when CJS output is still required and how to
  provide it safely.

### B. The `package.json` package boundary
- **`"type"`** (`module` vs `commonjs`) and `.mjs`/`.cjs`/`.mts`/`.cts` overrides.
- The **`exports`** field: conditional exports (`import`/`require`/`types`/`default`/`node`/`browser`/
  `development`/`production`), subpath exports, the **`types` condition ordering rule** (must come
  first), encapsulation (blocking deep imports), and the legacy `main`/`module`/`browser`/
  `typesVersions` fields it supersedes.
- The **`imports`** field (internal `#`-prefixed subpath imports) for internal aliasing without a
  bundler.
- Self-referencing; `sideEffects` (the tree-shaking hint — cross-ref 03).

### C. TypeScript's module settings (aligning the checker with reality)
- **`module`** and **`moduleResolution`**: `bundler` (when a bundler resolves) vs `node16`/`nodenext`
  (when Node resolves — enforces `exports`, extensions, conditions) vs the legacy `node`/`classic`;
  which to pick for an app vs a library.
- **Extensioned imports** under `nodenext` (`import './x.js'` from `x.ts`), `allowImportingTsExtensions`
  (+ `noEmit`/bundler), and why the extension rules exist.
- **`verbatimModuleSyntax`** and `import type`/`export type` — type-elision correctness, and its
  interaction with `isolatedModules` (cross-ref 01/03).

### D. The runtime landscape (the portability tax)
- **Node.js** (the current LTS line at the anchor — verify), its module + `exports` resolution as the
  reference; built-in modules (`node:` protocol).
- **Deno** (native TS, secure-by-default permissions, `npm:`/`jsr:` specifiers, `deno.json`) and
  **Bun** (speed, Node-compat surface, built-in tooling) — where each diverges from Node.
- **Edge runtimes** (Cloudflare Workers, Vercel Edge, Deno Deploy) — the **Web-API-only subset** (no
  Node built-ins, no filesystem), and designing for portability across them.
- **Runtime detection & the portability discipline:** targeting the intersection (Web APIs) vs
  gating Node-specific code; the WinterCG/WinterTC common-minimum-API effort (status at anchor).

### E. Resolution debugging & correctness
- `tsc --traceResolution`, `--explainFiles`; **`@arethetypeswrong/cli` (attw)** and **`publint`** as
  the tools that catch broken `exports`/`types`/dual-package setups *before* publishing (the *gates*
  are prompt 07; the *failure modes* they detect are enumerated here).

## Controversies to resolve (positions first, then a recommendation)

- **ESM-only vs dual ESM/CJS publishing** in 2026 — is CJS output still worth the complexity?
- **`moduleResolution: bundler` vs `nodenext`** for a library (the "author to Node's rules even if a
  bundler consumes you" argument).
- Extensioned imports: annoyance vs correctness.
- Betting on Node-compat in Bun/Deno vs authoring to the Web-API intersection.

## Sources to prioritize

The **Node.js** docs (ESM, `package.json` `exports`/`imports`, `require(esm)`, module resolution
algorithm); the **TypeScript** handbook (modules, `moduleResolution` reference, the "Modules —
Reference"/"Choosing Compiler Options" pages); **attw** and **publint** docs (the failure taxonomy);
**Deno** and **Bun** docs (compat matrices); **WinterCG/WinterTC** common-API work; the "Are ESM and
CJS reconciled yet" ecosystem write-ups (as opinion). Changelogs for all (VERSION-DEPENDENT).

## Output contract

Produce a ground-truth manifest (suggested filename `js_modules_packages_runtime_manifest.md`): TL;DR
(the ESM-first + `exports`-correct + resolution-aligned thesis); the **ESM/CJS interop matrix**; the
**`package.json` field reference** (field → purpose → correct usage → the hazard it prevents); the
**TS module-settings decision** (app vs library table); the **runtime portability matrix** (feature/
API → Node/Deno/Bun/edge); the **resolution-debugging** toolset and the failure taxonomy attw/publint
catch; a version matrix; an anti-pattern checklist (dual-package hazard, `types`-condition-last,
deep-import leakage, CJS-in-ESM default-interop bugs, Node-API on the edge); sources; cross-references.

## Cross-references

The contract that prompt 03 (build) emits and prompt 07 (publishing gates: publint/attw) enforces;
shares emit flags with prompt 01; the runtime targets constrain prompt 04 (native deps) and prompt 05
(which runtime APIs exist for boundaries). References `../web_manifests/web_platform_baseline_manifest.md`
§4 (ESM/import maps) for the browser-native baseline.
