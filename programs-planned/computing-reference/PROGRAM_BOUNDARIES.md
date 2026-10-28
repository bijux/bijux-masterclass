# Program Boundaries

Every topic has one primary conceptual owner. Adjacent programs may reference it only from their own perspective.

## 01. Programming Languages & Semantics

**Purpose:** Build a language-independent model of how programs are represented, typed, evaluated, composed, and given precise meaning.

**Prerequisites:** discrete mathematics; proficiency in at least two contrasting languages; basic data structures and algorithms.

**Owns**

- syntax and binding
- dynamic and static semantics
- type systems
- evaluation strategies
- state and effects
- module systems
- runtime semantics
- comparative language design

**Does not own**

- deep object-oriented practice (Program 02)
- deep functional practice (Program 03)
- concurrent/parallel programming practice (Program 04)
- compiler construction (Program 08)
- computability and complexity (Program 15)

**Professional outcome:** Ready to reason across language families, review language designs, explain runtime and type-system trade-offs, and enter advanced language implementation or formal-semantics work.

## 02. Programming Languages: Object-Oriented Programming

**Purpose:** Develop precise command of object models, object-oriented abstraction, polymorphism, composition, and maintainable object-oriented implementation across languages.

**Prerequisites:** Programming Languages & Semantics Level I; data structures; testing fundamentals.

**Owns**

- object models
- encapsulation
- class and prototype systems
- subtyping and dispatch
- composition and inheritance
- object lifecycles
- OO generics
- OO concurrency
- OO runtime behavior
- large-scale OO code

**Does not own**

- general domain modeling (Program 09)
- pattern catalogues (Program 11)
- system-wide architecture (Program 12)
- general programming-language semantics (Program 01)

**Professional outcome:** Ready to design, implement, test, review, and evolve substantial object-oriented systems in Java-, C#-, C++-, Python-, or similar ecosystems.

## 03. Programming Languages: Functional Programming

**Purpose:** Develop practical and theoretical command of programming with immutable values, first-class functions, algebraic data, compositional effects, and equational reasoning.

**Prerequisites:** Programming Languages & Semantics Level I; recursion and data structures; basic discrete mathematics.

**Owns**

- pure functions
- immutable data
- higher-order programming
- algebraic data types
- pattern matching
- lazy and strict FP
- effect composition
- functional architecture
- functional concurrency
- equational reasoning

**Does not own**

- general PL semantics (Program 01)
- formal programming theory (Program 07)
- general software design (Program 09)
- distributed-system algorithms (Program 27)

**Professional outcome:** Ready to build and review production functional or functional-first software in Haskell, Scala, F#, OCaml, Clojure, Rust, or functional Python ecosystems.

## 04. Programming Languages: Concurrent & Parallel Programming

**Purpose:** Build precise, practical command of concurrency and parallelism across shared memory, asynchronous runtimes, actors, accelerators, and distributed-memory programming.

**Prerequisites:** Programming Languages & Semantics Level I; algorithms and data structures; basic computer architecture.

**Owns**

- language-level concurrency
- synchronization
- memory models
- async programming
- actors
- task and data parallelism
- lock-free programming
- SIMD and GPU models
- distributed-memory parallel programming
- parallel performance

**Does not own**

- operating-system scheduler implementation (Program 22)
- distributed fault tolerance and consensus (Program 27)
- network protocol engineering (Program 24)
- general language semantics (Program 01)

**Professional outcome:** Ready to implement, debug, test, and optimize concurrent and parallel software using threads, async/await, actors, SIMD, OpenMP-style tasks, GPUs, and MPI-style message passing.

## 05. Programming Languages: Systems Programming

**Purpose:** Develop command of low-level software construction where memory, representation, operating-system interfaces, latency, portability, and failure behavior are explicit.

**Prerequisites:** Programming Languages & Semantics Level I; Computer Architecture Level I or equivalent; basic operating-system concepts.

**Owns**

- C and Rust systems programming
- memory and resource management
- Unix/POSIX interfaces
- binary representation
- process and file APIs
- sockets and evented I/O
- FFI
- debugging and profiling
- portable low-level libraries
- systems hardening

**Does not own**

- kernel design and implementation (Program 22)
- compiler implementation (Program 08)
- network protocol architecture (Program 24)
- parallel programming theory (Program 04)

**Professional outcome:** Ready to build and maintain command-line tools, daemons, networking components, storage utilities, runtime components, and performance-sensitive libraries in C, C++, or Rust.

## 06. Programming Languages: Metaprogramming

**Purpose:** Develop disciplined command of programs that inspect, generate, transform, or specialize programs while preserving readability, safety, tooling, and compatibility.

**Prerequisites:** Programming Languages & Semantics Level I; one statically typed and one dynamic language; basic compiler front-end concepts.

**Owns**

- textual and syntactic macros
- reflection
- annotations and decorators
- generics and templates as metaprogramming
- AST transformation
- code generation
- staging and specialization
- typed metaprogramming
- DSL construction
- metaprogramming governance

**Does not own**

- full parsing and compiler back ends (Program 08)
- general language semantics (Program 01)
- software pattern catalogues (Program 11)

**Professional outcome:** Ready to build and review macros, decorators, annotation processors, schema/code generators, typed derivation systems, build-time generators, and embedded DSLs.

## 07. Programming Languages: Theory of Programming

**Purpose:** Build the mathematical foundations for specifying, proving, analyzing, and deriving programs, connecting logic, type theory, semantics, and static analysis.

**Prerequisites:** discrete mathematics and logic; Programming Languages & Semantics Levels I-II or equivalent; algorithms.

**Owns**

- logic for programs
- lambda calculi
- type theory
- program logics
- refinement
- separation logic
- abstract interpretation
- program analysis
- model checking
- proof assistants

**Does not own**

- language feature survey (Program 01)
- compiler engineering (Program 08)
- computability and complexity of problems (Program 15)
- testing practice (Program 13)

**Professional outcome:** Ready to read graduate programming-languages research, write formal specifications and proofs, use proof assistants and model checkers, and reason rigorously about program correctness.

## 08. Compilers & Language Implementation

**Purpose:** Develop end-to-end command of interpreters, compilers, intermediate representations, analyses, optimization, code generation, runtimes, and production toolchains.

**Prerequisites:** Programming Languages & Semantics Levels I-II; data structures and algorithms; systems programming basics; computer architecture basics.

**Owns**

- lexing and parsing
- name and type analysis
- interpreters
- IR design
- dataflow analysis
- optimization
- code generation
- runtimes and GC
- JIT compilation
- compiler tooling and correctness

**Does not own**

- general language semantics (Program 01)
- metaprogramming APIs (Program 06)
- computer-architecture design (Program 23)

**Professional outcome:** Ready to implement and maintain language front ends, transpilers, static analyzers, bytecode engines, optimizing compilers, DSL toolchains, and runtime components.

## 09. Software Engineering: Software Design & Domain Modeling

**Purpose:** Develop the ability to turn ambiguous domain knowledge and changing requirements into precise, modular, testable software models.

**Prerequisites:** programming proficiency; OOP or FP foundations; testing fundamentals; basic software construction.

**Owns**

- problem framing
- modularity
- responsibility design
- domain modeling
- DDD tactical and strategic modeling
- contracts and invariants
- state and workflow models
- boundary design
- model evolution
- design review

**Does not own**

- pattern catalogue ownership (Program 11)
- system-wide architecture (Program 12)
- project methodology (Program 10)
- database physical design (Program 18)

**Professional outcome:** Ready to lead code- and component-level design, facilitate domain discovery, define boundaries and contracts, and evolve models in business-critical software.

## 10. Software Engineering: Methods & Evolution

**Purpose:** Develop disciplined methods for discovering, planning, building, maintaining, and changing software across its full economic and organizational lifecycle.

**Prerequisites:** software construction experience; basic teamwork and version control; one substantial software project.

**Owns**

- software lifecycle models
- requirements engineering
- agile and lean methods
- Scrum and Kanban
- planning and estimation
- configuration and change management
- maintenance and refactoring
- legacy modernization
- software economics
- socio-technical evolution

**Does not own**

- code-level design (Program 09)
- architecture ownership (Program 12)
- testing techniques (Program 13)
- delivery pipeline mechanics and production reliability (Program 14)

**Professional outcome:** Ready to choose and adapt development methods, run effective Scrum or Kanban systems, manage requirements and risk, and lead the evolution of long-lived software.

## 11. Software Engineering: Patterns

**Purpose:** Build a rigorous vocabulary for recurring software design problems, the forces that shape them, and the consequences of applying or misapplying established patterns.

**Prerequisites:** OOP foundations; software design fundamentals; experience maintaining a nontrivial codebase.

**Owns**

- pattern form and forces
- object design patterns
- enterprise application patterns
- integration and messaging patterns
- concurrency patterns
- distributed resilience patterns
- data-access patterns
- anti-patterns
- pattern languages
- pattern selection

**Does not own**

- domain discovery and modeling (Program 09)
- system-wide architecture design (Program 12)
- protocol algorithms (Program 27)
- platform product design (Program 29)

**Professional outcome:** Ready to recognize, select, adapt, combine, and critique design, integration, concurrency, data, and distributed-system patterns without pattern-driven overengineering.

## 12. Software Engineering: Software Architecture

**Purpose:** Develop the ability to shape software-intensive systems through explicit quality attributes, boundaries, structures, deployment models, and evolutionary decisions.

**Prerequisites:** software design experience; databases and networking basics; distributed-systems foundations; production software experience.

**Owns**

- architectural drivers
- quality attributes
- views and viewpoints
- architectural styles
- component and service boundaries
- data and integration architecture
- deployment architecture
- architecture evaluation
- evolution and governance
- socio-technical architecture

**Does not own**

- code-level domain design (Program 09)
- pattern catalogues (Program 11)
- cloud implementation detail (Program 30)
- distributed algorithms (Program 27)

**Professional outcome:** Ready to act as a senior architect or technical lead who can design, document, evaluate, communicate, and evolve production architectures.

## 13. Software Engineering: Testing & Quality Engineering

**Purpose:** Develop rigorous, economical approaches for evaluating software behavior, preventing defects, diagnosing failures, and making quality visible across the lifecycle.

**Prerequisites:** software construction; basic design and architecture; version control and CI familiarity.

**Owns**

- test theory
- unit and component testing
- integration and system testing
- test design
- property and model-based testing
- fuzzing and mutation
- performance and security testing
- test automation architecture
- quality models and metrics
- defect prevention

**Does not own**

- delivery pipelines (Program 14)
- formal proof theory (Program 07)
- security architecture (Program 25)
- domain design ownership (Program 09)

**Professional outcome:** Ready to design and lead testing strategies, build reliable automation, test distributed and data-intensive systems, and improve organizational quality engineering.

## 14. Software Engineering: Software Delivery & Reliability Engineering

**Purpose:** Develop the engineering discipline required to turn source changes into safe production releases and keep services reliable under change, load, dependency failure, and operator error.

**Prerequisites:** software engineering experience; basic networking, systems, and cloud knowledge; testing fundamentals.

**Owns**

- build and artifact engineering
- continuous integration and delivery
- release and deployment safety
- observability
- SRE
- incident management
- resilience engineering
- capacity and overload
- disaster recovery
- software supply-chain delivery

**Does not own**

- cloud resource design (Program 30)
- platform product construction (Program 29)
- testing technique ownership (Program 13)
- security engineering ownership (Program 25)

**Professional outcome:** Ready to design CI/CD systems, release strategies, observability, SLOs, incident response, resilience mechanisms, and reliability programs for production services.

## 15. Theory of Computation & Complexity

**Purpose:** Develop rigorous understanding of formal languages, computability, reductions, resource-bounded computation, and the structural limits of efficient algorithms.

**Prerequisites:** discrete mathematics; proof techniques; algorithms and asymptotic analysis.

**Owns**

- automata and formal languages
- computability and undecidability
- reductions
- time and space complexity
- NP-completeness
- randomized complexity
- approximation hardness
- parameterized and fine-grained complexity
- circuit and communication complexity
- interactive and quantum complexity foundations

**Does not own**

- algorithm implementation and empirical performance (Program 16)
- program semantics and proof systems (Program 07)
- compiler construction (Program 08)

**Professional outcome:** Ready for graduate algorithms, cryptography, formal languages, complexity research, and principled reasoning about what software can and cannot compute efficiently.

## 16. Algorithm Engineering

**Purpose:** Develop the full cycle of algorithmic work: precise problem formulation, design, proof, implementation, measurement, tuning, and selection under real machine and workload constraints.

**Prerequisites:** discrete mathematics; programming proficiency; data structures; basic probability.

**Owns**

- algorithm design paradigms
- correctness and analysis
- searching and sorting
- graph and flow algorithms
- string and sequence algorithms
- optimization algorithms
- randomized and approximation algorithms
- online and streaming algorithms
- parallel and external-memory algorithms
- experimental algorithmics

**Does not own**

- complexity-class theory (Program 15)
- data-structure implementation ownership (Program 17)
- hardware architecture (Program 23)

**Professional outcome:** Ready to solve unfamiliar computational problems, implement robust high-performance algorithms, compare alternatives empirically, and justify choices in production or research software.

## 17. Data Structures Engineering

**Purpose:** Develop workload-aware command of in-memory, persistent, concurrent, external-memory, approximate, and distributed data structures, including their invariants and machine-level costs.

**Prerequisites:** programming proficiency; algorithms and asymptotic analysis; basic memory hierarchy.

**Owns**

- abstract data types and invariants
- linear and associative structures
- trees and heaps
- graph and string structures
- persistent structures
- concurrent structures
- external-memory structures
- probabilistic structures
- spatial and vector indexes
- succinct and distributed structures

**Does not own**

- algorithm-design ownership (Program 16)
- database-engine internals beyond structures (Program 18)
- distributed consistency protocols (Program 27)

**Professional outcome:** Ready to design, implement, test, benchmark, and select data structures for libraries, databases, runtimes, search systems, and high-performance applications.

## 18. Database Engineering

**Purpose:** Develop end-to-end command of database storage, indexing, query processing, transactions, recovery, replication, distribution, specialization, and production operation.

**Prerequisites:** data structures and algorithms; systems programming basics; operating-system and storage basics; SQL familiarity.

**Owns**

- relational and physical models
- storage engines
- indexes
- transactions and concurrency control
- query execution and optimization
- logging and recovery
- replication and HA
- distributed databases
- specialized database engines
- database operations

**Does not own**

- pipeline construction (Program 19)
- enterprise data architecture (Program 20)
- distributed algorithms beyond database context (Program 27)

**Professional outcome:** Ready to design schemas and workloads, diagnose database behavior, tune and operate production databases, and contribute to database engines or data infrastructure.

## 19. Data Engineering

**Purpose:** Develop command of reliable data ingestion, modeling, transformation, orchestration, quality, lineage, and delivery across batch and streaming workflows.

**Prerequisites:** SQL and Python; database fundamentals; basic statistics; software engineering and version control.

**Owns**

- data representation and schemas
- ingestion and CDC
- data modeling for analytics
- batch transformations
- stream processing at pipeline level
- orchestration
- data quality
- metadata and lineage
- analytical serving
- data pipeline operations

**Does not own**

- enterprise-wide data architecture and governance operating models (Program 20)
- cluster-engine internals and extreme scale (Program 21)
- database engine internals (Program 18)

**Professional outcome:** Ready to build, test, operate, and evolve production data pipelines and analytical data products using SQL, Python, databases, object storage, and modern orchestration systems.

## 20. Data Architecture Engineering

**Purpose:** Develop the ability to shape organization-wide data structures, ownership, flows, platforms, governance, and evolution across operational, analytical, and AI use cases.

**Prerequisites:** database and data-engineering foundations; software architecture fundamentals; business-domain modeling; security and governance basics.

**Owns**

- enterprise data architecture
- data domains and ownership
- conceptual and logical models
- integration architecture
- master and reference data
- metadata and semantics
- governance architecture
- data mesh and fabric
- privacy and lifecycle architecture
- data modernization

**Does not own**

- pipeline implementation (Program 19)
- cluster and engine internals (Program 21)
- database engine design (Program 18)
- general software architecture ownership (Program 12)

**Professional outcome:** Ready to work as a data architect who can define target architectures, domain boundaries, integration strategies, governance mechanisms, migration plans, and decision records.

## 21. Large-Scale Data Systems Engineering

**Purpose:** Develop deep command of distributed storage and computation mechanisms that make large-scale batch, streaming, and analytical systems correct, efficient, and operable.

**Prerequisites:** Data Engineering Levels I-II or equivalent; Distributed Systems Level I or equivalent; algorithms, databases, and systems basics.

**Owns**

- distributed data storage
- cluster dataflow engines
- shuffle and distributed joins
- stream processors
- large-scale query engines
- lakehouse internals
- resource scheduling
- fault tolerance
- skew and performance
- cluster cost and capacity

**Does not own**

- ordinary pipeline construction (Program 19)
- organization-wide data architecture (Program 20)
- general consensus and distributed theory (Program 27)
- database internals outside analytical scale (Program 18)

**Professional outcome:** Ready to build, tune, and diagnose cluster-scale data systems and to contribute to distributed processing, storage, query, or lakehouse infrastructure.

## 22. Operating Systems

**Purpose:** Develop deep command of the abstractions, mechanisms, policies, and implementation trade-offs that mediate hardware resources and application execution.

**Prerequisites:** systems programming; computer architecture foundations; concurrency basics; data structures.

**Owns**

- kernel architecture
- processes and threads
- scheduling
- synchronization
- virtual memory
- filesystems
- I/O and devices
- network stack internals
- virtualization and isolation
- OS security, observability, and reliability

**Does not own**

- user-space systems programming practice (Program 05)
- processor microarchitecture (Program 23)
- network protocol engineering above OS stack (Program 24)

**Professional outcome:** Ready to work on kernels, runtimes, containers, low-level infrastructure, performance diagnosis, and operating-system-adjacent systems software.

## 23. Computer Architecture

**Purpose:** Develop command of processor, memory, interconnect, accelerator, and system architecture from instruction-set contracts through microarchitectural performance and energy trade-offs.

**Prerequisites:** digital logic basics; systems programming; algorithms; basic probability and performance analysis.

**Owns**

- digital implementation foundations
- instruction-set architecture
- datapaths and control
- pipelining
- caches and virtual memory hardware
- out-of-order execution
- multicore and coherence
- interconnects
- accelerators
- architecture evaluation and security

**Does not own**

- operating-system policy and kernel implementation (Program 22)
- language compiler construction (Program 08)
- parallel programming techniques (Program 04)

**Professional outcome:** Ready to reason about hardware-software performance, contribute to architecture or low-level systems work, and diagnose how software maps onto modern processors and memory systems.

## 24. Network Engineering

**Purpose:** Develop protocol-level and operational command of how packets move through local, wide-area, wireless, datacenter, and cloud networks, including routing, transport, security, automation, and failure diagnosis.

**Prerequisites:** systems fundamentals; basic probability; command-line and scripting skills.

**Owns**

- layered networking
- Ethernet and switching
- IP addressing and routing
- transport protocols
- DNS and application protocols
- routing protocols
- datacenter and cloud networking
- wireless networking
- SDN and automation
- network operations and performance

**Does not own**

- kernel network-stack implementation (Program 22)
- application API semantics (Program 28)
- cloud provider service design (Program 30)
- general security engineering (Program 25)

**Professional outcome:** Ready to design, configure, automate, troubleshoot, secure, and performance-engineer production networks and networked systems.

## 25. Security Engineering

**Purpose:** Develop adversarial, risk-based command of designing, building, operating, and assessing trustworthy software and infrastructure.

**Prerequisites:** systems, networking, and software engineering fundamentals; basic probability; programming and command-line skills.

**Owns**

- security principles and risk
- applied cryptography
- identity and access
- application security
- systems and network security
- cloud and infrastructure security
- data and privacy security
- software supply chain
- detection and incident response
- security architecture and assurance

**Does not own**

- cryptographic complexity theory (Program 15)
- network engineering ownership (Program 24)
- delivery mechanics (Program 14)
- platform implementation ownership (Program 29)

**Professional outcome:** Ready to perform threat modeling, design identity and access controls, secure applications and platforms, assess vulnerabilities, monitor attacks, and lead remediation and incident response.

## 26. Systems Engineering

**Purpose:** Develop a disciplined, lifecycle-wide method for defining, modeling, integrating, verifying, operating, and evolving complex software-intensive and cyber-physical systems.

**Prerequisites:** software and computer-systems foundations; basic probability and statistics; experience with multidisciplinary projects.

**Owns**

- systems thinking
- stakeholder needs
- requirements engineering
- functional and physical architecture
- model-based systems engineering
- interfaces and integration
- trade studies
- reliability and safety
- verification and validation
- system lifecycle and systems of systems

**Does not own**

- software component design (Program 09)
- software architecture detail (Program 12)
- project delivery method ownership (Program 10)
- cloud and platform implementation (Programs 29-30)

**Professional outcome:** Ready to work as a systems engineer on complex products or platforms, managing stakeholder needs, requirements, interfaces, trade studies, risk, verification, and system evolution.

## 27. Distributed Systems Engineering

**Purpose:** Develop rigorous command of computation across unreliable, concurrent machines, including time, ordering, replication, consistency, consensus, transactions, partitioning, and fault tolerance.

**Prerequisites:** algorithms; networking; concurrency; databases and operating systems basics.

**Owns**

- distributed models and failure
- time and ordering
- communication semantics
- replication
- consistency models
- consensus
- distributed transactions
- partitioning and coordination
- CRDTs and Byzantine resilience
- distributed-system testing and operations

**Does not own**

- large-scale data engine specifics (Program 21)
- database internals (Program 18)
- network protocol engineering (Program 24)
- API design (Program 28)

**Professional outcome:** Ready to design, implement, test, and operate distributed services, coordination systems, replicated storage, event systems, and geo-distributed platforms.

## 28. API & Service Engineering

**Purpose:** Develop end-to-end command of designing, implementing, securing, evolving, testing, and operating synchronous and asynchronous service interfaces.

**Prerequisites:** software design; networking and HTTP basics; security foundations; distributed-systems foundations.

**Owns**

- HTTP semantics
- resource and operation design
- API contracts and schemas
- REST, RPC, GraphQL, and event APIs
- authentication and authorization at APIs
- compatibility and versioning
- resilience and performance
- API testing and observability
- gateways and service interaction
- API governance and developer experience

**Does not own**

- overall software architecture (Program 12)
- general distributed algorithms (Program 27)
- platform product ownership (Program 29)
- network-layer engineering (Program 24)

**Professional outcome:** Ready to build and lead production API and service work across HTTP/REST, RPC, GraphQL, events, gateways, contracts, security, reliability, and governance.

## 29. Platform Engineering

**Purpose:** Develop the product, architecture, and implementation skills needed to create safe self-service platforms that reduce cognitive load and enable teams to deliver and operate software independently.

**Prerequisites:** cloud and infrastructure foundations; containers and Kubernetes basics; software architecture; delivery and reliability basics.

**Owns**

- platform as product
- developer experience and cognitive load
- self-service interfaces
- containers and Kubernetes as platform substrate
- control planes and operators
- golden paths
- developer portals
- multi-tenancy and policy
- platform observability and reliability
- platform adoption and economics

**Does not own**

- cloud resource and network architecture (Program 30)
- software delivery practice ownership (Program 14)
- service API design ownership (Program 28)
- general software architecture (Program 12)

**Professional outcome:** Ready to design, build, operate, and evolve internal developer platforms, paved roads, control planes, developer portals, and shared runtime capabilities.

## 30. Cloud & Infrastructure Engineering

**Purpose:** Develop provider-independent command of compute, networking, storage, identity, automation, resilience, governance, and economics in public, private, hybrid, and multi-cloud infrastructure.

**Prerequisites:** operating systems and networking basics; security fundamentals; scripting and version control; software architecture basics.

**Owns**

- cloud operating models
- compute and virtualization
- cloud networking
- storage and managed data services
- IAM and security foundations
- infrastructure as code
- resilience and disaster recovery
- observability and cost
- hybrid and multi-cloud
- infrastructure governance and migration

**Does not own**

- internal developer-platform product design (Program 29)
- software release and SRE practice ownership (Program 14)
- application API design (Program 28)
- network protocol depth (Program 24)

**Professional outcome:** Ready to design, provision, secure, operate, migrate, and optimize production cloud infrastructure using infrastructure as code and modern managed services.
