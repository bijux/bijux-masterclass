import { sha256Identity } from "./identity.js";

export type WorkloadModel = "open" | "closed" | "mixed";

export interface WorkloadInput {
  id: string;
  model: WorkloadModel;
  ratePerSecond: number;
  durationSeconds: number;
  datasetId: string;
  requestMix: Record<string, number>;
  maxOutstandingPerClient?: number;
  thinkTimeSeconds?: number;
  annotations?: Record<string, string>;
}

export interface WorkloadSpec extends Required<Omit<WorkloadInput, "annotations">> {
  annotations: Readonly<Record<string, string>>;
  identity: string;
}

export function createWorkloadSpec(input: WorkloadInput): WorkloadSpec {
  if (!input.id.startsWith("WL-")) throw new Error("workload id must start with WL-");
  if (!["open", "closed", "mixed"].includes(input.model)) {
    throw new Error("unsupported workload model");
  }
  if (!Number.isFinite(input.ratePerSecond) || input.ratePerSecond <= 0) {
    throw new Error("rate must be positive and finite");
  }
  if (!Number.isSafeInteger(input.durationSeconds) || input.durationSeconds <= 0) {
    throw new Error("duration must be a positive integer");
  }
  if (!input.datasetId) throw new Error("dataset is required");
  const entries = Object.entries(input.requestMix);
  if (entries.length === 0) throw new Error("request mix is required");
  let total = 0;
  for (const [operation, weight] of entries) {
    if (!operation || !Number.isFinite(weight) || weight <= 0) {
      throw new Error("invalid request mix");
    }
    total += weight;
  }
  if (Math.abs(total - 1) > 1e-9) {
    throw new Error("request mix weights must sum to 1");
  }
  const maxOutstandingPerClient = input.maxOutstandingPerClient ?? 1;
  const thinkTimeSeconds = input.thinkTimeSeconds ?? 0;
  if (!Number.isSafeInteger(maxOutstandingPerClient) || maxOutstandingPerClient <= 0) {
    throw new Error("max outstanding must be positive");
  }
  if (!Number.isFinite(thinkTimeSeconds) || thinkTimeSeconds < 0) {
    throw new Error("think time must be non-negative");
  }
  const semantic = {
    id: input.id,
    model: input.model,
    ratePerSecond: input.ratePerSecond,
    durationSeconds: input.durationSeconds,
    datasetId: input.datasetId,
    requestMix: input.requestMix,
    maxOutstandingPerClient,
    thinkTimeSeconds,
  };
  return {
    ...semantic,
    annotations: Object.freeze({ ...(input.annotations ?? {}) }),
    identity: sha256Identity(semantic),
  };
}

export interface EnvironmentInput {
  runtime: string;
  runtimeVersion: string;
  cpuLogical: number;
  memoryLimitBytes: string;
  processCount: number;
  workerCount: number;
  sourceRevision: string;
  datasetId: string;
  databaseProfile: string;
  featureFlags?: Record<string, boolean>;
}

export interface EnvironmentFingerprint extends EnvironmentInput {
  featureFlags: Record<string, boolean>;
  identity: string;
}

export function createEnvironment(input: EnvironmentInput): EnvironmentFingerprint {
  if (!input.runtime || !input.runtimeVersion) throw new Error("runtime is required");
  for (const value of [input.cpuLogical, input.processCount, input.workerCount]) {
    if (!Number.isSafeInteger(value) || value <= 0) throw new Error("invalid count");
  }
  if (!/^[1-9][0-9]*$/.test(input.memoryLimitBytes)) {
    throw new Error("memoryLimitBytes must be a positive decimal string");
  }
  const semantic = { ...input, featureFlags: input.featureFlags ?? {} };
  return { ...semantic, identity: sha256Identity(semantic) };
}
