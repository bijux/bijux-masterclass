export class ValidationError extends Error {}
export class Conflict extends Error {}
export class Unauthorized extends Error {}
export class Unavailable extends Error {}
export class DeadlineExceeded extends Error {}

export type RunState =
  | "queued"
  | "running"
  | "completed"
  | "failed"
  | "cancelled";

export interface RequestContext {
  subject: string;
  tenant: string;
  workload: string;
  scopes: ReadonlySet<string>;
  deadlineMs: number;
  nowMs: number;
  traceId: string;
}

export function requireScope(ctx: RequestContext, scope: string): void {
  if (!ctx.scopes.has(scope)) {
    throw new Unauthorized(`missing scope: ${scope}`);
  }
}

export function childContext(
  ctx: RequestContext,
  elapsedMs: number,
  reserveMs = 0,
): RequestContext {
  const nowMs = ctx.nowMs + Math.max(0, elapsedMs);
  if (ctx.deadlineMs - nowMs <= reserveMs) {
    throw new DeadlineExceeded("no remaining deadline budget");
  }
  return {
    ...ctx,
    nowMs,
    deadlineMs: ctx.deadlineMs - reserveMs,
  };
}

export interface RunRecord {
  runId: string;
  tenant: string;
  owner: string;
  datasetId: string;
  attemptId: string;
  state: RunState;
  version: number;
  artifactIds: string[];
}

export interface ArtifactRecord {
  artifactId: string;
  tenant: string;
  runId: string;
  attemptId: string;
  sha256: string;
  content: Uint8Array;
  version: number;
  state: "published" | "orphaned";
}

export interface OperationResult<T> {
  value: T;
  authoritative: boolean;
  partial: boolean;
  warnings: readonly string[];
}
