import test from 'node:test';
import assert from 'node:assert/strict';
import { TypedEventHub } from '../src/index.js';

interface Events {
  started: readonly [id: string];
  finished: readonly [id: string, value: number];
}

test('delivery is synchronous, ordered, and disposable', () => {
  const hub = new TypedEventHub<Events>();
  const trace: string[] = [];
  const offA = hub.on('started', id => trace.push(`a:${id}`));
  hub.on('started', id => trace.push(`b:${id}`));
  trace.push('before'); hub.emit('started', 'x'); trace.push('after');
  offA(); offA(); hub.emit('started', 'y');
  assert.deepEqual(trace, ['before', 'a:x', 'b:x', 'after', 'b:y']);
});

test('once resolves the typed argument tuple and cleans up', async () => {
  const hub = new TypedEventHub<Events>();
  const waiting = hub.once('finished');
  assert.equal(hub.listenerCount('finished'), 1);
  hub.emit('finished', 'x', 4);
  assert.deepEqual(await waiting, ['x', 4]);
  assert.equal(hub.listenerCount('finished'), 0);
});

test('aborted once wait removes its listener', async () => {
  const hub = new TypedEventHub<Events>();
  const controller = new AbortController();
  const waiting = hub.once('started', controller.signal);
  controller.abort(new Error('stop'));
  await assert.rejects(waiting, /stop/);
  assert.equal(hub.listenerCount('started'), 0);
});
