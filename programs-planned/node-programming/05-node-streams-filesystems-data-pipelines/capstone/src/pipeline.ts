import { createHash, timingSafeEqual } from 'node:crypto';
import { createReadStream } from 'node:fs';
import { PassThrough, Writable, type WritableOptions } from 'node:stream';
import { pipeline } from 'node:stream/promises';
import { createGunzip, createGzip } from 'node:zlib';

import type { FlowEvent } from './domain.js';
import { FlowError } from './errors.js';
import { DEFAULT_LIMITS, type FlowLimits } from './limits.js';
import {
  ByteLimit,
  ByteTap,
  EventEncoder,
  EventSelector,
  ExpandedLimit,
  FlowEventDecoder,
} from './streams.js';
import { withTransactionalOutput } from './transaction.js';

export interface InspectReport {
  readonly operation: 'inspect';
  readonly sourceBytes: number;
  readonly expandedBytes: number;
  readonly records: number;
  readonly sourceSha256: string;
  readonly kinds: Readonly<Record<string, number>>;
}

export interface TransformReport {
  readonly operation: 'normalize' | 'filter';
  readonly inspected: number;
  readonly emitted: number;
  readonly filtered: number;
  readonly sourceBytes: number;
  readonly expandedBytes: number;
  readonly outputBytes: number;
  readonly sourceSha256: string;
  readonly canonicalSha256: string;
  readonly outputSha256: string;
  readonly committed: true;
}

class EventInspector extends Writable {
  #records = 0;
  readonly counts = new Map<string, number>();

  constructor() {
    super({ objectMode: true } satisfies WritableOptions);
  }

  get records(): number {
    return this.#records;
  }

  override _write(
    event: FlowEvent,
    _encoding: BufferEncoding,
    callback: (error?: Error | null) => void,
  ): void {
    this.#records += 1;
    this.counts.set(event.kind, (this.counts.get(event.kind) ?? 0) + 1);
    callback();
  }
}

function eventLimits(limits: FlowLimits) {
  return {
    maxIdBytes: limits.maxIdBytes,
    maxKindBytes: limits.maxKindBytes,
  };
}

export async function inspectFile(
  input: string,
  gzipInput: boolean,
  signal?: AbortSignal,
  limits: FlowLimits = DEFAULT_LIMITS,
): Promise<InspectReport> {
  const sourceLimit = new ByteLimit(
    limits.maxSourceBytes,
    'SOURCE_LIMIT',
    'source',
  );
  const sourceTap = new ByteTap(true);
  const expanded = new ExpandedLimit(limits.maxExpandedBytes);
  const decoder = new FlowEventDecoder(
    limits.maxLineBytes,
    limits.maxEvents,
    eventLimits(limits),
  );
  const sink = new EventInspector();
  const stages = [
    createReadStream(input),
    sourceLimit,
    sourceTap,
    ...(gzipInput ? [createGunzip()] : [new PassThrough()]),
    expanded,
    decoder,
    sink,
  ] as const;

  await pipeline(...stages, { signal });

  return {
    operation: 'inspect',
    sourceBytes: sourceTap.bytes,
    expandedBytes: expanded.bytes,
    records: sink.records,
    sourceSha256: sourceTap.digestHex(),
    kinds: Object.fromEntries(
      [...sink.counts].sort(([left], [right]) => left.localeCompare(right)),
    ),
  };
}

export interface TransformOptions {
  readonly kind?: string | undefined;
  readonly gzipInput: boolean;
  readonly gzipOutput: boolean;
  readonly replace: boolean;
  readonly signal?: AbortSignal | undefined;
  readonly limits?: FlowLimits | undefined;
}

export async function transformFile(
  input: string,
  output: string,
  options: TransformOptions,
): Promise<TransformReport> {
  const limits = options.limits ?? DEFAULT_LIMITS;
  const sourceLimit = new ByteLimit(
    limits.maxSourceBytes,
    'SOURCE_LIMIT',
    'source',
  );
  const sourceTap = new ByteTap(true);
  const expanded = new ExpandedLimit(limits.maxExpandedBytes);
  const decoder = new FlowEventDecoder(
    limits.maxLineBytes,
    limits.maxEvents,
    eventLimits(limits),
  );
  const selector = new EventSelector(options.kind);
  const encoder = new EventEncoder();
  const canonicalTap = new ByteTap(true);
  const outputLimit = new ByteLimit(
    limits.maxOutputBytes,
    'OUTPUT_LIMIT',
    'output',
  );
  const outputTap = new ByteTap(true);
  const operation: 'normalize' | 'filter' =
    options.kind === undefined ? 'normalize' : 'filter';

  const partial = await withTransactionalOutput(
    output,
    { replace: options.replace },
    async (sink) => {
      const stages = [
        createReadStream(input),
        sourceLimit,
        sourceTap,
        ...(options.gzipInput ? [createGunzip()] : [new PassThrough()]),
        expanded,
        decoder,
        selector,
        encoder,
        canonicalTap,
        ...(options.gzipOutput ? [createGzip({ level: 6 })] : [new PassThrough()]),
        outputLimit,
        outputTap,
        sink,
      ] as const;

      await pipeline(...stages, { signal: options.signal });
      if (decoder.stats.inspected !== selector.emitted + selector.filtered) {
        throw new Error('record accounting mismatch');
      }

      return {
        operation,
        inspected: decoder.stats.inspected,
        emitted: selector.emitted,
        filtered: selector.filtered,
        sourceBytes: sourceTap.bytes,
        expandedBytes: expanded.bytes,
        outputBytes: outputTap.bytes,
        sourceSha256: sourceTap.digestHex(),
        canonicalSha256: canonicalTap.digestHex(),
        outputSha256: outputTap.digestHex(),
      };
    },
  );

  return { ...partial, committed: true };
}

export async function verifyFile(
  input: string,
  expected: string,
  signal?: AbortSignal,
  limits: FlowLimits = DEFAULT_LIMITS,
): Promise<{
  readonly operation: 'verify';
  readonly bytes: number;
  readonly sha256: string;
  readonly matched: true;
}> {
  if (!/^[0-9a-fA-F]{64}$/u.test(expected)) {
    throw new FlowError(
      'DIGEST_MISMATCH',
      'expected sha256 must contain 64 hexadecimal characters',
    );
  }

  const hash = createHash('sha256');
  let bytes = 0;
  for await (const raw of createReadStream(input, { signal })) {
    const chunk = Buffer.from(raw);
    bytes += chunk.length;
    if (bytes > limits.maxSourceBytes) {
      throw new FlowError(
        'SOURCE_LIMIT',
        `source bytes exceed ${limits.maxSourceBytes}`,
      );
    }
    hash.update(chunk);
  }

  const actual = hash.digest();
  const wanted = Buffer.from(expected, 'hex');
  if (!timingSafeEqual(wanted, actual)) {
    throw new FlowError(
      'DIGEST_MISMATCH',
      `sha256 mismatch: expected ${expected}, actual ${actual.toString('hex')}`,
    );
  }

  return {
    operation: 'verify',
    bytes,
    sha256: actual.toString('hex'),
    matched: true,
  };
}
