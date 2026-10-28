# RB-TELEMETRY-PIPELINE — Telemetry pipeline degradation

**Owner:** Observability platform owner

**Trigger:** Sustained application drops, collector refusal, or missing known signal

**Customer impact:** Diagnostic visibility is reduced; customer correctness cannot be inferred from telemetry alone.

## Prerequisites

- Independent durable-state and synthetic checks.
- Access to exporter and collector self-observability.

## Immediate actions

- Verify customer-facing journeys from independent evidence.
- Do not restart healthy API instances solely to restore telemetry.

## Stop conditions

- Do not make collector availability a liveness dependency.
- Stop increasing telemetry volume while exporter queues are saturated.

## Diagnosis

- Inspect exporter queue, collector memory limiter, refusal, and drop metrics.
- Check endpoint, TLS, authentication, and schema compatibility.
- Identify missing signal types and time ranges.

## Mitigation

- Reduce nonessential telemetry volume.
- Restore collector capacity or endpoint connectivity.
- Preserve bounded structured local events while export is unavailable.

## Rollback

- Restore the normal sampling and batching policy after recovery.
- Remove emergency local retention before it becomes unbounded.

## Recovery validation

- Collector accepts data without sustained refusal.
- Application drop counters stop increasing.
- A known trace, metric, and structured event arrive end to end.

## Closure criteria

- No unexplained telemetry gap remains in the incident interval.
- Any lost evidence is documented as a proof limitation.
- Follow-up capacity or configuration work is owned.

## Escalation

- Escalate to platform owner for collector or backend defects.
- Escalate to security when telemetry loss may be deliberate.
