import test from "node:test";
import assert from "node:assert/strict";

import {
  CursorCodec,
  analyze,
  audienceHash,
  decodeGlobalId,
  encodeGlobalId,
  normalizedFilterHash,
  parseDocument,
} from "../dist/index.js";

const principal = {
  subject: "learner",
  tenantId: "tenant-a",
  permissions: new Set(["RUN_READ"]),
};

test("global identifiers round trip", () => {
  const id = encodeGlobalId("Project", "proj-1");
  assert.deepEqual(decodeGlobalId(id), ["Project", "proj-1"]);
  assert.throws(() => encodeGlobalId("Secret", "x"));
});

test("cursor binds tenant, audience, scope, filter, and expiry", () => {
  const codec = new CursorCodec(
    Buffer.from("0123456789abcdef0123456789abcdef"),
  );
  const filterHash = normalizedFilterHash({ status: "RUNNING" });
  const value = codec.encode({
    tenantId: "tenant-a",
    audienceHash: audienceHash(principal),
    scope: "Query.analysisRuns",
    filterHash,
    afterPrimary: "2026-08-02T00:00:00Z",
    afterTiebreaker: "run-2",
    highWaterPrimary: "2026-08-03T00:00:00Z",
    highWaterTiebreaker: "run-3",
    expiresAt: 2_000_000_000,
    version: 1,
  });
  const decoded = codec.decode(value, {
    tenantId: "tenant-a",
    audienceHash: audienceHash(principal),
    scope: "Query.analysisRuns",
    filterHash,
    nowEpoch: 1_900_000_000,
  });
  assert.equal(decoded.afterTiebreaker, "run-2");
  assert.throws(() =>
    codec.decode(value, {
      tenantId: "tenant-b",
      audienceHash: audienceHash(principal),
      scope: "Query.analysisRuns",
      filterHash,
      nowEpoch: 1_900_000_000,
    }),
  );
  assert.throws(() =>
    codec.decode(value, {
      tenantId: "tenant-a",
      audienceHash: audienceHash(principal),
      scope: "Project.analysisRuns",
      filterHash,
      nowEpoch: 1_900_000_000,
    }),
  );
  assert.throws(() =>
    codec.decode(value, {
      tenantId: "tenant-a",
      audienceHash: audienceHash(principal),
      scope: "Query.analysisRuns",
      filterHash,
      nowEpoch: 2_000_000_001,
    }),
  );
});

test("operation analyzer expands aliases and fragments", () => {
  const document = parseDocument(
    'query Q { a: project(id:"1") { ...P } } fragment P on Project { id name }',
  );
  const report = analyze(document, "Q");
  assert.equal(report.aliases, 1);
  assert.ok(report.depth >= 2);
});

test("fragment cycles are rejected", () => {
  const document = parseDocument(
    'query Q { project(id:"1") { ...A } } fragment A on Project { ...B } fragment B on Project { ...A }',
  );
  assert.throws(() => analyze(document, "Q"));
});
