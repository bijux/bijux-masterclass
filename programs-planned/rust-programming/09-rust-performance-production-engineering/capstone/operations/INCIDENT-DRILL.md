# MetricRail Incident Drill

## Scenario

A release changes snapshot rendering. Under high-cardinality traffic, snapshot memory and queue residence rise. Ingestion remains correct, but readiness begins to flap and clients retry snapshot requests.

## Exercise

1. Detect the condition from signals rather than source inspection.
2. Establish a timeline of rollout, load, queue, memory, rejection, and readiness.
3. Stop promotion.
4. Enable the explicit snapshot-degraded mode or reduce snapshot admission.
5. Verify ingestion remains within its objective.
6. Roll back the artifact and configuration.
7. Confirm queues drain, memory returns to the expected envelope, and readiness stabilizes.
8. Preserve a profile and representative workload.

## Learning record

The review must answer:

- Which model failed?
- Which limit or signal was absent?
- Why did retry amplify the condition?
- Which test should be added?
- Which rollout criterion should change?
- Can the architecture be simplified?

Actions change durable controls, tests, or models. “Monitor more carefully” is not a complete action.
