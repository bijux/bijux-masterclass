import {
  Readable,
  Transform,
  Writable,
  type TransformCallback,
  type WritableOptions,
} from 'node:stream';
import { pipeline } from 'node:stream/promises';

export type TraceEvent =
  | 'readable-end'
  | 'transform-finish'
  | 'transform-end'
  | 'writable-finish'
  | 'writable-close';

export class ByteCounter extends Transform {
  #bytes = 0;

  get bytes(): number {
    return this.#bytes;
  }

  override _transform(
    chunk: Buffer,
    _encoding: BufferEncoding,
    callback: TransformCallback,
  ): void {
    this.#bytes += chunk.length;
    callback(null, chunk);
  }
}

export class CollectingWritable extends Writable {
  readonly chunks: Buffer[] = [];

  constructor(options: WritableOptions = {}) {
    super(options);
  }

  override _write(
    chunk: Buffer,
    _encoding: BufferEncoding,
    callback: (error?: Error | null) => void,
  ): void {
    this.chunks.push(Buffer.from(chunk));
    callback();
  }

  bytes(): Buffer {
    return Buffer.concat(this.chunks);
  }
}

export interface Observation {
  readonly trace: readonly TraceEvent[];
  readonly bytes: number;
  readonly output: Buffer;
  readonly final: {
    readonly readableEnded: boolean;
    readonly writableFinished: boolean;
    readonly destroyed: boolean;
  };
}

export async function observe(
  chunks: readonly Uint8Array[],
): Promise<Observation> {
  const trace: TraceEvent[] = [];
  const source = Readable.from(
    chunks.map((chunk) => Buffer.from(chunk)),
    { objectMode: false },
  );
  const counter = new ByteCounter();
  const sink = new CollectingWritable();

  source.once('end', () => trace.push('readable-end'));
  counter.once('finish', () => trace.push('transform-finish'));
  counter.once('end', () => trace.push('transform-end'));
  sink.once('finish', () => trace.push('writable-finish'));
  sink.once('close', () => trace.push('writable-close'));

  await pipeline(source, counter, sink);

  return {
    trace,
    bytes: counter.bytes,
    output: sink.bytes(),
    final: {
      readableEnded: source.readableEnded,
      writableFinished: sink.writableFinished,
      destroyed: sink.destroyed,
    },
  };
}
