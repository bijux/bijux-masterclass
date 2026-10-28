export interface SLODefinition { readonly id: string; readonly objective: number; readonly windowSeconds: number; readonly description?: string; readonly version?: string }
export interface SLOWindow { readonly good: number; readonly total: number }

export function validateSLO(definition: SLODefinition): void {
  if (!(definition.objective > 0 && definition.objective < 1)) throw new Error("objective must be between zero and one");
  if (definition.windowSeconds <= 0) throw new Error("window must be positive");
  const version = definition.version ?? "1.0";
  if (version.length < 1 || version.length > 40) throw new Error("SLO definition version must contain 1..40 characters");
}
export function bad(window: SLOWindow): number { if (window.good < 0 || window.total < window.good) throw new Error("invalid counts"); return window.total - window.good; }
export function compliance(window: SLOWindow): number | undefined { return window.total === 0 ? undefined : window.good / window.total; }
export function burnRate(definition: SLODefinition, window: SLOWindow): number | undefined {
  validateSLO(definition); if (window.total === 0) return undefined; return (bad(window) / window.total) / (1 - definition.objective);
}
export function budgetRemainingFraction(definition: SLODefinition, window: SLOWindow): number | undefined {
  validateSLO(definition); if (window.total === 0) return undefined;
  const allowed = (1 - definition.objective) * window.total; return (allowed - bad(window)) / allowed;
}
