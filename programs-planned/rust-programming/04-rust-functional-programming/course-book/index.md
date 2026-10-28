# Course 4 — Functional Rust

## Closures, Iterators, Fallible Dataflow, and Effect Isolation

## The promise

Course 4 develops a functional style that remains honest about ownership and mutation. You learn to derive closure capabilities, read iterator pipelines as state machines, choose reductions and short-circuiting deliberately, compose fallible traversal, implement custom iteration, and isolate effects around a deterministic core.

> **Governing question:** How can Rust make capture, traversal, cardinality, ordering, failure, accumulation, structural sharing, effects, and cost visible in one dataflow?

Course 3 established lawful contracts and explicit variation boundaries. Course 4 keeps those boundaries and turns the reader’s attention to flow: what closures capture, what iterators consume, how failures travel, which state a reduction preserves, where effects occur, and what each transformation costs.

## Before Day 1

You should be able to design trait boundaries, use static and dynamic dispatch, understand ownership through collections, and model state explicitly.

From a blank page, sketch one earlier product or a comparable program. Mark an owner, a valid and invalid state, a failure path, cleanup, and a public promise. Repair any relationship you cannot explain before adding this course’s mechanisms.

## Outcomes

- Distinguish function items, function pointers, and anonymous closure types.
- Explain the distinct roles of `IntoIterator`, `Iterator`, adapters, and consumers.
- Derive the item type and cardinality effect of common iterator adapters.
- Design a fold accumulator with a precise prefix invariant.
- Compose optional and fallible transformations while preserving ownership and error meaning.
- Implement a correct custom `Iterator` by defining state and exhaustion behavior.
- Define recursive algebraic data with the appropriate indirection.
- Separate deterministic domain decisions from filesystem, time, environment, and terminal effects.
- Design domain combinators that preserve type and error meaning.
- Produce a transformation map that identifies source, shape, ownership, failure, state, and effect boundaries.
- Integrate all ten mechanisms in LedgerFlow without creating competing authorities.
- Complete and defend an unseen change using a whole-pipeline architecture map.

## The ten-day line

| Day | Module | Governing question | Capability that must become visible | Laboratory |
|---:|---|---|---|---|
| 1 | [31 — Closures, Capture, and Callable Contracts](./module-31-closures-capture-and-callable-contracts/index.md) | What does a closure capture, which callable traits does it implement, and what invocation contract should an API require? | **Distinguish function items, function pointers, and anonymous closure types.** | [Closure Policy Matrix](../labs/module-01-closure-policy-matrix/README.md) |
| 2 | [32 — The Iterator Model](./module-32-the-iterator-model/index.md) | What state does an iterator own, when does work happen, and what is consumed by each call to next? | **Explain the distinct roles of `IntoIterator`, `Iterator`, adapters, and consumers.** | [Lazy Log Query](../labs/module-02-lazy-log-query/README.md) |
| 3 | [33 — Iterator Algebra and Pipeline Shape](./module-33-iterator-algebra-and-pipeline-shape/index.md) | How do adapters change item type, cardinality, order, ownership, and stopping behavior across a pipeline? | **Derive the item type and cardinality effect of common iterator adapters.** | [Record-Shaping Pipeline](../labs/module-03-record-shaping-pipeline/README.md) |
| 4 | [34 — Folds, Scans, and Short-Circuiting](./module-34-folds-scans-and-short-circuiting/index.md) | What invariant does an accumulator maintain, and when should a traversal continue, emit intermediate state, or stop early? | **Design a fold accumulator with a precise prefix invariant.** | [Streaming Metrics](../labs/module-04-streaming-metrics/README.md) |
| 5 | [35 — Option, Result, and Fallible Traversal](./module-35-option-result-and-fallible-traversal/index.md) | Should a fallible traversal skip, fail fast, recover, accumulate diagnostics, or continue with an explicit default? | **Compose optional and fallible transformations while preserving ownership and error meaning.** | [Resilient Import](../labs/module-05-resilient-import/README.md) |
| 6 | [36 — Custom Iterators and Collection Protocols](./module-36-custom-iterators-and-collection-protocols/index.md) | What laws must a custom traversal obey, and who owns the collection when iteration begins? | **Implement a correct custom `Iterator` by defining state and exhaustion behavior.** | [Custom Cursors](../labs/module-06-custom-cursors/README.md) |
| 7 | [37 — Recursive Data and Structural Sharing](./module-37-recursive-data-and-structural-sharing/index.md) | How can recursive values be transformed without hiding ownership, rebuilding cost, or structural sharing? | **Define recursive algebraic data with the appropriate indirection.** | [Persistent History](../labs/module-07-persistent-history/README.md) |
| 8 | [38 — Functional Core and Effect Isolation](./module-38-functional-core-and-effect-isolation/index.md) | Which decisions can remain pure, which effects must occur at the boundary, and what data should cross between them? | **Separate deterministic domain decisions from filesystem, time, environment, and terminal effects.** | [Deterministic Batch Runner](../labs/module-08-deterministic-batch-runner/README.md) |
| 9 | [39 — Combinator Laws and Cost Models](./module-39-combinator-laws-and-cost-models/index.md) | What semantic laws should a combinator preserve, and what can honestly be claimed about evaluation and cost? | **Design domain combinators that preserve type and error meaning.** | [Combinator Contracts](../labs/module-09-combinator-contracts/README.md) |
| 10 | [40 — Functional Architecture Synthesis](./module-40-functional-architecture-synthesis/index.md) | How do closure, iterator, error, reduction, structural-sharing, and effect decisions compose into a readable whole system? | **Produce a transformation map that identifies source, shape, ownership, failure, state, and effect boundaries.** | [Route Analysis Engine](../labs/module-10-route-analysis-engine/README.md) |

The table is a dependency chain, not a menu. A later module may use an earlier mechanism but may not silently weaken its ownership, failure, ordering, capacity, safety, compatibility, or evidence contract.

## Decision rules

| Decision | Rule used throughout this course |
|---|---|
| Closure bound | Derive `Fn`, `FnMut`, or `FnOnce` from invocation count and capture behavior. |
| Iterator ownership | State whether the source is borrowed, mutably borrowed, or consumed and what item type follows. |
| Failure policy | Choose fail-fast, skip, recover, or accumulate diagnostics explicitly. |
| Reduction | Write the accumulator invariant before replacing a loop with `fold` or `try_fold`. |
| Effect boundary | Keep deterministic decisions pure enough to test without the filesystem, clock, terminal, or process. |

Use these rules during prediction and review. When a rule does not decide the case, write the missing product requirement instead of selecting an API by habit.

## The reasoning record

The ten module-specific records culminate in a **whole-pipeline architecture map**. Trace capture, item shape, cardinality, ordering, failure, accumulator state, effect, and cost through the complete dataflow. Keep the record small enough to inspect but complete enough to expose the first unsupported assumption.

## Scope and handoff

The course uses ordinary functions, closures, iterators, and immutable public models. It does not treat mutation as forbidden, and it postpones macro construction, parallel iteration, async streams, and benchmark-driven optimization.

Course 5 moves repetition and cross-surface consistency to compile time, but only when one declaration genuinely deserves authority over several generated Rust surfaces.

## Capstone — LedgerFlow

LedgerFlow parses append-only ledger events, preserves diagnostics and source order, reduces valid events into deterministic state, retains an immutable audit history, exposes borrowed queries, and keeps filesystem and terminal effects outside the core.

Open the [engineering guide](capstone.md) before Day 1 so the final architecture is visible. Implement only the current increment. The independent laboratory remains separate so that the mechanism can be learned without hiding behind accumulated capstone code.

## Completion

The course is complete when you can build and defend:

> Build a deterministic route-analysis engine whose parser, fallible transformation, reductions, persistent history, borrowed queries, and effect shell can be tested independently.

and then change the capstone under this constraint:

> Add balance checkpoints to LedgerFlow without introducing a second source of truth for event order or reducer semantics.

A passing test suite is necessary. It is not sufficient unless you can explain why the tests are capable of falsifying the claim and which target-, scheduler-, workload-, peer-, or policy-dependent facts remain outside them.

## Continue

- [Ten-day plan](study-plan.md)
- [Module 31 — Closures, Capture, and Callable Contracts](./module-31-closures-capture-and-callable-contracts/index.md)
- [LedgerFlow engineering guide](capstone.md)
- [Course reference](reference.md)
- [Final review](final-review.md)
- [Compiler and design investigations](../compiler-labs/README.md)
- [Independent laboratories](../labs/)
