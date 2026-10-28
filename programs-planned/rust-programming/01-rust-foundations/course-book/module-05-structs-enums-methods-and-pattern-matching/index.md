# Module 05 — Structs, Enums, Methods, and Pattern Matching

**Course 1 · Day 5 · Module 5 of 100**
`█░░░░░░░░░░░░░░░░░░░░░░░░` **5/100**

[Program](../../../README.md) · [Course 1](../index.md) · [Workbook](workbook.md) · [Laboratory](../../labs/module-05-state-machine/README.md) · [Taskboard guide](../capstone.md)

[← Module 4: Borrowing, References, Slices, and Strings](../module-04-borrowing-references-slices-and-strings/index.md) · [Module 6: Collections, Iterators, and Closures →](../module-06-collections-iterators-and-closures/index.md)

## The question

> How can the type system make valid states representable and contradictory states difficult or impossible to construct?

## Why this comes now

Ownership tells you who controls a value; domain modeling tells you what values may exist. Structs and enums now replace tuples, strings, and flag combinations with explicit states. Pattern matching becomes the bridge between representation and behavior, making invalid cases visible at compile time rather than hiding them in convention.

### Prerequisite bridge

Module 4 established **Borrowing, References, Slices, and Strings**. Before continuing, verify that you can return borrowed views only when provenance remains valid and explain the source of every returned reference. This module preserves that capability and adds the ability to choose structs, tuple structs, newtypes, enums, and associated data from domain shape rather than language familiarity. Module 6, **Collections, Iterators, and Closures**, will rely on both when it asks: *Does an algorithm borrow, mutate, or consume a collection, and what complexity and invalidation consequences follow?*

### Scope boundary

This module owns the reasoning for **structs, enums, methods, and pattern matching** inside Course 1. The course stays in safe Rust and mostly in the standard library. It introduces the ownership, trait, iterator, lifetime, module, and testing vocabulary required by later courses, but it does not yet pursue advanced lifetime algebra, smart-pointer architecture, unsafe code, concurrency, async runtimes, or macro construction. The purpose of the boundary is to keep the decisive relationship visible before later mechanisms are layered on top of it.

## What you will be able to do

- Choose structs, tuple structs, newtypes, enums, and associated data from domain shape rather than language familiarity.
- Place invariants at constructors and methods while keeping representation private where external mutation would bypass rules.
- Use exhaustive pattern matching to expose every state and transition.
- Represent absence with Option and distinguish it from malformed input or failed operations.
- Replace Boolean-flag and stringly typed state with an explicit state machine and tested legal transitions.

## Core model

### Why this module exists

Many bugs are not algorithmic; they are representational. A record with `is_started`, `is_done`, `is_deleted`, and `status_text` permits contradictory combinations. A string status permits misspellings. A public numeric ID can be confused with a count. Rust's structs, enums, newtypes, methods, and exhaustive matching allow the domain model to remove entire classes of states.

### Choose a type from the state space

Use a struct when several named fields exist together. Use a tuple struct/newtype when a value needs a distinct domain identity or invariant. Use an enum when a value is exactly one of several alternatives, especially when each alternative carries different data.

```rust
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct TaskId(u64);

impl TaskId {
    pub fn new(value: u64) -> Option<Self> {
        (value != 0).then_some(Self(value))
    }

    pub const fn get(self) -> u64 {
        self.0
    }
}
```

A private field prevents arbitrary construction outside the module. The constructor centralizes the nonzero invariant. The type makes accidental interchange with other `u64` values harder.

### Enums carry exactly the data a state needs

```rust
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum JobState {
    Queued,
    Running { worker: String },
    Completed { artifact: String },
    Failed { message: String },
}
```

There is no state in which a queued job has a completion artifact or a completed job lacks one. That is stronger than documenting a convention among optional fields.

The goal is not to eliminate every invalid input at compile time. External text is still fallible. The goal is that after conversion, internal operations can rely on stronger facts.

### Methods and receiver choice

Receiver choice communicates ownership:

- `&self`: inspect without consuming;
- `&mut self`: mutate while retaining identity;
- `self`: consume or transition ownership;
- associated function: construct or operate without an existing instance.

A method should protect the type's invariant rather than merely move a free function into an `impl` block.

```rust
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Status {
    Todo,
    Doing,
    Done,
}

impl Status {
    pub fn start(self) -> Result<Self, TransitionError> {
        match self {
            Self::Todo => Ok(Self::Doing),
            Self::Doing | Self::Done => Err(TransitionError::CannotStart(self)),
        }
    }
}
```

Taking `self` works well for a small `Copy` state value. A task method may instead borrow `&mut self` and replace its field only after the transition succeeds.

### Exhaustive matching is change detection

An exhaustive `match` forces the program to address every current variant. A wildcard arm is appropriate only when all remaining cases genuinely share one stable policy. It can otherwise hide a new variant during evolution.

```rust
pub fn label(status: Status) -> &'static str {
    match status {
        Status::Todo => "todo",
        Status::Doing => "doing",
        Status::Done => "done",
    }
}
```

Adding `Blocked` now creates compiler errors at policy sites that must be reviewed. That is useful change-impact evidence.

### Option is absence, not arbitrary failure

Use `Option<T>` when a valid value may simply be absent: a lookup may find no task, a slice may be empty, a filter may have no first match. Use `Result<T, E>` when the operation fails for a reason the caller may need to distinguish: invalid transition, malformed command, unreadable file.

`if let` and `let else` are focused pattern tools. Use `match` when alternatives carry meaningful policy; use focused forms when only one pattern continues and the rest share a simple path.

### Worked derivation: task transition

```rust
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Task {
    id: TaskId,
    title: String,
    status: Status,
}

impl Task {
    pub fn start(&mut self) -> Result<(), TransitionError> {
        let next = self.status.start()?;
        self.status = next;
        Ok(())
    }
}
```

The method computes a valid next state before mutation. Failure leaves the task unchanged. The public fields remain private, so callers cannot bypass transition rules.

### Try without the scaffold

Model a payment as `Created`, `Authorized { authorization_id }`, `Captured { receipt }`, or `Cancelled { reason }`. List every legal transition before coding. Decide whether transition methods consume the enum or mutate an aggregate. Write one compile-time impossible state from the old optional-field design.

### Misconception clinic

- **“Enums are named integers.”** Rust enums can carry variant-specific data and define a sum type.
- **“Private fields are overengineering.”** They are the boundary that makes constructor/method invariants meaningful.
- **“A wildcard arm is future-proof.”** It can suppress required review when the state space changes.
- **“Option is a lightweight Result.”** Absence and failure convey different contracts.

### A struct is a product of fields

A named-field struct says that one value contains all of its fields at the same time:

```rust
struct Task {
    id: u64,
    title: String,
    complete: bool,
}
```

Mathematically, the set of possible `Task` values is approximately the product of the possible values of each field. This matters because every public field expands what outside code can construct and mutate.

A struct is therefore more than grouped storage. It is a candidate **invariant boundary**: a place where several facts must remain consistent together.

### Group fields that change under one rule

A useful struct groups data whose validity is governed by a coherent set of operations.

```rust
#[derive(Debug, Eq, PartialEq)]
struct TemperatureRange {
    minimum: i32,
    maximum: i32,
}
```

The pair has an invariant: `minimum <= maximum`. Public fields allow callers to violate it after construction. Private fields plus a validating constructor make the boundary meaningful:

```rust
#[derive(Debug, Eq, PartialEq)]
struct TemperatureRange {
    minimum: i32,
    maximum: i32,
}

impl TemperatureRange {
    fn new(minimum: i32, maximum: i32) -> Option<Self> {
        (minimum <= maximum).then_some(Self { minimum, maximum })
    }

    fn contains(&self, value: i32) -> bool {
        self.minimum <= value && value <= self.maximum
    }
}
```

Within the defining module, methods can access private fields. Outside that module, callers must use the admitted operations.

Privacy does not prove an invariant by itself. It gives the implementation one controlled place to preserve the invariant.

### Construction is part of the public contract

Rust has no privileged constructor syntax. `new` is an associated function by convention. Different construction policies can be explicit:

```rust
#[derive(Debug, Eq, PartialEq)]
struct RangeError {
    minimum: i32,
    maximum: i32,
}

impl TemperatureRange {
    fn point(value: i32) -> Self {
        Self {
            minimum: value,
            maximum: value,
        }
    }

    fn try_new(minimum: i32, maximum: i32) -> Result<Self, RangeError> {
        if minimum <= maximum {
            Ok(Self { minimum, maximum })
        } else {
            Err(RangeError { minimum, maximum })
        }
    }
}
```

The implementation exposes the complete decision: every valid pair constructs a range, and every reversed pair returns the rejected values as structured evidence.

Constructor names should communicate whether failure is possible. `new` often means infallible. `try_new`, `parse`, or a domain-specific verb signals validation.

### Newtypes separate meaning from representation

Two values may both use `u64` but should not be interchangeable:

```rust
struct TaskId(u64);
struct UserId(u64);
```

Without newtypes, this compiles:

```rust
fn assign(task_id: u64, user_id: u64) { /* ... */ }

assign(user_id, task_id);
```

The machine representation cannot express the semantic mistake. Newtypes make the distinction part of type checking:

```rust
fn assign(task_id: TaskId, user_id: UserId) { /* ... */ }
```

Now accidental reversal is rejected.

A newtype can also narrow construction:

```rust
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
struct TaskId(u64);

impl TaskId {
    fn new(value: u64) -> Option<Self> {
        (value != 0).then_some(Self(value))
    }

    fn get(self) -> u64 {
        self.0
    }
}
```

Code outside the module cannot construct `TaskId(0)` when the tuple field is private.

### Field visibility is not accessor bureaucracy

A getter is justified when it reveals stable information without granting mutation:

```rust
impl Task {
    fn title(&self) -> &str {
        &self.title
    }
}
```

Returning `&str` lets callers inspect the title without cloning or replacing it. A `set_title(String)` method may still be too broad if titles require validation. Prefer an operation that enforces the rule:

```rust
fn rename(&mut self, title: String) -> Result<(), TitleError> {
    validate_title(&title)?;
    self.title = title;
    Ok(())
}
```

The method name and return type expose the possibility of rejection. The assignment occurs only after validation, so failure preserves the old title.

### Structural update can bypass intended validation

Struct update syntax is useful inside trusted construction code:

```rust
let revised = Configuration {
    timeout_seconds: 60,
    ..original
};
```

But if fields are public, any caller can create combinations the module intended to prohibit. Privacy is the stronger boundary; syntax convenience is secondary.

### Derives are contracts, not decoration

```rust
#[derive(Clone, Debug, Eq, PartialEq)]
struct Task { /* fields */ }
```

Each derive grants behavior:

- `Debug` supports programmer-facing diagnostics;
- `PartialEq` and `Eq` define equality from all fields;
- `Clone` authorizes explicit duplication of the entire value;
- `Copy` would authorize implicit bitwise duplication and is inappropriate for `String`-owning structs.

Derive only behavior that has a coherent domain meaning. Equality over every field may be wrong if identity alone should determine equality. The compiler can generate an implementation; it cannot decide the semantics.

### Receiver choice states an ownership effect

An associated function has no receiver:

```rust
impl Task {
    fn new(id: TaskId, title: String) -> Self {
        Self { id, title }
    }
}
```

A method receives one of three ordinary forms:

```rust
fn id(&self) -> TaskId
fn rename(&mut self, title: String) -> Result<(), TitleError>
fn into_title(self) -> String
```

These are not stylistic alternatives.

| Receiver | Effect | Caller consequence |
|---|---|---|
| `&self` | shared inspection | value remains usable |
| `&mut self` | exclusive in-place operation | value remains usable after borrow ends |
| `self` | consumes the value | original binding cannot be used afterward unless returned |

Choose the weakest receiver that expresses the real effect. Taking `&mut self` for a read-only operation unnecessarily excludes simultaneous readers. Taking `self` for inspection forces ownership transfer. Taking `&self` for an operation that must replace internal state cannot work without other mechanisms outside this course.

### Method-call syntax performs limited auto-borrowing

Given:

```rust
let task = Task::new(id, title);
let identifier = task.id();
```

Rust can automatically borrow `task` for an `&self` method. This convenience does not erase the receiver contract. The method declaration remains the reliable way to reason about whether the call reads, mutates, or consumes.

The fully qualified shape is approximately:

```rust
let identifier = Task::id(&task);
```

### Construction should establish the initial invariant

A task's initial status should not be supplied by every caller if the domain requires all new tasks to begin in `Todo`:

```rust
impl Task {
    fn new(id: TaskId, title: String, priority: Priority) -> Self {
        Self {
            id,
            title,
            priority,
            status: Status::Todo,
        }
    }
}
```

Accepting `status: Status` would broaden the constructor contract and permit callers to create already-completed tasks. That may be valid for deserialization, but it should be a separate, more controlled path such as `from_stored_parts` inside the storage boundary.

Do not weaken the ordinary constructor merely because another layer needs restoration.

### Mutation methods should be transactional at their scale

Consider renaming:

```rust
fn rename(&mut self, candidate: String) -> Result<(), RenameError> {
    validate_title(&candidate)?;
    self.title = candidate;
    Ok(())
}
```

The method validates before replacing the old title. Therefore:

- success establishes the new invariant;
- failure reports why;
- failure preserves the previous value.

A weaker implementation might first assign and then discover invalid input, requiring rollback. Prefer designs in which invalid input never reaches the mutation point.

### Consuming methods expose ownership recovery

A consuming method can dismantle a value and return owned components:

```rust
impl Task {
    fn into_title(self) -> String {
        self.title
    }
}
```

This is useful when the wrapper is no longer needed and the caller needs ownership of an inner resource. It avoids cloning. The consumed `Task` cannot be used afterward.

A method can consume, transform, and return a new state:

```rust
fn with_priority(mut self, priority: Priority) -> Self {
    self.priority = priority;
    self
}
```

Builder-style consuming methods are appropriate when constructing a value before it becomes shared. They are not automatically superior to mutable methods; the ownership flow should match how the value is used.

### Separate queries from commands

A query observes:

```rust
fn is_done(&self) -> bool
```

A command attempts change:

```rust
fn complete(&mut self) -> Result<(), TransitionError>
```

Keeping this distinction visible improves review. A method named `status` should not mutate hidden counters. A method named `complete` should define its failure behavior.

Rust does not enforce command-query separation, but receiver choice and return types make violations easier to notice.

### Associated constants can centralize domain limits

```rust
impl Task {
    const MAX_TITLE_CHARS: usize = 120;
}
```

A named limit belongs near the invariant it constrains. Tests should exercise the boundary at `MAX_TITLE_CHARS - 1`, exactly `MAX_TITLE_CHARS`, and `MAX_TITLE_CHARS + 1` rather than only obvious cases.

### Do not manufacture methods for every field

A method should represent useful behavior or controlled observation. Mechanical setters recreate public-field semantics behind function calls:

```rust
fn set_status(&mut self, status: Status) {
    self.status = status;
}
```

This setter bypasses legal transitions. Prefer domain verbs:

```rust
fn start(&mut self) -> Result<(), TransitionError>
fn complete(&mut self) -> Result<(), TransitionError>
fn reopen(&mut self) -> Result<(), TransitionError>
```

The interface then describes the state graph rather than exposing storage.

### An enum represents one alternative at a time

```rust
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
enum Status {
    Todo,
    Doing,
    Done,
}
```

A `Status` value is exactly one variant. Unlike independent Boolean flags, it cannot be simultaneously `Todo` and `Done`.

Three Boolean fields produce eight bit combinations:

```text
is_todo × is_doing × is_done = 2 × 2 × 2 = 8
```

Only three combinations may be meaningful. The remaining five are representable contradictions. A three-variant enum has exactly the intended top-level alternatives.

This counting technique is useful during design: compare the cardinality of the representation with the cardinality of the domain.

### Variants can carry different data

Enums are not restricted to labels:

```rust
enum Command {
    Add {
        priority: Priority,
        title: String,
    },
    List {
        status: Option<Status>,
    },
    Start(TaskId),
    Done(TaskId),
    Help,
}
```

Each command carries only the fields relevant to that operation. A struct with optional fields would admit nonsense such as a `Help` command with a task ID and title.

Compare:

```rust
struct WeakCommand {
    name: String,
    id: Option<TaskId>,
    title: Option<String>,
    priority: Option<Priority>,
}
```

The struct's field product contains many combinations that require runtime policing. The enum is a sum of meaningful variant payloads.

### Sum and product reasoning

For simplified finite types:

- a struct's possibilities multiply;
- an enum's variant possibilities add.

Suppose `Priority` has three variants and `Status` has three variants. A task with both has `3 × 3 = 9` combinations before considering its ID and title. A command enum with `Help`, `Start(TaskId)`, and `Add(Priority, Title)` has the union of those variant shapes; no value can carry two command identities at once.

This reasoning exposes hidden invalid states before code is written.

### Associated data makes state-specific facts local

Consider a job lifecycle:

```rust
enum JobState {
    Queued,
    Running { worker: String },
    Failed { message: String, retryable: bool },
    Succeeded { output_path: String },
}
```

A `worker` exists only while running. An output path exists only after success. A flat struct with all fields wrapped in `Option` would allow a queued job with a success output or a failed job without a message.

The enum makes each payload conditional on the variant.

### Nested enums express layered uncertainty

`Option<Result<T, E>>` and `Result<Option<T>, E>` are not interchangeable.

- `Option<Result<T, E>>`: an operation may not have been attempted; if attempted, it may succeed or fail.
- `Result<Option<T>, E>`: the operation is attempted and may fail; success may contain or not contain a value.

Read from the outside inward. The outer enum determines the first decision the caller must handle.

### Variant names should express domain language

Names such as `State1`, `State2`, or `Other` conceal meaning. Variants should match the vocabulary used in requirements and tests. A new reviewer should be able to compare the enum directly with the state diagram.

Avoid a catch-all `Unknown` unless unknown input is a legitimate stored domain state. Often unknown text belongs in a parse error, not in the model.

### Enum evolution and exhaustive consumers

Adding a variant can break every exhaustive `match`. That friction is valuable. It identifies all locations whose behavior may need revision.

A wildcard arm suppresses the evidence:

```rust
match status {
    Status::Done => "complete",
    _ => "open",
}
```

This may be correct when all current and future non-done states truly share one policy. It is weak when each state requires an intentional rendering or transition rule.

### `match` is a total decision expression

```rust
fn status_label(status: Status) -> &'static str {
    match status {
        Status::Todo => "todo",
        Status::Doing => "doing",
        Status::Done => "done",
    }
}
```

Every possible `Status` is handled, and every arm returns `&'static str`. Because `match` is an expression, the result becomes the function's result.

Exhaustiveness is a maintenance property: adding a new variant identifies every total decision that must be reconsidered.

### Patterns bind structure

```rust
match command {
    Command::Add { priority, title } => add(priority, title),
    Command::Start(id) => start(id),
    Command::List { status: None } => list_all(),
    Command::List { status: Some(status) } => list_status(status),
    Command::Help => print_help(),
}
```

Patterns simultaneously test the variant and bind its payload. The bindings follow ordinary ownership rules. Matching an owned `Command` can move its owned `String` out of `Add`. Matching `&Command` binds borrowed views unless the pattern requests copied fields.

### Match the ownership form you need

Owned match:

```rust
fn execute(command: Command) {
    match command {
        Command::Search(query) => consume_query(query),
        // other arms
        # _ => {}
    }
}
```

Borrowed match:

```rust
fn describe(command: &Command) -> &'static str {
    match command {
        Command::Search(_) => "search",
        // other arms
        # _ => "other",
    }
}
```

Do not add `clone()` merely because matching moved a field. Decide whether the function should consume the command or inspect it.

### Destructuring structs and tuples

```rust
let TaskSummary { id, status, .. } = summary;
```

`..` ignores remaining fields. A rename can distinguish local names:

```rust
let TaskSummary {
    id: task_id,
    status: current_status,
    ..
} = summary;
```

Destructuring an owned value can partially move non-`Copy` fields. After:

```rust
let Task { title, priority, .. } = task;
```

`title` moves if it is a `String`; copied fields remain copied. The original aggregate may no longer be usable as a whole.

Destructure a reference when observation is sufficient.

### Guards refine but do not add coverage

```rust
match priority {
    value if value == Priority::High => "urgent",
    _ => "ordinary",
}
```

A guard is evaluated after a structural pattern matches. The compiler does not generally use arbitrary guard logic to prove exhaustiveness; an unguarded fallback is still required.

Prefer direct variant patterns when available. Guards are useful when the condition is not part of the enum shape.

### Alternatives with `|`

```rust
match status {
    Status::Todo | Status::Doing => "open",
    Status::Done => "closed",
}
```

Alternative patterns must bind compatible names and types. Use them when variants intentionally share policy, not merely to shorten code.

### `matches!` for a Boolean question

```rust
fn is_open(status: Status) -> bool {
    matches!(status, Status::Todo | Status::Doing)
}
```

`matches!` is appropriate when the required output is only `bool`. Use `match` when different variants produce distinct values or effects.

### Wildcards trade future evidence for convenience

A wildcard is correct for a truly irrelevant remainder:

```rust
match pair {
    (0, _) => "zero first component",
    _ => "nonzero first component",
}
```

It is weak in domain rendering where every variant should receive an intentional label. Reviewers should ask whether the wildcard expresses policy or merely silences the compiler.

### Absence is a value, not a sentinel

```rust
fn find_task(tasks: &[Task], id: TaskId) -> Option<&Task> {
    tasks.iter().find(|task| task.id() == id)
}
```

The return type states two legitimate outcomes:

- `Some(&Task)`: a borrowed task was found;
- `None`: no task matched.

No numeric ID, empty string, null pointer, or panicking index is overloaded to mean absence.

### `Option<T>` has zero-or-one cardinality

`Option<T>` adds one explicit absence case to the possible values of `T`. It composes with ownership:

- `Option<Task>` may own one task;
- `Option<&Task>` may borrow one task;
- `Option<&mut Task>` may grant exclusive temporary access to one task.

The wrapper does not erase the inner ownership mode.

### Use `match` when both branches carry policy

```rust
match board.find(id) {
    Some(task) => render(task),
    None => render_missing(id),
}
```

This is explicit and total. It is preferable when both cases do meaningful work or return different domain values.

### Use `if let` for one focused branch

```rust
if let Some(task) = board.find(id) {
    println!("{}", task.title());
}
```

`if let` intentionally ignores the other variant. Add `else` when the absence case matters. Do not use it to conceal required failure handling.

### Use `let ... else` for an early exit

```rust
fn start(board: &mut TaskBoard, id: TaskId) -> bool {
    let Some(task) = board.find_mut(id) else {
        return false;
    };
    task.start().is_ok()
}
```

The pattern must match for execution to continue. The `else` branch must diverge: it returns, breaks, continues, or panics. In capstoneion code, return a typed error rather than `bool` once error design is introduced.

This form keeps the successful path unindented.

### Combinators transform without unpacking manually

```rust
let title = board.find(id).map(Task::title);
```

`map` transforms `Some(T)` into `Some(U)` and preserves `None`.

```rust
let first_done = tasks.iter().find(|task| task.status() == Status::Done);
```

Use combinators when they directly state the operation. Do not turn a multi-step policy into a dense chain that hides which absence case occurred.

### `unwrap` is not an absence policy

```rust
let task = board.find(id).unwrap();
```

This converts a normal missing-ID condition into a panic. It is justified only when the surrounding proof makes `None` impossible and that invariant is locally obvious. User input and persistent data do not meet that standard.

In this course, ordinary library paths return absence or error explicitly.

### `Option` versus `Result`

Use `Option` when absence is the only non-value outcome and callers do not need a reason. Use `Result` when failure carries information or requires different handling.

```rust
fn lookup(id: TaskId) -> Option<&Task>
fn require(id: TaskId) -> Result<&Task, BoardError>
```

The second can convert `None` into `BoardError::NotFound(id)`. The distinction belongs at the API boundary where caller needs are known.

### Begin with a graph, not methods

For the course task domain:

```text
Todo ──start──▶ Doing ──complete──▶ Done
 ▲                                      │
 └──────────────── reopen ──────────────┘
```

This graph defines legal transitions. Every other source-operation pair is rejected. Writing methods before the graph often produces accidental rules because direct assignment is easy.

### Store one authoritative state

```rust
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
enum Status {
    Todo,
    Doing,
    Done,
}
```

Do not duplicate authority:

```rust
struct WeakTask {
    status: Status,
    is_complete: bool,
}
```

Now two fields can disagree. Derived questions should be computed from the authoritative state:

```rust
fn is_complete(&self) -> bool {
    self.status == Status::Done
}
```

### Centralize transition legality

```rust
fn transition(&mut self, target: Status) -> Result<(), TransitionError> {
    let legal = matches!(
        (self.status, target),
        (Status::Todo, Status::Doing)
            | (Status::Doing, Status::Done)
            | (Status::Done, Status::Todo)
    );

    if !legal {
        return Err(TransitionError {
            from: self.status,
            to: target,
        });
    }

    self.status = target;
    Ok(())
}
```

Public domain verbs call this private mechanism:

```rust
fn start(&mut self) -> Result<(), TransitionError> {
    self.transition(Status::Doing)
}
```

Centralization makes the graph reviewable and prevents one method from silently using different rules.

### Validate before mutation

The legal check occurs before assignment. On `Err`, the original status remains unchanged. Tests must prove this:

```rust
let before = task.status();
let result = task.complete();
assert!(result.is_err());
assert_eq!(task.status(), before);
```

A function returning an error after partial mutation needs an explicit transactional design. For this state machine, the simpler and stronger rule is: reject before changing anything.

### Transition errors should expose useful state

```rust
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
struct TransitionError {
    from: Status,
    to: Status,
}
```

This is stronger than `false` or an undifferentiated string. Tests can compare exact failures, and a later `Display` implementation can render user-facing text without losing structured information.

### A typed model cannot prevent every bad value

An enum prevents impossible status combinations, but a `String` title can still be empty and a `u64` ID can still be zero. Strong design layers constraints:

- a `TaskId` newtype narrows valid IDs;
- a private `Task` constructor validates titles;
- a `Status` enum closes the state set;
- private transition methods preserve the graph;
- collection-level code prevents duplicate IDs.

No single type must carry every invariant. Assign each invariant to the smallest boundary that owns enough information to enforce it.

### Typestate is not required here

A more advanced design could use distinct types such as `TodoTask`, `DoingTask`, and `DoneTask`, consuming one and returning another. That can make illegal transitions unrepresentable at compile time, but it complicates heterogeneous storage in a single `Vec` and belongs in a later course.

For this foundation, a runtime enum with private, checked transitions is the appropriate tradeoff. Strong modeling does not mean maximizing type machinery.

### Persistence creates a privileged reconstruction boundary

Stored records already contain a status. Loading cannot call only the ordinary `Task::new`, because that always creates `Todo`. The model can expose a narrowly scoped reconstruction function to the storage module:

```rust
pub(crate) fn from_stored_parts(
    id: TaskId,
    title: String,
    priority: Priority,
    status: Status,
) -> Result<Self, ModelError> {
    validate_title(&title)?;
    Ok(Self { id, title, priority, status })
}
```

`pub(crate)` keeps it unavailable to external users while permitting trusted internal restoration. Storage still validates every field; “came from disk” is not proof of validity.

### Test the graph as a matrix

For three states and three target states, there are nine pairs. A rigorous test table checks all pairs, not only the happy cycle:

| From | To | Expected |
|---|---|---|
| Todo | Todo | reject |
| Todo | Doing | accept |
| Todo | Done | reject |
| Doing | Todo | reject |
| Doing | Doing | reject |
| Doing | Done | accept |
| Done | Todo | accept |
| Done | Doing | reject |
| Done | Done | reject |

This matrix is executable specification. When the graph changes, the table must change intentionally.

### Model checkpoint

Before the complete-program example, verify that the model can decide a design rather than merely name its mechanism.

1. **Outcome 1.** For choose structs, tuple structs, newtypes, enums, and associated data from domain shape rather than language familiarity, construct one positive and one causal negative example. Mark the first decisive fact in the **state model** and state which evidence could falsify the claim.

2. **Outcome 2.** For place invariants at constructors and methods while keeping representation private where external mutation would bypass rules, construct one positive and one causal negative example. Mark the first decisive fact in the **state model** and state which evidence could falsify the claim.

3. **Outcome 3.** For use exhaustive pattern matching to expose every state and transition, construct one positive and one causal negative example. Mark the first decisive fact in the **state model** and state which evidence could falsify the claim.

4. **Outcome 4.** For represent absence with Option and distinguish it from malformed input or failed operations, construct one positive and one causal negative example. Mark the first decisive fact in the **state model** and state which evidence could falsify the claim.

5. **Preservation.** Name one earlier invariant that an easier but less precise implementation could regress.

6. **Boundary.** State one claim this module can justify and one adjacent claim that requires a later course, platform contract, peer behavior, or measurement.

A strong answer records state before and after the operation, the failure path, and the public consequence. An API name by itself is not a model.

## Use the idea in a complete program

The course capstone is **Taskboard**, a persistent command-line task board. Replace stringly records with `Task`, `TaskId`, `Priority`, `Status`, and `Command`. The state graph should make contradictory combinations unrepresentable. The exact implementation task is in the [workbook](workbook.md); the full product contract is in the [capstone guide](../capstone.md).

## Practice sequence

1. Reproduce the important examples from this chapter without copying them line for line.
2. Complete the prediction and repair sections in the [workbook](workbook.md).
3. Build the independent [laboratory](../../labs/module-05-state-machine/README.md).
4. Apply the capstone increment.
5. Open the [reasoned solutions](solutions.md) only after recording your own answer.

## Ready to continue

You are ready for Module 6 when you can:

- answer the module question—“How can the type system make valid states representable and contradictory states difficult or impossible to construct?”—without reading the chapter;
- demonstrate this outcome on a fresh example: Choose structs, tuple structs, newtypes, enums, and associated data from domain shape rather than language familiarity;
- repair the debugging case while preserving its product requirement;
- complete the laboratory transfer variant and explain the decisive design choice;
- name a simpler alternative and the condition under which you would prefer it.

## Primary Rust references

This chapter is self-contained. These official sources are included for verification and future language updates, not as required reading:

- [The Rust Book: Structs](https://doc.rust-lang.org/book/ch05-00-structs.html)
- [The Rust Book: Enums and Pattern Matching](https://doc.rust-lang.org/book/ch06-00-enums.html)
- [Rust Reference: Patterns](https://doc.rust-lang.org/reference/patterns.html)

[← Module 4](../../../01-rust-foundations/course-book/module-04-borrowing-references-slices-and-strings/index.md) · [one-hundred-module map](../../../COURSE_MAP.md) · [Module 6 →](../../../01-rust-foundations/course-book/module-06-collections-iterators-and-closures/index.md)

## Continue

Continue to [Module 6 — Collections, Iterators, and Closures](../module-06-collections-iterators-and-closures/index.md) after completing the workbook, independent laboratory, capstone increment, and closed-book explanation for this module.
