# 52 — Files, Durability, and Transactional Replacement

**Course 6, day 2 · Module 52 of 90**  
`█████████████████░░░` **52/90**

[← Module 51: Binary Data Contracts: Bytes, Endianness, and Checked Parsing](../module-51-binary-data-contracts/index.md) · [Course 6 overview](../index.md) · [Ninety-module map](../../../COURSE_MAP.md) · [Module 53: Paths, Names, and Platform Boundaries →](../module-53-paths-names-and-platform-boundaries/index.md)

## The question

> What has actually been promised after a file operation succeeds: bytes written, buffers flushed, data synchronized, a name replaced, or a recoverable durable state?

## Why this comes now

Module 51 established a trustworthy in-memory format. A real systems product must persist it through APIs that permit partial I/O, delayed errors, concurrent filesystem changes, and platform-specific rename behavior. This module turns “save the file” into a sequence of explicit state transitions and claims. It also corrects a common overstatement: no short standard-library recipe proves crash durability on every filesystem and operating system.

## What you will be able to do

- Distinguish read, write, flush, data synchronization, metadata synchronization, and directory-entry durability.
- Handle short reads and writes through the `Read` and `Write` contracts.
- Use `OpenOptions` to make creation and truncation policy explicit.
- Design a same-directory temporary-file replacement with cleanup on failure.
- State the portability limits of `rename`, file locking, and durable replacement.
- Preserve the previous valid file when encoding or writing fails.

## Core model

### A file is a resource plus an evolving external state

`File` is an owned handle whose methods ask an operating system and filesystem to perform work. Success does not mean “the disk now contains exactly my new durable document.” It means the documented operation completed at a particular boundary.

The state you care about may include file contents, length, permissions, directory entries, and the relationship between a path and an underlying file object. Each can fail or change independently. Systems code should name the strongest claim it can support and avoid turning a convenient local observation into a universal guarantee.

### Reads and writes may be partial

`Read::read` may return fewer bytes than requested without reaching end of file. `Write::write` may accept only part of the buffer. Correct code either loops or uses combinators whose contract loops:

```rust
reader.read_exact(&mut header)?;
writer.write_all(encoded)?;
```

`read_exact` distinguishes a short stream through an error; `write_all` repeatedly writes until all bytes are accepted or an error occurs. Neither operation validates the meaning of bytes. Neither makes data durable.

When streaming a large payload, a bounded loop should also track total bytes and reject growth beyond policy. `read_to_end` is convenient only after a trusted or bounded source size has been established.

### OpenOptions is part of the state machine

Opening a file is not one generic action. Ask for the exact capability and transition:

```rust
let file = std::fs::OpenOptions::new()
    .write(true)
    .create_new(true)
    .open(&temporary_path)?;
```

`create_new(true)` makes an existing temporary name an error rather than silently truncating it. A direct destination write might use `truncate(true)`, but FrameVault avoids that because a later encoding or write failure would destroy the previous valid archive.

Read-only operations should not request write access. Append semantics are different from seek-then-write, especially when multiple writers exist. Capability choice is part of correctness and least authority.

### Buffering is not persistence

`BufWriter` reduces system calls by holding bytes in memory. `flush` asks the writer to pass buffered bytes to the underlying writer. It does not necessarily ask the operating system to synchronize storage media.

`File::sync_data` requests synchronization of file content and the metadata required to retrieve that content. `sync_all` also requests all metadata. Filesystems, hardware caches, mount options, and operating-system semantics still affect the durability claim. The API can return errors that were delayed from earlier writes.

A precise save routine therefore treats `flush`, `sync_all`, and `rename` as separate fallible steps and reports which one failed.

### Replacement protects the previous valid value

A common update protocol is:

1. encode the complete new value independently;
2. create a uniquely named temporary file in the destination directory;
3. write all bytes;
4. flush buffered writers;
5. synchronize the temporary file when the product requires it;
6. rename the temporary path over the destination according to platform policy;
7. optionally synchronize the directory using platform-specific support;
8. remove an abandoned temporary file on failure.

Using the same directory improves the chance that source and destination are on the same filesystem, a usual precondition for atomic rename semantics. It does not make every step universally crash-atomic or durable.

The essential application guarantee is simpler and testable: before rename succeeds, the old destination remains untouched; after successful rename, readers opening the destination see the replacement name. Stronger claims require target-specific evidence.

### Temporary names need collision and attack policy

A predictable `.tmp` name can collide with another process or be pre-created. The standard library has no cross-platform secure temporary-file constructor. For the course product, generate a name from destination, process ID, and a monotonic attempt counter, then open with `create_new(true)` and retry a bounded number of times.

This is sufficient for a controlled local tool but is not presented as a hardened hostile-directory solution. Production code often uses a well-reviewed temporary-file library or platform-specific APIs that provide stronger creation semantics. The lesson is to state the threat model rather than label every temporary file “safe.”

### Rename has platform and filesystem conditions

`std::fs::rename` maps to platform facilities and can fail when source and destination cross filesystems, when the destination type conflicts, when permissions deny replacement, or when platform sharing rules prevent it. Whether replacement is atomic, and what happens under crash, depends on the platform and filesystem.

Do not add an existence check before rename and assume the result remains true. That creates a time-of-check/time-of-use window. Attempt the operation and handle its result. When a product needs a no-replace rename or exchange operation, use a platform-specific API or a crate that documents the contract.

### Seek changes position, not file structure

`Seek` is useful for fixed headers, indexes, and patching known offsets. It does not make a multi-step update transactional. If a program overwrites a header and crashes before the payload is updated, the file may become self-inconsistent.

Prefer encode-then-replace for small and medium artifacts. For large stores where full replacement is too expensive, design a journaled or append-only format with commit records, checksums, and recovery rules. That is a format architecture decision, not a clever use of `seek`.

### Directory traversal and ordering are not implicit

`read_dir` yields entries through an iterator and can encounter errors after iteration begins. Returned order is not a portable deterministic order. If output or generated data requires stable ordering, collect the relevant names, define a comparison policy, and sort them.

Filename comparison must operate on `OsStr` or an explicit portable logical representation. Converting every path through lossy Unicode can collapse distinct names. Module 53 develops that boundary.

### Test failure states, not only successful saves

A persistence test should cover:

- encoder failure before any destination change;
- temporary creation collision;
- write failure using a custom `Write` implementation;
- flush failure;
- synchronization failure where injectable;
- rename failure;
- cleanup failure that must not hide the primary error;
- successful replacement;
- old destination preserved before the commit point.

The standard filesystem does not make every failure easy to inject. Isolate the pure encoding and write protocol behind small functions so custom writers can exercise partial writes and errors deterministically.

### A durability claim ladder

Persistence conversations become confused because “saved” is used for several different states. Use a claim ladder:

1. **Encoded** — a complete byte sequence exists in memory.
2. **Accepted by writer** — every byte was accepted by the `Write` implementation.
3. **Flushed through buffering** — language-level buffers handed bytes to the underlying file handle.
4. **File synchronization requested successfully** — the operating system reported success for `sync_data` or `sync_all`.
5. **Destination name replaced** — the namespace operation reported success.
6. **Directory metadata synchronization requested successfully** — available only through target-specific support in many designs.
7. **Survives a specified crash model** — established by filesystem, mount, hardware, and target evidence, not inferred from the previous words alone.

A product may reasonably promise level 5 failure atomicity under a controlled local filesystem and separately request levels 4 and 6. It should not silently rename that combination “guaranteed durable everywhere.”

### Worked replacement protocol

A reusable store can separate pure bytes from filesystem effects:

```rust
pub fn replace_bytes(path: &Path, bytes: &[u8]) -> Result<(), StoreError> {
    let parent = path.parent().unwrap_or_else(|| Path::new("."));
    let (temporary_path, mut temporary) = create_temporary(parent, path)?;

    let result = (|| {
        temporary
            .write_all(bytes)
            .map_err(|source| StoreError::WriteTemp {
                path: temporary_path.clone(),
                source,
            })?;
        temporary
            .flush()
            .map_err(|source| StoreError::FlushTemp {
                path: temporary_path.clone(),
                source,
            })?;
        temporary
            .sync_all()
            .map_err(|source| StoreError::SyncTemp {
                path: temporary_path.clone(),
                source,
            })?;
        drop(temporary);
        std::fs::rename(&temporary_path, path).map_err(|source| {
            StoreError::Replace {
                from: temporary_path.clone(),
                to: path.to_path_buf(),
                source,
            }
        })?;
        Ok(())
    })();

    if result.is_err() {
        let _cleanup_result = std::fs::remove_file(&temporary_path);
    }
    result
}
```

This sketch still needs a platform policy. Some platforms do not replace an existing destination under the same conditions; open handles and file types matter. A production implementation may need target-specific replacement. The design value is that the commit point is explicit and cleanup cannot replace the primary failure.

The encoder runs before `replace_bytes`. If encoding fails because an entry name exceeds the field width, no temporary file is needed and the destination is unchanged. This is strong failure isolation.

### Error injection without a fake filesystem

Pure helper functions can expose I/O behavior through `Write`:

```rust
struct FailAfter {
    accepted: usize,
    limit: usize,
}

impl Write for FailAfter {
    fn write(&mut self, input: &[u8]) -> io::Result<usize> {
        if self.accepted >= self.limit {
            return Err(io::Error::new(io::ErrorKind::Other, "injected"));
        }
        let allowed = (self.limit - self.accepted).min(input.len()).min(3);
        self.accepted += allowed;
        Ok(allowed)
    }

    fn flush(&mut self) -> io::Result<()> { Ok(()) }
}
```

This tests short writes and mid-stream failure. A separate writer can fail on flush. Filesystem integration tests then cover path creation, replacement, and cleanup in a fresh temporary directory created with `create_dir` and a collision-resistant name.

The test suite should inspect the destination bytes after every failure. Merely checking an error result does not prove that the old file survived.

### Append-only and replacement are different architectures

When archives grow too large for complete replacement, do not quietly mutate this protocol. An append-only design needs record framing, transaction or commit markers, recovery after torn writes, compaction, and concurrency policy. It can provide excellent properties, but it is a different course product.

Module 52 teaches a general decision rule: choose the simplest persistence architecture whose failure states you can enumerate. Direct overwrite has fewer files but destroys the previous value early. Replacement preserves the old value until commit. Journaling avoids full rewrites but introduces recovery state. Each design moves complexity; none removes it.

## Use the idea in a complete program

FrameVault adds `store.rs`: bounded file loading, complete encoding before commit, same-directory temporary creation with `create_new`, `write_all`, `flush`, `sync_all`, and replacement. Its documentation promises failure-atomic replacement with respect to pre-rename errors on supported local usage, not universal crash durability. Tests retain the previous archive when encoding or temporary writing fails.

The matching independent laboratory is [Atomic Archive Store](../../labs/module-02-atomic-archive-store/README.md). It isolates the mechanism so you can test the proof without carrying the whole capstone in your head.

## Practice sequence

Complete the [workbook](workbook.md) by naming the visible and durable state after every injected failure. Build the Atomic Archive Store lab, then trace FrameVault's save path from encoded bytes through temporary cleanup and post-rename directory synchronization. Your explanation must say whether the old value, new value, or uncertain durability survives each boundary.

## Ready to continue

You are ready when you can name the commit point, distinguish buffering from synchronization, explain why the old file survives every pre-commit failure, and qualify every portability claim about rename and durability.

## Primary Rust references

- [Rust standard library: File](https://doc.rust-lang.org/std/fs/struct.File.html)
- [Rust standard library: OpenOptions](https://doc.rust-lang.org/std/fs/struct.OpenOptions.html)
- [Rust standard library: rename](https://doc.rust-lang.org/std/fs/fn.rename.html)
- [Rust standard library: Write](https://doc.rust-lang.org/std/io/trait.Write.html)

## Continue

1. Complete the [Module 52 workbook](workbook.md) and freeze every prediction before compiling.
2. Build [Laboratory 52 — Atomic Archive Store](../../labs/module-02-atomic-archive-store/README.md) from its public contract.
3. Apply the Module 52 increment in the [FrameVault engineering guide](../capstone.md).
4. Review the [reasoned solutions](solutions.md) only after an independent attempt, then revise the causal model rather than copying code shape.
