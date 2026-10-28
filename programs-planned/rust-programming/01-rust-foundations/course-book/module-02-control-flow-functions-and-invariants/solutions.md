# Reasoned Solutions — Module 02: Control Flow, Functions, and Invariants

[Workbook](workbook.md) · [Chapter](index.md) · [Laboratory](../../labs/module-02-control-flow-policy/README.md) · [Taskboard guide](../capstone.md)

Use these notes only after preserving your prediction and repair for **Module 2: Control Flow, Functions, and Invariants**. Compare the reasoning against this question: *How can control flow make every path, boundary, and loop invariant visible enough to test and review?* Do not compare line count first. A different implementation is valid when it preserves the same public contract and can defend its ownership, failure, ordering, capacity, safety, compatibility, and evidence consequences.

## Compiler specimen reasoning

### 1. `01-break-values-agree.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** one loop expression cannot yield unrelated break types.
- **Causal explanation:** The compiler rejects the specimen because one loop expression cannot yield unrelated break types.
- **Principled repair:** Make every reachable `break` yield the loop expression’s one result type.
- **Weak repair to reject:** Do not discard a meaningful result by converting every `break` to unit.

### 2. `02-accumulator-needs-mutation.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** accumulator binding is reassigned.
- **Causal explanation:** The compiler rejects the specimen because accumulator binding is reassigned.
- **Principled repair:** Make the accumulator mutable, or replace reassignment with a fold that returns a new accumulator.
- **Weak repair to reject:** Do not move the accumulator into hidden global state.

### 3. `03-while-needs-bool.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** Rust has no integer truthiness.
- **Causal explanation:** The compiler rejects the specimen because rust has no integer truthiness.
- **Principled repair:** Write an explicit Boolean condition that states the loop invariant.
- **Weak repair to reject:** Do not compare against a magic number merely to imitate integer truthiness.

### 4. `04-return-expression-lost.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** one branch and therefore the function can yield unit.
- **Causal explanation:** The compiler rejects the specimen because one branch and therefore the function can yield unit.
- **Principled repair:** Ensure every reachable branch yields the function’s declared result, using a guard return where that clarifies control flow.
- **Weak repair to reject:** Do not weaken the return type to `()` or insert a meaningless default.

### 5. `05-loop-result-needs-context.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** rejects at formatting: unit does not implement Display.
- **Causal explanation:** The compiler rejects the specimen because rejects at formatting: unit does not implement Display.
- **Principled repair:** Give the loop a value-producing `break`, or format it with a representation appropriate for unit if unit is truly intended.
- **Weak repair to reject:** Do not switch to debug formatting just to conceal an unintended unit result.

### 6. `06-range-end-is-exclusive.rs`

- **Outcome:** `run-fail`
- **Governing rule:** compiles then fails: an exclusive range exposes a behavioral defect.
- **Causal explanation:** The specimen type-checks, then its assertion or reachable operation fails because compiles then fails: an exclusive range exposes a behavioral defect.
- **Principled repair:** Use an inclusive range when the product contract includes the upper endpoint, or correct the expected result if the range is intentionally half-open.
- **Weak repair to reject:** Do not change the assertion to whatever the current code happens to produce without resolving the range contract.

## Exercise reasoning and worked answers
### 1. Boundary classifier

```rust
pub fn severity_name(severity: u8) -> Option<&'static str> {
    if severity > 10 {
        return None;
    }
    Some(if severity >= 8 {
        "high"
    } else if severity >= 4 {
        "normal"
    } else {
        "low"
    })
}
```

Tests must include 0, 3, 4, 7, 8, 10, and 11.

### 2. Leap year

```rust
pub const fn is_leap_year(year: u32) -> bool {
    if year % 400 == 0 {
        true
    } else if year % 100 == 0 {
        false
    } else {
        year % 4 == 0
    }
}
```

Order is the policy: checking divisibility by 4 first would incorrectly classify 1900.

### 3. Sum inclusive range

```rust
pub fn sum_inclusive(start: i32, end: i32) -> Option<i64> {
    if start > end {
        return None;
    }
    let mut total = 0_i64;
    for value in start..=end {
        total += i64::from(value);
    }
    Some(total)
}
```

The range is finite and each iteration advances to the inclusive endpoint. Widening each value avoids `i32` accumulation overflow for many ordinary ranges, though a full `i32` range can still challenge practical iteration/time and `i64` sum bounds.

### 4. First divisor

```rust
pub fn first_divisor(value: u64) -> Option<u64> {
    if value < 4 {
        return None;
    }
    (2..value).find(|candidate| value % candidate == 0)
}
```

If iterators have not yet been studied, the equivalent loop is preferred at this stage:

```rust
for candidate in 2..value {
    if value % candidate == 0 {
        return Some(candidate);
    }
}
None
```

This is intentionally simple rather than optimized to square root.

### 5. Loop with value

```rust
pub fn first_multiple_at_least(divisor: u64, minimum: u64) -> Option<u64> {
    if divisor == 0 {
        return None;
    }
    let mut candidate = 0_u64;
    loop {
        if candidate >= minimum {
            break Some(candidate);
        }
        candidate = candidate.checked_add(divisor)?;
    }
}
```

The loop variant is distance to the threshold, reduced by each positive divisor step. Checked addition provides an exit if representable space is exhausted.

### 6. Countdown trace

```rust
pub fn countdown(start: u8) -> Vec<u8> {
    let mut values = Vec::new();
    let mut current = start;
    loop {
        values.push(current);
        if current == 0 {
            break;
        }
        current -= 1;
    }
    values
}
```

A naive `while current >= 0` is meaningless for unsigned values and would not terminate safely. Checking before decrement prevents underflow.

### 7. Title policy

```rust
pub fn title_is_valid(title: &str) -> bool {
    if title.trim().is_empty() {
        return false;
    }
    if title.trim() != title {
        return false;
    }
    if title.chars().count() > 80 {
        return false;
    }
    if title.chars().any(|character| matches!(character, '\t' | '\n' | '\r')) {
        return false;
    }
    true
}
```

Each guard maps directly to one contract clause and test.

### 8. Transition policy

```rust
pub fn operation_is_allowed(state: &str, operation: &str) -> bool {
    (state == "todo" && operation == "start")
        || (state == "doing" && operation == "done")
        || (state == "done" && operation == "reopen")
}
```

No catch-all state is interpreted as done.

### 9. Simulator

```rust
pub fn simulate(initial_state: &str, operations: &[&str]) -> (String, usize, usize) {
    let mut state = initial_state.to_owned();
    let mut accepted = 0;
    let mut rejected = 0;

    for operation in operations {
        if !operation_is_allowed(&state, operation) {
            rejected += 1;
            continue;
        }
        state = if *operation == "start" {
            "doing".to_owned()
        } else if *operation == "done" {
            "done".to_owned()
        } else {
            "todo".to_owned()
        };
        accepted += 1;
    }
    (state, accepted, rejected)
}
```

The returned `String` owns its result; ownership is formalized next module.

### 10. Refactor monolith

A valid responsibility map:

```text
main: choose sample/input and print
validate_title: title policy
severity_name: threshold policy
operation_is_allowed: transition policy
simulate: sequence orchestration
render_summary: text layout
```

The essential proof is that each helper has boundary tests and `main` contains no duplicate policy conditions.

### Post-key transfer

Review a policy engine, identify its invariant and termination argument, then replace one nested branch structure with total typed logic.

## Reference implementation comparison

The complete laboratory implementation is in [`module-02-control-flow-policy/solution`](../../labs/module-02-control-flow-policy/solution). Before reading it, write down:

- your public API;
- the invariant each type owns;
- the failure behavior;
- the ownership or dispatch topology;
- the complexity claim you are prepared to defend.

For **Control Flow, Functions, and Invariants**, compare the contract, invariant, failure behavior, ownership or dispatch topology, and cost before comparing syntax. A different implementation is sound when it preserves those properties and makes the module’s central relationship at least as clear.

## What a strong answer demonstrates

- Treat if and loop constructs as typed expressions and prove branch agreement and loop result behavior.
- Select for, while, or loop from termination knowledge and data shape, then state the loop invariant and variant.
- Design functions with explicit preconditions, postconditions, total behavior, and guard clauses.
- Decompose stateful logic without creating flag soup, hidden fallthrough, or duplicated policy.
- Test control-flow boundaries systematically, including invalid domains, empty inputs, and off-by-one edges.

A complete explanation of **Control Flow, Functions, and Invariants** also states the boundary of the mechanism: which guarantee it does not provide, which cost it introduces, and which simpler design should be preferred when that guarantee is unnecessary.

## Deep reasoning and transfer

### Decisive model

> How can control flow make every path, boundary, and loop invariant visible enough to test and review?

Build a **control-flow table**. Mark the owner or authority, valid and invalid states, first decisive phase or event, state after failure, and visible consequence. The model is too weak when it records only the API call and not the relationship that makes the call legal or useful.

### Outcome checks

1. **Treat if and loop constructs as typed expressions and prove branch agreement and loop result behavior.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
2. **Select for, while, or loop from termination knowledge and data shape, then state the loop invariant and variant.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
3. **Design functions with explicit preconditions, postconditions, total behavior, and guard clauses.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
4. **Decompose stateful logic without creating flag soup, hidden fallthrough, or duplicated policy.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
5. **Test control-flow boundaries systematically, including invalid domains, empty inputs, and off-by-one edges.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.

### Repair discipline

The weak repair for this module is any change that makes the current example pass by deleting the first outcome: **Treat if and loop constructs as typed expressions and prove branch agreement and loop result behavior.** A principled repair preserves that requirement, narrows the unsupported assumption, and makes the deciding fact observable in the control-flow table.

### Laboratory transfer review

For [Control-Flow Policy Engine](../../labs/module-02-control-flow-policy/README.md), compare contract, state transitions, adversarial cases, cleanup, and public behavior before syntax. Identify the earliest operation that could violate the contract and the type, check, protocol, or review procedure that prevents it. Then state when a simpler design would be preferable.

### Capstone transfer

In Taskboard, Module 2 is complete only when the new behavior fits the existing authority map. Trace the changed fact from input through validation, state transition, effect, output, and tests. Two components deciding the same fact indicate a second source of truth rather than successful integration.

### Oral defense

Answer these without notes:

1. In **Control Flow, Functions, and Invariants**, which relationship decides this question: “How can control flow make every path, boundary, and loop invariant visible enough to test and review?”
2. What is the smallest causal negative case?
3. Which repair preserves the requirement?
4. Which tempting repair deletes it?
5. What can the chosen evidence falsify, and what remains unproved?
6. How would the design change in a product unrelated to Taskboard?
