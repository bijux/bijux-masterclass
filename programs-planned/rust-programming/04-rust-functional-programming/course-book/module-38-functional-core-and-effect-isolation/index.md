# Module 38 — Functional Core and Effect Isolation

**Course 4 · Day 8 · Module 38 of 100**
`██████████░░░░░░░░░░░░░░░` **38/100**

[Program](../../../README.md) · [Course 4](../index.md) · [Workbook](workbook.md) · [Laboratory](../../labs/module-08-deterministic-batch-runner/README.md) · [LedgerFlow guide](../capstone.md)

[← Module 37: Recursive Data and Structural Sharing](../module-37-recursive-data-and-structural-sharing/index.md) · [Module 39: Combinator Laws and Cost Models →](../module-39-combinator-laws-and-cost-models/index.md)

## The question

> Which decisions can remain pure, which effects must occur at the boundary, and what data should cross between them?

## Why this comes now

Pure transformations become valuable when the program must also read files, consult time, print output, or mutate external state. This module separates decision data from effect execution. The result is not artificial purity; it is a core that can be tested exhaustively and a boundary whose failures are visible.

### Prerequisite bridge

Module 37 established **Recursive Data and Structural Sharing**. Before continuing, verify that you can recognize recursion-depth and allocation costs and select iterative alternatives when required. This module preserves that capability and adds the ability to separate deterministic domain decisions from filesystem, time, environment, and terminal effects. Module 39, **Combinator Laws and Cost Models**, will rely on both when it asks: *What semantic laws should a combinator preserve, and what can honestly be claimed about evaluation and cost?*

### Scope boundary

This module owns the reasoning for **functional core and effect isolation** inside Course 4. The course uses ordinary functions, closures, iterators, and immutable public models. It does not treat mutation as forbidden, and it postpones macro construction, parallel iteration, async streams, and benchmark-driven optimization. The purpose of the boundary is to keep the decisive relationship visible before later mechanisms are layered on top of it.

## What you will be able to do

- Separate deterministic domain decisions from filesystem, time, environment, and terminal effects.
- Inject small effect capabilities through parameters, closures, or narrow traits without building a framework.
- Represent intended effects as data when plan-then-execute improves safety or testability.
- Design idempotent and replayable boundaries where the domain permits them.
- Test the core with values and test the shell with focused boundary evidence.

Rust functions may read globals, mutate through interior mutability, perform I/O, consult time, or call foreign code. A signature such as `fn f(x: i32) -> i32` does not prove mathematical purity.

In this course, a **deterministic core function** is one whose observable result depends only on explicit inputs under its stated domain and whose execution does not perform external effects.

```rust
fn classify(amount: i64, threshold: i64) -> Risk {
    if amount >= threshold { Risk::High } else { Risk::Normal }
}
```

This is easy to test and replay.

```rust
fn classify_now(amount: i64) -> Risk {
    let threshold = std::env::var("THRESHOLD")
        .ok()
        .and_then(|s| s.parse().ok())
        .unwrap_or(1000);
    classify(amount, threshold)
}
```

The second function observes process environment and hides configuration failure. It belongs in a shell or configuration boundary.

## Core model

### Determinism has assumptions

Hash-map iteration order, locale-dependent services, floating-point reordering, and nondeterministic external inputs can affect results. State assumptions explicitly.

### Internal mutation can remain deterministic

A function may mutate uniquely owned local data and still satisfy deterministic input/output behavior. Purity here is an architectural property, not a syntactic ban.

### Effects as explicit inputs

Time can be passed as a timestamp, randomness as a seed or generated token, and environment as a parsed configuration. The core then reasons over values.

### Decision rule — Effects as explicit inputs

Do not claim Rust proves purity. Identify observable effects and move unstable inputs into explicit parameters or narrow boundaries. Test determinism as a product property.

The shell acquires inputs and performs effects. The core transforms values and decides what should happen.

```rust
fn run(path: &Path) -> Result<ExitCode, AppError> {
    let text = std::fs::read_to_string(path)?;       // shell
    let analysis = analyze(&text);                   // core
    print!("{}", render(&analysis));                // shell
    Ok(exit_code(&analysis))                         // core decision
}
```

`analyze`, `render`, and `exit_code` can be tested without the filesystem or process output.

### Boundary data should be typed

The shell should parse environment and CLI strings into domain values before calling the core. The core should return structured reports or plans rather than printing.

### Do not make the shell an untestable `main`

A thin `main` can delegate to a `run` function that accepts arguments and I/O abstractions. Process-level tests still verify exit codes and output.

### Core failure and shell failure differ

Invalid input data may be a reportable analysis result with exit code 1. Failure to open a file is an operational error with exit code 2. Keeping them separate prevents every rejection from becoming an I/O-style error.

### Effect sequence

The shell may need transactional ordering: write a temporary file, flush, replace, then report success. Functional isolation does not remove effect protocol design; it narrows where it lives.

### Decision rule — Effect sequence

Keep domain parsing, validation, reduction, and rendering deterministic where practical. Put acquisition, persistence, terminal output, and process exit behavior in a narrow shell with explicit operational errors.

Time, randomness, and identifier generation are inputs even when APIs expose them as ambient services.

### Pass values when one observation is enough

```rust
fn expire(records: &[Record], now: Timestamp) -> Vec<RecordId> {
    records
        .iter()
        .filter(|record| record.deadline <= now)
        .map(|record| record.id)
        .collect()
}
```

The caller observes the clock once. Every record uses the same `now`, improving consistency.

### Pass a callable when repeated generation is part of the protocol

```rust
fn assign_ids<T, F>(items: Vec<T>, mut next_id: F) -> Vec<(Id, T)>
where
    F: FnMut() -> Id,
{
    items.into_iter().map(|item| (next_id(), item)).collect()
}
```

Tests provide a deterministic counter closure. The production shell may wrap a real generator.

### Call-count contract matters

If validation can reject items before ID assignment, decide whether rejected items consume IDs. Adapter order and short-circuiting affect generator calls. Required uniqueness should not depend on a callback being invoked an undocumented number of times by another algorithm.

### Traits or closures

Use a closure for one narrow operation. Use a trait when several methods form a stable capability or multiple components share the boundary, as established in Course 3. Do not build a service-container framework.

### Random seeds and replay

Passing a seed permits replay only if the algorithm and version are controlled. Passing generated choices as explicit data is stronger for long-term audit.

### Decision rule — Random seeds and replay

Pass a value for one observation, a callable for one narrow repeated operation, and a trait for a coherent capability. Specify call count and whether failures consume generated values.

A query returns information without requesting a state change. A command requests a change. Keeping them distinct clarifies retries and tests.

### Plan then execute

The core can produce an effect plan:

```rust
#[derive(Debug, PartialEq, Eq)]
enum FileAction {
    Write { path: PathBuf, contents: String },
    Remove { path: PathBuf },
}

fn plan_export(report: &Report, destination: PathBuf) -> Vec<FileAction> {
    vec![FileAction::Write {
        path: destination,
        contents: render(report),
    }]
}
```

The shell executes actions and handles I/O failure.

### Benefits

- plan logic is deterministic and easy to inspect;
- tests compare values rather than mock calls;
- dry-run output is natural;
- authorization can review the plan;
- execution can record exactly which actions succeeded.

### Limits

A plan can become stale between creation and execution. Files may change, permissions may disappear, or another process may race. The executor must still validate assumptions and report partial completion.

### Commands as data are not always necessary

For one direct read or write, a plan type can add ceremony. Use it when review, dry-run, batching, retry, or transactional sequencing matters.

### Query purity

A method named `query` that updates a hidden cache is logically observational but internally effectful. That may be acceptable with interior mutability, but document thread and reentrancy behavior. In the functional core, prefer explicit derived values unless caching is justified.

### Decision rule — Query purity

Represent effects as data when planning has product value. Keep command and query semantics distinct, and do not mistake a plan for guaranteed execution.

An operation is idempotent when applying it repeatedly has the same observable result as applying it once, under stated conditions.

Normalization often aims for idempotence:

```rust
fn normalize_tag(value: &str) -> String {
    value.split_whitespace().collect::<Vec<_>>().join(" ").to_ascii_lowercase()
}
```

Test:

```rust
let once = normalize_tag(input);
let twice = normalize_tag(&once);
assert_eq!(once, twice);
```

### Not every transformation should be idempotent

Appending an event, incrementing a counter, or generating a new ID is intentionally not idempotent. Do not impose the law where it conflicts with meaning.

### Replay

A reducer is replayable when the same ordered events and initial state yield the same result. Hidden time, random values, environment, and nondeterministic ordering break this property.

### Stable ordering

Use deterministic collections or sort before rendering when output order matters. Sorting requires a total ordering policy and may materialize data.

### Duplicate events

Replay-safe event processing often needs stable event IDs and duplicate policy. “Apply twice” may not be equivalent to replay if duplicate suppression is external or stateful.

### Idempotent effect execution

Writing identical content to the same file may be idempotent in final state but still updates metadata or triggers observers. Define the observable boundary before claiming idempotence.

### Decision rule — Idempotent effect execution

State the domain, preconditions, and observation boundary of every idempotence or replay claim. Test counterexamples such as reordered input, duplicates, and hidden unstable values.

A deterministic core is tested with values, examples, laws, and exhaustive small domains. A shell is tested through boundary behavior and controlled dependencies.

### Core tests

- exact input/output examples;
- invariant preservation;
- law tests such as normalization idempotence;
- order sensitivity and duplicate behavior;
- empty, singleton, and boundary values;
- failure accumulation versus fail-fast behavior.

### Shell tests

- missing and unreadable files;
- valid input process output;
- exit codes for accepted, rejected, and operational-error states;
- output destination failures;
- no write after failed core validation when that is the contract;
- deterministic formatting.

### Avoid mocking the standard library broadly

A function accepting `impl Read` or input text is often enough. Use temporary directories only where real filesystem behavior matters. The course avoids third-party testing crates, but the principle is broader.

### Golden files

Golden output can protect formatting, but it should be small, reviewed, and paired with structural tests. Large snapshots can approve accidental changes without understanding.

### Test effect ordering

When failure atomicity depends on sequence, use a fake executor that records attempted actions and can fail at a chosen step. This is a justified callback or trait boundary.

### Decision rule — Test effect ordering

Test deterministic logic directly with values. Test the shell at its real observable boundaries, and introduce fakes only for protocols that cannot be proven through values alone.

### Printing from domain functions

A parser that prints diagnostics cannot be reused by a GUI, library, or test without capturing process output. Return a diagnostic value.

### Reading configuration everywhere

Calling `env::var` in several domain functions produces inconsistent snapshots and scattered failure policy. Parse configuration once at the boundary.

### Hidden global caches

They complicate tests, concurrency, lifetime, and invalidation. A local owned cache or explicit memoization object is easier to reason about.

### Callback service locators

Passing ten closures for filesystem, time, IDs, logging, configuration, and output is not automatically functional. It can recreate a dependency container with anonymous fields. Group coherent capabilities or move the boundary upward.

### Plans that mirror every I/O call

An effect plan with dozens of low-level variants can become an invented operating system. Model domain actions, not implementation instructions, unless replay requires the lower level.

### “Pure” wrappers around effects

Returning a closure that performs I/O later does not make the operation pure; it defers the effect. The effect flow must still record execution timing and failure.

### Over-isolation

A tiny CLI may be clearest with one `run` function that reads, transforms, and writes using well-tested helpers. Architecture should reduce risk, not maximize layers.

### Decision rule — Over-isolation

Isolate effects at the smallest boundary that improves determinism, reuse, review, or failure control. Reject layers that only relocate complexity.

### Batch export

Core:

```rust
fn analyze(text: &str, now: Timestamp) -> Analysis
fn plan_export(analysis: &Analysis, destination: PathBuf) -> Vec<FileAction>
fn exit_code(analysis: &Analysis) -> u8
```

Shell:

```rust
fn run(args: Args) -> Result<u8, OperationalError> {
    let text = fs::read_to_string(&args.input)?;
    let now = system_time()?;
    let analysis = analyze(&text, now);
    let actions = plan_export(&analysis, args.output);
    execute(actions)?;
    Ok(exit_code(&analysis))
}
```

The core remains deterministic for explicit `text` and `now`. The shell can fail independently. Invalid records are an analysis result; unreadable input is operational failure.

### ID injection

A batch assignment function accepts `FnMut() -> Id`. Tests supply a deterministic sequence. The contract states IDs are generated only after validation, so rejected items do not consume IDs.

### Rejected plan

A plan that stores `Box<dyn FnOnce() -> io::Result<()>>` hides actions and cannot support review or dry-run rendering. Domain action values are preferable.

### Model checkpoint

Before the complete-program example, verify that the model can decide a design rather than merely name its mechanism.

1. **Outcome 1.** For separate deterministic domain decisions from filesystem, time, environment, and terminal effects, construct one positive and one causal negative example. Mark the first decisive fact in the **effect boundary map** and state which evidence could falsify the claim.

2. **Outcome 2.** For inject small effect capabilities through parameters, closures, or narrow traits without building a framework, construct one positive and one causal negative example. Mark the first decisive fact in the **effect boundary map** and state which evidence could falsify the claim.

3. **Outcome 3.** For represent intended effects as data when plan-then-execute improves safety or testability, construct one positive and one causal negative example. Mark the first decisive fact in the **effect boundary map** and state which evidence could falsify the claim.

4. **Outcome 4.** For design idempotent and replayable boundaries where the domain permits them, construct one positive and one causal negative example. Mark the first decisive fact in the **effect boundary map** and state which evidence could falsify the claim.

5. **Preservation.** Name one earlier invariant that an easier but less precise implementation could regress.

6. **Boundary.** State one claim this module can justify and one adjacent claim that requires a later course, platform contract, peer behavior, or measurement.

A strong answer records state before and after the operation, the failure path, and the public consequence. An API name by itself is not a model.

## Use the idea in a complete program

The course capstone is **LedgerFlow**, a deterministic event-analysis pipeline with diagnostics, audit history, queries, and reports. Move filesystem and terminal operations into an effect shell around a deterministic analysis core. Represent intended effects as data where that improves testing. The exact implementation task is in the [workbook](workbook.md); the full product contract is in the [capstone guide](../capstone.md).

## Practice sequence

1. Reproduce the important examples from this chapter without copying them line for line.
2. Complete the prediction and repair sections in the [workbook](workbook.md).
3. Build the independent [laboratory](../../labs/module-08-deterministic-batch-runner/README.md).
4. Apply the capstone increment.
5. Open the [reasoned solutions](solutions.md) only after recording your own answer.

## Ready to continue

You are ready for Module 39 when you can:

- answer the module question—“Which decisions can remain pure, which effects must occur at the boundary, and what data should cross between them?”—without reading the chapter;
- demonstrate this outcome on a fresh example: Separate deterministic domain decisions from filesystem, time, environment, and terminal effects;
- repair the debugging case while preserving its product requirement;
- complete the laboratory transfer variant and explain the decisive design choice;
- name a simpler alternative and the condition under which you would prefer it.

## Primary Rust references

This chapter is self-contained. These official sources are included for verification and future language updates, not as required reading:

- [The Rust Book: I/O Project](https://doc.rust-lang.org/book/ch12-00-an-io-project.html)
- [std::io](https://doc.rust-lang.org/std/io/)

[← Module 37](../../../04-rust-functional-programming/course-book/module-37-recursive-data-and-structural-sharing/index.md) · [one-hundred-module map](../../../COURSE_MAP.md) · [Module 39 →](../../../04-rust-functional-programming/course-book/module-39-combinator-laws-and-cost-models/index.md)

## Continue

Continue to [Module 39 — Combinator Laws and Cost Models](../module-39-combinator-laws-and-cost-models/index.md) after completing the workbook, independent laboratory, capstone increment, and closed-book explanation for this module.
