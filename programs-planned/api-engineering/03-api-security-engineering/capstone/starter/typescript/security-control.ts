export interface SecurityDecision { readonly allowed: boolean; readonly reason: string }
export function evaluateUntrustedInput(_value: unknown): SecurityDecision {
  throw new Error("implement from the module requirement and tests");
}
