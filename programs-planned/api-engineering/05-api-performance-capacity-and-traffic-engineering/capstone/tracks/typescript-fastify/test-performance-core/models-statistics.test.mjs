import test from "node:test";
import assert from "node:assert/strict";

import { canonicalJson, sha256Identity } from "../dist/performance/identity.js";
import { createEnvironment, createWorkloadSpec } from "../dist/performance/models.js";
import { nearestRank, summarize } from "../dist/performance/statistics.js";
import { estimatedClosedThroughput, openSchedule } from "../dist/performance/workload.js";

test("canonical identity ignores object key order", () => {
  const left = { b: 2, a: { y: 2, x: 1 } };
  const right = { a: { x: 1, y: 2 }, b: 2 };
  assert.equal(canonicalJson(left), canonicalJson(right));
  assert.equal(sha256Identity(left), sha256Identity(right));
});

test("identity rejects non-finite and unsafe numbers", () => {
  assert.throws(() => canonicalJson({ value: Number.NaN }));
  assert.throws(() => canonicalJson({ value: Number.MAX_SAFE_INTEGER + 1 }));
});

test("workload identity excludes annotations", () => {
  const base = {
    id: "WL-RUN-LIST",
    model: "open",
    ratePerSecond: 120,
    durationSeconds: 60,
    datasetId: "DS-MEDIUM",
    requestMix: { listRuns: 1 },
  };
  const a = createWorkloadSpec({ ...base, annotations: { note: "a" } });
  const b = createWorkloadSpec({ ...base, annotations: { note: "b" } });
  assert.equal(a.identity, b.identity);
  assert.notEqual(a.identity, createWorkloadSpec({ ...base, ratePerSecond: 100 }).identity);
});

test("invalid workload mix is rejected", () => {
  assert.throws(() =>
    createWorkloadSpec({
      id: "WL-X",
      model: "open",
      ratePerSecond: 1,
      durationSeconds: 1,
      datasetId: "DS",
      requestMix: { a: 0.4, b: 0.4 },
    }),
  );
});

test("environment identity uses string bytes", () => {
  const environment = createEnvironment({
    runtime: "node",
    runtimeVersion: "22.16.0",
    cpuLogical: 4,
    memoryLimitBytes: "1073741824",
    processCount: 1,
    workerCount: 1,
    sourceRevision: "abc123",
    datasetId: "DS-MEDIUM",
    databaseProfile: "local",
  });
  assert.match(environment.identity, /^sha256:/);
});

test("nearest-rank summary is deterministic", () => {
  const values = [2, 4, 4, 8, 20];
  assert.equal(nearestRank(values, 0.5), 4);
  assert.equal(nearestRank(values, 0.9), 20);
  const summary = summarize(values);
  assert.equal(summary.count, 5);
  assert.equal(summary.p95, 20);
  assert.equal(summary.quantileAlgorithm, "nearest-rank");
});

test("open and closed workload arithmetic", () => {
  const arrivals = openSchedule(100, 2);
  assert.equal(arrivals.length, 200);
  assert.equal(arrivals[1].scheduledNs, 10_000_000n);
  assert.equal(estimatedClosedThroughput(40, 0.3, 0.2), 80);
});
