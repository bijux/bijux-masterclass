export type FindingKind =
  | "run-without-job"
  | "job-without-run"
  | "terminal-job-nonterminal-run"
  | "terminal-run-nonterminal-job"
  | "completed-run-missing-artifact"
  | "multiple-artifacts"
  | "artifact-without-completed-run"
  | "terminal-run-missing-outbox"
  | "duplicate-terminal-outbox"
  | "terminal-run-missing-event"
  | "duplicate-terminal-event";

export interface Snapshot {
  readonly runs: readonly { readonly runId: string; readonly status: string }[];
  readonly jobs: readonly { readonly runId: string; readonly status: string }[];
  readonly artifacts: readonly { readonly runId: string; readonly artifactId: string }[];
  readonly outbox: readonly { readonly runId: string; readonly eventType: string }[];
  readonly events?: readonly { readonly runId: string; readonly status: string }[];
}

export interface Finding {
  readonly kind: FindingKind;
  readonly runId: string;
  readonly repairKey: string;
  readonly detail: string;
}

const RUN_TERMINAL = new Set(["completed", "failed", "canceled"]);
const JOB_TERMINAL = new Set(["completed", "dead", "canceled"]);
const OUTBOX_EXPECTED: Readonly<Record<string, string>> = {
  completed: "analysis.completed",
  failed: "analysis.failed",
};

function append<K, V>(map: Map<K, V[]>, key: K, value: V): void {
  const values = map.get(key) ?? [];
  values.push(value);
  map.set(key, values);
}

export function inspect(snapshot: Snapshot): Finding[] {
  const runs = new Map(snapshot.runs.map((row) => [row.runId, row]));
  const jobs = new Map(snapshot.jobs.map((row) => [row.runId, row]));
  const artifacts = new Map<string, (typeof snapshot.artifacts)[number][]>();
  const outbox = new Map<string, (typeof snapshot.outbox)[number][]>();
  const events = new Map<string, NonNullable<Snapshot["events"]>[number][]>();
  for (const row of snapshot.artifacts) append(artifacts, row.runId, row);
  for (const row of snapshot.outbox) append(outbox, row.runId, row);
  for (const row of snapshot.events ?? []) append(events, row.runId, row);

  const identifiers = new Set([
    ...runs.keys(), ...jobs.keys(), ...artifacts.keys(), ...outbox.keys(), ...events.keys(),
  ]);
  const findings: Finding[] = [];
  for (const runId of [...identifiers].sort()) {
    const run = runs.get(runId);
    const job = jobs.get(runId);
    const runArtifacts = artifacts.get(runId) ?? [];
    const runOutbox = outbox.get(runId) ?? [];
    const runEvents = events.get(runId) ?? [];

    if (run === undefined && job !== undefined) {
      findings.push(finding("job-without-run", runId));
      continue;
    }
    if (run === undefined) {
      if (runArtifacts.length > 0) {
        findings.push(finding("artifact-without-completed-run", runId));
      }
      continue;
    }

    if (["queued", "running"].includes(run.status) && job === undefined) {
      findings.push(finding("run-without-job", runId));
    }
    if (job !== undefined && JOB_TERMINAL.has(job.status) && !RUN_TERMINAL.has(run.status)) {
      findings.push(finding("terminal-job-nonterminal-run", runId));
    }
    if (job !== undefined && RUN_TERMINAL.has(run.status) && !JOB_TERMINAL.has(job.status)) {
      findings.push(finding("terminal-run-nonterminal-job", runId));
    }
    if (run.status === "completed" && runArtifacts.length === 0) {
      findings.push(finding("completed-run-missing-artifact", runId));
    }
    if (runArtifacts.length > 1) findings.push(finding("multiple-artifacts", runId));
    if (runArtifacts.length > 0 && run.status !== "completed") {
      findings.push(finding("artifact-without-completed-run", runId));
    }

    const expectedOutbox = OUTBOX_EXPECTED[run.status];
    const matchingOutbox = expectedOutbox === undefined
      ? []
      : runOutbox.filter((row) => row.eventType === expectedOutbox);
    if (expectedOutbox !== undefined && matchingOutbox.length === 0) {
      findings.push(finding("terminal-run-missing-outbox", runId));
    }
    if (expectedOutbox !== undefined && matchingOutbox.length > 1) {
      findings.push(finding("duplicate-terminal-outbox", runId));
    }

    const matchingEvents = runEvents.filter((row) => row.status === run.status);
    if (RUN_TERMINAL.has(run.status) && matchingEvents.length === 0) {
      findings.push(finding("terminal-run-missing-event", runId));
    }
    if (RUN_TERMINAL.has(run.status) && matchingEvents.length > 1) {
      findings.push(finding("duplicate-terminal-event", runId));
    }
  }

  const unique = new Map(findings.map((item) => [`${item.kind}\u0000${item.runId}`, item]));
  return [...unique.values()].sort((a, b) =>
    a.runId.localeCompare(b.runId) || a.kind.localeCompare(b.kind)
  );
}

export function findingCounts(findings: readonly Finding[]): Readonly<Record<string, number>> {
  const result: Record<string, number> = {};
  for (const item of findings) result[item.kind] = (result[item.kind] ?? 0) + 1;
  return Object.fromEntries(Object.entries(result).sort(([a], [b]) => a.localeCompare(b)));
}

function finding(kind: FindingKind, runId: string): Finding {
  return {
    kind,
    runId,
    repairKey: `repair:${kind}:${runId}`,
    detail: `${kind} detected for ${runId}`,
  };
}
