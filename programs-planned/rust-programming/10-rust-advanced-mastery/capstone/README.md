# AxiomStore

## Course role

AxiomStore is a versioned embedded record engine with lending views, const bounds, runtime validators, one private initialized-prefix abstraction, deterministic storage, migrations, compatibility fixtures, and a claim-specific verification matrix.

AxiomStore is not a showcase of ten independent features. It is the place where the course’s mechanisms must coexist without creating a second owner for state, validation, order, failure, compatibility, or resource policy.

## Invariants carried through the product

- Every advanced abstraction begins with a proof obligation rather than a feature preference.
- Generic and lending APIs state the exact type, lifetime, and equality relationships callers may rely on.
- Const parameters encode only invariants supported by stable Rust and by the product representation.
- Unsafe inline storage maintains one initialized-prefix invariant through movement, failure, and drop.
- Verification evidence is matched to claim class and never promoted beyond the paths or model it covers.
- Format versions, MSRV, features, provider capabilities, migration, and deprecation remain explicit compatibility contracts.

## Module-to-product map

| Module | Mechanism added | Acceptance criterion |
|---:|---|---|
| 91 | Reading Rust Through the Compiler: HIR, MIR, Borrow Checking, and Codegen | Separate parsing, name resolution, type checking, trait solving, borrow checking, monomorphization, optimization, and linking as distinct explanatory phases |
| 92 | Advanced Trait Solving: Goals, Projections, and Type Equality | Rewrite a complex generic error as a small set of trait goals, projection goals, and equality constraints |
| 93 | GATs, Higher-Ranked Bounds, and Lending Interfaces | Distinguish one associated type from a lifetime-indexed family of associated types |
| 94 | Const Generics, Witness Types, and Compile-Time Invariants | Use const parameters when a numeric fact changes representation, layout, or legal composition |
| 95 | Opaque and Erased Types: impl Trait, dyn Trait, Any, and Plugin Boundaries | Distinguish opaque return types from trait objects and explain why different branches of `impl Trait` must share one hidden concrete type |
| 96 | Auditing Unsafe Abstractions: Validity, Provenance, Drop, Panic, and Auto Traits | Write a safety dossier that names representation states, public preconditions, internal invariants, and proof obligations for every unsafe operation |
| 97 | From Source to Machine Code: Monomorphization, Dispatch, Layout, and Code Size | Explain when generic functions are monomorphized and why source-level abstraction does not determine final code duplication |
| 98 | Verification Beyond Examples: Compile-Fail, Property, Model, Fuzz, Miri, and Concurrency Exploration | Classify claims as type-level, functional, algebraic, state-machine, memory-safety, concurrency, compatibility, or performance claims |
| 99 | Long-Lived APIs: SemVer, MSRV, Features, Migrations, and Workspace Stewardship | Analyze a proposed change from the perspectives of downstream callers, downstream implementors, type inference, pattern matching, and stored data |
| 100 | Architectural Synthesis: Building and Defending a Long-Lived Rust System | Construct an invariant map connecting product claims to types, runtime validation, synchronization, unsafe proofs, tests, and operational policy |

## Reading route

1. Read the AxiomStore contract and non-goals in the [engineering guide](../course-book/capstone.md).
2. Locate the type or component that owns each invariant above.
3. Run the baseline tests and one end-to-end demonstration before changing code.
4. Implement only the current module increment and its adversarial test.
5. Trace success, rejection, partial failure, cleanup, order, and capacity through the public surface.
6. Re-run the complete course route, then explain which claims remain conditioned on a compiler, target, scheduler, peer, workload, or operating system.

AxiomStore is the cumulative capstone for Course 10, **Advanced Rust Mastery**. It is a deliberately bounded embedded record engine: large enough to expose advanced type, memory, compatibility, and verification obligations, but small enough that one reader can trace every byte and every ownership transition.

The reference implementation uses only the Rust standard library. That restriction is pedagogical, not a claim that production storage engines should avoid mature crates. It keeps the decisive mechanisms visible: a lending codec, const-generic local bounds, runtime policy erasure, private unsafe storage, versioned bytes, candidate-first mutation, and explicit filesystem assumptions.

## Product

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

The library provides:

- validated owned `Record` values with private fields;
- deterministic `AXIOM01` encoding;
- immutable snapshots that own verified archive bytes;
- GAT-based lending traversal over borrowed record views;
- const-generic maximum encoded-record size and transaction capacity;
- an ordered runtime registry of dyn-compatible validators;
- a private `InlineBatch<T, N>` over `MaybeUninit<T>`;
- in-memory candidate construction before persistent replacement;
- legacy `key=value` migration into a new destination;
- typed errors carrying byte offsets, line numbers, validator identity, and I/O operation context;
- golden fixtures, negative format tests, model-oriented transaction tests, process tests, and compile-fail API evidence.

AxiomStore is not a multi-process database, a crash-consistent journal, an authenticated format, an unbounded archive reader, or a portable atomic-replacement library. Those exclusions are part of the contract rather than hidden deficiencies.

## AXIOM01 format

All integers are big endian.

```text
8 bytes   magic: ASCII AXIOM01 followed by NUL
4 bytes   record count
records, strictly ordered by key:
  4 bytes key length
  key UTF-8 bytes
  4 bytes value length
  value UTF-8 bytes
4 bytes   FNV-1a checksum of every preceding byte
```

The eight-byte magic is therefore `b"AXIOM01\0"`, not the seven printable characters alone. The checksum detects accidental corruption. It does not authenticate the writer or protect against deliberate tampering.

The parser rejects:

- truncated headers, lengths, fields, and checksums;
- unsupported magic;
- checked-arithmetic overflow;
- a declared record larger than `MAX_RECORD` before slicing its complete payload;
- impossible record counts for the available byte length;
- invalid UTF-8;
- invalid key or value domain strings;
- duplicate or noncanonical key order;
- checksum mismatch;
- trailing or unaccounted bytes.

`fixtures/` contains immutable positive and negative format evidence. Ordinary tests consume those bytes; they do not call the current encoder to manufacture their own expected result.

## Type and variation boundaries

The private codec is statically selected because it owns an associated family of borrowed view types:

```rust
trait RecordCodec<const MAX_RECORD: usize> {
    type View<'a>
    where
        Self: 'a;

    type DecodeError;

    fn decode<'a>(
        bytes: &'a [u8],
        offset: usize,
    ) -> Result<(Self::View<'a>, usize), Self::DecodeError>;
}
```

A snapshot owns validated bytes. Its cursor lends `RecordView<'a>` values whose key and value slices cannot outlive the cursor loan or snapshot. Domain validation examines those borrowed slices directly, so verification does not construct temporary owned records. A caller that needs retention invokes the explicit owned conversion.

Validators use dynamic dispatch because policy is assembled at runtime and heterogeneous implementations coexist in one ordered registry. The erased contract consumes the stable owned `Record`, not a codec-specific borrowed view. Duplicate validator names are rejected because diagnostics and configuration need stable identity.

`MAX_RECORD` and `TX_CAP` are type parameters because they affect local representation and legal operations. The reference does **not** impose an archive-wide byte or record-count limit beyond address-space and file-reading constraints. Before processing hostile archives in a deployed service, add a file-size and record-count policy at the store boundary. This residual limit is intentional and documented rather than falsely described as implemented.

## Transaction semantics

A transaction only stages operations. It does not capture a snapshot when constructed. `commit(self)` performs:

1. open and verify the current archive;
2. decode it into an owned candidate map;
3. apply staged operations in source order;
4. validate every candidate record;
5. encode complete canonical bytes;
6. decode and verify those candidate bytes;
7. persist the candidate through the filesystem protocol;
8. return the already verified snapshot.

Capacity or validation failure during staging or candidate construction cannot alter the archive. `commit` consumes the transaction; a commit error does not return the staged transaction for retry. That ownership policy is explicit.

The implementation assumes one external writer. It does not lock across processes and does not detect a competing writer between snapshot read and replacement. Multiple writers can therefore lose updates. A deployment needing concurrent writers must add an external lock or a different storage protocol.

## Filesystem contract

Initial creation uses `create_new`, writes the complete archive, flushes, synchronizes the file, and synchronizes the parent directory on Unix. If the process crashes while writing the first file, an incomplete new path may remain; later verification rejects it. Initialization never replaces an existing destination.

Updates on Unix use a same-directory temporary file:

```text
encode and verify candidate
    -> create temporary file exclusively
    -> write all bytes
    -> flush
    -> synchronize temporary file
    -> rename over destination
    -> synchronize parent directory
```

A failure before rename leaves the previous archive unchanged. A parent-directory synchronization failure occurs **after** the new archive has been installed; it is reported as `StoreError::Durability`, whose message states that the visible commit may already have occurred. This distinction prevents callers from assuming that every returned error means rollback.

The reference implementation relies on Unix rename-overwrite semantics for update commits. On non-Unix targets, creation and read-only verification remain available, but update commits return `UnsupportedPlatform`. This is more honest than silently using remove-then-rename and calling it atomic.

Migration creates a new destination and refuses to replace an existing path. The V0 source is never modified.

## Unsafe boundary

`InlineBatch<T, N>` has one representation invariant:

```text
0 <= len <= N
slots[0..len] contain live T values owned by the batch
slots[len..N] are logically uninitialized
no safe reference reaches an uninitialized slot
every initialized value is dropped exactly once
```

The capstone needs only `push`, shared slice access, length queries, and `Drop`. Keeping the unsafe API smaller than the independent Inline Batch laboratory reduces the proof surface. Push writes a value before incrementing `len`. Slice construction covers exactly the initialized prefix. Destruction calls `assume_init_drop` once for each initialized slot. `N = 0` is a defined always-full state.

The type has no manual `Send`, `Sync`, or `Unpin` implementation. Auto traits follow its fields. Every unsafe block has a local `SAFETY:` explanation, but the authoritative proof is the whole invariant and transition review, not the comments alone.

## Verification route

From this directory:

```bash
cargo test --all-targets
cargo test --doc
cargo clippy --all-targets -- -D warnings
cargo fmt --all -- --check
```

When Miri is installed:

```bash
cargo miri test inline_batch
```

The evidence set includes:

- compile-fail documentation for view escape;
- checked-in canonical and malformed binary fixtures;
- writer-versus-fixture comparison;
- checksum corruption tests;
- dynamic-validator failure-state tests;
- bounded transaction sequences compared with an independent `BTreeMap` model;
- migration tests that preserve source and existing destination data;
- real CLI status, stdout, and stderr tests;
- destructor-count tests for the unsafe batch;
- manual safety, compatibility, and filesystem-contract review.

No single green command establishes complete soundness or compatibility. Each form of evidence has a stated scope.

## Final independent extension

The course’s final assessment adds `AXIOM02` schema tags while preserving `AXIOM01` reads. The reference deliberately does not implement that extension. The reader must define the reader/writer matrix, eight-byte magic (`AXIOM02` plus NUL), migration behavior, unknown-tag policy, fixtures, CLI reporting, and rollback story before changing code.
