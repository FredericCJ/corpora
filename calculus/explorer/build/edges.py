# -*- coding: utf-8 -*-
"""Inference-layer records hand-transcribed from calc-analysis.md: §3 edge list (authoritative),
§4 parallel sets, §5 quality-gate ledger, §6 DOT rendering (used only as a cross-check against
the authoritative table), §7 recommended lineage, §8 open register, Caveats.
Evidence tags are the report's own epistemic labels: EVIDENCED (tables of contents, stated
prerequisites, published reviews) vs JUDGMENT (reasoned pedagogical judgment)."""

E, J = 'EVIDENCED', 'JUDGMENT'
DITTO = 'seam stated as “same” in the source table; expanded from the preceding row'

# §3 — the authoritative edge list: (from, to, seam / shared topics, tag, transcription-note)
EDGES = [
    ('N01', 'N02', 'real numbers, exponents/radicals, algebraic & rational expressions, equations, complex numbers', E, ''),
    ('N02', 'N06', 'functions & graphs, trigonometry, exponentials/logs, problem-solving prologue', E, ''),
    ('N02', 'N07', 'same precalculus foundation feeding concepts-first calculus', E, ''),
    ('N02', 'N03', 'algebraic prerequisites (equations, lines, quadratics, logs, trig) reviewed then derivative', E, ''),
    ('N02', 'N04', 'function library → integrals, FTC', E, ''),
    ('N02', 'N05', 'functions → multivariable, sequences/series', E, ''),
    ('N06', 'N08', 'limits, derivatives, integrals, sequences/series (computational → proved)', E, ''),
    ('N07', 'N08', 'same computational calculus → rigorous treatment', E, ''),
    ('N03', 'N08', 'derivative theory → rigorous calculus', J, ''),
    ('N04', 'N08', 'integral theory → rigorous calculus', J, ''),
    ('N05', 'N08', 'multivariable/series → rigorous calculus + linear algebra', J, ''),
    ('N06', 'N09', 'mathematical reasoning maturity → formal proof technique', J, ''),
    ('N07', 'N09', 'mathematical reasoning maturity → formal proof technique', J, DITTO),
    ('N05', 'N09', 'mathematical reasoning maturity → formal proof technique', J, DITTO),
    ('N09', 'N10', 'logic, sets, induction, functions → rigorous limits/derivatives/integrals', E, ''),
    ('N09', 'N11', 'proof technique → sequences/series convergence proofs', E, ''),
    ('N09', 'N12', 'proof technique → ε-δ real analysis', E, ''),
    ('N09', 'N13', 'proof technique → abstract vector spaces/linear maps', E, ''),
    ('N10', 'N12', 'rigorous single-variable calculus → real analysis (metric/topology of ℝ)', E, ''),
    ('N10', 'N14', 'real number construction, limits, continuity, series → Rudin', E, ''),
    ('N11', 'N14', 'sequences, series, continuity, uniform convergence → Rudin', E, ''),
    ('N12', 'N14', 'completeness, sequences, topology of ℝ, functional limits → Rudin', E, ''),
    ('N11', 'N15', 'real numbers, limits, continuity → Pugh (topology, function spaces)', E, ''),
    ('N12', 'N15', 'real numbers, limits, continuity → Pugh (topology, function spaces)', E, DITTO),
    ('N08', 'N14', 'rigorous continuity/series + linear algebra → metric-space analysis', E, ''),
    ('N08', 'N16', 'multivariable calculus + linear algebra → vector calculus/forms', E, ''),
    ('N13', 'N17', 'abstract vector spaces, inner products, operators → analysis on vector spaces', E, ''),
    ('N13', 'N16', 'linear maps/matrices → vector calculus & differential forms', E, ''),
    ('N14', 'N19', 'metric spaces, Riemann–Stieltjes, sequences of functions → Lebesgue measure/complex', E, ''),
    ('N14', 'N20', 'topology of ℝⁿ, Riemann integral, uniform convergence → measure/Lebesgue', E, ''),
    ('N14', 'N24', 'Riemann integration, metric spaces → Lebesgue measure & integration', E, ''),
    ('N14', 'N21', 'analytic groundwork, series → complex function theory', E, ''),
    ('N14', 'N22', 'rigorous limits/series → analytic functions', E, ''),
    ('N14', 'N23', 'rigorous analysis → complex function theory (GTM)', E, ''),
    ('N15', 'N20', 'Lebesgue intro in Pugh → full measure theory', E, ''),
    ('N15', 'N24', 'undergraduate Lebesgue → graduate measure', E, ''),
    ('N15', 'N19', 'real analysis maturity → Rudin RCA', J, ''),
    ('N17', 'N19', 'Banach-space & integration maturity → graduate real/complex', J, ''),
    ('N19', 'N25', 'measure/integration, Lᵖ, Hilbert/Banach basics → abstract measure & functional analysis', E, ''),
    ('N20', 'N25', 'measure, integration, Hilbert spaces → modern techniques (topology/functional)', E, ''),
    ('N24', 'N25', 'Lebesgue measure/integration → abstract measure & functional analysis', E, ''),
    ('N20', 'N26', 'Lᵖ/Hilbert spaces → Banach spaces, distributions, probability (series IV)', E, ''),
    ('N19', 'N27', 'Lᵖ, functional-analytic tools → functional analysis, Sobolev, PDE', E, ''),
    ('N24', 'N27', 'measure/integration → functional analysis, Sobolev, PDE', E, ''),
    ('N25', 'N26', 'functional analysis basics, distributions → further topics (probability, SCV, oscillatory integrals)', E, ''),
    ('N25', 'N27', 'functional analysis, Lᵖ, distributions → Sobolev spaces & PDE', E, ''),
]

# §6 — the DOT rendering's edge statements, transcribed independently as a cross-check.
DOT_EDGES = set(
    [('N01', 'N02')] +
    [('N02', t) for t in ('N06', 'N07', 'N03', 'N04', 'N05')] +
    [(s, 'N08') for s in ('N06', 'N07', 'N03', 'N04', 'N05')] +
    [(s, 'N09') for s in ('N06', 'N07', 'N05')] +
    [('N09', t) for t in ('N10', 'N11', 'N12', 'N13')] +
    [('N10', 'N12'), ('N10', 'N14'),
     ('N11', 'N14'), ('N12', 'N14'), ('N11', 'N15'), ('N12', 'N15'),
     ('N08', 'N14'), ('N08', 'N16'),
     ('N13', 'N17'), ('N13', 'N16')] +
    [('N14', t) for t in ('N19', 'N20', 'N24', 'N21', 'N22', 'N23')] +
    [('N15', 'N20'), ('N15', 'N24'), ('N15', 'N19'),
     ('N17', 'N19'),
     ('N19', 'N25'), ('N20', 'N25'), ('N24', 'N25'),
     ('N20', 'N26'), ('N19', 'N27'), ('N24', 'N27'), ('N25', 'N26'), ('N25', 'N27')]
)

# §4 — parallel sets: equivalent-scope siblings; shared, not sequenced (no internal ordering).
PARALLEL_SETS = [
    dict(id='PS-1', label='Tier 0/1 spine alternatives', members=['N06', 'N07'],
         note='Equivalent-scope single-variable calculus; user-mandated siblings.'),
    dict(id='PS-2', label='Tier 1 fast on-ramps', members=['N03', 'N04', 'N05'],
         note='User-mandated sibling alternatives; share incoming edge from N02 and outgoing edges to '
              'N08/N09; no internal sequence.'),
    dict(id='PS-3', label='Tier 4 first-analysis', members=['N11', 'N12'],
         note='Equivalent-scope introductory real analysis; no dependency between them.'),
    dict(id='PS-4', label='Tier 5 undergraduate real analysis', members=['N14', 'N15'],
         note='Equivalent scope; Pugh adds pictures + a Lebesgue preview.'),
    dict(id='PS-5', label='Tier 6 graduate complex analysis', members=['N21', 'N22', 'N23'],
         note='Equivalent-scope graduate complex analysis.'),
    dict(id='PS-6', label='Tier 6 graduate measure/real', members=['N19', 'N20', 'N24'],
         note='Equivalent-scope graduate measure/integration (Rudin RCA additionally covers complex).'),
]

# §7 — recommended lineage + the higher-overlap variant. Steps carry the report's seam justifications.
LINEAGES = [
    dict(id='main', label='Recommended lineage (source → sink)',
         path=['N01', 'N02', 'N06', 'N08', 'N14', 'N19', 'N25', 'N27'],
         note='One full source-to-sink path.',
         steps=[
             dict(frm='N01', to='N02', note='Intermediate Algebra supplies the real-number/expression/equation '
                  'machinery that forms Chapter 1 (“Fundamentals”) of the Precalculus text — near-total seam overlap.'),
             dict(frm='N02', to='N06', note='Precalculus delivers the functions, trigonometry and log/exponential '
                  'library that Stewart’s Calculus assumes on page one; only limits are new.'),
             dict(frm='N06', to='N08', note='Stewart teaches every computational technique (limits, derivatives, '
                  'integrals, series) that Apostol re-derives with proofs, so the jump is purely in rigor, not topic.'),
             dict(frm='N08', to='N14', note='Apostol’s rigorous continuity, sequences/series and its integrated '
                  'linear algebra cover Rudin PMA’s opening chapters; Rudin advances into metric-space topology.'),
             dict(frm='N14', to='N19', note='Rudin PMA’s metric spaces, Riemann–Stieltjes integral and sequences of '
                  'functions are exactly the assumed background for Rudin RCA, which advances to Lebesgue measure '
                  'and complex analysis.'),
             dict(frm='N19', to='N25', note='RCA’s measure/integration, Lᵖ and Hilbert/Banach basics overlap '
                  'Folland’s core, which advances into abstract point-set topology and fuller functional analysis.'),
             dict(frm='N25', to='N27', note='Folland’s functional analysis, Lᵖ and distribution groundwork feed '
                  'directly into Brezis, which advances to Sobolev spaces and PDE — a genuine graduate sink.'),
         ]),
    dict(id='variant', label='Higher-overlap real-analysis on-ramp',
         path=['N02', 'N06', 'N09', 'N12', 'N14'],
         note='Routes through Velleman’s proof techniques and Abbott’s motivated ε-δ analysis, which maximizes '
              'the seam into Rudin PMA — the recommended path for a student who has not yet written proofs.',
         steps=[]),
]

# §5 — quality-gate ledger, one row per candidate as the report states it.
GATE = [
    dict(candidate='N01 Miller/O’Neill/Hyde', ids=['N01'], status='kept',
         reason='Only algebra-readiness source; current 6th ed. (2022).'),
    dict(candidate='N02 Stewart/Redlin/Watson Precalc', ids=['N02'], status='kept',
         reason='Standard, chapter-verified bridge (Fundamentals → functions → trig).'),
    dict(candidate='N03–N05 Ashlock Fast Start', ids=['N03', 'N04', 'N05'], status='kept',
         reason='User-mandated parallel set; concise self-reviewing on-ramps.'),
    dict(candidate='N06 Stewart Calculus', ids=['N06'], status='kept',
         reason='Dominant, precise, complete single/multivariable calculus.'),
    dict(candidate='N07 Stewart–Kokoska', ids=['N07'], status='kept',
         reason='User-mandated sibling; concepts-first alternative (5th ed., ©2023).'),
    dict(candidate='N08 Apostol', ids=['N08'], status='kept',
         reason='Uniquely bridges computation→proof with integrated linear algebra.'),
    dict(candidate='N18 Woods Advanced Calculus (1926/1934)', ids=['N18'], status='dropped',
         reason='Superseded by Apostol/Loomis–Sternberg: 1930s notation, no modern measure/forms treatment; '
                'retained in bibliography only.'),
    dict(candidate='N09 Velleman', ids=['N09'], status='kept',
         reason='Dedicated transition-to-proof text; closes the biggest seam (logic→sets→induction).'),
    dict(candidate='N10 Spivak', ids=['N10'], status='kept',
         reason='Rigorous single-variable calculus, proof-first (Parts I–V culminating in real-number construction).'),
    dict(candidate='N11 Ross / N12 Abbott', ids=['N11', 'N12'], status='kept',
         reason='Two gentle first-analysis texts; MAA-reviewed as accessible ε-δ introductions (parallel).'),
    dict(candidate='N13 Axler', ids=['N13'], status='kept',
         reason='Canonical proof-based abstract linear algebra; open-access 4th ed. (CC BY-NC, 2024).'),
    dict(candidate='N14 Rudin PMA', ids=['N14'], status='kept',
         reason='Canonical undergraduate real analysis (interior, not sink).'),
    dict(candidate='N15 Pugh', ids=['N15'], status='kept',
         reason='Strong Rudin-level sibling with Lebesgue preview.'),
    dict(candidate='N16 Hubbard & Hubbard', ids=['N16'], status='kept',
         reason='Unified multivariable analysis + differential forms bridge.'),
    dict(candidate='N17 Loomis & Sternberg', ids=['N17'], status='kept',
         reason='Advanced calculus on vector spaces/manifolds; maturity bridge to graduate.'),
    dict(candidate='N19 Rudin RCA', ids=['N19'], status='kept',
         reason='Interior graduate node (not sink); unified real+complex.'),
    dict(candidate='N20 Stein–Shakarchi Real', ids=['N20'], status='kept',
         reason='Modern graduate measure theory; integrated series.'),
    dict(candidate='N24 Royden–Fitzpatrick', ids=['N24'], status='kept',
         reason='Classic graduate measure/integration; current 4th ed.'),
    dict(candidate='N21/N22/N23 complex trio', ids=['N21', 'N22', 'N23'], status='kept',
         reason='Three canonical graduate complex-analysis options (parallel).'),
    dict(candidate='N25 Folland', ids=['N25'], status='kept',
         reason='Standard second-course abstract measure + functional analysis.'),
    dict(candidate='N26 Stein–Shakarchi Functional', ids=['N26'], status='kept',
         reason='Research-level sink (distributions, probability, SCV, oscillatory integrals).'),
    dict(candidate='N27 Brezis', ids=['N27'], status='kept',
         reason='Research-level sink (functional analysis, Sobolev, PDE).'),
]

# §8 — open register.
REGISTER = [
    dict(title='Woods Advanced Calculus last edition [VERIFIED, noted]',
         body='A 1934 “New edition” (Ginn; LC QA303.W885 1934) exists beyond the 1926 first edition; both '
              'catalogued, node dropped by the quality gate. No unresolved bibliographic uncertainty remains.'),
    dict(title='No open topical gap',
         body='No invented bridge was required; the proof-transition seam is closed by Velleman (N09) and the '
              'Tier-4 first-analysis set (Ross/Abbott/Spivak). Every node resolved to a specific edition and year; '
              'the only formerly-unverified item (N07 Stewart–Kokoska) is now confirmed as 5th ed., ©2023 '
              '(Cengage, ISBN 9780357632499).'),
]

# Caveats — carried verbatim in substance; they gate what the views may claim.
CAVEATS = [
    dict(title='Overlap is structural, never numeric',
         body='All seam-overlap claims are inferred from tables of contents, stated prerequisites and published '
              'reviews (tagged EVIDENCED) or from reasoned pedagogical judgment where evidence underdetermines '
              'the call (JUDGMENT) — never from full-text comparison or invented percentages.'),
    dict(title='Edition currency',
         body='Axler’s 4th ed. carries a 2024 copyright; some retail pages list 2023 (print release). Stewart '
              'Calculus 9e is dated 2020 with a 2021 copyright. Stewart–Kokoska is confirmed 5th ed. ©2023. '
              'These are catalog-page facts and can shift with reprints.'),
    dict(title='Parallel-set edges are shared, not sequenced',
         body='Within each parallel set no A→B ordering is implied; siblings inherit the same incoming and '
              'outgoing edges.'),
    dict(title='Judgment edges from the Ashlock set',
         body='N03–N05 → N08/N09 reflect that these concise “Fast Start” volumes cover derivative/integral/'
              'multivariable material at lower depth than Stewart; a student using only the Ashlock path may '
              'need supplementary problem sets before Apostol.'),
    dict(title='The complex-analysis trio are terminal leaves',
         body='N21/N22/N23 are not dead ends pedagogically — they represent a parallel graduate specialization '
              'rather than a step toward the functional-analysis sinks; a learner may pursue the complex branch '
              'and the measure/functional branch independently after Rudin PMA.'),
    dict(title='Woods (N18) verified but dropped',
         body='Included in the bibliography for completeness and because the seed list requested resolution of '
              'its edition (1926 first / 1934 new edition).'),
]

# View definitions — what each model means, asks, and computes.
VIEWS = {
    'graph': dict(label='Prerequisite DAG',
                  semantic='The verified 26-node prerequisite DAG, tier-layered top-to-bottom (plus the one '
                           'dropped node as a ghost).',
                  question='What must I read before this book, and where does it lead?',
                  computed='All 46 edges of the authoritative edge list; rows are tiers 0–8; within-row order is '
                           'a pure barycenter pass; dashed enclosures are parallel sets; solid edges EVIDENCED, '
                           'dashed amber edges JUDGMENT; hover traces the full ancestor+descendant closure.'),
    'tiers': dict(label='Tier ladder',
                  semantic='The nine-tier maturity scheme derived from stated prerequisites, series placement, '
                           'and reviews.',
                  question='What does each maturity level contain, and which texts sit at my level?',
                  computed='Tier columns 0–8 with the scheme’s own name/focus/rigor per tier; nodes bucketed by '
                           'catalogue tier; no inference.'),
    'lineage': dict(label='Lineages & paths',
                    semantic='The report’s recommended source-to-sink lineage, its proof-novice variant, and a '
                             'path finder over the DAG.',
                    question='In what order do I actually read — and what are my alternatives?',
                    computed='Preset paths carried verbatim with per-seam justifications; the finder enumerates '
                             'every directed path between two chosen nodes (exact count by DP over the DAG, '
                             'enumeration capped and said so).'),
    'parallel': dict(label='Parallel sets',
                     semantic='Six sets of equivalent-scope siblings — shared, not sequenced.',
                     question='Which books are alternatives to each other rather than prerequisites?',
                     computed='Membership carried from §4; shared vs partial prerequisite/continuation '
                              'neighborhoods computed from the actual edge list, so stated claims are checkable.'),
    'gate': dict(label='Quality gate',
                 semantic='The report’s own editorial spine: TL;DR, kept/dropped ledger, open register, caveats.',
                 question='Why is each text in (or out), and what should temper my trust?',
                 computed='Ledger rows, register and caveats carried verbatim; no inference.'),
}
