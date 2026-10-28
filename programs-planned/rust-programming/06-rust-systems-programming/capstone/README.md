# FrameVault

## Course role

FrameVault is a versioned binary archive with checked parsing, transactional replacement, extraction policy, process capture, one manual allocation owner, and a C ABI with opaque sessions and callback rules.

FrameVault is not a showcase of ten independent features. It is the place where the course’s mechanisms must coexist without creating a second owner for state, validation, order, failure, compatibility, or resource policy.

## Invariants carried through the product

- No hostile length, offset, count, or path component is trusted before bounded validation.
- File replacement distinguishes pre-commit failure, visible commit, and durability evidence.
- Native paths and portable archive names remain separate types and threat models.
- Every unsafe operation is justified by a local invariant reachable from the safe facade.
- Manual allocation records the exact layout used for allocation and deallocation.
- C declarations, Rust ABI declarations, nullability, panic policy, and ownership agree.

## Module-to-product map

| Module | Mechanism added | Acceptance criterion |
|---:|---|---|
| 51 | Binary Data Contracts: Bytes, Endianness, and Checked Parsing | Define a binary format as a versioned contract rather than a sequence of convenient writes |
| 52 | Files, Durability, and Transactional Replacement | Distinguish read, write, flush, data synchronization, metadata synchronization, and directory-entry durability |
| 53 | Paths, Names, and Platform Boundaries | Distinguish portable logical names, `Path`, `PathBuf`, `OsStr`, and display text |
| 54 | Processes, Environments, and Standard Streams | Construct commands from a program plus arguments, not an interpolated shell line |
| 55 | Unsafe Rust as a Proof Boundary | Name the operations Rust requires an unsafe context to perform |
| 56 | Raw Pointers, Provenance, and Uninitialized Memory | Distinguish raw pointers from references and explain why conversion does not transfer ownership |
| 57 | Manual Allocation and Owning Unsafe Abstractions | Construct and validate `Layout` values without unchecked size arithmetic |
| 58 | C FFI: ABI, Strings, Pointers, and Error Boundaries | Distinguish ABI compatibility from semantic validity and ownership |
| 59 | Foreign Resources, Callbacks, and Wrapper Architecture | Separate raw bindings, checked unsafe shims, and safe domain wrappers |
| 60 | Integrated Systems Design, Testing, and Audit | Draw one boundary map from external bytes to final effects and back to foreign callers |

## Reading route

1. Read the FrameVault contract and non-goals in the [engineering guide](../course-book/capstone.md).
2. Locate the type or component that owns each invariant above.
3. Run the baseline tests and one end-to-end demonstration before changing code.
4. Implement only the current module increment and its adversarial test.
5. Trace success, rejection, partial failure, cleanup, order, and capacity through the public surface.
6. Re-run the complete course route, then explain which claims remain conditioned on a compiler, target, scheduler, peer, workload, or operating system.

FrameVault is the cumulative product for **Rust Systems Programming**. It is a small versioned binary archive, file-replacement, extraction, process-capture, manual-allocation, and C-ABI system. Its purpose is not to compete with established archive formats. Its purpose is to put several systems boundaries in one codebase where every claim can be inspected.

The implementation keeps five responsibilities separate:

1. `codec` converts between hostile bytes and validated Rust domain values without raw pointers.
2. `store`, `path_policy`, and `process_capture` mediate filesystem and process effects while naming the limits of their guarantees.
3. `aligned` contains the capstone’s manually allocated storage and exposes only ordinary slices.
4. `ffi` presents a C-compatible stateless validator and opaque owning session without exposing Rust layout, unwinding, or allocator details.
5. `app` and the binary assemble those pieces into a deterministic command-line product.

## Commands

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

`create` accepts a host source path directly or an explicit `--entry <logical-name> <source>` triple. The separate tokens avoid ambiguity when a host path contains `=`. Use `--source <source>` when a host path itself begins with `--`. Logical names are portable archive names, not host paths: they use `/`, remain relative, and reject empty components, `.`, `..`, backslashes, drive markers, NUL, and control characters.

`capture` invokes the program directly with `std::process::Command`; it does not construct a shell command. Standard output and standard error remain separate byte vectors. Because `Command::output` buffers before returning, the configured storage limit is a post-capture acceptance limit rather than a hard memory bound. A hostile child requires a concurrent or asynchronous draining design, which belongs to later courses.

A nonzero child exit status is recorded as captured data; it does not make the FrameVault `capture` command fail when spawning, collection, encoding, and storage all succeed. Process execution failure and observed child outcome are separate contracts.

## Binary format

The version-one archive begins with the eight-byte magic `FRMVLT01`, a little-endian entry count, and a zero reserved field. Each entry stores a kind, flags, name length, payload length, non-cryptographic checksum, another reserved field, UTF-8 logical-name bytes, and opaque payload bytes. The decoder checks the full representation before constructing an `Archive`:

- total input size;
- entry count;
- every field boundary;
- host integer conversion;
- per-name and per-payload limits;
- cumulative payload size;
- UTF-8 and logical-path validity;
- known kind and zero flags/reserved fields;
- payload checksum;
- duplicate names;
- exact end-of-input.

The checksum detects accidental corruption only. It is not an authenticity mechanism and must not be described as one.

## File replacement and durability

`save_atomic` encodes before touching the destination, creates a new temporary file in the destination directory, writes all bytes, flushes userspace buffering, synchronizes the temporary file, and then installs it. On Unix, same-directory rename is used to replace an existing path, followed by parent-directory synchronization. On other platforms the standard-library implementation refuses to overwrite an existing destination when it cannot express an equivalent replacement guarantee.

This sequence is stronger than direct truncating writes, but the result is still a precisely scoped operating-system claim rather than a universal promise about every filesystem, storage controller, power-loss model, or network mount.

## Extraction policy

Extraction combines validated logical paths, one-component-at-a-time parent creation, symlink inspection, and `create_new` final-file creation. It refuses overwrite. It does not claim adversarial race-proof containment: pathname inspection and pathname creation are separate operations. A stronger sandbox must use descriptor-relative platform APIs and a threat model that accounts for concurrent filesystem mutation.

Extraction is transactional per file, not across the complete archive. If a later entry fails, files already created by this invocation remain and existing files are never overwritten. This makes partial success observable and preserves evidence for recovery; callers that require all-or-nothing tree installation need a staged-directory protocol and target-specific replacement policy.

## Unsafe core

`AlignedBytes` is intentionally small. Its proof obligations are:

- a non-empty pointer comes from `alloc_zeroed` with the stored `Layout`;
- the pointer remains live until `Drop`;
- safe shared and mutable slice methods preserve Rust aliasing;
- zero-length state performs no allocation or deallocation;
- `Drop` deallocates exactly once with the original layout.

The rest of the codec does not need raw pointers. This is the desired shape of unsafe abstraction: a narrow proof boundary with a disproportionately large safe surface.

## C ABI

`include/framevault.h` defines the foreign contract. The library exports:

```text
framevault_version
framevault_validate
framevault_open
framevault_entry_count
framevault_for_each_entry
framevault_free
```

The ABI uses fixed-layout C records, integer status codes, raw byte ranges, an opaque session pointer, and a callback whose entry view is borrowed only for the duration of the call. Public unsafe Rust functions state their pointer and ownership requirements. Internal panics are caught and converted to `FV_PANIC_CONTAINED`; callers must still obey the rule that foreign callbacks do not unwind across the C boundary.

## Verification

From this directory:

```bash
cargo fmt --all -- --check
cargo clippy --all-targets -- -D warnings
cargo test --all-targets
cargo test --doc
cargo build --release
sh scripts/demo.sh
```

The course-level `make proof` route also checks all labs, compiler specimens, source policy, local links, and the unified reader book.

## Architectural exclusions

FrameVault deliberately does not include compression, encryption, signatures, memory mapping, network I/O, threads, async runtimes, OS-specific descriptor sandboxes, or benchmark claims. Those would obscure the systems contracts this course is designed to expose or belong to later courses. The product is complete within its declared boundary: checked binary decoding, transactional storage, defensive extraction, direct process capture, one audited unsafe owner, and a usable C ABI.
