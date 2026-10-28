# Workbook — Module 08: Generics, Traits, Conversions, and Lifetime Basics

[Return to the chapter](index.md) · [Open the Taskboard engineering guide](../capstone.md) · [Open solutions only after attempting the work](solutions.md)

This workbook tests whether you can use **Generics, Traits, Conversions, and Lifetime Basics** without relying on surface syntax. Keep the module question in view: *What behavior is genuinely shared, what constraints make it valid, and what borrow relationship must a signature expose?* For every task, identify the program point where the decisive type, ownership, dispatch, failure, or cost relationship is established. Compile only after committing to a prediction, and preserve the smallest counterexample that changes your model.

## Part 1 — Predict

For each specimen, write a five-part diagnosis: expected outcome; decisive expression or signature; governing rule; smallest requirement-preserving repair; and one tempting change that would compile while weakening the design. Tie every answer to **Generics, Traits, Conversions, and Lifetime Basics** rather than quoting a diagnostic without explaining its cause.

| # | Specimen | Your prediction |
|---:|---|---|
| 1 | [`01-missing-display-bound.rs`](../../compiler-labs/module-08/01-missing-display-bound.rs) | Pass or fail? What exact rule decides? |
| 2 | [`02-incompatible-impl-trait-branches.rs`](../../compiler-labs/module-08/02-incompatible-impl-trait-branches.rs) | Pass or fail? What exact rule decides? |
| 3 | [`03-orphan-rule.rs`](../../compiler-labs/module-08/03-orphan-rule.rs) | Pass or fail? What exact rule decides? |
| 4 | [`04-consumed-writer.rs`](../../compiler-labs/module-08/04-consumed-writer.rs) | Pass or fail? What exact rule decides? |
| 5 | [`05-ambiguous-output-lifetime.rs`](../../compiler-labs/module-08/05-ambiguous-output-lifetime.rs) | Pass or fail? What exact rule decides? |
| 6 | [`06-lifetime-cannot-save-local.rs`](../../compiler-labs/module-08/06-lifetime-cannot-save-local.rs) | Pass or fail? What exact rule decides? |

Run all specimens for this course from the course root with:

```bash
python3 ../tools/run_compiler_labs.py 01-rust-foundations
```

## Part 2 — Diagnose and repair


Review this design:

```rust
trait Store<T, E>
where
    T: Clone + Default + Debug + Display + Ord,
    E: Debug + Display,
{
    fn load<'a>(&'a self) -> Result<&'a Vec<T>, E>;
    fn save(&mut self, values: Vec<T>) -> Result<bool, E>;
}

struct FileTaskStore<'a> {
    path: &'a str,
    cached: Vec<Task>,
}
```

It was introduced solely so tests could avoid the filesystem.

### Review tasks

Identify at least twelve problems, including:

- bounds unrelated to the trait methods;
- `Vec<T>` leakage rather than slice or iterator contracts;
- returned references tied to mutable cache state;
- unexplained `Default` and ordering requirements;
- Boolean success inside `Result`;
- consuming the full vector on every save;
- path represented as UTF-8 text;
- trait and error genericity without real implementations;
- unclear cache invalidation;
- lifetime propagation from a borrowed path;
- inability to test codec rules independently;
- architecture built around testing technique instead of production boundaries.

### Required repair

Remove the custom trait unless you can produce two genuine production implementations with the same semantics. Use:

```rust
fn load_from<R: BufRead>(reader: R) -> Result<TaskBoard, StorageError>;
fn save_to<W: Write>(writer: &mut W, board: &TaskBoard) -> Result<(), StorageError>;
fn load(path: &Path) -> Result<TaskBoard, StorageError>;
fn save(path: &Path, board: &TaskBoard) -> Result<(), StorageError>;
```

Implement standard traits for domain parsing and display. Own the path only in configuration or error values that outlive a call.

### Defense questions

1. Which variation remains generic after the repair?
2. Why are `BufRead` and `Write` meaningful substitution contracts?
3. Which previous bounds disappear and why?
4. How do in-memory tests work without a custom repository interface?
5. Which values now own data, and which are temporary borrows?
6. What future requirement would justify revisiting a repository trait?

## Part 3 — Focused exercises

### Access protocol

Attempt every required exercise and commit the attempt before opening `exercise-answers.md`. Mark each as:


Each answer must explain why its generic parameters, bounds, and lifetimes are necessary. A compiling solution with unexplained generality does not pass.

### 1. Borrowed extrema

Implement `min_max<T: Ord>(values: &[T]) -> Option<(&T, &T)>` in one traversal. Define one-element behavior.

### 2. Generic partition

Implement a function that consumes `Vec<T>` and partitions values according to `FnMut(&T) -> bool`, preserving relative order. State allocations and moves.

### 3. Method-specific bounds

Create `Bag<T>` with `len` for all `T`, `contains` only for `T: PartialEq`, and sorted output only for `T: Ord + Clone`. Justify the clone requirement or redesign to sort references.

### 4. Domain display and parsing

Implement `Display` and `FromStr` for `Priority` and `Status`. Test complete round trips and all unknown tokens.

### 5. Infallible and fallible conversion

Implement `From<DomainError> for AppError` and `TryFrom<u64> for TaskId`. Explain why the inverse conversions are absent.

### 6. `impl Trait` argument relation

Write one function accepting two independently displayable values and another requiring two values of the same displayable type. Demonstrate the call-site difference.

### 7. Generic writer

Implement a deterministic table renderer over `W: Write`. It must not consume the caller's writer and must report write errors.

### 8. Generic reader

Implement a line reader over `R: BufRead` that returns numbered nonempty lines. Decide whether ignoring blank lines belongs in the generic helper or a format-specific layer.

### 9. Longest title

Write a function returning the longer title from two borrowed tasks. State the lifetime relation explicitly. Then write a more precise function that always returns the first title and gives the second input an independent lifetime.

### 10. Borrowed projection

Create `TaskView<'a>` and a function producing views from a task slice. Demonstrate which board mutations are blocked while views remain in use.

### 11. Ownership redesign

Given a report struct with five lifetime parameters that must be stored after its source board is dropped, redesign it to own only the necessary bounded values. Quantify allocations.

### 12. Abstraction audit

Audit all custom traits and generic functions in your capstone branch. For each, list substitutions, required behavior, bounds, callers, and a concrete alternative. Remove anything without a demonstrated benefit.



## Part 4 — Independent laboratory



### Purpose

Build a reusable but bounded report system. The lab tests whether you can distinguish justified genericity from abstraction for its own sake.

### Domain

```rust
struct Metric {
    name: String,
    value: i64,
}

struct Report {
    title: String,
    metrics: Vec<Metric>,
}
```

Invariants:

- titles and metric names are trimmed, nonempty, and at most 80 bytes;
- names contain no tabs or line breaks;
- metric names are unique within a report;
- canonical output sorts metrics by name.

### Required traits

Implement standard traits where justified:

- `Display` for a compact `Metric` view;
- `FromStr` for one metric line;
- `TryFrom<(String, i64)>` for validated `Metric` construction;
- `Default` for an empty `Report` only if the title policy gives it a meaningful title; otherwise do not implement it.

Define at most one custom trait. If you define one, the design document must show at least two meaningful implementations and one generic caller. No custom trait is also a valid and likely outcome.

### Required generic functions

```rust
fn load_report<R: BufRead>(reader: R) -> Result<Report, ReportError>;
fn write_report<W: Write>(writer: &mut W, report: &Report) -> Result<(), ReportError>;
fn extrema<T: Ord>(values: &[T]) -> Option<(&T, &T)>;
```

### Lifetime task

Implement:

```rust
fn choose_metric<'a>(left: &'a Metric, right: &'a Metric) -> &'a Metric;
```

Then implement a function that always returns from the first report while accepting an unrelated second borrow, using separate lifetimes.

### Laboratory: Tests

- all standard-trait round trips;
- invalid names and duplicate metrics;
- generic in-memory read/write;
- exact deterministic bytes;
- write failure using a small custom writer that fails after a byte limit;
- lifetime functions exercised with nested scopes;
- generic extrema for integers and strings;
- a compile-fail explanation for a returned local reference.

### Design document

Explain:

- each generic parameter and bound;
- where monomorphization occurs conceptually;
- every owned versus borrowed field;
- why each standard trait matches its semantic law;
- whether a custom trait survived review;
- which allocations canonical sorting performs;
- why the codec does not know filesystem paths.

### Acceptance

The lab passes only when removing any bound either makes a body operation illegal or broadens semantics incorrectly. Redundant bounds and artificial traits are defects, not extra credit.

### Tiered hints

Do not open a later tier until the previous tier has produced a written attempt.

- **Hint 1 — concept:** return to the governing question: What behavior is genuinely shared, what constraints make it valid, and what borrow relationship must a signature expose?
- **Hint 2 — topology:** draw owners/borrows/states/errors before changing syntax; identify the one boundary that should own the invariant.
- **Hint 3 — structure:** separate validation from mutation and pure transformation from effects. Use the standard operation that encodes the safety fact before inventing an abstraction.
- **Hint 4 — implementation-adjacent:** consult only the relevant standard-library or Reference page; do not open `solution/src`.

The executable starter and reference implementation are in [module-08-traits-and-lifetimes](../../labs/module-08-traits-and-lifetimes/README.md). Implement from the contract first. Compare with the reference only after your tests pass or you have written a precise blocker.

## Part 5 — Capstone transfer

### Outcomes mapped

- Write generic functions and types whose bounds correspond to operations actually performed.
- Define and implement small traits as behavioral contracts without abstraction theater.
- Use Display, Error, From, FromStr, Read, BufRead, and Write at natural boundaries.
- Derive ordinary lifetime annotations from input-output provenance and distinguish annotation from lifetime extension.
- Choose ownership instead of adding lifetime parameters when values must be retained independently.


### Objective

Refactor the capstone so shared behavior is expressed through standard contracts without turning the domain into a generic framework.

### Required standard traits

Implement where semantically justified:

- `Display` for `TaskId`, `Priority`, `Status`, and user-facing error types;
- `FromStr` for `TaskId`, `Priority`, and `Status`;
- `TryFrom<u64>` for `TaskId` if construction is public enough to benefit;
- `From<CommandError>`, `From<DomainError>`, and `From<StorageError>` for `AppError` when conversion preserves all information;
- `Default` for `TaskBoard` if it is exactly equivalent to `TaskBoard::new()`.

Do not implement ordering, hashing, cloning, or defaults without a real use and valid domain meaning.

### Generic codec boundary

Storage must support in-memory tests through:

```rust
fn load_from<R: BufRead>(reader: R) -> Result<TaskBoard, StorageError>;
fn save_to<W: Write>(writer: &mut W, board: &TaskBoard) -> Result<(), StorageError>;
```

The path-based wrappers own path context and commit behavior.

### Lifetime audit

Document these relationships:

- `Task::title(&self) -> &str` returns from task-owned storage;
- `TaskBoard::tasks(&self) -> &[Task]` returns a view tied to the board;
- `TaskBoard::find(&self, id) -> Option<&Task>` returns from board storage;
- rendering returns owned `String` so output can leave the borrow scope;
- parsing errors own bounded token evidence.

Do not annotate lifetimes already clear by elision unless the annotation teaches a nontrivial relation.

### Abstraction exclusions

The capstone should not add:

- a generic `TaskBoard<T>`;
- a custom collection trait;
- a repository trait with one implementation;
- generic error parameters;
- trait-object command handlers;
- lifetime parameters on owned domain types.

### Capstone: Tests

- `Display`/`FromStr` round trip for each domain token;
- invalid token variants retain original text;
- generic codec works with in-memory input/output;
- conversion to `AppError` preserves nested variant and source;
- borrowed accessors do not allocate;
- ownership-returning operations are explicit.

### Review questions
For every `impl`, generic parameter, bound, and explicit lifetime in the capstone, provide one sentence answering: “What contract would be lost if this were removed?” Remove code without a convincing answer.



### Capstone defense

Refactor a concrete file codec into a BufRead/Write boundary and derive the lifetime of a borrowed selector without overconstraining unrelated inputs.

## Part 6 — Reconstruct and defend

Complete this checkpoint closed-book. Compiler access is allowed only after the prediction portion has been committed.

### Outcome reconstruction

For each outcome, write a claim, one example, one non-example, and one limitation.

- Write generic functions and types whose bounds correspond to operations actually performed.
- Define and implement small traits as behavioral contracts without abstraction theater.
- Use Display, Error, From, FromStr, Read, BufRead, and Write at natural boundaries.
- Derive ordinary lifetime annotations from input-output provenance and distinguish annotation from lifetime extension.
- Choose ownership instead of adding lifetime parameters when values must be retained independently.

### Closed-book checkpoint

#### Part A — Generic reasoning

1. Write `first<T>(&[T]) -> Option<&T>` and explain why no bounds are needed.
2. Write `maximum<T: Ord>(&[T]) -> Option<&T>` and justify `Ord`.
3. Explain monomorphization without claiming exact binary duplication.
4. Give an example where a method-specific bound is better than a type-level bound.
5. Explain why an unconstrained generic return may need annotation.

#### Part B — Trait contracts

1. State the orphan-rule condition at a practical level.
2. Explain one conflict caused by a blanket implementation.
3. Distinguish `Display` and `Debug`.
4. Distinguish `From` and `TryFrom`.
5. Explain why deriving `Ord` may be semantically wrong.
6. Name one standard trait that provides a test seam in this course.

#### Part C — `impl Trait`

1. Contrast two independent argument-position `impl Display` parameters with one named `T: Display`.
2. Explain why return-position `impl Iterator` must hide one concrete type.
3. State whether either form implies runtime dynamic dispatch.

#### Part D — Lifetimes

Annotate and explain:

```rust
fn title(task: &Task) -> &str;
fn choose(left: &Task, right: &Task) -> &Task;
fn first(left: &Task, unrelated: &Task) -> &Task;
```

Then explain why this cannot be repaired with a lifetime:

```rust
fn generated() -> &str {
    &String::from("temporary")
}
```

#### Part E — Ownership audit

Choose borrowed or owned output for:

- a task title displayed immediately;
- a report row stored after the board is dropped;
- an invalid token inside a propagated error;
- a parser cursor over caller input;
- persistent task state.

#### Pass standard

Pass requires:

- every bound tied to a body operation or semantic law;
- no confusion between static generics and runtime dispatch;
- correct orphan and conversion reasoning;
- precise output lifetime sources;
- willingness to own data where borrowing harms the lifecycle.

Any belief that `'static` prolongs a local value requires repeating the lifetime chapter and compiler lab.

### Transfer defense

Refactor a concrete file codec into a BufRead/Write boundary and derive the lifetime of a borrowed selector without overconstraining unrelated inputs.

Your answer must include:
