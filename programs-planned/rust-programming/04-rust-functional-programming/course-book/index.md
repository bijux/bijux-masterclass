# Course 4 — Functional Rust

## Closures, Iterators, Fallible Dataflow, and Effect Isolation

Make callable capability, laziness, traversal, failure, accumulation, structural sharing, effects, and cost explicit enough that a reader can reason about the whole dataflow without reconstructing hidden mutation.

## Why this course exists

Functional Rust is not a contest to remove every loop or every mutation. It is a discipline for exposing how data is captured, requested, transformed, rejected, accumulated, shared, and finally connected to effects. Course 3 provides the trait and architectural joints; this course makes information flow through those joints visible. The goal is pipelines whose ownership, cardinality, order, failure policy, and cost can be defended stage by stage.

## Before you begin

Course 3, including generic and trait bounds, associated types, static and dynamic dispatch, adapters, composition, and public API reasoning.

Keep a closure-capture ledger, iterator stage map, failure-policy matrix, accumulator invariant, and cost ledger beside the code. The record changes shape as the course advances, but its purpose is constant: make the decisive relationship visible before syntax hides it.

## What you will be able to do

- Distinguish function items, function pointers, and closure types; derive capture mode and the resulting `Fn`, `FnMut`, or `FnOnce` capability.
- Design callback bounds from invocation count, retained state, movement, and concurrency assumptions rather than choosing the broadest callable trait.
- Explain the pull-based iterator model, laziness, iterator state, source ownership, exhaustion, and why adapters do no work without a consumer.
- Trace item type, cardinality, order, ownership, stopping behavior, and allocation through `map`, `filter`, `filter_map`, `flatten`, `flat_map`, `take`, `skip`, and `collect`.
- Choose explicit loops when state, early exit, or diagnostics are clearer than a chain, and explain that choice without treating loops as a failure of style.
- Design folds and scans from a prefix invariant; distinguish `fold`, `reduce`, `try_fold`, `scan`, `sum`, and short-circuiting consumers.
- Select among fail-fast traversal, omission, recovery, defaults, warning accumulation, and full diagnostic accumulation as explicit product policies.
- Use `Option`, `Result`, `transpose`, fallible `collect`, and custom accumulation without losing source order or error context.
- Implement lawful iterators and `IntoIterator` surfaces with correct ownership, exhaustion, size hints, and collection behavior.
- Use `FromIterator` and `Extend` to express construction protocols while preserving validation and duplicate policy.
- Transform recursive data by shape, use persistent updates and structural sharing where version retention is a requirement, and avoid accidental full copies.
- Separate deterministic domain decisions from filesystem, terminal, clock, randomness, process, and other effects through a functional core and effect shell.
- State and test combinator laws with counterexamples, including identity, composition, order, failure, and duplication behavior.
- Make cost claims only for named operations and data shapes; distinguish asymptotic complexity, allocation, copying, and benchmark-dependent performance.
- Design an integrated dataflow system whose capture, traversal, failure, reduction, sharing, ordering, and effect choices can be read and defended independently.

## What this course deliberately leaves for later

The course is single-threaded and synchronous. Parallel iterators, channels, async streams, networking, and measurement-driven optimization are reserved for Courses 7–9.

## Ten-day route

1. [Module 31: Closures, Capture, and Callable Contracts](module-31-closures-capture-and-callable-contracts/index.md) — What does a closure capture, which callable traits does it implement, and what invocation contract should an API require?
2. [Module 32: The Iterator Model](module-32-the-iterator-model/index.md) — What state does an iterator own, when does work happen, and what is consumed by each call to next?
3. [Module 33: Iterator Algebra and Pipeline Shape](module-33-iterator-algebra-and-pipeline-shape/index.md) — How do adapters change item type, cardinality, order, ownership, and stopping behavior across a pipeline?
4. [Module 34: Folds, Scans, and Short-Circuiting](module-34-folds-scans-and-short-circuiting/index.md) — What invariant does an accumulator maintain, and when should a traversal continue, emit intermediate state, or stop early?
5. [Module 35: Option, Result, and Fallible Traversal](module-35-option-result-and-fallible-traversal/index.md) — Should a fallible traversal skip, fail fast, recover, accumulate diagnostics, or continue with an explicit default?
6. [Module 36: Custom Iterators and Collection Protocols](module-36-custom-iterators-and-collection-protocols/index.md) — What laws must a custom traversal obey, and who owns the collection when iteration begins?
7. [Module 37: Recursive Data and Structural Sharing](module-37-recursive-data-and-structural-sharing/index.md) — How can recursive values be transformed without hiding ownership, rebuilding cost, or structural sharing?
8. [Module 38: Functional Core and Effect Isolation](module-38-functional-core-and-effect-isolation/index.md) — Which decisions can remain pure, which effects must occur at the boundary, and what data should cross between them?
9. [Module 39: Combinator Laws and Cost Models](module-39-combinator-laws-and-cost-models/index.md) — What semantic laws should a combinator preserve, and what can honestly be claimed about evaluation and cost?
10. [Module 40: Functional Architecture Synthesis](module-40-functional-architecture-synthesis/index.md) — How do closure, iterator, error, reduction, structural-sharing, and effect decisions compose into a readable whole system?

## How the learning surfaces fit

The chapter is the authoritative explanation. The workbook exposes the model you actually hold through prediction, repair, construction, transfer, and defense. The independent lab removes accumulated capstone complexity so one mechanism remains visible. The capstone increment then asks that mechanism to coexist with every earlier decision.

The cumulative product is **LedgerFlow**: a deterministic ledger-event analyzer with fallible parsing, explicit row policy, prefix-safe reduction, lazy borrowed queries, persistent audit history, and a functional core around a narrow effect shell. Do not read the complete implementation before attempting the corresponding increment; the value of the capstone is the sequence of design decisions, not possession of the finished source.

Use the [compiler investigations](../compiler-labs/README.md), the [ten-day study plan](study-plan.md), the [LedgerFlow engineering guide](capstone.md), the [course reference](reference.md), and the [independent final review](final-review.md).

## Completion standard

The course is complete when you can satisfy the public behavior, explain the decisive rule without notes, repair a misleading implementation without weakening its requirement, and transfer the mechanism to the final independent product. A passing test suite without a causal model is incomplete; a persuasive explanation without working evidence is also incomplete.

## Course handoff

Course 5 shifts from composing runtime values to generating source surfaces while preserving the same requirements for authority, failure, and comprehensibility.

[Return to the program start](../../README.md) · [Open the ninety-module map](../../COURSE_MAP.md)
