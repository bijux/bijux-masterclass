# Laboratory 9 — Library Boundary Refactor

This is the independent product for **Course 1, Module 9: Crates, Modules, Public APIs, Tests, and Documentation**. Read the [module chapter](../../course-book/module-09-crates-modules-public-apis-tests-and-documentation/index.md) and complete its [workbook](../../course-book/module-09-crates-modules-public-apis-tests-and-documentation/workbook.md) before consulting the reference implementation.

## Learning target

The laboratory asks one focused version of the module’s governing question:

> Which surfaces are product contracts, which are implementation details, and what independent evidence protects each boundary?

By the end, the answer must be visible in the public API, failure behavior, adversarial tests, and design explanation—not merely in comments.

## Product

### Purpose

Build a package with a reusable library and thin binary. The lab tests architecture, visibility, public documentation, and multi-level evidence.


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

#### Documentation

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

### Architecture defense

Submit a diagram and a public API inventory. For every public item, state the downstream operation requiring it. For every module, state its reason to change and forbidden dependencies.

### Acceptance

The lab fails if tests require public fields, if binary logic duplicates library rules, if output order relies on `HashMap`, or if documentation examples are not executed.

## Working route

Use the common [laboratory method](../../../START_HERE.md#laboratory-method). Work from `starter/`, add the first adversarial test before the design-changing repair, and complete the workbook’s transfer problem before reading the reference implementation.

```bash
cd starter
cargo test
cargo fmt -- --check
cargo clippy -- -D warnings
```

## Completion check

The laboratory is complete when the required behavior and failure paths pass and you can answer this question without the chapter:

> Which surfaces are product contracts, which are implementation details, and what independent evidence protects each boundary?

Demonstrate the same mechanism once in the workbook’s unrelated transfer domain. Name one shortcut that would compile or pass the happy path while weakening the product contract.

## Reference comparison

Open [`solution/`](solution/) only after your implementation works or you have written a precise blocker. For **Library Boundary Refactor**, compare accepted and rejected inputs, state after failure, ownership or authority, deterministic behavior, public surface, and justified cost before comparing syntax.
