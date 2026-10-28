import { createHash } from "node:crypto";
import {
  type AnalysisRun, type Principal, requestFingerprint, etag,
} from "./model.js";

interface IdempotencyRecord {
  readonly fingerprint: string;
  readonly name: string;
}

export class AnalysisStore {
  private readonly runs = new Map<string, AnalysisRun>();
  private readonly requests = new Map<string, IdempotencyRecord>();

  public createRun(input: {
    parent: string;
    requestId: string;
    datasetName: string;
    algorithm: string;
    principal: Principal;
  }): AnalysisRun {
    if (!input.parent.startsWith("projects/")) throw new Error("INVALID_ARGUMENT");
    if (!input.datasetName.startsWith("datasets/")) throw new Error("INVALID_ARGUMENT");
    if (!["qc", "align", "summarize"].includes(input.algorithm)) {
      throw new Error("INVALID_ARGUMENT");
    }
    const fingerprint = requestFingerprint(input);
    const key = `${input.principal.subject}\0${input.requestId}`;
    const existing = this.requests.get(key);
    if (existing !== undefined) {
      if (existing.fingerprint !== fingerprint) throw new Error("ALREADY_EXISTS");
      const replay = this.runs.get(existing.name);
      if (replay === undefined) throw new Error("corrupt idempotency record");
      return replay;
    }
    const digest = createHash("sha256")
      .update(`${input.principal.subject}:${input.requestId}:${fingerprint}`)
      .digest("hex").slice(0, 16);
    const run: AnalysisRun = {
      name: `${input.parent}/runs/r-${digest}`,
      projectName: input.parent,
      datasetName: input.datasetName,
      state: "QUEUED",
      progressPercent: 0,
      revision: 1n,
    };
    this.runs.set(run.name, run);
    this.requests.set(key, { fingerprint, name: run.name });
    return run;
  }

  public getRun(name: string): AnalysisRun {
    const run = this.runs.get(name);
    if (run === undefined) throw new Error("NOT_FOUND");
    return run;
  }

  public cancelRun(name: string, expectedEtag: string): AnalysisRun {
    const run = this.getRun(name);
    if (etag(run) !== expectedEtag) throw new Error("ABORTED");
    if (["COMPLETED", "FAILED"].includes(run.state)) {
      throw new Error("FAILED_PRECONDITION");
    }
    if (run.state === "CANCELLED") return run;
    const updated: AnalysisRun = {
      ...run, state:"CANCELLED", revision:run.revision + 1n,
    };
    this.runs.set(name, updated);
    return updated;
  }

  public etag(name: string): string { return etag(this.getRun(name)); }
}
