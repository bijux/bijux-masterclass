import test from "node:test";
import assert from "node:assert/strict";
import { Counter, MetricError, evaluateHealth } from "../dist-reliability/index.js";

test("metric cardinality budget", () => {
  const counter = new Counter({ name: "requests_total", description: "requests", unit: "{request}", labels: ["route"], maxSeries: 2 });
  counter.add(1, { route: "/a" }); counter.add(1, { route: "/b" }); assert.throws(() => counter.add(1, { route: "/c" }), MetricError);
});

test("draining is live and not ready", () => {
  const health = evaluateHealth({ phase: "draining", startupComplete: true, eventLoopProgressing: true, components: [{ name: "postgres", requiredForReadiness: true, available: true }] });
  assert.equal(health.live, true); assert.equal(health.ready, false); assert.ok(health.reasons.includes("draining"));
});
