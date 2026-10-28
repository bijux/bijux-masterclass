import assert from 'node:assert/strict';
import test from 'node:test';

import {
  ChildOutputLimitError,
  runChildFilter,
  validateCommand,
} from '../src/index.js';

const base = {
  program: process.execPath,
  maxStdoutBytes: 1024,
  stderrLimit: 64,
} as const;

test('streams input through a directly spawned child', async () => {
  const script = [
    "process.stdin.on('data', chunk => process.stdout.write(chunk.toString().toUpperCase()));",
  ].join('');
  const result = await runChildFilter({
    ...base,
    args: ['-e', script],
    input: Buffer.from('hello'),
  });

  assert.equal(result.stdout.toString(), 'HELLO');
  assert.equal(result.code, 0);
});

test('preserves argument boundaries including spaces', async () => {
  const script = 'process.stdout.write(JSON.stringify(process.argv.slice(1)))';
  const result = await runChildFilter({
    ...base,
    args: ['-e', script, 'two words', 'third'],
    input: Buffer.alloc(0),
  });

  assert.deepEqual(JSON.parse(result.stdout.toString()), ['two words', 'third']);
});

test('retains bounded stderr while draining the complete stream', async () => {
  const script = "process.stderr.write('x'.repeat(100));process.stdout.write('ok')";
  const result = await runChildFilter({
    ...base,
    args: ['-e', script],
    input: Buffer.alloc(0),
    stderrLimit: 8,
  });

  assert.equal(result.stdout.toString(), 'ok');
  assert.equal(result.stderr.toString(), 'xxxxxxxx');
  assert.equal(result.stderrTruncated, true);
});

test('rejects nonzero exit after preserving bounded diagnostics', async () => {
  const script = "process.stderr.write('failure detail');process.exit(3)";
  await assert.rejects(
    runChildFilter({
      ...base,
      args: ['-e', script],
      input: Buffer.alloc(0),
      stderrLimit: 7,
    }),
    /code 3; stderr=failure/,
  );
});

test('rejects semantic stdout beyond its configured bound', async () => {
  const script = "process.stdout.write('x'.repeat(32));setInterval(()=>{},1000)";
  await assert.rejects(
    runChildFilter({
      ...base,
      args: ['-e', script],
      input: Buffer.alloc(0),
      maxStdoutBytes: 8,
    }),
    (error: unknown) => error instanceof ChildOutputLimitError,
  );
});

test('reports spawn failure without leaving unowned branches', async () => {
  await assert.rejects(
    runChildFilter({
      ...base,
      program: 'definitely-not-a-real-program-course5',
      args: [],
      input: Buffer.alloc(0),
    }),
  );
});

test('cancellation waits for child close before rejecting', async () => {
  const controller = new AbortController();
  const script = "process.stdin.resume();setInterval(()=>{},1000)";
  const operation = runChildFilter({
    ...base,
    args: ['-e', script],
    input: Buffer.alloc(0),
    signal: controller.signal,
  });
  setImmediate(() => controller.abort(new Error('cancel child')));

  await assert.rejects(operation);
});

test('command validation rejects empty and NUL-containing values', () => {
  assert.throws(() => validateCommand({ program: '', args: [] }), /required/);
  assert.throws(
    () => validateCommand({ program: 'x', args: ['a\0b'] }),
    /NUL/,
  );
});
