# Reasoned solutions — Module 07: Errors, Parsing, Files, and Persistence

[Return to the workbook](workbook.md) · [Return to the chapter](index.md) · [Open the Taskboard engineering guide](../capstone.md)

Use these explanations to review your reasoning about **Errors, Parsing, Files, and Persistence**, not to substitute for an attempt. The decisive question is: *Which failures are part of the product contract, where are they detected, and what state is visible after failure?* When your design differs, separate three possibilities: a Rust rule was applied incorrectly, the product contract changed, or two architectures satisfy the same contract with different trade-offs.

## Compiler specimen reasoning

### 1. `01-question-mark-needs-result.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** question mark requires a compatible residual-returning function.
- **Causal explanation:** The compiler rejects the specimen because question mark requires a compatible residual-returning function.
- **Principled repair:** Return a compatible `Result`/`Option` from the function, or handle the failure locally with an explicit branch.
- **Weak repair to reject:** Do not replace `?` with `unwrap` merely to keep the original return type.

### 2. `02-option-question-mark-in-result.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** Option residual is not automatically a Result error.
- **Causal explanation:** The compiler rejects the specimen because option residual is not automatically a Result error.
- **Principled repair:** Convert `None` to a domain error with `ok_or`/`ok_or_else` before using `?`.
- **Weak repair to reject:** Do not invent a meaningless default value for absence.

### 3. `03-error-source-type.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** String does not implement Error and cannot be a source.
- **Causal explanation:** The compiler rejects the specimen because string does not implement Error and cannot be a source.
- **Principled repair:** Use an error type that implements `Error` as the source, or store the string as context rather than a source.
- **Weak repair to reject:** Do not fabricate an unrelated source error to satisfy the trait.

### 4. `04-use-after-partial-parse-move.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** parsing borrows str data; it does not consume String.
- **Causal explanation:** The specimen compiles because parsing borrows str data; it does not consume String.
- **Principled repair:** No repair is required. Preserve the example and explain the exact type, ownership, or visibility rule that permits it.
- **Weak repair to reject:** Do not replace this demonstration—parsing borrows str data; it does not consume String—with broader ownership, visibility, or allocation merely to make the reasoning easier.

### 5. `05-writer-must-be-mutable.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** Write methods require mutable access to writer state.
- **Causal explanation:** The compiler rejects the specimen because write methods require mutable access to writer state.
- **Principled repair:** Accept `&mut W` or take the writer by value when the function must advance writer state.
- **Weak repair to reject:** Do not recreate a writer for every operation or conceal mutation behind global state.

### 6. `06-swallowed-error.rs`

- **Outcome:** `manual-review`
- **Governing rule:** compiles but collapses missing, permission, and corruption policy into empty text.
- **Causal explanation:** The specimen type-checks, but design review must reject the behavior because compiles but collapses missing, permission, and corruption policy into empty text.
- **Principled repair:** Return a typed `Result` and distinguish an intentionally absent file from permission, I/O, and decoding failures.
- **Weak repair to reject:** Do not collapse every failure into empty content or panic on all failures.

## Exercise reasoning and worked answers
These are reference designs, not text to copy before attempting the work. Equivalent designs are valid when they preserve the same distinctions and invariants.

### 1. Classification

| Condition | Representation | Reason |
|---|---|---|
| searched ID absent | `Option<&Task>` at lookup; domain error when a command requires it | absence is ordinary until an operation requires presence |
| malformed command ID | `Result` | untrusted syntax and caller can show usage |
| storage file absent on first run | handled `NotFound` branch returning a new board | documented environmental condition |
| permission denied | `Result` | operation failed and must not be hidden |
| duplicate stored ID | `Result` | corrupted or invalid persistent state |
| impossible private enum state | usually structurally unrepresentable; otherwise assertion | programmer invariant, not user input |
| broken output pipe | `Result` at output boundary | environment can cause it |
| help requested | ordinary command/outcome | not a failure |
| next-ID overflow | `Result` domain failure | valid historical use can reach it |
| failed test assertion | panic in test harness | test contract was violated |

### 2. Positive task ID

```rust
use std::num::ParseIntError;

#[derive(Debug)]
enum ParseTaskIdError {
    InvalidInteger { source: ParseIntError },
    Zero,
}

#[derive(Clone, Copy, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
struct TaskId(u64);

impl TaskId {
    fn new(value: u64) -> Option<Self> {
        (value != 0).then_some(Self(value))
    }
}

fn parse_task_id(text: &str) -> Result<TaskId, ParseTaskIdError> {
    let value = text
        .parse::<u64>()
        .map_err(|source| ParseTaskIdError::InvalidInteger { source })?;
    TaskId::new(value).ok_or(ParseTaskIdError::Zero)
}
```

The lexical and domain failures remain distinct.

### 3. Contextual line reader

```rust
use std::io;

#[derive(Debug)]
enum StorageError {
    ReadLine { line: usize, source: io::Error },
}

fn contextual_line(
    line: io::Result<String>,
    physical_line: usize,
) -> Result<String, StorageError> {
    line.map_err(|source| StorageError::ReadLine {
        line: physical_line,
        source,
    })
}
```

The caller supplies the physical position because the iterator item alone does not know it.

### 4. Transactional import

```rust
#[derive(Debug, PartialEq, Eq)]
struct ImportError {
    index: usize,
    token: String,
}

fn append_numbers(
    input: &[&str],
    output: &mut Vec<u64>,
) -> Result<(), ImportError> {
    let decoded = input
        .iter()
        .enumerate()
        .map(|(index, token)| {
            token.parse::<u64>().map_err(|_| ImportError {
                index,
                token: (*token).to_owned(),
            })
        })
        .collect::<Result<Vec<_>, _>>()?;

    output.extend(decoded);
    Ok(())
}
```

All parsing finishes into temporary ownership before `output` changes. A manual loop into a temporary vector is equally clear.

### 5. Record grammar

A suitable grammar is:

```text
record = "TASK" TAB id TAB status TAB priority TAB title
```

Decode with a bounded field iterator, not unrestricted indexing. After reading exactly five fields, reject a sixth. Parse leaf values through typed functions. Pass the title through the same constructor used by interactive creation so storage cannot bypass domain invariants.

```rust
fn required<'a>(
    fields: &mut impl Iterator<Item = &'a str>,
    name: &'static str,
) -> Result<&'a str, RecordError> {
    fields.next().ok_or(RecordError::MissingField { name })
}
```

The complete course capstone contains the full implementation.

### 6. Conversion graph

A defensible graph is:

```text
ParseIntError -> ParseTaskIdError -> CommandError
RecordError ----------------------> StorageError -> AppError
DomainError -------------------------------------> AppError
CommandError ------------------------------------> AppError
```

The parse-int conversion may be explicit with `map_err` because token context differs by field. `StorageError -> RecordError` is not implemented because a storage failure cannot generally become a record failure.

### 7. Generic codec

```rust
use std::io::{self, BufRead, Write};

fn decode_lines<R: BufRead>(reader: R) -> Result<Vec<String>, io::Error> {
    reader.lines().collect()
}

fn encode_lines<W: Write>(
    writer: &mut W,
    lines: &[String],
) -> io::Result<()> {
    for line in lines {
        writeln!(writer, "{line}")?;
    }
    Ok(())
}
```

The actual task codec replaces raw strings with version and domain validation. An in-memory test can pass `&bytes[..]` to a `BufReader` and a `Vec<u8>` as writer.

### 8. Missing-file policy

```rust
use std::{fs::File, io, path::Path};

fn load(path: &Path) -> Result<TaskBoard, StorageError> {
    match File::open(path) {
        Ok(file) => load_from(io::BufReader::new(file)),
        Err(source) if source.kind() == io::ErrorKind::NotFound => {
            Ok(TaskBoard::new())
        }
        Err(source) => Err(StorageError::Open {
            path: path.to_path_buf(),
            source,
        }),
    }
}
```

Do not make `load_from` interpret an empty reader as “not found.” It has no path or open event and should enforce the file grammar.

### 9. Canonical output

Sort a borrowed view or rely on a board invariant that stores tasks in ID order. Do not mutate domain order solely for display unless that is the domain contract.

```rust
let mut tasks: Vec<&Task> = board.tasks().iter().collect();
tasks.sort_by_key(|task| task.id());
for task in tasks {
    encode_task(writer, task)?;
}
```

This allocates a vector of references, not cloned tasks. A test should compare exact bytes, including final newline.

### 10. Aggregate validation

Track IDs in a `HashSet` or sort and inspect adjacent values. Reject duplicates. For a nonempty board, require `next_id > max_id`; for an empty board, require the documented initial value, normally 1. Guard against `max_id == u64::MAX`, because no valid next ID exists.

### 11. Preserve the old file

A foundational sequence:

```text
derive sibling temporary path
create temporary with create_new or documented collision handling
encode complete content
flush buffered writer
sync temporary file
rename temporary over target
```

The implementation should remove its own temporary file after a reported failure where safe. Tests can prove that serialization failure never touches the target and that a successful save replaces it. Complete cross-platform crash guarantees require more machinery than this course claims.

### 12. Error-contract review

A representative row:

| Operation | Success proof | Errors | Context | Mutation | Recovery |
|---|---|---|---|---|---|
| `load` | returned board satisfies all invariants | open, read, version, record, aggregate | path, line, field, source | constructs temporary values; no caller state mutation | application reports and exits |
| `start` | target exists and becomes `Doing` | unknown ID, illegal current state | ID, current state | only after all checks | application reports domain error |
| `save` | canonical bytes replaced target | create, write, flush, sync, rename | operation and paths | target replacement only at commit | application reports failure |

Command and storage errors may both lead to exit status 2 or 1 under a simple CLI policy, while remaining typed internally for diagnostics and tests.

### Final review

A solution is weaker than the reference when it erases operation context, mutates before validation, tests only messages, or claims stronger persistence than it implements. A different enum layout is acceptable when caller decisions and source chains remain clear.

### Post-key transfer

Audit a loader that silently drops malformed records and a saver that overclaims atomicity; repair both contracts and tests.



## Laboratory comparison

The complete laboratory implementation is in [`module-07-record-codec/solution`](../../labs/module-07-record-codec/solution). Before reading it, write down:

- your public API;
- the invariant each type owns;
- the failure behavior;
- the ownership or dispatch topology;
- the complexity claim you are prepared to defend.

For **Errors, Parsing, Files, and Persistence**, compare the contract, invariant, failure behavior, ownership or dispatch topology, and cost before comparing syntax. A different implementation is sound when it preserves those properties and makes the module’s central relationship at least as clear.

## What a strong answer demonstrates

- Distinguish absence, recoverable failure, invariant violation, process failure, and ordinary values.
- Design typed errors with context and source preservation rather than flattening failures into strings.
- Parse untrusted text transactionally by tokenizing, converting, validating, and only then committing state.
- Build generic buffered reader and writer boundaries that preserve precise line-level diagnostics and source errors.
- State the exact persistence guarantee of a temporary-file-and-rename protocol, including what it does not guarantee across platforms, crashes, and concurrent writers.

A complete explanation of **Errors, Parsing, Files, and Persistence** also states the boundary of the mechanism: which guarantee it does not provide, which cost it introduces, and which simpler design should be preferred when that guarantee is unnecessary.
