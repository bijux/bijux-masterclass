import test from "node:test";
import assert from "node:assert/strict";
import {
  CircuitBreaker,
  InMemoryEventSink,
  MetricRegistry,
  StructuredLogger,
  FaultPlan,
  burnRate,
  parseRunbook,
} from "../dist-reliability/index.js";

test("histogram buckets are cumulative and rendered", () => {
  const registry = new MetricRegistry();
  const histogram = registry.histogram(
    { name: "analysis_duration_seconds", description: "Observed duration", unit: "s", labels: ["operation"] },
    [0.1, 0.5, 1.0],
  );
  histogram.observe(0.3, { operation: "startAnalysis" });
  histogram.observe(2.0, { operation: "startAnalysis" });
  const point = [...histogram.values.values()][0];
  assert.deepEqual(point.buckets, [0, 1, 1, 2]);
  const output = registry.renderPrometheus();
  assert.match(output, /le="0.5"} 1/);
  assert.match(output, /le="\+Inf"} 2/);
});

test("half-open cancellation cannot consume the probe forever", () => {
  let now = 0;
  const clock = { nowMs: () => now };
  const breaker = new CircuitBreaker(1, 100);
  breaker.failure(clock);
  now = 100;
  breaker.allow(clock);
  assert.equal(breaker.state, "half-open");
  breaker.abandonProbe(clock);
  assert.equal(breaker.state, "open");
});

test("telemetry contains resource identity and sink is bounded", () => {
  const sink = new InMemoryEventSink(1);
  const logger = new StructuredLogger({ nowMs: () => 10, sink, serviceName: "analysis-runs-api", serviceVersion: "1.3.0", deploymentEnvironment: "test", schemaVersion: "1.0" });
  assert.equal(logger.emit("worker.job.claimed"), true);
  assert.equal(logger.emit("worker.job.completed"), false);
  assert.equal(sink.dropped, 1);
  assert.equal(sink.events[0].deploymentEnvironment, "test");
});

test("runbooks require stop, rollback, and closure fields", () => {
  assert.throws(() => parseRunbook({ id: "RB-X" }));
});

test("metric profile rejects unique identifier labels", () => {
  const registry = new MetricRegistry();
  assert.throws(
    () => registry.counter({
      name: "analysis_run_events_total",
      description: "Incorrect metric with one series per run.",
      unit: "events",
      labels: ["run_id"],
    }),
    /forbidden identifier/,
  );
});

test("SLO definitions carry a version boundary", () => {
  assert.throws(
    () => burnRate(
      { id: "api", objective: 0.999, windowSeconds: 60, version: "" },
      { good: 100, total: 100 },
    ),
    /version/,
  );
});

test("fault plans require a falsifiable hypothesis", () => {
  const valid = new FaultPlan({
    id: "worker-loss",
    hypothesis: "one expired lease is recovered without duplicate effects",
    steadyState: ["one durable accepted run exists"],
    blastRadius: "one synthetic run",
    abortConditions: ["duplicate terminal effect"],
    cleanup: ["restore worker", "run reconciliation"],
  });
  valid.validate();
  assert.throws(() => new FaultPlan({
    id: "worker-loss", hypothesis: "",
    steadyState: ["one durable accepted run exists"],
    blastRadius: "one synthetic run",
    abortConditions: ["duplicate terminal effect"], cleanup: ["restore worker"],
  }).validate(), /hypothesis/);
});
