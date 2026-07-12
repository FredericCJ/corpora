# -*- coding: utf-8 -*-
"""TYPED reading-relation layer — the SWE-parity typed edge corpus over the netsim resources.

Unlike the mechanical `overlaps/mentions/named-in` edges (derived in build.py from item-number
references and shared identifiers), these are the *semantic* reading relations: the twelve-kind
vocabulary carried verbatim from the SWE explorer. Two provenance grades only — netsim's source
reports carry no typed edge list, so there is no `report:*` grade here:

  * `derived`   — mechanically grounded in report text (the mechanical edges, re-typed; the quote
                  is kept in `note`). Emitted by build.py's PHASE 3.6, not listed in this file.
  * `editorial` — maintainer judgment; a one-line rationale rides in `note`; rendered EDITORIAL and
                  dotted in the reading graph. Two sources: (1) the two EDITORIAL overlays, re-expressed
                  into the twelve kinds by the map below; (2) the hand-authored EXTRA_EDGES here.

Node ids are POST-merge explorer ids (g<item> / m<item> / gU<n> / mU<n>): build.py alias-rewrites and
drops any edge whose endpoint is not a corpus node, so a stale id fails soft (skipped), never silently
mis-links. Quarantined nodes may be endpoints only of `derived` `references` edges (build.py enforces).
"""

# The twelve kinds, verbatim from SWE. Directed reading semantics `s → t`.
KINDS = ['prerequisite-of', 'refines', 'subsumes', 'formalizes', 'surveys', 'applies-method-of',
         'companion', 'evaluates', 'critiques', 'supersedes', 'part-of', 'references']

# ── overlay re-expression ────────────────────────────────────────────────────────────────────────
# Each overlay stores directed (s, t) edges under one bespoke edgeKind. Map each into a typed kind
# and a direction; carry the overlay's own rationale verbatim as the edge note.
#   didactic       'read-before'    (s→t = "read s before t")          => (s, t, 'prerequisite-of')
#   specialization 'specialized-by' (s→t = "t specializes s → applied")=> (t, s, 'applies-method-of')
# The specialization default ('applies-method-of', flipped) reads "the applied instance applies the
# method of the theory"; EXTRA_EDGES below override individual pairs to the finer kind (refines /
# subsumes / formalizes) where the lineage warrants it.
OVERLAY_TYPED = {
    'didactic':       {'kind': 'prerequisite-of',   'flip': False},
    'specialization': {'kind': 'applies-method-of', 'flip': True},
}

# ── hand-authored editorial edges (the spine, and finer kinds beyond the overlay defaults) ─────────
# (s, t, kind, note). Precedence: EXTRA_EDGES override overlay-derived and mechanical-derived edges on
# the same ordered (s, t) pair, so a finer kind here replaces the coarse default. Seeded here; the NR1
# authoring pass extends this list over the grown corpus.
EXTRA_EDGES = [
    # edition / consolidation lineages
    ('g5', 'g6', 'supersedes',
     'Theory of Modeling and Simulation 3rd ed. consolidates and post-dates the 2nd — the later edition subsumes the earlier'),
    # surveys that catalog a tool / literature already in the corpus
    ('g2', 'g41', 'surveys',
     'a systematic literature review that maps the ns-3 simulation literature'),
    ('g14', 'g5', 'references',
     'a comparative evaluation of DEVS simulation tools against the formalism'),
    # compositional-analysis lineage (refine, not a bare reference)
    ('g174', 'g173', 'companion',
     'SymTA/S extends real-time/network calculus to compositional system-level worst-case analysis'),
    # co-design toolbox succession
    ('m40', 'm39', 'refines',
     'transient-performance analysis refines the jitter-performance toolbox for control-scheduling co-design'),
    # the frontier displacing an incumbent (report coverage text: "Sionna displacing MATLAB link-level tools")
    ('g105', 'm16', 'companion',
     'GPU-native, ML-integrated wireless simulation displaces MATLAB link-level tooling (report coverage summary)'),
    # formalization of the discrete-event tradition
    ('g5', 'g9', 'companion',
     'the DEVS formalism gives a formal system-theoretic semantics to discrete-event systems'),
    # an empirical evaluation grounding a simulator
    ('g104', 'g103', 'evaluates',
     'a calibration study evaluating the NR system-level simulator against 3GPP references'),
]

# ── NR1 authored edges ─────────────────────────────────────────────────────────────────────────
# Populated by the NR1 typed-edge authoring workflow (per-lane agents over the grown corpus). All
# editorial-grade (maintainer judgment; netsim's reports carry no edge list). Format: (s, t, kind, note).
# These override the coarse overlay-derived defaults on any shared (s, t) pair, and connect the
# breadth nodes (g177+) into the reading graph. Validated (endpoints exist, non-quarantined) at merge.
AUTHORED_EDGES = [
    ('g55', 'g54', 'refines', "Node states 'Mininet fork (Containernet) that runs Docker containers as emulated hosts with runtime add/remove' — extends Mininet for NFV/MEC/fog service prototyping."),
    ('g181', 'g54', 'refines', "Node states it 'Extends Mininet with virtual Wi-Fi stations and access points plus propagation and mobility models' — the SDN-wireless extension of Mininet."),
    ('g56', 'g54', 'applies-method-of', "Node states it 'Distributes Mininet across a cluster of workers via GRE tunnels and a configurable time-dilation factor' — scales the Mininet emulator to thousands of nodes."),
    ('g39', 'g54', 'refines', 'Mininet-HiFi adds container-based CPU/bandwidth resource isolation and a fidelity monitor to Mininet, making its emulated experiments performance-faithful and reproducible.'),
    ('g177', 'g54', 'prerequisite-of', "Emulab established the integrated real-node emulation testbed with time/space multiplexing; Mininet miniaturizes that emulation model onto a single laptop, so Emulab's testbed concepts underpin it."),
    ('g54', 'g134', 'applies-method-of', "Mininet's software switches (Open vSwitch) speak OpenFlow, so the emulator instantiates OpenFlow-based SDN prototyping — its founding purpose."),
    ('g57', 'g177', 'refines', "CrystalNet is the later cloud-scale, high-fidelity descendant of Emulab's run-real-code testbed idea, booting production device firmware images loaded with real configs."),
    ('g61', 'g178', 'companion', "The CORE manual/model documentation and the introducing paper 'CORE: A Real-Time Network Emulator' describe the same tool — sibling artifacts of one effort, no precedence."),
    ('g178', 'g54', 'companion', 'CORE and Mininet are parallel OS-namespace emulators; CORE emphasizes real-time operation, wireless/mobility scripting and hardware-in-the-loop, Mininet targets SDN/OpenFlow prototyping.'),
    ('g179', 'g180', 'companion', 'Kathara and containerlab are the two main declarative, container-based network-lab emulators, wiring Docker/generic containers into reproducible YAML topologies for labs and CI.'),
    ('g180', 'g55', 'companion', 'containerlab and Containernet both emulate network services from containers — containerlab wires vendor NOS/Linux containers via YAML, Containernet runs Docker hosts inside Mininet.'),
    ('g182', 'g56', 'companion', 'Kollaps (decentralized, tc/eBPF, no central emulator) and MaxiNet (GRE-tunneled cluster distribution) are parallel approaches to scaling container/SDN emulation across many machines.'),
    ('g183', 'g56', 'companion', "Both use time dilation / virtual time to decouple emulation from wall-clock and overcome host resource limits — MaxiNet's configurable time-dilation factor and TimeKeeper's kernel virtual clock."),
    ('g183', 'g58', 'companion', "TimeKeeper's controllable virtual time for real emulation parallels Shadow's simulated-time discrete-event execution of real applications — both make experiments independent of wall-clock speed."),
    ('g182', 'g59', 'companion', 'Both emulate end-to-end path properties (delay/bandwidth/loss) for unmodified applications — Kollaps via tc/eBPF topology shaping, Mahimahi via record-and-replay link shells.'),
    ('g183', 'g39', 'companion', 'Kernel virtual time is the enabling mechanism for the timing fidelity that container-based faithful emulation (Mininet-HiFi) strives to guarantee under host resource contention.'),
    ('g54', 'g42', 'companion', 'Mininet (emulation of real code in namespaces) and ns-3 (discrete-event simulation) are the two dominant open network-experimentation platforms, chosen by the fidelity/scale trade-off.'),
    ('g54', 'g44', 'companion', 'Mininet emulation versus OMNeT++ component-based discrete-event simulation — parallel paradigms for network-protocol experimentation.'),
    ('g39', 'g36', 'companion', 'Container-based reproducible emulation experiments and the simulation-credibility critique are parallel efforts to make network-experiment results trustworthy and repeatable.'),
    ('g60', 'g59', 'applies-method-of', "Pantheon builds its calibrated emulated network paths using Mahimahi's link/delay/loss emulation shells as the record-and-replay engine."),
    ('g62', 'g141', 'refines', 'Adds a lightweight virtual switch to raise P4-emulation fidelity and throughput beyond the BMv2 reference software switch, the standard but slow P4 dataplane target.'),
    ('g141', 'g137', 'applies-method-of', 'BMv2 is the reference behavioral-model implementation of the P4 abstract switch, executing compiled P4 programs.'),
    ('g138', 'g137', 'surveys', "Titled 'A Survey on Data Plane Programming with P4: Fundamentals, Advances, and...' — it catalogs the P4 language work and its ecosystem."),
    ('g135', 'g134', 'surveys', "The comprehensive SDN survey extensively catalogs OpenFlow, the protocol that launched software-defined networking, as the field's foundational enabling work."),
    ('g135', 'g54', 'references', 'The SDN survey cites Mininet as the de-facto SDN prototyping and emulation environment for experimenting with OpenFlow controllers.'),
    ('g140', 'g137', 'applies-method-of', 'P4sim brings the P4 programmable-data-plane model into ns-3, instantiating P4 packet processing inside the simulator.'),
    ('g181', 'g63', 'companion', 'Mininet-WiFi (software Wi-Fi/propagation-model emulation) and Colosseum (large-scale hardware RF channel emulator) are wireless-network emulators at opposite fidelity/scale points.'),
    ('g184', 'g128', 'part-of', 'GARNET is a component of gem5: "A Detailed On-Chip Network Model Inside a Full-System Simulator ... now gem5\'s Ruby" on-chip network model.'),
    ('g213', 'g129', 'part-of', '"The macroscale (SST/macro) element of Sandia\'s Structural Simulation Toolkit" — SST/macro is a module of SST.'),
    ('g68', 'g67', 'applies-method-of', 'ROSS is an optimistic "Time Warp" engine; the Time Warp / optimistic-synchronization mechanism originates in Jefferson\'s Virtual Time.'),
    ('g68', 'g210', 'applies-method-of', 'Reverse computation is "the defining method behind ROSS" for memory-frugal rollback instead of state-saving.'),
    ('g69', 'g68', 'applies-method-of', 'CODES torus/dragonfly models are "running on ROSS" — CODES instantiates the ROSS Time Warp engine.'),
    ('g210', 'g67', 'refines', "Reverse computation refines Time Warp's rollback, replacing state-saving with invertible event handlers; later work in Jefferson's optimistic lineage."),
    ('g214', 'g67', 'applies-method-of', "WARPED is a configurable Time Warp kernel implementing Jefferson's optimistic Virtual Time mechanism (antimessages, GVT)."),
    ('g215', 'g67', 'applies-method-of', "muSik's optimistic mode uses Time Warp state-saving synchronization derived from Virtual Time (it also supports conservative)."),
    ('g216', 'g68', 'evaluates', 'Warp Speed is a strong-scaling benchmark of ROSS (PHOLD at ~504B events/s) on ~2M Blue Gene/Q cores.'),
    ('g216', 'g210', 'applies-method-of', 'The 2M-core study runs "ROSS Time Warp + reverse computation" — it applies the reverse-computation rollback method.'),
    ('g187', 'g186', 'supersedes', 'Ramulator is the faster (~2.5x), template-based, more extensible DRAM simulator that largely displaced DRAMSim2 for new memory studies.'),
    ('g188', 'g186', 'companion', 'DiskSim (storage subsystem) and DRAMSim2 (memory subsystem) are sibling device-level timing simulators that add detailed subsystem fidelity to full-system studies.'),
    ('g129', 'g186', 'applies-method-of', "SST's memHierarchy can drive DRAMSim2 as its DRAM-timing backend, using its cycle-accurate memory engine as a component model."),
    ('g128', 'g187', 'applies-method-of', 'gem5 integrates Ramulator (via its gem5 wrapper) as an external cycle-level DRAM model.'),
    ('g130', 'g184', 'companion', 'BookSim (standalone) and GARNET (embedded in full-system simulators) are the two canonical cycle-accurate interconnection/NoC simulators.'),
    ('g185', 'g184', 'applies-method-of', "ASTRA-SIM drives gem5's Garnet as a cycle-accurate network backend to model collective communication over the fabric."),
    ('g211', 'g212', 'companion', 'GTNetS and PDNS are both Georgia Tech (Riley/Fujimoto) MPI-parallel packet-level network simulators scaling to hundreds of thousands of elements.'),
    ('g217', 'g212', 'companion', 'Both concern conservative (null-message) synchronization for parallel large-scale packet-level network simulation.'),
    ('g126', 'g213', 'companion', 'SimGrid (SMPI) and SST/macro both coarsely simulate skeletonized HPC/MPI applications over modeled network platforms.'),
    ('g215', 'g214', 'companion', 'muSik and WARPED are both reusable/configurable PDES kernels serving as testbeds for synchronization-algorithm research.'),
    ('g132', 'g185', 'references', "SimAI's distributed-DL-training infrastructure simulator builds on and references the ASTRA-SIM co-design approach."),
    ('g64', 'g67', 'surveys', 'The PDES survey catalogs optimistic synchronization / the Time Warp mechanism originating in Virtual Time.'),
    ('g64', 'g217', 'prerequisite-of', 'The PDES survey catalogs conservative synchronization algorithms for large-scale simulation.'),
    ('g131', 'g185', 'companion', 'Two index entries for the ASTRA-SIM distributed-DL-training simulator.'),
    ('g65', 'g64', 'subsumes', 'Fujimoto\'s book "Parallel and Distributed Simulation Systems" consolidates and generalizes his CACM "Parallel Discrete Event Simulation" survey.'),
    ('g42', 'g211', 'references', "ns-3's architecture and scalability lineage trace to Riley's GTNetS (shared author and design ancestry)."),
    ('g69', 'g213', 'companion', 'CODES/ROSS (dragonfly/torus, optimistic) and SST/macro (coarse-grained) are parallel large-scale HPC-interconnect PDES models — bridging the PDES-engine and architecture-simulator lineages.'),
    ('g120', 'g118', 'supersedes', "CloudSim Plus is a ground-up modular re-engineering of the CloudSim codebase (now Java 17+); its own summary calls it a re-engineering that 'effectively supersedes' CloudSim as the maintained implementation most new projects adopt."),
    ('g121', 'g118', 'applies-method-of', "iFogSim is 'built on CloudSim' (endpoint description), reusing CloudSim's discrete-event engine and datacenter/VM/host abstractions to model cloud-fog-IoT hierarchies and placement/offloading policies."),
    ('g189', 'g121', 'supersedes', "iFogSim2's description states it 'Extends and supersedes iFogSim', adding real EUA mobility traces, dynamic distributed clustering and microservice orchestration."),
    ('g189', 'g118', 'applies-method-of', 'iFogSim2, like its predecessor, still runs on the CloudSim engine, inheriting its discrete-event core and datacenter abstractions beneath the added mobility/clustering/microservice layers.'),
    ('g122', 'g118', 'applies-method-of', "EdgeCloudSim is a 'CloudSim-based environment' (endpoint description) that reuses CloudSim's engine and adds edge-specific WLAN/WAN network modeling, mobility models and an edge-orchestrator module."),
    ('g122', 'g121', 'companion', 'Sibling CloudSim-based edge/fog simulators of the same generation attacking the same modeling gap; EdgeCloudSim emphasizes network/mobility fidelity where iFogSim emphasizes application-placement policies. No precedence between them.'),
    ('g124', 'g123', 'companion', 'Parallel Python-based fog/IoT simulators built outside the CloudSim/Java lineage: LEAF contributes a granular analytical+DES energy model over application graphs, YAFS a topology/latency focus.'),
    ('g124', 'g190', 'companion', 'Energy-aware simulators that treat power/energy as the first-class metric: GreenCloud models datacenter server/switch/link power (DVFS/DNS) at packet level, LEAF models fog/edge device energy across thousands of devices.'),
    ('g190', 'g47', 'applies-method-of', "GreenCloud is 'implemented as an ns-2 extension' (endpoint description), running on the ns-2 packet-level engine that g47 documents; g47 is the corpus's ns-2 reference."),
    ('g190', 'g133', 'companion', 'Packet-level datacenter simulators modeling the fabric at packet granularity for different objectives: GreenCloud for energy/DVFS accounting, htsim for transport/congestion-control behavior.'),
    ('g191', 'g126', 'companion', 'Peer large-scale distributed-system simulators with no precedence: PeerSim targets P2P/overlay protocols (gossip, epidemic, churn) with cycle- and event-driven engines; SimGrid targets distributed applications on grid/cloud/HPC platforms.'),
    ('g193', 'g126', 'applies-method-of', "Batsim is a 'SimGrid-based ... simulator' (endpoint description): it runs on the SimGrid kernel and layers an RJMS/job-scheduling abstraction (driven by the external batsched scheduler) on top."),
    ('g192', 'g18', 'applies-method-of', "BigHouse's Statistical Queuing Simulation instantiates queueing-theoretic datacenter-server models, sampling empirical arrival/service distributions - the applied 'queueing theory in action' method of Harchol-Balter's text."),
    ('g192', 'g16', 'references', "BigHouse's statistical server-system models are traceable to the classical queueing-theory foundations in Kleinrock Vol. 1."),
    ('g194', 'g121', 'surveys', "The survey explicitly catalogs 'iFogSim, EdgeCloudSim, YAFS' as the fog/edge simulation tools it compares and taxonomizes."),
    ('g194', 'g122', 'surveys', "Named among the compared tools in the survey's description: 'iFogSim, EdgeCloudSim, YAFS'."),
    ('g194', 'g123', 'surveys', "Named among the compared tools in the survey's description: 'iFogSim, EdgeCloudSim, YAFS'."),
    ('g194', 'g125', 'companion', 'Parallel surveys of fog/edge simulation tooling with no precedence: g209 emphasizes simulators plus deployment-planners (FogTorchPI/Brogi & Forti), g125 catalogs open-source edge simulators and emulators.'),
    ('g12', 'g118', 'prerequisite-of', 'CloudSim is a discrete-event simulator; the DES foundations (event scheduling, random-variate generation, output/statistical analysis) in Banks & Carson are prerequisite to building and trusting CloudSim experiments.'),
    ('g118', 'g126', 'companion', 'Contemporaneous, independently developed toolkits for simulating distributed/cloud computing: CloudSim models cloud datacenters and VM allocation in Java; SimGrid models distributed applications on grid/cloud/HPC platforms in C.'),
    ('g119', 'g118', 'refines', 'CloudSim 7G is an integrated extension of the CloudSim core adding 5G/6G and future-network models, refining the original toolkit for next-generation scenarios.'),
    ('g127', 'g118', 'applies-method-of', 'CloudSimSDN builds on CloudSim to model software-defined cloud datacenters, adding dynamic flow routing and bandwidth allocation.'),
    ('g125', 'g121', 'surveys', 'The open-source edge-computing-simulators survey catalogs iFogSim among the fog/edge tools it compares.'),
    ('g125', 'g122', 'surveys', 'The survey catalogs EdgeCloudSim among the edge simulators it compares.'),
    ('g125', 'g123', 'surveys', 'The survey catalogs YAFS among the open-source fog/edge simulators it compares.'),
    ('g125', 'g124', 'surveys', 'The survey catalogs energy-aware fog/edge simulators, including LEAF, among the open-source tools it compares.'),
    ('g75', 'g74', 'refines', 'RouteNet-Erlang is the Erlang-extended successor in the RouteNet GNN lineage, adding multi-queue scheduling and topology generalization to the original RouteNet model.'),
    ('g76', 'g75', 'supersedes', "RouteNet-Fermi is the later RouteNet-family model, handling non-Markovian traffic and arbitrary scheduling and thereby superseding RouteNet-Erlang's scope."),
    ('g77', 'g76', 'refines', 'RouteNet-Gauss is the hardware-enhanced successor to RouteNet-Fermi in the same RouteNet GNN lineage.'),
    ('g199', 'g75', 'surveys', "The BNN-UPC GNN survey explicitly 'Frames RouteNet-Erlang/Fermi' among its network-modeling use cases."),
    ('g199', 'g76', 'surveys', "The BNN-UPC GNN survey explicitly 'Frames RouteNet-Erlang/Fermi' among its network-modeling use cases."),
    ('g199', 'g74', 'surveys', "The GNN-for-networks survey catalogs the foundational RouteNet model as the origin of the group's network-modeling line."),
    ('g199', 'g84', 'surveys', 'The survey covers graph-based deep-learning models built from captured traffic as a GNN network-modeling use case.'),
    ('g199', 'g80', 'surveys', 'The survey covers the GNN-based network digital twin (TwinNet) as a management/optimization use case.'),
    ('g199', 'g86', 'references', "The survey points to the group's GNN datasets and GNNet Challenge infrastructure used to train and benchmark these models."),
    ('g75', 'g17', 'critiques', "RouteNet-Erlang, by its own account 'outperforming queueing-theory models,' challenges classical queueing-network/Markov-chain analysis for performance prediction."),
    ('g76', 'g17', 'critiques', 'RouteNet-Fermi predicts delay/jitter/loss under realistic non-Markovian traffic, challenging the Markov-chain assumptions underlying classical queueing-network models.'),
    ('g76', 'g25', 'references', "RouteNet-Fermi's emphasis on realistic non-Markovian traffic echoes the empirically demonstrated failure of Poisson/Markovian traffic modeling."),
    ('g196', 'g195', 'supersedes', "m4 is the fully-learned flow-level simulator succeeding m3's hybrid fluid+ML estimator on the same data-center latency task (~100x vs 4-8x speedup)."),
    ('g195', 'g78', 'companion', 'm3 and MimicNet are sibling ML approaches to fast data-center network performance estimation.'),
    ('g196', 'g79', 'companion', 'm4 and DeepQueueNet are parallel fully-learned network simulators aimed at scalable, generalized performance estimation.'),
    ('g196', 'g42', 'critiques', 'm4 argues that learned flow-level simulation can replace packet-level DES such as ns-3, which does not scale to large data-center networks.'),
    ('g81', 'g42', 'applies-method-of', 'ns3-gym wraps the ns-3 packet-level simulator as an OpenAI Gym environment, using ns-3 as its underlying simulation engine.'),
    ('g82', 'g81', 'supersedes', "ns3-ai replaces ns3-gym's socket bridge with shared memory, its note reporting '50-100x faster inter-process data exchange than ns3-gym's ZeroMQ.'"),
    ('g82', 'g42', 'applies-method-of', 'ns3-ai bridges the ns-3 simulator to Python AI (DL/RL) frameworks via a shared-memory interface.'),
    ('g197', 'g81', 'companion', 'NetworkGym and ns3-gym are sibling RL-environment frameworks exposing network simulation to reinforcement-learning agents.'),
    ('g197', 'g42', 'applies-method-of', "NetworkGym's high-fidelity full-stack RL environments run on the ns-3 simulation backend."),
    ('g198', 'g12', 'applies-method-of', 'Differentiable DES builds on the discrete-event system simulation paradigm, smoothing its event dynamics to make the simulator differentiable.'),
    ('g198', 'g85', 'companion', 'Both make network simulation differentiable to enable gradient-based control/optimization — queueing-network control here, traffic engineering there.'),
    ('g198', 'g17', 'references', 'Differentiable DES targets control of queueing networks, the objects studied by classical queueing-network theory.'),
    ('g60', 'g81', 'companion', "Pantheon (a 'training ground') and ns3-gym (a 'playground') are sibling ML-in-networking training environments: real-path emulation versus RL-in-simulation."),
    ('g80', 'g74', 'applies-method-of', 'TwinNet builds a network digital twin using the RouteNet GNN as its underlying performance model.'),
    ('g84', 'g74', 'applies-method-of', 'The captured-traffic graph deep-learning model instantiates the RouteNet GNN approach on measured, real traffic.'),
    ('g79', 'g78', 'companion', 'DeepQueueNet and MimicNet are parallel ML-based network performance estimators targeting scalable data-center/network prediction.'),
    ('g92', 'g76', 'references', 'The data-driven digital-twin performance-modeling perspective builds on learned GNN network models such as RouteNet-Fermi as its modeling engine.'),
    ('g200', 'g41', 'applies-method-of', 'Hypatia pairs its satgenpy constellation/routing generator with "an ns-3 packet-level engine" as its simulation core, i.e. it instantiates the ns-3 model library.'),
    ('g201', 'g200', 'companion', "StarPerf (analytical constellation-abstraction estimates of area-to-area latency/throughput/coverage) is the analytical sibling to Hypatia's packet-level ns-3 approach; both target the same emerging LEO mega-constellations."),
    ('g202', 'g201', 'companion', 'SILLEO-SCNS and StarPerf are both standalone LEO constellation simulators that derive metrics from shortest-path/analytical abstractions (Dijkstra ISL latency) rather than a packet-level engine; parallel analytical tools.'),
    ('g203', 'g44', 'applies-method-of', 'OS3 is a "OMNeT++/INET open-source satellite simulator": it runs on and uses the OMNeT++ discrete-event simulation environment (with INET) as its engine.'),
    ('g204', 'g41', 'part-of', 'Title labels SNS3 an "ns-3 satellite module"; it is literally a module inside the ns-3 model library implementing DVB-S2/RCS2 links.'),
    ('g204', 'g206', 'companion', 'Both are Magister Solutions system-level satellite/NTN simulators (SNS3: DVB-S2/RCS2 ns-3 module; g226: 5G-NR NTN system simulator) — sibling tools from the same developer group.'),
    ('g205', 'g39', 'applies-method-of', 'StarryNet is a Docker-container emulation framework running real network stacks; it instantiates the container-based network-emulation methodology that g39 establishes for reproducible experiments.'),
    ('g206', 'g103', 'refines', "Per the paper, the Magister 5G-NTN system-level simulator is built as a 5G NTN extension of ns-3's 5G-LENA (NR) module, adding 3GPP TR 38.811/38.821 channel and orbital-geometry models — later work in the 5G-LENA lineage."),
    ('g207', 'g54', 'applies-method-of', 'xeoverse is a "Mininet/VM real-time simulator": it models satellites, terminals and ground stations as lightweight hosts inside Mininet, using the Network-in-a-Laptop prototyping engine.'),
    ('g207', 'g200', 'evaluates', "xeoverse's evaluation benchmarks total simulation time against Hypatia (reported ~2.9x faster), positioning its real-time engine against Hypatia's packet-level simulator on the same mega-constellation workloads."),
    ('g207', 'g205', 'evaluates', 'xeoverse benchmarks against StarryNet (reported ~40x faster) and reports that StarryNet cannot scale to large mega-constellations, empirically comparing the two emulation platforms.'),
    ('g208', 'g203', 'refines', 'leosatellites is described as the model that "extends OS3 ported to INET 4.3" and validates against FCC-filed constellations — the finer, later work in the OS3 OMNeT++ lineage.'),
    ('g208', 'g46', 'applies-method-of', 'leosatellites is "ported to INET 4.3"; it runs on and uses the INET framework\'s protocol/model stack as its base.'),
    ('g209', 'g200', 'surveys', 'The LEO satellite networking survey catalogs Hypatia among the LEO simulation platforms used for routing/topology and ISL experimentation.'),
    ('g209', 'g201', 'surveys', 'The survey covers StarPerf as an analytical mega-constellation performance-characterization tool within its treatment of LEO simulation methodology.'),
    ('g209', 'g202', 'surveys', 'The survey catalogs SILLEO-SCNS among standalone LEO constellation simulators for ISL/ground-link design and shortest-path latency.'),
    ('g209', 'g205', 'surveys', 'The survey references StarryNet as a container-based ISTN emulation/digital-twin platform for LEO networking experiments.'),
    ('g209', 'g207', 'surveys', 'The survey catalogs xeoverse as a real-time large-scale LEO mega-constellation simulation platform.'),
    ('g107', 'g206', 'surveys', 'The comprehensive 6G-simulators survey includes the Magister 5G/NR NTN system-level simulator within its NTN simulator scope.'),
    ('g107', 'g200', 'surveys', 'The 6G-simulators survey catalogs Hypatia as a LEO/NTN packet-level simulator relevant to space-terrestrial 6G evaluation.'),
    ('g108', 'g102', 'evaluates', 'Title "Comparative Analysis of Three Open-Source 5G Simulation Tools (Simu5G, ...)" — the comparative study empirically benchmarks Simu5G against the other tools.'),
    ('g108', 'g103', 'evaluates', "The three-tool comparative analysis of open-source 5G simulators empirically compares ns-3's 5G-LENA alongside Simu5G."),
    ('g103', 'g41', 'part-of', '5G-LENA is the CTTC NR simulator built on and distributed for ns-3 — a component/extension of the ns-3 model ecosystem.'),
    ('g102', 'g44', 'applies-method-of', 'Titled "Simu5G — An OMNeT++ Library for End-to-End Performance Evaluation of 5G"; it is a 5G library within the OMNeT++/INET simulation ecosystem.'),
    ('g117', 'g41', 'part-of', 'Titled "ns-3 mmWave module"; it is an ns-3 module extending the model library with mmWave PHY/MAC (relevant to Ka/mmWave NTN links).'),
    ('g218', 'g223', 'prerequisite-of', 'The Anick-Mitra-Sondhi fluid queue (buffer fed by on/off exponential sources, solved by spectral/ODE decomposition) is the foundational fluid-flow model whose coupled-ODE machinery the Misra-Gong-Towsley TCP/AQM fluid model builds on; understand it first.'),
    ('g224', 'g223', 'applies-method-of', "Gu-Liu-Towsley's hybrid simulation uses the Misra-Gong-Towsley TCP/AQM coupled-ODE fluid model as its fluid component, time-stepping it alongside event-driven packet simulation."),
    ('g222', 'g220', 'formalizes', 'Multilevel-splitting theory derives efficiency conditions and near-optimal splitting factors, giving the rigorous mathematical analysis of the RESTART importance-splitting heuristic.'),
    ('g221', 'g219', 'surveys', "Heidelberger's classic rare-event survey catalogs the failure-biasing importance-sampling approach for highly dependable Markovian models introduced by this unified framework."),
    ('g225', 'g219', 'surveys', 'The Juneja-Shahabuddin survey catalogs failure-biasing importance sampling for dependability/reliability models, including this canonical unified Markovian framework.'),
    ('g225', 'g220', 'surveys', 'The survey covers the importance-splitting family, with RESTART as the canonical splitting technique for network buffer-overflow/cell-loss estimation.'),
    ('g225', 'g222', 'surveys', 'The survey covers multilevel splitting and its efficiency analysis among the recent advances in splitting-based rare-event estimation.'),
    ('g225', 'g221', 'refines', "Juneja-Shahabuddin (2006) is the later, broader survey extending Heidelberger's 1995 rare-event survey with a decade of advances: multilevel splitting and heavy-tailed importance sampling."),
    ('g227', 'g219', 'subsumes', 'The Rubino-Tuffin edited volume gathers the rare-event Monte Carlo methods, including failure-biasing importance sampling for dependability, into one comprehensive reference.'),
    ('g227', 'g220', 'surveys', 'The Rubino-Tuffin book consolidates the splitting family, with RESTART, within its treatment of rare-event Monte Carlo methods.'),
    ('g227', 'g222', 'surveys', 'The book gathers multilevel-splitting theory among the splitting methods it consolidates for dependability and telecommunications applications.'),
    ('g227', 'g225', 'companion', 'The Rubino-Tuffin book (2009) and the Juneja-Shahabuddin survey (2006) are the two standard comprehensive references for rare-event simulation, parallel treatments of the same field with no precedence.'),
    ('g226', 'g218', 'references', 'The Benaim-Le Boudec mean-field limit derives a deterministic ODE description for N interacting objects, generalizing to interacting populations the fluid/deterministic-limit modeling philosophy pioneered by the Anick-Mitra-Sondhi fluid queue.'),
    ('g226', 'g223', 'companion', 'Both replace a large stochastic network with a deterministic ODE description: the mean-field interaction limit and the Misra-Gong-Towsley TCP/AQM fluid model are parallel fluid-limit routes to scalable network modeling.'),
    ('g228', 'g40', 'references', "g250 is by its own framing 'part of the movement that established ACM Artifact Review and Badging,' empirically assessing artifact availability/reproducibility across four ACM networking venues against that badging standard."),
    ('g228', 'g36', 'references', "This artifact/reproducibility survey extends the credibility-of-network-simulation critique (Pawlikowski's credibility work) into the artifact-availability era, quantifying reproducibility empirically."),
    ('g236', 'g229', 'prerequisite-of', "Baier-Katoen's textbook (transition systems, temporal logics, probabilistic/CTMC model checking) is the foundation to read before PRISM, whose DTMC/CTMC/MDP/PTA verification instantiates that theory."),
    ('g236', 'g230', 'prerequisite-of', 'Understand the probabilistic model-checking foundations (DTMC/CTMC/MDP, LTL/PCTL) taught here before using Storm, a probabilistic model checker built on the same theory.'),
    ('g236', 'g231', 'prerequisite-of', "The transition-system, temporal-logic and reachability foundations in this textbook underpin UPPAAL's timed-automata model checking; read them first."),
    ('g236', 'g235', 'prerequisite-of', 'The LTL/automata-theoretic explicit-state model-checking algorithms SPIN implements are developed in this textbook; read it before the SPIN reference manual.'),
    ('g236', 'g237', 'prerequisite-of', 'Statistical model checking presupposes the model-checking problem, temporal logics and (probabilistic) semantics defined in this foundational text.'),
    ('g236', 'g238', 'prerequisite-of', 'This applications survey presumes the CTMC/PTA probabilistic model-checking foundations that Principles of Model Checking establishes.'),
    ('g230', 'g229', 'supersedes', 'Storm is the modern high-performance successor to PRISM: it consumes PRISM/JANI models but outperforms PRISM on large DTMC/CTMC/MDP instances, replacing it for demanding verification.'),
    ('g232', 'g229', 'refines', "PRISM-games 3.0 'Extends the PRISM framework to turn-based and concurrent stochastic multi-player games' with equilibria and time, a finer extension in the PRISM lineage."),
    ('g233', 'g230', 'companion', 'The Modest Toolset and Storm are parallel modern quantitative model checkers interoperating through the JANI model-exchange format, with no precedence between them.'),
    ('g234', 'g237', 'applies-method-of', 'UPPAAL-SMC instantiates statistical model checking (simulation plus hypothesis testing), the method g259 surveys, applied to networks of priced/stochastic timed automata.'),
    ('g234', 'g231', 'part-of', "g256 is 'the statistical model checking engine of UPPAAL' - a component/mode of the UPPAAL tool represented by its tutorial (g253)."),
    ('g235', 'g231', 'companion', 'SPIN and UPPAAL are the two canonical model checkers for concurrent systems - SPIN for explicit-state untimed PROMELA, UPPAAL for networks of timed automata - parallel workhorses with no precedence.'),
    ('g238', 'g229', 'applies-method-of', "The survey demonstrates 'probabilistic model checking (via PRISM and probabilistic timed automata)' on real communication protocols, instantiating PRISM's engine."),
    ('g229', 'g17', 'references', "PRISM's CTMC steady-state/transient verification computes the same Markov-chain performance measures treated analytically in Queueing Networks and Markov Chains; the tools are complementary."),
    ('g225', 'g16', 'references', "Rare-event simulation targets the buffer-overflow and tail probabilities of the queueing systems whose exact theory is developed in Kleinrock's Queueing Systems, Vol. 1."),
    ('g224', 'g35', 'references', "Hybrid fluid/packet simulation is motivated by the scalability limits of packet-level Internet simulation articulated in 'Difficulties in Simulating the Internet'; fluid components cut the event load."),
    ('g237', 'g225', 'references', 'Statistical model checking of low-probability (rare) properties must borrow the importance-sampling and splitting techniques surveyed in this rare-event reference to remain statistically efficient.'),
    ('g234', 'g220', 'references', 'UPPAAL-SMC integrates importance-splitting (RESTART-style level crossing) to estimate rare/low-probability properties of stochastic timed automata efficiently.'),
    ('g233', 'g237', 'applies-method-of', "The Modest Toolset's 'modes' simulator is a statistical-model-checking engine, instantiating the SMC method that g259 surveys."),
    ('g28', 'g218', 'references', 'Stochastic network calculus bounds the backlog/buffer-overflow distributions for bursty on/off sources that the Anick-Mitra-Sondhi fluid queue first solved exactly, generalizing that statistical-multiplexing analysis to networks.'),
]
