# Module 45 — Files, File Handles, Paths, and Transactional Replacement

**Progress: 45/100**

## The governing question

> What does it mean for a file operation to be complete, visible, replaced, durable, and safely owned in a Node.js process?

## Why this module comes now

Modules 41–44 built byte and stream reasoning. Files add a pathname namespace, open-handle lifetime, metadata races, partial writes, replacement policy, and durability distinctions. A successful stream into a file is only one stage of a product-level commit.

The previous modules owned in-memory flow and stream termination. Files add a namespace, a kernel resource, and a visibility transition. A successful write to a file descriptor is not the same event as publishing a new pathname, and publication is not the same claim as surviving every crash model. Course 1’s persistence discipline returns here at a lower and more precise layer.

The module treats “save” as an imprecise word. Every design must name candidate creation, write completion, synchronization, close, replacement, and post-publication reporting separately.

## Observable outcomes

By the end of this module, you can:

- choose among whole-file helpers, FileHandle operations, and file streams based on size and lifecycle

- own open handles and close them on every terminal path

- distinguish pathname identity, open-file identity, visibility, replacement, flush, synchronization, and durability

- implement same-directory staged replacement with explicit cleanup and overwrite policy

- state platform and adversarial-race limitations honestly

## The module ledger

Use this ledger while reading examples and before writing the laboratory design. It is deliberately specific to this module.

| Dimension | Question to answer |
|---|---|
| namespace | Which pathname is looked up, created, replaced, or removed? |
| open identity | Which `FileHandle` or stream owns the opened file object? |
| candidate state | Where are incomplete bytes kept before publication? |
| overwrite policy | Must an existing destination be preserved, rejected, or replaced? |
| publication point | Which rename or manifest update makes the candidate visible? |
| durability claim | What does synchronization establish in the intended filesystem environment? |

## Pathnames and open files are different identities

A pathname is a lookup route in a filesystem namespace. Opening it yields a handle to an object that can remain valid even if the pathname is renamed or removed, depending on the platform. Rechecking metadata by pathname after opening can describe a different object. When identity matters, perform the operation through the owned FileHandle and avoid treating repeated path lookups as one atomic fact.

Node path values may be strings, Buffers, or URL objects in selected APIs. Converting native paths to UTF-8 strings can lose information on some systems. Course 5 uses ordinary project paths but keeps the distinction visible so later security and server courses can define stricter boundaries.

## Whole-file helpers trade simplicity for retention

readFile and writeFile are excellent when product limits guarantee the complete value fits comfortably in memory. They are not morally inferior to streams. The correct choice follows the size contract, not fashion. A whole-file helper can simplify atomic validation and error handling; a stream is justified when input may exceed the desired retained-memory bound or when processing should begin before the entire value arrives.

Always state the maximum file size accepted by a whole-file operation. Without that limit, the API quietly converts external file size into process memory demand.

## File completion has layers

A write callback or writable finish means Node accepted the bytes through the file descriptor. FileHandle.sync asks the operating system to synchronize file data and metadata required for retrieval. Renaming a staged file changes pathname visibility. Synchronizing the parent directory is a further durability step on systems where directory entries require it. These operations have different failure points and should not be compressed into “saved”.

Most application code cannot promise survival across every crash, filesystem, network mount, or power-loss model. State the intended environment and claim. Same-directory stage, sync, close, and rename gives a much stronger replacement protocol than direct overwrite, but cross-process coordination and hostile directory races remain separate concerns.

## Staged replacement preserves the previous visible candidate

The usual single-writer pattern creates a unique temporary file beside the destination, writes and validates the complete candidate, flushes and synchronizes it, closes it, then renames it over or into the final path according to policy. Before rename, the old destination remains visible. On failure, remove the stage. After rename, a later error must be reported as post-commit because rolling back may be unsafe or impossible.

Temporary naming must avoid collisions and accidental following of an existing path. Exclusive creation with a randomized or process-specific name is better than opening a predictable shared name. Permissions and ownership policy must also be deliberate.

## File streams do not remove handle ownership

createReadStream and createWriteStream can own the file descriptor they open, or they can be constructed around an existing descriptor or FileHandle. The autoClose and emitClose choices affect who releases the resource. Mixing a manually owned FileHandle with a stream that also closes it creates double-ownership ambiguity.

The function that opens a handle should normally close it in a finally block unless ownership is explicitly transferred. A public API that returns a stream over an open file must document whether destroying or ending the stream closes the file and what the caller must do after early stop.

## Pathnames are lookups, not stable resource identities

Opening a path obtains a handle to the resolved filesystem object. Repeating a path check later can observe a different object if the namespace changed. This is why “check then open” is not an authorization protocol and why operations that depend on one file identity should remain on the acquired handle where possible.

For this course, staged output is created in the destination directory with exclusive creation. That avoids cross-device rename and predictable temporary-name collisions. It does not solve hostile directory replacement, symlink races, or multi-writer coordination; those belong to an explicit threat model rather than optimistic wording.

## Completion, visibility, and durability form separate layers

A writable’s `finish` says that its accepted chunks have been handed through the writable implementation. Closing releases the descriptor. `FileHandle.sync()` requests synchronization of file contents and metadata required for retrieval. Rename changes namespace visibility. Depending on the platform and durability goal, synchronizing the parent directory may be another step.

An API should return a result that names the strongest completed layer. If rename succeeded but a later directory synchronization failed, reporting “nothing was saved” is false; reporting unqualified success may also be too strong. Typed pre-commit and post-commit errors preserve that distinction.

## Transactional replacement is a protocol, not a helper name

A single-path staged replacement can preserve the prior visible file until the candidate is complete. It cannot automatically make several output files appear atomically, coordinate independent processes, or roll back a publication after the new pathname becomes visible. Those stronger requirements need version directories, a committed manifest, locking, or another store.

The protocol’s usefulness comes from its explicit failure matrix. Before rename, cleanup can remove the stage and the old destination remains authoritative. At rename, visibility changes. After rename, failures are recovery or durability concerns rather than safe rollback opportunities.

## Worked case — Staged text replacement

```ts
import { open, rename, rm } from 'node:fs/promises';
import { dirname, join, basename } from 'node:path';
import { randomUUID } from 'node:crypto';

export async function replaceText(path: string, text: string): Promise<void> {
  const stage = join(dirname(path), `.${basename(path)}.${randomUUID()}.tmp`);
  let committed = false;
  try {
    const handle = await open(stage, 'wx', 0o600);
    try {
      await handle.writeFile(text, { encoding: 'utf8' });
      await handle.sync();
    } finally {
      await handle.close();
    }
    await rename(stage, path);
    committed = true;
  } finally {
    if (!committed) await rm(stage, { force: true });
  }
}
```

The candidate is complete and synchronized before rename. The stage is in the destination directory, avoiding cross-device rename. The code does not claim that parent-directory metadata is durable, does not coordinate multiple writers, and inherits platform-specific overwrite semantics. Those are not defects hidden by the helper; they are explicit boundaries for a later product policy.

## Extended case analysis

Suppose normalization writes directly to `events.ndjson` and fails on record 900. The old valid file has already been truncated and the new file contains a prefix. Staging redirects partial work to a private candidate; record 900 can fail without changing the visible destination. The rename does not make parsing safer—it moves the visibility boundary until after parsing, transformation, and file completion have all succeeded.

## What this mechanism establishes

A correct implementation establishes these local facts:

- The final path is not opened for truncating write.

- The stage is created exclusively in the destination directory.

- The candidate stream completes and the file is synchronized before rename.

It does **not** establish the stronger claims hidden by these shortcuts:

- writing directly to the destination;

- using a predictable shared temporary name;

Those distinctions are part of the public contract. Later modules may add stronger guarantees, but they must not be backdated into this mechanism.

## Decision procedure

1. State the maximum input or output size and choose whole-file or streaming I/O accordingly.

2. Name the scope that owns each FileHandle or file stream.

3. Separate candidate completion, synchronization, visibility, and durability claims.

4. Choose no-overwrite, replace-existing, or versioned-output policy explicitly.

5. Place the stage beside the destination and create it exclusively.

6. Test failure before write, during write, during sync, before rename, and after rename.

Make each answer visible in an API, graph, or test. Labels such as “streaming,” “safe,” and “atomic” are incomplete until representation, owner, bound, and terminal evidence are named.

## Common wrong models

### Writing directly to the destination

A crash or transform error can expose a truncated or semantically invalid file.

### Calling access before open as authorization

The namespace can change between checks and use; open errors remain authoritative.

### Closing both FileHandle and stream without an ownership plan

Resource release becomes duplicated and errors are easily lost.

### Calling the operation durable after rename alone

Directory-entry durability and filesystem behavior require a narrower claim.

## Apply the mechanism in FlowLedger

Build FlowLedger’s staged output owner. The final pathname must change only after the entire stream pipeline succeeds and the candidate file is synchronized and closed.

Before editing FlowLedger, record the changed edge, owner, bound, and success observation. Update implementation, errors, tests, documentation, and report as one feature.

## Independent transfer

Design a checkpoint writer for a long-running import. Decide whether checkpoints replace one file, append immutable versions, or update a directory manifest, and state the crash-recovery evidence for the choice.

The transfer is successful when the new design preserves the module’s governing relationship without copying the laboratory’s domain names or relying on its exact data shape.

## Practice sequence

1. Reconstruct the module ledger from memory.
2. Read the worked case and mark every copy, view, queue, wait, and terminal observation.
3. Predict all eight Module 45 investigations before running them.
4. Complete the workbook’s diagnosis section without broad assertions or whole-input shortcuts.
5. Build **Transactional File Sink** from the starter package.
6. Compare only after your adversarial tests pass, beginning with the first different design decision.
7. Transfer the mechanism into FlowLedger and explain one earlier-course invariant that could regress.

## Readiness standard

Continue only when you can:

- Choose among whole-file helpers, FileHandle operations, and file streams based on size and lifecycle

- Own open handles and close them on every terminal path

- Distinguish pathname identity, open-file identity, visibility, replacement, flush, synchronization, and durability

- Implement same-directory staged replacement with explicit cleanup and overwrite policy

- State platform and adversarial-race limitations honestly
- explain which observation is necessary but insufficient for product completion;
- state one capacity or durability guarantee this module deliberately does not make;
- defend the laboratory’s failure path without reading the reference source.

## Primary references

- [https://nodejs.org/docs/latest-v24.x/api/fs.html](https://nodejs.org/docs/latest-v24.x/api/fs.html)
- [https://nodejs.org/docs/latest-v24.x/api/path.html](https://nodejs.org/docs/latest-v24.x/api/path.html)

The chapter is self-contained. These links are primary-source routes for checking version-sensitive Node.js details.

## Continue

- [Workbook](workbook.md)
- [Reasoned solutions](solutions.md)
- [Laboratory brief](../../labs/module-45-transactional-file-sink/README.md)
- [FlowLedger engineering guide](../capstone.md)
