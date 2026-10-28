# Workbook — Module 09: Crates, Modules, Public APIs, Tests, and Documentation

[Chapter](index.md) · [Laboratory](../../labs/module-09-library-boundaries/README.md) · [Taskboard guide](../capstone.md) · [Solutions](solutions.md)

This workbook tests whether **Crates, Modules, Public APIs, Tests, and Documentation** has become a usable model rather than remembered vocabulary. Its governing question is: *Which surfaces are product contracts, which are implementation details, and what independent evidence protects each boundary?* Preserve your first prediction and record decisive facts in a **module and API map**. A repair succeeds only when it keeps the difficult product requirement visible.

## Retrieval warm-up

Before compiling or running anything:

1. Restate the invariant from Module 8 — Generics, Traits, Conversions, and Lifetime Basics that today’s mechanism must preserve.
2. Rewrite the governing question in your own words: **Which surfaces are product contracts, which are implementation details, and what independent evidence protects each boundary?**
3. Draw the smallest **module and API map** that could decide one positive and one negative case.
4. Name one shortcut that could make the visible example pass while deleting ownership, failure, ordering, capacity, safety, compatibility, or evidence required by the product.

## Part 1 — Predict

For each specimen, write a five-part diagnosis: expected outcome; decisive expression or signature; governing rule; smallest requirement-preserving repair; and one tempting change that would compile while weakening the design. Tie every answer to **Crates, Modules, Public APIs, Tests, and Documentation** rather than quoting a diagnostic without explaining its cause.

| # | Specimen | Your prediction |
|---:|---|---|
| 1 | [`01-private-library-item.rs`](../../compiler-labs/module-09/01-private-library-item.rs) | Pass or fail? What exact rule decides? |
| 2 | [`02-public-type-private-field.rs`](../../compiler-labs/module-09/02-public-type-private-field.rs) | Pass or fail? What exact rule decides? |
| 3 | [`03-reexport-path.rs`](../../compiler-labs/module-09/03-reexport-path.rs) | Pass or fail? What exact rule decides? |
| 4 | [`04-integration-crate-root.rs`](../../compiler-labs/module-09/04-integration-crate-root.rs) | Pass or fail? What exact rule decides? |
| 5 | [`05-doctest-question-mark-context.rs`](../../compiler-labs/module-09/05-doctest-question-mark-context.rs) | Pass or fail? What exact rule decides? |
| 6 | [`06-public-field-invariant-hole.rs`](../../compiler-labs/module-09/06-public-field-invariant-hole.rs) | Pass or fail? What exact rule decides? |

Run all specimens for this course from the course root with:

```bash
python3 ../tools/run_compiler_labs.py 01-rust-foundations
```

## Part 2 — Diagnose and repair

You inherit:

```text
src/main.rs              1,900 lines
src/utils.rs               700 lines
```

Every struct field and helper is `pub`. `main` reads environment variables, parses commands, mutates task vectors, writes files directly, formats output, and calls `process::exit` from several branches. Tests import `utils::*` and assert exact helper call sequences. Documentation contains examples copied from an older API but no doc-test route.

### Defect inventory

Identify at least twenty defects under these headings:

- package/target architecture;
- invariant ownership;
- dependency direction;
- visibility;
- error and exit policy;
- filesystem isolation;
- test boundaries;
- brittle implementation assertions;
- documentation drift;
- lint policy;
- fixture reproducibility;
- module cohesion.

### Required refactor

Produce a package no more fragmented than:

```text
src/
├── lib.rs
├── model.rs
├── command.rs
├── storage.rs
├── app.rs
└── main.rs

tests/
├── public_behavior.rs
├── persistence.rs
└── cli.rs
```

Requirements:

1. `main.rs` contains no domain transition rules or storage grammar.
2. private fields remain private.
3. the crate root re-exports only the intended product vocabulary.
4. storage codecs are testable in memory.
5. integration tests use only public API.
6. CLI tests isolate their path and inspect process behavior.
7. rustdoc examples compile.
8. the complete proof route starts from the package root.
9. no lint is suppressed globally merely to finish the refactor.
10. every source file has one coherent reason to change.

### Clinic: Architecture defense

Draw the dependency graph and answer:

- Why does `storage` depend on `model`, not the reverse?
- Why is `app` allowed to depend on both command and storage?
- What is the smallest public entry point needed by the binary?
- Which tests are allowed to inspect private parsing helpers?
- Which behavior is proven only by launching the binary?
- Which future change can occur without changing downstream import paths because of re-exports?

## Part 3 — Focused exercises

### Access protocol

Attempt every required exercise and commit the attempt before opening `exercise-answers.md`. Mark each as:

### 1. Vocabulary map

For ten artifacts in the course workspace, label package, crate, target, module, path, or item. Include the capstone library, capstone binary, one integration test, one lab solution, `model.rs`, and `TaskBoard::add`.

### 2. Module dependency graph

Draw the capstone graph. Reject any edge from model to command, storage, app, or binary. Explain each remaining edge.

### 3. Visibility audit

List every public item in the capstone. For each, provide a downstream use case, invariant impact, documentation status, and whether narrower visibility works.

### 4. Validated mutation API

Replace public `Task` fields with accessors and validated methods. Prove external code cannot create an illegal title or transition by assignment.

### 5. Re-export facade

Make internal module paths private while exposing a coherent crate-root vocabulary. Write an integration test that imports only from the root.

### 6. Thin binary

Reduce `main.rs` to environment adaptation, library invocation, stream output, and exit policy. No business-rule branch may remain.

### 7. Test placement matrix

For twenty capstone behaviors, choose unit, integration, documentation, or CLI tests and justify the narrowest sufficient boundary.

### 8. Corruption suite

Build table-driven storage tests covering every grammar field, physical line context, duplicate metadata, and aggregate invariant.

### 9. Executable docs

Write crate-level docs and item-level docs for `TaskBoard`, `TaskBoard::add`, and `storage::load`. Include examples and accurate error sections.

### 10. Manifest review

Explain every field in the package and workspace manifests. Remove any unused feature, dependency, target declaration, profile override, or lint exception.

### 11. Clean-checkout proof

Write one shell route that runs structural audits, formatting, check, Clippy, all tests, docs, and a release build. It must not depend on local untracked files.

### 12. Refactoring-resilience test

Change a private helper name and internal collection traversal. Prove public integration and CLI tests remain unchanged while unit tests change only where they intentionally cover representation.

### Interleaved reasoning pass

1. For **Distinguish package, crate, target, and module while organizing code by responsibility rather than one file per type**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the module and API map.
2. For **Design private representation and a minimal public API that preserves invariants**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the module and API map.
3. For **Choose unit, integration, process, fixture, and documentation tests from the contract under proof**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the module and API map.
4. For **Write rustdoc examples that teach and execute, and maintain a deliberate warning/lint policy**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the module and API map.

5. Identify one guarantee from an earlier course that a careless implementation of **Crates, Modules, Public APIs, Tests, and Documentation** could regress.

For one case, write both a principled repair and a weaker repair that appears to work. The principled repair must preserve the requirement; the weaker repair must name the information, state, bound, or compatibility promise it silently discards.

## Part 4 — Independent laboratory

### Purpose

Build a package with a reusable library and thin binary. The lab tests architecture, visibility, public documentation, and multi-level evidence.

### Product

`text-index` reads plain-text documents, builds a word-to-document index, and supports:

```text
text-index add <path>
text-index search <word>
text-index stats
```

The lab may keep state in memory for one process. Persistence is optional only if fully specified; do not copy the capstone format mechanically.

### Required package shape

```text
src/
├── lib.rs
├── model.rs
├── tokenize.rs
├── app.rs
└── main.rs

tests/
├── public_behavior.rs
└── cli.rs
```

A different shape is allowed when the responsibility graph is documented and no file is trivial fragmentation.

### Domain requirements

- document IDs are validated newtypes;
- document paths use `PathBuf`;
- tokens are normalized under an explicitly documented ASCII policy;
- index representation is private;
- search results have deterministic path order;
- duplicate document paths are rejected;
- empty query tokens are errors.

### Public API

Expose only what a downstream caller needs to create an index, add text/path metadata, search, and inspect statistics. Internal tokenization helpers remain private unless they form a coherent supported API.

### Testing requirements

#### Unit

- tokenization boundaries;
- duplicate detection;
- deterministic ordering;
- empty/large input;
- exact statistics.

#### Integration

- add two documents and search through public API;
- invalid input preserves index state;
- public imports come only from crate root.

#### Documentation tests

- crate-level end-to-end example;
- `Index::add` example and error documentation;
- `Index::search` borrowing behavior.

#### CLI

- help success;
- unknown command failure;
- add missing path failure;
- search output and exit status using isolated files.

### Tooling requirements

- `cargo fmt --check` passes;
- Clippy warnings are denied;
- all targets and docs test;
- release build succeeds;
- no third-party dependencies;
- README includes one clean-checkout proof route.

### Laboratory: Architecture defense

Submit a diagram and a public API inventory. For every public item, state the downstream operation requiring it. For every module, state its reason to change and forbidden dependencies.

### Acceptance

The lab fails if tests require public fields, if binary logic duplicates library rules, if output order relies on `HashMap`, or if documentation examples are not executed.

### Tiered hints

Do not open a later tier until the previous tier has produced a written attempt.

- **Hint 1 — concept:** return to the governing question: Which surfaces are product contracts, which are implementation details, and what independent evidence protects each boundary?
- **Hint 2 — topology:** draw owners/borrows/states/errors before changing syntax; identify the one boundary that should own the invariant.
- **Hint 3 — structure:** separate validation from mutation and pure transformation from effects. Use the standard operation that encodes the safety fact before inventing an abstraction.
- **Hint 4 — implementation-adjacent:** consult only the relevant standard-library or Reference page; do not open `solution/src`.

The executable starter and reference implementation are in [module-09-library-boundaries](../../labs/module-09-library-boundaries/README.md). Implement from the contract first. Compare with the reference only after your tests pass or you have written a precise blocker.

### Laboratory acceptance trace

Before opening the reference implementation for **Library Boundary Refactor**, record:

- the public behavior that demonstrates **Distinguish package, crate, target, and module while organizing code by responsibility rather than one file per type**;
- one adversarial input, state transition, schedule, peer action, workload, or build condition appropriate to this module;
- the exact state after rejection or partial failure;
- ownership and cleanup;
- ordering and capacity;
- one shortcut deliberately excluded by the contract;
- one claim the tests cannot establish.

## Part 5 — Capstone transfer

### Outcomes mapped

- Distinguish package, crate, target, and module while organizing code by responsibility rather than one file per type.
- Design private representation and a minimal public API that preserves invariants.
- Choose unit, integration, process, fixture, and documentation tests from the contract under proof.
- Write rustdoc examples that teach and execute, and maintain a deliberate warning/lint policy.
- Separate a thin effectful binary shell from a testable library core.

### Target source structure

```text
capstone/
├── Cargo.toml
├── README.md
├── src/
│   ├── lib.rs
│   ├── model.rs
│   ├── command.rs
│   ├── storage.rs
│   ├── app.rs
│   └── main.rs
└── tests/
    ├── public_behavior.rs
    ├── persistence.rs
    └── cli.rs
```

Combine files if one has no coherent responsibility; do not add more without a clear dependency boundary.

### Public facade

`lib.rs` should:

- contain crate-level docs;
- declare private modules;
- re-export primary domain/application types;
- avoid exposing storage record internals;
- provide the smallest entry point needed by the binary and external tests.

### Binary constraint

`main.rs` may:

- read arguments and `TASKBOARD_FILE`;
- call the library;
- write stdout/stderr;
- select process exit status.

It may not parse storage records, validate titles, implement transitions, or mutate task collections directly.

### Test matrix
| Contract | Primary evidence |
|---|---|
| title/status/ID invariants | model unit tests |
| command grammar | command unit tests |
| file grammar and canonical bytes | storage unit + persistence tests |
| public workflow | integration test |
| API usability | rustdoc tests |
| exit status/streams/environment path | CLI tests |
| no forbidden production constructs | policy audit |
| complete build/lint/test/docs route | root Make proof |

### Capstone documentation

Required:

- crate-level architecture and quick example;
- public type/method docs with errors and ownership;
- capstone README with commands, storage contract, failure policy, and proof commands;
- no stale example using internal paths.

### Review questions
Run the complete proof route from a fresh copy of only committed course files. Then rename a private helper and change one internal traversal. Public integration, documentation, and CLI tests should continue to pass without edits.

### Capstone defense

Reduce an over-public monolithic CLI to a library with explicit boundaries and build one test at each relevant evidence layer.

### Capstone invariant trace

For the Module 9 Taskboard increment, name the changed invariant and its owner before editing code. Follow it through input, validation, state transition, effect, output, failure, cleanup, and tests. Add storage, wire, scheduler, generated-code, compatibility, resource, or measurement consequences when this course makes them relevant. End by naming one earlier guarantee that remains unchanged.

## Part 6 — Reconstruct and defend

Complete this checkpoint closed-book. Compiler access is allowed only after the prediction portion has been committed.

### Outcome reconstruction

For each outcome, write a claim, one example, one non-example, and one limitation.

Without reopening the chapter, reconstruct the outcomes for **Module 09: Crates, Modules, Public APIs, Tests, and Documentation**. Compare your list with the earlier outcome map only after writing it, then mark each item as modelled, predicted, repaired, built, transferred, or still unsupported.

### Closed-book checkpoint

#### Part A — Vocabulary

Define package, crate, target, module, item, and path. Give one capstone example of each. Explain how one package contains both a library and binary crate.

#### Part B — Visibility

1. Explain private-by-default behavior.
2. Contrast `pub`, `pub(crate)`, and a crate-root `pub use`.
3. Explain why public fields can invalidate constructor guarantees.
4. Design visibility for `Task::restore`, used only by storage.
5. State why integration tests cannot access private modules.

#### Part C — Architecture

Draw the model/command/storage/app/library/binary dependency graph. Explain why the model cannot depend on storage and why the binary should not own domain rules.

#### Part D — Test selection

Choose the narrowest appropriate test category for:

- title length boundary;
- public add-and-complete workflow;
- README-like API example;
- CLI unknown command exit code;
- exact storage bytes;
- private record decoder edge case;
- malformed file preservation behavior.

#### Part E — Documentation

Write a complete doc comment outline for a fallible public method: summary, invariants, errors, side effects, example, and relevant links. Explain how the proof route checks it.

#### Part F — Tooling

Write the ordered commands for formatting, check, Clippy, tests, doc tests, docs, and release build. State what each can find that the others cannot.

#### Pass standard

Pass requires:

- exact vocabulary rather than file/module confusion;
- a public surface justified by downstream use;
- correct dependency direction;
- correct test boundary for at least 85% of cases;
- executable documentation understanding;
- no proposal to silence warnings globally.

A capstone with domain logic in `main.rs` cannot pass regardless of test count.

### Transfer defense

Transfer **Module 09: Crates, Modules, Public APIs, Tests, and Documentation** to a product unrelated to the course capstone. Change the domain model and failure mode, preserve the governing relationship, and identify which part of the original design was essential rather than accidental.

Your answer must include:

- the governing rule for **Module 09: Crates, Modules, Public APIs, Tests, and Documentation** in plain language;
- state, ownership, or authority before and after the decisive operation;
- one causal negative case that fails for the intended reason;
- one principled repair and one easier repair that deletes a requirement;
- the limit of the evidence you used;
- one transfer to a product with different data and failure behavior.


### Closed-book defense

In five minutes, answer “Which surfaces are product contracts, which are implementation details, and what independent evidence protects each boundary?” using the **module and API map**. Include one positive case, one causal negative case, one principled repair, one rejected shortcut, and one transfer outside Taskboard. A list of APIs without the deciding relationship is incomplete.
