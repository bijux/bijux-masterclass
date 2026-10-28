export interface Pending { readonly deadlineMs: number; readonly attempts: number }
export const pending = new Map<string, Pending>();
