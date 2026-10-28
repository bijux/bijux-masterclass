# Final review — Course 4: Functional Rust

## Part A — trace dataflow

For each pipeline, write item type, cardinality, order, ownership, stopping, and allocation after every stage. Include:

- borrowed filter then map;
- `filter_map` over parse attempts;
- `flat_map` over grouped records;
- `take_while` followed by `collect`;
- `try_fold` with a prefix invariant;
- `scan` emitting running metrics.

## Part B — callable contracts

1. Derive `Fn`, `FnMut`, or `FnOnce` from four closure bodies.
2. Explain why `move` and `FnOnce` are not synonyms.
3. Show a deferred closure that extends a borrow and repair the API.
4. Replace an overboxed callback boundary with a generic parameter.
5. Identify a requirement that genuinely needs `Box<dyn Fn...>`.

## Part C — failure and effect policy

Choose and justify policy for:

- optional configuration;
- malformed rows where all diagnostics are required;
- a fatal header error;
- duplicate events where first occurrence wins;
- a report writer failure after pure analysis succeeds.

Then separate the pure decision core from filesystem, clock, terminal, and process effects. Represent intended effects as data where replay or failure injection is valuable.

## Part D — law and cost review

Write law tests for identity, composition, order preservation, and error propagation for one combinator. Produce a counterexample to an invalid law. State cost as an exact bound, asymptotic bound, allocation statement under conditions, or measurement—not as “zero cost.”

## Part E — independent construction

Build a route-analysis engine that parses fallible input, exposes borrowed lazy traversal, computes streaming metrics with explicit empty-input behavior, retains persistent history through structural sharing, and renders deterministic output through an effect shell.

Course 4 is complete when a loop and an iterator chain can be compared by contract and clarity rather than ideology.
