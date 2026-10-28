# Lab — Module 05: Hostile Input and File Handling

## Objective

Process valid and hostile uploads, paths, filenames, Unicode, archives, and query controls through both tracks. Plant a decoded-traversal omission and an unbounded buffering implementation; capture escape/resource evidence and repair.


## Setup conditions

The previous baseline is: **Every operation has a policy; correct scope without ownership and ownership without permission both fail.** Run its checkpoint before changing code. Record the exact baseline command and predict how the planted defect will violate this module question: *How do valid-looking values become injection, traversal, confusion, or resource-exhaustion attacks after parsing?*

## Failure action and investigation

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

## Operational oracle

The system satisfies the chapter’s central question: How do valid-looking values become injection, traversal, confusion, or resource-exhaustion attacks after parsing? The result must be visible through public behavior or durable state, not inferred only from logs.

## Required evidence

- baseline transcript proving the previous checkpoint before **Hostile Input and File Handling** changes
- source, fixture, contract, migration, or configuration diff for this module
- focused result for: Distinguish schema validation from semantic security validation.
- public, durable, security, or operational observation showing: A shared hostile-input corpus exercises both language tracks and the artifact-storage boundary.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **semantic input and file confinement**
- a limitation statement naming every live database, network, process, telemetry backend, or operated exercise not run

## Cleanup and reset

1. Restore the control changed for **Hostile Input and File Handling**.
2. Remove synthetic data, faults, credentials, permits, files, or delivery state created by this lab.
3. Rerun the focused regression and `make module-proof MODULE=05`.
4. Confirm the system again provides this result: A shared hostile-input corpus exercises both language tracks and the artifact-storage boundary.

## Completion gate

- Distinguish schema validation from semantic security validation.
- Reject traversal after decoding and normalization.
- Treat filenames as labels, never paths.
- Bound archive and upload expansion.
- Prevent SQL, command, template, and deserialization injection.
