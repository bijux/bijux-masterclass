# Worked answers — Incremental Extraction, Strangler Migration, and Final Architecture Defense

These answers demonstrate reasoning. Revise your own answer when its decision rule or evidence is weaker.

## 1. Why is Notification Delivery extracted before Artifact Delivery?

It already consumes durable events, has independent retry/retention behavior, and can be shadowed without entering the run-completion critical path.

**Decisive evidence:** extraction sequence ADR

## 2. Why is Artifact extraction delayed until capability authorization exists?

Otherwise the service must query Control synchronously or trust identity headers, preserving coupling or creating an authorization hole.

**Decisive evidence:** artifact prerequisites proof

## 3. What is the authority during shadow mode?

The legacy path. Candidate results are compared and must suppress uncontrolled external effects.

**Decisive evidence:** shadow routing record

## 4. Why must canary selection be stable?

Stateful users or resources should not alternate unpredictably between implementations, which can hide or create divergence.

**Decisive evidence:** deterministic canary test

## 5. How do you avoid uncontrolled dual writes during artifact extraction?

Backfill historical state, shadow reads, then move new write authority through one controlled path with idempotent import and reconciliation.

**Decisive evidence:** write-authority transition report

## 6. What is required before decommission?

Consumer inventory, old writer removal, retention decision, credential and route removal, backup ownership, alert/runbook update, and reconciliation window completion.

**Decisive evidence:** decommission checklist

## 7. When can the legacy path be removed?

After cutover remains within correctness and SLO policy for the declared window, rollback evidence is archived, and no hidden consumers remain.

**Decisive evidence:** decommission gate

## 8. What makes merge-back a valid outcome?

If independent ownership, scaling, and release value fail to materialize while coordination cost remains, merging restores cohesion without erasing contracts.

**Decisive evidence:** merge-back review

## 9. Why does the Course 9 handoff forbid direct database joins?

GraphQL must compose through service contracts and batching; database joins would bypass ownership and recreate a distributed monolith at the graph layer.

**Decisive evidence:** GraphQL boundary brief

## 10. What must a final defense say about Worker Plane?

It is an independently scalable compute deployment; Control remains the authority for leases, attempts, and run completion.

**Decisive evidence:** state ownership defense

## 11. How do you prove the extraction did not weaken the public API?

Run the inherited HTTP conformance and user-journey proof against the cutover topology, including partial and failure outcomes.

**Decisive evidence:** public contract regression

## 12. What is the strongest sign that Course 8 succeeded?

The team can explain why only two services were extracted, how each owns its data and failures, and how to stop or reverse the decision.

**Decisive evidence:** final architecture defense
