import test from 'node:test';
import assert from 'node:assert/strict';
import { Budget } from '../src/index.js';

test('child budget cannot extend parent', () => {
  let now = 10;
  const parent = new Budget(100, () => now);
  assert.equal(parent.child(200).deadline, 100);
  assert.equal(parent.child(20).deadline, 30);
  now = 101;
  assert.equal(parent.remaining(), 0);
});
