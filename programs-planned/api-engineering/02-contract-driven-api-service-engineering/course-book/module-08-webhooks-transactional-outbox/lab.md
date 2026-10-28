# Lab — Module 08: Transactional Outbox and Webhook Delivery

## Objective

Complete a run, atomically create its event/outbox record, survive receiver failure and dispatcher restart, verify HMAC signatures, deliver duplicates safely, and reject forbidden destinations.

## Setup conditions

The previous baseline is: **Dataset upload and artifact download are bounded, checksummed, atomic, and resumably observable.** Run its checkpoint before changing code. Record the exact baseline command and predict how the planted defect will violate this module question: *How can a committed domain outcome produce an external notification without losing intent or duplicating effects unpredictably?*

## Failure action and investigation

1. **Implement terminal run/event/artifact/outbox atomic transaction.**
2. **Implement outbox expansion into callback and subscription deliveries.**
3. **Implement delivery claim, lease generation, bounded retry, and attempt recording.**
4. **Implement serialize-once HMAC signing in the primary track.**
5. **Run shared signature vectors against both tracks and receiver.**
6. **Use receiver `fail_first`, forced 4xx/5xx, duplicate, stale, and changed-body cases.**
7. **Kill between commit and send, restart dispatcher, and prove eventual delivery.**
8. **Plant direct send-after-commit without outbox, demonstrate lost notification on kill, repair, and retain the process proof.**

### Required planted defect

> Remove the outbox insert and send only after commit; kill the process in the gap and prove the receiver never learns about the completed run.

Preserve the following evidence:

```text
prediction:
change introduced:
minimal setup:
first failing command:
public symptom:
durable/process state:
root cause:
repair:
regression path:
remaining limitation:
```

## Operational oracle

If the terminal run transaction commits, exactly one logical outbox event exists; network failure may delay delivery but cannot erase or invent the domain event.

## Required evidence

- baseline transcript proving the previous checkpoint before **Transactional Outbox and Webhook Delivery** changes
- source, fixture, contract, migration, or configuration diff for this module
- focused result for: Explain the dual-write failure.
- public, durable, security, or operational observation showing: Run completion and webhook intent cannot diverge; duplicate delivery is detectable and safe.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **transactional outbox delivery**
- a limitation statement naming every live database, network, process, telemetry backend, or operated exercise not run

## Cleanup and reset

1. Restore the control changed for **Transactional Outbox and Webhook Delivery**.
2. Remove synthetic data, faults, credentials, permits, files, or delivery state created by this lab.
3. Rerun the focused regression and `make module-proof MODULE=08`.
4. Confirm the system again provides this result: Run completion and webhook intent cannot diverge; duplicate delivery is detectable and safe.

## Completion gate

- atomic outbox
- durable after crash
- stable event identity
- signed exact bytes
- freshness enforced
- receiver dedup
- bounded classified retry
- destination policy
