import type { RunSummary, TaskOutcome } from './domain.js';
import { describeError } from './errors.js';
import type { TaskGraph } from './graph.js';

export function renderGraph(graph: TaskGraph): string {
  const lines = [`tasks: ${graph.tasks.length}`, `topological: ${graph.topologicalOrder.join(' -> ')}`];
  for (const task of graph.tasks) {
    lines.push(`${task.id}	${task.kind}	priority=${task.priority}	depends=${task.dependsOn.join(',') || '-'}`);
  }
  return `${lines.join('\n')}\n`;
}

function outcomeLine(outcome: TaskOutcome): string {
  switch (outcome.status) {
    case 'succeeded': return `${outcome.id}	succeeded	${outcome.value}`;
    case 'failed': return `${outcome.id}	failed	${describeError(outcome.error)}`;
    case 'timed-out': return `${outcome.id}	timed-out	${describeError(outcome.error)}`;
    case 'cancelled': return `${outcome.id}	cancelled	${describeError(outcome.reason)}`;
    case 'blocked': return `${outcome.id}	blocked	${outcome.blockedBy.join(',')}`;
  }
}

export function renderSummary(summary: RunSummary): string {
  const counts = new Map<string, number>();
  for (const outcome of summary.outcomes) counts.set(outcome.status, (counts.get(outcome.status) ?? 0) + 1);
  const lines = [
    `run: ${summary.runId}`,
    `policy: ${summary.policy}`,
    `peak-concurrency: ${summary.peakConcurrency}`,
    ...summary.outcomes.map(outcomeLine),
    `totals: ${[...counts.entries()].map(([key, value]) => `${key}=${value}`).join(' ')}`,
  ];
  return `${lines.join('\n')}\n`;
}
