# Case 5 — Expansion half complete

## Incident

A PVC request increases from 100 GiB to 200 GiB. Kubernetes reports the new capacity, but the database filesystem remains 100 GiB and reaches 100% usage.

## Evidence

- Controller-side volume expansion succeeded.
- The backend device reports 200 GiB.
- Node expansion failed after a node-plugin upgrade.
- The filesystem was never resized.
- Monitoring watched PVC capacity but not filesystem capacity.

## Failure

The release treated expansion as one API update rather than a multi-phase operation. The observed metric represented requested/backend capacity, not application-usable space.

## Correct response

Stop nonessential writes, preserve evidence, repair the node expansion path, and verify device and filesystem sizes before returning normal traffic. Add phase-specific telemetry and an alert for persistent divergence. Future expansion begins before emergency thresholds and includes a rollback or migration plan.

## Lesson

Capacity has several representations. Readiness and alerts must use the one the application actually consumes.
