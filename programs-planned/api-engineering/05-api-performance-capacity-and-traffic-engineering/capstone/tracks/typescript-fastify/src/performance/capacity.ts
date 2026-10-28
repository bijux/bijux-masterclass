import {
  add,
  compare,
  decimal,
  divide,
  formatDecimal,
  multiply,
  subtract,
  type DecimalValue,
} from "./decimal.js";

const ZERO = decimal("0");
const ONE = decimal("1");

export function cpuDemand(input: {
  cores: DecimalValue;
  utilization: DecimalValue;
  intervalSeconds: DecimalValue;
  completions: DecimalValue;
}): DecimalValue {
  if (
    compare(input.cores, ZERO) <= 0 ||
    compare(input.intervalSeconds, ZERO) <= 0 ||
    compare(input.completions, ZERO) <= 0 ||
    compare(input.utilization, ZERO) < 0 ||
    compare(input.utilization, ONE) > 0
  ) {
    throw new Error("invalid CPU demand inputs");
  }
  return divide(
    multiply(multiply(input.cores, input.utilization), input.intervalSeconds),
    input.completions,
  );
}

export function utilizationFromDemand(input: {
  arrivalRate: DecimalValue;
  demandPerCompletion: DecimalValue;
  capacityUnits: DecimalValue;
}): DecimalValue {
  if (
    compare(input.arrivalRate, ZERO) < 0 ||
    compare(input.demandPerCompletion, ZERO) < 0 ||
    compare(input.capacityUnits, ZERO) <= 0
  ) {
    throw new Error("invalid utilization inputs");
  }
  return divide(
    multiply(input.arrivalRate, input.demandPerCompletion),
    input.capacityUnits,
  );
}

export function backlogDrainSeconds(input: {
  backlog: DecimalValue;
  completionRate: DecimalValue;
  arrivalRate: DecimalValue;
}): DecimalValue {
  if (
    compare(input.backlog, ZERO) < 0 ||
    compare(input.completionRate, ZERO) < 0 ||
    compare(input.arrivalRate, ZERO) < 0
  ) {
    throw new Error("rates and backlog must be non-negative");
  }
  const surplus = subtract(input.completionRate, input.arrivalRate);
  if (compare(surplus, ZERO) <= 0) {
    throw new Error("backlog cannot drain when completion <= arrival");
  }
  return divide(input.backlog, surplus);
}

export interface WorkloadDemand {
  id: string;
  ratePerSecond: string;
  resourceDemand: Record<string, string>;
}

export interface ResourceCapacity {
  id: string;
  capacityUnits: string;
  targetUtilization: string;
  costPerHour?: string;
}

export interface ResourceResult {
  id: string;
  utilization: string;
  targetUtilization: string;
  headroomFraction: string;
  withinTarget: boolean;
}

export function evaluateCapacity(
  workloads: readonly WorkloadDemand[],
  resources: readonly ResourceCapacity[],
): { resources: ResourceResult[]; firstBottleneck?: string } {
  const results: ResourceResult[] = resources.map((resource) => {
    const capacity = decimal(resource.capacityUnits);
    const target = decimal(resource.targetUtilization);
    if (compare(capacity, ZERO) <= 0 || compare(target, ZERO) <= 0 || compare(target, ONE) > 0) {
      throw new Error("invalid resource capacity");
    }
    let total = ZERO;
    for (const workload of workloads) {
      const rate = decimal(workload.ratePerSecond);
      const demand = decimal(workload.resourceDemand[resource.id] ?? "0");
      if (compare(rate, ZERO) < 0 || compare(demand, ZERO) < 0) {
        throw new Error("resource demand cannot be negative");
      }
      total = add(total, multiply(rate, demand));
    }
    const utilization = divide(total, capacity);
    const headroom = divide(subtract(target, utilization), target);
    return {
      id: resource.id,
      utilization: formatDecimal(utilization),
      targetUtilization: formatDecimal(target),
      headroomFraction: formatDecimal(headroom),
      withinTarget: compare(utilization, target) <= 0,
    };
  });
  const ordered = [...results].sort((left, right) => {
    const leftRatio = divide(decimal(left.utilization), decimal(left.targetUtilization));
    const rightRatio = divide(decimal(right.utilization), decimal(right.targetUtilization));
    const cmp = compare(rightRatio, leftRatio);
    return cmp !== 0 ? cmp : right.id.localeCompare(left.id);
  });
  const first = ordered[0]?.id;
  return first === undefined ? { resources: results } : { resources: results, firstBottleneck: first };
}

export function storageBytes(input: {
  dailyObjects: DecimalValue;
  meanObjectBytes: DecimalValue;
  retentionDays: DecimalValue;
  replicationFactor?: DecimalValue;
  overheadFraction?: DecimalValue;
}): DecimalValue {
  const replication = input.replicationFactor ?? ONE;
  const overhead = input.overheadFraction ?? ZERO;
  if (
    compare(input.dailyObjects, ZERO) < 0 ||
    compare(input.meanObjectBytes, ZERO) < 0 ||
    compare(input.retentionDays, ZERO) < 0 ||
    compare(replication, ZERO) <= 0 ||
    compare(overhead, ZERO) < 0
  ) {
    throw new Error("invalid storage inputs");
  }
  return multiply(
    multiply(
      multiply(input.dailyObjects, input.meanObjectBytes),
      input.retentionDays,
    ),
    multiply(replication, add(ONE, overhead)),
  );
}

export { decimal, formatDecimal };
