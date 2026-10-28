import { createHash } from 'node:crypto';
import {
  Readable,
  Transform,
  Writable,
  type TransformCallback,
} from 'node:stream';
import { pipeline } from 'node:stream/promises';
import { createGzip, gunzipSync } from 'node:zlib';

class HashTap extends Transform {
  #hash = createHash('sha256');
  #bytes = 0;
  #digest: string | undefined;

  get bytes(): number {
    return this.#bytes;
  }

  digest(): string {
    if (this.#digest === undefined) {
      throw new Error('digest unavailable before completion');
    }
    return this.#digest;
  }

  override _transform(
    chunk: Buffer,
    _encoding: BufferEncoding,
    callback: TransformCallback,
  ): void {
    this.#bytes += chunk.length;
    this.#hash.update(chunk);
    callback(null, chunk);
  }

  override _flush(callback: TransformCallback): void {
    this.#digest = this.#hash.digest('hex');
    callback();
  }
}

class Collector extends Writable {
  readonly chunks: Buffer[] = [];

  override _write(
    chunk: Buffer,
    _encoding: BufferEncoding,
    callback: (error?: Error | null) => void,
  ): void {
    this.chunks.push(Buffer.from(chunk));
    callback();
  }

  buffer(): Buffer {
    return Buffer.concat(this.chunks);
  }
}

export interface CompressionReport {
  readonly sourceBytes: number;
  readonly compressedBytes: number;
  readonly sourceSha256: string;
  readonly compressedSha256: string;
  readonly compressed: Buffer;
}

export async function gzipWithDigests(
  source: AsyncIterable<Uint8Array>,
): Promise<CompressionReport> {
  async function* byteSource(): AsyncGenerator<Buffer> {
    for await (const chunk of source) {
      yield Buffer.from(chunk.buffer, chunk.byteOffset, chunk.byteLength);
    }
  }

  const sourceTap = new HashTap();
  const compressedTap = new HashTap();
  const sink = new Collector();
  await pipeline(
    Readable.from(byteSource(), { objectMode: false }),
    sourceTap,
    createGzip({ level: 6 }),
    compressedTap,
    sink,
  );

  return {
    sourceBytes: sourceTap.bytes,
    compressedBytes: compressedTap.bytes,
    sourceSha256: sourceTap.digest(),
    compressedSha256: compressedTap.digest(),
    compressed: sink.buffer(),
  };
}

export function gunzipBounded(
  input: Uint8Array,
  maxExpandedBytes: number,
): Buffer {
  if (!Number.isInteger(maxExpandedBytes) || maxExpandedBytes <= 0) {
    throw new RangeError('maxExpandedBytes must be a positive integer');
  }
  const output = gunzipSync(input, { maxOutputLength: maxExpandedBytes });
  if (output.length > maxExpandedBytes) {
    throw new Error('expanded bytes exceed limit');
  }
  return output;
}
