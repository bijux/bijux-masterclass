# Taskboard

This directory contains the executable capstone for Course 1. The reader-facing design and ten-step learning route are in the [capstone chapter](../course-book/capstone.md).

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

