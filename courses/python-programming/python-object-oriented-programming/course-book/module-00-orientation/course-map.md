# Course Map

This map shows the full progression of the course. The sequence is deliberate:
start with the Python object model, move into responsibility and layering, then
into state design, collaboration boundaries, and finally operational survival.

The running example is a monitoring system. Each module sharpens that system from
ad hoc scripts into a design with explicit value types, aggregate roots, lifecycle
controls, and compatibility boundaries.

## Module 1 – Python’s Object Model, Identity, and the Data Model

**Theme:** Understand what Python objects *really* are: identity, layout, equality, collections, and the data model. No hand-holding.

- **Core 01 – Object Identity, State, Behaviour (Python’s Real Model)**
- **Core 02 – Attribute Layout: `__dict__`, Class vs Instance, Descriptors in the Chain**
- **Core 03 – Construction Discipline: `__init__`, Required State, and Half-Baked Objects**
- **Core 04 – Encapsulation and Public Surface: Representations, Debuggability, and Leaks**
- **Core 05 – Equality, Ordering, and Hashing: Contracts with Containers**
- **Core 06 – Collections Hazards: Aliasing, Mutable Keys, and Shared State**
- **Core 07 – Copying and Cloning: Shallow, Deep, and Custom Semantics**
- **Core 08 – Python Data Model as Design Surface (Iteration, Containers, Context, Numeric)**
- **Core 09 – When OOP Is the Wrong Tool in Python**
- **Core 10 – Refactor 0: Script → Object Model with Correct Identity/Data-Model Semantics**

---

## Module 2 – Responsibilities, Interfaces, Inheritance, and Layering

**Theme:** From individual objects to **collaborating roles**: composition first, inheritance when justified, explicit interfaces, and layered design.

- **Core 11 – Responsibilities, Cohesion, and Object Smells**
- **Core 12 – Composition over Inheritance as Default**
- **Core 13 – Value Objects vs Entities: Identity and Lifecycle**
- **Core 14 – Avoiding Primitive Obsession: Semantic Types, Not Raw Str/Int**
- **Core 15 – Service Objects and Operations vs Stateful Entities**
- **Core 16 – Layering: Domain, Application, Infrastructure in a Python Codebase**
- **Core 17 – Inheritance: Legit Use Cases and the Fragile Base Class Problem**
- **Core 18 – Template Method and Tiny Hierarchies without a Framework Zoo**
- **Core 19 – Interfaces in Python: Duck Typing, ABCs, Protocols (Prescriptive Choices)**
- **Core 20 – Refactor 1: Thin Layered Architecture with Explicit Roles & Small Hierarchies**

---

## Module 3 – State, Dataclasses, Validation, Nulls, and Typestate

**Theme:** State as a **designed object**: dataclasses, immutability, validation, null/optional propagation, lifecycles, typestate, and property-based tests.

**Core 21 – Properties and Computed Attributes: Clarity vs Hidden Work**
When `@property` improves readability; when it hides I/O or heavy work; invariants for property use; migration strategies away from “property as mini-coroutine”.

**Core 22 – Descriptors Mental Model (Without Writing Your Own)**
What a descriptor is; what `@property` actually expands to; why “data vs non-data descriptor” matters for attribute resolution; enough model to debug and design, not to impress.

**Core 23 – Dataclasses, the Good: Concise Value and Entity Definitions**
Using `@dataclass` for value and entity types: default factories, equality, ordering; designing fields intentionally; when to say “no dataclass here”.

**Core 24 – Dataclasses, the Ugly: Inheritance, Defaults, Slots, Frozen Pitfalls**
Real bug gallery: field order, base-class fields, `slots=True` and tooling, “frozen but not really” interactions; how these break equality, hashing, and copying; safe subsets you can rely on.

**Core 25 – Post-Init Validation and “Invalid States Unrepresentable”**
Using `__post_init__` and helper constructors to enforce invariants; centralising validation logic; eliminating “partially valid” instances.

**Core 26 – Boundary Validation Libraries: Where Pydantic and Friends Belong**
Using Pydantic (or similar) at I/O boundaries (JSON, HTTP) while keeping internal domain objects clean; mapping between external schemas and core dataclasses; avoiding “Pydantic everywhere” as a smell.

**Core 27 – Nulls, Optionals, and Partial Objects: Designing Instead of Hoping**
Systematic treatment of `None`: optional fields, sentinel objects, partial aggregates, and how nulls propagate across layers; when to push null handling to the edges vs represent it explicitly.

**Core 28 – Lifecycle and Typestate: Draft → Active → Retired Objects**
Modeling object lifecycles as explicit states; design patterns for legal transitions; how typestate interacts with collections, caches, and persistence.

**Core 29 – Enforcing Typestate in Python APIs (Without Fancy Type Systems)**
Designing APIs that make illegal states/operations hard: separate types vs runtime checks vs constructor patterns; trade-offs; when typestate is worth the complexity.

**Core 30 – Refactor 2: Configs and Rules → Dataclasses, Null-Safe APIs, Typestate & Hypothesis**
Replace dict-based `Rule` configs with dataclasses; introduce null/optional semantics deliberately; encode `Rule` lifecycle; add Hypothesis tests for transitions, validity, and error conditions.

---

## Module 4 – Aggregates, Domain Events, Object Graphs, and Collaboration Patterns

**Theme:** Move from isolated objects to **coherent domains**: aggregates, events, patterns, and debuggable object graphs.

**Core 31 – Aggregates and Consistency Boundaries in a Python Service**
Define aggregates (`AlertAggregate` owning `Rule` plus `MetricHistory`); deciding where invariants live; who is allowed to mutate what and how.

**Core 32 – Cross-Object Invariants and Aggregate-Level Validation**
Invariants spanning multiple objects (e.g. “no open alerts without rules”); enforcing them at aggregate root; designing methods/commands that preserve those invariants.

**Core 33 – Aggregate Lifecycle and Failure Semantics**
Create/activate/deactivate aggregates; what happens when an operation partially fails; how to represent and surface failure at the aggregate level without leaking infrastructure detail.

**Core 34 – Domain Events for Decoupling (Without Full Event Sourcing)**
Designing `AlertTriggered`, `RuleChanged`, etc. as domain events; using events to decouple parts of the system in a **single process**; what you deliberately *do not* model (no CQRS, no distributed log).

**Core 35 – In-Process Event Dispatch: Tiny Observer and Event Bus**
Implement a minimal synchronous event bus: subscribers, dispatch order, error handling strategies; how this differs from global signals or raw callbacks.

**Core 36 – Projections, Read Models, and Object-Graph Debug Views**
Using events and aggregate state to build read models (dashboards, summaries) and **debug views**: who owns whom, what states are active, where cycles exist.

**Core 37 – Strategy and Policy Objects for Rule Evaluation and Decisions**
Implement Strategy for rule evaluation; representing rules as data + pluggable behaviour; defining a stable interface for adding new rule types later.

**Core 38 – Adapter and Bridge: Wrapping External Systems and Storage**
Wrapping third-party metric sources and storage backends; designing “ports and adapters” at the object level; avoiding leakage of HTTP/DB concerns into domain code.

**Core 39 – Designing Collaboration Surfaces: How Objects Talk Without Tangle**
Choosing method signatures that minimise coupling: “tell, don’t ask”; capability surfaces; avoiding “omniscient” god services that know every concrete class.

**Core 40 – Refactor 3: Monolithic Logic → Aggregates + Events + Strategies + Debuggable Graph**
Restructure the monitoring system to: a clear `AlertAggregate`, event emission on state changes, pluggable rule strategies, adapters for source/storage; add tests that assert expected events and verify object-graph sanity.

---

## Module 5 – Resources, Failures, Smells, Boundaries, and Evolution (Core Level)

**Theme:** Make object systems **survive**: resources, failure handling, smells & refactoring, copying semantics, and basic evolution/compatibility.

**Core 41 – Resources and Context Managers: Objects That Own Things**
Designing resource objects that encapsulate files, network connections, cursors; responsibilities for acquisition and release; when to implement `__enter__`/`__exit__` vs use helpers.

**Core 42 – Unit-of-Work: Grouping Changes and Handling Failures**
Grouping aggregate operations under a single “unit of work”; basic commit/rollback semantics purely in memory; how to structure application services around this pattern.

**Core 43 – Deterministic Cleanup and Leak Prevention in Pure Python**
Using `ExitStack`, `try/finally`, and object lifetimes to guarantee cleanup; where relying on GC is a bug; designing APIs that don’t force callers into cleanup hell.

**Core 44 – Idempotent Operations and Safe Retries (Sync-Only Context)**
Designing operations so that retrying doesn’t double-apply side effects: idempotent commands vs unsafe ones; how this interacts with aggregates and events, even in a single-process system.

**Core 45 – Logging and Error Propagation as Part of Object Contracts**
Designing logging as a deliberate contract: what gets logged, with what IDs/context; how domain errors propagate across layers; avoiding “log everywhere, fix nowhere” patterns.

**Core 46 – Public vs Internal Modules and Facades for OOP Codebases**
Defining which packages and classes are the public API; designing `monitoring.api` or similar; hiding infrastructure details behind facades; how this shapes later evolution.

**Core 47 – Design Smells and Refactoring Patterns in OOP Python**
Catalogue of critical smells (God objects, feature envy, long parameter lists, inappropriate intimacy, cyclic dependencies); concrete refactorings using tools from Modules 1–4.

**Core 48 – Copying and Versioning of Objects and Aggregates Over Time**
Designing clones and snapshots of entities/aggregates; how copying semantics interact with future evolution; when to snapshot state vs recompute; serialisation boundaries.

**Core 49 – Evolution Basics and Compatibility Contracts**
Semantic versioning for object APIs and serialized forms; distinguishing structural vs behavioural vs format compatibility; where to be strict vs tolerant in a Python service.

**Core 50 – Refactor 4: Introduce New Feature, Preserve Old Behaviour, Document Smell Fixes**
Add a non-trivial feature (e.g. new rule type or new metric dimension) to the monitoring system:
– without breaking existing callers or stored data,
– after cleaning up key smells,
– with explicit tests for compatibility, logs, and resource correctness.
