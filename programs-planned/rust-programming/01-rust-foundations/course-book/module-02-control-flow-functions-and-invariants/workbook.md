# Workbook — Module 02: Control Flow, Functions, and Invariants

[Return to the chapter](index.md) · [Open the Taskboard engineering guide](../capstone.md) · [Open solutions only after attempting the work](solutions.md)

This workbook tests whether you can use **Control Flow, Functions, and Invariants** without relying on surface syntax. Keep the module question in view: *How can control flow make every path, boundary, and loop invariant visible enough to test and review?* For every task, identify the program point where the decisive type, ownership, dispatch, failure, or cost relationship is established. Compile only after committing to a prediction, and preserve the smallest counterexample that changes your model.

## Part 1 — Predict

For each specimen, write a five-part diagnosis: expected outcome; decisive expression or signature; governing rule; smallest requirement-preserving repair; and one tempting change that would compile while weakening the design. Tie every answer to **Control Flow, Functions, and Invariants** rather than quoting a diagnostic without explaining its cause.

| # | Specimen | Your prediction |
|---:|---|---|
| 1 | [`01-break-values-agree.rs`](../../compiler-labs/module-02/01-break-values-agree.rs) | Pass or fail? What exact rule decides? |
| 2 | [`02-accumulator-needs-mutation.rs`](../../compiler-labs/module-02/02-accumulator-needs-mutation.rs) | Pass or fail? What exact rule decides? |
| 3 | [`03-while-needs-bool.rs`](../../compiler-labs/module-02/03-while-needs-bool.rs) | Pass or fail? What exact rule decides? |
| 4 | [`04-return-expression-lost.rs`](../../compiler-labs/module-02/04-return-expression-lost.rs) | Pass or fail? What exact rule decides? |
| 5 | [`05-loop-result-needs-context.rs`](../../compiler-labs/module-02/05-loop-result-needs-context.rs) | Pass or fail? What exact rule decides? |
| 6 | [`06-range-end-is-exclusive.rs`](../../compiler-labs/module-02/06-range-end-is-exclusive.rs) | Pass or fail? What exact rule decides? |

Run all specimens for this course from the course root with:

```bash
python3 ../tools/run_compiler_labs.py 01-rust-foundations
```

## Part 2 — Diagnose and repair


The following simulator has both compile errors and behavioral defects:

```rust
fn allowed(state: &str, operation: &str) -> bool {
    if state == "todo" {
        operation == "start";
    } else if state == "doing" {
        operation == "done"
    } else {
        operation == "reopen"
    }
}

fn simulate(operations: &[&str]) -> (&str, usize, usize) {
    let state = "todo";
    let accepted = 0;
    let rejected = 0;

    for operation in operations {
        if allowed(state, operation) {
            accepted += 1;
            if *operation == "start" { state = "doing"; }
            if *operation == "done" { state = "done"; }
            if *operation == "reopen" { state = "todo"; }
        }
        rejected += 1;
    }
    (state, accepted, rejected)
}
```

### Compile-level repairs

- remove the semicolon from `operation == "start"`;
- mark `state`, `accepted`, and `rejected` mutable;
- state returned text has a static lifetime here because it is always a literal; `&'static str` is an honest explicit return type.

### Behavioral repair

The original increments `rejected` for every operation, including accepted ones. Use an explicit invalid guard:

```rust
fn simulate(operations: &[&str]) -> (&'static str, usize, usize) {
    let mut state = "todo";
    let mut accepted = 0;
    let mut rejected = 0;

    for operation in operations {
        if !allowed(state, operation) {
            rejected += 1;
            continue;
        }

        state = if *operation == "start" {
            "doing"
        } else if *operation == "done" {
            "done"
        } else {
            "todo"
        };
        accepted += 1;
    }
    (state, accepted, rejected)
}
```

### Remaining design disease

`allowed("corrupt", "reopen")` returns true because every unrecognized state falls into the final branch. This is a total function but a defective domain model.

Immediate Module 2 repair:

```rust
(state == "todo" && operation == "start")
    || (state == "doing" && operation == "done")
    || (state == "done" && operation == "reopen")
```

Module 5 repair: make invalid state text unrepresentable with `enum Status`.

### Required tests

- valid complete cycle;
- invalid first operation;
- two invalid operations;
- unknown state rejects every operation;
- accepted + rejected equals input length;
- rejected operation preserves state.

## Part 3 — Focused exercises

### Access protocol

Attempt every required exercise and commit the attempt before opening `exercise-answers.md`. Mark each as:


### Exercise 1 — Boundary classifier

Implement `severity_name(u8) -> Option<&'static str>` for valid range 0–10: low 0–3, normal 4–7, high 8–10, `None` above 10. Test every boundary.

### Exercise 2 — Leap year

Implement Gregorian leap-year logic:

- divisible by 400: leap;
- divisible by 100: not leap;
- otherwise divisible by 4: leap.

Use a value-producing expression and test 1900, 2000, 2024, and 2025.

### Exercise 3 — Sum inclusive range

Implement `sum_inclusive(start: i32, end: i32) -> Option<i64>`. Return `None` when start > end. Widen before accumulation. State the termination argument.

### Exercise 4 — First divisor

Implement `first_divisor(value: u64) -> Option<u64>` returning the smallest divisor from 2 through `value - 1`, or `None` for primes and values below 4. Use `for`; avoid an unbounded search.

### Exercise 5 — Loop with value

Implement `first_multiple_at_least(divisor: u64, minimum: u64) -> Option<u64>`. Reject divisor zero. Use `loop` and `break value`, with checked addition to avoid overflow.

### Exercise 6 — Countdown trace

Implement `countdown(start: u8) -> Vec<u8>` with `while`, including zero as the final element. State the variant and ensure zero does not underflow.

### Exercise 7 — Title policy

Implement one predicate for nonempty, trimmed, <=80 characters, no tab/newline. Write separate tests per guard.

### Exercise 8 — Transition policy

With string states/operations, implement `operation_is_allowed`. Unknown states and operations return false. Construct a 3×4 table test.

### Exercise 9 — Simulator

Implement `simulate(initial_state, operations) -> (String, usize, usize)`. Rejected operations preserve state. Invalid initial state should reject all operations without changing the text.

### Exercise 10 — Refactor monolith

Given a 60-line `main` that validates, classifies, simulates, and prints, extract pure functions. Submit before/after responsibility maps and prove behavior with tests.



## Part 4 — Independent laboratory



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

### Tiered hints

Do not open a later tier until the previous tier has produced a written attempt.

- **Hint 1 — concept:** return to the governing question: How can control flow make every path, boundary, and loop invariant visible enough to test and review?
- **Hint 2 — topology:** draw owners/borrows/states/errors before changing syntax; identify the one boundary that should own the invariant.
- **Hint 3 — structure:** separate validation from mutation and pure transformation from effects. Use the standard operation that encodes the safety fact before inventing an abstraction.
- **Hint 4 — implementation-adjacent:** consult only the relevant standard-library or Reference page; do not open `solution/src`.

The executable starter and reference implementation are in [module-02-control-flow-policy](../../labs/module-02-control-flow-policy/README.md). Implement from the contract first. Compare with the reference only after your tests pass or you have written a precise blocker.

## Part 5 — Capstone transfer

### Outcomes mapped

- Treat if and loop constructs as typed expressions and prove branch agreement and loop result behavior.
- Select for, while, or loop from termination knowledge and data shape, then state the loop invariant and variant.
- Design functions with explicit preconditions, postconditions, total behavior, and guard clauses.
- Decompose stateful logic without creating flag soup, hidden fallthrough, or duplicated policy.
- Test control-flow boundaries systematically, including invalid domains, empty inputs, and off-by-one edges.


Extend the capstone without parsing real process arguments yet.

### Add pure functions

```rust
pub fn priority_from_score(score: u8) -> &'static str;
pub fn id_is_valid(id: u64) -> bool;
pub fn transition_is_allowed(state: &str, operation: &str) -> bool;
```

Use the same textual transition graph as the lab. These functions are temporary scaffolding; Module 5 replaces string states with enums.

### Main demonstration

In `main.rs`, construct fixed sample values and print a deterministic policy report:

```text
priority: high
id-valid: true
transition: allowed
```

Do not read environment arguments or files yet. The point is function contracts and branch coverage.

### Tests

- every priority threshold;
- ID zero/nonzero;
- full state-operation matrix;
- unknown strings reject;
- no `main` branch duplicates library policy.

### Design note

Answer:

1. Why does `priority_from_score` return a static string rather than allocate?
2. Which inputs remain representable but nonsensical?
3. Which function is total over its Rust input type?
4. Which policy will later move into an enum/method?
5. Why is output formatting kept separate from policy?

### Integration discipline

The capstone's final code does not retain these exact temporary functions. Keep the commit history: it should show a later typed refactor replacing rather than layering over string state. A learning capstone should preserve evidence of improved representation.



### Capstone defense

Review a policy engine, identify its invariant and termination argument, then replace one nested branch structure with total typed logic.

## Part 6 — Reconstruct and defend

Complete this checkpoint closed-book. Compiler access is allowed only after the prediction portion has been committed.

### Outcome reconstruction

For each outcome, write a claim, one example, one non-example, and one limitation.

- Treat if and loop constructs as typed expressions and prove branch agreement and loop result behavior.
- Select for, while, or loop from termination knowledge and data shape, then state the loop invariant and variant.
- Design functions with explicit preconditions, postconditions, total behavior, and guard clauses.
- Decompose stateful logic without creating flag soup, hidden fallthrough, or duplicated policy.
- Test control-flow boundaries systematically, including invalid domains, empty inputs, and off-by-one edges.

### Closed-book checkpoint

#### Closed-book questions

1. Why must a Rust condition have type `bool`?
2. Distinguish `1..4` and `1..=4`.
3. When should `for`, `while`, and `loop` each be selected?
4. What is a loop termination variant?
5. What type does plain `break;` provide to a loop expression?
6. Why should validation precede mutation?
7. Define a loop invariant for accepted/rejected command counts.
8. Why is unknown string state a modeling problem rather than only a branch problem?
9. When is a guard clause clearer than a value-producing `if`?
10. What does a failing assertion prove that a successful compile does not?

#### Reconstruction

Write without notes:

```rust
fn first_multiple(divisor: u64, minimum: u64) -> Option<u64>
```

Requirements: divisor zero returns `None`; use `loop` and `break` with value; no unchecked overflow.

Then write a table-driven test for transition policy with exactly three accepted pairs.

### Transfer defense

Review a policy engine, identify its invariant and termination argument, then replace one nested branch structure with total typed logic.

Your answer must include:
