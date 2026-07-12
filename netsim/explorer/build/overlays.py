# -*- coding: utf-8 -*-
"""EDITORIAL overlay layer — maintainer-curated typed relations over the parsed corpus.

Unlike everything else in data/, these relations are NOT stated in the reports. They are
deliberate editorial judgment (requested by the corpus maintainer, authored 2026-07-10), in the
same epistemic class as the SWE explorer's EDITORIAL edges and the calculus explorer's JUDGMENT
edges: every edge carries a one-line rationale, every view that renders them says EDITORIAL, and
build.py machine-checks membership, acyclicity, and level monotonicity before emission.

Node ids are POST-merge explorer ids (g<item> / m<item>): re-check against data/corpus.json when
the reports gain entries. Overlays deliberately cover a curated subset, not all 281 entries —
they are reading maps, not a re-tagging of the corpus.
"""

PROVENANCE = ('EDITORIAL overlay — maintainer-curated 2026-07-10; not stated in the source '
              'reports. Every edge carries its rationale; treat as reading guidance, not corpus fact.')

OVERLAYS = [
    # ────────────────────────── overlay 1: didactic, ground-up ──────────────────────────
    dict(
        id='didactic',
        label='Didactic — ground up',
        edgeKind='read-before',
        semantic='A learning order over a curated subset: levels run from easiest-to-apprehend '
                 'entry points to research-frontier material; an edge s→t means "understanding s '
                 'first makes t substantially easier".',
        question='In what order do I read my way from “what is network simulation?” to the '
                 'frontier — with the multi-station scheduling goal on the main line?',
        levels=[
            dict(key='d0', label='First contact', note='Plain-language entry points — what network simulation is and looks like.'),
            dict(key='d1', label='First models & primers', note='First executable models and the gentlest textbooks.'),
            dict(key='d2', label='Theory cores', note='The load-bearing theory: queueing, DES/DEVS, methodology standards, RM/EDF.'),
            dict(key='d3', label='Build multi-station models', note='The tooling level: SimEvents/SoC/TrueTime/wireless stacks and their scheduling examples.'),
            dict(key='d4', label='Methodology mastery', note='Validity, credibility, control–scheduling co-design, deterministic calculi.'),
            dict(key='d5', label='Frontier & scale', note='PADS, learned simulation, digital twins, TSN, FMI co-simulation research.'),
        ],
        members={
            # d0
            'm19': 'd0', 'm7': 'd0', 'm2': 'd0', 'm24': 'd0',
            # d1
            'm1': 'd1', 'm4': 'd1', 'm8': 'd1', 'g18': 'd1', 'g19': 'd1', 'g12': 'd1', 'g15': 'd1',
            # d2
            'g16': 'd2', 'g9': 'd2', 'g11': 'd2', 'g20': 'd2', 'g166': 'd2', 'g168': 'd2', 'g5': 'd2', 'g10': 'd2',
            # d3
            'm10': 'd3', 'm65': 'd3', 'm66': 'd3', 'm68': 'd3', 'm69': 'd3', 'm73': 'd3', 'm3': 'd3',
            'm5': 'd3', 'm74': 'd3', 'm62': 'd3', 'm63': 'd3', 'm70': 'd3', 'm16': 'd3', 'm18': 'd3',
            'g41': 'd3', 'g44': 'd3',
            # d4
            'g38': 'd4', 'g35': 'd4', 'g36': 'd4', 'g167': 'd4', 'g170': 'd4', 'g171': 'd4',
            'g164': 'd4', 'g163': 'd4', 'g26': 'd4', 'g173': 'd4', 'm81': 'd4', 'm39': 'd4', 'm75': 'd4',
            # d5
            'g64': 'd5', 'g66': 'd5', 'g29': 'd5', 'g74': 'd5', 'g78': 'd5', 'g87': 'd5', 'g105': 'd5',
            'g176': 'd5', 'm80': 'd5', 'm77': 'd5', 'm78': 'd5', 'm79': 'd5', 'g175': 'd5',
        },
        edges=[
            ('m19', 'm2', 'from what network simulation is to the first executable DES model'),
            ('m19', 'm24', 'vocabulary before the hands-on wireless exercises'),
            ('m7', 'm2', 'vendor positioning before the getting-started semantics'),
            ('m19', 'g12', 'why simulate, then the classical textbook'),
            ('m2', 'm4', 'entity/event semantics, then the canonical M/M/1'),
            ('m2', 'm1', 'guided intro before the full block/doc tree'),
            ('m2', 'm70', 'block semantics before partition-scheduling infrastructure'),
            ('m24', 'm16', 'workshop exercises before the simulator API'),
            ('m4', 'g16', 'watch a queue behave before deriving it'),
            ('g19', 'g18', 'probability foundations before queueing pedagogy'),
            ('g18', 'g16', 'motivated queueing before the rigorous origin text'),
            ('g15', 'g20', 'the classic performance triad before rigorous methodology'),
            ('g12', 'g11', 'teaching text before the methodology standard'),
            ('g12', 'g9', 'simulation practice before DES system theory'),
            ('g12', 'g10', 'simulation practice before formal net models'),
            ('g12', 'g41', 'general DES before a packet-level simulator'),
            ('g12', 'g44', 'general DES before the OMNeT++ ecosystem'),
            ('g9', 'g5', 'DES automata view before the DEVS formalization'),
            ('m1', 'm10', 'use SimEvents before extending its framework'),
            ('m1', 'm65', 'core queues/servers before the multicore scheduler model'),
            ('m1', 'm68', 'core blocks before custom resource arbitration'),
            ('m1', 'm69', 'core blocks before the job-shop plant'),
            ('m4', 'm65', 'one queue before multi-core task dispatch'),
            ('m8', 'm73', 'state machines before a full contention MAC'),
            ('m3', 'm73', 'wired CSMA/CD before wireless CSMA/CA'),
            ('m5', 'm74', 'a taste of network-induced delay before the RTOS+network kernel'),
            ('g166', 'm65', 'priority-scheduling math before the shipped scheduler'),
            ('g166', 'm63', 'RM/EDF before Task Manager priorities'),
            ('g166', 'm70', 'RM theory before Simulink rate-monotonic multitasking'),
            ('g166', 'g168', 'the origin paper before the systematic textbook'),
            ('g166', 'g167', 'the origin paper before the historical synthesis'),
            ('g168', 'm74', 'the scheduling textbook before the kernel that simulates it'),
            ('m62', 'm63', 'product concepts before the task-execution example'),
            ('m65', 'm66', 'shipped policy before authoring your own'),
            ('m18', 'm16', 'product overview before the scheduler object API'),
            ('m73', 'm16', 'hand-built MAC before the packaged multinode stack'),
            ('g20', 'g38', 'measurement rigor before V&V frameworks'),
            ('g11', 'g38', 'methodology standard before the V&V discipline'),
            ('g35', 'g36', 'the validity problem before the credibility audit'),
            ('g36', 'g38', 'credibility failures motivate systematic V&V'),
            ('g167', 'g170', 'the scheduling canon before co-design algorithms'),
            ('g171', 'g170', 'single-loop feedback scheduling before feedback-feedforward'),
            ('g170', 'm39', 'co-design questions before the jitter-analysis toolbox'),
            ('g163', 'g164', 'the seminal trigger rule before the tutorial'),
            ('g164', 'g175', 'event-triggered basics before weakly-hard co-design'),
            ('g26', 'g173', 'network calculus before its real-time sibling'),
            ('g173', 'm81', 'RTC theory before the MATLAB toolbox'),
            ('m74', 'm75', 'use TrueTime before the thesis behind it'),
            ('m74', 'g176', 'co-simulation practice before FMI step semantics'),
            ('m74', 'm77', 'the kernel before the modular scheduler/network bundle'),
            ('g176', 'm80', 'FMI semantics before the concrete ns-3 bridge'),
            ('g41', 'm80', 'ns-3 before its FMU export'),
            ('g44', 'g29', 'the OMNeT++ ecosystem before the TSN modeling literature'),
            ('g26', 'g29', 'calculus bounds before TSN’s modeling survey'),
            ('g64', 'g66', 'the PADS survey before the modern agenda'),
            ('g74', 'g78', 'GNN network models before hybrid learned simulation'),
            ('g66', 'g87', 'the online-simulation agenda before digital-twin surveys'),
            ('m16', 'g105', 'packaged wireless system simulation before GPU-native differentiable PHY'),
            ('m66', 'm78', 'custom SimEvents schedulers before the multicore memory-contention study'),
            ('m10', 'm79', 'the extensible framework before timing-injection techniques'),
        ],
    ),
    # ─────────────────── overlay 2: theory → applied transitive specialization ───────────────────
    dict(
        id='specialization',
        label='Theory → applied',
        edgeKind='specialized-by',
        semantic='Transitive specialization chains over a curated subset: THEORY is operationalized '
                 'by METHODOLOGY, embodied in FRAMEWORKS & TOOLS, and instantiated in APPLIED models '
                 'and studies; an edge s→t means "t specializes s toward application". Stage-skipping '
                 'edges are allowed where the lineage is direct.',
        question='How does each theory become a runnable multi-station model — and which chains '
                 'stop short of an applied endpoint?',
        levels=[
            dict(key='s0', label='Theory', note='Origin results and formalisms: queueing, DEVS/DES, RM/EDF, event triggering, fluid models, (network/real-time) calculus.'),
            dict(key='s1', label='Methodology & analysis', note='Methodology standards, V&V/credibility, co-design algorithms, compositional analysis, NCS surveys.'),
            dict(key='s2', label='Frameworks & tools', note='The engines: SimEvents, TrueTime, SoC Blockset, wireless simulators, ns-3/OMNeT++, analysis toolboxes.'),
            dict(key='s3', label='Applied models & studies', note='Runnable examples and published studies that instantiate the chain.'),
        ],
        members={
            # s0
            'g16': 's0', 'g5': 's0', 'g9': 's0', 'g24': 's0', 'g25': 's0', 'g166': 's0',
            'g163': 's0', 'g165': 's0', 'm36': 's0', 'g26': 's0', 'g173': 's0',
            # s1
            'g11': 's1', 'g12': 's1', 'g38': 's1', 'g36': 's1', 'g171': 's1', 'g170': 's1',
            'g164': 's1', 'g167': 's1', 'g168': 's1', 'g174': 's1', 'g27': 's1', 'm37': 's1',
            'm38': 's1', 'g176': 's1', 'g7': 's1', 'g159': 's1', 'g162': 's1', 'g175': 's1',
            # s2
            'm1': 's2', 'm10': 's2', 'm74': 's2', 'm39': 's2', 'm40': 's2', 'm77': 's2',
            'm81': 's2', 'm62': 's2', 'm70': 's2', 'm16': 's2', 'm29': 's2', 'g41': 's2',
            'g44': 's2', 'g103': 's2', 'm49': 's2', 'm80': 's2',
            # s3
            'm4': 's3', 'm5': 's3', 'm65': 's3', 'm66': 's3', 'm68': 's3', 'm69': 's3',
            'm63': 's3', 'm64': 's3', 'm71': 's3', 'm72': 's3', 'm13': 's3', 'm78': 's3',
            'm43': 's3', 'm46': 's3', 'm30': 's3', 'm56': 's3', 'g104': 's3', 'g32': 's3',
            'g33': 's3', 'g4': 's3',
        },
        edges=[
            # queueing → methodology → DES engines → validated example
            ('g16', 'g11', 'queueing theory embedded in the DES methodology standard'),
            ('g16', 'g12', 'queueing theory as the textbook’s analytical backbone'),
            ('g16', 'm4', 'M/M/1 theory validated directly by the shipped SimEvents example'),
            ('g24', 'g11', 'traffic self-similarity constrains input modeling'),
            ('g25', 'g11', 'the Poisson failure constrains input modeling'),
            ('g12', 'g41', 'DES methodology embodied in the packet-level simulator'),
            ('g12', 'g44', 'DES methodology embodied in the OMNeT++ framework'),
            # DEVS lineage
            ('g5', 'g7', 'the DEVS formalism operationalized as practitioner method'),
            ('g7', 'g4', 'the practitioner method instantiated in a DEVS network study'),
            # DES theory → SimEvents lineage → scheduling examples & studies
            ('g9', 'm10', 'DES semantics operationalized as the Simulink DES framework'),
            ('m1', 'm4', 'the engine instantiating the canonical queue'),
            ('m1', 'm5', 'the engine instantiating the CAN/ABS delay study'),
            ('m1', 'm65', 'the engine instantiating the multicore scheduler model'),
            ('m1', 'm68', 'the engine instantiating custom resource arbitration'),
            ('m1', 'm69', 'the engine instantiating the job-shop plant'),
            ('m10', 'm66', 'the extensibility framework enabling custom scheduler policies'),
            ('m10', 'm13', 'the framework instantiated in the Mcity ITS study'),
            ('m10', 'm78', 'the framework instantiated in the multicore memory-contention study'),
            # real-time scheduling lineage
            ('g166', 'g167', 'the origin result consolidated into the scheduling canon'),
            ('g166', 'g168', 'the origin result systematized as a textbook'),
            ('g166', 'g174', 'schedulability theory extended to compositional system-level analysis'),
            ('g166', 'm70', 'rate-monotonic theory shipped as Simulink multitasking semantics'),
            ('g166', 'm65', 'priority-scheduling theory instantiated by the shipped scheduler example'),
            ('g167', 'm62', 'the scheduling canon productized in the vendor SoC task stack'),
            ('g167', 'm77', 'the scheduling canon modularized as scheduler/task/message S-functions'),
            ('g168', 'm74', 'textbook policies (RM/EDF) implemented in the TrueTime kernel'),
            ('m62', 'm63', 'the product instantiated by the task-execution example'),
            ('m62', 'm64', 'the product instantiated by the HW/SW streaming datapath example'),
            # control–scheduling co-design lineage (Lund school)
            ('g165', 'g164', 'event-based sampling origin folded into the ET/ST tutorial'),
            ('g163', 'g164', 'the trigger rule folded into the canonical tutorial'),
            ('g171', 'g170', 'the single-loop feedback scheduler refined feedback-feedforward'),
            ('g170', 'm74', 'feedback-scheduling algorithms exercised in TrueTime stations'),
            ('g170', 'm39', 'co-design analysis needs met by the jitter-performance toolbox'),
            ('m39', 'm40', 'the jitter toolbox succeeded by transient-performance analysis'),
            ('m74', 'm43', 'the kernel extended into the wireless-NCS toolchain'),
            ('m74', 'm46', 'TrueTime-class control models coupled to industrial-wireless co-simulation'),
            ('g162', 'g175', 'modern NCS co-design specialized to the weakly-hard branch'),
            ('g159', 'g162', 'the foundational NCS taxonomy carried into the modern survey'),
            ('g159', 'm5', 'the NCS delay taxonomy instantiated by the CAN/ABS example'),
            # calculi
            ('g26', 'g27', 'the calculus made algorithmic and tool-oriented'),
            ('g27', 'g32', 'deterministic calculus applied to TSN delay analysis'),
            ('g173', 'm81', 'real-time calculus implemented as the MATLAB RTC toolbox'),
            # fluid/AQM lineage (no applied endpoint in-corpus — honest gap, see U-register)
            ('m36', 'm37', 'the fluid model used for AQM controller design'),
            ('m37', 'm38', 'design results consolidated in the congestion-control monograph'),
            # credibility → fidelity/calibration
            ('g36', 'g38', 'the credibility crisis answered by systematic V&V'),
            ('g36', 'm49', 'the credibility crisis answered by a reproducibility-first simulator suite'),
            ('g38', 'g104', 'V&V discipline instantiated as calibration against 3GPP references'),
            ('g36', 'g33', 'credibility concerns instantiated as hardware-aligned fidelity work'),
            ('g44', 'g33', 'the framework specialized by the TSN fidelity study'),
            # wireless system-level chains
            ('m16', 'm71', 'the simulator instantiated by the FDD MAC-scheduler evaluation'),
            ('m16', 'm72', 'the simulator extended by the custom-scheduler plug-in example'),
            ('g103', 'g104', 'the NR simulator specialized by its calibration study'),
            ('m29', 'm30', 'the scenario engine instantiated by the multi-hop link example'),
            ('m29', 'm56', 'the toolbox used as system-of-record in satellite networking studies'),
            # FMI / co-simulation bridges
            ('g176', 'm80', 'FMI step semantics realized in the ns-3 FMU export'),
            ('g41', 'm80', 'the packet simulator wrapped as an FMI subordinate'),
        ],
    ),
]


# ─────────── breadth extensions (2026-07 typed-relations wave) — new nodes woven into the maps ───────────
# Generated by the overlay-extension workflow; validated (in-corpus, non-quarantined, level-monotone,
# acyclic via build PHASE 3.5). Merged into OVERLAYS at import so the build sees one extended structure.
_DID_ADD = {'g177': 'd3', 'g179': 'd3', 'g180': 'd3', 'g181': 'd3', 'g183': 'd5', 'g189': 'd3', 'g191': 'd3', 'g194': 'd5', 'g196': 'd5', 'g199': 'd5', 'g200': 'd5', 'g203': 'd3', 'g209': 'd4', 'g210': 'd5', 'g211': 'd5', 'g212': 'd5', 'g216': 'd5', 'g217': 'd5', 'g218': 'd2', 'g225': 'd4', 'g226': 'd4', 'g236': 'd2'}
_DID_EDGES = [
    ('g41', 'g177', 'after a core simulator like ns-3, meet the integrated hardware-in-the-loop testbed'),
    ('g177', 'g179', "from Emulab's heavyweight testbed to lightweight container-based labs"),
    ('g179', 'g180', 'from Kathará teaching labs to declarative vendor-NOS containerlab topologies'),
    ('m18', 'g181', 'after wireless toolbox modeling, emulate software-defined Wi-Fi stations hands-on'),
    ('g179', 'g183', 'from container labs to the virtual-time mechanism that scales them to high-speed links'),
    ('g64', 'g183', "grasp PDES virtual time before TimeKeeper's Linux time-dilation realization"),
    ('g64', 'g210', 'the reverse-computation rollback method builds directly on PDES foundations'),
    ('g64', 'g217', 'conservative null-message synchronization deepens the PDES synchronization foundation'),
    ('g210', 'g216', 'reverse computation is the enabling method for the ~2M-core Time Warp run'),
    ('g64', 'g216', 'the landmark strong-scaling study realizes PDES at extreme scale'),
    ('g66', 'g211', 'a canonical large-scale MPI-parallel network simulator answering the scale challenges surveyed'),
    ('g66', 'g212', 'parallelizing the sequential ns simulator addresses distributed-simulation research challenges'),
    ('g9', 'g189', 'master DES foundations before building fog/edge multi-station models in iFogSim2'),
    ('g9', 'g191', "understand event-driven DES before PeerSim's large-scale P2P/overlay models"),
    ('m10', 'g194', 'grasp an extensible DES framework before the comparative fog/edge simulator survey'),
    ('g189', 'g194', 'study the concrete iFogSim2 tool before the survey that taxonomizes it against peers'),
    ('g74', 'g199', 'RouteNet is the seminal GNN network model this survey catalogs and generalizes'),
    ('g74', 'g196', 'extends GNN-based network modeling into a fully learned flow-level simulator'),
    ('g199', 'g196', 'the learned flow-level simulator exemplifies the GNN methods this survey systematizes'),
    ('g44', 'g203', 'OS3 is the OMNeT++/INET satellite module you build orbital scenarios with after learning OMNeT++'),
    ('g35', 'g209', 'move from general internet-simulation difficulties to a focused survey of the LEO networking landscape'),
    ('g209', 'g200', 'survey the LEO networking field before running the Hypatia mega-constellation simulator'),
    ('g203', 'g200', 'progress from single-tool satellite modeling in OS3 to full-scale packet-level constellation simulation'),
    ('g41', 'g200', 'Hypatia scales the ns-3 packet-level engine up to complete LEO constellations'),
    ('g16', 'g218', 'the fluid data-handling model builds directly on classical queueing theory'),
    ('g9', 'g236', 'model-checking theory rests on discrete-event / transition-system foundations'),
    ('g11', 'g225', 'rare-event simulation is advanced methodology extending general simulation analysis'),
    ('g218', 'g226', 'mean-field ODE limits extend the fluid-model approach to large populations of interacting objects'),
]
_SPEC_ADD = {'g177': 's2', 'g178': 's2', 'g179': 's2', 'g180': 's2', 'g181': 's3', 'g182': 's2', 'g183': 's2', 'g184': 's2', 'g185': 's3', 'g186': 's2', 'g187': 's2', 'g188': 's2', 'g189': 's2', 'g190': 's2', 'g191': 's2', 'g192': 's2', 'g193': 's2', 'g194': 's1', 'g195': 's3', 'g196': 's3', 'g197': 's2', 'g198': 's1', 'g199': 's1', 'g200': 's2', 'g201': 's3', 'g202': 's2', 'g203': 's2', 'g204': 's2', 'g205': 's2', 'g206': 's3', 'g207': 's2', 'g208': 's2', 'g209': 's1', 'g210': 's1', 'g211': 's2', 'g212': 's2', 'g213': 's2', 'g214': 's2', 'g215': 's2', 'g216': 's3', 'g217': 's1', 'g218': 's0', 'g219': 's1', 'g220': 's1', 'g221': 's1', 'g222': 's1', 'g223': 's0', 'g224': 's3', 'g225': 's1', 'g226': 's0', 'g227': 's1', 'g228': 's1', 'g229': 's2', 'g230': 's2', 'g231': 's2', 'g232': 's2', 'g233': 's2', 'g234': 's2', 'g235': 's2', 'g236': 's0', 'g237': 's1', 'g238': 's3'}
_SPEC_EDGES = [
    ('g36', 'g177', 'Emulab answers simulation-credibility concerns with a controlled real-node experimental environment'),
    ('g41', 'g178', 'CORE runs ns-3 and real stacks inside emulated nodes, extending the simulator toward live emulation'),
    ('g177', 'g178', "CORE continues Emulab's integrated-testbed lineage as a real-time emulator"),
    ('g177', 'g179', 'Kathará specializes the shared-testbed idea into scalable Docker/Kubernetes labs'),
    ('g179', 'g180', 'containerlab generalizes container-based labbing to declarative vendor-NOS topologies'),
    ('g178', 'g181', 'Mininet-WiFi applies emulated-node techniques to SDN wireless experiments'),
    ('m16', 'g181', 'Mininet-WiFi brings propagation and mobility models to hybrid wireless emulation studies'),
    ('g27', 'g182', 'Kollaps enforces specified end-to-end path delay/bandwidth, applying deterministic path modeling in practice'),
    ('g11', 'g183', 'TimeKeeper realizes accurate virtual-time emulation grounded in simulation-timing analysis'),
    ('g9', 'g217', 'applies discrete-event-system theory to conservative parallel synchronization analysis'),
    ('g9', 'g210', 'applies discrete-event execution semantics to a reversible optimistic rollback method'),
    ('g210', 'g214', 'the reverse-computation technique is realized in an optimistic Time Warp kernel'),
    ('g217', 'g215', 'conservative-vs-optimistic synchronization unified inside a PDES micro-kernel'),
    ('g210', 'g215', 'optimistic state-saving synchronization embodied within the micro-kernel'),
    ('g214', 'g216', 'the Time Warp kernel is scaled to ~2M cores in a strong-scaling study'),
    ('g210', 'g216', 'reverse computation drives the ~504-billion-event PHOLD run'),
    ('g41', 'g211', 'a packet-level network simulator in the ns lineage built for MPI-parallel scale'),
    ('g41', 'g212', 'a framework federating and parallelizing the ns simulator over MPI (PDNS)'),
    ('g217', 'g211', 'conservative synchronization enabling large-scale parallel packet simulation'),
    ('g217', 'g213', 'conservative parallel synchronization applied to a large-scale architecture simulator'),
    ('g5', 'g184', 'applies modeling-and-simulation theory to a cycle-accurate on-chip network model'),
    ('g184', 'g185', 'on-chip/scale-up network modeling extended to distributed DL-training fabric simulation'),
    ('g5', 'g186', 'applies M&S theory to a cycle-accurate DRAM memory-system model'),
    ('g186', 'g187', 'a faster, extensible DRAM simulator succeeding the cycle-accurate DRAMSim2'),
    ('g5', 'g188', 'applies M&S theory to a validated storage-subsystem simulator'),
    ('g194', 'g189', 'iFogSim2 is a concrete fog/edge tool cataloged by the comparative overview'),
    ('g16', 'g192', 'BigHouse specializes queueing theory via Statistical Queuing Simulation of datacenter servers'),
    ('g9', 'g191', 'PeerSim applies event-driven DES to scalable P2P overlay and churn scenarios'),
    ('g9', 'g193', 'Batsim applies DES to HPC/cluster resource-and-job management scheduling'),
    ('g41', 'g190', 'GreenCloud extends the ns-2 packet-level network simulator lineage toward energy-aware datacenters'),
    ('m36', 'g195', 'applies fluid flow-level network modeling, accelerated by an ML surrogate, to data-center tail-latency estimation'),
    ('g199', 'g195', 'ML flow-level estimator instantiating the learned-network-modeling agenda the survey frames'),
    ('g41', 'g196', 'learns a neural surrogate replacing packet/flow-level simulators such as ns-3'),
    ('g199', 'g196', 'realizes the GNN-based network-modeling methodology this survey systematizes'),
    ('g41', 'g197', 'packages ns-3-based full-stack simulation as reinforcement-learning environments (Simulation-as-a-Service)'),
    ('g9', 'g198', 'makes classical discrete-event simulation differentiable for gradient-based policy optimization'),
    ('g16', 'g198', 'differentiable simulation of queueing networks whose theory this text establishes'),
    ('g41', 'g200', 'Hypatia embeds the ns-3 packet-level engine, applied to LEO constellations'),
    ('g41', 'g204', 'SNS3 is an ns-3 module adding DVB-S2/RCS2 satellite links'),
    ('g44', 'g203', 'OS3 is an OMNeT++/INET module specializing the framework for satellite simulation'),
    ('g203', 'g208', 'leosatellites extends OS3 ported to INET 4.3 for LEO constellations'),
    ('g44', 'g208', 'leosatellites builds on the OMNeT++/INET simulation framework'),
    ('g103', 'g206', 'the 5G NTN system simulator extends 5G NR system-level simulation to non-terrestrial per 3GPP TR 38.811/38.821'),
    ('m29', 'g206', 'applies satellite channel/geometry modeling to 5G NR NTN evaluation'),
    ('m29', 'g202', 'SILLEO-SCNS specializes satellite link modeling toward inter-satellite and ground-link design'),
    ('g200', 'g201', 'StarPerf offers an analytical mega-constellation alternative to packet-level LEO simulation for performance characterization'),
    ('g200', 'g205', 'StarryNet reuses constellation topology generation, delivering a container-based ISTN digital twin'),
    ('g200', 'g207', 'xeoverse adopts the precomputed-topology approach for real-time Mininet/VM LEO emulation'),
    ('g209', 'g201', "the survey's mega-constellation research directions are realized in StarPerf's characterization"),
    ('g209', 'g206', "the survey's 3GPP NTN standardization thread is realized in the 5G NTN system simulator"),
    ('g16', 'g218', 'the fluid-queue model specializes classical queueing theory to aggregated on/off sources'),
    ('g218', 'g223', 'the fluid AQM network model applies the fluid-queue framework to TCP window dynamics'),
    ('g218', 'g226', 'mean-field interaction models generalize the fluid ODE limit to N interacting objects'),
    ('g223', 'm37', 'AQM controller design and analysis builds on the fluid model of TCP/AQM'),
    ('g223', 'g224', 'hybrid packet/fluid simulation integrates the fluid AQM model with event-driven packets'),
    ('g11', 'g221', 'rare-event importance sampling specializes general Monte Carlo simulation methodology'),
    ('g221', 'g219', 'the failure-biasing framework is a rare-event IS technique cataloged by the survey'),
    ('g221', 'g220', "RESTART importance splitting is a rare-event acceleration technique within the survey's scope"),
    ('g220', 'g222', 'multilevel-splitting efficiency analysis formalizes the RESTART splitting method'),
    ('g221', 'g225', 'the modern rare-event survey updates and extends the classic importance-sampling tutorial'),
    ('g225', 'g227', 'the edited Monte Carlo reference compiles the rare-event techniques catalogued by the survey'),
    ('g36', 'g228', 'the artifact/reproducibility survey extends the credibility-of-simulation-studies critique'),
    ('g236', 'g229', 'PRISM is a tool implementing probabilistic model-checking theory'),
    ('g236', 'g235', 'SPIN is a tool implementing explicit-state model-checking theory'),
    ('g236', 'g231', 'Uppaal is a tool implementing timed-automata model checking'),
    ('g236', 'g230', 'Storm is a tool implementing modern probabilistic model-checking theory'),
    ('g236', 'g233', 'the Modest toolset implements quantitative (probabilistic/real-time/hybrid) model-checking theory'),
    ('g236', 'g237', 'statistical model checking is a simulation-based alternative to the exact model-checking theory'),
    ('g229', 'g230', 'Storm is a modern successor consuming PRISM/JANI models'),
    ('g229', 'g232', 'PRISM-games extends the PRISM framework to stochastic multi-player games'),
    ('g231', 'g234', 'Uppaal SMC is the statistical model-checking engine built into Uppaal'),
    ('g237', 'g234', 'Uppaal SMC implements the statistical model-checking methodology'),
    ('g229', 'g238', 'the survey demonstrates PRISM/probabilistic model checking applied to communication protocols'),
]
for _ov in OVERLAYS:
    if _ov['id'] == 'didactic':
        _ov['members'].update(_DID_ADD); _ov['edges'].extend(_DID_EDGES)
    elif _ov['id'] == 'specialization':
        _ov['members'].update(_SPEC_ADD); _ov['edges'].extend(_SPEC_EDGES)
