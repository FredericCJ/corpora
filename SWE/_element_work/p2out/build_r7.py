import json, io, os

W = []
def w(action,id,title,authors,year,venue,ident,type,role,verification,unresolved,note,elements):
    W.append(dict(action=action,id=id,title=title,authors=authors,year=year,venue=venue,
                  ident=ident,type=type,role=role,verification=verification,
                  unresolved=unresolved,note=note,elements=elements))

# ---------- MEMBERSHIPS (reuse exact corpus ids; citation lives in corpus) ----------
w("membership","preschern","Fluent C: Principles, Practices, and Patterns","Christopher Preschern","2022","O'Reilly",None,"book","anchor","verified",None,
  "Route anchor for C code-structure idioms: #ifdef escape patterns, include guards, file/module organization, data lifetime & ownership (stateless vs global-state modules), Handle (opaque pointer).",
  ["escaping-ifdef-hell","include-guard","organizing-files-in-modular-c-programs","software-module-with-global-state","stateless-software-module","opaque-pointer"])
w("membership","preschernplop","Patterns for... EuroPLoP/PLoP pattern-paper series (organizing files; returning error information)","Christopher Preschern","UNRESOLVED","EuroPLoP/PLoP",None,"paper","core","verified",None,
  "The EuroPLoP paper form of the file-organization and data-lifetime pattern sets; names the route's module-state patterns.",
  ["organizing-files-in-modular-c-programs","software-module-with-global-state","stateless-software-module"])
w("membership","hanson","C Interfaces and Implementations: Techniques for Creating Reusable Software","David R. Hanson","1996","Addison-Wesley",None,"book","core","verified",None,
  "Canonical treatment of interface/implementation separation in C via opaque pointer types (ADTs behind incomplete types).",
  ["opaque-pointer"])
w("membership","tornhill","Patterns in C","Adam Tornhill","UNRESOLVED","Leanpub",None,"book","core","verified",None,
  "Names the same mechanism First-Class ADT; C-idiom treatment of opaque handles.",
  ["opaque-pointer"])
w("membership","ldd3","Linux Device Drivers, 3rd ed.","Jonathan Corbet, Alessandro Rubini, Greg Kroah-Hartman","2005","O'Reilly",None,"book","core","verified",None,
  "Teaches container_of embedded-struct navigation as the kernel's intrusive-composition idiom.",
  ["container-of"])
w("membership","noblesmallmem","Small Memory Software: Patterns for Systems with Limited Memory","James Noble, Charles Weir","2000","Addison-Wesley",None,"book","core","verified",None,
  "Pattern-catalog source for the memory-constrained data-representation trio: Compression, Multiple Representations, Packed Data.",
  ["compression","multiple-representations","packed-data"])
w("membership","iglberger","C++ Software Design: Design Principles and Patterns for High-Quality Software","Klaus Iglberger","2022","O'Reilly",None,"book","core","verified",None,
  "Modern C++ treatment that names and teaches Type Erasure and value semantics as design tools.",
  ["type-erasure","value-semantics"])
w("membership","carnieregisters","Making things do stuff (register access using C++ templates), Parts 1-8","Glennan Carnie","2017","Feabhas Sticky Bits blog",None,"blog","advanced","verified",None,
  "Embedded register-access series that applies tag dispatching and traits machinery in anger; the route's named_in for tag dispatching.",
  ["tag-dispatching","traits-class"])
w("membership","coreguidelines","C++ Core Guidelines","Bjarne Stroustrup, Herb Sutter (eds.)","living","isocpp.github.io",None,"tooling-doc","core","verified",None,
  "House C++ rules covering SF.8 include guards and Enum.3 prefer enum class (type-safe enumeration).",
  ["include-guard","type-safe-enum"])
w("membership","meyerseffmod","Effective Modern C++","Scott Meyers","2014","O'Reilly",None,"book","core","verified",None,
  "Item 10 (prefer scoped enums) is the modern C++ statement of the type-safe enum idiom.",
  ["type-safe-enum"])
w("membership","fowlerref","Refactoring","Martin Fowler","UNRESOLVED","Addison-Wesley",None,"book","core","verified",None,
  "Extract Function/Method is the operational route to Composed Method; Replace Method with Method Object (2nd ed. Replace Function with Command) and Replace Loop with Pipeline carry Method Object and Collection Pipeline.",
  ["composed-method","method-object","collection-pipeline"])
w("membership","embeddedrust","The Embedded Rust Book / Discovery book / Ferrous Systems materials","Rust Embedded WG","living","docs.rust-embedded.org",None,"course","core","verified",None,
  "Static Guarantees chapter is the living catalog-grade treatment of typestate programming (peripheral state machines in types).",
  ["typestate"])

# ---------- NEW WORKS ----------
w("new","becksbpp","Smalltalk Best Practice Patterns","Kent Beck","1996","Prentice Hall / Pearson","ISBN 978-0-13-476904-2","book","anchor","verified",None,
  "Names Composed Method and Method Object among its 92 coding patterns; the origin catalog for method-level structure.",
  ["composed-method","method-object"])
w("new","hodgsontoggles","Feature Toggles (aka Feature Flags)","Pete Hodgson","2017","martinfowler.com","https://martinfowler.com/articles/feature-toggles.html","guide","anchor","verified",None,
  "The catalog-grade treatment of feature flags: toggle taxonomy (release/experiment/ops/permissioning), toggle points, routers, configuration.",
  ["feature-flag"])
w("new","vlissideshatching","Pattern Hatching: Design Patterns Applied","John Vlissides","1998","Addison-Wesley","ISBN 978-0-201-43293-0","book","core","verified",None,
  "Names and works through Generation Gap (keeping generated and hand-written code apart via subclassing).",
  ["generation-gap"])
w("new","erlangcodereplace","Erlang/OTP System Documentation - Compilation and Code Loading","Ericsson AB","living","erlang.org","https://www.erlang.org/doc/system/code_loading.html","official-doc","anchor","verified",None,
  "Authoritative current/old-code semantics for hot code replacement; the reference realization of hot code reload.",
  ["hot-code-reload"])
w("new","meyersxmacros","The New C: X Macros","Randy Meyers","2001","C/C++ Users Journal 19(5)",None,"paper","core","unverified","primary page (CUJ/Dr. Dobb's defunct; archived full text at jacobfilipp.com/DrDobbs loaded live this session)",
  "The naming article for the X-macro parallel-table technique; full archived text confirms title/author/issue.",
  ["x-macro"])
w("new","clrs","Introduction to Algorithms, 3rd ed.","Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, Clifford Stein","2009","MIT Press","https://www.cs.dartmouth.edu/~thc/","book","core","verified",None,
  "Standard textbook treatment of graph representations (adjacency list vs adjacency matrix, ch. 22); edition/years confirmed on Cormen's page (MIT Press site blocks fetch, ISBN omitted).",
  ["adjacency-list-adjacency-matrix"])
w("new","nystromgpp","Game Programming Patterns","Robert Nystrom","2014","genever benning / gameprogrammingpatterns.com","https://gameprogrammingpatterns.com/","book","anchor","verified",None,
  "Route anchor for game-domain representation mechanisms: Bytecode (ch. 11) and Data Locality (ch. 17) confirmed in live ToC.",
  ["bytecode","data-locality"])
w("new","abadicolumn","The Design and Implementation of Modern Column-Oriented Database Systems","Daniel Abadi, Peter Boncz, Stavros Harizopoulos, Stratos Idreos, Samuel Madden","2013","Foundations and Trends in Databases 5(3)","DOI 10.1561/1900000024","paper","survey","verified",None,
  "The catalog-grade survey of columnar storage: column layouts, dictionary and light-weight compression encodings, PAX hybrid; verified via author-hosted final PDF.",
  ["column-oriented-storage","dictionary-encoding","pax-page-layout"])
w("new","plopd4","Pattern Languages of Program Design 4","Neil Harrison, Brian Foote, Hans Rohnert (eds.)","1999","Addison-Wesley","ISBN 978-0-201-43304-3","book","core","verified",None,
  "PLoPD volume carrying Noble's Basic Relationship Patterns (Relationship Object) and Carlson/Estepp/Fowler Temporal Patterns (Temporal Property).",
  ["relationship-object","temporal-property"])
w("new","plopd5","Pattern Languages of Program Design 5","Dragos Manolescu, Markus Voelter, James Noble (eds.)","2006","Addison-Wesley","ISBN 978-0-321-32194-7","book","core","verified",None,
  "PLoPD volume carrying the Comparand pattern (cheap identity testing via dedicated comparison values).",
  ["comparand"])
w("new","evansddd","Domain-Driven Design: Tackling Complexity in the Heart of Software","Eric Evans","2003","Addison-Wesley","ISBN 978-0-321-12521-7","book","core","verified",None,
  "Defines Entity and Value Object as domain-modeling building blocks (identity-bearing vs attribute-defined objects).",
  ["entity","value-object"])
w("new","fowlerpeaa","Patterns of Enterprise Application Architecture","Martin Fowler with Rice, Foemmel, Hieatt, Mee, Stafford","2002","Addison-Wesley","ISBN 0321127420","book","anchor","verified",None,
  "Enterprise pattern catalog naming Data Transfer Object, Record Set, and Value Object at design-element altitude.",
  ["data-transfer-object","record-set","value-object"])
w("new","fowleranalysis","Analysis Patterns: Reusable Object Models","Martin Fowler","1996","Addison-Wesley","ISBN 0201895420","book","core","verified",None,
  "Names Quantity (value + unit) and Range as reusable domain-model representations.",
  ["quantity","range"])
w("new","fowlerpipeline","Collection Pipeline","Martin Fowler","2015","martinfowler.com","https://martinfowler.com/articles/collection-pipeline/","guide","core","verified",None,
  "The naming treatment of the collection-pipeline style (map/filter/reduce composition) across languages.",
  ["collection-pipeline"])
w("new","hamming1950","Error Detecting and Error Correcting Codes","Richard W. Hamming","1950","Bell System Technical Journal 29(2)",None,"paper","core","unverified","doi/primary page (IEEE/Wiley archive not loadable this session)",
  "The founding paper of error-correcting codes (Hamming codes/distance); canonical naming source.",
  ["error-correcting-codes"])
w("new","chambersself89","An Efficient Implementation of Self, a Dynamically-Typed Object-Oriented Language Based on Prototypes","Craig Chambers, David Ungar, Elgin Lee","1989","OOPSLA '89 / SIGPLAN Notices 24(10)","https://bibliography.selflanguage.org/implementation.html","paper","core","verified",None,
  "Introduces implementation-level maps - the mechanism V8 later popularized as hidden classes; verified on the official Self bibliography site.",
  ["hidden-class"])
w("new","luebkelod","Level of Detail for 3D Graphics","David Luebke, Martin Reddy, Jonathan Cohen, Amitabh Varshney, Benjamin Watson, Robert Huebner","2003","Morgan Kaufmann","ISBN 1-55860-838-9","book","core","verified",None,
  "The book-length canonical treatment of level-of-detail representations; ISBN confirmed on official companion site lodbook.com.",
  ["level-of-detail"])
w("new","westecs","Evolve Your Hierarchy: Refactoring Game Entities with Components","Mick West","2007","Cowboy Programming (blog)","https://cowboyprogramming.com/2007/01/05/evolve-your-heirachy/","blog","anchor","verified",None,
  "The seminal article moving game entities from deep hierarchies to component composition; the route's ECS naming source.",
  ["entity-component-system"])
w("new","rustpatterns","Rust Design Patterns","rust-unofficial contributors","living","rust-unofficial.github.io","https://rust-unofficial.github.io/patterns/","guide","survey","verified",None,
  "Living Rust idiom catalog; Newtype entry confirmed live (zero-cost opaque wrapper types).",
  ["newtype"])
w("new","trpl","The Rust Programming Language","Steve Klabnik, Carol Nichols","living","doc.rust-lang.org","https://doc.rust-lang.org/book/","official-doc","core","verified",None,
  "Official book; ch. 6 teaches enums (tagged unions) and Option<T>, ch. 19 the newtype pattern - the mainstream systems-language realization of these representations.",
  ["tagged-union","option-type","newtype"])
w("new","rustapiguidelines","Rust API Guidelines","Rust library team","living","rust-lang.github.io","https://rust-lang.github.io/api-guidelines/future-proofing.html","official-doc","core","verified",None,
  "C-SEALED documents the sealed-trait idiom (private supertrait blocking downstream impls) as an API future-proofing rule.",
  ["sealed-trait"])
w("new","piercetapl","Types and Programming Languages","Benjamin C. Pierce","2002","MIT Press","ISBN 0-262-16209-1","book","core","verified",None,
  "Textbook foundation for sums/variants - the type-theoretic account of tagged unions; verified on the author's official book page.",
  ["tagged-union"])
w("new","ailamakipax01","Weaving Relations for Cache Performance","Anastassia Ailamaki, David J. DeWitt, Mark D. Hill, Marios Skounakis","2001","VLDB 2001","http://www.vldb.org/conf/2001/P169.pdf","paper","core","verified",None,
  "Introduces the PAX (Partition Attributes Across) page layout; verified via the official VLDB proceedings PDF.",
  ["pax-page-layout"])
w("new","wilsonkakkad92","Pointer Swizzling at Page Fault Time: Efficiently and Compatibly Supporting Huge Address Spaces on Standard Hardware","Paul R. Wilson, Sheetal V. Kakkad","1992","Int. Workshop on Object Orientation in Operating Systems (IWOOOS '92)",None,"paper","core","unverified","doi/primary page (only aggregator copies located this session)",
  "Canonical paper on swizzling persistent object references to raw pointers at fault time.",
  ["pointer-swizzling"])
w("new","gudeman93","Representing Type Information in Dynamically Typed Languages","David Gudeman","1993","University of Arizona TR 93-27",None,"report","survey","unverified","primary page (UA TR archive not loadable; identity corroborated via citing literature only)",
  "The canonical survey of pointer tagging, NaN-boxing and related runtime type-representation schemes.",
  ["pointer-tagging"])
w("new","petrovdbint","Database Internals: A Deep-Dive into How Distributed Data Systems Work","Alex Petrov","2019","O'Reilly","https://www.databass.dev/","book","core","verified",None,
  "Storage-engine half teaches on-disk page organization including slotted pages; confirmed via the book's official site (ISBN not shown there, omitted).",
  ["slotted-page-layout"])
w("new","ivanovatlas","Practical Texture Atlases","Ivan-Assen Ivanov","2006","Game Developer (Gamasutra)","https://www.gamedeveloper.com/programming/practical-texture-atlases","blog","core","verified",None,
  "Practitioner treatment of texture-atlas packing and batching; the NVIDIA 2004 whitepaper names the technique but has no stable primary page.",
  ["texture-atlas"])
w("new","blocheffjava","Effective Java, 3rd ed.","Joshua Bloch","2017","Addison-Wesley","ISBN 978-0-13-468599-1","book","core","verified",None,
  "Item 34 (enums instead of int constants) carries the Type-Safe Enum idiom Bloch named in the 1st ed. (2001, Item 21).",
  ["type-safe-enum"])
w("new","reactdocs","React documentation - Reconciliation","Meta / React team","living","legacy.reactjs.org / react.dev","https://legacy.reactjs.org/docs/reconciliation.html","official-doc","anchor","verified",None,
  "Official description of the virtual DOM diffing/reconciliation algorithm (O(n) heuristic, keys).",
  ["virtual-dom"])
w("new","appelcwc","Compiling with Continuations","Andrew W. Appel","1991","Cambridge University Press","DOI 10.1017/CBO9780511609619","book","core","verified",None,
  "The book-length treatment of continuation-passing style as a compiler intermediate representation.",
  ["continuation-passing-style"])
w("new","posa4","Pattern-Oriented Software Architecture Vol. 4: A Pattern Language for Distributed Computing","Frank Buschmann, Kevlin Henney, Douglas C. Schmidt","2007","Wiley","https://www.dre.vanderbilt.edu/~schmidt/POSA/","book","core","verified",None,
  "Carries Henney's value patterns incl. Copied Value; title/publisher/year confirmed on co-author Schmidt's official POSA page (ISBN omitted - Wiley page blocked).",
  ["copied-value"])
w("new","huttonhaskell","Programming in Haskell, 2nd ed.","Graham Hutton","2016","Cambridge University Press","ISBN 978-1316626221","book","anchor","verified",None,
  "Route anchor for FP idiom teaching: currying (ch. 4), algebraic data types incl. Maybe (ch. 8), monads (ch. 12); confirmed on the author's official CUP-linked page.",
  ["currying-partial-application","monad","option-type","tagged-union"])
w("new","moggi91","Notions of Computation and Monads","Eugenio Moggi","1991","Information and Computation 93(1)","https://person.dibris.unige.it/moggi-eugenio/ftp/ic91.pdf","paper","advanced","verified",None,
  "The paper that brought monads into programming-language semantics; verified via the author-hosted full text (title/author on first page).",
  ["monad"])
w("new","reynolds72","Definitional Interpreters for Higher-Order Programming Languages","John C. Reynolds","1972","ACM Annual Conference 1972; reprinted Higher-Order and Symbolic Computation 11 (1998)","https://homepages.inf.ed.ac.uk/wadler/papers/papers-we-love/reynolds-definitional-interpreters-1998.pdf","paper","advanced","verified",None,
  "Introduces defunctionalization (and CPS transformation of interpreters); verified via the hosted HOSC 1998 reprint full text.",
  ["defunctionalization"])
w("new","plotkinpretnar09","Handlers of Algebraic Effects","Gordon Plotkin, Matija Pretnar","2009","ESOP 2009, LNCS 5502, pp. 80-94","DOI 10.1007/978-3-642-00590-9_7","paper","advanced","verified",None,
  "The naming paper for effect handlers as the general mechanism behind exceptions, state, I/O and concurrency effects.",
  ["effect-handler"])
w("new","vandevoordetemplates","C++ Templates: The Complete Guide, 2nd ed.","David Vandevoorde, Nicolai M. Josuttis, Douglas Gregor","2017","Addison-Wesley","ISBN 978-0-321-71412-1","book","anchor","verified",None,
  "Route anchor for C++ template idioms: names and teaches SFINAE, traits, tag dispatching, typelists, EBCO, and expression templates in one catalog-grade reference.",
  ["sfinae","traits-class","tag-dispatching","typelist","empty-base-optimization-ebo","expression-templates"])
w("new","swierstra08","Data Types a la Carte","Wouter Swierstra","2008","Journal of Functional Programming 18(4)","DOI 10.1017/S0956796808006758","paper","advanced","verified",None,
  "Functional pearl assembling data types and interpreters from components via free monads; the route's free-monad source.",
  ["free-monad"])
w("new","coplienadvcpp","Advanced C++: Programming Styles and Idioms","James O. Coplien","1991","Addison-Wesley","ISBN 978-0-201-54855-6","book","core","verified",None,
  "The original C++ idioms catalog; names the functor (function object) idiom.",
  ["function-object"])
w("new","alexandrescu","Modern C++ Design: Generic Programming and Design Patterns Applied","Andrei Alexandrescu","2001","Addison-Wesley","ISBN 978-0-201-70431-0","book","advanced","verified",None,
  "Names Typelists (ch. 3) and generalized functors (ch. 5), with TypeTraits (ch. 2) - foundational C++ type-level idiom catalog.",
  ["typelist","function-object","traits-class"])
w("new","bernhardtfcis","Functional Core, Imperative Shell","Gary Bernhardt","2012","Destroy All Software screencast (Classic Season 4)","https://www.destroyallsoftware.com/screencasts/catalog/functional-core-imperative-shell","course","anchor","verified",None,
  "The naming screencast for the functional-core/imperative-shell structuring idiom; episode confirmed in the live catalog.",
  ["functional-core-imperative-shell"])
w("new","fosterlenses","Combinators for Bi-Directional Tree Transformations: A Linguistic Approach to the View Update Problem","J. Nathan Foster, Michael B. Greenwald, Jonathan T. Moore, Benjamin C. Pierce, Alan Schmitt","2007","ACM TOPLAS 29(3)","https://www.cis.upenn.edu/~bcpierce/papers/lenses-toplas-final.pdf","paper","advanced","verified",None,
  "The paper that dubbed bidirectional accessors lenses; verified via the author-hosted TOPLAS final text (DOI omitted - ACM DL blocked).",
  ["lens"])
w("new","osmanijs","Learning JavaScript Design Patterns, 2nd ed.","Addy Osmani","2023","O'Reilly","https://patterns.addy.ie/","book","core","verified",None,
  "Catalog-grade JS pattern book; Module and Revealing Module pattern chapters confirmed on the author's official online edition.",
  ["module-pattern"])
w("new","leijenmeijer99","Domain Specific Embedded Compilers","Daan Leijen, Erik Meijer","1999","2nd USENIX Conference on Domain-Specific Languages (DSL'99)",None,"paper","advanced","unverified","primary page (USENIX pages returned 403 this session; listing seen in search index only)",
  "The paper that introduced phantom type variables for typing embedded DSL expressions.",
  ["phantom-type"])
w("new","ingerman61","Thunks: A Way of Compiling Procedure Statements with Some Comments on Procedure Declarations","P. Z. Ingerman","1961","Communications of the ACM 4(1)",None,"paper","core","unverified","doi (ACM DL blocked this session)",
  "The naming paper for thunks (delayed-evaluation closures for call-by-name argument passing).",
  ["thunk"])
w("new","stromyemini86","Typestate: A Programming Language Concept for Enhancing Software Reliability","Robert E. Strom, Shaula Yemini","1986","IEEE Transactions on Software Engineering SE-12(1)",None,"paper","advanced","unverified","doi/primary page (IEEE Xplore not loadable this session)",
  "The naming paper for typestate; the Embedded Rust Book membership carries the living realization.",
  ["typestate"])
w("new","carettetagless09","Finally Tagless, Partially Evaluated: Tagless Staged Interpreters for Simpler Typed Languages","Jacques Carette, Oleg Kiselyov, Chung-chieh Shan","2009","Journal of Functional Programming 19(5), pp. 509-543","https://okmij.org/ftp/tagless-final/index.html","paper","advanced","verified",None,
  "The naming paper for the tagless-final embedding style; JFP citation confirmed on Kiselyov's official tagless-final page.",
  ["tagless-final"])
w("new","kennedyunits","Types for Units-of-Measure: Theory and Practice","Andrew Kennedy","2010","CEFP 2009, LNCS 6299, pp. 268-305","DOI 10.1007/978-3-642-17685-2_8","paper","core","verified",None,
  "Definitive treatment of units-of-measure types (theory + the F# realization); subsumes Kennedy's 1996 dissertation line of work.",
  ["units-of-measure-types"])
w("new","morecppidioms","More C++ Idioms","Wikibooks contributors","living","en.wikibooks.org","https://en.wikibooks.org/wiki/More_C%2B%2B_Idioms","guide","survey","verified",None,
  "Living C++ idiom catalog; EBO, SFINAE/enable-if, Type Erasure, Expression Template, and Tag Dispatching entries confirmed in live ToC.",
  ["empty-base-optimization-ebo","sfinae","type-erasure","expression-templates","tag-dispatching"])

out = {
 "route": "r7",
 "works": W,
 "gaps": [],
 "notes": ("All route elements are covered by >=1 catalog-grade work; no gaps. 12 memberships reuse exact corpus ids "
           "(membership verification is inherited from the corpus - no bibliographic re-verification performed, per contract). "
           "48 new works: 41 verified against live primary/authoritative pages this session (publisher/InformIT pages, official project "
           "sites, author-hosted final texts, Springer/Cambridge DOIs, VLDB proceedings, Self bibliography); 7 unverified with the soft "
           "field named (meyersxmacros, hamming1950, wilsonkakkad92, gudeman93, leijenmeijer99, ingerman61, stromyemini86 - defunct venues "
           "or ACM/IEEE fetch blocks; each is nonetheless the canonical naming source for its element). Economy choices: "
           "C++ Templates 2nd ed. + More C++ Idioms jointly cover the C++ type-idiom cluster instead of six single-idiom articles "
           "(Veldhuizen 1995 and Myers 1995 C++ Report naming articles noted here in prose, not added as nodes); the Abadi et al. "
           "FnT survey covers the columnar cluster so C-Store (Stonebraker 2005) is not added as a separate node; Hutton's Programming in "
           "Haskell carries FP teaching coverage (currying/monads/Maybe/ADTs) so the Haskell 98 Report is not added. Corrections found "
           "during verification: Coplien's Advanced C++ is 1991 (route file said 1992); Beck SBPP is 1996 (route said 1997); PLoPD4 "
           "published Dec 1999 (copyright 2000); Kennedy units chapter is 2010 (LNCS 6299) covering the CEFP 2009 school.")
}

# validation: coverage completeness + id integrity
base = os.path.dirname(os.path.abspath(__file__))
route = json.load(open(os.path.join(base, "..", "p2", "r7.json"), encoding="utf-8"))
route_ids = {e["id"] for e in route["elements"]}
covered = set()
for wk in W:
    for e in wk["elements"]:
        assert e in route_ids, "unknown element %s in %s" % (e, wk["id"])
        covered.add(e)
missing = route_ids - covered
assert not missing, "uncovered: %s" % missing
ids = [wk["id"] for wk in W]
assert len(ids) == len(set(ids)), "dup work ids"
print("route elements:", len(route_ids), "| covered:", len(covered), "| works:", len(W),
      "| memberships:", sum(1 for x in W if x["action"]=="membership"),
      "| new:", sum(1 for x in W if x["action"]=="new"),
      "| new verified:", sum(1 for x in W if x["action"]=="new" and x["verification"]=="verified"),
      "| new unverified:", sum(1 for x in W if x["action"]=="new" and x["verification"]=="unverified"))

with io.open(os.path.join(base, "r7.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("written")
