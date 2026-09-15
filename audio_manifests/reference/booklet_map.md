# Booklet map — where the reasoning lives

**This package operationalizes; the booklet argues.** When you need the *why* behind a rule — or
you are about to reason past one — read the owning chapter of
`E:\dev\corpora\realtime-audio-pc-architecture-and-design-r1.md` (r1.0, 17 chapters, 20 invariants,
7 decision trees). One hop, then come back. Its parent (the embedded-C booklet at repo root) owns
the family-wide laws: information hiding, the effect boundary, error dispositions, the
enforcement thesis.

| topic | booklet |
|---|---|
| the machine model, hybrid cores, why the OS is a peer | ch. 1 |
| the deadline, the two planes, quasi-real-time honesty, xrun taxonomy | ch. 2 |
| the twenty invariants (each with its route) | ch. 3 |
| DT-1 choosing the period / latency dial | §2.5 |
| the core as a compiled graph; decisions-as-data; composition root order | ch. 4 |
| ports, ALSA/WASAPI adapter shapes, one-codebase mechanics, thread port | ch. 5 |
| why no locks on the RT plane (the full argument) | §6.2 |
| the five channels and their contracts | §6.3 |
| DT-2/DT-3 crossing the boundary; DT-4 parallelizing; DT-5 waiting | §6.4–§6.7 |
| memory-ordering discipline (C11 model, four idioms) | §6.6 |
| two clocks, drift, end-to-end latency accounting | ch. 7 |
| residency, allocation classes (DT-6), stacks, layout, working sets | ch. 8 |
| ILP, hazards (data/structural/control), flush inventory, FP regime, SIMD ladder | ch. 9 |
| DT-7 the optimization ladder | §9.8 |
| toolchain pinning, flag canon rationale, ThinLTO/PGO/BOLT, bench protocol | ch. 10 |
| elevation, placement, power, autopsy, deployment hardening, refusals | ch. 11 |
| error dispositions per plane, degrade ladder, safe state, watchdog analog | ch. 12 |
| flight recorder, always-on metrics, session report, crash capture, replay | ch. 13 |
| test topology, goldens, properties, fault injection, CI matrix, soak | ch. 14 |
| enforcement routes instantiated, RT guard, audits, budgets, contract-only register | ch. 15 |
| the pin table vs the parent, version-hub declaration, OPEN register | ch. 16 |
| lineage: corpus works, editorial register, external sources | ch. 17 |

Every card's "Go deeper" already points at reference sections; this map is for when the reference
section's rule meets a situation it does not fit — the booklet is where the tradeoff was priced.
