# Concurrency Channels — Cross-Plane Reference Implementations

**Purpose.** The five channel shapes that carry **everything** that crosses the RT/control plane boundary — the selection trees, full C17 reference implementations (SPSC ring, snapshot swap, triple-slot mailbox, seqlock, atomic params), the RT worker pool with its eventcount join, the torture recipes that keep the channels honest, and the shutdown protocol that takes them down without hanging.

Facts verified 2026-08-12. Version-dependent claims route to reference/audio_platform_baseline_manifest.md (the hub); if any file disagrees with the hub, the hub wins.

Reasoning root: the booklet `realtime-audio-pc-architecture-and-design-r1.md` (repo root) — ch. 6 whole, 4.3, 12.6. This file operationalizes it; it never re-argues it.

**Scope split.** Plane membership, banned operations, the RT guard, and the memory-ordering *idiom registry* live in reference/rt_plane_rules_manifest.md (R1, R2, R4, R6); this file implements the idioms. Channel storage residency → reference/memory_residency_manifest.md sections M2/M8. Test harness mechanics → reference/testing_verification_manifest.md section T7. Quick route: cards/concurrency-channels.md.

**Tag legend.** ESTABLISHED (named primary source) · VERSION-DEPENDENT (- hub H&lt;n&gt;) · MEASURED (run on this machine, command recorded) · OPEN (project decision: ASSUMED = default until overridden, NEEDS-INPUT = blocked on the human) · CC-FACT (model knowledge of API/OS mechanics, no named primary source) · FLAGGED-SECONDARY · UNVERIFIED.

**Code status.** Every C snippet below was concatenated into one TU and passed `clang -std=c17 -Wall -Wextra -Wno-unused-function -fsyntax-only` on CLANG64 clang 22.1.8, target x86_64-w64-windows-gnu [MEASURED 2026-08-12]. Pure `stdatomic.h` core in C2–C6 (no platform headers); C7/C9 name thread-port primitives only as `extern` declarations.

---

## C1. Channel selection decision tree

Five shapes cover the boundary; **nothing else crosses** [ESTABLISHED: booklet 6.3]. Selection is a composition-root decision, recorded per traffic class — an ad-hoc channel invented mid-feature is a review reject (contract-only; register it in reference/rt_plane_rules_manifest.md section R8).

### DT-2 — data INTO the RT plane (walk in order; first yes decides)

| # | question | channel | go to |
|---|---|---|---|
| 1 | one independent scalar (or a few, each independently consistent)? | (a) atomic param, RT-side smoothing per its declared semantics | C6 |
| 2 | must changes arrive in order, grouped atomically, or timed to a sample? | (b) SPSC command ring: a group travels as ONE message; sample-accurate events carry frame timestamps and the block splits on them | C2 |
| 3 | structural — internal pointers, consistency spanning many words, or KB-sized? | (c) snapshot swap, built complete off-plane, published whole | C3 |
| 4 | "newest wins, history worthless"? | (d) triple-slot mailbox | C4 |
| 5 | none of the above | design smell: the RT plane is *pulling*. Restate as data the control plane pushes, or move the work off-plane (disk streaming = control-plane worker + ring of filled pool buffers) | what-crosses-where table, last row |

[ESTABLISHED: booklet 6.4 DT-2]

### DT-3 — data OUT of the RT plane

| # | question | channel | go to |
|---|---|---|---|
| 1 | loss acceptable if counted? (meters, spectra, debug taps) | (d) if latest-only; (b) outward with drop counters if the consumer wants the sequence | C4 / C2 |
| 2 | must every record survive? (flight-ring events, xrun records) | (b) outward, sized so overflow is a design-error signal; drops counted AND alarmed, not merely counted | C2; sizing → reference/observability_flightring_manifest.md section O3 |
| 3 | tiny always-current gauge cluster? (position, transport) | (e) seqlock | C5 |
| 4 | big AND must survive? (captured buffers, full-res analysis) | RT writes into pool blocks handed to it in advance; ownership travels IN via (b), back OUT via (b); bulk never copies, RT never allocates | C2 + reference/memory_residency_manifest.md section M3 |

[ESTABLISHED: booklet 6.4 DT-3]

### What crosses where — the standing assignment

Reviews argue about deviations from this table, not about the menu [ESTABLISHED: booklet 6.3].

| traffic | channel | section |
|---|---|---|
| independent parameter targets | (a) atomic params | C6 |
| grouped/ordered commands; sample-accurate events | (b) SPSC ring inward | C2 |
| new schedule, resource tables, impulse responses, wavetables | (c) snapshot swap | C3 |
| meter/analysis frames outward | (d) mailbox — or (b) outward where every frame matters and loss must be counted | C4 / C2 |
| flight-ring events, histograms | (b) outward, drops counted + alarmed | C2 + O3 |
| stream position / transport gauges | (e) seqlock | C5 |
| streaming audio from disk | control-plane worker fills pool buffers, hands them in via (b) | C2 + M3 |

### Never (RT side of any channel)

| rule | route |
|---|---|
| Never a mutex, spinlock, try-lock, or CAS retry loop on the RT side — a lock's worst case on a desktop kernel cannot fit a millisecond budget [ESTABLISHED: booklet 6.2] | analysis-catchable (poison list config/rt_prelude_poison.h) + runtime-catchable (RT guard, reference/rt_plane_rules_manifest.md section R4) |
| Never allocate channel storage after go-live — all channel memory is immortal-arena, sized at the root [ESTABLISHED: booklet 6.3, invariant 3] | runtime-catchable (guard traps allocator on RT threads) + build-catchable (arena audit, reference/quality_gates_ci_manifest.md section G3) |
| Never a pointer through a param or a seqlock — pointers cross only via (c) with the reclaim protocol, or as pool-block ownership via (b) [ESTABLISHED: booklet 4.3] | compiler-catchable (param/seqlock payload types are value-only by API shape) |
| Never a bare `atomic_*` without `_explicit` ordering + an idiom comment — default seq_cst is unstated intent and buys a fence per store on x86 [ESTABLISHED: booklet 6.6] | build-catchable (source grep for non-`_explicit` stdatomic calls in RT TUs — register the audit in G3) |
| Never sleep-to-poll or yield-as-sync on the RT plane [ESTABLISHED: booklet 6.7] | analysis-catchable (poison list) + contract-only elsewhere |
| Never a standalone fence outside a channel implementation — the channels ARE the concurrency API [ESTABLISHED: booklet 6.6] | build-catchable (grep `atomic_thread_fence` outside `chan_*.c/h` — G3 audit row) |

### Decisions you must not invent (OPEN register for this file)

| decision | status |
|---|---|
| command-ring capacity (worst legitimate burst: control-surface sweep, automation dump) | [OPEN NEEDS-INPUT; ASSUMED 1024 records until product data exists] |
| command record size (fixed-size union; larger payloads become resources via C3) | [OPEN ASSUMED: 64 B/record] |
| flight-ring capacity + alarm threshold | owned by reference/observability_flightring_manifest.md section O3 [OPEN there] |
| smoothing ramp default (shape, ms) | [OPEN ASSUMED: linear re-aim, 5 ms; product decides per param — C6] |
| worker spin budget | [OPEN ASSUMED: ≈ measured fork latency; tune per P2 bench — C7] |
| pool width on the reference machine | ≤ 8 RT render threads total (8 P-cores) [MEASURED 2026-08-12 machine facts; hub H2] — C7 |
| shutdown join deadline per thread | [OPEN ASSUMED: 500 ms/join, then E9 harvest + abort — C9] |
| fade-out duration at shutdown | [OPEN NEEDS-INPUT: product; C9 assumes 10–50 ms class] |

---

## C2. SPSC ring

The parent's canonical channel, with three platform tightenings: separated index cache lines, power-of-two capacity (wrap = mask), and cached peer indices so the common-case crossing cost is one uncontended load-and-store pair [ESTABLISHED: booklet 6.3(b), Disruptor-lineage batching].

### Contract

| clause | statement | route |
|---|---|---|
| topology | ONE producer thread, ONE consumer thread, both named at the composition root; a second producer is a different channel instance | contract-only (thread inventory, R1) + host-test-catchable (TSan stress, C8) |
| element | fixed-size POD, `memcpy`-safe; no pointers to non-immortal storage | compiler-catchable (API takes size at init; record types audited in review) |
| capacity | power of two; checked at init; indices are free-running counters, wrap by mask — correct across counter wrap because unsigned arithmetic is modular [ESTABLISHED: C17 6.2.5] and capacity divides 2^64 | runtime-catchable (init returns false → named startup error, reference/error_tracing_contract_manifest.md section E3) |
| progress | push and pop are wait-free per op: bounded steps regardless of peer state, including a dead peer [ESTABLISHED: booklet 6.2, Herlihy's wait-free definition] | host-test-catchable (contract suite T7 asserts no unbounded loop by construction/review) |
| overflow | push on full COMPLETES by returning false and bumping the drop counter — policy per traffic class below | host-test-catchable (boundary storm, C8) |
| residency | `slots` points into the immortal arena (M2); ring struct itself immortal | build-catchable (G3 arena audit) |

### Reference implementation — struct + init

```c
#include <stdatomic.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>
#include <string.h>

typedef struct {
    _Alignas(64) atomic_size_t head;   /* producer line: producer writes head */
    size_t tail_cache;                 /* producer's stale copy of tail       */
    _Alignas(64) atomic_size_t tail;   /* consumer line: consumer writes tail */
    size_t head_cache;                 /* consumer's stale copy of head       */
    _Alignas(64) atomic_uint_fast64_t dropped; /* producer bumps on overflow  */
    _Alignas(64) size_t mask;          /* capacity - 1; immutable after init  */
    size_t elem_size;                  /* immutable after init                */
    unsigned char *slots;              /* immortal arena, capacity*elem_size  */
} spsc_ring;

static bool spsc_init(spsc_ring *r, void *slots, size_t capacity, size_t elem_size)
{
    if (capacity == 0u || (capacity & (capacity - 1u)) != 0u) return false;
    r->mask = capacity - 1u;
    r->elem_size = elem_size;
    r->slots = slots;
    r->tail_cache = 0u;
    r->head_cache = 0u;
    atomic_init(&r->head, 0u);
    atomic_init(&r->tail, 0u);
    atomic_init(&r->dropped, 0u);
    return true;
}
```

`_Alignas(64)` splits producer-owned and consumer-owned state onto separate cache lines — on one line, every push invalidates every pop's cached index and the channel's cost triples [ESTABLISHED: booklet 6.3(b)]. `head`+`tail_cache` share the producer's line by design (both touched only by the producer). Line size 64 B on the reference class [MEASURED 2026-08-12 machine facts; hub H8].

### push / pop

```c
static bool spsc_push(spsc_ring *r, const void *elem)
{
    size_t head = atomic_load_explicit(&r->head, memory_order_relaxed);
    if (head - r->tail_cache > r->mask) {                    /* looks full   */
        r->tail_cache = atomic_load_explicit(&r->tail, memory_order_acquire);
        if (head - r->tail_cache > r->mask) {                /* really full  */
            atomic_fetch_add_explicit(&r->dropped, 1u, memory_order_relaxed);
            return false;                    /* wait-free: bounded, complete */
        }
    }
    memcpy(r->slots + (head & r->mask) * r->elem_size, elem, r->elem_size);
    atomic_store_explicit(&r->head, head + 1u, memory_order_release);
    return true;
}

static bool spsc_pop(spsc_ring *r, void *out)
{
    size_t tail = atomic_load_explicit(&r->tail, memory_order_relaxed);
    if (tail == r->head_cache) {                             /* looks empty  */
        r->head_cache = atomic_load_explicit(&r->head, memory_order_acquire);
        if (tail == r->head_cache) return false;             /* really empty */
    }
    memcpy(out, r->slots + (tail & r->mask) * r->elem_size, r->elem_size);
    atomic_store_explicit(&r->tail, tail + 1u, memory_order_release);
    return true;
}
```

### Why each ordering (the idiom map — registry: R6)

| op | ordering | why |
|---|---|---|
| load own index (`head` in push, `tail` in pop) | relaxed | single writer of that index is this thread; no synchronization carried [ESTABLISHED: C17 7.17.3 per-object coherence suffices] |
| refresh peer cache (`tail` in push, `head` in pop) | acquire | pairs with the peer's release below: push's acquire of `tail` proves the consumer's `memcpy`-out completed before the slot is overwritten; pop's acquire of `head` proves the producer's `memcpy`-in completed before the slot is read [ESTABLISHED: booklet 6.6 release/acquire publication idiom] |
| publish own index after `memcpy` | release | makes the slot contents visible to the peer's acquire — safe-publication [ESTABLISHED: booklet 6.6] |
| `dropped` counter | relaxed | read for trend, not ordering; single writer [ESTABLISHED: booklet 6.6 relaxed-counter idiom] |

The cached-index refresh happens only when the cached value says full/empty — the common case crosses no shared line except the owner's own publication store [ESTABLISHED: booklet 6.3(b)].

### Overflow policy hooks — per traffic class, declared at init time

| traffic | policy on full | traceability duty |
|---|---|---|
| commands inward | REJECT AND REPORT: caller keeps the message and emits a named error carrying the command id + sequence — never silently drop half a group [ESTABLISHED: booklet 6.4] | error code from the E3 registry; message per reference/error_tracing_contract_manifest.md section E6 (what/where/why + command identity) |
| meter/analysis outward | count-and-continue; `dropped` is a canonical counter with an id from reference/observability_flightring_manifest.md section O5 | drops visible in the session report (O7) |
| flight-ring events outward | count AND alarm: nonzero drops trip the supervisor (O6) because a lossy flight ring is a design-error signal [ESTABLISHED: booklet 6.4, invariant 13] | alarm event with ring id + high-water mark |

The reference implementation bumps `dropped` unconditionally; the reject-and-report duty is the CALLER's, so command senders wrap `spsc_push` in a helper that owns the error emission (self-locating failure: the report names the ring, the command, and the fill level — the doctrine's WHAT/WHERE/WHY).

### Tests (pointers; harness mechanics in T7)

| test | asserts | route |
|---|---|---|
| FIFO property: sequence-numbered elements, randomized burst push/drain | order preserved; `pops + resident + dropped == pushes` | host-test-catchable (reference/testing_verification_manifest.md section T7) |
| boundary storm at capacity 1 and 2 | full/empty edges exact; no lost or duplicated element | host-test-catchable (C8 recipe) |
| index-wrap test: test-only init sets `head = tail = SIZE_MAX - 3` | mask math survives counter wrap | host-test-catchable |
| two-thread race storm under TSan | no data race reported | host-test-catchable — Linux leg ONLY: TSan runtime is absent on CLANG64 [MEASURED 2026-08-12]; matrix → hub H5, legs → reference/testing_verification_manifest.md section T8 |

---

## C3. Snapshot swap + generation reclaim

For structure — the compiled schedule, an impulse response, a resource table. Publish-and-retire: control builds the new object COMPLETE off-plane, publishes one pointer with a release-store; RT acquires the pointer ONCE per block and uses it without copying; the old object retires on a generation protocol. Single-reader epoch reclamation [ESTABLISHED: booklet 6.3(c)].

### Contract

| clause | statement | route |
|---|---|---|
| immutability | the published object is never mutated again — a "snapshot" anyone mutates after publication is a data race wearing a design pattern's name [ESTABLISHED: booklet 6.3(c)] | host-test-catchable (TSan stress, hazard table below) + compiler-catchable assist (`const engine_schedule *` API) |
| acquire cadence | RT acquires ONCE per block, never mid-block — one coherent world per block [ESTABLISHED: booklet 6.3(c)] | contract-only + host-test-catchable (offline harness renders with per-block swap storms and asserts single-acquire via instrumented slot) |
| retire | control retires the old object only after quiescence proof (below) or with the stream stopped | host-test-catchable (poison-on-retire stress, C8) |
| cost | double-buffering across the swap window; retire latency ≥ 1 block — both accepted by design [ESTABLISHED: booklet 6.3(c)] | contract-only |
| state migration | a new schedule points surviving nodes into the SAME state-arena slots — migration resolved at schedule-compile time, not at swap time [ESTABLISHED: booklet 6.4] | host-test-catchable (T4 golden: swap mid-note, no state reset audible) |

### Reference implementation

```c
typedef struct engine_schedule engine_schedule; /* immutable after publish */

typedef struct {
    _Alignas(64) _Atomic(const engine_schedule *) live; /* control publishes */
    _Alignas(64) atomic_uint_fast64_t block_gen;        /* RT stamps         */
} sched_slot;

static inline const engine_schedule *sched_acquire(sched_slot *s)
{   /* RT plane: exactly once per block, at block start */
    return atomic_load_explicit(&s->live, memory_order_acquire);
}

static inline void sched_stamp(sched_slot *s)
{   /* RT plane: at block end, after the last touch of the snapshot */
    atomic_fetch_add_explicit(&s->block_gen, 1u, memory_order_release);
}

static inline const engine_schedule *sched_publish(sched_slot *s,
                                                   const engine_schedule *fresh)
{   /* control plane: fresh is COMPLETE and will never be mutated again */
    const engine_schedule *old =
        atomic_load_explicit(&s->live, memory_order_relaxed);
    atomic_store_explicit(&s->live, fresh, memory_order_release);
    return old; /* retire only after sched_quiescent() or stream stopped */
}

static inline uint_fast64_t sched_gen_now(sched_slot *s)
{
    return atomic_load_explicit(&s->block_gen, memory_order_acquire);
}

static inline bool sched_quiescent(sched_slot *s, uint_fast64_t gen_at_publish)
{   /* control plane polls this (it may sleep between polls; shell owns wait) */
    return atomic_load_explicit(&s->block_gen, memory_order_acquire)
           >= gen_at_publish + 2u;
}
```

The core exposes only the quiescence QUERY; the control shell owns the waiting loop (it may sleep) and its timeout — a bounded wait per the control plane's rules, with timeout → named error + diagnosis, never an infinite poll (reference/error_tracing_contract_manifest.md section E3).

### The retire protocol, operational

1. Build `fresh` completely in a control-plane arena; run its self-checks (schedule validation is a control-plane luxury — spend it).
2. `old = sched_publish(slot, fresh); g0 = sched_gen_now(slot);` — read the generation AFTER the publish.
3. If the stream is NOT running (device loop stopped/parked — a control-plane-owned fact), retire `old` immediately: no RT reader exists. The stopped fact must carry a happens-before edge: thread join, or an acquire-read of the loop's stopped/parked flag that the loop release-stores after its final block (and so after its last touch of the snapshot). A stop believed but not synchronized is not a stop for reclaim purposes. **This branch is mandatory**: waiting for generation advance while the device loop is parked is a designed hang (C9 hang class 2). Route: host-test-catchable (shutdown-with-pending-retire test).
4. Else poll `sched_quiescent(slot, g0)` at control cadence; when true, retire `old` (return its arena/pool block — reference/memory_residency_manifest.md section M3).

**Why `g0 + 2`, not `+ 1`**: the block that stamps `g0+1` may have acquired the pointer BEFORE the publish and legitimately renders the old snapshot to its end; the first stamp that can only come from a block that STARTED after the publish landed is `g0+2` [ESTABLISHED: booklet 6.3(c) grace protocol, operationalized].

**Ordering fine print** (two rows, then move on):

- The stamp is `release` and the control-side reads are `acquire` so that "quiescent observed" carries a happens-before edge from the RT plane's last touch of `old` to the retire/free — without that pair the free formally races with the RT reads even on x86-TSO, and the Linux TSan lane would flag exactly that [CC-FACT: C11 happens-before reasoning; TSan honors orderings]. Booklet 6.6 classes generation stamps "relaxed (trend reads)" — that classification covers TELEMETRY consumers of the counter (heartbeat, O6); the reclaim read-back is the one consumer that needs the edge, and this file tightens it deliberately.
- The `+2` rule assumes a published pointer becomes visible to the RT plane's next block-start acquire — guaranteed in practice because store visibility (ns) ≪ block duration (ms class); the C17 model promises only "visible in a finite period" [ESTABLISHED: C17 7.17.3 note on visibility; gap reasoning CC-FACT]. Where a proof-grade edge is wanted, use the paranoid variant: RT mirrors the acquired pointer into a second atomic (`live_seen`, release-store once per block); control waits for `live_seen == fresh` — equality with the NEW pointer, so pointer reuse (ABA) cannot fool it [CC-FACT: single-slot hazard-pointer reduction]. Same API shape; +8 bytes. [OPEN ASSUMED: generation protocol as primary; adopt the mirror if the TSan lane ever reports the retire edge]

### Hazards → the test that catches each

| hazard | defect | catching test | route |
|---|---|---|---|
| publish-before-complete | pointer stored before object finished (missing release, or built in place) | stress: every snapshot carries a trailing checksum; fake-RT reader validates checksum on every acquire under swap storm; TSan (Linux leg) flags the unsynchronized field | host-test-catchable (T7 + T8) |
| retire-too-early | grace protocol skipped or `+1` used | poison-on-retire: retire path memsets `0xDD` before freeing; reader checksum fails loudly; ASan flags use-after-free when snapshots are heap-backed in the harness — ASan present BOTH legs [MEASURED 2026-08-12: `-fsanitize=address` links and runs clean on CLANG64] | host-test-catchable |
| mutate-after-publish | builder keeps writing the live object | TSan writer-vs-reader race (Linux leg); plus a negative meta-test that INTENTIONALLY mutates and asserts the detector fires — a silent detector is a broken lane | host-test-catchable (C8 meta-test) |

---

## C4. Triple-slot mailbox

Latest-wins bulk state — a meter frame, an analysis spectrum, a control-surface state block. Three slots: writer owns one, reader owns one, `latest` holds the third; each side swaps by ONE atomic exchange. Both sides wait-free; intermediate values drop BY DESIGN; unlike the ring it never reports full [ESTABLISHED: booklet 6.3(d) — the booklet's own editorial contract for the three-slot form].

### Reference implementation

```c
#define MB3_FRESH 0x4u
#define MB3_IDX   0x3u

typedef struct { uint64_t block; float rms[2]; float peak[2]; } meter_frame;

typedef struct {
    _Alignas(64) _Atomic uint_fast32_t latest; /* slot index | MB3_FRESH */
    _Alignas(64) uint_fast32_t wr;             /* writer-owned slot      */
    _Alignas(64) uint_fast32_t rd;             /* reader-owned slot      */
    _Alignas(64) meter_frame slot[3];
} mb3;

static void mb3_init(mb3 *m)
{
    atomic_init(&m->latest, 0u);
    m->wr = 1u;
    m->rd = 2u;
}

static void mb3_publish(mb3 *m, const meter_frame *f) /* one writer thread */
{
    m->slot[m->wr] = *f;
    uint_fast32_t prev = atomic_exchange_explicit(
        &m->latest, m->wr | MB3_FRESH, memory_order_acq_rel);
    m->wr = prev & MB3_IDX;
}

static bool mb3_take(mb3 *m, meter_frame *out) /* one reader thread */
{
    if (!(atomic_load_explicit(&m->latest, memory_order_relaxed) & MB3_FRESH))
        return false;                      /* nothing new since last take */
    uint_fast32_t prev = atomic_exchange_explicit(
        &m->latest, m->rd, memory_order_acq_rel); /* FRESH bit not set */
    m->rd = prev & MB3_IDX;
    *out = m->slot[m->rd];
    return true;
}
```

### Contract + mechanics

| clause | statement | route |
|---|---|---|
| topology | one writer thread, one reader thread (either direction across the planes); the three indices — `latest & MB3_IDX`, `wr`, `rd` — are a permutation of {0,1,2} at every quiescent point: init establishes it, exchanges preserve it | host-test-catchable (T7 invariant check in stress) |
| progress | one `atomic_exchange` per op — wait-free at the C level (no retry loop); single-instruction `XCHG` on x86-64 [ESTABLISHED: booklet 6.3(d); x86 mapping CC-FACT] | host-test-catchable |
| ordering | both exchanges `acq_rel`: writer's release publishes the slot payload; writer's acquire on the received slot pairs with the READER's release handing that slot back, so the reader's in-flight loads of its old slot complete before the writer overwrites it (idiom: acquire-release RMW on exchange slots — R6, booklet 6.6) | host-test-catchable (TSan, Linux leg) |
| freshness | `MB3_FRESH` set only by publish, cleared only by take; `take` returning false = "nothing new", the reader keeps re-reading its own slot freely | compiler-catchable (API shape) |
| loss | drops are the policy; the frame's own `block` stamp makes loss DERIVABLE (gaps in taken stamps), so no drop counter is required — count taken/published in O5 telemetry if the product wants the ratio [ESTABLISHED: booklet 6.3(d); derivability = this file's traceability duty] | contract-only |
| torn values | impossible: slots exchange whole; payload copied only while owned | host-test-catchable (checksum storm, C8) |
| residency + padding | three payload copies resident forever; `_Alignas(64)` on the members keeps `latest` off the payload lines; when the writer is the RT plane and frames are hot, pad each `slot[i]` to a line multiple to stop writer/reader false sharing (cost row → reference/memory_residency_manifest.md section M8) | build-catchable (G3 layout audit) [OPEN ASSUMED: pad slots when payload < 64 B] |

Init state legality: `latest = 0` WITHOUT `MB3_FRESH` means a take before the first publish correctly returns false; `wr=1, rd=2` keeps the permutation.

---

## C5. Seqlock

The inverted channel: the RT plane WRITES wait-free, the control plane retries. For a small, mixed, read-mostly gauge cluster published by RT — stream position, transport state, a few meters — read at UI rate without dedicating a channel per field [ESTABLISHED: booklet 6.3(e)].

### When to use / when not

| use | refuse |
|---|---|
| POD gauge cluster ≤ 1–2 cache lines, RT-written once per block at most, control-read at UI rate | anything with a pointer (the retry protects the WORDS, not the pointee's lifetime — structure rides C3) |
| the always-on "where is the stream" surface; the heartbeat counter of the supervisor (booklet 12.6) rides here | high-rate readers on the RT plane (readers retry — retries are control-plane work) |

### Reference implementation

```c
#define SEQ_WORDS 4u /* payload: SEQ_WORDS * 8 bytes of POD gauges */

typedef struct {
    _Alignas(64) atomic_uint_fast32_t seq; /* odd while RT is writing */
    _Atomic uint64_t w[SEQ_WORDS];         /* payload words           */
} seqgauges;

static void seq_publish(seqgauges *g, const uint64_t src[SEQ_WORDS])
{   /* RT plane writer: wait-free; at most once per block */
    uint_fast32_t s = atomic_load_explicit(&g->seq, memory_order_relaxed);
    atomic_store_explicit(&g->seq, s + 1u, memory_order_relaxed); /* odd  */
    atomic_thread_fence(memory_order_release);       /* odd before data   */
    for (unsigned i = 0; i < SEQ_WORDS; i++)
        atomic_store_explicit(&g->w[i], src[i], memory_order_relaxed);
    atomic_store_explicit(&g->seq, s + 2u, memory_order_release); /* even */
}

static void seq_read(const seqgauges *g, uint64_t dst[SEQ_WORDS])
{   /* control plane reader: retries while a write overlaps */
    for (;;) {
        uint_fast32_t s1 = atomic_load_explicit(&g->seq, memory_order_acquire);
        if (s1 & 1u) continue;                        /* mid-write: retry  */
        for (unsigned i = 0; i < SEQ_WORDS; i++)
            dst[i] = atomic_load_explicit(&g->w[i], memory_order_relaxed);
        atomic_thread_fence(memory_order_acquire);    /* data before check */
        if (atomic_load_explicit(&g->seq, memory_order_relaxed) == s1)
            return;
    }
}
```

### Mechanics rows

| clause | statement | route |
|---|---|---|
| payload representation | relaxed-atomic words, copied through a word loop — NOT plain fields: a discarded torn read of plain memory is still a formal data race in the C model; the atomic-word form is the standard model-clean seqlock [ESTABLISHED: Boehm, "Can seqlocks get along with programming language memory models?", MSPC 2012] | compiler-catchable (API is `uint64_t` words only; struct views live outside the channel via `memcpy`) |
| fence pairing | writer's release fence orders the odd store before the payload stores as observed through any payload read; reader's acquire fence orders payload loads before the `s2` re-check — fence-to-fence synchronization [ESTABLISHED: C17 7.17.4] | host-test-catchable (read storm, C8) |
| writer progress | wait-free: two stores + N payload stores, no waiting on readers ever (idiom: paired sequence-number protocol — R6, booklet 6.6) | host-test-catchable |
| reader starvation | structurally bounded by the WRITE rate: at most one write per block, write duration is ns-class, so a reader overlaps at most one short window per block; a reader that spins forever means the writer is stuck odd — that is a hang signature, not a livelock (feed it to the supervisor, O6) [ESTABLISHED: booklet 6.3(e)] | runtime-catchable (reader retry-count threshold → named error E3) |
| reader loop bound | production readers cap retries (e.g. 1000) and report the retry count on threshold — self-locating: gauge-cluster id + last odd `seq` value | runtime-catchable [OPEN ASSUMED: cap 1000] |

The heartbeat consumer (booklet 12.6): the device loop's block counter is one of the words here; the control-plane supervisor alarms when the stream claims live but the counter stalls — wiring and cadence in reference/observability_flightring_manifest.md section O6.

---

## C6. Atomic params + smoothing

One independent value, one writer (control), read by the RT plane as a TARGET. Control-rate writes and audio-rate consumption decouple: write-target / consume-at-block-start / ramp-across-block [ESTABLISHED: booklet 6.3(a), 4.3].

### Declared semantics — every parameter states one, in the port contract

| semantics | meaning | mechanism |
|---|---|---|
| smoothed(shape, ms) | continuous audio-affecting value (gain, cutoff, mix) | atomic target + RT-side ramp (below); shapes and durations owned by reference/dsp_kernel_patterns_manifest.md section K3 |
| stepped-at-block | value where interpolation is WRONG (mode index, integer count) | atomic target consumed at block start, applied as a step; click risk handled inside the op (crossfade) if audible |
| sample-accurate-event | must land on a frame (note-on at frame 37) | NOT an atomic param: timestamped event through the command ring (C2); the block splits at event boundaries [ESTABLISHED: booklet 4.3, 4.4] |

Zipper rationale, one line: a parameter that steps at a block edge is audible as the zipper artifact, so smoothing is part of the parameter's CONTRACT — ramp shape and duration — not a nicety [ESTABLISHED: booklet 4.3].

### Reference implementation

```c
typedef struct {
    _Atomic float target; /* control writes; RT reads; idiom (b): relaxed independent value */
    float current;        /* RT-owned ramp state (state arena)  */
    float step;           /* per-sample increment, this block   */
} param_smoothed;         /* declared semantics: smoothed(linear re-aim, ramp_ms) */

static inline void param_write(param_smoothed *p, float v)
{   /* control plane, any rate; last write wins (coalescing is the contract); idiom (b) */
    atomic_store_explicit(&p->target, v, memory_order_relaxed);
}

static inline void param_begin_block(param_smoothed *p, float inv_ramp_frames)
{   /* RT plane, once per block, before the op renders; idiom (b) */
    float t = atomic_load_explicit(&p->target, memory_order_relaxed);
    p->step = (t - p->current) * inv_ramp_frames; /* re-aimed every block */
}
/* per sample inside the kernel:  p->current += p->step;  use p->current  */
```

Re-aiming a linear step at the target every block converges exponentially toward it — an acceptable default; exact ramp laws (true linear over N frames, one-pole, equal-power) are K3's table, and a param carrying an audibly wrong default is a K3 defect, not a channel defect. Snap-to-target when `|t - current|` is below an epsilon to stop denormal-feeding tails (hygiene row: reference/dsp_kernel_patterns_manifest.md section K7).

### Rules

| rule | route |
|---|---|
| relaxed is the blessed ordering for INDEPENDENT params — the value pairs with nothing; the moment two values must be seen together, this shape is WRONG: use C2 (grouped command) or C3 (structure) [ESTABLISHED: booklet 6.3(a), 6.6] | contract-only + review; grouped-write misuse surfaces in T5 property tests as torn pairs |
| params never carry pointers — a pointer smuggled through a param is an ownership transfer nobody contracted [ESTABLISHED: booklet 4.3] | compiler-catchable (param slots are `float`/`int32_t` only, by API) |
| one control-plane writer per param slot; two writers = last-wins interleavings TSan cannot flag (atomics are not races) | contract-only (writer named in the param registry) |
| every param's semantics declared in the generated param registry; unstated smoothing is how two builds disagree audibly [ESTABLISHED: booklet 4.3] | build-catchable where the registry is generated (G3 structural audit); contract-only otherwise |
| lock-freedom verified at the composition root before go-live: `atomic_is_lock_free` on one representative of each atomic payload width; refuse to start otherwise with a named E3 error — C17 provides no compile-time macro for `_Atomic float` [ESTABLISHED: C17 7.17.5 lock-free macros cover integer types] | runtime-catchable |
| `_Atomic float` load/store compiles lock-free on the x86-64 legs [MEASURED 2026-08-12: snippet TU compiles clean; lock-freedom asserted at root per row above — CC-FACT for the expectation, the root check makes it a fact per build] | runtime-catchable |

RT-plane feedback values (gain reduction, detected pitch) do NOT write params backward — they leave via C4/C5. Params flow control → RT, period (booklet 4.3 dataflow direction). Route: contract-only.

---

## C7. RT worker pool + eventcount join

Fork-join inside the block, for when the measured schedule cost crowds the headroom floor and latency cannot grow. Walk booklet DT-4 FIRST: shrink the work (P1 ladder), pay with latency (period dial), pipeline (throughput paths) — the pool is the last rung [ESTABLISHED: booklet 6.5].

### Pool rules

| rule | statement | route |
|---|---|---|
| fixed at root | workers created at the composition root, elevated and placed like the device-loop thread (thread port carries plane, stack, priority request, placement hint; the GRANT is reported, not assumed) [ESTABLISHED: booklet 5.3, 6.5] | runtime-catchable (root checks reported grants; shortfall = named E3 error + policy decision) |
| population frozen | RT thread population fixed between go-live and teardown; no worker appears or vanishes mid-stream [ESTABLISHED: booklet 5.3] | runtime-catchable (RT guard traps thread-create on RT plane — R4) |
| static partition | work assignment compiled into the schedule (C3 snapshot) — a schedule swap changes the partition atomically at a block boundary. NO work-stealing on the RT plane: stealing buys load balance with CAS traffic and unbounded steal attempts, which have no place inside a deadline [ESTABLISHED: booklet 6.5] | contract-only + build-catchable (no deque type exists in RT TUs — G3 audit) |
| pool width | total RT render threads (device loop + workers) ≤ physical P-cores available to the process; SMT siblings do not count; E-cores excluded by placement policy. Reference machine: 8 P-cores → ≤ 8 [ESTABLISHED: booklet 6.5, 11.2; machine numbers MEASURED 2026-08-12; hub H2] — oversubscribed RT threads do not overlap, they queue, and elevated queuing is priority inversion against yourself | runtime-catchable (root refuses a pool wider than the reported P-core set) |
| waiting policy | workers use the eventcount hybrid: bounded spin (budget ≈ fork latency to hide), then park on the OS wait primitive; parked blocking when the stream stops [ESTABLISHED: booklet 6.5, 6.7 DT-5] | host-test-catchable (park/unpark storm, C8) + runtime-catchable (guard allows ONLY the sanctioned wait/wake syscalls on RT threads — classification in reference/rt_plane_rules_manifest.md section R7) |
| serial spine honesty | the join, the final mix, and the submit bound the speedup — measure the parallel schedule's TAIL, not its mean, before shipping the complexity (bench: reference/optimization_microarch_manifest.md section P2) [ESTABLISHED: booklet 6.5] | host-test-catchable (T10 bench lane gate) |

### Thread-port wait primitives (the only platform names in this file)

| primitive | Linux leg | Windows leg |
|---|---|---|
| `rtport_wait_u32(addr, undesired)` | `futex(FUTEX_WAIT_PRIVATE)` — kernel re-checks `*addr == undesired` atomically against wakes before sleeping, so a wake between user-space check and sleep is never lost [ESTABLISHED: futex(2)] | `WaitOnAddress` — same compare-and-sleep contract, link `-lsynchronization` (`libsynchronization.a` present on CLANG64). Probe verified: sleeping path returns FALSE + `ERROR_TIMEOUT` when `*addr` matches, immediate TRUE when it differs [MEASURED 2026-08-12: `clang -std=c17 woa_probe.c -lsynchronization` compiles, links, runs on clang 22.1.8; per-wake semantics beyond the probe CC-FACT] |
| `rtport_wake_all_u32(addr)` | `futex(FUTEX_WAKE_PRIVATE, INT_MAX)` [ESTABLISHED: futex(2)] | `WakeByAddressAll` [MEASURED 2026-08-12: same probe] |
| `rtport_spin_relax()` | x86 `pause` via `_mm_pause()` on both legs (ISA floor → hub H8) [CC-FACT: Intel intrinsic] | same |

Adapters live behind the thread port (booklet 5.3); per-leg build rows in reference/toolchain_build_manifest.md section B4.

### Reference implementation — the block gate

```c
extern void rtport_wait_u32(_Atomic uint32_t *addr, uint32_t undesired);
extern void rtport_wake_all_u32(_Atomic uint32_t *addr);
extern void rtport_spin_relax(void);

typedef struct {
    _Alignas(64) _Atomic uint32_t epoch;     /* master bumps to launch     */
    _Alignas(64) _Atomic uint32_t remaining; /* workers decrement on done  */
    _Alignas(64) _Atomic uint32_t quit;      /* control sets at shutdown   */
} block_gate;

static void gate_launch(block_gate *g, uint32_t nworkers)
{   /* device-loop thread, per block, after writing the block's inputs */
    atomic_store_explicit(&g->remaining, nworkers, memory_order_relaxed);
    atomic_fetch_add_explicit(&g->epoch, 1u, memory_order_release);
    rtport_wake_all_u32(&g->epoch);      /* unparks any sleeping worker */
}

static uint32_t gate_await(block_gate *g, uint32_t seen_epoch,
                           uint32_t spin_budget)
{   /* worker: spin briefly, then park — the eventcount hybrid */
    for (uint32_t i = 0; i < spin_budget; ++i) {
        uint32_t e = atomic_load_explicit(&g->epoch, memory_order_acquire);
        if (e != seen_epoch) return e;
        rtport_spin_relax();
    }
    for (;;) {
        uint32_t e = atomic_load_explicit(&g->epoch, memory_order_acquire);
        if (e != seen_epoch) return e;
        rtport_wait_u32(&g->epoch, seen_epoch); /* kernel re-checks value */
    }
}

static void gate_done(block_gate *g)
{   /* worker, after rendering its static partition */
    atomic_fetch_sub_explicit(&g->remaining, 1u, memory_order_release);
}

static void gate_join(block_gate *g)
{   /* device-loop thread: bounded spin — partition bounds worker runtime */
    while (atomic_load_explicit(&g->remaining, memory_order_acquire) != 0u)
        rtport_spin_relax();
}
```

### Worker body

```c
typedef struct { block_gate *gate; uint32_t spin_budget; /* + partition */ } worker_ctx;
extern void render_partition(worker_ctx *w);

static int rt_worker_main(void *arg)
{
    worker_ctx *w = arg;
    uint32_t seen = 0u;
    for (;;) {
        seen = gate_await(w->gate, seen, w->spin_budget);
        if (atomic_load_explicit(&w->gate->quit, memory_order_acquire)) break;
        render_partition(w);  /* ops assigned by the compiled schedule */
        gate_done(w->gate);
    }
    return 0;
}
```

### Ordering + cost rows

| row | statement | route |
|---|---|---|
| launch publishes inputs | `epoch` release / worker `acquire` makes the master's block-input writes (and the `remaining` reset, sequenced before the release) visible to every worker [idiom: release/acquire publication — R6] | host-test-catchable (TSan, Linux leg) |
| join collects outputs | `gate_done` release / `gate_join` acquire carries each worker's partition-output writes to the master before it mixes/submits | host-test-catchable |
| join is a spin, not a park | the master's wait is bounded by the static partition's measured cost — parking the MASTER would put a scheduler visit on the deadline path every block | contract-only + T10 bench (join tail measured) |
| wake syscall economics | `rtport_wake_all_u32` with no parked waiter is the cheap path but still a syscall from the device-loop thread; ELIGIBLE optimization: track a `parked` count and skip the wake when zero — safe ONLY because the kernel/OS re-validates `*addr` under its own lock, so the racing worker never sleeps through a bumped epoch [ESTABLISHED: futex(2) re-check; Windows equivalence CC-FACT]. Adopt only with the park/unpark storm test green | host-test-catchable (C8) [OPEN ASSUMED: plain wake-always until the bench shows the syscall on the tail] |
| spin budget | per-product tune ≈ the fork latency it must hide; too high burns a P-core per worker while idle, too low puts a park/unpark on every block [ESTABLISHED: booklet 6.5] | host-test-catchable (T10: join-latency histogram vs budget sweep) [OPEN ASSUMED: start at ~2000 relax iterations, tune by P2 bench] |
| guard interaction | `rtport_wait/wake` are on the R7 sanctioned-syscall list for RT threads (the ONLY blocking point besides the device pacing wait); everything else the guard traps | runtime-catchable (R4 guard) |

---

## C8. Stress/torture recipes

Channel correctness is claimed by contract and PROVEN by storm. Every recipe below is a host test (T1 topology) that runs threads against a channel instance for a seeded, bounded duration and counts its checks.

### Harness output contract (the doctrine, applied)

A torture run that fails must be patchable from its artifact alone: print `seed`, `duration`, `iterations`, `checked=N failed=M`, and for the FIRST failure: channel id, thread role (producer/consumer/writer/reader/master/worker), element index or generation, expected vs got. `checked=0` with a pass is a BROKEN HARNESS — assert a minimum check count. Naming and machine-readable shape per reference/testing_verification_manifest.md section T2; message grammar per reference/error_tracing_contract_manifest.md section E6. Route: host-test-catchable (the meta-assert on `checked`).

### Recipes

| channel | storm | asserts |
|---|---|---|
| C2 ring | boundary storm: capacities 1, 2, 64; producer pushes random-size bursts, consumer drains with random stalls; both sides yield-free tight loops | FIFO order via sequence numbers; `pops + resident + dropped == pushes`; wrap test with indices initialized near `SIZE_MAX` |
| C2 ring | full-edge flutter: producer holds the ring exactly at full, consumer pops one/pushes race the boundary | no lost slot, no duplicate, drop counter exact |
| C3 swap | swap/retire race: control republishes at ~1 kHz with poison-on-retire (`0xDD` memset) + trailing checksum; fake-RT acquires once per simulated block, validates checksum across the whole object | zero checksum failures; under ASan (both legs) zero use-after-free [MEASURED 2026-08-12: ASan present CLANG64]; under TSan (Linux leg) zero races |
| C3 swap | retire-early NEGATIVE meta-test: a deliberately broken `+1` retire must make the detector fire | the failure is DETECTED — a silent lane is the defect |
| C4 mailbox | cadence mismatch: writer at block cadence, reader at jittered UI cadence, then both at max rate | taken `block` stamps strictly monotonic; frame checksum never torn; index-permutation invariant holds |
| C5 seqlock | read storm: N control readers spin-reading while the RT-sim writer publishes per block; each payload word carries the generation in its high 32 bits, the field id in its low bits | every accepted read has ALL words from one generation; retry counts bounded; no reader starves past the cap |
| C7 gate | park/unpark storm: random spin budgets including 0 (always park) and huge (never park); random inter-block gaps; frequent quit/restart cycles | no missed wake (join always completes under deadline); no lost `remaining` decrement; quit always terminates every worker |

### Where they run

| lane | what | evidence |
|---|---|---|
| Linux leg, TSan | ALL recipes — the race detector is the mechanical net under the happens-before arguments | TSan runtime ABSENT on CLANG64 → Linux-only lane [MEASURED 2026-08-12; VERSION-DEPENDENT - hub H5, re-check on toolchain bumps]; leg wiring → reference/testing_verification_manifest.md section T8 and reference/quality_gates_ci_manifest.md section G5 |
| both legs, ASan + UBSan | C3 poison/UAF recipes; arithmetic in harnesses | ASan and UBSan run clean on CLANG64 [MEASURED 2026-08-12] |
| both legs, plain | all recipes at full speed (sanitizer slowdown hides timing windows — run BOTH sanitized and plain) [CC-FACT: TSan/ASan skew interleavings] | per-change quick versions (seconds) in T7; nightly soak durations (minutes) per T12 cadence |

Assertion counters double as coverage evidence: each recipe reports checks/second into the bench lane so a silent slowdown of the harness itself is visible (T10).

---

## C9. Shutdown protocol

Full shutdown is two-phase termination end to end: signal intent, then dismantle in reverse dependency order [ESTABLISHED: booklet 6.8]. Stream-contract RECONFIGURATION (rate/format/period/device) is this same tail stopped and restarted; graph-only changes ride C3 without stopping [ESTABLISHED: booklet 6.8].

### The order (deviations are defects)

| step | actor | mechanism | failure it prevents |
|---|---|---|---|
| 1. signal intent | control | shutdown command IN the command ring (C2) — the RT plane learns by data, never by signal/kill | RT plane torn mid-block |
| 2. fade | RT | degrade-ladder ramp to silence over the declared duration (duration [OPEN NEEDS-INPUT], booklet ch. 12 ramp) | audible click/pop at stop |
| 3. stop device loop | control → device adapter | stop pacing after fade completes; adapter verbs in reference/device_adapter_manifest.md sections D3/D7 | callback firing into a dismantled graph |
| 4. release eventcounts | control | `pool_release_workers` (below): set `quit` release, bump `epoch`, `wake_all` — BEFORE any join | hang class 1: worker parked forever on a gate nobody signals |
| 5. join workers | control | reverse creation order, each join under a deadline | join ordering deadlocks; a zombie RT thread outliving its arenas |
| 6. drain rings | control | drain flight ring + telemetry OUT-rings to the session report (reference/observability_flightring_manifest.md section O7); drain loop bounded by "ring empty AND producers joined", never "wait for more data" | hang class 2: drain waiting on a ring nobody fills |
| 7. free | control | retire pending snapshots (stream stopped → immediate, C3 step 3), unlock/release arenas (M5/M6), free last | use-after-free during teardown; leaked locked pages |

### Pool release

```c
static void pool_release_workers(block_gate *g)
{   /* control plane: after fade completed and device loop stopped */
    atomic_store_explicit(&g->quit, 1u, memory_order_release);
    atomic_fetch_add_explicit(&g->epoch, 1u, memory_order_release);
    rtport_wake_all_u32(&g->epoch);  /* unpark ALL, so joins can complete */
    /* then: join worker threads in reverse creation order, each join under
       a deadline; on timeout -> dirty-exit harvest (E9), then abort */
}
```

`quit` is stored BEFORE the epoch bump: a worker woken by the bump acquires `epoch`, then reads `quit` — the release on `epoch` carries the `quit` store, so no worker can observe the wake without the reason [idiom: release/acquire publication — R6]. A worker that breaks on `quit` skips `gate_done` by design; nothing joins on `remaining` after step 3.

### Hang classes → the tests that target them

| hang class | test | route |
|---|---|---|
| parked worker nobody signals (quit set but no wake, or wake before quit visible) | shutdown storm: create pool, shut down while workers are (i) parked, (ii) spinning, (iii) mid-render; repeat under randomized timing; every join must complete inside the deadline | host-test-catchable (T7 shutdown suite; harness watchdog converts a hang into a failure artifact) |
| drain waiting on a ring nobody fills | shutdown with (i) empty, (ii) half-full, (iii) exactly-full rings; drain must terminate and the session report must contain every drained record | host-test-catchable |
| wrong order: device stopped before fade completed | offline render of the shutdown sequence; assert the tail envelope decays monotonically to silence (property suite) | host-test-catchable (reference/testing_verification_manifest.md sections T3/T5) |
| double shutdown / shutdown-during-reconfig | idempotence test: second shutdown call is a no-op with a logged event, not a crash | host-test-catchable |
| retire pending during stop | pending C3 retire + immediate shutdown: object retired exactly once, after the joins | host-test-catchable |

### Timeout discipline (traceability at the exit)

Every control-plane join/drain in this protocol carries a deadline [ESTABLISHED: booklet 6.7 — every control wait bounded]. On timeout: capture thread states + the flight ring's tail FIRST (the dirty-exit harvest, reference/error_tracing_contract_manifest.md section E9), emit a named error identifying WHICH step and WHICH primitive timed out (self-locating: step number, thread name, gate/ring id), then abort. A shutdown that hangs silently is the one failure the next session cannot diagnose — the harvest is the artifact that makes the hang patchable. Deadline value [OPEN ASSUMED: 500 ms per join; product may tighten]. Route: runtime-catchable (the deadline) + host-test-catchable (the harvest content asserted in the shutdown suite).
