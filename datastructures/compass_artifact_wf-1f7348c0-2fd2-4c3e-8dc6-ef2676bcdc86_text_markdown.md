# Audit of ChatGPT's "Foundational Source" Answers for 17 Data Structures

## TL;DR
- ChatGPT's answers are largely defensible: I CONFIRM the core attribution for roughly two-thirds of the 17 structures, but several theory/implementation slots need correction or expansion.
- The clearest FIXES: **Array** (FORTRAN is not the foundational root of the array concept — index registers / subscripted variables predate it), **Hash table** (Dumey 1956 is the foundational *public* source, not Peterson 1957), **Priority queue** (Williams 1964 is the root, not Crane 1972), and **Record/struct** (Hoare's 1965 "Record Handling" is the root of the typed-record concept, and the ALGOL 68 date should be 1975, not 1978).
- Several structures legitimately admit multiple defensible options (Binary search tree, Set, Map/dictionary, Stack theory-root, Graph, String); I enumerate them rather than forcing a single answer, and I downgrade several "Knuth = root" claims to "canonical reference, not origin."

## Key Findings
- ChatGPT correctly identified the linked-list (Information Processing Language, IPL), stack (Bauer & Samelson), heap (Williams/Floyd), binary search tree (multiple 1960 origins), and graph-theory (Euler/Cayley) lineages.
- The recurring weakness is the *theory-root* slot for pre-computer mathematical structures and for structures whose "invention" was really a gradual machine-level practice (arrays, records, queues).
- Where ChatGPT cited Knuth's *The Art of Computer Programming* (TAOCP) as a "root," this is generally a FIX or qualification: Knuth is a canonical *synthesizer/reference*, not the foundational root of queue, deque, tree-implementation, or binary tree.
- Abbreviations expanded on first use: FORTRAN = Formula Translation; IBM = International Business Machines; IPL = Information Processing Language; SETL = Set Language; TAOCP = The Art of Computer Programming; CODASYL = Conference on Data Systems Languages; COBOL = Common Business-Oriented Language; ACE = Automatic Computing Engine; ACM = Association for Computing Machinery; CACM = Communications of the ACM; JACM = Journal of the ACM; SNOBOL = String Oriented Symbolic Language; BST = Binary Search Tree; LIFO = last-in-first-out; FIFO = first-in-first-out.

## Details

### 1. Array
**ChatGPT:** theory = Backus, Herrick, Ziller et al., "Preliminary Report: Specifications for the IBM Mathematical Formula Translating System, FORTRAN" (1954); implementation = Backus et al., "The FORTRAN Automatic Coding System" (1957).
**Verdict: FIX (theory-root) / defensible (implementation).**
The subscripted-variable/array *concept* and its machine realization predate FORTRAN. Index registers (called "B-lines" in Britain) were first used on the Manchester Mark 1: the intermediary Manchester Mark 1 was operational by April 1949 with two modifier registers (B-lines, for modifying instruction addresses), and the index-register patent was filed 3 June 1949 in the names of Frederic C. Williams, Tom Kilburn, G. C. Tootill, A. A. Robinson, and M. H. A. Newman (University of Manchester Computer50 archive). Konrad Zuse's Plankalkül (designed 1942–45) also had array-like aggregates. So FORTRAN is not the foundational *root of lineage* for arrays as a stored, index-addressed structure. FORTRAN's genuine contribution was the *high-level-language array with subscript notation and compiler-generated indexing*. The implementation paper — "The FORTRAN Automatic Coding System" (J. W. Backus, R. J. Beeber, S. Best, R. Goldberg, L. M. Haibt, H. L. Herrick, R. A. Nelson, D. Sayre, P. B. Sheridan, H. Stern, I. Ziller, R. A. Hughes, R. Nutt; *Proceedings of the Western Joint Computer Conference*, February 1957, pp. 188–198) — is a defensible implementation-description root for the *language-level* array.
**Recommended framing:** theory-root of the array-as-machine-structure = index registers on the Manchester Mark 1 (1949); FORTRAN (1954 specification / 1957 implementation) is the foundational root only for the high-level-language array abstraction.

### 2. Dynamic array / list
**ChatGPT:** theory = Knuth TAOCP Vol. 1 (1997) for linear lists / sequential allocation; implementation = no single early canonical root, cites Tarjan "Amortized Computational Complexity" (1985) as later, non-foundational.
**Verdict: CONFIRM (with refinement).**
Knuth's TAOCP Vol. 1, §2.2 (linear lists, sequential allocation) is a reasonable theory/reference anchor, though it is a synthesis rather than an origin. The "dynamic array" as a self-resizing structure with O(1) amortized append has no single foundational paper; the analysis technique that explains it (amortization) was formally introduced by Robert Endre Tarjan, "Amortized Computational Complexity," *SIAM Journal on Algebraic and Discrete Methods*, 6(2):306–318 (1985). ChatGPT correctly marks Tarjan 1985 as *later and non-foundational* to the structure itself (it analyzes, not invents). This is the correct application of the "no foundational implementation" rule. **Confirmed.**

### 3. Linked list
**ChatGPT:** both = Newell & Shaw, "Programming the Logic Theory Machine" (1957); IPL lineage as first linked-list implementation.
**Verdict: CONFIRM.**
Linked lists were developed 1955–1956 by Allen Newell, Cliff Shaw, and Herbert A. Simon at the RAND Corporation (and Carnegie Institute of Technology) as the core structure of Information Processing Language (IPL). The classic node-and-arrow diagram appears in Allen Newell and J. C. Shaw, "Programming the Logic Theory Machine," *Proceedings of the Western Joint Computer Conference* (1957), pp. 230–240. This single source reasonably covers both the conceptual introduction and the first implementation. Minor note: Herbert Simon is a co-originator of the IPL work though not a co-author of the 1957 Newell–Shaw paper specifically. **Confirmed.**

### 4. Stack
**ChatGPT:** both = Bauer & Samelson, "Sequential Formula Translation" (1960); the "cellar" stack lineage.
**Verdict: ENUMERATE DEFENSIBLE OPTIONS (ChatGPT's is defensible; the theory-root has an earlier claimant worth naming).**
Defensible options:
- **Alan Turing (1946), Automatic Computing Engine (ACE) reports**, used "bury"/"unbury" for subroutine call/return — the earliest appearance of LIFO discipline in the computing literature. Argument: genuine root of the *concept* in computing.
- **Charles L. Hamblin** independently developed the stack (for what became reverse-Polish evaluation) in the first half of 1954, with publication in 1957; the concept was also independently developed by Wilhelm Kämmerer ("automatisches Gedächtnis").
- **Klaus Samelson & Friedrich L. Bauer**, Technical University of Munich: proposed the "Operationskeller" (operational cellar) in 1955, filed German patent DBP 1094019 in 1957, presented the stack principle publicly at the 1959 IFIP Congress in Paris, and published the influential Samelson & Bauer, "Sequential Formula Translation," *Communications of the ACM* 3(2):76–83 (February 1960). Bauer received the 1988 IEEE Computer Society Computer Pioneer Award; the official citation reads simply "For computer stacks" (the award went to Bauer alone, Samelson having died by 1988). Argument: this is the foundational lineage of the stack as an explicitly named, general-purpose data structure used for formula translation — the root of the stack as *used today*.
Under the task's "early AND influential root-of-lineage" definition, **Bauer & Samelson is the strongest single choice** for the stack as a named data structure (ChatGPT is defensible and arguably correct), but the audit should acknowledge Turing (1946) as the earliest conceptual appearance and Hamblin (1954/1957) as an independent origin. The 1960 CACM paper reasonably covers both theory and implementation (formula translation via the cellar).

### 5. Queue
**ChatGPT:** both = Knuth TAOCP Vol. 1 (1997).
**Verdict: FIX / qualify.**
The queue (first-in-first-out list) has no single "inventor" paper; it is an ancient operational concept formalized gradually. Knuth's TAOCP Vol. 1 §2.2.1 ("Stacks, Queues, and Deques") is the *canonical reference definition* but is explicitly a synthesis (Vol. 1 first published 1968; 3rd edition 1997), not a foundational root. The correct verdict per the task's rules is: **theory-root is definitional/diffuse with no single foundational paper; Knuth is a non-foundational canonical reference** sitting decades from any origin. Citing Knuth as *the* root overstates it, and there is no distinct foundational implementation paper either.

### 6. Deque (double-ended queue)
**ChatGPT:** both = Knuth TAOCP Vol. 1 (1997).
**Verdict: FIX / qualify (same reasoning as Queue).**
Knuth's TAOCP Vol. 1 §2.2.1 is where the term "deque" and its input-/output-restricted variants are canonically defined and popularized — a defensible *reference*, but a synthesis rather than a foundational origin. Knuth attributes and surveys rather than invents. Verdict: canonical reference, not foundational root; no distinct earlier single-source origin is cleanly identifiable, and Knuth sits far from any true root.

### 7. Set
**ChatGPT:** theory = Cantor, "Beiträge zur Begründung der transfiniten Mengenlehre" (1895–1897); implementation = Schwartz, "Set Theory as a Language for Program Specification and Programming" / SETL (1970).
**Verdict: CONFIRM theory; ENUMERATE DEFENSIBLE OPTIONS for implementation.**
Theory-root: Georg Cantor, "Beiträge zur Begründung der transfiniten Mengenlehre," *Mathematische Annalen* 46 (1895): 481–512 and 49 (1897): 207–246, is the correct foundational treatment of set theory. **Confirmed.**
Implementation: Jacob T. ("Jack") Schwartz, "Set Theory as a Language for Program Specification and Programming" (Courant Institute of Mathematical Sciences, New York University, September 1970), which founded SETL (Set Language) with finite sets as the fundamental data type, is a *defensible* foundational implementation of the set as a primitive programming data type. However, per the task's caution, the set-as-data-structure has no single canonical implementation root the way the linked list does — sets are realized via hash tables, trees, or bit-vectors, each with its own lineage. SETL is defensible as the first language making *finite sets the fundamental data type*, but it is one defensible option, not the sole root. This should be flagged, not asserted as the unique implementation root.

### 8. Map / dictionary (associative array)
**ChatGPT:** theory = Griswold, Poage, Polonsky, "The SNOBOL4 Programming Language" (1971); implementation = Griswold, "The Macro Implementation of SNOBOL4" (1972).
**Verdict: ENUMERATE DEFENSIBLE OPTIONS.**
Built-in syntactic support for associative arrays under the name "table" was introduced by SNOBOL4 (c. 1969, documented in Ralph E. Griswold, J. F. Poage & Ivan P. Polonsky, *The SNOBOL4 Programming Language*, 1971). This is a defensible root for the *language-level associative array as a first-class construct*, and Griswold's "The Macro Implementation of SNOBOL4" (1972) is a defensible implementation source. But competing/earlier claims exist:
- **Lisp association lists (a-lists), c. 1960** (John McCarthy's Lisp): the earliest key–value lookup structure in a programming language, though inefficient (linear search).
- **Hash tables (Luhn 1953 / Dumey 1956)**: the underlying implementation mechanism for most maps, predating SNOBOL4 by roughly 15 years.
So: SNOBOL4 is defensible as the origin of the *built-in associative-array language feature*; Lisp a-lists are the earlier *conceptual* key–value structure; and the hash table is the foundational *implementation* substrate. ChatGPT's SNOBOL4 answer is defensible but not uniquely correct — the theory of the abstract map is better traced to the a-list / dictionary-problem lineage.

### 9. Hash table
**ChatGPT:** both = Peterson, "Addressing for Random-Access Storage" (1957); notes Luhn's 1953 IBM memorandum is earlier but internal.
**Verdict: FIX.**
The genuinely foundational *public* source is **Arnold I. Dumey, "Indexing for Rapid Random Access Memory Systems," *Computers and Automation* 5(12):6–9 (December 1956)** — the first published description of hashing (with chaining) and the modulo-a-prime hash function, as documented by Knuth (TAOCP Vol. 3, §6.4) and standard hashing histories (e.g., Pagh's "Cuckoo Hashing"; Thorup, "High Speed Hashing for Integers and Strings"). Hans Peter Luhn's January 1953 internal IBM memorandum is the earliest *conception* (hashing with chaining) but was internal/unpublished. W. Wesley Peterson's "Addressing for Random-Access Storage," *IBM Journal of Research and Development* (1957), is a classic and coined the term "open addressing," but it is *not* the first public source — Dumey precedes it.
**Fix:** first-public-description / theory root = Dumey 1956; earliest conception = Luhn 1953 (internal); Peterson 1957 is influential but not the foundational public origin.

### 10. Tree
**ChatGPT:** theory = Cayley, "On the Theory of the Analytical Forms called Trees" (1857); implementation = Knuth TAOCP Vol. 1 (1997).
**Verdict: CONFIRM theory; FIX/qualify implementation.**
Theory-root: Arthur Cayley, "On the Theory of the Analytical Forms called Trees," *Philosophical Magazine*, Series 4, 13 (1857): 172–176, is the correct foundational mathematical treatment (and coined "tree"). **Confirmed.** (Note: K. G. C. von Staudt in 1847 and Gustav Kirchhoff in 1847 used tree structures earlier within proofs, but Cayley is the acknowledged root of tree *theory*.)
Implementation: Knuth's TAOCP Vol. 1 §2.3 is a canonical *reference* for tree representation/traversal, but is a synthesis, not the foundational implementation origin. Tree data-structure implementation in computing has no single clean root; Knuth documents and standardizes. Verdict: qualify Knuth as canonical reference, not origin.

### 11. Binary tree
**ChatGPT:** both = Knuth TAOCP Vol. 1 (1997).
**Verdict: FIX/qualify.**
Same issue: Knuth's TAOCP Vol. 1 §2.3.1 is the canonical reference for binary-tree representation and traversal, but is explicitly a synthesis of prior practice (Vol. 1 first published 1968), not the foundational root. The binary tree as a computing structure emerged in the late 1950s–early 1960s across multiple works. Knuth is the best single *reference* but should not be labeled the foundational origin.

### 12. Binary search tree
**ChatGPT:** theory = Windley, "Trees, Forests and Rearranging" (1960) AND Booth & Colin, "On the Efficiency of a New Method of Dictionary Construction" (1960); implementation = Hibbard, "Some Combinatorial Properties of Certain Trees with Applications to Searching and Sorting" (1962).
**Verdict: CONFIRM / ENUMERATE (well handled).**
The binary search tree was discovered independently c. 1960 by several researchers:
- P. F. Windley, "Trees, Forests and Rearranging," *The Computer Journal* 3(2):84 (1960).
- A. D. Booth & A. J. T. Colin, "On the Efficiency of a New Method of Dictionary Construction" (1960).
- Thomas N. Hibbard, "Some Combinatorial Properties of Certain Trees with Applications to Searching and Sorting," *Journal of the ACM* 9:13–28 (1962) — the earliest widely cited BST *algorithmic* treatment, a good implementation-root.
- Additionally, the method is attributed to Conway Berners-Lee and David Wheeler (magnetic-tape labeled-data storage, c. 1960).
ChatGPT's enumeration of the multiple 1960 origins plus Hibbard 1962 for implementation is accurate and well-founded. **Confirmed** as a correct multi-origin treatment; the only addition is the Berners-Lee/Wheeler attribution.

### 13. Heap
**ChatGPT:** theory = Williams, "Algorithm 232: Heapsort" (1964); implementation = Floyd, "Algorithm 245: Treesort 3" (1964).
**Verdict: CONFIRM.**
J. W. J. Williams, "Algorithm 232 — Heapsort," *Communications of the ACM* 7(6):347–348 (1964), introduced both the binary heap as a data structure and the heapsort algorithm. Robert W. Floyd, "Algorithm 245 — Treesort 3," *Communications of the ACM* 7(12):701 (1964), gave the in-place, linear-time bottom-up build-heap. The theory-root (Williams introduces the heap) / implementation-refinement (Floyd's efficient construction) split is drawn correctly. **Confirmed.** (Nuance: both are algorithm papers; Williams is the origin of the structure, Floyd the efficient construction — ChatGPT's labeling is essentially right.)

### 14. Priority queue
**ChatGPT:** theory = Crane, "Linear Lists and Priority Queues as Balanced Binary Trees" (1972); implementation = Williams, "Algorithm 232: Heapsort" (1964).
**Verdict: FIX.**
This attribution is mis-slotted. The priority queue *concept and its canonical implementation* originate with **J. W. J. Williams' binary heap (1964)** — the heap was introduced expressly as a priority-queue mechanism, and the literature dates "intense research on priority queues" from Williams 1964. Clark Allan Crane's 1972 Stanford PhD thesis, "Linear Lists and Priority Queues as Balanced Binary Trees" (STAN-CS-72-259), introduced the *leftist tree / leftist heap* (a mergeable priority queue) — an important but *later, specialized* development, not the theory-root of the priority queue in general.
**Fix:** the foundational root (both concept and first canonical implementation) is Williams 1964; Crane 1972 is a non-foundational later contribution (a specific mergeable-heap variant), sitting eight years downstream of the root. ChatGPT's implementation slot (Williams 1964) is correct, but its theory slot (Crane 1972) should be replaced by Williams 1964, with Crane noted as non-foundational.

### 15. Graph
**ChatGPT:** theory = Euler, "Solutio problematis ad geometriam situs pertinentis" (1741); implementation = Hopcroft & Tarjan, "Algorithm 447: Efficient Algorithms for Graph Manipulation" (1973).
**Verdict: CONFIRM (with date note).**
Theory-root: Leonhard Euler's Seven Bridges of Königsberg paper, "Solutio problematis ad geometriam situs pertinentis," is the founding paper of graph theory. **Date note:** it is standardly dated **1736** (presentation) with publication in *Commentarii Academiae Scientiarum Imperialis Petropolitanae*, vol. 8, pp. 128–140, appearing **1741**. ChatGPT's "1741" is the publication date and is defensible; most historians cite 1736. Both are correct depending on convention — flag the dual date.
Implementation: John E. Hopcroft & Robert Endre Tarjan, "Algorithm 447: Efficient Algorithms for Graph Manipulation," *Communications of the ACM* 16(6):372–378 (1973), is a defensible foundational source for efficient graph representation/manipulation (adjacency-structure algorithms). It is not the *only* candidate (adjacency-matrix/list representations predate it), but it is a reasonable, influential implementation anchor. **Confirmed** with the date nuance.

### 16. Record / struct
**ChatGPT:** theory = CODASYL, "Initial Specifications for a Common Business-Oriented Language" (1960); implementation = van Wijngaarden et al., "Revised Report on the Algorithmic Language ALGOL 68" (1978).
**Verdict: FIX.**
The typed-record concept as used today does **not** originate with COBOL/CODASYL. COBOL/FLOWMATIC (1959–1960) had hierarchical, statically nested records in the Data Division — a genuine earlier precedent for *named hierarchical data aggregates*, and C. A. R. (Tony) Hoare explicitly credited "Business Oriented Languages" for the named-field idea. But the foundational root of the **typed record / record class with typed references** — the modern data-type notion — is **C. A. R. Hoare, "Record Handling," ALGOL Bulletin No. 21, pp. 39–69 (1 November 1965)** (also as a book chapter in F. Genuys, ed., *Programming Languages*, Academic Press, pp. 291–346, 1968). Hoare introduced "record," "record class," the typed "reference" (pointer), dynamic allocation, and the null reference, explicitly building on John McCarthy's Cartesian-product "new types" proposal. Historian Simone Martini ("Several Types of Types in Programming Languages," 2015/2016) identifies this paper as where types "change their ontology — from an implementation issue, they programmatically become a general abstraction mechanism."
The foundational **implementation** root is **Niklaus Wirth & C. A. R. Hoare, "A Contribution to the Development of ALGOL," *Communications of the ACM* 9(6):413–432 (June 1966)**, which adopted Hoare's records ("replacement of tree structures by records as proposed by the second author") and was realized as ALGOL W (Stanford, IBM System/360). The ALGOL 68 Revised Report (A. van Wijngaarden, B. J. Mailloux, J. E. L. Peck, C. H. A. Koster, M. Sintzoff, C. H. Lindsey, L. G. L. T. Meertens, R. G. Fisker) was published in **Acta Informatica 5:1–236 (1975)** (Springer book edition 1976) — *not* 1978, which is the year of the German translation.
**Fix:** theory-root = Hoare 1965 (with COBOL 1960 as an acknowledged earlier hierarchical-record precedent, not the typed-record root); implementation-root = Wirth & Hoare / ALGOL W (1966), with ALGOL 68 (1975) as a later, more elaborate realization; correct the "1978" date to 1975.

### 17. String
**ChatGPT:** theory = Chomsky, "Three Models for the Description of Language" (1956); implementation = Farber, Griswold, Polonsky, "SNOBOL, A String Manipulation Language" (1964).
**Verdict: ENUMERATE / partial FIX.**
Implementation: David J. Farber, Ralph E. Griswold, and Ivan P. Polonsky, "SNOBOL, A String Manipulation Language," *Journal of the ACM* 11(1):21–30 (1964), is a strong, defensible foundational implementation root for the string as a manipulable data type in a programming language. **Confirmed** for implementation.
Theory: Noam Chomsky, "Three Models for the Description of Language," *IRE Transactions on Information Theory* 2(3):113–124 (1956), is the foundational text of *formal-language / string (symbol-sequence) theory* — it formalizes strings over an alphabet and grammars generating string sets. It is defensible as a theory-root for the *string as a formal object*, but it is arguably a category mismatch: Chomsky's subject is formal grammars, not the string *data structure* per se. A defensible alternative theory-root is the theory of free monoids / strings over an alphabet in formal-language and automata theory more broadly.
**Verdict:** Chomsky 1956 is a defensible theory anchor for string/formal-language theory; flag that it addresses formal languages rather than the string data structure directly, and that the string *data structure* has no single distinct theory paper beyond the formal-language lineage.

## Recommendations
1. **Adopt the FIXES** for:
   - Array — theory-root → Manchester Mark 1 index registers (1949, patent filed 3 June 1949 by Williams, Kilburn, Tootill, Robinson, Newman); keep FORTRAN 1957 as the *language-level* implementation root.
   - Hash table — public origin → Dumey 1956; Luhn 1953 as earliest (internal) conception; Peterson 1957 influential but not the origin.
   - Priority queue — root (concept + implementation) → Williams 1964; Crane 1972 marked non-foundational (leftist-heap variant).
   - Record/struct — typed-record root → Hoare 1965; implementation → Wirth & Hoare / ALGOL W 1966; correct ALGOL 68 date to 1975.
2. **Downgrade Knuth citations** (Queue, Deque, Tree-implementation, Binary tree) from "foundational root" to "canonical reference/synthesis," per the task's rule against substituting a modern reference for an absent foundational origin.
3. **Present multi-option structures** (Binary search tree, Set implementation, Map/dictionary, Stack theory-root, Graph theory date, String theory) as enumerated defensible options rather than single answers.
4. **Benchmark for revision:** if a primary source earlier than the cited one is located (e.g., a public hashing paper predating Dumey 1956, or a pre-1949 subscripted-variable machine realization), update the theory-root accordingly.

### Verdict summary table
| # | Structure | Theory-root verdict | Implementation-root verdict |
|---|-----------|--------------------|-----------------------------|
| 1 | Array | FIX (Manchester Mark 1 index registers, 1949) | Defensible (FORTRAN 1957) |
| 2 | Dynamic array/list | CONFIRM (Knuth as reference) | CONFIRM (no foundational root; Tarjan 1985 non-foundational) |
| 3 | Linked list | CONFIRM (IPL / Newell & Shaw 1957) | CONFIRM (same) |
| 4 | Stack | ENUMERATE (Turing 1946; Hamblin 1954/57; Bauer & Samelson strongest) | CONFIRM (Bauer & Samelson 1960) |
| 5 | Queue | FIX/qualify (no single root; Knuth = reference) | FIX/qualify (no root) |
| 6 | Deque | FIX/qualify (Knuth = reference) | FIX/qualify (no root) |
| 7 | Set | CONFIRM (Cantor 1895–97) | ENUMERATE (SETL 1970 defensible, not sole) |
| 8 | Map/dictionary | ENUMERATE (Lisp a-lists / SNOBOL4 / hash table) | Defensible (Griswold 1972) |
| 9 | Hash table | FIX (Dumey 1956 public; Luhn 1953 internal) | FIX (Dumey 1956, not Peterson 1957) |
| 10 | Tree | CONFIRM (Cayley 1857) | FIX/qualify (Knuth = reference) |
| 11 | Binary tree | FIX/qualify (Knuth = reference) | FIX/qualify (Knuth = reference) |
| 12 | Binary search tree | CONFIRM/ENUMERATE (Windley; Booth & Colin 1960; +Berners-Lee/Wheeler) | CONFIRM (Hibbard 1962) |
| 13 | Heap | CONFIRM (Williams 1964) | CONFIRM (Floyd 1964) |
| 14 | Priority queue | FIX (Williams 1964, not Crane 1972) | CONFIRM (Williams 1964) |
| 15 | Graph | CONFIRM (Euler 1736/1741) | CONFIRM (Hopcroft & Tarjan 1973) |
| 16 | Record/struct | FIX (Hoare 1965, not CODASYL 1960) | FIX (Wirth & Hoare/ALGOL W 1966; ALGOL 68 = 1975 not 1978) |
| 17 | String | ENUMERATE/partial FIX (Chomsky 1956 = formal-language, category caveat) | CONFIRM (Farber, Griswold, Polonsky 1964) |

## Caveats
- Several "origin" claims rely on secondary histories (Wikipedia, HandWiki, history-of-computing archives and blogs) corroborated against primary citations (CACM, Journal of the ACM, Acta Informatica, Philosophical Magazine, Mathematische Annalen, the University of Manchester Computer50 archive). Where possible I cite the primary publication.
- Dates given are years of definitive/last publication where the task requests; presentation vs. publication dates differ for Euler (1736 vs. 1741) and for conference-vs-journal versions (e.g., SNOBOL memoranda 1963 vs. JACM 1964; Hoare "Record Handling" ALGOL Bulletin 1965 vs. Academic Press book 1968).
- "Foundational" is inherently interpretive; for structures with diffuse origins (queue, deque, string), reasonable experts differ, and I have flagged these rather than forcing a single root.
- The subagent-verified record/struct findings (Hoare 1965 in ALGOL Bulletin No. 21; Wirth & Hoare CACM 1966; ALGOL 68 Revised Report in Acta Informatica 1975) are drawn from primary bibliographic records and Simone Martini's scholarly history; the claim that Hoare's 1966 follow-up added subclassing while ALGOL W tracked the 1965 version is from informed online commentary and is flagged as unverified.
- One residual uncertainty: the exact page range of the Wirth & Hoare 1966 CACM paper is cited as either 413–431 or 413–432 across sources; I report 413–432.