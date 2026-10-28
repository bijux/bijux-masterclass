import { once } from 'node:events';
import { Writable } from 'node:stream';
import { finished } from 'node:stream/promises';

export interface WriteReport {
  readonly chunks: number;
  readonly bytes: number;
  readonly pressureWaits: number;
}

export async function writeWithBackpressure(
  destination: Writable,
  source: AsyncIterable<Uint8Array>,
  signal?: AbortSignal,
): Promise<WriteReport> {
  signal?.throwIfAborted();
  const terminal = finished(destination, { cleanup: true });
  let destinationFailure: unknown;
  void terminal.catch((error: unknown) => {
    destinationFailure ??= error;
  });

  let chunks = 0;
  let bytes = 0;
  let pressureWaits = 0;

  try {
    for await (const value of source) {
      signal?.throwIfAborted();
      if (destinationFailure !== undefined) {
        throw destinationFailure;
      }

      const chunk = Buffer.from(
        value.buffer,
        value.byteOffset,
        value.byteLength,
      );
      const accepted = destination.write(chunk);
      chunks += 1;
      bytes += chunk.length;

      if (!accepted) {
        pressureWaits += 1;
        await once(destination, 'drain', { signal });
      }
      if (destinationFailure !== undefined) {
        throw destinationFailure;
      }
    }

    destination.end();
    await terminal;
    return { chunks, bytes, pressureWaits };
  } catch (error) {
    const causalError = destinationFailure ?? error;
    if (!destination.destroyed) {
      destination.destroy();
    }
    await Promise.allSettled([terminal]);
    throw causalError;
  }
}

export class DeferredSink extends Writable {
  readonly chunks: Buffer[] = [];

  constructor(highWaterMark = 1) {
    super({ highWaterMark });
  }

  override _write(
    chunk: Buffer,
    _encoding: BufferEncoding,
    callback: (error?: Error | null) => void,
  ): void {
    this.chunks.push(Buffer.from(chunk));
    setImmediate(callback);
  }

  output(): Buffer {
    return Buffer.concat(this.chunks);
  }
}
