# scheduler_prompt — a prompt system for real-time fixed-priority scheduling models

A reusable prompt system that makes Claude answer **iterative real-time scheduling modeling** questions
— *"propose a simulatable static fixed-priority preemptive scheduler; now augment it with a
priority-inversion protocol; now add interrupt routines; now …"* — with domain-correct theory and a
**runnable simulator** at every step. Grounded in the real-time scheduling keystones this corpus curates
(Liu & Layland, Buttazzo, Sha/Rajkumar/Lehoczky, response-time analysis, TrueTime, SimEvents).

## Files
- **`system_prompt.md`** — the system prompt: role, five-section deliverable contract (Model · Simulator
  · Demonstration · Analysis · Limits), the iteration protocol (each request is a minimal *delta*), the
  correctness rules, and grounding. **The main artifact.**
- **`reference_card.md`** — the grounded facts it applies: task model, priority scale, response-time
  analysis, utilization bound, priority-inversion protocols (basic inheritance / immediate ceiling),
  interrupt/ISR interference — each with a citation to the corpus keystones.
- **`simulator_skeleton.py`** — a deterministic, **verified** fixed-priority preemptive simulator (1-µs
  tick, single core) the model extends each iteration. Reproduces the response-time analysis exactly
  (`{T1:20, T2:60, T3:240}` on the demo task set — run it: `python simulator_skeleton.py`).
- **`standalone_prompt.md`** — a single self-contained variant (facts folded in, no attached files) for
  one-off use where you cannot attach companions.

## Use it
- **Recommended:** put `system_prompt.md` in the system slot and include `reference_card.md` +
  `simulator_skeleton.py` in context (attachment / project knowledge). Ask the scheduling question and
  keep iterating; each answer is a model + runnable simulator + demonstration + schedulability analysis +
  limits, extended minimally from the previous iteration.
- **One-off:** paste `standalone_prompt.md` as the system prompt (or first message).

## How it was built and checked (2026-07-12)
- The two most error-prone facts — the Linux `prio` 0-is-highest scale, and the blocking bounds of basic
  priority inheritance vs the immediate-ceiling protocol — were web-verified.
- The simulator skeleton was run against the response-time analysis and matches.
- The whole system was **empirically validated** by an 8-agent adversarial workflow: two agents answered
  all four iterations (plus open-ended surprises — constrained deadlines, a sporadic task); six examiners
  graded the outputs on theory, simulator, and iteration discipline. **Zero high-severity findings.** The
  one real gap surfaced — the model narrating a Gantt chart instead of running the simulator — is closed
  by the "code output is authoritative; never hand-draw a trace" rules.

## Grounding (corpus scheduling keystones)
Liu & Layland, *JACM* 1973 (RM/EDF, utilization bound) · Joseph & Pandya 1986 / Audsley et al. 1993
(response-time analysis) · Leung & Whitehead 1982 (deadline-monotonic optimality) · Sha, Rajkumar &
Lehoczky, *IEEE TC* 39(9) 1990 (priority inheritance & ceiling protocols) · Buttazzo, *Hard Real-Time
Computing Systems* · Cervin & Henriksson, TrueTime · MathWorks SimEvents.
