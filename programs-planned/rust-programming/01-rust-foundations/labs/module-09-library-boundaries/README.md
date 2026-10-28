# Laboratory 9 — Library Boundary Refactor

**Course 1 · Module 9: Crates, Modules, Public APIs, Tests, and Documentation**

[Chapter](../../course-book/module-09-crates-modules-public-apis-tests-and-documentation/index.md) · [Workbook](../../course-book/module-09-crates-modules-public-apis-tests-and-documentation/workbook.md) · [Taskboard guide](../../course-book/capstone.md) · [Program method](../../../START_HERE.md#laboratory-method)

## Why this laboratory exists

The laboratory isolates one decision from **Crates, Modules, Public APIs, Tests, and Documentation**: Which surfaces are product contracts, which are implementation details, and what independent evidence protects each boundary? The product must make **Distinguish package, crate, target, and module while organizing code by responsibility rather than one file per type** visible through its public behavior, failure state, and tests rather than through explanatory comments alone.

Work from `starter/` with a **module and API map** beside the code. Preserve the first failing case and your original design before reading `solution/`; the reference is a comparison surface, not a sequence of missing lines.

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

1. Read the product contract and run the starter’s baseline checks for **Library Boundary Refactor**.
2. Draw the smallest **module and API map** capable of deciding the governing question.
3. Add a causal negative or adversarial test that fails for the intended relationship.
4. Implement one invariant at a time; after each failure, record state, ownership, cleanup, order, and capacity.
5. Complete the transfer task in a domain unrelated to Taskboard so that syntax cannot substitute for understanding.
6. Compare with `solution/` by contract, proof boundary, and rejected shortcuts before comparing implementation shape.

## Completion check

The laboratory is complete when the required behavior and failure paths pass and you can answer this question without the chapter:

For **Laboratory 9 — Library Boundary Refactor**, answer the learning-target question from the completed product. Point to the public boundary that carries the rule, the adversarial case that would falsify it, and one fact the test suite does not establish.

Demonstrate the same mechanism once in the workbook’s unrelated transfer domain. Name one shortcut that would compile or pass the happy path while weakening the product contract.

## Reference comparison

Open [`solution/`](solution/) only after your implementation works or you have written a precise blocker. For **Library Boundary Refactor**, compare accepted and rejected inputs, state after failure, ownership or authority, deterministic behavior, public surface, and justified cost before comparing syntax.

## Completion standard

The laboratory is complete when the implementation and tests demonstrate:

- Distinguish package, crate, target, and module while organizing code by responsibility rather than one file per type.
- Design private representation and a minimal public API that preserves invariants.
- Choose unit, integration, process, fixture, and documentation tests from the contract under proof.

Also preserve one ordinary success trace, one causal rejection or partial-failure trace, cleanup, deterministic behavior where promised, and one explicit limit on what the tests establish. A happy-path implementation or an explanation that merely names the API is incomplete.

## Independent transfer

Rebuild the decisive relationship from Module 9 in a different product. Change the domain types, names, public behavior, and failure mode while retaining the same **module and API map**. Defend why your design is simpler than one plausible alternative under the new requirements.
