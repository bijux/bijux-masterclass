import test from 'node:test';
import assert from 'node:assert/strict';
import type { TaskExecutor } from '../src/executor.js';
import type { TaskSpec } from '../src/domain.js';
import { parseManifest } from '../src/manifest.js';
import { TaskGraph } from '../src/graph.js';
import { runGraph } from '../src/scheduler.js';

function deferred<T>(): { promise: Promise<T>; resolve: (value: T) => void; reject: (reason: unknown) => void } {
  let resolve!: (value: T) => void; let reject!: (reason: unknown) => void;
  const promise = new Promise<T>((ok, bad) => { resolve = ok; reject = bad; });
  return { promise, resolve, reject };
}

class ControlledExecutor implements TaskExecutor {
  readonly starts: string[] = [];
  readonly gates = new Map<string, ReturnType<typeof deferred<string>>>();
  execute(task: TaskSpec, signal: AbortSignal): Promise<string> {
    this.starts.push(task.id);
    const gate = deferred<string>(); this.gates.set(task.id, gate);
    if (signal.aborted) gate.reject(signal.reason);
    else signal.addEventListener('abort', () => gate.reject(signal.reason), { once: true });
    return gate.promise;
  }
}

test('priority selects among ready tasks while final outcomes remain source ordered', async () => {
  const graph = TaskGraph.validate(parseManifest({ version: 'TASK_HARBOR_V1', tasks: [
    { id: 'low', kind: 'echo', text: 'l', priority: 'low' },
    { id: 'high', kind: 'echo', text: 'h', priority: 'high' },
    { id: 'normal', kind: 'echo', text: 'n' },
  ] }));
  const executor = new ControlledExecutor();
  const run = runGraph(graph, { concurrency: 1, policy: 'continue', executor, runId: 'r' });
  await new Promise<void>(resolve => setImmediate(resolve));
  assert.deepEqual(executor.starts, ['high']); executor.gates.get('high')!.resolve('h');
  await new Promise<void>(resolve => setImmediate(resolve));
  assert.deepEqual(executor.starts, ['high', 'normal']); executor.gates.get('normal')!.resolve('n');
  await new Promise<void>(resolve => setImmediate(resolve));
  executor.gates.get('low')!.resolve('l');
  const summary = await run;
  assert.deepEqual(summary.outcomes.map(outcome => outcome.id), ['low', 'high', 'normal']);
});

test('failed dependency blocks dependent and independent work continues', async () => {
  const graph = TaskGraph.validate(parseManifest({ version: 'TASK_HARBOR_V1', tasks: [
    { id: 'bad', kind: 'fail', message: 'bad' },
    { id: 'blocked', kind: 'echo', text: 'x', dependsOn: ['bad'] },
    { id: 'free', kind: 'echo', text: 'ok' },
  ] }));
  const summary = await runGraph(graph, { concurrency: 2, policy: 'continue', runId: 'r' });
  assert.deepEqual(summary.outcomes.map(outcome => outcome.status), ['failed', 'blocked', 'succeeded']);
});

test('fail-fast joins running siblings and accounts for pending tasks', async () => {
  const graph = TaskGraph.validate(parseManifest({ version: 'TASK_HARBOR_V1', tasks: [
    { id: 'bad', kind: 'fail', message: 'bad', priority: 'high' },
    { id: 'slow', kind: 'delay', milliseconds: 100 },
    { id: 'later', kind: 'echo', text: 'later' },
  ] }));
  const summary = await runGraph(graph, { concurrency: 2, policy: 'fail-fast', runId: 'r' });
  assert.equal(summary.outcomes.length, 3);
  assert.equal(summary.outcomes[0]?.status, 'failed');
  assert.ok(summary.outcomes.slice(1).every(outcome => outcome?.status === 'cancelled'));
});
