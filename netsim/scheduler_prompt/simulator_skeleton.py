"""simulator_skeleton.py — deterministic fixed-priority preemptive scheduler simulator (single core).

Time base: integer microseconds. Priority convention: 0 = highest (smaller number wins).
Time-driven 1-µs tick: simplest correct engine, easy to extend each iteration.
Extend, don't rewrite:
  Iter 2 (resources + inversion protocol): give each Task a `sections` list of (resource, length);
    track locks, raise the holder's effective priority (inheritance) or to the ceiling (IPCP).
  Iter 3 (interrupts): add an ISR source that, every T_isr, runs C_isr ticks above all tasks and,
    being non-nestable, is not itself preempted.
"""
from dataclasses import dataclass
from math import gcd
from functools import reduce


@dataclass
class Task:
    id: str
    period: int          # T (µs)
    wcet: int            # C (µs)
    priority: int        # 0 = highest
    deadline: int = None  # D; defaults to the period (implicit deadline)

    def __post_init__(self):
        if self.deadline is None:
            self.deadline = self.period


def hyperperiod(tasks):
    return reduce(lambda a, b: a * b // gcd(a, b), (t.period for t in tasks))


def simulate(tasks, horizon=None, trace=False):
    """Fixed-priority preemptive, single core. Returns {id: worst-case response time},
    or {id: None} if that task ever misses a deadline / overruns into its next release."""
    H = horizon if horizon is not None else hyperperiod(tasks)
    rem = {t.id: 0 for t in tasks}      # remaining execution of the current job
    rel = {t.id: 0 for t in tasks}      # release time of the current job
    active = {t.id: False for t in tasks}
    wcrt = {t.id: 0 for t in tasks}
    missed = {t.id: False for t in tasks}
    timeline = []

    for now in range(H):
        # 1. releases (all tasks phase-aligned at t=0, then every period)
        for t in tasks:
            if now % t.period == 0:
                if active[t.id]:                       # prior job unfinished at new release
                    missed[t.id] = True
                rem[t.id], rel[t.id], active[t.id] = t.wcet, now, True
        # 2. dispatch: highest priority (smallest number), tie-break by id
        ready = [t for t in tasks if active[t.id] and rem[t.id] > 0]
        running = min(ready, key=lambda t: (t.priority, t.id)) if ready else None
        timeline.append(running.id if running else 'idle')
        # 3. run one tick
        if running:
            rem[running.id] -= 1
            if rem[running.id] == 0:
                active[running.id] = False
                resp = (now + 1) - rel[running.id]
                wcrt[running.id] = max(wcrt[running.id], resp)
                if resp > running.deadline:
                    missed[running.id] = True

    if trace:
        print(_gantt(timeline))
    return {t.id: (None if missed[t.id] else wcrt[t.id]) for t in tasks}


def _gantt(timeline):
    """Compress equal runs into a compact ASCII timeline."""
    out, prev, start = [], timeline[0], 0
    for i, x in enumerate(timeline[1:], 1):
        if x != prev:
            out.append(f'[{start:>5}-{i:>5}) {prev}')
            prev, start = x, i
    out.append(f'[{start:>5}-{len(timeline):>5}) {prev}')
    return '\n'.join(out)


if __name__ == '__main__':
    demo = [Task('T1', 100, 20, 10), Task('T2', 150, 40, 20), Task('T3', 350, 100, 30)]
    print('worst-case response times (µs):', simulate(demo))
    # RTA expectation: R1=20, R2=60, R3=240; all ≤ deadline ⇒ schedulable.
