import { Readable } from 'node:stream';

export async function* batch<T>(
  source: AsyncIterable<T>,
  size: number,
  signal?: AbortSignal,
): AsyncGenerator<readonly T[]> {
  if (!Number.isInteger(size) || size <= 0) {
    throw new RangeError('size must be positive');
  }

  signal?.throwIfAborted();
  let current: T[] = [];

  try {
    for await (const item of source) {
      signal?.throwIfAborted();
      current.push(item);

      if (current.length === size) {
        const ready = current;
        current = [];
        yield ready;
      }
    }

    if (current.length > 0) {
      const ready = current;
      current = [];
      yield ready;
    }
  } finally {
    current.length = 0;
  }
}

export async function* take<T>(
  source: AsyncIterable<T>,
  count: number,
): AsyncGenerator<T> {
  if (!Number.isInteger(count) || count < 0) {
    throw new RangeError('count must be non-negative');
  }
  if (count === 0) {
    return;
  }

  let seen = 0;
  for await (const item of source) {
    yield item;
    seen += 1;
    if (seen === count) {
      return;
    }
  }
}

export function repeatable<T>(values: readonly T[]): AsyncIterable<T> {
  const snapshot = [...values];
  return {
    [Symbol.asyncIterator]: async function* (): AsyncGenerator<T> {
      for (const value of snapshot) {
        yield value;
      }
    },
  };
}

export async function webRoundTrip(
  chunks: readonly Uint8Array[],
): Promise<Buffer> {
  const nodeReadable = Readable.from(chunks.map((chunk) => Buffer.from(chunk)));
  const webReadable = Readable.toWeb(nodeReadable);
  const restored = Readable.fromWeb(webReadable);
  const output: Buffer[] = [];

  for await (const chunk of restored) {
    output.push(Buffer.from(chunk));
  }

  return Buffer.concat(output);
}
