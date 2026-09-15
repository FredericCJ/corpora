# Card: observability — events, counters, histograms

**Load when:** adding or changing an event, a counter, a histogram, the session report, or any
logging; wiring the heartbeat; using diagnosis mode.
**Depth:** `reference/observability_flightring_manifest.md` (O1–O9). Crash-side evidence:
`reference/error_tracing_contract_manifest.md` section E9. Using these instruments on a failure:
`cards/diagnose-failure.md`. Error dispositions that feed them: `cards/handle-errors.md`.

Facts verified 2026-08-12. Version-dependent claims route to
`reference/audio_platform_baseline_manifest.md` (the hub); if any file disagrees with the hub, the
hub wins. Reasoning root: the child booklet `realtime-audio-pc-architecture-and-design-r1.md`
(repo root) — operationalized here, never re-argued.

## The standard this card serves

**Evidence designed in, recorded always, harvested after.** [ESTABLISHED: booklet section 13.1]
On the RT plane, evidence costs one relaxed atomic add or one fixed-size ring write — never a
string, never a format, never a syscall (invariant 13). Emission is always on; transport happens
on the control plane's time. The failure artifact this discipline produces is what
`cards/diagnose-failure.md` reads — break the schema and you blind the loop.

## The always-on set

[Table derives from booklet section 13.2; one writer on-plane, readers off-plane, per instrument.]

| instrument | contents | RT-plane cost |
|---|---|---|
| callback histogram | every render's cost + the wakeup-gap split, fixed log-spaced bins | one relaxed increment |
| headroom gauge | cost-over-budget, smoothed; feeds the degrade ladder and the UI meter | one store through the channel |
| counters | xruns by class, degrade-rung entries/exits, per-ring drop counts, pool high-water and steals, output-sentinel interventions, denormal/NaN patrol trips, guard trips (dev) | one relaxed add each — "there is no budget argument against any of them" |
| event stream | stream/device/elevation/ladder state transitions, port crossings (grants, denials, faults), every xrun with autopsy attachment, every rung change | one fixed-size ring write |

## Recipe: add a counter

1. **Registry row first** (`reference/observability_flightring_manifest.md` section O2): id, name,
   unit, meaning, writer thread + plane. Ids are allocated, never reused; retired ids stay
   reserved. [ESTABLISHED: booklet section 13.5] *(build-catchable — G3 audits diff the registry)*
2. One relaxed add at the site — the blessed idiom for trend-read values
   (`reference/rt_plane_rules_manifest.md` section R6). *(analysis-catchable ordering discipline)*
3. Surface it: drain rendering + session-report field = a **schema version bump**, additive only
   (`config/session_report.schema.json`). *(build-catchable — schema validation in CI)*
4. A test that it **ticks** under the scenario it witnesses. *(host-test-catchable)*

## Recipe: add an event

1. Registry id row (O2) — stable forever, payload-word meanings documented in the row.
2. Fixed-size payload: id + timestamp + a few words. No strings, no heap pointers, ever.
   [ESTABLISHED: booklet section 13.1] *(compiler-catchable in RT TUs via the poison prelude for
   the formatting families; review for the rest)*
3. Emit through the flight ring (O3); the ring's overflow policy is declared and **drops are
   counted, never silent** (invariant 2). *(runtime-catchable — the drop counter is the witness)*
4. Drain decode entry: the control-plane renderer maps id → human text. An event the drain cannot
   decode is a defect the drain counts. *(host-test-catchable — decode-coverage test)*
5. If it reaches the session report: schema version note.

```c
typedef struct ar_event {   /* one ring slot: fixed size, POD                    */
    uint32_t id;            /* O2 registry row — allocated, never reused         */
    uint32_t w0;            /* payload words; meaning fixed per id               */
    uint64_t t_mono;        /* timestamp from the monotonic pair stream          */
    uint64_t w1, w2;        /* no strings, no heap pointers                      */
} ar_event;                 /* layout static-asserted (booklet section 8.4)      */
```

Identifiers illustrative; normative layout in `reference/observability_flightring_manifest.md`
sections O2–O3.

## Recipe: add a histogram

Fixed log-spaced bins sized at design time; one relaxed increment on-plane; percentile extraction
happens **off-plane only**. [ESTABLISHED: booklet section 13.2] Bins that reach the session report
are schema fields — version bump. Never resize or re-bin live *(contract-only, review)*.

## The session report — fields you must not break

Every run can end in one artifact; its consumers are deliberately format-identical: the user's bug
report, the soak rig's gate evidence (invariant 6 gates on these exact fields), and the opt-in
fleet view. [ESTABLISHED: booklet section 13.3] Consequences:

- The schema is a **versioned contract**: `config/session_report.schema.json`. Additive change =
  minor `schema_version` bump + schema re-hash; breaking change = new major and a new report
  filename — never a silent field edit, because soak gates and downstream parsers read these
  fields [ESTABLISHED: the schema file's own `$comment` contract]. *(build-catchable — CI
  validates reports against the schema; the prose twin is
  `reference/error_tracing_contract_manifest.md` section E8, and the two must match exactly)*
- Load-bearing fields: build identity (invariant 17), machine class + negotiated format, the
  histograms, every counter, degrade/xrun event history with autopsies. [ESTABLISHED: booklet
  section 13.3]
- The report never carries audio content; upload is explicit and consented. [ESTABLISHED: booklet
  section 13.3] *(contract-only + review)*
- The **replay dividend**: recorded command-ring traffic + events + the deterministic core = the
  session re-rendered bit-exactly offline. Keep the recording path working — it is the field-bug
  to regression-test conveyor. *(host-test-catchable — replay round-trip test)*

## Heartbeat and supervisor

The device loop publishes its block counter as proof of *progress* (it advances only when blocks
render); a control-plane supervisor alarms when the stream claims live but the counter stalls,
then walks the escalating-restart ladder — stream, engine, process — leaving its story in the
flight ring first. [ESTABLISHED: booklet section 12.6] Mechanics:
`reference/observability_flightring_manifest.md` section O6. *(runtime-catchable)*

## Diagnosis mode

Off in ship-default, zero RT cost when off. [ESTABLISHED: booklet section 11.5] Arms: per-callback
deltas at block edges (minor/major faults, voluntary/involuntary switches, wakeup-gap vs duration
split — the xrun classifier's inputs); off-plane system-tracer correlation (ETW on NT, perf on
Linux) matched to the flight ring by monotonic timestamps; and the named residue — SMIs are
visible only as unattributed gaps. The soak rig always runs the first layer. Usage:
`reference/observability_flightring_manifest.md` section O9.

## Never on the RT plane

- Format, log, print, build a string — invariant 13. *(compiler-catchable:
  `config/rt_prelude_poison.h` poisons the stdio/formatting families in RT TUs [MEASURED
  2026-08-12: `#pragma GCC poison` yields "attempt to use a poisoned identifier" on CLANG64 clang
  22.1.8]; runtime-catchable: the guard net)*
- Block on the drain, or wait for the reader — the ring is wait-free on the RT side (invariant 2).
  *(host-test-catchable: channel contract suites)*
- Variable-size payloads or heap pointers in events. *(review + static assert on the slot type)*
- Percentile/summary computation on-plane. *(review; the guard traps the syscalls such code tends
  to drag in)*
- Silent drops — every ring names its overflow policy and counts. *(runtime-catchable)*

Control-plane logging is ordinary structured logging — leveled, rotated, boring; no secrets, no
PII, ids stable. [ESTABLISHED: booklet section 13.5] Depth:
`reference/observability_flightring_manifest.md` section O8.

## What you owe

Every new id: registry row + decode entry + schema bump (if surfaced) + a test that it ticks +
the ring's drop policy stated. Every schema change: version bump + expand-contract note + the
soak-gate fields untouched or migrated. Every removal: id retired, never recycled.

## Decisions you must not invent

Telemetry opt-in and consent posture · session-report location and retention · which counters are
front-page in the report · who may toggle diagnosis mode in the field · control-plane log sink,
rotation, and retention.

## Go deeper

| question | where |
|---|---|
| principles and the RT-cost argument | `reference/observability_flightring_manifest.md` section O1 |
| event schema and the id registry | `reference/observability_flightring_manifest.md` section O2 |
| the flight ring implementation | `reference/observability_flightring_manifest.md` section O3 |
| histogram bins and extraction | `reference/observability_flightring_manifest.md` section O4 |
| the counters canon | `reference/observability_flightring_manifest.md` section O5 |
| heartbeat and supervisor | `reference/observability_flightring_manifest.md` section O6 |
| session report generation | `reference/observability_flightring_manifest.md` section O7 |
| diagnosis mode operation | `reference/observability_flightring_manifest.md` section O9 |
| crash capture and dirty-exit harvest | `reference/error_tracing_contract_manifest.md` section E9 |
