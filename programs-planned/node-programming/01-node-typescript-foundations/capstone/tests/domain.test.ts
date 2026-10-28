import test from 'node:test';
import assert from 'node:assert/strict';
import {
  abandonSession,
  completeSession,
  emptyLedger,
  planSession,
  searchSessions,
  startSession,
  summarizeLedger,
} from '../src/index.js';

const t0 = '2026-08-01T09:00:00.000Z';
const t1 = '2026-08-01T09:05:00.000Z';
const t2 = '2026-08-01T09:35:00.000Z';

test('legal transitions create new ledgers and preserve prior versions', () => {
  const empty = emptyLedger();
  const planned = planSession(empty, '  Type narrowing  ', 30, t0);
  const active = startSession(planned, 1, t1);
  const completed = completeSession(active, 1, 28, t2, '  union exercise  ');

  assert.equal(empty.sessions.length, 0);
  assert.equal(planned.sessions[0]?.status, 'planned');
  assert.equal(active.sessions[0]?.status, 'active');
  assert.deepEqual(completed.sessions[0], {
    id: 1,
    status: 'completed',
    topic: 'Type narrowing',
    plannedMinutes: 30,
    createdAt: t0,
    startedAt: t1,
    completedAt: t2,
    actualMinutes: 28,
    note: 'union exercise',
  });
});

test('illegal transitions preserve the supplied ledger', () => {
  const ledger = planSession(emptyLedger(), 'ESM', 20, t0);
  assert.throws(() => completeSession(ledger, 1, 20, t2), /cannot complete a planned session/u);
  assert.equal(ledger.sessions[0]?.status, 'planned');
});

test('abandon records whether work had started', () => {
  const planned = planSession(emptyLedger(), 'Promises', 40, t0);
  const abandonedPlanned = abandonSession(planned, 1, t1, 'schedule changed');
  assert.equal(abandonedPlanned.sessions[0]?.status, 'abandoned');
  assert.equal(abandonedPlanned.sessions[0]?.status === 'abandoned' ? abandonedPlanned.sessions[0].startedAt : 'wrong', null);

  const active = startSession(planSession(emptyLedger(), 'Closures', 40, t0), 1, t1);
  const abandonedActive = abandonSession(active, 1, t2, 'blocked');
  assert.equal(abandonedActive.sessions[0]?.status === 'abandoned' ? abandonedActive.sessions[0].startedAt : null, t1);
});

test('search includes completed notes and abandoned reasons', () => {
  let ledger = planSession(emptyLedger(), 'Runtime boundaries', 30, t0);
  ledger = startSession(ledger, 1, t1);
  ledger = completeSession(ledger, 1, 25, t2, 'JSON validation');
  ledger = planSession(ledger, 'Object identity', 20, t0);
  ledger = abandonSession(ledger, 2, t1, 'Need JSON practice first');
  assert.deepEqual(searchSessions(ledger, 'json').map((session) => session.id), [1, 2]);
});

test('summary distinguishes planned and actual minutes', () => {
  let ledger = planSession(emptyLedger(), 'A', 30, t0);
  ledger = startSession(ledger, 1, t1);
  ledger = completeSession(ledger, 1, 20, t2);
  ledger = planSession(ledger, 'B', 45, t0);
  assert.deepEqual(summarizeLedger(ledger), {
    total: 2,
    planned: 1,
    active: 0,
    completed: 1,
    abandoned: 0,
    plannedMinutes: 75,
    completedMinutes: 20,
  });
});
