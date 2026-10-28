import test from "node:test";
import assert from "node:assert/strict";

import {
  AnalysisGraphGateway,
  classify,
  decide,
  demoOperations,
  encodeGlobalId,
  evaluate,
  runTour,
} from "../dist/index.js";

function context(permissions = [
  "PROJECT_READ",
  "PROJECT_WRITE",
  "RUN_READ",
  "RUN_WRITE",
  "ARTIFACT_READ",
  "DELIVERY_READ",
]) {
  return {
    principal: {
      subject: "learner",
      tenantId: "tenant-a",
      permissions: new Set(permissions),
    },
    requestId: "test",
    deadlineMs: 1_000,
    clientName: "test",
    nowEpoch: 1_786_147_200,
  };
}

function execute(gateway, registry, name, variables, ctx = context()) {
  return gateway.execute(registry.named(name).sha256, variables, ctx);
}

test("gateway tour batches and replays", () => {
  const value = runTour();
  assert.equal(value.overviewRuns, 2);
  assert.deepEqual(value.batchCalls, { artifact: 1, delivery: 1 });
  assert.equal(value.replayedFirst, false);
  assert.equal(value.replayedSecond, true);
  assert.equal(value.registeredOperations, 10);
});

test("all ten registered operations have semantic executors", () => {
  const registry = demoOperations();
  const gateway = new AnalysisGraphGateway(registry);
  const projectId = encodeGlobalId("Project", "proj-1");
  const run1 = encodeGlobalId("AnalysisRun", "run-1");
  const run2 = encodeGlobalId("AnalysisRun", "run-2");
  const cases = {
    Viewer: {},
    GetProjectOverview: { projectId, first: 2 },
    GetRun: { runId: run1 },
    ListRuns: { first: 2 },
    SearchPlatform: { text: "run", first: 3 },
    CreateProject: { input: { idempotencyKey: "p-key", name: "New Study" } },
    StartAnalysis: {
      input: {
        idempotencyKey: "r-key",
        projectId,
        datasetId: "d-x",
        algorithm: "qc",
      },
    },
    CancelAnalysis: {
      input: { runId: run2, expectedVersion: "2" },
    },
    RunUpdates: { runId: run1, afterSequence: "3" },
    NodeLookup: { by: { externalId: "project/proj-1" } },
  };
  for (const [name, variables] of Object.entries(cases)) {
    const result = execute(gateway, registry, name, variables);
    assert.notEqual(result.errors?.[0]?.message, "operation has no executor", name);
  }
});

test("nested field denial makes no artifact call", () => {
  const registry = demoOperations();
  const gateway = new AnalysisGraphGateway(registry);
  const result = execute(
    gateway,
    registry,
    "GetRun",
    { runId: encodeGlobalId("AnalysisRun", "run-1") },
    context(["RUN_READ"]),
  );
  assert.equal(result.data.analysisRun.artifacts, null);
  assert.equal(result.errors[0].code, "FORBIDDEN");
  assert.equal(gateway.artifacts.calls.count("batchByRun"), 0);
});

test("high-water cursor excludes a later newer insertion", () => {
  const registry = demoOperations();
  const gateway = new AnalysisGraphGateway(registry);
  const first = execute(gateway, registry, "ListRuns", { first: 1 });
  const cursor = first.data.analysisRuns.pageInfo.endCursor;
  gateway.analysis.runs.set("run-new", {
    id: "run-new",
    tenantId: "tenant-a",
    projectId: "proj-1",
    datasetId: "new",
    status: "RUNNING",
    version: "1",
    createdAt: "2026-08-09T00:00:00Z",
    resultSummary: null,
  });
  const continued = execute(gateway, registry, "ListRuns", {
    first: 10,
    after: cursor,
  });
  const ids = continued.data.analysisRuns.edges.map((edge) => edge.node.id);
  assert.ok(!ids.includes(encodeGlobalId("AnalysisRun", "run-new")));
  const fresh = execute(gateway, registry, "ListRuns", { first: 1 });
  assert.equal(
    fresh.data.analysisRuns.edges[0].node.id,
    encodeGlobalId("AnalysisRun", "run-new"),
  );
});

test("schema release classifications remain directional", () => {
  assert.equal(
    classify({ kind: "remove-field", coordinate: "AnalysisRun.status" })
      .classification,
    "breaking",
  );
  assert.equal(
    classify({ kind: "add-enum-value", coordinate: "RunStatus.PAUSED" })
      .classification,
    "review-required",
  );
  assert.equal(
    decide({
      compatibility: [classify({ kind: "remove-field", coordinate: "x" })],
      activeOperationsValid: true,
      budgetsPass: true,
      ownershipComplete: true,
      oldClientPasses: true,
    }).accepted,
    false,
  );
});

test("HTTP profile rejects mutation through GET", () => {
  assert.equal(
    evaluate({
      method: "POST",
      accept: "application/graphql-response+json",
      contentType: "application/json",
      operationType: "query",
    }).accepted,
    true,
  );
  assert.equal(
    evaluate({
      method: "GET",
      accept: "application/graphql-response+json",
      operationType: "mutation",
    }).status,
    405,
  );
});
