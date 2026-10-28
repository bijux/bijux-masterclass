# 07 — Errors, Parsing, Files, and Persistence

**Course 1, day 7 · Module 7 of 90**  
`██░░░░░░░░░░░░░░░░░░` **7/90**

[← Module 6: Collections, Iterators, and Closures](../module-06-collections-iterators-and-closures/index.md) · [Course 1 overview](../index.md) · [Ninety-module map](../../../COURSE_MAP.md) · [Module 8: Generics, Traits, Conversions, and Lifetime Basics →](../module-08-generics-traits-conversions-and-lifetime-basics/index.md)

## The question

> Which failures are part of the product contract, where are they detected, and what state is visible after failure?

## Why this comes now

Collections make input processing possible, but real input is missing, malformed, duplicated, or unreadable. This module turns failure into part of the type contract and separates parsing, validation, I/O, and state mutation. That separation is the foundation for trustworthy persistence in every later capstone.

## What you will be able to do

- Distinguish absence, recoverable failure, invariant violation, process failure, and ordinary values.
- Design typed errors with context and source preservation rather than flattening failures into strings.
- Parse untrusted text transactionally by tokenizing, converting, validating, and only then committing state.
- Build generic buffered reader and writer boundaries that preserve precise line-level diagnostics and source errors.
- State the exact persistence guarantee of a temporary-file-and-rename protocol, including what it does not guarantee across platforms, crashes, and concurrent writers.

## Core model

### Why this module exists

A reliable program distinguishes absence, malformed input, violated domain rules, I/O failure, and programmer invariants. It also defines what state remains visible when failure occurs. `Option`, `Result`, typed errors, and `?` provide vocabulary; they do not choose the boundary for you.

### Classify failure before choosing a type

- `Option<T>`: a value may validly be absent and no further explanation is required at this layer.
- `Result<T, E>`: the operation may fail and the caller can respond or add context.
- panic: a violated internal invariant or unrecoverable condition at a boundary that explicitly chooses termination.
- ordinary value: the condition is part of successful output, not exceptional.

Bad user input, missing files, and invalid transitions are normally recoverable product cases, not panics.

### `?` propagates; it does not handle

```rust
fn parse_id(input: &str) -> Result<TaskId, ParseIdError> {
    let raw = input.parse::<u64>().map_err(ParseIdError::NotInteger)?;
    TaskId::new(raw).ok_or(ParseIdError::Zero)
}
```

The operator returns early from the current function after converting the error as required. Handling happens where code chooses retry, fallback, user output, logging, or termination.

### Typed errors preserve structure

```rust
#[derive(Debug)]
pub enum LoadError {
    Io(std::io::Error),
    InvalidHeader,
    InvalidRecord { line: usize, message: String },
    DuplicateId { line: usize, id: u64 },
}
```

A typed error supports matching, source chaining, exit-code policy, and tests that do not depend on fragile prose. Display text remains important for people, but it is not the only representation.

Do not flatten an I/O error to `String` at every layer. Add context while preserving the source where possible.

### Parsing is a transaction

For untrusted text:

1. split/tokenize under explicit grammar rules;
2. convert primitive fields;
3. validate domain invariants;
4. validate cross-record invariants such as uniqueness;
5. construct candidate state;
6. expose/commit only after the whole input is valid.

A loader that mutates the live board record by record and then encounters a malformed line has exposed partial state. Build a candidate board and return it only on success.

### Generic I/O boundaries

A parser should not require a filesystem path when it only needs lines or bytes. Use `BufRead` and `Write` so tests can use in-memory buffers and the path layer can remain thin.

```rust
pub fn load_from<R: std::io::BufRead>(reader: R) -> Result<TaskBoard, LoadError> {
    let mut candidate = TaskBoard::new();

    for (zero_based_line, line) in reader.lines().enumerate() {
        let line_number = zero_based_line + 1;
        let line = line.map_err(LoadError::Io)?;
        let task = decode_record(line_number, &line)?;
        candidate
            .insert_loaded(task)
            .map_err(|message| LoadError::InvalidRecord {
                line: line_number,
                message,
            })?;
    }

    Ok(candidate)
}
```

The function constructs a private candidate and returns it only after every line and cross-record invariant succeeds. Dependency direction remains narrow: parsing depends on `BufRead`; path opening belongs to a filesystem adapter.

### Persistence guarantee matrix

A same-directory temporary file followed by flush/sync and `rename` can reduce the window in which the destination contains partial bytes, but the exact guarantee depends on platform and filesystem. The Course 1 capstone is a **single-process instructional protocol**, not a database transaction system.

It does **not** claim:

- coordination among concurrent writers;
- protection from lost updates;
- universal replacement behavior on every platform;
- directory-entry durability after sudden power loss;
- recovery from every crash point;
- locking, journaling, or transactional multi-file updates.

The documentation and tests must say exactly what is implemented: validate complete in-memory state, write a same-directory candidate, finish the file operation, replace the destination according to the platform API contract, and report errors. Later systems/production courses own stronger protocols.

### Worked derivation: line-context codec

Decode one record separately from file I/O:

```rust
pub fn decode_record(line_number: usize, line: &str) -> Result<Task, LoadError> {
    let mut fields = line.split('\t');
    let id = fields
        .next()
        .ok_or_else(|| invalid(line_number, "missing id"))?
        .parse::<TaskId>()
        .map_err(|error| invalid(line_number, error.to_string()))?;
    let status = fields
        .next()
        .ok_or_else(|| invalid(line_number, "missing status"))?
        .parse::<Status>()
        .map_err(|error| invalid(line_number, error.to_string()))?;
    let title = fields
        .next()
        .ok_or_else(|| invalid(line_number, "missing title"))?;

    if fields.next().is_some() {
        return Err(invalid(line_number, "unexpected extra field"));
    }

    Task::from_stored(id, status, title.to_owned())
        .map_err(|message| invalid(line_number, message))
}
```

The line number is attached at the boundary where it is known. Tests can exercise this function without touching disk. A full loader preserves the original I/O source for read failures and uses record errors for malformed content.

### Try without the scaffold

Design an import function that accepts a reader and returns either a complete catalog or a typed error containing line and field. Add a duplicate-key check. Prove that an error leaves the existing catalog unchanged.

### Misconception clinic

- **“`?` catches errors.”** It exits and propagates them.
- **“Missing file means empty data.”** Only if the product contract deliberately defines that special case.
- **“Rename means atomic durable save.”** That phrase hides failure model, platform, synchronization, and concurrency assumptions.
- **“String errors are simpler.”** They often discard structure that later layers need.

### Four different conditions

Programs become unreliable when unlike conditions share one representation. Start by separating four categories.

#### Ordinary absence

Absence is part of successful operation. Searching a board for an unknown ID can legitimately find nothing:

```rust
fn find_task(tasks: &[Task], id: TaskId) -> Option<&Task> {
    tasks.iter().find(|task| task.id() == id)
}
```

`None` does not explain why an operation failed. It states that the requested value is absent under an otherwise valid computation.

#### Recoverable operational failure

A caller may respond to an unreadable file, malformed number, invalid transition, or failed write. Use `Result`:

```rust
fn parse_task_id(text: &str) -> Result<TaskId, ParseTaskIdError>;
```

The error should provide the distinction the caller needs. A command layer may print usage for a malformed ID but print a storage diagnostic for an unreadable board.

#### Violated programmer assumption

Indexing a fixed two-element array at index 2, reaching an enum arm declared impossible by an internal proof, or corrupting an unsafe abstraction can indicate a defect in the program. Panicking may be appropriate when continuing would fabricate results and the condition cannot arise from untrusted input.

The key test is not “could this happen?” It is “can a user, file, network peer, environment variable, or ordinary operating condition cause it?” If yes, model it as data.

#### Process-level fatal policy

A binary may decide that a recoverable library error means the current command cannot continue. The binary prints an error and exits nonzero. That is policy at the outer shell, not permission for deep library code to terminate the process.

```rust
fn main() {
    if let Err(error) = taskboard::run_from_env() {
        eprintln!("error: {error}");
        std::process::exit(1);
    }
}
```

The library returns evidence. The binary selects presentation and process status.

### Why sentinel values fail

Returning `0` for “not found” creates ambiguity when zero is a valid quantity. Returning an empty board for every load failure erases corruption and permission failures. Returning `false` from a transition loses whether the ID was absent, the current state was illegal, or validation failed.

A useful signature forces the caller to confront the state space:

```rust
fn start(&mut self, id: TaskId) -> Result<(), TransitionError>;
```

This does not guarantee a good error type, but it prevents silent ambiguity.

### Panic is not a substitute for validation

Untrusted values include command arguments, file contents, environment variables, current directories, clock values, and operating-system responses. Validate them and return errors.

```rust,compile_fail
fn parse_positive(text: &str) -> u64 {
    text.parse::<u64>().unwrap()
}
```

The problem is not merely that `unwrap` can panic. The function's return type falsely claims that every string determines a positive integer.

A truthful version exposes both lexical parsing and domain validation:

```rust
#[derive(Debug, PartialEq, Eq)]
enum PositiveError {
    NotAnInteger,
    Zero,
}

fn parse_positive(text: &str) -> Result<u64, PositiveError> {
    let value = text
        .parse::<u64>()
        .map_err(|_| PositiveError::NotAnInteger)?;
    if value == 0 {
        return Err(PositiveError::Zero);
    }
    Ok(value)
}
```

### `expect` is still a panic

An informative panic message is useful in tests and in startup assertions about developer-controlled assets. It does not convert input failure into recovery. “Use `expect` with a good message” is not an error-handling architecture.

### Assertions and debug assertions

Assertions state internal invariants:

```rust
fn midpoint(low: usize, high: usize) -> usize {
    assert!(low <= high, "range must be ordered");
    low + (high - low) / 2
}
```

If callers can supply an unordered range during ordinary use, return `Result` instead. `debug_assert!` is removed from optimized builds and therefore cannot enforce externally necessary validation.

### Error boundaries in `taskboard`

The capstone uses different representations deliberately:

- `find`: `Option<&Task>` because absence is normal;
- `start`, `done`, `reopen`, `remove`: `Result<_, DomainError>` because the caller needs to distinguish missing IDs and illegal transitions;
- command parsing: `Result<Command, CommandError>`;
- storage loading: `Result<TaskBoard, StorageError>`;
- application execution: `Result<Outcome, AppError>`;
- `main`: render error, choose exit status.

Do not merge these layers solely to have one universal error enum. Convert errors where a broader boundary genuinely needs to aggregate them.

### `Result` is a control-flow type

```rust
pub enum Result<T, E> {
    Ok(T),
    Err(E),
}
```

A function returning `Result<T, E>` promises one of two typed outcomes. Pattern matching makes both paths explicit:

```rust
fn load_count(text: &str) -> Result<u64, CountError> {
    match text.parse::<u64>() {
        Ok(value) if value > 0 => Ok(value),
        Ok(_) => Err(CountError::Zero),
        Err(source) => Err(CountError::InvalidInteger { source }),
    }
}
```

The value inside `Ok` is not available on the error path. Code after a propagated error does not execute.

### What `?` actually does

For ordinary `Result`, this:

```rust
let line = read_header(reader)?;
```

is conceptually similar to:

```rust
let line = match read_header(reader) {
    Ok(line) => line,
    Err(error) => return Err(From::from(error)),
};
```

Three consequences matter:

1. `?` returns from the enclosing function or closure, not from the nearest block.
2. the enclosing return type must support the residual error through compatible conversion;
3. `?` propagates an error—it does not log, display, retry, or repair it.

### Add context at the boundary where it becomes known

A raw `ParseIntError` does not know that a token came from line 17, field `id`, in `tasks.db`. The record parser should attach field context; the file loader should attach line and path context.

```rust
fn parse_id(token: &str) -> Result<TaskId, RecordError> {
    let value = token.parse::<u64>().map_err(|source| {
        RecordError::InvalidId {
            token: token.to_owned(),
            source,
        }
    })?;
    TaskId::new(value).ok_or(RecordError::ZeroId)
}
```

A caller should not have to reconstruct lost facts from a formatted sentence.

### Preserve the original source

When a lower-level error remains diagnostically valuable, store it:

```rust
#[derive(Debug)]
enum StorageError {
    Read {
        path: PathBuf,
        source: std::io::Error,
    },
}
```

`Display` can present a concise message. `Error::source` can expose the chain to diagnostics. Structured fields support tests and programmatic handling.

### `map_err` versus `From`

Use `map_err` when conversion needs local context:

```rust
let file = File::open(path).map_err(|source| StorageError::Open {
    path: path.to_path_buf(),
    source,
})?;
```

Use `From` when a context-free conversion is meaningful and unambiguous:

```rust
impl From<DomainError> for AppError {
    fn from(error: DomainError) -> Self {
        Self::Domain(error)
    }
}
```

Do not use a broad `From<io::Error>` if the application needs to know whether the failure occurred during open, read, create, write, flush, sync, or rename. A convenient conversion can erase the operation that matters.

### Combinators are not automatically clearer

`map`, `and_then`, `ok_or`, `ok_or_else`, and `map_err` are useful when they express a short transformation. Deeply nested chains can obscure ownership and early-return behavior.

```rust
fn find_required<'a>(board: &'a TaskBoard, id: TaskId) -> Result<&'a Task, DomainError> {
    board.find(id).ok_or(DomainError::UnknownTask { id })
}
```

A multi-stage validation often reads better with local bindings and guard clauses.

### Context must be bounded

Copying an entire multi-gigabyte input into an error is not responsible context. Preserve the path, line, field, a bounded token representation, and the source. For sensitive data, do not echo secrets merely because they are available.

### Error messages are not the error model

This test is brittle and weak:

```rust
assert_eq!(error.to_string(), "bad task");
```

Prefer matching structured variants:

```rust
assert!(matches!(
    error,
    StorageError::InvalidRecord { line: 3, .. }
));
```

Then add a small number of tests for user-facing formatting where wording is itself part of the CLI contract.

### Design from caller decisions

List the actions a caller may take before naming variants. A command caller might:

- show usage for malformed syntax;
- report an unknown command;
- report an invalid status token;
- distinguish a missing operand from an extra operand.

A storage caller might:

- treat a genuinely missing file as an empty board;
- stop on permission denial;
- identify unsupported format versions;
- report a malformed record with a line number;
- preserve an existing board when saving fails.

These decisions suggest different enums. One gigantic `Error` type used everywhere usually exposes irrelevant variants and encourages arbitrary conversions.

### Carry data, not preformatted prose

```rust
#[derive(Debug)]
pub enum CommandError {
    Empty,
    UnknownCommand { command: String },
    MissingArgument { command: &'static str, name: &'static str },
    UnexpectedArgument { command: &'static str, value: String },
    InvalidTaskId { value: String },
    InvalidStatus { value: String },
}
```

The variant identifies the condition; fields preserve evidence. `Display` owns presentation:

```rust
impl std::fmt::Display for CommandError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::Empty => write!(f, "no command supplied"),
            Self::UnknownCommand { command } => {
                write!(f, "unknown command {command:?}")
            }
            Self::MissingArgument { command, name } => {
                write!(f, "{command} requires <{name}>")
            }
            // remaining variants omitted here
            _ => write!(f, "invalid command"),
        }
    }
}
```

In production course code, implement every arm explicitly. A broad catch-all in an error formatter can hide newly added variants from review.

### Implement `std::error::Error` deliberately

Marker-only errors can use an empty implementation:

```rust
impl std::error::Error for CommandError {}
```

Errors wrapping lower-level sources should return them:

```rust
impl std::error::Error for StorageError {
    fn source(&self) -> Option<&(dyn std::error::Error + 'static)> {
        match self {
            Self::Open { source, .. }
            | Self::Read { source, .. }
            | Self::Write { source, .. } => Some(source),
            Self::InvalidHeader { .. }
            | Self::InvalidRecord { .. }
            | Self::UnsupportedVersion { .. } => None,
        }
    }
}
```

Trait objects appear here only as part of the standard `Error` contract; designing trait-object architectures belongs later in the program.

### Avoid recursive or cyclic conversion

Conversions should move errors outward through layers:

```text
ParseIntError -> RecordError -> StorageError -> AppError
DomainError -------------------------------> AppError
CommandError ------------------------------> AppError
```

Do not implement conversions in both directions. Converting a broad application error back into a narrow storage error generally requires inventing information.

### Transparent versus contextual wrapping

A transparent wrapper preserves the source's meaning with little added data. A contextual wrapper states what operation failed:

```rust
StorageError::Rename {
    from: PathBuf,
    to: PathBuf,
    source: io::Error,
}
```

The operation, both paths, and source can all matter when diagnosing a failed commit.

### Error types and public API stability

A public error enum exposes variants as part of the API. Adding variants can affect exhaustive downstream matches. For this foundational capstone, explicit enums are valuable because you own both library and callers. In a broadly published library, error evolution requires deliberate compatibility policy.

### No borrowed diagnostics from temporary input

An error containing `&str` ties its lifetime to input storage. This can be appropriate for immediate parsing, but owned fields simplify propagation beyond the input buffer:

```rust
#[derive(Debug)]
struct InvalidToken {
    field: &'static str,
    token: String,
}
```

Own only the bounded evidence needed; do not copy full files.

### Parsing establishes trust in stages

Text is not a domain value. A robust parser separates at least four layers:

1. **lexical recognition** — can this token be read as an integer or known word?
2. **structural validation** — are the required fields present in the correct order?
3. **semantic validation** — is the integer nonzero, the title legal, and the state recognized?
4. **cross-record validation** — are IDs unique and is the declared next ID consistent with all records?

Mixing all stages into one loop often creates partial mutation and weak diagnostics.

### Parse one record as a pure function

```rust
fn decode_task(line: &str) -> Result<Task, RecordError> {
    let mut fields = line.split('\t');
    let marker = fields.next().ok_or(RecordError::MissingField("marker"))?;
    if marker != "TASK" {
        return Err(RecordError::WrongMarker(marker.to_owned()));
    }

    let id = parse_id(fields.next().ok_or(RecordError::MissingField("id"))?)?;
    let status = parse_status(
        fields.next().ok_or(RecordError::MissingField("status"))?
    )?;
    let priority = parse_priority(
        fields.next().ok_or(RecordError::MissingField("priority"))?
    )?;
    let title = fields.next().ok_or(RecordError::MissingField("title"))?;

    if let Some(extra) = fields.next() {
        return Err(RecordError::ExtraField(extra.to_owned()));
    }

    Task::restore(id, title.to_owned(), priority, status)
        .map_err(RecordError::InvalidTask)
}
```

This function neither opens files nor mutates a board. It is deterministic and cheap to test.

### Validate first, commit once

A dangerous loader pushes each decoded task directly into the live board. If line 80 is malformed, lines 1–79 have already changed state.

Instead:

```rust
fn decode_board<R: BufRead>(reader: R) -> Result<TaskBoard, StorageError> {
    let mut decoded = Vec::new();
    let mut next_id = None;

    // read and validate all lines into temporary values

    TaskBoard::restore(decoded, next_id.ok_or(StorageError::MissingNextId)?)
        .map_err(StorageError::InvalidBoard)
}
```

`TaskBoard::restore` performs cross-record validation and returns a complete valid board. The caller replaces its old board only after `Ok`.

### Exact grammar beats permissive guessing

Document the storage grammar. For example:

```text
file        = header newline next-id newline *task-line
header      = "TASKBOARD-V1"
next-id     = "NEXT_ID" tab positive-integer
 task-line   = "TASK" tab id tab status tab priority tab title
status      = "todo" / "doing" / "done"
priority    = "low" / "normal" / "high"
```

A format parser should reject unknown markers, extra fields, malformed escaping, duplicate singleton records, and unsupported headers. Silent acceptance makes later evolution unpredictable.

### Empty lines are a policy decision

Do not sprinkle `.filter(|line| !line.trim().is_empty())` into a parser without specifying whether blank lines are legal. Ignoring them may conceal truncation or accidental edits. This course format rejects unexpected blank records.

### Line numbers are physical evidence

When reading after a header, preserve actual physical line numbers. Avoid an off-by-one caused by restarting enumeration:

```rust
for (offset, line) in lines.enumerate() {
    let physical_line = offset + 2; // first remaining line is line 2
    // attach physical_line to any error
}
```

If another line has already been consumed, update the base accordingly. Write tests against exact physical positions.

### Command parsing and file parsing differ

Command parsing has shell token boundaries already established by the operating system. File parsing receives lines and fields according to the format. Reusing one parser merely because both consume strings can couple unrelated grammars.

Both should, however, share typed leaf parsers such as `FromStr` for `Status`, `Priority`, and `TaskId` once Module 8 formalizes those traits.

### Paths are not guaranteed UTF-8 strings

Use `Path` and `PathBuf` for filesystem paths:

```rust
fn load(path: &Path) -> Result<TaskBoard, StorageError>;
```

`&Path` is a borrowed path view; `PathBuf` owns path data. Avoid converting paths to `String` merely for storage. Use `path.display()` for human-facing lossy display and preserve the original `PathBuf` inside errors.

### Open semantics must be explicit

`File::open` can fail because a file does not exist, permission is denied, a path component is not a directory, or the process has exhausted resources. Only `ErrorKind::NotFound` should become an empty initial board if that is the documented application policy.

```rust
match File::open(path) {
    Ok(file) => load_from(BufReader::new(file)),
    Err(source) if source.kind() == io::ErrorKind::NotFound => {
        Ok(TaskBoard::new())
    }
    Err(source) => Err(StorageError::Open {
        path: path.to_path_buf(),
        source,
    }),
}
```

Treating every open error as absence hides security and operational defects.

### Buffering changes syscall behavior, not semantics

`BufReader<R>` reduces repeated small reads from an underlying source. `BufWriter<W>` accumulates writes. Buffering does not validate content and does not guarantee durable persistence.

A buffered writer can retain an error until `flush`. Do not rely solely on destructor cleanup because `Drop` cannot report failure to the caller.

```rust
writer.flush().map_err(|source| StorageError::Flush {
    path: path.to_path_buf(),
    source,
})?;
```

### Generic I/O isolates pure codec logic

```rust
fn load_from<R: BufRead>(reader: R) -> Result<TaskBoard, StorageError>;

fn save_to<W: Write>(
    writer: &mut W,
    board: &TaskBoard,
) -> Result<(), StorageError>;
```

The filesystem wrapper supplies `File`; tests supply byte slices and vectors. This is dependency inversion through standard traits, not abstraction for its own sake.

Be precise about ownership:

- taking `R` by value lets the function own the reader wrapper;
- taking `&mut W` allows repeated writes while the caller retains the writer;
- returning the writer is unnecessary unless the caller needs its final state and ownership was consumed.

### Read strategy and bounded memory

`read_to_string` is concise but loads the entire file and requires UTF-8. A line-oriented format can use `BufRead::lines`, which allocates one `String` per line. For a small local task board this is acceptable and clear. Large-stream systems require explicit size limits and possibly `read_until` over bytes.

State the bound instead of pretending it does not exist. The capstone rejects titles above its domain limit and is designed for a local work queue, not arbitrary unbounded ingestion.

### Write strategy

Serialization should write deterministic bytes:

- fixed header;
- fixed field order;
- stable task order;
- one newline policy;
- explicit escaping or rejected delimiters;
- no hash-table iteration leakage.

`writeln!` returns an I/O result and should be propagated.

### Filesystem wrappers remain thin

A clean split is:

```text
load(path)     -> open + missing-file policy + buffered reader + load_from
load_from(r)   -> grammar + validation
save(path, b)  -> temporary path + create + save_to + flush/sync + rename
save_to(w, b)  -> deterministic encoding
```

This separation makes the codec testable and keeps path context at the layer that knows the path.

### A file format is an API

Once a program persists data, the byte representation outlives one process invocation. Treat it as a compatibility contract. A version header prevents a future parser from silently interpreting old bytes under new rules:

```text
TASKBOARD-V1
NEXT_ID	4
TASK	1	todo	high	Repair parser
TASK	3	done	normal	Write tests
```

The parser accepts exactly the versions it understands. It should report an unsupported future version rather than guessing.

### Encode one canonical representation

Canonical output simplifies testing and change review:

- records are ordered by task ID;
- enums have one lowercase spelling;
- numeric fields have no padding;
- the file ends with one newline;
- forbidden delimiters are rejected by domain validation;
- no optional whitespace is emitted.

A parser may accept a slightly broader but documented input language, yet the writer should emit one form.

### Validate aggregate invariants

Per-record validity is insufficient. After decoding all records, verify:

- task IDs are unique;
- every ID is positive;
- `next_id` is greater than every stored ID;
- `next_id` has not overflowed;
- all required singleton records occur exactly once;
- no data follows a terminal marker if the grammar defines one.

Put domain-level checks in a constructor such as `TaskBoard::restore`, not only in the file parser. Any future import path should establish the same invariants.

### Failure atomicity of saving

Writing directly to the target can destroy the old valid file if serialization or writing fails halfway. A stronger basic sequence is:

1. create a temporary file in the target directory;
2. serialize the complete board;
3. flush buffered bytes;
4. ask the file to synchronize its data;
5. close or release the temporary file handle as needed by the platform;
6. rename the temporary path over the target;
7. remove the temporary file after failure when possible.

Keeping the temporary file in the same directory increases the chance that rename uses one filesystem and is atomic with respect to observing either name.

### Durability must be described honestly

A successful file `sync_all` and rename is stronger than direct overwrite, but full crash durability can also require synchronizing the containing directory, and replacement semantics differ across operating systems. This foundational course implements and tests preservation under ordinary reported errors. It does not claim a database-grade transaction protocol.

That limitation belongs in documentation, not hidden in implementation comments.

### Temporary-name collisions

A fixed `.tmp` sibling can collide with another process or a previous crash. For a single-user foundational CLI, the course uses a deterministic sibling and fails if safety cannot be established. Later systems coursework can introduce robust unique creation, locking, and multi-process coordination.

Never delete an arbitrary path supplied by untrusted data under the assumption that it is “the temporary file.” Derive it from the configured target under a documented policy.

### Save only after a successful mutation

Application flow should be:

```text
load valid board
parse typed command
execute against in-memory board
if command changed state:
    save new board
render success
else:
    render read-only result without rewriting
```

If domain execution fails, no save occurs. If save fails, the application reports failure and the previous target file remains the authoritative state. The current process may hold a changed in-memory board, but it exits without claiming success.

### Compatibility tests

A format deserves tests for:

- known valid fixture loads to expected values;
- save then load preserves domain equality;
- output bytes are canonical;
- unsupported version fails distinctly;
- malformed integer reports exact line and field;
- duplicate ID fails;
- missing `NEXT_ID` fails;
- inconsistent `NEXT_ID` fails;
- truncated final record fails;
- old target remains after an injected or naturally induced save failure where the test platform can establish it.

## Use the idea in a complete program

The course capstone is **Taskboard**, a persistent command-line task board. Add typed command and storage errors, a versioned codec, transactional loading, and explicit save behavior. Invalid input must not partially mutate the board. The exact implementation task is in the [workbook](workbook.md); the full product contract is in the [capstone guide](../capstone.md).

## Practice sequence

1. Reproduce the important examples from this chapter without copying them line for line.
2. Complete the prediction and repair sections in the [workbook](workbook.md).
3. Build the independent [laboratory](../../labs/module-07-record-codec/README.md).
4. Apply the capstone increment.
5. Open the [reasoned solutions](solutions.md) only after recording your own answer.

## Ready to continue

You are ready for Module 8 when you can:

- answer the module question—“Which failures are part of the product contract, where are they detected, and what state is visible after failure?”—without reading the chapter;
- demonstrate this outcome on a fresh example: Distinguish absence, recoverable failure, invariant violation, process failure, and ordinary values;
- repair the debugging case while preserving its product requirement;
- complete the laboratory transfer variant and explain the decisive design choice;
- name a simpler alternative and the condition under which you would prefer it.

## Primary Rust references

This chapter is self-contained. These official sources are included for verification and future language updates, not as required reading:

- [The Rust Book: Error Handling](https://doc.rust-lang.org/book/ch09-00-error-handling.html)
- [The Rust Book: I/O Project](https://doc.rust-lang.org/book/ch12-00-an-io-project.html)
- [std::io](https://doc.rust-lang.org/std/io/)

[← Module 6](../../../01-rust-foundations/course-book/module-06-collections-iterators-and-closures/index.md) · [ninety-module map](../../../COURSE_MAP.md) · [Module 8 →](../../../01-rust-foundations/course-book/module-08-generics-traits-conversions-and-lifetime-basics/index.md)

## Continue

1. Complete the [Module 7 workbook](workbook.md) and freeze every prediction before compiling.
2. Build [Laboratory 7 — Versioned Record Codec](../../labs/module-07-record-codec/README.md) from its public contract.
3. Apply the Module 7 increment in the [Taskboard engineering guide](../capstone.md).
4. Review the [reasoned solutions](solutions.md) only after an independent attempt, then revise the causal model rather than copying code shape.
