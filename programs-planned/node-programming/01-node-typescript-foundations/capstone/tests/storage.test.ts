import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtemp, readFile, readdir, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { emptyLedger, loadLedger, planSession, saveLedger } from '../src/index.js';

const t0 = '2026-08-01T09:00:00.000Z';

test('missing storage is an empty ledger and a save creates the parent directory', async () => {
  const root = await mkdtemp(join(tmpdir(), 'studyledger-storage-'));
  const path = join(root, 'nested', 'ledger.json');
  assert.deepEqual(await loadLedger(path), emptyLedger());
  const ledger = planSession(emptyLedger(), 'Testing', 30, t0);
  await saveLedger(path, ledger);
  assert.deepEqual(await loadLedger(path), ledger);
  assert.equal((await readdir(join(root, 'nested'))).some((name) => name.endsWith('.tmp')), false);
});

test('malformed storage is not confused with a missing file', async () => {
  const root = await mkdtemp(join(tmpdir(), 'studyledger-storage-'));
  const path = join(root, 'ledger.json');
  await writeFile(path, '{bad json', 'utf8');
  await assert.rejects(loadLedger(path), /invalid JSON/u);
  assert.equal(await readFile(path, 'utf8'), '{bad json');
});
