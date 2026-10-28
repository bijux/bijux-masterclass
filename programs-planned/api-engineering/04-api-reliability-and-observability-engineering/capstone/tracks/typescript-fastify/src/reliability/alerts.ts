import { burnRate, type SLODefinition, type SLOWindow } from "./slo.js";
export interface BurnRateAlert { readonly id: string; readonly severity: string; readonly longWindowSeconds: number; readonly shortWindowSeconds: number; readonly threshold: number; readonly minimumEvents?: number }
export interface AlertEvaluation { readonly firing: boolean; readonly longBurnRate?: number; readonly shortBurnRate?: number; readonly reason: string }
export function evaluateBurnRateAlert(definition: SLODefinition, alert: BurnRateAlert, longWindow: SLOWindow, shortWindow: SLOWindow): AlertEvaluation {
  if (alert.longWindowSeconds <= alert.shortWindowSeconds) throw new Error("long window must exceed short window");
  const minimum = alert.minimumEvents ?? 1;
  if (longWindow.total < minimum || shortWindow.total < minimum) return { firing: false, reason: "insufficient-traffic" };
  const longBurnRate = burnRate(definition, longWindow)!; const shortBurnRate = burnRate(definition, shortWindow)!;
  const firing = longBurnRate >= alert.threshold && shortBurnRate >= alert.threshold;
  return { firing, longBurnRate, shortBurnRate, reason: firing ? "budget-burning" : "within-alert-threshold" };
}
