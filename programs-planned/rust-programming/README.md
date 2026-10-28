# Rust Programming — Courses 1–9

This repository is one **ninety-module learning path**, not nine adjacent surveys. Each course raises the level of responsibility while preserving the reasoning habits built before it:

```text
values and control
        ↓
resources and memory
        ↓
contracts and architecture
        ↓
dataflow and effects
        ↓
syntax and compile-time authority
        ↓
external boundaries and systems proofs
        ↓
concurrent schedules and parallel work
        ↓
asynchronous lifecycles and network protocols
        ↓
measured performance and production operation
```

The course books are the primary product. Each authoritative chapter builds one mental model before asking you to use it. Workbooks test prediction, causal repair, construction, transfer, and defense. Labs isolate one mechanism. Compiler and design investigations train precise diagnosis. Capstones force ten mechanisms to coexist in one complete product.

## Begin

1. Read [How to study this program](START_HERE.md).
2. Learn the shared [Rust reasoning model](REASONING_MODEL.md).
3. Inspect the [ninety-module course map](COURSE_MAP.md).
4. Use the [skill map](SKILL_MAP.md) to see how each course changes design responsibility.
5. Track actual completion in [PROGRESS.md].

## The nine-course sequence

| Course | Course book | You finish able to… | Capstone |
|---:|---|---|---|
| 1 | [Rust Foundations](01-rust-foundations/course-book/index.md) | Read Rust as a typed language, make ownership visible, model valid states, handle failure explicitly, and finish a complete tested program. | **Taskboard** |
| 2 | [Ownership, Lifetimes, and Memory](02-rust-ownership-lifetimes-memory/course-book/index.md) | Design borrowed APIs, cleanup protocols, shared graphs, interior mutability, representation claims, variance, and pinning from explicit memory relationships. | **Memory Workspace** |
| 3 | [Traits, Generics, and Architectural Design](03-rust-traits-generics-architectural-design/course-book/index.md) | Define lawful contracts, choose static or dynamic polymorphism, compose behavior, encode protocols, and evolve public APIs. | **Review Engine** |
| 4 | [Functional Rust](04-rust-functional-programming/course-book/index.md) | Make callable capability, laziness, traversal, failure, accumulation, structural sharing, and effects explicit enough to reason about composition and cost. | **LedgerFlow** |
| 5 | [Rust Metaprogramming](05-rust-metaprogramming/course-book/index.md) | Use generation only where one checked declaration should own several Rust surfaces or validated build data, while keeping expansion understandable as ordinary Rust. | **CommandForge** |
| 6 | [Rust Systems Programming](06-rust-systems-programming/course-book/index.md) | Cross byte, filesystem, process, allocator, unsafe, ABI, callback, and foreign-resource boundaries without losing earlier guarantees. | **FrameVault** |
| 7 | [Rust Concurrency and Parallelism](07-rust-concurrency-parallelism/course-book/index.md) | Design bounded threaded and data-parallel work whose synchronization, liveness, failure, and final meaning remain explicit across legal schedules. | **BatchWeave** |
| 8 | [Rust Async and Networked Services](08-rust-async-networked-services/course-book/index.md) | Derive future state machines, own Tokio task lifecycles, frame hostile streams, design versioned protocols, enforce capacity, preserve cancellation safety, and build resilient services. | **JobWire** |
| 9 | [Rust Performance and Production Engineering](09-rust-performance-production-engineering/course-book/index.md) | Define falsifiable performance contracts, profile causally, budget memory and data movement, observe and harden services, control overload, secure the supply chain, and ship traceable operable artifacts. | **MetricRail** |

## One course, ten dense days

Each course occupies ten focused study days across two calendar weeks. One module is one full day:

```text
chapter
   ↓
closed-book prediction
   ↓
causal repair
   ↓
focused construction
   ↓
independent laboratory
   ↓
capstone transfer
   ↓
reconstruction and defense
```

Advance only when you can explain the decisive rule and transfer it to a different problem. A passing test suite proves selected behavior, not understanding. An explanation without working code proves vocabulary, not engineering skill. The program requires both.

## What changes in Course 9

Course 8 ends with a correct, bounded asynchronous service. Course 9 asks whether its production claims are true.

Ten permanent questions are added:

1. **Claim:** what user-visible behavior or resource property is being asserted?
2. **Workload:** which input distribution, scale, skew, and environment does the claim cover?
3. **Measurement:** where does observation begin and end, and what noise or bias remains?
4. **Cost:** which CPU, allocation, copying, waiting, contention, or system-call mechanism dominates?
5. **Boundedness:** what limits memory, queues, labels, retries, output, and retained state?
6. **Observability:** which signal answers the operator’s question, and is it authoritative or advisory?
7. **Reliability:** how do admission, retry, degradation, and recovery preserve useful work?
8. **Security:** which assets, boundaries, dependencies, secrets, and privileges can be abused?
9. **Artifact:** which source, lockfile, toolchain, profile, target, and features produced the binary?
10. **Operation:** what capacity, rollout, rollback, runbook, and incident-learning evidence supports deployment?

These questions extend rather than replace ownership, memory, architecture, concurrency, and protocol reasoning.

## Toolchain and dependencies

The program uses Rust 2024 Edition and pins Rust 1.97.1.

- Course 5 pins the procedural-macro ecosystem used to build real derives and DSLs.
- Course 7 pins Rayon for data-parallel work.
- Course 8 pins Tokio, Tokio Util, Bytes, Futures Util, Hyper, Hyper Util, and HTTP Body Util.
- Course 9 pins Criterion, Bytes, Tokio, Tracing, and Tracing Subscriber for benchmarking, shared buffers, service execution, structured diagnostics, and production surfaces.

Exact pins make the teaching release reproducible enough to discuss specific APIs. They do not turn third-party behavior into Rust language guarantees.

See [Source notes](SOURCE_NOTES.md) for primary contracts.

## Repository commands

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

`make proof` is the strongest included route. It requires the pinned Rust toolchain and MkDocs.
