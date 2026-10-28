import { createHash } from "node:crypto";

export type RunState =
  | "UNSPECIFIED"
  | "QUEUED"
  | "RUNNING"
  | "COMPLETED"
  | "FAILED"
  | "CANCELLED";

export interface Principal {
  readonly subject: string;
  readonly tenant: string;
  readonly scopes: ReadonlySet<string>;
  readonly workload: "gateway" | "worker";
}

export interface AnalysisRun {
  readonly name: string;
  readonly projectName: string;
  readonly datasetName: string;
  readonly state: RunState;
  readonly progressPercent: number;
  readonly revision: bigint;
  readonly resultSummary?: string;
  readonly failureCode?: string;
}

export function etag(run: AnalysisRun): string {
  return `"run-${run.revision.toString()}"`;
}

export function parseInt64(value: string): bigint {
  if (!/^-?(0|[1-9][0-9]*)$/.test(value)) {
    throw new Error("invalid int64 decimal");
  }
  const parsed = BigInt(value);
  const min = -(1n << 63n);
  const max = (1n << 63n) - 1n;
  if (parsed < min || parsed > max) {
    throw new Error("int64 overflow");
  }
  return parsed;
}

export function requestFingerprint(input: {
  parent: string;
  datasetName: string;
  algorithm: string;
  principal: Principal;
}): string {
  const canonical = JSON.stringify({
    algorithm: input.algorithm,
    dataset_name: input.datasetName,
    parent: input.parent,
    subject: input.principal.subject,
    tenant: input.principal.tenant,
  });
  return createHash("sha256").update(canonical).digest("hex");
}

export function advanceRun(
  run: AnalysisRun,
  next: {
    state: RunState;
    progressPercent: number;
    resultSummary?: string;
    failureCode?: string;
  },
): AnalysisRun {
  if (next.progressPercent < run.progressPercent ||
      next.progressPercent < 0 || next.progressPercent > 100) {
    throw new Error("invalid progress");
  }
  if (["COMPLETED", "FAILED", "CANCELLED"].includes(run.state)) {
    throw new Error("terminal run cannot advance");
  }
  if (next.state === "COMPLETED" && next.progressPercent !== 100) {
    throw new Error("completed run requires 100 percent");
  }
  if (next.state === "FAILED" && !next.failureCode) {
    throw new Error("failed run requires failure code");
  }
  return {
    ...run,
    state: next.state,
    progressPercent: next.progressPercent,
    revision: run.revision + 1n,
    ...(next.resultSummary !== undefined
      ? { resultSummary: next.resultSummary }
      : run.resultSummary !== undefined
        ? { resultSummary: run.resultSummary }
        : {}),
    ...(next.failureCode !== undefined
      ? { failureCode: next.failureCode }
      : run.failureCode !== undefined
        ? { failureCode: run.failureCode }
        : {}),
  };
}
