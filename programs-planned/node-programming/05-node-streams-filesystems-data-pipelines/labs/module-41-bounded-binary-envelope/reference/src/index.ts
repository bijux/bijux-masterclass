import { Buffer } from 'node:buffer';

export const HEADER_BYTES = 7;

export interface Envelope {
  readonly version: 1;
  readonly kind: number;
  readonly payload: Buffer;
}

export interface DecodeOptions {
  readonly maxPayloadBytes: number;
  readonly copyPayload?: boolean;
}

function assertNonNegativeInteger(value: number, name: string): void {
  if (!Number.isInteger(value) || value < 0) {
    throw new RangeError(`${name} must be a non-negative integer`);
  }
}

function assertUInt16(value: number): void {
  if (!Number.isInteger(value) || value < 0 || value > 0xffff) {
    throw new RangeError('kind must be an unsigned 16-bit integer');
  }
}

export function encodeEnvelope(
  kind: number,
  payload: Uint8Array,
  maxPayloadBytes: number,
): Buffer {
  assertUInt16(kind);
  assertNonNegativeInteger(maxPayloadBytes, 'maxPayloadBytes');
  if (payload.byteLength > maxPayloadBytes) {
    throw new RangeError('payload exceeds limit');
  }

  const total = HEADER_BYTES + payload.byteLength;
  if (!Number.isSafeInteger(total)) {
    throw new RangeError('envelope size overflow');
  }

  const output = Buffer.alloc(total);
  output[0] = 1;
  output.writeUInt16BE(kind, 1);
  output.writeUInt32BE(payload.byteLength, 3);
  Buffer.from(
    payload.buffer,
    payload.byteOffset,
    payload.byteLength,
  ).copy(output, HEADER_BYTES);
  return output;
}

export function decodeEnvelope(
  input: Uint8Array,
  options: DecodeOptions,
): Envelope {
  assertNonNegativeInteger(options.maxPayloadBytes, 'maxPayloadBytes');
  const bytes = Buffer.from(input.buffer, input.byteOffset, input.byteLength);

  if (bytes.length < HEADER_BYTES) {
    throw new Error('truncated header');
  }
  const version = bytes[0];
  if (version !== 1) {
    throw new Error(`unsupported version ${String(version)}`);
  }

  const kind = bytes.readUInt16BE(1);
  const declaredLength = bytes.readUInt32BE(3);
  if (declaredLength > options.maxPayloadBytes) {
    throw new Error('payload exceeds limit');
  }

  const end = HEADER_BYTES + declaredLength;
  if (end !== bytes.length) {
    throw new Error('declared length does not match envelope');
  }

  const visiblePayload = bytes.subarray(HEADER_BYTES, end);
  return {
    version: 1,
    kind,
    payload: options.copyPayload === false
      ? visiblePayload
      : Buffer.from(visiblePayload),
  };
}
