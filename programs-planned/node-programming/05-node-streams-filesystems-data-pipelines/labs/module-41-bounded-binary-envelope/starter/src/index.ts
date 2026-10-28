import { Buffer } from 'node:buffer';
export const HEADER_BYTES = 7;
export interface EnvelopeHeader {
    readonly version: number;
    readonly kind: number;
    readonly length: number;
}
export function copyVisibleBytes(input: Uint8Array): Buffer {
    return Buffer.from(input);
}
export function readHeader(input: Uint8Array): EnvelopeHeader | undefined {
    const bytes = copyVisibleBytes(input);
    if (bytes.length < HEADER_BYTES)
        return undefined;
    return { version: bytes[0] ?? 0, kind: bytes.readUInt16BE(1), length: bytes.readUInt32BE(3) };
}
