# RB-API-ERROR-BUDGET — API error-budget burn

**Owner:** API service owner

**Trigger:** Fast or slow availability-budget burn alert

**Customer impact:** Eligible requests are failing or exceeding their latency objective.

## Prerequisites

- Access to SLI queries, deployment history, and dependency health.
- An incident channel and named incident commander for page-severity events.

## Immediate actions

- Confirm the alert uses eligible production traffic.
- Assign incident commander and operations lead.
- Freeze unrelated releases while the fast-burn condition is active.

## Stop conditions

- Stop an action that increases eligible failures or bypasses a security control.
- Escalate rather than repeatedly restarting healthy instances.

## Diagnosis

- Compare failures by operation, outcome, and status class.
- Inspect PostgreSQL pool wait, query spans, and recent releases.
- Use representative traces only after aggregate impact is confirmed.

## Mitigation

- Remove an unhealthy instance from readiness.
- Rollback the suspected release when evidence supports causality.
- Disable only an optional dependency whose degraded response remains contract-honest.

## Rollback

- Reverse the mitigation if the burn rate worsens in both windows.
- Restore the previous service release without rolling back an irreversible schema migration.

## Recovery validation

- Burn rate falls below one in both windows.
- Synthetic and real eligible journeys succeed.
- No security control was bypassed and no durable submission was lost.

## Closure criteria

- The SLO remains healthy for one short alert window.
- Follow-up work has an owner and due date.
- Incident evidence and customer impact are recorded.

## Escalation

- Escalate to the database owner when PostgreSQL is implicated.
- Escalate to communications lead for sustained customer impact.
