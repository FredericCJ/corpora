# Deep-Research Prompt 05 — Boundary & Runtime Type-Safety (Where Types Lie)

**Part of** the General JS/TS Safety & Maintainability program. **Apply `00_master_research_brief.md`**
for the general target, version anchor (mid-2026), epistemic protocol, source priority, and output
house style. This file adds only the mission-specific brief.

---

## Mission (the one question)

**How do you re-establish type-safety at the many boundaries where TypeScript's types are erased and
external data arrives untyped — via schema-first validation, end-to-end type flow across the network
and database, and typed configuration — so that a compiled TS program's guarantees actually hold at
runtime, as of mid-2026?**

## The mess this addresses

TypeScript's types **vanish at compile time**; at runtime, every byte crossing a boundary is
`unknown` that the compiler has been *told* is typed. In a general/full-stack app the boundaries are
many — HTTP requests and responses (both directions), database rows, environment variables, config
files, CLI args, message queues, webhooks, third-party SDK responses, `JSON.parse`, `FormData`,
WebSocket frames — and at every one, a wrong `as SomeType` is a lie the type system will faithfully
propagate into a runtime crash far away. The narrow `../js/` program handles this with small
hand-rolled parsers at a few browser boundaries; the general program needs it **industrialized**: one
source of truth for each contract, validated at the edge, with types *derived from* the validator so
the two cannot drift.

## Scope

- **In:** the erasure gap and the boundary inventory; schema-first validation libraries; the
  parse-don't-validate discipline industrialized; end-to-end type safety (RPC/GraphQL/OpenAPI/typed
  DB); typed environment & config; the illegal-states-unrepresentable + contract-drift problems.
- **Out / defer:** the *static* type-system mechanics (branding, discriminated unions at the type
  level) → prompt 01 (this prompt owns the *runtime* half of the same seam); *error propagation
  channels* once a parse fails → `../web_manifests/js_error_tracing_contract_manifest.md` (referenced);
  the browser-only boundary set → `../js/` (referenced, generalized here).
- **Do NOT duplicate** prompt 01's type-design content; this is its runtime counterpart.

## Research decomposition (find answers to these)

### A. The erasure gap & the boundary inventory
- State the gap precisely (types are compile-time only; `as`/casts are unchecked promises; `JSON.parse`
  and untyped SDKs return `any`/`unknown`). Enumerate the **general boundary set** and mark each as
  untrusted-on-read: HTTP req/res, DB reads, env/config, CLI args, files, queues/webhooks, third-party
  API responses, `postMessage`/WebSocket, deserialization. (Generalizes `../js/` §5 and the typing
  sibling's boundary list.)

### B. Schema-first validation libraries (survey + verdict, VERSION-DEPENDENT)
- **Zod** (the incumbent; v4-era perf/tree-shaking — verify), **Valibot** (modular, tiny bundle),
  **ArkType** (TS-syntax types, high performance), **TypeBox** (JSON-Schema-first, great for
  OpenAPI/Ajv), **Effect Schema** (bidirectional + effect ecosystem); the **Standard Schema** spec as
  the interop layer letting tools accept any of them. For each: **type inference from the schema**
  (single source of truth), bundle-size/perf, error-message quality, JSON-Schema interop, and fit.
- The core pattern: `schema → parse(unknown) → T` with `type T = infer<typeof schema>`; validated data
  carries a **branded** type inward (ties to 01).

### C. Parse-don't-validate, industrialized
- Validate **once at the edge**, trust the typed value inward; one parser per boundary; typed parse
  errors vs thrown — the Result-vs-exception choice (cross-ref
  `../web_manifests/js_error_tracing_contract_manifest.md`); coercion/transformation at the boundary
  (dates, numbers from strings); versioned/evolving payloads (old stored data — cross-ref the storage
  boundary).

### D. End-to-end type safety (types across the wire, without duplication)
- **When both ends are TS:** **tRPC** (types flow client↔server with no codegen) — power and its
  limit (TS-only, coupling). **Schema/codegen bridges:** **GraphQL + codegen**, **OpenAPI→types**
  (openapi-typescript, orval, ts-rest), **typed DB clients** (**Prisma**, **Drizzle**, Kysely). The
  goal — one contract, both sides typed — and the honest limits: codegen steps, drift when the schema
  isn't the source of truth, and the "types don't validate the wire; you still need runtime checks at
  trust boundaries" caveat.
- **Contract-drift defenses:** derive one artifact from the other (schema→types, or types→schema);
  shared contract package in a monorepo (cross-ref 07); or **contract tests** when the ends can't share
  code.

### E. Typed environment & config
- Env vars are strings from an untrusted boundary; **validate at startup and fail fast** (**t3-env**,
  znv, or a hand-rolled schema parse); typed config objects; secret handling (never in the type as a
  literal; never logged — cross-ref observability).

### F. Make illegal states unrepresentable (the runtime half)
- Discriminated unions + exhaustive handling at boundaries; branded validated IDs/units; narrowing
  external data into a domain model the rest of the code can trust; the payoff (bugs become
  compile-or-parse errors, not deep runtime surprises) and the limit (the type system can't express
  ranges/relations — the runtime schema must — the reciprocal handoff with prompt 01).

## Controversies to resolve (positions first, then a recommendation)

- **Zod vs Valibot vs ArkType vs TypeBox** — the default schema library, keyed to bundle-budget vs
  ergonomics vs JSON-Schema interop.
- **tRPC vs OpenAPI/GraphQL-codegen** — tight TS-to-TS coupling vs language-agnostic contracts.
- **Validate everything vs validate only at trust boundaries** — the perf/ceremony vs safety tradeoff
  (internal service-to-service, or your own DB, may not need full re-validation).
- **Schema-as-source-of-truth vs types-as-source-of-truth** (which direction to derive).

## Sources to prioritize

Docs for **Zod, Valibot, ArkType, TypeBox, Effect Schema** and the **Standard Schema** spec; **tRPC**,
**GraphQL Code Generator**, **openapi-typescript/orval/ts-rest**, **Prisma/Drizzle/Kysely** docs;
**t3-env** docs; Alexis King "Parse, don't validate" (the source doctrine); "make illegal states
unrepresentable" write-ups (as opinion). Separate each library's inference *claims* from demonstrated
edge-case behavior. References `../web_manifests/js_error_tracing_contract_manifest.md` and `../js/`.

## Output contract

Produce a ground-truth manifest (suggested filename `js_boundary_type_safety_manifest.md`): TL;DR (the
erasure gap + schema-first + derive-don't-duplicate thesis); the **boundary inventory** (boundary →
untrusted? → parser obligation); the **schema-library survey** table (library → inference → size/perf →
JSON-Schema interop → fit → verdict); the **parse-don't-validate industrialized** pattern; the
**end-to-end type-safety** options table (approach → coupling → codegen → drift-defense → fit); **typed
env/config**; the **illegal-states-unrepresentable** discipline and its handoff to prompt 01; a version
matrix; an anti-pattern checklist (`as`-instead-of-parse, `JSON.parse`-flows-inward, unvalidated env,
schema/type drift, trusting third-party SDK types, over-validating internal calls); sources;
cross-references.

## Cross-references

The runtime counterpart of prompt 01 (they share the illegal-states seam; 01 owns compile-time, 05
owns runtime); parse-failure propagation defers to `../web_manifests/js_error_tracing_contract_manifest.md`;
shared-contract packages hand off to prompt 07 (monorepo); runtime APIs available depend on prompt 02.
Generalizes `../js/`'s browser-boundary parsing and the typing sibling's §5.
