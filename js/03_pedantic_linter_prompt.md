# Deep-Research Prompt 03 — The Pedantic Linter (and Formatter)

**Part of** the JavaScript Safety & Maintainability program. **Apply `00_master_research_brief.md`**
for the version anchor (mid-2026), target context, epistemic protocol, source priority, and output
house style. This file adds only the mission-specific brief.

---

## Mission (the one question)

**What is the maximally-pedantic-yet-defensible static-analysis and formatting layer for raw browser
JS as of mid-2026 — the linter (engine, config system, curated rule set, plugin ecosystem, custom
rules), the formatter, their division of labor with the type-checker, and the discipline for
managing suppressions and rule debt?**

## The mess this addresses

Unlinted JS accumulates inconsistency and latent, bug-shaped code. But *over*-linting — thousands of
style nits, mutually-conflicting rules, minute-long runs — causes rule-bankruptcy and the
blanket-`eslint-disable` that follows. The pedantry has to be *defensible*: every rule earns its
false-positive cost. The sibling manifests keep deferring to here — the typing manifest's "pin the
lint stack," the error manifest's "enforce `no-floating-promises` in CI," the observability
manifest's "lint-ban stray `console` outside app modules." This mission builds the actual linting
doctrine those deferrals assume.

## Scope

- **In:** ESLint 9+ flat config; typescript-eslint (type-aware linting of JSDoc'd raw JS); the rule
  **taxonomy** and a curated **maximal-defensible** set; the **plugin ecosystem**; the
  linter/typechecker/formatter **boundary**; **formatting** (Prettier vs Biome vs dprint); **Biome
  & oxlint** as fast all-in-one contenders; **custom AST rules**; **security** linting;
  **suppression & rule-debt hygiene**; type-aware lint **performance**.
- **Out / defer:** *which practices* to encode (prompt 04 supplies the practice list and its
  rationale; 03 supplies the enforcing rule); *running* lint in the pipeline / pre-commit / CI →
  prompt 05 (03 defines the checks, 05 wires them); type-**coverage** gating → prompt 02; complexity
  **thresholds** → prompt 06 sets the number, 03 enforces it.
- **Do NOT duplicate** prompt 04's practice rationale or prompt 05's pipeline wiring.

## Research decomposition (find answers to these)

### A. Engine & config
- **ESLint 9+ flat config** (`eslint.config.js`) as the norm at the anchor; migration from
  `.eslintrc`; the `languageOptions` / `plugins` / `rules` model; config composition/sharing.
- **typescript-eslint** integration for *type-aware* linting of raw JSDoc'd `.js`
  (`parserOptions.projectService`); which powerful rules require type info; the **performance cost**
  of type-aware linting and how to scope it (project service, caching).

### B. The rule taxonomy (organize the universe, then curate)
Classify the rule space and name the load-bearing members of each class:
- **(i) Correctness / possible-errors** (the bug-catchers): `no-floating-promises`, `no-unsafe-*`
  (typescript-eslint), `no-cond-assign`, `no-constant-condition`, `use-isnan`, `valid-typeof`,
  `require-atomic-updates`, `no-unused-vars`, `no-fallthrough`, …
- **(ii) Suspicious / best-practice:** `eqeqeq`, `no-implicit-coercion`, `no-param-reassign`,
  `no-shadow`, `consistent-return`, `no-return-await`, `prefer-const`, …
- **(iii) Restriction (ban features):** `no-var`, `no-eval`, `no-implied-eval`, `no-with`,
  `no-proto`, `no-console` (**with the app-module exception** the observability sibling requires),
  and the general-purpose banhammers `no-restricted-syntax` / `-globals` / `-imports` / `-properties`.
- **(iv) Complexity / maintainability:** `complexity`, `max-depth`, `max-lines`,
  `max-lines-per-function`, `max-params`, `max-statements`, `max-nested-callbacks` — **thresholds
  owned by prompt 06**, mechanism here.
- **(v) Stylistic:** mostly **ceded to the formatter** (see §D) — enumerate what should *not* live in
  lint.
For each class, state which rules are worth their false-positive cost for the target and which are
noise.

### C. The plugin ecosystem (survey + a verdict each)
Assess, with an adopt/skip verdict for the maximal-defensible set:
- **typescript-eslint** (mandatory for type-aware rules).
- **eslint-plugin-unicorn** (pedantic modernizer — flag which rules are dogma).
- **eslint-plugin-sonarjs** (bug/smell detection, cognitive-complexity — overlaps prompt 06).
- **eslint-plugin-security** / **eslint-plugin-no-unsanitized** (XSS sinks; the Trusted Types
  adjacency — `innerHTML`/`insertAdjacentHTML` detection).
- **eslint-plugin-promise**; **eslint-plugin-import(-x)** (module hygiene, cycle detection, ordering)
  and **eslint-plugin-boundaries** (architecture — hand the *gate* to prompt 05).
- **eslint-plugin-jsdoc** (JSDoc completeness/validity — the enforcement half of the typing
  sibling's doc conventions; `@throws`, `@param` completeness).
- **eslint-plugin-regexp** (ReDoS / regex safety — enforces prompt 01's §E findings).
- **eslint-plugin-compat** (Baseline-target enforcement — ties to `web_platform_baseline_manifest.md`
  §2).
- **eslint-plugin-eslint-comments** (govern the *suppressions themselves* — §F).

### D. Linter vs type-checker vs formatter — the division of labor
State a crisp doctrine: **types** catch type errors; the **linter** catches patterns/practices/idioms
and bug-shaped code; the **formatter** owns whitespace/quotes/semicolons/line-width. **Disable every
stylistic lint rule that conflicts with the formatter** (`eslint-config-prettier`, or Biome's
unified model). Never relitigate formatting inside lint.

### E. Formatting
- **Prettier 3.x** (opinionated, near-universal, ends the debate) vs the **Biome** formatter vs
  **dprint** — determinism, config minimalism, the "one formatter, no arguments" rule. Recommend a
  default and name the tradeoff (verify versions against changelogs).

### F. The fast all-in-one contenders (maturity assessment — separate claim from demonstrated)
- **Biome** (Rust; lint + format unified): rule parity with ESLint? Does it do **type-aware** rules
  yet at the anchor? Plugin story? — report the *demonstrated* limitation set.
- **oxlint** (Rust / Oxc; very fast): rule coverage vs ESLint; the "fast pre-filter alongside ESLint
  for the type-aware depth" pattern.
- The honest recommendation: **ESLint + typescript-eslint** for depth, optionally **Biome/oxlint**
  for speed — and precisely where each falls short for the target.

### G. Custom rules (when the curated set can't express a project invariant)
- Writing an **AST rule** (ESLint custom rule via `@typescript-eslint/utils`) vs the cheap path of
  `no-restricted-syntax` with an **ESQuery selector**.
- A cookbook of **project-invariant rules that enforce sibling manifests**: ban `console` outside
  designated app modules (observability §4); forbid `fetch` outside the client module (architecture
  §3.7); require `cause` on re-throws / forbid `throw` of non-`Error` (error §3–§4); ban reading
  state back out of the DOM (architecture §3.1). These convert prose doctrine into machine-checked
  contracts.

### H. Suppression & rule-debt hygiene
- `eslint-disable` discipline: require a reason; prefer line/next-line over file/block; **ban blanket
  disables** via eslint-plugin-eslint-comments; count disables as debt and **ratchet** (same
  philosophy as prompt 02).
- **`--max-warnings 0` in CI** — the "a warning that doesn't block is a lie" stance; the error-vs-warn
  taxonomy (what should *block* vs *inform*, and why "warn" is mostly a migration state).

### I. The deliverable config
- A recommended, **annotated flat-config shape** as the maximal-defensible starting point: the
  base/curated blocks, the plugin set, the type-aware layer, the formatter-conflict disables, the
  app-module override for `no-console`, the pinned versions — with per-block rationale.

## Controversies to resolve (positions first, then a recommendation)

- **recommended vs strict vs all** rule posture — does maximal pedantry pay, or backfire into
  disable-blindness?
- **Prettier vs Biome** formatter.
- **ESLint vs oxlint/Biome** maturity for a serious pedantic config in 2026.
- **StandardJS's** zero-config/no-semicolon stance vs a curated configurable set.
- How much of **unicorn** is real safety vs taste.
- **type-aware lint cost** vs value on a no-build project; **warnings-as-errors**.

## Sources to prioritize

ESLint docs (flat config, rule reference); typescript-eslint docs; each plugin's own docs;
Prettier / Biome / dprint docs + any published benchmarks; oxlint / Oxc docs; **changelogs for all**
(versions are perishable — master brief §3); the sibling manifests for the specific rules they
demand (`js_error_tracing_contract_manifest.md` §6/§13, `browser_observability_manifest.md` §4,
`js_typing_contract_manifest.md` §8, `web_platform_baseline_manifest.md` §2/§7).

## Output contract

Produce a ground-truth manifest (suggested filename `js_linting_formatting_manifest.md`): TL;DR (the
division-of-labor doctrine + the curated-set thesis + the Biome/oxlint verdict); the
**linter/typechecker/formatter division-of-labor** doctrine; the **rule taxonomy** with the curated
maximal-defensible set (each rule → what it catches → verdict); the **plugin adoption table**; the
**formatter decision**; the **Biome/oxlint maturity verdict** (claim vs demonstrated); the
**custom-rule cookbook** (with the sibling-seam examples); the **suppression-hygiene** rules; the
**annotated recommended config** artifact; a version matrix; an anti-pattern checklist (blanket
disable, non-blocking warnings, format-in-lint, unpinned plugins); sources with access dates;
cross-references.

## Cross-references

Enforces prompts 01 (footgun rules) and 04 (practices-as-rules); enforces sibling doctrine
(observability §4, error §6/§13, architecture §3.7, platform §2). Feeds prompt 05 (which runs lint
as a gate) and receives thresholds from prompt 06 (complexity rules). Coordinates with prompt 02 on
the typescript-eslint `no-unsafe-*` family.
