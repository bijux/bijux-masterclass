import { compareObjectSchemas } from "./evolution.js";

export interface ReleaseDecision { status: "accepted" | "review-required" | "rejected"; reasons: readonly string[] }

export function evaluateEventRelease(oldSchema: Record<string, any>, newSchema: Record<string, any>, gates: { replaySafe: boolean; catalogComplete: boolean; contractValid: boolean; securityValid?: boolean; reliabilityReady?: boolean }): ReleaseDecision {
  const reasons: string[] = [];
  const securityValid = gates.securityValid ?? true;
  const reliabilityReady = gates.reliabilityReady ?? true;
  if (!gates.contractValid) reasons.push("AsyncAPI contract is invalid");
  const report = compareObjectSchemas(oldSchema, newSchema);
  reasons.push(...report.issues.map((issue) => `${issue.severity}: ${issue.path}: ${issue.message}`));
  if (!gates.replaySafe) reasons.push("candidate is not replay safe");
  if (!gates.catalogComplete) reasons.push("event catalogue is incomplete");
  if (!securityValid) reasons.push("event security policy is not satisfied");
  if (!reliabilityReady) reasons.push("consumer reliability evidence is incomplete");
  if (!gates.contractValid || report.status === "rejected" || !gates.replaySafe || !gates.catalogComplete || !securityValid || !reliabilityReady) return { status: "rejected", reasons };
  if (report.status === "review-required") return { status: "review-required", reasons };
  return { status: "accepted", reasons };
}
