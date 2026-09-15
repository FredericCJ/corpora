# Python manifest set — update & augmentation endeavour — RESUME STATE

**What:** re-verified the Python manifest set against live primary sources and augmented it from the
`SWE/` research corpus, giving each of the five mission pillars (testable, diagnosable, maintainable,
modular, incrementally buildable) an owning manifest, and giving the collection the **version hub** and
**enforcement ladder** it previously lacked. Executed 2026-08-08 under Opus 5 (ultrathink + ultracode)
per `_work/PLAN.md`. **Nothing committed — the user's call (standing rule).**

## Final numbers

- **17 files · 1,715,457 bytes · 17,221 lines** (was 9 files / ~260 KB).
- **2,294 tagged claims**: 874 ESTABLISHED · 656 VERSION-DEPENDENT · 490 OPEN · 92 MEASURED ·
  69 FLAGGED-SECONDARY · 65 UNVERIFIED · 48 CC-FACT. **644 unique source URLs**, all stamped
  `Accessed 8 Aug 2026`.
- Agents: **18 research scouts + 12 authors + 6 auditors + 9 fixers = 45**. Research produced **1.28 MB**
  of fact packs (`_work/facts/r01–r14`) and **235 KB** of corpus-mining packs (`_work/seed/s1–s4`).
- The audit checked **946 claims** and found **66 defects** (7 CRITICAL / 28 MAJOR / 31 MINOR); all 66
  were dispositioned, with **103 claims verified by running the tool** and **24 audit prescriptions
  refuted or corrected with a primary source**. See `AUDIT.md`.

## Repackaged for agent consumption (2026-08-08, second pass)

After the augmentation endeavour completed, the flat 17-file set was **reorganised into a
redistributable, progressively-disclosed package** — same content, shape an agent can actually use.
The 16 manifests moved to **`reference/`** (co-located, so their bare-filename cross-references still
resolve); everything else is new scaffolding around them.

```
AGENTS.md      entry point: 20 non-negotiables, tag protocol, task router     (~2.8k tokens)
INDEX.json     647 reference sections, machine-queryable (jq/grep, never read)
cards/         11 task cards - the layer agents read                          (~1.4-1.9k tokens each)
config/        6 copy-in artefacts (pyproject, import contracts, check.sh, hooks, CI)
reference/     the 16 ground-truth manifests, unchanged                       (~425k tokens)
adapters/      wiring for Claude Code (skill), Cursor, Copilot, custom loops
_work/         this provenance trail
```

**The number that justifies the shape:** entry + the largest card = **4,688 tokens = 1.10%** of the
425k-token reference corpus. Previously the minimum useful unit was one 24-46k-token file, and the set
as a whole was unusable as context.

Verified during repackaging: the `[tool.ruff]` block in `config/pyproject.toml` is **byte-identical**
(`diff`, 57 lines) to `reference/python_linting_practices_manifest.md` §4.3 — the only measured artefact
in `config/`, and the one most likely to be corrupted by paraphrase. All internal filename references
resolve; all 50 sampled `§` cross-references from cards into reference sections resolve (one broken
pointer, `observability §6a`, was found and repointed to §8c/§8b). `check.sh` passes `sh -n`;
`INDEX.json` parses.

**Cards are pointers plus rules, never summaries.** The evidence, citations and epistemic tags stay in
`reference/`; collapsing them into the cards would have destroyed the provenance that makes the package
worth trusting. Config artefacts are copied verbatim, never re-derived — an earlier draft's invented
`D216` is exactly what re-derivation produces.

## File spine now

| file | lines | status |
|---|---|---|
| `README.md` | 194 | **NEW** — collection entry point, pillar table, reading order, epistemic protocol |
| `python_platform_baseline_manifest.md` | 1256 | **NEW** — the version hub; owns **CPython** dates (tool versions stay with the file whose subject they are) |
| `python_language_hazards_manifest.md` | 1367 | **NEW** — 13 hazard classes, 170 routing rows, 172 verified rule codes |
| `python_linting_practices_manifest.md` | 1886 | **NEW** — rule set as committed artefact + practice/anti-pattern catalogue |
| `python_module_boundaries_manifest.md` | 1677 | **NEW** — layout, packaging, imports as contract, enforced dependency direction |
| `python_runtime_diagnostics_manifest.md` | 1528 | **NEW** — attach, dumps, memory, profiling, design-for-diagnosis |
| `python_concurrency_determinism_manifest.md` | 1698 | **NEW** — four execution models + determinism under test |
| `python_quality_gates_manifest.md` | 2328 | **NEW** — gate ledger, ratchet, supply chain, measurement with honest evidence |
| `python_typing_contract_manifest.md` | 529 | updated 35→180 KB |
| `python_testing_tooling_manifest.md` | 594 | updated 29→152 KB |
| `error_tracing_contract_manifest.md` | 622 | updated 31→141 KB |
| `logging_observability_manifest.md` | 1493 | updated 33→119 KB |
| `architecture_manifest_default.md` | 695 | augmented 17→33 KB, **reasoning register preserved** |
| `software_spec_discipline_manifest.md` | 177 | sibling list extended to all 11 Python files |
| `spec_recovery_reverse_engineering_manifest.md` | 478 | untouched (byte-identical) |
| `uml25_ocl_conformance_manifest.md` | 269 | untouched (byte-identical) |
| `claude_code_agent_teams_manifest.md` | 430 | untouched (byte-identical) |

## The two structural additions that reshape the set

1. **A version hub.** Previously every file carried its own drifting version-anchor paragraph. Now
   `python_platform_baseline_manifest.md` owns all release dates, support phases, EOLs, PEP-status-by-
   version, build variants and the `-X`/`PYTHON*` switchboard. Every sibling states *behaviour* plus an
   inline gate and says explicitly: **if a version fact here disagrees with the hub, the hub wins and
   this file is stale.** The sibling collection `../web_manifests/` already had this shape; the Python
   set did not.
2. **The enforcement ladder**, inherited from the `js/` and `jsts/` prompt programs:
   `hazards` (diagnose) → `typing` (type) → `linting_practices` (lint + practise) →
   `quality_gates` (enforce + measure). Every hazard and practice carries one of **seven** enforcement
   routes: type-catchable / lint-catchable / feature-eliminated / test-catchable / fitness-function /
   runtime-catchable / **contract-only**. An unrouted practice is treated as a defect. The canonical
   route table is `python_language_hazards_manifest.md` §0.1; §0.2 defines the `[on]`/`[off]`/`[?]`
   default-status markers written beside every rule code.

## Load-bearing facts established this pass

- **CPython 3.14.7 (2026-08-05)** is latest stable; **3.15 is at rc1 (2026-08-04)** per PEP 790, final
  due 2026-10-01, ABI-frozen from rc1; **3.16 has no artefact of any kind** — PEP 826 puts alpha 1 at
  2026-10-13 and final at 2027-10-05, and `main` is 3.16, the only branch accepting features.
  **3.10 reaches EOL ~2026-10**, retiring the lowest leg of most CI matrices.
  **PEP 2026 (CalVer) is REJECTED** — there is no "Python 3.26".
- **3.15 ships** PEP 686 (UTF-8 default), PEP 810 (lazy imports), PEP 661 (`sentinel()` builtin),
  PEP 728 (`TypedDict` `closed=`/`extra_items=`), PEP 747 (`TypeForm`), PEP 800 (`disjoint_base`), and
  PEP 799 — a **new stdlib sampling profiler** (`profiling.sampling`, "Tachyon", up to 1 MHz), with
  `cProfile` demoted to an alias and `profile` deprecated for removal in 3.17.
- **ruff 0.16.0 (2026-07-23) raised its default rule set from 59 to 413 and silently dropped 18 codes**
  without recording it in `BREAKING_CHANGES.md`. Two of the dropped codes are **E711 (`== None`)** and
  **E712 (`== True`)** — the version bump switched off the enforcement route for the identity hazard.
  This is the collection's central lesson: **an implicit default set is not a standard.** Pinned at
  ruff 0.16.2 (2026-08-07).
- **Four checkers now exist**, not two: mypy 2.3.0, pyright 1.1.411, pyrefly 1.2.0, **ty 0.0.69** —
  reported at the maturity each project itself claims, not oversold.
- **PEP 768** (Final, 3.14): `sys.remote_exec(pid, script)` + `python -m pdb -p PID`; disabled by
  `PYTHON_DISABLE_REMOTE_DEBUG` **on any value including empty**, `-X disable-remote-debug`, or
  `--without-remote-debug`. Disabling it silently breaks `pdb -p` and `profiling.sampling attach`.
- **pytest 9.0.0–9.0.3 silently ignored `--strict-markers`/`--strict-config` from `addopts`**; pytest 9
  added a native `[tool.pytest]` TOML table that **cannot coexist** with `[tool.pytest.ini_options]`.
- **PEP 751** (Final): the lock file is `pylock.toml`; the canonical spec now lives on the PyPA specs
  page, not in the PEP.

## Discipline that was actually held

- Authors **rejected** pack suggestions with stated reasons rather than absorbing them (the hub author
  rejected 8, including its own `cp313t` slip and a `tomli` claim no pack had verified).
- A research scout **caught itself inventing** a RUF rule name whose page 404'd and quarantined the
  whole family rather than shipping it; the hazards author kept it out and said so in §1.4.
- Two primary-source **conflicts were recorded rather than smoothed**: 3.16.0-final differs by one day
  between devguide and PEP 826; free-threading single-thread overhead is quoted as both "5–10%" (3.14
  What's New) and ~1%/~8% (free-threading HOWTO), so a bare percentage is forbidden.
- A source conflict was resolved **by measurement over prose**: ruff's FAQ implies DTZ is off by
  default; measuring resolved settings on 0.16.2 shows all ten DTZ rules inside the 413. The
  generalised rule is now in the file: verify default status by measuring, never by reading prose.
- ~40 rule codes carry `[?]` ("default status not verified — check with this command") rather than an
  implied status. `[on]`/`[off]` were only asserted where measured.

## What the audit changed (see `AUDIT.md` for the full record)

The audit was the phase that earned its keep. It found a **fabricated rule code** (`D216`) that makes
ruff abort, a rule wrongly listed as enabled-by-default in a table headed "do not lose" (`LOG004`), and
**three mutually contradictory answers** to the single most consequential line in a new
`pyproject.toml`. All three classes are invisible to an author re-reading their own work.

Resolved as collection-wide decisions in `fixes/DECISIONS.md`, now applied:

- **One floor.** Hub §3e states a recommended default — `requires-python = ">=3.13"` — with its
  behavioural and calendar rationale, the SPEC 0-aligned alternative (`">=3.12"`) and exactly what that
  forfeits. The policy stays `OPEN`; the reader is no longer stranded. `target-version = "py313"` now
  tracks it, and three files that used to give their own answers cite §3e.
- **Ownership enforced.** Six duplicated treatments (the mypy `--strict` inventory, coverage arithmetic,
  the suppression tables, the pydocstyle mechanism, the removed-code list, the `-X dev` inventory) were
  cut to cross-references naming the owner. The collection now states each rule once.
- **Three false "silently ineffective" claims corrected.** Removed rule codes are *loud* — redirects
  warn and enable the successor, fully-removed codes make ruff refuse to run. Preview selection warns by
  exact code and is silent only by *prefix*. The formatter guard rail exists but only in `ruff format`
  and only for 2 of 15 documented conflicts. All three had been tagged `ESTABLISHED`/`MEASURED`.
- **Two misattributed quotations fixed** — the corpus's own editorial glosses had been quoted as
  ISO 26262's and Kuhn et al.'s words.
- **Every ground-truth file now carries all four required sections** (TL;DR, anti-patterns, Sources,
  Sibling manifests). Previously three were missing one or more.
- **The recommended `[tool.ruff]` block was run as a real `pyproject.toml`**: loads clean, resolves to
  708 rules, and no default-on code is left unaccounted for.

## Known limitations, stated plainly

- **Size is the real cost of this pass.** Files run 97–183 KB (≈24k–46k tokens). The set cannot be handed
  to an agent wholesale; `README.md`'s per-task reading order is the mitigation. A compact one-page
  operating card was deliberately **not** written — trimming or re-shaping verified content is the
  owner's call, not the author's.
- **Print sources were never checked against the books.** BCK *SAIP*, Meszaros, POSA 2/4, Feathers, JCiP,
  Douglass, Evans, Bloch, Kerrisk and Kuhn et al. are not online. Element attributions were verified
  against the SWE corpus's own `named_in`/`works` records, so a systematic error *inside* the corpus
  would pass invisibly — which is exactly the class the `feature-toggle`/`feature-flag` misattribution
  belonged to. Treat corpus attributions as corpus-accurate, not book-verified.
- **Two errors remain in `facts/r01_platform_baseline.md`** (`ALLOW_MISSING` mis-filed under 3.15; an
  unsourced bugfix count). Fact packs are dated evidence snapshots and were deliberately not edited; the
  corrections live in the hub and in `AUDIT.md`.
- **Wrap discipline — measured correctly this time.** All seven new files are at **zero** lines over 100
  characters. `python_testing_tooling_manifest.md` (289) and `python_typing_contract_manifest.md` (240)
  retain their original one-paragraph-per-line format by design, because reflowing them would have
  destroyed the diff. An earlier draft of this file claimed "6–115 violations in the new files"; that was
  an artefact of measuring with `awk`, which counts **bytes** — every em dash and `§` in these files is
  three bytes and one character. Recorded because the same mistake will otherwise be made again.

## Re-verification triggers (from hub §8)

Three fire within ten weeks of 2026-08-08 and invalidate the hub's TL;DR and §1–§3:
**3.15.0 final (2026-10-01)** · **3.10 EOL and the final 3.13 bugfix (~2026-10)** ·
**3.16 alpha 1 (2026-10-13)**. Also re-verify on any ruff / mypy / pyright / pytest bump — the rule-code
and strictness tables are pinned to this session's pages, several of which carry no version stamp.

## How to resume

- `_work/PLAN.md` — scope boundaries per file, the 11 house rules, the two-register discipline.
- `_work/facts/r01–r14_*.md` — the verified fact packs, each with its own Sources section.
- `_work/seed/s1–s4_*.md` — SWE corpus mining, with import / fold / do-not-transpose adjudication.
- Audit findings and their disposition are recorded in `_work/AUDIT.md`.
