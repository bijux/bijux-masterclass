import test from 'node:test';
import assert from 'node:assert/strict';
import { runSupervised, type SupervisedJob } from '../src/index.js';

function gate<T>(): { promise: Promise<T>; resolve: (value: T) => void } {
  let resolve!: (value: T) => void;
  const promise = new Promise<T>(done => { resolve = done; });
  return { promise, resolve };
}

test('bounded workers preserve source-ordered outcomes', async () => {
  const first = gate<number>(); const second = gate<number>();
  let active = 0; let peak = 0;
  const make = (id: string, promise: Promise<number>): SupervisedJob<number> => ({
    id, run: async () => { active += 1; peak = Math.max(peak, active); try { return await promise; } finally { active -= 1; } },
  });
  const run = runSupervised([make('a', first.promise), make('b', second.promise)], { concurrency: 2, policy: 'continue' });
  second.resolve(2); first.resolve(1);
  const outcomes = await run;
  assert.equal(peak, 2);
  assert.deepEqual(outcomes.map(value => value.id), ['a', 'b']);
});

test('continue records failure and keeps independent work', async () => {
  const outcomes = await runSupervised([
    { id: 'bad', run: async () => { throw new Error('bad'); } },
    { id: 'good', run: async () => 2 },
  ], { concurrency: 1, policy: 'continue' });
  assert.deepEqual(outcomes.map(value => value.status), ['failed', 'succeeded']);
});

test('fail-fast accounts for every source item', async () => {
  const outcomes = await runSupervised([
    { id: 'bad', run: async () => { throw new Error('bad'); } },
    { id: 'later', run: async () => 2 },
    { id: 'last', run: async () => 3 },
  ], { concurrency: 1, policy: 'fail-fast' });
  assert.equal(outcomes.length, 3);
  assert.equal(outcomes[0]?.status, 'failed');
  assert.deepEqual(outcomes.slice(1).map(value => value.status), ['cancelled', 'cancelled']);
});
