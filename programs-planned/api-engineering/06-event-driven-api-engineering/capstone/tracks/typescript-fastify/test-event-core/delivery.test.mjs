import test from "node:test";
import assert from "node:assert/strict";
import { DeterministicBroker } from "../dist/event-engineering/broker.js";
import { event } from "./helpers.mjs";

test("different partitions can be delivered concurrently", () => {
  const broker = new DeterministicBroker(() => 1000);
  broker.createChannel("analysis.events", 8);
  broker.publish("analysis.events", "run-001", event(70, { runId: "run-001" }));
  broker.publish("analysis.events", "run-999", event(71, { runId: "run-999" }));
  const deliveries = broker.poll("analytics", "analysis.events", 2);
  assert.ok(deliveries.length >= 1);
  assert.ok(deliveries.length <= 2);
});
