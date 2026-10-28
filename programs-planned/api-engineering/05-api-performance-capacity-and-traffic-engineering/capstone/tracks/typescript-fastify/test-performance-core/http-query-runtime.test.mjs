import test from "node:test";
import assert from "node:assert/strict";

import {
  RangeNotSatisfiable,
  chooseContentEncoding,
  estimatedApplicationBufferBytes,
  ifNoneMatchMatches,
  ifRangeAllowsRange,
  parseSingleRange,
  strongMatch,
  weakMatch,
} from "../dist/performance/http-efficiency.js";
import {
  possibleConnections,
  summarizePlan,
} from "../dist/performance/query-plans.js";
import { measureCallable } from "../dist/performance/runtime.js";
import { littleLaw, mm1Approximation } from "../dist/performance/queueing.js";

test("validator matching distinguishes weak and strong", () => {
  assert.equal(weakMatch('W/"abc"', '"abc"'), true);
  assert.equal(strongMatch('W/"abc"', '"abc"'), false);
  assert.equal(ifNoneMatchMatches('"x", W/"abc"', '"abc"'), true);
  assert.equal(ifRangeAllowsRange('"abc"', '"abc"'), true);
});

test("single ranges normalize exactly", () => {
  const fixed = parseSingleRange("bytes=100-199", 1000n);
  assert.equal(fixed.start, 100n);
  assert.equal(fixed.endExclusive, 200n);
  assert.equal(fixed.length, 100n);
  assert.equal(fixed.contentRange, "bytes 100-199/1000");
  const suffix = parseSingleRange("bytes=-200", 1000n);
  assert.equal(suffix.start, 800n);
  assert.throws(
    () => parseSingleRange("bytes=1500-", 1000n),
    RangeNotSatisfiable,
  );
  assert.throws(() => parseSingleRange("bytes=0-1,5-6", 10n));
});

test("compression and buffer policy", () => {
  assert.equal(
    chooseContentEncoding({
      acceptEncoding: "gzip, br",
      mediaType: "application/json",
      bodyLength: 5000,
    }),
    "gzip",
  );
  assert.equal(
    chooseContentEncoding({
      acceptEncoding: "gzip",
      mediaType: "application/octet-stream",
      bodyLength: 5000,
    }),
    "identity",
  );
  assert.equal(
    estimatedApplicationBufferBytes(200n, 64n * 1024n, 2n),
    25n * 1024n * 1024n,
  );
});

test("PostgreSQL plan summary preserves bigint counts", () => {
  const plan = [
    {
      Plan: {
        "Node Type": "Limit",
        "Plan Rows": 50,
        "Actual Rows": 50,
        "Shared Hit Blocks": 1,
        "Shared Read Blocks": 2,
        Plans: [
          {
            "Node Type": "Index Scan",
            "Index Name": "idx_runs",
            "Plan Rows": 50,
            "Actual Rows": 50,
            "Shared Hit Blocks": 1,
            "Shared Read Blocks": 2,
          },
        ],
      },
    },
  ];
  const summary = summarizePlan(plan);
  assert.equal(summary.actualRows, 50n);
  assert.deepEqual(summary.indexScans, ["idx_runs"]);
  assert.equal(summary.sharedReadBlocks, 4n);
});

test("connection budget", () => {
  assert.equal(
    possibleConnections({
      apiInstances: 8,
      apiPoolMax: 20,
      workers: 4,
      workerPoolMax: 5,
      operationalReserve: 10,
    }),
    190,
  );
});

test("runtime measurement and queueing", () => {
  const { value, sample } = measureCallable(() =>
    Array.from({ length: 1000 }, (_, index) => index).reduce((a, b) => a + b, 0),
  );
  assert.equal(value, 499500);
  assert.ok(sample.wallNs > 0n);
  assert.ok(sample.cpuUserMicros >= 0);
  assert.equal(
    littleLaw({ throughputPerSecond: 20, meanTimeSeconds: 5 }).meanInSystem,
    100,
  );
  assert.equal(mm1Approximation(95, 100).meanTimeSeconds, 0.2);
});
