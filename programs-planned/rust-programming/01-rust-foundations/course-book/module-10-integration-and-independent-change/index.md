# Module 10 — Integration and Independent Change

**Course 1 · Day 10 · Module 10 of 100**
`██░░░░░░░░░░░░░░░░░░░░░░░` **10/100**

[Program](../../../README.md) · [Course 1](../index.md) · [Workbook](workbook.md) · [Laboratory](../../labs/module-10-inventory-ledger/README.md) · [Taskboard guide](../capstone.md)

[← Module 9: Crates, Modules, Public APIs, Tests, and Documentation](../module-09-crates-modules-public-apis-tests-and-documentation/index.md) · [Module 11: Places, Move Paths, and Advanced Borrowing →](../../../02-rust-ownership-lifetimes-memory/course-book/module-11-places-move-paths-and-advanced-borrowing/index.md)

## The question

> Can you make and defend a cross-layer change without tutorial imitation or accidental contract regression?

## Why this comes now

The first course ends by removing the tutorial scaffold. Every earlier mechanism must now cooperate in one change that crosses model, parser, storage, tests, documentation, and CLI behavior. The goal is not another Rust feature; it is proof that you can reason through a complete small program independently.

### Prerequisite bridge

Module 9 established **Crates, Modules, Public APIs, Tests, and Documentation**. Before continuing, verify that you can separate a thin effectful binary shell from a testable library core. This module preserves that capability and adds the ability to trace a behavioral change through grammar, types, domain rules, persistence, rendering, tests, and documentation. Module 11, **Places, Move Paths, and Advanced Borrowing**, will rely on both when it asks: *Which places, projections, move paths, and loans are active at each program point, and how can access be decomposed safely?*

### Scope boundary

This module owns the reasoning for **integration and independent change** inside Course 1. The course stays in safe Rust and mostly in the standard library. It introduces the ownership, trait, iterator, lifetime, module, and testing vocabulary required by later courses, but it does not yet pursue advanced lifetime algebra, smart-pointer architecture, unsafe code, concurrency, async runtimes, or macro construction. The purpose of the boundary is to keep the decisive relationship visible before later mechanisms are layered on top of it.

## What you will be able to do

- Trace a behavioral change through grammar, types, domain rules, persistence, rendering, tests, and documentation.
- Preserve failure atomicity, deterministic behavior, and public invariants while refactoring across architectural layers.
- Review unfamiliar Rust for ownership workarounds, swallowed errors, invalid-state models, and missing evidence.
- Build a closed-book small program and an independent capstone feature from specification only.
- Defend design choices, rejected alternatives, known limitations, and verification boundaries with concrete evidence.

## Core model

### Why this module exists

The final module tests transfer. Following ten guided implementations does not guarantee that you can change an unfamiliar program coherently. Mastery is the ability to take a behavioral requirement, identify every affected contract, predict ownership/failure consequences, implement the change, add evidence, and explain limitations without a recipe.

### Change-impact map

For any new command or feature, inspect:

```text
user grammar
  ↓
raw token parsing
  ↓
typed command/data
  ↓
domain invariants and state transition
  ↓
application orchestration
  ↓
persistence compatibility and commit decision
  ↓
rendered output / exit status
  ↓
unit + integration + process + documentation evidence
```

A change is incomplete if one layer still uses an older assumption. For example, adding `rename` requires title validation, typed command data, model mutation, “changed state” classification, save behavior, help text, parsing tests, domain tests, persistence round-trip tests, CLI tests, and documentation.

### Preserve failure atomicity

For an in-memory operation, decide whether failure may leave partial state. The capstone aims for a strong application-level rule: validate and locate before replacing live fields; a failed domain operation leaves the board unchanged. For persistence, the course states a narrower single-process replacement protocol and does not confuse it with crash-proof database atomicity.

Tests should inspect state after failure, not merely assert that an error occurred.

### Independent feature method

1. Restate behavior as examples and invariants.
2. Identify new states and failures.
3. Mark affected modules/files before coding.
4. Write one failing public-behavior test.
5. Implement the smallest domain change.
6. connect parsing/orchestration/persistence.
7. Add hostile and regression tests.
8. run the proof route.
9. remove debug output and accidental API widening.
10. defend one rejected design.

The compiler is allowed, but tutorial code and reference solutions are not.

### Bug-hunting taxonomy

Review unfamiliar Rust for:

- ownership workarounds: unexplained clones, long mutable borrows, avoidable ownership;
- model defects: strings/flags permitting contradiction;
- error defects: `unwrap`, swallowed parse errors, missing context, wrong exit code;
- persistence defects: partial mutation, unstable ordering, broad durability claims;
- API defects: public fields, unnecessary generics/lifetimes, effect leakage;
- evidence defects: tests asserting only happy paths or internal structure.

A compiler-clean program can contain every one of these defects.

### Worked impact review: adding `archive`

Suppose tasks can be archived only from `done` and archived tasks do not appear in ordinary lists.

Questions before code:

- Is archive a new `Status` variant or a separate visibility flag? A single status variant avoids contradictory “todo and archived.”
- Does the storage grammar need a new token? Yes; version compatibility must be considered.
- Can older readers reject the new token contextually? They should, unless a migration policy is defined.
- Does `reopen` accept archived tasks? The policy must say.
- Do statistics include archived? Define separate counts.
- Is archive a mutating command? Yes; save only after success.
- Which exhaustive matches now fail? Treat those errors as a review checklist.

This is the value of typed state: change pressure becomes visible.

### Release proof versus mastery proof

A release proof establishes artifact properties under a toolchain: formatting, compilation, lint policy, tests, docs, and scenarios. A mastery proof establishes independent capability: predictions, independent construction, changed requirements, and explanation. Neither substitutes for the other.

### Independent transfer

Add a `prioritize <id> <priority>` command or another independently selected feature. Do not begin from parser code. Begin with state and invariant policy, then trace outward. After completion, explain who owns every new string, which functions borrow, and what state survives each failure.

### Misconception clinic

- **“Tests pass, therefore the specification is correct.”** Tests are samples of an interpreted specification.
- **“The compiler makes refactoring safe.”** It protects type/borrow rules, not product semantics.
- **“More code proves mastery.”** A smaller coherent change with strong evidence is better.
- **“Mastery means no documentation.”** Experts consult references; mastery is knowing what must be checked and how to integrate it.

### Invariants need owners

An invariant without one responsible constructor or operation will eventually be bypassed. The capstone's principal invariants include:

- every `TaskId` is positive;
- IDs are unique within a board;
- `next_id` is greater than every stored ID and has not overflowed;
- titles are trimmed, nonempty, bounded, and free of version-1 delimiters;
- priority and status are closed enums;
- transitions follow the legal state machine;
- task ordering in rendered and stored output is deterministic;
- a returned board is fully valid;
- a failed command does not claim or persist success;
- a failed load does not replace valid caller state;
- a failed save does not intentionally destroy the prior target.

Create an invariant map:

| Invariant | Established by | Preserved by | Rejected at |
|---|---|---|---|
| positive ID | `TaskId::try_from` | copy/borrow only | command and record parsing |
| title validity | `Task::new` / `restore` / `rename` | private field | domain constructor |
| legal transition | task transition methods | private status | domain operation |
| unique IDs | `TaskBoard::add` / `restore` | private vector mutation | board construction |
| canonical bytes | `save_to` | fixed encoder | exact-byte tests |

If two unrelated layers each implement the same invariant, they can drift. A parser may do early checks for better context, but domain construction remains authoritative.

### Trace one mutating command

For `taskboard done 7`:

1. the shell provides argument strings;
2. command parsing borrows tokens and constructs owned/typed `Command::Done(TaskId)`;
3. the application loads a valid `TaskBoard` from the configured path;
4. board lookup obtains exclusive access to the target task;
5. the task transition validates current status and mutates it;
6. the application receives a changed outcome;
7. storage encodes the complete new board to a temporary file;
8. commit replaces the target;
9. an owned success message is returned;
10. the binary writes stdout and selects a success exit status.

On any error, identify exactly which later steps do not occur.

### Borrow scopes are architectural events

Finding a mutable task inside a vector creates an exclusive borrow of the board's task storage. Do not retain that borrow while asking the board to perform another operation:

```rust
fn complete(&mut self, id: TaskId) -> Result<(), DomainError> {
    let task = self
        .tasks
        .iter_mut()
        .find(|task| task.id() == id)
        .ok_or(DomainError::UnknownTask { id })?;
    task.complete()
}
```

The borrow ends at return. If subsequent board-level validation is needed, use a narrower block or collect the needed scalar before releasing the task borrow.

### Error flow is data flow

A malformed stored ID may travel:

```text
ParseIntError
  -> RecordError::InvalidId { token, source }
  -> StorageError::InvalidRecord { line, source }
  -> AppError::Storage
  -> Display + exit policy
```

At each conversion, preserve or add evidence. Never convert backward or discard the line because the final user message is brief.

### Output and persistent state are separate contracts

A command can compute correct output and still fail to persist. Therefore success rendering must occur after save. Conversely, a read-only command should not rewrite the file merely because output was generated.

### Requirements must be observable

Weak requirement:

> Add archive support.

Operational specification:

> `taskboard archive <id>` succeeds only for a task in `Done`, removes it from active listings, preserves it in persistent state, makes `list archived` display it in ID order, returns exit status 1 for unknown IDs or non-done tasks, and remains compatible with all version-1 files under a stated format strategy.

The second statement defines inputs, state transitions, visibility, failure, order, process behavior, and compatibility. It still leaves implementation decisions to you.

### Build a behavior matrix

For `reopen <id>`:

| Current condition | Result | State change | Save | Exit |
|---|---|---:|---:|---:|
| task is `Done` | success | `Done -> Todo` | yes | 0 |
| task is `Todo` | illegal transition | none | no | nonzero |
| task is `Doing` | illegal transition | none | no | nonzero |
| ID absent | unknown task | none | no | nonzero |
| malformed ID | command error | none/load not attempted | no | nonzero |
| storage corrupt | storage error | none | no | nonzero |

This table becomes test input and prevents happy-path tunnel vision.

### Map every affected surface

A feature can affect:

- `Command` enum and parser;
- help and README;
- model state/transition methods;
- application dispatch;
- rendering;
- storage only if representation changes;
- standard-trait parsing/display;
- unit/integration/doc/CLI tests;
- public exports;
- complexity and allocation.

An impact matrix is not bureaucracy. It prevents a green domain test from hiding an outdated CLI or incompatible format.

### Preserve format unless behavior requires change

A new query such as `search` may require no storage change. A new persistent field does. When a format change is required, choose explicitly:

- keep version 1 and derive the new behavior from existing data;
- define version 2 and reject version 1;
- define version 2 and migrate/read both versions;
- use an extension record compatible with version-1 grammar only if version 1 explicitly permits unknown records.

Do not append a field while retaining the same header and call it compatible.

### Define no-op semantics

Some operations can succeed without change; others should report an error. For example, “set priority to its current value” could be a successful no-op or a distinct outcome. The specification must state whether the file is rewritten and what output appears.

### Nonfunctional constraints are still contracts

Add explicit limits:

- title/query byte bounds;
- deterministic order;
- maximum acceptable one-pass complexity for the current collection model;
- standard-library-only boundary;
- safe Rust only;
- no hidden network or clock dependency.

### In-memory failure atomicity

This is unsafe semantically:

```rust
fn rename_all(tasks: &mut [Task], prefix: &str) -> Result<(), DomainError> {
    for task in tasks {
        task.rename(format!("{prefix} {}", task.title()))?;
    }
    Ok(())
}
```

If the fourth title exceeds the limit, three tasks changed. A transactional design computes and validates all new titles, then commits:

```rust
let names = tasks
    .iter()
    .map(|task| validated_title(format!("{prefix} {}", task.title())))
    .collect::<Result<Vec<_>, _>>()?;

for (task, name) in tasks.iter_mut().zip(names) {
    task.rename_validated(name);
}
```

The internal `rename_validated` must remain restricted so callers cannot bypass validation.

### Persistence audit

Trace these failure points:

- target open/read;
- temporary path derivation;
- temporary create;
- serialization;
- buffered write;
- flush;
- file synchronization;
- rename;
- cleanup;
- output write after commit.

The final point is subtle: storage may commit successfully and stdout may then fail. The command changed state but could not report success. The CLI should return an output error without pretending persistence rolled back.

### Idempotence and retry

A failed response after successful commit can make blind retry dangerous for non-idempotent operations. `add` could create a second task. This foundational CLI cannot solve all distributed-failure ambiguity, but documentation should distinguish:

- failure before commit: old persistent state authoritative;
- failure at commit: result may require inspection depending on platform/error;
- failure after commit while printing: new state authoritative though command reports output failure.

This is deeper honesty than “any error means nothing happened.”

### Corruption and compatibility audit

Load tests should prove:

- no invalid board is returned;
- unknown versions are rejected distinctly;
- line context is physical and stable;
- duplicate IDs and inconsistent metadata are rejected;
- exact valid fixtures remain accepted;
- writer output remains canonical.

### Step 1 — Rewrite the requirement as examples

Before code, write concrete scenarios with arguments, initial state, expected result, file change, output, and exit status. Include invalid syntax, absent IDs, illegal states, empty results, and boundary lengths.

### Step 2 — Build the impact matrix

Mark command, domain, application, rendering, storage, public API, tests, and docs. Write “no change” explicitly with a reason. This prevents accidental omission from masquerading as deliberate scope.

### Step 3 — Choose the invariant owner

A new priority change belongs in a `Task` method if it affects one task and has domain rules. A board-wide unique constraint belongs in `TaskBoard`. Text token spelling belongs in `FromStr`; command arity belongs in command parsing.

### Step 4 — Design signatures before bodies

For a rename feature:

```rust
pub fn rename(&mut self, id: TaskId, title: String) -> Result<(), DomainError>;
```

Questions:

- Why own `String`? Because successful state must retain it.
- Can validation borrow before movement? Yes.
- Should the caller keep the original string on failure? If required, accept `&str` and allocate after validation or return the input in the error; specify the contract.
- What does `Ok(())` prove? The named task exists and now owns a valid title.

### Step 5 — Write failing tests at boundaries

Start with model behavior matrix and command grammar. Add integration tests for workflow and CLI tests for process behavior. Do not overbuild a private implementation merely to satisfy speculative tests.

### Step 6 — Implement from inside out

A stable order:

1. domain type/method;
2. command enum/parser;
3. application dispatch;
4. rendering;
5. persistence only if representation changes;
6. binary help/output;
7. docs.

Run focused tests after each boundary, then full proof.

### Step 7 — Perform ownership and cost review

For every changed function:

- values moved/borrowed/cloned;
- allocation count and bound;
- collection passes and complexity;
- deterministic order;
- borrow scopes;
- errors and preserved context.

### Step 8 — Audit negative space

Ask what must not happen:

- invalid command must not load or save;
- failed domain rule must not change state;
- read-only query must not rewrite;
- old format must not be silently reinterpreted;
- private representation must not become public for tests;
- output must not rely on hash order.

### Review in passes

A single linear read misses classes of defects. Use separate passes.

#### Pass 1 — Contract and state space

Compare code with behavior matrices. Look for missing enum cases, silent no-ops, wrong exit policy, and undocumented accepted input.

#### Pass 2 — Ownership and borrowing

Find clones, owned parameters, long mutable borrows, returned references, and allocations. Ask whether each matches lifecycle rather than merely satisfying the compiler.

#### Pass 3 — Failure and mutation

Mark every `?`, mutation, file operation, and output operation. Verify failure state at each point.

#### Pass 4 — Determinism and complexity

Inspect hash iteration, sorting, repeated lowercase allocation, nested scans, vector removal, and unnecessary passes. Optimize only where the contract or evidence requires it.

#### Pass 5 — Architecture and visibility

Look for lower layers importing upper concerns, public fields, test-only API, duplicated rules, and files with mixed responsibilities.

#### Pass 6 — Evidence quality

Find untested variants, round-trip-only formats, message-only assertions, shared filesystem fixtures, and docs outside the proof route.

### Compiler-clean bugs

Rust prevents many memory and type errors, but it cannot decide:

- whether `next_id` must exceed maximum ID;
- whether `swap_remove` violates output order;
- whether a parse error should preserve line number;
- whether a command should save after a no-op;
- whether a source error is discarded;
- whether a title limit is bytes or characters;
- whether help exits successfully;
- whether direct overwrite risks data loss.

Treat compiler success as one evidence layer.

### Refactoring safely

A refactor preserves observable behavior. Before moving code:

1. make public behavior tests complete;
2. capture exact canonical bytes and CLI outputs that are contractual;
3. change one responsibility at a time;
4. keep the full proof green;
5. avoid combining refactor with format or feature change unless explicitly reviewed.

### Diff review

Inspect the final diff for:

- newly public items;
- new dependencies/features;
- changed storage bytes;
- removed error context;
- broadened accepted input;
- added clones or allocations;
- deleted tests;
- lint allowances;
- stale docs/help.

### A proof route is reproducible evidence

Run from the course root in a clean copy:

```bash
make course-audit
cargo fmt --all -- --check
cargo check --workspace --all-targets
cargo clippy --workspace --all-targets -- -D warnings
cargo test --workspace --all-targets
cargo test --workspace --doc
cargo doc --workspace --no-deps
cargo build --workspace --release
make capstone-confirm
```

For a reproducible engineering record, note the toolchain version, command, exit status, and checksum of any package you distribute.

### What the route proves

- required files and links exist;
- source formatting is deterministic;
- all declared targets type-check;
- selected lints report no unresolved warnings;
- unit/integration/CLI/doc tests pass;
- API documentation builds;
- optimized compilation succeeds;
- capstone demonstration follows expected behavior.

It does not prove absence of all bugs, security against hostile environments, database-grade crash consistency, optimal performance, or mastery of later Rust topics.

### Clean-checkout discipline

Delete build artifacts or unpack the product package into a new directory. Confirm that:

- no absolute developer path appears;
- all fixtures are committed;
- tests create isolated temporary data;
- no network is needed after toolchain/documentation dependencies are installed;
- commands run from documented working directories;
- generated documentation does not hide unresolved links.

### Mastery defense

You should answer questions selected from:

#### Ownership

- Why does `Task` own its title?
- Why does `find` return `Option<&Task>`?
- Which command values are moved into the board?
- Where could a clone be removed?

#### Modeling

- Which invalid states are unrepresentable?
- Why are priority/status enums rather than strings?
- Which invariant remains runtime-validated?

#### Failure

- Where is physical line context added?
- What remains authoritative after each save failure point?
- Why is missing file not the same as unreadable file?

#### Abstraction

- Why are codecs generic but the board not generic?
- Which explicit lifetime is necessary?
- Why is no repository trait present?

#### Architecture

- Why is the binary thin?
- Which public items can become private?
- Which test proves downstream API usability?

### Do not cargo-cult the layout

The capstone has a command parser, stateful domain, versioned storage, and binary shell. A numerical library, network protocol parser, GUI, or embedded program will need different boundaries. Transfer the questions, not the filenames.

For any new Rust problem, ask:

1. What values exist and who owns them?
2. Which states are valid?
3. Which operations borrow, mutate, or consume?
4. Which inputs are untrusted?
5. Which failures require caller decisions?
6. Where are effects performed?
7. What order and complexity are contractual?
8. What public API should remain stable?
9. What tests independently prove behavior?
10. What remains deliberately outside scope?

### Example: CSV summary tool

The domain may be stateless aggregation rather than persistent entities. It still needs:

- byte/string ownership decisions;
- typed field parsing;
- row/column context;
- streaming versus collection tradeoffs;
- deterministic output;
- generic reader/writer seams;
- binary process policy.

It may need no custom `struct` beyond report types and no storage module.

### Example: in-memory simulation

A simulation may emphasize:

- newtypes for units;
- enums for modes;
- vectors and indexed relationships;
- deterministic stepping;
- invalid parameter errors;
- tests over invariants and conservation laws.

It may have no text parser or CLI initially.

### Readiness for Course 2

Course 2 deepens ownership and memory with smart pointers, RAII patterns, interior mutability, advanced lifetimes, memory representation, pinning foundations, and carefully bounded unsafe reasoning. Advance only when ordinary references, owned collections, and enum-based design no longer feel mysterious.

You should be able to write a small safe-Rust package from a specification without defaulting to:

- global state;
- pervasive clones;
- reference-counted ownership before need;
- public fields;
- stringly states;
- panic-based input handling;
- one universal error string;
- trait abstractions with no substitutes.

### Final transfer exercise

Choose a domain unrelated to task management. In one page, design:

- value/state model;
- ownership map;
- failure vocabulary;
- effect boundaries;
- package/module shape;
- evidence matrix;
- one limitation.

Then implement a 150–300 line safe-Rust library and one thin executable or example. The design should resemble the domain, not the capstone directory.

### Model checkpoint

Before the complete-program example, verify that the model can decide a design rather than merely name its mechanism.

1. **Outcome 1.** For trace a behavioral change through grammar, types, domain rules, persistence, rendering, tests, and documentation, construct one positive and one causal negative example. Mark the first decisive fact in the **whole-program invariant map** and state which evidence could falsify the claim.

2. **Outcome 2.** For preserve failure atomicity, deterministic behavior, and public invariants while refactoring across architectural layers, construct one positive and one causal negative example. Mark the first decisive fact in the **whole-program invariant map** and state which evidence could falsify the claim.

3. **Outcome 3.** For review unfamiliar Rust for ownership workarounds, swallowed errors, invalid-state models, and missing evidence, construct one positive and one causal negative example. Mark the first decisive fact in the **whole-program invariant map** and state which evidence could falsify the claim.

4. **Outcome 4.** For build a closed-book small program and an independent capstone feature from specification only, construct one positive and one causal negative example. Mark the first decisive fact in the **whole-program invariant map** and state which evidence could falsify the claim.

5. **Preservation.** Name one earlier invariant that an easier but less precise implementation could regress.

6. **Boundary.** State one claim this module can justify and one adjacent claim that requires a later course, platform contract, peer behavior, or measurement.

A strong answer records state before and after the operation, the failure path, and the public consequence. An API name by itself is not a model.

## Use the idea in a complete program

The course capstone is **Taskboard**, a persistent command-line task board. Implement an independently selected cross-layer feature and defend the entire path from domain invariant to exit status. This is the transfer proof for Course 1. The exact implementation task is in the [workbook](workbook.md); the full product contract is in the [capstone guide](../capstone.md).

## Practice sequence

1. Reproduce the important examples from this chapter without copying them line for line.
2. Complete the prediction and repair sections in the [workbook](workbook.md).
3. Build the independent [laboratory](../../labs/module-10-inventory-ledger/README.md).
4. Apply the capstone increment.
5. Open the [reasoned solutions](solutions.md) only after recording your own answer.

## Ready to continue

You are ready for Module 11 when you can:

- answer the module question—“Can you make and defend a cross-layer change without tutorial imitation or accidental contract regression?”—without reading the chapter;
- demonstrate this outcome on a fresh example: Trace a behavioral change through grammar, types, domain rules, persistence, rendering, tests, and documentation;
- repair the debugging case while preserving its product requirement;
- complete the laboratory transfer variant and explain the decisive design choice;
- name a simpler alternative and the condition under which you would prefer it.

## Primary Rust references

This chapter is self-contained. These official sources are included for verification and future language updates, not as required reading:

- [The Rust Book: I/O Project](https://doc.rust-lang.org/book/ch12-00-an-io-project.html)
- [Cargo Book: Package layout](https://doc.rust-lang.org/cargo/guide/project-layout.html)

[← Module 9](../module-09-crates-modules-public-apis-tests-and-documentation/index.md) · [one-hundred-module map](../../../COURSE_MAP.md) · [Module 11 →](../../../02-rust-ownership-lifetimes-memory/course-book/module-11-places-move-paths-and-advanced-borrowing/index.md)

## Continue

Continue to [Module 11 — Places, Move Paths, and Advanced Borrowing](../../../02-rust-ownership-lifetimes-memory/course-book/module-11-places-move-paths-and-advanced-borrowing/index.md) after completing the workbook, independent laboratory, capstone increment, and closed-book explanation for this module.
