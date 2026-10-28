import assert from 'node:assert/strict';
import { Writable } from 'node:stream';
import test from 'node:test';

import { DeferredSink, writeWithBackpressure } from '../src/index.js';

async function* values(): AsyncGenerator<Buffer> {
  yield Buffer.from('a');
  yield Buffer.from('b');
  yield Buffer.from('c');
}

test('waits for pressure and preserves each byte exactly once', async () => {
  const sink = new DeferredSink(1);
  const report = await writeWithBackpressure(sink, values());
  assert.equal(sink.output().toString(), 'abc');
  assert.deepEqual(
    { chunks: report.chunks, bytes: report.bytes },
    { chunks: 3, bytes: 3 },
  );
  assert.ok(report.pressureWaits >= 1);
});

test('a larger high-water mark changes waits but not semantics', async () => {
  const sink = new DeferredSink(1024);
  const report = await writeWithBackpressure(sink, values());
  assert.equal(report.pressureWaits, 0);
  assert.equal(sink.output().toString(), 'abc');
});

test('abort settles the owner and destroys the destination', async () => {
  const controller = new AbortController();
  async function* source(): AsyncGenerator<Buffer> {
    yield Buffer.alloc(2);
    controller.abort(new Error('stop'));
    yield Buffer.alloc(2);
  }

  const sink = new DeferredSink(1);
  await assert.rejects(
    writeWithBackpressure(sink, source(), controller.signal),
    /stop/,
  );
  assert.equal(sink.destroyed, true);
});

test('source failure destroys the destination and preserves the cause', async () => {
  async function* source(): AsyncGenerator<Buffer> {
    yield Buffer.from('prefix');
    throw new Error('source failed');
  }

  const sink = new DeferredSink(1);
  await assert.rejects(writeWithBackpressure(sink, source()), /source failed/);
  assert.equal(sink.destroyed, true);
});

test('asynchronous destination failure is owned by the operation', async () => {
  class FailingSink extends Writable {
    override _write(
      _chunk: Buffer,
      _encoding: BufferEncoding,
      callback: (error?: Error | null) => void,
    ): void {
      setImmediate(() => callback(new Error('destination failed')));
    }
  }

  await assert.rejects(
    writeWithBackpressure(new FailingSink({ highWaterMark: 1024 }), values()),
    /destination failed/,
  );
});
