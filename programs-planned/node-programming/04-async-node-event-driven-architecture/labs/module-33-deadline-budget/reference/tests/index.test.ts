import test from 'node:test';
import assert from 'node:assert/strict';
import { abortableDelay, Budget, DeadlineExceededError, withinBudget } from '../src/index.js';

test('successful operation completes inside budget', async () => {
  const budget = new Budget(performance.now() + 100);
  assert.equal(await withinBudget(budget, async () => 'ok'), 'ok');
});

test('parent cancellation preserves its reason', async () => {
  const parent = new AbortController();
  const reason = new Error('parent stopped');
  const promise = withinBudget(
    new Budget(performance.now() + 1000),
    signal => abortableDelay(500, signal),
    parent.signal,
  );
  parent.abort(reason);
  await assert.rejects(promise, error => error === reason);
});

test('deadline is classified explicitly', async () => {
  await assert.rejects(
    withinBudget(new Budget(performance.now() + 5), signal => abortableDelay(100, signal)),
    DeadlineExceededError,
  );
});

test('expired budget fails before operation starts', async () => {
  let started = false;
  await assert.rejects(
    withinBudget(new Budget(0, () => 1), async () => { started = true; }),
    DeadlineExceededError,
  );
  assert.equal(started, false);
});
