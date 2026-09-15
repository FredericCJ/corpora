# Card: handle errors

**Load when:** adding a fallible path, allocating an error code, writing a check, converting a
platform error at an adapter, or deciding what a fault does on the RT plane.
**Depth:** `reference/error_tracing_contract_manifest.md` (E1–E10) end to end. Diagnosing a failure
that already happened: `cards/diagnose-failure.md`. Per-device fault recovery:
`reference/device_adapter_manifest.md` sections D4, D8.

Facts verified 2026-08-12. Version-dependent claims route to
`reference/audio_platform_baseline_manifest.md` (the hub); if any file disagrees with the hub, the
hub wins. Reasoning root: the child booklet `realtime-audio-pc-architecture-and-design-r1.md`
(repo root) — operationalized here, never re-argued.

## The standard this card serves

Every failure travels a designed channel and leaves a machine-readable trace that names WHAT,
WHERE, WHY. Error paths are product paths: each one has a registry row, a conversion row if it
crosses a port, and a fault-suite test that reaches it. [ESTABLISHED: booklet sections 12.1, 14.4]

## The dispositions, per plane

[Table derives from booklet section 12.1; routes inline.]

| where the fault lands | disposition | mechanics | route |
|---|---|---|---|
| control plane | **return it, typed** | status-code result convention (E4); every fallible call checked or *visibly* discarded | compiler-catchable (`warn_unused_result` + the promoted warning canon, `reference/toolchain_build_manifest.md` section B3) |
| RT plane, expected fault | **absorb and mark — nothing else** | substitute the safe value (silence for a starved voice, clamp for an over), emit a fixed-size event into the flight ring, bump the counter, keep rendering. The mark IS the handling; absorbing with no record is try/continue with extra steps | runtime-catchable (counters are the witness) + host-test-catchable (fault suites, T6) |
| RT plane, contract violation, ship build | **stream safe state** | mark, fade, park the stream healthy; hand the control plane the evidence and the decision. Never abort mid-callback | runtime-catchable |
| RT plane, contract violation, dev/test build | **assert densely** | CHECK/ASSERT with the E6 message contract; break under debugger, fail the test otherwise | runtime-catchable (dev builds) |
| process-wide integrity indicted | **stop-the-world — a control-plane verb** | decided by the control plane holding the evidence; the stream is the restartable unit | runtime-catchable + contract-only (the criteria) |

Overload is not an error: it is expected-condition number one and runs the degrade ladder (entered
and exited on measured headroom, with hysteresis, every rung counted; terminal rung = ramped
silence, stream alive). [ESTABLISHED: booklet sections 12.2, 12.5] The ladder's rung policies are
product-recorded *(contract-only)*; the ladder's behavior is fault-injection-tested per commit
*(host-test-catchable, `reference/testing_verification_manifest.md` section T6)*.

## The code registry

Normative: `reference/error_tracing_contract_manifest.md` section E3.

- **Allocate a code = add one row in the ONE owner file** (`core/err_registry.def`, x-macro —
  rule E3-1): symbol, module, code number, disposition, owning reference section. One row per
  distinct condition; a row missing its reference pointer fails the audit (E3-3).
- **Never reuse, never renumber; retired ids stay reserved** with a `/* RETIRED */` row — every
  archived artifact carrying the code must stay greppable to its row forever. [ESTABLISHED:
  booklet section 13.5, the id-stability rule] *(build-catchable — the registry diff gate,
  `reference/quality_gates_ci_manifest.md` section G3)*
- **No bare numeric at the raise site** — the registry symbol is the greppable thread from
  artifact to row to handler. Error codes and flight-ring event ids are distinct id spaces
  sharing only the module-prefix convention and the generation tool; O2 owns the event-id side
  (E3-4).

## Result convention in C — the shape

```c
typedef int32_t ar_status;                 /* 0 = OK; nonzero = an E3 registry code   */
#define AR_MUST_USE __attribute__((warn_unused_result))

AR_MUST_USE ar_status ar_device_open(ar_device *d, const ar_device_cfg *cfg);

ar_status st = ar_device_open(&dev, &cfg);
if (st != 0) return st;                    /* raw propagation only inside a subsystem */

(void)ar_report_flush(rep);                /* discard is legal only when VISIBLE      */
```

Identifiers illustrative; the normative convention (names, ok-value, composition helpers) is
`reference/error_tracing_contract_manifest.md` section E4. [CC-FACT: clang diagnoses ignored
`warn_unused_result` returns; the warning canon promotes it to an error — C17 itself has no
`[[nodiscard]]`, that is C23.] *(compiler-catchable)*

## Conversion at the adapter — one vocabulary inward

The platform's error vocabulary (errno and negative returns on the ALSA leg, HRESULTs on the
WASAPI leg) converts to the codebase's fault verbs **at the port, never inward raw**. [ESTABLISHED:
booklet section 12.1] The full matrices are `reference/error_tracing_contract_manifest.md` section
E5 and `reference/device_adapter_manifest.md` section D8 — copy rows from there; two shape
examples:

| platform fact | port verb | adapter's move |
|---|---|---|
| ALSA write/read returns `-EPIPE` (xrun) [CC-FACT — verify against ALSA docs; matrix row in D8] | underrun-recovered | run the platform recovery protocol, ramp in from silence, emit event + classified counter |
| WASAPI returns `AUDCLNT_E_DEVICE_INVALIDATED` [CC-FACT — verify against MS WASAPI docs; matrix row in D8] | device-lost | stream safe state; control plane runs the bounded, backed-off reopen loop |

Both verbs are designed events with tested recovery paths (invariant 19) — injected through the
fake device per commit *(host-test-catchable, T6)*.

## RT-plane absorb-and-mark — the shape

```c
/* Output sentinel at the final bus (booklet section 12.5): containment, not tolerance. */
float s = bus[i];
if (!isfinite(s)) {                                     /* NaN/Inf must not reach ears */
    s = 0.0f;                                           /* safe value                  */
    ar_ring_emit2(rb, EV_SENTINEL_HIT, ch, i);          /* fixed-size event, no string */
    atomic_fetch_add_explicit(&ctr->sentinel, 1, memory_order_relaxed);
}
out[i] = (s > 1.0f) ? 1.0f : (s < -1.0f ? -1.0f : s);  /* clamp, branchless-lowering  */
```

Identifiers illustrative. A nonzero sentinel counter is a filed bug upstream by definition —
invariant 4 makes the intervention itself the defect report. [ESTABLISHED: booklet section 12.5]

## The check-message contract

Every check failure is **one machine-parseable `CHECK-FAIL` line, format v1**: `id=` (the E3
registry symbol), `file=`/`line=` repo-relative, `expr=`, `expected=`/`actual=`, `ctx=` (up to
three `key=val` pairs), `build=`. Marker and field order are frozen; RT-plane checks never
format — they emit a binary ring event the drain renders into the identical line (invariant 13,
rule E6-2). Anatomy with example: `cards/diagnose-failure.md`; normative grammar and rules:
`reference/error_tracing_contract_manifest.md` section E6. Dev asserts compile out of ship
builds; field checks survive and dispose per the registry — which flavor a new check gets is a
review question, not a habit (E6-3). *(runtime-catchable; the RT emission constraint
compiler-catchable via `config/rt_prelude_poison.h`)*

## Never

- Absorb without mark + count — on the RT plane the mark is the error handling. [ESTABLISHED:
  booklet section 12.1] *(runtime-catchable: fault suites assert the counter ticks)*
- Let errno/HRESULT vocabulary travel inward past the adapter. *(analysis-catchable: include/
  symbol audits keep OS headers out of core — invariant 8; plus review)*
- Reuse or renumber a registry code. *(build-catchable, G3 audit)*
- Format, log, or print an error on the RT plane — invariant 13; events only.
  *(compiler-catchable: `config/rt_prelude_poison.h`; runtime-catchable: the guard)*
- Abort the process from the RT plane in a ship build — the stream's safe state is the verb.
  *(runtime-catchable)*
- Parse error *text* anywhere — fields are the contract, the message is for humans. *(contract-only)*
- Swallow a fallible return without `(void)` + reason. *(compiler-catchable)*

## What you owe

Every new fallible path ships with: its registry row (E3) · its conversion row if it crosses a
port (E5/D8) · a fault-suite test that **reaches it** and asserts the disposition — the safe value,
the event, the counter (T6) · a self-locating failure artifact (E6 fields). Error paths are tested
like product paths; an untested error path is an untested product path. [ESTABLISHED: booklet
section 14.4]

## Decisions you must not invent

Code-number ranges and allocation authority per subsystem · the ship-build assert policy · degrade
ladder rung set, thresholds, and audibility ordering (product-recorded) · process-fatal criteria ·
fallback-device policy on device loss · user-facing error presentation.

## Go deeper

| question | where |
|---|---|
| the loop and the dispositions, argued | `reference/error_tracing_contract_manifest.md` sections E1, E2 |
| registry mechanics and allocation | `reference/error_tracing_contract_manifest.md` section E3 |
| result conventions, composition, visible discard | `reference/error_tracing_contract_manifest.md` section E4 |
| errno/HRESULT conversion matrices | `reference/error_tracing_contract_manifest.md` section E5; `reference/device_adapter_manifest.md` section D8 |
| check/assert message grammar | `reference/error_tracing_contract_manifest.md` section E6 |
| evidence chain and session report | `reference/error_tracing_contract_manifest.md` sections E7, E8 |
| crash capture, dirty-exit harvest | `reference/error_tracing_contract_manifest.md` section E9 |
| fault-injection suite rows | `reference/testing_verification_manifest.md` section T6 |
