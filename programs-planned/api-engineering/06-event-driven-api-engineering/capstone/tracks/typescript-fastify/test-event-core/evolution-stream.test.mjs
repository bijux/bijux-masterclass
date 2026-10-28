import test from "node:test";
import assert from "node:assert/strict";
import { compareObjectSchemas } from "../dist/event-engineering/evolution.js";
import { executeReplay } from "../dist/event-engineering/replay.js";
import { EventTimeWindows } from "../dist/event-engineering/stream.js";
import { evaluateEventRelease } from "../dist/event-engineering/release.js";
import { event } from "./helpers.mjs";

const oldSchema = { type: "object", properties: { runId: { type: "string" } }, required: ["runId"] };

test("schema evolution distinguishes additive, review, and breaking change", () => {
  const additive = { type: "object", properties: { runId: { type: "string" }, summary: { type: "string" } }, required: ["runId"] };
  const required = { type: "object", properties: { runId: { type: "string" }, region: { type: "string" } }, required: ["runId", "region"] };
  const enumOld = { type: "object", properties: { kind: { type: "string", enum: ["full"] } } };
  const enumNew = { type: "object", properties: { kind: { type: "string", enum: ["full", "partial"] } } };
  assert.equal(compareObjectSchemas(oldSchema, additive).status, "accepted");
  assert.equal(compareObjectSchemas(oldSchema, required).status, "rejected");
  assert.equal(compareObjectSchemas(enumOld, enumNew).status, "review-required");
});

test("replay is bounded, tenant-filtered, and side-effect disabled", () => {
  const events = [event(20), event(21, { tenantId: "tenant-b" })];
  const report = executeReplay({ replayId: "replay-1", consumer: "analytics:v2", mode: "dry-run", allowedTypes: new Set([events[0].type]), maximumEvents: 2, sideEffects: "disabled", tenantId: "tenant-a" }, events, (_event, dry) => dry);
  assert.deepEqual(report, { selected: 1, applied: 0, skipped: 0, wouldApply: 1 });
  assert.throws(() => executeReplay({ replayId: "replay-2", consumer: "analytics:v2", mode: "apply", allowedTypes: new Set([events[0].type]), maximumEvents: 1, sideEffects: "disabled" }, events, () => true));
});

test("event-time windows deduplicate and quarantine events beyond allowed lateness", () => {
  const windows = new EventTimeWindows(5 * 60_000, 60_000);
  const value = event(22);
  assert.equal(windows.apply(value).completed, 1);
  assert.equal(windows.apply(value), null);
  windows.advanceWatermark(Date.parse("2026-08-07T11:00:00Z"));
  const late = event(23, { data: { runId: "run-001", durationMs: 1, artifactCount: 1, occurredAt: "2026-08-07T10:00:00Z" } });
  assert.equal(windows.apply(late), null);
  assert.equal(windows.lateEvents.length, 1);
});

test("release decision rejects unsafe replay and breaking schema", () => {
  const additive = { type: "object", properties: { runId: { type: "string" }, summary: { type: "string" } }, required: ["runId"] };
  const breaking = { type: "object", properties: { runId: { type: "string" }, region: { type: "string" } }, required: ["runId", "region"] };
  assert.equal(evaluateEventRelease(oldSchema, additive, { replaySafe: true, catalogComplete: true, contractValid: true }).status, "accepted");
  assert.equal(evaluateEventRelease(oldSchema, additive, { replaySafe: false, catalogComplete: true, contractValid: true }).status, "rejected");
  assert.equal(evaluateEventRelease(oldSchema, breaking, { replaySafe: true, catalogComplete: true, contractValid: true }).status, "rejected");
});
