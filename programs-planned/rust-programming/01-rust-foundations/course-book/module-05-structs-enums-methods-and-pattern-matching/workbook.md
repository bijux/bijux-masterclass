# Workbook — Module 05: Structs, Enums, Methods, and Pattern Matching

[Chapter](index.md) · [Laboratory](../../labs/module-05-state-machine/README.md) · [Taskboard guide](../capstone.md) · [Solutions](solutions.md)

This workbook tests whether **Structs, Enums, Methods, and Pattern Matching** has become a usable model rather than remembered vocabulary. Its governing question is: *How can the type system make valid states representable and contradictory states difficult or impossible to construct?* Preserve your first prediction and record decisive facts in a **state model**. A repair succeeds only when it keeps the difficult product requirement visible.

## Retrieval warm-up

Before compiling or running anything:

1. Restate the invariant from Module 4 — Borrowing, References, Slices, and Strings that today’s mechanism must preserve.
2. Rewrite the governing question in your own words: **How can the type system make valid states representable and contradictory states difficult or impossible to construct?**
3. Draw the smallest **state model** that could decide one positive and one negative case.
4. Name one shortcut that could make the visible example pass while deleting ownership, failure, ordering, capacity, safety, compatibility, or evidence required by the product.

## Part 1 — Predict

For each specimen, write a five-part diagnosis: expected outcome; decisive expression or signature; governing rule; smallest requirement-preserving repair; and one tempting change that would compile while weakening the design. Tie every answer to **Structs, Enums, Methods, and Pattern Matching** rather than quoting a diagnostic without explaining its cause.

| # | Specimen | Your prediction |
|---:|---|---|
| 1 | [`01-private-newtype-field.rs`](../../compiler-labs/module-05/01-private-newtype-field.rs) | Pass or fail? What exact rule decides? |
| 2 | [`02-non-exhaustive-match.rs`](../../compiler-labs/module-05/02-non-exhaustive-match.rs) | Pass or fail? What exact rule decides? |
| 3 | [`03-moved-enum-payload.rs`](../../compiler-labs/module-05/03-moved-enum-payload.rs) | Pass or fail? What exact rule decides? |
| 4 | [`04-option-is-not-sentinel.rs`](../../compiler-labs/module-05/04-option-is-not-sentinel.rs) | Pass or fail? What exact rule decides? |
| 5 | [`05-method-receiver-mismatch.rs`](../../compiler-labs/module-05/05-method-receiver-mismatch.rs) | Pass or fail? What exact rule decides? |
| 6 | [`06-let-else-diverges.rs`](../../compiler-labs/module-05/06-let-else-diverges.rs) | Pass or fail? What exact rule decides? |

Run all specimens for this course from the course root with:

```bash
python3 ../tools/run_compiler_labs.py 01-rust-foundations
```

## Part 2 — Diagnose and repair

### Defective model

A migrated application uses this representation:

```rust
#[derive(Debug)]
pub struct WorkItem {
    pub id: u64,
    pub title: String,
    pub status_text: String,
    pub is_started: bool,
    pub is_complete: bool,
    pub completed_message: Option<String>,
}

pub fn complete(item: &mut WorkItem) -> bool {
    item.is_complete = true;
    if !item.is_started {
        return false;
    }
    item.status_text = "done".to_owned();
    item.completed_message = Some("completed".to_owned());
    true
}
```

The function compiles. It can return `false` while leaving `is_complete == true`. Callers can also construct:

```text
status_text = "todo"
is_started = false
is_complete = true
completed_message = None
```

No single field is authoritative.

### Required repair

Replace the representation with:

- a non-zero `WorkItemId` newtype;
- a `WorkState` enum;
- a `WorkItem` struct with private fields;
- an infallible constructor for a validated ID and non-empty title;
- named `start`, `complete`, and `reopen` methods;
- a structured `TransitionError` containing source and target states;
- read-only accessors returning borrowed text;
- no general `set_state` method.

The legal graph is:

```text
Queued -> Active -> Completed -> Queued
```

Every other transition fails and preserves the previous state.

### Clinic: Constraints

- Do not make fields public.
- Do not keep the old Boolean flags as caches.
- Do not use arbitrary status strings as authoritative state.
- Do not clone the title to satisfy a getter.
- Do not mutate before all checks pass.
- Do not use a wildcard in the state renderer.
- Do not convert transition failure to `bool` inside the model.

### Test matrix

Write tests for all nine source-target pairs. Add separate tests for:

1. ID zero is rejected;
2. the title accessor borrows rather than allocates;
3. a failed transition leaves the complete value equal to a snapshot taken before the call;
4. the renderer handles every state;
5. outside-module code cannot mutate fields directly—this is demonstrated by the public API shape and compiler-lab reasoning rather than a passing runtime test.

### Diagnostic method

Before editing, produce a state-space analysis:

| Representation | Approximate combinations | Meaningful combinations | Contradictions admitted |
|---|---:|---:|---:|
| three flags | 8 | 3 | 5 |
| free-form string | unbounded | 3 | unbounded |
| three-variant enum | 3 | 3 | 0 at top level |

Then identify the invariant boundary for each fact:

| Fact | Boundary |
|---|---|
| ID is non-zero | `WorkItemId::new` |
| title is non-empty | `WorkItem::new` |
| state is one of three variants | `WorkState` type |
| transition is legal | private transition method |
| failed transition preserves state | method ordering plus tests |

### Review questions

1. Which old fields were independent but should have been derived?
2. Why is `completed_message: Option<String>` suspicious in every state?
3. Would a state enum with associated data be stronger if completion carried a timestamp? Show the shape.
4. Which invariants remain runtime-checked after the refactor?
5. Why can the compiler not prove the entire transition graph from this enum alone?

## Part 3 — Focused exercises

### Access protocol

Attempt every required exercise and commit the attempt before opening `exercise-answers.md`. Mark each as:

Complete every exercise before reading the answer file. Each solution must include tests and a short representation argument, not only code.

### Exercise 1 — Representation cardinality

For each design below, enumerate or calculate the possible top-level states and identify the meaningful subset:

1. `is_new`, `is_running`, `is_finished` Boolean flags;
2. `status: String` intended to hold three spellings;
3. `enum Status { New, Running, Finished }`;
4. `Option<Status>`;
5. `Result<Option<Status>, ParseError>`.

Explain which invalid states are removed by type choice and which still require runtime validation.

### Exercise 2 — Non-zero identifiers

Implement a private-field `TaskId` newtype with:

- `TaskId::new(u64) -> Option<TaskId>`;
- `TaskId::get(self) -> u64`;
- `Debug`, `Clone`, `Copy`, `Eq`, and `PartialEq`;
- tests for zero, one, and `u64::MAX`.

Explain why `get` can take `self` without consuming the caller's usable value.

### Exercise 3 — Validated range

Implement `ScoreRange` with private `minimum` and `maximum` fields. Construction fails when `minimum > maximum`. Provide:

- `try_new`;
- `contains`;
- `width` using checked subtraction or a type choice that makes overflow reasoning explicit;
- read-only accessors.

Test exact boundaries and failed construction.

### Exercise 4 — Receiver audit

For each operation on a document type, choose no receiver, `&self`, `&mut self`, or `self`, then implement it:

- construct from a title and body;
- read title;
- count body characters;
- rename after validation;
- append text;
- extract the owned body because the document will be discarded;
- create a modified document in builder style.

Record why stronger access would be unnecessary.

### Exercise 5 — Typed commands

Replace this weak command struct:

```rust
struct RawCommand {
    action: String,
    id: Option<u64>,
    title: Option<String>,
    priority: Option<String>,
}
```

with enums that represent only these operations:

```text
add PRIORITY TITLE
list [STATUS]
start ID
complete ID
help
```

Calculate at least five contradictory values admitted by `RawCommand` that the enum cannot represent.

### Exercise 6 — Exhaustive rendering

Define `Priority` and `Status` enums. Write total functions returning stable storage tokens and separate human-facing labels. Do not use wildcard arms. Add one temporary variant and observe every consumer that becomes incomplete; record the locations before removing it.

### Exercise 7 — Pattern ownership

Given `Command::Add { title: String, priority: Priority }`:

1. write a function that consumes the command and returns the owned title when it is `Add`;
2. write a function that borrows the command and returns `Option<&str>`;
3. explain why the first cannot use the original command afterward;
4. demonstrate a partial move from a struct and a borrowed destructure that avoids it.

### Exercise 8 — Optional lookup

Over `&[Task]`, implement:

- `find(&[Task], TaskId) -> Option<&Task>`;
- `find_mut(&mut [Task], TaskId) -> Option<&mut Task>`;
- `require(&[Task], TaskId) -> Result<&Task, LookupError>`.

Use `let ... else` in one implementation and a combinator in another. Explain why returning a reference to a local fallback task is invalid.

### Exercise 9 — Transition matrix

Implement a three-state task graph:

```text
Todo -> Doing -> Done -> Todo
```

Expose named methods, keep the general transition method private, and test all nine source-target pairs. Every rejected transition must preserve the original task exactly.

### Exercise 10 — Associated-data redesign

A processing job currently stores:

```rust
struct Job {
    state: String,
    worker: Option<String>,
    error: Option<String>,
    output: Option<String>,
}
```

Redesign the state with associated data so that:

- queued jobs carry no worker, error, or output;
- running jobs carry a worker;
- failed jobs carry a message and retryability;
- successful jobs carry an output path.

Write exhaustive functions `summary(&JobState) -> String` and `can_retry(&JobState) -> bool`. Identify which cross-field contradictions disappear and which payload validations remain.

### What to record
For every exercise submit:

- source and tests;
- a one-paragraph ownership note;
- a one-paragraph state-space or invariant note;
- the exact `cargo test` result;
- any compiler diagnostic that changed the design.

### Interleaved reasoning pass

1. For **Choose structs, tuple structs, newtypes, enums, and associated data from domain shape rather than language familiarity**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the state model.
2. For **Place invariants at constructors and methods while keeping representation private where external mutation would bypass rules**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the state model.
3. For **Use exhaustive pattern matching to expose every state and transition**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the state model.
4. For **Represent absence with Option and distinguish it from malformed input or failed operations**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the state model.

5. Identify one guarantee from an earlier course that a careless implementation of **Structs, Enums, Methods, and Pattern Matching** could regress.

For one case, write both a principled repair and a weaker repair that appears to work. The principled repair must preserve the requirement; the weaker repair must name the information, state, bound, or compatibility promise it silently discards.

## Part 4 — Independent laboratory

### Objective

Build an independent package whose public API makes task identity, priority, status, and legal transitions explicit. The laboratory is not a reduced capstone copy; it is a focused proof that you can turn a state graph into a private, testable model.

The complete specification is mirrored at `labs/module-05-state-machine/README.md`. Do not inspect the `solution` directory until the independent attempt passes the required behavioral tests.

### Required model

Implement:

```rust
pub struct TaskId(/* private non-zero u64 */);

pub enum Priority {
    Low,
    Normal,
    High,
}

pub enum Status {
    Todo,
    Doing,
    Done,
}

pub struct Task {
    // private fields
}
```

`Task` owns its title. Accessors expose borrowed or copied values as appropriate.

### Required invariants

1. `TaskId` cannot be constructed from zero through the public API.
2. A new task begins in `Status::Todo`.
3. The title is not empty after trimming.
4. The only legal state cycle is:

   ```text
   Todo -> Doing -> Done -> Todo
   ```

5. A rejected transition preserves every task field.
6. No public operation can assign an arbitrary status.

### Required operations

- `TaskId::new`;
- `Task::try_new` or a documented equivalent;
- `id`, `title`, `priority`, and `status` accessors;
- `rename` with validation-before-mutation;
- `start`, `complete`, and `reopen`;
- total textual rendering for `Priority` and `Status`;
- a structured title error;
- a structured transition error carrying source and target.

### Laboratory: Required tests

At minimum:

- zero and non-zero ID construction;
- empty, whitespace-only, valid, and boundary-length titles;
- initial status;
- complete legal cycle;
- all six illegal source-target pairs;
- exact transition error contents;
- equality of the whole task before and after every rejected operation;
- rename success and rename failure preservation;
- exhaustive stable tokens for all priority and status variants.

Do not test only `is_err()`. Compare the error and post-state.

### Analysis deliverable

Submit a table showing the representation before and after:

| Concern | Weak representation | Typed representation | Remaining runtime check |
|---|---|---|---|
| identity | raw `u64` | `TaskId` | non-zero at construction |
| state | strings/flags | `Status` | transition legality |
| title | unrestricted `String` | private owned field | content validation |
| mutation | public assignment | named methods | operation-specific policy |

Add a receiver table for every public method.

### Laboratory: Constraints

- standard library only;
- safe Rust only;
- no public fields;
- no general status setter;
- no panic-based user-input validation;
- no direct `.unwrap()` or `.expect()` in library code;
- no wildcard in domain rendering;
- no clone added only to bypass ownership reasoning.

### Verification

From the course root:

```bash
cargo test -p rust-foundations-lab-05
cargo clippy -p rust-foundations-lab-05 --all-targets -- -D warnings
cargo fmt --all -- --check
```

### Reference comparison

After completion, inspect `labs/module-05-state-machine/solution/`. Compare:

- public surface;
- transition centralization;
- mutation ordering;
- error information;
- tests for preservation.

Do not replace a stronger independent design merely because the reference differs.

### Tiered hints

Do not open a later tier until the previous tier has produced a written attempt.

- **Hint 1 — concept:** return to the governing question: How can the type system make valid states representable and contradictory states difficult or impossible to construct?
- **Hint 2 — topology:** draw owners/borrows/states/errors before changing syntax; identify the one boundary that should own the invariant.
- **Hint 3 — structure:** separate validation from mutation and pure transformation from effects. Use the standard operation that encodes the safety fact before inventing an abstraction.
- **Hint 4 — implementation-adjacent:** consult only the relevant standard-library or Reference page; do not open `solution/src`.

The executable starter and reference implementation are in [module-05-state-machine](../../labs/module-05-state-machine/README.md). Implement from the contract first. Compare with the reference only after your tests pass or you have written a precise blocker.

### Laboratory acceptance trace

Before opening the reference implementation for **Typed Workflow State Machine**, record:

- the public behavior that demonstrates **Choose structs, tuple structs, newtypes, enums, and associated data from domain shape rather than language familiarity**;
- one adversarial input, state transition, schedule, peer action, workload, or build condition appropriate to this module;
- the exact state after rejection or partial failure;
- ownership and cleanup;
- ordering and capacity;
- one shortcut deliberately excluded by the contract;
- one claim the tests cannot establish.

## Part 5 — Capstone transfer

### Outcomes mapped

- Choose structs, tuple structs, newtypes, enums, and associated data from domain shape rather than language familiarity.
- Place invariants at constructors and methods while keeping representation private where external mutation would bypass rules.
- Use exhaustive pattern matching to expose every state and transition.
- Represent absence with Option and distinguish it from malformed input or failed operations.
- Replace Boolean-flag and stringly typed state with an explicit state machine and tested legal transitions.

### Starting point

The Day 4 capstone can borrow titles and locate mutable records, but its task representation still uses tuples or weak textual fields. That representation was useful for exposing ownership mechanics. It is now the principal design liability.

### Required transformation

Introduce private domain types equivalent to:

```rust
pub struct TaskId(u64);

pub enum Priority {
    Low,
    Normal,
    High,
}

pub enum Status {
    Todo,
    Doing,
    Done,
}

pub struct Task {
    id: TaskId,
    title: String,
    priority: Priority,
    status: Status,
}
```

The exact field order is irrelevant. The invariant boundary is not.

### Construction routes

Provide two conceptually different routes:

1. an ordinary constructor that creates a validated new task in `Todo`;
2. an internal reconstruction route for a later persistence layer, capable of validating stored status without exposing arbitrary construction publicly.

At Day 5, the reconstruction route may remain `pub(crate)` and unused. Document why it is not part of the external API.

### Typed commands

Replace command names plus optional fields with:

```rust
enum Command {
    Add { priority: Priority, title: String },
    List { status: Option<Status> },
    Start(TaskId),
    Done(TaskId),
    Reopen(TaskId),
    Remove(TaskId),
    Search(String),
    Stats,
    Help,
}
```

Parsing is completed later. Today, hard-coded commands may drive execution. The design proof is that a constructed command has all and only the data required by its variant.

### Transition contract

Implement:

```text
Todo --start--> Doing
Doing --complete--> Done
Done --reopen--> Todo
```

Every illegal operation returns a structured error and leaves the task unchanged. No general `set_status` function may remain.

### Visibility contract

Outside the model module:

- fields are inaccessible;
- status changes occur only through domain verbs;
- title observation returns `&str`;
- ID, priority, and status may be copied if their types are `Copy`;
- reconstructing an arbitrary status is not part of the public library API.

### Capstone: Required tests

1. a new task starts in `Todo`;
2. title validation rejects forbidden input;
3. all legal transitions succeed;
4. all illegal transitions return exact source/target errors;
5. failed rename and transition operations preserve the whole task;
6. all enum renderers are exhaustive;
7. zero cannot become a `TaskId`;
8. command variants carry the intended payloads.

### Design record

Add a capstone architecture note answering:

- Which impossible values disappeared?
- Which invalid values remain possible inside raw input but not inside the model?
- Why is a private field stronger than a public setter pair?
- Which invariants belong to `Task`, and which will belong to `TaskBoard`?
- What change would be required to add a `Blocked { reason }` state?

### Acceptance

Run the capstone model tests and the whole workspace. The step fails review if arbitrary status assignment remains possible, even if all current tests pass.

### Capstone defense

Convert a contradictory multi-flag workflow into one authoritative enum and prove that illegal combinations are no longer constructible.

### Capstone invariant trace

For the Module 5 Taskboard increment, name the changed invariant and its owner before editing code. Follow it through input, validation, state transition, effect, output, failure, cleanup, and tests. Add storage, wire, scheduler, generated-code, compatibility, resource, or measurement consequences when this course makes them relevant. End by naming one earlier guarantee that remains unchanged.

## Part 6 — Reconstruct and defend

Complete this checkpoint closed-book. Compiler access is allowed only after the prediction portion has been committed.

### Outcome reconstruction

For each outcome, write a claim, one example, one non-example, and one limitation.

Without reopening the chapter, reconstruct the outcomes for **Module 05: Structs, Enums, Methods, and Pattern Matching**. Compare your list with the earlier outcome map only after writing it, then mark each item as modelled, predicted, repaired, built, transferred, or still unsupported.

### Closed-book checkpoint

Close the course book and source files. Answer in one sitting. Compile only after all predictions are recorded.

#### Part A — Representation reasoning

1. Three Boolean state flags admit how many combinations? If exactly one should be true, how many are contradictory?
2. Why is `status: String` weaker than a three-variant enum even when parsing validates input once?
3. Give one invariant a newtype can protect and one it cannot protect alone.
4. Explain why private fields do not automatically prove a valid struct.
5. Distinguish an ordinary constructor from a persistence reconstruction route.

#### Part B — Receiver selection

For each operation, choose associated function, `&self`, `&mut self`, or `self` and justify:

1. construct a task;
2. read its title;
3. start it;
4. extract its owned title and discard the task;
5. return a copy of its ID;
6. validate an independent title string.

#### Part C — Match and ownership

Predict whether each operation moves data:

1. matching an owned enum and binding a `String` payload;
2. matching `&Command` and binding its title;
3. matching a `Copy` status by value;
4. destructuring an owned struct with one `String` field ignored by `..`;
5. returning `Option<&str>` from a borrowed command.

#### Part D — `Option`

1. What outcomes does `Option<&mut Task>` represent?
2. When is `let Some(value) = expression else { ... };` preferable to a nested `match`?
3. Why must its `else` branch diverge?
4. Convert `Option<&Task>` to `Result<&Task, LookupError>` without a manual `match`.
5. Explain why `unwrap` is not acceptable for a missing user-selected ID.

#### Part E — State graph

From memory, write the complete 3×3 transition matrix for `Todo`, `Doing`, and `Done`. Then implement the legality predicate in one expression.

State precisely why this sequence is required:

```text
validate source/target -> return error if illegal -> assign target -> return success
```

#### Part F — Repair

A method does this:

```rust
fn complete(&mut self) -> Result<(), TransitionError> {
    self.status = Status::Done;
    if self.was_started {
        Ok(())
    } else {
        Err(TransitionError)
    }
}
```

Identify every representation and failure-contract defect. Produce a typed repair without `was_started`.

#### Pass conditions

- at least 85% overall;
- no incorrect receiver selection;
- complete transition matrix;
- explicit recognition that an error-returning operation can still corrupt state;
- correct ownership analysis for matching owned versus borrowed enums.

Failure on the transition or ownership sections requires targeted repair before collection traversal begins.

### Transfer defense

Transfer **Module 05: Structs, Enums, Methods, and Pattern Matching** to a product unrelated to the course capstone. Change the domain model and failure mode, preserve the governing relationship, and identify which part of the original design was essential rather than accidental.

Your answer must include:

- the governing rule for **Module 05: Structs, Enums, Methods, and Pattern Matching** in plain language;
- state, ownership, or authority before and after the decisive operation;
- one causal negative case that fails for the intended reason;
- one principled repair and one easier repair that deletes a requirement;
- the limit of the evidence you used;
- one transfer to a product with different data and failure behavior.


### Closed-book defense

In five minutes, answer “How can the type system make valid states representable and contradictory states difficult or impossible to construct?” using the **state model**. Include one positive case, one causal negative case, one principled repair, one rejected shortcut, and one transfer outside Taskboard. A list of APIs without the deciding relationship is incomplete.
