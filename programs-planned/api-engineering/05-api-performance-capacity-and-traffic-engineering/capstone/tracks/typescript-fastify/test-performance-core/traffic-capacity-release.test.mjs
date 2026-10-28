import test from "node:test";
import assert from "node:assert/strict";

import {
  LimiterRegistry,
  TokenBucket,
  reserveAtomically,
} from "../dist/performance/traffic.js";
import { chooseShedding } from "../dist/performance/shedding.js";
import {
  backlogDrainSeconds,
  cpuDemand,
  decimal,
  evaluateCapacity,
  formatDecimal,
  storageBytes,
  utilizationFromDemand,
} from "../dist/performance/capacity.js";
import { costPerUsefulCompletion } from "../dist/performance/cost.js";
import { evaluateMetric } from "../dist/performance/regression.js";
import { evaluateRelease } from "../dist/performance/release.js";

test("token bucket uses exact bigint refill", () => {
  const bucket = new TokenBucket(10_000_000n, 2_000_000n, 5_000_000n);
  const first = bucket.consume(0n, 5_000_000n);
  assert.equal(first.allowed, true);
  const second = bucket.consume(2_000_000_000n, 5_000_000n);
  assert.equal(second.allowed, false);
  assert.equal(second.remaining, 4_000_000n);
  assert.equal(second.retryAfterNs, 500_000_000n);
});

test("multi-budget reservation rolls back", () => {
  const globalBucket = new TokenBucket(10n, 1n);
  const tenantBucket = new TokenBucket(2n, 1n, 0n);
  const before = globalBucket.state;
  const result = reserveAtomically(
    [
      { bucket: globalBucket, cost: 5n },
      { bucket: tenantBucket, cost: 1n },
    ],
    0n,
  );
  assert.equal(result.allowed, false);
  assert.deepEqual(globalBucket.state, before);
});

test("limiter registry is bounded", () => {
  const registry = new LimiterRegistry(2, 10n, 10n, 1n);
  registry.bucket("a", 0n);
  registry.bucket("b", 0n);
  assert.throws(() => registry.bucket("c", 1n));
  registry.bucket("c", 10n);
  assert.equal(registry.size, 1);
});

test("shedding stages protect controls", () => {
  assert.equal(
    chooseShedding({
      databasePoolFraction: 0.2,
      durableJobFraction: 0.2,
      streamPermitFraction: 0.2,
      storageAvailable: true,
      durableDatabaseAvailable: true,
    }).stage,
    0,
  );
  const unavailable = chooseShedding({
    databasePoolFraction: 0.1,
    durableJobFraction: 0.1,
    streamPermitFraction: 0.1,
    storageAvailable: true,
    durableDatabaseAvailable: false,
  });
  assert.equal(unavailable.stage, 5);
  assert.equal(unavailable.allowedOperations.has("getRun"), true);
  assert.equal(unavailable.allowedOperations.has("submitRun"), false);
});

test("capacity decimal arithmetic", () => {
  const demand = cpuDemand({
    cores: decimal("4"),
    utilization: decimal("0.60"),
    intervalSeconds: decimal("60"),
    completions: decimal("12000"),
  });
  assert.equal(formatDecimal(demand), "0.012");
  assert.equal(
    formatDecimal(
      utilizationFromDemand({
        arrivalRate: decimal("100"),
        demandPerCompletion: decimal("0.005"),
        capacityUnits: decimal("1"),
      }),
    ),
    "0.5",
  );
  assert.equal(
    formatDecimal(
      backlogDrainSeconds({
        backlog: decimal("18000"),
        completionRate: decimal("140"),
        arrivalRate: decimal("100"),
      }),
    ),
    "450",
  );
});

test("capacity chooses first bottleneck", () => {
  const result = evaluateCapacity(
    [
      {
        id: "reads",
        ratePerSecond: "100",
        resourceDemand: { cpu: "0.005", db: "0.008" },
      },
      {
        id: "writes",
        ratePerSecond: "10",
        resourceDemand: { cpu: "0.01", db: "0.03" },
      },
    ],
    [
      { id: "cpu", capacityUnits: "2", targetUtilization: "0.70" },
      { id: "db", capacityUnits: "1", targetUtilization: "0.70" },
    ],
  );
  assert.equal(result.firstBottleneck, "db");
});

test("storage and useful cost", () => {
  assert.equal(
    formatDecimal(
      storageBytes({
        dailyObjects: decimal("10"),
        meanObjectBytes: decimal("100"),
        retentionDays: decimal("30"),
        replicationFactor: decimal("2"),
        overheadFraction: decimal("0.1"),
      }),
    ),
    "66000",
  );
  assert.equal(
    costPerUsefulCompletion("25", "1000").costPerCompletion,
    "0.025",
  );
});

const policy = {
  metrics: [
    {
      name: "p95Ms",
      direction: "lower",
      absoluteRegression: "5",
      relativeRegression: "0.05",
      hardMaximum: "200",
    },
    {
      name: "throughputPerSecond",
      direction: "higher",
      absoluteRegression: "5",
      relativeRegression: "0.03",
      hardMinimum: "50",
    },
    {
      name: "peakMemoryBytes",
      direction: "lower",
      absoluteRegression: "1000000",
      relativeRegression: "0.05",
      hardMaximum: "536870912",
    },
  ],
};

const envelope = ({
  workloadHash = "sha256:w",
  environmentHash = "sha256:e",
  correct = true,
  started = 100,
  missing = 0,
  p95 = "100",
  throughput = "100",
  memory = "100000000",
} = {}) => ({
  profileVersion: "1.0",
  workloadHash,
  environmentHash,
  correctness: { passed: correct },
  outcomes: {
    offered: 100,
    started,
    admitted: 100,
    completed: 100 - missing,
    rejected: 0,
    failed: 0,
    missing,
  },
  summary: {
    p95Ms: p95,
    throughputPerSecond: throughput,
    peakMemoryBytes: memory,
  },
});

test("metric and release decisions", () => {
  assert.equal(
    evaluateMetric("100", "104", {
      name: "p95Ms",
      direction: "lower",
      absoluteRegression: "5",
      relativeRegression: "0.05",
    }).passed,
    true,
  );
  const accepted = evaluateRelease(
    envelope(),
    envelope({ p95: "90", throughput: "110", memory: "95000000" }),
    policy,
  );
  assert.equal(accepted.status, "accepted");
  assert.equal(accepted.gates[0].name, "comparability");
  assert.equal(accepted.gates[1].name, "correctness");
});

test("release rejects correctness and supports inconclusive", () => {
  assert.equal(
    evaluateRelease(envelope(), envelope({ correct: false }), policy).status,
    "rejected",
  );
  assert.equal(
    evaluateRelease(
      envelope(),
      envelope({ environmentHash: "sha256:other" }),
      policy,
    ).status,
    "inconclusive",
  );
  assert.equal(
    evaluateRelease(
      envelope(),
      envelope({ p95: "130", throughput: "80", memory: "600000000" }),
      policy,
    ).status,
    "rejected",
  );
});
