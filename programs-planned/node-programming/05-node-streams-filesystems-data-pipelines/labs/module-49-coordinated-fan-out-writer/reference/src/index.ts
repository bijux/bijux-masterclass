import { once } from 'node:events';
import { Writable } from 'node:stream';
import { finished } from 'node:stream/promises';

async function writeOne(
  destination: Writable,
  chunk: Buffer,
  signal?: AbortSignal,
): Promise<void> {
  signal?.throwIfAborted();
  if (destination.write(chunk)) {
    return;
  }
  await once(destination, 'drain', { signal });
}

export async function fanOut(
  source: AsyncIterable<Uint8Array>,
  destinations: readonly Writable[],
  signal?: AbortSignal,
): Promise<{ readonly chunks: number; readonly bytes: number }> {
  if (destinations.length === 0) {
    throw new Error('at least one destination is required');
  }

  const terminalPromises = destinations.map((destination) =>
    finished(destination, { cleanup: true }),
  );
  let terminalFailure: unknown;
  for (const terminal of terminalPromises) {
    void terminal.catch((error: unknown) => {
      terminalFailure ??= error;
    });
  }

  let chunks = 0;
  let bytes = 0;

  try {
    for await (const raw of source) {
      signal?.throwIfAborted();
      if (terminalFailure !== undefined) {
        throw terminalFailure;
      }

      const chunk = Buffer.from(raw.buffer, raw.byteOffset, raw.byteLength);
      await Promise.all(
        destinations.map((destination) => writeOne(destination, chunk, signal)),
      );

      if (terminalFailure !== undefined) {
        throw terminalFailure;
      }
      chunks += 1;
      bytes += chunk.length;
    }

    for (const destination of destinations) {
      destination.end();
    }
    await Promise.all(terminalPromises);
    return { chunks, bytes };
  } catch (error) {
    for (const destination of destinations) {
      if (!destination.destroyed) {
        destination.destroy();
      }
    }
    await Promise.allSettled(terminalPromises);
    throw error;
  }
}

export class CollectingSink extends Writable {
  readonly parts: Buffer[] = [];

  constructor(highWaterMark = 1) {
    super({ highWaterMark });
  }

  override _write(
    chunk: Buffer,
    _encoding: BufferEncoding,
    callback: (error?: Error | null) => void,
  ): void {
    this.parts.push(Buffer.from(chunk));
    setImmediate(callback);
  }

  output(): Buffer {
    return Buffer.concat(this.parts);
  }
}
