# Master Research Brief — JavaScript Safety & Maintainability

**Read this before running any prompt in this folder.** It is the shared preamble every
sub-prompt inherits: the mission, the version anchor, the epistemic protocol, the source-priority
rules, the output house style, the boundary map that keeps the six prompts from overlapping, and
the recurring ways this research goes wrong. Sub-prompts state only their mission-specific brief
and say "apply the master brief."

---

## 1. The mission

Produce a citable, decision-grade corpus answering: **how do you make raw, browser-native
JavaScript safe and maintainable — and mechanically enforce it?** The program follows the user's
escalation ladder, bracketed by diagnosis and measurement:

**diagnose** (what is intrinsically messy — 01) → **type** (02) → **lint** (03) →
**practice** (04) → **ENFORCE** (05, the payoff) → **measure** (06).

The load-bearing claim of the whole program: *a control that can be skipped will be skipped, and
advice that isn't mechanically enforced decays to zero.* Every prompt is judged by whether its
output lets a small team make and then **mechanically hold** a decision — not by how much it
surveys.

## 2. Relationship to the existing collection (extend, never duplicate)

A sibling collection lives at `../web_manifests/` (seven files: platform baseline, architecture,
typing-contract, testing, error-tracing, observability, spec discipline). It establishes the
*foundations*; this program builds the *enforcement, measurement, and diagnosis* layers on top.
Each sub-prompt names the sibling(s) it must **reference and extend rather than re-derive**. When
in doubt, cite the sibling by filename + section and move on. Duplicating a sibling's content is a
defect, not thoroughness.

The shared **version hub** for platform/edition/toolchain facts stays
`../web_manifests/web_platform_baseline_manifest.md`. This program adds the *tooling* version
facts (linters, formatters, gate tooling, metric tools); pin them the same way (exact versions,
re-baseline at each major).

## 3. Version anchor

**mid-2026.** Every version-dependent fact must be **dated**, tagged **VERSION-DEPENDENT**,
verified against a **primary changelog**, and flagged for re-verification at the next toolchain or
Baseline bump. The tool landscape moved fast into 2026 (ESLint flat config as the norm,
typescript-eslint majors, TypeScript 6.0 GA / 7.0 "Corsa" RC, Biome/oxlint maturing) — treat every
version number as perishable. Do not assert a precise tool version as fact from memory; name the
tool, state the anchor, and verify.

## 4. Target context (this constrains every recommendation)

Identical to the sibling collection: **raw HTML/CSS/JS; entirely client-side; API calls only where
unavoidable; no framework; no mandatory build step; reuse-first components; small-scale.**
Consequences the researcher must honor:

- **The deliverable runs in a browser; the tooling runs in CI/Node.** Keep browser-*runtime* facts
  and Node-*tooling* facts strictly distinct.
- **No-build is the default, not a limitation to design around.** Tooling that assumes a
  bundler/transpiler pipeline (Babel plugins, webpack/Vite loaders, framework-coupled configs) is a
  poor default here. CI-time checkers that read *raw* `.js` (tsc `--checkJs`, ESLint, formatters,
  graph analyzers) are the fit.
- **Introducing a build step is a recordable architectural decision, not a free move** (cf.
  `web_platform_baseline_manifest.md` §4). Where an option genuinely requires one (e.g. authoring in
  `.ts`, minification stripping `invariant()` calls), present it *as* such a decision with its
  tradeoff — never smuggle a build in as the default.
- **Small-scale + reuse-first** means: prefer the 15-line fake over the framework, the ratchet over
  the rewrite, the smallest gate a team will actually keep green over the maximal one they will
  bypass.

## 5. Epistemic protocol (the tag legend + the rules)

Tag every material claim:

- **ESTABLISHED** — normative (ECMA-262 / WHATWG / W3C) or long-stable and primary-sourced.
- **VERSION-DEPENDENT** — bound to a spec edition, browser/Baseline tier, or tool version. Date it.
- **OPEN** — no authoritative source, a project-policy call, or a genuinely contested question.

Rules:
1. **Distinguish three registers:** spec-normative *fact* vs community *convention* vs individual
   *opinion*. Never launder opinion as fact. A style-guide rule and a language semantic are not the
   same kind of claim.
2. **On contested questions, present the major positions with their strongest cases *before* giving
   a decision-grade recommendation.** The recommendation is required (this is not a survey), but it
   must be visibly earned.
3. **Separate what a tool *claims* from what is *demonstrated*.** "10× faster," "zero-config,"
   "strictest" are marketing until you find the benchmark, the adoption evidence, and the known
   limitation set. Report the limitation set.
4. **Primary sources and changelogs over blog aggregations and lagging registry pages.** Cite with
   **URL + access date**. Flag any claim resting only on a vendor blog.
5. **Empirical claims need empirical sources.** Metric validity, defect prediction, and
   mutation-testing efficacy are research questions — cite the literature and report when it is
   mixed, not just the convenient result.

## 6. Source priority

1. **Normative specs** — TC39 / ECMA-262, WHATWG (HTML/DOM/Fetch/Console), W3C.
2. **Official tool docs + release notes/changelogs** — TypeScript, ESLint, typescript-eslint,
   Biome, oxlint, Prettier, Stryker, dependency-cruiser, knip, Husky/lefthook, commitlint, betterer,
   SonarJS, etc.
3. **MDN + web.dev/Baseline** for platform support and per-feature availability.
4. **Named practitioners/authorities** where the question is *doctrine* not fact — cite them **as
   opinion** and critique, don't canonize (Crockford, Fowler, Ford, Tornhill, King, Bernhardt,
   Feathers).
5. **Peer-reviewed / empirical SE literature** where a claim is empirical.

## 7. Output house style (every deliverable)

Match the sibling manifests exactly:

- A **TL;DR** stating the 3–6 load-bearing decisions.
- **Numbered sections**; dense, decision-oriented prose; no filler.
- A **tag legend** and consistent inline tagging (§5).
- **Decision-grade recommendations** — say what to *do* and name the tradeoff, not just "here are
  the options."
- A **VERSION MATRIX** table for version-dependent facts (feature/tool → version → note).
- An **ANTI-PATTERN / smell checklist**.
- A **DECISION FLOWCHART or checklist** where the topic supports one.
- A **"what this CANNOT do / residual risk"** section — the honest limits, and what it hands off to
  a sibling.
- A **Sources** list (URL + access date).
- **Cross-references** to siblings by filename + section.

## 8. The sub-prompt boundary map (read to avoid overlap)

- **01 — Language safety subset & footguns.** The *diagnosis*: intrinsic hazards and the
  maximal-safety modern subset; the 4-way catchability classification (type / lint / feature /
  contract-only). Hands the contract-only residue to the typing + error siblings.
- **02 — Static typing: enforcement, coverage, migration, decision.** *Deepens*
  `js_typing_contract_manifest.md`; does **not** re-derive JSDoc vocabulary. Owns: strictness-dial
  completeness, type-coverage measurement + gate, `any`/assertion/`@ts-expect-error` debt ratchet,
  untyped-dependency strategy, untyped→strict migration, the JSDoc-vs-TS-vs-TC39 approach decision,
  the static/runtime seam.
- **03 — The pedantic linter (+ formatter).** Owns the automated static-analysis layer: ESLint flat
  config + typescript-eslint, the rule taxonomy + curated maximal-defensible set, the plugin
  ecosystem, custom AST rules, Biome/oxlint, the lint/typecheck/format division of labor,
  formatting, suppression hygiene. **Defines** checks; 05 **wires** them.
- **04 — Coding practices, idioms & anti-patterns.** The human-convention layer at
  function/expression/module-hygiene altitude (one level *below* the architecture sibling). Every
  item tagged with its enforcement mechanism, routing specifics to 02/03/05/06 and naming the
  review-only residue.
- **05 — Enforcement machinery & quality gates.** The *payoff*: the layered defense pipeline,
  git-hook/staged-lint/commit-lint tooling, architectural fitness functions, mutation testing, gate
  design (blocking vs advisory, ratcheting/baselines for legacy), toolchain pinning + CI parity, the
  "make the right thing the only easy thing" philosophy. **Wires** the checks 02/03/06 define;
  does not redefine them.
- **06 — Maintainability measurement & complexity budgets.** What to *measure* so 05 can gate it:
  cognitive vs cyclomatic complexity, size/coupling metrics, churn×complexity hotspots, the tool
  landscape, metric validity, budget-setting + ratcheting under the Goodhart/diagnostic discipline.
  Extends (does not duplicate) the testing sibling's coverage-as-diagnostic stance to the other
  metrics.

## 9. How to run

Each prompt is self-contained. Run one in isolation for a single manifest, or the whole program in
order `01 → 06`. When run as a program, later prompts may cite earlier outputs (e.g. 05 wires the
config 03 recommends; 06 feeds thresholds to 03/05; 02's migration order consumes 06's hotspots).
Each prompt's **output contract** names the manifest it should produce and a suggested filename.

## 10. Pitfalls for the researcher (recurring failure modes)

1. **Node-tooling vs browser-runtime confusion.** The two live in the same repo but different
   worlds. Label which is which.
2. **Bundler/framework assumptions.** Most "JS best practice" content assumes React + Vite/webpack.
   Filter hard for the no-build raw-JS target; discard framework-coupled advice or mark it as
   out-of-context.
3. **Version drift.** Date and changelog-verify every tool/edition fact. A config that was "strict"
   in an earlier major may mean something different now.
4. **Tool marketing.** Convert every superlative into a demonstrated fact + a limitation set.
5. **Goodhart on every metric.** Carry the sibling testing manifest's diagnostic-not-target
   discipline into typing coverage (02), lint counts (03), and all maintainability metrics (06).
6. **Recommending heavy where the target is small.** A ratchet beats a rewrite; a 15-line fake beats
   a framework; the smallest green-able gate beats the maximal bypassed one.

## 11. Optional extensions (flag, don't assume)

If the program should grow, the two most defensible additions are: a dedicated
**security/injection-hardening** mission (Trusted Types, CSP, XSS sinks, supply-chain provenance) if
the threat surface exceeds the XSS/boundary coverage folded into 03/04/05; and a
**dependency/supply-chain** mission if the app's dependency count grows past "minimal." Both are out
of scope for the core six unless the target context changes.
