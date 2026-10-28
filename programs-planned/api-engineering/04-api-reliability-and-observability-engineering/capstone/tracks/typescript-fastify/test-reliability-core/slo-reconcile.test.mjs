import test from "node:test";
import assert from "node:assert/strict";
import { burnRate, evaluateBurnRateAlert, inspect } from "../dist-reliability/index.js";

test("burn rate and multiwindow alert", () => {
  const slo = { id: "availability", objective: 0.999, windowSeconds: 2419200 };
  assert.ok(Math.abs(burnRate(slo, { good: 970, total: 1000 }) - 30) < 1e-9);
  const result = evaluateBurnRateAlert(slo, { id: "fast", severity: "page", longWindowSeconds: 3600, shortWindowSeconds: 300, threshold: 14.4, minimumEvents: 10 }, { good: 980, total: 1000 }, { good: 96, total: 100 });
  assert.equal(result.firing, true);
});

test("reconciliation finds inconsistencies", () => {
  const findings = inspect({ runs: [{ runId: "run_1", status: "completed" }, { runId: "run_2", status: "running" }], jobs: [{ runId: "run_2", status: "dead" }], artifacts: [], outbox: [{ runId: "run_2", eventType: "analysis.failed" }] });
  const kinds = new Set(findings.map((value) => value.kind));
  assert.ok(kinds.has("completed-run-missing-artifact")); assert.ok(kinds.has("terminal-run-missing-outbox")); assert.ok(kinds.has("terminal-job-nonterminal-run"));
});
