# Course 4 Reference Desk — Functional Rust

Use this page while designing or reviewing. It is a decision aid, not a replacement for the module explanations.

## Governing question

> How can Rust make capture, traversal, cardinality, ordering, failure, accumulation, structural sharing, effects, and cost visible in one dataflow?

## Working record

Keep a capture map, iterator stage table, cardinality and order trace, failure-policy matrix, accumulator invariant, structural-sharing graph, effect boundary, and qualitative cost model. A design is not ready when the record still contains unnamed owners, contradictory states, implicit failure, accidental order, unbounded accumulation, or a claim with no matching evidence.

## Decision rules

| Decision | Rule |
|---|---|
| Closure bound | Derive `Fn`, `FnMut`, or `FnOnce` from invocation count and capture behavior. |
| Iterator ownership | State whether the source is borrowed, mutably borrowed, or consumed and what item type follows. |
| Failure policy | Choose fail-fast, skip, recover, or accumulate diagnostics explicitly. |
| Reduction | Write the accumulator invariant before replacing a loop with `fold` or `try_fold`. |
| Effect boundary | Keep deterministic decisions pure enough to test without the filesystem, clock, terminal, or process. |

## Module quick reference

| Module | Mechanism | Minimum usable outcome |
|---:|---|---|
| 31 | Closures, Capture, and Callable Contracts | Distinguish function items, function pointers, and anonymous closure types |
| 32 | The Iterator Model | Explain the distinct roles of `IntoIterator`, `Iterator`, adapters, and consumers |
| 33 | Iterator Algebra and Pipeline Shape | Derive the item type and cardinality effect of common iterator adapters |
| 34 | Folds, Scans, and Short-Circuiting | Design a fold accumulator with a precise prefix invariant |
| 35 | Option, Result, and Fallible Traversal | Compose optional and fallible transformations while preserving ownership and error meaning |
| 36 | Custom Iterators and Collection Protocols | Implement a correct custom `Iterator` by defining state and exhaustion behavior |
| 37 | Recursive Data and Structural Sharing | Define recursive algebraic data with the appropriate indirection |
| 38 | Functional Core and Effect Isolation | Separate deterministic domain decisions from filesystem, time, environment, and terminal effects |
| 39 | Combinator Laws and Cost Models | Design domain combinators that preserve type and error meaning |
| 40 | Functional Architecture Synthesis | Produce a transformation map that identifies source, shape, ownership, failure, state, and effect boundaries |

## Claim boundary

Separate language guarantees, library contracts, product policy, target observations, and measured artifact facts. When an exact API or version detail matters, follow the primary source from [Source Notes](../../SOURCE_NOTES.md).

Functional Rust is not “never mutate” and not “replace every loop with adapters.” It is the discipline of making dataflow, state, failure, effects, and cost explicit.

## Closure ledger

For each closure, record:

```text
captured value | by shared borrow / mutable borrow / move | body action |
maximum calls | required trait (`Fn`, `FnMut`, `FnOnce`) | escape lifetime
```

`move` controls capture ownership; it does not by itself mean the closure consumes captures when called. The body determines callable capability. Require the weakest sufficient trait.

## Iterator stage map

For every stage, record:

| Stage | Input item | Output item | Cardinality | Order | Ownership | Stops? | Allocates? |
|---|---|---|---|---|---|---|---|

Iterator adapters are lazy until a consumer drives them. `map` preserves cardinality; `filter` may reduce it; `flat_map` may expand it; `take` bounds demand; `find` and `any` may stop early; `collect` chooses a destination and performs allocation according to that destination.

Do not collect merely to appease the borrow checker. First ask whether a shorter borrow scope, a different stage order, or a named iterator solves the real problem.

## Reduction choices

- `fold`: one final accumulator;
- `scan`: emit intermediate states while retaining hidden state;
- `try_fold`: accumulate while short-circuiting on failure;
- `ControlFlow`: explicit continue/break result from traversal;
- ordinary loop: often clearest when several state transitions or error branches must be reviewed together.

State the prefix invariant: after processing the first *n* inputs, exactly what does the accumulator represent?

## Fallible traversal policy

Choose policy before choosing combinators:

| Policy | Typical shape |
|---|---|
| absence is ordinary | `Option<T>` |
| first error stops traversal | iterator of `Result` collected into `Result<Vec<_>, E>` or `try_fold` |
| invalid rows are skipped with evidence | `(accepted, diagnostics)` accumulator |
| all independent validation errors are needed | validate fields/rows and accumulate structured diagnostics |
| recover with an explicit default | `unwrap_or_else`, `or_else`, or domain-specific branch with documented semantics |

Never turn malformed input into “missing” merely to simplify the type.

## Custom traversal contracts

A custom iterator owns traversal state and must advance or terminate. Once exhausted, repeated `next` calls should remain `None` when the type claims fusion. `size_hint` is a bound, not a promise unless exactness is established. Implement `IntoIterator` for borrowed, mutably borrowed, and owned forms only when each ownership story is useful.

## Structural transformation

Recursive data often requires rebuilding the path from the changed node to the root. Structural sharing keeps untouched subtrees behind shared ownership. State what is copied, what is shared, and the asymptotic and allocation cost. Persistent data is not free mutation; it moves cost into controlled rebuilding and reference management.

## Functional core and effect shell

Keep deterministic decisions in functions that receive values and return values or planned effects. The shell performs files, clocks, randomness, terminal output, processes, or network actions. This makes failure injection, replay, and tests ordinary.

## Laws and cost

A combinator should have a law or at least a precise behavioral contract. Test identity, composition, order, error propagation, and duplicate behavior with counterexamples. Make cost claims in the right category: exact bound, asymptotic bound, allocation count under stated conditions, or observed measurement.

## Course 4 readiness

You are ready for Course 5 when you can derive closure bounds, trace lazy demand and item shape, state reduction invariants, select a failure policy, implement lawful custom traversal, explain structural-sharing cost, isolate effects, and reject a clever combinator whose laws or evaluation behavior are unclear.
