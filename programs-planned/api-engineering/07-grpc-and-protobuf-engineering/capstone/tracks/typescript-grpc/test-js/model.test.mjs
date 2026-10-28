import test from "node:test";
import assert from "node:assert/strict";
import { advanceRun, etag, parseInt64, requestFingerprint } from "../dist/src/model.js";
import { AnalysisStore } from "../dist/src/inprocess.js";

const principal = {
  subject: "user-write", tenant: "tenant-a",
  scopes: new Set(["runs:write"]), workload: "gateway",
};

test("int64 preserves values above JavaScript safe integer", () => {
  assert.equal(parseInt64("9007199254740992"), 9007199254740992n);
  assert.throws(() => parseInt64("01"));
  assert.throws(() => parseInt64("9223372036854775808"));
});

test("optional terminal fields remain absent", () => {
  const run = {
    name:"projects/p-1/runs/r-1", projectName:"projects/p-1",
    datasetName:"datasets/d-1", state:"QUEUED",
    progressPercent:0, revision:1n,
  };
  const running = advanceRun(run, { state:"RUNNING", progressPercent:10 });
  assert.equal("resultSummary" in running, false);
  assert.equal(etag(running), '"run-2"');
});

test("completed run requires 100 percent", () => {
  const run = {
    name:"r", projectName:"p", datasetName:"d", state:"QUEUED",
    progressPercent:0, revision:1n,
  };
  assert.throws(() => advanceRun(run, { state:"COMPLETED", progressPercent:99 }));
});

test("request fingerprint is stable", () => {
  const input = { parent:"projects/p-1", datasetName:"datasets/d-1", algorithm:"qc", principal };
  assert.equal(requestFingerprint(input), requestFingerprint(input));
});

test("persistent-shape idempotency replays and rejects changed input", () => {
  const store = new AnalysisStore();
  const first = store.createRun({
    parent:"projects/p-1", requestId:"req-1",
    datasetName:"datasets/d-1", algorithm:"qc", principal,
  });
  const replay = store.createRun({
    parent:"projects/p-1", requestId:"req-1",
    datasetName:"datasets/d-1", algorithm:"qc", principal,
  });
  assert.equal(first.name, replay.name);
  assert.throws(() => store.createRun({
    parent:"projects/p-1", requestId:"req-1",
    datasetName:"datasets/d-2", algorithm:"qc", principal,
  }), /ALREADY_EXISTS/);
});
