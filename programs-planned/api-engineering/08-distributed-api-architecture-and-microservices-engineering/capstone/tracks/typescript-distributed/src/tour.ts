import { createHash } from "node:crypto";

import { CapabilityAuthority } from "./capability.js";
import { reconcile } from "./reconciliation.js";
import {
  AnalysisControlService,
  ArtifactService,
  Gateway,
  NotificationService,
} from "./services.js";
import type { RequestContext } from "./model.js";

export function runTour(): Record<string, unknown> {
  const authority = new CapabilityAuthority(
    "analysis-control",
    "course-eight-capability-key",
  );
  const control = new AnalysisControlService(authority);
  const artifacts = new ArtifactService(authority);
  const notifications = new NotificationService();
  const gateway = new Gateway(control, artifacts);

  const ctx: RequestContext = {
    subject: "learner",
    tenant: "tenant-a",
    workload: "edge-gateway",
    scopes: new Set(["runs:read", "runs:write"]),
    deadlineMs: 10_000,
    nowMs: 0,
    traceId: "trace-tour",
  };

  const run = control.createRun(ctx, "request-1", "dataset-1");
  control.start(run.runId);

  const content = new TextEncoder().encode(
    "course-eight-distributed-artifact",
  );
  const digest = createHash("sha256").update(content).digest("hex");
  const token = control.mintUploadCapability(
    ctx,
    run.runId,
    digest,
    1024,
    100,
  );
  const artifact = artifacts.store(token, ctx.tenant, content, 101);
  control.attachAndComplete(
    run.runId,
    run.attemptId,
    artifact.artifactId,
    `completed:${run.runId}:3`,
  );

  const event = control.events.find(
    (candidate) => candidate.type === "AnalysisRunCompleted",
  );
  if (!event) throw new Error("completion event was not recorded");
  notifications.consume(event);

  const findings = reconcile({
    controlArtifactRefs: control.artifactRefs,
    artifactIds: new Set(artifacts.artifacts.keys()),
    completedRuns: new Set([run.runId]),
    notificationRunIds: notifications.notificationRunIds,
  });
  if (findings.length > 0) throw new Error(findings.join(","));

  const fullView = gateway.getRunView(ctx, run.runId);
  const partialView = gateway.getRunView(ctx, run.runId, false);
  return {
    runId: run.runId,
    state: control.runs.get(run.runId)?.state,
    artifactId: artifact.artifactId,
    artifactSha256: artifact.sha256,
    deliveryCount: notifications.deliveries.length,
    fullViewPartial: fullView.partial,
    degradedViewPartial: partialView.partial,
    degradedViewWarnings: partialView.warnings,
    reconciliation: findings,
  };
}

if (import.meta.url === `file://${process.argv[1]}`) {
  console.log(JSON.stringify(runTour(), null, 2));
}
