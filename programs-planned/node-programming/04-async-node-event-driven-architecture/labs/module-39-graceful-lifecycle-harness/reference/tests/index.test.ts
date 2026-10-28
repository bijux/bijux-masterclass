import test from 'node:test';
import assert from 'node:assert/strict';
import { LifecycleHost, type LifecycleResource } from '../src/index.js';

function resource(name: string, trace: string[], options: { failStart?: boolean; waitForAbort?: boolean } = {}): LifecycleResource {
  return {
    name,
    async start() { trace.push(`start:${name}`); if (options.failStart) throw new Error(`start:${name}`); },
    async quiesce() { trace.push(`quiesce:${name}`); },
    async drain(signal) {
      trace.push(`drain:${name}`);
      if (options.waitForAbort && !signal.aborted) {
        await new Promise<void>(resolve => signal.addEventListener('abort', () => resolve(), { once: true }));
      }
    },
    async force() { trace.push(`force:${name}`); },
    async close() { trace.push(`close:${name}`); },
  };
}

test('start and graceful shutdown have explicit order', async () => {
  const trace: string[] = [];
  const host = new LifecycleHost([resource('a', trace), resource('b', trace)]);
  await host.start();
  const first = host.shutdown(100); const second = host.shutdown(1);
  assert.strictEqual(first, second);
  assert.deepEqual(await first, { forced: false, issues: [] });
  assert.deepEqual(trace, ['start:a', 'start:b', 'quiesce:a', 'quiesce:b', 'drain:a', 'drain:b', 'close:b', 'close:a']);
});

test('startup failure rolls back started resources', async () => {
  const trace: string[] = [];
  const host = new LifecycleHost([resource('a', trace), resource('b', trace, { failStart: true })]);
  await assert.rejects(host.start(), /start:b/);
  assert.deepEqual(trace, ['start:a', 'start:b', 'close:a']);
});

test('grace expiry forces resources and still joins drain', async () => {
  const trace: string[] = [];
  const host = new LifecycleHost([resource('a', trace, { waitForAbort: true })]);
  await host.start();
  const report = await host.shutdown(5);
  assert.equal(report.forced, true);
  assert.deepEqual(trace, ['start:a', 'quiesce:a', 'drain:a', 'force:a', 'close:a']);
});
