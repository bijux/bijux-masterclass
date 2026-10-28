import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtemp, mkdir, rm, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { indexDirectory } from '../src/index.js';

test('indexes regular files in deterministic order', async () => {
  const directory = await mkdtemp(join(tmpdir(), 'file-index-'));
  try {
    await writeFile(join(directory, 'b.txt'), 'bb');
    await writeFile(join(directory, 'a.txt'), 'a');
    await mkdir(join(directory, 'nested'));
    const result = await indexDirectory(directory, 3);
    assert.deepEqual(result.map(({ name, size }) => ({ name, size })), [{ name: 'a.txt', size: 1 }, { name: 'b.txt', size: 2 }]);
  } finally { await rm(directory, { recursive: true, force: true }); }
});

test('rejects entry overflow before stat aggregation', async () => {
  const directory = await mkdtemp(join(tmpdir(), 'file-index-'));
  try {
    await writeFile(join(directory, 'a'), '');
    await writeFile(join(directory, 'b'), '');
    await assert.rejects(() => indexDirectory(directory, 1), /maximum is 1/);
  } finally { await rm(directory, { recursive: true, force: true }); }
});

test('observes pre-aborted signal', async () => {
  const controller = new AbortController(); controller.abort(new Error('stop'));
  await assert.rejects(() => indexDirectory('.', 10, controller.signal), /stop/);
});
