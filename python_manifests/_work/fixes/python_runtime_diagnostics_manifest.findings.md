# Audit findings for `python_runtime_diagnostics_manifest.md`

4 findings: MAJOR 1, MINOR 3

Each finding was produced by an adversarial auditor that verified the claim against a
primary source or by running the tool itself. Line numbers were correct at audit time and
will shift as you edit - locate by the quoted text, not the number.

---

## 1. [MAJOR] around line 1205

**Quoted text being challenged:**

> - **A hand-rolled supervision tree, retry budget, dead-letter queue, or health-check HTTP port in a\n  single-process app** — the restarter is systemd or the orchestrator, and the rest is\n  distributed-systems machinery at the wrong scale (§10e, §10c, §10h).

**What is actually true:**

§10 of this file contains only three subsections: `### 10a.` (L998), `### 10b.` (L1017) and `### 10c.` (L1034). There is no §10d, §10e, §10f, §10g or §10h anywhere in the file — not as a heading and not as a bolded numbered sub-block (unlike python_module_boundaries_manifest.md §5, whose 5.1–5.6 exist as bolded blocks and do resolve). Fourteen references to those five non-existent ids appear on 12 lines: L94 (×2, §10d), L95 (§10h), L364 (§10e), L369 (§10f), L756 (§10d), L1082 (§10h), L1111 (§10h), L1205 (§10e, §10h), L1207 (§10f), L1209 (§10g), L1243 (§10h), L1490 (§10h). The content they point at was evidently folded into §10b's nine-row mechanism table (`sanity-check`/`correcting-audits` = the §10d target, `watchdog` = §10e, `safe-state` = §10f, `software-rejuvenation` = §10g, `record-playback` = §10h) without the pointers being updated. Three of the broken pointers sit in the anti-patterns checklist, which PLAN.md house rule 8 requires to be 'a rejection list, one line each, each pointing at the section it violates. This is the part agents actually obey.' Two more sit in the TL;DR symptom→instrument routing table at L94–L95, i.e. the file's front door.

**Source the auditor checked:**

E:/dev/corpora/manifests/python_runtime_diagnostics_manifest.md (grep -n '^#\{2,4\} 10' → only 990/998/1017/1034; grep -n '§10[d-h]' → 12 lines); E:/dev/corpora/manifests/_work/PLAN.md house rule 8

**Prescribed fix:**

Repoint all fourteen references at the row that now carries the content, or restore the sub-numbering. Concretely: §10d → §10b (`sanity-check` and `correcting-audits` rows); §10e → §10b (`watchdog` row); §10f → §10b (`safe-state` row); §10g → §10b (`software-rejuvenation` row); §10h → §10b (`record-playback` row). For L1205 write `(§10b, §10c)`; for L1207 write `(§10b)`; for L1209 write `(§10b)`; for L94 write `(§10b)` in both cells; for L95, L1082, L1111, L1243, L1490 write `§10b`. Alternatively promote the five §10b rows that are referenced back into `### 10d.`–`### 10h.` subsections.

---

## 2. [MINOR] around line 750

**Quoted text being challenged:**

> **ESTABLISHED — the four non-effects, each a live agent error.** `-X dev` does **not** enable `tracemalloc`

**What is actually true:**

The hub, which owns the interpreter-switch inventory, titles the same fact "### 6b. What `-X dev` does — and **the two things it does not**" (python_platform_baseline_manifest.md:614) and lists exactly two non-effects (no tracemalloc; no protection of `assert` from `-O`). runtime_diagnostics lists four (adding: does not enable `-X importtime`/`-X showrefcount`; does not turn warnings into errors). The two files also tag the identical fact differently — hub ESTABLISHED, runtime_diagnostics "VERSION-DEPENDENT (3.7+)" — and both enumerate the seven enables in full, despite runtime_diagnostics' own scope block at lines 24-26 ceding "interpreter-switch-inventory ... facts" to the hub. A reader who checks the hub, the file the collection designates authoritative on switches, gets a two-item list presented as complete.

**Source the auditor checked:**

python_platform_baseline_manifest.md:614-633 (§6b); python_runtime_diagnostics_manifest.md:24-26 (its own scope boundary) and :739-761 (§7a)

**Prescribed fix:**

Make hub §6b the single enumeration: retitle it "and the four things it does not", add the `-X importtime`/`-X showrefcount` and warnings-are-not-errors items, keep ESTABLISHED. Then cut runtime_diagnostics §7a's seven-enables and four-non-effects lists to "The exact effect list is owned by `python_platform_baseline_manifest.md` §6b", keeping only the diagnostics-specific residue (startup-only, read back via `sys.flags.dev_mode`, why it belongs in the failure report §11b).

---

## 3. [MINOR] around line 466

**Quoted text being challenged:**

> A process that wants every failure recorded must install all four hooks plus the loop handler.

**What is actually true:**

Four hooks plus the loop handler is five, but the section's own table (lines 470-474) has exactly four rows and the loop handler is one of them. The owning file counts it the same way: error_tracing_contract_manifest.md:351 says "There are **four** separate last-resort channels plus one library that has none", and its four hook rows are `sys.excepthook`, `threading.excepthook`, `sys.unraisablehook` and `loop.set_exception_handler` (the fifth row is `concurrent.futures`, which has no hook at all). So this prose over-counts by one against its own table and against the owner's canonical count, and an agent writing `install_error_hooks()` from it hunts for a fifth hook that does not exist.

**Source the auditor checked:**

error_tracing_contract_manifest.md:349-361 (§20a, the owning section); python_runtime_diagnostics_manifest.md:470-474 (its own four-row table)

**Prescribed fix:**

Change to "must install all four channels — the three hooks plus the asyncio loop handler — and additionally retrieve `concurrent.futures` results by hand, because that library ships no hook at all (`error_tracing_contract_manifest.md` §20a)."

---

## 4. [MINOR] around line 411

**Quoted text being challenged:**

> | d | `gdb -p PID` then `thread apply all py-bt` | gdb 7.0+ with Python support, plus debug info | The only answer when the target is blocked below Python entirely (§4e) |

**What is actually true:**

In the §4d "nothing pre-installed" ladder, rows (a) and (f) carry version preconditions and row (e) is marked POSIX, but row (d) carries no platform note although `gdb -p` against CPython is not a Windows path. The file is otherwise scrupulous about this gap — line 373-374 says "The `SIGUSR1`-dumps-a-stack runbook is POSIX-only and needs a documented Windows alternative (§4d) before it goes into a cross-platform runbook", and its Open questions (line 1232) carry "Include the Windows answer, since `faulthandler.register` does not exist there." That honest flagging is correct behaviour; row (d) is the one unflagged residue, and it leaves a Windows-hosted incident with exactly one usable instrument in the ladder (row b, py-spy) without saying so.

**Source the auditor checked:**

Internal: python_runtime_diagnostics_manifest.md lines 373-374, 405-413, 423, 1232. Confirmed the file's own platform notes at line 1305 ("`register`/`unregister` unavailable on Windows")

**Prescribed fix:**

Add to the Requires cell of row (d) at line 411: `gdb 7.0+ with Python support, plus debug info — **POSIX only**`, and add one line under the table: "**On Windows the ladder is (b) py-spy only** until the §Open-questions Windows answer is recorded; WER (§4e) covers the crash case, not the wedge case."

---
