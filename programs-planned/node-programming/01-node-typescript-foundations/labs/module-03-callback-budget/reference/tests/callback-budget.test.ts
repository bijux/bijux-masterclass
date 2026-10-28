import test from 'node:test';
import assert from 'node:assert/strict';
import { firstAccepted } from '../src/index.js';

test('stops at first accepted result', () => {
  const seen: number[] = [];
  const result = firstAccepted([1, 2, 3, 4], 4, (value) => { seen.push(value); return value * 2; }, (value) => value >= 6);
  assert.deepEqual(result, { kind: 'accepted', value: 6, sourceIndex: 2, calls: 3 });
  assert.deepEqual(seen, [1, 2, 3]);
});

test('enforces zero and finite budgets', () => {
  assert.deepEqual(firstAccepted([1], 0, (v) => v, () => true), { kind: 'budget-exhausted', calls: 0 });
  assert.throws(() => firstAccepted([1], -1, (v) => v, () => true));
});

test('does not retry thrown callbacks', () => {
  let calls = 0;
  assert.throws(() => firstAccepted([1, 2], 2, () => { calls += 1; throw new Error('boom'); }, () => true), /boom/);
  assert.equal(calls, 1);
});
