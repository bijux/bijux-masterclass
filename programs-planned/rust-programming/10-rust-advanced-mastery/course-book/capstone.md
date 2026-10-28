# AxiomStore Engineering Guide

## A versioned embedded record engine

AxiomStore is the final cumulative capstone of the ten-course program. It is intentionally smaller than a database and deeper than a demonstration. The product stores key/value records in a deterministic versioned archive, exposes borrowed read views, applies runtime validation policy, stages bounded transactions, migrates legacy data, and provides a CLI. Its architecture exists to make advanced Rust proof obligations visible.

The capstone is standard-library-only. This keeps the decisive type, memory, format, and compatibility mechanisms in view. Production systems may select mature crates for serialization, storage, error handling, property generation, fuzzing, or plugins after understanding the contracts those crates own.

## Product interface

```text
axiomstore init <archive.ax>
axiomstore put <archive.ax> <key> <value>
axiomstore list <archive.ax>
axiomstore verify <archive.ax>
axiomstore migrate-v0 <legacy.txt> <archive.ax>
axiomstore schema
axiomstore version
axiomstore help
```

The library exposes stable owned records, archive verification, snapshots, transactions, and validation registration. It keeps version-specific codecs, raw parser cursors, inline storage, and migration staging private.

## Stable domain model

```rust
#[derive(Clone, Debug, PartialEq, Eq, PartialOrd, Ord)]
pub struct Record {
    key: String,
    value: String,
}
```

Construction validates:

- nonempty keys;
- no tab, carriage return, line feed, or NUL in keys or values;
- bounded UTF-8 byte lengths;
- canonical key ordering in encoded archives;
- unique keys after a transaction commits.

Fields remain private. Public observers return `&str`. This prevents callers from bypassing validation after construction.

## AXIOM01 format

All integers use big-endian encoding.

```text
8 bytes   magic = ASCII AXIOM01 followed by NUL
4 bytes   record count
repeated record count times:
  4 bytes key length
  key bytes
  4 bytes value length
  value bytes
4 bytes   FNV-1a checksum of all preceding bytes
```

The decoder rejects:

- wrong magic;
- unsupported version;
- truncated fields;
- lengths above configured bounds;
- checked-addition overflow;
- invalid UTF-8;
- invalid domain strings;
- duplicate or noncanonical keys;
- checksum mismatch;
- trailing bytes.

The writer produces one canonical representation. Canonical ordering makes known vectors and migration comparisons stable; the checksum detects accidental corruption but is not an authentication mechanism.

## Static codec with a borrowed associated family

AxiomStore’s private codec contract is:

```rust
pub(crate) trait RecordCodec<const MAX_RECORD: usize> {
    type View<'a>
    where
        Self: 'a;

    type DecodeError;

    fn decode<'a>(
        bytes: &'a [u8],
        offset: usize,
    ) -> Result<(Self::View<'a>, usize), Self::DecodeError>;

    fn encode(record: &Record, out: &mut Vec<u8>)
        -> Result<(), StoreError>;
}
```

The GAT keeps borrowed slices local to immutable archive bytes. The stable public `Record` is owned. This split avoids copying during verification and listing while preventing archive-buffer lifetimes from spreading through transactions, validator registries, CLI code, and migrations.

The codec remains static. It owns representation relationships and a lifetime-indexed view family that is not a natural runtime-erased plugin boundary.

## Snapshot and lending traversal

Opening an archive yields an owned `Snapshot` containing validated bytes and the verified record count. The cursor derives each next offset while lending a view; offset internals remain private. The snapshot exposes:

```rust
pub trait LendingRecords {
    type View<'a>
    where
        Self: 'a;

    fn next<'a>(
        &'a mut self,
    ) -> Option<Result<Self::View<'a>, StoreError>>;
}
```

A borrowed `RecordView<'a>` contains `&'a str` key and value slices. The next exclusive cursor borrow cannot occur while the previous view is retained. Callers that need durable ownership call `RecordView::to_owned`.

This protocol is deliberate. An ordinary `Iterator<Item = Record>` would allocate or clone. An iterator over precomputed `&Record` values would require owned parsed records in the snapshot. A callback could prevent escape but would be less composable for the course’s query examples. The lending cursor makes the storage reuse contract explicit.

## Const bounds and runtime limits

The primary library type is parameterized by two local representation limits:

```rust
pub struct Store<
    const MAX_RECORD: usize = 4096,
    const TX_CAP: usize = 32,
> { /* private */ }
```

`MAX_RECORD` bounds one encoded record and participates in codec checks. `TX_CAP` determines the inline transaction batch representation. The reference intentionally does not impose an archive-wide byte or record-count limit. It reads one archive into memory before validation. A deployment that accepts hostile files must add file-size and record-count admission at the store boundary. That residual limit remains runtime policy rather than a const-generic type identity.

The design distinguishes:

- compile-time maximum capacity;
- runtime current length;
- initialized slot count;
- archive-level limits;
- domain-level validity.

No one number is allowed to stand in for all five.

## Runtime validator registry

Validation policy is open at runtime:

```rust
pub trait Validator {
    fn name(&self) -> &'static str;
    fn validate(&self, record: &Record) -> Result<(), ValidationIssue>;
}
```

The store owns `Vec<Box<dyn Validator>>`. Validators run in registration order. Duplicate validator names are rejected because diagnostics and configuration need stable identity. Validation receives an owned stable `Record`, not a codec-specific borrowed view. This keeps the object contract dyn compatible and prevents representation lifetimes from entering the plugin boundary.

Built-in validators include maximum logical value length and reserved key-prefix rejection. The CLI uses a deterministic default registry. The public library permits explicit registration before transactions begin.

## Bounded transaction and unsafe inline storage

A transaction stages up to `TX_CAP` operations in `InlineBatch<Operation, TX_CAP>`. The type uses `[MaybeUninit<T>; N]` and a runtime `len` representing an initialized prefix.

The complete invariant is:

```text
0 <= len <= N
slots[0..len] contain live T values owned by the batch
slots[len..N] are logically uninitialized
no reference to an uninitialized slot is created
each initialized value is moved or dropped exactly once
the backing array moves only as raw storage; no internal self-reference exists
```

The capstone uses a deliberately smaller API than the independent Inline Batch laboratory. Push writes the value before incrementing `len`; shared slice construction covers only `0..len`; `Drop` calls `assume_init_drop` over exactly that prefix. `N = 0` is valid and always reports full. The type contains no manual `Send`, `Sync`, or `Unpin` implementation; auto traits follow `T` and the fields.

The independent laboratory compares the representation with a safe `Vec<T>` oracle and exercises pop, clear, mutation, and panic-oriented transitions. The capstone retains destructor-count tests for the operations it exposes. Miri is an optional additional route when available. The safety dossier remains authoritative even when every dynamic tool passes.

## Transaction semantics

A transaction stages operations without touching persistent state:

```text
Put(Record)
Remove(key)
Clear
```

It does not capture a snapshot when constructed. `commit(self)` consumes the transaction and follows this sequence:

1. open and verify the current archive;
2. copy its current logical map into an owned candidate;
3. apply staged operations to the candidate in source order;
4. validate every resulting record through the registry;
5. encode a complete AXIOM01 candidate;
6. decode and verify that candidate;
7. write the candidate to a same-directory temporary file;
8. flush and synchronize the temporary file;
9. on Unix, rename over the destination and synchronize the parent directory;
10. return the already verified snapshot.

Capacity, decode, validation, encoding, temporary-write, and pre-rename failures leave the previous archive unchanged. The transaction is consumed even when commit fails; the error does not return staged operations for retry. A parent-directory synchronization failure occurs after replacement and is reported separately because the new archive may already be visible.

The reference is single-writer. It has no inter-process lock and cannot prevent lost updates between concurrent writers. Update replacement depends on Unix rename-overwrite semantics. Non-Unix targets can create and verify archives, but update commits return an explicit unsupported-platform error rather than silently using a non-atomic remove-then-rename sequence.

## Filesystem and writer boundary

Initial creation uses exclusive `create_new` semantics, complete write, flush, file synchronization, and parent-directory synchronization on Unix. A process crash during the first write can leave an incomplete new file; later verification rejects it. Initialization never overwrites an existing destination.

Update commits use same-directory temporary files and Unix rename-overwrite semantics. The previous archive is preserved until rename. A failure after rename but during directory synchronization is not rollback: the error reports that installation may already have occurred. The standard-library reference deliberately refuses update commits on non-Unix targets because it cannot promise equivalent replacement semantics there without a platform-specific implementation.

AxiomStore assumes one external writer. It does not lock the path, compare generations, or detect another process committing between snapshot read and rename. Add an external lock or a different storage protocol before using the reference as a multi-writer engine.

## Legacy migration

The legacy V0 format is:

```text
key=value
```

Blank lines and lines beginning with `#` are ignored. Each other physical line must contain a first `=` delimiter; the remainder belongs to the value. Migration preserves physical line numbers in diagnostics, validates records, rejects duplicates, constructs a complete AXIOM01 candidate, verifies it, and then creates a new destination exclusively.

The V0 source is never modified, and migration refuses to replace an existing destination. These two rules preserve an unambiguous recovery path after parsing, validation, encoding, or output failure.

## Error taxonomy

Public errors distinguish:

- CLI usage;
- invalid key or value;
- transaction capacity;
- validation rejection with validator identity;
- malformed archive with byte offset;
- unsupported format;
- checksum mismatch;
- duplicate key;
- legacy migration with physical line;
- destination-already-exists;
- unsupported replacement platform;
- I/O operation and path;
- post-install durability uncertainty.

User, stored-data, compatibility, and operating-system failures are ordinary `Result` values. An unsafe invariant violation would be a software defect; the safe public API does not invent a recoverable domain error for undefined internal state.

## Verification matrix

| Claim | Primary evidence | Complementary evidence |
|---|---|---|
| views cannot outlive snapshots | compile-fail documentation | public API review |
| incompatible capacities do not compose accidentally | type checks and constructor tests | compatibility review |
| encode/decode preserves records | known vectors and properties | malformed corpus |
| transaction matches specification | safe BTreeMap model sequences | integration tests |
| initialized values drop exactly once | drop-counting operation sequences | Miri when available |
| old data remains readable | checked-in AXIOM01 and V0 golden fixtures | migration and process tests |
| CLI exit and output contracts hold | process tests | manual demonstration |
| dispatch choices preserve semantics | parity oracle | artifact observation |
| code-size conclusions are scoped | pinned source-to-artifact record | repeat on release changes |
| public evolution is supported | downstream fixture and MSRV/feature matrix | release review |

The matrix names partial evidence rather than collapsing everything into one “verified” label.

## Module increments

### Module 91 — Reading Rust Through the Compiler: HIR, MIR, Borrow Checking, and Codegen

Begin with a source-to-evidence notebook for four AxiomStore questions: codec method resolution, the lifetime of a lent `RecordView`, destruction of a partially staged transaction, and the code shape of static versus dynamic validation. The increment produces diagrams and causal specimens before it changes architecture. Later modules reuse those records rather than rediscovering the compiler model from error messages.

**Required evidence:** update the compiler evidence ledger, preserve every earlier known vector and public test, and add one negative case whose causal result depends on the new boundary.
### Module 92 — Advanced Trait Solving: Goals, Projections, and Type Equality

Introduce the private codec family and write its trait-goal graph. The codec owns the relationship among an archive version, a borrowed view, and a decode error; the store owns translation into `StoreError`. Keep runtime validators on the stable owned `Record` boundary. The finished signatures should contain only bounds required by an operation, with projection equalities documented where composition depends on them.

**Required evidence:** update the trait-goal graph, preserve every earlier known vector and public test, and add one negative case whose causal result depends on the new boundary.
### Module 93 — GATs, Higher-Ranked Bounds, and Lending Interfaces

Implement the snapshot cursor as a lending interface. Each call chooses a fresh view lifetime tied to that borrow of the cursor, while the underlying bytes remain owned by the snapshot. Domain checks inspect the borrowed fields in place. Add `to_owned` only at the retention boundary, then prove through a negative example that a view cannot outlive its snapshot or survive a conflicting cursor advance.

**Required evidence:** update the lifetime quantifier map, preserve every earlier known vector and public test, and add one negative case whose causal result depends on the new boundary.
### Module 94 — Const Generics, Witness Types, and Compile-Time Invariants

Parameterize the store by maximum encoded-record size and inline transaction capacity. Enforce both at construction or staging boundaries, and add zero-capacity and exact-boundary tests. Keep archive version, record count, policy choices, and deployment limits as runtime data. Record why moving any of those values into a const parameter would create incompatible type identities without improving the proof.

**Required evidence:** update the compile-time/runtime invariant table, preserve every earlier known vector and public test, and add one negative case whose causal result depends on the new boundary.
### Module 95 — Opaque and Erased Types: impl Trait, dyn Trait, Any, and Plugin Boundaries

Add the validator registry as the deliberately open boundary: ordered `Box<dyn Validator>` entries consume stable owned records and reject duplicate names. Keep archive codecs statically selected because their GAT family participates in representation. Use an enum for the reader-owned set of built-in versions and opaque iterators for query implementation details. The increment ends with a variation map explaining each choice.

**Required evidence:** update the variation and erasure map, preserve every earlier known vector and public test, and add one negative case whose causal result depends on the new boundary.
### Module 96 — Auditing Unsafe Abstractions: Validity, Provenance, Drop, Panic, and Auto Traits

Replace the safe staging vector with the private `InlineBatch<T, N>` only after freezing transaction behavior against a `Vec` oracle. The implementation owns one initialized-prefix invariant and exposes no raw storage. Exercise full, empty, zero-capacity, movement, and destructor paths; then write the safety dossier from safe constructors through `Drop`. Revert to `Vec` if the inline-storage requirement cannot justify that burden.

**Required evidence:** update the unsafe abstraction safety dossier, preserve every earlier known vector and public test, and add one negative case whose causal result depends on the new boundary.
### Module 97 — From Source to Machine Code: Monomorphization, Dispatch, Layout, and Code Size

Create a dispatch observatory around three existing boundaries: monomorphized codec calls, enum-based version dispatch, and trait-object validators. First prove semantic parity. Then inspect symbols, size, and assembly for one pinned profile and target. The deliverable is not “static is faster”; it is an artifact record that separates observed duplication and indirect calls from the architecture’s stable behavior.

**Required evidence:** update the source-to-artifact observation record, preserve every earlier known vector and public test, and add one negative case whose causal result depends on the new boundary.
### Module 98 — Verification Beyond Examples: Compile-Fail, Property, Model, Fuzz, Miri, and Concurrency Exploration

Build the claim matrix from AxiomStore’s actual promises. Protect binary compatibility with immutable vectors, lifetime misuse with compile-fail cases, transaction semantics with an independent `BTreeMap` model, malformed input with a bounded corpus and fuzz target, unsafe state with destructor tests and optional Miri, and CLI behavior with process tests. Every row must state the residual claim left unproved.

**Required evidence:** update the claim-to-evidence verification matrix, preserve every earlier known vector and public test, and add one negative case whose causal result depends on the new boundary.
### Module 99 — Long-Lived APIs: SemVer, MSRV, Features, Migrations, and Workspace Stewardship

Publish the compatibility contract before adding another format: immutable `AXIOM01` fixtures, deterministic legacy migration, unknown-version rejection, no-default feature policy, and a declared MSRV. Add downstream fixture crates that exercise the public surface. Draft the `AXIOM02` reader/writer matrix now, but leave its implementation for the independent final change.

**Required evidence:** update the compatibility and migration matrix, preserve every earlier known vector and public test, and add one negative case whose causal result depends on the new boundary.
### Module 100 — Architectural Synthesis: Building and Defending a Long-Lived Rust System

Finish AxiomStore by reconciling all ten ledgers: ownership, compiler phase, trait goals, lifetime quantifiers, const/runtime invariants, variation, unsafe safety, artifact observations, verification, and compatibility. Remove any mechanism that lacks a unique requirement. Then implement `AXIOM02` schema tags as an unseen change; success means the new version extends the existing authorities instead of creating parallel models or write paths.

**Required evidence:** update the architecture defense dossier, preserve every earlier known vector and public test, and add one negative case whose causal result depends on the new boundary.

## Final independent extension: AXIOM02

The final assessment adds schema tags:

```text
8 bytes   magic = ASCII AXIOM02 followed by NUL
2 bytes   schema tag length
schema tag bytes
4 bytes   record count
records...
checksum
```

Requirements:

- existing AXIOM01 files remain readable;
- the default writer becomes AXIOM02 only after tests and documentation change together;
- schema tags use the same domain-validation discipline as keys;
- unknown tags have an explicit policy;
- version dispatch remains private;
- the stable public record model changes only if schema semantics require it;
- migrations preserve source data until the candidate is verified;
- all AXIOM01 golden fixtures remain in the repository;
- the compatibility matrix records read/write support;
- unsafe storage invariants remain unchanged unless justified;
- the CLI exposes the detected version and schema without leaking parser internals.

No reference implementation of AXIOM02 is supplied. The extension tests whether the first nine increments produced an architecture that can absorb change.

## Architecture defense

The final defense uses eight artifacts:

1. product and threat boundary;
2. invariant ownership map;
3. trait-goal and lifetime-quantifier records;
4. variation and erasure map;
5. unsafe safety dossier;
6. verification matrix;
7. compatibility and migration matrix;
8. source-to-artifact observation record.

The defense must also reject at least five plausible mechanisms. Examples include async storage, public codec plugins, a proc-macro schema language, lock-free transaction state, self-referential record objects, global `Arc` ownership, or platform-specific memory mapping. A rejection is strong when it acknowledges the mechanism’s benefit and explains why its proof, compatibility, or operating cost is not justified for AxiomStore’s current requirements.
