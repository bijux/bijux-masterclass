# Checkpoint — Module 03: Dependency Resilience and Graceful Degradation

## Required result

Add dependency-local state machines, bounded probes, concurrency isolation, and truthful degraded responses.

## Demonstrate

- Classify dependency failures and ownership.
- Use bulkheads to bound local resource consumption.
- Design circuit state and half-open probe ownership.
- Avoid fallbacks that fabricate correctness.
- Keep telemetry failure from becoming business failure.

## Commands

```bash
make module-proof MODULE=03
make core-proof
```

## Evidence to retain

- baseline transcript proving the previous checkpoint before **Dependency Resilience and Graceful Degradation** changes
- the exact source, fixture, contract, migration, or configuration diff that implements **Dependency Resilience and Graceful Degradation**
- focused result for: Classify dependency failures and ownership.
- public, durable, security, or operational observation showing: PostgreSQL, artifact storage, webhook delivery, and telemetry export each receive a justified resilience policy.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **dependency-local resilience**
- a limitation statement naming every live dependency required to support the strongest **Dependency Resilience and Graceful Degradation** claim but not exercised

## Defend the design

1. Answer the central question: **When a dependency slows or fails, which work should stop, continue, queue, or degrade—and what must the API say?**
2. Demonstrate this capstone result: PostgreSQL, artifact storage, webhook delivery, and telemetry export each receive a justified resilience policy.
3. Show the **Dependency Resilience and Graceful Degradation** defect, the first failing oracle, and the exact regression retained after repair.
4. Explain why this invariant is shared across languages: circuits, bulkheads, retry policy, and degradation apply per dependency and never convert uncertain durable outcomes into success.
5. State which environment-backed **Dependency Resilience and Graceful Degradation** route was not run and how that limits the claim.

## Continue only when

Continue when the system again provides this module result—PostgreSQL, artifact storage, webhook delivery, and telemetry export each receive a justified resilience policy.—all focused checks pass, the **Dependency Resilience and Graceful Degradation** planted defect has failed for the predicted reason, and the record identifies every live claim not executed in the current environment.
