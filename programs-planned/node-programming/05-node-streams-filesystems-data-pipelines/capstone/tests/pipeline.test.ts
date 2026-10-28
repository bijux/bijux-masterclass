import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
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

import { FlowError } from '../src/errors.js';
import { DEFAULT_LIMITS } from '../src/limits.js';
import { inspectFile, transformFile, verifyFile } from '../src/pipeline.js';

const data = [
  '{"id":"2","timestamp":"2026-08-09T10:00:00.000Z","kind":"drop","value":2}',
  '{"id":"1","timestamp":"2026-08-09T09:00:00.000Z","kind":"keep","value":1}',
  '',
].join('\n');

async function withTempDirectory(
  run: (directory: string) => Promise<void>,
): Promise<void> {
  const directory = await mkdtemp(join(tmpdir(), 'flowledger-pipeline-'));
  try {
    await run(directory);
  } finally {
    await rm(directory, { recursive: true, force: true });
  }
}

test('inspects and filters deterministically', async () => {
  await withTempDirectory(async (directory) => {
    const input = join(directory, 'input.ndjson');
    const output = join(directory, 'output.ndjson');
    await writeFile(input, data);

    const inspection = await inspectFile(input, false);
    assert.equal(inspection.records, 2);
    assert.deepEqual(inspection.kinds, { drop: 1, keep: 1 });

    const report = await transformFile(input, output, {
      kind: 'keep',
      gzipInput: false,
      gzipOutput: false,
      replace: false,
    });
    assert.deepEqual(
      { inspected: report.inspected, emitted: report.emitted, filtered: report.filtered },
      { inspected: 2, emitted: 1, filtered: 1 },
    );
    assert.match(await readFile(output, 'utf8'), /"id":"1"/);
    await verifyFile(output, report.outputSha256);
  });
});

test('canonical and output digests coincide for uncompressed output', async () => {
  await withTempDirectory(async (directory) => {
    const input = join(directory, 'input');
    const output = join(directory, 'output');
    await writeFile(input, data);
    const report = await transformFile(input, output, {
      gzipInput: false,
      gzipOutput: false,
      replace: false,
    });
    assert.equal(report.canonicalSha256, report.outputSha256);
    assert.equal(
      report.outputSha256,
      createHash('sha256').update(await readFile(output)).digest('hex'),
    );
  });
});

test('preserves an existing destination after invalid input', async () => {
  await withTempDirectory(async (directory) => {
    const input = join(directory, 'input');
    const output = join(directory, 'output');
    await writeFile(input, 'not json\n');
    await writeFile(output, 'old');

    await assert.rejects(
      transformFile(input, output, {
        gzipInput: false,
        gzipOutput: false,
        replace: true,
      }),
    );
    assert.equal(await readFile(output, 'utf8'), 'old');
    assert.deepEqual((await readdir(directory)).sort(), ['input', 'output']);
  });
});

test('enforces source and output limits as separate policies', async () => {
  await withTempDirectory(async (directory) => {
    const input = join(directory, 'input');
    const output = join(directory, 'output');
    await writeFile(input, data);

    await assert.rejects(
      inspectFile(input, false, undefined, {
        ...DEFAULT_LIMITS,
        maxSourceBytes: 8,
      }),
      (error: unknown) =>
        error instanceof FlowError && error.code === 'SOURCE_LIMIT',
    );

    await assert.rejects(
      transformFile(input, output, {
        gzipInput: false,
        gzipOutput: false,
        replace: false,
        limits: { ...DEFAULT_LIMITS, maxOutputBytes: 8 },
      }),
      (error: unknown) =>
        error instanceof FlowError && error.code === 'OUTPUT_LIMIT',
    );
    await assert.rejects(readFile(output));
  });
});

test('verify rejects malformed expectations and exact digest mismatches', async () => {
  await withTempDirectory(async (directory) => {
    const input = join(directory, 'input');
    await writeFile(input, 'abc');
    await assert.rejects(verifyFile(input, 'not-a-digest'), /64 hexadecimal/);
    await assert.rejects(
      verifyFile(input, '0'.repeat(64)),
      (error: unknown) =>
        error instanceof FlowError && error.code === 'DIGEST_MISMATCH',
    );
  });
});
