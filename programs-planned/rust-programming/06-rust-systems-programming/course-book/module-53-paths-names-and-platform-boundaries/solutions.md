# Reasoned solutions — Module 53: Paths, Names, and Platform Boundaries

[Return to the workbook](workbook.md) · [Return to the chapter](index.md) · [Open the FrameVault engineering guide](../capstone.md)

Use these solutions after freezing your own analysis. The code result matters less than locating the first broken contract and identifying who owns the repair.

Read each answer as a boundary proof: identify the missing fact, the component able to establish it, and the state that must remain unchanged when the proof fails.

## Prediction analysis

### Prediction 1

**Problem.** `to_string_lossy` is used as a hash-map key for native paths. What identity bug can occur?

**Reasoned answer.** Distinct native names can collapse to the same replacement-character string.

### Prediction 2

**Problem.** The archive rejects any name containing the substring `..`. Is that a sound component policy?

**Reasoned answer.** No. It both rejects harmless names and fails to model actual components and platform prefixes.

### Prediction 3

**Problem.** A validated name is joined beneath a root containing an attacker-controlled symlink. Is lexical containment enough?

**Reasoned answer.** No. Filesystem resolution can escape through the link.

### Prediction 4

**Problem.** `metadata` says a path is a regular file, but the directory entry is a symlink. Why?

**Reasoned answer.** `metadata` follows the link; `symlink_metadata` inspects the link entry.

### Prediction 5

**Problem.** A path is canonicalized, checked, and opened later. Can a race remain?

**Reasoned answer.** Yes. Namespace entries can change between check and use.

### Prediction 6

**Problem.** A Unix mode is restored on Windows. Is the security meaning preserved?

**Reasoned answer.** No. Permission models are not equivalent; platform-tagged metadata or an explicit omission is required.

### Prediction 7

**Problem.** A CLI prints `path.display()`. May that output be used to reconstruct the path?

**Reasoned answer.** No. Display can be lossy and is not a serialization format.

### Prediction 8

**Problem.** A directory walk relies on `read_dir` order for archive determinism. Is the order portable?

**Reasoned answer.** No. Define and apply an explicit sort policy.

## Construction guidance

### Logical grammar

Use UTF-8 components separated by `/`; reject empty, dot, dot-dot, NUL, excessive component count, and excessive total length.

### Typed validation

Do not return only “invalid path.” Preserve which component violated which rule and the original logical name.

### Threat model

A fresh process-controlled tree plus no existing symlink components supports a bounded claim; attacker-controlled concurrent mutation remains outside that claim.

### Platform module

Expose one internal function returning an enum such as `Portable`, `UnixMode(u32)`, or `Unavailable`, rather than leaking conditional types.

### Cache transfer

A stable cross-machine cache key cannot be based on an opaque native path encoding without a defined normalization and portability policy.

## Boundary-trace reference

A strong solution trace for this module must trace a portable logical archive name through lexical validation, component parsing, native path construction, ancestor inspection, directory creation, final exclusive creation, and later filesystem resolution. Keep the portable name, display text, and native path as separate columns. It should reveal the earliest point at which an invalid assumption would become observable and the unique owner responsible for cleanup or rollback.

## Weak repairs to reject

Reject solutions built around these shortcuts:

- converting every `Path` to UTF-8 and using the string as identity;
- rejecting traversal with substring searches;
- removing `..` components instead of rejecting them;
- checking containment once and claiming race-proof confinement;
- following existing symlink ancestors;
- silently overwriting an existing destination;

A principled repair makes the missing fact explicit in a type, checked operation, state transition, safety contract, platform qualification, or foreign-call contract. It does not merely move the assumption to a less visible line.

## Name-to-path proof table

| Layer | Representation | Allowed claim |
|---|---|---|
| archive identity | validated relative components separated by `/` | portable logical name under the format grammar |
| host mapping | `PathBuf` assembled component by component | intended destination path on this host |
| preflight inspection | metadata without following final symlink where available | observed ancestor types at one instant |
| file creation | exclusive open of the intended final path | this call created a new file at the resolved pathname |
| adversarial containment | directory-handle-relative operations and platform support | resistance to pathname races, only when actually implemented |

A lexical `starts_with` check after joining paths proves far less than it appears to prove. It does not prevent a symlink ancestor from redirecting resolution, does not address case-folding collisions, and may compare paths that have not been normalized under the same policy.

## Collision and identity clinic

Reject empty, `.`, and `..` components before host conversion. Reject backslashes and drive/scheme markers when `/` is the only archive separator. Decide whether Unicode normalization and case folding are part of the archive identity; if they are not, two names may still collide on a particular host and extraction must detect that host-specific conflict.

The course implementation deliberately claims safe extraction into a non-adversarial destination after symlink/ancestor preflight. It does not claim race-proof sandboxing. That stronger product would need directory handles, no-follow operations, and platform-specific APIs that remain outside this standard-library course boundary.

## Completion check

Use the chapter’s readiness statement as the first threshold:

You are ready when you can explain why a validated relative name is not by itself race-free filesystem containment, preserve non-Unicode host identities in errors, and state the exact link and destination threat model of an extraction routine.

Then perform this destructive regression check: replace component validation with a string-prefix check and show which traversal, separator, or drive-prefix fixture now passes incorrectly. The resulting failure should be caught for the causal reason predicted in the workbook, not by an unrelated panic or syntax error.
