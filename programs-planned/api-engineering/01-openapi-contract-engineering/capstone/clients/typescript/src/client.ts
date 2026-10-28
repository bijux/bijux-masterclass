import { readFile } from "node:fs/promises";
import { basename, extname } from "node:path";

import type {
  AnalysisRun,
  Artifact,
  Dataset,
  Problem,
  Project,
  UploadReceipt,
  WorkflowResult,
} from "./types.js";

export class ApiError extends Error {
  public readonly status: number;
  public readonly problemType: string;
  public readonly requestId: string | undefined;

  public constructor(problem: Problem) {
    super(`${problem.status} ${problem.title}: ${problem.detail}${problem.requestId ? ` [${problem.requestId}]` : ""}`);
    this.name = "ApiError";
    this.status = problem.status;
    this.problemType = problem.type;
    this.requestId = problem.requestId;
  }
}

export type ClientOptions = {
  bearerToken?: string;
  apiKey?: string;
  fetch?: typeof globalThis.fetch;
};

export class AnalysisClient {
  private readonly baseUrl: string;
  private readonly authHeaders: Readonly<Record<string, string>>;
  private readonly fetcher: typeof globalThis.fetch;

  public constructor(baseUrl: string, options: ClientOptions) {
    const hasBearer = Boolean(options.bearerToken);
    const hasApiKey = Boolean(options.apiKey);
    if (hasBearer === hasApiKey) {
      throw new TypeError("configure exactly one of bearerToken or apiKey");
    }
    this.baseUrl = baseUrl.replace(/\/$/, "");
    this.authHeaders = hasBearer
      ? { Authorization: `Bearer ${String(options.bearerToken)}` }
      : { "X-API-Key": String(options.apiKey) };
    this.fetcher = options.fetch ?? globalThis.fetch;
  }

  private async request<T>(path: string, init: RequestInit = {}): Promise<{ body: T; response: Response }> {
    const headers = new Headers(init.headers);
    for (const [name, value] of Object.entries(this.authHeaders)) {
      headers.set(name, value);
    }
    const response = await this.fetcher(`${this.baseUrl}${path}`, { ...init, headers });
    if (!response.ok) {
      const contentType = response.headers.get("content-type") ?? "";
      if (contentType.includes("application/problem+json")) {
        throw new ApiError((await response.json()) as Problem);
      }
      throw new Error(`${response.status} ${response.statusText}: ${await response.text()}`);
    }
    const body = response.status === 204 ? (undefined as T) : ((await response.json()) as T);
    return { body, response };
  }

  public async health(): Promise<Record<string, unknown>> {
    return (await this.request<Record<string, unknown>>("/health")).body;
  }

  public async createProject(name: string, description?: string): Promise<Project & { _etag?: string | null }> {
    const payload: { name: string; description?: string } = { name };
    if (description !== undefined) payload.description = description;
    const { body, response } = await this.request<Project>("/projects", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    return { ...body, _etag: response.headers.get("etag") };
  }

  public async updateProject(
    projectId: string,
    etag: string,
    patch: { name?: string; description?: string | null },
  ): Promise<Project & { _etag?: string | null }> {
    const { body, response } = await this.request<Project>(`/projects/${encodeURIComponent(projectId)}`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/merge-patch+json",
        "If-Match": etag,
      },
      body: JSON.stringify(patch),
    });
    return { ...body, _etag: response.headers.get("etag") };
  }

  public async registerLocalDataset(
    projectId: string,
    name: string,
    fileName: string,
    mediaType: "text/csv" | "application/json" | "application/octet-stream" = "text/csv",
  ): Promise<Dataset> {
    return (
      await this.request<Dataset>(`/projects/${encodeURIComponent(projectId)}/datasets`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name,
          source: { kind: "local-file", fileName, mediaType },
        }),
      })
    ).body;
  }

  public async uploadDatasetContent(
    datasetId: string,
    content: Blob,
    fileName = "dataset.csv",
  ): Promise<UploadReceipt> {
    const body = new FormData();
    body.set("file", content, fileName);
    return (
      await this.request<UploadReceipt>(`/datasets/${encodeURIComponent(datasetId)}/content`, {
        method: "POST",
        body,
      })
    ).body;
  }

  public async startRun(
    projectId: string,
    datasetId: string,
    idempotencyKey: string,
    algorithm: "quality-summary" | "line-count" | "checksum" = "quality-summary",
  ): Promise<AnalysisRun & { _replay?: boolean; _location?: string | null }> {
    const { body, response } = await this.request<AnalysisRun>("/analysis-runs", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Idempotency-Key": idempotencyKey,
      },
      body: JSON.stringify({
        projectId,
        datasetId,
        parameters: { algorithm, priority: "normal" },
      }),
    });
    return {
      ...body,
      _replay: response.headers.get("idempotent-replay") === "true",
      _location: response.headers.get("location"),
    };
  }

  public async getRun(runId: string): Promise<AnalysisRun> {
    return (await this.request<AnalysisRun>(`/analysis-runs/${encodeURIComponent(runId)}`)).body;
  }

  public async waitForRun(runId: string, maxPolls = 10): Promise<AnalysisRun> {
    for (let poll = 0; poll < maxPolls; poll += 1) {
      const run = await this.getRun(runId);
      if (["completed", "failed", "canceled"].includes(run.status)) return run;
    }
    throw new Error(`run ${runId} did not reach a terminal state`);
  }

  public async listArtifacts(runId: string): Promise<Artifact[]> {
    const page = await this.request<{ items: Artifact[] }>(
      `/analysis-runs/${encodeURIComponent(runId)}/artifacts`,
    );
    return page.body.items;
  }

  public async completeWorkflow(
    projectName: string,
    datasetPath: string,
    idempotencyKey: string,
  ): Promise<WorkflowResult> {
    const bytes = await readFile(datasetPath);
    const fileName = basename(datasetPath);
    const mediaType = extname(fileName) === ".json" ? "application/json" : "text/csv";
    const project = await this.createProject(projectName);
    const dataset = await this.registerLocalDataset(project.id, fileName.replace(/\.[^.]+$/, ""), fileName, mediaType);
    const upload = await this.uploadDatasetContent(dataset.id, new Blob([bytes], { type: mediaType }), fileName);
    const accepted = await this.startRun(project.id, dataset.id, idempotencyKey);
    const run = await this.waitForRun(accepted.id);
    const artifacts = await this.listArtifacts(run.id);
    return { project, dataset, upload, run, artifacts };
  }
}
