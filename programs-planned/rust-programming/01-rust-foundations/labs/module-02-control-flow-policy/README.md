# Laboratory 2 — Control-Flow Policy Engine

**Course 1 · Module 2: Control Flow, Functions, and Invariants**

[Chapter](../../course-book/module-02-control-flow-functions-and-invariants/index.md) · [Workbook](../../course-book/module-02-control-flow-functions-and-invariants/workbook.md) · [Taskboard guide](../../course-book/capstone.md) · [Program method](../../../START_HERE.md#laboratory-method)

## Why this laboratory exists

The laboratory isolates one decision from **Control Flow, Functions, and Invariants**: How can control flow make every path, boundary, and loop invariant visible enough to test and review? The product must make **Treat if and loop constructs as typed expressions and prove branch agreement and loop result behavior** visible through its public behavior, failure state, and tests rather than through explanatory comments alone.

Work from `starter/` with a **control-flow table** beside the code. Preserve the first failing case and your original design before reading `solution/`; the reference is a comparison surface, not a sequence of missing lines.

## Learning target

The laboratory asks one focused version of the module’s governing question:

> How can control flow make every path, boundary, and loop invariant visible enough to test and review?

By the end, the answer must be visible in the public API, failure behavior, adversarial tests, and design explanation—not merely in comments.

## Product

### Product contract

Build a pure library that simulates textual work-item operations before typed domain modeling is available.

Required API:

```rust
pub fn severity_name(severity: u8) -> &'static str;
pub fn title_is_valid(title: &str) -> bool;
pub fn operation_is_allowed(state: &str, operation: &str) -> bool;
pub fn simulate(initial_state: &str, operations: &[&str]) -> (String, usize, usize);
pub fn first_legal_operation<'a>(state: &str, operations: &'a [&str]) -> Option<&'a str>;
```

### Policy

- severity 0–3 low, 4–7 normal, >=8 high;
- title nonblank, trimmed, <=80 characters, no tabs/newlines;
- legal transitions: todo/start, doing/done, done/reopen;
- every other state-operation pair is rejected;
- rejected operation leaves state unchanged;
- accepted + rejected equals number of operations;
- search returns the first legal operation in input order or `None`.

### Required test matrix

Build a table over states `todo`, `doing`, `done`, `corrupt` and operations `start`, `done`, `reopen`, `remove`. Exactly three pairs are legal.

Test simulations:

1. complete cycle;
2. invalid first operation followed by valid cycle;
3. all invalid;
4. invalid initial state;
5. empty operation list.

### Termination arguments

- `simulate` traverses a finite slice once;
- `first_legal_operation` traverses a finite slice and returns early or reaches its end.

Record these explicitly. “It obviously terminates” is not a proof habit.

### Deliberate limitation

The string representation permits arbitrary states and operations and duplicates transition spellings. Do not hide this weakness. In the design note, enumerate invalid values that the type system currently permits. Module 5 must remove them.

### Proof route

```bash
cargo fmt --all -- --check
cargo check --all-targets
cargo clippy --all-targets -- -D warnings
cargo test --all-targets
cargo run --quiet
```

Reference: `labs/module-02-control-flow-policy/solution/`.

## Design record

Before implementation, complete this record for **Control-Flow Policy Engine**:

| Question | Required answer |
|---|---|
| Module decision | How does **Control Flow, Functions, and Invariants** answer its governing question in this product? |
| Authority | Which type or component decides the main rule? |
| Valid states | Which states may be observed through the public API? |
| Rejection | What exact input or transition is refused, and what remains unchanged? |
| Ownership | Who owns every resource before, during, and after the decisive operation? |
| Order and bounds | Which sequence, capacity, lifetime, or compatibility limit is promised? |
| Evidence | Which test, compiler case, model, trace, or review could falsify the claim? |

Use the **control-flow table** to answer the table. Then add at least three adversarial cases: one at the smallest boundary, one at the largest accepted or rejected boundary, and one that leaves partial work before failure. For each, state the final observable state before running the test.

## Working route

1. Read the product contract and run the starter’s baseline checks for **Control-Flow Policy Engine**.
2. Draw the smallest **control-flow table** capable of deciding the governing question.
3. Add a causal negative or adversarial test that fails for the intended relationship.
4. Implement one invariant at a time; after each failure, record state, ownership, cleanup, order, and capacity.
5. Complete the transfer task in a domain unrelated to Taskboard so that syntax cannot substitute for understanding.
6. Compare with `solution/` by contract, proof boundary, and rejected shortcuts before comparing implementation shape.

## Completion check

The laboratory is complete when the required behavior and failure paths pass and you can answer this question without the chapter:

For **Laboratory 2 — Control-Flow Policy Engine**, answer the learning-target question from the completed product. Point to the public boundary that carries the rule, the adversarial case that would falsify it, and one fact the test suite does not establish.

Demonstrate the same mechanism once in the workbook’s unrelated transfer domain. Name one shortcut that would compile or pass the happy path while weakening the product contract.

## Reference comparison

Open [`solution/`](solution/) only after your implementation works or you have written a precise blocker. For **Control-Flow Policy Engine**, compare accepted and rejected inputs, state after failure, ownership or authority, deterministic behavior, public surface, and justified cost before comparing syntax.

## Completion standard

The laboratory is complete when the implementation and tests demonstrate:

- Treat if and loop constructs as typed expressions and prove branch agreement and loop result behavior.
- Select for, while, or loop from termination knowledge and data shape, then state the loop invariant and variant.
- Design functions with explicit preconditions, postconditions, total behavior, and guard clauses.

Also preserve one ordinary success trace, one causal rejection or partial-failure trace, cleanup, deterministic behavior where promised, and one explicit limit on what the tests establish. A happy-path implementation or an explanation that merely names the API is incomplete.

## Independent transfer

Rebuild the decisive relationship from Module 2 in a different product. Change the domain types, names, public behavior, and failure mode while retaining the same **control-flow table**. Defend why your design is simpler than one plausible alternative under the new requirements.
