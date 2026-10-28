export interface ScheduledArrival {
  sequence: number;
  scheduledNs: bigint;
}

export function openSchedule(
  ratePerSecond: number,
  durationSeconds: number,
  startNs = 0n,
): ScheduledArrival[] {
  if (!Number.isFinite(ratePerSecond) || ratePerSecond <= 0) {
    throw new Error("rate must be positive");
  }
  if (!Number.isFinite(durationSeconds) || durationSeconds <= 0) {
    throw new Error("duration must be positive");
  }
  const count = Math.floor(ratePerSecond * durationSeconds + 1e-12);
  const interval = 1_000_000_000 / ratePerSecond;
  return Array.from({ length: count }, (_, sequence) => ({
    sequence,
    scheduledNs: startNs + BigInt(Math.round(sequence * interval)),
  }));
}

export function estimatedClosedThroughput(
  users: number,
  meanResponseSeconds: number,
  thinkTimeSeconds = 0,
): number {
  if (!Number.isSafeInteger(users) || users <= 0) throw new Error("invalid users");
  const cycle = meanResponseSeconds + thinkTimeSeconds;
  if (!Number.isFinite(cycle) || cycle <= 0) throw new Error("invalid cycle");
  return users / cycle;
}
