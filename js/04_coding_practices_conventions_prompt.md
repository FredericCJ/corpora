# Deep-Research Prompt 04 — Coding Practices, Idioms & Anti-Patterns

**Part of** the JavaScript Safety & Maintainability program. **Apply `00_master_research_brief.md`**
for the version anchor (mid-2026), target context, epistemic protocol, source priority, and output
house style. This file adds only the mission-specific brief.

---

## Mission (the one question)

**What is the decision-grade catalogue of coding practices, idioms, and anti-patterns that make raw
browser JS maintainable — and for each one, is it mechanically enforceable, and by what (a type, a
named lint rule, an architectural fitness function, the formatter) or is it review-only?**

## The mess this addresses

Beyond what types and linters catch lies a large space of *judgment-level* practice — naming,
decomposition, immutability discipline, async idioms, module hygiene, boundary defensiveness — and
this is where much "messy JS" actually lives. Left implicit, these get relitigated in every code
review. This mission makes them explicit **and routes each to its enforcement mechanism**, so the
human-convention layer connects directly to prompts 03/05 (what's automatable) and isolates the
**review-only residue** (what humans must still catch). The connective mapping is the point — a
practice catalogue that doesn't say "and here's how it's enforced" just adds more unenforced advice.

## Scope

- **In:** the practice/idiom catalogue; the anti-pattern/code-smell catalogue; a style-guide survey;
  and — the payload — the **enforceability mapping**.
- **Out / defer:** architecture-altitude decisions (state ownership, seams, the paradigm menu, CSS
  architecture, concurrency model) → `web_architecture_manifest.md` (reference, don't re-derive);
  lint-rule *definitions* → prompt 03; complexity *numbers* → prompt 06; test practices → the
  testing sibling; error/logging idioms → the error + observability siblings (reference).
- **Do NOT duplicate the architecture manifest.** Operate one altitude **below** it — at the
  function / expression / module-hygiene level. If a point is about *which component owns state*, it
  belongs to the sibling; if it's about *how to write the function*, it belongs here.

## Research decomposition (find answers to these)

### A. Style-guide survey (extract the durable, discard the framework-bound)
- Airbnb, Google, StandardJS, XO, and the historical Crockford: what each mandates, where they
  conflict, and what survives for **no-build raw JS in 2026**. Resolve the stance: adopt a
  **formatter + a curated lint set** (prompt 03) over a prose style guide — argue it.

### B. Naming & readability
- Naming conventions (casing; intention-revealing names; boolean/predicate naming; the async-function
  and event-handler naming conventions; boundary-parser naming); the abbreviation stance.
- **Comment discipline:** why-not-what; the JSDoc *prose* obligations from the typing sibling
  (`@throws`, preconditions); the "self-documenting code" claim and its real limits.
- Magic numbers/strings → named frozen constants (ties to prompt 01 §D and literal-union derivation
  in the typing sibling).

### C. Function & expression discipline
- Small, pure functions; single responsibility at function altitude; **parameter count** and the
  **options-object** idiom; the **boolean-trap** parameter; **guard clauses / early return** over
  nested `if`; no parameter reassignment; isolating side effects (functional-core alignment);
  expression-level clarity (avoid clever nested ternaries, the comma operator, over-dense chaining).

### D. Immutability & data-shaping idioms
- `const` by default; **change-by-copy over mutation** (coordinate with prompt 01 §D); local mutation
  fine, shared mutation not; `readonly`/`as const` at the type layer (→ prompt 02); `Object.freeze`
  for shared constants; defensive copy / `structuredClone` at boundaries; normalizing shapes over
  deep nesting.

### E. Async idioms
- `async`/`await` over raw `.then` chains; `Promise.all`/`allSettled` over serial awaits;
  no-`await`-in-loop without cause; **every promise awaited, returned, or `.catch`-terminated** (the
  error sibling's rule; enforced by prompt 03's `no-floating-promises`); `AbortController` for
  cancellation; sequential-vs-concurrent as an *explicit* choice; avoiding the `Promise`-constructor
  anti-pattern.

### F. Module & file organization (file-hygiene altitude)
- One responsibility per module; **named over default exports** (rename/refactor safety); **barrel
  file** (`index` re-export) tradeoffs and cycle risk; import ordering/grouping; no circular imports;
  no module-level mutable state (singleton-per-realm — architecture §3.2, restated as a practice);
  explicit public surface; colocating types/tests. *(Feature-over-technology foldering is the
  architecture sibling's; here, the within-module hygiene.)*

### G. Boundary defensiveness (the practice-level of parse-don't-validate)
- Treat all ingress as hostile; validate at edges only, trust inward; the safe-DOM-sink discipline
  (`textContent` over `innerHTML`; the Trusted Types adjacency → prompt 03 security lint); **never
  read state back out of the DOM** (architecture §3.1, restated as a practice); handle **every**
  fetch failure branch (error §12).

### H. The anti-pattern & code-smell catalogue (JS-specific)
- God modules/functions; deeply nested callbacks/promises; **stringly-typed** code; **boolean
  traps**; **primitive obsession** (→ branded types, prompt 02); shotgun mutation; hidden temporal
  coupling; leaky abstractions across the three-languages boundary (behavior in inline HTML `on*`
  attributes, layout constants in JS); dead/commented-out code; copy-paste duplication;
  over-abstraction / premature generality (YAGNI — spec sibling); over- vs under-engineering.

### I. The enforceability mapping (the connective payload — a table)
For **every** practice and anti-pattern above, one row with columns: *enforced by types?* /
*enforced by a named lint rule (which)?* / *enforced by a fitness function (which)?* / *formatter?* /
**review-only?** This table is what routes 04 into prompts 02/03/05/06. Then extract the
**review-only residue** into an explicit list — *this is where human code review must concentrate,*
because nothing else will catch it.

## Controversies to resolve (positions first, then a recommendation)

- **StandardJS** (zero-config, no semicolons) vs a curated configurable set.
- **Default vs named** exports; **barrel files** (ergonomics vs cycles/bloat).
- "Comments are a smell" vs "comments carry the why" — reconcile with the JSDoc-prose obligation.
- **Functional vs OOP** idiom in raw JS; **classes vs factory functions**.
- How much immutability discipline is worth its ergonomic cost at small scale.

## Sources to prioritize

The major style guides (Airbnb / Google / StandardJS / XO); Fowler *Refactoring* (the code-smell
catalogue — cite as the reference taxonomy); Clean Code and similar (cite **as opinion**, critique
against the target); MDN idioms; the sibling manifests for the practices they already mandate
(architecture §3, error, observability, spec discipline / YAGNI).

## Output contract

Produce a ground-truth manifest (suggested filename `js_coding_practices_manifest.md`): TL;DR (the
"formatter+curated-lint over prose-guide" thesis + the top maintainability practices); the
**practice catalogue** (§B–G, grouped, each decision-grade); the **anti-pattern catalogue** (§H); the
**style-guide survey verdict**; **THE enforceability mapping table** (the centerpiece); the
**review-only residue** list; an anti-pattern checklist; sources with access dates; cross-references.
This file is a **routing hub** — expect heavy cross-referencing.

## Cross-references

Routes to prompt 03 (practices → lint rules), prompt 02 (branding/immutability at the type layer),
prompt 05 (module/boundary practices → fitness functions), prompt 06 (function-size/complexity
practices → budgets). References `web_architecture_manifest.md`, the error and observability
siblings, and the spec-discipline sibling (YAGNI). Hands the review-only residue to human review.
