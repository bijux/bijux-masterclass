import test from 'node:test';
import assert from 'node:assert/strict';
import { HarborEventHub, eventStream } from '../src/events.js';
import { EventOverflowError } from '../src/errors.js';

test('observer failure is isolated and remaining observers still run', () => {
  const hub = new HarborEventHub(); const trace: string[] = [];
  hub.on(() => { throw new Error('observer'); }); hub.on(event => trace.push(event.type));
  const errors = hub.emit({ type: 'run-finished', runId: 'r' });
  assert.equal(errors.length, 1); assert.deepEqual(trace, ['run-finished']);
});

test('event stream closes on early return and overflows explicitly', async () => {
  const hub = new HarborEventHub();
  const stream = eventStream(hub, { capacity: 1 })[Symbol.asyncIterator]();
  hub.emit({ type: 'run-finished', runId: 'a' });
  hub.emit({ type: 'run-finished', runId: 'b' });
  await assert.rejects(stream.next(), EventOverflowError);
  await stream.return?.();
  assert.equal(hub.listenerCount, 0);
});
