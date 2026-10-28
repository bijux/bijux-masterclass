# Workbook — Module 10: Integration and Independent Change

[Return to the chapter](index.md) · [Open the Taskboard engineering guide](../capstone.md) · [Open solutions only after attempting the work](solutions.md)

This workbook tests whether you can use **Integration and Independent Change** without relying on surface syntax. Keep the module question in view: *Can you make and defend a cross-layer change without tutorial imitation or accidental contract regression?* For every task, identify the program point where the decisive type, ownership, dispatch, failure, or cost relationship is established. Compile only after committing to a prediction, and preserve the smallest counterexample that changes your model.

## Part 1 — Predict

For each specimen, write a five-part diagnosis: expected outcome; decisive expression or signature; governing rule; smallest requirement-preserving repair; and one tempting change that would compile while weakening the design. Tie every answer to **Integration and Independent Change** rather than quoting a diagnostic without explaining its cause.

| # | Specimen | Your prediction |
|---:|---|---|
| 1 | [`01-move-into-command.rs`](../../compiler-labs/module-10/01-move-into-command.rs) | Pass or fail? What exact rule decides? |
| 2 | [`02-shared-view-blocks-mutation.rs`](../../compiler-labs/module-10/02-shared-view-blocks-mutation.rs) | Pass or fail? What exact rule decides? |
| 3 | [`03-iterator-terminal-consumes.rs`](../../compiler-labs/module-10/03-iterator-terminal-consumes.rs) | Pass or fail? What exact rule decides? |
| 4 | [`04-generic-sort-bound.rs`](../../compiler-labs/module-10/04-generic-sort-bound.rs) | Pass or fail? What exact rule decides? |
| 5 | [`05-incompatible-iterator-branches.rs`](../../compiler-labs/module-10/05-incompatible-iterator-branches.rs) | Pass or fail? What exact rule decides? |
| 6 | [`06-local-rendered-output.rs`](../../compiler-labs/module-10/06-local-rendered-output.rs) | Pass or fail? What exact rule decides? |

Run all specimens for this course from the course root with:

```bash
python3 ../tools/run_compiler_labs.py 01-rust-foundations
```

## Part 2 — Diagnose and repair


A feature branch adds `rename <id> <title>`. It compiles and its one happy-path test passes. The diff includes:

```rust
pub struct Task {
    pub id: u64,
    pub title: String,
    pub status: String,
}

pub fn rename(board: &mut TaskBoard, args: &[String], path: &Path) -> bool {
    let id = args[0].parse::<u64>().unwrap();
    let title = args[1..].join(" ");

    for task in &mut board.tasks {
        if task.id == id {
            task.title = title.clone();
            let _ = storage::save(path, board);
            return true;
        }
    }

    false
}
```

Storage writing now appends the title as a sixth field but retains `TASKBOARD-V1`. Help text and README are unchanged.

### Required audit

Find at least twenty-five defects across:

- argument bounds and panic behavior;
- typed ID and zero handling;
- title validation and delimiter compatibility;
- ownership and cloning;
- public representation;
- stringly status;
- direct collection access;
- state mutation before save;
- ignored save error;
- Boolean error collapse;
- output/exit policy;
- format-version compatibility;
- old fixture behavior;
- read-only/mutation classification;
- test gaps;
- documentation drift;
- module responsibility;
- clean-checkout proof.

### Repair specification

`rename <id> <title>` must:

1. reject missing ID/title and extra grammar ambiguity through `CommandError`;
2. parse a positive `TaskId`;
3. validate title under existing storage rules;
4. preserve the old task title on validation failure;
5. update exactly one existing task;
6. report unknown IDs distinctly;
7. save only after a successful domain mutation;
8. propagate save failure and avoid printing success;
9. require no storage-format change because title already exists;
10. update help, README, docs, and all test layers.

### Deliverables

- behavior matrix;
- impact matrix;
- repaired implementation;
- model, command, integration, persistence-regression, documentation, and CLI tests;
- ownership/cost note;
- final diff review.

Do not solve by making a universal `rename` utility or exposing fields for tests.

## Part 3 — Focused exercises

### Access protocol

Attempt every required exercise and commit the attempt before opening `exercise-answers.md`. Mark each as:


### 1. Invariant map

Produce a complete map of capstone invariants, owner functions/types, preservation operations, failure variants, and proving tests.

### 2. End-to-end trace

Trace `add high "Repair parser"` from shell token ownership through command, board, storage, output, and process status. Include every allocation and fallible boundary.

### 3. Behavior matrix

Write full matrices for `start`, `done`, `reopen`, and `remove`, including malformed IDs, missing storage, corrupt storage, unknown IDs, illegal states, save failure, and output failure.

### 4. Independent `rename` feature

Implement the debugging-clinic specification from tests first. Do not alter storage version.

### 5. Query feature

Implement `list priority <low|normal|high>` or an equivalent independently specified query. Prove it is read-only, deterministic, and performs no unnecessary title cloning.

### 6. Transactional batch operation

Design `complete-all <query>` so either every matched task can legally complete and all do, or none change. Specify no-match behavior and persistence semantics.

### 7. Format evolution plan

Without implementing it, design a version 2 adding creation timestamps. State timestamp type/ownership, encoding, version detection, version-1 policy, migration strategy, canonical order, and tests. Do not assume a time crate or timezone policy without naming it.

### 8. Semantic bug hunt

Review the entire capstone for ten compiler-clean risks: order, overflow, line numbers, UTF-8 byte/character policy, save commit, output failure, no-op rewrites, source chains, temporary collisions, and public evolution.

### 9. Refactor

Change the internal task collection traversal or module organization without changing public imports, storage bytes, CLI output, or tests at external boundaries. Explain which unit tests legitimately changed.

### 10. Clean-package proof

Package the completed product, unpack it elsewhere, run its documented Cargo proof routes, and produce a SHA-256 inventory. Record unavailable tools honestly rather than converting missing execution into a pass.

### 11. Oral defense

Answer twenty randomized questions spanning all ten modules in under forty minutes. Each answer must include one code-level example or signature.

### 12. Transfer project

Build a 150–300 line safe-Rust program in an unrelated domain, with typed state, error boundary, tests, docs, and thin shell. Submit a comparison explaining which capstone patterns were reused and which were rejected.



## Part 4 — Independent laboratory



### Purpose

Build a separate safe-Rust application from a behavioral specification only. Do not copy taskboard module names blindly. The lab is the final transfer test.

### Product

A local lending ledger tracks items and loans:

```text
ledger add-item "The Rust Book"
ledger register "Mina"
ledger lend <item-id> <member-id>
ledger return <item-id>
ledger list available
ledger list loaned
ledger member <member-id>
ledger stats
```

### Required domain rules

- item and member IDs are positive newtypes and unique in their collections;
- names/titles are trimmed, bounded, and delimiter-safe;
- an item is either available or loaned to exactly one member;
- only available items can be lent;
- only loaned items can be returned;
- member views list loans in item-ID order;
- all public reports are deterministic;
- ID allocation detects exhaustion;
- invalid operations preserve state.

### Persistence

Design one versioned text format with explicit grammar. It must store members, items, loan state, and next-ID metadata. The loader validates cross-record references: every loaned member ID must exist. Construct complete temporary state before returning a ledger.

Saving uses a same-directory temporary file and canonical ordering. Document the exact durability boundary.

### Architecture

Choose modules from responsibilities. A likely shape includes domain, command, storage, application, and binary, but combining domain files or separating member/item logic may be better. Submit a dependency graph before code.

### Independent extension

After the base proof passes, add one feature selected from:

- remove member only when no active loans;
- search item titles;
- rename member;
- list overdue items using an injected date value rather than hidden current time.

Write behavior and impact matrices before implementation.

### Acceptance defense

Explain:

- ownership of names, titles, and report views;
- why loan state is modeled as it is;
- how cross-record validation works;
- failure state at every save stage;
- generic I/O bounds;
- lifetime annotations, if any;
- public API inventory;
- complexity of list/search/stats;
- evidence limitations.

The lab fails if it uses string statuses, public mutable fields, panic-based input parsing, partial-load mutation, non-deterministic output, or an untested storage grammar.

### Tiered hints

Do not open a later tier until the previous tier has produced a written attempt.

- **Hint 1 — concept:** return to the governing question: Can you make and defend a cross-layer change without tutorial imitation or accidental contract regression?
- **Hint 2 — topology:** draw owners/borrows/states/errors before changing syntax; identify the one boundary that should own the invariant.
- **Hint 3 — structure:** separate validation from mutation and pure transformation from effects. Use the standard operation that encodes the safety fact before inventing an abstraction.
- **Hint 4 — implementation-adjacent:** consult only the relevant standard-library or Reference page; do not open `solution/src`.

The executable starter and reference implementation are in [module-10-inventory-ledger](../../labs/module-10-inventory-ledger/README.md). Implement from the contract first. Compare with the reference only after your tests pass or you have written a precise blocker.

## Part 5 — Capstone transfer

### Outcomes mapped

- Trace a behavioral change through grammar, types, domain rules, persistence, rendering, tests, and documentation.
- Preserve failure atomicity, deterministic behavior, and public invariants while refactoring across architectural layers.
- Review unfamiliar Rust for ownership workarounds, swallowed errors, invalid-state models, and missing evidence.
- Build a closed-book small program and an independent capstone feature from specification only.
- Defend design choices, rejected alternatives, known limitations, and verification boundaries with concrete evidence.


### Part 1 — Independent feature

Implement `rename <id> <title>` from this behavioral contract:

- ID must be a positive typed value;
- title is formed from remaining argument tokens;
- the same title invariants used by `add` apply;
- unknown ID and invalid title are distinct errors;
- failure leaves the board and file unchanged;
- success changes only the title and saves once;
- storage remains version 1 because the field already exists;
- list/search output reflects the new title immediately;
- help, command reference, docs, and tests are updated.

No implementation recipe is supplied. Begin with behavior and impact matrices.

### Part 2 — Whole-program audit

Produce `FINAL_AUDIT.md` covering:

1. invariant ownership;
2. move/borrow/clone inventory for every public operation;
3. error conversion/source graph;
4. parsing stages and line context;
5. collection complexity and deterministic order;
6. storage grammar and failure atomicity;
7. public API and visibility;
8. test boundary matrix;
9. documentation proof;
10. known limitations and later-course topics.

### Part 3 — Regression bug hunt

Seed or inspect at least five bugs from these classes:

- line-number offset;
- swallowed save error;
- hash-order output;
- transition state changed before validation;
- stale help/doc example;
- title clone that can move;
- missing-file policy swallowing permission error;
- incorrect next-ID restore rule.

For each, add a regression test before repair.

### Part 4 — Release proof

Required commands:

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

Then archive only `programs/rust-programming/`, unpack elsewhere, and rerun the available proof. Generate an inventory with SHA-256 hashes.

### Part 5 — Defense

Answer twenty questions sampled from the mastery defense bank. At least five must require predicting code without compiler access, five must concern failure state, and five must require architectural tradeoffs.



### Capstone defense

Implement an unseen command across every taskboard layer, add adversarial tests, and explain the ownership and failure model without running the code.

## Part 6 — Reconstruct and defend

Complete this checkpoint closed-book. Compiler access is allowed only after the prediction portion has been committed.

### Outcome reconstruction

For each outcome, write a claim, one example, one non-example, and one limitation.

- Trace a behavioral change through grammar, types, domain rules, persistence, rendering, tests, and documentation.
- Preserve failure atomicity, deterministic behavior, and public invariants while refactoring across architectural layers.
- Review unfamiliar Rust for ownership workarounds, swallowed errors, invalid-state models, and missing evidence.
- Build a closed-book small program and an independent capstone feature from specification only.
- Defend design choices, rejected alternatives, known limitations, and verification boundaries with concrete evidence.

### Closed-book checkpoint

Complete in a fresh session without notes.

#### Section 1 — Prediction

Predict every case before compiling, then revisit each incorrect prediction until you can name the governing rule. For each failure, name the rule and a design-preserving repair.

#### Section 2 — Architecture reconstruction

From memory, draw:

- package targets;
- module dependency graph;
- public re-export facade;
- command-to-output data flow;
- storage load and save flows;
- error conversion graph.

#### Section 3 — Invariant defense

Name at least twelve invariants and their authoritative owner. Explain why no parser-only check is sufficient for domain invariants.

#### Section 4 — Failure-state table

For malformed command, corrupt file, unknown ID, illegal transition, serialization failure, write failure, rename failure, and stdout failure, state:

- whether board memory changed;
- whether target file changed or may have changed;
- whether success output occurred;
- whether retry is safe;
- error category and retained context.

#### Section 5 — Independent design

Given a new requirement, produce behavior and impact matrices, signatures, error changes, tests, and documentation plan in forty-five minutes. No code is required until the design is reviewed.

#### Section 6 — Transfer

Design a small unrelated Rust program with:

- owned state model;
- one borrowed query;
- one fallible transition;
- one generic standard-library boundary;
- unit and integration evidence;
- no unnecessary custom trait.

#### Passing rule

- compiler prediction at least 89%;
- ownership/borrowing defense at least 80%;
- state/failure defense at least 80%;
- complete independent feature;
- clean public architecture;
- deterministic compatible persistence;
- all executable proof routes available in the local environment pass;
- limitations are reported without exaggeration.

### Transfer defense

Implement an unseen command across every taskboard layer, add adversarial tests, and explain the ownership and failure model without running the code.

Your answer must include:
