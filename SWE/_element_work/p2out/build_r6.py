# -*- coding: utf-8 -*-
import json, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

BASE = r"C:/Users/frede/AppData/Local/Temp/claude/E--dev-corpora/af68f286-e2b9-4227-a910-623820ffa376/scratchpad"

def W(action, id, title, authors, year, venue, ident, type, role, verification, unresolved, note, elements):
    return {"action": action, "id": id, "title": title, "authors": authors, "year": year,
            "venue": venue, "ident": ident, "type": type, "role": role,
            "verification": verification, "unresolved": unresolved, "note": note,
            "elements": elements}

works = [
# ---------------- MEMBERSHIPS ----------------
W("membership","posa3","Pattern-Oriented Software Architecture Vol. 3: Patterns for Resource Management","Kircher & Jain","2004","Wiley",None,"book","core","verified",None,
  "Names and teaches the Caching pattern (resource-management form) that anchors this route's caching axis; citation lives in corpus.",
  ["caching"]),
W("membership","white","Making Embedded Systems: Design Patterns for Great Software, 2nd ed.","Elecia White","2024","O'Reilly",None,"book","core","verified",None,
  "Embedded math chapter teaches lookup tables (with interpolation) as the standard embedded space/time trade; upgrades the element from its bare-Wikipedia naming.",
  ["lookup-table"]),
W("membership","hanson","C Interfaces and Implementations: Techniques for Creating Reusable Software","David R. Hanson","1996","Addison-Wesley",None,"book","core","verified",None,
  "Interface-per-chapter C treatments of the container floor: lists, hash tables (Table/Set), resizable arrays/sequences, bit vectors, stack-as-interface exemplar.",
  ["linked-list","hash-table","dynamic-array","bitmap-bitset","stack"]),
W("membership","noblesmallmem","Small Memory Software: Patterns for Systems with Limited Memory","Noble & Weir","2000","Addison-Wesley",None,"book","core","verified",None,
  "Names Embedded Pointer and teaches intrusive linking as a memory-constrained design move.",
  ["embedded-pointer"]),
W("membership","etl","Embedded Template Library (ETL)","John Wellbelove","living","official project site",None,"tooling-doc","core","verified",None,
  "The living canonical realization of fixed-capacity containers for C++ without heap; defines the element's contract (compile-time capacity, no allocation).",
  ["fixed-capacity-container"]),
W("membership","hanmer","Patterns for Fault Tolerant Software","Robert Hanmer","2007","Wiley",None,"book","core","verified",None,
  "Names Checkpoint as a fault-tolerance pattern; the design-level treatment of periodic durable state capture.",
  ["checkpointing"]),
W("membership","progit","Pro Git, 2nd ed.","Scott Chacon & Ben Straub","2014","Apress / git-scm.com",None,"book","core","verified",None,
  "Git Internals chapter is the canonical modern teaching of a content-addressable object store (hash-keyed blobs, write-once).",
  ["content-addressable-storage"]),

# ---------------- NEW: algorithms & container canon ----------------
W("new","clrs","Introduction to Algorithms, 4th ed.","Cormen, Leiserson, Rivest & Stein","2022","MIT Press","ISBN 9780262046305","book","anchor","verified",None,
  "The reference treatment for the container/algorithm floor of this route: elementary structures, hash tables, BSTs, heaps, B-trees, union-find, augmented/interval trees, amortized table doubling; 4th ed adds suffix-array material.",
  ["b-tree","binary-heap-priority-queue","binary-search-tree","disjoint-set-union-find","dynamic-array","hash-table","interval-tree","linked-list","queue-fifo","stack","suffix-array"]),
W("new","sedgewick","Algorithms, 4th ed.","Robert Sedgewick & Kevin Wayne","2011","Addison-Wesley; official site algs4.cs.princeton.edu","https://algs4.cs.princeton.edu/","book","core","verified",None,
  "Teaching canon with live companion site; confirmed chapters for priority queues (2.4), BSTs (3.2), hash tables (3.4), tries (5.2), suffix arrays (6.3).",
  ["binary-heap-priority-queue","binary-search-tree","hash-table","queue-fifo","stack","suffix-array","trie"]),
W("new","taocp1","The Art of Computer Programming, Vol. 1: Fundamental Algorithms, 3rd ed.","Donald E. Knuth","1997","Addison-Wesley","ISBN 0-201-89683-4","book","advanced","verified",None,
  "Names and exhaustively treats the linear-list family; the naming source for deque (2.2.1) and the deep treatment of linked allocation.",
  ["deque","linked-list"]),
W("new","okasaki","Purely Functional Data Structures","Chris Okasaki","1998","Cambridge University Press","doi:10.1017/CBO9780511530104","book","core","verified",None,
  "The canonical treatment of persistent (immutable) data structure design: path copying, laziness, amortization under persistence.",
  ["persistent-data-structure"]),

# ---------------- NEW: database / storage treatments ----------------
W("new","kleppmann","Designing Data-Intensive Applications","Martin Kleppmann","2017","O'Reilly; official site dataintensive.net","https://dataintensive.net/","book","anchor","verified",None,
  "Ch.3 storage/retrieval is the modern teaching path for this route's storage-engine elements: log-structured storage vs B-trees, LSM/SSTables, tombstones, secondary indexes, bitmap-encoded columns, WAL; ch.6 treats hash partitioning/consistent hashing.",
  ["b-tree","bitmap-index","consistent-hashing","log-structured-storage","lsm-tree","secondary-index","tombstone","write-ahead-log"]),
W("new","petrov","Database Internals: A Deep-Dive into How Distributed Data Systems Work","Alex Petrov","2019","O'Reilly","ISBN 9781492040347","book","anchor","verified",None,
  "Storage-engine half teaches buffer pool/page cache and eviction (incl. LRU variants), B-trees and copy-on-write B-trees, WAL/recovery, LSM trees with memtable skip lists and Bloom filters — the named source for cache-eviction-policy.",
  ["b-tree","bloom-filter","buffer-pool","cache-eviction-policy","copy-on-write-b-tree","lru-cache","lsm-tree","skip-list","write-ahead-log"]),
W("new","hellersteindb","Architecture of a Database System","Hellerstein, Stonebraker & Hamilton","2007","Foundations and Trends in Databases 1(2)","doi:10.1561/1900000002","paper","survey","verified",None,
  "Survey that names buffer pool as a DBMS component and situates buffer management among the shared components; loaded live from the author's Berkeley copy.",
  ["buffer-pool"]),
W("new","grayreuter","Transaction Processing: Concepts and Techniques","Jim Gray & Andreas Reuter","1992","Morgan Kaufmann / Elsevier","https://shop.elsevier.com/books/transaction-processing/gray/978-0-08-051955-5","book","core","verified",None,
  "The durability canon: names and teaches write-ahead logging, group commit, checkpointing, and the shadow-page alternative it critiques.",
  ["checkpointing","group-commit","shadow-paging","write-ahead-log"]),
W("new","lorie1977","Physical Integrity in a Large Segmented Database","Raymond A. Lorie","1977","ACM TODS 2(1)",None,"paper","advanced","unverified","doi",
  "Naming source for shadow paging (System R's shadow-page recovery); kept as canon alongside the Gray-Reuter treatment.",
  ["shadow-paging"]),
W("new","lfs1992","The Design and Implementation of a Log-Structured File System","Mendel Rosenblum & John K. Ousterhout","1992","ACM TOCS 10(1); SOSP 1991","https://web.stanford.edu/~ouster/cgi-bin/papers/lfs.pdf","paper","core","verified",None,
  "Naming paper for log-structured storage; first page loaded live from Ousterhout's Stanford copy.",
  ["log-structured-storage"]),
W("new","moerkotte1998","Small Materialized Aggregates: A Light Weight Index Structure for Data Warehousing","Guido Moerkotte","1998","VLDB 1998","https://www.vldb.org/conf/1998/p476.pdf","paper","advanced","verified",None,
  "Naming source for the zone-map/SMA mechanism (per-bucket min/max aggregates used to skip scans); loaded live from vldb.org proceedings.",
  ["zone-map"]),
W("new","oneilquass1997","Improved Query Performance with Variant Indexes","Patrick O'Neil & Dallan Quass","1997","ACM SIGMOD 1997",None,"paper","advanced","unverified","doi",
  "Canonical bitmap-index paper (value-list/bit-sliced indexes); complements DDIA's columnar bitmap-encoding treatment.",
  ["bitmap-index"]),
W("new","guttman1984","R-Trees: A Dynamic Index Structure for Spatial Searching","Antonin Guttman","1984","ACM SIGMOD 1984",None,"paper","core","unverified","doi",
  "Naming paper and still the standard reference for the R-tree spatial index; no treatment in this route's work-set covers R-trees.",
  ["r-tree"]),

# ---------------- NEW: caching axis ----------------
W("new","coherencecache","Caching Data Sources (Oracle Coherence Developing Applications guide)","Oracle","living","docs.oracle.com, Coherence 14.1.1","https://docs.oracle.com/en/middleware/standalone/coherence/14.1.1.2206/develop-applications/caching-data-sources.html","official-doc","anchor","verified",None,
  "The living naming source that defines the read-through / write-through / write-behind / refresh-ahead family; definitions confirmed live.",
  ["read-through-cache","refresh-ahead-cache","write-behind-cache","write-through-cache"]),
W("new","azurepatterns","Cloud Design Patterns: Cache-Aside","Microsoft (Azure Architecture Center)","living","learn.microsoft.com","https://learn.microsoft.com/en-us/azure/architecture/patterns/cache-aside","official-doc","core","verified",None,
  "The maintained catalog entry that names Cache-Aside and specifies its read-miss-populate / write-invalidate contract.",
  ["cache-aside"]),
W("new","hennessypatterson","Computer Architecture: A Quantitative Approach, 6th ed.","John L. Hennessy & David A. Patterson","2017","Morgan Kaufmann / Elsevier","https://shop.elsevier.com/books/computer-architecture/hennessy/978-0-12-811905-1","book","core","verified",None,
  "Memory-hierarchy chapters are the canonical treatment of the hardware ends of this route: prefetching, write-through vs write-back policy, and replacement (LRU) as an eviction policy.",
  ["cache-eviction-policy","lru-cache","prefetching","write-behind-cache","write-through-cache"]),
W("new","vattani2015","Optimal Probabilistic Cache Stampede Prevention","Vattani, Chierichetti & Lowenstein","2015","PVLDB 8(8)","https://www.vldb.org/pvldb/vol8/p886-vattani.pdf","paper","advanced","verified",None,
  "Names the cache-stampede problem and gives the XFetch early-recomputation mechanism; loaded live from PVLDB.",
  ["cache-stampede-protection"]),
W("new","rfc2308","Negative Caching of DNS Queries (DNS NCACHE)","M. Andrews","1998","IETF RFC 2308","https://www.rfc-editor.org/rfc/rfc2308.html","standard","core","verified",None,
  "Standards-body naming and specification of negative caching; the general mechanism's canonical citation.",
  ["negative-caching"]),
W("new","michie1968","'Memo' Functions and Machine Learning","Donald Michie","1968","Nature 218",None,"paper","advanced","unverified","doi",
  "Naming paper for memoization (memo functions); Nature page blocked live, identifier held at recall grade.",
  ["memoization"]),
W("new","paip","Paradigms of Artificial Intelligence Programming: Case Studies in Common Lisp","Peter Norvig","1992","Morgan Kaufmann; full text at github.com/norvig/paip-lisp","https://github.com/norvig/paip-lisp","book","core","verified",None,
  "Ch. 9 (Efficiency) is a genuine teaching treatment of memoization as a general design device; author-published full text confirmed live.",
  ["memoization"]),
W("new","deutschschiffman1984","Efficient Implementation of the Smalltalk-80 System","L. Peter Deutsch & Allan M. Schiffman","1984","ACM POPL 1984",None,"paper","advanced","unverified","doi",
  "Naming paper for inline caching in dynamic-language runtimes; no treatment in the work-set covers it.",
  ["inline-caching"]),

# ---------------- NEW: probabilistic / distributed structures ----------------
W("new","bloom1970","Space/Time Trade-offs in Hash Coding with Allowable Errors","Burton H. Bloom","1970","CACM 13(7)",None,"paper","core","unverified","doi",
  "The canon naming paper for the Bloom filter; kept alongside Petrov's storage-engine treatment.",
  ["bloom-filter"]),
W("new","flajolet2007","HyperLogLog: the analysis of a near-optimal cardinality estimation algorithm","Flajolet, Fusy, Gandouet & Meunier","2007","DMTCS Proceedings AH (AofA 2007)","doi:10.46298/dmtcs.3545","paper","core","verified",None,
  "Naming paper and only catalog-grade source for HyperLogLog; confirmed live on the DMTCS episciences page.",
  ["hyperloglog"]),
W("new","cormode2005","An Improved Data Stream Summary: The Count-Min Sketch and its Applications","Graham Cormode & S. Muthukrishnan","2005","Journal of Algorithms 55(1)","http://dimacs.rutgers.edu/~graham/pubs/papers/cm-full.pdf","paper","core","verified",None,
  "Naming paper for the count-min sketch; first page loaded live from Cormode's DIMACS copy.",
  ["count-min-sketch"]),
W("new","tdigest2019","Computing Extremely Accurate Quantiles Using t-Digests","Ted Dunning & Otmar Ertl","2019","arXiv","arXiv:1902.04023","paper","core","verified",None,
  "Naming paper for the t-digest quantile sketch; confirmed live on arXiv.",
  ["t-digest"]),
W("new","karger1997","Consistent Hashing and Random Trees: Distributed Caching Protocols for Relieving Hot Spots on the World Wide Web","Karger, Lehman, Leighton, Panigrahy, Levine & Lewin","1997","ACM STOC 1997",None,"paper","core","unverified","doi",
  "Naming paper for consistent hashing; DDIA supplies the modern partitioning treatment.",
  ["consistent-hashing"]),
W("new","merkle1987","A Digital Signature Based on a Conventional Encryption Function","Ralph C. Merkle","1987","CRYPTO 1987 (Springer LNCS 293)",None,"paper","core","unverified","doi",
  "Canonical citation for the Merkle (hash) tree; Springer page blocked live this session.",
  ["merkle-tree"]),
W("new","shapiro2011","Conflict-free Replicated Data Types","Shapiro, Preguica, Baquero & Zawirski","2011","SSS 2011; INRIA RR-7687",None,"paper","core","unverified","doi",
  "Naming paper defining CRDTs and the CvRDT/CmRDT taxonomy; HAL and Springer pages blocked live this session.",
  ["conflict-free-replicated-data-type-crdt"]),

# ---------------- NEW: concurrency structures ----------------
W("new","michaelscott1996","Simple, Fast, and Practical Non-Blocking and Blocking Concurrent Queue Algorithms","Maged M. Michael & Michael L. Scott","1996","ACM PODC 1996","https://www.cs.rochester.edu/u/scott/papers/1996_PODC_queues.pdf","paper","core","verified",None,
  "The paper the lock-free FIFO queue element is named after; first page loaded live from Scott's Rochester copy.",
  ["lock-free-fifo-queue-michael-scott"]),
W("new","herlihyshavit","The Art of Multiprocessor Programming, 2nd ed.","Herlihy, Shavit, Luchangco & Spear","2020","Morgan Kaufmann / Elsevier","ISBN 9780124159501","book","core","verified",None,
  "The teaching treatment for lock-free structures: Treiber stack, Michael-Scott queue, and concurrent skip lists, with correctness reasoning.",
  ["lock-free-fifo-queue-michael-scott","lock-free-stack-treiber","skip-list"]),
W("new","pugh1990","Skip Lists: A Probabilistic Alternative to Balanced Trees","William Pugh","1990","CACM 33(6)",None,"paper","core","unverified","doi",
  "Canon naming paper for skip lists; Petrov and Herlihy-Shavit carry the treatments.",
  ["skip-list"]),

# ---------------- NEW: spatial / games / graphics ----------------
W("new","ericson","Real-Time Collision Detection","Christer Ericson","2005","Morgan Kaufmann; official site realtimecollisiondetection.net","https://realtimecollisiondetection.net/","book","anchor","verified",None,
  "One treatment covering the spatial cluster: BVHs, uniform grids and spatial hashing, quadtrees/octrees, k-d/BSP trees — the route entry point for spatial partitioning.",
  ["bounding-volume-hierarchy","k-d-tree","quadtree-octree","spatial-partition","uniform-spatial-hash-grid"]),
W("new","rtr4","Real-Time Rendering, 4th ed.","Akenine-Möller, Haines & Hoffman","2018","CRC Press",None,"book","core","unverified","isbn",
  "Named source for scene graph and BVH in the rendering context (acceleration/spatial data structure chapters); publisher and book-site pages blocked live this session.",
  ["bounding-volume-hierarchy","quadtree-octree","scene-graph"]),
W("new","nystromgpp","Game Programming Patterns","Robert Nystrom","2014","Genever Benning; full text at gameprogrammingpatterns.com","https://gameprogrammingpatterns.com/spatial-partition.html","book","core","verified",None,
  "Names Spatial Partition as a design pattern; chapter confirmed live on the author's full-text site.",
  ["spatial-partition"]),
W("new","millingtonai","AI for Games, 3rd ed.","Ian Millington","2019","CRC Press",None,"book","core","unverified","isbn",
  "Pathfinding chapters teach navigation meshes as the standard game-AI world representation; CRC/Taylor & Francis pages blocked live this session.",
  ["navigation-mesh"]),
W("new","deberg","Computational Geometry: Algorithms and Applications, 3rd ed.","de Berg, Cheong, van Kreveld & Overmars","2008","Springer",None,"book","core","unverified","isbn",
  "The textbook treatment of geometric range structures: kd-trees, interval trees, segment trees; Springer page unreachable (cookie wall) this session.",
  ["interval-tree","k-d-tree","segment-tree"]),

# ---------------- NEW: strings / text / niche structures ----------------
W("new","finseth","The Craft of Text Editing: Emacs for the Modern World","Craig A. Finseth","1991","Springer; full text at finseth.com/craft","https://www.finseth.com/craft/","book","core","verified",None,
  "Ch. 6 (The Internal Sub-Editor) is the catalog treatment of the buffer-gap method and its paged variant; confirmed live on the author's site.",
  ["gap-buffer"]),
W("new","vscodepiecetree","Text Buffer Reimplementation (VS Code blog)","Peng Lyu / Microsoft","2018","code.visualstudio.com","https://code.visualstudio.com/blogs/2018/03/23/text-buffer-reimplementation","blog","core","verified",None,
  "Official project engineering post teaching the piece table (and its piece-tree evolution) as a production text-buffer structure; confirmed live.",
  ["piece-table"]),
W("new","boehm1995","Ropes: an Alternative to Strings","Boehm, Atkinson & Plass","1995","Software: Practice and Experience 25(12)",None,"paper","core","unverified","doi",
  "Naming paper for the rope structure; Wiley page blocked live this session.",
  ["rope"]),
W("new","bagwell2001","Ideal Hash Trees","Phil Bagwell","2001","EPFL (LAMP) technical report","https://lampwww.epfl.ch/papers/idealhashtrees.pdf","paper","core","verified","year (commonly cited as 2001; not shown on the EPFL copy's first page)",
  "Naming paper for the hash array mapped trie; first page loaded live from the EPFL LAMP host.",
  ["hash-array-mapped-trie-hamt"]),
W("new","huet1997","The Zipper","Gérard Huet","1997","Journal of Functional Programming 7(5)","doi:10.1017/S0956796897002864","paper","core","verified",None,
  "The functional pearl that names the zipper; confirmed live on Cambridge Core.",
  ["zipper"]),
W("new","fenwick1994","A New Data Structure for Cumulative Frequency Tables","Peter M. Fenwick","1994","Software: Practice and Experience 24(3)",None,"paper","advanced","unverified","doi",
  "Naming paper for the Fenwick (binary indexed) tree; Wiley page blocked live this session.",
  ["fenwick-tree"]),
W("new","briggstorczon1993","An Efficient Representation for Sparse Sets","Preston Briggs & Linda Torczon","1993","ACM LOPLAS 2(1-4)",None,"paper","advanced","unverified","doi",
  "Naming paper for the sparse-set representation (dense/sparse array pair), the basis of modern ECS storage.",
  ["sparse-set"]),
W("new","p0661","slot_map Container in C++ (WG21 P0661)","Allan Deutsch","2017","ISO C++ committee (LEWG/SG14), open-std.org","https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/p0661r0.pdf","paper","advanced","verified",None,
  "The WG21 proposal that names slot_map and specifies its generation-keyed contract; loaded live from open-std.org.",
  ["slot-map"]),
W("new","meyerseffstl","Effective STL: 50 Specific Ways to Improve Your Use of the Standard Template Library","Scott Meyers","2001","Addison-Wesley; author site aristeia.com","https://www.aristeia.com/books.html","book","core","verified",None,
  "Names and teaches the erase-remove idiom (Item 32); author's page confirmed live.",
  ["erase-remove"]),

# ---------------- NEW: search / IR ----------------
W("new","manningiir","Introduction to Information Retrieval","Manning, Raghavan & Schütze","2008","Cambridge University Press; full text at nlp.stanford.edu/IR-book","https://nlp.stanford.edu/IR-book/","book","anchor","verified",None,
  "The IR canon: inverted index construction (chs. 1-4) and shingling/MinHash near-duplicate detection (ch. 19); official Stanford site confirmed live.",
  ["inverted-index","minhash"]),

# ---------------- NEW: persistence: enterprise + flash + CAS ----------------
W("new","peaa","Patterns of Enterprise Application Architecture","Martin Fowler","2002","Addison-Wesley","ISBN 0321127420","book","anchor","verified",None,
  "The naming catalog for this route's whole object-relational cluster: gateways, mappers, unit of work, identity map/field, inheritance mappings, embedded value, query object, repository.",
  ["active-record","association-table-mapping","class-table-inheritance","concrete-table-inheritance","data-mapper","dependent-mapping","embedded-value","foreign-key-mapping","identity-field","identity-map","inheritance-mappers","metadata-mapping","query-object","repository","row-data-gateway","single-table-inheritance","table-data-gateway","unit-of-work"]),
W("new","mfeaadev","martinfowler.com: Further Enterprise Application Architecture development (Event Sourcing; Memory Image)","Martin Fowler","living","martinfowler.com","https://martinfowler.com/eaaDev/EventSourcing.html","blog","core","verified",None,
  "Fowler's maintained articles naming Event Sourcing (2005) and Memory Image (2011); both pages confirmed live.",
  ["event-sourcing","memory-image"]),
W("new","venti2002","Venti: A New Approach to Archival Storage","Sean Quinlan & Sean Dorward","2002","USENIX FAST 2002; Bell Labs","https://9p.io/sys/doc/venti/venti.html","paper","core","verified",None,
  "Naming paper for content-addressable storage as a design mechanism (hash-of-contents block identity, write-once coalescing); full text confirmed live on the Plan 9 doc host.",
  ["content-addressable-storage"]),
W("new","an2594","AN2594: EEPROM emulation in STM32F10x microcontrollers","STMicroelectronics","living","st.com application note",None,"official-doc","core","unverified","url (st.com fetch timed out this session)",
  "The vendor app note that names the EEPROM-emulation-in-flash technique (paged flash + wear distribution) for MCUs.",
  ["eeprom-emulation-in-flash"]),
W("new","chungftl2009","A Survey of Flash Translation Layer","Chung, Park, Park, Lee, Lee & Song","2009","Journal of Systems Architecture 55(5-6)",None,"paper","survey","unverified","doi",
  "Survey treatment of FTL mapping schemes and wear-leveling policies; the catalog-grade umbrella for both flash elements.",
  ["flash-translation-layer","flash-wear-leveling"]),
W("new","littlefs","littlefs DESIGN.md","Christopher Haster / littlefs-project","living","github.com/littlefs-project/littlefs","https://github.com/littlefs-project/littlefs/blob/master/DESIGN.md","tooling-doc","core","verified",None,
  "Living embedded-flash design document teaching dynamic wear leveling and log-structured metadata on raw flash; confirmed live.",
  ["flash-wear-leveling","log-structured-storage"]),
]

gaps = []

notes = ("Route r6 (caching/memoization, data structures, persistence/durability; 97 elements) resolves to 7 memberships + 52 new works; "
         "every element is covered, no gaps. Anchors: CLRS (container/algorithm floor), Petrov + Kleppmann (storage engines), PEAA (the 18-element O/R mapping cluster), "
         "Ericson (spatial cluster), Coherence docs (the read/write-through naming family), IIR (search structures). "
         "Naming papers were included only where canon or sole coverage (Bloom, Flajolet, Cormode, Karger, Merkle, Pugh, Shapiro, Michael-Scott, Huet, Bagwell, Guttman, Fenwick, Briggs-Torczon, Lorie, Michie, Deutsch-Schiffman, P0661); "
         "O'Neil LSM 1996, ARIES, Mattson 1970, Manber-Myers, Fredkin, Broder and Bayer-McCreight were judged redundant against verified treatments (Petrov/Kleppmann/Gray-Reuter/Sedgewick/CLRS/IIR) and omitted. "
         "Crowley 1998 (piece-table naming) has no live authoritative host; coverage moved to Finseth (gap buffer) and the official VS Code piece-tree post. "
         "Verification: 34 of 52 new works confirmed on primary pages this session (publisher/author/standards/official project pages; several via first-page text of author-hosted PDFs). "
         "The 18 unverified entries carry UNRESOLVED soft fields, mostly DOIs behind blocked ACM/Springer/Wiley walls (dl.acm.org, link.springer.com and st.com were unreachable from this session). "
         "Memberships defer bibliographic verification to their existing corpus records.")

out = {"route": "r6", "works": works, "gaps": gaps, "notes": notes}

# ---- mechanical validation against the route file ----
route = json.load(open(BASE + "/p2/r6.json", encoding="utf-8"))
route_ids = {e["id"] for e in route["elements"]}
covered = set()
for w in works:
    for e in w["elements"]:
        assert e in route_ids, f"work {w['id']} references non-route element {e}"
        covered.add(e)
gap_ids = {g["element"] for g in gaps}
missing = route_ids - covered - gap_ids
assert not missing, f"uncovered elements: {sorted(missing)}"

ids = [w["id"] for w in works]
assert len(ids) == len(set(ids)), "duplicate work ids"

# id collision check for NEW works
work_tsv = {l.split("\t")[0] for l in open(BASE + "/work_ids.tsv", encoding="utf-8")}
elem_idx = {l.strip().split("\t")[0].split(" ")[0] for l in open(BASE + "/elements_index.txt", encoding="utf-8")}
for w in works:
    if w["action"] == "new":
        assert w["id"] not in work_tsv, f"new id collides with corpus work: {w['id']}"
        assert w["id"] not in elem_idx, f"new id collides with element id: {w['id']}"
    else:
        assert w["id"] in work_tsv, f"membership id not in corpus: {w['id']}"

n_mem = sum(1 for w in works if w["action"]=="membership")
n_new = sum(1 for w in works if w["action"]=="new")
n_ver = sum(1 for w in works if w["action"]=="new" and w["verification"]=="verified")
n_unv = sum(1 for w in works if w["action"]=="new" and w["verification"]=="unverified")

with open(BASE + "/p2out/r6.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)

print(f"OK route_elements={len(route_ids)} covered={len(covered)} memberships={n_mem} new={n_new} verified_new={n_ver} unverified_new={n_unv} gaps={len(gaps)}")
