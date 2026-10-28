import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import test from 'node:test';

import { auditPipeline } from '../src/index.js';

const input = Buffer.from(
  '{"z":1,"kind":"keep"}\n{"kind":"drop","a":2}\n',
);

async function* chunks(size: number): AsyncGenerator<Buffer> {
  for (let offset = 0; offset < input.length; offset += size) {
    yield input.subarray(offset, offset + size);
  }
}

const options = {
  maxLineBytes: 128,
  maxOutputBytes: 256,
  accept: (record: Readonly<Record<string, unknown>>) => record.kind === 'keep',
} as const;

test('semantic output and accounting are independent of chunking', async () => {
  const oneByte = await auditPipeline(chunks(1), options);
  const whole = await auditPipeline(chunks(1024), options);

  assert.equal(oneByte.output.toString(), whole.output.toString());
  assert.equal(oneByte.output.toString(), '{"kind":"keep","z":1}\n');
  assert.deepEqual(
    { inspected: oneByte.inspected, emitted: oneByte.emitted, filtered: oneByte.filtered },
    { inspected: 2, emitted: 1, filtered: 1 },
  );
});

test('source and output digests identify their exact representations', async () => {
  const report = await auditPipeline(chunks(3), options);
  assert.equal(
    report.sourceSha256,
    createHash('sha256').update(input).digest('hex'),
  );
  assert.equal(
    report.outputSha256,
    createHash('sha256').update(report.output).digest('hex'),
  );
  assert.notEqual(report.sourceSha256, report.outputSha256);
});

test('multibyte text split at every byte remains stable', async () => {
  const data = Buffer.from('{"kind":"keep","name":"é"}\n');
  const expected = await auditPipeline(
    (async function* () { yield data; })(),
    options,
  );

  for (let split = 0; split <= data.length; split += 1) {
    const actual = await auditPipeline(
      (async function* () {
        yield data.subarray(0, split);
        yield data.subarray(split);
      })(),
      options,
    );
    assert.deepEqual(actual.output, expected.output, `split at ${split}`);
  }
});

test('rejects malformed JSON with physical line context', async () => {
  await assert.rejects(
    auditPipeline(
      (async function* () { yield Buffer.from('{"ok":1}\nnot-json\n'); })(),
      options,
    ),
    /line 2: invalid JSON/,
  );
});

test('rejects invalid UTF-8 without replacement decoding', async () => {
  const invalid = Buffer.from([0x7b, 0x22, 0x78, 0x22, 0x3a, 0xff, 0x7d, 0x0a]);
  await assert.rejects(
    auditPipeline((async function* () { yield invalid; })(), options),
    /invalid UTF-8/,
  );
});

test('enforces line and canonical-output bounds independently', async () => {
  await assert.rejects(
    auditPipeline(chunks(2), { ...options, maxLineBytes: 4 }),
    /line 1 exceeds/,
  );
  await assert.rejects(
    auditPipeline(chunks(2), { ...options, maxOutputBytes: 8 }),
    /output exceeds/,
  );
});

test('predicate failures reject without falsifying terminal accounting', async () => {
  await assert.rejects(
    auditPipeline(chunks(4), {
      ...options,
      accept() {
        throw new Error('predicate failed');
      },
    }),
    /predicate failed/,
  );
});
