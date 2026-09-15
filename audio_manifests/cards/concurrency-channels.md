# Card: concurrency channels

**Five channel shapes cover the plane boundary — wait-free on the RT side, bounded, overflow policy declared, drops counted. Nothing else crosses.**

Facts verified 2026-08-12. Version-dependent claims route to reference/audio_platform_baseline_manifest.md (the hub); if any file disagrees with the hub, the hub wins.
Reasoning root: the child booklet `realtime-audio-pc-architecture-and-design-r1.md` (repo root). This card operationalizes it; it never re-argues it.

**Load when:** data must cross a thread or plane boundary; implementing, selecting, or reviewing a channel; designing shutdown.
**Depth:** reference/concurrency_channels_manifest.md. Plane rules the channels serve: cards/write-rt-code.md.

## The standard this card serves

**Wait-free means THIS thread completes THIS operation in a bounded number of its own steps regardless of every other thread — including a dead one** [ESTABLISHED: booklet section 6.2, after Herlihy]. Every channel's RT side meets that bar; every channel declares its overflow policy; drops are counted, never silent [ESTABLISHED: booklet ch. 3 invariant 2].

## Selection — walk the tree, first yes decides (DT-2/DT-3 condensed)

**INTO the RT plane** [ESTABLISHED: booklet section 6.4]:

| question | channel |
|---|---|
| one independent scalar (or several, each independently consistent)? | (a) atomic parameter — RT side reads a *target*, smooths per its contract |
| ordered, grouped-atomic, or sample-timestamped? | (b) SPSC command ring — a group travels as one message; the block splits at event timestamps |
| structural — internal pointers, multi-word consistency, kilobytes? | (c) snapshot swap — built off-plane, published whole |
| newest wins, history worthless? | (d) triple-slot mailbox |
| none of the above? | the design is making the RT plane *ask* — pull is the wrong direction; restate as pushable data or as work the plane should not do |

**OUT of the RT plane** [ESTABLISHED: booklet section 6.4]:

| question | channel |
|---|---|
| loss acceptable if counted (meters, spectra, taps)? | (d) latest-only, or (b) outward with drop counters if sequence matters |
| every record must survive (flight-ring events, xrun records)? | (b) outward, sized so overflow is a design-error alarm |
| tiny always-current gauge cluster (position, transport)? | (e) seqlock |
| big and must survive (captures, full-res analysis)? | pool blocks pre-handed inward via (b), returned outward via (b) — ownership transfer, zero copy, zero RT allocation |

## The five shapes — contract highlights and which implementation to copy

Copy the reference implementation; never rewrite one from memory.

| shape | copy from | contract you must not break | cost |
|---|---|---|---|
| (a) atomic parameter | reference/concurrency_channels_manifest.md section C6 | one writer; release-store / acquire-load (or relaxed where the value pairs with nothing); naturally aligned ≤ pointer width so it never tears; RT consumes as target + ramp | ~nothing [ESTABLISHED: booklet section 6.3] |
| (b) SPSC ring | reference/concurrency_channels_manifest.md section C2 | one producer, one consumer; each index written by one side; acquire/release on index publication; capacity a power of two (wrap = mask); head/tail on separate cache lines; each side caches the peer's index, refreshing only on apparent full/empty | a few ns/element; capacity resident forever [ESTABLISHED: booklet section 6.3] |
| (c) snapshot swap | reference/concurrency_channels_manifest.md section C3 | build completely off-plane; publish with one release-store; RT acquires **once per block**, never mid-block; retire old only after the RT generation counter proves the plane moved past it; published object is immutable | double-buffered structure; one-block retire latency [ESTABLISHED: booklet section 6.3] |
| (d) mailbox | reference/concurrency_channels_manifest.md section C4 | three slots; writer exchanges filled slot for "latest", reader exchanges "latest" for its held slot; both sides one atomic exchange; never reports full; intermediate values drop by design | 3 payload copies resident [ESTABLISHED: booklet section 6.3] |
| (e) seqlock | reference/concurrency_channels_manifest.md section C5 | writer (RT) wait-free: sequence odd → write fields → sequence even; reader retries on torn window; write rate ≤ once per block bounds reader starvation | trivial [ESTABLISHED: booklet section 6.3] |

`_Alignas(64)` for the cache-line separation and C17 `stdatomic.h` acquire/release compile clean on both legs [MEASURED 2026-08-12: CLANG64 clang 22.1.8].

## Memory ordering — the four blessed idioms

C11 model only, explicit orderings only; the compiler is the adversary, not x86 [ESTABLISHED: booklet section 6.6]. Every atomic use cites its idiom in a comment; a bare default (seq_cst) atomic is treated as unreviewed code.

1. Release-store / acquire-load publication — channels (a), (b), (c).
2. Relaxed counters — statistics, generation stamps; anything read for trend, never for ordering.
3. Acquire-release RMW on exchange slots — channel (d).
4. The seqlock's paired sequence protocol — channel (e).

```c
/* idiom 1: release/acquire publication (R6) */
atomic_store_explicit(&box->snap, new_snap, memory_order_release);   /* control: publish */
const schedule_t *s = atomic_load_explicit(&box->snap, memory_order_acquire); /* RT: once per block */
```

Standalone fences appear only inside channel implementations, never in kernels or shell logic [ESTABLISHED: booklet section 6.6]. A new channel shape requires a written happens-before argument in review (route: contract-only) with the stress suites and the Linux race-detector lane as the net under it.

## Overflow policy — declared per channel, at creation

| traffic | policy |
|---|---|
| commands inward | **reject and report** — never silently drop half a group; size for the worst legitimate burst (automation dump, control sweep) [ESTABLISHED: booklet section 6.4] |
| meters/analysis outward | latest-wins by design (d), or counted drops (b) |
| flight-ring events | sized so overflow alarms; drops counted **and alarmed** [ESTABLISHED: booklet section 6.4; ch. 3 invariant 13] |

## The RT worker join (C7)

Fork-join inside the block uses a **fixed pool** created at the root, elevated and placed like its master; the join waits via the eventcount hybrid — spin briefly, then park on the OS primitive [ESTABLISHED: booklet section 6.5]. Work assignment is static per schedule — no work-stealing: steal deques buy load balance with CAS traffic and unbounded steal attempts, which have no place inside a deadline — and the pool never exceeds the physical P-cores available to the process; oversubscribed RT threads do not overlap, they queue [ESTABLISHED: booklet section 6.5]. Implementation to copy: reference/concurrency_channels_manifest.md section C7.

## Shutdown protocol (C9 condensed)

Two-phase termination, end to end [ESTABLISHED: booklet section 6.8]: signal intent (a command in-ring) → RT fades to silence → stop the device pacing → join RT workers and threads in reverse creation order → drain and persist the flight ring's tail → free. Stream-contract changes (rate/format/period/device) are a stop-and-restart of the composition root's tail, not a swap; graph-only changes ride the snapshot swap without stopping. A teardown that can hang — a worker parked on an eventcount nobody signals, a drain on a ring nobody fills — is a named defect class with its own tests (route: host-test-catchable shutdown storms).

## Stress tests owed (C8 condensed)

Channel code is never done at "it works": **channel torture** — full/empty boundary races on every ring, swap/retire generation races, seqlock read-retry storms, mailbox exchange storms — plus **shutdown storms** under adversarial timing [ESTABLISHED: booklet section 14.4]. These run under TSan on the **Linux leg only** — the TSan runtime is absent from CLANG64 [MEASURED 2026-08-12: no tsan in clang runtime libs]; the C11-model discipline is what makes one leg's detection speak for both, since the code under test is identical [ESTABLISHED: booklet section 10.8].

## Never

- Invent a sixth shape without the written happens-before argument and review (route: contract-only) [ESTABLISHED: booklet section 6.6].
- Mutate a snapshot after publication — a data race wearing a design pattern's name [ESTABLISHED: booklet section 6.3].
- Retire the old snapshot without generation proof (route: host-test-catchable + TSan lane).
- Acquire the snapshot pointer more than once per block — one coherent world per block [ESTABLISHED: booklet section 6.3].
- Use (a) for values that must be seen together — coherence across values is (c)/(d) territory.
- Smuggle a pointer through a parameter channel — an ownership transfer nobody contracted [ESTABLISHED: booklet section 4.3].
- Share a cache line between producer and consumer indices (route: compiler-catchable static assert on layout) [ESTABLISHED: booklet section 6.3].
- Drop anything silently, anywhere (route: runtime-catchable counters) [ESTABLISHED: booklet ch. 3 invariant 2].
- Let the RT side wait, retry-loop, or CAS-spin on a peer [ESTABLISHED: booklet section 6.2].

## Decisions you must not invent

- Ring capacities — sized from the product's worst legitimate burst per ring [OPEN NEEDS-INPUT].
- Which outward meter traffic uses (b)-with-counters vs (d) — per-consumer product decision [OPEN NEEDS-INPUT].
- Streaming-worker prefetch depth — [OPEN NEEDS-INPUT; booklet section 6.5 makes it a product parameter].
- Flight-ring depth — [OPEN ASSUMED: the sizing rule in reference/observability_flightring_manifest.md section O3; alarm-on-overflow stands regardless].

## What you owe when done

Per reference/testing_verification_manifest.md section T11: the channel's **contract suite** green (wait-free claims exercised at full/empty boundaries), the **stress/torture suite** extended and green on the Linux TSan lane, **drop/high-water counters** wired into the observability canon (reference/observability_flightring_manifest.md section O5), and shutdown-storm coverage if the channel participates in teardown. The gate ledger reference/quality_gates_ci_manifest.md section G1 carries the TSan lane per commit via config/check.sh. A torture failure must print the channel, the interleaving seed, and the violated contract clause — self-locating, per the doctrine.

## Go deeper

| question | where |
|---|---|
| the full decision tree with edge cases | reference/concurrency_channels_manifest.md section C1 |
| SPSC ring reference implementation | reference/concurrency_channels_manifest.md section C2 |
| snapshot swap + generation reclaim | reference/concurrency_channels_manifest.md section C3 |
| mailbox and seqlock implementations | reference/concurrency_channels_manifest.md sections C4, C5 |
| atomic params + smoothing | reference/concurrency_channels_manifest.md section C6 |
| RT worker pool + eventcount join | reference/concurrency_channels_manifest.md section C7 |
| torture recipes, exactly | reference/concurrency_channels_manifest.md section C8 |
| shutdown protocol, normatively | reference/concurrency_channels_manifest.md section C9 |
| why no locks — the settled argument | booklet section 6.2 |
