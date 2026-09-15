# Cross-file decisions for the fix round — binding on every fixer

The audit found several defects that span files. If each fixer decides independently, the collection
ends up with new contradictions. **These decisions are already made. Apply them; do not re-litigate
them.** Where your findings file prescribes something that conflicts with a decision here, this file
wins — and say so in your receipt.

---

## D1. The minimum-target floor — ONE answer, stated in the hub

**The defect:** the collection currently gives three answers. `python_testing_tooling_manifest.md`
asserts "3.11 is the defensible floor for new work"; `error_tracing_contract_manifest.md` §21 says
"3.13+, and prefer 3.14"; the hub declares the whole question OPEN and takes no position, so
`python_module_boundaries_manifest.md` defers to a hub that defers back. An agent writing a new
`pyproject.toml` has no answer at all.

**The decision:** the hub states a **recommended default with its rationale, its alternative, and what
each forfeits**. The floor stays tagged `OPEN` as a *policy* choice — that is honest, because a library
needing reach may legitimately go lower — but it now carries a starting point, so no reader is stranded.

**The default is `requires-python = ">=3.13"`.** The reasoning is behavioural and calendar-based, not
fashion:
- On 2026-08-08 **only 3.13 and 3.14 are in the bugfix phase**; 3.12 and below are security-only, and
  3.10 reaches EOL around 2026-10. A new project should not floor on a security-only branch.
- 3.13 makes native **every construct this collection's own rules depend on**: `@warnings.deprecated`
  (PEP 702), callable `split`/`subgroup` conditions on `ExceptionGroup`, and `exc_type_str`. Below 3.13
  the deprecation-visibility contract (D4) cannot be satisfied without backports.

  **ERRATUM (recorded 2026-08-08, after the fix round).** This decision as originally written also
  listed *group-aware `contextlib.suppress`* among the constructs 3.13 makes native. **That was wrong**
  — `docs.python.org/3/library/contextlib.html` reads "Changed in version 3.12: `suppress` now supports
  suppressing exceptions raised as part of a `BaseExceptionGroup`". The hub fixer caught the error,
  refused to propagate it, and recorded the correction in
  `python_platform_baseline_manifest.md`. The decision itself is unaffected — three constructs still
  justify the 3.13 floor, and 3.12 is security-only regardless — but the error is left visible here
  rather than quietly deleted, because a decisions file that silently rewrites itself is worthless as
  provenance. It is also the round's clearest evidence that instructing fixers to refute their
  instructions with sources was the right call.
- Prefer **3.14** where nothing forces compatibility: it adds the PEP 765 `SyntaxWarning` that converts
  the `return`-in-`finally` rule from review-only into compiler-enforced, plus PEP 768 remote attach.

**The alternative, stated rather than hidden:** `">=3.12"` aligns with SPEC 0's 36-month window and is
the right choice for a package inside the scientific ecosystem. It forfeits the four 3.13 constructs
above and therefore requires `typing_extensions` for `@deprecated`. Say this; do not silently prefer
one.

**Per-file application:**
- `python_platform_baseline_manifest.md` §3e — add the default, the rationale, the alternative and the
  forfeit list, immediately after the existing floor table. Keep the `OPEN` tag on the *policy*.
- `python_testing_tooling_manifest.md` — **delete** "so 3.11 is the defensible floor for new work".
  Replace with a pointer to hub §3e. This file does not own the policy.
- `error_tracing_contract_manifest.md` §21 — keep the behavioural argument, but reframe it as
  *supplying the behavioural case for* the hub's default, not as a competing recommendation.
- `python_module_boundaries_manifest.md` — the circular deferral is resolved; cite hub §3e's default.
- `python_linting_practices_manifest.md` — `target-version` MUST equal the floor: **`"py313"`**, with
  the comment that it tracks `requires-python`, never the newest release.

---

## D2. What the hub owns — CPython facts only

The hub owns **CPython** release dates, support phases, EOLs, PEP-status-by-version, build variants,
the removal calendar and the interpreter switchboard. It does **not** own third-party tool versions:
each file pins the tools that are its own subject matter and dates them. README's line "the only file
that owns dates" is too broad and becomes "the only file that owns **CPython** dates".

**Consequence:** strip restated CPython dates and support phases from every non-hub file, including the
places that cede ownership and then restate a date in the same breath. Replace with the fact plus a
pointer to hub §1a. Known sites: `python_testing_tooling_manifest.md:387`,
`python_quality_gates_manifest.md:1192-1194`, and any other occurrence you find while editing.

---

## D3. Ownership map for duplicated content — who cuts, who cites

The audit found full parallel treatments that will drift. In each case the **owner keeps the content**
and the **other file cuts to a one-or-two-sentence cross-reference** naming the owner and its section.
Do not delete the *obligation* — delete the *re-teaching*.

| content | OWNER (keeps it) | CUTS to a cross-reference |
|---|---|---|
| mypy `--strict` flag set; the opt-in error-code inventory | `python_typing_contract_manifest.md` §1 | `python_quality_gates_manifest.md` §5.1; `python_linting_practices_manifest.md` |
| coverage measurement semantics / "the arithmetic that makes thresholds lie" | `python_testing_tooling_manifest.md` §5a | `python_quality_gates_manifest.md` §6.1 — keep commands, exit codes, required config only |
| suppression rule-code table + per-checker mirror | `python_linting_practices_manifest.md` §8.2–§8.3 | `python_quality_gates_manifest.md` §4.5 — keep the budget formula and the two `--fix` hazards only |
| PEP 257 content + `lint.pydocstyle.convention` mechanism and its disable lists | `python_linting_practices_manifest.md` §6.3 | `python_quality_gates_manifest.md` §11.1 — keep the gate obligation only |
| the 18 removed ruff codes, the prefix distribution, the preview-selection trap, rule-family config | `python_linting_practices_manifest.md` | `python_language_hazards_manifest.md` §1.1 — keep only the routing fact that `E711`/`E712` are the identity-hazard route and that `select` replaces the default set |
| `-X dev` contents and the default warning filters | `python_platform_baseline_manifest.md` §6b–§6c | `python_runtime_diagnostics_manifest.md`; `python_module_boundaries_manifest.md` |
| the four-execution-model menu | `python_concurrency_determinism_manifest.md` | `architecture_manifest_default.md` stays agnostic — do NOT present the two menus as the same menu; the concurrency file must say how its four models relate to the agnostic paradigm menu without claiming identity |

---

## D4. The deprecation-visibility contract has FOUR parts, not three

Two files define a mandatory contract with the same absolutist framing and different members. The
canonical set is four:

1. **producer, runtime** — `@warnings.deprecated` (PEP 702) on the deprecated member;
2. **producer, test** — `-W error::DeprecationWarning` in the project's own suite, so the project sees
   its own deprecations;
3. **consumer, static** — the type checker reports use of a `@deprecated` member (mypy `deprecated`
   error code);
4. **consumer, test** — pytest `filterwarnings` promoting `DeprecationWarning` to error in the
   consumer's suite.

`python_module_boundaries_manifest.md` §9.3 renames its table to **"The four-part visibility contract"**
and adds the missing consumer-test row. `python_quality_gates_manifest.md` §8.4 replaces its three-part
list with a citation of that table plus the CI wiring only.

---

## D5. Two "silently ineffective" claims are FALSE — correct them everywhere

Both were established by the auditor **running ruff 0.16.2**, and both are currently asserted in
multiple files, some tagged ESTABLISHED or MEASURED. That combination — a confident tag on a false
claim — is the worst failure mode in the collection.

**D5a. Removed rule codes are LOUD, not silent.** `TRY200`, `PGH001`, `PGH002` are *redirects*: ruff
prints `has been remapped to …` **and enables the successor rule** (`B904`, `S307`, `G010`) — so the
config is not inert either. `PT004` was *fully removed* and ruff **refuses to run**
(`Rule PT004 was removed and cannot be selected`). Correct at
`python_linting_practices_manifest.md:282` and `python_language_hazards_manifest.md:862`, `:245`,
`:1045`.

**D5b. Preview-rule selection is silent only by PREFIX.** Selecting a preview rule by **exact code**
prints `Selection <X> has no effect because preview is not enabled.` — a warning, not a failure, so it
dies in CI log noise. Selection by **prefix** is genuinely silent. Correct at
`python_linting_practices_manifest.md:184` and `:1407`, and
`python_language_hazards_manifest.md:197-199`.

**D5c. The formatter-conflict guard rail exists but is partial and in the wrong subcommand.**
`ruff format` warns `The following rules may cause conflicts when used with the formatter: …` — but
only for `COM812` and `D203` of the fourteen documented conflicts, and only from the `format`
subcommand, not `check`. The blanket refutation at `python_linting_practices_manifest.md:464` is wrong
and overrode a fact pack that had the docs right. Correct it, and keep the real lesson: the guard rail
does not cover `W191`, `E111/E114/E117`, `D206`, `D300`, `Q000-Q004`, `COM819`, `ISC002`.

---

## D6. Missing house-template sections — add them

- `error_tracing_contract_manifest.md` and `logging_observability_manifest.md` have **no `## TL;DR`**.
  Add one to each: 4–6 bullets, each an actionable decision, each tagged. Place it immediately after
  the version-anchor line and the `---`.
- `python_testing_tooling_manifest.md` has **no anti-patterns / rejection list at all**. Add
  `## Anti-patterns checklist` immediately before `## Sources`, one line per entry, each naming the
  section it violates. The material is already in the file and needs only inverting.

---

## D7. Tag-legend completeness

`MEASURED` and `UNVERIFIED` are both in active use across the ground-truth files but appear in no tag
legend. Either rename them to an existing tag or add them to the legend of every file that uses them —
**add them**, since both carry real meaning:
- **MEASURED** — established by running the tool in this environment, not by reading its docs. Strictly
  stronger than ESTABLISHED for tool behaviour, and it must name the tool version.
- **UNVERIFIED** — asserted by a source but not confirmed against a primary page this pass.

Add both to `README.md`'s tag table too, and note there that MEASURED claims are pinned to the measured
tool version.

---

## D8. Standing rules for this round

1. **Add no new unverified identifiers.** If a rule code, flag or API name is not in your findings file,
   not in `_work/facts/`, and not on a page you load yourself, do not write it. Where the audit says a
   default status was never measured, write `[?]` plus the exact verification command.
2. **Do not renumber sections.** Where a cross-reference points at a section that does not exist (e.g.
   the `§10d`–`§10h` references in `python_runtime_diagnostics_manifest.md`), **repoint the reference at
   the section that now carries the content** rather than inventing new headings.
3. **Preserve each file's register and wrapping.** Match the paragraph you are editing. Do not reflow
   surrounding text.
4. **Edit only your assigned file(s).** Do not touch `_work/PLAN.md`, `_work/RESUME_STATE.md`, or any
   file assigned to another fixer.
5. **Where a finding is wrong, say so instead of applying it.** The auditors were adversarial, not
   infallible. If you verify a prescription against a primary source and it fails, do not apply it —
   record the refutation in your receipt with the source. That is a valid and valuable outcome.
