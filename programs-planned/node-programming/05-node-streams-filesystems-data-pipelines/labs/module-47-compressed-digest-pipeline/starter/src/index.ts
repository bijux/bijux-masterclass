import { createHash } from 'node:crypto';
export function sha256(bytes: Uint8Array): string { return createHash('sha256').update(bytes).digest('hex'); }
export interface DigestLabel {
    readonly representation: 'source' | 'canonical' | 'compressed';
    readonly algorithm: 'sha256';
    readonly hex: string;
}
