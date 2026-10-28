import type { EventEnvelope } from "./envelope.js";

export interface ReplayPlan {
  readonly replayId: string;
  readonly consumer: string;
  readonly mode: "dry-run" | "apply";
  readonly allowedTypes: ReadonlySet<string>;
  readonly maximumEvents: number;
  readonly sideEffects: "disabled";
  readonly tenantId?: string;
}

export interface ReplayReport { readonly selected: number; readonly applied: number; readonly skipped: number; readonly wouldApply: number }

export function executeReplay(plan: ReplayPlan, events: readonly EventEnvelope[], handler: (event: EventEnvelope, dryRun: boolean) => boolean): ReplayReport {
  if (!Number.isSafeInteger(plan.maximumEvents) || plan.maximumEvents <= 0) throw new Error("maximumEvents must be positive");
  let selected = 0, applied = 0, skipped = 0, wouldApply = 0;
  for (const event of events) {
    if (!plan.allowedTypes.has(event.type)) continue;
    if (plan.tenantId !== undefined && event.tenantid !== plan.tenantId) continue;
    selected += 1;
    if (selected > plan.maximumEvents) throw new Error("replay event bound exceeded");
    if (plan.mode === "dry-run") { if (handler(event, true)) wouldApply += 1; }
    else if (handler(event, false)) applied += 1;
    else skipped += 1;
  }
  return { selected, applied, skipped, wouldApply };
}
