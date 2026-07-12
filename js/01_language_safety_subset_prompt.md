# Deep-Research Prompt 01 — The Safe Language Subset & Footgun Elimination

**Part of** the JavaScript Safety & Maintainability program. **Apply `00_master_research_brief.md`**
for the version anchor (mid-2026), target context (raw browser JS, no-build, reuse-first,
small-scale), epistemic protocol (ESTABLISHED / VERSION-DEPENDENT / OPEN), source priority, and
output house style. This file adds only the mission-specific brief.

---

## Mission (the one question)

**What is the maximal-safety subset of modern (ES2025/26-era) JavaScript for the target context,
and for each intrinsic language hazard, what mechanism neutralizes it — classified by whether the
hazard is eliminated by static type-checking, caught by a linter, replaced by a modern language
feature, or reachable only by a runtime contract or human discipline?**

## The mess this addresses

JavaScript's *intrinsic* footguns — implicit coercion, ambient mutability, dynamic `this`,
hoisting, automatic semicolon insertion, prototype hazards, floating-point, ordering surprises —
are the substrate every other kind of "messy JS" grows on. Before layering types, linters, and
gates, you must know which hazards are real in 2026 (many "good parts"-era hazards are obsolete
now that `let`/`const` exist), which subset of the language to deliberately use, and — critically —
**which layer can actually catch each hazard**. This is the diagnosis that aims the rest of the
program.

## Scope

- **In:** the intrinsic-hazard catalogue; the modern-feature replacements; the "safe subset"
  decision (use / avoid / ban); and the **4-way catchability classification** of every hazard.
- **Out / defer to sibling:** runtime-contract *mechanics* (`invariant()`, parse-don't-validate,
  typed errors) → `js_typing_contract_manifest.md` §5–§6 and `js_error_tracing_contract_manifest.md`;
  the *configuration* of lint rules → prompt 03; type-system *mechanics* → prompt 02 + the typing
  sibling.
- **Do NOT duplicate:** the architecture manifest's paradigm/state discussion — this file operates
  at *language-mechanics* altitude (expressions, declarations, values), not architecture.

## Research decomposition (find answers to these)

### A. Coercion & equality
- The genuine hazards of loose equality (`==`/`!=`) vs strict (`===`); the abstract-equality
  algorithm's surprising cases; when (if ever) `== null` is a defensible idiom.
- The `+` operator's string/number overloading; implicit coercion in comparisons, template
  literals, and boolean contexts; `Symbol.toPrimitive`/`valueOf`/`toString` surprises.
- `NaN` semantics (`NaN !== NaN`, `Number.isNaN` vs global `isNaN`); `typeof null === 'object'`;
  `Number()`/`parseInt`/`parseFloat`/`BigInt` boundary behaviors and radix traps.
- For each: is it **type-catchable**, **lint-catchable** (name the rule family, e.g. `eqeqeq`,
  `no-implicit-coercion`), or neither?

### B. Declarations, scope & hoisting
- `var` vs `let`/`const`; the temporal dead zone; function vs block scope; function-declaration
  hoisting; the classic closure-in-loop bug and how `let` fixes it; variable shadowing; the
  const-by-default rule and its limits (`const` ≠ immutable).

### C. `this`, binding & functions
- Dynamic `this`; arrow vs `function`; method extraction losing `this`; `bind`/`call`/`apply`;
  `new`-related hazards; class fields as arrow methods; the "minimize reliance on dynamic `this`"
  stance — is it a real safety win or dogma? (a controversy to resolve).

### D. Mutability & sharing
- Reference vs value semantics; shared-mutable aliasing of objects/arrays; the change-by-copy
  methods (`toSorted`/`toReversed`/`with`/`at`, ES2023) vs their mutating twins
  (`sort`/`reverse`/`splice`); `structuredClone`; `Object.freeze` (shallow) and why runtime
  immutability differs from `readonly`/`as const` (→ prompt 02); the immutable-update idioms.

### E. Numbers, dates, text & data
- IEEE-754 pitfalls (`0.1 + 0.2`), integer safety (`Number.MAX_SAFE_INTEGER`, `BigInt` boundaries),
  `Intl` for formatting; `Date` hazards and **Temporal**'s Baseline status as of the anchor
  (ship/polyfill/avoid?); regex hazards — **catastrophic backtracking / ReDoS** (client-side
  practical risk?), the `v` flag; JSON round-trip lossiness (`undefined`, `NaN`, `BigInt`, `Map`/
  `Set`, key ordering).

### F. Truthiness & nullish
- The falsy set; `??`/`?.` (nullish coalescing / optional chaining) vs `||`/`&&`; the
  nullish-vs-falsy class of bugs (empty string, `0`, `NaN` traps); optional-chaining short-circuit
  semantics.

### G. Syntax hazards
- ASI pitfalls and the minimal rules that avoid them; the comma operator; banned constructs
  (`with`, `eval`, `Function` constructor); labeled statements; sparse arrays; `arguments` vs rest;
  getter/setter side effects.

### H. Prototype & object hazards
- Prototype pollution (`__proto__`, `constructor.prototype`) — the client-side attack surface;
  `Object.create(null)` and `Map`/`Set` as safe dictionaries; `Object.hasOwn` over
  `hasOwnProperty`; property enumeration order; `for..in` vs `Object.keys/entries`.

### I. Async hazards (language level)
- Floating promises / forgotten `await`; `await`-in-loop vs `Promise.all`; `async` callbacks in
  `Array.forEach`; unhandled rejection; the `Promise` constructor anti-pattern; interleave/race at
  every `await` point. *(Defer the propagation-channel mechanics to
  `js_error_tracing_contract_manifest.md` §6; here, catalogue the language-level traps and their
  catchability — e.g. `no-floating-promises` is type-aware-lint-catchable.)*

### J. Module-level hazards
- Module-level mutable state (singleton-per-realm); import-time side effects; circular imports;
  live bindings. *(Architecture altitude is the sibling's; here, the language-mechanics reality.)*

### K. The synthesis: "the good parts, 2026 edition"
- The recommended **use / prefer / avoid / ban** subset; a **prefer-X-over-Y** table (e.g. `===`
  over `==`, `const` over `let` over `var`, `toSorted` over `sort`, `??` over `||` for defaults,
  `Map` over object-as-dictionary, `structuredClone` over hand-rolled deep copy).
- **The catchability matrix (the core deliverable):** for every hazard above, four columns —
  *caught by types?* / *caught by lint (which rule family)?* / *eliminated by a language feature?* /
  *contract-or-discipline-only?* The contract-only residue is the explicit hand-off to the typing
  and error siblings.

## Controversies to resolve (positions first, then a recommendation)

- How much of Crockford's *Good Parts* survives to 2026 vs is made moot by `let`/`const`/modules?
- Is `this`/class-avoidance a genuine safety win, or dogma? Classes vs factory functions/closures.
- Are all implicit coercions hazards, or are some idiomatic and fine?
- ReDoS: a real client-side risk or a server-shaped worry imported without cause?

## Sources to prioritize

ECMA-262 (the normative semantics); MDN (per-operator/per-method behavior); TC39 proposal pages
(Temporal and its Baseline status); Crockford *JavaScript: The Good Parts* and *You Don't Know JS*
(historical, **critique** them against 2026); the relevant ESLint / typescript-eslint / `unicorn` /
`regexp` rule docs (for *catchability*, not configuration); OWASP (prototype pollution, ReDoS).

## Output contract

Produce a ground-truth manifest (suggested filename `js_language_safety_subset_manifest.md`) in the
house style: TL;DR (the safe-subset thesis + the top footguns that survive to 2026); the
**hazard catalogue** organized by §A–J; the **catchability matrix** (the centerpiece); the
**use/prefer/avoid/ban** decision list and the prefer-X-over-Y table; an **anti-pattern checklist**;
a **"contract-only residue"** section listing exactly what static tooling cannot catch (handed to
the typing + error siblings); a version matrix (ES editions, Temporal, feature availability);
sources with access dates; cross-references.

## Cross-references

Feeds prompt 02 (what types must cover) and prompt 03 (which lint rules earn their place); hands the
contract-only residue to `js_typing_contract_manifest.md` and `js_error_tracing_contract_manifest.md`.
