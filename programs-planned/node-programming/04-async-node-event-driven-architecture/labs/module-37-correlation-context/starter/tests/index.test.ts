import test from 'node:test';
import assert from 'node:assert/strict';
import { childContext } from '../src/index.js';

test('starter creates an immutable child context', () => {
  assert.deepEqual(childContext({ runId: 'r' }, 't'), { runId: 'r', taskId: 't' });
});
