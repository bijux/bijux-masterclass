export function encodeVarint(value: bigint): Uint8Array {
  if (value < 0n) throw new Error("unsigned varint cannot be negative");
  const out: number[] = [];
  let current = value;
  do {
    let byte = Number(current & 0x7fn);
    current >>= 7n;
    if (current !== 0n) byte |= 0x80;
    out.push(byte);
  } while (current !== 0n);
  return Uint8Array.from(out);
}

export function decodeVarint(
  bytes: Uint8Array,
  start = 0,
): { value: bigint; next: number } {
  let result = 0n;
  let shift = 0n;
  let index = start;
  for (; index < bytes.length && index < start + 10; index += 1) {
    const byte = bytes[index];
    if (byte === undefined) break;
    result |= BigInt(byte & 0x7f) << shift;
    if ((byte & 0x80) === 0) return { value: result, next: index + 1 };
    shift += 7n;
  }
  throw new Error("invalid or truncated varint");
}

export function encodeStringField(tag: number, value: string): Uint8Array {
  const data = new TextEncoder().encode(value);
  return concat(
    encodeVarint(BigInt((tag << 3) | 2)),
    encodeVarint(BigInt(data.length)),
    data,
  );
}

export function encodeInt64Field(tag: number, value: bigint): Uint8Array {
  if (value < 0n) throw new Error("course field expects non-negative int64");
  return concat(encodeVarint(BigInt(tag << 3)), encodeVarint(value));
}

export function concat(...parts: Uint8Array[]): Uint8Array {
  const size = parts.reduce((sum, part) => sum + part.length, 0);
  const out = new Uint8Array(size);
  let offset = 0;
  for (const part of parts) {
    out.set(part, offset);
    offset += part.length;
  }
  return out;
}
