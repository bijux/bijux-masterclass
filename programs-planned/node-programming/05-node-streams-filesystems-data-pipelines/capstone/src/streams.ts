import { createHash, type Hash } from 'node:crypto';
import { Transform, type TransformCallback } from 'node:stream';

import {
  encodeFlowEvent,
  parseFlowEvent,
  type EventLimits,
  type FlowEvent,
} from './domain.js';
import { FlowError, type FlowErrorCode } from './errors.js';

export class ByteTap extends Transform {
  #bytes = 0;
  #hash: Hash | undefined;
  #finalized = false;
  #digest: string | undefined;

  constructor(hash = false) {
    super();
    if (hash) {
      this.#hash = createHash('sha256');
    }
  }

  get bytes(): number {
    return this.#bytes;
  }

  digestHex(): string {
    if (!this.#hash) {
      throw new Error('hashing is disabled');
    }
    if (!this.#finalized || !this.#digest) {
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
    this.#hash?.update(chunk);
    callback(null, chunk);
  }

  override _flush(callback: TransformCallback): void {
    if (this.#hash) {
      this.#digest = this.#hash.digest('hex');
    }
    this.#finalized = true;
    callback();
  }
}

export class ByteLimit extends Transform {
  #bytes = 0;

  constructor(
    readonly maxBytes: number,
    readonly code: FlowErrorCode,
    readonly label: string,
  ) {
    super();
    if (!Number.isInteger(maxBytes) || maxBytes <= 0) {
      throw new RangeError(`${label} limit must be a positive integer`);
    }
  }

  get bytes(): number {
    return this.#bytes;
  }

  override _transform(
    chunk: Buffer,
    _encoding: BufferEncoding,
    callback: TransformCallback,
  ): void {
    this.#bytes += chunk.length;
    if (this.#bytes > this.maxBytes) {
      callback(
        new FlowError(
          this.code,
          `${this.label} bytes exceed ${this.maxBytes}`,
        ),
      );
      return;
    }
    callback(null, chunk);
  }
}

export class ExpandedLimit extends ByteLimit {
  constructor(maxBytes: number) {
    super(maxBytes, 'EXPANDED_LIMIT', 'expanded');
  }
}

export interface DecoderStats {
  readonly inspected: number;
}

export class FlowEventDecoder extends Transform {
  #pending = Buffer.alloc(0);
  #line = 1;
  #inspected = 0;

  constructor(
    readonly maxLineBytes: number,
    readonly maxEvents: number,
    readonly eventLimits: EventLimits,
  ) {
    super({ readableObjectMode: true });
    if (!Number.isInteger(maxLineBytes) || maxLineBytes <= 0) {
      throw new RangeError('maxLineBytes must be a positive integer');
    }
    if (!Number.isInteger(maxEvents) || maxEvents <= 0) {
      throw new RangeError('maxEvents must be a positive integer');
    }
  }

  get stats(): DecoderStats {
    return { inspected: this.#inspected };
  }

  #decodeUtf8(bytes: Buffer): string {
    try {
      return new TextDecoder('utf-8', { fatal: true }).decode(bytes);
    } catch (error) {
      throw new FlowError(
        'DECODE',
        `line ${this.#line}: invalid UTF-8`,
        { cause: error },
      );
    }
  }

  #emitLine(raw: Buffer): void {
    const content = raw.at(-1) === 0x0d ? raw.subarray(0, -1) : raw;
    if (content.length > this.maxLineBytes) {
      throw new FlowError(
        'LINE_LIMIT',
        `line ${this.#line} exceeds ${this.maxLineBytes} bytes`,
      );
    }
    if (content.length === 0) {
      this.#line += 1;
      return;
    }

    const text = this.#decodeUtf8(content);
    let value: unknown;
    try {
      value = JSON.parse(text);
    } catch (error) {
      throw new FlowError(
        'JSON_SYNTAX',
        `line ${this.#line}: invalid JSON`,
        { cause: error },
      );
    }

    let event: FlowEvent;
    try {
      event = parseFlowEvent(value, this.eventLimits);
    } catch (error) {
      throw new FlowError(
        'EVENT_SCHEMA',
        `line ${this.#line}: invalid event`,
        { cause: error },
      );
    }

    this.#inspected += 1;
    if (this.#inspected > this.maxEvents) {
      throw new FlowError(
        'EVENT_LIMIT',
        `event count exceeds ${this.maxEvents}`,
      );
    }
    this.push(event);
    this.#line += 1;
  }

  #consume(chunk: Buffer): void {
    this.#pending = this.#pending.length === 0
      ? Buffer.from(chunk)
      : Buffer.concat([this.#pending, chunk]);

    let newline = this.#pending.indexOf(0x0a);
    while (newline >= 0) {
      this.#emitLine(this.#pending.subarray(0, newline));
      this.#pending = Buffer.from(this.#pending.subarray(newline + 1));
      newline = this.#pending.indexOf(0x0a);
    }

    const possibleCr = this.#pending.at(-1) === 0x0d ? 1 : 0;
    if (this.#pending.length - possibleCr > this.maxLineBytes) {
      throw new FlowError(
        'LINE_LIMIT',
        `line ${this.#line} exceeds ${this.maxLineBytes} bytes`,
      );
    }
  }

  override _transform(
    chunk: Buffer,
    _encoding: BufferEncoding,
    callback: TransformCallback,
  ): void {
    try {
      this.#consume(chunk);
      callback();
    } catch (error) {
      callback(error instanceof Error ? error : new Error(String(error)));
    }
  }

  override _flush(callback: TransformCallback): void {
    try {
      if (this.#pending.length > 0) {
        const final = this.#pending;
        this.#pending = Buffer.alloc(0);
        this.#emitLine(final);
      }
      callback();
    } catch (error) {
      callback(error instanceof Error ? error : new Error(String(error)));
    }
  }
}

export class EventSelector extends Transform {
  #emitted = 0;
  #filtered = 0;

  constructor(readonly kind: string | undefined) {
    super({ readableObjectMode: true, writableObjectMode: true });
  }

  get emitted(): number {
    return this.#emitted;
  }

  get filtered(): number {
    return this.#filtered;
  }

  override _transform(
    event: FlowEvent,
    _encoding: BufferEncoding,
    callback: TransformCallback,
  ): void {
    if (this.kind === undefined || event.kind === this.kind) {
      this.#emitted += 1;
      callback(null, event);
      return;
    }
    this.#filtered += 1;
    callback();
  }
}

export class EventEncoder extends Transform {
  constructor() {
    super({ writableObjectMode: true });
  }

  override _transform(
    event: FlowEvent,
    _encoding: BufferEncoding,
    callback: TransformCallback,
  ): void {
    callback(null, encodeFlowEvent(event));
  }
}
