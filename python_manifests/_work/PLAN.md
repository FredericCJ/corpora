# Python manifest set — update & augmentation plan (2026-08-08)

**Mandate.** `manifests/` is the grounding pack handed to coding agents so they build Python software
that is **testable, diagnosable, maintainable, modular, and easy to build incrementally**. This
endeavour (a) re-verifies and updates the existing Python manifests against live primary sources, and
(b) augments the set from the SWE research corpus so every one of those five pillars has a manifest
that names its mechanisms in citable vocabulary.

## The five pillars → the file that owns each

| pillar | owning manifest | status |
|---|---|---|
| version ground truth (shared hub) | `python_platform_baseline_manifest.md` | **NEW** |
| testable | `python_testing_tooling_manifest.md` | update |
| diagnosable — error contract | `error_tracing_contract_manifest.md` | update |
| diagnosable — logs & telemetry | `logging_observability_manifest.md` | update |
| diagnosable — live runtime | `python_runtime_diagnostics_manifest.md` | **NEW** |
| maintainable — contracts | `python_typing_contract_manifest.md` | update |
| maintainable — hazard diagnosis | `python_language_hazards_manifest.md` | **NEW** |
| maintainable — lint & practice | `python_linting_practices_manifest.md` | **NEW** |
| modular | `python_module_boundaries_manifest.md` | **NEW** |
| incremental build — enforce & measure | `python_quality_gates_manifest.md` | **NEW** |
| concurrency (cuts across all five) | `python_concurrency_determinism_manifest.md` | **NEW** |
| reasoning frame (agnostic) | `architecture_manifest_default.md` | augment |
| spec discipline (agnostic) | `software_spec_discipline_manifest.md` | light touch |
| collection entry point | `README.md` | **NEW** |

## The enforcement ladder — inherited from the sibling `js/` and `jsts/` programs

The project owner's stated throughline, which this set now carries for Python:

> Static typing is a good start. A pedantic linter is very nice. A set of coding practices is also
> nice. **A way of enforcing all of it is the point** — advice that isn't mechanically enforced
> decays to zero.

The rungs, and the file that owns each:

`python_language_hazards_manifest.md` (**diagnose** what is actually treacherous) →
`python_typing_contract_manifest.md` (**type**) →
`python_linting_practices_manifest.md` (**lint + practise**) →
`python_quality_gates_manifest.md` (**enforce + measure**).

Every hazard and practice in the middle two files carries an explicit **enforcement route**:
type-catchable (which checker and flag) · lint-catchable (the exact rule code) · feature-eliminated
(a modern construct removes the hazard class) · test-catchable · fitness-function (a CI structural
check) · **contract-only** (nothing mechanical catches it — say so rather than implying coverage).
An unrouted practice is a defect: it is a preference dressed as grounding.

Out of primary scope this pass: `uml25_ocl_conformance_manifest.md`,
`spec_recovery_reverse_engineering_manifest.md`, `claude_code_agent_teams_manifest.md` (cross-links
updated only).

## Two registers — do not mix them

The folder holds two deliberately different kinds of document. Match the register of the file you are
writing.

**Ground-truth register** — `python_*`, `error_tracing_*`, `logging_observability_*`, and every NEW
file. Version-anchored, epistemically tagged, inline-cited, `## Sources` with access dates. Opens with
a bolded **Purpose.**/**Scope.** paragraph that states the target (small-to-mid, strictly-typed Python),
declares *GROUNDING, not a rulebook*, defines the tag legend, and names the sibling manifests it defers
to. Ends with anti-patterns, open questions, and sources.

**Reasoning register** — `architecture_manifest_default.md`, `software_spec_discipline_manifest.md`.
Domain-agnostic, hard-wrapped ~70 cols, no version anchors, no tags, no source list. Prose that names
tradeoffs and refuses to prescribe. Augment additively; never retro-fit the ground-truth template onto
these two.

## House rules for every file touched

1. **Epistemic tags are mandatory in the ground-truth register.** `ESTABLISHED` (normative and stable
   in the cited primary source) · `VERSION-DEPENDENT` (bind to the exact version) · `OPEN` (no
   authoritative source; a convention the project must pin) · `CC-FACT` (Claude Code mechanics).
   An untagged factual claim is a defect.
2. **Never fabricate.** No invented version, date, PEP number, API name, element id, or citation.
   Omit sooner than guess; an honest `OPEN` outranks a plausible sentence. Where the only evidence is
   secondary, write `FLAGGED-SECONDARY` inline.
3. **Version facts route through the hub.** `python_platform_baseline_manifest.md` is the single
   version anchor. Other files state *behaviour* and cite the hub for *when*; they do not re-assert
   release dates. Each keeps a one-line "Version anchor: see `python_platform_baseline_manifest.md`
   (2026-08-08)" header instead of its own drifting table.
4. **Cross-reference, never duplicate.** State the rule once in its owning file; elsewhere name the
   file. Every manifest ends with a `### Sibling manifests` block that says what it defers to.
5. **Hard-wrap prose at 100 columns** in new files. Do not reflow existing files wholesale — that
   destroys the diff. Match the local wrapping of the paragraph you are editing.
6. **Line width of tables is exempt** from the wrap rule.
7. **Sources carry access dates**: `- <what> — <url> . Accessed 8 Aug 2026.`
8. **Anti-patterns section is a rejection list**, one line each, each pointing at the section it
   violates. This is the part agents actually obey.
9. **Open questions are addressed to the project**, phrased as a decision to be made, tagged `OPEN`,
   and cross-referenced to `software_spec_discipline_manifest.md` §G5.
10. **Named vocabulary imported from the SWE corpus must carry its citation** — the naming work and
    year, as recorded in `SWE/design_elements_corpus_v1_0.md`. Vocabulary without a source is a
    preference, not grounding, and must be tagged `OPEN`.
11. **Scale discipline.** The target is small-to-mid single-process Python, not a distributed
    platform. When importing a mechanism whose home is distributed systems, say plainly that it is
    over-engineering at this scale. Restraint is content.
12. **Where a claim is about what a tool DOES, run the tool.** Added after the 2026-08-08 audit, which
    found that both config-breaking CRITICAL defects were tool-behaviour claims taken from
    documentation prose rather than from the tool — a rule code that does not exist (`D216`) and a rule
    wrongly listed as enabled-by-default (`LOG004`). Documentation describes intent; the resolved
    settings are the fact. So: if the tool can be run, run it, and record **the tool version and the
    exact command** beside the result under the `MEASURED` tag. A measurement reported without its
    command is not reproducible and is not evidence — one of this pass's wrong claims came from a
    measurement run against the wrong subcommand and reported as if it settled the question.

## Scope boundaries between the new files — enforced, to prevent overlap

- `python_platform_baseline_manifest.md` — **only** version/support/schedule/PEP-status facts,
  interpreter switches, build variants, and the minimum-target policy. No design advice.
- `python_module_boundaries_manifest.md` — the *unit of change*: project layout, packaging metadata,
  the import system as a boundary, public-API and deprecation contract, plugin seams, and machine
  enforcement of dependency direction. Owns `import-linter`/`Tach`. Does **not** own CI wiring.
- `python_quality_gates_manifest.md` — the *ratchet*: which checks run, where, how they fail, and how
  a standard is adopted incrementally without a big-bang rewrite. Owns `ruff`/`pre-commit`/CI matrix/
  supply-chain gates/metrics. Does **not** re-teach typing or testing content — it gates them.
- `python_runtime_diagnostics_manifest.md` — everything that inspects a **running or crashed** process:
  attach, monitoring, faulthandler, tracemalloc, profilers, post-mortem, self-test, health surfaces.
  Logs and telemetry stay in `logging_observability_manifest.md`; the error *contract* stays in
  `error_tracing_contract_manifest.md`.
- `python_concurrency_determinism_manifest.md` — the four execution models, structured concurrency,
  cancellation, and how to keep concurrent code deterministic under test. Owns free-threading and
  subinterpreter facts *as behaviour*; the hub owns their version status.
- `python_language_hazards_manifest.md` — the *diagnosis*: intrinsic Python footguns and the
  maximal-safety modern subset, every hazard routed to its enforcement mechanism. States hazards; does
  **not** teach the type system (that is the typing manifest) and does **not** enumerate lint config
  (that is the linting manifest) — it cites the rule code and moves on.
- `python_linting_practices_manifest.md` — the *rule set and the idiom catalogue*: which ruff/pylint
  families to enable and why, the formatter/linter/checker division of labour, suppression hygiene, and
  the function/module/expression-altitude practice and anti-pattern catalogue with each entry routed.
  Does **not** own CI wiring or metrics.

## Provenance of this pass

- Live re-verification: `_work/facts/r01..r10_*.md` — one fact pack per topic, primary sources loaded
  2026-08-08.
- SWE corpus mining: `_work/seed/s1..s4_*.md` — named, citable design/architecture vocabulary mapped
  to Python mechanisms, with fold/import/do-not-transpose adjudication.
- Nothing is committed to git; that is the user's call (standing house rule).
