# Module 08 — Generics, Traits, Conversions, and Lifetime Basics

**Course 1 · Day 8 · Module 8 of 100**
`██░░░░░░░░░░░░░░░░░░░░░░░` **8/100**

[Program](../../../README.md) · [Course 1](../index.md) · [Workbook](workbook.md) · [Laboratory](../../labs/module-08-traits-and-lifetimes/README.md) · [Taskboard guide](../capstone.md)

[← Module 7: Errors, Parsing, Files, and Persistence](../module-07-errors-parsing-files-and-persistence/index.md) · [Module 9: Crates, Modules, Public APIs, Tests, and Documentation →](../module-09-crates-modules-public-apis-tests-and-documentation/index.md)

## The question

> What behavior is genuinely shared, what constraints make it valid, and what borrow relationship must a signature expose?

## Why this comes now

You have now written several concrete versions of the same shapes: parsing, rendering, comparison, and borrowed selection. Generics and traits are introduced at the point where duplication is real, while foundational lifetimes explain only the reference relationships that signatures must expose. Course 3 will later treat public trait architecture in depth.

### Prerequisite bridge

Module 7 established **Errors, Parsing, Files, and Persistence**. Before continuing, verify that you can state the exact persistence guarantee of a temporary-file-and-rename protocol, including what it does not guarantee across platforms, crashes, and concurrent writers. This module preserves that capability and adds the ability to write generic functions and types whose bounds correspond to operations actually performed. Module 9, **Crates, Modules, Public APIs, Tests, and Documentation**, will rely on both when it asks: *Which surfaces are product contracts, which are implementation details, and what independent evidence protects each boundary?*

### Scope boundary

This module owns the reasoning for **generics, traits, conversions, and lifetime basics** inside Course 1. The course stays in safe Rust and mostly in the standard library. It introduces the ownership, trait, iterator, lifetime, module, and testing vocabulary required by later courses, but it does not yet pursue advanced lifetime algebra, smart-pointer architecture, unsafe code, concurrency, async runtimes, or macro construction. The purpose of the boundary is to keep the decisive relationship visible before later mechanisms are layered on top of it.

## What you will be able to do

- Write generic functions and types whose bounds correspond to operations actually performed.
- Define and implement small traits as behavioral contracts without abstraction theater.
- Use Display, Error, From, FromStr, Read, BufRead, and Write at natural boundaries.
- Derive ordinary lifetime annotations from input-output provenance and distinguish annotation from lifetime extension.
- Choose ownership instead of adding lifetime parameters when values must be retained independently.

## Core model

### Why this module exists

Generics and traits should express real shared behavior, not decorate code with abstraction. Foundational lifetimes should expose where a returned borrow comes from, not become an annotation guessing game. This module gives enough depth to design ordinary reusable APIs while reserving advanced trait architecture and lifetime algebra for later courses.

### Generic code is type-checked under constraints

```rust
pub fn first_equal<T: PartialEq>(values: &[T], target: &T) -> Option<&T> {
    values.iter().find(|value| *value == target)
}
```

The bound exists because equality is used. It is not added because “generic functions need traits.” At compilation, Rust monomorphizes many generic uses into concrete code; this is not dynamic dispatch.

Use a `where` clause when bounds become easier to read or apply to associated relationships. Avoid making every input generic if the product only supports one domain type.

### Traits are behavioral contracts

A useful trait has a coherent semantic promise and more than one meaningful implementation or an important abstraction boundary.

```rust
pub trait Render {
    fn render(&self) -> String;
}
```

This trait is weak unless the course defines formatting stability, allocation expectations, or why callers need to abstract across renderers. Often the standard `Display` trait is the natural boundary instead.

Prefer standard traits when their contract matches:

- `Display` for user-facing formatting;
- `FromStr` for whole-value textual parsing;
- `From`/`TryFrom` for conversions;
- `Error` for error sources;
- `Read`/`BufRead`/`Write` for I/O capabilities.

Do not implement a trait solely to demonstrate syntax.

### `impl Trait` and named parameters

In argument position, `impl Trait` is shorthand for a generic parameter in many ordinary uses:

```rust
pub fn write_report(mut output: impl std::io::Write, report: &Report) -> std::io::Result<()> {
    writeln!(output, "{}", report)
}
```

A named parameter is needed when two arguments must share the same concrete type or the type appears elsewhere in the signature. Return-position `impl Trait` hides one concrete return type chosen by the function; it does not mean “any type implementing the trait.” Course 3 studies these design boundaries more deeply.

### Lifetime annotations expose provenance

Elision handles common one-source signatures:

```rust
pub fn first_word(input: &str) -> &str { /* ... */ # input }
```

The returned borrow is tied to `input`. With multiple candidate sources, the relationship must be stated:

```rust
pub fn choose<'a>(left: &'a str, right: &'a str, use_left: bool) -> &'a str {
    if use_left { left } else { right }
}
```

The named `'a` does not force the runtime borrows to have equal original duration and does not extend either value. At a call, it represents a region compatible with both inputs and the returned use—typically no longer than the shorter relevant borrow.

A function returning only from `left` should not tie `right` unnecessarily:

```rust
pub fn prefix_from<'a>(left: &'a str, right: &str) -> &'a str {
    let _ = right;
    left.split_whitespace().next().unwrap_or("")
}
```

Course 2 turns this into explicit constraint algebra.

### Reference-bearing types versus ownership

A struct containing references is useful when it is truly a temporary view:

```rust
pub struct RecordView<'a> {
    pub key: &'a str,
    pub value: &'a str,
}
```

If the value must be queued, cached, returned independently, or stored beyond the input's borrow, own it. Adding lifetime parameters cannot make local data live longer. Ownership often produces a simpler and more truthful API.

### Worked derivation: generic codec boundary

```rust
pub fn save_to<W: std::io::Write>(
    mut writer: W,
    board: &TaskBoard,
) -> Result<(), SaveError> {
    writeln!(writer, "TASKBOARD-V1").map_err(SaveError::Io)?;
    for task in board.tasks() {
        writeln!(writer, "{}", EncodedTask(task)).map_err(SaveError::Io)?;
    }
    Ok(())
}
```

The generic parameter exists because tests can supply `Vec<u8>` and production can supply a buffered file. The board is borrowed because saving does not retain or mutate it. `EncodedTask` can implement `Display` to centralize the grammar.

### Try without the scaffold

Implement `parse_pair<'a>(left: &'a str, delimiter: &str) -> Option<(&'a str, &'a str)>`. Derive why the delimiter lifetime is independent. Then decide whether a parsed record should keep borrowed fields or own them for later storage.

### Misconception clinic

- **“Generics are runtime polymorphism.”** Generic instantiations are normally statically compiled.
- **“A custom trait makes code extensible.”** It may add indirection and public commitment without a real variation point.
- **“Lifetime annotations extend validity.”** They constrain relationships among already-valid borrows.
- **“Most generic API is best.”** The best API exposes the needed capability with the smallest truthful contract.

### Generalize one real axis

Two functions that differ only in element type may justify a generic function:

```rust
fn first<T>(values: &[T]) -> Option<&T> {
    values.first()
}
```

The body does not inspect or copy `T`; it only uses slice structure. Therefore no trait bound is needed.

By contrast, this function needs ordering:

```rust
fn maximum<T: Ord>(values: &[T]) -> Option<&T> {
    values.iter().max()
}
```

The bound is not decoration. It is evidence that comparisons used by `max` are legal.

### Generic types preserve relationships

```rust
#[derive(Debug, PartialEq, Eq)]
struct Pair<T> {
    left: T,
    right: T,
}
```

Both fields have the same type. A two-parameter design permits different types:

```rust
struct Mapping<K, V> {
    key: K,
    value: V,
}
```

Choose parameters that encode actual relationships. Splitting every field into a separate parameter can make an API technically flexible and semantically unbounded.

### Type inference remains local

```rust
let numbers = vec![1_u64, 2, 3];
let first_number = first(&numbers);
```

The compiler infers `T = u64` from the argument. If no use constrains a parameter, annotation may be necessary:

```rust
let empty: Vec<Task> = Vec::new();
```

A generic return type that cannot be inferred from inputs or expected context is often awkward API design.

### Monomorphization

For ordinary static generics, Rust compiles concrete versions required by use sites. Conceptually, calls to `first::<u64>` and `first::<String>` produce type-specific machine code after optimization.

Practical consequences:

- operations are statically checked for each concrete type;
- there is normally no per-call virtual dispatch cost;
- many concrete instantiations can increase compile time and binary size;
- implementation details can still be optimized away;
- this is not a license to make every helper generic.

Do not promise exact code duplication without inspecting compiler output; optimizers can merge or eliminate code. The useful model is static specialization by concrete type.

### Turbofish syntax

Usually inference is enough. Explicit type arguments help when output is ambiguous:

```rust
let value = "42".parse::<u64>()?;
let numbers = tokens.collect::<Result<Vec<u64>, _>>()?;
```

The `::<...>` syntax is not a different call mechanism; it supplies generic arguments explicitly.

### Generic methods

An implementation may be generic because the type is generic:

```rust
impl<T> Pair<T> {
    fn swap(self) -> Self {
        Self {
            left: self.right,
            right: self.left,
        }
    }
}
```

Other methods can require extra bounds:

```rust
impl<T: Ord> Pair<T> {
    fn ordered(self) -> Self {
        if self.left <= self.right {
            self
        } else {
            self.swap()
        }
    }
}
```

Values of `Pair<T>` still exist for non-`Ord` types; only `ordered` is unavailable.

### Avoid abstracting coincidental syntax

Two functions may both contain a loop but serve unrelated contracts. Extracting one generic engine can force complex callbacks, bounds, and error types that obscure each operation. Generalize when variation is stable and substitution is meaningful.

### A trait names substitutable behavior

```rust
trait Summary {
    fn summary(&self) -> String;
}
```

The syntax is easy. The design question is whether different types can satisfy one meaningful contract and whether generic code benefits from treating them uniformly.

```rust
fn print_summary(item: &impl Summary) {
    println!("{}", item.summary());
}
```

A trait named after one implementation or one call site is often a disguised helper function.

### Required methods and provided methods

```rust
trait Identified {
    type Id;

    fn id(&self) -> &Self::Id;

    fn same_id(&self, other: &Self) -> bool
    where
        Self::Id: PartialEq,
    {
        self.id() == other.id()
    }
}
```

Associated types are introduced only at this basic level: one implementation chooses one `Id` type. Deeper associated-type design belongs to Course 3.

A default method should follow from the required contract. It should not guess domain policy that implementers may need to undo.

### Coherence and the orphan rule

An implementation is permitted when the trait or the type is local to your crate. You cannot generally implement a foreign trait for a foreign type:

```rust,compile_fail
impl std::fmt::Display for Vec<String> {
    // both Display and Vec are foreign
}
```

Use a newtype when you own the semantic wrapper:

```rust
struct Titles(Vec<String>);

impl std::fmt::Display for Titles {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{} titles", self.0.len())
    }
}
```

The rule prevents competing crates from defining incompatible implementations for the same pair.

### Blanket implementations

A generic implementation can cover many types:

```rust
trait Empty {
    fn is_empty(&self) -> bool;
}

impl<T> Empty for Vec<T> {
    fn is_empty(&self) -> bool {
        Vec::is_empty(self)
    }
}
```

Broad implementations consume coherence space. Once a blanket implementation applies, a more specific overlapping implementation is not allowed on stable Rust. Keep implementations as broad as the contract warrants, not broader.

### Derive versus manual implementation

Deriving `Debug`, `Clone`, `PartialEq`, `Eq`, `PartialOrd`, `Ord`, or `Hash` asks the compiler to implement fieldwise behavior. That behavior must match domain meaning.

For `TaskId(u64)`, derived ordering is sensible. For a user record, deriving `Ord` may accidentally define ordering by field declaration order even when no domain order exists. Do not derive traits merely because they are available.

### Trait laws are partly social contracts

The compiler checks method types, not all semantics. `Eq` and `Ord` users expect coherent equality and total ordering. `From` users expect infallibility. `Display` users expect stable human-facing representation. Document and test laws that the type system cannot prove.

### Traits and architecture

In this course, prefer standard traits at boundaries:

- `FromStr` for typed text parsing;
- `Display` for user-facing formatting;
- `From` or `TryFrom` for conversions;
- `BufRead` and `Write` for codecs.

A custom repository trait for `TaskBoard` is not justified when only one in-memory implementation exists and no test substitute is needed.

### Bounds grant operations

```rust
fn render_twice<T: std::fmt::Display>(value: T) -> String {
    format!("{value} | {value}")
}
```

`Display` permits formatting. If the body also needs cloning, add `Clone`; do not add `Debug`, `Eq`, or `'static` defensively.

Multiple bounds can use `+`:

```rust
fn ordered_label<T>(left: &T, right: &T) -> String
where
    T: Ord + std::fmt::Display,
{
    let selected = if left <= right { left } else { right };
    selected.to_string()
}
```

`where` clauses are preferred when inline bounds obscure the signature or involve multiple related types.

### Bounds on implementations versus methods

```rust
struct Bag<T> {
    values: Vec<T>,
}

impl<T> Bag<T> {
    fn len(&self) -> usize {
        self.values.len()
    }
}

impl<T: PartialEq> Bag<T> {
    fn contains(&self, target: &T) -> bool {
        self.values.contains(target)
    }
}
```

Do not put `T: PartialEq` on the struct unless every valid `Bag<T>` operation requires it. Overconstraining types prevents useful construction and propagates bounds unnecessarily.

### `impl Trait` in argument position

```rust
fn announce(value: &impl std::fmt::Display) {
    println!("{value}");
}
```

This is convenient syntax for an anonymous generic parameter in many ordinary cases. Each argument position written with a separate `impl Trait` may be a different type:

```rust
fn pair(left: impl Display, right: impl Display) { /* ... */ }
```

If both arguments must share one concrete type, use a named parameter:

```rust
fn same_type<T: Display>(left: T, right: T) { /* ... */ }
```

### `impl Trait` in return position

```rust
fn task_ids(tasks: &[Task]) -> impl Iterator<Item = TaskId> + '_ {
    tasks.iter().map(Task::id)
}
```

The caller knows the trait contract but not the concrete iterator type. One function body must return one concrete hidden type across all branches:

```rust,compile_fail
fn numbers(flag: bool) -> impl Iterator<Item = u64> {
    if flag {
        vec![1, 2].into_iter()
    } else {
        std::iter::once(3)
    }
}
```

These branch types differ. Dynamic trait objects are one possible later tool, but for Course 1 prefer restructuring, collecting to one concrete type, or returning an enum of domain alternatives.

### Bounds and ownership

A bound does not imply ownership. Compare:

```rust
fn display_ref<T: Display + ?Sized>(value: &T) { /* ... */ }
fn display_owned<T: Display>(value: T) { /* ... */ }
```

The first borrows and admits dynamically sized types through `?Sized`; the second consumes. `?Sized` is introduced here only to read common signatures such as `AsRef<T: ?Sized>`. Advanced dynamically sized type reasoning belongs later.

### Avoid bound accumulation

When compiler errors produce a chain of requested bounds, inspect the body. A call to `sort` may require `Ord`; cloning inside a closure may be unnecessary; formatting for debugging may not belong in the generic algorithm. Remove accidental operations before expanding the public contract.

### `Display` is user-facing representation

Implement `Display` when a type has a natural human-readable form:

```rust
use std::fmt;

impl fmt::Display for Priority {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        let text = match self {
            Self::Low => "low",
            Self::Normal => "normal",
            Self::High => "high",
        };
        f.write_str(text)
    }
}
```

`Debug` supports developer inspection and can include type/field detail. Do not use `Debug` output as a persistence format; derived representation can change when fields change.

### `FromStr` creates typed parsing at the leaf

```rust
use std::str::FromStr;

impl FromStr for Priority {
    type Err = ParsePriorityError;

    fn from_str(text: &str) -> Result<Self, Self::Err> {
        match text {
            "low" => Ok(Self::Low),
            "normal" => Ok(Self::Normal),
            "high" => Ok(Self::High),
            _ => Err(ParsePriorityError {
                value: text.to_owned(),
            }),
        }
    }
}
```

Now command and storage parsers share one spelling contract:

```rust
let priority = token.parse::<Priority>()?;
```

Context such as field or line still belongs in the surrounding parser.

### `From` means infallible conversion

```rust
impl From<DomainError> for AppError {
    fn from(value: DomainError) -> Self {
        Self::Domain(value)
    }
}
```

The conversion always succeeds and loses no required information. The standard library provides `Into` automatically in the opposite calling direction when `From` exists; normally implement `From`, not both.

### `TryFrom` means validation can fail

```rust
impl TryFrom<u64> for TaskId {
    type Error = ZeroTaskId;

    fn try_from(value: u64) -> Result<Self, Self::Error> {
        if value == 0 {
            Err(ZeroTaskId)
        } else {
            Ok(Self(value))
        }
    }
}
```

Use `TryFrom` when the source domain includes values the target rejects. Do not implement `From<u64>` and panic on zero; that violates the infallible contract.

### `AsRef` at ergonomic outer boundaries

```rust
fn load(path: impl AsRef<Path>) -> Result<TaskBoard, StorageError> {
    let path = path.as_ref();
    // ...
}
```

This accepts `&Path`, `PathBuf`, `&str`, and `String` where implementations exist. It can be useful for a public convenience function. Internal helpers should often accept `&Path` directly to simplify types and diagnostics.

`AsRef` is a cheap borrowed conversion contract, not a general-purpose parser.

### `Default` must represent a meaningful default

`TaskBoard::default()` can sensibly be an empty board with next ID 1. A `Task` may have no meaningful default title or identity, so deriving `Default` would create invalid or arbitrary values.

### Formatting and persistence remain separate

Even when enum `Display` spelling matches storage today, keep file encoding explicit enough to review version compatibility. Human messages may evolve independently of stored bytes. For tiny closed enums, calling `Display` inside a version-specific encoder can be acceptable when the compatibility contract documents that spelling.

### Depend on the operation, not the device

A codec needs lines or bytes; it does not need a filesystem path. Express the narrow capability:

```rust
fn load_from<R: BufRead>(reader: R) -> Result<TaskBoard, StorageError>;

fn save_to<W: Write>(
    writer: &mut W,
    board: &TaskBoard,
) -> Result<(), StorageError>;
```

The path wrapper remains concrete because it owns path policy, temporary files, and error context.

### Why `BufRead` rather than `Read`

`Read` provides bytes. `BufRead` adds methods such as `read_line`, `lines`, and `fill_buf`. A line grammar directly depends on buffered line access, so `BufRead` is the honest bound.

Accepting a broader trait is not always more general in a useful way. If the body immediately wraps any `Read` in `BufReader`, that can be valid, but it changes ownership and buffering policy. Select the bound from the algorithm.

### Generic references also implement traits

If `W: Write`, then `&mut W` can be passed to helpers requiring `Write` because suitable reference implementations exist:

```rust
fn write_task<W: Write>(writer: &mut W, task: &Task) -> io::Result<()> {
    writeln!(writer, "{}", task.title())
}

fn write_all<W: Write>(writer: &mut W, tasks: &[Task]) -> io::Result<()> {
    for task in tasks {
        write_task(writer, task)?;
    }
    Ok(())
}
```

Reborrowing prevents consumption of the caller's writer.

### Test substitutes are ordinary values

```rust
let input = b"TASKBOARD-V1\nNEXT_ID\t1\n";
let board = load_from(std::io::BufReader::new(&input[..]))?;

let mut output = Vec::new();
save_to(&mut output, &board)?;
assert_eq!(output, input);
```

No mocking framework is required. The trait boundary admits in-memory standard-library types.

### Avoid a universal repository trait

It can be tempting to define:

```rust
trait Repository {
    fn load(&self) -> Result<TaskBoard, Error>;
    fn save(&self, board: &TaskBoard) -> Result<(), Error>;
}
```

For this capstone, there is one local-file policy and no runtime substitution requirement. The trait adds indirection, error design, and lifecycle questions without current value. Generic codec traits already provide the test seam needed.

Course 3 will examine architectural traits when multiple implementations and substitution contracts are real.

### Bound location and diagnostics

A named helper can simplify errors and signatures:

```rust
fn decode<R>(reader: R) -> Result<TaskBoard, StorageError>
where
    R: BufRead,
{
    // ...
}
```

Do not leak internal generic parameters into public API when a concrete wrapper is all callers need. Public `load(&Path)` plus crate-private `load_from<R: BufRead>` is a valid design.

### Every reference has a lifetime

Most lifetimes are inferred:

```rust
fn title(task: &Task) -> &str {
    task.title()
}
```

The output borrow is tied to the input task borrow. Written explicitly:

```rust
fn title<'a>(task: &'a Task) -> &'a str {
    task.title()
}
```

The annotation does not extend the task's life. It states that any returned reference cannot outlive the borrowed task.

### Elision rules for function signatures

For foundational reasoning, remember:

1. each elided input reference gets its own lifetime parameter;
2. if exactly one input lifetime exists, it is assigned to all elided output references;
3. for methods, if `&self` or `&mut self` exists, its lifetime is assigned to elided output references.

These rules explain common signatures but do not replace borrow checking of the body.

### Multiple sources require a stated relationship

```rust,compile_fail
fn longer(left: &str, right: &str) -> &str {
    if left.len() >= right.len() { left } else { right }
}
```

The output may come from either input. State one shared lifetime:

```rust
fn longer<'a>(left: &'a str, right: &'a str) -> &'a str {
    if left.len() >= right.len() { left } else { right }
}
```

At a call site, the usable output lifetime is constrained by the shorter overlapping borrow because the function may return either.

### Separate lifetimes when only one source is returned

```rust
fn prefer_left<'a, 'b>(left: &'a str, _right: &'b str) -> &'a str {
    left
}
```

Using one `'a` for both inputs would unnecessarily couple the output to `right`. Lifetimes are part of API precision.

### Lifetimes cannot repair dangling data

```rust,compile_fail
fn generated<'a>() -> &'a str {
    let text = String::from("generated");
    &text
}
```

No caller-owned storage exists. Return `String`:

```rust
fn generated() -> String {
    String::from("generated")
}
```

When a function creates data, ownership is usually the correct return contract.

### Method elision

```rust
impl TaskBoard {
    fn find(&self, id: TaskId) -> Option<&Task> {
        self.tasks.iter().find(|task| task.id() == id)
    }
}
```

The returned task reference is tied to `&self`. It cannot survive board mutation requiring exclusive access.

### `'static` has two common meanings

A `&'static str` points to data valid for the entire program, commonly a string literal. A bound `T: 'static` means `T` contains no non-static borrowed references; it does not mean the value itself is kept forever.

This course uses `&'static str` for fixed field names and command names in error variants. Do not use `'static` to silence local lifetime errors.

### A struct can borrow data

```rust
struct TaskView<'a> {
    id: TaskId,
    title: &'a str,
}
```

A `TaskView` cannot outlive the task title it references. This can avoid allocation for a short-lived projection, but it propagates lifetime relationships into every owner of `TaskView`.

### Borrowed views are best at local boundaries

A rendering function can create views and consume them immediately:

```rust
fn views(tasks: &[Task]) -> Vec<TaskView<'_>> {
    tasks
        .iter()
        .map(|task| TaskView {
            id: task.id(),
            title: task.title(),
        })
        .collect()
}
```

The vector owns view records, not title bytes. The original task slice must remain alive and unmutated in conflicting ways while the views are used.

### Owning small output often simplifies architecture

If a report must outlive the board, cross threads later, enter a cache, or survive mutation, owning strings may be the right contract:

```rust
struct TaskReportRow {
    id: TaskId,
    title: String,
}
```

One bounded allocation can be cheaper than infecting several layers with lifetime coupling and restrictive borrow scopes. “Zero allocation” is not automatically superior design.

### Do not store self-references

A struct that owns a `String` and stores a slice into that same string is not an ordinary safe self-referential design. Moving the struct could invalidate internal assumptions, and construction cannot easily express the borrow from a field into the containing value.

For foundational code, store indexes/ranges, recompute slices on demand, or split ownership into a separate longer-lived owner. Pinning and advanced self-referential techniques are deliberately outside this course.

### Lifetime parameters express dependency direction

```rust
struct Parser<'a> {
    input: &'a str,
    offset: usize,
}
```

The parser depends on caller-owned input. The caller does not depend on the parser. This is appropriate for a short-lived cursor.

By contrast, persistent domain entities should usually own their names and titles because they are the authoritative state.

### API ownership audit

For every reference-bearing return or struct, ask:

1. Who owns the bytes?
2. How long must the output remain usable?
3. Will the owner need mutation while output exists?
4. Is allocation bounded and acceptable?
5. Does borrowing make invalid states impossible or merely make signatures complex?
6. Can a slice or iterator avoid materializing a struct entirely?

### Capstone decisions

- `Task` owns `String` because the board is authoritative persistent state.
- `Task::title` returns `&str` because callers need a view.
- `TaskBoard::find` returns `Option<&Task>` tied to the board.
- rendered output owns `String` because it leaves the borrow scope and is written later.
- errors own bounded invalid tokens and paths because they may propagate beyond input buffers.
- storage parsing borrows line fields only during one decode call, then constructs owned domain values.

### Model checkpoint

Before the complete-program example, verify that the model can decide a design rather than merely name its mechanism.

1. **Outcome 1.** For write generic functions and types whose bounds correspond to operations actually performed, construct one positive and one causal negative example. Mark the first decisive fact in the **trait and lifetime contract** and state which evidence could falsify the claim.

2. **Outcome 2.** For define and implement small traits as behavioral contracts without abstraction theater, construct one positive and one causal negative example. Mark the first decisive fact in the **trait and lifetime contract** and state which evidence could falsify the claim.

3. **Outcome 3.** For use Display, Error, From, FromStr, Read, BufRead, and Write at natural boundaries, construct one positive and one causal negative example. Mark the first decisive fact in the **trait and lifetime contract** and state which evidence could falsify the claim.

4. **Outcome 4.** For derive ordinary lifetime annotations from input-output provenance and distinguish annotation from lifetime extension, construct one positive and one causal negative example. Mark the first decisive fact in the **trait and lifetime contract** and state which evidence could falsify the claim.

5. **Preservation.** Name one earlier invariant that an easier but less precise implementation could regress.

6. **Boundary.** State one claim this module can justify and one adjacent claim that requires a later course, platform contract, peer behavior, or measurement.

A strong answer records state before and after the operation, the failure path, and the public consequence. An API name by itself is not a model.

## Use the idea in a complete program

The course capstone is **Taskboard**, a persistent command-line task board. Use standard conversion traits and generic readers and writers where they remove real duplication. Add only the lifetime annotations required by returned borrowed data. The exact implementation task is in the [workbook](workbook.md); the full product contract is in the [capstone guide](../capstone.md).

## Practice sequence

1. Reproduce the important examples from this chapter without copying them line for line.
2. Complete the prediction and repair sections in the [workbook](workbook.md).
3. Build the independent [laboratory](../../labs/module-08-traits-and-lifetimes/README.md).
4. Apply the capstone increment.
5. Open the [reasoned solutions](solutions.md) only after recording your own answer.

## Ready to continue

You are ready for Module 9 when you can:

- answer the module question—“What behavior is genuinely shared, what constraints make it valid, and what borrow relationship must a signature expose?”—without reading the chapter;
- demonstrate this outcome on a fresh example: Write generic functions and types whose bounds correspond to operations actually performed;
- repair the debugging case while preserving its product requirement;
- complete the laboratory transfer variant and explain the decisive design choice;
- name a simpler alternative and the condition under which you would prefer it.

## Primary Rust references

This chapter is self-contained. These official sources are included for verification and future language updates, not as required reading:

- [The Rust Book: Generics, Traits, and Lifetimes](https://doc.rust-lang.org/book/ch10-00-generics.html)
- [Rust Reference: Trait bounds](https://doc.rust-lang.org/reference/trait-bounds.html)

[← Module 7](../module-07-errors-parsing-files-and-persistence/index.md) · [one-hundred-module map](../../../COURSE_MAP.md) · [Module 9 →](../module-09-crates-modules-public-apis-tests-and-documentation/index.md)

## Continue

Continue to [Module 9 — Crates, Modules, Public APIs, Tests, and Documentation](../module-09-crates-modules-public-apis-tests-and-documentation/index.md) after completing the workbook, independent laboratory, capstone increment, and closed-book explanation for this module.
