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

import { throughChild } from '../src/child.js';
import { FlowError } from '../src/errors.js';
import { DEFAULT_LIMITS } from '../src/limits.js';

async function withTempDirectory(
  run: (directory: string) => Promise<void>,
): Promise<void> {
  const directory = await mkdtemp(join(tmpdir(), 'flowledger-child-'));
  try {
    await run(directory);
  } finally {
    await rm(directory, { recursive: true, force: true });
  }
}

test('commits successful child stdout and reports both byte domains', async () => {
  await withTempDirectory(async (directory) => {
    const input = join(directory, 'input');
    const output = join(directory, 'output');
    await writeFile(input, 'hello');
    const script = [
      "process.stdin.on('data', chunk => process.stdout.write(chunk.toString().toUpperCase()));",
    ].join('');

    const report = await throughChild(
      input,
      output,
      process.execPath,
      ['-e', script],
      false,
    );
    assert.equal(await readFile(output, 'utf8'), 'HELLO');
    assert.equal(report.inputBytes, 5);
    assert.equal(report.outputBytes, 5);
  });
});

test('preserves direct argument boundaries including spaces', async () => {
  await withTempDirectory(async (directory) => {
    const input = join(directory, 'input');
    const output = join(directory, 'output');
    await writeFile(input, '');
    const script = 'process.stdout.write(JSON.stringify(process.argv.slice(1)))';

    await throughChild(
      input,
      output,
      process.execPath,
      ['-e', script, 'two words', 'third'],
      false,
    );
    assert.deepEqual(
      JSON.parse(await readFile(output, 'utf8')),
      ['two words', 'third'],
    );
  });
});

test('does not commit stdout from a nonzero child', async () => {
  await withTempDirectory(async (directory) => {
    const input = join(directory, 'input');
    const output = join(directory, 'output');
    await writeFile(input, 'hello');
    const script = [
      "process.stdout.write('partial');",
      "process.stderr.write('bad');",
      'process.exit(4);',
    ].join('');

    await assert.rejects(
      throughChild(input, output, process.execPath, ['-e', script], false),
      /code 4; stderr=bad/,
    );
    await assert.rejects(readFile(output));
    assert.deepEqual(await readdir(directory), ['input']);
  });
});

test('bounds child stdout and removes the staged candidate', async () => {
  await withTempDirectory(async (directory) => {
    const input = join(directory, 'input');
    const output = join(directory, 'output');
    await writeFile(input, '');
    const script = "process.stdout.write('x'.repeat(64));setInterval(()=>{},1000)";

    await assert.rejects(
      throughChild(
        input,
        output,
        process.execPath,
        ['-e', script],
        false,
        undefined,
        { ...DEFAULT_LIMITS, maxChildOutputBytes: 8 },
      ),
      (error: unknown) =>
        error instanceof FlowError && error.code === 'CHILD_OUTPUT_LIMIT',
    );
    assert.deepEqual(await readdir(directory), ['input']);
  });
});

test('reports spawn failure without publishing a candidate', async () => {
  await withTempDirectory(async (directory) => {
    const input = join(directory, 'input');
    const output = join(directory, 'output');
    await writeFile(input, '');

    await assert.rejects(
      throughChild(
        input,
        output,
        'definitely-not-a-real-program-flowledger',
        [],
        false,
      ),
      (error: unknown) =>
        error instanceof FlowError && error.code === 'CHILD_FAILED',
    );
    assert.deepEqual(await readdir(directory), ['input']);
  });
});

test('cancellation rejects only after owned child work settles', async () => {
  await withTempDirectory(async (directory) => {
    const input = join(directory, 'input');
    const output = join(directory, 'output');
    await writeFile(input, '');
    const controller = new AbortController();
    const operation = throughChild(
      input,
      output,
      process.execPath,
      ['-e', "process.stdin.resume();setInterval(()=>{},1000)"],
      false,
      controller.signal,
    );
    setImmediate(() => controller.abort(new Error('cancel through')));

    await assert.rejects(operation);
    assert.deepEqual(await readdir(directory), ['input']);
  });
});
