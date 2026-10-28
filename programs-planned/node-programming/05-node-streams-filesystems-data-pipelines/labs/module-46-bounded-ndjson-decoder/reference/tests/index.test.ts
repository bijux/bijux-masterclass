import assert from 'node:assert/strict';
import test from 'node:test';

import { decodeNdjson, NdjsonError } from '../src/index.js';

async function* chunks(values: readonly Uint8Array[]): AsyncGenerator<Uint8Array> {
  for (const value of values) {
    yield value;
  }
}

async function collect(
  values: readonly Uint8Array[],
  options: { readonly maxLineBytes: number; readonly allowFinalUnterminated?: boolean },
) {
  const output = [];
  for await (const located of decodeNdjson(chunks(values), options)) {
    output.push(located);
  }
  return output;
}

test('every byte partition produces the same records', async () => {
  const input = Buffer.from('{"name":"é"}\n{"name":"x"}\n');
  const expected = await collect([input], { maxLineBytes: 64 });

  for (let split = 0; split <= input.length; split += 1) {
    const actual = await collect(
      [input.subarray(0, split), input.subarray(split)],
      { maxLineBytes: 64 },
    );
    assert.deepEqual(actual, expected, `split at byte ${split}`);
  }
});

test('reports the physical line for invalid JSON', async () => {
  await assert.rejects(
    collect([Buffer.from('{"ok":1}\nnope\n')], { maxLineBytes: 64 }),
    (error: unknown) =>
      error instanceof NdjsonError &&
      error.line === 2 &&
      error.code === 'INVALID_JSON',
  );
});

test('rejects invalid UTF-8 instead of replacing bytes silently', async () => {
  const invalid = Buffer.from([0x7b, 0x22, 0x78, 0x22, 0x3a, 0xff, 0x7d, 0x0a]);
  await assert.rejects(
    collect([invalid], { maxLineBytes: 64 }),
    (error: unknown) =>
      error instanceof NdjsonError && error.code === 'INVALID_UTF8',
  );
});

test('enforces the line limit in encoded bytes', async () => {
  const exact = Buffer.from('{"x":"é"}');
  assert.equal(exact.length, 10);

  assert.equal(
    (await collect([Buffer.concat([exact, Buffer.from('\n')])], { maxLineBytes: 10 })).length,
    1,
  );
  await assert.rejects(
    collect([Buffer.concat([exact, Buffer.from('\n')])], { maxLineBytes: 9 }),
    (error: unknown) =>
      error instanceof NdjsonError && error.code === 'LINE_TOO_LONG',
  );
});

test('bounds an unfinished line independently of chunk shape', async () => {
  await assert.rejects(
    collect([Buffer.from('{"x":"1234'), Buffer.from('56789"}')], { maxLineBytes: 8 }),
    (error: unknown) =>
      error instanceof NdjsonError && error.code === 'LINE_TOO_LONG',
  );
});

test('supports CRLF, blank lines, and final unterminated policy explicitly', async () => {
  const output = await collect(
    [Buffer.from('\r\n{"x":1}\r\n{"y":2}')],
    { maxLineBytes: 16 },
  );
  assert.deepEqual(output.map((entry) => entry.line), [2, 3]);

  await assert.rejects(
    collect([Buffer.from('{"x":1}')], {
      maxLineBytes: 16,
      allowFinalUnterminated: false,
    }),
    (error: unknown) =>
      error instanceof NdjsonError && error.code === 'UNTERMINATED_LINE',
  );
});

test('rejects non-object JSON values', async () => {
  await assert.rejects(
    collect([Buffer.from('[1,2]\n')], { maxLineBytes: 16 }),
    (error: unknown) =>
      error instanceof NdjsonError && error.code === 'NOT_OBJECT',
  );
});
