import {
  ConflictError,
  DownstreamUnavailable,
  PreconditionFailed,
  type Principal,
} from "./model.js";

export interface Project {
  id: string;
  tenantId: string;
  name: string;
  version: string;
}

export interface Run {
  id: string;
  tenantId: string;
  projectId: string;
  datasetId: string;
  status: string;
  version: string;
  createdAt: string;
  resultSummary: string | null;
}

export interface Artifact {
  id: string;
  tenantId: string;
  runId: string;
  mediaType: string;
  size: number;
  sha256: string;
  downloadUrl: string;
}

export type AnalysisSearchItem =
  | { type: "Project"; value: Project }
  | { type: "AnalysisRun"; value: Run };

export class CallLog {
  readonly calls: Array<readonly [string, readonly string[]]> = [];

  add(method: string, ...keys: string[]): void {
    this.calls.push([method, keys]);
  }

  count(method: string): number {
    return this.calls.filter(([name]) => name === method).length;
  }

  reset(): void {
    this.calls.length = 0;
  }
}

function clone<T>(value: T): T {
  return structuredClone(value);
}

export class AnalysisControlClient {
  readonly calls = new CallLog();
  readonly projects = new Map<string, Project>([
    [
      "proj-1",
      {
        id: "proj-1",
        tenantId: "tenant-a",
        name: "Genome Study",
        version: "3",
      },
    ],
  ]);
  readonly runs = new Map<string, Run>([
    [
      "run-1",
      {
        id: "run-1",
        tenantId: "tenant-a",
        projectId: "proj-1",
        datasetId: "data-1",
        status: "COMPLETED",
        version: "5",
        createdAt: "2026-08-01T10:00:00Z",
        resultSummary: "complete",
      },
    ],
    [
      "run-2",
      {
        id: "run-2",
        tenantId: "tenant-a",
        projectId: "proj-1",
        datasetId: "data-2",
        status: "RUNNING",
        version: "2",
        createdAt: "2026-08-02T10:00:00Z",
        resultSummary: null,
      },
    ],
  ]);

  private readonly idempotency = new Map<
    string,
    { fingerprint: string; objectType: "Project" | "AnalysisRun"; objectId: string }
  >();

  readonly events = new Map<string, Array<Record<string, unknown>>>([
    [
      "run-1",
      [
        { sequence: 4, status: "RUNNING" },
        { sequence: 5, status: "COMPLETED" },
      ],
    ],
    [
      "run-2",
      [
        { sequence: 1, status: "QUEUED" },
        { sequence: 2, status: "RUNNING" },
      ],
    ],
  ]);

  getProject(principal: Principal, id: string): Project | undefined {
    this.calls.add("getProject", id);
    const value = this.projects.get(id);
    return value?.tenantId === principal.tenantId ? clone(value) : undefined;
  }

  getRun(principal: Principal, id: string): Run | undefined {
    this.calls.add("getRun", id);
    const value = this.runs.get(id);
    return value?.tenantId === principal.tenantId ? clone(value) : undefined;
  }

  listRuns(principal: Principal, projectId?: string, status?: string): Run[] {
    this.calls.add("listRuns", projectId ?? "*", status ?? "*");
    return [...this.runs.values()]
      .filter(
        (value) =>
          value.tenantId === principal.tenantId &&
          (projectId === undefined || value.projectId === projectId) &&
          (status === undefined || value.status === status),
      )
      .map(clone)
      .sort(
        (left, right) =>
          right.createdAt.localeCompare(left.createdAt) ||
          right.id.localeCompare(left.id),
      );
  }

  search(principal: Principal, text: string): AnalysisSearchItem[] {
    this.calls.add("search", text);
    const needle = text.toLocaleLowerCase();
    const values: AnalysisSearchItem[] = [];
    for (const project of this.projects.values()) {
      if (
        project.tenantId === principal.tenantId &&
        `${project.id} ${project.name}`.toLocaleLowerCase().includes(needle)
      ) {
        values.push({ type: "Project", value: clone(project) });
      }
    }
    for (const run of this.runs.values()) {
      if (
        run.tenantId === principal.tenantId &&
        `${run.id} ${run.status} ${run.datasetId}`
          .toLocaleLowerCase()
          .includes(needle)
      ) {
        values.push({ type: "AnalysisRun", value: clone(run) });
      }
    }
    return values;
  }

  resolveExternalId(
    principal: Principal,
    externalId: string,
  ): { type: "Project" | "AnalysisRun"; value: Project | Run } | undefined {
    const [prefix, localId] = externalId.split("/", 2);
    if (!prefix || !localId) {
      return undefined;
    }
    if (prefix === "project") {
      const value = this.getProject(principal, localId);
      return value ? { type: "Project", value } : undefined;
    }
    if (prefix === "run") {
      const value = this.getRun(principal, localId);
      return value ? { type: "AnalysisRun", value } : undefined;
    }
    return undefined;
  }

  createProject(
    principal: Principal,
    key: string,
    name: string,
  ): { project: Project; replayed: boolean } {
    const fingerprint = JSON.stringify([principal.tenantId, name]);
    const old = this.idempotency.get(key);
    if (old) {
      if (old.fingerprint !== fingerprint || old.objectType !== "Project") {
        throw new ConflictError("idempotency conflict");
      }
      return { project: clone(this.projects.get(old.objectId)!), replayed: true };
    }

    const id = `proj-${this.projects.size + 1}`;
    const project: Project = {
      id,
      tenantId: principal.tenantId,
      name,
      version: "1",
    };
    this.projects.set(id, project);
    this.idempotency.set(key, {
      fingerprint,
      objectType: "Project",
      objectId: id,
    });
    return { project: clone(project), replayed: false };
  }

  startAnalysis(
    principal: Principal,
    key: string,
    projectId: string,
    datasetId: string,
    algorithm: string,
  ): { run: Run; replayed: boolean } {
    const fingerprint = JSON.stringify([
      principal.tenantId,
      projectId,
      datasetId,
      algorithm,
    ]);
    const old = this.idempotency.get(key);
    if (old) {
      if (old.fingerprint !== fingerprint || old.objectType !== "AnalysisRun") {
        throw new ConflictError("idempotency conflict");
      }
      return { run: clone(this.runs.get(old.objectId)!), replayed: true };
    }
    if (!this.getProject(principal, projectId)) {
      throw new Error("not-found");
    }

    const id = `run-${this.runs.size + 1}`;
    const run: Run = {
      id,
      tenantId: principal.tenantId,
      projectId,
      datasetId,
      status: "QUEUED",
      version: "1",
      createdAt: "2026-08-08T12:00:00Z",
      resultSummary: null,
    };
    this.runs.set(id, run);
    this.events.set(id, [{ sequence: 1, status: "QUEUED" }]);
    this.idempotency.set(key, {
      fingerprint,
      objectType: "AnalysisRun",
      objectId: id,
    });
    return { run: clone(run), replayed: false };
  }

  cancel(principal: Principal, id: string, expectedVersion: string): Run {
    const run = this.runs.get(id);
    if (!run || run.tenantId !== principal.tenantId) {
      throw new Error("not-found");
    }
    if (run.version !== expectedVersion) {
      throw new PreconditionFailed("stale version");
    }
    if (["COMPLETED", "FAILED", "CANCELLED"].includes(run.status)) {
      throw new ConflictError("terminal run");
    }
    run.status = "CANCELLED";
    run.version = String(Number(run.version) + 1);
    return clone(run);
  }

  updates(
    principal: Principal,
    runId: string,
    after: number,
  ): Array<Record<string, unknown>> {
    this.calls.add("updates", runId, String(after));
    const run = this.runs.get(runId);
    if (!run || run.tenantId !== principal.tenantId) {
      return [];
    }
    return (this.events.get(runId) ?? [])
      .filter((event) => Number(event.sequence) > after)
      .map((event) => ({ ...event, run: clone(run) }));
  }
}

export class ArtifactServiceClient {
  readonly calls = new CallLog();
  available = true;
  readonly byRun = new Map<string, Artifact[]>([
    [
      "run-1",
      [
        {
          id: "artifact-1",
          tenantId: "tenant-a",
          runId: "run-1",
          mediaType: "application/json",
          size: 128,
          sha256: "a".repeat(64),
          downloadUrl: "https://artifacts.invalid/a",
        },
      ],
    ],
  ]);

  batchByRun(
    principal: Principal,
    ids: readonly string[],
  ): ReadonlyMap<string, readonly Artifact[]> {
    if (!this.available) {
      throw new DownstreamUnavailable("artifact-service");
    }
    this.calls.add("batchByRun", ...ids);
    return new Map(
      ids.map((id) => [
        id,
        (this.byRun.get(id) ?? [])
          .filter((value) => value.tenantId === principal.tenantId)
          .map(clone),
      ]),
    );
  }

  get(principal: Principal, artifactId: string): Artifact | undefined {
    if (!this.available) {
      throw new DownstreamUnavailable("artifact-service");
    }
    this.calls.add("get", artifactId);
    for (const values of this.byRun.values()) {
      const value = values.find(
        (item) =>
          item.id === artifactId && item.tenantId === principal.tenantId,
      );
      if (value) {
        return clone(value);
      }
    }
    return undefined;
  }

  search(principal: Principal, text: string): Artifact[] {
    if (!this.available) {
      throw new DownstreamUnavailable("artifact-service");
    }
    this.calls.add("search", text);
    const needle = text.toLocaleLowerCase();
    return [...this.byRun.values()]
      .flat()
      .filter(
        (value) =>
          value.tenantId === principal.tenantId &&
          `${value.id} ${value.mediaType} ${value.runId}`
            .toLocaleLowerCase()
            .includes(needle),
      )
      .map(clone);
  }

  resolveExternalId(
    principal: Principal,
    externalId: string,
  ): Artifact | undefined {
    const [prefix, localId] = externalId.split("/", 2);
    return prefix === "artifact" && localId
      ? this.get(principal, localId)
      : undefined;
  }
}

export class NotificationServiceClient {
  readonly calls = new CallLog();
  available = true;
  readonly summaries = new Map<string, Record<string, unknown>>([
    [
      "run-1",
      {
        runId: "run-1",
        tenantId: "tenant-a",
        delivered: 1,
        pending: 0,
        failed: 0,
        observedAt: "2026-08-08T11:59:50Z",
        stalenessSeconds: 10,
      },
    ],
    [
      "run-2",
      {
        runId: "run-2",
        tenantId: "tenant-a",
        delivered: 0,
        pending: 1,
        failed: 0,
        observedAt: "2026-08-08T11:59:45Z",
        stalenessSeconds: 15,
      },
    ],
  ]);

  batchByRun(
    principal: Principal,
    ids: readonly string[],
  ): ReadonlyMap<string, Record<string, unknown>> {
    if (!this.available) {
      throw new DownstreamUnavailable("notification-service");
    }
    this.calls.add("batchByRun", ...ids);
    const output = new Map<string, Record<string, unknown>>();
    for (const id of ids) {
      const value = this.summaries.get(id);
      if (value?.tenantId === principal.tenantId) {
        output.set(id, clone(value));
      }
    }
    return output;
  }
}
