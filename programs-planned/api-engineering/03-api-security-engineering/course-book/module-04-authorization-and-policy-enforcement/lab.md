# Lab — Module 04: Authorization and Policy Enforcement

## Objective

Implement the full API 1.2 policy matrix and run cross-tenant object, list, mutation, artifact, and support-context tests. Plant one missing owner predicate in artifact retrieval and prove the shared attack vector detects it.


## Setup conditions

The previous baseline is: **Fixture credentials are replaced by a deterministic but realistic resource-server validation boundary.** Run its checkpoint before changing code. Record the exact baseline command and predict how the planted defect will violate this module question: *After identity is known, which exact action on which exact resource is allowed, and where is that decision enforced?*

## Failure action and investigation

1. Freeze the baseline that currently provides: Every operation has a policy; correct scope without ownership and ownership without permission both fail.
2. Construct the smallest local counterexample to: After identity is known, which exact action on which exact resource is allowed, and where is that decision enforced?
3. Implement and test the control needed to separate authentication from authorization.
4. Exercise the valid boundary and at least two hostile boundaries from the shared vectors.
5. Remove or bypass the central control and prove the predicted oracle fails.
6. Restore the control and verify prevent existence leaks and stale authorization decisions.
7. Compare the secondary track through the shared security outcome.
8. Clean runtime state and retain only the minimized regression and named evidence.

### Required planted defect

Remove or bypass the central control for **Authorization and Policy Enforcement** in a temporary branch. Predict the first failing check before running it, then retain the minimized reproducer as a regression after repair.

## Operational oracle

The system satisfies the chapter’s central question: After identity is known, which exact action on which exact resource is allowed, and where is that decision enforced? The result must be visible through public behavior or durable state, not inferred only from logs.

## Required evidence

- baseline transcript proving the previous checkpoint before **Authorization and Policy Enforcement** changes
- source, fixture, contract, migration, or configuration diff for this module
- focused result for: Separate authentication from authorization.
- public, durable, security, or operational observation showing: Every operation has a policy; correct scope without ownership and ownership without permission both fail.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **default-deny resource authorization**
- a limitation statement naming every live database, network, process, telemetry backend, or operated exercise not run

## Cleanup and reset

1. Restore the control changed for **Authorization and Policy Enforcement**.
2. Remove synthetic data, faults, credentials, permits, files, or delivery state created by this lab.
3. Rerun the focused regression and `make module-proof MODULE=04`.
4. Confirm the system again provides this result: Every operation has a policy; correct scope without ownership and ownership without permission both fail.

## Completion gate

- Separate authentication from authorization.
- Model operation policy explicitly.
- Constrain collection queries before loading data.
- Apply field-level input and output policy.
- Prevent existence leaks and stale authorization decisions.
