# Audit findings for `error_tracing_contract_manifest.md`

5 findings: MAJOR 3, MINOR 2

Each finding was produced by an adversarial auditor that verified the claim against a
primary source or by running the tool itself. Line numbers were correct at audit time and
will shift as you edit - locate by the quoted text, not the number.

---

## 1. [MAJOR] around line 133

**Quoted text being challenged:**

> *"a predefined operating condition without unreasonable risk that the system deliberately enters on fault detection"*

**What is actually true:**

This quoted string is the SWE corpus's own editorial `what` field for the `safe-state` element, not wording from ISO 26262 — yet the row's source column reads "ISO 26262:2018; Bass, Clements & Kazman ...", so the quotation marks put the corpus compilers' summary in a standards body's mouth. elements.json `safe-state`.what = "A predefined operating condition without unreasonable risk that the system deliberately enters on fault detection (outputs de-energized, actuators parked, subsystem disabled)." ISO 26262-1:2018 (Vocabulary) actually defines safe state as "operating mode, in case of a failure of an item, without an unreasonable level of risk" — different wording, and it is scoped explicitly to the failure case. The corpus records this text as its own gloss (there is no quotation provenance on the field), so no quotation from ISO is licensed here.

**Source the auditor checked:**

E:/dev/corpora/SWE/explorer/data/elements.json (node `safe-state`, field `what`, named_in "ISO 26262:2018 - Road vehicles - Functional safety"); ISO 26262-1:2018(en) Vocabulary — https://www.iso.org/obp/ui/en/#!iso:std:68383:en

**Prescribed fix:**

Drop the quotation marks and attribute the gloss, e.g.: "the corpus's gloss — a predefined operating condition without unreasonable risk that the system deliberately enters on fault detection — refuse to start on bad config with a **distinct exit code**, ...". If a quotation from the standard is wanted, quote ISO 26262-1:2018's actual definition: "operating mode, in case of a failure of an item, without an unreasonable level of risk".

---

## 2. [MAJOR] around line 90

**Quoted text being challenged:**

> **Why the core is where irreplaceable state lives (Error Kernel, Kuhn et al. 2017).** The failure-side argument for the seam: *"keep the irreplaceable state … in a small, maximally simple core, delegating risky or failure-prone work to expendable child components."*

**What is actually true:**

The italic quotation is the SWE corpus's editorial `what` field for `error-kernel`, not text from Kuhn, Hanafee & Allen's *Reactive Design Patterns*. elements.json `error-kernel`.what = "Keep the irreplaceable state and critical logic in a small, maximally simple core, delegating risky or failure-prone work to expendable child components that can crash and be restarted." Placing it in quotation marks immediately after "(Error Kernel, Kuhn et al. 2017)" reads as quoting the book. The same pattern recurs in this file: line 201 quotes *"Full result verification is often infeasible, but gross faults are cheap to catch."* under "(naming work: Douglass, *Real-Time Design Patterns*)" — that string is `sanity-check`.problem; and line 102 quotes *"Report failure immediately, rather than doing work that is doomed to fail slowly."* under "(naming work: Nygard, *Release It!*)" — that is a re-capitalised fragment of `fail-fast`.what ("Check preconditions and resource availability up front and report failure immediately, ..."), so it is not even verbatim against the corpus field it came from. Sibling files frame identical material correctly: python_testing_tooling_manifest.md:108 writes "the catalog's justification is that external APIs are 'awkward, unstable, and hard to fake'" and python_concurrency_determinism_manifest.md:740 writes "problem is 'unbounded queues hide overload until memory or latency blows up'". I machine-matched 45 places where manifest quotations reproduce corpus `what`/`problem` fields; the four in this file are the ones whose framing attributes them to a named primary source.

**Source the auditor checked:**

E:/dev/corpora/SWE/explorer/data/elements.json (nodes `error-kernel`, `sanity-check`, `fail-fast` — fields `what`/`problem`, which carry no quotation provenance); contrast framing at python_testing_tooling_manifest.md:108 and python_concurrency_determinism_manifest.md:740

**Prescribed fix:**

Attribute the gloss to the corpus rather than the author in all four places. At line 90: "**Why the core is where irreplaceable state lives (Error Kernel, Kuhn et al. 2017).** The failure-side argument for the seam, in the corpus's wording: keep the irreplaceable state and critical logic in a small, maximally simple core, delegating risky or failure-prone work to expendable child components that can crash and be restarted." Apply the same de-quoting at lines 102, 133 and 201 (or prefix each with "the corpus element's summary:").

---

## 3. [MAJOR] around line 199

**Quoted text being challenged:**

> - **FOR:** internal **can't-happen invariants** and **pre/post-conditions** — programmer-believed facts whose violation means a **bug**, not bad input (e.g. "this list is non-empty here", a postcondition on a pure function).

**What is actually true:**

Three files endorse `assert` for production internal invariants — this line, and python_quality_gates_manifest.md §8.6 ("**Executable Assertions**: `assert` is for internal invariants") — while python_linting_practices_manifest.md line 1338 states "**exactly why `S101` must be enforced in `src` and exempted only in the test tree**", §4.2 line 328 says "a global `ignore` re-permits assert-as-validation in production", the anti-patterns list rejects "**A global `ignore = [\"S101\"]`**", and the §4.3 `per-file-ignores` exempts S101 for `tests/**` only. So an agent that writes the endorsed can't-happen assert in src/ hits a REQUIRED pre-commit gate (ledger row 2) with no sanctioned escape: global ignore is rejected, per-file-ignores is for tests, and neither file mentions a per-site `# noqa: S101` with a reason. error_tracing §14 also contradicts itself: the audit checklist in the same section says "Search for and **re-express**: (1) bare `assert` outside tests", which rejects what the FOR bullet endorses.

**Source the auditor checked:**

Internal cross-check: error_tracing_contract_manifest.md line 199 vs line 203 (the audit) ; python_linting_practices_manifest.md lines 328, 1338, and the S101 anti-pattern at ~1429 ; python_quality_gates_manifest.md §8.6 Executable Assertions paragraph

**Prescribed fix:**

Add one sentence to error_tracing §14 after the FOR bullet: "**The lint consequence:** `S101` is enforced in `src` (`python_linting_practices_manifest.md` §4.2), so a legitimate internal-invariant assert in production code carries a per-site `# noqa: S101  # internal invariant, §14` — never a global `ignore` and never a `per-file-ignores` entry outside `tests/**`." Mirror that permitted escape in python_linting_practices_manifest.md §4.2 row for S101, and delete or requalify item (1) of the §14 audit checklist so it reads "bare `assert` used as a boundary/auth/resource check" rather than "outside tests".

---

## 4. [MINOR] around line 201

**Quoted text being challenged:**

> files `executable-assertions` under BCK's `control-and-observe-system-state` — i.e. as

**What is actually true:**

`control-and-observe-system-state` is not an element id — it is a corpus *tag*, and its actual spelling is `bck-cat:control-and-observe-system-state` (elements.json `executable-assertions`.tags = ['bck-cat:control-and-observe-system-state', 'same-name:design-realm']). Because this collection uses bare backticked kebab-case for element ids throughout, dropping the `bck-cat:` namespace makes it read as an element id that does not exist. The sibling files get this right: python_runtime_diagnostics_manifest.md:1003 writes "category `bck-cat:control-and-observe-system-state`", as do _work/seed/s2_errors_diagnosability.md:381 and :425.

**Source the auditor checked:**

E:/dev/corpora/SWE/explorer/data/elements.json (node `executable-assertions`, field `tags`); consistent spelling at python_runtime_diagnostics_manifest.md:1003 and _work/seed/s2_errors_diagnosability.md:381

**Prescribed fix:**

Write the namespaced tag: "files `executable-assertions` under BCK's category `bck-cat:control-and-observe-system-state` — i.e. as"

---

## 5. [MINOR] around line 11

**Quoted text being challenged:**

> ## 1. Purpose and scope

**What is actually true:**

Neither error_tracing_contract_manifest.md nor logging_observability_manifest.md carries a TL;DR block (`grep -in 'TL;DR|TLDR|at a glance|the short version'` returns zero hits in both). The other nine ground-truth files all open with one: python_platform_baseline L26, python_typing_contract, python_language_hazards L55, python_linting_practices, python_testing_tooling L5, python_runtime_diagnostics, python_module_boundaries L27, python_quality_gates, python_concurrency_determinism. Both files jump from the Purpose/version-anchor header straight into numbered sections. Note this is a collection-consistency gap rather than a PLAN violation — PLAN.md's ground-truth register spec mandates the Purpose/Scope opening, tag legend, anti-patterns, open questions and sources but does not name a TL;DR.

**Source the auditor checked:**

E:/dev/corpora/manifests/error_tracing_contract_manifest.md and logging_observability_manifest.md (grep -n '^#\{2,3\} ' on both; grep -in 'TL;DR' on both → 0)

**Prescribed fix:**

Add a `## TL;DR` block to each, immediately after the version-anchor/deferral header and before the first numbered section — error_tracing after L9 (before `## 1. Purpose and scope`), logging after L26 (before `## 1. Scope and the three goals`). Each bullet should end in its tag and its section, matching the nine siblings' form. The material already exists: error_tracing's can be distilled from §2–§3 (no checked exceptions; typed in-band for contract outcomes, raise for exceptional ones; two channels, three dispositions), §7a–§7b (transient-fault and disposition mechanisms named then gated), §14 (`assert` is stripped by `-O`), §18 (`ExceptionGroup`/`except*`); logging's from §2 (five emittable levels; NOTSET is a sentinel, not a sixth), §4 (library authors add a `NullHandler` and configure nothing), §7a (there is no stdlib JSON formatter), §9 (lazy `%`-args and `isEnabledFor`), §10 (log once at the handling boundary), §11a (redact at the Logger, never the Formatter).

---
