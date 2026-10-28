# Workbook — Module 07: Errors, Parsing, Files, and Persistence

[Return to the chapter](index.md) · [Open the Taskboard engineering guide](../capstone.md) · [Open solutions only after attempting the work](solutions.md)

This workbook tests whether you can use **Errors, Parsing, Files, and Persistence** without relying on surface syntax. Keep the module question in view: *Which failures are part of the product contract, where are they detected, and what state is visible after failure?* For every task, identify the program point where the decisive type, ownership, dispatch, failure, or cost relationship is established. Compile only after committing to a prediction, and preserve the smallest counterexample that changes your model.

## Part 1 — Predict

For each specimen, write a five-part diagnosis: expected outcome; decisive expression or signature; governing rule; smallest requirement-preserving repair; and one tempting change that would compile while weakening the design. Tie every answer to **Errors, Parsing, Files, and Persistence** rather than quoting a diagnostic without explaining its cause.

| # | Specimen | Your prediction |
|---:|---|---|
| 1 | [`01-question-mark-needs-result.rs`](../../compiler-labs/module-07/01-question-mark-needs-result.rs) | Pass or fail? What exact rule decides? |
| 2 | [`02-option-question-mark-in-result.rs`](../../compiler-labs/module-07/02-option-question-mark-in-result.rs) | Pass or fail? What exact rule decides? |
| 3 | [`03-error-source-type.rs`](../../compiler-labs/module-07/03-error-source-type.rs) | Pass or fail? What exact rule decides? |
| 4 | [`04-use-after-partial-parse-move.rs`](../../compiler-labs/module-07/04-use-after-partial-parse-move.rs) | Pass or fail? What exact rule decides? |
| 5 | [`05-writer-must-be-mutable.rs`](../../compiler-labs/module-07/05-writer-must-be-mutable.rs) | Pass or fail? What exact rule decides? |
| 6 | [`06-swallowed-error.rs`](../../compiler-labs/module-07/06-swallowed-error.rs) | Pass or fail? What exact rule decides? |

Run all specimens for this course from the course root with:

```bash
python3 ../tools/run_compiler_labs.py 01-rust-foundations
```

## Part 2 — Diagnose and repair


A junior implementation appears convenient:

```rust
fn load_board(path: &Path, board: &mut TaskBoard) -> bool {
    let text = match std::fs::read_to_string(path) {
        Ok(text) => text,
        Err(_) => return true,
    };

    for line in text.lines() {
        let fields: Vec<_> = line.split('|').collect();
        if fields.len() != 4 {
            continue;
        }
        let id = fields[0].parse::<u64>().unwrap_or(0);
        let status = fields[1].to_owned();
        let priority = fields[2].to_owned();
        let title = fields[3].to_owned();
        board.push_raw(id, status, priority, title);
    }

    true
}
```

### Defect inventory

Identify at least fifteen defects. Your review must include:

- error taxonomy;
- API truthfulness;
- missing-file policy;
- permission and decoding failures;
- format versioning;
- delimiter rules;
- allocation behavior;
- panic or sentinel behavior;
- arbitrary string states;
- duplicate IDs;
- zero IDs;
- partial mutation;
- absent line context;
- unknown extra records;
- aggregate invariants;
- testability.

### Repair constraints

Refactor into these responsibilities:

```rust
fn decode_task(line: &str) -> Result<Task, RecordError>;
fn load_from<R: BufRead>(reader: R) -> Result<TaskBoard, StorageError>;
fn load(path: &Path) -> Result<TaskBoard, StorageError>;
```

Requirements:

1. Only a true not-found open error becomes `TaskBoard::new()`.
2. The format begins with an exact version header.
3. Invalid physical lines report their line number.
4. Unknown status and priority values are errors.
5. Duplicate IDs and inconsistent next-ID metadata are rejected.
6. The destination board is replaced only after complete validation.
7. No source error is discarded when it remains useful.
8. Pure parsing tests need no filesystem.
9. One integration test uses a real temporary directory created with the standard library.

### Clinic: Review questions

After repair, answer:

- Where does the first mutation of the returned board occur?
- Which function knows the path?
- Which function knows the line number?
- Which function enforces cross-record invariants?
- Which errors can the application convert into usage messages?
- What condition still prevents claiming database-grade durability?

## Part 3 — Focused exercises

### Access protocol

Attempt every required exercise and commit the attempt before opening `exercise-answers.md`. Mark each as:


Attempt every exercise before reading the answers. Each solution requires tests for at least one success path and every named failure class.

### 1. Classify ten conditions

Classify each as `Option`, `Result`, internal assertion, or outer process policy: missing searched ID, malformed command ID, missing storage file on first run, permission denied, duplicate stored ID, impossible private enum state, broken pipe while printing, user requests help, integer overflow in next-ID allocation, and a failing unit-test assertion.

### 2. Positive task ID

Implement a `TaskId` constructor and parser that distinguish zero from nonnumeric input. Retain the underlying integer parse error.

### 3. Contextual line reader

Implement a helper that maps `io::Result<String>` into a storage error carrying a physical line number and source.

### 4. Transactional integer import

Implement:

```rust
fn append_numbers(input: &[&str], output: &mut Vec<u64>) -> Result<(), ImportError>;
```

On any invalid token, `output` must remain byte-for-byte equivalent to its state before the call.

### 5. Record grammar

Specify and implement a tab-separated `Task` record decoder. Reject missing fields, extra fields, zero IDs, unknown enum tokens, forbidden title characters, and overlong titles.

### 6. Exact error conversion

Create `RecordError`, `StorageError`, and `AppError`. Draw and implement only the justified outward conversions.

### 7. Generic codec

Implement a reader-based loader and writer-based encoder. Test them entirely in memory.

### 8. Missing-file policy

Implement a path-based loader where only `ErrorKind::NotFound` yields a new board. Test a malformed existing file separately.

### 9. Canonical output

Encode tasks in ID order with fixed enum spelling and one final newline. Prove that two boards with identical domain state produce identical bytes.

### 10. Aggregate validation

Given decoded tasks and `next_id`, reject duplicates and any `next_id` not greater than all task IDs. Explain the empty-board rule.

### 11. Preserve the old file

Design and implement a same-directory temporary-file save. Document every failure point and the state expected after it. Where deterministic injection is difficult with the standard library, isolate serialization and test it independently.

### 12. Error-contract review

Audit the capstone. Produce a table containing operation, success proof, error variants, preserved context, mutation timing, recovery owner, and tests. Identify one error distinction the CLI intentionally presents with the same exit status but retains internally.



## Part 4 — Independent laboratory



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

### Tiered hints

Do not open a later tier until the previous tier has produced a written attempt.

- **Hint 1 — concept:** return to the governing question: Which failures are part of the product contract, where are they detected, and what state is visible after failure?
- **Hint 2 — topology:** draw owners/borrows/states/errors before changing syntax; identify the one boundary that should own the invariant.
- **Hint 3 — structure:** separate validation from mutation and pure transformation from effects. Use the standard operation that encodes the safety fact before inventing an abstraction.
- **Hint 4 — implementation-adjacent:** consult only the relevant standard-library or Reference page; do not open `solution/src`.

The executable starter and reference implementation are in [module-07-record-codec](../../labs/module-07-record-codec/README.md). Implement from the contract first. Compare with the reference only after your tests pass or you have written a precise blocker.

## Part 5 — Capstone transfer

### Outcomes mapped

- Distinguish absence, recoverable failure, invariant violation, process failure, and ordinary values.
- Design typed errors with context and source preservation rather than flattening failures into strings.
- Parse untrusted text transactionally by tokenizing, converting, validating, and only then committing state.
- Build generic buffered reader and writer boundaries that preserve precise line-level diagnostics and source errors.
- State the exact persistence guarantee of a temporary-file-and-rename protocol, including what it does not guarantee across platforms, crashes, and concurrent writers.


### Objective

Replace any provisional storage with a versioned, validated, deterministic persistence boundary. Do not change command semantics merely to simplify storage.

### Required format

The capstone uses:

```text
TASKBOARD-V1
NEXT_ID	4
TASK	1	todo	high	Repair parser
TASK	3	done	normal	Write tests
```

Titles cannot contain tabs or line breaks, so no escaping layer is required in Course 1. That restriction must be enforced at task construction and restoration.

### Required functions

The code should expose responsibilities equivalent to:

```rust
pub fn load(path: &Path) -> Result<TaskBoard, StorageError>;
pub fn load_from<R: BufRead>(reader: R) -> Result<TaskBoard, StorageError>;
pub fn save(path: &Path, board: &TaskBoard) -> Result<(), StorageError>;
pub fn save_to<W: Write>(
    writer: &mut W,
    board: &TaskBoard,
) -> Result<(), StorageError>;
```

Concrete visibility may be narrower if only the crate needs a helper.

### Invariant allocation

| Invariant | Owner |
|---|---|
| title syntax and length | `Task` constructor/restorer |
| status and priority spelling | typed enum parser |
| exact record field count | record decoder |
| physical line context | board decoder |
| unique IDs and next-ID consistency | `TaskBoard::restore` |
| missing-file policy | path-based `load` |
| deterministic byte order | `save_to` |
| target replacement | path-based `save` |

### Application order

For a mutating command:

1. parse the command;
2. load a fully valid board;
3. execute the domain transition;
4. save only after successful mutation;
5. render success only after save succeeds.

For `list`, `search`, and `stats`, do not rewrite storage.

### Required tests

- valid fixture loads expected IDs, states, priorities, and next ID;
- exact canonical fixture is reproduced by `save_to`;
- round trip preserves board equality;
- invalid header has its own variant;
- invalid line reports actual physical line;
- duplicate ID is rejected;
- invalid `NEXT_ID` is rejected;
- nonexistent path becomes a new board;
- malformed existing path is not swallowed;
- CLI mutation persists only after domain success;
- read-only command does not change file bytes or modification behavior where portable observation is available.

### Capstone: Review questions
Before moving to Module 8, trace one malformed file from `File::open` through the line decoder, aggregate validator, application error, CLI rendering, and exit status. Identify every ownership transfer and every retained context field.



### Capstone defense

Audit a loader that silently drops malformed records and a saver that overclaims atomicity; repair both contracts and tests.

## Part 6 — Reconstruct and defend

Complete this checkpoint closed-book. Compiler access is allowed only after the prediction portion has been committed.

### Outcome reconstruction

For each outcome, write a claim, one example, one non-example, and one limitation.

- Distinguish absence, recoverable failure, invariant violation, process failure, and ordinary values.
- Design typed errors with context and source preservation rather than flattening failures into strings.
- Parse untrusted text transactionally by tokenizing, converting, validating, and only then committing state.
- Build generic buffered reader and writer boundaries that preserve precise line-level diagnostics and source errors.
- State the exact persistence guarantee of a temporary-file-and-rename protocol, including what it does not guarantee across platforms, crashes, and concurrent writers.

### Closed-book checkpoint

Complete without notes, compiler, or editor. Then verify your answers with small programs.

#### Part A — Classification

For each condition, choose `Option`, `Result`, panic/assertion, or normal command outcome and justify it:

1. search finds no matching title;
2. `done 41` names no task;
3. a status token is `finished` rather than `done`;
4. a private constructor produces an impossible zero ID;
5. the first-run storage path does not exist;
6. the storage path is unreadable because of permissions;
7. help was requested;
8. stdout reports a broken pipe;
9. a unit-test equality assertion fails;
10. next-ID allocation overflows.

#### Part B — Propagation

Explain this line precisely:

```rust
let board = storage::load(path)?;
```

Your answer must name:

- the called function's success and error types;
- the enclosing function that returns early;
- any conversion required;
- what code does not run on error;
- what `?` does not do.

#### Part C — Parsing pipeline

Write the four validation stages and place each check:

- `u64` lexical syntax;
- nonzero ID;
- five record fields;
- known status spelling;
- title delimiter rule;
- duplicate ID;
- next ID greater than maximum;
- supported version.

#### Part D — Transactional reasoning

Given a board with two tasks and an input file whose third task line is invalid, state every mutation that may occur under a correct loader. Then contrast it with a push-as-you-parse loader.

#### Part E — I/O architecture

Reconstruct signatures for path-based and generic reader/writer load/save functions. Explain why path context belongs only in some errors.

#### Part F — Storage proof

List ten tests needed to claim a versioned format is implemented. At least four must be corruption tests, one must inspect exact bytes, and one must prove old-state preservation.

#### Pass standard

Pass requires:

- 90% classification accuracy;
- exact explanation of `?`;
- no confusion between parse stages;
- a correct load-validate-commit account;
- a bounded durability claim;
- no use of “just catch everything” as a recovery design.

Failure on transactional mutation or missing-file policy requires repeating the module lab before Module 8.

### Transfer defense

Audit a loader that silently drops malformed records and a saver that overclaims atomicity; repair both contracts and tests.

Your answer must include:
