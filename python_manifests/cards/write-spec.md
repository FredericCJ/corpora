# Card: write a spec before implementing

**Load when:** asked to design before building, to write a component contract, or to record a decision.
**Depth:** `reference/software_spec_discipline_manifest.md` (how to write it) and
`reference/architecture_manifest_default.md` (how to reason about it). Both are **language-agnostic** and
carry no version facts by design — Python facts come from the `python_*` files.

## The boundary that makes a spec worth writing

**Specify the contract, not the computation.** A spec states inputs, outputs, invariants, error modes,
ordering constraints and observable behaviour. It does not state the algorithm, the control flow, the
internal data structure, or code. **The implementer owns HOW; the spec owns WHAT and HOW-WELL.**

Type-level scaffolding is in scope — a signature, a `Protocol`, a dataclass field set, an invariant
expressed as a type. **Function bodies are not.** When a snippet is needed to disambiguate, it is a
signature, never an implementation.

Note the useful distinction: *implementation-agnostic* is not *Python-agnostic*. A spec may rely on the
type system to carry a contract; that is a platform constraint it is entitled to assume, not an
implementation decision. Say which you are doing when it matters.

## What a component contract must carry

| element | why it is not optional |
|---|---|
| **inputs and outputs, typed** | the signature is the contract's spine |
| **invariants**, at named boundaries (entry, exit, between calls) | these are what tests and assertions check |
| **error modes** — which failures are typed in-band, which raise | this is the caller's obligation; unstated, it becomes tribal knowledge |
| **ordering / lifecycle constraints** | "must be called after `open`" is a contract, not a comment |
| **observable behaviour** — what a caller can detect | anything not observable is not specifiable |
| **nomenclature** | two names for one concept is a defect that compounds |

Enough that a developer implements with no further questions — and it **stops at the body**.

## Test obligations, not test code

For each component, name: the **seam**, the **observable contract**, the **input partitions**
(equivalence classes + boundary values), the **expected observable**, and the **error-path obligations**
explicitly. Every obligation maps to at least one assertion. You are not writing assertions here —
you are writing what must be asserted. → `cards/write-tests.md` for the mechanics.

## Reusability is a first-class objective, not a hope

If a unit is meant to be lifted into another application, the spec states its **standalone contract** and
its **dependency surface** — what it needs, what it configures, what it assumes about its host. The
recurring failure is a component that works only inside its original application because its dependency
surface was never written down. For Python specifically, the logging discipline
(`cards/observability.md`) is where this is most often violated.

## The `OPEN` protocol — the part agents get wrong

Everything the `python_*` manifests tag `OPEN` is a decision that lands in a spec. Split every one:

- **ASSUMED** — you proceeded on a stated default. Record the default **and** what it would take to
  revisit it.
- **NEEDS-INPUT** — you cannot responsibly choose. Record the question, the options, and what each
  forfeits.

Never silently resolve an `OPEN`, and never stall on one you could reasonably assume. The `OPEN`s that
recur most: the `requires-python` floor, the authoritative checker, the result/raise seam, the error-code
scheme, the coverage gate's purpose, and the concurrency model.

## Record decisions, keep the dissent

A decision log captures each contested call: what was decided, who objected from which concern, how it
resolved, and its epistemic tag. **Overruled dissent is recorded, not deleted** — it is the cheapest
future-debugging asset you will ever write. One traceable spine: requirement → component → design spec →
verification, navigable in both directions, so a reader can answer both *"why does this exist?"* and
*"what verifies this?"*

## Never

- **Specify the algorithm** when the contract would do. It removes the implementer's judgement and
  freezes a choice that should stay changeable.
- **Write a function body** in a spec.
- **Leave error modes unstated.** Silence here is the most expensive omission in the document.
- **Invent a requirement** to fill a template section. An empty section is honest; a fabricated one
  becomes load-bearing.
- **State a version fact.** Cite `reference/python_platform_baseline_manifest.md` instead — a spec that
  hard-codes a version becomes wrong on a schedule.
- **Copy a principle from this package into the spec as a rule** without saying whether it materially
  shaped the decision. These manifests are grounding; quoting them where they do not apply is misuse.

## Go deeper

| question | where |
|---|---|
| the implementation-agnostic boundary, in full | spec-discipline §A |
| the requirements cascade — roles, altitudes, feedback | spec-discipline §B |
| reusability as an objective, and the reusability ledger | spec-discipline §C |
| requirements writing discipline — atomicity, testability | spec-discipline §E |
| the testability reasoning framework | spec-discipline §F |
| spec output, traceability, and the `OPEN` split | spec-discipline §G, esp. §G5 |
| vocabulary: component, contract, invariant, seam, coupling, cohesion | architecture §1 |
| the paradigm menu, with the conditions each degrades under | architecture §2 |
| testability and debuggability pattern families | architecture §4–§5 |
| recovering a spec from code that has none | `reference/spec_recovery_reverse_engineering_manifest.md` |
