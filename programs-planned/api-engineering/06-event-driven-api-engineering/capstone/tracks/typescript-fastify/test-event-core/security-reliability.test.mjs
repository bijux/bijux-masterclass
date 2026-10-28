import test from "node:test";
import assert from "node:assert/strict";
import { DeterministicBroker } from "../dist/event-engineering/broker.js";
import { authorizeMessage, SecurityError, signMessage, verifyMessage } from "../dist/event-engineering/security.js";
import { classifyLag, ConsumerRunner, DeadLetterStore, PermanentMessageError } from "../dist/event-engineering/reliability.js";
import { event } from "./helpers.mjs";

function grant(value) {
  return { producerId: "analysis-control", sources: new Set([value.source]), channels: new Set(["analysis.events"]), eventTypes: new Set([value.type]), tenants: new Set(["tenant-a"]) };
}

test("producer grant binds source, channel, type, and tenant", () => {
  const value = event(30);
  assert.doesNotThrow(() => authorizeMessage(grant(value), "analysis.events", value));
  assert.throws(() => authorizeMessage(grant(value), "artifact.events", value), SecurityError);
  assert.throws(() => authorizeMessage(grant(value), "analysis.events", event(31, { data: { runId: "run-001", accessToken: "secret" } })), SecurityError);
});

test("exact-byte signature verifies, alteration and staleness fail", () => {
  const value = event(32);
  const secret = new TextEncoder().encode("fixture-secret");
  const signed = signMessage(value, "key-1", secret, new Date("2026-08-07T10:00:00Z"));
  const keys = new Map([["key-1", secret]]);
  assert.doesNotThrow(() => verifyMessage(signed, keys, new Date("2026-08-07T10:01:00Z")));
  assert.throws(() => verifyMessage({ ...signed, body: new Uint8Array([...signed.body, 32]) }, keys, new Date("2026-08-07T10:01:00Z")), SecurityError);
  assert.throws(() => verifyMessage(signed, keys, new Date("2026-08-07T11:00:00Z")), SecurityError);
});

test("permanent failure dead-letters immediately", () => {
  const broker = new DeterministicBroker(() => 1000);
  broker.createChannel("analysis.events", 1);
  broker.publish("analysis.events", "run-001", event(33));
  const dead = new DeadLetterStore();
  const runner = new ConsumerRunner(broker, dead, 3, () => 0);
  assert.equal(runner.step("analytics", "analysis.events", () => { throw new PermanentMessageError("unsupported schema"); }), "dead-lettered");
  assert.equal(dead.rows.length, 1);
});

test("transient failure retries then dead-letters", () => {
  const broker = new DeterministicBroker(() => 1000);
  broker.createChannel("analysis.events", 1);
  broker.publish("analysis.events", "run-001", event(34));
  const dead = new DeadLetterStore();
  const runner = new ConsumerRunner(broker, dead, 2, () => 0);
  const handler = () => { throw new Error("database unavailable"); };
  assert.equal(runner.step("analytics", "analysis.events", handler), "retry");
  assert.equal(runner.step("analytics", "analysis.events", handler), "dead-lettered");
});

test("lag health considers both count and oldest age", () => {
  assert.equal(classifyLag(1, 4000, { warningLag: 100, criticalLag: 1000, warningAge: 60, criticalAge: 3600 }).state, "critical");
  assert.equal(classifyLag(101, 1, { warningLag: 100, criticalLag: 1000, warningAge: 60, criticalAge: 3600 }).state, "warning");
});
