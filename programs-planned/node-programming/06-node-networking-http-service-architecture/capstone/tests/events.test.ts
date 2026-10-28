import test from 'node:test';
import assert from 'node:assert/strict';
import { EventJournal } from '../src/events.js';

test('replays retained events and detects gaps', () => {
  const journal = new EventJournal(2, 1);
  journal.append({ type: 'service-quiescing', occurredAtMs: 1 });
  journal.append({ type: 'service-quiescing', occurredAtMs: 2 });
  journal.append({ type: 'service-quiescing', occurredAtMs: 3 });
  assert.throws(() => journal.open(0, () => {}), /predates/);
  const seen: number[] = [];
  const sub = journal.open(1, (event) => seen.push(event.sequence));
  assert.deepEqual(sub.replay.map((event) => event.sequence), [2, 3]);
  journal.append({ type: 'service-quiescing', occurredAtMs: 4 });
  assert.deepEqual(seen, [4]);
  sub.dispose();
});
