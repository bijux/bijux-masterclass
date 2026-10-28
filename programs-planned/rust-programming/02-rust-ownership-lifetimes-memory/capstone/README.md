# Memory Workspace

## Course role

Memory Workspace is a single-threaded document workspace with generational handles, borrowed views, staged edits, snapshots, weak observers, caches, and explicit memory accounting. Every feature exists to make an ownership or lifetime relationship observable.

Memory Workspace is not a showcase of ten independent features. It is the place where the course’s mechanisms must coexist without creating a second owner for state, validation, order, failure, compatibility, or resource policy.

## Invariants carried through the product

- A document handle is valid only when both slot and generation match.
- Borrowed views never outlive the workspace or snapshot that owns their bytes.
- An edit commits only against the revision it was prepared from.
- Strong snapshots own liveness; weak observers never keep data alive.
- Cache validity is tied to revision and runtime borrows never escape their operation.
- Memory reports name their inclusions and exclusions instead of claiming exact heap truth.

## Module-to-product map

| Module | Mechanism added | Acceptance criterion |
|---:|---|---|
| 11 | Places, Move Paths, and Advanced Borrowing | Distinguish values from places and trace projections, move paths, partial initialization, and later destruction obligations |
| 12 | Lifetime Relationships and Borrowed APIs | Translate lifetime syntax into constraints among borrows rather than durations attached to values |
| 13 | Scoped Access and Escape Prevention | Distinguish caller-chosen named lifetimes from fresh lifetimes generated independently for each callback invocation |
| 14 | RAII, Drop, Unwinding, and Failure Atomicity | Derive local, field, tuple, temporary, and scope destruction order from documented rules |
| 15 | Box, Deref, Dynamically Sized Types, and Cow | Use Box for exclusive heap-owned indirection and recursive finite-size representation without equating Box with shared ownership |
| 16 | Rc, Weak, and Ownership Graphs | Draw strong and weak ownership graphs and derive allocation liveness from roots and reference counts |
| 17 | Interior Mutability and Runtime Borrows | Explain UnsafeCell as the primitive behind interior mutability while remaining within safe APIs |
| 18 | Memory Representation, Validity, and Layout | Separate semantic value, validity invariant, abstract layout guarantee, ABI promise, and measured observation |
| 19 | Subtyping, Variance, PhantomData, and Drop Checking | State lifetime subtype direction through substitutability and derive covariance, contravariance, and invariance operationally |
| 20 | Pinning and Address-Sensitive Design | Distinguish ownership movement from mechanical relocation and identify genuine address-sensitive invariants |

## Reading route

1. Read the Memory Workspace contract and non-goals in the [engineering guide](../course-book/capstone.md).
2. Locate the type or component that owns each invariant above.
3. Run the baseline tests and one end-to-end demonstration before changing code.
4. Implement only the current module increment and its adversarial test.
5. Trace success, rejection, partial failure, cleanup, order, and capacity through the public surface.
6. Re-run the complete course route, then explain which claims remain conditioned on a compiler, target, scheduler, peer, workload, or operating system.

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
