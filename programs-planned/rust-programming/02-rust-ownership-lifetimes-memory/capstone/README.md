# Memory Workspace

This directory contains the executable capstone for Course 2. The reader-facing design and ten-step learning route are in the [capstone chapter](../course-book/capstone.md).

`memory-workspace` is the complete capstone for **Rust Ownership, Lifetimes, and Memory**. It is a single-threaded in-memory document workspace designed to make ownership topology observable.

## Mechanisms demonstrated

- generational handles and stale-identity rejection;
- borrowed document and search views;
- owned staged edits with optimistic revision checks;
- commit failure that returns the owned session;
- immutable `Rc` snapshots and non-owning `Weak` watchers;
- revisioned `RefCell` caches behind an immutable query API;
- `Cow` plus a higher-ranked scoped callback;
- semantic payload accounting separated from layout observations;
- an explicit design decision not to use pinning.

The implementation is safe Rust and has no third-party dependencies.

## Run

From the course root:

```bash
cargo run -p memory-workspace -- demo
cargo run -p memory-workspace -- script capstone/scripts/demo.memory-workspace
cargo run -p memory-workspace -- help
cargo test -p memory-workspace --all-targets
cargo test -p memory-workspace --doc
cargo clippy -p memory-workspace --all-targets -- -D warnings
```

Or from this directory:

```bash
make confirm
```

## Script grammar

Fields are separated by literal tab characters. Empty lines and `#` comments are ignored.

```text
ADD<TAB>document-alias<TAB>title<TAB>text
SHOW<TAB>document-alias
EDIT<TAB>document-alias<TAB>expected-revision<TAB>replacement-text
RENAME<TAB>document-alias<TAB>expected-revision<TAB>title
TAG<TAB>document-alias<TAB>expected-revision<TAB>tag
SEARCH<TAB>query
SNAPSHOT<TAB>snapshot-alias<TAB>document-alias
WATCH<TAB>watcher-alias<TAB>snapshot-alias
DROP-SNAPSHOT<TAB>snapshot-alias
EVICT<TAB>document-alias<TAB>revision
CHECK-WATCH<TAB>watcher-alias
REMOVE<TAB>document-alias
MEMORY
LIST
```

The built-in demo proves that a weak watcher remains alive while any strong snapshot owner exists and expires after cache eviction plus removal of the final explicit alias.

## Architecture

```text
src/
├── handle.rs     logical identity and parsing
├── cache.rs      pure line-range derivation
├── model.rs      live document, borrowed views, removed ownership
├── edit.rs       owned staged edit state
├── snapshot.rs   immutable shared snapshots and weak watchers
├── workspace.rs  validation and state-transition protocol
├── memory.rs     bounded memory accounting and observations
├── script.rs     typed tab-separated execution language
├── lib.rs        restrained public API
└── main.rs       process shell and exit status
```

The detailed engineering book begins at `../course-book/capstone/index.md`.

## Non-goals

This capstone is not a persistent editor, concurrent service, Unicode-normalized search engine, exact heap profiler, self-referential data structure, or unsafe pinning implementation. Those boundaries are deliberate and tested in the course defense.

## Verification

```bash
cargo test
cargo fmt -- --check
cargo clippy --all-targets -- -D warnings
```
