# Lab — Module 04: Authorization and Policy Enforcement

> **Module 04:** Authorization and Policy Enforcement

## Objective

Implement the full API 1.2 policy matrix and run cross-tenant object, list, mutation, artifact, and support-context tests. Plant one missing owner predicate in artifact retrieval and prove the shared attack vector detects it.

## Why this lab matters

This lab turns the module’s governing question—**How are scopes, roles, ownership, tenant membership, relationships, assurance, and freshness combined under default deny?**—into a falsifiable experiment. Existence concealment is a deliberate response policy. For selected tenant-owned resources, a wrong-owner request can return the same not-found problem as an absent identifier. That choice must be consistent across detail, update, artifact content, list counts, and diagnostic events. Concealment is not achieved if the status matches but latency, ETag, or error extensions reveal the foreign object.

It advances the cumulative Analysis Runs Platform by requiring this result: **Build explicit authorization decisions for collections, individual resources, fields, support access, and administration**. The result is acceptable only if the inherited contract, security, durability, reliability, and performance guarantees remain intact.

## Setup conditions

The previous baseline is: **Fixture credentials are replaced by a deterministic but realistic resource-server validation boundary.** Run its checkpoint before changing code. Record the exact baseline command and predict how the planted defect will violate this module question: *After identity is known, which exact action on which exact resource is allowed, and where is that decision enforced?*

## Hypothesis

The clean implementation should satisfy this claim: **Separate authentication from authorization; Model operation policy explicitly; Constrain collection queries before loading data; Apply field-level input and output policy; Prevent existence leaks and stale authorization decisions.** When the lab introduces this fault—**Remove or bypass the central control and prove the predicted oracle fails**—at least one part of that oracle must fail before a downstream layer can report success. After repair, the same action sequence must restore the oracle without suppressing the fault, deleting evidence, or weakening an inherited guarantee.

## Controlled action and investigation

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

### Investigation notes

Before editing code, predict the first observable divergence caused by **Remove or bypass the central control and prove the predicted oracle fails**. Record a timeline with five columns: action, authoritative state, external outcome, diagnostic evidence, and interpretation. After repair, explain which boundary owns the mechanism needed to achieve **Implement the full API 1.2 policy matrix and run cross-tenant object, list, mutation, artifact, and support-context tests. Plant one missing owner predicate in artifact retrieval and prove the shared attack vector detects it**, and identify one attractive implementation that would pass the happy path while failing the oracle.

## Operational oracle

- Separate authentication from authorization.
- Model operation policy explicitly.
- Constrain collection queries before loading data.
- Apply field-level input and output policy.
- Prevent existence leaks and stale authorization decisions.

## Required evidence

- baseline transcript proving the previous checkpoint before **Authorization and Policy Enforcement** changes
- the exact source, fixture, contract, migration, or configuration diff that implements **Authorization and Policy Enforcement**
- focused result for: Separate authentication from authorization.
- public, durable, security, or operational observation showing: Every operation has a policy; correct scope without ownership and ownership without permission both fail.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **default-deny resource authorization**
- a limitation statement naming every live dependency required to support the strongest **Authorization and Policy Enforcement** claim but not exercised

## Interpretation and defense

1. Which state or effect is authoritative for **Authorization and Policy Enforcement**, and which observations are merely diagnostic?
2. Which retained artifact proves the causal link between **Remove or bypass the central control and prove the predicted oracle fails** and the first violated part of the oracle?
3. What plausible shortcut would satisfy the clean path but fail under the controlled action?
4. How may the Python and TypeScript implementations differ internally while preserving the same external and durable result?
5. Which inherited guarantee would be lost if the mechanism were moved to a boundary that does not own the required state?

## Cleanup and reset

1. Restore the control changed for **Authorization and Policy Enforcement**.
2. Remove the temporary data, faults, credentials, permits, files, or delivery state created by the **Authorization and Policy Enforcement** experiment.
3. Rerun the focused regression and `make module-proof MODULE=04`.
4. Confirm the system again provides this result: Every operation has a policy; correct scope without ownership and ownership without permission both fail.

## Completion gate

- Separate authentication from authorization.
- Model operation policy explicitly.
- Constrain collection queries before loading data.
- Apply field-level input and output policy.
- Prevent existence leaks and stale authorization decisions.

Retain the pre-repair failure, post-repair success, causal timeline, and cleanup evidence for **Authorization and Policy Enforcement**. A green command without the negative case and causal explanation does not satisfy this gate.
