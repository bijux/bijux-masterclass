/** Field-level authorization policy for the semantic gateway. */

import {
  AuthorizationError,
  type Principal,
} from "./model.js";

const permissions: Readonly<Record<string, string>> = {
  "Query.project": "PROJECT_READ",
  "Query.analysisRun": "RUN_READ",
  "Query.artifact": "ARTIFACT_READ",
  "Query.deliverySummary": "DELIVERY_READ",
  "AnalysisRun.artifacts": "ARTIFACT_READ",
  "AnalysisRun.deliverySummary": "DELIVERY_READ",
  "Mutation.createProject": "PROJECT_WRITE",
  "Mutation.startAnalysis": "RUN_WRITE",
  "Mutation.cancelAnalysis": "RUN_WRITE",
  "Subscription.analysisRunUpdated": "RUN_READ",
};

export function requireField(
  principal: Principal,
  coordinate: string,
  resourceTenant?: string,
): void {
  const required = permissions[coordinate];
  if (required && !principal.permissions.has(required)) {
    throw new AuthorizationError(
      `missing permission for ${coordinate}`,
    );
  }

  if (
    resourceTenant !== undefined &&
    resourceTenant !== principal.tenantId
  ) {
    throw new AuthorizationError("tenant mismatch");
  }
}
