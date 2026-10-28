import test from "node:test";
import assert from "node:assert/strict";
import { canonicalJson, CanonicalizationError } from "../dist/event-engineering/canonical.js";
import { validateEnvelope } from "../dist/event-engineering/envelope.js";
import { partitionFor } from "../dist/event-engineering/partitioning.js";
import { BrokerError, DeterministicBroker } from "../dist/event-engineering/broker.js";
import { event } from "./helpers.mjs";

test("canonical JSON sorts keys and rejects unsafe integers", () => {
  assert.equal(canonicalJson({ b: 1, a: 2 }), '{"a":2,"b":1}');
  assert.throws(() => canonicalJson({ value: Number.MAX_SAFE_INTEGER + 1 }), CanonicalizationError);
  assert.throws(() => canonicalJson({ value: 1.5 }), CanonicalizationError);
});

test("envelope profile and partition function are deterministic", () => {
  assert.equal(validateEnvelope(event(1)).specversion, "1.0");
  assert.equal(partitionFor("run-001", 8), partitionFor("run-001", 8));
  assert.throws(() => validateEnvelope({ ...event(2), type: "AnalysisCompleted" }));
  assert.throws(() => validateEnvelope({ ...event(2), causationid: "not-a-uuid" }));
});

test("ack advances one consumer group but not another", () => {
  const broker = new DeterministicBroker(() => 1000);
  broker.createChannel("analysis.events", 4);
  broker.publish("analysis.events", "run-001", event(3));
  const delivery = broker.poll("analytics", "analysis.events")[0];
  assert.ok(delivery);
  broker.ack(delivery.token);
  assert.equal(broker.poll("analytics", "analysis.events").length, 0);
  assert.equal(broker.poll("audit", "analysis.events").length, 1);
});

test("expired acknowledgement redelivers the same record", () => {
  let now = 1000;
  const broker = new DeterministicBroker(() => now);
  broker.createChannel("analysis.events", 2);
  broker.publish("analysis.events", "run-001", event(4));
  const first = broker.poll("analytics", "analysis.events", 1, 50)[0];
  assert.ok(first);
  now += 51;
  const second = broker.poll("analytics", "analysis.events")[0];
  assert.ok(second);
  assert.equal(second.record.event.id, first.record.event.id);
  assert.equal(second.attempt, 2);
  assert.notEqual(second.token, first.token);
});

test("nack delays redelivery and tokens settle once", () => {
  let now = 1000;
  const broker = new DeterministicBroker(() => now);
  broker.createChannel("analysis.events", 1);
  broker.publish("analysis.events", "run-001", event(5));
  const first = broker.poll("analytics", "analysis.events")[0];
  assert.ok(first);
  broker.nack(first.token, 100);
  assert.equal(broker.poll("analytics", "analysis.events").length, 0);
  now += 100;
  const second = broker.poll("analytics", "analysis.events")[0];
  assert.ok(second);
  broker.ack(second.token);
  assert.throws(() => broker.ack(second.token), BrokerError);
});

test("per-partition order prevents the second record from overtaking", () => {
  const broker = new DeterministicBroker(() => 1000);
  broker.createChannel("analysis.events", 4);
  broker.publish("analysis.events", "run-001", event(6));
  broker.publish("analysis.events", "run-001", event(7));
  const first = broker.poll("analytics", "analysis.events")[0];
  assert.equal(first.record.offset, "0");
  assert.equal(broker.poll("analytics", "analysis.events").length, 0);
  broker.ack(first.token);
  assert.equal(broker.poll("analytics", "analysis.events")[0].record.offset, "1");
});

test("NATS request preserves structured CloudEvent bytes and message identity", async () => {
  const { toNatsRequest } = await import("../dist/event-engineering/nats-adapter.js");
  const value = event(8);
  const request = toNatsRequest("analysis.events.run.lifecycle.v1", value);
  assert.equal(request.messageId, value.id);
  assert.equal(request.headers["Content-Type"], "application/cloudevents+json");
  assert.equal(new TextDecoder().decode(request.payload).includes(value.id), true);
});

test("all contract examples match the published cross-language canonical hashes", async () => {
  const fs = await import("node:fs");
  const path = await import("node:path");
  const crypto = await import("node:crypto");
  const vectorPath = path.resolve("../../shared/vectors/envelope.json");
  const examplesRoot = path.resolve("../../contracts/examples");
  const vector = JSON.parse(fs.readFileSync(vectorPath, "utf8"));
  for (const row of vector.canonicalExamples) {
    const value = JSON.parse(fs.readFileSync(path.join(examplesRoot, row.file), "utf8"));
    const digest = crypto.createHash("sha256").update(canonicalJson(value)).digest("hex");
    assert.equal(digest, row.sha256, row.file);
  }
});
