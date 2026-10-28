import { createHash } from 'node:crypto';

export interface AuditOptions {
  readonly maxLineBytes: number;
  readonly maxOutputBytes: number;
  readonly accept: (record: Readonly<Record<string, unknown>>) => boolean;
}

export interface AuditReport {
  readonly inspected: number;
  readonly emitted: number;
  readonly filtered: number;
  readonly sourceSha256: string;
  readonly outputSha256: string;
  readonly output: Buffer;
}

function validatePositiveInteger(value: number, name: string): void {
  if (!Number.isInteger(value) || value <= 0) {
    throw new RangeError(`${name} must be a positive integer`);
  }
}

function canonical(record: Readonly<Record<string, unknown>>): Buffer {
  const sorted = Object.fromEntries(
    Object.entries(record).sort(([left], [right]) => left.localeCompare(right)),
  );
  return Buffer.from(`${JSON.stringify(sorted)}\n`);
}

function decodeLine(
  raw: Buffer,
  line: number,
  maxLineBytes: number,
): Readonly<Record<string, unknown>> | undefined {
  const content = raw.at(-1) === 0x0d ? raw.subarray(0, -1) : raw;
  if (content.length > maxLineBytes) {
    throw new Error(`line ${line} exceeds byte limit`);
  }
  if (content.length === 0) {
    return undefined;
  }

  let text: string;
  try {
    text = new TextDecoder('utf-8', { fatal: true }).decode(content);
  } catch (error) {
    throw new Error(`line ${line}: invalid UTF-8`, { cause: error });
  }

  let value: unknown;
  try {
    value = JSON.parse(text);
  } catch (error) {
    throw new Error(`line ${line}: invalid JSON`, { cause: error });
  }

  if (typeof value !== 'object' || value === null || Array.isArray(value)) {
    throw new Error(`line ${line}: expected object`);
  }
  return value as Readonly<Record<string, unknown>>;
}

async function* decode(
  source: AsyncIterable<Uint8Array>,
  maxLineBytes: number,
): AsyncGenerator<Readonly<Record<string, unknown>>> {
  let pending = Buffer.alloc(0);
  let line = 1;

  for await (const raw of source) {
    const chunk = Buffer.from(raw.buffer, raw.byteOffset, raw.byteLength);
    pending = pending.length === 0
      ? Buffer.from(chunk)
      : Buffer.concat([pending, chunk]);

    let delimiter = pending.indexOf(0x0a);
    while (delimiter >= 0) {
      const value = decodeLine(pending.subarray(0, delimiter), line, maxLineBytes);
      if (value) {
        yield value;
      }
      line += 1;
      pending = Buffer.from(pending.subarray(delimiter + 1));
      delimiter = pending.indexOf(0x0a);
    }

    const possibleCr = pending.at(-1) === 0x0d ? 1 : 0;
    if (pending.length - possibleCr > maxLineBytes) {
      throw new Error(`line ${line} exceeds byte limit`);
    }
  }

  if (pending.length > 0) {
    const value = decodeLine(pending, line, maxLineBytes);
    if (value) {
      yield value;
    }
  }
}

export async function auditPipeline(
  source: AsyncIterable<Uint8Array>,
  options: AuditOptions,
): Promise<AuditReport> {
  validatePositiveInteger(options.maxLineBytes, 'maxLineBytes');
  validatePositiveInteger(options.maxOutputBytes, 'maxOutputBytes');

  const sourceHash = createHash('sha256');
  const outputHash = createHash('sha256');
  const outputParts: Buffer[] = [];
  let outputBytes = 0;
  let inspected = 0;
  let emitted = 0;
  let filtered = 0;

  async function* tapped(): AsyncGenerator<Uint8Array> {
    for await (const chunk of source) {
      sourceHash.update(chunk);
      yield chunk;
    }
  }

  for await (const value of decode(tapped(), options.maxLineBytes)) {
    inspected += 1;
    if (!options.accept(value)) {
      filtered += 1;
      continue;
    }

    const encoded = canonical(value);
    if (outputBytes + encoded.length > options.maxOutputBytes) {
      throw new Error('canonical output exceeds byte limit');
    }
    outputParts.push(encoded);
    outputHash.update(encoded);
    outputBytes += encoded.length;
    emitted += 1;
  }

  if (inspected !== emitted + filtered) {
    throw new Error('record accounting mismatch');
  }

  return {
    inspected,
    emitted,
    filtered,
    sourceSha256: sourceHash.digest('hex'),
    outputSha256: outputHash.digest('hex'),
    output: Buffer.concat(outputParts, outputBytes),
  };
}
