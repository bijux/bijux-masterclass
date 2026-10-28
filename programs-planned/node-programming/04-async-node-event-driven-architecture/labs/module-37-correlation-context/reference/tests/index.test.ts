import test from 'node:test';
import assert from 'node:assert/strict';
import { ContextManager, contextDiagnostics, type ContextDiagnostic } from '../src/index.js';

function deferred(): { promise: Promise<void>; resolve: () => void } {
  let resolve!: () => void;
  const promise = new Promise<void>(done => { resolve = done; });
  return { promise, resolve };
}

test('concurrent contexts remain isolated across opposite resume order', async () => {
  const manager = new ContextManager();
  const a = deferred(); const b = deferred();
  const first = manager.run({ runId: 'a' }, async () => { await a.promise; return manager.current()?.runId; });
  const second = manager.run({ runId: 'b' }, async () => { await b.promise; return manager.current()?.runId; });
  b.resolve(); a.resolve();
  assert.deepEqual(await Promise.all([first, second]), ['a', 'b']);
  assert.equal(manager.current(), undefined);
});

test('nested child restores parent', async () => {
  const manager = new ContextManager();
  await manager.run({ runId: 'run', taskId: 'parent' }, async () => {
    await manager.child('child', async () => {
      assert.deepEqual(manager.current(), { runId: 'run', taskId: 'child', parentTaskId: 'parent' });
    });
    assert.deepEqual(manager.current(), { runId: 'run', taskId: 'parent' });
  });
});

test('diagnostic subscription is optional and removable', async () => {
  const manager = new ContextManager();
  const messages: ContextDiagnostic[] = [];
  const listener = (message: ContextDiagnostic): void => { messages.push(message); };
  contextDiagnostics.subscribe(listener);
  try { await manager.run({ runId: 'r' }, async () => undefined); }
  finally { contextDiagnostics.unsubscribe(listener); }
  assert.deepEqual(messages.map(message => message.phase), ['start', 'end']);
});
