import { DeterministicBroker } from "./broker.js";
import { buildEvent } from "./envelope.js";
import { TransactionalProjection } from "./inbox.js";
import { DomainOutboxStore, OutboxRelay } from "./outbox.js";

export function runDemo(): Record<string, unknown> {
  let now = Date.parse("2026-08-07T10:00:00Z");
  const broker = new DeterministicBroker(() => now);
  broker.createChannel("analysis.events", 4);
  const event = buildEvent({ source: "urn:bijux:analysis-control", eventType: "org.bijux.analysis.run.completed.v1", subject: "analysis-runs/run-001", dataSchema: "https://schemas.bijux.test/analysis-run-completed/v1", tenantId: "tenant-a", correlationId: "00000000-0000-4000-8000-000000000010", partitionKey: "run-001", data: { runId: "run-001", durationMs: 8421, artifactCount: 2, occurredAt: "2026-08-07T09:59:59Z" }, eventId: "00000000-0000-4000-8000-000000000011", time: new Date(now) });
  const store = new DomainOutboxStore();
  store.commit({ aggregateId: "run-001", aggregateState: { status: "completed" }, channel: "analysis.events", key: "run-001", event });
  const relay = new OutboxRelay(store, broker, () => now);
  try { relay.step(true); } catch {}
  relay.step();
  const projection = new TransactionalProjection();
  for (let index = 0; index < 2; index += 1) {
    const delivery = broker.poll("analytics-v1", "analysis.events")[0];
    if (!delivery) throw new Error("missing delivery");
    projection.apply({ tenantId: "tenant-a", consumer: "analytics", effectVersion: "v1", event: delivery.record.event, mutation: (state) => { state.completed = Number(state.completed ?? 0) + 1; } });
    broker.ack(delivery.token);
  }
  return { brokerRecords: broker.records("analysis.events").length, projection: projection.snapshot("tenant-a", "analytics", "v1"), effects: projection.appliedCount };
}
