# Reasoned Solutions — Module 01: Compilation, Expressions, and Types

[Workbook](workbook.md) · [Chapter](index.md) · [Laboratory](../../labs/module-01-measurement-report/README.md) · [Taskboard guide](../capstone.md)

Use these notes only after preserving your prediction and repair for **Module 1: Compilation, Expressions, and Types**. Compare the reasoning against this question: *How does Rust turn source text into a typed program, and what type and value does every expression produce?* Do not compare line count first. A different implementation is valid when it preserves the same public contract and can defend its ownership, failure, ordering, capacity, safety, compatibility, and evidence consequences.

## Compiler specimen reasoning

### 1. `01-semicolon-changes-return.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** final semicolon makes the function body evaluate to unit.
- **Causal explanation:** The compiler rejects the specimen because final semicolon makes the function body evaluate to unit.
- **Principled repair:** Remove the final semicolon so the block yields the intended value, or explicitly return that value.
- **Weak repair to reject:** Do not change the declared return type to `()` merely to match the accidental body type.

### 2. `02-immutable-binding.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** assignment requires a mutable binding.
- **Causal explanation:** The compiler rejects the specimen because assignment requires a mutable binding.
- **Principled repair:** Declare the binding `mut` only if reassignment is part of the intended state transition; otherwise compute a new binding.
- **Weak repair to reject:** Do not introduce interior mutability or global state for a local reassignment.

### 3. `03-array-length-is-type.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** array length participates in the type.
- **Causal explanation:** The compiler rejects the specimen because array length participates in the type.
- **Principled repair:** Use the exact array length required by the function, or accept a slice when length is not part of the contract.
- **Weak repair to reject:** Do not copy elements into an arbitrary fixed-size array just to satisfy one call site.

### 4. `04-if-arms-one-type.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** both branches of a value-producing if need one type.
- **Causal explanation:** The compiler rejects the specimen because both branches of a value-producing if need one type.
- **Principled repair:** Make both branches yield one common type, usually by returning the same domain representation from each branch.
- **Weak repair to reject:** Do not stringify unrelated values merely to erase a useful type distinction.

### 5. `05-parse-needs-target-type.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** generic parsing has no target type.
- **Causal explanation:** The compiler rejects the specimen because generic parsing has no target type.
- **Principled repair:** Provide the parse target through an annotation, turbofish, or a surrounding typed binding.
- **Weak repair to reject:** Do not parse to an arbitrary type and cast afterward.

### 6. `06-shadowing-can-change-type.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** each shadowing declaration creates a new statically typed binding.
- **Causal explanation:** The specimen compiles because each shadowing declaration creates a new statically typed binding.
- **Principled repair:** No repair is required. Preserve the example and explain the exact type, ownership, or visibility rule that permits it.
- **Weak repair to reject:** Do not replace this demonstration—each shadowing declaration creates a new statically typed binding—with broader ownership, visibility, or allocation merely to make the reasoning easier.

## Exercise reasoning and worked answers
These are reference answers, not the only valid implementations.

### 1. Expression table

| Expression | Type | Value |
|---|---|---|
| `{ 3 + 4 }` | `i32` by default context | `7` |
| `{ 3 + 4; }` | `()` | `()` |
| `if true { 8 } else { 9 }` | `i32` | `8` |
| `(8)` | `i32` | `8` |
| `(8,)` | `(i32,)` | one-element tuple |
| `[0_u8; 4]` | `[u8; 4]` | four zeros |

Two punctuation variations:

```rust
let pair = (1, 2); // (i32, i32)
let grouped = (1); // i32

let result = { 5 };  // i32
let no_result = { 5; }; // ()
```

### 2. Unit conversions

```rust
pub fn celsius_to_fahrenheit(value: f64) -> f64 {
    value * 9.0 / 5.0 + 32.0
}

pub fn fahrenheit_to_celsius(value: f64) -> f64 {
    (value - 32.0) * 5.0 / 9.0
}

pub fn kilometres_to_miles(value: f64) -> f64 {
    value * 0.621_371
}

pub fn seconds_to_hours(value: u64) -> f64 {
    value as f64 / 3_600.0
}

#[cfg(test)]
mod conversion_tests {
    use super::*;

    fn close(left: f64, right: f64) -> bool {
        (left - right).abs() < 1e-10
    }

    #[test]
    fn temperature_points_convert() {
        assert!(close(celsius_to_fahrenheit(0.0), 32.0));
        assert!(close(celsius_to_fahrenheit(100.0), 212.0));
        assert!(close(celsius_to_fahrenheit(-40.0), -40.0));
        assert!(close(fahrenheit_to_celsius(32.0), 0.0));
    }
}
```

The function names carry units. A generic `convert` function would hide the contract.

### 3. Fixed three-vector

```rust
pub fn dot3(left: [f64; 3], right: [f64; 3]) -> f64 {
    left[0] * right[0] + left[1] * right[1] + left[2] * right[2]
}
```

The length is part of both parameter types, so a caller cannot pass two or four coordinates. Indexing is safe because the type proves all three positions exist.

### 4. Slice total

```rust
pub fn total(values: &[i64]) -> i64 {
    let mut result = 0;
    for value in values {
        result += value;
    }
    result
}
```

An empty sum is zero by identity. An empty minimum has no corresponding identity in the represented domain.

### 5. Honest bounds

```rust
pub fn bounds(values: &[i32]) -> Option<(i32, i32)> {
    let (&first, rest) = values.split_first()?;
    let mut minimum = first;
    let mut maximum = first;
    for &value in rest {
        minimum = minimum.min(value);
        maximum = maximum.max(value);
    }
    Some((minimum, maximum))
}
```

Initializing from the first actual value avoids fake sentinels such as `i32::MAX` and `i32::MIN`, though sentinels could be made correct for this exact type. `split_first` states the empty/nonempty distinction directly.

### 6. Mean

```rust
pub fn mean(values: &[f64]) -> Option<f64> {
    if values.is_empty() {
        return None;
    }
    let mut total = 0.0;
    for value in values {
        total += value;
    }
    Some(total / values.len() as f64)
}
```

This reference assumes ordinary finite values and does not reject `NaN` or infinity. A production scientific contract should decide those cases explicitly.

### 7. Score classification

```rust
pub fn classify_score(score: i32) -> &'static str {
    if !(0..=100).contains(&score) {
        "invalid"
    } else if score < 50 {
        "low"
    } else if score < 80 {
        "normal"
    } else {
        "high"
    }
}

#[test]
fn every_score_boundary_is_protected() {
    for (score, expected) in [
        (-1, "invalid"),
        (0, "low"),
        (49, "low"),
        (50, "normal"),
        (79, "normal"),
        (80, "high"),
        (100, "high"),
        (101, "invalid"),
    ] {
        assert_eq!(classify_score(score), expected);
    }
}
```

The branch ordering makes later upper bounds implicit after the invalid guard.

### 8. Shadowed parser

```rust
pub fn parse_percentage(input: &str) -> Result<u8, &'static str> {
    let input = input.trim();
    let input = input.parse::<u8>().map_err(|_| "not an unsigned integer")?;
    if input > 100 {
        return Err("percentage exceeds 100");
    }
    Ok(input)
}
```

The parsed `u8` already excludes negative values and values above 255. The explicit domain check handles 101–255.

### 9. Package inspection

A package is the manifest-described unit. `src/lib.rs` is the root of one library crate target. `src/main.rs` is the root of one binary crate target. Both can contain multiple modules; modules are internal namespace/privacy subdivisions, not additional packages.

### 10. Proof route

No code answer replaces running the commands. If Clippy recommends a change, write what behavior remains invariant before applying it. If rustdoc warns about a public item, document contract and edge behavior rather than copying the function name.

### Post-key transfer

Given an unfamiliar package with several targets, explain what Cargo will build, predict the types of its key expressions, and repair one warning without changing behavior.

## Reference implementation comparison

The complete laboratory implementation is in [`module-01-measurement-report/solution`](../../labs/module-01-measurement-report/solution). Before reading it, write down:

- your public API;
- the invariant each type owns;
- the failure behavior;
- the ownership or dispatch topology;
- the complexity claim you are prepared to defend.

For **Compilation, Expressions, and Types**, compare the contract, invariant, failure behavior, ownership or dispatch topology, and cost before comparing syntax. A different implementation is sound when it preserves those properties and makes the module’s central relationship at least as clear.

## What a strong answer demonstrates

- Distinguish package, crate, target, module, compiler, Cargo, profile, and artifact without collapsing them into “the project”.
- Derive the type and value of blocks, branches, tuples, arrays, function bodies, and semicolon-sensitive expressions before compiling.
- Choose numeric types and conversions from domain constraints, including overflow and floating-point limitations, rather than from habit.
- Use compiler diagnostics, tests, rustfmt, Clippy, and rustdoc as separate evidence channels and explain what each channel does not prove.
- Build and verify a small library-plus-binary package with pure calculation separated from rendering.

A complete explanation of **Compilation, Expressions, and Types** also states the boundary of the mechanism: which guarantee it does not provide, which cost it introduces, and which simpler design should be preferred when that guarantee is unnecessary.

## Deep reasoning and transfer

### Decisive model

> How does Rust turn source text into a typed program, and what type and value does every expression produce?

Build a **type trace**. Mark the owner or authority, valid and invalid states, first decisive phase or event, state after failure, and visible consequence. The model is too weak when it records only the API call and not the relationship that makes the call legal or useful.

### Outcome checks

1. **Distinguish package, crate, target, module, compiler, Cargo, profile, and artifact without collapsing them into “the project”.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
2. **Derive the type and value of blocks, branches, tuples, arrays, function bodies, and semicolon-sensitive expressions before compiling.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
3. **Choose numeric types and conversions from domain constraints, including overflow and floating-point limitations, rather than from habit.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
4. **Use compiler diagnostics, tests, rustfmt, Clippy, and rustdoc as separate evidence channels and explain what each channel does not prove.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
5. **Build and verify a small library-plus-binary package with pure calculation separated from rendering.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.

### Repair discipline

The weak repair for this module is any change that makes the current example pass by deleting the first outcome: **Distinguish package, crate, target, module, compiler, Cargo, profile, and artifact without collapsing them into “the project”.** A principled repair preserves that requirement, narrows the unsupported assumption, and makes the deciding fact observable in the type trace.

### Laboratory transfer review

For [Measurement Report](../../labs/module-01-measurement-report/README.md), compare contract, state transitions, adversarial cases, cleanup, and public behavior before syntax. Identify the earliest operation that could violate the contract and the type, check, protocol, or review procedure that prevents it. Then state when a simpler design would be preferable.

### Capstone transfer

In Taskboard, Module 1 is complete only when the new behavior fits the existing authority map. Trace the changed fact from input through validation, state transition, effect, output, and tests. Two components deciding the same fact indicate a second source of truth rather than successful integration.

### Oral defense

Answer these without notes:

1. In **Compilation, Expressions, and Types**, which relationship decides this question: “How does Rust turn source text into a typed program, and what type and value does every expression produce?”
2. What is the smallest causal negative case?
3. Which repair preserves the requirement?
4. Which tempting repair deletes it?
5. What can the chosen evidence falsify, and what remains unproved?
6. How would the design change in a product unrelated to Taskboard?
