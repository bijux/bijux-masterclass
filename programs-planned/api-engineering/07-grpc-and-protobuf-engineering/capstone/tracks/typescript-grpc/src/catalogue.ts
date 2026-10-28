export type Shape = "unary" | "server-stream" | "client-stream" | "bidi-stream";

export interface MethodDeclaration {
  readonly path: string;
  readonly shape: Shape;
  readonly owner: string;
  readonly stateOwner: string;
  readonly deadlineOwner: string;
  readonly retry: "none" | "safe-read" | "durable-idempotency" | "resume";
  readonly requiredScope: string;
}

export const METHODS: readonly MethodDeclaration[] = [
  {
    path: "/bijux.analysis.v1.AnalysisControlService/CreateRun",
    shape: "unary", owner: "analysis-control", stateOwner: "analysis-control",
    deadlineOwner: "edge", retry: "durable-idempotency", requiredScope: "runs:write",
  },
  {
    path: "/bijux.analysis.v1.AnalysisControlService/GetRun",
    shape: "unary", owner: "analysis-control", stateOwner: "analysis-control",
    deadlineOwner: "caller", retry: "safe-read", requiredScope: "runs:read",
  },
  {
    path: "/bijux.analysis.v1.AnalysisControlService/CancelRun",
    shape: "unary", owner: "analysis-control", stateOwner: "analysis-control",
    deadlineOwner: "edge", retry: "durable-idempotency", requiredScope: "runs:write",
  },
  {
    path: "/bijux.analysis.v1.AnalysisControlService/WatchRun",
    shape: "server-stream", owner: "analysis-control", stateOwner: "analysis-control",
    deadlineOwner: "subscriber", retry: "resume", requiredScope: "runs:read",
  },
  {
    path: "/bijux.analysis.v1.DatasetTransferService/UploadDataset",
    shape: "client-stream", owner: "dataset-transfer", stateOwner: "analysis-control",
    deadlineOwner: "caller", retry: "durable-idempotency", requiredScope: "datasets:write",
  },
  {
    path: "/bijux.analysis.v1.DatasetTransferService/DownloadArtifact",
    shape: "server-stream", owner: "dataset-transfer", stateOwner: "analysis-control",
    deadlineOwner: "caller", retry: "resume", requiredScope: "artifacts:read",
  },
  {
    path: "/bijux.analysis.v1.WorkerPlaneService/Work",
    shape: "bidi-stream", owner: "worker-plane", stateOwner: "analysis-control",
    deadlineOwner: "worker-session", retry: "resume", requiredScope: "worker:connect",
  },
] as const;

export function validateCatalogue(): void {
  const paths = new Set<string>();
  for (const method of METHODS) {
    if (paths.has(method.path)) throw new Error(`duplicate method ${method.path}`);
    paths.add(method.path);
    if (!method.path.startsWith("/bijux.analysis.v1.")) {
      throw new Error(`unexpected method package ${method.path}`);
    }
  }
}
