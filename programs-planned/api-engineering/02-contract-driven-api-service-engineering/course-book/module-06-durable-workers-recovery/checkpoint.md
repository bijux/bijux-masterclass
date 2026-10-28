# Checkpoint — Module 06: Durable Workers and Recovery

## Required result

Add durable jobs, leases, heartbeats, fencing, cancellation, duplicate-safe effects, and abandoned-work recovery.

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

## Evidence to retain

- baseline transcript proving the previous checkpoint before **Durable Workers and Recovery** changes
- the exact source, fixture, contract, migration, or configuration diff that implements **Durable Workers and Recovery**
- focused result for: Separate durable acceptance from execution.
- public, durable, security, or operational observation showing: Analysis work survives restart, abandoned leases are recovered, and stale workers cannot overwrite newer results.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **durable job leasing and fencing**
- a limitation statement naming every live dependency required to support the strongest **Durable Workers and Recovery** claim but not exercised

## Defend the design

1. Answer the central question: **What internal machinery makes `202 Accepted` honest after API or worker processes die?**
2. Demonstrate this capstone result: Analysis work survives restart, abandoned leases are recovered, and stale workers cannot overwrite newer results.
3. Show the **Durable Workers and Recovery** defect, the first failing oracle, and the exact regression retained after repair.
4. Explain why this invariant is shared across languages: a lease generation prevents an expired worker from committing effects after another worker takes ownership.
5. State which environment-backed **Durable Workers and Recovery** route was not run and how that limits the claim.

## Continue only when

Continue when the system again provides this module result—Analysis work survives restart, abandoned leases are recovered, and stale workers cannot overwrite newer results.—all focused checks pass, the **Durable Workers and Recovery** planted defect has failed for the predicted reason, and the record identifies every live claim not executed in the current environment.
