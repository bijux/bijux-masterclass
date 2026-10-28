import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtemp, readFile, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { addBook, decodeLedger, emptyLedger, encodeLedger, finishBook, loadLedger, saveLedger, startBook } from '../src/index.js';

test('performs immutable lifecycle', () => {
  const empty = emptyLedger();
  const queued = addBook(empty, '  Systems  ', '2026-08-09T08:00:00.000Z');
  const reading = startBook(queued, 1, '2026-08-09T09:00:00.000Z');
  const finished = finishBook(reading, 1, 300, '2026-08-10T09:00:00.000Z');
  assert.equal(finished.books[0]?.state, 'finished');
  assert.equal(queued.books[0]?.state, 'queued');
});

test('round trips canonical format', () => {
  const ledger = addBook(emptyLedger(), 'A', '2026-08-09T08:00:00.000Z');
  assert.deepEqual(decodeLedger(encodeLedger(ledger)), ledger);
});

test('loads missing and saves real file', async () => {
  const directory = await mkdtemp(join(tmpdir(), 'reading-ledger-'));
  const path = join(directory, 'ledger.json');
  try {
    assert.deepEqual(await loadLedger(path), emptyLedger());
    const ledger = addBook(emptyLedger(), 'A', '2026-08-09T08:00:00.000Z');
    await saveLedger(path, ledger);
    assert.deepEqual(decodeLedger(await readFile(path, 'utf8')), ledger);
  } finally { await rm(directory, { recursive: true, force: true }); }
});
