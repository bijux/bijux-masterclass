# Checkpoint — Module 05: Hostile Input and File Handling

## Required result

Harden input parsing, Unicode, traversal, MIME, streaming upload, checksum, query, and error behavior.

## Demonstrate

- Distinguish schema validation from semantic security validation.
- Reject traversal after decoding and normalization.
- Treat filenames as labels, never paths.
- Bound archive and upload expansion.
- Prevent SQL, command, template, and deserialization injection.

## Commands

```bash
make module-proof MODULE=05 TRACK=python
make module-proof MODULE=05 TRACK=typescript
make core-proof
```

## Evidence to retain

- baseline transcript proving the previous checkpoint before **Hostile Input and File Handling** changes
- the exact source, fixture, contract, migration, or configuration diff that implements **Hostile Input and File Handling**
- focused result for: Distinguish schema validation from semantic security validation.
- public, durable, security, or operational observation showing: A shared hostile-input corpus exercises both language tracks and the artifact-storage boundary.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **semantic input and file confinement**
- a limitation statement naming every live dependency required to support the strongest **Hostile Input and File Handling** claim but not exercised

## Defend the design

1. Answer the central question: **How do valid-looking values become injection, traversal, confusion, or resource-exhaustion attacks after parsing?**
2. Demonstrate this capstone result: A shared hostile-input corpus exercises both language tracks and the artifact-storage boundary.
3. Show the **Hostile Input and File Handling** defect, the first failing oracle, and the exact regression retained after repair.
4. Explain why this invariant is shared across languages: decoding, normalization, path resolution, symlink policy, byte budgets, and archive budgets are applied in the correct order.
5. State which environment-backed **Hostile Input and File Handling** route was not run and how that limits the claim.

## Continue only when

Continue when the system again provides this module result—A shared hostile-input corpus exercises both language tracks and the artifact-storage boundary.—all focused checks pass, the **Hostile Input and File Handling** planted defect has failed for the predicted reason, and the record identifies every live claim not executed in the current environment.
