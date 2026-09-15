# Card: set up or tighten quality gates

**Load when:** wiring CI, adding a check, raising a standard on an existing codebase, or deciding what
should block a merge.
**Depth:** `reference/python_quality_gates_manifest.md`. The rule set itself is
`reference/python_linting_practices_manifest.md`; ready-made config is in `config/`.

## Two rules that decide whether any of this survives

1. **The same command must run in the editor, in the pre-commit hook, and in CI.** A gate that only
   exists in CI teaches people to push and wait, and a gate that only exists locally does not exist.
2. **A gate that cannot be adopted incrementally will be switched off.** So every standard arrives with a
   ratchet, never as a big-bang rewrite.

## The gate set

| # | gate | command | blocking? |
|---|---|---|---|
| 1 | format | `ruff format --check` | yes |
| 2 | lint | `ruff check` | yes |
| 3 | types | your pinned checker, `strict` | yes (ratcheted) |
| 4 | tests | `pytest` | yes |
| 5 | deprecations | `filterwarnings = ["error::DeprecationWarning"]` **plus `-X dev`** | yes |
| 6 | boundaries | `lint-imports` | yes |
| 7 | dependency drift | `deptry .` | yes |
| 8 | vulnerabilities | audit the lock file | yes |
| 9 | coverage | measured, reported, **not** thresholded as the objective | advisory |
| 10 | mutation / complexity / docstring coverage | diagnostics only | never blocking |

**Pin every tool version.** ruff 0.16.0 moved its default rule set from 59 to 413 and dropped 18 codes;
teams that had not pinned discovered it as a red build. Write `select` out explicitly — an implicit
default set is not a standard.

## The ratchet — how to raise a bar without stopping the world

The mechanism matters more than the intent. Ranked by how well they hold:

1. **A monotonically decreasing count.** Record today's number of suppressions (`# noqa`,
   `# type: ignore`), fail the build if it goes **up**. Cheap, unambiguous, cannot rot.
2. **Per-module strictness.** Turn the standard on module by module, newest and most-changed first. For
   type checking, `enable_error_code`/`disable_error_code` are per-module settable — that is the real
   ratcheting lever.
3. **New-code-only enforcement.** Apply the standard to changed lines. Honest, but needs tooling that
   understands the diff, and it lets old debt sit forever.
4. **A baseline file** of accepted violations. Works, but rots quietly: nobody re-reads it, and it becomes
   a permission slip. If you use one, date every entry and review it on a schedule.

**Every ratchet needs a floor and an owner.** A ratchet with neither is a number that drifts.

## Suppressions are a budget, not a fix

Every suppression names **a code and a reason** (`PGH003`, `PGH004`). A suppression that no longer
suppresses anything is itself a defect (`RUF100`). Count them, publish the count, and make it a one-way
number. Per-file exemptions belong in config where they are reviewable — not scattered as inline
comments; `tests/**` legitimately exempts `S101` and friends, and that exemption lives in
`config/pyproject.toml`.

## Coverage — read this before setting a threshold

Coverage tells you what was **executed**, not what was **verified**. A percentage gate is gameable by
construction, and the arithmetic works against you: precision settings participate in the comparison, so
"80%" is not a single number. Gate instead on things that mean something:

- **no assertion-free tests** (a real gate)
- **every new error path has a test that reaches it**
- coverage **reported** on the diff, read by a human, with the *missing* lines as the artefact

If an external mandate forces a percentage, pair it with the assertion-free ban and treat the number as
a smell check, not a goal.

## Supply chain and release

Lock for applications (`pylock.toml`); audit the lock, not the loose ranges. Scan your CI workflow
definitions too — they execute with your credentials. Prefer trusted publishing over long-lived tokens.
Generate an SBOM if you have a consumer who wants one, and reproducible builds if you have a reason —
otherwise say plainly that you are not doing them rather than half-doing them. → gates §7

## Incremental delivery

Trunk-based, small changes, gates fast enough to run on every one. **Toggles have categories with
different lifetimes and different removal obligations** — a release toggle is temporary and must have an
owner and a removal date; an experiment toggle is measured; an ops kill-switch is permanent. An
undifferentiated pile of flags is technical debt with a config file. Migrations follow
**expand → migrate → contract**. The CI interpreter matrix is **not** the same list as `requires-python`.
→ gates §8

## Measurement — what is defensible

Be sceptical here; the manifest is. Complexity metrics correlate strongly with raw size and add little
independent predictive power, so treat them as **diagnostics** and never as gates. What genuinely
ratchets is **structural and countable**:

- boundary-contract violations (target: zero)
- import cycles (target: zero)
- suppression count (one-way)
- annotation coverage (one-way)
- flake rate and test-suite runtime (both maintainability properties in their own right)

Process signals — change coupling, churn×complexity hotspots, delivery metrics — are useful *diagnostics*
with real evidence behind them. Nothing above measures whether the design is good; that is a review
judgement, and saying so is what keeps the rest credible. → gates §9–§10

## Never

- A coverage number as the objective.
- A gate nobody can run locally.
- An advisory gate with no date and no owner for making it blocking.
- `--fix` or any autofix **in CI** — CI reports; humans and hooks fix.
- Unpinned tools, or an implicit default rule set.
- A required gate that the same file's own guidance calls a diagnostic. (This exact contradiction was
  found by audit in this package — check yours for it.)

## Decisions you must not invent

Which gates block vs advise · the ratchet mechanism and its floor · whether coverage has a threshold at
all and what it is *for* · the interpreter matrix · the deprecation window · who owns each advisory
gate's promotion · whether mutation testing runs, and on what subset.

## Go deeper

| question | where |
|---|---|
| the full gate ledger with exit-code contracts and runtimes | gates §2 |
| local/CI parity, and the runner choice | gates §3 |
| the ratchet in detail, and which mechanisms rot | gates §4 |
| type checking as a ratchetable gate | gates §5 |
| test gates, flake policy, quarantine | gates §6 |
| supply chain and the release path | gates §7 |
| metrics that are defensible, and the ones that are not | gates §9 |
| Goodhart, and what cannot be measured at all | gates §10 |
