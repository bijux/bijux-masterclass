import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import {
  burnRate,
  classifyHttpOutcome,
  evaluateBurnRateAlert,
  evaluateHealth,
  fitDelaysToDeadline,
  inspect,
  parseRetryAfterMs,
  parseTraceparent,
  redact,
  retryable,
} from "../dist-reliability/index.js";

const vector = (name) => JSON.parse(
  readFileSync(resolve(process.cwd(), "../../shared/vectors", name), "utf8"),
);

test("trace context vectors", () => {
  for (const value of vector("trace-context.json").cases) {
    if (value.valid) assert.equal(parseTraceparent(value.value).sampled, value.sampled, value.id);
    else assert.throws(() => parseTraceparent(value.value), undefined, value.id);
  }
});

test("retry vectors", () => {
  const values = vector("retries.json");
  for (const value of values.classificationCases) {
    assert.equal(retryable({ status: value.status, transportError: value.transportError, safety: value.safety }), value.retry, value.id);
  }
  for (const value of values.fitCases) {
    const clock = { nowMs: () => value.nowMs };
    const deadline = { remainingMs: (source) => Math.max(0, value.deadlineMs - source.nowMs()) };
    assert.deepEqual(fitDelaysToDeadline(value.delays, { clock, deadline, minimumAttemptMs: value.minimumAttemptMs }), value.expected, value.id);
  }
  for (const value of values.retryAfterCases) {
    assert.equal(parseRetryAfterMs(value.value, value.nowMs), value.expectedMs ?? undefined, value.id);
  }
});


test("HTTP outcome vectors", () => {
  for (const value of vector("http-outcomes.json").cases) {
    assert.deepEqual(
      classifyHttpOutcome(value.operation, value.status),
      { eligibility: value.eligibility, outcome: value.outcome },
      value.id,
    );
  }
});

test("health vectors", () => {
  for (const value of vector("health.json").cases) {
    const result = evaluateHealth({ phase: value.phase, startupComplete: value.startupComplete, eventLoopProgressing: value.eventLoopProgressing, components: value.components });
    assert.deepEqual([result.live, result.ready], [value.live, value.ready], value.id);
  }
});

test("slo and alert vectors", () => {
  for (const value of vector("slo.json").cases) {
    const result = burnRate({ id: value.id, objective: value.objective, windowSeconds: 2419200 }, { good: value.good, total: value.total });
    if (value.burnRate === null) assert.equal(result, undefined, value.id);
    else assert.ok(Math.abs(result - value.burnRate) < 1e-8, value.id);
  }
  for (const value of vector("alerts.json").cases) {
    const result = evaluateBurnRateAlert(
      { id: value.id, objective: value.objective, windowSeconds: 2419200 },
      { id: value.id, severity: "page", longWindowSeconds: 3600, shortWindowSeconds: 300, threshold: value.threshold, minimumEvents: value.minimumEvents },
      value.long,
      value.short,
    );
    assert.equal(result.firing, value.firing, value.id);
    if (value.reason !== undefined) assert.equal(result.reason, value.reason, value.id);
  }
});

test("reconciliation vectors", () => {
  for (const value of vector("reconciliation.json").cases) {
    assert.deepEqual(
      inspect(value.snapshot).map((item) => item.kind).sort(),
      [...value.findings].sort(),
      value.id,
    );
  }
});

test("telemetry redaction vectors", () => {
  for (const value of vector("telemetry.json").cases) {
    if (value.attributes !== undefined) assert.deepEqual(redact(value.attributes), value.expected, value.id);
  }
});
