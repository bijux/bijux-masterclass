# Workbook — Module 53: Paths, Names, and Platform Boundaries

[Chapter](index.md) · [Laboratory](../../labs/module-03-sandboxed-extraction-paths/README.md) · [FrameVault guide](../capstone.md) · [Solutions](solutions.md)

This workbook tests whether **Paths, Names, and Platform Boundaries** has become a usable model rather than remembered vocabulary. Its governing question is: *How do you manipulate host paths without pretending that every operating-system name is UTF-8, every component is harmless, or every lookup remains stable?* Preserve your first prediction and record decisive facts in a **path threat model**. A repair succeeds only when it keeps the difficult product requirement visible.

## Retrieval warm-up

Before compiling or running anything:

1. Restate the invariant from Module 52 — Files, Durability, and Transactional Replacement that today’s mechanism must preserve.
2. Rewrite the governing question in your own words: **How do you manipulate host paths without pretending that every operating-system name is UTF-8, every component is harmless, or every lookup remains stable?**
3. Draw the smallest **path threat model** that could decide one positive and one negative case.
4. Name one shortcut that could make the visible example pass while deleting ownership, failure, ordering, capacity, safety, compatibility, or evidence required by the product.

## Part 1 — Predict

### Prediction 1

`to_string_lossy` is used as a hash-map key for native paths. What identity bug can occur?

Record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 2

The archive rejects any name containing the substring `..`. Is that a sound component policy?

For **Prediction 2**, record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 3

A validated name is joined beneath a root containing an attacker-controlled symlink. Is lexical containment enough?

For **Prediction 3**, record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 4

`metadata` says a path is a regular file, but the directory entry is a symlink. Why?

For **Prediction 4**, record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 5

A path is canonicalized, checked, and opened later. Can a race remain?

For **Prediction 5**, record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 6

A Unix mode is restored on Windows. Is the security meaning preserved?

For **Prediction 6**, record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 7

A CLI prints `path.display()`. May that output be used to reconstruct the path?

For **Prediction 7**, record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 8

A directory walk relies on `read_dir` order for archive determinism. Is the order portable?

For **Prediction 8**, record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

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

### Interleaved reasoning pass

1. For **Distinguish portable logical names, `Path`, `PathBuf`, `OsStr`, and display text**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the path threat model.
2. For **Validate archive-relative paths by components rather than substring tests**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the path threat model.
3. For **Explain why lexical checks, canonicalization, and race-free resolution solve different problems**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the path threat model.
4. For **Distinguish metadata that follows links from metadata about the link itself**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the path threat model.

5. Identify one guarantee from an earlier course that a careless implementation of **Paths, Names, and Platform Boundaries** could regress.

For one case, write both a principled repair and a weaker repair that appears to work. The principled repair must preserve the requirement; the weaker repair must name the information, state, bound, or compatibility promise it silently discards.

## Part 4 — Independent laboratory

Build [Sandboxed Extraction Paths](../../labs/module-03-sandboxed-extraction-paths/README.md) from the starter. Freeze the public boundary and adversarial cases before opening the solution. Produce the evidence required by the lab:

- a table separating logical-name rules from host-path observations;
- tests for absolute forms, parent and current components, empty components, backslashes, drive markers, and control characters;
- tests for existing files, existing symlink ancestors, and non-directory ancestors;
- a step-by-step creation trace for one nested destination;
- an explicit statement of the remaining time-of-check/time-of-use race.

Also identify one feature deliberately excluded because it would enlarge the trust, portability, concurrency, or unsafe proof surface.

### Laboratory acceptance trace

Before opening the reference implementation for **Sandboxed Extraction Paths**, record:

- the public behavior that demonstrates **Distinguish portable logical names, `Path`, `PathBuf`, `OsStr`, and display text**;
- one adversarial input, state transition, schedule, peer action, workload, or build condition appropriate to this module;
- the exact state after rejection or partial failure;
- ownership and cleanup;
- ordering and capacity;
- one shortcut deliberately excluded by the contract;
- one claim the tests cannot establish.

## Part 5 — Capstone transfer

Implement the matching increment from the [capstone engineering guide](../capstone.md). Add one regression test that fails if this module’s central contract is removed.

### Capstone invariant trace

For the Module 53 FrameVault increment, name the changed invariant and its owner before editing code. Follow it through input, validation, state transition, effect, output, failure, cleanup, and tests. Add storage, wire, scheduler, generated-code, compatibility, resource, or measurement consequences when this course makes them relevant. End by naming one earlier guarantee that remains unchanged.

## Part 6 — Reconstruct and defend

Answer these questions without the chapter:

1. Which rules define the portable logical-name language?
2. Which facts can component validation establish without filesystem access?
3. Which facts can pathname preflight observe but not freeze?
4. What stronger operating-system primitive would be needed against an adversarial race?

End by naming the strongest honest claim after success and one claim the implementation deliberately does not make.

### Independent transfer

Define a portable package name with segments separated by `/`, then map it below a host root. Include cases for empty text, absolute syntax, drive-like prefixes, backslashes, `.` and `..`, repeated separators, NUL, and non-ASCII names. Add a symlink-ancestor test on targets that support symlinks. Write two threat models: one for accidental/malicious archive names without concurrent mutation, and one for a hostile local process racing the extraction. Explain why the same implementation does not satisfy both.

### Closed-book defense

In five minutes, answer “How do you manipulate host paths without pretending that every operating-system name is UTF-8, every component is harmless, or every lookup remains stable?” using the **path threat model**. Include one positive case, one causal negative case, one principled repair, one rejected shortcut, and one transfer outside FrameVault. A list of APIs without the deciding relationship is incomplete.
