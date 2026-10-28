# Reasoned Solutions — Module 53: Paths, Names, and Platform Boundaries

[Workbook](workbook.md) · [Chapter](index.md) · [Laboratory](../../labs/module-03-sandboxed-extraction-paths/README.md) · [FrameVault guide](../capstone.md)

Use these notes only after preserving your prediction and repair for **Module 53: Paths, Names, and Platform Boundaries**. Compare the reasoning against this question: *How do you manipulate host paths without pretending that every operating-system name is UTF-8, every component is harmless, or every lookup remains stable?* Do not compare line count first. A different implementation is valid when it preserves the same public contract and can defend its ownership, failure, ordering, capacity, safety, compatibility, and evidence consequences.

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

## Deep reasoning and transfer

### Decisive model

> How do you manipulate host paths without pretending that every operating-system name is UTF-8, every component is harmless, or every lookup remains stable?

Build a **path threat model**. Mark the owner or authority, valid and invalid states, first decisive phase or event, state after failure, and visible consequence. The model is too weak when it records only the API call and not the relationship that makes the call legal or useful.

### Outcome checks

1. **Distinguish portable logical names, `Path`, `PathBuf`, `OsStr`, and display text.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
2. **Validate archive-relative paths by components rather than substring tests.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
3. **Explain why lexical checks, canonicalization, and race-free resolution solve different problems.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
4. **Distinguish metadata that follows links from metadata about the link itself.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
5. **Use target configuration without scattering platform assumptions through domain code.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.

### Repair discipline

The weak repair for this module is any change that makes the current example pass by deleting the first outcome: **Distinguish portable logical names, `Path`, `PathBuf`, `OsStr`, and display text.** A principled repair preserves that requirement, narrows the unsupported assumption, and makes the deciding fact observable in the path threat model.

### Reference implementation comparison

For [Sandboxed Extraction Paths](../../labs/module-03-sandboxed-extraction-paths/README.md), compare contract, state transitions, adversarial cases, cleanup, and public behavior before syntax. Identify the earliest operation that could violate the contract and the type, check, protocol, or review procedure that prevents it. Then state when a simpler design would be preferable.

### Capstone transfer

In FrameVault, Module 53 is complete only when the new behavior fits the existing authority map. Trace the changed fact from input through validation, state transition, effect, output, and tests. Two components deciding the same fact indicate a second source of truth rather than successful integration.

### Oral defense

Answer these without notes:

1. In **Paths, Names, and Platform Boundaries**, which relationship decides this question: “How do you manipulate host paths without pretending that every operating-system name is UTF-8, every component is harmless, or every lookup remains stable?”
2. What is the smallest causal negative case?
3. Which repair preserves the requirement?
4. Which tempting repair deletes it?
5. What can the chosen evidence falsify, and what remains unproved?
6. How would the design change in a product unrelated to FrameVault?
