# Course 4 — Functional Rust

## Closures, Iterators, Fallible Dataflow, and Effect Isolation

Course 4 develops a functional style that remains honest about ownership and mutation. You learn to derive closure capabilities, read iterator pipelines as state machines, choose reductions and short-circuiting deliberately, compose fallible traversal, implement custom iteration, and isolate effects around a deterministic core.

> **Governing question:** How can Rust make capture, traversal, cardinality, ordering, failure, accumulation, structural sharing, effects, and cost visible in one dataflow?

## Entry point

You should be able to design trait boundaries, use static and dynamic dispatch, understand ownership through collections, and model state explicitly.

The immediate prerequisite is [Course 3: Traits, Generics, and Architectural Design](../03-rust-traits-generics-architectural-design/course-book/index.md). Entering mid-program is reasonable only when you can complete the previous course’s final review and one independent construction without following its solution.

## Ten-day route

| Day | Module | Capability added | Independent laboratory |
|---:|---|---|---|
| 1 | [31 — Closures, Capture, and Callable Contracts](course-book/module-31-closures-capture-and-callable-contracts/index.md) | Distinguish function items, function pointers, and anonymous closure types | [Closure Policy Matrix](labs/module-01-closure-policy-matrix/README.md) |
| 2 | [32 — The Iterator Model](course-book/module-32-the-iterator-model/index.md) | Explain the distinct roles of `IntoIterator`, `Iterator`, adapters, and consumers | [Lazy Log Query](labs/module-02-lazy-log-query/README.md) |
| 3 | [33 — Iterator Algebra and Pipeline Shape](course-book/module-33-iterator-algebra-and-pipeline-shape/index.md) | Derive the item type and cardinality effect of common iterator adapters | [Record-Shaping Pipeline](labs/module-03-record-shaping-pipeline/README.md) |
| 4 | [34 — Folds, Scans, and Short-Circuiting](course-book/module-34-folds-scans-and-short-circuiting/index.md) | Design a fold accumulator with a precise prefix invariant | [Streaming Metrics](labs/module-04-streaming-metrics/README.md) |
| 5 | [35 — Option, Result, and Fallible Traversal](course-book/module-35-option-result-and-fallible-traversal/index.md) | Compose optional and fallible transformations while preserving ownership and error meaning | [Resilient Import](labs/module-05-resilient-import/README.md) |
| 6 | [36 — Custom Iterators and Collection Protocols](course-book/module-36-custom-iterators-and-collection-protocols/index.md) | Implement a correct custom `Iterator` by defining state and exhaustion behavior | [Custom Cursors](labs/module-06-custom-cursors/README.md) |
| 7 | [37 — Recursive Data and Structural Sharing](course-book/module-37-recursive-data-and-structural-sharing/index.md) | Define recursive algebraic data with the appropriate indirection | [Persistent History](labs/module-07-persistent-history/README.md) |
| 8 | [38 — Functional Core and Effect Isolation](course-book/module-38-functional-core-and-effect-isolation/index.md) | Separate deterministic domain decisions from filesystem, time, environment, and terminal effects | [Deterministic Batch Runner](labs/module-08-deterministic-batch-runner/README.md) |
| 9 | [39 — Combinator Laws and Cost Models](course-book/module-39-combinator-laws-and-cost-models/index.md) | Design domain combinators that preserve type and error meaning | [Combinator Contracts](labs/module-09-combinator-contracts/README.md) |
| 10 | [40 — Functional Architecture Synthesis](course-book/module-40-functional-architecture-synthesis/index.md) | Produce a transformation map that identifies source, shape, ownership, failure, state, and effect boundaries | [Route Analysis Engine](labs/module-10-route-analysis-engine/README.md) |

The route is cumulative. Day 1 establishes this course’s vocabulary and Day 10 requires an architectural change that preserves all earlier guarantees.

## Working method

Trace capture, item shape, cardinality, ordering, failure, accumulator state, effect, and cost through the complete dataflow. Use the module-specific reasoning record named in each chapter. Freeze predictions before compiling, preserve causal diagnostics, and compare the lab reference only after recording your own design.

## Capstone — LedgerFlow

LedgerFlow parses append-only ledger events, preserves diagnostics and source order, reduces valid events into deterministic state, retains an immutable audit history, exposes borrowed queries, and keeps filesystem and terminal effects outside the core.

The [engineering guide](course-book/capstone.md) supplies the ten integration steps. The executable [capstone directory](capstone/README.md) contains the product and tests. Each increment must name the changed invariant, the component that owns it, state after failure, and the earlier guarantee that must remain unchanged.

## Scope

The course uses ordinary functions, closures, iterators, and immutable public models. It does not treat mutation as forbidden, and it postpones macro construction, parallel iteration, async streams, and benchmark-driven optimization.

Course 5 moves repetition and cross-surface consistency to compile time, but only when one declaration genuinely deserves authority over several generated Rust surfaces.

## Exit standard

Complete this independent construction:

> Build a deterministic route-analysis engine whose parser, fallible transformation, reductions, persistent history, borrowed queries, and effect shell can be tested independently.

Then complete this capstone extension:

> Add balance checkpoints to LedgerFlow without introducing a second source of truth for event order or reducer semantics.

The next step is [Course 5: Rust Metaprogramming](../05-rust-metaprogramming/course-book/index.md).

## Reading and execution routes

- [Course book](course-book/index.md)
- [Ten-day study plan](course-book/study-plan.md)
- [Course reference](course-book/reference.md)
- [Final review](course-book/final-review.md)
- [Compiler and design investigations](compiler-labs/README.md)
- [Laboratories](labs/)

```bash
make static-proof
make compiler-labs
make check
make test
make starters
make docs
make proof
```

Static inspection and compilation answer different questions. The strongest completion route uses the pinned toolchain, executes tests and investigations, renders the book, and preserves the resulting evidence with the code under review.
