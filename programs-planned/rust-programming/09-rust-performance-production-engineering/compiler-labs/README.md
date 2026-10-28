# Course 9 Compiler and Design Investigations

These eighty specimens test the boundary between what the Rust compiler can reject and what production engineering must review separately.

The set uses five outcome categories:

- `compile-pass` — valid Rust whose type-level claim should compile;
- `compile-fail` — invalid Rust that should fail for the stated causal reason;
- `run-pass` — valid Rust with a deterministic runtime assertion;
- `run-fail` — valid Rust whose deliberate runtime failure demonstrates a boundary;
- `manual-review` — valid Rust that embodies an operationally weak design the compiler cannot reject.

Freeze your prediction before running the specimen. For a compile failure, identify the target rule and the smallest requirement-preserving repair. For a manual review, explain why compilation is insufficient: the defect may be an unbounded queue, leaked high-cardinality labels, unstable release metadata, hidden setup cost, weak retry policy, or a security disclosure.

Run the set through the program-level compiler-lab runner. Direct cases are compiled with warnings denied, so incidental warnings cannot stand in for the intended result.
