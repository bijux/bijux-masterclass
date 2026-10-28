export interface PolicyValues { readonly maxItems: number; readonly retentionDays: number }
export function validatePositiveInteger(value: unknown, name: string): number {
  if (typeof value !== 'number' || !Number.isSafeInteger(value) || value <= 0) throw new Error(`${name} must be a positive safe integer`);
  return value;
}
export function createDefaultPolicy(values: PolicyValues): Readonly<PolicyValues> {
  return Object.freeze({ maxItems: validatePositiveInteger(values.maxItems, 'maxItems'), retentionDays: validatePositiveInteger(values.retentionDays, 'retentionDays') });
}
