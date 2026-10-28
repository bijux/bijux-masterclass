import assert from 'node:assert/strict';
import { Writable } from 'node:stream';
import test from 'node:test';

import { CollectingSink, fanOut } from '../src/index.js';

async function* source(): AsyncGenerator<Buffer> {
  yield Buffer.from('a');
  yield Buffer.from('bc');
}

test('required branches receive identical bytes in source order', async () => {
  const first = new CollectingSink(1);
  const second = new CollectingSink(8);
  const report = await fanOut(source(), [first, second]);

  assert.equal(first.output().toString(), 'abc');
  assert.equal(second.output().toString(), 'abc');
  assert.deepEqual(report, { chunks: 2, bytes: 3 });
});

test('different pressure schedules do not duplicate chunks', async () => {
  const fast = new CollectingSink(64);
  const slow = new CollectingSink(1);
  const report = await fanOut(source(), [fast, slow]);

  assert.equal(fast.output().toString(), 'abc');
  assert.equal(slow.output().toString(), 'abc');
  assert.equal(report.chunks, 2);
});

test('one branch failure invalidates and closes the complete operation', async () => {
  class FailingSink extends Writable {
    #writes = 0;
    override _write(
      _chunk: Buffer,
      _encoding: BufferEncoding,
      callback: (error?: Error | null) => void,
    ): void {
      this.#writes += 1;
      callback(this.#writes === 2 ? new Error('sink failed') : undefined);
    }
  }

  const sibling = new CollectingSink();
  const failing = new FailingSink();
  await assert.rejects(fanOut(source(), [sibling, failing]), /sink failed/);
  assert.equal(sibling.destroyed, true);
  assert.equal(failing.destroyed, true);
});

test('requires at least one required destination', async () => {
  await assert.rejects(fanOut(source(), []), /at least one/);
});

test('abort while pressure is active destroys every branch', async () => {
  const controller = new AbortController();
  async function* abortingSource(): AsyncGenerator<Buffer> {
    yield Buffer.from('a');
    controller.abort(new Error('stop fan-out'));
    yield Buffer.from('b');
  }

  const first = new CollectingSink(1);
  const second = new CollectingSink(1);
  await assert.rejects(
    fanOut(abortingSource(), [first, second], controller.signal),
    /stop fan-out/,
  );
  assert.equal(first.destroyed, true);
  assert.equal(second.destroyed, true);
});
