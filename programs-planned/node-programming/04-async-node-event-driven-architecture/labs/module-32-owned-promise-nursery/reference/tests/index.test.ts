import test from 'node:test';
import assert from 'node:assert/strict';
import { TaskNursery } from '../src/index.js';

test('nursery observes every task in registration order', async () => {
  const nursery = new TaskNursery<number>();
  nursery.spawn('slow', async () => new Promise(resolve => setTimeout(() => resolve(1), 8)));
  nursery.spawn('fast', async () => 2);
  nursery.spawn('bad', async () => { throw 'reason'; });
  const outcomes = await nursery.join();
  assert.deepEqual(outcomes.map(value => value.id), ['slow', 'fast', 'bad']);
  assert.deepEqual(outcomes.map(value => value.status), ['fulfilled', 'fulfilled', 'rejected']);
});

test('synchronous throw is captured and join is repeatable', async () => {
  const nursery = new TaskNursery<number>();
  nursery.spawn('sync', () => { throw new Error('sync'); });
  const first = await nursery.join();
  const second = await nursery.join();
  assert.strictEqual(first, second);
  assert.equal(first[0]?.status, 'rejected');
});

test('duplicate and late registration are rejected', async () => {
  const nursery = new TaskNursery<number>();
  nursery.spawn('one', async () => 1);
  assert.throws(() => nursery.spawn('one', async () => 2), /duplicate/);
  await nursery.join();
  assert.throws(() => nursery.spawn('two', async () => 2), /closed/);
});
