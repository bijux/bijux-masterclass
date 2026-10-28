import http from 'node:http';

export async function readBoundedBody(
  request: http.IncomingMessage,
  maxBytes: number,
): Promise<Buffer> {
  const chunks: Buffer[] = [];
  let total = 0;
  for await (const chunk of request) {
    const bytes = Buffer.isBuffer(chunk) ? chunk : Buffer.from(chunk);
    total += bytes.byteLength;
    if (total > maxBytes) throw new Error('body too large');
    chunks.push(bytes);
  }
  return Buffer.concat(chunks, total);
}

export function jsonBytes(value: unknown): Buffer {
  return Buffer.from(JSON.stringify(value), 'utf8');
}
