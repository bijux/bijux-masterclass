# Checkpoint — Module 08: Abuse Resistance and Resource Budgets

## Required result

Introduce principal/tenant/operation/cost budgets, concurrency permits, quotas, and bounded degradation.

## Demonstrate

- Choose rate-limit dimensions from abuse paths.
- Implement deterministic token-bucket behavior.
- Limit simultaneous expensive work with leak-free permits.
- Bound uploads, streams, queue depth, and storage.
- Return coherent `429` or `503` outcomes without amplifying retries.

## Commands

```bash
make module-proof MODULE=08 TRACK=python
make module-proof MODULE=08 TRACK=typescript
make core-proof
```

## Evidence to retain

- baseline transcript proving the previous checkpoint before **Abuse Resistance and Resource Budgets** changes
- the exact source, fixture, contract, migration, or configuration diff that implements **Abuse Resistance and Resource Budgets**
- focused result for: Choose rate-limit dimensions from abuse paths.
- public, durable, security, or operational observation showing: Analysis submission, upload, streaming, and webhook registration have explicit resource budgets.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **resource budgets and abuse admission**
- a limitation statement naming every live dependency required to support the strongest **Abuse Resistance and Resource Budgets** claim but not exercised

## Defend the design

1. Answer the central question: **How does the API keep expensive operations bounded when valid-looking clients consume resources aggressively?**
2. Demonstrate this capstone result: Analysis submission, upload, streaming, and webhook registration have explicit resource budgets.
3. Show the **Abuse Resistance and Resource Budgets** defect, the first failing oracle, and the exact regression retained after repair.
4. Explain why this invariant is shared across languages: cost is charged before expensive work and bounded by principal, tenant, operation, concurrency, storage, and time dimensions.
5. State which environment-backed **Abuse Resistance and Resource Budgets** route was not run and how that limits the claim.

## Continue only when

Continue when the system again provides this module result—Analysis submission, upload, streaming, and webhook registration have explicit resource budgets.—all focused checks pass, the **Abuse Resistance and Resource Budgets** planted defect has failed for the predicted reason, and the record identifies every live claim not executed in the current environment.
