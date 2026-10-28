import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import test from "node:test";

import { CapabilityAuthority } from "../dist/src/capability.js";
import { reconcile } from "../dist/src/reconciliation.js";
import {
  AnalysisControlService,
  ArtifactService,
  Gateway,
  NotificationService,
} from "../dist/src/services.js";
import { runTour } from "../dist/src/tour.js";


const context = {
  subject: "u",
  tenant: "tenant-a",
  workload: "gateway",
  scopes: new Set(["runs:read", "runs:write"]),
  deadlineMs: 10_000,
  nowMs: 0,
  traceId: "trace-test",
};

function completeRun() {
  const authority = new CapabilityAuthority(
    "analysis-control",
    "course-eight-capability-key",
  );
  const control = new AnalysisControlService(authority);
  const artifacts = new ArtifactService(authority);
  const notifications = new NotificationService();
  const run = control.createRun(context, "request-1", "dataset-1");
  control.start(run.runId);
  const body = new TextEncoder().encode("result");
  const digest = createHash("sha256").update(body).digest("hex");
  const token = control.mintUploadCapability(
    context,
    run.runId,
    digest,
    10,
    1,
  );
  const artifact = artifacts.store(token, context.tenant, body, 2);
  control.attachAndComplete(
    run.runId,
    run.attemptId,
    artifact.artifactId,
    "done",
  );
  const event = control.events.find((candidate) => candidate.event_id === "done");
  if (!event) throw new Error("completion event missing");
  notifications.consume(event);
  return { control, artifacts, notifications, run, artifact, event, token, body };
}


test("distributed completion keeps one owner per effect", () => {
  const result = completeRun();
  const replay = result.artifacts.store(
    result.token,
    context.tenant,
    result.body,
    2,
  );
  assert.equal(result.artifact.artifactId, replay.artifactId);
  assert.equal(result.notifications.consume(result.event), "duplicate");
  assert.deepEqual(reconcile({
    controlArtifactRefs: result.control.artifactRefs,
    artifactIds: new Set(result.artifacts.artifacts.keys()),
    completedRuns: new Set([result.run.runId]),
    notificationRunIds: result.notifications.notificationRunIds,
  }), []);
});


test("upload capability requires the current running attempt", () => {
  const authority = new CapabilityAuthority(
    "analysis-control",
    "course-eight-capability-key",
  );
  const control = new AnalysisControlService(authority);
  const run = control.createRun(context, "not-running", "dataset-1");
  assert.throws(() => control.mintUploadCapability(
    context,
    run.runId,
    "0".repeat(64),
    10,
    1,
  ));
});


test("artifact service copies caller-owned bytes", () => {
  const authority = new CapabilityAuthority(
    "analysis-control",
    "course-eight-capability-key",
  );
  const control = new AnalysisControlService(authority);
  const artifacts = new ArtifactService(authority);
  const run = control.createRun(context, "request-2", "dataset-2");
  control.start(run.runId);
  const body = new TextEncoder().encode("result");
  const digest = createHash("sha256").update(body).digest("hex");
  const token = control.mintUploadCapability(
    context,
    run.runId,
    digest,
    10,
    1,
  );
  const artifact = artifacts.store(token, context.tenant, body, 2);
  body.fill(120);
  assert.equal(new TextDecoder().decode(artifact.content), "result");
});


test("gateway marks a degraded composition as partial", () => {
  const result = completeRun();
  const gateway = new Gateway(result.control, result.artifacts);
  const complete = gateway.getRunView(context, result.run.runId);
  assert.equal(complete.partial, false);
  assert.equal(complete.value.artifacts.length, 1);

  const degraded = gateway.getRunView(context, result.run.runId, false);
  assert.equal(degraded.partial, true);
  assert.deepEqual(degraded.warnings, ["artifactsUnavailable"]);
  assert.deepEqual(degraded.value.artifacts, []);
});


test("tour completes and demonstrates explicit degradation", () => {
  const result = runTour();
  assert.equal(result.state, "completed");
  assert.equal(result.fullViewPartial, false);
  assert.equal(result.degradedViewPartial, true);
  assert.deepEqual(result.degradedViewWarnings, ["artifactsUnavailable"]);
  assert.deepEqual(result.reconciliation, []);
});


test("reconciliation finds missing effects", () => {
  assert.deepEqual(reconcile({
    controlArtifactRefs: new Set(),
    artifactIds: new Set(["a"]),
    completedRuns: new Set(["r"]),
    notificationRunIds: new Set(),
  }), ["orphan-artifact:a", "missing-notification:r"]);
});
