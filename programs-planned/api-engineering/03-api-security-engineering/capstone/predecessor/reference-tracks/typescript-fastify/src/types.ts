export type ProjectCreate = {
  name: string;
  description?: string;
};

export type ProjectPatch = {
  name?: string;
  description?: string | null;
};

export type Project = {
  id: string;
  ownerId: string;
  name: string;
  description: string | null;
  version: number;
  createdAt: string;
  updatedAt: string;
};

export type LocalFileSource = {
  kind: "local-file";
  fileName: string;
  mediaType: "text/csv" | "application/json" | "application/octet-stream";
};

export type RemoteObjectSource = {
  kind: "remote-object";
  uri: string;
  checksumSha256?: string;
};

export type DatasetSource = LocalFileSource | RemoteObjectSource;

export type DatasetCreate = {
  name: string;
  source: DatasetSource;
};

export type Dataset = {
  id: string;
  projectId: string;
  ownerId: string;
  name: string;
  source: DatasetSource;
  status: "awaiting-upload" | "ready" | "deleted";
  contentLength: number | null;
  checksumSha256: string | null;
  createdAt: string;
  updatedAt: string;
};

export type AnalysisParameters = {
  algorithm: "quality-summary" | "line-count" | "checksum";
  priority?: "normal" | "high";
  labels?: Record<string, string>;
};

export type NormalizedAnalysisParameters = {
  algorithm: "quality-summary" | "line-count" | "checksum";
  priority: "normal" | "high";
  labels: Record<string, string>;
};

export type AnalysisRunCreate = {
  projectId: string;
  datasetId: string;
  parameters: AnalysisParameters;
  callbackUrl?: string;
};

export type RunStatus =
  | "queued"
  | "running"
  | "completed"
  | "failed"
  | "canceled";

export type AnalysisRun = {
  id: string;
  projectId: string;
  datasetId: string;
  ownerId: string;
  status: RunStatus;
  parameters: NormalizedAnalysisParameters;
  progress: number;
  createdAt: string;
  updatedAt: string;
  completedAt: string | null;
  artifactIds: string[];
};

export type ResultSummary = {
  algorithm: "quality-summary" | "line-count" | "checksum";
  artifactCount: number;
};

export type AnalysisRunV12 = AnalysisRun & {
  resultSummary: ResultSummary | null;
};

export type RunRepresentation = AnalysisRun | AnalysisRunV12;

export type Artifact = {
  id: string;
  runId: string;
  ownerId: string;
  name: string;
  mediaType: "application/json" | "text/plain";
  size: number;
  checksumSha256: string;
  createdAt: string;
};

export type WebhookSubscriptionCreate = {
  targetUrl: string;
  eventTypes: Array<"analysis.completed" | "analysis.failed">;
  secret: string;
};

export type WebhookSubscription = {
  id: string;
  ownerId: string;
  targetUrl: string;
  eventTypes: Array<"analysis.completed" | "analysis.failed">;
  secretHint: string;
  createdAt: string;
};

export type RunProgressEvent = {
  eventId: string;
  runId: string;
  status: RunStatus;
  progress: number;
  occurredAt: string;
};

export type RunCompletedEvent = {
  eventId: string;
  eventType: "analysis.completed";
  occurredAt: string;
  run: RunRepresentation;
};

export type Principal = {
  subject: string;
  scopes: ReadonlySet<string>;
  admin: boolean;
};

export type StagedFile = Readonly<{
  temporaryPath: string;
  size: number;
  checksumSha256: string;
  mediaType: string;
}>;

export type ClaimedJob = Readonly<{
  runId: string;
  datasetId: string;
  ownerId: string;
  algorithm: "quality-summary" | "line-count" | "checksum";
  sourceKind: "local-file" | "remote-object";
  source: DatasetSource;
  contentPath: string | null;
  expectedChecksum: string | null;
  attempt: number;
  leaseOwner: string;
  leaseGeneration: number;
}>;

export type ClaimedDelivery = Readonly<{
  deliveryId: string;
  eventId: string;
  deliveryKind: "subscription" | "callback";
  targetUrl: string;
  payload: Record<string, unknown>;
  secret: string;
  attempt: number;
  leaseOwner: string;
  leaseGeneration: number;
}>;
