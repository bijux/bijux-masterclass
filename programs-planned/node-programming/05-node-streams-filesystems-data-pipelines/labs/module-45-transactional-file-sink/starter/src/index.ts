import { basename, dirname, join } from 'node:path';
export function stagePath(destination: string, token: string): string { return join(dirname(destination), `.${basename(destination)}.${token}.tmp`); }
export interface PublicationState {
    readonly committed: boolean;
    readonly stage: string;
    readonly destination: string;
}
