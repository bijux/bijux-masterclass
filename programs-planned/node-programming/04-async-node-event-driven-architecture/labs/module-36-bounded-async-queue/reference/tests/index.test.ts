import test from 'node:test';
import assert from 'node:assert/strict';
import { BoundedAsyncQueue } from '../src/index.js';

test('capacity applies backpressure until a value is consumed', async () => {
  const queue = new BoundedAsyncQueue<number>(1);
  await queue.push(1);
  let secondSettled = false;
  const second = queue.push(2).then(() => { secondSettled = true; });
  await Promise.resolve(); assert.equal(secondSettled, false);
  assert.deepEqual(await queue.take(), { done: false, value: 1 });
  await second;
  assert.deepEqual(await queue.take(), { done: false, value: 2 });
});

test('normal close drains buffered values then completes', async () => {
  const queue = new BoundedAsyncQueue<number>(2);
  await queue.push(1); await queue.push(2); queue.close();
  assert.deepEqual(await queue.take(), { done: false, value: 1 });
  assert.deepEqual(await queue.take(), { done: false, value: 2 });
  assert.equal((await queue.take()).done, true);
  await assert.rejects(queue.push(3), /closed/);
});

test('early iterator return rejects a blocked producer', async () => {
  const queue = new BoundedAsyncQueue<number>(1);
  const iterator = queue[Symbol.asyncIterator]();
  await queue.push(1);
  const blocked = queue.push(2);
  await iterator.return?.();
  await assert.rejects(blocked, /consumer ended/);
});

test('failure rejects a pending consumer', async () => {
  const queue = new BoundedAsyncQueue<number>(1);
  const pending = queue.take();
  queue.fail(new Error('broken'));
  await assert.rejects(pending, /broken/);
});
