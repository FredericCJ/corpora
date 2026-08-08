# reference_card.md — fixed-priority real-time scheduling (apply these; cite the source)

## Task model
- Periodic task τᵢ = (Tᵢ period, Cᵢ WCET, Dᵢ deadline, Pᵢ priority). Implicit deadline Dᵢ = Tᵢ.
  Sporadic: Tᵢ = minimum inter-arrival. All times integer µs.
- Utilization Uᵢ = Cᵢ/Tᵢ; U = Σ Uᵢ. Hyperperiod H = lcm(Tᵢ).
- **Critical instant** (Liu & Layland): a task's worst-case response occurs when it is released
  together with all higher-priority tasks. Simulate from t=0 with releases aligned to expose it.

## Priority scale
- Linux effective priority `prio` ∈ [0,139], MAX_PRIO = 140, **lower number = higher priority**
  (RT 0–99; normal 100–139 with nice −20..+19 → 100..139). This model uses the same convention:
  **0 = highest**. [confirmed via kernel priority references]

## Fixed-priority preemptive scheduling
- At every instant the **ready job with the smallest priority number** runs and preempts any running
  job with a larger number. Equal priorities → deterministic tie-break (task id / FIFO), stated.
- hp(i) = tasks with priority number < Pᵢ; lp(i) = larger number.

## Response-Time Analysis — exact test (Joseph & Pandya 1986; Audsley et al. 1993)
    Rᵢ = Cᵢ + Bᵢ + Iᵢ + Σ_{j ∈ hp(i)} ⌈Rᵢ / Tⱼ⌉ · Cⱼ
- Bᵢ = worst-case blocking by lower-priority tasks (0 with no shared resources).
- Iᵢ = interrupt interference (0 with no interrupts).
- Iterate from Rᵢ⁽⁰⁾ = Cᵢ+Bᵢ+Iᵢ upward to a fixpoint. **Schedulable ⇔ Rᵢ ≤ Dᵢ ∀i.** If Rᵢ exceeds
  Dᵢ before converging, the task is unschedulable.
- **Constrained deadlines** (Dᵢ ≤ Tᵢ): same recurrence, tested against Dᵢ; the optimal fixed-priority
  ordering is **deadline-monotonic** — shorter Dᵢ ⇒ higher priority (Leung & Whitehead 1982).

## Utilization bound — sufficient, not necessary (Liu & Layland 1973)
- Rate-monotonic (shorter period ⇒ higher priority), implicit deadlines: schedulable if
  U ≤ n(2^{1/n} − 1) → ln 2 ≈ 0.693. Quick sufficient check; RTA above is exact.

## Priority inversion & resource protocols (Sha, Rajkumar & Lehoczky 1990)
- **Priority inversion:** a high-priority job blocks on a resource held by a low-priority job.
  **Unbounded** when medium-priority jobs preempt the holder (Mars Pathfinder, 1997). Needs shared
  resources to arise.
- **Basic Priority Inheritance (PIP):** while a low-priority holder blocks a higher-priority job it
  **inherits** that job's priority until it releases the resource. Bounds blocking but permits
  chained blocking and deadlock.
- **Immediate Priority Ceiling (IPCP / "highest-locker" / POSIX PTHREAD_PRIO_PROTECT):** each resource
  has a static **ceiling** = highest priority of any task that uses it; on lock a task's priority is
  **immediately raised to the ceiling**. Bounds blocking to **at most one** lower-priority critical
  section and **prevents deadlock**. Simplest correct choice for a "simple" model.
- Blocking term: Bᵢ = longest single critical section of any lower-priority task on a resource whose
  ceiling ≥ Pᵢ.

## Interrupts / ISRs
- ISRs run in interrupt context **above every task priority** and preempt any task. **Non-nestable**
  ⇒ interrupts are masked during an ISR, so ISRs run to completion and never preempt each other.
- Model a periodic ISR as top-priority periodic load (T_isr, C_isr, no task priority). Interference on
  task i: Iᵢ = ⌈Rᵢ / T_isr⌉ · C_isr (sum over ISRs). Fold context-switch / mask latency into C_isr if
  modeled.

## Deterministic simulation pattern
- **Time-driven** (1-µs tick) is the simplest correct engine and the easiest to extend — recommended
  for "simple" models. **Event-driven** (release/complete/preempt/lock/unlock/interrupt with
  tie-broken ordering) is the fast form. Either must be reproducible. Co-simulation references: TrueTime
  (RTOS tasks + interrupts + network), SimEvents (entity/server DES).

## Canonical sources (the netsim corpus scheduling keystones)
Liu & Layland, *JACM* 20(1) 1973 — RM/EDF & utilization bound · Joseph & Pandya 1986 / Audsley,
Burns, Richardson, Tindell & Wellings 1993 — response-time analysis · Leung & Whitehead 1982 —
deadline-monotonic optimality · Sha, Rajkumar & Lehoczky, *IEEE Trans. Computers* 39(9) 1990 —
priority inheritance & ceiling protocols · Buttazzo, *Hard Real-Time Computing Systems* — textbook ·
Cervin & Henriksson, **TrueTime** — RTOS+network+interrupt co-simulation · MathWorks **SimEvents** —
discrete-event scheduler models.
