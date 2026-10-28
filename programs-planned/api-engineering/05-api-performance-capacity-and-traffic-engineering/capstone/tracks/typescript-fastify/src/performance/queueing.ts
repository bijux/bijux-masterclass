export interface LittleLawResult {
  throughputPerSecond: number;
  meanTimeSeconds: number;
  meanInSystem: number;
  unit: string;
}

export function littleLaw(input: {
  throughputPerSecond: number;
  meanTimeSeconds: number;
  unit?: string;
}): LittleLawResult {
  if (
    !Number.isFinite(input.throughputPerSecond) ||
    !Number.isFinite(input.meanTimeSeconds) ||
    input.throughputPerSecond < 0 ||
    input.meanTimeSeconds < 0
  ) {
    throw new Error("invalid Little's Law inputs");
  }
  return {
    throughputPerSecond: input.throughputPerSecond,
    meanTimeSeconds: input.meanTimeSeconds,
    meanInSystem: input.throughputPerSecond * input.meanTimeSeconds,
    unit: input.unit ?? "work-items",
  };
}

export function mm1Approximation(
  arrivalRate: number,
  serviceRate: number,
): { utilization: number; meanTimeSeconds: number; meanInSystem: number } {
  if (
    !Number.isFinite(arrivalRate) ||
    !Number.isFinite(serviceRate) ||
    arrivalRate < 0 ||
    serviceRate <= 0 ||
    arrivalRate >= serviceRate
  ) {
    throw new Error("M/M/1 steady state requires 0 <= arrival < service");
  }
  const meanTimeSeconds = 1 / (serviceRate - arrivalRate);
  return {
    utilization: arrivalRate / serviceRate,
    meanTimeSeconds,
    meanInSystem: arrivalRate * meanTimeSeconds,
  };
}
