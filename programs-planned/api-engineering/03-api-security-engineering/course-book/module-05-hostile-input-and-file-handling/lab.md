# Lab — Module 05: Hostile Input and File Handling

> **Module 05:** Hostile Input and File Handling

## Objective

Process valid and hostile uploads, paths, filenames, Unicode, archives, and query controls through both tracks. Plant a decoded-traversal omission and an unbounded buffering implementation; capture escape/resource evidence and repair.

## Why this lab matters

This lab turns the module’s governing question—**How are hostile strings, numbers, paths, filenames, uploads, and serialized structures constrained at the correct boundary?**—into a falsifiable experiment. export function confinedPath(root: string, input: string, percentDecode = true): string { let decoded: string; try { decoded = percentDecode ?

It advances the cumulative Analysis Runs Platform by requiring this result: **Harden input parsing, Unicode, traversal, MIME, streaming upload, checksum, query, and error behavior**. The result is acceptable only if the inherited contract, security, durability, reliability, and performance guarantees remain intact.

## Setup conditions

The previous baseline is: **Every operation has a policy; correct scope without ownership and ownership without permission both fail.** Run its checkpoint before changing code. Record the exact baseline command and predict how the planted defect will violate this module question: *How do valid-looking values become injection, traversal, confusion, or resource-exhaustion attacks after parsing?*

## Hypothesis

The clean implementation should satisfy this claim: **Distinguish schema validation from semantic security validation; Reject traversal after decoding and normalization; Treat filenames as labels, never paths; Bound archive and upload expansion; Prevent SQL, command, template, and deserialization injection.** When the lab introduces this fault—**Remove or bypass the central control and prove the predicted oracle fails**—at least one part of that oracle must fail before a downstream layer can report success. After repair, the same action sequence must restore the oracle without suppressing the fault, deleting evidence, or weakening an inherited guarantee.

## Controlled action and investigation

1. Freeze the baseline that currently provides: A shared hostile-input corpus exercises both language tracks and the artifact-storage boundary.
2. Construct the smallest local counterexample to: How do valid-looking values become injection, traversal, confusion, or resource-exhaustion attacks after parsing?
3. Implement and test the control needed to distinguish schema validation from semantic security validation.
4. Exercise the valid boundary and at least two hostile boundaries from the shared vectors.
5. Remove or bypass the central control and prove the predicted oracle fails.
6. Restore the control and verify prevent SQL, command, template, and deserialization injection.
7. Compare the secondary track through the shared security outcome.
8. Clean runtime state and retain only the minimized regression and named evidence.

### Required planted defect

Remove or bypass the central control for **Hostile Input and File Handling** in a temporary branch. Predict the first failing check before running it, then retain the minimized reproducer as a regression after repair.

### Investigation notes

Before editing code, predict the first observable divergence caused by **Remove or bypass the central control and prove the predicted oracle fails**. Record a timeline with five columns: action, authoritative state, external outcome, diagnostic evidence, and interpretation. After repair, explain which boundary owns the mechanism needed to achieve **Process valid and hostile uploads, paths, filenames, Unicode, archives, and query controls through both tracks. Plant a decoded-traversal omission and an unbounded buffering implementation; capture escape/resource evidence and repair**, and identify one attractive implementation that would pass the happy path while failing the oracle.

## Operational oracle

- Distinguish schema validation from semantic security validation.
- Reject traversal after decoding and normalization.
- Treat filenames as labels, never paths.
- Bound archive and upload expansion.
- Prevent SQL, command, template, and deserialization injection.

## Required evidence

- baseline transcript proving the previous checkpoint before **Hostile Input and File Handling** changes
- the exact source, fixture, contract, migration, or configuration diff that implements **Hostile Input and File Handling**
- focused result for: Distinguish schema validation from semantic security validation.
- public, durable, security, or operational observation showing: A shared hostile-input corpus exercises both language tracks and the artifact-storage boundary.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **semantic input and file confinement**
- a limitation statement naming every live dependency required to support the strongest **Hostile Input and File Handling** claim but not exercised

## Interpretation and defense

1. Which state or effect is authoritative for **Hostile Input and File Handling**, and which observations are merely diagnostic?
2. Which retained artifact proves the causal link between **Remove or bypass the central control and prove the predicted oracle fails** and the first violated part of the oracle?
3. What plausible shortcut would satisfy the clean path but fail under the controlled action?
4. How may the Python and TypeScript implementations differ internally while preserving the same external and durable result?
5. Which inherited guarantee would be lost if the mechanism were moved to a boundary that does not own the required state?

## Cleanup and reset

1. Restore the control changed for **Hostile Input and File Handling**.
2. Remove the temporary data, faults, credentials, permits, files, or delivery state created by the **Hostile Input and File Handling** experiment.
3. Rerun the focused regression and `make module-proof MODULE=05`.
4. Confirm the system again provides this result: A shared hostile-input corpus exercises both language tracks and the artifact-storage boundary.

## Completion gate

- Distinguish schema validation from semantic security validation.
- Reject traversal after decoding and normalization.
- Treat filenames as labels, never paths.
- Bound archive and upload expansion.
- Prevent SQL, command, template, and deserialization injection.

Retain the pre-repair failure, post-repair success, causal timeline, and cleanup evidence for **Hostile Input and File Handling**. A green command without the negative case and causal explanation does not satisfy this gate.
