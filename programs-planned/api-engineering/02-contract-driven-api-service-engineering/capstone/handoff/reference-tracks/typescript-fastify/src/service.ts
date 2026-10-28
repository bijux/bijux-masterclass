import type { MultipartFile } from "@fastify/multipart";

import { FileSystemArtifactStore } from "./artifacts.js";
import { parseCursor } from "./domain.js";
import { ApiProblem } from "./problems.js";
import { PostgresRepository } from "./repository.js";
import { validateDestination } from "./webhooks.js";
import type {
  AnalysisRunCreate,
  DatasetCreate,
  Principal,
  ProjectCreate,
  ProjectPatch,
  WebhookSubscriptionCreate,
} from "./types.js";

const ALLOWED_UPLOAD_MEDIA_TYPES = new Set([
  "text/csv",
  "application/json",
  "application/octet-stream",
]);

/** Framework-independent application use cases. */
export class AnalysisService {
  public constructor(
    public readonly repository: PostgresRepository,
    private readonly artifacts: FileSystemArtifactStore,
    private readonly uploadLimit: number,
  ) {}

  public listProjects(
    principal: Principal,
    limit: number,
    cursor: string | undefined,
    name: string | undefined,
  ) {
    return this.repository.listProjects(
      principal,
      limit,
      parseCursor(cursor),
      name,
    );
  }

  public createProject(principal: Principal, body: ProjectCreate) {
    return this.repository.createProject(principal, body);
  }

  public getProject(principal: Principal, projectId: string) {
    return this.repository.getProject(principal, projectId);
  }

  public updateProject(
    principal: Principal,
    projectId: string,
    ifMatch: string | undefined,
    body: ProjectPatch,
  ) {
    return this.repository.updateProject(
      principal,
      projectId,
      ifMatch,
      body,
    );
  }

  public listDatasets(
    principal: Principal,
    projectId: string,
    limit: number,
    cursor: string | undefined,
    status: string | undefined,
  ) {
    return this.repository.listDatasets(
      principal,
      projectId,
      limit,
      parseCursor(cursor),
      status,
    );
  }

  public createDataset(
    principal: Principal,
    projectId: string,
    body: DatasetCreate,
  ) {
    return this.repository.createDataset(principal, projectId, body);
  }

  public getDataset(principal: Principal, datasetId: string) {
    return this.repository.getDataset(principal, datasetId);
  }

  public deleteDataset(principal: Principal, datasetId: string) {
    return this.repository.deleteDataset(principal, datasetId);
  }

  public async uploadDataset(
    principal: Principal,
    datasetId: string,
    part: MultipartFile,
  ) {
    const mediaType = part.mimetype.split(";", 1)[0]!.trim().toLowerCase();
    if (!ALLOWED_UPLOAD_MEDIA_TYPES.has(mediaType)) {
      throw new ApiProblem(
        415,
        "Unsupported media type",
        `Unsupported uploaded media type: ${mediaType || "<missing>"}.`,
        "unsupported-media-type",
      );
    }

    const staged = await this.artifacts.stageStream(
      part.file,
      mediaType,
      this.uploadLimit,
    );
    const storageKey =
      `datasets/${staged.checksumSha256.slice(0, 2)}/` +
      staged.checksumSha256;

    // Publishing first may leave an unreferenced content-addressed object if
    // the following transaction fails, but never a dangling database pointer.
    // The orphan audit is the compensating mechanism.
    await this.artifacts.publish(staged, storageKey);
    return this.repository.attachUploadedContent(
      principal,
      datasetId,
      staged,
      storageKey,
    );
  }

  public listRuns(
    principal: Principal,
    limit: number,
    cursor: string | undefined,
    status: string | undefined,
  ) {
    return this.repository.listRuns(
      principal,
      limit,
      parseCursor(cursor),
      status,
    );
  }

  public createRun(
    principal: Principal,
    idempotencyKey: string,
    body: AnalysisRunCreate,
  ) {
    if (body.callbackUrl !== undefined) validateDestination(body.callbackUrl);
    return this.repository.createRunIdempotently(
      principal,
      idempotencyKey,
      body,
    );
  }

  public getRun(principal: Principal, runId: string) {
    return this.repository.getRun(principal, runId);
  }

  public cancelRun(principal: Principal, runId: string) {
    return this.repository.cancelRun(principal, runId);
  }

  public listArtifacts(principal: Principal, runId: string) {
    return this.repository.listArtifacts(principal, runId);
  }

  public getArtifact(principal: Principal, artifactId: string) {
    return this.repository.getArtifact(principal, artifactId);
  }

  public async artifactFile(principal: Principal, artifactId: string) {
    const artifact = await this.repository.getArtifact(principal, artifactId);
    const storageKey = await this.repository.artifactStorageKey(
      principal,
      artifactId,
    );
    const path = await this.artifacts.pathFor(
      storageKey,
      artifact.checksumSha256,
    );
    return { artifact, path };
  }

  public events(
    principal: Principal,
    runId: string,
    afterPosition = "0",
  ) {
    return this.repository.progressEvents(
      principal,
      runId,
      afterPosition,
    );
  }

  public createSubscription(
    principal: Principal,
    body: WebhookSubscriptionCreate,
  ) {
    validateDestination(body.targetUrl);
    return this.repository.createSubscription(principal, body);
  }
}
