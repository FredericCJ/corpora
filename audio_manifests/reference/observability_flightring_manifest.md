# Observability & Flight Ring — Ground-Truth Manifest

**Purpose.** The always-on evidence layer of the audio engine: flight-ring events, histograms, counters, heartbeat, session report, control-plane logs, and diagnosis mode — specified so that any field failure explains itself from artifacts alone (WHAT = event id, WHERE = module prefix + stream_pos + t_mono_ns, WHY = payload + autopsy + counters) and the coding agent can patch from a report without a rerun.

Facts verified 2026-08-12. Version-dependent claims route to reference/audio_platform_baseline_manifest.md (the hub); if any file disagrees with the hub, the hub wins.

Reasoning root: the booklet at realtime-audio-pc-architecture-and-design-r1.md (repo root) — this file operationalizes booklet ch. 13 (the flight recorder), section 11.5 (the autopsy), and section 7.1 (the two clocks). It never re-argues them.

**Tag legend.** [ESTABLISHED: source] · [VERSION-DEPENDENT - hub Hn] · [MEASURED 2026-08-12] (run on the reference machine, command recorded) · [OPEN — ASSUMED or NEEDS-INPUT] (project decision) · [CC-FACT] (model knowledge of API/OS mechanics, verification pointer given) · [FLAGGED-SECONDARY] · [UNVERIFIED]. An untagged factual claim is a defect in this file.

**Siblings, not duplicated.** Ring implementation → reference/concurrency_channels_manifest.md section C2. RT-plane bans and the guard → reference/rt_plane_rules_manifest.md sections R2/R4. Error-code registry and evidence chain → reference/error_tracing_contract_manifest.md sections E3/E7. Session-report field semantics → section E8 + config/session_report.schema.json. Crash capture and dirty-exit harvest → section E9. Task entry points: cards/observability.md, cards/diagnose-failure.md.

---

## O1. Principles

The recorder is always on; the *recording* (format, persist, ship) is never on the RT plane. Evidence is designed in, recorded always, harvested after [ESTABLISHED: booklet section 13.1]. The histogram, not the log line, is the primary instrument, because the product lives in the tail of a distribution [ESTABLISHED: booklet section 2.6].

| # | principle | operational meaning | route |
|---|---|---|---|
| P1 | **Never on RT: no format, no log, no print, no I/O** — events only | RT code emits fixed-size records into a wait-free ring (O3); rendering happens on the control plane [ESTABLISHED: booklet section 13.1, invariant 13] | compiler-catchable (poison list in config/rt_prelude_poison.h; mechanism verified — [MEASURED 2026-08-12: `#pragma GCC poison malloc` → "attempt to use a poisoned identifier", CLANG64 clang 22.1.8]) + runtime-catchable (R4 guard) |
| P2 | **Ids, not strings** | every event is a u16 registry id plus scalar words; identifiers and words, never format strings [ESTABLISHED: booklet section 13.2] | compiler-catchable (the emit API accepts only integers — O3; no `char*` overload exists) |
| P3 | **Always-on at negligible cost** | one relaxed add per counter, one relaxed store pair per histogram bin, nanoseconds per event; "there is no budget argument against any of them" [ESTABLISHED: booklet section 13.2] | target-test-catchable (bench lane shows observability delta below noise — reference/optimization_microarch_manifest.md section P2) |
| P4 | **Postmortem-first** | design for the failure on a stranger's machine: ring + counters live in one contiguous named region so every crash dump contains the recorder by construction [ESTABLISHED: booklet sections 13.1, 13.4] | build-catchable (region symbol present — audit via llvm-nm; symbol listing works [MEASURED 2026-08-12: llvm-nm lists object symbols on CLANG64]) |
| P5 | **Failure artifacts are self-locating** | every artifact (event, log line, report) carries event id, module, both clocks, and build identity; the agent patches from the artifact, not from a rerun [ESTABLISHED: booklet section 13.3; house doctrine] | host-test-catchable (T2 self-location contract — reference/testing_verification_manifest.md section T2) |
| P6 | **Every drop is counted** | lossy transport is legal, silent loss is not; drops are witnessed twice (counter + seq gap) [ESTABLISHED: booklet sections 6.3(b), 13.1, invariant 2] | host-test-catchable (T7 full-ring stress) |

### Never

- Never call `printf`/`fprintf`/`snprintf`/`fopen`/`write`/`malloc` (or any O8 logging entry point) from RT TUs — poison header rejects at compile [MEASURED 2026-08-12: poison mechanism works on CLANG64 clang 22.1.8]; guard traps escapes at runtime (R4). *(compiler-catchable + runtime-catchable)*
- Never place a pointer in payload words that the drain must dereference — the record must decode from a crash dump with no live heap. Addresses are legal only as opaque correlation ids, declared by the payload kind. *(contract-only — register in reference/rt_plane_rules_manifest.md section R8)*
- Never block, spin, or retry on ring full — drop-newest and count (O3). *(host-test-catchable: T7)*
- Never reset live counters or histograms by `memset` — re-baseline in the drain (O4). *(host-test-catchable: TSan on the Linux leg; TSan is Linux-leg only [MEASURED 2026-08-12: no tsan runtime in CLANG64 clang runtime libs])*
- Never emit unbounded event storms — every RT emit site has a per-block cap; a storm collapses to a counter plus one event per block (O5). *(host-test-catchable: T6 fault injection)*
- Never timestamp an event with the calendar clock — monotonic + stream position only; calendar time is display-only [ESTABLISHED: booklet section 7.1]. *(compiler-catchable: wall-clock APIs are on the R2 poison list for RT TUs)*

### Decisions you must not invent

Ring capacities and drain cadence beyond the ASSUMED defaults (O3) · log rotation policy, file locations, retention counts (O7, O8) · the PII/filename redaction policy (O8) · degrade-rung ownership map (O5) · watchdog cadence and stall thresholds (O6) · whether ship builds keep runtime-armable diagnosis or compile it out (O9) · fleet telemetry opt-in (O7). Each is tagged OPEN at its site; record the product's answer in the project spec, not in code comments.

## O2. Event schema and the id registry

### The record — package contract

This 56-byte fixed-size record is the wire contract of the whole observability layer. This file owns it [OPEN — ASSUMED: package contract, this manifest is the authority; change = expand/contract migration per O8].

```c
#include <stdint.h>

typedef struct fr_event {
    uint16_t event_id;      /* module-prefixed registry id (below)            */
    uint16_t payload_kind;  /* bits [15:13] severity, bits [12:0] kind id     */
    uint32_t seq;           /* per-ring monotonic, wraps; gaps witness drops  */
    uint64_t t_mono_ns;     /* machine time: OS monotonic ns                  */
    uint64_t stream_pos;    /* device time: frames since stream start        */
    uint64_t payload[4];    /* meaning fixed by payload_kind                  */
} fr_event;

_Static_assert(sizeof(fr_event) == 56, "fr_event is the 56-byte wire contract");
```

- No padding on x86-64 SysV or Windows-x64 ABIs (2+2+4 = 8, then five 8-byte members) — the `_Static_assert` is the proof and gates both legs [CC-FACT; the assert makes it build-catchable]. This exact struct, the assert, and the O3/O4 snippets compile clean and run [MEASURED 2026-08-12: `clang -std=c17 -Wall -Wextra -O2 fr_check.c -lpsapi`, zero diagnostics, CLANG64 clang 22.1.8, target x86_64-w64-windows-gnu].
- Every event carries **both clocks** so any event joins both timelines without a lookup; the pair stream of booklet section 7.1 is the cross-timeline anchor, and events inherit its discipline [ESTABLISHED: booklet sections 7.1, 13.1].
- Little-endian on both legs; a crash-dump decoder reads slots raw [CC-FACT: x86-64 is little-endian on both OSes].

### Severity is a field, not a channel

One ring per producer; severity never selects a transport. Severity lives in bits [15:13] of `payload_kind` so a raw dump decodes without the registry table:

```c
enum fr_sev { FR_TRACE = 0, FR_DEBUG, FR_INFO, FR_WARN, FR_ERROR, FR_FATAL };
#define FR_PK(sev, kind) ((uint16_t)(((unsigned)(sev) << 13) | ((kind) & 0x1FFFu)))
```

RULE: severity is fixed per event id, declared in the registry row; the encoded field MUST equal the registry's declaration (redundancy is deliberate — it makes dumps self-describing and mismatches detectable). *(build-catchable: G3 structural audit greps emit sites against the generated table — reference/quality_gates_ci_manifest.md section G3)* [OPEN — ASSUMED: fixed-per-id severity; dynamic escalation is NOT allowed in r1.]

RULE: RT code never branches on severity (no "if error then do more work" on the plane); the drain routes by severity off-plane. *(contract-only + host-test-catchable: T7 asserts emit cost is severity-independent)*

### Id registry discipline

Same discipline and same generator as the error-code registry — module-prefixed, stable forever, generated from one table [cross-ref reference/error_tracing_contract_manifest.md section E3]. Event ids and error codes are distinct id spaces sharing the module-prefix map and the generation tool [OPEN — ASSUMED: one shared source table with a `kind` column (ERR vs EV); E3 owns the table location and generator].

| rule | statement | route |
|---|---|---|
| stable | an id, once shipped, never changes meaning; retired ids stay reserved [ESTABLISHED: booklet section 13.5] | build-catchable (G3 audit diffs the generated table against the last released baseline) |
| generated | handwritten event-id constants are forbidden; the generated header is the only source | build-catchable (G3 grep for numeric literals at emit sites) |
| module-prefixed | high byte of `event_id` = module; the drain and the agent can localize WHERE from the id alone | build-catchable (generator enforces range ownership) |
| registered payload | every `payload_kind` documents its four words (name, unit, packing) in the same table | build-catchable (generator rejects unregistered kinds) |

### Starter allocation

[OPEN — ASSUMED: starter map below; the generated table is the authority once E3's tooling lands. Do not extend by hand — add rows to the table.]

| prefix | module | starter ids (severity) |
|---|---|---|
| 0x00 | session/meta | 0x0001 EV_SESSION_START (info), 0x0002 EV_SESSION_END (info), 0x0003 EV_DIRTY_EXIT_HARVEST (warn) |
| 0x01 | device/stream | 0x0101 EV_STREAM_STATE (info), 0x0102 EV_DEVICE_FAULT (error), 0x0103 EV_FORMAT_NEGOTIATED (info) |
| 0x02 | deadline/xrun | 0x0201 EV_XRUN (error), 0x0202 EV_XRUN_ESCALATE (error), 0x0203 EV_CB_DELTAS (debug) |
| 0x03 | degrade ladder | 0x0301 EV_RUNG_ENTER (warn), 0x0302 EV_RUNG_EXIT (info), 0x0303 EV_VOICE_STEAL (info) |
| 0x04 | observability self | 0x0401 EV_RING_DROP (warn), 0x0402 EV_BUDGET_NEAR (warn), 0x0403 EV_DIAG_MARK (info) |
| 0x05 | watchdog | 0x0501 EV_WD_STALL_SUSPECT (warn), 0x0502 EV_WD_STREAM_RESTART (error), 0x0503 EV_WD_ENGINE_RESTART (error), 0x0504 EV_WD_PROC_KILL (fatal), 0x0505 EV_WD_RECOVERED (info) |
| 0x06 | memory/pools | 0x0601 EV_POOL_PRESSURE (warn) |
| 0x07 | guards/patrols | 0x0701 EV_GUARD_TRIP (error), 0x0702 EV_SENTINEL_CLAMP (warn), 0x0703 EV_FP_PATROL (warn) |
| 0x08 | control/UI/log | 0x0801 EV_REPORT_WRITTEN (info), 0x0802 EV_DIAG_ARMED (info), 0x0803 EV_DIAG_DISARMED (info), 0x08FF EV_ADHOC (debug; dev builds only — forbidden in ship, G3 grep) |

Starter payload kinds: `PK_NONE`=0 · `PK_WORDS` (raw scalars) · `PK_XRUN` (w0 = class per booklet section 2.4: 0 self-overrun, 1 late-wakeup, 2 external-stall, 3 device-fault; w1 = gap_ns; w2 = dur_ns; w3 = E3 error code if any) · `PK_STATE` (w0 = from, w1 = to, w2 = E3 error code, w3 = 0) · `PK_RUNG` (w0 = rung 1..5, w1 = headroom permille, w2 = blocks in previous state) · `PK_DROP` (w0 = ring id, w1 = dropped count, w2 = first lost seq) · `PK_CB_DELTAS_POSIX` / `PK_CB_DELTAS_NT` (O9). E3 error codes appearing in payload words is the join point of the evidence chain [cross-ref reference/error_tracing_contract_manifest.md section E7].

### Add a new event — walkthrough

1. Add one row to the shared id table (module range, name, severity, payload kind, meaning of each of the four words) — reference/error_tracing_contract_manifest.md section E3 owns the table and generator; never hand-write the constant.
2. Regenerate the header; generation fails on range collisions or unregistered payload kinds. *(build-catchable)*
3. Emit with `fr_emit(ring, EV_..., FR_PK(sev, PK_...), pos, w0, w1, w2, w3)` (O3); RT emit sites respect the per-block cap (O1 Never list).
4. The drain needs no change — severity and kind are self-describing; add a pretty-printer entry only when a payload deserves unit formatting.
5. If severity ≥ warn, the golden log-line test gains a case (O8). *(host-test-catchable)*
6. The session report picks the event up through its generic event array — schema untouched; G3's table diff records the addition as append-only. *(build-catchable)*

## O3. The flight ring

The transport: an SPSC ring of `fr_event` records per RT-producing thread, drained by one control-plane telemetry thread. Implementation (claim/publish halves, cache-line-split indices, cached peer index, power-of-two mask) is owned by reference/concurrency_channels_manifest.md section C2 and is not restated here [ESTABLISHED: booklet section 6.3(b)].

### Topology

| element | value | tag |
|---|---|---|
| producers | one ring per RT thread (device-callback thread + each RT worker); SPSC means never share a ring between producers | [ESTABLISHED: booklet section 6.3(b) — one named producer] |
| consumer | the telemetry drain, one control-plane thread (thread inventory: reference/rt_plane_rules_manifest.md section R1) | [ESTABLISHED: booklet section 13.1 — drain renders/persists on control-plane time] |
| residency | rings + counters + histograms in one contiguous immortal-arena region with a magic header (`"FLTRING1"`, u32 layout version, build-id hash) so dumps and the dirty-exit harvester self-validate | [ESTABLISHED: booklet section 13.4 — one known named region] + [OPEN — ASSUMED: magic/header layout]; arena: reference/memory_residency_manifest.md section M2 |
| slot stride | 64 bytes (56-byte record + 8 reserved-zero pad), `_Alignas(64)` — no record straddles a cache line | [CC-FACT: 64-byte lines on Alder Lake; machine row - hub H8] |

### Emit — the only RT-side API

```c
/* RT plane. Wait-free. Never blocks, never formats, never allocates. */
static inline void fr_emit(fr_ring *r, uint16_t id, uint16_t pk, uint64_t pos,
                           uint64_t w0, uint64_t w1, uint64_t w2, uint64_t w3)
{
    uint32_t seq = r->seq_next++;         /* consumed even on drop: gap == loss   */
    fr_event *e = fr_try_claim(r);        /* C2 claim half; NULL when full        */
    if (!e) { fr_count_drop(r); return; } /* drop-newest + one relaxed add        */
    *e = (fr_event){ id, pk, seq, fr_mono_ns(), pos, { w0, w1, w2, w3 } };
    fr_publish(r);                        /* C2 release-store of the head index   */
}
```

`fr_mono_ns()` = `clock_gettime(CLOCK_MONOTONIC)` on Linux (vDSO, no kernel entry) and `QueryPerformanceCounter` scaled to ns on NT (user-mode TSC read; scale factor computed once at init, RT does multiply/shift only) [CC-FACT — classification as RT-safe is owned by reference/rt_plane_rules_manifest.md section R7; QPC frequency is a machine fact - hub H2].

### Overflow policy: drop-newest, alarmed

- On full: the new event is dropped at the producer and the ring's drop counter gets one relaxed add. Drop-newest (not overwrite-oldest) because overwriting unread slots would race the single consumer and break C2's contract; the "black-box tail" survives because the drain runs continuously — the ring only holds the not-yet-drained suffix [ESTABLISHED: booklet section 6.3(b) — declared overflow policy, counted drops].
- The **drain**, not the producer, emits `EV_RING_DROP` (payload `PK_DROP`) when it observes the drop counter advance, and cross-checks counter delta against the `seq` gap — two independent witnesses [ESTABLISHED: booklet invariant 2, quoted at section 13.2]. *(host-test-catchable: T7 stress fills the ring and asserts counter == seq gap == expected loss)*
- Sustained drops at nominal load are a release blocker: the soak gate asserts zero flight-ring drops over the soak window [cross-ref reference/quality_gates_ci_manifest.md section G7]. *(target-test-catchable)*

### Sizing rule

`capacity = next_pow2(max(1024, events_per_block_cap × blocks_per_sec × 2 × drain_period_sec))`, then multiply by stall armor.

Worked default [OPEN — ASSUMED]: cap 8 events/block × 375 blocks/s (48 kHz / 128) × 2 × 0.05 s drain period = 300 → pow2 floor 1024 minimum; default **4096 slots × 64 B = 256 KiB per ring** buys ~1.4 s of full-rate history, so a stalled drain — exactly the moment history matters — loses nothing. Three RT producers = 768 KiB, accounted in the working-set budget [cross-ref reference/memory_residency_manifest.md section M8].

### Drain obligations (control plane, every pass)

1. Batch-pop at most one capacity per ring per pass (C2 consumer idiom); never busy-wait between passes — cadence default 20 Hz [OPEN — ASSUMED].
2. Append records to the in-memory session event log (bounded; spill-to-file only in diagnosis mode [OPEN — ASSUMED: bound 65536 events]).
3. Project severity ≥ warn into the control-plane log (O8) — the text log is a *projection*, the report carries the full stream.
4. Compare drop counters to last pass; emit `EV_RING_DROP` on delta.
5. Feed the session-report accumulator (O7) and the supervisor's view (O6).
6. On shutdown: final sweep runs after the RT plane stops and before the report is built — ordering owned by the shutdown protocol [cross-ref reference/concurrency_channels_manifest.md section C9]. *(host-test-catchable: shutdown test asserts no event emitted after final sweep is lost)*

### Failure modes in the artifacts

Merge rule first: per-ring order is seq order; the drain merge-sorts across rings by `t_mono_ns` (stable, seq as tiebreak) before report assembly — never assume global order across rings. *(host-test-catchable: T7 interleaving test)*

| symptom | meaning | first move |
|---|---|---|
| drop delta > 0 and the seq gap matches | drain stalled, or a burst beat the cap | check drain-thread liveness, then re-run the sizing math above; in soak this fails the G7 gate |
| seq gap with no matching drop count | producer-side contract violation (torn claim, missed publish) | T7 stress repro; TSan on the Linux leg [MEASURED 2026-08-12: no tsan runtime on CLANG64 — Linux leg only] |
| drop count with no seq gap | double-count in the drop path, or a dirty-exit harvest overlapped a live ring | audit the emit path; check harvest ordering [cross-ref reference/error_tracing_contract_manifest.md section E9] |
| `t_mono_ns` regressions in the merged stream | drain merged without the stable sort | fix the merge; each ring's stream is monotonic by construction |
| `stream_pos` frozen while `t_mono_ns` advances | the device stopped delivering — a stream fault, not an observability bug | route to the adapter fault verbs [cross-ref reference/device_adapter_manifest.md sections D4, D7, D8] |

## O4. Histograms

Two per RT thread, always on: **callback duration** (start → end) and **wakeup gap** (expected start per the device-paced schedule → actual start) — the split that classifies the xrun taxonomy [ESTABLISHED: booklet sections 11.5, 13.2]. Worker-thread job-duration histograms are optional [OPEN — ASSUMED: off in r1]. Percentile extraction is off-plane; the RT side pays one relaxed load+store pair per sample [ESTABLISHED: booklet section 13.2 — "the whole distribution §2.6 demands, for the cost of an add"].

### Bin table — package contract

18 log2-spaced bins over **binary microseconds** (1 ubin = 1024 ns; edges are powers of two of that unit — deliberate: `ns >> 10` replaces a division, and log bins do not care about the 2.4% unit skew) [OPEN — ASSUMED: this file owns the bin map; changing it is an expand/contract migration because reports and gates parse it].

| bin | covers (approx) | bin | covers (approx) |
|---|---|---|---|
| 0 | < 1.02 us | 9 | 262 – 524 us |
| 1 | 1.02 – 2.05 us | 10 | 0.52 – 1.05 ms |
| 2 | 2.05 – 4.10 us | 11 | 1.05 – 2.10 ms |
| 3 | 4.10 – 8.19 us | 12 | 2.10 – 4.19 ms |
| 4 | 8.19 – 16.4 us | 13 | 4.19 – 8.39 ms |
| 5 | 16.4 – 32.8 us | 14 | 8.39 – 16.8 ms |
| 6 | 32.8 – 65.5 us | 15 | 16.8 – 33.6 ms |
| 7 | 65.5 – 131 us | 16 | 33.6 – 67.1 ms |
| 8 | 131 – 262 us | 17 | >= 67.1 ms (overflow) |

### Writer idiom — single writer, relaxed, no RMW

```c
#include <stdatomic.h>

typedef struct fr_hist {
    _Alignas(64) _Atomic uint64_t bin[18];
    _Atomic uint64_t max_ns;              /* exact worst case, bin-independent */
} fr_hist;

static inline void fr_hist_add(fr_hist *h, uint64_t ns)
{
    uint64_t u = ns >> 10;                                   /* binary us */
    unsigned i = (u == 0) ? 0u : (unsigned)(64 - __builtin_clzll(u));
    if (i > 17u) i = 17u;
    uint64_t b = atomic_load_explicit(&h->bin[i], memory_order_relaxed);
    atomic_store_explicit(&h->bin[i], b + 1u, memory_order_relaxed);
    uint64_t m = atomic_load_explicit(&h->max_ns, memory_order_relaxed);
    if (ns > m) atomic_store_explicit(&h->max_ns, ns, memory_order_relaxed);
}
```

Single writer means load+store (no lock-prefixed RMW) is sufficient and cheaper; the blessed-idiom argument is owned by reference/rt_plane_rules_manifest.md section R6 [ESTABLISHED: booklet section 13.2 — "one relaxed increment"]. Compiles clean as C17 with `-Wall -Wextra` on CLANG64 [MEASURED 2026-08-12: snippet compile check, clang 22.1.8]. `__builtin_clzll` is a clang builtin, both legs [CC-FACT]. *(host-test-catchable: TSan on the Linux leg over a reader/writer stress — TSan is Linux-leg only [MEASURED 2026-08-12: no tsan runtime on CLANG64]; cross-ref reference/testing_verification_manifest.md section T8)*

### Reading and reset

| rule | statement | route |
|---|---|---|
| percentiles off-plane | drain snapshots bins, reports p50/p95/p99/p99.9 as the **upper edge** of the first bin where the cumulative count crosses the quantile (conservative: "at most this"); exact worst case comes from `max_ns`, never from a bin [ESTABLISHED: booklet section 2.6 — percentiles and maxima are the assertions] | host-test-catchable (unit test on known distributions) |
| no live reset | bins and `max_ns` are cumulative for the session; the RT side never zeroes them and the control side never `memset`s while the writer lives — windowed views are drain-side **snapshot deltas**; "reset" = re-baseline in the drain | host-test-catchable (TSan, Linux leg) + contract-only for the intent |
| config epochs | on period/format renegotiation the drain stamps the snapshot with `EV_FORMAT_NEGOTIATED` so the report can segment distributions per configuration [OPEN — ASSUMED] | host-test-catchable |
| gate feed | bench and soak gates consume the same bins — one instrument, no parallel truth [cross-ref reference/testing_verification_manifest.md section T10, reference/quality_gates_ci_manifest.md section G4] | build-catchable (gate reads report JSON) |

### Percentile extraction (off-plane)

```c
/* Control plane. Conservative: returns the UPPER edge of the crossing bin. */
static uint64_t fr_hist_quantile_ns(const uint64_t bin[18], double q)
{
    uint64_t total = 0, acc = 0;
    for (int i = 0; i < 18; i++) total += bin[i];
    if (total == 0) return 0;
    uint64_t need = (uint64_t)(q * (double)total) + 1u;
    for (int i = 0; i < 17; i++) {
        acc += bin[i];
        if (acc >= need) return 1024ull << i;         /* upper edge, ns */
    }
    return UINT64_MAX;   /* crossed in the overflow bin — see rule below */
}
```

Reports state quantiles as "<= edge". A quantile landing in bin 17 is reported as the exact `max_ns` plus an overflow flag — never as a fabricated interior value. *(host-test-catchable: unit test against known synthetic distributions)*

## O5. Counters canon

The always-on set, verbatim from booklet section 13.2, each a single-writer relaxed u64 (same idiom as O4). Every counter has one writer on the plane, readers off it; thresholds convert counts into events so trends become visible without polling archaeology [ESTABLISHED: booklet section 13.2].

| counter | writer | reader | on threshold → event |
|---|---|---|---|
| `ct_xrun[4]` — by class: self-overrun, late-wakeup, external-stall, device-fault [ESTABLISHED: booklet section 2.4] | RT device-adapter loop | drain, supervisor | every xrun → `EV_XRUN` (`PK_XRUN`, autopsy words attached per O9); leaky-bucket rate overflow → `EV_XRUN_ESCALATE` [ESTABLISHED: booklet section 12.3] |
| `ct_ring_drop[ring]` | producing RT thread | drain | delta > 0 per drain pass → `EV_RING_DROP` (O3) |
| `ct_pool_hw[pool]` high-water, `ct_pool_steal[pool]` | RT pool owner [cross-ref reference/memory_residency_manifest.md section M3] | drain | high-water > configured watermark → `EV_POOL_PRESSURE`; steals also count under the degrade ladder row below |
| `ct_sentinel` — output-sentinel interventions [ESTABLISHED: booklet section 12.5] | RT output stage | drain | any in a block → `EV_SENTINEL_CLAMP`, max 1/block (storm collapses to count) |
| `ct_denorm`, `ct_nan` — FP patrol trips [ESTABLISHED: booklet section 9.6; cross-ref reference/dsp_kernel_patterns_manifest.md section K7] | RT kernel patrol | drain | first trip per session → `EV_FP_PATROL`; afterwards count-only |
| `ct_guard` — RT-guard trips (dev builds) | RT guard [cross-ref reference/rt_plane_rules_manifest.md section R4] | drain, test harness | every trip → `EV_GUARD_TRIP`; in dev/CI a trip fails the run *(host-test-catchable by design)* |
| `ct_rung_enter[5]`, `ct_rung_exit[5]` — degrade ladder [ESTABLISHED: booklet section 12.2] | rung owner [OPEN — NEEDS-INPUT: per-rung ownership map (RT-local for shed/steal/bypass vs control for tier swap) is a product decision recorded in config] | drain, UI | every change → `EV_RUNG_ENTER`/`EV_RUNG_EXIT` (`PK_RUNG` carries headroom permille) |
| `ct_blocks` — heartbeat block counter | RT adapter loop (via seqlock, O6) | supervisor | stall → O6 ladder |
| `ct_cb_max_ns`, `ct_gap_max_ns` | RT adapter loop | drain | new max ≥ 90% of budget → `EV_BUDGET_NEAR` [OPEN — ASSUMED: 90% threshold] |
| `g_headroom` gauge — smoothed cost-over-budget, published via channel (e) | RT adapter loop | degrade ladder, UI | threshold crossings surface as `EV_RUNG_*` via the ladder [ESTABLISHED: booklet section 13.2] |

RULES:
- One writer per counter, period; two modules that both want to count the same thing get two counters, summed by the drain. *(host-test-catchable: TSan, Linux leg)*
- Counters are never reset while the stream runs (O4 semantics apply). *(contract-only + host-test-catchable)*
- Threshold-to-event conversion happens in the drain or the owning plane's cheap compare — never a syscall, never formatting on RT. *(runtime-catchable: R4 guard)*
- Every counter appears in the session report by its canonical name above; renaming is expand/contract [cross-ref O8]. *(build-catchable: schema validation, G2 check.sh)*

## O6. Heartbeat and supervisor

The watchdog translated to this platform: a control-plane supervisor of the RT plane's *progress* [ESTABLISHED: booklet section 12.6].

- **Heartbeat = progress, not existence.** The device loop publishes `{ct_blocks, stream_state, last_cb_mono_ns, stream_pos}` through the seqlock surface (channel (e)) once per block — the counter only advances when blocks actually render [ESTABLISHED: booklet sections 12.6, 6.3(e); impl cross-ref reference/concurrency_channels_manifest.md section C5].
- **Supervisor cadence.** A control-plane timer consumer checks every 100 ms; *stall suspected* when `stream_state == live` and `ct_blocks` unchanged for `max(8 × period, 250 ms)`; *stall declared* on the second consecutive suspect check [OPEN — ASSUMED: all three numbers; record the product's values]. False-positive guard: device-paused and drain-stopped states are legal non-progress, encoded in `stream_state`.
- **Response ladder** — pointer, not restatement: booklet section 12.6's escalating restart, scoped to restartable units: (0) capture diagnosis, (1) tear down and rebuild the stream, (2) rebuild the engine, (3) where the product splits processes, let the engine process die and be respawned. Rebuild verbs live with the adapters [cross-ref reference/device_adapter_manifest.md sections D4, D7]; teardown ordering is C9's [cross-ref reference/concurrency_channels_manifest.md section C9]; process respawn posture is a product-level row [ESTABLISHED: booklet section 12.6].
- **Escalation events.** Every rung stamps its event **before** acting — `EV_WD_STALL_SUSPECT` → `EV_WD_STREAM_RESTART` → `EV_WD_ENGINE_RESTART` → `EV_WD_PROC_KILL` — so the supervisor's kill is readable in the next session's harvest [ESTABLISHED: booklet section 12.6 — "every rung leaves its story in the flight ring first"; harvest cross-ref reference/error_tracing_contract_manifest.md section E9]. Dwell before escalating to the next rung: one retry within 5 s [OPEN — ASSUMED].

### Supervisor states

| state | entered when | action | event |
|---|---|---|---|
| OK | progress within window | none | — |
| SUSPECT | `stream_state == live` and `ct_blocks` static past threshold | snapshot heartbeat + headroom gauge; re-check next tick | `EV_WD_STALL_SUSPECT` |
| DECLARED | second consecutive SUSPECT | run the ladder rung by rung, each stamped before acting | `EV_WD_STREAM_RESTART` → `EV_WD_ENGINE_RESTART` → `EV_WD_PROC_KILL` |
| RECOVERED | progress resumes before the next rung fires | count it, return to OK | `EV_WD_RECOVERED` |

[OPEN — ASSUMED: two-check confirmation; a single-check declaration is a legitimate product choice at short periods — record it.]

RULE: the supervisor runs on the control plane and never touches RT state directly — it acts through the same channels and shutdown protocol as any other control code. *(host-test-catchable: T6 fault injection freezes the fake clock / wedges a fake callback and asserts detection latency and ladder order — cross-ref reference/testing_verification_manifest.md section T6)*

RULE: a stall during diagnosis mode first triggers capture (O9's `EV_DIAG_MARK` + external-tracer window) before rung 1, so the evidence survives the restart. *(runtime-catchable)*

## O7. Session report generation

Every run can end in an artifact; the report is the package's primary failure artifact and the agent's patch input [ESTABLISHED: booklet section 13.3].

### Triggers

| trigger | mechanism | tag |
|---|---|---|
| normal exit | built during C9 shutdown, after the RT plane stops and the final drain sweep completes | [ESTABLISHED: booklet section 13.3 — "written on exit"] |
| on demand | maintenance surface request (read-only member); also the diagnosis workflow's snapshot | [ESTABLISHED: booklet section 13.5]; surface authorization is a product row [OPEN — NEEDS-INPUT] |
| dirty exit | **next start** detects the dirty marker, harvests the previous ring tail + counters from the persisted region/dump, emits `EV_DIRTY_EXIT_HARVEST` as the new session's first event, and attaches the harvest to the new report | [ESTABLISHED: booklet section 13.4]; harvest mechanics owned by reference/error_tracing_contract_manifest.md section E9 |
| periodic checkpoint | diagnosis mode only | [OPEN — ASSUMED: off otherwise] |

### Builder rules

- Control plane only, from drained copies (O3 event log, O4 snapshots, O5 counters) — the builder never reads RT-owned memory while the plane runs. *(runtime-catchable: R4 guard in dev; host-test-catchable ordering test)*
- **MUST conform to config/session_report.schema.json.** Field names and semantics are owned by reference/error_tracing_contract_manifest.md section E8; this section owns only *when* and *from what sources*. Content groups: identity (build id, schema version, session id, OS, machine class), negotiated format (device, rate, period, channels), histograms with the O4 bin map, all O5 counters by canonical name, the bounded event history, xrun records with autopsy attachments, degrade history, exit disposition [ESTABLISHED: booklet section 13.3]. *(host-test-catchable: T-suite validates every generated report against the schema; build-catchable: config/check.sh runs the same validation — cross-ref reference/quality_gates_ci_manifest.md section G2)*
- **Build identity stamping**: the report's build id MUST equal the id embedded in the binary [ESTABLISHED: booklet invariant 17, quoted at section 13.3; embedding owned by reference/toolchain_build_manifest.md section B10]. A report without a build id is not evidence — reject it in tooling. *(build-catchable: schema marks the field required)*
- Atomic write: serialize to `report.json.tmp`, flush, rename over the target (`rename` same-directory atomicity on POSIX; `MoveFileExW` + `MOVEFILE_REPLACE_EXISTING` on NT) [CC-FACT — verify against MS docs for ReplaceFile vs MoveFileEx if crash-during-write matters]. *(host-test-catchable: kill-during-write test yields either old or new report, never a torn one)*
- Clock anchoring: events carry monotonic time only; the report records one `(t_mono_ns, t_wall_iso8601)` anchor pair captured at session start on the control plane so postmortem tooling can place events in calendar time without ever putting wall clock in events [ESTABLISHED: booklet section 7.1 posture] [OPEN — ASSUMED: single anchor, no re-anchoring in r1].
- Privacy posture: the report never carries audio, content identifiers, or user paths [ESTABLISHED: booklet section 13.3 — "nothing in the report identifies content"]; fleet upload is opt-in and explicit [OPEN — NEEDS-INPUT: product telemetry policy]. *(contract-only + review)*

### Consumers — deliberately one format

User bug report (attach the file) · soak-rig evidence (the gate asserts on exactly these fields — cross-ref reference/quality_gates_ci_manifest.md section G7) · fleet view where opted in [ESTABLISHED: booklet section 13.3]. The **replay dividend**: recorded command-ring traffic + the event stream are a complete reproduction recipe for the deterministic core — the offline harness re-renders the session's decision path bit-exactly [ESTABLISHED: booklet section 13.3; harness cross-ref reference/testing_verification_manifest.md section T3]. Reading a report is a card task [cross-ref cards/diagnose-failure.md; reference/testing_verification_manifest.md section T13].

## O8. Control-plane logging

The control plane logs like ordinary software — structured, leveled, rotated, boring [ESTABLISHED: booklet section 13.5]. The format below is this file's contract because the primary reader is a parser (the agent, CI, report tooling), not a human tailing a terminal.

### Line grammar — package contract

One event per line, UTF-8, `key=value` fields, space-separated, values with spaces double-quoted with backslash escapes. The first five keys are fixed, in order [OPEN — ASSUMED: this file owns the grammar; changes are expand/contract]:

```
t=2026-08-12T14:03:22.117Z mono=8123456789012 lvl=warn mod=dev.wasapi ev=0x0102 err=0x2103 msg="device invalidated" action=rebuild
```

| field | meaning | rule |
|---|---|---|
| `t` | wall clock, ISO-8601 UTC, ms, `Z` | display/join only; never used for ordering (mono orders) [ESTABLISHED: booklet section 7.1] |
| `mono` | `t_mono_ns` at log call | the join key to flight events and external traces |
| `lvl` | trace/debug/info/warn/error/fatal | same enum as O2 severity — one vocabulary |
| `mod` | dotted lowercase module | matches the id-registry module map (O2) |
| `ev` | event id `0xNNNN` from the registry | mandatory; free-form dev lines use `EV_ADHOC` (0x08FF), which is forbidden in ship builds *(build-catchable: G3 grep)* |
| `err=` | E3 error code when the line reports an error | joins the E7 evidence chain [cross-ref reference/error_tracing_contract_manifest.md sections E3, E7] |

First line of every log file: `ev=EV_SESSION_START` with `fmt=1 build=<id> session=<id>` — the file is self-locating without external context. *(host-test-catchable: golden log-line test pins the grammar; cross-ref reference/testing_verification_manifest.md section T4)*

### Rules

| rule | statement | route |
|---|---|---|
| never on RT | no logging entry point is callable from RT TUs — events only (P1); log lines about RT facts are the drain's projection of severity ≥ warn events (O3) | compiler-catchable (poison) + runtime-catchable (R4 guard) |
| log-once-at-boundary | an error is logged exactly once, at the boundary that converts or handles it; inner layers attach context to the error value, not extra log lines — no catch-log-rethrow towers producing N copies of one event | contract-only (review row in cards/review-code.md; dispositions and message contract owned by reference/error_tracing_contract_manifest.md sections E2, E6) |
| no secrets, no PII | never audio samples, content titles, user filenames (basename/hash redaction policy [OPEN — NEEDS-INPUT]), credentials, or machine identifiers beyond the machine-class string [ESTABLISHED: booklet section 13.5 hygiene + 13.3 privacy posture] | contract-only + review; grep-assisted audit for known sink calls (G3) |
| rotation | size-based: 8 MiB per file, keep 4, rotate on open and on size [OPEN — ASSUMED]; location per-OS app-data dir [OPEN — NEEDS-INPUT] | host-test-catchable (rotation unit test) |
| stable format = versioned contract | parsers key on `fmt=`; schema evolution is expand/contract — add keys freely, never rename/retype the fixed five; retired `ev` ids stay reserved [ESTABLISHED: booklet section 13.5] | build-catchable (golden log-line test + G3 table diff) |
| one vocabulary | the same event id names the flight event, the log line, and the report entry — grep any one id across all three artifacts and the story lines up | host-test-catchable (T13 exercises the join) |

### Worked micro-example — one xrun, three artifacts, one grep

1. RT emit at the deadline miss: `fr_emit(ring, EV_XRUN, FR_PK(FR_ERROR, PK_XRUN), pos, /*class*/ 1, gap_ns, dur_ns, 0)`.
2. Drain projection (error ≥ warn): `t=... mono=8123456789012 lvl=error mod=deadline ev=0x0201 class=late_wakeup gap_ns=2210000 dur_ns=410000`.
3. Report: an `events[]` entry (same mono, same id), `ct_xrun[1]` bumped, wakeup-gap histogram grown by one in bin 12.
4. The agent greps `ev=0x0201` across log and report. WHAT = xrun, late-wakeup class (id + class word). WHERE = module 0x02, deadline plane, at `stream_pos`. WHY = gap 2.21 ms against a 2.67 ms period with duration quiet and fault counters at zero → OS scheduling latency, so route to elevation/placement checks [cross-ref reference/optimization_microarch_manifest.md section P9; privilege conventions - hub H7] — no rerun needed. Deeper worked examples: reference/error_tracing_contract_manifest.md section E10; artifact reading order: reference/testing_verification_manifest.md section T13.

## O9. Diagnosis mode

The autopsy's armed layers, operationalized [ESTABLISHED: booklet section 11.5]. Ship default: **off**; when off the RT cost is one relaxed load and one predicted branch per block — measured-negligible by the bench lane *(target-test-catchable)*. Arming is a control command through channel (a) (atomic flag; cross-ref reference/concurrency_channels_manifest.md section C6), stamped as `EV_DIAG_ARMED`/`EV_DIAG_DISARMED`. Optional compile-out for hardened ship variants [OPEN — ASSUMED: r1 keeps runtime-armable ship builds, per booklet section 11.5 "build/runtime flag"].

### Layer 1 — per-callback deltas, on-plane at block edges

When armed, the RT thread samples cheap OS counters at block start and end, computes integer deltas, and emits one event — no alloc, no lock, no formatting; the added syscalls are the armed mode's declared exception, whitelisted by the guard only while armed [cross-ref reference/rt_plane_rules_manifest.md sections R4, R7]. *(runtime-catchable: guard traps these calls when unarmed)*

| leg | call | fields used | caveat |
|---|---|---|---|
| Linux | `getrusage(RUSAGE_THREAD, &ru)` [CC-FACT] | `ru_minflt`, `ru_majflt`, `ru_nvcsw`, `ru_nivcsw` | `RUSAGE_THREAD` is a Linux extension; it is a real syscall — armed mode only [CC-FACT; verify: man getrusage(2)] |
| NT | `QueryThreadCycleTime(GetCurrentThread(), &cycles)` [CC-FACT] | cycles consumed by the thread | cycles, not ns; the ratio of cycle delta to QPC-elapsed exposes preemption (ratio well below 1.0 = the thread was off-core) [CC-FACT] |
| NT | `GetProcessMemoryInfo(...)` → `PROCESS_MEMORY_COUNTERS.PageFaultCount` [CC-FACT] | page-fault count | **process-wide, not per-thread** — attribute with care; link psapi or use the `K32`-prefixed kernel32 export [CC-FACT; verify: MS docs "GetProcessMemoryInfo"] |
| NT | (no per-thread involuntary-context-switch counter in Win32) [CC-FACT] | — | context-switch attribution on NT needs the ETW capture below |

```c
/* RT plane, armed only. Raw block-edge sample; the caller subtracts the
   block-start sample per field, then packs the DELTAS into EV_CB_DELTAS
   payload words (per-leg kinds in O2). No alloc, no lock, no formatting. */
typedef struct diag_raw { uint64_t a, b, c, d; } diag_raw;

#if defined(__linux__)
#include <sys/resource.h>
static inline diag_raw diag_sample(void)   /* a=minflt b=majflt c=nvcsw d=nivcsw */
{
    struct rusage ru;
    getrusage(RUSAGE_THREAD, &ru);                                /* [CC-FACT] */
    return (diag_raw){ (uint64_t)ru.ru_minflt, (uint64_t)ru.ru_majflt,
                       (uint64_t)ru.ru_nvcsw,  (uint64_t)ru.ru_nivcsw };
}
#else
#include <windows.h>
#include <psapi.h>
static inline diag_raw diag_sample(void)   /* a=proc page faults, d=thread cycles */
{
    PROCESS_MEMORY_COUNTERS pmc = { .cb = sizeof(pmc) };
    ULONG64 cyc = 0;
    QueryThreadCycleTime(GetCurrentThread(), &cyc);               /* [CC-FACT] */
    GetProcessMemoryInfo(GetCurrentProcess(), &pmc, sizeof(pmc)); /* [CC-FACT] */
    return (diag_raw){ pmc.PageFaultCount, 0, 0, cyc };
}
#endif
```

The NT branch compiles, links with `-lpsapi`, and runs on this machine — `QueryThreadCycleTime` and `GetProcessMemoryInfo` resolve [MEASURED 2026-08-12: snippet compile check, CLANG64 clang 22.1.8]; the Linux branch is [CC-FACT] until the Linux-leg CI compiles it.

Emitted as `EV_CB_DELTAS`, one per block in diagnosis mode; the soak rig runs this layer armed always but emits only anomalous blocks plus a 1 Hz summary [ESTABLISHED: booklet section 11.5 — soak runs layer 1 always; emission policy OPEN — ASSUMED]. Payload packing (per-leg kinds): `PK_CB_DELTAS_POSIX` w0=gap_ns, w1=dur_ns, w2=(minflt<<32)|majflt, w3=(nvcsw<<32)|nivcsw (saturating u32 halves); `PK_CB_DELTAS_NT` w0=gap_ns, w1=dur_ns, w2=process page-fault delta, w3=thread cycle delta.

### Classification — the taxonomy decided at the block edge

Evaluate top-to-bottom; a nonzero `majflt` or `nivcsw` takes precedence over gap alone (per error_tracing_contract_manifest.md E10c) unless gap growth dominates by a stated margin [OPEN: NEEDS-INPUT — the margin].

| signature in the deltas | class [ESTABLISHED: booklet sections 11.5, 2.4] |
|---|---|
| involuntary switches or major faults mid-work | external stall |
| gap grew, duration normal, counters quiet | late wakeup |
| duration grew, counters quiet | self-overrun |
| adapter error verbs, not timing | device fault [cross-ref reference/device_adapter_manifest.md section D8] |
| unattributed gap, nothing moved | irreducible residue (SMI-class); named honestly, never guessed [ESTABLISHED: booklet section 11.5]; dedicated-rig SMI tracer is a hub row [VERSION-DEPENDENT - hub H4] |

The classification word lands in `EV_XRUN`'s payload (`PK_XRUN` w0) so the field report carries its own diagnosis [ESTABLISHED: booklet section 11.5].

### Layer 2 — system tracers, off-plane, external commands

The OS's scheduler's-eye view, captured by the operator or a control-plane helper during a diagnosis session; these tools stay **outside the product** [ESTABLISHED: booklet section 13.5]. All commands [CC-FACT] — verify flags on the machine before scripting them; availability is a hub fact [VERSION-DEPENDENT - hub H4 (Linux), hub H2 (Windows)].

Linux (perf):

```
perf sched record -k CLOCK_MONOTONIC -a -- sleep 10   # verify -k: perf record --help | grep -i clockid
perf sched latency --sort max                          # worst scheduling delays per task
perf sched timehist                                    # per-wakeup timeline
```

`-k CLOCK_MONOTONIC` makes perf timestamps the same timebase as `t_mono_ns` — direct correlation, no offset solving [CC-FACT].

Windows (WPR/xperf, ADK):

```
wpr -start CPU -filemode          # verify profile name: wpr -profiles
<reproduce the glitch>
wpr -stop rt_diag.etl
```

xperf alternative with ready-thread stacks: `xperf -on PROC_THREAD+LOADER+PROFILE+CSWITCH+DISPATCHER -stackwalk CSwitch+ReadyThread -f kernel.etl` then `xperf -stop -d rt_diag.etl` [CC-FACT; verify kernel flags: `xperf -providers k`]. Analyze in WPA: "CPU Usage (Precise)" is the context-switch view; filter to the RT thread id and read Ready/Waits columns [CC-FACT]. ETW timestamps default to QPC — the same source as `t_mono_ns` on NT [CC-FACT; verify in trace properties].

### Correlation protocol

1. Arm diagnosis; the toggle emits `EV_DIAG_MARK` with the capture tool named in payload w0 (registry-coded), giving both artifacts a shared fence post.
2. Reproduce; layer-1 deltas and any xruns land in the ring with `t_mono_ns`.
3. Stop capture; the drain stamps a closing `EV_DIAG_MARK`.
4. Join: filter the OS trace to the window between the two marks, align by monotonic/QPC time, and attribute each anomalous block edge to a scheduler event ("which driver's interrupt storm ate my period" is answered in the OS's evidence, not the program's guess) [ESTABLISHED: booklet section 11.5].
5. Attach findings to the xrun's flight-ring event; the session report then carries the diagnosis as far as the platform allowed [ESTABLISHED: booklet section 11.5].

RULE: diagnosis mode adds counters and events only — it never changes RT-plane control flow, buffer sizes, or scheduling, so the observed system is the shipped system (the placement/elevation knobs live elsewhere [cross-ref reference/optimization_microarch_manifest.md section P9]). *(contract-only + bench-lane check that armed-vs-off deltas stay within noise, target-test-catchable)*

RULE: when off, zero RT cost beyond the single flag load; the guard asserts no diagnosis syscalls occur unarmed. *(runtime-catchable in dev; target-test-catchable in soak)*
