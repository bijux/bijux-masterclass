import test from 'node:test';
import assert from 'node:assert/strict';
import { closeReverse } from '../src/index.js';

test('starter closes resources in reverse ownership order', async () => {
  const trace: string[] = [];
  await closeReverse([
    { name: 'a', close: async () => { trace.push('a'); } },
    { name: 'b', close: async () => { trace.push('b'); } },
  ]);
  assert.deepEqual(trace, ['b', 'a']);
});
