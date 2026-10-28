export interface RecordValue { readonly fingerprint: string; readonly jobId: string }
export const records = new Map<string, RecordValue>();
