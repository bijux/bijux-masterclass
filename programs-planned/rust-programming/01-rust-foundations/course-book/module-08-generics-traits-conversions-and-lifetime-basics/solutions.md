# Reasoned Solutions — Module 08: Generics, Traits, Conversions, and Lifetime Basics

[Workbook](workbook.md) · [Chapter](index.md) · [Laboratory](../../labs/module-08-traits-and-lifetimes/README.md) · [Taskboard guide](../capstone.md)

Use these notes only after preserving your prediction and repair for **Module 8: Generics, Traits, Conversions, and Lifetime Basics**. Compare the reasoning against this question: *What behavior is genuinely shared, what constraints make it valid, and what borrow relationship must a signature expose?* Do not compare line count first. A different implementation is valid when it preserves the same public contract and can defend its ownership, failure, ordering, capacity, safety, compatibility, and evidence consequences.

## Compiler specimen reasoning

### 1. `01-missing-display-bound.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** formatting requires T: Display.
- **Causal explanation:** The compiler rejects the specimen because formatting requires T: Display.
- **Principled repair:** Add the weakest bound that the body actually uses, here `T: Display`, at the narrowest useful boundary.
- **Weak repair to reject:** Do not replace the generic function with a single concrete type merely to avoid stating the capability.

### 2. `02-incompatible-impl-trait-branches.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** return-position impl Trait is one hidden concrete type.
- **Causal explanation:** The compiler rejects the specimen because return-position impl Trait is one hidden concrete type.
- **Principled repair:** Return one concrete iterator type, use an enum wrapper, or deliberately erase behind a trait object when runtime variation is required.
- **Weak repair to reject:** Do not allocate both branches into a vector only to make their types match unless eager collection is required.

### 3. `03-orphan-rule.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** foreign trait for foreign type violates coherence.
- **Causal explanation:** The compiler rejects the specimen because foreign trait for foreign type violates coherence.
- **Principled repair:** Introduce a local newtype or a local trait so at least one side of the implementation is owned by this crate.
- **Weak repair to reject:** Do not fork or copy the foreign type just to claim implementation ownership.

### 4. `04-consumed-writer.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** first call moves the writer.
- **Causal explanation:** The compiler rejects the specimen because first call moves the writer.
- **Principled repair:** Borrow the writer mutably or reborrow it for each call rather than moving the writer into the first operation.
- **Weak repair to reject:** Do not reopen or duplicate the output destination for every write.

### 5. `05-ambiguous-output-lifetime.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** output source among two borrowed inputs is not stated.
- **Causal explanation:** The compiler rejects the specimen because output source among two borrowed inputs is not stated.
- **Principled repair:** Name lifetimes so the return is tied to the selected input, or return an enum/owned result when either input may supply it.
- **Weak repair to reject:** Do not tie both inputs to one unnecessarily long lifetime merely because that compiles.

### 6. `06-lifetime-cannot-save-local.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** annotation cannot extend local ownership.
- **Causal explanation:** The compiler rejects the specimen because annotation cannot extend local ownership.
- **Principled repair:** Return owned data or a reference into caller-owned storage; lifetime syntax cannot extend a local owner.
- **Weak repair to reject:** Do not leak local memory or use unsafe lifetime extension.

## Exercise reasoning and worked answers
### 1. Borrowed extrema

```rust
fn min_max<T: Ord>(values: &[T]) -> Option<(&T, &T)> {
    let first = values.first()?;
    let mut minimum = first;
    let mut maximum = first;

    for value in &values[1..] {
        if value < minimum {
            minimum = value;
        }
        if value > maximum {
            maximum = value;
        }
    }

    Some((minimum, maximum))
}
```

The output references are tied by elision to the one input slice. One element returns the same reference twice. `Ord` is sufficient; cloning is unnecessary.

### 2. Generic partition

```rust
fn partition<T, F>(values: Vec<T>, mut predicate: F) -> (Vec<T>, Vec<T>)
where
    F: FnMut(&T) -> bool,
{
    let mut yes = Vec::new();
    let mut no = Vec::new();

    for value in values {
        if predicate(&value) {
            yes.push(value);
        } else {
            no.push(value);
        }
    }

    (yes, no)
}
```

Each `T` moves exactly once from the input allocation into one output vector. The closure borrows a value only for the decision. Two output allocations may grow; capacities can be tuned only with evidence.

### 3. Method-specific bounds

```rust
struct Bag<T> {
    values: Vec<T>,
}

impl<T> Bag<T> {
    fn len(&self) -> usize { self.values.len() }
}

impl<T: PartialEq> Bag<T> {
    fn contains(&self, value: &T) -> bool {
        self.values.contains(value)
    }
}

impl<T: Ord> Bag<T> {
    fn sorted_refs(&self) -> Vec<&T> {
        let mut refs: Vec<_> = self.values.iter().collect();
        refs.sort();
        refs
    }
}
```

Sorting references removes the `Clone` bound and leaves the bag unchanged. The returned vector borrows the bag.

### 4. Display and parsing

Use an exhaustive `match` in both directions. `Display` emits one canonical human token; `FromStr` owns invalid input in its error if the error may outlive the argument. Test every variant with:

```rust
for value in [Priority::Low, Priority::Normal, Priority::High] {
    assert_eq!(value.to_string().parse::<Priority>(), Ok(value));
}
```

Also test case sensitivity explicitly; do not normalize unless the command contract promises it.

### 5. Conversions

`DomainError -> AppError` is infallible wrapping. `u64 -> TaskId` can reject zero, so `TryFrom` is required. `AppError -> DomainError` is absent because the application enum also contains command and storage failures. `TaskId -> u64` can be exposed through a method or `From<TaskId> for u64` if representation conversion is intentionally public.

### 6. Argument relations

```rust
use std::fmt::Display;

fn mixed(left: impl Display, right: impl Display) -> String {
    format!("{left}:{right}")
}

fn same<T: Display>(left: T, right: T) -> String {
    format!("{left}:{right}")
}
```

`mixed(1_u64, "task")` is valid; `same(1_u64, "task")` is not because one `T` cannot be both types.

### 7. Generic writer

```rust
use std::io::{self, Write};

fn write_rows<W: Write>(
    writer: &mut W,
    rows: &[(&str, u64)],
) -> io::Result<()> {
    for (label, value) in rows {
        writeln!(writer, "{label}\t{value}")?;
    }
    Ok(())
}
```

The caller retains the writer; every write result is propagated.

### 8. Generic reader

```rust
use std::io::{self, BufRead};

fn numbered_lines<R: BufRead>(reader: R) -> io::Result<Vec<(usize, String)>> {
    reader
        .lines()
        .enumerate()
        .map(|(index, line)| line.map(|line| (index + 1, line)))
        .collect()
}
```

Do not discard blank lines here. Whether they are legal belongs to the consuming grammar.

### 9. Lifetime relationships

```rust
fn longer_title<'a>(left: &'a Task, right: &'a Task) -> &'a str {
    if left.title().len() >= right.title().len() {
        left.title()
    } else {
        right.title()
    }
}

fn first_title<'a, 'b>(left: &'a Task, _right: &'b Task) -> &'a str {
    left.title()
}
```

The second signature does not shorten the output merely because the second task is short-lived.

### 10. Borrowed projection

```rust
struct TaskView<'a> {
    id: TaskId,
    title: &'a str,
}

fn task_views(tasks: &[Task]) -> Vec<TaskView<'_>> {
    tasks
        .iter()
        .map(|task| TaskView {
            id: task.id(),
            title: task.title(),
        })
        .collect()
}
```

Any mutation requiring exclusive access to the task vector is blocked while the views are later used. Dropping or last-using the views ends the borrow.

### 11. Ownership redesign

Store copied scalar IDs and owned bounded strings needed by the report. Do not duplicate full task objects. If five displayed fields are all strings, a report of `n` rows performs at most `5n` string allocations unless fields can be formatted into one row string or represented as enums/scalars. Choose from lifecycle and measured cost.

### 12. Audit outcome

In this course, justified generic abstractions normally include collection algorithms over `T`, closure parameters for policy, and I/O over `BufRead`/`Write`. Standard traits should own parsing and formatting. A capstone-specific repository trait is normally removed because there is one production storage mechanism and generic codecs already enable tests.

### Final review

A reference answer is not superior merely because it is more generic. Prefer the version with the smallest accurate contract, clear ownership, and callers that benefit from substitution.

### Post-key transfer

Refactor a concrete file codec into a BufRead/Write boundary and derive the lifetime of a borrowed selector without overconstraining unrelated inputs.

## Reference implementation comparison

The complete laboratory implementation is in [`module-08-traits-and-lifetimes/solution`](../../labs/module-08-traits-and-lifetimes/solution). Before reading it, write down:

- your public API;
- the invariant each type owns;
- the failure behavior;
- the ownership or dispatch topology;
- the complexity claim you are prepared to defend.

For **Generics, Traits, Conversions, and Lifetime Basics**, compare the contract, invariant, failure behavior, ownership or dispatch topology, and cost before comparing syntax. A different implementation is sound when it preserves those properties and makes the module’s central relationship at least as clear.

## What a strong answer demonstrates

- Write generic functions and types whose bounds correspond to operations actually performed.
- Define and implement small traits as behavioral contracts without abstraction theater.
- Use Display, Error, From, FromStr, Read, BufRead, and Write at natural boundaries.
- Derive ordinary lifetime annotations from input-output provenance and distinguish annotation from lifetime extension.
- Choose ownership instead of adding lifetime parameters when values must be retained independently.

A complete explanation of **Generics, Traits, Conversions, and Lifetime Basics** also states the boundary of the mechanism: which guarantee it does not provide, which cost it introduces, and which simpler design should be preferred when that guarantee is unnecessary.

## Deep reasoning and transfer

### Decisive model

> What behavior is genuinely shared, what constraints make it valid, and what borrow relationship must a signature expose?

Build a **trait and lifetime contract**. Mark the owner or authority, valid and invalid states, first decisive phase or event, state after failure, and visible consequence. The model is too weak when it records only the API call and not the relationship that makes the call legal or useful.

### Outcome checks

1. **Write generic functions and types whose bounds correspond to operations actually performed.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
2. **Define and implement small traits as behavioral contracts without abstraction theater.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
3. **Use Display, Error, From, FromStr, Read, BufRead, and Write at natural boundaries.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
4. **Derive ordinary lifetime annotations from input-output provenance and distinguish annotation from lifetime extension.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
5. **Choose ownership instead of adding lifetime parameters when values must be retained independently.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.

### Repair discipline

The weak repair for this module is any change that makes the current example pass by deleting the first outcome: **Write generic functions and types whose bounds correspond to operations actually performed.** A principled repair preserves that requirement, narrows the unsupported assumption, and makes the deciding fact observable in the trait and lifetime contract.

### Laboratory transfer review

For [Trait and Lifetime Boundary](../../labs/module-08-traits-and-lifetimes/README.md), compare contract, state transitions, adversarial cases, cleanup, and public behavior before syntax. Identify the earliest operation that could violate the contract and the type, check, protocol, or review procedure that prevents it. Then state when a simpler design would be preferable.

### Capstone transfer

In Taskboard, Module 8 is complete only when the new behavior fits the existing authority map. Trace the changed fact from input through validation, state transition, effect, output, and tests. Two components deciding the same fact indicate a second source of truth rather than successful integration.

### Oral defense

Answer these without notes:

1. In **Generics, Traits, Conversions, and Lifetime Basics**, which relationship decides this question: “What behavior is genuinely shared, what constraints make it valid, and what borrow relationship must a signature expose?”
2. What is the smallest causal negative case?
3. Which repair preserves the requirement?
4. Which tempting repair deletes it?
5. What can the chosen evidence falsify, and what remains unproved?
6. How would the design change in a product unrelated to Taskboard?
