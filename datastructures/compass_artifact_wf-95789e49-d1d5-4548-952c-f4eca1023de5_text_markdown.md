# Topology of Data Structures: A Modern-Anchored, Bottom-Up Lineage Graph

## TL;DR
- Every modern data structure in the textbook canon, practitioner-standard set, and research frontier traces upward through a small number of verified intermediate structures to the 17 foundational roots — plus **8 back-filled foundational elements** (bit array, trie, associative array, multiset, priority-queue-as-ADT, self-balancing tree concept, B-tree, and approximate-membership) that the prior report omitted.
- The dominant lineage is the **tree → binary tree → binary search tree → self-balancing BST** spine, from which AVL, red-black, splay, treap, tango, and dozens of others descend; the second-densest is the **hash table** spine (cuckoo, Robin Hood, hopscotch, HAMT, Bloom/counting filters).
- Genuine relation-typed cycles exist (e.g., trie ⇄ hash table via HAMT, which *hybridizes* both; heap ⇄ BST via treap and Cartesian tree), and they arise only across differing relation types, exactly as the method requires.

## 1. Inclusion Rule (Bounding the Modern Set)

A data structure is **in scope** if it belongs to at least one of three tiers:

- **(a) Textbook canon** — anything taught in a standard advanced data-structures curriculum as represented by Cormen, Leiserson, Rivest & Stein (CLRS = Cormen, Leiserson, Rivest, Stein), Robert Sedgewick's *Algorithms*, and Donald Knuth's *The Art of Computer Programming* (TAOCP = The Art of Computer Programming).
- **(b) Practitioner-standard** — structures deployed in production systems (databases, editors, distributed systems, concurrent runtimes).
- **(c) Research-frontier / exotic** — structures appearing primarily in the algorithms research literature, including purely theoretical artifacts with no production implementation.

Completeness is measured against this rule. Each variant is its own node at full granularity; families are grouped only for readability.

## 2. Node Inventory

Foundational nodes carried over from the prior 17-structure report are marked **[F-prior]**. Newly back-filled foundational nodes are marked **[F-NEW]** with full foundational treatment. All others are modern nodes with a one-line identity.

### 2.1 Foundational Roots

**Carried over [F-prior]:** Array (Manchester Mark 1 B-lines, 1949; FORTRAN, 1957); Dynamic array; Linked list (Information Processing Language / IPL, Newell, Shaw & Simon, RAND, ~1956); Stack (Turing ACE, 1946; Bauer & Samelson "cellar," 1957–60); Queue; Deque; Set (Cantor, 1895–97; SETL = Set Language, Schwartz, 1970); Map/dictionary (Lisp association lists, ~1960; SNOBOL4); Hash table (Dumey, 1956; Luhn memo, 1953); Tree (Cayley, 1857); Binary tree; Binary search tree (Windley; Booth & Colin; Hibbard — all ~1960–62); Heap (Williams, 1964); Priority queue (Williams, 1964); Graph (Euler, 1741; Hopcroft & Tarjan Algorithm 447, 1973); Record/struct (Hoare, ~1965–66; ALGOL 68); String (Chomsky, 1956; SNOBOL, 1964).

**Back-filled foundational elements [F-NEW]:**

- **Bit array / bitmap [F-NEW]** — a compact array of bits addressed individually; the substrate of Bloom filters, roaring bitmaps, and succinct rank/select. *Theory root:* the concept is coextensive with the characteristic-vector representation of a subset of a finite universe (Cantorian set theory made concrete). *Implementation root:* pervasive from the earliest word-addressed machines; **no single foundational implementation paper exists** — flagged per the no-modern-substitute rule.
- **Trie (digital/prefix tree) [F-NEW]** — a tree keyed by successive symbols of the key, with shared prefixes. *Theory + implementation root:* Edward Fredkin, "Trie Memory," *Communications of the ACM* 3(9):490–499, 1960 (precursor: René de la Briandais, "File searching using variable length keys," Western Joint Computer Conference, 1959).
- **Associative array (as ADT distinct from map implementation) [F-NEW]** — the abstract key→value lookup interface. *Theory root:* Lisp association lists (~1960) and the general dictionary ADT. *Implementation root:* shares SNOBOL4 / Lisp roots with map; treated as the ADT layer above hash table and search tree.
- **Multiset / bag [F-NEW]** — a set permitting repeated elements (with multiplicity). *Theory root:* multiset theory (formalized by Blizard and others; roots in combinatorics). *Implementation root:* SETL supports tuples/sets; **no single foundational implementation paper** — flagged.
- **Priority-queue-as-ADT vs heap [F-NEW]** — the priority-queue abstract interface (insert, extract-min) as distinct from the binary-heap implementation. *Root:* John William Joseph Williams, "Algorithm 232: Heapsort," *Communications of the ACM* 7(6):347–348, 1964 introduced both the heap and its use as a priority queue; the ADT/implementation distinction is conceptual.
- **Self-balancing tree concept [F-NEW]** — the general principle of maintaining logarithmic height under updates via rotations/restructuring. *Theory + implementation root:* Georgy Adelson-Velsky & Evgenii Landis, "An algorithm for the organization of information," *Proceedings of the USSR Academy of Sciences* 146:263–266, 1962 (English translation by Myron J. Ricci in *Soviet Mathematics Doklady* 3:1259–1263, 1962) — the AVL tree, first self-balancing BST.
- **B-tree [F-NEW]** — a balanced multiway search tree for block/disk storage, minimum 50% node occupancy. *Theory + implementation root:* Rudolf Bayer & Edward M. McCreight, "Organization and Maintenance of Large Ordered Indexes," *Acta Informatica* 1(3):173–189, 1972 (first circulated as a Boeing Research Labs technical report, July 1970).
- **Approximate / probabilistic membership [F-NEW]** — space-efficient set membership permitting a controlled false-positive rate. *Theory + implementation root:* Burton H. Bloom, "Space/Time Trade-offs in Hash Coding with Allowable Errors," *Communications of the ACM* 13(7):422–426, 1970.

### 2.2 Tree-Family Modern Nodes

- **2-3 tree** — balanced search tree with 2- and 3-nodes; invented by John Hopcroft in 1970 and first described in print in Alfred Aho, John Hopcroft & Jeffrey Ullman, *The Design and Analysis of Computer Algorithms* (Addison-Wesley, 1974) and Knuth's TAOCP Vol. 3 (1973), which notes that a B-tree of order 3 is a 2-3 tree.
- **2-3-4 tree / 2-4 tree** — balanced search tree with 2-, 3-, and 4-nodes; the order-4 B-tree case; equivalent to Bayer's symmetric binary B-tree.
- **B+-tree** — B-tree variant storing all records in leaves with a linked leaf level; described by Knuth (TAOCP Vol. 3, 1973) and Douglas Comer's "The Ubiquitous B-tree," *ACM Computing Surveys* 11(2):121–137, 1979.
- **AVL tree** — height-balanced BST (subtree heights differ by ≤1); Adelson-Velsky & Landis, 1962.
- **Red-black tree** — BST with one color bit per node maintaining balance; Leonidas J. Guibas & Robert Sedgewick, "A Dichromatic Framework for Balanced Trees," 19th Annual Symposium on Foundations of Computer Science (FOCS), 1978, derived from Bayer's symmetric binary B-tree.
- **Symmetric binary B-tree** — Rudolf Bayer, "Symmetric binary B-Trees: Data structure and maintenance algorithms," *Acta Informatica* 1(4):290–306, 1972; the direct ancestor of red-black trees.
- **Left-leaning red-black tree** — simplified red-black variant; Robert Sedgewick, "Left-leaning Red-Black Trees," 2008.
- **Splay tree** — self-adjusting BST bringing accessed nodes to root; Daniel Sleator & Robert Tarjan, "Self-Adjusting Binary Search Trees," *Journal of the ACM* 32(3):652–686, 1985.
- **Treap / randomized BST** — BST + heap on random priorities; Raimund Seidel & Cecilia Aragon, "Randomized Search Trees," *Algorithmica* 16(4):464–497, 1996 (rediscovering Vuillemin's Cartesian tree; the term "treap" was first used by Edward McCreight ~1980 for a different structure).
- **Cartesian tree** — binary tree that is simultaneously a BST on position and a heap on value; introduced by Jean Vuillemin, "A Unifying Look at Data Structures," *Communications of the ACM* 23(4):229–239, 1980, in the context of geometric range searching.
- **Weight-balanced tree (BB[α])** — Jürg Nievergelt & Edward Reingold, "Binary search trees of bounded balance," ACM Symposium on Theory of Computing (STOC), 1972.
- **Scapegoat tree**, **AA tree**, **rank-balanced/WAVL tree** — later self-balancing BST variants (Haeupler, Sen & Tarjan gave rank-balanced trees).
- **Tango tree** — dynamically-optimal-within-O(log log n) BST; Erik Demaine, Dion Harmon, John Iacono & Mihai Pătrașcu, "Dynamic Optimality—Almost," FOCS 2004 (journal: *SIAM Journal on Computing* 37(1):240–251, 2007).
- **Link-cut tree (dynamic tree / ST-tree)** — maintains a forest under link/cut; Daniel Sleator & Robert Tarjan, "A Data Structure for Dynamic Trees," STOC 1981 (published 1983).
- **Euler tour tree** — dynamic-trees structure via BST over the Euler tour; Monika Henzinger & Valerie King, "Randomized dynamic graph algorithms with polylogarithmic time per operation," STOC 1995; simplified by Robert Tarjan, "Dynamic trees as search trees via Euler tours," *Mathematical Programming* 78:169–177, 1997.
- **Trie variants:** **Radix tree / PATRICIA** (Donald Morrison, "PATRICIA — Practical Algorithm to Retrieve Information Coded in Alphanumeric," *Journal of the ACM* 15(4):514–534, 1968); **ternary search tree**; **adaptive radix tree**; **HAMT** (see hash family); **suffix tree** (Peter Weiner, "Linear pattern matching algorithms," 14th IEEE Symposium on Switching and Automata Theory, 1973; refined by McCreight 1976 and Ukkonen 1995); **suffix array** (Manber & Myers, 1990).
- **van Emde Boas tree (stratified tree)** — O(log log u) integer priority queue; Peter van Emde Boas, "Preserving order in a forest in less than logarithmic time," FOCS 1975 (journal, with R. Kaas & E. Zijlstra, "Design and implementation of an efficient priority queue," *Mathematical Systems Theory* 10:99–127, 1976/77).
- **x-fast trie & y-fast trie** — Dan Willard, "Log-logarithmic worst-case range queries are possible in space Θ(N)," *Information Processing Letters* 17(2):81–84, 1983.
- **Fusion tree** — o(log n) integer search via word-level parallelism; Michael Fredman & Dan Willard, "Surpassing the information theoretic bound with fusion trees," ACM Symposium on Theory of Computing 1990 (journal: *Journal of Computer and System Sciences* 47(3):424–436, 1993).
- **Wavelet tree** — succinct sequence/text index; Roberto Grossi, Ankur Gupta & Jeffrey Scott Vitter, "High-order entropy-compressed text indexes," ACM-SIAM Symposium on Discrete Algorithms (SODA), 2003.
- **Segment tree** — range-query tree over intervals (Jon Bentley, ~1977, in the computational-geometry literature).
- **Fenwick tree / binary indexed tree** — cumulative-frequency structure via least-significant-bit index manipulation; Boris Ryabko, "A fast on-line code," *Soviet Mathematics Doklady* 39(3):533–537, 1989 (priority), popularized by Peter Fenwick, "A new data structure for cumulative frequency tables," *Software: Practice and Experience* 24(3):327–336, 1994.
- **Interval tree**, **range tree**, **priority search tree** — geometric query trees (priority search tree: McCreight).
- **Cache-oblivious B-tree** — Michael Bender, Erik Demaine & Martin Farach-Colton, "Cache-Oblivious B-Trees," FOCS 2000 (journal: *SIAM Journal on Computing* 35(2):341–358, 2005), within the cache-oblivious model of Matteo Frigo, Charles Leiserson, Harald Prokop & Sridhar Ramachandran, "Cache-Oblivious Algorithms," FOCS 1999.
- **Funnel heap** — cache-oblivious priority queue (Gerth Stølting Brodal & Rolf Fagerberg, 2002).

### 2.3 Spatial / Geometric Modern Nodes

- **k-d tree** — Jon Bentley, "Multidimensional binary search trees used for associative searching," *Communications of the ACM* 18(9):509–517, 1975.
- **Quadtree** — Raphael Finkel & Jon Bentley, "Quad Trees: A Data Structure for Retrieval on Composite Keys," *Acta Informatica* 4:1–9, 1974.
- **Octree** — 3-D analogue of the quadtree.
- **R-tree** — Antonin Guttman, "R-trees: A Dynamic Index Structure for Spatial Searching," ACM SIGMOD, 1984; variants **R*-tree** (Beckmann, Kriegel, Schneider & Seeger, 1990), **R+-tree** (Sellis, Roussopoulos & Faloutsos, 1987), **Hilbert R-tree**.
- **BSP tree (Binary Space Partitioning)** — Fuchs, Kedem & Naylor, 1980.
- **Bounding volume hierarchy (BVH)** — spatial hierarchy of bounding volumes for collision detection / ray tracing.

### 2.4 Heap-Family Modern Nodes

- **Binary heap** — John William Joseph Williams, 1964 (with Robert Floyd's O(n) build-heap, 1964).
- **Binomial heap** — Jean Vuillemin, "A data structure for manipulating priority queues," *Communications of the ACM* 21(4):309–314, 1978.
- **Fibonacci heap** — Michael Fredman & Robert Tarjan, "Fibonacci heaps and their uses in improved network optimization algorithms," *Journal of the ACM* 34(3):596–615, 1987 (developed 1984).
- **Pairing heap** — Michael Fredman, Robert Sedgewick, Daniel Sleator & Robert Tarjan, "The pairing heap: A new form of self-adjusting heap," *Algorithmica* 1(1):111–129, 1986.
- **Soft heap** — Bernard Chazelle, "The Soft Heap: An Approximate Priority Queue with Optimal Error Rate," *Journal of the ACM* 47(6):1012–1027, 2000.
- **Brodal queue** — worst-case-optimal meldable priority queue (Gerth Stølting Brodal, 1996).
- **Leftist heap, skew heap, d-ary heap, 2-3 heap, rank-pairing heap** — further heap variants.

### 2.5 Hash-Family Modern Nodes

- **Separate chaining** and **open addressing (linear/quadratic probing, double hashing)** — classical collision-resolution schemes.
- **Cuckoo hashing** — Rasmus Pagh & Flemming Friche Rodler, "Cuckoo Hashing," European Symposium on Algorithms (ESA), 2001 (journal: *Journal of Algorithms* 51(2):122–144, 2004).
- **Robin Hood hashing** — Pedro Celis, Per-Åke Larson & J. Ian Munro, "Robin Hood Hashing," FOCS 1985.
- **Hopscotch hashing** — Maurice Herlihy, Nir Shavit & Moran Tzafrir, "Hopscotch Hashing," International Symposium on Distributed Computing (DISC), 2008.
- **HAMT (Hash Array Mapped Trie)** — Phil Bagwell, "Ideal Hash Trees," EPFL technical report, 2001 (building on his "Fast and Space Efficient Trie Searches," 2000).
- **Dynamic perfect hashing** — Dietzfelbinger, Karlin, Mehlhorn, Meyer auf der Heide, Rohnert & Tarjan, 1994; **FKS perfect hashing** — Fredman, Komlós & Szemerédi, 1984.

### 2.6 Probabilistic / Approximate Modern Nodes

- **Bloom filter** — Burton Bloom, 1970 (foundational, see §2.1).
- **Counting Bloom filter**, **spectral Bloom filter**, **Bloomier filter** — Bloom-filter extensions.
- **Quotient filter** — compact hash-based approximate membership (Bender et al., 2012).
- **Cuckoo filter** — Fan, Andersen, Kaminsky & Mitzenmacher, 2014.
- **Count-min sketch** — Graham Cormode & S. Muthukrishnan, "An improved data stream summary: The Count-Min Sketch and its applications," *Journal of Algorithms* 55(1):58–75, 2005.
- **HyperLogLog** — Philippe Flajolet, Éric Fusy, Olivier Gandouet & Frédéric Meunier, "HyperLogLog: the analysis of a near-optimal cardinality estimation algorithm," Analysis of Algorithms (AofA), 2007 (predecessor: Flajolet & Martin, "Probabilistic counting algorithms for data base applications," 1985).

### 2.7 Storage / Systems Modern Nodes

- **LSM-tree (Log-Structured Merge tree)** — Patrick O'Neil, Edward Cheng, Dieter Gawlick & Elizabeth O'Neil, "The log-structured merge-tree (LSM-tree)," *Acta Informatica* 33(4):351–385, 1996 (originating from a 1991 University of Massachusetts Boston technical report).
- **Learned index** — Tim Kraska, Alex Beutel, Ed H. Chi, Jeffrey Dean & Neoklis Polyzotis, "The Case for Learned Index Structures," ACM SIGMOD, 2018.
- **Merkle tree (hash tree)** — Ralph Merkle, Stanford PhD thesis "Secrecy, Authentication, and Public Key Systems," 1979 (definitive published paper: "A Digital Signature Based on a Conventional Encryption Function," CRYPTO '87, 1987/1988).
- **Roaring bitmap** — Samy Chambi, Daniel Lemire, Owen Kaser & Robert Godin, "Better bitmap performance with Roaring bitmaps," *Software: Practice and Experience* 46(5):709–719, 2016.

### 2.8 Text / Sequence Modern Nodes

- **Rope** — Hans-J. Boehm, Russ Atkinson & Michael Plass, "Ropes: an Alternative to Strings," *Software: Practice and Experience* 25(12):1315–1330, 1995.
- **Gap buffer** — folklore text-editor structure (TECO/Emacs, late 1970s); **no origin paper**.
- **Piece table** — text-editor structure with conflicting attribution (Bravo editor, Xerox PARC, Butler Lampson & Charles Simonyi, mid-1970s; also credited to J Strother Moore); **no canonical origin paper**.

### 2.9 Concurrent / Persistent / Functional Modern Nodes

- **Michael-Scott queue** — lock-free FIFO queue; Maged M. Michael & Michael L. Scott, "Simple, Fast, and Practical Non-Blocking and Blocking Concurrent Queue Algorithms," 15th Annual ACM Symposium on Principles of Distributed Computing (PODC '96), pp. 267–275, 1996.
- **Lock-free / Treiber stack** — R. Kent Treiber, "Systems Programming: Coping with Parallelism," IBM Almaden Research Center Technical Report RJ 5118, April 1986.
- **Persistent data structures (fat node, path copying)** — James Driscoll, Neil Sarnak, Daniel Sleator & Robert Tarjan, "Making Data Structures Persistent," *Journal of Computer and System Sciences* 38(1):86–124, 1989 (STOC 1986).
- **Finger tree** — Ralf Hinze & Ross Paterson, "Finger trees: a simple general-purpose data structure," *Journal of Functional Programming* 16(2):197–217, 2006.
- **Retroactive data structures** — Demaine, Iacono & Langerman, 2007.
- **Succinct data structures** — Guy Jacobson, "Space-efficient Static Trees and Graphs," FOCS 1989.
- **Union-find / disjoint-set** — Bernard Galler & Michael Fisher, "An improved equivalence algorithm," *Communications of the ACM*, 1964 (amortized analysis: Hopcroft & Ullman 1973; Tarjan & van Leeuwen 1984).
- **Ring / circular buffer** — bounded FIFO over a fixed array; folklore.

## 3. Typed Edge List (Grouped by Foundational Lineage, Root → Modern)

Edge relations: **refines / generalizes / specializes / hybridizes / encodes / influences**. Presented root→modern.

### 3.1 Descent from TREE
- Tree → *specializes* → Binary tree
- Tree → *specializes* → Trie [F-NEW]
- Tree → *specializes* → B-tree [F-NEW]
- Tree → *specializes* → Quadtree; Tree → *specializes* → Octree
- Tree → *specializes* → BSP tree; Tree → *generalizes* → Bounding volume hierarchy

### 3.2 Descent from BINARY TREE
- Binary tree → *specializes* → Binary search tree
- Binary tree → *encodes* → Binary heap (implicit complete binary tree in an array)
- Binary tree → *specializes* → Cartesian tree

### 3.3 Descent from BINARY SEARCH TREE (the densest spine)
- Binary search tree → *refines* (via self-balancing concept [F-NEW]) → AVL tree
- Binary search tree → *refines* → Weight-balanced tree BB[α]
- Symmetric binary B-tree → *refines* → Red-black tree; 2-3-4 tree → *encodes* → Red-black tree
- Red-black tree → *refines* → Left-leaning red-black tree
- Binary search tree → *refines* → Splay tree
- Binary search tree + Binary heap → *hybridizes* → Treap
- Cartesian tree → *influences* → Treap
- Binary search tree → *refines* → Scapegoat tree; AA tree; rank-balanced (WAVL) tree
- Balanced BST + link-cut auxiliary trees → *refines* → Tango tree
- Splay tree → *specializes* → Link-cut tree
- Balanced BST → *encodes* (Euler tour) → Euler tour tree
- Binary search tree → *specializes* (multidimensional) → k-d tree
- Binary search tree → *refines* (persistence) → Persistent BST (fat node / path copying)

### 3.4 Descent from B-TREE [F-NEW]
- B-tree → *specializes* → 2-3 tree (order-3 case); B-tree → *specializes* → 2-3-4 tree (order-4 case)
- B-tree → *refines* → B+-tree
- 2-3 tree → *specializes* → 2-3-4 tree
- B-tree → *refines* (word-parallel nodes) → Fusion tree
- B-tree → *refines* (cache-oblivious layout) → Cache-oblivious B-tree
- B-tree → *influences* → LSM-tree (write-optimized alternative to B-tree indexing)
- B-tree index → *influences* (learned model replaces the tree) → Learned index
- B-tree → *generalizes* (spatial) → R-tree; R-tree → *refines* → R*-tree, R+-tree, Hilbert R-tree

### 3.5 Descent from TRIE [F-NEW]
- Trie → *refines* → Radix tree / PATRICIA
- Trie → *specializes* → Ternary search tree; Adaptive radix tree
- Trie → *specializes* (over suffixes) → Suffix tree
- Trie + Hash table → *hybridizes* → HAMT
- Trie → *influences* → van Emde Boas tree (bit-recursive trie over the universe)
- van Emde Boas tree → *refines* (space reduction via hashing) → x-fast trie → *refines* → y-fast trie

### 3.6 Descent from HEAP / PRIORITY QUEUE
- Priority queue (ADT) [F-NEW] → *specializes* → Binary heap
- Binary heap → *generalizes* → d-ary heap
- Binomial tree → *encodes* → Binomial heap
- Binomial heap → *refines* → Fibonacci heap
- Fibonacci heap → *refines* → Pairing heap
- Binomial heap → *refines* (approximate, bounded corruption) → Soft heap
- Binary heap → *refines* → Leftist heap; Skew heap; 2-3 heap; Rank-pairing heap; Brodal queue
- Cache-oblivious model → *refines* → Funnel heap
- van Emde Boas tree → *specializes* → integer priority queue (vEB as PQ)

### 3.7 Descent from HASH TABLE
- Hash table → *refines* → Separate chaining; Open addressing
- Open addressing → *refines* → Cuckoo hashing; Robin Hood hashing; Hopscotch hashing
- Hash table → *refines* → Dynamic perfect hashing; FKS perfect hashing
- Hash table + Trie → *hybridizes* → HAMT

### 3.8 Descent from SET / APPROXIMATE MEMBERSHIP [F-NEW] and BIT ARRAY [F-NEW]
- Set → *specializes* → Multiset / bag [F-NEW]
- Bit array [F-NEW] + Hash table → *hybridizes* → Bloom filter [F-NEW]
- Bloom filter → *refines* → Counting Bloom filter; Spectral Bloom filter; Bloomier filter
- Hash table → *refines* (approximate) → Quotient filter; Cuckoo filter
- Bit array → *encodes* → Roaring bitmap (two-level array/bitmap containers)
- Hash + counter array → *encodes* → Count-min sketch
- Hash + register array → *encodes* → HyperLogLog

### 3.9 Descent from ARRAY / DYNAMIC ARRAY
- Array → *refines* → Dynamic array
- Array → *specializes* → Bit array [F-NEW]
- Array → *encodes* → Binary heap; Fenwick tree; Segment tree
- Array + movable gap → *refines* → Gap buffer
- Dynamic array → *refines* → Ring / circular buffer
- Segment tree → *refines* (LSB indexing) → Fenwick tree

### 3.10 Descent from STRING / LINKED LIST
- String → *refines* (balanced tree over fragments) → Rope
- String → *refines* (span index over buffers) → Piece table
- Linked list → *refines* (lock-free) → Treiber stack; Michael-Scott queue
- Linked list + probabilistic levels → *hybridizes* → Skip list (William Pugh, "Skip lists: a probabilistic alternative to balanced trees," *Communications of the ACM* 33(6):668–676, 1990)

### 3.11 Descent from GRAPH and DISJOINT-SET
- Graph → *influences* → Union-find / disjoint-set forest
- Tree (forest of trees) → *encodes* → Union-find
- Graph algorithms → *influence* → Link-cut tree, Euler tour tree (dynamic connectivity)

### 3.12 Descent to SUCCINCT / FINGER / RETROACTIVE / CRYPTOGRAPHIC
- Bit array + rank/select → *encodes* → Succinct data structures (Jacobson)
- Succinct bit-vectors → *encode* → Wavelet tree; Trie → *influences* → Wavelet tree
- 2-3 tree → *refines* (functional, amortized) → Finger tree
- Persistent structures → *generalize* → Retroactive data structures
- Binary tree + cryptographic hash → *hybridizes* → Merkle tree

## 4. Cycles and the Relation Types That Produce Them

Per the method, a genuine cycle must cross differing relation types. The following were found:

1. **Trie ⇄ Hash table (via HAMT).** Hash table → *hybridizes* → HAMT and Trie → *hybridizes* → HAMT; conversely HAMT is used to *implement* (encodes) associative arrays that back a hash-map interface. The cross-type loop (hybridizes vs. encodes) is genuine: the HAMT is simultaneously a descendant of both parents and an implementation substitute for one of them.
2. **Heap ⇄ Binary search tree (via treap / Cartesian tree).** Binary search tree + Binary heap → *hybridizes* → Treap, while Cartesian tree → *influences* → Treap and Binary tree → *specializes* → Cartesian tree (which is itself both a BST-on-position and a heap-on-value). The BST and heap ordering invariants meet in one node, producing a cross-relation cycle (specializes vs. hybridizes).
3. **van Emde Boas tree ⇄ Priority queue.** vEB is *specialized from* the trie/associative-array lineage yet *specializes* the priority-queue ADT (it is literally called the "van Emde Boas priority queue") — a loop across influences/specializes.
4. **B-tree ⇄ Binary search tree.** B-tree *generalizes* the binary search tree (more children per node), while the red-black tree (a BST) *encodes* a 2-3-4 tree (a B-tree). The generalizes/encodes pair forms a legitimate cross-type cycle between the two spines.

Same-relation "cycles" (e.g., A generalizes B while B specializes A) are **not** counted as cycles, per the rule; those are simply inverse edges of one relation.

## 5. Back-Filled Foundational Elements (Additions to the Prior 17)

The following eight were reached by upward traces and are added with full foundational treatment (see §2.1): **Bit array/bitmap** (theory = characteristic vector; no single implementation paper — flagged); **Trie** (Fredkin, 1960); **Associative array as ADT** (Lisp/SNOBOL4 roots); **Multiset/bag** (multiset theory; no single implementation paper — flagged); **Priority-queue-as-ADT** (Williams, 1964); **Self-balancing tree concept** (AVL: Adelson-Velsky & Landis, 1962); **B-tree** (Bayer & McCreight, 1972); **Approximate/probabilistic membership** (Bloom, 1970).

## 6. Recommendations

- **For a teaching or reference artifact:** organize the graph around the four densest spines — BST/self-balancing, B-tree, trie, and hash table — and present the heap and probabilistic families as secondary clusters. This matches how CLRS and Sedgewick sequence the material and maximizes navigability. Benchmark: if a candidate structure cannot be attached to one of these four spines plus the array/heap/graph roots, treat that as a signal to add a new foundational back-fill node rather than forcing a fit.
- **For a rigor threshold:** treat a lineage claim as *verified* only when an origin paper with named authors and venue is confirmed (as done here for AVL, red-black, B-tree, splay, treap, van Emde Boas, fusion, tango, LSM, HAMT, Bloom, count-min, HyperLogLog, cuckoo, Robin Hood, hopscotch, Fibonacci/pairing/soft heaps, persistent, finger, succinct, and others). Treat gap buffer and piece table as *conjectural-origin* nodes: they have no canonical paper and should be labeled folklore.
- **Escalation trigger:** if a downstream consumer needs the *implementation-root* slots filled for the two flagged theory-only foundational nodes (bit array, multiset), do not substitute a modern structure — surface the flag, per the method's no-substitute rule. The threshold that would change this: discovery of a primary source that introduces the structure *as an implemented artifact* (not merely uses it), at which point it graduates from flagged to fully treated.

## 7. Caveats

- **Merkle tree year is genuinely ambiguous:** the invention is in Merkle's 1979 Stanford PhD thesis and 1979 patent filing (US 4,309,569, issued 1982), but the definitive published paper is CRYPTO '87 (proceedings LNCS 293, 1988). All are defensible; select per citation purpose.
- **Fenwick/binary indexed tree priority:** Boris Ryabko (1989) has priority over Peter Fenwick (1994); the popular name honors Fenwick. Both are cited; the two were independent inventions.
- **Piece table and gap buffer** lack canonical origin papers; attributions conflict (piece table: Lampson/Simonyi at Xerox PARC's Bravo editor, mid-1970s, vs. J Strother Moore). These are flagged as folklore.
- **Segment tree** attribution is less crisply documented than the others (commonly credited to Bentley, ~1977, in the computational-geometry literature); treated as verified-but-soft.
- **Treap terminology:** "treap" was first coined by Edward McCreight (~1980) for what he later renamed the priority search tree; the modern treap is Seidel & Aragon's independent randomized-BST construction, itself a rediscovery of Vuillemin's 1980 Cartesian tree. The naming trail is a known source of confusion.
- Several "influences" edges (e.g., B-tree → learned index) are conceptual/design-inspiration rather than genealogical descent; they are labeled *influences* precisely to distinguish inspiration from structural lineage.
- The inventory is bounded by the inclusion rule but is not exhaustive; the algorithms literature contains many further variants (e.g., every additional heap and self-balancing BST variant) that occupy the same lineage slots as their listed siblings.