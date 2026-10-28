import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import test from 'node:test';

import { gunzipBounded, gzipWithDigests } from '../src/index.js';

async function* chunks(parts: readonly string[]): AsyncGenerator<Buffer> {
  for (const part of parts) {
    yield Buffer.from(part);
  }
}

test('names source and compressed representations separately', async () => {
  const report = await gzipWithDigests(chunks(['hello ', 'world']));
  assert.equal(report.sourceBytes, 11);
  assert.equal(report.compressedBytes, report.compressed.length);
  assert.equal(gunzipBounded(report.compressed, 100).toString(), 'hello world');
  assert.notEqual(report.sourceSha256, report.compressedSha256);
});

test('each digest identifies the exact bytes at its tap', async () => {
  const source = Buffer.from('digest me');
  const report = await gzipWithDigests(chunks(['digest ', 'me']));
  assert.equal(
    report.sourceSha256,
    createHash('sha256').update(source).digest('hex'),
  );
  assert.equal(
    report.compressedSha256,
    createHash('sha256').update(report.compressed).digest('hex'),
  );
});

test('source digest and decompressed product are chunk-independent', async () => {
  const one = await gzipWithDigests(chunks(['abcdef']));
  const many = await gzipWithDigests(chunks(['a', 'bc', 'def']));
  assert.equal(one.sourceSha256, many.sourceSha256);
  assert.deepEqual(
    gunzipBounded(one.compressed, 64),
    gunzipBounded(many.compressed, 64),
  );
});

test('enforces expanded output bound', async () => {
  const report = await gzipWithDigests(chunks(['hello ', 'world']));
  assert.throws(() => gunzipBounded(report.compressed, 5));
});

test('rejects invalid compressed bytes and invalid limits', async () => {
  assert.throws(() => gunzipBounded(Buffer.from('not gzip'), 100));
  assert.throws(() => gunzipBounded(Buffer.alloc(0), 0), /positive/);
});

test('empty source still has well-defined representation digests', async () => {
  const report = await gzipWithDigests(chunks([]));
  assert.equal(report.sourceBytes, 0);
  assert.equal(gunzipBounded(report.compressed, 1).length, 0);
  assert.equal(
    report.sourceSha256,
    createHash('sha256').update(Buffer.alloc(0)).digest('hex'),
  );
});
