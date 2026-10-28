import assert from 'node:assert/strict';
import test from 'node:test';

import { batch, repeatable, take, webRoundTrip } from '../src/index.js';

async function collect<T>(source: AsyncIterable<T>): Promise<T[]> {
  const values: T[] = [];
  for await (const value of source) {
    values.push(value);
  }
  return values;
}

test('batch emits independent arrays including the final partial batch', async () => {
  const output = await collect(batch(repeatable([1, 2, 3, 4, 5]), 2));
  assert.deepEqual(output, [[1, 2], [3, 4], [5]]);
  assert.notEqual(output[0], output[1]);
});

test('repeatable snapshots the source and supports distinct passes', async () => {
  const sourceValues = ['a', 'b'];
  const source = repeatable(sourceValues);
  sourceValues.push('later');

  assert.deepEqual(await collect(source), ['a', 'b']);
  assert.deepEqual(await collect(source), ['a', 'b']);
});

test('take returns the requested prefix and closes upstream', async () => {
  const trace: string[] = [];
  async function* source(): AsyncGenerator<number> {
    try {
      trace.push('start');
      yield 1;
      trace.push('after-1');
      yield 2;
      trace.push('after-2');
      yield 3;
    } finally {
      trace.push('finally');
    }
  }

  assert.deepEqual(await collect(take(source(), 2)), [1, 2]);
  assert.deepEqual(trace, ['start', 'after-1', 'finally']);
});

test('take with zero does not pull upstream', async () => {
  let pulls = 0;
  const source: AsyncIterable<number> = {
    [Symbol.asyncIterator]() {
      return {
        async next() {
          pulls += 1;
          return { done: false, value: 1 };
        },
      };
    },
  };

  assert.deepEqual(await collect(take(source, 0)), []);
  assert.equal(pulls, 0);
});

test('batch observes cancellation before retaining another item', async () => {
  const controller = new AbortController();
  async function* source(): AsyncGenerator<number> {
    yield 1;
    controller.abort(new Error('stop batching'));
    yield 2;
  }

  await assert.rejects(
    collect(batch(source(), 2, controller.signal)),
    /stop batching/,
  );
});

test('invalid sizes and counts fail before useful work begins', async () => {
  await assert.rejects(collect(batch(repeatable([1]), 0)), /positive/);
  await assert.rejects(collect(take(repeatable([1]), -1)), /non-negative/);
});

test('Node-to-Web round trip preserves byte values', async () => {
  const output = await webRoundTrip([
    Buffer.from('ab'),
    Buffer.from([0, 255]),
    Buffer.from('c'),
  ]);
  assert.deepEqual(output, Buffer.concat([
    Buffer.from('ab'),
    Buffer.from([0, 255]),
    Buffer.from('c'),
  ]));
});
