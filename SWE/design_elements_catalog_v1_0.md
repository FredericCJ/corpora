# SWE Corpus — Design-Element Catalog v1.0 (`design-elements`, realm: design)
**Object.** Named, recurring, implementation-level building blocks and mechanisms of software design — the mid-level vocabulary below software architecture and above raw language syntax. Compiled 2026-07-10 by coverage-driven enumeration: corpus seed-mining (GoF, POSA 1–3, Douglass, Samek, White, Koopman, Pont, Noble–Weir, Hanmer, Hanson/Schreiner/Tornhill/Preschern, Nygard …), web sweeps of the established catalogs (PLoP/Hillside, Nystrom, EIP, Fowler, wikis, language idiom collections), and per-axis gap hunts to saturation (stopping rule: a full kind × source × domain sweep yielding <5 new elements, then one adversarial gap hunt).

**Entry contract.** One element per mechanism (synonyms folded into `aka`); GoF/POSA names canonical for their patterns; every element is named in at least one citable published source (`named-in`; `corpus:<id>` = the work is already in `explorer/data/corpus.json`); `borderline` tags carry a one-line altitude rationale. ids are kebab-case, unique, stable — they become node ids in Phase 4.

**Census.** **708 elements** across 22 kind axes · confidence: 456 established / 252 spot-checked / 0 needs-check · 157 borderline · 203 candidates parked to the architecture realm (Phase 3 input) · 316 notable exclusions.

**Per-axis counts.**

| kind | n |
|---|---|
| data-representation | 33 |
| data-flow-buffering | 28 |
| execution-concurrency | 37 |
| synchronization-coordination | 57 |
| state-management | 33 |
| resource-management | 56 |
| caching-memoization | 16 |
| error-handling | 50 |
| robustness-security | 40 |
| communication | 43 |
| scheduling-time | 25 |
| oo-patterns | 65 |
| construction-api | 29 |
| functional-type-idioms | 26 |
| data-structures | 52 |
| persistence-durability | 29 |
| parsing-text | 20 |
| serialization-framing | 21 |
| numeric-precision | 10 |
| code-structure | 11 |
| testing-constructs | 11 |
| embedded-systems | 16 |
| **total** | **708** |

Kind axes are scaffolding for coverage and readability only — no structural or ontological commitment.

---

## Data representation — `data-representation` (33)

### adjacency-list-adjacency-matrix — Adjacency List / Adjacency Matrix
- aka: adjacency-list representation, adjacency-matrix representation, compressed sparse row (CSR, packed variant)
- kind: data-representation
- what: The two canonical in-memory graph representations: per-vertex edge lists (sparse-friendly, Theta(V+E) space) versus a V-by-V boolean/weight matrix (dense-friendly, O(1) edge test).
- problem: Every graph-processing component must commit to an edge-storage layout; the list/matrix choice trades memory and iteration locality against constant-time adjacency tests.
- named-in: Introduction to Algorithms - Cormen, Leiserson, Rivest, Stein (2009)
- tags: graphs, borderline — Charter-flagged: a representation choice rather than a single structure; kept as ONE element covering the named pair since the choice itself is the recurring design act.

### bytecode — Bytecode
- aka: —
- kind: data-representation
- what: Encode behavior as instructions for a small purpose-built virtual machine and execute it with an interpreter, instead of hard-coding it in the host language.
- problem: Behavior must be data-driven, moddable, hot-reloadable, or sandboxed; native code is too rigid and privileged, while Interpreter-pattern object trees are too slow and memory-hungry.
- named-in: Game Programming Patterns - Robert Nystrom (2014)
- tags: games, scripting

### column-oriented-storage — Column-Oriented Storage
- aka: columnar storage, column store layout, DSM (decomposition storage model)
- kind: data-representation
- what: Store all values of each column contiguously (rather than row by row), typically with per-column compression, so queries read only the columns they touch.
- problem: Analytical scans over wide tables waste I/O and cache on unused columns in row layout; columnar layout minimizes bytes read and makes runs of same-typed values highly compressible and SIMD-friendly.
- named-in: C-Store: A Column-oriented DBMS - Stonebraker et al. (2005)
- tags: db, storage-engine, analytics

### comparand — Comparand
- aka: dedicated comparison value, cheap identity testing value
- kind: data-representation
- what: Equip objects with a dedicated comparand value used solely for cheap identity/equality testing, avoiding expensive structural comparison or unreliable address comparison.
- problem: Identity tests on structured objects are frequent and must be fast; comparing full contents is costly and comparing addresses breaks when objects are copied or serialized.
- named-in: 'The Comparand Pattern: Cheap Identity Testing Using Dedicated Values', PLoPD5 ch. 8 (2006) (Library of Congress ToC loaded live)
- tags: identity, related to interning (sharing, in index) but distinct mechanism, borderline — Obscure; named at chapter-title level in a published volume, mechanism stated in the title. Merge team may fold into sharing/interning if judged too thin.

### compression — Compression
- aka: Table Compression, Difference Coding, Adaptive Compression, compressed in-memory representation
- kind: data-representation
- what: Store data in a compressed representation in memory or storage, decompressing on access, to fit more data in less space.
- problem: Bulk data exceeds available memory; compression trades CPU time for footprint. Noble & Weir's specializations (Table Compression, Difference Coding, Adaptive Compression) are folded here as variants per the no-algorithm-zoo rule.
- named-in: corpus:noblesmallmem — Small Memory Software: Patterns for Systems with Limited Memory - Noble & Weir (2000)
- tags: embedded, memory

### container-of — container_of
- aka: intrusive back-pointer recovery, offsetof-based container access
- kind: data-representation
- what: Recover a pointer to the enclosing struct from a pointer to one of its embedded members via offsetof arithmetic, enabling intrusive/generic embedded nodes.
- problem: Generic subsystems (lists, kobjects, work items) hold pointers to embedded member structs; container_of maps back to the owning object without per-type containers or extra pointers.
- named-in: corpus:ldd3 — Linux Device Drivers, 3rd ed. - Corbet, Rubini & Kroah-Hartman (2005)
- tags: c, linux, embedded

### data-locality — Data Locality
- aka: cache-friendly data layout, structure of arrays / array of structures (SoA/AoS)
- kind: data-representation
- what: Arrange data contiguously in memory in the order it is processed (e.g. packed homogeneous arrays instead of pointer-linked heap objects) to exploit CPU caching.
- problem: Memory access dominates modern performance; pointer-chasing scattered objects thrashes the cache, while contiguous hot data turns cache misses into streaming reads.
- named-in: Game Programming Patterns - Robert Nystrom (2014)
- tags: games, performance, cache

### data-transfer-object — Data Transfer Object
- aka: DTO, Transfer Object
- kind: data-representation
- what: An object that carries data between processes or layers in a single package, with serialization support and no behavior beyond storage.
- problem: Chatty fine-grained remote or cross-layer calls are expensive; batching the needed data into one dumb, serializable object reduces round trips and decouples wire shape from domain shape.
- named-in: Patterns of Enterprise Application Architecture - Martin Fowler (2002)
- tags: enterprise, distribution

### dictionary-encoding — Dictionary Encoding
- aka: dictionary compression, domain encoding, dictionary encoding with patching (variant)
- kind: data-representation
- what: Replace repeated wide values in a column with small fixed-width integer codes indexing a dictionary of the distinct values; operators can often work directly on the codes.
- problem: Low-cardinality columns waste space and memory bandwidth storing the same strings repeatedly; integer codes compress the data and make scans and comparisons cheaper, especially in columnar layouts.
- named-in: Abadi, Boncz, Harizopoulos, Idreos, Madden — The Design and Implementation of Modern Column-Oriented Database Systems (Foundations and Trends in Databases 5(3), 2013)
- tags: databases, columnar

### empty-base-optimization-ebo — Empty Base Optimization (EBO)
- aka: empty member optimization, EBCO
- kind: data-representation
- what: Inherit from (rather than store) an empty policy/allocator class so it occupies zero bytes in the derived object's layout.
- problem: Stateless components stored as members still cost at least one byte plus padding; EBO removes that overhead in size-sensitive generic code.
- named-in: More C++ Idioms - Wikibooks (living); 'The Empty Member C++ Optimization' - Nathan Myers, Dr. Dobb's (1997)
- tags: c++, borderline — Object-layout micro-optimization near the compiler floor; kept because it is named, recurring, and shapes generic-library design.

### entity — Entity
- aka: Reference Object
- kind: data-representation
- what: A domain object defined primarily by a thread of continuity and identity rather than by its attributes, with identity maintained across state changes and representations.
- problem: Some domain objects must be tracked through changes and matched across forms and stores; modeling them around an explicit identity (not attribute equality) prevents mismatches and aliasing errors.
- named-in: Domain-Driven Design: Tackling Complexity in the Heart of Software - Eric Evans (2003)
- tags: ddd, domain-modeling

### entity-component-system — Entity Component System
- aka: ECS, entity system, component entity system
- kind: data-representation
- what: Organize a simulation as plain-id entities, pure-data components stored in contiguous per-type arrays, and systems that iterate over all entities holding a given component set.
- problem: Deep entity class hierarchies cannot express cross-cutting feature combinations and scatter hot data; ECS composes capabilities as data and lets systems process components in cache-friendly batches.
- named-in: Evolve Your Hierarchy: Refactoring Game Entities with Components - Mick West (2007)
- tags: games, performance, borderline — In-process program-organization pattern that verges on engine-level architecture; included per charter - it is implementable inside one program, named, and recurring across codebases.

### error-correcting-codes — Error-Correcting Codes
- aka: ECC, Hamming code, forward error correction, FEC
- kind: data-representation
- what: Encode data with structured redundancy so that a bounded number of bit errors can be not only detected but corrected on read/receive.
- problem: When retransmission or re-read is impossible or too slow, correction must come from the data itself; redundant encodings trade space for self-healing data. Code-family variants (Hamming, Reed-Solomon, LDPC) stay in the algorithmics zoo.
- named-in: Error Detecting and Error Correcting Codes - Hamming (1950)
- tags: embedded, storage, networking

### hidden-class — Hidden Class
- aka: maps (Self, original name), shapes (SpiderMonkey), Structures (JavaScriptCore), object shapes, shape/map transition tree (mechanism detail)
- kind: data-representation
- what: The runtime assigns each object a shared internal layout descriptor (map/shape/hidden class) recording its property names and slot offsets, transitioning objects between descriptors as properties are added, so objects created the same way share one layout.
- problem: Prototype- and dictionary-based languages have no static classes, so naive objects carry per-instance property tables; shared layout descriptors recover class-like memory density and give inline caches a cheap identity to guard on.
- named-in: Chambers, Ungar & Lee, 'An Efficient Implementation of SELF, a Dynamically-Typed Object-Oriented Language Based on Prototypes', OOPSLA 1989 (names 'maps'; verified live this session); 'hidden class' is the V8 documentation term
- tags: virtual machines, language runtimes, dynamic languages, JavaScript engines

### level-of-detail — Level of Detail
- aka: LOD, discrete LOD, continuous LOD (variant)
- kind: data-representation
- what: Maintain multiple representations of an object at different fidelities and select the cheapest one whose error is imperceptible given current importance (typically distance from the viewer).
- problem: Rendering or simulating everything at full fidelity wastes resources on objects that contribute little to the result; graded representations bound cost while preserving perceived quality. Generalizes beyond graphics (audio, AI, simulation LOD).
- named-in: Level of Detail for 3D Graphics - Luebke, Reddy, Cohen, Varshney, Watson, Huebner (2003)
- tags: games, graphics, performance, borderline — Graphics-domain optimization technique rather than a general software mechanism, but it is named, recurring, and implementable inside one component; included per charter.

### multiple-representations — Multiple Representations
- aka: —
- kind: data-representation
- what: Provide several implementations of an object, each optimized for different size/speed trade-offs, behind one common interface.
- problem: One representation cannot be optimal for all instances (small vs large, read-only vs mutable); switching representations per instance keeps memory minimal without changing clients.
- named-in: corpus:noblesmallmem — Small Memory Software: Patterns for Systems with Limited Memory - Noble & Weir (2000)
- tags: embedded, memory

### newtype — Newtype
- aka: wrapper type, strong typedef (C++), tiny types, whole value (related CHECKS pattern), strong typedef, micro type
- kind: data-representation
- what: Wrap an existing type in a distinct single-field type so the compiler distinguishes semantically different values (Miles vs Kilometers) and the wrapper can carry its own invariants and trait implementations.
- problem: Raw primitives let unrelated quantities be mixed silently and leak representation; the zero-cost wrapper restores type safety and API encapsulation.
- named-in: Rust Design Patterns (rust-unofficial, living); keyword-level origin in Haskell (newtype)
- tags: rust, haskell, c++, fp

### opaque-pointer — Opaque Pointer
- aka: opaque handle, incomplete type idiom, Handle (Fluent C), pimpl in C, First-Class ADT, first-class abstract data type, opaque instance-based module, Opaque Type, handle-based interface
- kind: data-representation
- what: An API exposes only a forward-declared struct pointer whose definition lives in the implementation file, so clients cannot see or touch the representation.
- problem: C has no access control; the incomplete type makes information hiding compiler-enforced and keeps ABI stable across representation changes.
- named-in: corpus:hanson — C Interfaces and Implementations - David R. Hanson (1996)
- tags: c, embedded

### packed-data — Packed Data
- aka: bit packing, bit-fields, struct packing
- kind: data-representation
- what: Pack data items within a structure (bit-fields, smaller types, eliminated padding) so they occupy minimum space.
- problem: Naturally-aligned, full-width representations waste scarce RAM; packing trades access cost for a smaller memory footprint.
- named-in: corpus:noblesmallmem — Small Memory Software: Patterns for Systems with Limited Memory - Noble & Weir (2000)
- tags: embedded, memory

### pax-page-layout — PAX Page Layout
- aka: PAX, Partition Attributes Across, cache-conscious page layout, columnar page layout, hybrid row/column page layout
- kind: data-representation
- what: Within each fixed-size storage page, values are grouped per attribute into minipages instead of being stored row-contiguously, keeping a page's records together on disk while making each attribute cache-line-contiguous in memory.
- problem: Row-oriented (NSM) pages drag all attributes of a record through the cache when a scan touches only a few columns, while full column stores (DSM) pay record-reconstruction joins; PAX gets columnar cache behavior without changing page-level I/O or record placement.
- named-in: Ailamaki, DeWitt, Hill, Skounakis — Weaving Relations for Cache Performance, VLDB 2001
- tags: db, storage-engine, cache-conscious

### pointer-swizzling — Pointer Swizzling
- aka: swizzling, unswizzling (inverse), swizzling at page-fault time (eager variant), lazy swizzling
- kind: data-representation
- what: Converts persistent references (file offsets, object IDs, page-relative addresses) into raw in-memory pointers when data is loaded, and back again on write-out.
- problem: Persisted or memory-mapped object graphs cannot store raw virtual addresses; following offset-based references on every access is slow, so references are rewritten to native pointers while resident.
- named-in: Wilson & Kakkad, 'Pointer Swizzling at Page Fault Time' (1992); Moss, 'Working with Persistent Objects: To Swizzle or Not to Swizzle' (IEEE TSE, 1992)
- tags: databases, persistence, object stores, memory-mapped data

### pointer-tagging — Pointer Tagging
- aka: tagged pointer, tag bits, immediate values, small-integer tagging (Smi), NaN-boxing (NaN-payload variant), NuN-boxing / pointer boxing (variants)
- kind: data-representation
- what: Encodes type or other metadata in otherwise-unused bits of a pointer-sized word (low alignment bits, high address bits, or unused NaN payload space), so small values carry their own type tag and need no heap allocation.
- problem: Dynamic-language runtimes must represent values of many types uniformly and compactly; boxing every integer or float on the heap costs allocation, indirection, and GC pressure.
- named-in: Gudeman, 'Representing Type Information in Dynamically Typed Languages', Univ. of Arizona TR 93-27, 1993 (canonical survey; verified via live search this session)
- tags: interpreters, virtual machines, language runtimes, borderline — index's reference-counting entry lists 'ABA Mitigation via Tagged Pointer' as an aka — that is a different mechanism (version bits for ABA), not type tagging; no dedup conflict

### quantity — Quantity
- aka: measure, amount with unit
- kind: data-representation
- what: A value type pairing a number with its unit of measure, with arithmetic and comparisons that respect unit compatibility and conversion.
- problem: Bare numbers lose their units, inviting silent unit-mismatch bugs (feet vs meters, dollars vs euros); carrying the unit in the type makes mismatched arithmetic impossible or explicit.
- named-in: Analysis Patterns: Reusable Object Models - Martin Fowler (1996)
- tags: domain-modeling, borderline — Analysis-pattern (domain-modeling) altitude, but a directly implementable value type recurring across codebases.

### range — Range
- aka: interval object
- kind: data-representation
- what: A value object representing an interval by its start and end (with open/closed ends), answering inclusion, overlap, and abutment queries.
- problem: Pairs of loose start/end fields breed off-by-one and boundary-convention bugs repeated at every comparison; one range type centralizes the boundary logic.
- named-in: Analysis Patterns: Reusable Object Models - Martin Fowler (1996)
- tags: domain-modeling, borderline — Analysis-pattern (domain-modeling) altitude, but a directly implementable value type recurring across codebases.

### record-set — Record Set
- aka: —
- kind: data-representation
- what: An in-memory representation of tabular data that looks and acts like the result of a database query but can be built and manipulated disconnected from the database.
- problem: UI machinery and table-oriented logic want a generic table-shaped data structure independent of any live connection; a disconnected record set lets the same tooling work on queried or synthesized data.
- named-in: Patterns of Enterprise Application Architecture - Martin Fowler (2002)
- tags: enterprise

### relationship-object — Relationship Object
- aka: association object, relationship as full object, reified relationship
- kind: data-representation
- what: Reify a relationship between objects as a first-class object that stores the participants plus the relationship's own attributes and behavior, instead of encoding the link as mutual references.
- problem: Relationships with their own state (start date, role, quantity) or lifecycle cannot live naturally inside either participant; direct mutual pointers scatter the relationship's logic and complicate consistency.
- named-in: Noble, 'Basic Relationship Patterns', PLoPD4 (2000); also Boyd, 'Business Patterns of Association Objects', PLoPD3 (1997) (both ToCs loaded live)
- tags: domain-modeling, in-memory counterpart of association-table-mapping (index)

### slotted-page-layout — Slotted Page Layout
- aka: slotted pages, slot directory, slot array page
- kind: data-representation
- what: A page format with a slot directory growing from one end and variable-length records growing from the other, so records are addressed by stable slot number rather than byte offset.
- problem: Variable-length records must be inserted, deleted, and relocated within a fixed-size page without invalidating external record identifiers; the indirection slot array permits in-page compaction while record ids stay stable.
- named-in: Database Internals - Petrov (2019)
- tags: db, storage-engine

### tagged-union — Tagged Union
- aka: sum type, discriminated union, variant, disjoint union
- kind: data-representation
- what: A data type whose value is exactly one of several named alternatives, carrying a tag that identifies which alternative is present.
- problem: Safely representing 'one of N shapes' data without unchecked casts or sentinel conventions; enables exhaustive case analysis so unhandled alternatives are caught statically.
- named-in: Types and Programming Languages - Benjamin C. Pierce (2002)
- tags: fp, c, rust, fsharp, scala, haskell

### temporal-property — Temporal Property
- aka: temporal object (whole-object variant), historic mapping, effectivity (validity-interval variant), snapshot view (derived), bitemporal record (two-dimensional variant)
- kind: data-representation
- what: Represent an attribute (or whole object) as a time-indexed collection of values so the model can answer 'what was/is/will be the value at time T' rather than only the current value.
- problem: Domain data changes over time and past states must remain queryable (retroactive corrections, effective dates); overwriting in place destroys history.
- named-in: Carlson, Estepp & Fowler, 'Temporal Patterns', PLoPD4 (2000) (ToC loaded live); living treatment: Fowler's eaaDev temporal patterns (Temporal Property, Temporal Object, Snapshot, Effectivity)
- tags: domain-modeling, time

### texture-atlas — Texture Atlas
- aka: sprite sheet, sprite atlas, texture packing, atlasing, sub-texture packing
- kind: data-representation
- what: Pack many small images into one large texture and remap each user's texture coordinates into its sub-rectangle, so a single bound resource serves many logical images.
- problem: Per-texture bind/state changes break rendering batches and dominate CPU submission cost; consolidating images into one atlas lets unrelated geometry share render state and be submitted together, at the cost of packing, bleeding/padding, and mip-level management.
- named-in: NVIDIA SDK White Paper 'Improve Batching Using Texture Atlases' (WP-01387-001, 2004); Ivan-Assen Ivanov, 'Practical Texture Atlases', Gamasutra/Game Developer, 2006
- tags: g, a, m, e, s, ;,  , g, r, a, p, h, i, c, s, ;,  , U, I,  , (, i, c, o, n,  , s, p, r, i, t, e,  , s, h, e, e, t, s, ), ;,  , w, e, b,  , (, C, S, S,  , s, p, r, i, t, e, s,  , a, s,  , t, h, e,  , s, a, m, e,  , m, e, c, h, a, n, i, s, m, )

### type-safe-enum — Type-Safe Enum
- aka: enum pattern, typesafe enum pattern, enum class precursor
- kind: data-representation
- what: Represent an enumerated type as a class with a fixed set of public static final instances and a private constructor, giving type safety, namespacing, and behavior per constant.
- problem: int/#define constants are unchecked, unprintable, and collide; the pattern (since absorbed into Java enum / C++ enum class) makes enumerations real types. Bloch's enum-singleton is a folded application.
- named-in: Effective Java - Joshua Bloch (1st ed. 2001, Item 21)
- tags: java, c++

### value-object — Value Object
- aka: —
- kind: data-representation
- what: A small immutable object, such as a date or money amount, whose equality is based on its attribute values rather than on identity.
- problem: Treating conceptually value-like data as identity-bearing objects invites aliasing bugs and wrong equality; value semantics (immutability, whole-value replacement, structural equality) make such data safe to share and compare.
- named-in: Patterns of Enterprise Application Architecture - Martin Fowler (2002)
- tags: enterprise, ddd

### virtual-dom — Virtual DOM
- aka: VDOM, virtual DOM diffing, reconciliation
- kind: data-representation
- what: Keeps a lightweight in-memory tree describing the desired UI, diffs it against the previous tree on every update, and applies only the minimal set of mutations (reconciliation) to the real, expensive display tree.
- problem: Direct manipulation of a retained display tree (the browser DOM) is slow and hard to reason about; declaring the whole UI and diffing lets code be written as 'render from state' while paying only for what changed. Keyed list reconciliation and the incremental-DOM alternative are variants folded here.
- named-in: Reconciliation - React documentation - Meta
- tags: ui, js


## Data flow & buffering — `data-flow-buffering` (28)

### backpressure — Backpressure
- aka: Create Back Pressure, flow control, Back Pressure (Nygard)
- kind: data-flow-buffering
- what: Propagate 'slow down' signals upstream - via bounded queues, blocking, or demand signaling - so producers cannot outrun consumers.
- problem: Unbounded queues hide overload until memory or latency blows up; making queues bounded pushes the overload decision back to the producer, where it can be handled.
- named-in: corpus:nygard — Release It! Design and Deploy Production-Ready Software, 2nd ed. - Nygard (2018)
- tags: stability, streaming

### credit-based-flow-control — Credit-Based Flow Control
- aka: credit scheme, Leaky Bucket of Credits (Meszaros), demand signaling (Reactive Streams request(n)), credit grant window
- kind: data-flow-buffering
- what: A receiver grants the sender explicit credits, each authorizing transmission of one unit; the sender stops when credits run out and resumes as the receiver replenishes them from freed buffer space.
- problem: A producer must never overrun a consumer's buffering capacity; explicit credits achieve lossless flow control without dropping or blind rate guessing.
- named-in: Kung & Morris, 'Credit-Based Flow Control for ATM Networks', IEEE Network (1995); Meszaros, capacity pattern language, PLoPD1 (1995); Reactive Streams specification (request(n) demand)
- tags: flow-control, networking, reactive-streams, borderline — Specific mechanism beneath the general backpressure element (in index) and sibling of sliding-window-flow-control (in index); kept because the credit mechanism is independently named and distinct from windowed ack-based control.

### disruptor — Disruptor
- aka: LMAX Disruptor, ring buffer with sequence barriers, mechanical-sympathy ring buffer
- kind: data-flow-buffering
- what: A pre-allocated ring buffer where producers and consumers coordinate through monotonic sequence counters and sequence barriers instead of locks, supporting dependency graphs of consumers over the same entries.
- problem: Bounded queues concentrate contention on head and tail and add latency per pipeline stage; sequence-gated access to a shared ring gives orders-of-magnitude lower latency and lets multiple consumers process entries in dependency order without copying.
- named-in: Thompson, Farley, Barker, Gee, Stewart — Disruptor: High Performance Alternative to Bounded Queues for Exchanging Data Between Concurrent Threads (LMAX technical paper, 2011)
- tags: java-origin, low-latency, lock-free

### double-buffer — Double Buffer
- aka: double buffering, page flipping
- kind: data-flow-buffering
- what: Maintain two copies of a piece of state - one being read/displayed while the other is written - and swap them atomically when the write completes.
- problem: A consumer must never observe state mid-modification (torn frames, half-updated simulation state); writing into a hidden buffer and swapping makes updates appear instantaneous.
- named-in: Game Programming Patterns - Robert Nystrom (2014)
- tags: games, graphics

### draw-call-batching — Draw-Call Batching
- aka: batching (rendering), static batching, dynamic batching, sprite batching (SpriteBatch), geometry instancing / GPU instancing (single-call many-instances variant)
- kind: data-flow-buffering
- what: Merge many draw submissions that share render state into fewer, larger GPU submissions — by pre-combining static geometry, transforming and appending small dynamic meshes into a shared buffer, or issuing one instanced call for many copies.
- problem: Each draw call carries fixed CPU driver/validation overhead, so thousands of small state-changing draws leave the GPU starved; batching restructures scene data and material assignment so submissions amortize that overhead.
- named-in: Matthias Wloka, 'Batch, Batch, Batch: What Does It Really Mean?', GDC 2003 (NVIDIA); Unity Manual, 'Draw call batching' (static/dynamic batching); GPU Gems 2 ch. 3 'Inside Geometry Instancing' (instancing variant)
- tags: g, a, m, e, s, ;,  , g, r, a, p, h, i, c, s, ;,  , b, o, r, d, e, r, l, i, n, e,  , —,  , c, o, n, t, e, s, t, a, b, l, e,  , a, s,  , p, u, r, e,  , p, e, r, f, o, r, m, a, n, c, e,  , p, r, a, c, t, i, c, e, ,,  , k, e, p, t,  , b, e, c, a, u, s, e,  , i, t,  , i, s,  , a,  , n, a, m, e, d, ,,  , r, e, c, u, r, r, i, n, g,  , s, t, r, u, c, t, u, r, a, l,  , m, e, c, h, a, n, i, s, m,  , (, s, h, a, r, e, d, -, m, a, t, e, r, i, a, l,  , s, c, e, n, e,  , o, r, g, a, n, i, z, a, t, i, o, n, ,,  , m, e, r, g, e, d,  , v, e, r, t, e, x,  , b, u, f, f, e, r, s, ,,  , i, n, s, t, a, n, c, e,  , s, t, r, e, a, m, s, ),  , d, i, s, t, i, n, c, t,  , f, r, o, m,  , u, p, d, a, t, e, -, b, a, t, c, h, i, n, g,  , (, U, I, -, r, e, a, c, t, i, v, e,  , s, t, a, t, e,  , f, l, u, s, h, ), ,,  , b, a, t, c, h, -, m, e, t, h, o, d,  , (, A, P, I,  , s, h, a, p, e, ), ,,  , a, n, d,  , g, r, o, u, p, -, c, o, m, m, i, t,  , (, d, u, r, a, b, i, l, i, t, y, )

### event-coalescing — Event Coalescing
- aka: coalesced events, input event merging
- kind: data-flow-buffering
- what: Merges multiple fine-grained input events that occur within one processing frame into a single delivered event, optionally exposing the merged raw events on demand.
- problem: Input devices can report far faster than the frame rate; delivering every raw event floods handlers, while coalescing delivers one event per frame with the raw history (e.g. getCoalescedEvents) available for precision uses like inking.
- named-in: Pointer Events Level 2 - W3C Recommendation (coalesced events / getCoalescedEvents)
- tags: ui, js

### event-time-watermark — Watermark (Event-Time)
- aka: low watermark, event-time watermark, perfect watermark / heuristic watermark (variants), watermark propagation
- kind: data-flow-buffering
- what: A monotonic progress signal flowing through a stream processor asserting that no events with timestamps older than T will arrive, used to decide when buffered event-time computations (windows, timers) are complete and may fire.
- problem: Unbounded streams arrive out of order; without a completeness signal, an operator can never know when it has seen all data for a time interval and must choose between wrong results and waiting forever.
- named-in: Akidau et al., 'The Dataflow Model' (PVLDB 8(12), 2015; verified live); also Akidau, Chernyak & Lax, Streaming Systems (O'Reilly 2018)
- tags: stream processing, distributed data, time, borderline — mechanism inside one stream-processing engine (passes altitude test), though usually deployed in distributed pipelines

### fresh-work-before-stale — Fresh Work Before Stale
- aka: adaptive LIFO, newest-first queue discipline
- kind: data-flow-buffering
- what: Under overload, serve the newest requests first (LIFO) because the oldest queued requests have likely already timed out or been abandoned by their requesters.
- problem: FIFO under sustained overload spends capacity on requests whose callers have given up, so nobody gets service; newest-first lets at least recent requesters succeed.
- named-in: corpus:hanmer — Patterns for Fault Tolerant Software - Hanmer (2007)
- tags: overload, borderline — A queue-discipline choice shading into policy; kept as a named, implementable overload mechanism (cf. adaptive LIFO in later SRE literature).

### functional-reactive-programming — Functional Reactive Programming
- aka: FRP, behaviors and events, reactive combinators
- kind: data-flow-buffering
- what: Programming with first-class time-varying values (behaviors/signals) and event streams composed declaratively, with the runtime propagating changes through the dependency graph.
- problem: Replaces manual observer wiring and callback state machines for time- and event-driven logic (UIs, animation, robotics) with composable declarative dataflow.
- named-in: Functional Reactive Animation - Elliott & Hudak (ICFP, 1997)
- tags: fp, haskell, ui, functional, borderline — A programming model verging on paradigm; kept because it is library-implementable inside one program (Yampa, reflex, Rx-style signal libraries) and canonically named. Overlaps concurrency/reactive scout - fine.

### jitter-buffer — Jitter Buffer
- aka: playout buffer, de-jitter buffer, playout delay buffer, adaptive jitter buffer
- kind: data-flow-buffering
- what: Buffer arriving media packets briefly and release them on a steady clock (reordering by sequence number), absorbing variation in network transit time.
- problem: Real-time audio/video must be played at a constant rate but packets arrive with variable delay and out of order; buffering trades a bounded added latency for smooth, gap-free playout. Static vs adaptive sizing folded as variants.
- named-in: Understanding Jitter in Packet Voice Networks - Cisco (live technical doc)
- tags: networking, media, voip, real-time

### load-shedding — Load Shedding
- aka: Shed Load
- kind: data-flow-buffering
- what: When offered load exceeds capacity, deliberately reject or drop a portion of incoming work (cheaply and early) so accepted work still completes within acceptable time.
- problem: Accepting all work under overload degrades service for every request and can collapse the system; refusing excess work keeps the remainder healthy.
- named-in: corpus:nygard — Release It! Design and Deploy Production-Ready Software, 2nd ed. - Nygard (2018)
- tags: stability, overload

### memory-mapped-file-i-o — Memory-Mapped File I/O
- aka: mmap, file mapping, memory-mapped I/O (file)
- kind: data-flow-buffering
- what: Map a file's contents into the process address space so it is read and written through ordinary memory access, with the OS paging data in and out on demand.
- problem: Explicit read/write loops double-buffer data and force the program to manage its own windowing over large files; mapping delegates buffering, caching, and lazy loading to the virtual-memory system and enables sharing between processes. Distinct from memory-mapped device registers (embedded scout's territory).
- named-in: Advanced Programming in the UNIX Environment - W. Richard Stevens (1992), 'Memory-Mapped I/O'
- tags: c, os, persistence, performance

### ping-pong-buffer — Ping-Pong Buffer
- aka: ping-pong buffering, buffer role swapping
- kind: data-flow-buffering
- what: Two buffers alternate roles between a producer and a consumer: while one is being filled the other is processed, and the roles swap on completion.
- problem: A producer (ISR, DMA, sampling loop) and consumer working in one buffer corrupt or lose data; alternating disjoint buffers lets both proceed concurrently on different memory. Kept distinct from double-buffered DMA: ping-pong is the general software-role-swap mechanism, DMA double-buffering its hardware-managed realization.
- named-in: Ping Pong Buffers - Embedded.fm (White, 2017); Microchip DMA 'Ping-Pong Mode' documentation
- tags: embedded, dsp, audio

### reactive-programming — Reactive Programming
- aka: reactive programming model, dataflow-style change propagation
- kind: data-flow-buffering
- what: A programming model in which programs are expressed as dataflows of time-varying values and the runtime automatically propagates changes through the dependency graph, as in a spreadsheet.
- problem: Interactive programs are dominated by manually wiring 'when X changes, update Y' logic (callback hell, inconsistent intermediate states); declaring dependencies and letting the system propagate changes removes that class of code. Umbrella over FRP, Rx, and signals.
- named-in: A Survey on Reactive Programming - Bainomugisha, Carreton, Van Cutsem, Mostinckx, De Meuter (ACM Computing Surveys, 2013)
- tags: ui, borderline — Umbrella programming model rather than a single mechanism; included per the asynchronous-programming-models precedent in the mission's anchor table - decision logged.

### render-graph — Render Graph
- aka: frame graph, FrameGraph, render dependency graph (RDG)
- kind: data-flow-buffering
- what: Render passes declare their input/output resources up front, building a per-frame DAG that the engine compiles into an execution schedule with automatic barrier placement and transient resource memory aliasing.
- problem: Hand-wired render pipelines couple passes to concrete resources and make reordering, async compute, and transient-memory reuse error-prone; a declared pass/resource graph decouples features and lets the compiler derive scheduling and aliasing.
- named-in: O'Donnell, 'FrameGraph: Extensible Rendering Architecture in Frostbite', GDC 2017
- tags: games, graphics, borderline — Modern (2017) and graphics-domain, but named, recurring (Frostbite FrameGraph, Unreal RDG, Unity SRP render graph), and implementable inside one renderer component, so it passes the gates.

### resequencer — Resequencer
- aka: —
- kind: data-flow-buffering
- what: A stateful buffer that holds out-of-order messages and releases them downstream in the correct sequence based on a sequence number.
- problem: Parallel processing or unordered channels scramble message order while consumers require it; buffering until gaps fill restores order without blocking the producers.
- named-in: Enterprise Integration Patterns - Hohpe & Woolf (2003)
- tags: messaging

### ring-buffer — Ring Buffer
- aka: circular buffer, circular queue, cyclic buffer
- kind: data-flow-buffering
- what: Fixed-size array with wrapping head and tail indices forming a FIFO that never moves data or allocates, naturally overwriting or blocking when full.
- problem: Producer-consumer handoff (ISR-to-task, audio, logging, SPSC queues) needs constant-time bounded buffering without allocation; wrap-around indexing gives it with two indices.
- named-in: corpus:white — Making Embedded Systems: Design Patterns for Great Software - Elecia White (2024)
- tags: embedded, c, concurrency, audio

### scatter-gather-dma — Scatter-Gather DMA
- aka: DMA descriptor chaining, chained DMA, vectored DMA, Scatter-Gather I/O, vectored I/O, readv/writev, scatter read and gather write
- kind: data-flow-buffering
- what: Program the DMA controller with a chain of descriptors so one logical transfer moves data to/from multiple non-contiguous memory regions without CPU intervention between segments.
- problem: Data often lives in scattered buffers (protocol headers + payload, page-fragmented memory); descriptor chains avoid copying into one contiguous bounce buffer and avoid per-segment CPU servicing.
- named-in: corpus:ldd3 — Linux Device Drivers, 3rd ed. - Corbet, Rubini & Kroah-Hartman (2005)
- tags: embedded, os, dma, c, networking, os-kernel

### sliding-window-rate-limiting — Sliding-Window Rate Limiting
- aka: sliding window counter, sliding window log, fixed window counter
- kind: data-flow-buffering
- what: Admit a request only if the count of requests in the trailing time window is below a limit, tracked by a per-window counter, a timestamp log, or a weighted blend of adjacent windows.
- problem: API quotas expressed as 'N requests per interval' need a counting mechanism; window variants trade memory and precision against boundary-burst artifacts. Granularity decision: the three window variants are folded into this one element; token bucket and leaky bucket stay separate mechanisms.
- named-in: System Design Interview - An Insider's Guide - Xu (2020)
- tags: web, rate-limiting

### snapshot-interpolation — Snapshot Interpolation
- aka: entity interpolation, state snapshot buffering
- kind: data-flow-buffering
- what: Buffer received snapshots of remote simulation state for a short delay and render by interpolating between two slightly-past snapshots, reconstructing smooth motion from discrete, jittery updates.
- problem: State updates arrive at a lower and irregular rate than the display refresh; interpolating between delayed buffered snapshots hides network jitter and packet spacing at the cost of added latency.
- named-in: Snapshot Interpolation - Glenn Fiedler (Gaffer On Games, 2015)
- tags: games, networking, borderline — A networked-game state-synchronization technique, but the buffering-and-interpolation mechanism itself is implemented entirely inside the receiving process; the surrounding client-server topology is parked for Phase 3.

### spsc-lock-free-ring-buffer — SPSC Lock-Free Ring Buffer
- aka: single-producer single-consumer queue, Lamport queue, wait-free bounded buffer
- kind: data-flow-buffering
- what: A bounded circular buffer where one producer owns the write index and one consumer owns the read index, so each side progresses wait-free with only acquire/release ordering and no atomic RMW.
- problem: Passing data between exactly two threads (or thread and ISR) with minimal, bounded, allocation-free overhead; the ownership split removes the need for locks or CAS entirely.
- named-in: Proving the Correctness of Multiprocess Programs - Leslie Lamport (1977)
- tags: c, cpp, embedded, audio, systems

### stream-buffer — Stream Buffer
- aka: message buffer (framed variant), FreeRTOS stream buffer, byte stream buffer, xStreamBuffer/xMessageBuffer
- kind: data-flow-buffering
- what: RTOS kernel object providing a single-writer single-reader byte stream (message-buffer variant: discrete variable-length messages) with blocking send/receive and a trigger level controlling how many bytes must arrive before the reader unblocks.
- problem: Passing continuous byte data or framed messages from exactly one task/ISR to exactly one task; the single-reader/single-writer restriction permits a much lighter implementation than a general message queue while keeping blocking semantics.
- named-in: corpus:freertosbook — freertos.org 'RTOS Stream Buffers' (title verified live 2026-07-10); Mastering the FreeRTOS Real-Time Kernel ch. Stream and Message Buffers
- tags: embedded, freertos, rtos, borderline — blocking kernel-object layer over an SPSC ring buffer (cf. existing spsc-lock-free-ring-buffer); kept because trigger-level blocking byte/message-stream semantics is a distinct named kernel mechanism, not just the underlying data structure

### stream-trigger — Trigger (Stream Processing)
- aka: triggers, watermark trigger, processing-time trigger, repeated/composite triggers, early/on-time/late firings (panes), accumulation mode (discarding/accumulating/retracting, companion policy)
- kind: data-flow-buffering
- what: A declarative mechanism that decides WHEN the accumulated contents of a window are materialized and emitted, driven by signals such as watermark passage, processing time, element count, or composites of these.
- problem: Windowing says where in event time data is grouped and the watermark says when input is believed complete, but neither says when to emit results; a trigger decouples output timing from input completeness, enabling early speculative results and late corrections instead of a single emit-at-watermark policy.
- named-in: The Dataflow Model (Akidau et al., PVLDB 8(12), 2015, sec. 2.3); modern canonical treatment: Streaming Systems (Akidau, Chernyak, Lax, 2018) and the Apache Beam programming guide (sec. 9 'Triggers', verified live 2026-07-10)
- tags: s, t, r, e, a, m, i, n, g, ;,  , d, a, t, a, b, a, s, e, s, ;,  , d, i, s, t, r, i, b, u, t, e, d, -, a, d, j, a, c, e, n, t,  , b, u, t,  , i, m, p, l, e, m, e, n, t, a, b, l, e,  , i, n, s, i, d, e,  , a,  , s, i, n, g, l, e,  , s, t, r, e, a, m,  , o, p, e, r, a, t, o, r, /, e, n, g, i, n, e,  , c, o, m, p, o, n, e, n, t, ;,  , c, o, m, p, l, e, m, e, n, t, s,  , s, t, r, e, a, m, -, w, i, n, d, o, w, i, n, g,  , a, n, d,  , e, v, e, n, t, -, t, i, m, e, -, w, a, t, e, r, m, a, r, k,  , (, d, i, s, t, i, n, c, t,  , m, e, c, h, a, n, i, s, m, :,  , o, u, t, p, u, t,  , t, i, m, i, n, g, ,,  , n, o, t,  , g, r, o, u, p, i, n, g,  , o, r,  , c, o, m, p, l, e, t, e, n, e, s, s, )

### stream-windowing — Stream Windowing
- aka: tumbling window, fixed window, sliding window, hopping window, session window, window operator
- kind: data-flow-buffering
- what: Partitions an unbounded event stream into finite time- or count-based buckets (fixed, sliding, session) that scope aggregations, with per-window state buffered until the window closes or triggers.
- problem: Aggregations over an infinite stream never terminate; windowing bounds state and computation and gives every emitted result a defined temporal scope.
- named-in: Akidau et al., 'The Dataflow Model' (PVLDB 2015; formal windowing model, verified live); window constructs also in CQL (Arasu, Babu & Widom, VLDB Journal 2006)
- tags: stream processing, distributed data, borderline — distinct from index entries sliding-window-flow-control (protocol ARQ) and sliding-window-rate-limiting (rate limiter) and list-virtualization's UI 'windowing'

### update-batching — Update Batching
- aka: automatic batching, async update queue, microtask-deferred flush
- kind: data-flow-buffering
- what: Buffers multiple state mutations occurring in one synchronous turn and flushes their downstream effects (re-render, DOM patch) once, typically on the next microtask or tick, deduplicating redundant work.
- problem: Naively reacting to every individual state write causes repeated renders and observable intermediate states; queueing and deduplicating watchers per tick makes updates coalesce (React automatic batching, Vue's async update queue / nextTick).
- named-in: React documentation - Automatic Batching (React 18); Vue.js Guide - Reactivity in Depth (Async Update Queue)
- tags: ui, js

### vectorized-execution — Vectorized Execution
- aka: batch-at-a-time execution, vectorized query processing, vector-at-a-time model
- kind: data-flow-buffering
- what: Query operators pass batches (vectors) of hundreds or thousands of values per next() call instead of single tuples, running tight primitive loops over each batch.
- problem: Tuple-at-a-time iteration pays interpretation overhead per row and defeats CPU caches and SIMD; batching amortizes dispatch cost and enables cache- and SIMD-friendly inner loops.
- named-in: MonetDB/X100: Hyper-Pipelining Query Execution - Boncz, Zukowski & Nes (2005)
- tags: db, query-execution, performance, borderline — Arguably an optimization of the iterator model rather than a distinct mechanism; kept separate because the batch-interface design is independently named and adopted (DuckDB, Velox, Arrow).

### volcano-iterator-model — Volcano Iterator Model
- aka: iterator model, open-next-close model, pull-based query execution, tuple-at-a-time execution
- kind: data-flow-buffering
- what: Every query operator implements a uniform open/next/close iterator interface and pulls one tuple at a time from its children, composing arbitrary operator trees into demand-driven pipelines.
- problem: Operators need to compose without materializing intermediate results or knowing each other's internals; the uniform pull interface makes pipelining and operator extensibility mechanical.
- named-in: Volcano - An Extensible and Parallel Query Evaluation System - Graefe (1994)
- tags: db, query-execution

### zero-copy-i-o — Zero-Copy I/O
- aka: zero-copy, sendfile, splice
- kind: data-flow-buffering
- what: Move data between endpoints (file, socket, device) without copying it through intermediate user-space buffers, via DMA, page remapping, or in-kernel transfer.
- problem: Each redundant copy across the user/kernel boundary costs CPU cycles, cache pollution, and memory bandwidth; for high-throughput I/O paths the copies dominate the cost of the transfer itself.
- named-in: Zero-copy - Wikipedia
- tags: networking, os-kernel, performance


## Execution & concurrency — `execution-concurrency` (37)

### active-object — Active Object
- aka: Concurrent Object, Actor Model, actors, active entities with mailboxes
- kind: execution-concurrency
- what: Method invocation is decoupled from method execution: calls are reified as requests on an activation queue and executed by the object's own thread via a scheduler, with futures for results.
- problem: An object needs its own thread of control so clients are not blocked and its internal state is accessed by one thread only, serializing concurrency at the object boundary.
- named-in: corpus:posa2 — Pattern-Oriented Software Architecture Vol. 2: Patterns for Concurrent and Networked Objects - Schmidt, Stal, Rohnert, Buschmann (2000)
- tags: threads, embedded, erlang, scala, c, c++, concurrency, borderline — In-process actor frameworks (Akka on one JVM, Erlang processes in one node, actor libraries in C++/Rust) pass the altitude test; distributed actor systems as deployment topology are architecture-level and belong to Phase 3.

### async-await-model — Async-Await Model
- aka: async workflows, async functions, awaitable model
- kind: execution-concurrency
- what: A language-level model in which functions marked async are compiled into continuation/state-machine form so that awaiting an asynchronous result suspends the function without blocking its thread.
- problem: Callback-based asynchronous code inverts control flow and destroys readability; async-await preserves sequential-looking code while keeping execution non-blocking.
- named-in: The F# Asynchronous Programming Model - Syme, Petricek, Lomov (2011)
- tags: csharp, fsharp, javascript, python, rust

### asynchronous-completion-token — Asynchronous Completion Token
- aka: ACT
- kind: execution-concurrency
- what: The initiator of an asynchronous operation passes along an opaque token that comes back with the completion event, letting the response be demultiplexed to the right state and actions in constant time.
- problem: When responses to async operations arrive out of order, the receiver must efficiently re-associate each completion with the context needed to process it, without searching.
- named-in: corpus:posa2 — Pattern-Oriented Software Architecture Vol. 2: Patterns for Concurrent and Networked Objects - Schmidt, Stal, Rohnert, Buschmann (2000)
- tags: async, networking

### bytecode-virtual-machine — Bytecode Virtual Machine
- aka: bytecode interpreter, VM, stack machine / register machine (implementation variants)
- kind: execution-concurrency
- what: An interpreter that first compiles source to a compact linear instruction encoding (bytecode) and then executes it in a dispatch loop over a virtual instruction set, usually with an operand stack or virtual registers.
- problem: Tree walking pays pointer-chasing and dynamic-dispatch costs on every node visit; a dense linear instruction stream improves locality and dispatch speed while remaining portable across host platforms.
- named-in: Crafting Interpreters - Robert Nystrom (2021)
- tags: interpreters, languages, games

### cancellation-token — Cancellation Token
- aka: cancellation context, context propagation (Go context.Context), CancellationToken / CancellationTokenSource (.NET), cooperative cancellation, done channel (Go idiom precursor)
- kind: execution-concurrency
- what: An explicit token/context object threaded through the call graph that carries a cancellation signal (and often a deadline) which long-running operations poll or subscribe to, exiting cooperatively when it fires.
- problem: Work spawned on behalf of a request must stop promptly when the request is abandoned or times out; forced termination is unsafe, so a propagated, observable cancellation signal lets every participant release resources cooperatively.
- named-in: Sameer Ajmani, 'Go Concurrency Patterns: Context' (Go blog, 2014-07-29); Microsoft Learn, 'Cancellation in Managed Threads' (CancellationToken)
- tags: go, csharp, cross-language, borderline — Overlaps deadline-propagation (already in index) which covers the deadline/budget facet; this entry is the explicit cancellation-signal object itself. Also adjacent to two-phase-termination, which is the shutdown protocol rather than the propagated signal carrier.

### competing-consumers — Competing Consumers
- aka: —
- kind: execution-concurrency
- what: Multiple concurrent consumers receive from the same point-to-point channel, each message going to exactly one of them, so throughput scales with consumer count.
- problem: A single consumer cannot keep up with message arrival rate; letting a pool of consumers race for messages parallelizes processing while the queue preserves once-only delivery.
- named-in: Enterprise Integration Patterns - Hohpe & Woolf (2003)
- tags: messaging, concurrency

### coroutine — Coroutine
- aka: cooperative routine, generator (restricted form)
- kind: execution-concurrency
- what: A routine that can suspend its own execution at yield points and later be resumed with its local state intact, enabling cooperative multitasking on one thread.
- problem: Some computations (pipelines, state machines, async I/O) are naturally expressed as multiple interleaved control flows without the cost and preemption hazards of OS threads.
- named-in: Design of a Separable Transition-Diagram Compiler - Conway (1963)
- tags: python, kotlin, cpp, lua

### deoptimization — Deoptimization
- aka: dynamic deoptimization, deopt, on-stack replacement (OSR, the frame-replacement mechanism, folded), uncommon trap (HotSpot), bailout (JS-engine usage), tiering down
- kind: execution-concurrency
- what: The runtime invalidates speculatively optimized compiled code and transfers a running activation back to unoptimized code (interpreter or baseline), reconstructing the equivalent stack frames and local state at a mapped program point; the same frame-replacement machinery run upward (OSR entry) promotes a hot running loop into optimized code.
- problem: JIT compilers optimize on assumptions (class hierarchy, type profiles, no debugger) that can be invalidated at runtime, and debuggers need source-level state from optimized frames; the runtime must be able to abandon optimized frames mid-execution without losing correctness.
- named-in: Hoelzle, Chambers & Ungar, 'Debugging Optimized Code with Dynamic Deoptimization', PLDI 1992 (verified live via selflanguage.org bibliography this session)
- tags: virtual machines, JIT, language runtimes, speculative optimization

### event-loop — Event Loop
- aka: message loop, message pump, dispatch loop, run loop
- kind: execution-concurrency
- what: A single loop that waits for events (I/O readiness, messages, timers) and dispatches each to its handler, serializing all handler execution on one thread.
- problem: Handling many concurrent event sources with one thread avoids locking and thread overhead, provided handlers never block the loop; the pattern form for demultiplexing is POSA2's Reactor.
- named-in: Event loop - Wikipedia
- tags: javascript, ui, servers, embedded

### executor — Executor
- aka: executor service, task-queue execution model, task executor
- kind: execution-concurrency
- what: An abstraction that decouples task submission from the policy of task execution (which thread, when, in what order), typically backed by a work queue and thread pool.
- problem: Hard-coding 'new thread per task' couples application logic to an execution policy; an executor lets throughput, ordering, and resource policy vary independently of submitted work.
- named-in: Java Concurrency in Practice - Goetz, Peierls, Bloch, Bowbeer, Holmes, Lea (2006)
- tags: java

### false-sharing-avoidance-via-cache-line-padding — False-Sharing Avoidance via Cache-Line Padding
- aka: cache-line alignment, padding to cache line, hardware_destructive_interference_size
- kind: execution-concurrency
- what: Pad or align independently-written shared variables so no two of them share a cache line.
- problem: False sharing: logically independent data co-resident in one cache line causes coherence-protocol ping-pong that silently serializes unrelated threads.
- named-in: corpus:dreppermem — What Every Programmer Should Know About Memory - Ulrich Drepper (2007)
- tags: c, cpp, systems, embedded, performance

### fast-path — Fast Path
- aka: fast path / slow path split, Parallel Fastpath (McKenney), Optimize High-Runner Cases (Meszaros), common-case optimization path
- kind: execution-concurrency
- what: Provide a short, cheap code path for the common case (often lock-free or per-CPU) and fall back to a general, heavier slow path for the rare or complex cases.
- problem: Optimizing an entire algorithm for the worst case penalizes the dominant case; splitting paths buys common-case speed while keeping rare-case correctness in simpler code.
- named-in: McKenney, 'Selecting Locking Designs for Parallel Programs', PLoPD2 (1996) — Parallel Fastpath (verified via rdrop.com paper/perfbook); Meszaros, capacity pattern language, PLoPD1 (1995)
- tags: systems, concurrency, kernel idiom

### fork-join — Fork-Join
- aka: fork/join parallelism, divide-and-conquer parallelism
- kind: execution-concurrency
- what: A task forks subtasks that run in parallel and then joins on their completion, typically applied recursively to divide-and-conquer problems.
- problem: Recursive decomposable work needs a structured way to express parallelism whose task graph mirrors the call tree, keeping synchronization implicit in the join points.
- named-in: Patterns for Parallel Programming - Mattson, Sanders, Massingill (2004)
- tags: java, hpc

### future-promise — Future / Promise
- aka: future, promise, deferred, IOU, delay object
- kind: execution-concurrency
- what: A placeholder object representing the eventual result of an asynchronous computation, which consumers can query, wait on, or attach continuations to.
- problem: A caller wants to start an asynchronous operation and continue working without blocking, yet still obtain the result (or its failure) later in a first-class, composable way.
- named-in: Promises: Linguistic Support for Efficient Asynchronous Procedure Calls - Liskov, Shrira (1988)
- tags: —

### game-loop — Game Loop
- aka: fixed timestep loop, update-render loop
- kind: execution-concurrency
- what: A continuous loop that processes input without blocking, updates the simulation, and renders, decoupling the progression of game time from user input and processor speed.
- problem: Interactive simulations must keep running at a controlled rate regardless of whether the user does anything and regardless of hardware speed; the loop owns time and drives everything else.
- named-in: Game Programming Patterns - Robert Nystrom (2014)
- tags: games

### green-threads — Green Threads
- aka: fibers, user-level threads, lightweight threads, virtual threads
- kind: execution-concurrency
- what: Threads scheduled by a runtime or library in user space rather than by the operating system, multiplexed onto a smaller number of kernel threads.
- problem: Kernel threads are expensive to create and context-switch; user-level scheduling permits very large numbers of cheap concurrent activities at the cost of runtime-managed blocking.
- named-in: Green thread - Wikipedia
- tags: java, go, erlang

### half-sync-half-async — Half-Sync/Half-Async
- aka: —
- kind: execution-concurrency
- what: Concurrent processing is split into an asynchronous layer (interrupt/event-driven) and a synchronous layer (blocking service threads) mediated by a queueing layer between them.
- problem: Combine the performance of asynchronous event handling with the programming simplicity of synchronous code, without either style polluting the other.
- named-in: corpus:posa2 — Pattern-Oriented Software Architecture Vol. 2: Patterns for Concurrent and Networked Objects - Schmidt, Stal, Rohnert, Buschmann (2000)
- tags: os, networking, embedded, borderline — POSA2 labels it architectural, but it is a within-process/within-subsystem layering (e.g. OS network stacks, single servers), so it passes the altitude test.

### job-system — Job System
- aka: task graph, job scheduler, fiber-based job system, task-based parallelism (engine form), job kernel
- kind: execution-concurrency
- what: The engine decomposes each frame's work into many small jobs with declared dependencies (a task DAG) and schedules them onto a fixed pool of worker threads (often via fibers and work-stealing), instead of dedicating threads to subsystems.
- problem: Per-subsystem threads leave cores idle and serialize the frame; fine-grained dependency-scheduled jobs keep all cores saturated and let the frame's parallelism scale with hardware.
- named-in: Gregory, Game Engine Architecture, 3rd ed. (job systems chapter); Gyrling, 'Parallelizing the Naughty Dog Engine Using Fibers', GDC 2015
- tags: games, engine, borderline — Overlaps thread-pool, executor, fork-join, and work-stealing (all in index); kept because the engine literature names it distinctly: whole-frame dependency-declared task graph over a shared worker pool, with fiber-based suspension as its signature realization.

### leader-followers — Leader/Followers
- aka: —
- kind: execution-concurrency
- what: A pool of threads takes turns: one leader waits for and demultiplexes an event, promotes a follower to be the new leader, then processes the event itself before rejoining the followers.
- problem: High-throughput event processing on many threads without a queue between demultiplexing and processing, avoiding context switches, dynamic allocation, and data handoffs.
- named-in: corpus:posa2 — Pattern-Oriented Software Architecture Vol. 2: Patterns for Concurrent and Networked Objects - Schmidt, Stal, Rohnert, Buschmann (2000)
- tags: thread-pool, networking

### loop-parallelism — Loop Parallelism
- aka: parallel loop, parallel-for
- kind: execution-concurrency
- what: Distributing the iterations of a (semantically independent) loop across threads, typically via compiler directives or a parallel-for library construct.
- problem: Much compute time in existing sequential programs concentrates in loops; parallelizing iterations in place yields speedup with minimal restructuring when iterations are independent.
- named-in: Patterns for Parallel Programming - Mattson, Sanders, Massingill (2004)
- tags: openmp, hpc, cpp

### master-slave — Master-Slave
- aka: Master-Worker, master-slave (parallel form), manager-workers, task farm, work farm
- kind: execution-concurrency
- what: A master component partitions work into semantically identical sub-tasks, delegates them to interchangeable slave components, and combines their results into the final answer.
- problem: Divide-and-conquer for fault tolerance, parallel speed-up, or computational accuracy, while keeping clients unaware that the service is internally replicated or partitioned.
- named-in: Pattern-Oriented Software Architecture Vol. 1: A System of Patterns - Buschmann, Meunier, Rohnert, Sommerlad, Stal (1996)
- tags: parallelism, fault-tolerance, hpc

### multi-state-task — Multi-State Task
- aka: state-machine task, non-blocking task decomposition
- kind: execution-concurrency
- what: Implement a long-running activity as a state machine that advances one short step per scheduler invocation instead of blocking or busy-waiting.
- problem: A cooperative scheduler cannot tolerate tasks that block or run long; decomposing the activity into per-tick states keeps every invocation short and the schedule predictable.
- named-in: corpus:pont — Patterns for Time-Triggered Embedded Systems - Pont (2001)
- tags: embedded, c, real-time

### nested-interrupt-handling — Nested Interrupt Handling
- aka: interrupt nesting, preemptive interrupt priorities
- kind: execution-concurrency
- what: Allow a higher-priority interrupt to preempt a running lower-priority ISR by re-enabling interrupts (or relying on NVIC priority hardware) inside handlers.
- problem: With nesting disabled, a slow low-priority ISR delays urgent interrupts past their deadlines; controlled nesting bounds latency for critical sources at the cost of stack depth and reentrancy discipline.
- named-in: corpus:yiu — The Definitive Guide to ARM Cortex-M3 and Cortex-M4 Processors - Yiu (2013)
- tags: embedded, interrupts, arm

### parallel-reduction — Parallel Reduction
- aka: reduce (parallel pattern), reduction tree, tree reduction, parallel aggregation, combiner with associative operator
- kind: execution-concurrency
- what: Combine a collection of values into one result with an associative operator arranged as a tree of partial reductions computed in parallel, then merged.
- problem: A sequential fold serializes aggregation; exploiting associativity turns O(n) dependent steps into parallel partials plus O(log n) merge, without data races on a shared accumulator.
- named-in: McCool, Robison, Reinders, Structured Parallel Programming: Patterns for Efficient Computation (2012)
- tags: parallelism, peer of loop-parallelism / fork-join / pipeline-parallelism already in catalog

### pipeline-parallelism — Pipeline Parallelism
- aka: pipeline pattern, software pipeline, pipelining
- kind: execution-concurrency
- what: Decomposing a computation into ordered stages, each run by its own thread(s) and connected by queues, so different data items are processed in different stages simultaneously.
- problem: A sequential multi-stage transformation of a data stream leaves all but one stage idle; overlapping stages on different items converts stage count into throughput.
- named-in: Patterns for Parallel Programming - Mattson, Sanders, Massingill (2004)
- tags: hpc, embedded

### proactor — Proactor
- aka: —
- kind: execution-concurrency
- what: Applications initiate asynchronous operations and a completion dispatcher later invokes the matching completion handlers when the OS finishes the operations.
- problem: Exploit OS-level asynchronous I/O for throughput while structuring the resulting completion-driven control flow so application code stays modular and mechanism-independent.
- named-in: corpus:posa2 — Pattern-Oriented Software Architecture Vol. 2: Patterns for Concurrent and Networked Objects - Schmidt, Stal, Rohnert, Buschmann (2000)
- tags: networking, async-io

### protothread — Protothreads
- aka: stackless threads, local continuations, local-continuation threads
- kind: execution-concurrency
- what: Extremely lightweight stackless thread abstraction for C that gives event-driven code a sequential blocking-style structure, implemented with switch-based local continuations.
- problem: Event-driven state-machine code obscures control flow while real threads cost a stack each; protothreads express sequential waits in ~2 bytes of state per thread on memory-constrained MCUs.
- named-in: corpus:protothreads — Protothreads: Simplifying Event-Driven Programming of Memory-Constrained Embedded Systems - Dunkels et al. (2006)
- tags: embedded, c

### reactor — Reactor
- aka: Dispatcher, Notifier
- kind: execution-concurrency
- what: A synchronous event demultiplexer (select/poll) waits on multiple event sources and dispatches ready events to registered handler objects, serially, in one thread of control.
- problem: A server must service many clients or I/O sources concurrently without one thread per connection, while keeping application-level event handling single-threaded and simple.
- named-in: corpus:posa2 — Pattern-Oriented Software Architecture Vol. 2: Patterns for Concurrent and Networked Objects - Schmidt, Stal, Rohnert, Buschmann (2000)
- tags: networking, event-loop, embedded

### restartable-sequences — Restartable Sequences
- aka: rseq, per-CPU critical sections
- kind: execution-concurrency
- what: Short userspace critical sections over per-CPU data registered with the kernel, which aborts and restarts the sequence if the thread is preempted or migrated mid-section.
- problem: Per-CPU fast paths in userspace cannot otherwise know they stayed on one CPU; rseq gives atomic-free per-CPU updates at the cost of a restartable code discipline.
- named-in: Restartable sequences - LWN.net (2015)
- tags: c, linux, systems, borderline — Kernel-assisted like futex: the abort protocol needs kernel cooperation, but the element is a userspace code-structuring mechanism recurring in allocators and libc.

### spmd — SPMD
- aka: single program multiple data
- kind: execution-concurrency
- what: All processing elements run the same program, using their unique id to select the data partition and branch to role-specific behavior.
- problem: Writing and deploying one distinct program per processor does not scale; a single parameterized program keeps parallel code maintainable while allowing per-rank specialization.
- named-in: Patterns for Parallel Programming - Mattson, Sanders, Massingill (2004)
- tags: hpc, mpi, gpu

### stencil — Stencil
- aka: stencil computation, structured-grid pattern, neighborhood computation, ghost cells (supporting mechanism)
- kind: execution-concurrency
- what: Update every element of a regular grid as a fixed function of its spatial neighborhood, typically double-buffered between generations and tiled/parallelized over the grid.
- problem: Grid computations (image filters, cellular automata, PDE solvers, convolution) share a regular neighbor-access shape whose naive form thrashes caches and races on in-place updates.
- named-in: McCool, Robison, Reinders, Structured Parallel Programming: Patterns for Efficient Computation (2012), stencil chapter
- tags: scientific-computing, games, borderline: domain-parallel kernel shape at the algorithm-zoo edge; kept on pattern-catalog naming and cross-domain recurrence

### structured-concurrency — Structured Concurrency
- aka: nursery pattern, task scope, scoped concurrency, concurrency scopes, nursery (Trio), task scope / StructuredTaskScope (Java), coroutine scope (Kotlin), scoped task spawning
- kind: execution-concurrency
- what: Concurrent tasks may only be spawned inside a lexical scope (nursery / task scope) that cannot be exited until all child tasks complete, so errors and cancellation propagate through a tree of scopes.
- problem: Fire-and-forget spawning (go statement, detached threads) breaks local reasoning, error propagation, and cancellation; binding task lifetimes to block structure restores them, analogous to structured programming's elimination of goto.
- named-in: Smith, Notes on structured concurrency, or: Go statement considered harmful (vorpus.org, 2018); Trio nursery documentation; JEP 453: Structured Concurrency (JDK 21)
- tags: python-trio, kotlin-coroutines, java, swift-concurrency

### thread-pool — Thread Pool
- aka: worker pool, pooled threads
- kind: execution-concurrency
- what: A fixed or bounded set of pre-created worker threads that repeatedly take tasks from a queue and execute them, amortizing thread creation cost.
- problem: Creating a thread per task wastes creation/teardown cost and allows unbounded resource consumption under load; a pool bounds concurrency and reuses threads.
- named-in: Java Concurrency in Practice - Goetz, Peierls, Bloch, Bowbeer, Holmes, Lea (2006)
- tags: java, servers, spot-checked-wikipedia-concurrency-pattern-list

### thread-specific-storage — Thread-Specific Storage
- aka: Thread-Local Storage, TLS, per-thread data, Per-CPU Data Sharding, data ownership, per-CPU variables, counter sharding
- kind: execution-concurrency
- what: Each thread gets its own copy of a logically global datum, accessed through one 'global' access point that transparently resolves to the calling thread's instance.
- problem: Data such as errno or per-thread caches must be globally reachable yet not shared, avoiding both lock contention and explicit parameter threading.
- named-in: corpus:posa2 — Pattern-Oriented Software Architecture Vol. 2: Patterns for Concurrent and Networked Objects - Schmidt, Stal, Rohnert, Buschmann (2000)
- tags: threads, systems, c, cpp, java, linux-kernel

### threaded-code — Threaded Code
- aka: direct threading, indirect threading, computed-goto dispatch
- kind: execution-concurrency
- what: An interpreter code representation where the program is a sequence of addresses of operation routines, each routine jumping directly to the next, eliminating a central decode-dispatch loop.
- problem: A switch-based dispatch loop pays a decode branch per instruction and defeats branch prediction; threading the code through direct jumps cuts dispatch overhead and code size, historically crucial on memory-constrained machines (Forth).
- named-in: Threaded Code - James R. Bell, Communications of the ACM (1973)
- tags: interpreters, forth, embedded, performance

### trampoline — Trampoline
- aka: trampolined style, bounce loop
- kind: execution-concurrency
- what: A driver loop that repeatedly invokes returned thunks/step objects so that deep or mutual recursion runs in constant stack space.
- problem: Avoids stack overflow from deep tail or mutual recursion on runtimes without tail-call elimination by converting nested calls into iterated returns.
- named-in: Trampolined Style - Ganz, Friedman, Wand (ICFP, 1999)
- tags: fp, java, javascript, scala, clojure

### two-phase-termination — Two-Phase Termination
- aka: cooperative shutdown, graceful thread termination
- kind: execution-concurrency
- what: Shutting down a thread or active object by setting a termination request flag (phase 1) that the target observes at safe points, then letting it release resources and exit cleanly (phase 2).
- problem: Forcibly killing threads corrupts shared state and leaks resources; termination must be a cooperative protocol in which the thread finishes or abandons work at well-defined points.
- named-in: Patterns in Java, Volume 1: A Catalog of Reusable Design Patterns Illustrated with UML - Grand (1998)
- tags: java


## Synchronization & coordination — `synchronization-coordination` (57)

### aba-mitigation-via-tagged-pointer — ABA Mitigation via Tagged Pointer
- aka: version counter, modification counter, stamped reference, generation count
- kind: synchronization-coordination
- what: Pair the CAS-protected word with a monotonically increasing tag/version so a value that was changed and changed back still fails the CAS.
- problem: Plain CAS cannot distinguish 'unchanged' from 'changed A->B->A', which corrupts lock-free structures that recycle nodes; the tag makes every mutation observable.
- named-in: The Art of Multiprocessor Programming - Herlihy & Shavit (2008)
- tags: c, cpp, systems

### acquire-release-ordering — Acquire-Release Ordering
- aka: acquire/release semantics, release-acquire pairing, publication safety
- kind: synchronization-coordination
- what: Pair a release-ordered store by the producer with an acquire-ordered load by the consumer so everything written before the release is visible after the acquire, without full fences.
- problem: Sequentially-consistent atomics are needlessly expensive for the common publish/consume handoff; the acquire-release pair expresses exactly the one-way visibility the handoff needs.
- named-in: Acquire and Release Semantics - Jeff Preshing (2012)
- tags: cpp, c, rust, systems, borderline — Codified as language memory-model vocabulary (C++11/C11), but used as a portable design discipline for lockless handoff rather than a single-keyword feature.

### balking — Balking
- aka: balk
- kind: synchronization-coordination
- what: A method that immediately returns (or reports failure) instead of waiting when the object is not in an appropriate state to execute the request.
- problem: Some requests are only valid in a particular state and are pointless to queue (e.g., saving when no changes are dirty, starting an already-started service); refusing beats blocking.
- named-in: Patterns in Java, Volume 1: A Catalog of Reusable Design Patterns Illustrated with UML - Grand (1998)
- tags: java, spot-checked-wikipedia-concurrency-pattern-list

### coarse-grained-lock — Coarse-Grained Lock
- aka: —
- kind: synchronization-coordination
- what: Locks a group of related objects with a single lock (often a shared version object or a lock on an aggregate root) instead of locking each member.
- problem: Locking every object in a cluster is expensive and deadlock-prone when the cluster changes as a unit; one lock covering the whole group makes acquisition atomic and cheap.
- named-in: Patterns of Enterprise Application Architecture - Martin Fowler (2002)
- tags: enterprise, concurrency

### compare-and-swap-loop — Compare-and-Swap Loop
- aka: CAS, atomic variables, atomic read-modify-write, optimistic retry loop, CAS Retry Loop, read-modify-CAS loop, LL/SC retry loop
- kind: synchronization-coordination
- what: The nonblocking update idiom: read the current value, compute a new value, and atomically install it only if the location still holds the value read, retrying on failure.
- problem: Lock-based updates of single words suffer contention, priority inversion, and deadlock risk; a CAS retry loop achieves lock-free progress for small state transitions.
- named-in: Wait-Free Synchronization - Herlihy (1991)
- tags: c, cpp, java, systems, embedded, borderline — The bare CAS instruction is a hardware/ISA primitive below the design band; included for the CAS-retry-loop / atomic-variable design idiom as taught in JCiP ch. 15 and the nonblocking literature.

### condition-variable — Condition Variable
- aka: condition queue, wait/notify condition
- kind: synchronization-coordination
- what: A queue on which threads wait, releasing an associated lock, until another thread signals that a state predicate may now hold; woken threads re-acquire the lock and re-test the predicate.
- problem: Threads must wait efficiently for a condition over shared state to become true; busy-polling wastes CPU and naive sleep/wake without a lock protocol loses wakeups.
- named-in: Monitors: An Operating System Structuring Concept - Hoare (1974)
- tags: c, cpp, java, os

### coordinator — Coordinator
- aka: Task Coordinator
- kind: synchronization-coordination
- what: A coordinator drives a task spanning multiple participants through prepare and commit phases so either all participants complete their work or none do.
- problem: A task touching several resources/participants must not leave the system partially updated on failure; two-phase coordination yields all-or-nothing semantics at design level.
- named-in: corpus:posa3 — Pattern-Oriented Software Architecture Vol. 3: Patterns for Resource Management - Kircher, Jain (2004)
- tags: atomicity, transactions

### critical-region — Critical Region
- aka: critical section, interrupt masking, Mutex, mutual exclusion lock, lock, Single Threaded Execution
- kind: synchronization-coordination
- what: Making a code region atomic by disabling interrupts or task switching (or holding a global lock) for its duration.
- problem: Shared data touched by ISRs or multiple tasks can be corrupted by preemption mid-update; the bluntest fix is to forbid preemption across the update.
- named-in: corpus:douglasspatternsc — Design Patterns for Embedded Systems in C - Bruce Powel Douglass (2011)
- tags: embedded, concurrency, os, c, cpp

### deadlock-detection — Deadlock Detection
- aka: waits-for graph detection, cycle detection in wait graph, deadlock victim selection
- kind: synchronization-coordination
- what: Maintain a waits-for graph of which transactions block which, periodically detect cycles, and break them by aborting a chosen victim (alternatives: timeouts, wound-wait/wait-die prevention).
- problem: Blocking lock protocols can produce circular waits that never resolve; explicit detection converts a permanent hang into a bounded abort-and-retry.
- named-in: Transaction Processing: Concepts and Techniques - Gray & Reuter (1992)
- tags: db, concurrency, os

### direct-to-task-notification — Direct-to-Task Notification
- aka: task notification, notification value, thread flags (CMSIS-RTOS2 analog), lightweight task signal
- kind: synchronization-coordination
- what: Each task carries built-in notification slots (a 32-bit value plus pending state) that other tasks or ISRs can set, increment, overwrite, or OR bits into, letting the task block on its own notification instead of on a separate kernel object.
- problem: Binary/counting semaphores, event flags, and one-deep mailboxes used purely to wake a single known task cost a separate kernel object and slower code paths; notifying the receiving task directly is significantly faster and uses less RAM when there is exactly one receiver.
- named-in: corpus:freertosbook — freertos.org 'Direct to task notifications' (title verified live 2026-07-10); Mastering the FreeRTOS Real-Time Kernel; CMSIS-RTOS2 Thread Flags API
- tags: embedded, freertos, cmsis-rtos, rtos

### double-checked-locking — Double-Checked Locking
- aka: DCLP, Double-Checked Locking Optimization, Lock Hint, DCL
- kind: synchronization-coordination
- what: Code checks a condition (typically 'initialized?') before and again after acquiring a lock, so the common already-initialized path skips locking entirely.
- problem: Thread-safe lazy initialization of shared state without paying lock overhead on every access; note the pattern is broken without memory-ordering guarantees (fences/atomics), a hazard documented since its publication.
- named-in: corpus:posa2 — Pattern-Oriented Software Architecture Vol. 2: Patterns for Concurrent and Networked Objects - Schmidt, Stal, Rohnert, Buschmann (2000)
- tags: c++, java, memory-model, lazy-init, cpp, spot-checked-wikipedia-concurrency-pattern-list

### event-flags-group — Event Flags Group
- aka: event group (FreeRTOS), event flags (CMSIS-RTOS2, ThreadX, uC/OS), event register, event set, AND/OR flag wait
- kind: synchronization-coordination
- what: A kernel object holding a word of boolean event bits that tasks and ISRs set or clear atomically and that tasks block on with AND/OR combinations of bits, optionally auto-clearing the bits on wake.
- problem: A task must wait for any-of or all-of several distinct conditions signaled by different tasks/ISRs; semaphores signal only a single anonymous event and compose poorly for conjunction/disjunction waits.
- named-in: corpus:freertosbook — Mastering the FreeRTOS Real-Time Kernel (event groups chapter)
- tags: embedded, rtos, cmsis-rtos

### eventcount — Eventcount
- aka: eventcounts and sequencers, event count with sequencer
- kind: synchronization-coordination
- what: A monotonically increasing counter that threads can read, advance, and await reaching a value, letting a lock-free fast path add blocking ('sleep until something changed') without locks.
- problem: Pure lock-free algorithms busy-wait when empty; an eventcount lets consumers block on a condition over lock-free state without introducing a mutex into the producer path.
- named-in: Synchronization with Eventcounts and Sequencers - Reed & Kanodia (1979)
- tags: c, cpp, systems

### fencing-token — Fencing Token
- aka: fencing, monotonic lock token
- kind: synchronization-coordination
- what: Attach a monotonically increasing token to each lock/lease grant; resources reject requests bearing a token older than one already seen, fencing off stale holders.
- problem: A paused or partitioned client may act on an expired lease it believes it still holds; token comparison at the resource makes such zombie writes rejectable.
- named-in: Designing Data-Intensive Applications - Kleppmann (2017)
- tags: distributed

### flat-combining — Flat Combining
- aka: combining funnel (ancestor), delegation via combiner
- kind: synchronization-coordination
- what: Threads publish operation requests to a shared list; one thread acquires a global lock and applies everyone's pending operations in a batch on their behalf.
- problem: Under high contention, N threads fighting for a structure cost more than one thread doing N operations; combining turns synchronization overhead into cheap sequential batching.
- named-in: Flat Combining and the Synchronization-Parallelism Tradeoff - Hendler, Incze, Shavit & Tzafrir (2010)
- tags: cpp, java, systems

### futex — Futex
- aka: fast userspace mutex, futex-based blocking
- kind: synchronization-coordination
- what: Synchronization objects keep their state in a plain userspace word manipulated with atomics; the kernel is invoked only to sleep on or wake waiters when the fast path fails.
- problem: Uncontended lock and unlock should cost one atomic instruction with zero syscalls, while contended waiters still block properly instead of spinning.
- named-in: Fuss, Futexes and Furwocks: Fast Userlevel Locking in Linux - Franke, Russell & Kirkwood (2002)
- tags: c, linux, systems, borderline — Kernel-assisted: the mechanism spans a syscall boundary, but the design element (userspace fast path + kernel wait queue keyed by address) is implemented inside one component and recurs across runtimes.

### guarded-call — Guarded Call
- aka: mutex-protected call, protected synchronous call
- kind: synchronization-coordination
- what: Cross-thread service invocation performed synchronously but guarded by a mutual-exclusion semaphore so only one caller executes the service at a time.
- problem: Asynchronous queuing adds latency, but naked synchronous calls across threads race; serializing calls through a mutex gives timely, safe access.
- named-in: corpus:douglasspatternsc — Design Patterns for Embedded Systems in C - Bruce Powel Douglass (2011)
- tags: embedded, concurrency

### guarded-suspension — Guarded Suspension
- aka: guarded wait, guarded methods
- kind: synchronization-coordination
- what: A method that suspends the calling thread until a precondition (guard) over the object's state becomes true, then executes; the wait-loop-on-condition-variable pattern form.
- problem: An operation only makes sense in certain object states; rather than failing or polling, the caller blocks until another thread changes the state and signals.
- named-in: Patterns in Java, Volume 1: A Catalog of Reusable Design Patterns Illustrated with UML - Grand (1998)
- tags: java, spot-checked-wikipedia-concurrency-pattern-list

### implicit-lock — Implicit Lock
- aka: —
- kind: synchronization-coordination
- what: Has framework or layer-supertype code acquire the needed offline locks automatically so application code cannot forget them.
- problem: Offline locking only works if every code path locks correctly, and one forgotten lock silently corrupts data; moving acquisition into shared plumbing makes locking unskippable.
- named-in: Patterns of Enterprise Application Architecture - Martin Fowler (2002)
- tags: enterprise, concurrency

### interrupt-masking-critical-section — Interrupt-Masking Critical Section
- aka: disabling interrupts, interrupt lock, PRIMASK/BASEPRI critical section
- kind: synchronization-coordination
- what: Protect data shared between mainline code and ISRs by briefly disabling (or priority-masking) interrupts around the access.
- problem: An interrupt arriving mid-update leaves shared data half-written (the shared-data problem); masking interrupts for a short bounded window makes the access atomic on a uniprocessor.
- named-in: corpus:dsimonprimer — An Embedded Software Primer - Simon (1999)
- tags: embedded, interrupts, borderline — Overlaps the general critical-section element owned by the synchronization scout; kept for its ISR-specific form and naming.

### latch — Latch
- aka: countdown latch, gate, one-shot barrier
- kind: synchronization-coordination
- what: A one-shot synchronizer that blocks waiting threads until it reaches its terminal (open) state - typically when a count of prerequisite events reaches zero - and then stays open forever.
- problem: Threads must not proceed until some set of initialization steps or prerequisite tasks has completed exactly once; a latch expresses this irreversible ready condition directly.
- named-in: Java Concurrency in Practice - Goetz, Peierls, Bloch, Bowbeer, Holmes, Lea (2006)
- tags: java

### lock-escalation — Lock Escalation
- aka: lock promotion to coarser granularity
- kind: synchronization-coordination
- what: When a transaction holds too many fine-grained locks, the lock manager replaces them with a single coarser-granularity lock to cap lock-table memory.
- problem: Fine-grained locking has per-lock overhead that can exhaust the lock table; escalation trades concurrency for bounded lock-manager resources.
- named-in: Transaction Processing: Concepts and Techniques - Gray & Reuter (1992)
- tags: db, concurrency, borderline — A resource-bounding policy inside the lock manager rather than a standalone mechanism; included as it is named, recurring, and independently implementable.

### lock-striping — Lock Striping
- aka: striped locking, lock splitting (coarser sibling), striped locks, lock splitting (finer-grained variant), segmented locking
- kind: synchronization-coordination
- what: Partitioning a data structure's protection across an array of locks (e.g., one per hash-bucket group) so independent operations contend only on their stripe.
- problem: A single lock over a large structure serializes logically independent operations; striping trades a bounded increase in lock count for near-linear reduction in contention.
- named-in: Java Concurrency in Practice - Goetz, Peierls, Bloch, Bowbeer, Holmes, Lea (2006)
- tags: java, cpp, systems

### logical-clock — Logical Clock
- aka: Lamport clock, Lamport timestamp, vector clock, version vector, hybrid logical clock (HLC)
- kind: synchronization-coordination
- what: A per-process counter (scalar or vector) advanced on local events and merged on message receipt so that timestamp order respects causal (happened-before) order without synchronized physical clocks.
- problem: Concurrent and distributed components need to order events, detect causality, and version state when wall clocks are unreliable or unavailable.
- named-in: Lamport, 'Time, Clocks, and the Ordering of Events in a Distributed System', CACM 1978
- tags: distributed, in-process mechanism precedent: crdt and operational-transformation already in catalog

### mcs-queue-lock — MCS Queue Lock
- aka: MCS lock, queue-based spinlock, CLH lock (variant), qspinlock
- kind: synchronization-coordination
- what: Waiters enqueue a per-thread node and spin only on their own node's flag; the releaser hands the lock to its queue successor.
- problem: Global-spin locks generate cache-coherence traffic proportional to waiters; local spinning on a private cache line makes acquisition scalable and FIFO-fair on many-core machines.
- named-in: Algorithms for Scalable Synchronization on Shared-Memory Multiprocessors - Mellor-Crummey & Scott (1991)
- tags: c, linux-kernel, systems

### memory-barrier — Memory Barrier
- aka: memory fence, smp_mb, full fence, store/load barrier
- kind: synchronization-coordination
- what: An explicit instruction or compiler directive that constrains the order in which memory operations before and after it may become visible to other processors.
- problem: Compilers and CPUs reorder memory accesses; lockless code communicating through shared memory must pin down ordering at the points where publication and observation happen.
- named-in: Linux kernel memory-barriers.txt - McKenney, Howells et al. (Linux kernel documentation)
- tags: c, cpp, embedded, systems, borderline — Sits at the hardware/language floor of the band, but barrier placement discipline is a named, recurring design activity in every lockless codebase, distinct from the raw instruction.

### monitor-object — Monitor Object
- aka: Monitor, synchronized object
- kind: synchronization-coordination
- what: An object synchronizes its own method execution with an internal lock plus condition variables, so at most one method runs at a time and methods can wait for state conditions inside the object.
- problem: Multiple threads share one object; the object itself, not its clients, should enforce mutual exclusion and cooperative scheduling on its state (mechanism rooted in Hoare's 1974 monitors).
- named-in: corpus:posa2 — Pattern-Oriented Software Architecture Vol. 2: Patterns for Concurrent and Networked Objects - Schmidt, Stal, Rohnert, Buschmann (2000)
- tags: threads, condition-variables, java, os, spot-checked-wikipedia-concurrency-pattern-list

### multi-granularity-locking — Multi-Granularity Locking
- aka: intention locks, intent locks, hierarchical locking, MGL
- kind: synchronization-coordination
- what: Locks are taken at multiple granularities (database, table, page, row) with intention modes (IS, IX, SIX) on ancestors advertising finer-grained locks below.
- problem: Row-only locking makes whole-table operations acquire millions of locks, while table-only locking kills concurrency; the intention-mode hierarchy lets both coexist with cheap conflict checks.
- named-in: Granularity of Locks and Degrees of Consistency in a Shared Data Base - Gray, Lorie, Putzolu & Traiger (1976)
- tags: db, concurrency

### multiversion-concurrency-control — Multiversion Concurrency Control
- aka: MVCC, multi-version concurrency control, versioned records
- kind: synchronization-coordination
- what: Keep multiple timestamped versions of each data item so readers see a consistent older version while writers create new ones, with obsolete versions garbage-collected later.
- problem: Lock-based schemes make readers and writers block each other; versioning lets reads proceed without locks against a stable snapshot at the cost of version storage and cleanup (vacuum).
- named-in: Multiversion Concurrency Control - Theory and Algorithms - Bernstein & Goodman (1983)
- tags: db, concurrency

### operational-transformation — Operational Transformation
- aka: OT, dOPT (original algorithm)
- kind: synchronization-coordination
- what: Keep concurrently edited replicas consistent by transforming each incoming operation against the concurrent operations already applied locally, preserving intention and causality without locking.
- problem: Optimistic concurrent editing of shared data (collaborative text editors) requires every replica to converge to the same state while staying responsive; transforming operations reorders their effects instead of blocking users.
- named-in: Ellis & Gibbs, Concurrency Control in Groupware Systems (ACM SIGMOD 1989, pp. 399-407)
- tags: collaborative-editing, alternative-to:conflict-free-replicated-data-type-crdt

### optimistic-concurrency-control — Optimistic Concurrency Control
- aka: OCC, optimistic concurrency control, optimistic locking, validate-then-commit, validation-based concurrency control, version validation
- kind: synchronization-coordination
- what: Proceed without locks, recording versions of the data read; at commit time re-check the versions and retry the whole operation if anything changed.
- problem: When conflicts are rare, pessimistic locking pays its cost on every access; optimistic validation moves the cost to the rare conflicting case.
- named-in: On Optimistic Methods for Concurrency Control - Kung & Robinson (1981)
- tags: databases, systems, java, db, concurrency

### optimistic-offline-lock — Optimistic Offline Lock
- aka: —
- kind: synchronization-coordination
- what: Prevents conflicts between concurrent business transactions by validating at commit time (typically via a version field) that no other session changed the data since it was read.
- problem: Business transactions span multiple requests and cannot hold database locks throughout; assuming conflict is rare, detect it at commit and roll back the loser instead of blocking everyone.
- named-in: Patterns of Enterprise Application Architecture - Martin Fowler (2002)
- tags: enterprise, concurrency

### ordered-locking — Ordered Locking
- aka: lock ordering, lock hierarchy, resource ordering
- kind: synchronization-coordination
- what: Every lockable resource gets a global order/ID and all tasks must acquire locks in strictly increasing order, making circular wait impossible.
- problem: Deadlock requires a cycle of waiters; imposing a total acquisition order breaks all cycles while still allowing incremental locking.
- named-in: corpus:douglasspatternsc — Design Patterns for Embedded Systems in C - Bruce Powel Douglass (2011)
- tags: embedded, concurrency, deadlock-avoidance

### pessimistic-offline-lock — Pessimistic Offline Lock
- aka: —
- kind: synchronization-coordination
- what: Prevents conflicts between concurrent business transactions by acquiring an application-managed lock on data before working with it, forcing other sessions to wait or be refused.
- problem: When conflicts are likely or losing work at commit is unacceptable, optimistic validation is too costly; an explicit lock table owned by the application serializes access across long-running sessions.
- named-in: Patterns of Enterprise Application Architecture - Martin Fowler (2002)
- tags: enterprise, concurrency

### priority-ceiling-protocol — Priority Ceiling Protocol
- aka: Priority Ceiling Pattern, PCP, Highest Locker Pattern, immediate priority ceiling protocol, highest locker protocol, immediate ceiling priority protocol
- kind: synchronization-coordination
- what: Each resource is assigned a ceiling priority equal to the highest priority of any task that may lock it, and locking rules built on the ceilings bound blocking to one critical section and prevent deadlock.
- problem: Priority inheritance alone still permits chained blocking and deadlock among nested locks; ceilings give a stronger, analyzable bound.
- named-in: corpus:douglassrtcorpus — Real-Time Design Patterns - Bruce Powel Douglass (2002)
- tags: embedded, real-time, concurrency, rtos

### priority-inheritance-protocol — Priority Inheritance Protocol
- aka: priority inheritance, PIP
- kind: synchronization-coordination
- what: A task holding a lock temporarily inherits the highest priority of any task blocked on that lock, releasing the boost when it unlocks.
- problem: Unbounded priority inversion: a medium-priority task can preempt a low-priority lock holder indefinitely, starving the blocked high-priority task (the Mars Pathfinder failure mode).
- named-in: Priority Inheritance Protocols: An Approach to Real-Time Synchronization - Sha, Rajkumar & Lehoczky (1990)
- tags: embedded, real-time, concurrency, rtos

### read-copy-update — Read-Copy-Update
- aka: RCU, quiescent-state-based reclamation, QSBR
- kind: synchronization-coordination
- what: Readers traverse shared data with essentially zero synchronization while updaters publish new versions atomically and defer reclamation of old versions until all pre-existing readers have finished (a grace period).
- problem: Read-mostly kernel/data-plane structures cannot afford reader-side locks or atomics; RCU shifts the entire coordination cost to the rare update path.
- named-in: Read-Copy Update: Using Execution History to Solve Concurrency Problems - McKenney, Slingwine (1998)
- tags: c, linux-kernel, os, systems

### readers-writer-lock — Readers-Writer Lock
- aka: read-write lock, shared-exclusive lock, RW lock
- kind: synchronization-coordination
- what: A lock admitting either many concurrent readers or one exclusive writer, exploiting the fact that reads do not conflict with each other.
- problem: Read-mostly data serialized behind a plain mutex forfeits read parallelism; distinguishing shared from exclusive access recovers it at the cost of fairness/starvation policy decisions.
- named-in: Concurrent Control with 'Readers' and 'Writers' - Courtois, Heymans, Parnas (1971)
- tags: os, c, java, spot-checked-wikipedia-concurrency-pattern-list

### reentrant-lock — Reentrant Lock
- aka: recursive lock, recursive mutex
- kind: synchronization-coordination
- what: A mutex variant that the holding thread may re-acquire without deadlocking, tracked by owner and hold count; charter-noted as a variant of the plain mutex kept separate for its distinct semantics.
- problem: Lock-guarded methods that call other guarded methods on the same object self-deadlock under a non-reentrant mutex; reentrancy makes lock acquisition composable within one thread.
- named-in: Java Concurrency in Practice - Goetz, Peierls, Bloch, Bowbeer, Holmes, Lea (2006)
- tags: java, c, posix

### rendezvous — Rendezvous
- aka: barrier synchronization, synchronization point, extended rendezvous, entry call/accept, Barrier, cyclic barrier, phase barrier
- kind: synchronization-coordination
- what: An explicit synchronization object at which multiple tasks wait until a predetermined condition (e.g., all parties arrived) is met, then proceed together.
- problem: Independently scheduled tasks sometimes must align at known points before continuing; ad hoc flag-spinning is error-prone and unanalyzable.
- named-in: corpus:douglasspatternsc — Design Patterns for Embedded Systems in C - Bruce Powel Douglass (2011)
- tags: embedded, concurrency, ada, realtime, hpc, java, spot-checked-wikipedia-concurrency-pattern-list

### safe-publication — Safe Publication
- aka: safe object publication
- kind: synchronization-coordination
- what: The set of idioms (final fields, volatile references, locks, initialized statics, concurrent collections) that make an object and its state visible to other threads in a fully constructed form.
- problem: Handing a reference from a constructing thread to another thread without a happens-before edge can expose partially constructed state; publication must use a memory-model-sanctioned channel.
- named-in: Java Concurrency in Practice - Goetz, Peierls, Bloch, Bowbeer, Holmes, Lea (2006)
- tags: java, borderline — More a memory-model correctness discipline than a standalone mechanism, but it is named, recurring, and taught as a unit in JCiP; charter flags it borderline and includes it.

### safepoint — Safepoint
- aka: GC point, GC-safe point, safepoint poll (polling-page / poll-instruction mechanism), stop-the-world synchronization point, yieldpoint (generalized form)
- kind: synchronization-coordination
- what: A designated point in generated or interpreted code at which a thread's state (GC roots, stack maps) is fully described and the thread can be safely blocked; the runtime brings all threads to safepoints (via polls, page-protection tricks, or interpreter checks) before running GC, deoptimization, or other global VM operations.
- problem: A runtime cannot scan stacks, move objects, or patch code while mutator threads are at arbitrary instructions; restricting global operations to well-described points bounds metadata cost and makes stop-the-world coordination correct and cheap on the fast path.
- named-in: OpenJDK, 'HotSpot Glossary of Terms' (openjdk.org, verified live this session); mechanism analyzed in Agesen, 'GC Points in a Threaded Environment' (Sun Labs TR SMLI TR-98-70, 1998)
- tags: virtual machines, language runtimes, garbage collection, JIT

### scoped-locking — Scoped Locking
- aka: Synchronized Block idiom, Guard idiom
- kind: synchronization-coordination
- what: A guard object acquires a lock in its constructor and releases it in its destructor, so every exit path from a scope (including exceptions) releases the lock.
- problem: Manually paired lock/unlock calls leak locks on early returns and exceptions; RAII applied to locks makes release automatic and exception-safe.
- named-in: corpus:posa2 — Pattern-Oriented Software Architecture Vol. 2: Patterns for Concurrent and Networked Objects - Schmidt, Stal, Rohnert, Buschmann (2000)
- tags: c++, idiom, raii

### self-pipe-trick — Self-Pipe Trick
- aka: self-pipe, wakeup pipe
- kind: synchronization-coordination
- what: A process writes a byte to a pipe it also polls, converting an asynchronous event (typically a signal) into a file-descriptor readiness event handled in the main event loop.
- problem: Signals interrupt at arbitrary points and cannot safely do real work, and select/poll cannot wait on them directly; funneling the notification through a self-owned pipe unifies all wakeups race-free in one multiplexing point. Modern kernel equivalents (eventfd, signalfd, pselect) folded here as notes; attributed to D. J. Bernstein.
- named-in: The Linux Programming Interface - Michael Kerrisk (2010), sec. 63.5.2 'The Self-Pipe Trick'
- tags: c, unix, event-loop

### semaphore — Semaphore
- aka: counting semaphore, binary semaphore, P/V operations
- kind: synchronization-coordination
- what: An integer counter with atomic wait (decrement-or-block) and signal (increment-and-wake) operations, used to control access to a pool of permits.
- problem: Programs need to bound how many threads enter a region or consume a finite resource, and to signal occurrence of events between threads, with primitive-level generality.
- named-in: Cooperating Sequential Processes - Dijkstra (1965)
- tags: os, embedded, c

### sequence-lock — Sequence Lock
- aka: seqlock, sequence counter, seqcount
- kind: synchronization-coordination
- what: A writer increments a sequence counter before and after updating; readers retry their lock-free read if the counter was odd or changed across the read.
- problem: Lets many readers access small, frequently-read data without locking while guaranteeing they never act on a torn/inconsistent snapshot; writers never wait for readers.
- named-in: Sequence counters and sequential locks - Linux kernel documentation (locking/seqlock.rst)
- tags: c, linux-kernel, systems, embedded

### simultaneous-locking — Simultaneous Locking
- aka: all-or-none resource locking
- kind: synchronization-coordination
- what: A task acquires all resources it will need in one atomic all-or-none step (releasing everything on partial failure), so it never holds some while waiting for others.
- problem: Deadlock requires hold-and-wait; grabbing the whole resource set atomically removes that condition at the cost of reduced concurrency.
- named-in: corpus:douglasspatternsc — Design Patterns for Embedded Systems in C - Bruce Powel Douglass (2011)
- tags: embedded, concurrency, deadlock-avoidance

### snapshot-isolation — Snapshot Isolation
- aka: SI
- kind: synchronization-coordination
- what: A transaction reads from a consistent snapshot taken at its start and commits only if no concurrent committed transaction wrote the same items (first-committer-wins).
- problem: Gives long-running reads a stable, non-blocking view while catching write-write conflicts; weaker than serializability (admits write skew), which is exactly the trade-off it names.
- named-in: A Critique of ANSI SQL Isolation Levels - Berenson, Bernstein, Gray, Melton, O'Neil & O'Neil (1995)
- tags: db, concurrency, borderline — Primarily an isolation-level semantics; included because it names the concrete snapshot-read + first-committer-wins mechanism MVCC engines implement.

### software-transactional-memory — Software Transactional Memory
- aka: STM, atomic blocks, transactional memory (software)
- kind: synchronization-coordination
- what: Shared-memory operations grouped into transactions that execute optimistically and commit atomically, aborting and retrying on conflict, giving composable lock-free-style synchronization.
- problem: Locks do not compose - correct lock-based components combine into deadlock-prone systems; transactions let programmers state atomicity declaratively and leave conflict resolution to the runtime.
- named-in: Software Transactional Memory - Shavit, Touitou (1995)
- tags: haskell, clojure, scala, cpp, systems

### spinlock — Spinlock
- aka: busy-wait lock, spin lock, test-and-set lock
- kind: synchronization-coordination
- what: A lock acquired by busy-waiting (repeatedly testing an atomic flag) instead of blocking, trading CPU cycles for elimination of scheduler round-trips.
- problem: For very short critical sections, or contexts where blocking is impossible (interrupt handlers, kernels), the cost of putting a thread to sleep exceeds the cost of spinning.
- named-in: The Performance of Spin Lock Alternatives for Shared-Memory Multiprocessors - Anderson (1990)
- tags: os, embedded, c

### strategized-locking — Strategized Locking
- aka: —
- kind: synchronization-coordination
- what: The synchronization mechanism a component uses is a pluggable strategy (template parameter or polymorphic lock object), including a null lock for single-threaded configurations.
- problem: The same component must run efficiently under different concurrency models; hard-wiring one lock type either wastes performance or sacrifices safety.
- named-in: corpus:posa2 — Pattern-Oriented Software Architecture Vol. 2: Patterns for Concurrent and Networked Objects - Schmidt, Stal, Rohnert, Buschmann (2000)
- tags: c++, policy

### test-and-test-and-set-lock — Test-and-Test-and-Set Lock
- aka: TTAS lock, spin-on-read spinlock, TTAS with exponential backoff
- kind: synchronization-coordination
- what: Spin reading the lock word from cache until it appears free, and only then attempt the atomic test-and-set; typically combined with exponential backoff between attempts.
- problem: Naive test-and-set spinning hammers the bus with atomic operations; spinning on a cached read plus backoff bounds coherence traffic under contention.
- named-in: The Art of Multiprocessor Programming - Herlihy & Shavit (2008)
- tags: c, cpp, systems, embedded

### thread-confinement — Thread Confinement
- aka: stack confinement, serial thread confinement
- kind: synchronization-coordination
- what: Restricting all access to mutable data to a single thread, making synchronization unnecessary for that data.
- problem: Shared mutable state requires locking that is easy to get wrong; if data is only ever touched by one thread (e.g., a UI thread or per-connection handler), thread safety follows by construction.
- named-in: Java Concurrency in Practice - Goetz, Peierls, Bloch, Bowbeer, Holmes, Lea (2006)
- tags: java, ui

### thread-safe-interface — Thread-Safe Interface
- aka: —
- kind: synchronization-coordination
- what: Public interface methods acquire the component's lock and then delegate to non-locking private implementation methods; implementation methods never call locking interface methods.
- problem: Intra-component method calls under a non-recursive mutex cause self-deadlock or needless locking overhead; a locking discipline at the interface boundary avoids both.
- named-in: corpus:posa2 — Pattern-Oriented Software Architecture Vol. 2: Patterns for Concurrent and Networked Objects - Schmidt, Stal, Rohnert, Buschmann (2000)
- tags: locking-discipline

### ticket-lock — Ticket Lock
- aka: ticket spinlock, bakery-style spinlock
- kind: synchronization-coordination
- what: A spinlock built from two counters: acquirers atomically take a ticket and spin until the now-serving counter reaches it.
- problem: Test-and-set spinlocks are unfair and cause contention storms; the ticket discipline grants the lock in strict FIFO order with one atomic op per acquisition.
- named-in: Algorithms for Scalable Synchronization on Shared-Memory Multiprocessors - Mellor-Crummey & Scott (1991)
- tags: c, linux-kernel, systems, embedded

### timestamp-ordering-concurrency-control — Timestamp-Ordering Concurrency Control
- aka: T/O, timestamp ordering, basic timestamp ordering
- kind: synchronization-coordination
- what: Assign each transaction a unique timestamp at start and enforce that all conflicting reads and writes execute in timestamp order, aborting operations that arrive too late.
- problem: Provides serializability without locks or deadlocks by pre-deciding the serialization order; the third classic concurrency-control family alongside 2PL and OCC.
- named-in: Concurrency Control in Distributed Database Systems - Bernstein & Goodman (1981)
- tags: db, concurrency

### two-phase-locking — Two-Phase Locking
- aka: 2PL, strict two-phase locking, S2PL
- kind: synchronization-coordination
- what: A locking discipline in which a transaction acquires all its locks before releasing any (growing then shrinking phase), which suffices to guarantee serializable executions.
- problem: Ad-hoc lock acquisition and release admits non-serializable interleavings; the two-phase rule is the classic protocol-level fix, at the price of blocking and possible deadlock.
- named-in: The Notions of Consistency and Predicate Locks in a Database System - Eswaran, Gray, Lorie & Traiger (1976)
- tags: db, concurrency


## State management — `state-management` (33)

### aggregate — Aggregate
- aka: —
- kind: state-management
- what: A cluster of associated objects treated as a single unit for data changes, with one root entity through which all external references and modifications must pass.
- problem: Invariants spanning several objects cannot be enforced if outside code mutates members freely; drawing a boundary with a single root gives a scope for consistency, locking, and atomic persistence.
- named-in: Domain-Driven Design: Tackling Complexity in the Heart of Software - Eric Evans (2003)
- tags: ddd, domain-modeling

### behavior-tree — Behavior Tree
- aka: BT, behaviour tree, behavior DAG (Isla)
- kind: state-management
- what: AI decision logic is structured as a tree of composable nodes (sequence, selector/fallback, parallel, decorators, leaf tasks) evaluated by periodic ticks that return success/failure/running, giving reactive hierarchical behavior without explicit state-transition wiring.
- problem: Flat and hierarchical FSMs for complex agents suffer transition explosion and poor reuse; a tree of prioritized, composable behaviors scales, supports designer-authored logic, and re-decides reactively every tick.
- named-in: Isla, 'Handling Complexity in the Halo 2 AI', GDC 2005; Champandard & Dunstan, 'The Behavior Tree Starter Kit', Game AI Pro, 2013
- tags: games, ai, robotics

### client-side-prediction — Client-Side Prediction
- aka: prediction and reconciliation, server reconciliation (companion mechanism), input prediction, prediction with rewind-and-replay, prediction, client prediction, server reconciliation (companion correction step)
- kind: state-management
- what: The client applies its own inputs to a locally predicted copy of authoritative state immediately, tags each input with a sequence number, and on receiving authoritative server state rewinds to it and replays still-unacknowledged inputs.
- problem: Waiting a full round trip for server-authoritative state makes controls feel laggy; predicting locally and reconciling against authoritative updates hides latency while keeping the server authoritative.
- named-in: Bernier, 'Latency Compensating Methods in Client/Server In-game Protocol Design and Optimization' (GDC 2001, Valve); Gambetta, 'Client-Side Prediction and Server Reconciliation' (verified live)
- tags: games, networking, UI-latency cousin: optimistic-ui-update (already in index, distinct mechanism)

### collections-for-states — Collections for States
- aka: —
- kind: state-management
- what: Objects are placed in per-state collections; an object's state is encoded by which collection currently holds it, and state transitions move it between collections.
- problem: When many objects cycle through the same modes and are processed per mode, storing state in each object forces scans; per-state collections make 'all objects in state X' direct.
- named-in: Pattern-Oriented Software Architecture Vol. 4: A Pattern Language for Distributed Computing - Buschmann, Henney, Schmidt (2007)
- tags: fsm, schedulers

### context-object — Context Object
- aka: —
- kind: state-management
- what: Execution-scoped state (security principal, transaction, locale, request data) is bundled into one context object passed along the processing path instead of via globals or long parameter lists.
- problem: Components along a call chain need shared per-activity state without global variables, thread coupling, or interface pollution with pass-through parameters.
- named-in: Pattern-Oriented Software Architecture Vol. 4: A Pattern Language for Distributed Computing - Buschmann, Henney, Schmidt (2007)
- tags: framework

### data-binding — Data Binding
- aka: property binding, one-way binding, two-way binding
- kind: state-management
- what: Declaratively connects a UI element's displayed value to a data source so changes propagate automatically instead of via hand-written synchronization code.
- problem: Keeping view and model state consistent by hand is repetitive and error-prone; binding centralizes the sync and lets direction (one-way source-to-view vs two-way round-trip) be declared, not coded.
- named-in: Data Binding Overview - WPF documentation - Microsoft
- tags: ui

### dead-reckoning — Dead Reckoning
- aka: dead reckoning models, predictive extrapolation of entity state, DIS dead reckoning, extrapolation (netcode)
- kind: state-management
- what: Each node extrapolates remote entities' current state from their last received kinematic update (position, velocity, acceleration) via an agreed model, and senders transmit a new update only when their real state diverges from the shared model beyond a threshold.
- problem: Broadcasting every entity's state every tick overwhelms bandwidth and latency hides the true present; a shared extrapolation model keeps remote entities moving plausibly between sparse, threshold-triggered updates.
- named-in: Aronson, 'Dead Reckoning: Latency Hiding for Networked Games', Gamasutra 1997; IEEE 1278.1 (DIS) dead reckoning algorithms
- tags: games, networking, simulation, borderline — Extrapolation complement of snapshot-interpolation (already in index); kept as its own element because it is independently named, standardized in DIS, and includes the sender-side threshold protocol, not just receiver-side smoothing.

### decomposed-and-state — Decomposed AND-State
- aka: AND-state decomposition, orthogonal regions implementation
- kind: state-management
- what: Implementing a statechart's concurrent (AND) regions by decomposing them into separate coordinated state machine objects, each handling its region's events.
- problem: Flattening independent concerns into one state machine multiplies states combinatorially; decomposing AND-states keeps each region's machine small and independently maintainable.
- named-in: corpus:douglasspatternsc — Design Patterns for Embedded Systems in C - Bruce Powel Douglass (2011)
- tags: c, embedded, statecharts

### deferred-event — Deferred Event
- aka: event deferral
- kind: state-management
- what: Events that arrive at an inconvenient state are set aside in a deferral queue and recalled for processing when the machine reaches a state that can handle them.
- problem: Dropping an out-of-sequence event loses information and handling it immediately corrupts the current activity; deferral preserves the event until the machine is ready.
- named-in: corpus:samekbook — Practical UML Statecharts in C/C++, 2nd ed. - Miro Samek (2008)
- tags: embedded, statecharts

### deterministic-lockstep — Deterministic Lockstep
- aka: lockstep simulation, lockstep protocol, input-synchronous simulation, synchronized simulation, lockstep networking
- kind: state-management
- what: Peers run bit-identical deterministic simulations from the same seed and exchange only per-tick inputs; each side advances a tick only once all participants' inputs for that tick have arrived.
- problem: Replicating full simulation state across the network scales with world size; if the simulation is deterministic, synchronizing inputs alone keeps all peers' states identical at input-sized bandwidth.
- named-in: Fiedler, 'Deterministic Lockstep' (gafferongames.com; verified live); Bettner & Terrano, '1500 Archers on a 28.8: Network Programming in Age of Empires and Beyond' (GDC 2001)
- tags: games, simulation, networking, borderline — spans peers, but included on the same footing as snapshot-interpolation: the mechanism (deterministic fixed tick + per-tick input queue gating) is implemented inside each program

### dirty-checking — Dirty Checking
- aka: change detection by comparison, digest cycle (AngularJS)
- kind: state-management
- what: Detects state changes by re-evaluating watched expressions and comparing new values against stored previous values in a check loop (repeated until stable), rather than by intercepting writes.
- problem: When state can be mutated by arbitrary plain code, there is no write hook to observe; periodic compare-against-last-value detects any change at the cost of scanning all watchers per cycle. Canonical in AngularJS's $digest; contrast with signals' write-time tracking.
- named-in: AngularJS Developer Guide - Scopes ($digest / dirty checking)
- tags: ui, js

### dirty-flag — Dirty Flag
- aka: dirty bit
- kind: state-management
- what: Track whether derived data is out of sync with its primary source using a boolean flag, and recompute the derived data only when it is both dirty and needed.
- problem: Expensive derived computation (world transforms, saved-state sync) should not rerun on every source change or every read; the flag defers and batches recalculation to the last responsible moment.
- named-in: Game Programming Patterns - Robert Nystrom (2014)
- tags: games

### dirty-rectangles — Dirty Rectangles
- aka: dirty-rectangle animation, dirty region tracking, damage rectangles, damage regions, invalidation rectangles
- kind: state-management
- what: Track the screen regions modified since the last frame and redraw or recomposite only those rectangles instead of the whole display.
- problem: Full-screen redraw wastes time when only small areas change (sprites over static background, UI repaint); region invalidation makes redraw cost proportional to actual change. A regional specialization of the dirty-flag idea, kept separate because the tracked unit (2D regions, merging/overlap handling) is its own mechanism.
- named-in: Michael Abrash's Graphics Programming Black Book - Michael Abrash (1997), ch. 45 'Dog Hair and Dirty Rectangles'
- tags: games, graphics, ui

### finite-state-machine — Finite State Machine
- aka: FSM, finite automaton, state machine
- kind: state-management
- what: Behavior modeled as a finite set of states, events, and transitions, where the reaction to an event depends on the current state.
- problem: Mode-dependent behavior coded as scattered flags and conditionals becomes untraceable; an explicit state model makes reachable behavior enumerable and verifiable.
- named-in: corpus:samekbook — Practical UML Statecharts in C/C++, 2nd ed. - Samek (2008)
- tags: embedded, foundational, c, c++

### hierarchical-state-machine — Hierarchical State Machine
- aka: statechart, HSM, Harel statechart, UML state machine
- kind: state-management
- what: A state machine extended with nested states (behavioral inheritance of transitions from enclosing states), orthogonal regions, and history, per Harel's statechart formalism.
- problem: Flat FSMs explode combinatorially and repeat identical transitions in many states; hierarchy factors out common behavior and orthogonality separates concurrent aspects.
- named-in: corpus:samekbook — Practical UML Statecharts in C/C++, 2nd ed. - Samek (2008); formalism from Harel, Statecharts: A Visual Formalism for Complex Systems (1987)
- tags: embedded, uml, statecharts, c, c++

### hydration — Hydration
- aka: client-side hydration, rehydration
- kind: state-management
- what: Attaches client-side behavior (event listeners, component state) to server-rendered static markup by re-running component logic and adopting the existing DOM instead of re-creating it.
- problem: Server-side rendering delivers fast first paint but inert markup; hydration makes it interactive without discarding the server's work, and mismatch detection guards divergence. Partial/lazy hydration and resumability (Qwik) are variants noted here.
- named-in: Server-Side Rendering (SSR) - Vue.js documentation (Client Hydration)
- tags: ui, js, borderline — Web-platform-specific rendering technique; passes the altitude test (implementable in one component, named, recurring) but domain-narrow.

### immutable-value — Immutable Value
- aka: Immutable Object, Immutable, value object (overlapping), value immutability, Immutable Instance (Fluent C)
- kind: state-management
- what: Value objects are made unmodifiable after construction, so they can be freely shared and aliased - including across threads - without copying or locking.
- problem: Shared mutable values require defensive copies or synchronization; immutability makes sharing safe by construction and simplifies reasoning about state.
- named-in: Pattern-Oriented Software Architecture Vol. 4: A Pattern Language for Distributed Computing - Buschmann, Henney, Schmidt (2007)
- tags: value-semantics, concurrency, java, functional, fp, oo

### interior-mutability — Interior Mutability
- aka: Cell/RefCell pattern, shared mutability behind immutable references
- kind: state-management
- what: Types like Cell/RefCell/Mutex allow controlled mutation through shared (immutable) references by moving aliasing checks to runtime or hardware.
- problem: Rust's aliasing rules forbid mutation through shared references, but caches, counters, and observer lists need it; interior mutability provides a sound, localized escape hatch.
- named-in: The Rust Programming Language - Klabnik & Nichols ('RefCell<T> and the Interior Mutability Pattern')
- tags: rust

### lag-compensation — Lag Compensation
- aka: server-side rewind, backward reconciliation, lag-compensated hit detection, favor the shooter
- kind: state-management
- what: The server keeps a short history of world state and, when processing a client's time-stamped action, temporarily rewinds targets to where the acting client saw them at the moment of the action before adjudicating it.
- problem: With interpolation and latency, clients aim at where targets were in the past; without compensation players must lead their targets by their own ping, so the server re-executes actions against the past state each client actually perceived.
- named-in: Bernier, 'Latency Compensating Methods in Client/Server In-game Protocol Design and Optimization', GDC 2001 (Valve); Valve Developer Community, 'Lag Compensation'
- tags: games, networking

### methods-for-states — Methods for States
- aka: —
- kind: state-management
- what: Modal behavior is realized by swapping function/method references (or delegates) as the mode changes, so dispatch selects the current mode's behavior without conditionals.
- problem: Mode-dependent behavior via if/switch on a state code is error-prone and non-extensible; binding behavior directly to the current state removes the dispatch logic.
- named-in: Pattern-Oriented Software Architecture Vol. 4: A Pattern Language for Distributed Computing - Buschmann, Henney, Schmidt (2007)
- tags: fsm, embedded

### multiple-event-receptor — Multiple Event Receptor
- aka: multiple event receptor state machine
- kind: state-management
- what: A state machine implementation exposing one function per event type, each dispatching internally on the current state.
- problem: For synchronous machines, per-event functions give compile-time-checked interfaces and fast dispatch without event objects or queues.
- named-in: corpus:douglasspatternsc — Design Patterns for Embedded Systems in C - Bruce Powel Douglass (2011)
- tags: c, embedded

### optimistic-ui-update — Optimistic UI Update
- aka: optimistic updates
- kind: state-management
- what: Applies the expected result of a user action to local UI state immediately, before server confirmation, then reconciles with the authoritative response - rolling back if the operation fails.
- problem: Waiting a network round-trip for every mutation makes interfaces feel sluggish; predicting the result hides latency, at the cost of needing rollback/reconciliation logic for the failure case.
- named-in: Apollo Client documentation - Optimistic mutation results
- tags: ui, js, distributed

### orthogonal-component — Orthogonal Component
- aka: orthogonal component state pattern
- kind: state-management
- what: Independent concurrent behaviors are implemented as separate state-machine components contained by (and exchanging events with) a container machine, instead of as orthogonal regions of one chart.
- problem: Full orthogonal-region support is expensive in small frameworks; composing state-machine objects gives AND-state concurrency with plain aggregation.
- named-in: corpus:samekbook — Practical UML Statecharts in C/C++, 2nd ed. - Miro Samek (2008)
- tags: embedded, statecharts

### reactive-signals — Signals (fine-grained reactivity)
- aka: reactive signals, observable values with dependency tracking, computed/derivations, reactive primitives
- kind: state-management
- what: State cells that automatically track which computations read them and re-run exactly those computations (computeds/effects) when the cell changes, giving fine-grained dependency-graph updates without diffing.
- problem: Coarse re-render-and-diff wastes work and manual subscription management leaks or over-fires; automatic dependency tracking updates precisely the affected derived values and effects. TC39 has a standard proposal based on Solid, Vue, Angular, MobX et al.
- named-in: JavaScript Signals standard proposal - TC39 (proposal-signals)
- tags: ui, js

### reminder — Reminder
- aka: reminder event
- kind: state-management
- what: The state machine posts an event to itself to convert an internal condition into an explicit event that triggers further transitions.
- problem: Statecharts react only to events, but sometimes logically related transitions depend on conditions the machine itself computes; a self-posted reminder makes the dependency an event the topology can consume.
- named-in: corpus:samekbook — Practical UML Statecharts in C/C++, 2nd ed. - Miro Samek (2008)
- tags: embedded, statecharts

### rollback-netcode — Rollback Netcode
- aka: rollback networking, GGPO-style netcode, predict-and-rollback, speculative execution netcode
- kind: state-management
- what: Peers advance a deterministic simulation without waiting for remote inputs by predicting them; when actual remote inputs arrive and differ from the prediction, the engine restores a saved earlier state and re-simulates the intervening frames with the corrected inputs.
- problem: Plain lockstep stalls every frame on the slowest peer's latency; speculative execution keeps local inputs frame-perfect and hides network delay, trading it for state save/restore and cheap re-simulation of a few frames.
- named-in: Cannon, 'Fight the Lag! The Trick Behind GGPO's Low-Latency Netcode', Game Developer Magazine, Sept 2012 (republished as 'The lag-fighting techniques behind GGPO's netcode', gamedeveloper.com); ggpo.net
- tags: games, networking, determinism, borderline — Composes deterministic simulation with prediction, but kept separate from client-side-prediction: peer-to-peer full-simulation rewind/re-simulate with no authoritative server is a distinctly named, recurring mechanism (fighting games, GGPO, MK11, emulators).

### rules-engine — Rules Engine
- aka: production rule system, business rules engine, inference engine (forward-chaining), Rete-based rule engine (realization)
- kind: state-management
- what: A component that evaluates a collection of independent condition-action (production) rules against working state, with the engine — not imperative code order — deciding which rules fire, including chaining when one rule's action changes another rule's condition.
- problem: Domain logic consisting of many independent, frequently-changing decision rules becomes tangled when hard-coded as nested conditionals; representing it as declarative rules run by an evaluation loop keeps each rule separate and independently modifiable.
- named-in: Fowler, bliki 'RulesEngine' (7 Jan 2009; loaded live — 'you can build a simple rules engine yourself', production rules, Rete, chaining); production rule system literature (Forgy, Rete algorithm, 1982)
- tags: business-logic, declarative, borderline: also a commercial product category (BRMS) at system scale; included at the in-process altitude Fowler describes (rule objects + evaluation loop inside one application), sibling of behavior-tree/interpreter

### run-to-completion-event-processing — Run-to-Completion Event Processing
- aka: RTC step, run-to-completion semantics
- kind: state-management
- what: Each event is processed fully - all transitions, entry/exit actions - before the next event is dequeued, so the machine is never observed mid-transition.
- problem: Allowing a new event to interrupt in-progress transition processing creates unanalyzable interleavings; RTC serializes event handling per machine and underpins queue-based event-driven designs.
- named-in: corpus:samekbook — Practical UML Statecharts in C/C++, 2nd ed. - Miro Samek (2008)
- tags: embedded, statecharts, borderline — An execution-semantics rule of event-driven frameworks rather than a free-standing construct, but named, recurring, and implemented as a concrete queue/dispatch mechanism.

### single-event-receptor — Single Event Receptor
- aka: single event receptor state machine
- kind: state-management
- what: A state machine implementation exposing one event-receptor function that takes a parameterized event object and dispatches on current state and event type (synchronously or via a queue).
- problem: A uniform single entry point lets events be queued, forwarded, and processed asynchronously - the natural fit for message-driven embedded C designs.
- named-in: corpus:douglasspatternsc — Design Patterns for Embedded Systems in C - Bruce Powel Douglass (2011)
- tags: c, embedded

### state-transition-table — State Transition Table
- aka: State Table Pattern, table-driven state machine
- kind: state-management
- what: The state machine's transitions are encoded as a state x event table of handler/next-state entries, and a generic engine indexes the table to dispatch events.
- problem: Nested switch statements for large state machines are error-prone to modify; a table makes the machine data-driven, uniform in dispatch time, and auditable against the specification.
- named-in: corpus:douglasspatternsc — Design Patterns for Embedded Systems in C - Bruce Powel Douglass (2011)
- tags: c, embedded

### transition-to-history — Transition to History
- aka: history state, deep history, shallow history
- kind: state-management
- what: The most recently active substate of a composite state is recorded on exit so a later transition can return to where the machine left off rather than to the default initial substate.
- problem: Interruptions (errors, mode changes, power cycles) should not force a workflow to restart from scratch; history transitions resume the prior context.
- named-in: corpus:samekbook — Practical UML Statecharts in C/C++, 2nd ed. - Miro Samek (2008)
- tags: embedded, statecharts

### ultimate-hook — Ultimate Hook
- aka: —
- kind: state-management
- what: A composite (super)state provides default event handling that nested substates inherit and may selectively override, mirroring how a GUI framework's default window procedure works.
- problem: Common policies (help, shutdown, error handling) should apply everywhere without repeating transitions in every state; the outermost state becomes the hook of last resort.
- named-in: corpus:samekbook — Practical UML Statecharts in C/C++, 2nd ed. - Miro Samek (2008)
- tags: embedded, statecharts

### undo-redo-command-stack — Undo/Redo Command Stack
- aka: command history, undo stack, undo history
- kind: state-management
- what: Records executed operations as command objects (with state backups or inverse operations) on a history stack, so popping replays/reverts them to implement undo and redo.
- problem: Reversing arbitrary user operations requires either remembering prior state or an inverse for every action; reifying operations as stacked command objects makes multi-level undo/redo systematic.
- named-in: corpus:gof — Design Patterns - Gamma, Helm, Johnson, Vlissides (1994), Command: undo/redo via command history
- tags: ui, oo, borderline — Composition of GoF Command + Memento rather than a primitive; included because it is independently named (command history) and recurring - decision logged.


## Resource management — `resource-management` (56)

### allocation-wrapper — Allocation Wrapper
- aka: malloc wrapper, xmalloc (GNU checked-allocation convention)
- kind: resource-management
- what: Wrap the raw allocation/deallocation calls (malloc/free) in your own functions so every allocation flows through one place that can check for failure, add statistics, tagging, debugging hooks, or alternative backing allocators.
- problem: Scattered direct malloc calls duplicate out-of-memory handling and make it impossible to instrument, audit, or retarget allocation behavior centrally.
- named-in: corpus:preschern — Fluent C ch. 3, memory management patterns (Preschern 2022)
- tags: c

### asset-streaming — Asset Streaming
- aka: resource streaming, level streaming, world streaming, texture streaming (mip streaming)
- kind: resource-management
- what: The engine loads and unloads game assets (geometry, textures, audio, world chunks) asynchronously in the background, keyed to player position or predicted need, keeping only a sliding working set resident within a memory budget.
- problem: Open worlds exceed RAM and load screens break immersion; position-driven background load/unload bounds memory while presenting a seamless world.
- named-in: Gregory, Game Engine Architecture (resource management / streaming); Unreal Engine documentation, 'Level Streaming'
- tags: games, engine, borderline — Near paging, prefetching, and resource-files (all in index); kept per charter as the named game-engine form: spatially keyed, budgeted, asynchronous load/unload of a world working set.

### boundary-tags — Boundary Tags
- aka: boundary tag coalescing, header/footer block tags
- kind: resource-management
- what: Size/status fields at both ends of each heap block let an allocator find and merge free neighbors in constant time on free.
- problem: Coalescing adjacent free blocks is essential to fight fragmentation, but without boundary metadata a freeing block cannot locate its neighbors cheaply.
- named-in: corpus:dlmalloc — A Memory Allocator (dlmalloc essay) - Lea (2000); technique originally due to Knuth
- tags: c, systems

### buddy-memory-allocation — Buddy Memory Allocation
- aka: buddy system, binary buddy allocator
- kind: resource-management
- what: Manage memory in power-of-two-sized blocks that split into two 'buddies' on allocation and coalesce back with their buddy on free, found by address arithmetic.
- problem: General free-list allocators suffer slow coalescing and external fragmentation; restricting block sizes to powers of two makes split/merge O(1)-ish and bounds fragmentation predictably, at the price of internal fragmentation. Technique due to Knowlton (1965); named and analyzed by Knuth.
- named-in: The Art of Computer Programming, Vol. 1 - Donald E. Knuth (1968), sec. 2.5 'Dynamic Storage Allocation'
- tags: c, os-kernel, embedded, allocators

### bulkhead — Bulkhead
- aka: resource partitioning, bulkheading
- kind: resource-management
- what: Partition resources (thread pools, connection pools, memory) into isolated compartments per client or function so one compartment's exhaustion cannot sink the rest.
- problem: A shared pool lets one misbehaving consumer or one slow dependency exhaust capacity for everyone; partitioning contains the damage.
- named-in: corpus:nygard — Release It! Design and Deploy Production-Ready Software, 2nd ed. - Nygard (2018)
- tags: stability, resilience, borderline — Also applied at deployment/cluster level (architecture); the in-process pool-partitioning form is squarely design-level.

### callee-allocates — Callee Allocates
- aka: callee-allocated result, library-allocated buffer with free function
- kind: resource-management
- what: The callee allocates the result buffer (of size only it knows) and returns it with a paired deallocation function the caller must invoke.
- problem: When result size is unknown to the caller, callee allocation avoids guess-and-retry sizing at the cost of an explicit ownership-transfer contract.
- named-in: corpus:preschern — Fluent C - Christopher Preschern (2022)
- tags: c

### caller-owned-buffer — Caller-Owned Buffer
- aka: caller-allocates, user-supplied buffer
- kind: resource-management
- what: The caller allocates and owns the buffer, passing pointer and size for the callee to fill.
- problem: Callee-side allocation forces heap use and ambiguous ownership; caller-owned buffers keep allocation strategy (stack, static, pool) and lifetime with the caller - vital in embedded code.
- named-in: corpus:preschern — Fluent C - Christopher Preschern (2022)
- tags: c, embedded

### captain-oates — Captain Oates
- aka: memory sacrifice, cache shedding on pressure
- kind: resource-management
- what: On memory pressure, have less vital components voluntarily sacrifice their memory (caches, optional buffers) so more important tasks can proceed.
- problem: When memory runs out, failing the currently-allocating (possibly critical) task is the wrong victim choice; deliberately releasing low-value memory first preserves the vital functions.
- named-in: corpus:noblesmallmem — Small Memory Software: Patterns for Systems with Limited Memory - Noble & Weir (2000)
- tags: embedded, memory

### compaction — Compaction
- aka: memory compaction, defragmentation
- kind: resource-management
- what: Move live objects together in memory to squeeze out the unused gaps between them, recovering memory lost to fragmentation.
- problem: Long-running allocation and deallocation leaves free memory scattered in unusable fragments; relocating objects (usually via handles or indirection) coalesces free space into allocatable blocks.
- named-in: corpus:noblesmallmem — Small Memory Software: Patterns for Systems with Limited Memory - Noble & Weir (2000)
- tags: embedded, memory

### component-configurator — Component Configurator
- aka: Service Configurator
- kind: resource-management
- what: An application links and unlinks component implementations at runtime via a uniform component lifecycle interface (init, suspend, resume, fini) and a central configurator, without recompiling or restarting.
- problem: Which component implementations run, and when, should be decided late (deployment/runtime) and be changeable dynamically, decoupling implementation from configuration time.
- named-in: corpus:posa2 — Pattern-Oriented Software Architecture Vol. 2: Patterns for Concurrent and Networked Objects - Schmidt, Stal, Rohnert, Buschmann (2000)
- tags: dynamic-loading, lifecycle

### copy-on-write — Copy-on-Write
- aka: COW, lazy copy, COW string, thread-safe copy-on-write (variant), implicit sharing, copy-on-write pages
- kind: resource-management
- what: Share an object between clients until one needs to modify it, then transparently copy it and let the writer mutate the private copy.
- problem: Eager copying wastes memory and time when most copies are never modified; deferring the copy to first write keeps sharing cheap while preserving value semantics.
- named-in: corpus:noblesmallmem — Small Memory Software: Patterns for Systems with Limited Memory - Noble & Weir (2000)
- tags: embedded, memory, os, java, cpp, c++, os-kernel, databases, overlap:concurrency-scout

### custom-allocator — Custom Allocator
- aka: pluggable allocator, allocator parameter, allocator model
- kind: resource-management
- what: Containers and subsystems take an allocator object/parameter so memory sourcing policy is chosen by the client, not hard-coded.
- problem: One global heap cannot satisfy games/embedded constraints (budgets per subsystem, alignment, determinism); pluggable allocation decouples data structures from memory policy.
- named-in: corpus:eastl — EASTL - Electronic Arts Standard Template Library (WG21 N2271) - Pedriana (2007)
- tags: c++, games, embedded

### data-files — Data Files
- aka: streamed processing from secondary storage
- kind: resource-management
- what: Process data a little at a time from secondary storage, keeping only the current working portion in main memory.
- problem: Data sets that do not fit in RAM cannot be loaded whole; incremental streaming bounds the memory footprint regardless of data size.
- named-in: corpus:noblesmallmem — Small Memory Software: Patterns for Systems with Limited Memory - Noble & Weir (2000)
- tags: embedded, memory

### dedicated-ownership — Dedicated Ownership
- aka: single owner, explicit ownership convention, Caller-Owned Instance (Fluent C)
- kind: resource-management
- what: Every allocation is assigned exactly one owner responsible for freeing it, with ownership transfer made explicit at API boundaries.
- problem: Manual memory management fails through unclear responsibility (double free, leak); naming an owner per object makes deallocation auditable.
- named-in: corpus:preschern — Fluent C: Principles, Practices, and Patterns - Preschern (2022)
- tags: c

### dispose-pattern — Dispose Pattern
- aka: IDisposable pattern, try-with-resources (Java), using statement, Basic Dispose Pattern, context manager (Python with-statement)
- kind: resource-management
- what: Objects owning unmanaged resources expose an explicit Dispose/close method, invoked deterministically via language constructs (using / try-with-resources), with finalizers only as backstop.
- problem: Garbage collection reclaims memory but not files, sockets, or handles at predictable times; the pattern restores deterministic cleanup in GC languages.
- named-in: Framework Design Guidelines - Cwalina & Abrams (2005); Effective Java Item 9 (try-with-resources)
- tags: csharp, java, dotnet, python

### eager-acquisition — Eager Acquisition
- aka: —
- kind: resource-management
- what: Resources are acquired up front, before actual use (at startup or configuration time), and handed out from the pre-acquired set at run time.
- problem: Acquisition at use time is too slow or can fail unpredictably; paying the cost early makes run-time access fast and deterministic - central to real-time and embedded design.
- named-in: corpus:posa3 — Pattern-Oriented Software Architecture Vol. 3: Patterns for Resource Management - Kircher, Jain (2004)
- tags: real-time, embedded, determinism

### epoch-based-reclamation — Epoch-Based Reclamation
- aka: EBR, epoch GC
- kind: resource-management
- what: Threads announce a global epoch on entering read-side sections; retired nodes are freed only after all threads have advanced past the epoch in which the nodes were retired.
- problem: Amortizes the cost of safe memory reclamation for lock-free structures: per-access publication (as in hazard pointers) is replaced by cheap per-critical-section epoch bookkeeping.
- named-in: Practical Lock-Freedom (UCAM-CL-TR-579) - Keir Fraser (2004)
- tags: c, cpp, rust, systems

### evictor — Evictor
- aka: —
- kind: resource-management
- what: An evictor monitors resource usage and, under a configurable strategy (LRU, LFU, priorities), releases or swaps out the least valuable resources to bound consumption.
- problem: Long-running systems accumulate rarely used resources; systematic, policy-driven eviction prevents exhaustion while keeping hot resources available.
- named-in: corpus:posa3 — Pattern-Oriented Software Architecture Vol. 3: Patterns for Resource Management - Kircher, Jain (2004)
- tags: memory, caching

### execute-around-method — Execute Around Method
- aka: Execute-Around Object, Execute Around idiom, execute-around pointer (C++), loan pattern (Scala), with-style resource block
- kind: resource-management
- what: A method (or scoped object) performs guaranteed paired actions - acquire/release, open/close, begin/end - around a client-supplied block of code.
- problem: Clients forget or fail to perform the closing half of paired operations, especially on error paths; centralizing the pairing makes correct usage the only possible usage.
- named-in: Smalltalk Best Practice Patterns - Kent Beck (1997)
- tags: smalltalk, idiom, raii-alternative, c++, java, scala

### fixed-sized-buffer — Fixed Sized Buffer
- aka: fixed-size allocation
- kind: resource-management
- what: Allocate memory only in one (or a few) fixed sizes - sized for the worst case - so freed blocks are always exactly reusable.
- problem: Variable-size heap requests interleave into unusable fragments over time; uniform block sizes eliminate external fragmentation at the cost of internal waste.
- named-in: corpus:douglassrtcorpus — Real-Time Design Patterns - Bruce Powel Douglass (2002)
- tags: embedded, memory

### free-list — Free List
- aka: available list, freelist, list of available space, intrusive free list, segregated free lists, size-class bins
- kind: resource-management
- what: Linked list threaded through unused memory blocks or object slots themselves, from which an allocator pops on allocate and onto which it pushes on free.
- problem: Recycling fixed-size blocks in O(1) without heap traffic or fragmentation bookkeeping; the backbone of pool allocators, slab allocators, and embedded memory managers.
- named-in: corpus:wilsonsurvey — Dynamic Storage Allocation: A Survey and Critical Review - Wilson, Johnstone, Neely & Boles (1995)
- tags: c, embedded, allocators, games

### garbage-collection — Garbage Collection
- aka: automatic memory reclamation, garbage compactor, compacting collector, Tracing Garbage Collection, mark-sweep, mark-compact, copying collection
- kind: resource-management
- what: A runtime mechanism that finds no-longer-referenced allocations and reclaims (and, in compacting variants, relocates) them without explicit frees.
- problem: Manual deallocation causes leaks and dangling pointers; automated reclamation trades CPU time and determinism for memory safety. (Douglass catalogs both Garbage Collection and Garbage Compactor patterns; folded here as one mechanism with a compaction variant.)
- named-in: corpus:douglassrtcorpus — Real-Time Design Patterns - Bruce Powel Douglass (2002)
- tags: memory, runtime, runtimes, java, lisp, go

### gc-read-barrier — GC Read Barrier
- aka: read barrier, load barrier
- kind: resource-management
- what: A small check or fixup executed on every (or selected) pointer load so a concurrent or moving collector can intercept reads of stale or unforwarded references.
- problem: Concurrent and moving garbage collectors must keep the mutator from observing objects mid-move or mid-mark; intercepting reads lets the collector repair or redirect references lazily.
- named-in: The Garbage Collection Handbook — Jones, Hosking, Moss (2011)
- tags: runtime, gc

### gc-write-barrier — GC Write Barrier
- aka: write barrier, card table (folded implementation variant), card marking, remembered-set maintenance (role), snapshot-at-the-beginning barrier (variant), incremental-update barrier (variant), Yuasa barrier / Dijkstra barrier / Steele barrier (variants)
- kind: resource-management
- what: A small code sequence the compiler or runtime inserts on every pointer store that records or checks the mutated reference (e.g. by marking a card in a card table or appending to a remembered set), so the collector can find cross-generation or concurrently-mutated pointers without rescanning the whole heap.
- problem: Generational and incremental/concurrent collectors must know which old-generation or already-scanned objects now point into the young generation or unscanned space; intercepting mutator writes is the only way to track this without full-heap scans.
- named-in: Jones, Hosking & Moss, 'The Garbage Collection Handbook: The Art of Automatic Memory Management' (2011), sect. 11.8 'Write barrier mechanisms' incl. 'Card tables' (verified live via O'Reilly index/ToC this session)
- tags: virtual machines, language runtimes, garbage collection, memory management

### hazard-pointers — Hazard Pointers
- aka: SMR via hazard pointers
- kind: resource-management
- what: Each thread publishes single-writer pointers naming the nodes it is currently accessing; reclaimers defer freeing any node named in a hazard pointer.
- problem: Safe memory reclamation for lock-free data structures: a node removed from the structure may still be dereferenced by a concurrent reader, so freeing must wait until no reader can hold it.
- named-in: Hazard Pointers: Safe Memory Reclamation for Lock-Free Objects - Maged M. Michael (2004)
- tags: c, cpp, systems

### hooks — Hooks
- aka: indirection over ROM, patch table
- kind: resource-management
- what: Access read-only information through hooks (pointers or jump slots) held in writable storage, so changing the hooks gives the illusion of changing ROM content.
- problem: Information baked into ROM cannot be updated in the field; a small writable indirection layer allows patching and extension without rewriting read-only storage.
- named-in: corpus:noblesmallmem — Small Memory Software: Patterns for Systems with Limited Memory - Noble & Weir (2000)
- tags: embedded, memory

### lazy-cleanup — Lazy Cleanup
- aka: no explicit deallocation, let the OS reclaim at exit
- kind: resource-management
- what: Deliberately never free dynamically allocated memory whose lifetime spans the whole program run, relying on the operating system to reclaim it at process exit.
- problem: Explicit deallocation of long-lived allocations adds code, ownership bookkeeping, and dangling-pointer risk for memory the process needs until it dies anyway; skipping the free removes that entire error class at the cost of unbounded-lifetime allocations.
- named-in: corpus:preschern — Fluent C ch. 3, memory management patterns (Preschern 2022)
- tags: c, borderline — distinct from Eternal Memory / static allocation (already in index under static-allocation): here memory IS dynamically allocated, only the cleanup is skipped

### leasing — Leasing
- aka: Lease, time-bounded lock, expiring grant
- kind: resource-management
- what: A resource is granted for a limited time; the holder must renew the lease to keep it, and expiry releases the resource automatically.
- problem: Resource holders that crash or forget to release cause leaks in loosely coupled systems; time-bounded grants make reclamation the default rather than the exception.
- named-in: corpus:posa3 — Pattern-Oriented Software Architecture Vol. 3: Patterns for Resource Management - Kircher, Jain (2004)
- tags: timeouts, robustness, distributed, caching

### list-virtualization — List Virtualization
- aka: UI virtualization, virtual scrolling, view recycling
- kind: resource-management
- what: Renders only the subset of a long scrollable list that is visible in the viewport (plus a small buffer), creating, recycling, and repositioning a fixed pool of item views as the user scrolls.
- problem: Instantiating a widget per item makes large lists consume unbounded memory and layout time; virtualizing bounds live widget count to the viewport size. Named across stacks: WPF UI virtualization, Android RecyclerView view recycling, react-window windowing, CDK virtual scrolling.
- named-in: Optimizing Performance: Controls (UI Virtualization) - WPF documentation - Microsoft
- tags: ui, js

### lookup — Lookup
- aka: —
- kind: resource-management
- what: Resource providers register references with a lookup service under known names or properties; users query the service to find and access the resources.
- problem: Resource users should not hard-code the identity or location of providers; a mediating registry decouples acquisition from provider placement and lifetime.
- named-in: corpus:posa3 — Pattern-Oriented Software Architecture Vol. 3: Patterns for Resource Management - Kircher, Jain (2004)
- tags: registry, borderline — Often distribution-flavored (naming services), but equally an in-process service registry; POSA3 documents it as a resource-acquisition design pattern.

### memory-arena — Memory Arena
- aka: arena allocator, region-based memory management, region allocator, bump allocator, linear allocator, frame allocator, obstack
- kind: resource-management
- what: Allocate objects by bumping a pointer through a large block and free them all at once by resetting or discarding the whole arena.
- problem: Per-object malloc/free is slow and error-prone when many objects share one lifetime (a request, a frame, a compilation pass); grouping them into one region makes allocation a pointer increment and deallocation a single bulk release. Canonical name decided as 'memory arena' (mission anchor; Hanson's Arena interface); region/bump/linear/frame allocator folded as aka.
- named-in: corpus:hanson — C Interfaces and Implementations - David R. Hanson (1996), ch. 'Arenas'
- tags: c, games, embedded, compilers, allocators

### memory-discard — Memory Discard
- aka: region allocation, arena discard, scratch workspace
- kind: resource-management
- what: Allocate temporary objects from a temporary workspace and reclaim them all at once by discarding the whole workspace.
- problem: Freeing many short-lived temporaries individually is slow and error-prone; discarding an entire scratch region on completion reclaims everything in one cheap operation.
- named-in: corpus:noblesmallmem — Small Memory Software: Patterns for Systems with Limited Memory - Noble & Weir (2000)
- tags: embedded, memory

### memory-limit — Memory Limit
- aka: memory budget, per-component quota
- kind: resource-management
- what: Set an explicit memory budget for each component and fail allocations that would exceed the component's limit.
- problem: Competing components can starve each other of memory unpredictably; enforced per-component limits contain failures and make memory use plannable.
- named-in: corpus:noblesmallmem — Small Memory Software: Patterns for Systems with Limited Memory - Noble & Weir (2000)
- tags: embedded, memory, borderline — Closer to a budgeting policy than a code mechanism, but pattern-cataloged and implemented via allocator quota checks - kept IN.

### memory-overlay — Memory Overlay
- aka: overlays, code overlaying, overlay manager, code overlay, overlay description
- kind: resource-management
- what: Divide a program into sections that share the same memory region, loading each overlay from secondary storage into the shared region only when its code/data is needed.
- problem: The program is larger than the memory it must run in; time-multiplexing one region among mutually exclusive sections fits large programs into small RAM, predating and paralleling virtual memory.
- named-in: corpus:levine — Linkers and Loaders - Levine (1999)
- tags: embedded, memory, c, borderline — Realized through linker machinery (ops territory), but choosing an overlay scheme is a genuine program-level memory-design decision.

### object-manager — Object Manager
- aka: —
- kind: resource-management
- what: A manager component separate from both clients and managed objects controls the objects' creation, access, and destruction, issuing references while owning the lifecycle.
- problem: When object lifetime is governed by application-wide concerns rather than any single client, per-client ownership fails; a dedicated manager centralizes lifecycle policy.
- named-in: Explicit Interface and Object Manager: Two Patterns from a Pattern Language for Distributed Computing - Buschmann, Henney, Schmidt (EuroPLoP 2003)
- tags: lifecycle

### paging — Paging
- aka: data paging, demand paging (application-level)
- kind: resource-management
- what: Keep code and data on secondary storage and move fixed-size pages in and out of main memory on demand, giving the illusion of more memory.
- problem: The working set exceeds physical RAM; paging trades access latency for effectively unbounded addressable data (the OS virtual-memory realization is the system-level cousin).
- named-in: corpus:noblesmallmem — Small Memory Software: Patterns for Systems with Limited Memory - Noble & Weir (2000)
- tags: embedded, memory, os

### partial-acquisition — Partial Acquisition
- aka: —
- kind: resource-management
- what: A large resource is acquired in stages - only the part needed now, with further parts acquired progressively (e.g. lazy-loading pages of an image or file).
- problem: A resource may be too large or costly to acquire whole, yet partially usable; staged acquisition balances memory, latency, and availability.
- named-in: corpus:posa3 — Pattern-Oriented Software Architecture Vol. 3: Patterns for Resource Management - Kircher, Jain (2004)
- tags: streaming, memory

### pool-allocation — Pool Allocation
- aka: memory pool, fixed-block allocator, block pool, Pooled Allocation, pool allocator, fixed-size-block allocation, partition allocator, memory slab (Zephyr k_mem_slab)
- kind: resource-management
- what: Pre-allocated pools of fixed-size blocks (often one pool per object type/size) from which objects are checked out and returned in O(1).
- problem: General-purpose heap allocation fragments memory and has variable timing; pools give deterministic allocation with bounded memory per type.
- named-in: corpus:douglassrtcorpus — Real-Time Design Patterns - Bruce Powel Douglass (2002)
- tags: embedded, real-time, memory, c

### pooling — Pooling
- aka: Resource Pool, Object Pool, Connection Pool, pool
- kind: resource-management
- what: Released resources are recycled into a pool and handed out again on demand, amortizing acquisition/release cost across many uses; the pool manages size and eviction.
- problem: Frequent creation and destruction of expensive, identity-free resources (threads, connections, buffers, objects) wastes time and fragments memory.
- named-in: corpus:posa3 — Pattern-Oriented Software Architecture Vol. 3: Patterns for Resource Management - Kircher, Jain (2004)
- tags: performance, embedded, memory, games, resource

### raii-resource-acquisition-is-initialization — RAII (Resource Acquisition Is Initialization)
- aka: scope-bound resource management, RAII guard (Rust), constructor acquires, destructor releases (CADRe), RAII, Resource Acquisition Is Initialization
- kind: resource-management
- what: Tie a resource's lifetime to an object's lifetime so acquisition happens in the constructor and release happens deterministically in the destructor at scope exit.
- problem: Manual release paths leak resources on early returns and exceptions; RAII makes cleanup automatic and exception-safe.
- named-in: The Design and Evolution of C++ - Stroustrup (1994)
- tags: c++, rust, embedded

### read-only-memory — Read-Only Memory
- aka: ROMable data, const-in-ROM
- kind: resource-management
- what: Place read-only code and constant data in ROM/flash rather than RAM, reserving scarce writable memory for mutable state.
- problem: RAM is the scarcest memory on small systems while ROM/flash is comparatively plentiful; segregating immutable content into read-only memory frees RAM.
- named-in: corpus:noblesmallmem — Small Memory Software: Patterns for Systems with Limited Memory - Noble & Weir (2000)
- tags: embedded, memory

### reference-counting — Reference Counting
- aka: Counted Body, Counted Pointer, Counting Handle, Reference Counting idiom, automatic reference counting (ARC), counted body, intrusive reference counting, refcounting, reference-counted handle/body, shared_ptr semantics
- kind: resource-management
- what: A handle class embeds a reference counter in (or beside) a dynamically allocated body object, updating it on copy/assignment/destruction and deleting the body when the count reaches zero.
- problem: Shared dynamically allocated objects in C++ need deterministic deallocation without ownership ambiguity, dangling pointers, or leaks.
- named-in: A Method for Overlapping and Erasure of Lists - George E. Collins (1960)
- tags: c++, idiom, memory, c, cpp, systems, objc, swift, python, os-kernel

### resource-files — Resource Files
- aka: resource bundle, on-demand configuration loading
- kind: resource-management
- what: Keep configuration data and read-only resources in files on secondary storage, loading and discarding each item as needed.
- problem: Keeping all configuration and UI resources resident wastes RAM and hard-codes content; externalized, demand-loaded resources cut memory use and ease localization/updates.
- named-in: corpus:noblesmallmem — Small Memory Software: Patterns for Systems with Limited Memory - Noble & Weir (2000)
- tags: embedded, memory

### resource-lifecycle-manager — Resource Lifecycle Manager
- aka: RLM
- kind: resource-management
- what: A dedicated manager component centrally controls the whole lifecycle of a class of resources - acquisition, coordination, optimization, and release - decoupling lifecycle from resource use.
- problem: When many users share many resources, per-user lifecycle handling causes leaks and conflicting policies; centralizing lifecycle management enables global optimization.
- named-in: corpus:posa3 — Pattern-Oriented Software Architecture Vol. 3: Patterns for Resource Management - Kircher, Jain (2004)
- tags: lifecycle

### rule-of-three-five-zero — Rule of Three/Five/Zero
- aka: rule of three, rule of five, rule of zero, rule of the big four (and a half)
- kind: resource-management
- what: If a class defines any of destructor/copy/move special members it should deliberately define the whole set (three/five) - or own no resources directly and define none (zero).
- problem: Compiler-generated special members silently mismanage owned resources (double frees, slicing of ownership semantics); the rule makes ownership responsibilities explicit.
- named-in: corpus:coreguidelines — C++ Core Guidelines (C.20/C.21) - Stroustrup & Sutter (living)
- tags: c++, borderline — A coding guideline about special members rather than a standalone mechanism; kept because it is the named contract governing RAII-style ownership.

### scope-guard — Scope Guard
- aka: ScopeGuard, defer (Go/Zig analog), gsl::finally
- kind: resource-management
- what: An ad-hoc RAII object that runs an arbitrary cleanup or rollback action when a scope exits, optionally dismissible on success.
- problem: One-off cleanup/rollback obligations (not tied to a reusable resource class) must still run on every exit path including exceptions.
- named-in: Generic<Programming>: Change the Way You Write Exception-Safe Code - Forever - Andrei Alexandrescu & Petru Marginean, Dr. Dobb's/CUJ (2000)
- tags: c++

### sharing — Sharing
- aka: shared instances, interning, String Interning, atom table, symbol interning
- kind: resource-management
- what: Store one copy of identical information and reference it from everywhere it is needed instead of duplicating it.
- problem: Multiple copies of the same data multiply memory cost; sharing a single instance removes the duplication at the price of managing shared ownership and mutation (closely related to GoF Flyweight).
- named-in: corpus:noblesmallmem — Small Memory Software: Patterns for Systems with Limited Memory - Noble & Weir (2000)
- tags: embedded, memory, interpreters, compilers

### slab-allocator — Slab Allocator
- aka: object-caching allocator, slab cache
- kind: resource-management
- what: Carve memory into per-type slabs of preconstructed, fixed-size objects and cache freed objects in initialized state for immediate reuse.
- problem: Frequently allocated kernel objects pay repeated construction/destruction and fragmentation costs under a general allocator; caching constructed objects per type removes both and improves locality. Slab coloring and the later magazine/vmem layer (Bonwick & Adams 2001) are folded here as variants.
- named-in: The Slab Allocator: An Object-Caching Kernel Memory Allocator - Jeff Bonwick (1994)
- tags: c, os-kernel, allocators

### small-buffer-optimization — Small Buffer Optimization
- aka: small object optimization (SOO), small string optimization (SSO), inline storage, SBO, small string optimization, small object optimization
- kind: resource-management
- what: A container or wrapper embeds a small fixed-size buffer inside itself and only falls back to heap allocation when contents exceed it.
- problem: Heap allocation dominates cost for typically-small payloads (short strings, small callables); inline storage removes the allocation and improves locality.
- named-in: corpus:iglberger — C++ Software Design - Iglberger (2022)
- tags: c++, embedded

### smart-pointer — Smart Pointer
- aka: —
- kind: resource-management
- what: A pointer-like object that wraps a raw pointer, validity-checks access, and manages the pointee's lifetime (typically by reference counting), releasing it when the last reference disappears.
- problem: Raw pointers invite dangling access, double free, and leaks; wrapping pointer mechanics in an object enforces the ownership rules mechanically.
- named-in: corpus:douglassrtcorpus — Real-Time Design Patterns - Bruce Powel Douglass (2002)
- tags: c, c++, memory

### stack-first — Stack First
- aka: prefer automatic storage
- kind: resource-management
- what: Default data placement on the call stack (automatic storage), reaching for static or heap storage only when lifetime or size demands it.
- problem: Heap allocation on constrained systems risks fragmentation, leaks, and nondeterminism; stack allocation is self-releasing and timing-safe.
- named-in: corpus:preschern — Fluent C: Principles, Practices, and Patterns - Preschern (2022)
- tags: c, embedded

### static-allocation — Static Allocation
- aka: compile-time allocation, no-heap allocation, Fixed Allocation, pre-allocation, Eternal Memory, whole-lifetime allocation
- kind: resource-management
- what: All objects and buffers are allocated at compile/link time or once at startup, and the heap is never used afterwards.
- problem: Dynamic allocation brings fragmentation, nondeterministic timing, and out-of-memory failures that safety-critical and long-running embedded systems cannot tolerate.
- named-in: corpus:douglassrtcorpus — Real-Time Design Patterns - Bruce Powel Douglass (2002)
- tags: embedded, real-time, memory, c, safety-critical

### steady-state — Steady State
- aka: resource recycling, log rotation discipline
- kind: resource-management
- what: For every mechanism that accumulates a resource (log files, cache entries, rows, temp files), pair a mechanism that recycles or purges it, so the program can run indefinitely without human cleanup.
- problem: Unbounded accumulation (logs filling disks, caches growing without eviction) eventually kills long-running systems and forces routine human intervention.
- named-in: corpus:nygard — Release It! Design and Deploy Production-Ready Software, 2nd ed. - Nygard (2018)
- tags: stability, borderline — Close to an operability principle, but kept: it prescribes concrete in-program purge/rotation/eviction mechanisms.

### two-level-segregated-fit-allocator-tlsf — Two-Level Segregated Fit Allocator (TLSF)
- aka: TLSF
- kind: resource-management
- what: A dynamic allocator using a two-level bitmap-indexed segregated-fit structure giving O(1) worst-case malloc and free.
- problem: Real-time systems need dynamic allocation with a hard constant-time bound and low fragmentation, which classic best-fit/first-fit heaps cannot guarantee.
- named-in: corpus:tlsf — TLSF: a New Dynamic Memory Allocator for Real-Time Systems - Masmano, Ripoll, Crespo, Real (ECRTS 2004)
- tags: c, embedded, real-time

### variable-allocation — Variable Allocation
- aka: dynamic allocation
- kind: resource-management
- what: Allocate and deallocate variable-sized objects on demand from a heap as the program needs them.
- problem: Fixed pre-allocation wastes memory on empty reserved space; allocating only what is needed, when needed, avoids unused headroom at the cost of allocation failure handling and fragmentation.
- named-in: corpus:noblesmallmem — Small Memory Software: Patterns for Systems with Limited Memory - Noble & Weir (2000)
- tags: embedded, memory

### weak-reference — Weak Reference
- aka: weak pointer, weak_ptr, WeakReference
- kind: resource-management
- what: A reference that does not keep its target alive: it can be dereferenced only while the target still exists and observably lapses when the target is reclaimed.
- problem: Reference-counted or traced object graphs with back-pointers, caches, or observer lists otherwise leak via cycles or unwanted retention; a non-owning, lapse-aware reference breaks the cycle while remaining safe to use. Kept as a separate element from reference counting per decision log (distinct mechanism, also exists in tracing-GC runtimes).
- named-in: The Garbage Collection Handbook - Jones, Hosking & Moss (2011)
- tags: cpp, java, python, swift


## Caching & memoization — `caching-memoization` (16)

### buffer-pool — Buffer Pool
- aka: page cache, buffer manager, buffer cache
- kind: caching-memoization
- what: A fixed set of in-memory frames that caches disk pages, tracks pin counts and dirty state, and mediates all page reads and writes between the storage layer and disk.
- problem: Disk access is orders of magnitude slower than memory; a managed page cache exploits locality while controlling exactly when dirty pages reach disk, which the recovery protocol depends on (steal/force policies).
- named-in: Architecture of a Database System - Hellerstein, Stonebraker & Hamilton (2007)
- tags: db, storage-engine, os

### cache-aside — Cache-Aside
- aka: lazy loading, look-aside cache, lazy caching
- kind: caching-memoization
- what: Application code checks the cache first, loads from the backing store on a miss, populates the cache itself, and invalidates or updates the entry when it writes the store.
- problem: Keeps the cache optional and the store authoritative when the cache cannot sit transparently in the data path; the application accepts responsibility for population and invalidation consistency.
- named-in: Cloud Design Patterns - Microsoft patterns & practices (2014)
- tags: db, caching, web, databases

### cache-eviction-policy — Cache Eviction Policy
- aka: cache replacement policy, page replacement policy, LRU, LFU, CLOCK, FIFO eviction, 2Q, LRU-K, ARC
- kind: caching-memoization
- what: The rule a bounded cache uses to choose which resident entry to discard when admitting a new one, approximating 'least likely to be needed again' (recency-, frequency-, or clock-based).
- problem: A cache smaller than its working set must evict; the choice of victim policy determines hit rate and scan-resistance and is a named, pluggable design decision in every cache and buffer pool.
- named-in: Database Internals - Petrov (2019)
- tags: db, caching, os

### cache-stampede-protection — Cache Stampede Protection
- aka: dog-pile prevention, dogpile effect mitigation, cache stampede prevention, request coalescing, singleflight (Go), duplicate call suppression, probabilistic early expiration / XFetch (variant), thundering herd mitigation (cache-miss form)
- kind: caching-memoization
- what: Mechanisms ensuring that when a popular cache entry expires, only one computation regenerates it - concurrent requesters are coalesced onto the in-flight computation (singleflight/lock) or expirations are jittered via probabilistic early recomputation.
- problem: When a hot entry expires, every concurrent miss triggers the same expensive recomputation simultaneously, overloading the backing store exactly when it is most needed; deduplicating or pre-staggering the regeneration removes the spike.
- named-in: Vattani, Chierichetti, Lowenstein, 'Optimal Probabilistic Cache Stampede Prevention', PVLDB 8(8), 2015; request-coalescing realization named in Go's golang.org/x/sync/singleflight
- tags: distributed-adjacent, web, databases

### caching — Caching
- aka: Resource Cache, Cache
- kind: caching-memoization
- what: Released or fetched resources are kept in fast intermediate storage so re-acquisition is served from the cache instead of the expensive source, under an invalidation/consistency policy.
- problem: Repeatedly re-acquiring identical resources dominates cost; trading memory for re-use requires managing staleness, eviction, and consistency.
- named-in: corpus:posa3 — Pattern-Oriented Software Architecture Vol. 3: Patterns for Resource Management - Kircher, Jain (2004)
- tags: performance

### identity-map — Identity Map
- aka: —
- kind: caching-memoization
- what: Keeps every object loaded from the database in a map keyed by identity so each record is materialized as exactly one in-memory object.
- problem: Loading the same row twice yields two objects whose updates conflict and whose comparisons lie; a per-session lookup table guarantees one object per identity and doubles as a read cache.
- named-in: Patterns of Enterprise Application Architecture - Martin Fowler (2002)
- tags: enterprise, orm

### inline-caching — Inline Caching
- aka: monomorphic inline cache, polymorphic inline cache, PIC, megamorphic cache (degenerate case)
- kind: caching-memoization
- what: Caches the result of dynamic method/property lookup at each individual call site (classically by patching the call instruction itself), so repeated dispatch at that site becomes a type-guard check plus a direct jump.
- problem: Dynamic dispatch and dynamic-language attribute lookup are expensive, but call sites are overwhelmingly type-stable in practice; per-site caching exploits that stability.
- named-in: Deutsch & Schiffman, 'Efficient Implementation of the Smalltalk-80 System' (POPL 1984); Hölzle, Chambers & Ungar, 'Optimizing Dynamically-Typed Object-Oriented Languages With Polymorphic Inline Caches' (ECOOP 1991)
- tags: interpreters, virtual machines, language runtimes

### lookup-table — Lookup Table
- aka: LUT, precomputed table, interpolated lookup table (variant)
- kind: caching-memoization
- what: Replace runtime computation with indexing into a precomputed table of results, optionally interpolating between entries for continuous functions.
- problem: Transcendental math, calibration curves, and CRC steps are too slow (or need an FPU) on small CPUs; trading ROM for computation gives constant-time, deterministic evaluation.
- named-in: Lookup table - Wikipedia
- tags: embedded, performance

### lru-cache — LRU Cache
- aka: least-recently-used cache
- kind: caching-memoization
- what: Bounded map coupling a hash table with a recency-ordered doubly linked list so lookup, insert, and evict-least-recently-used are all O(1).
- problem: Fixed-size caches must pick a victim on overflow; recency ordering approximates future usefulness cheaply, and the hash-plus-list composition makes the policy constant-time.
- named-in: Evaluation Techniques for Storage Hierarchies - Mattson, Gecsei, Slutz, Traiger (1970)
- tags: caching, os, databases

### memoization — Memoization
- aka: memo function, tabling, function result caching
- kind: caching-memoization
- what: Caching a function's results keyed by its arguments so repeated calls with the same inputs return the stored answer instead of recomputing.
- problem: Trades memory for time on pure or effectively-pure functions with overlapping call patterns (recursive decomposition, repeated queries), often turning exponential recursions polynomial.
- named-in: 'Memo' Functions and Machine Learning - Donald Michie (Nature, 1968)
- tags: fp, functional

### negative-caching — Negative Caching
- aka: negative cache, negative result caching, caching of misses/failures, negative TTL, DNS NCACHE, nonexistence caching
- kind: caching-memoization
- what: Caching the fact that a lookup failed (name does not exist, entry not found, call errored) with its own, usually shorter, TTL so repeated misses are answered from cache.
- problem: Repeated lookups for nonexistent keys bypass a positive-only cache and hammer the backing store; remembering not-found/error outcomes absorbs that load, while a bounded negative TTL limits the staleness window when the item comes into existence.
- named-in: RFC 2308, 'Negative Caching of DNS Queries (DNS NCACHE)' (M. Andrews, 1998); general form in OS name caches (Linux dentry negative entries)
- tags: networking, databases, os

### prefetching — Prefetching
- aka: readahead, read-ahead, anticipatory fetching, sequential prefetch
- kind: caching-memoization
- what: Fetch data into a cache or buffer before it is requested, based on a predicted access pattern (most commonly sequential readahead), overlapping fetch latency with useful work.
- problem: Demand fetching stalls the consumer for the full miss latency; when the access pattern is predictable, speculatively issuing fetches early hides that latency at the risk of wasted bandwidth on wrong guesses.
- named-in: Computer Architecture: A Quantitative Approach - Hennessy & Patterson (1990)
- tags: db, os, caching, cpu-caches

### read-through-cache — Read-Through Cache
- aka: read-through caching
- kind: caching-memoization
- what: The cache itself, not the application, loads missing entries from the backing store via a pluggable loader when a get misses, then returns and retains the value.
- problem: Centralizes miss-handling so callers see one always-answering interface, and lets the cache coalesce concurrent misses for the same key (thundering-herd protection).
- named-in: Read-Through, Write-Through, Write-Behind, and Refresh-Ahead Caching - Oracle Coherence Developer's Guide (2009)
- tags: db, caching

### refresh-ahead-cache — Refresh-Ahead Cache
- aka: refresh-ahead caching, proactive refresh
- kind: caching-memoization
- what: When a cached entry is read close to its expiry, the cache returns the current value and asynchronously reloads a fresh one from the backing store before it expires.
- problem: Plain TTL expiry makes some unlucky reader pay the reload latency on hot keys; refreshing ahead of expiry hides reload cost for frequently accessed entries.
- named-in: Read-Through, Write-Through, Write-Behind, and Refresh-Ahead Caching - Oracle Coherence Developer's Guide (2009)
- tags: db, caching

### write-behind-cache — Write-Behind Cache
- aka: write-back cache, deferred write, write-behind caching
- kind: caching-memoization
- what: Writes are acknowledged once they hit the cache and are propagated to the backing store asynchronously, often batched and coalesced, after a delay.
- problem: Synchronous store writes cap write latency and throughput; deferring and batching them absorbs bursts and coalesces repeated writes, at the risk of losing acknowledged-but-unflushed data.
- named-in: Read-Through, Write-Through, Write-Behind, and Refresh-Ahead Caching - Oracle Coherence Developer's Guide (2009)
- tags: db, caching, cpu-caches

### write-through-cache — Write-Through Cache
- aka: write-through caching
- kind: caching-memoization
- what: Writes go to the cache, which synchronously propagates them to the backing store before acknowledging, keeping cache and store consistent at all times.
- problem: Guarantees the store never lags the cache (no dirty data to lose) at the cost of paying full store latency on every write; the safety end of the write-policy spectrum.
- named-in: Read-Through, Write-Through, Write-Behind, and Refresh-Ahead Caching - Oracle Coherence Developer's Guide (2009)
- tags: db, caching, cpu-caches


## Error handling — `error-handling` (50)

### brown-out-handling — Brown-Out Handling
- aka: brown-out detection, BOD, brown-out reset (BOR), low-voltage detect
- kind: error-handling
- what: Detect supply voltage sagging below a safe threshold (via an on-chip or external detector) and hold the MCU in reset or run a controlled shutdown until power is reliable.
- problem: During sags the CPU and flash misbehave unpredictably (corrupted writes, erratic execution) without a clean power-off; explicit brown-out detection converts an undefined-behavior region into a defined reset or safe-save path.
- named-in: AVR180: External Brown-out Protection - Atmel/Microchip application note
- tags: embedded, power, robustness

### built-in-self-test — Built-In Self-Test
- aka: BIST, power-on self-test (POST), startup self-test, periodic self-test
- kind: error-handling
- what: Firmware routines that exercise and verify the system's own hardware (RAM patterns, ROM checksums, register/ALU checks, peripheral loopbacks) at startup or periodically.
- problem: Latent hardware faults otherwise surface only as mysterious runtime failures; explicit self-tests detect them at a moment the system can still report, refuse to run, or fail safe. RAM march tests and ROM CRC checks are folded here as variants.
- named-in: Built-in self-test - Wikipedia
- tags: embedded, safety-critical, robustness

### circuit-breaker — Circuit Breaker
- aka: —
- kind: error-handling
- what: A stateful wrapper around a failure-prone operation that trips open after a failure threshold, rejects calls while open, and probes recovery via a half-open state.
- problem: Repeatedly calling a failing dependency wastes resources, slows callers, and hammers the struggling system; the breaker fails fast and gives the dependency time to recover.
- named-in: corpus:nygard — Release It! Design and Deploy Production-Ready Software, 2nd ed. - Nygard (2018)
- tags: stability, distributed, resilience

### cleanup-record — Cleanup Record
- aka: acquisition tracking record
- kind: error-handling
- what: A variable records which acquisition steps succeeded so a single cleanup path can conditionally release exactly what was obtained.
- problem: Multi-resource initialization in C must undo partial progress on failure without duplicating release logic per exit point.
- named-in: corpus:preschern — Fluent C: Principles, Practices, and Patterns - Preschern (2022)
- tags: c

### complete-parameter-checking — Complete Parameter Checking
- aka: defensive interface validation
- kind: error-handling
- what: Validate all parameters and inputs at component boundaries every time, detecting errors close to their source at the cost of some performance.
- problem: Faults manifest as bad values crossing interfaces; checking at the boundary shortens fault latency and stops propagation into the component.
- named-in: corpus:hanmer — Patterns for Fault Tolerant Software - Hanmer (2007)
- tags: fault-detection

### copy-and-swap — Copy-and-Swap
- aka: create-a-temporary-and-swap
- kind: error-handling
- what: Implement assignment by constructing a copy and swapping its guts with *this via a non-throwing swap, so the operation either fully succeeds or leaves the object untouched.
- problem: Hand-written assignment operators struggle with self-assignment and partial-failure states; copy-and-swap gives the strong exception guarantee for free.
- named-in: Exceptional C++ - Herb Sutter (1999)
- tags: c++

### core-dump — Core Dump
- aka: crash dump, coredump capture, minidump, postmortem dump, fault dump, crash log with register/stack snapshot
- kind: error-handling
- what: On a fatal fault, a handler serializes the program's execution state (registers, stack, selected memory regions, fault status) to persistent storage or a host channel for postmortem analysis.
- problem: Crashes in the field or in hard-to-reproduce conditions leave no debugger attached; capturing machine state at the moment of failure lets developers diagnose the fault after the fact instead of losing it to a silent reset.
- named-in: white
- tags: e, m, b, e, d, d, e, d, ,,  , d, e, b, u, g, g, i, n, g, ,,  , b, o, r, d, e, r, l, i, n, e,  , —,  , d, i, a, g, n, o, s, t, i, c, s, /, t, o, o, l, i, n, g, -, a, d, j, a, c, e, n, t,  , m, e, c, h, a, n, i, s, m,  , (, h, o, s, t, e, d,  , O, S, e, s,  , p, r, o, v, i, d, e,  , i, t,  , a, s,  , a,  , f, a, c, i, l, i, t, y, ), ,,  , i, n, c, l, u, d, e, d,  , b, e, c, a, u, s, e,  , e, m, b, e, d, d, e, d,  , s, y, s, t, e, m, s,  , d, e, s, i, g, n,  , i, t,  , i, n,  , e, x, p, l, i, c, i, t, l, y,  , a, s,  , a,  , h, a, r, d, -, f, a, u, l, t, -, h, a, n, d, l, e, r,  , m, e, c, h, a, n, i, s, m, ,,  , s, a, m, e,  , a, l, t, i, t, u, d, e,  , a, s,  , t, h, e,  , c, a, t, a, l, o, g, e, d,  , s, t, a, c, k, -, p, a, i, n, t, i, n, g, -, w, a, t, e, r, m, a, r, k, i, n, g

### correcting-audits — Correcting Audits
- aka: data audits, audit programs
- kind: error-handling
- what: Routinely scan in-memory or stored data for structural and semantic errors and repair them (rebuild links, reset invalid fields) as they are found.
- problem: Data errors accumulate silently from faults elsewhere and eventually trigger failures; active auditing finds and corrects them before they are used.
- named-in: corpus:hanmer — Patterns for Fault Tolerant Software - Hanmer (2007)
- tags: fault-tolerance, telecom

### cyclic-redundancy-check — Cyclic Redundancy Check
- aka: CRC, cyclic code checksum, CRC Integrity Check, CRC validation, image/ROM checksum, message CRC, frame check sequence
- kind: error-handling
- what: Data blocks carry a checksum computed by polynomial division over GF(2); the receiver/reader recomputes it to detect corruption in storage or transit.
- problem: Large data regions and messages accumulate bit errors that simple parity misses; CRCs detect burst errors with small, cheaply computed check values.
- named-in: corpus:hanmer — Patterns for Fault Tolerant Software - Hanmer (2007)
- tags: embedded, networking, safety, robustness, communication, fault-detection

### dead-letter-channel — Dead Letter Channel
- aka: dead letter queue, DLQ
- kind: error-handling
- what: A designated channel to which the messaging layer moves messages that cannot be delivered or processed, instead of dropping or endlessly retrying them.
- problem: Undeliverable or repeatedly failing messages would otherwise poison the main queue or vanish silently; parking them aside preserves them for inspection and keeps the main flow healthy.
- named-in: Enterprise Integration Patterns - Hohpe & Woolf (2003)
- tags: messaging

### deferred-validation — Deferred Validation
- aka: validate on use, delayed integrity checking
- kind: error-handling
- what: Delay comprehensive validity checking of captured data until an action requires it, scaling the rigor of the check to the consequences of that action (edit freely, validate on save/commit/publish).
- problem: Eager validation at entry time rejects legitimately incomplete in-progress data and hard-codes one rigidity level; different actions need different degrees of integrity.
- named-in: Cunningham, 'The CHECKS Pattern Language of Information Integrity' (PLoP 1994; c2.com/ppr/checks.html, loaded live)
- tags: validation, domain-modeling

### diagnostic-context — Diagnostic Context
- aka: mapped diagnostic context (MDC), nested diagnostic context (NDC), log context, contextual logging
- kind: error-handling
- what: Attach per-thread/per-request key-value context (transaction id, user, request id) to a stash that the logging system automatically appends to every message emitted within that scope.
- problem: Interleaved logs from concurrent activities are unattributable; carrying context explicitly through every call is invasive, so the logger holds it ambiently per execution scope.
- named-in: Harrison, 'Patterns for Logging Diagnostic Messages', PLoPD3 (1997); canonical living form: log4j/logback/SLF4J MDC/NDC documentation
- tags: diagnostics, logging, observability

### diagnostic-logger — Diagnostic Logger
- aka: logger, logging facility, centralized diagnostic logging
- kind: error-handling
- what: Route all diagnostic messages through a dedicated logger object that decouples message producers from output destinations, formats, and severity filtering.
- problem: Ad-hoc prints scatter diagnostic policy through the code; a central logger lets destination, format, and level be configured without touching call sites.
- named-in: Harrison, 'Patterns for Logging Diagnostic Messages', PLoPD3 (1997) (PLoPD3 ToC loaded live); living realizations: log4j/syslog-style logging frameworks
- tags: diagnostics, logging

### error-handler — Error Handler
- aka: separated error-processing code
- kind: error-handling
- what: Concentrate error-processing logic in dedicated handler components/blocks separate from normal-flow code, invoked when errors are detected.
- problem: Error handling interleaved with mainline logic is duplicated, inconsistent, and untestable; separating it gives one place to get recovery right.
- named-in: corpus:hanmer — Patterns for Fault Tolerant Software - Hanmer (2007)
- tags: fault-tolerance

### error-kernel — Error Kernel
- aka: —
- kind: error-handling
- what: Keep the irreplaceable state and critical logic in a small, maximally simple core, delegating risky or failure-prone work to expendable child components that can crash and be restarted.
- problem: If valuable state lives where risky work happens, every failure threatens it; pushing risk to the leaves lets crashes stay cheap while the kernel stays reliable.
- named-in: Reactive Design Patterns - Kuhn, Hanafee, Allen (2017)
- tags: erlang, scala, actor-model

### escalation — Escalation
- aka: recovery escalation ladder
- kind: error-handling
- what: When a recovery action fails to clear an error, escalate to a progressively more drastic action (retry -> restart task -> restart process -> reboot) up a defined ladder.
- problem: No single recovery action handles all faults; an ordered ladder bounds recovery time while preferring the least disruptive action that works.
- named-in: corpus:hanmer — Patterns for Fault Tolerant Software - Hanmer (2007)
- tags: fault-tolerance, embedded

### exceptional-value — Exceptional Value
- aka: exceptional value object, distinguished out-of-range value
- kind: error-handling
- what: A distinguished value object representing missing or invalid input that flows through the domain model, absorbing or rejecting messages instead of raising errors.
- problem: Real-world input contains blanks and illegible entries; letting a typed placeholder value propagate keeps exceptional-case handling concentrated near the UI instead of scattered through business logic, while still recording that the input was bad.
- named-in: Cunningham, The CHECKS Pattern Language of Information Integrity (PLoP 1994; c2.com/ppr/checks.html)
- tags: information-integrity, borderline — adjacent to null-object and special-case (both indexed); kept as the CHECKS-named propagate-through-computation mechanism the mission explicitly seeds

### fail-fast — Fail Fast
- aka: precondition rejection
- kind: error-handling
- what: Check preconditions and resource availability up front and report failure immediately, rather than doing work that is doomed to fail slowly.
- problem: Slow failures consume caller time and system resources; failing before acquiring resources preserves capacity and gives callers fast, actionable errors.
- named-in: corpus:nygard — Release It! Design and Deploy Production-Ready Software, 2nd ed. - Nygard (2018)
- tags: stability

### goto-cleanup — Goto Cleanup
- aka: goto error handling (Fluent C), centralized exiting of functions (Linux kernel), goto chain, cleanup record (variant), Goto Error Cleanup, goto error handling, centralized function exit
- kind: error-handling
- what: On failure, jump forward to a single labeled cleanup section at the end of the function that releases resources in reverse acquisition order.
- problem: Multi-step acquisition in C needs unwinding on every failure path; one exit chain avoids duplicated cleanup code and leak-prone nested conditionals.
- named-in: corpus:kernelstyle — Linux kernel coding style (living); also Goto Error Handling in Fluent C - Preschern (2022)
- tags: c, linux, embedded, systems

### guard-clause — Guard Clause
- aka: early return, replace nested conditional with guard clauses, bouncer pattern
- kind: error-handling
- what: Check preconditions/special cases at the top of a function and return immediately, keeping the main path unindented.
- problem: Deeply nested conditionals obscure the dominant path; guard clauses flatten control flow and make precondition handling explicit.
- named-in: corpus:fowlerref — Refactoring - Martin Fowler (1999), 'Replace Nested Conditional with Guard Clauses'; also Fluent C (2022)
- tags: c, borderline — Statement-level code-shaping idiom below typical design altitude; kept because two catalogs name it as a pattern.

### happy-eyeballs — Happy Eyeballs
- aka: fast fallback, connection racing, dual-stack connection attempts
- kind: error-handling
- what: Race connection attempts over alternative paths (canonically IPv6 vs IPv4) with small staggered delays, keep the first to succeed, and cancel the rest.
- problem: Trying alternatives strictly in sequence makes users wait out full timeouts when the preferred path is broken; staggered parallel attempts hide failures at the cost of a little duplicate work.
- named-in: RFC 8305: Happy Eyeballs Version 2: Better Connectivity Using Concurrency - Schinazi & Pauly (2017)
- tags: networking, ipv6, clients

### heartbeat — Heartbeat
- aka: liveness ping, keepalive, TCP keepalive, liveness probe, application-level keepalive
- kind: error-handling
- what: A monitored component emits (or answers) a periodic signal; missing beats mark it as failed and trigger recovery.
- problem: A silently dead task or peer is indistinguishable from a slow one without an agreed periodic liveness signal and timeout.
- named-in: corpus:hanmer — Patterns for Fault Tolerant Software - Hanmer (2007)
- tags: fault-detection, distributed, embedded, networking, fault-tolerance

### leaky-bucket-counter — Leaky Bucket Counter
- aka: decaying error counter
- kind: error-handling
- what: An error counter incremented on each fault and decremented ('leaked') periodically; recovery escalates only when the count crosses a threshold, i.e. errors arrive faster than they drain.
- problem: Distinguishing an acceptable background rate of transient errors from a persistent fault requires rate, not count; the leak encodes the acceptable rate. Distinct from the leaky-bucket traffic shaper.
- named-in: corpus:hanmer — Patterns for Fault Tolerant Software - Hanmer (2007)
- tags: fault-detection, embedded

### let-it-crash — Let It Crash
- aka: crash-only software, fail and restart
- kind: error-handling
- what: On unexpected error, abandon in-process recovery: let the failing unit die immediately and rely on an external mechanism (supervisor, restart) to recreate it in a known-good state.
- problem: Defensive recovery code for unanticipated errors is itself error-prone and can leave corrupt state; a clean crash-plus-restart returns to a verified initial state.
- named-in: corpus:nygard — Release It! Design and Deploy Production-Ready Software, 2nd ed. - Nygard (2018)
- tags: erlang, stability, borderline — Erlang-rooted philosophy verging on a design principle; kept because it names a concrete, recurring failure-handling mechanism (crash + supervised restart). Related: Candea & Fox crash-only software.

### log-errors — Log Errors
- aka: error logging, diagnostic error logging channel
- kind: error-handling
- what: Record error details on a separate diagnostic channel (log file, console, trace buffer) at the point where the error occurs, instead of forcing all debug information through return values to the caller.
- problem: Callers need only actionable error information, but programmers debugging the system need full detail; funneling both through return codes bloats APIs and loses context available only at the error site.
- named-in: corpus:preschern — Fluent C ch. 2 (Preschern 2022); also 'Patterns for Returning Error Information in C' (Preschern, EuroPLoP 2019, ACM DL)
- tags: c

### loop-timeout — Loop Timeout
- aka: hardware timeout (timer-based variant), timeout-protected polling loop
- kind: error-handling
- what: Bound every polling/wait loop with a software counter or hardware timer so the loop cannot hang forever if the awaited hardware condition never occurs.
- problem: Unbounded waits on hardware flags hang the whole system when a peripheral fails; an explicit timeout converts a hang into a detectable, handleable error. Pont's HARDWARE TIMEOUT timer-based variant is folded here.
- named-in: corpus:pont — Patterns for Time-Triggered Embedded Systems - Pont (2001)
- tags: embedded, c, robustness

### marked-data — Marked Data
- aka: data poisoning flag, corrupt-data marking
- kind: error-handling
- what: Tag data elements known or suspected to be erroneous so subsequent processing can skip, repair, or handle them specially instead of propagating the corruption.
- problem: Deleting bad data may be worse than keeping it; an explicit corruption mark contains the error while preserving structure and audit trail.
- named-in: corpus:hanmer — Patterns for Fault Tolerant Software - Hanmer (2007)
- tags: fault-tolerance

### meaningless-behavior — Meaningless Behavior
- aka: let meaningless computations fail quietly
- kind: error-handling
- what: Write domain methods without defensive input checks; let computations on exceptional/missing values fail or yield meaningless results, and have the input/output boundary recover (e.g. display blank) instead.
- problem: Defensive checks duplicated through every domain method obscure the model; centering recovery at the presentation boundary keeps domain code minimal while tolerating bad data.
- named-in: Cunningham, 'The CHECKS Pattern Language of Information Integrity' (PLoP 1994; c2.com/ppr/checks.html, loaded live)
- tags: validation, domain-modeling

### n-version-programming — N-Version Programming
- aka: multiversion programming, design diversity with voting
- kind: error-handling
- what: Run N independently developed implementations of the same specification and adjudicate their outputs by a voter to mask residual design faults.
- problem: Identical redundant copies share design faults; diverse implementations plus majority voting tolerate faults no single version can. The voter/voting mechanism (Hanmer: Voting) is folded here.
- named-in: The N-Version Approach to Fault-Tolerant Software - Avizienis (1985)
- tags: fault-tolerance, safety-critical, borderline — Development-process-heavy (independent teams, common spec), but the runtime N-version-plus-voter execution is implementable inside one program; kept with tag rather than parked.

### notification — Notification
- aka: error-collecting parameter object
- kind: error-handling
- what: An object that accumulates errors and messages during an operation (typically validation) and is returned or passed across a layer boundary instead of throwing on first failure.
- problem: Exceptions abort at the first problem and cross layer boundaries poorly; a notification gathers all failures so callers can report them together.
- named-in: Notification - Martin Fowler, Further Enterprise Application Architecture development (eaaDev)
- tags: oo

### quarantine — Quarantine
- aka: fault isolation of a unit
- kind: error-handling
- what: Isolate a faulty element from the rest of the system - stop routing work to it, fence its outputs - so its errors cannot spread while diagnosis or recovery proceeds.
- problem: A faulty unit that keeps participating spreads corrupt data and secondary failures; active isolation contains the damage.
- named-in: corpus:hanmer — Patterns for Fault Tolerant Software - Hanmer (2007)
- tags: fault-tolerance, borderline — Presumes isolatable units, which shades architectural; kept because in-process quarantine (disabling a worker, fencing a plugin) is implementable in one component.

### railway-oriented-programming — Railway-Oriented Programming
- aka: two-track error handling, Result chaining, Kleisli composition of Results
- kind: error-handling
- what: Composing a workflow as a chain of functions over a two-track success/failure type, where any failure switches the rest of the pipeline onto the error track automatically.
- problem: Keeps multi-step validation/IO workflows linear and readable while still short-circuiting on the first failure and accumulating error information, without nested conditionals or exceptions.
- named-in: Railway Oriented Programming - Scott Wlaschin (fsharpforfunandprofit.com / NDC, 2014)
- tags: fp, fsharp, borderline — Essentially a named usage idiom of the result type (monadic bind); kept as a separate entry because the name is established and widely taught, cross-linked to result-type.

### recovery-blocks — Recovery Blocks
- aka: recovery block scheme
- kind: error-handling
- what: Execute a primary algorithm, validate its result with an acceptance test, and on failure roll back and run an alternate implementation of the same function.
- problem: A single implementation may contain residual design faults; structured alternates plus an acceptance test give software fault tolerance within one program.
- named-in: System Structure for Software Fault Tolerance - Randell (1975)
- tags: fault-tolerance

### restart — Restart
- aka: microreboot, component restart
- kind: error-handling
- what: Recover from an unhandled or unrecoverable error by reinitializing the affected unit (task, process, component, or whole program) to its known-good initial state.
- problem: Some errors leave state too corrupt to repair in place; restarting from verified initial conditions is the recovery of last resort with predictable cost.
- named-in: corpus:hanmer — Patterns for Fault Tolerant Software - Hanmer (2007)
- tags: fault-tolerance, embedded

### result-type — Result Type
- aka: Either type, Try, error union, error object, status_code error object, expected, outcome, object-based error handling
- kind: error-handling
- what: A sum type carrying either a success value or an error value, returned instead of throwing, so failure is part of the function's signature.
- problem: Makes failure paths visible and composable in the type system, avoiding invisible exception control flow and forcing callers to acknowledge errors.
- named-in: corpus:p1028 — P1028 SG14 status_code and standard error object - Douglas (WG21, 2020)
- tags: fp, rust, haskell, fsharp, scala, swift, c++, c, embedded

### retry-budget — Retry Budget
- aka: retry ratio cap, per-client retry quota
- kind: error-handling
- what: Cap retries globally as a fraction of primary requests (e.g. retries may add at most 10% extra load), disabling retry when the budget is exhausted.
- problem: Per-request retry limits still multiply load during a broad outage; a system-wide budget prevents retry amplification from turning partial failure into total overload.
- named-in: Site Reliability Engineering: How Google Runs Production Systems - Beyer, Jones, Petoff, Murphy eds. (2016)
- tags: distributed, overload

### retry-with-exponential-backoff-and-jitter — Retry with Exponential Backoff and Jitter
- aka: exponential backoff, truncated binary exponential backoff, retry with jitter
- kind: error-handling
- what: Retry a failed operation a bounded number of times, doubling the wait between attempts and randomizing (jittering) it to avoid synchronized retry storms.
- problem: Immediate or fixed-interval retries from many clients synchronize into load spikes that prolong the outage they respond to; capped attempts (Hanmer: Limit Retries, folded here) prevent infinite retry loops.
- named-in: Timeouts, Retries, and Backoff with Jitter - Brooker, AWS Builders' Library (2019)
- tags: distributed, networking

### return-status-code — Return Status Code
- aka: error code return convention, errno-style status (related convention), return relevant errors, error code convention, errno-style error reporting, status return convention
- kind: error-handling
- what: Functions return a numeric/enum status indicating success or a specific failure, delivering actual results through out-parameters.
- problem: C has no exceptions; a uniform status-return channel makes failure explicit and checkable at every call boundary.
- named-in: corpus:preschern — Fluent C - Christopher Preschern (2022); also Preschern's EuroPLoP error-handling pattern papers
- tags: c, embedded

### riding-over-transients — Riding Over Transients
- aka: transient fault filtering
- kind: error-handling
- what: Deliberately ignore errors that are momentary and self-clearing, acting only when an error persists or recurs beyond a threshold.
- problem: Reacting instantly to every transient glitch triggers needless recovery actions that cost more than the fault itself; filtering separates transient from persistent faults.
- named-in: corpus:hanmer — Patterns for Fault Tolerant Software - Hanmer (2007)
- tags: fault-tolerance, embedded

### roll-forward — Roll-Forward
- aka: forward error recovery
- kind: error-handling
- what: Recover from an error by advancing the system to a new consistent state ahead of the error point, reconstructing or discarding in-flight work rather than returning to a checkpoint.
- problem: Rolling back can be impossible (real-time deadlines, external side effects already visible); moving forward to the next safe state keeps the system live.
- named-in: corpus:hanmer — Patterns for Fault Tolerant Software - Hanmer (2007)
- tags: fault-tolerance

### rollback — Rollback
- aka: backward error recovery
- kind: error-handling
- what: Recover from an error by restoring the system to a previously saved consistent state (a checkpoint) and resuming from there.
- problem: An error may have corrupted current state; returning to a known-good earlier state removes the error's effects at the cost of redoing work.
- named-in: corpus:hanmer — Patterns for Fault Tolerant Software - Hanmer (2007)
- tags: fault-tolerance

### safe-state — Safe State
- aka: fail-safe state, safe state transition
- kind: error-handling
- what: A predefined operating condition without unreasonable risk that the system deliberately enters on fault detection (outputs de-energized, actuators parked, subsystem disabled).
- problem: When a fault makes continued normal operation untrustworthy, the firmware needs a designed, reachable state that minimizes harm; defining and driving to that state is the core functional-safety mechanism.
- named-in: corpus:iso26262 — ISO 26262:2018 - Road vehicles - Functional safety
- tags: embedded, safety-critical, borderline — A system-safety concept as much as a code mechanism, but implemented as a concrete in-program transition routine - kept IN with the tag.

### samurai-principle — Samurai Principle
- aka: return victorious or not at all, crash early (related, Pragmatic Programmer)
- kind: error-handling
- what: For errors the caller cannot meaningfully handle, do not return an error code - assert/abort at the failure point instead.
- problem: Propagating unhandleable errors buries the fault and corrupts state downstream; failing fast at the point of detection preserves the evidence.
- named-in: corpus:preschern — Fluent C - Christopher Preschern (2022)
- tags: c, embedded, robustness

### sentinel-value — Sentinel Value
- aka: flag value, rogue value, signal value, trip value
- kind: error-handling
- what: A special in-band value, distinct from all legal data, used to signal a condition such as end-of-data, absence, or failure (NUL terminator, -1, null pointer).
- problem: When a channel or return type has no out-of-band way to signal termination or absence, a reserved value carries the signal without extra state or size bookkeeping.
- named-in: The Art of Computer Programming Vol. 3: Sorting and Searching - Donald Knuth (1973); also Code Complete 2nd ed. - McConnell (2004)
- tags: c, embedded

### setjmp-longjmp-error-handling — setjmp/longjmp Error Handling
- aka: CException, TRY/EXCEPT macros in C, non-local jump error handling, exceptions in C, TRY/EXCEPT macros, Hanson Except module, non-local exit
- kind: error-handling
- what: Macro-wrapped setjmp/longjmp implementing raise-and-catch non-local control transfer as an exception facility in C.
- problem: Deeply nested call chains cannot practically thread error codes through every level; a structured non-local jump delivers errors straight to a handler.
- named-in: corpus:hanson — C Interfaces and Implementations - Hanson (1996)
- tags: c, embedded

### software-rejuvenation — Software Rejuvenation
- aka: proactive restart, planned rejuvenation
- kind: error-handling
- what: Proactively restart or reinitialize a long-running process on a schedule or on resource-degradation signals, before software aging (leaks, fragmentation, drift) causes failure.
- problem: Long-running processes accumulate degradation that eventually causes outages at uncontrolled moments; planned rejuvenation converts that into cheap, scheduled downtime.
- named-in: Software Rejuvenation: Analysis, Module and Applications - Huang, Kintala, Kolettis, Fulton (1995)
- tags: fault-tolerance, long-running-systems

### special-return-value — Special Return Value
- aka: in-band error value, sentinel return (NULL, -1, EOF)
- kind: error-handling
- what: Reserve one or more values of the normal return domain (NULL, -1, EOF) to signal failure in-band, avoiding a separate status channel.
- problem: When the result domain has spare values, in-band signaling keeps APIs terse; the C-API-convention face of the general sentinel-value element.
- named-in: corpus:preschern — Fluent C - Christopher Preschern (2022)
- tags: c

### stack-painting-watermarking — Stack Painting / Watermarking
- aka: stack high-water mark, stack fill pattern, stack usage watermarking
- kind: error-handling
- what: Fill each stack with a known pattern at startup and later scan for the deepest overwritten address to measure worst-case stack usage and detect near-overflow.
- problem: Stack overflow in fixed-stack embedded systems corrupts adjacent memory silently; painting makes actual usage observable so stack sizes can be right-sized and overflows caught (complementary to canary/guard-zone checks).
- named-in: corpus:freertosbook — Mastering the FreeRTOS Real-Time Kernel (stack overflow detection and uxTaskGetStackHighWaterMark)
- tags: embedded, rtos, robustness

### supervisor — Supervisor
- aka: supervision tree, supervisor hierarchy
- kind: error-handling
- what: A component whose only job is to monitor child workers and apply a declared restart strategy (one-for-one, one-for-all, escalation to its own supervisor) when they crash.
- problem: Let-it-crash needs someone to do the restarting; a hierarchy of supervisors turns individual crashes into localized, policy-driven recovery instead of whole-program failure.
- named-in: OTP Design Principles (Erlang/OTP documentation) - Ericsson (living)
- tags: erlang, elixir, actor-model

### timeout — Timeout
- aka: timed wait, deadline on blocking call
- kind: error-handling
- what: Bound every blocking wait on an external resource or call with a maximum duration, treating expiry as failure.
- problem: Unbounded waits on unresponsive dependencies tie up threads and connections, propagating a remote failure into local resource exhaustion and cascading failure.
- named-in: corpus:nygard — Release It! Design and Deploy Production-Ready Software, 2nd ed. - Nygard (2018)
- tags: stability, networking


## Robustness & security — `robustness-security` (40)

### access-control-list — Access Control List
- aka: ACL, per-object permission list, access matrix by column
- kind: robustness-security
- what: Store, with each protected object, the list of subjects and the operations each may perform on it; checks consult the object's list.
- problem: The full subject-by-object access matrix is sparse; attaching permissions to the object makes per-object review and revocation direct (the column-slice of Lampson's access matrix).
- named-in: Lampson, Protection (1971, access matrix); Saltzer & Schroeder (1975); standard OS textbooks
- tags: security, authorization, data-representation-flavored

### allowlist-input-validation — Allowlist Input Validation
- aka: whitelist validation, positive validation, positive security model, denylist/blacklist validation (weaker complement), Intercepting Validator (placement variant, Core Security Patterns)
- kind: robustness-security
- what: Validate untrusted input by accepting only what matches an explicit specification of the known-good (type, length, range, grammar) and rejecting everything else.
- problem: Enumerating bad input (denylist) always misses encodings and novel attacks; specifying the accepted language flips the default to reject-unknown.
- named-in: OWASP Input Validation Cheat Sheet; Steel, Nagappan & Lai, Core Security Patterns (2005)
- tags: security, validation, borderline — Overlaps index entry complete-parameter-checking (Hanmer, fault-tolerance framing); kept because the positive-security-model discipline against adversarial input is the distinctly named security mechanism

### audit-log — Audit Log
- aka: audit trail, security event log, Secure Logger (Core Security Patterns), tamper-evident log / hash-chained log (hardened variant), change log (domain-level)
- kind: robustness-security
- what: An append-only record of security-relevant events (who did what, when, from where), written at the point of action for later reconstruction and accountability.
- problem: After a fault or breach you must reconstruct what happened; ordinary debug logging is neither complete, attributable, nor protected against tampering.
- named-in: Fowler, Audit Log (martinfowler.com eaaDev); Steel, Nagappan & Lai, Core Security Patterns (2005, 'Secure Logger'); Schneier & Kelsey (1999, secure audit logs)
- tags: security, persistence-flavored

### authenticated-encryption — Authenticated Encryption
- aka: AEAD, authenticated encryption with associated data, encrypt-then-MAC (generic construction), AES-GCM / ChaCha20-Poly1305 (realizations)
- kind: robustness-security
- what: Encrypt and authenticate a message in one construction (optionally binding unencrypted associated data), so ciphertext cannot be undetectably modified.
- problem: Encryption alone is malleable — attackers can flip ciphertext bits meaningfully; ad hoc MAC+encrypt compositions have failed repeatedly (padding oracles), so the combined primitive is the designer-facing element.
- named-in: RFC 5116 (An Interface and Algorithms for Authenticated Encryption, 2008); Rogaway AEAD literature
- tags: security, crypto, borderline — Crypto-primitive altitude; included as the modern reach-for-by-role encryption element

### canonicalization-before-validation — Canonicalization Before Validation
- aka: input canonicalization, normalize before validate, path canonicalization
- kind: robustness-security
- what: Reduce input (paths, URLs, Unicode strings) to its single canonical form before applying validation or access checks, so equivalent encodings cannot slip past the check.
- problem: The same resource or string has many encodings (../, %2e%2e, Unicode homoglyphs, symlinks); validating a non-canonical form lets an equivalent alias bypass the filter after the check.
- named-in: corpus:seacordsecure — SEI CERT rules IDS01-J (normalize before validating) / FIO02-C (canonicalize path names); OWASP Input Validation guidance; Seacord, Secure Coding in C and C++
- tags: security, validation

### capability — Capability
- aka: capability list, object-capability, unforgeable reference, capability token, access matrix by row
- kind: robustness-security
- what: An unforgeable token/reference that both designates an object and carries the authority to use it; possession is permission (the row-slice of the access matrix).
- problem: Checking identity against lists on every access needs ambient authority and a subject database; handing out unforgeable, delegatable, attenuable references makes authority flow with the references themselves.
- named-in: Dennis & Van Horn, Programming Semantics for Multiprogrammed Computations (CACM 1966); Miller, Robust Composition (2006, object-capability)
- tags: security, authorization, borderline — OS-level origin, but in-language object-capability discipline (E, Caja, handle-based APIs) is an established in-process form

### check-point — Check Point
- aka: Access Verification, Validation and Penalization
- kind: robustness-security
- what: A single configurable object/component that concentrates authentication, authorization and violation-response decisions, so the security policy can change without touching callers.
- problem: Security policy evolves and differs per deployment; hard-coding checks throughout the application makes policy change and penalization logic unmaintainable. PAM-style pluggable authentication is a canonical realization.
- named-in: Yoder & Barcalow (PLoP 1997); Schumacher et al., Security Patterns (Wiley 2006)
- tags: security, application-level

### constant-time-comparison — Constant-Time Comparison
- aka: timing-safe equality, constant-time programming
- kind: robustness-security
- what: Compare secret-dependent data (MACs, tokens, passwords hashes) with an algorithm whose running time and memory access pattern are independent of the data values.
- problem: Early-exit comparison leaks how many leading bytes matched through timing, letting attackers recover secrets byte by byte; data-independent execution closes the side channel.
- named-in: BearSSL: Constant-Time Crypto - Pornin (living)
- tags: security, cryptography, c

### cryptographic-hash-function — Cryptographic Hash Function
- aka: message digest, one-way hash, collision-resistant hash, fingerprint / content hash (roles)
- kind: robustness-security
- what: A fixed-size digest function that is one-way and collision-resistant, used for integrity fingerprints, content addressing, commitment, and as a building block for MACs and signatures.
- problem: CRCs and checksums detect accidental corruption only; against an adversary who can recompute them, integrity requires a digest that cannot be forged or collided.
- named-in: Menezes, van Oorschot & Vanstone, Handbook of Applied Cryptography (1996, ch. 9); FIPS 180 (Secure Hash Standard)
- tags: security, crypto, borderline — Crypto-primitive altitude; included because index elements (merkle-tree, constant-time-comparison) already presuppose it and CRC is in the catalog

### csprng — Cryptographically Secure Pseudorandom Number Generator
- aka: CSPRNG, DRBG (deterministic random bit generator), secure random source
- kind: robustness-security
- what: A random generator whose output is computationally unpredictable even to an observer of prior output, seeded from real entropy, for keys, tokens, nonces and salts.
- problem: Ordinary PRNGs (linear congruential, Mersenne Twister) are predictable from a few outputs; any security value derived from them (session ids, keys) is guessable.
- named-in: NIST SP 800-90A (DRBG); RFC 4086 (Randomness Requirements for Security)
- tags: security, crypto, borderline — Crypto-primitive altitude; note the index has no PRNG element at all — the whole random-generation band is absent

### defensive-copy — Defensive Copy
- aka: defensive copying, copy-in/copy-out at trust boundaries
- kind: robustness-security
- what: Copy mutable inputs on receipt and mutable internal state on return, so external aliases can never mutate an object's invariant-protected state.
- problem: Sharing references to mutable components lets callers corrupt invariants (time-of-check/time-of-use attacks); copying at the boundary restores encapsulation.
- named-in: Effective Java - Joshua Bloch (2001; 3rd ed. Item 50)
- tags: java, csharp

### dual-channel — Dual Channel
- aka: homogeneous/heterogeneous dual channel
- kind: robustness-security
- what: Two parallel channels (identical or diversely implemented) process the same inputs, with comparison or switchover logic detecting faults and continuing or safing on disagreement.
- problem: Single-channel systems cannot keep operating through a channel fault; replication (homogeneous for random faults, heterogeneous for systematic ones) buys fault tolerance with hardware/software cost.
- named-in: corpus:douglasspatternsc — Design Patterns for Embedded Systems in C - Bruce Powel Douglass (2011)
- tags: embedded, safety, borderline — Sits at the design/architecture boundary - kept per the DPESC safety-pattern canon; the system-scale redundancy variants are parked for Phase 3.

### full-view-with-errors — Full View With Errors
- aka: Full Access with Errors
- kind: robustness-security
- what: Show users the complete set of operations/data and reject unauthorized attempts with explicit errors at use time.
- problem: Tailoring the interface per user is complex; presenting everything and enforcing at the action point is simpler and keeps the enforcement in one place, at the cost of revealing what exists.
- named-in: Yoder & Barcalow (PLoP 1997); Schumacher et al. (Wiley 2006)
- tags: security, ui, borderline — UI-policy flavored, but an in-application enforcement-placement mechanism; dual of Limited View

### guard-page — Guard Page
- aka: red zone, redzone, guard region, PAGE_GUARD, electric fence
- kind: robustness-security
- what: Place an inaccessible (or trap-on-touch) memory page or poisoned band adjacent to a stack or allocation so that overrun/overflow faults immediately at the boundary instead of corrupting neighbors.
- problem: Buffer and stack overflows silently corrupt adjacent memory and surface far from the bug; a trapping boundary converts the overrun into an immediate, located fault (and enables lazy stack growth). Allocator redzones (ASan-style poisoned bands) folded as aka; distinct from the ABI 'red zone' stack optimization.
- named-in: Creating Guard Pages - Microsoft Win32 documentation (live)
- tags: os, memory-safety, debugging, borderline — Relies on MMU protection, so it straddles the OS/hardware boundary - but it is set up inside one program (allocator, runtime, thread library), so kept IN.

### html-sanitization — HTML Sanitization
- aka: markup sanitization, HTML sanitizer, DOM-based sanitization
- kind: robustness-security
- what: Parse untrusted markup into a DOM and rebuild it keeping only an allowlist of safe elements/attributes, yielding markup that renders but cannot execute script.
- problem: When users must be allowed to supply rich markup, output encoding would destroy it; regex filtering of markup is reliably bypassable, so parse-filter-serialize is the established defense.
- named-in: OWASP HTML Sanitization guidance (XSS Prevention Cheat Sheet); OWASP Java HTML Sanitizer; WHATWG HTML Sanitizer API (draft)
- tags: security, web, parsing-flavored, borderline — Distinct from index entry escape-sequence: sanitization filters a parsed structure rather than encoding characters

### limited-view — Limited View
- aka: Limited Access
- kind: robustness-security
- what: Present users only the operations and data their permissions allow, so unauthorized actions cannot even be attempted.
- problem: Letting users attempt forbidden operations and then failing them leaks structure and frustrates; filtering the view by permission prevents the attempt, at the cost of computing per-user views.
- named-in: Yoder & Barcalow (PLoP 1997); Schumacher et al. (Wiley 2006, 'Limited Access')
- tags: security, ui, borderline — UI-policy flavored, but an in-application enforcement-placement mechanism; dual of Full View With Errors

### memory-poisoning — Memory Poisoning
- aka: poison values, fill patterns, magic debug values, page poisoning, slab poisoning, 0xDEADBEEF fill, use-after-free poisoning
- kind: robustness-security
- what: Fills freed or uninitialized memory with a recognizable poison pattern and verifies it later (on reallocation or access), so stale reads, use-after-free, and buffer overruns surface as the pattern or its corruption.
- problem: Memory-lifetime bugs are silent and nondeterministic; deterministic poison patterns make invalid accesses detectable, reproducible, and diagnosable from a crash dump.
- named-in: Linux kernel CONFIG_PAGE_POISONING and slab-poisoning documentation (verified live); also AddressSanitizer shadow-poisoning terminology (Serebryany et al., USENIX ATC 2012)
- tags: memory debugging, allocators, embedded, kernels, borderline — distinct from stack-painting (usage watermarking), guard-page (trapping region), and marked-data (flagging known-corrupt application data)

### message-authentication-code — Message Authentication Code
- aka: MAC, HMAC, keyed hash, authentication tag
- kind: robustness-security
- what: A keyed digest over a message that only holders of the secret key can produce or verify, authenticating both integrity and origin.
- problem: A plain hash of a message can be recomputed by anyone, so it proves nothing about who produced it; binding the digest to a shared secret defeats tampering and forgery in transit or at rest.
- named-in: RFC 2104 (HMAC, 1997); Handbook of Applied Cryptography ch. 9
- tags: security, crypto, borderline — Crypto-primitive altitude; the index's constant-time-comparison exists chiefly to compare MAC tags safely

### nonce — Nonce
- aka: number used once, anti-replay counter (monotonic variant), challenge value (challenge-response usage)
- kind: robustness-security
- what: A value used exactly once within a security context (random, counter, or timestamp-based) so that replayed or duplicated messages/operations are detectable and rejected.
- problem: A verifier cannot otherwise distinguish a fresh legitimate message from a captured-and-replayed one; uniqueness per interaction restores freshness.
- named-in: RFC 4949 (Internet Security Glossary); Handbook of Applied Cryptography ch. 10
- tags: security, crypto, protocol, borderline — Protocol-element flavored, but implemented and checked in-process; sibling of index entries idempotency key and serial-number-arithmetic

### one-s-complement-data-storage — One's Complement Data Storage
- aka: One's Complement Pattern, inverted duplicate storage
- kind: robustness-security
- what: Critical data is stored twice - once normally, once bit-inverted - and every read verifies the pair still complement each other before use.
- problem: Memory corruption (EMI, cosmic rays, stuck bits, wild pointers) silently alters safety-relevant values; a complemented copy detects corruption at each access.
- named-in: corpus:douglasspatternsc — Design Patterns for Embedded Systems in C - Bruce Powel Douglass (2011)
- tags: embedded, safety

### parameterized-query — Parameterized Query
- aka: prepared statement, bind variables, placeholders, query parameterization
- kind: robustness-security
- what: Send the query text and the data values to the interpreter separately, so values are bound as data and can never be parsed as code.
- problem: Building queries by string concatenation lets attacker-controlled input change the query structure (SQL injection); separating code from data removes the injection channel by construction.
- named-in: OWASP Query Parameterization Cheat Sheet / OWASP Top 10 injection guidance; every major database API
- tags: security, databases, injection-defense

### pointer-check — Pointer Check
- aka: NULL-after-free discipline, explicit pointer invalidation and check
- kind: robustness-security
- what: Explicitly set pointers to an invalid value (NULL) when uninitialized or freed, and check pointers against that invalid value before dereferencing them.
- problem: Dangling and uninitialized pointers cause corruption far from the defect site; pairing deliberate invalidation with checks before use converts silent memory corruption into detectable, handleable conditions.
- named-in: corpus:preschern — Fluent C ch. 3, memory management patterns (Preschern 2022)
- tags: c, borderline — overlaps sanity-check and complete-parameter-checking in the index; kept separate because the mechanism is the invalidate-on-free/init + check-before-use pairing specific to raw-pointer lifetime, not general input validation

### privilege-bracketing — Privilege Bracketing
- aka: privilege drop/restore, temporary privilege elevation, drop privileges, seteuid bracketing
- kind: robustness-security
- what: Hold elevated privilege only across the exact operations that need it: raise at the last possible moment, perform the action, drop immediately after (and permanently once never needed again).
- problem: A process that keeps privileges it rarely needs turns every bug into a privileged bug; bracketing minimizes the window in which a fault or exploit runs privileged.
- named-in: Oracle Solaris Developer's Guide to Security ('privilege bracketing'); Viega & Messier, Secure Programming Cookbook for C and C++ (2003, dropping privileges in setuid programs)
- tags: security, least-privilege, unix

### privilege-separation — Privilege Separation
- aka: privsep, privileged monitor / unprivileged worker split, OpenSSH privilege separation
- kind: robustness-security
- what: Split one application into a small privileged process and unprivileged worker processes that request sensitive operations over a narrow IPC interface, so a compromise of the exposed code yields no privileges.
- problem: Monolithic privileged programs let any exploited parsing/network-facing code inherit full privileges; confining privileges to a minimal monitor bounds the damage.
- named-in: Provos, Friedl, Honeyman, 'Preventing Privilege Escalation', 12th USENIX Security Symposium 2003 (verified live)
- tags: security, unix, borderline: multi-process internal structure edges toward architecture; kept design-realm because it is a named mechanism implemented within one application (privilege-bracketing covers only the temporal form)

### program-sequence-monitoring — Program Sequence Monitoring
- aka: control flow monitoring, logical program flow monitoring, logical supervision (AUTOSAR WdgM), control flow checking
- kind: robustness-security
- what: Instrument checkpoints along required execution paths and have a monitor (often the watchdog manager) verify that checkpoints occur in the legal order and cadence.
- problem: A timing watchdog alone cannot detect code that runs on time but in the wrong order (skipped safety checks, corrupted control flow); sequence monitoring detects illegal execution paths.
- named-in: corpus:iec61508 — IEC 61508-7:2010 - program sequence monitoring technique
- tags: embedded, safety-critical, robustness

### protected-single-channel — Protected Single Channel
- aka: —
- kind: robustness-security
- what: A single end-to-end data/processing channel augmented with integrity checks at one or more points (CRCs, range checks, monitoring) so faults are detected even without redundant channels.
- problem: Full channel redundancy is costly; when fail-safe (not fail-operational) behavior suffices, one channel plus systematic checking detects faults at lower recurring cost.
- named-in: corpus:douglasspatternsc — Design Patterns for Embedded Systems in C - Bruce Powel Douglass (2011)
- tags: embedded, safety, borderline — Channel-scale structure verging on architecture, but implementable within one component and cataloged by Douglass as a design-level safety pattern.

### reference-monitor — Reference Monitor
- aka: security kernel (hardened realization), policy enforcement point / policy decision point (operational split), Controlled Object Monitor (object-level variant)
- kind: robustness-security
- what: A component that mediates every access by subjects to protected objects, checking each request against the authorization rules before allowing it.
- problem: Access checks sprinkled through code can be skipped or diverge from policy; complete mediation requires one tamper-evident chokepoint that is always invoked and small enough to verify.
- named-in: Anderson, Computer Security Technology Planning Study (1972); Schumacher et al., Security Patterns (Wiley 2006, 'Reference Monitor')
- tags: security, authorization

### role-based-access-control — Role-Based Access Control
- aka: RBAC, Roles (Yoder & Barcalow), role hierarchy, roles as privilege groups
- kind: robustness-security
- what: Authorization is granted to named roles rather than individual users; users acquire permissions by role membership, with optional role hierarchies.
- problem: Per-user permission assignment does not scale and drifts; grouping privileges into roles matches organizational structure and makes review/revocation tractable.
- named-in: Ferraiolo & Kuhn, Role-Based Access Controls (NIST, 1992); ANSI INCITS 359; Yoder & Barcalow 'Roles' (PLoP 1997); Schumacher et al. (Wiley 2006)
- tags: security, authorization

### salted-password-hashing — Salted Password Hashing
- aka: salt, key stretching, adaptive one-way function, password-based key derivation (PBKDF2/bcrypt/scrypt/Argon2 realizations)
- kind: robustness-security
- what: Store passwords only as the output of a deliberately slow one-way function over password plus per-entry random salt, so verification is possible but recovery and precomputation are not.
- problem: Stored plaintext or fast unsalted hashes fall to theft, rainbow tables and cross-user cracking; per-user salt defeats precomputation and cost-tunable hashing keeps brute force expensive as hardware improves.
- named-in: Morris & Thompson, Password Security: A Case History (CACM 1979, introduces salt); OWASP Password Storage Cheat Sheet
- tags: security, crypto

### sanity-check — Sanity Check
- aka: reasonableness check, plausibility check, Runtime Assertion, assert, invariant check, Assertion, runtime contract check
- kind: robustness-security
- what: A lightweight independent monitor verifies that outputs or system state remain within physically/logically plausible bounds, triggering fault handling when they do not.
- problem: Full result verification is often infeasible, but gross faults are cheap to catch; checking plausibility gives broad fault coverage at minimal cost.
- named-in: corpus:douglassrtcorpus — Real-Time Design Patterns - Bruce Powel Douglass (2002)
- tags: embedded, safety, defensive-programming, c, correctness, c++, borderline — Adjacent to the raw assert language facility; included as the named defensive-design mechanism (Hanson's Assert interface, design-by-contract lite).

### secure-access-layer — Secure Access Layer
- aka: —
- kind: robustness-security
- what: An application-internal layer that wraps the security mechanisms of the platforms it sits on (OS, database, network APIs), giving the application one coherent security interface.
- problem: Application security is only as strong as its integration with lower-level security; scattering raw platform security calls through the code couples it to each platform and invites misuse.
- named-in: Yoder & Barcalow (PLoP 1997)
- tags: security, borderline — Layer-shaped; kept design-side as an in-application integration layer on the HAL/wrapper-facade precedent — Phase 3 may claim it upward

### secure-boot-image-verification — Secure Boot Image Verification
- aka: verified boot, authenticated boot, firmware signature verification, signed image check
- kind: robustness-security
- what: Before transferring control, the bootloader cryptographically verifies the next stage or application image against a trusted public key, refusing or falling back on failure.
- problem: A CRC (already in the index) only catches corruption; against malicious firmware replacement the boot stage must verify authenticity, anchoring each stage in the previous one.
- named-in: UEFI Specification (Secure Boot); Android Verified Boot documentation; embedded bootloader literature (e.g. MCUboot documentation)
- tags: security, embedded, crypto, borderline — The full chain-of-trust across stages is architecture; the in-bootloader verify-then-jump step is the in-process element (complements index entries bootloader-jump-handoff and a-b-firmware-image-update)

### secure-zeroization — Secure Zeroization
- aka: memset_s, explicit_bzero, sensitive-data scrubbing
- kind: robustness-security
- what: Erase sensitive data (keys, passwords) from memory using an operation the compiler cannot optimize away, immediately after last use.
- problem: Ordinary memset before free is dead-store-eliminated by optimizers, leaving secrets recoverable from memory dumps, swap, or reuse; guaranteed-erase primitives close the gap.
- named-in: corpus:certc — The CERT C Coding Standard, 2nd ed. - Seacord (2014)
- tags: c, security, cryptography, embedded

### security-session — Security Session
- aka: Session (Yoder & Barcalow), authenticated session object, session token (realization)
- kind: robustness-security
- what: An object holding an authenticated subject's identity and security attributes across a sequence of actions, so each request need not re-authenticate or re-derive permissions.
- problem: Distributing a user's security state across many interactions invites inconsistency and repeated credential handling; one session object localizes it and gives it a lifetime (timeout, invalidation).
- named-in: Yoder & Barcalow (PLoP 1997); Schumacher et al., Security Patterns (Wiley 2006, 'Security Session')
- tags: security, state

### single-access-point — Single Access Point
- aka: one entry point for security checks, login window (web/GUI realization)
- kind: robustness-security
- what: Route all entry into a program or module through one guarded entry point where identity and validity checks run before anything else executes.
- problem: Multiple scattered entrances make security checks inconsistent and individually bypassable; a single funnel makes the check set complete and auditable.
- named-in: Yoder & Barcalow, Architectural Patterns for Enabling Application Security (PLoP 1997); Schumacher et al., Security Patterns (Wiley 2006)
- tags: security, application-level

### smart-data — Smart Data
- aka: self-checking data, range-checked type
- kind: robustness-security
- what: Data types that carry their own validity metadata (ranges, units, CRC) and check every set/get operation, rejecting or flagging out-of-range values.
- problem: Plain C data accepts any bit pattern, so faults propagate silently; building the checks into the data type enforces validity at every touch point.
- named-in: corpus:douglasspatternsc — Design Patterns for Embedded Systems in C - Bruce Powel Douglass (2011)
- tags: c, embedded, safety

### stack-canary — Stack Canary
- aka: stack cookie, stack-smashing protector, StackGuard canary, stack protector, canary value, StackGuard
- kind: robustness-security
- what: Place a secret guard value between a stack frame's buffers and its control data (return address); verify it before returning, aborting if a buffer overflow overwrote it.
- problem: Stack buffer overflows silently overwrite return addresses, enabling control-flow hijack; a checked sentinel converts the overwrite into a detected crash.
- named-in: StackGuard: Automatic Adaptive Detection and Prevention of Buffer-Overflow Attacks - Cowan et al. (1998)
- tags: c, security, systems, compilers, embedded

### synchronizer-token — Synchronizer Token Pattern
- aka: anti-CSRF token, CSRF token, double-submit cookie (stateless variant)
- kind: robustness-security
- what: Embed a per-session (or per-request) unpredictable token in each legitimate form/request and verify it server-side, so cross-site forged requests lacking the token are rejected.
- problem: Browsers attach ambient credentials (cookies) to any request, letting a hostile page forge state-changing requests; a secret the attacker cannot read distinguishes genuine requests.
- named-in: OWASP Cross-Site Request Forgery Prevention Cheat Sheet ('Synchronizer Token Pattern')
- tags: security, web

### taint-checking — Taint Checking
- aka: taint mode, taint tracking, taint propagation, dynamic taint analysis
- kind: robustness-security
- what: Mark data from untrusted sources as tainted, propagate the mark through computations, and refuse (or flag) its use in sensitive sinks until it passes an explicit untainting step.
- problem: Manually tracking which values derive from untrusted input across a codebase fails silently; making trust a tracked property of the data enforces the source-to-sink discipline mechanically.
- named-in: Perl perlsec (taint mode); Ruby $SAFE taint (historical); Schwartz & Christiansen Perl literature; dynamic taint analysis literature (Newsome & Song 2005)
- tags: security, language-runtime, perl, ruby

### watchdog — Watchdog
- aka: watchdog timer, WDT, COP timer, computer operating properly timer, windowed watchdog (variant), software watchdog / task supervision (variant), watchdog kicking/petting, windowed watchdog, dead man's switch
- kind: robustness-security
- what: A hardware or software timer that must be periodically serviced ('kicked') by correctly running software; missing the deadline triggers reset or a safety action.
- problem: Hung, livelocked, or timing-broken software cannot report its own failure; an independent timer converts liveness violations into detectable, recoverable events.
- named-in: corpus:douglassrtcorpus — Real-Time Design Patterns - Bruce Powel Douglass (2002)
- tags: embedded, safety, real-time, robustness, c, fault-detection


## Communication — `communication` (43)

### acceptor-connector — Acceptor-Connector
- aka: —
- kind: communication
- what: Connection establishment and service initialization (acceptor for passive, connector for active roles) are decoupled from the service processing performed once a connection is established.
- problem: Connection setup logic changes independently of application service logic; separating them enables reuse of either and supports both synchronous and asynchronous establishment.
- named-in: corpus:posa2 — Pattern-Oriented Software Architecture Vol. 2: Patterns for Concurrent and Networked Objects - Schmidt, Stal, Rohnert, Buschmann (2000)
- tags: networking, sockets

### acknowledgement — Acknowledgement
- aka: ack, positive acknowledgement
- kind: communication
- what: The receiver of a message or request returns an explicit acknowledgement, letting the sender detect loss or peer failure via missing acks within a timeout.
- problem: Fire-and-forget communication gives the sender no way to know the peer is alive and the work arrived; acks piggyback failure detection onto normal traffic.
- named-in: corpus:hanmer — Patterns for Fault Tolerant Software - Hanmer (2007)
- tags: fault-detection, networking

### aggregator — Aggregator
- aka: —
- kind: communication
- what: A stateful component that collects correlated messages until a completeness condition holds, then publishes a single combined message.
- problem: Results that were split or produced in parallel must be recombined; the aggregator manages correlation, partial state, and completion/timeout rules.
- named-in: Enterprise Integration Patterns - Hohpe & Woolf (2003)
- tags: messaging

### bit-banging — Bit Banging
- aka: software-driven serial protocol, GPIO protocol emulation
- kind: communication
- what: Implement a communications protocol entirely in software by directly toggling and sampling GPIO pins with timed code, instead of using dedicated peripheral hardware.
- problem: The MCU lacks (or has run out of) hardware controllers for a needed protocol; software-timed pin manipulation trades CPU load and timing precision for hardware independence.
- named-in: Bit banging - Wikipedia
- tags: embedded, hardware-io

### callback — Callback
- aka: callback function, call-after function, delegate, handler registration
- kind: communication
- what: A piece of executable code (function pointer, closure, object method) passed to another component to be invoked later at a defined point, synchronously or asynchronously.
- problem: A library or lower layer must trigger caller-defined behavior without compile-time knowledge of it; passing the code in inverts control while keeping the layers decoupled.
- named-in: corpus:schreiner — Object-Oriented Programming with ANSI-C - Schreiner (1993/2011)
- tags: c, embedded, c++, borderline — Fundamental technique near the syntax floor, but named, recurring, and the basis of whole API styles - included.

### callback-with-context-pointer — Callback with Context Pointer
- aka: user-data pointer, void* context argument, closure emulation in C
- kind: communication
- what: Register a function pointer together with an opaque void* context that the callee passes back on invocation, giving the callback access to its state.
- problem: C function pointers carry no environment; the paired context pointer emulates closures so one callback implementation can serve many registered instances.
- named-in: corpus:hanson — Callback (computer programming) - Wikipedia; used pervasively in Hanson's C Interfaces and Implementations (closure 'cl' parameters)
- tags: c, embedded

### claim-check — Claim Check
- aka: reference-based messaging
- kind: communication
- what: Store a message's bulky payload in a shared data store and pass only a key (the claim check) through the channel; the consumer redeems the key to retrieve the data.
- problem: Large payloads clog channels and intermediate processors that only need headers; moving the body out of band keeps messages small without losing access to the full data.
- named-in: Enterprise Integration Patterns - Hohpe & Woolf (2003)
- tags: messaging

### client-dispatcher-server — Client-Dispatcher-Server
- aka: —
- kind: communication
- what: A dispatcher component sits between clients and servers, providing name-to-server resolution and connection establishment so clients request services by name only.
- problem: Clients should stay independent of server location and connection details; a level of indirection provides location transparency and late binding of services.
- named-in: Pattern-Oriented Software Architecture Vol. 1: A System of Patterns - Buschmann, Meunier, Rohnert, Sommerlad, Stal (1996)
- tags: ipc, networking, borderline — Distribution-flavored, but implementable as an in-process dispatcher/registry inside one program; POSA1 classes it as a design pattern.

### content-based-router — Content-Based Router
- aka: —
- kind: communication
- what: A router that examines message content and forwards each message to one of several output channels based on data-driven conditions.
- problem: Different messages in one stream must be handled by different processors; routing on content keeps senders ignorant of the receiver taxonomy.
- named-in: Enterprise Integration Patterns - Hohpe & Woolf (2003)
- tags: messaging

### correlation-identifier — Correlation Identifier
- aka: correlation id
- kind: communication
- what: A unique identifier stamped on a request message and copied into its reply so the requester can match responses to outstanding requests.
- problem: With asynchronous request handling, replies arrive out of order and interleaved; without a carried token the requester cannot tell which reply answers which request.
- named-in: Enterprise Integration Patterns - Hohpe & Woolf (2003)
- tags: messaging

### csp-channel — CSP Channel
- aka: channel, synchronous channel, Go channel, message channel (in-process)
- kind: communication
- what: A typed conduit through which concurrent processes communicate and synchronize by sending and receiving values, with rendezvous (unbuffered) or bounded-buffer semantics.
- problem: Threads need to exchange data and coordinate without exposing shared mutable state; making communication the synchronization ('share memory by communicating') removes explicit locking.
- named-in: Communicating Sequential Processes - Hoare (1978)
- tags: go, occam, rust, kotlin

### domain-event — Domain Event
- aka: —
- kind: communication
- what: A full-fledged domain object that represents something that happened in the domain, captured as an immutable record and used to trigger and decouple consequent behavior.
- problem: Side effects of a domain change otherwise get hard-wired into the code that makes the change; reifying the occurrence as an event decouples cause from consequences and creates an auditable history.
- named-in: Domain-Driven Design Reference - Eric Evans (2015)
- tags: ddd, domain-modeling, events

### event-aggregator — Event Aggregator
- aka: event bus, in-process publish-subscribe, in-process event bus
- kind: communication
- what: A single in-process object that registers for events from many sources and lets clients subscribe once with it, channeling and optionally generalizing all events to interested observers.
- problem: With many event sources, requiring each observer to find and register with every source explodes coupling and complicates observer lifetime management; a central aggregator makes registration one-stop and eases memory management of observers.
- named-in: Event Aggregator (martinfowler.com eaaDev) - Martin Fowler (2004)
- tags: eventing, ui, gui, oo

### event-delegation — Event Delegation
- aka: delegated event handling
- kind: communication
- what: Attaches a single event handler on a common ancestor and uses event bubbling plus target inspection to handle events for many (possibly dynamically created) descendant elements.
- problem: Registering one handler per element wastes memory and breaks for elements added after registration; one delegated handler on the ancestor covers all current and future descendants.
- named-in: Event delegation - javascript.info (The Modern JavaScript Tutorial)
- tags: ui, js

### event-driven-consumer — Event-Driven Consumer
- aka: asynchronous receiver
- kind: communication
- what: A consumer whose message-handling callback is invoked by the messaging layer as soon as a message arrives, rather than the consumer polling for it.
- problem: Polling wastes cycles and adds latency when messages are sporadic; inverting control lets messages be processed immediately with no busy-waiting.
- named-in: Enterprise Integration Patterns - Hohpe & Woolf (2003)
- tags: messaging

### forwarder-receiver — Forwarder-Receiver
- aka: —
- kind: communication
- what: Peers communicate through paired forwarder and receiver intermediaries that encapsulate marshaling, delivery mechanism, and endpoint mapping behind a simple send/receive interface.
- problem: Peer components need transparent inter-process communication without hard-coding the IPC mechanism, so the transport can be exchanged without touching peer logic.
- named-in: Pattern-Oriented Software Architecture Vol. 1: A System of Patterns - Buschmann, Meunier, Rohnert, Sommerlad, Stal (1996)
- tags: ipc, networking

### gateway — Gateway
- aka: —
- kind: communication
- what: An object that encapsulates access to an external system or resource behind an interface shaped for the application's needs.
- problem: External APIs are awkward, unstable, and hard to fake; wrapping them in a thin application-owned object keeps the awkwardness in one place and makes the boundary swappable for testing.
- named-in: Patterns of Enterprise Application Architecture - Martin Fowler (2002)
- tags: enterprise

### half-object-plus-protocol — Half-Object plus Protocol
- aka: HOPP
- kind: communication
- what: A logically single object is split into two coordinated half-objects, one per address space, each implementing the locally needed functionality, kept consistent by a private protocol between them.
- problem: An object is needed in two places at once (e.g. client and server) with low-latency local behavior on both sides; neither pure remote access nor full replication fits.
- named-in: Half-Object + Protocol - Gerard Meszaros, in Pattern Languages of Program Design (1995)
- tags: distribution, borderline — Distribution-motivated, but the mechanism is a concrete object-splitting design implementable within one codebase; POSA4 documents it as a design pattern.

### handshaking — Handshaking
- aka: can-you-handle-this signaling
- kind: communication
- what: Server and client cooperatively signal readiness before work is sent, letting the server refuse or defer new work when saturated.
- problem: Protocols that fire requests blindly (plain HTTP) give the server no way to say 'stop sending'; explicit readiness signaling lets components throttle their own load.
- named-in: corpus:nygard — Release It! Design and Deploy Production-Ready Software, 2nd ed. - Nygard (2018)
- tags: stability, networking

### hedged-request — Hedged Request
- aka: backup request, request hedging
- kind: communication
- what: After a brief delay (e.g. the 95th-percentile latency), send the same request to a second replica and use whichever response returns first, cancelling the other.
- problem: Tail latency of a fan-out is dominated by the slowest straggler; a small number of duplicate requests cuts tail latency dramatically for modest extra load.
- named-in: The Tail at Scale - Dean, Barroso (2013)
- tags: distributed, latency, borderline — Targets multi-replica distributed systems, but is a purely client-side implementable mechanism; kept per charter with tag.

### idempotent-receiver — Idempotent Receiver
- aka: idempotent consumer, idempotency key, message deduplication
- kind: communication
- what: A consumer designed so that processing the same message more than once has the same effect as processing it once, typically by tracking already-seen message identifiers.
- problem: At-least-once delivery and retry produce duplicates; making the receiver duplicate-safe is cheaper and more robust than trying to guarantee exactly-once transport.
- named-in: Enterprise Integration Patterns - Hohpe & Woolf (2003)
- tags: messaging, web, distributed

### interest-management — Interest Management
- aka: area-of-interest management, AoI filtering, relevance filtering, data distribution management (HLA DDM), scoping / ghost scoping (Tribes)
- kind: communication
- what: The replication layer filters which entities' state updates each connected client receives, matching entity 'update regions' against per-client interest expressions (typically spatial area-of-interest, visibility, or subscription predicates).
- problem: Broadcasting every entity update to every client scales as O(entities x clients) and explodes bandwidth; filtering to each client's relevant subset bounds per-connection traffic in large worlds.
- named-in: Morse, 'Interest Management in Large-Scale Distributed Simulations', UC Irvine ICS TR 96-27, 1996; HLA (IEEE 1516) Data Distribution Management; Frohnmayer & Gift, 'The TRIBES Engine Networking Model', GDC 2001 (scoping)
- tags: games, networking, simulation, borderline — Leans toward distributed-system scale, but passes the altitude test as a filtering mechanism implemented inside one server/replication component; the multi-federate infrastructure form (HLA RTI) is the architecture-side reading.

### mailbox — Mailbox
- aka: message mailbox, actor mailbox
- kind: communication
- what: A per-receiver message deposit point - in RTOS kernels a one-message (or small) exchange object a task pends on; in actor systems the queue holding all messages addressed to one actor.
- problem: A task or actor needs a private, addressable place where others can leave messages for it to consume on its own schedule, decoupling sender timing from receiver processing.
- named-in: corpus:labrosse — MicroC/OS-III: The Real-Time Kernel (and MicroC/OS-II message mailboxes) - Jean J. Labrosse (2009)
- tags: embedded, rtos, c, actor-model

### message — Message
- aka: command message, document message, event message
- kind: communication
- what: A discrete, self-contained packet of data (header plus body) exchanged between decoupled parts of a program through a channel rather than by direct call.
- problem: Two components need to exchange information without sharing call stacks, timing, or memory layout; packaging data as an addressable unit lets it be queued, routed, stored, and retried independently of sender and receiver.
- named-in: Enterprise Integration Patterns - Hohpe & Woolf (2003)
- tags: messaging

### message-dispatcher — Message Dispatcher
- aka: —
- kind: communication
- what: A single consumer that receives messages from a channel and distributes each to one of several performers (typically worker threads) it coordinates.
- problem: When consumers must not compete directly (ordering, channel limitations, or work-assignment logic), one dispatcher can centralize receipt and delegate processing while still exploiting parallelism.
- named-in: Enterprise Integration Patterns - Hohpe & Woolf (2003)
- tags: messaging, concurrency

### message-expiration — Message Expiration
- aka: message TTL, time-to-live
- kind: communication
- what: A timestamp or time-to-live stamped on a message after which the messaging layer or consumer treats it as stale and discards or dead-letters it instead of processing it.
- problem: Some data is only useful for a bounded time (quotes, sensor readings); expiration prevents consumers from acting on obsolete messages that queued up during delays.
- named-in: Enterprise Integration Patterns - Hohpe & Woolf (2003)
- tags: messaging

### message-filter — Message Filter
- aka: —
- kind: communication
- what: A routing component that inspects each incoming message and passes it on only if it meets specified criteria, silently discarding the rest.
- problem: A consumer receives a broader stream than it wants; filtering at the channel keeps unwanted traffic from reaching downstream logic.
- named-in: Enterprise Integration Patterns - Hohpe & Woolf (2003)
- tags: messaging

### message-queue — Message Queue
- aka: Queuing Pattern, message queue, point-to-point channel, FIFO message queue, event queue, event buffer
- kind: communication
- what: Tasks communicate by posting messages into a queue that the receiver drains at its own pace, sharing information asynchronously without sharing memory access timing.
- problem: Direct data sharing between concurrent tasks needs locking and couples their timing; queued messages decouple producer and consumer and serialize access naturally.
- named-in: corpus:douglasspatternsc — Design Patterns for Embedded Systems in C - Bruce Powel Douglass (2011)
- tags: embedded, concurrency, messaging, rtos, os

### nagle-s-algorithm — Nagle's Algorithm
- aka: small-packet avoidance, tinygram avoidance, TCP_NODELAY (disable knob)
- kind: communication
- what: Coalesce small outgoing writes by holding new small segments while any previously sent data remains unacknowledged, sending them as one larger segment when the ACK arrives.
- problem: Streams of tiny writes (keystrokes, RPC headers) generate one mostly-header packet each, congesting the network; self-clocked coalescing amortizes header overhead without a fixed timer. Interaction with delayed ACK and the TCP_CORK variant noted.
- named-in: RFC 896: Congestion Control in IP/TCP Internetworks - John Nagle (1984)
- tags: networking, tcp, borderline — Stack-internal in TCP, but the small-write-coalescing mechanism is named, recurring, and reimplemented in user protocol libraries - kept IN.

### observable-streams — Observable Streams
- aka: Rx Observable, reactive streams, event streams, observable sequences
- kind: communication
- what: An asynchronous push-based sequence abstraction: a producer pushes multiple values over time to subscribers, composable with declarative operators; the Reactive Streams specification adds demand-signalled flow control (backpressure).
- problem: Callback-based async event handling tangles composition, completion, and error propagation; observables extend the Observer pattern to sequences with uniform error/completion semantics, and backpressure keeps fast producers from overwhelming slow consumers (resilience-axis overlap noted).
- named-in: ReactiveX documentation - Introduction/Observable (reactivex.io)
- tags: ui, js, communication

### polling-consumer — Polling Consumer
- aka: synchronous receiver
- kind: communication
- what: A consumer that explicitly asks the channel for a message when it is ready to process one, blocking or returning empty if none is available.
- problem: The application must control when and at what rate messages are consumed (e.g., single-threaded loops, rate limiting); pull-based receipt keeps consumption on the consumer's schedule.
- named-in: Enterprise Integration Patterns - Hohpe & Woolf (2003)
- tags: messaging

### producer-consumer — Producer-Consumer
- aka: bounded buffer, producer-consumer queue
- kind: communication
- what: One or more producer threads place work items into a shared (usually bounded, blocking) queue from which one or more consumer threads remove and process them.
- problem: Producers and consumers run at different, varying rates; a shared buffer decouples them in time, smooths bursts, and bounds memory while coordinating handoff safely.
- named-in: Cooperating Sequential Processes - Dijkstra (1965)
- tags: embedded, servers

### publish-subscribe-channel — Publish-Subscribe Channel
- aka: pub-sub channel, topic
- kind: communication
- what: A channel that delivers a copy of each published message to every currently subscribed consumer instead of to a single receiver.
- problem: One event must reach an open-ended set of interested parties without the publisher knowing who they are; the channel handles fan-out so subscribers can be added or removed independently.
- named-in: Enterprise Integration Patterns - Hohpe & Woolf (2003)
- tags: messaging, borderline — Publish-subscribe as a system-wide architecture style is Phase 3 territory; this entry is the in-process/inter-thread channel mechanism (in-proc topics, broadcast queues).

### remote-procedure-call — Remote Procedure Call
- aka: RPC, Remote Method Call Pattern, remote method invocation
- kind: communication
- what: Invocations on a remote service are made through local stub/proxy machinery that marshals arguments, transmits, and unmarshals results so the call looks local.
- problem: Hand-rolled request/response messaging for every cross-node call is repetitive and error-prone; stub-generated call semantics standardize marshaling, dispatch, and error surfaces.
- named-in: Implementing Remote Procedure Calls - Birrell & Nelson (1984)
- tags: networking, distributed, borderline — Crosses process/system boundaries, but the stub/marshaling mechanism itself is implemented inside one component; the system topology built on it is Phase 3 territory.

### request-reply — Request-Reply
- aka: request-response
- kind: communication
- what: A two-message exchange in which a requester sends a message on one channel and the replier sends a response message back on another, layering call semantics over one-way messaging.
- problem: Messaging is inherently one-way, but many interactions need an answer; pairing a request channel with a reply channel restores the ask-and-answer conversation without blocking the transport.
- named-in: Enterprise Integration Patterns - Hohpe & Woolf (2003)
- tags: messaging

### return-address — Return Address
- aka: reply-to
- kind: communication
- what: A field in the request message telling the replier which channel to send the reply on.
- problem: A replier serving many requesters cannot hard-code where responses go; carrying the reply channel in the message lets each requester receive its own answers.
- named-in: Enterprise Integration Patterns - Hohpe & Woolf (2003)
- tags: messaging

### scatter-gather — Scatter-Gather
- aka: —
- kind: communication
- what: Broadcast a request to multiple recipients, then use an aggregator to collect and combine their replies into a single response message.
- problem: One question has several potential answerers (best quote, parallel sub-computations); fan-out plus reply aggregation gets all answers concurrently and reduces them to one result.
- named-in: Enterprise Integration Patterns - Hohpe & Woolf (2003)
- tags: messaging, borderline — Named for cross-system integration, but recurs as an in-process fan-out/fan-in composite (parallel dispatch + join); altitude-contested, kept IN.

### selective-consumer — Selective Consumer
- aka: message selector
- kind: communication
- what: A consumer that applies a selection predicate so it receives only the subset of a channel's messages it is interested in, leaving the rest for other consumers.
- problem: Several consumer types share one channel but each handles only certain messages; consumer-side selection avoids either exploding the channel count or processing-and-discarding.
- named-in: Enterprise Integration Patterns - Hohpe & Woolf (2003)
- tags: messaging

### shared-memory-communication — Shared Memory Communication
- aka: Shared Memory Pattern
- kind: communication
- what: Concurrent tasks or processors exchange data through a commonly addressable memory region, coordinated by locks, flags, or hardware semaphores.
- problem: Message passing copies data and adds latency; for high-bandwidth or multi-processor data exchange, a shared region is the cheapest channel - at the price of explicit synchronization.
- named-in: corpus:douglassrtcorpus — Real-Time Design Patterns - Bruce Powel Douglass (2002)
- tags: embedded, concurrency, borderline — Douglass files it under distribution patterns, but as an inter-task/inter-processor mechanism it is implementable inside one program and passes the altitude test.

### signals-and-slots — Signals and Slots
- aka: signal/slot mechanism
- kind: communication
- what: A type-safe callback mechanism where objects declare signals they emit and slots (member functions) that can be connected to any compatible signal, with the framework routing emissions to all connected slots.
- problem: Raw function-pointer callbacks are type-unsafe and couple caller to callee; signals/slots decouple emitter from receivers with checked signatures and many-to-many connections. Qt's canonical realization of Observer; also Boost.Signals2, GTK signals.
- named-in: Signals & Slots - Qt Documentation - The Qt Company
- tags: ui, c++, qt

### sliding-window-flow-control — Sliding Window Flow Control
- aka: sliding window protocol, window-based flow control, go-back-N, selective repeat
- kind: communication
- what: Sender and receiver agree on a window of unacknowledged data that may be in flight; acknowledgments slide the window forward, throttling the sender to the receiver's capacity.
- problem: Stop-and-wait wastes bandwidth on every round trip, while unlimited sending overruns the receiver; a sliding window pipelines transmission up to a negotiated bound and doubles as the receiver's backpressure signal. Go-back-N and selective repeat are retransmission variants folded here; silly-window-syndrome avoidance noted.
- named-in: TCP/IP Illustrated, Vol. 1: The Protocols - W. Richard Stevens (1994)
- tags: networking, protocols, embedded

### splitter — Splitter
- aka: —
- kind: communication
- what: A component that breaks a composite message into a series of individual messages, each processable on its own.
- problem: A single message containing repeating elements (an order with many line items) must be handled per element; splitting lets each part flow through the pipeline independently.
- named-in: Enterprise Integration Patterns - Hohpe & Woolf (2003)
- tags: messaging

### wire-tap — Wire Tap
- aka: —
- kind: communication
- what: A fixed component inserted into a channel that forwards each message unchanged to the main destination while also copying it to a secondary channel for inspection, logging, or analysis.
- problem: You need to observe traffic on a point-to-point channel (debugging, auditing) without disturbing the primary flow or modifying sender/receiver.
- named-in: Enterprise Integration Patterns - Hohpe & Woolf (2003)
- tags: messaging, borderline — Commonly deployed as integration infrastructure, but equally implementable inside one in-process pipeline; kept IN as an observation mechanism, altitude-contested.


## Scheduling & time — `scheduling-time` (25)

### cyclic-executive — Cyclic Executive
- aka: timeline scheduling, main-loop scheduler, frame-based executive, major/minor frame scheduling, Time-Triggered Cooperative Scheduler, TT scheduler, super-loop with timer tick
- kind: scheduling-time
- what: A fixed infinite loop that runs each task to completion in a predetermined order every cycle, with no preemption.
- problem: Small systems with stable, known task sets need utterly predictable, low-overhead scheduling without an RTOS.
- named-in: corpus:douglasspatternsc — Design Patterns for Embedded Systems in C - Bruce Powel Douglass (2011)
- tags: embedded, real-time, safety-critical, c

### deadline-propagation — Deadline Propagation
- aka: propagated deadlines, cascading timeout budget
- kind: scheduling-time
- what: Carry an absolute deadline (or remaining budget) with each request and pass it down the call chain; every stage checks it and aborts work whose deadline has already passed.
- problem: Independent per-hop timeouts let deep call chains do work the original caller has already abandoned; a propagated deadline stops wasted work everywhere at once.
- named-in: Site Reliability Engineering: How Google Runs Production Systems - Beyer, Jones, Petoff, Murphy eds. (2016)
- tags: distributed, grpc, borderline — Spans a call chain across services, but each hop implements it locally (check-and-forward); kept as design-level with tag.

### debouncing — Debouncing
- aka: debounce, switch debouncing, contact debouncing, de-glitching, switch debounce
- kind: scheduling-time
- what: Filtering the intermittent make/break bounce of mechanical inputs (or noisy edges generally) by accepting a state change only after it is stable for a defined interval.
- problem: Mechanical switches and noisy signals produce bursts of spurious transitions per actuation; naive edge handling registers many false events.
- named-in: corpus:douglasspatternsc — Design Patterns for Embedded Systems in C - Bruce Powel Douglass (2011)
- tags: embedded, hardware-access, hardware-io, ui, javascript, js

### deferrable-work — Deferrable Work
- aka: deferred non-critical processing
- kind: scheduling-time
- what: Classify work as essential vs deferrable and, under overload, postpone deferrable tasks (audits, housekeeping, statistics) until load subsides.
- problem: Under overload every cycle matters; explicitly deferring non-urgent work preserves capacity for revenue/critical processing without dropping it entirely.
- named-in: corpus:hanmer — Patterns for Fault Tolerant Software - Hanmer (2007)
- tags: overload, borderline — An overload policy inside one component; near operational policy but named and mechanically implementable (priority demotion, deferral queues).

### dynamic-priority-scheduling — Dynamic Priority Scheduling
- aka: earliest deadline first, EDF, Dynamic Priority Pattern, deadline scheduling
- kind: scheduling-time
- what: Task priorities are recomputed at runtime from urgency - classically earliest-deadline-first, where the task with the nearest deadline runs.
- problem: Fixed priorities cannot always achieve full utilization or handle aperiodic arrivals; deadline-driven priorities schedule optimally on one processor at the cost of predictability under overload.
- named-in: corpus:douglassrtcorpus — Real-Time Design Patterns - Bruce Powel Douglass (2002)
- tags: embedded, real-time, rtos

### fixed-timestep — Fixed Timestep
- aka: fixed time step, timestep accumulator loop, semi-fixed timestep (variant)
- kind: scheduling-time
- what: Advance the simulation in constant-size time increments driven by an accumulator of elapsed real time, decoupling the simulation rate from the (variable) render rate, typically with interpolation of the leftover fraction for display.
- problem: Variable delta-time updates make physics non-deterministic, unstable at low frame rates, and irreproducible; a fixed step gives determinism and stability while the accumulator keeps game time synchronized with wall-clock time.
- named-in: Fix Your Timestep! - Glenn Fiedler (Gaffer On Games, 2004)
- tags: games, physics

### governor — Governor
- aka: automation rate limiter
- kind: scheduling-time
- what: Cap the rate or scope of automated actions (restarts, scale-downs, config pushes) so automation cannot do damage faster than humans can react.
- problem: Automation acts at machine speed; a runaway control loop can destroy capacity in seconds, so its actuation rate is deliberately slowed like an engine governor.
- named-in: corpus:nygard — Release It! Design and Deploy Production-Ready Software, 2nd ed. - Nygard (2018)
- tags: stability, borderline — Governs ops automation, verging on operations tooling; kept as a named implementable rate-limiting mechanism from a pattern catalog.

### idle-task-hook — Idle Task Hook
- aka: idle hook, vApplicationIdleHook, idle callback, idle-time background processing
- kind: scheduling-time
- what: A user callback invoked repeatedly from the RTOS idle task (the lowest-priority always-ready task), used to run work that should consume only otherwise-idle cycles: low-power sleep entry, background self-tests, stack watermark checks.
- problem: Firmware has background work and power-management actions that must run only when nothing else is runnable, without a dedicated task or any interference with real-time work.
- named-in: corpus:freertosbook — freertos.org 'The Idle Task and the Idle Task Hook'; Mastering the FreeRTOS Real-Time Kernel; uC/OS-II OSTaskIdleHook
- tags: embedded, rtos, borderline — arguably just a registered callback (hook method) into the scheduler; kept because idle-context background processing is a named, recurring firmware mechanism across RTOSes (FreeRTOS idle hook, Zephyr idle thread, uC/OS idle hook) with distinct constraints (must not block)

### interrupt-coalescing — Interrupt Coalescing
- aka: interrupt moderation, interrupt throttling, interrupt blanking, interrupt mitigation
- kind: scheduling-time
- what: Hold back events that would each raise an interrupt until a count threshold or timeout is reached, then deliver one interrupt for the whole batch.
- problem: Per-event interrupts under high event rates (e.g. NIC packet arrival) swamp the CPU with context switches; batching trades a bounded latency increase for an order-of-magnitude drop in interrupt load. NAPI-style hybrid interrupt/polling is the software realization folded here.
- named-in: Interrupt coalescing - Wikipedia (live)
- tags: embedded, networking, os-kernel, drivers

### leaky-bucket — Leaky Bucket
- aka: leaky bucket algorithm, traffic shaper queue, leaky bucket as a meter/queue
- kind: scheduling-time
- what: Arriving work enters a bounded bucket that drains at a constant rate; overflow is rejected, converting bursty input into a smooth constant-rate output.
- problem: Downstream stages that cannot absorb bursts need arrival smoothing; the bucket enforces a hard output rate regardless of input burstiness. Distinct from Hanmer's Leaky Bucket Counter (error counting).
- named-in: New Directions in Communications (or Which Way to the Information Age?) - Turner (1986)
- tags: networking, rate-limiting, qos

### round-robin-scheduling — Round Robin Scheduling
- aka: time-slicing
- kind: scheduling-time
- what: The scheduler grants each ready task a turn (optionally a fixed time slice) in rotating order, giving fairness rather than urgency-driven preference.
- problem: When tasks have comparable importance and no hard deadlines, fair progress for all is preferable to priority starvation.
- named-in: corpus:douglassrtcorpus — Real-Time Design Patterns - Bruce Powel Douglass (2002)
- tags: embedded, os

### sandwich-delay — Sandwich Delay
- aka: fixed-duration code section, jitter-equalizing delay
- kind: scheduling-time
- what: Wrap a code section between a hardware-timer start and a wait-for-timer end so the section always consumes the same wall-clock duration regardless of path taken.
- problem: Variable execution paths introduce task jitter that degrades time-triggered control and sampling quality; padding every path to a fixed duration with a timer equalizes timing.
- named-in: Meeting Real-Time Constraints Using 'Sandwich Delays' - Pont, Kurian & Bautista (EuroPLoP 2006)
- tags: embedded, real-time, jitter

### schedule-table — Schedule Table
- aka: time-triggered schedule table, OSEKtime dispatch table, AUTOSAR schedule table
- kind: scheduling-time
- what: A statically configured table of expiry points on a counter, each releasing tasks or setting events at fixed offsets, cyclically or once, as an OS-level time-triggered dispatch mechanism.
- problem: Periodic activations with precise relative phasing are clumsy to build from individual alarms; a schedule table expresses the whole time-triggered activation pattern declaratively and synchronizably (e.g. to a global time base).
- named-in: AUTOSAR Specification of Operating System (schedule tables); OSEK/VDX time-triggered OS
- tags: embedded, real-time, automotive

### scheduler — Scheduler
- aka: —
- kind: scheduling-time
- what: An object that explicitly sequences waiting threads' access to a resource according to a scheduling policy (FIFO, priority, deadline) instead of leaving the order to the lock implementation.
- problem: When the order in which contending threads proceed matters (fairness, priorities, deadlines), the policy must be lifted out of the lock and made an explicit, pluggable decision.
- named-in: Patterns in Java, Volume 1: A Catalog of Reusable Design Patterns Illustrated with UML - Grand (1998)
- tags: java, spot-checked-wikipedia-concurrency-pattern-list

### software-timer — Software Timer
- aka: RTOS timer, kernel timer, timer object, one-shot timer / auto-reload (periodic) timer, timer service task / timer daemon
- kind: scheduling-time
- what: Kernel facility multiplexing many logical one-shot or auto-reload callback timers onto a single hardware tick/timer, with expiry callbacks typically executed by a timer-service (daemon) task rather than in interrupt context.
- problem: Applications need many independent timed callbacks but hardware timers are scarce; a software timer layer provides unlimited cheap timers without dedicating a hardware timer or a task per delay.
- named-in: corpus:freertosbook — Mastering the FreeRTOS Real-Time Kernel (software timers chapter)
- tags: embedded, rtos, borderline — decision logged: index has timer-wheel, but that is an implementation data structure for large timer populations; the RTOS software-timer kernel facility (one-shot/auto-reload objects + timer daemon) is the mechanism designers name and reach for, so a separate element is warranted

### static-priority-scheduling — Static Priority Scheduling
- aka: fixed-priority preemptive scheduling, rate-monotonic priority assignment, Rate-Monotonic Scheduling, RMS, rate-monotonic analysis, RMA
- kind: scheduling-time
- what: Tasks receive fixed, design-time priorities and a preemptive scheduler always runs the highest-priority ready task; rate-monotonic assignment (priority by period) is the classic policy.
- problem: Concurrent tasks with different urgencies must meet deadlines; fixed priorities give analyzable, predictable preemption behavior.
- named-in: corpus:douglasspatternsc — Design Patterns for Embedded Systems in C - Bruce Powel Douglass (2011)
- tags: embedded, real-time, rtos

### system-tick — System Tick
- aka: tick interrupt, RTOS tick, SysTick, kernel tick, tick counter, tick time base, jiffies (Linux)
- kind: scheduling-time
- what: A periodic timer interrupt increments a monotonic tick counter that serves as the system's software time base, driving timekeeping, timeouts, and scheduler preemption decisions.
- problem: Bare-metal and RTOS code needs a cheap, uniform notion of elapsed time without dedicating a hardware timer per consumer; a single periodic tick gives every timeout, delay, software timer, and time-slice decision one shared clock.
- named-in: white
- tags: e, m, b, e, d, d, e, d, ,,  , r, t, o, s, ,,  , b, a, r, e, -, m, e, t, a, l, ;,  , t, h, e,  , m, e, c, h, a, n, i, s, m,  , t, i, c, k, l, e, s, s, -, i, d, l, e,  , (, a, l, r, e, a, d, y,  , c, a, t, a, l, o, g, e, d, ),  , s, u, p, p, r, e, s, s, e, s,  , a, n, d,  , s, c, h, e, d, u, l, e, r, s,  , l, i, k, e,  , t, h, e,  , T, T, C,  , s, c, h, e, d, u, l, e, r,  , c, o, n, s, u, m, e,  , —,  , t, h, e,  , t, i, c, k,  , t, i, m, e,  , b, a, s, e,  , i, t, s, e, l, f,  , w, a, s,  , t, h, e,  , m, i, s, s, i, n, g,  , e, l, e, m, e, n, t

### throttle — Throttle
- aka: throttling, function rate limiting, rate limiting (of handlers)
- kind: scheduling-time
- what: Ensure a function or action executes at most once per interval, discarding or coalescing invocations that arrive faster.
- problem: High-frequency event streams (scroll, sensor readings, status updates) would trigger expensive handlers far faster than useful; throttling caps the execution rate while keeping periodic updates.
- named-in: Debouncing and Throttling Explained Through Examples - Corbacho, CSS-Tricks (2016)
- tags: javascript, ui, embedded, js

### tickless-idle — Tickless Idle
- aka: tickless kernel, dynamic tick suppression
- kind: scheduling-time
- what: Suppress the periodic scheduler tick during idle, program a one-shot wakeup for the next deadline, and sleep the CPU in a low-power mode until then.
- problem: A free-running tick interrupt wakes the CPU pointlessly and dominates power draw in mostly-idle systems; eliminating idle ticks lets the MCU stay in deep sleep between real events.
- named-in: corpus:freertosbook — Mastering the FreeRTOS Real-Time Kernel (tickless idle mode)
- tags: embedded, low-power, rtos

### time-to-live-ttl — Time to Live (TTL)
- aka: expiry, expiration timestamp, hop limit
- kind: scheduling-time
- what: Attach a lifetime to a datum, message, or entry; holders treat it as invalid (and evict or drop it) once the lifetime elapses.
- problem: Stale cache entries, undead packets, and orphaned records need a self-destruct mechanism that works without coordination; a carried lifetime bounds staleness and loops.
- named-in: RFC 791: Internet Protocol - Postel (1981)
- tags: networking, caching, borderline — Often just a protocol field or config knob; kept for the recurring in-program expiry mechanism (cache TTLs, message expiry, session lifetime).

### time-triggered-co-operative-scheduler — Time-Triggered Co-operative Scheduler
- aka: TTC scheduler, cooperative scheduler, tick-driven task scheduler, time-triggered hybrid scheduler (TTH variant)
- kind: scheduling-time
- what: Dispatch short run-to-completion tasks from a timer-tick-driven table at fixed periods and offsets, with no preemption between tasks.
- problem: Preemptive kernels bring race conditions and jitter that are hard to certify; a cooperative tick-driven dispatcher gives highly predictable timing provided every task's duration stays under the tick. Pont's hybrid (TTH) variant, allowing one preemptive task, is folded here.
- named-in: corpus:pont — Patterns for Time-Triggered Embedded Systems - Pont (2001)
- tags: embedded, c, real-time

### timer-wheel — Timer Wheel
- aka: timing wheel, hashed timing wheel, hierarchical timing wheel
- kind: scheduling-time
- what: A circular array of time slots, each holding the timers expiring in that tick; a pointer advances per tick, making start/stop/expire O(1) for large timer populations.
- problem: Sorted timer lists degrade with tens of thousands of pending timeouts (protocol stacks, event systems); the wheel bounds per-tick work regardless of timer count. Hashed/hierarchical forms are variants, not separate elements.
- named-in: Hashed and Hierarchical Timing Wheels: Data Structures for the Efficient Implementation of a Timer Facility - Varghese, Lauck (1987)
- tags: networking, os, embedded

### token-bucket — Token Bucket
- aka: token bucket filter, committed rate limiting, committed access rate
- kind: scheduling-time
- what: Tokens accrue in a bucket at a fixed rate up to a capacity; each admitted unit of work consumes tokens, allowing bursts up to the bucket size while enforcing a long-term average rate.
- problem: Pure fixed-rate policing forbids legitimate bursts; the bucket capacity encodes an allowed burst while still bounding sustained throughput.
- named-in: Computer Networks, 3rd ed. - Tanenbaum (1996)
- tags: networking, rate-limiting, qos, overlap:robustness-scout

### update-method — Update Method
- aka: update function, tick method
- kind: scheduling-time
- what: Simulate a collection of independent objects by giving each an update() method that the game loop calls once per frame, letting each object advance its own behavior one step at a time.
- problem: Many active entities must appear to behave concurrently; per-frame incremental updates avoid one object monopolizing control while keeping each object's behavior encapsulated.
- named-in: Game Programming Patterns - Robert Nystrom (2014)
- tags: games

### work-stealing — Work Stealing
- aka: work-stealing scheduler, stealing deques
- kind: scheduling-time
- what: Each worker keeps its own deque of tasks and, when idle, steals tasks from the tail of other workers' deques, balancing load with minimal contention.
- problem: A single shared task queue becomes a contention bottleneck and balances load poorly for fine-grained, dynamically spawned tasks; per-worker deques with stealing keep processors busy cheaply.
- named-in: Scheduling Multithreaded Computations by Work Stealing - Blumofe, Leiserson (1999)
- tags: java, cilk, rust


## OO design patterns — `oo-patterns` (65)

### abstract-factory — Abstract Factory
- aka: Kit
- kind: oo-patterns
- what: An interface for creating families of related or dependent objects without specifying their concrete classes.
- problem: A system must be independent of how its products are created and composed, and must work with any of several families of related products while keeping the family members consistent with each other.
- named-in: corpus:gof — Design Patterns: Elements of Reusable Object-Oriented Software - Gamma, Helm, Johnson, Vlissides (1994)
- tags: creational

### abstract-session — Abstract Session
- aka: session object (per-client service state), service access point object
- kind: oo-patterns
- what: A server object hands each client an opaque session object encapsulating the per-client state of their conversation; the client makes further requests through the session rather than the server, with full type safety.
- problem: A service serving many clients must keep per-client state without exposing its internals or forcing clients to pass identity/state tokens on every call (the untyped-handle alternative).
- named-in: Pryce, 'Abstract Session: An Object Structural Pattern', PLoPD4 (2000) (PLoPD4 ToC loaded live; c2 AbstractSessionPattern page exists)
- tags: structural, sockets-style APIs, in-process sessions

### acyclic-visitor — Acyclic Visitor
- aka: —
- kind: oo-patterns
- what: A Visitor variant that breaks the dependency cycle between the element hierarchy and the visitor by using a degenerate base visitor plus per-element visitor interfaces and a runtime cast.
- problem: Classic GoF Visitor couples every visitor to every element class, forcing full recompilation when elements change; the acyclic form allows partial visitors and incremental growth.
- named-in: Acyclic Visitor - Robert C. Martin, in Pattern Languages of Program Design 3 (1998)
- tags: oo, cpp

### adapter — Adapter
- aka: Wrapper (GoF alias, shared with Decorator)
- kind: oo-patterns
- what: Converts the interface of a class into another interface clients expect, letting classes with incompatible interfaces work together.
- problem: An existing class has useful behavior but its interface does not match the one a client or framework requires, and the class cannot or should not be modified.
- named-in: corpus:gof — Design Patterns: Elements of Reusable Object-Oriented Software - Gamma, Helm, Johnson, Vlissides (1994)
- tags: structural

### bridge — Bridge
- aka: Handle/Body, Pimpl, compilation firewall, Cheshire Cat, pointer to implementation
- kind: oo-patterns
- what: Decouples an abstraction from its implementation so the two can vary independently, via a handle object delegating to an implementor hierarchy.
- problem: A permanent binding between abstraction and implementation (via inheritance) makes both hard to extend and combine; both dimensions need to evolve and be selected independently, possibly at run time.
- named-in: corpus:gof — Design Patterns: Elements of Reusable Object-Oriented Software - Gamma, Helm, Johnson, Vlissides (1994)
- tags: structural, c++

### builder — Builder
- aka: —
- kind: oo-patterns
- what: Separates the construction of a complex object from its representation so the same construction process can create different representations.
- problem: The algorithm for creating a complex object should be independent of the parts that make up the object and how they are assembled, and construction must allow different representations of what is built.
- named-in: corpus:gof — Design Patterns: Elements of Reusable Object-Oriented Software - Gamma, Helm, Johnson, Vlissides (1994)
- tags: creational

### bureaucracy — Bureaucracy
- aka: hierarchical control compound pattern
- kind: oo-patterns
- what: A compound pattern composing Composite, Mediator, Chain of Responsibility, and Observer to build self-maintaining hierarchical structures where each level mediates its children and escalates requests upward.
- problem: Hierarchies (documents, GUIs, organizations) must maintain internal consistency and route interactions across levels without external coordination logic.
- named-in: Riehle, 'Bureaucracy', PLoPD3 (1997) (PLoPD3 ToC loaded live)
- tags: compound-pattern, borderline — Compound of four patterns already in the index; kept as an independently named, published composite mechanism.

### chain-of-responsibility — Chain of Responsibility
- aka: —
- kind: oo-patterns
- what: Passes a request along a chain of candidate handler objects until one handles it, decoupling sender from receiver.
- problem: More than one object may handle a request and the handler is not known a priori; the sender should not be coupled to a specific receiver, and the set of handlers should be configurable dynamically.
- named-in: corpus:gof — Design Patterns: Elements of Reusable Object-Oriented Software - Gamma, Helm, Johnson, Vlissides (1994)
- tags: behavioral

### collecting-parameter — Collecting Parameter
- aka: —
- kind: oo-patterns
- what: Pass a collecting object through a series of methods, each of which adds its partial results to it, instead of composing return values.
- problem: Building a compound result (a report, an aggregate collection) across many methods via return values forces awkward merging; a shared collector accumulates in place.
- named-in: Smalltalk Best Practice Patterns - Kent Beck (1997)
- tags: smalltalk, oo, borderline — Micro-scale code-organization pattern; included because it is named in a canonical catalog and recurs across codebases.

### command — Command
- aka: Action, Transaction
- kind: oo-patterns
- what: Encapsulates a request as an object, letting requests be parameterized, queued, logged, and undone.
- problem: The invoker of an operation (button, menu, scheduler) must not know the operation or its receiver; requests need to be first-class values to support queuing, macro recording, and undo/redo.
- named-in: corpus:gof — Design Patterns: Elements of Reusable Object-Oriented Software - Gamma, Helm, Johnson, Vlissides (1994)
- tags: behavioral, games, gof-revisit

### command-processor — Command Processor
- aka: —
- kind: oo-patterns
- what: A dedicated processor component manages user requests reified as command objects: it schedules, executes, logs, and stores them, enabling undo/redo and macro services.
- problem: Applications need flexible, decoupled handling of requests plus request-level services (undo, logging, scheduling, macros) that the request initiators should not implement themselves.
- named-in: Pattern-Oriented Software Architecture Vol. 1: A System of Patterns - Buschmann, Meunier, Rohnert, Sommerlad, Stal (1996)
- tags: behavioral, ui

### component — Component
- aka: entity component
- kind: oo-patterns
- what: Split a single entity's state and behavior across multiple component objects, one per domain (physics, rendering, AI, input), which the entity aggregates.
- problem: A monolithic entity class couples every domain together and deep inheritance hierarchies cannot express cross-cutting combinations; composition of per-domain components keeps domains isolated and entities configurable.
- named-in: Game Programming Patterns - Robert Nystrom (2014)
- tags: games

### composite — Composite
- aka: —
- kind: oo-patterns
- what: Composes objects into tree structures representing part-whole hierarchies, letting clients treat individual objects and compositions uniformly.
- problem: Clients must handle both primitive objects and containers of objects; distinguishing them everywhere complicates the code, so a common interface over leaves and composites is needed.
- named-in: corpus:gof — Design Patterns: Elements of Reusable Object-Oriented Software - Gamma, Helm, Johnson, Vlissides (1994)
- tags: structural

### curiously-recurring-template-pattern-crtp — Curiously Recurring Template Pattern (CRTP)
- aka: static polymorphism idiom, F-bound polymorphism (theory name), CRTP, mixin from below, compile-time polymorphism, template-based polymorphism
- kind: oo-patterns
- what: A class derives from a template instantiated with itself, letting the base call derived-class members at compile time.
- problem: Provides polymorphic-style reuse and interface injection without virtual dispatch cost; the related Barton-Nackman trick is a historical application.
- named-in: Curiously Recurring Template Patterns - Coplien (C++ Report, 1995)
- tags: c++, embedded

### decorator — Decorator
- aka: Wrapper (GoF alias, shared with Adapter)
- kind: oo-patterns
- what: Attaches additional responsibilities to an object dynamically by wrapping it in an object with the same interface that forwards and augments requests.
- problem: Responsibilities should be addable and removable per object at run time; extending by subclassing is static and explodes combinatorially when features must be mixed freely.
- named-in: corpus:gof — Design Patterns: Elements of Reusable Object-Oriented Software - Gamma, Helm, Johnson, Vlissides (1994)
- tags: structural

### delegation — Delegation
- aka: object composition forwarding
- kind: oo-patterns
- what: An object handles a request by forwarding it to a helper object (the delegate), optionally passing itself so the delegate can refer back to the original receiver.
- problem: Behavior reuse without inheritance: composition plus forwarding lets behavior be chosen and changed at runtime and shared across unrelated classes.
- named-in: Using Prototypical Objects to Implement Shared Behavior in Object-Oriented Systems - Henry Lieberman (OOPSLA 1986); discussed as a reuse mechanism in GoF
- tags: oo, borderline — Fundamental technique rather than a discrete pattern; included because it is named, recurring, and catalogued (Wikipedia structural list, GoF).

### domain-service — Domain Service
- aka: Service (DDD)
- kind: oo-patterns
- what: A stateless operation in the domain layer, defined by what it does rather than what it is, for domain logic that does not naturally belong to any entity or value object.
- problem: Forcing an operation that spans several domain objects into one of them distorts the model; a named stateless service keeps the operation in the ubiquitous language without inventing an artificial owner.
- named-in: Domain-Driven Design: Tackling Complexity in the Heart of Software - Eric Evans (2003)
- tags: ddd, domain-modeling

### double-dispatch — Double Dispatch
- aka: —
- kind: oo-patterns
- what: A technique where the operation executed depends on the runtime types of two receivers, implemented by a pair of single dispatches (each object virtual-calls into the other).
- problem: Single-dispatch languages select behavior on one receiver only; interactions like collide(shapeA, shapeB) or Visitor's element/visitor pairing need selection on two types.
- named-in: A Simple Technique for Handling Multiple Polymorphism - Daniel H. H. Ingalls (OOPSLA 1986); mechanism underlying GoF Visitor
- tags: oo

### envelope-letter — Envelope-Letter
- aka: —
- kind: oo-patterns
- what: A handle/body variant where the envelope (handle) and letters (bodies) share a common base class, letting the letter's dynamic type change at runtime behind a stable envelope.
- problem: Allows an object to change its apparent class (e.g. number types promoting, state changes) while clients hold a value-semantics handle.
- named-in: Advanced C++: Programming Styles and Idioms - James O. Coplien (1992)
- tags: c++

### extension-object — Extension Object
- aka: extension interface (POSA2 relative)
- kind: oo-patterns
- what: Let clients ask an object for an extension implementing a specific interface (getExtension(type)), so new interfaces can be added to a class family without changing its core.
- problem: Unanticipated clients need new operations on existing abstractions; extensions attach role-specific interfaces without bloating the base class or breaking existing clients.
- named-in: Extension Object - Erich Gamma, in Pattern Languages of Program Design 3 (1998)
- tags: oo

### external-polymorphism — External Polymorphism
- aka: adapter-based polymorphism
- kind: oo-patterns
- what: Make unrelated concrete classes (possibly without virtual functions or a common base) polymorphic by wrapping them in a parallel adapter hierarchy defined outside the classes.
- problem: Third-party or performance-critical classes cannot be modified to join an inheritance hierarchy; external polymorphism adds dynamic dispatch non-intrusively and underlies modern type erasure.
- named-in: External Polymorphism - Cleeland, Schmidt & Harrison (PLoP 1996)
- tags: c++

### facade — Facade
- aka: —
- kind: oo-patterns
- what: Provides a unified, higher-level interface to a set of interfaces in a subsystem, making the subsystem easier to use.
- problem: Clients become coupled to many classes of a complex subsystem; a single simplified entry point reduces coupling and shields clients from subsystem internals without forbidding direct access.
- named-in: corpus:gof — Design Patterns: Elements of Reusable Object-Oriented Software - Gamma, Helm, Johnson, Vlissides (1994)
- tags: structural

### factory-method — Factory Method
- aka: Virtual Constructor
- kind: oo-patterns
- what: Defines an interface for creating an object but lets subclasses decide which class to instantiate, deferring instantiation to subclasses.
- problem: A class cannot anticipate the class of objects it must create; it wants its subclasses (or clients) to specify the concrete product while keeping the creation call site generic.
- named-in: corpus:gof — Design Patterns: Elements of Reusable Object-Oriented Software - Gamma, Helm, Johnson, Vlissides (1994)
- tags: creational

### flyweight — Flyweight
- aka: —
- kind: oo-patterns
- what: Uses sharing to support large numbers of fine-grained objects efficiently by factoring state into shared intrinsic and externally supplied extrinsic parts.
- problem: An application needs huge numbers of small objects whose storage cost is prohibitive; most of their state can be shared or moved outside, making shared instances feasible.
- named-in: corpus:gof — Design Patterns: Elements of Reusable Object-Oriented Software - Gamma, Helm, Johnson, Vlissides (1994)
- tags: structural, memory, games, gof-revisit

### function-pointer-dispatch-table — Function Pointer Dispatch Table
- aka: dispatch table, jump table, branch table, Dynamic Interface (Fluent C), pointer-to-function array
- kind: oo-patterns
- what: An indexed or keyed table of function pointers replaces switch/if chains: look up the handler, then call it.
- problem: Large multiway branches are slow to extend and error-prone; a table makes dispatch data-driven, O(1), and extensible (also the substrate for state machines and command interpreters).
- named-in: corpus:kandr — The C Programming Language, 2nd ed. - Kernighan & Ritchie (1988), sec. 5.11 pointers to functions
- tags: c, embedded

### hook-method — Hook Method
- aka: hook operation, hot spot method
- kind: oo-patterns
- what: A method deliberately left empty or with default behavior at a designed extension point, which subclasses or clients override to inject custom behavior into a fixed skeleton.
- problem: Frameworks and template algorithms need designated points of planned variability; hooks let extenders customize behavior without touching the invariant control flow.
- named-in: Meta Patterns - A Means for Capturing the Essentials of Reusable Object-Oriented Design - Wolfgang Pree (ECOOP 1994); 'hook operations' in GoF Template Method
- tags: oo, borderline — Fold-vs-separate decision: kept separate from Template Method because hook methods recur outside it (framework hot spots, lifecycle hooks, event hooks); logged per charter.

### interceptor — Interceptor
- aka: —
- kind: oo-patterns
- what: A framework exposes dispatch points where registered interceptor objects are invoked automatically on framework-internal events, letting services be added transparently via callbacks and context objects.
- problem: Frameworks must be extensible with out-of-band services (logging, security, monitoring) after deployment without changing framework or application code.
- named-in: corpus:posa2 — Pattern-Oriented Software Architecture Vol. 2: Patterns for Concurrent and Networked Objects - Schmidt, Stal, Rohnert, Buschmann (2000)
- tags: framework, extensibility

### interpreter — Interpreter
- aka: —
- kind: oo-patterns
- what: Given a language, defines a class per grammar rule and an interpret operation over the resulting abstract syntax tree to evaluate sentences of the language.
- problem: A recurring class of problems is best expressed as sentences in a simple language; representing the grammar as an object structure makes the language easy to implement, extend, and evaluate.
- named-in: corpus:gof — Design Patterns: Elements of Reusable Object-Oriented Software - Gamma, Helm, Johnson, Vlissides (1994)
- tags: behavioral, languages

### iterator — Iterator
- aka: Cursor, database cursor, scrollable cursor, result-set iterator, cursor iterator
- kind: oo-patterns
- what: Provides a way to access the elements of an aggregate object sequentially without exposing its underlying representation.
- problem: Clients need to traverse collections of different internal structure uniformly, possibly with multiple simultaneous or specialized traversals, without bloating the aggregate's interface.
- named-in: corpus:gof — Design Patterns: Elements of Reusable Object-Oriented Software - Gamma, Helm, Johnson, Vlissides (1994)
- tags: behavioral, db, api, sql, c, c++

### layer-supertype — Layer Supertype
- aka: —
- kind: oo-patterns
- what: A common superclass for all types in a layer, holding the behavior every member of that layer shares.
- problem: Every domain object or every mapper repeats the same boilerplate (id handling, common hooks); hoisting it into one per-layer base class removes the duplication.
- named-in: Patterns of Enterprise Application Architecture - Martin Fowler (2002)
- tags: enterprise

### mapper — Mapper
- aka: —
- kind: oo-patterns
- what: An object that sets up communication between two independent subsystems that must remain ignorant of each other.
- problem: Two subsystems need to exchange data without either taking a dependency on the other; a third-party object owned by neither performs the transfer and isolates the coupling.
- named-in: Patterns of Enterprise Application Architecture - Martin Fowler (2002)
- tags: enterprise

### marker-interface — Marker Interface
- aka: tag interface, marker annotation (successor form), tagging interface
- kind: oo-patterns
- what: An empty interface whose only purpose is to tag implementing classes with a compile-time-checkable property (Serializable, Cloneable).
- problem: Some type-level properties carry no operations but must be testable and enforceable by the type system; the marker makes membership a static type.
- named-in: Effective Java - Joshua Bloch (3rd ed., Item 41)
- tags: java

### mediator — Mediator
- aka: —
- kind: oo-patterns
- what: Defines an object that encapsulates how a set of objects interact, so colleagues refer only to the mediator instead of to each other.
- problem: A set of objects communicate in well-defined but complex ways; the many-to-many interconnections make the objects hard to reuse or vary independently, so the interaction logic is centralized.
- named-in: corpus:gof — Design Patterns: Elements of Reusable Object-Oriented Software - Gamma, Helm, Johnson, Vlissides (1994)
- tags: behavioral

### memento — Memento
- aka: Token
- kind: oo-patterns
- what: Captures and externalizes an object's internal state, without violating encapsulation, so the object can be restored to that state later.
- problem: Undo/rollback requires snapshots of an object's state, but exposing the state publicly would break encapsulation; a memento gives the originator alone full access to the saved state.
- named-in: corpus:gof — Design Patterns: Elements of Reusable Object-Oriented Software - Gamma, Helm, Johnson, Vlissides (1994)
- tags: behavioral

### mixin — Mixin
- aka: mixin class, parameterized base class (C++ realization), flavors (historical)
- kind: oo-patterns
- what: A small class providing one slice of behavior that is composed into other classes by inheritance (in C++ typically by inheriting from a template parameter) rather than used standalone.
- problem: Cross-cutting behaviors (counting, serialization, non-copyability) would otherwise be duplicated across unrelated hierarchies; mixins make them composable units.
- named-in: Mixin-Based Inheritance - Gilad Bracha & William Cook (OOPSLA 1990; term from Lisp Flavors, Moon 1986)
- tags: c++, python, ruby, scala

### monostate — Monostate
- aka: Borg pattern (Python)
- kind: oo-patterns
- what: A class whose every instance shares the same state by declaring all fields static, so construction is unrestricted but behavior is singleton-like.
- problem: Singleton's single-instance enforcement leaks into client code; Monostate gives shared-state semantics behind an ordinary class interface, swappable and subclassable.
- named-in: Agile Software Development: Principles, Patterns, and Practices - Robert C. Martin (2002); originally Ball & Crawford
- tags: oo, cpp, python

### multiton — Multiton
- aka: registry of singletons
- kind: oo-patterns
- what: A class that manages a map of named instances of itself, guaranteeing exactly one instance per key.
- problem: Singleton generalized: a system needs a controlled, globally accessible set of instances keyed by identity (one per database, one per device) rather than one total.
- named-in: Multiton pattern - Wikipedia (software design pattern list, creational)
- tags: oo

### non-virtual-interface-nvi — Non-Virtual Interface (NVI)
- aka: template method idiom for C++, public non-virtual, private virtual
- kind: oo-patterns
- what: Public interface functions are non-virtual and delegate to private/protected virtual hooks that derived classes override.
- problem: Separates the interface contract (invariants, pre/postconditions, instrumentation) from the customization points, keeping base-class control over how overrides are invoked.
- named-in: Virtuality - Herb Sutter, C/C++ Users Journal (2001)
- tags: c++

### null-object — Null Object
- aka: Active Nothing
- kind: oo-patterns
- what: A do-nothing implementation of an interface stands in for 'no object', so clients invoke it uniformly without null checks.
- problem: Scattered null/None checks clutter client code and invite omission errors; representing absence as a polymorphic object removes the special case.
- named-in: Null Object - Bobby Woolf, in Pattern Languages of Program Design 3 (1998; PLoP 1996)
- tags: behavioral, oo, c, embedded

### object-orientation-in-c — Object Orientation in C
- aka: inheritance by structure extension, dynamic linkage, vtable in C, generic functions via function pointers
- kind: oo-patterns
- what: Encapsulation, inheritance, and polymorphism realized in plain C via struct embedding, per-class function-pointer tables, and first-member upcasting.
- problem: Reusing OO design vocabulary (class hierarchies, dynamic dispatch, delegates) in C codebases and kernels where C++ is unavailable or disallowed.
- named-in: corpus:schreiner — Object-Oriented Programming with ANSI-C - Schreiner (1993/2011)
- tags: c, embedded, borderline — A coherent cluster of mechanisms (struct embedding + vtables + dynamic type checks) cataloged as one element; splitting is a Phase-1 merge decision.

### object-recursion — Object Recursion
- aka: recursive delegation over polymorphic structure
- kind: oo-patterns
- what: Distribute the handling of a request recursively over a polymorphic object structure: each recurser handles its part and delegates the remainder to its successor(s) until terminator objects stop the recursion.
- problem: A request must be processed piecewise along a linked/hierarchical structure; centralizing the traversal in one loop couples it to the structure, while polymorphic recursion keeps each node's contribution local.
- named-in: Woolf, 'The Object Recursion Pattern', PLoPD4 (2000) (PLoPD4 ToC loaded live)
- tags: structural, borderline — Generalizes the traversal shared by Composite, Decorator, Chain of Responsibility and Interpreter (all in index); kept because it is independently named and distinguishes handle-vs-forward semantics.

### observer — Observer
- aka: Dependents, Publish-Subscribe, Publisher-Subscriber, Pub-Sub, listener, publish-subscribe (in-process)
- kind: oo-patterns
- what: Defines a one-to-many dependency between objects so that when one object changes state, all its dependents are notified and updated automatically.
- problem: Multiple objects must stay consistent with one subject's state without the subject being coupled to their concrete classes or their number being fixed.
- named-in: corpus:gof — Design Patterns: Elements of Reusable Object-Oriented Software - Gamma, Helm, Johnson, Vlissides (1994)
- tags: behavioral, events, games, gof-revisit

### oo-in-c-via-explicit-vtable — OO in C via Explicit Vtable
- aka: virtual function table in C, class emulation in C, poor man's objects
- kind: oo-patterns
- what: Structs of function pointers (shared per 'class', pointed to by each instance) plus first-argument self pointers implement classes, inheritance, and dynamic dispatch in C.
- problem: C lacks language-level polymorphism; the explicit vtable brings substitutable implementations to drivers, OS interfaces, and embedded frameworks.
- named-in: corpus:schreiner — Object-Oriented Programming with ANSI-C - Axel-Tobias Schreiner (1993/2011)
- tags: c, embedded, os

### pluggable-selector — Pluggable Selector
- aka: pluggable behavior (umbrella), pluggable block (closure variant), stored method selector
- kind: oo-patterns
- what: Store the name (selector) of a method in an instance variable and dispatch on it reflectively, so instances of one class exhibit different behavior without subclassing.
- problem: A family of trivially differing subclasses (each overriding one small method) is overkill; parameterizing instances by a stored selector collapses the hierarchy.
- named-in: Beck, Smalltalk Best Practice Patterns (1997)
- tags: smalltalk, reflection, also used in xUnit test-method dispatch

### policy-based-design — Policy-Based Design
- aka: policy classes, policies
- kind: oo-patterns
- what: Assemble a class's behavior from small orthogonal 'policy' template parameters, each supplying one aspect (allocation, threading, checking).
- problem: Monolithic classes cannot cover the combinatorial space of design choices; policies let users compose exactly the variant they need at compile time with no runtime cost.
- named-in: Modern C++ Design - Andrei Alexandrescu (2001)
- tags: c++

### private-class-data — Private Class Data
- aka: —
- kind: oo-patterns
- what: Move a class's state into a separate data object initialized once at construction, exposing it to the main class only through read access.
- problem: Write access to fields after construction invites unintended mutation; separating the data class enforces initialize-then-read-only discipline structurally.
- named-in: Private Class Data - SourceMaking design patterns catalog (structural)
- tags: oo

### prototype — Prototype
- aka: clone, Virtual Constructor (C++ clone idiom usage)
- kind: oo-patterns
- what: Specifies the kinds of objects to create using a prototypical instance and creates new objects by copying (cloning) this prototype.
- problem: A system should be independent of how its products are created when the classes to instantiate are specified at run time, or when building a class hierarchy of factories parallel to the product hierarchy is too costly.
- named-in: corpus:gof — Design Patterns: Elements of Reusable Object-Oriented Software - Gamma, Helm, Johnson, Vlissides (1994)
- tags: creational, games, gof-revisit

### proxy — Proxy
- aka: Surrogate, Virtual Proxy, Remote Proxy, Protection Proxy, Counting Proxy, Lazy Acquisition, Lazy Initialization, Lazy Load, ghost, value holder, lazy instantiation, initialization-on-demand holder idiom (Java)
- kind: oo-patterns
- what: Provides a surrogate or placeholder object that controls access to another object, standing in with the same interface.
- problem: Direct access to an object is undesirable or impossible - it may be remote, expensive to create, or need access control - so a stand-in mediates creation, access, or communication (remote, virtual, protection proxies).
- named-in: corpus:gof — Design Patterns: Elements of Reusable Object-Oriented Software - Gamma, Helm, Johnson, Vlissides (1994)
- tags: structural, startup, embedded, enterprise, orm, java

### registry — Registry
- aka: —
- kind: oo-patterns
- what: A well-known object that other objects use to find common objects and services, typically via static or thread-scoped accessors.
- problem: Some widely needed objects (connections, configuration, current session) cannot sensibly be threaded through every call chain; a known lookup point provides access while keeping scope (process, thread, session) explicit.
- named-in: Patterns of Enterprise Application Architecture - Martin Fowler (2002)
- tags: enterprise

### role-object — Role Object
- aka: —
- kind: oo-patterns
- what: Adapt a core object to different client contexts by attaching and detaching role objects at runtime, each role extending the core's interface for one context.
- problem: One domain object (Customer) is viewed differently by many subsystems; subclassing per view explodes and freezes the combination at compile time, while roles compose dynamically.
- named-in: The Role Object Pattern - Dirk Baeumer, Dirk Riehle, Wolf Siberski, Martina Wulf (PLoP 1997)
- tags: oo

### separated-interface — Separated Interface
- aka: —
- kind: oo-patterns
- what: Defines an interface in a separate package from its implementation so clients depend only on the interface package.
- problem: A client package must call functionality whose implementation it should not depend on (to break cycles or invert a dependency); placing the interface with the client and the implementation elsewhere reverses the compile-time dependency.
- named-in: Patterns of Enterprise Application Architecture - Martin Fowler (2002)
- tags: enterprise

### servant — Servant
- aka: —
- kind: oo-patterns
- what: A helper class that provides a common behavior (e.g., movement, printing) to a group of otherwise unrelated classes, which are passed to the servant as parameters.
- problem: A behavior is needed by many classes that share no useful ancestor; centralizing it in a servant avoids duplicating the implementation in each class.
- named-in: Servant (design pattern) - Wikipedia (software design pattern list, behavioral)
- tags: oo, borderline — Thin catalog presence outside Wikipedia; mechanism overlaps plain utility/strategy composition - included per charter with the honest tag.

### singleton — Singleton
- aka: —
- kind: oo-patterns
- what: Ensures a class has only one instance and provides a global point of access to it.
- problem: Exactly one instance of a class is needed (a single shared resource or registry) and it must be accessible from a well-known access point while remaining extensible by subclassing.
- named-in: corpus:gof — Design Patterns: Elements of Reusable Object-Oriented Software - Gamma, Helm, Johnson, Vlissides (1994)
- tags: creational, games, gof-revisit

### special-case — Special Case
- aka: —
- kind: oo-patterns
- what: A subclass that provides special behavior for particular cases (missing customer, unknown value), returned in place of null or an error code.
- problem: Callers otherwise repeat the same null/edge-case checks everywhere; a polymorphic special-case object answers the common protocol with safe defaults, removing conditional clutter (Null Object is the best-known instance).
- named-in: Patterns of Enterprise Application Architecture - Martin Fowler (2002)
- tags: enterprise

### specification — Specification
- aka: specification object
- kind: oo-patterns
- what: Encapsulates a business rule as a separate predicate object that can test candidates for satisfaction and be combined with other specifications via and/or/not.
- problem: Selection, validation, and construction criteria otherwise get duplicated and buried in queries and conditionals; reifying the criterion as a combinable object lets one rule serve all three uses.
- named-in: Specifications - Eric Evans & Martin Fowler (1997)
- tags: ddd, domain-modeling, oo

### sponsor-selector — Sponsor-Selector
- aka: sponsor/selector triad
- kind: oo-patterns
- what: Separate three responsibilities — sponsors that know when a resource is useful, a selector that picks among sponsors' recommendations, and the client that uses the chosen resource — to select the best resource dynamically.
- problem: A system must choose the best of a dynamically changing set of resources/strategies without hard-coding selection knowledge into the client.
- named-in: Wallingford, 'Sponsor-Selector: A Pattern Language for Choosing the Best Resource', PLoPD3 (1997) (cs.uni.edu/~wallingf/patterns/sponsor-selector.html verified)
- tags: dynamic-selection, AI-systems-origin

### state — State
- aka: Objects for States
- kind: oo-patterns
- what: Lets an object alter its behavior when its internal state changes by delegating state-dependent behavior to interchangeable state objects.
- problem: An object's behavior depends on its state and changes at run time; large multi-way conditionals on state constants scatter the state logic, so each state becomes its own class.
- named-in: corpus:gof — Design Patterns: Elements of Reusable Object-Oriented Software - Gamma, Helm, Johnson, Vlissides (1994)
- tags: behavioral, games, gof-revisit

### strategy — Strategy
- aka: Policy
- kind: oo-patterns
- what: Defines a family of algorithms, encapsulates each one behind a common interface, and makes them interchangeable within the client that uses them.
- problem: A class needs one of many variants of an algorithm; hardwiring the variants or exposing them via conditionals couples clients to the algorithms and prevents run-time selection.
- named-in: corpus:gof — Design Patterns: Elements of Reusable Object-Oriented Software - Gamma, Helm, Johnson, Vlissides (1994)
- tags: behavioral

### subclass-sandbox — Subclass Sandbox
- aka: —
- kind: oo-patterns
- what: A base class defines an abstract sandbox method and a suite of protected operations; subclasses implement their behavior by combining only those provided operations.
- problem: Many similar subclasses (e.g. dozens of superpowers) would each couple to many game systems; funneling all their behavior through base-class primitives confines coupling to one place.
- named-in: Game Programming Patterns - Robert Nystrom (2014)
- tags: games

### template-method — Template Method
- aka: —
- kind: oo-patterns
- what: Defines the skeleton of an algorithm in a base-class operation, deferring specific steps to subclass hook methods without changing the algorithm's structure.
- problem: Several classes share an algorithm's invariant structure but differ in individual steps; the invariant part should be implemented once, with the variant steps overridable.
- named-in: corpus:gof — Design Patterns: Elements of Reusable Object-Oriented Software - Gamma, Helm, Johnson, Vlissides (1994)
- tags: behavioral

### twin — Twin
- aka: —
- kind: oo-patterns
- what: Model multiple inheritance in a single-inheritance language by splitting one conceptual object into two closely coupled partner objects, each subclassing one parent and holding a reference to its twin.
- problem: Languages like Java forbid inheriting from two classes; the twin pair simulates the combined subtype while avoiding the diamond problem.
- named-in: Twin - A Design Pattern for Modelling Multiple Inheritance - Hannes Moessenboeck (Johannes Kepler University Linz)
- tags: java, oo

### type-object — Type Object
- aka: power type
- kind: oo-patterns
- what: Represent a category of things as an ordinary runtime object (the type object) that instances hold a reference to, instead of as a compile-time class.
- problem: New kinds of entities (monster breeds, item types) must be definable in data without recompiling or growing a class hierarchy; type-as-data makes kinds authorable and shareable at runtime.
- named-in: Game Programming Patterns - Robert Nystrom (2014)
- tags: games, data-driven, oo

### view-handler — View Handler
- aka: —
- kind: oo-patterns
- what: A view handler component manages all views of an application: it opens, coordinates, tiles, clones, updates, and closes them through a uniform view interface.
- problem: Multi-view applications need centralized, extensible management of view lifecycle and inter-view coordination instead of scattering it across the views.
- named-in: Pattern-Oriented Software Architecture Vol. 1: A System of Patterns - Buschmann, Meunier, Rohnert, Sommerlad, Stal (1996)
- tags: ui

### visitor — Visitor
- aka: —
- kind: oo-patterns
- what: Represents an operation to be performed on the elements of an object structure as a separate visitor object, letting new operations be added without changing the element classes (double dispatch).
- problem: Many distinct, unrelated operations must be performed over a stable object structure of heterogeneous classes; embedding every operation in every class pollutes the classes and scatters each operation.
- named-in: corpus:gof — Design Patterns: Elements of Reusable Object-Oriented Software - Gamma, Helm, Johnson, Vlissides (1994)
- tags: behavioral

### whole-part — Whole-Part
- aka: Composite Aggregate, Part-Whole Hierarchy
- kind: oo-patterns
- what: An aggregate component (the Whole) encapsulates constituent Part objects, organizes their collaboration, and is the sole access point to their combined functionality.
- problem: Clients need to treat an assembly of cooperating objects as a single semantic unit without depending on, or bypassing, its internal parts.
- named-in: Pattern-Oriented Software Architecture Vol. 1: A System of Patterns - Buschmann, Meunier, Rohnert, Sommerlad, Stal (1996)
- tags: structural


## Construction & API shape — `construction-api` (29)

### aggregate-instance — Aggregate Instance
- aka: return struct by value, parameter/result object in C
- kind: construction-api
- what: Bundle multiple related values into a struct and pass/return that aggregate by value instead of using several out-parameters.
- problem: Returning multiple related data items through separate pointers scatters the contract; the aggregate makes the data relationship explicit and copyable.
- named-in: corpus:preschern — Fluent C - Christopher Preschern (2022)
- tags: c

### batch-method — Batch Method
- aka: —
- kind: construction-api
- what: An interface method operates on a whole set of elements per call (bulk get/set) rather than requiring one call per element.
- problem: Element-at-a-time access across an expensive boundary (locks, IPC, network) multiplies overhead; batching amortizes the boundary cost over many elements.
- named-in: Pattern-Oriented Software Architecture Vol. 4: A Pattern Language for Distributed Computing - Buschmann, Henney, Schmidt (2007)
- tags: api-design, performance

### combined-method — Combined Method
- aka: —
- kind: construction-api
- what: Operations that clients commonly invoke as a sequence are combined into a single interface method executed as one unit (e.g. put-if-absent, open-and-read).
- problem: Call sequences across an interface boundary are non-atomic under concurrency and costly over process boundaries; combining them restores atomicity and cuts round trips.
- named-in: Pattern-Oriented Software Architecture Vol. 4: A Pattern Language for Distributed Computing - Buschmann, Henney, Schmidt (2007)
- tags: concurrency, api-design

### construct-on-first-use — Construct On First Use
- aka: Meyers singleton, function-local static, lazy static initialization
- kind: construction-api
- what: Access a static object only through a function that holds it as a function-local static, so it is constructed on the first call.
- problem: Avoids the static initialization order fiasco by making initialization demand-driven; since C++11 the construction is also thread-safe.
- named-in: More C++ Idioms - Wikibooks (living); popularized by the C++ FAQ (Cline) and Effective C++ (Meyers)
- tags: c++

### dependency-injection — Dependency Injection
- aka: DI, constructor injection, setter injection, interface injection
- kind: construction-api
- what: An assembler supplies a component's dependencies from outside (via constructor, setter, or interface) instead of the component constructing or locating them itself.
- problem: Components that instantiate their own collaborators are hard-wired to concrete classes, untestable in isolation, and unconfigurable; injection moves the wiring decision out of the component.
- named-in: Inversion of Control Containers and the Dependency Injection pattern - Fowler (2004)
- tags: oo, c, c++

### design-by-contract — Design by Contract
- aka: contracts, preconditions/postconditions/invariants, programming by contract
- kind: construction-api
- what: Specify each routine's obligations as executable preconditions, postconditions, and class invariants, checked at runtime, with blame assigned by which side's clause failed.
- problem: Informal interface expectations cause misuse and blur responsibility for failures; executable contracts document, verify, and localize violations at the boundary where they occur.
- named-in: Object-Oriented Software Construction - Meyer (1988)
- tags: eiffel, correctness

### embedded-domain-specific-language — Embedded Domain-Specific Language
- aka: EDSL, internal DSL, domain-specific embedded language
- kind: construction-api
- what: A domain-specific vocabulary implemented as a library within a host language, reusing the host's syntax, types, and tooling instead of a separate parser.
- problem: Gives domain experts a notation close to their problem while inheriting the host language's abstraction, checking, and ecosystem - no separate compiler to build or maintain.
- named-in: Building Domain-Specific Embedded Languages - Paul Hudak (ACM Computing Surveys, 1996)
- tags: fp, haskell, scala, borderline — Umbrella technique spanning many concrete idioms (fluent interfaces, combinator libraries, tagless final); kept because the name and canonical source are established and the mechanism is in-program.

### enumeration-method — Enumeration Method
- aka: Internal Iterator, Callback Iterator (Fluent C)
- kind: construction-api
- what: A collection owner exposes a method that applies a client-supplied operation to each element internally, instead of handing out an external iterator.
- problem: External iteration leaks collection structure and is unsafe under concurrent modification; internalizing the loop keeps traversal control, locking, and structure encapsulated.
- named-in: Pattern-Oriented Software Architecture Vol. 4: A Pattern Language for Distributed Computing - Buschmann, Henney, Schmidt (2007)
- tags: collections, functional

### explicit-interface — Explicit Interface
- aka: —
- kind: construction-api
- what: A component's usage contract is captured in an interface type explicitly separated from any implementation class, so clients depend only on the declared interface.
- problem: Clients coupled to concrete classes inhibit substitution, testing, and evolution; reifying the interface as a first-class artifact decouples contract from realization.
- named-in: Explicit Interface and Object Manager: Two Patterns from a Pattern Language for Distributed Computing - Buschmann, Henney, Schmidt (EuroPLoP 2003)
- tags: component, borderline — Close to the 'program to an interface' design principle, but published as a named pattern with concrete structure; included per over-inclusion rule.

### expression-builder — Expression Builder
- aka: —
- kind: construction-api
- what: An object, or family of objects, that provides a fluent interface layered over a normal command-query API, translating chained expression-style calls into calls on the underlying objects.
- problem: Putting fluent methods directly on domain objects pollutes their command-query API and couples them to one DSL syntax; a separate builder layer isolates the fluent facade so the domain API stays conventional and multiple fluent syntaxes can coexist.
- named-in: Fowler, Domain-Specific Languages (Addison-Wesley, 2010), ch. 32; martinfowler.com/dslCatalog ('An object, or family of objects, that provides a fluent interface over a normal command-query API', verified live 2026-07-10)
- tags: i, n, t, e, r, n, a, l,  , D, S, L, s, ;,  , d, i, s, t, i, n, c, t,  , f, r, o, m,  , f, l, u, e, n, t, -, i, n, t, e, r, f, a, c, e,  , (, t, h, e,  , s, t, y, l, e, ),  , —,  , t, h, i, s,  , i, s,  , t, h, e,  , d, e, d, i, c, a, t, e, d,  , b, u, i, l, d, e, r,  , o, b, j, e, c, t,  , t, h, a, t,  , c, a, r, r, i, e, s,  , t, h, e,  , s, t, y, l, e, ;,  , c, o, m, p, o, s, e, s,  , w, i, t, h,  , b, u, i, l, d, e, r,  , a, n, d,  , m, e, t, h, o, d,  , c, h, a, i, n, i, n, g

### extension-interface — Extension Interface
- aka: —
- kind: construction-api
- what: A component exports multiple role-specific interfaces reachable through a root interface (QueryInterface-style), rather than one ever-growing interface.
- problem: Prevents interface bloat and client breakage when components evolve new capabilities; clients depend only on the interface roles they use.
- named-in: corpus:posa2 — Pattern-Oriented Software Architecture Vol. 2: Patterns for Concurrent and Networked Objects - Schmidt, Stal, Rohnert, Buschmann (2000)
- tags: com, component

### facade-backend-module-pattern — Facade/Backend Module Pattern
- aka: pw facade pattern, link-time facade, compile-time facade
- kind: construction-api
- what: A module exposes a fixed facade API whose backend implementation is selected at build/link time per target platform.
- problem: Portable embedded code needs per-platform implementations behind one interface without runtime indirection cost; the seam is moved to the build.
- named-in: corpus:pigweedsdk — Pigweed SDK documentation (living)
- tags: c++, embedded, borderline — Half build-system convention, half design pattern - effectively link-time dependency injection; included with the ops flavor noted.

### fluent-interface — Fluent Interface
- aka: fluent API, method chaining (enabling technique)
- kind: construction-api
- what: An API designed so chained method calls read like flowing prose, building configuration or computation as an internal domain-specific language.
- problem: Constructing complex objects or requests through many setters is verbose and hides intent; designing return values for chaining makes multi-step construction readable and self-documenting.
- named-in: FluentInterface, martinfowler.com bliki - Martin Fowler & Eric Evans (2005)
- tags: api-design, oo

### function-control — Function Control
- aka: control parameter, flag argument, mode parameter
- kind: construction-api
- what: Add a data parameter (enum, flag, mode value) to a function that selects which of several behaviors the function performs, letting one API entry point cover a family of variants without passing function pointers.
- problem: An API needs caller-selectable behavior variation but a full callback/dynamic interface is overkill; a control parameter keeps the interface small at the cost of coupling the caller to a behavior selector.
- named-in: corpus:preschern — Fluent C ch. 6, 'Flexible APIs' (Preschern 2022)
- tags: c, borderline — API-shape mechanism near the syntax floor; the same construct is cataloged as the 'flag argument' smell by Fowler - included as the named Fluent C mechanism with that tension recorded

### functional-options — Functional Options
- aka: functional options pattern, self-referential functions as options, option functions, self-referential functions and options (Pike)
- kind: construction-api
- what: A constructor takes a variadic list of option functions, each of which mutates the value being configured; options are first-class values that can be composed, defaulted, and added without breaking callers.
- problem: Constructors with many optional parameters degenerate into config structs or telescoping overloads; closures-as-options keep the zero-option case clean and the API forward-compatible.
- named-in: Pike, Self-referential functions and the design of options (commandcenter blog, 2014); Cheney, Functional options for friendly APIs (dave.cheney.net / dotGo, 2014)
- tags: go

### hardware-abstraction-layer — Hardware Abstraction Layer
- aka: HAL, driver abstraction interface, MCU peripheral abstraction
- kind: construction-api
- what: A stable set of interfaces that isolates application and middleware code from register-level hardware detail, so the same firmware runs across MCUs by swapping the layer beneath.
- problem: Register-level code welds the application to one chip; a defined abstraction boundary makes firmware portable, testable off-target, and reusable across product lines.
- named-in: corpus:beningofw — Reusable Firmware Development: A Practical Approach to APIs, HALs and Drivers - Beningo (2017)
- tags: embedded, c, borderline — Layering shades toward architecture; kept IN as an implementable interface construct within one firmware program, with the layered-firmware-architecture reading parked for Phase 3.

### immediate-mode-gui — Immediate-Mode GUI
- aka: IMGUI, immediate mode (graphics API)
- kind: construction-api
- what: A GUI API style where user code re-declares the widgets to draw every frame inside the input/render loop (DoButton() each frame rather than CreateButton() once), with the library retaining little or no widget object state.
- problem: Retained widget trees force state duplication between application data and widget objects and constant synchronization; immediate mode derives the UI from application state each frame, eliminating the sync problem at the cost of per-frame re-specification. Coined by Casey Muratori (2002); Dear ImGui and Nuklear are canonical implementations.
- named-in: Immediate mode (computer graphics) - Wikipedia; Immediate-Mode Graphical User Interfaces - Casey Muratori (2005)
- tags: ui, games, borderline — API/state paradigm rather than a single mechanism, but named, recurring, and implementable inside one component - IN per altitude test.

### introspective-interface — Introspective Interface
- aka: —
- kind: construction-api
- what: A component offers a separate interface through which clients can query metadata about its capabilities, properties, and configuration at runtime.
- problem: Generic clients (tools, containers, scripting layers) must discover what a component can do without compile-time knowledge of its concrete type.
- named-in: Pattern-Oriented Software Architecture Vol. 4: A Pattern Language for Distributed Computing - Buschmann, Henney, Schmidt (2007)
- tags: reflection, component

### lifecycle-callback — Lifecycle Callback
- aka: Lifecycle Hooks
- kind: construction-api
- what: A framework or container invokes designated component methods at defined lifecycle transitions (initialize, activate, passivate, destroy), inverting control of lifecycle handling.
- problem: Components hosted by a runtime must react to lifecycle events they do not drive; standardized callbacks let the host manage many heterogeneous components uniformly.
- named-in: Pattern-Oriented Software Architecture Vol. 4: A Pattern Language for Distributed Computing - Buschmann, Henney, Schmidt (2007)
- tags: framework, inversion-of-control

### named-parameter-idiom — Named Parameter Idiom
- aka: method chaining for parameters, named parameters via proxy object
- kind: construction-api
- what: Replace long positional parameter lists with a parameter object whose chained setter calls name each argument, passed to the real function.
- problem: Calls with many defaulted positional arguments are unreadable and error-prone in languages without named arguments; the idiom simulates them.
- named-in: More C++ Idioms - Wikibooks (living); classical C++ FAQ (Cline) entry
- tags: c++

### nifty-counter — Nifty Counter
- aka: Schwarz counter
- kind: construction-api
- what: A per-translation-unit static counter object ensures a shared static resource (e.g. std::cout) is initialized before first use and destroyed after last use across translation units.
- problem: C++ gives no cross-translation-unit ordering for static initialization (the static initialization order fiasco); the counter forces correct init/teardown ordering.
- named-in: More C++ Idioms - Wikibooks (living)
- tags: c++

### out-parameters — Out-Parameters
- aka: output arguments, result via pointer parameter
- kind: construction-api
- what: Return data by writing through caller-supplied pointers, keeping the return value free for status.
- problem: C functions return a single value; out-parameters deliver multiple results while preserving the status-code channel.
- named-in: corpus:preschern — Fluent C - Christopher Preschern (2022)
- tags: c

### plugin — Plugin
- aka: —
- kind: construction-api
- what: Links classes to an abstraction during configuration rather than compilation, so behavior is selected per deployment via configuration.
- problem: Behavior that varies by environment (id generation, tax rules, test doubles) should not require recompiling or littering code with conditionals; a configuration-time linkage point centralizes the substitution.
- named-in: Patterns of Enterprise Application Architecture - Martin Fowler (2002)
- tags: enterprise

### product-trader — Product Trader
- aka: creation by specification
- kind: construction-api
- what: Clients create objects by naming an abstract product class plus a specification; a trader maps specifications to concrete product classes and performs the instantiation.
- problem: Direct constructor calls couple clients to concrete classes; a trader decouples client from product, easing configuration and evolution of class hierarchies and frameworks.
- named-in: Baeumer & Riehle, 'Product Trader', PLoPD3 (1997) (riehle.org paper page and PLoPD3 ToC loaded live)
- tags: creational, framework-design

### retained-mode-gui — Retained-Mode GUI
- aka: retained mode, scene-graph GUI
- kind: construction-api
- what: A GUI/graphics API style where the library retains a persistent object model of the scene (widget tree/scene graph) that client code creates once and mutates, with the library handling redraws from the retained model.
- problem: Re-specifying the whole UI every frame is wasteful for mostly-static interfaces; retaining the scene lets the library optimize redraw, hit-testing, and accessibility, at the cost of keeping the retained model in sync with application state. Historically the dominant GUI style.
- named-in: Retained mode - Wikipedia
- tags: ui, borderline — The dominant default paradigm; cataloged for contrast with immediate mode - arguably ambient rather than a reached-for element.

### service-locator — Service Locator
- aka: service registry (in-process)
- kind: construction-api
- what: Provide a global access point to a service through a locator that resolves the concrete provider at runtime, hiding both the provider's class and the lookup process.
- problem: Code all over the codebase needs a service (audio, logging) without coupling to a concrete implementation or passing it everywhere; the locator centralizes binding and allows swapping providers (including null services) at runtime.
- named-in: Core J2EE Patterns: Best Practices and Design Strategies - Alur, Crupi, Malks (2001)
- tags: games, java, oo

### smart-constructor — Smart Constructor
- aka: validating constructor function
- kind: construction-api
- what: A function that is the only exported way to build a value of an abstract type, performing validation or normalization so every constructed value satisfies the type's invariants.
- problem: Guarantees invariants at the construction boundary - hiding the raw data constructor makes invalid values unrepresentable to the rest of the program.
- named-in: Smart constructors - Haskell wiki (haskell.org)
- tags: fp, haskell, rust, scala

### static-factory-method — Static Factory Method
- aka: named constructor (C++ analog), valueOf/of/from conventions
- kind: construction-api
- what: A public static method returns instances instead of a public constructor, allowing naming, caching, subtype return, and non-instantiation.
- problem: Constructors cannot be named, cannot return cached or covariant instances, and always allocate; static factories decouple 'get an instance' from 'construct an object' (distinct from GoF Factory Method).
- named-in: Effective Java - Joshua Bloch (2001; 3rd ed. 2018, Item 1)
- tags: java, c++, csharp

### wrapper-facade — Wrapper Facade
- aka: —
- kind: construction-api
- what: Concise, cohesive, type-safe class interfaces encapsulate low-level, non-portable system APIs (sockets, threads, mutexes) and their associated data.
- problem: Programming directly against low-level C-style OS APIs is verbose, error-prone, and non-portable; wrapping them yields robustness and portability without significant overhead.
- named-in: corpus:posa2 — Pattern-Oriented Software Architecture Vol. 2: Patterns for Concurrent and Networked Objects - Schmidt, Stal, Rohnert, Buschmann (2000)
- tags: c++, systems, portability


## Functional & type-level idioms — `functional-type-idioms` (26)

### collection-pipeline — Collection Pipeline
- aka: method chaining over collections, streams pipeline, LINQ pipeline
- kind: functional-type-idioms
- what: Organizes a computation as a sequence of operations (filter, map, reduce, and kin) each taking a collection from the previous stage and feeding one to the next.
- problem: Imperative loops with accumulating temporaries obscure the data transformation being performed; composing named collection operations expresses the transformation as a readable, refactorable pipeline.
- named-in: Collection Pipeline, martinfowler.com - Martin Fowler (2015)
- tags: functional, fp, java, csharp, javascript

### continuation-passing-style — Continuation-Passing Style
- aka: CPS, callback-passing style
- kind: functional-type-idioms
- what: Writing functions to take an explicit continuation - a callback receiving the result - instead of returning, making control flow a first-class value.
- problem: Reifies 'what happens next' so programs can implement early exit, backtracking, coroutines, and asynchronous flows in a language without those control features.
- named-in: Compiling with Continuations - Andrew W. Appel (1992)
- tags: fp, scheme, javascript

### copied-value — Copied Value
- aka: Value Object (copy semantics)
- kind: functional-type-idioms
- what: Value-typed objects are passed and stored by copy, so each holder owns an independent instance and mutation cannot cause aliasing surprises.
- problem: Sharing mutable value-like objects by reference invites unintended interference between holders and races under concurrency; copying restores value semantics.
- named-in: Pattern-Oriented Software Architecture Vol. 4: A Pattern Language for Distributed Computing - Buschmann, Henney, Schmidt (2007)
- tags: value-semantics

### currying-partial-application — Currying / Partial Application
- aka: curried function, curry, partial application, functools.partial (Python realization), sectioning (Haskell operator sections)
- kind: functional-type-idioms
- what: Transform a multi-argument function into a chain of single-argument functions (currying), or fix a subset of a function's arguments to produce a new function of the remainder (partial application).
- problem: Building specialized functions from general ones without wrapper boilerplate; enables point-free composition, reusable configuration-first APIs, and incremental supply of arguments as they become available.
- named-in: Standard FP vocabulary: Wikipedia 'Currying'/'Partial application'; Reg Braithwaite, JavaScript Allongé; Python stdlib functools.partial documentation
- tags: javascript, python, functional, cross-language, borderline — In curried languages (Haskell/ML) this is the ambient function semantics, i.e. a language feature; cataloged as the deliberate API/design idiom it constitutes in uncurried languages (JS, Python). Two related mechanisms folded into one entry per house dedup rule; sources routinely treat them together.

### defunctionalization — Defunctionalization
- aka: defunctionalisation, closure conversion by tags
- kind: functional-type-idioms
- what: Replacing first-class functions with a tagged-union of the closures that actually occur plus an apply function that dispatches on the tag.
- problem: Lets higher-order programs run (or be serialized, stored, or sent) in first-order settings - C, wire protocols, event logs - by turning behavior into data.
- named-in: Definitional Interpreters for Higher-Order Programming Languages - John C. Reynolds (1972)
- tags: fp, borderline — Charter-flagged: originated as a compiler/interpreter transformation, but is a recurring in-program design move (serializable jobs, state machines from closures), so it passes the altitude test.

### effect-handler — Effect Handler
- aka: algebraic effect handler, algebraic effects and handlers
- kind: functional-type-idioms
- what: A construct that intercepts declared effect operations performed by a computation and decides how to interpret them and how to resume the suspended computation.
- problem: Separates what effects a computation performs from how they are implemented, enabling swappable interpreters, testing without mocks, and user-defined control flow (exceptions, generators, async).
- named-in: Handlers of Algebraic Effects - Plotkin & Pretnar (ESOP, 2009)
- tags: fp, ocaml, koka, borderline — Charter-flagged modern: still primarily a language/library research construct, but implemented in shipping languages (OCaml 5, Koka, Unison) and libraries, so it clears the establishedness gate.

### expression-templates — Expression Templates
- aka: lazy expression trees via templates
- kind: functional-type-idioms
- what: Overloaded operators build compile-time expression trees instead of computing eagerly, letting whole expressions be evaluated in one fused pass.
- problem: Naive operator overloading on vectors/matrices creates temporaries per operation; expression templates eliminate temporaries and enable loop fusion in numeric libraries.
- named-in: Expression Templates - Todd Veldhuizen, C++ Report (1995)
- tags: c++, numerics

### free-monad — Free Monad
- aka: free monad interpreter pattern, program-as-data
- kind: functional-type-idioms
- what: Representing a computation as a data structure of instructions (built from a functor) that is later run by separately-defined interpreters.
- problem: Decouples the description of an effectful program from its execution, enabling multiple interpreters (production, test, dry-run, logging) over one program value.
- named-in: Data Types à la Carte - Wouter Swierstra (JFP, 2008)
- tags: fp, haskell, scala, borderline — Could be folded into the monad umbrella as a variant, but it names a distinct design move (reify program, interpret later) with its own literature, so kept as an entry.

### function-object — Function Object
- aka: functor, callable object, lambda object (modern form)
- kind: functional-type-idioms
- what: An object overloading the call operator so it can be invoked like a function while carrying state and being inlinable through templates.
- problem: Plain function pointers carry no state and defeat inlining in generic algorithms; function objects give stateful, zero-overhead callables.
- named-in: Advanced C++: Programming Styles and Idioms - James O. Coplien (1992; 'functor')
- tags: c++

### functional-core-imperative-shell — Functional Core, Imperative Shell
- aka: impureim sandwich
- kind: functional-type-idioms
- what: Structuring a component as a pure decision-making core wrapped by a thin imperative layer that performs all IO and mutation.
- problem: Isolates hard-to-test effects at the boundary so the bulk of logic is pure, deterministic, and unit-testable without mocks.
- named-in: Functional Core, Imperative Shell - Gary Bernhardt (Destroy All Software screencast, 2012)
- tags: fp, borderline — Charter-flagged: a program-structuring statement that pulls toward architecture, but it is implementable inside one component and named/recurring, so kept in the design realm.

### lens — Lens
- aka: optics, functional reference, prism, traversal
- kind: functional-type-idioms
- what: A first-class, composable pair of getter and updater focused on a part of an immutable structure, so nested reads and copy-with-change updates compose like functions.
- problem: Removes the boilerplate of updating deeply nested immutable records, where each level otherwise requires manual copy-and-replace code.
- named-in: Combinators for Bidirectional Tree Transformations - Foster, Greenwald, Moore, Pierce, Schmitt (TOPLAS, 2007)
- tags: fp, haskell, scala

### module-pattern — Module Pattern
- aka: revealing module pattern
- kind: functional-type-idioms
- what: Use a closure (classically an IIFE) to create private state and functions, returning an object that exposes only the intended public interface.
- problem: Languages without native access modifiers or namespaces (pre-ES6 JavaScript) need encapsulation and a single namespace-safe export; the closure provides both.
- named-in: Learning JavaScript Design Patterns - Addy Osmani (2012); popularized by Crockford
- tags: javascript

### monad — Monad
- aka: computation builder, Kleisli triple
- kind: functional-type-idioms
- what: An interface (unit/return plus bind) for sequencing computations inside a context - optionality, failure, state, IO - so effectful steps compose like plain functions.
- problem: Gives one uniform composition law for wildly different effect plumbings, removing hand-written propagation of state, errors, or absence through call chains.
- named-in: Notions of Computation and Monads - Eugenio Moggi (1991)
- tags: fp, haskell, scala, borderline — Umbrella abstraction: concrete instances (State, Reader, Writer, IO, monad transformers) are folded here as variants, not enumerated; kept because the interface itself is the recurring design element.

### option-type — Option Type
- aka: Maybe type, Optional, nullable type
- kind: functional-type-idioms
- what: A sum type with exactly two cases - a present value (Some/Just) or absence (None/Nothing) - making optionality explicit in the type.
- problem: Eliminates null-reference and sentinel-value failure modes by forcing every consumer to handle the absent case before touching the value.
- named-in: Haskell 98 Language and Libraries Report - Simon Peyton Jones, ed. (2003)
- tags: fp, haskell, ml, rust, fsharp, scala

### phantom-type — Phantom Type
- aka: phantom type parameter, marker type parameter
- kind: functional-type-idioms
- what: A type parameter that appears in a type's signature but not in its runtime representation, used purely to encode compile-time distinctions or states.
- problem: Statically separates values that share a representation but must not mix (sanitized vs raw strings, units, protocol states) at zero runtime cost.
- named-in: Domain Specific Embedded Compilers - Leijen & Meijer (DSL '99, 1999)
- tags: fp, haskell, rust, ocaml

### sealed-trait — Sealed Trait
- aka: C-SEALED, private supertrait sealing, closed trait hierarchy
- kind: functional-type-idioms
- what: A public trait made unimplementable outside its crate via an unnameable private supertrait, keeping the set of implementors closed.
- problem: Public traits are otherwise open to downstream implementations, so adding a method is a breaking change; sealing preserves evolvability of the API.
- named-in: Rust API Guidelines (C-SEALED, living)
- tags: rust

### sfinae — SFINAE
- aka: Substitution Failure Is Not An Error, enable_if, detection idiom / member detector
- kind: functional-type-idioms
- what: Exploit the rule that invalid template-argument substitution removes a candidate from overload resolution to enable/disable overloads based on type properties.
- problem: Generic code must choose implementations by capability of the instantiating types; SFINAE gives compile-time introspection and constraint before language-level concepts existed.
- named-in: C++ Templates: The Complete Guide - Vandevoorde & Josuttis (2002; acronym coined here)
- tags: c++

### tag-dispatching — Tag Dispatching
- aka: tag dispatch, Int2Type/Type2Type (Alexandrescu forms), iterator-category dispatch
- kind: functional-type-idioms
- what: Select among overloads at compile time by passing an extra empty 'tag' type argument that encodes a property of the inputs.
- problem: Different implementations are optimal for different type categories (e.g. iterator strength); tags route the call without runtime branching or specialization sprawl.
- named-in: corpus:carnieregisters — Making things do stuff (register access using C++ templates) - Carnie (Feabhas Sticky Bits, 2017)
- tags: c++, borderline — Compile-time overload-selection plumbing; near the raw-language floor but named, recurring, and a standard-library house technique.

### tagless-final — Tagless Final
- aka: finally tagless, final encoding, object algebra (OO cousin)
- kind: functional-type-idioms
- what: Encoding an embedded language's operations as a parameterized interface (type class/trait) so programs are polymorphic terms interpretable by any implementation.
- problem: Allows multiple interpreters (evaluate, pretty-print, optimize) over the same program description and extension with new operations without reworking existing code, avoiding the tag-dispatch and expression-problem costs of a data-type encoding.
- named-in: Finally Tagless, Partially Evaluated - Carette, Kiselyov, Shan (JFP, 2009)
- tags: fp, haskell, scala, borderline — Advanced FP-community pattern rather than broad-industry vocabulary; establishedness is solid (canonical paper, standard Scala/Haskell pattern name) so kept with honest tag.

### thunk — Thunk
- aka: suspension, delayed evaluation, lazy evaluation, delay/force
- kind: functional-type-idioms
- what: A zero-argument closure standing in for a not-yet-computed value, forced (evaluated) on first demand and typically cached thereafter.
- problem: Defers expensive or possibly-unneeded computation until its result is actually demanded, enabling infinite structures, call-by-need semantics, and cheap short-circuiting.
- named-in: Thunks: A Way of Compiling Procedure Statements with Some Comments on Procedure Declarations - P. Z. Ingerman (CACM, 1961)
- tags: fp, haskell, scheme

### traits-class — Traits Class
- aka: traits, type traits, traits template
- kind: functional-type-idioms
- what: A template that associates compile-time information (types, constants, operations) with a type non-intrusively, specialized per type.
- problem: Generic code needs per-type metadata and adaptation points without modifying the types themselves; traits externalize that mapping.
- named-in: Traits: a new and useful template technique - Myers (C++ Report, 1995)
- tags: c++, embedded

### type-erasure — Type Erasure
- aka: duck-typed value wrapper, std::function/std::any technique, erased value wrapper
- kind: functional-type-idioms
- what: Wrap arbitrary concrete types satisfying an interface behind a single value type, hiding the concrete type via an internal vtable/template bridge.
- problem: Combines value semantics with runtime polymorphism and removes client dependencies on concrete types and inheritance hierarchies.
- named-in: corpus:iglberger — C++ Software Design - Klaus Iglberger (2022)
- tags: c++

### typelist — Typelist
- aka: type list, compile-time type sequence
- kind: functional-type-idioms
- what: A compile-time list of types built from nested templates (or variadic packs), manipulated by metafunctions to generate code over type collections.
- problem: Generating hierarchies or dispatch code over an open set of types requires a compile-time collection abstraction; typelists are that data structure.
- named-in: Modern C++ Design - Andrei Alexandrescu (2001)
- tags: c++, borderline — Metaprogramming infrastructure rather than an end-user design mechanism; kept as the named building block of policy/hierarchy generation.

### typestate — Typestate
- aka: typestate programming, phantom-type state encoding, compile-time state machine API, session-typed API, state-encoding types
- kind: functional-type-idioms
- what: Encode an object's protocol state in its static type (consuming and returning distinct types per transition) so illegal operations for the current state do not compile.
- problem: Runtime state checks catch protocol misuse only when it happens; typestate moves the state machine into the type system - idiomatic in Rust where move semantics enforce transitions.
- named-in: Typestate: A Programming Language Concept for Enhancing Software Reliability - Strom & Yemini, IEEE TSE (1986); Rust realization in The Embedded Rust Book
- tags: rust, embedded, fp, cpp

### units-of-measure-types — Units-of-Measure Types
- aka: units of measure (F#), dimension types, dimensional analysis in the type system, static unit checking
- kind: functional-type-idioms
- what: Encode physical units and dimensions as type-level annotations so the compiler checks unit correctness and infers result units through arithmetic, with no runtime cost.
- problem: Mixing quantities of different units (feet vs meters, ms vs s) compiles silently with raw numerics; type-level units turn unit mistakes into type errors.
- named-in: Kennedy, Types for Units-of-Measure: Theory and Practice (CEFP 2009, LNCS 6299); Kennedy, Programming Languages and Dimensions (Cambridge TR 391, 1996); shipped in F# 2.0
- tags: fsharp, type-level, covers-anchor:semantic-data-types

### value-semantics — Value Semantics
- aka: regular types
- kind: functional-type-idioms
- what: Designing types to behave like built-in values - copyable, comparable, independent after copy - rather than as aliased reference-semantic objects.
- problem: Reference semantics couple lifetimes and invite aliasing bugs; value-semantic designs localize reasoning and compose safely.
- named-in: corpus:iglberger — C++ Software Design - Iglberger (2022)
- tags: c++, borderline — A design style/principle more than a discrete mechanism; included because the corpus work names it as a first-class design element.


## Data structures & algorithms (design-building-block granularity) — `data-structures` (52)

### b-tree — B-tree
- aka: B+ tree (leaf-linked variant)
- kind: data-structures
- what: Self-balancing wide-fanout search tree whose nodes hold many keys sized to a block/page, keeping the tree shallow; B+ trees keep all values in linked leaves for range scans.
- problem: Binary trees generate one I/O or cache miss per level; matching node size to the storage block minimizes disk/page accesses for ordered indexes, making it the default database and filesystem index.
- named-in: Organization and Maintenance of Large Ordered Indexes - Bayer & McCreight (1972)
- tags: databases, filesystems, indexing

### binary-heap-priority-queue — Binary Heap (Priority Queue)
- aka: priority queue, min-heap, max-heap, d-ary heap (variant), pairing/Fibonacci heap (research variants, sibling corpus)
- kind: data-structures
- what: Implicit complete binary tree stored in an array maintaining the heap order property, giving O(log n) insert and extract-min/max with no pointers.
- problem: Schedulers, event queues, Dijkstra-style algorithms, and timer systems repeatedly need the next-highest-priority item without keeping the whole collection sorted.
- named-in: Algorithm 232: Heapsort - J. W. J. Williams (1964)
- tags: scheduling, containers, embedded

### binary-search-tree — Binary Search Tree
- aka: BST, self-balancing BST, red-black tree (balanced variant), AVL tree (balanced variant), treap / splay tree (research variants, sibling corpus)
- kind: data-structures
- what: Binary tree maintaining the search-order invariant (left < node < right); self-balancing variants (red-black, AVL) guarantee O(log n) ordered operations.
- problem: Ordered maps/sets needing sorted iteration, predecessor/successor, and range queries - which hash tables cannot provide - with logarithmic worst-case bounds (std::map, kernel schedulers).
- named-in: Introduction to Algorithms - Cormen, Leiserson, Rivest, Stein (2009)
- tags: containers, indexing

### bitmap-bitset — Bitmap / Bitset
- aka: bit array, bit vector, bitset, Roaring bitmap (compressed variant)
- kind: data-structures
- what: Dense array of bits representing set membership or boolean flags by index, supporting bulk bitwise set operations word-at-a-time; compressed variants (Roaring, WAH) handle sparse ranges.
- problem: Sets over a bounded integer universe cost far less as one bit per element than as pointer structures, and AND/OR/NOT over machine words gives vectorized set algebra (allocator maps, DB bitmap indexes, ECS masks).
- named-in: Programming Pearls - Jon Bentley (1986)
- tags: embedded, databases, memory-efficient

### bitmap-index — Bitmap Index
- aka: bit-map index, bitmapped index, bit-sliced index (variant), bitmap join index (variant), encoded bitmap index (variant)
- kind: data-structures
- what: An index that keeps, for each distinct value (or value range) of a column, a bitmap with one bit per row; multi-predicate queries are answered by bitwise AND/OR/NOT over the bitmaps before touching any rows.
- problem: B-tree row-id lists are bulky and slow to intersect for low-cardinality columns and ad-hoc conjunctive predicates; per-value bitmaps make multi-column selection a stream of word-wide boolean operations and compress well on skewed data.
- named-in: O'Neil — Model 204 Architecture and Performance, HPTS 1987; O'Neil & Quass — Improved Query Performance with Variant Indexes, SIGMOD 1997
- tags: db, analytics, index, borderline — distinct from bitmap-bitset (the raw data structure already in the index): this is the database index mechanism built from per-value bitmaps, with its own naming literature

### bloom-filter — Bloom Filter
- aka: counting Bloom filter (deletable variant), blocked Bloom filter, cuckoo filter (alternative with deletion), XOR filter (static alternative)
- kind: data-structures
- what: Bit array plus k hash functions answering approximate set membership with no false negatives and a tunable false-positive rate.
- problem: Storing full key sets to answer 'definitely absent?' wastes memory; a few bits per element let a component skip expensive lookups (disk reads, cache probes, network calls) for keys that cannot be present.
- named-in: Space/Time Trade-offs in Hash Coding with Allowable Errors - Burton H. Bloom (1970)
- tags: probabilistic, databases, networking

### bounding-volume-hierarchy — Bounding Volume Hierarchy
- aka: BVH, AABB tree
- kind: data-structures
- what: Tree whose nodes are bounding volumes (typically AABBs) enclosing their children, with scene objects at the leaves, letting intersection queries prune whole subtrees.
- problem: Ray tracing and collision detection against thousands of objects cannot test each primitive; hierarchical bounds reduce intersection tests to a logarithmic descent.
- named-in: Real-Time Rendering - Akenine-Moller, Haines, Hoffman (2018)
- tags: spatial, graphics, games, physics

### conflict-free-replicated-data-type-crdt — Conflict-free Replicated Data Type (CRDT)
- aka: convergent replicated data type (CvRDT), commutative replicated data type (CmRDT), G-Counter / PN-Counter / G-Set / OR-Set / LWW-Register / RGA (family members, folded)
- kind: data-structures
- what: Family of replicated data types (counters, sets, registers, sequences) whose merge operations are commutative/associative/idempotent, so concurrently edited replicas converge without coordination.
- problem: Multi-writer replication without locks or consensus produces conflicts; algebraically merge-safe state lets offline-first apps and collaborative editors converge deterministically.
- named-in: Conflict-free Replicated Data Types - Shapiro, Preguica, Baquero, Zawirski (2011)
- tags: distributed, collaboration, borderline — Charter mandates ONE element for the family; each replica's type is implementable in one component (IN), though the replication context shades distributed-systems territory.

### consistent-hashing — Consistent Hashing
- aka: hash ring, rendezvous hashing (alternative), jump consistent hash (variant)
- kind: data-structures
- what: Hashing scheme placing keys and buckets on the same ring so each key maps to the nearest bucket, remapping only ~1/n of keys when a bucket joins or leaves; virtual nodes smooth the load.
- problem: Modulo hashing reshuffles nearly every key when the bucket count changes; caches and partitioned stores need key-to-node assignment that is stable under membership churn.
- named-in: Consistent Hashing and Random Trees: Distributed Caching Protocols for Relieving Hot Spots on the World Wide Web - Karger et al. (1997)
- tags: distributed, caching, borderline — The ring structure is implementable inside one component (IN); its use as a cluster-partitioning scheme shades architectural - parked companion entry for Phase 3.

### copy-on-write-b-tree — Copy-on-Write B-Tree
- aka: CoW B-tree, append-only B-tree
- kind: data-structures
- what: A B-tree whose updates never modify pages in place: changed pages and their ancestors up to the root are rewritten to new locations, and commit is an atomic root swap.
- problem: Combines B-tree lookup with crash safety and lock-free readers (old roots stay valid snapshots) without a separate recovery log; used by LMDB and btrfs at the cost of write amplification.
- named-in: Database Internals - Petrov (2019)
- tags: db, storage-engine, filesystems

### count-min-sketch — Count-Min Sketch
- aka: —
- kind: data-structures
- what: Sub-linear 2-D counter array indexed by multiple hash functions that answers approximate frequency queries over a stream, with one-sided (over-count) error.
- problem: Counting exact per-item frequencies over high-volume streams needs memory proportional to distinct items; a fixed small sketch bounds error probabilistically for heavy-hitter and frequency estimation.
- named-in: An Improved Data Stream Summary: The Count-Min Sketch and its Applications - Cormode & Muthukrishnan (2005)
- tags: probabilistic, streaming

### deque — Deque
- aka: double-ended queue
- kind: data-structures
- what: Sequence container supporting O(1) insertion and removal at both ends, typically as a ring buffer or blocked array.
- problem: Sliding windows, work-stealing schedulers, and undo histories need queue and stack behavior simultaneously; neither a plain stack nor a FIFO queue suffices.
- named-in: The Art of Computer Programming, Vol. 1: Fundamental Algorithms - Donald Knuth (1968)
- tags: containers

### disjoint-set-union-find — Disjoint-Set (Union-Find)
- aka: union-find, merge-find set, disjoint-set forest
- kind: data-structures
- what: Forest of trees tracking a partition of elements into disjoint sets, with union-by-rank and path compression making find/union near-constant amortized.
- problem: Incremental equivalence tracking (connected components, type unification, Kruskal's MST, image segmentation) needs merge-and-query on partitions far faster than recomputing reachability.
- named-in: Introduction to Algorithms - Cormen, Leiserson, Rivest, Stein (2009)
- tags: graphs, compilers

### dynamic-array — Dynamic Array
- aka: growable array, dynamic table, resizable array, vector (C++), ArrayList (Java)
- kind: data-structures
- what: Contiguous array that grows by amortized capacity doubling (and optionally shrinks), preserving O(1) amortized append and O(1) random access.
- problem: Fixed-size arrays force a size guess up front; linked structures sacrifice cache locality and random access. Amortized reallocation gives list flexibility at array speed.
- named-in: Introduction to Algorithms - Cormen, Leiserson, Rivest, Stein (2009)
- tags: containers

### embedded-pointer — Embedded Pointer
- aka: intrusive links, intrusive linked list, intrusive container, embedded list node (Linux list_head style)
- kind: data-structures
- what: Embed the pointers that maintain a collection directly into each member object instead of allocating external link nodes.
- problem: External link nodes double the allocation count and memory overhead of collections; embedding the links in the objects removes per-node allocations (the intrusive-container idiom).
- named-in: corpus:noblesmallmem — Small Memory Software: Patterns for Systems with Limited Memory - Noble & Weir (2000)
- tags: embedded, memory, c, cpp, kernel

### erase-remove — Erase-Remove
- aka: remove-erase idiom
- kind: data-structures
- what: Combine std::remove/remove_if (which compacts kept elements) with container erase to actually delete matching elements from a sequence container.
- problem: STL algorithms cannot change container size; the two-step idiom is the established way to physically delete elements without quadratic cost.
- named-in: Effective STL - Scott Meyers (2001)
- tags: c++, borderline — A micro container-usage idiom rather than a design mechanism; kept as a canonical named C++ idiom (now std::erase_if).

### fenwick-tree — Fenwick Tree
- aka: binary indexed tree, BIT
- kind: data-structures
- what: Implicit array-based tree exploiting binary index decomposition to maintain prefix sums with O(log n) point update and prefix query in n words of memory.
- problem: The prefix-sum-with-updates role of a segment tree, in a fraction of the memory and code, when only invertible aggregates (sums, counts) are needed.
- named-in: A New Data Structure for Cumulative Frequency Tables - Peter Fenwick (1994)
- tags: ranges, borderline — Near the research-zoo line; included because it is the named lighter-weight alternative designers actually reach for over segment trees for cumulative counts.

### fixed-capacity-container — Fixed-Capacity Container
- aka: static container, no-heap container, etl::vector-style container
- kind: data-structures
- what: STL-style containers whose maximum capacity is a compile-time parameter, storing elements in embedded (static or stack) storage with no heap use.
- problem: Standard containers allocate dynamically, which embedded and safety-critical code forbids; fixed-capacity variants keep container ergonomics with deterministic memory.
- named-in: corpus:etl — Embedded Template Library (ETL) documentation - Wellbelove (living)
- tags: c++, embedded

### gap-buffer — Gap Buffer
- aka: —
- kind: data-structures
- what: Contiguous text buffer with a movable gap of free space at the cursor position, making localized insertions and deletions O(1) until the gap moves or fills.
- problem: Text editing clusters around a cursor; keeping the free space there converts the common-case edit from an O(n) array shift into an in-place write (Emacs's buffer representation).
- named-in: The Craft of Text Editing - Craig A. Finseth (1991)
- tags: strings, text-editors

### hash-array-mapped-trie-hamt — Hash Array Mapped Trie (HAMT)
- aka: ideal hash tree, persistent hash map, CHAMP (variant)
- kind: data-structures
- what: Trie over hash-code bit chunks using per-node bitmaps to compress sparse children, giving an efficiently persistent (structurally shared, immutable) hash map.
- problem: Immutable/functional programs need maps whose 'updates' return new versions in O(log n) time and memory via structural sharing rather than full copies (Clojure, Scala, Immutable.js collections).
- named-in: Ideal Hash Trees - Phil Bagwell (2001)
- tags: functional, immutability, containers

### hash-table — Hash Table
- aka: hash map, dictionary, associative array, unordered map
- kind: data-structures
- what: Key-value store mapping keys through a hash function into an array of buckets, with collisions resolved by separate chaining or open addressing (linear/quadratic probing, Robin Hood, cuckoo, Swiss-table variants folded here).
- problem: Provides expected O(1) lookup, insert, and delete by key when key ordering is not needed, trading memory overhead and worst-case degradation for speed.
- named-in: Introduction to Algorithms - Cormen, Leiserson, Rivest, Stein (2009)
- tags: containers, indexing

### hyperloglog — HyperLogLog
- aka: LogLog (predecessor), HLL++
- kind: data-structures
- what: Cardinality-estimation sketch that hashes items and records maximum leading-zero runs in a small register array, estimating distinct counts within a few percent using kilobytes.
- problem: Exact distinct-count over large streams requires storing every seen key; probabilistic register merging gives mergeable, fixed-memory cardinality estimates (unique visitors, distinct keys).
- named-in: HyperLogLog: the analysis of a near-optimal cardinality estimation algorithm - Flajolet, Fusy, Gandouet, Meunier (2007)
- tags: probabilistic, streaming, distributed

### interval-tree — Interval Tree
- aka: augmented interval tree, centered interval tree
- kind: data-structures
- what: Search tree over intervals (typically a BST augmented with subtree max-endpoints) answering which stored intervals overlap a query point or interval in O(log n + k).
- problem: Schedulers, editors (marker ranges), genomics, and calendars repeatedly ask 'what overlaps this range?', which sorted lists answer only by linear scan.
- named-in: Introduction to Algorithms - Cormen, Leiserson, Rivest, Stein (2009)
- tags: intervals, borderline — Charter-flagged: kept IN - a recurring designer-reachable role (overlap queries), not just an algorithmics exercise.

### inverted-index — Inverted Index
- aka: postings list, inverted file
- kind: data-structures
- what: Mapping from each term to the sorted list of documents (and positions) containing it, the core structure of full-text search engines.
- problem: Scanning documents per query is linear in corpus size; inverting the term-document relation makes multi-term queries an intersection/union of postings lists.
- named-in: Introduction to Information Retrieval - Manning, Raghavan, Schutze (2008)
- tags: search, databases, indexing

### k-d-tree — k-d Tree
- aka: k-dimensional tree
- kind: data-structures
- what: Binary space-partitioning tree that splits points on alternating coordinate axes, supporting nearest-neighbor and orthogonal range queries in low dimensions.
- problem: Nearest-neighbor and range search over point sets is linear without an index; axis-aligned recursive splits prune most of the space per query.
- named-in: Multidimensional Binary Search Trees Used for Associative Searching - Jon Bentley (1975)
- tags: spatial, graphics, ml

### linked-list — Linked List
- aka: singly linked list, doubly linked list, circular linked list, unrolled linked list (variant)
- kind: data-structures
- what: Sequence of nodes each holding an element and a pointer to the next (and optionally previous) node, giving O(1) insertion/removal at a known position without element movement.
- problem: Sequences with frequent mid-stream splicing, stable element addresses, or no contiguous memory (allocators, kernels) cannot use arrays; pointer links trade locality for splice freedom.
- named-in: Introduction to Algorithms - Cormen, Leiserson, Rivest, Stein (2009)
- tags: containers, borderline — Near the lower altitude floor (elementary ADT) but unambiguously named, recurring, and a deliberate design choice versus arrays; kept IN.

### lock-free-fifo-queue-michael-scott — Lock-Free FIFO Queue (Michael-Scott)
- aka: Michael-Scott queue, MS queue, nonblocking concurrent queue
- kind: data-structures
- what: A linked-list MPMC queue where enqueue and dequeue advance head/tail with CAS, and threads help complete a lagging tail swing before proceeding.
- problem: A shared FIFO whose operations never block: no lock-holder preemption stalls, safe in mixed-priority and signal contexts, scalable under moderate contention.
- named-in: Simple, Fast, and Practical Non-Blocking and Blocking Concurrent Queue Algorithms - Michael & Scott (1996)
- tags: c, cpp, java, systems

### lock-free-stack-treiber — Lock-Free Stack (Treiber)
- aka: Treiber stack, nonblocking LIFO, IBM freelist
- kind: data-structures
- what: A linked LIFO where push and pop swing the top-of-stack pointer with a CAS retry loop (with an ABA guard when nodes are recycled).
- problem: The minimal lock-free container: a shared free list or work stack usable from contexts where locking is forbidden or unscalable.
- named-in: Systems Programming: Coping with Parallelism (IBM Research Report RJ 5118) - R. K. Treiber (1986)
- tags: c, cpp, systems

### lsm-tree — LSM Tree
- aka: log-structured merge-tree, memtable + SSTable
- kind: data-structures
- what: Write-optimized index that batches writes in an in-memory table, flushes them as sorted immutable runs (SSTables), and merges runs in the background via compaction.
- problem: In-place index updates (B-trees) turn random writes into random I/O; sequential append plus deferred merge converts write-heavy workloads into sequential I/O at the cost of read amplification.
- named-in: The Log-Structured Merge-Tree (LSM-Tree) - O'Neil, Cheng, Gawlick, O'Neil (1996)
- tags: databases, storage-engines, db, storage-engine

### merkle-tree — Merkle Tree
- aka: hash tree
- kind: data-structures
- what: Tree whose leaves are hashes of data blocks and whose internal nodes hash their children, so one root hash authenticates the whole set and any block is verifiable with a log-length path.
- problem: Verifying integrity or divergence of large or distributed data sets without transferring them; enables efficient tamper-evidence, sync anti-entropy, and inclusion proofs (Git, ZFS, certificate transparency, blockchains).
- named-in: A Digital Signature Based on a Conventional Encryption Function - Ralph Merkle (1987)
- tags: security, distributed, storage

### minhash — MinHash
- aka: min-wise independent permutations, MinHash LSH (composition)
- kind: data-structures
- what: Similarity sketch storing the minimum hash values of a set under many hash functions, so sketch agreement estimates Jaccard similarity between sets.
- problem: Near-duplicate detection and similarity search over huge document/set collections cannot compare full sets pairwise; small fixed sketches make similarity estimable in constant time.
- named-in: On the Resemblance and Containment of Documents - Andrei Broder (1997)
- tags: probabilistic, search, dedup

### navigation-mesh — Navigation Mesh
- aka: navmesh, walkable-surface mesh
- kind: data-structures
- what: A data structure representing an environment's walkable space as connected convex polygons, over which agents path-find polygon-to-polygon and then smooth (e.g. string-pulling/funnel) within the free space.
- problem: Waypoint graphs under-represent open walkable areas and force unnatural paths; a polygon mesh of free space supports arbitrary agent movement, cheap search over few polygons, and locally optimal smoothing.
- named-in: Snook, 'Simplified 3D Movement and Pathfinding Using Navigation Meshes', Game Programming Gems, 2000
- tags: games, ai, spatial

### persistent-data-structure — Persistent Data Structure
- aka: immutable data structure, structural sharing, purely functional data structure
- kind: data-structures
- what: A data structure whose update operations return a new version while old versions remain valid, sharing unchanged substructure between versions.
- problem: Provides safe sharing across threads and cheap history/undo without defensive copying, by making every version immutable and reusing common parts.
- named-in: Making Data Structures Persistent - Driscoll, Sarnak, Sleator, Tarjan (JCSS, 1989)
- tags: fp, clojure, scala, haskell

### piece-table — Piece Table
- aka: piece chain, piece tree (VS Code variant)
- kind: data-structures
- what: Edit representation keeping the original file and an append-only add buffer immutable, with the document described as a sequence of pieces (spans) into the two buffers.
- problem: Editors need fast arbitrary edits, cheap undo, and untouched original file data; recording edits as span descriptors avoids moving text and makes undo a piece-list operation.
- named-in: Data Structures for Text Sequences - Charles Crowley (1998)
- tags: strings, text-editors

### quadtree-octree — Quadtree / Octree
- aka: octree (3D analogue), region quadtree, point quadtree, loose octree (variant)
- kind: data-structures
- what: Hierarchical spatial partition recursively subdividing 2D space into four quadrants (or 3D into eight octants) until cells meet an occupancy or depth bound.
- problem: Spatial queries (culling, collision broad-phase, image regions, point clouds) over non-uniform data need adaptive subdivision that concentrates resolution where objects cluster.
- named-in: Quad Trees: A Data Structure for Retrieval on Composite Keys - Finkel & Bentley (1974)
- tags: spatial, games, graphics, gis

### queue-fifo — Queue (FIFO)
- aka: FIFO, first-in-first-out queue
- kind: data-structures
- what: First-in-first-out collection with enqueue at the tail and dequeue at the head, array- or list-backed.
- problem: Order-preserving buffering between producers and consumers - task queues, BFS frontiers, request pipelines - requires arrival-order service as a structural guarantee.
- named-in: Introduction to Algorithms - Cormen, Leiserson, Rivest, Stein (2009)
- tags: containers, borderline — Elementary ADT at the band's floor; kept IN as the in-process structure (the message-queue mechanism and broker topology belong to other scouts/Phase 3).

### r-tree — R-tree
- aka: R*-tree (variant), Hilbert R-tree (variant)
- kind: data-structures
- what: Balanced B-tree-like index of minimum bounding rectangles that may overlap, grouping nearby spatial objects for disk-friendly window and containment queries.
- problem: Databases need paged, balanced indexing of extended spatial objects (rectangles, polygons) where point-based partitions fail; the standard spatial index of GIS databases.
- named-in: R-Trees: A Dynamic Index Structure for Spatial Searching - Antonin Guttman (1984)
- tags: spatial, databases, gis

### rope — Rope
- aka: cord
- kind: data-structures
- what: Balanced binary tree of string fragments representing a long string, making concatenation, insertion, and splitting O(log n) instead of O(n) copies.
- problem: Flat strings make every edit of a large text a full copy; editors and string-heavy systems need sublinear splice operations and cheap substring sharing.
- named-in: Ropes: an Alternative to Strings - Boehm, Atkinson, Plass (1995)
- tags: strings, text-editors

### scene-graph — Scene Graph
- aka: transform hierarchy, scene tree
- kind: data-structures
- what: Represent a scene as a hierarchy of nodes whose spatial transforms (and other attributes) compose parent-to-child, so moving a parent moves its whole subtree.
- problem: Objects are naturally attached to one another (turret on tank, moon around planet); a hierarchy lets local transforms be authored independently while world transforms are derived by composition, and supports hierarchical culling and traversal.
- named-in: Real-Time Rendering - Akenine-Moller, Haines, Hoffman (2008, 3rd ed.)
- tags: games, graphics

### secondary-index — Secondary Index
- aka: non-clustered index, alternate-key index
- kind: data-structures
- what: An auxiliary structure mapping non-primary-key attribute values to record locations (or primary keys), maintained alongside the base data on every write.
- problem: Queries on attributes other than the primary access path degenerate to full scans; a redundant per-attribute index buys lookup speed at the cost of write amplification and consistency maintenance.
- named-in: Designing Data-Intensive Applications - Kleppmann (2017)
- tags: db, storage-engine, borderline — Generic 'index' altitude is contested; kept because 'secondary index' names a specific recurring design decision (redundant derived access path maintained on write).

### segment-tree — Segment Tree
- aka: statistic tree, segment tree with lazy propagation (variant)
- kind: data-structures
- what: Complete binary tree over an array where each node stores an aggregate (sum, min, max) of its range, giving O(log n) range queries and point/range updates.
- problem: Alternating range-aggregate queries and updates over an array defeat both prefix-sum arrays (slow update) and raw arrays (slow query); the tree balances the two.
- named-in: Computational Geometry: Algorithms and Applications - de Berg, Cheong, van Kreveld, Overmars (2008)
- tags: ranges, borderline — Charter-flagged research-zoo borderline: kept IN - named, recurring, and reached-for by role (range aggregate index) well beyond competitive programming; variants folded.

### skip-list — Skip List
- aka: —
- kind: data-structures
- what: Sorted linked list augmented with probabilistic express lanes at multiple levels, giving expected O(log n) search/insert/delete without rebalancing.
- problem: Balanced trees achieve ordered O(log n) operations through intricate rebalancing; randomized levels achieve the same expectation with simpler code and easier concurrent (lock-free) implementation.
- named-in: Skip Lists: A Probabilistic Alternative to Balanced Trees - William Pugh (1990)
- tags: containers, concurrency-friendly, databases

### slot-map — Slot Map
- aka: generational arena, generational index array, handle map
- kind: data-structures
- what: Contiguous object pool addressed by stable keys that pair a slot index with a generation counter, so freed-and-reused slots invalidate stale handles while keeping O(1) access and dense iteration.
- problem: Game and systems code needs stable, dangle-proof references into pools of frequently created/destroyed objects without pointer invalidation or use-after-free; generations make stale handles detectable.
- named-in: slot_map Container in C++ (WG21 P0661) - Allan Deutsch (2017)
- tags: cpp, rust, games

### sparse-set — Sparse Set
- aka: sparse-dense set
- kind: data-structures
- what: Pair of arrays (dense packed elements plus sparse index-by-value) representing an integer set with O(1) insert, delete, membership, and clear, and cache-friendly iteration over only the members.
- problem: Sets over a bounded integer universe that are cleared and iterated constantly (compiler live-sets, ECS component membership) need O(1) clear and dense iteration, which bitmaps and hash sets lack.
- named-in: An Efficient Representation for Sparse Sets - Briggs & Torczon (1993)
- tags: games, compilers, performance

### spatial-partition — Spatial Partition
- aka: spatial partitioning, spatial index
- kind: data-structures
- what: Store objects in a data structure organized by their spatial position (grid, quadtree, BSP, etc.) so that location-based queries need only examine nearby cells.
- problem: Finding objects near a point or each other (collision, combat range, rendering culling) is O(n^2) by pairwise scan; position-keyed structures cut queries to near-constant or logarithmic cost. Concrete structures (quadtree, k-d tree, BSP) are enumerated in the datastructures corpus, not here.
- named-in: Game Programming Patterns - Robert Nystrom (2014)
- tags: games, performance

### stack — Stack
- aka: LIFO, pushdown list
- kind: data-structures
- what: Last-in-first-out collection with push/pop/peek at one end, whether array- or list-backed.
- problem: Nested and reversible processes - call frames, undo, parsing, DFS, expression evaluation - need most-recent-first access as a structural guarantee.
- named-in: Introduction to Algorithms - Cormen, Leiserson, Rivest, Stein (2009)
- tags: containers, borderline — Elementary ADT at the band's floor; kept IN because designers reach for 'a stack' by role constantly and it anchors many other elements.

### suffix-array — Suffix Array
- aka: suffix tree (heavier predecessor, folded), FM-index (compressed successor, noted)
- kind: data-structures
- what: Sorted array of all suffix start positions of a text, supporting binary-search substring queries; the array-based, cache-friendly successor to the suffix tree.
- problem: Repeated arbitrary-substring search over a fixed large text (bioinformatics, plagiarism detection, search indexing) needs a full-text index cheaper than a suffix tree's pointers.
- named-in: Suffix Arrays: A New Method for On-Line String Searches - Manber & Myers (1990)
- tags: strings, bioinformatics, borderline — Shades research-zoo; kept IN as the designer-reachable full-text-substring-index role, with suffix tree and FM-index folded as variants.

### t-digest — t-digest
- aka: quantile sketch (role), GK sketch / KLL sketch (alternatives, noted)
- kind: data-structures
- what: Mergeable sketch of a numeric distribution built from size-varying centroid clusters, estimating quantiles (esp. extreme percentiles) accurately in constant memory.
- problem: Monitoring systems need p99/p999 latency over unbounded streams and across shards; exact quantiles require storing all samples, and fixed-bin histograms lose tail accuracy.
- named-in: Computing Extremely Accurate Quantiles Using t-Digests - Dunning & Ertl (2019)
- tags: probabilistic, streaming, observability

### trie — Trie
- aka: prefix tree, digital tree, radix tree (path-compressed variant), Patricia trie (binary path-compressed variant)
- kind: data-structures
- what: Tree keyed by successive symbols of the key, so all descendants of a node share a common prefix; radix/Patricia variants compress single-child chains into one edge.
- problem: Prefix lookup, autocomplete, longest-prefix match (IP routing), and ordered string sets need key-structure-aware indexing that comparison trees and hash tables do not give.
- named-in: Trie Memory - Edward Fredkin (1960)
- tags: strings, networking, indexing

### uniform-spatial-hash-grid — Uniform Spatial Hash Grid
- aka: spatial hashing, uniform grid, bin-lattice
- kind: data-structures
- what: Partition of space into uniform cells whose coordinates hash into buckets of contained objects, so neighborhood queries examine only nearby cells.
- problem: Broad-phase collision and proximity queries need O(1) neighbor lookup for roughly uniformly-sized objects without the build cost or pointer-chasing of trees.
- named-in: Optimized Spatial Hashing for Collision Detection of Deformable Objects - Teschner et al. (2003)
- tags: spatial, games, physics, simulation

### zipper — Zipper
- aka: Huet zipper, focused data structure, one-hole context
- kind: data-structures
- what: A representation of a position inside an immutable structure as the focused element plus its inverted surrounding context, allowing O(1) local edits and navigation.
- problem: Enables efficient localized updates and cursor-style navigation in purely functional trees and lists, where naive editing would rebuild the path from the root on every step.
- named-in: The Zipper - Gérard Huet (Journal of Functional Programming, 1997)
- tags: fp, haskell, clojure

### zone-map — Zone Map
- aka: small materialized aggregates, SMA, min-max index, block range index, BRIN, data skipping index, storage index
- kind: data-structures
- what: A tiny per-block summary (typically min/max, optionally count/sum) kept for each zone of contiguously stored tuples; scans consult the summaries first and skip every block whose value range cannot satisfy the predicate.
- problem: Full-precision secondary indexes on bulk-loaded analytic data are expensive to build and maintain; a few bytes of precomputed aggregate per block prunes most of a scan for range/equality predicates at near-zero load and storage cost.
- named-in: Moerkotte — Small Materialized Aggregates: A Light Weight Index Structure for Data Warehousing, VLDB 1998 (naming source); 'zone map' is the Netezza-originated industry name (Ziauddin et al., Dimensions Based Data Clustering and Zone Maps, PVLDB 2017); PostgreSQL BRIN is the same mechanism
- tags: db, analytics, index


## Persistence & durability — `persistence-durability` (29)

### active-record — Active Record
- aka: —
- kind: persistence-durability
- what: An object that wraps one row of a database table, encapsulating the database access and adding domain logic on that data.
- problem: For CRUD-shaped domains, separating data access from domain behavior adds indirection with little payoff; fusing row data, persistence methods, and logic in one class is the simplest thing that works.
- named-in: Patterns of Enterprise Application Architecture - Martin Fowler (2002)
- tags: enterprise, orm

### association-table-mapping — Association Table Mapping
- aka: join table mapping
- kind: persistence-durability
- what: Maps a many-to-many association to a separate table holding pairs of foreign keys into the two associated tables.
- problem: Relational schemas cannot store multivalued fields in a row; an intermediate link table represents the association that neither object's table can hold.
- named-in: Patterns of Enterprise Application Architecture - Martin Fowler (2002)
- tags: enterprise, orm

### checkpointing — Checkpointing
- aka: checkpoint, fuzzy checkpoint, database checkpoint, checkpoint/restart, snapshot state saving
- kind: persistence-durability
- what: Periodically record a consistent marker of which logged changes have reached the main data store, bounding how far back crash recovery must scan the log.
- problem: Without checkpoints the recovery log grows without bound and restart must replay the whole history; a checkpoint truncates the redo horizon and caps recovery time.
- named-in: corpus:hanmer — Patterns for Fault Tolerant Software - Hanmer (2007)
- tags: db, storage-engine, long-running-computation, fault-tolerance

### class-table-inheritance — Class Table Inheritance
- aka: —
- kind: persistence-durability
- what: Maps each class in an inheritance hierarchy to its own table holding only that class's fields, joined by shared primary key.
- problem: One-table-per-hierarchy wastes columns and one-table-per-concrete-class duplicates them; a table per class keeps the schema normalized at the cost of joins to assemble an object.
- named-in: Patterns of Enterprise Application Architecture - Martin Fowler (2002)
- tags: enterprise, orm

### concrete-table-inheritance — Concrete Table Inheritance
- aka: leaf table inheritance
- kind: persistence-durability
- what: Maps each concrete class in an inheritance hierarchy to its own table containing all its fields, inherited and declared.
- problem: Loading an object of a known concrete class should touch one table only; duplicating inherited columns per concrete table removes joins at the cost of schema duplication and cross-table key discipline.
- named-in: Patterns of Enterprise Application Architecture - Martin Fowler (2002)
- tags: enterprise, orm

### content-addressable-storage — Content-Addressable Storage
- aka: content addressing, content-addressed store, CAS (storage sense), hash-addressed storage, content-defined chunking deduplication (companion mechanism)
- kind: persistence-durability
- what: Store immutable blocks/objects keyed by a cryptographic hash of their contents, so identical data coalesces, references are self-verifying, and writes are idempotent.
- problem: Location-addressed storage cannot cheaply deduplicate, verify integrity, or share immutable history; hashing the content makes the identifier both the address and the checksum.
- named-in: Quinlan & Dorward, 'Venti: A New Approach to Archival Storage', USENIX FAST 2002 (verified live); canonical modern realization: the Git object store
- tags: storage, version-control

### data-mapper — Data Mapper
- aka: —
- kind: persistence-durability
- what: A layer of mapper objects that moves data between in-memory objects and the database while keeping the two schemas independent of each other.
- problem: Rich domain objects and relational schemas evolve differently; putting the transfer logic in dedicated mappers lets neither side know about the other.
- named-in: Patterns of Enterprise Application Architecture - Martin Fowler (2002)
- tags: enterprise, orm

### dependent-mapping — Dependent Mapping
- aka: —
- kind: persistence-durability
- what: Has one class (the owner) perform the database mapping for a child class whose objects are accessed only through it.
- problem: Objects that exist only within one owner (line items in an order) do not need their own mapper, identity map, or independent updates; letting the owner map them simplifies the machinery.
- named-in: Patterns of Enterprise Application Architecture - Martin Fowler (2002)
- tags: enterprise, orm

### eeprom-emulation-in-flash — EEPROM Emulation in Flash
- aka: flash-based parameter storage, emulated EEPROM
- kind: persistence-durability
- what: Emulate byte-updatable EEPROM semantics on page-erasable flash by journaling variable records across reserved pages and swapping/compacting pages when full.
- problem: Many MCUs lack true EEPROM while flash only erases in large pages with limited endurance; record journaling plus page rotation provides small-datum persistence with wear spreading and power-loss recovery.
- named-in: AN2594 - EEPROM emulation in STM32F10x microcontrollers (STMicroelectronics)
- tags: embedded, flash, persistence

### embedded-value — Embedded Value
- aka: aggregate mapping, composer
- kind: persistence-durability
- what: Maps a value object into the columns of its owner's table rather than giving it a table of its own.
- problem: Small value objects (money, date range) do not merit their own tables and joins; flattening their fields into the owning record keeps the object model rich and the schema simple.
- named-in: Patterns of Enterprise Application Architecture - Martin Fowler (2002)
- tags: enterprise, orm

### event-sourcing — Event Sourcing
- aka: —
- kind: persistence-durability
- what: Captures every change to application state as an immutable event in an append-only log, so current state is derived by replaying the events rather than stored destructively.
- problem: Update-in-place storage loses history, complicates audit, and makes past states unrecoverable; storing the events themselves makes state reconstruction, temporal queries, and replay-based recovery possible.
- named-in: Event Sourcing, martinfowler.com (Further Enterprise Application Architecture development) - Martin Fowler (2005)
- tags: enterprise, events, borderline — The in-component append-log persistence mechanism is IN; the system-wide event-sourced architecture style is parked for Phase 3.

### flash-translation-layer — Flash Translation Layer
- aka: FTL, logical-to-physical flash mapping, flash mapping layer, out-of-place flash update
- kind: persistence-durability
- what: A firmware layer that remaps logical block writes to out-of-place physical flash pages, maintaining a logical-to-physical mapping table plus garbage collection so erase-constrained flash presents an ordinary rewritable block device.
- problem: NAND/NOR flash cannot rewrite in place and erases in large blocks with limited endurance; out-of-place remapping hides erase-before-write, enables wear leveling, and keeps a consistent mapping across power loss.
- named-in: Intel 'Understanding the Flash Translation Layer (FTL) Specification' (AP-684, 1998); Chung et al., 'A survey of Flash Translation Layer', Journal of Systems Architecture 2009
- tags: embedded, flash, storage, borderline — composite mechanism (composes flash-wear-leveling + out-of-place update + garbage collection); kept because FTL is the established name for the mapping mechanism itself, which the existing flash-wear-leveling entry does not cover

### flash-wear-leveling — Flash Wear Leveling
- aka: wear levelling, erase-cycle balancing
- kind: persistence-durability
- what: Distribute writes and erases evenly across flash pages/blocks (via remapping or rotation) so no single block exhausts its limited erase endurance prematurely.
- problem: Flash blocks endure only a bounded number of erase cycles while write traffic is naturally skewed to hot data; leveling the wear multiplies effective device lifetime.
- named-in: Wear leveling - Wikipedia; AN798 EEPROM Emulation with Wear-Leveling (Silicon Labs)
- tags: embedded, flash, persistence

### foreign-key-mapping — Foreign Key Mapping
- aka: —
- kind: persistence-durability
- what: Maps an object reference between objects to a foreign key column in the referring object's table.
- problem: In-memory pointers do not exist in relational storage; translating references to keys on save and keys back to references on load preserves the object graph.
- named-in: Patterns of Enterprise Application Architecture - Martin Fowler (2002)
- tags: enterprise, orm

### group-commit — Group Commit
- aka: batch commit
- kind: persistence-durability
- what: Accumulate the log records of several concurrently committing transactions and flush them to stable storage with a single synchronous write.
- problem: One fsync per commit makes the log device the throughput ceiling; amortizing one flush over many commits trades a little latency for large gains in commit throughput.
- named-in: Transaction Processing: Concepts and Techniques - Gray & Reuter (1992)
- tags: db, storage-engine, throughput

### identity-field — Identity Field
- aka: —
- kind: persistence-durability
- what: Saves the database identity (primary key) as a field in the in-memory object to maintain the correspondence between object and row.
- problem: Objects and rows must be matched reliably across loads and saves; storing the key in the object gives every domain object a durable identity handle.
- named-in: Patterns of Enterprise Application Architecture - Martin Fowler (2002)
- tags: enterprise, orm

### inheritance-mappers — Inheritance Mappers
- aka: —
- kind: persistence-durability
- what: A structure of mapper classes mirroring an inheritance hierarchy, so each domain class has a mapper that handles its own fields and delegates inherited ones upward.
- problem: Mapping code for a class hierarchy duplicates superclass field handling in every concrete mapper; organizing the mappers as a parallel hierarchy factors the shared mapping once.
- named-in: Patterns of Enterprise Application Architecture - Martin Fowler (2002)
- tags: enterprise, orm

### log-structured-storage — Log-Structured Storage
- aka: log-structured file system, LFS, append-only storage with segment cleaning, segment cleaning, copy-forward garbage collection, journal-structured storage
- kind: persistence-durability
- what: All updates are written as appends to the head of a sequential log divided into large segments; live data is never overwritten in place, and a cleaner process copies still-live records out of old segments to reclaim them.
- problem: Small random writes waste disk/flash bandwidth on seeks and read-modify-write cycles, and in-place update complicates crash recovery; turning the entire store into a sequential log makes writes device-speed and recovery a log replay, at the cost of background cleaning.
- named-in: Rosenblum & Ousterhout — The Design and Implementation of a Log-Structured File System, SOSP 1991 / ACM TOCS 1992
- tags: db, filesystem, flash, embedded (FTLs and flash filesystems are log-structured), borderline — kept separate from lsm-tree: LSM is a sorted-run merge index structure; log-structured storage is the persistence mechanism (append-only segments + cleaning) usable with no sorted-merge component at all (LFS, FTLs, journal-based KV stores)

### memory-image — Memory Image
- aka: system prevalence, object prevalence, prevalent system (Prevayler)
- kind: persistence-durability
- what: Keep the authoritative application state entirely in main memory and obtain durability by logging every state-changing event to persistent storage, replaying the log (accelerated by periodic snapshots) to rebuild state after restart.
- problem: Routing all state through a database costs IO and mapping complexity; when the working set fits in RAM, an event log plus snapshots gives durability while the program works at memory speed with plain in-memory structures.
- named-in: Fowler, bliki 'MemoryImage' (31 Aug 2011; loaded live — cites Prevayler/'system prevalence' and the LMAX architecture as realizations)
- tags: in-memory, event-log, borderline: composes event-sourcing + checkpointing/snapshot and Fowler frames it as an architectural approach; included because it is a single-process persistence mechanism with library-level realizations (Prevayler) and its own established name (system prevalence)

### metadata-mapping — Metadata Mapping
- aka: —
- kind: persistence-durability
- what: Holds the object-relational mapping details as metadata (tables/files or annotations) interpreted or code-generated at runtime, instead of hand-coding each mapper.
- problem: Dozens of hand-written mappers are repetitive and drift from the schema; expressing the mapping once as data lets generic code perform it uniformly.
- named-in: Patterns of Enterprise Application Architecture - Martin Fowler (2002)
- tags: enterprise, orm, borderline — Shades toward ORM-framework architecture; included as the in-program metadata-interpretation mechanism.

### query-object — Query Object
- aka: —
- kind: persistence-durability
- what: An object that represents a database query as a structure of criteria referring to domain classes, later translated into SQL.
- problem: Embedding SQL strings couples domain code to table schemas and duplicates query logic; building queries as interpretable objects lets them be composed, checked, and retargeted.
- named-in: Patterns of Enterprise Application Architecture - Martin Fowler (2002)
- tags: enterprise, orm

### repository — Repository
- aka: —
- kind: persistence-durability
- what: Mediates between the domain and data-mapping layers using a collection-like interface for accessing and querying domain objects.
- problem: Domain code that speaks SQL or mapper APIs directly couples business logic to storage; an in-memory-collection illusion isolates query construction and enables substitution in tests.
- named-in: Patterns of Enterprise Application Architecture - Martin Fowler (2002)
- tags: enterprise, orm, ddd, borderline — Sits at the domain/persistence seam and is sometimes treated as a layer element, but it is a class-level construct implementable inside one component; also a DDD tactical pattern (Evans 2003).

### row-data-gateway — Row Data Gateway
- aka: —
- kind: persistence-durability
- what: An object that acts as a gateway to a single database row, one instance per row, exposing the row's fields and its insert/update/delete operations.
- problem: Code that manipulates individual records needs record-shaped access without embedding SQL at every use site; a per-row gateway object gives record semantics while confining the database code.
- named-in: Patterns of Enterprise Application Architecture - Martin Fowler (2002)
- tags: enterprise, orm

### shadow-paging — Shadow Paging
- aka: shadow pages, shadow copy update
- kind: persistence-durability
- what: Perform updates on copies of pages and atomically switch a page-table root from the old (shadow) versions to the new ones at commit, never overwriting committed state in place.
- problem: Gives atomic, no-log crash recovery: a crash before the root switch leaves the intact shadow state; the cost is copying pressure and lost clustering, the classic alternative to write-ahead logging.
- named-in: Physical Integrity in a Large Segmented Database - Lorie (1977)
- tags: db, storage-engine, filesystems

### single-table-inheritance — Single Table Inheritance
- aka: —
- kind: persistence-durability
- what: Maps all classes of an inheritance hierarchy to one table whose columns are the union of all fields, with a type discriminator column.
- problem: Relational databases have no inheritance; one wide table avoids joins and moves objects between subclasses cheaply, at the cost of nullable unused columns.
- named-in: Patterns of Enterprise Application Architecture - Martin Fowler (2002)
- tags: enterprise, orm

### table-data-gateway — Table Data Gateway
- aka: —
- kind: persistence-durability
- what: An object that acts as the single gateway to a database table, with one instance handling all the rows and methods for the table's SQL.
- problem: Scattering SQL through application code makes schema change and testing painful; centralizing all queries for a table behind one stateless object confines the SQL to one place.
- named-in: Patterns of Enterprise Application Architecture - Martin Fowler (2002)
- tags: enterprise, orm

### tombstone — Tombstone
- aka: deletion marker, delete marker, timestamped deletion record
- kind: persistence-durability
- what: A persisted marker record written in place of an actual deletion in append-only or replicated storage, treated as a write that shadows earlier data and purged later by compaction after a grace period.
- problem: Log-structured and replicated stores cannot delete in place; without an explicit durable marker, deleted data resurrects from older segments or from replicas that missed the delete.
- named-in: Apache Cassandra documentation, 'Tombstones' (verified live); Kleppmann, Designing Data-Intensive Applications (log compaction chapter)
- tags: databases, storage engines, LSM, replication

### unit-of-work — Unit of Work
- aka: —
- kind: persistence-durability
- what: Maintains a list of objects affected by a business transaction and coordinates writing out the changes and resolving concurrency problems in one commit.
- problem: Writing objects back one at a time causes many small database calls, ordering problems, and inconsistent partial updates; changes must be tracked and flushed atomically.
- named-in: Patterns of Enterprise Application Architecture - Martin Fowler (2002)
- tags: enterprise, orm

### write-ahead-log — Write-Ahead Log
- aka: WAL, write-ahead logging, redo log, commit log, journaling, undo/redo logging
- kind: persistence-durability
- what: Append every intended change to a sequential durable log and force it to stable storage before the corresponding in-place data update, so committed work can be redone and uncommitted work undone after a crash.
- problem: In-place updates can be half-applied when a crash hits; sequential logging makes durability cheap (one sequential write) and gives recovery a total order of changes to replay or roll back.
- named-in: Transaction Processing: Concepts and Techniques - Gray & Reuter (1992)
- tags: db, storage-engine, filesystems


## Parsing & text processing — `parsing-text` (20)

### abstract-syntax-tree — Abstract Syntax Tree
- aka: AST, syntax tree
- kind: parsing-text
- what: A tree representation of parsed input that keeps semantic structure (operators, operands, constructs) while dropping concrete-syntax artifacts like punctuation and grouping tokens.
- problem: Later stages (analysis, interpretation, code generation, refactoring) need to traverse program structure repeatedly; a purpose-built tree decouples them from surface syntax and token order.
- named-in: Compilers: Principles, Techniques, and Tools (Dragon Book) - Aho, Lam, Sethi, Ullman (2006, 2nd ed.)
- tags: compilers, interpreters, tooling

### escape-sequence — Escape Sequence
- aka: character escaping, escape character, entity encoding (HTML/XML variant)
- kind: parsing-text
- what: Representing characters that are unrepresentable or syntactically significant in a textual context by a marker character followed by an encoded form (\n, \", &lt;), with matching unescaping on read.
- problem: Embedding arbitrary text inside delimited syntax (string literals, markup, CSV) collides with the delimiters themselves; a reserved escape marker makes any character representable, at the cost of escaping the marker too.
- named-in: Escape sequence - Wikipedia; escape sequences defined in ISO/IEC 9899 (C standard)
- tags: text-processing, security

### event-driven-parsing — Event-Driven Parsing
- aka: SAX-style parsing, push parsing, streaming parsing, pull parsing (StAX variant)
- kind: parsing-text
- what: A parser that emits a stream of callbacks/events (start-element, text, end-element) as it consumes input, instead of materializing a full document tree.
- problem: Building a complete in-memory tree (DOM-style) for large or unbounded documents costs memory proportional to the document; event streaming lets consumers process input incrementally in constant memory.
- named-in: Simple API for XML - Wikipedia (SAX, Megginson et al. 1998)
- tags: xml, streaming, text-processing

### lexer — Lexer
- aka: lexical analyzer, tokenizer, scanner
- kind: parsing-text
- what: A component that converts a raw character stream into a stream of classified tokens (identifiers, literals, operators), usually via maximal-munch matching driven by a finite automaton or hand-written switch.
- problem: Parsing directly over characters entangles grammar logic with whitespace, comments, and literal syntax; a separate tokenization stage gives the parser a clean, higher-level symbol stream.
- named-in: Compilers: Principles, Techniques, and Tools (Dragon Book) - Aho, Lam, Sethi, Ullman (2006, 2nd ed.)
- tags: compilers, interpreters, text-processing

### lr-parser — LR Parser
- aka: shift-reduce parser, bottom-up parser, table-driven parser, LALR / SLR parser (table-construction variants), yacc/bison-generated parser, GLR (generalized variant, folded)
- kind: parsing-text
- what: Bottom-up table-driven parsing: a state stack plus action/goto tables shifts input tokens and reduces recognized handles to grammar nonterminals.
- problem: Recursive descent cannot directly handle left recursion or many deterministic context-free grammars; generating a shift-reduce table mechanically from the grammar gives linear-time parsing with grammar-level maintainability.
- named-in: Aho, Sethi, Ullman, Compilers: Principles, Techniques, and Tools (the Dragon Book), ch. 4
- tags: compilers, canonical counterpart of recursive-descent-parser already in catalog

### maximal-munch — Maximal Munch
- aka: longest match rule, longest-prefix tokenization, maximal munch tokenization, longest lexeme rule
- kind: parsing-text
- what: The lexing rule that each token consumed is the longest prefix of the remaining input that matches any token pattern, restarting the automaton after each match (with backtracking or tabulation when a long attempt fails).
- problem: Token patterns overlap ('>' vs '>=', identifiers vs keywords); without a deterministic disambiguation rule tokenization is ambiguous, and naive longest-match backtracking can go quadratic - the named linear-time construction fixes that.
- named-in: Thomas Reps, "'Maximal-Munch' Tokenization in Linear Time", ACM TOPLAS 20(2), 1998; the longest-match rule also stated in Aho/Sethi/Ullman (Dragon Book)
- tags: compilers, lexing, borderline — rule-vs-mechanism: it is a disambiguation rule, but one realized as a concrete mechanism (DFA restart with last-accepting-state rollback) inside essentially every hand-written or generated lexer

### packrat-parsing — Packrat Parsing
- aka: PEG parsing, memoized recursive descent, parsing expression grammar parser
- kind: parsing-text
- what: Recursive descent over a parsing expression grammar (ordered choice, unlimited lookahead) with per-position memoization of intermediate results, giving linear-time parsing despite backtracking.
- problem: Backtracking parsers can go exponential re-parsing the same input; memoizing every (rule, position) result trades memory for guaranteed linear time and lets PEGs stay composable and unambiguous.
- named-in: Packrat Parsing: Simple, Powerful, Lazy, Linear Time - Bryan Ford (2002)
- tags: compilers, borderline — The PEG formalism itself is grammar notation (excluded as notation); packrat parsing is the implementable memoized-parsing mechanism and is kept.

### panic-mode-error-recovery — Panic-Mode Error Recovery
- aka: error synchronization, synchronizing tokens, error productions (related technique)
- kind: parsing-text
- what: On a syntax error, the parser discards input tokens until it reaches a designated synchronizing token (statement end, closing brace), then resumes parsing to report further errors in one pass.
- problem: Stopping at the first syntax error forces users into fix-one-recompile cycles, while naive continuation produces error cascades; synchronizing at stable grammar boundaries yields multiple meaningful diagnostics per run.
- named-in: Compilers: Principles, Techniques, and Tools (Dragon Book) - Aho, Lam, Sethi, Ullman (2006, 2nd ed.)
- tags: compilers, interpreters, error-handling

### parser-combinator — Parser Combinator
- aka: combinator parsing, monadic parsing, monadic parser
- kind: parsing-text
- what: Building parsers as first-class values composed with higher-order functions (sequence, choice, repetition), so the grammar is expressed directly as executable code.
- problem: Provides modular, testable, incrementally-buildable parsers inside the host language, avoiding external grammar files and generator build steps for mid-complexity input languages.
- named-in: Monadic Parser Combinators - Hutton & Meijer (1996)
- tags: fp, haskell, scala, rust, functional, text-processing

### pratt-parser — Pratt Parser
- aka: top-down operator precedence parser, operator-precedence parser, precedence climbing
- kind: parsing-text
- what: An expression parser that associates binding powers and parse functions (prefix/infix handlers) with token types, looping on precedence instead of encoding one grammar level per function.
- problem: Pure recursive descent needs one procedure per precedence level and deep recursion for expression grammars; driving the parse by token binding power handles arbitrary operators, precedence, and associativity in one compact loop.
- named-in: Top Down Operator Precedence - Vaughan Pratt (1973)
- tags: compilers, interpreters, expressions

### pretty-printer — Pretty-Printer
- aka: prettyprinting, code formatter, unparser
- kind: parsing-text
- what: A component that renders structured data or an AST back to formatted text, choosing line breaks and indentation against a target line width using grouping/fill primitives.
- problem: Emitting readable text from structure requires globally consistent break and indent decisions; a layout engine over logical blocks solves this once for all output (formatters, error printers, code generators).
- named-in: Prettyprinting - Derek C. Oppen, ACM TOPLAS (1980)
- tags: compilers, tooling, text-processing

### read-eval-print-loop — Read-Eval-Print Loop
- aka: REPL, interactive interpreter, language shell
- kind: parsing-text
- what: An interactive loop that reads one expression from the user, evaluates it in a persistent environment, prints the result, and repeats.
- problem: Batch compile-run cycles make exploration and debugging slow; an incremental read-evaluate loop with persistent state gives immediate feedback and interactive program construction.
- named-in: Read-eval-print loop - Wikipedia (term from the Lisp tradition)
- tags: interpreters, lisp, tooling

### recursive-descent-parser — Recursive Descent Parser
- aka: predictive parser (LL(1) special case)
- kind: parsing-text
- what: A top-down parser written as a set of mutually recursive procedures, one per grammar nonterminal, each consuming the tokens its rule derives.
- problem: Table-driven parsing machinery is heavyweight and opaque; mapping grammar rules directly onto call structure yields a parser that is hand-writable, debuggable, and easy to extend with good error messages.
- named-in: Compilers: Principles, Techniques, and Tools (Dragon Book) - Aho, Lam, Sethi, Ullman (2006, 2nd ed.)
- tags: compilers, interpreters

### regular-expressions — Regular Expressions
- aka: regex, regexp, pattern matching over text
- kind: parsing-text
- what: A declarative pattern notation for regular languages, compiled to a finite automaton (NFA/DFA) or backtracking matcher, used to search, validate, split, and rewrite text.
- problem: Hand-coding character-by-character scanning logic for each text pattern is verbose and error-prone; a compiled pattern language expresses match logic declaratively and reuses one matching engine.
- named-in: Regular Expression Search Algorithm - Ken Thompson, Communications of the ACM (1968)
- tags: text-processing, validation

### scannerless-parsing — Scannerless Parsing
- aka: scannerless generalized-LR parsing, SGLR, lexer-less parsing, character-level parsing, single-phase parsing
- kind: parsing-text
- what: Parsing without a separate lexer: lexical and context-free syntax are integrated into one grammar and the parser consumes individual characters, resolving token-level ambiguity with grammar-level disambiguation (follow restrictions, reject productions).
- problem: A separate scanner cannot use parsing context, which breaks on composed/embedded languages and context-sensitive tokens; folding lexing into the parser removes the lexer-parser interface mismatch at the cost of more ambiguity to manage.
- named-in: Eelco Visser, 'Scannerless Generalized-LR Parsing', Univ. of Amsterdam tech report P9707, 1997; term scannerless coined by Salomon & Cormack (SIGPLAN 1989)
- tags: compilers, grammarware, borderline — approach-vs-mechanism: it is a parser-construction strategy rather than a data mechanism, but named, recurring, and implemented inside single components (SGLR, PEG-based parsers are naturally scannerless)

### semantic-model — Semantic Model
- aka: —
- kind: parsing-text
- what: The in-memory model that a DSL parse populates and that the rest of the system executes against, kept deliberately separate from the parser and from any syntax tree.
- problem: Binding behavior directly to parsing (or to the syntax tree) entangles language processing with domain logic; a separate semantic model lets the same model be populated by multiple syntaxes, tested without parsing, and evolved independently of the grammar.
- named-in: Fowler, Domain-Specific Languages (Addison-Wesley, 2010), ch. 11; martinfowler.com/dslCatalog ('The model that's populated by a DSL', verified live 2026-07-10)
- tags: D, S, L,  , p, r, o, c, e, s, s, i, n, g, ;,  , p, a, i, r, s,  , w, i, t, h,  , a, b, s, t, r, a, c, t, -, s, y, n, t, a, x, -, t, r, e, e,  , (, t, h, e,  , s, y, n, t, a, x, -, s, i, d, e,  , r, e, p, r, e, s, e, n, t, a, t, i, o, n, ),  , a, n, d,  , e, m, b, e, d, d, e, d, -, d, o, m, a, i, n, -, s, p, e, c, i, f, i, c, -, l, a, n, g, u, a, g, e

### shunting-yard-algorithm — Shunting-Yard Algorithm
- aka: shunting yard, operator-stack expression parsing, two-stack infix parsing, infix-to-postfix conversion
- kind: parsing-text
- what: An iterative expression parser that uses an explicit operator stack (and output queue/operand stack) to convert infix input to postfix order or an AST, shunting operators aside until higher-precedence work completes.
- problem: Infix expressions with precedence and associativity need reordering before evaluation; an explicit-stack single pass handles arbitrary precedence tables without recursion, suiting calculators, spreadsheet formula engines, and stack-limited environments.
- named-in: E.W. Dijkstra, 'Making a Translator for ALGOL 60' / Mathematisch Centrum report MR 34/61 (1961); the railway shunting-yard name is Dijkstra's own
- tags: compilers, expression-evaluation, borderline — overlap with pratt-parser (whose aka already holds operator-precedence parser / precedence climbing): kept separate because the mechanism genuinely differs - iterative explicit-stack infix-to-postfix conversion vs recursive top-down parsing with binding powers; relation is alternative-to

### symbol-table — Symbol Table
- aka: scope table, environment (interpreter environments)
- kind: parsing-text
- what: A map from names to their declarations/attributes (type, storage, scope), typically organized as a stack or chain of per-scope tables to resolve lexically scoped lookups.
- problem: Compilers and interpreters must connect every use of a name to the right declaration under nesting and shadowing; a scoped name-to-binding structure centralizes resolution and attribute storage.
- named-in: Compilers: Principles, Techniques, and Tools (Dragon Book) - Aho, Lam, Sethi, Ullman (2006, 2nd ed.)
- tags: compilers, interpreters

### template-engine — Template Engine
- aka: template processor, text templating, templating engine, Template View (P of EAA web specialization), string template, template expansion, macro/template substitution
- kind: parsing-text
- what: Produce output text by interpolating data-model values and evaluating restricted directives (conditionals, loops, includes) inside a template document that fixes the static structure of the output.
- problem: Generating HTML, code, or reports by string concatenation entangles logic with presentation; a template engine separates the output's static shape from the data that fills it, ideally enforcing strict model-view separation.
- named-in: Parr, Enforcing Strict Model-View Separation in Template Engines (WWW 2004, StringTemplate); Fowler, Patterns of Enterprise Application Architecture (2002) names the web form 'Template View'
- tags: web, codegen

### tree-walking-interpreter — Tree-Walking Interpreter
- aka: AST interpreter, tree-walk interpreter
- kind: parsing-text
- what: An interpreter that executes a program by recursively traversing its abstract syntax tree, evaluating each node directly against a runtime environment.
- problem: Compiling to another representation costs implementation effort; evaluating the AST directly is the simplest correct execution strategy and keeps the interpreter structurally isomorphic to the language grammar, at the cost of dispatch overhead.
- named-in: Crafting Interpreters - Robert Nystrom (2021)
- tags: interpreters, languages


## Serialization, framing & encoding — `serialization-framing` (21)

### binary-to-text-encoding — Binary-to-Text Encoding
- aka: Base64, Base32, Base16/hex encoding, quoted-printable, ASCII armor
- kind: serialization-framing
- what: Re-encoding arbitrary bytes into a restricted printable-character alphabet (e.g. 6 bits per Base64 character, with padding) so binary data can traverse text-only channels.
- problem: Many channels and formats (email, JSON, URLs, config files, logs) only carry text safely; mapping bytes onto a safe alphabet trades ~33% size overhead for lossless transport through them.
- named-in: RFC 4648 - The Base16, Base32, and Base64 Data Encodings (2006)
- tags: text-processing, networking, interop

### bit-stuffing — Bit Stuffing
- aka: zero-bit insertion, HDLC bit stuffing
- kind: serialization-framing
- what: Inserting a 0 bit after every run of five consecutive 1 bits in payload so the flag pattern 01111110 can never occur inside a frame; the receiver removes stuffed bits.
- problem: Bit-level protocols (HDLC, CAN) delimit frames with a unique bit pattern and need clock-recovery transitions; stuffing guarantees the flag's uniqueness and bounds run lengths for synchronization.
- named-in: Computer Networks - Tanenbaum, Wetherall (2011, 5th ed.); mechanism defined in ISO/IEC 13239 (HDLC)
- tags: embedded, networking, datalink, can-bus

### byte-stuffing — Byte Stuffing
- aka: character stuffing, delimiter framing with escaping, SLIP ESC framing, HDLC byte stuffing, escape stuffing, SLIP/PPP escaping
- kind: serialization-framing
- what: Framing messages with a reserved delimiter byte (e.g. SLIP END 0xC0) and escaping any payload occurrence of the delimiter or escape byte via a substitution sequence, reversed on receive.
- problem: A delimiter-based frame boundary breaks when the delimiter value appears in binary payload; stuffing/escaping preserves binary transparency while keeping the receiver's resynchronization trivially simple after corruption.
- named-in: RFC 1055 - Nonstandard for Transmission of IP Datagrams over Serial Lines: SLIP - Romkey (1988)
- tags: embedded, networking, serial, c, protocols

### canonical-serialization — Canonical Serialization
- aka: deterministic encoding, distinguished encoding (DER), canonicalization (JSON Canonicalization Scheme)
- kind: serialization-framing
- what: Constraining a serialization format so each abstract value has exactly one legal byte encoding (fixed key order, minimal-length integers, normalized escapes), making encodings byte-comparable.
- problem: Signing, hashing, caching, and deduplication over serialized data break when equivalent values encode differently; a canonical form makes byte equality coincide with value equality.
- named-in: ITU-T X.690 - Distinguished Encoding Rules (DER); RFC 8785 - JSON Canonicalization Scheme (2020)
- tags: security, cryptography, binary-protocols, borderline — A property imposed on a format as much as a mechanism; kept because named standards (DER, JCS) exist specifically to implement it and designers build encoders around it.

### chunked-transfer-encoding — Chunked Transfer Encoding
- aka: chunked transfer coding, chunked framing
- kind: serialization-framing
- what: Framing a stream of unknown total length as a sequence of length-prefixed chunks terminated by a zero-length chunk, optionally followed by trailers.
- problem: Length-prefix framing requires knowing the full size up front, which streaming producers cannot; per-chunk lengths plus an explicit terminator let a sender stream indefinitely while receivers still detect truncation.
- named-in: RFC 9112 - HTTP/1.1 (2022), sec. 7.1 'Chunked Transfer Coding'
- tags: networking, http, streaming

### consistent-overhead-byte-stuffing — Consistent Overhead Byte Stuffing
- aka: COBS, byte stuffing (refines SLIP/HDLC-style escaping)
- kind: serialization-framing
- what: Encode packets so the frame delimiter byte never appears in the payload, with a small, fixed worst-case overhead, enabling unambiguous packet boundaries on byte streams.
- problem: Classic escape-based byte stuffing (SLIP/HDLC) can double packet size in the worst case, which breaks buffer and bandwidth budgets; COBS bounds overhead to one byte per 254 while keeping delimiter-free payloads.
- named-in: Consistent Overhead Byte Stuffing - Cheshire & Baker (IEEE/ACM Transactions on Networking, 1999)
- tags: embedded, networking, framing, serial, c

### delta-encoding — Delta Encoding
- aka: delta compression, differencing, delta timestamps
- kind: serialization-framing
- what: Storing or transmitting values as differences from a predecessor or baseline (previous sample, previous version, base frame) instead of absolute values.
- problem: Sequences with strong local correlation (timestamps, sensor readings, file versions) carry redundant absolute magnitude; encoding differences shrinks the representation and pairs naturally with varints and RLE.
- named-in: RFC 3229 - Delta Encoding in HTTP (2002); Delta encoding - Wikipedia
- tags: compression, telemetry, embedded, databases

### length-prefix-framing — Length-Prefix Framing
- aka: length-delimited encoding, length field framing, netstring, Pascal string (length-prefixed string)
- kind: serialization-framing
- what: Prefixing each message or field with its byte length so a receiver knows exactly how many bytes to read, delimiting records in a byte stream without inspecting payload content.
- problem: Byte streams (TCP, files, UARTs) have no message boundaries; an explicit length header restores boundaries with zero payload transformation, allowing binary-transparent payloads and preallocated reads.
- named-in: Protocol Buffers Encoding documentation - Google (living; 'length prefixes' / LEN wire type)
- tags: networking, embedded, binary-protocols

### magic-number-file-signature — Magic Number (File Signature)
- aka: file signature, magic bytes, format identifier, byte-order mark (text-encoding variant)
- kind: serialization-framing
- what: A fixed constant placed at the start of a file or message (0x7F'ELF', %PDF, 0xCAFEBABE) that identifies the format independent of names or metadata, often paired with a version field.
- problem: Consumers must cheaply reject wrong or corrupted inputs before parsing and dispatch on format without trusting file extensions; a distinctive leading constant provides both checks in a few bytes.
- named-in: Magic number (programming) - Wikipedia; List of file signatures - Wikipedia
- tags: file-formats, binary-protocols, robustness

### network-byte-order-handling — Network Byte Order Handling
- aka: endianness conversion, big-endian wire order, htons/ntohl idiom, byte swapping
- kind: serialization-framing
- what: Fixing a single byte order (conventionally big-endian) for multi-byte values on the wire or in files, with explicit host-to-wire conversion at serialization boundaries.
- problem: Hosts of different endianness reinterpret the same bytes as different numbers; declaring one canonical wire order and converting at the edges makes binary formats portable across architectures.
- named-in: RFC 791 - Internet Protocol, Appendix B: Data Transmission Order (1981)
- tags: networking, embedded, c, portability, borderline — Arguably a convention plus a pair of library calls rather than a mechanism; kept because cross-endianness handling is a named, recurring design obligation in every binary format.

### percent-encoding — Percent-Encoding
- aka: URL encoding, URI escaping
- kind: serialization-framing
- what: Encoding reserved or non-ASCII octets in a URI component as a percent sign followed by two hex digits, with context-dependent reserved sets per component.
- problem: URIs use characters like '/', '?', '&' as structural delimiters, so data containing them corrupts the URI's own syntax; %XX escaping embeds arbitrary octets while preserving parseability.
- named-in: RFC 3986 - Uniform Resource Identifier (URI): Generic Syntax (2005), sec. 2.1
- tags: web, text-processing, security

### run-length-encoding — Run-Length Encoding
- aka: RLE, run-length compression
- kind: serialization-framing
- what: Replacing runs of repeated values with a (count, value) pair, the simplest lossless compression scheme designers hand-roll for run-heavy data.
- problem: Data with long repeats (bitmaps, sparse buffers, sensor flatlines) wastes space stored literally; counting runs compresses it with trivial, allocation-free encode/decode suitable for constrained targets.
- named-in: Run-length encoding - Wikipedia (technique published by Robinson and Cherry, 1967)
- tags: compression, embedded, graphics, borderline — Edge of the compression-algorithm zoo (datastructures corpus territory); kept as the one run-compression element designers routinely implement inline rather than pull as a library.

### schema-evolution-via-field-tags — Schema Evolution via Field Tags
- aka: tagged fields, field numbers, forward/backward-compatible encoding
- kind: serialization-framing
- what: Identifying each serialized field by a stable numeric tag rather than by position or name, so encoders and decoders built against different schema versions can skip unknown tags and default missing ones.
- problem: Long-lived systems must exchange data between old and new code; stable tags plus skip-by-wire-type rules give forward and backward compatibility without lockstep upgrades.
- named-in: Designing Data-Intensive Applications - Martin Kleppmann (2017), ch. 4 'Encoding and Evolution'
- tags: binary-protocols, protobuf, thrift, borderline — Sits between a wire-format mechanism and a data-management policy; kept because the tag-and-skip mechanism is concretely implementable and named in a canonical text.

### serialization-proxy — Serialization Proxy
- aka: —
- kind: serialization-framing
- what: Serialize a small dedicated proxy object representing the logical state instead of the real object, reconstructing the real object through its public constructors on read.
- problem: Default serialization is an extralinguistic constructor that bypasses invariant checks and locks in representation; the proxy restores invariant enforcement and representation freedom.
- named-in: Effective Java - Joshua Bloch (3rd ed., Item 90)
- tags: java, oo, security

### serialized-lob — Serialized LOB
- aka: —
- kind: serialization-framing
- what: Persists an object graph by serializing it into a single large object (BLOB/CLOB) stored in one database field.
- problem: A hierarchic object cluster that is always read and written whole is painful to shred into relational rows; serializing the whole graph into one column trades queryability for simplicity.
- named-in: Patterns of Enterprise Application Architecture - Martin Fowler (2002)
- tags: enterprise, orm, borderline — As much a persistence-encoding decision as an in-program mechanism, but the serialize/deserialize machinery is implemented inside one component.

### serializer — Serializer
- aka: —
- kind: serialization-framing
- what: Stream objects into and out of arbitrary backends by pairing a Reader/Writer protocol with backend-specific concrete serializers, keeping the object graph traversal generic.
- problem: Objects must move across formats and media (files, network, databases) without embedding format knowledge in every class; the pattern isolates format behind a uniform protocol.
- named-in: Serializer - Dirk Riehle, Wolf Siberski, Dirk Baeumer, Daniel Megert, Heinz Zuellighoven, in Pattern Languages of Program Design 3 (1998)
- tags: oo

### sync-word — Sync Word
- aka: syncword, preamble, start-of-frame delimiter, sync character, training sequence
- kind: serialization-framing
- what: A known byte/bit sequence placed at the start of each frame that a receiver scans for to acquire frame (and sometimes clock) alignment in an undifferentiated stream.
- problem: A receiver joining or resynchronizing mid-stream has no idea where frames begin; a recognizable, low-false-positive marker sequence lets it lock onto boundaries and recover after corruption.
- named-in: Syncword - Wikipedia
- tags: embedded, networking, serial, wireless

### tolerant-reader — Tolerant Reader
- aka: —
- kind: serialization-framing
- what: A consumer-side reading strategy that extracts only the data elements it needs from a payload, ignores unknown or extra content, and makes minimal assumptions about structure.
- problem: Strictly schema-bound consumers break whenever a service provider evolves its message format; reading tolerantly (Postel's robustness principle applied to payload consumption) lets providers add or rearrange elements without breaking existing clients.
- named-in: Fowler, bliki 'TolerantReader' (9 May 2011; loaded live — notes Rob Daigneau published the full pattern in Service Design Patterns, Addison-Wesley 2011)
- tags: integration, schema-evolution, robustness, web-services

### type-length-value-encoding — Type-Length-Value Encoding
- aka: TLV, tag-length-value, KLV (key-length-value), identifier-length-contents (ASN.1 BER)
- kind: serialization-framing
- what: Encoding each data item as a type/tag code, a byte length, and the value bytes, so records are self-describing enough to be skipped, reordered, or extended without a shared positional layout.
- problem: Fixed positional layouts break when fields are added or when readers meet unknown fields; TLV lets old readers skip unknown types by length and lets messages carry optional fields sparsely.
- named-in: ITU-T X.690 - ASN.1 Basic Encoding Rules (BER/CER/DER); Type-length-value - Wikipedia
- tags: networking, embedded, binary-protocols, smartcards

### varint — Varint
- aka: variable-length integer, LEB128, variable-length quantity (VLQ), base-128 encoding
- kind: serialization-framing
- what: Encoding an integer in base 128 using 7 payload bits per byte with a continuation bit, so small values take one byte and the encoding is self-delimiting.
- problem: Fixed-width integer fields waste space when most values are small; a continuation-bit encoding sizes each value to its magnitude while still marking its own end without a length field.
- named-in: Protocol Buffers Encoding documentation - Google (living); LEB128 defined in the DWARF Debugging Information Format standard
- tags: binary-protocols, compression, protobuf, wasm

### zigzag-encoding — ZigZag Encoding
- aka: zig-zag integer encoding
- kind: serialization-framing
- what: Mapping signed integers to unsigned by interleaving positive and negative values (p -> 2p, n -> 2|n|-1) so small-magnitude negatives encode to small unsigned values.
- problem: Two's-complement negatives have all high bits set, so they encode as maximum-length varints; zigzag remaps them so varint length tracks magnitude for both signs.
- named-in: Protocol Buffers Encoding documentation - Google (living)
- tags: binary-protocols, protobuf, compression


## Numeric & precision — `numeric-precision` (10)

### arbitrary-precision-arithmetic — Arbitrary-Precision Arithmetic
- aka: bignum, multiple-precision arithmetic, big integer / BigInt, arbitrary-precision integers, GMP-style arithmetic
- kind: numeric-precision
- what: Represent and compute on integers (or rationals/decimals) whose size is limited only by memory, using multi-limb representations and carry-propagating algorithms instead of fixed-width machine words.
- problem: Fixed-width machine integers overflow; cryptography, computer algebra, financial and exact computation need results beyond 64 bits with exact semantics.
- named-in: Knuth, The Art of Computer Programming Vol. 2: Seminumerical Algorithms, sec. 4.3 'Multiple-Precision Arithmetic'
- tags: numerics, crypto

### checked-arithmetic — Checked Arithmetic
- aka: overflow-checked arithmetic, ckd_add/ckd_sub/ckd_mul (C23 stdckdint.h), __builtin_add_overflow (GCC/Clang), checked_add/overflowing_add (Rust), overflow detection, trapping arithmetic (variant)
- kind: numeric-precision
- what: Integer arithmetic operations that report overflow explicitly (a boolean flag or Option/panic) instead of silently wrapping or invoking undefined behavior.
- problem: Silent integer overflow corrupts computations and is a chronic security-bug source; detecting it at each operation lets the program reject, saturate, or widen instead of proceeding with a wrong value.
- named-in: ISO/IEC 9899:2024 (C23) <stdckdint.h> checked integer arithmetic macros; GCC integer overflow builtins; Rust std checked_* methods
- tags: C, Rust, numerics, security-adjacent, borderline — language-feature-vs-mechanism: standardized as library/intrinsic surface, but the mechanism (perform op, test overflow condition, branch) is language-independent and routinely hand-implemented where intrinsics are absent

### epsilon-ulp-float-comparison — Epsilon/ULP Floating-Point Comparison
- aka: approximate float equality, relative-epsilon comparison, AlmostEqualRelative, AlmostEqualUlps, ULP-based comparison, essentially equal (Knuth), tolerance comparison
- kind: numeric-precision
- what: Comparing floating-point values for near-equality using an absolute/relative epsilon tolerance or a bounded distance in units-in-the-last-place (ULPs) instead of exact ==.
- problem: Rounding error makes exact equality tests on floats unreliable; a fixed absolute epsilon is wrong across magnitudes, so comparisons must scale with the operands (relative epsilon) or count representable values between them (ULPs).
- named-in: Bruce Dawson, 'Comparing Floating Point Numbers, 2012 Edition' (randomascii.wordpress.com, 2012); ULP framing also in Knuth TAOCP Vol. 2 ('essentially equal') and Goldberg 1991
- tags: numerics, floating-point, borderline — mechanism-vs-practice: partly a coding practice, but the ULP-distance comparison is a concrete implementable mechanism (bit-pattern reinterpretation, adjacent-float counting) with named canonical realizations (AlmostEqualUlps)

### fixed-point-arithmetic — Fixed-Point Arithmetic
- aka: Q format, Qm.n arithmetic, binary scaling
- kind: numeric-precision
- what: Represent fractional values as scaled integers with an implicit binary point (Qm.n), doing real-number math with integer instructions.
- problem: Floating point is slow, large, or absent on many MCUs/DSPs and complicates certification; fixed-point gives fast deterministic fractional math at the cost of explicit range/precision management.
- named-in: corpus:labrosse — Embedded Systems Building Blocks - Labrosse (fixed-point math chapter)
- tags: embedded, dsp, c

### interval-arithmetic — Interval Arithmetic
- aka: interval analysis, interval computation, directed rounding intervals, validated numerics (field name)
- kind: numeric-precision
- what: Representing each numeric quantity as an interval [lo, hi] guaranteed to contain the true value, with arithmetic rules (and outward/directed rounding) that propagate the bounds through every operation.
- problem: Floating-point results carry unquantified rounding and input error; carrying rigorous lower/upper bounds through a computation yields a guaranteed enclosure of the exact result, at the cost of wider results and dependency-induced overestimation.
- named-in: Ramon E. Moore, 'Interval Analysis' (Prentice-Hall, 1966); standardized as IEEE 1788-2015
- tags: numerics, scientific-computing, borderline — algorithmics-zoo adjacency: kept as a design element because it is a representation choice a designer reaches for (bounded-error numeric type), standardized (IEEE 1788) and realized as reusable library types; the algorithm-variant zoo (Taylor models, affine arithmetic) stays in the sibling corpus

### kahan-summation — Kahan Summation
- aka: compensated summation, Kahan summation algorithm, Kahan-Babuška summation (variant), Neumaier summation (variant)
- kind: numeric-precision
- what: Accumulates a floating-point sum together with a running compensation term that captures the low-order bits lost by each addition, keeping total rounding error near machine epsilon instead of growing with n.
- problem: Naively summing many floating-point values accumulates rounding error proportional to the number of terms; compensated summation restores accuracy without resorting to wider arithmetic.
- named-in: Goldberg, 'What Every Computer Scientist Should Know About Floating-Point Arithmetic' (ACM Computing Surveys 1991; 'Kahan Summation Formula', Thm. 8); Higham, Accuracy and Stability of Numerical Algorithms (SIAM)
- tags: scientific computing, numerics, borderline — algorithm-variant adjacency (excluded by one hunter, added by another); kept as the one named designer mechanism for compensated float accumulation

### money — Money
- aka: —
- kind: numeric-precision
- what: A value object representing a monetary amount together with its currency, with allocation/rounding rules that conserve the total.
- problem: Representing money as bare floats loses cents to rounding and silently mixes currencies; a dedicated type enforces currency safety and distributes remainders deterministically.
- named-in: Patterns of Enterprise Application Architecture - Martin Fowler (2002)
- tags: enterprise, finance

### pseudorandom-number-generator — Pseudorandom Number Generator
- aka: PRNG, seeded random generator, deterministic random source, LCG / Mersenne Twister / xorshift / PCG (algorithm variants, folded)
- kind: numeric-precision
- what: A deterministic state machine that expands a seed into a stream of statistically random-looking numbers, giving reproducible randomness on demand.
- problem: Programs need randomness (simulation, games, sampling, testing) that is fast, portable, and — via the seed — exactly reproducible for replay and debugging; true entropy sources provide none of these.
- named-in: Knuth, The Art of Computer Programming Vol. 2: Seminumerical Algorithms, ch. 3 'Random Numbers'
- tags: simulation, games, testing, borderline: algorithm-flavored; included as the deterministic, seeded-reproducibility counterpart of the already-cataloged csprng, with algorithm variants folded into aka

### saturation-arithmetic — Saturation Arithmetic
- aka: saturating arithmetic, clamped arithmetic
- kind: numeric-precision
- what: Arithmetic in which results exceeding the representable range clamp to the minimum/maximum value instead of wrapping around.
- problem: Two's-complement wraparound turns small overflows into catastrophic sign flips in control and signal paths; saturating operations (often single DSP instructions) degrade gracefully at range limits.
- named-in: Saturation arithmetic - Wikipedia
- tags: embedded, dsp

### serial-number-arithmetic — Serial Number Arithmetic
- aka: sequence number wraparound comparison, RFC 1982 arithmetic
- kind: numeric-precision
- what: Compare fixed-width, wrapping sequence numbers using modular half-range rules so ordering remains correct across wraparound.
- problem: Naive comparison of wrapping counters (TCP sequence numbers, DNS serials, timestamps) breaks at rollover; half-range modular comparison keeps 'newer than' well-defined.
- named-in: RFC 1982: Serial Number Arithmetic - Elz, Bush (1996)
- tags: networking, dns, embedded


## Code structure & variant management — `code-structure` (11)

### composed-method — Composed Method
- aka: compose methods out of intention-revealing calls
- kind: code-structure
- what: Structure a method as a short sequence of calls to other intention-named methods, all at a single level of abstraction.
- problem: Long methods that mix abstraction levels are hard to read, reuse, and override; dividing behavior into small, identically-leveled named steps yields composable, self-documenting units.
- named-in: Beck, Smalltalk Best Practice Patterns (Prentice Hall, 1997), 'Composed Method'
- tags: smalltalk-origin, language-neutral, borderline — sits near practice territory (method-writing guidance), kept: a named pattern in a canonical pattern catalog describing a concrete code construct

### escaping-ifdef-hell — Escaping #ifdef Hell
- aka: conditional-compilation isolation, variant abstraction
- kind: code-structure
- what: Named patterns (avoid variants, isolated primitives, abstraction layer) that confine platform #ifdef variation to dedicated files behind common interfaces.
- problem: Scattered conditional compilation makes code unreadable and untestable; isolating variant points restores a single analyzable code path.
- named-in: corpus:preschern — Fluent C: Principles, Practices, and Patterns - Preschern (2022)
- tags: c, embedded, borderline — A chapter-level cluster of variant-management patterns cataloged as one element pending Phase-1 merge granularity decisions.

### feature-flag — Feature Flag
- aka: feature toggle, feature switch, toggle point, toggle router, release toggle / ops toggle / experiment toggle / permission toggle (variants), toggle point + toggle router (implementation elements), release/ops/experiment/permission toggles (categories)
- kind: code-structure
- what: A conditional branch point (toggle point) whose path is selected at runtime by a toggle router reading external toggle configuration, so a feature can be enabled or disabled without redeploying code.
- problem: Shipping latent or incomplete features, decoupling deployment from release, kill switches, and experiments all require switching code paths at runtime instead of maintaining long-lived branches.
- named-in: Hodgson, 'Feature Toggles (aka Feature Flags)', martinfowler.com, 2017 (verified live; names toggle point, toggle router, toggle configuration)
- tags: configuration, deployment, web, services

### generation-gap — Generation Gap
- aka: generated core class + hand-written subclass, regeneration-safe extension
- kind: code-structure
- what: Keep machine-generated code in a core base class that is never edited, and put all hand-written modifications in a subclass that survives regeneration unchanged.
- problem: Generated code is overwritten on every regeneration, destroying manual edits; separating generated and hand-written code by inheritance makes modifications durable across regenerations.
- named-in: Vlissides, 'Generation Gap', Pattern Hatching: Design Patterns Applied (1998; earlier C++ Report 1996)
- tags: code-generation, still standard in GUI builders / ORM / protocol-compiler output

### hot-code-reload — Hot Code Reload
- aka: hot code loading, code replacement (Erlang/OTP), dynamic software updating (DSU), hot swapping, live code reload, edit-and-continue (IDE variant)
- kind: code-structure
- what: Replaces a module's code in a running program, keeping old and new versions briefly coexistent and migrating state and in-flight control to the new version without a restart.
- problem: Restart-to-deploy loses process state and availability; long-running systems and interactive development need in-place replacement of code with controlled state handover.
- named-in: Erlang/OTP System Documentation, 'Code Replacement' (current/old code semantics; verified live); Hicks & Nettles, 'Dynamic Software Updating' (ACM TOPLAS 2005)
- tags: language runtimes, high-availability systems, development tooling, Erlang

### include-guard — Include Guard
- aka: header guard, #pragma once (non-standard alternative)
- kind: code-structure
- what: Preprocessor conditionals (or #pragma once) that make a header idempotent under multiple inclusion.
- problem: Multiple inclusion of a header causes redefinition errors; the guard is the established convention making header composition safe.
- named-in: corpus:preschern — Fluent C - Christopher Preschern (2022); also More C++ Idioms (Wikibooks)
- tags: c, c++, borderline — Preprocessor mechanics at the raw-syntax floor; kept because both Fluent C and the wikibook catalog it as a named pattern.

### method-object — Method Object
- aka: Replace Method with Method Object (Fowler, Refactoring), worker object, Replace Function with Command (Fowler, Refactoring 2nd ed.)
- kind: code-structure
- what: Reify a complex method as its own class: parameters and local variables become instance variables, the body becomes small methods on the new object.
- problem: A method whose many temporaries and parameters resist decomposition can be split freely once its working state lives in a dedicated object.
- named-in: corpus:fowlerref — Beck, Smalltalk Best Practice Patterns (1997), 'Method Object'; Fowler, Refactoring (1999) names the move 'Replace Method with Method Object'
- tags: smalltalk-origin, refactoring-target

### organizing-files-in-modular-c-programs — Organizing Files in Modular C Programs
- aka: header/implementation file organization, self-contained component files
- kind: code-structure
- what: Named patterns for splitting a C codebase into header/implementation files and directories so modules stay self-contained with explicit interfaces.
- problem: C offers no module system; without a file-organization discipline, include dependencies and hidden coupling erode modularity in large programs.
- named-in: corpus:preschernplop — Patterns for Organizing Files in Modular C Programs - Preschern (EuroPLoP 2020)
- tags: c, borderline — Pattern-collection granularity and code-organization (not runtime mechanism); included per charter, honest tag over silent exclusion.

### software-module-with-global-state — Software-Module with Global State
- aka: global-state module, instance-less module with file-scope state
- kind: code-structure
- what: Implement a module whose related functions operate on shared file-scope (static global) state inside the module, with initialization/cleanup functions for that state, while callers hold no instance at all.
- problem: Functions need common prepared resources (buffers, connections, config) but callers should not manage per-caller instances; one module-internal state blob serves all callers, trading simplicity for a single shared context.
- named-in: corpus:preschern — Fluent C ch. 5, 'Data Lifetime and Ownership' (Preschern 2022); also Preschern, 'C Patterns on Data Lifetime and Ownership' (PLoP paper)
- tags: c, borderline — sits near Singleton/Monostate (both in index) but is the instance-less C module form, named in its own right; do not fold - no object identity or class is involved

### stateless-software-module — Stateless Software-Module
- aka: stateless module, pure-function module
- kind: code-structure
- what: Provide a set of logically related functions that keep no state between calls: every resource a function needs is acquired and released inside the call, so the caller owns nothing and calls are independent.
- problem: Callers should not have to reason about initialization order, ownership, or hidden coupling between calls; making the module stateless eliminates those questions at the cost of ruling out cross-call caching or context.
- named-in: corpus:preschern — Fluent C ch. 5, 'Data Lifetime and Ownership' (Preschern 2022); also Preschern, 'C Patterns on Data Lifetime and Ownership' (PLoP paper)
- tags: c, borderline — module-structure decision close to a design principle, but named as a discrete pattern with a concrete C realization in two published sources

### x-macro — X-Macro
- aka: data/table-driven macro lists
- kind: code-structure
- what: A single macro list of entries is expanded multiple times with different definitions of X to generate parallel artifacts (enums, string tables, dispatch tables) from one source of truth.
- problem: Parallel lists (enum + names + handlers) drift apart under maintenance; the X-macro keeps them generated from one list.
- named-in: The New C: X Macros - Randy Meyers, C/C++ Users Journal (2001)
- tags: c, embedded


## Testing constructs — `testing-constructs` (11)

### four-phase-test — Four-Phase Test
- aka: setup-exercise-verify-teardown, Arrange-Act-Assert (AAA), Given-When-Then (BDD phrasing)
- kind: testing-constructs
- what: Structure every test as four ordered phases — fixture setup, exercise the system under test, result verification, fixture teardown — one behavior per test.
- problem: Unstructured test methods interleave setup, actions and assertions, hiding what is tested and leaking state between tests; a fixed phase skeleton makes intent and independence mechanical.
- named-in: Meszaros, xUnit Test Patterns (2007); xunitpatterns.com 'Four Phase Test' (verified live)
- tags: testing, borderline: test-code structuring pattern near the practice boundary; included on Meszaros catalog establishedness and the composed-method altitude precedent

### golden-master-testing — Golden Master Testing
- aka: approval testing, snapshot testing, characterization testing (legacy-code framing), reference-output testing, golden file testing
- kind: testing-constructs
- what: Captures the complete observed output of the system under test as a stored reference artifact (the golden master) and asserts that future runs reproduce it exactly, with an explicit approve-the-diff step when change is intended.
- problem: Legacy or complex-output code has no specification to assert against; recording current behavior as the oracle makes refactoring safe and turns output drift into a visible diff.
- named-in: Feathers, Working Effectively with Legacy Code (2004; 'characterization test'); ApprovalTests / approvaltests.com; 'snapshot testing' in Jest documentation (naming verified via live search this session)
- tags: testing, legacy code, UI/serializer outputs, borderline — technique-flavored, but included on the same footing as Test Double: it is a concrete test construct (stored reference artifact + comparator + approval step), not a process practice

### humble-object — Humble Object
- aka: humble dialog, humble executable
- kind: testing-constructs
- what: Strip hard-to-test code (GUI bindings, thread glue, framework touchpoints) down to a trivial 'humble' shell that immediately delegates all logic to a testable collaborator.
- problem: Logic embedded in untestable contexts (event handlers, ISRs, UI classes) cannot be unit-tested; extracting it leaves only trivially-correct glue untested.
- named-in: xUnit Test Patterns: Refactoring Test Code - Gerard Meszaros (2007)
- tags: testing, ui, borderline — Testability-driven structuring pattern; passes altitude as a concrete code-level construct, not a process practice.

### object-mother — Object Mother
- aka: —
- kind: testing-constructs
- what: A factory class dedicated to producing ready-made, semantically meaningful example objects (a standard customer, an overdue invoice) for use across many tests.
- problem: Complex domain objects are tedious to assemble in every test; a shared mother centralizes canonical test fixtures, at the cost of coupling tests to shared exemplars.
- named-in: ObjectMother: Easing Test Object Creation in XP - Peter Schuh, Stephanie Punke (XP Universe 2001); name coined on a ThoughtWorks project
- tags: testing, borderline — Test-support construction class; code-level construct in the testing domain.

### page-object — Page Object
- aka: Window Driver (Fowler's earlier eaaDev name), page object model (POM, Selenium usage)
- kind: testing-constructs
- what: A test-side object that wraps a UI page or fragment behind an application-specific API, so tests manipulate intention-revealing methods instead of raw HTML/widget structure.
- problem: UI-driving tests coupled directly to page structure break en masse on every markup change; a page object centralizes the UI knowledge in one place and keeps test logic readable and stable.
- named-in: Fowler, bliki 'PageObject' (10 Sep 2013; loaded live — states it was first described as Window Driver at eaaDev and popularized as 'page object' by Selenium); Selenium project documentation
- tags: testing, ui, web

### parameterized-test — Parameterized Test
- aka: table-driven tests (Go), data-driven test, test parameterization, row test
- kind: testing-constructs
- what: A single test-logic body executed once per row of a table of inputs and expected outputs, with each row reported as its own test case.
- problem: Many near-identical test methods differing only in data invite copy-paste divergence and under-coverage; separating the test logic from the example table makes adding cases one-line cheap and failures individually attributable.
- named-in: Gerard Meszaros, xUnit Test Patterns: Refactoring Test Code (2007) — 'Parameterized Test' (with 'Data-Driven Test' as the externalized-data variation); Go wiki 'TableDrivenTests'
- tags: go, cross-language, testing

### property-based-testing — Property-Based Testing
- aka: QuickCheck-style testing, generative testing, property testing, random testing with shrinking, generators and shrinkers
- kind: testing-constructs
- what: Tests state universally quantified properties of the code; a harness draws random inputs from composable generators, checks the property, and shrinks any failing input to a minimal counterexample.
- problem: Example-based tests only cover cases the author imagined; executable properties plus generated inputs explore the input space systematically and document intended laws of the API.
- named-in: Claessen & Hughes, 'QuickCheck: A Lightweight Tool for Random Testing of Haskell Programs' (ICFP 2000)
- tags: testing, functional programming heritage, now cross-language (Hypothesis, proptest, fast-check)

### service-stub — Service Stub
- aka: mock service
- kind: testing-constructs
- what: Removes dependence on a problematic external service during testing by substituting an in-process stand-in that implements the same gateway interface.
- problem: Slow, unreliable, or unavailable external services stall development and make tests nondeterministic; a local fake behind the same interface keeps work and tests running.
- named-in: Patterns of Enterprise Application Architecture - Martin Fowler (2002)
- tags: enterprise, testing

### test-data-builder — Test Data Builder
- aka: —
- kind: testing-constructs
- what: A builder with sensible defaults and fluent with-methods used in tests to construct complex objects, overriding only the fields relevant to each test.
- problem: Object Mothers proliferate variants and obscure which attributes matter to a test; a builder makes the significant values explicit while defaulting the rest.
- named-in: Test Data Builders: an alternative to the Object Mother pattern - Nat Pryce (2007); also in Growing Object-Oriented Software, Guided by Tests - Freeman & Pryce (2009)
- tags: testing, borderline — Test-support construction class; distinct mechanism from Object Mother (parameterized builder vs canned factory), so two entries.

### test-double — Test Double
- aka: mock object, test stub, fake object, test spy, dummy object
- kind: testing-constructs
- what: A substitute object installed in place of a production dependency during a test; the family spans dummy, fake, stub, spy, and mock by increasing behavioral sophistication.
- problem: Real dependencies make tests slow, nondeterministic, or unable to observe indirect inputs/outputs; a double controls the collaborator's behavior and records interactions.
- named-in: xUnit Test Patterns: Refactoring Test Code - Gerard Meszaros (2007)
- tags: testing, borderline — Folded mock/stub/fake/spy/dummy into one element per charter; kept IN as a code construct (a class you write), not a process practice.

### test-fixture — Test Fixture
- aka: Fresh Fixture, Shared Fixture, fixture setup
- kind: testing-constructs
- what: The arranged pre-test state (objects, data, environment) a test depends on, built fresh per test or shared across tests under an explicit strategy.
- problem: Tests need a known starting state that is cheap to build, isolated enough to prevent inter-test coupling, and expressive enough to read; fixture strategy is the named design decision governing that trade-off.
- named-in: xUnit Test Patterns: Refactoring Test Code — Gerard Meszaros (2007)
- tags: testing


## Embedded / systems — `embedded-systems` (16)

### a-b-firmware-image-update — A/B Firmware Image Update
- aka: dual-bank firmware update, A/B partitions, seamless update, golden image / rollback (variants)
- kind: embedded-systems
- what: Keep two firmware image slots; write the new image into the inactive slot, verify it, then atomically switch the boot selection, keeping the old image as instant fallback.
- problem: In-place firmware updates brick the device on power loss or a bad image; dual slots make updates atomic and reversible. Golden-image recovery slots, anti-rollback counters, and delta updates are folded here as variants.
- named-in: corpus:memfaultea — Device Firmware Update Cookbook - Memfault Interrupt
- tags: embedded, firmware-update, robustness

### bootloader-jump-handoff — Bootloader Jump / Handoff
- aka: jump to application, bootloader-to-app transition, vector table relocation on boot
- kind: embedded-systems
- what: A small boot program validates the application image, then hands off execution by loading the application's stack pointer and reset vector (relocating the vector table) and jumping to it with hardware in a known state.
- problem: Field-updatable and multi-image devices need a trusted first stage that can select, verify, and start an application image; the disciplined SP/PC/vector handoff is the mechanism that makes the transition safe and restartable.
- named-in: corpus:zerotomain — From Zero to main(): How to Write a Bootloader from Scratch - Memfault Interrupt (2019)
- tags: embedded, firmware-update, arm

### deferred-interrupt-processing — Deferred Interrupt Processing
- aka: top half / bottom half, ISR with deferred work, tasklet, deferred procedure call, deferred procedure call (DPC), interrupt handler split, PendSV-deferred processing, Deferred Interrupt Handling, bottom half, softirq, second-level interrupt handler (SLIH), work queue deferral
- kind: embedded-systems
- what: Split interrupt handling into a minimal ISR that acknowledges the hardware and queues work, plus deferred task-level code that completes the processing later.
- problem: Long ISRs increase interrupt latency and jitter for everything else; deferring the bulk of the work keeps interrupt context short while preserving responsiveness.
- named-in: corpus:ldd3 — Linux Device Drivers, 3rd ed. - Corbet, Rubini & Kroah-Hartman (2005)
- tags: embedded, os, concurrency, interrupts, c, os-kernel, overlap:embedded-scout

### device-driver — Device Driver
- aka: driver
- kind: embedded-systems
- what: A module encapsulating all interaction with one device class behind a uniform operations interface (open/read/write/ioctl or vendor API).
- problem: Hardware detail must be quarantined behind a stable interface so application logic stays portable and per-device knowledge lives in one place.
- named-in: corpus:ldd3 — Linux Device Drivers, 3rd ed. - Corbet, Rubini, Kroah-Hartman (2005)
- tags: c, embedded, systems, borderline — A component role more than a mechanism, but named, recurring, and implementable as one module - passes the altitude test on balance.

### direct-memory-access-dma-transfer — Direct Memory Access (DMA) Transfer
- aka: DMA, double-buffered DMA, DMA ping-pong, DMA double-buffer mode, circular DMA with half-transfer interrupt, DMA memory-pointer swap
- kind: embedded-systems
- what: Configuring a DMA controller to move data between peripherals and memory without CPU involvement, with completion signaled by interrupt; often paired with double buffering so one buffer fills while the other is processed.
- problem: High-rate I/O consumes the CPU if every word is moved by software; offloading transfers frees cycles and meets throughput deadlines.
- named-in: corpus:white — Making Embedded Systems - Elecia White (2024)
- tags: embedded, hardware-access, data-flow, dma, hardware-io

### hardware-adapter — Hardware Adapter
- aka: —
- kind: embedded-systems
- what: An adapter layer that converts the interface a hardware device (or its proxy) actually offers into the interface the application expects.
- problem: Applications written against one device interface must run with a different-but-similar device; the adapter absorbs the mismatch so neither client nor device code changes.
- named-in: corpus:douglasspatternsc — Design Patterns for Embedded Systems in C - Bruce Powel Douglass (2011)
- tags: embedded, hardware-access

### hardware-proxy — Hardware Proxy
- aka: —
- kind: embedded-systems
- what: A class/module that encapsulates all access to a hardware device behind a device-neutral interface, hiding register layout, encoding, and access mechanics.
- problem: Clients scattered with direct register access break whenever the hardware changes; centralizing access in one proxy isolates hardware detail and eases porting and testing.
- named-in: corpus:douglasspatternsc — Design Patterns for Embedded Systems in C - Bruce Powel Douglass (2011)
- tags: embedded, hardware-access

### interrupt-service-routine — Interrupt Service Routine
- aka: Interrupt Pattern, ISR, interrupt handler
- kind: embedded-systems
- what: Hardware-vectored handler code that preempts normal execution to service an event, doing minimal work at interrupt context before returning.
- problem: Urgent, asynchronous hardware events must be handled with low latency without the CPU wasting cycles waiting for them.
- named-in: corpus:douglasspatternsc — Design Patterns for Embedded Systems in C - Bruce Powel Douglass (2011)
- tags: embedded, concurrency, c, borderline — The handler construct itself is hardware-defined; included because ISR design rules (and ISR-with-deferred-work) are a named recurring design concern - the mission's anchor form.

### interrupt-vector-table — Interrupt Vector Table
- aka: IVT, vector table, exception vector table
- kind: embedded-systems
- what: A table of handler entry addresses, indexed by exception/interrupt number, through which the CPU dispatches to the right ISR; firmware populates and sometimes relocates it (e.g. VTOR).
- problem: Hardware must find the correct handler in bounded time for any interrupt source; a fixed-layout dispatch table is the universal mechanism, and its relocation underlies bootloaders and RAM-vectored systems.
- named-in: corpus:yiu — The Definitive Guide to ARM Cortex-M3 and Cortex-M4 Processors - Yiu (2013)
- tags: embedded, interrupts, c, borderline — Hardware-defined structure at the floor of the design band - kept IN per charter as the named dispatch construct firmware designs around.

### iohw-h-standard-hardware-i-o-interface — iohw.h Standard Hardware I/O Interface
- aka: <iohw.h>, standard I/O hardware addressing interface
- kind: embedded-systems
- what: A standardized C/C++ macro interface (iord/iowr on abstract register designators) that isolates device-register access from platform addressing details.
- problem: Register-access code is inherently platform-specific; a standard indirection layer lets driver logic port across buses and toolchains unchanged.
- named-in: corpus:tr18015 — ISO/IEC TR 18015:2006 Technical Report on C++ Performance, hardware-interface chapter
- tags: c, c++, embedded, borderline — A standardized API shape rather than a pattern; included as the TR-blessed portable hardware-access mechanism.

### memory-mapped-register-access — Memory-Mapped Register Access
- aka: memory-mapped I/O access, device register access in C, volatile register access, bit-banding (Cortex-M alias variant), MMIO device modeling, memory-mapped device access, volatile register struct
- kind: embedded-systems
- what: Address peripheral hardware registers as (volatile-qualified) memory locations through typed pointers or structure overlays, with disciplined read/write ordering.
- problem: Peripherals must be controlled from portable C/C++ without compiler-reordered or elided accesses; the volatile-pointer/struct-overlay discipline (plus hardware aids like Cortex-M bit-banding for atomic bit access) is the canonical mechanism.
- named-in: corpus:sakscolumns — Dan Saks embedded.com columns on memory-mapped devices in C and C++
- tags: embedded, c, cpp, hardware-io, c++

### pid-controller — PID Controller
- aka: PID control loop, proportional-integral-derivative controller, PI / PD controller (reduced forms), discrete PID with anti-windup
- kind: embedded-systems
- what: A periodic feedback loop computing an actuator command as the weighted sum of proportional, integral, and derivative terms of the setpoint error, implemented as a fixed-rate update with output clamping, integrator anti-windup, and derivative filtering.
- problem: Driving a physical process to a setpoint despite disturbances and lag needs a standard, tunable feedback structure; the discrete PID update is the established implementable one.
- named-in: Åström & Hägglund, PID Controllers: Theory, Design, and Tuning (ISA, 1995); Wescott, 'PID Without a PhD' (Embedded Systems Programming, 2000); Åström & Murray, Feedback Systems (Princeton UP)
- tags: embedded, control, robotics, borderline — control-theory algorithm rather than a software-structural pattern — included because embedded-software literature treats the discrete PID loop (anti-windup, derivative filtering, sample-time handling) as a named implementation-level building block a firmware designer reaches for

### polling — Polling
- aka: periodic polling, opportunistic polling, busy-wait polling, Polled I/O, status-flag polling, programmed I/O
- kind: embedded-systems
- what: The software repeatedly samples device or data status - periodically on a timer or opportunistically in the main loop - instead of being interrupted.
- problem: When events are frequent, non-urgent, or interrupts are unavailable/undesirable, checking on the program's own schedule is simpler and avoids preemption hazards.
- named-in: corpus:douglasspatternsc — Design Patterns for Embedded Systems in C - Bruce Powel Douglass (2011)
- tags: embedded, hardware-access, hardware-io

### shadow-register — Shadow Register
- aka: register shadowing, software register copy, hardware shadowed/buffered register (vendor variant)
- kind: embedded-systems
- what: Maintain a RAM copy of a hardware register's intended contents, perform all read-modify-write logic on the copy, and write the whole copy to the device.
- problem: Write-only registers cannot be read back and read-modify-write on live registers races with hardware (the PIC RMW problem); a software shadow makes register state knowable and updates atomic. Vendors also use 'shadow register' for hardware-buffered registers that latch atomically (e.g. PWM compare shadows) - noted as the hardware sense.
- named-in: Shadow Register - ScienceDirect Topics (Elsevier embedded-systems references); PIC/AVR vendor documentation
- tags: embedded, hardware-io, c

### super-loop — Super Loop
- aka: superloop, main loop, big loop, foreground/background system, while(1) scheduler
- kind: embedded-systems
- what: Structure the whole application as one endless main loop that calls each task function in turn, with ISRs as the only asynchronous activity.
- problem: Tiny systems need multitask-like behavior without the cost and complexity of an RTOS; a single repeating loop plus interrupts is the minimal, fully deterministic executive.
- named-in: corpus:pont — Patterns for Time-Triggered Embedded Systems - Pont (2001)
- tags: embedded, c, bare-metal

### typesafe-register-access-via-c-templates — Typesafe Register Access via C++ Templates
- aka: template register abstraction, register abstraction DSL, compile-time register access
- kind: embedded-systems
- what: Hardware registers and bitfields modeled as template types so illegal accesses fail at compile time while generated code equals hand-written volatile pokes.
- problem: Raw address-and-mask register code is unchecked and error-prone; encoding register semantics in the type system catches wrong-register/wrong-field bugs at zero runtime cost.
- named-in: corpus:kensmith — C++ Hardware Register Access Redux - Smith (2010)
- tags: c++, embedded


---

# Decision log

## Granularity, merge & altitude decisions

- SPLIT: transitive-aka fusion of super-loop / game-loop / event-loop / Message Dispatcher (chained via 'main loop' and 'message dispatcher' aliases) split into four elements; 'main loop' kept as alias only on super-loop (in embedded usage it names the superloop; the games/UI senses are folded into their own entries). Four genuinely different mechanisms: bare-metal task cycling (Pont/White), timestep-controlled update-render (Nystrom), event demultiplex-dispatch (event loop), and EIP's dispatcher-to-performers.
- SPLIT: Test Double (Meszaros) had fused into Null Object via shared 'stub' alias; restored as its own element under the new testing-constructs axis. Null Object keeps only 'Active Nothing' as alias. Special Case (PoEAA) kept as a separate element (Fowler's generalization: special-behavior subclasses beyond the null case) - the pair gets a specializes relation in Phase 3 rather than a fold.
- MERGE: message-queuing (Douglass Queuing + EIP Point-to-Point Channel) and Nystrom's Event Queue are one mechanism - canonicalized as message-queue with 'event queue' folded as alias. 'task mailbox' alias removed: Mailbox stays a separate element (bounded one-slot/small exchange object with RTOS semantics distinct from an unbounded FIFO channel).
- MERGE: segregated free lists folded into free-list as the size-class refinement (same naming source, Wilson et al. allocation survey); free-list assigned to resource-management (allocator role). TLSF stays a separate element (a specific named two-level policy, not a synonym).
- RENAME: element id 'protothreads' -> 'protothread' to avoid exact collision with the corpus work id 'protothreads' (Dunkels' paper); the element and the work stay linked via named-in.
- RENAME: canonical name for the version-validate-commit mechanism set to the established 'Optimistic Concurrency Control' (Kung & Robinson).
- RENAME: back-pressure -> backpressure (Reactive Streams spelling), Nygard's 'Back Pressure' kept as alias.
- CANONICALIZATION: the reference-count mechanism entry is named 'Reference Counting' (general mechanism); POSA1's Counted Pointer kept as the idiom alias rather than a second element - one mechanism, one entry. Smart Pointer remains separate (ownership-wrapper family: unique/shared/weak semantics, not only counting).
- FOLD: Python's context-manager protocol recorded as an alias of the Dispose pattern (same mechanism: deterministic scoped finalization hook) rather than a separate element.
- AXES: two axes added to the mission's twenty - code-structure (x-macro, include guard, modular C file organization, #ifdef variant-management patterns: source-level organization mechanisms with no better home) and testing-constructs (test double, service stub, object mother, test data builder, humble object: code-level constructs, not process practices). Kind overrides applied where scout votes split (watchdog->robustness-security, token/leaky bucket->scheduling-time, heartbeat->error-handling, checkpointing->persistence-durability, SBO->resource-management, etc.); kinds remain scaffolding, not ontology.
- KEEP-BOTH decisions (near-miss pairs that are genuinely distinct mechanisms): read/write/behind-through caches; wrapper-facade vs facade; static-factory-method vs factory-method; hardware-proxy/adapter vs GoF proxy/adapter; command vs command-processor; aggregator vs event-aggregator; leaky-bucket (shaper) vs leaky-bucket-counter (Hanmer error counter); bit-stuffing vs byte-stuffing; optimistic vs pessimistic offline lock; lookup (POSA3) vs lookup-table (LUT); loop-timeout (Pont, poll-loop bound) vs timeout (Nygard, blocking-call bound); shadow-paging vs paging (Noble-Weir); monad vs free-monad; visitor vs acyclic-visitor (published variant with its own forces); hooks (Noble-Weir ROM hooks) vs hook-method (Pree) vs ultimate-hook (Samek); delegation vs event-delegation (DOM); stack (structure) vs stack-first (Preschern allocation policy); reactive-programming (model umbrella) vs functional-reactive-programming (Elliott-Hudak) vs reactive-signals (fine-grained implementation) - specializes edges in Phase 3.
- ALIAS AMBIGUITY: 'main loop' names different mechanisms per community (embedded superloop / game loop / event loop) - resolved to super-loop only; search still finds the others by name.
- SPLIT: GoF Decorator had been folded into Adapter (both carry the GoF alias 'Wrapper'); restored as its own element. The shared alias is kept on both entries in annotated, non-colliding form.
- SPLIT: GoF Prototype had been folded into Factory Method ('Virtual Constructor' names Factory Method in GoF but also the C++ clone idiom); restored as its own element; the ambiguous alias annotated on Prototype, GoF's own 'Virtual Constructor' kept on Factory Method.
- SPLIT: ABA mitigation (tagged pointer / version counter beside a CAS-updated word) had fused into Reference Counting via the shared 'version counter' alias; restored as its own synchronization element - counting for reclamation and counting for ABA-detection are different mechanisms.
- SPLIT: Stream Windowing (Dataflow Model) had folded into UI list-virtualization via the bare 'windowing' alias; restored; the ambiguous alias dropped from both.
- MERGE: the two setjmp/longjmp error-handling entries (corpus-seed and idioms scouts) were one mechanism; merged as setjmp-longjmp-error-handling with Hanson's Except module and CException among the aliases.
- AKA: CRC no longer claims 'checksum' (broader family; additive checksums are recorded in CRC's note, not as a second element) nor 'message digest' (cryptographic-hash-function now exists and the conflation is an altitude error).
- AKA: 'latency compensation' removed from optimistic-ui-update - it is Bernier's netcode umbrella term (lag-compensation element).
- AKA: lsm-tree narrowed - 'log-structured storage engine' now names the distinct log-structured-storage element (LFS lineage: append + segment cleaning, no sorted-run merging).
- AKA: byte-stuffing no longer lists COBS or bit-stuffing as aliases - both are separate elements (COBS is a distinct algorithmic approach; bit stuffing is the bit-level HDLC variant).
- KEEP-BOTH: lru-cache (the concrete keyed structure: hash map + recency list) vs cache-eviction-policy (the policy family with LRU/LFU/CLOCK/ARC as named members) - structure vs policy; aliases disentangled; Phase 3 relates them.
- CONFLICT RESOLVED: Kahan summation - one hunter excluded it as algorithmics-zoo, another added it independently; editor keeps it borderline-tagged (the numeric axis's named mechanism for compensated accumulation); deeper variants stay with the datastructures corpus.
- KEEP: LMAX Disruptor kept as its own element against a fold-into-ring-buffer recommendation - a published, named mechanism (preallocated ring + sequence barriers + claim strategies) with its own naming source; Phase 3 relates it to ring-buffer.
- KEEP (block decision): the cryptographic-primitive band (cryptographic hash, MAC, AEAD, CSPRNG, nonce, salted password hashing) kept with borderline tags - designer-reachable named building blocks the rest of the catalog already presupposes (constant-time comparison, Merkle tree, secure zeroization); algorithm families (SHA-2 vs BLAKE3 etc.) stay out.
- ANCHOR COVERAGE: 'semantic data types' (mission calibration anchor) is not a published element name in any source checked (incl. White 2011/2024); the mechanism is covered by newtype (Whole Value folded as alias, Cunningham CHECKS 1994), value-object, quantity, and the new units-of-measure-types (Kennedy). 'Asynchronous programming models' anchor is covered by async-await-model + coroutine + future-promise + event-loop + proactor rather than one umbrella entry.
- HONEST GAP: MPU-based task/memory isolation (FreeRTOS-MPU, Zephyr user mode) is real practice but has no single established element name across vendors - not cataloged; revisit if a citable pattern name emerges. Power-management mechanism names beyond tickless idle (race-to-sleep etc.) similarly failed the establishedness gate.
- SPLIT: Expression Builder had folded into Semantic Model via an em-dash no-alias placeholder that normalized to an empty key (tooling bug, fixed); both Fowler DSL (2010) patterns restored as separate elements.
- KIND: fast-path (McKenney, Parallel Fastpath family) moved to execution-concurrency; SoA/AoS recorded as data-locality aliases per the final adversarial hunt.
- OVERRIDE: privilege separation was parked to architecture by the security hunter but added borderline by the final adversarial hunt (Provos et al. 2003); editor keeps it as a borderline design element - a single program restructuring itself into privileged/unprivileged halves is implementable at program level; the platform-topology sense stays parked.
- SATURATION RECORD: round 1 (19 scouts) 713 raw -> 577 merged; round 2 (10 hunters) +105; round 3 (5 strict lens hunters + mandated adversarial closer) +25, of which lens hunters contributed 2-4 each (mostly rejection records) and the adversarial closer 9 (4 borderline; its 5 non-borderline finds land in the pre-identified thin axes) - verdict SATURATED at the ~5-per-lens threshold; catalog frozen at 708. EWMA/median smoothing declined under the algorithm-zoo rule (flagged, editor concurs: DSP filter family belongs to the numerics/datastructures corpora).
- CITATION AUDIT: cross-checked all corpus:<id> naming citations against work titles; 6 miscitations fixed (dependency-injection, traits-class, CRTP, external-polymorphism, RAII had corpus ids belonging to works that teach-but-do-not-name them; null-object had inherited the fused test-double citation - restored to Woolf, PLoP). Works that teach an element without naming it stay in the element sources for the pass-8 mapping, not in named-in.

## Parked to the architecture realm (Phase 3 input)

Candidates the altitude test rejected upward; they enter the Phase 3 architecture catalog (or are dropped there with rationale).

- **Abstraction Layer / Hardware Abstraction Layer (Fluent C, Beningo)** — Fluent C names 'Abstraction Layer' for escaping #ifdef variant hell, but as a platform-spanning layer it states component/system structure - architecture realm (HAL).
- **Activator (POSA4)** — On-demand activation of services/processes (inetd-style); deployment/system-level resource mechanism.
- **Active-object framework (run-to-completion kernel)** — QP/QP++ 'active-object / inversion-of-control realization' is framework/kernel-level organization; the Active Object pattern itself is captured as a design element.
- **Ambassador** — Azure: out-of-process helper proxy for remote communication on behalf of a service - topology.
- **Anti-corruption Layer** — Strategic DDD: isolating translation layer between two systems' models - inter-system boundary structure (Evans 2003).
- **Application Controller** — Centralized point for application flow/navigation control - app-structure altitude.
- **Application Controller (POSA4, from PoEAA)** — App-level centralization of screen/action flow.
- **Application Switching (Noble & Weir)** — Splits the system into independent executables run one at a time - a statement of system-level structure, not an in-program mechanism (fails altitude test upward).
- **Authoritative Server model** — Client/server with server-authoritative simulation (vs peer-to-peer lockstep) is a system-topology decision, not an in-component mechanism; the in-component mechanisms it induces (prediction, reconciliation, lag compensation) are cataloged above.
- **Authoritative server with client-side prediction** — System-level netcode topology (who owns truth, how clients reconcile) - a statement about multi-node structure, not an in-process mechanism; the in-process piece (snapshot interpolation) is cataloged above.
- **Authorization (POSA4, from Yoder-Barcalow)** — Security-architecture pattern (policy enforcement structure across a system); Phase 3 / security territory.
- **AUTOSAR Virtual Function Bus / RTE** — Middleware/communication topology between components - squarely architectural.
- **Backends for Frontends** — Azure: per-frontend backend services - whole-system structuring.
- **Blackboard** — On Wikipedia's behavioral list but canonically a POSA1 architectural pattern - system-level knowledge-source structure.
- **Blackboard (POSA1)** — Architectural style for whole problem-solving systems with cooperating knowledge sources.
- **Blockchain / Merkle-chained distributed ledger** — System-of-nodes construct composing Merkle trees with consensus; the Merkle tree itself is cataloged as the design element.
- **Board Support Package (BSP)** — System-structure packaging of all board-specific support (simmonds/emb-arch); layer-level construct.
- **Bodyguard (das Neves & Garrido, PLoPD3)** — Sharing and protecting objects across address spaces in distributed systems without full RPC; distribution-level.
- **Bootloader** — Named in zerotomain ('How to Write a Bootloader from Scratch'); a whole-program/system role and boot topology rather than an intra-program mechanism.
- **Bounded Context** — Strategic DDD: explicit boundary within which a model applies - system-decomposition altitude (Evans 2003).
- **Bounded Context (Evans DDD; Fowler bliki 2014)** — Strategic-design decomposition of a large model/system into contexts with explicit boundaries — system-structure altitude, Phase 3 (belongs with the DDD strategic set alongside already-parked Service Layer etc.).
- **Broker (POSA1/POSA4)** — Distributed-system topology / middleware structure.
- **Broker Pattern (RTDP/POSA1)** — Intermediary-based distributed system topology - POSA1 architecture canon.
- **Canonical Data Model** — Enterprise-wide agreement on a common data format to minimize translator count (EIP); cross-system data governance, not an implementable mechanism.
- **Chained Processors** — 
- **Channel Adapter** — Connects an application that was not built for messaging to the messaging infrastructure (EIP); a system-integration topology element.
- **Channel Architecture Pattern / Channel Pattern (RTDP ch4, DPESC ch6 base form)** — Organizes the system as sequential data-transformation channels; the base channel concept is system structure (its safety refinements Protected Single Channel and Dual Channel were kept as design elements per charter).
- **Claim Check / Sequential Convoy / Messaging Bridge / Asynchronous Request-Reply / Choreography** — Azure/EIP system-messaging patterns - inter-service; EIP scout may claim mid-level subsets.
- **Client Proxy (POSA4)** — Broker-decomposition middleware role for remote invocation infrastructure.
- **Client Request Handler (POSA4)** — Broker-decomposition middleware transport role.
- **Client Session State** — System-level decision to hold session state on the client - state-placement across tiers (PoEAA).
- **Client-Server (DPESC ch1)** — System-level role topology between requesters and providers.
- **Competing Consumers** — Azure/EIP: multiple consumer instances on a shared channel - system-scale messaging.
- **Compilation pipeline (multi-pass compiler structure)** — The lexer->parser->analyzer->codegen decomposition is a whole-program pipes-and-filters structure - system-level shape, not a single implementable mechanism; its stages (lexer, parser, AST) are cataloged as elements.
- **Component-Based Architecture / ROOM Pattern (RTDP)** — Whole-system component structuring per ROOM methodology - architecture altitude.
- **Compute Resource Consolidation** — Azure: packing tasks into deployment units - deployment-level.
- **Container (POSA4)** — Component-hosting execution infrastructure (EJB/CCM-style); system-level runtime structure.
- **Context Map** — Strategic DDD: map of bounded contexts and their relationships - system-level structure (Evans 2003).
- **Control Bus** — Separate management/monitoring channel overlay for administering a distributed messaging system (EIP system management); operations topology.
- **CQRS** — Command Query Responsibility Segregation - splitting a system's read and write models is an architecture style (Fowler bliki 2011; Greg Young).
- **Data Bus Pattern (RTDP)** — System-wide shared communication backbone topology.
- **Database Session State** — System-level decision to hold session state in the database - state-placement across tiers (PoEAA).
- **Dataflow programming (as a system paradigm)** — As a whole-system execution paradigm/topology it is architecture-realm; the in-program design elements it decomposes into (collection pipeline, FRP) are cataloged here.
- **Datatype Channel** — Channel-per-datatype organization convention for a messaging system (EIP); a channel-topology design decision, not a mechanism.
- **Decoupling Middleware** — Nygard stability pattern; choosing middleware topology to decouple systems is architectural.
- **Defense in Depth / Compartmentalization (as structure)** — System-structuring principle; layered independent controls is an architecture-level statement
- **Demilitarized Zone, Packet Filter Firewall, Proxy-Based Firewall (Schumacher et al.)** — Network security topology patterns from the same catalog; clearly architecture realm
- **Deployment Stamps / Geode** — Azure: replicated deployment units / geo-distributed nodes - deployment topology.
- **Distributed hash table (Chord/Kademlia/DHT)** — System-level overlay topology built atop consistent hashing; the routing overlay is a multi-node structure, not implementable inside one component.
- **Distributed replicated log (Kafka-style commit log)** — As a cluster-wide ordering/replication backbone it is a topology; the in-process append-only log / WAL mechanism belongs to the persistence scout.
- **Distributed Snapshot / Checkpoint Barrier (Chandy-Lamport; Flink Asynchronous Barrier Snapshotting)** — 
- **Domain Model** — Way of organizing domain logic as an interconnected object model - domain-logic organization, app-structure altitude (PoEAA).
- **Domain Model (POSA4)** — Application-scale organization of business logic (Fowler PoEAA origin); statement about whole-app structure.
- **Domain Object (POSA4)** — Component-partitioning construct for structuring applications around self-contained domain concepts.
- **Durable Subscriber** — Subscription persistence so a disconnected subscriber misses no messages (EIP); a QoS feature of messaging infrastructure.
- **Dynamic Object Model / Adaptive Object Model (Riehle, Tilman & Johnson, PLoPD5)** — Yoder/Johnson describe it as an architectural style; its design-level constituents (Type Object, Property/attribute objects, Strategy, Interpreter) are already in the catalog.
- **Elm Architecture** — aka Model-View-Update (MVU); whole-app structure (model/update/view triad) from the Elm guide - app-structure altitude.
- **Error Containment Barrier** — Hanmer architectural pattern; primarily prescribes structural boundaries for error propagation across the system.
- **Event Collaboration (Fowler, eaaDev 'Focusing on Events')** — Components coordinate by broadcasting events instead of making requests — as a cross-component interaction style this is event-driven architecture's territory (Phase 3); its in-process mechanisms are already cataloged (observer, event-aggregator, domain-event, message-queue).
- **Event Sourcing** — Azure: append-only event store as the system of record - data-architecture level (db scout may claim a mechanism-level form).
- **Event Sourcing (architecture style)** — The system-wide event-sourced-system style (event store as backbone, projections, replay across services) - the in-component persistence mechanism is cataloged as element event-sourcing.
- **Event-driven architecture (event-driven OS)** — TinyOS is characterized as a 'tiny event-driven OS' - style-level; the event-loop design element belongs to other scouts' territory.
- **Failover** — Hanmer pattern; switching service to a redundant unit is primarily a system-level structure/tactic (per charter directive: park if system-level).
- **Fault Observer** — Hanmer pattern; a system-wide component collecting and publishing fault reports - topology-level.
- **Federated Identity / Valet Key** — Azure: cross-system authentication delegation / token-based direct resource access - system-level security structures.
- **Firewall Proxy (POSA4)** — Network security topology element.
- **Five-Layer Architecture Pattern (RTDP)** — A specific whole-system layering template for embedded/real-time applications.
- **Flux** — Facebook's application architecture for unidirectional data flow (dispatcher/store/view) - app-structure altitude; Redux/centralized-store is its best-known descendant.
- **Front Controller** — Single handler consolidating all request handling for a web application - app-structure altitude.
- **Front Controller (POSA4, from PoEAA)** — Web-application structuring pattern; app-level control topology.
- **Function-as-a-Service / serverless functions** — Deployment and topology construct ('functions' as unit of system decomposition); architecture realm, Phase 3.
- **Gatekeeper** — Azure: dedicated validating host between clients and backends - deployment topology for security.
- **Gateway Aggregation / Gateway Routing / Gateway Offloading** — Azure: system-edge gateway structures - topology.
- **Graceful Degradation** — System-level quality tactic (SRE / Bass availability tactics); realized by design elements like load shedding and circuit breaker but itself a system property.
- **Graceful Degradation / Degraded Mode** — 
- **Guaranteed Delivery** — Persistence-backed delivery quality-of-service of the messaging infrastructure (EIP); a system-level guarantee rather than an in-process mechanism.
- **Half-Object + Protocol (HOPP)** — PLoP (Meszaros 1995): splitting an object across address spaces with a protocol between halves - distribution structure.
- **Half-Sync/Half-Async** — POSA2 labels it an architectural pattern: it layers an entire concurrent system into synchronous and asynchronous service layers with a queueing layer between - system structuring, not an in-component mechanism.
- **Hardware Abstraction Layer (HAL)** — Named across beningofw/CMSIS/White as a structural layer of the system, not an intra-component mechanism - Phase 3 architecture realm (bridge target for facade-backend, device-driver, register-access elements).
- **Health Check (endpoint)** — Per charter directive; a service-exposed liveness/readiness probe is a system/operations integration construct (cf. heartbeat, which stays design-level).
- **Health Check API** — Richardson (microservices.io) names it, but it is a service-topology observability endpoint contract, not an in-program mechanism; belongs in the Phase 3 architecture realm.
- **Health Endpoint Monitoring** — Azure: externally-probed health checks - operational/system monitoring structure.
- **Heterogeneous Redundancy Pattern (RTDP)** — Diversely implemented redundant channels against systematic faults - system-level safety architecture.
- **Hierarchical Control Pattern (RTDP)** — System-wide distribution of control policy across a hierarchy of controllers.
- **HLA Run-Time Infrastructure / federated simulation** — IEEE 1516 federation of simulators is system-level structure; only its interest-management/DDM mechanism passes the altitude test (included above).
- **Homogeneous Redundancy Pattern (RTDP)** — System-level replication of identical channels for fault tolerance.
- **Index Table / Materialized View** — Azure: data-tier query structures - data-architecture; db scout may claim mechanism-level forms.
- **Integration Styles (File Transfer, Shared Database, Remote Procedure Invocation, Messaging)** — EIP's root-level styles for connecting applications; pure architecture-realm vocabulary for Phase 3.
- **Interface definition language / schema-first contract (IDL)** — Generating serializers from a shared schema contract (protobuf .proto, ASN.1, CORBA IDL) is a cross-component contract-and-toolchain structure; the wire mechanisms it emits are cataloged individually.
- **Intrusion Detection System** — Infrastructure component observing systems from outside
- **Invoker (POSA4)** — Broker-decomposition middleware role (server-side dispatch machinery).
- **Islands Architecture** — Page-level structure for partial hydration (Astro et al.); the hydration mechanism itself is cataloged as a design element.
- **Kernel-bypass networking (DPDK, user-space network stacks)** — A restructuring of the whole I/O path across OS/application boundary - deployment/system-structure decision, not implementable inside one component.
- **Layered firmware architecture (driver/HAL/middleware/application)** — The layering itself is architectural structure; only the HAL interface construct was kept as a borderline design element (corpus: lacamera, beningodesign).
- **Layered game engine runtime architecture** — Gregory-style engine layering (platform/core/resources/gameplay) is whole-system structure; encountered while sourcing scene graph, belongs to the Phase 3 architecture realm.
- **Layered Pattern (RTDP)** — System-level organization of the whole software stack into abstraction layers - architecture style, POSA1/RTDP canon.
- **Layered software architecture** — AUTOSAR Classic layered architecture and Noergaard's layered model are canonical architecture-style statements (MCAL -> ECU abstraction -> services -> RTE).
- **Layers (POSA1)** — Whole-system structuring into abstraction levels - the canonical architectural pattern.
- **Leader Election** — Azure: coordination across distributed instances - distributed-systems mechanism above component level.
- **Limp-home / degraded mode operation** — System-level behavioral policy for continuing service under fault (automotive lexicon); the in-program safe-state transition is cataloged instead.
- **Log shipping / replication log (primary-replica replication)** — Reuses the WAL as a system-level replication channel between nodes - statement of system structure, feeds Phase 3 (named in Kleppmann DDIA).
- **Maintenance Interface** — Hanmer pattern; a separate management/maintenance channel beside the application interface - architectural interface decision.
- **MapReduce** — Dean & Ghemawat 2004 - a cluster-scale programming model plus execution framework/topology; the in-program kernel of it is covered by master/worker + pipeline elements.
- **Message Broker** — Central intermediary topology that decouples all senders from all receivers system-wide (EIP); primarily a statement of system-level structure.
- **Message Bus** — Shared enterprise-wide bus connecting many applications via common channels and data model (EIP); an architecture style, not an in-process mechanism.
- **Message Channel (POSA4, from EIP)** — Inter-system messaging infrastructure role; middleware topology.
- **Message Endpoint (POSA4, from EIP)** — Inter-system messaging infrastructure role.
- **Message Router (POSA4, from EIP)** — Inter-system routing topology element.
- **Message Translator (POSA4, from EIP)** — Inter-system integration role (format mediation between systems).
- **Messaging Bridge** — Connects two separate messaging systems so messages flow between them (EIP); inter-system topology.
- **Microkernel** — seL4/L4 papers named in emb-arch; OS architecture style, feeds Phase 3.
- **Microkernel (POSA1)** — Platform/product-line level system structure (minimal core plus extensions).
- **Microkernel Architecture Pattern (RTDP)** — Whole-system structuring around a minimal core plus plug-in services - architecture altitude.
- **Model View Controller** — Whole-app UI structure splitting an application into model, view, and controller responsibilities - app-structure altitude (PoEAA web presentation family).
- **Model-View-Controller (MVC)** — Discussed in GoF chapter 1 as the motivating example, but it is a whole-application/UI structural decomposition (Smalltalk-80 lineage) - fails the altitude test upward; feed to Phase 3. GoF itself decomposes MVC into Observer, Composite, and Strategy, which are cataloged here.
- **Model-View-Controller (POSA1)** — Application-level structuring of interactive systems.
- **Model-View-Intent (MVI)** — Reactive app-structure variant (cycle.js lineage) of unidirectional data flow - Phase 3 with the MV* family.
- **Model-View-Presenter (MVP)** — App-structure variant of MVC (Potel; Fowler's Passive View and Supervising Controller are its sub-variants) - Phase 3.
- **Model-View-ViewModel (MVVM)** — App-structure pattern (Gossman, Microsoft WPF) built on data binding; the binding mechanism is cataloged as a design element, the structure parks here.
- **Monitor-Actuator (channel pair)** — Douglass safety pattern in the same Preschern EuroPLoP 2013 safety pattern system: separate actuation channel and monitoring channel as distinct components - architecture-level channel structure (index's dual-channel and protected-single-channel cover the in-component mechanisms).
- **Monitor-Actuator Pattern (RTDP)** — Paired actuation and monitoring channels - channel-pair system structure for safety.
- **MV* family (Model-View-Controller, MVP, MVVM)** — Osmani's JS pattern catalog includes MV* patterns, and none appear in the element index under any alias; they are GUI architectural patterns (POSA1 names MVC an architectural pattern). Parked so Phase 3 verifies the architecture realm covers them - flagged here because their total absence from the design index is conspicuous.
- **Object Synchronizer (Silva, Pereira & Marques, PLoPD4)** — Synchronization policy for distributed object replicas; distribution-level.
- **Page Controller** — Per-page request-handling structure for a web application - app-structure altitude.
- **Page Controller (POSA4, from PoEAA)** — Web-application structuring pattern; app-level control topology.
- **Partitioning / sharding** — Distribution of a dataset across nodes is system-level structure (DDIA ch. 6); the in-component analogue (hash partitioning of an in-memory structure) would be a different, unnamed-at-this-altitude candidate.
- **Pipes and Filters (integration style)** — As EIP presents it: system-level composition of processing steps connected by channels; the in-process pipeline/pipes-and-filters idiom is a distinct design-level element for the concurrency/POSA scout.
- **Pipes and Filters (POSA1)** — Architectural style: dataflow topology of a whole processing system (the in-process pipeline mechanism is a separate, smaller element other scouts may carry).
- **Policy Decision Point / centralized authorization service (XACML PEP/PDP/PIP)** — Distributed authorization topology; its in-process kernel is covered by reference-monitor
- **Polyglot Persistence (Fowler/Sadalage, bliki 2011)** — Using different datastore technologies per data need across a system — data-architecture stance, Phase 3 territory.
- **Presentation Model** — Fowler GUI-architecture pattern (2004) - app-structure separation predecessor of MVVM.
- **Presentation-Abstraction-Control (PAC)** — POSA 1 architectural pattern - hierarchical agent decomposition of an interactive system, system-structure altitude.
- **Presentation-Abstraction-Control (POSA1)** — Hierarchy of cooperating agents structuring a whole interactive application.
- **Privilege Separation (Provos et al.)** — Splits a program into privileged monitor and unprivileged worker processes — multi-process system structure, not in-process; distinguished from privilege bracketing (which is in-process and included)
- **Process Manager** — Central workflow/orchestration engine maintaining process state across multi-step message flows (EIP); system-level control structure.
- **Process Pairs** — Gray (1985, Tandem); primary/backup process structure with takeover - system-level redundancy organization.
- **Protocol layering / encapsulation stack** — Nesting each layer's PDU inside the next (headers-around-payload) is a system structuring principle for communication stacks; the per-layer framing mechanisms (stuffing, TLV, length prefixes) are the design-level elements.
- **Publish-Subscribe (as system topology)** — GoF lists Publish-Subscribe as an aka of Observer (in-process, IN and folded into the observer entry's aka); pub-sub as a distributed messaging/system topology is architecture-level and belongs to Phase 3 - the name lives in both realms per the mission's same-name-two-realms rule.
- **Publisher-Subscriber** — Azure: system-scale async messaging topology; in-process pub-sub is covered by Observer/Event Aggregator in the design realm.
- **Query optimizer / query planner** — Named recurring construct but primarily a component role in DBMS system structure (Hellerstein et al. 2007 anatomy) rather than a reusable design mechanism; parked rather than dropped.
- **Queue-Based Load Leveling** — Azure: queue as buffer between services - inter-service topology (in-process message queue is a separate design element owned elsewhere).
- **Recursive Containment Pattern (RTDP)** — Recursive system decomposition strategy - statement about system structure.
- **Recursive Control (Selic, PLoPD3)** — Structuring pattern for whole real-time control systems (hierarchy of control components); system-level structure, fails altitude upward.
- **Redundancy (spatial/temporal/informational)** — Hanmer architectural pattern; provisioning redundant units is an availability tactic / system structure, not an in-program mechanism.
- **Redundant channel structures (TMR, dual-channel 1oo2, homogeneous/heterogeneous redundancy)** — Replication topologies across channels/processors are system-level fault-tolerance structure (Douglass channel patterns; IEC 61508).
- **Reflection (POSA1)** — Two-level meta/base architecture for self-modifying systems - system-level structure in POSA1's formulation.
- **Remote Facade** — Coarse-grained facade over fine-grained objects to serve remote calls - primarily about distribution-boundary structure (PoEAA).
- **Replicated Component Group (POSA4)** — System-level replication structure for availability/scalability.
- **Reporting Database (Fowler, bliki 2004)** — Separate database fed from the operational store for reporting/analytics — system-level data topology, fails altitude upward.
- **Requestor (POSA4)** — Broker-decomposition middleware role (client-side invocation machinery).
- **Routing Slip** — Itinerary attached to a message driving it through a system-level sequence of processing steps (EIP); trends architectural (dynamic workflow across components).
- **Safety Executive** — Douglass safety pattern cataloged in Preschern/Kajtazovic/Kreiner 'Building a Safety Architecture Pattern System' (EuroPLoP 2013, ACM 10.1145/2739011.2739028): a centralized safety monitor component coordinating fail-safe shutdown across subsystems - system-level structure, fails the altitude test upward.
- **Safety Executive Pattern (RTDP)** — Centralized system-wide safety coordinator managing shutdown/recovery across subsystems.
- **Safety tactics catalog (Wu-Kelly, via Preschern's GSN tactic analysis)** — Preschern's EuroPLoP 2013/2019 safety-pattern-system papers organize patterns under safety tactics (condition monitoring, degradation, replication/diversity redundancy, repair...) - tactics are Phase 3 architecture-realm material; the implementable members (sanity check, watchdog, N-version, dual channel) are already in the design index.
- **Saga** — Distributed long-lived transaction decomposition with compensations (Garcia-Molina & Salem 1987; Richardson); cross-service coordination topology, not an in-program element.
- **Saga / Compensating Transaction** — Garcia-Molina & Salem (1987); long-lived transaction structure spanning services - architecture-level failure handling (flagging for Phase 3; may also belong to a persistence scout).
- **Sandbox / process sandboxing (seccomp, pledge, jails)** — OS-enforced isolation topology around a process, not a mechanism inside it
- **Scheduler Agent Supervisor** — Azure: distributed action coordination and recovery - multi-service structure.
- **Search-engine index tier (index + query fan-out architecture)** — The inverted index is cataloged; the sharded index-serving tier around it is architecture.
- **Secrets management service / vault** — Infrastructure for credential storage and distribution
- **Secure channel / Secure Pipe (TLS)** — Inter-system communication security infrastructure (Core Security Patterns 'Secure Pipe')
- **SEDA (Staged Event-Driven Architecture)** — Welsh et al. 2001 - a whole-service structure of event-driven stages connected by queues with per-stage admission control; primarily a statement of system-level structure (charter directs it here).
- **Self-Contained Component (Fluent C, Organizing Files chapter)** — Prescribes directory/component structure and dependency direction across modules - code-organization at component granularity, feeds the architecture catalog.
- **Server concurrency models (iterative, process-per-connection, preforked, prethreaded server)** — Stevens UNP ch. 30 catalogs these as whole-server structural alternatives - system-level structure, not an in-component mechanism; feed Phase 3 (relates to thread pool, Leader/Followers).
- **Server Request Handler (POSA4)** — Broker-decomposition middleware transport role.
- **Server Session State** — System-level decision to hold session state in server memory - state-placement across tiers (PoEAA).
- **Service Layer** — Layer defining an application's boundary of available operations - explicitly a layer construct, architecture altitude (PoEAA).
- **Service-oriented architecture (AUTOSAR Adaptive ara::com)** — Report names AUTOSAR Adaptive as 'POSIX-based service-oriented architecture' - style-level.
- **Session State placement trio: Client Session State / Server Session State / Database Session State (PoEAA)** — 
- **Sharding** — Azure: horizontal partitioning of a data store - data-architecture.
- **Sharding / data partitioning scheme** — System-level data-distribution decision across nodes; the in-process hash-ring structure is cataloged, the cluster partitioning strategy is Phase 3's.
- **Shared Repository (POSA4)** — System integration style: components coordinate through a central data store.
- **Shared-nothing architecture** — Per-CPU/per-thread sharding scaled to whole-system partitioning (Stonebraker's shared-nothing) is a statement of system structure, not an in-component mechanism.
- **Shared-nothing parallel database architecture** — Whole-system partitioning/topology decision (Stonebraker 1986 'The Case for Shared Nothing') - clearly architecture realm.
- **Shed Work at Periphery** — Hanmer overload pattern; prescribes WHERE in the system to shed load (at the edge) - a placement/topology statement; the mechanism itself is the load-shedding element.
- **Sidecar** — Azure: auxiliary component deployed as a separate process/container alongside the main application - deployment topology.
- **Single Access Point + Check Point (Yoder & Barcalow, PLoPD4)** — Presented as 'Architectural Patterns for Enabling Application Security'; application-entry security structure, Phase 3 territory.
- **Single Sign-On / third-party authentication (Kerberos, OAuth/OIDC topology)** — Cross-system identity federation topology
- **Small Architecture (Noble & Weir pattern group)** — The 'small architecture' group of Small Memory Software states memory-conscious system structure; its member mechanisms (pools, overlays, compression) are design-level.
- **Someone in Charge** — Hanmer architectural pattern; assigns system-wide responsibility for fault-handling actions - structural/organizational.
- **Spatial/temporal partitioning (ARINC 653 / IMA)** — Platform-level isolation architecture between applications; MPU/MMU enforcement is configuration of system structure (corpus: arinc653, rushby).
- **Split top-half/bottom-half driver architecture (as OS structuring principle)** — The per-driver mechanism is IN as deferred-interrupt-handling; the kernel-wide layering of all drivers into halves is a statement of system structure for Phase 3.
- **Static Content Hosting / External Configuration Store** — Azure: moving content/config to external services - deployment decisions.
- **Strangler Fig** — Azure/Fowler: incremental legacy-system replacement strategy - system migration structure.
- **System Monitor** — Hanmer detection pattern; a dedicated monitoring component watching the rest of the system - system-level structure.
- **Table Module** — Way of organizing domain logic with one class per table - domain-logic organization, app-structure altitude (PoEAA).
- **Template View** — Web-presentation rendering structure (markup with embedded markers) - app-structure altitude.
- **Template View (POSA4, from PoEAA)** — Web presentation-layer structure; app-structure flavored - a Fowler-focused scout may reclaim it downward.
- **Time-Triggered Architecture (Kopetz)** — System/network-level computation and communication architecture (TTA, TTP); the in-program TTC scheduler element is cataloged, the architecture goes to Phase 3 (corpus: kopetzbauer).
- **Time-Triggered Architecture (TTA)** — Kopetz-Bauer TTA is a system-level architecture; its in-program counterpart is captured as the time-triggered-scheduler design element.
- **Time/space partitioning (ARINC 653 / IMA)** — Partitioning of applications across an RTOS/hypervisor is system-level structure (APEX API, Rushby partitioning report).
- **Transaction Script** — Way of organizing all domain logic as procedures per request - domain-logic organization, app-structure altitude (PoEAA).
- **Transactional Outbox** — Reliable event publication across a database + broker boundary; inherently a multi-component reliability topology (Richardson names it); park for Phase 3.
- **Transform View** — Web-presentation rendering structure (transform domain data element by element into HTML) - app-structure altitude.
- **Transform View (POSA4, from PoEAA)** — Web presentation-layer structure; app-structure flavored - a Fowler-focused scout may reclaim it downward.
- **Triple Modular Redundancy (TMR)** — Lyons & Vanderkulk (1962); hardware/system-level redundancy with voting; software analog covered by n-version-programming element.
- **Triple Modular Redundancy Pattern (RTDP)** — Three-channel voting redundancy - system-level safety architecture.
- **Two Step View** — Two-stage page-rendering structure (logical page then formatting) - app-structure altitude.
- **Two-Phase Commit** — 
- **Two-phase commit (2PC)** — Atomic commit protocol coordinating multiple independent participants across a system - a distributed/system-structure protocol, not a single-component mechanism (Gray & Reuter name it; Phase 3 candidate).
- **Unidirectional Data Flow** — App-wide data-flow discipline umbrella (Flux/Elm/MVI family) - a constraint on system structure, not an in-component mechanism.
- **Units of Mitigation** — Hanmer architectural pattern; defines the system's recovery-unit decomposition - a structural statement.
- **Virtual Machine Pattern (RTDP)** — Douglass presents it as an architecture pattern (portable system atop an abstract machine); the interpreter mechanism itself belongs to the GoF/language scouts.

## Notable exclusions (not elements)

- **ABI machinery (AAPCS calling conventions, name mangling, Itanium __cxa runtime, vtable layout, static-init guards)** — Compiler/runtime contract, not designable elements; charter routes ABI machinery to ops.
- **Abstract Class (Woolf, PLoPD4)** — Design principle / language-feature usage guidance, not a nameable mechanism.
- **Account lockout, session-ID regeneration, password policy (OWASP)** — Narrow operational practices/policies under security-session and password mechanisms, below element granularity
- **Accounting patterns: Account, Accounting Entry, Accounting Transaction, Replacement/Reversal/Difference Adjustment (Fowler eaaDev/Analysis Patterns)** — Domain analysis/modeling patterns for a specific business domain — analysis-pattern altitude, not implementation mechanisms; money (the value-representation mechanism) is already cataloged.
- **ACID properties / SQL isolation levels (read committed, repeatable read, serializable)** — Correctness semantics and contract taxonomy, not implementable mechanisms (Haerder & Reuter 1983; Berenson et al. 1995); snapshot isolation alone was admitted as the mechanism-shaped borderline.
- **Active Object (POSA2)** — Samek's core execution model, but POSA2 is its canonical naming source - left to the POSA/concurrency scout to avoid duplicate entry.
- **Active queue management (RED, CoDel)** — Network-infrastructure queue policy running in routers; algorithm family rather than an in-process design element.
- **algebraic data type (ADT)** — DECISION LOG (charter-directed): NOT a separate umbrella entry. ADT = sum types + product types; the design element is tagged-union (which carries the sum side and the aliases); product/record types are raw language syntax. Recorded here so the decision is auditable.
- **Allowed Lateness** — 
- **Anemic Domain Model (Fowler bliki 2003)** — Anti-pattern/smell, not a design element; catalog excludes anti-patterns.
- **Anti-patterns (God Object, Big Ball of Mud, Poltergeist, magic numbers, cloud antipattern catalog)** — Charter rule: anti-patterns are not elements; Azure maintains a separate antipatterns catalog.
- **AoS/SoA layout** — 
- **API-design bliki vocabulary: Command Oriented Interface, Duck Interface, Required Interface, Typed Collection, User Defined Field, Courtesy Implementation, Decorated Command, Interface Implementation Pair, Seal, Getter Eradicator, Flag Argument, Constructor/Setter Initialization** — Checked against the live API-design tag page: essays, language-feature discussions, or already folded (Flag Argument = aka on function-control; constructor/setter injection = aka on dependency-injection; Seal's mechanism = sealed-trait; Typed Collection is a dated pre-generics workaround). None survives as a distinct absent mechanism.
- **ARIES** — A specific published recovery algorithm (Mohan et al. 1992), not a distinct design element - its ideas (WAL, fuzzy checkpointing, redo/undo passes) are folded into the write-ahead-log and checkpointing entries.
- **ASLR (address space layout randomization)** — OS loader/kernel security facility, not implementable inside one program.
- **ASLR, DEP/W^X, CFI, shadow stack, pointer authentication** — Platform/compiler/hardware mitigations a program enables rather than implements; NOTE: index precedent stack-canary is also compiler-inserted — editor may want to revisit the boundary either way
- **Asset hot-reload** — Live reloading of changed assets/code is development-workflow tooling (pass-7 practice territory), not a shipped-program mechanism.
- **Asynchronous Programming Models (mission anchor phrase)** — Umbrella term, not one mechanism. Covered in the index by async-await-model, coroutine, future-promise, event-loop, proactor, green-threads, protothread, continuation-passing-style. Anchor considered covered; nothing added.
- **Atomic RMW primitives (CAS/LL-SC/fetch-and-add instructions)** — Raw hardware/language primitives below the band; the in-scope elements are the idioms built on them (CAS retry loop, tagged pointer).
- **Authenticator (Fernandez; Schumacher I&A patterns)** — Decision-level/abstract pattern; the implementable mechanisms are check-point, salted-password-hashing, security-session
- **Automated Garbage Collection (POSA4)** — Language-runtime memory management facility - below the design band as normally consumed (platform feature, not a design element one implements).
- **B+ tree, counting/cuckoo/XOR filters, Roaring bitmap, red-black/AVL/splay/treap, Patricia/radix trie, Fibonacci/pairing heaps, suffix tree, octree, R* variants, CHAMP, HLL++** — Variant-zoo entries folded into their role-level elements' aka/notes per charter; the datastructures sibling corpus owns variant-level enumeration.
- **Barton-Nackman trick** — Historical CRTP application (folded into CRTP note per one-element-per-mechanism rule).
- **Binary search / sorting** — 
- **Binding Properties (charter seed, attributed to Grand 1998)** — Attribution did not verify live: Wikipedia's 'Binding properties pattern' credits Victor Porton, not Grand, and searches of Grand's Patterns in Java vol 1 contents did not surface it. The mechanism (synchronize properties across objects via change observers) is the indexed data-binding element (aka already includes 'property binding'). Recommend adding 'Binding Properties' and 'bound properties (JavaBeans API spec 1.01, 1997)' to data-binding's aka rather than creating a duplicate.
- **Biquad filter / block-based audio processing** — 
- **BNF / EBNF / PEG grammar notation** — Specification notation, not an implementable mechanism; the implementable side of PEG is kept as packrat parsing.
- **Branch By Abstraction (Fowler bliki 2014)** — Transitional technique for large-scale change on trunk (introduce abstraction, migrate implementations, remove scaffolding) — change-sequencing practice, not a runtime mechanism.
- **Bulk Synchronous Parallel (BSP)** — Valiant 1990 - an abstract bridging/cost model of parallel computation, not an implementable in-program mechanism; its in-program echo is the barrier element.
- **Cache Warming** — Named (cache warm-up/pre-warming) but primarily an operational practice of pre-populating a cache before serving traffic; its mechanism substance is already covered by the existing prefetching and refresh-ahead-cache entries.
- **Caller-Owned Instance (Fluent C ch. 5)** — Mechanism is fully covered by the combination of existing index entries opaque-pointer (First-Class ADT with create/destroy already in its aka) + dedicated-ownership; proposing it would duplicate. Suggest adding 'Caller-Owned Instance (Fluent C)' as an aka on dedicated-ownership.
- **Canary Release / Blue-Green Deployment / Dark Launching / Keystone Interface (bliki)** — Release-engineering and deployment practices — pass-7/ops territory, not design elements (feature-flag, the enabling mechanism, is already cataloged).
- **Card table / card marking as a separate element** — Folded into gc-write-barrier as the dominant implementation variant per one-element-per-mechanism (GC Handbook treats card tables as a write-barrier implementation, sect. 11.8).
- **Cascade (Beck SBPP)** — Smalltalk message-cascade syntax (';'); raw language syntax. The general mechanism is covered by fluent-interface (in index).
- **Chaos Engineering / fault injection in production** — Practice/discipline (Principles of Chaos Engineering), pass-7 process territory.
- **Checksum / CRC / frame check sequence trailer** — Integral to real framing schemes but robustness-security territory (integrity checking); expected from that scout - flagged so the framing-integrity pairing is not lost.
- **Clock Wrapper (Fowler bliki)** — Injectable abstraction over the ambient time source for testability — application of dependency-injection + test-double to one dependency (time); fold, optionally as aka ('fake/virtual clock') on test-double.
- **Code Locking / Data Locking / Data Ownership (McKenney, PLoPD2)** — Already covered: coarse-grained-lock, lock-striping, and thread-specific-storage (which carries 'data ownership' as aka).
- **Collation** — Locale-aware string ordering (Unicode Collation Algorithm, UTS #10) is a facility/standardized service you configure and call, not a mechanism you implement inside one program; fails the altitude test sideways (library/platform facility, like Unicode normalization).
- **Command Message / Document Message / Event Message** — EIP's message-intent taxonomy; sub-classifications of Message folded into the message entry's aka rather than three separate elements.
- **Command Query Separation / Tell Don't Ask / Uniform Access / Hollywood Principle (bliki)** — Principles/guidelines, not mechanisms (DI, the mechanism behind Hollywood Principle, is already cataloged).
- **Command-response protocol over serial links** — 
- **Compiler Explorer codegen inspection (Godbolt)** — Verification method/tooling, not a design element.
- **Composed Method (Beck)** — Code-style/refactoring guidance at raw-code altitude, not a reusable mechanism.
- **Constant pool** — JVM-spec structure recurring across VMs (CLR metadata, CPython co_consts), but spec-internal representation detail; adjacent to symbol-table and sharing/interning already in index.
- **Content Security Policy / same-origin policy** — Browser-platform policy configuration, not an in-process mechanism of the application
- **Contract Test (Fowler bliki 2011)** — Testing strategy verifying a test double (or provider) matches the real contract (consumer-driven contracts, Pact) — cross-component testing practice rather than an in-program construct; excluded at strictness peak.
- **Controlled / uncontrolled components** — React-framework-specific idiom for where form state lives; folded conceptually under data binding rather than cataloged.
- **Counting Handle / Resource Cache / Resource Pool / Task Coordinator / Virtual Proxy (POSA4 names)** — POSA4 renames of already-cataloged mechanisms; folded as aka into Counted Pointer, Caching, Pooling, Coordinator, and Proxy respectively.
- **CQRS (verification, not a new decision)** — VERIFIED already parked: merged_design.json carries the poeaa-ddd scout's park ('splitting a system's read and write models is an architecture style, Fowler bliki 2011; Greg Young') plus the wiki-longtail duplicate. No action needed.
- **CQS / CQRS** — 
- **crt0 / startup code / .bss-.data initialization** — Toolchain/runtime bring-up (zerotomain, picolibc picocrt) - ops territory.
- **currying / partial application** — Language-level calling-convention technique, below the altitude band; not an in-program design mechanism in its own right.
- **Data Clump (Fowler, Refactoring)** — Code smell, not a mechanism; refactoring/practice territory.
- **Data-oriented design** — A design philosophy/methodology broader than any single mechanism; its concrete cacheable-layout mechanism is captured as the Data Locality element.
- **Dead reckoning** — Strongest near-miss cut at the 15 cap: IEEE 1278 (DIS) standardizes dead-reckoning algorithms for entity-state extrapolation; genuinely established and distinct from client-side prediction; recommend a follow-up scout adopt it.
- **Debug command interpreter / serial CLI shell (command table)** — 
- **Decimal floating point (IEEE 754-2008)** — 
- **Default Visitor / Extrinsic Visitor (Nordberg, PLoPD3)** — Visitor variants; fold as aka under visitor (in index).
- **Defensive Programming** — Umbrella practice (McConnell); its concrete mechanisms are cataloged individually (assertions, parameter checking, fail fast).
- **Demand paging / virtual memory** — OS facility spanning hardware and kernel; the in-process analog is lazy loading / lazy initialization (creational scout).
- **Descriptor Protocol (Python)** — Named (Python data model; Hettinger's Descriptor HowTo Guide) but a language feature - the attribute-access hook mechanism of the interpreter, akin to 'virtual' - below the design-element band.
- **Design principles (SOLID, Law of Demeter, DRY)** — Principles/heuristics, not implementable named mechanisms.
- **Design-for-change / information hiding (White, Parnas)** — Principle; realized concretely by the opaque-type element.
- **Detour, Smart Proxy, Message History, Message Store, Test Message, Channel Purger** — EIP system-management instrumentation for operating a messaging system; operational/practice-level rather than in-process design mechanisms (Wire Tap, the one with clear in-process recurrence, was kept IN).
- **Diff / patch (Myers diff, edit script computation)** — Myers — An O(ND) Difference Algorithm and Its Variations (Algorithmica 1986) is algorithmics zoo per the scope rules; the designer-facing mechanism (representing changes as deltas) is already carried by delta-encoding (aka differencing) in the index. Patch application adds no separate implementable mechanism at catalog altitude.
- **DMA cache-coherence maintenance (clean/invalidate discipline)** — Real recurring discipline (LDD3, ARM docs) but a hardware-correctness protocol tied to cache architecture; left for the OS/systems scout to weigh.
- **Dual-target testing / TDD for embedded (Grenning)** — Process/practice; its in-code enabler (test double) was included borderline.
- **Dynamic Invocation Interface (POSA4)** — CORBA-style runtime-composed invocation API; middleware-internal vocabulary with little life outside ORBs - recorded, not cataloged.
- **eaaDev frozen drafts: Agreement Dispatcher, Parallel Model, Retroactive Event, Event Poster, Eager Read Derivation, Proposed Object, Request-Response Collaboration, Autonomous View, Presentation Chooser, Money Bag, Time Point** — Development-only drafts of the frozen (2006) eaaDev material — fail the establishedness gate for a strictness round (no recurrence beyond Fowler's drafts); Time Point additionally folds into the cataloged temporal family (temporal-property, range).
- **EAFP / LBYL (Python)** — Named in the Python glossary but a coding style dichotomy (try/except-first vs check-first), not an implementable mechanism.
- **Echo Back (CHECKS)** — UI interaction feedback (redisplay interpreted input for user verification); interaction-design guidance rather than an implementable software mechanism — fails the altitude test sideways.
- **Encapsulated Context (Kelly, PLoPD5)** — Same mechanism as context-object (in index); recommend aka merge.
- **Encapsulated Implementation (POSA4)** — Restates the encapsulation/information-hiding principle rather than naming a distinct implementable mechanism.
- **Entity interpolation / snapshot extrapolation** — Already covered: index snapshot-interpolation carries 'entity interpolation' as aka; the extrapolation side enters as dead-reckoning above.
- **Enum singleton (Effective Java Item 3)** — Folded per charter: an implementation note on the GoF Singleton element, not a separate mechanism.
- **errgroup-style bounded concurrency (Go)** — golang.org/x/sync/errgroup is a library facility; its general mechanisms are structured concurrency (proposed this round) plus semaphore-bounded workers (semaphore, thread-pool already in index).
- **errno convention** — Library/ABI convention rather than a design mechanism; noted as related convention under Return Status Code.
- **Essence (Carlson, PLoPD4)** — Staged construction with completeness validation before yielding the real object — folds into Builder + Smart Constructor (both in index).
- **Event bubbling / capturing** — Raw DOM platform dispatch semantics (DOM spec feature), not a design element; event delegation - the mechanism built on it - is cataloged.
- **EWMA / median smoothing filters** — established and absent, but declined under the algorithm-zoo rule - would open the DSP filter family; datastructures/numerics corpus territory (flagged by embedded3 hunter, editor concurs)
- **EWMA / moving-average smoothing** — 
- **Exception-unwinding machinery (LSDA, personality routines, EHABI table unwinding)** — Compiler runtime mechanics; the design-level choices are captured as result-type and setjmp/longjmp elements.
- **Execute-in-place (XIP)** — Platform memory-configuration choice (run code directly from flash) rather than an in-program mechanism; recorded for completeness.
- **Factory (DDD)** — Evans defers to GoF factory patterns; canonical naming and cataloging belongs to the GoF scout (dedup).
- **Fail-Safe Defaults** — Saltzer & Schroeder security design principle - a principle, not an implementable mechanism.
- **Fail-secure / fail-safe defaults** — Saltzer & Schroeder design principle, not an implementable mechanism (charter anticipated this call)
- **Fake clock / virtual time** — 
- **Fallback (Hystrix/Polly)** — 
- **Fan-Out / Fan-In (Go blog 'Pipelines and cancellation')** — Named in the Go blog but not a distinct mechanism at this altitude: fan-out folds into competing-consumers / master-slave (task farm), fan-in into aggregator/multiplexed channels - all already in the index.
- **Fast path / slow path split** — Named usage exists (kernel literature, Wikipedia 'Fast path') but it is an optimization heuristic for shaping code, closer to practice than to a discrete mechanism.
- **Flash file system (littlefs / SPIFFS)** — 
- **Flash journaling / journaling filesystem** — Dedup: write-ahead-log already carries 'journaling' in its aka; a journaling FS is WAL applied to filesystem metadata. Power-loss-resilient update in flash is otherwise covered by copy-on-write + shadow-paging + eeprom-emulation-in-flash.
- **Flow Synchronization / Observer Synchronization (Fowler eaaDev 2004)** — Screen-to-session-state synchronization variants — Observer Synchronization is Observer applied to presentation sync, Flow Synchronization is its manual counterpart; folded into cataloged observer/data-binding territory, no distinct mechanism survives.
- **Fluent C ch. 8 sub-patterns (Software-Module Directories, Global Include Directory, Self-Contained Component, API Copy)** — Already folded into the index's organizing-files-in-modular-c-programs aggregate entry (house precedent: chapter-level folding); splitting them out would fragment one mechanism cluster.
- **Fluent C ch. 9 sub-patterns (Avoid Variants, Isolated Primitives, Atomic Primitives, Abstraction Layer, Split Variant Implementation)** — Already folded into the index's escaping-ifdef-hell aggregate entry; same folding precedent.
- **Fluent C iterator patterns (Index Access, Cursor Iterator, Callback Iterator)** — C-API realizations of GoF Iterator; fold as implementation notes under Iterator rather than separate mechanisms.
- **Fluent C memory patterns (Stack First, Eternal Memory, Memory Pool, Allocation Wrapper, Pointer Check, Dedicated Ownership)** — Deliberately left to the resource-management scout to avoid duplicate ownership; Memory Pool = object pool/memory arena family. Recorded so they are not lost if that scout misses Fluent C.
- **fold / map / higher-order functions** — Charter-directed exclusion: syntax-level primitives; their design-level composition is captured by collection-pipeline.
- **Format Indicator** — A version/format field convention inside a message; below element granularity.
- **FreeRTOS heap_1-heap_5 allocator schemes** — Implementation menu of allocator variants; the underlying mechanisms are covered by memory-pool, segregated-free-lists, and boundary-tags entries.
- **Fresh Fixture / Shared Fixture and finer Meszaros entries (Custom Assertion, Test Utility Method)** — 
- **frustum culling** — 
- **Function Split (Fluent C ch. 1)** — Refactoring-level: split a function so each part handles its own responsibilities/cleanup - essentially Fowler's Extract Function applied to error handling; below the mechanism band.
- **Functor / Applicative (typeclass hierarchy)** — 
- **functor / applicative functor hierarchy** — Type-class abstraction ladder (McBride & Paterson 2008); monad is kept as the representative umbrella entry, the rest of the hierarchy is not enumerated per the one-element-per-mechanism rule.
- **Fuzzing / fuzz harness** — 
- **Garbage Collection (Noble & Weir chapter pattern)** — Same as reference counting - general resource-management territory; recorded here so the fold is not silent.
- **GC read barrier / load barrier (Brooks pointer, ZGC colored-pointer load barrier)** — Established (GC Handbook sect. 11.8 sibling of write barriers) and genuinely absent, but outside this round's charter candidate list and a dual mechanism of narrower reach; at strictness peak recorded here rather than added. Flag for the editor if VM coverage is later deepened.
- **Generator Pipeline (Python, Beazley 'Generator Tricks for Systems Programmers')** — Real and named, but the mechanism - staged lazy transformation of a data stream - folds into collection-pipeline already in the index (which lists lazy streams pipelines). Recommend adding 'generator pipeline (Beazley)' as an aka on collection-pipeline instead of a new element.
- **geometry instancing / GPU instancing** — 
- **Given When Then (Fowler bliki 2013)** — Test-description convention (BDD scenario format, kin of arrange-act-assert) — a writing style/practice, not an implementable construct.
- **Goal-Oriented Action Planning (GOAP)** — Named (Orkin, 'Three States and a Plan: The A.I. of F.E.A.R.', GDC 2006) but it is a STRIPS-family planning algorithm applied to agents - algorithm-zoo side of the line; reconsider if a game-AI axis is grown.
- **GoF State Pattern (DPESC ch5 'State Pattern')** — DPESC restates the GoF State pattern in C - canonical entry belongs to the GoF scout.
- **GPU command buffer recording** — 
- **Graphics command buffer** — Recording device commands for deferred submission is a graphics-API construct (Vulkan/D3D12) conceptually covered by Command + message-queue + double-buffer composition; no independent design-element naming source at the right altitude.
- **Halo exchange / ghost cells** — 
- **Hardware memory-consistency models (TSO, x86-TSO, ARM weak ordering)** — Properties of hardware, not designable elements; the designable counterparts (barrier placement, acquire-release) are included.
- **Harmony / ROPES process (Douglass)** — Development process/methodology, not a design element - pass 7 territory.
- **Header Files (Fluent C ch. 6)** — C practice/syntax-level (declare API in .h); the design-level residue is already covered by the index's organizing-files-in-modular-c-programs aggregate.
- **Header Interface (Fowler bliki 2006)** — Counterpart vocabulary to Role Interface (one interface mirroring a whole class); same rejection — characterization, not mechanism.
- **Honeypot / honeytoken** — Deception operations/infrastructure, not an in-process design element
- **Hot code reload** — Already in the catalog: hot-code-reload (code-structure). Charter check confirmed present.
- **Humane Interface / Minimal Interface (Fowler bliki)** — API-design stance debate (how rich an interface should be) — vocabulary, not mechanisms.
- **Identity Map vs cache distinction note** — Not an element - PoEAA distinguishes Identity Map from a general cache; general caching elements belong to other scouts.
- **IIFE (Immediately-Invoked Function Expression, JS)** — Named (Ben Alman 2010; Osmani) but syntax-level: a single expression form for creating scope. The design-level element it enables, Module Pattern (with Revealing Module as aka), is already in the index.
- **In Memory Test Database (Fowler bliki)** — Test-environment substitution technique — practice, plus covered conceptually by test-double/service-stub territory.
- **Index Access (Fluent C ch. 7)** — Near-syntax API convention (expose element access by integer index); no mechanism beyond array subscripting behind a function.
- **Initialization-on-demand holder idiom** — Java-specific micro-idiom (class-loader-based lazy init); a language-level alternative realization of what double-checked locking covers - variant-level, folded into DCL's territory.
- **Inline caching / polymorphic inline cache** — Already in the catalog: inline-caching (caching-memoization) covers monomorphic/polymorphic/megamorphic ICs. Checked because hidden-class is adjacent; judged genuinely distinct (IC caches per-site lookup results; hidden class is the layout descriptor the IC guards on), so hidden-class added as its own element.
- **input buffering (fighting-game technique)** — 
- **Instant Projection / Hypothetical Publication / Forecast Confirmation / Diagnostic Query (CHECKS)** — Publication-workflow and inspection-process patterns, above/os-outside the single-program mechanism band.
- **Intention-Revealing Interface / Side-Effect-Free Function / Assertion (DDD supple design)** — Design principles/heuristics from Evans 2003 ch.10, not named recurring mechanisms.
- **Intermediate representation (IR)** — A broad compiler-internal concept spanning many concrete forms; the concrete recurring elements (AST, bytecode) are cataloged instead.
- **Interpreter and Visitor (GoF patterns)** — Canonically GoF-named; deferred to the oo-patterns scout to keep GoF names in one place (Visitor is the standard AST-traversal realization).
- **Interpreter dispatch loop (switch dispatch)** — Covered between bytecode-virtual-machine (bytecode interpreter) and threaded-code (dispatch variants); a separate 'dispatch loop' entry would duplicate both.
- **Interrupt latency budgeting** — Practice/analysis activity (budget allocation and measurement), not an implementable in-program mechanism; fails the altitude test downward into process territory.
- **Interrupt priority grouping / nesting discipline** — 
- **Invalid Message Channel** — At this altitude the same mechanism as Dead Letter Channel (side channel for bad messages); EIP distinguishes only the cause (malformed vs undeliverable/expired).
- **Inversion of Control** — Principle, not a mechanism; realized by concrete elements (dependency injection, hook methods, callbacks).
- **Inversion of control (principle)** — Design principle, not a discrete mechanism; its concrete realizations (dependency injection, callback, active-object framework) are cataloged.
- **Invertible Bloom Lookup Table (IBLT)** — Named and citable (Goodrich & Mitzenmacher, Allerton 2011) but judged research-zoo tier: a set-reconciliation specialist below the count-min-sketch/HyperLogLog prominence line the index already draws; belongs in the datastructures sibling corpus as a Bloom-family variant, cross-referenced rather than cataloged.
- **Join algorithms (nested-loop, sort-merge, hash join, grace/hybrid hash)** — Excluded per charter: algorithm zoo at algorithmics granularity - datastructures corpus territory; the execution-model elements (Volcano, vectorized) carry the design-level content.
- **Kahan Summation (compensated summation)** — Named and canonical (Kahan 1965) but sits in the numerical-algorithmics zoo the mission excludes from this catalog; cross-reference the datastructures/algorithms sibling corpus rather than enumerate summation-algorithm variants (Kahan, Neumaier, pairwise) here.
- **Key derivation function (HKDF) and key rotation** — KDF-for-passwords folded into salted-password-hashing aka; general KDF and rotation are crypto-engineering practice below/beside the band already flagged as borderline
- **Key matrix scanning** — 
- **Language subsetting (MISRA, EC++, freestanding C++, safety profiles)** — Practice/standardization activity constraining language use, not design mechanisms.
- **Latch** — DB-internals name for a short-term lightweight mutex on in-memory structures (Hellerstein et al. 2007 distinguishes locks vs latches); folds into the generic mutex/lock element owned by the concurrency scout - recorded so the aka is not lost.
- **Least privilege, complete mediation, economy of mechanism, open design (Saltzer & Schroeder set)** — Principles; their mechanisms (privilege bracketing, reference monitor) are cataloged instead
- **Legacy Seam / Seam (Feathers WELC 2004; Fowler bliki LegacySeam)** — Analytical concept naming *where* behavior can be substituted without editing source (object/link/preprocessing seams) — a testability property of code plus legacy-work practice, not a recurring implementable mechanism; strictness round excludes.
- **Linker scripts / memory-layout control (SECTIONS, MEMORY, KEEP, VMA/LMA)** — Ops/toolchain machinery per charter; the design-level residue (memory overlay) was included separately.
- **Linker-script section placement (attribute/section control, KEEP, memory regions)** — Toolchain mechanism below the design band (corpus ld, zephyrlinker); recurring but tool-configuration rather than program design.
- **Literate programming (Knuth)** — Documentation/programming practice, not an in-program mechanism.
- **littlefs metadata pairs / CTZ skip-list** — Named only in the littlefs DESIGN.md; single-project construct names that fail the 'recurring across codebases' gate. The recurring mechanisms littlefs composes (copy-on-write, wear leveling, checksummed commit) are already in the index.
- **LMAX Disruptor** — A specific product/library, not a named recurring element; its mechanisms fold into ring buffer (data-flow scout territory) and single-writer principle.
- **Local DTO (Fowler bliki 2004)** — Usage discussion (DTOs within a process) of the already-cataloged data-transfer-object; no separate mechanism.
- **Lock file / pidfile** — 
- **Lock-free audio callback discipline** — Bencina's 'Real-time audio programming 101: time waits for nothing' is citable, but it is a real-time coding rule set (never lock/allocate/IO in the callback), i.e. practice; its mechanisms (spsc-lock-free-ring-buffer, pool-allocation) are already in the index.
- **Lock-free queue (Michael-Scott), concurrent hash map, RCU-protected structures** — Real designer-reachable structures but concurrency-mechanism-first; left to the execution-concurrency scout to avoid duplicate ids (flagged as a cross-scout dependency, not dropped).
- **LR / LALR / LL table-driven, Earley, GLR parsing algorithms** — Algorithm-variant zoo (datastructures corpus territory); recursive descent and Pratt carry the design-building-block roles per the no-variant-enumeration rule.
- **LTO / ThinLTO** — Toolchain optimization technology, not a program design element.
- **Main-loop watchdog kick placement (pet from main loop, never from a timer ISR)** — 
- **make illegal states unrepresentable** — Design principle (Yaron Minsky), not a mechanism; realized via tagged-union, newtype, phantom-type, typestate, smart-constructor entries.
- **Manager (Sommerlad, PLoPD3) and Domain Object Manager (PLoPD5)** — Same mechanism as object-manager already in index (lifecycle + lookup of a class's instances); recommend adding 'Manager (Sommerlad)' and 'Domain Object Manager' as aka on object-manager.
- **Match Progress Work with New Work / Finish Work in Progress / Share the Load / Work Shed at Periphery (Meszaros, PLoPD1)** — Capacity-tuning policy guidance; established siblings already in index (load-shedding, fresh-work-before-stale, leaky-bucket-counter). Work Shed at Periphery folds into load-shedding aka.
- **Materialized view / incremental view maintenance** — 
- **Maximal munch (longest-match lexing rule)** — A disambiguation rule inside the lexer mechanism, not a standalone element; noted here so the name is preserved.
- **Memory barrier / fence** — Hardware/ISA-level ordering instruction below the design band (raw instruction granularity, like a keyword); its design-level surface appears inside safe publication, DCL, and CAS entries.
- **Message catalog (i18n)** — POSIX catgets / GNU gettext name it, but the in-program mechanism — keyed lookup of externalized strings — folds into the existing resource-files entry (aka 'resource bundle'); i18n-specific forces (locale fallback chains, plural rules) did not justify a second mechanism entry. Judged per charter and rejected as duplicate-risk.
- **Message Channel, Message Router, Message Endpoint** — EIP root generalizations; the concrete specializations (point-to-point, pub-sub, content-based router, consumers) are cataloged instead of the abstract parents.
- **Message Sequence** — EIP construction pattern for multi-part transmission via sequence numbering; below charter granularity here, but sequence numbering itself may merit an element under a serialization-framing scout.
- **Message Translator, Envelope Wrapper, Content Enricher, Content Filter, Normalizer** — EIP message-transformation family; integration-side restatements of adapter/mapping/serialization concerns owned by other scouts' axes.
- **Messaging Gateway, Messaging Mapper, Service Activator, Transactional Client** — Messaging-endpoint API-shape patterns (gateway/mapper/adapter family); construction-api territory better owned by the Fowler PoEAA / API-shape scout.
- **Metric instrument types (counter/gauge/histogram)** — Prometheus/OpenTelemetry name the trio, but it is an API taxonomy for telemetry libraries, not a mechanism; the underlying mechanisms (counters, sketches like t-digest) are in the index.
- **Middleware chain (Express/Rack style)** — 
- **Middleware chain (Express/Redux style)** — Recurring JS usage but the mechanism folds into interceptor and chain-of-responsibility, both already in the index.
- **Minimize Human Intervention / Maximize Human Participation** — Hanmer patterns; human-factors and operations principles.
- **Module-Level Singleton (Python)** — The 'modules are singletons' idiom is a language-provided realization of Singleton (already in index), not a distinct mechanism; at most an aka/implementation note on singleton.
- **Monkey Patching (Python/JS/Ruby)** — Named and recurring, but a runtime-modification practice/hazard rather than a design building block; closest mechanism (open classes / dynamic dispatch tables) is language machinery.
- **Moving-average / exponential-smoothing (EWMA) / median smoothing filters** — 
- **MPU-based task/memory isolation (FreeRTOS-MPU style)** — Named mostly in RTOS/vendor docs; the partitioning concept parked at architecture (ARINC 653 entry), the per-task MPU configuration judged platform setup rather than a design element - honest borderline exclusion.
- **Mutation testing** — 
- **N-ary Storage Model (NSM) as a separate entry** — The row-oriented counterpart of DSM/PAX is the unnamed default, not a reached-for mechanism; it is adequately carried as context in the pax-page-layout and column-oriented-storage entries.
- **Nuclear reaction pattern** — Listed on Wikipedia's concurrency-pattern page but with no established catalog/textbook naming source found; fails the establishedness gate rather than the altitude test.
- **nullptr idiom / Address Of / Checked Delete / Multi-statement Macro / Named Loop (wikibooks)** — Micro-idioms or workarounds superseded by language features; below design altitude.
- **Object Recovery (Silva et al., PLoPD3)** — Object-level state save/restore — folds into Memento + Checkpointing + Rollback (all in index).
- **Objects for States (POSA4)** — Alias of GoF State pattern; folded - GoF State is the canonical entry (GoF scout territory).
- **Observer / Proxy / Adapter / Mediator / State patterns as they appear in Douglass** — GoF names are canonical - cataloged once by the GoF scout; only the embedded-specific specializations (Hardware Proxy, Hardware Adapter) are entered here.
- **occlusion culling** — 
- **Off-side rule (significant indentation)** — A grammar convention (Landin 1966); its implementation is an INDENT/DEDENT tokenization variant inside the lexer element.
- **On-stack replacement (OSR) as a separate element** — Judged per charter: OSR and deoptimization share one frame-replacement mechanism (reconstructing equivalent activation frames at a mapped point, run in either tier direction); at strictness peak folded into deoptimization as aka rather than split into two entries.
- **Output encoding / contextual escaping (OWASP)** — Folds into existing index entry escape-sequence (its aka already covers entity encoding); HTML sanitization is kept separate because it filters parsed structure rather than encoding
- **Packages (Noble & Weir)** — Deployment/dynamic-loading granularity - realized by OS loader machinery, below/aside the design band as a program-internal mechanism.
- **Page-replacement policies (LRU, clock, second-chance, WSClock)** — OS instance of cache eviction - fold as a note under the cache-eviction-policy element (caching scout owns); policy variants are the algorithmics zoo.
- **Pagination (offset/keyset)** — 
- **Pane accumulation modes (Discarding / Accumulating / Accumulating & Retracting)** — 
- **Parallel Change / Expand-Contract (Fowler bliki 2014)** — Interface-migration sequencing technique (expand, migrate, contract) — practice altitude, same family as Branch by Abstraction.
- **parse, don't validate** — Principle/slogan (Alexis King, 2019), not a mechanism; its mechanism side is the smart-constructor entry.
- **Parser generator (yacc, ANTLR)** — A build-time tool/practice rather than an in-program mechanism; fails the altitude test sideways into tooling.
- **pattern matching** — Charter-directed exclusion: language syntax level (destructuring/case analysis feature), below the altitude band; it is the consumption syntax for tagged unions, noted there.
- **Per-frame / frame arena allocator (single-frame allocator)** — Folded as aka of memory arena per charter (arena owned by the resource-management sweep); naming source for the game-specific form: 'Frame-Based Memory Allocation' - Steven Ranck, Game Programming Gems 1 (2000). Central merge should attach these aliases and source to the arena element.
- **Pipes / FIFOs (OS IPC facility)** — Kernel-provided facility, not an implementable element; the in-process analog (inter-thread channel / blocking queue) is the communication scout's element.
- **Pluggable Object (Beck SBPP)** — Parameterize behavior by plugging in an object instead of subclassing — folds into Strategy (in index); Pluggable Selector kept as the genuinely distinct reflective variant.
- **Pointer tagging / NaN-boxing / small-integer tagging** — Already in the catalog: pointer-tagging (data-representation) with NaN-boxing and Smi as aka. No new element needed.
- **Polyfill / shim** — 
- **Polyfill / Shim (JS)** — Named (Remy Sharp 2010; MDN) but a compatibility-artifact practice; the underlying mechanisms are feature detection plus adapter/facade, already covered.
- **POSA5: On Patterns and Pattern Languages (2007)** — Meta-theory of patterns and pattern languages (pattern form, sequences, languages); catalogs no implementable elements - noted per charter, nothing extracted.
- **POSIX signal handler** — 
- **Predicate locking** — Named in Eswaran et al. 1976 but essentially a (rarely implemented) generalization within the 2PL family; folded as a note under two-phase-locking rather than a separate element.
- **Prefix sum (parallel scan)** — 
- **Preforking / process pool** — 
- **Presentation Model / Passive View / Supervising Controller (verification, not a new decision)** — VERIFIED already parked: ui-reactive scout parked the whole MV* family (MVC, MVP with Passive View and Supervising Controller as sub-variants, MVVM, Presentation Model, Elm/MVU, MVI) as app-structure altitude for Phase 3.
- **printf-style format strings** — Library/language feature near the raw-syntax floor; the general structured-output mechanism is covered by the pretty-printer entry.
- **Progress-guarantee taxonomy (wait-free / lock-free / obstruction-free)** — Classification vocabulary (Herlihy), not an implementable mechanism; belongs in prose/notes, not as an element.
- **Protocol version negotiation** — 
- **Proxy objects (Carnie register series)** — Names GoF Proxy in a register-access context - left to the GoF catalog sweep to avoid a duplicate seed entry.
- **Published Interface (Fowler bliki)** — Public-vs-published distinction is API-evolution/management vocabulary (who may depend on it), not an implementable mechanism — practice/altitude fail sideways.
- **Pulse-width modulation (PWM)** — 
- **pure function / referential transparency** — A semantic property, not a mechanism; the structural idiom that operationalizes it (functional core, imperative shell) is cataloged.
- **QP / QEP framework (Samek)** — A concrete framework/product realizing the patterns, not an element; belongs in the works corpus (samekcourse/samekbook already present).
- **Quarantine (Azure)** — Supply-chain/ops practice, not an implementable mechanism.
- **Race-to-sleep / DVFS / peripheral clock gating** — 
- **Race-to-sleep / low-power mode management** — 
- **Rate-monotonic / earliest-deadline-first scheduling policies** — Named scheduling algorithms with analysis theory (Liu & Layland, corpus liulayland) - algorithm/analysis level; flagged for the scheduling scout's policy call.
- **Rate-monotonic analysis (Liu & Layland 1973)** — Schedulability analysis technique, not an implementable mechanism; RMS priority assignment is noted as aka under Static Priority Scheduling.
- **React Hooks** — Framework-proprietary API surface, not a cross-codebase mechanism name.
- **Readiness- vs completion-based I/O multiplexing (select/poll/epoll/kqueue vs IOCP/io_uring)** — The syscall families are facilities; the design-level elements are Reactor and Proactor, owned by POSA2 (corpus id posa2) via the concurrency scout.
- **Realistic Threshold / Existing Metrics** — Hanmer detection patterns that are parameter-tuning guidance rather than mechanisms.
- **Recipient List, Dynamic Router, Composed Message Processor** — EIP routing variants beyond the charter's in-process subset; mechanisms are compositions/variants of Content-Based Router + Splitter/Aggregator already cataloged.
- **Record Set (PoEAA)** — 
- **Recursion schemes (catamorphism etc.)** — 
- **recursion schemes (catamorphism/anamorphism etc.)** — Meijer, Fokkinga & Paterson 1991 ('bananas' paper); generalized folds - theory/syntax altitude, and enumeration would open an algorithmics zoo owned elsewhere.
- **Redux reducer / unidirectional data flow (Flux)** — 
- **Reference Counting (Noble & Weir chapter pattern)** — Genuine element, deliberately ceded to the resource-management scout (general, not embedded-specific) to avoid cross-scout duplication; N&W is a naming source if needed.
- **Remembered set as a separate element** — The data structure a write barrier maintains; GC Handbook ch. 11 treats barrier and remembered set as one recording mechanism. Folded into gc-write-barrier aka as a role.
- **Reset cause handling (act on power-on vs watchdog vs brown-out reset at boot)** — 
- **Return Value (Fluent C ch. 4)** — Raw language mechanism (the C return statement); no design content beyond syntax.
- **Revealing Constructor Pattern (JS, Domenic Denicola 2014)** — Citable but essentially single-source naming with thin recurrence beyond describing the Promise constructor; omitted per anti-invention discipline.
- **Ring-buffer / flight-recorder logging** — Real and widespread (kernel printk buffer, JDK Flight Recorder, embedded trace logs) but it is a composition of ring-buffer + logging with no established mechanism name independent of products; ring-buffer already in index.
- **Role Interface (Fowler bliki 2006)** — Interface-granularity vocabulary (interface shaped per collaborator role, contrasted with Header Interface); ISP-adjacent characterization of interface design, not a distinct implementable mechanism beyond 'an interface'. Catalog already carries the mechanism-bearing interface constructs (separated-interface, explicit-interface, extension-interface, marker-interface).
- **Root Cause Analysis / Revise Procedure / Reproducible Error / Let Sleeping Dogs Lie** — Hanmer fault-treatment patterns; engineering/ops process guidance.
- **Rounding-mode control** — 
- **Routine Audits / Routine Exercises / Routine Maintenance** — Hanmer detection patterns of the operational-practice kind (scheduled ops activities), unlike Correcting Audits which is an in-program mechanism.
- **RTOS priority-based preemptive scheduling** — 
- **Rust micro-idioms (mem::take/replace, temporary mutability, on-stack dynamic dispatch, format! concatenation)** — Named in rust-unofficial/patterns but statement-level usage tips below design altitude.
- **Sacrificial Architecture (Fowler bliki 2014)** — Lifecycle strategy (plan to throw one away) — strategy essay, neither a design element nor a catalogable architecture element.
- **Safe bool idiom** — Established C++ idiom (wikibooks) but obsoleted by C++11 explicit operator bool; historical language-workaround, recorded not cataloged.
- **Seedwork (Fowler bliki, term from Michael Feathers)** — Copy-then-diverge code-reuse approach for small starter kits — development practice vocabulary, weak establishedness as an element; excluded.
- **select-based channel multiplexing (Go)** — Language syntax (select statement) over csp-channel, which is already in the index.
- **Self Initializing Fake (Fowler bliki 2009)** — Record-and-replay fake that primes itself from the real service on first run — judged a variant of the cataloged test-double rather than a separate mechanism; recommend merge team add 'self-initializing fake / record-and-replay fake' to test-double's aka.
- **Semantic Data Types (mission anchor phrase)** — No published source names this exact phrase as a design element (searched, including White's Making Embedded Systems). The mechanism is covered by newtype + value-object + quantity + Whole Value (already an aka of newtype, verified live in Cunningham's CHECKS at c2.com/ppr/checks.html), now extended by the new units-of-measure-types entry. Anchor considered covered.
- **Semihosting** — Debug transport mechanism between target and host - ops territory per charter.
- **Semihosting / RTT debug channels** — Debug/tooling infrastructure (corpus semihosting, segger), not a design mechanism of the shipped program.
- **Separated Presentation (Fowler eaaDev)** — Separation principle (presentation vs domain), not a mechanism; its concrete realizations (data-binding, presentation-model family) are cataloged or parked.
- **session types** — Type-system research feature for communication protocols (Honda 1993); language-level, not an in-program mechanism; the practical in-program cousin (typestate) is cataloged.
- **Shared memory segments (System V / POSIX shm)** — Facility-not-element; in-process analog is plain shared address-space state plus synchronization primitives (concurrency scout).
- **Shunting-yard algorithm** — A specific stack-based infix-to-postfix algorithm; the design-level role (operator-precedence expression parsing) is carried by the Pratt parser entry.
- **Skeleton screens** — UX/perceived-performance presentation practice (Wroblewski) rather than an implementation mechanism.
- **Small Interfaces (Noble & Weir)** — API-design guidance ('let clients control data transfer') rather than an implementable mechanism; flagged for the construction-api scout to reconsider.
- **Smalltalk Scaffolding Patterns (Doble & Auer, PLoPD4)** — Development-process/temporary-code practices, pass-7 territory.
- **Smart UI** — Named by Evans 2003 as an anti-pattern / whole-app structure alternative, not a design element.
- **Software Update / Small Patches** — Hanmer fault-treatment patterns; deployment/maintenance process, not in-program mechanisms.
- **Sorting/search algorithm families (quicksort, timsort, binary search)** — Algorithms, not structures; charter covers structures a designer reaches for by role.
- **sprite batching** — 
- **SSA form / register allocation** — 
- **Stack overflow detection hook (vApplicationStackOverflowHook / FreeRTOS methods 1 & 2)** — Dedup: the detection techniques are already covered by stack-painting-watermarking (fill-pattern check, method 2) and guard-page/MPU redzone; FreeRTOS method 1 (SP bounds check at context switch) is an implementation detail, and the hook itself is a plain callback, not a distinct mechanism.
- **Stack-usage analysis (-fstack-usage) and binary-size profiling (Bloaty, puncover, pw_bloat)** — Ops tooling/measurement, not mechanisms.
- **Staged rollout / fallback lifeboat firmware update** — 
- **Standard driver interface (open/close/read/write/ioctl)** — 
- **Steal/no-steal, force/no-force buffer policies** — A 2x2 policy taxonomy for buffer-pool/recovery interaction (Haerder & Reuter 1983), noted under buffer-pool and write-ahead-log rather than as standalone elements.
- **Steering behaviors** — Reynolds, 'Steering Behaviors for Autonomous Characters', GDC 1999 - a family of movement algorithms (seek/flee/flock); algorithmics zoo, cross-reference territory rather than a design element.
- **Strangler Fig / Front Controller / Page Controller / Transaction Script / Table Module / Service Layer / Remote Facade (verification, not a new decision)** — VERIFIED already parked by wiki-longtail, posa, and poeaa-ddd scouts in merged_design.json.
- **Stream/connection multiplexing** — 
- **struct hack / flexible array member** — Raw language feature (C99) rather than a named design mechanism.
- **Struct-of-arrays vs array-of-structs (SoA/AoS), small-vector/small-string optimization** — Data-representation/layout idioms; data-representation scout territory.
- **Structured logging** — Established terminology, but it is an output-format convention/practice, not a distinct implementable mechanism; no catalog-grade naming source at mechanism level found. Judged hard per charter and rejected.
- **Subcommand dispatch (CLI)** — 
- **Superinstructions / instruction dispatch optimizations** — Ertl & Gregg name them, but they are VM optimization variants under threaded-code, which the index already carries.
- **sync.Once / call-once initialization (Go)** — Library facility; mechanism covered by construct-on-first-use and double-checked-locking already in the index.
- **System V / POSIX message queues, UNIX domain sockets** — OS facilities; the design-level element is the in-process message queue / mailbox (communication scout).
- **TCP congestion-control algorithm family (slow start, AIMD, CUBIC, BBR)** — Stack-internal algorithm zoo, not a reusable in-process building block; AIMD as a concept may merit a note under rate limiting if another scout claims it.
- **Test Harness** — Nygard stability pattern, but it is testing infrastructure/practice, not a runtime design mechanism.
- **Texture atlas / sprite sheet** — Near-miss cut at the cap: NVIDIA SDK whitepaper 'Improve Batching Using Texture Atlases' names it; naming-source grade weaker than the accepted 15; candidate for follow-up.
- **Threaded code / computed-goto dispatch (Bell, CACM 1973)** — Already in the catalog: threaded-code (execution-concurrency) with aka direct threading, indirect threading, computed-goto dispatch. Charter candidate rejected as duplicate.
- **Tick hook (vApplicationTickHook)** — Plain periodic callback from the tick ISR; unlike the idle hook it carries no distinct execution-context semantics beyond 'callback registered in ISR context' — covered by callback + interrupt-service-routine.
- **Timer wheel** — Scheduling-and-time element (Varghese & Lauck 1987); scheduling scout territory - verify coverage at merge.
- **Toolkit / framework distinction** — GoF chapter 1 concept about reuse granularity - a classification of software artifacts, not an implementable mechanism; fails the altitude test as neither design element nor architecture element.
- **Trapezoidal motion profile; quadrature encoder decoding** — 
- **Tri-color marking / mark-sweep / copying collection** — Covered by the existing garbage-collection element's aka set (mark-sweep, mark-compact, copying collection); no separate entry warranted.
- **Triple buffering** — Variant of double buffering; belongs as an aka/variant under the existing double-buffer entry, not a new element.
- **Trust boundary** — Threat-modeling concept, not a mechanism
- **type class** — Language type-system feature (Wadler & Blott 1989, 'How to make ad-hoc polymorphism less ad hoc'), not an implementable in-program mechanism; the patterns built on it (tagless final, newtype instances) are cataloged.
- **Ubiquitous Language** — DDD practice/communication discipline, not an implementable mechanism - process/practice territory (pass 7).
- **Unicode normalization** — 
- **Unix signal handler / async-signal-safety** — OS API plus a safety rule set, not a design element; the design-element response to it (self-pipe-trick) is already in the index.
- **UNIX signals (as a facility)** — Kernel-delivered asynchronous notification facility; the design-level handling idiom is captured as the self-pipe trick element.
- **UTF-8 and character encodings** — Standardized data formats rather than reusable design mechanisms; the byte-order mark is noted as an aka under magic number.
- **Utility AI / utility system** — Named (Mark, 'Behavioral Mathematics for Game AI'; Graham, 'An Introduction to Utility Theory', Game AI Pro) but it is a scoring/selection technique with weak mechanism boundaries rather than a recurring implementable construct.
- **Value Holder (PoEAA lazy-load variant)** — 
- **Variable timestep / delta-time update** — Recorded as a variation inside the Game Loop chapter rather than a separate element; the established named mechanism in this space is Fixed Timestep, cataloged separately.
- **Version field in protocol/firmware ('Version!')** — 
- **Visible Implication (CHECKS)** — Display of derived quantities for user review; the mechanism half (computed/derived values) is covered by reactive-signals' computed/derivations aka; the rest is UI guidance.
- **volatile qualifier discipline** — Raw language-syntax level; folded as a note into memory-mapped register access (see eideregehr for the miscompilation literature).
- **Volatile-correctness for device access (Eide & Regehr)** — Raw language-feature usage caveat; the mechanism level is captured by memory-mapped-register-access.
- **Wavelet tree, van Emde Boas tree, Judy array, finger tree, succinct/compressed structures (FM-index et al.)** — Research-zoo granularity; not designer-role vocabulary outside specialist niches - sibling corpus territory.
- **Whole Value (CHECKS)** — Already folded into the index: newtype carries 'whole value (related CHECKS pattern)' as aka, and quantity covers the unit-bearing case. No separate entry proposed; merge team may promote if it prefers CHECKS naming.
- **Whole Value (Cunningham CHECKS)** — Verified live (c2.com/ppr/checks.html) but already folded into the index as an aka of newtype; kept folded per the dedup rule. Integrator may prefer promoting it to a standalone element since it is the closest published name for the 'semantic data types' anchor; if promoted, remove it from newtype's aka.
- **Window Driver (Fowler eaaDev)** — Folded as aka into the new page-object element — Fowler's PageObject bliki states it is the same pattern under his earlier name.
- **Workqueue (Zephyr k_work / Linux workqueue)** — Dedup: same mechanism as deferred-interrupt-processing, whose aka list already contains 'work queue deferral' (plus tasklet, softirq, DPC). No new element.
- **Write amplification / read amplification / space amplification** — Named evaluation metrics for storage designs (RUM conjecture), not mechanisms.
- **Write-ahead log / append-only log** — Persistence-durability mechanism, not a container role; assumed owned by the persistence scout (verify coverage at merge).
- **xUnit test-organization patterns (Four-Phase Test, Fresh Fixture, Testcase Class per Class, etc.)** — Meszaros patterns about test structure/process, not code-level constructs; only the code-construct subset (Test Double, Humble Object) taken.
- **Z-buffer / depth buffer** — Catmull 1974 names it; judged a domain rendering algorithm co-designed with hardware rather than a software design element; honest borderline, rejected downward-domain.
- **Z-order curve / Morton code, geohash** — Spatial key-encoding techniques rather than container structures; borderline algorithmic - recorded for a possible follow-up sweep.
- **Zephyr memory slab (k_mem_slab)** — Dedup: despite the name it is a fixed-size block pool, i.e. already covered by pool-allocation (aka fixed-block allocator, partition allocator). It is NOT the Bonwick object-caching slab-allocator; folding it there would be wrong. Recommend adding 'memory slab (Zephyr)' as an aka of pool-allocation.
- **ZOMBIES heuristic (Grenning)** — Unit-test-ordering process heuristic - pass-7 process territory.
