# Module 01 — Compilation, Expressions, and Types

**Course 1 · Day 1 · Module 1 of 100**
`░░░░░░░░░░░░░░░░░░░░░░░░░` **1/100**

[Program](../../../README.md) · [Course 1](../index.md) · [Workbook](workbook.md) · [Laboratory](../../labs/module-01-measurement-report/README.md) · [Taskboard guide](../capstone.md)

[Module 2: Control Flow, Functions, and Invariants →](../module-02-control-flow-functions-and-invariants/index.md)

## The question

> How does Rust turn source text into a typed program, and what type and value does every expression produce?

## Why this comes now

Rust's compiler is not merely a final judge; it is the first instrument you learn to use. Before ownership or traits can make sense, you need a reliable loop for turning source text into typed feedback and for reading expressions as values. This module establishes that loop and the vocabulary every later explanation depends on.

### Prerequisite bridge

Bring one small program you already understand. Name one input assumption, one state invariant, one failure, and one observable result. This module gives you the type and compilation vocabulary to state those claims precisely; Module 2 will reuse that vocabulary when control flow introduces multiple paths and loop invariants.

### Scope boundary

This module owns the reasoning for **compilation, expressions, and types** inside Course 1. The course stays in safe Rust and mostly in the standard library. It introduces the ownership, trait, iterator, lifetime, module, and testing vocabulary required by later courses, but it does not yet pursue advanced lifetime algebra, smart-pointer architecture, unsafe code, concurrency, async runtimes, or macro construction. The purpose of the boundary is to keep the decisive relationship visible before later mechanisms are layered on top of it.

## What you will be able to do

- Distinguish package, crate, target, module, compiler, Cargo, profile, and artifact without collapsing them into “the project”.
- Derive the type and value of blocks, branches, tuples, arrays, function bodies, and semicolon-sensitive expressions before compiling.
- Choose numeric types and conversions from domain constraints, including overflow and floating-point limitations, rather than from habit.
- Use compiler diagnostics, tests, rustfmt, Clippy, and rustdoc as separate evidence channels and explain what each channel does not prove.
- Build and verify a small library-plus-binary package with pure calculation separated from rendering.

## Core model

### Why this module exists

Rust's surface syntax is not the difficult part. The first difficulty is that almost every construct participates in a static type calculation: blocks have types, branches must agree, array length is part of a type, numeric literals acquire types from context, and a semicolon can deliberately discard a value. If you treat these as isolated syntax facts, you will repeatedly “fix” diagnostics without understanding the program. The purpose of this module is to establish type-directed reading.

### The compilation model

A **package** is the manifest-described unit in `Cargo.toml`. A package can contain several **targets**: commonly one library crate and one or more binary crates, examples, tests, or benchmarks. Each target is compiled as a **crate**. Modules organize names and privacy inside a crate; they are not miniature packages.

Cargo coordinates dependency resolution, target selection, build profiles, compiler invocation, and test/documentation workflows. `rustc` type-checks and compiles a crate. `cargo check` proves that selected targets type-check; it does not run tests. `cargo test` builds test harnesses and executes tests; it does not prove untested behavior. `cargo clippy` applies a chosen lint policy; a clean run is not a semantic proof. `cargo doc` and documentation tests provide another contract surface.

This separation matters because “the project builds” is ambiguous. A library can check while a binary target fails; unit tests can pass while documentation examples are stale; debug behavior can differ from release behavior at overflow or optimization-sensitive boundaries.

### Expressions are typed values

Read a Rust function from the inside out. For every block, ask:

1. What is the type of the final expression?
2. Was that value discarded by a semicolon?
3. What type does the surrounding context require?
4. Do all control-flow paths produce that type?

```rust
fn clamp_to_byte(value: i32) -> u8 {
    let bounded = if value < 0 {
        0
    } else if value > i32::from(u8::MAX) {
        i32::from(u8::MAX)
    } else {
        value
    };

    bounded as u8
}
```

The `if` expression must have one type. Each branch produces `i32`; the final cast is safe because the preceding logic establishes the range. The cast is not safe merely because Rust permits `as`. The program's domain proof makes it safe for this contract.

Contrast:

```rust
fn broken(value: bool) -> i32 {
    if value {
        1
    } else {
        2;
    }
}
```

The semicolon makes the second branch `()`. The useful diagnosis is not “remove the semicolon”; it is “the branch types disagree because one branch discards its value.” That explanation transfers to blocks, match arms, and function bodies.

### Numeric contracts before numeric types

Do not begin with `i32` because examples do. State the domain:

- Can values be negative?
- What maximum must be represented?
- Is wraparound meaningful, invalid, or an error?
- Is fractional representation required?
- Are `NaN` and infinity accepted?
- Does conversion lose information?

For counts tied to indexing, `usize` is often natural at the collection boundary, but it is not a portable serialization type. For external formats, choose an explicit width. For arithmetic that may overflow, choose checked, saturating, wrapping, or overflowing operations according to the contract. Debug-versus-release overflow behavior is not a substitute for that decision.

Floating-point tests should state tolerance semantics. An absolute tolerance can be adequate around a known scale; relative or combined tolerances may be needed across magnitudes. This course does not pretend that `f64` arithmetic provides exact decimal or robust scientific statistics.

### Worked derivation: measurement summary

Suppose a function summarizes a borrowed slice:

```rust
#[derive(Debug, Clone, Copy, PartialEq)]
pub struct Summary {
    pub count: usize,
    pub minimum: f64,
    pub maximum: f64,
    pub total: f64,
    pub mean: f64,
}

pub fn summarize(values: &[f64]) -> Option<Summary> {
    let (&first, rest) = values.split_first()?;
    let mut minimum = first;
    let mut maximum = first;
    let mut total = first;

    for &value in rest {
        minimum = minimum.min(value);
        maximum = maximum.max(value);
        total += value;
    }

    let count = values.len();
    Some(Summary {
        count,
        minimum,
        maximum,
        total,
        mean: total / count as f64,
    })
}
```

The type `Option<Summary>` exposes the fact that minimum and maximum are undefined for empty input. `split_first()?` is preview syntax for early return from `Option`; the important Module 1 fact is that the function has a total return type and that the nonempty path obtains an actual initial value instead of inventing a sentinel. The loop never indexes, and the final struct expression is the value wrapped by `Some`.

A production numerical API would decide what to do with `NaN`, infinity, overflow in a different numeric domain, and large-sum accuracy. The lab states a narrower contract instead of claiming more.

### Try without the scaffold

Design `bounds_i64(values: &[i64]) -> Option<(i64, i64)>`. Before coding, write the types of:

- `values.split_first()`;
- the pattern `let (&first, rest) = ...`;
- `minimum.min(value)`;
- the tuple returned from the function.

Then implement it without indexing. If compilation fails, classify the failure before editing: pattern mismatch, reference/value mismatch, branch/return mismatch, or unrelated lint.

### Misconception clinic

- **“A semicolon is formatting.”** It changes an expression into a statement whose value is discarded.
- **“Inference is dynamic typing.”** Types are fixed and checked before execution; inference only reduces annotations.
- **“A cast proves conversion safety.”** It proves only that the language permits the conversion. The domain must prove that information loss is acceptable.
- **“A passing test proves the function.”** It proves only the executed examples under that build configuration.

### Decision discipline

When a diagnostic appears, do not begin with the suggested edit. Record:

```text
required type:
observed type:
expression that produced it:
contract that should hold:
smallest semantic repair:
repair that would compile but weaken the contract:
```

This record is the first evidence that you are using the compiler as a dialogue rather than a slot machine.

A Rust project is easier to reason about when its build vocabulary is exact.

### Toolchain responsibilities

`rustc` is the Rust compiler. Given a crate, it parses syntax, resolves names, checks types and borrows, performs monomorphization and code generation as needed, and emits artifacts.

Cargo is the package manager and build orchestrator. It reads `Cargo.toml`, resolves packages and dependencies, selects targets, invokes rustc with the correct flags, runs tests and examples, builds documentation, and manages build profiles.

The distinction matters. A rustc diagnostic is a language/compiler claim. A Cargo error may instead concern package layout, target selection, a manifest field, or dependency resolution.

```text
Cargo.toml + source tree
          │
          ▼
       Cargo plan
          │ invokes
          ▼
        rustc ─────► library/binary/test artifacts
```

rustfmt formats source according to the language's formatting conventions. Clippy analyzes compilable Rust for suspicious or non-idiomatic patterns. rustdoc extracts API documentation and compiles documentation examples. Rust Analyzer is an editor-facing language server; it does not replace the compiler proof route.

### Package, crate, target, module

A **package** is a Cargo distribution/build unit described by one `Cargo.toml`. A package may contain multiple **targets**: usually a library, one primary binary, additional binaries, examples, integration tests, and benchmarks.

A **crate** is one compilation unit. A library target is compiled as a library crate; each binary target is compiled as a binary crate. Integration-test files are separate crates that depend on the package library like an external caller.

A **module** is a namespace and privacy unit inside a crate. Modules do not automatically become packages or separate compilation units.

Conflating these words leads to architecture errors. Splitting `model.rs` and `storage.rs` creates modules in one library crate; it does not create micro-packages.

### Conventional package layout

```text
measurement-report/
├── Cargo.toml
├── src/
│   ├── lib.rs       # library crate root, when present
│   └── main.rs      # primary binary crate root, when present
├── tests/           # integration-test crates
├── examples/        # example binary targets
└── benches/         # benchmark targets
```

A package may have only `src/main.rs`, only `src/lib.rs`, or both. Course labs generally use both: reusable logic belongs in the library; demonstration output belongs in the binary.

### Manifest as contract

A minimal manifest:

```toml
[package]
name = "measurement-report"
version = "0.1.0"
edition = "2024"
rust-version = "1.85"
publish = false
```

- `name` determines the package name and default crate import name, with hyphens converted to underscores in Rust paths.
- `version` identifies the package release.
- `edition` controls edition-specific language behavior and migration boundaries; it is not the compiler version.
- `rust-version` declares the minimum supported Rust version for the package.
- `publish = false` prevents accidental registry publication.

The workspace centralizes these fields so ten lab packages share one policy.

### Build graph and incremental questions

Use the narrow command matching the evidence needed:

```bash
cargo check                    # semantic checks; usually no final code generation
cargo build                    # development artifacts
cargo build --release          # optimized release profile
cargo test                     # build test harnesses and run tests
cargo doc --no-deps            # build package documentation
cargo run -- arg1 arg2         # build and run one binary target
```

During type investigation, `cargo check` is usually the fastest relevant proof. During behavior work, select one test:

```bash
cargo test mixed_values_are_aggregated
```

A full release build proves something different from a check: it exercises optimized code generation and verifies that a deliverable artifact can be produced. It does not make an untested behavior correct.

### Reading `cargo metadata`

`cargo metadata --no-deps --format-version 1` exposes the build graph as JSON. At this stage, locate package names, targets, manifests, workspace members, and the target directory. Do not treat generated JSON as curriculum material; use it to verify your mental model of package structure.

### Design consequence

Before adding a directory, decide which boundary you need:

- another function: behavior decomposition;
- another module: namespace/privacy responsibility;
- another target: independently built entry point or test surface;
- another package: independent dependency/version/build unit;
- another workspace member: coordinated package in the same repository.

Course 1 favors one package with coherent modules unless a lab is intentionally independent.

### Immutable by default

```rust
let count = 3;
```

`count` is a binding to an inferred integer value. The binding cannot be assigned a new value unless declared mutable:

```rust
let mut count = 3;
count += 1;
```

Immutability is not a statement that the underlying type can never change internally; that distinction appears later with interior mutability. In ordinary Course 1 code, immutable means the binding cannot be used to mutate the value through ordinary mutable access.

Default immutability makes change visible in code review. It also narrows the compiler's reasoning: a value that is never mutated has fewer possible histories.

### Shadowing is a new binding

```rust
let input = " 42 ";
let input = input.trim();
let input = input.parse::<u32>();
```

Each `let input` creates a new binding. Shadowing may change type because it is not reassignment. The earlier binding becomes inaccessible by that name, though its value follows normal scope and ownership rules.

Use shadowing when the conceptual entity remains the same while its representation is refined: raw text → trimmed text → parsed value. Avoid shadowing when it hides two simultaneously meaningful values.

```rust
let metres = 10.0;
let miles = metres * 0.000_621_371; // two meanings deserve two names
```

### Constants

```rust
const MAX_TITLE_CHARS: usize = 120;
```

Constants require a type annotation and a compile-time-evaluable expression. They are named values substituted wherever used, not mutable storage. Prefer constants for domain limits that should be visible and shared.

### Scalar types

Rust has four scalar families:

- integers: signed `i8`…`i128`, `isize`; unsigned `u8`…`u128`, `usize`;
- floating point: `f32`, `f64`;
- Boolean: `bool`;
- Unicode scalar value: `char`.

`usize` is the natural type for collection lengths and indices because its width matches the platform address size. It is not a universal ID type. A task ID should be chosen for persistence/domain semantics, often `u64` in this course.

Numeric conversion is explicit. Rust does not silently mix arbitrary numeric types:

```rust
let count: usize = 3;
let total: f64 = 12.0;
let mean = total / count as f64;
```

The cast should be justified. Converting a potentially large `u64` to `u32` can truncate; converting an integer count to `f64` for a mean is explicit and acceptable within known bounds.

### Integer literals and inference

```rust
let attempts = 3;
```

The literal has no permanently dynamic type. Compiler context selects an integer type, defaulting to `i32` when unconstrained. Suffixes and annotations make constraints explicit:

```rust
let task_id = 3_u64;
let count: usize = 3;
```

Inference removes redundant annotations; it does not defer checking until runtime.

### Floating-point realities

Floating-point values are approximate. Tests should compare within a tolerance when operations may accumulate rounding error:

```rust
let actual = 0.1_f64 + 0.2;
assert!((actual - 0.3).abs() < 1e-12);
```

`f64` does not implement `Eq` because IEEE floating point includes `NaN`, whose equality behavior violates equivalence assumptions. This becomes relevant when deriving traits in Module 5.

### `char` is not a byte

```rust
let letter = 'é';
```

A Rust `char` is a Unicode scalar value and occupies four bytes as a Rust value. Its UTF-8 encoding may use one to four bytes. This distinction is why string indexing cannot pretend that “character number” equals byte offset. Module 4 treats strings in depth.

### Type annotations as communication

Annotate when:

- the compiler lacks context (`parse::<u64>()`);
- multiple valid types would encode different product meaning;
- a public boundary should make intent obvious;
- a numeric narrowing/widening deserves review;
- an empty collection literal has no element evidence.

Do not annotate every local merely to resemble another language. The compiler already proves inferred types.

The semicolon is not formatting punctuation. It can change a program's type.

### Expressions produce values

Literals, arithmetic, function calls, blocks, `if`, `match`, and many loops are expressions.

```rust
let width = 4;
let area = width * width;
```

`width * width` is an expression of type `i32` in this context.

### Statements perform an action without becoming the block value

A `let` binding is a statement. An expression followed by `;` is converted into an expression statement whose value is discarded.

```rust
let value = {
    let base = 4;  // statement
    base * 3       // final expression
};
```

`value` is `12`. Add a semicolon:

```rust
let value = {
    let base = 4;
    base * 3;
};
```

Now the block's final value is the unit value `()`. Unit is a real zero-sized type used when no meaningful value is produced.

### Function return expressions

```rust
fn doubled(value: i32) -> i32 {
    value * 2
}
```

The body is a block whose final expression must have type `i32`. This is equivalent to `return value * 2;`, but the final-expression style exposes the body's value naturally.

A semicolon creates a type mismatch:

```rust
fn doubled(value: i32) -> i32 {
    value * 2; // body now evaluates to ()
}
```

The compiler is not complaining about style. The declared contract says callers receive `i32`; the body produces `()`.

Use explicit `return` for early exits and guard clauses:

```rust
fn safe_ratio(total: f64, count: usize) -> Option<f64> {
    if count == 0 {
        return None;
    }
    Some(total / count as f64)
}
```

### `if` is an expression

```rust
let label = if score >= 80 { "high" } else { "normal" };
```

Both branches must produce one compatible type because `label` has one static type. Rust does not permit a variable to be sometimes text and sometimes an integer.

A missing `else` has unit as the no-branch value. Therefore this is valid only when the taken branch also produces unit:

```rust
if invalid {
    errors += 1;
}
```

This cannot initialize an integer:

```rust
let value = if condition { 4 }; // false branch would be ()
```

### Blocks create scope and values

Blocks can limit temporary names and borrows while returning a result:

```rust
let normalized_length = {
    let trimmed = input.trim();
    trimmed.len()
};
```

`trimmed` is unavailable outside; `normalized_length` remains. Later modules use smaller scopes to end borrows and deterministic resource lifetimes.

### Diverging expressions

Some expressions never produce a normal value: `return`, `break` in context, and `panic!` diverge. Their type is conceptualized as the never type `!`, which can coerce to other types because execution does not continue through that path.

```rust
let first = match values.first() {
    Some(value) => value,
    None => return None,
};
```

The `None` arm does not need to produce `&T`; it returns from the function.

### Parentheses versus tuples

```rust
let grouped = (1 + 2); // i32
let one_tuple = (1 + 2,); // (i32,)
```

The comma creates a tuple, not the parentheses. `()` is the empty tuple and unit value/type.

### Review method

For every block:

1. identify all statements;
2. locate the final expression, if any;
3. determine each branch type;
4. identify paths that diverge;
5. state the resulting block type.

This method scales directly to `match`, closures, and async blocks later.

### Function signatures are proof obligations

```rust
fn fahrenheit(celsius: f64) -> f64 {
    celsius * 9.0 / 5.0 + 32.0
}
```

Parameter types are mandatory in named functions. Return types are explicit unless the function returns unit. The signature lets callers reason without reading the body and lets the compiler check every path.

Choose function boundaries around one policy or transformation. A function named `process` that parses input, mutates state, writes a file, and formats output hides four contracts.

### Pure functions first

A pure function returns a value determined by its inputs and does not mutate external state. Pure boundaries are easier to test and later easier to parallelize or reuse.

```rust
fn valid_score(score: i32) -> bool {
    (0..=100).contains(&score)
}
```

The course capstone separates pure title validation and command parsing from filesystem effects for this reason.

### Tuples group a fixed heterogeneous product

```rust
fn bounds(values: &[i32]) -> Option<(i32, i32)> {
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

A tuple is appropriate for a small local result whose positions remain obvious. Once fields have independent domain meaning or many call sites, a named struct is clearer; Module 5 makes that refactor.

Destructure rather than repeatedly using numeric positions:

```rust
let Some((minimum, maximum)) = bounds(&values) else {
    return;
};
```

### Arrays encode length in the type

```rust
let readings: [f64; 4] = [18.5, 20.0, 19.25, 21.75];
```

`[f64; 4]` and `[f64; 5]` are different types. Arrays are fixed-size values stored inline. Their size is known at compile time and participates in type checking.

A function that accepts exactly three coordinates can take `[f64; 3]`. A function that accepts any number of borrowed values should generally take a slice `&[f64]`, introduced fully in Module 4:

```rust
fn total(values: &[f64]) -> f64 {
    let mut result = 0.0;
    for value in values {
        result += value;
    }
    result
}
```

At this point, read `&[f64]` as “a borrowed view of zero or more contiguous `f64` values.” Ownership details arrive later.

### Empty-input contracts

Minimum, maximum, and mean do not exist for an empty sequence. Returning `0.0` would conflate “no value” with a real zero-valued dataset. Return `Option`:

```rust
fn mean(values: &[f64]) -> Option<f64> {
    if values.is_empty() {
        return None;
    }
    Some(total(values) / values.len() as f64)
}
```

`Option` is previewed here as an honest return shape and treated as an enum in Module 5.

### Numeric overflow and profile behavior

Integer overflow behavior can differ between checked debug builds and optimized builds unless explicit checked/wrapping/saturating operations are chosen. Product logic should not rely on profile differences.

```rust
fn next_id(current: u64) -> Option<u64> {
    current.checked_add(1)
}
```

This makes exhaustion a value. For ordinary small counters in early exercises, simple arithmetic is sufficient, but identify where overflow would violate a domain invariant.

### Floating-point aggregate design

A summary should make its domain assumptions explicit:

- Are `NaN` inputs allowed?
- Are infinities allowed?
- Does order affect accumulated rounding?
- Is an arithmetic mean meaningful for the measurements?

The Module 1 lab accepts finite ordinary course inputs and uses tolerance-based tests. It does not claim numerically stable large-scale statistics; that is a separate scientific-computing topic.

### Read diagnostics as a chain

Consider a function declared to return `i32` whose body ends with a semicolon. The diagnostic usually identifies:

- the declaration establishing expected type `i32`;
- the body expression that produced unit;
- a suggestion to remove the semicolon.

The governing rule is “the function body block must evaluate to the declared return type,” not “Rust dislikes semicolons.” Record the general rule.

### Type annotations should resolve ambiguity, not suppress reasoning

When parsing text:

```rust
let id = "42".parse::<u64>();
```

The annotation tells the generic `parse` method which target type's `FromStr` implementation to use. An annotation cannot make an invalid conversion valid; it selects among implementations the type system knows.

### Unit tests near the behavior

```rust
pub fn celsius_to_fahrenheit(celsius: f64) -> f64 {
    celsius * 9.0 / 5.0 + 32.0
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn boiling_point_converts() {
        let actual = celsius_to_fahrenheit(100.0);
        assert!((actual - 212.0).abs() < 1e-10);
    }
}
```

`#[cfg(test)]` includes the module when building the test configuration. `#[test]` marks a zero-argument function as a test. `use super::*` brings parent-module items into scope.

A useful test names behavior and boundary. `test_conversion` is weaker than `boiling_point_converts` because failure output should reveal the contract.

### Testing absence

```rust
assert_eq!(summarize(&[]), None);
```

The test establishes that empty input is represented as absence rather than a fabricated summary. Boundary tests often protect more design meaning than ordinary examples.

### Test filtering and output

```bash
cargo test empty_input
cargo test -- --nocapture
```

The first filters test names. The second passes arguments after `--` to the test harness. Avoid `--nocapture` as a default; passing tests should not depend on inspected print output.

### Formatting

```bash
cargo fmt --all
cargo fmt --all -- --check
```

The first rewrites source. The second verifies no changes are needed. Formatting is deterministic collaboration infrastructure: review should focus on semantics rather than personal layout.

Do not manually fight rustfmt. When formatting looks awkward, the underlying expression may be too dense.

### Clippy

```bash
cargo clippy --all-targets -- -D warnings
```

Clippy runs after code compiles and may identify needless allocations, suspicious comparisons, confusing APIs, or standard-library patterns. A lint suggestion is subject to the same semantic review as a compiler suggestion.

The workspace denies several shortcuts (`unwrap_used`, `expect_used`, `todo`, `unimplemented`, `dbg_macro`) in compiled packages. This forces intentional error paths in later modules.

### Build profiles

Cargo's development and release profiles choose optimization and debug settings. Use:

```bash
cargo build
cargo build --release
```

Never encode product correctness in profile-dependent overflow behavior or timing assumptions. A release build is a delivery proof, not a behavioral specification.

### Documentation from Day 1

Public functions can use `///` documentation comments. Explain units, empty behavior, and failure conditions rather than restating the name.

```rust
/// Converts Celsius to Fahrenheit.
///
/// The calculation uses `f64`; callers requiring exact decimal arithmetic
/// need a different representation.
pub fn celsius_to_fahrenheit(celsius: f64) -> f64 {
    celsius * 9.0 / 5.0 + 32.0
}
```

### Daily proof route

```bash
cargo fmt --all -- --check
cargo check --all-targets
cargo clippy --all-targets -- -D warnings
cargo test --all-targets
```

Run narrow checks during development and the complete route at module exit.

### Model checkpoint

Before the complete-program example, verify that the model can decide a design rather than merely name its mechanism.

1. **Outcome 1.** For distinguish package, crate, target, module, compiler, Cargo, profile, and artifact without collapsing them into “the project”, construct one positive and one causal negative example. Mark the first decisive fact in the **type trace** and state which evidence could falsify the claim.

2. **Outcome 2.** For derive the type and value of blocks, branches, tuples, arrays, function bodies, and semicolon-sensitive expressions before compiling, construct one positive and one causal negative example. Mark the first decisive fact in the **type trace** and state which evidence could falsify the claim.

3. **Outcome 3.** For choose numeric types and conversions from domain constraints, including overflow and floating-point limitations, rather than from habit, construct one positive and one causal negative example. Mark the first decisive fact in the **type trace** and state which evidence could falsify the claim.

4. **Outcome 4.** For use compiler diagnostics, tests, rustfmt, Clippy, and rustdoc as separate evidence channels and explain what each channel does not prove, construct one positive and one causal negative example. Mark the first decisive fact in the **type trace** and state which evidence could falsify the claim.

5. **Preservation.** Name one earlier invariant that an easier but less precise implementation could regress.

6. **Boundary.** State one claim this module can justify and one adjacent claim that requires a later course, platform contract, peer behavior, or measurement.

A strong answer records state before and after the operation, the failure path, and the public consequence. An API name by itself is not a model.

## Use the idea in a complete program

The course capstone is **Taskboard**, a persistent command-line task board. Create the Taskboard package, its help surface, and a title-validation function. The important product lesson is that even the first small function has a type contract and tests. The exact implementation task is in the [workbook](workbook.md); the full product contract is in the [capstone guide](../capstone.md).

## Practice sequence

1. Reproduce the important examples from this chapter without copying them line for line.
2. Complete the prediction and repair sections in the [workbook](workbook.md).
3. Build the independent [laboratory](../../labs/module-01-measurement-report/README.md).
4. Apply the capstone increment.
5. Open the [reasoned solutions](solutions.md) only after recording your own answer.

## Ready to continue

You are ready for Module 2 when you can:

- answer the module question—“How does Rust turn source text into a typed program, and what type and value does every expression produce?”—without reading the chapter;
- demonstrate this outcome on a fresh example: Distinguish package, crate, target, module, compiler, Cargo, profile, and artifact without collapsing them into “the project”;
- repair the debugging case while preserving its product requirement;
- complete the laboratory transfer variant and explain the decisive design choice;
- name a simpler alternative and the condition under which you would prefer it.

## Primary Rust references

This chapter is self-contained. These official sources are included for verification and future language updates, not as required reading:

- [The Rust Book: Getting Started](https://doc.rust-lang.org/book/ch01-00-getting-started.html)
- [Cargo Book](https://doc.rust-lang.org/cargo/)
- [Rust Reference: Expressions](https://doc.rust-lang.org/reference/expressions.html)

[one-hundred-module map](../../../COURSE_MAP.md) · [Module 2 →](../module-02-control-flow-functions-and-invariants/index.md)

## Continue

Continue to [Module 2 — Control Flow, Functions, and Invariants](../module-02-control-flow-functions-and-invariants/index.md) after completing the workbook, independent laboratory, capstone increment, and closed-book explanation for this module.
