export interface ReconciliationInput {
  controlArtifactRefs: ReadonlySet<string>;
  artifactIds: ReadonlySet<string>;
  completedRuns: ReadonlySet<string>;
  notificationRunIds: ReadonlySet<string>;
}

export function reconcile(input: ReconciliationInput): string[] {
  const findings: string[] = [];
  for (const id of [...input.artifactIds].sort()) {
    if (!input.controlArtifactRefs.has(id)) {
      findings.push(`orphan-artifact:${id}`);
    }
  }
  for (const id of [...input.controlArtifactRefs].sort()) {
    if (!input.artifactIds.has(id)) {
      findings.push(`missing-artifact:${id}`);
    }
  }
  for (const id of [...input.completedRuns].sort()) {
    if (!input.notificationRunIds.has(id)) {
      findings.push(`missing-notification:${id}`);
    }
  }
  return findings;
}
