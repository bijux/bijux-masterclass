import test from "node:test";
import assert from "node:assert/strict";

import {
  BatchLoader,
  ResumableSubscription,
  requireField,
} from "../dist/index.js";

test("batch loader collapses duplicate keys and preserves association", () => {
  const calls = [];
  const loader = new BatchLoader((keys) => {
    calls.push([...keys]);
    return new Map([...keys].reverse().map((key) => [key, key.toUpperCase()]));
  });
  const first = loader.load("run-1");
  const duplicate = loader.load("run-1");
  const second = loader.load("run-2");
  loader.dispatch();
  assert.equal(first, duplicate);
  assert.equal(first.get(), "RUN-1");
  assert.equal(second.get(), "RUN-2");
  assert.deepEqual(calls, [["run-1", "run-2"]]);
});

test("separate loaders do not share request cache", () => {
  let calls = 0;
  for (let request = 0; request < 2; request += 1) {
    const loader = new BatchLoader((keys) => {
      calls += 1;
      return new Map(keys.map((key) => [key, key]));
    });
    loader.load("run-1");
    loader.dispatch();
  }
  assert.equal(calls, 2);
});

test("field policy binds permission and tenant", () => {
  const principal = {
    subject: "u",
    tenantId: "tenant-a",
    permissions: new Set(["ARTIFACT_READ"]),
  };
  requireField(principal, "AnalysisRun.artifacts", "tenant-a");
  assert.throws(() =>
    requireField(principal, "AnalysisRun.artifacts", "tenant-b"),
  );
  assert.throws(() =>
    requireField(
      { ...principal, permissions: new Set() },
      "AnalysisRun.artifacts",
      "tenant-a",
    ),
  );
});

test("subscription suppresses duplicates and rejects gaps", () => {
  const subscription = new ResumableSubscription();
  assert.deepEqual(
    subscription
      .resume(
        [
          { sequence: 4, payload: {} },
          { sequence: 4, payload: {} },
          { sequence: 5, payload: {} },
        ],
        3,
      )
      .map((event) => event.sequence),
    [4, 5],
  );
  assert.throws(() =>
    subscription.resume([{ sequence: 5, payload: {} }], 3),
  );
});

test("subscription buffer remains bounded", () => {
  const subscription = new ResumableSubscription(2);
  assert.throws(() =>
    subscription.resume(
      [
        { sequence: 1, payload: {} },
        { sequence: 2, payload: {} },
        { sequence: 3, payload: {} },
      ],
      0,
    ),
  );
});
