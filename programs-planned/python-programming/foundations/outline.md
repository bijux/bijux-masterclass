## Module 1 – Beginner Foundations (Cores 1–10)

**Goal:** Core execution model, basic data, and first contact with algorithms, correctness, and performance.

- **Core 1 – Python as a Program**: Interpreter model, execution, source → bytecode, names as bindings (not boxes).
- **Core 2 – Expressions and Control Flow**: Expressions vs statements, conditionals, loops, short-circuiting, tracing execution paths.
- **Core 3 – Collections and Data**: Lists, dicts, sets; mutability and aliasing; safe basic transformations.

### **Core 4 – Functions and Parameters**
Defining/calling functions, parameters vs arguments, scope, basic pure-style design.

### **Core 5 – Errors and Debugging**
Syntax vs runtime errors, tracebacks, step-by-step debugging mindset.

### **Core 6 – File I/O and Simple Data Processing**
Text files, context managers, line iteration; simple CSV/log reading.

### **Core 7 – Modules and Imports**
Files as modules, namespaces, import patterns, avoiding global clutter.

### **Core 8 – Introductory Algorithms**
Linear search, simple sorting, informal Big-O reasoning (O(1) vs O(n)).

### **Core 9 – Assertions and Basic Testing**
Assertions, simple test functions, doctest-style checking of expected behaviour.

### **Core 10 – Project 1: Data Loader**
Small ETL-style script: read file → transform → write result, with basic tests and clear structure.

---

## Module 2 – Core Programming Skills (Cores 11–20)

**Goal:** Reusable abstractions with OOP, FP, core data structures, testing, algorithms, and first performance awareness.

### **Core 11 – Object Model Essentials**
Objects, identity, mutability, `__dict__`, instance vs class attributes.

### **Core 12 – Classes and Methods**
Constructors, required state, methods, minimal and coherent class design.

### **Core 13 – API Design and Public Surface**
Function and method signatures, docstrings, public vs “internal” API, stable interfaces.

### **Core 14 – Functions as Objects (FP Basics)**
First-class functions, lambdas, closures, higher-order functions as basic combinators.

### **Core 15 – Data Structures I: Lists, Dicts, Sets Internals**
How lists grow, dict/set hashing, expected complexity for lookups, inserts, deletes.

### **Core 16 – Unit Testing Fundamentals**
pytest basics, parametrized tests, coverage as a sanity metric, testing edge cases.

### **Core 17 – Recursion and Iteration**
Recursive vs iterative solutions, base cases, simple complexity comparison.

### **Core 18 – Immutability and Purity**
Immutable data (tuples, frozen dataclasses), map/filter-style pipelines, separating pure logic from IO.

### **Core 19 – Performance Seeds**
Timing code with `timeit`, recognizing hot loops, avoiding premature micro-optimizations.

### **Core 20 – Project 2: Hybrid Processor**
Program using OOP for stateful entities plus FP transformations for core logic, with a proper unit test suite.

---

## Module 3 – Intermediate Architectures (Cores 21–30)

**Goal:** Composable designs, metaprogramming seeds, more serious data structures, basic concurrency, and static correctness.

### **Core 21 – Descriptors and Properties**
Attribute lookup chain, `@property`, data vs non-data descriptors as controlled access mechanisms.

### **Core 22 – Composition Patterns (Over Inheritance)**
Delegation, “has-a” vs “is-a”, composing behaviours instead of building deep hierarchies.

### **Core 23 – Advanced Error Handling**
Custom exception types, structured error propagation, context managers for cleanup.

### **Core 24 – Data Structures II: Trees and Graphs**
Representing trees/graphs in Python, basic traversals (DFS/BFS), typical use-cases.

### **Core 25 – Functional Pipelines and Generators**
Generator functions, lazy iteration, `itertools`, building linear data-flow pipelines.

### **Core 26 – Concurrency Intro (Threads and GIL Reality)**
What the GIL is, IO-bound vs CPU-bound workloads, basic threaded producer–consumer with `queue`.

### **Core 27 – Bytecode and Introspection**
Using `dis` and `inspect` to see what Python executes; understanding function signatures and frames.

### **Core 28 – Type Hints and Contracts**
Type annotations, mypy/pyright basics, simple protocol interfaces, using types as partial specs.

### **Core 29 – Memory Basics**
Reference counting, cycles and GC, object lifetime, recognizing common leak patterns.

### **Core 30 – Project 3: Typed Architecture**
Multi-module pipeline using OOP entities, FP pipelines, descriptors or properties where appropriate, and static type checking.

---

## Module 4 – Systems, Parallelism, and Performance (Cores 31–40)

**Goal:** Scaling and optimizing: async, multiprocessing, OS interaction, stronger algorithms, profiling, and integration testing.

### **Core 31 – Async IO Fundamentals**
`async`/`await`, event loop mental model, basic async tasks (e.g., concurrent network calls).

### **Core 32 – Multiprocessing and True Parallelism**
Process pools, task distribution, data transfer cost (pickling), when to prefer processes over threads.

### **Core 33 – OS Primitives and System Interaction**
Using `os`/`sys`, environment variables, PIDs, signals, basic process introspection.

### **Core 34 – Algorithm Design Patterns**
Greedy, divide-and-conquer, simple dynamic programming; correctness and complexity trade-offs.

### **Core 35 – Profiling in Practice**
`cProfile`, line profilers, reading flame-style views, identifying real bottlenecks vs noise.

### **Core 36 – Advanced FP: Currying and Partials**
`functools.partial`, simple implicit configuration via function wrapping, small combinators.

### **Core 37 – OOP Depth: Equality, Hashing, Identity**
Designing value objects vs entities, implementing `__eq__` and `__hash__`, invariant preservation.

### **Core 38 – Invariants and Preconditions in Code**
Using checks to enforce business rules, making illegal states unrepresentable where feasible.

### **Core 39 – Integration and System Testing**
Testing across modules, fixtures, mocking/stubbing external services, basic test architecture.

### **Core 40 – Project 4: Parallel Optimizer**
End-to-end data processing pipeline using async and/or multiprocessing, systematically profiled and tuned, with integration tests.

---

## Module 5 – Correctness, Semantics, and Synthesis (Cores 41–50)

**Goal:** Holistic mastery: networking, deeper metaprogramming, PLT seeds, advanced data structures, property testing, optimization, and full-system synthesis.

### **Core 41 – Networking Basics**
TCP sockets, client/server basics, message framing, timeouts, robust error handling.

### **Core 42 – Metaprogramming Depth: Decorators and Metaclasses**
Well-behaved decorators, class decorators, minimal metaclass use-cases (registries, validation).

### **Core 43 – Functional Architectures**
“Pure core, imperative shell” pattern, configuration as data, deterministic computation pipelines.

### **Core 44 – PLT Evaluation: ASTs and Simple Interpreters**
Using `ast` to parse, walking ASTs, implementing a tiny expression evaluator or rule language.

### **Core 45 – Advanced Data Structures**
Tries, LRU caches, bisect-based structures; when specialized structures beat plain dict/list.

### **Core 46 – Property-Based Testing**
Hypothesis (or similar), generating inputs, expressing invariants, finding edge-case bugs automatically.

### **Core 47 – Optimization Tactics**
Vectorization with NumPy, caching and memoization, reducing Python overhead via better data layout.

### **Core 48 – Advanced Systems: Filesystem and Subprocess**
`mmap`, atomic file writes, robust use of `subprocess` (no shell injection, proper cleanup).

### **Core 49 – Semantics and API Evolution**
Backward compatibility, deprecation strategies, behaviour-preserving refactors, semantic versioning mindset.

### **Core 50 – Capstone: Unified System**
Design and implement a small but non-trivial system that combines: clean OOP model, FP pipelines, basic metaprogramming, concurrency/parallelism, tests (unit + property + integration), profiling and optimization, and careful system interaction. Formal write-up of architecture and trade-offs.
