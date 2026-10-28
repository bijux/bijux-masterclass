# Checkpoint — Module 05: Hostile Input and File Handling

## Required result

A shared hostile-input corpus exercises both language tracks and the artifact-storage boundary.

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

## Defend the design

1. Answer the central question: **How do valid-looking values become injection, traversal, confusion, or resource-exhaustion attacks after parsing?**
2. Demonstrate this capstone result: A shared hostile-input corpus exercises both language tracks and the artifact-storage boundary.
3. Show the planted defect, the first failing oracle, and the retained regression.
4. Explain why this invariant is shared across languages: decoding, normalization, path resolution, symlink policy, byte budgets, and archive budgets are applied in the correct order.
5. State exactly which database, network, process, telemetry backend, or operated exercise was not run in the current environment.

## Continue only when

Continue when the system again provides this module result—A shared hostile-input corpus exercises both language tracks and the artifact-storage boundary.—all focused checks pass, the **Hostile Input and File Handling** planted defect has failed for the predicted reason, and the record identifies every live claim not executed in the current environment.
