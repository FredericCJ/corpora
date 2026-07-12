# Deep-Research Prompt 02 — Static Typing: Enforcement, Coverage, Migration & the Approach Decision

**Part of** the JavaScript Safety & Maintainability program. **Apply `00_master_research_brief.md`**
for the version anchor (mid-2026), target context, epistemic protocol, source priority, and output
house style. This file adds only the mission-specific brief.

---

## Mission (the one question)

**For strictly-checked raw JS (tsc `--checkJs` + JSDoc, per the typing sibling), how do you MEASURE
and ENFORCE type safety over time, MIGRATE an untyped codebase to strict, handle untyped
dependencies, and DECIDE between raw-JS+JSDoc and its alternatives (TS-as-language + build; the
TC39 type-annotations / Node type-stripping trajectory; Flow) — as of mid-2026?**

## The mess this addresses

Types you don't *measure* or *enforce* erode: `any` leaks inward, assertions accumulate, strictness
silently regresses at a compiler upgrade, and a half-migrated codebase hands out false confidence.
`js_typing_contract_manifest.md` establishes the type *vocabulary* and the parse-don't-validate
boundary — and **explicitly leaves the enforcement layer OPEN** (§8: "add a CI gate counting
`@ts-expect-error`/`any` occurrences as tracked debt"; the lint stack "OPEN — pin at adoption").
This mission closes exactly those gaps.

## Scope

- **In:** the complete strictness dial + rationale; type-**coverage** measurement and CI gating;
  `any`/assertion/`@ts-expect-error` **debt tracking + ratchet**; untyped-**dependency** strategy;
  the untyped-→-strict **migration** playbook; the **approach decision** matrix; the
  static↔runtime-contract **handshake** (where static stops).
- **Out / defer to sibling:** JSDoc *vocabulary*, branded types, discriminated unions,
  parse-don't-validate *mechanics* → `js_typing_contract_manifest.md` (reference, don't re-derive);
  lint *configuration* → prompt 03; the error-result union → `js_error_tracing_contract_manifest.md`;
  the migration *ordering* by hotspot → consumes prompt 06's churn analysis.
- **Do NOT duplicate the typing sibling.** Cite it as the foundation; build the
  measurement/enforcement/migration/decision layer on top. If you find yourself re-explaining JSDoc
  `@typedef` or branding, stop and reference §2 of the sibling instead.

## Research decomposition (find answers to these)

### A. The strictness dial, completely
- Enumerate **every** compiler flag that tightens checking beyond the `strict` umbrella —
  `noUncheckedIndexedAccess`, `exactOptionalPropertyTypes`, `noImplicitOverride`,
  `noFallthroughCasesInSwitch`, `noImplicitReturns`, `noUnusedLocals`/`noUnusedParameters`,
  `noPropertyAccessFromIndexSignature`, `allowUnreachableCode: false`, `verbatimModuleSyntax`,
  `isolatedModules`/`isolatedDeclarations` (relevance under no-build?), and the `strict`-family
  members themselves (`strictNullChecks`, `noImplicitAny`, `useUnknownInCatchVariables`, …).
- For each: **what it catches**, its false-positive/ergonomic cost, and a **verdict** for
  raw-JS+JSDoc specifically (some flags behave differently checking `.js` than `.ts`).
- The recommended **maximal-defensible `tsconfig.json`** — committed, version-pinned — as a
  concrete artifact with per-flag rationale.
- What changed at **TS 6.0** (strict / ESM / `target: es2025` became defaults) and **TS 7.0** (Go
  "Corsa" port, ~10× faster, *same checking semantics* by design) — and the "re-baseline CI at every
  major" discipline (VERSION-DEPENDENT; verify against the TS blog).

### B. Measuring type safety
- The **`type-coverage`** tool (percent of expressions with a non-`any` type): how to compute,
  trend, and read it; the `--strict`/`--detail`/per-file hotspot views; realistic targets vs
  Goodhart risk (coordinate with prompt 06).
- `tsc --noEmit` as the **binary gate**; `--incremental`/`--build` and **tsgo** (TS7) for CI speed;
  coverage as the **continuous** metric layered on top of the binary gate.

### C. Debt tracking & ratcheting (the sibling's OPEN item)
- Counting the leaks: explicit `any`, implicit-`any` via untyped imports, type **assertions**
  (`/** @type {X} */ (expr)`), and `@ts-expect-error`/`@ts-ignore`.
- The **ratchet** gate: fail CI on *increase*, not on absolute zero — baseline the current debt and
  burn it down. Tools/patterns: **betterer** (ratchet arbitrary checks), typescript-eslint's
  `no-explicit-any` / `no-unsafe-*` family, custom count scripts.
- **`@ts-expect-error` over `@ts-ignore` always** — it self-reports when the suppression goes stale
  (the `--warn-unused-ignores` analogue); require a reason comment; count suppressions as debt.

### D. Untyped dependencies (the residual `any` leak)
- DefinitelyTyped `@types/*`; authoring your own `.d.ts`; `declare module` ambients; the
  `skipLibCheck` tradeoff (what it buys, what it hides); auditing types-optional imports; the "type
  the boundary of a dependency" discipline so third-party `any` cannot flow inward untyped.

### E. Migration playbook (untyped → strict raw JS)
- The **ordered** strategy: enable `allowJs`+`checkJs` with strict *off* → fix the implicit-`any`
  flood → ratchet strict flags **one at a time** → file-level `// @ts-check` vs project-wide → use
  `@ts-expect-error` as migration scaffolding with a burn-down list → **prioritize by
  churn×complexity hotspot** (consume prompt 06) → the "strict for new files, grandfather old"
  baseline.
- What **not** to do: big-bang rewrite; `any`-casting to green; enabling everything at once on a
  large surface.

### F. The approach decision (VERSION-DEPENDENT — present the matrix, then recommend per profile)
- **(A)** raw JS + JSDoc + `tsc --checkJs` — the sibling's choice; no build, ships raw `.js`.
- **(B)** author in `.ts`, type-strip/emit to `.js` — a build step (better DX and refactor tooling,
  worse no-build purity). Cover the **erasable-syntax / "types as comments"** constraint, Node's
  `--experimental-strip-types` / `--strip-types` maturity as of the anchor, and native-TS runtimes
  (Deno/Bun) — verify status against changelogs.
- **(C)** the **TC39 Type Annotations** proposal ("types as ignorable syntax in JS") — stage,
  status, and realistic timeline at the anchor, and *why the sibling says "do not design for it
  yet."*
- **(D)** Flow — niche; note only.
- **Decision axes:** no-build purity, authoring DX, refactor/rename tooling, ecosystem, **type
  expressiveness** (what JSDoc genuinely cannot express or expresses awkwardly vs `.ts`),
  portability if a build is later added. Give a **decision-grade recommendation keyed to project
  profile**, consistent with the no-build default (introducing a build is a recordable decision, per
  the master brief §4).

### G. The static↔runtime handshake (where static stops)
- Restate *only enough to place the seam*: types check shape and vanish at runtime, so ranges,
  cross-field invariants, ordering/typestate, units, DOM reality, and event-payload shapes **must**
  be runtime contracts. Enumerate the seam; measure **"boundary coverage"** (every ingress has a
  parse function). Hand the *mechanics* to `js_typing_contract_manifest.md` §5–§6 and
  `js_error_tracing_contract_manifest.md` §8/§12.

## Controversies to resolve (positions first, then a recommendation)

- **JSDoc vs `.ts` authoring** — is no-build worth the JSDoc ergonomic tax in 2026, given TS 7's
  speed and Node type-stripping? (the central decision of §F).
- `skipLibCheck` on vs off.
- Type-coverage **percentage as a target** — the Goodhart hazard (coordinate with prompt 06).
- Does the TC39 proposal's trajectory change the calculus, or is it still "ignore for now"?

## Sources to prioritize

TypeScript handbook (JS projects & JSDoc; **tsconfig** reference); the TypeScript blog (6.0 GA,
7.0 RC — dates + semantics); typescript-eslint docs (`no-unsafe-*`, `no-explicit-any`);
`type-coverage` and `betterer` docs; **Node.js** type-stripping docs + release notes; the **TC39
type-annotations** proposal repo; DefinitelyTyped docs; the sibling
`js_typing_contract_manifest.md` and `web_platform_baseline_manifest.md` §7.

## Output contract

Produce a ground-truth manifest (suggested filename `js_typing_enforcement_manifest.md`): TL;DR (the
enforcement thesis + the approach recommendation); the annotated **maximal `tsconfig.json`**
artifact; the **strictness-flag table** (flag → catches → cost → verdict); the **coverage + ratchet
recipe**; the **migration playbook** (ordered steps + what-not-to-do); the **approach decision
matrix** + per-profile recommendation; the **static↔runtime seam list**; a version matrix (TS 6/7,
Node type-stripping, ES editions); an anti-pattern checklist (`any`-to-green, big-bang migration,
`@ts-ignore`, unmeasured coverage, untyped-dep leak); sources with access dates; cross-references.

## Cross-references

Extends `js_typing_contract_manifest.md`. Feeds prompt 03 (the typescript-eslint rules that enforce
this), prompt 05 (the CI gate that runs the ratchet), and consumes prompt 06 (hotspot-ordered
migration). Hands runtime-contract mechanics to the typing + error siblings.
