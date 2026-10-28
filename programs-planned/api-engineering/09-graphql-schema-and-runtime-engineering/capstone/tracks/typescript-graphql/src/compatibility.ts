/** Directional schema-change classification for Course 9 release gates. */

export type Classification =
  | "breaking"
  | "review-required"
  | "additive";

export interface SchemaChange {
  kind: string;
  coordinate: string;
  activeOperationUses?: boolean;
}

export interface CompatibilityDecision {
  classification: Classification;
  reason: string;
}

const breakingChanges = new Set([
  "remove-field",
  "remove-type",
  "add-required-argument",
  "add-required-input-field",
  "remove-enum-value",
  "output-nonnull-to-nullable",
]);

const reviewRequiredChanges = new Set([
  "add-enum-value",
  "add-union-member",
  "add-interface-implementation",
  "output-nullable-to-nonnull",
  "increase-fanout",
]);

const additiveChanges = new Set([
  "add-optional-field",
  "add-optional-argument",
  "deprecate-field",
]);

export function classify(change: SchemaChange): CompatibilityDecision {
  if (breakingChanges.has(change.kind)) {
    return { classification: "breaking", reason: change.kind };
  }
  if (reviewRequiredChanges.has(change.kind)) {
    return { classification: "review-required", reason: change.kind };
  }
  if (additiveChanges.has(change.kind)) {
    return { classification: "additive", reason: change.kind };
  }
  return {
    classification: "review-required",
    reason: "unknown change",
  };
}
