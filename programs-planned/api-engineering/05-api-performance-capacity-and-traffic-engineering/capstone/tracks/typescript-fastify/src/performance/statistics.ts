export interface SampleSummary {
  count: number;
  minimum: number;
  maximum: number;
  mean: number;
  p50: number;
  p90: number;
  p95: number;
  p99: number;
  quantileAlgorithm: "nearest-rank";
}

function validated(samples: readonly number[]): number[] {
  if (samples.length === 0) throw new Error("at least one sample is required");
  if (samples.some((value) => !Number.isFinite(value))) {
    throw new Error("samples must be finite");
  }
  return [...samples];
}

export function nearestRank(samples: readonly number[], quantile: number): number {
  const values = validated(samples).sort((a, b) => a - b);
  if (!Number.isFinite(quantile) || quantile <= 0 || quantile > 1) {
    throw new Error("quantile must be in (0, 1]");
  }
  const index = Math.ceil(quantile * values.length) - 1;
  const value = values[index];
  if (value === undefined) throw new Error("internal rank failure");
  return value;
}

export function summarize(samples: readonly number[]): SampleSummary {
  const values = validated(samples);
  const sum = values.reduce((left, right) => left + right, 0);
  return {
    count: values.length,
    minimum: Math.min(...values),
    maximum: Math.max(...values),
    mean: sum / values.length,
    p50: nearestRank(values, 0.5),
    p90: nearestRank(values, 0.9),
    p95: nearestRank(values, 0.95),
    p99: nearestRank(values, 0.99),
    quantileAlgorithm: "nearest-rank",
  };
}
