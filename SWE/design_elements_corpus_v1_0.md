# SWE Corpus — Pass 8: The Design-Element Resource Pass (`design-elements`)

**Scope.** The works that *define and teach* the 708 elements of `design_elements_catalog_v1_0.md` — naming sources plus best modern treatments, mapped many-to-many onto element ids. This pass merges into the existing 7-pass unified corpus by record id: works already carried by another pass are **memberships** (they REUSE the exact existing id), only genuinely absent works are new nodes.

**Collection date:** 2026-07-11 (elements catalog frozen 2026-07-10). **Mapping rule:** every catalog element must be reachable from ≥1 catalog-grade work; a work claims an element only when it defines or teaches it at catalog grade (mere mention is not coverage); unreachable elements are explicit gaps, never padded.

## Tag legend

- `route:` r1–r11 — the element-domain route that claimed the work (a work can serve several; it is listed under its primary route with the others noted).
- `role:` anchor | core | advanced | survey — the route's own emphasis.
- `verification:` **verified** = a primary or authoritative page (publisher / ACM–IEEE DL / standards body / official project site) was loaded live this session confirming the exact identifier; **unverified** = recall/search-index only, soft field named in `UNRESOLVED`. No ISBN/DOI/year is fabricated — omitted sooner than guessed.
- `elements:` the many-to-many payload — catalog element ids this work defines/teaches (machine-parseable; Phase 4 ingests it).

**Census.** **399 pass-8 members** = **63 memberships** (existing corpus works reclaimed under the element lens) + **336 new nodes** (273 verified / 63 unverified-quarantined). Element coverage: **706/709** elements reachable from ≥1 work; multiplicity: 473×1, 178×2, 55×≥3. Uncovered: 3 (listed in the audit section).

---

## R1. OO, construction & testing canon

### New

1. **Smalltalk Best Practice Patterns** — Kent Beck, 1997. Prentice Hall. ISBN 978-0-13-476904-2. `{r1 | anchor | verified}` — Names Collecting Parameter and Pluggable Selector among its 92 coding patterns. InformIT page loaded live (published Oct 1996, copyright 1997). (also serves r11, r7)
   - elements: collecting-parameter, composed-method, execute-around-method, method-object, pluggable-selector
2. **Domain-Driven Design: Tackling Complexity in the Heart of Software** — Eric Evans, 2003. Addison-Wesley. ISBN 978-0-321-12521-7. `{r1 | anchor | verified}` — Defines Domain Services and gives the book-form treatment of Specification. InformIT page loaded live. (also serves r10, r7)
   - elements: aggregate, domain-service, entity, specification, value-object
3. **Inversion of Control Containers and the Dependency Injection pattern** — Martin Fowler, 2004. martinfowler.com. https://martinfowler.com/articles/injection.html. `{r1 | anchor | verified}` — The naming article for Dependency Injection (constructor/setter/interface forms) and the standard catalog-grade comparison with Service Locator. Loaded live (23 Jan 2004).
   - elements: dependency-injection, service-locator
4. **xUnit Test Patterns: Refactoring Test Code** — Gerard Meszaros, 2007. Addison-Wesley. ISBN 978-0-13-149505-0. `{r1 | anchor | verified}` — The testing-constructs anchor: names Four-Phase Test, Humble Object, Parameterized Test, Test Double, and the fixture pattern family; documents Object Mother as a Creation Method variation. InformIT page loaded live.
   - elements: four-phase-test, humble-object, object-mother, parameterized-test, test-double, test-fixture
5. **Object-Oriented Software Construction, 2nd ed.** — Bertrand Meyer, 1997. Prentice Hall. https://bertrandmeyer.com/oosc2/. `{r1 | anchor | verified}` — The defining treatment of Design by Contract. Author's official OOSC2 page loaded live (full text hosted with Pearson's permission); ISBN not shown, omitted.
   - elements: design-by-contract
6. **Game Programming Patterns** — Robert Nystrom, 2014. Genever Benning / gameprogrammingpatterns.com. https://gameprogrammingpatterns.com/. `{r1 | anchor | verified}` — Official site contents loaded live confirming all ten route chapters: Component, Subclass Sandbox, Type Object, Service Locator, plus the GoF revisits (Command, Flyweight, Observer, Prototype, Singleton, State). (also serves r10, r3, r4, r6, r7)
   - elements: bytecode, bytecode-virtual-machine, command, component, data-locality, dirty-flag, double-buffer, finite-state-machine, fixed-timestep, flyweight, game-loop, observer, prototype, service-locator, singleton, spatial-partition, state, subclass-sandbox, type-object, undo-redo-command-stack, update-method
7. **Pattern Languages of Program Design 3** — Robert C. Martin, Dirk Riehle, Frank Buschmann (eds.), 1997. Addison-Wesley. ISBN 978-0-201-31011-5. `{r1 | anchor | verified}` — The PLoP canon volume for this route: Null Object (Woolf), Acyclic Visitor (Martin), Extension Object (Gamma), External Polymorphism (Cleeland/Schmidt/Harrison), Product Trader (Baeumer/Riehle), Sponsor-Selector (Wallingford), Bureaucracy (Riehle), Type Object (Johnson/Woolf). InformIT page loaded live; published Oct 1997 (often cited 1998). (also serves r8)
   - elements: acyclic-visitor, bureaucracy, diagnostic-context, diagnostic-logger, extension-object, external-polymorphism, null-object, product-trader, sponsor-selector, type-object
8. **Patterns of Enterprise Application Architecture** — Martin Fowler (with Rice, Foemmel, Hieatt, Mee, Stafford), 2002. Addison-Wesley. https://martinfowler.com/books/eaa.html. `{r1 | anchor | verified}` — Names the route's base patterns (Plugin, Registry, Mapper, Layer Supertype, Separated Interface, Special Case, Service Stub); official book page + eaaCatalog loaded live confirming all seven; ISBN not shown on page, omitted. (also serves r2, r3, r5, r6, r7, r9)
   - elements: active-record, association-table-mapping, class-table-inheritance, coarse-grained-lock, concrete-table-inheritance, data-mapper, data-transfer-object, dependent-mapping, embedded-value, foreign-key-mapping, gateway, identity-field, identity-map, implicit-lock, inheritance-mappers, layer-supertype, mapper, metadata-mapping, money, optimistic-offline-lock, pessimistic-offline-lock, plugin, query-object, record-set, registry, repository, row-data-gateway, separated-interface, serialized-lob, service-stub, single-table-inheritance, special-case, table-data-gateway, template-engine, unit-of-work, value-object
9. **QuickCheck: A Lightweight Tool for Random Testing of Haskell Programs** — Koen Claessen, John Hughes, 2000. ICFP 2000 / official QuickCheck page, Chalmers. https://www.cse.chalmers.se/~rjmh/QuickCheck/. `{r1 | anchor | verified}` — The paper that founded property-based testing; authors' official QuickCheck page loaded live referencing the ICFP 2000 paper (ACM DL 403, DOI omitted).
   - elements: property-based-testing
10. **Mixin-Based Inheritance** — Gilad Bracha, William Cook, 1990. OOPSLA/ECOOP '90, ACM SIGPLAN Notices 25(10). `{r1 | advanced | unverified}` — The paper that established mixins as a linguistic construct; Osmani (verified) is the covering modern treatment. **UNRESOLVED:** doi/primary page — ACM DL 403 and bracha.org paper page 404 this session; DOI omitted rather than guessed.
   - elements: mixin
11. **Functional options for friendly APIs** — Dave Cheney, 2014. dave.cheney.net / dotGo 2014. https://dave.cheney.net/2014/10/17/functional-options-for-friendly-apis. `{r1 | core | verified}` — The standard reference for Go functional options; loaded live, credits Rob Pike's 2014 self-referential-functions post as origin.
   - elements: functional-options
12. **Advanced C++: Programming Styles and Idioms** — James O. Coplien, 1991. Addison-Wesley. ISBN 978-0-201-54855-6. `{r1 | core | verified}` — The original C++ idioms catalog; names the functor (function object) idiom. **UNRESOLVED:** isbn — no publisher page reachable this session (Pearson page gone; only retail/archive listings); ISBN omitted rather than guessed. (also serves r7)
   - elements: bridge, envelope-letter, function-object
13. **Effective Java, 3rd ed.** — Joshua Bloch, 2018. Addison-Wesley. ISBN 978-0-13-468599-1. `{r1 | core | verified}` — Item 1 is the canonical static-factory-method treatment, Item 41 defines marker interfaces, Item 2 is the modern Builder treatment. InformIT page loaded live (published Dec 2017, copyright 2018). (also serves r7, r8, r9)
   - elements: builder, defensive-copy, marker-interface, serialization-proxy, static-factory-method, type-safe-enum
14. **Domain-Specific Languages** — Martin Fowler (with Rebecca Parsons), 2010. Addison-Wesley. ISBN 0-321-71294-3. `{r1 | core | verified}` — Official book page loaded live (ISBN shown). Catalogs Expression Builder (ch. 32 / dslCatalog) and is the standard treatment of internal/embedded DSLs as fluent APIs over a host language. (also serves r9)
   - elements: embedded-domain-specific-language, expression-builder, parser-combinator, semantic-model, symbol-table
15. **FluentInterface (bliki)** — Martin Fowler (term coined with Eric Evans), 2005. martinfowler.com. https://martinfowler.com/bliki/FluentInterface.html. `{r1 | core | verified}` — The naming source for the fluent-interface style. Loaded live (20 Dec 2005).
   - elements: fluent-interface
16. **PageObject (bliki)** — Martin Fowler, 2013. martinfowler.com. https://martinfowler.com/bliki/PageObject.html. `{r1 | core | verified}` — The canonical definition of the Page Object UI-test pattern (popularized by Selenium). Loaded live (10 Sep 2013).
   - elements: page-object
17. **Growing Object-Oriented Software, Guided by Tests** — Steve Freeman, Nat Pryce, 2009. Addison-Wesley. ISBN 978-0-321-50362-6. `{r1 | core | verified}` — Book-form treatment of Test Data Builders (ch. 22), from the pattern's author (Pryce, 2007). InformIT page loaded live.
   - elements: test-data-builder
18. **Smart constructors (Haskell wiki)** — haskell.org wiki contributors, living. wiki.haskell.org. https://wiki.haskell.org/Smart_constructors. `{r1 | core | verified}` — The established treatment of the smart-constructor idiom (runtime, compile-time, and normalizing variants); loaded live.
   - elements: smart-constructor
19. **Building Domain-Specific Embedded Languages** — Paul Hudak, 1996. ACM Computing Surveys 28(4es). `{r1 | advanced | unverified}` — The naming paper for embedded (internal) DSLs in the FP tradition; Fowler's DSL book is the verified modern treatment. **UNRESOLVED:** doi — ACM DL returned 403 this session; DOI omitted rather than guessed.
   - elements: embedded-domain-specific-language
20. **A Simple Technique for Handling Multiple Polymorphism** — Daniel H. H. Ingalls, 1986. OOPSLA 1986. `{r1 | advanced | unverified}` — The naming paper for double dispatch; GoF's Visitor section (membership) is the verified covering treatment. **UNRESOLVED:** doi/primary page — ACM DL 403 this session and no author-hosted copy found; citation from route file.
   - elements: double-dispatch
21. **Using Prototypical Objects to Implement Shared Behavior in Object-Oriented Systems** — Henry Lieberman, 1986. OOPSLA 1986. http://web.media.mit.edu/~lieber/Lieberary/OOP/Delegation/Delegation.html. `{r1 | core | verified}` — The naming treatment of delegation as an object-composition mechanism; author's MIT-hosted full text loaded live.
   - elements: delegation
22. **Agile Software Development: Principles, Patterns, and Practices** — Robert C. Martin, 2003. Pearson / Prentice Hall. ISBN 978-0-13-597444-5. `{r1 | core | verified}` — Ch. 16 (Singleton and Monostate) is the standard Monostate treatment; ch. 17 is a full Null Object chapter. InformIT page loaded live with ToC.
   - elements: monostate, null-object
23. **More C++ Idioms** — Wikibooks contributors, living. en.wikibooks.org. https://en.wikibooks.org/wiki/More_C%2B%2B_Idioms. `{r1 | core | verified}` — The established living catalog of C++ idioms; loaded live confirming Construct On First Use, Named Parameter, and Nifty Counter entries. (also serves r7)
   - elements: construct-on-first-use, empty-base-optimization-ebo, expression-templates, named-parameter-idiom, nifty-counter, sfinae, tag-dispatching, type-erasure
24. **Modern C++ Design: Generic Programming and Design Patterns Applied** — Andrei Alexandrescu, 2001. Addison-Wesley. ISBN 978-0-201-70431-0. `{r1 | core | verified}` — The naming source and canonical treatment of policy-based design. InformIT page loaded live. (also serves r7)
   - elements: function-object, policy-based-design, traits-class, typelist
25. **Retained Mode Versus Immediate Mode (Win32 Learn)** — Microsoft, living. learn.microsoft.com. https://learn.microsoft.com/en-us/windows/win32/learnwin32/retained-mode-versus-immediate-mode. `{r1 | core | verified}` — Official definitional treatment of retained-mode vs immediate-mode APIs (declarative scene model vs per-frame draw commands); loaded live in full.
   - elements: immediate-mode-gui, retained-mode-gui
26. **Immediate-Mode Graphical User Interfaces (2005)** — Casey Muratori, 2005. caseymuratori.com (video lecture). https://caseymuratori.com/blog_0001. `{r1 | core | verified}` — The lecture that coined IMGUI as a GUI paradigm; author's page loaded live.
   - elements: immediate-mode-gui
27. **Learning JavaScript Design Patterns, 2nd ed.** — Addy Osmani, living. O'Reilly / patterns.addy.ie. https://patterns.addy.ie/. `{r1 | core | verified}` — Author's official online 2nd edition loaded live; its structural-patterns chapter gives a catalog-grade modern Mixin treatment (subclassing/superclassing/constructor-augmenting variants). (also serves r7)
   - elements: mixin, module-pattern
28. **Pattern Languages of Program Design 4** — Neil Harrison, Brian Foote, Hans Rohnert (eds.), 2000. Addison-Wesley. ISBN 978-0-201-43304-3. `{r1 | core | verified}` — InformIT page loaded live with contents confirming Abstract Session (Pryce), Object Recursion (Woolf), and Role Object (Baeumer/Riehle/Siberski/Wulf) — Role Object lives here, not in PLoPD3. Published Dec 1999, copyright 2000. (also serves r7)
   - elements: abstract-session, object-recursion, relationship-object, role-object, temporal-property
29. **Pattern-Oriented Software Architecture Vol. 1: A System of Patterns** — Frank Buschmann, Regine Meunier, Hans Rohnert, Peter Sommerlad, Michael Stal, 1996. Wiley. ISBN 0471958697. `{r1 | core | verified}` — Names Forwarder-Receiver, Client-Dispatcher-Server, and Publisher-Subscriber; ISBN/year/publisher confirmed live via hillside.net book record + Schmidt's POSA series page (Wiley/O'Reilly pages blocked this session). **UNRESOLVED:** isbn/authors — Wiley and O'Reilly product pages returned 403 this session; title + year 1996 confirmed live on Schmidt's official POSA series page; ISBN omitted rather than guessed. (also serves r2, r4)
   - elements: client-dispatcher-server, command-processor, forwarder-receiver, master-slave, observer, publish-subscribe-channel, view-handler, whole-part
30. **Pattern-Oriented Software Architecture Vol. 4: A Pattern Language for Distributed Computing** — Buschmann, Henney, Schmidt, 2007. Wiley. ISBN 0-470-05902-8. `{r1 | core | verified}` — Names the route's interface/interaction patterns Batch Method, Combined Method, Enumeration Method, Explicit Interface, Introspective Interface, Lifecycle Callback. Schmidt's official POSA4 page loaded live (title/authors/year/ISBN). (also serves r10, r11, r2, r7)
   - elements: batch-method, collections-for-states, combined-method, context-object, copied-value, enumeration-method, explicit-interface, half-object-plus-protocol, immutable-value, introspective-interface, lifecycle-callback, lookup, methods-for-states, object-manager
31. **Refactoring.Guru — Design Patterns catalog** — Alexander Shvets, living. refactoring.guru. https://refactoring.guru/design-patterns. `{r1 | survey | verified}` — Living catalog loaded live: modern multi-language treatments of 22 GoF patterns (all except Interpreter).
   - elements: abstract-factory, adapter, bridge, builder, chain-of-responsibility, command, composite, decorator, facade, factory-method, flyweight, iterator, mediator, memento, observer, prototype, proxy, singleton, state, strategy, template-method, visitor
32. **SourceMaking — Design Patterns catalog** — SourceMaking, living. sourcemaking.com. https://sourcemaking.com/design_patterns. `{r1 | survey | verified}` — Living catalog; its Private Class Data page (loaded live) is the only catalog-grade treatment of that element found.
   - elements: private-class-data
33. **Specifications** — Eric Evans, Martin Fowler, 1997. PLoP workshop paper, hosted at martinfowler.com. https://www.martinfowler.com/apsupp/spec.pdf. `{r1 | advanced | unverified}` — The naming paper for the Specification pattern, kept as provenance alongside the DDD book treatment. **UNRESOLVED:** year/venue — the hosted PDF downloaded live but is password-protected and unreadable this session; citation from route file.
   - elements: specification
34. **Virtuality** — Herb Sutter, 2001. C/C++ Users Journal 19(9). `{r1 | core | unverified}` — The article that names the Non-Virtual Interface (NVI) idiom; Meyers Effective C++ Item 35 (membership) is the verified covering treatment. **UNRESOLVED:** live page — gotw.ca failed TLS handshake this session and archive fetch is blocked; citation from route file.
   - elements: non-virtual-interface-nvi
35. **Twin — A Design Pattern for Modeling Multiple Inheritance** — Hanspeter Moessenboeck, 2000. Perspectives of System Informatics (PSI 1999), Springer LNCS 1755. DOI 10.1007/3-540-46562-6_31. `{r1 | core | verified}` — The naming paper for the Twin pattern; Springer chapter page loaded live (pp. 358-369, LNCS 1755). Only catalog-grade source for this element.
   - elements: twin
36. **Working Effectively with Legacy Code** — Michael Feathers, 2004. Prentice Hall. ISBN 978-0-13-117705-5. `{r1 | core | verified}` — Defines characterization tests — the canonical book form of golden-master/snapshot testing. InformIT page loaded live.
   - elements: golden-master-testing

### Membership (existing works, reclaimed under the element lens)

37. **[MEMBERSHIP id=gof]** `{r1 | anchor | verified}` — The canonical catalog for the route's 23 GoF patterns; ch.1 also defines delegation as a reuse mechanism, Visitor defines double dispatch, Template Method defines hook operations. (also serves r10)
   - elements: abstract-factory, adapter, bridge, builder, chain-of-responsibility, command, composite, decorator, delegation, double-dispatch, facade, factory-method, flyweight, hook-method, interpreter, iterator, mediator, memento, observer, prototype, proxy, singleton, state, strategy, template-method, undo-redo-command-stack, visitor
38. **[MEMBERSHIP id=posa2]** `{r1 | anchor | verified}` — Names and specifies Wrapper Facade, Extension Interface, and Interceptor with full pattern forms. (also serves r11, r2, r4, r5)
   - elements: acceptor-connector, active-object, asynchronous-completion-token, component-configurator, double-checked-locking, event-loop, extension-interface, half-sync-half-async, interceptor, leader-followers, monitor-object, proactor, reactor, scoped-locking, strategized-locking, thread-safe-interface, thread-specific-storage, wrapper-facade
39. **[MEMBERSHIP id=preschern]** `{r1 | anchor | verified}` — Names the route's C API-shape patterns Aggregate Instance, Function Control, and Out-Parameters. (also serves r11, r7, r8)
   - elements: aggregate-instance, allocation-wrapper, callee-allocates, caller-owned-buffer, cleanup-record, dedicated-ownership, escaping-ifdef-hell, function-control, goto-cleanup, guard-clause, include-guard, lazy-cleanup, log-errors, opaque-pointer, organizing-files-in-modular-c-programs, out-parameters, pointer-check, pool-allocation, return-status-code, samurai-principle, software-module-with-global-state, special-return-value, stack-first, stateless-software-module
40. **[MEMBERSHIP id=beningofw]** `{r1 | core | verified}` — Book-length treatment of designing hardware abstraction layers for embedded C.
   - elements: hardware-abstraction-layer
41. **[MEMBERSHIP id=fowlerref]** `{r1 | core | verified}` — Introduce Null Object (1st ed.) / Introduce Special Case (2nd ed.) are catalog-grade treatments of both elements. (also serves r7, r8)
   - elements: collection-pipeline, composed-method, guard-clause, method-object, null-object, special-case
42. **[MEMBERSHIP id=grenningtdd]** `{r1 | core | verified}` — Teaches test doubles (spies/fakes/mocks in C), test fixtures, and the four-phase test structure in the corpus's embedded center of gravity.
   - elements: four-phase-test, test-double, test-fixture
43. **[MEMBERSHIP id=iglberger]** `{r1 | core | verified}` — The best modern C++ treatment of the classic patterns it revisits (value-semantic Visitor/Strategy, External Polymorphism, CRTP, Bridge/pimpl, Decorator, Singleton). (also serves r11, r7)
   - elements: adapter, bridge, command, curiously-recurring-template-pattern-crtp, decorator, external-polymorphism, observer, prototype, singleton, small-buffer-optimization, strategy, type-erasure, value-semantics, visitor
44. **[MEMBERSHIP id=kandr]** `{r1 | core | verified}` — Sec. 5.11 pointers-to-functions is the naming-grade source for the C function-pointer dispatch table.
   - elements: function-pointer-dispatch-table
45. **[MEMBERSHIP id=martincleanarch]** `{r1 | core | verified}` — Ch. 23 (Presenters and Humble Objects) is a modern treatment of the Humble Object pattern beyond its test-pattern origin.
   - elements: humble-object
46. **[MEMBERSHIP id=mcconnell]** `{r1 | core | verified}` — Ch. 18 Table-Driven Methods is the modern didactic treatment of dispatch/jump tables. (also serves r8)
   - elements: function-pointer-dispatch-table, sanity-check, sentinel-value
47. **[MEMBERSHIP id=meyerseffcpp]** `{r1 | core | verified}` — Item 4 teaches the construct-on-first-use local-static technique; Item 35 presents NVI as the named alternative to public virtuals.
   - elements: construct-on-first-use, non-virtual-interface-nvi
48. **[MEMBERSHIP id=pigweedsdk]** `{r1 | core | verified}` — Defines the facade/backend module pattern as its documented module architecture.
   - elements: facade-backend-module-pattern
49. **[MEMBERSHIP id=schreiner]** `{r1 | core | verified}` — The canonical construction of OO in plain C, including explicit vtable dispatch. (also serves r2)
   - elements: callback, object-orientation-in-c, oo-in-c-via-explicit-vtable

## R2. Communication & messaging

### New

50. **Implementing Remote Procedure Calls** — Andrew D. Birrell, Bruce Jay Nelson, 1984. ACM Transactions on Computer Systems 2(1), 39-59. DOI 10.1145/2080.357392. `{r2 | core | verified}` — The canon paper defining the RPC mechanism (stubs, binding, transport semantics) - both naming source and implementation treatment; dblp record loaded live.
   - elements: remote-procedure-call
51. **Domain-Driven Design Reference: Definitions and Pattern Summaries** — Eric Evans, 2015. Domain Language, Inc.. https://www.domainlanguage.com/ddd/reference/. `{r2 | core | unverified}` — Phase-1 naming source for Domain Event (the DDD pattern definition); element remains verified-reachable via eaadev. **UNRESOLVED:** primary page (domainlanguage.com) returned HTTP 403 this session; title/year carried from the Phase-1 catalog, not re-confirmed live.
   - elements: domain-event
52. **The Little Book of Semaphores** — Allen B. Downey. Green Tea Press. https://greenteapress.com/wp/semaphores/. `{r2 | core | verified}` — The free canonical modern teaching of the classical synchronization problems including producer-consumer; publisher page loaded live. **UNRESOLVED:** year: publisher page loaded live confirms title/author/producer-consumer coverage but shows no edition year.
   - elements: producer-consumer
53. **Further Enterprise Application Architecture development (eaaDev pattern drafts)** — Martin Fowler, living. martinfowler.com. https://martinfowler.com/eaaDev/. `{r2 | core | verified}` — Fowler's post-PoEAA draft catalog: EventAggregator.html (2004) and DomainEvent.html (2005) loaded live - the naming/defining pages for Event Aggregator and the standard free treatment of Domain Event. (also serves r8)
   - elements: audit-log, domain-event, event-aggregator, notification
54. **Effective Go** — The Go project, living. go.dev. https://go.dev/doc/effective_go. `{r2 | core | verified}` — The best-known living treatment of CSP channels in practice ('share memory by communicating'; buffered/unbuffered channels, channel idioms); page loaded live.
   - elements: csp-channel
55. **Cooperating Sequential Processes (EWD123)** — Edsger W. Dijkstra, 1965. Technological University Eindhoven / E.W. Dijkstra Archive (UT Austin). https://www.cs.utexas.edu/users/EWD/transcriptions/EWD01xx/EWD123.html. `{r2 | core | verified}` — The naming source of the producer-consumer cooperation problem (sections 4.1/4.3: producer/consumer, bounded buffer, semaphores); archive transcription loaded live confirming content. **UNRESOLVED:** year: transcription page itself undated; 1965 is the EWD archive's standard dating for EWD123. (also serves r5)
   - elements: critical-region, producer-consumer, semaphore
56. **Communicating Sequential Processes** — C. A. R. Hoare, 1978. Communications of the ACM 21(8), 666-677. DOI 10.1145/359576.359585. `{r2 | core | verified}` — The canon naming paper for CSP-style channel communication between processes; dblp record loaded live confirming DOI/venue/year (ACM DL blocked).
   - elements: csp-channel
57. **Interest management for distributed virtual environments: A survey** — Elvis S. Liu, Georgios K. Theodoropoulos, 2014. ACM Computing Surveys 46(4), 51:1-51:42. DOI 10.1145/2535417. `{r2 | survey | verified}` — The catalog-grade survey of interest management (aura/region/class-based filtering in networked games and simulations) - upgrades the element from tech-report-only naming; dblp record loaded live.
   - elements: interest-management
58. **Event Delegation - The Modern JavaScript Tutorial** — Ilya Kantor et al. (javascript.info), living. javascript.info. https://javascript.info/event-delegation. `{r2 | core | verified}` — The tutorial chapter defining and teaching event delegation (single ancestor handler + event.target dispatch, behavior pattern); page loaded live.
   - elements: event-delegation
59. **Signals & Slots - Qt Documentation** — The Qt Company, living. doc.qt.io (Qt 6). https://doc.qt.io/qt-6/signalsandslots.html. `{r2 | core | verified}` — The defining vendor documentation of the signals-and-slots inter-object communication mechanism (type-safe, loosely coupled callback replacement); page loaded live.
   - elements: signals-and-slots
60. **ReactiveX documentation: Introduction / Observable** — ReactiveX contributors, living. reactivex.io. https://reactivex.io/intro.html. `{r2 | core | verified}` — The project's own definition of observable sequences / observable streams for composing asynchronous event-based programs; page loaded live.
   - elements: observable-streams
61. **RFC 896: Congestion Control in IP/TCP Internetworks** — John Nagle, 1984. IETF. https://datatracker.ietf.org/doc/html/rfc896. `{r2 | core | verified}` — The primary standard describing small-packet coalescing (inhibit new segments while unacked data is outstanding) - later known as Nagle's algorithm; RFC loaded live.
   - elements: nagle-s-algorithm
62. **TCP/IP Illustrated, Volume 1: The Protocols** — W. Richard Stevens, 1994. Addison-Wesley Professional. ISBN 0-201-63346-9. `{r2 | core | verified}` — The canonical protocol-mechanics text: teaches sliding-window flow control and Nagle's algorithm with live traces; InformIT publisher page loaded live confirming ISBN (pub. 1993, copyright 1994).
   - elements: nagle-s-algorithm, sliding-window-flow-control
63. **The Tail at Scale** — Jeffrey Dean, Luiz Andre Barroso, 2013. Communications of the ACM 56(2), 74-80. DOI 10.1145/2408776.2408794. `{r2 | core | verified}` — The canon paper naming hedged requests (send a duplicate request after a delay, take the first reply) among tail-latency-tolerant techniques; dblp record loaded live.
   - elements: hedged-request

### Membership (existing works, reclaimed under the element lens)

64. **[MEMBERSHIP id=ganssle]** `{r2 | core | verified}` — Ganssle's 'Bit Banging' article (Embedded Systems Programming, Dec 1991; ganssle.com/articles/auart.htm, loaded live) teaches software-implemented UART serial I/O on GPIO pins - the catalog-grade upgrade over the Wikipedia-only naming; claimed under the corpus's existing Ganssle-materials entry.
   - elements: bit-banging
65. **[MEMBERSHIP id=labrosse]** `{r2 | core | verified}` — Defines and teaches RTOS message mailboxes and message queues as kernel IPC objects (uC/OS-II mailboxes; uC/OS-III message queues). (also serves r3)
   - elements: fixed-point-arithmetic, mailbox, message-queue, software-timer

## R3. Embedded, scheduling & numeric

### New

66. **AUTOSAR Classic Platform — Specification of Operating System (SWS OS)** — AUTOSAR consortium, living. autosar.org. `{r3 | anchor | unverified}` — The AUTOSAR OS specification defines schedule tables (statically configured expiry-point tables driving OSEK/AUTOSAR task activation) — the defining document for the element. **UNRESOLVED:** live page — autosar.org failed TLS verification this session; current release identifier not confirmed.
   - elements: schedule-table
67. **Scheduling Multithreaded Computations by Work Stealing** — Robert D. Blumofe, Charles E. Leiserson, 1999. Journal of the ACM 46(5), pp. 720-748. DOI 10.1145/324133.324234. `{r3 | anchor | verified}` — The canonical work-stealing scheduler paper (Cilk lineage; basis of Java ForkJoinPool, TBB, Rayon). Verified via dblp record (ACM DL blocked this session).
   - elements: work-stealing
68. **Comparing Floating Point Numbers, 2012 Edition** — Bruce Dawson, 2012. Random ASCII (randomascii.wordpress.com). https://randomascii.wordpress.com/2012/02/25/comparing-floating-point-numbers-2012-edition/. `{r3 | anchor | verified}` — The de facto canonical practitioner treatment of epsilon vs relative-epsilon vs ULP float comparison, including the near-zero failure modes.
   - elements: epsilon-ulp-float-comparison
69. **A Guide to Debouncing** — Jack Ganssle, 2004. ganssle.com (rev. 2006-2014). https://www.ganssle.com/debouncing.htm. `{r3 | anchor | verified}` — The empirical classic on switch bounce (measured bounce data for 18 switches) plus hardware and software debounce algorithms. Loaded live on the author's site.
   - elements: debouncing
70. **Meeting Real-Time Constraints Using 'Sandwich Delays'** — Michael J. Pont, Susan Kurian, Ricardo Bautista-Quintero, 2009. Transactions on Pattern Languages of Programming I, LNCS 5770, Springer, pp. 94-102 (orig. EuroPLoP 2006). DOI 10.1007/978-3-642-10832-7_4. `{r3 | anchor | verified}` — The naming paper for the Sandwich Delay pattern (fixed-duration code sections to kill jitter in time-triggered systems). Springer chapter page loaded live.
   - elements: sandwich-delay
71. **RFC 1982: Serial Number Arithmetic** — Robert Elz, Randy Bush, 1996. IETF (Standards Track). RFC 1982. `{r3 | anchor | verified}` — Defines wrap-around serial number comparison for 32-bit counters (DNS SOA serials; the pattern behind sequence-number comparison in protocols and embedded counters). Loaded live at rfc-editor.org.
   - elements: serial-number-arithmetic
72. **The Art of Computer Programming, Volume 2: Seminumerical Algorithms, 3rd ed.** — Donald E. Knuth, 1997. Addison-Wesley. ISBN 0-201-89684-2. `{r3 | anchor | verified}` — Ch. 3 (Random Numbers) and sec. 4.3 (Multiple-Precision Arithmetic) are the canonical treatments of PRNGs and arbitrary-precision arithmetic. Verified on Knuth's Stanford TAOCP page.
   - elements: arbitrary-precision-arithmetic, pseudorandom-number-generator
73. **Hashed and Hierarchical Timing Wheels: Data Structures for the Efficient Implementation of a Timer Facility** — George Varghese, Anthony (Tony) Lauck, 1987. SOSP '87, Proceedings of the 11th ACM Symposium on Operating Systems Principles, pp. 25-38. DOI 10.1145/41457.37504. `{r3 | anchor | verified}` — The naming paper for hashed/hierarchical timer wheels — O(1) start/stop/tick timer facilities; still the canonical reference for kernel and RTOS timer implementations. Verified via dblp record (dl.acm.org blocked this session).
   - elements: timer-wheel
74. **PID Without a PhD** — Tim Wescott, 2000. Embedded Systems Programming, October 2000; maintained at wescottdesign.com. http://www.wescottdesign.com/articles/Sampling/pidwophd.html. `{r3 | anchor | verified}` — The embedded-practitioner classic on implementing and tuning software PID controllers in C without formal control theory. Loaded live on the author's site.
   - elements: pid-controller
75. **Feedback Systems: An Introduction for Scientists and Engineers, 2nd ed.** — Karl Johan Åström, Richard M. Murray, living. Princeton University Press; full text maintained at fbswiki.org. https://fbswiki.org. `{r3 | advanced | verified}` — The modern rigorous treatment of feedback control including a dedicated PID Control chapter; the freely maintained online edition is the current canonical text. Verified on the official book wiki.
   - elements: pid-controller
76. **ISO/IEC 9899:2024 — Information technology — Programming languages — C (C23)** — ISO/IEC JTC1/SC22/WG14, 2024. ISO/IEC. ISO/IEC 9899:2024. `{r3 | core | verified}` — C23 standardizes checked integer arithmetic via <stdckdint.h> (ckd_add/ckd_sub/ckd_mul). Adoption and identifier confirmed live on the WG14 committee site (open-std.org); iso.org blocked this session.
   - elements: checked-arithmetic
77. **Debouncing and Throttling Explained Through Examples** — David Corbacho, 2016. CSS-Tricks. https://css-tricks.com/debouncing-throttling-explained-examples/. `{r3 | core | verified}` — The standard UI-side treatment distinguishing debounce vs throttle (vs requestAnimationFrame) with interactive examples — anchors the throttle element and the event-side sense of debouncing.
   - elements: debouncing, throttle
78. **Fix Your Timestep!** — Glenn Fiedler, 2004. Gaffer On Games. https://gafferongames.com/post/fix_your_timestep/. `{r3 | core | verified}` — The naming article for the fixed-timestep game/physics loop with accumulator and render interpolation; still the standard citation.
   - elements: fixed-timestep
79. **What Every Computer Scientist Should Know About Floating-Point Arithmetic** — David Goldberg, 1991. ACM Computing Surveys 23(1), March 1991. https://docs.oracle.com/cd/E19957-01/806-3568/ncg_goldberg.html. `{r3 | core | verified}` — The canonical floating-point survey: 'Relative Error and Ulps' section grounds ULP comparison; Theorem 8 states the Kahan Summation Formula. Verified via the authoritative Oracle/Sun reprint (ACM DL blocked this session).
   - elements: epsilon-ulp-float-comparison, kahan-summation
80. **Site Reliability Engineering: How Google Runs Production Systems** — Betsy Beyer, Chris Jones, Jennifer Petoff, Niall Richard Murphy (eds.), 2016. O'Reilly; free online at sre.google. https://sre.google/sre-book/. `{r3 | core | verified}` — Ch. 22 (Addressing Cascading Failures) names and teaches deadline propagation down RPC trees. Chapter loaded live on sre.google. (also serves r8)
   - elements: deadline-propagation, retry-budget, retry-with-exponential-backoff-and-jitter
81. **IEEE 1788-2015 — IEEE Standard for Interval Arithmetic** — IEEE Computer Society, Microprocessor Standards Committee, 2015. IEEE. IEEE 1788-2015. `{r3 | core | verified}` — The standardization of interval arithmetic operations over IEEE 754 formats; confirmed live on standards.ieee.org (status inactive-reserved as of 2026, still the defining document).
   - elements: interval-arithmetic
82. **Eliminating Receive Livelock in an Interrupt-driven Kernel** — Jeffrey C. Mogul, K. K. Ramakrishnan, 1996. USENIX Annual Technical Conference 1996, pp. 99-112 (extended in ACM TOCS 15(3), 1997). https://research.google/pubs/eliminating-receive-livelock-in-an-interrupt-driven-kernel/. `{r3 | core | verified}` — The canonical paper motivating interrupt mitigation/coalescing and hybrid interrupt-polling (NAPI lineage) — upgrades interrupt coalescing beyond its Wikipedia naming. Verified via research.google publication page.
   - elements: interrupt-coalescing
83. **Interval Analysis** — Ramon E. Moore, 1966. Prentice-Hall. `{r3 | advanced | unverified}` — The founding monograph that named interval arithmetic/analysis; included as the naming source alongside the IEEE 1788 standard. **UNRESOLVED:** primary page not loadable this session; no ISBN cited.
   - elements: interval-arithmetic
84. **RFC 791: Internet Protocol** — Jon Postel (ed.), 1981. IETF/DARPA. RFC 791. `{r3 | core | verified}` — Defines the Time to Live field — the naming source for TTL as a lifetime-bounding mechanism. Loaded live at rfc-editor.org. (also serves r9)
   - elements: network-byte-order-handling, time-to-live-ttl
85. **Computer Networks, 6th ed.** — Andrew S. Tanenbaum, Nick Feamster, David J. Wetherall, 2021. Pearson. ISBN 9780137523214. `{r3 | core | verified}` — The standard networking text: traffic shaping with leaky bucket and token bucket, and TTL/hop-limit semantics — the modern catalog-grade treatment for all three. Pearson catalog page loaded live. (r9 cited the 5th ed.; node carries the current 6th.) (also serves r9)
   - elements: bit-stuffing, byte-stuffing, leaky-bucket, length-prefix-framing, sync-word, time-to-live-ttl, token-bucket

### Membership (existing works, reclaimed under the element lens)

86. **[MEMBERSHIP id=pont]** `{r3 | anchor | verified}` — Names Super Loop and the time-triggered co-operative scheduler pattern language; cyclic-executive style schedulers throughout. (also serves r4, r8)
   - elements: cyclic-executive, loop-timeout, multi-state-task, super-loop, time-triggered-co-operative-scheduler
87. **[MEMBERSHIP id=sakscolumns]** `{r3 | anchor | verified}` — The canonical column series on memory-mapped register access idioms in C/C++ (volatile, placement, structs over registers).
   - elements: memory-mapped-register-access
88. **[MEMBERSHIP id=barrc]** `{r3 | core | verified}` — Codifies ISR coding rules (naming, volatile discipline, keep-short constraints) — the coding-standard-grade treatment of the ISR element.
   - elements: interrupt-service-routine
89. **[MEMBERSHIP id=buttazzo]** `{r3 | core | verified}` — The real-time scheduling theory text: cyclic executives, fixed-priority (RM) and dynamic-priority (EDF) scheduling, round robin, scheduler design.
   - elements: cyclic-executive, dynamic-priority-scheduling, round-robin-scheduling, scheduler, static-priority-scheduling
90. **[MEMBERSHIP id=gustedt]** `{r3 | core | verified}` — The C23-era teaching text for checked integer arithmetic (<stdckdint.h> ckd_add/ckd_sub/ckd_mul) alongside the standard itself.
   - elements: checked-arithmetic
91. **[MEMBERSHIP id=kensmith]** `{r3 | core | verified}` — Naming source for typesafe register access via C++ templates; also a substantive treatment of memory-mapped access tradeoffs.
   - elements: memory-mapped-register-access, typesafe-register-access-via-c-templates
92. **[MEMBERSHIP id=liulayland]** `{r3 | core | verified}` — The founding paper: rate-monotonic (static priority) and EDF (dynamic priority) scheduling with utilization bounds.
   - elements: dynamic-priority-scheduling, static-priority-scheduling
93. **[MEMBERSHIP id=memfaultea]** `{r3 | core | verified}` — Device Firmware Update Cookbook is the naming source and practical treatment of A/B firmware image update slots.
   - elements: a-b-firmware-image-update
94. **[MEMBERSHIP id=tr18015]** `{r3 | core | verified}` — The hardware-interface chapter defines the iohw.h standard hardware I/O interface — the naming source itself.
   - elements: iohw-h-standard-hardware-i-o-interface
95. **[MEMBERSHIP id=yiu]** `{r3 | core | verified}` — Definitive treatment of the vector table/NVIC and of Cortex-M saturating (QADD/SSAT) arithmetic — upgrades saturation arithmetic beyond its Wikipedia naming. (also serves r4)
   - elements: interrupt-vector-table, nested-interrupt-handling, saturation-arithmetic
96. **[MEMBERSHIP id=zerotomain]** `{r3 | core | verified}` — 'How to Write a Bootloader from Scratch' names and walks the bootloader jump/handoff mechanism (vector relocation, stack swap, jump to app).
   - elements: bootloader-jump-handoff

## R4. Execution & concurrency

### New

97. **Crafting Interpreters** — Robert Nystrom, 2021. self-published (craftinginterpreters.com); print via Genever Benning. ISBN 9780990582939. `{r4 | anchor | verified}` — Part III builds a complete bytecode virtual machine (clox) — the catalog-grade teaching text that names the element; official site loaded live (ISBN confirmed). (also serves r9)
   - elements: abstract-syntax-tree, bytecode-virtual-machine, lexer, panic-mode-error-recovery, pratt-parser, read-eval-print-loop, recursive-descent-parser, tree-walking-interpreter
98. **Java Concurrency in Practice** — Goetz, Peierls, Bloch, Bowbeer, Holmes, Lea, 2006. Addison-Wesley Professional. ISBN 978-0-321-34960-6. `{r4 | anchor | verified}` — Canonical teaching text for task-execution mechanisms: the Executor framework (ch.6), applying thread pools (ch.8), and Future-based result handling; names Executor and Thread Pool for the catalog. Verified via InformIT publisher page. (also serves r5)
   - elements: condition-variable, double-checked-locking, executor, future-promise, latch, lock-striping, reentrant-lock, safe-publication, thread-confinement, thread-pool
99. **Patterns for Parallel Programming** — Mattson, Sanders, Massingill, 2004. Addison-Wesley Professional. ISBN 978-0-321-22811-6. `{r4 | anchor | verified}` — The parallel pattern language that names five route elements outright — SPMD, Loop Parallelism, Fork/Join, Master/Worker, Pipeline (ch.5 Supporting Structures; TOC confirmed on InformIT publisher page).
   - elements: fork-join, loop-parallelism, master-slave, pipeline-parallelism, spmd
100. **Is Parallel Programming Hard, And, If So, What Can You Do About It?** — Paul E. McKenney (ed.), living. kernel.org (freely published; continuously revised). https://www.kernel.org/pub/linux/kernel/people/paulmck/perfbook/perfbook.html. `{r4 | anchor | verified}` — The kernel-school concurrency book: parallel fastpath designs (McKenney's own PLoPD2 lineage), per-thread/per-CPU data ownership, and cache-line/false-sharing effects — modern treatment for three route elements. Official kernel.org page loaded live. (also serves r5)
   - elements: acquire-release-ordering, false-sharing-avoidance-via-cache-line-padding, fast-path, memory-barrier, read-copy-update, sequence-lock, spinlock, thread-specific-storage
101. **Threaded Code** — James R. Bell, 1973. Communications of the ACM 16(6). `{r4 | core | unverified}` — The CACM note that named threaded code; canon for interpreter dispatch technique naming. **UNRESOLVED:** doi/pages — ACM DL Cloudflare-blocked this session; citation cross-checked only via Ertl's academic threaded-code bibliography (bell73, CACM, received June).
   - elements: threaded-code
102. **Design of a Separable Transition-Diagram Compiler** — Melvin E. Conway, 1963. Communications of the ACM 6(7), p. 396. http://melconway.com/Home/pdf/compiler.pdf. `{r4 | core | verified}` — The paper that coined 'coroutine'. Verified live on the author's own site: melconway.com/Home/Inventor.html cites 'Comm. ACM 6 (July 1963), 396' and hosts the scanned PDF.
   - elements: coroutine
103. **Threaded Code (what is threaded code, direct/indirect threading, dispatch techniques)** — M. Anton Ertl, living. TU Wien (complang.tuwien.ac.at/forth/threaded-code.html). https://www.complang.tuwien.ac.at/forth/threaded-code.html. `{r4 | core | verified}` — The standing modern treatment of threaded-code dispatch (direct/indirect/token threading, computed goto) by the field's principal researcher; loaded live.
   - elements: threaded-code
104. **Trampolined Style** — Ganz, Friedman, Wand, 1999. ICFP '99, Paris, pp. 18-27. `{r4 | core | verified}` — Names trampolined style: a single scheduler loop stepping suspended computations — the canon for the trampoline element. Full citation + abstract confirmed live on Mitchell Wand's own bibliography page (ccs.neu.edu).
   - elements: trampoline
105. **Patterns in Java, Volume 1: A Catalog of Reusable Design Patterns Illustrated with UML** — Mark Grand, 1998. Wiley. ISBN 0-471-25839-3. `{r4 | core | verified}` — Names the Balking and Guarded Suspension concurrency patterns (7-pattern concurrency chapter). Wiley legacy catalog page loaded live (title, author, ISBN, 1998). **UNRESOLVED:** isbn — Wiley product page is client-rendered and exposed no bibliographic payload this session; 1st-ed ISBN not confirmed on a primary page. (also serves r5)
   - elements: balking, guarded-suspension, two-phase-termination
106. **A Universal Modular ACTOR Formalism for Artificial Intelligence** — Hewitt, Bishop, Steiger, 1973. IJCAI-73 proceedings. https://www.ijcai.org/Proceedings/1973. `{r4 | advanced | verified}` — Origin of the actor model, folded into active-object as aka support (actors = active entities with mailboxes). Title confirmed live in the official IJCAI 1973 proceedings listing.
   - elements: active-object
107. **Debugging Optimized Code with Dynamic Deoptimization** — Hölzle, Chambers, Ungar, 1992. ACM SIGPLAN PLDI '92, pp. 32-43 (SIGPLAN Notices 27(7)). `{r4 | core | verified}` — The paper that introduced dynamic deoptimization (in the Self VM) — the naming source and still the definitive mechanism description. Verified live via the official Self project bibliography (bibliography.selflanguage.org) incl. full citation.
   - elements: deoptimization
108. **HotSpot Glossary of Terms** — OpenJDK HotSpot group, living. openjdk.org. https://openjdk.org/groups/hotspot/docs/HotSpotGlossary.html. `{r4 | core | verified}` — Authoritative living definition of deoptimization in the production VM that mainstreamed it (uncommon traps, nmethod invalidation); definition quoted live this session. (also serves r5)
   - elements: deoptimization, safepoint
109. **JEP 444: Virtual Threads** — OpenJDK (Pressler, Bateman), 2023. openjdk.org (delivered in JDK 21). https://openjdk.org/jeps/444. `{r4 | core | verified}` — Authoritative modern treatment of user-mode (green) threads: explicitly contrasts historical M:1 green threads, 1:1 platform threads, and M:N virtual threads — upgrades the element from its bare-Wikipedia naming. Loaded live (title + green-threads discussion confirmed).
   - elements: green-threads
110. **Concurrent Programming in Java: Design Principles and Patterns, 2nd ed.** — Doug Lea, 1999. Addison-Wesley. ISBN 0-201-31009-0. `{r4 | advanced | verified}` — The pre-java.util.concurrent pattern catalog: worker threads (4.1.4), futures (4.3.3), fork/join parallel decomposition (4.4.1) — the design-pattern-level treatment behind JCiP's APIs. Verified via Lea's own supplement page (gee.cs.oswego.edu/dl/cpj).
   - elements: fork-join, future-promise, thread-pool
111. **Promises: Linguistic Support for Efficient Asynchronous Procedure Calls in Distributed Systems** — Liskov, Shrira, 1988. ACM SIGPLAN PLDI '88. `{r4 | advanced | unverified}` — Canonical naming paper for promises/futures as first-class results of asynchronous calls; kept despite failed live check because it is the element's naming canon. **UNRESOLVED:** doi/pages — ACM DL Cloudflare-blocked and PMG CSAIL unreachable this session; identifier not confirmed against a primary page.
   - elements: future-promise
112. **Restartable sequences** — Jonathan Corbet, 2015. LWN.net. https://lwn.net/Articles/650333/. `{r4 | core | verified}` — The naming article for restartable sequences (per-CPU critical sections with kernel-assisted restart, later the rseq(2) syscall); title/author/date 2015-07-07 confirmed live.
   - elements: restartable-sequences
113. **Structured Parallel Programming: Patterns for Efficient Computation** — McCool, Robison, Reinders, 2012. Morgan Kaufmann (Elsevier). ISBN 978-0-12-415993-8. `{r4 | core | verified}` — Modern deterministic-pattern treatment: map (loop parallelism), collectives/reduction (ch.5), stencil (ch.7), pipeline (ch.9) — the best current teaching of the data-parallel kernel shapes. Verified via Elsevier shop page with TOC.
   - elements: loop-parallelism, parallel-reduction, pipeline-parallelism, stencil
114. **Cancellation in Managed Threads** — Microsoft (.NET documentation), living. Microsoft Learn. https://learn.microsoft.com/en-us/dotnet/standard/threading/cancellation-in-managed-threads. `{r4 | core | verified}` — The authoritative treatment of the cancellation-token mechanism: CancellationTokenSource/CancellationToken, cooperative polling/callback/wait-handle listening, linked tokens. Loaded live in full.
   - elements: cancellation-token
115. **The Node.js Event Loop (Event Loop, Timers, and process.nextTick)** — Node.js project (OpenJS Foundation), living. nodejs.org Learn docs. https://nodejs.org/en/learn/asynchronous-work/event-loop-timers-and-nexttick. `{r4 | core | verified}` — Catalog-grade official teaching of the event-loop mechanism (phases: timers, poll, check, close; microtask queue) — upgrades the element from its bare-Wikipedia naming. Loaded live.
   - elements: event-loop
116. **Revisiting Coroutines** — de Moura, Ierusalimschy, 2009. ACM TOPLAS 31(2), pp. 6.1-6.31. DOI 10.1145/1462166.1462167. `{r4 | survey | verified}` — The modern canonical survey/formalization of coroutines (full asymmetric coroutines, expressiveness vs one-shot continuations) — the best current treatment pairing Conway's 1963 naming. Citation incl. DOI confirmed live on Ierusalimschy's publications page.
   - elements: coroutine
117. **The F# Asynchronous Programming Model** — Syme, Petricek, Lomov, 2011. PADL 2011, Springer LNCS 6539. DOI 10.1007/978-3-642-18378-2_15. `{r4 | core | verified}` — The paper behind async/await: F# async workflows, the direct ancestor of C# await and the JS/Python/Rust async models; Springer chapter page loaded live confirming title and DOI.
   - elements: async-await-model
118. **Notes on structured concurrency, or: Go statement considered harmful** — Nathaniel J. Smith, 2018. vorpus.org (Trio project). https://vorpus.org/blog/notes-on-structured-concurrency-or-go-statement-considered-harmful/. `{r4 | core | verified}` — The essay that named and argued structured concurrency (nurseries); the acknowledged source behind Trio, Kotlin coroutine scopes, and JEP 453 (the latter kept as aka support only). Loaded live: title/author/date 2018-04-25 confirmed.
   - elements: structured-concurrency

### Membership (existing works, reclaimed under the element lens)

119. **[MEMBERSHIP id=dreppermem]** `{r4 | core | verified}` — Names false sharing and teaches the cache-line-padding/alignment countermeasure with measurements — the naming source for the element. (also serves r5)
   - elements: compare-and-swap-loop, false-sharing-avoidance-via-cache-line-padding, memory-barrier
120. **[MEMBERSHIP id=protothreads]** `{r4 | core | verified}` — Naming paper and complete treatment of the protothread mechanism (stackless threads over local continuations in C).
   - elements: protothread
121. **[MEMBERSHIP id=samekcourse]** `{r4 | core | verified}` — The course's later segments teach the Active Object model (event queue + private state + run-to-completion) as the central embedded concurrency discipline, with QP as the running realization.
   - elements: active-object

## R5. Synchronization & lock-free

### New

122. **The Art of Multiprocessor Programming, 2nd ed.** — Maurice Herlihy, Nir Shavit, Victor Luchangco, Michael Spear, 2020. Morgan Kaufmann / Elsevier. ISBN 978-0-12-415950-1. `{r5 | anchor | verified}` — The theory anchor of shared-memory synchronization (1st ed. 2008): spin locks and TTAS, queue locks incl. MCS, monitors/condition variables, semaphores, readers-writers, stamped (tagged) references for ABA, CAS retry loops, STM. Publisher page loaded live (Elsevier, 2nd ed. 2020). (also serves r6)
   - elements: aba-mitigation-via-tagged-pointer, compare-and-swap-loop, condition-variable, lock-free-fifo-queue-michael-scott, lock-free-stack-treiber, mcs-queue-lock, monitor-object, readers-writer-lock, semaphore, skip-list, software-transactional-memory, spinlock, test-and-test-and-set-lock
123. **Designing Data-Intensive Applications** — Martin Kleppmann, 2017. O'Reilly. ISBN 978-1-4493-7332-0. `{r5 | anchor | verified}` — Best modern treatment of the database/distributed synchronization elements: names fencing tokens; teaches snapshot isolation, MVCC, two-phase locking, and Lamport timestamps. Official site (dataintensive.net) loaded live incl. ISBN. (also serves r6, r9)
   - elements: b-tree, bitmap-index, consistent-hashing, fencing-token, log-structured-storage, logical-clock, lsm-tree, multiversion-concurrency-control, schema-evolution-via-field-tags, secondary-index, snapshot-isolation, tombstone, two-phase-locking, write-ahead-log
124. **Concurrency Control in Distributed Database Systems** — Philip A. Bernstein, Nathan Goodman, 1981. ACM Computing Surveys 13(2). DOI 10.1145/356842.356846. `{r5 | survey | verified}` — The classic survey framing two-phase locking and timestamp-ordering concurrency control, including distributed deadlock detection. Crossref DOI metadata confirmed live.
   - elements: deadlock-detection, timestamp-ordering-concurrency-control, two-phase-locking
125. **Futexes Are Tricky** — Ulrich Drepper, 2011. Red Hat / akkadia.org. https://www.akkadia.org/drepper/futex.pdf. `{r5 | advanced | verified}` — The canonical user-level treatment of futex-based synchronization construction. Primary PDF loaded live (title page: Nov 5, 2011).
   - elements: futex
126. **Concurrency Control in Groupware Systems** — C. A. Ellis, S. J. Gibbs, 1989. ACM SIGMOD '89, 399-407. DOI 10.1145/67544.66963. `{r5 | core | verified}` — Names operational transformation (dOPT) for collaborative editing; the canonical OT source. Crossref DOI metadata confirmed live.
   - elements: operational-transformation
127. **Flat Combining and the Synchronization-Parallelism Tradeoff** — Danny Hendler, Itai Incze, Nir Shavit, Moran Tzafrir, 2010. SPAA '10 (22nd ACM Symposium on Parallelism in Algorithms and Architectures). DOI 10.1145/1810479.1810540. `{r5 | advanced | verified}` — Names flat combining; sole catalog-grade source for the element. Crossref DOI metadata and Shavit's MIT publications page both loaded live.
   - elements: flat-combining
128. **Transaction Processing: Concepts and Techniques** — Jim Gray, Andreas Reuter, 1992. Morgan Kaufmann / Elsevier. ISBN 978-1-55860-190-1. `{r5 | core | verified}` — The catalog-grade treatment of database lock engineering: two-phase locking, multi-granularity locking, lock escalation, deadlock detection, optimistic schemes. Elsevier product page loaded live. (also serves r6)
   - elements: checkpointing, deadlock-detection, group-commit, lock-escalation, multi-granularity-locking, optimistic-concurrency-control, shadow-paging, two-phase-locking, write-ahead-log
129. **Monitors: An Operating System Structuring Concept** — C. A. R. Hoare, 1974. Communications of the ACM 17(10). DOI 10.1145/355620.361161. `{r5 | core | verified}` — Names the monitor and its condition variables (wait/signal). Crossref DOI metadata confirmed live.
   - elements: condition-variable, monitor-object
130. **Linux kernel locking, RCU and memory-barrier documentation** — Linux kernel community (David Howells, Paul E. McKenney, Will Deacon, Peter Zijlstra et al.), living. kernel.org (Documentation/locking, Documentation/RCU, memory-barriers.txt). https://www.kernel.org/doc/html/latest/locking/. `{r5 | core | verified}` — Official living documentation naming/teaching seqlocks, spinlock discipline, PI-futexes and rt-mutex priority inheritance, RCU (whatisRCU), and the memory-barriers.txt taxonomy of barrier kinds. locking/ index, memory-barriers.txt, and RCU/whatisRCU all loaded live.
   - elements: futex, memory-barrier, priority-inheritance-protocol, read-copy-update, sequence-lock, spinlock
131. **The Linux Programming Interface** — Michael Kerrisk, 2010. No Starch Press. ISBN 978-1-59327-220-3. `{r5 | core | verified}` — Names the self-pipe trick (sec. 63.5.2) and teaches POSIX-level condition variables and semaphores. Author's official page (man7.org/tlpi) loaded live.
   - elements: condition-variable, self-pipe-trick, semaphore
132. **On Optimistic Methods for Concurrency Control** — H. T. Kung, John T. Robinson, 1981. ACM Transactions on Database Systems 6(2). DOI 10.1145/319566.319567. `{r5 | core | verified}` — Names optimistic concurrency control (read/validate/write phases). ACM DL page title confirmed live.
   - elements: optimistic-concurrency-control
133. **Time, Clocks, and the Ordering of Events in a Distributed System** — Leslie Lamport, 1978. Communications of the ACM 21(7), 558-565. https://lamport.azurewebsites.net/pubs/pubs.html. `{r5 | core | verified}` — Names logical clocks and the happened-before ordering. Author's official publications page loaded live confirming venue/year.
   - elements: logical-clock
134. **Algorithms for Scalable Synchronization on Shared-Memory Multiprocessors** — John M. Mellor-Crummey, Michael L. Scott, 1991. ACM Transactions on Computer Systems 9(1). DOI 10.1145/103727.103729. `{r5 | core | verified}` — Names the MCS queue lock and is the canonical comparative treatment of spinning: test-and-test-and-set, ticket locks, queue locks. Crossref DOI metadata confirmed live.
   - elements: mcs-queue-lock, spinlock, test-and-test-and-set-lock, ticket-lock
135. **Preshing on Programming (lock-free and memory-ordering series)** — Jeff Preshing, living. preshing.com. https://preshing.com/20120913/acquire-and-release-semantics/. `{r5 | core | verified}` — Names acquire-release ordering as a programmer-facing concept (2012 post loaded live) and gives the standard accessible treatments of memory barriers and C++11 double-checked locking.
   - elements: acquire-release-ordering, double-checked-locking, memory-barrier
136. **Synchronization with Eventcounts and Sequencers** — David P. Reed, Rajendra K. Kanodia, 1979. Communications of the ACM 22(2). DOI 10.1145/359060.359076. `{r5 | advanced | verified}` — Names the eventcount (and sequencer) primitive; still the canonical source, echoed in modern lock-free queue designs. Crossref DOI metadata confirmed live.
   - elements: eventcount
137. **Priority Inheritance Protocols: An Approach to Real-Time Synchronization** — Lui Sha, Ragunathan Rajkumar, John P. Lehoczky, 1990. IEEE Transactions on Computers 39(9). DOI 10.1109/12.57058. `{r5 | core | verified}` — Names both the priority inheritance and priority ceiling protocols, with the schedulability analysis. Crossref DOI metadata confirmed live.
   - elements: priority-ceiling-protocol, priority-inheritance-protocol
138. **Software Transactional Memory** — Nir Shavit, Dan Touitou, 1995. PODC '95 (14th ACM Symposium on Principles of Distributed Computing). DOI 10.1145/224964.224987. `{r5 | advanced | verified}` — Names software transactional memory (Dijkstra Prize 2012); AMP ch. 18 is the textbook companion. Crossref DOI metadata confirmed live.
   - elements: software-transactional-memory

### Membership (existing works, reclaimed under the element lens)

139. **[MEMBERSHIP id=dsimonprimer]** `{r5 | core | verified}` — Names interrupt-masking critical sections and teaches semaphore discipline in the RTOS/interrupt context (shared-data problem).
   - elements: interrupt-masking-critical-section, semaphore

## R6. Data structures, persistence & caching

### New

140. **Introduction to Algorithms, 4th ed.** — Cormen, Leiserson, Rivest & Stein, 2022. MIT Press. ISBN 9780262046305. `{r6 | anchor | verified}` — The reference treatment for the container/algorithm floor of this route: elementary structures, hash tables, BSTs, heaps, B-trees, union-find, augmented/interval trees, amortized table doubling; 4th ed adds suffix-array material. (also serves r7)
   - elements: adjacency-list-adjacency-matrix, b-tree, binary-heap-priority-queue, binary-search-tree, disjoint-set-union-find, dynamic-array, hash-table, interval-tree, linked-list, queue-fifo, stack, suffix-array
141. **Caching Data Sources (Oracle Coherence Developing Applications guide)** — Oracle, living. docs.oracle.com, Coherence 14.1.1. https://docs.oracle.com/en/middleware/standalone/coherence/14.1.1.2206/develop-applications/caching-data-sources.html. `{r6 | anchor | verified}` — The living naming source that defines the read-through / write-through / write-behind / refresh-ahead family; definitions confirmed live.
   - elements: read-through-cache, refresh-ahead-cache, write-behind-cache, write-through-cache
142. **Real-Time Collision Detection** — Christer Ericson, 2005. Morgan Kaufmann; official site realtimecollisiondetection.net. https://realtimecollisiondetection.net/. `{r6 | anchor | verified}` — One treatment covering the spatial cluster: BVHs, uniform grids and spatial hashing, quadtrees/octrees, k-d/BSP trees — the route entry point for spatial partitioning.
   - elements: bounding-volume-hierarchy, k-d-tree, quadtree-octree, spatial-partition, uniform-spatial-hash-grid
143. **Introduction to Information Retrieval** — Manning, Raghavan & Schütze, 2008. Cambridge University Press; full text at nlp.stanford.edu/IR-book. https://nlp.stanford.edu/IR-book/. `{r6 | anchor | verified}` — The IR canon: inverted index construction (chs. 1-4) and shingling/MinHash near-duplicate detection (ch. 19); official Stanford site confirmed live.
   - elements: inverted-index, minhash
144. **Database Internals: A Deep-Dive into How Distributed Data Systems Work** — Alex Petrov, 2019. O'Reilly. ISBN 9781492040347. `{r6 | anchor | verified}` — Storage-engine half teaches buffer pool/page cache and eviction (incl. LRU variants), B-trees and copy-on-write B-trees, WAL/recovery, LSM trees with memtable skip lists and Bloom filters — the named source for cache-eviction-policy. (also serves r7)
   - elements: b-tree, bloom-filter, buffer-pool, cache-eviction-policy, copy-on-write-b-tree, lru-cache, lsm-tree, skip-list, slotted-page-layout, write-ahead-log
145. **AN2594: EEPROM emulation in STM32F10x microcontrollers** — STMicroelectronics, living. st.com application note. `{r6 | core | unverified}` — The vendor app note that names the EEPROM-emulation-in-flash technique (paged flash + wear distribution) for MCUs. **UNRESOLVED:** url (st.com fetch timed out this session).
   - elements: eeprom-emulation-in-flash
146. **Cloud Design Patterns: Cache-Aside** — Microsoft (Azure Architecture Center), living. learn.microsoft.com. https://learn.microsoft.com/en-us/azure/architecture/patterns/cache-aside. `{r6 | core | verified}` — The maintained catalog entry that names Cache-Aside and specifies its read-miss-populate / write-invalidate contract.
   - elements: cache-aside
147. **Ideal Hash Trees** — Phil Bagwell, 2001. EPFL (LAMP) technical report. https://lampwww.epfl.ch/papers/idealhashtrees.pdf. `{r6 | core | verified}` — Naming paper for the hash array mapped trie; first page loaded live from the EPFL LAMP host. **UNRESOLVED:** year (commonly cited as 2001; not shown on the EPFL copy's first page).
   - elements: hash-array-mapped-trie-hamt
148. **Space/Time Trade-offs in Hash Coding with Allowable Errors** — Burton H. Bloom, 1970. CACM 13(7). `{r6 | core | unverified}` — The canon naming paper for the Bloom filter; kept alongside Petrov's storage-engine treatment. **UNRESOLVED:** doi.
   - elements: bloom-filter
149. **Ropes: an Alternative to Strings** — Boehm, Atkinson & Plass, 1995. Software: Practice and Experience 25(12). `{r6 | core | unverified}` — Naming paper for the rope structure; Wiley page blocked live this session. **UNRESOLVED:** doi.
   - elements: rope
150. **An Efficient Representation for Sparse Sets** — Preston Briggs & Linda Torczon, 1993. ACM LOPLAS 2(1-4). `{r6 | advanced | unverified}` — Naming paper for the sparse-set representation (dense/sparse array pair), the basis of modern ECS storage. **UNRESOLVED:** doi.
   - elements: sparse-set
151. **A Survey of Flash Translation Layer** — Chung, Park, Park, Lee, Lee & Song, 2009. Journal of Systems Architecture 55(5-6). `{r6 | survey | unverified}` — Survey treatment of FTL mapping schemes and wear-leveling policies; the catalog-grade umbrella for both flash elements. **UNRESOLVED:** doi.
   - elements: flash-translation-layer, flash-wear-leveling
152. **An Improved Data Stream Summary: The Count-Min Sketch and its Applications** — Graham Cormode & S. Muthukrishnan, 2005. Journal of Algorithms 55(1). http://dimacs.rutgers.edu/~graham/pubs/papers/cm-full.pdf. `{r6 | core | verified}` — Naming paper for the count-min sketch; first page loaded live from Cormode's DIMACS copy.
   - elements: count-min-sketch
153. **Computational Geometry: Algorithms and Applications, 3rd ed.** — de Berg, Cheong, van Kreveld & Overmars, 2008. Springer. `{r6 | core | unverified}` — The textbook treatment of geometric range structures: kd-trees, interval trees, segment trees; Springer page unreachable (cookie wall) this session. **UNRESOLVED:** isbn.
   - elements: interval-tree, k-d-tree, segment-tree
154. **Efficient Implementation of the Smalltalk-80 System** — L. Peter Deutsch & Allan M. Schiffman, 1984. ACM POPL 1984. `{r6 | advanced | unverified}` — Naming paper for inline caching in dynamic-language runtimes; no treatment in the work-set covers it. **UNRESOLVED:** doi.
   - elements: inline-caching
155. **A New Data Structure for Cumulative Frequency Tables** — Peter M. Fenwick, 1994. Software: Practice and Experience 24(3). `{r6 | advanced | unverified}` — Naming paper for the Fenwick (binary indexed) tree; Wiley page blocked live this session. **UNRESOLVED:** doi.
   - elements: fenwick-tree
156. **The Craft of Text Editing: Emacs for the Modern World** — Craig A. Finseth, 1991. Springer; full text at finseth.com/craft. https://www.finseth.com/craft/. `{r6 | core | verified}` — Ch. 6 (The Internal Sub-Editor) is the catalog treatment of the buffer-gap method and its paged variant; confirmed live on the author's site.
   - elements: gap-buffer
157. **HyperLogLog: the analysis of a near-optimal cardinality estimation algorithm** — Flajolet, Fusy, Gandouet & Meunier, 2007. DMTCS Proceedings AH (AofA 2007). doi:10.46298/dmtcs.3545. `{r6 | core | verified}` — Naming paper and only catalog-grade source for HyperLogLog; confirmed live on the DMTCS episciences page.
   - elements: hyperloglog
158. **R-Trees: A Dynamic Index Structure for Spatial Searching** — Antonin Guttman, 1984. ACM SIGMOD 1984. `{r6 | core | unverified}` — Naming paper and still the standard reference for the R-tree spatial index; no treatment in this route's work-set covers R-trees. **UNRESOLVED:** doi.
   - elements: r-tree
159. **Architecture of a Database System** — Hellerstein, Stonebraker & Hamilton, 2007. Foundations and Trends in Databases 1(2). doi:10.1561/1900000002. `{r6 | survey | verified}` — Survey that names buffer pool as a DBMS component and situates buffer management among the shared components; loaded live from the author's Berkeley copy.
   - elements: buffer-pool
160. **Computer Architecture: A Quantitative Approach, 6th ed.** — John L. Hennessy & David A. Patterson, 2017. Morgan Kaufmann / Elsevier. https://shop.elsevier.com/books/computer-architecture/hennessy/978-0-12-811905-1. `{r6 | core | verified}` — Memory-hierarchy chapters are the canonical treatment of the hardware ends of this route: prefetching, write-through vs write-back policy, and replacement (LRU) as an eviction policy.
   - elements: cache-eviction-policy, lru-cache, prefetching, write-behind-cache, write-through-cache
161. **The Zipper** — Gérard Huet, 1997. Journal of Functional Programming 7(5). doi:10.1017/S0956796897002864. `{r6 | core | verified}` — The functional pearl that names the zipper; confirmed live on Cambridge Core.
   - elements: zipper
162. **Consistent Hashing and Random Trees: Distributed Caching Protocols for Relieving Hot Spots on the World Wide Web** — Karger, Lehman, Leighton, Panigrahy, Levine & Lewin, 1997. ACM STOC 1997. `{r6 | core | unverified}` — Naming paper for consistent hashing; DDIA supplies the modern partitioning treatment. **UNRESOLVED:** doi.
   - elements: consistent-hashing
163. **The Design and Implementation of a Log-Structured File System** — Mendel Rosenblum & John K. Ousterhout, 1992. ACM TOCS 10(1); SOSP 1991. https://web.stanford.edu/~ouster/cgi-bin/papers/lfs.pdf. `{r6 | core | verified}` — Naming paper for log-structured storage; first page loaded live from Ousterhout's Stanford copy.
   - elements: log-structured-storage
164. **littlefs DESIGN.md** — Christopher Haster / littlefs-project, living. github.com/littlefs-project/littlefs. https://github.com/littlefs-project/littlefs/blob/master/DESIGN.md. `{r6 | core | verified}` — Living embedded-flash design document teaching dynamic wear leveling and log-structured metadata on raw flash; confirmed live.
   - elements: flash-wear-leveling, log-structured-storage
165. **Physical Integrity in a Large Segmented Database** — Raymond A. Lorie, 1977. ACM TODS 2(1). `{r6 | advanced | unverified}` — Naming source for shadow paging (System R's shadow-page recovery); kept as canon alongside the Gray-Reuter treatment. **UNRESOLVED:** doi.
   - elements: shadow-paging
166. **A Digital Signature Based on a Conventional Encryption Function** — Ralph C. Merkle, 1987. CRYPTO 1987 (Springer LNCS 293). `{r6 | core | unverified}` — Canonical citation for the Merkle (hash) tree; Springer page blocked live this session. **UNRESOLVED:** doi.
   - elements: merkle-tree
167. **Effective STL: 50 Specific Ways to Improve Your Use of the Standard Template Library** — Scott Meyers, 2001. Addison-Wesley; author site aristeia.com. https://www.aristeia.com/books.html. `{r6 | core | verified}` — Names and teaches the erase-remove idiom (Item 32); author's page confirmed live.
   - elements: erase-remove
168. **martinfowler.com: Further Enterprise Application Architecture development (Event Sourcing; Memory Image)** — Martin Fowler, living. martinfowler.com. https://martinfowler.com/eaaDev/EventSourcing.html. `{r6 | core | verified}` — Fowler's maintained articles naming Event Sourcing (2005) and Memory Image (2011); both pages confirmed live.
   - elements: event-sourcing, memory-image
169. **Simple, Fast, and Practical Non-Blocking and Blocking Concurrent Queue Algorithms** — Maged M. Michael & Michael L. Scott, 1996. ACM PODC 1996. https://www.cs.rochester.edu/u/scott/papers/1996_PODC_queues.pdf. `{r6 | core | verified}` — The paper the lock-free FIFO queue element is named after; first page loaded live from Scott's Rochester copy.
   - elements: lock-free-fifo-queue-michael-scott
170. **'Memo' Functions and Machine Learning** — Donald Michie, 1968. Nature 218. `{r6 | advanced | unverified}` — Naming paper for memoization (memo functions); Nature page blocked live, identifier held at recall grade. **UNRESOLVED:** doi.
   - elements: memoization
171. **AI for Games, 3rd ed.** — Ian Millington, 2019. CRC Press. `{r6 | core | unverified}` — Pathfinding chapters teach navigation meshes as the standard game-AI world representation; CRC/Taylor & Francis pages blocked live this session. **UNRESOLVED:** isbn.
   - elements: navigation-mesh
172. **Small Materialized Aggregates: A Light Weight Index Structure for Data Warehousing** — Guido Moerkotte, 1998. VLDB 1998. https://www.vldb.org/conf/1998/p476.pdf. `{r6 | advanced | verified}` — Naming source for the zone-map/SMA mechanism (per-bucket min/max aggregates used to skip scans); loaded live from vldb.org proceedings.
   - elements: zone-map
173. **Purely Functional Data Structures** — Chris Okasaki, 1998. Cambridge University Press. doi:10.1017/CBO9780511530104. `{r6 | core | verified}` — The canonical treatment of persistent (immutable) data structure design: path copying, laziness, amortization under persistence.
   - elements: persistent-data-structure
174. **Improved Query Performance with Variant Indexes** — Patrick O'Neil & Dallan Quass, 1997. ACM SIGMOD 1997. `{r6 | advanced | unverified}` — Canonical bitmap-index paper (value-list/bit-sliced indexes); complements DDIA's columnar bitmap-encoding treatment. **UNRESOLVED:** doi.
   - elements: bitmap-index
175. **slot_map Container in C++ (WG21 P0661)** — Allan Deutsch, 2017. ISO C++ committee (LEWG/SG14), open-std.org. https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/p0661r0.pdf. `{r6 | advanced | verified}` — The WG21 proposal that names slot_map and specifies its generation-keyed contract; loaded live from open-std.org.
   - elements: slot-map
176. **Paradigms of Artificial Intelligence Programming: Case Studies in Common Lisp** — Peter Norvig, 1992. Morgan Kaufmann; full text at github.com/norvig/paip-lisp. https://github.com/norvig/paip-lisp. `{r6 | core | verified}` — Ch. 9 (Efficiency) is a genuine teaching treatment of memoization as a general design device; author-published full text confirmed live.
   - elements: memoization
177. **Skip Lists: A Probabilistic Alternative to Balanced Trees** — William Pugh, 1990. CACM 33(6). `{r6 | core | unverified}` — Canon naming paper for skip lists; Petrov and Herlihy-Shavit carry the treatments. **UNRESOLVED:** doi.
   - elements: skip-list
178. **Negative Caching of DNS Queries (DNS NCACHE)** — M. Andrews, 1998. IETF RFC 2308. https://www.rfc-editor.org/rfc/rfc2308.html. `{r6 | core | verified}` — Standards-body naming and specification of negative caching; the general mechanism's canonical citation.
   - elements: negative-caching
179. **Real-Time Rendering, 4th ed.** — Akenine-Möller, Haines & Hoffman, 2018. CRC Press. `{r6 | core | unverified}` — Named source for scene graph and BVH in the rendering context (acceleration/spatial data structure chapters); publisher and book-site pages blocked live this session. **UNRESOLVED:** isbn.
   - elements: bounding-volume-hierarchy, quadtree-octree, scene-graph
180. **Algorithms, 4th ed.** — Robert Sedgewick & Kevin Wayne, 2011. Addison-Wesley; official site algs4.cs.princeton.edu. https://algs4.cs.princeton.edu/. `{r6 | core | verified}` — Teaching canon with live companion site; confirmed chapters for priority queues (2.4), BSTs (3.2), hash tables (3.4), tries (5.2), suffix arrays (6.3).
   - elements: binary-heap-priority-queue, binary-search-tree, hash-table, queue-fifo, stack, suffix-array, trie
181. **Conflict-free Replicated Data Types** — Shapiro, Preguica, Baquero & Zawirski, 2011. SSS 2011; INRIA RR-7687. `{r6 | core | unverified}` — Naming paper defining CRDTs and the CvRDT/CmRDT taxonomy; HAL and Springer pages blocked live this session. **UNRESOLVED:** doi.
   - elements: conflict-free-replicated-data-type-crdt
182. **Computing Extremely Accurate Quantiles Using t-Digests** — Ted Dunning & Otmar Ertl, 2019. arXiv. arXiv:1902.04023. `{r6 | core | verified}` — Naming paper for the t-digest quantile sketch; confirmed live on arXiv.
   - elements: t-digest
183. **Optimal Probabilistic Cache Stampede Prevention** — Vattani, Chierichetti & Lowenstein, 2015. PVLDB 8(8). https://www.vldb.org/pvldb/vol8/p886-vattani.pdf. `{r6 | advanced | verified}` — Names the cache-stampede problem and gives the XFetch early-recomputation mechanism; loaded live from PVLDB.
   - elements: cache-stampede-protection
184. **Venti: A New Approach to Archival Storage** — Sean Quinlan & Sean Dorward, 2002. USENIX FAST 2002; Bell Labs. https://9p.io/sys/doc/venti/venti.html. `{r6 | core | verified}` — Naming paper for content-addressable storage as a design mechanism (hash-of-contents block identity, write-once coalescing); full text confirmed live on the Plan 9 doc host.
   - elements: content-addressable-storage
185. **Text Buffer Reimplementation (VS Code blog)** — Peng Lyu / Microsoft, 2018. code.visualstudio.com. https://code.visualstudio.com/blogs/2018/03/23/text-buffer-reimplementation. `{r6 | core | verified}` — Official project engineering post teaching the piece table (and its piece-tree evolution) as a production text-buffer structure; confirmed live.
   - elements: piece-table

### Membership (existing works, reclaimed under the element lens)

186. **[MEMBERSHIP id=progit]** `{r6 | core | verified}` — Git Internals chapter is the canonical modern teaching of a content-addressable object store (hash-keyed blobs, write-once).
   - elements: content-addressable-storage

## R7. Language idioms, functional & data representation

### New

187. **Functional Core, Imperative Shell** — Gary Bernhardt, 2012. Destroy All Software screencast (Classic Season 4). https://www.destroyallsoftware.com/screencasts/catalog/functional-core-imperative-shell. `{r7 | anchor | verified}` — The naming screencast for the functional-core/imperative-shell structuring idiom; episode confirmed in the live catalog.
   - elements: functional-core-imperative-shell
188. **Erlang/OTP System Documentation - Compilation and Code Loading** — Ericsson AB, living. erlang.org. https://www.erlang.org/doc/system/code_loading.html. `{r7 | anchor | verified}` — Authoritative current/old-code semantics for hot code replacement; the reference realization of hot code reload.
   - elements: hot-code-reload
189. **Feature Toggles (aka Feature Flags)** — Pete Hodgson, 2017. martinfowler.com. https://martinfowler.com/articles/feature-toggles.html. `{r7 | anchor | verified}` — The catalog-grade treatment of feature flags: toggle taxonomy (release/experiment/ops/permissioning), toggle points, routers, configuration.
   - elements: feature-flag
190. **Programming in Haskell, 2nd ed.** — Graham Hutton, 2016. Cambridge University Press. ISBN 978-1316626221. `{r7 | anchor | verified}` — Route anchor for FP idiom teaching: currying (ch. 4), algebraic data types incl. Maybe (ch. 8), monads (ch. 12); confirmed on the author's official CUP-linked page.
   - elements: currying-partial-application, monad, option-type, tagged-union
191. **C++ Templates: The Complete Guide, 2nd ed.** — David Vandevoorde, Nicolai M. Josuttis, Douglas Gregor, 2017. Addison-Wesley. ISBN 978-0-321-71412-1. `{r7 | anchor | verified}` — Route anchor for C++ template idioms: names and teaches SFINAE, traits, tag dispatching, typelists, EBCO, and expression templates in one catalog-grade reference.
   - elements: empty-base-optimization-ebo, expression-templates, sfinae, tag-dispatching, traits-class, typelist
192. **Evolve Your Hierarchy: Refactoring Game Entities with Components** — Mick West, 2007. Cowboy Programming (blog). https://cowboyprogramming.com/2007/01/05/evolve-your-heirachy/. `{r7 | anchor | verified}` — The seminal article moving game entities from deep hierarchies to component composition; the route's ECS naming source.
   - elements: entity-component-system
193. **The Design and Implementation of Modern Column-Oriented Database Systems** — Daniel Abadi, Peter Boncz, Stavros Harizopoulos, Stratos Idreos, Samuel Madden, 2013. Foundations and Trends in Databases 5(3). DOI 10.1561/1900000024. `{r7 | survey | verified}` — The catalog-grade survey of columnar storage: column layouts, dictionary and light-weight compression encodings, PAX hybrid; verified via author-hosted final PDF.
   - elements: column-oriented-storage, dictionary-encoding, pax-page-layout
194. **Weaving Relations for Cache Performance** — Anastassia Ailamaki, David J. DeWitt, Mark D. Hill, Marios Skounakis, 2001. VLDB 2001. http://www.vldb.org/conf/2001/P169.pdf. `{r7 | core | verified}` — Introduces the PAX (Partition Attributes Across) page layout; verified via the official VLDB proceedings PDF.
   - elements: pax-page-layout
195. **Compiling with Continuations** — Andrew W. Appel, 1991. Cambridge University Press. DOI 10.1017/CBO9780511609619. `{r7 | core | verified}` — The book-length treatment of continuation-passing style as a compiler intermediate representation.
   - elements: continuation-passing-style
196. **Finally Tagless, Partially Evaluated: Tagless Staged Interpreters for Simpler Typed Languages** — Jacques Carette, Oleg Kiselyov, Chung-chieh Shan, 2009. Journal of Functional Programming 19(5), pp. 509-543. https://okmij.org/ftp/tagless-final/index.html. `{r7 | advanced | verified}` — The naming paper for the tagless-final embedding style; JFP citation confirmed on Kiselyov's official tagless-final page.
   - elements: tagless-final
197. **An Efficient Implementation of Self, a Dynamically-Typed Object-Oriented Language Based on Prototypes** — Craig Chambers, David Ungar, Elgin Lee, 1989. OOPSLA '89 / SIGPLAN Notices 24(10). https://bibliography.selflanguage.org/implementation.html. `{r7 | core | verified}` — Introduces implementation-level maps - the mechanism V8 later popularized as hidden classes; verified on the official Self bibliography site.
   - elements: hidden-class
198. **Combinators for Bi-Directional Tree Transformations: A Linguistic Approach to the View Update Problem** — J. Nathan Foster, Michael B. Greenwald, Jonathan T. Moore, Benjamin C. Pierce, Alan Schmitt, 2007. ACM TOPLAS 29(3). https://www.cis.upenn.edu/~bcpierce/papers/lenses-toplas-final.pdf. `{r7 | advanced | verified}` — The paper that dubbed bidirectional accessors lenses; verified via the author-hosted TOPLAS final text (DOI omitted - ACM DL blocked).
   - elements: lens
199. **Analysis Patterns: Reusable Object Models** — Martin Fowler, 1996. Addison-Wesley. ISBN 0201895420. `{r7 | core | verified}` — Names Quantity (value + unit) and Range as reusable domain-model representations.
   - elements: quantity, range
200. **Collection Pipeline** — Martin Fowler, 2015. martinfowler.com. https://martinfowler.com/articles/collection-pipeline/. `{r7 | core | verified}` — The naming treatment of the collection-pipeline style (map/filter/reduce composition) across languages.
   - elements: collection-pipeline
201. **Representing Type Information in Dynamically Typed Languages** — David Gudeman, 1993. University of Arizona TR 93-27. `{r7 | survey | unverified}` — The canonical survey of pointer tagging, NaN-boxing and related runtime type-representation schemes. **UNRESOLVED:** primary page (UA TR archive not loadable; identity corroborated via citing literature only).
   - elements: pointer-tagging
202. **Error Detecting and Error Correcting Codes** — Richard W. Hamming, 1950. Bell System Technical Journal 29(2). `{r7 | core | unverified}` — The founding paper of error-correcting codes (Hamming codes/distance); canonical naming source. **UNRESOLVED:** doi/primary page (IEEE/Wiley archive not loadable this session).
   - elements: error-correcting-codes
203. **Thunks: A Way of Compiling Procedure Statements with Some Comments on Procedure Declarations** — P. Z. Ingerman, 1961. Communications of the ACM 4(1). `{r7 | core | unverified}` — The naming paper for thunks (delayed-evaluation closures for call-by-name argument passing). **UNRESOLVED:** doi (ACM DL blocked this session).
   - elements: thunk
204. **Practical Texture Atlases** — Ivan-Assen Ivanov, 2006. Game Developer (Gamasutra). https://www.gamedeveloper.com/programming/practical-texture-atlases. `{r7 | core | verified}` — Practitioner treatment of texture-atlas packing and batching; the NVIDIA 2004 whitepaper names the technique but has no stable primary page.
   - elements: texture-atlas
205. **Types for Units-of-Measure: Theory and Practice** — Andrew Kennedy, 2010. CEFP 2009, LNCS 6299, pp. 268-305. DOI 10.1007/978-3-642-17685-2_8. `{r7 | core | verified}` — Definitive treatment of units-of-measure types (theory + the F# realization); subsumes Kennedy's 1996 dissertation line of work.
   - elements: units-of-measure-types
206. **Domain Specific Embedded Compilers** — Daan Leijen, Erik Meijer, 1999. 2nd USENIX Conference on Domain-Specific Languages (DSL'99). `{r7 | advanced | unverified}` — The paper that introduced phantom type variables for typing embedded DSL expressions. **UNRESOLVED:** primary page (USENIX pages returned 403 this session; listing seen in search index only).
   - elements: phantom-type
207. **Level of Detail for 3D Graphics** — David Luebke, Martin Reddy, Jonathan Cohen, Amitabh Varshney, Benjamin Watson, Robert Huebner, 2003. Morgan Kaufmann. ISBN 1-55860-838-9. `{r7 | core | verified}` — The book-length canonical treatment of level-of-detail representations; ISBN confirmed on official companion site lodbook.com.
   - elements: level-of-detail
208. **The New C: X Macros** — Randy Meyers, 2001. C/C++ Users Journal 19(5). `{r7 | core | unverified}` — The naming article for the X-macro parallel-table technique; full archived text confirms title/author/issue. **UNRESOLVED:** primary page (CUJ/Dr. Dobb's defunct; archived full text at jacobfilipp.com/DrDobbs loaded live this session).
   - elements: x-macro
209. **Notions of Computation and Monads** — Eugenio Moggi, 1991. Information and Computation 93(1). https://person.dibris.unige.it/moggi-eugenio/ftp/ic91.pdf. `{r7 | advanced | verified}` — The paper that brought monads into programming-language semantics; verified via the author-hosted full text (title/author on first page).
   - elements: monad
210. **Types and Programming Languages** — Benjamin C. Pierce, 2002. MIT Press. ISBN 0-262-16209-1. `{r7 | core | verified}` — Textbook foundation for sums/variants - the type-theoretic account of tagged unions; verified on the author's official book page.
   - elements: tagged-union
211. **Pattern Languages of Program Design 5** — Dragos Manolescu, Markus Voelter, James Noble (eds.), 2006. Addison-Wesley. ISBN 978-0-321-32194-7. `{r7 | core | verified}` — PLoPD volume carrying the Comparand pattern (cheap identity testing via dedicated comparison values).
   - elements: comparand
212. **Handlers of Algebraic Effects** — Gordon Plotkin, Matija Pretnar, 2009. ESOP 2009, LNCS 5502, pp. 80-94. DOI 10.1007/978-3-642-00590-9_7. `{r7 | advanced | verified}` — The naming paper for effect handlers as the general mechanism behind exceptions, state, I/O and concurrency effects.
   - elements: effect-handler
213. **Definitional Interpreters for Higher-Order Programming Languages** — John C. Reynolds, 1972. ACM Annual Conference 1972; reprinted Higher-Order and Symbolic Computation 11 (1998). https://homepages.inf.ed.ac.uk/wadler/papers/papers-we-love/reynolds-definitional-interpreters-1998.pdf. `{r7 | advanced | verified}` — Introduces defunctionalization (and CPS transformation of interpreters); verified via the hosted HOSC 1998 reprint full text.
   - elements: defunctionalization
214. **Rust API Guidelines** — Rust library team, living. rust-lang.github.io. https://rust-lang.github.io/api-guidelines/future-proofing.html. `{r7 | core | verified}` — C-SEALED documents the sealed-trait idiom (private supertrait blocking downstream impls) as an API future-proofing rule.
   - elements: sealed-trait
215. **Rust Design Patterns** — rust-unofficial contributors, living. rust-unofficial.github.io. https://rust-unofficial.github.io/patterns/. `{r7 | survey | verified}` — Living Rust idiom catalog; Newtype entry confirmed live (zero-cost opaque wrapper types).
   - elements: newtype
216. **Typestate: A Programming Language Concept for Enhancing Software Reliability** — Robert E. Strom, Shaula Yemini, 1986. IEEE Transactions on Software Engineering SE-12(1). `{r7 | advanced | unverified}` — The naming paper for typestate; the Embedded Rust Book membership carries the living realization. **UNRESOLVED:** doi/primary page (IEEE Xplore not loadable this session).
   - elements: typestate
217. **Data Types a la Carte** — Wouter Swierstra, 2008. Journal of Functional Programming 18(4). DOI 10.1017/S0956796808006758. `{r7 | advanced | verified}` — Functional pearl assembling data types and interpreters from components via free monads; the route's free-monad source.
   - elements: free-monad
218. **Pattern Hatching: Design Patterns Applied** — John Vlissides, 1998. Addison-Wesley. ISBN 978-0-201-43293-0. `{r7 | core | verified}` — Names and works through Generation Gap (keeping generated and hand-written code apart via subclassing).
   - elements: generation-gap
219. **Pointer Swizzling at Page Fault Time: Efficiently and Compatibly Supporting Huge Address Spaces on Standard Hardware** — Paul R. Wilson, Sheetal V. Kakkad, 1992. Int. Workshop on Object Orientation in Operating Systems (IWOOOS '92). `{r7 | core | unverified}` — Canonical paper on swizzling persistent object references to raw pointers at fault time. **UNRESOLVED:** doi/primary page (only aggregator copies located this session).
   - elements: pointer-swizzling

### Membership (existing works, reclaimed under the element lens)

220. **[MEMBERSHIP id=carnieregisters]** `{r7 | advanced | verified}` — Embedded register-access series that applies tag dispatching and traits machinery in anger; the route's named_in for tag dispatching.
   - elements: tag-dispatching, traits-class
221. **[MEMBERSHIP id=embeddedrust]** `{r7 | core | verified}` — Static Guarantees chapter is the living catalog-grade treatment of typestate programming (peripheral state machines in types).
   - elements: typestate
222. **[MEMBERSHIP id=meyerseffmod]** `{r7 | core | verified}` — Item 10 (prefer scoped enums) is the modern C++ statement of the type-safe enum idiom.
   - elements: type-safe-enum
223. **[MEMBERSHIP id=preschernplop]** `{r7 | core | verified}` — The EuroPLoP paper form of the file-organization and data-lifetime pattern sets; names the route's module-state patterns. (also serves r8)
   - elements: log-errors, organizing-files-in-modular-c-programs, return-status-code, software-module-with-global-state, special-return-value, stateless-software-module
224. **[MEMBERSHIP id=tornhill]** `{r7 | core | verified}` — Names the same mechanism First-Class ADT; C-idiom treatment of opaque handles.
   - elements: opaque-pointer

## R8. Error handling, robustness & security

### New

225. **Timeouts, Retries, and Backoff with Jitter (Amazon Builders' Library)** — Marc Brooker, living. Amazon Builders' Library. https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/. `{r8 | anchor | unverified}` — The modern canonical treatment of the timeout/retry/backoff+jitter triad, including token-bucket retry limiting. **UNRESOLVED:** live primary page (URL 301s to builder.aws.com, which renders client-side; article content could not be loaded this session).
   - elements: retry-budget, retry-with-exponential-backoff-and-jitter, timeout
226. **Handbook of Applied Cryptography** — Alfred J. Menezes, Paul C. van Oorschot, Scott A. Vanstone, 1996. CRC Press. https://cacr.uwaterloo.ca/hac/. `{r8 | anchor | verified}` — Official free-PDF page loaded live: ch. 5 (pseudorandom bits/CSPRNGs), ch. 9 (hash functions and MACs), ch. 10 (nonces in identification protocols).
   - elements: cryptographic-hash-function, csprng, message-authentication-code, nonce
227. **OTP Design Principles (Erlang/OTP System Documentation)** — Ericsson / Erlang-OTP team, living. erlang.org. https://www.erlang.org/doc/system/design_principles.html. `{r8 | anchor | verified}` — Loaded live: defines supervisors, workers, supervision trees, and restart strategies — the primary source for the Supervisor element.
   - elements: supervisor
228. **OWASP Cheat Sheet Series** — OWASP, living. OWASP. https://cheatsheetseries.owasp.org/. `{r8 | anchor | verified}` — Index loaded live confirming Input Validation, Query Parameterization, CSRF Prevention (Synchronizer Token), Password Storage, and XSS Prevention sheets — the living catalog-grade treatment of these defenses.
   - elements: allowlist-input-validation, html-sanitization, parameterized-query, salted-password-hashing, synchronizer-token
229. **Architectural Patterns for Enabling Application Security** — Joseph Yoder, Jeffrey Barcalow, 1997. PLoP '97 (4th Pattern Languages of Programming conference). https://hillside.net/plop/plop97/Proceedings/yoder.pdf. `{r8 | anchor | verified}` — PDF loaded live: names the seven application-security patterns — Single Access Point, Check Point, Roles, Session, Full View With Errors, Limited View, Secure Access Layer.
   - elements: check-point, full-view-with-errors, limited-view, role-based-access-control, secure-access-layer, security-session, single-access-point
230. **AddressSanitizer: A Fast Address Sanity Checker** — Konstantin Serebryany, Derek Bruening, Alexander Potapenko, Dmitriy Vyukov, 2012. USENIX ATC 2012. https://research.google/pubs/addresssanitizer-a-fast-address-sanity-checker/. `{r8 | advanced | verified}` — Google Research publication page loaded live; shadow-memory redzone poisoning is the modern systematic form of memory poisoning (alongside kernel page/slab poisoning).
   - elements: memory-poisoning
231. **The N-Version Approach to Fault-Tolerant Software** — Algirdas Avizienis, 1985. IEEE Transactions on Software Engineering SE-11(12), pp. 1491-1501. DOI 10.1109/TSE.1985.231893. `{r8 | core | unverified}` — The canon definition of N-version programming; IEC 61508-7 (membership) carries the standards-grade backstop. **UNRESOLVED:** primary DL page (dl.acm.org/IEEE returned 403; DOI taken from the ACM DL link surfaced in search, not a loaded page).
   - elements: n-version-programming
232. **AVR180: External Brown-out Protection (application note)** — Atmel (now Microchip), 2002. Atmel/Microchip application note doc1051. https://ww1.microchip.com/downloads/en/AppNotes/doc1051.pdf. `{r8 | core | verified}` — PDF loaded live: the naming application note — preventing CPU/EEPROM corruption during brown-outs via low-voltage detectors, with discrete and IC solutions.
   - elements: brown-out-handling
233. **BearSSL: Constant-Time Crypto** — Thomas Pornin, living. bearssl.org. https://bearssl.org/constanttime.html. `{r8 | core | verified}` — Loaded live: the practitioner treatment of timing side channels and constant-time coding, including secret-independent comparison.
   - elements: constant-time-comparison
234. **Crash-Only Software** — George Candea, Armando Fox, 2003. HotOS IX (USENIX). https://dslab.epfl.ch/pubs/crashonly.pdf. `{r8 | advanced | verified}` — Author-lab (EPFL DSLab) PDF loaded live: crash-safe/recover-fast design — the systems-research statement of the let-it-crash discipline.
   - elements: crash-only-software, let-it-crash
235. **A Painless Guide to CRC Error Detection Algorithms** — Ross N. Williams, 1993. ross.net (self-published; widely mirrored). https://zlib.net/crc_v3.txt (mirror; ross.net unreachable this session). `{r8 | core | verified}` — Full document loaded live: the classic teaching treatment of CRC theory, the Rocksoft parameterized model, and table-driven implementations.
   - elements: cyclic-redundancy-check
236. **The CHECKS Pattern Language of Information Integrity** — Ward Cunningham, 1994. PLoP '94; c2.com Portland Pattern Repository. https://c2.com/ppr/checks.html. `{r8 | core | verified}` — Loaded live: names Exceptional Value, Meaningless Behavior, and Deferred Validation among its eleven information-integrity patterns.
   - elements: deferred-validation, exceptional-value, meaningless-behavior
237. **Software Rejuvenation: Analysis, Module and Applications** — Yennun Huang, Chandra Kintala, Nick Kolettis, N. Dudley Fulton, 1995. FTCS-25 (25th Int. Symposium on Fault-Tolerant Computing), pp. 381-390. `{r8 | advanced | unverified}` — The naming paper: proactive graceful restart to a clean internal state to counter software aging. **UNRESOLVED:** doi + primary DL page (IEEE Xplore not loaded this session; venue/pages from search indexes).
   - elements: software-rejuvenation
238. **Reactive Design Patterns** — Roland Kuhn with Brian Hanafee and Jamie Allen, 2017. Manning. ISBN 978-1-61729-180-7. `{r8 | core | verified}` — Publisher page loaded live; fault-tolerance pattern chapter is the book-form treatment of Error Kernel, Let-It-Crash, actor supervision, and Circuit Breaker.
   - elements: circuit-breaker, error-kernel, let-it-crash, supervisor
239. **MCUboot documentation** — MCUboot project, living. docs.mcuboot.com. https://docs.mcuboot.com/. `{r8 | core | verified}` — Loaded live: the reference secure bootloader for 32-bit MCUs — image signing (imgtool) and boot-time signature verification.
   - elements: secure-boot-image-verification
240. **Creating Guard Pages (Win32 memory management documentation)** — Microsoft, living. Microsoft Learn. https://learn.microsoft.com/en-us/windows/win32/memory/creating-guard-pages. `{r8 | core | verified}` — Loaded live: defines PAGE_GUARD one-shot alarm pages with a worked example — the OS-vendor definition of the guard page mechanism.
   - elements: guard-page
241. **perlsec — Perl security (taint mode)** — Perl 5 Porters, living. perldoc.perl.org. https://perldoc.perl.org/perlsec. `{r8 | core | verified}` — Loaded live: the canonical language-runtime definition of taint checking — taint sources, propagation, and laundering via pattern match.
   - elements: taint-checking
242. **Preventing Privilege Escalation** — Niels Provos, Markus Friedl, Peter Honeyman, 2003. 12th USENIX Security Symposium. `{r8 | advanced | unverified}` — The canonical privilege-separation paper (OpenSSH privsep): splitting a program into privileged monitor and unprivileged slave. **UNRESOLVED:** live primary page (usenix.org returned 403 on all paper URLs; citi.umich.edu unreachable this session).
   - elements: privilege-separation
243. **System Structure for Software Fault Tolerance** — Brian Randell, 1975. IEEE Transactions on Software Engineering SE-1(2), pp. 220-232. `{r8 | core | unverified}` — The canon naming paper for recovery blocks (and the domino effect); IEC 61508-7 (membership) backstops at standards grade. **UNRESOLVED:** doi + primary DL page (IEEE/ACM pages returned 403 this session).
   - elements: recovery-blocks
244. **RFC 5116: An Interface and Algorithms for Authenticated Encryption** — David McGrew, 2008. IETF. RFC 5116. `{r8 | core | verified}` — rfc-editor info page loaded live; defines the AEAD interface — the standards-body definition of authenticated encryption as a usable mechanism.
   - elements: authenticated-encryption
245. **RFC 8305: Happy Eyeballs Version 2: Better Connectivity Using Concurrency** — David Schinazi, Tommy Pauly, 2017. IETF. RFC 8305. `{r8 | core | verified}` — rfc-editor info page loaded live; the normative specification of the Happy Eyeballs concurrent-connection fallback algorithm.
   - elements: happy-eyeballs
246. **The Protection of Information in Computer Systems** — Jerome H. Saltzer, Michael D. Schroeder, 1975. Proceedings of the IEEE 63(9). https://web.mit.edu/Saltzer/www/publications/protection/. `{r8 | core | verified}` — Author's MIT page loaded live: defines access control lists vs capabilities (list-oriented vs ticket-oriented protection) — the canon for both elements.
   - elements: access-control-list, capability
247. **Security Patterns: Integrating Security and Systems Engineering** — Markus Schumacher, Eduardo Fernandez-Buglioni, Duane Hybertson, Frank Buschmann, Peter Sommerlad, 2006. Wiley (Wiley Software Patterns Series). ISBN 978-0-470-85884-4. `{r8 | core | verified}` — Front matter loaded live (Wiley e-preview) confirming title/authors; the book-form consolidation of the Yoder-Barcalow language plus Reference Monitor and RBAC patterns.
   - elements: check-point, full-view-with-errors, limited-view, reference-monitor, role-based-access-control, security-session, single-access-point
248. **Developer's Guide to Oracle Solaris Security — Privilege Bracketing** — Oracle, living. docs.oracle.com. https://docs.oracle.com/cd/E19120-01/open.solaris/819-2145/eyals/index.html. `{r8 | core | verified}` — Loaded live: names privilege bracketing and shows the enable-use-disable privilege discipline in both superuser and least-privilege models.
   - elements: privilege-bracketing
249. **StackGuard: Automatic Adaptive Detection and Prevention of Buffer-Overflow Attacks** — Crispin Cowan et al., 1998. 7th USENIX Security Symposium. `{r8 | advanced | unverified}` — Names the stack canary and defines the compiler-inserted canary-check mechanism. **UNRESOLVED:** live primary page (usenix.org returned 403).
   - elements: stack-canary
250. **Exceptional C++: 47 Engineering Puzzles, Programming Problems, and Solutions** — Herb Sutter, 1999. Addison-Wesley. ISBN 978-0-201-61562-3. `{r8 | core | verified}` — InformIT page loaded live; the exception-safety canon that established copy-and-swap for strongly exception-safe assignment.
   - elements: copy-and-swap
251. **Railway Oriented Programming** — Scott Wlaschin, 2014. fsharpforfunandprofit.com / NDC. https://fsharpforfunandprofit.com/rop/. `{r8 | core | verified}` — Loaded live: the naming treatment of railway-oriented error handling and a catalog-grade teaching of two-track Result-type composition.
   - elements: railway-oriented-programming, result-type

### Membership (existing works, reclaimed under the element lens)

252. **[MEMBERSHIP id=certc]** `{r8 | core | verified}` — Rule-level treatments: sensitive-data zeroization (MSC06/memset_s) and canonicalization before validation (FIO02-C).
   - elements: canonicalization-before-validation, secure-zeroization
253. **[MEMBERSHIP id=gdbmanual]** `{r8 | core | verified}` — The authoritative living doc for producing and analyzing core dump files (gcore, core-file debugging).
   - elements: core-dump
254. **[MEMBERSHIP id=iec61508]** `{r8 | core | verified}` — Part 7 technique catalog defines program sequence monitoring, self-tests (BIST), diverse/N-version programming, and recovery blocks as normative safety techniques.
   - elements: built-in-self-test, n-version-programming, program-sequence-monitoring, recovery-blocks
255. **[MEMBERSHIP id=iso26262]** `{r8 | core | verified}` — Defines and mandates the safe state concept for automotive fault reactions.
   - elements: safe-state
256. **[MEMBERSHIP id=kernelstyle]** `{r8 | core | verified}` — Chapter 7 codifies centralized function exit via goto for cleanup — the canonical goto-cleanup statement.
   - elements: goto-cleanup
257. **[MEMBERSHIP id=koopmanbess]** `{r8 | core | verified}` — Dedicated watchdog-timer chapter: correct kicking discipline, what a watchdog can and cannot detect.
   - elements: watchdog
258. **[MEMBERSHIP id=p1028]** `{r8 | advanced | verified}` — Status/result-object design for C++ — the systems-language face of the result type.
   - elements: result-type
259. **[MEMBERSHIP id=seacordsecure]** `{r8 | core | verified}` — Teaches stack-smashing mitigations (canaries/StackGuard lineage) and canonicalize-then-validate for file-name and input handling.
   - elements: canonicalization-before-validation, stack-canary

## R9. Parsing, text & serialization

### New

260. **Compilers: Principles, Techniques, and Tools (2nd ed.)** — Alfred V. Aho, Monica S. Lam, Ravi Sethi, Jeffrey D. Ullman, 2006. Addison-Wesley. http://www.cs.columbia.edu/~aho/books.html. `{r9 | anchor | verified}` — The canonical compiler text: names and teaches lexing, regex-to-automata, recursive-descent and LR parsing, ASTs, symbol tables, panic-mode recovery (Aho's own books page, loaded live, dates the AW printing 2007).
   - elements: abstract-syntax-tree, lexer, lr-parser, maximal-munch, panic-mode-error-recovery, recursive-descent-parser, regular-expressions, symbol-table
261. **Protocol Buffers Encoding (programming guide)** — Google / Protocol Buffers project, living. protobuf.dev. https://protobuf.dev/programming-guides/encoding/. `{r9 | anchor | verified}` — The living authoritative definition of base-128 varints, ZigZag encoding, LEN length-prefixed records, and field-tag wire format (page loaded live; confirms all four mechanisms).
   - elements: length-prefix-framing, schema-evolution-via-field-tags, varint, zigzag-encoding
262. **Consistent Overhead Byte Stuffing** — Stuart Cheshire, Mary Baker, 1999. IEEE/ACM Transactions on Networking 7(2). `{r9 | advanced | unverified}` — Naming paper for COBS - byte stuffing with tightly bounded worst-case overhead, now standard in embedded serial framing; IEEE/author pages not loadable this session. **UNRESOLVED:** doi.
   - elements: byte-stuffing, consistent-overhead-byte-stuffing
263. **Algol 60 Translation: An Algol 60 Translator for the X1 and Making a Translator for Algol 60** — Edsger W. Dijkstra, 1961. Stichting Mathematisch Centrum, report MR 34/61. https://ir.cwi.nl/pub/9251. `{r9 | core | verified}` — Primary source of the shunting-yard algorithm for infix-expression translation (record loaded live in the CWI institutional repository).
   - elements: shunting-yard-algorithm
264. **file / libmagic (official project site and magic file documentation)** — Ian Darwin; maintained by Christos Zoulas et al., living. darwinsys.com/file. https://darwinsys.com/file/. `{r9 | core | verified}` — The canonical operationalization of magic numbers / file signatures: the file command and libmagic identify formats by content signatures (official site loaded live).
   - elements: magic-number-file-signature
265. **Packrat Parsing: Simple, Powerful, Lazy, Linear Time** — Bryan Ford, 2002. ACM ICFP 2002. https://bford.info/packrat/. `{r9 | advanced | verified}` — Naming paper for packrat (memoizing PEG) parsing; confirmed live on Ford's own packrat/PEG bibliography page.
   - elements: packrat-parsing
266. **Monadic Parser Combinators** — Graham Hutton, Erik Meijer, 1996. Technical Report NOTTCS-TR-96-4, University of Nottingham. https://people.cs.nott.ac.uk/pszgmh/monparsing.pdf. `{r9 | core | verified}` — The tutorial that established monadic parser combinators as the FP idiom for building parsers (citation confirmed live on Hutton's Nottingham publications page).
   - elements: parser-combinator
267. **ISO/IEC 9899 - Programming Languages - C** — ISO/IEC JTC1/SC22/WG14, 2024. ISO/IEC (C23). ISO/IEC 9899:2024. `{r9 | core | verified}` — The C standard normatively defines escape sequences (\n, \xhh, ...), the definition every language's escape-sequence lexing inherits (WG14 official page loaded live confirming ISO/IEC 9899, C23 adopted 2024).
   - elements: escape-sequence
268. **On the Translation of Languages from Left to Right** — Donald E. Knuth, 1965. Information and Control 8(6). `{r9 | advanced | unverified}` — The paper that defined LR(k) parsing; canon naming source behind the Dragon Book's ch. 4 treatment (publisher page not loadable this session). **UNRESOLVED:** doi.
   - elements: lr-parser
269. **Prettyprinting** — Derek C. Oppen, 1980. ACM TOPLAS 2(4). `{r9 | core | unverified}` — The canonical linear-time pretty-printing algorithm paper that most later pretty-printer libraries descend from; ACM DL page not loadable this session. **UNRESOLVED:** doi.
   - elements: pretty-printer
270. **Enforcing Strict Model-View Separation in Template Engines** — Terence Parr, 2004. WWW 2004 (ACM). `{r9 | core | unverified}` — The StringTemplate paper - the principled treatment of template-engine design and model-view separation; author-site PDF retrieved but no citation page loadable this session. **UNRESOLVED:** doi.
   - elements: template-engine
271. **Top Down Operator Precedence** — Vaughan R. Pratt, 1973. ACM POPL '73. `{r9 | core | unverified}` — Naming paper for Pratt (top-down operator-precedence) parsing; ACM DL and author pages not loadable this session. **UNRESOLVED:** doi.
   - elements: pratt-parser
272. **"Maximal-Munch" Tokenization in Linear Time** — Thomas Reps, 1998. ACM TOPLAS 20(2):259-273. https://pages.cs.wisc.edu/~reps/. `{r9 | advanced | verified}` — Canonical paper on the maximal-munch (longest-match) tokenization rule and its linear-time realization (citation confirmed live on Reps's Wisconsin page).
   - elements: maximal-munch
273. **Nonstandard for Transmission of IP Datagrams over Serial Lines: SLIP** — J. Romkey, 1988. RFC 1055. https://www.rfc-editor.org/info/rfc1055. `{r9 | core | verified}` — The classic END/ESC byte-stuffing framing spec - the minimal worked example every serial-framing design descends from (RFC info page loaded live).
   - elements: byte-stuffing
274. **Delta Encoding in HTTP** — J. Mogul, B. Krishnamurthy, F. Douglis, A. Feldmann, Y. Goland, A. van Hoff, D. Hellerstein, 2002. RFC 3229. https://www.rfc-editor.org/info/rfc3229. `{r9 | advanced | verified}` — Standards-grade naming and treatment of delta encoding (transmitting differences instead of full instances) (RFC info page loaded live).
   - elements: delta-encoding
275. **Uniform Resource Identifier (URI): Generic Syntax** — T. Berners-Lee, R. Fielding, L. Masinter, 2005. RFC 3986 / STD 66. https://www.rfc-editor.org/info/rfc3986. `{r9 | core | verified}` — Sec. 2.1 is the normative definition of percent-encoding (RFC info page loaded live).
   - elements: percent-encoding
276. **The Base16, Base32, and Base64 Data Encodings** — S. Josefsson, 2006. RFC 4648. https://www.rfc-editor.org/info/rfc4648. `{r9 | core | verified}` — The normative definition of the standard binary-to-text encodings (RFC info page loaded live).
   - elements: binary-to-text-encoding
277. **JSON Canonicalization Scheme (JCS)** — Anders Rundgren, Bret Jordan, Samuel Erdtman, 2020. RFC 8785 (Informational). https://www.rfc-editor.org/info/rfc8785. `{r9 | advanced | verified}` — The modern canonical-serialization treatment for JSON (deterministic form for hashing/signing), complementing DER's binary canon (RFC info page loaded live).
   - elements: canonical-serialization
278. **HTTP/1.1** — R. Fielding, M. Nottingham, J. Reschke (eds.), 2022. RFC 9112 / STD 99. https://www.rfc-editor.org/info/rfc9112. `{r9 | core | verified}` — Current normative definition of chunked transfer coding - the canonical streaming length-delimited text framing (RFC info page loaded live).
   - elements: chunked-transfer-encoding
279. **Serializer** — Dirk Riehle, Wolf Siberski, Dirk Baeumer, Daniel Megert, Heinz Zuellighoven, 1998. Pattern Languages of Program Design 3, ch. 17, Addison-Wesley. https://riehle.org/computer-science/research/1996/plop-1996-serializer.html. `{r9 | core | verified}` — The pattern-form definition of Serializer (stream objects to/from arbitrary backends); PLoPD3 TOC with the Serializer chapter loaded live on Riehle's site.
   - elements: serializer
280. **Data Compression: The Complete Reference (4th ed.)** — David Salomon, 2007. Springer. ISBN 978-1-84628-603-2. `{r9 | survey | verified}` — The comprehensive compression reference; its Basic Techniques chapter is the catalog-grade treatment of run-length encoding (Springer book page loaded live).
   - elements: run-length-encoding
281. **SAX (Simple API for XML) - official project documentation** — David Megginson et al., living. sax.sourceforge.net. http://sax.sourceforge.net/. `{r9 | core | verified}` — The de-facto-standard event-based XML API whose docs ('Events vs. Trees') define push/event-driven parsing (official site loaded live).
   - elements: event-driven-parsing
282. **Programming Techniques: Regular Expression Search Algorithm** — Ken Thompson, 1968. Communications of the ACM 11(6). `{r9 | core | unverified}` — Canon naming/implementation paper for regular-expression matching (Thompson NFA construction); ACM DL not loadable this session; Dragon Book ch. 3 is the modern teaching treatment. **UNRESOLVED:** doi.
   - elements: regular-expressions
283. **Tolerant Reader (bliki)** — Martin Fowler, 2011. martinfowler.com. https://martinfowler.com/bliki/TolerantReader.html. `{r9 | core | verified}` — Names and defines the Tolerant Reader pattern (Postel-style liberal parsing for evolvable integrations); notes Daigneau's Service Design Patterns as the full write-up (bliki loaded live, dated 9 May 2011).
   - elements: tolerant-reader
284. **Scannerless Generalized-LR Parsing** — Eelco Visser, 1997. Technical Report P9707, Programming Research Group, University of Amsterdam. https://eelcovisser.org/publications/1997/Visser97-SGLR.pdf. `{r9 | advanced | verified}` — The SGLR report that made scannerless parsing practical (lexical + context-free syntax in one grammar); confirmed live via Visser's researchr bibliography and eelcovisser.org.
   - elements: scannerless-parsing
285. **ITU-T X.690 - ASN.1 Encoding Rules: BER, CER and DER** — ITU-T, 2021. ITU-T Recommendation X.690 (02/2021). https://www.itu.int/rec/T-REC-X.690. `{r9 | core | verified}` — The standards-grade definition of type-length-value encoding (BER) and of canonical/distinguished encodings (CER/DER) for byte-exact serialization (ITU page loaded live).
   - elements: canonical-serialization, type-length-value-encoding

### Membership (existing works, reclaimed under the element lens)

286. **[MEMBERSHIP id=dwarf5]** `{r9 | advanced | verified}` — Already in corpus (emb passes); pass-8 lens: normatively defines LEB128, the other canonical variable-length integer encoding beside protobuf varints.
   - elements: varint

## R10. Data flow, state & UI/games

### New

287. **Enterprise Integration Patterns: Designing, Building, and Deploying Messaging Solutions** — Gregor Hohpe, Bobby Woolf, 2003. Addison-Wesley. ISBN 0321200683; https://www.enterpriseintegrationpatterns.com/. `{r10 | anchor | verified}` — Names Resequencer (stateful filter that buffers and re-orders out-of-sequence messages); pattern page loaded live on the official EIP site. (also serves r2, r4, r8)
   - elements: aggregator, claim-check, competing-consumers, content-based-router, correlation-identifier, dead-letter-channel, event-driven-consumer, idempotent-receiver, message, message-dispatcher, message-expiration, message-filter, message-queue, message-translator, polling-consumer, publish-subscribe-channel, request-reply, resequencer, return-address, scatter-gather, selective-consumer, splitter, wire-tap
288. **Michael Abrash's Graphics Programming Black Book, Special Edition** — Michael Abrash, 1997. Coriolis; author-blessed free edition on GitHub. https://github.com/jagregory/abrash-black-book. `{r10 | core | verified}` — Ch. 45 'Dog Hair and Dirty Rectangles' is the classic treatment of dirty-rectangle screen updating; chapter loaded live from the edition reproduced with Abrash's blessing.
   - elements: dirty-rectangles
289. **The Dataflow Model: A Practical Approach to Balancing Correctness, Latency, and Cost in Massive-Scale, Unbounded, Out-of-Order Data Processing** — Akidau et al., 2015. PVLDB 8(12), pp. 1792-1803. https://research.google/pubs/the-dataflow-model-a-practical-approach-to-balancing-correctness-latency-and-cost-in-massive-scale-unbounded-out-of-order-data-processing/. `{r10 | core | verified}` — Naming/formalizing paper for the streaming trio — windowing model, triggers, event-time watermarks; verified on the Google Research publication page.
   - elements: event-time-watermark, stream-trigger, stream-windowing
290. **AngularJS Developer Guide: Scopes ($digest and dirty checking)** — Google / AngularJS project, living. docs.angularjs.org (source in angular/angular.js repo; project EOL 2022). https://github.com/angular/angular.js/blob/master/docs/content/guide/scope.ngdoc. `{r10 | core | verified}` — The naming source for dirty checking as a UI change-detection strategy ($digest loop over $watch lists); guide source loaded live from the official repo.
   - elements: dirty-checking
291. **Apollo Client documentation - Optimistic mutation results** — Apollo GraphQL, living. apollographql.com/docs. https://www.apollographql.com/docs/react/performance/optimistic-ui. `{r10 | core | verified}` — The naming doc for optimistic UI updates (render the predicted result, reconcile with the server response); loaded live.
   - elements: optimistic-ui-update
292. **Advanced Programming in the UNIX Environment, 3rd ed.** — W. Richard Stevens, Stephen A. Rago, 2013. Addison-Wesley. ISBN 978-0-321-63773-4. `{r10 | core | verified}` — The standing systems-programming treatment of memory-mapped I/O (mmap) named by Stevens since the 1992 1st ed.; verified on the InformIT publisher page.
   - elements: memory-mapped-file-i-o
293. **Dead Reckoning: Latency Hiding for Networked Games** — Jesse Aronson, 1997. Gamasutra / Game Developer. https://www.gamedeveloper.com/programming/dead-reckoning-latency-hiding-for-networked-games. `{r10 | core | verified}` — The games-side naming article for dead reckoning (extrapolation contracts inherited from DIS military simulation); loaded live.
   - elements: dead-reckoning
294. **A Survey on Reactive Programming** — Bainomugisha, Lombide Carreton, Van Cutsem, Mostinckx, De Meuter, 2013. ACM Computing Surveys 45(4). DOI 10.1145/2501654.2501666. `{r10 | survey | verified}` — The survey that fixes the reactive-programming vocabulary (time-varying values, lifting, glitch avoidance) and situates FRP; verified on the VUB research portal.
   - elements: functional-reactive-programming, reactive-programming
295. **Latency Compensating Methods in Client/Server In-game Protocol Design and Optimization** — Yahn W. Bernier (Valve), 2001. GDC 2001; maintained on the Valve Developer Community wiki. `{r10 | core | unverified}` — The naming source for client-side prediction and lag compensation as implemented in Half-Life/Source. **UNRESOLVED:** primary page — Valve Developer Community returned 403 this session; identifiers from secondary sources.
   - elements: client-side-prediction, lag-compensation
296. **MonetDB/X100: Hyper-Pipelining Query Execution** — Peter Boncz, Marcin Zukowski, Niels Nes, 2005. CIDR 2005. https://www.cidrdb.org/cidr2005/papers/P19.pdf. `{r10 | advanced | verified}` — Origin of vectorized (batch-at-a-time) query execution; PDF loaded live from the official CIDR proceedings host, identity confirmed at that exact URL.
   - elements: vectorized-execution
297. **The lag-fighting techniques behind GGPO's netcode** — Patrick Miller, with Tony Cannon, 2012. Game Developer magazine (Sept 2012); gamedeveloper.com. https://www.gamedeveloper.com/programming/the-lag-fighting-techniques-behind-ggpo-s-netcode. `{r10 | core | verified}` — The canonical published account of GGPO rollback netcode (speculative execution + rollback on mispredicted remote inputs); loaded live — note the article is authored by Miller about Cannon's system.
   - elements: rollback-netcode
298. **Understanding Jitter in Packet Voice Networks (Cisco IOS Platforms)** — Cisco Systems, living. cisco.com technical document 18902. https://www.cisco.com/c/en/us/support/docs/voice/voice-quality/18902-jitter-packet-voice.html. `{r10 | core | verified}` — Vendor-canonical definition of the de-jitter (playout delay) buffer, adaptive vs fixed; content confirmed via live search-fetched quotes (direct fetch 403).
   - elements: jitter-buffer
299. **How we built rate limiting capable of scaling to millions of domains** — Julien Desgats (Cloudflare), 2017. Cloudflare blog. https://blog.cloudflare.com/counting-things-a-lot-of-different-things/. `{r10 | core | verified}` — Production engineering treatment of sliding-window rate limiting (weighted previous+current window counters); upgrade over the interview-prep naming source; loaded live.
   - elements: sliding-window-rate-limiting
300. **Behavior Trees in Robotics and AI: An Introduction** — Michele Colledanchise, Petter Ögren, 2018. Chapman & Hall/CRC. ISBN 9781138593732; arXiv:1709.00084. `{r10 | core | verified}` — The book-length canonical treatment of behavior trees (games origin, robotics formalization); verified on the arXiv record carrying the CRC ISBN/DOI.
   - elements: behavior-tree
301. **Functional Reactive Animation** — Conal Elliott, Paul Hudak, 1997. ICFP 1997. `{r10 | core | unverified}` — The canonical naming paper of FRP (behaviors + events); kept despite verification failure because it is the field's origin point. **UNRESOLVED:** doi — conal.net refused connections and ACM DL returned 403 this session.
   - elements: functional-reactive-programming
302. **Ping Pong Buffers** — Elecia White, 2017. embedded.fm blog. https://embedded.fm/blog/2017/3/21/ping-pong-buffers. `{r10 | core | verified}` — The route's naming treatment for ping-pong buffering (DMA fills one buffer while the other is processed, then swap), by the author of the corpus's embedded anchor; loaded live.
   - elements: ping-pong-buffer
303. **RulesEngine (bliki)** — Martin Fowler, 2009. martinfowler.com. https://martinfowler.com/bliki/RulesEngine.html. `{r10 | core | verified}` — The in-process framing of rules engines (production rules: condition + action objects run over a collection) that keeps the element at design altitude; loaded live.
   - elements: rules-engine
304. **Gaffer On Games (Networked Physics / Game Networking series)** — Glenn Fiedler, living. gafferongames.com. https://gafferongames.com/. `{r10 | core | verified}` — The standing practitioner canon for deterministic lockstep and snapshot interpolation; both articles confirmed live in the Networked Physics series.
   - elements: deterministic-lockstep, snapshot-interpolation
305. **Fast-Paced Multiplayer (Client-Server Game Architecture series)** — Gabriel Gambetta, living. gabrielgambetta.com. https://www.gabrielgambetta.com/client-server-game-architecture.html. `{r10 | core | verified}` — The best modern teaching treatment of client-side prediction, server reconciliation, entity interpolation, and lag compensation, with live demo; loaded live.
   - elements: client-side-prediction, lag-compensation
306. **Volcano - An Extensible and Parallel Query Evaluation System** — Goetz Graefe, 1994. IEEE Transactions on Knowledge and Data Engineering 6(1). `{r10 | advanced | unverified}` — The naming paper of the Volcano open-next-close iterator model of query execution. **UNRESOLVED:** doi — IEEE Xplore and ACM DL both returned 403/empty this session.
   - elements: volcano-iterator-model
307. **Statecharts: A Visual Formalism for Complex Systems** — David Harel, 1987. Science of Computer Programming 8(3). `{r10 | core | unverified}` — The formalism behind the statechart cluster: introduces hierarchy (depth), orthogonality (AND-states), and history entrances that Samek's patterns implement. **UNRESOLVED:** doi — ScienceDirect/ACM DL returned 403 and the author's Weizmann PDF reset repeatedly this session.
   - elements: hierarchical-state-machine, orthogonal-component, transition-to-history
308. **Proving the Correctness of Multiprocess Programs** — Leslie Lamport, 1977. IEEE Transactions on Software Engineering SE-3(2). https://lamport.azurewebsites.net/pubs/pubs.html#proving. `{r10 | advanced | verified}` — Canonical origin of the single-producer/single-consumer lock-free FIFO correctness argument; entry confirmed live on Lamport's own publications page.
   - elements: spsc-lock-free-ring-buffer
309. **Disruptor: High Performance Alternative to Bounded Queues for Exchanging Data Between Concurrent Threads** — Thompson, Farley, Barker, Gee, Stewart, 2011. LMAX technical paper. https://lmax-exchange.github.io/disruptor/disruptor.html. `{r10 | advanced | verified}` — The naming technical paper, loaded live on the official project site; defines the pre-allocated ring-buffer + sequence-barrier mechanism.
   - elements: disruptor
310. **Zero-copy networking** — Jonathan Corbet, 2017. LWN.net. https://lwn.net/Articles/726917/. `{r10 | core | verified}` — Catalog-grade upgrade from the bare Wikipedia naming: kernel-press treatment of zero-copy transmit (MSG_ZEROCOPY, sendfile lineage); loaded live.
   - elements: zero-copy-i-o
311. **FrameGraph: Extensible Rendering Architecture in Frostbite** — Yuriy O'Donnell (EA/Frostbite), 2017. GDC 2017. https://www.gdcvault.com/play/1024612/FrameGraph-Extensible-Rendering-Architecture-in. `{r10 | advanced | verified}` — The naming talk for render/frame graphs (declared render passes + resources compiled into an execution schedule); GDC Vault entry loaded live.
   - elements: render-graph
312. **Pointer Events (W3C specification)** — W3C Pointer Events Working Group, living. w3.org/TR (Level 4 Working Draft loaded; coalescing introduced at Level 2). https://www.w3.org/TR/pointerevents/. `{r10 | core | verified}` — The standards-body naming source for event coalescing (getCoalescedEvents, sec. 'Coalesced and predicted events'); loaded live.
   - elements: event-coalescing
313. **React documentation (react.dev)** — Meta / React team, living. react.dev. https://react.dev/. `{r10 | core | verified}` — Official docs for state-update batching (Queueing a Series of State Updates) and hydration of server-rendered HTML (hydrateRoot); both pages loaded live. (also serves r7)
   - elements: hydration, update-batching, virtual-dom
314. **Reactive Streams Specification** — Reactive Streams initiative, living. reactive-streams.org (v1.0.4, 2022). https://www.reactive-streams.org/. `{r10 | core | verified}` — The standard codification of non-blocking backpressure; its Subscription.request(n) demand protocol is the modern credit-based flow control at design altitude.
   - elements: backpressure, credit-based-flow-control
315. **The Rust Programming Language** — Steve Klabnik, Carol Nichols, living. doc.rust-lang.org (official Rust documentation). https://doc.rust-lang.org/book/ch15-05-interior-mutability.html. `{r10 | core | verified}` — Ch. 15.5 names and teaches the Interior Mutability pattern (RefCell, runtime borrow checking); loaded live. (also serves r7)
   - elements: interior-mutability, newtype, option-type, tagged-union
316. **Streaming Systems: The What, Where, When, and How of Large-Scale Data Processing** — Akidau, Chernyak, Lax, 2018. O'Reilly. `{r10 | core | unverified}` — The book-length modern treatment of the Dataflow Model's windowing/trigger/watermark vocabulary by the same authors. **UNRESOLVED:** isbn — O'Reilly product page and streamingbook.net both unreachable (403/refused) this session.
   - elements: event-time-watermark, stream-trigger, stream-windowing
317. **JavaScript Signals standard proposal (proposal-signals)** — TC39 champions (Rob Eisenberg et al., with framework authors), living. TC39 / GitHub (Stage 1). https://github.com/tc39/proposal-signals. `{r10 | core | verified}` — The cross-framework standardization of fine-grained reactive signals (Signal.State/Computed, auto dependency tracking, glitch-free evaluation); loaded live.
   - elements: reactive-signals
318. **Vue.js documentation - Server-Side Rendering (Client Hydration)** — Vue.js team (Evan You et al.), living. vuejs.org. https://vuejs.org/guide/scaling-up/ssr.html. `{r10 | core | verified}` — The route's naming source for hydration (matching server-rendered DOM and attaching listeners); loaded live.
   - elements: hydration
319. **Batch, Batch, Batch: What Does It Really Mean?** — Matthias Wloka (NVIDIA), 2003. GDC 2003 presentation. https://www.nvidia.com/docs/io/8228/batchbatchbatch.pdf. `{r10 | core | verified}` — The canonical statement of draw-call batching economics (CPU cost per batch dominates); PDF loaded live from nvidia.com, title/author confirmed via fetched quotes.
   - elements: draw-call-batching
320. **Data binding overview (WPF)** — Microsoft, living. learn.microsoft.com. https://learn.microsoft.com/en-us/dotnet/desktop/wpf/data/. `{r10 | core | verified}` — The naming vendor doc for UI data binding (sources/targets, binding modes, update triggers); loaded live.
   - elements: data-binding

### Membership (existing works, reclaimed under the element lens)

321. **[MEMBERSHIP id=douglasspatternsc]** `{r10 | anchor | verified}` — Membership — names and teaches the C state-machine implementation patterns of this route (event receptors, state tables, AND-state decomposition). (also serves r11, r2, r3, r5, r8)
   - elements: critical-region, cyclic-executive, cyclic-redundancy-check, debouncing, decomposed-and-state, dual-channel, fixed-sized-buffer, garbage-collection, guarded-call, hardware-adapter, hardware-proxy, interrupt-masking-critical-section, interrupt-service-routine, message-queue, multiple-event-receptor, one-s-complement-data-storage, ordered-locking, polling, pool-allocation, protected-single-channel, rendezvous, simultaneous-locking, single-event-receptor, smart-data, smart-pointer, state-transition-table, static-allocation, static-priority-scheduling, watchdog
322. **[MEMBERSHIP id=freertosbook]** `{r10 | anchor | verified}` — Membership — the Stream and Message Buffers chapter is the naming/teaching source for the RTOS stream-buffer mechanism. (also serves r2, r3, r5, r8)
   - elements: deferred-interrupt-processing, direct-to-task-notification, event-flags-group, idle-task-hook, interrupt-masking-critical-section, mailbox, message-queue, producer-consumer, scheduler, semaphore, software-timer, stack-painting-watermarking, stream-buffer, system-tick, tickless-idle
323. **[MEMBERSHIP id=hanmer]** `{r10 | anchor | verified}` — Membership — names Fresh Work Before Stale and Shed Load in its overload-handling pattern language. (also serves r2, r3, r6, r8)
   - elements: acknowledgement, checkpointing, complete-parameter-checking, correcting-audits, cyclic-redundancy-check, deferrable-work, error-handler, escalation, fresh-work-before-stale, heartbeat, leaky-bucket-counter, load-shedding, marked-data, quarantine, restart, riding-over-transients, roll-forward, rollback
324. **[MEMBERSHIP id=ldd3]** `{r10 | anchor | verified}` — Membership — ch. 15 (Memory Mapping and DMA) is the standing kernel-side treatment of scatter/gather DMA. (also serves r3, r7)
   - elements: container-of, deferred-interrupt-processing, device-driver, direct-memory-access-dma-transfer, interrupt-coalescing, scatter-gather-dma
325. **[MEMBERSHIP id=nygard]** `{r10 | anchor | verified}` — Membership — Back Pressure and Shed Load are named stability patterns in the 2nd edition; the production-stability framing of this route's overload elements. (also serves r11, r2, r3, r8)
   - elements: backpressure, bulkhead, circuit-breaker, fail-fast, governor, handshaking, let-it-crash, load-shedding, steady-state, timeout
326. **[MEMBERSHIP id=samekbook]** `{r10 | anchor | verified}` — Membership — the statechart-pattern cluster anchor: FSM/HSM implementation, RTC semantics, and the state-pattern mini-catalog (Deferred Event, Reminder, Orthogonal Component, Transition to History, Ultimate Hook) all live here. (also serves r2, r4)
   - elements: active-object, deferred-event, finite-state-machine, hierarchical-state-machine, message-queue, orthogonal-component, publish-subscribe-channel, reminder, run-to-completion-event-processing, state-transition-table, transition-to-history, ultimate-hook
327. **[MEMBERSHIP id=white]** `{r10 | anchor | verified}` — Membership — the corpus's canonical embedded treatment of circular/ring buffers for interrupt-to-mainline data flow. (also serves r3, r6, r8)
   - elements: core-dump, debouncing, direct-memory-access-dma-transfer, interrupt-service-routine, lookup-table, polling, ring-buffer, super-loop, system-tick, watchdog

## R11. Resource management & memory

### New

328. **The Garbage Collection Handbook: The Art of Automatic Memory Management, 2nd ed.** — Richard Jones, Antony Hosking, Eliot Moss, 2023. Chapman and Hall/CRC. DOI 10.1201/9781003276142. `{r11 | anchor | verified}` — The GC canon: tracing vs reference counting, mark-compact, read/write barriers, weak references; anchor for all GC-side elements. Verified via gchandbook.org (official site) + Crossref DOI record (2023-06-01).
   - elements: compaction, garbage-collection, gc-read-barrier, gc-write-barrier, reference-counting, weak-reference
329. **The Slab Allocator: An Object-Caching Kernel Memory Allocator** — Jeff Bonwick, 1994. USENIX Summer 1994 Technical Conference, pp. 87-98. https://www.usenix.org/conference/usenix-summer-1994-technical-conference/slab-allocator-object-caching-kernel-memory. `{r11 | core | verified}` — Naming paper of the slab allocator (SunOS 5.4 object-caching kernel allocator). USENIX page 403s to fetchers; identity verified via dblp record conf/usenix/Bonwick94 (title/author/venue/pages/year).
   - elements: slab-allocator
330. **Simplify Your Exception-Safe Code - Forever (ScopeGuard)** — Andrei Alexandrescu, Petru Marginean, 2000. C/C++ Users Journal, December 2000. https://erdani.org/index.php/articles/. `{r11 | core | verified}` — Naming article of the ScopeGuard idiom (also circulated as the Dr. Dobb's 'Generic<Programming>: Change the Way You Write Exception-Safe Code - Forever'). Verified via Alexandrescu's own article listing at erdani.org.
   - elements: scope-guard
331. **Implement a Dispose method (.NET documentation)** — Microsoft, living. Microsoft Learn. https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/implementing-dispose. `{r11 | core | verified}` — The official living specification of the dispose pattern (IDisposable, Dispose(bool), SafeHandle). Verified via live load of the Microsoft Learn page.
   - elements: dispose-pattern
332. **Practical lock-freedom** — Keir Fraser, 2004. University of Cambridge Computer Laboratory, Technical Report UCAM-CL-TR-579. https://www.cl.cam.ac.uk/techreports/UCAM-CL-TR-579.html. `{r11 | core | verified}` — Naming source of epoch-based reclamation for lock-free data structures. Verified via the Cambridge CL technical-report page (Feb 2004, 116 pp.).
   - elements: epoch-based-reclamation
333. **Game Engine Architecture, 4th ed. (two-volume set)** — Jason Gregory, 2026. CRC Press / Taylor & Francis. ISBN 9781041162599. `{r11 | core | verified}` — The engine text whose concurrency chapters define the fiber-based job system (element named from the 3rd ed's job-system chapter; current edition verified live on gameenginebook.com incl. hardware-parallelism/concurrency coverage) and the frame/game loop. (also serves r4)
   - elements: asset-streaming, custom-allocator, game-loop, job-system, memory-arena, pool-allocation
334. **Hazard Pointers: Safe Memory Reclamation for Lock-Free Objects** — Maged M. Michael, 2004. IEEE Transactions on Parallel and Distributed Systems 15(6), pp. 491-504. DOI 10.1109/TPDS.2004.8. `{r11 | core | verified}` — Canonical naming paper of hazard pointers for safe memory reclamation in lock-free structures. Verified via live doi.org resolution of 10.1109/TPDS.2004.8 + dblp record journals/tpds/Michael04.
   - elements: hazard-pointers
335. **The Design and Evolution of C++** — Bjarne Stroustrup, 1994. Addison-Wesley. ISBN 0-201-54330-3. `{r11 | core | verified}` — Naming source of RAII (resource acquisition is initialization), from the language's designer. Verified via stroustrup.com/dne.html (author's page).
   - elements: raii-resource-acquisition-is-initialization
336. **The Art of Computer Programming, Volume 1: Fundamental Algorithms, 3rd ed.** — Donald E. Knuth, 1997. Addison-Wesley Professional. ISBN 978-0-201-89683-1. `{r11 | core | verified}` — Sec. 2.5 Dynamic Storage Allocation is the naming source of the buddy system and the boundary-tag method. Verified via InformIT publisher page. (also serves r6)
   - elements: boundary-tags, buddy-memory-allocation, deque, linked-list
337. **Optimize control performance (WPF documentation, UI virtualization)** — Microsoft, living. Microsoft Learn. https://learn.microsoft.com/en-us/dotnet/desktop/wpf/advanced/optimizing-performance-controls. `{r11 | core | verified}` — Official doc defining UI/list virtualization and container recycling (VirtualizingStackPanel). Verified via live load of the Microsoft Learn page.
   - elements: list-virtualization

### Membership (existing works, reclaimed under the element lens)

338. **[MEMBERSHIP id=noblesmallmem]** `{r11 | anchor | verified}` — The pattern catalog for constrained-memory design; names and teaches the bulk of this route's small-memory elements. (also serves r6, r7)
   - elements: captain-oates, compaction, compression, copy-on-write, data-files, embedded-pointer, hooks, memory-discard, memory-limit, multiple-representations, packed-data, paging, pool-allocation, read-only-memory, resource-files, sharing, static-allocation, variable-allocation
339. **[MEMBERSHIP id=posa3]** `{r11 | anchor | verified}` — The dedicated resource-management pattern language: acquisition, lifecycle, and release patterns of this route. (also serves r5, r6)
   - elements: caching, coordinator, eager-acquisition, evictor, leasing, lookup, partial-acquisition, pooling, resource-lifecycle-manager
340. **[MEMBERSHIP id=coreguidelines]** `{r11 | core | verified}` — Living canonical treatment of C++ resource-management idioms: RAII (R.1), Rule of Three/Five/Zero (C.20/C.21), smart pointers (R.20+), finally/scope guards (E.19). (also serves r7)
   - elements: include-guard, raii-resource-acquisition-is-initialization, rule-of-three-five-zero, scope-guard, smart-pointer, type-safe-enum
341. **[MEMBERSHIP id=dlmalloc]** `{r11 | core | verified}` — The living essay on general-purpose allocator design; working treatment of boundary tags and binned free lists.
   - elements: boundary-tags, free-list
342. **[MEMBERSHIP id=douglassrtcorpus]** `{r11 | core | verified}` — Real-Time Design Patterns names the embedded memory-pattern set (Fixed Sized Buffer, Pool/Static Allocation, Smart Pointer, Garbage Collection). (also serves r2, r3, r5, r8)
   - elements: dynamic-priority-scheduling, fixed-sized-buffer, garbage-collection, pool-allocation, priority-ceiling-protocol, priority-inheritance-protocol, round-robin-scheduling, sanity-check, scheduler, shared-memory-communication, smart-pointer, static-allocation, static-priority-scheduling, watchdog
343. **[MEMBERSHIP id=eastl]** `{r11 | core | verified}` — Canonical statement of why and how game/embedded C++ replaces standard allocators with custom allocators.
   - elements: custom-allocator
344. **[MEMBERSHIP id=etl]** `{r11 | core | verified}` — Living demonstration of heap-free C++: fixed-capacity containers and etl::pool realize static/pool allocation and fixed-size buffers. (also serves r6)
   - elements: fixed-capacity-container, fixed-sized-buffer, pool-allocation, static-allocation
345. **[MEMBERSHIP id=hanson]** `{r11 | core | verified}` — The Arena chapter is the classic implementable treatment of arena/region allocation in C. (also serves r2, r6, r7, r8)
   - elements: bitmap-bitset, callback, callback-with-context-pointer, dynamic-array, hash-table, linked-list, memory-arena, opaque-pointer, setjmp-longjmp-error-handling, stack
346. **[MEMBERSHIP id=levine]** `{r11 | core | verified}` — Standard treatment of memory overlays as a link-time memory-management mechanism.
   - elements: memory-overlay
347. **[MEMBERSHIP id=tlsf]** `{r11 | core | verified}` — Naming paper of the constant-time two-level segregated fit allocator for real-time systems.
   - elements: two-level-segregated-fit-allocator-tlsf
348. **[MEMBERSHIP id=wilsonsurvey]** `{r11 | survey | verified}` — The allocator-mechanism survey: free lists, boundary tags, buddy systems, segregated fits in one critical review.
   - elements: boundary-tags, buddy-memory-allocation, free-list

## R12. Phase 3 addendum — architecture-catalog naming sources (element ids in this route refer to `architecture_elements_catalog_v1_0.md`)

### New

349. **Big Data: Principles and Best Practices of Scalable Realtime Data Systems** — Nathan Marz, James Warren, 2015. Manning. ISBN 9781617290343. `{r12 | anchor | verified}` — Marz's book-length statement of the Lambda Architecture (batch + speed + serving layers); publisher page loaded live confirming ISBN and year.
   - elements: lambda-architecture
350. **Bitcoin: A Peer-to-Peer Electronic Cash System** — Satoshi Nakamoto, 2008. self-published whitepaper (bitcoin.org). `{r12 | anchor | verified}` — Title/author confirmed live on bitcoin.org (paper page); 31 October 2008 publication confirmed via Satoshi Nakamoto Institute library page.
   - elements: blockchain
351. **Distributed Snapshots: Determining Global States of Distributed Systems** — K. Mani Chandy, Leslie Lamport, 1985. ACM Transactions on Computer Systems 3(1). doi:10.1145/214451.214456. `{r12 | anchor | verified}` — The Chandy-Lamport global-snapshot algorithm. Verified live on Lamport's official publications page; journal/volume/DOI corroborated via Crossref.
   - elements: distributed-snapshot
352. **Chord: A Scalable Peer-to-peer Lookup Service for Internet Applications** — Ion Stoica, Robert Morris, David Karger, M. Frans Kaashoek, Hari Balakrishnan, 2001. ACM SIGCOMM 2001. doi:10.1145/383059.383071. `{r12 | anchor | unverified}` — The canonical distributed-hash-table paper: consistent-hashing ring lookup for peer-to-peer systems. **UNRESOLVED:** UNRESOLVED: publisher page — ACM DL returned 403; title/authors/venue/year/DOI corroborated via Crossref record only (MIT PDOS-hosted PDF served but unparseable this session).
   - elements: distributed-hash-table
353. **The Common Object Request Broker: Architecture and Specification** — Object Management Group (OMG), 1991. OMG standard (CORBA 1.0, August 1991; current 3.4, 2021). `{r12 | anchor | verified}` — Foundational distributed-object middleware standard; defines the OMG Interface Definition Language (IDL). Verified live at omg.org/spec/CORBA (v1.0 Aug 1991, IDL confirmed).
   - elements: interface-definition-language
354. **Model-View-Intent (Cycle.js documentation)** — André Staltz (Cycle.js project), living. cycle.js.org. `{r12 | anchor | verified}` — The canonical statement of the Model-View-Intent reactive UI architecture, in the official Cycle.js docs. Verified live at cycle.js.org/model-view-intent.html.
   - elements: model-view-intent
355. **An Intrusion-Detection Model** — Dorothy E. Denning, 1987. IEEE Transactions on Software Engineering SE-13(2). doi:10.1109/TSE.1987.232894. `{r12 | anchor | unverified}` — The founding paper of intrusion detection: a real-time anomaly-based intrusion-detection expert-system model. **UNRESOLVED:** UNRESOLVED: publisher page — IEEE Xplore page would not render this session; title/author/venue/year/DOI corroborated via Crossref record only.
   - elements: intrusion-detection-system
356. **Architectural Styles and the Design of Network-based Software Architectures** — Roy Thomas Fielding, 2000. PhD dissertation, University of California, Irvine. https://roy.gbiv.com/pubs/dissertation/top.htm. `{r12 | anchor | verified}` — Fielding's dissertation defining REST (Chapter 5) within a systematic derivation of network-based architectural styles; author's own copy loaded live (ics.uci.edu mirror had a TLS error).
   - elements: rest-representational-state-transfer
357. **Flux: In-Depth Overview** — Facebook Open Source. Flux documentation (facebookarchive.github.io/flux). `{r12 | anchor | verified}` — Facebook's official description of the Flux unidirectional-data-flow client architecture (dispatcher, stores, views). Verified live on the archived official docs; the page is undated, so year omitted rather than guessed (Flux announced 2014).
   - elements: flux
358. **Hexagonal Architecture (Ports and Adapters)** — Alistair Cockburn, 2005. alistair.cockburn.us (HaT Technical Report 2005.02). https://alistair.cockburn.us/hexagonal-architecture/. `{r12 | anchor | verified}` — Cockburn's original article naming the hexagonal / ports-and-adapters architecture; loaded live on the author's site (dated 2005-09-04).
   - elements: hexagonal-architecture
359. **Islands Architecture** — Jason Miller, 2020. jasonformat.com. `{r12 | anchor | verified}` — The naming article for the islands frontend architecture (server-rendered pages with independently hydrated interactive regions). Verified live at jasonformat.com/islands-architecture (2020-08-11).
   - elements: islands-architecture
360. **Questioning the Lambda Architecture** — Jay Kreps, 2014. O'Reilly Radar. https://www.oreilly.com/radar/questioning-the-lambda-architecture/. `{r12 | anchor | verified}` — The article that coins the Kappa Architecture as a single-stream-processor alternative to Lambda; loaded live (2014-07-02).
   - elements: kappa-architecture
361. **The Log: What every software engineer should know about real-time data's unifying abstraction** — Jay Kreps, 2013. LinkedIn Engineering blog. `{r12 | anchor | verified}` — LinkedIn Engineering post loaded live (16 December 2013); the canonical essay on the distributed commit log as an architectural backbone.
   - elements: distributed-commit-log
362. **The LMAX Architecture** — Martin Fowler, 2011. martinfowler.com. https://martinfowler.com/articles/lmax.html. `{r12 | anchor | verified}` — Canonical write-up of the LMAX single-threaded business-logic-processor architecture; distinct from the pass-8 Disruptor paper (lmaxdisruptor); loaded live (2011-07-12).
   - elements: lmax-architecture
363. **MapReduce: Simplified Data Processing on Large Clusters** — Jeffrey Dean, Sanjay Ghemawat, 2004. OSDI '04 (USENIX). https://research.google/pubs/mapreduce-simplified-data-processing-on-large-clusters/. `{r12 | anchor | verified}` — The paper that names the MapReduce programming/execution model; Google Research publication page loaded live (USENIX legacy page 403).
   - elements: mapreduce
364. **Micro Frontends** — Cam Jackson, 2019. martinfowler.com. https://martinfowler.com/articles/micro-frontends.html. `{r12 | anchor | verified}` — Canonical article defining micro frontends as independently deliverable frontend applications composed into a whole; loaded live (2019-06-19).
   - elements: micro-frontends
365. **Microservices** — James Lewis, Martin Fowler, 2014. martinfowler.com. https://martinfowler.com/articles/microservices.html. `{r12 | anchor | verified}` — The defining article of the microservice architectural style (nine characteristics); loaded live (2014-03-25).
   - elements: microservices
366. **What's a service mesh? And why do I need one?** — William Morgan, 2017. Buoyant blog (buoyant.io). `{r12 | anchor | unverified}` — The article that defined and popularized the term 'service mesh' (sidecar-proxy infrastructure layer for service-to-service communication). **UNRESOLVED:** UNRESOLVED: exact original title/URL — original buoyant.io/2017/04/25 URL retired (404); author, April 2017 date, and Buoyant origin confirmed live via CNCF republication (cncf.io blog, 2017-04-26, 'Service mesh: A critical component of the cloud native stack', credited 'originally published by William Morgan on Buoyant.io').
   - elements: service-mesh
367. **Zero Trust Architecture (NIST SP 800-207)** — Scott Rose, Oliver Borchert, Stu Mitchell, Sean Connelly, 2020. NIST Special Publication 800-207. DOI 10.6028/NIST.SP.800-207. `{r12 | anchor | verified}` — The NIST standard defining zero trust architecture (tenets, logical components, deployment models); csrc.nist.gov publication page loaded live confirming DOI and August 2020 date.
   - elements: zero-trust-architecture
368. **Microservices Patterns: With Examples in Java** — Chris Richardson, 2018. Manning Publications. isbn:9781617294549. `{r12 | anchor | verified}` — The canonical microservices pattern book (44 patterns incl. Health Check API and Log Aggregation); title/author/year/ISBN verified live on the Manning product page.
   - elements: health-check-api, log-aggregation
369. **Sagas** — Hector Garcia-Molina, Kenneth Salem, 1987. ACM SIGMOD 1987. doi:10.1145/38713.38742. `{r12 | anchor | unverified}` — Origin paper of the saga long-lived-transaction pattern, the canonical citation behind microservice sagas. **UNRESOLVED:** UNRESOLVED: ACM DL returned 403 this session; title/authors/venue/DOI corroborated via Crossref record only..
   - elements: saga
370. **SEDA: An Architecture for Well-Conditioned, Scalable Internet Services** — Matt Welsh, David Culler, Eric Brewer, 2001. SOSP '01. DOI 10.1145/502034.502057. `{r12 | anchor | unverified}` — The paper that names the staged event-driven architecture (SEDA): stages connected by explicit event queues with per-stage dynamic resource control. **UNRESOLVED:** UNRESOLVED: DOI — ACM DL returned 403; DOI 10.1145/502034.502057, authors, venue, year and pages 230-243 corroborated via dblp only..
   - elements: seda-staged-event-driven-architecture
371. **The Case for Shared Nothing** — Michael Stonebraker, 1986. IEEE Database Engineering Bulletin 9(1). `{r12 | anchor | unverified}` — Stonebraker's classic argument that shared-nothing multiprocessor architecture dominates shared-memory and shared-disk for scalable database systems. **UNRESOLVED:** UNRESOLVED: no DOI exists and no primary page loaded — venue, volume 9(1), pages 4-9 and year corroborated via dblp; the Berkeley-hosted PDF (dsf.berkeley.edu/papers/hpts85-nothing.pdf) was not text-extractable..
   - elements: shared-nothing-architecture
372. **A Robust Layered Control System for a Mobile Robot** — Rodney A. Brooks, 1986. IEEE Journal of Robotics and Automation 2(1). DOI 10.1109/JRA.1986.1087032. `{r12 | anchor | verified}` — The paper introducing the subsumption architecture (layered behavior-based robot control); Brooks's MIT CSAIL publication page loaded live confirming journal, vol 2 no 1, March 1986, pp 14-23; DOI corroborated via dblp (IEEE Xplore page rendered blank).
   - elements: subsumption-architecture
373. **CQRS Documents** — Greg Young, 2010. Self-published (cqrs.wordpress.com). `{r12 | anchor | verified}` — Young's defining treatment of Command Query Responsibility Segregation (plus events-as-storage); originated as a class manual. Verified live at cqrs.wordpress.com/documents (Greg Young, 2010).
   - elements: cqrs
374. **The Art of Scalability: Scalable Web Architecture, Processes, and Organizations for the Modern Enterprise, 2nd ed.** — Martin L. Abbott, Michael T. Fisher, 2015. Addison-Wesley Professional. isbn:9780134032801. `{r12 | core | verified}` — Origin of the AKF scale cube (X/Y/Z-axis scaling); 1st ed. 2009, 2nd ed. 2015 verified live on the InformIT (Pearson) product page.
   - elements: scale-cube
375. **Reducing the Scope of Impact with Cell-Based Architecture** — Amazon Web Services, 2023. AWS Well-Architected guidance. `{r12 | core | verified}` — AWS Well-Architected guidance (publication date September 20, 2023, confirmed live) canonizing cell-based architecture as workload-level fault isolation.
   - elements: cell-based-architecture
376. **Autoscaling Guidance — Azure Architecture Center** — Microsoft (Azure Architecture Center), living. learn.microsoft.com. `{r12 | core | verified}` — Cloud-vendor canonical treatment of auto-scaling (horizontal vs vertical, metrics-driven rules, flapping); verified live; AWS Auto Scaling docs are the parallel treatment.
   - elements: auto-scaling
377. **Design Patterns for Container-based Distributed Systems** — Brendan Burns, David Oppenheimer, 2016. 8th USENIX Workshop on Hot Topics in Cloud Computing (HotCloud '16). `{r12 | core | verified}` — Names the sidecar/ambassador/adapter single-node container patterns; verified live via the authors' Google Research publication page (USENIX page 403'd).
   - elements: adapter-container, os-container
378. **Enterprise Service Bus** — David A. Chappell, 2004. O'Reilly Media. isbn:9780596006754. `{r12 | core | unverified}` — The book that defined and popularized the enterprise service bus as an integration architecture. **UNRESOLVED:** UNRESOLVED: O'Reilly publisher page 403'd this session; title/author/year/ISBN corroborated via Open Library record only.
   - elements: enterprise-service-bus
379. **Core Security Patterns: Best Practices and Strategies for J2EE, Web Services, and Identity Management** — Christopher Steel, Ramesh Nagappan, Ray Lai, 2005. Prentice Hall (Pearson). ISBN 978-0-13-146307-3. `{r12 | core | verified}` — Publisher (InformIT/Pearson) page loaded live confirming title, authors, 2005 publication, ISBN; catalogs Single Sign-On among its security patterns.
   - elements: single-sign-on
380. **Cortex-R5 and Cortex-R5F Technical Reference Manual** — Arm Ltd., 2011. Arm developer documentation. Arm DDI 0460. `{r12 | core | unverified}` — Arm's processor reference manual documenting the twin-CPU redundant (dual-core lock-step) configuration for functional-safety systems. **UNRESOLVED:** UNRESOLVED: year/revision and live title — developer.arm.com pages are JS-rendered and would not load content this session; doc id DDI 0460 = Cortex-R5 (and Cortex-R5F) TRM corroborated via Arm developer search listings only.
   - elements: dual-core-lockstep
381. **How to Move Beyond a Monolithic Data Lake to a Distributed Data Mesh** — Zhamak Dehghani, 2019. martinfowler.com. `{r12 | core | verified}` — Article loaded live (20 May 2019); the piece that introduced and named the data mesh paradigm.
   - elements: data-mesh
382. **DO-297 — Integrated Modular Avionics (IMA) Development Guidance and Certification Considerations** — RTCA SC-200, 2005. RTCA, Inc.. `{r12 | core | unverified}` — The IMA certification standard contrasting integrated modular avionics with federated architectures (EUROCAE equivalent ED-124). **UNRESOLVED:** UNRESOLVED: RTCA store loaded live confirms DO-297 exists as a product, but full title and 2005 issue date were not displayed; ANSI/GlobalSpec aggregator pages 403'd.
   - elements: federated-avionics-architecture, integrated-modular-avionics
383. **DPDK Programmer's Guide** — DPDK Project (Linux Foundation), living. doc.dpdk.org. `{r12 | core | verified}` — Canonical documentation of user-space, kernel-bypass packet processing (poll-mode drivers, hugepage memory). Verified live at doc.dpdk.org/guides/prog_guide.
   - elements: kernel-bypass-networking
384. **The Elm Architecture (An Introduction to Elm, official guide)** — Evan Czaplicki, living. guide.elm-lang.org. `{r12 | core | verified}` — Official Elm guide chapter loaded live (Model/View/Update); authorship confirmed via the evancz/guide.elm-lang.org source repository.
   - elements: the-elm-architecture
385. **What do you mean by 'Event-Driven'?** — Martin Fowler, 2017. martinfowler.com. `{r12 | core | verified}` — Disambiguates four event-driven patterns; names Event-Carried State Transfer. Verified live at martinfowler.com/articles/201701-event-driven.html (2017-02-07).
   - elements: event-carried-state-transfer
386. **PolyglotPersistence (bliki)** — Martin Fowler, 2011. martinfowler.com bliki. `{r12 | core | verified}` — Bliki entry loaded live (dated 16 November 2011); names the polyglot-persistence data-architecture stance.
   - elements: polyglot-persistence
387. **ReportingDatabase (bliki)** — Martin Fowler, 2004. martinfowler.com bliki. `{r12 | core | verified}` — Bliki entry loaded live (originally 2 April 2004, later updated); names the separate read-optimized reporting database.
   - elements: reporting-database
388. **Introduction to Model/View/ViewModel pattern for building WPF apps** — John Gossman, 2005. Microsoft (MSDN blog, archived at learn.microsoft.com). `{r12 | core | verified}` — The post that named MVVM (2005-10-08); archived Microsoft Learn page loaded live confirming title, author, and date.
   - elements: model-view-viewmodel
389. **TEE System Architecture** — GlobalPlatform, living. GlobalPlatform Technology specification. GPD_SPE_009 v1.3 (May 2022). `{r12 | core | verified}` — GlobalPlatform specs-library page loaded live confirming document id GPD_SPE_009 v1.3; defines the Trusted Execution Environment hardware/software architecture.
   - elements: trusted-execution-environment
390. **IEEE Standard for Modeling and Simulation (M&S) High Level Architecture (HLA) — Framework and Rules** — IEEE, 2010. IEEE Standards Association. IEEE 1516-2010. `{r12 | core | verified}` — standards.ieee.org page loaded live; capstone of the HLA standards family defining federates/federations. Now inactive-reserved, superseded by IEEE 1516-2025.
   - elements: hla-federation
391. **ImmutableServer** — Kief Morris, 2013. martinfowler.com bliki. `{r12 | core | verified}` — The bliki entry (13 June 2013, confirmed live) naming the immutable-server/immutable-infrastructure practice; expanded in Morris's Infrastructure as Code (2016).
   - elements: immutable-infrastructure
392. **Kubernetes Documentation — Deployments** — The Kubernetes Authors (CNCF), living. kubernetes.io. `{r12 | core | verified}` — Official Deployment controller docs (RollingUpdate strategy, maxSurge/maxUnavailable, rollout/rollback), the de facto canonical treatment of rolling deployment; verified live.
   - elements: rolling-deployment
393. **Towards a Taxonomy of Software Connectors** — Nikunj R. Mehta, Nenad Medvidovic, Sandeep Phadke, 2000. ICSE 2000 (Proceedings of the 22nd International Conference on Software Engineering), pp. 178-187. doi:10.1145/337180.337201. `{r12 | core | unverified}` — The connector taxonomy paper — classifies software connectors into service categories (procedure call, event, data access, stream, linkage, distributor, arbitrator, adaptor) that TMD later canonized. **UNRESOLVED:** UNRESOLVED: ACM DL 403 this session; title/authors/year/pages/DOI corroborated via dblp record only.
   - elements: adaptor-connector, arbitrator-connector, data-access-connector, distributor-connector, event-connector, linkage-connector, procedure-call-connector, stream-connector
394. **microservices.io — A Pattern Language for Microservices** — Chris Richardson, living. microservices.io. `{r12 | core | verified}` — Living pattern-language site verified live (pattern index confirms API Composition, API Gateway, Database per Service, Distributed Tracing, Monolithic Architecture, Transactional Outbox); companion to the Microservices Patterns book.
   - elements: api-composition, api-gateway, database-per-service, distributed-tracing, monolithic-architecture, transactional-outbox
395. **Monolith to Microservices: Evolutionary Patterns to Transform Your Monolith** — Sam Newman, 2019. O'Reilly. ISBN 9781492047841. `{r12 | core | unverified}` — Newman's decomposition patterns book; names the modular monolith as an explicit architectural option and migration target. **UNRESOLVED:** UNRESOLVED: ISBN/year — O'Reilly publisher page 403; title/author/publisher confirmed on samnewman.io (author site), ISBN 9781492047841 and 2019 corroborated via OpenLibrary only..
   - elements: modular-monolith
396. **MVP: Model-View-Presenter — The Taligent Programming Model for C++ and Java** — Mike Potel, 1996. Taligent, Inc. (technical paper). `{r12 | core | verified}` — Naming source of Model-View-Presenter; primary PDF loaded live from the author's site (wildcrest.com), first page confirms title/author/1996 Taligent copyright.
   - elements: model-view-presenter
397. **Serverless Architectures** — Mike Roberts, 2018. martinfowler.com. `{r12 | core | verified}` — The canonical long-form treatment of serverless/FaaS vs BaaS; first published 2016, live page carries the revised edition dated 22 May 2018 (confirmed live).
   - elements: serverless-function-as-a-service
398. **UNIX Network Programming, Volume 1: The Sockets Networking API, 3rd ed.** — W. Richard Stevens, Bill Fenner, Andrew M. Rudoff, 2003. Addison-Wesley Professional. isbn:9780131411555. `{r12 | core | verified}` — Canonical sockets text whose server-design chapter defines the iterative/thread-per-connection/preforked/prethreaded server architectures; verified live on the InformIT (Pearson) product page.
   - elements: preforked-prethreaded-server, thread-per-connection-server
399. **eXtensible Access Control Markup Language (XACML) Version 3.0** — OASIS XACML Technical Committee, 2013. OASIS Standard. OASIS xacml-3.0-core-spec-os-en (22 January 2013). `{r12 | core | verified}` — OASIS spec loaded live; glossary defines Policy Decision Point and Policy Enforcement Point (terminology lineage: IETF RFC 2753 / ISO 10181-3).
   - elements: policy-decision-point-policy-enforcement-point

---

## Unverified quarantine

Real, on-scope, but not primary-confirmed this session — do not cite the soft field downstream without live verification.

- **Mixin-Based Inheritance** — Gilad Bracha, William Cook, 1990. **UNRESOLVED:** doi/primary page — ACM DL 403 and bracha.org paper page 404 this session; DOI omitted rather than guessed. elements: mixin
- **Building Domain-Specific Embedded Languages** — Paul Hudak, 1996. **UNRESOLVED:** doi — ACM DL returned 403 this session; DOI omitted rather than guessed. elements: embedded-domain-specific-language
- **A Simple Technique for Handling Multiple Polymorphism** — Daniel H. H. Ingalls, 1986. **UNRESOLVED:** doi/primary page — ACM DL 403 this session and no author-hosted copy found; citation from route file. elements: double-dispatch
- **Specifications** — Eric Evans, Martin Fowler, 1997. **UNRESOLVED:** year/venue — the hosted PDF downloaded live but is password-protected and unreadable this session; citation from route file. elements: specification
- **Virtuality** — Herb Sutter, 2001. **UNRESOLVED:** live page — gotw.ca failed TLS handshake this session and archive fetch is blocked; citation from route file. elements: non-virtual-interface-nvi
- **Latency Compensating Methods in Client/Server In-game Protocol Design and Optimization** — Yahn W. Bernier (Valve), 2001. **UNRESOLVED:** primary page — Valve Developer Community returned 403 this session; identifiers from secondary sources. elements: client-side-prediction, lag-compensation
- **Functional Reactive Animation** — Conal Elliott, Paul Hudak, 1997. **UNRESOLVED:** doi — conal.net refused connections and ACM DL returned 403 this session. elements: functional-reactive-programming
- **Volcano - An Extensible and Parallel Query Evaluation System** — Goetz Graefe, 1994. **UNRESOLVED:** doi — IEEE Xplore and ACM DL both returned 403/empty this session. elements: volcano-iterator-model
- **Statecharts: A Visual Formalism for Complex Systems** — David Harel, 1987. **UNRESOLVED:** doi — ScienceDirect/ACM DL returned 403 and the author's Weizmann PDF reset repeatedly this session. elements: hierarchical-state-machine, orthogonal-component, transition-to-history
- **Streaming Systems: The What, Where, When, and How of Large-Scale Data Processing** — Akidau, Chernyak, Lax, 2018. **UNRESOLVED:** isbn — O'Reilly product page and streamingbook.net both unreachable (403/refused) this session. elements: event-time-watermark, stream-trigger, stream-windowing
- **Domain-Driven Design Reference: Definitions and Pattern Summaries** — Eric Evans, 2015. **UNRESOLVED:** primary page (domainlanguage.com) returned HTTP 403 this session; title/year carried from the Phase-1 catalog, not re-confirmed live. elements: domain-event
- **AUTOSAR Classic Platform — Specification of Operating System (SWS OS)** — AUTOSAR consortium, living. **UNRESOLVED:** live page — autosar.org failed TLS verification this session; current release identifier not confirmed. elements: schedule-table
- **Interval Analysis** — Ramon E. Moore, 1966. **UNRESOLVED:** primary page not loadable this session; no ISBN cited. elements: interval-arithmetic
- **Threaded Code** — James R. Bell, 1973. **UNRESOLVED:** doi/pages — ACM DL Cloudflare-blocked this session; citation cross-checked only via Ertl's academic threaded-code bibliography (bell73, CACM, received June). elements: threaded-code
- **Promises: Linguistic Support for Efficient Asynchronous Procedure Calls in Distributed Systems** — Liskov, Shrira, 1988. **UNRESOLVED:** doi/pages — ACM DL Cloudflare-blocked and PMG CSAIL unreachable this session; identifier not confirmed against a primary page. elements: future-promise
- **AN2594: EEPROM emulation in STM32F10x microcontrollers** — STMicroelectronics, living. **UNRESOLVED:** url (st.com fetch timed out this session). elements: eeprom-emulation-in-flash
- **Space/Time Trade-offs in Hash Coding with Allowable Errors** — Burton H. Bloom, 1970. **UNRESOLVED:** doi. elements: bloom-filter
- **Ropes: an Alternative to Strings** — Boehm, Atkinson & Plass, 1995. **UNRESOLVED:** doi. elements: rope
- **An Efficient Representation for Sparse Sets** — Preston Briggs & Linda Torczon, 1993. **UNRESOLVED:** doi. elements: sparse-set
- **A Survey of Flash Translation Layer** — Chung, Park, Park, Lee, Lee & Song, 2009. **UNRESOLVED:** doi. elements: flash-translation-layer, flash-wear-leveling
- **Computational Geometry: Algorithms and Applications, 3rd ed.** — de Berg, Cheong, van Kreveld & Overmars, 2008. **UNRESOLVED:** isbn. elements: interval-tree, k-d-tree, segment-tree
- **Efficient Implementation of the Smalltalk-80 System** — L. Peter Deutsch & Allan M. Schiffman, 1984. **UNRESOLVED:** doi. elements: inline-caching
- **A New Data Structure for Cumulative Frequency Tables** — Peter M. Fenwick, 1994. **UNRESOLVED:** doi. elements: fenwick-tree
- **R-Trees: A Dynamic Index Structure for Spatial Searching** — Antonin Guttman, 1984. **UNRESOLVED:** doi. elements: r-tree
- **Consistent Hashing and Random Trees: Distributed Caching Protocols for Relieving Hot Spots on the World Wide Web** — Karger, Lehman, Leighton, Panigrahy, Levine & Lewin, 1997. **UNRESOLVED:** doi. elements: consistent-hashing
- **Physical Integrity in a Large Segmented Database** — Raymond A. Lorie, 1977. **UNRESOLVED:** doi. elements: shadow-paging
- **A Digital Signature Based on a Conventional Encryption Function** — Ralph C. Merkle, 1987. **UNRESOLVED:** doi. elements: merkle-tree
- **'Memo' Functions and Machine Learning** — Donald Michie, 1968. **UNRESOLVED:** doi. elements: memoization
- **AI for Games, 3rd ed.** — Ian Millington, 2019. **UNRESOLVED:** isbn. elements: navigation-mesh
- **Improved Query Performance with Variant Indexes** — Patrick O'Neil & Dallan Quass, 1997. **UNRESOLVED:** doi. elements: bitmap-index
- **Skip Lists: A Probabilistic Alternative to Balanced Trees** — William Pugh, 1990. **UNRESOLVED:** doi. elements: skip-list
- **Real-Time Rendering, 4th ed.** — Akenine-Möller, Haines & Hoffman, 2018. **UNRESOLVED:** isbn. elements: bounding-volume-hierarchy, quadtree-octree, scene-graph
- **Conflict-free Replicated Data Types** — Shapiro, Preguica, Baquero & Zawirski, 2011. **UNRESOLVED:** doi. elements: conflict-free-replicated-data-type-crdt
- **Representing Type Information in Dynamically Typed Languages** — David Gudeman, 1993. **UNRESOLVED:** primary page (UA TR archive not loadable; identity corroborated via citing literature only). elements: pointer-tagging
- **Error Detecting and Error Correcting Codes** — Richard W. Hamming, 1950. **UNRESOLVED:** doi/primary page (IEEE/Wiley archive not loadable this session). elements: error-correcting-codes
- **Thunks: A Way of Compiling Procedure Statements with Some Comments on Procedure Declarations** — P. Z. Ingerman, 1961. **UNRESOLVED:** doi (ACM DL blocked this session). elements: thunk
- **Domain Specific Embedded Compilers** — Daan Leijen, Erik Meijer, 1999. **UNRESOLVED:** primary page (USENIX pages returned 403 this session; listing seen in search index only). elements: phantom-type
- **The New C: X Macros** — Randy Meyers, 2001. **UNRESOLVED:** primary page (CUJ/Dr. Dobb's defunct; archived full text at jacobfilipp.com/DrDobbs loaded live this session). elements: x-macro
- **Typestate: A Programming Language Concept for Enhancing Software Reliability** — Robert E. Strom, Shaula Yemini, 1986. **UNRESOLVED:** doi/primary page (IEEE Xplore not loadable this session). elements: typestate
- **Pointer Swizzling at Page Fault Time: Efficiently and Compatibly Supporting Huge Address Spaces on Standard Hardware** — Paul R. Wilson, Sheetal V. Kakkad, 1992. **UNRESOLVED:** doi/primary page (only aggregator copies located this session). elements: pointer-swizzling
- **The N-Version Approach to Fault-Tolerant Software** — Algirdas Avizienis, 1985. **UNRESOLVED:** primary DL page (dl.acm.org/IEEE returned 403; DOI taken from the ACM DL link surfaced in search, not a loaded page). elements: n-version-programming
- **Timeouts, Retries, and Backoff with Jitter (Amazon Builders' Library)** — Marc Brooker, living. **UNRESOLVED:** live primary page (URL 301s to builder.aws.com, which renders client-side; article content could not be loaded this session). elements: retry-budget, retry-with-exponential-backoff-and-jitter, timeout
- **Software Rejuvenation: Analysis, Module and Applications** — Yennun Huang, Chandra Kintala, Nick Kolettis, N. Dudley Fulton, 1995. **UNRESOLVED:** doi + primary DL page (IEEE Xplore not loaded this session; venue/pages from search indexes). elements: software-rejuvenation
- **Preventing Privilege Escalation** — Niels Provos, Markus Friedl, Peter Honeyman, 2003. **UNRESOLVED:** live primary page (usenix.org returned 403 on all paper URLs; citi.umich.edu unreachable this session). elements: privilege-separation
- **System Structure for Software Fault Tolerance** — Brian Randell, 1975. **UNRESOLVED:** doi + primary DL page (IEEE/ACM pages returned 403 this session). elements: recovery-blocks
- **StackGuard: Automatic Adaptive Detection and Prevention of Buffer-Overflow Attacks** — Crispin Cowan et al., 1998. **UNRESOLVED:** live primary page (usenix.org returned 403). elements: stack-canary
- **Consistent Overhead Byte Stuffing** — Stuart Cheshire, Mary Baker, 1999. **UNRESOLVED:** doi. elements: byte-stuffing, consistent-overhead-byte-stuffing
- **On the Translation of Languages from Left to Right** — Donald E. Knuth, 1965. **UNRESOLVED:** doi. elements: lr-parser
- **Prettyprinting** — Derek C. Oppen, 1980. **UNRESOLVED:** doi. elements: pretty-printer
- **Enforcing Strict Model-View Separation in Template Engines** — Terence Parr, 2004. **UNRESOLVED:** doi. elements: template-engine
- **Top Down Operator Precedence** — Vaughan R. Pratt, 1973. **UNRESOLVED:** doi. elements: pratt-parser
- **Programming Techniques: Regular Expression Search Algorithm** — Ken Thompson, 1968. **UNRESOLVED:** doi. elements: regular-expressions
- **Towards a Taxonomy of Software Connectors** — Nikunj R. Mehta, Nenad Medvidovic, Sandeep Phadke, 2000. **UNRESOLVED:** UNRESOLVED: ACM DL 403 this session; title/authors/year/pages/DOI corroborated via dblp record only. elements: adaptor-connector, arbitrator-connector, data-access-connector, distributor-connector, event-connector, linkage-connector, procedure-call-connector, stream-connector
- **DO-297 — Integrated Modular Avionics (IMA) Development Guidance and Certification Considerations** — RTCA SC-200, 2005. **UNRESOLVED:** UNRESOLVED: RTCA store loaded live confirms DO-297 exists as a product, but full title and 2005 issue date were not displayed; ANSI/GlobalSpec aggregator pages 403'd. elements: federated-avionics-architecture, integrated-modular-avionics
- **Enterprise Service Bus** — David A. Chappell, 2004. **UNRESOLVED:** UNRESOLVED: O'Reilly publisher page 403'd this session; title/author/year/ISBN corroborated via Open Library record only. elements: enterprise-service-bus
- **What's a service mesh? And why do I need one?** — William Morgan, 2017. **UNRESOLVED:** UNRESOLVED: exact original title/URL — original buoyant.io/2017/04/25 URL retired (404); author, April 2017 date, and Buoyant origin confirmed live via CNCF republication (cncf.io blog, 2017-04-26, 'Service mesh: A critical component of the cloud native stack', credited 'originally published by William Morgan on Buoyant.io'). elements: service-mesh
- **Chord: A Scalable Peer-to-peer Lookup Service for Internet Applications** — Ion Stoica, Robert Morris, David Karger, M. Frans Kaashoek, Hari Balakrishnan, 2001. **UNRESOLVED:** UNRESOLVED: publisher page — ACM DL returned 403; title/authors/venue/year/DOI corroborated via Crossref record only (MIT PDOS-hosted PDF served but unparseable this session). elements: distributed-hash-table
- **Cortex-R5 and Cortex-R5F Technical Reference Manual** — Arm Ltd., 2011. **UNRESOLVED:** UNRESOLVED: year/revision and live title — developer.arm.com pages are JS-rendered and would not load content this session; doc id DDI 0460 = Cortex-R5 (and Cortex-R5F) TRM corroborated via Arm developer search listings only. elements: dual-core-lockstep
- **An Intrusion-Detection Model** — Dorothy E. Denning, 1987. **UNRESOLVED:** UNRESOLVED: publisher page — IEEE Xplore page would not render this session; title/author/venue/year/DOI corroborated via Crossref record only. elements: intrusion-detection-system
- **Sagas** — Hector Garcia-Molina, Kenneth Salem, 1987. **UNRESOLVED:** UNRESOLVED: ACM DL returned 403 this session; title/authors/venue/DOI corroborated via Crossref record only.. elements: saga
- **Monolith to Microservices: Evolutionary Patterns to Transform Your Monolith** — Sam Newman, 2019. **UNRESOLVED:** UNRESOLVED: ISBN/year — O'Reilly publisher page 403; title/author/publisher confirmed on samnewman.io (author site), ISBN 9781492047841 and 2019 corroborated via OpenLibrary only.. elements: modular-monolith
- **SEDA: An Architecture for Well-Conditioned, Scalable Internet Services** — Matt Welsh, David Culler, Eric Brewer, 2001. **UNRESOLVED:** UNRESOLVED: DOI — ACM DL returned 403; DOI 10.1145/502034.502057, authors, venue, year and pages 230-243 corroborated via dblp only.. elements: seda-staged-event-driven-architecture
- **The Case for Shared Nothing** — Michael Stonebraker, 1986. **UNRESOLVED:** UNRESOLVED: no DOI exists and no primary page loaded — venue, volume 9(1), pages 4-9 and year corroborated via dblp; the Berkeley-hosted PDF (dsf.berkeley.edu/papers/hpts85-nothing.pdf) was not text-extractable.. elements: shared-nothing-architecture

## Element-coverage audit

| axis | elements | covered | avg works/element |
|---|---|---|---|
| caching-memoization | 16 | 16 | 1.4 |
| code-structure | 11 | 11 | 1.5 |
| communication | 44 | 44 | 1.3 |
| construction-api | 29 | 29 | 1.1 |
| data-flow-buffering | 28 | 28 | 1.2 |
| data-representation | 33 | 33 | 1.3 |
| data-structures | 52 | 52 | 1.5 |
| embedded-systems | 16 | 15 | 1.5 |
| error-handling | 50 | 50 | 1.4 |
| execution-concurrency | 37 | 37 | 1.5 |
| functional-type-idioms | 26 | 26 | 1.5 |
| numeric-precision | 10 | 10 | 1.3 |
| oo-patterns | 65 | 63 | 1.8 |
| parsing-text | 20 | 20 | 1.6 |
| persistence-durability | 29 | 29 | 1.3 |
| resource-management | 56 | 56 | 1.4 |
| robustness-security | 40 | 40 | 1.3 |
| scheduling-time | 25 | 25 | 1.7 |
| serialization-framing | 21 | 21 | 1.3 |
| state-management | 33 | 33 | 1.3 |
| synchronization-coordination | 57 | 57 | 1.6 |
| testing-constructs | 11 | 11 | 1.4 |
| **total** | **709** | **706** | **1.4** |

### Unreachable elements (explicit gaps)

- `multiton` (oo-patterns) — Named only in Wikipedia's pattern list and blog posts; not in GoF (which offers only the 'registry of singletons' remark), Refactoring.Guru, SourceMaking, PoEAA, or any book/paper found this session. No catalog-grade treatment exists; candidate for aka-fold into singleton commentary or an editorial-tagged entry.
- `servant` (oo-patterns) — Named in Wikipedia; the originating source is Pecinovsky et al.'s design-patterns-first teaching papers (~2006), which treat it only as a pedagogy example, and the remaining treatments are community sites (java-design-patterns.com). No catalog-grade book/paper/official-doc treatment found this session.
- `shadow-register` (embedded-systems) — Named only in vendor knowledge-base pages (Infineon write-only-register shadow-copy KB, Microchip PIC shadow registers) and ScienceDirect topic aggregations; no catalog-grade book/paper/standard treatment surfaced after a live search this session. Best upgrade candidates are MCU family reference manuals (official-doc grade, per-part rather than general); recorded as a gap rather than padded.

## Coverage summary — where recall thins (honest gaps)

- **The membership layer confirms the corpus's center of gravity.** 63 existing works are reclaimed under the element lens, and the heaviest are the embedded canon: `douglasspatternsc`, `noblesmallmem`, `posa2`/`posa3`, `white`, `koopmanbess`, `pont`, `freertosbook`, `samekbook`, `hanmer`, `preschern(+plop)`, `hanson`, `tornhill`, `iglberger`, `coreguidelines`. The element layer did not import a foreign literature — it made explicit what the corpus already taught.
- **The 285 new nodes are dominated by two shapes**: (a) the missing catalog anchors — PoEAA, EIP, Meszaros, JCiP, Lea, Mattson, Herlihy–Shavit, perfbook, CLRS, Kleppmann, Petrov, Nystrom (both books), Gregory, GC Handbook, Dragon Book, Evans — each covering 5–30 elements; and (b) the canonical naming-paper tail (Bloom, Karger, Pugh, Merkle, MCS, Kung–Robinson, Harel, Hölzle, Chambers–Ungar, Reynolds, Moggi, Ellis–Gibbs, …), kept only where a treatment book does not genuinely teach the element or the paper is itself canon.
- **Digital-library bot-blocking is the one systematic verification hole.** ACM DL, IEEE Xplore, USENIX, Elsevier, Wiley and O'Reilly 403'd fetches throughout the session; the 52 unverified new nodes are almost all canonical papers whose identifiers therefore rest on dblp/Crossref/author-page corroboration, with the soft field named per entry (no identifier was guessed). The most exposed single case is `huangrejuv` (software-rejuvenation's only covering work). Verified status was earned via publisher pages, standards bodies (rfc-editor, ITU, WG14, IEEE SA), official project sites, and author-hosted primary texts.
- **Living docs are load-bearing for two domains** — UI/reactive (React docs, WPF/Microsoft Learn, Qt, TC39 proposal, ReactiveX, Apollo) and RTOS mechanism vocabulary (FreeRTOS book/site, Zephyr-adjacent vendor docs) name and teach mechanisms no book treats at catalog grade. This mirrors pass 7's finding that language-specific knowledge lives in tooling docs; here, framework-specific mechanism vocabulary lives in framework docs.
- **Coverage shape**: 472 of 705 covered elements are single-covered — deliberate economy (one catalog-grade treatment suffices per the mapping rule), concentrated in the idiom/paper tail. 233 elements carry ≥2 works (naming source + modern treatment pairing, per the mission's "best modern treatments" rule).
- **Three elements end unreachable** (the explicit-gap rule, not padding): `multiton` and `servant` (community-named OO long tail — named at title level per Phase 1's gate, but no catalog-grade treatment exists beyond wiki/tutorial sites) and `shadow-register` (vendor-KB vocabulary). They stay in the catalog with their Phase 1 naming sources; pass 8 simply records that no catalog-grade work teaches them.
- **Cross-corpus discipline held**: data-structure elements cross-reference the sibling `datastructures/` corpus for the algorithmics zoo; CLRS/Sedgewick/Okasaki enter here as designer-grade treatments, not as an invitation to enumerate variants.
- **Edition notes**: Gregory is carried at the live-verified 4th ed. (2026), GC Handbook at the 2nd ed. (2023), CLRS at the 4th (2022); where a route verified an older edition (Tanenbaum 5th), the node carries the current edition with the discrepancy noted in-entry.
