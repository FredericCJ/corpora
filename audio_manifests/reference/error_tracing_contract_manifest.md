# Error & Tracing Contract — Ground-Truth Manifest

**Purpose.** The traceability centerpiece of audio-rt-ground: how every failure in the codebase becomes a machine-readable, self-locating artifact that names its contract, its owning module, and the gate that proves the patch — so the coding agent can go from red to fixed without guessing.

Facts verified 2026-08-12. Version-dependent claims route to reference/audio_platform_baseline_manifest.md (the hub); if any file disagrees with the hub, the hub wins.

Reasoning root: the child booklet `realtime-audio-pc-architecture-and-design-r1.md` (repo root), chiefly booklet ch. 12 (dispositions, degrade, safe state), section 2.4 (xrun taxonomy), sections 13.2–13.4 (always-on set, session report, crash capture), section 11.5 (the autopsy). This file operationalizes; it never re-argues.

Sibling boundaries: event/flight-ring encoding → `reference/observability_flightring_manifest.md` O2/O3. Test-side failure lines and naming → `reference/testing_verification_manifest.md` T2, T13. Device fault verbs in full → `reference/device_adapter_manifest.md` D8. Gate wiring → `reference/quality_gates_ci_manifest.md` G2/G4. Agent-facing walkthroughs → `cards/handle-errors.md`, `cards/diagnose-failure.md`.

---

## E1. The failure-to-patch loop

**Package law.** TESTABILITY and TRACEABILITY are the coding agent's feedback loop: every red artifact must tell the agent WHAT failed, WHERE, and WHY, with enough machine-readable context to patch — and every artifact must be **self-locating**: it carries an id, and the id resolves to a contract, an owning module, and a reference section without human folklore. [OPEN ASSUMED — house doctrine, this package's commission; the architecture it operationalizes is booklet ch. 12–13]

The loop, stated once and cited everywhere:

1. **A gate goes red and leaves an artifact.** No failure without an artifact (E7's first law). The artifact is a single parseable line, a structured report, or a dump — never only prose on a console that scrolled away.
2. **Read the artifact's id and fields.** Formats are frozen parse targets (E6 for check lines, E8 for the session report, T2 for test lines). Parse; do not skim.
3. **The id names the contract.** One lookup in the error-code registry (E3): id → name, disposition, owning module, reference section.
4. **The contract names the patch site.** The registry row's module column is a directory; its reference column is the section of this package that states the rule the code must satisfy. Read that section before touching code.
5. **Patch.**
6. **Rerun the named gate.** Every artifact class has one proving gate (table below). Green closes the loop. Red with the same id: wrong patch. Red with a new id: next loop iteration — progress, not failure.

Artifact → first parse → registry hop → proving gate:

| red artifact | parse target | id lives in | first hop | gate to rerun | route |
|---|---|---|---|---|---|
| compiler/poison error | clang diagnostic (file:line:col) | diagnostic text | `reference/toolchain_build_manifest.md` B3/B11 | rebuild the failing preset (B5) | compiler-catchable |
| `CHECK-FAIL` line | E6 regex | `id=` field → E3 registry | registry row's reference column | the test or run that emitted it | runtime-catchable |
| test failure line | T2 grammar | test id → suite → contract | `reference/testing_verification_manifest.md` T13 | the named suite target | host-test-catchable |
| sanitizer report | tool's own format (E10a) | file:line → owning module | hub H5 for leg, then module's reference section | the sanitizer leg (T8) | host-test-catchable |
| flight event / counter | E8 `events[]` / `counters` | `code`+`name` → E3 registry | registry row | soak or stress rung that trips it (T7/T12) | runtime-catchable |
| xrun autopsy | E8 `xrun_autopsies[]` | `class` field (booklet section 2.4 taxonomy) | `cards/diagnose-failure.md`, then M5/M6, P9, or K-sections per class | soak rung with autopsy armed (G7) | runtime-catchable |
| crash dump | debugger + harvested ring (E9) | crash event code in ring tail | E9 harvest flow, then registry | dirty-exit harvest host test (T6) | runtime-catchable |

RULES:

| # | rule | route |
|---|---|---|
| E1-1 | Every failure-detecting mechanism added to the codebase must name, at the point of detection, a registered code (E3). Un-registered detection is a build defect. | build-catchable (registry audit, G3) |
| E1-2 | Every artifact carries build identity (E7's second law). An artifact without `build=` / `build{}` is not evidence — discard it and re-reproduce. | host-test-catchable (report schema validation) |
| E1-3 | The agent patches from the artifact, not from the symptom's prose description. If the artifact lacks the fields to locate the fault, the FIRST patch is to the artifact (add context fields), the second to the fault. | contract-only |

## E2. Dispositions per plane

The booklet's three dispositions with plane assignments [ESTABLISHED: booklet section 12.1]. The registry (E3) stamps exactly one disposition on every code; `err_disp_of()` returns it, so handling sites cannot improvise.

| disposition | plane | meaning | code shape |
|---|---|---|---|
| `DISP_RETURN` | control | typed status returned upward; every fallible call checked or visibly discarded | shape 1 |
| `DISP_ABSORB_MARK` | RT | substitute safe value + mark event into flight ring + count; **nothing else** — no return path, no log, no block | shape 2 |
| `DISP_SAFE_STATE` | RT | contract violation detected on the RT plane in ship: mark, fade, park the stream, hand control the evidence — never abort mid-callback | shape 3 |
| `DISP_FATAL` | control | stop-the-world; a control-plane verb only, decided while holding evidence of process-wide integrity loss | shape 4 |

Shape 1 — control plane, typed return [ESTABLISHED: booklet section 12.1]:

```c
rt_status_t st = dev_open(&cfg, &s->dev);
if (st != RT_OK) return st;            /* propagate unmodified, or RT_DISCARD(st, "why") — E4 */
```

Shape 2 — RT plane, absorb-and-mark. The mark IS the error handling; absorbing without the mark is `try/continue` with extra steps [ESTABLISHED: booklet section 12.1]:

```c
voice_t *v = pool_acquire(&st->voices);
if (v == NULL) {                                       /* starved: safe value = skip = silence */
    obs_mark2(ERR_MEM_POOL_EXHAUSTED, st->block_seq, POOL_ID_VOICES);  /* O3 emit, wait-free */
    ctr_inc(&st->ctr.pool_starved);
    return;                                            /* the rest of the graph keeps rendering */
}
```

Shape 3 — RT plane, contract violation in ship build (dev builds assert densely instead — booklet section 12.1):

```c
if (handle_gen(h) != pool_gen(p, h)) {                 /* impossible state: stale generation */
    obs_mark2(ERR_MEM_HANDLE_STALE, h.raw, pool_gen(p, h));
    stream_enter_safe_state(st);                       /* ramped silence, stream alive — booklet section 12.5 */
    return;                                            /* control plane decides what next */
}
```

Shape 4 — control plane, stop-the-world with the artifact written first:

```c
if (!arena_layout_valid(&g_arena)) {
    ctl_check_fail(ERR_MEM_LAYOUT_BROKEN, "arena_layout_valid(&g_arena)", "-", "-");  /* E6 line */
    report_write_final(RT_EXIT_DIRTY);                 /* E8 artifact precedes death */
    _Exit(70);                                         /* no atexit graph runs half-broken [ESTABLISHED: C17 7.22.4.5 _Exit] */
}
```

Never:

- **Never `abort()`/`_Exit()`/`exit()` from RT-plane code, any build.** Ship: shapes 2/3 only. Dev: the guard traps and breaks (R4). Route: analysis-catchable (banned-call list in RT TUs, R2) + compiler-catchable (poison prelude, `config/rt_prelude_poison.h`).
- **Never return a status from the render callback to "handle later" without the mark.** There is no later on the RT plane; the event is the handling. [ESTABLISHED: booklet section 12.1] Route: contract-only (review, R8).
- **Never escalate stream-scoped violations to process death.** The stream is the restartable unit; process-fatal is reserved for process-wide integrity, decided by control [ESTABLISHED: booklet section 12.1]. Route: contract-only.

## E3. The error-code registry

One 32-bit space for every failure the codebase can name:

```
uint32 code = (module_id << 16) | low16      /* 0x00000000 = RT_OK, reserved */
```

[OPEN ASSUMED — layout is this package's convention; booklet section 13.5 requires only that ids be stable and retired ids stay reserved]

RULES:

| # | rule | route |
|---|---|---|
| E3-1 | The whole registry lives in ONE owner file, `core/err_registry.def` (x-macro). The generated header is a build artifact; hand-editing it is a defect. | build-catchable (G3 audit: header regenerated and diffed in CI) |
| E3-2 | Codes are stable forever. Never renumber, never reuse. A retired code's number stays reserved with a `/* RETIRED */` row. [ESTABLISHED: booklet section 13.5 — "ids are stable, retired ids stay reserved"] | build-catchable (G3: registry diff gate rejects renumber/reuse) |
| E3-3 | Every code row carries: symbol, module, low16, disposition (E2), reference section. A row missing its reference pointer fails the audit. | build-catchable (G3) |
| E3-4 | Error codes and flight-ring event ids are DISTINCT 16-bit id spaces, never a range-split of one field: an error code's low16 never doubles as an `fr_event.event_id`. The two spaces share only the module-prefix convention and one generation tool (a shared source table with a `kind` column, ERR vs EV); `reference/observability_flightring_manifest.md` O2 owns the event-id side of that table and the split's final wording. An E3 error code reaches the flight ring only as a payload word (O2's `PK_XRUN` w3, `PK_STATE` w2), never as the record's `event_id` field. | build-catchable (shared registry audit) |
| E3-5 | Module ids are append-only, one per owning directory. | build-catchable (G3) |

Module registry [OPEN ASSUMED — numbering and directory names are project decisions; the canonical source layout is `cards/start-project.md`'s]:

| module_id | symbol | owns | reference |
|---|---|---|---|
| 0x0001 | `ERRM_CORE` | graph, schedule, kernels | `reference/dsp_kernel_patterns_manifest.md` K1 |
| 0x0002 | `ERRM_CHAN` | rings, snapshot, mailbox, seqlock | `reference/concurrency_channels_manifest.md` C1 |
| 0x0003 | `ERRM_MEM` | arenas, pools, residency | `reference/memory_residency_manifest.md` M1 |
| 0x0004 | `ERRM_THREAD` | thread port, elevation, affinity | `reference/rt_plane_rules_manifest.md` R1; hub H7 |
| 0x0005 | `ERRM_CLOCK` | clock pair, timers | `reference/device_adapter_manifest.md` D1 |
| 0x0006 | `ERRM_DEV` | audio-device port vocabulary (both adapters convert INTO this module — E5) | `reference/device_adapter_manifest.md` D8 |
| 0x0007 | `ERRM_OBS` | flight ring, drain, report writer | `reference/observability_flightring_manifest.md` O2 |
| 0x0008 | `ERRM_CTL` | control plane, session, supervisor | this file E2 |
| 0x0009 | `ERRM_ROOT` | composition root, go-live checks | this file E2; booklet section 4.5 |
| 0x000A–0x7FFF | — | unassigned, append-only | — |

The one owner file, x-macro shape (the generated-header route; a codegen script reading a table is the equally valid alternative — pick one per project, record in `_work`):

```c
/* core/err_registry.def — THE owner file (E3-1). Append-only. */
#define ERR_MODULES(X) /* X(sym, id, owning_dir, reference) */ \
  X(ERRM_CORE,   0x0001, "core",     "dsp_kernel_patterns K1")        \
  X(ERRM_CHAN,   0x0002, "core",     "concurrency_channels C1")       \
  X(ERRM_MEM,    0x0003, "core",     "memory_residency M1")           \
  X(ERRM_DEV,    0x0006, "adapters", "device_adapter D8")

#define ERR_CODES(X) /* X(sym, module, low16, disposition, reference) */ \
  X(CHAN_CMD_RING_FULL,  ERRM_CHAN, 0x0001, DISP_RETURN,      "concurrency_channels C2") \
  X(CHAN_EVT_RING_DROP,  ERRM_CHAN, 0x0002, DISP_ABSORB_MARK, "concurrency_channels C2") \
  X(MEM_POOL_EXHAUSTED,  ERRM_MEM,  0x0001, DISP_ABSORB_MARK, "memory_residency M3")     \
  X(MEM_HANDLE_STALE,    ERRM_MEM,  0x0002, DISP_SAFE_STATE,  "memory_residency M3")     \
  X(MEM_LAYOUT_BROKEN,   ERRM_MEM,  0x0003, DISP_FATAL,       "memory_residency M8")     \
  X(DEV_XRUN,            ERRM_DEV,  0x0001, DISP_ABSORB_MARK, "device_adapter D4/D7")    \
  X(DEV_LOST,            ERRM_DEV,  0x0002, DISP_RETURN,      "device_adapter D4/D7")    \
  X(DEV_FORMAT_INVALID,  ERRM_DEV,  0x0003, DISP_RETURN,      "device_adapter D9")       \
  X(THREAD_ELEV_DENIED,  ERRM_THREAD, 0x0001, DISP_RETURN,    "rt_plane_rules R7; hub H7") \
  X(THREAD_PLANE_VIOLATION, ERRM_THREAD, 0x0002, DISP_SAFE_STATE, "rt_plane_rules R4")   \
  X(OBS_SENTINEL_NANINF, ERRM_OBS,  0x0001, DISP_ABSORB_MARK, "observability_flightring O5") \
  X(CTL_DIRTY_EXIT_HARVEST, ERRM_CTL, 0x0001, DISP_RETURN,    "error_tracing_contract E9")
```

Generated view (`core/err_codes.h`, regenerated every build, diffed by G3):

```c
#include <stdint.h>
typedef uint32_t rt_status_t;
enum err_disp { DISP_RETURN, DISP_ABSORB_MARK, DISP_SAFE_STATE, DISP_FATAL };
enum err_module {
#define X(sym, id, dir, ref) sym = (id),
  ERR_MODULES(X)
#undef X
};
enum {
#define X(sym, mod, low, disp, ref) ERR_##sym = ((uint32_t)(mod) << 16) | (uint32_t)(low),
  ERR_CODES(X)
#undef X
};
#define RT_OK ((rt_status_t)0u)
const char    *err_name(rt_status_t c);     /* "MEM_HANDLE_STALE", "?" if unknown  */
enum err_disp  err_disp_of(rt_status_t c);
const char    *err_ref_of(rt_status_t c);   /* "memory_residency M3" — the E1 hop  */
```

`err_name` is one `switch` over the same x-macro (`case ERR_##sym: return #sym;`). A third expansion emits `tools/err_registry.json` at build time so the test harness, the drain, and the agent parse ONE source [OPEN ASSUMED — emission mechanism; the single-source requirement is E3-1]. The x-macro technique itself: [CC-FACT — standard C preprocessor idiom; compiles under `-std=c17` clang].

Retirement, in place (the number never returns to the pool):

```c
  /* X(DEV_JACK_RECONNECT, ERRM_DEV, 0x0004, ...)  RETIRED 2026-xx-xx: adapter removed */
```

The agent's E1 hop, as a command (either source works; the .def is authoritative):

```
grep -n "X(MEM_HANDLE_STALE" core/err_registry.def             # → module, disposition, reference
python -c "import json;print(json.load(open('tools/err_registry.json'))['MEM_HANDLE_STALE'])"
```

## E4. Result conventions in C

| # | rule | route |
|---|---|---|
| E4-1 | Fallible functions return `rt_status_t`; results leave via out-params, written ONLY on `RT_OK` (all-or-nothing; a partial out-param on failure is a latent use-of-garbage). | contract-only + host-test-catchable (contract suites assert out-params untouched on failure, T6) |
| E4-2 | Every status-returning declaration in a port or module header carries `RT_MUST_CHECK`. | compiler-catchable (`-Werror` promotes `-Wunused-result`; warning canon B3) |
| E4-3 | Ignoring a status is legal only through `RT_DISCARD(expr, "why")` — greppable, justified. | compiler-catchable (E4-2 makes the bare call an error) + build-catchable (G3 greps discards lacking justification) |
| E4-4 | `NULL` return means "absent, and absence is the documented, single, expected outcome" (pure lookups). Anything that can fail for more than one reason returns a status. Never `NULL`-as-error — it loses the code. | contract-only (review; `cards/review-code.md`) |
| E4-5 | `errno` and `HRESULT` never cross a port. Capture at the failing call site, convert once (E5), carry the native value only inside the event payload. `errno` must be read immediately — the next library call may overwrite it [ESTABLISHED: C17 7.5 — errno is thread-local, set by library functions]. | analysis-catchable (clang-tidy ban on `errno` outside adapters — B3 check set) + contract-only |

The attribute and the discard, via the compiler port (booklet section 5.6):

```c
#if defined(__clang__) || defined(__GNUC__)
#  define RT_MUST_CHECK __attribute__((warn_unused_result))
#else
#  define RT_MUST_CHECK
#endif

RT_MUST_CHECK rt_status_t dev_open(const dev_cfg_t *cfg, dev_t **out_dev);

/* The only legal way to drop a status. Assignment form silences the warning on
   BOTH compilers — a bare (void)call silences clang but NOT gcc [CC-FACT];
   the toolchain is clang-only (hub H3/H4) but the macro keeps reviews argument-free. */
#define RT_DISCARD(expr, why)                                       \
  do { rt_status_t rt_disc__ = (expr); (void)rt_disc__;            \
       _Static_assert(sizeof(why) > 1, "justify the discard"); } while (0)
```

`warn_unused_result` semantics: [ESTABLISHED: Clang attribute reference — warn_unused_result]. `_Static_assert` in a statement position: [ESTABLISHED: C17 6.7.10]. `sizeof("") == 1`, so the empty justification fails to compile [ESTABLISHED: C17 6.5.3.4].

E4-4 in code — the two legal shapes, side by side:

```c
const op_desc_t *op_find(const char *name);            /* NULL = not registered: the ONE
                                                          documented, expected absence   */
RT_MUST_CHECK rt_status_t op_instantiate(const op_desc_t *d, arena_t *a, op_t **out);
                                                       /* many failure reasons → status;
                                                          *out untouched unless RT_OK    */
```

Never:

- **Never a boolean success return** (`true`/`false` erases the code and the registry hop). Route: contract-only, review checklist.
- **Never `goto fail` chains that collapse distinct codes into one.** Return the code you detected. Route: contract-only.
- **Never check-and-log-and-continue on the control plane** ("logged = handled" is the lie E7 exists to kill; either handle, propagate, or `RT_DISCARD` with the why). Route: contract-only.

## E5. Adapter conversion tables

**The rule: convert at the adapter, once, with the native value preserved in the event payload for forensics.** Inward of the adapter there is exactly one error vocabulary (E3); the native `errno`/ALSA negative/`HRESULT` rides as a raw word in the flight event so the autopsy can still see the platform's own words [ESTABLISHED: booklet section 12.1 — adapters convert the platform's vocabulary at the port, never propagating it inward raw]. The fault-VERB set is exactly the three port verbs D1/D8 define — `underrun-recovered`, `device-lost`, `format-invalidated` (a fourth is a port-contract change) — owned by `reference/device_adapter_manifest.md` D8; rows below use those three spellings only, D8 holds the full matrix.

Codes named below and not shown in E3's sample (`ERR_MEM_LOCK_BUDGET`, `ERR_DEV_SUSPENDED`, `ERR_DEV_STATE_BROKEN`, `ERR_DEV_BUSY`, `ERR_DEV_OPEN_FAILED`, `ERR_DEV_IO`) are further rows of the same registry — E3's listing is a shape demo, never the census; the `.def` file is.

errno (Linux leg, thread/memory/elevation adapters):

| native | context | → code | disposition | note |
|---|---|---|---|---|
| `EPERM` / `EACCES` | `sched_setscheduler`, `mlockall` | `ERR_THREAD_ELEV_DENIED` | RETURN | degrade politely, tell the user; hub H7 owns the privilege dance [CC-FACT: POSIX errno meanings] |
| `ENOMEM` | `mlockall` / `mmap` | `ERR_MEM_LOCK_BUDGET` | RETURN | residency budget vs `RLIMIT_MEMLOCK` — M5 [CC-FACT] |
| `EINTR` | any blocking call, control plane | retried at the adapter | — | never surfaces inward [CC-FACT: POSIX] |
| `EAGAIN` | nonblocking I/O | wait-or-retry at adapter | — | not a fault [CC-FACT] |

ALSA (device adapter, D2–D4 own the loop):

| native | meaning | verb | → code | note |
|---|---|---|---|---|
| `-EPIPE` from `snd_pcm_writei`/`readi` | xrun (under/overrun) | underrun-recovered | `ERR_DEV_XRUN` | recovery via `snd_pcm_prepare`; `snd_pcm_recover()` handles `-EPIPE`/`-ESTRPIPE`/`-EINTR` in one call [ESTABLISHED: ALSA library docs, snd_pcm_recover] |
| `-ESTRPIPE` (resume succeeds) | stream suspended (power event), resume ok | underrun-recovered | `ERR_DEV_SUSPENDED` | loop `snd_pcm_resume` while `-EAGAIN`; ring preserved, no prepare needed (D4) [CC-FACT — verify against ALSA pcm docs] |
| `-ESTRPIPE` (resume exhausted) | stream suspended (power event), resume gives up | device-lost | `ERR_DEV_SUSPENDED` | fall back to `snd_pcm_prepare` on resume failure/`-ENOSYS` (D4) [CC-FACT — verify against ALSA pcm docs] |
| `-EBADFD` | PCM in wrong state — adapter's own state machine broke | device-lost | `ERR_DEV_STATE_BROKEN` | a contract violation of the adapter, not a device event [CC-FACT] |
| `-ENODEV` / `-ENOENT` | device gone | device-lost | `ERR_DEV_LOST` | designed event, booklet section 12.4; fallback-device policy runs on the control plane [CC-FACT] |

WASAPI / HRESULT (device adapter, D5–D7 own the loop). All `AUDCLNT_E_*` spellings below verified present in the CLANG64 `audioclient.h` [MEASURED 2026-08-12: `grep -o 'AUDCLNT_E_[A-Z_]*' /c/msys64/clang64/include/audioclient.h | sort -u`]; their semantics are [CC-FACT: MS WASAPI docs] per row:

| native | phase | verb | → code | note |
|---|---|---|---|---|
| `AUDCLNT_E_DEVICE_INVALIDATED` | any | device-lost | `ERR_DEV_LOST` | unplug / endpoint removed — booklet section 12.4's designed event |
| `AUDCLNT_E_RESOURCES_INVALIDATED` | any | device-lost | `ERR_DEV_LOST` | engine resources torn down; treat as device-lost class |
| `AUDCLNT_E_DEVICE_IN_USE` | Initialize | setup-local | `ERR_DEV_BUSY` | exclusive-mode contention; fires before a grant/stream exists — not a port verb; product policy falls to shared (D6) |
| `AUDCLNT_E_UNSUPPORTED_FORMAT` | Initialize/IsFormatSupported | setup-local | `ERR_DEV_FORMAT_INVALID` | fires before a grant/stream exists — not a port verb; format negotiation path D9 |
| `AUDCLNT_E_BUFFER_SIZE_NOT_ALIGNED` | Initialize (exclusive) | RETRY with aligned size | setup-local | recompute period from `GetBufferSize`, reinitialize (D6) |
| `AUDCLNT_E_INVALID_DEVICE_PERIOD` | Initialize | RETRY with legal period | setup-local | period outside device bounds (D6) |
| `AUDCLNT_E_SERVICE_NOT_RUNNING` | activation | RETURN | `ERR_DEV_OPEN_FAILED` | audio service down — control-plane error, user-visible |
| `AUDCLNT_E_OUT_OF_ORDER` / `AUDCLNT_E_BUFFER_OPERATION_PENDING` | GetBuffer/ReleaseBuffer | none — dev assert | — | adapter API misuse: a programming error, not a runtime fault (E6 dev assert) |
| `E_POINTER`, `E_INVALIDARG`, `CO_E_NOTINITIALIZED` | any COM call | none — dev assert | — | contract violation in our code (COM init per thread is the adapter's setup duty, D5) [CC-FACT: COM docs] |
| any other `FAILED(hr)` | any | RETURN | `ERR_DEV_OPEN_FAILED` or `ERR_DEV_IO` | preserve full 32-bit `hr` in payload word 0; `FAILED()` = severity bit set [ESTABLISHED: MS HRESULT docs] |

Row-split flag: `AUDCLNT_E_DEVICE_IN_USE`/`AUDCLNT_E_UNSUPPORTED_FORMAT` are marked `setup-local` above (they fire before a grant/stream exists, so no D1 port verb applies) but still carry a registry code; whether a setup-local fault should carry an E3 code at all, or route some other way, is [OPEN — NEEDS-INPUT: whoever finalizes D8's matrix].

Data-flag note: capture-side `AUDCLNT_BUFFERFLAGS_DATA_DISCONTINUITY` / `AUDCLNT_BUFFERFLAGS_SILENT` are verified spellings [MEASURED 2026-08-12: same grep] — they mark data conditions, not errors; the adapter converts them to counted marks, not statuses (D7).

RULES:

| # | rule | route |
|---|---|---|
| E5-1 | Conversion happens exactly once, in the adapter TU that made the native call. A second conversion site for the same native family is a defect. | build-catchable (G3: grep for `HRESULT`/`snd_pcm_`/`errno` outside the device/thread/memory-elevation adapter TUs under `adapters/` — exact sub-layout [OPEN — ASSUMED]; include audit keeps native headers out of core — booklet section 15.3) |
| E5-2 | The event payload for any converted fault carries the native value verbatim (sign-extended errno, raw 32-bit HRESULT) as word 0. | host-test-catchable (fault-injection suite asserts payload round-trip, T6) |
| E5-3 | The adapter's conversion table is data (a switch over the x-macro or a static table), not scattered `if`s — one function per adapter: `dev_alsa_convert(int err)`, `dev_wasapi_convert(HRESULT hr)`. | analysis-catchable (function exists; review) + host-test-catchable (T6 table-driven test walks every row) |

## E6. Check / assert message contract

Every check failure emits ONE machine-parseable line. This format is THE parse target for the coding agent — frozen, versioned, gate-checked.

```
CHECK-FAIL id=<REGISTRY_NAME> file=<repo-relative> line=<n> expr="<predicate>" expected="<x>" actual="<y>" ctx=<k1=v1,k2=v2,k3=v3> build=<git-short[-dirty]>
```

Example:

```
CHECK-FAIL id=MEM_HANDLE_STALE file=core/pool.c line=142 expr="handle_gen(h)==pool_gen(p,h)" expected="7" actual="9" ctx=pool=voices,slot=13,block=88412 build=8c1f22e
```

The same contract tripped on the RT plane arrives as a binary event and is rendered by the drain to the SAME grammar, values in hex, `expr` reconstructed from the registry (E6-2):

```
CHECK-FAIL id=MEM_HANDLE_STALE file=core/pool.c line=142 expr="<registry>" expected="-" actual="-" ctx=w0=0x2100000d,w1=0x9,block=88412 build=8c1f22e
```

One regex parses both — the agent never needs to know which plane detected it.

The frozen grammar (v1) as a parse regex [OPEN ASSUMED — this package's freeze; versioning rule below]:

```
^CHECK-FAIL id=([A-Z][A-Z0-9_]*) file=([^ ]+) line=([0-9]+) expr="([^"]*)" expected="([^"]*)" actual="([^"]*)" ctx=(-|[a-z0-9_]+=[^ ,]+(,[a-z0-9_]+=[^ ,]+){0,2}) build=([0-9a-f]{7,40}(-dirty)?)$
```

Field semantics:

| field | content | rule |
|---|---|---|
| `id` | the E3 registry NAME of the violated contract | the E1 hop; never free text |
| `file`,`line` | `__FILE__`/`__LINE__`, repo-relative | build compiles with `-fmacro-prefix-map=<abs-repo>/=` so `__FILE__` is repo-relative [MEASURED 2026-08-12: `clang --help` lists `-fmacro-prefix-map=<value>`, clang 22.1.8]; identity wiring in B10 |
| `expr` | stringized predicate | inner `"` replaced by `'` at emission; ≤ 120 chars, truncated with `…` |
| `expected`,`actual` | formatted values; `-` when inapplicable | control plane formats live; RT events are rendered by the drain with hex words (rule 3 below) |
| `ctx` | 1–3 `key=val` pairs, comma-joined, no spaces; `-` if none | the three most diagnostic values the callsite has; values truncated at 32 chars |
| `build` | short git hash, `-dirty` suffixed | must equal the session report's `build.git` (E8) |

RULES:

| # | rule | route |
|---|---|---|
| E6-1 | FREEZE: the `CHECK-FAIL` marker and field order are format v1. Any change ships under a NEW marker string (`CHECK-FAIL2`), never a silent field change — parsers must never need version sniffing on v1 lines. | build-catchable (G3: golden-regex test over emitted lines) + host-test-catchable (a unit test emits one of each and parses it back) |
| E6-2 | RT-plane checks NEVER format. They emit a binary event (code, file-id, line, ≤2 raw words) into the flight ring; the control-plane drain renders the identical v1 line, values in hex. File-id encoding is O2's. [ESTABLISHED: booklet section 13.1 — nothing on the RT plane may block or format, invariant 13] | compiler-catchable (poison prelude bans stdio/format in RT TUs) + runtime-catchable (guard, R4) |
| E6-3 | Dev asserts (`RT_DASSERT`) compile out of ship builds; they may trap/break. Field checks (`CTL_CHECK`, `RT_CHECK`) survive ship and dispose per the registry (E2). Choosing which flavor a new check gets is a review question, not a habit. | contract-only (review-code card) |
| E6-4 | One failure, one line. No multi-line essays, no repeated emission per retry loop (emit once, then count). | host-test-catchable (T6 asserts single emission under injected repeat) |
| E6-5 | Test-artifact failures do NOT share CHECK-FAIL's single-line token style. `reference/testing_verification_manifest.md` section T2 — the sole owner of test-artifact format — defines exactly one marker, the sentinel-delimited `TESTFAIL v1` block (`--- TESTFAIL v1 ---` … `--- END TESTFAIL ---`, one `KEY=value` per line); this file never introduces `TEST-FAIL`/`GOLDEN-FAIL`/`PROP-FAIL` as separate markers. | build-catchable (shared regex library in `tools/`, G3) |

Macro shapes (control, then RT):

```c
/* Control plane: formats live, then disposes per registry. */
#define CTL_CHECK(id, expr, exp_str, act_str, ctx_str)                        \
  do { if (!(expr)) {                                                         \
    log_line("CHECK-FAIL id=%s file=%s line=%d expr=\"%s\" expected=\"%s\" "  \
             "actual=\"%s\" ctx=%s build=%s",                                 \
             #id, __FILE__, __LINE__, #expr, (exp_str), (act_str),            \
             (ctx_str), rt_build_id());                                       \
    err_dispose_ctl(ERR_##id);                    /* RETURN or FATAL per E2 */\
  } } while (0)

/* RT plane: binary event only; drain renders the line off-plane (E6-2). */
#define RT_CHECK(id, expr, w0, w1)                                            \
  do { if (!(expr)) {                                                         \
    obs_mark4(ERR_##id, OBS_FILE_ID, __LINE__, (uint64_t)(w0), (uint64_t)(w1));\
    ctr_inc(&g_ctr.guard_trips);                                              \
    err_dispose_rt(ERR_##id);                 /* ABSORB_MARK or SAFE_STATE */ \
  } } while (0)

/* Dev-only assert, both planes; gone in ship. */
#if RT_BUILD_DEV
#  define RT_DASSERT(expr) do { if (!(expr)) rt_trap(); } while (0)
#else
#  define RT_DASSERT(expr) ((void)0)
#endif
```

`rt_trap()` = `__builtin_trap()` under clang [ESTABLISHED: Clang builtin docs], break-if-debugger in the dev guard (R4). `OBS_FILE_ID` is the build-generated per-TU file-table index (O2; part of build identity B10).

## E7. The evidence chain

Two laws, then the table.

**Law 1: no failure without an artifact.** A failure class with an empty "artifact" cell is a design defect — booklet section 2.4's closing sentence ("an xrun with no witness is a lie the system tells its own recorder") generalized to every class. [ESTABLISHED: booklet section 2.4]

**Law 2: an artifact without build identity is not evidence.** Every row below embeds `build` (E6 line field, E8 `build{}` block, dump-embedded id per booklet section 13.4 / invariant 17). [ESTABLISHED: booklet section 13.4]

| failure class | artifact | lands where | key fields | retention [OPEN ASSUMED defaults] |
|---|---|---|---|---|
| host test fail | T2-grammar line + failing-case file | stdout + `tests/out/<case>.json` | test id, seed, first divergence, build | CI artifact 30 days; local until next green |
| guard trip (R4) | `CHECK-FAIL id=THREAD_PLANE_VIOLATION ... ctx=sym=<wrapped>` | stderr (dev) + flight ring | callsite, plane tag, wrapped symbol | session report |
| sanitizer hit | tool report (ASan/UBSan/TSan text) | stderr → CI artifact | tool, file:line, stacks, build (leg per hub H5 [MEASURED 2026-08-12: ASan+UBSan run on CLANG64; TSan runtime ABSENT on CLANG64 → Linux leg only]) | CI artifact 30 days |
| xrun | flight event `ERR_DEV_XRUN` + autopsy attachment (booklet section 11.5) | ring → `xrun_autopsies[]` in session report | class (booklet section 2.4), gap/duration split, `minflt/majflt`, `nvcsw/nivcsw`, native word | report; last N=20 reports rotate |
| degrade-rung change | flight event | ring → `degrade_history[]` | rung from/to, reason, measured headroom | report |
| device fault | flight event with native payload (E5-2) | ring → `events[]` | verb, code, native errno/HRESULT, device id | report |
| output-sentinel intervention | flight event + counter | ring → `counters.sentinel_interventions` | kind (nan_inf/clamp), block seq | report; **nonzero = filed bug by definition** [ESTABLISHED: booklet section 12.5] |
| crash | minidump/core + dirty marker + last checkpoint | OS dump location + `reports/` | dump carries ring region + build id (E9) | dumps N=5 rotate |
| watchdog stall (booklet section 12.6) | supervisor event + forced report write | ring + report (`report_reason=watchdog`) | last heartbeat seq, stalled block counter, thread states | report |
| dirty exit (any) | marker file + harvested tail | next session's first events (E9) | previous build, exit class, ring tail | one generation |

Sanitizer artifact anatomy — the tool's own line is already self-locating; parse `file:line:col`, then the kind. Verified output shape on this machine's toolchain [MEASURED 2026-08-12: `clang -fsanitize=undefined` on CLANG64 clang 22.1.8, run of a 1-line overflow]:

```
p12_ubsan.c:2:34: runtime error: signed integer overflow: 2147483647 + 1 cannot be represented in type 'int'
SUMMARY: UndefinedBehaviorSanitizer: undefined-behavior p12_ubsan.c:2:34
```

The `SUMMARY:` line is the stable grep target across sanitizers [CC-FACT: LLVM sanitizer common format]. CI keeps sanitizer stderr as a file artifact, never only in the scrollback (E1 step 1).

Reading any of these as an agent: `cards/diagnose-failure.md` walks the triage; T13 owns the test-side reading discipline.

## E8. The session report

The per-run evidence artifact — booklet section 13.3's object, pinned field-by-field. **`config/session_report.schema.json` (JSON Schema draft-07) is the machine twin of this section; the two must match exactly — a divergence is a build defect** (G3 diffs schema hash; E8 and the schema version together). The SAME artifact gates CI (soak/stress rungs consume it — `reference/testing_verification_manifest.md` T12, `reference/quality_gates_ci_manifest.md` G7) and rides user bug reports [ESTABLISHED: booklet section 13.3 — consumers deliberately identical in format].

Writer: the drain, on clean exit, on demand, on watchdog, plus a periodic checkpoint (`session.partial.json`, atomic rename, default every 30 s [OPEN ASSUMED]) — generation mechanics in O7. Encoding: UTF-8, LF, one JSON object, keys snake_case, no NaN/Inf (JSON forbids them; absent measurements are `null` or omitted optional keys).

Field-by-field (mirror of the schema; ✱ = key added by this package beyond the booklet's list, still normative):

| path | type | content |
|---|---|---|
| `schema_version` | string `^1\.[0-9]+$` | this contract's version; minor bump = additive change + new `schema_hash`; major bump = new file name |
| `build.git` | string `^[0-9a-f]{7,40}(-dirty)?$` | commit of the running binary (B10) |
| `build.flags_hash` | 16 hex | first 16 hex of SHA-256 over the canonical flag string — B10 owns canonicalization |
| `build.schema_hash` | 16 hex | first 16 hex of SHA-256 of `config/session_report.schema.json` bytes: `sha256sum config/session_report.schema.json | cut -c1-16` [CC-FACT: coreutils] — recompute, never hardcode |
| `build.variant`✱ | `dev\|ship\|bench` | which build class emitted this (dev reports carry guard trips; bench reports feed P2) |
| `machine.cpu` | string | model string, e.g. `i9-12900K` |
| `machine.os` | string | `uname -sr` / Windows build string |
| `machine.leg` | `linux-clang\|windows-clang64` | toolchain leg (hub H3/H4 own the definitions) |
| `session.*`✱ | object | `started_utc`, `ended_utc` (null if crashed), `exit` ∈ `clean\|dirty\|crash\|watchdog\|running`, `report_reason` ∈ `exit\|on_demand\|harvest\|watchdog` — the E9 harvest writes `exit=dirty, report_reason=harvest` |
| `stream.rate_hz` | int | negotiated sample rate |
| `stream.format` | string | sample format token, e.g. `f32le` (negotiation D9) |
| `stream.channels`✱ | int | channel count |
| `stream.period_frames` | int | negotiated period (booklet section 2.5's product parameter) |
| `stream.device` | string | adapter's device id string |
| `stream.api`✱ | `alsa\|wasapi_shared\|wasapi_exclusive` | which adapter and mode |
| `histograms.callback_us` | histogram | per-render cost distribution, always on [ESTABLISHED: booklet section 13.2] |
| `histograms.wakeup_gap_us` | histogram | wakeup-to-start gap — the split that classifies late-wakeup xruns (booklet sections 11.5, 2.4) |
| histogram shape | object | `unit:"us"`, `edges[N+1]` ascending (serialized explicitly — parsers never assume binning; default 64 log-spaced bins 1 µs→100 ms [OPEN ASSUMED]), `counts[N]`, `overflow`, `total`, `max_seen` |
| `counters.xruns` | object | by class: `self_overrun`, `late_wakeup`, `external_stall`, `device_fault`, `unclassified` [ESTABLISHED: booklet section 2.4 taxonomy] |
| `counters.ring_drops` | object | channel-id → dropped count; keys are C1's registered channel names (invariant 2's witnesses) |
| `counters.pool_high_water` | object | pool-name → high-water mark (M3) |
| `counters.sentinel_interventions` | object | `nan_inf`, `clamp` — front-page number; nonzero = bug [ESTABLISHED: booklet section 12.5] |
| `counters.denormal_trips` | int | denormal/NaN patrol (K7) |
| `counters.guard_trips` | int | dev-build guard hits (R4); must be 0 in any report a gate accepts |
| `events[]` | array | flight-ring tail, oldest first, default last 256 [OPEN ASSUMED]; each: `seq`, `t_us` (monotonic µs since stream start, clock pair per booklet section 7.1), `code` (uint32, E3), `name` (registry name), `words[]` (≤6 raw payload words as `0x…` hex strings — 64-bit exactness; JSON numbers lose >2^53 [ESTABLISHED: RFC 8259 interop note]), optional `decoded{}` |
| `degrade_history[]` | array | each: `t_us`, `rung_from`, `rung_to` (0–5; 0 = full quality, 5 = fade-to-silence per booklet section 12.2), `reason` ∈ `headroom\|recovery\|forced`, `headroom_pct` |
| `xrun_autopsies[]` | array | each: `t_us`, `class`, `period_us`, `wakeup_gap_us`, `duration_us`, and when the autopsy layer is armed (booklet section 11.5): `minflt`, `majflt`, `nvcsw`, `nivcsw` (null when unarmed), `native` (decimal errno or `0x…` HRESULT, null if none), `recovered_ms` |

RULES:

| # | rule | route |
|---|---|---|
| E8-1 | Every emitted report validates against `config/session_report.schema.json`. `config/check.sh` (contract in G2) runs the validation on the reports the test rig produced. Well-formedness floor: `python -m json.tool < report.json` [CC-FACT: CPython stdlib]; full draft-07 validation tool: OPEN NEEDS-INPUT (candidate: `jsonschema` in the dev venv — not pinned here). | host-test-catchable |
| E8-2 | The report never carries audio, content identifiers, or PII — local-first; upload explicit and consented. [ESTABLISHED: booklet section 13.3] | contract-only (review) + build-catchable (G3 greps report writer for banned field families) |
| E8-3 | Additive schema change: minor `schema_version` bump, schema re-hashed, E8 table updated in the same commit. Breaking change: new major = new artifact filename; v1 parsers keep working on v1 files. | build-catchable (G3: schema hash + version cross-check) |
| E8-4 | File naming `session-<utc-compact>-<pid>.json` under the product data dir `reports/` [OPEN ASSUMED — location is a product decision, NEEDS-INPUT]. Atomic write: temp + rename. | host-test-catchable (T6) |

## E9. Crash capture and the dirty-exit harvest

When the process dies anyway, the dump must be worth reading: the flight ring and counters live in ONE contiguous, named region (the immortal arena, M2) so every dump contains the recorder by construction, and the build id is embedded in the image so the dump names its decoder [ESTABLISHED: booklet section 13.4].

### Windows leg: minidump

`SetUnhandledExceptionFilter` + `MiniDumpWriteDump` [CC-FACT: MS dbghelp docs]. Signature and the user-stream parameter verified in the CLANG64 headers: `MiniDumpWriteDump(HANDLE, DWORD, HANDLE, MINIDUMP_TYPE, PMINIDUMP_EXCEPTION_INFORMATION, PMINIDUMP_USER_STREAM_INFORMATION, PMINIDUMP_CALLBACK_INFORMATION)` [MEASURED 2026-08-12: declared in `/c/msys64/clang64/include/psdk_inc/_dbg_common.h` line 1687; import lib `libdbghelp.a` present → link `-ldbghelp`].

```c
static LONG WINAPI crash_writer(EXCEPTION_POINTERS *ep) {
    /* Everything pre-arranged at go-live: dump file pre-created, dbghelp pre-loaded,
       user-stream descriptor pointing at the ring region pre-filled. No CRT heap here. */
    MINIDUMP_EXCEPTION_INFORMATION mei = { GetCurrentThreadId(), ep, FALSE };
    obs_stamp_crash_event();                   /* plain stores into the locked ring   */
    MiniDumpWriteDump(GetCurrentProcess(), GetCurrentProcessId(), g_dump_file,
                      MiniDumpNormal, &mei, &g_ring_user_stream, NULL);
    return EXCEPTION_EXECUTE_HANDLER;          /* let the process die; no heroics     */
}
/* at go-live: */ SetUnhandledExceptionFilter(crash_writer);
```

`MiniDumpNormal` omits most data memory [CC-FACT: MS minidump docs] — the ring region is therefore attached explicitly as a `MINIDUMP_USER_STREAM` (the pre-filled `g_ring_user_stream`); the heavier alternative (`MiniDumpWithPrivateReadWriteMemory`) trades dump size for zero setup [CC-FACT]. Handler discipline: no allocation, no formatting, no COM, no lock acquisition — pre-open the file handle at go-live [CC-FACT: dbghelp is not reentrant-safe; keep the handler minimal].

Coverage caution: `abort()` and CRT fail-fast paths can bypass the unhandled-exception filter (Watson/`__fastfail` take over) [CC-FACT: MS CRT docs — verify per CRT; UCRT on this leg, hub H3]. The dirty-exit marker (below) is therefore the backstop that owes nothing to the filter: a death the handler never saw still gets harvested — with the dump missing, not the story.

### Linux leg: core dump

`RLIMIT_CORE` must be raised or cores are truncated to nothing; destination and naming are `/proc/sys/kernel/core_pattern`'s (systemd-coredump on most distros) [ESTABLISHED: man 5 core]. Machine-specific capture configuration is a hub row [VERSION-DEPENDENT - hub H4].

```c
struct rlimit rl = { RLIM_INFINITY, RLIM_INFINITY };
(void)setrlimit(RLIMIT_CORE, &rl);             /* at go-live, control plane */
```

Cores include the process's anonymous memory by default (`/proc/<pid>/coredump_filter` bit semantics) — the mlocked ring is present without extra work; never `madvise(MADV_DONTDUMP)` the arena region [ESTABLISHED: man 5 core; man 2 madvise]. If the process manipulates privileges at elevation time, re-assert dumpability: `prctl(PR_SET_DUMPABLE, 1)` [CC-FACT: man 2 prctl — dumpable can be cleared by credential changes].

In-handler discipline, both legs: async-signal-safe minimalism — plain stores (stamp the crash event), `write(2)` to a pre-opened fd, `_exit`/re-raise; never `malloc`, never `fprintf`, never unwinding [ESTABLISHED: man 7 signal-safety lists the async-signal-safe set].

### The dirty-exit marker + next-start harvest

1. Go-live writes `reports/session.dirty`: one line, same token grammar as E6 (marker, `key=value`, build last inverted to first for grep symmetry):

   ```
   DIRTY-MARKER build=8c1f22e pid=31337 started=2026-08-12T14:00:00Z partial=reports/session.partial.json
   ```

   Written by the control plane, before the stream starts.
2. The drain checkpoints `session.partial.json` every 30 s [OPEN ASSUMED] — atomic rename, schema-valid (E8).
3. Clean exit: final report written, marker deleted. That order — report, then marker — is the invariant the harvest relies on.
4. Crash: handler stamps the crash event and the OS writes the dump; the marker remains.
5. Next start, before go-live: marker present → previous session died dirty. Harvest: finalize the orphaned `session.partial.json` as `session-<ts>.json` with `session.exit=dirty|crash` (crash if a newer dump exists), `report_reason=harvest`; emit `ERR_CTL_DIRTY_EXIT_HARVEST` carrying the previous build id and ring-tail digest as the NEW session's first events — every relaunch tells the previous session's story [ESTABLISHED: booklet section 13.4].
6. Rotate: keep last 5 dumps, 20 reports [OPEN ASSUMED].

| # | rule | route |
|---|---|---|
| E9-1 | The harvest path is host-tested by killing the process under test and asserting the next start emits the harvest events. [ESTABLISHED: booklet section 13.4] | host-test-catchable (T6 fault injection) |
| E9-2 | Crash handlers are reviewed against the async-signal-safety allowlist; any call outside it is a defect even if it "works". | analysis-catchable (clang-tidy banned-call list on the handler TU) + contract-only |
| E9-3 | Dump + report + symbols resolve as a set: the dump's embedded build id must locate archived symbols (B9/B10). A dump whose id has no archived symbols is E7-law-2 dead evidence. | build-catchable (release rung archives symbols keyed by build id, G7) |

## E10. Worked examples — the loop, end to end

Three failures walked artifact-first. Excerpts are invented but format-true; test-line grammar is T2's, sanitizer format is the tool's own.

### (a) TSan race on ring indices

Artifact (Linux leg — TSan is Linux-only [MEASURED 2026-08-12: no tsan runtime in CLANG64 clang libs; hub H5]):

```
WARNING: ThreadSanitizer: data race (pid=31337)
  Write of size 8 at 0x7f3c2a801040 by thread T2:
    #0 spsc_push core/ring_spsc.c:74
  Previous read of size 8 at 0x7f3c2a801040 by thread T7:
    #0 spsc_pop core/ring_spsc.c:112
  Location is global 'g_cmd_ring' of size 192 at 0x7f3c2a801000 (+64)
SUMMARY: ThreadSanitizer: data race core/ring_spsc.c:74 in spsc_push
```

The loop: file `core/ring_spsc.c` → module `ERRM_CHAN` → registry reference → `reference/concurrency_channels_manifest.md` C2, whose contract requires acquire/release pairing on index publication [ESTABLISHED: booklet section 6.3(b)]. Inspect line 74: `r->head = h + 1;` — a plain store where C2's blessed idiom (R6) requires `atomic_store_explicit(&r->head, h + 1, memory_order_release)`. **Patch class: missing release on index publication.** Gate: rerun the Linux TSan stress leg — the channel torture recipe (C8) under `ctest` preset `linux-tsan` (T7/T8) — plus the cross-leg build to prove the fix compiles on CLANG64. Green TSan on the suite that provoked it closes the loop.

### (b) Golden first-divergence at a block boundary

Artifacts (two gates red together — that pairing IS the diagnosis):

```
--- TESTFAIL v1 ---
TEST_ID=golden.svf_sweep_48k.48k_128f
SPEC=reference/dsp_kernel_patterns_manifest.md K6
CONTRACT=bit-identical pinned-path output (exact regime)
SAMPLE=4096
CHANNEL=0
EXPECT=<decimal> (0x3f2a7c11)
ACTUAL=<decimal> (0x3f2a7c15)
BUILD_ID=8c1f22e
--- END TESTFAIL ---

--- TESTFAIL v1 ---
TEST_ID=property.block_partition.svf_lp
SPEC=reference/dsp_kernel_patterns_manifest.md K2
CONTRACT=output invariant to callback partitioning within the block quantum
SAMPLE=4096
SEED=0xc0ffee
X_PARTITIONS=128|64+64
BUILD_ID=8c1f22e
--- END TESTFAIL ---
```

Read the fields: divergence at frame 4096 = 32 × 128 — exactly a block boundary; the block-partition property (render in one 128 chunk vs 64+64 must be bit-identical) is red at the same frame. That signature means **hidden per-callback state**: the op does work per `process()` call that should be per-frame or per-stream (a coefficient smoother stepping once per call, state re-init in `process()`). Contract: `reference/dsp_kernel_patterns_manifest.md` K2 — partition invariance, the block quantum owes nothing to state [ESTABLISHED: booklet section 4.4]. **Patch class: move call-scoped state to prepare/reset; advance smoothers by frames processed, not by calls.** Gate: property suite (T5) + golden masters (T4) green, then the cross-leg exact-golden gate (G6) because bit-exactness claims are per-leg proofs.

### (c) Xrun autopsy shows a residency gap

Artifact (session report tail):

```json
{"t_us": 421337421, "class": "external_stall", "period_us": 2666.7,
 "wakeup_gap_us": 102.4, "duration_us": 3105.0,
 "minflt": 0, "majflt": 7, "nvcsw": 0, "nivcsw": 3, "native": null}
```

Read the fields against the taxonomy [ESTABLISHED: booklet sections 2.4, 11.5]: gap small (wakeup fine), duration blew the period, `majflt=7` mid-callback with involuntary switches — the callback took page faults: **an RT-plane page was not resident**. Contract: residency invariant — every byte the plane touches is locked at go-live (M1/M2). Verify: Linux — `grep VmLck /proc/<pid>/status` vs the arena's expected size, then M5's coverage audit; Windows — M6's `VirtualLock` coverage check (the working-set raise that makes it succeed is proven on this machine [MEASURED 2026-08-12: `VirtualLock` returns 1 on a 64 KiB region after `SetProcessWorkingSetSizeEx` raise]). Typical fault: a table allocated after `mlockall(MCL_CURRENT)` without `MCL_FUTURE`, or a region committed after the Windows lock pass. **Patch class: move the allocation into the immortal arena (M2) locked at go-live; add/repair the go-live residency assert (runtime-catchable, booklet section 15.1).** Gate: go-live assert green, then the soak rung with the autopsy layer armed (G7/T12) showing `majflt=0` across the soak's `xrun_autopsies[]` — the same artifact that caught it proves the fix.

---

Inline OPEN register: module numbering + directory map (E3), error/event id-space split with O2 (E3-4), fault-verb spellings pending D8 (E5), CHECK-FAIL freeze ownership v1 (E6-1), retention defaults (E7), checkpoint cadence + report location + tail length + histogram binning (E8/E9), schema validator choice (E8-1), dump/report rotation counts (E9). Each is marked at its row; decisions belong to the project, not to this file.
