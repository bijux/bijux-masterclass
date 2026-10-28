# Course 4 reference — Functional Rust

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
