export interface Transition { from: string; to: string; requires: string[]; }
export interface LifecyclePolicy { transitions: Transition[]; minimumNoticeDays: number; }
export interface LifecycleDecision { allowed: boolean; reason: string; missing?: string[]; }

export function evaluateTransition(input: {
  current: string; target: string; evidence: string[]; policy: LifecyclePolicy;
  blockingConsumers?: number; now?: Date; noticeEnd?: Date;
}): LifecycleDecision {
  const transition = input.policy.transitions.find((t) => t.from === input.current && t.to === input.target);
  if (!transition) return { allowed: false, reason: "transition-not-allowed" };
  const present = new Set(input.evidence);
  const missing = transition.requires.filter((item) => !present.has(item)).sort();
  if (missing.length) return { allowed: false, reason: "missing-evidence", missing };
  if (input.target === "retired" && (input.blockingConsumers ?? 0) > 0) return { allowed: false, reason: "blocking-consumers" };
  if (input.target === "retired" && input.now && input.noticeEnd && input.now < input.noticeEnd) return { allowed: false, reason: "notice-period-open" };
  return { allowed: true, reason: "allowed" };
}

export function deprecationImpact(consumers: Record<string, unknown>[], apiRef: string, version: string) {
  const affected = consumers.filter((c) => c.apiRef === apiRef && c.version === version && c.environment === "production");
  const blockers = affected.filter((c) => ["high","critical"].includes(String(c.criticality)) || c.migrationStatus !== "complete");
  return { apiRef, version, affectedConsumers: affected.map((c) => c.id), blockingConsumers: blockers.map((c) => c.id), retirementDecision: blockers.length ? "blocked" : "eligible" };
}
