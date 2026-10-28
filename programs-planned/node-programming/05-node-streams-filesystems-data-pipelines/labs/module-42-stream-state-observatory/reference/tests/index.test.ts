import assert from 'node:assert/strict';
import { Readable, Writable } from 'node:stream';
import { finished, pipeline } from 'node:stream/promises';
import test from 'node:test';

import { ByteCounter, CollectingWritable, observe } from '../src/index.js';

test('records distinct readable and writable terminal states', async () => {
  const result = await observe([Buffer.from('ab'), Buffer.from('c')]);
  assert.equal(result.bytes, 3);
  assert.equal(result.output.toString(), 'abc');
  assert.equal(result.final.readableEnded, true);
  assert.equal(result.final.writableFinished, true);
  assert.ok(result.trace.includes('readable-end'));
  assert.ok(result.trace.includes('transform-finish'));
  assert.ok(result.trace.includes('transform-end'));
  assert.ok(result.trace.includes('writable-finish'));
  assert.ok(result.trace.includes('writable-close'));
  assert.ok(
    result.trace.indexOf('readable-end') < result.trace.indexOf('writable-finish'),
  );
});

test('empty input still completes every stream side', async () => {
  const result = await observe([]);
  assert.equal(result.bytes, 0);
  assert.equal(result.output.length, 0);
  assert.equal(result.final.readableEnded, true);
  assert.equal(result.final.writableFinished, true);
});

test('the collecting sink owns historical chunk bytes', async () => {
  const sink = new CollectingWritable();
  const terminal = finished(sink);
  const input = Buffer.from([1, 2, 3]);
  sink.write(input);
  input[0] = 9;
  sink.end();
  await terminal;

  assert.deepEqual(sink.bytes(), Buffer.from([1, 2, 3]));
});

test('the byte counter counts zero-length and nonempty chunks accurately', async () => {
  const counter = new ByteCounter();
  const sink = new CollectingWritable();
  await pipeline(
    Readable.from([Buffer.alloc(0), Buffer.from('abc')], { objectMode: false }),
    counter,
    sink,
  );
  assert.equal(counter.bytes, 3);
});

test('pipeline failure is the operation failure even after earlier bytes passed', async () => {
  class FailingSink extends Writable {
    #writes = 0;
    override _write(
      _chunk: Buffer,
      _encoding: BufferEncoding,
      callback: (error?: Error | null) => void,
    ): void {
      this.#writes += 1;
      callback(this.#writes === 2 ? new Error('sink failure') : undefined);
    }
  }

  const counter = new ByteCounter();
  await assert.rejects(
    pipeline(
      Readable.from([Buffer.from('a'), Buffer.from('b')], { objectMode: false }),
      counter,
      new FailingSink(),
    ),
    /sink failure/,
  );
  assert.equal(counter.bytes, 2);
});
