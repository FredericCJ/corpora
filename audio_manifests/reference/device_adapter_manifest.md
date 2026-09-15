# Device Adapter Manifest — ALSA and WASAPI Behind One Audio Port

**Purpose.** The operational contract for the audio-device port and its two adapters: exact setup sequences, paced-loop shapes, error recovery, fault-verb conversion, and boundary format conversion — so the coding agent writes adapters that keep OS vocabulary out of the core and turn every native failure into a counted, self-locating port event.

Facts verified 2026-08-12. Version-dependent claims route to reference/audio_platform_baseline_manifest.md (the hub); if any file disagrees with the hub, the hub wins.

Reasoning root: the booklet `realtime-audio-pc-architecture-and-design-r1.md` (repo root). This file operationalizes booklet ch. 5 (ports), §2.4 (xrun taxonomy), §7.1 (the two clocks), §12.3–§12.4 (xrun lived through; device loss and format change). It never re-argues them.

**Tags.** [ESTABLISHED: source] · [VERSION-DEPENDENT — hub H\<n\>] · [MEASURED 2026-08-12] (ran on the reference machine, command recorded) · [OPEN — ASSUMED / NEEDS-INPUT] (project decision) · [CC-FACT] (model knowledge of API mechanics, no named primary source — verify pointer given) · [FLAGGED-SECONDARY] · [UNVERIFIED]. An untagged factual claim in this file is a defect.

**Deferred to siblings, not duplicated.** RT-plane bans, bounded-work, guard, syscall classes → reference/rt_plane_rules_manifest.md sections R2/R3/R4/R7. Channel selection for the timestamp/command paths → reference/concurrency_channels_manifest.md section C1; shutdown ordering → section C9. Error-code registry, C result type, check-message contract, evidence chain → reference/error_tracing_contract_manifest.md sections E3/E4/E6/E7. Event schema and counters canon → reference/observability_flightring_manifest.md sections O2/O5. Port contract suites and fault injection → reference/testing_verification_manifest.md section T6. Per-leg link rows and TU classes → reference/toolchain_build_manifest.md sections B1/B4. Entry card: cards/device-adapters.md; recovery decisions: cards/handle-errors.md.

---

## D1. The audio port contract

The prime port — the only place the two operating systems are allowed to look different [ESTABLISHED: booklet §5.2]. Its vocabulary is core-owned: frames, channels, sample formats — never handles, events, engine names, errno, or HRESULT [ESTABLISHED: booklet §5.2].

### The contract in six rows

| element | contract | source |
|---|---|---|
| **negotiation** | root-only, once per stream: request {rate, format, channels, period}; receive the **grant**, which may differ; **the grant is final for the stream's life** — any change is a stop-and-restart of the composition tail (concurrency C9), never an in-place mutation | [ESTABLISHED: booklet §5.2, §6.8] |
| **paced loop** | adapter owns the RT thread and the loop: *block on the device's pacing signal → wake → obtain the period's buffers → call the render entry with exactly the frames demanded → submit → repeat*. The wait is the **one sanctioned block** on the RT plane | [ESTABLISHED: booklet §5.1–5.2] |
| **render entry** | the RT plane's single doorway; deadline monitor wraps it (rt_plane_rules R4); called with `frames <= period_frames_max`, core handles any partition (dsp K2 partition invariance) | [ESTABLISHED: booklet §5.2, invariant 5] |
| **timestamps** | every wakeup captures the pair *(stream position, monotonic now)* — hardware-reported position where the API offers it, loop-counted where it does not — and publishes it to the control plane over a wait-free channel (concurrency C1) | [ESTABLISHED: booklet §7.1] |
| **fault verbs** | exactly three cross the port: `underrun-recovered` (counted, stream continues), `device-lost`, `format-invalidated`. Each is a control-plane event with a designed recovery (§D8); adding a fourth verb is a port-contract change | [ESTABLISHED: booklet §5.2, invariant 19] |
| **core format** | float32 deinterleaved planes, always; interleave and sample-format conversion happen **adapter-side only** (§D9) | [ESTABLISHED: booklet §5.2, §9.1] |

### Port surface shape (C)

Identifier spellings [OPEN — ASSUMED]; the shape is booklet §5.2's contract.

```c
/* ports/audio_device.h — core-owned. No OS header, handle, errno,
   or HRESULT may appear in this file. */
#include <stdint.h>

typedef struct adev_request {
    uint32_t rate_hz;             /* product rate; DT-1 sets period — booklet 2.5 */
    uint16_t channels_out, channels_in;
    uint32_t period_frames;
    uint32_t buffer_periods;      /* ALSA ring depth request, 2..3 — D2 */
} adev_request;

typedef struct adev_grant {       /* FINAL for the stream's life */
    uint32_t rate_hz;
    uint16_t channels_out, channels_in;
    uint32_t period_frames_max;   /* upper bound one wakeup may demand */
    uint32_t buffer_frames;
    uint8_t  wire_format;         /* ADEV_WIRE_* — logged, never seen by core */
} adev_grant;

typedef struct adev_stamp {       /* captured EVERY wakeup — booklet 7.1 */
    uint64_t stream_pos_frames;   /* device clock */
    uint64_t mono_ns;             /* machine clock, monotonic */
    uint32_t discontinuity;       /* nonzero on first wakeups after recovery */
} adev_stamp;

typedef void (*adev_render_fn)(void *ctx, float *const *out_planes,
                               const float *const *in_planes,
                               uint32_t frames, const adev_stamp *ts);
```

`discontinuity` is how the ramp-in rule travels: the adapter marks the first render after any recovery; the core's output stage applies the ramp (gain math stays in the core — dsp K3) [OPEN — ASSUMED mechanism; the rule itself is ESTABLISHED: booklet §12.3].

### Rules

| # | rule | route |
|---|---|---|
| D1-1 | no OS type crosses `ports/audio_device.h`; adapters include OS headers only under `adapters/alsa/`, `adapters/wasapi/` | analysis-catchable — config/audit_includes.py, wired per quality_gates G3 |
| D1-2 | grant immutable after go-live; adapter rejects mid-stream reconfiguration with a defect result (error E4) | host-test-catchable — T6 port contract suite |
| D1-3 | every wakeup that reaches the render decision publishes an `adev_stamp` before deciding how much to render; a spurious/error/timeout wakeup is counted instead (D3/D7 stall and fault counters), never silently dropped ("an xrun with no witness is a lie the system tells its own recorder") | host-test-catchable — T6 fake-device suite counts stamps vs wakeups [ESTABLISHED: booklet §2.4] |
| D1-4 | fault verbs are the only error vocabulary upward; native codes ride along as event *fields*, never as return values to the core | analysis-catchable (grep: no `errno.h`/`HRESULT` in core includes) + host-test-catchable (T6 fault injection) |
| D1-5 | the adapter's RT loop TU is an RT-class TU (build B1): compiled with config/rt_prelude_poison.h; setup/teardown live in a separate control-class TU | build-catchable — poison is a compile error [MEASURED 2026-08-12: `#pragma GCC poison malloc` → "attempt to use a poisoned identifier", clang 22.1.8 CLANG64] |
| D1-6 | both adapters pass the same contract suite; the fake device (offline harness, testing T3/T6) is the third adapter of this port | host-test-catchable [ESTABLISHED: booklet §5.1] |

### Thread-start prologue (both adapters, in order)

1. Elevation: MMCSS registration (Windows, §D7) / inherited SCHED_FIFO grant (Linux) — grant read back and **reported, not assumed** [ESTABLISHED: booklet §5.3, invariant 14]; conventions per hub H7.
2. FTZ/DAZ set on this thread (rt_plane_rules R5) [MEASURED 2026-08-12: `_MM_SET_FLUSH_ZERO_MODE` + `_MM_SET_DENORMALS_ZERO_MODE` → MXCSR=0x9fc0].
3. RT guard armed (rt_plane_rules R4); stack prefaulted (memory M7).
4. Only then: enter the paced loop.

### Never (both adapters)

- **Never call the render entry from any thread but the paced one.** It is the plane's single doorway [ESTABLISHED: booklet §5.2]. Route: host-test-catchable (T7 concurrency suite) + contract-only.
- **Never grow buffering silently to survive xruns** — "quietly growing hidden buffering until the product's stated latency is fiction" is the one forbidden response [ESTABLISHED: booklet §12.3]. Route: host-test-catchable — T6 asserts grant-latency invariance across recoveries.
- **Never let a native handle, event, or COM pointer appear in a port signature.** Route: analysis-catchable (D1-1 audit).
- **Never sleep, spin, or timer-wait instead of the device's own pacing signal** — the device wait is the only block (rt_plane_rules R2/R7). Route: runtime-catchable (guard R4).
- **Never recover before counting** — the pre-recovery state is the evidence (§D4). Route: host-test-catchable (D4-2).
- **Never do recovery work inside an OS notification callback** — post a command to the control plane (§D7). Route: contract-only, registered in rt_plane_rules R8.

### The same loop, twice — stage map

The normative loop realized per leg (details in D3/D7; native names [CC-FACT]):

| loop stage | ALSA | WASAPI |
|---|---|---|
| block | blocking `snd_pcm_writei`, or `poll` on PCM fds | `WaitForSingleObject` on the pacing event |
| frames demanded | granted period (multiples via `avail_update`) | `buffer_frames - padding` (shared) / full buffer (exclusive) |
| obtain | wire staging buffer, or `mmap_begin` areas | `GetBuffer` pointer |
| submit | `writei` return / `mmap_commit` | `ReleaseBuffer` |
| pair capture | `snd_pcm_htimestamp`, else loop count + `CLOCK_MONOTONIC` | `IAudioClock_GetPosition` (position + QPC) |
| xrun signal | `-EPIPE` return | **none** — detect via position discontinuity / missed event |
| device death | `-ENODEV` / `DISCONNECTED` state | `AUDCLNT_E_DEVICE_INVALIDATED` |
| suspend | `-ESTRPIPE` → resume protocol | surfaces as invalidation / notification, not a distinct code |

### Teardown order (voluntary stop; full protocol is concurrency C9)

| step | ALSA | WASAPI |
|---|---|---|
| 1. signal | stop flag + write shutdown eventfd (poll variant) | stop flag + `SetEvent` on the pacing event — we own the handle, the wait wakes [CC-FACT] |
| 2. fade | core ramps to silence first — a hard cut is a click (booklet §12.5) | same |
| 3. stop device | `snd_pcm_drain` (play out) or `snd_pcm_drop` (now) — voluntary stop drains, fault paths drop [OPEN — ASSUMED] | `IAudioClient_Stop` |
| 4. join | creator joins the paced thread — the join is the only proof the loop no longer touches the handle | same |
| 5. release | `snd_pcm_close` | `IAudioClient_Reset`, then Release per D5 table, reverse order; `CloseHandle` on the pacing event |

Release/close before the join is a use-after-free window: the paced thread may still be inside a device call it entered before observing stop.

Route for a teardown that can hang: host-test-catchable — the shutdown suite targets it by name [ESTABLISHED: booklet §6.8].

---

## D2. ALSA setup sequence

Control plane, composition root, once per stream. Nothing in this section is RT-safe (alsa-lib allocates internally during setup) [CC-FACT].

**Table-level tag, stated once:** every API name below is [CC-FACT] — alsa-lib spellings from model knowledge; verify against the alsa-lib PCM docs (alsa-project.org doxygen) on first use. alsa-lib version pinned at hub H4/H6 [VERSION-DEPENDENT — hub H6]. Policy cells cite the booklet.

### Call order (playback; capture mirrors with `SND_PCM_STREAM_CAPTURE`)

| # | call | purpose (one line) |
|---|---|---|
| 1 | `snd_pcm_open(&pcm, dev, SND_PCM_STREAM_PLAYBACK, 0)` | open PCM; `0` = blocking mode (writei variant), `SND_PCM_NONBLOCK` for the poll variant (D3) |
| 2 | `snd_pcm_hw_params_alloca(&hw)` | stack-allocate the hw-params container (setup thread only) |
| 3 | `snd_pcm_hw_params_any(pcm, hw)` | load the device's full configuration space |
| 4 | `snd_pcm_hw_params_set_access(pcm, hw, SND_PCM_ACCESS_RW_INTERLEAVED)` | transfer method; `SND_PCM_ACCESS_MMAP_INTERLEAVED` for the mmap optimization row (D3) |
| 5 | `snd_pcm_hw_params_set_format(pcm, hw, fmt)` | wire format from the D9 probe ladder (`SND_PCM_FORMAT_FLOAT_LE` → `S32_LE` → `S24_3LE` → `S16_LE`) |
| 6 | `snd_pcm_hw_params_set_rate(pcm, hw, rate, 0)` | **dir=0 demands the exact rate**; use `_set_rate_near` only if product policy accepts a neighboring rate — record which call was used in the grant |
| 7 | `snd_pcm_hw_params_set_channels(pcm, hw, ch)` | channel count |
| 8 | `snd_pcm_hw_params_set_period_size_near(pcm, hw, &period, &dir)` | wakeup quantum; `_near` because hardware constrains — read the result, it is the grant |
| 9 | `snd_pcm_hw_params_set_buffer_size_near(pcm, hw, &buf)` | total ring; request `2–3 × period` — 2 for the interactive tier, 3 as robust default [OPEN — ASSUMED split; the 2–3 band is ESTABLISHED: booklet §5.2 latency accounting] |
| 10 | `snd_pcm_hw_params(pcm, hw)` | commit to hardware — after this the grant is knowable |
| 11 | `snd_pcm_hw_params_get_rate/get_period_size/get_buffer_size` | **read back the grant**; never assume request == grant |
| 12 | `snd_pcm_sw_params_alloca(&sw)` + `snd_pcm_sw_params_current(pcm, sw)` | start sw params from the device's current set |
| 13 | `snd_pcm_sw_params_set_start_threshold(pcm, sw, buffer_frames)` | auto-start only when the ring is fully primed — prevents a start-instant xrun |
| 14 | `snd_pcm_sw_params_set_avail_min(pcm, sw, period_frames)` | wake granularity = one period; paces the loop |
| 15 | `snd_pcm_sw_params_set_tstamp_mode(pcm, sw, SND_PCM_TSTAMP_ENABLE)` + `snd_pcm_sw_params_set_tstamp_type(pcm, sw, SND_PCM_TSTAMP_TYPE_MONOTONIC)` | timestamps on, monotonic timebase — feeds the D1 pair via `snd_pcm_htimestamp` (D3) |
| 16 | `snd_pcm_sw_params(pcm, sw)` | commit sw params |
| 17 | `snd_pcm_prepare(pcm)` | reach PREPARED state |
| 18 | prime: write `buffer_frames` of silence (or the first rendered periods) | with step 13, the stream starts full |
| 19 | poll variant only: `snd_pcm_poll_descriptors_count/`, `snd_pcm_poll_descriptors(pcm, fds, n)` | export the fds the D3 poll loop blocks on |

Duplex: open capture and playback PCMs, then `snd_pcm_link(cap, pb)` so both start atomically on the start threshold [CC-FACT — verify alsa-lib docs].

### Device-string policy

| string | meaning | when |
|---|---|---|
| `hw:CARD,DEV` | direct hardware, no conversion layer — grant is the device's raw capability | exclusive low-latency product tier [ESTABLISHED: booklet §5.2] |
| `plughw:CARD,DEV` | alsa-lib plug layer converts format/rate in-process | compatibility middle ground; hidden copies — record the cost |
| `default` | system default route — usually a server (PipeWire/PulseAudio presenting as ALSA) | compatible default tier [ESTABLISHED: booklet §5.2] |

Which tier ships which string is **product configuration, not adapter logic** [ESTABLISHED: booklet §5.2] — the concrete default per product is [OPEN — NEEDS-INPUT].

### Rules

| # | rule | route |
|---|---|---|
| D2-1 | setup sequence runs before go-live only; any alsa-lib configuration call after go-live trips the guard | runtime-catchable — rt_plane_rules R4 |
| D2-2 | grant read-back (step 11) is mandatory; the recorded grant is emitted as the `adev.grant` negotiation event [OPEN — ASSUMED id; registry is observability O2] | host-test-catchable — T6 grants a divergent rate through the fake device |
| D2-3 | link row: `-lasound` on the Linux leg only [CC-FACT]; per-leg link table is build B4 | build-catchable |

---

## D3. ALSA paced loop

### Variant decision

| situation | loop variant | why |
|---|---|---|
| output-only, one device, simplest correct thing | blocking `snd_pcm_writei` | the write **is** the sanctioned block; least code |
| duplex, or shutdown must interrupt the wait, or >1 fd to watch | poll-descriptor loop | `poll()` multiplexes device fds + shutdown eventfd; readi/writei stay nonblocking |
| interleave/convert copy shows in the profile at small periods | mmap begin/commit | render straight into the DMA ring; one fewer copy — an optimization row, not a starting point [ESTABLISHED: booklet §5.2, §10.7]; climb the ladder first (optimization P1) |

All three are the same port; the variant is adapter-internal [ESTABLISHED: booklet §5.2].

### Blocking writei loop (reference shape)

```c
for (;;) {
    if (atomic_load_explicit(&ad->stop, memory_order_acquire)) break;  /* C9 */
    adev_render_to_planes(ad, g->period_frames);        /* core render, f32 planes */
    adev_convert_interleave(ad, ad->wire, g->period_frames);           /* D9 */
    snd_pcm_sframes_t n = snd_pcm_writei(pcm, ad->wire, g->period_frames);
    if (n < 0) { if (!adev_alsa_recover(ad, (int)n)) break; continue; }  /* D4 */
    if ((snd_pcm_uframes_t)n != g->period_frames)
        adev_count(ad, CTR_ADEV_SHORT_WRITE);           /* short write: counted */
    adev_publish_stamp(ad);                             /* pair via htimestamp */
}
```

`snd_pcm_writei` in blocking mode returns only when all frames are queued or on error [CC-FACT — verify alsa-lib docs]. Render-then-block ordering is correct here: the block lives in the submit.

### Poll-descriptor loop

```c
struct pollfd fds[ADEV_MAX_PFDS + 1];
int n = snd_pcm_poll_descriptors_count(pcm);
snd_pcm_poll_descriptors(pcm, fds, (unsigned)n);
fds[n] = (struct pollfd){ .fd = ad->shutdown_fd, .events = POLLIN };

for (;;) {
    int pr = poll(fds, (nfds_t)(n + 1), ad->wait_timeout_ms);    /* the sanctioned block */
    if (pr == 0) { adev_count(ad, CTR_ADEV_STALL); if (adev_alsa_stalled(ad)) break; continue; }   /* timeout: D8 stall row */
    if (pr < 0) continue;                       /* EINTR: counted, retry the wait */
    if (fds[n].revents) break;                          /* shutdown — C9 */
    unsigned short rev = 0;
    snd_pcm_poll_descriptors_revents(pcm, fds, (unsigned)n, &rev);
    if (rev & POLLERR) { if (!adev_alsa_recover_state(ad)) break; continue; }
    if (!(rev & POLLOUT)) continue;                     /* spurious wake */
    adev_publish_stamp(ad);                             /* pair via htimestamp — every pacing wakeup, before the render decision */
    snd_pcm_sframes_t avail = snd_pcm_avail_update(pcm);
    if (avail < 0) { if (!adev_alsa_recover(ad, (int)avail)) break; continue; }
    while (avail >= (snd_pcm_sframes_t)g->period_frames) {
        adev_render_convert_write(ad, g->period_frames);
        avail -= g->period_frames;
    }
}
```

`snd_pcm_poll_descriptors_revents` is mandatory — raw `revents` from ALSA fds are encoded and must be demangled through it [CC-FACT — verify alsa-lib docs]. `poll` timeout: `2 × period_ms + 10` [OPEN — ASSUMED]; a timeout (`pr == 0`, checked before the revents demangle) feeds the stall counter (D8) and the heartbeat (observability O6).

### mmap variant (optimization row)

`snd_pcm_avail_update` → `snd_pcm_mmap_begin(pcm, &areas, &offset, &frames)` → convert f32 planes directly into `areas[ch]` at `offset` → `snd_pcm_mmap_commit(pcm, offset, frames)` [CC-FACT — verify alsa-lib docs]. Commit fewer frames than begin granted only on fault. Entry criterion: the interleave copy is visible in the bench lane (testing T10) at the product's smallest period; exit criterion: same goldens byte-exact (quality G6).

### Duplex ordering

One paced loop, capture leads: linked PCMs (D2) start together; per iteration *block until a capture period is readable → `snd_pcm_readi` (or capture mmap) → convert to input planes → render → convert → `snd_pcm_writei`* — the capture side paces, the playback side follows within the same wakeup [CC-FACT — standard alsa-lib duplex shape; verify against alsa-lib PCM docs]. Rules that follow:

| # | rule | route |
|---|---|---|
| D3-D1 | one wait per iteration even in duplex — block on capture availability; never block twice (once per direction) in one pass | host-test-catchable — T6 duplex timing test |
| D3-D2 | input and output xruns are counted separately (overrun vs underrun — booklet §2.4's two directions of the same failed transaction) | host-test-catchable — T6 |
| D3-D3 | capture/playback grant mismatch (different granted periods) is a negotiation failure at the root, not something the loop papers over | host-test-catchable — T6 [ESTABLISHED: booklet §5.2 grant honesty] |

### Timestamps

`snd_pcm_htimestamp(pcm, &avail, &tstamp)` returns available frames plus the timestamp of that snapshot; with step 15 of D2 the timestamp is machine-monotonic, and stream position derives from the running frame count vs `avail` [CC-FACT — verify alsa-lib docs]. Where the driver reports garbage timestamps, fall back to loop-counted position + `clock_gettime(CLOCK_MONOTONIC)` — the booklet sanctions loop-counted position explicitly [ESTABLISHED: booklet §7.1].

### Rules

| # | rule | route |
|---|---|---|
| D3-1 | exactly one block per iteration (the write or the poll); everything else bounded compute — the pacing syscalls are the sanctioned rows of rt_plane_rules R7 | runtime-catchable (guard R4) + contract-only for the classification itself |
| D3-2 | shutdown interrupts the wait (eventfd row in poll variant; `snd_pcm_drop` + stop flag for writei variant) — a teardown that can hang is a designed defect class | host-test-catchable — shutdown tests, concurrency C9 [ESTABLISHED: booklet §6.8] |
| D3-3 | never call `snd_pcm_avail_update` in a spin to "poll harder"; the wait is the wait | contract-only — review, cards/write-rt-code.md |

---

## D4. ALSA errors + recovery

Count and classify **before** recovering: the event with its native code is the evidence; recovery destroys the state that explains it [ESTABLISHED: booklet §2.4 — every xrun counted, classified, stamped].

### Return-code table (from `writei`/`readi`/`avail_update`/`poll` demangle)

Native codes [CC-FACT — alsa-lib returns negative errno; verify per call in alsa-lib docs]. Verbs and owners: §D8.

| native | meaning | in-adapter recovery | port verb |
|---|---|---|---|
| `-EPIPE` | xrun (underrun on playback, overrun on capture) | `snd_pcm_prepare` → re-prime ring → mark `discontinuity` | `underrun-recovered` |
| `-ESTRPIPE` | stream suspended (system sleep) | `snd_pcm_resume` loop while it returns `-EAGAIN`, bounded; on success, continue (ring preserved — no prepare, no re-prime); on resume failure `snd_pcm_prepare` → re-prime; on exhaustion → escalate | `underrun-recovered` if resumed; `device-lost` if not |
| `-EBADFD` | PCM in wrong state — adapter state-machine defect | none in-loop; debug builds assert (error E6) | `device-lost` (release build) |
| `-ENODEV` / `-ENOTTY` / state `SND_PCM_STATE_DISCONNECTED` | device removed (USB pull) | none — leave the loop | `device-lost` |
| `-EAGAIN` | nonblocking: no space/data yet | not an error; back to the wait | none |
| `-EINTR` | interrupted wait | retry the wait | none (counted) |

`snd_pcm_recover(pcm, err, 1)` wraps the `-EPIPE`/`-ESTRPIPE` protocols and returns the error unchanged when it cannot handle it [CC-FACT — verify alsa-lib docs]. Acceptable as the mechanism **only after** the event is counted and classified from `err`; hand-rolled prepare/resume is equally sanctioned and makes the resume wait explicit.

### State readback (`snd_pcm_state`) — the second classification axis

States [CC-FACT — alsa-lib `snd_pcm_state_t`; verify]:

| state | meaning | loop's reaction |
|---|---|---|
| `SND_PCM_STATE_RUNNING` | healthy | none |
| `SND_PCM_STATE_XRUN` | xrun latched (also reachable via `poll` `POLLERR` with no negative return yet) | run the `-EPIPE` protocol |
| `SND_PCM_STATE_SUSPENDED` | suspend latched | run the `-ESTRPIPE` protocol |
| `SND_PCM_STATE_DISCONNECTED` | device gone | `device-lost`, leave loop |
| `SND_PCM_STATE_PREPARED` / `SETUP` / `OPEN` / `DRAINING` / `PAUSED` | mid-lifecycle; in the steady loop each is an adapter state-machine defect | debug assert (error E6); release: `device-lost` + defect event |

### Recovery shape (C) — count, classify, then recover

```c
/* Returns true if the loop may continue. Pre-recovery state is the evidence. */
static bool adev_alsa_recover(adev_alsa *ad, int err) {
    snd_pcm_state_t st = snd_pcm_state(ad->pcm);
    adev_event_fault(ad, err, (int)st);              /* E5 fields into the ring FIRST */
    switch (err) {
    case -EPIPE:                                     /* xrun */
        adev_count(ad, CTR_ADEV_XRUN);
        if (snd_pcm_prepare(ad->pcm) < 0) return adev_verb_device_lost(ad);
        adev_prime_silence(ad);
        ad->discontinuity = 1;                       /* core ramps in — D1 */
        return true;
    case -ESTRPIPE: {                                /* suspended: no deadline exists */
        adev_count(ad, CTR_ADEV_SUSPEND);
        int r = -EAGAIN;
        for (uint32_t t = 0; r == -EAGAIN && t < ad->resume_budget; ++t) {
            r = snd_pcm_resume(ad->pcm);
            if (r == -EAGAIN) adev_recovery_backoff(ad); /* sanctioned only here */
        }
        if (r < 0) { if (snd_pcm_prepare(ad->pcm) < 0) return adev_verb_device_lost(ad); adev_prime_silence(ad); }
        ad->discontinuity = 1;
        return true;
    }
    case -EINTR: case -EAGAIN: return true;          /* not faults */
    default: return adev_verb_device_lost(ad);       /* total: catch-all — D8 */
    }
}
```

### Recovery protocols, pinned

- **Xrun (`-EPIPE`).** Classify with what the adapter has: callback duration vs budget (self-overrun evidence), wakeup lateness (late-wakeup evidence) — the four-cause taxonomy is booklet §2.4; the histogram source is observability O4. Then prepare, re-prime with silence, set `discontinuity`, continue. First buffers after recovery **ramp in from silence — a resume click is a second defect on top of the first** [ESTABLISHED: booklet §12.3]. Ramp interval: one period or 5 ms, whichever is shorter [OPEN — ASSUMED].
- **Suspend (`-ESTRPIPE`).** While suspended no deadline exists — the device is not consuming. Retry `snd_pcm_resume` with backoff up to ~1 s total [OPEN — ASSUMED budget], sleeping between attempts is sanctioned *in this state only* (stream already broken; guard suspended around the recovery block, rt_plane_rules R4). Exhaustion → `device-lost`, control plane runs the backed-off reopen loop [ESTABLISHED: booklet §12.4].
- **Repeated xruns are a trend**, not N independent events: control plane watches the rate (leaky bucket) and escalates to the user with the honest trade — larger period, lighter session, diagnosis capture [ESTABLISHED: booklet §12.3]. Thresholds [OPEN — NEEDS-INPUT].

### Rules

| # | rule | route |
|---|---|---|
| D4-1 | every negative return is either mapped in the D8 matrix or hits the catch-all row — no silent `continue` on an unclassified error | host-test-catchable — T6 fault injection drives each row through the fake device |
| D4-2 | count + event **before** recover; the event carries the native code, `snd_pcm_state()`, stream position, and lateness (E5/E7 fields) | host-test-catchable — T6 asserts event-before-recovery ordering |
| D4-3 | ramp-in after every recovery path, no exceptions | host-test-catchable — T6 golden asserts no step discontinuity post-recovery |
| D4-4 | recovery loops are bounded (attempts × backoff), then escalate — unbounded retry on the RT thread is banned work | host-test-catchable + contract-only for the budget values (rt_plane_rules R3) |

---

## D5. WASAPI COM-in-C mechanics

COM is confined inside the adapter as an anti-corruption layer: initialized on adapter-owned threads only, never visible in a port signature, reference counting wrapped so the core never learns Windows has objects [ESTABLISHED: booklet §5.2].

### Compile + link

```c
#define COBJMACROS        /* IFoo_Method(p, ...) call macros            */
#define CINTERFACE        /* C vtable structs instead of C++ classes    */
#include <initguid.h>     /* exactly ONE TU: emits IID/CLSID storage    */
#include <mmdeviceapi.h>
#include <audioclient.h>
```

[MEASURED 2026-08-12: `COBJMACROS` + `CINTERFACE` with `mmdeviceapi.h` + `audioclient.h` compiles in pure C on CLANG64 clang 22.1.8; `IMMDeviceEnumerator_GetDefaultAudioEndpoint` and `IAudioClient3_GetSharedModeEnginePeriod` macros resolve.]

Link rows (Windows leg, build B4): `-lole32` (CoInitializeEx/CoCreateInstance), `-lavrt` (MMCSS) [MEASURED 2026-08-12: `-lavrt` links and `AvSetMmThreadCharacteristicsW` runs]; `-luuid` if IID/CLSID symbols stay unresolved without `initguid.h` [CC-FACT — MinGW import libs; verify at first link].

### Call pattern

```c
IMMDeviceEnumerator *enu = NULL;
HRESULT hr = CoCreateInstance(&CLSID_MMDeviceEnumerator, NULL, CLSCTX_ALL,
                              &IID_IMMDeviceEnumerator, (void **)&enu);
/* macro form and raw form are identical: */
hr = IMMDeviceEnumerator_GetDefaultAudioEndpoint(enu, eRender, eConsole, &dev);
hr = enu->lpVtbl->GetDefaultAudioEndpoint(enu, eRender, eConsole, &dev);
```

Use the macro form everywhere (grep-ability, one spelling) [OPEN — ASSUMED house style]. `eRender`/`eConsole` are `EDataFlow`/`ERole` enums from `mmdeviceapi.h` [CC-FACT].

### COM lifetime discipline

- `CoInitializeEx(NULL, COINIT_MULTITHREADED)` at the start of **every adapter-owned thread that touches COM**, paired `CoUninitialize()` at thread end. `S_OK` and `S_FALSE` (already initialized) both proceed; `RPC_E_CHANGED_MODE` means a host initialized STA on our thread — surface as a setup defect, do not limp [CC-FACT — verify MS COM docs].
- `GetMixFormat` output is freed with `CoTaskMemFree` after the grant is recorded [ESTABLISHED: MS WASAPI docs, IAudioClient::GetMixFormat].
- The RT loop calls only: `WaitForSingleObject`, `GetCurrentPadding`, `GetBuffer`, `ReleaseBuffer` (+ stored `IAudioClock::GetPosition`) — all on interfaces acquired at setup. No `CoCreateInstance` / `Activate` / `GetService` after go-live (they allocate) [CC-FACT]. Classification recorded in rt_plane_rules R7.

### Release table — every interface obtained, who releases, when

| object | obtained via | released by | when |
|---|---|---|---|
| `IMMDeviceEnumerator` | `CoCreateInstance` | adapter teardown | last — kept alive while the notification client (D7) is registered; unregister first |
| `IMMDevice` | `GetDefaultAudioEndpoint` / `GetDevice` | adapter teardown | after the client is released |
| `IAudioClient3` | `IMMDevice_Activate` | stream teardown | after `Stop`, after service interfaces |
| `IAudioRenderClient` / `IAudioCaptureClient` / `IAudioClock` | `IAudioClient_GetService` | stream teardown | first — before their parent client |
| `WAVEFORMATEX *` | `GetMixFormat` | `CoTaskMemFree` | as soon as the grant is copied out |
| pacing event `HANDLE` | `CreateEventW` | `CloseHandle` | teardown; not a COM object, not `Release` |

Order: reverse acquisition. NULL every pointer after release [OPEN — ASSUMED house style].

### Rules

| # | rule | route |
|---|---|---|
| D5-1 | `windows.h`/`audioclient.h`/`mmdeviceapi.h` appear only under `adapters/wasapi/` + `adapters/win32/` | analysis-catchable — config/audit_includes.py (quality G3) |
| D5-2 | one `Release` per acquisition, reverse order, at a named teardown site | target-test-catchable — Windows-leg open/close soak (T6) watches handle/refcount growth; ordering itself contract-only |
| D5-3 | `initguid.h` in exactly one TU | build-catchable — duplicate/missing GUID storage fails at link [CC-FACT] |
| D5-4 | COM init mode is MTA on adapter threads; never touch the process-wide apartment of a host | contract-only — register in rt_plane_rules R8 |
| D5-5 | HRESULTs render in artifacts as `0x%08lX` hex plus the symbolic name from the E5 table — never `FormatMessageW` on the fault path (allocates, localizes, and `AUDCLNT_E_*` codes have no system message) [CC-FACT] | host-test-catchable — E6 message-contract check on emitted events |

---

## D6. WASAPI setup

Control plane, composition root. **Table-level tag:** every API name and constant below is [CC-FACT] against MS WASAPI docs (IAudioClient / IAudioClient3 / IMMDevice) unless tagged otherwise; [MEASURED 2026-08-12] covers only that the headers + macros compile on CLANG64 (D5). `IAudioClient3` availability is Windows-version-bound [VERSION-DEPENDENT — hub H6].

### Share-mode decision

| product tier | mode | why |
|---|---|---|
| low-latency interactive | exclusive, event-driven | device-period floor, engine bypassed — the low-latency tier's mode [ESTABLISHED: booklet §5.2] |
| compatible default | shared via `IAudioClient3` low-latency | engine period bounds the floor and the grant says so honestly; coexists with other clients [ESTABLISHED: booklet §5.2] |
| fallback | shared `IAudioClient`, `GetDevicePeriod` default period | systems without `IAudioClient3` [VERSION-DEPENDENT — hub H6] |

Which tier the product ships is configuration, not adapter logic [ESTABLISHED: booklet §5.2]; the default is [OPEN — NEEDS-INPUT].

### Verify the spellings before first use

The house rule is *run the tool, not the docs*: the probe TU below (D5's defines + the two headers + one macro call per interface used) compiles or it doesn't — [MEASURED 2026-08-12: exactly this pattern compiled on CLANG64 clang 22.1.8; `IMMDeviceEnumerator_GetDefaultAudioEndpoint` and `IAudioClient3_GetSharedModeEnginePeriod` resolved]. Any macro this file names that fails to resolve in the probe is a defect **in this file** — fix the manifest, then the adapter. Keep the probe as `test/probe_wasapi_c.c`; it is the cheapest structural audit of D5–D7 (quality G3).

### Shared low-latency path (IAudioClient3) — the compatible default

| # | call | purpose (one line) |
|---|---|---|
| 1 | `CoInitializeEx(NULL, COINIT_MULTITHREADED)` | COM init, this thread (D5) |
| 2 | `CoCreateInstance(&CLSID_MMDeviceEnumerator, ..., &IID_IMMDeviceEnumerator, &enu)` | enumerator |
| 3 | `IMMDeviceEnumerator_GetDefaultAudioEndpoint(enu, eRender, eConsole, &dev)` — or `_GetDevice(enu, wid, &dev)` for a configured endpoint id | pick the endpoint |
| 4 | `IMMDevice_Activate(dev, &IID_IAudioClient3, CLSCTX_ALL, NULL, (void **)&ac)` | audio client; `E_NOINTERFACE` → fall back to `IAudioClient` + `GetDevicePeriod` path [VERSION-DEPENDENT — hub H6] |
| 5 | `IAudioClient3_GetMixFormat(ac, &wfx)` | engine format — shared streams adopt it (D9); free with `CoTaskMemFree` |
| 6 | `IAudioClient3_GetSharedModeEnginePeriod(ac, wfx, &def, &fund, &min, &max)` | engine periods in frames; legal request = multiple of `fund` in `[min, max]` |
| 7 | `IAudioClient3_InitializeSharedAudioStream(ac, AUDCLNT_STREAMFLAGS_EVENTCALLBACK, period_frames, wfx, NULL)` | init low-latency shared stream at the chosen period; `AUDCLNT_E_ENGINE_FORMAT_LOCKED` / `_PERIODICITY_LOCKED` mean another low-latency client pinned the engine — fall back to `def` period or mix format [CC-FACT — verify HRESULT names in audioclient.h] |
| 8 | `IAudioClient3_SetEventHandle(ac, ev)` with `ev = CreateEventW(NULL, FALSE, FALSE, NULL)` | auto-reset pacing event the engine signals per period |
| 9 | `IAudioClient3_GetBufferSize(ac, &buffer_frames)` | actual allocated ring — part of the grant |
| 10 | `IAudioClient3_GetService(ac, &IID_IAudioRenderClient, (void **)&rc)` + `GetService(&IID_IAudioClock, &clk)` | render client + position clock (D7 pair) |
| 11 | prime: `GetBuffer(buffer_frames)` → silence or first render → `ReleaseBuffer(buffer_frames, 0)` | start full; `AUDCLNT_BUFFERFLAGS_SILENT` on `ReleaseBuffer` writes silence without touching the buffer |
| 12 | `IAudioClient3_Start(ac)` | stream go |

Period choice: `min` for the interactive tier, `def` otherwise [OPEN — ASSUMED, mirrors booklet §2.5 DT-1]. In shared mode the engine period bounds the latency floor — the grant surfaces it honestly, never hides it [ESTABLISHED: booklet §5.2].

### Exclusive event-driven path — the low-latency tier

Steps 1–4 identical (activate `IID_IAudioClient` suffices). Then:

| # | call | purpose |
|---|---|---|
| 5 | build `WAVEFORMATEXTENSIBLE` candidates (D9 ladder) and probe `IAudioClient_IsFormatSupported(ac, AUDCLNT_SHAREMODE_EXCLUSIVE, &wfx, NULL)` | exclusive probe: closest-match out param must be NULL; `S_OK` or `AUDCLNT_E_UNSUPPORTED_FORMAT` per candidate |
| 6 | `IAudioClient_GetDevicePeriod(ac, &hnsDefault, &hnsMinimum)` | device periods in `REFERENCE_TIME` (100 ns units) |
| 7 | `IAudioClient_Initialize(ac, AUDCLNT_SHAREMODE_EXCLUSIVE, AUDCLNT_STREAMFLAGS_EVENTCALLBACK, hnsPeriod, hnsPeriod, &wfx, NULL)` | **buffer duration == periodicity in exclusive event-driven mode** [ESTABLISHED: MS WASAPI docs, IAudioClient::Initialize remarks] |
| 8 | on `AUDCLNT_E_BUFFER_SIZE_NOT_ALIGNED`: `GetBufferSize(&n)` → `hnsAligned = (REFERENCE_TIME)((10000.0 * 1000 / rate * n) + 0.5)` → `Release` the client → re-`Activate` → re-`Initialize` with `hnsAligned` | the documented alignment dance [ESTABLISHED: MS WASAPI docs, IAudioClient::Initialize remarks] |
| 9–12 | `SetEventHandle` → `GetBufferSize` → `GetService(render, clock)` → prime → `Start` | as shared path |

### Probe-candidate builder (C)

Field arithmetic per the `WAVEFORMATEXTENSIBLE` contract [CC-FACT — mmreg.h / ks headers; `SPEAKER_*` and `KSDATAFORMAT_SUBTYPE_*` names verify against MS docs]:

```c
static WAVEFORMATEXTENSIBLE adev_wfx(uint32_t rate, uint16_t ch, uint16_t bits,
                                     uint16_t valid_bits, int is_float) {
    WAVEFORMATEXTENSIBLE w = {0};
    w.Format.wFormatTag      = WAVE_FORMAT_EXTENSIBLE;
    w.Format.nChannels       = ch;
    w.Format.nSamplesPerSec  = rate;
    w.Format.wBitsPerSample  = bits;                  /* container size */
    w.Format.nBlockAlign     = (WORD)(ch * bits / 8);
    w.Format.nAvgBytesPerSec = rate * w.Format.nBlockAlign;
    w.Format.cbSize          = sizeof(WAVEFORMATEXTENSIBLE) - sizeof(WAVEFORMATEX);
    w.Samples.wValidBitsPerSample = valid_bits;       /* 24-in-32: bits=32, valid=24 */
    w.dwChannelMask = (ch == 2) ? (SPEAKER_FRONT_LEFT | SPEAKER_FRONT_RIGHT)
                                : 0; /* >2ch mask is product policy — D9 */
    w.SubFormat = is_float ? KSDATAFORMAT_SUBTYPE_IEEE_FLOAT
                           : KSDATAFORMAT_SUBTYPE_PCM;
    return w;
}
```

Probe order = the D9 ladder: `adev_wfx(rate, ch, 32, 32, 1)` (F32) → `(32, 24, 0)` (24-in-32) → `(32, 32, 0)` (S32) → `(16, 16, 0)` (S16); first `S_OK` wins; all rejected → negotiation failure surfaced to product config [OPEN — ASSUMED ladder order; format policy itself is §D9].

### Grant readback

The grant records: share mode, rate, wire format (from `wfx` actually accepted), `buffer_frames`, period in frames (`period_frames` requested vs `buffer_frames` actual for exclusive), engine periods (`def/fund/min/max`) for the session report. Emit as the `adev.grant` event [OPEN — ASSUMED id; observability O2 owns the registry]. Route for "request != grant handled": host-test-catchable — T6 fake device grants divergent formats.

---

## D7. WASAPI paced loop

### Thread prologue (order matters)

1. `CoInitializeEx(NULL, COINIT_MULTITHREADED)` — this thread renders, and it owns COM calls on acquired interfaces (D5).
2. MMCSS: `DWORD idx = 0; HANDLE mm = AvSetMmThreadCharacteristicsW(L"Pro Audio", &idx);` — link `-lavrt` [MEASURED 2026-08-12: returns non-null handle, observed task index 418; `AvRevertMmThreadCharacteristics` works]. Optionally `AvSetMmThreadPriority(mm, AVRT_PRIORITY_HIGH)` [CC-FACT — avrt.h; verify]. On NULL handle: proceed unelevated, **report the shortfall** — the grant is reported, not assumed [ESTABLISHED: booklet §5.3, §11.1]; policy on shortfall is the composition root's, conventions hub H7.
3. FTZ/DAZ + guard + stack prefault (D1 prologue).
4. `AvRevertMmThreadCharacteristics(mm)` at thread end [MEASURED 2026-08-12].

### Loop shape (shared mode, render)

```c
for (;;) {
    DWORD w = WaitForSingleObject(ad->event, ad->wait_timeout_ms); /* sanctioned block */
    if (w == WAIT_TIMEOUT) { if (adev_wasapi_stalled(ad)) break; continue; }
    if (w != WAIT_OBJECT_0) { if (!adev_wasapi_fault(ad, HRESULT_FROM_WIN32(GetLastError()))) break; continue; }  /* WAIT_FAILED/abandoned: D8 catch-all */
    if (atomic_load_explicit(&ad->stop, memory_order_acquire)) break;   /* C9 */
    adev_publish_stamp(ad);                          /* IAudioClock pair, below — every pacing wakeup, before the render decision */
    UINT32 pad = 0;
    HRESULT hr = IAudioClient3_GetCurrentPadding(ad->ac, &pad);
    if (FAILED(hr)) { if (!adev_wasapi_fault(ad, hr)) break; continue; } /* D8 */
    UINT32 frames = ad->buffer_frames - pad;         /* render exactly this many */
    if (frames == 0) continue;
    BYTE *p = NULL;
    hr = IAudioRenderClient_GetBuffer(ad->rc, frames, &p);
    if (FAILED(hr)) { if (!adev_wasapi_fault(ad, hr)) break; continue; }
    adev_render_to_planes(ad, frames);               /* core render entry, f32 planes */
    adev_convert_interleave(ad, p, frames);          /* D9: planes -> wire format */
    IAudioRenderClient_ReleaseBuffer(ad->rc, frames, 0);
}
```

`GetCurrentPadding` = frames queued and unplayed; free space = `buffer_frames - padding` [CC-FACT — MS docs, IAudioClient::GetCurrentPadding]. `frames` varies per wakeup in shared mode — the core absorbs any partition (dsp K2); `period_frames_max = buffer_frames` in the grant.

### Exclusive event-driven differences

No `GetCurrentPadding`: each event demands exactly one full buffer (`buffer_frames == period frames`); fill it whole every wakeup [CC-FACT — MS docs, exclusive event-driven mode]. Missing the event deadline produces a device-side glitch with **no error return** — detection is ours (below).

### Capture-side differences

`IAudioCaptureClient` delivers **packets**, not free space [CC-FACT — MS docs, IAudioCaptureClient; verify all rows]:

| step | call | note |
|---|---|---|
| 1 | `IAudioCaptureClient_GetNextPacketSize(cc, &n)` | loop until `n == 0` each wakeup — one event may cover several packets |
| 2 | `IAudioCaptureClient_GetBuffer(cc, &p, &frames, &flags, &devpos, &qpc)` | position + QPC arrive with the data — a free D1 pair per packet |
| 3 | flag `AUDCLNT_BUFFERFLAGS_SILENT` | treat packet as silence, do not read `p` |
| 4 | flag `AUDCLNT_BUFFERFLAGS_DATA_DISCONTINUITY` | glitch upstream: map to the port's `discontinuity` mark + `underrun-recovered` accounting |
| 5 | flag `AUDCLNT_BUFFERFLAGS_TIMESTAMP_ERROR` | discard that pair sample from the drift estimator's stream (booklet §7.1) |
| 6 | `IAudioCaptureClient_ReleaseBuffer(cc, frames)` | exactly the frames obtained |

### Timestamps pair

At setup, `GetService(&IID_IAudioClock, &clk)`; per wakeup `IAudioClock_GetPosition(clk, &pos, &qpc)` returns device position plus a QPC timestamp — the D1 pair in one call; `IAudioClock_GetFrequency` gives the position unit (ticks/s, **not** frames) — convert once at setup [CC-FACT — MS docs, IAudioClock]. Fallback where `GetPosition` fails persistently: loop-counted frames + `QueryPerformanceCounter` [ESTABLISHED: booklet §7.1 sanctions loop-counted position].

### Faults in the loop

| condition | handling |
|---|---|
| any HRESULT == `AUDCLNT_E_DEVICE_INVALIDATED` | `device-lost` verb; leave loop; control plane reopen (D8) [CC-FACT — audioclient.h] |
| `WAIT_TIMEOUT` (timeout = `2 × period_ms + 10` [OPEN — ASSUMED]) | count `adev.event_timeout`; N consecutive (N=4 [OPEN — ASSUMED]) → treat as `device-lost` |
| WASAPI has **no xrun return code**: shared-mode underruns play engine silence; exclusive misses glitch silently | detect via position discontinuity (`GetPosition` delta ≠ frames submitted) and missed-event timing; count as `underrun-recovered`, set `discontinuity` → core ramps in [CC-FACT mechanism; ramp rule ESTABLISHED: booklet §12.3] |
| `AUDCLNT_E_OUT_OF_ORDER`, `AUDCLNT_E_BUFFER_TOO_LARGE` | adapter logic defects: assert in debug (error E6), `device-lost` + defect event in release [CC-FACT — audioclient.h] |
| stop path | `IAudioClient_Stop` → `IAudioClient_Reset` → release per D5 table, reverse order (concurrency C9) |

### Default-device change — control plane only

`IMMNotificationClient` implemented as a hand-rolled C vtable (3 IUnknown + 5 notification methods), registered via `IMMDeviceEnumerator_RegisterEndpointNotificationCallback` [CC-FACT — mmdeviceapi.h]. Callbacks arrive on COM worker threads: treat as **control-plane input** — post a command; never touch the RT loop or COM teardown from inside the callback [ESTABLISHED: booklet §5.2 — invalidation notifications arrive on a control-plane thread, converted to fault verbs]. `OnDefaultDeviceChanged(eRender, eConsole|eMultimedia, id)` → product policy: follow the default (stop-and-restart tail onto new endpoint) or stick with the configured device [OPEN — NEEDS-INPUT]. `OnDeviceStateChanged(id, DEVICE_STATE_UNPLUGGED|_NOTPRESENT|_DISABLED)` for the current device → `device-lost`. Unregister before releasing the enumerator (D5 table).

Vtable skeleton — **member order must match `mmdeviceapi.h` exactly; copy from the header, never type from memory** [CC-FACT — order below believed correct; build-catchable only if a signature mismatches, order bugs compile clean and misdispatch]:

```c
typedef struct adev_notify {
    IMMNotificationClientVtbl *lpVtbl;   /* first member — COM ABI */
    LONG ref;
    adev_ctl *ctl;
} adev_notify;

static HRESULT STDMETHODCALLTYPE nc_OnDefaultDeviceChanged(
        IMMNotificationClient *self, EDataFlow flow, ERole role, LPCWSTR id) {
    adev_ctl_post(((adev_notify *)self)->ctl, ADEV_CMD_DEFAULT_CHANGED, id);
    return S_OK;                          /* post and return fast; decide elsewhere */
}
/* nc_QueryInterface / nc_AddRef / nc_Release: standard IUnknown over `ref`.
   nc_OnDeviceStateChanged / Added / Removed / OnPropertyValueChanged: same
   post-a-command pattern; every method returns S_OK promptly.               */

static IMMNotificationClientVtbl nc_vtbl = {
    nc_QueryInterface, nc_AddRef, nc_Release,
    nc_OnDeviceStateChanged, nc_OnDeviceAdded, nc_OnDeviceRemoved,
    nc_OnDefaultDeviceChanged, nc_OnPropertyValueChanged,
};
```

Route for the misdispatch hazard: target-test-catchable — T6's Windows-leg device-change test fires a real default-device switch and asserts the command arrives with the expected payload.

---

## D8. Fault-verb conversion matrix

Conversion is **total**: every native failure lands on exactly one row; the catch-all row still preserves the native code. The adapter converts; the control plane decides; the evidence chain never drops the original code (error E5 owns the full per-adapter tables; E7 the chain contract).

### The matrix

Event/counter ids shown here (`adev.*` dotted events; `ctr_adev_*`/`CTR_ADEV_*` counters, spelled in two different cases even within this file) are placeholders that do NOT follow `reference/observability_flightring_manifest.md`'s shipped grammar and must be renamed when wired: events take O2's `EV_<NAME>` form (uppercase, underscore, module encoded in the numeric id — e.g. `adev.xrun` → an `EV_*` row under the device/deadline module range); counters take O5's `ct_<name>` form (lowercase, underscore, no per-adapter infix — e.g. `ctr_adev_xrun`/`CTR_ADEV_XRUN` → `ct_xrun`, class-indexed per O5's `ct_xrun[4]`). O2/O5 own the final table; this file's job is the mapping, not a competing convention. Recovery owners: [ESTABLISHED: booklet §12.3–12.4].

| native condition | leg | port verb | who recovers — action | counted + event |
|---|---|---|---|---|
| `-EPIPE` | ALSA | `underrun-recovered` | adapter, in-loop: prepare → prime → ramp-in | `ctr_adev_xrun` (+ §2.4 class) · `adev.xrun` |
| `-ESTRPIPE`, resume succeeds | ALSA | `underrun-recovered` | adapter: bounded resume loop → prepare → prime → ramp-in | `ctr_adev_suspend` · `adev.suspend` |
| `-ESTRPIPE`, resume exhausted | ALSA | `device-lost` | control: safe state engaged; bounded, backed-off reopen loop; fallback-device policy | `ctr_adev_device_lost` · `adev.device_lost` |
| `-ENODEV`/`-ENOTTY`/`DISCONNECTED` state | ALSA | `device-lost` | control: as above; session untouched (it lives on the control plane) | same |
| `-EBADFD` persistent | ALSA | `device-lost` (+ defect flag) | control: reopen; debug: assert — this is our state machine, not the OS | `ctr_adev_defect` · `adev.defect` |
| position discontinuity / missed event | WASAPI | `underrun-recovered` | adapter: mark `discontinuity`, ramp-in, continue | `ctr_adev_xrun` · `adev.xrun` |
| `AUDCLNT_E_DEVICE_INVALIDATED` (any call) | WASAPI | `device-lost` | control: reopen loop / fallback policy | `ctr_adev_device_lost` · `adev.device_lost` |
| N consecutive `WAIT_TIMEOUT` | WASAPI | `device-lost` | control: reopen | `ctr_adev_event_timeout` · `adev.event_timeout` |
| `OnDeviceStateChanged` → unplugged/disabled (current device) | WASAPI | `device-lost` | control: reopen | `ctr_adev_device_lost` |
| `OnDefaultDeviceChanged` (follow policy on) / engine format change under stream | WASAPI | `format-invalidated` | control: full renegotiation — stop-and-restart tail, graph recompiles against new grant, stream resumes | `ctr_adev_format_inval` · `adev.format_invalidated` |
| server-side rate/layout switch under a `default`-routed stream | ALSA | `format-invalidated` | control: same tail | same |
| any unmapped negative / FAILED hr | both | `device-lost` (catch-all) | control: reopen; the unmapped code is a filed defect | `ctr_adev_unmapped` · `adev.unmapped` |
| `WaitForSingleObject` != WAIT_OBJECT_0/WAIT_TIMEOUT | WASAPI | `device-lost` (catch-all) | control: reopen; filed defect | `ctr_adev_unmapped` · `adev.unmapped` |

Format-invalidated on the ALSA `hw:` path is rare by construction (the grant is hardware-committed); it is primarily a server-routed and WASAPI-shared phenomenon [CC-FACT].

### What every fault event carries (self-locating failure artifact)

The doctrine: the artifact alone must tell the agent WHAT failed, WHERE, WHY, with enough machine-readable context to patch. Minimum fields — schema owned by observability O2, conversion tables by error E5:

1. event id + port verb; 2. native code verbatim (`errno` int / `HRESULT` hex) + the call site id that returned it; 3. `adev_stamp` pair at detection (stream position, monotonic); 4. grant snapshot hash (links to the `adev.grant` event); 5. xrun classification evidence where applicable: callback duration vs budget, wakeup lateness (booklet §2.4's four causes; histograms O4); 6. recovery action taken + outcome + retry count.

Worked example — one ALSA xrun as it lands in the session report (field names illustrative [OPEN — ASSUMED]; schema is observability O2 / error E8 / config/session_report.schema.json):

```json
{ "ev": "adev.xrun", "verb": "underrun-recovered", "leg": "alsa",
  "native": { "errno": -32, "call": "snd_pcm_writei",
              "site": "adapters/alsa/loop.c:214" },
  "pos_frames": 48239616, "mono_ns": 812345678901, "grant": "g#a1b2c3",
  "class": "late-wakeup", "lateness_us": 2410, "budget_used_pct": 31,
  "recovery": { "action": "prepare+prime+ramp", "ok": true, "retries": 0 } }
```

Reading it is the patch plan: `class:late-wakeup` + low `budget_used_pct` says the DSP is innocent and the wakeup was late — an elevation/placement problem (optimization P9, hub H7), not a kernel problem; `site` locates the detecting call without a debugger. `-EPIPE` is `-32` on Linux [CC-FACT]. Full disposition mapping: error E2; reading artifacts: testing T13.

### Rules

| # | rule | route |
|---|---|---|
| D8-1 | matrix is total; T6 fault injection drives every row through the fake device and asserts verb, counter, and event fields per row | host-test-catchable |
| D8-2 | real-device rows (`-ENODEV` via USB pull, WASAPI invalidation via device disable) exercised on the target rung | target-test-catchable — testing T12 cadences |
| D8-3 | native codes never cross the port as return values (D1-4); they cross as event fields only | analysis-catchable + host-test-catchable |
| D8-4 | reopen loop is bounded and backed-off (schedule [OPEN — ASSUMED: 0.25 s, 0.5 s, 1 s, 2 s, then 2 s steady, user-visible]); the user is told the truth immediately | host-test-catchable — T6 reopen test [ESTABLISHED: booklet §12.4] |

---

## D9. Negotiation + conversion

### Negotiation policy table

Policy cells [ESTABLISHED: booklet §5.2] unless marked; concrete defaults per product tier [OPEN — NEEDS-INPUT].

| leg / mode | rate | format | period / buffer |
|---|---|---|---|
| ALSA `hw:` (exclusive tier) | request exact, `dir=0`; refusal = negotiation failure surfaced to product config | probe ladder below, first accepted wins | `set_period_size_near` from DT-1; buffer 2–3 periods (D2) |
| ALSA `default`/`plughw:` (compat tier) | request product rate; plug/server converts — hidden copies accepted and recorded in the grant event | request `FLOAT_LE`; plug converts | as granted; read back |
| WASAPI shared (IAudioClient3) | **adopt the engine's mix format wholesale** — rate included; forcing a different rate in shared mode buys a resampler and is refused by default [OPEN — ASSUMED policy; consistent with booklet §5.2's honesty rule]. `AUDCLNT_STREAMFLAGS_AUTOCONVERTPCM` exists but inserts hidden conversion — compat fallback only [CC-FACT — audioclient.h; OPEN — ASSUMED refusal] | mix format (float32 typical [CC-FACT]) | `GetSharedModeEnginePeriod`: `min` interactive, `def` otherwise (D6) |
| WASAPI exclusive | probe exact rate via `IsFormatSupported` | device-native ints common; ladder below as `WAVEFORMATEXTENSIBLE` (`SubFormat` = `KSDATAFORMAT_SUBTYPE_IEEE_FLOAT` or `_PCM`, `wValidBitsPerSample` for 24-in-32) [CC-FACT] | period = buffer, alignment dance (D6) |

**Accept vs force, the rule:** accept the engine/device's grant whenever conversion at the boundary is cheap (format, interleave); force only what the core cannot absorb — and rate is the one axis where "convert" means a resampler, so rate mismatches are a product decision, never a silent adapter fix [ESTABLISHED: booklet §5.2 grant honesty + §7.2 who-resamples].

Channel mismatch: grant ≠ product channels → fill extra outputs with silence, ignore extra inputs; anything smarter (downmix, mapping matrices) is product policy [OPEN — NEEDS-INPUT], never invented in the adapter.

### Sample-format table

Wire formats this port supports, both legs [CC-FACT — format names from alsa-lib (`SND_PCM_FORMAT_*`) and WAVEFORMATEXTENSIBLE; verify per leg]:

| wire | layout | → f32 (input) | f32 → (output) | notes |
|---|---|---|---|---|
| `S16_LE` | int16 interleaved | `x * (1.0f/32768.0f)` | clamp to [-1.0, +1.0], `lrintf(x * 32767.0f)` | asymmetric full scale is inherent; dither policy [OPEN — NEEDS-INPUT, ASSUMED off] |
| `S24_3LE` | 3-byte packed LE | sign-extend 24→32, `* (1.0f/8388608.0f)` | clamp, `lrintf(x * 8388607.0f)`, store low 3 bytes | packed — scalar or shuffle conversion; no natural SIMD lane |
| `S32_LE` | int32 | `x * (1.0f/2147483648.0f)` | clamp, scale `2147483647.0f`, `lrint` | devices often use top 24 bits of the 32 [CC-FACT] |
| `F32` (`FLOAT_LE` / IEEE_FLOAT) | float32 | deinterleave copy | interleave copy | WASAPI shared mix format is float32 in practice [CC-FACT] |

Scale convention: full-scale int maps to [-1.0, +1.0) via `1/2^(N-1)`; output path clamps **then** scales **then** rounds with `lrintf` (round-to-nearest-even under default FP env, C17 7.12.9.5 [ESTABLISHED: C17 7.12.9.5]) — saturation is mandatory, wraparound on +1.0 overflow is a defect [OPEN — ASSUMED convention; register in rt_plane_rules R8].

### Conversion kernels

Live in `adapters/common/` [OPEN — ASSUMED layout extension of booklet §5.5], compiled as RT-class TUs; scratch (`wire` staging + plane pointers) sized `channels × period_frames_max` at negotiation from the immortal arena (memory M1/M2) — the loop allocates nothing. Fuse deinterleave with format conversion — one pass, not two:

```c
/* S16 interleaved -> f32 planes; bounded, alloc-free. */
static void adev_s16i_to_f32p(const int16_t *restrict in, float *const *planes,
                              uint32_t frames, uint32_t ch) {
    const float k = 1.0f / 32768.0f;
    for (uint32_t c = 0; c < ch; ++c) {
        float *restrict dst = planes[c];
        const int16_t *src = in + c;
        for (uint32_t i = 0; i < frames; ++i)
            dst[i] = (float)src[(size_t)i * ch] * k;
    }
}
```

Per-plane inner loops with `restrict` are vectorizable; hold them to the remark gate (build B8) [MEASURED 2026-08-12 analog: clang 22.1.8 `-O3 -march=x86-64-v3 -Rpass=loop-vectorize` vectorizes a restrict-qualified float loop at width 8, interleave 4]. Ladder and scalar-twin discipline: dsp K5; optimization P4/P6 for the strided-load cost.

### The two classic conversion defects, pre-empted

**Output overflow at +1.0.** `(int16_t)(x * 32768.0f)` at `x == 1.0f` is out of range — conversion of an out-of-range float to a signed integer is undefined behavior [ESTABLISHED: C17 6.3.1.4]. Saturate first, then scale, then round:

```c
static inline int16_t adev_f32_to_s16(float x) {
    x = fminf(fmaxf(x, -1.0f), 1.0f);      /* saturate — mandatory        */
    return (int16_t)lrintf(x * 32767.0f);  /* round-to-nearest-even under */
}                                           /* default FP env — C17 F.10   */
```

Route: host-test-catchable (T5 property suite feeds ±1.0, ±2.0, NaN) + the UBSan leg catches the raw-cast variant at runtime [MEASURED 2026-08-12: `-fsanitize=undefined` runs on CLANG64 and prints the violating file:line + SUMMARY].

**S24 sign extension.** Shift-based extension (`(int32_t)(u << 8) >> 8`) leans on implementation-defined/undefined shift behavior for the sign bit [ESTABLISHED: C17 6.5.7]. The portable idiom:

```c
static inline int32_t adev_s24le_load(const uint8_t *p) {
    int32_t v = (int32_t)((uint32_t)p[0] | ((uint32_t)p[1] << 8)
                                         | ((uint32_t)p[2] << 16));
    if (v & 0x800000) v -= 0x1000000;      /* portable 24-bit sign extension */
    return v;
}
```

Route: host-test-catchable — T5 round-trips the full-scale negative corner (`0x800000` → `-8388608`).

### Rules

| # | rule | route |
|---|---|---|
| D9-1 | conversion and interleave exist **only** in adapters; no wire-format enum, no interleaved buffer, no int sample type in `core/` | analysis-catchable — audit greps `core/` for wire-format identifiers (quality G3) |
| D9-2 | every conversion pair round-trips: f32 → wire → f32 within format quantization bound; property suite owns the bound | host-test-catchable — testing T5 |
| D9-3 | output conversion saturates; a NaN reaching the converter becomes silence and increments the sentinel counter (booklet §12.5; dsp K7) | host-test-catchable (T5 feeds NaN/±2.0) + runtime-catchable (output sentinel) |
| D9-4 | cross-leg golden equality: the same render through ALSA-fake and WASAPI-fake adapters is byte-exact in f32 before wire conversion | host-test-catchable — quality G6 exact-golden gate |
| D9-5 | negotiation outcome (request, grant, ladder position accepted, conversion cost) is one machine-readable event at go-live | host-test-catchable — T6 asserts `adev.grant` fields (observability O2) |

### Decisions you must not invent (whole-file register)

Product default device class per leg (`hw:` vs `default`; exclusive vs shared) · buffer depth 2 vs 3 periods per tier · channel-mapping policy on mismatch · dither on int output · default-device follow policy on Windows · recovery budgets (resume retries, event-timeout N, reopen backoff schedule) · ramp-in interval · xrun-rate escalation thresholds · event/counter id spellings (observability O2/O5 own them). Each is tagged OPEN above; cards/start-project.md collects the answers at project birth.
