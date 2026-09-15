# Audit findings for `python_concurrency_determinism_manifest.md`

3 findings: MINOR 3

Each finding was produced by an adversarial auditor that verified the claim against a
primary source or by running the tool itself. Line numbers were correct at audit time and
will shift as you edit - locate by the quoted text, not the number.

---

## 1. [MINOR] around line 460

**Quoted text being challenged:**

> VERSION-DEPENDENT (anyio 4.14.2, trio 0.33.0); the hub owns the version/date facts.

**What is actually true:**

The hub contains zero occurrences of "anyio" or "trio" (grep -c over python_platform_baseline_manifest.md returns 0), and PLAN.md scopes it to "only version/support/schedule/PEP-status facts, interpreter switches, build variants, and the minimum-target policy" — i.e. CPython. Every other file states the opposite convention for third-party pins: python_testing_tooling_manifest.md:3 ("The tool versions below ... are this file's own subject matter"), python_linting_practices_manifest.md:35 ("This file owns its tool pins"), python_quality_gates_manifest.md:31 ("Tool versions are this file's own subject"). A reader following this route to the hub finds nothing.

**Source the auditor checked:**

python_platform_baseline_manifest.md (no anyio/trio occurrences; sibling block at :1107-1134 scopes the file to "version, support, schedule, PEP-status, build-variant and interpreter-switch facts"); python_linting_practices_manifest.md:35; python_quality_gates_manifest.md:31

**Prescribed fix:**

Replace "the hub owns the version/date facts" with "these third-party pins are this file's own subject and were verified 2026-08-08; the hub owns only CPython version facts." Add anyio/trio (and pytest-trio if used) to this file's own Version-anchor block the way the other files pin theirs.

---

## 2. [MINOR] around line 57

**Quoted text being challenged:**

> - **Determinism is bought at four seams — clock, seed, executor, event loop — and nowhere else.**

**What is actually true:**

"and nowhere else" is an absolute claim contradicted by the file the collection designates the owner of test determinism. python_testing_tooling_manifest.md §6c (line 280) names "Four sources of nondeterminism", of which two — **order** (inter-test coupling, closed by `pytest-randomly` 4.1.0, where "reordering *is* the detector") and **network** (real sockets, closed by `respx`/`responses` plus `pytest-socket`) — are not among concurrency's four seams and are not reachable from them. Concurrency's own version anchor (lines 20-21) already routes "general test determinism (clock, seed, snapshot, fixtures)" to the testing file, so the absolutism is unnecessary as well as wrong.

**Source the auditor checked:**

python_testing_tooling_manifest.md:280-284 (§6c four-source table); python_concurrency_determinism_manifest.md:20-21 (its own deferral)

**Prescribed fix:**

Change to "**Concurrency determinism is bought at four seams — clock, seed, executor, event loop.** Test-order and network nondeterminism are separate obligations owned by `python_testing_tooling_manifest.md` §6c." Drop "and nowhere else".

---

## 3. [MINOR] around line 133

**Quoted text being challenged:**

> **VERSION-DEPENDENT (3.14).** CPython offers exactly four concurrency substrates in the standard library

**What is actually true:**

The collection now has two different four-item menus, both introduced as "choose the model before the primitives", and cross-references one to the other without reconciling them. architecture_manifest_default.md §3.4 (lines 223-232) opens "Choose a concurrency model before choosing primitives" and lists shared-memory-with-locks / message-passing / single-threaded event loop / parallel pure transformations. python_concurrency_determinism_manifest.md §1 is titled "The execution model is chosen before any primitive" and §2.1 lists asyncio / threads / subinterpreters / processes. These are orthogonal taxonomies (arch's is a state-sharing paradigm menu, concurrency's a CPython substrate menu) — "message-passing" maps onto three of concurrency's four substrates and "shared-memory locks" onto one — yet concurrency:26 names architecture §3.4 as "the model-choice reasoning frame", inviting exactly the conflation.

**Source the auditor checked:**

architecture_manifest_default.md:221-232 (§3.4); python_concurrency_determinism_manifest.md:26, :62, :131-137

**Prescribed fix:**

Add one sentence at the head of concurrency §2.1: "These four are CPython **substrates**. They are not the same list as the four state-sharing **paradigms** in `architecture_manifest_default.md` §3.4 (shared-memory, message-passing, event loop, parallel pure transformation) — the paradigm is chosen first, and it usually admits more than one substrate." Then use "substrate" consistently in concurrency and "paradigm" whenever citing arch §3.4.

---
