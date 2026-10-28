export function bounded(ms: number): AbortSignal { return AbortSignal.timeout(ms); }
