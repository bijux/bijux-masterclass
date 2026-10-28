import test from "node:test";
import assert from "node:assert/strict";
import { runDemo } from "../dist/event-engineering/demo.js";

test("capstone demo exposes duplicate publication and one committed effect", () => {
  const report = runDemo();
  assert.equal(report.brokerRecords, 2);
  assert.equal(report.effects, 1);
  assert.equal(report.projection.completed, 1);
});
