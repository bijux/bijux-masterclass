> Planned source collection. See [collection status](COLLECTION.md) for preservation and qualification limits.

# Rust Programming — One Hundred Modules, Ten Courses

This is one cumulative Rust curriculum, not ten disconnected surveys. It begins with ordinary typed programs and ends with the ability to review, evolve, and defend a long-lived Rust system. Each course keeps the obligations established before it and adds one new level of responsibility.

```text
values and control
        ↓
resources and memory
        ↓
contracts and architectural variation
        ↓
dataflow, fallibility, and effects
        ↓
compile-time syntax and authority
        ↓
bytes, operating systems, unsafe code, and FFI
        ↓
threads, synchronization, and parallel work
        ↓
futures, network protocols, and service lifecycles
        ↓
measurement, security, delivery, and operation
        ↓
compiler reasoning, soundness, compatibility, and change
```

The course books are the primary material. A module chapter develops one mental model; its workbook turns that model into prediction, repair, construction, transfer, and explanation. The independent lab isolates the mechanism. The course capstone forces ten mechanisms to coexist in one product without hiding their interactions.

## Start here

1. Read [How to study the program](START_HERE.md).
2. Learn the shared [reasoning model](REASONING_MODEL.md).
3. Inspect the [one-hundred-module map](COURSE_MAP.md).
4. Use the [skill map](SKILL_MAP.md) to see the entry and exit standard for every course.
5. Track completed work in [PROGRESS.md].
6. Keep the [glossary](GLOSSARY.md) and [source notes](SOURCE_NOTES.md) beside the course book.

## The ten-course path

| Course | Course book | Governing question | Capstone |
|---:|---|---|---|
| 1 | [Rust Foundations](01-rust-foundations/course-book/index.md) | How do Rust’s types, ownership rules, state models, and error boundaries combine into a complete program you can explain end to end? | **Taskboard** |
| 2 | [Ownership, Lifetimes, and Memory](02-rust-ownership-lifetimes-memory/course-book/index.md) | How do places, loans, lifetimes, destruction, shared liveness, representation, and address stability determine whether a memory design is valid? | **Memory Workspace** |
| 3 | [Traits, Generics, and Architectural Design](03-rust-traits-generics-architectural-design/course-book/index.md) | How should a Rust architecture represent shared behavior, type relationships, runtime variation, protocol states, and downstream extension without importing an inheritance model? | **Review Engine** |
| 4 | [Functional Rust](04-rust-functional-programming/course-book/index.md) | How can Rust make capture, traversal, cardinality, ordering, failure, accumulation, structural sharing, effects, and cost visible in one dataflow? | **LedgerFlow** |
| 5 | [Rust Metaprogramming](05-rust-metaprogramming/course-book/index.md) | Which facts deserve one compile-time source of truth, which generation mechanism is the least powerful adequate choice, and how can expanded code remain diagnosable ordinary Rust? | **CommandForge** |
| 6 | [Rust Systems Programming](06-rust-systems-programming/course-book/index.md) | What does each external boundary promise, which facts can Rust verify, which facts require a manual proof, and how does a safe interface contain those obligations? | **FrameVault** |
| 7 | [Rust Concurrency and Parallelism](07-rust-concurrency-parallelism/course-book/index.md) | Which facts remain true across every legal thread schedule, and what ownership, synchronization, progress, failure, and normalization arguments make those facts reviewable? | **BatchWeave** |
| 8 | [Rust Async and Networked Services](08-rust-async-networked-services/course-book/index.md) | How do suspension, wakeup, task ownership, framing, protocol state, capacity, cancellation, retry, and shutdown remain explicit when peers and timing are only partly observable? | **JobWire** |
| 9 | [Rust Performance and Production Engineering](09-rust-performance-production-engineering/course-book/index.md) | Which measurements, resource bounds, signals, security controls, artifact records, and operating policies make a Rust system defensible under representative load? | **MetricRail** |
| 10 | [Advanced Rust Mastery](10-rust-advanced-mastery/course-book/index.md) | How do you design and evolve a Rust system whose type relationships, unsafe boundaries, compiler behavior, compatibility promises, verification evidence, and operating limits survive independent change? | **AxiomStore** |

## The capstone ladder

The capstones are deliberately different. They are not ten versions of the same command-line application.

| Course | Product | Architectural step |
|---:|---|---|
| 1 | **Taskboard** | Complete safe-Rust program with typed state, errors, persistence, tests, and a library/binary boundary |
| 2 | **Memory Workspace** | Borrowed views, generational identity, staged mutation, shared snapshots, caches, and memory accounting |
| 3 | **Review Engine** | Static and dynamic polymorphism, adapters, typestate, law tests, and public evolution |
| 4 | **LedgerFlow** | Fallible dataflow, deterministic reduction, structural sharing, lazy queries, and effect isolation |
| 5 | **CommandForge** | Declarative and procedural generation with one authority per generated fact |
| 6 | **FrameVault** | Checked binary formats, transactional files, manual allocation, C ABI, and foreign ownership |
| 7 | **BatchWeave** | Bounded thread work, backpressure, panic containment, cancellation, and deterministic reconciliation |
| 8 | **JobWire** | Framed network protocol, async task tree, admission, idempotency, retry, and graceful shutdown |
| 9 | **MetricRail** | Representative measurement, observability, overload policy, threat modeling, traceable releases, and operations |
| 10 | **AxiomStore** | Compiler-shaped reasoning, advanced type relationships, unsafe review, compatibility, verification, and long-lived change |

## What completion means

A checked box is not the final standard. For every module you should be able to:

1. state the governing relationship in plain language;
2. predict the decisive compiler, runtime, build, platform, or schedule consequence;
3. repair a broken design without deleting the difficult requirement;
4. build the independent lab from its contract;
5. apply the mechanism to the capstone while preserving earlier invariants;
6. transfer the idea to a different domain and defend the trade-off.

For every course, complete the final review and one independent change that is not described step by step. The program is finished only when you can enter unfamiliar Rust code, locate its authorities and proof boundaries, change it without accidental regression, and state what your evidence does not establish.

## Study shape

Each course is designed as ten dense study days over two calendar weeks. One module occupies one full day. The normal route is:

```text
chapter
   ↓
closed-book prediction
   ↓
causal diagnosis and repair
   ↓
focused construction
   ↓
independent laboratory
   ↓
capstone integration
   ↓
reconstruction and defense
```

Use the study plan inside each course for the day-by-day sequence. Take the midpoint recovery day seriously: ownership, lifetime, synchronization, and protocol models consolidate through retrieval and reconstruction, not by adding another stack of pages.

## Toolchain

The release uses Rust 2024 Edition and pins Rust 1.97.1 so the examples, diagnostics, and dependency surfaces do not drift during study. Most courses use only the standard library. Courses that require real ecosystem mechanisms pin their dependencies exactly and explain why each dependency exists.

Common repository routes:

```bash
make audit
make links
make rust-source-audit
make progress
make compiler-labs
make check
make test
make starters
make docs
make proof
```

`make proof` is the strongest included route. It requires the pinned Rust toolchain and MkDocs. Static checks are useful, but they never substitute for compilation, tests, rendered documentation, or technical review.
