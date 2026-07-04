# build/nodes.py — PHASE 1: transcribed node facts (the ONLY place the two reports are read).
# Each record is a data-structure NODE. Facts are drawn verbatim from:
#   audit    = "Audit of ChatGPT's Foundational Source Answers for 17 Data Structures"
#              (compass_artifact_wf-1f7348c0-...): supplies CORRECTED foundational citations
#              + the CONFIRM / FIX / ENUMERATE verdict for each of the 17 roots.
#   topology = "Topology of Data Structures: A Modern-Anchored, Bottom-Up Lineage Graph"
#              (compass_artifact_wf-95789e49-...): supplies the modern inventory (§2) and the
#              typed edge list (§3-§4, see edges.py).
# No citation, author, year or venue here is invented: where a report gives none, the node is
# marked verification="flagged" with the reason in `flags`, per topology §6 (rigor threshold)
# and the manifest anti-fabrication discipline. `verdict` mirrors the audit's own labels.

# tier:         root (audit's 17 foundational) | backfill (topology's 8 [F-NEW]) | modern
# verification: verified (named authors + venue confirmed) | flagged (folklore / theory-only /
#               diffuse / uncited-in-source / ambiguous — reason in flags)
# verdict:      CONFIRM | FIX | ENUMERATE | ''   (audit verdict; empty for modern nodes)


def N(id, name, family, tier, year, origin, verification, verdict="", reports=("topology",),
      flags=(), note=""):
    return dict(id=id, name=name, family=family, tier=tier, year=year, origin=origin,
                verification=verification, verdict=verdict, reports=list(reports),
                flags=list(flags), note=note)


NODES = [
    # ─────────────────────────── FOUNDATIONAL ROOTS (audit's 17) ───────────────────────────
    N("array", "Array", "linear", "root", 1949,
      "Manchester Mark 1 index registers / B-lines (Williams, Kilburn, Tootill, Robinson, "
      "Newman), patent filed 3 Jun 1949; high-level-language array: Backus et al., FORTRAN, 1957",
      "verified", "FIX", ("audit", "topology"),
      note="Audit FIX: index registers / subscripted variables predate FORTRAN. FORTRAN "
           "(1954 spec / 1957 impl) is the root only of the high-level-language array abstraction."),
    N("dynarray", "Dynamic array / list", "linear", "root", None,
      "No single foundational paper. Knuth, TAOCP Vol.1 §2.2 = canonical reference (synthesis); "
      "amortization analysis: Tarjan, SIAM J. Alg. Disc. Meth. 6(2), 1985 (later, non-foundational)",
      "flagged", "CONFIRM", ("audit", "topology"), ("diffuse-origin",),
      note="Self-resizing O(1)-amortized-append array has no single origin paper; Tarjan 1985 "
           "analyses rather than invents it."),
    N("linkedlist", "Linked list", "linear", "root", 1957,
      "Newell & Shaw, 'Programming the Logic Theory Machine', WJCC 1957 (IPL; developed 1955-56 "
      "with Simon at RAND / Carnegie Tech)",
      "verified", "CONFIRM", ("audit", "topology")),
    N("stack", "Stack", "linear", "root", 1960,
      "Bauer & Samelson, 'Sequential Formula Translation', CACM 3(2):76-83, 1960 "
      "(Operationskeller, 1955; patent 1957). Earliest: Turing ACE reports, 1946; independent: "
      "Hamblin 1954/57; Kämmerer",
      "verified", "ENUMERATE", ("audit", "topology"),
      note="Audit ENUMERATE: Bauer & Samelson strongest as the named data structure; Turing "
           "(1946) is the earliest LIFO appearance, Hamblin an independent origin."),
    N("queue", "Queue", "linear", "root", None,
      "No single foundational paper; ancient FIFO concept. Knuth, TAOCP Vol.1 §2.2.1 = canonical "
      "reference definition (synthesis, decades from any origin)",
      "flagged", "FIX", ("audit", "topology"), ("diffuse-origin",),
      note="Audit FIX/qualify: definitional and diffuse; citing Knuth as the root overstates it."),
    N("deque", "Deque (double-ended queue)", "linear", "root", None,
      "Term and variants canonically defined by Knuth, TAOCP Vol.1 §2.2.1 (reference, not origin); "
      "no distinct earlier single-source origin",
      "flagged", "FIX", ("audit", "topology"), ("diffuse-origin",),
      note="Audit FIX/qualify, same reasoning as Queue."),
    N("set", "Set", "assoc", "root", 1895,
      "Cantor, 'Beiträge zur Begründung der transfiniten Mengenlehre', Math. Annalen 46 (1895) & "
      "49 (1897). Impl: Schwartz, SETL, Courant Institute, 1970 (defensible, not sole)",
      "verified", "ENUMERATE", ("audit", "topology"),
      note="Audit: Cantor confirmed for theory; SETL one defensible implementation option "
           "(sets are also realized via hash tables / trees / bit-vectors)."),
    N("map", "Map / dictionary", "assoc", "root", 1971,
      "Enumerate: SNOBOL4 built-in 'table' (Griswold, Poage & Polonsky, 1971; impl 1972); Lisp "
      "association lists (~1960, earlier conceptual key-value); hash table (Dumey 1956) as substrate",
      "verified", "ENUMERATE", ("audit", "topology"),
      note="Audit ENUMERATE: SNOBOL4 defensible for the built-in feature; a-lists earlier "
           "conceptually; hash table the implementation substrate."),
    N("hashtable", "Hash table", "hash", "root", 1956,
      "Dumey, 'Indexing for Rapid Random Access Memory Systems', Computers & Automation 5(12), "
      "Dec 1956 (first PUBLIC description). Luhn IBM memo, Jan 1953 (earliest, internal); "
      "Peterson, IBM JRD 1957 (coined 'open addressing', not first)",
      "verified", "FIX", ("audit", "topology"),
      note="Audit FIX: Dumey 1956 is the foundational public source; Peterson 1957 is influential "
           "but is preceded by Dumey."),
    N("tree", "Tree", "tree", "root", 1857,
      "Cayley, 'On the Theory of the Analytical Forms called Trees', Philosophical Magazine s.4, "
      "13:172-176, 1857 (coined 'tree'). Impl: Knuth TAOCP Vol.1 §2.3 = reference, not origin",
      "verified", "CONFIRM", ("audit", "topology"),
      note="Audit: Cayley confirmed for theory; von Staudt & Kirchhoff (1847) used trees earlier "
           "within proofs. Knuth is a canonical implementation reference, not the origin."),
    N("binarytree", "Binary tree", "tree", "root", None,
      "Knuth, TAOCP Vol.1 §2.3.1 = canonical reference for representation/traversal (synthesis of "
      "late-1950s-early-1960s practice), not a foundational root",
      "flagged", "FIX", ("audit", "topology"), ("reference-not-origin",),
      note="Audit FIX/qualify: Knuth is the best single reference but not the origin; the binary "
           "tree emerged across multiple works with no clean single root."),
    N("bst", "Binary search tree", "tree", "root", 1960,
      "Independently ~1960: Windley, Computer Journal 3(2), 1960; Booth & Colin, 1960; Hibbard, "
      "JACM 9:13-28, 1962 (implementation root); also Berners-Lee & Wheeler",
      "verified", "ENUMERATE", ("audit", "topology"),
      note="Audit CONFIRM/ENUMERATE: multi-origin 1960 discovery, Hibbard 1962 the algorithmic "
           "implementation root."),
    N("binaryheap", "Binary heap (Heap)", "heap", "root", 1964,
      "Williams, 'Algorithm 232: Heapsort', CACM 7(6):347-348, 1964 (introduced the binary heap); "
      "Floyd, 'Algorithm 245: Treesort 3', CACM 7(12):701, 1964 (O(n) bottom-up build)",
      "verified", "CONFIRM", ("audit", "topology"),
      note="Audit CONFIRM: Williams originates the structure, Floyd the efficient construction. "
           "The audit's 'Heap' root, unified here with topology's modern 'Binary heap' node."),
    N("priorityqueue", "Priority queue (ADT)", "heap", "root", 1964,
      "Williams, 'Algorithm 232: Heapsort', CACM 7(6), 1964 — the heap was introduced expressly "
      "as a priority-queue mechanism. Crane's 1972 leftist heap is a later, specialised variant",
      "verified", "FIX", ("audit", "topology"), ("adt-layer",),
      note="Audit FIX: root is Williams 1964, not Crane 1972. Also topology's [F-NEW] "
           "priority-queue-as-ADT (the abstract insert/extract-min interface above the heap)."),
    N("graph", "Graph", "advanced", "root", 1736,
      "Euler, 'Solutio problematis ad geometriam situs pertinentis' (Seven Bridges of "
      "Königsberg), presented 1736, published 1741. Impl: Hopcroft & Tarjan, 'Algorithm 447', "
      "CACM 16(6):372-378, 1973",
      "verified", "CONFIRM", ("audit", "topology"), ("ambiguous-date",),
      note="Audit CONFIRM with dual-date note: 1736 (presentation) vs 1741 (publication); most "
           "historians cite 1736."),
    N("record", "Record / struct", "linear", "root", 1965,
      "Hoare, 'Record Handling', ALGOL Bulletin No.21:39-69, 1 Nov 1965 (typed record, record "
      "class, typed reference). Impl: Wirth & Hoare / ALGOL W, CACM 9(6):413-432, 1966; ALGOL 68 "
      "Revised Report, Acta Informatica 5:1-236, 1975",
      "verified", "FIX", ("audit", "topology"),
      note="Audit FIX: root is Hoare 1965, not CODASYL/COBOL 1960 (an earlier hierarchical-record "
           "precedent). Correct the ALGOL 68 date to 1975 (1978 = German translation)."),
    N("string", "String", "trie", "root", 1964,
      "Impl: Farber, Griswold & Polonsky, 'SNOBOL, A String Manipulation Language', JACM 11(1):"
      "21-30, 1964. Theory: Chomsky, 'Three Models for the Description of Language', IRE Trans. "
      "Inf. Theory 2(3), 1956",
      "verified", "ENUMERATE", ("audit", "topology"),
      note="Audit: SNOBOL confirmed for implementation; Chomsky 1956 a defensible theory anchor "
           "but addresses formal languages, not the string data structure directly (category caveat)."),

    # ─────────────────────── BACK-FILLED FOUNDATIONAL (topology's 8 [F-NEW]) ───────────────────────
    N("bitarray", "Bit array / bitmap", "linear", "backfill", None,
      "Theory: characteristic-vector representation of a subset of a finite universe (set theory "
      "made concrete). NO single foundational implementation paper exists",
      "flagged", "", ("topology",), ("theory-only",),
      note="topology [F-NEW]: flagged per the no-modern-substitute rule; pervasive from the "
           "earliest word-addressed machines."),
    N("trie", "Trie (digital / prefix tree)", "trie", "backfill", 1960,
      "Fredkin, 'Trie Memory', CACM 3(9):490-499, 1960 (precursor: de la Briandais, 'File "
      "searching using variable length keys', WJCC 1959)",
      "verified", "", ("topology",)),
    N("assocarray", "Associative array (ADT)", "assoc", "backfill", 1960,
      "The abstract key→value interface, distinct from map implementation. Roots: Lisp "
      "association lists (~1960) and the general dictionary ADT (shares SNOBOL4 roots with Map)",
      "verified", "", ("topology",), ("adt-layer",),
      note="topology [F-NEW]: the ADT layer above hash table and search tree."),
    N("multiset", "Multiset / bag", "assoc", "backfill", None,
      "Theory: multiset theory (Blizard and others; roots in combinatorics). NO single "
      "foundational implementation paper exists",
      "flagged", "", ("topology",), ("theory-only",),
      note="topology [F-NEW]: flagged; SETL supports tuples/sets but no single impl paper."),
    N("selfbalancing", "Self-balancing tree (concept)", "tree", "backfill", 1962,
      "The general principle of maintaining logarithmic height under updates via rotations / "
      "restructuring. Theory + impl root: Adelson-Velsky & Landis (AVL), 1962 — the first "
      "self-balancing BST",
      "verified", "", ("topology",),
      note="topology [F-NEW]: the connective concept from which AVL, red-black, splay, treap, "
           "tango and dozens more descend."),
    N("btree", "B-tree", "tree", "backfill", 1972,
      "Bayer & McCreight, 'Organization and Maintenance of Large Ordered Indexes', Acta "
      "Informatica 1(3):173-189, 1972 (first as a Boeing Research Labs tech report, Jul 1970)",
      "verified", "", ("topology",)),
    N("bloomfilter", "Bloom filter", "approx", "backfill", 1970,
      "Bloom, 'Space/Time Trade-offs in Hash Coding with Allowable Errors', CACM 13(7):422-426, "
      "1970 (space-efficient membership with a controlled false-positive rate)",
      "verified", "", ("topology",)),

    # ───────────────────────────── MODERN — TREE FAMILY (§2.2) ─────────────────────────────
    N("avl", "AVL tree", "tree", "modern", 1962,
      "Adelson-Velsky & Landis, 'An algorithm for the organization of information', Proc. USSR "
      "Acad. Sci. 146:263-266, 1962 (Eng. transl. Soviet Math. Doklady 3:1259-1263)",
      "verified"),
    N("redblack", "Red-black tree", "tree", "modern", 1978,
      "Guibas & Sedgewick, 'A Dichromatic Framework for Balanced Trees', FOCS 1978 (derived from "
      "Bayer's symmetric binary B-tree)", "verified"),
    N("symbin", "Symmetric binary B-tree", "tree", "modern", 1972,
      "Bayer, 'Symmetric binary B-Trees: Data structure and maintenance algorithms', Acta "
      "Informatica 1(4):290-306, 1972 (direct ancestor of red-black trees)", "verified"),
    N("llrb", "Left-leaning red-black tree", "tree", "modern", 2008,
      "Sedgewick, 'Left-leaning Red-Black Trees', 2008 (simplified red-black variant)", "verified"),
    N("splay", "Splay tree", "tree", "modern", 1985,
      "Sleator & Tarjan, 'Self-Adjusting Binary Search Trees', JACM 32(3):652-686, 1985", "verified"),
    N("treap", "Treap / randomized BST", "tree", "modern", 1996,
      "Seidel & Aragon, 'Randomized Search Trees', Algorithmica 16(4):464-497, 1996 (rediscovers "
      "Vuillemin's Cartesian tree)", "verified", flags=("ambiguous-name",),
      note="'treap' was first used by McCreight (~1980) for a different structure — a known "
           "source of naming confusion."),
    N("cartesian", "Cartesian tree", "tree", "modern", 1980,
      "Vuillemin, 'A Unifying Look at Data Structures', CACM 23(4):229-239, 1980 (BST-on-position "
      "and heap-on-value simultaneously)", "verified"),
    N("weightbalanced", "Weight-balanced tree BB[α]", "tree", "modern", 1972,
      "Nievergelt & Reingold, 'Binary search trees of bounded balance', STOC 1972", "verified"),
    N("scapegoat", "Scapegoat tree", "tree", "modern", None,
      "Later self-balancing BST variant; origin paper not stated in the source", "flagged",
      flags=("origin-not-in-report",),
      note="topology §2.2 groups it as a 'later self-balancing BST variant' without a citation."),
    N("aatree", "AA tree", "tree", "modern", None,
      "Later self-balancing BST variant; origin paper not stated in the source", "flagged",
      flags=("origin-not-in-report",),
      note="topology §2.2 groups it without a citation."),
    N("wavl", "Rank-balanced (WAVL) tree", "tree", "modern", None,
      "Rank-balanced trees; Haeupler, Sen & Tarjan (venue / year not stated in the source)",
      "verified", flags=("origin-not-in-report",),
      note="Named authors given in topology §2.2; venue and year not stated."),
    N("tango", "Tango tree", "tree", "modern", 2004,
      "Demaine, Harmon, Iacono & Pătrașcu, 'Dynamic Optimality—Almost', FOCS 2004 (journal: SIAM "
      "J. Comput. 37(1):240-251, 2007)", "verified"),
    N("linkcut", "Link-cut tree (dynamic tree / ST-tree)", "tree", "modern", 1981,
      "Sleator & Tarjan, 'A Data Structure for Dynamic Trees', STOC 1981 (published 1983)",
      "verified"),
    N("eulertour", "Euler tour tree", "tree", "modern", 1995,
      "Henzinger & King, STOC 1995; simplified by Tarjan, 'Dynamic trees as search trees via "
      "Euler tours', Math. Programming 78:169-177, 1997", "verified"),
    N("tt23", "2-3 tree", "tree", "modern", 1970,
      "Invented by Hopcroft, 1970; first in print in Aho, Hopcroft & Ullman, 1974; Knuth TAOCP "
      "Vol.3, 1973 notes a B-tree of order 3 is a 2-3 tree", "verified"),
    N("tt234", "2-3-4 tree (2-4 tree)", "tree", "modern", 1972,
      "The order-4 B-tree case; equivalent to Bayer's symmetric binary B-tree (1972)", "verified"),
    N("bplustree", "B+-tree", "tree", "modern", 1979,
      "Described by Knuth (TAOCP Vol.3, 1973) and Comer, 'The Ubiquitous B-tree', ACM Comput. "
      "Surv. 11(2):121-137, 1979 (all records in linked leaves)", "verified"),
    N("fusiontree", "Fusion tree", "tree", "modern", 1990,
      "Fredman & Willard, 'Surpassing the information theoretic bound with fusion trees', STOC "
      "1990 (journal: JCSS 47(3):424-436, 1993)", "verified"),
    N("cobtree", "Cache-oblivious B-tree", "tree", "modern", 2000,
      "Bender, Demaine & Farach-Colton, 'Cache-Oblivious B-Trees', FOCS 2000 (journal: SIAM J. "
      "Comput. 35(2):341-358, 2005)", "verified"),

    # ───────────────────── MODERN — DIGITAL TREES & TEXT INDEX (§2.2) ─────────────────────
    N("radix", "Radix tree / PATRICIA", "trie", "modern", 1968,
      "Morrison, 'PATRICIA — Practical Algorithm to Retrieve Information Coded in Alphanumeric', "
      "JACM 15(4):514-534, 1968", "verified"),
    N("ternary", "Ternary search tree", "trie", "modern", None,
      "Trie variant; origin not stated in the source", "flagged", flags=("origin-not-in-report",)),
    N("adaptiveradix", "Adaptive radix tree", "trie", "modern", None,
      "Trie variant; origin not stated in the source", "flagged", flags=("origin-not-in-report",)),
    N("suffixtree", "Suffix tree", "trie", "modern", 1973,
      "Weiner, 'Linear pattern matching algorithms', 14th IEEE Symp. Switching & Automata Theory, "
      "1973 (refined by McCreight 1976 and Ukkonen 1995)", "verified"),
    N("suffixarray", "Suffix array", "trie", "modern", 1990,
      "Manber & Myers, 1990", "verified"),
    N("wavelet", "Wavelet tree", "trie", "modern", 2003,
      "Grossi, Gupta & Vitter, 'High-order entropy-compressed text indexes', SODA 2003 "
      "(succinct sequence / text index)", "verified"),
    N("vebtree", "van Emde Boas tree (stratified tree)", "trie", "modern", 1975,
      "van Emde Boas, 'Preserving order in a forest in less than logarithmic time', FOCS 1975 "
      "(with Kaas & Zijlstra, Math. Systems Theory 10:99-127, 1976/77) — O(log log u)", "verified"),
    N("xfast", "x-fast trie", "trie", "modern", 1983,
      "Willard, 'Log-logarithmic worst-case range queries are possible in space Θ(N)', IPL "
      "17(2):81-84, 1983", "verified"),
    N("yfast", "y-fast trie", "trie", "modern", 1983,
      "Willard, IPL 17(2):81-84, 1983", "verified"),

    # ─────────────────────────── MODERN — SPATIAL / GEOMETRIC (§2.3) ───────────────────────────
    N("kdtree", "k-d tree", "spatial", "modern", 1975,
      "Bentley, 'Multidimensional binary search trees used for associative searching', CACM "
      "18(9):509-517, 1975", "verified"),
    N("quadtree", "Quadtree", "spatial", "modern", 1974,
      "Finkel & Bentley, 'Quad Trees: A Data Structure for Retrieval on Composite Keys', Acta "
      "Informatica 4:1-9, 1974", "verified"),
    N("octree", "Octree", "spatial", "modern", None,
      "The 3-D analogue of the quadtree; the source gives no separate origin", "flagged",
      flags=("origin-not-in-report",)),
    N("rtree", "R-tree", "spatial", "modern", 1984,
      "Guttman, 'R-trees: A Dynamic Index Structure for Spatial Searching', ACM SIGMOD 1984",
      "verified"),
    N("rstar", "R*-tree", "spatial", "modern", 1990,
      "Beckmann, Kriegel, Schneider & Seeger, 1990 (R-tree variant)", "verified"),
    N("rplus", "R+-tree", "spatial", "modern", 1987,
      "Sellis, Roussopoulos & Faloutsos, 1987 (R-tree variant)", "verified"),
    N("hilbertr", "Hilbert R-tree", "spatial", "modern", None,
      "R-tree variant; origin not stated in the source", "flagged", flags=("origin-not-in-report",)),
    N("bsptree", "BSP tree (binary space partitioning)", "spatial", "modern", 1980,
      "Fuchs, Kedem & Naylor, 1980", "verified"),
    N("bvh", "Bounding volume hierarchy (BVH)", "spatial", "modern", None,
      "Spatial hierarchy of bounding volumes for collision detection / ray tracing; no single "
      "origin in the source", "flagged", flags=("origin-not-in-report",)),
    N("segmenttree", "Segment tree", "spatial", "modern", 1977,
      "Bentley, ~1977 (computational-geometry literature); attribution verified-but-soft",
      "verified", flags=("soft-attribution",)),
    N("fenwick", "Fenwick tree / binary indexed tree", "spatial", "modern", 1989,
      "Ryabko, 'A fast on-line code', Soviet Math. Doklady 39(3):533-537, 1989 (priority); "
      "popularised by Fenwick, Software: P&E 24(3):327-336, 1994", "verified",
      flags=("dual-priority",),
      note="Ryabko (1989) has priority; the popular name honours Fenwick (1994). Independent "
           "inventions."),
    N("intervaltree", "Interval tree", "spatial", "modern", None,
      "Geometric query tree; origin not detailed in the source", "flagged",
      flags=("origin-not-in-report",)),
    N("rangetree", "Range tree", "spatial", "modern", None,
      "Geometric query tree; origin not detailed in the source", "flagged",
      flags=("origin-not-in-report",)),
    N("prioritysearchtree", "Priority search tree", "spatial", "modern", None,
      "McCreight (venue / year not stated in the source)", "verified",
      flags=("origin-not-in-report",)),

    # ───────────────────────────── MODERN — HEAP FAMILY (§2.4) ─────────────────────────────
    N("binomialtree", "Binomial tree", "heap", "modern", 1978,
      "The tree structure that encodes the binomial heap; introduced with Vuillemin's binomial "
      "heap (CACM 21(4), 1978)", "verified", flags=("from-edge",),
      note="Appears in the topology edge list (§3.6) as the encoder of the binomial heap."),
    N("binomialheap", "Binomial heap", "heap", "modern", 1978,
      "Vuillemin, 'A data structure for manipulating priority queues', CACM 21(4):309-314, 1978",
      "verified"),
    N("fibheap", "Fibonacci heap", "heap", "modern", 1987,
      "Fredman & Tarjan, 'Fibonacci heaps and their uses in improved network optimization "
      "algorithms', JACM 34(3):596-615, 1987 (developed 1984)", "verified"),
    N("pairingheap", "Pairing heap", "heap", "modern", 1986,
      "Fredman, Sedgewick, Sleator & Tarjan, 'The pairing heap: A new form of self-adjusting "
      "heap', Algorithmica 1(1):111-129, 1986", "verified"),
    N("softheap", "Soft heap", "heap", "modern", 2000,
      "Chazelle, 'The Soft Heap: An Approximate Priority Queue with Optimal Error Rate', JACM "
      "47(6):1012-1027, 2000", "verified"),
    N("brodalq", "Brodal queue", "heap", "modern", 1996,
      "Brodal, 1996 — worst-case-optimal meldable priority queue", "verified"),
    N("leftistheap", "Leftist heap", "heap", "modern", 1972,
      "Crane, 'Linear Lists and Priority Queues as Balanced Binary Trees', Stanford PhD "
      "STAN-CS-72-259, 1972 (the mergeable leftist tree / leftist heap)", "verified",
      ("audit", "topology"),
      note="The audit identifies Crane 1972's leftist heap as a later, specialised mergeable-heap "
           "variant (non-foundational to the priority queue in general)."),
    N("skewheap", "Skew heap", "heap", "modern", None,
      "Further heap variant; origin not stated in the source", "flagged",
      flags=("origin-not-in-report",)),
    N("daryheap", "d-ary heap", "heap", "modern", None,
      "Generalisation of the binary heap to d children; origin not stated in the source",
      "flagged", flags=("origin-not-in-report",)),
    N("heap23", "2-3 heap", "heap", "modern", None,
      "Further heap variant; origin not stated in the source", "flagged",
      flags=("origin-not-in-report",)),
    N("rankpairing", "Rank-pairing heap", "heap", "modern", None,
      "Further heap variant; origin not stated in the source", "flagged",
      flags=("origin-not-in-report",)),
    N("funnelheap", "Funnel heap", "heap", "modern", 2002,
      "Brodal & Fagerberg, 2002 — cache-oblivious priority queue", "verified"),

    # ───────────────────────────── MODERN — HASH FAMILY (§2.5) ─────────────────────────────
    N("sepchaining", "Separate chaining", "hash", "modern", None,
      "Classical collision-resolution scheme; chaining is present from the earliest hashing work "
      "(Luhn 1953 / Dumey 1956)", "flagged", flags=("origin-not-in-report",)),
    N("openaddressing", "Open addressing", "hash", "modern", 1957,
      "Classical collision-resolution scheme (linear / quadratic probing, double hashing); term "
      "'open addressing' coined by Peterson, IBM JRD 1957", "verified", ("audit", "topology")),
    N("cuckoo", "Cuckoo hashing", "hash", "modern", 2001,
      "Pagh & Rodler, 'Cuckoo Hashing', ESA 2001 (journal: J. Algorithms 51(2):122-144, 2004)",
      "verified"),
    N("robinhood", "Robin Hood hashing", "hash", "modern", 1985,
      "Celis, Larson & Munro, 'Robin Hood Hashing', FOCS 1985", "verified"),
    N("hopscotch", "Hopscotch hashing", "hash", "modern", 2008,
      "Herlihy, Shavit & Tzafrir, 'Hopscotch Hashing', DISC 2008", "verified"),
    N("hamt", "HAMT (hash array mapped trie)", "hash", "modern", 2001,
      "Bagwell, 'Ideal Hash Trees', EPFL tech report, 2001 (building on 'Fast and Space Efficient "
      "Trie Searches', 2000)", "verified",
      note="A genuine hybrid of hash table and trie (see the trie⇄hash-table cycle, C1)."),
    N("dynperfhash", "Dynamic perfect hashing", "hash", "modern", 1994,
      "Dietzfelbinger, Karlin, Mehlhorn, Meyer auf der Heide, Rohnert & Tarjan, 1994", "verified"),
    N("fks", "FKS perfect hashing", "hash", "modern", 1984,
      "Fredman, Komlós & Szemerédi, 1984", "verified"),

    # ──────────────────────── MODERN — PROBABILISTIC / APPROXIMATE (§2.6) ────────────────────────
    N("countingbloom", "Counting Bloom filter", "approx", "modern", None,
      "Bloom-filter extension; origin not stated in the source", "flagged",
      flags=("origin-not-in-report",)),
    N("spectralbloom", "Spectral Bloom filter", "approx", "modern", None,
      "Bloom-filter extension; origin not stated in the source", "flagged",
      flags=("origin-not-in-report",)),
    N("bloomier", "Bloomier filter", "approx", "modern", None,
      "Bloom-filter extension; origin not stated in the source", "flagged",
      flags=("origin-not-in-report",)),
    N("quotientfilter", "Quotient filter", "approx", "modern", 2012,
      "Bender et al., 2012 — compact hash-based approximate membership", "verified"),
    N("cuckoofilter", "Cuckoo filter", "approx", "modern", 2014,
      "Fan, Andersen, Kaminsky & Mitzenmacher, 2014", "verified"),
    N("countminsketch", "Count-min sketch", "approx", "modern", 2005,
      "Cormode & Muthukrishnan, 'An improved data stream summary: The Count-Min Sketch and its "
      "applications', J. Algorithms 55(1):58-75, 2005", "verified"),
    N("hyperloglog", "HyperLogLog", "approx", "modern", 2007,
      "Flajolet, Fusy, Gandouet & Meunier, 'HyperLogLog', AofA 2007 (predecessor: Flajolet & "
      "Martin, 1985)", "verified"),

    # ──────────────────────────── MODERN — STORAGE / SYSTEMS (§2.7) ────────────────────────────
    N("lsmtree", "LSM-tree (log-structured merge tree)", "advanced", "modern", 1996,
      "O'Neil, Cheng, Gawlick & O'Neil, 'The log-structured merge-tree (LSM-tree)', Acta "
      "Informatica 33(4):351-385, 1996 (from a 1991 UMass Boston tech report)", "verified"),
    N("learnedindex", "Learned index", "advanced", "modern", 2018,
      "Kraska, Beutel, Chi, Dean & Polyzotis, 'The Case for Learned Index Structures', ACM "
      "SIGMOD 2018", "verified"),
    N("merkle", "Merkle tree (hash tree)", "advanced", "modern", 1979,
      "Merkle, Stanford PhD thesis 'Secrecy, Authentication, and Public Key Systems', 1979; "
      "definitive paper: 'A Digital Signature Based on a Conventional Encryption Function', "
      "CRYPTO '87 (1988)", "verified", flags=("ambiguous-date",),
      note="Year genuinely ambiguous: 1979 thesis/patent vs 1988 definitive paper."),
    N("roaring", "Roaring bitmap", "advanced", "modern", 2016,
      "Chambi, Lemire, Kaser & Godin, 'Better bitmap performance with Roaring bitmaps', Software: "
      "P&E 46(5):709-719, 2016", "verified"),

    # ───────────────────────────── MODERN — TEXT / SEQUENCE (§2.8) ─────────────────────────────
    N("rope", "Rope", "trie", "modern", 1995,
      "Boehm, Atkinson & Plass, 'Ropes: an Alternative to Strings', Software: P&E 25(12):"
      "1315-1330, 1995 (balanced tree over string fragments)", "verified"),
    N("gapbuffer", "Gap buffer", "trie", "modern", None,
      "Folklore text-editor structure (TECO / Emacs, late 1970s); NO origin paper", "flagged",
      flags=("folklore",), note="topology §7 flags this as conjectural-origin folklore."),
    N("piecetable", "Piece table", "trie", "modern", None,
      "Text-editor structure with conflicting attribution (Bravo editor, Xerox PARC — Lampson & "
      "Simonyi, mid-1970s; also credited to J Strother Moore); NO canonical origin paper",
      "flagged", flags=("folklore",),
      note="topology §7 flags this as conjectural-origin folklore."),

    # ─────────────────── MODERN — CONCURRENT / PERSISTENT / FUNCTIONAL (§2.9) ───────────────────
    N("msqueue", "Michael-Scott queue", "linear", "modern", 1996,
      "Michael & Scott, 'Simple, Fast, and Practical Non-Blocking and Blocking Concurrent Queue "
      "Algorithms', PODC '96, pp. 267-275, 1996 (lock-free FIFO)", "verified"),
    N("treiber", "Treiber stack", "linear", "modern", 1986,
      "Treiber, 'Systems Programming: Coping with Parallelism', IBM Almaden tech report RJ 5118, "
      "Apr 1986 (lock-free stack)", "verified"),
    N("skiplist", "Skip list", "linear", "modern", 1990,
      "Pugh, 'Skip lists: a probabilistic alternative to balanced trees', CACM 33(6):668-676, "
      "1990", "verified"),
    N("ringbuffer", "Ring / circular buffer", "linear", "modern", None,
      "Bounded FIFO over a fixed array; folklore", "flagged", flags=("folklore",)),
    N("persistent", "Persistent data structures", "advanced", "modern", 1989,
      "Driscoll, Sarnak, Sleator & Tarjan, 'Making Data Structures Persistent', JCSS 38(1):"
      "86-124, 1989 (STOC 1986) — fat node / path copying", "verified"),
    N("fingertree", "Finger tree", "advanced", "modern", 2006,
      "Hinze & Paterson, 'Finger trees: a simple general-purpose data structure', J. Functional "
      "Programming 16(2):197-217, 2006", "verified"),
    N("retroactive", "Retroactive data structures", "advanced", "modern", 2007,
      "Demaine, Iacono & Langerman, 2007", "verified"),
    N("succinct", "Succinct data structures", "advanced", "modern", 1989,
      "Jacobson, 'Space-efficient Static Trees and Graphs', FOCS 1989", "verified"),
    N("unionfind", "Union-find / disjoint-set", "assoc", "modern", 1964,
      "Galler & Fisher, 'An improved equivalence algorithm', CACM 1964 (amortized analysis: "
      "Hopcroft & Ullman 1973; Tarjan & van Leeuwen 1984)", "verified"),
    N("cacheobliviousmodel", "Cache-oblivious model", "advanced", "modern", 1999,
      "Frigo, Leiserson, Prokop & Ramachandran, 'Cache-Oblivious Algorithms', FOCS 1999 (a "
      "cost model / framework, not a structure — referenced by the edge list)", "verified",
      flags=("from-edge",)),
]
