# Checkpoint — Module 04: Authorization and Policy Enforcement

## Required result

Build explicit authorization decisions for collections, individual resources, fields, support access, and administration.

## Demonstrate

- Separate authentication from authorization.
- Model operation policy explicitly.
- Constrain collection queries before loading data.
- Apply field-level input and output policy.
- Prevent existence leaks and stale authorization decisions.

## Commands

```bash
make module-proof MODULE=04 TRACK=python
make module-proof MODULE=04 TRACK=typescript
make core-proof
```

## Evidence to retain

- baseline transcript proving the previous checkpoint before **Authorization and Policy Enforcement** changes
- the exact source, fixture, contract, migration, or configuration diff that implements **Authorization and Policy Enforcement**
- focused result for: Separate authentication from authorization.
- public, durable, security, or operational observation showing: Every operation has a policy; correct scope without ownership and ownership without permission both fail.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **default-deny resource authorization**
- a limitation statement naming every live dependency required to support the strongest **Authorization and Policy Enforcement** claim but not exercised

## Defend the design

1. Answer the central question: **After identity is known, which exact action on which exact resource is allowed, and where is that decision enforced?**
2. Demonstrate this capstone result: Every operation has a policy; correct scope without ownership and ownership without permission both fail.
3. Show the **Authorization and Policy Enforcement** defect, the first failing oracle, and the exact regression retained after repair.
4. Explain why this invariant is shared across languages: scope, role, tenant, relationship, assurance, freshness, and concealment are evaluated for the exact operation and resource.
5. State which environment-backed **Authorization and Policy Enforcement** route was not run and how that limits the claim.

## Continue only when

Continue when the system again provides this module result—Every operation has a policy; correct scope without ownership and ownership without permission both fail.—all focused checks pass, the **Authorization and Policy Enforcement** planted defect has failed for the predicted reason, and the record identifies every live claim not executed in the current environment.
