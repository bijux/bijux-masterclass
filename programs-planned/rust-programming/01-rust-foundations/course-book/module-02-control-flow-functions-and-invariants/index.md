# Module 02 — Control Flow, Functions, and Invariants

**Course 1 · Day 2 · Module 2 of 100**
`░░░░░░░░░░░░░░░░░░░░░░░░░` **2/100**

[Program](../../../README.md) · [Course 1](../index.md) · [Workbook](workbook.md) · [Laboratory](../../labs/module-02-control-flow-policy/README.md) · [Taskboard guide](../capstone.md)

[← Module 1: Compilation, Expressions, and Types](../module-01-compilation-expressions-and-types/index.md) · [Module 3: Ownership, Moves, Copying, and Destruction →](../module-03-ownership-moves-copying-and-destruction/index.md)

## The question

> How can control flow make every path, boundary, and loop invariant visible enough to test and review?

## Why this comes now

Once expressions have types, a program must decide which expressions run and how results move between functions. Control flow comes before ownership because you need to see complete execution paths before you can account for the values travelling along them. The emphasis is on explicit invariants and termination, not syntax cataloguing.

### Prerequisite bridge

Module 1 established **Compilation, Expressions, and Types**. Before continuing, verify that you can build and verify a small library-plus-binary package with pure calculation separated from rendering. This module preserves that capability and adds the ability to treat if and loop constructs as typed expressions and prove branch agreement and loop result behavior. Module 3, **Ownership, Moves, Copying, and Destruction**, will rely on both when it asks: *Who owns each resource after every assignment, call, return, destructure, and scope exit?*

### Scope boundary

This module owns the reasoning for **control flow, functions, and invariants** inside Course 1. The course stays in safe Rust and mostly in the standard library. It introduces the ownership, trait, iterator, lifetime, module, and testing vocabulary required by later courses, but it does not yet pursue advanced lifetime algebra, smart-pointer architecture, unsafe code, concurrency, async runtimes, or macro construction. The purpose of the boundary is to keep the decisive relationship visible before later mechanisms are layered on top of it.

## What you will be able to do

- Treat if and loop constructs as typed expressions and prove branch agreement and loop result behavior.
- Select for, while, or loop from termination knowledge and data shape, then state the loop invariant and variant.
- Design functions with explicit preconditions, postconditions, total behavior, and guard clauses.
- Decompose stateful logic without creating flag soup, hidden fallthrough, or duplicated policy.
- Test control-flow boundaries systematically, including invalid domains, empty inputs, and off-by-one edges.

## Core model

### Why this module exists

Control flow is where informal assumptions become executable policy. Off-by-one errors, missing branches, nontermination, and flag-driven state usually arise because the programmer cannot state the invariant or the set of possible outcomes. Rust helps by making `if`, `match`, and `loop` value-producing expressions, but the type system cannot invent the product policy. This module joins typed control flow with explicit invariants.

### Total decisions

A decision function should define behavior for every value in its input type or explicitly return failure/absence. Consider:

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
```

The first guard narrows the remaining domain to `0..=100`. Each later branch can rely on that fact. The final `else` is not a guess; it covers `80..=100`. Boundary tests should be derived from the intervals: one point just below, at, and just above every threshold.

A branch that “cannot happen” should be justified by a type or prior validation. A wildcard arm that silently maps unexpected input to a default often erases evidence.

### Selecting a loop from knowledge

Use `for` when iterating a known iterable domain. Use `while` when continuation depends on a condition evaluated between iterations. Use `loop` when the exit points themselves carry the result or when the operation is intentionally unbounded.

For every nontrivial loop, state:

- **invariant:** what remains true before and after each iteration;
- **variant:** what moves monotonically toward termination;
- **exit condition:** what fact becomes true when the loop ends;
- **result:** what value or state follows from the invariant plus exit condition.

```rust
pub fn first_multiple_at_least(start: u32, divisor: u32) -> Option<u32> {
    if divisor == 0 {
        return None;
    }

    let mut candidate = start;
    loop {
        if candidate % divisor == 0 {
            break Some(candidate);
        }
        candidate = candidate.checked_add(1)?;
    }
}
```

Invariant: `candidate >= start`. Variant: remaining representable `u32` values decrease. Exit: the candidate is divisible. The checked addition makes numeric exhaustion an explicit `None` rather than accidental wraparound.

### Function contracts and guards

A function boundary should make inputs, output, and failure visible. Guard clauses are useful when they remove invalid or exceptional regions and let the main path proceed under stronger facts.

```rust
pub fn allowed_transition(current: &str, requested: &str) -> bool {
    if current == requested {
        return false;
    }

    matches!(
        (current, requested),
        ("todo", "doing") | ("doing", "done") | ("done", "todo")
    )
}
```

This is still stringly typed and will be replaced by enums in Module 5. Here it serves one purpose: the transition relation is centralized and total over the represented inputs. The later type model will remove misspelled states.

### Worked derivation: bounded retry policy

A service simulator receives a maximum number of attempts and a sequence of outcomes. We want the index of the first success, or a reason for stopping.

```rust
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Stop {
    SucceededAt(usize),
    AttemptsExhausted,
    InputsExhausted,
}

pub fn run_policy(outcomes: &[bool], max_attempts: usize) -> Stop {
    if max_attempts == 0 {
        return Stop::AttemptsExhausted;
    }

    for (index, &succeeded) in outcomes.iter().take(max_attempts).enumerate() {
        if succeeded {
            return Stop::SucceededAt(index + 1);
        }
    }

    if outcomes.len() < max_attempts {
        Stop::InputsExhausted
    } else {
        Stop::AttemptsExhausted
    }
}
```

The output type distinguishes two failure explanations. `take(max_attempts)` bounds the loop. The final decision uses the original lengths to distinguish exhausted input from exhausted policy. Tests must cover zero attempts, immediate success, success at the limit, all failures with enough inputs, and too few inputs.

### Decomposition without flag soup

A long function should not be split merely to reduce line count. Split where a function can own one invariant or conversion. Poor decomposition passes several mutable flags among helpers. Better decomposition returns a meaningful value and makes the caller's next decision explicit.

Before extracting a helper, answer:

- What facts must be true on entry?
- What fact does the return value establish?
- Can the helper be tested without reconstructing the whole program?
- Does it remove duplicated policy or merely move it?

### Try without the scaffold

Implement a bounded scan that returns the first position where a running total reaches a target. Write the invariant and choose how integer overflow is represented. Do not code until you can state what happens for an empty input, target zero, and an unreachable target.

### Misconception clinic

- **“All loops are stylistic alternatives.”** Their shapes communicate different termination knowledge.
- **“One happy-path and one error test cover the function.”** Boundaries are derived from partitions, not vibes.
- **“A default branch is robust.”** It may silently collapse an unmodeled state.
- **“More helpers mean better design.”** Helpers that exchange mutable flags can obscure rather than expose invariants.

### Conditions are Boolean

Rust does not treat integers, strings, collections, or null-like values as truthy/falsy.

```rust
let remaining = 3;
if remaining > 0 {
    println!("work remains");
}
```

The condition has type `bool`. This removes a class of implicit conversions and makes accidental empty/zero semantics impossible.

### Comparisons and short-circuiting

```rust
let valid = score >= 0 && score <= 100;
```

`&&` evaluates the right operand only when the left is true. `||` evaluates the right only when the left is false. Use this property when the right side is only valid after a guard:

```rust
let first_is_digit = !input.is_empty()
    && input.as_bytes()[0].is_ascii_digit();
```

Later, safer APIs such as `first()` often remove the need for indexing entirely.

### `if` as a value

```rust
let priority = if severity >= 8 {
    "high"
} else if severity >= 4 {
    "normal"
} else {
    "low"
};
```

This is one expression with one resulting type. It avoids a mutable variable whose value is assigned in branches:

```rust
let priority;
if severity >= 8 {
    priority = "high";
} else {
    priority = "normal";
}
```

Rust can prove the second form when every path assigns exactly once, but the expression form states the intent more directly.

### Totality

A function is **total over its declared input domain** when every input has defined behavior. Rust's type checker enforces some totality:

- a non-unit function must return on every normal path;
- every `if` used as a value needs a compatible alternative;
- later, every `match` must cover every possible variant.

Product totality still requires design. This compiles:

```rust
fn category(score: i32) -> &'static str {
    if score >= 80 { "high" } else { "normal" }
}
```

But it silently treats `-500` as normal. If the declared input type includes all `i32`, either validate the domain or use a narrower type/model.

```rust
fn category(score: i32) -> &'static str {
    if !(0..=100).contains(&score) {
        "invalid"
    } else if score >= 80 {
        "high"
    } else {
        "normal"
    }
}
```

### Condition order is policy

Branches are evaluated in order. Once an earlier condition holds, later conditions are not considered.

```rust
if value >= 0 {
    "nonnegative"
} else if value >= 10 {
    "large"
} else {
    "negative"
}
```

The second branch is unreachable because every value at least 10 already satisfies the first. Order thresholds from exceptional/most specific to general, then test boundaries.

### Avoid Boolean parameters that hide meaning

```rust
fn render(compact: bool) -> String
```

At a call site, `render(true)` does not reveal what true means. A Boolean can be acceptable for a genuinely binary mathematical property, but domain alternatives usually deserve an enum later:

```rust
render(RenderMode::Compact)
```

Course 1 first teaches the control mechanics, then improves the model.

### Guarding a normal path

```rust
fn ratio(total: f64, count: usize) -> Option<f64> {
    if count == 0 {
        return None;
    }
    Some(total / count as f64)
}
```

The invalid/special case exits early. The remainder can be read under the invariant `count > 0`.

Rust provides three principal loop forms. Choose based on what controls repetition.

### `for`: traverse a finite iterable

```rust
let mut total = 0;
for value in 1..=4 {
    total += value;
}
```

Use `for` when processing each item from an iterator or range. It avoids manual index/state management and makes finite traversal apparent.

Ranges:

- `start..end` excludes `end`;
- `start..=end` includes `end`;
- `..end`, `start..`, and `..` are open forms used in appropriate contexts.

Off-by-one behavior is product behavior. Test both ends.

### `while`: repeat while a changing Boolean remains true

```rust
let mut remaining = 3;
while remaining > 0 {
    println!("{remaining}");
    remaining -= 1;
}
```

A termination argument must identify a **variant**: a quantity that moves monotonically toward a bound. Here `remaining` decreases by one and cannot remain above zero forever.

A `while` loop whose condition depends on external I/O may not have a finite mathematical bound; document the event that terminates it and any cancellation/timeout policy. Those concerns appear in later systems courses.

### `loop`: repeat until an internal event exits

```rust
let first_multiple = loop {
    candidate += 1;
    if candidate % divisor == 0 {
        break candidate;
    }
};
```

`loop` is an expression. `break candidate` supplies its value. All value-bearing breaks in the same loop must agree in type.

Use plain `break;` when the loop's value is unit.

### Labels for nested loops

```rust
'outer: for row in rows {
    for value in row {
        if value == target {
            break 'outer;
        }
    }
}
```

Labels make the intended loop explicit. Before using a labeled break, consider extracting a function that returns when the target is found; a function boundary often communicates better than nonlocal loop control.

### `continue`

`continue` skips the remainder of the current iteration.

```rust
for input in inputs {
    if input.trim().is_empty() {
        continue;
    }
    accepted += 1;
}
```

Guard-style `continue` can flatten loop bodies. Too many continues can make state updates hard to audit. Ensure every iteration updates the termination variant before any `continue` in `while`/`loop` forms.

### Infinite loops and diverging behavior

A server/event loop may intentionally be unbounded. Course 1 command-line programs should not contain accidental unbounded loops. A `loop` that is expected to exit needs a reachable `break`, `return`, or error path and a written reason that the event can occur.

### Logic errors compile

```rust
let mut total = 0;
for value in 1..4 {
    total += value;
}
assert_eq!(total, 10);
```

The program compiles; the assertion fails because the range contains 1, 2, 3 and totals 6. Static typing cannot infer that the intended endpoint was inclusive. Tests carry that requirement.

### Indexing is rarely the first loop choice

```rust
for index in 0..values.len() {
    println!("{}", values[index]);
}
```

Prefer:

```rust
for value in values {
    println!("{value}");
}
```

The direct form avoids index bounds and communicates that position is irrelevant. Use indices when the index itself is part of the result or when coordinated access requires it.

A function boundary should make one decision understandable without simulating the entire program.

### Contract components

For each function, state:

- accepted input domain;
- ownership/access mode (formalized in Modules 3–4);
- returned value and its meaning;
- recoverable failures or absence;
- side effects;
- invariants preserved.

```rust
/// Maps severity 0–10 to a stable priority label.
/// Values above 10 are rejected.
fn priority_for(severity: u8) -> Option<&'static str> {
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

The type `u8` excludes negatives but not 11–255, so the domain guard remains necessary.

### Preconditions are not excuses

A comment saying “caller must pass 0–10” is not enforcement. Options:

- validate and return an error/absence;
- construct a validated domain type so invalid values cannot reach the function;
- assert/panic only when violation represents an internal invariant and ordinary callers cannot recover.

Course 1 begins with validation functions; later modules introduce newtypes and typed errors.

### Guard clauses

Nested form:

```rust
fn accepted(title: &str, severity: u8) -> bool {
    if !title.is_empty() {
        if severity <= 10 {
            if !title.contains('\n') {
                return true;
            }
        }
    }
    false
}
```

Guard form:

```rust
fn accepted(title: &str, severity: u8) -> bool {
    if title.is_empty() {
        return false;
    }
    if severity > 10 {
        return false;
    }
    if title.contains('\n') {
        return false;
    }
    true
}
```

The guard version lets each invalid case be named/tested and leaves the final path under all invariants. Do not mechanically convert every branch; a compact value-producing `if` is clearer for simple alternatives.

### One level of abstraction

A function should not mix low-level character scanning with high-level persistence policy unless that combination is the function's actual responsibility.

```rust
fn execute_add(raw_args: &[String], path: &Path) { /* too many layers */ }
```

A better decomposition later becomes:

```text
parse words -> Command
validate/execute Command -> changed TaskBoard + output
save changed TaskBoard -> storage result
```

Module 2 practices this decomposition without modules or error types yet.

### Return information, not hidden mutation

Prefer:

```rust
fn classify(severity: u8) -> &'static str
```

rather than:

```rust
fn classify(severity: u8, output: &mut String)
```

when the function naturally computes a value. Returning values composes with tests and keeps effects at the edge.

### Boolean helper naming

Predicates should read as claims:

- `title_is_valid`;
- `transition_is_allowed`;
- `has_remaining_work`.

Avoid `check_title` returning `bool`; “check” does not reveal whether `true` means valid, found, changed, or failed.

### Boundary tables

For threshold policies, write a table before code:

| Input | Output |
|---:|---|
| 0–3 | low |
| 4–7 | normal |
| 8–10 | high |
| 11–255 | invalid |

Translate table boundaries directly into tests. This reduces accidental gaps/overlaps.

### Narrow scopes reduce possible histories

```rust
let result = {
    let normalized = input.trim();
    normalized.len()
};
```

`normalized` exists only while needed. Later, scope also controls when values are destroyed and when borrows end. A variable declared far before use increases the number of program points where it could be changed or misunderstood.

### Local mutation should have one purpose

An accumulator is a justified mutable local:

```rust
let mut accepted = 0;
for command in commands {
    if command_is_valid(command) {
        accepted += 1;
    }
}
```

A single `state` variable mutated for unrelated meanings is not:

```rust
let mut value = 0;
// count
// later status code
// later parsed ID
```

Type consistency does not imply conceptual consistency.

### Tuple destructuring

```rust
let result = ("done", 2, 1);
let (state, accepted, rejected) = result;
```

Destructuring assigns names to positions immediately. It is especially useful for a loop that returns several local results before structs are introduced.

Nested patterns:

```rust
let ((x, y), label) = ((3, 4), "point");
```

A pattern must match the value shape. Destructuring is compile-time checked; a three-element tuple cannot be bound by a two-element pattern.

### Ignoring deliberately

```rust
let (state, accepted, _) = simulate(...);
```

`_` ignores a value without binding it. Names beginning with underscore, such as `_rejected`, create a binding but suppress ordinary unused warnings. Use them only when retaining the value/name has documentary value; otherwise `_` is clearer.

### Shadowing in control flow

Shadowing can narrow a representation after validation:

```rust
let severity = raw.parse::<u8>();
let Ok(severity) = severity else {
    return "invalid";
};
```

`let else` is covered formally with patterns in Module 5, but the idea is consistent: after the guard, `severity` has the refined type/value needed by the normal path.

### Mutation across branches

Rust requires initialization before use and can prove branch assignment:

```rust
let label;
if high {
    label = "high";
} else {
    label = "normal";
}
println!("{label}");
```

Prefer an `if` expression here. Branch assignment becomes useful when initialization involves different side effects, but pure value selection is clearer as an expression.

### Scope as a design signal

If a function needs more than a handful of mutable locals whose updates interleave, it may contain multiple responsibilities or an implicit state machine. Before adding more flags, list the states and transitions; Module 5 will model them directly.

### From script to policy pipeline

A beginner program often grows as one procedure:

```text
read input
validate title
classify priority
check transition
update state
print outcome
```

The correct decomposition is not “one function per line.” Separate decisions that have independent contracts and tests:

```rust
fn title_is_valid(title: &str) -> bool;
fn severity_name(severity: u8) -> Option<&'static str>;
fn operation_is_allowed(state: &str, operation: &str) -> bool;
fn simulate(initial: &str, operations: &[&str]) -> (String, usize, usize);
```

The first three are pure policy. The fourth orchestrates them over a sequence.

### Invariants

An invariant is a condition preserved at designated program points. In a simulation:

- state is always one of `todo`, `doing`, `done`;
- accepted + rejected equals processed operation count;
- rejected operations do not change state.

Strings do not enforce the first invariant; tests and private construction can only approximate it. Module 5 replaces strings with an enum so arbitrary state text cannot be represented.

### Loop invariant example

```rust
for operation in operations {
    // before iteration:
    // accepted + rejected == number already processed
    // state reflects exactly the accepted prefix
    if !operation_is_allowed(&state, operation) {
        rejected += 1;
        continue;
    }
    state = next_state(&state, operation);
    accepted += 1;
}
```

After either branch, exactly one count increments. A test can assert the final count equation, but the invariant explains why it holds for all lengths.

### Preserve state on failure

A critical pattern:

```rust
if !operation_is_allowed(&state, operation) {
    rejected += 1;
    continue;
}
state = next_state(&state, operation);
```

Do not mutate first and validate afterward. A failed operation should leave prior valid state intact unless the contract explicitly defines partial effects.

This principle becomes central in the capstone and persistence tests.

### Derived versus authoritative state

If `accepted` and `rejected` are authoritative counts, total processed is derived as their sum. Avoid maintaining a third mutable `processed` unless needed; multiple representations can diverge.

Likewise, later task status is authoritative as one enum. Booleans `is_started` and `is_complete` would duplicate and potentially contradict it.

### Function extraction test

Extract a function when one or more apply:

- a policy has its own boundary table;
- behavior can be tested without surrounding effects;
- a name would replace a comment explaining a decision;
- repeated code has the same semantic contract;
- a block maintains a distinct invariant.

Do not extract a one-line function merely to reduce line count when its name adds no meaning and it is used once.

### Refactoring sequence

1. protect behavior with tests;
2. identify one responsibility;
3. extract inputs and output explicitly;
4. remove hidden dependence on outer mutable state;
5. run the narrow test;
6. run full regression proof;
7. document the resulting contract.

### Review lens: precedence is part of the contract

When several guards can reject the same input, their order determines the reported failure. Suppose a command has an unknown operation, a zero identifier, and an empty title. A parser that validates the ID first reports a different defect from one that recognizes the operation first. Neither order is automatically correct, but an accidental order is unstable.

Write a precedence sentence before implementation, for example: “recognize the command name, then validate arity, then parse scalar operands, then apply domain policy.” Derive one test in which multiple defects coexist. This test protects a user-visible contract that ordinary happy-path tests cannot see.

Decomposition also constrains effects. A validation function should not print, mutate a board, or terminate the process. Returning a typed decision lets the caller choose presentation and recovery. When a helper needs a mutable output flag solely to report what happened, reconsider whether the result should be a value-producing enum or tuple instead.

### Worked audit: one loop, three hidden obligations

Consider a function that allocates the next available identifier:

```rust
fn next_free(start: u64, occupied: &[u64]) -> u64 {
    let mut candidate = start;
    while occupied.contains(&candidate) {
        candidate += 1;
    }
    candidate
}
```

The surface intent is clear, but the contract is incomplete. First, termination assumes that some representable identifier at or above `start` is absent. Second, `candidate += 1` can overflow. Third, repeated linear `contains` checks make the total work proportional to the number of candidates multiplied by the collection length. Course 1 does not require optimizing every small input, but it does require naming these obligations.

A checked version can make numeric exhaustion visible:

```rust
fn next_free(start: u64, occupied: &[u64]) -> Option<u64> {
    let mut candidate = start;

    loop {
        if !occupied.contains(&candidate) {
            return Some(candidate);
        }
        candidate = candidate.checked_add(1)?;
    }
}
```

The `?` here operates on `Option`: overflow returns `None`. The loop still needs a termination argument. Because `u64` has a finite range and the candidate strictly increases until either a free value is found or checked addition fails, the function terminates. The postcondition is also precise: `Some(id)` means `id >= start` and `occupied` does not contain `id`; `None` means the search exhausted the representable suffix.

For a task board, this generic scan may be the wrong operation entirely. If the aggregate owns a `next_id` invariant that is always greater than every issued ID and IDs are never reused, allocation becomes a constant-time checked increment. This illustrates why decomposition and invariants are linked: a stronger aggregate invariant can remove a loop, its complexity, and its termination proof from every caller.

When reviewing control flow, therefore ask four questions in order: what value does each path produce; what state changes on each path; why does repetition terminate; and could a stronger invariant eliminate the branching or repetition altogether? That final question prevents local control-flow cleverness from compensating for a weak data model.

A reviewer should be able to reconstruct that argument without executing the program or trusting sample output.

### Model checkpoint

Before the complete-program example, verify that the model can decide a design rather than merely name its mechanism.

1. **Outcome 1.** For treat if and loop constructs as typed expressions and prove branch agreement and loop result behavior, construct one positive and one causal negative example. Mark the first decisive fact in the **control-flow table** and state which evidence could falsify the claim.

2. **Outcome 2.** For select for, while, or loop from termination knowledge and data shape, then state the loop invariant and variant, construct one positive and one causal negative example. Mark the first decisive fact in the **control-flow table** and state which evidence could falsify the claim.

3. **Outcome 3.** For design functions with explicit preconditions, postconditions, total behavior, and guard clauses, construct one positive and one causal negative example. Mark the first decisive fact in the **control-flow table** and state which evidence could falsify the claim.

4. **Outcome 4.** For decompose stateful logic without creating flag soup, hidden fallthrough, or duplicated policy, construct one positive and one causal negative example. Mark the first decisive fact in the **control-flow table** and state which evidence could falsify the claim.

5. **Preservation.** Name one earlier invariant that an easier but less precise implementation could regress.

6. **Boundary.** State one claim this module can justify and one adjacent claim that requires a later course, platform contract, peer behavior, or measurement.

A strong answer records state before and after the operation, the failure path, and the public consequence. An API name by itself is not a model.

## Use the idea in a complete program

The course capstone is **Taskboard**, a persistent command-line task board. Write pure policy functions for identifiers, priorities, and state-transition sketches. Keep command parsing out until the decisions can be tested without I/O. The exact implementation task is in the [workbook](workbook.md); the full product contract is in the [capstone guide](../capstone.md).

## Practice sequence

1. Reproduce the important examples from this chapter without copying them line for line.
2. Complete the prediction and repair sections in the [workbook](workbook.md).
3. Build the independent [laboratory](../../labs/module-02-control-flow-policy/README.md).
4. Apply the capstone increment.
5. Open the [reasoned solutions](solutions.md) only after recording your own answer.

## Ready to continue

You are ready for Module 3 when you can:

- answer the module question—“How can control flow make every path, boundary, and loop invariant visible enough to test and review?”—without reading the chapter;
- demonstrate this outcome on a fresh example: Treat if and loop constructs as typed expressions and prove branch agreement and loop result behavior;
- repair the debugging case while preserving its product requirement;
- complete the laboratory transfer variant and explain the decisive design choice;
- name a simpler alternative and the condition under which you would prefer it.

## Primary Rust references

This chapter is self-contained. These official sources are included for verification and future language updates, not as required reading:

- [The Rust Book: Functions and Control Flow](https://doc.rust-lang.org/book/ch03-03-how-functions-work.html)
- [Rust Reference: Control-flow expressions](https://doc.rust-lang.org/reference/expressions/loop-expr.html)

[← Module 1](../../../01-rust-foundations/course-book/module-01-compilation-expressions-and-types/index.md) · [one-hundred-module map](../../../COURSE_MAP.md) · [Module 3 →](../../../01-rust-foundations/course-book/module-03-ownership-moves-copying-and-destruction/index.md)

## Continue

Continue to [Module 3 — Ownership, Moves, Copying, and Destruction](../module-03-ownership-moves-copying-and-destruction/index.md) after completing the workbook, independent laboratory, capstone increment, and closed-book explanation for this module.
