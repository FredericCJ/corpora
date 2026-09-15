# Card: review a diff (or final-check your own work)

**Load when:** reviewing any change, or the final pass over your own edit before reporting done.
Finishing a change always ends here.
**Depth:** this is the anti-pattern union across the package, ordered by how often the defect
ships. Each item: how to spot it in a diff, what it breaks, the fixing card. Read the owning
reference section only when you need the argument.

Facts verified 2026-08-12. Version-dependent claims route to
`reference/audio_platform_baseline_manifest.md` (the hub); if any file disagrees with the hub, the
hub wins. Reasoning root: the child booklet `realtime-audio-pc-architecture-and-design-r1.md`
(repo root) — operationalized here, never re-argued.

## How to use this

Work top to bottom; every item is **reject on sight**, not a discussion prompt. State findings as:
**what is wrong → what it breaks → the fix.** A finding without a failure mode is a preference.
Where an item names a mechanical route, verify the mechanism is actually armed in this repo — a
poison header nobody includes is not a control.

## 1. RT-plane violations — ship-frequency #1

[All four derive from invariants 1 and 13 and booklet section 6.6; routes inline.]

- [ ] **Lock, allocation, blocking syscall, or I/O on the RT plane.** Spot: any new call in an
      RT-class TU from the alloc/lock/wait/stdio families — or any call whose implementation the
      author cannot name (blocking until proven otherwise [ESTABLISHED: booklet section 11.4]).
      Breaks: the deadline, unboundedly. Routes: compiler-catchable
      (`config/rt_prelude_poison.h` [MEASURED 2026-08-12: poison yields a compile error on
      CLANG64 clang 22.1.8]) + runtime-catchable (the guard net) — **a diff that adds a poison
      exemption or drops the prelude from a TU's class IS the finding.** → fix:
      `cards/write-rt-code.md`
- [ ] **Bare seq_cst atomics.** Spot: `atomic_load(`, `atomic_store(`, `atomic_fetch_*(`,
      `atomic_exchange(` without `_explicit`, or an explicit `memory_order_seq_cst` — C17 defaults
      the non-`_explicit` forms to seq_cst [ESTABLISHED: C17 7.17]. Breaks: unstated intent
      (unreviewable) plus a full fence on every x86 store. Every atomic cites one of the four
      blessed idioms in a comment [ESTABLISHED: booklet section 6.6]. Route: analysis-catchable
      (grep below) + contract-only (the idiom citation). → fix: `cards/concurrency-channels.md`,
      `reference/rt_plane_rules_manifest.md` section R6
- [ ] **`volatile` as a concurrency tool.** Spot: any new `volatile` outside a quarantined adapter
      signal/exception context. Breaks: nothing is synchronized — no atomicity, no ordering.
      Route: analysis-catchable (grep) + review. → fix: `cards/concurrency-channels.md`
- [ ] **Unbounded loop on the RT plane.** Spot: `while (1)`, `for (;;)`, retry/spin loops whose
      bound does not derive from a block-constant; loop bounds mutated in-body. Breaks:
      invariant 1's boundedness — and this one is **contract-only** (the guard cannot catch it):
      demand the boundedness argument in the diff. → fix: `cards/write-rt-code.md`;
      register: `reference/rt_plane_rules_manifest.md` section R8

Quick greps over the diff (review speed; the mechanical routes still run):

```sh
grep -nE '\b(malloc|calloc|realloc|free|strdup|printf|fprintf|snprintf)\b' <rt-tu-files>
grep -nE 'atomic_(load|store|exchange|fetch_[a-z]+)\(' core/ | grep -v '_explicit'
grep -nE '\bvolatile\b|memory_order_seq_cst' <diff>
```

## 2. Tests owed but missing

- [ ] Spot: the diff touches an op, channel, adapter, or error path with **no test delta**.
      What each change type owes is a table — `reference/testing_verification_manifest.md`
      section T11: new op → properties + tables + golden + twin equivalence; new channel → contract
      suite + torture row; new fallible path → fault-suite row that reaches it; kernel perf change
      → bench JSON. Breaks: the feedback loop this package exists for. Route:
      contract-only at review; the gates catch the *regression*, only review catches the *absence*.
      → fix: `cards/write-tests.md`

## 3. Untagged or mis-tagged claims

- [ ] Spot: a new or edited `reference/` row with no epistemic tag; a version claim outside the
      hub; a "the tool does X" claim with no [MEASURED] command; an invented flag, API name, rule
      code, or package name. Breaks: the package's ground truth — an invented identifier gets
      pasted into a real config and silently disables a check. Route: contract-only (this
      checklist) + the package's own audit where wired. → fix: the tag protocol in `AGENTS.md`;
      verify or delete the claim.

## 4. Error-code reuse

- [ ] Spot: a diff that edits an existing registry row's id, reassigns a retired id, or raises
      with a bare numeric. Breaks: every archived artifact and dump that carries the old code —
      traceability severed at the root. [ESTABLISHED: booklet section 13.5, id stability] Route:
      build-catchable (registry audit, `reference/quality_gates_ci_manifest.md` section G3).
      → fix: `cards/handle-errors.md`

## 5. Event schema / session report broken

- [ ] Spot: an event id reused or renumbered; payload-word meaning changed under the same id; a
      session-report field renamed/removed without a schema version bump
      (`config/session_report.schema.json`). Breaks: the soak gate, fleet parsers, and every old
      bug report. Route: build-catchable (schema validation) + review. → fix:
      `cards/observability.md`

## 6. Flag ad-hoc-ism

- [ ] Spot: a `-f`/`-W`/`-march`/optimization flag added in a target's own build file instead of
      the per-leg toolchain file; a TU pulled out of its class "just for this one". The canon is
      one table, TU class × configuration; a kernel that "just needs" one special flag is a new
      reviewed canon row or a design smell. [ESTABLISHED: booklet section 10.2] Route:
      build-catchable (flags derive from class; audit diffs the canon). → fix:
      `cards/build-and-flags.md`

## 7. Golden auto-approve

- [ ] Spot: regenerated master files in the same diff as the code change, with no approval note
      and no first-divergence analysis; a CI step that regenerates masters. Breaks: the suite —
      "a snapshot suite with auto-approval is a change recorder, not a test" [ESTABLISHED: booklet
      section 14.3]. An **exact-regime** diff is a determinism regression by definition, not a
      re-approval candidate. Route: contract-only (approval authority) + build-catchable (masters
      are approved artifacts, not build outputs). → fix: `cards/write-tests.md`

## 8. Bench-free performance claims

- [ ] Spot: "faster", "optimized", "cheaper" in the commit message, comments, or docs with no
      before/after JSON from the pinned protocol attached. An optimization nobody measured is
      folklore (invariant 15). Route: contract-only at review; the bench gate catches regressions,
      not unsubstantiated wins. → fix: `cards/optimize-performance.md`

## 9. Unrouted rules

- [ ] Spot: a new "must/never/always" in code comments, docs, or reference rows with no route —
      no gate, no analysis rule, no poison entry, no contract-only register line. A rule with no
      enforcer is a preference [ESTABLISHED: booklet ch. 3, meta-invariant]. Route it, or register
      it contract-only by name. → fix: `cards/gates-and-ci.md`; register:
      `reference/rt_plane_rules_manifest.md` section R8

## Never

- Approve a diff with an RT-plane lock/allocation/blocking-syscall/unbounded-loop finding still open — item 1 is reject-on-sight, not a discussion prompt.
- Wave through a change with no test delta for an op, channel, adapter, or error path it touches — the gates catch the regression, only review catches the absence (item 2).
- Accept an untagged or invented claim (flag, API name, rule code, version, package name) in a reviewed diff — verify or delete it before approving (item 3).
- Approve a registry-code reuse/renumber, a reused event id, or a session-report field rename with no schema bump (items 4-5).
- Let a flag move outside its per-leg toolchain file, or a golden master regenerate with no approval note and first-divergence analysis, into the same diff as the logic change (items 6-7).
- Take a bench-free performance claim ("faster", "optimized") at its word (item 8).
- Sign off on a new "must/never/always" with no route — no gate, no analysis rule, no contract-only register line (item 9).

## The contract-only register — ask these by name

Nothing mechanical checks these; the review is the enforcement. [ESTABLISHED: booklet section
15.5; register mapping: `reference/rt_plane_rules_manifest.md` section R8]

- [ ] New RT-plane loop → where is its **boundedness argument**?
- [ ] New thread → **plane declared** in its name and creation site? One line in review,
      catastrophic when skipped.
- [ ] New channel shape → written **happens-before argument** in C11-model terms?
- [ ] New channel implementation → its **wait-free claim** stated (the stress suite hunts
      violations; the claim is an argument)?
- [ ] New op → **latency declaration** present (a wrong one miscomputes the product's headline
      latency)?
- [ ] Bench numbers in the diff → **environment honesty** (frequency policy labeled, machine
      identified)?
- [ ] The refusals staying refused: inline asm, timer-resolution squeeze, mitigations off,
      priority kernel modules, undocumented tunables?

## What you owe — before you say "done"

- [ ] Every `OPEN` you hit is written down as **ASSUMED** (with the default you took) or
      **NEEDS-INPUT** (with the question) — never silently resolved.
- [ ] Every claim about tool behavior was **measured** (command + version recorded) or is flagged
      unverified.
- [ ] You invented no identifier — no flag, rule code, API name, version, or package name.
- [ ] Each finding you reported carries its failure mode and its fix.
- [ ] The named gates for every touched area are listed — and green
      (`cards/gates-and-ci.md`).

## Decisions you must not invent

Whether a given finding blocks the change · deviation-record acceptance authority ·
golden-master diff approval authority · the suppression budget and who spends it.

## Go deeper

| question | where |
|---|---|
| what each change type owes in tests | `reference/testing_verification_manifest.md` section T11 |
| the banned-operations table, per family | `reference/rt_plane_rules_manifest.md` section R2 |
| the contract-only register, complete | `reference/rt_plane_rules_manifest.md` section R8 |
| the blessed memory-ordering idioms | `reference/rt_plane_rules_manifest.md` section R6 |
| structural audits that back rows 4–6 | `reference/quality_gates_ci_manifest.md` section G3 |
| flag canon and TU classes | `reference/toolchain_build_manifest.md` sections B1, B2 |
