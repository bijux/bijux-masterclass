# Laboratory 7 — Versioned Record Codec

**Course 1 · Module 7: Errors, Parsing, Files, and Persistence**

[Chapter](../../course-book/module-07-errors-parsing-files-and-persistence/index.md) · [Workbook](../../course-book/module-07-errors-parsing-files-and-persistence/workbook.md) · [Taskboard guide](../../course-book/capstone.md) · [Program method](../../../START_HERE.md#laboratory-method)

## Why this laboratory exists

The laboratory isolates one decision from **Errors, Parsing, Files, and Persistence**: Which failures are part of the product contract, where are they detected, and what state is visible after failure? The product must make **Distinguish absence, recoverable failure, invariant violation, process failure, and ordinary values** visible through its public behavior, failure state, and tests rather than through explanatory comments alone.

Work from `starter/` with a **error map** beside the code. Preserve the first failing case and your original design before reading `solution/`; the reference is a comparison surface, not a sequence of missing lines.

## Learning target

The laboratory asks one focused version of the module’s governing question:

> Which failures are part of the product contract, where are they detected, and what state is visible after failure?

By the end, the answer must be visible in the public API, failure behavior, adversarial tests, and design explanation—not merely in comments.

## Product

### Purpose

Build a complete persistence boundary independent of `taskboard`. The lab proves that you can transfer the method to a new domain rather than reproduce capstone names.

### Domain

An inventory ledger tracks products:

```rust
struct ProductId(u64);

struct Product {
    id: ProductId,
    name: String,
    quantity: u64,
}

struct Ledger {
    products: Vec<Product>,
    next_id: u64,
}
```

Invariants:

- IDs are positive and unique;
- names are 1–80 bytes after trimming;
- names contain neither tabs nor line breaks;
- `next_id` is greater than every existing ID;
- product order in canonical storage is ascending by ID;
- quantities may be zero.

### File format

```text
INVENTORY-V1
NEXT_ID	3
PRODUCT	1	12	Hex bolts
PRODUCT	2	0	Washers
```

Define the complete grammar in the lab README before implementation.

### Required API

```rust
fn decode_product(line: &str) -> Result<Product, RecordError>;
fn load_from<R: BufRead>(reader: R) -> Result<Ledger, StorageError>;
fn save_to<W: Write>(writer: &mut W, ledger: &Ledger) -> Result<(), StorageError>;
fn load(path: &Path) -> Result<Ledger, StorageError>;
fn save(path: &Path, ledger: &Ledger) -> Result<(), StorageError>;
```

### Required failure distinctions

- unsupported or malformed header;
- missing or duplicate `NEXT_ID`;
- missing field;
- extra field;
- invalid product ID;
- invalid quantity;
- invalid name;
- duplicate product ID;
- inconsistent next ID;
- open, read, create, write, flush, sync, and rename failures where observable.

### Behavioral requirements

1. Pure decoding does not access the filesystem.
2. The loader constructs temporary values and returns a ledger only after aggregate validation.
3. A missing path returns an empty ledger under an explicit first-run policy.
4. Any other open failure is retained.
5. Encoding is deterministic and ends with one newline.
6. Saving uses a same-directory temporary file.
7. The target is not rewritten during loading or read-only inspection.
8. Error tests inspect structured variants and context fields.

### Mandatory tests

At minimum:

- empty new ledger round trip;
- three-product round trip;
- exact canonical bytes;
- unsupported version;
- malformed quantity on physical line 4;
- extra field;
- duplicate ID;
- inconsistent next ID;
- missing file policy;
- existing malformed file does not become empty;
- failed decode leaves a preexisting in-memory ledger unchanged in an application-level replacement test.

### Design review

Submit `DESIGN.md` containing:

- grammar;
- invariant ownership by function/type;
- error conversion graph;
- mutation timeline for load and save;
- memory and allocation model;
- exact durability claim;
- limitations deliberately deferred.

### Acceptance

The lab is complete when a reviewer can inject malformed bytes at every grammar position and predict the exact variant and line number, while a successful save-load cycle proves canonical compatibility.

## Working route

1. Read the product contract and run the starter’s baseline checks for **Versioned Record Codec**.
2. Draw the smallest **error map** capable of deciding the governing question.
3. Add a causal negative or adversarial test that fails for the intended relationship.
4. Implement one invariant at a time; after each failure, record state, ownership, cleanup, order, and capacity.
5. Complete the transfer task in a domain unrelated to Taskboard so that syntax cannot substitute for understanding.
6. Compare with `solution/` by contract, proof boundary, and rejected shortcuts before comparing implementation shape.

## Completion check

The laboratory is complete when the required behavior and failure paths pass and you can answer this question without the chapter:

For **Laboratory 7 — Versioned Record Codec**, answer the learning-target question from the completed product. Point to the public boundary that carries the rule, the adversarial case that would falsify it, and one fact the test suite does not establish.

Demonstrate the same mechanism once in the workbook’s unrelated transfer domain. Name one shortcut that would compile or pass the happy path while weakening the product contract.

## Reference comparison

Open [`solution/`](solution/) only after your implementation works or you have written a precise blocker. For **Versioned Record Codec**, compare accepted and rejected inputs, state after failure, ownership or authority, deterministic behavior, public surface, and justified cost before comparing syntax.

## Completion standard

The laboratory is complete when the implementation and tests demonstrate:

- Distinguish absence, recoverable failure, invariant violation, process failure, and ordinary values.
- Design typed errors with context and source preservation rather than flattening failures into strings.
- Parse untrusted text transactionally by tokenizing, converting, validating, and only then committing state.

Also preserve one ordinary success trace, one causal rejection or partial-failure trace, cleanup, deterministic behavior where promised, and one explicit limit on what the tests establish. A happy-path implementation or an explanation that merely names the API is incomplete.

## Independent transfer

Rebuild the decisive relationship from Module 7 in a different product. Change the domain types, names, public behavior, and failure mode while retaining the same **error map**. Defend why your design is simpler than one plausible alternative under the new requirements.
