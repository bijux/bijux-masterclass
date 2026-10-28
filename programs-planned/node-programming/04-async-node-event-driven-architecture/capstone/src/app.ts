import { loadManifest, parseManifest } from './manifest.js';
import { TaskGraph } from './graph.js';
import { runGraph, type RunOptions } from './scheduler.js';
import { renderGraph, renderSummary } from './render.js';

export async function inspectFile(path: string): Promise<string> {
  return renderGraph(TaskGraph.validate(await loadManifest(path)));
}
export async function runFile(path: string, options: RunOptions): Promise<{ readonly text: string; readonly success: boolean }> {
  const summary = await runGraph(TaskGraph.validate(await loadManifest(path)), options);
  const success = summary.outcomes.every(outcome => outcome.status === 'succeeded');
  return { text: renderSummary(summary), success };
}
export async function runDemo(options: Omit<RunOptions, 'runId'>): Promise<string> {
  const manifest = parseManifest({
    version: 'TASK_HARBOR_V1',
    tasks: [
      { id: 'warmup', kind: 'delay', milliseconds: 5, priority: 'normal' },
      { id: 'message', kind: 'uppercase', text: 'harbor', dependsOn: ['warmup'], priority: 'high' },
      { id: 'audit', kind: 'echo', text: 'complete', dependsOn: ['message'] },
    ],
  });
  return renderSummary(await runGraph(TaskGraph.validate(manifest), { ...options, runId: 'demo-run' }));
}
