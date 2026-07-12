# Deep-Research Prompt 01 — TypeScript & the Type System, Wielded Well

**Part of** the General JS/TS Safety & Maintainability program. **Apply `00_master_research_brief.md`**
for the general target (authored TS, build-normal, Node+multi-runtime, scale-open), version anchor
(mid-2026), epistemic protocol, source priority, and output house style. This file adds only the
mission-specific brief.

---

## Mission (the one question)

**How do you wield authored TypeScript for maximum safety and maintainability — the strict compiler
configuration, the full type-system spectrum and when each construct earns its place, and the
type-DESIGN discipline that separates genuine leverage from over-engineering — as of mid-2026?**

## The mess this addresses

TypeScript prevents one class of mess and enables another. Under-typed code leaks `any` through a
large codebase until the compiler is decorative; *over*-typed code drowns in conditional/mapped-type
astronautics that no one can read, that produce incomprehensible error messages, and that slow the
checker to a crawl. The maintainable middle — strict where it counts, simple where it can be, rich
types only where they pay — is a *design* skill, not a feature list. This prompt is the type pillar
for authored TS; it is distinct from `../js/02_static_typing_enforcement_prompt.md`, which covers
JSDoc-checking, coverage measurement, and migration.

## Scope

- **In:** the strict `tsconfig` for authored TS; the type-system spectrum (unions, generics,
  conditional/mapped/template-literal types, `satisfies`, variance, branding, exhaustiveness); the
  `any`/`unknown`/assertion discipline; declaration files & `.d.ts` emit; module/global augmentation;
  and **type-design discipline** (rich vs over-engineered).
- **Out / defer:** *runtime* validation of erased types → prompt 05; *module-resolution* and
  `moduleResolution`/`verbatimModuleSyntax` mechanics → prompt 02 (referenced, not owned here);
  *lint* enforcement of type rules → prompt 06; *build/emit* performance at the pipeline level →
  prompt 03; coverage measurement + migration + JSDoc → `../js/02_static_typing_enforcement_prompt.md`.
- **Do NOT duplicate** the language-footgun catalogue (`../js/01_language_safety_subset_prompt.md`) —
  reference it; cover only TS-specific hazards here.

## Research decomposition (find answers to these)

### A. The strict configuration for authored TS
- The `strict` family + the recommended additions (`noUncheckedIndexedAccess`,
  `exactOptionalPropertyTypes`, `noImplicitOverride`, `noFallthroughCasesInSwitch`,
  `noImplicitReturns`, `noUnusedLocals`/`Parameters`, `noPropertyAccessFromIndexSignature`,
  `useUnknownInCatchVariables`, `allowUnreachableCode: false`); the emit/interop flags that belong in a
  strict baseline (`verbatimModuleSyntax`, `isolatedModules`, `forceConsistentCasingInFileNames`) —
  cross-ref prompt 02 for their module meaning.
- What **TS 6.0** made default (strict/ESM/`es2025`) and **TS 7.0** (Go "Corsa" port / `tsgo`, ~10×
  faster, *same semantics*); shared bases (`@tsconfig/strictest`) vs a hand-committed config; the
  re-baseline-at-major discipline. (VERSION-DEPENDENT — verify against the TS blog.)

### B. The type-system spectrum (what each construct is *for*, and its cost)
- **Discriminated unions + exhaustiveness** — the workhorse for modeling state and results; `never`/
  `assertNever`; `switch` exhaustiveness; the `satisfies` operator for validated-yet-narrow values.
- **Generics** — constraints (`extends`), defaults, `const` type parameters, and **variance**
  (`in`/`out` annotations) — when explicit variance matters.
- **Conditional types**, `infer`, **mapped types** + key remapping (`as`), **template-literal types**
  — what problems genuinely need them (library-grade APIs, inference helpers) and their recursion/
  perf limits.
- **`unknown` as the honest top type** vs `any` the contagion; **type predicates** (`x is T`) and
  **assertion signatures** (`asserts x is T`); `as const`; the non-null `!` and double-assertion
  escape hatches — and their confinement discipline.
- **Nominal / branded types** — TS has no native nominal typing; the branding patterns and their
  runtime-construction discipline (ties to 05).
- **Utility types** (`Partial`/`Pick`/`Omit`/`Record`/`ReturnType`/`Awaited`/…) and when a hand-written
  type is clearer than a utility chain.

### C. The `any`/assertion discipline (the leak control)
- Where `any` enters (explicit, untyped deps, `JSON.parse`, `catch`, assertions) and the
  `unknown`-first counter-discipline; type assertions as unchecked promises; when a **type guard** or
  **schema parse** (05) is the right replacement for an assertion. (Enforcement of this is prompt 06's
  `no-unsafe-*`/`no-explicit-any`; measurement is `../js/02`.)

### D. Declaration files & the library dimension
- Authoring `.d.ts`; `declaration`/`declarationMap` emit; **`isolatedDeclarations`** (fast, portable
  d.ts emit — status/tradeoffs at the anchor); **module augmentation** and `declare module` (extending
  third-party and global types safely); global augmentation hazards; ambient vs module scope. (Library
  *publishing* correctness — publint/attw/api-extractor — is prompt 07.)

### E. Type-design discipline (the maintainability heart — the distinct contribution)
- **Rich types vs over-engineering:** the failure mode of "type astronautics" — clever type-level
  programming that is unreadable, produces opaque errors, and slows the checker. Heuristics for *when*
  a complex type pays (public library API, high-traffic inference boundary) vs when a **simpler type +
  a runtime check** (05) is more maintainable.
- **Error-message and DX cost** as a first-class design input; **compile-performance** cost of heavy
  types (the "types are also a program that runs" reality); readability for the next maintainer.
- **"Make illegal states unrepresentable"** at the type level (shared thesis with 05's runtime side)
  — and its limit: the type system cannot enforce value ranges/relations, which is the handoff to 05.

### F. Type-checking performance & scale
- Why `tsc` is slow; **project references** / composite / `incremental` (mechanics here; the monorepo
  *orchestration* is prompt 07); `skipLibCheck` tradeoff; **`tsgo`/TS 7** as the anchor's speed story;
  editor responsiveness vs CI check.

## Controversies to resolve (positions first, then a recommendation)

- **How rich should types be?** The "parse, don't validate + illegal-states-unrepresentable"
  maximalists vs the "keep types boring, validate at runtime" pragmatists — reconcile with 05.
- **`interface` vs `type`**; `enum` vs union-of-literals vs `as const` objects (enum's runtime/erasure
  quirks — cross-ref 03 `isolatedModules`).
- **`skipLibCheck`** on vs off at scale.
- **Branded types** worth the ceremony?
- Class-based vs functional/type-first modeling in TS.

## Sources to prioritize

The TypeScript handbook + `tsconfig` reference; the TypeScript blog (6.0/7.0 — dates + semantics);
the `isolatedDeclarations` and `satisfies`/`const`-type-param feature notes; `@tsconfig/*` bases;
`type-fest` (as a catalogue of what advanced types *can* do — and a caution on complexity); named
practitioners on type design *as opinion*. Reference `../js/02` and `../js/01`.

## Output contract

Produce a ground-truth manifest (suggested filename `ts_type_system_manifest.md`): TL;DR (the strict
baseline + the type-design thesis); the annotated **strict `tsconfig` for authored TS**; the
**type-system spectrum** table (construct → what it's for → cost → when to reach for it); the
**`any`/assertion discipline**; the **declaration-file** guidance; the **type-design discipline**
section (rich-vs-over-engineered, with heuristics and the handoff to 05); the **perf/scale** notes; a
version matrix (TS 6/7, feature availability); an anti-pattern checklist (type astronautics,
`any`-leak, assertion-abuse, enum-erasure surprises, unreadable inference); sources; cross-references.

## Cross-references

Hands runtime validation and "illegal states" enforcement to prompt 05; hands type-rule *enforcement*
to prompt 06; shares module/emit flags with prompt 02; hands scale orchestration to prompt 07.
References `../js/01` (footguns) and `../js/02` (JSDoc/coverage/migration).
