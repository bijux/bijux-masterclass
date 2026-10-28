export interface NdjsonOptions {
  readonly maxLineBytes: number;
  readonly allowFinalUnterminated?: boolean;
}

export interface LocatedRecord {
  readonly line: number;
  readonly value: Readonly<Record<string, unknown>>;
}

export type NdjsonErrorCode =
  | 'INVALID_UTF8'
  | 'LINE_TOO_LONG'
  | 'INVALID_JSON'
  | 'NOT_OBJECT'
  | 'UNTERMINATED_LINE';

export class NdjsonError extends Error {
  constructor(
    readonly line: number,
    readonly code: NdjsonErrorCode,
    message: string,
    options?: ErrorOptions,
  ) {
    super(message, options);
    this.name = 'NdjsonError';
  }
}

function validateLimit(maxLineBytes: number): void {
  if (!Number.isInteger(maxLineBytes) || maxLineBytes <= 0) {
    throw new RangeError('maxLineBytes must be a positive integer');
  }
}

function stripCarriageReturn(line: Buffer): Buffer {
  return line.at(-1) === 0x0d ? line.subarray(0, -1) : line;
}

function decodeUtf8(lineBytes: Buffer, line: number): string {
  try {
    return new TextDecoder('utf-8', { fatal: true }).decode(lineBytes);
  } catch (error) {
    throw new NdjsonError(
      line,
      'INVALID_UTF8',
      `line ${line}: invalid UTF-8`,
      { cause: error },
    );
  }
}

function parseRecord(lineBytes: Buffer, line: number): LocatedRecord | undefined {
  const content = stripCarriageReturn(lineBytes);
  if (content.length === 0) {
    return undefined;
  }

  const text = decodeUtf8(content, line);
  let value: unknown;
  try {
    value = JSON.parse(text);
  } catch (error) {
    throw new NdjsonError(
      line,
      'INVALID_JSON',
      `line ${line}: invalid JSON`,
      { cause: error },
    );
  }

  if (typeof value !== 'object' || value === null || Array.isArray(value)) {
    throw new NdjsonError(
      line,
      'NOT_OBJECT',
      `line ${line}: JSON value must be an object`,
    );
  }

  return { line, value: value as Readonly<Record<string, unknown>> };
}

function assertPendingBound(
  pending: Buffer,
  maxLineBytes: number,
  line: number,
): void {
  const possibleCr = pending.at(-1) === 0x0d ? 1 : 0;
  if (pending.length - possibleCr > maxLineBytes) {
    throw new NdjsonError(
      line,
      'LINE_TOO_LONG',
      `line ${line} exceeds byte limit`,
    );
  }
}

export async function* decodeNdjson(
  source: AsyncIterable<Uint8Array>,
  options: NdjsonOptions,
): AsyncGenerator<LocatedRecord> {
  validateLimit(options.maxLineBytes);

  let pending = Buffer.alloc(0);
  let line = 1;

  for await (const input of source) {
    const chunk = Buffer.from(input.buffer, input.byteOffset, input.byteLength);
    pending = pending.length === 0
      ? Buffer.from(chunk)
      : Buffer.concat([pending, chunk]);

    let delimiter = pending.indexOf(0x0a);
    while (delimiter >= 0) {
      const lineBytes = pending.subarray(0, delimiter);
      const contentLength = stripCarriageReturn(lineBytes).length;
      if (contentLength > options.maxLineBytes) {
        throw new NdjsonError(
          line,
          'LINE_TOO_LONG',
          `line ${line} exceeds byte limit`,
        );
      }

      const located = parseRecord(lineBytes, line);
      if (located) {
        yield located;
      }

      line += 1;
      pending = Buffer.from(pending.subarray(delimiter + 1));
      delimiter = pending.indexOf(0x0a);
    }

    assertPendingBound(pending, options.maxLineBytes, line);
  }

  if (pending.length === 0) {
    return;
  }
  if (options.allowFinalUnterminated === false) {
    throw new NdjsonError(
      line,
      'UNTERMINATED_LINE',
      `line ${line} is not newline terminated`,
    );
  }

  const contentLength = stripCarriageReturn(pending).length;
  if (contentLength > options.maxLineBytes) {
    throw new NdjsonError(
      line,
      'LINE_TOO_LONG',
      `line ${line} exceeds byte limit`,
    );
  }

  const located = parseRecord(pending, line);
  if (located) {
    yield located;
  }
}
