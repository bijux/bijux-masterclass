import test from 'node:test';
import assert from 'node:assert/strict';
import { cooperativeMap, observeControlledTurn } from '../src/index.js';

test('controlled timer context has the documented causal order', async () => {
  assert.deepEqual(await observeControlledTurn(), [
    'synchronous-start',
    'timer-callback',
    'next-tick',
    'queue-microtask',
    'promise-reaction',
    'immediate-after-timer',
  ]);
});

test('cooperative mapping preserves source order and yields', async () => {
  const trace: string[] = [];
  const immediate = new Promise<void>(resolve => {
    setImmediate(() => { trace.push('other-immediate'); resolve(); });
  });
  const mapped = cooperativeMap([1, 2, 3, 4], 1, value => {
    trace.push(`map-${value}`);
    return value * 10;
  });
  const result = await mapped;
  await immediate;
  assert.deepEqual(result, [10, 20, 30, 40]);
  assert.ok(trace.indexOf('other-immediate') < trace.indexOf('map-4'));
});

test('abort is observed at a chunk boundary', async () => {
  const controller = new AbortController();
  const promise = cooperativeMap([1, 2], 1, (value, index) => {
    if (index === 0) controller.abort(new Error('stop'));
    return value;
  }, controller.signal);
  await assert.rejects(promise, /stop/);
});
