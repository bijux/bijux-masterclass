import test from 'node:test';
import assert from 'node:assert/strict';
import { decodeLedger, encodeLedger, emptyLedger, planSession, startSession } from '../src/index.js';

const t0 = '2026-08-01T09:00:00.000Z';
const t1 = '2026-08-01T09:01:00.000Z';

test('encoding is canonical and round-trips a typed ledger', () => {
  const active = startSession(planSession(emptyLedger(), 'ESM', 30, t0), 1, t1);
  const text = encodeLedger(active);
  assert.match(text, /^\{\n  "format": "STUDY_LEDGER_V1"/u);
  assert.deepEqual(decodeLedger(text), active);
  assert.equal(text.endsWith('\n'), true);
});

test('decoder rejects unknown properties and duplicate ids with paths', () => {
  const text = JSON.stringify({
    format: 'STUDY_LEDGER_V1', nextId: 2, extra: true,
    sessions: [
      { id: 1, status: 'planned', topic: 'A', plannedMinutes: 10, createdAt: t0 },
      { id: 1, status: 'planned', topic: 'B', plannedMinutes: 10, createdAt: t0 },
    ],
  });
  assert.throws(() => decodeLedger(text), (error: unknown) => {
    assert.equal(error instanceof Error, true);
    assert.match(error instanceof Error ? error.message : '', /validation issues/u);
    return true;
  });
});

test('decoder rejects impossible chronology', () => {
  const text = JSON.stringify({
    format: 'STUDY_LEDGER_V1', nextId: 2,
    sessions: [{
      id: 1, status: 'active', topic: 'A', plannedMinutes: 10,
      createdAt: t1, startedAt: t0,
    }],
  });
  assert.throws(() => decodeLedger(text), /startedAt precedes createdAt/u);
});
