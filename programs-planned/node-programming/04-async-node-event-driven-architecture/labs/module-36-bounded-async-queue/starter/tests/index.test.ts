import test from 'node:test';
import assert from 'node:assert/strict';
import { fromValues } from '../src/index.js';

test('starter yields source values', async () => {
  const seen: number[] = [];
  for await (const value of fromValues([1, 2])) seen.push(value);
  assert.deepEqual(seen, [1, 2]);
});
