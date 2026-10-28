import { buildEvent } from "../dist/event-engineering/envelope.js";

export function event(suffix, options = {}) {
  const eventType = options.eventType ?? "org.bijux.analysis.run.completed.v1";
  const tenantId = options.tenantId ?? "tenant-a";
  const runId = options.runId ?? "run-001";
  const number = Number(suffix);
  return buildEvent({
    source: "urn:bijux:analysis-control",
    eventType,
    subject: `analysis-runs/${runId}`,
    dataSchema: `https://schemas.bijux.test/${eventType.slice(0, eventType.lastIndexOf("."))}/v1`,
    tenantId,
    correlationId: "00000000-0000-4000-8000-000000000010",
    partitionKey: runId,
    data: options.data ?? { runId, durationMs: 1000, artifactCount: 1, occurredAt: "2026-08-07T10:00:00Z" },
    eventId: `00000000-0000-4000-8000-${String(number).padStart(12, "0")}`,
    time: new Date("2026-08-07T10:00:00Z"),
  });
}
