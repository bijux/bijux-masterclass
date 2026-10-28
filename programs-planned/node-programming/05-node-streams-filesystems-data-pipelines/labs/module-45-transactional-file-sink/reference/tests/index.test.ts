import assert from 'node:assert/strict';
import {
  mkdtemp,
  readFile,
  readdir,
  rm,
  writeFile,
} from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import test from 'node:test';

import { copyTransactional, transactionalWrite } from '../src/index.js';

async function withTempDirectory(
  run: (directory: string) => Promise<void>,
): Promise<void> {
  const directory = await mkdtemp(join(tmpdir(), 'transactional-sink-'));
  try {
    await run(directory);
  } finally {
    await rm(directory, { recursive: true, force: true });
  }
}

async function* chunks(): AsyncGenerator<Buffer> {
  yield Buffer.from('ab');
  yield Buffer.from('c');
}

test('publishes the complete candidate and cleans the stage', async () => {
  await withTempDirectory(async (directory) => {
    const destination = join(directory, 'out');
    const report = await transactionalWrite(destination, chunks());
    assert.deepEqual(report, { bytes: 3, committed: true });
    assert.equal(await readFile(destination, 'utf8'), 'abc');
    assert.deepEqual(await readdir(directory), ['out']);
  });
});

test('preserves an existing destination when replacement is disabled', async () => {
  await withTempDirectory(async (directory) => {
    const destination = join(directory, 'out');
    await writeFile(destination, 'old');
    await assert.rejects(
      transactionalWrite(destination, chunks()),
      /already exists/,
    );
    assert.equal(await readFile(destination, 'utf8'), 'old');
    assert.deepEqual(await readdir(directory), ['out']);
  });
});

test('replaces an existing destination when policy permits it', async () => {
  await withTempDirectory(async (directory) => {
    const destination = join(directory, 'out');
    await writeFile(destination, 'old');
    await transactionalWrite(destination, chunks(), { replace: true });
    assert.equal(await readFile(destination, 'utf8'), 'abc');
  });
});

test('source failure leaves no final or staged product', async () => {
  await withTempDirectory(async (directory) => {
    async function* failing(): AsyncGenerator<Buffer> {
      yield Buffer.from('partial');
      throw new Error('source failed');
    }

    const destination = join(directory, 'out');
    await assert.rejects(
      transactionalWrite(destination, failing()),
      /source failed/,
    );
    assert.deepEqual(await readdir(directory), []);
  });
});

test('pre-aborted operation does not create a stage', async () => {
  await withTempDirectory(async (directory) => {
    const controller = new AbortController();
    controller.abort(new Error('cancel before write'));
    await assert.rejects(
      transactionalWrite(join(directory, 'out'), chunks(), {
        signal: controller.signal,
      }),
      /cancel before write/,
    );
    assert.deepEqual(await readdir(directory), []);
  });
});

test('copyTransactional streams an existing source into a new product', async () => {
  await withTempDirectory(async (directory) => {
    const source = join(directory, 'source');
    const destination = join(directory, 'destination');
    await writeFile(source, 'copy me');
    const report = await copyTransactional(source, destination);
    assert.equal(report.bytes, 7);
    assert.equal(await readFile(destination, 'utf8'), 'copy me');
  });
});
