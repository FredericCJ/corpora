# Card: device adapters

**Both OSes implement one port: core-owned vocabulary (frames, channels, formats), a paced loop that blocks only on the device's signal, three fault verbs with designed recoveries.**

Facts verified 2026-08-12. Version-dependent claims route to reference/audio_platform_baseline_manifest.md (the hub); if any file disagrees with the hub, the hub wins.
Reasoning root: the child booklet `realtime-audio-pc-architecture-and-design-r1.md` (repo root). This card operationalizes it; it never re-argues it.

**Load when:** writing or touching ALSA/WASAPI adapter code, device negotiation, stream fault handling, or the paced loop.
**Depth:** reference/device_adapter_manifest.md. The loop is RT-plane code: cards/write-rt-code.md. Fault → error conversion: cards/handle-errors.md.

## The standard this card serves

**The audio-device port is the only place the two operating systems may look different — and its signatures never mention handles, events, HRESULTs, or errno** [ESTABLISHED: booklet section 5.2].

## The port contract (D1 condensed)

| clause | contract |
|---|---|
| negotiation (root only) | request rate/format/channels/period; receive the grant, which may differ; **the grant is final for the stream's life**; every downstream size derives from it [ESTABLISHED: booklet sections 4.5, 5.2] |
| the paced loop (RT) | the adapter owns the RT thread and the loop: *block on the device signal → wake → obtain the period's buffers → call the render entry with exactly the frames demanded + paired (device-position, monotonic) timestamps → submit → repeat*; the render entry is the plane's single doorway and the deadline monitor wraps it [ESTABLISHED: booklet section 5.2; ch. 3 invariant 5] |
| fault verbs | `underrun-recovered` (counted, stream continues), `device-lost`, `format-invalidated` — each an event to the control plane, each with a designed recovery, none a surprise [ESTABLISHED: booklet section 5.2; ch. 3 invariant 19] |
| format boundary | core is 32-bit float, deinterleaved planes; any conversion to a non-native grant is adapter work at the boundary, never kernel work [ESTABLISHED: booklet sections 5.2, 9.1] |

## Per-leg recipes — where to copy from

| leg | do | depth |
|---|---|---|
| ALSA setup | configure hw params + sw params to the grant; device selection (`hw:` direct vs mixer/server route) is product configuration, not adapter opinion [ESTABLISHED: booklet section 5.2] | reference/device_adapter_manifest.md section D2 |
| ALSA paced loop | block per period on the poll descriptors or the blocking write path; recover documented error states through fault verbs — never leak errno upward [ESTABLISHED: booklet section 5.2; ALSA docs are the external register] | reference/device_adapter_manifest.md section D3 |
| ALSA errors | underrun errno and suspend state → the recovery protocol → `underrun-recovered`; mmap transfer is a measured-only optimization row [ESTABLISHED: booklet sections 5.2, 10.7] | reference/device_adapter_manifest.md section D4 |
| WASAPI COM-in-C | see the discipline block below | reference/device_adapter_manifest.md section D5 |
| WASAPI setup | audio client in event-callback mode, waitable event per period; exclusive for low-latency products, shared for the compatible default — shared mode's engine period bounds the floor and negotiation surfaces that honestly [ESTABLISHED: booklet section 5.2] | reference/device_adapter_manifest.md section D6 |
| WASAPI loop + MMCSS | register the RT thread with MMCSS at thread start; device-invalidation notifications arrive on a control-plane thread and convert to fault verbs [ESTABLISHED: booklet section 5.2] | reference/device_adapter_manifest.md section D7 |

MMCSS row, verified: `AvSetMmThreadCharacteristicsW(L"Pro Audio", &idx)` with `-lavrt` returns a non-null handle (observed task index 418); `AvRevertMmThreadCharacteristics` works [MEASURED 2026-08-12]. Privilege conventions per leg (rtkit, limits, MMCSS): [VERSION-DEPENDENT - hub H7].

## The loop's per-wake obligations

The adapter owns the RT thread; at thread start it requests elevation + placement, registers MMCSS (Windows leg), sets FTZ/DAZ, and reports the grants — before the first wake [ESTABLISHED: booklet sections 5.2, 5.3; ch. 3 invariant 14]. Then, forever:

1. Block on the device's pacing signal — the plane's only sanctioned block [ESTABLISHED: booklet section 5.1].
2. Wake; obtain exactly the period's buffers.
3. Stamp the pair (device position, monotonic now) through the clock port — the drift estimator consumes pairs [ESTABLISHED: booklet section 5.2].
4. Call the render entry with exactly the frames demanded — the deadline monitor wraps this call; every callback's cost lands in the histogram [ESTABLISHED: booklet ch. 3 invariant 5].
5. Submit; any adapter-side conversion happens inside the measured window.
6. On a platform error: convert to a fault verb (matrix below); the loop never decides policy.

The loop body is RT-plane code and obeys cards/write-rt-code.md in full.

## COM discipline (the anti-corruption layer)

COM is confined *inside* the WASAPI adapter: initialized on threads the adapter owns, never visible in any port signature, refcounting wrapped so the core never learns Windows has objects [ESTABLISHED: booklet section 5.2]. Pure C works:

```c
#define COBJMACROS
#define CINTERFACE
#include <mmdeviceapi.h>
#include <audioclient.h>
/* IMMDeviceEnumerator_GetDefaultAudioEndpoint(enum_, eRender, eConsole, &dev)
   and IAudioClient3_GetSharedModeEnginePeriod(...) resolve as C macros. */
```

[MEASURED 2026-08-12: compiles on CLANG64 clang 22.1.8]. Rules: every `Release` paired and owned; COM init/teardown lifetime matches the owning thread; no COM on the device-loop's hot path beyond what the loop itself requires [CC-FACT — verify per-call threading rules against MS WASAPI docs; reference/device_adapter_manifest.md section D5 is normative].

## Fault verbs — conversion matrix (D8 condensed)

Adapters convert the platform's vocabulary to the port's verbs at the boundary; raw errno/HRESULT never crosses inward [ESTABLISHED: booklet section 12.1].

| platform condition | port verb | designed recovery |
|---|---|---|
| ALSA underrun (`-EPIPE` from the write/poll path) [CC-FACT: ALSA docs name it; verify in D4] | `underrun-recovered` | run the platform recovery protocol; first buffers after recovery **ramp in from silence**; count + flight-ring event with autopsy attachment [ESTABLISHED: booklet section 12.3] |
| ALSA suspend state [CC-FACT: verify in D4] | `underrun-recovered` or `device-lost` per outcome | resume protocol; escalate to `device-lost` if resume fails |
| device unplugged / claimed exclusively / server restarted | `device-lost` | stream safe state engages; control plane runs a **bounded, backed-off** reopen loop against the configured device, else the fallback-device policy; session untouched; user told immediately [ESTABLISHED: booklet section 12.4] |
| WASAPI `AUDCLNT_E_DEVICE_INVALIDATED` [CC-FACT: MS WASAPI docs name it; verify in D8] | `device-lost` | as above |
| OS/user changed rate or layout under the stream | `format-invalidated` | full renegotiation via the stop-and-restart tail: composition-root steps from negotiation onward re-run, graph recompiles, stream resumes [ESTABLISHED: booklet sections 6.8, 12.4] |

Repeated xruns are a *trend*: leaky-bucket escalation offering the honest trade (larger period, lighter session, diagnosis capture) — never silently grown hidden buffering [ESTABLISHED: booklet section 12.3].

## Negotiation and conversion (D9)

The grant may differ from the request. What the adapter converts (sample format, interleaving) versus what forces renegotiation (rate, channel count) is policy the product records — see the OPEN block. Interleave/deinterleave and sample-format conversion live only at the adapter; store-heavy by nature, they never enter `core/` [ESTABLISHED: booklet section 9.3].

## Fake-device parity

Every behavior above is scriptable in the fake device — period sequences (fixed, alternating, legal shared-mode jitter), grants including refusals and downgrades, all three fault verbs, pacing modes [ESTABLISHED: booklet section 14.2]. The real and fake adapters pass the **same contract suite**; fault cases run against the fake per commit, device-in-loop runs at the release rungs [ESTABLISHED: booklet sections 14.2, 14.6].

## Never

- Leak errno/HRESULT/COM types/handles past the port signature (route: build-catchable include+symbol audits; contract-only at signature review) [ESTABLISHED: booklet sections 5.2, 12.1].
- Resume after an underrun without ramping in from silence — a resume click is a second defect on top of the first [ESTABLISHED: booklet section 12.3].
- Unbounded or un-backed-off reopen loops after `device-lost` (route: host-test-catchable fault suite).
- Touch the session/edit model from adapter fault handling — it lives on the control plane by construction [ESTABLISHED: booklet section 12.4].
- Hide shared-mode's engine-period floor from the product [ESTABLISHED: booklet section 5.2].
- Include one leg's adapter from another (route: build-catchable — config/audit_includes.py) [ESTABLISHED: booklet section 15.3].
- Add vendor-SDK paths (ASIO) — excluded by licensing; the port is designed so a grandchild adds that adapter without touching core [ESTABLISHED: booklet section 5.2].
- Block anywhere in the loop except on the device's pacing signal [ESTABLISHED: booklet section 5.1].

## Decisions you must not invent

- Shared vs exclusive default (WASAPI) and `hw:` vs server route (ALSA) per product — [OPEN NEEDS-INPUT; booklet section 5.2].
- Accept-non-native-grant policy: which conversions the adapter performs vs which grants it refuses — [OPEN NEEDS-INPUT; reference/device_adapter_manifest.md section D9].
- Fallback-device policy on loss (which device, whether to auto-follow default) — [OPEN NEEDS-INPUT].
- Reopen backoff parameters (initial, ceiling, give-up) — [OPEN ASSUMED: bounded exponential; exact numbers product-pinned].
- mmap (ALSA) and exclusive/raw (WASAPI) modes — measured-only options, off until the bench protocol justifies them on the target rig [ESTABLISHED: booklet section 10.7] [OPEN ASSUMED: off].
- MMCSS task name — [OPEN ASSUMED: `Pro Audio`, the measured-working convention; revisit only with cause].

## What you owe when done

Per reference/testing_verification_manifest.md section T11: the **port contract suite** green against fake and (where available) real adapter; a **fault-injection row per verb** you touched — loss mid-block, format invalidation mid-session, underrun-recovery with ramp-in asserted; a **conversion-matrix row** for any new platform error you now map (and its registry code per reference/error_tracing_contract_manifest.md section E3); negotiation cases including refusal and downgrade. All wired through config/check.sh into the gate ledger reference/quality_gates_ci_manifest.md section G1. A fault-suite failure must name the verb, the injected condition, and the state-machine transition that misfired — self-locating, per the doctrine.

## Go deeper

| question | where |
|---|---|
| the port contract, normatively | reference/device_adapter_manifest.md section D1 |
| ALSA setup / loop / errors | reference/device_adapter_manifest.md sections D2, D3, D4 |
| WASAPI COM mechanics / setup / loop+MMCSS | reference/device_adapter_manifest.md sections D5, D6, D7 |
| the full fault-verb conversion matrix | reference/device_adapter_manifest.md section D8 |
| negotiation + conversion policy | reference/device_adapter_manifest.md section D9 |
| API baselines and privilege conventions | reference/audio_platform_baseline_manifest.md sections H6, H7 |
| contract suites + fault injection | reference/testing_verification_manifest.md section T6 |
| adapter error conversion tables | reference/error_tracing_contract_manifest.md section E5 |
