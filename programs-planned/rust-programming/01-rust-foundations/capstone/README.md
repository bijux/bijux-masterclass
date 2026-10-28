# Taskboard

## Course role

Taskboard is a local persistent command-line work queue. Its small domain forces types, ownership, parsing, state transitions, storage, errors, modules, tests, and process behavior to work together without hiding the language behind a framework.

Taskboard is not a showcase of ten independent features. It is the place where the course’s mechanisms must coexist without creating a second owner for state, validation, order, failure, compatibility, or resource policy.

## Invariants carried through the product

- Task status and priority are closed typed domains, not arbitrary strings.
- Command parsing constructs typed commands before domain mutation begins.
- Every failed transition leaves the board and persistent file unchanged.
- Task identifiers remain unique and deterministic across load, mutation, and save.
- The library owns behavior; the binary owns environment, output, and exit status.
- Public output, storage order, tests, and documentation describe the same contract.

## Module-to-product map

| Module | Mechanism added | Acceptance criterion |
|---:|---|---|
| 1 | Compilation, Expressions, and Types | Distinguish package, crate, target, module, compiler, Cargo, profile, and artifact without collapsing them into “the project” |
| 2 | Control Flow, Functions, and Invariants | Treat if and loop constructs as typed expressions and prove branch agreement and loop result behavior |
| 3 | Ownership, Moves, Copying, and Destruction | Trace ownership through bindings, calls, returns, aggregates, and scopes using a move-path ledger |
| 4 | Borrowing, References, Slices, and Strings | Model shared and mutable references as permissions constrained by aliasing and validity |
| 5 | Structs, Enums, Methods, and Pattern Matching | Choose structs, tuple structs, newtypes, enums, and associated data from domain shape rather than language familiarity |
| 6 | Collections, Iterators, and Closures | Use Vec, slices, and HashMap with explicit length, capacity, invalidation, lookup, and ordering assumptions |
| 7 | Errors, Parsing, Files, and Persistence | Distinguish absence, recoverable failure, invariant violation, process failure, and ordinary values |
| 8 | Generics, Traits, Conversions, and Lifetime Basics | Write generic functions and types whose bounds correspond to operations actually performed |
| 9 | Crates, Modules, Public APIs, Tests, and Documentation | Distinguish package, crate, target, and module while organizing code by responsibility rather than one file per type |
| 10 | Integration and Independent Change | Trace a behavioral change through grammar, types, domain rules, persistence, rendering, tests, and documentation |

## Reading route

1. Read the Taskboard contract and non-goals in the [engineering guide](../course-book/capstone.md).
2. Locate the type or component that owns each invariant above.
3. Run the baseline tests and one end-to-end demonstration before changing code.
4. Implement only the current module increment and its adversarial test.
5. Trace success, rejection, partial failure, cleanup, order, and capacity through the public surface.
6. Re-run the complete course route, then explain which claims remain conditioned on a compiler, target, scheduler, peer, workload, or operating system.

`taskboard` is the cumulative product for Rust Foundations. It is a local, persistent command-line work queue implemented with safe Rust and the standard library only.

The application is intentionally small enough to understand completely and large enough to expose the interactions that determine whether a Rust design is sound: ownership of domain data, borrowed read paths, mutable transition paths, typed parsing, recoverable errors, generic stream I/O, module privacy, deterministic serialization, process exit behavior, and tests at several boundaries.

## Commands

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

The storage path is read from `TASKBOARD_FILE`. When the variable is absent, the binary uses `.taskboard.db` in the current directory.

```bash
export TASKBOARD_FILE=/tmp/my-board.db
cargo run -- add high "Repair record parser"
cargo run -- add normal "Write storage tests"
cargo run -- start 1
cargo run -- rename 2 "Write persistence and CLI tests"
cargo run -- list
cargo run -- stats
```

## Persistence contract

The versioned, tab-delimited protocol is deliberately implemented without a serialization dependency:

```text
TASKBOARD-V1
NEXT_ID\t3
TASK\t1\tdoing\thigh\tRepair record parser
TASK\t2\ttodo\tnormal\tWrite storage tests
```

Task titles may contain ordinary Unicode text but cannot contain tabs or line breaks. IDs are nonzero and monotonically allocated. Deleted IDs are never reused. The loader rejects malformed records, duplicate IDs, contradictory next-ID metadata, and unsupported headers. Save output is sorted by ID and is therefore deterministic.

`save_path` writes a same-directory temporary file, flushes and synchronizes it, and then commits it with `std::fs::rename`. Rename replacement semantics differ by operating system; the course book documents that portability boundary rather than claiming a universal transactional guarantee.

## Architecture

- `model.rs` owns domain invariants and legal task transitions.
- `command.rs` converts raw command-line tokens into typed commands.
- `storage.rs` owns the versioned persistence protocol and path I/O.
- `app.rs` executes typed commands and coordinates load/commit behavior.
- `main.rs` owns environment access, standard streams, and process exit codes.

The binary does not contain task rules or record parsing. Public consumers cannot construct invalid tasks by writing private fields.

## Failure policy

- command grammar failures exit with status `2`;
- domain and storage failures exit with status `1`;
- successful commands exit with status `0`;
- help and version do not read or create the storage file;
- read-only commands do not rewrite storage;
- failed transitions do not commit a modified board;
- user-visible success output is produced only after a required save succeeds.

## Verification

From this directory:

```bash
make confirm
```

From the course root:

```bash
make capstone-confirm
```

The proof route includes formatting, type checking, Clippy with warnings denied, unit tests, public API tests, real process tests, documentation tests, rustdoc generation, and a release build.
