# 09 — Crates, Modules, Public APIs, Tests, and Documentation

**Course 1, day 9 · Module 9 of 60**  
`███░░░░░░░░░░░░░░░░░` **9/60**

[← Module 8: Generics, Traits, Conversions, and Lifetime Basics](../module-08-generics-traits-conversions-and-lifetime-basics/index.md) · [Course 1 overview](../index.md) · [Sixty-module map](../../../COURSE_MAP.md) · [Module 10: Integration and Independent Change →](../module-10-integration-and-independent-change/index.md)

## The question

> Which surfaces are product contracts, which are implementation details, and what independent evidence protects each boundary?

## Why this comes now

A program that works in one file is not yet a maintainable product. Modules, visibility, library boundaries, tests, documentation, and Cargo now turn local correctness into an explicit public contract. This module prepares you to integrate rather than merely accumulate features.

## What you will be able to do

- Distinguish package, crate, target, and module while organizing code by responsibility rather than one file per type.
- Design private representation and a minimal public API that preserves invariants.
- Choose unit, integration, process, fixture, and documentation tests from the contract under proof.
- Write rustdoc examples that teach and execute, and maintain a deliberate warning/lint policy.
- Separate a thin effectful binary shell from a testable library core.

## Core model

### Why this module exists

A working function is not yet a maintainable product. The package must expose a deliberate public contract, hide representations that carry invariants, separate effects from logic, and provide independent evidence at the right boundaries. Rust's module system and Cargo targets make these decisions explicit.

### Package, crate, target, module

A package is described by one manifest. A target becomes a crate when compiled. Modules organize names/privacy within a crate. Splitting every type into its own file usually fragments responsibility; a module should own a coherent concept such as command parsing, domain state, storage, or application orchestration.

### Privacy is invariant protection

Items are private by default. Marking a struct field `pub` is a permanent promise that callers may construct and mutate it directly. If a field participates in an invariant, keep it private and expose a constructor or method with the exact capability required.

Use `pub(crate)` for internal collaboration only when the crate boundary is meaningful. Do not widen visibility merely to make a test compile. Unit tests can access private items within their module hierarchy; integration tests should exercise the public API.

### Library core and effect shell

A command-line binary should usually:

1. read environment/arguments;
2. call a library function;
3. render output/error;
4. choose an exit code.

Domain decisions, parsing, state transitions, and codecs belong in testable library modules. This is not absolute—small binaries can remain small—but the capstone is large enough to benefit from the separation.

### Choose the test by the contract

- unit test: local invariant or private helper behavior;
- integration test: public library contract from an external crate perspective;
- process/CLI test: arguments, environment, stdout/stderr, exit code, and filesystem interaction;
- documentation test: public example remains compilable and teaches the intended route;
- fixture test: compatibility with representative valid/hostile inputs.

Testing a private helper does not prove the CLI. Running the CLI once does not prove parser edge cases.

### Documentation is executable design

A public item should document:

- what it does;
- valid inputs and output;
- failure and panic behavior;
- ownership/borrowing implications when non-obvious;
- examples;
- platform or representation limitations where relevant.

Rustdoc examples can compile and run as tests. `compile_fail` examples can prove that a prohibited use is rejected, but the harness must ensure it fails for the intended reason.

### Tooling policy

`rustfmt` provides consistent formatting, not correctness. Clippy reports lints under a selected policy; not every lint is universally appropriate. Warnings denied in CI prevent drift but require deliberate lint configuration and documented exceptions. `Cargo.lock` policy depends on whether the package is an application or library; the course repositories keep reproducible workspace builds while later publishing guidance may differ.

### Worked architecture: taskboard

A restrained structure:

```text
src/
├── lib.rs       public re-exports and crate documentation
├── model.rs     task types and invariants
├── command.rs   raw tokens → typed command
├── storage.rs   board ↔ versioned text
├── app.rs       execute command and coordinate save
└── main.rs      environment, output, exit status
```

Each module owns a conversion boundary. `main` should not inspect task fields or parse records. `storage` should not decide CLI exit codes. `model` should not open files.

### Try without the scaffold

Given a one-file inventory CLI, mark every function as domain, parsing, persistence, orchestration, or effect shell. Propose the smallest module split that creates testable boundaries. List which items must be public and why.

### Misconception clinic

- **“More modules mean cleaner architecture.”** Excess files can hide the data flow.
- **“Tests require public fields.”** That destroys the invariant boundary; test through appropriate scopes/APIs.
- **“Clippy clean means idiomatic.”** Lints are evidence and suggestions, not an architecture oracle.
- **“Unit tests prove the product.”** Each external boundary needs its own evidence.

### The terms are not interchangeable

A **package** is the Cargo unit described by one `Cargo.toml`. It can contain one library crate and multiple binary targets, examples, tests, and benchmarks.

A **crate** is one compilation unit with one crate root. `src/lib.rs` is the conventional library crate root; `src/main.rs` is the conventional default binary crate root.

A **target** is something Cargo builds: library, binary, integration test, example, and more.

A **module** is a namespace and privacy boundary inside a crate. Modules are declared with `mod` and can live inline or in files.

A **path** identifies an item, such as `crate::model::Task` or `super::parse_id`.

Confusing these levels leads to statements such as “put each class in a crate” or “the file is public.” Rust visibility applies to items and modules, while files are one source organization mechanism.

### One package, two main crates

The capstone package contains:

```text
src/
├── lib.rs      # taskboard library crate root
└── main.rs     # taskboard binary crate root
```

Even though both live in one package, the binary refers to the library through the crate name:

```rust
fn main() {
    if let Err(error) = taskboard::run_from_env() {
        // outer process policy
    }
}
```

The binary is a downstream user of the library's public API. That pressure helps reveal whether the API is coherent.

### Declaring modules

In `lib.rs`:

```rust
mod app;
mod command;
mod model;
mod storage;

pub use app::{run, AppError, Outcome};
pub use command::{parse_command, Command, CommandError};
pub use model::{Priority, Status, Task, TaskBoard, TaskId};
```

`mod model;` includes `model.rs` as a module. It does not make the module or its items public. `pub use` re-exports selected items at the crate root.

### Absolute and relative paths

Prefer paths that communicate architectural position:

- `crate::model::Task` starts from the current crate;
- `super::RecordError` starts from the parent module;
- `self::helper` starts from the current module;
- `std::path::Path` starts from an external crate name.

Long import lists can use `use`, but do not import so aggressively that the origin of generic names becomes unclear.

### Files do not define architecture alone

A 1,500-line module may hide several responsibilities; ten 30-line modules may fragment one responsibility. Split when there is a stable boundary involving:

- invariant ownership;
- dependency direction;
- test scope;
- public visibility;
- change reasons.

The capstone's five source modules are a ceiling, not a command to create an identical layout for every small program.

### Module tree and dependency direction

A healthy dependency graph avoids cycles in responsibility:

```text
model      <- command
model      <- storage
model      <- app
command    <- app
storage    <- app
app        <- lib public facade
lib facade <- binary
```

The model should not import command-line or filesystem concerns. Storage may depend on model restoration APIs; the model should not know its file format.

### Private by default protects invariants

Rust items are private unless marked public. Private fields force construction and mutation through reviewed operations:

```rust
pub struct Task {
    id: TaskId,
    title: String,
    priority: Priority,
    status: Status,
}
```

External code can inspect through borrowing accessors and change state through domain methods. It cannot create a zero ID, insert a title containing the storage delimiter, or assign an arbitrary status field if constructors prevent those states.

### `pub` means reachable only through public ancestors

Making an item `pub` inside a private module does not automatically expose it outside the crate. Every path segment must be visible, or the item must be re-exported through a visible path.

This permits internal organization without forcing callers to know it:

```rust
mod model;
pub use model::{Task, TaskBoard, TaskId};
```

Callers use `taskboard::Task`, even if the implementation later splits `model.rs`.

### Restricted visibility

`pub(crate)` exposes an item anywhere in the current crate but not to downstream crates. `pub(super)` exposes it to the parent module. Use restricted visibility when multiple internal modules need a capability that is not part of the library contract.

For example, `Task::restore` may be `pub(crate)` so storage can reconstruct validated state without letting downstream users bypass normal creation policy.

### Constructors, accessors, and invariants

A public constructor should establish every invariant required by all methods:

```rust
impl Task {
    pub fn new(id: TaskId, title: String, priority: Priority) -> Result<Self, TaskError> {
        validate_title(&title)?;
        Ok(Self { id, title, priority, status: Status::Todo })
    }

    pub fn title(&self) -> &str {
        &self.title
    }
}
```

Do not expose mutable field references when arbitrary mutation could break validation. A `title_mut(&mut self) -> &mut String` would let callers insert tabs after construction. Provide a validated `rename` method instead.

### Re-export a product vocabulary

A good crate root presents domain concepts and primary operations, not all helpers. Internal modules can contain parsers, record structs, temporary paths, and rendering details.

Audit each public item:

1. Which downstream use requires it?
2. What invariant does it expose or preserve?
3. Is its name stable enough for a contract?
4. Could a narrower type or visibility suffice?
5. Is documentation complete?

### Public enums and evolution

A public exhaustive enum invites downstream `match` expressions. Adding a variant can break those matches. For a closed foundational application where library and binary evolve together, explicit enums are appropriate. A long-lived general library may use other evolution strategies, but hiding every variant also reduces usefulness. The decision is contractual, not automatic.

### Tests must not dictate unsafe visibility

If integration tests need to construct a task, expose a valid public constructor or test through commands. Do not mark fields public only for tests. Unit tests inside the defining module can inspect private representation where representation-specific evidence is genuinely needed.

### Keep process policy at the edge

The binary knows:

- command-line arguments;
- environment variables;
- current working directory;
- stdin/stdout/stderr;
- process exit status.

The domain should know none of these. A thin `main` makes the rest testable as ordinary Rust:

```rust
fn main() {
    let exit = match taskboard::run_from_env() {
        Ok(output) => {
            print!("{output}");
            std::process::ExitCode::SUCCESS
        }
        Err(error) => {
            eprintln!("error: {error}");
            std::process::ExitCode::FAILURE
        }
    };
    std::process::exit(exit.code().unwrap_or(1));
}
```

The exact process API can differ; the principle is that domain functions do not terminate the process.

### Functional core, imperative shell

A useful decomposition:

- parse tokens into `Command`;
- load a validated `TaskBoard`;
- apply a command to the board;
- decide whether state changed;
- persist changed state;
- render an owned outcome;
- let the binary write it.

The core can mutate in-memory state; “functional core” here means deterministic logic with explicit inputs and outputs, not a requirement for purely immutable code.

### Make effects injectable at narrow seams

Generic `BufRead`/`Write` functions provide codec seams. Application logic can also accept a path rather than reading an environment variable itself:

```rust
pub fn run(path: &Path, args: impl IntoIterator<Item = String>)
    -> Result<String, AppError>;
```

A convenience `run_from_env` may adapt real process inputs, but the core route remains directly callable.

### Model mutation outcomes explicitly

The application needs to know whether to save:

```rust
enum Execution {
    ReadOnly(String),
    Changed(String),
}
```

This is stronger than comparing boards after every command or always rewriting. A command executor can return an outcome carrying both rendered data and change status.

### Output failure is still an effect

Returning a `String` is simple for bounded output. Streaming large results through `Write` avoids a large allocation but introduces write failures into the application signature. The capstone's local board permits owned output. State that bound; do not claim it scales without limit.

### Avoid hidden global configuration

A library function that reads `TASKBOARD_FILE` internally is harder to test and reuse. Resolve environment configuration in the outer adapter and pass a `Path`. Defaults should be explicit and testable.

### Dependency direction

The binary depends on the library. The library must not import items from `main.rs`. Domain modules must not depend on application orchestration. If a lower layer needs to call upward, re-examine responsibility or pass a small value/function downward.

### Tests answer different questions

#### Unit tests

Unit tests live near implementation and can access private items through a child test module:

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn title_rejects_tabs() {
        assert!(matches!(
            validate_title("bad\ttitle"),
            Err(TitleError::ForbiddenCharacter)
        ));
    }
}
```

Use them for dense invariant matrices, pure parsers, state transitions, and edge cases.

#### Integration tests

Files in `tests/` compile as separate crates and use only public API. They prove that external callers can construct valid values and complete workflows.

```rust
use taskboard::{Priority, TaskBoard};

#[test]
fn add_then_complete_is_visible_through_public_api() {
    let mut board = TaskBoard::new();
    let id = board.add("Ship course".into(), Priority::High).unwrap();
    board.complete(id).unwrap();
    assert_eq!(board.find(id).unwrap().status().to_string(), "done");
}
```

#### Documentation tests

Rust code blocks in API documentation are compiled and, by default, run. They prove that examples match the public interface.

#### CLI tests

Command-line tests launch the built binary, configure an isolated storage path, provide arguments, and inspect exit status, stdout, stderr, and file effects. They test process behavior—not every domain branch.

### Test behavior, not helper sequence

A brittle test asserts that `parse_record`, then `insert_raw`, then `sort_internal` were called in a particular order. A robust test supplies bytes and observes the returned valid board or exact error.

Refactoring private algorithms should not require rewriting public-contract tests.

### Test matrices

For finite enums and state transitions, enumerate the full matrix. For parsers, test every grammar position and boundary length. For storage, combine exact fixtures, round trips, and corruption cases. Round trips alone can let an encoder and decoder share the same bug.

### Test failure state

Tests should inspect what did not change:

- invalid transition leaves status unchanged;
- failed import leaves destination unchanged;
- failed command does not rewrite storage;
- malformed file does not become an empty board;
- read-only command leaves canonical bytes unchanged.

### Isolated filesystem tests

Without external crates, create a unique directory under `std::env::temp_dir` using process ID plus a time/counter component, create it with `create_dir`, and remove it after the test. Use an RAII helper whose `Drop` attempts cleanup.

Do not share one fixed path across parallel tests. Do not depend on the developer's home directory.

### Avoid sleep-based assertions

File modification timestamps may have coarse resolution. Prefer byte comparison or operation seams over sleeping and checking timestamps. Test portable observable behavior.

### Test naming

Names should encode condition and expected result:

```text
load_rejects_duplicate_task_id_on_physical_line_four
complete_preserves_todo_state_when_id_is_unknown
cli_add_persists_only_after_success
```

A name such as `test_task_2` carries no contract.

### Public documentation is part of the API

A useful item-level document states:

- what the item represents;
- invariants;
- ownership or borrowing behavior;
- errors;
- panics, if any;
- side effects;
- examples;
- complexity when material.

Do not repeat the signature in prose. Explain the contract the signature cannot fully encode.

```rust
/// Adds a task in the `Todo` state and returns its newly allocated ID.
///
/// The title is trimmed and must contain 1–120 bytes. Tabs and line breaks
/// are rejected because the version-1 storage format uses them as delimiters.
///
/// # Errors
///
/// Returns [`DomainError::InvalidTitle`] when validation fails and
/// [`DomainError::IdExhausted`] when no further positive ID can be allocated.
///
/// # Examples
///
/// ```
/// use taskboard::{Priority, Status, TaskBoard};
///
/// let mut board = TaskBoard::new();
/// let id = board.add("Write docs".into(), Priority::Normal)?;
/// assert_eq!(board.find(id).map(|task| task.status()), Some(Status::Todo));
/// # Ok::<(), taskboard::DomainError>(())
/// ```
pub fn add(/* ... */) { /* ... */ }
```

The hidden `#` line appears to rustdoc but is omitted from rendered presentation; use it sparingly to make examples complete.

### Link related types

Intra-doc links such as ``[`TaskBoard`]`` and ``[`DomainError::InvalidTitle`]`` are checked by rustdoc when resolvable. They reduce stale manual paths.

### Crate-level documentation

`//!` comments at the top of `lib.rs` should provide:

- purpose;
- architecture overview;
- shortest useful example;
- error philosophy;
- storage compatibility boundary;
- links to primary types.

The README can address installation and course use; API docs address library callers.

### Examples should be minimal but real

A doc example that only constructs an empty value proves little. Show one meaningful operation and assertion. Do not include massive setup that hides the API. Move complex workflows to integration tests and link them conceptually.

### Compile-fail examples

Rustdoc can assert that code should fail to compile:

```rust
/// ```compile_fail
/// use taskboard::TaskId;
/// let id = TaskId::new_unchecked(0); // not a public operation
/// ```
```

Use compile-fail examples for important static guarantees, but avoid depending on exact compiler message text.

### Documentation drift is a test failure

Run:

```bash
cargo test --doc
cargo doc --no-deps
```

Broken examples and unresolved links should fail the proof route where feasible. Warnings in documentation deserve the same review as code warnings.

### The manifest is executable configuration

`Cargo.toml` identifies package metadata, targets, dependencies, features, profiles, and lint policy. Keep declarations minimal and reviewable.

```toml
[package]
name = "taskboard"
version = "0.1.0"
edition = "2024"
rust-version = "1.97.1"
publish = false

[lints]
workspace = true
```

The package `rust-version` states the minimum supported compiler for that package. The pinned `rust-toolchain.toml` selects the course's reproducible toolchain. They serve related but different roles.

### Target discovery

Cargo conventionally discovers:

- `src/lib.rs` as a library;
- `src/main.rs` as the default binary;
- `src/bin/*.rs` as additional binaries;
- `tests/*.rs` as integration-test crates;
- `examples/*.rs` as examples;
- `benches/*.rs` as benchmarks.

Explicit `[[bin]]` or `[lib]` sections are useful when names or paths differ from conventions, not mandatory ceremony.

### Lockfiles

`Cargo.lock` records exact resolved dependency versions. Applications and workspaces should commit it for reproducible builds. Published libraries do not use the library's lockfile to constrain downstream resolution, but keeping a workspace lockfile still gives maintainers reproducible local and CI testing.

This course has no third-party runtime dependencies, yet Cargo may still produce a lockfile. Retain it in the course artifact once generated by the pinned toolchain.

### Dependency discipline

Before adding a crate, answer:

1. What capability is missing from `std` or current dependencies?
2. What correctness/security burden does the crate remove?
3. What transitive graph and feature set does it introduce?
4. Is its minimum supported Rust version compatible?
5. Who maintains it and how will updates be reviewed?
6. Does it hide a mechanism this course intends to teach?

For Course 1, manual command and storage parsing are intentional. Later production work can evaluate established ecosystem crates.

### Features are conditional compilation contracts

Features can enable optional dependencies or code paths. They are additive by convention and can interact in combinations. This capstone needs no features; adding `cli`, `storage`, and `testing` flags would create untested build matrices without product need.

Understand features now so you can read manifests, but design them in later courses when optional capability is real.

### Profiles

Cargo's development and release profiles choose optimization and debug behavior. Avoid course-specific profile tuning without measurement. Correctness tests should run in ordinary test profile; a final release build proves optimized compilation but not performance quality.

### Workspace

The course root workspace aggregates the capstone, diagnostics, reference solutions, and lab solutions under one lockfile and proof command. Starter crates can remain excluded when they are intentionally reader-modifiable.

### One proof route, several tools

Each tool answers a different question:

```bash
cargo fmt --all -- --check
cargo check --workspace --all-targets
cargo clippy --workspace --all-targets -- -D warnings
cargo test --workspace --all-targets
cargo test --workspace --doc
cargo doc --workspace --no-deps
cargo build --workspace --release
```

- rustfmt: does source conform to deterministic formatting?
- `check`: do all targets type-check quickly?
- Clippy: do reviewed lint rules identify likely mistakes or unidiomatic constructs?
- tests: does executable behavior satisfy assertions?
- doc tests/docs: do examples and API documentation remain valid?
- release build: does optimized compilation succeed?

Passing one is not a substitute for the rest.

### Warnings as failures

`-D warnings` prevents warning accumulation and makes local/CI expectations explicit. It can also make compiler upgrades reveal new lints. Because the course pins a toolchain, the warning set is reproducible until the course deliberately updates.

When updating the toolchain, review new warnings. Do not suppress them globally to preserve a green badge.

### Clippy groups

The workspace deliberately selects lint groups by the kind of evidence they provide:

- `correctness` and `suspicious` are denied because they identify constructs that are probably wrong or misleading;
- `complexity` and `perf` begin as warnings so `cargo clippy ... -- -D warnings` still makes them proof failures;
- `dbg_macro`, `todo`, and `unimplemented` are denied because published solution code must not contain debugging residue or unfinished execution paths.

The course does not blanket-enable `clippy::all` or `clippy::pedantic`. Many style-oriented lints are valuable during review, but turning every current opinion into a permanent public contract makes toolchain upgrades noisy and can reward mechanical rewrites over clear design. Add a lint when it protects a named invariant, then document any exception.

Never enable the entire `restriction` group. Restriction lints are policy choices, can conflict with one another, and should be selected individually for a project's actual constraints.

### Local allowances

A local `#[allow(...)]` can be correct when:

- the lint conflicts with a deliberate API contract;
- a test intentionally demonstrates a pattern;
- the alternative reduces clarity or changes semantics;
- the rationale is documented adjacent to the allowance.

An allowance without reason is debt. A crate-level allowance for convenience is usually a warning sign.

### Formatting is not design

rustfmt removes style debate; it does not make names, modules, ownership, or algorithms good. Clippy suggestions are not commands. Read the lint, understand the semantic change, then fix or document the exception.

### CI should start from a clean checkout

A reliable route:

- installs or selects the pinned toolchain;
- checks committed generated/lock files as policy requires;
- runs from course root;
- does not depend on home-directory configuration;
- does not require network for standard-library-only tests after toolchain installation;
- uses isolated temporary paths;
- reports the failing stage clearly.

### Course structural audits

Code tools cannot prove that every module has exercises, answers, labs, links, and no empty instructional surfaces. The course includes Python audits for tree structure, local Markdown links, navigation targets, and Rust policy. These audits complement—never replace—Cargo verification.

## Use the idea in a complete program

The course capstone is **Taskboard**, a persistent command-line task board. Split reusable logic from the binary, minimize public visibility, and cover the contract with unit, integration, CLI, and documentation tests. The exact implementation task is in the [workbook](workbook.md); the full product contract is in the [capstone guide](../capstone.md).

## Practice sequence

1. Reproduce the important examples from this chapter without copying them line for line.
2. Complete the prediction and repair sections in the [workbook](workbook.md).
3. Build the independent [laboratory](../../labs/module-09-library-boundaries/README.md).
4. Apply the capstone increment.
5. Open the [reasoned solutions](solutions.md) only after recording your own answer.

## Ready to continue

You are ready for Module 10 when you can:

- answer the module question—“Which surfaces are product contracts, which are implementation details, and what independent evidence protects each boundary?”—without reading the chapter;
- demonstrate this outcome on a fresh example: Distinguish package, crate, target, and module while organizing code by responsibility rather than one file per type;
- repair the debugging case while preserving its product requirement;
- complete the laboratory transfer variant and explain the decisive design choice;
- name a simpler alternative and the condition under which you would prefer it.

## Primary Rust references

This chapter is self-contained. These official sources are included for verification and future language updates, not as required reading:

- [The Rust Book: Packages and Modules](https://doc.rust-lang.org/book/ch07-00-managing-growing-projects-with-packages-crates-and-modules.html)
- [The Rust Book: Testing](https://doc.rust-lang.org/book/ch11-00-testing.html)
- [rustdoc Book](https://doc.rust-lang.org/rustdoc/)

[← Module 8](../../../01-rust-foundations/course-book/module-08-generics-traits-conversions-and-lifetime-basics/index.md) · [sixty-module map](../../../COURSE_MAP.md) · [Module 10 →](../../../01-rust-foundations/course-book/module-10-integration-and-independent-change/index.md)

## Continue

1. Complete the [Module 9 workbook](workbook.md) and freeze every prediction before compiling.
2. Build [Laboratory 9 — Library Boundary Refactor](../../labs/module-09-library-boundaries/README.md) from its public contract.
3. Apply the Module 9 increment in the [Taskboard engineering guide](../capstone.md).
4. Review the [reasoned solutions](solutions.md) only after an independent attempt, then revise the causal model rather than copying code shape.
