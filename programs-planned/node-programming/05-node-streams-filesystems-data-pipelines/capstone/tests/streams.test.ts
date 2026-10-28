import assert from 'node:assert/strict';
import { Readable, Writable } from 'node:stream';
import { pipeline } from 'node:stream/promises';
import test from 'node:test';

import { FlowError } from '../src/errors.js';
import { FlowEventDecoder } from '../src/streams.js';

async function decode(
  chunks: readonly Uint8Array[],
  options: { readonly maxLineBytes?: number; readonly maxEvents?: number } = {},
): Promise<unknown[]> {
  const decoder = new FlowEventDecoder(
    options.maxLineBytes ?? 256,
    options.maxEvents ?? 10,
    { maxIdBytes: 20, maxKindBytes: 20 },
  );
  const output: unknown[] = [];
  const sink = new Writable({
    objectMode: true,
    write(value, _encoding, callback) {
      output.push(value);
      callback();
    },
  });
  await pipeline(
    Readable.from(chunks.map((chunk) => Buffer.from(chunk)), { objectMode: false }),
    decoder,
    sink,
  );
  return output;
}

const validLine = Buffer.from(
  '{"id":"é","timestamp":"2026-08-09T10:00:00.000Z","kind":"x","value":1}\n',
);

test('decodes valid records across every single-byte chunk', async () => {
  const chunks = [...validLine].map((_, index) => validLine.subarray(index, index + 1));
  const output = await decode(chunks);
  assert.equal(output.length, 1);
});

test('all two-part byte splits produce the same event', async () => {
  const expected = await decode([validLine]);
  for (let split = 0; split <= validLine.length; split += 1) {
    assert.deepEqual(
      await decode([validLine.subarray(0, split), validLine.subarray(split)]),
      expected,
      `split at byte ${split}`,
    );
  }
});

test('rejects invalid UTF-8 instead of replacement decoding', async () => {
  const prefix = Buffer.from('{"id":"');
  const suffix = Buffer.from(
    '","timestamp":"2026-08-09T10:00:00.000Z","kind":"x","value":1}\n',
  );
  await assert.rejects(
    decode([Buffer.concat([prefix, Buffer.from([0xff]), suffix])]),
    (error: unknown) => error instanceof FlowError && error.code === 'DECODE',
  );
});

test('rejects an overlong unfinished line before a delimiter arrives', async () => {
  await assert.rejects(
    decode([Buffer.alloc(300, 97)], { maxLineBytes: 256 }),
    (error: unknown) =>
      error instanceof FlowError && error.code === 'LINE_LIMIT',
  );
});

test('counts only successfully validated events against the event bound', async () => {
  const two = Buffer.concat([validLine, validLine]);
  await assert.rejects(
    decode([two], { maxEvents: 1 }),
    (error: unknown) =>
      error instanceof FlowError && error.code === 'EVENT_LIMIT',
  );
});

test('accepts CRLF and a final unterminated valid event', async () => {
  const crlf = Buffer.from(validLine.toString().replace('\n', '\r\n'));
  const unterminated = validLine.subarray(0, -1);
  assert.equal((await decode([crlf])).length, 1);
  assert.equal((await decode([unterminated])).length, 1);
});
