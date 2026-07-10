export const meta = {
  name: 'pass8-routes-p2',
  description: 'Phase 2: 11 route agents verify works and map element coverage for the pass-8 report',
  phases: [
    { title: 'Routes', detail: '11 verification + coverage agents' },
  ],
}

const SCRATCH = 'C:/Users/frede/AppData/Local/Temp/claude/E--dev-corpora/af68f286-e2b9-4227-a910-623820ffa376/scratchpad'

const SUMMARY = {
  type: 'object',
  additionalProperties: false,
  properties: {
    memberships: { type: 'integer' },
    new_works: { type: 'integer' },
    verified: { type: 'integer' },
    unverified: { type: 'integer' },
    gaps: { type: 'integer' },
    file: { type: 'string' },
    notes: { type: 'string' },
  },
  required: ['memberships', 'new_works', 'verified', 'unverified', 'gaps', 'file', 'notes'],
}

const ROUTES = [
  { key: 'r1', name: 'OO, construction & testing canon', seeds: `Membership candidates (grep work_ids.tsv): gof, iglberger, bloch (API-design paper), fowlerref (Refactoring), grenningtdd (TDD for Embedded C - only if it genuinely covers route elements). New-work candidates: Fowler PoEAA (2002), Meszaros xUnit Test Patterns (2007), Beck Smalltalk Best Practice Patterns (1997), Grand Patterns in Java vol 1 (1998), PLoPD3 (Pattern Languages of Program Design 3, 1998 - covers Null Object, Acyclic Visitor, External Polymorphism, Serializer, Product Trader, Sponsor-Selector, Bureaucracy, Role Object...; PLoPD1/2/4/5 only if elements need them), Cunningham CHECKS (PLoP 1994 paper), Bloch Effective Java (3rd ed 2018), Osmani Learning JavaScript Design Patterns, Fowler's individual articles where they name elements (Inversion of Control Containers and the Dependency Injection pattern 2004, FluentInterface 2005, PageObject 2013, TolerantReader 2011), Refactoring.Guru (living catalog site - one living-doc node), Evans DDD (2003) + DDD Reference (2015) for aggregate/domain-event, Fowler DSL book (2010) for semantic-model/expression-builder.` },
  { key: 'r2', name: 'Communication & messaging', seeds: `Membership candidates: posa2, douglasspatternsc, samekbook, freertosbook. New: Hohpe & Woolf Enterprise Integration Patterns (2003) - the route anchor covering most EIP-derived elements; POSA4 (2007) only if an element needs it; Qt Signals & Slots documentation (living); ReactiveX/Rx documentation (living); Reactive Streams specification (living, reactive-streams.org); OTP Design Principles (Erlang/OTP docs, living) for supervisor; MPI standard? only if an element needs it.` },
  { key: 'r3', name: 'Embedded, scheduling & numeric', seeds: `Membership candidates: white, koopmanbess, pont, douglasspatternsc, douglassrtcorpus, freertosbook, barrc, memfaultea, iec61508, liulayland or similar (grep for Liu-Layland rate monotonic), autosar OS-related ids (grep autosar). New: Varghese & Lauck hashed/hierarchical timing wheels (SOSP 1987), Buttazzo Hard Real-Time Computing Systems (grep buttazzo - may be membership!), Dawson Comparing Floating Point Numbers (2012 blog), ISO C23 stdckdint checked arithmetic (cite the standard), IEEE 1788-2015 interval arithmetic, Moore Interval Analysis (1966), ST AN2594 EEPROM emulation app note, Intel AP-684 FTL app note or Chung et al FTL survey (2009), Ganssle debouncing guide (if debounce element cites it).` },
  { key: 'r4', name: 'Execution & concurrency', seeds: `Membership candidates: posa2, protothreads, samekcourse, freertosbook. New: Goetz et al Java Concurrency in Practice (2006), Lea Concurrent Programming in Java 2nd ed (1999), Mattson/Sanders/Massingill Patterns for Parallel Programming (2004), Smith Notes on structured concurrency (2018, vorpus.org) or Trio docs, Kotlin/JEP 453 only as aka support, Agha Actors (1986) or Hewitt 1973 for actor-model, Hoelzle/Chambers/Ungar deoptimization (PLDI 1992), OpenJDK HotSpot Glossary (safepoint, living), Bell Threaded Code (CACM 1973) if threaded-code is in your element file, Conway coroutine paper (1963) or Knuth for coroutine naming - judge.` },
  { key: 'r5', name: 'Synchronization & lock-free', seeds: `Membership candidates: posa2, dreppermem (What Every Programmer Should Know About Memory), mckenney or perfbook ids (grep mckenney/perfbook). New: Herlihy & Shavit The Art of Multiprocessor Programming (2008/2012), McKenney Is Parallel Programming Hard (perfbook, living) if not a membership, Mellor-Crummey & Scott MCS lock (TOCS 1991), Michael Hazard Pointers (TPDS 2004), Michael & Scott queue (PODC 1996), Kung & Robinson On Optimistic Methods for Concurrency Control (TODS 1981), Bernstein & Goodman Concurrency Control in Distributed Database Systems (Computing Surveys 1981), Linux kernel locking/memory-barrier documentation (living official-doc), Drepper Futexes Are Tricky (2011), Preshing blog (living) only if an element's naming needs it, Lamport bakery/Treiber - only if elements demand.` },
  { key: 'r6', name: 'Data structures, persistence & caching', seeds: `Membership candidates: grep for CLRS/sedgewick/knuth (may exist via datastructures overlap), hanson. New: CLRS Introduction to Algorithms (3rd/4th ed), Sedgewick & Wayne Algorithms (4th ed 2011), Okasaki Purely Functional Data Structures (1998), Kleppmann Designing Data-Intensive Applications (2017), Petrov Database Internals (2019), Hellerstein/Stonebraker/Hamilton Architecture of a Database System (2007), Gray & Reuter Transaction Processing (1992), Ailamaki et al PAX (VLDB 2001), O'Neil bitmap index papers (1987/1997), Rosenblum & Ousterhout LFS (SOSP 1991), Manning/Raghavan/Schuetze Introduction to Information Retrieval (2008), Oracle Coherence caching documentation (read/write-through naming, living), plus original naming papers ONLY where no treatment covers the element (Bloom 1970, Flajolet HyperLogLog 2007, Cormode-Muthukrishnan count-min 2005, Karger consistent hashing 1997, Merkle 1987, Pugh skip lists 1990, O'Neil LSM 1996, Mohan ARIES 1992 - judge each: prefer the treatment book if it genuinely teaches the element).` },
  { key: 'r7', name: 'Language idioms, functional & data representation', seeds: `Membership candidates: coreguidelines, meyerseffcpp, meyerseffmod, iglberger, hanson, schreiner, tornhill, preschern, preschernplop, kernelstyle, kr2/kandr (grep kernighan). New: Coplien Advanced C++ (1992), Alexandrescu Modern C++ Design (2001), More C++ Idioms (Wikibooks, living), Stroustrup The Design and Evolution of C++ (1994 - names RAII), rust-unofficial/patterns (living), The Rust Programming Language book (Klabnik & Nichols, living - interior mutability), Haskell wiki (living - smart constructors), Moggi Notions of Computation and Monads (1991), Reynolds Definitional Interpreters (1972 - defunctionalization), Hutton & Meijer Monadic Parser Combinators (1996), Foster et al lenses (2007) or the Kmett ecosystem doc - judge, Plotkin & Pretnar effect handlers (2009), Kennedy units-of-measure (1996/2009), Chambers & Ungar An Efficient Implementation of Self (OOPSLA 1989 - hidden classes/maps), Gudeman Representing Type Information in Dynamically Typed Languages (TR 1993 - pointer tagging/NaN-boxing), Elliott & Hudak Functional Reactive Animation (1997) if FRP is in your file.` },
  { key: 'r8', name: 'Error handling, robustness & security', seeds: `Membership candidates: nygard, hanmer, preschern, preschernplop, douglasspatternsc, koopmanbess, seacordsecure (grep seacord), certc, iec61508. New: AWS Builders' Library (Timeouts retries and backoff with jitter - Brooker, living), Google SRE book (2016 - Handling Overload / cascading failures), Yoder & Barcalow Architectural Patterns for Enabling Application Security (PLoP 1997), Schumacher et al Security Patterns (Wiley 2006), Provos/Friedl/Honeyman Preventing Privilege Escalation (USENIX Security 2003), OWASP Cheat Sheet Series (living), Cowan et al StackGuard (USENIX Security 1998), Feathers Working Effectively with Legacy Code (2004 - characterization/golden-master), Claessen & Hughes QuickCheck (ICFP 2000), Meyer Object-Oriented Software Construction (2nd ed 1997 - design by contract), Candea & Fox Crash-Only Software / microreboot (HotOS 2003) - judge which elements need which; RFC 1982 serial number arithmetic; RFC 2308 negative caching if the element sits in your file.` },
  { key: 'r9', name: 'Parsing, text & serialization', seeds: `Membership candidates: grep for dragon/aho (unlikely). New: Aho/Lam/Sethi/Ullman Compilers (Dragon Book, 2nd ed 2006), Nystrom Crafting Interpreters (2021), Pratt Top Down Operator Precedence (POPL 1973), Knuth On the Translation of Languages from Left to Right (1965 - LR parsing) or the Dragon treatment - judge, Reps Maximal-Munch Tokenization in Linear Time (TOPLAS 1998), Visser Scannerless Generalized-LR Parsing (1997 TR P9707), Ford Parsing Expression Grammars (POPL 2004) + Packrat (ICFP 2002) as needed, Protocol Buffers Encoding documentation (living - varint/zigzag/length-prefix), ITU-T X.690 (TLV/BER), RFC 1055 SLIP, Cheshire & Baker COBS (IEEE/ACM ToN 1999), DWARF spec (LEB128) only if needed, Parr Enforcing Strict Model-View Separation in Template Engines (WWW 2004), Ellis & Gibbs operational transformation (SIGMOD 1989), Fowler DSL book if expression-builder/semantic-model land in your file.` },
  { key: 'r10', name: 'Data flow, state & UI/games', seeds: `Membership candidates: samekbook (HSM), douglassrtcorpus, white (if system-tick etc. cite it), nygard (backpressure). New: Nystrom Game Programming Patterns (2014) - route anchor, Gregory Game Engine Architecture (3rd ed 2018), Harel Statecharts (Sci. Comput. Program. 1987), Bernier Latency Compensating Methods (GDC 2001), Aronson Dead Reckoning (Gamasutra 1997), Fiedler gafferongames (living - deterministic lockstep/fixed timestep), O'Donnell FrameGraph (GDC 2017), NVIDIA texture atlas whitepaper (2004) or Ivanov 2006, Wloka Batch Batch Batch (GDC 2003), Thompson et al LMAX Disruptor technical paper (2011), Akidau et al The Dataflow Model (PVLDB 2015), Elliott & Hudak FRP (1997) if FRP sits here, Bainomugisha et al A Survey on Reactive Programming (CSUR 2013), React documentation (living - reconciliation/hydration/batching), Vue.js or Angular docs only where they are the naming source (dirty checking - AngularJS guide), WPF Data Binding Overview (living), TC39 Signals proposal (living), Apollo optimistic UI docs (living), Cannon Fight the Lag (2012) or GGPO docs for rollback netcode, Hodgson Feature Toggles (martinfowler.com 2017), Fowler Memory Image (2011), javascript.info event delegation (living) or a stronger source - judge.` },
  { key: 'r11', name: 'Resource management & memory', seeds: `Membership candidates: noblesmallmem, posa3, douglasspatternsc, white, preschern, coreguidelines, tlsf-paper ids (grep tlsf), lea/dlmalloc ids (grep dlmalloc/lea), etl (grep etl - Embedded Template Library). New: Jones/Hosking/Moss The Garbage Collection Handbook (2011/2023) - GC elements anchor, Bonwick The Slab Allocator (USENIX 1994), Wilson et al Dynamic Storage Allocation survey (IWMM 1995), Knuth TAOCP vol 1 (buddy system) - judge vs the Wilson survey, Masmano et al TLSF (ECRTS 2004) if not already a corpus work, Lea A Memory Allocator (dlmalloc essay, living) if not already a corpus work, Gay & Aiken region-based memory (PLDI 1998) or Tofte-Talpin (1997) for arena/region naming - judge, Collins reference counting (CACM 1960) or the GC Handbook treatment - judge.` },
]

function prompt(r) {
  return `You are pass-8 route agent "${r.key}: ${r.name}" for Phase 2 of the ELEMENT-layer mission (repo E:/dev/corpora).

GOAL: for every element in your route file, establish which catalog-grade works define and/or teach it, verifying every NEW work against a live primary page. This becomes the pass-8 report (design-elements) extending a 468-work corpus.

MANDATORY FIRST STEPS:
1. Read E:/dev/corpora/SWE/MISSION_design_elements_v1.md - the PHASE 2 section is your contract (merge discipline, many-to-many mapping, verification discipline).
2. Read ${SCRATCH}/p2/${r.key}.json - your route's elements (id, name, kind, named_in, named_in_corpus_id, other_sources, tags).
3. Read E:/dev/corpora/SWE/swe_process_corpus_v1_0.md lines 1-20 for the house entry style.
4. Grep ${SCRATCH}/work_ids.tsv aggressively - works already in the corpus MUST become memberships reusing the EXACT existing id, never new nodes.

WORK-SET SEEDS (verify, extend, or reject - your judgment governs): ${r.seeds}

RULES:
- MEMBERSHIP (work already in corpus): action=membership, reuse the exact corpus id, no bibliographic re-verification needed; give the pass-8 relevance note + covered elements.
- NEW work: action=new, propose a kebab/short id in corpus style (check it collides with NEITHER work_ids.tsv NOR element ids in ${SCRATCH}/elements_index.txt); verification=verified ONLY if you loaded a primary/authoritative page THIS SESSION confirming the exact identifier (publisher page, ACM/IEEE DL, standards body, official project site, author's page); otherwise verification=unverified with unresolved naming the soft field (e.g. "isbn", "year"). NEVER fabricate ISBN/DOI/year - omit sooner than guess.
- COVERAGE: assign each work the element ids (from your route file ONLY) it genuinely defines or teaches at catalog grade. Every element in your file must end covered by >=1 work, with two exceptions: (a) if the only source is a bare Wikipedia article, try to upgrade to a catalog-grade treatment (book/paper/official doc); if none exists, put the element in gaps with why; (b) never pad - a work that merely mentions an element does not cover it.
- Include the best modern treatment when the naming source is old (both get the element).
- role per work: anchor (route entry point) | core | advanced | survey.
- type: book | paper | standard | official-doc | tooling-doc | blog | guide | course | report | other.
- Aim for economy: prefer one treatment covering many elements over many single-element papers; include single-element naming papers only when nothing better covers the element or the paper is itself canon.

OUTPUT - write UTF-8 JSON to ${SCRATCH}/p2out/${r.key}.json:
{"route":"${r.key}",
 "works":[{"action":"membership|new","id":"...","title":"...","authors":"...","year":"2004|living","venue":"publisher/venue","ident":"ISBN/DOI/URL or null","type":"...","role":"anchor|core|advanced|survey","verification":"verified|unverified","unresolved":null,"note":"1-line relevance","elements":["..."]}],
 "gaps":[{"element":"id","why":"..."}],
 "notes":"route-level coverage remarks"}
VALIDATE via Bash: python -c "import json;json.load(open(r'${SCRATCH}/p2out/${r.key}.json',encoding='utf-8'))"
Return summary: memberships, new_works, verified, unverified, gaps, file, notes.`
}

phase('Routes')
log(`launching ${ROUTES.length} pass-8 route agents`)
const res = await parallel(ROUTES.map(r => () =>
  agent(prompt(r), { label: `p8:${r.key}`, phase: 'Routes', schema: SUMMARY, effort: 'high' })
    .then(x => (x ? { key: r.key, ...x } : null))
))
const ok = res.filter(Boolean)
log(`${ok.length}/${ROUTES.length} routes done; new works: ${ok.reduce((a, r) => a + r.new_works, 0)}, memberships: ${ok.reduce((a, r) => a + r.memberships, 0)}, gaps: ${ok.reduce((a, r) => a + r.gaps, 0)}`)
return { routes: ok, missing: ROUTES.filter((r, i) => !res[i]).map(r => r.key) }