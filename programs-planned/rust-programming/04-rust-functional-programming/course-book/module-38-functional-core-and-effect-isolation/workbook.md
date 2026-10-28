# Workbook — Module 38: Functional Core and Effect Isolation

[Chapter](index.md) · [Laboratory](../../labs/module-08-deterministic-batch-runner/README.md) · [LedgerFlow guide](../capstone.md) · [Solutions](solutions.md)

This workbook tests whether **Functional Core and Effect Isolation** has become a usable model rather than remembered vocabulary. Its governing question is: *Which decisions can remain pure, which effects must occur at the boundary, and what data should cross between them?* Preserve your first prediction and record decisive facts in a **effect boundary map**. A repair succeeds only when it keeps the difficult product requirement visible.

## Retrieval warm-up

Before compiling or running anything:

1. Restate the invariant from Module 37 — Recursive Data and Structural Sharing that today’s mechanism must preserve.
2. Rewrite the governing question in your own words: **Which decisions can remain pure, which effects must occur at the boundary, and what data should cross between them?**
3. Draw the smallest **effect boundary map** that could decide one positive and one negative case.
4. Name one shortcut that could make the visible example pass while deleting ownership, failure, ordering, capacity, safety, compatibility, or evidence required by the product.

## Part 1 — Predict

For each specimen, write a five-part diagnosis: expected outcome; decisive expression or signature; governing rule; smallest requirement-preserving repair; and one tempting change that would compile while weakening the design. Tie every answer to **Functional Core and Effect Isolation** rather than quoting a diagnostic without explaining its cause.

| # | Specimen | Your prediction |
|---:|---|---|
| 1 | [`case-01.rs`](../../compiler-labs/module-08/case-01.rs) | Pass or fail? What exact rule decides? |
| 2 | [`case-02.rs`](../../compiler-labs/module-08/case-02.rs) | Pass or fail? What exact rule decides? |
| 3 | [`case-03.rs`](../../compiler-labs/module-08/case-03.rs) | Pass or fail? What exact rule decides? |
| 4 | [`case-04.rs`](../../compiler-labs/module-08/case-04.rs) | Pass or fail? What exact rule decides? |
| 5 | [`case-05.rs`](../../compiler-labs/module-08/case-05.rs) | Pass or fail? What exact rule decides? |
| 6 | [`case-06.rs`](../../compiler-labs/module-08/case-06.rs) | Pass or fail? What exact rule decides? |
| 7 | [`case-07.rs`](../../compiler-labs/module-08/case-07.rs) | Pass or fail? What exact rule decides? |
| 8 | [`case-08.rs`](../../compiler-labs/module-08/case-08.rs) | Pass or fail? What exact rule decides? |

Run all specimens for this course from the course root with:

```bash
python3 ../tools/run_compiler_labs.py 04-rust-functional-programming
```

## Part 2 — Diagnose and repair

A function named `analyze` performs these operations internally:

- reads `SystemTime::now()`;
- reads an environment variable;
- allocates IDs from a global atomic;
- prints warnings;
- writes a cache file;
- returns a Boolean.

Tests sleep, modify process environment, and compare captured stderr. They are slow and still cannot distinguish a domain rejection from an I/O failure.

### Build an effect inventory

Classify each observation as an input, decision, output value, or shell effect. Current time and environment-derived configuration are inputs. Warning selection is a decision. Warning text is output data. Printing and cache writes are effects.

### Repair the boundary

Parse environment and observe time once in the shell. Pass values to the core. If ID generation must be demand-driven, pass one narrow `FnMut() -> Id` whose call count is testable. Return a structured `CoreOutcome` containing decisions, diagnostics, and an effect plan or renderable report.

The shell interprets that value and maps operational failures to process status. Do not introduce a universal `Effect` trait merely to wrap `println!` and `fs::write`.

### Determinism proof

Run the core twice with identical explicit inputs and assert equal outcomes. Change only injected time and show the documented field that changes. Execute the shell against temporary paths to prove stdout/stderr routing and no partial write after rejection.

### Diagnose hidden cache state

A cache may remain, but it must be an explicit owned component with a declared invalidation key. A file hidden inside `analyze` cannot be reasoned about as a value transformation.

### Transfer question

Not every function in the shell must be tiny or generic. The architectural objective is to keep domain decisions independently executable and effects visible, not to eliminate imperative code from the program.

## Part 3 — Focused exercises

### Exercise 1 — Classify effects

For a batch processor, classify file reading, parsing, validation, current time, ID generation, sorting, rendering, terminal output, and exit-code choice as core, shell, or injected input. Defend ambiguous cases.

### Exercise 2 — Refactor an effectful function

A function reads a file, parses rows, prints warnings, and returns `bool`. Split it into core and shell APIs with typed outcomes.

### Exercise 3 — Inject unstable inputs

A report embeds `SystemTime::now()` and a generated batch ID deep inside validation. Redesign without building a large dependency-injection framework.

### Exercise 4 — Plan then execute

A command should write two files and then print success only if both replacements succeed. Represent the intended effects as data and discuss failure protocol.

### Exercise 5 — Idempotence and replay

A batch import inserts events into a ledger. State the conditions under which replay is idempotent and design a test.

### Exercise 6 — Core and shell evidence matrix

Create a test matrix for `execute_text` and the real CLI. Which properties belong at each layer?

### Interleaved reasoning pass

1. For **Separate deterministic domain decisions from filesystem, time, environment, and terminal effects**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the effect boundary map.
2. For **Inject small effect capabilities through parameters, closures, or narrow traits without building a framework**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the effect boundary map.
3. For **Represent intended effects as data when plan-then-execute improves safety or testability**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the effect boundary map.
4. For **Design idempotent and replayable boundaries where the domain permits them**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the effect boundary map.

5. Identify one guarantee from an earlier course that a careless implementation of **Functional Core and Effect Isolation** could regress.

For one case, write both a principled repair and a weaker repair that appears to work. The principled repair must preserve the requirement; the weaker repair must name the information, state, bound, or compatibility promise it silently discards.

## Part 4 — Independent laboratory

The executable package is `labs/module-08-deterministic-batch-runner/README.md`. The laboratory separates decisions from effect execution and makes partial effects explicit.

### Boundary map

Classify each input or operation before writing code:

| Concern | Core input/value | Shell effect |
|---|---|---|
| current time | explicit `u64` | clock observation |
| generated ID | injected `FnMut` | external sequence/service |
| validation | deterministic decision | none |
| file write | `Action::Write` value | filesystem operation |
| notification | `Action::Notify` value | external delivery |
| dry run | rendering of actions | terminal write outside core |

The core may not read environment variables, call a clock, access files, or print.

### Planning contract

`plan` accepts inputs, an explicit `now`, and a stateful ID generator. Rejected records do not consume IDs. Accepted records produce both analysis data and ordered action values. Write a call-ledger test that places invalid and overdue records before a valid record and proves the first generated ID goes to the valid item.

The planner must remain deterministic for equal explicit inputs and equal generator output. This does not mean the injected generator is pure; it means its state is an explicit dependency at the boundary.

### Execution contract

`execute` processes action values in order through a fallible callback. On failure it reports the number of successfully completed actions and preserves the source error type. It does **not** claim rollback. Add tests for failure on the first action, a middle action, and success of all actions.

### Dry run

Render the plan without executing any callback. Use an execution-call counter to prove zero effects. The rendered order must match execution order. Match action variants explicitly; do not publish `Debug` output as a report contract, because a derived debugging representation is not a deliberately versioned user format.

### Replay questions

Document:

- whether repeating the same plan would repeat writes or notifications;
- which action types are idempotent under what external assumptions;
- how a production shell could record completion and resume;
- why a deterministic plan can still become stale before execution.

Do not solve these with hidden global state in the course lab.

### Rejected designs

- closure-valued actions that cannot be inspected;
- generating IDs before validation;
- swallowing the executor’s source error into `String`;
- describing a successful prefix as transactionality;
- reading `SystemTime::now()` inside `plan`;
- testing the core by capturing stdout.

Submit the boundary map, ID call ledger, effect-order tests, partial-failure report, dry-run proof, and replay note. Explain why `FnMut` is required for ID allocation, why action values are preferable to boxed one-shot callbacks here, and where operational I/O errors belong in a real CLI.

The executable starter and reference implementation are in [module-08-deterministic-batch-runner](../../labs/module-08-deterministic-batch-runner/README.md). Implement from the contract first. Compare with the reference only after your tests pass or you have written a precise blocker.

### Laboratory acceptance trace

Before opening the reference implementation for **Deterministic Batch Runner**, record:

- the public behavior that demonstrates **Separate deterministic domain decisions from filesystem, time, environment, and terminal effects**;
- one adversarial input, state transition, schedule, peer action, workload, or build condition appropriate to this module;
- the exact state after rejection or partial failure;
- ownership and cleanup;
- ordering and capacity;
- one shortcut deliberately excluded by the contract;
- one claim the tests cannot establish.

## Part 5 — Capstone transfer

Day 8 moves LedgerFlow’s parsing, reduction, query, and report decisions behind a value-to-value core. The shell remains responsible for acquiring bytes, writing text, reading environment, and selecting a process exit code. Rust does not enforce purity; this is an architectural boundary that tests and signatures must make visible.

### Inventory every effect

List each current effect and assign it to core or shell:

| Effect or unstable input | Current location | Required location | Value crossing boundary |
|---|---|---|---|
| file read | | shell | input text or typed read error |
| terminal output | | shell | rendered stdout/stderr values |
| environment/config | | shell | parsed configuration value |
| time/ID generation | | shell or injected capability | explicit value/callback |
| process exit | | shell | exit classification |

Any hidden clock, global counter, environment lookup, print, or write inside the core must be removed or represented through an explicit narrow input.

### Core contract

Expose an operation equivalent to:

```rust
pub fn execute_text(command: Command, input: &str) -> CoreOutcome;
```

`CoreOutcome` should carry structured success data, diagnostics, rendered or renderable report data, and an exit classification. Avoid returning only a string when callers need to inspect the decision separately from presentation.

The core must not open a path, print, terminate the process, or read global state.

### Effect plan where order matters

If one command requires several effects—such as write report, then write diagnostics, then set exit status—represent the plan as data with explicit order. The shell interprets the plan. Do not create a generic “effect framework” for two concrete operations; use the narrowest product vocabulary.

### Deterministic replay test

Store one command and input fixture. Execute the core twice and assert identical structured outcomes. Then render twice and assert byte-for-byte equality. A changing clock or generated ID must be injected so the fixture controls it.

Add shell tests that invoke the real binary with temporary files and verify:

- stdout/stderr routing;
- exit classification;
- missing-file behavior;
- no partial output file after core rejection, if writing is supported;
- identical core decisions independent of the current working directory.

### Boundary review

For every public core function, ask:

1. Is every input visible in the signature?
2. Is failure returned as data?
3. Can the function be run entirely in memory?
4. Does it mutate only owned/local state?
5. Is output order deterministic by contract?

For every shell function, ask whether it contains domain decisions that belong back in the core.

### Capstone invariant trace

For the Module 38 LedgerFlow increment, name the changed invariant and its owner before editing code. Follow it through input, validation, state transition, effect, output, failure, cleanup, and tests. Add storage, wire, scheduler, generated-code, compatibility, resource, or measurement consequences when this course makes them relevant. End by naming one earlier guarantee that remains unchanged.

## Part 6 — Reconstruct and defend

Do not advance because the calendar day ended. Advance when all hard evidence is present.

### Advancement decision

Advance only when the deterministic core can run without filesystem, terminal, clock, process, or environment access and the shell has explicit effect errors.

### Closed-book retrieval

1. What makes a function deterministic for a stated set of inputs?
2. Which values should cross from shell to core?
3. Why should the core return a report rather than print?
4. How do domain rejection and operational failure differ?
5. When is injecting a closure enough, and when is a trait justified?
6. What is an effect plan?
7. What preconditions make an operation idempotent?
8. What input must be recorded for deterministic replay?
9. Why does a thin shell still need process tests?
10. How can hidden environment reads invalidate unit-test confidence?

### Reconstruction task

Split a batch renamer into pure planning and effect execution. The pure stage must return an ordered plan plus domain rejections; the shell performs and reports operations.

### Transfer task

Design a deterministic report generator whose shell supplies time and input bytes while the core returns a renderable report and an effect plan. Produce:

- pure decision input and output types;
- effect plan separated from execution;
- deterministic rendering or ordering contract;
- test that runs the functional core without filesystem, terminal, clock, or process access;

### Spaced review

Repeat questions 2, 4, 7, and 10 after 24 hours. Repeat the reconstruction after seven days with a different domain.

### Closed-book defense

In five minutes, answer “Which decisions can remain pure, which effects must occur at the boundary, and what data should cross between them?” using the **effect boundary map**. Include one positive case, one causal negative case, one principled repair, one rejected shortcut, and one transfer outside LedgerFlow. A list of APIs without the deciding relationship is incomplete.
