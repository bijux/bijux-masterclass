/**
 * Reference snapshot of the shape emitted by `openapi-typescript` from
 * `spec/dist/openapi.bundle.yaml`. Run `make clients-generate` to create `schema.generated.d.ts` beside it
 * with the pinned generator's complete output.
 */
export interface paths {
  "/health": { get: operations["getHealth"] };
  "/projects": {
    get: operations["listProjects"];
    post: operations["createProject"];
  };
  "/projects/{projectId}": {
    get: operations["getProject"];
    patch: operations["updateProject"];
  };
  "/projects/{projectId}/datasets": {
    get: operations["listProjectDatasets"];
    post: operations["createDataset"];
  };
  "/datasets/{datasetId}": {
    get: operations["getDataset"];
    delete: operations["deleteDataset"];
  };
  "/datasets/{datasetId}/content": { post: operations["uploadDatasetContent"] };
  "/analysis-runs": {
    get: operations["listAnalysisRuns"];
    post: operations["createAnalysisRun"];
  };
  "/analysis-runs/{runId}": { get: operations["getAnalysisRun"] };
  "/analysis-runs/{runId}/cancellation": { post: operations["cancelAnalysisRun"] };
  "/analysis-runs/{runId}/artifacts": { get: operations["listAnalysisRunArtifacts"] };
  "/analysis-runs/{runId}/events": { get: operations["streamAnalysisRunEvents"] };
  "/artifacts/{artifactId}": { get: operations["getArtifact"] };
  "/webhook-subscriptions": { post: operations["createWebhookSubscription"] };
  "/internal/diagnostics": { get: operations["getDiagnostics"] };
}

export interface components {
  schemas: {
    Project: import("../src/types.js").Project;
    Dataset: import("../src/types.js").Dataset;
    AnalysisRun: import("../src/types.js").AnalysisRun;
    Artifact: import("../src/types.js").Artifact;
    Problem: import("../src/types.js").Problem;
  };
}

export interface operations {
  getHealth: unknown;
  listProjects: unknown;
  createProject: unknown;
  getProject: unknown;
  updateProject: unknown;
  listProjectDatasets: unknown;
  createDataset: unknown;
  getDataset: unknown;
  deleteDataset: unknown;
  uploadDatasetContent: unknown;
  listAnalysisRuns: unknown;
  createAnalysisRun: unknown;
  getAnalysisRun: unknown;
  cancelAnalysisRun: unknown;
  listAnalysisRunArtifacts: unknown;
  streamAnalysisRunEvents: unknown;
  getArtifact: unknown;
  createWebhookSubscription: unknown;
  getDiagnostics: unknown;
}
