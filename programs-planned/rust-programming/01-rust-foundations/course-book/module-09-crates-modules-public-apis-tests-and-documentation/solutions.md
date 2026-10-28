# Reasoned solutions — Module 09: Crates, Modules, Public APIs, Tests, and Documentation

[Return to the workbook](workbook.md) · [Return to the chapter](index.md) · [Open the Taskboard engineering guide](../capstone.md)

Use these explanations to review your reasoning about **Crates, Modules, Public APIs, Tests, and Documentation**, not to substitute for an attempt. The decisive question is: *Which surfaces are product contracts, which are implementation details, and what independent evidence protects each boundary?* When your design differs, separate three possibilities: a Rust rule was applied incorrectly, the product contract changed, or two architectures satisfy the same contract with different trade-offs.

## Compiler specimen reasoning

### 1. `01-private-library-item.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** private child-module item is inaccessible to parent.
- **Causal explanation:** The compiler rejects the specimen because private child-module item is inaccessible to parent.
- **Principled repair:** Expose only the required item with `pub(crate)` or `pub` and keep unrelated module details private.
- **Weak repair to reject:** Do not make the entire module tree public.

### 2. `02-public-type-private-field.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** public struct still protects private field construction.
- **Causal explanation:** The compiler rejects the specimen because public struct still protects private field construction.
- **Principled repair:** Provide a public constructor and accessors that preserve the field invariant.
- **Weak repair to reject:** Do not expose the field solely to simplify test setup.

### 3. `03-reexport-path.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** public re-export creates the root path while module remains private.
- **Causal explanation:** The specimen compiles because public re-export creates the root path while module remains private.
- **Principled repair:** No repair is required. Preserve the example and explain the exact type, ownership, or visibility rule that permits it.
- **Weak repair to reject:** Do not replace this demonstration—public re-export creates the root path while module remains private—with broader ownership, visibility, or allocation merely to make the reasoning easier.

### 4. `04-integration-crate-root.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** rejects standalone: integration tests import the package library by crate name.
- **Causal explanation:** The compiler rejects the specimen because rejects standalone: integration tests import the package library by crate name.
- **Principled repair:** Compile the example as an integration test of a Cargo package and import the library by its crate name.
- **Weak repair to reject:** Do not rewrite the test as an internal unit test merely to avoid the package boundary.

### 5. `05-doctest-question-mark-context.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** main returns unit and cannot propagate ParseIntError with question mark.
- **Causal explanation:** The compiler rejects the specimen because main returns unit and cannot propagate ParseIntError with question mark.
- **Principled repair:** Give the doctest function a compatible `Result` return or handle parsing failure explicitly.
- **Weak repair to reject:** Do not replace `?` with `unwrap` in documentation presented as production guidance.

### 6. `06-public-field-invariant-hole.rs`

- **Outcome:** `run-fail`
- **Governing rule:** compiles then fails: public mutation bypasses any title invariant.
- **Causal explanation:** The specimen type-checks, then its assertion or reachable operation fails because compiles then fails: public mutation bypasses any title invariant.
- **Principled repair:** Keep the title private and route construction and mutation through validation-preserving methods.
- **Weak repair to reject:** Do not remove the failing assertion or postpone validation until rendering.

## Exercise reasoning and worked answers
### 1. Vocabulary map

Representative classifications:

- `rust-foundations/Cargo.toml`: workspace manifest, not itself a crate;
- `capstone/Cargo.toml`: package manifest;
- `capstone/src/lib.rs`: library crate root and library target source;
- `capstone/src/main.rs`: binary crate root and binary target source;
- `capstone/tests/cli.rs`: integration-test target, compiled as its own crate;
- `labs/module-04/solution`: a package and workspace member;
- `model.rs`: source file containing the `model` module when declared by `mod model;`;
- `taskboard::TaskBoard`: public item path;
- `TaskBoard::add`: associated function item;
- `cargo test --doc`: command operating on documentation-test targets.

### 2. Dependency graph

```text
model <- command
model <- storage
model <- app
command <- app
storage <- app
app <- lib facade <- binary
```

`command` may depend on model leaf types such as `TaskId`, `Priority`, and `Status`. `storage` depends on model construction/restoration. `app` orchestrates all three. Model has no outward dependency on transport or persistence.

### 3. Visibility audit

A compact public surface normally contains domain types and read/transition methods, command parsing only when external callers benefit, application entry points, and public error types returned by them. Record parsers, temporary-file builders, raw restoration helpers, and renderer internals remain private or `pub(crate)`.

A field is not public simply because it has an accessor. Representation remains changeable while behavior remains stable.

### 4. Validated mutation

```rust
impl Task {
    pub fn title(&self) -> &str { &self.title }

    pub fn rename(&mut self, title: String) -> Result<(), DomainError> {
        validate_title(&title)?;
        self.title = title;
        Ok(())
    }
}
```

Status changes use `start`, `complete`, and `reopen` methods that match legal current states. No `status_mut` is exposed.

### 5. Re-export facade

```rust
mod app;
mod command;
mod model;
mod storage;

pub use app::{run, AppError, Outcome};
pub use command::{parse_command, Command, CommandError};
pub use model::{DomainError, Priority, Status, Task, TaskBoard, TaskId};
```

An integration test uses `use taskboard::{Priority, TaskBoard};`. Internal file movement does not change that path.

### 6. Thin binary

A suitable binary:

```rust
fn main() {
    match taskboard::run_from_env() {
        Ok(output) => print!("{output}"),
        Err(error) => {
            eprintln!("error: {error}");
            std::process::exit(error.exit_code());
        }
    }
}
```

Whether `exit_code` belongs on a library error is debatable; an even thinner adapter can match high-level error categories. It must not duplicate domain rules.

### 7. Test placement

Examples:

- title byte boundary: model unit test;
- complete-from-todo matrix: model unit test;
- valid fixture decode: storage unit or integration test depending on visibility;
- downstream add/list workflow: integration test;
- public API example: documentation test;
- unknown CLI command exit/stderr: CLI test;
- missing-file first run through public application API: integration test;
- temporary rename helper detail: unit test only if separately meaningful.

Use the narrowest layer that observes the promised contract.

### 8. Corruption suite

Table cases should include header, `NEXT_ID` marker/value/count, record marker, ID, status, priority, title delimiters/length, extra fields, duplicate ID, and inconsistent next ID. Expected data should include exact error variant and physical line. A table reduces duplicated setup while preserving named case clarity.

### 9. Executable docs

Crate docs present one end-to-end in-memory example. Item docs state invariants and errors. `load` docs distinguish missing path from malformed existing file and describe the version boundary. Examples should use public imports only.

### 10. Manifest review

The capstone needs name, version, edition, Rust version, publish policy, and inherited lints. Convention discovers library and binary targets. No dependencies or features are needed. Root workspace lists executable members and excludes editable starters. Profile overrides are absent until measurement justifies them.

### 11. Proof route

```bash
python3 scripts/check_course.py
python3 scripts/check_markdown_links.py
python3 scripts/check_rust_policy.py
cargo fmt --all -- --check
cargo check --workspace --all-targets
cargo clippy --workspace --all-targets -- -D warnings
cargo test --workspace --all-targets
cargo test --workspace --doc
cargo doc --workspace --no-deps
cargo build --workspace --release
```

A Make target may package this sequence. The repository must include every fixture and script it references.

### 12. Refactoring resilience

Public tests should assert results, variants, bytes, streams, and status—not helper names. Unit tests tied to a private parser may change when the parser changes, but even those should prefer grammar behavior. If renaming a private helper breaks integration tests, representation leaked through the API or tests bypassed visibility.

### Final review

A smaller source tree is not automatically cleaner, and a larger one is not automatically modular. Cohesion, dependency direction, privacy, and evidence boundaries determine quality.

### Post-key transfer

Reduce an over-public monolithic CLI to a library with explicit boundaries and build one test at each relevant evidence layer.



## Laboratory comparison

The complete laboratory implementation is in [`module-09-library-boundaries/solution`](../../labs/module-09-library-boundaries/solution). Before reading it, write down:

- your public API;
- the invariant each type owns;
- the failure behavior;
- the ownership or dispatch topology;
- the complexity claim you are prepared to defend.

For **Crates, Modules, Public APIs, Tests, and Documentation**, compare the contract, invariant, failure behavior, ownership or dispatch topology, and cost before comparing syntax. A different implementation is sound when it preserves those properties and makes the module’s central relationship at least as clear.

## What a strong answer demonstrates

- Distinguish package, crate, target, and module while organizing code by responsibility rather than one file per type.
- Design private representation and a minimal public API that preserves invariants.
- Choose unit, integration, process, fixture, and documentation tests from the contract under proof.
- Write rustdoc examples that teach and execute, and maintain a deliberate warning/lint policy.
- Separate a thin effectful binary shell from a testable library core.

A complete explanation of **Crates, Modules, Public APIs, Tests, and Documentation** also states the boundary of the mechanism: which guarantee it does not provide, which cost it introduces, and which simpler design should be preferred when that guarantee is unnecessary.
