import { createHash } from "node:crypto";

import { ApiProblem } from "./problems.js";
import type {
  AnalysisRun,
  AnalysisRunCreate,
  Artifact,
  Dataset,
  DatasetCreate,
  Principal,
  Project,
  ProjectCreate,
  ProjectPatch,
  RunCompletedEvent,
  RunProgressEvent,
  WebhookSubscription,
  WebhookSubscriptionCreate,
} from "./types.js";

const now = (): string => new Date().toISOString();

function page<T>(values: T[], cursor: string | undefined, limit: number): { items: T[]; nextCursor: string | null } {
  const start = Number.parseInt(cursor ?? "0", 10);
  const items = values.slice(start, start + limit);
  const nextCursor = start + limit < values.length ? String(start + limit) : null;
  return { items, nextCursor };
}

function canonical(value: unknown): string {
  if (Array.isArray(value)) {
    return `[${value.map(canonical).join(",")}]`;
  }
  if (value !== null && typeof value === "object") {
    const entries = Object.entries(value as Record<string, unknown>)
      .filter(([, item]) => item !== undefined)
      .sort(([left], [right]) => left.localeCompare(right));
    return `{${entries.map(([key, item]) => `${JSON.stringify(key)}:${canonical(item)}`).join(",")}}`;
  }
  return JSON.stringify(value);
}

export class InMemoryStore {
  private counters = {
    project: 0,
    dataset: 0,
    run: 0,
    artifact: 0,
    subscription: 0,
    event: 0,
  };

  private readonly projects = new Map<string, Project>();
  private readonly datasets = new Map<string, Dataset>();
  private readonly datasetContent = new Map<string, Buffer>();
  private readonly runs = new Map<string, AnalysisRun>();
  private readonly runCallbacks = new Map<string, string | null>();
  private readonly artifacts = new Map<string, Artifact>();
  private readonly subscriptions = new Map<string, WebhookSubscription>();
  private readonly idempotency = new Map<string, { fingerprint: string; runId: string }>();
  private readonly outboundEvents: RunCompletedEvent[] = [];
  private readonly progressByRun = new Map<string, RunProgressEvent[]>();
  private readonly runDueAt = new Map<string, number>();

  public reset(): void {
    this.counters = {
      project: 0,
      dataset: 0,
      run: 0,
      artifact: 0,
      subscription: 0,
      event: 0,
    };
    this.projects.clear();
    this.datasets.clear();
    this.datasetContent.clear();
    this.runs.clear();
    this.runCallbacks.clear();
    this.artifacts.clear();
    this.subscriptions.clear();
    this.idempotency.clear();
    this.outboundEvents.splice(0);
    this.progressByRun.clear();
    this.runDueAt.clear();
  }

  private id(kind: keyof InMemoryStore["counters"], prefix: string): string {
    this.counters[kind] += 1;
    return `${prefix}_${String(this.counters[kind]).padStart(4, "0")}`;
  }

  private visible(principal: Principal, ownerId: string): boolean {
    return principal.admin || principal.subject === ownerId;
  }

  public etag(project: Project): string {
    return `"${project.id}:${project.version}"`;
  }

  public createProject(principal: Principal, body: ProjectCreate): Project {
    const timestamp = now();
    const project: Project = {
      id: this.id("project", "prj"),
      ownerId: principal.subject,
      name: body.name,
      description: body.description ?? null,
      version: 1,
      createdAt: timestamp,
      updatedAt: timestamp,
    };
    this.projects.set(project.id, project);
    return project;
  }

  public getProject(projectId: string, principal: Principal): Project {
    const project = this.projects.get(projectId);
    if (!project || !this.visible(principal, project.ownerId)) {
      throw new ApiProblem(404, "Resource not found", "The requested project does not exist.", "not-found");
    }
    return project;
  }

  public listProjects(
    principal: Principal,
    limit: number,
    cursor: string | undefined,
    name: string | undefined,
  ): { items: Project[]; nextCursor: string | null } {
    const values = [...this.projects.values()]
      .filter(
        (project) =>
          this.visible(principal, project.ownerId) &&
          (name === undefined || project.name.toLowerCase().includes(name.toLowerCase())),
      )
      .sort((left, right) => left.id.localeCompare(right.id));
    return page(values, cursor, limit);
  }

  public updateProject(
    projectId: string,
    principal: Principal,
    ifMatch: string | undefined,
    patch: ProjectPatch,
  ): Project {
    const project = this.getProject(projectId, principal);
    if (!ifMatch) {
      throw new ApiProblem(
        428,
        "Precondition required",
        "This update requires the latest If-Match entity tag.",
        "precondition-required",
      );
    }
    if (ifMatch !== this.etag(project)) {
      throw new ApiProblem(412, "Precondition failed", "The supplied entity tag is stale.", "precondition-failed");
    }
    const revised: Project = {
      ...project,
      name: Object.hasOwn(patch, "name") ? (patch.name as string) : project.name,
      description: Object.hasOwn(patch, "description") ? (patch.description ?? null) : project.description,
      version: project.version + 1,
      updatedAt: now(),
    };
    this.projects.set(projectId, revised);
    return revised;
  }

  public createDataset(projectId: string, principal: Principal, body: DatasetCreate): Dataset {
    const project = this.getProject(projectId, principal);
    const timestamp = now();
    const dataset: Dataset = {
      id: this.id("dataset", "dts"),
      projectId,
      ownerId: project.ownerId,
      name: body.name,
      source: body.source,
      status: body.source.kind === "local-file" ? "awaiting-upload" : "ready",
      contentLength: null,
      checksumSha256:
        body.source.kind === "remote-object" ? (body.source.checksumSha256 ?? null) : null,
      createdAt: timestamp,
      updatedAt: timestamp,
    };
    this.datasets.set(dataset.id, dataset);
    return dataset;
  }

  public getDataset(datasetId: string, principal: Principal): Dataset {
    const dataset = this.datasets.get(datasetId);
    if (!dataset || dataset.status === "deleted" || !this.visible(principal, dataset.ownerId)) {
      throw new ApiProblem(404, "Resource not found", "The requested dataset does not exist.", "not-found");
    }
    return dataset;
  }

  public listDatasets(
    projectId: string,
    principal: Principal,
    limit: number,
    cursor: string | undefined,
    status: "awaiting-upload" | "ready" | undefined,
  ): { items: Dataset[]; nextCursor: string | null } {
    this.getProject(projectId, principal);
    const values = [...this.datasets.values()]
      .filter(
        (dataset) =>
          dataset.projectId === projectId &&
          dataset.status !== "deleted" &&
          this.visible(principal, dataset.ownerId) &&
          (status === undefined || dataset.status === status),
      )
      .sort((left, right) => left.id.localeCompare(right.id));
    return page(values, cursor, limit);
  }

  public uploadDataset(
    datasetId: string,
    principal: Principal,
    content: Buffer,
    mediaType: string,
  ): { datasetId: string; contentLength: number; checksumSha256: string; uploadedAt: string } {
    const dataset = this.getDataset(datasetId, principal);
    if (dataset.source.kind !== "local-file") {
      throw new ApiProblem(
        409,
        "Request conflict",
        "Remote-object datasets do not accept local uploads.",
        "conflict",
      );
    }
    const normalized = mediaType.split(";", 1)[0]?.trim().toLowerCase() ?? "";
    const allowed = new Set(["text/csv", "application/json", "application/octet-stream"]);
    if (!allowed.has(normalized)) {
      throw new ApiProblem(
        415,
        "Unsupported media type",
        `Unsupported uploaded media type: ${normalized || "<missing>"}.`,
        "unsupported-media-type",
      );
    }
    if (content.length === 0) {
      throw new ApiProblem(422, "Request validation failed", "The uploaded file is empty.", "validation");
    }
    if (content.length > 1_048_576) {
      throw new ApiProblem(413, "Payload too large", "The training upload limit is 1 MiB.", "payload-too-large");
    }
    const checksumSha256 = createHash("sha256").update(content).digest("hex");
    const uploadedAt = now();
    const revised: Dataset = {
      ...dataset,
      status: "ready",
      contentLength: content.length,
      checksumSha256,
      updatedAt: uploadedAt,
    };
    this.datasets.set(datasetId, revised);
    this.datasetContent.set(datasetId, content);
    return { datasetId, contentLength: content.length, checksumSha256, uploadedAt };
  }

  public deleteDataset(datasetId: string, principal: Principal): void {
    const dataset = this.getDataset(datasetId, principal);
    const active = [...this.runs.values()].some(
      (run) => run.datasetId === datasetId && (run.status === "queued" || run.status === "running"),
    );
    if (active) {
      throw new ApiProblem(
        409,
        "Request conflict",
        "An active analysis run depends on this dataset.",
        "conflict",
      );
    }
    this.datasets.set(datasetId, { ...dataset, status: "deleted", updatedAt: now() });
    this.datasetContent.delete(datasetId);
  }

  public createRun(
    principal: Principal,
    idempotencyKey: string,
    body: AnalysisRunCreate,
  ): { run: AnalysisRun; replay: boolean } {
    const project = this.getProject(body.projectId, principal);
    const dataset = this.getDataset(body.datasetId, principal);
    if (dataset.projectId !== project.id) {
      throw new ApiProblem(
        409,
        "Request conflict",
        "The dataset does not belong to the selected project.",
        "conflict",
      );
    }
    if (dataset.status !== "ready") {
      throw new ApiProblem(
        409,
        "Request conflict",
        "The dataset must be ready before analysis starts.",
        "conflict",
      );
    }

    const fingerprint = createHash("sha256").update(canonical(body)).digest("hex");
    const key = `${principal.subject}\0${idempotencyKey}`;
    const existing = this.idempotency.get(key);
    if (existing) {
      if (existing.fingerprint !== fingerprint) {
        throw new ApiProblem(
          409,
          "Request conflict",
          "The idempotency key was already used with a different request body.",
          "idempotency-conflict",
        );
      }
      const run = this.runs.get(existing.runId);
      if (!run) {
        throw new Error("idempotency record references a missing run");
      }
      return { run, replay: true };
    }

    const timestamp = now();
    const run: AnalysisRun = {
      id: this.id("run", "run"),
      projectId: project.id,
      datasetId: dataset.id,
      ownerId: project.ownerId,
      status: "queued",
      parameters: {
        algorithm: body.parameters.algorithm,
        priority: body.parameters.priority ?? "normal",
        labels: body.parameters.labels ?? {},
      },
      progress: 0,
      createdAt: timestamp,
      updatedAt: timestamp,
      completedAt: null,
      artifactIds: [],
    };
    this.runs.set(run.id, run);
    this.runCallbacks.set(run.id, body.callbackUrl ?? null);
    this.progressByRun.set(run.id, [
      {
        eventId: this.id("event", "evt"),
        runId: run.id,
        status: "queued",
        progress: 0,
        occurredAt: timestamp,
      },
    ]);
    // This is a Course 1 simulator. Course 2 replaces it with a durable
    // database-backed worker and leases. Reads never own this transition.
    this.runDueAt.set(run.id, Date.now() + 40);
    this.idempotency.set(key, { fingerprint, runId: run.id });
    return { run, replay: false };
  }

  public getRun(runId: string, principal: Principal): AnalysisRun {
    const run = this.runs.get(runId);
    if (!run || !this.visible(principal, run.ownerId)) {
      throw new ApiProblem(
        404,
        "Resource not found",
        "The requested run does not exist.",
        "not-found",
      );
    }
    return run;
  }

  public advanceSimulation(at = Date.now()): number {
    let changed = 0;
    for (const [runId, dueAt] of [...this.runDueAt.entries()]) {
      if (at < dueAt) continue;
      const run = this.runs.get(runId);
      if (!run || (run.status !== "queued" && run.status !== "running")) {
        this.runDueAt.delete(runId);
        continue;
      }
      if (run.status === "queued") {
        const occurredAt = now();
        const running: AnalysisRun = {
          ...run,
          status: "running",
          progress: 50,
          updatedAt: occurredAt,
        };
        this.runs.set(runId, running);
        this.progressByRun.get(runId)?.push({
          eventId: this.id("event", "evt"),
          runId,
          status: "running",
          progress: 50,
          occurredAt,
        });
        this.runDueAt.set(runId, at + 40);
      } else {
        const completed = this.complete(run);
        this.progressByRun.get(runId)?.push({
          eventId: this.id("event", "evt"),
          runId,
          status: "completed",
          progress: 100,
          occurredAt: completed.updatedAt,
        });
        this.runDueAt.delete(runId);
      }
      changed += 1;
    }
    return changed;
  }

  public listRuns(
    principal: Principal,
    limit: number,
    cursor: string | undefined,
    status: AnalysisRun["status"] | undefined,
  ): { items: AnalysisRun[]; nextCursor: string | null } {
    const values = [...this.runs.values()]
      .filter(
        (run) => this.visible(principal, run.ownerId) && (status === undefined || run.status === status),
      )
      .sort((left, right) => left.id.localeCompare(right.id));
    return page(values, cursor, limit);
  }

  private complete(run: AnalysisRun): AnalysisRun {
    const artifactPayload = Buffer.from(
      canonical({ runId: run.id, algorithm: run.parameters.algorithm, status: "completed" }),
    );
    const timestamp = now();
    const artifact: Artifact = {
      id: this.id("artifact", "art"),
      runId: run.id,
      ownerId: run.ownerId,
      name: `${run.parameters.algorithm}.json`,
      mediaType: "application/json",
      size: artifactPayload.length,
      checksumSha256: createHash("sha256").update(artifactPayload).digest("hex"),
      createdAt: timestamp,
    };
    this.artifacts.set(artifact.id, artifact);
    const completed: AnalysisRun = {
      ...run,
      status: "completed",
      progress: 100,
      updatedAt: timestamp,
      completedAt: timestamp,
      artifactIds: [artifact.id],
    };
    this.runs.set(run.id, completed);
    this.outboundEvents.push({
      eventId: this.id("event", "evt"),
      eventType: "analysis.completed",
      occurredAt: timestamp,
      run: completed,
    });
    return completed;
  }

  public cancelRun(runId: string, principal: Principal): AnalysisRun {
    const run = this.getRun(runId, principal);
    if (run.status !== "queued" && run.status !== "running") {
      throw new ApiProblem(409, "Request conflict", `A ${run.status} run cannot be canceled.`, "conflict");
    }
    const timestamp = now();
    const canceled: AnalysisRun = {
      ...run,
      status: "canceled",
      updatedAt: timestamp,
      completedAt: timestamp,
    };
    this.runs.set(runId, canceled);
    this.runDueAt.delete(runId);
    this.progressByRun.get(runId)?.push({
      eventId: this.id("event", "evt"),
      runId,
      status: "canceled",
      progress: canceled.progress,
      occurredAt: timestamp,
    });
    return canceled;
  }

  public listArtifacts(runId: string, principal: Principal): Artifact[] {
    const run = this.getRun(runId, principal);
    if (run.status !== "completed") {
      throw new ApiProblem(
        409,
        "Request conflict",
        "Artifacts are available only after completion.",
        "conflict",
      );
    }
    return run.artifactIds.map((artifactId) => {
      const artifact = this.artifacts.get(artifactId);
      if (!artifact) {
        throw new Error("run references a missing artifact");
      }
      return artifact;
    });
  }

  public getArtifact(artifactId: string, principal: Principal): Artifact {
    const artifact = this.artifacts.get(artifactId);
    if (!artifact || !this.visible(principal, artifact.ownerId)) {
      throw new ApiProblem(404, "Resource not found", "The requested artifact does not exist.", "not-found");
    }
    return artifact;
  }

  public progressEvents(
    runId: string,
    principal: Principal,
  ): RunProgressEvent[] {
    this.getRun(runId, principal);
    return [...(this.progressByRun.get(runId) ?? [])];
  }

  public createSubscription(
    principal: Principal,
    body: WebhookSubscriptionCreate,
  ): WebhookSubscription {
    const subscription: WebhookSubscription = {
      id: this.id("subscription", "whs"),
      ownerId: principal.subject,
      targetUrl: body.targetUrl,
      eventTypes: [...body.eventTypes],
      secretHint: `****${body.secret.slice(-4)}`,
      createdAt: now(),
    };
    this.subscriptions.set(subscription.id, subscription);
    return subscription;
  }

  public diagnostics(): {
    counts: Record<"projects" | "datasets" | "runs" | "artifacts" | "subscriptions", number>;
    outboundEvents: RunCompletedEvent[];
  } {
    return {
      counts: {
        projects: this.projects.size,
        datasets: [...this.datasets.values()].filter((dataset) => dataset.status !== "deleted").length,
        runs: this.runs.size,
        artifacts: this.artifacts.size,
        subscriptions: this.subscriptions.size,
      },
      outboundEvents: [...this.outboundEvents],
    };
  }
}

export const store = new InMemoryStore();
