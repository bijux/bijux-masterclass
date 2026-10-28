import test from 'node:test';
import assert from 'node:assert/strict';
import { executeCommand, emptyLedger, type StudyLedger } from '../src/index.js';

const instant = new Date('2026-08-01T09:00:00.000Z');

test('read-only commands load but never save or ask for the clock', async () => {
  let saves = 0;
  let clocks = 0;
  const result = await executeCommand({ kind: 'summary' }, {
    dataPath: '/virtual/ledger.json',
    load: async () => emptyLedger(),
    save: async () => { saves += 1; },
    now: () => { clocks += 1; return instant; },
  });
  assert.match(result.stdout, /total\t0/u);
  assert.equal(saves, 0);
  assert.equal(clocks, 0);
});

test('mutation saves before reporting success and asks for time once', async () => {
  const events: string[] = [];
  let stored: StudyLedger | undefined;
  const result = await executeCommand({ kind: 'plan', topic: 'Narrowing', minutes: 25 }, {
    dataPath: '/virtual/ledger.json',
    load: async () => { events.push('load'); return emptyLedger(); },
    save: async (_path, ledger) => { events.push('save'); stored = ledger; },
    now: () => { events.push('now'); return instant; },
  });
  events.push('returned');
  assert.deepEqual(events, ['load', 'now', 'save', 'returned']);
  assert.equal(stored?.sessions[0]?.topic, 'Narrowing');
  assert.equal(result.stdout, 'planned\t1\tNarrowing\n');
});

test('failed persistence does not return success', async () => {
  await assert.rejects(
    executeCommand({ kind: 'plan', topic: 'Errors', minutes: 20 }, {
      dataPath: '/virtual/ledger.json',
      load: async () => emptyLedger(),
      save: async () => { throw new Error('disk full'); },
      now: () => instant,
    }),
    /disk full/u,
  );
});
