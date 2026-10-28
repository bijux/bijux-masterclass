# Lab — duplicate Job attempt, single business effect

## Goal

Demonstrate at-least-once execution and exactly-once effect through durable idempotency.

## Safety boundary

Use the semantic Job runner and its local durable effect store. Do not target external production systems.

## Baseline

Create one maintenance Job with one logical operation ID and one expected completion.

## Hypothesis

If the first Pod performs the effect and crashes before reporting success, the controller creates another attempt. The second attempt observes the completed effect and exits success without repeating it.

## Controlled action

1. Execute the first attempt through external-effect commit.
2. Inject a crash before Pod success.
3. Reconcile the Job and run the replacement attempt.
4. Repeat reconciliation after Job completion.

## Oracle

At least two execution attempts exist, exactly one effect record exists, and Job completion becomes true. Repeated reconciliation creates no additional effect.

## Evidence

Preserve Job/Pod identities, attempt timeline, operation key, effect-store record, crash point, completion condition, and retry classification.

## Interpretation

Explain why “exactly once Job” is the wrong claim and why exactly-once effect is bounded to the durable effect store.

## Cleanup

Delete generated semantic state after copying the evidence report.

## Completion gate

Advance only when duplicate execution is visible and duplicate business effect is impossible under the tested crash point.
