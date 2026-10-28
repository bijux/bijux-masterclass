# Checkpoint — Module 08: Abuse Resistance and Resource Budgets

## Required result

Analysis submission, upload, streaming, and webhook registration have explicit resource budgets.

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

## Defend the design

1. Answer the central question: **How does the API keep expensive operations bounded when valid-looking clients consume resources aggressively?**
2. Demonstrate this capstone result: Analysis submission, upload, streaming, and webhook registration have explicit resource budgets.
3. Show the planted defect, the first failing oracle, and the retained regression.
4. Explain why this invariant is shared across languages: cost is charged before expensive work and bounded by principal, tenant, operation, concurrency, storage, and time dimensions.
5. State exactly which database, network, process, telemetry backend, or operated exercise was not run in the current environment.

## Continue only when

Continue when the system again provides this module result—Analysis submission, upload, streaming, and webhook registration have explicit resource budgets.—all focused checks pass, the **Abuse Resistance and Resource Budgets** planted defect has failed for the predicted reason, and the record identifies every live claim not executed in the current environment.
