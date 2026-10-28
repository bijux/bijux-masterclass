import test from 'node:test';
import assert from 'node:assert/strict';
import { ManualClock, pollUntil, PollDeadlineError } from '../src/index.js';

async function flush(): Promise<void> { await new Promise<void>(resolve => setImmediate(resolve)); }

test('poller advances deterministically and succeeds', async () => {
  const clock = new ManualClock();
  let attempts = 0;
  const result = pollUntil(() => (++attempts === 3 ? 'ready' : undefined), {
    clock, interval: 10, deadline: 50,
  });
  assert.equal(attempts, 1);
  clock.advanceBy(10); await flush(); assert.equal(attempts, 2);
  clock.advanceBy(10); await flush();
  assert.equal(await result, 'ready');
  assert.equal(clock.pending(), 0);
});

test('deadline is exact and does not create another full interval', async () => {
  const clock = new ManualClock();
  const result = pollUntil(() => undefined, { clock, interval: 10, deadline: 15 });
  const rejected = assert.rejects(result, PollDeadlineError);
  clock.advanceBy(10); await flush();
  clock.advanceBy(5); await flush();
  await rejected;
});

test('aborting removes a pending sleeper', async () => {
  const clock = new ManualClock();
  const controller = new AbortController();
  const sleep = clock.sleep(10, controller.signal);
  assert.equal(clock.pending(), 1);
  controller.abort(new Error('stop'));
  await assert.rejects(sleep, /stop/);
  assert.equal(clock.pending(), 0);
});
