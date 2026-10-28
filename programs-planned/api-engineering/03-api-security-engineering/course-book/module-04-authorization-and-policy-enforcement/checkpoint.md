# Checkpoint — Module 04: Authorization and Policy Enforcement

## Required result

Every operation has a policy; correct scope without ownership and ownership without permission both fail.

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

## Defend the design

1. Answer the central question: **After identity is known, which exact action on which exact resource is allowed, and where is that decision enforced?**
2. Demonstrate this capstone result: Every operation has a policy; correct scope without ownership and ownership without permission both fail.
3. Show the planted defect, the first failing oracle, and the retained regression.
4. Explain why this invariant is shared across languages: scope, role, tenant, relationship, assurance, freshness, and concealment are evaluated for the exact operation and resource.
5. State exactly which database, network, process, telemetry backend, or operated exercise was not run in the current environment.

## Continue only when

Continue when the system again provides this module result—Every operation has a policy; correct scope without ownership and ownership without permission both fail.—all focused checks pass, the **Authorization and Policy Enforcement** planted defect has failed for the predicted reason, and the record identifies every live claim not executed in the current environment.
