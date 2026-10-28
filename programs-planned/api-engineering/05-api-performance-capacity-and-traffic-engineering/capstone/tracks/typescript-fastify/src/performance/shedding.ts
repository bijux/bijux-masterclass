export interface ResourceSignals {
  databasePoolFraction: number;
  durableJobFraction: number;
  streamPermitFraction: number;
  storageAvailable: boolean;
  durableDatabaseAvailable: boolean;
}

export interface SheddingDecision {
  stage: number;
  allowedOperations: ReadonlySet<string>;
  reason: string;
}

const CONTROL = new Set(["getRun", "cancelRun", "health", "reconcile"]);
const READS = new Set([...CONTROL, "getProject", "listRuns"]);
const ARTIFACT = new Set([...READS, "downloadArtifact"]);
const ALL = new Set([...ARTIFACT, "submitRun", "uploadDataset", "diagnostics"]);

function decision(stage: number, values: ReadonlySet<string>, reason: string): SheddingDecision {
  return { stage, allowedOperations: new Set(values), reason };
}

export function chooseShedding(signals: ResourceSignals): SheddingDecision {
  for (const value of [
    signals.databasePoolFraction,
    signals.durableJobFraction,
    signals.streamPermitFraction,
  ]) {
    if (!Number.isFinite(value) || value < 0 || value > 1) {
      throw new Error("resource fractions must be in [0, 1]");
    }
  }
  if (!signals.durableDatabaseAvailable) {
    return decision(5, new Set([...CONTROL].filter((item) => item !== "reconcile")), "database-unavailable");
  }
  if (!signals.storageAvailable) return decision(4, READS, "storage-unavailable");
  if (signals.durableJobFraction >= 0.95) return decision(3, ARTIFACT, "job-capacity");
  if (signals.streamPermitFraction >= 0.95) {
    return decision(2, new Set([...READS, "submitRun"]), "stream-capacity");
  }
  if (signals.databasePoolFraction >= 0.85) {
    return decision(1, new Set([...ALL].filter((item) => item !== "diagnostics")), "database-pressure");
  }
  return decision(0, ALL, "normal");
}
