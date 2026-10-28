# FrameVault Engineering Guide

FrameVault is the cumulative system for Course 6. It is deliberately small enough to audit and broad enough to force all ten module boundaries to interact. The program stores files or structured process captures in a versioned binary archive, replaces archive files transactionally, extracts validated logical paths, owns one manually allocated aligned buffer, and exposes a C ABI with both stateless and opaque-session operations.

The product is not an exercise in feature count. Every component exists because it carries a distinct contract:

```text
host files and processes
        ↓ operating-system contracts
owned Rust domain values
        ↓ encoding contract
FRMVLT01 bytes
        ↓ checked decoding
validated Rust domain values
        ↓ safe wrapper / unsafe kernel
aligned owned storage
        ↓ C ABI contract
foreign callers and callbacks
```

The capstone succeeds only when each arrow is explicit. “Rust is safe,” “rename is atomic,” “the path is sanitized,” or “the pointer was checked” are not acceptable explanations. You must state which facts were checked, which remain assumptions, and which properties are deliberately not claimed.

## How this capstone completes the course

FrameVault is a versioned binary archive with checked parsing, transactional replacement, extraction policy, process capture, one manual allocation owner, and a C ABI with opaque sessions and callback rules.

The ten increments form one product history. An increment is accepted only when the new behavior fits the existing ownership and authority map, has a causal failure model, and preserves every earlier invariant not explicitly revised. The independent lab proves the mechanism in isolation; FrameVault proves that it can coexist with nine other mechanisms.

### Product invariants

| # | Invariant that must survive every increment |
|---:|---|
| 1 | No hostile length, offset, count, or path component is trusted before bounded validation. |
| 2 | File replacement distinguishes pre-commit failure, visible commit, and durability evidence. |
| 3 | Native paths and portable archive names remain separate types and threat models. |
| 4 | Every unsafe operation is justified by a local invariant reachable from the safe facade. |
| 5 | Manual allocation records the exact layout used for allocation and deallocation. |
| 6 | C declarations, Rust ABI declarations, nullability, panic policy, and ownership agree. |

For each FrameVault change, annotate the owning component, state before and after success, state after every rejected or partial path, cleanup, order, capacity, and public compatibility. Where the course concerns compiler, platform, scheduler, workload, or peer behavior, label that condition rather than promoting it into an unconditional guarantee.

### Ten-module integration map

| Module | Mechanism | Capability visible in the product | Independent laboratory |
|---:|---|---|---|
| 51 | Binary Data Contracts: Bytes, Endianness, and Checked Parsing | Define a binary format as a versioned contract rather than a sequence of convenient writes | [Checked Frame Codec](../labs/module-01-checked-frame-codec/README.md) |
| 52 | Files, Durability, and Transactional Replacement | Distinguish read, write, flush, data synchronization, metadata synchronization, and directory-entry durability | [Atomic Archive Store](../labs/module-02-atomic-archive-store/README.md) |
| 53 | Paths, Names, and Platform Boundaries | Distinguish portable logical names, `Path`, `PathBuf`, `OsStr`, and display text | [Sandboxed Extraction Paths](../labs/module-03-sandboxed-extraction-paths/README.md) |
| 54 | Processes, Environments, and Standard Streams | Construct commands from a program plus arguments, not an interpolated shell line | [Bounded Process Capture](../labs/module-04-bounded-process-capture/README.md) |
| 55 | Unsafe Rust as a Proof Boundary | Name the operations Rust requires an unsafe context to perform | [Unsafe Slice Kernel](../labs/module-05-unsafe-slice-kernel/README.md) |
| 56 | Raw Pointers, Provenance, and Uninitialized Memory | Distinguish raw pointers from references and explain why conversion does not transfer ownership | [Panic-Safe Batch Builder](../labs/module-06-panic-safe-batch-builder/README.md) |
| 57 | Manual Allocation and Owning Unsafe Abstractions | Construct and validate `Layout` values without unchecked size arithmetic | [Aligned Byte Buffer](../labs/module-07-aligned-byte-buffer/README.md) |
| 58 | C FFI: ABI, Strings, Pointers, and Error Boundaries | Distinguish ABI compatibility from semantic validity and ownership | [C ABI Line Validator](../labs/module-08-c-abi-archive-validator/README.md) |
| 59 | Foreign Resources, Callbacks, and Wrapper Architecture | Separate raw bindings, checked unsafe shims, and safe domain wrappers | [Opaque Foreign Session](../labs/module-09-opaque-foreign-session/README.md) |
| 60 | Integrated Systems Design, Testing, and Audit | Draw one boundary map from external bytes to final effects and back to foreign callers | [Systems Boundary Audit](../labs/module-10-systems-boundary-audit/README.md) |

### How to read the implementation

Begin with the product promise and private invariant-bearing types. Next locate validation and conversion boundaries, state transitions, effectful operations, cleanup, deterministic rendering or wire behavior, and finally the tests. This order prevents `main.rs` call order from being mistaken for architecture.

Use a **whole-system boundary dossier** to connect the implementation to the course. Every row should point to code, a test or review, and a documented limit on the claim. Missing evidence is not repaired by a stronger adjective.

### Acceptance traces

Preserve at least these six traces while completing the capstone:

1. FrameVault ordinary success from external input to visible output;
2. malformed or unsupported input rejected before trusted state changes;
3. domain or capacity rejection with the original authoritative state preserved;
4. partial work followed by failure, including cleanup and retry state;
5. the largest accepted and smallest rejected order, size, lifetime, or capacity boundary;
6. one compatibility, platform, scheduler, peer, compiler, or workload edge specific to this course.

A passing test suite is necessary, but the final defense also names a simpler architecture and explains why this product’s requirements justify the additional mechanism. If the simpler design would satisfy the real contract, prefer it.

## Product boundary

FrameVault supports these commands:

```text
framevault create <archive.fv> <source>...
framevault create <archive.fv> --entry <logical-name> <source> [--entry ...]
framevault list <archive.fv>
framevault verify <archive.fv>
framevault extract <archive.fv> <directory>
framevault capture <archive.fv> -- <program> [argument...]
framevault help
framevault version
```

It also builds as a library and `cdylib`. The C surface consists of:

```c
const char *framevault_version(void);
int32_t framevault_validate(
    const uint8_t *bytes,
    size_t length,
    FvReport *report
);
int32_t framevault_open(
    const uint8_t *bytes,
    size_t length,
    FvSession **out_session
);
int32_t framevault_entry_count(
    const FvSession *session,
    size_t *out_count
);
int32_t framevault_for_each_entry(
    const FvSession *session,
    void *context,
    FvEntryCallback callback
);
int32_t framevault_free(FvSession *session);
```

The complete C declaration is checked in as `capstone/include/framevault.h`. The Rust source does not ask a C consumer to understand Rust layout, generics, references, `Vec`, `String`, `Result`, or trait objects.

FrameVault does **not** implement compression, encryption, authentication, signatures, memory mapping, networking, concurrency, async I/O, descriptor-relative extraction, or benchmark-driven optimization. These exclusions are part of the architecture. Adding them would either require later-course mechanisms or distract from the contracts being studied here.

## Architecture map

```text
src/domain.rs
    EntryKind, LogicalPath, Entry, Archive
    pure invariants; no I/O; no unsafe

src/checksum.rs
    deterministic corruption check
    explicitly non-cryptographic

src/codec.rs
    FRMVLT01 encode/decode
    bounds, limits, offsets, exact consumption
    safe Rust only

src/aligned.rs
    one manual allocation owner
    all raw allocation and slice construction concentrated here

src/store.rs
    bounded file loading
    same-directory candidate write and replacement
    target-conditioned durability evidence

src/path_policy.rs
    portable logical names to host destinations
    symlink preflight and create-new extraction
    explicit race limitation

src/process_capture.rs
    shell-free command construction
    structured portable capture payload
    explicit post-capture—not hard runtime—limit

src/ffi.rs
    C records, status codes, raw ranges, opaque session
    panic containment and callback lifetime contract

src/app.rs
    command parsing and product orchestration

src/main.rs
    stdout, stderr, and process exit behavior
```

The unsafe dependency cone is intentionally narrow. `codec`, `domain`, `store`, `path_policy`, `process_capture`, and `app` use ordinary safe Rust. The `aligned` module contains manual allocation. The `ffi` module necessarily receives raw foreign pointers. This separation allows review to ask two different questions:

1. Is the safe product behavior correct under its stated input and platform contracts?
2. Are the unsafe preconditions established and preserved by the enclosing abstraction?

Do not combine those questions. A memory-safe decoder can still accept the wrong format. A format-correct FFI function can still be unsound if it creates a slice from an invalid pointer.

## The FRMVLT01 format

### Header

Every archive begins with sixteen bytes:

| Offset | Width | Field | Encoding | Rule |
|---:|---:|---|---|---|
| 0 | 8 | magic/version | bytes | exactly `FRMVLT01` |
| 8 | 4 | entry count | little-endian `u32` | no more than configured maximum |
| 12 | 4 | reserved | little-endian `u32` | must be zero |

The magic identifies both the family and version. Version one uses strict decoding. An unknown magic is rejected rather than guessed. The reserved field must be zero so a future version can assign meaning without an old decoder silently ignoring data it does not understand.

### Entry header

Each entry begins with twenty bytes:

| Relative offset | Width | Field | Encoding | Rule |
|---:|---:|---|---|---|
| 0 | 1 | kind | `u8` | `1 = file`, `2 = command capture` |
| 1 | 1 | flags | `u8` | must be zero in version one |
| 2 | 2 | name length | little-endian `u16` | within configured limit |
| 4 | 8 | payload length | little-endian `u64` | fits host and configured limits |
| 12 | 4 | payload checksum | little-endian `u32` | FNV-1a over payload |
| 16 | 4 | reserved | little-endian `u32` | must be zero |
| 20 | variable | name | UTF-8 bytes | valid `LogicalPath` |
| after name | variable | payload | opaque bytes | exact declared length |

The checksum detects accidental changes. It does not authenticate the writer, prevent chosen-prefix attacks, or protect against deliberate corruption. A security-sensitive archive would need a separately designed cryptographic authenticity layer and key-management policy.

### Decoder order

The decoder applies checks in this order:

1. reject input above the total archive limit;
2. read and compare the complete magic;
3. decode entry count and header reserved field;
4. reject count above the entry limit;
5. for each entry, check the fixed header range before interpreting it;
6. reject unknown kind, nonzero flags, and nonzero reserved field;
7. convert name and payload lengths without truncating casts;
8. enforce name, payload, and cumulative payload limits;
9. check complete variable ranges before borrowing them;
10. validate name UTF-8;
11. validate logical path grammar;
12. verify payload checksum;
13. copy the validated payload into the owned domain value;
14. reject duplicate logical names;
15. reject trailing bytes.

This order is not arbitrary. It prevents a declared length from authorizing allocation before the decoder knows the value fits the host and policy. It also avoids constructing a partially valid `Archive` and later discovering a representation error.

### Limits

`Limits` has five independent controls:

```rust
pub struct Limits {
    pub max_archive_bytes: usize,
    pub max_entries: usize,
    pub max_name_bytes: usize,
    pub max_payload_bytes: usize,
    pub max_total_payload_bytes: usize,
}
```

Each controls a different pressure:

- `max_archive_bytes` bounds the complete input accepted by file loading or FFI decoding;
- `max_entries` bounds loop and per-entry overhead;
- `max_name_bytes` prevents pathological identity data;
- `max_payload_bytes` limits one allocation;
- `max_total_payload_bytes` limits the sum even when every individual entry is legal.

Do not replace this with one total limit. Ten thousand zero-byte entries can be expensive even though payload total is zero. Many medium entries can evade a per-entry limit while exhausting the total budget.

## Domain invariants

### `LogicalPath`

A logical archive name is not a host path. It is a portable, normalized identifier with `/` separators. Construction rejects:

- empty text;
- leading `/` or `\\`;
- any backslash;
- any colon, avoiding drive-prefix and scheme ambiguity;
- NUL and control characters;
- empty components;
- `.` components;
- `..` components.

The type stores only a validated string. Every later use can rely on those lexical properties without repeating checks. It does **not** claim that joining the name below a host directory creates an adversarially secure filesystem sandbox. That is a separate operating-system problem.

### `Archive`

An `Archive` contains entries in deterministic source order and enforces unique logical names. Order matters because listing, FFI traversal, golden bytes, and reproducible encoding all use it. Duplicate-name rejection occurs both when constructing an archive from ordinary Rust values and when decoding bytes.

The domain model does not expose mutable entry fields. A caller cannot change an entry name after insertion and invalidate uniqueness behind the archive’s back.

## File loading

`store::load` does not call `fs::read` immediately. It follows a bounded sequence:

1. open the file;
2. read metadata length;
3. reject length above `max_archive_bytes`;
4. convert length to `usize` fallibly;
5. allocate one `AlignedBytes` region;
6. read exactly the declared length;
7. probe for one additional byte to detect growth during the read;
8. decode the complete region.

This is not a general snapshot guarantee. The file can still be modified in ways metadata/probe checks do not detect. It does prevent an obvious unbounded read and detects simple growth or shrink behavior around the read.

The aligned allocation is educational. A production decoder could use a `Vec<u8>` unless a downstream API requires alignment. The value here is architectural: one manually allocated owner feeds a much larger safe decoder surface.

## Transactional replacement

### State sequence

`save_atomic` encodes the entire archive before touching the destination. It then:

1. identifies the destination parent, using `.` for a bare relative filename;
2. creates the parent directory if needed;
3. reserves a sibling temporary name with `create_new`;
4. writes every encoded byte;
5. flushes the file writer;
6. synchronizes the temporary file;
7. closes the temporary handle;
8. installs the candidate;
9. synchronizes the parent directory on Unix;
10. removes the temporary file on any failed path where it still exists.

The temporary name includes the process ID and a bounded attempt counter. `create_new` is the authority: existence checks do not reserve names.

### Platform claim

On Unix, `std::fs::rename` is used for same-filesystem replacement of an existing destination. On non-Unix targets, this standard-library implementation refuses replacement when a destination already exists, because it cannot honestly claim equivalent overwrite semantics from the portable API alone.

This is a deliberate product choice. A weaker implementation might remove the old destination and rename the new file, but that creates a visible absence window and can lose the old file if the second operation fails. FrameVault prefers an explicit unsupported result over a silently weaker guarantee.

### Failure states

| Failure point | Destination | Candidate |
|---|---|---|
| encode | unchanged | not created |
| reserve candidate | unchanged | none or unrelated collision preserved |
| write | unchanged | removed best-effort |
| flush | unchanged | removed best-effort |
| file sync | unchanged | removed best-effort |
| rename/install | unchanged where operation fails before replacement | removed best-effort |
| parent sync after successful rename | new destination may already be visible | no candidate |

The last row matters. A failure after rename cannot be described as “nothing changed.” The error means the desired durability evidence was not fully obtained, not necessarily that the new name is absent.

## Extraction

`extract` loads and validates the archive first. It then processes each logical entry through `path_policy::write_new_file`.

For every destination:

1. create or inspect the extraction base;
2. reject a symlink base;
3. walk parent components one at a time;
4. reject existing symlink ancestors;
5. reject existing non-directory ancestors;
6. create missing directories;
7. reject an existing final object;
8. open the final path with `create_new`;
9. write, flush, and synchronize the file;
10. remove a partial final file if writing fails;
11. synchronize the parent directory where the implementation supports it.

This prevents lexical traversal, simple symlink redirection present at inspection time, and overwrite. It does not prevent a hostile local actor from replacing a checked directory between metadata inspection and final creation. The course names that limitation because security claims must follow the actual API structure.

A stronger Unix design would retain directory file descriptors and use descriptor-relative operations with no-follow flags. That design is valuable, but it is platform-specific and large enough to distract from the cross-platform foundation taught here.

## Process capture

### No shell

The `capture` command expects:

```text
framevault capture result.fv -- program argument...
```

The delimiter separates FrameVault options from the child program. The implementation passes the program and each argument directly to `Command`. It never joins them into one shell string.

The portable capture format requires Unicode program and argument text. Invocation still starts from `OsStr`/`OsString`; Unicode conversion is a storage-format policy applied before archive encoding, not an assumption that native process arguments are always UTF-8.

### Streams and status

Captured stdout and stderr remain independent byte vectors. A child may emit binary data or invalid UTF-8. Display conversion is not part of capture.

Exit status is represented as `Option<i32>`. `Some(code)` means the platform exposed a numeric code. `None` preserves signal or other platform termination without inventing a number.

### Storage limit

`Command::output` drains the child’s stdout and stderr and returns complete vectors. FrameVault checks their combined size after return. Therefore:

```text
property: accepted stored capture is within the configured limit
not claimed: child output memory usage was bounded while the child ran
```

A hard bound requires an architecture that drains streams incrementally, coordinates both pipes to avoid deadlock, and terminates or truncates overproducing children. That naturally introduces threads, async I/O, or platform-specific polling and belongs to Courses 7 and 8.

### FVCMD01 payload

A command entry stores a separate versioned payload:

- magic `FVCMD01\0`;
- length-prefixed UTF-8 program;
- `u16` argument count;
- each length-prefixed UTF-8 argument;
- status kind plus `i32` value;
- stdout length;
- stderr length;
- stdout bytes;
- stderr bytes.

The payload decoder rejects truncation, unknown status kind, invalid text, numeric overflow, and trailing bytes.

## The manual allocation owner

`AlignedBytes` has three fields:

```rust
pointer: NonNull<u8>
length: usize
alignment: usize
layout: Option<Layout>
```

The valid states are:

```text
length = 0
pointer = dangling non-null sentinel
layout = None
Drop performs no deallocation

length > 0
pointer = successful alloc_zeroed result
layout = Some(exact original layout)
Drop deallocates once with that layout
```

### Constructor proof

1. `Layout::from_size_align(length.max(1), alignment)` validates alignment and arithmetic.
2. Zero length returns before allocator invocation.
3. Nonzero length calls `alloc_zeroed` with the validated layout.
4. Null means construction fails and no owner is returned.
5. Non-null pointer and layout move into one `AlignedBytes` owner.

### Slice proof

`as_slice` requires `&self`, so safe code cannot simultaneously call `as_mut_slice`. For a nonempty value, the owner guarantees the pointer is live and valid for `length` initialized bytes. `from_raw_parts` therefore creates a shared slice tied to the borrow of the owner.

`as_mut_slice` requires `&mut self`, establishing exclusive access to the owner and its region. The returned mutable slice is tied to that exclusive borrow.

Zero length returns an ordinary empty slice without forming a raw slice from the dangling sentinel.

### Drop proof

If `layout` is `Some`, construction succeeded with exactly that layout and ownership was never transferred. `Drop` calls `dealloc` once. If `layout` is `None`, no allocation occurred and no deallocation is permitted.

The type does not manually implement `Send` or `Sync`. Course 6 refuses to make concurrency claims that belong to Course 7.

## C ABI design

### Status codes

```text
FV_OK = 0
FV_INVALID_ARGUMENT = 1
FV_INVALID_ARCHIVE = 2
FV_CALLBACK_STOPPED = 3
FV_PANIC_CONTAINED = 4
```

The ABI never returns Rust `Result`. Every fallible function returns one integer status and initializes documented output fields before or after validation according to its contract.

### Raw byte rule

For `(bytes, length)`:

- when `length == 0`, `bytes` may be null;
- when `length > 0`, `bytes` must be non-null and readable for exactly `length` bytes for the duration of the call.

The implementation handles zero length before calling `from_raw_parts`. It never creates a slice from null, even a zero-length slice.

### Stateless validation

`framevault_validate` requires a writable `FvReport`. It initializes the report first. Successful validation writes entry count, total payload bytes, and `SIZE_MAX` as the no-error sentinel. Decode failure writes the detected offset and returns `FV_INVALID_ARCHIVE`.

The function catches Rust panics and maps them to `FV_PANIC_CONTAINED`. This is a last boundary defense, not normal error handling.

### Opaque sessions

`framevault_open` initializes the output session pointer to null, decodes the borrowed bytes into an owned `Archive`, boxes the session, and transfers the raw pointer to C.

`framevault_entry_count` borrows the session for one call.

`framevault_for_each_entry` borrows the session and creates one stack `FvEntryView` per entry. Name and payload pointers borrow storage inside the session. The callback may inspect them only during that invocation. It must not retain the view or its fields, free or mutate the session, or unwind across the C ABI.

`framevault_free` accepts null as a no-op. A non-null pointer must be the unique live pointer returned by `open` and must be freed exactly once. `Box::from_raw` reconstructs ownership, and scope exit drops the archive.

### Panic boundary

Every exported fallible operation runs inside `catch_unwind(AssertUnwindSafe(...))`. The assertion is localized to the ABI shell. It says the boundary will convert an internal panic to a status; it does not make foreign callbacks unwind-safe. The callback contract still forbids unwinding.

## Ten increments

### Increment 51 — Establish the format and safe decoder

Create `domain`, `checksum`, and `codec`. Freeze golden bytes for one archive. Test:

- empty archive;
- one file;
- multiple kinds;
- every truncation point;
- unknown kind;
- nonzero flags and reserved fields;
- oversized name and payload;
- cumulative overflow;
- invalid UTF-8 name;
- path traversal name;
- duplicate name;
- checksum mismatch;
- trailing bytes.

Do not start file I/O until an in-memory byte slice can be decoded safely.

### Increment 52 — Add bounded load and transactional save

Implement `store`. Use metadata to reject obvious oversize before allocation, read exact length into owned storage, and probe for growth. Encode before candidate creation. Preserve the old destination on pre-install failures.

The acceptance question is not merely “does save work?” It is “what exact state remains after each failure boundary?”

### Increment 53 — Add extraction policy

Implement `LogicalPath` if it was not already part of decoding, then `path_policy`. Keep logical names separate from host paths. Refuse overwrite. Add a documented threat-model boundary.

Do not call the result a sandbox without naming the concurrent-mutation assumption.

### Increment 54 — Add direct process capture

Implement a portable command-capture payload and `capture` CLI command. Verify one argument containing spaces remains one argument. Verify nonzero exit status, stdout bytes, and stderr bytes remain distinct.

Document the post-capture limit honestly.

### Increment 55 — Freeze the unsafe dossier

Before manual allocation code, add a module-level explanation of the intended owner states and each unsafe operation. Keep the proposed fields private. Reject any public raw-pointer accessor not needed by the product.

### Increment 56 — Prove initialization and zero-length behavior

Use the batch-builder lab to establish the initialized-prefix model. In FrameVault, audit all pointer/length boundaries and zero-length cases. Ensure FFI design never creates a reference from null.

### Increment 57 — Implement `AlignedBytes`

Add allocation, safe slice access, and drop. Replace file-loading `Vec` allocation with `AlignedBytes` to exercise the abstraction. Keep the decoder unchanged; it receives `&[u8]` and does not know storage is manual.

This separation is the success criterion.

### Increment 58 — Add stateless C validation

Create C records, status codes, header, raw-range conversion, panic containment, and `framevault_validate`. Test the null/zero matrix and invalid offsets through Rust calls shaped like C.

### Increment 59 — Add opaque session lifecycle

Implement open, count, traversal callback, and free. Test one complete lifecycle, callback early stop, null rules, and deterministic order. State one ownership transfer and one release.

### Increment 60 — Complete CLI and audit

Connect create, list, verify, extract, capture, help, and version. Add process-level integration tests and the demonstration script. Run source, formatting, lint, unit, integration, doc, release, compiler-specimen, and documentation routes.

Then perform a manual audit: every unsafe operation must have a local safety comment and a supporting type invariant; every exported unsafe function must have a `# Safety` contract; every platform-conditioned statement must be labeled; every non-goal must remain absent.

## End-to-end systems proof

FrameVault is not seven independent demonstrations. Its safety depends on assumptions crossing layers. An archive entry decoded from bytes later becomes a logical path, a host path, a displayed CLI row, an FFI view, and possibly a payload stored in aligned memory. A defect in the earliest representation can invalidate every later proof.

### Claim ledger

For each major claim, state its evidence class:

| Claim | Evidence class | What supports it | What remains outside the claim |
|---|---|---|---|
| an archive is structurally valid | runtime validation over checked ranges and canonical rules | decoder tests at every truncation and malformed field | producer identity and malicious tampering |
| save is failure-atomic before installation | protocol/state-machine property | encode-first, sibling temp, complete write, sync, close, rename; injected failures | universal power-loss durability on every filesystem |
| extraction names are lexically safe | logical-name validation and component policy | traversal, separator, prefix, empty-component tests | adversarial races after pathname checks |
| child invocation preserves arguments | `Command` program-plus-arguments contract | process fixture echoing distinct arguments | behavior of an untrusted child after launch |
| `AlignedBytes` deallocates correctly | unsafe abstraction proof | exact stored layout, private fields, drop tests, safety review | allocator bugs or unsupported manual thread-safety claims |
| C validation does not unwind into C | panic boundary contract | `catch_unwind` at exported boundary and status mapping | foreign caller violating pointer preconditions |
| opaque session is freed exactly once by correct callers | ABI ownership protocol | open/free lifecycle tests and header documentation | use-after-free or double-free by a contract-violating caller |

This table prevents an implementation observation from becoming an exaggerated product promise.

### Cross-layer successful trace

Trace `framevault create vault.fv --entry reports/run.txt source.txt`:

1. CLI parsing keeps the destination host path and logical archive name in different types.
2. `LogicalPath::parse` validates the portable name before filesystem output begins.
3. Source bytes are read into owned payload data; I/O errors retain the host path and operation.
4. `Archive::new` rejects duplicate logical names and preserves entry order.
5. `encode` calculates every length with checked conversions, writes fixed little-endian fields, computes the corruption checksum, and produces one complete candidate buffer.
6. The store reserves a same-directory temporary file exclusively, writes all bytes, flushes and synchronizes it, closes it, installs the destination, and attempts parent-directory synchronization where supported.
7. The CLI reports success only according to the documented store result; it does not call the file universally crash-durable.

Now trace `framevault_verify` from C:

1. the caller provides pointer, length, and writable report storage under the header contract;
2. the exported function initializes the report before fallible decoding;
3. null-plus-zero input becomes an empty slice without forming a reference from null; nonzero length requires readable storage;
4. safe decoding produces either an archive or an offset-bearing error;
5. the boundary maps the result to stable integer status and filled report;
6. any Rust panic is contained and converted to the documented panic status.

The two traces share the codec but not ownership or failure semantics. Keeping those differences explicit is the purpose of the architecture.

### Commit points and surviving state

FrameVault has more than one commit concept:

- **decoder acceptance:** the complete byte buffer has passed structural validation;
- **archive construction:** domain invariants such as unique logical names hold;
- **file installation:** rename makes the new destination pathname authoritative;
- **directory synchronization request:** the program has requested persistence of the name update where supported;
- **FFI open success:** allocation ownership has transferred to the foreign caller;
- **callback return:** temporary entry views cease to be valid;
- **free:** the foreign allocation obligation has been discharged.

For every error, name which commit points have occurred. A directory-sync failure after rename cannot honestly be reported as “nothing changed.” A callback returning stop is not a decode failure. A failed `framevault_open` must leave the output session null and transfer no ownership.

### Unsafe dossier review

Every unsafe operation must have a local proof connection:

| Unsafe operation | Required facts | Establishing boundary |
|---|---|---|
| construct slice from raw input | null/zero rule, readable range, no forbidden mutation during borrow | exported FFI contract plus immediate checks |
| write `FvReport` or output session | non-null, alignment, writable storage, non-overlap where required | exported function safety contract |
| reconstruct `Box<FvSession>` in free | pointer came from successful open, remains uniquely live, not previously freed | foreign ownership protocol |
| call foreign callback | function pointer valid, context contract upheld, no unwind/retention/reentrant free | callback contract in header and Rust docs |
| allocate/deallocate aligned bytes | valid layout, non-null allocation, initialized bytes, exact same layout at drop | private `AlignedBytes` constructor and fields |

The safe API must make it impossible for a safe Rust caller to violate these preconditions. The C API cannot make a violating foreign caller safe; it can only specify the contract, detect a subset of invalid arguments, initialize outputs, and avoid adding avoidable undefined behavior.

### Threat and portability boundaries

FrameVault deliberately does not claim:

- cryptographic authentication or confidentiality;
- safe extraction against a hostile concurrent actor changing path components between checks;
- hard peak-memory limits while capturing child output through `Command::output`;
- universal atomic replacement of an existing destination on every target;
- universal power-loss durability;
- thread-safe concurrent use of opaque sessions;
- ABI stability for unversioned private Rust layout;
- correctness of a foreign caller that violates pointer, lifetime, callback, or exactly-once-free obligations.

These exclusions are part of the design, not unfinished work. Adding any one would require new mechanisms—cryptography, descriptor-relative filesystem APIs, concurrent pipe draining, platform-specific replacement primitives, synchronization, or a broader ABI versioning strategy—and belongs in a later course or product-specific extension.

### Test matrix

#### Codec

Test every truncation point of a valid archive, bad magic and version, unknown kind or flags, invalid UTF-8, invalid logical path, excessive count/length/total, checksum mismatch, duplicate name, and trailing bytes. Round-trip tests are necessary but insufficient because encoder and decoder can share the same defect.

#### Store

Inject short writes and failures at reservation, write, flush, sync, close, rename, directory sync, and cleanup. Assert both returned error and visible destination/temp state.

#### Paths

Test absolute forms, `.` and `..`, repeated separators, backslashes, drive/prefix markers, control bytes, collisions, existing final files, non-directory ancestors, and symlink ancestors. Keep a separate note that these tests do not prove race-free containment.

#### Processes

Use a fixture program that reports received arguments, selected environment, status, stdout bytes, and stderr bytes. Test non-UTF-8-capable byte handling where the target permits it and distinguish nonzero child status from launch failure.

#### Unsafe owner

Test zero length, invalid and valid alignments, pointer alignment, zero initialization, mutation through safe slices, movement of the owner, and destruction. Review with Miri when available, while recognizing that Miri is evidence rather than a replacement for the written safety proof.

#### FFI

Test null output, null-plus-zero input, null-plus-nonzero input, valid and invalid archives, initialized reports on failure, open/access/free lifecycle, callback continuation and early stop, and stable header syntax from C11 and C++17 consumers.

### Independent cross-layer change

Add a `Metadata` entry kind whose payload is UTF-8 `key=value` lines with unique keys and canonical sorted encoding.

Before coding, update:

1. wire kind allocation and unknown-kind compatibility policy;
2. payload size and line/key/value limits;
3. structural versus domain validation order;
4. canonical encoder sorting and duplicate rejection;
5. CLI list and extract behavior;
6. C `FvEntryView` semantics without changing its layout unnecessarily;
7. process-capture code, which must not accidentally emit this kind;
8. tests for old archives, new archives, unknown kinds, malformed metadata, and round trips;
9. documentation and version policy if old decoders cannot safely reject or skip the new entry.

Then trace one malformed metadata archive through the Rust CLI and C validator. Both may share the decoder, but their error surfaces and ownership obligations differ. The feature is incomplete until the compatibility and FFI views are reviewed, not merely when Rust decoding succeeds.

### Final defense

Present five diagrams:

1. `FRMVLT01` byte offsets and limits;
2. file replacement state machine with commit point;
3. logical-name to host-path policy and threat boundary;
4. `AlignedBytes` allocation/borrow/drop states with unsafe preconditions;
5. C session ownership and callback lifetime protocol.

For each diagram, identify one tempting stronger claim that the implementation does not support. Then show the test, type, runtime check, safety contract, operating-system result, or foreign obligation that supports every claim you do make.

## Acceptance matrix

| Area | Required evidence |
|---|---|
| format | golden bytes, round trip, all truncations, strict unknown/reserved handling |
| limits | per-name, per-payload, count, cumulative, complete archive |
| storage | new save, Unix replacement, cleanup on error, bounded load |
| extraction | nested output, traversal rejection, overwrite refusal, symlink test where available |
| process | direct arguments, binary streams, nonzero/no-code status model, capture payload round trip |
| unsafe owner | zero length, alignment, zero initialization, mutation, one drop proof |
| FFI stateless | null/zero matrix, invalid archive, report initialization, panic status contract |
| FFI session | open, count, ordered callbacks, early stop, free, null free |
| CLI | create/list/verify/extract route and capture route through real processes |
| documentation | exact format, threat model, portability, safety contracts, C header |

## Design defense

A final review should answer these questions without vague language:

1. Why is the decoder entirely safe while the file buffer is manually allocated?
2. Which field prevents an old decoder from silently accepting future semantics?
3. Why is cumulative payload length checked separately from archive input length?
4. What can be true after a parent-directory synchronization error?
5. Why does the extraction policy reject backslashes even on Unix?
6. Which local attacker can still escape the path policy, and what stronger API family would be needed?
7. Why is capture output not decoded as UTF-8?
8. Why is the capture limit not a hard memory bound?
9. Which exact unsafe operations exist in `AlignedBytes`?
10. What type-system facts make the safe slice methods preserve aliasing?
11. Why does the FFI allow null with zero length but still avoid `from_raw_parts(null, 0)`?
12. Which exported function transfers ownership, and which returns it?
13. What may a callback retain after it returns?
14. What does panic containment protect, and what does it not excuse?
15. Why is the checksum not a security boundary?
16. Which code would need to change to add a new entry kind without breaking strict decoding?
17. Which properties are tested but not proved universally?
18. Which features were excluded because they belong to later courses?

If any answer starts with “basically,” “usually,” or “Rust handles it,” return to the relevant module and write the actual contract.
