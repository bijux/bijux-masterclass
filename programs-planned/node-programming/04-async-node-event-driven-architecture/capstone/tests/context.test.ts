import test from 'node:test';
import assert from 'node:assert/strict';
import { TaskContextManager } from '../src/context.js';

test('task context crosses await and disappears afterward', async () => {
  const contexts = new TaskContextManager();
  const observed = await contexts.run({ runId: 'r', taskId: 't', index: 1 }, async () => {
    await Promise.resolve(); return contexts.current();
  });
  assert.deepEqual(observed, { runId: 'r', taskId: 't', index: 1 });
  assert.equal(contexts.current(), undefined);
});
