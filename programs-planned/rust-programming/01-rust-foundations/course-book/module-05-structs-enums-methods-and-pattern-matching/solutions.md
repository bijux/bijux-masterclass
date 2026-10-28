# Reasoned solutions — Module 05: Structs, Enums, Methods, and Pattern Matching

[Return to the workbook](workbook.md) · [Return to the chapter](index.md) · [Open the Taskboard engineering guide](../capstone.md)

Use these explanations to review your reasoning about **Structs, Enums, Methods, and Pattern Matching**, not to substitute for an attempt. The decisive question is: *How can the type system make valid states representable and contradictory states difficult or impossible to construct?* When your design differs, separate three possibilities: a Rust rule was applied incorrectly, the product contract changed, or two architectures satisfy the same contract with different trade-offs.

## Compiler specimen reasoning

### 1. `01-private-newtype-field.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** public type does not expose a private tuple field constructor.
- **Causal explanation:** The compiler rejects the specimen because public type does not expose a private tuple field constructor.
- **Principled repair:** Expose a validating constructor or public method while keeping the newtype representation private.
- **Weak repair to reject:** Do not make the field public and surrender the invariant.

### 2. `02-non-exhaustive-match.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** Paused is not handled.
- **Causal explanation:** The compiler rejects the specimen because paused is not handled.
- **Principled repair:** Handle `Paused` explicitly, or use a deliberate catch-all only when all remaining states share one stable policy.
- **Weak repair to reject:** Do not add `_ => ...` merely to silence future exhaustiveness checks.

### 3. `03-moved-enum-payload.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** matching by value moves the String payload.
- **Causal explanation:** The compiler rejects the specimen because matching by value moves the String payload.
- **Principled repair:** Match the payload by reference with `ref`/`&`, or accept the move and stop using the original enum.
- **Weak repair to reject:** Do not clone every enum payload to preserve accidental reuse.

### 4. `04-option-is-not-sentinel.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** Option must be handled rather than treated as an index.
- **Causal explanation:** The compiler rejects the specimen because option must be handled rather than treated as an index.
- **Principled repair:** Pattern-match the `Option`, use a combinator, or propagate absence according to the domain policy.
- **Weak repair to reject:** Do not map `None` to a sentinel index that can collide with valid data.

### 5. `05-method-receiver-mismatch.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** shared receiver cannot mutate ordinary field.
- **Causal explanation:** The compiler rejects the specimen because shared receiver cannot mutate ordinary field.
- **Principled repair:** Use `&mut self` for ordinary mutation, or choose interior mutability only when shared mutation is part of the contract.
- **Weak repair to reject:** Do not use unsafe casts to mutate through `&self`.

### 6. `06-let-else-diverges.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** let-else else branch must diverge.
- **Causal explanation:** The compiler rejects the specimen because let-else else branch must diverge.
- **Principled repair:** Make the `else` branch return, break, continue, or panic so successful execution leaves the pattern bound.
- **Weak repair to reject:** Do not replace `let else` with an arbitrary default that erases failure.

## Exercise reasoning and worked answers
These are reference solutions, not the only valid implementations. Compare the invariants, receiver effects, and failure preservation—not formatting alone.

### Answer 1 — Representation cardinality

Three independent flags admit `2³ = 8` combinations. If exactly one flag should be true, only three are meaningful; five are contradictory. A free-form `String` has an effectively unbounded set of values while the domain recognizes three. A three-variant enum admits exactly three top-level alternatives. `Option<Status>` admits four: absence plus three statuses. `Result<Option<Status>, ParseError>` first distinguishes parse success from failure; successful values then distinguish absence from the three statuses.

The enum removes misspellings and simultaneous top-level states. It does not validate data carried inside variants, title text, ID uniqueness, or transition legality.

### Answer 2 — Non-zero identifiers

```rust
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct TaskId(u64);

impl TaskId {
    #[must_use]
    pub fn new(value: u64) -> Option<Self> {
        (value != 0).then_some(Self(value))
    }

    #[must_use]
    pub const fn get(self) -> u64 {
        self.0
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn construction_respects_non_zero_invariant() {
        assert_eq!(TaskId::new(0), None);
        assert_eq!(TaskId::new(1).map(TaskId::get), Some(1));
        assert_eq!(TaskId::new(u64::MAX).map(TaskId::get), Some(u64::MAX));
    }
}
```

`TaskId` is `Copy`, so passing it by value to `get` copies the small newtype. The caller's binding remains usable. The private field prevents outside construction of `TaskId(0)`.

### Answer 3 — Validated range

```rust
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct ScoreRange {
    minimum: u32,
    maximum: u32,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct InvalidRange {
    pub minimum: u32,
    pub maximum: u32,
}

impl ScoreRange {
    pub fn try_new(minimum: u32, maximum: u32) -> Result<Self, InvalidRange> {
        if minimum > maximum {
            return Err(InvalidRange { minimum, maximum });
        }
        Ok(Self { minimum, maximum })
    }

    pub const fn minimum(&self) -> u32 { self.minimum }
    pub const fn maximum(&self) -> u32 { self.maximum }

    pub const fn contains(&self, value: u32) -> bool {
        self.minimum <= value && value <= self.maximum
    }

    pub const fn width(&self) -> u32 {
        self.maximum - self.minimum
    }
}
```

The constructor establishes `maximum >= minimum`, so subtraction cannot underflow. The proof for `width` depends on all construction paths respecting privacy. Tests should include point ranges, exact endpoints, and reversed inputs.

### Answer 4 — Receiver audit

```rust
#[derive(Clone, Debug, Eq, PartialEq)]
struct Document {
    title: String,
    body: String,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
struct EmptyTitle;

impl Document {
    fn new(title: String, body: String) -> Result<Self, EmptyTitle> {
        if title.trim().is_empty() {
            return Err(EmptyTitle);
        }
        Ok(Self { title, body })
    }

    fn title(&self) -> &str { &self.title }

    fn body_char_count(&self) -> usize { self.body.chars().count() }

    fn rename(&mut self, title: String) -> Result<(), EmptyTitle> {
        if title.trim().is_empty() {
            return Err(EmptyTitle);
        }
        self.title = title;
        Ok(())
    }

    fn append(&mut self, text: &str) { self.body.push_str(text); }

    fn into_body(self) -> String { self.body }

    fn with_title(mut self, title: String) -> Result<Self, EmptyTitle> {
        self.rename(title)?;
        Ok(self)
    }
}
```

Construction has no receiver. Queries use `&self`. In-place changes use `&mut self`. Extraction consumes `self` so the inner `String` can be returned without cloning. Builder style consumes and returns the document.

### Answer 5 — Typed commands

```rust
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
enum Priority { Low, Normal, High }

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
enum Status { Todo, Doing, Done }

#[derive(Clone, Debug, Eq, PartialEq)]
enum Command {
    Add { priority: Priority, title: String },
    List { status: Option<Status> },
    Start(TaskId),
    Complete(TaskId),
    Help,
}
```

Contradictions removed include: `help` with an ID, `start` with a title, `add` without a title, `list` with a priority, and an unknown action spelling. Text parsing may still fail before a `Command` exists; that belongs to a parse error.

### Answer 6 — Exhaustive rendering

```rust
fn status_token(status: Status) -> &'static str {
    match status {
        Status::Todo => "todo",
        Status::Doing => "doing",
        Status::Done => "done",
    }
}

fn status_label(status: Status) -> &'static str {
    match status {
        Status::Todo => "not started",
        Status::Doing => "in progress",
        Status::Done => "completed",
    }
}
```

Storage tokens and user labels are separate contracts. Adding a variant should make both functions incomplete, plus transition and filtering matches. Those compile failures are a change-impact inventory.

### Answer 7 — Pattern ownership

```rust
fn take_add_title(command: Command) -> Option<String> {
    match command {
        Command::Add { title, .. } => Some(title),
        _ => None,
    }
}

fn add_title(command: &Command) -> Option<&str> {
    match command {
        Command::Add { title, .. } => Some(title.as_str()),
        _ => None,
    }
}
```

The first consumes `Command`; moving `title` dismantles the selected variant. The second matches a borrowed command and returns a borrow tied to it.

Partial move:

```rust
struct Record { id: u64, title: String }
let record = Record { id: 1, title: "x".to_owned() };
let Record { id, title } = record;
```

Borrowed destructure:

```rust
let record = Record { id: 1, title: "x".to_owned() };
let Record { id, title } = &record;
assert_eq!((*id, title.as_str()), (1, "x"));
```

### Answer 8 — Optional lookup

```rust
fn find(tasks: &[Task], id: TaskId) -> Option<&Task> {
    tasks.iter().find(|task| task.id() == id)
}

fn find_mut(tasks: &mut [Task], id: TaskId) -> Option<&mut Task> {
    tasks.iter_mut().find(|task| task.id() == id)
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
struct LookupError(TaskId);

fn require(tasks: &[Task], id: TaskId) -> Result<&Task, LookupError> {
    find(tasks, id).ok_or(LookupError(id))
}
```

A `let ... else` form for mutation is:

```rust
fn rename(tasks: &mut [Task], id: TaskId, title: String) -> bool {
    let Some(task) = find_mut(tasks, id) else {
        return false;
    };
    task.rename(title).is_ok()
}
```

A local fallback cannot be returned because it is destroyed when the function returns. The returned borrow must originate from an input or a suitably long-lived location.

### Answer 9 — Transition matrix

Core implementation:

```rust
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
enum Status { Todo, Doing, Done }

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
struct TransitionError { from: Status, to: Status }

impl Task {
    fn start(&mut self) -> Result<(), TransitionError> {
        self.transition(Status::Doing)
    }

    fn complete(&mut self) -> Result<(), TransitionError> {
        self.transition(Status::Done)
    }

    fn reopen(&mut self) -> Result<(), TransitionError> {
        self.transition(Status::Todo)
    }

    fn transition(&mut self, to: Status) -> Result<(), TransitionError> {
        let from = self.status;
        let legal = matches!(
            (from, to),
            (Status::Todo, Status::Doing)
                | (Status::Doing, Status::Done)
                | (Status::Done, Status::Todo)
        );
        if !legal {
            return Err(TransitionError { from, to });
        }
        self.status = to;
        Ok(())
    }
}
```

A table-driven test can construct a task in each source state through trusted test helpers, attempt each target through an internal transition, and compare both result and final state. Public-method tests should separately prove the domain verbs map to the intended targets.

### Answer 10 — Associated-data redesign

```rust
#[derive(Clone, Debug, Eq, PartialEq)]
enum JobState {
    Queued,
    Running { worker: String },
    Failed { message: String, retryable: bool },
    Succeeded { output_path: String },
}

fn summary(state: &JobState) -> String {
    match state {
        JobState::Queued => "queued".to_owned(),
        JobState::Running { worker } => format!("running on {worker}"),
        JobState::Failed { message, retryable } => {
            format!("failed: {message}; retryable={retryable}")
        }
        JobState::Succeeded { output_path } => format!("succeeded: {output_path}"),
    }
}

fn can_retry(state: &JobState) -> bool {
    matches!(state, JobState::Failed { retryable: true, .. })
}
```

The redesign removes queued-with-worker, failed-without-error, successful-without-output, and simultaneous error/output combinations. It does not prove that worker names, messages, or paths are non-empty; constructors or newtypes must validate those payloads.

### Post-key transfer

Convert a contradictory multi-flag workflow into one authoritative enum and prove that illegal combinations are no longer constructible.



## Laboratory comparison

The complete laboratory implementation is in [`module-05-state-machine/solution`](../../labs/module-05-state-machine/solution). Before reading it, write down:

- your public API;
- the invariant each type owns;
- the failure behavior;
- the ownership or dispatch topology;
- the complexity claim you are prepared to defend.

For **Structs, Enums, Methods, and Pattern Matching**, compare the contract, invariant, failure behavior, ownership or dispatch topology, and cost before comparing syntax. A different implementation is sound when it preserves those properties and makes the module’s central relationship at least as clear.

## What a strong answer demonstrates

- Choose structs, tuple structs, newtypes, enums, and associated data from domain shape rather than language familiarity.
- Place invariants at constructors and methods while keeping representation private where external mutation would bypass rules.
- Use exhaustive pattern matching to expose every state and transition.
- Represent absence with Option and distinguish it from malformed input or failed operations.
- Replace Boolean-flag and stringly typed state with an explicit state machine and tested legal transitions.

A complete explanation of **Structs, Enums, Methods, and Pattern Matching** also states the boundary of the mechanism: which guarantee it does not provide, which cost it introduces, and which simpler design should be preferred when that guarantee is unnecessary.
