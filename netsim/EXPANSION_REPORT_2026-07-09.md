# Expansion report — Multi-station task & resource scheduling (2026-07-09)

**Target capability.** A MATLAB/Simulink simulation of a computer network with **multiple stations**, where each station executes **tasks** under a **scheduler** — i.e. joint simulation of (a) the network (topology, medium access, latency/loss) and (b) per-station task/resource scheduling (release, preemption, deadlines, server/resource contention). Both a **METHOD** layer (DES/NCS co-design, schedulability, queueing/resource, real-time calculus) and **EXAMPLE** artifacts (shipped MathWorks examples, File Exchange, GitHub, runnable papers) were required.

## 1. What was added

| Corpus | New numbered | New quarantine | New section |
|---|---|---|---|
| GEN (`MS_networks_systems_corpus_v1_0.md`) | **159–176** (18) | **U16–U18** (3) | §16 "Multi-station task & resource scheduling — co-design of network, tasks & resources (METHOD layer)" |
| MAT (`MATLAB_Simulink_network_MS_corpus_v1_0.md`) | **62–81** (20) | — | §8 "Multi-station task & resource scheduling models" |

- **41 new entries** total (38 numbered + 3 quarantine). Corpus grew 241 → **282 nodes**.
- Verification split moved 143/75/22 → **179/78/24** (web/train/unverified): +36 verified[WEB], +3 verified[TRAIN], +2 unverified.
- Build contract updated (the deliberate two-key gate): count assertions `158+15 → 176+18` and `61+8 → 81+8`; sequence ranges `→177 / →82`; `GEN_SECTION_MAP` gained §16 (mapped to the "beyond-the-anchor" column) with the quarantine route renumbered to §17; the hardcoded quarantine-section constants moved (GEN 16→17, MAT 8→9); PHASE-3 section-map bound `≤16→≤17`. `python netsim/explorer/build/build.py` passes clean; the explorer serves on `:8096`, loads with **zero JS errors**, and all five views render the new nodes with correctly-resolved cross-references (e.g. `m74 TrueTime → mentions m41/m42`; `m81 RTC Toolbox → overlaps/mentions g173` the Real-Time-Calculus paper).

## 2. Waves crawled

**Wave 0 (seeds, already in corpus):** MAT §1 SimEvents (esp. item 6, item 10 Li/Mani/Mosterman, item 14 Li/Cassandras); MAT §5 TrueTime 41–42, Jitterbug/JitterTime 39–40, PiccSIM 43, T-Res 47; MAT §2 wirelessNetworkSimulator 16–18; GEN 9 (Cassandras/Lafortune), 11–12 (Law/Banks), 29–34 (TSN schedulability), 150 (WSC).

**Wave 1 (executed):** four parallel scout clusters + first-hand keystone fetches. Hop limit 2 from each seed; frontier log kept in scratch. The wave yielded ~38 in-scope finds — far above the 3-per-wave floor and at the ~40-entry ceiling — so per the stop rule the crawl **halted after Wave 1**. A Wave 2 was not warranted: the highest-value 2-hop neighbours (network calculus, TSN gate-scheduling, WSC/WODES venue nodes) were already in the corpus or surfaced as the same cluster's backward edges.

### Per-cluster yield

| Cluster (edges followed) | In-scope finds | Landed as |
|---|---|---|
| **S1 — MathWorks vendor scheduling stack** (tool doc-tree + linked code) | 16 (15 fetched) | MAT 62–66, 68–73 (SoC Blockset, SimEvents scheduler/resource examples, Schedule Editor, 5G/WLAN MAC schedulers) |
| **S2 — TrueTime / Lund co-design school** (same-authors + forward cites) | 13 | MAT 74–76; GEN 165, 170–172, 175; quarantine U16–U17; resolved MAT U5 (JitterTime = ETFA 2019) |
| **S3 — NCS / event-triggered / schedulability / real-time calculus** (backward refs) | 13 (all Crossref-confirmed) | GEN 159–164, 166–169, 173–174; MAT 81 (RTC Toolbox) |
| **S4 — SimEvents/DES academic + co-sim + FEX/GitHub** (forward cites + code artifacts) | 13 | MAT 67, 77–80; GEN 176; resolved MAT U3 (T-Res = SAC '15, DOI 10.1145/2695664.2695876) |

First-hand fetches (verified[WEB], access date 2026-07-09) grounded the load-bearing keystones directly: SoC Blockset product page + Task Execution + Multicore Execution + Task Manager block; SimEvents "Simulate Scheduler of a Multicore Control System", "Resource Scheduling…", "Job Scheduling…Manufacturing Plant"; 5G "Use Custom Scheduler…" and "NR FDD Scheduling Performance Evaluation". Scout Crossref/dblp confirmations of DOIs/ISBNs are treated as live session verification.

## 3. Hypothesis leads — verdicts

- **SoC Blockset = the exact vendor stack?** *Partly confirmed.* It is the vendor's per-station scheduled-task model (Task Manager: timer/event tasks with period, priority, per-core mapping, preemption, overruns/drops) **plus** on-chip memory/AXI-interconnect timing and contention — but it models **one multicore SoC**, not a multi-station network. It supplies the *station* half with high fidelity; pair it with the network toolboxes or TrueTime for the *network* half. → MAT 62–64.
- **SimEvents shipped resource/job-shop/server-pool examples?** *Confirmed, richly.* → MAT 65–69 (multicore-scheduler control system, custom scheduler, MATLAB-DES resource policy, manufacturing job-scheduling with resource pools, multi-class job routing across service stations).
- **5G/WLAN scheduler-evaluation examples?** *Confirmed.* → MAT 71–72 (RR/PF/best-CQI + custom `nrScheduler`), complementing the WLAN OFDMA example already at MAT 23.
- **Årzén/Cervin/Henriksson co-design + 2015–2026 citing lit?** *Confirmed.* → GEN 165, 170–172, 175 + MAT 74–76; forward-citation review quarantined at U18.
- **Stateflow MAC/TDMA schedulers in multinode Simulink?** *Confirmed.* → MAT 73 (ALOHA/CSMA-CA three-node PHY/MAC with backoff, built in Simulink+Stateflow); TrueTime (MAT 74) supplies TDMA/FDMA/round-robin MAC natively.

## 4. Dead branches (killed to stay in scope)

- **Eker PhD thesis 1999** (Pålsjö/PAL feedback-scheduling groundwork) — no network model; out of the tightest scope.
- **Mcity SimEvents road-traffic ITS** (DEDS 2019, 10.1007/s10626-019-00286-w) — a real Clune/SimEvents forward-cite but road-traffic, not computer-network/task-scheduling.
- **Fuzzy/neural feedback-scheduling spin-offs** — cite TrueTime but don't extend the co-simulation method.
- **Probabilistic model-checking of schedulers (PRISM/UPPAAL/Storm)** — deliberately left as an unexpanded systems-boundary fork (consistent with the GEN report's existing stance).
- **Generic Simulink/Stateflow transceiver marketing pages** — no scheduling/network-scale content.

## 5. Verification discipline & honest gaps

- **verified[WEB] (fetched this session):** all MathWorks doc/example pages I or scout S1 loaded with concrete quoted detail; all GEN NCS/schedulability/RTC/co-design identifiers (Crossref/dblp field-matched today); the TrueTime archive page, Cervin/Henriksson theses (LUP), tres_bundle & ns3-fmi-export GitHub repos, Brandberg & Di Natale File Exchange #66173.
- **verified[TRAIN] (high-confidence, not primary-fetched):** Årzén "A Simple Event-Based PID Controller" 1999 (pre-DOI IFAC — GEN 165); Naderlinger WSC/DATE 2017 timing-block papers (index-confirmed only — MAT 79); **RTC Toolbox** (MAT 81) — its ETH page `mpa.ethz.ch/Rtctoolbox` presented an **expired TLS certificate** at access time and zbmath 403'd, so despite strong corroboration it is tagged TRAIN, not WEB (its underlying method paper, GEN 173, is verified[WEB]).
- **Quarantine (unverified):** U16 Årzén/Cervin/Eker/Sha "An Introduction to Control and Scheduling Co-design" CDC 2000 and U17 Cervin/Eker "The Control Server" ECRTS — real and directly on-target, but no identifier could be grounded; U18 Yusof et al. 2024 co-design review — fetched but an obscure open-access venue with no DOI (verified[WEB]-single-source).
- **Quarantine resolutions (documented, existing entries left byte-stable):** MAT **U3** (T-Res) is now grounded — Cremona, Morelli, Di Natale, "TRES…", ACM SAC 2015, pp. 1940–1947, DOI **10.1145/2695664.2695876** (see MAT 77). MAT **U5** (JitterTime venue) is now grounded — Cervin/Pazzaglia/Barzegaran/Mahfouzi, IEEE **ETFA 2019**, DOI **10.1109/ETFA.2019.8869221**, toolbox `github.com/ControlLTH/JitterTime`.
- **Where recall genuinely thins:** independent third-party **validation** of the young (2023+) MathWorks scheduler stack against real RTOS/hardware traces is essentially absent (a real gap, not a search miss); File Exchange breadth beyond the two academic models grounded; and the pre-DOI IFAC control literature (1999–2005) is hard to identifier-ground.

## 6. TOP 5 entries that most directly enable the model — with a build order

The single most on-target artifact is **TrueTime**: it is the only tool that natively co-simulates *both* per-station RTOS task scheduling *and* a multi-node MAC network inside Simulink. Everything else deepens one half.

1. **TrueTime 2.0** — MAT **74** (with the founding papers MAT 41–42). Preemptive RM/EDF (or user-defined) kernel per node + wired (Ethernet/CAN/TDMA/FDMA/round-robin/switched-Ethernet/FlexRay/PROFINET) and wireless (802.11b, 802.15.4) network blocks + continuous plant. **This is the reference realization of the target capability — start the build here.**
2. **SimEvents "Simulate Scheduler of a Multicore Control System"** — MAT **65** (+ "Develop Custom Scheduler" MAT **66**, and the method paper Li/Mani/Mosterman/Hübscher-Younger MAT **67**). The vendor-supported, extensible DES path: tasks as priority-sorted entities on a multi-core server with mutex-protected shared resources — use it to add custom scheduling policies and explicit resource contention that TrueTime abstracts.
3. **SoC Blockset — Task Execution / Task Manager** — MAT **63** (+ product doc **62**, interconnect-timing example **64**). Highest-fidelity *station* model: per-core task mapping, preemption, overrun/drop policy, and DDR/AXI memory contention — plug in when a station's compute/memory timing must be faithful.
4. **tres_bundle / T-Res** — MAT **77** (SAC '15, DOI 10.1145/2695664.2695876). The co-simulation *architecture* that generalizes beyond TrueTime: a per-node scheduler (RTsim) + a network simulator (OMNeT++) coupled to Simulink control via S-functions — the template if you need a richer network stack than TrueTime's built-ins. Pair with **ns3-fmi-export** (MAT **80**) to drive ns-3 as an FMI subordinate.
5. **Networked-scale MAC schedulers** — MAT **71–72** (5G NR RR/PF/best-CQI + custom `nrScheduler`) and MAT **23** (WLAN OFDMA), on the `wirelessNetworkSimulator` core (MAT 16–18). Use these when the *network* half must be a realistic, standards-based multi-station MAC at scale rather than TrueTime's abstract protocols.

**Method scaffolding to read alongside the build:** schedulability first — Liu & Layland (GEN **166**), Buttazzo (GEN **168**), Sha et al. historical (GEN **167**); then the network↔control coupling — Hespanha NCS survey (GEN **159**) and Tabuada event-triggered scheduling (GEN **163**); then worst-case sign-off — Real-Time Calculus (GEN **173**) with its MATLAB engine, the RTC Toolbox (MAT **81**), and SymTA/S (GEN **174**) to bound end-to-end delays the DES model then confirms.

**Suggested reading/build order (condensed):**
`GEN 159 → 166/168 → 172 (framing)` → `build in MAT 74 (TrueTime joint core)` → `refine scheduling/resources with MAT 65/66` → `add station compute fidelity with MAT 63` → `scale the network with MAT 71/72 or couple ns-3 via MAT 77/80` → `bound & validate with GEN 173 / MAT 81`.

## 7. Cross-corpus & structural notes

- Tool-agnostic methodology went to **GEN** (NCS surveys, event-triggered control, schedulability canon, feedback scheduling, RTC/SymTA/S theory, FMI co-sim semantics); MATLAB-applied artifacts went to **MAT** (SoC/SimEvents/5G/WLAN examples, TrueTime, theses that develop TrueTime, T-Res, RTC Toolbox, Naderlinger blocks, ns3-fmi bridge).
- One deliberate cross-corpus overlap flag was added: MAT 81 (RTC Toolbox) `[GEN-CORPUS overlap: item 173]` → the Thiele/Chakraborty/Naedele Real-Time-Calculus paper — the toolbox is the MATLAB implementation of that method.
- Cross-references were written to respect the build's mention-resolution heuristic (which routes any `item N` with N>61 to the GEN corpus): MAT→MAT links only reference existing items ≤61 (e.g. "items 41–42", "item 47", "items 41–45"); MAT→GEN links use the explicit `[GEN-CORPUS … item N]` flag; no new MAT item (62–81) is referenced by number.
