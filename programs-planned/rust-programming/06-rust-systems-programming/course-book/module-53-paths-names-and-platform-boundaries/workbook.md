# Workbook — Module 53: Paths, Names, and Platform Boundaries

[Return to the chapter](index.md) · [Open the FrameVault engineering guide](../capstone.md) · [Open solutions only after attempting the work](solutions.md)

This workbook tests whether the chapter has become an operational model. Freeze answers before compiling or reading the reference implementation. A correct result without the governing reason is incomplete.

## Part 1 — Predict

### Prediction 1

`to_string_lossy` is used as a hash-map key for native paths. What identity bug can occur?

Record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 2

The archive rejects any name containing the substring `..`. Is that a sound component policy?

Record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 3

A validated name is joined beneath a root containing an attacker-controlled symlink. Is lexical containment enough?

Record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 4

`metadata` says a path is a regular file, but the directory entry is a symlink. Why?

Record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 5

A path is canonicalized, checked, and opened later. Can a race remain?

Record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 6

A Unix mode is restored on Windows. Is the security meaning preserved?

Record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 7

A CLI prints `path.display()`. May that output be used to reconstruct the path?

Record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 8

A directory walk relies on `read_dir` order for archive determinism. Is the order portable?

Record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

## Part 2 — Diagnose and repair

### Boundary trace

Trace a portable logical archive name through lexical validation, component parsing, native path construction, ancestor inspection, directory creation, final exclusive creation, and later filesystem resolution. Keep the portable name, display text, and native path as separate columns.

For **Paths, Names, and Platform Boundaries**, choose table columns that expose the actual states rather than copying a generic checklist. Every row must name the owner, the fact established, the fact still delegated, the visible failure effect, and the component responsible for cleanup or rollback.

### Weak repairs to reject

For each prediction, identify a superficially convenient repair that violates the module contract. Reject at least these module-specific shortcuts:

- converting every `Path` to UTF-8 and using the string as identity;
- rejecting traversal with substring searches;
- removing `..` components instead of rejecting them;
- checking containment once and claiming race-proof confinement;
- following existing symlink ancestors;
- silently overwriting an existing destination;

Replace each with the smallest repair that preserves the requirement and state what evidence would distinguish the two designs.

## Part 3 — Focused exercises

### Construction 1

Specify a portable logical-name grammar independent of host `Path` parsing.

Required evidence: Include separators, components, encoding, forbidden values, and limits.

### Construction 2

Implement component-based validation for extraction names.

Required evidence: Return a typed reason for root, prefix, parent, current, empty, or invalid component.

### Construction 3

Write the threat model for extracting into a newly created tree.

Required evidence: State assumptions about concurrent modification and symlinks.

### Construction 4

Design a platform module for recording one optional metadata fact.

Required evidence: Keep `cfg` at the boundary and make unsupported behavior explicit.

### Construction 5

Transfer the method to a cache key derived from a host path.

Required evidence: Decide whether native identity, canonical identity, or portable display is actually required.

## Part 4 — Independent laboratory

Build [Sandboxed Extraction Paths](../../labs/module-03-sandboxed-extraction-paths/README.md) from the starter. Freeze the public boundary and adversarial cases before opening the solution. Produce the evidence required by the lab:

- a table separating logical-name rules from host-path observations;
- tests for absolute forms, parent and current components, empty components, backslashes, drive markers, and control characters;
- tests for existing files, existing symlink ancestors, and non-directory ancestors;
- a step-by-step creation trace for one nested destination;
- an explicit statement of the remaining time-of-check/time-of-use race.

Also identify one feature deliberately excluded because it would enlarge the trust, portability, concurrency, or unsafe proof surface.

## Part 5 — Capstone transfer

Implement the matching increment from the [capstone engineering guide](../capstone.md). Add one regression test that fails if this module’s central contract is removed.

## Part 6 — Reconstruct and defend

Answer these questions without the chapter:

1. Which rules define the portable logical-name language?
2. Which facts can component validation establish without filesystem access?
3. Which facts can pathname preflight observe but not freeze?
4. What stronger operating-system primitive would be needed against an adversarial race?

End by naming the strongest honest claim after success and one claim the implementation deliberately does not make.

### Independent transfer

Define a portable package name with segments separated by `/`, then map it below a host root. Include cases for empty text, absolute syntax, drive-like prefixes, backslashes, `.` and `..`, repeated separators, NUL, and non-ASCII names. Add a symlink-ancestor test on targets that support symlinks. Write two threat models: one for accidental/malicious archive names without concurrent mutation, and one for a hostile local process racing the extraction. Explain why the same implementation does not satisfy both.
