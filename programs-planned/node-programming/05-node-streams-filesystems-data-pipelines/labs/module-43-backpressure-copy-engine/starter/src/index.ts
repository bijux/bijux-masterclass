import { once } from 'node:events';
import type { Writable } from 'node:stream';
export async function waitForDrain(destination: Writable): Promise<void> { if (destination.writableNeedDrain)
    await once(destination, 'drain'); }
export interface CopyCounts {
    readonly chunks: number;
    readonly bytes: number;
}
export function countChunks(chunks: readonly Uint8Array[]): CopyCounts { return { chunks: chunks.length, bytes: chunks.reduce((n, c) => n + c.byteLength, 0) }; }
