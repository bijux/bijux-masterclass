/** Release decision logic for schema and runtime evidence. */

import type { CompatibilityDecision } from "./compatibility.js";

export interface ReleaseEvidence {
  compatibility: readonly CompatibilityDecision[];
  activeOperationsValid: boolean;
  budgetsPass: boolean;
  ownershipComplete: boolean;
  oldClientPasses: boolean;
}

export interface ReleaseDecision {
  accepted: boolean;
  classification: "accepted" | "rejected" | "review-required";
  reasons: readonly string[];
}

export function decide(
  evidence: ReleaseEvidence,
): ReleaseDecision {
  const reasons: string[] = [];

  if (
    evidence.compatibility.some(
      (item) => item.classification === "breaking",
    )
  ) {
    reasons.push("breaking-schema-change");
  }
  if (!evidence.activeOperationsValid) {
    reasons.push("active-operation-invalid");
  }
  if (!evidence.budgetsPass) {
    reasons.push("query-budget-regression");
  }
  if (!evidence.ownershipComplete) {
    reasons.push("field-owner-missing");
  }
  if (!evidence.oldClientPasses) {
    reasons.push("old-client-failed");
  }

  if (reasons.length > 0) {
    return {
      accepted: false,
      classification: "rejected",
      reasons,
    };
  }

  if (
    evidence.compatibility.some(
      (item) => item.classification === "review-required",
    )
  ) {
    return {
      accepted: false,
      classification: "review-required",
      reasons: ["manual-consumer-review-required"],
    };
  }

  return {
    accepted: true,
    classification: "accepted",
    reasons: [],
  };
}
