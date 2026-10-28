# Taskboard — Course 1 capstone

The capstone supports the course-book. It exists to force cross-layer transfer after each mechanism has been understood in isolation.

## Product

**Taskboard** is a persistent command-line task board.

## Ten increments

1. **Module 1:** Create the Taskboard package, its help surface, and a title-validation function. The important product lesson is that even the first small function has a type contract and tests.
2. **Module 2:** Write pure policy functions for identifiers, priorities, and state-transition sketches. Keep command parsing out until the decisions can be tested without I/O.
3. **Module 3:** Move owned task titles into board storage and document the owner after each operation. Avoid cloning simply because a caller's postcondition was never stated.
4. **Module 4:** Refactor read operations to borrow the board and updates to use one narrow mutable path. The signatures should make inspection, mutation, and ownership transfer visibly different.
5. **Module 5:** Replace stringly records with `Task`, `TaskId`, `Priority`, `Status`, and `Command`. The state graph should make contradictory combinations unrepresentable.
6. **Module 6:** Implement board operations, deterministic listing, filtering, search, and statistics. For each traversal, state whether it borrows, mutates, or consumes the collection.
7. **Module 7:** Add typed command and storage errors, a versioned codec, transactional loading, and explicit save behavior. Invalid input must not partially mutate the board.
8. **Module 8:** Use standard conversion traits and generic readers and writers where they remove real duplication. Add only the lifetime annotations required by returned borrowed data.
9. **Module 9:** Split reusable logic from the binary, minimize public visibility, and cover the contract with unit, integration, CLI, and documentation tests.
10. **Module 10:** Implement an independently selected cross-layer feature and defend the entire path from domain invariant to exit status. This is the transfer proof for Course 1.

## How to use the capstone

Do not read the finished implementation before attempting an increment. Begin with the public behavior, write the failure-path test, identify the types whose invariants change, and then implement the smallest coherent change. After the change passes, inspect the finished code to compare architecture rather than copy syntax.

## Product Contract

### 1. Why this product

A capstone must be large enough to force interactions between concepts but small enough to understand completely. A web service would introduce network protocols, async execution, framework conventions, and third-party types before you can distinguish language design from framework design. A one-file calculator would not force persistence, state transitions, public APIs, or failure recovery. A local task board occupies the useful middle.

The product is a persistent work queue operated through one command at a time:

```text
taskboard add <low|normal|high> <title...>
taskboard list [todo|doing|done]
taskboard start <id>
taskboard done <id>
taskboard reopen <id>
taskboard remove <id>
taskboard rename <id> <title...>
taskboard search <query...>
taskboard stats
taskboard help
taskboard version
```

The command set is intentionally closed. Every command has a typed representation. “Unknown command” is not a domain state; it is a command-grammar failure. “Task 7 does not exist” is not a grammar failure; it is a domain failure. “The storage file cannot be read” is neither of those; it is an I/O failure. Preserving those distinctions is part of the product contract.

### 2. Domain vocabulary

A **task** has four properties:

- a stable, positive `TaskId`;
- an owned UTF-8 title;
- one `Priority`;
- exactly one `Status`.

A **board** owns all retained tasks and the next identifier allocation token. The board is the aggregate authority: callers may inspect tasks, but only board operations allocate IDs, mutate lifecycle state, rename titles, or remove records.

The lifecycle graph is:

```text
Todo --start--> Doing --complete--> Done --reopen--> Todo
```

No other transition is legal. In particular:

- `Done -> Doing` is not an implicit restart;
- `Todo -> Done` is not a shortcut;
- repeating `start` or `complete` is not silently idempotent;
- removal is orthogonal to lifecycle state and is always explicit.

The strict graph gives you a real invariant to encode and test. A permissive “set status to any string” API would erase the design problem.

### 3. Title contract

Task titles:

- must contain at least one non-whitespace character;
- must be no more than 120 UTF-8 bytes;
- must not contain tab, carriage-return, or newline characters;
- may otherwise contain ordinary Unicode text.

The byte limit is deliberate. Persistence is a byte protocol, and `String::len` reports UTF-8 bytes. A title containing non-ASCII characters can have fewer user-perceived characters than bytes. The course does not pretend that byte length is grapheme length. It makes one bounded storage rule explicit and documents its semantics.

The delimiter restriction belongs to the domain boundary because the selected storage protocol cannot represent those characters without escaping. In a later design, escaping or a different format could move that restriction. In this product, accepting a tab and failing during save would violate a stronger rule: successful domain construction should not create data the persistence layer cannot encode.

### 4. Identifier contract

IDs are:

- nonzero `u64` values;
- allocated monotonically;
- never reused after removal;
- restored together with allocation metadata;
- exhausted after `u64::MAX` is allocated.

A newtype prevents accidental interchange with unrelated integers. `TaskId(0)` cannot be built through the public constructor. Text parsing rejects both zero and non-integer input.

The board stores `Option<u64>` as its next allocation token. `Some(n)` means `n` can be allocated. `None` means the ID space has been exhausted. This is more precise than using zero as a sentinel because zero is already outside the valid ID domain.

### 5. Observable output

List and search output use a deterministic tabular contract:

```text
ID\tSTATUS\tPRIORITY\tTITLE
1\tdoing\thigh\tRepair parser
2\ttodo\tnormal\tWrite tests
```

An empty result prints:

```text
no tasks
```

Statistics print one stable line per status plus a total:

```text
todo\t1
doing\t0
done\t1
total\t2
```

Determinism matters for users, tests, diffs, and reproducibility. The board retains tasks in ascending ID order after reconstruction, and the serializer explicitly sorts by ID. The implementation does not rely on incidental `HashMap` order.

### 6. Command success and persistence

Commands fall into three classes.

#### Environment-independent commands

`help` and `version` do not load, create, or inspect storage. They can succeed even when the configured storage path is unreadable.

#### Read-only commands

`list`, `search`, and `stats` load storage but do not rewrite it. Merely observing state must not update timestamps or canonicalize a file as a hidden side effect.

#### Mutating commands

`add`, `start`, `done`, `reopen`, `remove`, and `rename` load, validate, mutate the in-memory board, and save exactly once after successful execution. User-facing success output is returned only after the required save succeeds. A successful domain mutation followed by a failed save is reported as failure, not success.

### 7. Exit status contract

- `0`: success;
- `2`: command grammar or command-token conversion failure;
- `1`: domain or storage failure.

The distinction allows shell callers to separate malformed invocation from an operation that was validly requested but could not be completed.

### 8. Non-contracts

The product does not promise:

- concurrent writers;
- file locking;
- crash-consistent directory synchronization on every operating system;
- Unicode normalization or locale-aware search;
- stable storage compatibility beyond the declared `TASKBOARD-V1` format;
- transaction recovery after external process termination;
- authorization, networking, or multi-user behavior.

Naming non-contracts is not an apology. It keeps the claims reviewable and prevents a small course product from acquiring fictional production guarantees.

## Architecture and Dependency Graph

### 1. Responsibility before file count

Rust modules should follow responsibility boundaries, not a rule that every type receives a file. `taskboard` uses five source modules because it has five materially different reasons to change:

```text
src/
├── lib.rs       public crate surface and executable documentation
├── model.rs     domain values, invariants, transitions, aggregate state
├── command.rs   raw argument grammar -> typed Command
├── storage.rs   versioned records, reconstruction, path I/O, commit
├── app.rs       command execution, rendering, load/execute/save orchestration
└── main.rs      process environment, stdout/stderr, exit status
```

The split is neither minimal-file dogma nor architecture theater. Combining `model` and `command` would couple domain rules to one interface. Combining `storage` and `app` would obscure whether a failure occurred while decoding, executing, or committing. Splitting each enum into its own module would add paths without adding conceptual authority.

### 2. Dependency direction

The conceptual graph is:

```text
main
  |
  v
app -----> command
  |           |
  |           v
  +-------> model
  |
  v
storage ----> model
```

`model` is the stable center. It does not know command-line arguments, files, environment variables, standard streams, or process exit codes.

`command` depends on model parsing types because a successfully parsed command contains `TaskId`, `Priority`, and `Status`, not unvalidated strings.

`storage` depends on the model because records reconstruct tasks and boards. The model does not depend on storage; its invariants can be exercised in memory.

`app` coordinates typed commands and persistent state. It renders stable output, but it delegates domain mutation to `TaskBoard` and record details to `storage`.

`main` is an effect shell. It reads `std::env::args`, resolves `TASKBOARD_FILE`, calls `run`, writes one output stream, and converts failure categories to process status.

### 3. Library first, binary second

The package provides both a library and a binary. This is not done merely to satisfy a course checklist.

The library boundary provides three benefits:

1. Domain and persistence behavior can be exercised without spawning a process.
2. Integration tests observe only public contracts, revealing accidental visibility assumptions.
3. The binary remains small enough that environment and process behavior are easy to audit.

The public surface is re-exported from `capstone/src/lib.rs`. Internal module layout is not automatically a public commitment. A consumer imports `taskboard::TaskBoard`, not `taskboard::model::TaskBoard`. Re-exporting selected types permits internal module reorganization without forcing downstream path changes.

### 4. Aggregate authority

`Task` fields are private. A caller cannot write:

```rust,ignore
// Intentionally impossible through the public API.
task.status = Status::Done;
```

All state changes pass through `TaskBoard`. This centralizes:

- lookup and not-found behavior;
- legal transition checks;
- title validation;
- monotonic ID allocation;
- task removal;
- ordering and aggregate statistics.

The board is not merely a collection wrapper. It owns invariants spanning multiple tasks and allocation metadata. That is why restoration validates duplicate IDs and next-ID consistency at the board boundary.

### 5. Parse, validate, execute, commit

The application route is staged:

```text
raw OS arguments
    -> Vec<String>
    -> parse_command
    -> Command
    -> load_path
    -> TaskBoard
    -> execute
    -> Outcome { output, changed }
    -> conditional save_path
    -> output to caller
```

Each arrow narrows uncertainty.

- Before parsing, token count and spelling are unknown.
- After parsing, command grammar is valid and primitive operands are typed.
- After loading, the complete persisted snapshot satisfies record and aggregate invariants.
- After execution, either no mutation occurred or one valid in-memory change occurred.
- After a successful commit, success output may be returned.

A common weak design collapses this route into one large `match` in `main.rs`. Such a function can work, but it makes tests and failure-state reasoning expensive. Here, each stage has a direct API and direct tests.

### 6. Ownership across layers

The architecture is also an ownership design.

- `main` owns raw argument strings, then lends a slice to `run`.
- `parse_command` borrows the slice and allocates only command data that must outlive parsing, such as joined titles and queries.
- `load_path` returns an owned `TaskBoard` because the caller must mutate it independently of the file handle.
- `execute` borrows the board mutably for one operation and consumes the typed `Command` so owned title/query payloads can move into the correct destination.
- read paths borrow tasks; removal transfers an owned `Task` to permit confirmation output without cloning its title.
- `save_path` borrows the board because serialization observes state but does not consume it.

This ownership route should be explainable without reading function bodies. The signatures carry most of the contract.

### 7. What is deliberately not abstracted

The course does not add a `Repository` trait, command-handler trait hierarchy, generic renderer, or dependency-injection container. There is only one storage implementation and one rendering policy. An abstraction with one implementation and no pressure from substitution would conceal rather than clarify.

The generic boundaries that do exist solve concrete problems:

```rust,ignore
pub fn load_from<R: BufRead>(reader: R) -> Result<TaskBoard, StorageError>;
pub fn save_to<W: Write>(writer: &mut W, board: &TaskBoard) -> Result<(), StorageError>;
```

These bounds permit files, in-memory buffers, and fault-injecting test doubles without inventing a custom trait. Standard traits already express the capability.

### 8. Architectural audit questions

Before accepting a module split, answer:

- Which invariant authority lives here?
- What external effect does this module own?
- Can it be tested without a broader layer?
- Is dependency direction inward toward stable policy?
- Does public visibility reveal behavior or implementation?
- Would combining two files merge materially different failure classes?
- Would splitting one file create paths without independent responsibility?

The final structure is justified by answers to those questions, not by resemblance to a framework template.

## Domain Model and Invariants

### 1. Newtypes as boundary types

`TaskId` wraps `u64`:

```rust,ignore
pub struct TaskId(u64);
```

The field is private. The public constructor returns `Option<TaskId>`, and `FromStr` returns a typed parse error. This means every publicly obtained `TaskId` is nonzero.

A type alias would not create that boundary:

```rust,ignore
type TaskId = u64;
```

With an alias, every `u64` is also a `TaskId`, including zero. The newtype gives the compiler a distinct type and gives the implementation one place to protect construction.

The type derives ordering and hashing because those semantics are identical to the wrapped identifier. It implements `Display` for stable user-facing rendering. It does not expose arithmetic; clients are not allocation authorities.

### 2. Closed sets use enums

Priority and status are closed domains:

```rust,ignore
pub enum Priority { Low, Normal, High }
pub enum Status { Todo, Doing, Done }
```

A string representation would permit misspellings and states that no operation understands. An enum permits exhaustive matching and makes impossible spellings unrepresentable after parsing.

The `Display` and `FromStr` implementations define a deliberate textual boundary. Debug formatting is not used as a persistence protocol. Renaming a Rust variant or changing its debug representation must not silently change stored data.

### 3. Private fields and observational APIs

A task owns its title and stores typed values:

```rust,ignore
pub struct Task {
    id: TaskId,
    title: String,
    priority: Priority,
    status: Status,
}
```

Getters return copied scalar enums or borrowed text. `title(&self) -> &str` avoids allocation and does not transfer ownership. There is no public setter for `status`. Rename is an aggregate operation because it must combine lookup with the same title contract used by add and restore.

Private fields do more than prevent style violations. They make the constructor and mutation routes auditable. If every path to a valid task is controlled, other modules can rely on task invariants rather than revalidate on every read.

### 4. Validation before mutation

Consider rename:

```rust,ignore
pub fn rename(&mut self, id: TaskId, title: String) -> Result<(), TaskError> {
    validate_title(&title)?;
    let task = self.find_mut(id)?;
    task.title = title;
    Ok(())
}
```

Validation occurs before the mutation. Therefore:

- an invalid title leaves the existing task untouched;
- a missing ID leaves the board untouched;
- a successful operation moves the owned `String` into the task without cloning.

This ordering is part of failure atomicity at the model boundary. A weaker implementation might replace the title first and then discover that it cannot be serialized. Restoring the old value would require more state and more failure paths. The correct design avoids entering an invalid state.

### 5. State transition matrix

The complete operation matrix is:

| Current state | `start` | `complete` | `reopen` |
|---|---|---|---|
| `Todo` | `Doing` | error | error |
| `Doing` | error | `Done` | error |
| `Done` | error | error | `Todo` |

Every cell deserves a test. Testing only the three successful edges does not prove the graph; six illegal edges remain. Each failing operation must also prove that the original status is preserved.

Transitions read the current status before assignment. The error records the task ID, operation name, and source status. That context supports diagnostics without forcing callers to re-run lookup after failure.

### 6. Aggregate restoration

Loading records cannot construct a board by repeatedly calling `add`. Stored IDs may contain gaps after removals, and restored statuses may be non-`Todo`. Instead, storage decodes candidate tasks and calls an internal restoration function.

Restoration validates cross-record rules:

1. every task ID is unique;
2. a present `NEXT_ID` is nonzero and greater than every stored ID;
3. an exhausted allocation token is valid only when the maximum stored ID is `u64::MAX`;
4. tasks are sorted by ID before the board becomes observable.

This is a two-level validation design:

- `Task::restore` validates one record's local title and typed fields;
- `TaskBoard::restore` validates relationships across records and metadata.

Putting duplicate detection inside `Task::restore` would be impossible because one task cannot inspect its peers. Putting title validation only in `TaskBoard::restore` would make single-task construction less trustworthy. Each invariant belongs at the narrowest authority with enough information.

### 7. Identifier exhaustion

The next ID is stored as `Option<u64>`. Add performs:

1. reject `None` as `IdExhausted`;
2. construct the current `TaskId`;
3. compute the next token with `checked_add`;
4. push the task.

When the current raw ID is `u64::MAX`, `checked_add(1)` returns `None`. The maximum ID is still allocated once. Every later add fails. This behavior is precise and testable.

Using wrapping arithmetic would silently allocate zero, violating the ID type. Panicking arithmetic would turn a recoverable capacity condition into process termination. Saturating arithmetic would reuse `u64::MAX`, creating duplicates. `checked_add` maps the numerical boundary into the domain model.

### 8. Collection choice

The board uses `Vec<Task>`. Lookup and removal are linear. For this bounded local course application, the tradeoff is acceptable:

- deterministic ordered iteration is direct;
- storage reconstruction can sort once;
- ownership and borrowing behavior remains visible;
- no second index must be kept consistent;
- expected board sizes are small.

A `HashMap<TaskId, Task>` would improve average lookup but make stable rendering require a separate ordering step and introduce an unordered collection before it is needed. A `BTreeMap` would provide order and logarithmic lookup but place the key outside the task or duplicate it conceptually. Those designs may become appropriate under measured scale. Foundations should not pretend a more sophisticated container is automatically a better design.

### 9. Search semantics

Search is documented as ASCII case-insensitive. It normalizes the query once and each title during comparison. This is not full Unicode case folding, locale-aware matching, normalization, tokenization, or indexing.

The limitation is explicit. A course should not claim “case-insensitive Unicode search” because `to_ascii_lowercase` happens to handle English examples. The selected semantics are small, deterministic, and sufficient to teach borrowed iteration and closure capture.

### 10. Domain defense checklist

You should be able to answer:

- Which constructors can create `TaskId`?
- Why can no public caller construct an arbitrary `Task`?
- Why is status not a string?
- Why does rename accept `String` rather than `&str`?
- Why is title validation shared by add, rename, and restoration?
- Which failed operations preserve board equality?
- What makes restored next-ID metadata valid?
- Which operation transfers ownership of a complete task?
- Where does ID ordering become guaranteed?
- Which complexity costs follow from `Vec<Task>`?

An answer that says only “the compiler checks it” is insufficient. The compiler enforces type and borrow rules; the program's own constructors and methods enforce domain policy.

## Command Grammar and Parsing

### 1. The command enum is the grammar result

Raw command-line arguments are strings. Application execution should not continue to rediscover their meaning. Parsing converts them once into:

```rust,ignore
pub enum Command {
    Add { priority: Priority, title: String },
    List { status: Option<Status> },
    Start(TaskId),
    Done(TaskId),
    Reopen(TaskId),
    Remove(TaskId),
    Rename { id: TaskId, title: String },
    Search(String),
    Stats,
    Help,
    Version,
}
```

Each variant contains exactly the data required by that operation. There is no `Command` struct with optional `id`, optional `title`, optional `priority`, and a string operation name. Such a struct would allow nonsensical combinations and force execution to validate grammar again.

The enum acts as a proof: if `parse_command` returns `Ok(Command::Start(id))`, an ID token was supplied and converted to a valid nonzero `TaskId`.

### 2. Grammar table

| Command | Arity | Typed result | Mutates board |
|---|---:|---|---|
| `add` | priority + one or more title tokens | `Add { Priority, String }` | yes |
| `list` | zero or one status | `List { Option<Status> }` | no |
| `start` | exactly one ID | `Start(TaskId)` | yes |
| `done` | exactly one ID | `Done(TaskId)` | yes |
| `reopen` | exactly one ID | `Reopen(TaskId)` | yes |
| `remove` | exactly one ID | `Remove(TaskId)` | yes |
| `rename` | ID + one or more title tokens | `Rename { TaskId, String }` | yes |
| `search` | one or more query tokens | `Search(String)` | no |
| `stats` | zero | `Stats` | no |
| `help` | zero | `Help` | no |
| `version` | zero | `Version` | no |

Arity is strict. Ignoring extra arguments would turn typos into surprising behavior. For example, `taskboard done 4 now` is not interpreted as `done 4`; it is rejected.

### 3. Borrow input, own output

The parser signature is:

```rust,ignore
pub fn parse_command(arguments: &[String]) -> Result<Command, CommandParseError>
```

The input is borrowed because parsing does not need to consume the caller's argument vector. The output owns any text that execution must retain or move:

- an add title is joined into an owned `String` and later moved into the board;
- a rename title is owned for the same reason;
- a search query is owned by the command and borrowed during execution.

A parser returning `Command<'a>` full of borrowed slices could avoid some allocations, but it would couple command lifetime to the raw argument storage and introduce lifetime parameters before they solve an important course problem. The allocation cost is tiny and the ownership boundary is clearer.

### 4. Parse primitive boundary types early

ID, priority, and status tokens are converted during command parsing through `FromStr`. Execution does not receive `"high"` and decide what it means. This prevents stringly typed domain code and centralizes textual spelling.

Errors preserve their category:

```text
CommandParseError::InvalidId(...)
CommandParseError::InvalidPriority(...)
CommandParseError::InvalidStatus(...)
```

The command error implements `Error::source` for wrapped parse errors. A caller can inspect the chain instead of receiving one flattened message.

### 5. Missing, unexpected, and invalid are different

These invocations fail for different reasons:

```text
taskboard start             # missing argument
taskboard start 1 extra     # unexpected argument
taskboard start zero        # invalid ID
taskboard sparkle 1         # unknown command
```

The distinction improves diagnostics and tests. It also trains you to define error taxonomies by recoverable action rather than by one catch-all string.

`EmptyTitle` and `EmptyQuery` catch assembled text that contains only whitespace. Domain title validation still runs during execution because command parsing is not the only possible caller of `TaskBoard::add` or `rename`. The command layer checks grammar; the model remains the final invariant authority.

### 6. Aliases are grammar, not preprocessing

`--help`, `-h`, `--version`, and `-V` are accepted as names in the same top-level match. They still reject extra operands. This is preferable to blindly scanning arguments for a help flag, which might make `taskboard add high -h` print help rather than add a task titled `-h`.

The product uses a simple grammar: the first token is always the command name. That rule is documented and tested.

### 7. Parsing rename as an impact example

The final feature demonstrates how a grammar change propagates:

1. Add a `Command::Rename { id, title }` variant.
2. Add one help line.
3. Route the `rename` name.
4. Require an ID and at least one title token.
5. parse ID through `TaskId::from_str`.
6. join the remaining tokens into owned text.
7. distinguish missing title, invalid ID, and blank title.
8. add arity and conversion tests.
9. update execution exhaustively—the compiler identifies the missing match arm.

The enum turns a cross-layer feature into a compiler-assisted checklist. When the new variant is added, every exhaustive match over `Command` must acknowledge it.

### 8. What the parser does not do

The parser does not:

- read environment variables;
- open storage;
- look up task IDs;
- validate lifecycle transitions;
- print errors;
- exit the process;
- expand shell quotes.

The shell has already produced argument tokens before Rust receives them. Quote handling belongs to the shell, not `parse_command`. Whether an ID exists requires board state and belongs to execution. Keeping those boundaries separate makes pure parser tests possible.

### 9. Parser test matrix

For every command, tests should cover:

- minimum valid form;
- representative valid full form;
- missing each required operand;
- extra operand where forbidden;
- invalid typed token;
- whitespace-only joined text where relevant;
- exact owned title/query assembly;
- aliases where relevant.

Tests should compare typed variants, not merely `is_ok()`. A parser can return success with the wrong title or wrong status and still satisfy a weak success-only assertion.

## Storage Protocol and Reconstruction

### 1. Why a manual protocol

The capstone intentionally uses no serialization crate. The purpose is not to argue that manual text formats are preferable in production. The purpose is to expose the responsibilities a serializer normally absorbs:

- version identification;
- record grammar;
- primitive conversion;
- delimiter policy;
- physical line context;
- duplicate metadata detection;
- aggregate validation;
- canonical output;
- I/O error propagation.

Once you has implemented those responsibilities, later use of `serde` is informed rather than magical.

### 2. Version 1 grammar

The protocol is line-oriented UTF-8 text:

```text
TASKBOARD-V1
NEXT_ID\t<positive-u64 | exhausted>
TASK\t<id>\t<status>\t<priority>\t<title>
...
```

In EBNF-like notation:

```text
file        = header, newline, next-id-record, newline, { task-record, newline } ;
header      = "TASKBOARD-V1" ;
next-id-record = "NEXT_ID", tab, (positive-u64 | "exhausted") ;
task-record = "TASK", tab, task-id, tab, status, tab, priority, tab, title ;
status      = "todo" | "doing" | "done" ;
priority    = "low" | "normal" | "high" ;
```

The loader permits `NEXT_ID` to appear among task records but requires exactly one instance. The writer always emits it immediately after the header. Load acceptance and canonical save output are distinct concerns.

### 3. Physical line numbers

The loader enumerates physical lines and reports one-based positions. The header is line 1. Therefore the first record is line 2.

Line context is attached when a record-specific decoder fails:

```text
line 3: invalid status `flying`; expected todo, doing, or done
```

The record error itself does not need to know where it came from. `StorageError::InvalidRecord { line, source }` adds file-level context while preserving the record error as a source.

Blank lines are not silently skipped. In this strict format, a blank line is an unknown empty record tag. Silent skipping would make corruption or unintended edits less visible and would weaken canonical compatibility tests.

### 4. Decode locally, validate globally

Each task line is split into exactly five fields and converted:

```text
TASK -> TaskId -> Status -> Priority -> validated title
```

That produces a valid individual `Task`. The loader accumulates all tasks and the next-ID token, then calls board restoration. Only the aggregate can detect:

- duplicate task IDs;
- next ID colliding with or preceding retained IDs;
- exhausted metadata without a maximum allocated ID.

The loader does not mutate an existing live board as each line arrives. It constructs temporary candidate state. If line 800 is invalid, no partially updated board escapes.

### 5. Missing file is narrow policy

`load_path` treats only `io::ErrorKind::NotFound` as an empty new board. Other open failures—permission denied, path is a directory, I/O faults—are returned with path context.

This distinction prevents a dangerous pattern:

```rust,ignore
// Wrong: every failure becomes empty state.
let board = load_path(path).unwrap_or_default();
```

If permission failure became an empty board, a later successful save could overwrite or replace important state. Recovery policy must be based on a specific failure kind, not convenience.

### 6. Canonical save output

`save_to` writes:

1. the exact version header;
2. one next-ID metadata line;
3. tasks in ascending ID order.

The function accepts `&TaskBoard` because serialization observes rather than consumes state. It accepts `&mut W where W: Write` so tests can use `Vec<u8>` and fault-injecting writers.

Canonical order means equivalent boards produce identical bytes. This supports:

- exact fixture tests;
- readable version-control diffs;
- predictable CLI behavior;
- corruption comparison;
- future compatibility migration tests.

### 7. Path commit sequence

`save_path` performs:

```text
create unique same-directory temporary file
    -> encode board
    -> flush buffered writer
    -> sync temporary file contents/metadata
    -> close writer
    -> rename temporary path to target path
```

On any write, flush, or sync failure, it closes and attempts to remove the temporary file. On rename failure, it removes the temporary file and returns contextual I/O failure.

Using the same directory reduces cross-filesystem rename problems. `create_new(true)` prevents accidental reuse of an existing temporary path. The filename combines target name, process ID, timestamp, and bounded collision attempts.

### 8. The durability boundary

It would be inaccurate to call this universally transactional or fully crash durable.

- Rename replacement behavior differs across operating systems, especially when the target exists.
- Synchronizing the temporary file does not necessarily synchronize the containing directory entry.
- No file lock prevents concurrent writers from overwriting each other's work.
- Abrupt process or machine failure at specific points may leave platform-dependent results.

The capstone makes a stronger guarantee than direct truncate-and-write: encoding failure does not destroy the existing target, and successful mutation output is withheld until the save route succeeds. Later systems-programming courses can add directory syncing, platform-specific replacement semantics, locks, journaling, or database transactions.

### 9. Compatibility tests
A useful storage test suite includes:

- exact empty-board encoding;
- exact populated canonical fixture;
- load/save/load semantic round trip;
- unsupported header;
- empty input;
- missing next-ID metadata;
- duplicate next-ID metadata;
- wrong field count;
- invalid ID, status, priority, and title;
- duplicate task ID;
- inconsistent allocation metadata;
- blank and unknown records;
- missing file policy;
- fault-injecting writer;
- failed path commit cleanup.

Round-trip alone is weak. An encoder and decoder can share the same defect and still round-trip. Exact fixtures and independently constructed malformed inputs constrain both sides.

### 10. Why rename does not change the format

Rename changes only a title field already represented by `TASKBOARD-V1`. The grammar and meaning of the field remain the same, so the storage version does not change.

Version bumps are for incompatible representation or semantic changes, not every application feature. Unnecessary version increments create migration work without protecting compatibility.

## Errors, Commits, and Failure State

### 1. Error types follow boundaries

The capstone does not use one application-wide string error. It defines errors where recovery meaning changes:

```text
primitive parse errors
    -> command parse errors
    -> task domain errors
    -> record errors
    -> storage errors
    -> run errors
```

The hierarchy is not a class inheritance tree. Enums compose concrete failure variants and wrap source errors.

- `CommandParseError` describes invalid invocation grammar.
- `TaskError` describes invariant or transition failure.
- `RecordError` describes one malformed storage record.
- `StorageError` adds line, snapshot, path, and I/O context.
- `RunError` classifies top-level command, storage, and task failure for process behavior.

### 2. Display is for users; structure is for callers

Each error implements `Display` with actionable text. Tests and callers should still prefer variant matching where category matters.

This distinction is important:

```rust,ignore
assert!(matches!(error, StorageError::InvalidRecord { line: 3, .. }));
```

is stronger and less brittle than asserting one complete English sentence. Text tests remain useful for selected user-facing diagnostics, but structured variants carry semantic stability.

Wrapped errors implement `Error::source`. This preserves causal chains for diagnostics and future tooling. Converting everything with `format!("{error}")` would discard that structure.

### 3. The question-mark operator is propagation, not handling

`?` means:

1. if the result is `Ok`, extract the value;
2. if it is `Err`, convert as required by `From` and return from the current function.

It does not log, print, retry, or recover. In the application route, each layer adds context or converts category before propagation.

For example, path opening adds the operation and path because `io::Error` alone may say only “permission denied.” Record decoding adds a physical line. Top-level `RunError` adds the boundary label and exit category.

### 4. In-memory failure atomicity

A domain operation is failure-atomic when an error leaves observable model state unchanged.

Examples:

- `start` checks source status before assignment;
- `complete` checks source status before assignment;
- `rename` validates the new title before replacing the old one;
- `remove` finds the index before calling `Vec::remove`;
- `add` validates the title and confirms an available ID before pushing.

Tests should capture state before failure and compare after failure, not only assert `is_err()`.

### 5. Application commit protocol

`run` follows this order:

```text
parse -> special-case help/version -> load -> execute -> if changed, save -> return output
```

The `Outcome` contains:

- owned user-facing output;
- a Boolean declaring whether persistent state changed.

Read-only outcomes skip saving. Mutating outcomes save before the output is returned. This prevents a caller from receiving “added task 4” when the board could not be persisted.

The in-memory board may have changed before `save_path` fails, but it is local to the failed `run` call and is then dropped. The persistent source remains authoritative. This is a practical unit-of-work boundary.

### 6. Failure-state table

| Stage | Example failure | Board escaped? | Target file changed? | Exit class |
|---|---|---:|---:|---:|
| parse | invalid priority | no board loaded | no | 2 |
| load/open | permission denied | no | no | 1 |
| load/decode | invalid line 3 | no valid board returned | no | 1 |
| execute/lookup | unknown task ID | local board unchanged | no | 1 |
| execute/transition | `Todo -> Done` | local board unchanged | no | 1 |
| execute/rename validation | blank title | local board unchanged | no | 1 |
| save/write temp | device/write failure | local board later dropped | intended target preserved | 1 |
| save/rename | commit failure | local board later dropped | platform-dependent target remains prior state | 1 |
| stdout write | broken pipe after commit | state may already be committed | yes | process output failure |

The final row exposes an unavoidable ordering decision. For a mutating command, persistence must occur before success output. If stdout fails afterward, the state may be committed although the user did not receive confirmation. Reversing the order would produce the opposite and generally worse false-success problem.

### 7. Exit status ownership

`RunError::exit_code` maps command errors to 2 and storage/domain errors to 1. `main` owns actual process exit because library code should not terminate its caller.

The binary also handles stdout failure separately. It writes diagnostics to stderr and exits nonzero. The library remains reusable in tests and other processes.

### 8. Panics and `expect`

Production library code contains no direct `unwrap`, `expect`, `panic!`, `todo!`, or `unimplemented!`. This is not a claim that those constructs are universally forbidden in Rust. It is a capstone discipline:

- user input is expected to be invalid sometimes;
- files and writers can fail;
- domain operations can be rejected;
- every such path has a recoverable result type.

Tests use `expect` to make fixture assumptions readable. A failing test should stop and report why setup was expected to succeed. The production policy audit deliberately scans `capstone/src`, not test code.

### 9. Error audit method

For each fallible function, record:

1. What can fail?
2. Is the failure expected under ordinary use?
3. Which layer has enough context to describe it?
4. Does propagation preserve the source?
5. What state existed before the operation?
6. What state is observable after error?
7. Is retry meaningful?
8. Which test proves the answer?

An error type is complete only when its state semantics are understood. A polished message without state analysis is not robust error handling.

## Testing and Proof Matrix

### 1. Tests are assigned to contracts

A large undifferentiated test suite can still leave important boundaries unproved. `taskboard` uses several test levels because each can observe different facts.

| Boundary | Location | What it can prove |
|---|---|---|
| private module unit | `src/*.rs` | internal invariants, helper edge cases, exhaustive state cells |
| public crate integration | `tests/public_behavior.rs` | downstream usability without private field access |
| persistence integration | `tests/persistence.rs` | fixtures, path policy, corruption, commit cleanup, generic I/O |
| real process | `tests/cli.rs` | argument/environment/stdout/stderr/exit behavior across invocations |
| documentation | `src/lib.rs` rustdoc | examples compile as external-looking consumers |
| static policy | `scripts/check_rust_policy.py` | forbidden production shortcuts remain absent |
| course structure | `scripts/check_course.py` | required authored and executable surfaces exist |

A unit test cannot prove exit status. A CLI test can prove it, but using only CLI tests makes domain failures harder to isolate. The levels are complementary.

### 2. Domain test matrix

The model tests cover:

- zero and malformed task IDs;
- priority/status text round trips;
- blank, oversized, and delimiter-unsafe titles;
- monotonic ID allocation;
- every legal state transition;
- every illegal source/operation combination;
- not-found behavior;
- rename success and rejected-title state preservation;
- remove ownership transfer;
- search/filter semantics;
- state counts;
- duplicate and invalid restored metadata;
- ID exhaustion.

The state-transition matrix should be data-driven or at least explicit enough that every cell can be audited. Three success tests are not a complete transition proof.

### 3. Parser tests

Parser tests compare exact `Command` values. They cover:

- joined title ownership;
- optional list status;
- strict ID-command arity;
- rename's ID-plus-title grammar;
- help/version aliases;
- missing versus unknown command;
- invalid priority/status/ID categories;
- empty assembled query/title.

The parser is pure, so tests need no file setup. That purity is an architectural payoff.

### 4. Storage tests
Three kinds of evidence are required.

#### Exact fixtures

An exact expected byte string proves canonical serialization. It detects field reordering, spelling drift, missing metadata, and unstable order.

#### Semantic round trips

Load-save-load tests prove that public domain values survive encoding. They do not by themselves prove compatibility because both functions might share a defect.

#### Corruption cases

Independently authored malformed fixtures prove strict rejection and contextual error categories. Duplicate IDs and inconsistent `NEXT_ID` values test aggregate validation rather than only record parsing.

The fault-injecting writer proves that generic write failure is propagated with context and source. Path tests prove the missing-file rule and temporary cleanup after a failed rename.

### 5. Public integration tests

`public_behavior.rs` imports only re-exported crate items. It cannot access task fields or internal restoration functions. This tests whether the public API is sufficient for normal use without being excessive.

Typical assertions include:

- complete lifecycle through methods;
- illegal transition preserves status;
- rename works without field access;
- codec round trip preserves exposed values;
- typed execution distinguishes changed from read-only outcomes.

A public test is also an API design review. If it requires making internal fields public, the better question is whether a small behavior method or getter is missing.

### 6. Real-process tests

CLI tests use `env!("CARGO_BIN_EXE_taskboard")` to invoke the binary built by Cargo. Every test creates a unique temporary directory and sets `TASKBOARD_FILE`, preventing interference with user data or parallel tests.

They verify:

- persistence across independent processes;
- exact stdout for stable reports;
- stderr diagnostics;
- exit status 0, 1, and 2;
- read/search/filter/remove behavior;
- rename across storage boundaries;
- monotonic IDs after removal;
- failed transition and failed rename preserve file bytes;
- malformed storage line context;
- help/version do not touch storage.

The isolation harness is part of the test's correctness. A CLI test that writes `.taskboard.db` in the repository can become order-dependent and destructive.

### 7. Documentation tests

Crate-level examples are compiled by rustdoc as external-looking code. They demonstrate:

- constructing a board and transitioning a task;
- parsing a typed command;
- in-memory save and load through standard I/O traits.

Documentation tests are not a substitute for behavioral tests. They prove that public examples stay synchronized with exported names and signatures.

### 8. Negative compiler evidence

The `diagnostics` crate uses `compile_fail` rustdoc examples for representative ownership and borrowing violations. Negative tests matter because many foundational claims are about code Rust must reject.

A course should not merely show a screenshot of an error from one compiler version. A compile-fail example keeps the rejected relationship executable while allowing exact wording to evolve.

### 9. Proof commands

The root proof route separates concerns:

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

`cargo check` is not a test replacement. Formatting is not semantic proof. Clippy is not a compiler. Documentation build is not public behavior. Each route has a bounded claim.

### 10. Mutation-oriented review

A useful final audit asks whether plausible defects would be detected:

| Seeded defect | Expected catching evidence |
|---|---|
| `complete` accepts `Todo` | model matrix, CLI failure test |
| loader reports line 2 instead of 3 | storage unit/integration test |
| serializer uses collection iteration order | exact canonical fixture |
| unknown open error becomes empty board | missing-path narrow-policy test |
| rename assigns before validation | model/public/CLI preservation tests |
| mutating command returns output before save | application/CLI failure design test |
| help omits rename | help/parser documentation audit or CLI help assertion |
| removed IDs are reused | model and CLI monotonic-ID tests |

If no test would catch a defect, the contract is not yet proved. This is more meaningful than maximizing raw test count.

## Code-Reading Walkthrough

This chapter gives a disciplined order for reading the reference implementation. Do not begin with `main.rs` and scroll randomly through every call. Read from stable policy outward.

### Pass 1 — Public promise

Open `capstone/src/lib.rs`.

Record:

- crate purpose from the top-level documentation;
- the three executable examples;
- private module declarations;
- all re-exported public items.

Do not inspect module bodies yet. From names and signatures alone, write the expected responsibilities of `TaskBoard`, `Command`, `StorageError`, `execute`, and `run`.

Question: could a downstream consumer construct a `Task` with arbitrary status? The re-export list alone does not answer; you will verify field privacy in the next pass.

### Pass 2 — Domain types and invariants

Read `capstone/src/model.rs` in this order:

1. `TaskId` construction and parsing;
2. `Priority` and `Status` textual boundaries;
3. `Task` fields and getters;
4. `TaskError` taxonomy;
5. `TaskBoard` representation;
6. restoration;
7. add/find/mutation operations;
8. read iterators and statistics;
9. title validation;
10. unit tests.

Maintain an invariant table:

| Invariant | Authority | Established by | Rechecked by |
|---|---|---|---|
| ID nonzero | `TaskId` | `new`, `FromStr`, internal trusted construction | storage parse |
| title safe | model | add, rename, restore | not needed on reads |
| unique IDs | board | allocation, restore | restore only |
| legal status | enum + transitions | parse/restore, methods | exhaustive matches |
| next ID ahead | board | add, restore | restore |

Look specifically for mutation ordering. For every `&mut self` method, mark the first statement that can change state and every fallible operation before it.

### Pass 3 — Command grammar

Read `capstone/src/command.rs`.

First compare `Command` to the help string. Every supported operation should appear in both. Then inspect `CommandParseError`. Ask whether each error category gives the user a different corrective action.

Trace three inputs manually:

```text
add high Repair the codec
rename 7 Rebuild storage proof
list done
```

For each token, record whether it is borrowed, parsed, joined, or moved. Confirm that the returned command owns text needed after parsing.

Then trace three failures:

```text
start
start zero
list todo extra
```

Identify the exact helper returning each error.

### Pass 4 — Storage reconstruction

Read `capstone/src/storage.rs` in four sections.

#### Error layering

Map `RecordError` into `StorageError`. Note which variants provide sources and which are leaf policy errors.

#### Loading

Trace enumeration beginning at the header. Confirm the one-based line formula after consuming line 1. Mark local record decoding versus aggregate restoration.

#### Saving

Record canonical field order and task ordering. Confirm that `save_to` borrows the board and is generic over `Write`.

#### Path commit

Draw the temporary-file state machine:

```text
Absent -> Created -> Encoded -> Flushed -> Synced -> Renamed
             \          \          \          \
              +---------- failure cleanup ------+
```

Identify what is attempted on every failure edge and what remains platform-dependent.

### Pass 5 — Application orchestration

Read `capstone/src/app.rs`.

Compare `execute` and `run`:

- `execute` has no path I/O and operates on a borrowed board;
- `run` parses, loads, executes, conditionally commits, and returns output.

For every `Command` variant, classify:

- required board access;
- possible domain error;
- whether `Outcome::changed` is correct;
- exact output contract.

Then inspect the special handling of help and version. Explain why it occurs before storage load.

### Pass 6 — Effect shell

Read `capstone/src/main.rs`.

The file should be small. Identify:

- OS argument ownership;
- default storage path policy;
- stdout write and flush behavior;
- stderr diagnostics;
- mapping from `RunError` to exit status.

Look for domain or record logic. Finding any would be a boundary defect.

### Pass 7 — Evidence

Read tests in this order:

1. model unit tests;
2. command unit tests;
3. storage unit tests;
4. app unit tests;
5. `capstone/tests/public_behavior.rs`;
6. `capstone/tests/persistence.rs`;
7. `capstone/tests/cli.rs`;
8. crate documentation tests.

For each test, name the contract it proves and a defect it would catch. Mark redundant tests only when they observe the same contract at the same boundary. The same behavior tested at a model and process boundary is not automatically redundant; it can prove both local rule and end-to-end wiring.

### Final reading exercise

Without code access, reconstruct these signatures approximately:

```text
TaskBoard::add
TaskBoard::find
TaskBoard::rename
TaskBoard::filtered
parse_command
load_from
save_to
execute
run
```

Exact formatting is unimportant. Ownership, mutability, generic bounds, and result categories must be correct. Then reopen the source and explain every difference.

## Final Independent Feature — `rename`

### 1. Behavioral specification

The final capstone change is intentionally small in user-visible scope:

```text
taskboard rename <id> <title...>
```

Its value is cross-layer impact. The feature must satisfy:

- ID parses as a positive `TaskId`;
- at least one title token is required;
- the title is owned after parsing;
- the same invariant used by add and restore applies;
- missing ID and invalid title are distinct domain outcomes;
- failure leaves model and persisted bytes unchanged;
- success changes only the title;
- list and search immediately observe the new title;
- the existing storage version remains valid;
- help, documentation, and tests are updated.

### 2. Behavior matrix before code

| Case | Expected result | Model changed | File rewritten |
|---|---|---:|---:|
| valid ID + valid title | success | title only | yes |
| malformed ID token | command error | no board loaded | no |
| zero ID | command error | no board loaded | no |
| missing title tokens | command error | no board loaded | no |
| whitespace title | domain error after parsing | no | no |
| delimiter title | domain error | no | no |
| oversized title | domain error | no | no |
| unknown valid ID | domain not-found | no | no |
| storage load failure | storage error | no valid board | no |
| save failure after valid rename | storage error | local board dropped | prior target intended preserved |

This matrix distinguishes parser validation from model validation. A shell argument containing spaces may arrive as one nonempty token whose trimmed content is blank. The parser rejects assembled blank text, but the model remains authoritative because library callers can bypass the CLI.

### 3. Impact matrix

| Layer | Required change | Why |
|---|---|---|
| domain | `TaskBoard::rename` | invariant and lookup authority |
| command model | new enum variant | typed operation representation |
| grammar | parse ID plus remaining title | raw tokens become valid command |
| help | one command line | public interface consistency |
| execution | exhaustive match arm | invoke model, mark changed |
| storage | no schema change | title field already exists |
| unit tests | parser + model + app | local contracts |
| public test | rename without field access | API sufficiency |
| persistence test | round trip renamed title | format integration |
| CLI test | multi-process command | real wiring and commit |
| failure test | file bytes before/after rejected rename | persistence consequence |
| docs | command and architecture references | executable/public contract |

Writing this matrix first prevents the common failure of implementing one method and forgetting help, exit behavior, or persistence evidence.

### 4. Ownership design

The parser constructs an owned title:

```rust,ignore
Command::Rename { id, title: String }
```

Execution consumes the command and moves that string into `TaskBoard::rename`. The model validates by borrowing `&title`, finds the mutable task, and then moves the string into the field.

No clone is required. A signature taking `&str` would force the model to allocate a new `String` because the task must own its title after the call returns. Accepting `String` advertises ownership transfer and allows the caller's existing allocation to become the stored value.

### 5. Mutation ordering

The model method validates before obtaining the mutable task and assigning:

```rust,ignore
validate_title(&title)?;
let task = self.find_mut(id)?;
task.title = title;
```

This gives two failure-atomic paths:

- invalid title returns before lookup/mutation;
- missing task returns before assignment.

The order could be lookup then validation and still preserve state, but validation first shortens the mutable borrow and states that title validity is independent of task existence. Error precedence is therefore defined: when both ID is absent and title invalid, invalid title is reported first. That choice should be documented or tested if callers depend on it.

### 6. Compiler assistance

Adding `Command::Rename` makes the `execute` match non-exhaustive. The compiler points to the application boundary that must acknowledge the feature. It cannot identify stale help prose or missing CLI tests. Type exhaustiveness and repository audit complement each other.

This illustrates a broader principle:

> Model closed operation sets with enums so the compiler can identify semantic propagation points, then use tests and documentation audits for non-code surfaces.

### 7. Storage version reasoning

A rename updates the value of an existing title field under the same constraints. It does not add a field, change record order, reinterpret text, or alter allocation semantics. Therefore `TASKBOARD-V1` remains the correct format.

A schema version is not an application release number. Incrementing it for every feature would make backward compatibility noisy and meaningless.

### 8. Required regression tests
At minimum:

- parser returns exact `Command::Rename` with joined title;
- parser rejects absent title and invalid ID;
- model changes a valid title;
- invalid title preserves previous title;
- unknown ID returns `TaskError::NotFound`;
- typed execution marks successful rename as changed;
- public consumer can rename without field access;
- CLI invocation persists the new title across another process;
- rejected rename leaves storage bytes identical;
- help contains the command;
- storage round trip preserves the renamed value.

### 9. Review questions

- Why does the command own the title?
- Why does the board method take `String`?
- What error wins when both title and ID are invalid?
- Why is no new error variant required?
- Which match becomes non-exhaustive?
- Why does the storage version remain 1?
- Which test proves no file rewrite on failure?
- Which test proves private fields are not an obstacle?
- What would need to change for title history or undo?

The feature is complete only when these answers and the executable evidence agree.

## Defense and Evaluation

The final defense is a technical examination, not a product demonstration. You must reason without relying on compiler trial-and-error for every answer.

### 1. Ownership defense

Explain each signature and predict the caller's usable values afterward:

```rust,ignore
fn add(&mut self, priority: Priority, title: String) -> Result<TaskId, TaskError>;
fn find(&self, id: TaskId) -> Option<&Task>;
fn rename(&mut self, id: TaskId, title: String) -> Result<(), TaskError>;
fn remove(&mut self, id: TaskId) -> Result<Task, TaskError>;
fn save_to<W: Write>(writer: &mut W, board: &TaskBoard) -> Result<(), StorageError>;
```

Required themes:

- why copied enums and IDs do not move ownership burdens;
- why titles are owned at persistence boundaries;
- why read APIs expose references rather than cloned tasks;
- why remove returns ownership;
- how the iterator returned by search remains tied to the board borrow;
- why save borrows rather than consumes the board.

### 2. Type-model defense

Answer:

1. What invalid values does `TaskId` prevent?
2. What invalid combinations does `Command` prevent?
3. What contradictory states would Boolean task flags allow?
4. Why are `Status` and `Priority` separate enums?
5. Why is `Option<Status>` appropriate for list filtering?
6. Why is ID exhaustion represented by `Option<u64>` internally but by `TaskError` publicly?
7. Which invariants are local to one task and which require the board?

### 3. Failure-state defense

For each stage—parse, load, execute, save, output—state:

- possible errors;
- observable model state;
- persistent state;
- error category;
- exit status;
- evidence.

The examiner may inject a fault. Examples:

- malformed status on line 93;
- permission-denied storage path;
- `done 4` when task 4 is `Todo`;
- valid rename followed by temporary-file write failure;
- stdout broken after a successful commit.

You must not claim rollback beyond what the implementation proves.

### 4. Parsing and protocol defense

Reconstruct the command grammar and storage grammar. Explain why:

- shell quoting is outside parser responsibility;
- extra operands are rejected;
- textual spellings use `Display`/`FromStr` rather than debug output;
- line numbers are attached outside the record decoder;
- blank records are rejected;
- round trip is not sufficient compatibility proof;
- rename does not require a storage version increment.

### 5. Architecture defense

Draw the dependency graph and answer:

- Why does model not depend on command?
- Why does storage depend on model?
- What belongs in app rather than main?
- Why is `run` separate from `execute`?
- Why is a custom repository trait absent?
- Why is `Vec<Task>` acceptable here?
- Which public re-exports are necessary?
- Which types or functions must remain private?

### 6. Test defense

Given a defect, name the narrowest test that should catch it and one broader regression test:

| Defect | Narrow evidence | Broader evidence |
|---|---|---|
| invalid transition mutates first | model unit | CLI byte-preservation |
| parser accepts extra operand | command unit | CLI exit 2 |
| storage loses line context | storage unit | malformed-file CLI |
| public fields required by client | public integration | rustdoc consumer example |
| save order changes | exact storage fixture | process persistence output |
| help is stale | command/help assertion | CLI help assertion/docs build |

Explain why test count alone is not an adequacy metric.

### 7. Independent code prediction

The examiner supplies short programs involving:

- moved `String` values;
- overlapping mutable/shared borrows;
- `iter`, `iter_mut`, and `into_iter`;
- `Option<&T>`;
- `Result` propagation;
- generic `Read`/`Write` bounds;
- a two-input lifetime relationship;
- module privacy.

For each, predict compile success and explain the rule before using the compiler.

The reference proof requires:

- course structural audit passes;
- local links resolve;
- formatting passes;
- all targets type-check;
- Clippy warnings are denied under the course lint policy;
- unit, integration, CLI, and doc tests pass;
- rustdoc builds;
- release build succeeds;
- capstone production policy finds no forbidden shortcut;
- no malformed fixture is accepted as empty state;
- final rename behavior is implemented and tested.

## Known Limits and the Next Course

A serious course ends by identifying the exact frontier of its proof.

### 1. Concurrency

`taskboard` assumes one writer at a time. Two processes can load the same snapshot, make independent changes, and race to replace the file. The later writer may overwrite the earlier writer's update.

A stronger design may require:

- advisory or mandatory locking;
- compare-and-swap generation metadata;
- append-only journaling;
- a transactional database;
- conflict detection and merge policy.

Those are not solved by Rust ownership. Ownership protects memory relationships within a process; it does not serialize independent processes.

### 2. Durability and platform behavior

The temporary-file route reduces truncation risk but does not establish a universal crash-consistency theorem. Directory entry synchronization, target replacement, permissions, metadata preservation, and Windows/Unix differences require systems-level analysis.

Course 6 will revisit file descriptors, syscalls, durability, paths, permissions, and platform-specific abstractions. Course 9 will connect those choices to production operations and observability.

### 3. Unicode text semantics

Titles accept UTF-8, but:

- maximum length is bytes, not grapheme clusters;
- search is ASCII case-insensitive only;
- canonical normalization is not applied;
- locale-sensitive comparison is absent.

The behavior is documented, deterministic, and limited. A future text-heavy product would need explicit Unicode requirements and probably ecosystem crates.

### 4. Data structure scale

Lookup, search, and removal over `Vec<Task>` are linear. That is acceptable for the course workload. Larger boards might use indexed structures, but every additional index creates consistency obligations and potentially more complex borrowing.

Performance work should follow measurement. Course 9 covers benchmarking, profiling, allocation, cache behavior, and data-oriented tradeoffs.

### 5. Error ergonomics

The capstone manually implements standard error traits. Production applications may use libraries to reduce boilerplate and attach context. The course deliberately postpones that convenience until you understands source chains, conversion, and boundary taxonomies.

### 6. Generic and trait depth

The course uses foundational generic I/O and standard conversion/display traits. It does not cover:

- trait objects and object safety;
- associated type architecture;
- generic associated types;
- higher-ranked trait bounds;
- blanket-implementation coherence strategy;
- typestate APIs;
- advanced `impl Trait` capture rules.

Those belong principally to Course 3.

### 7. Lifetimes and memory

The capstone relies mostly on lifetime elision and short borrowed views. It does not teach:

- references stored across complex owner graphs;
- self-referential designs;
- variance;
- drop checking;
- smart pointers and reference cycles;
- interior mutability;
- pinning;
- unsafe lifetime invariants.

Course 2 owns that depth. Rust Foundations should make ordinary borrowing fluent without pretending that foundational lifetime syntax completes memory mastery.

### 8. Parallel, async, and network behavior

There are no threads, atomics, channels, futures, runtimes, sockets, or protocols. These are not omitted because they are marginal. They are omitted because their safety and cancellation behavior depend on the ownership foundation established here.

Course 7 covers concurrency and parallel algorithms. Course 8 covers async and networked systems.

### 9. Unsafe and FFI

The capstone forbids unsafe code. It therefore does not teach how safe abstractions are built over raw pointers, foreign functions, memory-mapped data, or OS handles. Course 6 introduces unsafe boundaries with explicit safety contracts and audit methods.

### 10. What has genuinely been mastered

Completing this course does not mean mastering all Rust. You have mastered the prerequisites that prevent advanced Rust from becoming cargo-cult syntax:

- expression and type reasoning;
- moves, borrowing, and owned/borrowed API choices;
- structs, enums, newtypes, and state modeling;
- collections and foundational iterators;
- recoverable error paths;
- foundational traits, generics, and lifetime reading;
- package/module/public API organization;
- tests and diagnostics as engineering evidence;
- one complete persistent safe-Rust application.

The next course can now deepen ownership, lifetimes, and memory without repairing a shallow syntax-only foundation.

## Architecture Decisions and Guarantee Matrix

The capstone should be defended by claims that are no broader than its code and tests.

### Guarantee matrix

| Concern | Implemented guarantee | Evidence | Explicitly not guaranteed |
|---|---|---|---|
| domain mutation | rejected add, rename, and transition operations leave the in-memory board unchanged | model and application failure tests | rollback across arbitrary external side effects |
| loading | no board is returned until every record and cross-record invariant succeeds | malformed fixture and duplicate-ID tests | repair of corrupt input |
| rendering | canonical deterministic order | storage and CLI snapshot tests | compatibility with unspecified external formats |
| saving | complete canonical bytes are written to a same-directory candidate before replacement is attempted | persistence tests and operation-specific errors | universal transactionality, directory fsync, multi-writer exclusion |
| public API | callers can perform supported workflows without field access | integration tests outside the library module | long-term semver stability beyond the current version |
| process behavior | command errors use stderr and nonzero status; ordinary output uses stdout | real-process tests | shell portability beyond documented invocation |

### Decision review questions

1. What owner is responsible for every `String` after command parsing and execution?
2. Which functions borrow because the caller must retain ownership?
3. Which invalid states are impossible to construct through the public API?
4. At which exact point can persistence fail after an in-memory change, and what process state remains?
5. Which save statements are language/library contracts, and which are product assumptions?
6. Which test would fail if `HashMap` iteration order accidentally became output order?
7. Which future feature would force a storage-version change rather than merely changing one field value?

The corresponding implementation-facing records are `capstone/ARCHITECTURE.md` and `capstone/LIMITATIONS.md`.

## Acceptance route

From the course root:

```bash
cargo test -p taskboard
cargo clippy --workspace --all-targets -- -D warnings
cargo fmt --all -- --check
```

The program should also pass the manual demonstration described in [`capstone/README.md`](../capstone/README.md).
