import { AnalysisGraphGateway } from "./gateway.js";
import { encodeGlobalId } from "./identity.js";
import type { Principal, RequestContext } from "./model.js";
import { PersistedOperationRegistry } from "./persisted.js";
import { registeredOperationDocuments } from "./registered-operations.js";

export function demoOperations(): PersistedOperationRegistry {
  const registry = new PersistedOperationRegistry();
  for (const [name, document] of Object.entries(registeredOperationDocuments)) {
    registry.register(name, document);
  }
  return registry;
}

export function runTour(): Record<string, unknown> {
  const registry = demoOperations();
  const gateway = new AnalysisGraphGateway(registry);
  const principal: Principal = {
    subject: "learner",
    tenantId: "tenant-a",
    permissions: new Set([
      "PROJECT_READ",
      "PROJECT_WRITE",
      "RUN_READ",
      "RUN_WRITE",
      "ARTIFACT_READ",
      "DELIVERY_READ",
    ]),
  };
  const context: RequestContext = {
    principal,
    requestId: "tour",
    deadlineMs: 1_000,
    clientName: "course",
    nowEpoch: 1_786_147_200,
  };
  const projectId = encodeGlobalId("Project", "proj-1");
  const overview = gateway.execute(
    registry.named("GetProjectOverview").sha256,
    { projectId, first: 2 },
    context,
  );
  const variables = {
    input: {
      idempotencyKey: "ts-tour",
      projectId,
      datasetId: "data-3",
      algorithm: "qc",
    },
  };
  const first = gateway.execute(
    registry.named("StartAnalysis").sha256,
    variables,
    context,
  );
  const second = gateway.execute(
    registry.named("StartAnalysis").sha256,
    variables,
    context,
  );
  const project = overview.data?.project as Record<string, unknown>;
  const connection = project.analysisRuns as Record<string, unknown>;
  const startFirst = first.data?.startAnalysis as Record<string, unknown>;
  const startSecond = second.data?.startAnalysis as Record<string, unknown>;
  return {
    overviewRuns: (connection.edges as unknown[]).length,
    batchCalls: overview.extensions?.batchCalls,
    replayedFirst: startFirst.replayed,
    replayedSecond: startSecond.replayed,
    registeredOperations: Object.keys(registeredOperationDocuments).length,
  };
}
