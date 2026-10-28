# Checkpoint — Module 06: Durable Workers and Recovery

## Required result

Analysis work survives restart, abandoned leases are recovered, and stale workers cannot overwrite newer results.

## Demonstrate

- Separate durable acceptance from execution.
- Claim work without holding a long transaction.
- Fence stale workers with lease generation.
- Recover abandoned jobs safely.
- Make duplicate execution converge on one durable outcome.

## Commands

```bash
make predecessor-proof
make operation-proof
make module-proof MODULE=06 TRACK=python
make module-proof MODULE=06 TRACK=typescript
make core-proof
```

## Defend the design

1. Answer the central question: **What internal machinery makes `202 Accepted` honest after API or worker processes die?**
2. Demonstrate this capstone result: Analysis work survives restart, abandoned leases are recovered, and stale workers cannot overwrite newer results.
3. Show the planted defect, the first failing oracle, and the retained regression.
4. Explain why this invariant is shared across languages: a lease generation prevents an expired worker from committing effects after another worker takes ownership.
5. State exactly which database, network, process, telemetry backend, or operated exercise was not run in the current environment.

## Continue only when

Continue when the system again provides this module result—Analysis work survives restart, abandoned leases are recovered, and stale workers cannot overwrite newer results.—all focused checks pass, the **Durable Workers and Recovery** planted defect has failed for the predicted reason, and the record identifies every live claim not executed in the current environment.
