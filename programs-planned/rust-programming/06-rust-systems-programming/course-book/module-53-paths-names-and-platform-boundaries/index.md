# Module 53 — Paths, Names, and Platform Boundaries

**Course 6 · Day 3 · Module 53 of 100**
`█████████████░░░░░░░░░░░░` **53/100**

[Program](../../../README.md) · [Course 6](../index.md) · [Workbook](workbook.md) · [Laboratory](../../labs/module-03-sandboxed-extraction-paths/README.md) · [FrameVault guide](../capstone.md)

[← Module 52: Files, Durability, and Transactional Replacement](../module-52-files-durability-and-transactional-replacement/index.md) · [Module 54: Processes, Environments, and Standard Streams →](../module-54-processes-environments-and-standard-streams/index.md)

## The question

> How do you manipulate host paths without pretending that every operating-system name is UTF-8, every component is harmless, or every lookup remains stable?

## Why this comes now

Binary archives use portable logical names; operating systems use native path representations and resolution rules. Treating those two domains as one `String` creates corruption, traversal vulnerabilities, and platform bugs. Module 53 gives path handling its own model before process execution and FFI add more platform boundaries.

### Prerequisite bridge

Module 52 established **Files, Durability, and Transactional Replacement**. Before continuing, verify that you can preserve the previous valid file when encoding or writing fails. This module preserves that capability and adds the ability to distinguish portable logical names, `path`, `pathbuf`, `osstr`, and display text. Module 54, **Processes, Environments, and Standard Streams**, will rely on both when it asks: *How do you launch another program without turning arguments into shell syntax, leaking ambient state, deadlocking on pipes, or misreporting its result?*

### Scope boundary

This module owns the reasoning for **paths, names, and platform boundaries** inside Course 6. The course covers single-threaded systems boundaries and narrow unsafe abstractions. Threads, atomics, async I/O, networking, and production measurement are deferred so each external contract remains visible. The purpose of the boundary is to keep the decisive relationship visible before later mechanisms are layered on top of it.

## What you will be able to do

- Distinguish portable logical names, `Path`, `PathBuf`, `OsStr`, and display text.
- Validate archive-relative paths by components rather than substring tests.
- Explain why lexical checks, canonicalization, and race-free resolution solve different problems.
- Distinguish metadata that follows links from metadata about the link itself.
- Use target configuration without scattering platform assumptions through domain code.
- Document when a cross-platform implementation deliberately rejects a native name.

## Core model

### A path is not a Unicode string

Rust uses `Path` and `PathBuf` for filesystem paths and `OsStr` and `OsString` for operating-system strings. These types exist because native names are not universally UTF-8. Unix paths are byte sequences excluding NUL and separator rules; Windows paths are represented through a platform model related to wide strings and prefixes. Rust deliberately keeps the portable abstraction opaque.

`path.to_str()` returns `Option<&str>` because conversion can fail. `path.to_string_lossy()` is appropriate for human-facing display when replacement is acceptable. It is not an identity-preserving key, archive name, or round-trip serialization. Two distinct native names can produce the same lossy display.

### Separate host path from archive name

FrameVault stores a portable logical entry name as validated UTF-8 with `/` separators. A host input remains a `PathBuf`. Packing performs an explicit conversion policy:

- the selected base directory is removed structurally;
- every remaining component must be `Component::Normal`;
- every normal component must be valid UTF-8;
- components are joined with `/`;
- empty names are rejected.

Rejecting a non-UTF-8 host component is a product limitation, not proof that the host name is invalid. The archive format could instead encode platform-tagged raw names, but that would complicate portability and extraction semantics. The course chooses a smaller honest contract.

### Validate components, not textual patterns

A traversal check such as `!name.contains("..")` is wrong. It rejects harmless `report..txt`, misses platform prefix forms, and does not model separators. Parse the logical archive grammar directly. For host paths, inspect `Path::components`:

```rust
for component in candidate.components() {
    match component {
        std::path::Component::Normal(part) => { /* accept under policy */ }
        std::path::Component::CurDir => { /* reject or normalize explicitly */ }
        std::path::Component::ParentDir
        | std::path::Component::RootDir
        | std::path::Component::Prefix(_) => return Err(PathError::EscapesRoot),
    }
}
```

For archive names, do not first construct a host path and assume every platform parses `/` identically. Define the archive syntax independently: nonempty UTF-8 components, `/` separator, no empty, `.` or `..` component, no NUL, and a length limit.

### Lexical containment is not filesystem containment

Joining validated normal components beneath an extraction root prevents an archive name from directly requesting `../outside`. It does not prove that the eventual filesystem operation remains beneath the root. An existing component might be a symbolic link or Windows reparse point that redirects resolution.

`canonicalize` resolves existing links and produces an absolute path, but checking a canonicalized parent and then opening a later path still leaves a race if another actor can modify the tree between check and use. Strong hostile-directory containment requires handle-relative platform APIs, no-follow flags, or a specialized library.

FrameVault states a bounded threat model: extraction creates a fresh destination tree controlled by the current process and refuses to traverse an existing symlink component. It does not claim race-free containment in an attacker-controlled directory.

### Follow-link and no-follow metadata answer different questions

`fs::metadata` follows symbolic links. `fs::symlink_metadata` reports the final directory entry itself. A packer that intends to reject symlinks must use the latter before opening, while recognizing that a separate check and open can still race.

A directory walk should choose deliberately among regular files, directories, symbolic links, sockets, devices, and other file types. “Anything that opens” is rarely a complete archive policy. FrameVault’s first format packs regular files only and reports other types rather than silently following them.

### Canonicalization is not string cleanup

`canonicalize` queries the filesystem, resolves symbolic links, and requires the path to exist. `components` performs limited syntactic normalization but intentionally does not resolve `..` across possible symlinks. A hand-written textual normalization that removes `a/../b` can change meaning when `a` is a symlink.

Use lexical component validation for an input language such as archive names. Use canonicalization when you need the filesystem’s current resolved identity and can accept its existence and race properties. Do not substitute one for the other.

### Platform configuration should live at a boundary

Target-specific code belongs behind a small module:

```rust
#[cfg(unix)]
mod platform { /* Unix metadata or descriptor helpers */ }

#[cfg(windows)]
mod platform { /* Windows metadata or handle helpers */ }
```

The rest of the product calls a stable internal interface. This keeps `cfg` expressions from fragmenting domain logic and makes unsupported targets explicit.

Prefer `cfg(target_family = "unix")`, `cfg(windows)`, or a precise target property over guessing from architecture names. Architecture, operating system, environment, and pointer width are separate target dimensions.

### Permissions are not one portable integer

`std::fs::Permissions` exposes portable read-only control. Unix mode bits are available through `std::os::unix::fs::PermissionsExt`; Windows permissions and access control follow different concepts. Storing one Unix mode field in a “portable” archive and applying it everywhere would overstate equivalence.

FrameVault records no permissions in version 1. Extraction creates files according to the destination environment and process policy. A later format extension could carry optional platform-tagged metadata. Omitting a feature is better than pretending incompatible security models are the same.

### Display paths without changing their identity

Diagnostics should keep the owned `PathBuf` and render it at the final display boundary. `path.display()` is human-friendly and can be lossy. `Debug` rendering makes escapes more visible. Neither should be parsed back as authoritative input.

Error types should not eagerly convert paths to `String`. Preserving `PathBuf` keeps the original native identity available for programmatic handling and platform-aware formatting.

### Path operations are authorization decisions

A program that writes or deletes a path is not merely manipulating text; it is exercising authority over an external namespace. The validation policy should answer:

- Which roots are allowed?
- May the operation create parents?
- Are existing files replaceable?
- Are links followed?
- Which file types are accepted?
- What races are in scope?
- How are non-Unicode names handled?

Writing these decisions makes later unsafe or FFI code easier to audit because the namespace boundary is already explicit.

### Worked extraction algorithm

A secure-looking join is not enough. FrameVault performs extraction in stages:

```text
logical UTF-8 archive name
    ↓ parse under archive grammar
Vec<LogicalComponent>
    ↓ join beneath fresh destination root
candidate PathBuf
    ↓ verify existing ancestors are directories and not links
create missing directories one component at a time
    ↓ create final file under no-overwrite policy
write, flush, and close
```

The logical parser does not use host path parsing. It splits on `/` and rejects empty, `.` and `..` components. On Windows this also prevents archive data from injecting drive or UNC prefixes through host interpretation because the result is never accepted as one unparsed native path.

The host stage joins each validated component. Before descending through an existing component, it uses `symlink_metadata` and rejects symbolic links. The destination root is created by the current operation and is assumed not to be modified by an attacker concurrently. That assumption is written in the public extraction contract.

A stronger extractor would use directory handles and relative opens with no-follow semantics on each platform. The standard library does not expose one uniform API for that exact guarantee. Recognizing that gap is part of systems design.

### Collision policy

Archive names can collide even when their byte strings differ under a destination filesystem’s rules. Case-insensitive filesystems, Unicode normalization, reserved names, trailing spaces or dots, and platform device names create conflicts. Version 1 uses two layers:

- the archive itself rejects exact duplicate UTF-8 names;
- extraction uses `create_new(true)` and reports destination collisions rather than overwriting.

It does not claim that an archive is extractable onto every filesystem. The verifier can report structurally valid names while extraction fails under local namespace rules. This is another reason to separate format validity from operation policy.

### Path race table

| Technique | What it proves | What it does not prove |
|---|---|---|
| reject `..` components | input language has no direct parent request | existing links cannot redirect |
| `starts_with(root)` after join | lexical prefix relation | filesystem resolution containment |
| `canonicalize` then compare | current resolved relation for existing paths | stability until later open |
| `symlink_metadata` before create | observed entry type at check time | entry cannot change before use |
| handle-relative no-follow operations | stronger namespace binding | portability without target code |

The table prevents absolutist claims. Choose a row that matches the threat model and say what remains.

### Non-Unicode diagnostic discipline

Suppose a Unix input contains bytes that are not UTF-8. The packer returns:

```rust
PackError::NameNotPortable {
    path: original_path.to_path_buf(),
    component_index,
}
```

`Display` may render the path lossily for a terminal. The stored error still retains the native `PathBuf`. Tests on Unix can construct such a name through `OsStrExt`; Windows tests use the corresponding wide-string facilities for non-scalar sequences. These are target-specific tests behind `cfg`.

Never serialize `OsStr::as_encoded_bytes` as a cross-machine archive name. Its encoding is intentionally unspecified and only safe for constrained same-version, same-target reconstruction rules.

### Model checkpoint

Before the complete-program example, verify that the model can decide a design rather than merely name its mechanism.

1. **Outcome 1.** For distinguish portable logical names, `Path`, `PathBuf`, `OsStr`, and display text, construct one positive and one causal negative example. Mark the first decisive fact in the **path threat model** and state which evidence could falsify the claim.

2. **Outcome 2.** For validate archive-relative paths by components rather than substring tests, construct one positive and one causal negative example. Mark the first decisive fact in the **path threat model** and state which evidence could falsify the claim.

3. **Outcome 3.** For explain why lexical checks, canonicalization, and race-free resolution solve different problems, construct one positive and one causal negative example. Mark the first decisive fact in the **path threat model** and state which evidence could falsify the claim.

4. **Outcome 4.** For distinguish metadata that follows links from metadata about the link itself, construct one positive and one causal negative example. Mark the first decisive fact in the **path threat model** and state which evidence could falsify the claim.

5. **Preservation.** Name one earlier invariant that an easier but less precise implementation could regress.

6. **Boundary.** State one claim this module can justify and one adjacent claim that requires a later course, platform contract, peer behavior, or measurement.

A strong answer records state before and after the operation, the failure path, and the public consequence. An API name by itself is not a model.

## Use the idea in a complete program

FrameVault adds a `LogicalPath` type for archive names and a path-policy module for packing and extraction. Extraction rejects absolute forms, empty components, `.` and `..`, NUL, excessive length, and any existing symlink component in its controlled destination tree. Host-path conversion rejects non-UTF-8 components with a typed error; diagnostics preserve the original `PathBuf`.

The matching independent laboratory is [Sandboxed Extraction Paths](../../labs/module-03-sandboxed-extraction-paths/README.md). It isolates the mechanism so you can test the proof without carrying the whole capstone in your head.

## Practice sequence

Complete the [workbook](workbook.md) with host-path and logical-name cases kept in separate columns. Build the Sandboxed Extraction Paths lab and test absolute names, parent components, existing links, collisions, and race assumptions. Then review FrameVault extraction without using lexical normalization as a claim of adversarial containment.

## Ready to continue

You are ready when you can explain why a validated relative name is not by itself race-free filesystem containment, preserve non-Unicode host identities in errors, and state the exact link and destination threat model of an extraction routine.

## Primary Rust references

- [Rust standard library: Path](https://doc.rust-lang.org/std/path/struct.Path.html)
- [Rust standard library: Component](https://doc.rust-lang.org/std/path/enum.Component.html)
- [Rust standard library: OsStr](https://doc.rust-lang.org/std/ffi/struct.OsStr.html)
- [Rust standard library: symlink_metadata](https://doc.rust-lang.org/std/fs/fn.symlink_metadata.html)

## Continue

Continue to [Module 54 — Processes, Environments, and Standard Streams](../module-54-processes-environments-and-standard-streams/index.md) after completing the workbook, independent laboratory, capstone increment, and closed-book explanation for this module.
