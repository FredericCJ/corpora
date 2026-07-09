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
