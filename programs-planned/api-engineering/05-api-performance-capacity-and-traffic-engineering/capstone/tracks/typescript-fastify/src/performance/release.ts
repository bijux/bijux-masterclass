import { evaluateMetric, type MetricFinding, type MetricPolicy } from "./regression.js";

export interface GateFinding {
  name: string;
  status: "passed" | "failed" | "inconclusive";
  reasons: string[];
}

export interface ReleaseDecision {
  status: "accepted" | "rejected" | "inconclusive";
  gates: GateFinding[];
  metrics: MetricFinding[];
}

interface Envelope {
  profileVersion: string;
  workloadHash: string;
  environmentHash: string;
  correctness: { passed: boolean };
  outcomes: {
    offered: number;
    started: number;
    admitted: number;
    completed: number;
    rejected: number;
    failed: number;
    missing: number;
  };
  summary: Record<string, string>;
}

export function evaluateRelease(
  baseline: Envelope,
  candidate: Envelope,
  policy: { metrics: MetricPolicy[] },
): ReleaseDecision {
  const gates: GateFinding[] = [];
  const mismatch: string[] = [];
  for (const field of ["workloadHash", "environmentHash", "profileVersion"] as const) {
    if (baseline[field] !== candidate[field]) mismatch.push(field);
  }
  gates.push({
    name: "comparability",
    status: mismatch.length === 0 ? "passed" : "inconclusive",
    reasons: mismatch,
  });

  if (!baseline.correctness.passed) throw new Error("baseline correctness must pass");
  gates.push({
    name: "correctness",
    status: candidate.correctness.passed ? "passed" : "failed",
    reasons: candidate.correctness.passed ? [] : ["candidate-correctness"],
  });

  const coverageReasons: string[] = [];
  if (candidate.outcomes.offered <= 0) coverageReasons.push("offered");
  if (candidate.outcomes.started !== candidate.outcomes.offered) {
    coverageReasons.push("schedule-coverage");
  }
  if (candidate.outcomes.missing !== 0) coverageReasons.push("missing-outcomes");
  gates.push({
    name: "coverage",
    status: coverageReasons.length === 0 ? "passed" : "failed",
    reasons: coverageReasons,
  });

  const metrics = policy.metrics.map((metric) => {
    const baselineValue = baseline.summary[metric.name];
    const candidateValue = candidate.summary[metric.name];
    if (baselineValue === undefined || candidateValue === undefined) {
      throw new Error(`missing metric ${metric.name}`);
    }
    return evaluateMetric(baselineValue, candidateValue, metric);
  });
  const metricFailures = metrics.filter((item) => !item.passed).map((item) => item.name);
  gates.push({
    name: "performance",
    status: metricFailures.length === 0 ? "passed" : "failed",
    reasons: metricFailures,
  });

  const statuses = new Set(gates.map((gate) => gate.status));
  const status: ReleaseDecision["status"] = statuses.has("inconclusive")
    ? "inconclusive"
    : statuses.has("failed")
      ? "rejected"
      : "accepted";
  return { status, gates, metrics };
}
