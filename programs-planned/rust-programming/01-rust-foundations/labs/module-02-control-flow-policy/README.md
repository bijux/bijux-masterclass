# Laboratory 2 — Control-Flow Policy Engine

This is the independent product for **Course 1, Module 2: Control Flow, Functions, and Invariants**. Read the [module chapter](../../course-book/module-02-control-flow-functions-and-invariants/index.md) and complete its [workbook](../../course-book/module-02-control-flow-functions-and-invariants/workbook.md) before consulting the reference implementation.

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

## Working route

Use the common [laboratory method](../../../START_HERE.md#laboratory-method). Work from `starter/`, add the first adversarial test before the design-changing repair, and complete the workbook’s transfer problem before reading the reference implementation.

```bash
cd starter
cargo test
cargo fmt -- --check
cargo clippy -- -D warnings
```

## Completion check

The laboratory is complete when the required behavior and failure paths pass and you can answer this question without the chapter:

> How can control flow make every path, boundary, and loop invariant visible enough to test and review?

Demonstrate the same mechanism once in the workbook’s unrelated transfer domain. Name one shortcut that would compile or pass the happy path while weakening the product contract.

## Reference comparison

Open [`solution/`](solution/) only after your implementation works or you have written a precise blocker. For **Control-Flow Policy Engine**, compare accepted and rejected inputs, state after failure, ownership or authority, deterministic behavior, public surface, and justified cost before comparing syntax.
