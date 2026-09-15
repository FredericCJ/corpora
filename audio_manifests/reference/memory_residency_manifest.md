# Memory and Residency — Ground-Truth Manifest

**Purpose.** Operational memory doctrine for the real-time audio process: the five allocation classes and their code contracts (immortal arena, epoch arena, pools with generation handles, frame scratch), residency made real on both legs (lock + prefault + verify), RT stack discipline, and the layout/working-set budget that keeps the hot path inside the cache hierarchy.

Facts verified 2026-08-12. Version-dependent claims route to reference/audio_platform_baseline_manifest.md (the hub); if any file disagrees with the hub, the hub wins.

Reasoning root: the booklet `realtime-audio-pc-architecture-and-design-r1.md` (repo root), ch. 8 (memory as architecture) and section 4.5 (composition-root order). This file operationalizes the booklet; it never re-argues it.

Adjacent files: the guard machinery that *proves* the class rules lives in reference/rt_plane_rules_manifest.md section R4 (this file owns the allocators); channel storage layout is reference/concurrency_channels_manifest.md; cache-miss diagnosis is reference/optimization_microarch_manifest.md section P7. Cards that route here: cards/start-project.md, cards/write-rt-code.md, cards/optimize-performance.md.

---

## M1. Allocation classes

Every object in the process belongs to exactly one of five classes, chosen by one question — **when does it die?** — and the class is declared where the object is created [ESTABLISHED: booklet section 8.3]. The RT plane touches only the first four; the fifth never crosses the boundary.

| class | "when does it die?" | freed how | backing allocator | RT plane | canonical contents |
|---|---|---|---|---|---|
| **immortal** | at process teardown | never individually — mapping released wholesale at exit (lazy-cleanup by design) | root bump arena (M2) | yes | state arena, buffer pool, channel storage, flight ring, lookup tables |
| **epoch** | at the next structural change | whole per-epoch arena retired at once after grace | per-epoch bump arena; reclaim via reference/concurrency_channels_manifest.md section C3 | yes (read-mostly) | compiled schedule + derived tables |
| **pooled** | slot recycled; N alive at once | slot to free-list; generation bumped | fixed-size pool + slot-map handles (M3) | yes | voices, in-flight events, streaming blocks |
| **block scratch** | at the end of the current block | pointer rewind; nothing freed | per-RT-thread scratch arena (M4) — the only legal RT allocator | yes | per-block kernel workspace |
| **control general** | ordinary lifetime | `free()` / heap discipline | system heap; dev builds route through the allocation wrapper (R4) | **never** | UI, session, files, device juggling |

Table shape [ESTABLISHED: booklet section 8.3]. Sizes and counts are rows of the root memory plan (below), derived from the negotiated device format and the compiled schedule (booklet sections 4.5, 8.3).

### Rules

| RULE | route | tag |
|---|---|---|
| The RT plane calls no allocator but the frame scratch (M4). `malloc`/`calloc`/`realloc`/`free`/`aligned_alloc` are poisoned in RT translation units via config/rt_prelude_poison.h | compiler-catchable | [MEASURED 2026-08-12: `#pragma GCC poison malloc` → "attempt to use a poisoned identifier", CLANG64 clang 22.1.8] |
| Dev builds wrap the heap (`-Wl,--wrap=malloc` and family) and the guard proves zero RT-plane hits (reference/rt_plane_rules_manifest.md section R4) | host-test-catchable (guard suite) | [MEASURED 2026-08-12: wrap links and fires under lld MinGW driver] |
| The wrap counter is zeroed at **plane entry**, not process start — the CRT allocates before `main` | runtime-catchable (dev) | [MEASURED 2026-08-12: `__wrap_malloc` observed 3 CRT-internal hits before `main` in a trivial exe] |
| RT object files carry no undefined heap symbols: config/audit_symbols.py greps `llvm-nm` output of RT-marked objects for `U malloc` etc., wired into config/check.sh (reference/quality_gates_ci_manifest.md section G3) | build-catchable | [MEASURED 2026-08-12: llvm-nm lists object symbols] |
| The root memory plan enumerates every immortal and pooled region with its size derivation; sizes asserted at go-live | build-catchable + runtime-catchable | [ESTABLISHED: booklet section 8.3] |
| Per-subsystem `memory-limit` budgets: exhaustion indicts a component, never "the process" | runtime-catchable (watermark counters, reference/observability_flightring_manifest.md section O5) | [ESTABLISHED: booklet section 8.3] |
| Control-plane bounded-time allocation (rare; it has no deadline): TLSF is the cataloged named option; default remains the system heap | contract-only | [ESTABLISHED: booklet section 8.3] |
| The class of every allocation is syntactically visible: arena / pool / scratch calls name the class; a bare heap call in shared code is a review defect | analysis-catchable (poison + symbol audit) + contract-only (declaration habit) | [ESTABLISHED: booklet section 8.3] |

### What memory owes the feedback loop

Failure artifacts are self-locating (the doctrine this package exists for). Every memory failure message carries: region name, requested vs available bytes, the limit that refused, `errno`/`GetLastError`, and the remedy pointer (hub H7 row) — per the check/assert message contract, reference/error_tracing_contract_manifest.md section E6. Error ids live in the registry (section E3); this file names the payloads only. [OPEN — ASSUMED: registry reserves a MEM family; final naming is E3's.]

| evidence | where it lands | what the agent does with it |
|---|---|---|
| immortal + epoch arena high-water vs capacity | session report, reference/observability_flightring_manifest.md section O7 | resize plan rows with numbers, not feelings |
| scratch high-water per RT thread | session report O7 | prove per-block workspace bound |
| pool watermark + shed count per pool | counters canon O5 | split defect (sized-against-design) from load (external demand) |
| locked-bytes actual vs plan (`VmLck` / `QueryWorkingSetEx`) | go-live assert + session report | residency proof without rerun |
| stack watermark per RT thread | soak report, reference/quality_gates_ci_manifest.md section G7 | ratchet stack budgets |

---

## M2. The immortal arena

One mapping, allocated at the composition root (booklet section 4.5 step 4), locked and prefaulted at step 5, never freed — teardown releases the whole mapping; lazy-cleanup is the design, not a leak [ESTABLISHED: booklet sections 8.1, 8.3]. One mapping keeps the lock call singular and the TLB footprint minimal [ESTABLISHED: booklet section 8.5]. This class is ~90% of the RT plane's bytes [ESTABLISHED: booklet section 8.3].

Backing: Linux `mmap(NULL, cap, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0)` [CC-FACT: mmap(2)]; Windows `VirtualAlloc(NULL, cap, MEM_RESERVE|MEM_COMMIT, PAGE_READWRITE)` [CC-FACT: MS VirtualAlloc docs]. Both return page-aligned bases [CC-FACT].

### The bump allocator

```c
#include <stddef.h>
#include <stdint.h>

typedef struct {
    unsigned char *base;   /* one page-aligned mapping, immortal */
    size_t         cap;
    size_t         off;    /* bump cursor */
    size_t         high;   /* == off; named for the session report row */
} arena_t;

/* align must be a power of two; default call sites pass 64 */
static inline void *arena_alloc(arena_t *a, size_t n, size_t align) {
    size_t off = (a->off + (align - 1)) & ~(align - 1);
    if (off > a->cap || n > a->cap - off)
        return NULL;             /* root converts to a loud go-live failure (E6 payload) */
    a->off = off + n;
    a->high = a->off;
    return a->base + off;
}
```

### Rules

| RULE | route | tag |
|---|---|---|
| Default alignment is 64 bytes (cache line on the reference class — hub H8); callers may request more (page alignment for the buffer pool). Page-aligned base + aligned offsets ⇒ returned pointers carry the requested alignment | compiler-catchable (`_Static_assert` on power-of-two at call sites) | [CC-FACT: arithmetic; line-size row: hub H8] |
| `_Alignas(64)` on arena-resident types compiles clean on both legs and is the preferred spelling for per-type guarantees | compiler-catchable | [MEASURED 2026-08-12: `_Alignas(64)` compiles clean, CLANG64 clang 22.1.8] |
| Never rely on heap alignment for SIMD state: `aligned_alloc` is control-plane-only and `malloc`'s guarantee is `max_align_t` (16 on this ABI), below the 64 the layouts assume | compiler-catchable (poison header removes the temptation in RT TUs) | [ESTABLISHED: C17 7.22.3 fundamental-alignment wording; 16-byte figure CC-FACT: x86-64 ABI] |
| Arena exhaustion at the root is a **startup** failure with a clean message — the root allocates everything up front precisely so memory exhaustion is never a mid-stream event (NT commit charge and Linux overcommit-OOM are two failure shapes with this one design answer) | runtime-catchable (root, invariant-14 loudness) | [ESTABLISHED: booklet section 8.1] |
| The arena never grows: no second mapping mid-stream. A plan that changed shape is an epoch/structural event (C3), not arena growth | analysis-catchable (mmap/VirtualAlloc are banned syscalls on the plane, reference/rt_plane_rules_manifest.md section R2) | [ESTABLISHED: booklet sections 8.1, 8.3] |
| Individual frees of immortal objects do not exist; there is no `arena_free`. Teardown releases the mapping wholesale after the two-phase stop (reference/concurrency_channels_manifest.md section C9) | contract-only (the API has no free to call) | [ESTABLISHED: booklet sections 4.5, 8.3] |
| Per-epoch arenas reuse this allocator verbatim: built control-side, published by snapshot swap, retired whole after grace — the arena *is* the discard unit, so fragmentation is structurally impossible | host-test-catchable (C3 reclaim suite) | [ESTABLISHED: booklet section 8.3] |

---

## M3. Pools and generation handles

Fixed-size pools serve the churning populations (voices, in-flight events, streaming blocks): slot storage carved from the immortal arena, a free-list of indices, and **generation-carrying handles** — the slot-map shape — so a stale handle is a *detected* error, never a corruption [ESTABLISHED: booklet section 8.3].

### Shape and code

Handle = one `uint32_t`: low 20 bits index, high 12 bits generation. [OPEN — ASSUMED split: 20/12 (1,048,576 slots, 4,095 generations); re-split per pool if churn analysis demands it.]

```c
#include <stddef.h>
#include <stdint.h>

typedef uint32_t handle32;                    /* 0 is the permanently invalid sentinel */
#define H_IDX(h) ((h) & 0xFFFFFu)
#define H_GEN(h) ((h) >> 20)

typedef struct {
    unsigned char *slots;      /* capacity * stride, immortal-arena backed */
    uint32_t      *gen;        /* per-slot generation; starts at 1 */
    uint32_t      *freelist;   /* stack of free indices */
    uint32_t       free_top, capacity, stride;
    uint32_t       shed_count; /* external-demand refusals; exported counter (O5) */
} pool_t;

static inline void *pool_resolve(pool_t *p, handle32 h) {
    uint32_t i = H_IDX(h);
    if (i >= p->capacity || p->gen[i] != H_GEN(h))
        return NULL;                          /* stale or forged: detected, not dereferenced */
    return p->slots + (size_t)i * p->stride;
}

static inline handle32 pool_acquire(pool_t *p) {
    if (p->free_top == 0) { p->shed_count++; return 0; }
    uint32_t i = p->freelist[--p->free_top];
    return (p->gen[i] << 20) | i;
}

static inline void pool_release(pool_t *p, handle32 h) {
    if (!pool_resolve(p, h)) return;          /* stale/double release: counted, E-coded, refused */
    uint32_t i = H_IDX(h);
    uint32_t g = (H_GEN(h) + 1u) & 0xFFFu;
    p->gen[i] = g ? g : 1u;                   /* wrap skips 0 so handle 0 stays invalid forever */
    p->freelist[p->free_top++] = i;
}
```

Stale-handle detection is the memory-poisoning instinct, typed [ESTABLISHED: booklet section 8.3]: releasing a slot bumps its generation, so every outstanding handle to it stops resolving. `pool_resolve` is branch-cheap and lock-free because pools are single-plane-owned; handles may cross planes as plain `u32` event payloads, but resolution always happens on the owning plane (channel selection: reference/concurrency_channels_manifest.md section C1).

### Exhaustion policy — the split you must preserve

| exhaustion cause | classification | response | route | tag |
|---|---|---|---|---|
| sized-against-design overflow (population the schedule bounds) | **defect** | plan row was wrong; dev check fires with pool name + capacity + demand; fix the plan | build-catchable (plan assert at root) + host-test-catchable | [ESTABLISHED: booklet section 8.3, invariant 11] |
| external-demand overflow (voices under a MIDI flood) | **load, not defect** | shed by recorded policy (voice-stealing is the domain name), `shed_count++`, degrade ladder owns the policy (booklet section 12.2) | runtime-catchable (counter + heartbeat, O5/O6) | [ESTABLISHED: booklet sections 8.3, 12.2] |

### Rules

| RULE | route | tag |
|---|---|---|
| Never dereference before resolve; never cache the resolved pointer across a release point (re-resolve after any point the slot could churn) | contract-only + host-test-catchable (T7 concurrency suites replay churn) | [ESTABLISHED: booklet section 8.3; suite: reference/testing_verification_manifest.md section T7] |
| A 12-bit generation wraps after 4,095 recycles of one slot; a stale handle can then false-validate. Size generation bits to churn rate; dev builds count wrap events into the session report | host-test-catchable (dev wrap counter) + contract-only (bit-split review) | [CC-FACT: pigeonhole arithmetic of the encoding above] |
| Pool capacities and strides come from the root memory plan (negotiated format + schedule), never from literals at the use site | build-catchable | [ESTABLISHED: booklet section 8.3] |
| Failure payloads name the pool, capacity, live count, and requesting subsystem — exhaustion indicts a component | runtime-catchable; message per reference/error_tracing_contract_manifest.md section E6 | [ESTABLISHED: booklet section 8.3] |

---

## M4. The frame scratch arena

Per-RT-thread workspace for kernels that need more than their state slots: a bump arena **reset every block** — pointer rewound, nothing freed — the cheapest allocator that exists and **the only one legal on the RT plane** [ESTABLISHED: booklet section 8.3].

```c
typedef struct { unsigned char *base; size_t cap, off, high; } scratch_t;

static inline void *scratch_alloc(scratch_t *s, size_t n) {
    size_t off = (s->off + 63u) & ~(size_t)63u;          /* 64B default, as M2 */
    if (off > s->cap || n > s->cap - off) return NULL;   /* design error — see rules */
    s->off = off + n;
    if (s->off > s->high) s->high = s->off;              /* watermark → session report */
    return s->base + off;
}

static inline void scratch_reset(scratch_t *s) {
    s->off = 0;                                          /* at block start, every block */
}
```

Backing storage is carved from the immortal arena per RT thread at the root; capacity = the schedule's worst-case per-block workspace, asserted at go-live [ESTABLISHED: booklet sections 4.5, 8.3].

### Rules

| RULE | route | tag |
|---|---|---|
| Scratch lifetime ends at `scratch_reset`; holding a scratch pointer across blocks is a defect. Dev builds poison the used range on reset (`0xDD` fill) so use-after-reset corrupts deterministically and fails the golden masters | host-test-catchable (offline renderer + goldens, reference/testing_verification_manifest.md sections T3–T4) + contract-only | [OPEN — ASSUMED house mechanism; poison fill is dev-only cost] |
| Scratch is thread-private: never pass a scratch pointer to another thread or into a channel | contract-only; torture recipes catch the crash (reference/concurrency_channels_manifest.md section C8) | [ESTABLISHED: booklet section 8.3 — per-thread by construction] |
| Overflow is always a **defect** (invariant-11 sized-against-design; the schedule bounds every kernel's ask): NULL here is unreachable once the root assert passed. Dev check fires with kernel id + ask + capacity; release disposition per reference/error_tracing_contract_manifest.md section E2 | build-catchable (root assert from schedule report) + runtime-catchable (dev check) | [ESTABLISHED: booklet section 8.3] |
| `scratch_reset` at block **start**, not end — a block never reads its predecessor's leavings | host-test-catchable (goldens are block-order invariant, reference/dsp_kernel_patterns_manifest.md section K2) | [OPEN — ASSUMED ordering convention] |
| No locks, no syscalls, no growth inside scratch — it is arithmetic on thread-private state | analysis-catchable (R2 banned-ops table covers the tempting escapes) | [ESTABLISHED: booklet section 8.3] |

---

## M5. Residency — Linux leg

Allocation is not residency: a successful allocation returns address space; pages arrive on first touch and can leave under pressure. A minor fault costs microseconds, a major fault milliseconds — one page fault can outspend a period [ESTABLISHED: booklet ch. 8 preamble]. The root closes the gap at step 5 (booklet section 4.5).

### The sequence, in root order

1. **Check the limit first** for a clean message: `getrlimit(RLIMIT_MEMLOCK)` vs the plan's locked total; on refusal, the message names the limit and the fix — the audio-group `memlock` limits row every Linux audio deployment inherits (deployment row: hub H7) [CC-FACT: getrlimit(2); convention ESTABLISHED: booklet section 8.1].
2. **Lock everything, current and future**: `mlockall(MCL_CURRENT | MCL_FUTURE)` [CC-FACT — verify: mlockall(2); TLPI is the booklet's carried reference for exact semantics].
3. **Touch every page just allocated** (step 5's prefault pass): locking prevents *reclaim*; the design does not lean on the lock call's own fault-in behavior — the write-touch pass below makes materialization (and CoW break) unconditional [ESTABLISHED: booklet section 8.1 — "the root still touches every page"].
4. **Bind now**: RT-reachable code resolves at load; lazy PLT resolution is a first-call fault. Leg flag row (`-Wl,-z,now`) lives in reference/toolchain_build_manifest.md section B9 [ESTABLISHED: booklet section 8.1, Drepper via booklet lineage; flag spelling CC-FACT: ld docs].
5. **Verify and assert**: read `VmLck` from `/proc/self/status`, assert ≥ plan's locked total, record actual in the session report [CC-FACT: proc(5)].

```c
#include <sys/mman.h>
#include <sys/resource.h>
#include <stdio.h>

int residency_lock_all(size_t planned_bytes) {   /* root step 5; control plane */
    struct rlimit rl;
    if (getrlimit(RLIMIT_MEMLOCK, &rl) == 0 && rl.rlim_cur != RLIM_INFINITY &&
        rl.rlim_cur < planned_bytes)
        return -1;                       /* message: limit value + hub H7 limits.d row */
    return mlockall(MCL_CURRENT | MCL_FUTURE);   /* errno into the failure payload */
}

static void prefault_rw(unsigned char *p, size_t n) {
    volatile unsigned char *v = p;       /* write-touch: a read of fresh anonymous pages
                                            maps the shared zero page; first write still
                                            faults (CoW break) [CC-FACT: Linux mm] */
    for (size_t i = 0; i < n; i += 4096) v[i] = v[i];
    if (n) v[n - 1] = v[n - 1];
}

long vmlck_kib(void) {                   /* go-live assert reads this; -1 on parse failure */
    FILE *f = fopen("/proc/self/status", "r");
    char line[128]; long kib = -1;
    if (!f) return -1;
    while (fgets(line, sizeof line, f))
        if (sscanf(line, "VmLck: %ld", &kib) == 1) break;
    fclose(f);
    return kib;
}
```

Human spot-check: `grep VmLck /proc/<pid>/status` [CC-FACT: proc(5)].

### Rules

| RULE | route | tag |
|---|---|---|
| `MCL_FUTURE` is process-wide: every later control-plane allocation is locked and charged against `RLIMIT_MEMLOCK` — the effectively-unlimited audio-group row (hub H7) is what makes the whole-address-space stance viable; under a finite limit, later `mmap`s fail `ENOMEM` far from the root | runtime-catchable (root limit check + loud message) + contract-only (deployment row) | [CC-FACT: mlock(2) semantics; stance ESTABLISHED: booklet section 8.1] |
| `MCL_FUTURE` covers RT thread stacks spawned at root step 6: new mappings are locked (population at creation is best-effort — MAP_LOCKED-class semantics, mmap(2): the prefault attempt may silently fall short and major-fault later; the M7 write-touch pass is what makes materialization unconditional) — the M7 prefault loop still runs, as depth-warming and belt-and-braces | runtime-catchable (M7 loop + watermark) | [CC-FACT: mlock(2)/mlockall future semantics] |
| Never `MCL_ONFAULT` (or `MAP_NORESERVE`) on RT-reachable memory: lock-on-fault defeats materialize-before-go-live by design | analysis-catchable (flag grep in config/check.sh) + contract-only | [CC-FACT: mlock2(2) MCL_ONFAULT semantics; doctrine ESTABLISHED: booklet ch. 8 law] |
| Locking defends against reclaim, **not commit exhaustion**: Linux overcommit means allocation success ≠ pages exist. The up-front allocate-and-touch at root converts overcommit surprise into a startup OOM with a clean message, never a mid-stream event | runtime-catchable (root) | [ESTABLISHED: booklet section 8.1; overcommit knob CC-FACT: /proc/sys/vm/overcommit_memory] |
| Lock refusal is a go-live decision — degrade (run unlocked, tell the user, expect stalls) or refuse — per the product's **recorded** policy; never a silent fallback discovered as an xrun in the field | runtime-catchable (invariant 14) + contract-only (the policy record) | [ESTABLISHED: booklet section 8.1; policy value OPEN — NEEDS-INPUT] |
| CI Linux leg asserts `VmLck` ≥ plan under the target rung | target-test-catchable (reference/quality_gates_ci_manifest.md section G5) | [CC-FACT: proc(5) field] |

---

## M6. Residency — Windows leg

Order matters: **raise the working set, then lock** — `VirtualLock` capacity is bounded by the process minimum working set (max lockable ≈ minimum working set minus a small overhead) [ESTABLISHED: MS VirtualLock docs]. The adapter documents the honest semantics: locked pages are guaranteed resident *while the process is scheduled* — which is the guarantee this design actually needs [ESTABLISHED: booklet section 8.1].

Measured on this machine: `VirtualLock` succeeds (returns 1) on a 64 KiB committed region after `SetProcessWorkingSetSizeEx(min+16 pages, max+64 pages, QUOTA_LIMITS_HARDWS_MIN_ENABLE | QUOTA_LIMITS_HARDWS_MAX_DISABLE)` [MEASURED 2026-08-12]. The +16/+64-page headroom is the working default. [OPEN — ASSUMED headroom; scale with the locked plan.]

```c
#include <windows.h>
#include <psapi.h>   /* link -lpsapi, or define PSAPI_VERSION=2 for the kernel32 export
                        [CC-FACT: MS psapi docs + mingw-w64 headers — verify at first build] */

int residency_lock_region(void *base, SIZE_T bytes, SIZE_T headroom_pages) {
    HANDLE self = GetCurrentProcess();
    SIZE_T mn, mx; DWORD fl;
    if (!GetProcessWorkingSetSizeEx(self, &mn, &mx, &fl)) return -1;
    mn += bytes + headroom_pages * 4096;              /* floor above the locked total */
    if (mx < mn + 64 * 4096) mx = mn + 64 * 4096;
    if (!SetProcessWorkingSetSizeEx(self, mn, mx,
            QUOTA_LIMITS_HARDWS_MIN_ENABLE | QUOTA_LIMITS_HARDWS_MAX_DISABLE)) return -1;
    return VirtualLock(base, bytes) ? 0 : -1;         /* GetLastError() → failure payload */
}

int residency_verify_page(void *page) {               /* go-live assert, per page or sampled */
    PSAPI_WORKING_SET_EX_INFORMATION w = { .VirtualAddress = page };
    if (!QueryWorkingSetEx(GetCurrentProcess(), &w, sizeof w)) return -1;
    return (w.VirtualAttributes.Flags & 1u) ? 0 : -1; /* bit 0 = Valid
                                                         [CC-FACT: MS PSAPI_WORKING_SET_EX_BLOCK] */
}
```

`QueryWorkingSetEx` batches: pass an array of entries, one call for the whole region — do that for the full-region go-live sweep [CC-FACT: MS QueryWorkingSetEx docs]. The block also carries a `Locked` bitfield; `Valid` is the assert the dictated contract keys on, `Locked` is corroborating evidence [CC-FACT: MS PSAPI docs — verify field spelling against psapi.h on CLANG64].

### Rules

| RULE | route | tag |
|---|---|---|
| Raise-then-lock, never lock-then-raise: a `VirtualLock` against the default quota fails once the plan exceeds the default minimum working set | runtime-catchable (root order; failure message names both sizes) | [ESTABLISHED: MS VirtualLock docs; order ESTABLISHED: booklet section 8.1] |
| `QUOTA_LIMITS_HARDWS_MIN_ENABLE` makes the raised floor hard; `QUOTA_LIMITS_HARDWS_MAX_DISABLE` keeps the ceiling soft so the control plane can still grow | runtime-catchable | [MEASURED 2026-08-12: this exact flag pair in the battery; flag semantics CC-FACT: MS SetProcessWorkingSetSizeEx docs] |
| Prefault pass (same `prefault_rw` as M5) still runs after commit: `MEM_COMMIT` charges commit but pages soft-fault on first touch | runtime-catchable (root step 5) | [CC-FACT: MS memory-management docs] |
| Commit-charge honesty: `VirtualAlloc(MEM_COMMIT)` failure at root is the clean startup failure; the design allocates everything up front so commit exhaustion can never be a mid-stream event | runtime-catchable (root) | [ESTABLISHED: booklet section 8.1] |
| **No delay-loaded imports on any RT-reachable path** — a delay-load stub is a first-call loader excursion. Gate: `llvm-readobj --coff-imports app.exe` shows an empty delay-import set; wire into config/check.sh (G3) | build-catchable | [ESTABLISHED: booklet section 8.1; tool row CC-FACT: llvm-readobj lists COFF import + delay-import descriptors; llvm tools present MEASURED 2026-08-12] |
| Shared-library count on RT paths stays near zero via the static-linking preference — reference/toolchain_build_manifest.md section B9 | build-catchable (link policy + map-file audit) | [ESTABLISHED: booklet sections 8.1, 10.4] |
| RT thread stacks: query bounds via `GetCurrentThreadStackLimits`, then `VirtualLock` the committed range after the M7 prefault | runtime-catchable (thread start, before plane entry) | [CC-FACT: MS GetCurrentThreadStackLimits docs (Win8+)] |
| Go-live sweep records locked-bytes actual vs plan in the session report (O7) | runtime-catchable + target-test-catchable (G5 Windows rung) | [CC-FACT: mechanism above] |

---

## M7. Real-time stacks

Each RT thread's stack is pre-sized by the thread port (a generous fixed budget — abundance spent on certainty), guard-paged below, locked, and prefaulted to depth at creation, before the thread enters its plane [ESTABLISHED: booklet section 8.2]. Budget default: 1 MiB per RT thread. [OPEN — ASSUMED; the soak watermark ratchets it, NEEDS-INPUT for the final figure.]

### Prefault and paint, at thread start

```c
#define RT_STACK_BYTES     (1u << 20)                    /* OPEN-ASSUMED budget */
#define RT_PREFAULT_BYTES  (RT_STACK_BYTES - 64u * 1024u) /* headroom above the guard */

void rt_stack_prefault_and_paint(bool paint) {   /* first call on the RT thread, pre-plane */
    volatile unsigned char pad[RT_PREFAULT_BYTES];
    if (paint) {                           /* dev/soak only — full descending fill */
        for (size_t off = sizeof pad; off >= 4096; off -= 4096) {
            volatile unsigned char *pg = &pad[off - 4096];
            for (size_t b = 0; b < 4096; ++b) pg[b] = 0xA5;
        }
    } else {
        for (size_t off = sizeof pad; off > 4096; off -= 4096)
            pad[off - 1] = 0xA5;           /* descend page-wise: nearest page first, so
                                              guard-grown stacks extend in order [CC-FACT] */
        pad[0] = 0xA5;
    }
}
```

Release (`paint == false`) touches one byte per page — the prefault, not a fill: it breaks CoW and proves every page is mapped, nothing more. Dev/soak (`paint == true`) fills every byte of every page with `0xA5`; the watermark reader scans from the deep end for the first non-pattern byte and reports actual depth vs budget into the soak report (reference/quality_gates_ci_manifest.md section G7; session report O7) [ESTABLISHED: booklet section 8.2 — stack-painting-watermarking] — a one-byte-per-page mark cannot support a byte-granular scan, since every unpainted byte in between is already zero from a fresh page and reads as "first non-pattern byte" one byte in. Painting is dev/soak-only; release builds may keep the prefault and skip the scan [ESTABLISHED: booklet section 8.2].

### Per-leg mechanics

| leg | pre-size | guard page | lock | tag |
|---|---|---|---|---|
| Linux | `pthread_attr_setstacksize` (glibc-allocated stack) | default guard = 1 page below | covered by `MCL_FUTURE` at creation (M5) | [CC-FACT: pthread_attr_setstacksize(3), pthread_attr_setguardsize(3)] |
| Linux, caller-provided stack | `pthread_attr_setstack` from the immortal arena | **guardsize is ignored with a caller-provided stack — `mprotect(PROT_NONE)` the bottom page yourself** | already inside the locked arena | [CC-FACT: pthread_attr_setguardsize POSIX/man — the documented trap] |
| Windows | `CreateThread` with `dwStackSize` = full budget, **without** `STACK_SIZE_PARAM_IS_A_RESERVATION` (commits the depth up front) | OS-managed guard below the commit | `GetCurrentThreadStackLimits` + `VirtualLock` of the committed range (M6) | [CC-FACT: MS CreateThread docs] |

### Rules

| RULE | route | tag |
|---|---|---|
| No recursion on the RT plane — unbounded stack in disguise. `misc-no-recursion` in config/.clang-tidy over RT TUs | analysis-catchable; bounded-work doctrine reference/rt_plane_rules_manifest.md section R3 | [ESTABLISHED: booklet section 8.2; check name CC-FACT: clang-tidy] |
| No VLAs — `-Wvla` (promoted to error in the warning canon, reference/toolchain_build_manifest.md section B3) | compiler-catchable | [ESTABLISHED: booklet section 8.2; flag CC-FACT: clang] |
| No `alloca` — `-Walloca` in the canon; poisoned in config/rt_prelude_poison.h besides | compiler-catchable | [ESTABLISHED: booklet section 8.2; flag CC-FACT: clang] |
| Prefault runs before plane entry, never inside it (it is a page-fault storm by design) | runtime-catchable (guard machinery R4 marks plane entry) | [ESTABLISHED: booklet sections 8.2, 4.5] |
| Watermark-over-budget in soak is a gate failure whose message carries thread name, budget, watermark | target-test-catchable (G7) | [ESTABLISHED: booklet sections 8.2, 14.6] |

---

## M8. Layout and the working-set budget

Residency makes memory exist; layout makes it cheap [ESTABLISHED: booklet section 8.4]. Four disciplines plus the budget procedure.

### Structure-of-arrays for the populations, hot/cold split

Voice state is parallel arrays per field, walked in processing order — lane k = voice k; the layout **is** the vectorization enabler (reference/dsp_kernel_patterns_manifest.md section K5 assumes it) [ESTABLISHED: booklet section 8.4]. Hot/cold split rides along: per-sample-touched fields in the SoA arrays; per-block/per-event fields (envelope stage, note id) in a cooler array; config-rate data elsewhere entirely — the innermost loop's cache lines carry nothing it does not read [ESTABLISHED: booklet section 8.4]. Packing is declined for hot state (natural alignment wins) and taken for cold config [ESTABLISHED: booklet section 8.4].

```c
#include <stdalign.h>
#include <stdint.h>
#define MAX_VOICES 64                      /* multiple of 16: arrays stay 64B-multiples */

typedef struct {                           /* hot: per-sample-touched fields ONLY */
    alignas(64) float phase[MAX_VOICES];
    alignas(64) float inc  [MAX_VOICES];
    alignas(64) float gain [MAX_VOICES];
} voices_hot_t;

typedef struct {                           /* cold: per-block / per-event */
    uint8_t  env_stage[MAX_VOICES];
    uint16_t note_id  [MAX_VOICES];
} voices_cold_t;

_Static_assert(MAX_VOICES % 16 == 0, "keep per-field arrays cache-line multiples");
_Static_assert(sizeof(voices_hot_t) % 64 == 0, "hot block is line-granular");
```

### Alignment and padding are contracts

| RULE | route | tag |
|---|---|---|
| Every SIMD-touched array aligns to the vector width (32B for the AVX2 floor — hub H8); 64B is the house default and satisfies it | compiler-catchable (`_Static_assert`, `alignas`) | [ESTABLISHED: booklet section 8.4; `_Alignas(64)` compiles clean MEASURED 2026-08-12] |
| Every cross-thread structure pads to the cache line; the canonical case is the SPSC ring's producer/consumer indices — reference/concurrency_channels_manifest.md section C2 (false-sharing avoidance) | compiler-catchable (static asserts on offsets) + host-test-catchable (C8 torture makes violations cost) | [ESTABLISHED: booklet section 8.4, perfbook via booklet] |
| Layout contracts are asserted, not commented: `_Static_assert` on `sizeof`/`offsetof` wherever a layout is a contract | compiler-catchable | [ESTABLISHED: booklet section 8.4] |

### Buffer-pool stride stagger

```c
stride = ((buf_bytes + 4095u) & ~4095u) + 64u;   /* page multiple + one cache line */
```

Rationale, two lines: many same-sized buffers at page-aligned strides put same-indexed elements in the same cache sets and defeat store-forwarding disambiguation on same-page-offset accesses — the classic 4 KiB-aliasing stall family. One extra line per slot staggers sets and offsets [ESTABLISHED: booklet section 8.4]. Diagnosing the stall when you suspect it anyway: reference/optimization_microarch_manifest.md section P7.

### The working-set-per-block budget procedure

Reference rows, this machine [MEASURED 2026-08-12; owned by hub H2]: L1d 48 KiB per P-core / 32 KiB per E-core; L2 1.25 MiB per P-core / 2 MiB shared per 4-E cluster; L3 30 MiB shared.

| footprint | target level | budget row | tag |
|---|---|---|---|
| innermost voice loop's per-iteration hot state | L1d | ≤ 32 KiB (2/3 of P-core L1d) | [ESTABLISHED: booklet section 8.4 for the level; fraction OPEN — ASSUMED] |
| whole block's touched bytes — **the workhorse target** | L2 | ≤ 768 KiB (~60% of P-core L2) | [ESTABLISHED: booklet section 8.4 for the level; fraction OPEN — ASSUMED] |
| sample libraries, delay histories, convolution tails | L3/DRAM, streamed | sequential by construction | [ESTABLISHED: booklet section 8.4] |

Procedure:

1. **Sum what one block actually touches** — state blocks of scheduled ops + parameter blocks + live buffer-pool slots + the schedule itself. Source: the graph compiler's liveness-based buffer assignment emits `touched_bytes_per_block` (booklet sections 4.2, 8.4); the bench harness prints it (reference/optimization_microarch_manifest.md section P2) and the session report records it (O7).
2. **Compare against the table** — hot sum vs L1d row, block sum vs L2 row.
3. **Placement dependence**: if RT threads are pinned to P-cores (policy: reference/optimization_microarch_manifest.md section P9), budget against P rows; if E-core landing is possible, budget against 32 KiB / shared-2-MiB rows instead. [MEASURED topology 2026-08-12; policy OPEN — NEEDS-INPUT, owned by P9.]
4. **Bench-verify**: the review gate is a comparison, not a feeling — wired per reference/quality_gates_ci_manifest.md section G4; a failing gate's message carries budget, measured value, and top contributors (self-locating failure, E6).
5. **When a kernel's measured cost disappoints, interrogate working set before instruction count** — on this class a cache-resident O(n log n) routinely beats a DRAM-touching O(n) [ESTABLISHED: booklet section 8.4].

### Streams, prefetch, non-temporal — the refusals

| technique | status | route | tag |
|---|---|---|---|
| sequential access for delay lines / histories / tails | default — hardware prefetchers hide DRAM latency | contract-only (it is a construction property) | [ESTABLISHED: booklet section 8.4] |
| software prefetch | measured-only, last resort, for genuinely irregular walks (modulated taps, granular clouds); inserted only where the bench shows the stall today; **re-measure every toolchain bump** — a stale distance becomes pollution | target-test-catchable (bench lane, reference/testing_verification_manifest.md section T10) | [ESTABLISHED: booklet section 8.4] |
| non-temporal stores | off the default menu — at audio block sizes almost nothing is write-once-never-reread-soon; behind a measurement if someone reaches for it | target-test-catchable (P2 protocol) | [ESTABLISHED: booklet section 8.4] |

### Pages, TLB, and huge pages

The immortal arena is one large mapping — one lock call, one contiguous range, minimal TLB entries — and hot tables live inside it, not as a constellation of allocations [ESTABLISHED: booklet section 8.5]. Beyond that, large/huge pages are an **optional, measured-only row**: worth evaluating for multi-hundred-megabyte sample sets and convolution libraries, noise for small graphs; transparent variants enabled machine-wide can move latency *into* the fault path [ESTABLISHED: booklet section 8.5]. Mechanism names for orientation only — Linux `MAP_HUGETLB` / `madvise(MADV_HUGEPAGE)`, Windows `MEM_LARGE_PAGES` + `SeLockMemoryPrivilege` + `GetLargePageMinimum()` [CC-FACT: mmap(2)/madvise(2)/MS large-page docs] — deployment knobs and privileges are hub rows (hub H7); adoption gate is a soak comparison (target-test-catchable, G7) [ESTABLISHED: booklet section 8.5].

---

## Never (file-wide)

- Never allocate, free, or map on the RT plane — poison + wrap + symbol audit enforce it (M1; mechanism reference/rt_plane_rules_manifest.md sections R2, R4). [MEASURED 2026-08-12: poison and wrap both fire on CLANG64]
- Never lock without checking/raising the quota first — `RLIMIT_MEMLOCK` on Linux (M5), working-set minimum on Windows (M6). [ESTABLISHED: booklet section 8.1; MS VirtualLock docs]
- Never read-touch as a prefault — write-touch (M5 `prefault_rw`); reads map the shared zero page. [CC-FACT: Linux mm]
- Never treat a lock refusal as a warning to log and forget — it is a go-live decision per recorded policy. [ESTABLISHED: booklet section 8.1]
- Never free an immortal or epoch object individually; the arena is the discard unit. [ESTABLISHED: booklet section 8.3]
- Never dereference a pool handle without `pool_resolve` (M3). [ESTABLISHED: booklet section 8.3]
- Never recurse, declare a VLA, or call `alloca` in RT translation units (M7). [ESTABLISHED: booklet section 8.2]
- Never lay out hot per-voice state as an array of structs (M8 SoA rule). [ESTABLISHED: booklet section 8.4]
- Never adopt prefetch, non-temporal stores, or huge pages without a bench/soak number attached (M8). [ESTABLISHED: booklet sections 8.4, 8.5]

## Decisions you must not invent (OPEN register)

| decision | status | owner row |
|---|---|---|
| lock-refusal go-live policy: degrade-unlocked-and-tell vs refuse-to-start | NEEDS-INPUT (product) | M5/M6; booklet section 8.1 |
| RT stack budget per thread class | ASSUMED 1 MiB; ratchet from soak watermarks | M7 |
| pool handle bit split and per-pool capacities | ASSUMED 20 index / 12 generation; capacities from the memory plan | M3 |
| working-set budget fractions | ASSUMED 32 KiB hot / 768 KiB block; confirm by bench | M8 |
| P-core-only budgeting vs E-core-worst-case | NEEDS-INPUT — follows the placement policy | M8; reference/optimization_microarch_manifest.md section P9 |
| Windows working-set headroom | ASSUMED +16 pages min / +64 pages max, from the measured battery | M6 |
| huge-page adoption threshold | measured-only; revisit when sample sets reach hundreds of MB | M8; hub H7 mechanisms |
| scratch poison-on-reset pattern and dev-only scope | ASSUMED `0xDD`, dev builds only | M4 |
