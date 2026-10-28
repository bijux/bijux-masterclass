import type { AddressInfo } from 'node:net';
export function portOf(value: AddressInfo | string): number | undefined { return typeof value === 'string' ? undefined : value.port; }
