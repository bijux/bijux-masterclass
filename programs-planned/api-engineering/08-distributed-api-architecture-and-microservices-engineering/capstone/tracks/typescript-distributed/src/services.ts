import { createHash } from "node:crypto";

import {
  CapabilityAuthority,
  type CapabilityClaims,
} from "./capability.js";
import {
  Conflict,
  type ArtifactRecord,
  type OperationResult,
  type RequestContext,
  type RunRecord,
  Unauthorized,
  ValidationError,
  requireScope,
} from "./model.js";

interface IdempotencyRecord {
  fingerprint: string;
  runId: string;
}

export class AnalysisControlService {
  readonly runs = new Map<string, RunRecord>();
  readonly idempotency = new Map<string, IdempotencyRecord>();
  readonly events: Array<Record<string, unknown>> = [];
  readonly artifactRefs = new Set<string>();

  private counter = 0;

  constructor(readonly authority: CapabilityAuthority) {}

  createRun(
    ctx: RequestContext,
    requestId: string,
    datasetId: string,
  ): RunRecord {
    requireScope(ctx, "runs:write");
    const fingerprint = createHash("sha256")
      .update(`${ctx.tenant}|${datasetId}`)
      .digest("hex");
    const idempotencyKey = `${ctx.tenant}|${requestId}`;
    const existing = this.idempotency.get(idempotencyKey);
    if (existing) {
      if (existing.fingerprint !== fingerprint) {
        throw new Conflict("idempotency key reused with changed input");
      }
      return this.requireRun(existing.runId);
    }

    this.counter += 1;
    const run: RunRecord = {
      runId: `run-${this.counter}`,
      tenant: ctx.tenant,
      owner: ctx.subject,
      datasetId,
      attemptId: `attempt-${this.counter}-1`,
      state: "queued",
      version: 1,
      artifactIds: [],
    };
    this.runs.set(run.runId, run);
    this.idempotency.set(idempotencyKey, {
      fingerprint,
      runId: run.runId,
    });
    this.events.push({
      type: "AnalysisRunRequested",
      run_id: run.runId,
      version: run.version,
      tenant: ctx.tenant,
    });
    return run;
  }

  start(runId: string): RunRecord {
    const run = this.requireRun(runId);
    if (run.state !== "queued") {
      throw new Conflict("run is not queued");
    }
    run.state = "running";
    run.version += 1;
    this.events.push({
      type: "AnalysisRunStarted",
      run_id: runId,
      version: run.version,
      tenant: run.tenant,
    });
    return run;
  }

  mintUploadCapability(
    ctx: RequestContext,
    runId: string,
    sha256: string,
    maxBytes: number,
    now: number,
  ): string {
    requireScope(ctx, "runs:write");
    const run = this.requireRun(runId);
    if (run.tenant !== ctx.tenant) {
      throw new Unauthorized("tenant mismatch");
    }
    if (run.state !== "running") {
      throw new Conflict(
        "artifact upload requires the current running attempt",
      );
    }
    const claims: CapabilityClaims = {
      jti: `upload:${runId}:${run.attemptId}:${sha256}`,
      issuer: this.authority.issuer,
      audience: "artifact-service",
      subject: ctx.subject,
      tenant: ctx.tenant,
      resource: runId,
      action: "artifact:upload",
      issuedAt: now,
      expiresAt: now + 300,
      sha256,
      maxBytes,
    };
    return this.authority.mint(claims);
  }

  attachAndComplete(
    runId: string,
    attemptId: string,
    artifactId: string,
    eventId: string,
  ): RunRecord {
    const run = this.requireRun(runId);
    if (run.attemptId !== attemptId) {
      throw new Conflict("stale worker attempt");
    }
    if (run.state === "completed") {
      if (run.artifactIds.includes(artifactId)) return run;
      throw new Conflict("run completed with another artifact");
    }
    if (run.state !== "running") {
      throw new Conflict("run is not running");
    }
    if (!run.artifactIds.includes(artifactId)) {
      run.artifactIds.push(artifactId);
      this.artifactRefs.add(artifactId);
    }
    run.state = "completed";
    run.version += 1;
    if (!this.events.some((event) => event.event_id === eventId)) {
      this.events.push({
        event_id: eventId,
        type: "AnalysisRunCompleted",
        run_id: runId,
        artifact_id: artifactId,
        version: run.version,
        tenant: run.tenant,
      });
    }
    return run;
  }

  getRun(ctx: RequestContext, runId: string): RunRecord {
    requireScope(ctx, "runs:read");
    const run = this.requireRun(runId);
    if (run.tenant !== ctx.tenant) {
      throw new Unauthorized("resource not visible");
    }
    return run;
  }

  private requireRun(runId: string): RunRecord {
    const run = this.runs.get(runId);
    if (!run) throw new ValidationError("unknown run");
    return run;
  }
}

export class ArtifactService {
  readonly artifacts = new Map<string, ArtifactRecord>();
  private readonly byEffect = new Map<string, string>();
  private counter = 0;

  constructor(readonly authority: CapabilityAuthority) {}

  store(
    token: string,
    tenant: string,
    content: Uint8Array,
    now: number,
  ): ArtifactRecord {
    const claims = this.authority.verify(token, {
      audience: "artifact-service",
      tenant,
      action: "artifact:upload",
      now,
    });
    const digest = createHash("sha256").update(content).digest("hex");
    if (claims.sha256 !== digest) {
      throw new ValidationError("artifact checksum mismatch");
    }
    if (claims.maxBytes !== undefined && content.byteLength > claims.maxBytes) {
      throw new ValidationError("artifact exceeds capability limit");
    }

    const attemptId = claims.jti.split(":")[2];
    if (!attemptId) {
      throw new ValidationError("capability does not identify an attempt");
    }
    const effect = `${claims.resource}|${attemptId}|${digest}`;
    const existingId = this.byEffect.get(effect);
    if (existingId) return this.requireArtifact(existingId);

    this.counter += 1;
    const artifact: ArtifactRecord = {
      artifactId: `artifact-${this.counter}`,
      tenant,
      runId: claims.resource,
      attemptId,
      sha256: digest,
      content: content.slice(),
      version: 1,
      state: "published",
    };
    this.artifacts.set(artifact.artifactId, artifact);
    this.byEffect.set(effect, artifact.artifactId);
    return artifact;
  }

  markOrphan(artifactId: string): void {
    const artifact = this.requireArtifact(artifactId);
    artifact.state = "orphaned";
    artifact.version += 1;
  }

  get(artifactId: string, tenant: string): ArtifactRecord {
    const artifact = this.requireArtifact(artifactId);
    if (artifact.tenant !== tenant) {
      throw new Unauthorized("artifact not visible");
    }
    return artifact;
  }

  private requireArtifact(artifactId: string): ArtifactRecord {
    const artifact = this.artifacts.get(artifactId);
    if (!artifact) throw new ValidationError("unknown artifact");
    return artifact;
  }
}

export class NotificationService {
  readonly inbox = new Set<string>();
  readonly notificationRunIds = new Set<string>();
  readonly deliveries: Array<Record<string, string>> = [];

  consume(event: Record<string, unknown>): "duplicate" | "ignored" | "accepted" {
    const eventId = String(
      event.event_id ?? `${event.type}:${event.run_id}:${event.version}`,
    );
    if (this.inbox.has(eventId)) return "duplicate";
    this.inbox.add(eventId);

    if (
      event.type !== "AnalysisRunCompleted" &&
      event.type !== "AnalysisRunFailed"
    ) {
      return "ignored";
    }
    const runId = String(event.run_id);
    this.notificationRunIds.add(runId);
    this.deliveries.push({
      deliveryId: `delivery:${eventId}`,
      runId,
      state: "pending",
    });
    return "accepted";
  }
}

export class Gateway {
  constructor(
    private readonly control: AnalysisControlService,
    private readonly artifacts: ArtifactService,
  ) {}

  getRunView(
    ctx: RequestContext,
    runId: string,
    artifactAvailable = true,
  ): OperationResult<Record<string, unknown>> {
    const run = this.control.getRun(ctx, runId);
    const artifactViews: Array<Record<string, unknown>> = [];
    const warnings: string[] = [];

    if (artifactAvailable) {
      for (const artifactId of run.artifactIds) {
        const artifact = this.artifacts.get(artifactId, ctx.tenant);
        artifactViews.push({
          artifactId: artifact.artifactId,
          sha256: artifact.sha256,
          size: artifact.content.byteLength,
          state: artifact.state,
        });
      }
    } else if (run.artifactIds.length > 0) {
      warnings.push("artifactsUnavailable");
    }

    return {
      value: {
        runId: run.runId,
        tenant: run.tenant,
        owner: run.owner,
        datasetId: run.datasetId,
        attemptId: run.attemptId,
        state: run.state,
        version: run.version,
        artifactIds: [...run.artifactIds],
        artifacts: artifactViews,
      },
      authoritative: true,
      partial: warnings.length > 0,
      warnings,
    };
  }
}
