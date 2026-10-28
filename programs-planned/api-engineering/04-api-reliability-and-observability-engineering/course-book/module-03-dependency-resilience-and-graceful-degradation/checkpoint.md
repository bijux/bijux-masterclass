# Checkpoint — Module 03: Dependency Resilience and Graceful Degradation

## Required result

PostgreSQL, artifact storage, webhook delivery, and telemetry export each receive a justified resilience policy.

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

## Defend the design

1. Answer the central question: **When a dependency slows or fails, which work should stop, continue, queue, or degrade—and what must the API say?**
2. Demonstrate this capstone result: PostgreSQL, artifact storage, webhook delivery, and telemetry export each receive a justified resilience policy.
3. Show the planted defect, the first failing oracle, and the retained regression.
4. Explain why this invariant is shared across languages: circuits, bulkheads, retry policy, and degradation apply per dependency and never convert uncertain durable outcomes into success.
5. State exactly which database, network, process, telemetry backend, or operated exercise was not run in the current environment.

## Continue only when

Continue when the system again provides this module result—PostgreSQL, artifact storage, webhook delivery, and telemetry export each receive a justified resilience policy.—all focused checks pass, the **Dependency Resilience and Graceful Degradation** planted defect has failed for the predicted reason, and the record identifies every live claim not executed in the current environment.
