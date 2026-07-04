# build/edges.py — PHASE 3: typed edges with provenance.
# Relation vocabulary (topology §3): refines / generalizes / specializes / hybridizes /
# encodes / influences. Direction is root → modern (ancestor → descendant), exactly as the
# report presents it.
#
# Provenance (mirrors the reference explorer's anti-fabrication discipline):
#   report:topology — an entry of the topology report's typed edge list (§3) or cycle set (§4).
#                     The §-number is kept in the note.
#   derived         — mechanically implied by an explicit sentence elsewhere in a report
#                     (the basis is quoted/paraphrased in the note).
#   editorial       — my reasoned structural judgment, never presented as report fact
#                     (rendered [EDITORIAL], dotted).
#
# cycle: one of C1..C4 (topology §4) tags the edges of a genuine relation-typed cycle.


def E(s, t, kind, src="report:topology", cycle="", note=""):
    return dict(s=s, t=t, kind=kind, src=src, cycle=cycle, note=note)


EDGES = [
    # ── §3.1 Descent from TREE ────────────────────────────────────────────────────────────
    E("tree", "binarytree", "specializes", note="§3.1"),
    E("tree", "trie", "specializes", note="§3.1"),
    E("tree", "btree", "specializes", note="§3.1"),
    E("tree", "quadtree", "specializes", note="§3.1"),
    E("tree", "octree", "specializes", note="§3.1"),
    E("tree", "bsptree", "specializes", note="§3.1"),
    E("tree", "bvh", "generalizes", note="§3.1"),

    # ── §3.2 Descent from BINARY TREE ─────────────────────────────────────────────────────
    E("binarytree", "bst", "specializes", note="§3.2"),
    E("binarytree", "binaryheap", "encodes", note="§3.2 implicit complete binary tree in an array"),
    E("binarytree", "cartesian", "specializes", cycle="C2", note="§3.2"),

    # ── §3.3 Descent from BINARY SEARCH TREE (the densest spine) ─────────────────────────
    E("bst", "avl", "refines", note="§3.3 via the self-balancing concept"),
    E("bst", "weightbalanced", "refines", note="§3.3"),
    E("symbin", "redblack", "refines", note="§3.3"),
    E("tt234", "redblack", "encodes", cycle="C4", note="§3.3 a 2-3-4 tree encodes a red-black tree"),
    E("redblack", "llrb", "refines", note="§3.3"),
    E("bst", "splay", "refines", note="§3.3"),
    E("bst", "treap", "hybridizes", cycle="C2", note="§3.3 BST + binary heap → treap"),
    E("binaryheap", "treap", "hybridizes", cycle="C2", note="§3.3 BST + binary heap → treap"),
    E("cartesian", "treap", "influences", cycle="C2", note="§3.3"),
    E("bst", "scapegoat", "refines", note="§3.3"),
    E("bst", "aatree", "refines", note="§3.3"),
    E("bst", "wavl", "refines", note="§3.3"),
    E("bst", "tango", "refines", note="§3.3 balanced BST + link-cut auxiliary trees → tango"),
    E("linkcut", "tango", "influences", note="§3.3 link-cut auxiliary trees"),
    E("splay", "linkcut", "specializes", note="§3.3"),
    E("bst", "eulertour", "encodes", note="§3.3 balanced BST encodes the Euler tour"),
    E("bst", "kdtree", "specializes", note="§3.3 multidimensional"),
    E("bst", "persistent", "refines", note="§3.3 persistence: fat node / path copying (persistent BST)"),

    # ── §3.4 Descent from B-TREE ──────────────────────────────────────────────────────────
    E("btree", "tt23", "specializes", note="§3.4 order-3 case"),
    E("btree", "tt234", "specializes", note="§3.4 order-4 case"),
    E("btree", "bplustree", "refines", note="§3.4"),
    E("tt23", "tt234", "specializes", note="§3.4"),
    E("btree", "fusiontree", "refines", note="§3.4 word-parallel nodes"),
    E("btree", "cobtree", "refines", note="§3.4 cache-oblivious layout"),
    E("btree", "lsmtree", "influences", note="§3.4 write-optimized alternative to B-tree indexing"),
    E("btree", "learnedindex", "influences", note="§3.4 a learned model replaces the tree"),
    E("btree", "rtree", "generalizes", note="§3.4 spatial"),
    E("rtree", "rstar", "refines", note="§3.4"),
    E("rtree", "rplus", "refines", note="§3.4"),
    E("rtree", "hilbertr", "refines", note="§3.4"),

    # ── §3.5 Descent from TRIE ────────────────────────────────────────────────────────────
    E("trie", "radix", "refines", note="§3.5 radix tree / PATRICIA"),
    E("trie", "ternary", "specializes", note="§3.5"),
    E("trie", "adaptiveradix", "specializes", note="§3.5"),
    E("trie", "suffixtree", "specializes", note="§3.5 over suffixes"),
    E("trie", "hamt", "hybridizes", cycle="C1", note="§3.5 trie + hash table → HAMT"),
    E("hashtable", "hamt", "hybridizes", cycle="C1", note="§3.7 hash table + trie → HAMT"),
    E("trie", "vebtree", "influences", cycle="C3", note="§3.5 bit-recursive trie over the universe"),
    E("vebtree", "xfast", "refines", note="§3.5 space reduction via hashing"),
    E("xfast", "yfast", "refines", note="§3.5"),

    # ── §3.6 Descent from HEAP / PRIORITY QUEUE ───────────────────────────────────────────
    E("priorityqueue", "binaryheap", "specializes", note="§3.6"),
    E("binaryheap", "daryheap", "generalizes", note="§3.6"),
    E("binomialtree", "binomialheap", "encodes", note="§3.6"),
    E("binomialheap", "fibheap", "refines", note="§3.6"),
    E("fibheap", "pairingheap", "refines", note="§3.6"),
    E("binomialheap", "softheap", "refines", note="§3.6 approximate, bounded corruption"),
    E("binaryheap", "leftistheap", "refines", note="§3.6"),
    E("binaryheap", "skewheap", "refines", note="§3.6"),
    E("binaryheap", "heap23", "refines", note="§3.6"),
    E("binaryheap", "rankpairing", "refines", note="§3.6"),
    E("binaryheap", "brodalq", "refines", note="§3.6"),
    E("cacheobliviousmodel", "funnelheap", "refines", note="§3.6"),
    E("vebtree", "priorityqueue", "specializes", cycle="C3",
      note="§3.6 van Emde Boas tree as an integer priority queue"),

    # ── §3.7 Descent from HASH TABLE ──────────────────────────────────────────────────────
    E("hashtable", "sepchaining", "refines", note="§3.7"),
    E("hashtable", "openaddressing", "refines", note="§3.7"),
    E("openaddressing", "cuckoo", "refines", note="§3.7"),
    E("openaddressing", "robinhood", "refines", note="§3.7"),
    E("openaddressing", "hopscotch", "refines", note="§3.7"),
    E("hashtable", "dynperfhash", "refines", note="§3.7"),
    E("hashtable", "fks", "refines", note="§3.7"),

    # ── §3.8 Descent from SET / APPROXIMATE MEMBERSHIP and BIT ARRAY ──────────────────────
    E("set", "multiset", "specializes", note="§3.8"),
    E("bitarray", "bloomfilter", "hybridizes", note="§3.8 bit array + hash table → Bloom filter"),
    E("hashtable", "bloomfilter", "hybridizes", note="§3.8 bit array + hash table → Bloom filter"),
    E("bloomfilter", "countingbloom", "refines", note="§3.8"),
    E("bloomfilter", "spectralbloom", "refines", note="§3.8"),
    E("bloomfilter", "bloomier", "refines", note="§3.8"),
    E("hashtable", "quotientfilter", "refines", note="§3.8 approximate"),
    E("hashtable", "cuckoofilter", "refines", note="§3.8 approximate"),
    E("bitarray", "roaring", "encodes", note="§3.8 two-level array/bitmap containers"),
    E("hashtable", "countminsketch", "encodes", note="§3.8 hash + counter array"),
    E("hashtable", "hyperloglog", "encodes", note="§3.8 hash + register array"),

    # ── §3.9 Descent from ARRAY / DYNAMIC ARRAY ───────────────────────────────────────────
    E("array", "dynarray", "refines", note="§3.9"),
    E("array", "bitarray", "specializes", note="§3.9"),
    E("array", "binaryheap", "encodes", note="§3.9"),
    E("array", "fenwick", "encodes", note="§3.9"),
    E("array", "segmenttree", "encodes", note="§3.9"),
    E("array", "gapbuffer", "refines", note="§3.9 array + movable gap"),
    E("dynarray", "ringbuffer", "refines", note="§3.9"),
    E("segmenttree", "fenwick", "refines", note="§3.9 LSB indexing"),

    # ── §3.10 Descent from STRING / LINKED LIST ───────────────────────────────────────────
    E("string", "rope", "refines", note="§3.10 balanced tree over fragments"),
    E("string", "piecetable", "refines", note="§3.10 span index over buffers"),
    E("linkedlist", "treiber", "refines", note="§3.10 lock-free"),
    E("linkedlist", "msqueue", "refines", note="§3.10 lock-free"),
    E("linkedlist", "skiplist", "hybridizes", note="§3.10 linked list + probabilistic levels"),

    # ── §3.11 Descent from GRAPH and DISJOINT-SET ─────────────────────────────────────────
    E("graph", "unionfind", "influences", note="§3.11"),
    E("tree", "unionfind", "encodes", note="§3.11 forest of trees"),
    E("graph", "linkcut", "influences", note="§3.11 dynamic connectivity"),
    E("graph", "eulertour", "influences", note="§3.11 dynamic connectivity"),

    # ── §3.12 Descent to SUCCINCT / FINGER / RETROACTIVE / CRYPTOGRAPHIC ──────────────────
    E("bitarray", "succinct", "encodes", note="§3.12 bit array + rank/select"),
    E("succinct", "wavelet", "encodes", note="§3.12 succinct bit-vectors"),
    E("trie", "wavelet", "influences", note="§3.12"),
    E("tt23", "fingertree", "refines", note="§3.12 functional, amortized"),
    E("persistent", "retroactive", "generalizes", note="§3.12"),
    E("binarytree", "merkle", "hybridizes", note="§3.12 binary tree + cryptographic hash"),

    # ── DERIVED — from explicit report sentences outside the §3 edge list ─────────────────
    E("bst", "selfbalancing", "refines", "derived",
      note="§3.3 parenthetical: BST refined 'via the self-balancing concept [F-NEW]'."),
    E("selfbalancing", "avl", "influences", "derived",
      note="§2.1: AVL (Adelson-Velsky & Landis, 1962) is the theory + implementation root of the "
           "self-balancing concept — its first instance."),
    E("hashtable", "assocarray", "encodes", "derived",
      note="§2.1: the associative-array ADT sits above the hash table (one of its substrates)."),
    E("bst", "assocarray", "encodes", "derived",
      note="§2.1: the associative-array ADT sits above the search tree (one of its substrates)."),
    E("hamt", "assocarray", "encodes", "derived", cycle="C1",
      note="§4 C1: the HAMT is used to implement (encodes) the associative arrays that back a "
           "hash-map interface."),

    # ── EDITORIAL — reasoned structural links, not report facts ──────────────────────────
    E("selfbalancing", "redblack", "influences", "editorial",
      note="The self-balancing principle also feeds the red-black lineage (structural judgment)."),
    E("map", "assocarray", "encodes", "editorial",
      note="Map/dictionary is the implementation flavour of the associative-array ADT."),

    # ── CONNECTING edges for inventory roots the topology §3 list leaves unlinked ─────────
    # These structures are in the inventory (audit's 17 / topology §2) but appear in no §3
    # edge. Rather than drop canonical roots, each is attached by a defensible relation whose
    # basis is quoted (derived) or flagged as my judgment (editorial).
    E("stack", "treiber", "specializes", "derived",
      note="The topology report names it a lock-free 'Treiber STACK' (§2.9 / §3.10)."),
    E("queue", "msqueue", "specializes", "derived",
      note="The topology report names it a 'Michael-Scott QUEUE' (§2.9 / §3.10)."),
    E("queue", "ringbuffer", "specializes", "derived",
      note="Ring / circular buffer = 'bounded FIFO over a fixed array' (§2.9) — a bounded queue."),
    E("deque", "queue", "generalizes", "derived",
      note="Audit §6: the deque's 'input-/output-restricted variants' — a queue is the "
           "output-restricted deque."),
    E("deque", "stack", "generalizes", "derived",
      note="Audit §6: restricted-deque framing — a stack is the input-restricted deque."),
    E("record", "linkedlist", "influences", "editorial",
      note="Hoare's typed record + typed reference (1965) is the type-theoretic basis of "
           "pointer-linked structures (influence, not descent)."),
    E("record", "bst", "influences", "editorial",
      note="Search-tree nodes are records with typed references (influence, not descent)."),
    E("suffixtree", "suffixarray", "refines", "editorial",
      note="The suffix array is the flat, space-efficient counterpart of the suffix tree "
           "(topology §2.2 lists them together)."),
    E("bst", "intervaltree", "specializes", "editorial",
      note="Augmented BST for geometric interval queries (topology §2.2)."),
    E("bst", "rangetree", "specializes", "editorial",
      note="Augmented BST for orthogonal range queries (topology §2.2)."),
    E("bst", "prioritysearchtree", "specializes", "editorial",
      note="McCreight's augmented BST for grounded range queries (topology §2.2)."),
]

# Cycle descriptions (topology §4), surfaced in the detail panel / MODELS.md.
CYCLES = {
    "C1": "Trie ⇄ Hash table (via HAMT): the HAMT is a descendant of both parents (hybridizes) "
          "and an implementation substitute for the associative array (encodes).",
    "C2": "Heap ⇄ Binary search tree (via treap / Cartesian tree): the BST and heap ordering "
          "invariants meet in one node (specializes vs hybridizes).",
    "C3": "van Emde Boas tree ⇄ Priority queue: vEB is influenced by the trie lineage yet "
          "specializes the priority-queue ADT (influences vs specializes).",
    "C4": "B-tree ⇄ Binary search tree: the B-tree generalizes the BST while a red-black tree "
          "(a BST) encodes a 2-3-4 tree (a B-tree) — generalizes vs encodes.",
}
