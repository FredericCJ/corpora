# SWE Corpus — Architecture-Element Catalog v1.0 (`architecture-elements`, realm: architecture)

**Object.** Named, recurring, architecture-level constructs — styles, patterns, tactics, connector types, deployment structures, reference architectures, and description constructs: the realm ABOVE the 708-element design catalog (`design_elements_catalog_v1_0.md`), built to the same ground rules (establishedness gate, canonical naming & dedup, borderline honesty, stable kebab ids). Compiled 2026-07-11 from the canonical vocabularies the corpus already carries (Bass–Clements–Kazman tactic trees, POSA1, Shaw–Garlan, Taylor–Medvidović–Dashofy styles + connector taxonomy, ISO/IEC/IEEE 42010, Kopetz/AUTOSAR/ARINC 653 embedded reference structures) plus demand-driven growth from the 203 candidates Phase 1 parked upward — every one of the 203 is adjudicated (admitted, folded, or dropped) in the intake log below.

**Same-name, two realms.** Some names live in both realms (heartbeat, event sourcing, bulkhead …). They are cataloged in each realm where sources establish them — ids disambiguated by kind suffix — and Phase 3b bridges the pairs; the realms are never collapsed.

**Census.** **370 elements** · kinds: style 64 · pattern 131 · tactic 109 · connector 14 · deployment 26 · reference-architecture 10 · description 16 · confidence: 355 established / 15 spot-checked / 0 needs-check · 44 borderline · tactic coverage by quality attribute: availability 49, deployability 12, energy-efficiency 13, integrability 10, manageability 1, modifiability 7, performance 16, reliability 2, resource-efficiency 1, safety 18, scalability 7, security 28, testability 8, usability 7.

**Per-kind counts.**

| kind | n |
|---|---|
| style | 64 |
| pattern | 131 |
| tactic | 109 |
| connector | 14 |
| deployment | 26 |
| reference-architecture | 10 |
| description | 16 |
| **total** | **370** |

---

## Architectural styles — `style` (64)

### actor-based-architecture — Actor-Based Architecture
- aka: actor system, active-object framework, run-to-completion kernel (QP-style), actor topology
- kind: style
- what: Organizes the whole system as actors that own their state and interact only via asynchronous messages processed run-to-completion from per-actor mailboxes.
- problem: Shared-state concurrency does not scale in complexity; message-owned state removes locks and makes distribution and supervision natural.
- named-in: corpus:hewitt1973 — A Universal Modular ACTOR Formalism for Artificial Intelligence - Hewitt, Bishop & Steiger (1973)
- tags: concurrency, distributed, embedded

### adaptive-object-model — Adaptive Object Model
- aka: Dynamic Object Model, Active Object-Model, user-defined domain model architecture
- kind: style
- what: Represents classes, attributes and rules as runtime data (metadata) interpreted by a generic engine, so the domain model is changed by users, not by code.
- problem: Businesses whose types and rules change constantly cannot afford recompile-redeploy for every change.
- named-in: corpus:plopd5 — Pattern Languages of Program Design 5 - Riehle, Tilman & Johnson (2006)
- tags: enterprise, metadata

### batch-sequential — Batch Sequential
- aka: batch sequential processing
- kind: style
- what: A degenerate data-flow organization in which each processing step runs to completion on the entire data set before passing the complete result to the next step.
- problem: How to structure data processing when steps need the whole input (or when interactive incremental flow is unnecessary); loses the incremental delivery and concurrency of pipes-and-filters but simplifies each stage.
- named-in: corpus:garlanshaw93 — An Introduction to Software Architecture - Garlan & Shaw (1993)
- tags: enterprise

### blackboard — Blackboard
- aka: blackboard system, blackboard model (HEARSAY-II lineage), blackboard model, knowledge-source architecture
- kind: style
- what: Independent specialized knowledge sources cooperate by reading and writing partial solutions on a shared data structure (the blackboard) under a control component's opportunistic scheduling.
- problem: For problems with no deterministic solution strategy (signal interpretation, recognition), no fixed control flow can be designed up front; opportunistic, data-driven cooperation of partial experts replaces a hardwired pipeline.
- named-in: corpus:posa1 — Pattern-Oriented Software Architecture Vol. 1: A System of Patterns - Buschmann et al (1996)
- tags: ai, knowledge-based, data

### blockchain — Blockchain
- aka: distributed ledger, Merkle-chained ledger with consensus
- kind: style
- what: A peer-to-peer system maintains a replicated append-only ledger of Merkle-chained blocks agreed by a consensus mechanism.
- problem: Mutually distrusting parties need a tamper-evident shared history without a trusted central authority.
- named-in: corpus:bitcoin — Bitcoin: A Peer-to-Peer Electronic Cash System - Nakamoto (2008)
- tags: distributed, security

### broker — Broker
- aka: object request broker, ORB architecture, distributed object middleware, Broker Pattern (RTDP), ORB topology, Broker Revisited (POSA4)
- kind: style
- what: Structures a distributed system around an intermediary component that coordinates remote service invocations - locating servers, marshalling requests/replies, and reporting errors - so clients and servers stay decoupled from location and transport.
- problem: Components of a distributed system should interact by service request without hardwiring host, transport, or wire format into every participant; the broker centralizes registration, lookup, and forwarding (CORBA/DCOM lineage). Distinct from EIP's Message Broker: this brokers request/reply remote invocations, not asynchronous message routing.
- named-in: corpus:posa1 — Pattern-Oriented Software Architecture Vol. 1: A System of Patterns - Buschmann et al (1996)
- tags: distributed, middleware

### c2 — C2
- aka: component-and-message architecture (GUI)
- kind: style
- what: A layered, message-based style in which components communicate only through explicit connectors via asynchronous notifications (downward) and requests (upward), under a strict substrate-independence rule: a component may know services above it but nothing below.
- problem: How to build flexible, distributable GUI-centric systems from reusable off-the-shelf components whose parts can be replaced or rewired at runtime; requires all interaction to be mediated, prohibiting direct component links and shared address-space assumptions.
- named-in: corpus:tmd — Software Architecture: Foundations, Theory, and Practice - Taylor, Medvidovic & Dashofy (2010)
- tags: ui, distributed

### channel-architecture — Channel Architecture
- aka: channels of transformation, Channel Architecture (RTDP), data transformation channels
- kind: style
- what: Organizing the system as one or more end-to-end channels, each a sequential chain of data transformations from sensing to actuation, so that redundancy and safety measures can be applied per-channel.
- problem: Safety and reliability engineering needs a unit to replicate, diversify, or protect; structuring the system as identifiable channels creates that unit and localizes data flow for analysis.
- named-in: corpus:douglassrtcorpus — Real-Time Design Patterns - Douglass (2002)
- tags: embedded, safety-critical, real-time, safety, dataflow

### clean-architecture — Clean Architecture
- aka: Onion Architecture (Palermo, 2008; folded), the Dependency Rule
- kind: style
- what: Concentric layers (entities, use cases, interface adapters, frameworks) with all source dependencies pointing inward toward policy.
- problem: Keep business rules independent of frameworks, UI, and databases so they outlive delivery mechanisms; generalizes hexagonal/onion into one dependency discipline.
- named-in: corpus:martincleanarch — Clean Architecture - Martin (2017)
- tags: app-structure, enterprise

### client-server — Client-Server
- aka: client/server model, two-tier client-server, requester-provider topology
- kind: style
- what: Server components provide services at known locations while client components initiate requests for them, typically via remote procedure call or request/response protocols, with the server unaware of client identities in advance.
- problem: How to share centralized resources and services among many distributed consumers; centralizes state and administration at the cost of a scalability and availability bottleneck at the server.
- named-in: corpus:garlanshaw93 — An Introduction to Software Architecture - Garlan & Shaw (1993)
- tags: distributed, enterprise, general

### code-on-demand — Code-on-Demand
- aka: COD, downloaded code style
- kind: style
- what: A mobile-code style in which a client that has the data and processing resources requests executable code (know-how) from a remote server and runs it locally, as with scripts delivered to a browser.
- problem: How to extend a deployed client's functionality without redeployment, moving computation to where the data and interaction are; introduces trust, versioning, and sandboxing obligations on the receiving site.
- named-in: corpus:tmd — Software Architecture: Foundations, Theory, and Practice - Taylor, Medvidovic & Dashofy (2010)
- tags: web, distributed, mobile-code

### component-based-architecture — Component-Based Architecture
- aka: ROOM pattern, component-and-connector organization, CBSE structuring
- kind: style
- what: Structures the whole system as replaceable components with explicit provided/required interfaces (ROOM: capsules with ports and protocols).
- problem: Monolithic structure prevents unit substitution, reuse and independent development of system parts.
- named-in: corpus:room — Real-Time Object-Oriented Modeling - Selic, Gullekson & Ward (1994)
- tags: embedded, general

### dataflow-architecture — Dataflow Architecture
- aka: dataflow systems (Shaw-Garlan), dataflow programming (system paradigm)
- kind: style
- what: Organizes the whole system around the availability and movement of data through transforming nodes rather than control flow.
- problem: Transformation-dominated systems are clearer and more parallelizable when structure follows the data path.
- named-in: corpus:shawgarlan96 — Software Architecture: Perspectives on an Emerging Discipline - Shaw & Garlan (1996)
- tags: dataflow, general

### distributed-commit-log — Distributed Commit Log
- aka: replicated log, Kafka-style log, log-centric architecture, replicated log backbone
- kind: style
- what: A partitioned, replicated append-only log serves as the system's ordering and integration backbone; producers append, consumers replay at their own pace.
- problem: Give many decoupled systems one durable, ordered, replayable record of what happened, unifying messaging, replication, and stream processing.
- named-in: corpus:krepslog — The Log: What every software engineer should know about real-time data's unifying abstraction - Kreps (LinkedIn Engineering, 2013)
- tags: distributed, data, streaming, messaging

### distributed-objects — Distributed Objects
- aka: CORBA-style architecture, broker-mediated objects
- kind: style
- what: System functionality is partitioned into objects whose methods can be invoked across process and machine boundaries through proxies and an object request broker, preserving OO interfaces over the network.
- problem: How to extend object-oriented organization to distributed systems while hiding location and transport; masks but does not remove the latency, partial-failure, and concurrency differences between local and remote calls.
- named-in: corpus:tmd — Software Architecture: Foundations, Theory, and Practice - Taylor, Medvidovic & Dashofy (2010)
- tags: distributed, enterprise

### distributed-processes — Distributed Processes
- aka: communicating processes, communicating sequential processes organization, independent components (family)
- kind: style
- what: The system is a set of independent processes, typically on multiple processors, interacting by message passing under some topological organization (ring, star, arbitrary graph).
- problem: How to structure systems whose components are inherently concurrent and physically distributed; the architecture must state both the topology and the communication protocol because no shared state exists.
- named-in: corpus:garlanshaw93 — An Introduction to Software Architecture - Garlan & Shaw (1993)
- tags: distributed, concurrency

### event-based-implicit-invocation — Event-Based Implicit Invocation
- aka: implicit invocation, event-based integration, selective broadcast, event system, event-based style (TMD), Event-Driven Architecture, EDA, broker topology / mediator topology (variants), event-based style, event-driven system
- kind: style
- what: Components announce (broadcast) events instead of invoking procedures directly; the system implicitly invokes every procedure registered as interested in that event.
- problem: How to integrate components without hard-wiring caller-callee identities; announcers gain strong decoupling but surrender control over which handlers run, in what order, and whether they run at all.
- named-in: corpus:garlanshaw93 — An Introduction to Software Architecture - Garlan & Shaw (1993)
- tags: distributed, enterprise, messaging, embedded, reactive

### event-sourcing-architecture-style — Event Sourcing (architecture style)
- aka: event-sourced system, event store as system of record
- kind: style
- what: System-level persistence strategy where the event log is the source of truth for whole services and downstream projections/read models are derived from it.
- problem: Full audit/history, temporal queries, and rebuildable projections across a system; couples consumers to event schemas over time.
- named-in: corpus:mfeaadev — Event Sourcing - Fowler (eaaDev, 2005)
- tags: enterprise, data, same-name-two-realms, borderline — Same-name-two-realms: the design realm's event-sourcing entry is the in-component persist-as-events mechanism; this entry is the system-level style built on it.

### event-triggered-architecture — Event-Triggered Architecture
- aka: ET architecture, event-triggered system
- kind: style
- what: System-level organization in which communication and task activation are initiated by the occurrence of significant events (interrupts, message arrivals) rather than by a global clock; Kopetz names it as the counterpoint to time-triggered control.
- problem: Sporadic, low-rate, or unpredictable stimuli waste bandwidth and CPU under static time-triggered schedules; event triggering gives flexibility and responsiveness at the cost of harder worst-case analysis and possible event showers.
- named-in: corpus:kopetz — Real-Time Systems: Design Principles for Distributed Embedded Applications - Kopetz & Steiner (2022)
- tags: embedded, real-time, distributed

### file-transfer — File Transfer
- aka: file-based integration, batch file exchange, File Transfer (integration style), flat-file integration
- kind: style
- what: Applications integrate by one producing files of shared data and others consuming them, with an agreed format and transfer/processing cadence.
- problem: Independently built applications must share information with maximum decoupling and no shared infrastructure; files buy universality and loose coupling at the cost of staleness, format-agreement effort, and no transactional coordination.
- named-in: corpus:hohpe — Enterprise Integration Patterns - Hohpe, Woolf (2003)
- tags: enterprise, integration, batch

### function-queue-scheduling-architecture — Function-Queue-Scheduling Architecture
- aka: function pointer queue architecture, run-to-completion dispatcher architecture
- kind: style
- what: A system structure in which interrupts enqueue pointers to task functions and the main loop dequeues and runs them to completion, allowing priority ordering of the queue without a preemptive kernel.
- problem: Round-robin loops cannot prioritize urgent work and full RTOS preemption may be overkill; queueing work as functions gives priority control and bounded response with cooperative simplicity.
- named-in: corpus:dsimonprimer — An Embedded Software Primer - Simon (1999)
- tags: embedded, real-time

### hexagonal-architecture — Hexagonal Architecture
- aka: Ports and Adapters
- kind: style
- what: Application core exposes technology-neutral ports; adapters translate between each external actor (UI, DB, tests, other systems) and the ports.
- problem: Let the application be driven equally by users, programs, or tests, and keep infrastructure swappable; kills business-logic leakage into UI and DB code.
- named-in: corpus:hexagonalarch — Hexagonal Architecture - Cockburn (alistair.cockburn.us, 2005)
- tags: app-structure, enterprise

### interpreter-architectural-style — Interpreter (Architectural Style)
- aka: table-driven interpreter, virtual machine style, interpreter/virtual machine
- kind: style
- what: The system is organized as a virtual machine: an interpretation engine, the pseudo-program it executes, and the engine's and program's state, closing the gap between the execution platform and the desired semantics.
- problem: How to execute programs for a machine that does not exist in hardware, or to make behavior data-driven and portable; the extra level of interpretation trades performance for flexibility.
- named-in: corpus:garlanshaw93 — An Introduction to Software Architecture - Garlan & Shaw (1993)
- tags: borderline — Same NAME as the design-realm GoF 'interpreter' pattern - the architectural style structures a whole system as a virtual machine; both kept, id suffixed.

### kappa-architecture — Kappa Architecture
- aka: —
- kind: style
- what: Everything is a stream: a single stream-processing pipeline over a replayable log serves both real-time and reprocessing needs, eliminating the separate batch layer.
- problem: Avoid maintaining dual batch/speed code paths of the lambda architecture; reprocessing is replaying the log through the same pipeline.
- named-in: corpus:kappakreps — Questioning the Lambda Architecture - Kreps (O'Reilly Radar, 2014)
- tags: distributed, data, streaming

### lambda-architecture — Lambda Architecture
- aka: —
- kind: style
- what: Data system split into a batch layer (immutable master dataset, recomputed views), a speed layer (incremental real-time views), and a serving layer merging both.
- problem: Combine the accuracy/robustness of batch recomputation with low-latency access to recent data.
- named-in: corpus:bigdatamarz — Big Data: Principles and best practices of scalable realtime data systems - Marz & Warren (2015)
- tags: distributed, data, streaming

### layers — Layers
- aka: layered architecture, strict/relaxed layering, abstraction layering, Layered Pattern (RTDP), Layered System, hierarchical layers, layered firmware architecture (driver/HAL/middleware/application), n-tier layering, strict vs relaxed layering
- kind: style
- what: Structures a whole system as a hierarchy of abstraction levels in which each layer offers services to the layer above and uses only the layer(s) below.
- problem: A large system mixes concerns at very different abstraction levels (hardware access, mechanism, policy, UI); one-way layered dependencies buy exchangeability, portability, and independent evolution at the cost of indirection and pass-through overhead.
- named-in: corpus:posa1 — Pattern-Oriented Software Architecture Vol. 1: A System of Patterns - Buschmann, Meunier, Rohnert, Sommerlad, Stal (1996)
- tags: general, os, embedded, networking, enterprise

### lmax-architecture — LMAX Architecture
- aka: business logic processor with input/output disruptors
- kind: style
- what: A single-threaded in-memory business logic processor is fed and drained by ring-buffer (Disruptor) pipelines, with event sourcing for durability.
- problem: Extreme-throughput low-latency processing is defeated by locks and database round-trips; single-writer in-memory design removes both.
- named-in: corpus:lmaxfowler — The LMAX Architecture - Martin Fowler (2011)
- tags: finance, performance, concurrency

### main-program-and-subroutines — Main Program and Subroutines
- aka: main program/subroutine organization, call-and-return organization
- kind: style
- what: A single main program drives the system by calling a hierarchy of subroutines, with control returning up the call tree after each call.
- problem: How to organize a computation-dominant system when the decomposition follows functional refinement; correctness of a component depends only on the subroutines it calls, but data flow through shared parameters/globals resists change.
- named-in: corpus:garlanshaw93 — An Introduction to Software Architecture - Garlan & Shaw (1993)
- tags: —

### mapreduce — MapReduce
- aka: map-reduce, map-reduce framework
- kind: style
- what: Batch computation structured as a parallel map phase over partitioned input, a shuffle, and a reduce phase, scheduled across a cluster by a framework.
- problem: Run large-scale data processing on commodity clusters while the framework handles partitioning, scheduling, and fault recovery.
- named-in: corpus:mapreduceosdi — MapReduce: Simplified Data Processing on Large Clusters - Dean & Ghemawat (OSDI 2004)
- tags: distributed, data, batch

### message-bus — Message Bus
- aka: bus topology (messaging), service bus, enterprise service bus (ESB, productized form), enterprise bus, bus integration topology
- kind: style
- what: A shared messaging backbone - common channels, a common data model, and a common command set - that all applications plug into to interoperate, joining or leaving without affecting the others.
- problem: An enterprise of separate applications must work as one system while letting individual systems be added, removed, or replaced; a common bus buys plug-in interoperability at the cost of enterprise-wide agreement on the shared contract.
- named-in: corpus:hohpe — Enterprise Integration Patterns - Hohpe, Woolf (2003)
- tags: enterprise, distributed, messaging

### messaging — Messaging
- aka: message-based integration, asynchronous messaging (integration style), Messaging (integration style)
- kind: style
- what: Applications integrate by exchanging discrete asynchronous messages over channels provided by a messaging infrastructure, decoupling senders from receivers in time and availability.
- problem: Integration must be frequent, immediate-enough, and reliable between systems that cannot assume each other's availability; asynchronous channels buy decoupling and reliability at the cost of eventual consistency and harder end-to-end reasoning.
- named-in: corpus:hohpe — Enterprise Integration Patterns - Hohpe, Woolf (2003)
- tags: enterprise, integration, distributed, messaging

### micro-frontends — Micro Frontends
- aka: —
- kind: style
- what: Frontend decomposed into independently built and deployed UI fragments owned end-to-end by the teams owning the corresponding backend services.
- problem: Extend microservice-style team autonomy through the UI layer instead of funneling all teams through one frontend monolith.
- named-in: corpus:microfrontends — Micro Frontends - Jackson (martinfowler.com, 2019)
- tags: web, enterprise

### microkernel — Microkernel
- aka: plug-in architecture, minimal core plus extensions, Microkernel Architecture Pattern (RTDP), OS microkernel (L4/seL4 lineage), minimal kernel plus servers, plug-in architecture (application form)
- kind: style
- what: Separates a minimal functional core (fundamental services, communication, extension management) from extended functionality delivered as internal/external servers or plug-ins loaded onto the core.
- problem: A platform or product family must adapt to changing requirements and support many variants; keeping the core minimal and pushing features into replaceable extensions buys portability and product-line flexibility at the cost of extra indirection through the core.
- named-in: corpus:posa1 — Pattern-Oriented Software Architecture Vol. 1: A System of Patterns - Buschmann et al (1996)
- tags: os, embedded, extensibility, product-line

### microservices — Microservices
- aka: fine-grained SOA
- kind: style
- what: Suite of small, independently deployable services, each owning its data, communicating over lightweight network mechanisms, organized around business capabilities.
- problem: Independent deployability, team autonomy, and heterogeneous technology per service; trades operational and distribution complexity for decoupling.
- named-in: corpus:microservicesfowler — Microservices - Lewis & Fowler (martinfowler.com, 2014)
- tags: distributed, enterprise, cloud

### mobile-agent — Mobile Agent
- aka: migrating computation
- kind: style
- what: A mobile-code style in which an entire computational unit - code, execution state, and data - migrates itself from site to site, resuming execution at each destination.
- problem: How to sustain a long-lived computation across intermittently connected or resource-shifting hosts; state capture, migration transparency, and security of both agent and host dominate the design.
- named-in: corpus:tmd — Software Architecture: Foundations, Theory, and Practice - Taylor, Medvidovic & Dashofy (2010)
- tags: distributed, mobile-code

### modular-monolith — Modular Monolith
- aka: —
- kind: style
- what: Single deployable unit whose interior is decomposed into strictly encapsulated modules with enforced boundaries.
- problem: Keep monolith deployment simplicity while getting service-like boundary discipline; a stepping stone to (or alternative to) microservices.
- named-in: corpus:monolith2micro — Monolith to Microservices - Newman (2019)
- tags: enterprise

### monolithic-architecture — Monolithic Architecture
- aka: monolith, single-process deployment
- kind: style
- what: The whole application is built and deployed as a single deployable unit.
- problem: Simplicity of development, testing, and deployment for one team/one unit; the named baseline against which service decomposition trades off.
- named-in: corpus:microservicesio — microservices.io: Pattern - Monolithic Architecture - Richardson (living)
- tags: enterprise, deployment

### n-tier-client-server — N-Tier Client-Server
- aka: three-tier architecture, multi-tier architecture, tiered architecture, N-Tier Architecture, multitier architecture, physical tiers
- kind: style
- what: Client-server generalized to a chain of tiers (e.g. presentation, business logic, data management), each acting as server to the tier before it and client of the tier after it, deployable on separate machines.
- problem: How to scale, secure, and independently evolve the presentation, application, and data concerns of an enterprise system; each added tier buys isolation and scaling at the price of latency and deployment complexity.
- named-in: corpus:tmd — Software Architecture: Foundations, Theory, and Practice - Taylor, Medvidovic & Dashofy (2010)
- tags: enterprise, distributed

### object-oriented-organization — Object-Oriented Organization
- aka: data abstraction and object-oriented organization, abstract data type style, ADT style
- kind: style
- what: The system is organized as a collection of abstract-data-type instances (objects) that hide their representations and interact by invoking each other's operations.
- problem: How to localize the effects of representation change; encapsulation lets internals evolve freely, at the cost that every caller must know the identity of the object it invokes.
- named-in: corpus:garlanshaw93 — An Introduction to Software Architecture - Garlan & Shaw (1993)
- tags: —

### peer-to-peer — Peer-to-Peer
- aka: P2P, symmetric client-server
- kind: style
- what: Networked components (peers) act as both clients and servers of one another, discovering and exchanging services directly without a distinguished central server.
- problem: How to achieve scalability, resilience, and resource pooling when no node can be trusted or provisioned as a permanent center; pays for decentralization with discovery, consistency, and trust problems.
- named-in: corpus:tmd — Software Architecture: Foundations, Theory, and Practice - Taylor, Medvidovic & Dashofy (2010)
- tags: distributed, networking

### pipes-and-filters — Pipes and Filters
- aka: pipeline architecture, pipes-and-filters (EIP integration style), dataflow pipeline (system-scale), pipe-and-filter, pipeline (linear specialization), data-flow network, filter pipeline, batch sequential (degenerate relative)
- kind: style
- what: Organizes a processing system as a chain of independent filter components connected by pipes that carry a data stream from source to sink.
- problem: A whole processing task must be decomposable, recombination-friendly, and incrementally streamable; independent filters buy reuse, reordering, and parallel deployment at the cost of shared-format agreement and per-stage transfer overhead. EIP restates the same macro structure at inter-application integration scale (steps joined by message channels).
- named-in: corpus:posa1 — Pattern-Oriented Software Architecture Vol. 1: A System of Patterns - Buschmann et al (1996)
- tags: dataflow, batch, integration, unix, general

### process-control-feedback-control-loop — Process Control (Feedback Control Loop)
- aka: closed-loop control architecture, feedback control loop style, control loop
- kind: style
- what: The system is organized around a control loop: a controller reads process variables from sensors, compares them to set points, and adjusts manipulated variables to keep a physical or continuing process on target.
- problem: How to maintain specified properties of an ongoing process in the face of external disturbances that cannot be predicted, using open- vs closed-loop and feedback vs feedforward variants; the architecture must make the loop, not the call graph, the primary structure.
- named-in: corpus:shawgarlan96 — Software Architecture: Perspectives on an Emerging Discipline - Shaw & Garlan (1996)
- tags: embedded, control

### protocol-layering — Protocol Layering
- aka: encapsulation stack, OSI layering, protocol stack, headers-around-payload nesting
- kind: style
- what: Structures communication software as a stack of protocol layers, each providing services to the layer above and encapsulating its PDU inside the layer below.
- problem: Communication concerns (framing, routing, reliability, sessions) must evolve independently; strict layering with encapsulation isolates them.
- named-in: corpus:tanenbaumcn — Computer Networks, 6th ed. - Tanenbaum, Feamster & Wetherall (2021)
- tags: networking, embedded

### publish-subscribe-architectural-style — Publish-Subscribe (Architectural Style)
- aka: pub-sub style, topic-based messaging architecture, event notification (system-scale), Publish-Subscribe (system topology), pub-sub (distributed), topic-based messaging topology, pub-sub messaging topology, Publisher-Subscriber (Azure, POSA4)
- kind: style
- what: Publishers emit messages classified by topic or content to an intermediary event service, which delivers them to all components that have subscribed, so producers and consumers never address each other.
- problem: How to decouple many-to-many information flow in space, time, and synchronization across a distributed system; delivery ordering, reliability, and subscription management move into the connector.
- named-in: corpus:tmd — Software Architecture: Foundations, Theory, and Practice - Taylor, Medvidovic & Dashofy (2010)
- tags: distributed, enterprise, messaging, same-name-two-realms, borderline — Same NAME as the design realm's in-process publish-subscribe (observer / event-aggregator / publish-subscribe-channel); this is the system-scale style with a distributed event service - both kept, id suffixed.

### remote-evaluation — Remote Evaluation
- aka: REV, remote execution of shipped code
- kind: style
- what: A mobile-code style in which a component that has the know-how sends code to a remote site that has the resources and data, where it executes and returns results.
- problem: How to bring computation to remote data or special resources instead of shipping bulk data to the computation; the receiving site must safely execute foreign code and account for its resource use.
- named-in: corpus:tmd — Software Architecture: Foundations, Theory, and Practice - Taylor, Medvidovic & Dashofy (2010)
- tags: distributed, mobile-code

### remote-procedure-invocation — Remote Procedure Invocation
- aka: RPI, RPC-based integration, remote invocation integration, Remote Procedure Invocation (integration style), RPC integration, RMI integration, remote invocation style
- kind: style
- what: Applications integrate by exposing procedures/services that other applications invoke synchronously over the network to exchange data and trigger behavior.
- problem: Integration needs behavior sharing and encapsulation, not just data sharing; synchronous invocation buys encapsulated interfaces at the cost of tight temporal coupling and distributed-failure fragility. The design realm's remote-procedure-call element is the invocation mechanism; this entry is the system-integration style built on it.
- named-in: corpus:hohpe — Enterprise Integration Patterns - Hohpe, Woolf (2003)
- tags: enterprise, integration, distributed

### repository-shared-data-style — Repository (Shared Data) Style
- aka: shared data style, data-centered architecture, shared repository, repository style (Shaw-Garlan), central data store coordination
- kind: style
- what: A central data structure represents the system state while a collection of independent components operate on it, coordinating only through the shared store.
- problem: How to let many computations cooperate on a large, evolving body of data without direct coupling; the choice of who triggers whom (transactions vs. store state) splits the style into database and blackboard variants.
- named-in: corpus:garlanshaw93 — An Introduction to Software Architecture - Garlan & Shaw (1993)
- tags: data, integration, borderline — Same NAME as the design-realm 'repository' (Fowler data-access pattern) - different mechanism, both kept per the same-name-two-realms rule; id suffixed.

### rest-representational-state-transfer — REST (Representational State Transfer)
- aka: representational state transfer, RESTful architecture
- kind: style
- what: A hybrid network-based style constraining client-server interaction to be stateless, cacheable, layered, and mediated by a uniform interface over resources identified by URIs and manipulated via exchanged representations, optionally extended by code-on-demand.
- problem: How to make an Internet-scale hypermedia system evolvable, scalable, and visible to intermediaries; the constraints trade per-interaction efficiency (self-descriptive messages, statelessness) for anarchic scalability and independent deployment of components.
- named-in: corpus:fieldingrest — Architectural Styles and the Design of Network-based Software Architectures - Fielding (2000)
- tags: web, distributed

### rtos-based-architecture — RTOS-Based Architecture
- aka: real-time operating system architecture, task-based architecture, multitasking RTOS structure
- kind: style
- what: A whole-system structure in which the application is decomposed into prioritized, preemptively scheduled RTOS tasks communicating through kernel objects (queues, semaphores, events), with response times set by priority rather than loop position.
- problem: When response requirements differ by orders of magnitude across activities, cooperative loops cannot bound latency for the urgent ones; a preemptive kernel decouples each activity's worst-case response from the rest of the system.
- named-in: corpus:dsimonprimer — An Embedded Software Primer - Simon (1999)
- tags: embedded, real-time, os

### rule-based-system — Rule-Based System
- aka: production system, rule-based interpreter
- kind: style
- what: An interpreter specialization in which a rule engine (inference/interpretation engine) selects and fires condition-action rules from a knowledge base against working memory.
- problem: How to keep volatile domain logic out of code so domain experts can evolve behavior as rules; control flow becomes emergent from rule selection rather than explicit.
- named-in: corpus:garlanshaw93 — An Introduction to Software Architecture - Garlan & Shaw (1993)
- tags: ai, enterprise

### seda-staged-event-driven-architecture — SEDA (Staged Event-Driven Architecture)
- aka: staged event-driven architecture, SEDA
- kind: style
- what: Service structured as a network of event-driven stages connected by explicit queues, each stage with its own thread pool and admission control.
- problem: Well-conditioned behavior under massive load: per-stage queues give backpressure points and prevent overcommit that thread-per-request designs suffer.
- named-in: corpus:sedasosp — SEDA: An Architecture for Well-Conditioned, Scalable Internet Services - Welsh, Culler & Brewer (SOSP 2001)
- tags: distributed, server, qa:performance, web, concurrency

### sense-compute-control — Sense-Compute-Control
- aka: SCC, sense-plan-act (robotics variant)
- kind: style
- what: An embedded-systems organization structured as a repeating loop of sensor reading, computation over the sensed values plus internal state, and actuator commands controlling the environment.
- problem: How to structure reactive embedded software whose primary job is continuous interaction with physical hardware; keeps timing and I/O concerns explicit at the top level rather than buried in a call hierarchy.
- named-in: corpus:tmd — Software Architecture: Foundations, Theory, and Practice - Taylor, Medvidovic & Dashofy (2010)
- tags: embedded, control, robotics

### service-based-architecture — Service-Based Architecture
- aka: —
- kind: style
- what: Small number of coarse-grained, separately deployed domain services sharing a single database, typically fronted by one UI.
- problem: Pragmatic middle ground between monolith and microservices: partial independent deployability without distributed-data complexity.
- named-in: corpus:richardsford — Fundamentals of Software Architecture - Richards & Ford (2020)
- tags: enterprise, distributed

### service-oriented-architecture — Service-Oriented Architecture
- aka: SOA, orchestration-driven service-oriented architecture, service orientation, ara::com service orientation (AUTOSAR Adaptive)
- kind: style
- what: Enterprise organized as coarse-grained reusable business/enterprise services coordinated through a mediating integration layer (often an ESB/orchestrator).
- problem: Enterprise-wide reuse of business functions across applications; centralizes integration and workflow at the cost of coupling to the mediator.
- named-in: corpus:richardsford — Fundamentals of Software Architecture - Richards & Ford (2020)
- tags: enterprise, distributed, automotive

### shared-database — Shared Database
- aka: shared data integration, integration database, Shared Database (integration style)
- kind: style
- what: Multiple applications integrate by reading and writing the same database schema, making one store the single point of data agreement.
- problem: Applications need consistent, immediately visible shared data; a common schema buys freshness and one source of truth at the cost of schema-coupling every application together and contention on the shared store. Distinct from Blackboard: an integration data store, not opportunistic problem-solving control.
- named-in: corpus:hohpe — Enterprise Integration Patterns - Hohpe, Woolf (2003)
- tags: enterprise, integration, data, database

### shared-nothing-architecture — Shared-Nothing Architecture
- aka: SN parallel architecture
- kind: style
- what: Nodes own disjoint partitions of data and memory and coordinate only by messages; no shared disk or shared memory.
- problem: Horizontal scalability without contention on shared resources; each node scales independently, at the price of cross-partition coordination.
- named-in: corpus:sharednothing — The Case for Shared Nothing - Stonebraker (1986)
- tags: distributed, data, qa:scalability, database

### space-based-architecture — Space-Based Architecture
- aka: tuple-space architecture, cloud architecture pattern (Richards' earlier name)
- kind: style
- what: Processing units with replicated in-memory data grids, synchronized asynchronously to persistent storage, so the database is out of the request path.
- problem: Extreme/variable concurrency where the database is the bottleneck; achieves elastic scale by removing the central data store from the hot path.
- named-in: corpus:richardsford — Fundamentals of Software Architecture - Richards & Ford (2020)
- tags: distributed, cloud, performance

### state-transition-system-architectural-organization — State Transition System (Architectural Organization)
- aka: state-transition organization, reactive system organization
- kind: style
- what: A whole reactive system is organized as a set of states plus named transitions that move the system between them, making the state machine the top-level structure rather than an internal mechanism.
- problem: How to give reactive/real-time systems an analyzable top-level structure whose behavior can be enumerated and verified; differs from an in-component FSM by governing system organization, not one module's logic.
- named-in: corpus:garlanshaw93 — An Introduction to Software Architecture - Garlan & Shaw (1993)
- tags: embedded, borderline — Names the same idea as the design-realm finite state machine at a different altitude; kept per same-name-two-realms rule as the system-level organization, prime Phase 3b bridge target for the design-realm FSM cluster.

### streaming-dataflow-architecture — Streaming Dataflow Architecture
- aka: stream processing topology, streaming pipeline (Beam/Flink model), unbounded dataflow processing
- kind: style
- what: Structures data processing as a long-running dataflow graph over unbounded streams with windowing, watermarks and triggers.
- problem: Unbounded, out-of-order data cannot be handled by batch topologies; the streaming model trades off correctness, latency and cost explicitly.
- named-in: corpus:akidaudataflow — The Dataflow Model - Akidau et al. (2015)
- tags: distributed, data, dataflow

### subsumption-architecture — Subsumption Architecture
- aka: behavior-based layered control
- kind: style
- what: Layers of behavior-producing modules run concurrently, with higher layers subsuming (suppressing/overriding) the outputs of lower ones instead of a central planner.
- problem: Robot control needs robust real-time reaction without a monolithic sense-plan-act pipeline; layered competence levels degrade gracefully and are incrementally buildable.
- named-in: corpus:subsumptionbrooks — A Robust Layered Control System for a Mobile Robot - Brooks (IEEE J. Robotics and Automation, 1986)
- tags: robotics, embedded

### superloop-architecture — Superloop Architecture
- aka: super loop (system architecture), round-robin architecture, foreground/background system, bare-metal main-loop architecture
- kind: style
- what: A whole-system structure with no operating system: one endless main loop polls and services every task in turn, optionally with interrupts as the foreground layer feeding flags/buffers to the background loop.
- problem: Small systems cannot afford an RTOS's footprint and complexity; a single statically ordered loop gives minimal overhead and full determinism of structure, at the cost of coarse timing control and poor scalability.
- named-in: corpus:pont — Patterns for Time-Triggered Embedded Systems - Pont (2001)
- tags: embedded, real-time, borderline — Same-name-two-realms: the design realm's super-loop is the loop mechanism itself; sources (Pont SUPER LOOP, Simon's Round-Robin in his 'Survey of Software Architectures' chapter) also treat it as the system-architecture choice against RTOS-based structure - that architecture sense is this entry.

### time-triggered-architecture — Time-Triggered Architecture
- aka: TTA, time-triggered system architecture, TT architecture, TTP-based architecture
- kind: style
- what: System-level organization in which all communication and computation are driven by the progression of a fault-tolerant global time base, with statically planned activation instants known a priori at all nodes.
- problem: Distributed hard real-time systems need temporal predictability, composability, and fault isolation; event-driven activation makes worst-case behavior and certification arguments hard, while a global static schedule makes temporal behavior verifiable by construction.
- named-in: corpus:kopetzbauer — The Time-Triggered Architecture - Kopetz & Bauer (2003)
- tags: embedded, real-time, distributed, safety-critical, safety

### virtual-machine-architectural-style — Virtual Machine (architectural style)
- aka: interpreter style, abstract machine, Virtual Machine Pattern (RTDP)
- kind: style
- what: Builds the system atop an abstract machine whose instruction set is interpreted, decoupling applications from the physical platform.
- problem: Portability and dynamic behavior require executing programs against a stable simulated machine rather than the real one.
- named-in: corpus:shawgarlan96 — Software Architecture: Perspectives on an Emerging Discipline - Shaw & Garlan (1996)
- tags: portability, languages, borderline — Design realm carries bytecode-virtual-machine (the in-program engine); this is the system-organization style.

### zero-trust-architecture — Zero Trust Architecture
- aka: ZTA, perimeterless security model, BeyondCorp (Google realization)
- kind: style
- what: A security architecture in which no implicit trust is granted by network location; every access to a resource is individually authenticated and authorized per session via policy decision/enforcement points.
- problem: Perimeter-based models grant broad trust once inside the network, so a single breach yields lateral movement; moving enforcement to each resource access removes the trusted interior.
- named-in: corpus:nistzerotrust — Zero Trust Architecture - Rose, Borchert, Mitchell, Connelly (NIST SP 800-207, 2020)
- tags: security, enterprise, distributed, qa:security


## Architecture patterns — `pattern` (131)

### anti-corruption-layer — Anti-Corruption Layer
- aka: ACL, Anticorruption Layer, ACL (DDD), isolating translation layer
- kind: pattern
- what: An isolating translation layer between two bounded contexts (typically new model and legacy/external system) that converts between the two models.
- problem: Integrate with a system whose model you must not absorb; keeps the foreign model from leaking into and corrupting your own.
- named-in: corpus:evansddd — Domain-Driven Design - Evans (2003)
- tags: ddd, enterprise, integration, migration

### api-composition — API Composition
- aka: composite service, aggregator service
- kind: pattern
- what: A composer queries multiple services and joins their results in memory to answer a query that spans service-owned databases.
- problem: Queries crossing database-per-service boundaries need an answer without shared storage; simple but limited by in-memory join cost.
- named-in: corpus:microservicesio — microservices.io: Pattern - API Composition - Richardson (living)
- tags: distributed, enterprise, data

### api-gateway — API Gateway
- aka: gateway aggregation (folded), gateway routing (folded), gateway offloading (folded), edge server, edge gateway, single API entry point
- kind: pattern
- what: Single entry point that routes, composes, and adapts client requests to backend services, and absorbs cross-cutting edge concerns (auth, TLS, rate limits).
- problem: Clients should not know service decomposition or make chatty cross-service calls; edge concerns should not be re-implemented per service.
- named-in: corpus:microservicesio — microservices.io: Pattern - API Gateway - Richardson (living)
- tags: distributed, web, enterprise, microservices

### application-controller — Application Controller
- aka: screen/action flow controller
- kind: pattern
- what: A centralized component owns the application's screen navigation and action flow, deciding which domain logic and view follow each input.
- problem: Wizard-like or state-dependent navigation duplicated across input controllers becomes inconsistent.
- named-in: corpus:poeaa — Patterns of Enterprise Application Architecture - Fowler (2002)
- tags: web, ui

### application-switching — Application Switching
- aka: one-program-at-a-time structure
- kind: pattern
- what: Splits the system into independent executables of which only one runs at a time, each fitting the memory budget alone.
- problem: Total functionality exceeds memory; sequential exclusive programs trade concurrency for footprint.
- named-in: corpus:noblesmallmem — Small Memory Software - Noble & Weir (2000)
- tags: embedded, memory

### asynchronous-request-reply — Asynchronous Request-Reply
- aka: async request-reply with status endpoint, 202-accepted polling
- kind: pattern
- what: A client-facing request is accepted immediately with a status/result endpoint while backend processing completes asynchronously.
- problem: Long-running backend work cannot hold client connections open; the reply channel is decoupled from the request.
- named-in: corpus:azurepatterns — Cloud Design Patterns - Microsoft Azure Architecture Center
- tags: web, cloud, messaging

### authoritative-server — Authoritative Server
- aka: server-authoritative simulation, client-server netcode with prediction
- kind: pattern
- what: One server owns the true game/simulation state; clients send inputs and locally predict, then reconcile against authoritative snapshots.
- problem: Trusting clients invites cheating and divergence, but pure server authority feels laggy - prediction plus reconciliation resolves both.
- named-in: corpus:bernier01 — Latency Compensating Methods in Client/Server In-game Protocol Design and Optimization - Bernier (2001)
- tags: games, networking

### authorization-security-pattern — Authorization (security pattern)
- aka: access control policy structure, subject-object rights model
- kind: pattern
- what: A system-level structure defining which subjects may perform which actions on which protected resources, enforced at guarded access points.
- problem: Ad hoc permission checks scattered through a system are inconsistent and unauditable; the rights structure must be explicit.
- named-in: corpus:schumacher — Security Patterns: Integrating Security and Systems Engineering - Schumacher et al. (2006)
- tags: security

### backends-for-frontends — Backends for Frontends
- aka: BFF
- kind: pattern
- what: One purpose-built edge/API backend per frontend type (mobile, web, ...), each owned by the corresponding frontend team.
- problem: A single general-purpose gateway becomes a contended, lowest-common-denominator bottleneck when client types have divergent needs.
- named-in: corpus:azurepatterns — Cloud Design Patterns - Microsoft Azure Architecture Center
- tags: distributed, web, enterprise, microservices

### board-support-package — Board Support Package
- aka: BSP, board port, platform support package
- kind: pattern
- what: The packaging of all board-specific software - boot code, clock and pin configuration, device drivers, memory maps - into one named unit that adapts an OS or firmware stack to a particular hardware board.
- problem: An OS or product firmware must run on many boards; isolating everything board-specific into a replaceable package makes 'support a new board' a bounded, well-understood unit of work.
- named-in: corpus:simmonds — Mastering Embedded Linux Programming, 3rd ed. - Simmonds (2021)
- tags: embedded, os, portability

### bodyguard — Bodyguard
- aka: —
- kind: pattern
- what: Shares objects across address spaces without full RPC by attaching a guard that intercepts and validates operations on the shared object.
- problem: Distributed object sharing needs protection against misbehaving remote clients without heavyweight middleware.
- named-in: corpus:plopd3 — Pattern Languages of Program Design 3 - das Neves & Garrido (1997)
- tags: distributed, security

### bounded-context — Bounded Context
- aka: context boundary (strategic DDD)
- kind: pattern
- what: An explicit boundary within which a domain model and its ubiquitous language apply consistently; large systems are partitioned into several.
- problem: One unified enterprise model fails at scale; explicit context boundaries prevent model corruption and define natural service/ownership seams.
- named-in: corpus:evansddd — Domain-Driven Design - Evans (2003)
- tags: ddd, enterprise

### bulkhead-deployment-isolation — Bulkhead (deployment isolation)
- aka: resource isolation partitions, failure domain partitioning, Bulkhead (deployment partitioning), bulkheads (Nygard stability pattern), dedicated instance pools per consumer/function, Bulkhead (system partitioning), bulkheads (Nygard)
- kind: pattern
- what: System capacity (instances, pools, clusters) is partitioned into isolated compartments per client, workload, or function so one compartment's failure cannot exhaust the rest.
- problem: Shared capacity lets one misbehaving consumer or dependency sink the whole system; compartments cap the blast radius.
- named-in: corpus:nygard — Release It! - Nygard (2007)
- tags: distributed, cloud, qa:availability, same-name-two-realms, availability, borderline — Same-name-two-realms: the design realm's bulkhead is the in-process resource-partitioning mechanism (pools, queues); this is the deployment/topology sense.

### canonical-data-model — Canonical Data Model
- aka: common data model, canonical message format, enterprise message model
- kind: pattern
- what: An application-independent shared data model for the messages exchanged across an integration solution; every application translates only between its internal format and the canonical one.
- problem: Translating directly between every pair of application formats needs O(N^2) translators and couples applications' formats to each other; a canonical hub format reduces this to 2N translations and decouples applications' data models enterprise-wide.
- named-in: corpus:hohpe — Enterprise Integration Patterns - Hohpe, Woolf (2003)
- tags: enterprise, integration, data, borderline — Data-governance flavored, but an established EIP structural pattern with clear bridge endpoints (message-translator, normalizer).

### chained-processors — Chained Processors
- aka: processor chaining, always-on coprocessor front end
- kind: pattern
- what: Arranges multiple processors in a chain where a small always-on processor handles front-line work and wakes or feeds larger downstream processors only when needed.
- problem: Running the big processor continuously wastes power; delegating vigil duty to a tiny processor cuts system energy dramatically.
- named-in: corpus:white — Making Embedded Systems, 2nd ed. - White (2024)
- tags: embedded, power

### channel-adapter — Channel Adapter
- aka: application adapter, endpoint adapter
- kind: pattern
- what: A component that connects an application never built for messaging to the messaging system, translating between the application's API/data/database/UI surface and messages on a channel.
- problem: Integration must reach packaged, legacy, or third-party applications that cannot be modified to speak messaging; an adapter at the boundary buys their participation at the cost of an extra mediation component per application.
- named-in: corpus:hohpe — Enterprise Integration Patterns - Hohpe, Woolf (2003)
- tags: enterprise, integration, legacy

### choreography — Choreography
- aka: choreography-based saga, event choreography, decentralized coordination (vs orchestration)
- kind: pattern
- what: Multi-service workflows emerge from services publishing and reacting to each other's events, with no central coordinator.
- problem: Avoid a coordination bottleneck and keep services autonomous; trades away a single place to see and control workflow state.
- named-in: corpus:azurepatterns — Cloud Design Patterns: Choreography - Azure Architecture Center (living)
- tags: distributed, enterprise, workflow, messaging, microservices

### client-proxy-remoting — Client Proxy (remoting)
- aka: stub, remote proxy (middleware role)
- kind: pattern
- what: A local object presenting the remote component's interface inside the client process, forwarding invocations to the remoting machinery.
- problem: Clients should program against ordinary local interfaces while calls actually cross the network.
- named-in: corpus:posa4 — Pattern-Oriented Software Architecture Vol. 4 - Buschmann, Henney & Schmidt (2007)
- tags: middleware, distributed

### client-request-handler — Client Request Handler
- aka: client-side transport handler
- kind: pattern
- what: Client-side middleware component that manages network resources, sends request messages and receives replies for requestors.
- problem: Connection management, timeouts and transport details belong in one reusable client-side layer.
- named-in: corpus:posa4 — Pattern-Oriented Software Architecture Vol. 4 - Buschmann, Henney & Schmidt (2007)
- tags: middleware, networking

### client-session-state — Client Session State
- aka: state on the client
- kind: pattern
- what: Session state is held on the client (cookies, hidden fields, client storage) and sent with each request; servers stay stateless.
- problem: Server statelessness for scale-out and failover; trades bandwidth, security exposure, and size limits on session data.
- named-in: corpus:poeaa — Patterns of Enterprise Application Architecture - Fowler (2002)
- tags: enterprise, web, state-placement

### competing-consumers-system-scale — Competing Consumers (system scale)
- aka: consumer group scaling
- kind: pattern
- what: Multiple service instances concurrently consume from one shared channel, each message going to exactly one of them.
- problem: Throughput and availability of message processing must scale by adding instances without coordination between them.
- named-in: corpus:hohpe — Enterprise Integration Patterns - Hohpe & Woolf (2003)
- tags: messaging, cloud, borderline — Design realm carries competing-consumers (in-process form); this is the multi-instance system form - same-name-two-realms.

### competing-consumers-system-topology — Competing Consumers (system topology)
- aka: consumer group, worker fleet on a queue
- kind: pattern
- what: Multiple independently deployed consumer instances pull from one shared message channel, so load spreads and any instance's failure is absorbed by the rest.
- problem: Scale-out and resilience of asynchronous message processing across nodes without a dispatcher knowing the consumers.
- named-in: corpus:hohpe — Enterprise Integration Patterns - Hohpe & Woolf (2003)
- tags: distributed, messaging, qa:scalability, same-name-two-realms, borderline — Same-name-two-realms: the design realm's competing-consumers is the in-process worker-pool-on-queue mechanism; this entry is the multi-instance topology sense (per charter judgment call).

### control-bus — Control Bus
- aka: management bus, administration channel overlay, management channel overlay
- kind: pattern
- what: A separate messaging channel overlay used to send configuration, heartbeat, test, and monitoring traffic to every component of a distributed messaging solution, distinct from the application-data channels.
- problem: A distributed integration solution spanning many machines must be administered and observed as one system; a dedicated control plane buys manageability without polluting or depending on the data plane it manages.
- named-in: corpus:hohpe — Enterprise Integration Patterns - Hohpe, Woolf (2003)
- tags: enterprise, operations, messaging, qa:manageability, ops

### cqrs — CQRS
- aka: Command Query Responsibility Segregation, read/write model split
- kind: pattern
- what: The system's write model (commands) and read model (queries) are separated into distinct models, often with distinct stores kept in sync asynchronously.
- problem: Read and write workloads have divergent shapes and scale; one canonical model serves both poorly. Costs eventual consistency between models.
- named-in: corpus:youngcqrs — CQRS Documents - Young (2010); also CQRS - Fowler (bliki, 2011)
- tags: enterprise, data, distributed

### crash-only-software — Crash-Only Software
- aka: crash-only design, microreboot architecture, recovery-oriented crash-restart structure
- kind: pattern
- what: A system is structured so its components have exactly one stop method (crash) and one start method (recover), making crash-restart the universal, well-tested recovery path.
- problem: Separate clean-shutdown and crash-recovery code paths mean the rarely exercised one is broken when needed; designing for crash as the only stop makes recovery the routine path and enables microreboots of subcomponents.
- named-in: corpus:candeafox — Crash-Only Software - Candea & Fox (HotOS IX, 2003)
- tags: distributed, qa:availability, borderline — Same-name-two-realms: design realm's let-it-crash carries 'crash-only software' as an aka for the in-program supervisor/restart idiom; Candea-Fox's sense is a system-structure commitment (crash-only components, microrebootable architecture) and earns the architecture entry.

### data-bus-rtdp — Data Bus (RTDP)
- aka: shared data bus backbone, common data exchange bus
- kind: pattern
- what: A system-wide shared bus abstraction through which components publish and read common data instead of holding pairwise links.
- problem: N-squared point-to-point connections between subsystems are unmaintainable; a common backbone decouples producers from consumers.
- named-in: corpus:douglassrtcorpus — Real-Time Design Patterns - Douglass (2002)
- tags: embedded, distributed

### database-per-service — Database per Service
- aka: private database per service
- kind: pattern
- what: Each service exclusively owns its persistent data; other services access it only through the service's API.
- problem: Shared databases couple services at the schema level; private data enables independent evolution and technology choice, at the cost of cross-service queries/transactions.
- named-in: corpus:microservicesio — microservices.io: Pattern - Database per Service - Richardson (living)
- tags: distributed, enterprise, data

### database-session-state — Database Session State
- aka: persisted session state, persisted session
- kind: pattern
- what: Session state is committed to shared persistent storage between requests, keyed by session, readable by any server instance.
- problem: Session survival across server failures and free request routing; costs a database round-trip per request and cleanup of dead sessions.
- named-in: corpus:poeaa — Patterns of Enterprise Application Architecture - Fowler (2002)
- tags: enterprise, web, state-placement, database

### datatype-channel — Datatype Channel
- aka: channel-per-datatype, typed channel organization, channel-per-type
- kind: pattern
- what: The channel topology is organized so each channel carries messages of exactly one data type, letting receivers know a message's type from the channel it arrived on.
- problem: Receivers must know how to interpret incoming messages without inspecting each one; dedicating channels per type buys implicit typing and simple receivers at the cost of channel proliferation and topology-wide naming discipline.
- named-in: corpus:hohpe — Enterprise Integration Patterns - Hohpe, Woolf (2003)
- tags: enterprise, messaging, borderline — A channel-topology organizing convention rather than a mechanism or whole topology; kept with honest tag per the over-inclusion rule (parked upward by the Phase 1 EIP scout as a channel-topology design decision).

### demilitarized-zone — Demilitarized Zone
- aka: DMZ, perimeter network, screened subnet
- kind: pattern
- what: Externally reachable services are placed in a separate network segment between two firewall layers, isolating them from both the internet and the internal network.
- problem: Public-facing servers are the most exposed components; segregating them means their compromise does not grant direct access to internal systems.
- named-in: corpus:schumacher — Security Patterns: Integrating Security and Systems Engineering - Schumacher et al. (2006)
- tags: security, network, enterprise, networking, deployment

### distributed-hash-table — Distributed Hash Table
- aka: DHT, structured peer-to-peer overlay, Chord ring, Kademlia overlay
- kind: pattern
- what: Nodes form a self-organizing overlay in which consistent-hashing-based routing locates the node responsible for any key in O(log n) hops.
- problem: Decentralized lookup at scale must survive churn without any directory server.
- named-in: corpus:chord01 — Chord: A Scalable Peer-to-peer Lookup Service for Internet Applications - Stoica et al. (2001)
- tags: distributed, p2p, networking

### distributed-snapshot — Distributed Snapshot
- aka: Chandy-Lamport algorithm, checkpoint barrier, asynchronous barrier snapshotting (Flink), Chandy-Lamport snapshot
- kind: pattern
- what: Marker messages flow through a distributed system's channels so each node records a mutually consistent cut of global state without stopping the world.
- problem: Consistent global checkpoints for recovery/exactly-once processing when no node can observe the whole system at one instant.
- named-in: corpus:chandylamport85 — Distributed Snapshots: Determining Global States of Distributed Systems - Chandy & Lamport (ACM TOCS, 1985)
- tags: distributed, streaming, qa:availability

### distributed-tracing — Distributed Tracing
- aka: request tracing, trace-context propagation (mechanism aspect)
- kind: pattern
- what: Every external request gets a trace id propagated through all service hops; per-hop spans are collected centrally to reconstruct the end-to-end path.
- problem: In a request that crosses many services, latency and failure localization are impossible from per-service logs alone.
- named-in: corpus:microservicesio — microservices.io: Pattern - Distributed Tracing - Richardson (living); canonical system: Dapper - Sigelman et al. (Google, 2010)
- tags: distributed, observability, borderline — Observability infrastructure sits near operations; kept as it is a named cross-cutting system structure and the bridge endpoint for the design realm's correlation-id mechanisms.

### domain-model — Domain Model
- aka: rich object domain layer
- kind: pattern
- what: Organizes domain logic as an interconnected object model where each object carries the data and behavior of one domain concept.
- problem: Complex, rule-heavy business logic becomes unmanageable as procedures; an object model localizes each rule with its data.
- named-in: corpus:poeaa — Patterns of Enterprise Application Architecture - Fowler (2002)
- tags: enterprise, ddd

### domain-object-posa4 — Domain Object (POSA4)
- aka: self-contained domain component
- kind: pattern
- what: Encapsulates each distinct unit of application functionality as a self-contained component behind an explicit interface, as the root partitioning move of a distributed design.
- problem: Distributed systems need functional partitioning into cohesive, independently deployable units before any infrastructure decisions.
- named-in: corpus:posa4 — Pattern-Oriented Software Architecture Vol. 4 - Buschmann, Henney & Schmidt (2007)
- tags: enterprise, distributed

### dual-core-lockstep — Dual-Core Lockstep
- aka: DCLS, lockstep execution, core lockstep, triple-core lockstep (TCLS variant)
- kind: pattern
- what: Two identical processor cores execute the same instruction stream cycle-aligned (one delayed a few cycles) while comparators check their outputs every cycle, signaling a fault on any divergence.
- problem: Software-visible redundancy cannot catch transient hardware faults inside the CPU with low latency; cycle-level comparison of redundant cores detects them immediately and transparently to software, at the cost of doubled silicon.
- named-in: corpus:cortexr5trm — Cortex-R5 and Cortex-R5F Technical Reference Manual - Arm (2011)
- tags: embedded, safety-critical, hardware-adjacent, borderline — Hardware-adjacent: the structure lives in silicon, but it is a named system-architecture option that safety firmware is designed around (fault response, self-test hooks) and a bridge endpoint for error-detection design elements; distinct from the design realm's deterministic-lockstep (game networking).

### durable-subscriber — Durable Subscriber
- aka: durable subscription, persistent subscription
- kind: pattern
- what: The messaging infrastructure persists a subscriber's subscription so that messages published while the subscriber is disconnected are saved and delivered when it reconnects.
- problem: Publish-subscribe normally delivers only to currently connected subscribers; when a subscriber must miss nothing across downtime, the infrastructure - not the application - has to hold its messages, trading broker storage and cleanup obligations for completeness.
- named-in: corpus:hohpe — Enterprise Integration Patterns - Hohpe, Woolf (2003)
- tags: enterprise, messaging, qa:reliability, borderline — Endpoint-scoped QoS rather than a topology; kept architecture-level because the durability obligation lives in the messaging infrastructure, not in application code (parked upward by the Phase 1 EIP scout).

### event-carried-state-transfer — Event-Carried State Transfer
- aka: ECST
- kind: pattern
- what: Events carry the full changed state so consumers maintain local replicas and need not call back to the source system.
- problem: Decouple availability and latency of consumers from the source system; trades data duplication and eventual consistency for autonomy.
- named-in: corpus:fowlereventdriven — What do you mean by 'Event-Driven'? - Fowler (martinfowler.com, 2017)
- tags: distributed, enterprise, messaging, data

### event-collaboration — Event Collaboration
- aka: event-based component collaboration
- kind: pattern
- what: Components collaborate by broadcasting events about what happened rather than requesting each other to act, each maintaining its own state from the stream.
- problem: Request-based collaboration couples callers to responsibilities; event collaboration inverts dependencies at the cost of harder reasoning about flow.
- named-in: corpus:eaadev — Further Enterprise Application Architecture development (eaaDev) - Fowler (2005)
- tags: enterprise, messaging

### fault-containment-region — Fault Containment Region
- aka: FCR, fault containment unit, FCU, error containment region, Error Containment Barrier, containment boundary
- kind: pattern
- what: A set of components (typically a node computer) engineered so that the immediate consequences of an internal fault stay inside the region's boundary, which is defined and enforced architecturally.
- problem: Without designated containment boundaries a single fault can corrupt arbitrary parts of a distributed system, defeating redundancy; partitioning the system into independent FCRs is the precondition for any fault-tolerance argument.
- named-in: corpus:kopetz — Real-Time Systems: Design Principles for Distributed Embedded Applications - Kopetz & Steiner (2022)
- tags: embedded, real-time, safety-critical, distributed, availability, safety

### fault-observer — Fault Observer
- aka: fault report collector
- kind: pattern
- what: A system-wide component that collects fault reports from everywhere and publishes them to interested parties (operators, loggers, recovery agents).
- problem: Fault information scattered across reporters never forms a coherent picture for diagnosis and response.
- named-in: corpus:hanmer — Patterns for Fault Tolerant Software - Hanmer (2007)
- tags: availability, ops

### fault-tolerant-unit — Fault-Tolerant Unit
- aka: FTU, replicated node group
- kind: pattern
- what: A group of replica-deterministic fault containment regions that produce the same outputs so that the failure of a member is masked by the remaining replicas (duplex fail-silent or triplicated voting configurations).
- problem: Individual nodes fail; grouping FCRs into an FTU lets the architecture deliver correct service despite the failure of any single member without involving the application.
- named-in: corpus:kopetz — Real-Time Systems: Design Principles for Distributed Embedded Applications - Kopetz & Steiner (2022)
- tags: embedded, real-time, safety-critical, distributed

### federated-identity — Federated Identity
- aka: single sign-on (SSO), identity provider / relying party topology, claims-based identity, delegated authentication (SAML, OAuth/OIDC, Kerberos), identity federation, delegated authentication (SAML/OIDC realization)
- kind: pattern
- what: Authentication is delegated to a separate identity provider that the application trusts, receiving identity claims/tokens instead of managing credentials itself.
- problem: Per-application credential stores multiply attack surface and user friction; trusting an external identity authority centralizes authentication and enables single sign-on across systems.
- named-in: corpus:azurepatterns — Cloud Design Patterns - Microsoft Azure Architecture Center (living)
- tags: security, enterprise, web, qa:security, cloud

### firewall — Firewall
- aka: access barrier, packet filter firewall, stateful firewall, proxy-based firewall / application gateway, network access control point, network-layer firewall, screening router
- kind: pattern
- what: A barrier that restricts access to designated resources (typically processors, memory, and network connections); a specific realization of the security Limit Access tactic used to keep unsafe effects from propagating.
- problem: Once part of a system misbehaves, unrestricted access lets the damage spread; a barrier confines it.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:safety, bck-cat:containment-barrier, security, safety-critical, network, enterprise, networking

### five-layer-architecture-rtdp — Five-Layer Architecture (RTDP)
- aka: five-layer embedded architecture
- kind: pattern
- what: A concrete whole-system layering template for real-time embedded applications (application, UI, communication, abstract OS, abstract hardware).
- problem: Embedded systems need a standard portable stratification separating application concerns from OS and hardware dependencies.
- named-in: corpus:douglassrtcorpus — Real-Time Design Patterns - Douglass (2002)
- tags: embedded, real-time

### flux — Flux
- aka: unidirectional data flow (umbrella name, annotated), Redux (derived realization), unidirectional data flow architecture, dispatcher-store-view, Redux (descendant)
- kind: pattern
- what: App structure with a strict one-way cycle: views dispatch actions, a dispatcher routes them to stores, stores update and re-render views.
- problem: Tame cascading, hard-to-trace two-way binding updates in complex UIs by forcing all state change through one auditable direction.
- named-in: corpus:fluxoverview — Flux: In-Depth Overview - Facebook (2014)
- tags: ui, web, app-structure

### front-controller — Front Controller
- aka: single entry handler
- kind: pattern
- what: One handler receives every request for a web application, performing common processing and dispatching to per-request commands or handlers.
- problem: Duplicating security, i18n and routing logic across per-page handlers is unmaintainable; centralize the request entry point.
- named-in: corpus:poeaa — Patterns of Enterprise Application Architecture - Fowler (2002)
- tags: web, enterprise

### functional-redundancy — Functional Redundancy
- aka: design diversity, diverse redundancy, Heterogeneous Redundancy, dissimilar redundancy, design diversity (channel level), N-Version Programming (system structure), NVP, multiversion software with adjudication
- kind: pattern
- what: Provide redundant components that are diversely designed and implemented but must produce the same output for the same input.
- problem: Common-mode failures defeat identical replicas because copies sharing an implementation fail together; diversity in the redundancy addresses systematic design faults, at higher development and verification cost.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:availability, qa:safety, bck-cat:detect-faults, bck-cat:containment-redundancy, fault-tolerance, safety-critical, embedded, real-time, safety, borderline — Same-name-two-realms: design realm has n-version-programming (error-handling); Avizienis frames NVP explicitly as a fault-tolerant software architecture (versions + execution environment + adjudicator), which is this entry. Overlaps the RTDP Heterogeneous Redundancy pattern parked to the douglass/resilience scout - flag for merge-time dedup.

### gateway-aggregation — Gateway Aggregation
- aka: —
- kind: pattern
- what: A gateway fans one client request out to multiple backend services and aggregates their results into a single response.
- problem: Chatty client-to-many-services interaction over high-latency links must be collapsed at the system edge.
- named-in: corpus:azurepatterns — Cloud Design Patterns - Microsoft Azure Architecture Center
- tags: cloud, web, microservices

### gateway-offloading — Gateway Offloading
- aka: —
- kind: pattern
- what: Shared edge functionality (TLS termination, authentication, compression) is offloaded from services into the gateway.
- problem: Duplicating edge concerns in every service wastes effort and spreads security-critical code.
- named-in: corpus:azurepatterns — Cloud Design Patterns - Microsoft Azure Architecture Center
- tags: cloud, security, web

### gateway-routing — Gateway Routing
- aka: —
- kind: pattern
- what: A gateway routes requests to different backend services from a single endpoint based on request attributes.
- problem: Clients should keep one stable address while backends split, move and re-version behind it.
- named-in: corpus:azurepatterns — Cloud Design Patterns - Microsoft Azure Architecture Center
- tags: cloud, web

### guaranteed-delivery — Guaranteed Delivery
- aka: persistent messaging, store-and-forward delivery
- kind: pattern
- what: The messaging system persists every message to a local data store at each hop before acknowledging, and deletes it only after successful handoff to the next store, so messages survive crashes and outages end to end.
- problem: Asynchronous integration is only trustworthy if a sent message cannot be lost while machines and networks fail; per-hop persistence buys the delivery guarantee at the cost of throughput and storage.
- named-in: corpus:hohpe — Enterprise Integration Patterns - Hohpe, Woolf (2003)
- tags: enterprise, messaging, qa:reliability, availability, borderline — A quality-of-service guarantee of the messaging infrastructure rather than a topology; kept architecture-level because it mandates persistent-store structure at every hop of the system (parked upward by the Phase 1 EIP scout).

### half-object-plus-protocol-arch — Half-Object plus Protocol (distribution structure)
- aka: HOPP
- kind: pattern
- what: Splits one logical object into coordinated halves in two address spaces with a private protocol keeping them consistent.
- problem: An object needed with low latency on both sides of a distribution boundary can live wholly on neither.
- named-in: corpus:posa4 — Pattern-Oriented Software Architecture Vol. 4 - Buschmann, Henney & Schmidt (2007)
- tags: distributed, borderline — Design realm carries half-object-plus-protocol (object-level mechanism); this is the distribution-structure reading - same-name-two-realms.

### half-sync-half-async-system-layering — Half-Sync/Half-Async (system layering)
- aka: —
- kind: pattern
- what: Layers a concurrent system into a synchronous service layer and an asynchronous event layer mediated by a queueing layer.
- problem: Synchronous code is simpler but async I/O is more efficient; the layering lets each part of the system use the model that suits it.
- named-in: corpus:posa2 — Pattern-Oriented Software Architecture Vol. 2 - Schmidt et al. (2000)
- tags: concurrency, os, borderline — Same name exists in the design realm (half-sync-half-async); POSA2 labels it an architectural pattern - cataloged in both realms per the same-name-two-realms rule.

### hardware-abstraction-layer-arch — Hardware Abstraction Layer (architectural layer)
- aka: HAL, MCU abstraction layer, peripheral abstraction layer, Hardware Abstraction Layer (platform layer), MCAL (AUTOSAR), Abstraction Layer (Fluent C), board abstraction layer
- kind: pattern
- what: A dedicated layer in the firmware stack that presents hardware-independent interfaces for all peripheral and processor access, so every layer above it is portable across boards and silicon.
- problem: Direct register access scattered through application code welds the product to one chip; concentrating hardware knowledge in one boundary layer makes ports, test doubles, and vendor changes tractable.
- named-in: corpus:beningofw — Reusable Firmware Development: A Practical Approach to APIs, HALs and Drivers - Beningo (2017)
- tags: embedded, portability, borderline — Same-name-two-realms: the design realm catalogs hardware-abstraction-layer as an API-shape mechanism; this entry is the layer as a position in the system's layer stack (parked from Phase 1, admitted here).

### health-check-api — Health Check API
- aka: health endpoint monitoring
- kind: pattern
- what: Each service exposes an endpoint reporting its own liveness/readiness, polled by orchestrators and load balancers to route around unhealthy instances.
- problem: Infrastructure must distinguish a live-but-degraded instance from a dead one to place traffic and restarts correctly; a self-reported health contract makes that decision mechanical.
- named-in: corpus:richardsonmp — Microservices Patterns - Richardson (2018), Health check API pattern
- tags: distributed, observability

### health-endpoint-monitoring — Health Endpoint Monitoring
- aka: health check API (Richardson), health endpoint, liveness/readiness probes (Kubernetes realization), Health Check API, liveness/readiness probes, Health Endpoint Monitoring (Azure)
- kind: pattern
- what: Services expose endpoints reporting their own health; external agents (monitors, orchestrators, load balancers) probe them to route or restart.
- problem: A process can be up yet unable to serve; standardized self-reported checks let infrastructure detect and react to partial failure.
- named-in: corpus:azurepatterns — Cloud Design Patterns: Health Endpoint Monitoring - Azure Architecture Center (living)
- tags: distributed, cloud, observability, qa:availability, microservices, ops, borderline — Design realm carries heartbeat (in-process liveness); this is the service-topology contract - related but distinct.

### health-monitor-arinc-653 — Health Monitor (ARINC 653)
- aka: HM, partition health monitoring, multi-level health monitoring
- kind: pattern
- what: A standardized architectural function that detects and reports faults at process, partition, and module level and applies configured recovery actions (restart, stop, switch) per level, defined by configuration tables rather than application code.
- problem: In a partitioned system, error handling must itself be partition-aware and criticality-aware; a system-level, table-driven monitor keeps fault escalation and recovery policy out of individual applications and under certification control.
- named-in: corpus:arinc653 — ARINC 653 - Avionics Application Standard Software Interface - AEEC (living)
- tags: embedded, avionics, safety-critical, real-time

### hierarchical-control-rtdp — Hierarchical Control (RTDP)
- aka: control hierarchy, hierarchy of controllers
- kind: pattern
- what: Distributes control policy across a hierarchy in which upper controllers set goals/modes and lower controllers execute them locally.
- problem: Centralizing all control logic does not scale and mixing policy with actuation entangles concerns.
- named-in: corpus:douglassrtcorpus — Real-Time Design Patterns - Douglass (2002)
- tags: embedded, control

### index-table — Index Table
- aka: secondary index table (storage-level)
- kind: pattern
- what: Maintains separate tables keyed by frequently queried fields over a data store that lacks native secondary indexes.
- problem: Key-value and partitioned stores answer non-key queries only via full scans unless the application maintains its own indexes.
- named-in: corpus:azurepatterns — Cloud Design Patterns - Microsoft Azure Architecture Center
- tags: data, cloud, database

### intrusion-detection-system — Intrusion Detection System
- aka: IDS, NIDS/HIDS, intrusion detection and prevention (IDPS)
- kind: pattern
- what: A dedicated component observes network traffic or host activity and flags (or blocks, as IPS) patterns indicating attack or misuse.
- problem: Preventive controls fail silently; a separate observing component turns compromise attempts into detectable, alertable events.
- named-in: corpus:denning87ids — An Intrusion-Detection Model - Denning (IEEE Trans. Software Engineering, 1987)
- tags: security, network, operability, qa:security, ops

### invoker — Invoker
- aka: server-side dispatch machinery
- kind: pattern
- what: Server-side middleware component that receives invocations, unmarshals them and dispatches to the target remote object's method.
- problem: Servers need generic machinery mapping wire requests onto object operations.
- named-in: corpus:posa4 — Pattern-Oriented Software Architecture Vol. 4 - Buschmann, Henney & Schmidt (2007)
- tags: middleware

### islands-architecture — Islands Architecture
- aka: component islands, partial hydration page structure
- kind: pattern
- what: Server-rendered pages contain isolated interactive islands that hydrate independently, leaving the rest static HTML.
- problem: Hydrating a whole page for a few interactive widgets wastes bandwidth and startup time.
- named-in: corpus:islandsarch — Islands Architecture - Jason Miller (2020)
- tags: web

### kernel-bypass-networking — Kernel-Bypass Networking
- aka: user-space networking, DPDK-style dataplane, OS-bypass I/O
- kind: pattern
- what: Restructures the I/O path so the application drives the NIC from user space via polled queues, bypassing the kernel network stack.
- problem: Kernel crossings and interrupts dominate latency/throughput at high packet rates; moving the dataplane into the application removes them.
- named-in: corpus:dpdkprogguide — DPDK Programmer's Guide (dpdk.org)
- tags: networking, performance, os

### leader-election — Leader Election
- aka: coordinator election, master election, bully/ring algorithms (realizations)
- kind: pattern
- what: Cooperating instances select exactly one of themselves as coordinator for a role, and re-elect when the leader fails.
- problem: Some actions must be done by exactly one instance in a fleet of equals; election plus failure detection avoids both split-brain and a fixed single point of failure.
- named-in: corpus:azurepatterns — Cloud Design Patterns: Leader Election - Azure Architecture Center (living)
- tags: distributed, qa:availability, coordination

### leaderless-replication — Leaderless Replication
- aka: Dynamo-style replication, quorum replication
- kind: pattern
- what: Clients (or coordinators) write to and read from multiple replicas directly, using read/write quorums, read repair, and hinted handoff instead of a leader.
- problem: High write availability under node failure and partition without failover machinery; trades strict ordering for quorum-tunable consistency.
- named-in: corpus:kleppmannddia — Designing Data-Intensive Applications - Kleppmann (2017)
- tags: distributed, data, qa:availability

### log-aggregation — Log Aggregation
- aka: centralized logging
- kind: pattern
- what: All services ship logs to a central searchable store rather than keeping them on individual hosts.
- problem: Per-host logs are useless when instances are ephemeral and requests span services; central aggregation restores a single queryable operational record.
- named-in: corpus:richardsonmp — Microservices Patterns - Richardson (2018), Log aggregation pattern
- tags: distributed, observability

### m-out-of-n-voting — MooN Voting Architecture
- aka: 1oo2, 2oo3, M-out-of-N architecture, hardware fault tolerance architectures (IEC 61508)
- kind: pattern
- what: The safety-instrumented channel topologies named MooN in IEC 61508: N channels of which M must agree/demand for the safety function to act (1oo1, 1oo2, 2oo2, 2oo3, 1oo2D...), each with defined diagnostic and voting arrangements.
- problem: Safe-failure and dangerous-failure probabilities pull channel topology in opposite directions (spurious trips vs missed demands); the MooN family names the standard trade-off points and the standard's SIL tables quantify them.
- named-in: corpus:iec61508 — IEC 61508:2010 - Functional safety of E/E/PE safety-related systems - IEC (2010)
- tags: embedded, safety-critical

### maintenance-interface — Maintenance Interface
- aka: management interface, out-of-band administration channel
- kind: pattern
- what: A separate interface/channel dedicated to administration, diagnosis and maintenance, distinct from the application service interface.
- problem: Mixing management traffic with application traffic obscures both and blocks maintenance exactly when the service path is congested or broken.
- named-in: corpus:hanmer — Patterns for Fault Tolerant Software - Hanmer (2007)
- tags: ops, embedded

### materialized-view-architecture-pattern — Materialized View (architecture pattern)
- aka: precomputed view, derived read store, Materialized View, query-shaped projection
- kind: pattern
- what: Precomputed, query-shaped copies of data are generated and refreshed from source-of-truth stores to serve reads the source format handles poorly.
- problem: Query shapes that would need expensive joins/scans against the write-optimized store; trades staleness and refresh machinery for read performance.
- named-in: corpus:azurepatterns — Cloud Design Patterns: Materialized View - Azure Architecture Center (living)
- tags: data, enterprise, database, borderline — The database-internal materialized view is a storage mechanism; kept here in its architecture-pattern sense (cross-store derived read models), per parked data-tier decision.

### message-broker — Message Broker
- aka: hub-and-spoke topology, integration broker, broker topology (messaging), hub-and-spoke messaging, Decoupling Middleware (Nygard, folded)
- kind: pattern
- what: A central intermediary receives messages from all senders and routes (and often transforms) them to the appropriate receivers, so every application couples only to the hub.
- problem: Point-to-point integration of N applications explodes into N^2 connections; a hub-and-spoke broker buys maintainable topology and central routing logic at the cost of a potential bottleneck and single point of failure. Distinct from POSA1 Broker: routes asynchronous messages rather than mediating remote invocations.
- named-in: corpus:hohpe — Enterprise Integration Patterns - Hohpe, Woolf (2003)
- tags: enterprise, distributed, messaging

### message-endpoint — Message Endpoint
- aka: messaging gateway boundary (relative)
- kind: pattern
- what: The component that connects an application to a messaging channel, encapsulating send/receive mechanics at the application boundary.
- problem: Application code should not be written against raw messaging APIs throughout; the endpoint isolates the messaging boundary.
- named-in: corpus:hohpe — Enterprise Integration Patterns - Hohpe & Woolf (2003)
- tags: messaging

### message-router — Message Router
- aka: routing component
- kind: pattern
- what: A component that consumes messages from one channel and republishes them to different channels according to routing conditions.
- problem: Senders should not need to know which consumer must handle each message; routing knowledge is centralized.
- named-in: corpus:hohpe — Enterprise Integration Patterns - Hohpe & Woolf (2003)
- tags: messaging

### messaging-bridge — Messaging Bridge
- aka: broker bridge, cross-broker connection, bridge between messaging systems, Messaging Bridge (Azure)
- kind: pattern
- what: A set of connected channel pairs (or a broker-to-broker connector) that replicates messages between two distinct messaging systems so each behaves as an extension of the other.
- problem: Organizations end up with multiple messaging infrastructures (mergers, vendors, platforms) whose applications must still exchange messages; a bridge buys interoperation without migrating either side, at the cost of mapping between two messaging semantics.
- named-in: corpus:hohpe — Enterprise Integration Patterns - Hohpe, Woolf (2003)
- tags: enterprise, integration, messaging

### model-view-controller — Model-View-Controller
- aka: MVC, Model/View/Controller (Smalltalk-80, Reenskaug lineage), Model/View/Controller (Smalltalk-80)
- kind: pattern
- what: Decomposes an interactive application into a model holding core data and logic, views presenting it, and controllers handling user input, with a change-propagation mechanism keeping them consistent.
- problem: User interfaces change far more often than the domain core and the same information needs multiple simultaneous presentations; separating model from presentation lets UIs be added or changed without touching the core. GoF ch.1 decomposes MVC into Observer, Composite, and Strategy - the design-realm bridge endpoints.
- named-in: corpus:posa1 — Pattern-Oriented Software Architecture Vol. 1: A System of Patterns - Buschmann et al (1996)
- tags: ui, interactive, app-structure

### model-view-intent — Model-View-Intent
- aka: MVI
- kind: pattern
- what: Structures the app as a reactive cycle: intents (user input streams) feed a model function producing state streams that the view renders.
- problem: Expressing the whole UI as composed observable streams removes callback wiring and mutable view state.
- named-in: corpus:cyclejsmvi — Model-View-Intent - Cycle.js documentation (Staltz)
- tags: ui, reactive

### model-view-presenter — Model-View-Presenter
- aka: MVP, supervising controller (variant), passive view (variant)
- kind: pattern
- what: UI structure where a presenter mediates all interaction between a (possibly passive) view and the model, absorbing presentation logic.
- problem: Make GUI logic testable and views thin by moving decision logic out of widgets into a mediating presenter.
- named-in: corpus:potelmvp — MVP: Model-View-Presenter - Potel (Taligent, 1996)
- tags: ui, app-structure

### model-view-viewmodel — Model-View-ViewModel
- aka: MVVM
- kind: pattern
- what: UI structure where a view binds declaratively (data binding) to a view-model exposing view-shaped state and commands over the model.
- problem: Exploit data-binding frameworks so views need no imperative glue code and presentation state is testable without the UI toolkit.
- named-in: corpus:gossmanmvvm — Introduction to Model/View/ViewModel pattern - Gossman (Microsoft blog, 2005)
- tags: ui, app-structure

### monitor-actuator — Monitor-Actuator
- aka: monitor-actuator pair, actuation channel with independent monitor, monitor-actuator channel pair, actuation channel with independent monitoring channel
- kind: pattern
- what: A two-channel structure separating the actuation channel from an independent monitoring channel that checks the actuator's physical effect against setpoints and forces a fail-safe state on divergence.
- problem: A single channel that both acts and checks itself shares failure modes between the two duties; an independent monitor with its own sensing detects actuation-channel faults without doubling the actuation hardware.
- named-in: corpus:douglassrtcorpus — Real-Time Design Patterns - Douglass (2002)
- tags: embedded, safety-critical, real-time, safety

### multi-leader-replication — Multi-Leader Replication
- aka: master-master replication, active-active replication
- kind: pattern
- what: Several nodes accept writes concurrently and asynchronously replicate to each other, requiring conflict resolution.
- problem: Accept writes in multiple datacenters or offline clients; trades single-writer simplicity for write availability plus conflict handling.
- named-in: corpus:kleppmannddia — Designing Data-Intensive Applications - Kleppmann (2017)
- tags: distributed, data, qa:availability

### object-synchronizer — Object Synchronizer
- aka: distributed object synchronization policy
- kind: pattern
- what: Decouples object replicas' synchronization policy from their functionality, coordinating state updates between distributed replicas.
- problem: Replica consistency strategies must be swappable without rewriting the replicated objects.
- named-in: corpus:plopd4 — Pattern Languages of Program Design 4 - Silva, Pereira & Marques (2000)
- tags: distributed

### page-controller — Page Controller
- aka: controller-per-page
- kind: pattern
- what: Each page or action of a web application has its own controller object handling its requests.
- problem: Simple sites are clearer with one input path per page than with a central dispatcher.
- named-in: corpus:poeaa — Patterns of Enterprise Application Architecture - Fowler (2002)
- tags: web

### policy-decision-point-policy-enforcement-point — Policy Decision Point / Policy Enforcement Point
- aka: PDP/PEP, externalized authorization, centralized authorization service, PEP-PDP-PIP-PAP topology (XACML), XACML authorization architecture
- kind: pattern
- what: Authorization is externalized: enforcement points embedded at resource boundaries defer every access decision to a central policy decision point that evaluates declarative policy.
- problem: Authorization logic scattered through components is inconsistent and unauditable; separating decision from enforcement centralizes policy while keeping enforcement local to each resource.
- named-in: corpus:xacml3 — eXtensible Access Control Markup Language (XACML) 3.0 - OASIS Standard (2013); terminology from IETF RFC 2753
- tags: security, enterprise, distributed, qa:security, borderline — Design realm holds reference-monitor (with PDP/PEP noted in its aka as the operational split); this entry catalogs the distributed authorization topology itself, the sense Phase 1's security scout parked upward.

### polyglot-persistence — Polyglot Persistence
- aka: per-need datastore selection
- kind: pattern
- what: A system deliberately uses multiple storage technologies, matching each data-management need to the store best suited for it.
- problem: One database type fits neither graph, document, relational, and cache workloads all at once; trades operational diversity for per-need fit.
- named-in: corpus:fowlerpolyglot — PolyglotPersistence - Fowler (bliki, 2011)
- tags: enterprise, data, database

### preforked-prethreaded-server — Preforked / Prethreaded Server
- aka: prefork worker pool, prethreaded server, worker-pool server (Apache prefork MPM)
- kind: pattern
- what: The server creates a pool of processes or threads at startup that take turns accepting and serving connections.
- problem: Per-connection fork/create cost and unbounded concurrency are avoided by amortizing workers across connections.
- named-in: corpus:unpv1 — UNIX Network Programming, Volume 1, 3rd ed. - Stevens, Fenner & Rudoff (2003)
- tags: networking, os, concurrency

### presentation-abstraction-control — Presentation-Abstraction-Control
- aka: PAC, PAC agents, agent hierarchy (Coutaz lineage), PAC agent hierarchy
- kind: pattern
- what: Structures an interactive system as a hierarchy of cooperating agents, each with its own presentation, abstraction, and control facet, communicating only through the control facets.
- problem: Interactive systems built from semi-autonomous subtasks (multiple tools, views, input modalities) need each agent independently developed and composed; full per-agent PAC triads buy composability at the cost of many small components and longer control paths.
- named-in: corpus:posa1 — Pattern-Oriented Software Architecture Vol. 1: A System of Patterns - Buschmann et al (1996)
- tags: ui, interactive, distributed

### presentation-model — Presentation Model
- aka: application model (Smalltalk lineage), view state abstraction
- kind: pattern
- what: A self-contained class holding all view state and behavior, which the view synchronizes with; the toolkit-independent predecessor of MVVM.
- problem: Pull view state and logic out of widgets into a testable object when the toolkit lacks data binding.
- named-in: corpus:eaadev — Further Enterprise Application Architecture development - Fowler (eaaDev, 2004)
- tags: ui, app-structure

### primary-replica-replication — Primary-Replica Replication
- aka: single-leader replication, leader-based replication, master-slave replication, log shipping
- kind: pattern
- what: One node accepts all writes and streams its change log to replicas, which serve reads and can be promoted on failure.
- problem: Read scale-out and failover for a single-writer dataset while keeping a simple consistency story on the write path.
- named-in: corpus:kleppmannddia — Designing Data-Intensive Applications - Kleppmann (2017)
- tags: distributed, data, qa:availability, database

### privilege-separation-arch — Privilege Separation
- aka: privsep, monitor/slave process split, Privilege Separation (process topology), privsep topology, privileged monitor + unprivileged worker processes, OpenSSH privilege separation, multi-process privilege partitioning
- kind: pattern
- what: Splits a program into a small privileged monitor process and unprivileged worker processes that request privileged operations over a narrow channel.
- problem: A compromise of the bulk of the code must not yield the process's privileges; the split confines them to a minimal auditable part.
- named-in: corpus:provos — Preventing Privilege Escalation - Provos, Friedl & Honeyman (2003)
- tags: security, os, qa:security

### process-manager — Process Manager
- aka: orchestrator, orchestration engine, central process control, workflow engine
- kind: pattern
- what: A central component maintains the state of each multi-step process instance and determines, step by step, which processing unit to invoke next based on intermediate results.
- problem: Multi-step message flows whose routing cannot be fixed at design time need central sequencing, state, and error handling; an orchestrator buys visibility and flexible flow control at the cost of a hub that all steps depend on. The structural alternative is itinerary-based routing (Routing Slip) or pure choreography.
- named-in: corpus:hohpe — Enterprise Integration Patterns - Hohpe, Woolf (2003)
- tags: enterprise, integration, workflow, messaging

### process-pairs — Process Pairs
- aka: primary/backup process pair, takeover pair (Tandem), checkpointing process pair, hot standby process
- kind: pattern
- what: A primary process executes while a backup process on another node receives checkpoints and takes over transparently when the primary fails.
- problem: Single-process services die with their host and lose in-flight state; a checkpointed backup converts host failure into a fast, state-preserving takeover.
- named-in: corpus:grayreuter — Transaction Processing: Concepts and Techniques - Gray & Reuter (1992); named earlier in Gray's 'Why Do Computers Stop' (1985)
- tags: distributed, qa:availability, availability

### proxy-based-firewall — Proxy-Based Firewall
- aka: application-level gateway, Firewall Proxy (POSA4)
- kind: pattern
- what: A firewall that terminates connections and re-issues them via per-protocol proxies, inspecting traffic at application level.
- problem: Packet-level rules cannot judge application-protocol content; proxying enables semantic filtering at the boundary.
- named-in: corpus:schumacher — Security Patterns: Integrating Security and Systems Engineering - Schumacher et al. (2006)
- tags: security, networking

### recursive-containment-rtdp — Recursive Containment (RTDP)
- aka: recursive decomposition of subsystems
- kind: pattern
- what: Decomposes the system recursively into parts that are themselves structured like systems, to any needed depth.
- problem: Very large systems need a uniform decomposition discipline so every level presents the same structural concepts.
- named-in: corpus:douglassrtcorpus — Real-Time Design Patterns - Douglass (2002)
- tags: embedded

### recursive-control — Recursive Control
- aka: hierarchical control components (Selic)
- kind: pattern
- what: Structures a real-time control system as a recursive hierarchy in which every component pairs its functional part with a control part, uniformly at all levels.
- problem: Startup, shutdown, failure and mode handling pervade control systems; making control structure recursive keeps it uniform and analyzable.
- named-in: corpus:plopd3 — Pattern Languages of Program Design 3 - Selic (1997)
- tags: embedded, control, real-time

### reflection — Reflection
- aka: meta-level architecture, open implementation, metaobject protocol (architecture-scale), Reflection (meta-level architecture), metaobject protocol (realization)
- kind: pattern
- what: Splits a system into a base level doing the application work and a meta level holding a self-representation (metaobjects) whose modification changes the base level's behavior and structure at runtime.
- problem: Systems that must change structure or behavior dynamically (type discovery, marshalling, adaptation) need change without editing and redeploying base code; an explicit meta level makes the software self-aware and modifiable at the price of complexity and opacity.
- named-in: corpus:posa1 — Pattern-Oriented Software Architecture Vol. 1: A System of Patterns - Buschmann et al (1996)
- tags: adaptability, middleware, general

### remote-facade — Remote Facade
- aka: coarse-grained remote facade
- kind: pattern
- what: A coarse-grained facade over fine-grained objects provides the remote interface, bundling many small interactions into few large calls.
- problem: Fine-grained object interfaces are unusable across a network; call granularity must change at the distribution boundary.
- named-in: corpus:poeaa — Patterns of Enterprise Application Architecture - Fowler (2002)
- tags: distributed, enterprise

### replicated-component-group — Replicated Component Group
- aka: component replica group
- kind: pattern
- what: Deploys a component as a coordinated group of replicas presented as one logical component, for availability or load distribution.
- problem: A single component instance is a single point of failure and a throughput ceiling.
- named-in: corpus:posa4 — Pattern-Oriented Software Architecture Vol. 4 - Buschmann, Henney & Schmidt (2007)
- tags: distributed, availability

### replication — Replication
- aka: identical redundancy, clones, Homogeneous Redundancy, replicated identical channels, replication redundancy
- kind: pattern
- what: Provide multiple identical copies of a component so their results can be voted on or a copy can take over; effective against random hardware faults.
- problem: Random hardware failures can silently corrupt a single component's behavior; pure replication offers no diversity, so it does not protect against design or implementation faults.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:availability, qa:safety, bck-cat:detect-faults, bck-cat:containment-redundancy, fault-tolerance, embedded, safety-critical, real-time, safety, availability

### reporting-database — Reporting Database
- aka: reporting replica, analytics offload database
- kind: pattern
- what: A separate database, fed from the operational store, structured and indexed for reporting/analytics queries.
- problem: Reporting workloads distort and degrade the operational schema and its performance; offloading isolates both.
- named-in: corpus:fowlerreportdb — ReportingDatabase - Fowler (bliki, 2004)
- tags: enterprise, data, database

### requestor — Requestor
- aka: client-side invocation machinery
- kind: pattern
- what: Client-side middleware component that constructs and sends remote invocations on behalf of proxies, handling marshaling and result delivery.
- problem: Invocation construction, marshaling and transport must be reusable machinery, not per-interface code.
- named-in: corpus:posa4 — Pattern-Oriented Software Architecture Vol. 4 - Buschmann, Henney & Schmidt (2007)
- tags: middleware

### routing-slip — Routing Slip
- aka: itinerary-based routing, itinerary pattern
- kind: pattern
- what: Each message carries its own list of processing steps; every step consumes its entry and forwards the message to the next step on the slip, so the route is decided once up front and no central router is consulted en route.
- problem: Message flows that vary per message but are computable at entry need sequential routing without a central orchestration bottleneck; the attached itinerary buys decentralized flow at the cost of no mid-flight re-planning and harder flow visibility.
- named-in: corpus:hohpe — Enterprise Integration Patterns - Hohpe, Woolf (2003)
- tags: enterprise, integration, workflow, messaging

### safety-executive — Safety Executive
- aka: safety kernel (Douglass usage), centralized safety monitor, safety kernel (coordinator sense)
- kind: pattern
- what: A centralized component that tracks safety-relevant events and coordinates all shutdown, recovery, and fail-safe transitions for the system, separating safety policy from the functional channels it supervises.
- problem: When safety measures are scattered across subsystems, complex shutdown sequences and cross-subsystem fault policy become inconsistent and unverifiable; centralizing them in one executive makes the safety logic auditable.
- named-in: corpus:douglassrtcorpus — Real-Time Design Patterns - Douglass (2002)
- tags: embedded, safety-critical, real-time, safety

### saga — Saga
- aka: long-lived transaction (Gray lineage), compensating-transaction sequence, long-lived transaction with compensations, orchestrated/choreographed saga
- kind: pattern
- what: A multi-step business transaction implemented as a sequence of local transactions, each with a compensating action to semantically undo it on failure.
- problem: Atomic distributed transactions (2PC) are unavailable or too coupling across services; sagas trade isolation for availability with explicit compensation.
- named-in: corpus:sagas — Sagas - Garcia-Molina & Salem (SIGMOD 1987)
- tags: distributed, enterprise, data, qa:availability, database, microservices

### sandbox — Sandbox
- aka: sandboxing, resource virtualization (form), process sandbox, software-based fault isolation (SFI), seccomp/pledge/jail confinement, broker + sandboxed renderer (Chromium), Process Sandboxing, OS-enforced isolation
- kind: pattern
- what: Isolate an instance of the system from the real world so it can be experimented on without permanent consequences, including virtualizing uncontrollable resources (system clock, memory, battery, network); stubs, mocks, and dependency injection are simple virtualization forms.
- problem: Testing against real resources with real consequences is dangerous or impossible (e.g. waiting for a real time boundary); a consequence-free, controllable replica removes the constraint.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:testability, bck-cat:control-and-observe-system-state, security, os, qa:security

### scheduler-agent-supervisor — Scheduler Agent Supervisor
- aka: —
- kind: pattern
- what: A scheduler drives distributed steps via agents while a supervisor tracks step state and triggers recovery or compensation for failed steps.
- problem: Distributed workflows need built-in observation and self-healing when individual remote actions fail.
- named-in: corpus:azurepatterns — Cloud Design Patterns - Microsoft Azure Architecture Center
- tags: cloud, distributed, workflow

### secrets-management-service — Secrets Management Service
- aka: secrets vault, vault, central secrets store, dynamic secrets issuance
- kind: pattern
- what: Credentials, keys, and tokens are held in a dedicated hardened service that issues them to workloads at runtime under authentication, audit, and rotation policies.
- problem: Secrets embedded in code, images, or config sprawl and leak; centralizing issuance gives one place for encryption at rest, access control, rotation, and audit.
- named-in: corpus:owaspcheat — OWASP Cheat Sheet Series - Secrets Management Cheat Sheet
- tags: security, cloud, operability, qa:security, ops, borderline — Named primarily in living vendor/platform documentation rather than a catalog work; kept because the component category is established across independent platforms and was parked by Phase 1's security scout.

### self-contained-component — Self-Contained Component
- aka: component directory structure (Fluent C)
- kind: pattern
- what: Organizes code into components each owning its directory, exposing one header interface, with dependencies pointing only toward more fundamental components.
- problem: Without enforced component boundaries and dependency direction, C codebases decay into cyclic tangles.
- named-in: corpus:preschern — Fluent C - Preschern (2022)
- tags: c, code-organization

### sequential-convoy — Sequential Convoy
- aka: ordered message group processing
- kind: pattern
- what: Related messages are grouped into convoys processed in order by a single consumer, while unrelated convoys proceed in parallel.
- problem: Per-key ordering must survive in a competing-consumers world that otherwise destroys sequence.
- named-in: corpus:azurepatterns — Cloud Design Patterns - Microsoft Azure Architecture Center
- tags: messaging, cloud

### server-request-handler — Server Request Handler
- aka: server-side transport handler
- kind: pattern
- what: Server-side middleware component that accepts connections, receives request messages and hands them to invokers, returning replies.
- problem: Server transport concerns (demuxing, concurrency, buffering) need a dedicated reusable layer below dispatch.
- named-in: corpus:posa4 — Pattern-Oriented Software Architecture Vol. 4 - Buschmann, Henney & Schmidt (2007)
- tags: middleware, networking

### server-session-state — Server Session State
- aka: in-memory session state, in-memory session
- kind: pattern
- what: Session state is kept in the application server's memory (possibly serialized or replicated) between requests.
- problem: Simplest handling of rich session data; costs sticky routing or replication and complicates failover and scale-out.
- named-in: corpus:poeaa — Patterns of Enterprise Application Architecture - Fowler (2002)
- tags: enterprise, web, state-placement

### service-layer — Service Layer
- aka: application service layer, application facade layer
- kind: pattern
- what: A layer of application services defines the system's available operations, coordinating domain logic, transactions and responses per operation.
- problem: Multiple interface kinds (UI, API, batch) must share one authoritative boundary of application operations.
- named-in: corpus:poeaa — Patterns of Enterprise Application Architecture - Fowler (2002)
- tags: enterprise

### sharding — Sharding
- aka: partitioning, horizontal partitioning, data partitioning, partitioning across nodes, Sharding (Azure)
- kind: pattern
- what: A dataset is split by key across nodes (range or hash partitioning) so each shard is stored and served independently, with rebalancing and request routing.
- problem: Data or write volume exceeds one node; partitioning scales linearly but introduces routing, rebalancing, hot spots, and cross-shard operations.
- named-in: corpus:kleppmannddia — Designing Data-Intensive Applications - Kleppmann (2017)
- tags: distributed, data, qa:scalability, database

### single-sign-on — Single Sign-On
- aka: SSO, third-party authentication topology, Kerberos/OAuth/OIDC federation (realizations)
- kind: pattern
- what: One authentication event with a trusted authority yields tokens/tickets accepted by many independent systems.
- problem: Per-system logins multiply credentials and attack surface; centralizing authentication trades in a single trusted authority.
- named-in: corpus:coresecpat — Core Security Patterns - Steel, Nagappan & Lai (2005)
- tags: security, enterprise

### someone-in-charge — Someone in Charge
- aka: designated fault-handling authority
- kind: pattern
- what: For every fault-tolerance activity some identified component is in charge of seeing it through to completion.
- problem: Recovery actions with no owner stall when the initiating component itself fails.
- named-in: corpus:hanmer — Patterns for Fault Tolerant Software - Hanmer (2007)
- tags: availability

### strangler-fig — Strangler Fig
- aka: strangler application, strangler pattern, StranglerFigApplication (Fowler 2004)
- kind: pattern
- what: Incrementally build the new system around the edges of the old, intercepting and redirecting functionality until the legacy system is fully displaced.
- problem: Big-bang rewrites fail; this gives continuously shippable migration with reversible steps and a shrinking legacy core.
- named-in: corpus:azurepatterns — Cloud Design Patterns - Microsoft Azure Architecture Center
- tags: enterprise, migration

### supervision-tree-otp — Supervision Tree (OTP)
- aka: supervisor hierarchy, OTP supervision principles
- kind: pattern
- what: Workers are organized under a tree of supervisors whose only job is to monitor children and apply restart strategies (one-for-one, one-for-all, rest-for-one).
- problem: Let-it-crash fault handling needs a system-wide structure that turns individual process failures into controlled restarts.
- named-in: corpus:otpdesign — OTP Design Principles - Erlang/OTP System Documentation
- tags: erlang, availability, concurrency, borderline — Design realm carries supervisor (the restart mechanism); this is the whole-system supervision topology - same-name-two-realms.

### table-module — Table Module
- aka: one class per table organization
- kind: pattern
- what: Organizes domain logic with one class per database table, each instance handling all rows of its table.
- problem: A middle ground between transaction scripts and a full domain model that maps directly onto record-set infrastructure.
- named-in: corpus:poeaa — Patterns of Enterprise Application Architecture - Fowler (2002)
- tags: enterprise, database

### template-view — Template View
- aka: server page rendering, markup with embedded markers
- kind: pattern
- what: Renders web pages from static markup templates with embedded markers that are filled with dynamic content.
- problem: Page structure should be editable as markup by non-programmers while dynamic data slots in cleanly.
- named-in: corpus:poeaa — Patterns of Enterprise Application Architecture - Fowler (2002)
- tags: web

### the-elm-architecture — The Elm Architecture
- aka: Model-View-Update, MVU, TEA
- kind: pattern
- what: App structured as an immutable model, a pure update function folding messages into the model, and a pure view function rendering it.
- problem: Make whole-app state transitions pure, replayable, and exhaustively type-checked; the functional refinement of unidirectional data flow.
- named-in: corpus:elmarch — The Elm Architecture - Czaplicki (Official Elm Guide, living)
- tags: ui, functional, app-structure

### thread-per-connection-server — Thread-per-Connection Server
- aka: one-thread-per-client, process-per-connection, fork-per-connection, concurrent server
- kind: pattern
- what: The server dedicates a freshly created process or thread to each accepted connection for its lifetime.
- problem: Serving clients concurrently with straightforward sequential per-client code, at the cost of per-connection resource use.
- named-in: corpus:unpv1 — UNIX Network Programming, Volume 1, 3rd ed. - Stevens, Fenner & Rudoff (2003)
- tags: networking, concurrency, os

### time-and-space-partitioning — Time and Space Partitioning
- aka: robust partitioning, partitioned RTOS architecture, ARINC 653 partitioning, APEX partition architecture, temporal and spatial partitioning, IMA partitioning, spatial/temporal partitioning
- kind: pattern
- what: An operating-system-enforced structure in which applications run in partitions with statically allocated memory regions (space) and fixed cyclic execution windows (time), so no partition can affect another's resources or timing.
- problem: Hosting multiple applications of different criticality on one computer risks interference; enforced partitioning lets mixed-criticality software share hardware while preserving the independence that certification requires.
- named-in: corpus:arinc653 — ARINC 653 - Avionics Application Standard Software Interface - AEEC (living)
- tags: embedded, real-time, avionics, safety-critical, os, safety

### transaction-script — Transaction Script
- aka: procedure-per-request organization
- kind: pattern
- what: Organizes all domain logic as one procedure per business transaction, each handling its request from presentation to database.
- problem: For simple logic, straight procedures are cheaper and clearer than an object model.
- named-in: corpus:poeaa — Patterns of Enterprise Application Architecture - Fowler (2002)
- tags: enterprise

### transactional-outbox — Transactional Outbox
- aka: outbox pattern, application events (Richardson's earlier name), application events via outbox relay
- kind: pattern
- what: Service writes outgoing messages into an outbox table within the local database transaction; a relay publishes them to the broker afterwards.
- problem: Atomically update state and publish an event without distributed transactions across a database and a message broker.
- named-in: corpus:microservicesio — microservices.io: Pattern - Transactional Outbox - Richardson (living)
- tags: distributed, enterprise, messaging, data, microservices, database

### transform-view — Transform View
- aka: element-by-element transform rendering
- kind: pattern
- what: Renders output by programmatically transforming each domain data element into its presentation form.
- problem: When output structure follows data structure, a transform is more testable and composable than a template.
- named-in: corpus:poeaa — Patterns of Enterprise Application Architecture - Fowler (2002)
- tags: web

### triple-modular-redundancy — Triple Modular Redundancy
- aka: TMR, triplex voting, 2-out-of-3 masking redundancy, 2oo3 voting, three-channel voting redundancy
- kind: pattern
- what: Three identical channels compute in parallel and a voter forwards the majority result, masking any single channel failure without interruption of service.
- problem: Fail-over redundancy has a detection-and-switch gap; majority voting removes the gap by masking the fault instantly, at the price of triple resources plus a voter that becomes the critical element.
- named-in: corpus:douglassrtcorpus — Real-Time Design Patterns - Douglass (2002)
- tags: embedded, safety-critical, real-time, safety, availability

### trusted-execution-environment — Trusted Execution Environment
- aka: TEE, secure enclave, TrustZone secure world, enclave (Intel SGX)
- kind: pattern
- what: A hardware-isolated execution partition runs security-critical code and holds secrets, exposing only a narrow call interface to the untrusted rich OS beside it.
- problem: Keys and critical logic cannot be protected by an OS that may itself be compromised; a hardware-enforced parallel world keeps them safe even under full OS compromise.
- named-in: corpus:gpteearch — TEE System Architecture - GlobalPlatform (living specification)
- tags: security, embedded, hardware, qa:security, borderline — Hardware-adjacent as charter notes, but the split into secure-world and normal-world software with a defined boundary is a software architecture structure, first-class for the corpus's embedded center of gravity.

### two-phase-commit — Two-Phase Commit
- aka: 2PC, XA transactions (standardized realization), atomic commitment protocol, presumed abort / presumed commit (variants)
- kind: pattern
- what: A coordinator drives distributed atomic commit: participants first vote prepared, then all commit or all abort on the coordinator's decision.
- problem: Atomicity across multiple resource managers; the price is blocking on coordinator failure and latency of two round trips.
- named-in: corpus:kleppmannddia — Designing Data-Intensive Applications - Kleppmann (2017); original treatment: Gray, Notes on Data Base Operating Systems (1978)
- tags: distributed, data, database

### two-step-view — Two Step View
- aka: logical page then formatting
- kind: pattern
- what: Renders pages in two stages: first a logical presentation independent of look, then a formatting stage applying the site appearance.
- problem: A consistent site-wide look must be changeable in one place across many page types.
- named-in: corpus:poeaa — Patterns of Enterprise Application Architecture - Fowler (2002)
- tags: web

### units-of-mitigation — Units of Mitigation
- aka: recovery unit decomposition, error-recovery granule
- kind: pattern
- what: Divides the system into the units within which errors are contained and recovery is performed - the granularity of restart and repair.
- problem: Recovery scope must be decided architecturally: too large and everything restarts, too small and coordination explodes.
- named-in: corpus:hanmer — Patterns for Fault Tolerant Software - Hanmer (2007)
- tags: availability

### valet-key — Valet Key
- aka: token-scoped direct resource access
- kind: pattern
- what: The application issues clients a restricted token granting direct, time-limited access to a specific resource or store, bypassing the application for data transfer.
- problem: Proxying bulk data through the application wastes its capacity; scoped tokens grant safe direct access.
- named-in: corpus:azurepatterns — Cloud Design Patterns - Microsoft Azure Architecture Center
- tags: security, cloud

### watchdog-architecture-pattern — Watchdog (architecture pattern)
- aka: watchdog pattern (RTDP), watchdog-supervised architecture, task supervision structure
- kind: pattern
- what: A system-level supervision structure: an independent watchdog component (often on separate hardware with its own time base) receives liveness/sanity evidence from the supervised channels and initiates recovery or fail-safe shutdown when evidence stops or fails checks.
- problem: A hung or corrupted system cannot rescue itself from within; placing the last-resort monitor outside the supervised computation, with an independent clock, keeps recovery credible under common-mode failure.
- named-in: corpus:douglassrtcorpus — Real-Time Design Patterns - Douglass (2002)
- tags: embedded, safety-critical, real-time, borderline — Same-name-two-realms: the design realm's watchdog is the timer mechanism and its kick discipline; Douglass's RTDP Watchdog Pattern is the system-level supervision structure cataloged here.


## Architectural tactics (Bass-style quality-attribute primitives) — `tactic` (109)

### abort — Abort
- aka: fail-safe termination
- kind: tactic
- what: If an operation is determined to be unsafe, terminate it before it causes damage — the conceptually simplest way to make a system fail safely.
- problem: Continuing a hazardous operation converts a detected unsafe state into an accident; stopping is often the safest available response.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:safety, bck-cat:containment-limit-consequences, safety-critical

### abstract-common-services — Abstract Common Services
- aka: factor common services
- kind: tactic
- what: Where elements provide similar services, factor the similarity into a single more general/abstract service used by all, hiding the specifics of the variants.
- problem: Duplicate similar services multiply both modification cost (each copy changes) and integration surface; one abstraction localizes both.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:integrability, qa:modifiability, bck-cat:limit-dependencies, bck-cat:reduce-coupling

### abstract-data-sources — Abstract Data Sources
- aka: swappable data sources
- kind: tactic
- what: Abstract the interfaces to a program's input data so test data can be substituted easily — e.g. repointing the system from a production customer database to test databases or data files without changing functional code.
- problem: Tests need controlled input data; hard-wired data sources force testing against uncontrollable production data.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:testability, bck-cat:control-and-observe-system-state

### adhere-to-standards — Adhere to Standards
- aka: follow standards, standards conformance
- kind: tactic
- what: Conform to published interface, protocol, and data standards so that elements built independently can interoperate with less adaptation.
- problem: Idiosyncratic interfaces force per-pair integration work; standardization lets the ecosystem amortize it.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:integrability, bck-cat:limit-dependencies

### aggregate-tactic — Aggregate
- aka: group operations
- kind: tactic
- what: Provide the ability to aggregate lower-level objects into a group so an operation applies to the whole group, e.g. selecting all slide objects and setting one font size.
- problem: Repeating the same operation across many objects is tedious and error-prone for users.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:usability, bck-cat:support-user-initiative, ui

### analytic-redundancy — Analytic Redundancy
- aka: input/output diversity, high-assurance/high-performance split
- kind: tactic
- what: Provide redundant components that are diverse not only internally but also in their inputs and outputs (e.g. computing aircraft altitude by barometric pressure, radar, and geometry), with a sophisticated blending/voting mechanism.
- problem: Specification errors defeat functionally redundant components built to the same specification; independent requirement specifications and diverse input sources tolerate them, and help when some inputs are intermittently unavailable.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:availability, qa:safety, bck-cat:detect-faults, bck-cat:containment-redundancy, embedded, safety-critical, fault-tolerance

### audit — Audit
- aka: audit trail (mechanism: see design-realm audit-log)
- kind: tactic
- what: Record user and system actions and their effects so an attacker's actions can be traced and identified, supporting prosecution and improved future defenses.
- problem: After a successful attack, reconstruction of what happened and by whom is impossible without a maintained record.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:security, bck-cat:recover-from-attacks, security, same-name:design-realm

### authenticate-actors — Authenticate Actors
- aka: authentication
- kind: tactic
- what: Ensure an actor actually is who or what it claims to be, via passwords, one-time passwords, digital certificates, two-factor authentication, biometrics, or CAPTCHA challenges, possibly with periodic re-authentication.
- problem: Identifiers can be claimed by anyone; proof of identity must back them before granting access.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:security, bck-cat:resist-attacks, security

### authorize-actors — Authorize Actors
- aka: authorization, access control
- kind: tactic
- what: Ensure an authenticated actor has the rights to access and modify data or services, via access control mechanisms assigned per actor, actor class, or role.
- problem: Authenticated identity alone says nothing about what the actor may do; permissions must be checked per resource and operation.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:security, bck-cat:resist-attacks, security

### bound-execution-times — Bound Execution Times
- aka: limit execution time, iteration bounds
- kind: tactic
- what: Place a limit on how much execution time is used to respond to an event — e.g. bounding iteration counts in data-dependent iterative algorithms — trading computational accuracy for bounded latency.
- problem: Unbounded computations make response time unpredictable; often paired with Manage Sampling Rate, and requires assessing whether the less-accurate result is good enough.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:performance, qa:energy-efficiency, bck-cat:control-resource-demand, real-time

### bound-queue-sizes — Bound Queue Sizes
- aka: limit queue sizes
- kind: tactic
- what: Control the maximum number of queued arrivals, and thereby the resources used to process them, with an explicit policy for what happens when queues overflow.
- problem: Unbounded queues consume unbounded resources and hide overload; bounding them forces a deliberate overflow/loss policy, usually paired with Limit Event Response.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:performance, bck-cat:manage-resources, same-name:design-realm

### cancel — Cancel
- aka: user cancel support
- kind: tactic
- what: Support user-issued cancellation: a listener not blocked by the operation being cancelled, termination of the activity, release of its resources, and notification of collaborating components so they act appropriately.
- problem: Users must be able to stop an in-progress operation; naive designs block the cancel path behind the very operation to be cancelled and leak its resources.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:usability, bck-cat:support-user-initiative, ui

### change-credential-settings — Change Credential Settings
- aka: change default settings (3rd ed name), credential rotation
- kind: tactic
- what: Force users to change default security settings and credentials on delivered systems, and require periodic password changes.
- problem: Publicly known default credentials and stale passwords give attackers ready-made entry.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:security, bck-cat:resist-attacks, security

### comparison — Comparison
- aka: redundant-output comparison
- kind: tactic
- what: Detect potentially unsafe states by comparing the outputs of redundant components and flagging divergence.
- problem: A single component cannot detect its own erroneous output; comparison against redundant peers exposes it. Detection counterpart of the availability Voting tactic (which also chooses a result).
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:safety, bck-cat:unsafe-state-detection, safety-critical

### condition-monitoring — Condition Monitoring
- aka: checksum monitoring (example)
- kind: tactic
- what: Check conditions in a process or device, or validate assumptions made during design (e.g. by computing checksums), to prevent the system from producing faulty behavior.
- problem: A system can drift outside its assumed operating conditions without any single operation failing; the monitor itself must be simple enough not to introduce new faults.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:availability, qa:safety, bck-cat:detect-faults

### configure-behavior — Configure Behavior
- aka: behavioral configuration
- kind: tactic
- what: Build components so their behavior can be configured — during build, deployment/startup, or runtime — to operate in the modes an integrating system expects.
- problem: A component with a single fixed behavior fits only one integration context; configurability lets one implementation satisfy many.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:integrability, bck-cat:adapt

### defense-in-depth — Defense in Depth
- aka: layered security, layered defense, security in depth, compartmentalized controls
- kind: tactic
- what: Multiple independent security controls are layered along the path to an asset so that compromising any single control does not compromise the system.
- problem: Any single control can fail or be bypassed; stacking heterogeneous barriers forces an attacker to defeat several mechanisms and buys detection time.
- named-in: corpus:schumacher — Security Patterns: Integrating Security and Systems Engineering - Schumacher et al. (2006); also NIST SP 800-53 usage
- tags: security, qa:security, borderline — Principle-flavored, admitted as the structural layering of independent controls (bridge endpoint for validation, authN/Z, and isolation design elements).

### defer-binding — Defer Binding
- aka: late binding, defer binding time
- kind: tactic
- what: Bind values and choices as late in the life cycle as cost-effective: at compile/build time (component replacement, compile-time parameterization, aspects), at deployment/startup (configuration-time binding, resource files), or at runtime (discovery, interpreted parameters, shared repositories, polymorphism).
- problem: Human-mediated change is costly and error-prone; building in flexibility lets computers effect the change, trading up-front mechanism cost against per-change cost and enabling change by non-developers ('externalizing' change).
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:modifiability, bck-cat:defer-binding

### degradation — Degradation
- aka: graceful degradation, degradation tactic (Bass), degraded mode, limp-home mode, load shedding at system level (relative)
- kind: tactic
- what: In the presence of component failures, maintain the most critical system functions while dropping or substituting less critical ones in a planned, deliberate, safe way.
- problem: Individual component failures should reduce system functionality gracefully rather than cause total collapse; e.g. a navigation system falling back to dead reckoning in a tunnel.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:availability, qa:safety, bck-cat:recover-preparation-and-repair, bck-cat:containment-limit-consequences, fault-tolerance, safety, availability

### detect-intrusion — Detect Intrusion
- aka: signature-based intrusion detection
- kind: tactic
- what: Compare network traffic or service request patterns within a system against a database of signatures or known patterns of malicious behavior (protocol, payload size, source/destination address, port).
- problem: Attacks in progress must be recognized among legitimate traffic before the system can react.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:security, bck-cat:detect-attacks, security

### detect-message-delay — Detect Message Delay
- aka: detect message delivery anomalies, timing-based MITM detection
- kind: tactic
- what: Detect potential man-in-the-middle attacks by checking the time taken to deliver or receive messages against normally stable delivery times, and by watching for anomalous connect/disconnect counts.
- problem: An interceptor that reads or modifies messages in transit adds latency and connection churn that timing analysis can expose.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:security, bck-cat:detect-attacks, security, networking

### detect-service-denial — Detect Service Denial
- aka: DoS detection
- kind: tactic
- what: Compare the pattern or signature of incoming network traffic against historical profiles of known denial-of-service attacks.
- problem: Denial-of-service traffic must be distinguished from legitimate load spikes before countermeasures can be applied.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:security, bck-cat:detect-attacks, security, networking

### discover — Discover
- aka: service discovery, discovery service, service registry, client-side discovery, server-side discovery, self-registration / third-party registration (variants)
- kind: tactic
- what: Match service requests to service providers at runtime through a discovery service, enabling identification and remote invocation of providers that were not bound at build time; in the energy context, requests can be annotated so providers are selected by energy characteristics.
- problem: Statically bound providers cannot be swapped or selected by runtime criteria (location, version, energy cost); a discovery mechanism defers and mediates the binding.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:integrability, qa:energy-efficiency, bck-cat:adapt, bck-cat:allocate-resources, distributed, cloud

### dynamic-classification — Dynamic Classification
- aka: dynamic energy model
- kind: tactic
- what: Estimate energy consumption with a dynamic model — a table lookup, a regression over past executions, or a simulation — that accounts for transient conditions such as workload.
- problem: Static energy models are insufficient when consumption depends heavily on runtime conditions.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:energy-efficiency, bck-cat:monitor-resources

### encapsulate — Encapsulate
- aka: introduce explicit interface
- kind: tactic
- what: Introduce an explicit interface to an element and hide its internals so that other elements depend only on the interface, reducing the strength of coupling and the syntactic/semantic distance to be bridged.
- problem: Direct dependence on an element's internals means every internal change and every integration must confront those internals; an interface localizes the dependency.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:integrability, qa:modifiability, bck-cat:limit-dependencies, bck-cat:reduce-coupling

### encrypt-data — Encrypt Data
- aka: encryption, symmetric/asymmetric encryption
- kind: tactic
- what: Apply encryption (symmetric or asymmetric) to stored data and to communication, providing confidentiality beyond authorization controls — and the sole protection on links that have none.
- problem: Data at rest and in transit can be read by parties outside the authorization perimeter; encryption makes possession without keys useless.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:security, bck-cat:resist-attacks, security

### escalating-restart — Escalating Restart
- aka: multi-level restart
- kind: tactic
- what: Recover by restarting components at progressively coarser granularity levels (e.g. child threads only, then unprotected memory, then all memory, then full image reload), choosing the least disruptive level that clears the fault.
- problem: A full restart is maximally disruptive; matching the restart granularity to the fault minimizes the impact on service, supporting graceful degradation.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:availability, bck-cat:recover-reintroduction, embedded, fault-tolerance

### exception-detection — Exception Detection
- aka: system-exception detection
- kind: tactic
- what: Detect system conditions that alter the normal flow of execution, refined by the book into system exceptions, parameter fence, parameter typing, and timeout.
- problem: Faults such as divide-by-zero, bus/address faults, illegal instructions, or violated timing constraints must be turned into detectable events rather than silent corruption.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:availability, bck-cat:detect-faults

### exception-handling — Exception Handling
- aka: error-code handling, exception classes
- kind: tactic
- what: After an exception is detected, handle it using mechanisms ranging from function return codes to exception classes carrying name, origin, and cause, so the fault can be masked or repaired.
- problem: Simply crashing on a detected exception is unacceptable for availability; the system needs structured information and a place to act on it.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:availability, bck-cat:recover-preparation-and-repair

### exception-prevention — Exception Prevention
- aka: smart pointers (example), wrappers (example), error-correcting codes (example)
- kind: tactic
- what: Employ techniques that keep exceptions from arising at all — error-correcting codes, abstract data types such as smart pointers, and wrappers that preclude dangling pointers or semaphore access violations.
- problem: Whole fault classes (resource leaks, out-of-bounds access) can be excluded by construction more cheaply than detecting and recovering from them.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:availability, bck-cat:prevent-faults

### executable-assertions — Executable Assertions
- aka: embedded assertions, pre/postconditions and invariants
- kind: tactic
- what: Hand-code assertions checking that data values satisfy specified constraints — placed wherever the data is referenced or modified, expressible as method pre/postconditions or class invariants — so the program flags when and where it enters a faulty state.
- problem: Faulty states can pass silently through execution; systematically placed assertions embed the test oracle in the code, increasing observability.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:testability, bck-cat:control-and-observe-system-state, same-name:design-realm

### failover — Failover
- aka: switchover to standby, active-passive takeover
- kind: tactic
- what: On failure of an active unit, service is switched to a redundant standby unit that assumes its role.
- problem: Continuity of service across unit failures requires a designated takeover path and role reassignment.
- named-in: corpus:hanmer — Patterns for Fault Tolerant Software - Hanmer (2007)
- tags: qa:availability, availability, distributed

### feature-toggle — Feature Toggle
- aka: kill switch, feature flag (design-realm realization)
- kind: tactic
- what: Integrate a runtime 'kill switch' for new features so a deployed feature can be automatically disabled without initiating a new deployment.
- problem: Even fully tested features can misbehave after deployment; controlling them without the cost and risk of redeploying requires a toggle mechanism in the architecture.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:deployability, bck-cat:manage-deployed-system, devops, same-name:design-realm

### heartbeat-tactic — Heartbeat
- aka: periodic liveness message, watchdog reset (special case)
- kind: tactic
- what: A monitored component periodically emits a message to (or resets a watchdog timer in) a system monitor, so that the absence of the heartbeat signals failure.
- problem: Failure of a component must be detected without the monitor having to actively probe it; the component itself takes the initiative to demonstrate liveness.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:availability, bck-cat:detect-faults, distributed, fault-tolerance, same-name:design-realm

### identify-actors — Identify Actors
- aka: actor identification
- kind: tactic
- what: Identify the source of any external input to the system — users by user IDs; other systems by access codes, IP addresses, protocols, or ports.
- problem: Authentication and authorization presuppose knowing which actor an input claims to come from.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:security, bck-cat:resist-attacks, security

### ignore-faulty-behavior — Ignore Faulty Behavior
- aka: ignore spurious messages
- kind: tactic
- what: Ignore messages from a particular source once they are determined to be spurious, e.g. messages from a sensor known to have failed.
- problem: A faulty component can flood the system with bogus events; continuing to act on them propagates the fault.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:availability, bck-cat:recover-preparation-and-repair, embedded

### increase-competence-set — Increase Competence Set
- aka: expand competence set
- kind: tactic
- what: Design a component to handle more cases — states that would otherwise be faults — as part of its normal operation, e.g. waiting or returning gracefully when a resource is blocked instead of throwing.
- problem: A component throws an exception when it finds itself outside the set of states it is competent to handle; enlarging that set converts faults into handled situations.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:availability, bck-cat:prevent-faults

### increase-resource-usage-efficiency — Increase Resource Usage Efficiency
- aka: increase efficiency, algorithmic optimization
- kind: tactic
- what: Improve the efficiency of the algorithms used in critical areas to decrease latency and improve throughput and resource consumption.
- problem: Inefficient critical-path algorithms consume resources that better algorithms would free; 'optimizing the code' is one tactic among many, not the only lever.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:performance, qa:energy-efficiency, bck-cat:control-resource-demand

### increase-resources — Increase Resources
- aka: scale up, add capacity
- kind: tactic
- what: Add or upgrade resources — faster processors, additional processors, more memory, faster networks — to improve performance.
- problem: When demand cannot be reduced, capacity must grow; despite its cost, adding resources is often the cheapest immediate route to better performance.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:performance, bck-cat:manage-resources

### inform-actors — Inform Actors
- aka: attack notification
- kind: tactic
- what: When the system detects an attack, notify the relevant set of actors — operators, other personnel, or cooperating systems — so they can act.
- problem: An ongoing attack may require human or cross-system action that the detecting system cannot take alone.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:security, bck-cat:react-to-attacks, security

### interlock — Interlock
- aka: sequence enforcement
- kind: tactic
- what: Protect against failures arising from incorrect event ordering by controlling all access to protected components, including enforcing the correct sequencing of events affecting them.
- problem: Some hazards arise not from wrong values but from right actions in the wrong order; an interlock makes illegal orderings impossible.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:safety, bck-cat:containment-barrier, embedded, safety-critical

### introduce-concurrency — Introduce Concurrency
- aka: parallel processing of requests
- kind: tactic
- what: Process requests in parallel — different event streams on different threads, or additional threads for different activity sets — to reduce blocked time, then choose a scheduling policy via Schedule Resources.
- problem: Serialized processing leaves requests blocked behind one another even when independent; concurrency reclaims that waiting time.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:performance, bck-cat:manage-resources

### limit-access — Limit Access
- aka: attack-surface reduction, DMZ (realization)
- kind: tactic
- what: Restrict access to computing resources by limiting the number of access points and/or the types of traffic allowed through them — e.g. a demilitarized zone between internet and intranet bounded by a pair of firewalls.
- problem: Every access point and permitted traffic type enlarges the attack surface; minimizing both contains exposure.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:security, bck-cat:resist-attacks, security, networking

### limit-event-response — Limit Event Response
- aka: maximum processing rate, event throttling
- kind: tactic
- what: Process events only up to a set maximum rate, queueing or deliberately dropping events that arrive faster, triggered by queue size, processor utilization, or SLA violation.
- problem: Bursts beyond processing capacity force a policy choice: guarantee no loss (size queues for the worst case) or drop events (and decide whether to log or notify).
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:performance, qa:energy-efficiency, bck-cat:control-resource-demand

### limit-exposure — Limit Exposure
- aka: minimize single-point exposure
- kind: tactic
- what: Minimize the damage a successful attack can do by reducing the amount of data or services reachable through any single access point — a passive defense that compartmentalizes value.
- problem: If one breached access point yields everything, every breach is catastrophic; spreading assets bounds per-attack loss.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:security, bck-cat:resist-attacks, security

### limit-nondeterminism — Limit Nondeterminism
- aka: determinism enforcement
- kind: tactic
- what: Find and, where possible, eliminate sources of behavioral nondeterminism such as unconstrained parallelism; where unavoidable (e.g. multithreaded response to unpredictable events), manage it with tactics like record/playback.
- problem: Nondeterministic systems are pernicious to test because failures do not reproduce; determinism restores repeatability.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:testability, bck-cat:limit-complexity

### limit-structural-complexity — Limit Structural Complexity
- aka: structural simplification for test
- kind: tactic
- what: Keep the structure simple enough to test: avoid or resolve cyclic dependencies, isolate and encapsulate environmental dependencies, reduce inter-component coupling, constrain inheritance depth/fan-out and polymorphism, and track metrics such as response-of-class, propagation cost, and decoupling level.
- problem: Large operational state spaces make recreating an exact state — and thus reproducing failures — hard; high cohesion, loose coupling, and separation of concerns shrink the state space.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:testability, bck-cat:limit-complexity

### localize-state-storage — Localize State Storage
- aka: externalized state, state machine as state store
- kind: tactic
- what: Store system/subsystem/component state in a single place — conveniently a state machine object tracking and reporting the current state — so tests can start the system in any desired state, at whatever granularity testing needs.
- problem: Hidden or scattered state makes starting a test from an arbitrary known state difficult or impossible.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:testability, bck-cat:control-and-observe-system-state

### maintain-multiple-copies-of-computations — Maintain Multiple Copies of Computations
- aka: replicated services, server pool
- kind: tactic
- what: Run multiple replicas of a computation (replicated services in a microservice architecture, replicated web servers in a pool) with a load balancer assigning new work among them.
- problem: Funneling all service requests through a single instance creates contention; replicas spread the load.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:performance, bck-cat:manage-resources, distributed

### maintain-multiple-copies-of-data — Maintain Multiple Copies of Data
- aka: caching (realization), data replication (realization)
- kind: tactic
- what: Keep copies of data — replication (separate identical copies to reduce contention) or caching (copies, possibly subsets, on storage with different access speeds, possibly predictively prefetched) — accepting the burden of keeping copies consistent.
- problem: Simultaneous access to one copy of data creates contention, and distant/slow storage adds latency; copies trade consistency-maintenance work for reduced contention and faster access.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:performance, bck-cat:manage-resources, distributed, same-name:design-realm

### maintain-system-model — Maintain System Model
- aka: system self-model, progress bar (manifestation)
- kind: tactic
- what: The system maintains an explicit model of itself to determine expected system behavior and give users appropriate feedback — the progress bar predicting time to completion is the canonical manifestation.
- problem: Users need feedback about what the system is doing and how long it will take; producing it requires the system to model its own behavior.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:usability, bck-cat:support-system-initiative, ui

### maintain-task-model — Maintain Task Model
- aka: task model
- kind: tactic
- what: Maintain a model of the task the user is performing so the system can infer context and assist — e.g. predictive type-ahead in search engines, spell correction in mail clients.
- problem: System-initiated help requires knowing what the user is trying to do; without a task model the system cannot anticipate.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:usability, bck-cat:support-system-initiative, ui

### maintain-user-model — Maintain User Model
- aka: user model
- kind: tactic
- what: Maintain an explicit model of a user or user class — their knowledge of the system, expected response-time behavior, error patterns — updated dynamically or offline; user-interface customization is a special case where users edit the model directly.
- problem: One-size-fits-all interaction ignores what individual users know and need; encapsulating the model makes tailoring and modification easy.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:usability, bck-cat:support-system-initiative, ui

### manage-event-arrival — Manage Event Arrival
- aka: manage work requests (parent grouping), SLA-based arrival control
- kind: tactic
- what: Control the arrival rate of events from external systems, canonically by setting a service level agreement that fixes the maximum event rate the system will support, constraining both system and clients.
- problem: Demand beyond the sustainable arrival rate degrades everyone's response time; capping arrivals makes load explicit and pushes overflow to additional instances.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:performance, qa:energy-efficiency, bck-cat:control-resource-demand, distributed

### manage-resources-integrability — Manage Resources (Integrability)
- aka: resource manager
- kind: tactic
- what: Interpose an explicit resource manager that mediates access to shared computing resources (memory, threads, hardware devices) so independently developed components can share them safely.
- problem: Components that each assume exclusive resource ownership conflict when integrated; a mediator arbitrates. (Named 'Manage Resources' in bck's integrability chapter; not to be confused with the performance category of the same name.)
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:integrability, bck-cat:coordinate, embedded

### manage-sampling-rate — Manage Sampling Rate
- aka: reduce sampling frequency, adaptive sampling
- kind: tactic
- what: Reduce (possibly dynamically) the frequency at which environmental input is sampled — sensor data rates, video frames per second — trading fidelity for predictable latency.
- problem: When the system cannot keep up with the incoming data stream, lower-fidelity but stable processing may beat unstable latency; common in signal-processing systems.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:performance, qa:energy-efficiency, bck-cat:control-resource-demand, embedded, real-time

### manage-service-interactions — Manage Service Interactions
- aka: version-coexistence management
- kind: tactic
- what: Allow multiple versions of system services to be deployed and executed simultaneously, with client requests routed to any version, coordinating inter-service interactions to proactively avoid version incompatibilities.
- problem: Simultaneously running old and new versions avoids fully duplicating resources during upgrade but introduces version-compatibility hazards that must be managed.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:deployability, bck-cat:manage-deployed-system, distributed, devops

### masking — Masking
- aka: fault masking by voting
- kind: tactic
- what: Mask a fault by comparing the results of several redundant components and using a voting procedure when they differ, so the faulty result never propagates; requires a simple, highly reliable voter.
- problem: Some systems must keep producing correct outputs through component faults, not merely detect them; masking hides the fault behind redundancy.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:safety, bck-cat:containment-limit-consequences, safety-critical, fault-tolerance

### metering — Metering
- aka: energy metering
- kind: tactic
- what: Collect data about the energy consumption of computing resources in near real time via a sensor infrastructure — from data-center meters down to metered rack PDUs, ASICs, or battery management systems.
- problem: Energy cannot be managed without being measured; different granularities of measurement need different instrumentation.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:energy-efficiency, bck-cat:monitor-resources, embedded, cloud

### monitor — Monitor
- aka: system monitor, fault monitor, dedicated monitoring component, external watchdog component
- kind: tactic
- what: A dedicated component monitors the health of other parts of the system (processors, processes, I/O, memory) and coordinates the other fault-detection tactics.
- problem: Faults must be observed by some part of the system before any repair can begin; a system needs a designated observer to detect failures or congestion, e.g. denial-of-service conditions.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:availability, bck-cat:detect-faults, fault-tolerance, availability, ops

### non-stop-forwarding — Non-Stop Forwarding
- aka: NSF, graceful restart
- kind: tactic
- what: Split functionality into a control/management plane and a data plane so that when the control plane fails, the data plane keeps forwarding along known routes while routing information is rebuilt and validated.
- problem: In router-like systems, supervisory failure should not stop the ongoing data-moving work; the concept originates in router design.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:availability, bck-cat:recover-reintroduction, networking

### nonrepudiation — Nonrepudiation
- aka: non-repudiation
- kind: tactic
- what: Guarantee that the sender of a message cannot later deny sending it and the receiver cannot deny receiving it, via some combination of digital signatures and trusted third-party certification.
- problem: Transactions between mutually distrustful parties need binding evidence of send and receipt.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:security, bck-cat:recover-from-attacks, security

### orchestrate — Orchestrate
- aka: orchestration (tactic), orchestrator-based coordination, orchestration-based saga
- kind: tactic
- what: Introduce a control mechanism (e.g. an orchestration engine or workflow controller) that coordinates, sequences, and invokes otherwise independent services so they work together.
- problem: Independently developed services have no shared control flow; centralizing coordination keeps the integration logic out of the services themselves.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:integrability, bck-cat:coordinate, distributed, enterprise, workflow

### package-dependencies — Package Dependencies
- aka: dependency bundling, containerize dependencies
- kind: tactic
- what: Package an element together with its dependencies (libraries, OS version, utility containers) — via containers, pods, or virtual machines — so they deploy together and dependency versions stay consistent from development to production.
- problem: An element that behaves correctly in development can fail in production when the surrounding dependency versions differ.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:deployability, bck-cat:manage-deployed-system, devops, cloud

### parameter-fence — Parameter Fence
- aka: memory fence pattern (0xDEADBEEF guard)
- kind: tactic
- what: Place a known data pattern immediately after any variable-length parameters of an object so that overwrites of that memory can be detected at runtime.
- problem: Buffer overruns into memory allocated for variable-length parameters are otherwise silent until they corrupt unrelated state.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:availability, bck-cat:detect-faults, borderline — Reads as an implementation-level guard mechanism (kin to design-realm canaries/guard bytes), but bck names it explicitly as an availability sub-tactic; kept per over-inclusion rule.

### parameter-typing — Parameter Typing
- aka: TLV message typing
- kind: tactic
- what: Use a base class defining functions to add, find, and iterate over type-length-value (TLV) message parameters so that sender and receiver agree on content types and disagreements are detected.
- problem: Untyped message payloads let sender and receiver silently disagree about the meaning of bytes on the wire.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:availability, bck-cat:detect-faults, borderline — Implementation-flavored like parameter fence, but named as an availability sub-tactic in bck; kept per over-inclusion rule.

### pause-resume — Pause/Resume
- aka: suspend and resume
- kind: tactic
- what: Let users pause and later resume long-running operations (e.g. large downloads), temporarily freeing resources for reallocation to other tasks.
- problem: Long-running operations monopolize resources and user attention; suspension without loss of progress restores control to the user.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:usability, bck-cat:support-user-initiative, ui

### ping-echo — Ping/Echo
- aka: —
- kind: tactic
- what: Nodes exchange asynchronous request/response message pairs to determine reachability and round-trip delay, with a time threshold before the pinged component is declared failed.
- problem: A monitor must determine whether a remote component is alive and reachable over a network path, and how long the path takes.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:availability, bck-cat:detect-faults, distributed, fault-tolerance

### predictive-model — Predictive Model
- aka: fault prediction
- kind: tactic
- what: Combine a model with monitoring to predict, from operational metrics (session establishment rates, threshold crossings, process-state and queue-length statistics), that a fault or unsafe condition is approaching, and take corrective action early.
- problem: Waiting for faults to occur before reacting is too late for high-availability and safety-critical operation; early warning enables preemptive correction.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:availability, qa:safety, bck-cat:prevent-faults, bck-cat:unsafe-state-avoidance

### prioritize-events — Prioritize Events
- aka: event prioritization
- kind: tactic
- what: Impose a priority scheme ordering events by importance of servicing them, so that under resource pressure low-priority events may be ignored at minimal cost.
- problem: Not all events are equally important (a fire alarm vs. a room-temperature notice); treating them uniformly wastes resources on the unimportant under load.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:performance, qa:energy-efficiency, bck-cat:control-resource-demand, real-time

### queue-based-load-leveling — Queue-Based Load Leveling
- aka: load leveling queue, queue as inter-service buffer
- kind: tactic
- what: A queue is placed between producers and a service so bursts are absorbed by the queue and the service consumes at its sustainable rate.
- problem: Intermittent heavy load overwhelms downstream services provisioned for average demand; the buffer converts bursts into throughput-bounded work.
- named-in: corpus:azurepatterns — Cloud Design Patterns: Queue-Based Load Leveling - Azure Architecture Center (living)
- tags: distributed, cloud, messaging, qa:availability, qa:performance, availability

### reconfiguration — Reconfiguration
- aka: logical remapping
- kind: tactic
- what: Recover from failure by reassigning responsibilities — remapping the logical architecture onto the (possibly limited) resources or components still functioning — while preserving as much functionality as possible.
- problem: After failures the remaining resources differ from the planned deployment; the system must keep operating on what is left, possibly combined with degradation.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:availability, qa:safety, bck-cat:recover-preparation-and-repair, bck-cat:safety-recovery, fault-tolerance

### record-playback — Record/Playback
- aka: capture/replay
- kind: tactic
- what: Record information as it crosses interfaces and use the recorded state to 'play the system back', recreating the fault-inducing state as input to further tests.
- problem: The state that causes a failure is often hard to recreate manually; capturing it at interfaces makes failures reproducible, including in nondeterministic systems.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:testability, bck-cat:control-and-observe-system-state

### redistribute-responsibilities — Redistribute Responsibilities
- aka: increase semantic coherence (3rd ed name)
- kind: tactic
- what: Move similar responsibilities scattered across several modules into one module (existing or new), guided by change scenarios showing which responsibilities move together.
- problem: When one likely change touches many modules, or a module contains parts untouched by any scenario, responsibilities are misallocated and change cost multiplies.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:modifiability, bck-cat:increase-cohesion

### reduce-computational-overhead — Reduce Computational Overhead
- aka: reduce indirection, co-locate communicating resources, periodic cleaning
- kind: tactic
- what: Reduce the work spent per event by removing costly indirection (while ideally preserving encapsulation through code optimization or proxy-established direct communication), co-locating communicating components (same processor, same runtime, same rack), and periodically cleaning inefficient-grown resources such as hash tables and virtual memory maps.
- problem: Intermediaries and separation of concerns — valuable for modifiability — add per-event processing and communication cost; this is the classic modifiability/performance trade-off.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:performance, qa:energy-efficiency, bck-cat:control-resource-demand

### reduce-usage — Reduce Usage
- aka: device power reduction, consolidation
- kind: tactic
- what: Reduce energy use by device-level actions (lower refresh rate, dim display), removing or deactivating unneeded resources (spin down disks, power off CPUs/servers, reduce clock rate), consolidating VMs onto fewer physical servers, or offloading computation to the cloud.
- problem: Resources kept powered beyond demand waste energy; usage must track need.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:energy-efficiency, bck-cat:allocate-resources, embedded, mobile, cloud

### redundant-spare — Redundant Spare
- aka: active redundancy (hot spare), passive redundancy (warm spare), cold spare, protection group, Redundancy, spatial/temporal/informational redundancy, active/passive redundancy, redundant channel structures
- kind: tactic
- what: Configure one or more spare components that can step in and take over when an active component fails; hot/warm/cold variants differ in how current the spare's state is at takeover.
- problem: A failed active component must be replaced quickly to keep the service available; the trade-off is between resource cost of keeping spares synchronized and recovery time.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:availability, bck-cat:recover-preparation-and-repair, fault-tolerance, distributed, availability, safety

### removal-from-service — Removal from Service
- aka: software rejuvenation, therapeutic reboot
- kind: tactic
- what: Temporarily place a system component out of service and reset it to scrub latent faults (memory leaks, fragmentation, soft errors) before they accumulate into failures.
- problem: Latent faults accumulate during long operation; proactive resets prevent them from ever affecting service.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:availability, bck-cat:prevent-faults, fault-tolerance

### repair-state — Repair State
- aka: state correction
- kind: tactic
- what: Repair an erroneous state — effectively enlarging the set of states the component handles competently — and continue execution, e.g. lane-keeping assist steering a drifting vehicle back between the lane lines.
- problem: Aborting or degrading is not always acceptable; some erroneous states can be actively corrected in place, though this is unsuited to recovering from unanticipated faults.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:safety, bck-cat:safety-recovery, safety-critical

### restrict-communication-paths — Restrict Communication Paths
- aka: limit communication paths
- kind: tactic
- what: Restrict the set of elements with which a given element can communicate, so the number of potential interaction points that must be understood and integrated stays small.
- problem: Unrestricted many-to-many communication makes the integration surface of each element grow with the system; deliberate path restriction contains it.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:integrability, bck-cat:limit-dependencies

### restrict-dependencies — Restrict Dependencies
- aka: limit dependencies, visibility restriction
- kind: tactic
- what: Restrict which modules a given module may interact with or depend on, in practice via interface visibility and authorization; seen in layered architectures (a layer may use only lower layers) and wrappers (outsiders see only the wrapper).
- problem: Unconstrained dependency graphs let changes ripple arbitrarily; restricting the allowed edges bounds the ripple. Sibling of the integrability tactic Restrict Communication Paths, kept separate as bck names both.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:modifiability, bck-cat:reduce-coupling

### restrict-login — Restrict Login
- aka: account lockout, login throttling
- kind: tactic
- what: Limit access from a computer after repeated failed login attempts to an account, typically for a bounded period, sometimes doubling the lockout after each further failure.
- problem: Repeated failed logins signal credential-guessing attacks, but legitimate users also mistype; time-bounded lockouts balance the two.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:security, bck-cat:react-to-attacks, security

### retry — Retry
- aka: bounded retry
- kind: tactic
- what: Assume the fault that caused a failure is transient and retry the operation, with a limit on the number of attempts before declaring a permanent failure.
- problem: In networks and server farms transient failures are expected and common; treating every failure as permanent wastes the chance of cheap recovery.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:availability, bck-cat:recover-preparation-and-repair, distributed, same-name:design-realm

### revoke-access — Revoke Access
- aka: emergency access restriction
- kind: tactic
- what: When an attack is believed to be underway, severely limit access to sensitive resources — even for normally legitimate users — until the threat is removed.
- problem: During an active compromise, normal access rights become an attack vector; temporary revocation trades usability for containment.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:security, bck-cat:react-to-attacks, security

### rollback-deployment — Rollback (Deployment)
- aka: deployment rollback, revert deployment
- kind: tactic
- what: Revert a defective or disappointing deployment to its prior state, tracking or being able to reverse the coordinated updates to multiple services and their data, ideally fully automatically.
- problem: A deployment may involve many coordinated service and data updates; discovering a defect after release requires undoing all of them safely. Distinct mechanism from the availability Rollback tactic, which reverts runtime state to a checkpoint.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:deployability, bck-cat:manage-deployment-pipeline, devops

### rollback-tactic — Rollback
- aka: backward recovery, rollback line
- kind: tactic
- what: On detecting a failure, revert the system to a previously saved known-good state (the rollback line), captured as checkpoints, and resume execution from there.
- problem: A failure can leave state corrupted; recovery requires a consistent earlier state to return to, often combined with transactions and redundant spares.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:availability, qa:safety, bck-cat:recover-preparation-and-repair, bck-cat:safety-recovery, fault-tolerance, same-name:design-realm

### sanity-checking — Sanity Checking
- aka: reasonableness check
- kind: tactic
- what: Check the validity or reasonableness of a component's specific operations or outputs, typically at interfaces, based on knowledge of the internal design, system state, or the nature of the information.
- problem: A component can produce syntactically valid but semantically implausible results; examining specific information flows catches such faults early.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:availability, qa:safety, bck-cat:detect-faults

### scale-rollouts — Scale Rollouts
- aka: gradual rollout, incremental rollout
- kind: tactic
- what: Deploy a new version of a service gradually to controlled subsets of the user population rather than to everyone at once, monitoring effects and rolling back if needed; blue/green deployment and rolling upgrade are pattern realizations.
- problem: Deploying a defective service to all users maximizes damage; incremental exposure requires an architectural mechanism outside the service that routes each user's requests to the new or old version.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:deployability, bck-cat:manage-deployment-pipeline, devops

### schedule-resources — Schedule Resources
- aka: scheduling policy selection
- kind: tactic
- what: When resources (processors, buffers, networks) are contended, choose and apply a scheduling policy — priority assignment plus dispatching, e.g. FIFO, fixed-priority (semantic importance, deadline-monotonic, rate-monotonic), dynamic-priority (round-robin, EDF, least-slack-first), or static/cyclic-executive scheduling — matched to each resource's usage characteristics; in the energy realm, schedule work onto the most energy-efficient resources under task constraints.
- problem: Contention forces choices among competing criteria — optimal use, importance, latency, throughput, starvation-freedom — and the chosen policy determines which are met.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:performance, qa:energy-efficiency, bck-cat:manage-resources, bck-cat:allocate-resources, real-time

### script-deployment-commands — Script Deployment Commands
- aka: scripted deployment, deployment-as-code
- kind: tactic
- what: Capture the many precisely ordered, coordinated deployment steps as scripts that are treated like code — documented, reviewed, tested, version-controlled — and executed by a script engine.
- problem: Complex manual deployments are slow and error-prone; automation removes human error and makes deployments repeatable.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:deployability, bck-cat:manage-deployment-pipeline, devops

### self-test — Self-Test
- aka: self-check
- kind: tactic
- what: A component or subsystem runs procedures to test itself for correct operation, initiated by itself or invoked periodically by the system monitor.
- problem: Latent faults in a component may not manifest during normal operation until they matter; proactive self-exercise surfaces them early.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:availability, bck-cat:detect-faults, embedded, same-name:design-realm

### separate-entities — Separate Entities
- aka: physical separation, air gap, data segregation
- kind: tactic
- what: Limit the scope of an attack by separating entities — physical separation onto different servers/networks, virtual machines, air gaps, and keeping sensitive data apart from non-sensitive data.
- problem: Co-located entities share fate under attack; separation prevents access to one from becoming access to all.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:security, bck-cat:resist-attacks, security

### shadow — Shadow
- aka: shadow mode, shadow operation
- kind: tactic
- what: Run a previously failed or freshly upgraded component in shadow mode for a predefined period, monitoring its behavior and letting it repopulate state before restoring it to an active role.
- problem: Reintroducing a repaired component directly into active service risks reintroducing the fault; its correctness must be demonstrated first.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:availability, bck-cat:recover-reintroduction, fault-tolerance

### software-upgrade — Software Upgrade
- aka: function patch, class patch, in-service software upgrade (ISSU), hitless upgrade
- kind: tactic
- what: Upgrade executable code images in service, without affecting the running service, via function patches, class patches, or hitless in-service software upgrade built on redundant spares.
- problem: Deploying fixes and features to systems that must not stop requires replacing code while it runs.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:availability, bck-cat:recover-preparation-and-repair

### specialized-interfaces — Specialized Interfaces
- aka: test interfaces, set/get/report/reset methods
- kind: tactic
- what: Provide dedicated test interfaces — set/get methods for important variables, report methods returning full object state, reset methods forcing a given internal state, verbose/logging/instrumentation switches — clearly separated from functional interfaces so they can be removed.
- problem: Testers need to control and capture component state beyond normal inputs and outputs; but shipping code different from tested code is problematic in performance- and safety-critical systems.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:testability, bck-cat:control-and-observe-system-state

### split-module — Split Module
- aka: module refactoring by responsibility
- kind: tactic
- what: Refactor a module whose responsibilities are not cohesive into several modules that are each individually cohesive — not an arbitrary bisection, but a principled separation of responsibilities.
- problem: When one module carries unrelated responsibilities, changes to any of them cost as much as changing all; splitting reduces the average cost of future change.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:modifiability, bck-cat:increase-cohesion

### state-resynchronization — State Resynchronization
- aka: state resync
- kind: tactic
- what: Restore and verify state consistency between active and standby components, either naturally under active redundancy (with periodic comparison via checksums or message digests) or by periodic state transfer/checkpointing under passive redundancy.
- problem: A reintroduced or standby component must have state consistent with the active one before it can safely take over.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:availability, bck-cat:recover-reintroduction, distributed, fault-tolerance

### static-classification — Static Classification
- aka: static energy model
- kind: tactic
- what: Estimate energy consumption by cataloging the computing resources used and their known static energy characteristics (from benchmarks or manufacturer specifications), e.g. energy per disk read.
- problem: Real-time energy data collection is sometimes impossible (e.g. on external cloud services); reference models substitute for measurement.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:energy-efficiency, bck-cat:monitor-resources

### substitution — Substitution
- aka: hardware substitution for software safety functions
- kind: tactic
- what: Replace potentially hazardous software design features with protection mechanisms — typically hardware devices such as watchdogs, monitors, and interlocks — that provide and control their own resources.
- problem: Software versions of protection mechanisms can be starved of resources by the very failures they guard against; substitution pays off when the protected function is relatively simple.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:safety, bck-cat:unsafe-state-avoidance, embedded, safety-critical

### tailor-interface — Tailor Interface
- aka: interface tailoring
- kind: tactic
- what: Add capabilities to or hide capabilities of an interface without changing the underlying implementation — e.g. adding buffering, data transformation, or masking functions (adapter/decorator-like mechanisms at the architectural boundary).
- problem: Independently developed components rarely present exactly the interfaces their integrators need; adapting at the interface avoids modifying either side.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:integrability, bck-cat:adapt

### throttling-service-admission-control — Throttling (service admission control)
- aka: rate limiting (service-level), admission control
- kind: tactic
- what: A service enforces consumption limits per tenant/client and degrades or rejects excess requests to protect its SLA under load.
- problem: Autoscaling has limits and lag; explicit admission control keeps the system functional when demand exceeds capacity.
- named-in: corpus:azurepatterns — Cloud Design Patterns: Throttling - Azure Architecture Center (living)
- tags: distributed, cloud, qa:performance, qa:availability, same-name-two-realms, borderline — Same-name-two-realms: the design realm carries throttle/rate-limiter mechanisms (token bucket, sliding window); this is the system-boundary policy structure.

### timeout-tactic — Timeout
- aka: time-constraint exception
- kind: tactic
- what: A component raises an exception when it detects that it or another component has failed to meet its timing constraints, e.g. when a response takes longer than a set bound.
- problem: Hung or slow components would otherwise block their clients indefinitely; violated time constraints must become detectable events.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:availability, qa:safety, bck-cat:detect-faults, same-name:design-realm

### timestamp — Timestamp
- aka: sequence numbering (variant)
- kind: tactic
- what: Assign the state of a local clock (or a sequence number) to events immediately after they occur so that incorrect event ordering can be detected.
- problem: In distributed message-passing systems, events may arrive or be processed out of order and local clocks may be inconsistent across processors.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:availability, qa:safety, bck-cat:detect-faults, distributed

### transactions — Transactions
- aka: ACID semantics, two-phase commit (realization)
- kind: tactic
- what: Use transaction semantics (ACID properties, most commonly implemented via two-phase commit) to bundle state updates exchanged between distributed components so they are atomic, consistent, isolated, and durable.
- problem: Race conditions from concurrent updates to the same data, and partial failures mid-update, would otherwise leave inconsistent state.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:availability, bck-cat:prevent-faults, distributed

### undo — Undo
- aka: multi-level undo
- kind: tactic
- what: Maintain sufficient information about earlier system state — snapshots/checkpoints or sets of reversible operations, with detailed change records where operations are not invertible — to restore it on user request, in single- or multi-level variants.
- problem: Users make mistakes; recovery requires the system to have planned for state restoration, since some operations (mass replace, or anything with external effects) cannot be reversed naively or at all.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:usability, bck-cat:support-user-initiative, ui

### use-an-intermediary — Use an Intermediary
- aka: insert intermediary, broker/bus (realizations)
- kind: tactic
- what: Break a dependency between elements by interposing an intermediary (broker, publish-subscribe bus, name server, etc.) that manages the interaction on their behalf.
- problem: Direct dependencies between many elements multiply coupling and integration effort; an intermediary centralizes and standardizes the interaction, at some performance cost.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:integrability, qa:modifiability, bck-cat:limit-dependencies, bck-cat:reduce-coupling

### validate-input — Validate Input
- aka: input sanitization, input filtering
- kind: tactic
- what: Sanitize and check input as it is received — filtering, canonicalization, and cleansing, typically via a security framework or validation classes — as an early line of defense.
- problem: Uninspected input is the vector for SQL injection, cross-site scripting, and kin; validation at the boundary stops malicious payloads before they reach interpreters.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:security, bck-cat:resist-attacks, security, web

### verify-message-integrity — Verify Message Integrity
- aka: checksum verification, hash verification
- kind: tactic
- what: Use checksums or hash values to verify the integrity of messages, resource files, deployment files, and configuration files, maintaining the redundant verification information separately.
- problem: Tampered or corrupted messages and artifacts must be detectable; even small changes must produce large, visible differences in the verification value.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:security, bck-cat:detect-attacks, security

### voting — Voting
- aka: voter
- kind: tactic
- what: Compare computational results from multiple sources that should produce the same result and decide which to use when they differ, using simple, heavily reviewed voting logic.
- problem: A single component's output cannot be trusted in the presence of hardware or software faults; multiple evaluable sources plus a highly reliable voter allow faulty results to be outvoted.
- named-in: corpus:bck — Software Architecture in Practice, 4th ed. — Bass, Clements & Kazman (2021)
- tags: qa:availability, bck-cat:detect-faults, fault-tolerance


## Connector types — `connector` (14)

### adaptor-connector — Adaptor Connector
- aka: adaptor (connector type), adapter connector, wrapper connector
- kind: connector
- what: A connector that converts between mismatched interaction policies, interfaces, or data formats of components not designed to interoperate - wrappers, transformers, and protocol converters.
- problem: How to compose heterogeneous or independently developed components whose assumptions disagree; conversion cost and semantic fidelity of the mapping are the central forces.
- named-in: corpus:mehtaconnectors — Towards a Taxonomy of Software Connectors - Mehta, Medvidovic & Phadke (2000)
- tags: borderline — Same NAME family as the design-realm GoF Adapter pattern; the connector type is the architecture-level interaction mediator - both kept per same-name-two-realms rule.

### arbitrator-connector — Arbitrator Connector
- aka: arbitrator (connector type), arbitration connector
- kind: connector
- what: A connector that resolves conflicts and redirects control among components with conflicting needs, providing concurrency control (locks, semaphores), scheduling, load balancing, and fault-handling negotiation.
- problem: How to coordinate components that contend for shared resources or must agree despite failures; centralizes the coordination policy in the connector instead of scattering it through components.
- named-in: corpus:mehtaconnectors — Towards a Taxonomy of Software Connectors - Mehta, Medvidovic & Phadke (2000)
- tags: concurrency

### autosar-virtual-function-bus-rte — AUTOSAR Virtual Function Bus / RTE
- aka: VFB, runtime environment, RTE, Run-Time Environment (RTE)
- kind: connector
- what: A communication abstraction in which software components interact through typed ports on a virtual bus, generated per-ECU as the runtime environment (RTE) that maps port communication to intra-ECU calls or network signals.
- problem: Component-to-component communication must be independent of deployment; the VFB lets components be designed against logical connections and relocated across ECUs, with the generated RTE realizing each mapping.
- named-in: corpus:autosarclassic — AUTOSAR Classic Platform - Layered Software Architecture - AUTOSAR (living)
- tags: embedded, automotive, distributed, middleware

### data-access-connector — Data Access Connector
- aka: data access (connector type), shared-data connector, query connector
- kind: connector
- what: A connector through which a component reads or writes data maintained by a data store or another component, covering repository access, database queries, and accessor operations, often with translation/conversion.
- problem: How to mediate interaction that flows through persistent or shared state rather than control transfer; transactionality, locality, and format conversion are the governing forces.
- named-in: corpus:mehtaconnectors — Towards a Taxonomy of Software Connectors - Mehta, Medvidovic & Phadke (2000)
- tags: —

### distributor-connector — Distributor Connector
- aka: distributor (connector type), routing connector
- kind: connector
- what: A connector that identifies interaction paths and routes communication among components - naming, registration/lookup, and delivery services such as DNS-style naming, routing, and multicast distribution.
- problem: How interacting parties find each other and how messages reach them across a topology; never used alone, it composes with procedure-call or stream connectors to form RPCs and distributed messaging.
- named-in: corpus:mehtaconnectors — Towards a Taxonomy of Software Connectors - Mehta, Medvidovic & Phadke (2000)
- tags: distributed, networking

### enterprise-service-bus — Enterprise Service Bus
- aka: ESB
- kind: connector
- what: A shared messaging backbone providing routing, transformation, protocol bridging, and orchestration between enterprise applications.
- problem: Point-to-point integration among N systems explodes to N^2 adapters; a mediating bus centralizes translation and routing (and becomes its own coupling point).
- named-in: corpus:chappellesb — Enterprise Service Bus - Chappell (2004)
- tags: enterprise, messaging, integration

### event-connector — Event Connector
- aka: event (connector type), event notification connector
- kind: connector
- what: A connector that transfers control and data by delivering occurrences (events) from producers to registered observers, with dimensions for cardinality, delivery guarantees, synchronicity, and notification mode.
- problem: How to interact without the initiator knowing or waiting on the recipients; decouples identity and time, but delivery ordering, loss, and causality become connector-level design decisions.
- named-in: corpus:mehtaconnectors — Towards a Taxonomy of Software Connectors - Mehta, Medvidovic & Phadke (2000)
- tags: —

### linkage-connector — Linkage Connector
- aka: linkage (connector type), binding connector
- kind: connector
- what: A connector that ties system elements together by establishing and enforcing associations - name bindings, imports/exports, and compile- or load-time linking - enabling other connectors to act at runtime.
- problem: How components come to be composed at all: the facilitation of later interaction; linkage decisions (static vs dynamic, granularity of binding) fix how late a system can be reconfigured.
- named-in: corpus:mehtaconnectors — Towards a Taxonomy of Software Connectors - Mehta, Medvidovic & Phadke (2000)
- tags: —

### message-channel — Message Channel
- aka: messaging channel, virtual pipe between applications
- kind: connector
- what: A named logical conduit of the messaging system that senders write messages to and receivers read from.
- problem: Applications need addressable, decoupled conduits rather than direct connections to each other.
- named-in: corpus:hohpe — Enterprise Integration Patterns - Hohpe & Woolf (2003)
- tags: messaging

### procedure-call-connector — Procedure Call Connector
- aka: procedure call (connector type), method invocation connector, RPC (distributed composite variant)
- kind: connector
- what: A connector that transfers control and data between components through invocation with parameters and (usually) a return, spanning local calls, method invocations, callbacks, and system calls.
- problem: How to couple components when the caller needs the callee's result before proceeding; the dominant, best-understood interaction primitive, but synchronous and identity-coupled by default.
- named-in: corpus:mehtaconnectors — Towards a Taxonomy of Software Connectors - Mehta, Medvidovic & Phadke (2000)
- tags: —

### secure-channel — Secure Channel
- aka: secure pipe, TLS/mTLS connection, encrypted transport link, Secure Pipe (Core Security Patterns), TLS channel, encrypted transport connector
- kind: connector
- what: A connector type in which communication between components crosses an authenticated, encrypted transport so confidentiality and integrity hold over untrusted networks.
- problem: Data in transit over shared networks can be read and altered; making the channel itself cryptographically protected frees endpoints from trusting the path.
- named-in: corpus:schumacher — Security Patterns: Integrating Security and Systems Engineering - Schumacher et al. (2006)
- tags: security, network, distributed, qa:security, networking

### stream-connector — Stream Connector
- aka: stream (connector type), data stream connector
- kind: connector
- what: A connector that transfers sequences of data between autonomous processes, covering pipes, sockets, and other bounded/unbounded, buffered, structured or raw data flows.
- problem: How to move large or continuous data between concurrently executing components; buffering, throughput, ordering, and blocking behavior are the connector's defining choices.
- named-in: corpus:mehtaconnectors — Towards a Taxonomy of Software Connectors - Mehta, Medvidovic & Phadke (2000)
- tags: —

### temporal-firewall — Temporal Firewall
- aka: temporally firewalled interface, state-message interface
- kind: connector
- what: A unidirectional, time-controlled shared-memory interface between subsystems: the sender deposits temporally accurate state data that the receiver reads at predefined instants, with no control signals crossing the interface in either direction.
- problem: Control-flow coupling (interrupts, handshakes) lets timing faults propagate between subsystems; a data-only interface with a priori known access instants blocks error propagation and makes each side independently analyzable.
- named-in: corpus:kopetz — Real-Time Systems: Design Principles for Distributed Embedded Applications - Kopetz & Steiner (2022)
- tags: embedded, real-time, safety-critical, distributed

### time-triggered-bus — Time-Triggered Bus
- aka: TDMA bus schedule, TTP/C bus, FlexRay static segment, time-division communication schedule
- kind: connector
- what: A broadcast communication channel whose access is governed by a static TDMA schedule: each node owns pre-assigned slots in a cyclic schedule known to all nodes, so message timing is known a priori.
- problem: Contention-based buses make message latency load-dependent and unbounded in the worst case; a static slot schedule gives constant, verifiable latency and doubles as a fault-isolation mechanism (babbling nodes are cut off by bus guardians).
- named-in: corpus:kopetzbauer — The Time-Triggered Architecture - Kopetz & Bauer (2003)
- tags: embedded, real-time, distributed, networking


## Deployment, release & scaling structures — `deployment` (26)

### activator — Activator
- aka: on-demand activation, inetd-style activation, activate-on-request
- kind: deployment
- what: A component that launches services or server processes on demand when a request arrives and can shut them down when idle, instead of keeping every service resident at all times.
- problem: Keeping rarely used services running wastes memory and startup capacity, but clients must still be able to reach them at any time; an activation intermediary buys resource economy at the cost of first-request latency.
- named-in: corpus:posa4 — Pattern-Oriented Software Architecture Vol. 4: A Pattern Language for Distributed Computing - Buschmann, Henney, Schmidt (2007)
- tags: distributed, os, operations, qa:resource-efficiency, middleware, deployment

### adapter-container — Adapter (container)
- aka: adapter pattern (container-level)
- kind: deployment
- what: A sidecar variant that presents a standardized interface (e.g., uniform metrics/log format) over a heterogeneous application to the rest of the system.
- problem: Uniform monitoring/management across services built differently, without modifying each service.
- named-in: corpus:burnshotcloud — Design Patterns for Container-based Distributed Systems - Burns & Oppenheimer (HotCloud 2016)
- tags: cloud, deployment, containers, same-name-two-realms, borderline — Shares the GoF Adapter name; kept separate: this is a deployment-unit structure, not an object-interface mechanism.

### ambassador — Ambassador
- aka: ambassador container, ambassador proxy
- kind: deployment
- what: A sidecar variant that proxies the application's outbound connections to the outside world, hiding discovery, sharding, or protocol detail.
- problem: Let a component talk to remote dependencies as if local and unsharded; the ambassador absorbs routing/resilience client logic.
- named-in: corpus:azurepatterns — Cloud Design Patterns - Microsoft Azure Architecture Center
- tags: cloud, deployment, containers, microservices, networking

### auto-scaling — Auto-Scaling
- aka: autoscaling, elastic scaling, horizontal pod autoscaling, scale-out/scale-in policy
- kind: deployment
- what: The instance pool grows and shrinks automatically, driven by metrics or schedules evaluated against scaling policies.
- problem: Static provisioning wastes capacity at trough and fails at peak; policy-driven elasticity matches deployed capacity to demand without operator action.
- named-in: corpus:azureautoscale — Autoscaling guidance - Microsoft Azure Architecture Center (living); also AWS Auto Scaling documentation
- tags: cloud, distributed, qa:scalability, operability

### blue-green-deployment — Blue-Green Deployment
- aka: blue/green release, red-black deployment (Netflix), A/B environment switch
- kind: deployment
- what: Two identical production environments are maintained and releases go live by switching traffic from the active (blue) to the newly deployed (green) environment.
- problem: Releasing in place risks downtime and slow rollback; keeping a fully deployed standby environment makes cutover and rollback a routing switch instead of a redeploy.
- named-in: corpus:contdeliv — Continuous Delivery - Humble & Farley (2010); also BlueGreenDeployment - Fowler bliki (2010)
- tags: distributed, web, operability, qa:deployability

### bootloader-application-split — Bootloader-Application Split
- aka: staged boot architecture, boot architecture, bootloader + app images, two-stage boot
- kind: deployment
- what: Partitioning firmware into a small, rarely-changed bootloader image and one or more application images in separate flash regions, with the bootloader validating, selecting, updating, and jumping to the application.
- problem: Field-updatable devices must survive a failed or interrupted update; keeping an immutable boot stage that can verify images and fall back (golden image, A/B banks) makes the update path recoverable and the root of trust small.
- named-in: corpus:zerotomain — From Zero to main() series - Memfault Interrupt (2019)
- tags: embedded, deployment, security

### bootloader-boot-stage-architecture — Bootloader (boot-stage architecture)
- aka: boot loader, multi-stage boot, MCUboot-style secure bootloader
- kind: deployment
- what: A dedicated boot-stage program that initializes the platform, selects/validates an application image, and hands off execution to it.
- problem: Field update, image validation and bring-up need a stage that is independent of - and can replace - the application image.
- named-in: corpus:zerotomain — From Zero to main() series - Memfault (2019)
- tags: embedded, os, security

### canary-release — Canary Release
- aka: canary deployment, canarying, canary releasing, incremental rollout to a user subset
- kind: deployment
- what: A new version is deployed to a small slice of production servers or users and observed before the rollout is widened to the whole fleet.
- problem: Full-fleet releases expose every user to an undetected defect at once; a canary bounds the blast radius and turns release into a monitored experiment.
- named-in: corpus:contdeliv — Continuous Delivery - Humble & Farley (2010); also Site Reliability Engineering - Beyer et al. (2016)
- tags: distributed, web, operability, qa:deployability

### cell-based-architecture — Cell-Based Architecture
- aka: cellular architecture, cells
- kind: deployment
- what: Workload deployed as multiple isolated, self-sufficient instances (cells), each serving a partition of requests, with a thin router directing traffic to cells.
- problem: Reduce blast radius: a failure or bad deployment is contained to one cell's share of traffic; fault-isolation bulkheads at workload level.
- named-in: corpus:awscellbased — Reducing the Scope of Impact with Cell-Based Architecture - AWS Well-Architected (2023)
- tags: cloud, deployment, qa:availability

### component-container — Container
- aka: component container, application container, EJB/CCM-style container, managed execution environment, Container (component container), EJB/CCM container, managed component environment
- kind: deployment
- what: An execution environment that hosts application components and transparently provides them the technical services they need - lifecycle, transactions, security, persistence, resource access - via contracts the components declare.
- problem: Domain components should not each reimplement cross-cutting runtime services; hosting them in a managing container buys uniform infrastructure and deploy-time configuration at the cost of conforming to the container's component model. Distinct from OS-level containers (Docker-style isolation), which are a separate deployment element.
- named-in: corpus:posa4 — Pattern-Oriented Software Architecture Vol. 4: A Pattern Language for Distributed Computing - Buschmann, Henney, Schmidt (2007)
- tags: enterprise, distributed, middleware

### compute-resource-consolidation — Compute Resource Consolidation
- aka: task packing into shared units
- kind: deployment
- what: Multiple tasks or operations are consolidated into shared compute units to raise utilization and cut cost.
- problem: One deployment unit per small task wastes allocated capacity; packing trades isolation for density.
- named-in: corpus:azurepatterns — Cloud Design Patterns - Microsoft Azure Architecture Center
- tags: cloud, deployment

### deployment-pipeline — Deployment Pipeline
- aka: continuous delivery pipeline, build pipeline, staged release pipeline, path to production
- kind: deployment
- what: An automated, staged structure through which every change flows from commit to production - build, automated test stages, and deployment stages, each gating promotion of the same artifact.
- problem: Manual, ad-hoc release paths make delivery slow and unrepeatable; a single automated pipeline makes the route to production an inspectable, versioned system structure.
- named-in: corpus:contdeliv — Continuous Delivery - Humble & Farley (2010), ch. 5 'Anatomy of the Deployment Pipeline'
- tags: operability, qa:deployability, borderline — Practice-adjacent (CI/CD is pass-7 territory), but the pipeline itself is a named, recurring structure - stages, gates, artifact promotion - not just a practice; included as the structural core of the CD literature.

### deployment-stamps — Deployment Stamps
- aka: stamps, scale units, pods (Azure usage), cells / cell-based architecture, geode (geographical node variant)
- kind: deployment
- what: The full solution is replicated as identical scale-unit deployments (stamps), each hosting a subset of tenants/load, with routing in front.
- problem: Scale beyond a single deployment's limits and isolate tenants by adding units instead of growing one deployment.
- named-in: corpus:azurepatterns — Cloud Design Patterns: Deployment Stamps - Azure Architecture Center (living)
- tags: cloud, deployment, qa:scalability, distributed, qa:availability

### external-configuration-store — External Configuration Store
- aka: centralized configuration service
- kind: deployment
- what: Configuration for all application instances is moved to a central external store fetched at startup/run time.
- problem: Per-deployment config files diverge across instances and redeploys; centralization gives one managed source.
- named-in: corpus:azurepatterns — Cloud Design Patterns - Microsoft Azure Architecture Center
- tags: cloud, ops

### feature-flag-driven-release — Feature-Flag-Driven Release
- aka: release toggle, dark launch, decoupling deploy from release, percentage rollout / ring rollout
- kind: deployment
- what: Code ships to production dark behind runtime toggles, and release becomes a configuration act - enabling the flag for cohorts, rings, or percentages - independent of deployment.
- problem: Coupling release to deployment forces long-lived branches and big-bang exposure; runtime toggles let incomplete or risky features ride mainline deploys and be exposed, tested, and killed selectively.
- named-in: corpus:hodgsontoggles — Feature Toggles (aka Feature Flags) - Hodgson (2017); also Continuous Delivery - Humble & Farley (2010)
- tags: web, operability, qa:deployability, borderline — Same-name-two-realms: design realm has feature-flag (the in-code toggle point/router mechanism); this entry is the release-strategy structure built on it. Kept per the same-name rule.

### gatekeeper — Gatekeeper
- aka: validating front host
- kind: deployment
- what: A dedicated hardened host between clients and backends validates and sanitizes all requests, holding no keys or sensitive data itself.
- problem: Exposing application hosts directly widens the attack surface; a minimal broker instance absorbs first contact.
- named-in: corpus:azurepatterns — Cloud Design Patterns - Microsoft Azure Architecture Center
- tags: cloud, security

### geodes — Geodes
- aka: geographical node, geo-distributed active-active nodes
- kind: deployment
- what: Identical active-active deployments distributed across geographic regions, each able to serve any user, backed by globally replicated data.
- problem: Serve a global user base with low regional latency and region-loss tolerance, instead of active-passive DR.
- named-in: corpus:azurepatterns — Cloud Design Patterns: Geodes - Azure Architecture Center (living)
- tags: cloud, deployment, qa:availability, distributed, borderline — Name currency is largely Azure-specific; the structure (geo-distributed active-active units) is real and bridgeable, so kept with the caveat.

### immutable-infrastructure — Immutable Infrastructure
- aka: immutable server, phoenix server, replace-not-patch deployment
- kind: deployment
- what: Deployed servers/images are never modified in place; every change produces a new image that replaces the old instance wholesale.
- problem: In-place patching accumulates configuration drift and snowflake servers; rebuilding from a versioned image makes every environment reproducible and rollback a redeploy of the previous image.
- named-in: corpus:immutableserver — ImmutableServer - Kief Morris (martinfowler.com bliki, 2013); also Infrastructure as Code - Morris (2016)
- tags: cloud, operability, qa:deployability, borderline — Practice-vs-structure judged: kept because it names a deployment structure (versioned images replacing mutable servers), not merely a working habit; the enclosing infrastructure-as-code practice is rejected below.

### load-balancer — Load Balancer
- aka: load-balanced pool, server farm behind a virtual IP, reverse-proxy load balancing, L4/L7 load balancing
- kind: deployment
- what: An intermediary distributes incoming requests across a pool of equivalent service instances, presenting the pool as one logical endpoint.
- problem: A single instance limits capacity and is a single point of failure; a fronting distributor lets capacity scale horizontally and routes around dead instances.
- named-in: corpus:nygard — Release It! - Nygard (2007/2018)
- tags: distributed, web, qa:scalability, qa:availability

### os-container — OS Container
- aka: Linux container, Docker container, containerized deployment unit
- kind: deployment
- what: An OS-level isolated execution unit packaging an application with its dependencies, sharing the host kernel, used as the standard unit of deployment and scheduling.
- problem: Deployable units need environment-independent packaging and fast, dense isolation without full-VM overhead; containers make the deployment topology reproducible and orchestratable.
- named-in: corpus:burnshotcloud — Design Patterns for Container-based Distributed Systems - Burns & Oppenheimer (USENIX HotCloud 2016)
- tags: cloud, deployment

### rolling-deployment — Rolling Deployment
- aka: rolling update, rolling upgrade, in-place incremental update
- kind: deployment
- what: Instances in a load-balanced pool are replaced with the new version a few at a time, keeping the service up while old and new versions briefly coexist.
- problem: Replacing an entire fleet at once requires downtime or double capacity; rolling replacement trades a window of mixed-version operation for zero-downtime upgrades within existing capacity.
- named-in: corpus:k8sdeploy — Kubernetes Documentation - Deployments (RollingUpdate strategy) (living)
- tags: distributed, web, operability, qa:deployability

### scale-cube — Scale Cube
- aka: AKF scale cube, x/y/z-axis scaling, X-axis cloning / Y-axis functional decomposition / Z-axis data partitioning
- kind: deployment
- what: A three-axis model of scaling structures: X - cloning identical instances behind a load balancer, Y - splitting by function/service, Z - partitioning by data/customer subset.
- problem: Systems that only clone hit data and code-complexity limits; naming the three orthogonal scaling structures lets architects combine duplication, decomposition, and sharding deliberately.
- named-in: corpus:abbottfisher — The Art of Scalability - Abbott & Fisher (2009; 2nd ed. 2015)
- tags: distributed, web, qa:scalability, borderline — A named model organizing three scaling structures rather than a single mechanism; included because it is the established name for the trio and each axis is a concrete, bridgeable deployment structure (sharding and functional-split design elements bridge to its axes). Verified live at akfpartners.com this session.

### serverless-function-as-a-service — Serverless / Function-as-a-Service
- aka: FaaS, serverless architecture, BaaS+FaaS, Function-as-a-Service, serverless functions
- kind: deployment
- what: Application logic deployed as provider-managed, event-triggered ephemeral functions (plus managed backend services), with no server capacity owned by the team.
- problem: Eliminate server provisioning and idle cost; scale-to-zero and per-invocation billing, traded against cold starts, execution limits, and provider coupling.
- named-in: corpus:robertsserverless — Serverless Architectures - Roberts (martinfowler.com, 2016)
- tags: cloud, deployment, distributed

### service-mesh — Service Mesh
- aka: —
- kind: deployment
- what: Dedicated infrastructure layer of per-service proxies (data plane) plus a control plane that transparently handles inter-service traffic: routing, retries, mTLS, telemetry.
- problem: Move reliability and security of service-to-service communication out of every application's code into uniform, operable infrastructure.
- named-in: corpus:morganservicemesh — What's a service mesh? And why do I need one? - Morgan (Buoyant, 2017)
- tags: distributed, cloud, deployment

### sidecar — Sidecar
- aka: sidekick container, sidecar container, sidekick pattern
- kind: deployment
- what: A helper process/container co-deployed with an application instance, sharing its lifecycle and local resources to extend it (proxying, logging, config).
- problem: Add cross-cutting capabilities to heterogeneous services without changing their code or language; per-instance co-location keeps latency and fate-sharing local.
- named-in: corpus:azurepatterns — Cloud Design Patterns - Microsoft Azure Architecture Center
- tags: cloud, deployment, containers, microservices

### static-content-hosting — Static Content Hosting
- aka: static assets on storage/CDN
- kind: deployment
- what: Static content is served from dedicated storage/CDN services instead of the application's compute instances.
- problem: Serving immutable assets from application servers wastes expensive compute on cacheable bytes.
- named-in: corpus:azurepatterns — Cloud Design Patterns - Microsoft Azure Architecture Center
- tags: cloud, web


## Reference architectures — `reference-architecture` (10)

### autosar-adaptive-platform — AUTOSAR Adaptive Platform
- aka: ARA, AUTOSAR adaptive architecture, ara::com service-oriented communication
- kind: reference-architecture
- what: The POSIX-based automotive reference architecture for high-performance ECUs: dynamically scheduled applications communicate via service-oriented ara::com middleware (SOME/IP) instead of the Classic platform's static signal routing.
- problem: Autonomous-driving and connectivity functions need dynamic deployment, high compute, and update-over-the-air, which the statically configured Classic platform cannot provide; the Adaptive platform standardizes a service-oriented alternative alongside it.
- named-in: corpus:autosaradaptive — AUTOSAR Adaptive Platform - Explanation of Adaptive and Classic Platform Software Architectural Decisions - AUTOSAR (living)
- tags: embedded, automotive, distributed

### autosar-layered-software-architecture — AUTOSAR Layered Software Architecture
- aka: AUTOSAR Classic layered architecture, MCAL/ECU-abstraction/services layering, basic software (BSW) stack
- kind: reference-architecture
- what: The automotive reference layering for ECU software: application layer above the RTE, above basic software split into services, ECU abstraction, and microcontroller abstraction (MCAL) layers, plus complex device drivers as a sanctioned bypass.
- problem: Automotive software must be portable across ECUs and suppliers; a standardized layer stack with fixed interface contracts decouples application components from hardware and lets OEMs integrate multi-vendor code.
- named-in: corpus:autosarclassic — AUTOSAR Classic Platform - Layered Software Architecture - AUTOSAR (living)
- tags: embedded, automotive, real-time

### data-mesh — Data Mesh
- aka: —
- kind: reference-architecture
- what: Analytical data architecture decentralized into domain-owned data products with self-serve platform and federated governance, instead of one central lake/warehouse.
- problem: Central data teams become bottlenecks and lose domain context at scale; aligns data ownership with domain (bounded-context) boundaries.
- named-in: corpus:datamesh — How to Move Beyond a Monolithic Data Lake to a Distributed Data Mesh - Dehghani (martinfowler.com, 2019)
- tags: data, enterprise, borderline — Organizational/socio-technical as much as structural; kept because it is an established named reference structure and a bridge endpoint for bounded-context-aligned data elements.

### domain-specific-software-architecture — Domain-Specific Software Architecture
- aka: DSSA, domain reference architecture
- kind: reference-architecture
- what: A reference structure specialized to one application domain (e.g. avionics, vehicle management) that fixes the component types, coordination model, and configuration rules that products in that domain instantiate.
- problem: How to exploit deep domain regularities for reuse and generation across a product family, trading generality for the power to derive concrete systems (semi-)automatically from the architecture.
- named-in: corpus:garlanshaw93 — An Introduction to Software Architecture - Garlan & Shaw (1993)
- tags: embedded, product-line

### federated-avionics-architecture — Federated Avionics Architecture
- aka: federated architecture, one function one computer
- kind: reference-architecture
- what: The traditional avionics system structure in which each function runs on its own dedicated computer with private resources, integrated only through inter-box data buses.
- problem: Physical separation gives inherent fault containment and simple per-box certification, at the cost of hardware proliferation; it is the named baseline against which IMA and partitioned architectures are defined.
- named-in: corpus:do297 — DO-297 - Integrated Modular Avionics (IMA) Development Guidance and Certification Considerations - RTCA (2005)
- tags: embedded, avionics, safety-critical, borderline — Named mostly as the contrast concept to IMA; kept because avionics sources name it as an architecture in its own right and dedicated-hardware design elements need a specific bridge endpoint.

### hla-federation — HLA Federation
- aka: High Level Architecture, IEEE 1516 RTI federation, federated simulation
- kind: reference-architecture
- what: Independent simulators (federates) interoperate through a Run-Time Infrastructure under a federation object model and interface specification.
- problem: Heterogeneous simulations must interoperate and be reused across federations without pairwise integration.
- named-in: corpus:ieee1516 — IEEE 1516-2010 - High Level Architecture (HLA)
- tags: simulation, distributed

### integrated-modular-avionics — Integrated Modular Avionics
- aka: IMA, IMA platform architecture
- kind: reference-architecture
- what: A domain reference architecture in which multiple avionics functions, formerly on dedicated boxes, are hosted as partitioned applications on a shared set of common computing modules with standardized interfaces (ARINC 653 APEX) and defined supplier roles.
- problem: Federated one-function-one-computer designs multiply size, weight, power, and spares; IMA consolidates functions onto shared platforms while preserving per-function independence through robust partitioning and incremental certification.
- named-in: corpus:do297 — DO-297 - Integrated Modular Avionics (IMA) Development Guidance and Certification Considerations - RTCA (2005)
- tags: embedded, avionics, safety-critical, real-time

### layered-game-engine-architecture — Layered Game Engine Architecture
- aka: engine runtime layering, platform/core/resources/gameplay layering
- kind: reference-architecture
- what: The canonical layering of a game engine runtime: platform independence layer, core systems, resource management, rendering/physics/audio, gameplay foundations, game-specific code.
- problem: Game engines recur in structure; the reference layering keeps engine subsystems independent of game code and platform.
- named-in: corpus:gregorygea — Game Engine Architecture, 4th ed. - Gregory (2026)
- tags: games

### multi-pass-compiler-pipeline — Multi-Pass Compiler Pipeline
- aka: compilation phases, front-end / middle-end / back-end structure, lexer-parser-analyzer-codegen decomposition
- kind: reference-architecture
- what: The canonical decomposition of a compiler into sequential phases (lexical analysis, parsing, semantic analysis, IR optimization, code generation) over shared intermediate representations.
- problem: Language translation is intractable as one step; the phase structure isolates concerns and enables retargeting front and back ends.
- named-in: corpus:dragonbook — Compilers: Principles, Techniques, and Tools, 2nd ed. - Aho, Lam, Sethi & Ullman (2006)
- tags: languages, dataflow

### relational-dbms-reference-architecture — Relational DBMS Reference Architecture
- aka: anatomy of a database system, query processor / transactional storage manager decomposition
- kind: reference-architecture
- what: The canonical decomposition of a DBMS into process manager, query processor (parser, rewriter, optimizer, executor), transactional storage manager, and shared utilities.
- problem: Database engines recur in structure; the reference decomposition names the component roles every implementation fills.
- named-in: corpus:hellersteindb — Architecture of a Database System - Hellerstein, Stonebraker & Hamilton (2007)
- tags: database


## Architecture-description constructs — `description` (16)

### 4-1-view-model — 4+1 View Model
- aka: 4+1 architectural view model, Kruchten 4+1
- kind: description
- what: A fixed viewpoint set — logical, process, development, and physical views, plus scenarios (the +1) that tie them together — for describing a software architecture.
- problem: Single-diagram architecture descriptions overload one drawing with every stakeholder's concerns; a small fixed set of concurrent views, validated by use-case scenarios, covers the stakeholder spectrum without conflating concerns.
- named-in: corpus:kruchten — Architectural Blueprints — The 4+1 View Model of Software Architecture — Kruchten (1995)
- tags: architecture-description, viewpoint-set

### allocation-view — Allocation View
- aka: allocation viewtype, mapping view
- kind: description
- what: A view type mapping software elements onto structures in the system's environment — hardware and networks (deployment), file systems (implementation), and teams (work assignment).
- problem: Neither module nor runtime structure says where software executes, lives on disk, or who builds it; a dedicated mapping view type carries the software-to-environment correspondences these concerns need.
- named-in: corpus:vab — Documenting Software Architectures: Views and Beyond, 2nd ed. — Clements et al. (2010)
- tags: architecture-description, viewtype, deployment

### architectural-perspective — Architectural Perspective
- aka: perspective (Rozanski–Woods), quality perspective
- kind: description
- what: A collection of activities, tactics, and guidelines for ensuring that a system exhibits a particular quality property, applied across all of a description's views rather than forming a view of its own.
- problem: Quality attributes (security, performance, availability, evolution) cut across every view; treating each as yet another view duplicates content, so a cross-cutting construct is applied to existing views instead. Highly bridgeable: perspective instances map onto quality attributes and their tactics.
- named-in: corpus:rozanski — Software Systems Architecture, 2nd ed. — Rozanski & Woods (2011)
- tags: architecture-description, quality-attributes

### architecture-decision-record — Architecture Decision Record
- aka: ADR, architectural decision record, decision record
- kind: description
- what: A short, versioned document capturing one architecturally significant decision together with its context, status, and consequences.
- problem: Design rationale evaporates as teams change; later maintainers see what was decided but not why, and either cargo-cult the decision or blindly reverse it. A lightweight per-decision record kept with the code preserves the why at low cost.
- named-in: corpus:nygardadr — Documenting Architecture Decisions — Michael Nygard (2011)
- tags: architecture-description, documentation, agile

### architecture-description — Architecture Description
- aka: AD, architectural description
- kind: description
- what: The concrete work product (documents, models, views) used to express the architecture of a system of interest.
- problem: An architecture is intangible and lives partly in architects' heads; stakeholders need a durable, reviewable artifact that expresses it and can be checked for concern coverage.
- named-in: corpus:iso42010 — ISO/IEC/IEEE 42010:2022 — Architecture description
- tags: architecture-description, standard

### architecture-description-language — Architecture Description Language
- aka: ADL
- kind: description
- what: A formal notation whose first-class constructs are architectural — components, connectors, configurations — used to model and analyze a software architecture.
- problem: Box-and-line diagrams lack defined semantics, so descriptions cannot be analyzed or checked for consistency; an ADL gives architectural constructs a defined syntax and semantics amenable to tooling (instances — AADL, Wright, Rapide, Darwin, ACME — stay works; AADL is corpus work feilergluch).
- named-in: corpus:iso42010 — ISO/IEC/IEEE 42010:2022 — Architecture description
- tags: architecture-description, formal-methods

### architecture-framework — Architecture Framework
- aka: architecture description framework, ADF
- kind: description
- what: An established package of conventions, principles, viewpoints, and practices for architecture description within a specific domain or stakeholder community.
- problem: Communities and organizations repeatedly need the same viewpoints and description conventions; packaging them as a reusable framework standardizes descriptions across projects (instances such as TOGAF or DoDAF stay works, not elements).
- named-in: corpus:iso42010 — ISO/IEC/IEEE 42010:2022 — Architecture description
- tags: architecture-description, enterprise

### architecture-view — Architecture View
- aka: view, architectural view
- kind: description
- what: A representation of a system's architecture from the perspective of a related set of concerns, composed of one or more architecture models.
- problem: No single representation can serve all stakeholders; splitting the description into concern-focused views keeps each representation coherent, readable, and auditable against the concerns it frames.
- named-in: corpus:iso42010 — ISO/IEC/IEEE 42010:2022 — Architecture description
- tags: architecture-description

### architecture-viewpoint — Architecture Viewpoint
- aka: viewpoint
- kind: description
- what: A reusable work product establishing the conventions — model kinds, notations, methods — for constructing, interpreting, and using views that frame a specific set of stakeholder concerns.
- problem: Views built ad hoc are inconsistent across systems and teams; making the conventions first-class lets viewpoints be declared, reused, and conformance-checked independently of any one system.
- named-in: corpus:iso42010 — ISO/IEC/IEEE 42010:2022 — Architecture description
- tags: architecture-description

### component-and-connector-view — Component-and-Connector View
- aka: C&C view, component-and-connector viewtype, runtime view
- kind: description
- what: A view type documenting the system's runtime elements (components) and their interaction pathways (connectors) — pipes-and-filters, client-server, publish-subscribe structures and the like.
- problem: Static module structure says little about runtime behavior, concurrency, or data flow; a dedicated runtime view type is where architectural styles and connector choices become visible and analyzable.
- named-in: corpus:vab — Documenting Software Architectures: Views and Beyond, 2nd ed. — Clements et al. (2010)
- tags: architecture-description, viewtype

### context-map — Context Map
- aka: bounded-context relationship map
- kind: description
- what: A documented map of the system's bounded contexts and the relationship type at each seam (partnership, customer-supplier, conformist, ACL, ...).
- problem: Teams need a shared, honest picture of model boundaries and inter-context translation obligations to coordinate integration.
- named-in: corpus:evansddd — Domain-Driven Design - Evans (2003)
- tags: ddd, enterprise, description, borderline — An architecture-description artifact rather than a runtime structure; kind description per 42010-style constructs.

### interface-definition-language — Interface Definition Language
- aka: IDL, schema-first contract, .proto contract, ASN.1 module
- kind: description
- what: A language-neutral contract describing component interfaces and data types from which stubs, skeletons and serializers are generated.
- problem: Cross-language, cross-component boundaries need a single authoritative contract rather than per-language duplication.
- named-in: corpus:corbaspec — The Common Object Request Broker: Architecture and Specification - OMG (1991)
- tags: distributed, integration, borderline — A contract-and-toolchain construct rather than a runtime structure, but the established architecture-level boundary description mechanism.

### model-kind — Model Kind
- aka: architecture model kind
- kind: description
- what: The conventions (notation, modeling template, analytic methods) for one type of architecture model used within a viewpoint, e.g. a state-machine or dataflow model kind.
- problem: A viewpoint typically needs several distinct model types; declaring each model type's conventions separately keeps individual models checkable and lets model kinds be reused across viewpoints.
- named-in: corpus:iso42010 — ISO/IEC/IEEE 42010:2022 — Architecture description
- tags: architecture-description

### module-view — Module View
- aka: module viewtype, module structure view
- kind: description
- what: A view type documenting the system's units of implementation (modules) and their static relations — decomposition, uses, layering, generalization, data-model.
- problem: Stakeholders doing construction, modification-impact analysis, and work assignment reason about code structure, not runtime; a dedicated static-structure view type keeps implementation-unit concerns separate from runtime concerns.
- named-in: corpus:vab — Documenting Software Architectures: Views and Beyond, 2nd ed. — Clements et al. (2010)
- tags: architecture-description, viewtype

### rozanski-woods-viewpoint-catalog — Rozanski–Woods Viewpoint Catalog
- aka: viewpoint catalog (Rozanski–Woods)
- kind: description
- what: A catalog of seven viewpoints — context, functional, information, concurrency, development, deployment, operational — for describing information-system architectures.
- problem: Architects reinvent view structure per project; a checklist-strength, reusable viewpoint catalog with defined models and pitfalls per viewpoint standardizes coverage. Granularity call: the catalog is one element, not seven — per-viewpoint entries would balloon the realm without adding bridge endpoints beyond what 4+1 and the Views-and-Beyond viewtypes already give.
- named-in: corpus:rozanski — Software Systems Architecture, 2nd ed. — Rozanski & Woods (2011)
- tags: architecture-description, viewpoint-set, enterprise

### stakeholder-concern — Stakeholder Concern
- aka: concern, architecture concern
- kind: description
- what: An interest in the system relevant to one or more stakeholders, used to scope which viewpoints and views an architecture description must provide.
- problem: Architecture descriptions must demonstrably address what matters to whom; naming concerns explicitly lets viewpoint selection be justified and concern coverage be audited.
- named-in: corpus:iso42010 — ISO/IEC/IEEE 42010:2022 — Architecture description
- tags: architecture-description, borderline — Concept-vs-construct call: included as a construct because ISO 42010 defines it normatively and viewpoints are specified by the concerns they frame; bridging value to design elements is low — bridge indirectly via quality attributes where applicable.


---

# Decision log

## Granularity, merge & altitude decisions

- MERGE: four same-element pairs from different scouts folded (anti-corruption layer, EIP remote-procedure-invocation integration style, Provos privilege separation, POSA4 component container).
- RENAME: id hygiene - privilege-separation-arch, component-container (POSA4 sense; the OS/deployment container is its own new element), m-out-of-n-voting, half-object-plus-protocol-arch, hardware-abstraction-layer-arch.
- KEEP-BOTH: dataflow-architecture (Shaw-Garlan classical family) vs streaming-dataflow-architecture (Akidau unbounded-stream topology) - specializes edge in 3b; monitor (Bass tactic) vs design-realm monitor (Hoare) per same-name-two-realms; channel-architecture (Douglass) vs message-channel (connector); temporal-firewall (Kopetz) vs firewall; time-triggered-bus (connector) vs time-triggered-architecture (style).
- EDITOR ADDS (scout-flagged gaps, certain sources): subsumption-architecture (Brooks 1986 - robotics control vocabulary, bridge target for behavior-tree); os-container (Burns-Oppenheimer 2016 - the deployment-unit sense, distinct from POSA4 component-container); the observability structures the quality scout flagged as unowned - distributed-tracing (Dapper 2010), log-aggregation + health-check-api (Richardson 2018). Declined: sense-plan-act (naming diffuse across robotics texts), models of computation (leeseshia - modeling formalisms, a different band than architecture elements; logged not cataloged), 'metrics collection' (Richardson names it but it folds into log-aggregation/observability family - too thin alone... kept OUT, noted).
- INTAKE AUDIT CLOSURE: 'Pipes and Filters (POSA1)' was a fuzz miss (pipes-and-filters is cataloged); 'Competing Consumers' now carries an explicit drop record (bridge, not catalog).
- REALM RESOLUTION: message-translator existed verbatim in both realms after the design-realm repair (bridge agent g2 flagged the id collision); the architecture entry is dropped - EIP establishes one mechanism-level sense; the bridge carries its relation to the messaging integration style.

## Parked-candidate intake (the Phase 1 → Phase 3a audit)

Disposition of candidates parked upward by Phases 1–2: admissions appear as catalog entries above; folds and drops are recorded here.

- **ATAM (Architecture Tradeoff Analysis Method)** — drop: Analysis/evaluation method, i.e. process, not an architecture element — excluded per charter rule.
- **ATAM (Architecture Tradeoff Analysis Method)** — drop: Analysis/evaluation method — process, not an element, per mission rule.
- **ATAM / QAW** — drop: Analysis/evaluation methods, excluded by charter rule (process, not elements).
- **Big Ball of Mud** — drop: Anti-pattern (Foote & Yoder 1997), excluded by mission rule; noted per charter instruction.
- **Blackboard** — drop: POSA1 scout carries it per charter.
- **Broker** — drop: POSA1 scout's territory (Broker is a POSA1 architectural pattern); not carried here to avoid duplicate ids - merge step should verify it landed.
- **Chaos Engineering** — drop: Met while judging operability candidates: an evaluation/verification method (like ATAM, methods are process, not elements).
- **Circuit Breaker (architecture sense)** — drop: Design realm already carries the circuit-breaker mechanism (Nygard); no distinct system-topology structure beyond the mechanism plus deployment - bridge, don't duplicate. Tactics scout may still claim the availability-tactic slot.
- **Claim Check (Azure/EIP, system-scale, in the wiki-longtail multi-entry)** — drop: Duplicate of design-realm element claim-check; the system-scale form is the same mechanism riding on message-broker plus an external store - bridge it in 3b.
- **Communication / Coordination / Conversion / Facilitation (connector service categories)** — drop: The four service categories are classification dimensions of the taxonomy, not connector types; the eight types are the elements.
- **Competing Consumers (system-topology sense)** — drop → competing-consumers (design realm): the in-process element owns the mechanism; the scaling-topology sense is expressed by bridging it to messaging/message-broker/load-balanced pools, not by a second node
- **correspondence / correspondence rule (ISO 42010)** — drop: Normative bookkeeping construct relating AD elements within the standard; essentially no use outside the standard's text and no bridge value to design elements.
- **Data Lake** — drop: Named (Dixon 2010; Fowler bliki 2015) but is a storage-topology concept with weak structural commitments; data-mesh carries the analytical-data reference-architecture slot.
- **Distributed Consensus (Paxos/Raft)** — drop: Judged algorithm/protocol granularity for this catalog (algorithmics zoo); leader-election and replication entries carry the architectural slots. Flag for the merge editor: DDIA names consensus as a first-class concept - revisit if the bridge needs the endpoint.
- **Fielding's intermediate derived styles (client-stateless-server, layered-client-server, etc.)** — drop: Constraint-composition waypoints on the derivation path to REST, not independently used styles; REST itself is cataloged.
- **GitOps** — drop: Met while judging deployment candidates: a delivery practice (declarative desired state reconciled from git), pass-7 territory, not a structural element.
- **Heartbeat (availability tactic)** — drop: Bass-tactics scout's slot (charter's heartbeat-tactic example illustrates id suffixing, not assignment); design realm already has the mechanism.
- **Heterogeneous Architectures** — drop: Garlan-Shaw 3.8 is a meta-observation (styles combine hierarchically, per-component, or by elaboration), not a specific bridgeable structure; a catch-all node is worthless by mission rule.
- **Increase Cohesion / Reduce Coupling / Detect Faults / Recover from Faults / Prevent Faults / Detect Attacks / Resist Attacks / React to Attacks / Recover from Attacks / Containment / Limit Consequences / Barrier / Monitor Resources / Allocate Resources / Reduce Resource Demand / Control Resource Demand / Manage Resources (performance) / Limit Dependencies / Adapt / Coordinate / Control and Observe System State / Limit Complexity / Support User Initiative / Support System Initiative** — drop: Tactic-category headings, recorded as bck-cat: tags on the leaf elements instead of as elements — a catch-all node is worthless by mission rule.
- **Infrastructure as Code** — drop: A practice (managing infrastructure through versioned definitions) - pass-7 process territory; its structural corollary is cataloged as immutable-infrastructure.
- **KWIC solutions / compiler / Hearsay-II / cruise-control case studies** — drop: Shaw-Garlan case studies are exemplars illustrating the styles, not elements.
- **Layered Architecture / Pipes-and-Filters** — drop: Canonical Shaw-Garlan/POSA1 styles belonging to those scouts; my n-tier entry covers only the physical-tier enterprise variant.
- **Limp-home / degraded mode operation** — drop: Parked by embedded-mech, but it is the graceful-degradation family - resilience-scout territory (Graceful Degradation is on the parked list under that scout); dropping here to avoid cross-scout duplication, not from the catalog.
- **Message Broker / Message Bus / integration styles (File Transfer, Shared Database, RPC, Messaging)** — drop: EIP scout territory (Hohpe root patterns and integration styles); overlap permitted but not duplicated from here.
- **Message Translator** — drop → message-translator (design realm): EIP names one mid-level transformation mechanism, implementable in-process - it belongs to the design realm (added there as element 709 by the Phase 3 audit); not a same-name-two-realms case since only one sense is source-established. Bridge expresses its architecture relation (realizes messaging integration style).
- **Microkernel / Plug-in Architecture** — drop: POSA1 pattern (also a Richards & Ford style); left to the POSA1 scout - merge step should verify it landed.
- **Models of computation (synchronous-reactive, SDF, discrete-event - Lee & Seshia)** — drop: Named and canonical (leeseshia) but they are architecture-description/semantic-model constructs (kind: description) closer to an ADL/MoC scout's territory; flagged as thin spot rather than claimed here.
- **OSEK/AUTOSAR OS conformance classes (BCC/ECC)** — drop: API conformance profiles of an OS standard, not architectural structures.
- **Presentation-Abstraction-Control (PAC)** — drop: POSA1 scout may carry per charter; not duplicated here.
- **Process Manager (EIP)** — drop: EIP's name for the central workflow engine; the generic structure is cataloged here as orchestration - EIP scout may still carry Process Manager, merge as alternative naming.
- **Publisher-Subscriber (POSA1 / distributed pub-sub style)** — drop: Out of this scout's charter, not a rejection of the element: POSA1 lists it among its design patterns (design realm holds observer with publish-subscribe as aka), and distributed pub-sub as an architecture style belongs to the Shaw-Garlan/Taylor styles scout per the same-name-two-realms rule. Recorded here only to prevent double-entry.
- **QAW (Quality Attribute Workshop)** — drop: Elicitation workshop — process, not an element, per mission rule.
- **Replicated Component Group (POSA4)** — drop: Could not confirm this exact pattern name on a live POSA4 pattern list this session (Container 20.2 and Activator 20.14 were confirmed; this was not in the retrieved list); replication-for-availability structure belongs with the Bass availability-tactics scout (redundancy/replication tactics) - deferred there, not silently discarded.
- **REST** — drop: Charter assigns REST to the shaw-garlan-tmd scout; skipped here per instruction.
- **SAAM / CBAM** — drop: Evaluation methods — process, not elements, per mission rule.
- **Safety island** — drop: Real SoC construct (Arm/NVIDIA automotive platforms) but naming is vendor-doc level and hardware-platform scoped; establishedness as a software-architecture element too thin this pass.
- **Safety tactics catalog (Wu-Kelly, via Preschern)** — drop: A tactics taxonomy/organizing scheme, not an element; its named members are admitted individually (redundancy, graceful-degradation, monitor-actuator, triple-modular-redundancy) or already live in the design realm (sanity check, watchdog, N-version).
- **Self-Contained Systems (SCS)** — drop: scs-architecture.org names it, but it substantially overlaps service-based architecture + micro-frontends; establishedness beyond its advocacy site is thin.
- **Shed Work at Periphery** — drop: A placement corollary of the design element load-shedding (shed at the edge); bridge load-shedding to api-gateway/gatekeeper in 3b rather than minting a separate architecture element.
- **Single Access Point + Check Point (Yoder & Barcalow)** — drop: Duplicate of design-realm elements single-access-point and check-point (already cataloged there); the Yoder-Barcalow architectural framing is bridged in 3b instead of duplicating the nodes.
- **Small Architecture (Noble & Weir pattern group)** — drop: A pattern-group/chapter heading, not one mechanism; its architecture-level member Application Switching is admitted, the remaining members (pools, overlays, compression) are design-level.
- **Sparse global time base** — drop: Kopetz names it, but it is a property/model of the time domain underpinning TTA, not a structural element; TTA's entry carries the concept.
- **Split top-half/bottom-half driver architecture (as OS structuring principle)** — drop: The per-driver mechanism is the design element deferred-interrupt-processing; the kernel-wide 'all drivers in halves' principle has no independent established name beyond being an instance of layering.
- **stakeholder** — drop: A role concept, not an architecture-description construct; the bridgeable content lives in stakeholder-concern.
- **Subsumption architecture / Sense-Plan-Act (robotics)** — drop: Established robotics reference architectures (Brooks 1986; Murphy) but outside this charter's corpus base; flagged as a gap-sweep candidate if no scout owns robotics/CPS control structures.
- **Tactics-Based Questionnaires** — drop: Assessment instrument appearing in every bck QA chapter; process artifact, not an element.
- **Three-Phase Commit** — drop: Skeen's non-blocking variant of 2PC - algorithm-variant granularity (algorithmics zoo); 2PC carries the architectural slot.
- **Twelve-Factor App** — drop: Methodology/practice checklist (process territory, pass 7), not a structure.
- **Twelve-Factor App** — drop: A methodology - a checklist of twelve practices for SaaS operability - not a structural element; its structural factors (external configuration, stateless processes, port binding, disposability) are covered by or bridgeable to specific elements. Charter judged as likely non-element; confirmed drop.
- **UML as architecture notation** — drop: A general modeling language is a work/notation, not an architecture element; corpus work medvidovicuml covers the works angle.
- **view packet (Views and Beyond)** — drop: Documentation chunking device (a small stakeholder-sized piece of a view) within one book's method; too fine-grained, no bridge value.
- **Abstraction Layer / Hardware Abstraction Layer (Fluent C, Beningo)** — fold → hardware-abstraction-layer-arch: Fluent C's Abstraction Layer names the same platform-layer construct; recorded as aka.
- **Active Redundancy (hot spare) / Passive Redundancy (warm spare) / Cold Spare** — fold → redundant-spare-tactic: 3rd-ed separate tactics merged in the 4th ed into one Redundant Spare tactic with hot/warm/cold variants; kept as aka.
- **Active-object framework (run-to-completion kernel)** — fold → actor-model-architecture: QP-style active-object frameworks are the embedded realization of actor-based architecture; recorded as aka there. The Active Object pattern itself is a design element.
- **ADL instances (AADL, Wright, Rapide, Darwin, xADL, ACME)** — fold → architecture-description-language: Per charter: ADL is one element; instances stay works (AADL is already corpus work feilergluch).
- **APEX API** — fold → time-space-partitioning: The ARINC 653 partition API is the interface of the partitioning architecture, not a separate architecture element.
- **Application Controller (POSA4)** — fold → application-controller: POSA4 reuse of the PoEAA pattern; one element.
- **architecture decision / architecture rationale (ISO 42010; Perry & Wolf 1992)** — fold → architecture-decision-record: The ADR is the established, bridgeable documentation construct; decision and rationale (first named as an architecture component in perrywolf) are its content, not separable elements.
- **architecture model** — fold → model-kind: The model is an instance; the model kind carries the reusable conventions — one element suffices.
- **Authoritative Server model (gap-games-netcode)** — fold → authoritative-server: Duplicate of the nystrom-games candidate.
- **Blackboard (wiki-longtail)** — fold → blackboard: Duplicate of the POSA1 Blackboard candidate.
- **Bounded Context (gap2-fowler-bliki-sweep)** — fold → bounded-context: Duplicate of the poeaa-ddd candidate.
- **Broker (POSA1/POSA4, posa scout)** — fold → broker: Duplicate of the douglass-samek Broker candidate; one element citing POSA1.
- **Client Proxy (POSA4)** — fold → broker-style: POSA4's decomposition of Broker into internal middleware roles; component-level machinery below architecture altitude - documented as Broker internals, resurrectable if Phase 3b needs finer endpoints (design realm already carries proxy aka Remote Proxy).
- **Client Request Handler (POSA4)** — fold → broker-style: Broker-internal transport role (POSA4 Broker decomposition); below architecture altitude on its own.
- **Compartmentalization** — fold → privilege-separation-arch: Parked as 'Defense in Depth / Compartmentalization'; the compartment structures are already specific entries (privilege-separation-arch, sandbox-architecture, bulkhead-arch, dmz) - a general compartmentalization node would be a catch-all, worthless for bridging.
- **Compensating Transaction (Azure)** — fold → saga: The compensating action is the saga's constituent mechanism, not a separate topology; folded as aka.
- **Component Replacement / Compile-time Parameterization / Aspects / Configuration-time Binding / Resource Files / Interpret Parameters / Shared Repositories / Polymorphism (as binding mechanisms)** — fold → defer-binding-tactic: Enumerated as binding-time mechanisms realizing Defer Binding (ch8) and as component-substitution techniques (ch12); realization-level, mostly covered by design-realm elements.
- **Cyclic executive (architecture sense)** — fold → superloop-architecture: The design realm's cyclic-executive already carries the timeline/major-minor-frame vocabulary; at system level the choice it represents is covered by the superloop and time-triggered style entries. Flag for the editor: if Phase 3b needs a distinct avionics-style cyclic-executive endpoint (Baker & Shaw 1989), it can be split back out.
- **Dark Launch** — fold → feature-flag-release: Deploying dark and exposing later is exactly the feature-flag-driven release structure; kept as aka.
- **Decoupling Middleware (Nygard)** — fold → message-broker: Nygard's stability pattern prescribes exactly the broker/messaging intermediary topology; recorded as aka.
- **Domain Model (POSA4)** — fold → domain-model: POSA4 took it from PoEAA; one element citing PoEAA.
- **Event Notification (Fowler 2017)** — fold → publish-subscribe-topology: Fowler's event-notification is the plain pub-sub interaction (thin events, callback for state); the distinct mechanism he separates out - event-carried state transfer - is cataloged as its own element.
- **Event Notification (TMD style entry)** — fold → implicit-invocation: TMD's 'event-based' style is the same mechanism Garlan-Shaw name event-based implicit invocation; the distributed many-to-many variant with an event service is publish-subscribe-style.
- **Event Sourcing (Azure)** — fold → event-sourcing-style: Duplicate of the poeaa-ddd event-sourcing-style candidate.
- **Fail-silent unit** — fold → fault-containment-region: Kopetz's fail-silence is a failure-mode assumption placed on an FCR, not a separate structure; noted in the FCR/FTU entries.
- **Firewall Proxy (POSA4)** — fold → proxy-based-firewall: Same mechanism as Schumacher's Proxy-Based Firewall; recorded as aka.
- **Front Controller (POSA4)** — fold → front-controller: POSA4 reuse of the PoEAA pattern; one element.
- **Function Patch / Class Patch / In-Service Software Upgrade (ISSU)** — fold → software-upgrade-tactic: Named as realization variants of the Software Upgrade tactic; kept as aka.
- **Gateway Aggregation / Gateway Routing / Gateway Offloading (Azure)** — fold → api-gateway: Three facets of the single gateway role; folded as aka to avoid triple-counting one structure.
- **Graceful Degradation / Degraded Mode (gap2-adversarial-final)** — fold → graceful-degradation: Duplicate of the resilience candidate.
- **Health Check (endpoint) (resilience scout)** — fold → health-check-api: Duplicate of the Richardson-named candidate.
- **Health Check API (Richardson)** — fold → health-endpoint-monitoring: Same structure as Azure's Health Endpoint Monitoring; Richardson's name folded as aka, Azure entry kept as canonical because the naming source is corpus-citable (azurepatterns).
- **Health Endpoint Monitoring (Azure)** — fold → health-check-api: External probing reading of the same health-endpoint contract; recorded as aka.
- **individual Rozanski-Woods perspectives (security, performance and scalability, availability and resilience, evolution, ...)** — fold → architectural-perspective: The construct is the element; perspective instances bridge via qa:<attribute> tactics, which are the tactics scouts' territory.
- **individual Rozanski-Woods viewpoints (context, functional, information, concurrency, development, deployment, operational)** — fold → rozanski-woods-viewpoint-set: Granularity call: the book names them as one coherent catalog; seven per-viewpoint entries add no bridge endpoints beyond the catalog, 4+1, and the three viewtypes.
- **Invoker (POSA4)** — fold → broker-style: Broker-internal server-side dispatch role (POSA4 Broker decomposition); below architecture altitude on its own.
- **Layered firmware architecture (driver/HAL/middleware/application)** — fold → layered-architecture: Domain instance of Layers; recorded as aka. The HAL layer itself is admitted separately (hardware-abstraction-layer-arch).
- **Layered Pattern (RTDP)** — fold → layered-architecture: Same mechanism as POSA1 Layers; RTDP name recorded as aka.
- **Layers (POSA1)** — fold → layered-architecture: The admitted element cites POSA1 Layers as its naming source; this parked duplicate folds.
- **Limp-home / degraded mode operation** — fold → graceful-degradation: Automotive name for the same tactic; recorded as aka.
- **Manage Work Requests** — fold → manage-event-arrival-tactic: 4th-ed parent grouping whose two leaves (manage event arrival, manage sampling rate) are cataloged; the parent adds no distinct mechanism.
- **MCAL / ECU Abstraction Layer / Complex Device Driver** — fold → autosar-layered-architecture: Named sub-layers of the AUTOSAR layer stack; splitting them out would fragment one reference layering into non-bridgeable shards.
- **Message Channel (POSA4, from EIP)** — fold → message-bus-arch: Generic root concept, too catch-all to be a bridgeable endpoint; the concrete channel kinds are already design-realm elements (message-queue aka point-to-point channel; publish-subscribe-channel) and the topology-scale channel fabric is Message Bus / Message Broker.
- **Message Endpoint (POSA4, from EIP)** — fold → channel-adapter-arch: The application-side connection code is design-level (design realm carries event-driven-consumer, idempotent-receiver, message-dispatcher); its system-boundary flavor at architecture scale is the Channel Adapter.
- **Message Router (POSA4, from EIP)** — fold → message-broker-arch: The routing mechanism is already a design-realm element (content-based-router); the topology-scale routing intermediary is the Message Broker hub.
- **Message Translator (POSA4, from EIP)** — fold → canonical-data-model-arch: Format mediation as an architecture-scale statement is the Canonical Data Model (plus the broker's transformation stage); the in-component translator mechanism is design-level - flagged as a design-realm addendum candidate rather than duplicated here.
- **Messaging Bridge (Azure, in the wiki-longtail multi-entry)** — fold → messaging-bridge: Duplicate of the EIP Messaging Bridge.
- **Microkernel (POSA1)** — fold → microkernel: Duplicate; the admitted element cites POSA1.
- **Microkernel Architecture Pattern (RTDP)** — fold → microkernel: Same mechanism as POSA1 Microkernel; RTDP name recorded as aka.
- **Model View Controller (PoEAA)** — fold → model-view-controller: Same pattern; POSA1 citation is canonical for the architecture realm.
- **Model-View-Controller (POSA1)** — fold → model-view-controller: Duplicate; one element.
- **Monitor-Actuator (Preschern EuroPLoP)** — fold → monitor-actuator: Duplicate; Douglass RTDP is the naming source.
- **MV* family (Model-View-Controller, MVP, MVVM) (Osmani)** — fold → model-view-controller: Family flag; MVC, MVP and MVVM are each admitted individually - the conspicuous-absence concern is resolved.
- **Onion Architecture** — fold → clean-architecture: Palermo (2008) names the same concentric dependency-rule structure Martin generalizes; kept as aka on clean-architecture per charter fold decision. Hexagonal kept separate (ports/adapters is a distinct named structure with its own naming source and mechanism emphasis).
- **Packet Filter Firewall** — fold → firewall: Schumacher et al. catalog it as a separate pattern, but at catalog granularity it is a variant mechanism of the firewall choke point; kept as aka.
- **Page Controller (POSA4)** — fold → page-controller: POSA4 reuse of the PoEAA pattern; one element.
- **Pipeline** — fold → pipes-and-filters: Linear specialization of pipes-and-filters (Garlan-Shaw name it as such); recorded as aka.
- **Pipes and Filters (EIP integration style)** — fold → pipes-and-filters-style: EIP explicitly restates the POSA1/Garlan-Shaw style at integration scale (steps joined by message channels); same macro structure, one element - EIP usage recorded in the entry's aka and problem text.
- **Pipes and Filters (integration style, EIP)** — fold → pipes-and-filters: EIP's integration reading of the same POSA1/Shaw-Garlan style; one architecture element.
- **Preprocessor Macros (testability substitution technique)** — fold → specialized-interfaces-tactic: ch12 lists it as a technique to swap in state-reporting code; a realization mechanism, not a tactic leaf.
- **Presentation-Abstraction-Control (ui-reactive)** — fold → presentation-abstraction-control: Duplicate of the POSA1 PAC candidate.
- **Proxy-Based Firewall** — fold → firewall: Same judgment as packet filter firewall - application-level variant of the firewall element; kept as aka.
- **Publisher-Subscriber (Azure)** — fold → publish-subscribe-style: Azure name for the pub-sub system topology; recorded as aka.
- **Query optimizer / query planner** — fold → relational-dbms-reference-architecture: A component role within the DBMS reference decomposition (Hellerstein et al.), not a standalone style/pattern; the reference architecture is admitted and carries the role.
- **Redundant channel structures (TMR, dual-channel 1oo2, homogeneous/heterogeneous)** — fold → redundancy: Umbrella over structures admitted individually (triple-modular-redundancy, homogeneous-redundancy, heterogeneous-redundancy); the general provisioning decision is the redundancy tactic.
- **Reference Monitor (architecture twin)** — fold → policy-decision-point: Design realm already holds reference-monitor (robustness-security) with the PDP/PEP operational split in its aka; the system-level sense that the parked list demanded is the PDP/PEP externalized-authorization topology, cataloged here - a second reference-monitor node would duplicate it.
- **Requestor (POSA4)** — fold → broker-style: Broker-internal client-side invocation role (POSA4 Broker decomposition); below architecture altitude on its own.
- **Restore (security recover-from-attacks item)** — fold → redundant-spare-tactic: ch11 explicitly delegates restoration to the ch4 availability recover-from-faults tactics rather than naming a distinct security tactic.
- **Round-Robin with Interrupts (Simon) / foreground-background system** — fold → superloop-architecture: Simon distinguishes it from plain round-robin, but Labrosse and common usage equate foreground/background with the superloop family; kept as aka to avoid over-splitting one bare-metal style.
- **RPC (Remote Procedure Call) as connector element** — fold → procedure-call-connector: In the Mehta-Medvidovic-Phadke taxonomy RPC is a composite species (procedure call + distributor), not a ninth basic type; recorded as aka on procedure-call-connector, composition noted on distributor-connector.
- **Safety Executive (Preschern EuroPLoP)** — fold → safety-executive: Duplicate; Douglass RTDP is the naming source, Preschern's pattern system a treatment.
- **Saga (gap-adversarial)** — fold → saga: Duplicate of the resilience Saga/Compensating Transaction candidate.
- **Scheduling policies (FIFO, fixed-priority, semantic importance, rate-monotonic, deadline-monotonic, round-robin, EDF, least-slack-first, cyclic executive/static scheduling)** — fold → schedule-resources-tactic: Named in a sidebar as policies selectable by the Schedule Resources tactic, not tactics themselves; the design realm already carries scheduling elements (e.g. dynamic-priority-scheduling) that will bridge here.
- **Search-engine index tier (index + query fan-out architecture)** — fold → sharding: The sharded index-serving tier is sharding (plus replication) applied to an inverted index; no distinct canonical name establishes it as its own element.
- **Server Request Handler (POSA4)** — fold → broker-style: Broker-internal transport role (POSA4 Broker decomposition); below architecture altitude on its own.
- **Session State placement trio (gap2-streams-poeaa-tail)** — fold → client-session-state: Duplicate of the poeaa-ddd trio; client-session-state, server-session-state and database-session-state are each admitted.
- **Sharding (Azure)** — fold → sharding: Duplicate; recorded as aka.
- **Sharding / data partitioning scheme (dsa-blocks)** — fold → sharding: Duplicate of the db-internals sharding candidate; one element.
- **Shared-nothing architecture (lockfree-mem)** — fold → shared-nothing-architecture: Duplicate of the db-internals shared-nothing candidate.
- **Spatial/temporal partitioning (ARINC 653 / IMA, embedded-mech)** — fold → time-space-partitioning: Duplicate of the corpus-seed ARINC 653 candidate.
- **System Exceptions** — fold → exception-detection-tactic: Listed as a refinement of exception detection; names a category of processor exceptions, not a distinct tactic.
- **Template View (POSA4)** — fold → template-view: POSA4 reuse of the PoEAA pattern; one element.
- **Time-Triggered Architecture (Kopetz, embedded-mech)** — fold → time-triggered-architecture: Duplicate of the corpus-seed TTA candidate.
- **Transform View (POSA4)** — fold → transform-view: POSA4 reuse of the PoEAA pattern; one element.
- **Triple Core Lock-Step (TCLS)** — fold → lockstep-cores: Arm's TCLS (2016/2019 papers) is the voting variant of core lockstep; folded as aka.
- **Triple Modular Redundancy (resilience scout)** — fold → triple-modular-redundancy: Duplicate of the RTDP TMR candidate; Lyons & Vanderkulk 1962 noted as origin.
- **Two-Phase Commit (gap2-adversarial-final)** — fold → two-phase-commit: Duplicate of the db-internals 2PC candidate.
- **Unidirectional Data Flow** — fold → flux: Family umbrella over Flux/Elm/MVI; recorded as aka on flux, with elm-architecture and model-view-intent admitted as the other named members.
- **Unidirectional Data Flow (umbrella)** — fold → flux-architecture: Family umbrella over Flux/Elm/MVI - a catch-all node is worthless by mission rule; the concrete named members (Flux, Elm Architecture) are cataloged and the umbrella name is annotated as aka on Flux.
- **viewtype (generic Views-and-Beyond term)** — fold → module-view: The generic term is scaffolding; the three named viewtypes (module, C&C, allocation) are the established elements. Folded nominally into module-view; applies equally to all three.
- **Virtual Machine (as separate style)** — fold → interpreter-style: Garlan-Shaw and TMD treat interpreters and virtual machines as one organization ('virtual machines' is TMD's group label for interpreter/mobile-code/rule-based); aka recorded on interpreter-style.
- **Zero-Downtime Deployment** — fold → blue-green-deployment: An umbrella goal-name, not a distinct mechanism; realized by blue-green, rolling, and canary structures already cataloged.
