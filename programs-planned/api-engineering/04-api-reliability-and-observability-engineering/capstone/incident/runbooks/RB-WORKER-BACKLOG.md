# RB-WORKER-BACKLOG — Worker backlog and run-start freshness

**Owner:** Analysis worker owner

**Trigger:** Run-start freshness budget burn or oldest queued age above objective

**Customer impact:** Accepted runs remain queued beyond the promised start interval.

## Prerequisites

- Access to durable job state, lease evidence, and queue-age metrics.
- Ability to pause admissions without losing accepted work.

## Immediate actions

- Confirm queue age, claim rate, and durable API submission.
- Separate worker inability from a shared dependency bottleneck.

## Stop conditions

- Do not add workers while database lock or artifact latency is the bottleneck.
- Stop recovery if duplicate completion or fencing violations appear.

## Diagnosis

- Inspect worker liveness, lease renewals, expired claims, and claim failures.
- Check PostgreSQL lock, pool, and query evidence.
- Compare the last known healthy worker release.

## Mitigation

- Restart only workers that cannot make progress.
- Recover expired leases with the existing generation-fencing rule.
- Pause new admissions if the queue cannot drain safely.

## Rollback

- Return admission policy and worker count to the recorded baseline.
- Remove temporary fault controls and verify no orphaned lease remains.

## Recovery validation

- Oldest queue age falls monotonically.
- New runs start within objective.
- No duplicate artifact, terminal event, or outbox event is created.

## Closure criteria

- Backlog is below the steady-state threshold.
- Reconciliation reports no target findings.
- Root cause and prevention work are recorded.

## Escalation

- Escalate to database owner for claim contention.
- Escalate to artifact owner for completion stalls.
