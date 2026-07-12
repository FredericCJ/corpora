# Deep-Research Prompt 06 — Maintainability Measurement & Complexity Budgets

**Part of** the JavaScript Safety & Maintainability program. **Apply `00_master_research_brief.md`**
for the version anchor (mid-2026), target context, epistemic protocol, source priority, and output
house style. This file adds only the mission-specific brief.

---

## Mission (the one question)

**What should you MEASURE to know raw browser JS is maintainable (and to detect it becoming a mess),
which tools compute it as of mid-2026, how valid is each metric, and how do you set and RATCHET
defensible budgets — feeding thresholds to the linter (03) and gates (05) while respecting the
diagnostic-not-target discipline?**

## The mess this addresses

"Maintainable" is usually *asserted*, not *measured*. Teams either ignore complexity until it is
unmanageable, or adopt a vanity metric (a coverage number, a Maintainability Index) that Goodhart's
into meaninglessness. This mission grounds measurement: which metrics actually track maintenance
pain, which are theater, how to compute them cheaply in a no-build project, and how to gate on them
**honestly** — so prompt 05 has real numbers to enforce and prompt 02 has a real signal for
migration order.

## Scope

- **In:** the metric catalogue + validity assessment; the tool landscape; budget-setting +
  ratcheting; churn/hotspot analysis; the Goodhart/diagnostic discipline.
- **Out / defer:** the ENFORCEMENT *wiring* → prompt 05 (05 gates the budgets 06 sets); the lint-rule
  *mechanics* → prompt 03 (03 enforces the number 06 chooses); **test coverage** as a metric → the
  testing sibling §7 (reference its coverage-as-diagnostic stance; do **not** re-derive it — 06 covers
  the *other* maintainability metrics); **type coverage** → prompt 02.
- **Do NOT duplicate** the testing sibling's coverage treatment. *Extend* its measurement philosophy
  to complexity/size/coupling/churn.

## Research decomposition (find answers to these)

### A. Size & structure metrics
- LOC/SLOC per file/function; function length; parameter count; nesting depth; statements per
  function. What each predicts and its sane limits for raw JS; the ESLint rules that measure them
  (`max-lines`, `max-lines-per-function`, `max-params`, `max-depth`, `max-statements`,
  `max-nested-callbacks`) — **thresholds set here, enforced by prompt 03**.

### B. Complexity metrics — the core
- **Cyclomatic complexity** (McCabe): definition, what it captures (independent paths → a test-count
  lower bound), its blind spots.
- **Cognitive complexity** (SonarSource): how it differs — penalizes nesting and broken control flow,
  ignores mere size — and why it is arguably the better *maintainability* proxy. **Recommend it as
  the primary complexity metric** (argue it).
- **Halstead** measures: historical, low practical value — say so plainly.
- The ESLint `complexity` rule vs `eslint-plugin-sonarjs` cognitive-complexity; recommended
  thresholds + rationale.

### C. Coupling & cohesion metrics
- Fan-in/fan-out, afferent/efferent coupling, instability, **dependency cycles**, module-graph
  metrics; computed via **dependency-cruiser** / **madge** / import graphs (tool overlaps prompt 05's
  fitness functions — **here it is measurement, there it is the gate**). The thesis: **cyclic
  dependencies and high fan-out are the maintainability killers**; argue where the signal is real.

### D. Composite indices & their critics
- The **Maintainability Index** (Coleman–Oman; the radon/Visual-Studio-style formula): what it
  combines, and the **substantial critique** (arbitrary constants, gameability, weak validity).
  Present honestly; **recommend against it as a target**. Note any 2026 successors.

### E. Churn & hotspots (highest-signal, most-underused)
- **Code churn × complexity = hotspots** (Adam Tornhill, *Your Code as a Crime Scene* / CodeScene):
  why files that are **both** complex **and** frequently-changed concentrate maintenance cost;
  computing it from **git history** (log-based; tool-assisted); using it to **prioritize** — the
  migration order for prompt 02, refactor targets, and where code-review rigor should go (prompt 04's
  review-only residue). This reframes measurement from "score everything equally" to "**find the few
  places that matter.**"

### F. Duplication & dead code
- Copy-paste detection (**jscpd**, SonarJS); dead code / unused exports/deps (**knip** — measurement
  side; prompt 05 gates it). Duplication as a maintainability tax; the "rule of three" vs premature
  DRY (coordinate with prompt 04's over-abstraction anti-pattern).

### G. The tool landscape (survey + verdict, VERSION-DEPENDENT)
- **SonarJS / SonarQube-or-SonarCloud** (cognitive complexity, smells, duplication — heaviest, most
  complete); **ESLint complexity rules + eslint-plugin-sonarjs** (in-pipeline, lightweight);
  **dependency-cruiser / madge** (coupling/graph); **jscpd** (duplication); **knip** (dead code);
  git-based **churn** tooling / CodeScene (hotspots). State what fits a **small no-build raw-JS
  project** (lightweight, in-CI) vs what is overkill.

### H. Setting & ratcheting budgets (the honest part)
- How to pick a threshold: **percentile of the current distribution**, not a magic number — start
  where you are and **ratchet down** (coordinate with prompt 05's betterer); per-metric budgets;
  fail-vs-warn; the "**budget the trend, not the absolute**" stance; justified per-file escape
  hatches.

### I. The Goodhart / diagnostic discipline (the throughline)
- Every metric is a **flashlight, not a target** (inherit the testing sibling §7 doctrine); a gamed
  metric is worse than none; **combine metrics** (no single number); use them to **ask questions**
  ("*why* is this file a hotspot?") not to rank people; the metric-abuse anti-patterns
  (coverage-100%-theater, MI-as-KPI, complexity-gaming by extracting meaningless helper functions).

## Controversies to resolve (positions first, then a recommendation)

- **Cyclomatic vs cognitive** complexity as the primary gate metric.
- Is the **Maintainability Index** worth anything, or pure theater?
- Do these metrics **predict defects / maintenance cost at all**? (the empirical literature is mixed
  — present it, don't cherry-pick.)
- **SonarQube heaviness** vs an ESLint-only lightweight stack for a small project.
- **Churn/hotspots** (high-signal, less-known) vs traditional per-file scores as the primary lens.
- **Absolute thresholds** vs **distribution-relative** vs **ratchet-only**.

## Sources to prioritize

McCabe's original cyclomatic-complexity paper; the **SonarSource cognitive-complexity** white paper;
the **Maintainability Index** critiques (blog + literature); **Adam Tornhill / CodeScene** on churn &
hotspots; **empirical SE literature** on metric validity and defect prediction (report the mixed
results honestly); tool docs (SonarJS, ESLint complexity rules, dependency-cruiser, madge, jscpd,
knip); the **testing sibling §7** for the coverage-as-diagnostic doctrine this extends. Changelogs
for version-dependent tool facts.

## Output contract

Produce a ground-truth manifest (suggested filename `js_maintainability_metrics_manifest.md`): TL;DR
(the "measure hotspots + cognitive complexity + cycles, ratchet not target, no single number"
thesis); the **metric catalogue** (metric → what it predicts → validity → tool → recommended budget →
verdict); the **"primary metrics to actually gate"** shortlist (cognitive complexity + size limits +
cycles + hotspots) vs the **"measure-but-don't-gate / theater"** list (MI, Halstead); the
**churn×complexity hotspot method** (with a concrete how-to from git history); the **budget-setting +
ratchet recipe**; the **Goodhart discipline** restated for these metrics; a metric-abuse
anti-pattern checklist; a version matrix; sources with access dates; cross-references.

## Cross-references

Feeds prompt 03 (complexity/size *thresholds* to enforce), prompt 05 (budgets to *gate*, via
betterer), and prompt 02 (hotspot-ordered migration). Extends the testing sibling §7
(coverage-as-diagnostic) to complexity/coupling/churn; supplies prompt 04 the data for where
review-only attention should concentrate.
