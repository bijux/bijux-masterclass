import {
  compare,
  decimal,
  divide,
  formatDecimal,
  subtract,
  type DecimalValue,
} from "./decimal.js";

export interface MetricPolicy {
  name: string;
  direction: "lower" | "higher";
  absoluteRegression: string;
  relativeRegression: string;
  hardMinimum?: string;
  hardMaximum?: string;
}

export interface MetricFinding {
  name: string;
  baseline: string;
  candidate: string;
  absoluteChange: string;
  relativeChange?: string;
  passed: boolean;
  reason: string;
}

function abs(value: DecimalValue): DecimalValue {
  return value.units < 0n ? { units: -value.units, scale: value.scale } : value;
}

export function evaluateMetric(
  baselineText: string,
  candidateText: string,
  policy: MetricPolicy,
): MetricFinding {
  const baseline = decimal(baselineText);
  const candidate = decimal(candidateText);
  const absolute = subtract(candidate, baseline);
  const relative =
    baseline.units === 0n ? undefined : divide(absolute, abs(baseline));

  let hardPass = true;
  let hardReason = "";
  if (
    policy.hardMinimum !== undefined &&
    compare(candidate, decimal(policy.hardMinimum)) < 0
  ) {
    hardPass = false;
    hardReason = "below-hard-minimum";
  }
  if (
    policy.hardMaximum !== undefined &&
    compare(candidate, decimal(policy.hardMaximum)) > 0
  ) {
    hardPass = false;
    hardReason = "above-hard-maximum";
  }

  const adverseAbsolute =
    policy.direction === "lower"
      ? absolute
      : { units: -absolute.units, scale: absolute.scale };
  const adverseRelative =
    relative === undefined
      ? undefined
      : policy.direction === "lower"
        ? relative
        : { units: -relative.units, scale: relative.scale };

  const absoluteExceeded =
    compare(adverseAbsolute, decimal(policy.absoluteRegression)) > 0;
  const relativeExceeded =
    adverseRelative === undefined
      ? candidate.units !== 0n
      : compare(adverseRelative, decimal(policy.relativeRegression)) > 0;
  const thresholdPass = !(absoluteExceeded && relativeExceeded);
  const passed = hardPass && thresholdPass;
  return {
    name: policy.name,
    baseline: formatDecimal(baseline),
    candidate: formatDecimal(candidate),
    absoluteChange: formatDecimal(absolute),
    ...(relative === undefined ? {} : { relativeChange: formatDecimal(relative) }),
    passed,
    reason: !hardPass
      ? hardReason
      : !thresholdPass
        ? "regression-threshold"
        : "within-policy",
  };
}
