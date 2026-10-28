# Lab — Module 09: Evolution, Compatibility, and Audience Views

## Objective

Publish a reproducible v1.1, prove an attempted breaking v1.2 is blocked for three independent reasons, and permit v2.0 only with explicit migration evidence; derive and verify public/partner Overlay views.

## Setup conditions

The previous baseline is: **Every operation has an explicit security decision and cross-owner artifact access is rejected.** Run its checkpoint before changing code. Record the exact baseline command and predict how the planted defect will violate this module question: *How can a published API change without silently breaking existing consumers?*

## Failure action and investigation

1. Freeze v1.0 and v1.1 bundled contracts with deterministic digests, changelog entries, and pinned tool metadata.
2. Classify the provided change-case matrix in both provider-request and consumer-response directions before running tools.
3. Run the built-in comparator and oasdiff where available against the intentionally breaking v1.2 fixture; require all planted defects.
4. Regenerate representative Python and TypeScript client snapshots for v1.1 and the attempted candidate to expose source changes.
5. Create v2.0 with intentional removal, an approval marker, affected-operation inventory, and executable migration example.
6. Apply public and partner Overlay 1.1 documents in order and assert expected and forbidden operation sets.
7. Produce one CI report containing baseline/candidate digests, machine classifications, reviewer decisions, limitations, and release outcome.

### Required planted defect

Choose one defect from Failure Modes. Before fixing it, keep:

```text
defect:
predicted first failing gate:
actual first failing gate:
minimal request/instance/diff:
root cause:
repair:
permanent regression location:
```

## Operational oracle

The system satisfies the chapter’s central question: How can a published API change without silently breaking existing consumers? The result must be visible through public behavior or durable state, not inferred only from logs.

## Required evidence

- baseline transcript proving the previous checkpoint before **Evolution, Compatibility, and Audience Views** changes
- source, fixture, contract, migration, or configuration diff for this module
- focused result for: Analyze compatibility in the correct message direction.
- public, durable, security, or operational observation showing: API 1.1 is released, a breaking candidate is rejected, and public/partner views are derived from the canonical contract.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **Evolution, Compatibility, and Audience Views**
- a limitation statement naming every live database, network, process, telemetry backend, or operated exercise not run

## Cleanup and reset

1. Restore the control changed for **Evolution, Compatibility, and Audience Views**.
2. Remove synthetic data, faults, credentials, permits, files, or delivery state created by this lab.
3. Rerun the focused regression and `make module-proof MODULE=09`.
4. Confirm the system again provides this result: API 1.1 is released, a breaking candidate is rejected, and public/partner views are derived from the canonical contract.

## Completion gate

- v1.1 is classified non-breaking under stated policy
- attempted v1.2 fails for all planted defects
- v2.0 needs migration and approval evidence
- release bundles reproduce exact digests
- public/partner views exclude forbidden operations
- every suppression is exact and justified
