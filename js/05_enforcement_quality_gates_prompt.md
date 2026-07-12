# Deep-Research Prompt 05 — Enforcement Machinery & Quality Gates

**Part of** the JavaScript Safety & Maintainability program. **Apply `00_master_research_brief.md`**
for the version anchor (mid-2026), target context, epistemic protocol, source priority, and output
house style. This file adds only the mission-specific brief. **This is the program's payoff** — "a
way of enforcing it is even nicer."

---

## Mission (the one question)

**What is the layered enforcement pipeline that makes typing, linting, formatting, practices, and
metrics NON-OPTIONAL for raw browser JS — from editor to pre-commit to CI to merge gate to release —
including tool choices, gate design (blocking vs advisory, ratcheting for legacy code),
architectural fitness functions, mutation testing, and the reproducibility (pinned toolchain, CI
parity) that makes a gate trustworthy?**

## The mess this addresses

Every check that *can* be skipped *will* be skipped under deadline; advice that isn't mechanically
enforced decays to zero (master brief §1). Prompts 02/03/06 define the *checks* (types, lint, format,
practices-as-rules, metrics); this mission makes them **fire automatically, block reliably, run
reproducibly, and stay adoptable on a legacy codebase** (ratchet, not rewrite). Without this layer,
the rest of the program is a pile of good intentions.

## Scope

- **In:** the defense-in-depth pipeline and layer design; **git hooks + staged-lint + commit-lint**
  tooling; **CI gate** design; **architectural fitness functions** (dependency/import boundaries,
  dead-code); **mutation testing** (gate confidence); **ratcheting / baselines** for legacy;
  **toolchain pinning + CI/local parity + reproducibility**; the "make the right thing the only easy
  thing" philosophy.
- **Out / defer:** the CHECKS themselves — prompt 02 (types), prompt 03 (lint/format), prompt 06
  (metrics). 05 **wires and sequences** them; it does not redefine them. Test **strategy/obligations**
  → the testing sibling (05 *runs* tests as a gate; it does not design them). Spec/traceability → the
  spec sibling.
- **Do NOT duplicate** the definition of any check. If you're specifying *what a rule catches*,
  you've drifted into prompt 03; come back to *how it's made to block*.

## Research decomposition (find answers to these)

### A. The defense-in-depth model
- The layers, fastest/cheapest first, and what each should catch:
  1. **Editor / LSP** (real-time: `tsserver`, ESLint LSP, format-on-save, **EditorConfig**);
  2. **pre-commit** (fast, *staged files only*: format + lint-fix + quick lint);
  3. **pre-push** (heavier: full typecheck, full lint, unit tests);
  4. **CI** (authoritative: everything, on a clean checkout);
  5. **merge / branch protection** (required status checks; no merging around a red build);
  6. **release** (build/publish-time, if any).
- The principle: **fail as early as possible, but CI is the source of truth** — local hooks are
  convenience and are bypassable (`--no-verify`). State *which check belongs at which layer and why*
  (speed vs authority).

### B. Git-hook & staged tooling (survey + verdict, VERSION-DEPENDENT)
- **Husky** vs **lefthook** vs **simple-git-hooks** vs native `core.hooksPath` vs the Python
  `pre-commit` framework — tradeoffs (speed, config surface, dependency weight, **Windows/PowerShell
  cross-platform** behavior — the target's primary OS).
- **lint-staged** (run linters/formatters on staged files only) — the standard partner; the
  "convenience, not enforcement" caveat (`--no-verify` exists → CI must re-check).
- **EditorConfig** as the editor-level baseline that needs no plugin agreement.

### C. Commit & PR hygiene
- **Conventional Commits + commitlint** (machine-readable history; changelog/semver automation); the
  `commit-msg` hook; PR-title linting. The value (traceability — spec sibling) vs ceremony tradeoff;
  when it is worth it for a small team.

### D. CI gate design
- The stages: install with **frozen lockfile** → typecheck (`tsc --noEmit`) → lint
  (`--max-warnings 0`) → format-check → test + coverage → fitness functions → build if any.
- **fail-fast vs run-all-then-report**; **required vs advisory** checks; branch protection / required
  status checks / no-force-push-to-main; caching for speed (tsc `--incremental`, ESLint cache); the
  **"green means green"** rule — no `|| true`, no ignored failures, no silently-non-blocking steps.

### E. Architectural fitness functions (enforce the architecture sibling mechanically)
- **dependency-cruiser** (forbidden dependencies, layering rules, orphan/cycle detection,
  visualization) and/or **eslint-plugin-boundaries** / **import-x** rules — encoding "no `fetch`
  outside the client module," "the pure core does not import the shell," "no cycles," "no cross-feature
  imports" (architecture §3.7, §3.1, functional-core/imperative-shell).
- **knip** (unused files / exports / dependencies — dead-code and dependency hygiene as a gate).
- The concept: **architecture as an executable test** (Ford et al., *Building Evolutionary
  Architectures* — fitness functions). Import-map / dependency-drift checks.

### F. Mutation testing (gate CONFIDENCE, not just coverage)
- **Stryker (JS/Mutator)**: mutants, mutation score, *why it beats line coverage* as a quality
  signal (coordinate with the testing sibling's "coverage as diagnostic" §7); the **cost** (slow —
  scope to the pure core; run on a schedule, not per-PR); realistic small-app adoption (targeted, not
  universal).

### G. The legacy problem — ratcheting & baselines (the adoption key)
- You cannot switch on maximal strictness/lint/complexity over an existing messy codebase without
  thousands of errors. The **ratchet**: baseline current debt, gate on "**no new violations / debt
  must not increase**," burn down over time.
- Tools/patterns: **betterer** (ratchet arbitrary checks — types, lint, complexity, custom);
  per-rule warn→error migration; tsconfig strict-flag-at-a-time (prompt 02 §E); ESLint baseline
  files; "**strict for new files, grandfather old**." The principle: the gate must be **adoptable on
  real code from day one**.

### H. Reproducibility & trust (a gate you can't reproduce isn't a gate)
- Pin the **entire toolchain** in `package.json` + a committed **lockfile**; `npm ci` /
  frozen-lockfile in CI; pin the Node/tool versions (`.nvmrc` / Volta / `engines`); **local↔CI
  parity** — ideally one aggregate script (`npm run check`) that both humans and CI run; deterministic
  checks (no network inside checks; pinned formatter/rules); the **re-baseline-at-major-bump**
  discipline (typing + platform siblings). Tie tool-version pinning to
  `web_platform_baseline_manifest.md` §7.

### I. The philosophy: make the right thing the only easy thing
- Golden-path scripts (`npm run check`, `npm run fix`); scaffolding/templates that **start
  compliant**; **defaults over documentation**; the smallest-viable gate a small team will actually
  keep green; avoiding **gate-bankruptcy** (too slow or too noisy → routinely bypassed). "Make the
  wrong thing hard or impossible" beats "document that it's discouraged."

## Controversies to resolve (positions first, then a recommendation)

- Are **git hooks** worth it given `--no-verify` and CI-as-authority? **Husky vs lefthook.**
- **Conventional-commits** ROI vs ceremony for a small team.
- **Mutation testing** ROI at small scale — worth the wall-clock?
- **Blocking vs advisory** for slow/fuzzy checks (mutation, some fitness functions).
- How strict a gate can a **solo/volunteer** team sustain before bankruptcy?
- **Ratchet-forever** vs scheduled cleanup sprints.

## Sources to prioritize

Docs for Husky / lefthook / simple-git-hooks / lint-staged / commitlint; the CI platform docs
(GitHub Actions, branch protection / required status checks); dependency-cruiser / knip /
eslint-plugin-boundaries / import-x docs; **Stryker** docs; **betterer** docs; Neal Ford, Rebecca
Parsons, Patrick Kua, *Building Evolutionary Architectures* (fitness functions — cite as the source
concept); the sibling manifests (architecture boundaries §3, testing coverage stance §7, platform
pinning §7). **Changelogs for every tool** — versions are perishable.

## Output contract

Produce a ground-truth manifest (suggested filename `js_enforcement_quality_gates_manifest.md`):
TL;DR (the layered-defense thesis + the "CI is truth, hooks are convenience, ratchet not rewrite"
principles); the **layered pipeline table** (layer → checks → speed → authority → bypassable?); the
**tool-choice verdicts** (hooks, staged, commitlint, fitness functions, mutation, ratchet); the
**recommended CI gate** definition (stages, blocking set, the aggregate `check` script); the
**fitness-function cookbook** (encoding sibling boundaries as executable rules); the **ratchet /
baseline playbook** for legacy; the **reproducibility checklist**; the **philosophy principles**; a
**gate-smell anti-pattern checklist** (`|| true`, ignored warnings, unpinned tools,
not-reproducible-locally, un-ratchetable, bypassed-hooks-as-only-line); a version matrix; sources
with access dates; cross-references.

## Cross-references

**Wires** prompt 02 (type gate + ratchet), prompt 03 (lint/format gate + `--max-warnings 0`), prompt
06 (metric budgets as gates), and the testing sibling (tests as a gate). Enforces
`web_architecture_manifest.md` §3 via fitness functions. Depends on
`web_platform_baseline_manifest.md` §7 for pinned versions.
