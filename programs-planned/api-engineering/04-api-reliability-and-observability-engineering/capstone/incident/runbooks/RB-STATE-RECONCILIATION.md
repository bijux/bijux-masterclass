# RB-STATE-RECONCILIATION — Cross-table state reconciliation

**Owner:** Analysis service owner

**Trigger:** Confirmed run, job, artifact, event, or outbox divergence

**Customer impact:** Customers may observe incorrect terminal state, missing output, or missing notification.

## Prerequisites

- A transactionally consistent read-only snapshot.
- A reviewed definition of authoritative evidence for the affected finding.

## Immediate actions

- Freeze automatic repair.
- Capture a read-only reconciliation snapshot.
- Open an incident when customer-visible state is wrong.

## Stop conditions

- Stop when sources disagree and authority is ambiguous.
- Never invent an artifact, completion, or successful delivery.

## Diagnosis

- Identify the earliest durable divergence.
- Check transaction, worker lease, and stale-generation evidence.
- Verify artifact checksums before proposing mutation.

## Mitigation

- Apply only reviewed idempotent repair actions.
- Use one stable repair key per finding.
- Repair the minimum state required to restore an existing truth.

## Rollback

- A repair must define its inverse before execution.
- Restore from captured before-state only when the inverse preserves newer writes.

## Recovery validation

- Rerun reconciliation with zero target findings.
- Verify the public resource, progress events, artifact, and webhook state.
- Retain before-and-after evidence.

## Closure criteria

- No unresolved customer-visible divergence remains.
- Repair actions are independently reviewed.
- The missing prevention or detection control has an owner.

## Escalation

- Escalate to service owner for ambiguous truth.
- Escalate to security if integrity compromise is suspected.
