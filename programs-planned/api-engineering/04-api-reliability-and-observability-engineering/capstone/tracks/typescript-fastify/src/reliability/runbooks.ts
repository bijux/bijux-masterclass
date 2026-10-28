export interface Runbook {
  readonly identifier: string;
  readonly title: string;
  readonly owner: string;
  readonly trigger: string;
  readonly customerImpact: string;
  readonly prerequisites: readonly string[];
  readonly immediateActions: readonly string[];
  readonly stopConditions: readonly string[];
  readonly diagnosis: readonly string[];
  readonly mitigation: readonly string[];
  readonly rollback: readonly string[];
  readonly recoveryValidation: readonly string[];
  readonly closureCriteria: readonly string[];
  readonly escalation: readonly string[];
}

const LIST_FIELDS = [
  "prerequisites", "immediateActions", "stopConditions", "diagnosis",
  "mitigation", "rollback", "recoveryValidation", "closureCriteria", "escalation",
] as const;
const TEXT_FIELDS = ["id", "title", "owner", "trigger", "customerImpact"] as const;

export function parseRunbook(value: unknown): Runbook {
  if (value === null || typeof value !== "object" || Array.isArray(value)) {
    throw new Error("runbook must be an object");
  }
  const record = value as Record<string, unknown>;
  for (const field of TEXT_FIELDS) {
    if (typeof record[field] !== "string" || record[field].trim() === "") {
      throw new Error(`runbook field ${field} must be non-empty text`);
    }
  }
  for (const field of LIST_FIELDS) {
    const items = record[field];
    if (!Array.isArray(items) || items.length === 0 ||
        items.some((item) => typeof item !== "string" || item.trim() === "")) {
      throw new Error(`runbook field ${field} must be a non-empty string list`);
    }
  }
  return {
    identifier: record.id as string,
    title: record.title as string,
    owner: record.owner as string,
    trigger: record.trigger as string,
    customerImpact: record.customerImpact as string,
    prerequisites: record.prerequisites as string[],
    immediateActions: record.immediateActions as string[],
    stopConditions: record.stopConditions as string[],
    diagnosis: record.diagnosis as string[],
    mitigation: record.mitigation as string[],
    rollback: record.rollback as string[],
    recoveryValidation: record.recoveryValidation as string[],
    closureCriteria: record.closureCriteria as string[],
    escalation: record.escalation as string[],
  };
}
