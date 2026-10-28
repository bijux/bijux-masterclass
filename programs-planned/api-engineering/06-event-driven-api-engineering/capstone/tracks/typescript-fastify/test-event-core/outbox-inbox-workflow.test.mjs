import test from "node:test";
import assert from "node:assert/strict";
import { DeterministicBroker } from "../dist/event-engineering/broker.js";
import { DomainOutboxStore, OutboxRelay } from "../dist/event-engineering/outbox.js";
import { TransactionalProjection } from "../dist/event-engineering/inbox.js";
import { initialRunProcess, RunProcessManager } from "../dist/event-engineering/workflows.js";
import { event } from "./helpers.mjs";

test("relay crash after broker acceptance can duplicate publication", () => {
  const broker = new DeterministicBroker(() => 1000);
  broker.createChannel("analysis.events", 2);
  const store = new DomainOutboxStore();
  const value = event(10);
  store.commit({ aggregateId: "run-001", aggregateState: { status: "completed" }, channel: "analysis.events", key: "run-001", event: value });
  const relay = new OutboxRelay(store, broker, () => 1000);
  assert.throws(() => relay.step(true));
  assert.equal(relay.step(), "published");
  const records = broker.records("analysis.events");
  assert.equal(records.length, 2);
  assert.equal(records[0].event.id, records[1].event.id);
});

test("duplicate delivery creates one effect per effect version", () => {
  const projection = new TransactionalProjection();
  const value = event(11);
  const mutation = (state) => { state.count = Number(state.count ?? 0) + 1; };
  assert.equal(projection.apply({ tenantId: "tenant-a", consumer: "analytics", effectVersion: "v1", event: value, mutation }).status, "applied");
  assert.equal(projection.apply({ tenantId: "tenant-a", consumer: "analytics", effectVersion: "v1", event: value, mutation }).status, "duplicate");
  assert.equal(projection.snapshot("tenant-a", "analytics", "v1").count, 1);
  assert.equal(projection.apply({ tenantId: "tenant-a", consumer: "analytics", effectVersion: "v2", event: value, mutation }).status, "applied");
});

test("process manager emits a stable command identity and rejects impossible completion", () => {
  const manager = new RunProcessManager();
  const state = initialRunProcess("run-001");
  const requested = event(12, { eventType: "org.bijux.analysis.run.requested.v1", data: { runId: "run-001", requestedAt: "2026-08-07T10:00:00Z" } });
  assert.equal(manager.apply(state, requested), "applied");
  assert.equal(state.commandId, "start:run-001:1");
  assert.equal(manager.apply(state, requested), "duplicate");
  const completed = event(13);
  assert.equal(manager.apply(state, completed), "applied");
  assert.equal(state.status, "completed");
  assert.equal(manager.timeout(state, 1), "stale");
});
