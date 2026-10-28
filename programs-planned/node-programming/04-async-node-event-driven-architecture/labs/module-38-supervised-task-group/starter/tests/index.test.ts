import test from 'node:test';
import assert from 'node:assert/strict';
import { runSequential } from '../src/index.js';

test('starter runs jobs in source order', async () => {
  const trace: string[] = [];
  const values = await runSequential([
    { id: 'a', run: async () => { trace.push('a'); return 1; } },
    { id: 'b', run: async () => { trace.push('b'); return 2; } },
  ]);
  assert.deepEqual(trace, ['a', 'b']); assert.deepEqual(values, [1, 2]);
});
