export type Problem = {
  type: string;
  title: string;
  status: number;
  detail: string;
  instance?: string;
  requestId?: string;
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

export type Dataset = {
  id: string;
  projectId: string;
  ownerId: string;
  name: string;
  source:
    | {
        kind: "local-file";
        fileName: string;
        mediaType: "text/csv" | "application/json" | "application/octet-stream";
      }
    | {
        kind: "remote-object";
        uri: string;
        checksumSha256?: string;
      };
  status: "awaiting-upload" | "ready" | "deleted";
  contentLength: number | null;
  checksumSha256: string | null;
  createdAt: string;
  updatedAt: string;
};

export type UploadReceipt = {
  datasetId: string;
  contentLength: number;
  checksumSha256: string;
  uploadedAt: string;
};

export type AnalysisRun = {
  id: string;
  projectId: string;
  datasetId: string;
  ownerId: string;
  status: "queued" | "running" | "completed" | "failed" | "canceled";
  parameters: {
    algorithm: "quality-summary" | "line-count" | "checksum";
    priority: "normal" | "high";
    labels: Record<string, string>;
  };
  progress: number;
  createdAt: string;
  updatedAt: string;
  completedAt: string | null;
  artifactIds: string[];
};

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

export type WorkflowResult = {
  project: Project & { _etag?: string | null };
  dataset: Dataset;
  upload: UploadReceipt;
  run: AnalysisRun;
  artifacts: Artifact[];
};
